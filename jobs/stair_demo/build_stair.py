"""
Stair ST-1 - typical single-flight stair, A3 reinforcement drawing (demonstration, Rev A).

Engine            : copied from jobs/nooker_rw/build_rw.py (same pens, text, dimension style, annotation engine).
Drafting standard : EIT 011006-19 + office conventions (DRAWING_STANDARD_EIT-011006-19.md section 19)
Model space       : 1 unit = 1 mm, full size. Paper: one A3 layout, scaled locked viewports.

usage: python build_stair.py <out_dir>      -> <out_dir>/STR-ST_Stair_ST-1_A3_RevA.dxf
"""
import math
import sys
from pathlib import Path

import ezdxf
from ezdxf import bbox
from ezdxf.path import make_path
from ezdxf.enums import TextEntityAlignment as TA, MTextEntityAlignment as MA

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
DXF = OUT / "STR-ST_Stair_ST-1_A3_RevA.dxf"

# --------------------------------------------------------------------------- project data
PROJ = dict(
    code="STR",
    owner="[ OWNER NAME ]",
    project="TYPICAL SINGLE-FLIGHT STAIR ST-1",
    location="[ BUILDING / LOCATION ]",
    office="[ DESIGN OFFICE NAME ]",
    office2="[ ADDRESS / TEL. / E-MAIL ]",
    date="28/09/2026",
    stage="D", rev="A",
)
SHEETS = [("5101", ["STAIR ST-1", "SECTIONS & REINFORCEMENT"], "AS SHOWN")]
AN_B = r"\fArial Narrow|b1|i0|c0|p34;"   # MTEXT inline bold Arial Narrow


def dwg_no(series):
    return f"{PROJ['code']}-ST-{series}-{PROJ['stage']}-{PROJ['rev']}"


def hdr(s):
    """MTEXT paragraph header: bold, 2.8 mm."""
    return "{" + AN_B + r"\H2.8;" + s + "}"


# --------------------------------------------------------------------------- document setup
doc = ezdxf.new("R2018", setup=False, units=4)
doc.header["$MEASUREMENT"] = 1
doc.header["$LTSCALE"] = 1.0
doc.header["$PSLTSCALE"] = 1
doc.header["$LWDISPLAY"] = 1
doc.header["$CELTSCALE"] = 1.0
doc.header["$TEXTSTYLE"] = "AN"
doc.header["$PLINEGEN"] = 1        # dash pattern runs continuously along polylines

# family name as well: AutoCAD resolves a TrueType font through the Windows font registry, where the file name
# differs between installs (ARIALN.TTF / ARIALN_0.TTF); without it, it substitutes an SHX font
doc.styles.add("AN", font="ARIALN.TTF").set_extended_font_data(family="Arial Narrow")
doc.styles.add("ANB", font="ARIALNB.TTF").set_extended_font_data(family="Arial Narrow", bold=True)

# EIT linetypes, dash lengths in plotted mm. Own names (EIT_*) so an acadiso.lin reload can never
# overwrite them. Hidden periods kept <= 4.5 mm so short hidden edges still read as dashed.
for name, pat, desc in [
    ("EIT_CENTER", [8.5, -1.4, 1.4, -1.4], "EIT centre / cutting plane ____ . ____ ."),
    ("EIT_PHANTOM", [7.0, -1.4, 1.4, -1.4, 1.4, -1.4], "EIT property line ____ . . ____"),
    ("EIT_HIDDEN", [3.0, -1.5], "EIT hidden (below slab / below ground) -- -- --"),
    ("EIT_HIDDEN_FINE", [1.5, -0.75], "EIT hidden fine - - - - -"),
]:
    doc.linetypes.add(name, pattern=[sum(abs(x) for x in pat)] + pat, description=desc)

# name, ACI colour, lineweight (1/100 mm), linetype, plot
# Pens: EIT Table 2.3 A2 values used unreduced (sheets are A3 originals, not reductions), plus
# cut-concrete emphasis (0.35 cut / 0.25 seen). ACI 8 = secondary info, plotted 50 % grey by NRW-EIT.ctb.
GREY = 8
LAYERS = [
    ("S-FRAME", 7, 70, "Continuous", True),
    ("S-TTLB", 7, 35, "Continuous", True),
    ("S-TTLB-THIN", GREY, 18, "Continuous", True),
    ("S-ZONE", GREY, 18, "Continuous", True),
    ("S-TEXT", 7, 18, "Continuous", True),
    ("S-TITLE", 7, 35, "Continuous", True),
    ("S-DIMS", 2, 18, "Continuous", True),
    ("S-ANNO", 3, 18, "Continuous", True),
    ("S-SYMB", 3, 25, "Continuous", True),
    ("S-CONC", 4, 35, "Continuous", True),            # concrete CUT (sections, plan sections)
    ("S-CONC-VIS", 4, 25, "Continuous", True),        # concrete SEEN (plan, elevation)
    ("S-CONC-HIDN", GREY, 25, "EIT_HIDDEN", True),
    ("S-CONC-JNT", GREY, 18, "Continuous", True),     # chamfer arris
    ("S-CJOINT", 7, 25, "Continuous", True),          # construction joint zig-zag
    ("S-LEAN", 7, 18, "Continuous", True),
    ("S-SOIL", 32, 25, "Continuous", True),
    ("S-EXCV", GREY, 25, "EIT_HIDDEN", True),         # excavation line (temporary cut)
    ("S-HATCH", GREY, 13, "Continuous", True),
    ("S-PROP", 6, 25, "EIT_PHANTOM", True),
    ("S-CUTL", 6, 25, "EIT_CENTER", True),
    ("S-BREAK", GREY, 18, "Continuous", True),
    ("S-REBR", 1, 50, "Continuous", True),            # main reinforcement
    ("S-REBR-SEC", 30, 35, "Continuous", True),       # secondary (DB10) / stirrup class
    ("S-DWL", 1, 50, "Continuous", True),
    ("S-DWL-SLV", GREY, 18, "Continuous", True),
    ("S-DRAIN", 5, 25, "Continuous", True),
    ("S-DRAIN-HIDN", GREY, 25, "EIT_HIDDEN", True),
    ("S-GEOT", 3, 18, "EIT_HIDDEN_FINE", True),
    ("S-JOINT", 6, 25, "Continuous", True),
    ("S-JFILL", GREY, 18, "Continuous", True),
    ("S-SURCH", 3, 18, "Continuous", True),
    ("S-VPORT", GREY, 13, "Continuous", False),
]
LAYER_LW = {n: lw for n, c, lw, lt, plot in LAYERS}
for n, c, lw, lt, plot in LAYERS:
    lay = doc.layers.add(n, color=c, linetype=lt)
    lay.dxf.lineweight = lw
    lay.dxf.plot = 1 if plot else 0


def dimstyle(name, scale):
    ds = doc.dimstyles.new(name)
    d = ds.dxf
    d.dimscale = scale
    d.dimtxt = 2.0
    d.dimtsz = 0.0          # arrowheads, not ticks
    d.dimblk = ""           # "" = closed filled arrowhead
    d.dimasz = 2.0          # arrowhead length 2.0 mm (plotted)
    d.dimexe = 2.0          # extension beyond dim line (~2 mm, EIT 3.2.2)
    d.dimexo = 1.0          # small gap from object
    d.dimgap = 0.6
    d.dimtad = 1
    d.dimtih = 0            # text aligned with dim line
    d.dimtoh = 0
    d.dimdec = 0
    d.dimtxsty = "AN"
    d.dimlwd = 18
    d.dimlwe = 18
    d.dimclrd = 2
    d.dimclre = 8           # extension lines grey (ACI 8 -> 50 % screened by NRW-EIT.ctb), like grid lines
    d.dimclrt = 7
    d.dimtofl = 1
    d.dimatfit = 3
    d.dimtmove = 1          # narrow space: text outside with leader-less move (EIT Fig 3.8)
    d.dimdli = 5.0
    d.dimzin = 8
    return name


DS = {s: dimstyle(f"EIT-{s}", s) for s in (1, 2, 5, 10, 20, 25, 50, 100)}

msp = doc.modelspace()


# --------------------------------------------------------------------------- drawing helpers
def A(layer, **kw):
    kw["layer"] = layer
    return kw


def pline(sp, pts, layer, close=False):
    e = sp.add_lwpolyline(pts, close=close, dxfattribs=A(layer))
    e.dxf.flags = e.dxf.flags | 128          # PLINEGEN: continuous linetype across vertices
    return e


def line(sp, p1, p2, layer):
    return sp.add_line(p1, p2, dxfattribs=A(layer))


def text(sp, s, p, h, layer="S-TEXT", align=TA.BOTTOM_LEFT, rot=0, style="AN"):
    t = sp.add_text(s, height=h, rotation=rot, dxfattribs=A(layer, style=style))
    t.set_placement(p, align=align)
    return t


def mtext(sp, s, p, h, width, layer="S-TEXT", attach=MA.TOP_LEFT, style="AN", spacing=1.0):
    m = sp.add_mtext(s, dxfattribs=A(layer, style=style, char_height=h, width=width))
    m.dxf.line_spacing_factor = spacing
    m.set_location(insert=p, attachment_point=attach)
    return m


# hatch pattern scale per 1 mm of plotted spacing and per unit view scale
# (ezdxf ISO pattern set: ANSI31 pitch 3.175, EARTH ~6.35, GRAVEL ~25)
PAT_K = {"ANSI31": 1 / 3.175, "EARTH": 1 / 6.35, "GRAVEL": 1 / 5.0, "AR-CONC": 0.005, "AR-SAND": 1 / 40.0}


def pscale(pattern, S, paper_mm):
    """pattern scale giving ~paper_mm plotted pitch in a 1:S view"""
    return PAT_K[pattern] * S * paper_mm


