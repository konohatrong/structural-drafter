"""
Steel layers and drawing helpers on top of the general engine (drafter/td_engine.py): steel layers and the EIT grid
linetype, weld graphics (hatch only), AWS A2.4 weld symbols, pipe breaks, CHS sections, plates, holes, slots, bolts,
cutting planes, detail callouts, work points and member tags. Rules: docs/steel/STEEL_DETAILING_INSTRUCTION.md S4 - S5,
docs/general/SYMBOLS.md section 4, docs/general/ANNOTATION_ALIGNMENT_GUIDE.md section 9.

Import it from the job's engine module AFTER the project data and options are set on td_engine:
    from drafter import td_engine
    from drafter.td_engine import *
    ... PROJ.update(...), td_engine.LEADER_ORTH = True, TABLES ...
    from drafter.steel import *
Importing it adds the steel layers to the open document (once per process).
First used on jobs/steel_roof_truss (split out of srt_engine.py, 2026-10-03; output unchanged).
"""
import math

from .td_engine import *                                           # noqa: F401,F403

# --------------------------------------------------------------------------- steel layers (pens by colour)
# EIT grid / centre line (DRAWING_STANDARD 19, S-GRID): chain 12 / 2 / 2 / 2 mm plotted, 0.18, grey ACI 8.
# Plotted = pattern x LTS / SC (td_engine), so the pattern is the plotted length / 0.15.
_K = LTS / SC
doc.linetypes.add("EIT_GRID", pattern=[18 / _K, 12 / _K, -2 / _K, 2 / _K, -2 / _K],
                  description="EIT grid / centre line 12-2-2-2 (plotted)")
STEEL_LAYERS = [
    ("S-GRID", 8, "EIT_GRID", True),             # truss and member centre lines, work lines: grey chain 0.18
    ("S-STL-WALL", 8, HID_FINE, True),           # inner wall of a hollow section: fine hidden, grey 0.18
    ("S-STL", 4, "Continuous", True),            # steel member / plate outline (cut or main subject): 0.35
    ("S-STL-VIS", 5, "Continuous", True),        # steel seen beyond: 0.25
    ("S-STL-HIDN", 252, HID_FINE, True),         # steel hidden: grey dashed
    ("S-STL-NF", 252, "Continuous", True),       # steel that is not the subject of the detail: grey
    ("S-BOLT", 6, "Continuous", True),           # bolts, holes: 0.25
    ("S-WELD", 9, "Continuous", True),           # weld bead fill: grey
    ("S-CALL", 6, HID, True),                    # detail callout boundary: dashed (HIDDENX2) 0.25
]
for n, c, lt, plot in STEEL_LAYERS:
    lay = doc.layers.add(n, color=c, linetype=lt)
    lay.dxf.lineweight = PEN[c][0]
    lay.dxf.plot = 1 if plot else 0
    LAYER_LW[n] = PEN[c][0]
_cen = doc.layers.get("S-CENT")                    # bolt / hole / rod centre lines: grey ACI 8, 0.18 (user 2026-10-03)
_cen.color = 8
_cen.dxf.lineweight = PEN[8][0]
LAYER_LW["S-CENT"] = PEN[8][0]

WELD_MIN = 1.0                     # smallest plotted fillet leg, mm (like the minimum bar dot)
lay = doc.layers.get("Defpoints") if doc.layers.has_entry("Defpoints") else doc.layers.add("Defpoints", color=7)
lay.dxf.plot = 0                                  # AutoCAD never plots Defpoints: weld hatch boundaries


def weld_region(sp, P, pts, w, S):
    """a weld as seen: the region hatched at 45 deg (ANSI31, S-WELD), spacing a third of the leg (0.2 - 0.5 mm
    plotted). Its boundary goes on Defpoints - kept for the hatch, never plotted"""
    pitch = min(0.5, max(0.2, w / S / 3))
    q = [P(*v) for v in pts]
    hatch(sp, q, "ANSI31", pscale("ANSI31", S, pitch), layer="S-WELD")
    pline(sp, q, "Defpoints", close=True)


