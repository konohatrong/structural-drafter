"""
Nooker retaining wall - NRW-ST A3 structural drawing set generator (7 sheets, Rev A).

Drafting standard : EIT 011006-19 + office conventions (DRAWING_STANDARD_EIT-011006-19.md section 19)
Model space       : 1 unit = 1 mm, full size. Each view lives in its own model region.
Paper space       : one A3 layout per sheet, scaled locked viewports, LTSCALE=1 / PSLTSCALE=1.
Text              : Arial Narrow, 2.0 mm body / 2.8 mm headers (plotted height).
Pens              : 0.50 bars, 0.35 cut concrete, 0.25 seen/hidden, 0.18 dims/leaders, 0.13 hatch; ACI 8 = grey.
Annotation        : engine below (leader / note_cfg / capture) - see ANNOTATION_ALIGNMENT_GUIDE.md.
Handover          : jobs/nooker_rw/README.md (design, geometry, sheets, build, plot, revise).

usage: python build_rw.py <out_dir>      -> <out_dir>/NRW-ST_Retaining_Wall_A3_RevB.dxf
"""
import math
import sys
from pathlib import Path

import ezdxf
from ezdxf import bbox
from ezdxf.path import make_path
from ezdxf.enums import TextEntityAlignment as TA, MTextEntityAlignment as MA

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
DXF = OUT / "NRW-ST_Retaining_Wall_A3_RevB.dxf"

# --------------------------------------------------------------------------- project data
PROJ = dict(
    code="NRW",
    owner="[ OWNER NAME ]",
    project="RETAINING WALL - NOOKER",
    location="[ PLOT / TITLE DEED NO., TAMBON, AMPHOE, PROVINCE ]",
    office="[ DESIGN OFFICE NAME ]",
    office2="[ ADDRESS / TEL. / E-MAIL ]",
    date="03/10/2026",
    stage="D", rev="B",
)
SHEETS = [  # (layout name = series, title lines, scale text)
    ("1001", ["GENERAL NOTES,", "DESIGN CRITERIA & LEGEND"], "N.T.S."),
    ("3001", ["TYPICAL PLAN &", "LONGITUDINAL ELEVATION"], "1:100"),
    ("5001", ["SECTION A", "TYPICAL WALL SECTION"], "1:10"),
    ("5002", ["EXPANSION JOINT", "DETAILS"], "1:5"),
    ("5003", ["CONTRACTION JOINT &", "JOINT PLANE"], "AS SHOWN"),
    ("5004", ["CORNER & WALL END", "DETAILS"], "AS SHOWN"),
    ("5005", ["REINFORCEMENT SCHEDULE", "& BAR PLANES"], "AS SHOWN"),
]
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


DS = {s: dimstyle(f"EIT-{s}", s) for s in (2, 5, 10, 20, 25, 100)}

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


def leader(sp, tip, knee, s, S, side="R", width=48, layer="S-ANNO", dot_tip=False, mark=None, ring=0):
    """ring=db: bar cut in section -> open circle of 2 x the drawn bar diameter round the bar dot"""
    n = dict(sp=sp, tip=tip, knee=knee, s=s, S=S, side=side, width=width, layer=layer,
             dot=dot_tip and not ring, mark=mark, ring=ring)    # bars along their length: filled arrow
    if _NOTES is None or _CFG.get("free"):
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


