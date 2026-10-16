"""
Full-size model space for CAD deliverables (opt-in; the engine and its build output are not changed).

The engine composes every sheet in model space at the composition scale SC (1:25 frames side by side): a view block
DET-<sheet>-<id> is inserted there at SC / S, and the paper-level items (view titles, notes, tables) sit at x SC. That
plots correctly, but a 1:100 plan is a quarter of its true size in the DWG. `convert()` rewrites a built DXF so that
model space is full size (1 unit = 1 mm) and the sheets keep their look:

- every DET block is inserted at scale 1 in its own place in model space (one row per sheet, no overlap);
- each sheet's layout gets one locked viewport per view at the view scale 1:S, where the view was on the sheet; the
  layout's viewport onto the old composed sheet is deleted;
- the paper-level items of a sheet move into its layout at 1:1; the no-plot sheet frames (S-SHEET, S-TB-AREA) go;
- line types: PSLTSCALE stays 0 and LTSCALE becomes LTSCALE x ref_scale / SC (CHATAM: 3.75 x 100 / 25 = 15, the
  office value at 1:100); the entities of a view at 1:S get ltscale x S / ref_scale, so every dash plots as before;
- xref paths can be re-pointed for a transmittal (`xref_paths={"X-AR-BG": "xref\\\\file.dwg"}`).

Rule: docs/general/DRAWING_ENGINE.md, "Full-size model space" (user, BANWA2 08/10/2026; CHATAM 16/10/2026: "make 1:1
scale on all cad file"). Check after converting: a known dimension in model space, no two views overlapping, and an
AutoCAD plot of the converted file against the plot of the composition.
"""
from ezdxf import bbox
from ezdxf.math import Matrix44

NO_PLOT_FRAMES = ("S-SHEET", "S-TB-AREA")
VP_LOCKED = 16384


def _sheets(msp):
    """x origin and width of every composed sheet, from its S-SHEET frame, left to right"""
    out = []
    for e in msp.query("LWPOLYLINE"):
        if e.dxf.layer == "S-SHEET":
            xs = [p[0] for p in e.get_points("xy")]
            out.append((min(xs), max(xs) - min(xs)))
    return sorted(out)


def _sheet_of(x, sheets):
    """the last sheet starting at or before x (the gap after a sheet still belongs to it)"""
    cand = [i for i, (x0, w) in enumerate(sheets) if x0 - 1e-6 <= x]
    if not cand or x > sheets[cand[-1]][0] + 2 * sheets[cand[-1]][1]:
        raise ValueError(f"x {x:.0f} is on no composed sheet")
    return cand[-1]