def hatch(sp, pts, pattern, scale, layer="S-HATCH", angle=0.0, islands=()):
    h = sp.add_hatch(color=256, dxfattribs=A(layer))
    h.paths.add_polyline_path(pts, is_closed=True, flags=1)
    for isl in islands:
        h.paths.add_polyline_path(isl, is_closed=True, flags=16)   # BOUNDARY_PATH_OUTERMOST = island
    if pattern == "SOLID":
        h.set_solid_fill(color=256)
    else:
        h.set_pattern_fill(pattern, scale=scale, angle=angle, color=256)
    return h


def circle_pts(c, r, n=32):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def dot(sp, c, r, layer="S-REBR"):
    h = sp.add_hatch(color=256, dxfattribs=A(layer))
    ep = h.paths.add_edge_path()
    ep.add_arc(c, r, 0, 360)
    h.set_solid_fill(color=256)
    sp.add_circle(c, r, dxfattribs=A(layer))


def arrowhead(sp, tip, frm, size, layer="S-ANNO"):
    dx, dy = tip[0] - frm[0], tip[1] - frm[1]
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    bx, by = tip[0] - ux * size, tip[1] - uy * size
    w = size * 0.3
    sp.add_solid([tip, (bx - uy * w, by + ux * w), (bx + uy * w, by - ux * w)], dxfattribs=A(layer))


# --------------------------------------------------------------------------- annotation engine
# See ANNOTATION_ALIGNMENT_GUIDE.md. Views register notes with leader(); capture() then lays them out:
#  * COLUMN mode (sides "L"/"R"): all notes of a side share one knee x, so text edges align on one line
#    (L = right-justified, R = left-justified). Notes are stacked top-down in the order of their targets,
#    at a uniform pitch, as close as possible to their target height, avoiding reserved y-bands.
#  * ROW mode (sides "T"/"B"): notes share one knee y above / below the view, ordered by target x.
#  * One straight leader segment + 3 mm horizontal shelf. Crossing leaders are swapped.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))    # repository root: shared drafter package
from drafter.fonts import text_w, wrap                           # noqa: E402  widths from the Arial Narrow TTFs


TXT_H = 2.0            # note text height, paper mm
PITCH = TXT_H * 5 / 3  # MTEXT line pitch at spacing factor 1.0
SHELF = 3.0            # horizontal shelf, paper mm
TGAP = 1.0             # shelf end -> text / bubble
BUB_R = 2.0            # bar-mark bubble radius (4 mm dia)
NGAP = 1.6             # clear gap between stacked notes, paper mm
ARROW = 2.0            # filled leader arrowhead length, paper mm
RING_K = 2.0           # open-circle terminator: Ø = 2 x drawn bar diameter (bars cut in section)
RISE = 3.0             # preferred rise of a note above its target -> every leader gets an inclined leg
LEG_ANGLES = (45.0, 60.0)   # inclined leg angles (from horizontal), in order of preference
HLINE_CLEAR = 1.5      # a leader's horizontal run keeps this clear of horizontal drawing lines (paper mm)
_HSEGS = []            # horizontal drawing segments of the current view: (x0, x1, y)
_SOLIDS = []           # solid-filled regions of the view: ("p", pts) polygons / ("c", cx, cy, r) circles
_BARS = []             # bar / dowel centre-line segments: (x0, y0, x1, y1, half plotted pen mm)
EDGE_GAP = 0.05        # arrow tip stops this far outside a filled object's edge (paper mm)

_NOTES = None
_CFG = {}
_BOXES = []          # true note text boxes (ezdxf under-measures multi-line MTEXT)


def note_cfg(**kw):
    """per-view layout settings (model units): xL / xR = knee x of the columns, yT / yB = knee y of rows,
    avoidL / avoidR = list of (y0, y1) bands the notes must not occupy; free=True draws notes as given."""
    _CFG.update(kw)


def leader(sp, tip, knee, s, S, side="R", width=48, layer="S-ANNO", dot_tip=False, mark=None, ring=0, fixed=False):
    """ring=db: bar cut in section -> open circle of 2 x the drawn bar diameter round the bar dot.
    fixed=True: drawn at the given knee (not packed), but after the view is collected so the edge rule applies."""
    n = dict(sp=sp, tip=tip, knee=knee, s=s, S=S, side=side, width=width, layer=layer,
             dot=dot_tip and not ring, mark=mark, ring=ring, fixed=fixed or _CFG.get("free", False))
    if _NOTES is None:
        n["lines"] = wrap(s, TXT_H, width - (2 * BUB_R + TGAP if mark else 0))
        _draw_note(n, knee)
    else:
        _NOTES.append(n)


def leader_path(tip, knee, S, angles=LEG_ANGLES, xmin=None):
    """target -> inclined leg at a standard angle (45 / 60 deg) -> horizontal run -> knee.
    Falls back to one straight line only if no standard leg fits (steeper than 60 deg)."""
    tx, ty = tip
    kx, ky = knee
    dx, dy = kx - tx, ky - ty
    if abs(dy) < 0.3 * S or abs(dx) < 0.3 * S:
        return [tip, knee]
    for a in angles:
        run = abs(dy) / math.tan(math.radians(a))
        if run <= abs(dx) - 1.0 * S:
            lx = tx + math.copysign(run, dx)
            if xmin is not None and lx < xmin:
                continue
            return [tip, (lx, ky), knee]
    return [tip, knee]


def _pip(x, y, pts):
    inside = False
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def _seg_d(x, y, x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((x - x0) * dx + (y - y0) * dy) / L2))
    return math.hypot(x - x0 - t * dx, y - y0 - t * dy)


def _in_filled(q, S):
    x, y = q
    for f in _SOLIDS:
        if f[0] == "c":
            if math.hypot(x - f[1], y - f[2]) <= f[3]:
                return True
        elif _pip(x, y, f[1]):
            return True
    for x0, y0, x1, y1, hw in _BARS:
        if _seg_d(x, y, x0, y0, x1, y1) <= hw * S:
            return True
    return False


def edge_tip(tip, toward, S):
    """slide an arrow tip along the leader until it sits just outside the filled object it touches,
    so the arrowhead never disappears into a black bar, strip or sealant fill"""
    if not _in_filled(tip, S):
        return tip
    dx, dy = toward[0] - tip[0], toward[1] - tip[1]
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    t, step = 0.0, 0.02 * S
    while t < 10 * S and _in_filled((tip[0] + ux * t, tip[1] + uy * t), S):
        t += step
    t += EDGE_GAP * S
    return (tip[0] + ux * t, tip[1] + uy * t)


def _path_of(n, knee):
    row = n["side"] in ("T", "B")
    sgn = -1 if n["side"] == "L" else 1
    if (knee[0] - n["tip"][0]) * sgn < 0:          # run would double back over the text -> direct leg
        return [n["tip"], knee]
    return leader_path(n["tip"], knee, n["S"], angles=(60.0, 45.0) if row else LEG_ANGLES,
                       xmin=n.get("xmin"))


def _draw_note(n, knee):
    sp, S, side = n["sp"], n["S"], n["side"]
    h = TXT_H * S
    sgn = -1 if side == "L" else 1
    kx, ky = knee
    ex = kx + sgn * SHELF * S
    path = _path_of(n, knee)
    tip = n["tip"]
    if n["ring"]:                                     # open circle, leader starts on its edge
        rr = RING_K * rdot(n["ring"], S)
        sp.add_circle(tip, rr, dxfattribs=A(n["layer"]))
        dx, dy = path[1][0] - tip[0], path[1][1] - tip[1]
        L = math.hypot(dx, dy) or 1.0
        tip = (tip[0] + dx / L * rr, tip[1] + dy / L * rr)
    if not n["ring"] and not n["dot"]:
        tip = edge_tip(tip, path[1], S)
    pline(sp, [tip] + path[1:] + [(ex, ky)], n["layer"])
    if n["dot"]:
        dot(sp, tip, 0.35 * S, n["layer"])
    elif not n["ring"]:
        arrowhead(sp, tip, path[1], ARROW * S, n["layer"])
    tx = ex + sgn * TGAP * S
    if n["mark"]:
        cx = tx + sgn * BUB_R * S
        sp.add_circle((cx, ky), BUB_R * S, dxfattribs=A("S-SYMB"))
        text(sp, str(n["mark"]), (cx, ky), (TXT_H if len(str(n["mark"])) < 2 else 1.7) * S, "S-TEXT",
             TA.MIDDLE_CENTER, style="ANB")
        tx = cx + sgn * (BUB_R + TGAP) * S
    body = "\\P".join(n["lines"])
    if side == "T":          # text grows upward; leader on the line nearest the view (last line)
        att, ty = MA.BOTTOM_LEFT, ky - h / 2
    elif side == "L":
        att, ty = MA.TOP_RIGHT, ky + h / 2
    else:                    # R and B: leader on the first line
        att, ty = MA.TOP_LEFT, ky + h / 2
    wmax = max(text_w(l, TXT_H) for l in n["lines"]) * 1.04 + 0.5      # box = measured lines, no re-wrap
    mtext(sp, body, (tx, ty), h, wmax * S, attach=att)
    hbox = (len(n["lines"]) - 1) * PITCH * S + h
    x0, x1 = (tx - wmax * S, tx) if side == "L" else (tx, tx + wmax * S)
    y1 = ty + hbox if side == "T" else ty
    _BOXES.append((min(x0, kx), y1 - hbox - 0.6 * S, max(x1, kx), y1))


