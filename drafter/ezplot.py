"""
Plot without AutoCAD: render every paper-space layout of a built DXF to a vector PDF with ezdxf's drawing add-on
(PyMuPDF backend), using the same CTB as the AutoCAD plot (lineweight by colour, greys screened). The DWG and the
block library (one file per detail block) are written with the ODA File Converter when it is installed; without
it the library is written as DXF and no DWG is made.

AutoCAD's plot stays the reference for an issued set: this renderer is close but not identical (see README,
"Plotting without AutoCAD").

plot() exits with code 1 when a font of a text style does not resolve to its TrueType file (ezdxf would draw the
text in a substitute font) or a sheet is empty.
"""
import sys
from pathlib import Path

import ezdxf
import pymupdf
from ezdxf import xref
from ezdxf.addons import acadctb, odafc
from ezdxf.addons.drawing import Frontend, RenderContext, config, layout
from ezdxf.addons.drawing.pymupdf import PyMuPdfBackend
from ezdxf.fonts import fonts
from ezdxf.math import BoundingBox2d

A3 = (420.0, 297.0)


def _fix_hatch_transform():
    """ezdxf 1.4 scales and rotates a hatch pattern on transform by the NEW absolute pattern scale and angle
    instead of by the change: in a block inserted at 2.5, an AR-SAND hatch at scale 0.15 gets its pattern lines
    x 0.375 instead of x 2.5 - 6.7 x too dense, millions of strokes (slab-on-ground sheets 1126 - 1128). The
    renderer explodes every INSERT through this transform. Patched here, for rendering only: the DXF is right.
    Fixed upstream after 1.4.4 (ezdxf issues #1391, #1399, #1402): the patch is applied only when the installed
    ezdxf still has the bug, so a fixed release keeps its own (better) transform."""
    from ezdxf.entities.polygon import DXFPolygon
    from ezdxf.math import Matrix44
    orig = DXFPolygon.transform
    if getattr(orig, "drafter_fix", False):
        return
    probe = ezdxf.new().modelspace().add_hatch()        # ANSI31 at 0.5, scaled x 2: lines must double
    probe.paths.add_polyline_path([(0, 0), (1, 0), (1, 1)])
    probe.set_pattern_fill("ANSI31", scale=0.5)
    y0 = probe.pattern.lines[0].offset.y
    probe.transform(Matrix44.scale(2, 2, 2))
    if abs(probe.pattern.lines[0].offset.y - 2 * y0) < 1e-9:
        return                                         # this ezdxf transforms patterns correctly

    def transform(self, m):
        if not self.pattern or not self.dxf.pattern_scale:
            return orig(self, m)
        s0, a0, lines = self.dxf.pattern_scale, self.dxf.pattern_angle, self.pattern.as_list()
        orig(self, m)                                  # boundary, OCS, new scale / angle (pattern lines wrong)
        self.pattern.clear()
        for line in lines:
            self.pattern.add_line(*line)
        self.pattern.scale(self.dxf.pattern_scale / s0, self.dxf.pattern_angle - a0)   # by the change only
        return self

    transform.drafter_fix = True
    DXFPolygon.transform = transform


_fix_hatch_transform()
CONFIG = config.Configuration(background_policy=config.BackgroundPolicy.WHITE,
                              color_policy=config.ColorPolicy.COLOR,
                              lineweight_policy=config.LineweightPolicy.ABSOLUTE)


def render_ctb(ctb):
    """ezdxf takes the pen colour from the CTB but ignores screening: a colour screened s % plots as the grey
    that s % of black gives on white paper (50 % -> 128), every other colour black"""
    out = acadctb.ColorDependentPlotStyles()
    for aci in range(1, 256):
        out[aci].lineweight = ctb[aci].lineweight
        g = round(255 * (1 - ctb[aci].screen / 100))
        out[aci].color = (g, g, g)
    out.lineweights = ctb.lineweights
    return out