def dim(sp, p1, p2, base, S, angle=0, override=None):
    d = sp.add_linear_dim(base=base, p1=p1, p2=p2, angle=angle, dimstyle=DS[S],
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


# --------------------------------------------------------------------------- geometry constants (mm)
TS = 200      # stem thickness
B = 1200      # footing width
TF = 250      # footing thickness
TOW = 600     # top of wall (= max fill level)
TOF = -150    # top of footing
BOF = -400    # bottom of footing
LEAN = 50
KB, KD = 250, 300   # shear key at heel end
KX0 = B - KB        # 950
KBOT = BOF - KD     # -700
DRN_W = 300   # drainage stone zone width
DRN_TOP = 300
PIPE_R = 57   # PVC dia 100 nominal, OD 114
PIPE_C = (350, TOF + PIPE_R + 20)
CH = 20       # chamfer

C_EXP = 40    # cover: exposed / formed / soil face
C_TOP = 50
C_BOT = 50    # on lean concrete
C_EARTH = 75  # cast against earth

XB = TS - C_EXP - 6            # 154  soil-face vertical DB12 (centre)
XF = C_EXP + 5                 # 45   exposed-face vertical DB10 (centre)
YHB = XB - 12                  # 142  soil-face horizontal DB12
YHF = XF + 10                  # 55   exposed-face horizontal DB10


def wall_outline(P):
    return [P(0, TOW - CH), P(CH, TOW), P(TS - CH, TOW), P(TS, TOW - CH), P(TS, TOF),
            P(B, TOF), P(B, KBOT), P(KX0, KBOT), P(KX0, BOF), P(0, BOF)]


# --------------------------------------------------------------------------- bar geometry (centrelines, mm)
# origin: x = 0 at exposed face (property line), +x into the fill; z = 0 at adjacent ground +-0.000
ZT = TOW - C_EXP - 6            # 554   (1) top leg
ZTT = TOF - C_TOP - 6           # -206  (5) C-bar top leg
ZBB = BOF + C_BOT + 6           # -344  (5) C-bar bottom leg
ZLT, ZLB = ZTT - 12, ZBB + 12   # -218 / -332  (6) longitudinal, inside (5)
ZTAIL = ZLB + 12                # -320  (1) tail seated on bottom (6) bars
Z3TAIL = ZTAIL + 11             # -309  (3) tail (own plane)
XTOE = C_EARTH + 6              # 81    (5) toe return, 75 cover (cast against earth)
XCEND = 1105                    # (5) straight ends at heel, clear of key U-bar leg
KL, KR = KX0 + C_EARTH + 6, B - C_EARTH - 6      # 1031 / 1119  (7) key U legs
KZ = KBOT + C_EARTH + 6         # -619
KTOP = TOF - 100                # -250  (7) legs up into footing cage
XLONG = [102, 300, 500, 700, 900, 1100]            # (6) first bar sits in the C-bar bend
ZSTEMH = [-75, 125, 325, 525]   # (2) / (4) horizontal levels @200
# bar planes along the wall, measured from the joint face (EIT: show on drawing if not on shop drawing)
PLANES = {"1": 50, "7": 50, "5": 150, "3": 100}     # first plane; (1),(5),(7) repeat @200, (3) @400


EXC_WS = 150                    # working space beyond the heel at founding level
EXC_X0 = B + EXC_WS             # toe of the excavation slope
EXC_V, EXC_H = 2.0, 1.0         # excavation slope V : H = 2 : 1
XRB = 1650                      # right break line of Section A


def EXC_Y(x):
    """excavation line: 2 vertical : 1 horizontal from the working-space edge at founding level"""
    return BOF - LEAN + (x - EXC_X0) * EXC_V / EXC_H


EXC_XT = EXC_X0 + (0 - (BOF - LEAN)) * EXC_H / EXC_V     # top of cut at existing ground +-0.000


# ======================================================================= SECTION A (1:10)
def section_a(ox, oy):
    S = 10
    sp = msp
    P = lambda x, y: (ox + x, oy + y)

    # ---- draw order: hatches / soil -> concrete -> reinforcement -> annotation
    lean = [P(0, BOF - LEAN), P(KX0, BOF - LEAN), P(KX0, BOF), P(0, BOF)]
    hatch(sp, lean, "AR-CONC", 0.05)
    earth_band(sp, [P(0, BOF - LEAN), P(KX0, BOF - LEAN)], 70, S)
    earth_band(sp, [P(KX0, KBOT), P(B, KBOT)], 70, S)
    earth_band(sp, [P(-780, 0), P(0, 0)], 70, S)
    # selected fill behind the wall, bounded by the 2:1 (V:H) excavation, existing ground and a break line
    fill = [P(TS, TOW), P(XRB, TOW), P(XRB, 0), P(EXC_XT, 0), P(EXC_X0, BOF - LEAN), P(B, BOF - LEAN),
            P(B, TOF), P(TS + DRN_W, TOF), P(TS + DRN_W, DRN_TOP), P(TS, DRN_TOP)]
    hatch(sp, fill, "AR-SAND", pscale("AR-SAND", S, 1.0))
    exc = [P(B, BOF - LEAN), P(EXC_X0, BOF - LEAN), P(EXC_XT, 0)]
    earth_band(sp, exc + [P(XRB, 0)], 70, S)
    pline(sp, exc, "S-EXCV")
    line(sp, P(EXC_XT, 0), P(XRB, 0), "S-SOIL")                          # existing ground, retained side
    zbreak(sp, P(XRB, -120), P(XRB, TOW + 60), S)
    # slope triangle 2 : 1 (V : H) on the fill side of the cut
    th = 50                                                               # 1 unit = 50 mm
    tx0 = EXC_X0 + 25
    ty0 = EXC_Y(tx0)
    pline(sp, [P(tx0, ty0), P(tx0, ty0 + EXC_V * th), P(tx0 + EXC_H * th, ty0 + EXC_V * th)], "S-ANNO")
    text(sp, "2", P(tx0 - 12, ty0 + EXC_V * th / 2), 2.0 * S, align=TA.MIDDLE_RIGHT)
    text(sp, "1", P(tx0 + EXC_H * th / 2, ty0 + EXC_V * th + 12), 2.0 * S, align=TA.BOTTOM_CENTER)
    stone = [P(TS, TOF), P(TS + DRN_W, TOF), P(TS + DRN_W, DRN_TOP), P(TS, DRN_TOP)]
    hatch(sp, stone, "GRAVEL", pscale("GRAVEL", S, 1.0), islands=[circle_pts(P(*PIPE_C), PIPE_R + 2)])

    pline(sp, lean, "S-LEAN", close=True)
    line(sp, P(-780, 0), P(0, 0), "S-SOIL")
    line(sp, P(0, -960), P(0, 1000), "S-PROP")
    sp.add_circle(P(*PIPE_C), PIPE_R, dxfattribs=A("S-DRAIN"))
    sp.add_circle(P(*PIPE_C), PIPE_R - 6, dxfattribs=A("S-DRAIN"))
    pline(sp, [P(TS, DRN_TOP), P(TS + DRN_W, DRN_TOP), P(TS + DRN_W, TOF)], "S-GEOT")
    line(sp, P(TS, TOW), P(XRB, TOW), "S-SOIL")
    text(sp, "FILL LEVEL +0.600 MAX.", P(230, TOW + 12), 2.0 * S)
    for x in range(550, 1301, 150):
        line(sp, P(x, TOW + 170), P(x, TOW + 25), "S-SURCH")
        arrowhead(sp, P(x, TOW + 8), P(x, TOW + 170), 1.5 * S, "S-SURCH")
    line(sp, P(550, TOW + 170), P(1300, TOW + 170), "S-SURCH")
    mtext(sp, "DESIGN SURCHARGE q = 10 kPa (1.0 t/m²)\\PLIGHT VEHICLES - PAVEMENT BY OTHERS",
          P(550, TOW + 200), 2.0 * S, 60 * S, attach=MA.BOTTOM_LEFT)

    pline(sp, wall_outline(P), "S-CONC", close=True)
    zigzag(sp, P(0, TOF), P(TS, TOF), S)                                  # horizontal construction joint

    # ---- reinforcement (centrelines, filleted bends R = 3.5 db)
    bar(sp, [P(XB - 94, ZT), P(XB, ZT), P(XB, ZTAIL), P(XB + 300, ZTAIL)], 12)                    # (1)
    bar(sp, [P(XF + 95, ZT - 12), P(XF, ZT - 12), P(XF, Z3TAIL), P(XF + 200, Z3TAIL)], 10, "S-REBR-SEC")  # (3)
    bar(sp, [P(XCEND, ZTT), P(XTOE, ZTT), P(XTOE, ZBB), P(XCEND, ZBB)], 12)                        # (5)
    bar(sp, [P(KL, KTOP), P(KL, KZ), P(KR, KZ), P(KR, KTOP)], 12)                                    # (7)
    r12, r10 = rdot(12, S), rdot(10, S)
    for i, x in enumerate(XLONG):                                                                   # (6)
        dot(sp, P(x, ZLT - (9 if i == 0 else 0)), r12)
        dot(sp, P(x, ZLB + (9 if i == 0 else 0)), r12)
    for z in ZSTEMH:                                                                                # (2),(4)
        dot(sp, P(YHB, z), r12)
        dot(sp, P(YHF, z), r10, "S-REBR-SEC")
    dot(sp, P(KL + 21, KZ + 21), r12)                                                               # (8)
    dot(sp, P(KR - 21, KZ + 21), r12)

    # ---- dimensions (concrete, plus the hook tail which is not fixed by cover)
    dim(sp, P(0, TOW), P(TS, TOW), P(0, TOW + 330), S)
    dim(sp, P(TS, TOW), P(TS + DRN_W, TOW), P(0, TOW + 330), S)
    dim(sp, P(0, KBOT), P(TS, KBOT), P(0, KBOT - 170), S)
    dim(sp, P(TS, KBOT), P(KX0, KBOT), P(0, KBOT - 170), S)
    dim(sp, P(KX0, KBOT), P(B, KBOT), P(0, KBOT - 170), S)
    dim(sp, P(0, KBOT), P(B, KBOT), P(0, KBOT - 290), S)
    for z0, z1 in [(BOF - LEAN, BOF), (BOF, TOF), (TOF, 0), (0, TOW)]:
        dim(sp, P(-720, z0), P(-720, z1), P(-800, 0), S, angle=90)
    dim(sp, P(-720, BOF - LEAN), P(-720, TOW), P(-900, 0), S, angle=90)
    dim(sp, P(KX0, KBOT), P(KX0, BOF), P(KX0 - 110, 0), S, angle=90)

    # ---- levels (outside the section, left): extension lines run to the concrete face;
    #      the height chain sits on the level lines, outside the note column
    LX = -700
    LEV = [(TOW, "+0.600", "TOP OF WALL"), (0, "±0.000", "ADJACENT GROUND"), (TOF, "-0.150", "T.O. FOOTING"),
           (BOF, "-0.400", "B.O. FOOTING"), (KBOT, "-0.700", "B.O. SHEAR KEY")]
    for z, v, d in LEV:
        level(sp, P(LX, 0)[0], P(0, z)[1], v, d, S, ext=(-2, 68))
    line(sp, P(-20, KBOT), P(KX0 - 20, KBOT), "S-ANNO")

    # ---- notes: left column = boundary side / exposed face, right column = retained side
    note_cfg(xL=P(-330, 0)[0], xR=P(XRB + 60, 0)[0],
             avoidL=[(P(0, z)[1] - 8, P(0, z)[1] + 34) for z, _, _ in LEV])
    kl, kr = P(-330, 0), P(XRB + 60, 0)
    leader(sp, P(CH / 2, TOW - CH / 2), kl, "20x20 CHAMFER (TYP.)", S, "L", 36)
    leader(sp, P(XF, 240), kl, "DB10@400 VERT. - EXPOSED FACE, TAIL 200", S, "L", 36, mark=3)
    leader(sp, P(YHF, 125), kl, "DB10@200 HORIZ. - EXPOSED FACE", S, "L", 36, mark=4, ring=10)
    leader(sp, P(60, TOF), kl, "CONSTRUCTION JOINT - ROUGHEN TO 5 mm", S, "L", 36)
    leader(sp, P(300, BOF - 25), kl, "LEAN CONCRETE 50 THK.", S, "L", 36)
    leader(sp, P(250, BOF - LEAN - 40), kl, "COMPACTED SUBGRADE ≥ 95% STD. PROCTOR (DH-T 107); qa ≥ 50 kPa - VERIFY ON SITE", S, "L", 36)
    leader(sp, P(0, -880), kl, "PROPERTY LINE = FRONT FACE OF WALL (SURVEYED)", S, "L", 36)

    leader(sp, P(XB, 450), kr, "DB12@200 VERT. - SOIL FACE: 90° HOOK, TAIL 300 SEATED ON (6); NO LAPS", S, "R", 44, mark=1)
    leader(sp, P(YHB, 325), kr, "DB12@200 HORIZ. - SOIL FACE, INSIDE (1)", S, "R", 44, mark=2, ring=12)
    leader(sp, P(1000, 420), kr, "SELECTED FILL ≥ 95% MOD. PROCTOR (DH-T 108), 200 LAYERS", S, "R", 44)
    leader(sp, P(EXC_X0 + 190, EXC_Y(EXC_X0 + 190)), kr, "EXCAVATION 2:1 (V:H) OR FLATTER; WORKING SPACE 150", S, "R", 46)
    leader(sp, P(TS + DRN_W, 180), kr, "NON-WOVEN GEOTEXTILE WRAP ≥ 200 g/m²", S, "R", 44)
    leader(sp, P(440, 20), kr, "FREE-DRAINING CRUSHED STONE 12-25 mm, 300 WIDE", S, "R", 44)
    leader(sp, (P(*PIPE_C)[0] + 40, P(*PIPE_C)[1] + 40), kr,
           "SUBSOIL DRAIN: PERFORATED PVC Ø100 CL. 8.5 (TIS 17), FALL ≥ 1:200", S, "R", 44)
    leader(sp, P(850, ZTT), kr, "DB12@200 C-BAR, CLOSED AT TOE", S, "R", 46, mark=5)
    leader(sp, P(XLONG[-1], ZLT), kr, "6+6-DB12 LONG. (T & B), INSIDE (5)", S, "R", 44, mark=6, ring=12)
    leader(sp, P(KR, -450), kr, "DB12@200 U-BAR (SHEAR KEY)", S, "R", 44, mark=7)
    leader(sp, P(KR - 21, KZ + 21), kr, "2-DB12 LONG. (SHEAR KEY)", S, "R", 44, mark=8, ring=12)
    leader(sp, P(B, KBOT + 60), kr, "KEY CAST AGAINST UNDISTURBED SOIL", S, "R", 44)
    text(sp, "BOUNDARY SIDE", P(-700, 990), 2.8 * S, style="ANB")
    text(sp, "RETAINED SIDE", P(800, 990), 2.8 * S, style="ANB")


# ======================================================================= PLAN & ELEVATION (1:100)
EJ_X = [0, 24000]
CJ_X = [6000, 12000, 18000]
XL, XR = -1500, 25500
EJG = 10      # half gap of expansion joint (gap centred on the joint line)


def wall_segments(x0, x1, gaps):
    segs, cur = [], x0
    for a, b in sorted(gaps):
        if x0 < a and b < x1:
            segs.append((cur, a))
            cur = b
    segs.append((cur, x1))
    return segs


GAPS = [(x - EJG, x + EJG) for x in EJ_X] + [(x, x) for x in CJ_X]


def plan_view(ox, oy):
    S = 100
    note_cfg(free=True)
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    for a, b in wall_segments(XL, XR, GAPS):
        line(sp, P(a, 0), P(b, 0), "S-CONC-VIS")
        line(sp, P(a, TS), P(b, TS), "S-CONC-VIS")
        for xx in (a, b):
            if xx not in (XL, XR):
                line(sp, P(xx, 0), P(xx, TS), "S-CONC-VIS")
                line(sp, P(xx, TS), P(xx, B), "S-CONC-HIDN")
        line(sp, P(a, B), P(b, B), "S-CONC-HIDN")
        line(sp, P(a, KX0), P(b, KX0), "S-CONC-HIDN")
    zbreak(sp, P(XL, -350), P(XL, B + 350), S)
    zbreak(sp, P(XR, -350), P(XR, B + 350), S)
    line(sp, P(XL, 350), P(XR, 350), "S-DRAIN-HIDN")
    for x in EJ_X:                                                    # outlets at E.J.
        line(sp, P(x + 350, 350), P(x + 350, 2250), "S-DRAIN-HIDN")
        arrowhead(sp, P(x + 350, 2400), P(x + 350, 2000), 1.8 * S, "S-DRAIN")
    leader(sp, P(350, 2000), P(900, 2550), "OUTLET AT EACH E.J. TO OWNER'S SITE DRAINAGE (BY OTHERS)", S, "R", 60)
    line(sp, P(XL - 900, 0), P(XR + 700, 0), "S-PROP")
    for x, tag, ref in [(x, "E.J.", "1/5002") for x in EJ_X] + [(x, "C.J.", "1/5003") for x in CJ_X]:
        line(sp, P(x, B + 100), P(x, B + 500), "S-ANNO")
        text(sp, ref, P(x, B + 600), 2.0 * S, align=TA.BOTTOM_CENTER)
        text(sp, tag, P(x, B + 950), 2.0 * S, align=TA.BOTTOM_CENTER, style="ANB")
    xs = [0] + CJ_X + [24000]
    for a, b in zip(xs[:-1], xs[1:]):
        dim(sp, P(a, 0), P(b, 0), P(0, -800), S, override={"dimpost": "<> MAX."})
    dim(sp, P(0, 0), P(24000, 0), P(0, -1400), S,
        override={"dimpost": "<> MAX. BETWEEN E.J. (WALL LENGTH VARIES - SEE SITE PLAN)"})
    dim(sp, P(XL + 300, 0), P(XL + 300, TS), P(XL - 400, 0), S, angle=90)
    dim(sp, P(XL + 300, TS), P(XL + 300, B), P(XL - 400, 0), S, angle=90)
    # section cut A (viewed toward -x: section is drawn with the boundary on the left)
    cx = 10500
    line(sp, P(cx, -450), P(cx, B + 450), "S-CUTL")
    for yy, dy in ((-450, -1), (B + 450, 1)):
        tip = P(cx - 700, yy)
        line(sp, P(cx, yy), tip, "S-SYMB")
        arrowhead(sp, tip, P(cx, yy), 2.2 * S, "S-SYMB")
        text(sp, "A", P(cx - 380, yy + (120 if dy > 0 else -420)), 2.8 * S, align=TA.BOTTOM_CENTER, style="ANB")
    text(sp, "5001", P(cx + 150, B + 450), 2.0 * S, align=TA.MIDDLE_LEFT)
    text(sp, "RETAINED SIDE - FILL / DRIVEWAY, FILL LEVEL +0.600 MAX.", P(6500, B + 1750), 2.0 * S)
    text(sp, "ADJACENT LAND (BOUNDARY SIDE)  ±0.000", P(1500, -2150), 2.0 * S)
    text(sp, "PROPERTY LINE (P.L.) = FRONT FACE OF WALL", P(14500, -2150), 2.0 * S)
    leader(sp, P(3000, TS / 2), P(3400, -450), "RC WALL 200 THK. (STEM)", S, "R", 40)
    leader(sp, P(21000, B), P(21400, B + 1750), "HEEL / SHEAR KEY BELOW FILL (HIDDEN)", S, "R", 45)
    leader(sp, P(15000, 350), P(15400, 750), "SUBSOIL DRAIN (HIDDEN)", S, "R", 40)


def elevation_view(ox, oy):
    S = 100
    note_cfg(free=True)
    sp = msp
    P = lambda x, z: (ox + x, oy + z)
    for a, b in wall_segments(XL, XR, GAPS):
        line(sp, P(a, TOW), P(b, TOW), "S-CONC-VIS")
        line(sp, P(a, BOF), P(b, BOF), "S-CONC-HIDN")
        line(sp, P(a, KBOT), P(b, KBOT), "S-CONC-HIDN")
        for xx in (a, b):
            if xx not in (XL, XR):
                line(sp, P(xx, 0), P(xx, TOW), "S-CONC-VIS")
                line(sp, P(xx, KBOT), P(xx, 0), "S-CONC-HIDN")
    zbreak(sp, P(XL, KBOT - 200), P(XL, TOW + 200), S)
    zbreak(sp, P(XR, KBOT - 200), P(XR, TOW + 200), S)
    line(sp, P(XL - 2300, 0), P(XR + 400, 0), "S-SOIL")
    for x, tag in [(x, "E.J.") for x in EJ_X] + [(x, "C.J.") for x in CJ_X]:
        text(sp, tag, P(x, TOW + 250), 2.0 * S, align=TA.BOTTOM_CENTER, style="ANB")
    lx = XL - 2100
    level(sp, lx, P(0, TOW)[1], "+0.600", "T.O. WALL", S, ext=(-2, 19))
    level(sp, lx, P(0, 0)[1], "±0.000", "ADJ. GROUND", S, ext=(-2, 19))
    level(sp, lx, P(0, BOF)[1], "-0.400", "B.O. FOOTING", S, ext=(-2, 19))
    level(sp, lx, P(0, KBOT)[1], "-0.700", "B.O. KEY", S, ext=(-2, 19))
    leader(sp, P(9000, 300), P(9400, 1250), "EXPOSED FACE ON PROPERTY LINE - 20x20 CHAMFER TO TOP EDGES", S, "R", 70)
    leader(sp, P(15000, KBOT), P(15400, -1350), "FOOTING & SHEAR KEY BELOW GROUND (HIDDEN)", S, "R", 70)
    leader(sp, P(12000, 450), P(12400, 950), "SEALED JOINT (TYP.) - SEE 3/3001", S, "R", 50)


def partial_elevation(ox, oy):
    """Enlarged elevation at an E.J. with the adjacent C.J. behaviour noted (1:25), viewed from adjacent land."""
    S = 25
    sp = msp
    P = lambda x, z: (ox + x, oy + z)
    X0, X1 = -1200, 1200
    for a, b in ((X0, -EJG), (EJG, X1)):
        line(sp, P(a, TOW), P(b, TOW), "S-CONC-VIS")
        line(sp, P(a, TOW - CH), P(b, TOW - CH), "S-CONC-JNT")          # chamfer arris
        line(sp, P(a, TOF), P(b, TOF), "S-CONC-HIDN")                   # construction joint (below ground)
        line(sp, P(a, BOF), P(b, BOF), "S-CONC-HIDN")
        line(sp, P(a, KBOT), P(b, KBOT), "S-CONC-HIDN")
    line(sp, P(X0, BOF - LEAN), P(X1, BOF - LEAN), "S-CONC-HIDN")       # lean concrete continuous
    for xx in (-EJG, EJG):
        line(sp, P(xx, 0), P(xx, TOW), "S-CONC-VIS")
        line(sp, P(xx, KBOT), P(xx, 0), "S-CONC-HIDN")
    seal = [P(-EJG, -100), P(EJG, -100), P(EJG, TOW), P(-EJG, TOW)]
    hatch(sp, seal, "SOLID", 1, layer="S-JOINT")
    zbreak(sp, P(X0, KBOT - 150), P(X0, TOW + 150), S)
    zbreak(sp, P(X1, KBOT - 150), P(X1, TOW + 150), S)
    line(sp, P(X0 - 60, 0), P(X1 + 300, 0), "S-SOIL")
    # dowels (hidden) crossing the joint
    for z in (450, 150, (TOF + BOF) / 2):
        line(sp, P(-300, z), P(300, z), "S-CONC-HIDN")
    # subsoil drain behind and outlet turning away at E.J.
    line(sp, P(X0, TOF + 77), P(X1, TOF + 77), "S-DRAIN-HIDN")
    dim(sp, P(-EJG, TOW), P(EJG, TOW), P(0, TOW + 180), S)
    dim(sp, P(-300, 450), P(0, 450), P(0, TOW + 90), S)
    dim(sp, P(0, 450), P(300, 450), P(0, TOW + 90), S)
    for z0, z1 in ((0, TOW), (TOF, 0), (BOF, TOF), (KBOT, BOF)):
        dim(sp, P(X1 + 120, z0), P(X1 + 120, z1), P(X1 + 120, 0), S, angle=90)
    lx = X1 + 600
    level(sp, lx, P(0, TOW)[1], "+0.600", "T.O. WALL", S, ext=(-2, 30))
    level(sp, lx, P(0, 0)[1], "±0.000", "ADJACENT GROUND", S, ext=(-2, 30))
    level(sp, lx, P(0, TOF)[1], "-0.150", "T.O. FOOTING", S, ext=(-2, 30))
    level(sp, lx, P(0, BOF)[1], "-0.400", "B.O. FOOTING", S, ext=(-2, 30))
    level(sp, lx, P(0, KBOT)[1], "-0.700", "B.O. SHEAR KEY", S, ext=(-2, 30))
    note_cfg(yT=P(0, TOW + 330)[1], yB=P(0, KBOT - 180)[1])
    kT, kB = P(0, TOW + 330), P(0, KBOT - 180)
    leader(sp, P(-1000, TOW - CH / 2), kT, "20x20 CHAMFER", S, "T", 30)
    leader(sp, P(-EJG, 450), kT, "E.J. 20 - PU SEALANT ON EXPOSED FACE & TOP, TO 100 BELOW GROUND (1/5002)", S, "T", 40)
    leader(sp, P(250, 150), kT, "RB16@300 SLIP DOWELS (HIDDEN)", S, "T", 30)
    leader(sp, P(-900, TOF), kB, "CONSTRUCTION JOINT T.O. FOOTING (HIDDEN)", S, "B", 30)
    leader(sp, P(-500, BOF - LEAN), kB, "LEAN CONCRETE CONTINUOUS", S, "B", 30)
    leader(sp, P(700, TOF + 77), kB, "SUBSOIL DRAIN BEHIND STEM (HIDDEN)", S, "B", 30)


# ======================================================================= JOINT DETAILS
def stem_plan_section(ox, oy, kind):
    """Plan section through stem at +0.300 (1:5). kind = 'EJ' or 'CJ'. Exposed (boundary) face at y=0."""
    S = 5
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    g = EJG if kind == "EJ" else 0          # joint centred on x=0
    L0, L1 = -370, 370
    c = 10                                  # arris chamfer at exposed joint edge
    if kind == "EJ":
        pline(sp, [P(L0, 0), P(-g - c, 0), P(-g, c), P(-g, TS), P(L0, TS)], "S-CONC")
        pline(sp, [P(L1, 0), P(g + c, 0), P(g, c), P(g, TS), P(L1, TS)], "S-CONC")
        fill = [P(-g, 40), P(g, 40), P(g, TS), P(-g, TS)]
        pline(sp, fill, "S-JFILL", close=True)
        hatch(sp, fill, "ANSI31", pscale("ANSI31", S, 0.8))
        sp.add_circle(P(0, 27), 11, dxfattribs=A("S-JOINT"))
        seal = [P(-g - c, 0), P(g + c, 0), P(g, c), P(g, 14), P(-g, 14), P(-g, c)]
        hatch(sp, seal, "SOLID", 1, layer="S-JOINT")
    else:
        pline(sp, [P(L0, 0), P(L1, 0)], "S-CONC")
        pline(sp, [P(L0, TS), P(L1, TS)], "S-CONC")
        line(sp, P(0, 15), P(0, TS), "S-JOINT")
        groove = [P(-8, 0), P(8, 0), P(8, 15), P(-8, 15)]
        hatch(sp, groove, "SOLID", 1, layer="S-JOINT")
    zbreak(sp, P(L0, -50), P(L0, TS + 50), S)
    zbreak(sp, P(L1, -50), P(L1, TS + 50), S)
    gw = 250 if kind == "EJ" else 150
    line(sp, P(-gw, TS + 8), P(gw, TS + 8), "S-GEOT")
    strip(sp, P(L0 + 20, YHB), P(-g - 50, YHB), 12)                    # (2) true width at 1:5
    strip(sp, P(g + 50, YHB), P(L1 - 20, YHB), 12)
    strip(sp, P(L0 + 20, YHF), P(-g - 50, YHF), 10, "S-REBR-SEC")      # (4)
    strip(sp, P(g + 50, YHF), P(L1 - 20, YHF), 10, "S-REBR-SEC")
    for x in (-g - 75, -g - 275, g + 75, g + 275):
        dot(sp, P(x, XB), 6)
    for x in (-g - 175, g + 175):
        dot(sp, P(x, XF), 5, "S-REBR-SEC")
    yd = TS / 2
    pline(sp, [P(-g - 300, yd - 8), P(g + 300, yd - 8), P(g + 300, yd + 8), P(-g - 300, yd + 8)], "S-DWL", close=True)
    sl_end = g + 300 + (25 if kind == "EJ" else 0)
    pline(sp, [P(g, yd - 12), P(sl_end, yd - 12), P(sl_end, yd + 12), P(g, yd + 12)], "S-DWL-SLV", close=True)
    yb = TS + 60
    if kind == "EJ":
        dim(sp, P(-g, TS), P(g, TS), P(0, yb), S)
    note_cfg(yT=P(0, TS + 120)[1], yB=P(0, -100)[1], xmaxT=P(L1 + 40, 0)[0], xmaxB=P(L1 + 40, 0)[0])
    dim(sp, P(L1 - 30, 0), P(L1 - 30, TS), P(L1 + 60, 0), S, angle=90)
    dim(sp, P(g, YHB), P(g + 50, YHB), P(0, TS - 20), S)
    kT, kB = P(0, TS + 120), P(0, -100)
    if kind == "EJ":
        leader(sp, P(0, 150), kT, "PREFORMED BITUMINOUS FIBRE JOINT FILLER 20 THK. (ASTM D1751), FULL SECTION INCL. FOOTING & KEY", S, "T", 44)
        leader(sp, P(g + 150, TS + 8), kT, "NON-WOVEN GEOTEXTILE STRIP 500 WIDE, BONDED ONE SIDE ONLY - SOIL FACE", S, "T", 44)
        leader(sp, P(0, 5), kB, "PU SEALANT ON Ø25 BACKER ROD - SEE 3/5002", S, "B", 40)
        leader(sp, P(g + 200, yd - 8), kB, "RB16@300 SLIP DOWEL L = 600 (SR24, TIS 20-2559): PVC SLEEVE + GREASE ONE SIDE, 25 VOID END CAP - SEE 2/5002", S, "B", 50)
    else:
        leader(sp, P(0, 150), kT, "TIGHT BUTT JOINT: 2 COATS BITUMINOUS PAINT BOND BREAKER ON HARDENED FACE OF 1ST POUR", S, "T", 44)
        leader(sp, P(100, TS + 8), kT, "NON-WOVEN GEOTEXTILE STRIP 300 WIDE, BONDED ONE SIDE ONLY - SOIL FACE", S, "T", 44)
        leader(sp, P(0, 8), kB, "SEALED GROOVE - SEE 3/5003", S, "B", 40)
        leader(sp, P(200, yd - 8), kB, "RB16@300 SLIP DOWEL L = 600 (SR24, TIS 20-2559): PVC SLEEVE + GREASE ONE SIDE, NO END CAP - SEE 2/5002", S, "B", 50)
    leader(sp, P(-g - 150, YHB), kT, "ALL HORIZONTAL BARS STOP 50 CLEAR EACH SIDE (TYP.)", S, "T", 36)
    text(sp, "SOIL FACE", P(L0 - 60, TS), 2.0 * S, align=TA.MIDDLE_RIGHT, style="ANB")
    text(sp, "EXPOSED FACE", P(L0 - 60, 20), 2.0 * S, align=TA.MIDDLE_RIGHT, style="ANB")
    text(sp, "(BOUNDARY)", P(L0 - 60, -8), 2.0 * S, align=TA.MIDDLE_RIGHT)
    text(sp, "1ST POUR", P(L0 + 30, 14), 2.0 * S, style="ANB")
    text(sp, "2ND POUR", P(L1 - 30, 14), 2.0 * S, align=TA.BOTTOM_RIGHT, style="ANB")


def sealant_ej(ox, oy):
    """E.J. sealant at exposed face, plan, 1:2."""
    S = 2
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    g, c = EJG, 10
    pline(sp, [P(-60, 0), P(-g - c, 0), P(-g, c), P(-g, 75)], "S-CONC")
    pline(sp, [P(60, 0), P(g + c, 0), P(g, c), P(g, 75)], "S-CONC")
    zbreak(sp, P(-60, -8), P(-60, 75), S)
    zbreak(sp, P(60, -8), P(60, 75), S)
    fill = [P(-g, 40), P(g, 40), P(g, 75), P(-g, 75)]
    hatch(sp, fill, "ANSI31", pscale("ANSI31", S, 0.8))
    line(sp, P(-g, 40), P(g, 40), "S-JFILL")
    sp.add_circle(P(0, 27), 11, dxfattribs=A("S-JOINT"))
    seal = [P(-g - c, 0), P(g + c, 0), P(g, c), P(g, 14), P(-g, 14), P(-g, c)]
    pline(sp, seal, "S-JOINT", close=True)
    hatch(sp, seal, "SOLID", 1, layer="S-JOINT")
    dim(sp, P(-g, 75), P(g, 75), P(0, 88), S)
    dim(sp, P(g + c + 25, 0), P(g + c + 25, 14), P(g + 40, 0), S, angle=90)
    dim(sp, P(g + c + 25, 14), P(g + c + 25, 40), P(g + 40, 0), S, angle=90)
    dim(sp, P(-g - c, -4), P(-g, -4), P(0, -14), S)
    note_cfg(xL=P(-80, 0)[0])
    k = P(-80, 0)
    leader(sp, P(-5, 55), k, "JOINT FILLER 20, RAKED OUT 40", S, "L", 26)
    leader(sp, P(-9, 27), k, "Ø25 CLOSED-CELL PE BACKER ROD (COMPRESSED)", S, "L", 26)
    leader(sp, P(-6, 8), k, "PU SEALANT 20 x 14 MIN. (ASTM C920 TYPE S, NS, CLASS 25) WITH PRIMER", S, "L", 26)
    leader(sp, P(-g - c / 2, c / 2), k, "10 x 10 ARRIS CHAMFER", S, "L", 26)


def groove_cj(ox, oy):
    """C.J. sealed groove at exposed face, plan, 1:2."""
    S = 2
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    pline(sp, [P(-60, 0), P(-8, 0), P(-8, 15), P(8, 15), P(8, 0), P(60, 0)], "S-CONC")
    line(sp, P(0, 15), P(0, 75), "S-JOINT")
    zbreak(sp, P(-60, -8), P(-60, 75), S)
    zbreak(sp, P(60, -8), P(60, 75), S)
    groove = [P(-8, 0), P(8, 0), P(8, 13), P(-8, 13)]
    hatch(sp, groove, "SOLID", 1, layer="S-JOINT")
    line(sp, P(-8, 14), P(8, 14), "S-JOINT")
    dim(sp, P(-8, 0), P(8, 0), P(0, -14), S)
    dim(sp, P(30, 0), P(30, 15), P(40, 0), S, angle=90)
    note_cfg(xL=P(-80, 0)[0])
    k = P(-80, 0)
    leader(sp, P(0, 45), k, "BITUMINOUS PAINT BOND BREAKER (2 COATS) ON 1ST-POUR FACE", S, "L", 26)
    leader(sp, P(-6, 14), k, "BOND-BREAKER TAPE AT GROOVE BASE", S, "L", 26)
    leader(sp, P(-4, 5), k, "PU SEALANT (ASTM C920) IN FORMED GROOVE 16 x 15, WITH PRIMER", S, "L", 26)
    text(sp, "1ST POUR", P(-55, 60), 2.0 * S, style="ANB")
    text(sp, "2ND POUR", P(55, 60), 2.0 * S, align=TA.BOTTOM_RIGHT, style="ANB")


def joint_face(ox, oy):
    """View on joint face (1:20): joint plane through stem, footing and key; dowel layout."""
    S = 20
    sp = msp
    P = lambda x, z: (ox + x, oy + z)
    outline = wall_outline(P)
    pline(sp, outline, "S-CONC", close=True)
    hatch(sp, outline, "ANSI31", pscale("ANSI31", S, 1.6))
    zigzag(sp, P(0, TOF), P(TS, TOF), S)                                  # horizontal construction joint
    lean = [P(0, BOF - LEAN), P(KX0, BOF - LEAN), P(KX0, BOF), P(0, BOF)]
    pline(sp, lean, "S-CONC-HIDN", close=True)
    line(sp, P(-450, 0), P(0, 0), "S-SOIL")
    earth_band(sp, [P(-450, 0), P(0, 0)], 60, S)
    line(sp, P(TS, TOW), P(1250, TOW), "S-SOIL")
    for z in (450, 150):
        dowel_end(sp, P(TS / 2, z), rdot(16, S))
    zf = (TOF + BOF) / 2
    for x in (150, 450, 750, 1050):
        dowel_end(sp, P(x, zf), rdot(16, S))
    pline(sp, [P(-15, -100), P(-15, TOW + 15), P(TS + 15, TOW + 15)], "S-JOINT")
    pline(sp, [P(TS + 15, TOW - 50), P(TS + 15, TOF + 15), P(TS + 520, TOF + 15)], "S-GEOT")
    dim(sp, P(TS / 2, TOW), P(TS / 2, 450), P(-230, 0), S, angle=90)
    dim(sp, P(TS / 2, 450), P(TS / 2, 150), P(-230, 0), S, angle=90)
    xs = [0, 150, 450, 750, 1050, B]
    for a, b in zip(xs[:-1], xs[1:]):
        dim(sp, P(a, zf), P(b, zf), P(0, KBOT - 150), S)
    note_cfg(xR=P(1330, 0)[0])
    k = P(1330, 0)
    leader(sp, P(100, TOW + 15), k, "PU SEALANT ON BACKER ROD: EXPOSED FACE TO 100 BELOW GROUND & ACROSS TOP", S, "R", 45)
    leader(sp, P(TS / 2, 450), k, "RB16@300 DOWELS AT STEM CENTRE LINE (2 NOS.)", S, "R", 45, ring=16)
    leader(sp, P(TS + 300, TOF + 15), k, "GEOTEXTILE STRIP OVER JOINT: SOIL FACE OF STEM + TOP OF HEEL", S, "R", 45)
    leader(sp, P(1050, zf), k, "RB16@300 DOWELS AT FOOTING MID-DEPTH -0.275 (4 NOS.)", S, "R", 45, ring=16)
    leader(sp, P(B, -560), k, "JOINT PLANE THROUGH STEM, FOOTING & SHEAR KEY: FILLER 20 (E.J.) / BOND BREAKER (C.J.)", S, "R", 45)
    leader(sp, P(KX0 - 20, BOF - 25), k, "LEAN CONCRETE CONTINUOUS (NO JOINT)", S, "R", 45)
    text(sp, "BOUNDARY", P(-430, 60), 2.0 * S, style="ANB")
    text(sp, "RETAINED FILL", P(700, TOW + 160), 2.0 * S, style="ANB")


def dowel_detail(ox, oy):
    S = 5
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    g = EJG
    pline(sp, [P(-g - 300, -8), P(g + 300, -8), P(g + 300, 8), P(-g - 300, 8)], "S-DWL", close=True)
    pline(sp, [P(g, -12), P(g + 325, -12), P(g + 325, 12), P(g, 12)], "S-DWL-SLV", close=True)
    line(sp, P(g + 325, -14), P(g + 325, 14), "S-DWL")
    line(sp, P(-g, -70), P(-g, 70), "S-JOINT")
    line(sp, P(g, -70), P(g, 70), "S-JOINT")
    dim(sp, P(-g - 300, 0), P(-g, 0), P(0, 60), S)
    dim(sp, P(-g, 0), P(g, 0), P(0, 60), S)
    dim(sp, P(g, 0), P(g + 300, 0), P(0, 60), S)
    dim(sp, P(g + 300, 0), P(g + 325, 0), P(0, 100), S)
    note_cfg(yB=P(0, -110)[1])
    kB = P(0, -110)
    leader(sp, P(-250, -8), kB, "RB16 (SR24, TIS 20-2559) L = 600, SAW-CUT, DEBURRED; ALIGN NORMAL TO JOINT WITHIN 1:100 BOTH PLANES", S, "B", 44)
    leader(sp, P(-150, -8), kB, "BONDED HALF - CAST IN 1ST POUR", S, "B", 30)
    leader(sp, P(g, -50), kB, "JOINT FACE (E.J. GAP 20 / C.J. TIGHT)", S, "B", 30)
    leader(sp, P(g + 150, -12), kB, "PVC SLEEVE Ø20 (TIS 17) + GREASE; END CAP WITH 25 VOID (E.J. ONLY)", S, "B", 40)


# ======================================================================= CORNER & WALL END (1:20 / 1:25)
CLA = 2000        # leg length shown in corner views


def corner_plan(ox, oy):
    """External corner, site in +x,+y quadrant; property lines on x=0 and y=0. Plan section at +0.300."""
    S = 20
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    LA = LB = CLA
    EJ0, EJ1 = B, B + 2 * EJG                         # E.J. across leg B at 1200..1220
    # hidden footing / keys first, then stems
    pline(sp, [P(LA, B), P(B, B), P(B, LB)], "S-CONC-HIDN")
    line(sp, P(KX0, KX0), P(LA, KX0), "S-CONC-HIDN")
    line(sp, P(KX0, KX0), P(KX0, LB), "S-CONC-HIDN")
    for yy in (EJ0, EJ1):
        line(sp, P(TS, yy), P(B, yy), "S-CONC-HIDN")
    pline(sp, [P(LA, 350), P(650, 350)], "S-DRAIN-HIDN")
    sp.add_arc(P(650, 650), 300, 180, 270, dxfattribs=A("S-DRAIN-HIDN"))
    pline(sp, [P(350, 650), P(350, LB)], "S-DRAIN-HIDN")
    fill = [P(0, EJ0), P(TS, EJ0), P(TS, EJ1), P(0, EJ1)]
    hatch(sp, fill, "ANSI31", pscale("ANSI31", S, 0.6))
    pline(sp, [P(LA, 0), P(0, 0), P(0, EJ0), P(TS, EJ0), P(TS, TS), P(LA, TS)], "S-CONC")
    pline(sp, [P(0, LB), P(0, EJ1), P(TS, EJ1), P(TS, LB)], "S-CONC")
    zbreak(sp, P(LA, -250), P(LA, B + 250), S)
    zbreak(sp, P(-250, LB), P(B + 250, LB), S)
    line(sp, P(-500, 0), P(LA + 300, 0), "S-PROP")
    line(sp, P(0, -500), P(0, LB + 300), "S-PROP")
    # corner L-bars: legs 950 (DB12, soil face) / 800 (DB10, exposed face); laps 800 / 650 (psi_t = 1.3) with the
    # straight bars, which are drawn offset one bar diameter for clarity
    bar(sp, [P(YHB + 944, YHB), P(YHB, YHB), P(YHB, YHB + 944)], 12)                       # (9)
    bar(sp, [P(YHF + 795, YHF), P(YHF, YHF), P(YHF, YHF + 795)], 10, "S-REBR-SEC")         # (10)
    s2 = YHB + 944 - 800                                   # straight (2) start -> lap 800
    s4 = YHF + 795 - 650                                   # straight (4) start -> lap 650
    line(sp, P(s2, YHB - 12), P(LA - 60, YHB - 12), "S-REBR")
    line(sp, P(YHB - 12, s2), P(YHB - 12, EJ0 - 50), "S-REBR")
    line(sp, P(s4, YHF + 11), P(LA - 60, YHF + 11), "S-REBR-SEC")
    line(sp, P(YHF + 11, s4), P(YHF + 11, EJ0 - 50), "S-REBR-SEC")
    r = rdot(12, S)
    # vertical-bar dots drawn clear of the horizontal bars / bend (dot > true size at 1:20; offset for clarity)
    VB = YHB + LAYER_LW["S-REBR"] / 200 * S + r + 0.4 * S
    VF = YHF - LAYER_LW["S-REBR-SEC"] / 200 * S - r - 0.4 * S
    rin = 3.5 * 12 - LAYER_LW["S-REBR"] / 200 * S - r - 0.3 * S          # inside the (9) bend
    VC = YHB + 3.5 * 12 - rin / math.sqrt(2)
    for c in [(VC, VC), (VF, VF), (VF, VB), (VB, VF)]:
        dot(sp, P(*c), r)
    for x in (400, 600, 800, 1000, 1200, 1400, 1600, 1800):                                # (1) @200 typ.
        dot(sp, P(x, VB), r)
        dot(sp, P(VB, x) if x < EJ0 - 50 else P(VB, x + 60), r)
    # dims
    dim(sp, P(0, 0), P(TS, 0), P(0, -350), S)
    dim(sp, P(TS, 0), P(B, 0), P(0, -350), S)
    dim(sp, P(0, 0), P(0, EJ0), P(-350, 0), S, angle=90)
    dim(sp, P(0, EJ0), P(0, EJ1), P(-350, 0), S, angle=90)
    dim(sp, P(YHB - 6, YHB), P(YHB + 944, YHB), P(0, 560), S)
    dim(sp, P(s2, YHB), P(YHB + 944, YHB), P(0, 470), S, override={"dimpost": "<> LAP"})
    # labels
    note_cfg(xR=P(1350, 0)[0], yminR=P(0, 1330)[1])
    k = P(1350, 0)
    leader(sp, P(TS, EJ0 + 10), k, "E.J. (1/5002) ACROSS LEG B ON LINE OF LEG A HEEL", S, "R", 36)
    leader(sp, P(650 - 212, 650 - 212), k, "SUBSOIL DRAIN CONTINUOUS - SWEPT BEND; RODDING EYES AT ENDS", S, "R", 36)
    leader(sp, P(VC, VC), k, "CORNER VERTICALS: 4 BARS OF SHAPE (1)", S, "R", 36, ring=12)
    leader(sp, P(1000, VB), k, "DB12@200 VERT. (TYP.)", S, "R", 36, mark=1, ring=12)
    leader(sp, P(YHB + 500, YHB), k, "4-DB12 L-BARS 950 x 950 PER CORNER, SOIL FACE, AT LEVELS OF (2) - LAP 800", S, "R", 36, mark=9)
    leader(sp, P(YHF + 450, YHF), k, "4-DB10 L-BARS 800 x 800 PER CORNER, EXPOSED FACE - LAP 650 WITH (4)", S, "R", 36, mark=10)
    text(sp, "STRAIGHT BARS AND VERTICAL-BAR DOTS DRAWN OFFSET FOR CLARITY", P(250, -620), 2.0 * S)
    text(sp, "LEG A", P(1500, -150), 2.8 * S, align=TA.TOP_CENTER, style="ANB")
    text(sp, "LEG B", P(-150, 1900), 2.8 * S, align=TA.BOTTOM_CENTER, rot=90, style="ANB")
    text(sp, "P.L.", P(LA + 320, 0), 2.0 * S, align=TA.MIDDLE_LEFT)
    text(sp, "P.L.", P(0, LB + 320), 2.0 * S, align=TA.BOTTOM_CENTER)


def corner_footing(ox, oy):
    """Corner block footing reinforcement, plan at footing mid-depth -0.275 (1:25).
    EIT Table 3.2 item 4: one representative bar per set + distribution line."""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    LA = LB = 1800
    EJ0, EJ1 = B, B + 2 * EJG
    fill = [P(0, EJ0), P(B, EJ0), P(B, EJ1), P(0, EJ1)]
    hatch(sp, fill, "ANSI31", pscale("ANSI31", S, 0.6))
    # stems above (hidden), keys below (hidden)
    for pts in ([P(LA, TS), P(TS, TS), P(TS, LB)], [P(LA, KX0), P(KX0, KX0), P(KX0, LB)]):
        pline(sp, pts, "S-CONC-HIDN")
    # footing cut outline
    pline(sp, [P(LA, 0), P(0, 0), P(0, EJ0), P(LA, EJ0)], "S-CONC")
    pline(sp, [P(0, LB), P(0, EJ1), P(B, EJ1), P(B, LB)], "S-CONC")
    line(sp, P(B, EJ0), P(B, EJ1), "S-CONC")
    zbreak(sp, P(LA, -200), P(LA, EJ0 + 200), S)
    zbreak(sp, P(-200, LB), P(B + 200, LB), S)
    # leg A C-bars (run in y), continuous through the corner block
    xa = 1450
    bar(sp, [P(xa, XCEND), P(xa, XTOE)], 12)
    dist_line(sp, P(XTOE + 50, 750), P(LA - 60, 750), P(xa, 750), S)
    # leg B C-bars in the block, at 90 deg (two-way cage), and in leg B beyond the E.J.
    yb1, yb2 = 500, 1500
    bar(sp, [P(XCEND, yb1), P(XTOE, yb1)], 12)
    bar(sp, [P(XCEND, yb2), P(XTOE, yb2)], 12)
    dist_line(sp, P(420, XTOE + 50), P(420, EJ0 - 50), P(420, yb1), S)
    dist_line(sp, P(420, EJ1 + 50), P(420, LB - 60), P(420, yb2), S)
    # longitudinal bars: leg A continuous to 75 cover at leg B toe; leg B stops 50 clear of E.J.
    line(sp, P(XTOE, 250), P(LA - 60, 250), "S-REBR")
    line(sp, P(250, EJ1 + 50), P(250, LB - 60), "S-REBR")
    note_cfg(xR=P(LA + 150, 0)[0], yT=P(0, LB + 250)[1])
    k, kT = P(LA + 150, 0), P(0, LB + 250)
    leader(sp, P(B / 2, EJ1), k, "E.J. ON LINE OF LEG A HEEL - NO RE-ENTRANT CORNER IN THE BLOCK", S, "R", 36)
    leader(sp, P(xa, 1000), k, "DB12@200 C-BARS LEG A - CONTINUOUS THROUGH CORNER BLOCK", S, "R", 36, mark=5)
    leader(sp, P(1000, yb1), k, "DB12@200 C-BARS AT 90° ACROSS THE CORNER BLOCK (TWO-WAY CAGE)", S, "R", 36, mark=5)
    leader(sp, P(1600, 250), k, "LEG A CONTINUOUS TO 75 COVER AT LEG B TOE", S, "R", 36, mark=6)
    leader(sp, P(250, 1700), kT, "LEG B - STOP 50 CLEAR OF E.J.", S, "T", 30, mark=6)
    leader(sp, P(900, yb2), kT, "DB12@200 C-BARS LEG B - STOP 50 CLEAR OF E.J.", S, "T", 34, mark=5)
    dim(sp, P(0, 0), P(B, 0), P(0, -250), S)
    dim(sp, P(0, 0), P(0, EJ0), P(-250, 0), S, angle=90)
    text(sp, "CORNER BLOCK (CAST WITH LEG A)", P(80, 1030), 2.0 * S, style="ANB")


def wall_end_plan(ox, oy):
    S = 20
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    LE = 1300
    pline(sp, [P(TS, TS), P(0, TS), P(0, B), P(LE, B)], "S-CONC-HIDN")
    line(sp, P(0, KX0), P(LE, KX0), "S-CONC-HIDN")
    pline(sp, [P(LE, 0), P(CH, 0), P(0, CH), P(0, TS), P(LE, TS)], "S-CONC")
    zbreak(sp, P(LE, -250), P(LE, B + 250), S)
    line(sp, P(-400, 0), P(LE + 250, 0), "S-PROP")
    xe = C_EXP + 6
    Ru0 = (YHB - YHF) / 2.0                                   # U end drawn as a true semicircle
    u = sp.add_lwpolyline([(P(xe + 900, YHB)[0], P(0, YHB)[1], 0), (P(xe + Ru0, YHB)[0], P(0, YHB)[1], 1.0),
                           (P(xe + Ru0, YHF)[0], P(0, YHF)[1], 0), (P(xe + 900, YHF)[0], P(0, YHF)[1], 0)],
                          format="xyb", dxfattribs=A("S-REBR"))                           # (11)
    u.dxf.flags = u.dxf.flags | 128
    line(sp, P(xe + 100, YHB - 12), P(LE - 60, YHB - 12), "S-REBR")
    line(sp, P(xe + 100, YHF + 11), P(LE - 60, YHF + 11), "S-REBR-SEC")
    # end verticals of shape (1) sit INSIDE the U-bend, touching its inner face (tied), 45 deg either side
    # of the wall axis: centre of bend c, U centre-line radius Ru, bar centre at Ru - db_U/2 - db_V/2
    Ru = (YHB - YHF) / 2.0
    cxu, cyu = xe + Ru, (YHB + YHF) / 2.0
    r = rdot(12, S)
    rv = Ru - 0.25 * S - r - 0.3 * S          # drawn dot + U pen half-width + visible gap (dot > true size at 1:20)
    EV = [(cxu - rv * math.cos(math.radians(a_)), cyu + rv * math.sin(math.radians(a_))) for a_ in (60, -60)]
    for q in EV:
        dot(sp, P(*q), r)
    dim(sp, P(xe, 0), P(xe + 900, 0), P(0, -300), S)       # U leg = 100 (straight bars stop short of the bend) + lap 800
    note_cfg(xL=P(-250, 0)[0])
    k = P(-250, 0)
    leader(sp, P(0, 600), k, "FOOTING & KEY END FLUSH WITH STEM END (HIDDEN)", S, "L", 36)
    leader(sp, P(300, YHB), k, "4-DB12 U-BARS PER END (HORIZ.) - LAP 800 WITH (2)/(4)", S, "L", 36, mark=11)
    leader(sp, P(*EV[0]), k, "2 END VERTICALS OF SHAPE (1), INSIDE U-BEND, TIED", S, "L", 36, ring=12)
    leader(sp, P(8, 8), k, "20x20 CHAMFER", S, "L", 36)
    text(sp, "P.L.", P(LE + 270, 0), 2.0 * S, align=TA.MIDDLE_LEFT)


def bar_planes(ox, oy):
    """Bar plane arrangement from a joint face (plan, 1:10): x across the wall (0 = exposed face),
    y along the wall (0 = joint face). Transverse sets in alternate planes so (1), (5), (3) never clash."""
    S = 10
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L = 650
    pline(sp, [P(0, L), P(0, 0), P(B, 0), P(B, L)], "S-CONC-HIDN")
    line(sp, P(TS, 0), P(TS, L), "S-CONC-HIDN")
    line(sp, P(KX0, 0), P(KX0, L), "S-CONC-HIDN")
    line(sp, P(-120, 0), P(B + 120, 0), "S-JOINT")
    zbreak(sp, P(-120, L), P(B + 120, L), S)
    for y in range(PLANES["1"], L, 200):
        bar(sp, [P(XB - 6, y), P(XB + 300, y)], 12)                       # (1) tail
        dot(sp, P(XB, y), rdot(12, S))                                    # (1) vertical leg
        bar(sp, [P(KL, y), P(KR, y)], 12)                                 # (7) key U
    for y in range(PLANES["5"], L, 200):
        bar(sp, [P(XTOE, y), P(XCEND, y)], 12)                            # (5) C-bar
    for y in range(PLANES["3"], L, 400):
        bar(sp, [P(XF, y), P(XF + 200, y)], 10, "S-REBR-SEC")             # (3) tail
        dot(sp, P(XF, y), rdot(10, S), "S-REBR-SEC")
    ys = [0, 50, 100, 150, 250, 350, 450, 550]
    for a, b in zip(ys[:-1], ys[1:]):
        dim(sp, P(0, a), P(0, b), P(-160, 0), S, angle=90)
    note_cfg(yB=P(0, -170)[1])
    kB = P(0, -170)
    leader(sp, P(70, PLANES["3"]), kB, "(3): 100, 500, 900 ... @400", S, "B", 30, mark=3)
    leader(sp, P(300, PLANES["1"]), kB, "(1) & (7): 50, 250, 450 ... @200 FROM JOINT FACE", S, "B", 38, mark=1)
    leader(sp, P(700, PLANES["5"]), kB, "(5): 150, 350, 550 ... @200", S, "B", 30, mark=5)
    text(sp, "JOINT FACE (E.J. / C.J.)", P(B + 140, 0), 2.0 * S, align=TA.MIDDLE_LEFT, style="ANB")
    text(sp, "P.L.", P(0, L + 60), 2.0 * S, align=TA.BOTTOM_CENTER)
    text(sp, "STEM", P(TS / 2, L + 60), 2.0 * S, align=TA.BOTTOM_LEFT)
    text(sp, "HEEL", P(600, L + 60), 2.0 * S, align=TA.BOTTOM_CENTER)
    text(sp, "KEY", P((KX0 + B) / 2, L + 60), 2.0 * S, align=TA.BOTTOM_CENTER)


# ======================================================================= place model views
EXT = {
    "SEC": capture(section_a, 0, 0),
    "PLAN": capture(plan_view, 0, 20000),
    "ELEV": capture(elevation_view, 0, 12000),
    "PEL": capture(partial_elevation, 0, 30000),
    "EJ": capture(stem_plan_section, 60000, 0, "EJ"),
    "DW": capture(dowel_detail, 60000, -3000),
    "SEJ": capture(sealant_ej, 60000, -6000),
    "CJ": capture(stem_plan_section, 80000, 0, "CJ"),
    "JF": capture(joint_face, 80000, -4000),
    "GCJ": capture(groove_cj, 80000, -8000),
    "CO": capture(corner_plan, 100000, 0),
    "END": capture(wall_end_plan, 100000, -5000),
    "CF": capture(corner_footing, 100000, -10000),
    "BP": capture(bar_planes, 120000, 0),
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
    revs = [("A", "ISSUED FOR APPROVAL", "28/09/2026"),
            ("B", "HORIZ. BAR LAPS", PROJ["date"])]
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
    text(ps, "SITE BOUNDARY - SEE SITE PLAN", (xc, (by0 + by1) / 2 + 2.5), 2.0, align=TA.MIDDLE_CENTER)
    text(ps, "HEAVY LINE = RETAINING WALL", (xc, (by0 + by1) / 2 - 2.5), 2.0, align=TA.MIDDLE_CENTER)

    # status stamp + sheet notes (text area, EIT 2.2.2.2)
    sy = y_kp1 + 3
    pline(ps, [(x0 + 3, sy), (x1 - 3, sy), (x1 - 3, sy + 12), (x0 + 3, sy + 12)], "S-TITLE", close=True)
    text(ps, "FOR APPROVAL", (xc, sy + 8.2), 2.8, align=TA.MIDDLE_CENTER, style="ANB")
    text(ps, "NOT FOR CONSTRUCTION", (xc, sy + 3.8), 2.8, align=TA.MIDDLE_CENTER, style="ANB")
    text(ps, "NOTES", (tx, FY1 - 3.5), 2.0, align=TA.MIDDLE_LEFT, style="ANB")
    notes = ("1. READ WITH GENERAL NOTES " + dwg_no("1001") + ".\\P"
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


# ---------------------------------------------------------------- 1001 general notes
def notes(items):
    """join note paragraphs; blank string = small gap"""
    return "\\P".join(items)


GEN1 = notes([
    hdr("1.  GENERAL"),
    "1.1  THESE DRAWINGS SHOW A TYPICAL L-SHAPED RC CANTILEVER RETAINING WALL (HEEL ONLY, NO TOE) BUILT ALONG THE PROPERTY LINE. READ WITH THE SITE PLAN AND BOUNDARY SURVEY (BY OTHERS).",
    "1.2  DIMENSIONS ARE IN MILLIMETRES. LEVELS ARE IN METRES (3 DECIMALS) REFERRED TO SITE DATUM ±0.000 = EXISTING GROUND OF THE ADJACENT LAND AT THE WALL LINE. RELATE TO THE PROJECT BENCHMARK BEFORE SETTING OUT.",
    "1.3  THE PROPERTY LINE SHALL BE LOCATED BY A LICENSED SURVEYOR. THE FRONT FACE OF THE WALL IS ON THE PROPERTY LINE; NO PART OF THE WALL, FOOTING OR KEY SHALL PROJECT BEYOND IT.",
    "1.4  DO NOT SCALE FROM THE DRAWINGS. REPORT ANY DISCREPANCY TO THE ENGINEER BEFORE WORK PROCEEDS.",
    "1.5  ISSUE STATUS: FOR CLIENT AND LOCAL-AUTHORITY APPROVAL - NOT FOR CONSTRUCTION UNTIL RE-ISSUED 'FOR CONSTRUCTION'.",
    "1.6  DRAFTING STANDARD: EIT 011006-19.",
    "",
    hdr("2.  DESIGN CRITERIA"),
    "2.1  BUILDING CONTROL ACT B.E. 2522 (AS AMENDED) AND RELATED MINISTERIAL REGULATIONS.",
    "2.2  RC DESIGN: EIT 1008-38 (STRENGTH DESIGN), LOAD FACTOR 1.7 ON EARTH PRESSURE AND SURCHARGE. DEVELOPMENT, HOOKS AND LAPS: ACI 318-19.",
    "2.3  RETAINED HEIGHT 0.60 m MAX. ABOVE ADJACENT GROUND; DESIGN HEIGHT 1.00 m (TOP OF WALL TO FOUNDING LEVEL -0.400).",
    "2.4  SOIL: γ = 18 kN/m³ (1.8 t/m³); AT-REST K0 = 0.50 (COMPACTED BACKFILL); BASE FRICTION μ = 0.40; PASSIVE RESISTANCE AT SHEAR KEY ONLY (0.5 Kp, Kp = 3.0).",
    "2.5  SURCHARGE 10 kPa (1.0 t/m²) UNIFORM ON RETAINED SIDE - LIGHT VEHICLES (CARS / PICK-UPS). TRUCKS AND CONSTRUCTION PLANT NOT PERMITTED WITHIN 1.5 m OF THE WALL.",
    "2.6  ALLOWABLE BEARING qa ≥ 50 kPa (5 t/m²) AT -0.450 - TO BE VERIFIED ON SITE BY THE ENGINEER.",
    "2.7  GROUNDWATER ASSUMED BELOW -0.700. WALL DESIGNED AS FULLY DRAINED (NOTE 6.4).",
    "2.8  SEISMIC EARTH PRESSURE NOT CONSIDERED (RETAINED HEIGHT ≤ 1.0 m).",
])

GEN2 = notes([
    hdr("4.  MATERIALS (THAI INDUSTRIAL STANDARDS, TIS)"),
    "4.1  STRUCTURAL CONCRETE: fc' ≥ 240 ksc (24 MPa) CYLINDER AT 28 DAYS (≈ 280 ksc CUBE). READY-MIXED TO TIS 213-2552; PORTLAND CEMENT TYPE I TO TIS 15 OR HYDRAULIC CEMENT TO TIS 2594; ADMIXTURES TO TIS 733; MAX. AGGREGATE 20 mm; MAX. W/C 0.50; SLUMP 75-100 mm. CYLINDERS: 3 PER POUR OR PER 25 m³, TESTED TO TIS 409.",
    "4.2  LEAN CONCRETE: 50 THK., MIX 1:3:5 BY VOLUME.",
    "4.3  DEFORMED BARS: SD40 TO TIS 24-2559 (fy ≥ 4,000 ksc / 390 MPa): DB10, DB12.",
    "4.4  ROUND BARS (DOWELS): SR24 TO TIS 20-2559 (fy ≥ 2,400 ksc / 235 MPa): RB16.",
    "4.5  SUBSOIL DRAIN: PVC Ø100 CLASS 8.5 TO TIS 17-2532, PERFORATED 2 ROWS Ø10 @ 100 STAGGERED (HOLES DOWN), IN GEOTEXTILE SOCK. OUTLET PIPES SOLID PVC Ø100 CL. 8.5.",
    "4.6  DRAINAGE STONE: CLEAN CRUSHED ROCK 12-25 mm, FINES < 0.075 mm ≤ 5%. DENSE-GRADED CRUSHED ROCK IS NOT ACCEPTABLE.",
    "4.7  GEOTEXTILE: NON-WOVEN NEEDLE-PUNCHED POLYPROPYLENE ≥ 200 g/m². (NO TIS - SUBMIT DATA SHEET FOR APPROVAL.)",
    "4.8  JOINT FILLER: PREFORMED BITUMINOUS FIBRE BOARD 20 THK., ASTM D1751. SEALANT: POLYURETHANE, ASTM C920 TYPE S, GRADE NS, CLASS 25, ON CLOSED-CELL PE BACKER ROD. (NO TIS.)",
    "",
    hdr("5.  REINFORCEMENT & COVER"),
    "5.1  CLEAR COVER: 40 STEM FACES; 50 TOP OF HEEL AND ON LEAN CONCRETE; 75 CAST AGAINST EARTH (FOOTING ENDS, SHEAR KEY).",
    "5.2  AT THE BOUNDARY, WHERE FORMWORK CANNOT BE STRIPPED, USE PERMANENT FIBRE-CEMENT FORMWORK SO THAT 40 COVER APPLIES; OTHERWISE PROVIDE 75.",
    "5.3  TENSION LAPS OF HORIZONTAL BARS (CLASS B 1.3 ℓd x ψt 1.3, > 300 FRESH CONCRETE BELOW): DB10 = 650, DB12 = 800, STAGGERED 50%. NO LAPS IN (1).",
    "5.4  BENDS COLD ON A MANDREL OF 6 db (ACI 318-19 TABLE 25.3.1); NO HEATING OR RE-BENDING. 90° HOOK EXTENSION ≥ 12 db.",
    "5.5  CONCRETE SPACERS OF THE SAME GRADE ≤ 1.0 m EACH WAY (NO TIMBER, BRICK OR PLASTIC ON THE SOIL FACE); 1.25 mm ANNEALED TIE WIRE AT EVERY OUTER INTERSECTION, ALTERNATE INSIDE. CAGE SELF-SUPPORTING BEFORE FORMS ARE CLOSED.",
    "5.6  HORIZONTAL AND LONGITUDINAL BARS STOP 50 CLEAR EACH SIDE OF E.J. AND C.J.; ONLY DOWELS CROSS JOINTS.",
    "5.7  TRANSVERSE BARS IN ALTERNATE PLANES - SEE 2/5005. BAR SCHEDULE 1/5005 IS INDICATIVE; CONTRACTOR TO ISSUE SHOP SCHEDULE.",
    "5.8  HOLD POINT: ENGINEER TO INSPECT REINFORCEMENT AND DOWELS BEFORE EACH POUR. COVER SHALL NEVER BE LESS THAN SPECIFIED.",
])

GEN3 = notes([
    hdr("6.  EARTHWORK & DRAINAGE"),
    "6.1  EXCAVATION SHALL NOT EXTEND BEYOND THE PROPERTY LINE; DO NOT UNDERMINE THE ADJACENT LAND OR EXCAVATE IT BELOW -0.450 WITHOUT THE ENGINEER'S APPROVAL. ON THE RETAINED SIDE CUT AT 2:1 (V:H) OR FLATTER WITH 150 WORKING SPACE; SUPPORT THE CUT IF UNSTABLE.",
    "6.2  REMOVE TOPSOIL AND SOFT MATERIAL. COMPACT SUBGRADE TO ≥ 95% STANDARD PROCTOR (DH-T 107); FIELD DENSITY BY SAND CONE (DH-T 603). ENGINEER TO INSPECT FORMATION BEFORE LEAN CONCRETE.",
    "6.3  BACKFILL ONLY WHEN CONCRETE IS ≥ 7 DAYS OLD AND ≥ 70% fc'. SELECTED FILL IN 200 LAYERS TO ≥ 95% MODIFIED PROCTOR (DH-T 108). WITHIN 1.0 m OF THE WALL USE HAND-OPERATED PLATE COMPACTORS ONLY.",
    "6.4  NO WEEP HOLES THROUGH THE WALL - NO WATER SHALL DISCHARGE ONTO THE ADJACENT LAND. SUBSOIL DRAIN FALLS ≥ 1:200 TO OUTLETS AT EACH E.J. (≤ 24 m) OR THE LOW END, CONNECTED TO THE OWNER'S SITE DRAINAGE (BY OTHERS). RODDING EYE AT EACH END.",
    "6.5  NO VEHICLE SURCHARGE UNTIL CONCRETE IS 28 DAYS OLD AND BACKFILL IS COMPLETE.",
    "",
    hdr("7.  JOINTS"),
    "7.1  EXPANSION JOINT (E.J.) 20 FULL SECTION AT ≤ 24.0 m, AT CORNERS, WALL ENDS AGAINST OTHER STRUCTURES, AND CHANGES OF DIRECTION OR HEIGHT - 1/5002.",
    "7.2  CONTRACTION JOINT (C.J.): TIGHT FORMED JOINT AT ≤ 6.0 m, EQUALLY SPACED BETWEEN E.J. - 1/5003.",
    "7.3  CAST IN ALTERNATE BAYS; INFILL BAYS NOT EARLIER THAN 48 h AFTER THE ADJACENT POUR.",
    "7.4  HORIZONTAL CONSTRUCTION JOINT ONLY AT TOP OF FOOTING -0.150: ROUGHEN TO 5 mm AMPLITUDE, CLEAN, SATURATED SURFACE-DRY.",
    "",
    hdr("8.  CONSTRUCTION"),
    "8.1  CURE ALL CONCRETE ≥ 7 DAYS (WET CURING OR APPROVED COMPOUND).",
    "8.2  SIDE FORMS MAY BE STRIPPED AFTER 24 h. 20x20 CHAMFER ON ALL EXPOSED EDGES.",
    "8.3  WHERE THE FILL IS LOWER THAN +0.600, THE TOP OF WALL MAY STEP DOWN IN 150 INCREMENTS AT JOINTS; THE FOOTING SHALL NOT BE REDUCED.",
    "8.4  THE WALL IS NOT A VEHICLE BARRIER - WHEEL STOPS / KERBS BY OTHERS.",
])


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


def sheet_1001():
    ps = new_sheet(0)
    colw, gap = 100.0, 6.0
    x = FX0 + 4
    xs = [x + k * (colw + gap) for k in range(3)]
    mtext(ps, GEN1, (xs[0], FY1 - 5), 2.0, colw, spacing=1.15)
    mtext(ps, GEN2, (xs[1], FY1 - 5), 2.0, colw, spacing=1.15)
    mtext(ps, GEN3, (xs[2], FY1 - 5), 2.0, colw, spacing=1.15)
    # design summary table (col 1, bottom)
    yt = FY0 + 88
    text(ps, "3.  DESIGN SUMMARY (PER METRE RUN)", (xs[0], yt + 3), 2.8, "S-TITLE", style="ANB")
    rows = [
        ["OVERTURNING", "FS = 4.0", "≥ 2.0", "OK"],
        ["SLIDING (WITH SHEAR KEY)", "FS = 1.57", "≥ 1.5", "OK"],
        ["SLIDING, DRAIN BLOCKED (ACCIDENTAL)", "FS = 1.03", "≥ 1.0", "OK *"],
        ["BEARING (RESULTANT IN MIDDLE THIRD)", "41 kPa", "≤ 50 kPa", "VERIFY"],
        ["STEM FLEXURE  Mu / φMn", "3.5 / 29.5", "kN·m/m", "OK"],
        ["HEEL FLEXURE  Mu / φMn", "25.1 / 37.4", "kN·m/m", "OK"],
        ["STEM BAR HOOK  ldh REQ. / AVAIL.", "150 / 176", "mm", "OK"],
    ]
    yb = table(ps, xs[0], yt, [0, 48, 68, 86, 100], ["CHECK", "RESULT", "LIMIT", ""], rows, rh=4.8)
    text(ps, "* DRAINS MUST BE KEPT CLEAR (MAINTENANCE BY OWNER).", (xs[0], yb - 3), 2.0)
    # legend (col 2, bottom)
    ly = FY0 + 80
    text(ps, "LEGEND - LINES (EIT 011006-19 TABLE 2.3)", (xs[1], ly + 3), 2.8, "S-TITLE", style="ANB")
    lrows = [
        ("S-CONC", "CONCRETE CUT (SECTIONS)", "0.35"),
        ("S-CONC-VIS", "CONCRETE SEEN (PLAN / ELEVATION)", "0.25"),
        ("S-CONC-HIDN", "HIDDEN / BELOW GROUND (GREY)", "0.25"),
        ("S-REBR", "MAIN REINFORCEMENT, DOWELS", "0.50"),
        ("S-REBR-SEC", "SECONDARY REINFORCEMENT (DB10)", "0.35"),
        ("S-DIMS", "DIMENSION / LEADER", "0.18"),
        ("S-CUTL", "CUTTING PLANE", "0.25"),
        ("S-PROP", "PROPERTY LINE", "0.25"),
        ("S-GEOT", "GEOTEXTILE", "0.18"),
        ("S-CJOINT", "CONSTRUCTION JOINT (ZIG-ZAG)", "0.25"),
        ("S-HATCH", "HATCH (GREY)", "0.13"),
    ]
    yy = ly - 2.5
    for lay, desc, pen in lrows:
        if lay == "S-CJOINT":
            zigzag(ps, (xs[1], yy), (xs[1] + 22, yy), 1)
        else:
            line(ps, (xs[1], yy), (xs[1] + 22, yy), lay)
        text(ps, desc, (xs[1] + 26, yy), 2.0, align=TA.MIDDLE_LEFT)
        text(ps, pen + " mm", (xs[1] + 82, yy), 2.0, align=TA.MIDDLE_LEFT)
        yy -= 3.8
    ab = notes([hdr("ABBREVIATIONS"),
                "DB = DEFORMED BAR   RB = ROUND BAR   @ = SPACING C/C   (T) / (B) = TOP / BOTTOM",
                "E.J. / C.J. = EXPANSION / CONTRACTION JOINT   T.O. / B.O. = TOP OF / BOTTOM OF",
                "THK. = THICKNESS   TYP. = TYPICAL   P.L. = PROPERTY LINE   CL. = CLASS",
                "PLOT: NRW-EIT.ctb - ALL BLACK, ACI 8 LAYERS AT 50 % GREY; OBJECT LINEWEIGHTS."])
    mtext(ps, ab, (xs[1], yy - 1), 2.0, colw)
    # drawing list (col 3, bottom)
    dl = [hdr("DRAWING LIST")] + [f"{dwg_no(s)}    " + " ".join(t).replace(",", "") for s, t, _ in SHEETS]
    mtext(ps, notes(dl), (xs[2], FY0 + 38), 2.0, colw, spacing=1.15)


def sheet_3001():
    ps = new_sheet(1)
    top = FY1 - 3
    px, pw, ph = viewport(ps, "PLAN", 100, FX0, top, AREA_W)
    view_title(ps, None, top - ph - 6, "TYPICAL PLAN - JOINT LAYOUT", "1:100", ("1", "3001"))
    top2 = top - ph - 16
    px, pw2, ph2 = viewport(ps, "ELEV", 100, FX0, top2, AREA_W)
    view_title(ps, None, top2 - ph2 - 6, "LONGITUDINAL ELEVATION - VIEWED FROM ADJACENT LAND", "1:100", ("2", "3001"))
    top3 = top2 - ph2 - 16
    px3, pw3, ph3 = viewport(ps, "PEL", 25, FX0, top3, 238)
    view_title(ps, None, top3 - ph3 - 6, "PARTIAL ELEVATION AT E.J. - VIEWED FROM ADJACENT LAND", "1:25", ("3", "3001"))
    # joint schedule + layout notes (right of partial elevation / bottom)
    tx0 = FX0 + 242
    n = notes([
        hdr("LAYOUT NOTES"),
        "1. A TYPICAL 24 m PANEL IS SHOWN. WALL LENGTH AND ALIGNMENT VARY: SET OUT JOINTS FROM WALL ENDS AND CORNERS TO THE SITE PLAN; ADJUST C.J. TO EQUAL BAYS ≤ 6.0 m.",
        "2. EVERY JOINT RUNS IN ONE VERTICAL PLANE THROUGH STEM, FOOTING AND SHEAR KEY; LEAN CONCRETE IS CONTINUOUS (2/5003).",
        "3. CORNERS AND FREE ENDS: SEE 5004.",
        "4. SUBSOIL DRAIN BEHIND THE STEM ON THE HEEL, FALL ≥ 1:200, OUTLETS AT E.J. TO THE OWNER'S DRAINAGE. NO DISCHARGE ONTO THE ADJACENT LAND.",
    ])
    mtext(ps, n, (tx0, top3 - 1), 2.0, TBX - tx0 - 3, spacing=1.1)
    yt = FY0 + 27
    text(ps, "JOINT SCHEDULE", (FX0 + 5, yt + 3), 2.8, "S-TITLE", style="ANB")
    table(ps, FX0 + 5, yt, [0, 16, 50, 283, 305],
          ["MARK", "TYPE", "LOCATION / SPACING", "DETAIL"],
          [["E.J.", "EXPANSION JOINT 20", "≤ 24.0 m C/C; AT CORNERS, WALL ENDS AGAINST OTHER STRUCTURES, CHANGES OF DIRECTION OR HEIGHT", "1/5002"],
           ["C.J.", "CONTRACTION JOINT", "≤ 6.0 m C/C, EQUALLY SPACED BETWEEN E.J.; CAST IN ALTERNATE BAYS (≥ 48 h)", "1/5003"],
           ["CONST.", "CONSTRUCTION JOINT", "HORIZONTAL AT TOP OF FOOTING -0.150 ONLY, ROUGHENED TO 5 mm", "A/5001"]],
          rh=4.8, bold_first_col=True)


def sheet_5001():
    ps = new_sheet(2)
    top = FY1 - 2
    px, pw, ph = viewport(ps, "SEC", 10, FX0, top, AREA_W)
    view_title(ps, None, top - ph - 6, "SECTION A - TYPICAL RETAINING WALL SECTION",
               "1:10", ("A", "3001"), triangles=True,
               note="CLEAR COVER 40 STEM FACES, 50 TOP OF HEEL & ON LEAN CONCRETE, 75 AGAINST EARTH U.N.O.")
    yb = top - ph - 22
    k1 = notes([
        hdr("REINFORCEMENT KEY"),
        "(1)  DB12@200 VERT., SOIL FACE - 90° HOOK, TAIL 300 ON (6), NO LAPS",
        "(2)  DB12@200 HORIZ., SOIL FACE, INSIDE (1)",
        "(3)  DB10@400 VERT., EXPOSED FACE - TAIL 200",
        "(4)  DB10@200 HORIZ., EXPOSED FACE, INSIDE (3)",
    ])
    k2 = notes([
        "",
        "(5)  DB12@200 C-BAR, CLOSED AT TOE (TOP & BOTTOM LEGS)",
        "(6)  6+6-DB12 LONG. (T & B), INSIDE (5)",
        "(7)  DB12@200 U-BAR IN SHEAR KEY",
        "(8)  2-DB12 LONG. IN SHEAR KEY",
    ])
    k3 = notes([
        hdr("BAR DRAWING CONVENTION"),
        "BARS ON CENTRELINE; BENDS DRAWN AT R = 3.5 db (6 db MANDREL).",
        "TRANSVERSE BARS IN ALTERNATE PLANES - 2/5005.",
        "BAR SCHEDULE (INDICATIVE) - 1/5005.",
    ])
    mtext(ps, k1, (FX0 + 4, yb), 2.0, 100)
    mtext(ps, k2, (FX0 + 106, yb), 2.0, 100)
    mtext(ps, k3, (FX0 + 212, yb), 2.0, 104)


def sheet_5002():
    ps = new_sheet(3)
    top = FY1 - 2
    px, pw, ph = viewport(ps, "EJ", 5, FX0, top)
    view_title(ps, None, top - ph - 6, "EXPANSION JOINT (E.J.) - PLAN SECTION THROUGH STEM AT +0.300", "1:5", ("1", "5002"))
    top2 = top - ph - 17
    px, pw2, ph2 = viewport(ps, "DW", 5, FX0, top2)
    view_title(ps, None, top2 - ph2 - 6, "SLIP DOWEL DETAIL", "1:5", ("2", "5002"))
    rx = FX0 + 206
    n = notes([
        hdr("E.J. - INSTALLATION"),
        "1. FILLER 20 THK. FULL HEIGHT AND WIDTH OF STEM, FOOTING AND SHEAR KEY, FIXED TO THE 1ST-POUR FACE BEFORE CASTING THE 2ND POUR.",
        "2. ALL REINFORCEMENT DISCONTINUED; ONLY RB16 SLIP DOWELS CROSS THE JOINT (2 IN STEM, 4 IN FOOTING - 2/5003).",
        "3. DOWELS FIXED THROUGH A DRILLED STOP-END; SLEEVE AND END CAP ON THE 2ND-POUR SIDE. CHECK ALIGNMENT BEFORE CASTING.",
        "4. RAKE OUT FILLER 40 DEEP ON THE EXPOSED FACE AND TOP OF WALL; INSERT BACKER ROD; PRIME AND SEAL (3/5002).",
        "5. GEOTEXTILE STRIP ON SOIL FACE AND TOP OF HEEL, BONDED ONE SIDE ONLY, BEFORE BACKFILLING.",
        "6. INSPECT AND RESEAL AS REQUIRED (MAINTENANCE BY OWNER).",
    ])
    mtext(ps, n, (rx, top - 2), 2.0, TBX - rx - 3, spacing=1.1)
    ext = EXT["SEJ"]
    ph3 = (ext[3] - ext[1]) / 2 + 2 * PAD
    top3 = FY0 + 14 + ph3
    viewport(ps, "SEJ", 2, rx - 2, top3, TBX - rx + 2)
    view_title(ps, None, top3 - ph3 - 6, "E.J. SEALANT", "1:2", ("3", "5002"))


def sheet_5003():
    ps = new_sheet(4)
    top = FY1 - 2
    px, pw, ph = viewport(ps, "CJ", 5, FX0, top)
    view_title(ps, None, top - ph - 6, "CONTRACTION JOINT (C.J.) - PLAN SECTION THROUGH STEM AT +0.300", "1:5", ("1", "5003"))
    top2 = top - ph - 17
    px, pw2, ph2 = viewport(ps, "JF", 20, FX0 + 10, top2)
    view_title(ps, None, top2 - ph2 - 6, "JOINT PLANE - VIEW ON JOINT FACE (E.J. / C.J.)", "1:20", ("2", "5003"))
    rx = FX0 + 206
    n = notes([
        hdr("C.J. - INSTALLATION"),
        "1. FORM THE JOINT WITH A STOP-END DRILLED FOR DOWELS. AFTER STRIPPING, PAINT THE HARDENED FACE WITH 2 COATS OF BITUMINOUS PAINT (BOND BREAKER).",
        "2. ALL HORIZONTAL AND LONGITUDINAL BARS STOP 50 CLEAR; ONLY RB16 SLIP DOWELS CROSS THE JOINT.",
        "3. FORM A 16 x 15 GROOVE ON THE EXPOSED FACE AND TOP OF WALL; SEAL ON BOND-BREAKER TAPE (3/5003).",
        "4. ADJACENT BAY NOT EARLIER THAN 48 h AFTER THE FIRST POUR.",
        "",
        hdr("JOINT PLANE"),
        "ONE VERTICAL PLANE THROUGH STEM, FOOTING AND SHEAR KEY; LEAN CONCRETE CONTINUOUS. DOWELS: 2 IN STEM AT CENTRE LINE (+0.450, +0.150); 4 IN FOOTING AT MID-DEPTH (-0.275) @ 300.",
    ])
    mtext(ps, n, (rx, top - 2), 2.0, TBX - rx - 3, spacing=1.1)
    ext = EXT["GCJ"]
    ph3 = (ext[3] - ext[1]) / 2 + 2 * PAD
    top3 = FY0 + 14 + ph3
    viewport(ps, "GCJ", 2, rx - 2, top3, TBX - rx + 2)
    view_title(ps, None, top3 - ph3 - 6, "C.J. SEALED GROOVE", "1:2", ("3", "5003"))


def sheet_5004():
    ps = new_sheet(5)
    top = FY1 - 2
    px, pw, ph = viewport(ps, "CO", 20, FX0, top)
    view_title(ps, None, top - ph - 6, "TYPICAL CORNER - PLAN AT +0.300", "1:20", ("1", "5004"))
    rx = FX0 + pw + 4
    px3, pw3, ph3 = viewport(ps, "END", 20, rx, top)
    view_title(ps, None, top - ph3 - 6, "WALL FREE END - PLAN AT +0.300", "1:20", ("3", "5004"))
    top2 = top - ph3 - 16
    px2, pw2, ph2 = viewport(ps, "CF", 25, rx, top2)
    view_title(ps, None, top2 - ph2 - 6, "CORNER BLOCK FOOTING - PLAN AT -0.275", "1:25", ("2", "5004"))
    n = notes([
        hdr("CORNER & END NOTES"),
        "1. THE CORNER BLOCK (1200 x 1200) IS CAST MONOLITHIC WITH LEG A. THE E.J. IN LEG B IS ON THE LINE OF THE LEG A HEEL, SO THE BLOCK HAS NO RE-ENTRANT CORNER.",
        "2. STEM: HORIZONTAL BARS MADE CONTINUOUS AROUND THE CORNER WITH L-BARS (9) / (10); NEVER ACROSS AN E.J. OR C.J.",
        "3. FOOTING: LEG A C-BARS (5) AND LONGITUDINAL BARS (6) RUN THROUGH THE BLOCK; LEG B C-BARS (5) PLACED AT 90° ACROSS THE BLOCK FORM A TWO-WAY CAGE (2/5004).",
        "4. SHEAR KEYS AND LEAN CONCRETE CONTINUOUS THROUGH THE CORNER BLOCK.",
        "5. FREE END: STEM CLOSED WITH U-BARS (11) AND 2 END VERTICALS OF SHAPE (1); FOOTING AND KEY END FLUSH WITH THE STEM.",
        "6. WHERE THE WALL ABUTS ANOTHER STRUCTURE, PROVIDE AN E.J. (1/5002) WITHOUT DOWELS.",
    ])
    mtext(ps, n, (FX0 + 4, top - ph - 19), 2.0, pw - 6, spacing=1.1)


# ---------------------------------------------------------------- 5005 bar schedule
UW = {10: 0.617, 12: 0.888, 16: 1.578}       # kg/m (TIS 24 / TIS 20 nominal mass)
BAY = 6000


def n_planes(first, step, length=BAY):
    return len(range(first, length - 50 + 1, step))


def r5(v):
    return int(5 * round(v / 5))


def bbs_rows():
    """(mark, db, shape, dims[(letter, mm)], nbends, spacing, count, remark) - outside dimensions."""
    d1 = [("A", 100), ("B", (ZT + 6) - (ZTAIL - 6)), ("C", 300 + 6)]
    d3 = [("A", 100), ("B", (ZT - 12 + 5) - (Z3TAIL - 5)), ("C", 200 + 5)]
    d5 = [("A", XCEND - (XTOE - 6)), ("B", (ZTT + 6) - (ZBB - 6)), ("C", XCEND - (XTOE - 6))]
    d7 = [("A", KTOP - (KZ - 6)), ("B", (KR + 6) - (KL - 6)), ("C", KTOP - (KZ - 6))]
    st = [("A", BAY - 100)]
    per_bay = [
        ("1", 12, "Z", d1, 2, "@200", n_planes(PLANES["1"], 200), "STEM VERT. SOIL FACE, NO LAPS"),
        ("2", 12, "-", st, 0, "@200", len(ZSTEMH), "STEM HORIZ. SOIL FACE"),
        ("3", 10, "Z", d3, 2, "@400", n_planes(PLANES["3"], 400), "STEM VERT. EXPOSED FACE"),
        ("4", 10, "-", st, 0, "@200", len(ZSTEMH), "STEM HORIZ. EXPOSED FACE"),
        ("5", 12, "C", d5, 2, "@200", n_planes(PLANES["5"], 200), "FOOTING C-BAR, CLOSED AT TOE"),
        ("6", 12, "-", st, 0, "6+6", 2 * len(XLONG), "FOOTING LONG. T & B"),
        ("7", 12, "U", d7, 2, "@200", n_planes(PLANES["7"], 200), "SHEAR KEY U-BAR"),
        ("8", 12, "-", st, 0, "2 NOS", 2, "SHEAR KEY LONG."),
    ]
    extra = [
        ("9", 12, "L", [("A", 950), ("B", 950)], 1, "PER CORNER", len(ZSTEMH), "CORNER L-BAR, SOIL FACE, LAP 800"),
        ("10", 10, "L", [("A", 800), ("B", 800)], 1, "PER CORNER", len(ZSTEMH), "CORNER L-BAR, EXPOSED FACE, LAP 650"),
        ("1", 12, "Z", d1, 2, "PER CORNER", 4, "CORNER VERTICALS, SHAPE (1)"),
        ("11", 12, "U", [("A", 906), ("B", (YHB + 6) - (YHF - 6)), ("C", 906)], 2, "PER END", len(ZSTEMH), "FREE-END U-BAR, LAP 800"),
        ("1", 12, "Z", d1, 2, "PER END", 2, "END VERTICALS, SHAPE (1)"),
        ("D", 16, "-", [("A", 600)], 0, "PER JOINT", 6, "RB16 SR24 SLIP DOWEL (2 STEM + 4 FTG)"),
    ]
    return per_bay, extra


def shape_sketch(ps, kind, x, y, w, h):
    """schematic shape in a table cell (square corners - bend radius is defined by note)"""
    m = 1.2
    x0, x1, y0, y1 = x + m, x + w - m, y - h + m, y - m
    xm = (x0 + x1) / 2
    pts = {
        "-": [(x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2)],
        "Z": [(x0, y1), (x0 + 2.5, y1), (x0 + 2.5, y0), (x1 - 6, y0)],
        "C": [(x1, y1), (x0 + 4, y1), (x0 + 4, y0), (x1, y0)],
        "U": [(xm - 3, y1), (xm - 3, y0), (xm + 3, y0), (xm + 3, y1)],
        "L": [(x0 + 4, y1), (x0 + 4, y0), (x1 - 4, y0)],
    }[kind]
    pline(ps, pts, "S-REBR")


def sheet_5005():
    ps = new_sheet(6)
    per_bay, extra = bbs_rows()
    x = FX0 + 4
    cols = [0, 11, 22, 46, 112, 128, 150, 162, 180, 196, 314]
    heads = ["MARK", "BAR", "SHAPE", "DIMENSIONS (mm, OUT-TO-OUT)", "CUT L. (m)", "SPACING", "NO.", "TOTAL (m)",
             "WT. (kg)", "REMARKS"]
    rh = 5.6

    def table_rows(rows, y_top, title, per):
        text(ps, title, (x, y_top + 3), 2.8, "S-TITLE", style="ANB")
        xs = [x + c for c in cols]
        n = len(rows) + 1
        tot = {}
        for k in range(n + 1):
            line(ps, (xs[0], y_top - k * rh), (xs[-1], y_top - k * rh), "S-TTLB" if k in (0, 1, n) else "S-TTLB-THIN")
        for cx in xs:
            line(ps, (cx, y_top), (cx, y_top - n * rh), "S-TTLB-THIN")
        for cx, h_ in zip(xs, heads):
            text(ps, h_, (cx + 1.0, y_top - rh / 2), 2.0, align=TA.MIDDLE_LEFT, style="ANB")
        for r, (mk, db, shp, dims, nb, spc, cnt, rem) in enumerate(rows, start=1):
            yy = y_top - r * rh - rh / 2
            cut = round((sum(v for _, v in dims) - 2 * db * nb) / 1000, 2)
            tl = round(cut * cnt, 2)
            wt = round(tl * UW[db], 1)
            tot[db] = tot.get(db, 0) + wt
            cx, cy = xs[0] + 3.5, yy
            ps.add_circle((cx, cy), 2.0, dxfattribs=A("S-SYMB"))
            text(ps, mk, (cx, cy), 2.0 if len(mk) < 2 else 1.7, align=TA.MIDDLE_CENTER, style="ANB")
            text(ps, ("RB" if mk == "D" else "DB") + str(db), (xs[1] + 1.0, yy), 2.0, align=TA.MIDDLE_LEFT)
            shape_sketch(ps, shp, xs[2], y_top - r * rh, cols[3] - cols[2], rh)
            text(ps, "  ".join(f"{a}={r5(v)}" for a, v in dims), (xs[3] + 1.0, yy), 2.0, align=TA.MIDDLE_LEFT)
            for i, v in ((4, f"{cut:.2f}"), (5, spc), (6, str(cnt)), (7, f"{tl:.2f}"), (8, f"{wt:.1f}")):
                text(ps, v, (xs[i] + 1.0, yy), 2.0, align=TA.MIDDLE_LEFT)
            text(ps, rem, (xs[9] + 1.0, yy), 2.0, align=TA.MIDDLE_LEFT)
        return y_top - n * rh, tot

    y1, tot = table_rows(per_bay, FY1 - 9, "1  BAR SCHEDULE - PER TYPICAL 6.00 m BAY (BETWEEN JOINTS)", "bay")
    kg = sum(tot.values())
    text(ps, f"TOTAL PER BAY:  DB12 {tot.get(12, 0):.1f} kg  +  DB10 {tot.get(10, 0):.1f} kg  =  {kg:.1f} kg"
             f"  ({kg / (BAY / 1000):.1f} kg PER METRE OF WALL)", (x + cols[3], y1 - 3.5), 2.0, style="ANB")
    y2, _ = table_rows(extra, y1 - 13, "ADDITIONAL BARS - PER CORNER / PER FREE END / PER JOINT", "extra")
    # bar planes view + notes
    top3 = y2 - 6
    px, pw, ph = viewport(ps, "BP", 10, FX0, top3)
    view_title(ps, None, top3 - ph - 6, "BAR PLANES FROM A JOINT FACE - PLAN", "1:10", ("2", "5005"))
    n = notes([
        hdr("SCHEDULE NOTES"),
        "1. DIMENSIONS OUT-TO-OUT OF BAR. CUT LENGTH = SUM OF DIMENSIONS - 2 db PER 90° BEND.",
        "2. BAR COUNT PER BAY FROM THE PLANE ARRANGEMENT 2/5005, BARS 50 CLEAR OF BOTH JOINT FACES.",
        "3. SHAPE SKETCHES ARE SCHEMATIC; BENDS ON 6 db MANDREL.",
        "4. THIS SCHEDULE IS INDICATIVE. THE CONTRACTOR SHALL ISSUE A SHOP BAR SCHEDULE AND CONFIRM LENGTHS ON SITE BEFORE CUTTING.",
        "5. STOCK LENGTH 10 m; NO BAR EXCEEDS 6.0 m.",
        "",
        hdr("FIXING"),
        "SEE GENERAL NOTES 5.1-5.8 (1001). HOLD POINT: ENGINEER'S INSPECTION BEFORE EACH POUR.",
    ])
    mtext(ps, n, (FX0 + pw + 8, top3 - 1), 2.0, TBX - (FX0 + pw + 8) - 3, spacing=1.1)


for fn in (sheet_1001, sheet_3001, sheet_5001, sheet_5002, sheet_5003, sheet_5004, sheet_5005):
    fn()
if "Layout1" in doc.layouts:
    doc.layouts.delete("Layout1")

OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(DXF)
print("saved", DXF)
