"""
General notes - structural concrete, A3 drawing (office master, Rev A).

Content : GENERAL_NOTES_STRUCTURAL_CONCRETE.md (EIT 011014-19 materials & construction, ACI 318-19 / ACI 301 refs).
Engine  : copied from jobs/stair_demo/build_stair.py (frame, title strip, pens, text styles).
Rule    : every annotation = general drawing rule x K, K = 1.25/2.00 (text 1.25 / 1.75, pitch 2.08, dims 1.25);
          frame, title strip and pens unchanged. Text laid out line by line with measured widths (fontTools).
Guide   : GENERAL_NOTES_DRAWING_INSTRUCTION.md

usage: python build_gn.py <out_dir>      -> <out_dir>/STR-ST-1001_General_Notes_Concrete_A3_RevA.dxf
"""
import math
import sys
from pathlib import Path

import ezdxf
from ezdxf import bbox
from ezdxf.path import make_path
from ezdxf.enums import TextEntityAlignment as TA, MTextEntityAlignment as MA

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
DXF = OUT / "STR-ST-1001_General_Notes_Concrete_A3_RevA.dxf"

# --------------------------------------------------------------------------- project data
PROJ = dict(
    code="STR",
    owner="[ OWNER NAME ]",
    project="[ PROJECT NAME ]",
    location="[ BUILDING / LOCATION ]",
    office="[ DESIGN OFFICE NAME ]",
    office2="[ ADDRESS / TEL. / E-MAIL ]",
    date="29/09/2026",
    stage="D", rev="A",
)
SHEETS = [("1001", ["GENERAL NOTES", "STRUCTURAL CONCRETE"], "N.T.S.")]
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
    text(ps, "NOT APPLICABLE", (xc, (by0 + by1) / 2 + 2.5), 2.0, align=TA.MIDDLE_CENTER)
    text(ps, "(GENERAL NOTES)", (xc, (by0 + by1) / 2 - 2.5), 2.0, align=TA.MIDDLE_CENTER)

    # status stamp + sheet notes (text area, EIT 2.2.2.2)
    sy = y_kp1 + 3
    pline(ps, [(x0 + 3, sy), (x1 - 3, sy), (x1 - 3, sy + 12), (x0 + 3, sy + 12)], "S-TITLE", close=True)
    text(ps, "FOR REVIEW", (xc, sy + 8.2), 2.8, align=TA.MIDDLE_CENTER, style="ANB")
    text(ps, "NOT FOR CONSTRUCTION", (xc, sy + 3.8), 2.8, align=TA.MIDDLE_CENTER, style="ANB")
    text(ps, "NOTES", (tx, FY1 - 3.5), 2.0, align=TA.MIDDLE_LEFT, style="ANB")
    notes = ("1. APPLIES TO ALL STRUCTURAL DRAWINGS.\\P"
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


# ======================================================================= GENERAL NOTES - layout engine
# Every line of text is placed as its own TEXT entity at a measured position, so the plotted sheet
# matches the layout exactly (no MTEXT re-wrapping in AutoCAD).
# GENERAL-NOTES SHEET RULE: every annotation size = general drawing rule x K, K = 1.25 / 2.00.
# NOT scaled: sheet frame, zone grid, title strip (set-wide furniture) and pen weights (plot pens).
# See GENERAL_NOTES_DRAWING_INSTRUCTION.md section 2.
K = 1.25 / 2.00
TB = TXT_H * K               # 1.25  body text              (rule 2.0)
TH = 2.8 * K                 # 1.75  headers, bold          (rule 2.8)
LP = PITCH * K               # 2.08  body line pitch        (rule 3.33 = 5/3 x text)
TLP = LP                     # 2.08  extra line in a wrapped table cell
TRH = 5.2 * K                # 3.25  single-line table row  (rule 5.2)
HP = TH + 2.0 * K            # 3.00  header + gap below     (rule 2.0)
PG = NGAP * K                # 1.00  gap after a note       (rule 1.6)
SG = 3.0 * K                 # 1.88  gap before a header    (rule 3.0)
NCOL = 3
CGAP = 8.0 * K               # 5.00  column gap             (rule 8.0)
CX0, CX1 = FX0 + 3.5, TBX - 3.5
COLW = (CX1 - CX0 - (NCOL - 1) * CGAP) / NCOL
CY1 = FY1 - 3.5
IND = 8.0 * K                # 5.00  hanging indent for note numbers ("12.10")  (rule 8.0)
CPAD = 1.2 * K               # 0.75  text inset in a table cell (rule 1.2)

_gds = doc.dimstyles.get(DS[1]).dxf  # dimensions on this sheet: rule dimstyle x K
_gds.dimtxt, _gds.dimasz, _gds.dimexe = 2.0 * K, 2.0 * K, 2.0 * K        # 1.25 text / arrow / extension
_gds.dimexo, _gds.dimgap, _gds.dimdli = 1.0 * K, 0.6 * K, 5.0 * K        # 0.625 offset / 0.375 gap


def wrap_s(s, h, width, style="AN"):
    out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if cur and text_w(t, h, style) > width:
            out.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out or [""]


class Flow:
    """sequential column flow; draw=False only measures"""
    def __init__(self, ps, y_bottom, draw=True):
        """y_bottom: one bottom line for all columns, or a list with one per column"""
        self.ps, self.draw = ps, draw
        self.ybs = list(y_bottom) if isinstance(y_bottom, (list, tuple)) else [y_bottom] * NCOL
        self.col, self.y = 0, CY1

    @property
    def x(self):
        return CX0 + self.col * (COLW + CGAP)

    def need(self, h):
        if self.y - h < self.ybs[min(self.col, NCOL - 1)] and self.y < CY1 - 0.01:
            self.col += 1
            self.y = CY1

    def gap(self, g):
        if self.y < CY1 - 0.01:
            self.y -= g

    def header(self, s):
        self.gap(SG)
        self.need(HP + 3 * LP)
        if self.draw:
            text(self.ps, s, (self.x, self.y - TH), TH, "S-TEXT", style="ANB")
        self.y -= HP

    def para(self, num, body, level=0):
        x_num = self.x + level * IND
        lines = wrap_s(body, TB, COLW - (level + 1) * IND)
        self.need(min(2, len(lines)) * LP)                  # no single orphan line at a column foot
        for k, ln in enumerate(lines):
            self.need(LP)
            if self.draw:
                if k == 0 and num:
                    text(self.ps, num, (self.x + level * IND, self.y - TB), TB, "S-TEXT")
                text(self.ps, ln, (self.x + (level + 1) * IND, self.y - TB), TB, "S-TEXT")
            self.y -= LP
        self.y -= PG

    def table(self, title, widths, heads, rows, note=None, align=None):
        """widths in fractions of the column width; cells wrap; first row = heads (bold).
        align: one letter per column, "L" = middle-left, "C" = middle-centre (numbers, sizes, values).
        Every cell is centred vertically on its row (AutoCAD MIDDLE alignment = middle of the cap height);
        a wrapped cell is centred as a block."""
        ws = [f * COLW for f in widths]
        align = (align or "L" * len(ws)).upper()
        allrows = [heads] + rows
        cells = [[wrap_s(c, TB, w - 1.4, "ANB" if r == 0 else "AN") for c, w in zip(row, ws)]
                 for r, row in enumerate(allrows)]
        rhs = [TRH + (max(len(c) for c in row) - 1) * TLP for row in cells]
        nl = wrap_s(note, TB, COLW) if note else []
        tot = LP + 0.6 * K + sum(rhs) + len(nl) * LP + 1.6 * K + (PG if nl else 0.0)
        self.gap(PG)
        self.need(tot)
        if self.draw:
            ps, x0 = self.ps, self.x
            text(ps, title, (x0, self.y - TB), TB, "S-TEXT", style="ANB")
            yt = self.y - LP - 0.6 * K
            xs = [x0]
            for w in ws:
                xs.append(xs[-1] + w)
            y = yt
            for r, (row, rh) in enumerate(zip(cells, rhs)):
                line(ps, (xs[0], y), (xs[-1], y), "S-TTLB" if r <= 1 else "S-TTLB-THIN")
                ym = y - rh / 2                                     # row centre line
                for c, (cl, cx) in enumerate(zip(row, xs)):
                    centre = align[c] == "C"
                    tx = cx + ws[c] / 2 if centre else cx + CPAD
                    for k, ln in enumerate(cl):
                        ty = ym + ((len(cl) - 1) / 2 - k) * TLP
                        text(ps, ln, (tx, ty), TB, "S-TEXT", TA.MIDDLE_CENTER if centre else TA.MIDDLE_LEFT,
                             style="ANB" if r == 0 else "AN")
                y -= rh
            line(ps, (xs[0], y), (xs[-1], y), "S-TTLB")
            for cx in xs:
                line(ps, (cx, yt), (cx, y), "S-TTLB-THIN")
            for k, ln in enumerate(nl):
                text(ps, ln, (x0, y - 1.6 * K - TB - k * LP), TB, "S-TEXT")
        self.y -= tot

    def figure(self, h, fn):
        self.gap(PG)
        self.need(h)
        if self.draw:
            fn(self.ps, self.x, self.y)
        self.y -= h


# ======================================================================= GENERAL NOTES - data
# Design standard: EIT 011008-21 (based on ACI 318-11). Materials & construction: EIT 011014-19.
FC_LAP = 23.5                # MPa (240 ksc) - basis of the lap / anchorage table
FY_LAP = 390.0               # SD40


def rup(v, step=50):
    return int(math.ceil(v / step - 1e-9) * step)


def ld_simple(db, top=False):
    """EIT 011008 12.2.2 simplified ld (clear cover >= db and clear spacing >= 2 db, or cover >= db, spacing >= db
    with minimum stirrups): fy psi_t psi_e / (2.1 lambda sqrt f'c) db for bars <= 20 mm, 1.7 for >= 22 mm;
    uncoated (psi_e = 1), normalweight (lambda = 1), psi_t = 1.3 for top bars; ld >= 300"""
    k = 2.1 if db <= 20 else 1.7
    return max(300.0, FY_LAP * (1.3 if top else 1.0) / (k * math.sqrt(FC_LAP)) * db)


def lap_len(db, top=False):
    """class B tension lap = 1.3 ld >= 300 (EIT 011008 12.14.1), rounded up to 50"""
    return max(300, rup(1.3 * ld_simple(db, top)))


def lap_comp(db):
    """compression lap 0.071 fy db >= 300 (fy <= 420 MPa) (EIT 011008 12.15.1), rounded up to 50"""
    return max(300, rup(0.071 * FY_LAP * db))


def ldh(db):
    """standard-hook development fy / (4.2 lambda sqrt f'c) db >= 8 db >= 150 (EIT 011008 12.5.2), up to 50"""
    return rup(max(FY_LAP / (4.2 * math.sqrt(FC_LAP)) * db, 8 * db, 150))


def cov(c0, alpha):
    a = 1.0 if c0 <= 20 else alpha
    return int(math.ceil(a * c0 / 5.0 - 1e-9) * 5)


LAP_DB = [10, 12, 16, 20, 25, 28, 32]
# cover by structural element - EIT 011008-21 7.7.1 (cast in place): (element, condition, <= DB16, >= DB20)
COVER_ELEM = [
    ("FOOTINGS, PILE CAPS", "CAST AGAINST EARTH (BOTTOM, SIDES)", "75", "75"),
    ("FOOTINGS, PILE CAPS", "FORMED FACES IN CONTACT WITH EARTH", "40", "50"),
    ("GROUND BEAMS, SUSPENDED GROUND SLABS", "IN CONTACT WITH EARTH", "40", "50"),
    ("COLUMNS, BEAMS", "INTERIOR (TO TIES / STIRRUPS)", "40", "40"),
    ("COLUMNS, BEAMS", "EXPOSED TO WEATHER", "40", "50"),
    ("SLABS, JOISTS, STAIRS", "INTERIOR", "20", "30"),
    ("SLABS, ROOF DECKS, CANOPIES", "EXPOSED TO WEATHER", "40", "50"),
    ("WALLS", "INTERIOR", "20", "30"),
    ("RETAINING, BASEMENT WALLS, TANKS", "EARTH OR WEATHER FACE", "40", "50"),
    ("SHELLS, FOLDED PLATES", "INTERIOR", "15", "20"),
]
# recommendation - exposure based, EIT 011014-19 2.5.1.5 (T2.23 corrosion risk) with alpha by f'c
COVER_ENV = [("CORROSION RISK: SLABS, WALLS", 50), ("CORROSION RISK: OTHER MEMBERS", 65)]


def content(f):
    H, P, T = f.header, f.para, f.table
    E8, E14 = "EIT 011008", "EIT 011014"          # citation prefixes: design / materials & construction

    H("1. GENERAL")
    P("1.1", "THESE NOTES APPLY TO ALL STRUCTURAL CONCRETE WORK UNLESS NOTED OTHERWISE (U.N.O.) ON THE DRAWINGS. "
             "READ WITH THE ARCHITECTURAL AND MEP DRAWINGS AND THE SPECIFICATION. WHERE DOCUMENTS DIFFER, THE MORE "
             "STRINGENT REQUIREMENT GOVERNS; REFER ANY DISCREPANCY TO THE ENGINEER BEFORE PROCEEDING.")
    P("1.2", "DIMENSIONS ARE IN MILLIMETRES AND LEVELS IN METRES U.N.O. DO NOT SCALE FROM THE DRAWINGS.")
    P("1.3", f"THE WORK SHALL BE INSPECTED THROUGHOUT BY A LICENSED CIVIL ENGINEER (SUPERVISING ENGINEER) STATIONED "
             f"ON SITE; DUCTILE MOMENT FRAMES DESIGNED FOR EARTHQUAKE REQUIRE CONTINUOUS INSPECTION OF REINFORCEMENT "
             f"AND CONCRETING. [{E8} 1.3.1, 1.3.5; {E14} 1.2.3]")
    P("1.4", f"BEFORE WORK STARTS THE CONTRACTOR SHALL SUBMIT FOR APPROVAL: CONSTRUCTION PLAN AND POUR SEQUENCE; "
             f"CONCRETE MIX DESIGNS WITH TRIAL-MIX RESULTS; MATERIAL CERTIFICATES; FORMWORK AND SHORING DESIGN; BAR "
             f"BENDING SCHEDULES. [{E14} 1.2.4, 3.1, 10.3]")
    P("1.5", f"NO OPENING, SLEEVE, CHASE OR EMBEDDED ITEM NOT SHOWN ON THE STRUCTURAL DRAWINGS SHALL BE MADE WITHOUT "
             f"THE ENGINEER'S APPROVAL. [{E8} 6.3.1]")

    H("2. DESIGN BASIS AND STANDARDS")
    P("2.1", f"DESIGN: EIT 011008-21, RC BUILDINGS BY STRENGTH DESIGN (BASED ON ACI 318-11). SEISMIC: DPT 1301/1302-61 "
             f"WHERE REQUIRED BY MINISTERIAL REGULATION. LOADS: MINISTERIAL REGULATIONS UNDER THE BUILDING CONTROL ACT "
             f"B.E. 2522; LIVE LOADS AS SHOWN ON THE DESIGN CRITERIA / FRAMING PLANS. [{E8} 1.1, 1.2.1, 19.1]")
    P("2.2", "MATERIALS AND CONSTRUCTION: EIT 011014-19. DRAFTING: EIT 011006-19. WHERE THESE ARE SILENT: ACI 301 AND "
             "ACI 318.")
    P("2.3", "TIS (CURRENT EDITIONS): 15, 849, 2587, 2594 CEMENTS; 566 AGGREGATES; 733, 874, 985 ADMIXTURES; 2135 "
             "FLY ASH; 213 READY-MIXED CONCRETE; 409 COMPRESSION TEST; 20 ROUND BARS; 24 DEFORMED BARS; 737 WELDED WIRE "
             "FABRIC; 1227 STRUCTURAL STEEL. DPT: 1208 / 1210 CYLINDERS; 1212 MIXING WATER; 1332 DURABILITY.")
    P("2.4", "ACI GUIDES FOR WORKMANSHIP: ACI 117 TOLERANCES; ACI 304 PLACING; ACI 305 HOT WEATHER; ACI 308 "
             "CURING; ACI 309 CONSOLIDATION; ACI 347 FORMWORK.")

    H("3. CONCRETE")
    T("CONCRETE SCHEDULE (U.N.O. ON DRAWINGS)", [0.37, 0.24, 0.12, 0.14, 0.13],
      ["ELEMENT", "f'c CYL. 28 d", "MAX. w/b", "SLUMP cm", "MAX. AGG."],
      [["LEAN CONCRETE 50 THK.", "150 ksc (15 MPa)", "–", "5 – 10", "20"],
       ["FOOTINGS, PILE CAPS, GROUND BEAMS", "240 ksc (23.5 MPa)", "0.50", "5 – 7.5", "25"],
       ["COLUMNS, WALLS", "240 ksc (23.5 MPa)", "0.50", "5 – 12.5", "20"],
       ["BEAMS, SLABS, STAIRS", "240 ksc (23.5 MPa)", "0.50", "5 – 10", "20"],
       ["WATER-RETAINING, ROOF SLABS", "280 ksc (27.5 MPa)", "0.50", "7.5 – 10", "20"],
       ["SEVERE EXPOSURE (CHLORIDE, SEWAGE)", "320 ksc (31.5 MPa)", "0.45", "7.5 – 10", "20"],
       ["CONGESTED REINFORCEMENT", "AS ABOVE", "AS ABOVE", "10 – 15", "20"]],
      note=f"STRUCTURAL CONCRETE f'c ≥ 18 MPa. SLUMP TOLERANCE ±2.5 cm (±3.5 cm ABOVE 15 cm). "
           f"[{E8} 1.1.1; {E14} T1.1, T3.5, T3.6, T5.1]", align="LCCCC")
    P("3.1", f"f'c IS THE SPECIFIED STRENGTH OF STANDARD CYLINDERS Ø150 x 300 AT 28 DAYS, U.N.O. (CUBE ≈ CYLINDER + "
             f"5 MPa FOR 20 – 50 MPa). [{E8} 5.1.3, 5.1.4; {E14} FIG. 3.2]")
    P("3.2", f"CEMENT: PORTLAND CEMENT TYPE I TO TIS 15 U.N.O.; TIS 849, 2587, 2594 ONLY WITH APPROVAL. MIXED CEMENT "
             f"(TIS 80) SHALL NOT BE USED FOR STRUCTURAL CONCRETE. [{E8} 3.2; {E14} 2.1]")
    P("3.3", f"AGGREGATES TO TIS 566: CLEAN, HARD AND DURABLE. SEA SAND ONLY WITH APPROVAL (Cl ≤ 0.02 % OF DRY SAND). "
             f"MAX. SIZE ≤ 1/5 OF THE NARROWEST FORM DIMENSION, 1/3 OF THE SLAB THICKNESS AND 2/3 OF THE CLEAR BAR "
             f"SPACING. [{E8} 3.3; {E14} 2.3]")
    P("3.4", f"WATER: CLEAN, TO DPT 1212. SEA OR BRACKISH WATER SHALL NOT BE USED. [{E8} 3.4; {E14} 2.2]")
    P("3.5", f"ADMIXTURES (TIS 733, 874, 985) AND FLY ASH (TIS 2135) ONLY WITH APPROVAL AND BY TRIAL MIX. CALCIUM "
             f"CHLORIDE OR CHLORIDE ADMIXTURES ARE PROHIBITED IN PRESTRESSED CONCRETE, WITH EMBEDDED ALUMINIUM OR "
             f"AGAINST GALVANIZED FORMS; Cl FROM ADMIXTURES ≤ 0.02 % OF BINDER. [{E8} 3.6; {E14} 2.4]")
    P("3.6", f"MAX. ACID-SOLUBLE CHLORIDE (ASTM C1152), % OF CEMENTITIOUS MATERIAL: RC 0.30; RC EXPOSED TO CHLORIDE "
             f"0.20; RC DRY OR PROTECTED 1.00; PRESTRESSED 0.08. [{E8} T5.6; {E14} T1.2]")
    T("SULFATE EXPOSURE", [0.19, 0.17, 0.17, 0.33, 0.14],
      ["SEVERITY", "SO4 WATER ppm", "SO4 SOIL %", "CEMENT", "MAX. w/cm"],
      [["NORMAL", "< 150", "< 0.1", "NO RESTRICTION", "–"],
       ["MODERATE", "150 – 1,500", "0.1 – 0.2", "TYPE 2 OR 5, OR 1 + POZZOLAN", "0.50"],
       ["SEVERE", "1,500 – 10,000", "0.2 – 2.0", "TYPE 5, OR 1 + POZZOLAN", "0.45"],
       ["VERY SEVERE", "> 10,000", "> 2.0", "TYPE 5 OR 1, WITH POZZOLAN", "0.40"]],
      note=f"MAGNESIUM SULFATE: TYPE 5, NO POZZOLAN REPLACEMENT, PER {E8} T5.5. [{E8} 5.5.1, T5.4]",
      align="LCCLC")
    P("3.7", f"MIX DESIGN BY THE SUPPLIER FOR f'cr ≥ THE LARGER OF f'c + 1.34 ss AND f'c + 2.33 ss − 3.5 MPa (ss FROM "
             f"≥ 30 TESTS, OR 15 – 29 x FACTOR); WITHOUT DATA f'cr = f'c + 7.0 (f'c < 21), f'c + 8.3 (21 – 35), "
             f"1.1 f'c + 5.0 (> 35) MPa. [{E8} 5.3, T5.1, T5.2]")
    P("3.8", f"READY-MIXED CONCRETE TO TIS 213 FROM AN APPROVED PLANT; SITE MIXING IN AN APPROVED MIXER ≥ 1.5 min "
             f"AFTER ALL MATERIALS ARE IN. DELIVERY TICKETS SHALL SHOW PLANT, TICKET AND TRUCK NO., CLASS, VOLUME, "
             f"BATCHING AND DISCHARGE TIMES, SLUMP, MAX. AGGREGATE AND ADMIXTURES. [{E8} 5.8.2; {E14} 5.1, 5.6.5]")
    P("3.9", f"DISCHARGE WITHIN 2 h OF BATCHING (1 h WITHOUT A RETARDER). NO WATER SHALL BE ADDED ON SITE; SLUMP MAY "
             f"BE RESTORED ONLY WITH SUPERPLASTICIZER AND ≥ 30 DRUM REVOLUTIONS. CONCRETE THAT HAS BEGUN TO SET OR IS "
             f"RETEMPERED SHALL NOT BE USED. [{E8} 5.8.4; {E14} 5.3, 5.6.3]")

    H("4. TESTING AND ACCEPTANCE")
    P("4.1", f"SAMPLE AT THE POINT OF PLACING (ASTM C172), PER CLASS: ≥ ONCE PER DAY, PER 50 m³ AND PER 250 m² OF "
             f"SLAB OR WALL; ≥ 5 RANDOM BATCHES WHERE FEWER TESTS RESULT. 1 SET = 3 CYLINDERS (DPT 1208), TESTED TO "
             f"TIS 409 / DPT 1210 AT 28 DAYS; ADD 7-DAY AND FIELD-CURED SETS FOR EARLY STRIPPING OR LOADING. SLUMP "
             f"TEST EVERY SAMPLED TRUCK. [{E8} 5.7.1; {E14} 5.6.4, 12.3]")
    P("4.2", "ACCEPTANCE - ALL OF:")
    P("(a)", f"MEAN OF ANY 3 CONSECUTIVE TESTS ≥ f'c, AND NO TEST BELOW f'c − 3.5 MPa. [{E8} 5.7.2]", 1)
    P("(b)", f"EACH SET MEAN ≥ f'c AND EVERY CYLINDER ≥ 0.85 f'c. [{E14} 5.6.4]", 1)
    P("(c)", f"WITH ≥ 30 RESULTS: MEAN ≥ f'c + 1.65 Sn. [{E14} 12.4]", 1)
    P("4.3", f"FIELD-CURED CYLINDERS BELOW 85 % OF THE COMPANION LAB-CURED STRENGTH (AND NOT ABOVE f'c + 3.5 MPa): "
             f"IMPROVE CURING AND PROTECTION. [{E8} 5.7.3]")
    P("4.4", f"LOW STRENGTH: 3 CORES PER DEFICIENT TEST (DPT 1210); ADEQUATE IF THE CORE MEAN ≥ 0.85 f'c AND NO CORE "
             f"< 0.75 f'c. OTHERWISE LOAD TEST AT ≥ 56 DAYS WITH 0.85 (1.4D + 1.7L) FOR 24 h: ACCEPT IF DEFLECTION ≤ "
             f"lt² / (20,000 h) OR RECOVERY ≥ 75 % IN 24 h. STRENGTHENING OR REMOVAL AT THE CONTRACTOR'S COST. "
             f"[{E8} 5.7.4, 18.3.2, 18.4]")
    P("4.5", f"REPORT RESULTS TO THE ENGINEER IMMEDIATELY; KEEP CONTROL CHARTS. [{E14} 12.2.4, 12.3]")

    H("5. REINFORCEMENT")
    P("5.1", f"DEFORMED BARS (DB) SD40 TO TIS 24, fy ≥ 390 MPa (4,000 ksc). ROUND BARS (RB) SR24 TO TIS 20, fy ≥ 235 "
             f"MPa (2,400 ksc), FOR STIRRUPS, TIES AND SPIRALS ONLY. WELDED WIRE FABRIC TO TIS 737. MILL CERTIFICATE "
             f"AND TENSILE TEST PER DELIVERY AND SIZE. [{E8} 3.5; {E14} 2.5.1.1, 12.2.3]")
    P("5.2", f"STORE UNDER COVER, OFF THE GROUND, BY SIZE AND GRADE. AT CONCRETING BARS SHALL BE FREE OF MUD, OIL AND "
             f"LOOSE RUST; LIGHT RUST OR MILL SCALE IS ACCEPTABLE. [{E8} 7.4; {E14} 2.6.5]")
    P("5.3", f"BEND COLD, BY MACHINE, TO THE APPROVED SCHEDULE. NO HEATING, RE-BENDING OR FIELD BENDING OF BARS "
             f"PARTLY EMBEDDED IN CONCRETE, U.N.O. NO BEND WITHIN 10 db OF A WELD. [{E8} 7.3; {E14} 2.5.1.2]")
    T("HOOKS AND BENDS", [0.36, 0.42, 0.22],
      ["BAR", "STANDARD HOOK", "MIN. INSIDE BEND Ø"],
      [["MAIN BARS DB10 – DB25", "90° + 12 db  /  180° + 4 db ≥ 65", "6 db"],
       ["MAIN BARS DB28 – DB36", "90° + 12 db", "8 db"],
       ["STIRRUPS, TIES RB6 – DB16", "135° + 6 db  (90° + 6 db)", "4 db"],
       ["STIRRUPS, TIES DB20 – DB25", "135° + 6 db  (90° + 12 db)", "6 db"]],
      note=f"90° STIRRUP HOOKS ONLY WHERE DETAILED; SEISMIC FRAMES: 135° + 6 db ≥ 75 (MIN. REG. NO. 49, DPT 1302). "
           f"[{E8} 7.1, 7.2, T7.1; {E14} 2.5.1.2]", align="LCC")
    P("5.4", f"CLEAR SPACING ≥ db AND ≥ 25 mm; LAYERS ALIGNED, ≥ 25 mm APART; COLUMN BARS ≥ 1.5 db AND ≥ 40 mm; MAIN "
             f"BARS IN SLABS AND WALLS ≤ 3 h AND ≤ 450 mm. BUNDLES: ≤ 4 DB, NONE > DB36 IN BEAMS, CUTOFFS STAGGERED "
             f"40 db. [{E8} 7.6]")
    P("5.5", f"FIX BARS RIGIDLY WITH ≥ 0.9 mm (USE 1.25 mm) ANNEALED WIRE; ERECTION BARS AND CHAIRS AS NEEDED. NO "
             f"TACK WELDING WITHOUT APPROVAL. [{E8} 7.5.1, 7.5.4; {E14} 2.5.1.3]")
    P("5.6", f"SPACERS: PRECAST CONCRETE OR MORTAR OF STRENGTH ≥ THE CONCRETE, AT ≤ 1.0 m EACH WAY. PLASTIC OR "
             f"STAINLESS ONLY WITH APPROVAL; NO TIMBER, BRICK OR STONE. [{E14} 2.5.1.3]")
    P("5.7", f"PLACING TOLERANCE: d ±10 mm (d ≤ 200) / ±13 mm; COVER −10 / −13 mm AND ≤ 1/3 OF THE SPECIFIED COVER; "
             f"BENDS AND BAR ENDS ±50 mm (±25 mm AT DISCONTINUOUS ENDS, ±13 mm AT CORBELS). [{E8} 7.5.2; {E14} T2.20]")
    T("COLUMN TIES", [0.50, 0.50],
      ["LONGITUDINAL BAR", "MIN. TIE"],
      [["≤ DB12", "RB6"],
       ["DB16 – DB20", "RB9"],
       ["DB25 – DB28", "DB10"],
       ["≥ DB32, BUNDLES", "DB12"]],
      note=f"TIE SPACING ≤ LEAST OF 16 db (MAIN BAR), 48 db (TIE) AND THE LEAST COLUMN DIMENSION. EVERY CORNER AND ALTERNATE BAR IN A TIE CORNER ≤ 135°, NO BAR > 150 CLEAR FROM A SUPPORTED BAR; FIRST TIE "
           f"≤ s/2 FROM SLAB. SPIRALS ≥ 9 mm, CLEAR PITCH 25 – 75, 1.5 EXTRA TURNS, LAP 48 db (DEFORMED) / 72 db "
           f"(PLAIN) ≥ 300. ANCHOR BOLTS: ≥ 2-DB12 OR 3-DB10 TIES WITHIN 125 OF THE TOP. [{E8} 7.10.4, 7.10.5]",
      align="CC")
    P("5.8", f"BEAMS: COMPRESSION BARS ENCLOSED BY TIES AS FOR COLUMNS; CLOSED STIRRUPS WHERE TORSION OR STRESS "
             f"REVERSAL, WITH 135° HOOKS ROUND A BAR OR CLASS B LAPS. [{E8} 7.11]")
    P("5.9", f"SHRINKAGE AND TEMPERATURE BARS: As/Ag ≥ 0.0025 (SR24), 0.0020 (SD30), 0.0018 (SD40) AND ≥ 0.0014, "
             f"AT ≤ 5 h AND ≤ 400 mm. [{E8} 7.12]")
    P("5.10", f"INTEGRITY: PERIMETER BEAMS CONTINUOUS WITH ≥ 1/6 OF TOP SUPPORT BARS AND ≥ 1/4 OF BOTTOM MIDSPAN BARS "
              f"(≥ 2 BARS EACH), IN CLOSED STIRRUPS WITH 135° HOOKS; SPLICE TOP BARS AT MIDSPAN, BOTTOM BARS NEAR "
              f"SUPPORTS, CLASS B. [{E8} 7.13]")
    P("5.11", f"PROTECT STARTER BARS AND FUTURE-EXTENSION ITEMS FROM CORROSION; REMOVE COATINGS BEFORE CONCRETING. "
              f"[{E8} 7.7.6; {E14} 2.5.1.4]")

    H("6. DEVELOPMENT AND SPLICES")
    P("6.1", f"LAP ONLY WHERE SHOWN OR APPROVED. TENSION LAPS CLASS B (CLASS A ONLY WHERE As ≥ 2 x REQUIRED AND "
             f"≤ 50 % IS SPLICED); STAGGER ADJACENT LAPS ≥ 1.0 m; NO LAPS FOR BARS LARGER THAN DB36 OR IN "
             f"BEAM-COLUMN JOINTS. [{E8} 12.13, 12.14; {E14} 2.5.1.4]")
    T(f"LAP AND ANCHORAGE LENGTH (mm) - f'c 240 ksc, SD40",
      [0.23] + [0.77 / len(LAP_DB)] * len(LAP_DB),
      ["BAR"] + [f"DB{d}" for d in LAP_DB],
      [["TENSION LAP"] + [str(lap_len(d)) for d in LAP_DB],
       ["TENSION LAP, TOP *"] + [str(lap_len(d, True)) for d in LAP_DB],
       ["COMPRESSION LAP"] + [str(lap_comp(d)) for d in LAP_DB],
       ["STANDARD HOOK ldh"] + [str(ldh(d)) for d in LAP_DB]],
      note=f"CLASS B = 1.3 ld, ld PER {E8} 12.2.2 (CLEAR COVER ≥ db, CLEAR SPACING ≥ 2 db, UNCOATED, NORMALWEIGHT). "
           f"* HORIZONTAL BARS WITH > 300 mm OF FRESH CONCRETE BELOW. COMPRESSION LAP 0.071 fy db ≥ 300 (+ 1/3 IF "
           f"f'c < 21 MPa). ldh ≥ 8 db ≥ 150 (x 0.7 WITH SIDE COVER ≥ 65; x 0.8 WITHIN TIES AT ≤ 3 db). "
           f"[{E8} 12.2, 12.5, 12.14, 12.15]", align="L" + "C" * len(LAP_DB))
    P("6.2", f"U.N.O.: ≥ 1/3 (SIMPLE) OR 1/4 (CONTINUOUS) OF BOTTOM BARS EXTEND ≥ 150 INTO THE SUPPORT; ≥ 1/3 OF TOP "
             f"BARS EXTEND BEYOND THE POINT OF INFLECTION ≥ d, 12 db AND ln/16. [{E8} 12.10, 12.11]")
    P("6.3", f"WELDED SPLICES AND MECHANICAL COUPLERS SHALL DEVELOP ≥ 1.25 fy, TESTED BY AN APPROVED LABORATORY BEFORE "
             f"USE (3 COPIES OF RESULTS); WELD TYPE AND LOCATION AS SHOWN. [{E8} 3.5.2, 12.13.3; {E14} 2.5.1.4]")
    P("6.4", f"EVERY SPLICE SHALL BE INSPECTED AND APPROVED BY THE ENGINEER BEFORE CONCRETING. [{E14} 2.5.1.4]")

    H("7. CONCRETE COVER")
    T("MINIMUM CLEAR COVER BY STRUCTURAL ELEMENT (mm)", [0.36, 0.38, 0.13, 0.13],
      ["ELEMENT", "CONDITION", "≤ DB16", "≥ DB20"],
      [list(r) for r in COVER_ELEM],
      note=f"CAST IN PLACE; COVER FROM THE CONCRETE SURFACE TO THE OUTERMOST BAR (STIRRUP, TIE OR SPIRAL); "
           f"BAR SIZE = SIZE OF THAT BAR. BUNDLES: EQUIVALENT DIAMETER ≤ 50 (75 AGAINST EARTH). EMBEDDED PIPES: 35 "
           f"EXPOSED / 20 INTERIOR. PRECAST: PER {E8} 7.7.2. [{E8} 7.7.1, 7.7.3, 6.3.10]", align="LLCC")
    P("7.1", "RECOMMENDATION - ENVIRONMENT (WHERE THE PROJECT REQUIRES IT):")
    T("RECOMMENDED COVER, AGGRESSIVE EXPOSURE (mm)", [0.55, 0.15, 0.15, 0.15],
      ["MEMBER", "f'c < 20", "21 – 40", "> 40"],
      [[m, str(cov(c0, 1.2)), str(cov(c0, 1.0)), str(cov(c0, 0.9))] for m, c0 in COVER_ENV],
      note=f"COASTAL, CHLORIDE, SEWAGE, SULFATE OR CHEMICAL EXPOSURE: INCREASE COVER TO c = α · c0 (ROUNDED UP TO 5; "
           f"α 1.2 / 1.0 / 0.9 BY f'c) AND USE DENSER CONCRETE (w/b ≤ 0.45). FIRE: WHERE REGULATIONS NEED MORE COVER "
           f"THE LARGER GOVERNS (COLUMNS, BEAMS ≥ 300: 40; SLABS ≥ 115: 20). "
           f"[{E8} 7.7.4, 7.7.5; {E14} 2.5.1.5, T2.21, T2.23, T2.24; DPT 1332]", align="LCCC")

    H("8. FORMWORK, SHORING AND EMBEDDED ITEMS")
    P("8.1", f"DESIGNED, ERECTED AND REMOVED BY THE CONTRACTOR (ACI 347), FOR PLACING RATE, CONSTRUCTION AND IMPACT "
             f"LOADS, FRESH-CONCRETE PRESSURE, DEFLECTION, BRACING AND SHORE SPLICES; SUBMIT WHERE REQUIRED. LOADS: "
             f"CONCRETE 2,400 + STEEL 150 kg/m³; CONSTRUCTION 60 – 250 kg/m²; LATERAL ≥ 150 kg/m OR 2 % DL. "
             f"[{E8} 6.1; {E14} 10.1 – 10.3]")
    P("8.2", f"FORMS MORTAR-TIGHT; VISIBLE DEFLECTION ≤ SPAN/240; 20 x 20 CHAMFER ON EXPOSED CORNERS; CLEAN-OUTS AT "
             f"COLUMN AND WALL BASES; RELEASE AGENT KEPT OFF BARS AND JOINTS. [{E14} 10.3.1, 10.4]")
    P("8.3", f"SHORES BRACED, ON A FIRM BASE, WEDGE OR JACK ADJUSTED; SPLICED ≤ EVERY 2ND SHORE UNDER SLABS, 3RD UNDER "
             f"BEAMS. NO CONSTRUCTION LOAD ON ANY PART UNTIL IT CAN CARRY IT. [{E8} 6.2.1, 6.2.2; {E14} 10.3.2]")
    T("FORM REMOVAL (GENERAL STRUCTURES)", [0.52, 0.26, 0.22],
      ["FORMWORK", "FIELD-CURED f'c", "OR AGE"],
      [["SIDES OF COLUMNS, BEAMS, WALLS, FOOTINGS", "≥ 5 MPa", "2 DAYS"],
       ["SOFFITS OF SLABS AND BEAMS, INCL. SHORES", "≥ 14 MPa", "14 DAYS"]],
      note=f"CANTILEVERS, TRANSFER MEMBERS AND LONG SPANS ONLY ON THE ENGINEER'S INSTRUCTION. RESHORE ONLY TO AN "
           f"APPROVED PLAN, IMMEDIATELY AFTER STRIPPING. [{E8} 6.2; {E14} T10.1, T10.2, 10.6]", align="LCC")
    P("8.4", f"EMBEDDED PIPES AND CONDUITS ONLY WITH APPROVAL; NO ALUMINIUM. OUTSIDE Ø ≤ 1/3 OF THE MEMBER THICKNESS, "
             f"≥ 3 Ø C/C, IN SLABS BETWEEN THE TOP AND BOTTOM BARS; IN COLUMNS ≤ 4 % OF THE AREA. PROVIDE 0.002 Ac "
             f"NORMAL TO PIPING; DO NOT CUT OR DISPLACE BARS. [{E8} 6.3]")
    T("CONSTRUCTION TOLERANCES (mm)", [0.58, 0.42],
      ["ITEM", "TOLERANCE"],
      [["PLUMB: COLUMNS, WALLS", "6 PER 3 m; 25 MAX."],
       ["PLUMB: EXPOSED CORNERS, CONSPICUOUS LINES", "6 PER 3 m; 12 MAX."],
       ["LEVEL: SLAB AND BEAM SOFFITS (BEFORE STRIPPING)", "6 PER 3 m; 10 PER BAY; 20 MAX."],
       ["BUILDING LINES; COLUMN AND WALL POSITION", "12 PER BAY; 25 MAX."],
       ["OPENINGS: SIZE AND POSITION", "± 6"],
       ["SECTIONS; SLAB AND WALL THICKNESS", "− 5 / + 10"],
       ["FOOTINGS: PLAN / ECCENTRICITY", "− 12 / + 50;  ≤ 2 % ≤ 50"],
       ["FOOTINGS: THICKNESS", "− 5 % / + 100"],
       ["STAIRS: RISER / TREAD IN FLIGHT (ADJACENT)", "4 / 6  (2 / 4)"]],
      note=f"[{E14} 10.7; ACI 117]", align="LC")

    H("9. PLACING AND COMPACTION")
    P("9.1", f"HOLD POINT: THE ENGINEER SHALL APPROVE FORMWORK, REINFORCEMENT, SPLICES, COVER AND EMBEDDED ITEMS "
             f"IN WRITING BEFORE EACH POUR. [{E14} 7.1.1, 2.5.1.4]")
    P("9.2", f"CLEAN EQUIPMENT AND FORMS; REMOVE STANDING WATER; PRE-WET WITHOUT PONDING; REMOVE LAITANCE FROM "
             f"HARDENED CONCRETE. [{E8} 5.8.1; {E14} 7.1.1]")
    P("9.3", f"DEPOSIT NEAR THE FINAL POSITION, CONTINUOUSLY TO A PANEL END OR A PLANNED JOINT, WITHOUT SEGREGATION. "
             f"FREE FALL ≤ 1.5 m; COLUMNS AND WALLS ≤ 2 – 3 m/h RISE; EACH LAYER BEFORE THE LOWER ONE SETS. DO NOT MOVE "
             f"CONCRETE WITH VIBRATORS. [{E8} 5.8.3, 5.8.4; {E14} 7.1.2]")
    P("9.4", f"INTERNAL VIBRATORS AT 450 – 750 mm CENTRES FOR 5 – 15 s, 100 mm INTO THE LAYER BELOW; KEEP A STANDBY "
             f"VIBRATOR. [{E14} 7.2; ACI 309]")
    P("9.5", f"BEAMS AND SLABS SHALL NOT BE CAST UNTIL THE SUPPORTING COLUMNS AND WALLS HAVE HARDENED (PAUSE 1 – 2 h "
             f"MIN.). [{E8} 6.4.6; {E14} 7.2.4]")
    P("9.6", f"HOT WEATHER: CONCRETE ≤ 35 °C AT PLACING; PROTECT FROM SUN AND WIND; ABOVE 35 °C RECORD TEMPERATURES "
             f"AND MEASURES TAKEN. [{E8} 1.3.3, 5.8.6; ACI 305]")

    H("10. CURING")
    P("10.1", f"CURE IMMEDIATELY: KEEP MOIST AND ABOVE 10 °C ≥ 7 DAYS (TYPE I), ≥ 3 DAYS (HIGH EARLY STRENGTH); "
              f"LONGER WITH FLY ASH OR SLAG (UP TO 21 DAYS). PROTECT FROM DRYING, RAIN, VIBRATION AND OVERLOAD. "
              f"[{E8} 5.8.5; {E14} 8.2, 8.6]")
    P("10.2", f"CURING COMPOUND ONLY WITH APPROVAL, ≥ 2 COATS, KEPT OFF BARS AND JOINTS. [{E14} 8.5]")

    H("11. JOINTS")
    P("11.1", f"CONSTRUCTION JOINTS ONLY WHERE SHOWN OR APPROVED: SLABS AND BEAMS IN THE MIDDLE THIRD OF THE SPAN; "
              f"GIRDERS ≥ 2 x THE SECONDARY-BEAM WIDTH FROM ITS INTERSECTION; COLUMNS AND WALLS AT THE TOP OF THE "
              f"FOOTING OR SLAB AND BELOW THE FLOOR SOFFIT. DROP PANELS, CAPITALS AND HAUNCHES ARE CAST WITH THE "
              f"FLOOR. [{E8} 6.4.3 – 6.4.7; {E14} 9.1]")
    P("11.2", f"REMOVE LAITANCE TO EXPOSE THE AGGREGATE (≈ 5 mm AMPLITUDE); CLEAN, WET, REMOVE STANDING WATER; GROUT "
              f"WITH w/c LOWER THAN THE CONCRETE. [{E8} 6.4.1, 6.4.2; {E14} 9.1.1, 9.1.2]")
    P("11.3", f"WHERE COLUMN f'c > 1.4 x FLOOR f'c, PLACE COLUMN CONCRETE IN THE FLOOR OVER 4 x THE COLUMN AREA, "
              f"MONOLITHIC WITH THE FLOOR. [{E14} 9.1.3]")
    P("11.4", f"EXPANSION AND CONTRACTION JOINTS AS DETAILED, WITH FILLER, SEALANT AND WATER STOP WHERE SHOWN. "
              f"[{E8} 1.2.1; {E14} 9.2, 9.3]")

    H("12. FINISHING AND REPAIR")
    P("12.1", f"DO NOT TROWEL WITH BLEED WATER PRESENT OR IN RAIN. ROOF SLABS SHALL NOT BE STEEL-TROWELLED SMOOTH "
              f"U.N.O. [{E14} 11.2]")
    P("12.2", f"HONEYCOMB AND DEFECTS ARE REPAIRED ONLY BY AN APPROVED METHOD: CUT BACK TO SOUND CONCRETE, WET, "
              f"REPAIR WITH APPROVED MORTAR OR CONCRETE. STRUCTURAL DEFECTS PER THE ENGINEER. [{E14} 11.3]")

    H("13. INSPECTION AND RECORDS")
    P("13.1", f"KEEP RECORDS OF MATERIALS, MIXES, DELIVERY TICKETS, POURS (DATE, TIME, LOCATION, VOLUME, WEATHER), "
              f"TESTS, CURING, FORMWORK AND SHORING, REINFORCEMENT APPROVALS, CONSTRUCTION LOADS, DEVIATIONS AND "
              f"PHOTOGRAPHS; RETAIN ≥ 2 YEARS AFTER COMPLETION. [{E8} 1.3.2 – 1.3.4, 3.1.2; {E14} 13.1]")
    P("13.2", f"INSPECT COMPLETED MEMBERS; REPAIR DEFECTS AS INSTRUCTED BEFORE THE STRUCTURE IS USED. [{E14} 12.5.1]")

    H("ABBREVIATIONS")
    P("", "DB DEFORMED BAR · RB ROUND BAR · db BAR DIAMETER · f'c SPECIFIED CYLINDER STRENGTH · f'cr REQUIRED MEAN "
          "STRENGTH · fy YIELD STRENGTH · ld, ldh DEVELOPMENT LENGTH (STRAIGHT, HOOK) · w/b, w/cm WATER-BINDER RATIO · "
          "ss, Sn STANDARD DEVIATION · U.N.O. UNLESS NOTED OTHERWISE · EIT 011008 = EIT STANDARD 011008-21 (DESIGN) · "
          "EIT 011014 = EIT STANDARD 011014-19 (MATERIALS AND CONSTRUCTION) · ksc = kg/cm² (1 MPa ≈ 10.2 ksc).", -1)


def stirrup(ps, tl, tr, br, bl, leg, layer="S-REBR-SEC"):
    """closed stirrup on its centreline. Each corner is an arc concentric with its corner bar
    (corner = (cx, cy, R), R = bar radius + half stirrup diameter), so the stirrup wraps the bars.
    Both 135 deg hooks are at the top-left bar: one end wraps from the top edge round to 225 deg, the other
    from the left edge round to 45 deg; the two legs run into the core at 45 deg, one each side of the bar."""
    def pt(c, ang):
        return (c[0] + c[2] * math.cos(math.radians(ang)), c[1] + c[2] * math.sin(math.radians(ang)))
    b = lambda deg: math.tan(math.radians(deg) / 4)          # bulge of a CCW arc of 'deg'
    d = (0.7071, -0.7071)                                     # hook legs: 45 deg down into the core
    p45, p225 = pt(tl, 45), pt(tl, 225)
    pts = [(p45[0] + leg * d[0], p45[1] + leg * d[1], 0),    # hook end 1
           (*p45, b(135)), (*pt(tl, 180), 0),                 # wrap TL bar 45 -> 180
           (*pt(bl, 180), b(90)), (*pt(bl, 270), 0),
           (*pt(br, 270), b(90)), (*pt(br, 0), 0),
           (*pt(tr, 0), b(90)), (*pt(tr, 90), 0),
           (*pt(tl, 90), b(135)), (*p225, 0),                 # wrap TL bar 90 -> 225
           (p225[0] + leg * d[0], p225[1] + leg * d[1], 0)]  # hook end 2
    e = ps.add_lwpolyline(pts, format="xyb", dxfattribs=A(layer))
    e.dxf.flags = e.dxf.flags | 128
    return e


# ======================================================================= typical details band
def ptitle(ps, x, y, name, scale):
    """view title of the general rule (view_title) x K: bold title on an underline, scale text below"""
    yl = y - TH - 0.9 * K
    text(ps, name, (x, yl + 0.9 * K), TH, "S-TEXT", style="ANB")
    line(ps, (x, yl), (x + text_w(name, TH, "ANB") + 3.0 * K, yl), "S-TITLE")
    text(ps, scale, (x, yl - 1.2 * K), TB, "S-TEXT", align=TA.TOP_LEFT)


def note_lines(ps, x, y, s, width):
    for k, ln in enumerate(wrap_s(s, TB, width)):
        text(ps, ln, (x, y - TB - k * LP), TB, "S-TEXT")


def det_cover(ps, x, y, w):
    """typical beam section 250 x 350 at 1:10 - clear cover to the stirrup"""
    ptitle(ps, x, y, "TYPICAL COVER - BEAM SECTION", "SCALE 1:10")
    k = 0.1
    B, D = 250, 350
    bx, bh = B * k, D * k
    x0, y0 = x + 8, y - 10 - bh
    pline(ps, [(x0, y0), (x0 + bx, y0), (x0 + bx, y0 + bh), (x0, y0 + bh)], "S-CONC", close=True)
    c, ds = 40, 9
    rb, rt = 10, 8                                               # 3-DB20 bottom, 2-DB16 top
    ib, it = c + ds + rb, c + ds + rt                            # bar centre insets (mm)
    corner = lambda px, py, r: (x0 + px * k, y0 + py * k, (r + ds / 2) * k)
    tl, tr = corner(it, D - it, rt), corner(B - it, D - it, rt)
    bl, br = corner(ib, ib, rb), corner(B - ib, ib, rb)
    stirrup(ps, tl, tr, br, bl, max(6 * ds, 75) * k)
    for cx in (ib, B / 2, B - ib):
        dot(ps, (x0 + cx * k, y0 + ib * k), rb * k)
    for cx in (it, B - it):
        dot(ps, (x0 + cx * k, y0 + (D - it) * k), rt * k)
    dim(ps, (x0, y0), (x0 + bx, y0), (0, y0 - 4.5), 1, text=str(B))
    dim(ps, (x0 + bx, y0), (x0 + bx, y0 + bh), (x0 + bx + 4.5, 0), 1, angle=90, text=str(D))
    dim(ps, (x0, y0), (x0, y0 + c * k), (x0 - 4.5, 0), 1, angle=90, text="c")
    dim(ps, (x0, y0 + bh), (x0 + c * k, y0 + bh), (0, y0 + bh + 3), 1, text="c")
    tx = x0 + bx + 9
    tw = w - (tx - x)
    note_lines(ps, tx, y0 + bh, "c = CLEAR COVER TO THE OUTERMOST BAR: THE STIRRUP IN BEAMS, THE TIE OR SPIRAL IN "
               "COLUMNS, THE OUTER LAYER IN SLABS AND WALLS. VALUES BY ELEMENT: TABLE 7 (INTERIOR BEAMS AND "
               "COLUMNS 40).", tw)
    note_lines(ps, tx, y0 + 14, "STIRRUP CORNERS WRAP THE CORNER BARS; BOTH 135° HOOKS ROUND THE SAME BAR. "
               "SPACERS UNDER THE STIRRUP AT ≤ 1.0 m. [EIT 011008 7.7.1]", tw)


def det_hooks(ps, x, y, w):
    """standard hooks - N.T.S., stacked; bars drawn with the bar pen, bends filleted"""
    ptitle(ps, x, y, "STANDARD HOOKS", "N.T.S.")
    dbd = 0.55
    tx = x + 24
    r1 = y - 12.0                                                # 90 deg hook
    bar(ps, [(x + 2, r1), (x + 15, r1), (x + 15, r1 - 8)], dbd)
    text(ps, "12 db", (x + 16.2, r1 - 5.5), TB, "S-TEXT")
    text(ps, "90° - MAIN BARS", (tx, r1 - 1.0), TB, "S-TEXT", style="ANB")
    text(ps, "EXTENSION 12 db", (tx, r1 - 1.0 - LP), TB, "S-TEXT")
    r2 = r1 - 16.0                                               # 180 deg hook
    bar(ps, [(x + 2, r2), (x + 14, r2), (x + 14, r2 - 4.0), (x + 9.5, r2 - 4.0)], dbd)
    text(ps, "180° - MAIN BARS", (tx, r2 - 1.0), TB, "S-TEXT", style="ANB")
    text(ps, "EXTENSION 4 db ≥ 65", (tx, r2 - 1.0 - LP), TB, "S-TEXT")
    r3 = r2 - 11.0                                               # 135 deg stirrup / tie
    s_, rd, rs = 9.0, 0.7, 0.3
    cn = [(x + 4 + rd, r3 - rd), (x + 4 + s_ - rd, r3 - rd), (x + 4 + s_ - rd, r3 - s_ + rd), (x + 4 + rd, r3 - s_ + rd)]
    stirrup(ps, *[(cx, cy, rd + rs) for cx, cy in cn], 3.6, "S-REBR")
    for cx, cy in cn:
        dot(ps, (cx, cy), rd)
    text(ps, "135° - STIRRUPS, TIES", (tx, r3 - 3.0), TB, "S-TEXT", style="ANB")
    text(ps, "EXTENSION 6 db ≥ 75", (tx, r3 - 3.0 - LP), TB, "S-TEXT")
    text(ps, "BENDS: TABLE IN 5 [EIT 011008 7.1, 7.2]", (tx, r3 - 3.0 - 2 * LP), TB, "S-TEXT")


def det_laps(ps, x, y, w):
    """lap splices staggered - N.T.S."""
    ptitle(ps, x, y, "TYPICAL LAP SPLICES - STAGGER", "N.T.S.")
    xa, xb = x + 2, x + w - 3
    L = 15.0
    rows = [(y - 16, xa + 7), (y - 22, xa + 7 + L + 12), (y - 28, xa + 7)]
    for yy, xl in rows:
        line(ps, (xa, yy), (xl + L, yy), "S-REBR")
        line(ps, (xl, yy + 1.0), (xb, yy + 1.0), "S-REBR")
        for t in (xl + 2, xl + L / 2, xl + L - 2):                # tie wire
            line(ps, (t - 0.4, yy - 0.6), (t + 0.4, yy + 1.6), "S-ANNO")
    y1, xl1 = rows[0]
    y2, xl2 = rows[1]
    dim(ps, (xl1, y1 + 1.0), (xl1 + L, y1 + 1.0), (0, y1 + 4.5), 1, text="LAP (TABLE 6)")
    dim(ps, (xl1 + L, y2), (xl2, y2), (0, y2 - 10.0), 1, text="≥ 1.0 m CLEAR")
    note_lines(ps, x + 2, y - 40, "LAPS OF ADJACENT BARS STAGGERED ≥ 1.0 m CLEAR; ≤ 50 % OF THE BARS LAPPED AT ONE "
               "SECTION; BARS IN CONTACT, TIED WITH ≥ 0.9 mm WIRE. LAP ONLY WHERE SHOWN OR APPROVED; NO LAPS FOR BARS "
               "> DB36 OR IN BEAM-COLUMN JOINTS. [EIT 011008 12.13, 12.14; EIT 011014 2.5.1.4]", w - 3)


BAND = [(det_cover, 0.40), (det_hooks, 0.27), (det_laps, 0.33)]
BAND_GAP = 6.0


def band(ps, ytop, xleft):
    """typical-details band from xleft to the right edge of the note area (under columns 2 and 3)"""
    line(ps, (xleft, ytop + 2.5), (CX1, ytop + 2.5), "S-TTLB-THIN")
    text(ps, "TYPICAL DETAILS", (xleft, ytop - TH), TH, "S-TEXT", style="ANB")
    yp = ytop - HP - 1.0
    wt = CX1 - xleft - (len(BAND) - 1) * BAND_GAP
    x = xleft
    for fn, fr in BAND:
        fn(ps, x, yp, fr * wt)
        x += fr * wt + BAND_GAP


def col_bottoms(yb):
    """column 1 runs to the foot of the sheet; columns 2 .. NCOL stop at yb, above the details band"""
    return [FY0 + 3.0] + [yb] * (NCOL - 1)


def fits(yb):
    f = Flow(None, col_bottoms(yb), draw=False)
    content(f)
    return f.col < NCOL


def sheet_1001():
    ps = new_sheet(0)
    # balance columns 2 .. NCOL: highest common bottom line at which all notes still fit
    lo, hi = FY0 + 3.0, CY1 - 20
    for _ in range(40):
        mid = (lo + hi) / 2
        if fits(mid):
            lo = mid
        else:
            hi = mid
    yb = lo
    f = Flow(ps, col_bottoms(yb))
    content(f)
    print(f"  notes: K = {K:.3f}: text {TB:.2f} / {TH:.2f}, pitch {LP:.2f}, table row {TRH:.2f}")
    print(f"  notes: {f.col + 1} columns, column width {COLW:.1f} mm; columns 2-{NCOL} end at y = {yb:.1f}")
    for k in range(1, NCOL):                                  # thin grey column rules
        xr = CX0 + k * (COLW + CGAP) - CGAP / 2
        line(ps, (xr, (FY0 + 3.0) if k == 1 else yb + 1.0, ), (xr, CY1), "S-TTLB-THIN")
    xleft = CX0 + COLW + CGAP
    band(ps, yb - 5.0, xleft)
    print(f"  details band: {yb - 5.0 - FY0:.0f} mm tall, {CX1 - xleft:.0f} mm wide")


sheet_1001()
if "Layout1" in doc.layouts:
    doc.layouts.delete("Layout1")
OUT.mkdir(parents=True, exist_ok=True)
doc.saveas(DXF)
print("saved", DXF)