def _pack(lens, desired, bands=(), item_bands=None):
    """1-D packing along u (increasing). Items keep their order and are shifted as little as possible
    from their desired start (cluster averaging), then pushed out of reserved bands."""
    blocks = []
    for i in range(len(lens)):
        blocks.append([desired[i], [i]])
        while len(blocks) > 1:
            (s0, ids0), (s1, ids1) = blocks[-2], blocks[-1]
            if s0 + sum(lens[k] for k in ids0) <= s1:
                break
            ids = ids0 + ids1
            cum, acc = [], 0.0
            for k in ids:
                cum.append(acc)
                acc += lens[k]
            blocks[-2:] = [[sum(desired[k] - c for k, c in zip(ids, cum)) / len(ids), ids]]
    starts = [0.0] * len(lens)
    for st, ids in blocks:
        acc = st
        for k in ids:
            starts[k] = acc
            acc += lens[k]
    prev_end = -1e18
    for k in range(len(lens)):
        u = max(starts[k], prev_end)
        moved = True
        while moved:
            moved = False
            for b0, b1 in bands:
                if u < b1 and u + lens[k] > b0:
                    u = b1
                    moved = True
            for b0, b1 in (item_bands[k] if item_bands else ()):
                if b0 < u < b1:                       # start (= leader run) inside a forbidden strip
                    u = b1
                    moved = True
        starts[k] = u
        prev_end = u + lens[k]
    return starts