def convert(doc, *, sc=25.0, ref_scale=100.0, pad=1.0, gap=10_000.0, xref_paths=None):
    """rewrite the document in place; returns one record per view (block, layout, scale, full-size extents)"""
    msp = doc.modelspace()
    sheets = _sheets(msp)
    if not sheets:
        raise ValueError("no S-SHEET frames: not an engine composition")
    lts = float(doc.header.get("$LTSCALE", 1.0))
    # layouts by sheet: the viewport each layout had onto its composed sheet
    lay_of = {}
    for name in doc.layouts.names_in_taborder():
        if name == "Model":
            continue
        lay = doc.layouts.get(name)
        for v in list(lay.query("VIEWPORT")):
            if v.dxf.id > 1:
                lay_of[_sheet_of(v.dxf.view_center_point.x, sheets)] = lay
                lay.delete_entity(v)
    views = []
    for e in list(msp):
        if e.dxf.layer in NO_PLOT_FRAMES:
            msp.delete_entity(e)
            continue
        if e.dxftype() == "INSERT":
            x = e.dxf.insert.x
        else:
            ext = bbox.extents([e])
            if not ext.has_data:
                continue
            x = ext.extmin.x
        i = _sheet_of(x, sheets)
        if i not in lay_of:
            raise ValueError(f"sheet {i} has no layout")
        if e.dxftype() == "INSERT" and e.dxf.name.startswith("DET-"):
            views.append((i, e))
            continue
        c = e.copy()                                                  # a paper-level item: into the layout at 1:1
        c.transform(Matrix44.chain(Matrix44.translate(-sheets[i][0], 0, 0), Matrix44.scale(1 / sc, 1 / sc, 1 / sc)))
        lay_of[i].add_entity(c)
        msp.delete_entity(e)
    records = []
    y_row = 0.0
    for i in sorted({i for i, _ in views}):
        row = sorted((e for j, e in views if j == i), key=lambda e: e.dxf.insert.x)
        x_cur, row_h = 0.0, 0.0
        for e in row:
            blk = doc.blocks.get(e.dxf.name)
            be = bbox.extents(blk)
            base = blk.block.dxf.base_point
            xs = e.dxf.xscale
            s = sc / xs                                               # the view scale 1:S
            # where the view was on the sheet (paper mm)
            px0 = (e.dxf.insert.x + (be.extmin.x - base.x) * xs - sheets[i][0]) / sc
            py0 = (e.dxf.insert.y + (be.extmin.y - base.y) * xs) / sc
            w, h = be.size.x / s, be.size.y / s
            # full size in model space, its own place
            q = (x_cur - (be.extmin.x - base.x), y_row - (be.extmin.y - base.y), 0.0)
            e.dxf.insert = q
            e.dxf.xscale = e.dxf.yscale = e.dxf.zscale = 1.0
            k = s / ref_scale
            if abs(k - 1.0) > 1e-9:
                for ent in blk:
                    ent.dxf.ltscale = ent.dxf.get("ltscale", 1.0) * k
            cx, cy = q[0] + be.center.x - base.x, q[1] + be.center.y - base.y
            v = lay_of[i].add_viewport(center=(px0 + w / 2, py0 + h / 2), size=(w + 2 * pad, h + 2 * pad),
                                       view_center_point=(cx, cy), view_height=(h + 2 * pad) * s,
                                       dxfattribs={"layer": "S-VPORT"})
            v.dxf.flags |= VP_LOCKED
            records.append({"block": e.dxf.name, "layout": lay_of[i].name, "scale": round(s, 3),
                            "model_size_mm": (round(be.size.x), round(be.size.y)), "insert": q})
            x_cur += be.size.x + gap
            row_h = max(row_h, be.size.y)
        y_row -= row_h + gap
    for name, path in (xref_paths or {}).items():
        doc.blocks.get(name).block.dxf.xref_path = path
    doc.header["$LTSCALE"] = lts * ref_scale / sc
    doc.header["$PSLTSCALE"] = 0
    doc.header["$INSUNITS"] = 4
    doc.header["$MEASUREMENT"] = 1
    for name in doc.layouts.names_in_taborder():
        if name != "Model":
            dl = doc.layouts.get(name).dxf_layout
            dl.dxf.layout_flags = dl.dxf.get("layout_flags", 0) & ~1          # PSLTSCALE off per layout
    ext = bbox.extents(msp)
    if ext.has_data:
        doc.set_modelspace_vport(height=ext.size.y * 1.1, center=(ext.center.x, ext.center.y))
    return records


def overlaps(doc):
    """pairs of view blocks whose full-size extents overlap in model space (must be none)"""
    boxes = []
    for e in doc.modelspace().query("INSERT"):
        if e.dxf.name.startswith("DET-"):
            ext = bbox.extents([e])
            boxes.append((e.dxf.name, ext.extmin, ext.extmax))
    out = []
    for k, (a, a0, a1) in enumerate(boxes):
        for b, b0, b1 in boxes[k + 1:]:
            if a0.x < b1.x and b0.x < a1.x and a0.y < b1.y and b0.y < a1.y:
                out.append((a, b))
    return out