def weld_bead(sp, P, J, e1, e2, w, S):
    """fillet weld in cross-section: legs w from the root J along the unit vectors e1, e2 (true size, but at least
    WELD_MIN plotted)"""
    w = max(w, WELD_MIN * S)
    weld_region(sp, P, [J, (J[0] + e1[0] * w, J[1] + e1[1] * w), (J[0] + e2[0] * w, J[1] + e2[1] * w)], w, S)


def weld_band(sp, P, p0, p1, toward, w, S):
    """fillet weld along a straight joint line p0-p1 seen face-on: a band of width w on the side 'toward'"""
    w = max(w, WELD_MIN * S)
    weld_region(sp, P, [p0, p1, (p1[0] + toward[0] * w, p1[1] + toward[1] * w),
                        (p0[0] + toward[0] * w, p0[1] + toward[1] * w)], w, S)


def _break_arc(n, n0, R):
    """offset along the member of the break arc on the half n0 .. n0 + R at n (chs_break geometry)"""
    h = 0.26 * R
    rho = (R * R / 4 + h * h) / (2 * h)
    nm = n0 + R / 2
    return math.sqrt(max(rho * rho - (n - nm) ** 2, 0.0)) - (rho - h)


def break_point(c, u, D_, n):
    """where a line inside the tube at offset n (along nv = (-u_y, u_x)) meets the pipe break at c (u toward the
    part broken away): the first break curve met from the kept side - the single arc on the n < 0 half, the inner
    arc of the lens on the n > 0 half"""
    R = D_ / 2
    s = _break_arc(n, -R, R) if n < 0 else -_break_arc(n, 0.0, R)
    nv = (-u[1], u[0])
    return (c[0] + n * nv[0] + s * u[0], c[1] + n * nv[1] + s * u[1])


def chs_break(sp, c, u, D_, t, S, layer="S-STL"):
    """conventional break of a round tube: across the tube, one half is a single arc bulging toward the broken-away
    part, the other half a lens (that arc plus one bulging back) - the cut end seen. Circular arcs, sagitta R/4.
    c = point on the member axis at the cut, u = unit vector pointing to the part that is broken away"""
    R = D_ / 2
    h = 0.26 * R                                      # sagitta of every arc (chord = R)
    nv = (-u[1], u[0])
    Q = lambda n_, s_: (c[0] + n_ * nv[0] + s_ * u[0], c[1] + n_ * nv[1] + s_ * u[1])
    rho = (R * R / 4 + h * h) / (2 * h)               # radius of a circular arc on a chord R with sagitta h

    def arc(n0, sgn, k=12):
        nm = n0 + R / 2
        return [Q(n, sgn * (math.sqrt(max(rho * rho - (n - nm) ** 2, 0.0)) - (rho - h)))
                for n in (n0 + R * i / k for i in range(k + 1))]

    pline(sp, arc(-R, 1) + arc(0.0, 1)[1:], layer)   # single arc on one half, outer arc of the lens on the other
    pline(sp, arc(0.0, -1), layer)                    # inner arc of the lens (bulging back)


def chs_section(sp, c, D_, t, layer="S-STL", fill=True):
    """CHS cut in section: outer and inner circle, wall solid-filled (thin walls read as a solid ring)"""
    sp.add_circle(c, D_ / 2, dxfattribs=A(layer))
    sp.add_circle(c, D_ / 2 - t, dxfattribs=A(layer))
    if fill:
        h = sp.add_hatch(color=256, dxfattribs=A("S-WELD"))
        h.paths.add_edge_path().add_arc(c, D_ / 2, 0, 360)
        h.paths.add_edge_path(flags=16).add_arc(c, D_ / 2 - t, 0, 360)
        h.set_solid_fill(color=256)


def plate(sp, P, pts, layer="S-STL"):
    pline(sp, [P(*q) for q in pts], layer, close=True)


