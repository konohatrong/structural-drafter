"""
Typical-detail engine (11xx series): document, layers, pens, dimension styles, leader engine, title strip,
viewports, stirrup / crosstie graphics and paper-space table / notes helpers.

Rule    : normal drawing rule (2.0 / 2.8 text, 2 mm arrows, standard pens) - detail sheets.
Engine  : from jobs/general_notes/build_gn.py.  Content modules: td_columns.py (1101/1102), td_beams.py (1111/1112).
Driver  : build_td.py.   Guide: TYPICAL_DETAILS_INSTRUCTION.md
"""
import math
import sys
from pathlib import Path

import ezdxf
from ezdxf import bbox
from ezdxf.path import make_path
from ezdxf.enums import TextEntityAlignment as TA, MTextEntityAlignment as MA


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
SHEETS = []            # filled by the content module: (series, title lines, scale text)
EXT = {}               # model extents per view key, filled by the content module (capture)
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

doc.styles.add("AN", font="ARIALN.TTF")
doc.styles.add("ANB", font="ARIALNB.TTF")

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
from fontTools.pens.boundsPen import BoundsPen as _BP
from fontTools.ttLib import TTFont as _TTF

_FONTS = {}
for _k, _f in (("AN", "ARIALN.TTF"), ("ANB", "ARIALNB.TTF")):
    _t = _TTF("C:/Windows/Fonts/" + _f)
    _gs = _t.getGlyphSet()
    _bp = _BP(_gs)
    _gs[_t.getBestCmap()[ord("H")]].draw(_bp)
    _FONTS[_k] = (_t.getBestCmap(), _t["hmtx"], _bp.bounds[3])


def text_w(s, h, style="AN"):
    """plotted width of a single-line string at text height h (AutoCAD TTF height = cap height)"""
    cmap, hm, cap = _FONTS[style]
    return sum(hm[cmap.get(ord(c), cmap[ord("M")])][0] for c in s) / cap * h


def wrap(s, h, width):
    out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if cur and text_w(t, h) > width:
            out.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out


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
_DIMSEGS = []          # dimension + extension lines of the current view: (x0, y0, x1, y1) - leaders never cross them
DIM_CLEAR = 1.2        # a leader's horizontal run keeps this clear of a dimension / extension line end (paper mm)
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
    pts = [tip] + path[1:] + [(ex, ky)]
    for (x0, y0, x1, y1) in _DIMSEGS:                 # a leader crossing a dimension reads as part of it
        if any(_cross(p, q, (x0, y0), (x1, y1)) for p, q in zip(pts[:-1], pts[1:])):
            print(f"  !! leader crosses a dimension: '{n['s'][:40]}'")
            break
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
                dd = DIM_CLEAR * S
                for x0, y0, x1, y1 in _DIMSEGS:               # the run must not cross a dimension / extension line
                    if max(x0, x1) > a and min(x0, x1) < b:
                        ylo, yhi = min(y0, y1), max(y0, y1)
                        out.append((-(yhi + dd) - 0.5 * PITCH * S, -(ylo - dd) - 0.5 * PITCH * S))
                return sorted(out)

            RB = {k: run_bands(k) for k in range(len(ns))}

            def place_up(order):
                """upward packing (note_cfg(up<side>=True)): lowest tip first, each note at or above its desired
                knee and above the previous one, stepping UP past forbidden run heights - never below ymin"""
                half = 0.5 * PITCH * S
                cur = _CFG.get("ymin" + side, -1e18)
                res = {}
                for k in order:
                    ln = lens[k]
                    top = max(ns[k]["tip"][1] + RISE * S + half, cur + ln)     # top of the note text box
                    moved = True
                    while moved:
                        moved = False
                        for u0, u1 in RB[k]:                                    # forbidden knee heights
                            y_lo, y_hi = -u1 - half, -u0 - half
                            if y_lo < top - half < y_hi:
                                top = y_hi + half
                                moved = True
                    res[k] = (kx, top - half)
                    cur = top
                return res

            def place(order):
                if _CFG.get("up" + side):
                    return place_up(order)
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
            order = sorted(range(len(ns)), key=lambda k: (1 if _CFG.get("up" + side) else -1) * ns[k]["tip"][1])
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
    _DIMSEGS.clear()
    for e in msp:
        if e.dxf.handle in before:
            continue
        if e.dxftype() == "DIMENSION":
            for ve in e.virtual_entities():
                if ve.dxftype() == "LINE":
                    _DIMSEGS.append((ve.dxf.start.x, ve.dxf.start.y, ve.dxf.end.x, ve.dxf.end.y))
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
    _DIMSEGS.clear()
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
    text(ps, "(TYPICAL DETAILS)", (xc, (by0 + by1) / 2 - 2.5), 2.0, align=TA.MIDDLE_CENTER)

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
    w = text_w(name, 2.8, "ANB") + 3   # measured (fontTools)
    text(ps, name, (x, y + 0.9), 2.8, "S-TITLE", style="ANB")
    line(ps, (x, y), (x + w, y), "S-TITLE")
    text(ps, f"SCALE {scale_txt}", (x, y - 1.2), 2.0, align=TA.TOP_LEFT)
    top, bot = bubble
    r = 4.6
    if note:                          # below the bubble (bottom at y - r), never beside it
        text(ps, note, (x, y - r - 1.6), 2.0, align=TA.TOP_LEFT)
        if y - r - 1.6 - 2.0 < FY0 + 1:
            print(f"  !! view-title note too low: '{note[:40]}'")
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