def font_problems(doc):
    """text styles whose TrueType file ezdxf cannot find (it would substitute another font)"""
    bad = []
    for st in doc.styles:
        f = st.dxf.get("font", "")
        if f.lower().endswith(".ttf") and fonts.resolve_font_face(f).filename.lower() != f.lower():   # as the renderer
            bad.append(f"{st.dxf.name}: {f}")
    return bad


def paper(lay):
    w, h = lay.dxf.get("paper_width", 0), lay.dxf.get("paper_height", 0)
    return (w, h) if w > 0 and h > 0 else A3


def plot(dxf, layouts, ctb, *, wblocks=(), lib=None):
    """Render each layout to one page of <dxf dir>/<base>.pdf at 1:1; DWG and library through ODA when installed.
    ctb: the plot's ColorDependentPlotStyles (pens by colour, screens)."""
    dxf = Path(dxf)
    pdf, dwg = dxf.with_suffix(".pdf"), dxf.with_suffix(".dwg")
    doc = ezdxf.readfile(dxf)
    for d in doc.entitydb.values():               # a dimension with blank text (" ") has no text midpoint;
        if d.dxftype() == "DIMENSION" and not d.dxf.hasattr("text_midpoint"):   # ezdxf's renderer needs one
            d.dxf.text_midpoint = d.dxf.defpoint  # (in memory only: AutoCAD accepts the DXF as it is)
    problems = [f"font not found, would be substituted - {b}" for b in font_problems(doc)]
    if problems:
        for p in problems:
            print("  !!", p)
        sys.exit(f"!! plot of {dxf.name} failed: install the fonts first")
    for p in [pdf, dwg]:
        if p.exists():
            try:
                p.unlink()
            except PermissionError:
                sys.exit(f"!! {p} is open in another program - close it and plot again")

    pens = render_ctb(ctb)
    merged = pymupdf.open()
    for name in layouts:
        lay = doc.layouts.get(name)
        ctx = RenderContext(doc, ctb=pens, export_mode=True)    # export mode: layers set not to plot stay hidden
        ctx.set_current_layout(lay, ctb=pens)
        be = PyMuPdfBackend()
        Frontend(ctx, be, config=CONFIG).draw_layout(lay, finalize=True)
        w, h = paper(lay)
        page = layout.Page(w, h, layout.Units.mm)
        data = be.get_pdf_bytes(page, settings=layout.Settings(fit_page=False, scale=1),
                                render_box=BoundingBox2d([(0, 0), (w, h)]))   # paper space 0,0 = sheet corner
        with pymupdf.open("pdf", data) as d:
            if not d[0].get_drawings():
                problems.append(f"sheet {name} is empty")
            merged.insert_pdf(d)
    merged.save(pdf)
    msg = f"pages {merged.page_count} -> {pdf} | ezdxf {ezdxf.__version__} (no AutoCAD)"

    if odafc.is_installed():
        odafc.export_dwg(doc, dwg, version="R2018", replace=True)
        msg += f" | dwg exists: {dwg.exists()}"
    else:
        msg += " | no DWG: ODA File Converter not installed"
    if wblocks:
        Path(lib).mkdir(exist_ok=True)
        for b in wblocks:
            for old in (Path(lib) / f"{b}.dwg", Path(lib) / f"{b}.dxf"):
                if old.exists():
                    old.unlink()             # never leave a DWG from an earlier AutoCAD plot beside a newer DXF
            blk = doc.blocks.get(b)
            part = xref.write_block(list(blk), origin=blk.block.dxf.base_point)   # like WBLOCK: base point = origin
            if odafc.is_installed():
                odafc.export_dwg(part, Path(lib) / f"{b}.dwg", version="R2018", replace=True)
            else:
                part.saveas(Path(lib) / f"{b}.dxf")
        msg += f" | library {len(wblocks)} {'DWG' if odafc.is_installed() else 'DXF'}"
    print(msg)
    for p in problems:
        print("  !!", p)
    if problems:
        sys.exit(f"!! plot of {dxf.name} finished with {len(problems)} problem(s)")