def hole(sp, c, d, S, layer="S-BOLT"):
    """bolt hole: circle and a centre mark"""
    sp.add_circle(c, d / 2, dxfattribs=A(layer))
    k = d / 2 + 1.5 * S
    line(sp, (c[0] - k, c[1]), (c[0] + k, c[1]), "S-CENT")
    line(sp, (c[0], c[1] - k), (c[0], c[1] + k), "S-CENT")


def slot(sp, c, d, length, S, layer="S-BOLT"):
    """long slot along x, d wide, 'length' overall"""
    r, a = d / 2, length / 2 - d / 2
    sp.add_arc((c[0] - a, c[1]), r, 90, 270, dxfattribs=A(layer))
    sp.add_arc((c[0] + a, c[1]), r, 270, 90, dxfattribs=A(layer))
    line(sp, (c[0] - a, c[1] + r), (c[0] + a, c[1] + r), layer)
    line(sp, (c[0] - a, c[1] - r), (c[0] + a, c[1] - r), layer)
    line(sp, (c[0] - length / 2 - 1.5 * S, c[1]), (c[0] + length / 2 + 1.5 * S, c[1]), "S-CENT")


def bolt_side(sp, P, x, y0, y1, d, S, layer="S-BOLT"):
    """bolt seen from the side through plates y0..y1 (axis along y): shank, head and nut + washer outlines"""
    hh, nh, w = 0.65 * d, 0.85 * d, 1.7 * d
    line(sp, P(x - d / 2, y0), P(x - d / 2, y1), "S-STL-HIDN")
    line(sp, P(x + d / 2, y0), P(x + d / 2, y1), "S-STL-HIDN")
    pline(sp, [P(x - w / 2, y1), P(x + w / 2, y1), P(x + w / 2, y1 + hh), P(x - w / 2, y1 + hh)], layer, close=True)
    pline(sp, [P(x - w / 2, y0), P(x + w / 2, y0), P(x + w / 2, y0 - nh), P(x - w / 2, y0 - nh)], layer, close=True)
    line(sp, P(x - d / 2 - 0.5 * d, y0 - nh - 0.4 * d), P(x + d / 2 + 0.5 * d, y0 - nh - 0.4 * d), layer)