def rng(a, b, s):
    out, y = [], a
    while y <= b + 1e-6:
        out.append(y)
        y += s
    return out


# ----------------------------------------------------------------------- 1102: tie arrangements (sections, 1:25)
def crosstie(sp, pa, pb, r, leg, layer="S-REBR-SEC"):
    """crosstie between two bars, wrapping both (arcs concentric with the bars, radius r).
    The body runs tangent to the bars on the -n side; at pa it bends 135 deg round the bar with the
    tail back into the core, at pb 90 deg round the bar with the tail along the face (outside the hoop).
    The side (s = +/-1) is chosen so the 135 deg tail points away from the top-left corner, where the
    hoop's own 135 deg hooks are."""
    (xa, ya), (xb, yb) = pa, pb
    L = math.hypot(xb - xa, yb - ya)
    ux, uy = (xb - xa) / L, (yb - ya) / L
    back = math.degrees(math.atan2(-uy, -ux))
    tail = lambda s: math.radians(back - 135 * s)               # 135 deg tail direction at pa
    toward_tl = lambda s: -math.cos(tail(s)) + math.sin(tail(s))
    s = min((1, -1), key=toward_tl)
    nx, ny = -uy * s, ux * s
    f0 = math.degrees(math.atan2(-ny, -nx))                   # body side of both bars
    on = lambda c, ang: (c[0] + r * math.cos(math.radians(ang)), c[1] + r * math.sin(math.radians(ang)))
    b = lambda deg: math.tan(math.radians(deg) / 4) * s
    a1 = on(pa, f0 - 135 * s)                                # 135 deg hook end of the arc at pa
    ta = tail(s)
    b1 = on(pb, f0 + 90 * s)                                 # 90 deg hook end of the arc at pb
    pts = [(a1[0] + leg * math.cos(ta), a1[1] + leg * math.sin(ta), 0),
           (*a1, b(135)), (*on(pa, f0), 0),
           (*on(pb, f0), b(90)), (*b1, 0),
           (b1[0] + leg * nx, b1[1] + leg * ny, 0)]
    e = sp.add_lwpolyline(pts, format="xyb", dxfattribs=A(layer))
    return e


# ======================================================================= paper-space text helpers (normal rule)
LPN = PITCH                      # 3.33 line pitch at 2.0 text


REL = ("=", "≤", "≥", "≈", "<", ">", "×", "+", "–", "−")


def glue(words):
    """keep a relation with its operands: 'hx ≤ 350', '(R = 5)', '≥ 1.2 ΣMb' never break inside"""
    out = []
    for w in words:
        if out and (w in REL or out[-1].split()[-1] in REL):
            out[-1] += " " + w
        else:
            out.append(w)
    return out


def wrap_s(s, h, width, style="AN"):
    out, cur = [], ""
    for w in glue(s.split()):
        t = (cur + " " + w).strip()
        if cur and text_w(t, h, style) > width:
            out.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out or [""]