def _cross(p1, p2, q1, q2):
    def o(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (o(p1, p2, q1) * o(p1, p2, q2) < 0) and (o(q1, q2, p1) * o(q1, q2, p2) < 0)


def _layout_notes():
    by = {}
    for n in _NOTES:
        if n["fixed"]:
            n["lines"] = wrap(n["s"], TXT_H, n["width"] - (2 * BUB_R + TGAP if n["mark"] else 0))
            _draw_note(n, n["knee"])
            continue
        by.setdefault(n["side"], []).append(n)
    for side, ns in by.items():
        S = ns[0]["S"]
        for n in ns:
            n["lines"] = wrap(n["s"], TXT_H, n["width"] - (2 * BUB_R + TGAP if n["mark"] else 0))
        if side in ("L", "R"):
            kx = _CFG.get("x" + side, (min if side == "L" else max)(n["knee"][0] for n in ns))
            lens = [(len(n["lines"]) * PITCH + NGAP) * S for n in ns]
            bands = [(-b1, -b0) for b0, b1 in _CFG.get("avoid" + side, [])]      # u = -y

            def run_bands(k):
                """forbidden starts u so the horizontal run never lies on a horizontal drawing line"""
                tx, ty = ns[k]["tip"]
                a, b = min(tx, kx), max(tx, kx)
                d = HLINE_CLEAR * S
                out = []
                for x0, x1, yl in _HSEGS:
                    if x1 > a + 0.5 * S and x0 < b - 0.5 * S:
                        out.append((-(yl + d) - 0.5 * PITCH * S, -(yl - d) - 0.5 * PITCH * S))
                return sorted(out)

            RB = {k: run_bands(k) for k in range(len(ns))}

            def place(order):
                des = [-(ns[k]["tip"][1] + RISE * S + 0.5 * PITCH * S) for k in order]
                st = _pack([lens[k] for k in order], des, bands, [RB[k] for k in order])
                res = {k: (kx, -u - 0.5 * PITCH * S) for k, u in zip(order, st)}
                lo = min(y - (len(ns[k]["lines"]) - 0.5) * PITCH * S for k, (x, y) in res.items())
                hi = max(y + 0.5 * PITCH * S for x, y in res.values())
                dy = 0.0
                if "ymin" + side in _CFG and lo < _CFG["ymin" + side]:
                    dy = _CFG["ymin" + side] - lo
                if "ymax" + side in _CFG and hi + dy > _CFG["ymax" + side]:
                    dy = _CFG["ymax" + side] - hi
                return {k: (x, y + dy) for k, (x, y) in res.items()}
            order = sorted(range(len(ns)), key=lambda k: -ns[k]["tip"][1])
        else:
            ky = _CFG.get("y" + side, (max if side == "T" else min)(n["knee"][1] for n in ns))
            lens = [(SHELF + TGAP + (2 * BUB_R + TGAP if n["mark"] else 0) + 3.0) * S
                    + max(text_w(l, TXT_H) for l in n["lines"]) * S for n in ns]

            def place(order):
                des = [ns[k]["tip"][0] + abs(ky - ns[k]["tip"][1]) * 0.577 for k in order]   # 60 deg leg
                st = _pack([lens[k] for k in order], des)
                xmax = _CFG.get("xmax" + side)
                if xmax is not None and st:                 # keep the row inside the view width
                    over = st[-1] + lens[order[-1]] - xmax
                    if over > 0:
                        st = [u - over for u in st]
                res = {k: (u, ky) for k, u in zip(order, st)}
                prev_end = -1e18
                for k in order:                       # a leg must not end under the left neighbour's text
                    ns[k]["xmin"] = prev_end
                    prev_end = res[k][0] + lens[k]
                return res
            order = sorted(range(len(ns)), key=lambda k: ns[k]["tip"][0])
        pos = place(order)
        for _ in range(3 * len(ns)):
            swapped = False
            for a in range(len(order) - 1):
                i, j = order[a], order[a + 1]
                pi, pj = _path_of(ns[i], pos[i]), _path_of(ns[j], pos[j])
                if any(_cross(pi[a1], pi[a1 + 1], pj[b1], pj[b1 + 1])
                       for a1 in range(len(pi) - 1) for b1 in range(len(pj) - 1)):
                    order[a], order[a + 1] = j, i
                    pos = place(order)
                    swapped = True
            if not swapped:
                break
        for k, n in enumerate(ns):
            _draw_note(n, pos[k])


# --------------------------------------------------------------------------- reinforcement drawing
def rdot(db, S):
    """bar-in-section dot radius: true size, but never below 1.1 mm plotted diameter"""
    return max(db / 2, 0.55 * S)


def bar(sp, pts, db, layer="S-REBR"):
    """Bar on its centreline; every bend filleted at the centreline radius 3.5 db
    (inside bend dia 6 db, ACI 318-19 Table 25.3.1 / EIT 1008-38; EIT 011006-19 Table 3.2 item 1)."""
    R = 3.5 * db
    out = [(pts[0][0], pts[0][1], 0.0)]
    for i in range(1, len(pts) - 1):
        p0, p1, p2 = pts[i - 1], pts[i], pts[i + 1]
        ux, uy = p1[0] - p0[0], p1[1] - p0[1]
        lu = math.hypot(ux, uy)
        vx, vy = p2[0] - p1[0], p2[1] - p1[1]
        lv = math.hypot(vx, vy)
        ux, uy, vx, vy = ux / lu, uy / lu, vx / lv, vy / lv
        th = math.acos(max(-1.0, min(1.0, ux * vx + uy * vy)))
        if th < 1e-6:
            out.append((p1[0], p1[1], 0.0))
            continue
        t = min(R * math.tan(th / 2), 0.5 * lu, 0.5 * lv)
        sgn = 1 if ux * vy - uy * vx > 0 else -1
        out.append((p1[0] - ux * t, p1[1] - uy * t, sgn * math.tan(th / 4)))
        out.append((p1[0] + vx * t, p1[1] + vy * t, 0.0))
    out.append((pts[-1][0], pts[-1][1], 0.0))
    e = sp.add_lwpolyline(out, format="xyb", dxfattribs=A(layer))
    e.dxf.flags = e.dxf.flags | 128
    return e


def strip(sp, p1, p2, db, layer="S-REBR"):
    """straight bar along its length at true width (1:5 and larger), solid"""
    (x1, y1), (x2, y2) = p1, p2
    L = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / L * db / 2, (x2 - x1) / L * db / 2
    pts = [(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)]
    hatch(sp, pts, "SOLID", 1, layer=layer)
    pline(sp, pts, layer, close=True)


def zigzag(sp, p1, p2, S, layer="S-CJOINT", amp=0.8, pitch=2.0):
    """construction joint symbol: zig-zag (roughened / keyed surface) between p1 and p2,
    amplitude and tooth pitch in paper mm"""
    (x1, y1), (x2, y2) = p1, p2
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -uy, ux
    n = max(2, int(round(L / (pitch * S))))
    step = L / n
    pts = [p1]
    for i in range(n):
        t = (i + 0.5) * step
        a = amp * S * (1 if i % 2 == 0 else -1)
        pts.append((x1 + ux * t + nx * a, y1 + uy * t + ny * a))
    pts.append(p2)
    pline(sp, pts, layer)


def dowel_end(sp, c, r, layer="S-DWL"):
    """plain round bar seen end-on: open circle with cross (distinct from filled deformed-bar dots)"""
    sp.add_circle(c, r, dxfattribs=A(layer))
    line(sp, (c[0] - r, c[1]), (c[0] + r, c[1]), layer)
    line(sp, (c[0], c[1] - r), (c[0], c[1] + r), layer)


def dist_line(sp, p1, p2, cross_pt, S, layer="S-ANNO"):
    """EIT Table 3.2 item 4: thin distribution line with 45 deg end ticks and a circle where it
    crosses the one representative (very thick) bar of the set."""
    line(sp, p1, p2, layer)
    (x1, y1), (x2, y2) = p1, p2
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    a = 1.0 * S
    for (px, py) in (p1, p2):
        line(sp, (px - (ux - uy) * a * 0.7, py - (uy + ux) * a * 0.7),
             (px + (ux - uy) * a * 0.7, py + (uy + ux) * a * 0.7), layer)
    sp.add_circle(cross_pt, 1.0 * S, dxfattribs=A(layer))


def level(sp, x, y, value, desc, S, ext=(-6, 30)):
    """EIT Fig 3.12 datum triangle (open, apex on line) with value above the line."""
    line(sp, (x + ext[0] * S, y), (x + ext[1] * S, y), "S-ANNO")
    tri = [(x, y), (x - 1.2 * S, y + 2.0 * S), (x + 1.2 * S, y + 2.0 * S)]
    pline(sp, tri, "S-ANNO", close=True)
    lab = f"{value}  {desc}" if desc else value
    text(sp, lab, (x + 2.0 * S, y + 0.6 * S), 2.0 * S, "S-TEXT")


def dim(sp, p1, p2, base, S, angle=0, override=None, text="<>"):
    d = sp.add_linear_dim(base=base, p1=p1, p2=p2, angle=angle, dimstyle=DS[S], text=text,
                          override=override or {}, dxfattribs=A("S-DIMS"))
    d.render()
    return d


def zbreak(sp, p1, p2, S, layer="S-BREAK"):
    """EIT break line: straight with a single Z in the middle (Table 2.3)."""
    x1, y1 = p1
    x2, y2 = p2
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -uy, ux
    m = L / 2
    a = 1.5 * S
    pts = [p1,
           (x1 + ux * (m - a), y1 + uy * (m - a)),
           (x1 + ux * (m - a / 2) + nx * a * 1.5, y1 + uy * (m - a / 2) + ny * a * 1.5),
           (x1 + ux * (m + a / 2) - nx * a * 1.5, y1 + uy * (m + a / 2) - ny * a * 1.5),
           (x1 + ux * (m + a), y1 + uy * (m + a)),
           p2]
    pline(sp, pts, layer)


def earth_band(sp, pts_line, depth, S, below=True):
    """Thin earth-hatch band under (or above) a ground polyline."""
    sgn = -1 if below else 1
    poly = list(pts_line) + [(x, y + sgn * depth) for x, y in reversed(pts_line)]
    hatch(sp, poly, "EARTH", pscale("EARTH", S, 1.6), angle=45)


def capture(fn, *args):
    """Run a view builder, return model extents of everything it created (plus margin)."""
    global _NOTES
    before = {e.dxf.handle for e in msp}
    _NOTES = []
    _CFG.clear()
    _BOXES.clear()
    fn(*args)
    _HSEGS.clear()
    _SOLIDS.clear()
    _BARS.clear()
    for e in msp:
        if e.dxf.handle in before:
            continue
        if e.dxftype() == "HATCH" and e.dxf.solid_fill:
            for pth in e.paths:
                if hasattr(pth, "vertices"):
                    _SOLIDS.append(("p", [(v[0], v[1]) for v in pth.vertices]))
                else:
                    for ed in pth.edges:
                        if ed.EDGE_TYPE == "ArcEdge":
                            _SOLIDS.append(("c", ed.center.x, ed.center.y, ed.radius))
            continue
        if e.dxf.layer in ("S-REBR", "S-REBR-SEC", "S-DWL") and e.dxftype() in ("LINE", "LWPOLYLINE"):
            hw = LAYER_LW[e.dxf.layer] / 200.0
            pts = [(v.x, v.y) for v in make_path(e).flattening(1.0)]
            for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
                _BARS.append((x0, y0, x1, y1, hw))
        if e.dxf.layer in ("S-HATCH", "S-VPORT"):
            continue
        if e.dxftype() == "LINE":
            (x0, y0), (x1, y1) = (e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y)
            if abs(y1 - y0) < 1e-6 and abs(x1 - x0) > 1e-6:
                _HSEGS.append((min(x0, x1), max(x0, x1), y0))
        elif e.dxftype() == "LWPOLYLINE":
            pts = list(e.get_points("xyb"))
            if e.closed:
                pts.append(pts[0])
            for (x0, y0, b), (x1, y1, _) in zip(pts[:-1], pts[1:]):
                if b == 0 and abs(y1 - y0) < 1e-6 and abs(x1 - x0) > 1e-6:
                    _HSEGS.append((min(x0, x1), max(x0, x1), y0))
    _layout_notes()
    _NOTES = None
    new = [e for e in msp if e.dxf.handle not in before]
    ext = bbox.extents(new)
    x0, y0, x1, y1 = ext.extmin.x, ext.extmin.y, ext.extmax.x, ext.extmax.y
    for a, b, c, d in _BOXES:
        x0, y0, x1, y1 = min(x0, a), min(y0, b), max(x1, c), max(y1, d)
    return (x0, y0, x1, y1)

# ======================================================================= STAIR ST-1 geometry (mm)
# Single flight, waist slab 150 normal to soffit, spanning between beam B1 (lower floor) and B2 (upper floor).
# x = horizontal along the flight (0 = face of B1 = first riser), y = level (0 = FFL lower floor), z = across.
NR = 10                     # risers
RH = 170                    # riser height
TG = 250                    # going (tread)
WS = 150                    # waist, normal to soffit
WID = 1200                  # flight width
C_SL = 20                   # clear cover, stair and slab
TANT = RH / TG
CO, SI = math.cos(math.atan(TANT)), math.sin(math.atan(TANT))
XTOP = (NR - 1) * TG        # 2250 = last riser = face of B2
FFL1 = NR * RH              # 1700
B1X0, B1X1, B1YB = -200, 0, -400                 # B1 200x400, top = +-0.000
B2X0, B2X1, B2YB = XTOP, XTOP + 200, FFL1 - 500  # B2 200x500, top = +1.700
HS = 120                    # floor slab (by others)
XL, XR = -900, XTOP + 900   # break lines of Section A-A
XBB = 375                   # Section B-B cut (mid tread 2)
LTOP = 700                  # top bars: 700 horizontal beyond beam face (>= 0.3 Ln = 675)
HOOK = 150                  # hook leg (>= 12 db = 144)
XE1 = B1X0 + 50             # bar ends 50 from far face of B1
XE2 = B2X1 - 70             # ... and of B2 (clear of the slab bottom bars)
D1 = C_SL + 6               # (1) centre, normal distance above soffit
D2 = C_SL + 6               # (2)/(3) centre, normal distance below the step-root line
D4 = C_SL + 12 + 5          # (4) true centre distance (inside the main bars)


def y_root(x):              # line through the step roots (inner corners)
    return TANT * x


def y_soff(x):
    return TANT * x - WS / CO


def y_bot(x, d):            # parallel to soffit, d above it (normal)
    return y_soff(x) + d / CO


def y_top(x, d):            # parallel to the root line, d below it (normal)
    return y_root(x) - d / CO


def s_list(first, last, step=200):
    out, s = [], first
    while s <= last + 1e-6:
        out.append(s)
        s += step
    return out


SLOPE_L = XTOP / CO                                              # 2721 soffit length between beam faces
S4B = s_list(100, SLOPE_L - 100)                                 # (4) bottom, along slope from B1 face
S4T1 = s_list(100, LTOP / CO - 40)                               # (4) under (2)
S4T2 = [SLOPE_L - s for s in s_list(100, LTOP / CO - 40)]        # (4) under (3)
N_ACROSS = len(range(100, WID, 200))                             # 6 bars across the flight @200

doc.layers.add("S-CUTL-END", color=7, linetype="Continuous").dxf.lineweight = 50
LAYER_LW["S-CUTL-END"] = 50


def cutmark(sp, p1, p2, look, label, S, ref=None):
    """cutting plane: chain line, 0.50 end strokes, arrows toward the viewing direction, letters"""
    (x1, y1), (x2, y2) = p1, p2
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    line(sp, p1, p2, "S-CUTL")
    for (px, py), sg in ((p1, 1), (p2, -1)):
        line(sp, (px, py), (px + ux * sg * 5 * S, py + uy * sg * 5 * S), "S-CUTL-END")
        tip = (px + look[0] * 5 * S, py + look[1] * 5 * S)
        line(sp, (px, py), tip, "S-SYMB")
        arrowhead(sp, tip, (px, py), 2.0 * S, "S-SYMB")
        text(sp, label, (px - ux * sg * 2.6 * S, py - uy * sg * 2.6 * S), 2.8 * S, "S-TEXT", TA.MIDDLE_CENTER,
             style="ANB")
    if ref:
        text(sp, ref, (x2 - ux * 2.6 * S, y2 - uy * 2.6 * S - 3.2 * S), 2.0 * S, "S-TEXT", TA.MIDDLE_CENTER)


def beam_cage(sp, P, x0, x1, yb, yt, S):
    """beam by others, shown for context: RB6 stirrup + 4-DB16 corner bars (secondary pen)"""
    c = 30 + 3
    xm = (x0 + x1) / 2
    bar(sp, [P(xm, yt - c), P(x1 - c, yt - c), P(x1 - c, yb + c), P(x0 + c, yb + c), P(x0 + c, yt - c),
             P(xm + 20, yt - c)], 6, "S-REBR-SEC")
    for x in (x0 + 44, x1 - 44):
        for y in (yb + 44, yt - 44):
            dot(sp, P(x, y), rdot(16, S), "S-REBR-SEC")


# ======================================================================= SECTION A-A (1:20)
def section_aa(ox, oy):
    S = 20
    sp = msp
    P = lambda x, y: (ox + x, oy + y)

    top = [P(XL, 0), P(0, 0)]
    for i in range(NR - 1):
        top += [P(i * TG, (i + 1) * RH), P((i + 1) * TG, (i + 1) * RH)]
    top += [P(XTOP, FFL1), P(XR, FFL1)]
    pline(sp, top, "S-CONC")
    bot = [P(XR, FFL1 - HS), P(B2X1, FFL1 - HS), P(B2X1, B2YB), P(B2X0, B2YB), P(XTOP, y_soff(XTOP)),
           P(0, y_soff(0)), P(0, B1YB), P(B1X0, B1YB), P(B1X0, -HS), P(XL, -HS)]
    pline(sp, bot, "S-CONC")
    zbreak(sp, P(XL, -HS - 60), P(XL, 60), S)
    zbreak(sp, P(XR, FFL1 - HS - 60), P(XR, FFL1 + 60), S)

    # ---- beams and floor slabs by others (context, secondary pen)
    beam_cage(sp, P, B1X0, B1X1, B1YB, 0, S)
    beam_cage(sp, P, B2X0, B2X1, B2YB, FFL1, S)
    bar(sp, [P(XL, -25), P(-60, -25), P(-60, -125)], 10, "S-REBR-SEC")
    line(sp, P(XL, -HS + 25), P(B1X0 + 50, -HS + 25), "S-REBR-SEC")
    bar(sp, [P(XR, FFL1 - 25), P(B2X0 + 60, FFL1 - 25), P(B2X0 + 60, FFL1 - 125)], 10, "S-REBR-SEC")
    line(sp, P(XR, FFL1 - HS + 25), P(B2X1 - 150, FFL1 - HS + 25), "S-REBR-SEC")

    # ---- stair reinforcement (centrelines, bends R = 3.5 db)
    bar(sp, [P(XE1, y_bot(XE1, D1)), P(XE2, y_bot(XE2, D1))], 12)                                     # (1)
    bar(sp, [P(LTOP, y_top(LTOP, D2)), P(XE1, y_top(XE1, D2)), P(XE1, y_top(XE1, D2) - HOOK)], 12)    # (2)
    x3 = XTOP - LTOP
    bar(sp, [P(x3, y_top(x3, D2)), P(XE2, y_top(XE2, D2)), P(XE2, y_top(XE2, D2) - HOOK)], 12)        # (3)
    # (4) cut: drawn 0.4 S clear of the main bar line (true position D4 is too close to show at 1:20)
    r10 = rdot(10, S)
    dd = D1 + r10 + LAYER_LW["S-REBR"] / 200 * S + 0.4 * S
    for s in S4B:
        x = s * CO
        dot(sp, P(x, y_bot(x, dd)), r10, "S-REBR-SEC")
    for s in S4T1 + S4T2:
        x = s * CO
        dot(sp, P(x, y_top(x, dd)), r10, "S-REBR-SEC")

    # ---- dimensions
    yd = B1YB - 160
    dim(sp, P(B1X0, B1YB), P(0, B1YB), P(0, yd), S)
    dim(sp, P(0, B1YB), P(XTOP, B2YB), P(0, yd), S, override={"dimpost": "<> CLEAR"})
    dim(sp, P(XTOP, B2YB), P(B2X1, B2YB), P(0, yd), S)
    dim(sp, P(B1X0, B1YB), P(B2X1, B2YB), P(0, yd - 120), S)
    i = 5                                                                   # typical step
    dim(sp, P(i * TG, i * RH), P((i + 1) * TG, (i + 1) * RH), P(0, (i + 1) * RH + 90), S,
        override={"dimpost": "<> TYP."})
    dim(sp, P((i + 1) * TG, i * RH), P((i + 1) * TG, (i + 1) * RH), P(i * TG + 170, 0), S, angle=90)
    xw = 1250                                                               # waist, normal to soffit
    p1 = P(xw, y_soff(xw))
    p2 = (p1[0] - SI * WS, p1[1] + CO * WS)
    d = sp.add_aligned_dim(p1=p1, p2=p2, distance=-6 * S, dimstyle=DS[S], dxfattribs=A("S-DIMS"))
    d.render()
    level(sp, -650, P(0, 0)[1], "±0.000", "FFL", S, ext=(-3, 3))
    level(sp, XTOP + 480, P(0, FFL1)[1], "+1.700", "FFL", S, ext=(-3, 3))

    # ---- member tags (beams cut)
    for x, y, a, t in ((B1X0 - 30, -300, TA.MIDDLE_RIGHT, ("B1  200x400", "SEE BEAM SCHEDULE")),
                       (B2X1 + 40, B2YB + 130, TA.MIDDLE_LEFT, ("B2  200x500", "SEE BEAM SCHEDULE"))):
        text(sp, t[0], P(x, y + 30), 2.0 * S, align=a, style="ANB")
        text(sp, t[1], P(x, y - 30), 2.0 * S, align=a)
    text(sp, "FLOOR SLAB (BY OTHERS)", P(XL + 20, -HS - 30), 2.0 * S, align=TA.TOP_LEFT)
    text(sp, "FLOOR SLAB (BY OTHERS)", P(XR - 20, FFL1 - HS - 30), 2.0 * S, align=TA.TOP_RIGHT)

    # ---- notes: left column = lower support (above the lower floor), bottom row = soffit (under the flight),
    #      upper support = fixed note in the free space above the steps
    note_cfg(xL=P(-110, 0)[0], yB=P(0, -140)[1], yminL=P(0, 90)[1], xmaxB=P(XTOP - 80, 0)[0])
    kl, kb = P(-110, 0), P(0, -140)
    leader(sp, P(350, y_top(350, D2)), kl, "DB12@200 TOP, 700 BEYOND FACE OF B1, HOOKED 150 INTO B1", S, "L", 50,
           mark=2)
    x4 = S4T1[1] * CO
    leader(sp, P(x4, y_top(x4, dd)), kl, "DB10@200 DIST. UNDER (2) & (3)", S, "L", 50, mark=4, ring=10)
    x4 = S4B[1] * CO
    leader(sp, P(x4, y_bot(x4, dd)), kb, "DB10@200 DIST. ON (1)", S, "B", 36, mark=4, ring=10)
    leader(sp, P(700, y_bot(700, D1)), kb, "DB12@200 BOTTOM MAIN, 150 INTO B1 & B2, NO LAPS", S, "B", 44, mark=1)
    leader(sp, P(2150, y_top(2150, D2)), P(1700, 1660), "DB12@200 TOP, 700 BEYOND FACE OF B2, HOOKED 150 INTO B2",
           S, "L", 50, mark=3, fixed=True)


# ======================================================================= SECTION B-B (1:10)
def section_bb(ox, oy):
    S = 10
    sp = msp
    P = lambda u, y: (ox + u, oy + y)
    ys = y_soff(XBB)
    yt = (int(XBB // TG) + 1) * RH
    pline(sp, [P(0, ys), P(WID, ys), P(WID, yt), P(0, yt)], "S-CONC", close=True)
    us = list(range(100, WID, 200))
    r12 = rdot(12, S)
    for u in us:
        dot(sp, P(u, y_bot(XBB, D1)), r12)                     # (1)
        dot(sp, P(u, y_top(XBB, D2)), r12)                     # (2)
    e = C_SL + 5
    line(sp, P(e, y_bot(XBB, D4)), P(WID - e, y_bot(XBB, D4)), "S-REBR-SEC")      # (4)
    line(sp, P(e, y_top(XBB, D4)), P(WID - e, y_top(XBB, D4)), "S-REBR-SEC")
    yd = ys - 90
    yb1 = y_bot(XBB, D1)
    dim(sp, P(0, ys), P(us[0], yb1), P(0, yd), S)
    dim(sp, P(us[0], yb1), P(us[-1], yb1), P(0, yd), S,
        text=f"{len(us) - 1} @ 200 = {us[-1] - us[0]}")
    dim(sp, P(us[-1], yb1), P(WID, ys), P(0, yd), S)
    dim(sp, P(0, ys), P(WID, ys), P(0, yd - 70), S, override={"dimpost": "<> FLIGHT WIDTH"})
    note_cfg(xR=P(WID + 110, 0)[0])
    kr = P(WID + 110, 0)
    leader(sp, P(us[-1], y_top(XBB, D2)), kr, "DB12@200 TOP", S, "R", 30, mark=2, ring=12)
    leader(sp, P(WID - 60, y_top(XBB, D4)), kr, "DB10@200 DIST.", S, "R", 30, mark=4)
    leader(sp, P(WID - 60, y_bot(XBB, D4)), kr, "DB10@200 DIST.", S, "R", 30, mark=4)
    leader(sp, P(us[-1], yb1), kr, "DB12@200 BOTTOM", S, "R", 30, mark=1, ring=12)
    text(sp, "TREAD 2", P(WID / 2, yt + 25), 2.0 * S, align=TA.BOTTOM_CENTER)


# ======================================================================= PLAN (1:50)
def plan_st(ox, oy):
    S = 50
    sp = msp
    note_cfg(free=True)
    P = lambda x, z: (ox + x, oy + z)
    XLp, XRp = -700, XTOP + 700
    for z in (0, WID):
        line(sp, P(XLp, z), P(XRp, z), "S-CONC-VIS")
    for i in range(NR):
        line(sp, P(i * TG, 0), P(i * TG, WID), "S-CONC-VIS")
        text(sp, str(i + 1), P(i * TG + 45, WID - 110), 2.0 * S, align=TA.MIDDLE_LEFT)
    for x in (B1X0, B2X1):
        line(sp, P(x, 0), P(x, WID), "S-CONC-HIDN")
    zbreak(sp, P(XLp, -150), P(XLp, WID + 150), S)
    zbreak(sp, P(XRp, -150), P(XRp, WID + 150), S)
    # walking line, UP from the first riser
    zc = WID / 2 + 100
    sp.add_circle(P(TG / 2, zc), 0.8 * S, dxfattribs=A("S-ANNO"))
    line(sp, P(TG / 2 + 0.8 * S, zc), P(XTOP - 60, zc), "S-ANNO")
    arrowhead(sp, P(XTOP - 30, zc), P(XTOP - 200, zc), 2.5 * S, "S-ANNO")
    text(sp, "UP", P(2 * TG + 60, zc + 60), 2.8 * S, align=TA.BOTTOM_LEFT, style="ANB")
    text(sp, "FFL ±0.000", P((XLp + B1X0) / 2, WID + 80), 2.0 * S, align=TA.BOTTOM_CENTER)
    text(sp, "FFL +1.700", P((XRp + B2X1) / 2, WID + 80), 2.0 * S, align=TA.BOTTOM_CENTER)
    text(sp, "B1 (BELOW)", P(B1X0 - 40, WID / 2), 2.0 * S, align=TA.MIDDLE_CENTER, rot=90)
    text(sp, "B2 (BELOW)", P(B2X1 + 60, WID / 2), 2.0 * S, align=TA.MIDDLE_CENTER, rot=90)
    # cutting planes
    cutmark(sp, P(XLp - 250, 250), P(XRp + 250, 250), (0, 1), "A", S)
    cutmark(sp, P(XBB, -300), P(XBB, WID + 300), (1, 0), "B", S)
    # dimensions
    zd = -650
    dim(sp, P(B1X0, 0), P(0, 0), P(0, zd), S)
    dim(sp, P(0, 0), P(XTOP, 0), P(0, zd), S, text=f"{NR - 1} @ {TG} = {XTOP}")
    dim(sp, P(XTOP, 0), P(B2X1, 0), P(0, zd), S)
    dim(sp, P(XRp, 0), P(XRp, WID), P(XRp + 350, 0), S, angle=90)


# ======================================================================= place model views
EXT = {
    "AA": capture(section_aa, 0, 0),
    "BB": capture(section_bb, 0, -3000),
    "PL": capture(plan_st, 0, 6000),
}

# ======================================================================= paper space
W, H = 420.0, 297.0
FX0, FY0, FX1, FY1 = 20.0, 10.0, 410.0, 287.0      # frame (EIT A2-A4: 10, left 20)
TBW = 70.0                                           # title strip width (EIT 100 mm x 0.7 for A3)
TBX = FX1 - TBW                                      # 340
PAD = 2.0


def frame_and_zones(ps):
    pline(ps, [(FX0, FY0), (FX1, FY0), (FX1, FY1), (FX0, FY1)], "S-FRAME", close=True)
    nx, ny = 8, 6
    dx, dy = (FX1 - FX0) / nx, (FY1 - FY0) / ny
    for i in range(nx + 1):
        x = FX0 + i * dx
        line(ps, (x, FY1), (x, FY1 + 4), "S-ZONE")
        line(ps, (x, FY0), (x, FY0 - 4), "S-ZONE")
        if i < nx:
            text(ps, str(i + 1), (x + dx / 2, FY1 + 4), 2.0, "S-ZONE", TA.MIDDLE_CENTER)
            text(ps, str(i + 1), (x + dx / 2, FY0 - 4), 2.0, "S-ZONE", TA.MIDDLE_CENTER)
    for j in range(ny + 1):
        y = FY1 - j * dy
        line(ps, (FX0 - 4, y), (FX0, y), "S-ZONE")
        line(ps, (FX1, y), (FX1 + 4, y), "S-ZONE")
        if j < ny:
            lab = "ABCDEF"[j]
            text(ps, lab, (FX0 - 4, y - dy / 2), 2.0, "S-ZONE", TA.MIDDLE_CENTER)
            text(ps, lab, (FX1 + 4, y - dy / 2), 2.0, "S-ZONE", TA.MIDDLE_CENTER)
    # trim / centring marks
    for x in (W / 2,):
        line(ps, (x, 0), (x, 3), "S-ZONE")
        line(ps, (x, H), (x, H - 3), "S-ZONE")


def title_block(ps, series, title_lines, scale_txt, sheet_i):
    x0, x1 = TBX, FX1
    xc = (x0 + x1) / 2
    tx = x0 + 1.5
    line(ps, (x0, FY0), (x0, FY1), "S-TTLB")

    def hline(yy, lay="S-TTLB"):
        line(ps, (x0, yy), (x1, yy), lay)

    y_app = FY0 + 7
    y_des = y_app + 32
    y_tit = y_des + 20
    y_off = y_tit + 18
    y_prj = y_off + 20
    y_own = y_prj + 14
    for yy in (y_app, y_des, y_tit, y_off, y_prj, y_own):
        hline(yy)
    text(ps, "APPROVED BY : ..........................   DATE : ............", (tx, FY0 + 3.5), 2.0, align=TA.MIDDLE_LEFT)
    xm = x0 + 35
    line(ps, (xm, y_app), (xm, y_des), "S-TTLB")
    ly = y_des - 3.5
    for lab in ["DESIGNED : ......................", "DRAWN : ...........................",
                "CHECKED : .......................", "ENGINEER : .......................",
                "COE LICENSE NO. : ..............", "SIGNATURE : ....................."]:
        text(ps, lab, (tx, ly), 2.0, align=TA.MIDDLE_LEFT)
        ly -= 4.8
    text(ps, "DRAWING NO.", (xm + 1.5, y_des - 3.5), 2.0, align=TA.MIDDLE_LEFT)
    text(ps, dwg_no(series), (xm + 1.5, y_des - 8.5), 2.8, align=TA.MIDDLE_LEFT, style="ANB")
    text(ps, f"SHEET {sheet_i} OF {len(SHEETS)}  |  A3", (xm + 1.5, y_des - 13.5), 2.0, align=TA.MIDDLE_LEFT)
    line(ps, (xm, y_app + 13), (x1, y_app + 13), "S-TTLB-THIN")
    line(ps, (xm + 14, y_app), (xm + 14, y_app + 13), "S-TTLB-THIN")
    text(ps, "SCALE", (xm + 1.5, y_app + 10), 2.0, align=TA.MIDDLE_LEFT)
    text(ps, scale_txt, (xm + 1.5, y_app + 4.5), 2.0, align=TA.MIDDLE_LEFT, style="ANB")
    text(ps, "DATE", (xm + 15.5, y_app + 10), 2.0, align=TA.MIDDLE_LEFT)
    text(ps, PROJ["date"], (xm + 15.5, y_app + 4.5), 2.0, align=TA.MIDDLE_LEFT)
    text(ps, "DRAWING TITLE", (tx, y_tit - 3), 2.0, align=TA.MIDDLE_LEFT)
    yy = y_tit - 9
    for tl in title_lines:
        text(ps, tl, (xc, yy), 2.8, align=TA.MIDDLE_CENTER, style="ANB")
        yy -= 4.3
    text(ps, "STRUCTURAL DESIGN OFFICE", (tx, y_off - 3), 2.0, align=TA.MIDDLE_LEFT)
    text(ps, PROJ["office"], (xc, y_off - 9), 2.8, align=TA.MIDDLE_CENTER)
    text(ps, PROJ["office2"], (xc, y_off - 14.5), 2.0, align=TA.MIDDLE_CENTER)
    text(ps, "PROJECT", (tx, y_prj - 3), 2.0, align=TA.MIDDLE_LEFT)
    text(ps, PROJ["project"], (xc, y_prj - 9), 2.8, align=TA.MIDDLE_CENTER, style="ANB")
    text(ps, PROJ["location"], (xc, y_prj - 15), 1.8, align=TA.MIDDLE_CENTER)
    text(ps, "OWNER", (tx, y_own - 3), 2.0, align=TA.MIDDLE_LEFT)
    text(ps, PROJ["owner"], (xc, y_own - 9), 2.8, align=TA.MIDDLE_CENTER)

    y_auth = y_own + 20
    y_cli = y_auth + 16
    hline(y_auth)
    hline(y_cli)
    text(ps, "LOCAL AUTHORITY (BUILDING CONTROL)", (tx, y_auth - 3), 2.0, align=TA.MIDDLE_LEFT, style="ANB")
    text(ps, "PERMIT NO. : ...................................", (tx, y_auth - 8), 2.0, align=TA.MIDDLE_LEFT)
    text(ps, "[ STAMP ]", (xc, y_auth - 15), 2.0, align=TA.MIDDLE_CENTER)
    text(ps, "OWNER / CLIENT APPROVAL", (tx, y_cli - 3), 2.0, align=TA.MIDDLE_LEFT, style="ANB")
    text(ps, "SIGNATURE : ...................................", (tx, y_cli - 8), 2.0, align=TA.MIDDLE_LEFT)
    text(ps, "NAME : ......................  DATE : ..........", (tx, y_cli - 13), 2.0, align=TA.MIDDLE_LEFT)

    # revision table - EIT 2.2.2.4: above title block, same width, rows >= 5 mm
    rh = 5.0
    nrows = 4
    y_r0 = y_cli
    y_hdr = y_r0 + nrows * rh
    y_rt = y_hdr + rh
    for k in range(nrows + 2):
        line(ps, (x0, y_r0 + k * rh), (x1, y_r0 + k * rh), "S-TTLB-THIN" if 0 < k else "S-TTLB")
    cols = [x0, x0 + 7, x0 + 45, x0 + 60, x1]
    for cx in cols[1:-1]:
        line(ps, (cx, y_r0), (cx, y_rt), "S-TTLB-THIN")
    for cx, lab in zip(cols[:-1], ["REV", "DESCRIPTION", "DATE", "SIGN"]):
        text(ps, lab, (cx + 1, y_hdr + rh / 2), 2.0, align=TA.MIDDLE_LEFT)
    revs = [("A", "ISSUED FOR REVIEW", PROJ["date"])]
    for k, (r, d, dt) in enumerate(revs):
        yy = y_hdr - rh / 2 - k * rh
        text(ps, r, (cols[0] + 1, yy), 2.0, align=TA.MIDDLE_LEFT)
        text(ps, d, (cols[1] + 1, yy), 2.0, align=TA.MIDDLE_LEFT)
        text(ps, dt, (cols[2] + 0.6, yy), 1.9, align=TA.MIDDLE_LEFT)
    text(ps, "REVISIONS", (tx, y_rt + 3), 2.0, align=TA.MIDDLE_LEFT, style="ANB")
    hline(y_rt + 6)

    # key plan - EIT 2.2.2.5
    y_kp0 = y_rt + 6
    y_kp1 = y_kp0 + 32
    hline(y_kp1)
    text(ps, "KEY PLAN (N.T.S.)", (tx, y_kp1 - 3), 2.0, align=TA.MIDDLE_LEFT, style="ANB")
    bx0, by0, bx1, by1 = x0 + 10, y_kp0 + 5, x1 - 10, y_kp1 - 7
    pline(ps, [(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)], "S-TTLB-THIN", close=True)
    pline(ps, [(bx0, by0), (bx1, by0)], "S-FRAME")
    text(ps, "STAIR ST-1 - SEE ARCH. PLANS", (xc, (by0 + by1) / 2 + 2.5), 2.0, align=TA.MIDDLE_CENTER)
    text(ps, "LOCATION / GRIDS BY ARCH.", (xc, (by0 + by1) / 2 - 2.5), 2.0, align=TA.MIDDLE_CENTER)

    # status stamp + sheet notes (text area, EIT 2.2.2.2)
    sy = y_kp1 + 3
    pline(ps, [(x0 + 3, sy), (x1 - 3, sy), (x1 - 3, sy + 12), (x0 + 3, sy + 12)], "S-TITLE", close=True)
    text(ps, "FOR REVIEW", (xc, sy + 8.2), 2.8, align=TA.MIDDLE_CENTER, style="ANB")
    text(ps, "NOT FOR CONSTRUCTION", (xc, sy + 3.8), 2.8, align=TA.MIDDLE_CENTER, style="ANB")
    text(ps, "NOTES", (tx, FY1 - 3.5), 2.0, align=TA.MIDDLE_LEFT, style="ANB")
    notes = ("1. READ WITH THE NOTES ON THIS SHEET.\\P"
             "2. DIMENSIONS IN mm; LEVELS IN m.\\P"
             "3. DO NOT SCALE FROM DRAWINGS.\\P"
             "4. DRAFTING TO EIT 011006-19.")
    mtext(ps, notes, (tx, FY1 - 6.5), 2.0, TBW - 3)


def view_title(ps, x, y, name, scale_txt, bubble, triangles=False, note=None):
    if x is None:                     # align with the left edge of the view just placed
        x = _LASTVP[0] + PAD
    """EIT 2.10: underlined title, scale below, split bubble (ID / sheet) at right end."""
    w = len(name) * 1.86 + 3          # Arial Narrow Bold 2.8 mm caps ~1.8 mm/char (measured on plot)
    text(ps, name, (x, y + 0.9), 2.8, "S-TITLE", style="ANB")
    line(ps, (x, y), (x + w, y), "S-TITLE")
    text(ps, f"SCALE {scale_txt}", (x, y - 1.2), 2.0, align=TA.TOP_LEFT)
    if note:
        text(ps, note, (x, y - 4.6), 2.0, align=TA.TOP_LEFT)
    top, bot = bubble
    r = 4.6
    cx, cy = x + w + r + 1.0, y
    ps.add_circle((cx, cy), r, dxfattribs=A("S-SYMB"))
    line(ps, (cx - r, cy), (cx + r, cy), "S-SYMB")
    text(ps, top, (cx, cy + 2.1), 2.8, "S-TEXT", TA.MIDDLE_CENTER, style="ANB")
    text(ps, bot, (cx, cy - 2.2), 2.0, "S-TEXT", TA.MIDDLE_CENTER)
    if triangles:                     # section bubble "hat" (EIT Fig 2.9)
        for s_ in (-1, 1):
            ps.add_solid([(cx + s_ * r, cy), (cx + s_ * (r + 2.6), cy), (cx + s_ * r * 0.5, cy + r * 0.87)],
                         dxfattribs=A("S-SYMB"))
    return w + 2 * r + 4


_LASTVP = [0, 0, 0, 0]


def viewport(ps, key, scale, px, py_top, center_w=None):
    """Place viewport for model extents EXT[key] with its top-left at (px, py_top). Returns (w, h)."""
    x0, y0, x1, y1 = EXT[key]
    pw = (x1 - x0) / scale + 2 * PAD
    ph = (y1 - y0) / scale + 2 * PAD
    if center_w:
        px = px + (center_w - pw) / 2
    vp = ps.add_viewport(center=(px + pw / 2, py_top - ph / 2), size=(pw, ph),
                         view_center_point=((x0 + x1) / 2, (y0 + y1) / 2), view_height=ph * scale,
                         dxfattribs=A("S-VPORT"))
    vp.dxf.flags = vp.dxf.flags | 16384        # lock display (VSF_LOCK_ZOOM)
    _LASTVP[:] = [px, py_top - ph, pw, ph]
    if px < FX0 - 0.1 or px + pw > TBX + 0.1 or py_top - ph < FY0 - 0.1 or py_top > FY1 + 0.1:
        print(f"  !! viewport {key} outside drawing area: x {px:.0f}-{px + pw:.0f}, y {py_top - ph:.0f}-{py_top:.0f}")
    print(f"  vp {key:5s} 1:{scale:<4} {pw:6.1f} x {ph:6.1f}  at x={px:.0f} y_top={py_top:.0f}")
    return px, pw, ph


def new_sheet(i):
    name, tl, sc = SHEETS[i]
    ps = doc.layouts.new(name)
    ps.page_setup(size=(W, H), margins=(0, 0, 0, 0), units="mm", offset=(0, 0), rotation=0, scale=1,
                  name="ISO_full_bleed_A3_(420.00_x_297.00_MM)", device="DWG To PDF.pc3")
    ps.dxf_layout.dxf.current_style_sheet = "monochrome.ctb"
    frame_and_zones(ps)
    title_block(ps, name, tl, sc, i + 1)
    print(f"sheet {dwg_no(name)}")
    return ps


AREA_W = TBX - FX0          # 320


def notes(items):
    """join note paragraphs; blank string = small gap"""
    return "\\P".join(items)

def table(ps, x, y_top, cols, heads, rows, rh=5.2, bold_first_col=False):
    """simple grid table; cols = list of column x-offsets incl. right edge"""
    xs = [x + c for c in cols]
    nr = len(rows) + 1
    for k in range(nr + 1):
        line(ps, (xs[0], y_top - k * rh), (xs[-1], y_top - k * rh), "S-TTLB-THIN" if 0 < k < nr else "S-TTLB")
    for cx in xs:
        line(ps, (cx, y_top), (cx, y_top - nr * rh), "S-TTLB-THIN")
    for cx, h_ in zip(xs, heads):
        text(ps, h_, (cx + 1.3, y_top - rh / 2), 2.0, align=TA.MIDDLE_LEFT, style="ANB")
    for r, row in enumerate(rows, start=1):
        for i, (cx, v) in enumerate(zip(xs, row)):
            text(ps, v, (cx + 1.3, y_top - r * rh - rh / 2), 2.0, align=TA.MIDDLE_LEFT,
                 style="ANB" if (bold_first_col and i == 0) else "AN")
    return y_top - nr * rh
# ---------------------------------------------------------------- 5101 stair sheet
UW = {10: 0.617, 12: 0.888, 16: 1.578}       # kg/m (TIS 24 nominal mass)


def r5(v):
    return int(5 * round(v / 5))


def bbs_rows():
    """(mark, db, shape, dims[(letter, mm)], no., remark) - one flight, out-to-out dimensions"""
    a1 = (XE2 - XE1) / CO
    a2 = (LTOP - XE1) / CO
    a3 = (XE2 - (XTOP - LTOP)) / CO
    n4 = len(S4B) + len(S4T1) + len(S4T2)
    return [
        ("1", 12, "-", [("A", a1)], N_ACROSS, "BOTTOM"),
        ("2", 12, "J", [("A", a2), ("B", HOOK)], N_ACROSS, "TOP, B1"),
        ("3", 12, "J", [("A", a3), ("B", HOOK)], N_ACROSS, "TOP, B2"),
        ("4", 10, "-", [("A", WID - 2 * C_SL)], n4, f"{len(S4B)} B + {len(S4T1) + len(S4T2)} T"),
    ]


def shape_sketch(ps, kind, x, y, w, h):
    m = 1.2
    x0, x1, y0, y1 = x + m, x + w - m, y - h + m, y - m
    pts = {"-": [(x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2)],
           "J": [(x0, y0 + 0.6), (x1 - 1.0, y1), (x1 - 1.0, y0 + 0.2)]}[kind]
    pline(ps, pts, "S-REBR")


def schedule(ps, x, y_top):
    cols = [0, 9, 18, 29, 52, 58, 67, 76, 91]
    heads = ["MARK", "BAR", "SHAPE", "DIM. (mm)", "NO.", "CUT m", "kg", "REMARKS"]
    rh = 5.6
    text(ps, "BAR SCHEDULE - ONE FLIGHT", (x, y_top + 3), 2.8, "S-TITLE", style="ANB")
    xs = [x + c for c in cols]
    rows = bbs_rows()
    n = len(rows) + 1
    for k in range(n + 1):
        line(ps, (xs[0], y_top - k * rh), (xs[-1], y_top - k * rh), "S-TTLB" if k in (0, 1, n) else "S-TTLB-THIN")
    for cx in xs:
        line(ps, (cx, y_top), (cx, y_top - n * rh), "S-TTLB-THIN")
    for cx, h_ in zip(xs, heads):
        text(ps, h_, (cx + 1.0, y_top - rh / 2), 2.0, align=TA.MIDDLE_LEFT, style="ANB")
    tot = {}
    for r, (mk, db, shp, dims, cnt, rem) in enumerate(rows, start=1):
        yy = y_top - r * rh - rh / 2
        cut = sum(v for _, v in dims) / 1000
        wt = cut * cnt * UW[db]
        tot[db] = tot.get(db, 0) + wt
        ps.add_circle((xs[0] + 4.5, yy), 2.0, dxfattribs=A("S-SYMB"))
        text(ps, mk, (xs[0] + 4.5, yy), 2.0, align=TA.MIDDLE_CENTER, style="ANB")
        text(ps, f"DB{db}", (xs[1] + 1.0, yy), 2.0, align=TA.MIDDLE_LEFT)
        shape_sketch(ps, shp, xs[2], y_top - r * rh, cols[3] - cols[2], rh)
        text(ps, "  ".join(f"{a}={r5(v)}" for a, v in dims), (xs[3] + 1.0, yy), 2.0, align=TA.MIDDLE_LEFT)
        for i, v in ((4, str(cnt)), (5, f"{cut:.2f}"), (6, f"{cut * cnt * UW[db]:.1f}")):
            text(ps, v, (xs[i] + 1.0, yy), 2.0, align=TA.MIDDLE_LEFT)
        text(ps, rem, (xs[7] + 1.0, yy), 2.0, align=TA.MIDDLE_LEFT)
    yb = y_top - n * rh
    kg = sum(tot.values())
    text(ps, f"TOTAL: DB12 {tot[12]:.1f} kg + DB10 {tot[10]:.1f} kg = {kg:.1f} kg PER FLIGHT", (x, yb - 3.5), 2.0,
         style="ANB")
    text(ps, "HOOK B = VERTICAL LEG, DIMENSIONS OUT-TO-OUT; CUT LENGTH INDICATIVE.", (x, yb - 7.5), 2.0)
    return yb - 9


NOTES = notes([
    hdr("NOTES"),
    "1.  DEMONSTRATION DRAWING: TYPICAL SINGLE-FLIGHT STAIR SPANNING BETWEEN BEAMS B1 AND B2. CONFIRM LEVELS, RISERS AND WIDTH WITH THE ARCHITECTURAL DRAWINGS.",
    "2.  CONCRETE fc' ≥ 240 ksc (CYLINDER, 28 DAYS), READY-MIXED TO TIS 213. DEFORMED BARS SD40 TO TIS 24.",
    "3.  CLEAR COVER 20 TO STAIR AND SLABS, 30 TO BEAM STIRRUPS.",
    "4.  DESIGN: LL 3.0 kPa (300 kg/m², STAIR), FINISHES 1.0 kPa, U = 1.4D + 1.7L (EIT 1008-38). SIMPLY SUPPORTED, L = 2.45 m C/C BEAMS: Mu = 11.6 kN·m/m ≤ φMn = 23.5 kN·m/m WITH (1). WAIST 150 ≥ L(SLOPE)/20 = 148.",
    "5.  (4) ≥ 0.0018 bh = 270 mm²/m: DB10@200 = 393 mm²/m.",
    "6.  TOP BARS (2) AND (3) RUN STRAIGHT PAST THE RE-ENTRANT CORNERS INTO THE BEAMS - DO NOT BEND BARS AROUND AN INSIDE CORNER.",
    "7.  BENDS ON A 6 db MANDREL; NO LAPS IN (1), (2), (3).",
    "8.  STEPS ARE STRUCTURAL PROFILE; FINISHES BY ARCH. RISERS EQUAL AFTER FINISHES.",
    "9.  CAST THE FLIGHT MONOLITHIC WITH B1 AND B2 OR PROVIDE STARTER BARS; NO CONSTRUCTION JOINT IN THE FLIGHT.",
])


def legend(ps, x, y_top):
    """line & reinforcement legend - every sample drawn with the same layer / helper as the views"""
    colw = 104
    text(ps, "LEGEND - LINES & REINFORCEMENT (PEN = PLOTTED LINEWEIGHT)", (x, y_top + 3), 2.8, "S-TITLE", style="ANB")
    rows1 = [("S-CONC", "CONCRETE CUT IN SECTION", "0.35"),
             ("S-CONC-VIS", "CONCRETE SEEN (PLAN / BEYOND)", "0.25"),
             ("S-CONC-HIDN", "HIDDEN (BEAMS BELOW) - GREY", "0.25"),
             ("S-CUTL", "CUTTING PLANE, 0.50 END STROKES", "0.25"),
             ("S-BREAK", "BREAK LINE - GREY", "0.18"),
             ("DIM", "DIMENSION: 2 mm ARROWS, GREY EXTENSION LINES", "0.18")]
    rows2 = [("S-REBR", "STAIR BARS ALONG THEIR LENGTH", "0.50"),
             ("S-REBR-SEC", "DISTRIBUTION / BARS BY OTHERS", "0.35"),
             ("HOOK", "HOOK: BEND ON 6 db MANDREL (R = 3.5 db)", "0.50"),
             ("DOT", "BAR CUT IN SECTION: FILLED DOT, MIN. 1.1 mm", "-"),
             ("ARW", "LEADER TO A BAR: 2 mm ARROW ON THE BAR EDGE", "0.18"),
             ("RING", "LEADER TO A CUT BAR: RING Ø = 2 x DOT", "0.18")]
    for c, rows in enumerate((rows1, rows2)):
        x0 = x + c * (colw + 8)
        yy = y_top - 3
        for lay, desc, pen in rows:
            a, b = (x0, yy), (x0 + 20, yy)
            if lay == "DIM":
                dim(ps, (x0 + 2, yy - 1.5), (x0 + 18, yy - 1.5), (0, yy + 0.3), 1, text=" ")
            elif lay == "HOOK":
                bar(ps, [(x0, yy + 1.2), (x0 + 16, yy + 1.2), (x0 + 16, yy - 1.8)], 1.0)
            elif lay == "DOT":
                for k in range(4):
                    dot(ps, (x0 + 3 + 4.5 * k, yy), 0.55)
            elif lay == "ARW":
                line(ps, (x0, yy - 1.2), (x0 + 20, yy - 1.2), "S-REBR")
                pline(ps, [(x0 + 10, yy - 0.8), (x0 + 12.5, yy + 1.7), (x0 + 20, yy + 1.7)], "S-ANNO")
                arrowhead(ps, (x0 + 10, yy - 0.8), (x0 + 12.5, yy + 1.7), ARROW)
            elif lay == "RING":
                dot(ps, (x0 + 8, yy - 1), 0.55)
                ps.add_circle((x0 + 8, yy - 1), 1.1, dxfattribs=A("S-ANNO"))
                pline(ps, [(x0 + 8.8, yy - 0.2), (x0 + 10.7, yy + 1.7), (x0 + 16, yy + 1.7)], "S-ANNO")
                ps.add_circle((x0 + 18, yy + 1.7), 2.0, dxfattribs=A("S-SYMB"))
                text(ps, "4", (x0 + 18, yy + 1.7), 2.0, align=TA.MIDDLE_CENTER, style="ANB")
            elif lay == "S-CUTL":
                line(ps, (x0 + 3, yy), (x0 + 17, yy), "S-CUTL")
                line(ps, (x0, yy), (x0 + 3, yy), "S-CUTL-END")
                line(ps, (x0 + 17, yy), (x0 + 20, yy), "S-CUTL-END")
            elif lay == "S-BREAK":
                zbreak(ps, a, b, 1)
            else:
                line(ps, a, b, lay)
            text(ps, desc, (x0 + 24, yy), 2.0, align=TA.MIDDLE_LEFT)
            text(ps, pen, (x0 + colw - 8, yy), 2.0, align=TA.MIDDLE_LEFT)
            yy -= 5.2
    text(ps, "TEXT ARIAL NARROW 2.0 mm, HEADERS 2.8 mm.  PLOT WITH NRW-EIT.ctb: ALL BLACK, ACI 8 AT 50 % GREY.",
         (x, y_top - 3 - 6 * 5.2 - 1), 2.0)


def sheet_5101():
    ps = new_sheet(0)
    top = FY1 - 3
    px, pw, ph = viewport(ps, "AA", 20, FX0, top)
    view_title(ps, None, top - ph - 6, "SECTION A-A - STAIR ST-1", "1:20", ("A", "5101"), triangles=True,
               note="CLEAR COVER 20 U.N.O.  BEAMS & SLABS (THIN BARS) BY OTHERS - SHOWN FOR CONTEXT.")
    xr = FX0 + pw + 3
    yb = schedule(ps, xr, top - 6)
    mtext(ps, NOTES, (xr, yb - 3), 2.0, TBX - xr - 3, spacing=1.1)
    top2 = top - ph - 18
    px2, pw2, ph2 = viewport(ps, "PL", 50, FX0, top2)
    view_title(ps, None, top2 - ph2 - 6, "PLAN - STAIR ST-1", "1:50", ("1", "5101"),
               note=f"{NR} RISERS @ {RH} = {NR * RH}, {NR - 1} TREADS @ {TG}")
    px3, pw3, ph3 = viewport(ps, "BB", 10, FX0 + pw2 + 6, top2)
    view_title(ps, None, top2 - ph3 - 6, "SECTION B-B", "1:10", ("B", "5101"), triangles=True,
               note="VERTICAL CUT AT MID-TREAD 2, LOOKING UP THE FLIGHT; STEPS BEYOND NOT SHOWN.")
    legend(ps, FX0 + 4, top2 - max(ph2, ph3) - 24)


sheet_5101()
if "Layout1" in doc.layouts:
    doc.layouts.delete("Layout1")
OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(DXF)
print("saved", DXF)