def weld(sp, tip, ref, S, size, all_round=False, field=False, other=False, tail=None, left=False, side=None,
         size2=None, length=None, groove=None, ndt=None, rl=None):
    """AWS A2.4 weld symbol (DSC pp.115-127, DG21 Fig 3-36): arrow(s) to the joint, reference line, basic symbol,
    size left of it and length right of it on the same side, all-round circle, field flag pointing to the tail,
    tail with a reference. ref = junction of the arrow and the reference line; the line runs right (left=True:
    runs left). tip = a point or a list of points (one arrow each). side = "arrow" (below the line, default),
    "other" (above) or "both" (other=True is "both"); both sizes are always written (size2 = other side).
    groove = "bevel": bevel-groove symbol (perpendicular leg on the left), size written as (E), the arrow broken
    toward the member to prepare. ndt = test letters on the line beyond the symbol (e.g. "MT"). Drawn on S-ANNO.
    The arrow is never collinear with the reference line."""
    side = side or ("both" if other else "arrow")
    rl = rl or (16.0 + (5.0 if length else 0.0) + (4.0 if ndt else 0.0)) * S
    sgn = -1 if left else 1
    end = (ref[0] + sgn * rl, ref[1])
    line(sp, ref, end, "S-ANNO")
    for tp in (tip if isinstance(tip, list) else [tip]):
        if groove:                                      # broken arrow: the break points to the prepared member
            mx, my = ref[0] + 0.55 * (tp[0] - ref[0]), ref[1] + 0.55 * (tp[1] - ref[1])
            kx, ky = mx + 1.6 * S * sgn, my
            pline(sp, [ref, (mx, my), (kx, ky), tp], "S-ANNO")
            arrowhead(sp, tp, (kx, ky), 2.0 * S)
        else:
            line(sp, ref, tp, "S-ANNO")
            arrowhead(sp, tp, ref, 2.0 * S)
    xs = ref[0] + 7.0 * S if not left else ref[0] - (7.0 + (5.0 if length else 0.0) + (4.0 if ndt else 0.0)) * S
    tri = 2.4 * S
    sides = {"arrow": (-1,), "other": (1,), "both": (-1, 1)}[side]
    for sd in sides:
        y = ref[1]
        if groove == "bevel":                          # | / : vertical leg on the left, root on the line
            line(sp, (xs, y), (xs, y + sd * tri), "S-ANNO")
            line(sp, (xs, y), (xs + tri, y + sd * tri), "S-ANNO")
        else:                                          # fillet: perpendicular leg on the left
            pline(sp, [(xs, y), (xs, y + sd * tri), (xs + tri, y)], "S-ANNO")
        sz = size if sd == -1 or side == "other" else (size2 if size2 is not None else size)
        lab = f"({sz})" if groove else f"{sz}"
        text(sp, lab, (xs - 1.0 * S, y + sd * 0.8 * S), 2.0 * S,
             align=TA.TOP_RIGHT if sd == -1 else TA.BOTTOM_RIGHT)
        if length:
            text(sp, f"{length}", (xs + tri + 1.0 * S, y + sd * 0.8 * S), 2.0 * S,
                 align=TA.TOP_LEFT if sd == -1 else TA.BOTTOM_LEFT)
    if ndt:
        xn = xs + tri + (1.0 + (text_w(str(length), 2.0) + 1.5 if length else 0.0)) * S
        text(sp, ndt, (xn, ref[1] - sides[0] * 0.8 * S), 2.0 * S,
             align=TA.BOTTOM_LEFT if sides[0] == -1 else TA.TOP_LEFT)
    if all_round:
        sp.add_circle(ref, 1.3 * S, dxfattribs=A("S-ANNO"))
    if field:                                          # flag on the junction, pointing toward the tail
        fl = [(ref[0], ref[1]), (ref[0], ref[1] + 4.5 * S), (ref[0] + sgn * 3.0 * S, ref[1] + 3.6 * S),
              (ref[0], ref[1] + 2.7 * S)]
        sp.add_solid([fl[1], fl[2], fl[3]], dxfattribs=A("S-ANNO"))
        line(sp, fl[0], fl[1], "S-ANNO")
    if tail:
        tend = end
        line(sp, tend, (tend[0] + sgn * 1.8 * S, tend[1] + 1.8 * S), "S-ANNO")
        line(sp, tend, (tend[0] + sgn * 1.8 * S, tend[1] - 1.8 * S), "S-ANNO")
        text(sp, tail, (tend[0] + sgn * 2.6 * S, tend[1]), 2.0 * S,
             align=TA.MIDDLE_LEFT if not left else TA.MIDDLE_RIGHT)


if not doc.layers.has_entry("S-CUTL"):
    lay = doc.layers.add("S-CUTL", color=6, linetype="EIT_GRID")
    lay.dxf.lineweight = PEN[6][0]
    LAYER_LW["S-CUTL"] = PEN[6][0]