def tbl(ps, x, y_top, widths, heads, rows, align, title=None, rh=5.2):
    """grid table, text 2.0; every cell centred on its row (MIDDLE alignment); align L / C per column"""
    if title:
        text(ps, title, (x, y_top + 2.0), 2.8, "S-TITLE", style="ANB")
    xs = [x]
    for w in widths:
        xs.append(xs[-1] + w)
    allrows = [heads] + rows
    cells = [[wrap_s(c, 2.0, w - 2.0, "ANB" if r == 0 or (i == 0) else "AN") for i, (c, w) in enumerate(zip(row, widths))]
             for r, row in enumerate(allrows)]
    y = y_top
    for r, row in enumerate(cells):
        n = max(len(c) for c in row)
        h = rh + (n - 1) * LPN
        line(ps, (xs[0], y), (xs[-1], y), "S-TTLB" if r <= 1 else "S-TTLB-THIN")
        ym = y - h / 2
        for i, (cl, cx) in enumerate(zip(row, xs)):
            cen = align[i] == "C"
            tx = cx + widths[i] / 2 if cen else cx + 1.2
            for k, ln in enumerate(cl):
                text(ps, ln, (tx, ym + ((len(cl) - 1) / 2 - k) * LPN), 2.0, "S-TEXT",
                     TA.MIDDLE_CENTER if cen else TA.MIDDLE_LEFT, style="ANB" if (r == 0 or i == 0) else "AN")
        y -= h
    line(ps, (xs[0], y), (xs[-1], y), "S-TTLB")
    for cx in xs:
        line(ps, (cx, y_top), (cx, y), "S-TTLB-THIN")
    return y


def zone(a, b, s, first=50):
    """stirrup positions from face a toward b (either direction): first at 'first', then s"""
    sg = 1 if b > a else -1
    out, x = [], a + sg * first
    while (x - b) * sg <= 1e-6:
        out.append(x)
        x += sg * s
    return out


def tick(sp, p, S, sgn=1, layer="S-REBR"):
    """end of an additional bar (TATA Fig 2.13): short inclined stroke across the bar end"""
    a = 1.1 * S
    line(sp, (p[0] - sgn * a * 0.5, p[1] - a), (p[0] + sgn * a * 0.5, p[1] + a), layer)


def bar_end_legend(ps, x, y_top, width):
    """paper-space key to the bar-end symbols used on elevations (TATA Fig 2.13 slash = end of a bar)"""
    text(ps, "BAR-END SYMBOLS", (x, y_top - 2.8), 2.8, "S-TITLE", style="ANB")
    rows = [
        ("TICK", "SLASH ACROSS A BAR END: THE BAR STOPS HERE (END OF AN ADDITIONAL / CUT-OFF BAR OR OF A LAPPED BAR)"),
        ("HOOK", "STANDARD 90° HOOK, 12 db TAIL, BENT IN THE DIRECTION DRAWN"),
        ("BREAK", "NO END MARK AT A BREAK LINE: THE BAR CONTINUES"),
        ("LAP", "LAPPED BARS: DRAWN APART FOR CLARITY, PLACED IN CONTACT; LAP LENGTH PER 1001 TABLE 6"),
    ]
    y = y_top - 2.8 - 5.0
    for kind, s in rows:
        lines = wrap_s(s, 2.0, width - 20)
        ym = y - (len(lines) - 1) * LPN / 2 - 1.0            # symbol centred on the text block
        if kind == "TICK":
            line(ps, (x, ym), (x + 14, ym), "S-REBR")
            line(ps, (x + 14 - 0.55, ym - 1.1), (x + 14 + 0.55, ym + 1.1), "S-REBR")
        elif kind == "HOOK":
            bar(ps, [(x, ym + 1.5), (x + 13, ym + 1.5), (x + 13, ym - 2.5)], 0.4)
        elif kind == "BREAK":
            line(ps, (x, ym), (x + 13, ym), "S-REBR")
            zbreak(ps, (x + 13, ym - 3.0), (x + 13, ym + 3.0), 1)
        else:
            line(ps, (x, ym + 0.7), (x + 11, ym + 0.7), "S-REBR")
            line(ps, (x + 4, ym - 0.7), (x + 16, ym - 0.7), "S-REBR")
        for k, ln in enumerate(lines):
            text(ps, ln, (x + 20, y - k * LPN), 2.0, align=TA.TOP_LEFT)
        y -= len(lines) * LPN + 2.0
    return y


def notes_block(ps, x, y_top, width, title, items):
    text(ps, title, (x, y_top - 2.8), 2.8, "S-TITLE", style="ANB")
    y = y_top - 2.8 - 3.0
    for num, s in items:
        lines = wrap_s(s, 2.0, width - 6.0)
        for k, ln in enumerate(lines):
            if k == 0:
                text(ps, num, (x, y - 2.0), 2.0, "S-TEXT")
            text(ps, ln, (x + 6.0, y - 2.0), 2.0, "S-TEXT")
            y -= LPN
        y -= 1.0
    return y