def cutmark(sp, p1, p2, look, label, S, ref=None, ends_only=True, lab="end"):
    """cutting plane (EIT: chain 0.25, heavy end strokes): arrows toward the viewing direction 'look' (unit vector;
    sections look left or down, DSC p.94 #10), the section letter at each end, the sheet below it. ends_only:
    the chain is left out across the drawing (only the end strokes and arrows outside the object)"""
    (x1, y1), (x2, y2) = p1, p2
    Lc = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / Lc, (y2 - y1) / Lc
    if not ends_only:
        line(sp, p1, p2, "S-CUTL")
    for (px, py), sg in ((p1, 1), (p2, -1)):
        line(sp, (px, py), (px + ux * sg * 4 * S, py + uy * sg * 4 * S), "S-STL")
        tip = (px + look[0] * 4.5 * S, py + look[1] * 4.5 * S)
        line(sp, (px, py), tip, "S-SYMB")
        arrowhead(sp, tip, (px, py), 2.0 * S, "S-SYMB")
        if lab == "side":                                          # beside the arrow, beyond its tip
            q = (px + look[0] * 7.5 * S, py + look[1] * 7.5 * S)
            text(sp, label, (q[0], q[1] + 0.6 * S), 2.8 * S, "S-TEXT", TA.BOTTOM_CENTER, style="ANB")
            if ref:
                text(sp, ref, (q[0], q[1] - 0.6 * S), 2.0 * S, "S-TEXT", TA.TOP_CENTER)
        else:                                                      # beyond the end of the plane
            q = (px - ux * sg * 3.5 * S, py - uy * sg * 3.5 * S)
            if ref:
                text(sp, f"{label}/{ref}", q, 2.4 * S, "S-TEXT", TA.MIDDLE_CENTER, style="ANB")
            else:
                text(sp, label, q, 2.8 * S, "S-TEXT", TA.MIDDLE_CENTER, style="ANB")


def detail_callout(sp, P, c, r, S, at=0.0):
    """detail callout: a dashed circle (S-CALL, 0.25) round the part enlarged elsewhere. Returns the point of the
    circle edge at the angle 'at' (deg; 0 = right-most, facing a right note column; -90 = bottom): the leader's arrow
    lands there and runs to a note 'DETAIL n/sheet - WHAT' (annotation guide 9.7). Pick the point in clear space,
    off members and lines"""
    sp.add_circle(P(*c), r, dxfattribs=A("S-CALL"))
    a = math.radians(at)
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


def wp_mark(sp, c, S, label="WP"):
    """work point: small cross in a circle"""
    r = 1.2 * S
    sp.add_circle(c, r, dxfattribs=A("S-SYMB"))
    line(sp, (c[0] - r, c[1]), (c[0] + r, c[1]), "S-SYMB")
    line(sp, (c[0], c[1] - r), (c[0], c[1] + r), "S-SYMB")


def _seg_dist(p, a, b):
    ax, ay, bx, by = a[0], a[1], b[0], b[1]
    L2 = (bx - ax) ** 2 + (by - ay) ** 2 or 1e-9
    t = max(0.0, min(1.0, ((p[0] - ax) * (bx - ax) + (p[1] - ay) * (by - ay)) / L2))
    return math.hypot(p[0] - ax - t * (bx - ax), p[1] - ay - t * (by - ay))


def place_tag(cands, w, h, obstacles, taken):
    """the candidate tag centre whose box keeps the largest clearance from the obstacle segments
    [(a, b, half width)] and from the boxes already placed [(cx, cy, w, h)]"""
    best, bv = None, -1e18
    for c in cands:
        pts = [(c[0] + dx * w / 2, c[1] + dy * h / 2) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
        d = min(_seg_dist(q, a, b) - hw for q in pts for a, b, hw in obstacles)
        for tx, ty, tw, th in taken:
            gx = max(0.0, abs(c[0] - tx) - (w + tw) / 2)
            gy = max(0.0, abs(c[1] - ty) - (h + th) / 2)
            d = min(d, math.hypot(gx, gy) if gx or gy else -1e6)
        if d > bv:
            best, bv = c, d
    return best


def tag_r(s):
    """radius (paper mm) of the circle round a member mark"""
    return max(2.4, (text_w(s, 2.0, "ANB") + 1.4) / 2)


def tag(sp, c, s, S, layer="S-TEXT"):
    """member mark (e.g. D1) in a circle"""
    sp.add_circle(c, tag_r(s) * S, dxfattribs=A("S-SYMB"))
    text(sp, s, c, 2.0 * S, layer, TA.MIDDLE_CENTER, style="ANB")
