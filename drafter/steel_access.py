"""
Steel access structures: stairs, guards and fixed ladders - drawing helpers on top of drafter/steel.py.
Rules: docs/steel/STEEL_DETAILING_INSTRUCTION.md S4.11, S4.13, S4.14 and docs/steel/stairs/17_STAIR_DETAILING_PRACTICE.md
and 18_LADDER_DETAILING.md (what a stair or ladder detail must show, view by view).

Opt-in: import it in the job's engine after drafter.steel:
    from drafter.steel import *
    from drafter.steel_access import *
Nothing here changes an existing helper; every function draws through P, the job's local-to-model transform
(P(u, z) -> model point), in real millimetres. Each function returns the segments it drew (local mm) so the job can
keep them as obstacles for tags and labels (clear_tag).
First used on RPM Staircase stair C review A3 and jobs/steel_ladder_typical (2026-10-15), after the user asked for
details "equivalent to" an office standard set of stair and ladder details.
"""
import math

from .steel import *                                               # noqa: F401,F403

_HID_LAYER = "S-STL-HIDN"
# steel cut in section, solid (steel S4.1): cyan 0.35, as the RPM engine first defined it
if "S-CUT" not in doc.layers:
    _l = doc.layers.add("S-CUT", color=4, linetype="Continuous")
    _l.dxf.lineweight = PEN[4][0]
    LAYER_LW["S-CUT"] = PEN[4][0]


# ------------------------------------------------------------------------------------------------ actual sections
# A steel member cut in a section, or seen end-on, is drawn as its actual profile - root and toe radii, flange taper,
# corner radii - as an outline, never as a solid fill that reads as a thick line (user, 2026-10-15: "not draw as thick
# line for steel section we draw actual section"; steel S4.15). Radii and the channel flange slope are those of the
# office block library (G:\My Drive\##Workset_Autocad\Autocad_Work_Set\Autocad_Work_Set\Block\Technical Standards\
# Steel Work: H-200X100X5.5 r 11, H-100X100X6 r 10, C-200X80X7.5 r1 12 / r2 6, C-150X75X6.5 r1 10 / r2 5, SQ tubes
# outer 3t / inner 2t); other sizes take the fallback rules below.
SLOPE_C = 0.0875                                  # JIS channel inner flange slope (blocks: 1 : 11.4, about 5 deg)
RADII = {"H 100x100x6x8": 10.0, "H 200x100x5.5x8": 11.0,
         "C 200x80x7.5x11": (12.0, 6.0), "C 150x75x6.5x10": (10.0, 5.0),
         "L 100x100x10": (10.0, 7.0), "L 50x50x5": (6.5, 3.0), "L 65x65x6": (8.5, 4.0), "L 75x75x6": (8.5, 4.0)}
# a thin wall or plate (less than about 1 mm on paper) is outlined with the fine pen, so its two edges do not merge
# into one heavy line (user, 2026-10-15, review of A6: "improve line weight")
if "S-CUT-FINE" not in doc.layers:
    _l = doc.layers.add("S-CUT-FINE", color=7, linetype="Continuous")
    _l.dxf.lineweight = PEN[7][0]
    LAYER_LW["S-CUT-FINE"] = PEN[7][0]


def _arc(c, r, a0, a1, n=8):
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
             c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def h_profile(h, b, tw, tf, r=None):
    """rolled H / I with parallel flanges: closed outline, origin at the web centre at mid-height"""
    r = r if r is not None else RADII.get(f"H {h:g}x{b:g}x{tw:g}x{tf:g}", round(1.3 * tf))
    x1, y1, xw, yf = b / 2, h / 2, tw / 2, h / 2 - tf
    pts = [(-x1, -y1), (x1, -y1), (x1, -yf)]
    pts += _arc((xw + r, -yf + r), r, 270, 180) + _arc((xw + r, yf - r), r, 180, 90)
    pts += [(x1, yf), (x1, y1), (-x1, y1), (-x1, yf)]
    pts += _arc((-xw - r, yf - r), r, 90, 0) + _arc((-xw - r, -yf + r), r, 0, -90)
    pts += [(-x1, -yf)]
    return [pts]


def c_profile(h, b, tw, tf, r1=None, r2=None):
    """JIS channel with the inner flange faces sloped SLOPE_C (thickness tf at mid-flange), root radius r1 and toe
    radius r2: closed outline, origin on the back of the web at mid-height, flanges toward +x"""
    rr = RADII.get(f"C {h:g}x{b:g}x{tw:g}x{tf:g}", (tf + 1.0, (tf + 1.0) / 2))
    r1 = rr[0] if r1 is None else r1
    r2 = rr[1] if r2 is None else r2
    m, s = SLOPE_C, math.sqrt(1 + SLOPE_C ** 2)
    xm = (tw + b) / 2
    yl = lambda x: -h / 2 + tf + m * (xm - x)                 # bottom flange inner face
    c1 = (tw + r1, yl(tw + r1) + r1 * s)                      # root circle: tangent to the web and the flange face
    c2 = (b - r2, yl(b - r2) - r2 * s)                        # toe circle: tangent to the toe and the flange face
    a1 = math.degrees(math.atan2(-1 / s, -m / s))             # tangent point on the flange face, root circle
    a2 = math.degrees(math.atan2(1 / s, m / s))               # tangent point on the flange face, toe circle
    bottom = [(0.0, -h / 2), (b, -h / 2), (b, c2[1])] + _arc(c2, r2, 0, a2, 4) + _arc(c1, r1, a1 % 360, 180)
    top = [(x, -y) for x, y in reversed(bottom)]
    return [bottom + top]


def rhs_profile(h, b, t, ro=None, ri=None):
    """cold-formed RHS / SHS: outer and inner rounded rectangles (blocks: outer radius 3t, inner 2t), origin at the
    centre, h along y"""
    ro, ri = (3 * t if ro is None else ro), (2 * t if ri is None else ri)

    def rr(w, d, r):
        x, y = w / 2, d / 2
        return (_arc((x - r, -y + r), r, -90, 0, 4) + _arc((x - r, y - r), r, 0, 90, 4) +
                _arc((-x + r, y - r), r, 90, 180, 4) + _arc((-x + r, -y + r), r, 180, 270, 4))
    return [rr(b, h, ro), rr(b - 2 * t, h - 2 * t, ri)]


def chs_profile(D, t):
    return [_arc((0.0, 0.0), D / 2, 0, 360, 32)[:-1], _arc((0.0, 0.0), D / 2 - t, 0, 360, 32)[:-1]]


def l_profile(b, t, r1=None, r2=None):
    """equal angle with root radius r1 and toe radii r2 (office block L100X100X10: r1 10, r2 7): closed outline,
    heel at the origin, one leg along +x (its top face on y = 0) and one along -y (its outer face on x = 0)"""
    rr = RADII.get(f"L {b:g}x{b:g}x{t:g}", (t + 1.5, (t + 1.5) / 2))
    r1 = rr[0] if r1 is None else r1
    r2 = rr[1] if r2 is None else r2
    pts = [(0.0, 0.0), (b, 0.0)] + _arc((b - r2, -t + r2), r2, 0, -90, 4)
    pts += _arc((t + r1, -t - r1), r1, 90, 180, 6)
    pts += _arc((t - r2, -b + r2), r2, 0, -90, 4) + [(0.0, -b)]
    return [pts]


def plate_profile(w, h):
    return [[(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]]


def profile(spec):
    """outline loops of a member spec: ("H", h, b, tw, tf), ("C", h, b, tw, tf), ("RHS", h, b, t), ("CHS", D, t),
    ("PL", w, h) - or a Thai standard section name, "H 150x150x7x10", "LC 100x50x20x2.3" ... (TIS 1227 / 1228,
    drafter.tis_sections: the standard's radii and flange slopes; user 2026-10-18)"""
    if isinstance(spec, str):
        from .tis_sections import outline
        return outline(spec)
    k = spec[0]
    if k == "H":
        return h_profile(*spec[1:])
    if k == "C":
        return c_profile(*spec[1:])
    if k == "RHS":
        return rhs_profile(*spec[1:])
    if k == "CHS":
        return chs_profile(*spec[1:])
    if k == "L":
        return l_profile(*spec[1:])
    return plate_profile(*spec[1:])


def draw_profile(sp, P, loops, at=(0.0, 0.0), rot=0.0, mirror=False, sx=1.0, sy=1.0, layer="S-CUT",
                 inner_layer=None, cross=False, mirror_y=False):
    """draw outline loops (local mm) mirrored about x = 0 (mirror) or y = 0 (mirror_y), scaled (sy: a member cut
    obliquely), rotated 'rot' degrees and moved to 'at' (local mm of the view). Outline only, never filled.
    inner_layer: layer of the inner loops (a hollow section's inner wall, fine pen); cross: a cut hollow section
    gets the cross symbol, the two diagonals of its inner loop (user, review of A6). Returns the segments"""
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    segs = []
    for k, loop in enumerate(loops):
        q = []
        for x, y in loop:
            x = (-x if mirror else x) * sx
            y = (-y if mirror_y else y) * sy
            q.append((at[0] + x * ca - y * sa, at[1] + x * sa + y * ca))
        lay = layer if k == 0 or inner_layer is None else inner_layer
        pline(sp, [P(*p) for p in q], lay, close=True)
        segs += _segs(q, True)
        if cross and k == 1:
            xs, ys = [p[0] for p in q], [p[1] for p in q]
            x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
            line(sp, P(x0, y0), P(x1, y1), inner_layer or layer)
            line(sp, P(x0, y1), P(x1, y0), inner_layer or layer)
    return segs


# ------------------------------------------------------------------------------------------------ small geometry
def _unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L_ = math.hypot(dx, dy) or 1e-9
    return dx / L_, dy / L_, L_


def fillet_path(pts, r, n=10):
    """centre line of a bent member: the polyline pts with every inner corner rounded to radius r (bend radius on
    the centre line), n chords per bend. A corner whose legs are too short takes the largest radius that fits"""
    if len(pts) < 3 or r <= 0:
        return list(pts)
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        u1 = _unit(b, a)
        u2 = _unit(b, c)
        cosq = max(-1.0, min(1.0, u1[0] * u2[0] + u1[1] * u2[1]))
        q = math.acos(cosq)                                       # angle between the legs at b
        if q > math.pi - 1e-3 or q < 1e-3:
            out.append(b)
            continue
        t = r / math.tan(q / 2)
        lim = 0.45 * min(u1[2], u2[2])
        rr = r if t <= lim else lim * math.tan(q / 2)
        t = min(t, lim)
        p1 = (b[0] + u1[0] * t, b[1] + u1[1] * t)
        p2 = (b[0] + u2[0] * t, b[1] + u2[1] * t)
        bis = (u1[0] + u2[0], u1[1] + u2[1])
        bl = math.hypot(*bis)
        dcen = rr / math.sin(q / 2)
        cen = (b[0] + bis[0] / bl * dcen, b[1] + bis[1] / bl * dcen)
        a1 = math.atan2(p1[1] - cen[1], p1[0] - cen[0])
        a2 = math.atan2(p2[1] - cen[1], p2[0] - cen[0])
        da = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
        out += [(cen[0] + rr * math.cos(a1 + da * k / n), cen[1] + rr * math.sin(a1 + da * k / n)) for k in range(n + 1)]
    out.append(pts[-1])
    return out


def _offset(path, d):
    """polyline offset by d to the left (miter at the small kinks of a flattened arc)"""
    out = []
    for i, p in enumerate(path):
        if i == 0:
            ux, uy, _ = _unit(path[0], path[1])
            nx, ny = -uy, ux
        elif i == len(path) - 1:
            ux, uy, _ = _unit(path[-2], path[-1])
            nx, ny = -uy, ux
        else:
            a = _unit(path[i - 1], p)
            b = _unit(p, path[i + 1])
            n1, n2 = (-a[1], a[0]), (-b[1], b[0])
            nx, ny = n1[0] + n2[0], n1[1] + n2[1]
            k = nx * n1[0] + ny * n1[1] or 1e-9
            nx, ny = nx / k, ny / k
        out.append((p[0] + nx * d, p[1] + ny * d))
    return out


def _segs(pts, close=False):
    s = list(zip(pts, pts[1:]))
    if close:
        s.append((pts[-1], pts[0]))
    return s


# ------------------------------------------------------------------------------------------------ symbols
def wp_point(sp, P, c, S, label="WP", at=135.0, dist=2.4):
    """work point (setting-out point at the nosing line / floor intersection): a circle 2.6 mm with two opposite
    quarters filled, its label 'dist' mm (paper) from the centre at angle 'at' (deg), in clear space. Stronger than
    steel.wp_mark, which stays for trusses"""
    r = 1.3 * S
    x, y = P(*c)
    sp.add_circle((x, y), r, dxfattribs=A("S-SYMB"))
    for a0 in (90.0, 270.0):
        pts = [(x, y)] + [(x + r * math.cos(math.radians(a0 + 90 * k / 8)), y + r * math.sin(math.radians(a0 + 90 * k / 8)))
                          for k in range(9)]
        hatch(sp, pts, "SOLID", 1.0, "S-SYMB")
    if label:
        a = math.radians(at)
        text(sp, label, (x + dist * S * math.cos(a), y + dist * S * math.sin(a)), 1.8 * S, "S-TEXT", TA.MIDDLE_CENTER)
    return [((c[0] - r, c[1]), (c[0] + r, c[1])), ((c[0], c[1] - r), (c[0], c[1] + r))]


def call_box(sp, P, x0, y0, x1, y1, S, r=None):
    """detail boundary on a general view: a dashed rectangle with round corners (S-CALL) round the joint shown
    enlarged elsewhere - it fits a joint better than a circle. Returns the box (x0, y0, x1, y1) for ref_bubble"""
    r = r if r is not None else min(3.0 * S, 0.3 * min(x1 - x0, y1 - y0))
    b = math.tan(math.radians(90) / 4)
    pts = [(x0 + r, y0, 0), (x1 - r, y0, b), (x1, y0 + r, 0), (x1, y1 - r, b), (x1 - r, y1, 0), (x0 + r, y1, b),
           (x0, y1 - r, 0), (x0, y0 + r, b)]
    sp.add_lwpolyline([(*P(px, py), 0, 0, bb) for px, py, bb in pts], format="xyseb", close=True,
                      dxfattribs=A("S-CALL"))
    return (x0, y0, x1, y1)


def round_box_point(c, box, rc):
    """the point of a rounded rectangle (x0, y0, x1, y1, corner radius rc) nearest to c, c outside it: on a corner
    arc where c lies off a corner, so a leader always ends on the drawn outline"""
    bx0, by0, bx1, by1 = box[:4]
    q = (min(max(c[0], bx0 + rc), bx1 - rc), min(max(c[1], by0 + rc), by1 - rc))
    ux, uy, L_ = _unit(q, c)
    return (q[0] + ux * rc, q[1] + uy * rc)


def ref_bubble(sp, P, c, top, bottom, S, box=None, rc=None):
    """detail reference: a split bubble "n / sheet" (r 4 mm) at c with a thin leader to the nearest point of the
    detail boundary 'box' (call_box; rc its corner radius, call_box's default when None). The leader ends on the
    drawn outline, on the corner arc where the bubble is off a corner (user, 2026-10-16, RPM review of R2: "line not
    touch call out"). Returns the bubble's obstacle segments"""
    r = 4.0 * S
    x, y = P(*c)
    sp.add_circle((x, y), r, dxfattribs=A("S-SYMB"))
    line(sp, (x - r, y), (x + r, y), "S-SYMB")
    text(sp, top, (x, y + r * 0.45), 2.5 * S, "S-TEXT", TA.MIDDLE_CENTER, style="ANB")
    text(sp, bottom, (x, y - r * 0.45), 2.0 * S, "S-TEXT", TA.MIDDLE_CENTER)
    if box is not None:
        bx0, by0, bx1, by1 = box[:4]
        if bx0 < c[0] < bx1 and by0 < c[1] < by1:
            ex, ey = (bx0 if c[0] - bx0 < bx1 - c[0] else bx1), c[1]
        else:
            rc = rc if rc is not None else min(3.0 * S, 0.3 * min(bx1 - bx0, by1 - by0))
            ex, ey = round_box_point(c, box, rc)
        ux, uy, L_ = _unit(c, (ex, ey))
        if L_ > r:
            line(sp, P(c[0] + ux * r, c[1] + uy * r), P(ex, ey), "S-ANNO")
    return [((c[0] - r, c[1] - r), (c[0] + r, c[1] + r)), ((c[0] - r, c[1] + r), (c[0] + r, c[1] - r))]


def member_break(sp, P, a, b, S, over=1.5):
    """break line square across a member that is cut off in the view: a - b are the two edges of the member at the
    cut; the Z break line runs 'over' mm (paper) past each edge (EIT break, S-BREAK)"""
    ux, uy, L_ = _unit(a, b)
    e = over * S
    zbreak(sp, P(a[0] - ux * e, a[1] - uy * e), P(b[0] + ux * e, b[1] + uy * e), S)


def bolt_along(sp, P, a, b, d, S, layer="S-BOLT", nut_layer=None, washers=(True, True), proj=None):
    """a bolt seen side-on with its axis a -> b (local mm): a = face under the nut, b = face under the head. The
    shank is hidden inside the grip; head 0.65 d and nut 0.85 d high, 1.7 d across; washers 0.15 d x 2 d; the
    thread end 'proj' (default 0.4 d) past the nut; centre line. nut_layer: draw the nut end hidden (S-STL-HIDN) when
    it lies inside a closed member (blind nut)"""
    ux, uy, L_ = _unit(a, b)
    nx, ny = -uy, ux
    proj = 0.4 * d if proj is None else proj
    nut_layer = nut_layer or layer

    def rect(p, along, across, lay):
        q = [(p[0] + nx * across / 2, p[1] + ny * across / 2),
             (p[0] + ux * along + nx * across / 2, p[1] + uy * along + ny * across / 2),
             (p[0] + ux * along - nx * across / 2, p[1] + uy * along - ny * across / 2),
             (p[0] - nx * across / 2, p[1] - ny * across / 2)]
        pline(sp, [P(*x) for x in q], lay, close=True)

    for s in (d / 2, -d / 2):
        line(sp, P(a[0] + nx * s, a[1] + ny * s), P(b[0] + nx * s, b[1] + ny * s), _HID_LAYER)
    wh = 0.15 * d
    hb = b
    if washers[1]:
        rect(b, wh, 2.0 * d, layer)
        hb = (b[0] + ux * wh, b[1] + uy * wh)
    rect(hb, 0.65 * d, 1.7 * d, layer)
    na = a
    if washers[0]:
        rect(a, -wh, 2.0 * d, nut_layer)
        na = (a[0] - ux * wh, a[1] - uy * wh)
    rect(na, -0.85 * d, 1.7 * d, nut_layer)
    e = (na[0] - ux * (0.85 * d + proj), na[1] - uy * (0.85 * d + proj))
    for s in (d / 2, -d / 2):
        line(sp, P(na[0] - ux * 0.85 * d + nx * s, na[1] - uy * 0.85 * d + ny * s), P(e[0] + nx * s, e[1] + ny * s),
             nut_layer)
    line(sp, P(e[0] + nx * d / 2, e[1] + ny * d / 2), P(e[0] - nx * d / 2, e[1] - ny * d / 2), nut_layer)
    c0 = (e[0] - ux * 1.5 * S, e[1] - uy * 1.5 * S)
    c1 = (hb[0] + ux * (0.65 * d + 1.5 * S), hb[1] + uy * (0.65 * d + 1.5 * S))
    line(sp, P(*c0), P(*c1), "S-CENT")


def anchor_in_concrete(sp, P, top, hef, d, S, axis=(0.0, -1.0), hole=None, plate_t=0.0, nuts=1):
    """post-installed (chemical) anchor as built, steel S8.4: axis from the concrete face 'top' into the concrete
    (unit 'axis'); the drilled hole (Ø hole, default d + 2) hef + 10 deep with its resin (ANSI31 fine), the rod to
    hef, and above the face, through a plate plate_t thick, washer and 'nuts' nuts (2 = double nuts)"""
    ux, uy = axis
    nx, ny = -uy, ux
    hole = d + 2.0 if hole is None else hole
    dep = hef + 10.0
    q = [(top[0] + nx * hole / 2, top[1] + ny * hole / 2), (top[0] + ux * dep + nx * hole / 2, top[1] + uy * dep + ny * hole / 2),
         (top[0] + ux * dep - nx * hole / 2, top[1] + uy * dep - ny * hole / 2), (top[0] - nx * hole / 2, top[1] - ny * hole / 2)]
    hatch(sp, [P(*x) for x in q], "ANSI31", pscale("ANSI31", S, 0.6), "S-HATCH")
    pline(sp, [P(*x) for x in q], "S-CONC-VIS")
    up = plate_t + 0.15 * d + nuts * 0.85 * d + 0.4 * d       # rod projection above the concrete face
    a = (top[0] - ux * up, top[1] - uy * up)
    b = (top[0] + ux * hef, top[1] + uy * hef)
    for s in (d / 2, -d / 2):
        line(sp, P(a[0] + nx * s, a[1] + ny * s), P(b[0] + nx * s, b[1] + ny * s), "S-BOLT")
    line(sp, P(b[0] + nx * d / 2, b[1] + ny * d / 2), P(b[0] - nx * d / 2, b[1] - ny * d / 2), "S-BOLT")
    line(sp, P(a[0] + nx * d / 2, a[1] + ny * d / 2), P(a[0] - nx * d / 2, a[1] - ny * d / 2), "S-BOLT")
    p = (top[0] - ux * plate_t, top[1] - uy * plate_t)
    for h, w in [(0.15 * d, 2.0 * d)] + [(0.85 * d, 1.7 * d)] * nuts:
        r = [(p[0] + nx * w / 2, p[1] + ny * w / 2), (p[0] - ux * h + nx * w / 2, p[1] - uy * h + ny * w / 2),
             (p[0] - ux * h - nx * w / 2, p[1] - uy * h - ny * w / 2), (p[0] - nx * w / 2, p[1] - ny * w / 2)]
        pline(sp, [P(*x) for x in r], "S-BOLT", close=True)
        p = (p[0] - ux * h, p[1] - uy * h)
    line(sp, P(a[0] - ux * 1.5 * S, a[1] - uy * 1.5 * S), P(b[0] + ux * 1.5 * S, b[1] + uy * 1.5 * S), "S-CENT")


# ------------------------------------------------------------------------------------------------ tubes and rails
def tube_run(sp, P, pts, D, S, r=None, layer="S-STL-VIS", cl=None, cap=(True, True)):
    """a round tube (handrail, guard rail, ladder hoop) seen side-on along the polyline of centre points 'pts':
    both edges D apart, every corner bent on a centre-line radius r (default 2.5 D), the centre line (S-CENT) when
    the tube is 2 mm or more on paper (cl=None: automatic), the ends closed square. Returns the edge segments"""
    r = 2.5 * D if r is None else r
    c = fillet_path(pts, r)
    e1, e2 = _offset(c, D / 2), _offset(c, -D / 2)
    pline(sp, [P(*q) for q in e1], layer)
    pline(sp, [P(*q) for q in e2], layer)
    if cap[0]:
        line(sp, P(*e1[0]), P(*e2[0]), layer)
    if cap[1]:
        line(sp, P(*e1[-1]), P(*e2[-1]), layer)
    if cl or (cl is None and D / S >= 2.0):
        pline(sp, [P(*q) for q in c], "S-CENT")
    return _segs(e1) + _segs(e2)


def tube_end_section(sp, P, c, D, t, S, layer="S-CUT"):
    """a round tube cut square (rail seen end-on in a section): outer and inner circle, no fill (steel S4.15)"""
    sp.add_circle(P(*c), D / 2, dxfattribs=A(layer))
    sp.add_circle(P(*c), D / 2 - t, dxfattribs=A(layer))
    return [((c[0] - D / 2, c[1]), (c[0] + D / 2, c[1]))]


def post_side(sp, P, base, top, w, S, layer="S-STL-VIS", cl=None):
    """a guard post (RHS or CHS w wide) seen side-on from base to top centre points, with its centre line when it
    reads (w >= 2 mm on paper)"""
    ux, uy, L_ = _unit(base, top)
    nx, ny = -uy * w / 2, ux * w / 2
    pts = [(base[0] + nx, base[1] + ny), (top[0] + nx, top[1] + ny), (top[0] - nx, top[1] - ny),
           (base[0] - nx, base[1] - ny)]
    pline(sp, [P(*q) for q in pts], layer, close=True)
    if cl or (cl is None and w / S >= 2.0):
        line(sp, P(base[0] - ux * 2 * S, base[1] - uy * 2 * S), P(top[0] + ux * 2 * S, top[1] + uy * 2 * S), "S-CENT")
    return _segs(pts, True)


# ------------------------------------------------------------------------------------------------ stairs
def stringer_side(sp, P, top_a, top_b, depth, S, layer="S-STL", toe=None, ends=("v", "v"), zfloor=None,
                  open_ends=(False, False)):
    """a sloping stringer seen side-on: top edge top_a -> top_b (local mm, top_a the lower end), depth measured
    square to the member. toe = flange thickness of a channel (PFC) seen from its back: the flange lines toe mm
    inside both edges (fine, S-STL-VIS). ends: "v" vertical cut, "h" horizontal cut at zfloor (a foot on the floor),
    "n" square to the member. open_ends: an end broken off is closed by its break line only, never by a member line
    (user, review of A6: "proper break line no member line here"). Returns the outline (local mm, closed)"""
    ux, uy, L_ = _unit(top_a, top_b)
    nx, ny = uy, -ux                                    # toward the underside
    bot_a = (top_a[0] + nx * depth, top_a[1] + ny * depth)
    bot_b = (top_b[0] + nx * depth, top_b[1] + ny * depth)

    def cut(p_top, p_bot, kind, sign):
        if kind == "n":
            return p_top, p_bot
        if kind == "v":                                 # vertical through the top-edge point
            k = (p_top[0] - p_bot[0]) / ux if abs(ux) > 1e-9 else 0.0
            return p_top, (p_bot[0] + ux * k, p_bot[1] + uy * k)
        z = zfloor                                       # horizontal at the floor
        kt = (z - p_top[1]) / uy
        kb = (z - p_bot[1]) / uy
        return (p_top[0] + ux * kt, z), (p_bot[0] + ux * kb, z)

    ta, ba = cut(top_a, bot_a, ends[0], -1)
    tb, bb = cut(top_b, bot_b, ends[1], 1)
    out = [ta, tb, bb, ba]
    line(sp, P(*ta), P(*tb), layer)
    line(sp, P(*bb), P(*ba), layer)
    if not open_ends[1]:
        line(sp, P(*tb), P(*bb), layer)
    if not open_ends[0]:
        line(sp, P(*ba), P(*ta), layer)
    if toe:
        for d in (toe, depth - toe):
            p = (top_a[0] + nx * d, top_a[1] + ny * d)
            q = (top_b[0] + nx * d, top_b[1] + ny * d)
            line(sp, P(*p), P(*q), "S-STL-VIS")
    return out


def level_across(sp, P, u0, u, z, value, desc, S, ext=(-4, 24)):
    """level mark on a steel section, elevation or detail (SYMBOLS "Level mark"): the level line in the grid linetype,
    grey (S-GRID), run across the view from u0 (the far edge of the object) to the mark at u and ext[1] mm (paper)
    past it; the open triangle (apex on the line) and the value as td.level() (user, 2026-10-06, BANWA2: "colour 8
    grid linetype"; 2026-10-16, RPM review of R2: "add level line extent across object grid line type and color
    no. 8, put this as a rule apply to every section detail that present level"). u0 may be a pair (u_from, u_to)
    when the mark stands inside the view: the line spans both. Returns the line's segment"""
    x, y = P(u, z)
    us = list(u0) if isinstance(u0, (tuple, list)) else [u0]
    xs = [P(v, z)[0] for v in us] + [x + ext[0] * S, x + ext[1] * S]
    line(sp, (min(xs), y), (max(xs), y), "S-GRID")
    pline(sp, [(x, y), (x - 1.2 * S, y + 2.0 * S), (x + 1.2 * S, y + 2.0 * S)], "S-ANNO", close=True)
    text(sp, f"{value}  {desc}" if desc else value, (x + 2.0 * S, y + 0.6 * S), 2.0 * S, "S-TEXT")
    return [((min(us + [u]), z), (max(us + [u]), z))]


def nosing_line(sp, P, a, b, S, label="NOSING LINE", at=0.55):
    """the nosing line of a flight (chain, S-GRID) with its label above the line at fraction 'at'"""
    ux, uy, L_ = _unit(a, b)
    e = 3 * S
    line(sp, P(a[0] - ux * e, a[1] - uy * e), P(b[0] + ux * e, b[1] + uy * e), "S-GRID")
    if label:
        m = (a[0] + (b[0] - a[0]) * at - uy * 1.6 * S, a[1] + (b[1] - a[1]) * at + ux * 1.6 * S)
        text(sp, label, P(*m), 1.8 * S, "S-TEXT", TA.BOTTOM_CENTER, rot=math.degrees(math.atan2(uy, ux)))
    return [(a, b)]


def treads_behind(sp, P, nosings, going, h, S, t=0.0, layer=_HID_LAYER, back_up=0.0):
    """treads seen through the near stringer (hidden, steel S4.11): for every nosing point (u, z) a rectangle
    'going' long (toward +u) and h deep under the walking surface, with the plate line t below the top when t > 0.
    back_up = kick of a back upstand. Returns nothing (hidden lines are not obstacles)"""
    for (u, z) in nosings:
        pts = [(u, z), (u + going, z), (u + going, z - h), (u, z - h)]
        pline(sp, [P(*q) for q in pts], layer, close=True)
        if t > 0:
            line(sp, P(u, z - t), P(u + going, z - t), layer)
        if back_up > 0:
            line(sp, P(u + going, z), P(u + going, z + back_up), layer)


def treads_cut(sp, P, nosings, going, S, plate_t, frame=None, frame_t=3.2, layer="S-CUT"):
    """treads cut along the flight (section between the stringers), actual sections in outline (steel S4.15): the
    plate going x plate_t under each nosing (fine pen when under 1 mm on paper), and the front and back frame tubes
    (frame = (b, h), wall frame_t) with the cross symbol and the inner wall in the fine pen"""
    out = []
    for (u, z) in nosings:
        pts = [(u, z - plate_t), (u + going, z - plate_t), (u + going, z), (u, z)]
        pline(sp, [P(*q) for q in pts], "S-CUT-FINE" if plate_t / S < 1.0 else layer, close=True)
        out += _segs(pts, True)
        if frame:
            b, h = frame
            for u0 in (u, u + going - b):
                out += draw_profile(sp, P, rhs_profile(h, b, frame_t), (u0 + b / 2, z - plate_t - h / 2), layer=layer,
                                    inner_layer="S-CUT-FINE", cross=True)
    return out


def flight_dims(sp, P, low, n, rise, going, S, u_dim, z_dim, risers_side="R"):
    """the dimension pair every flight carries (steel S4.14): risers "n R @ rise = total" on a vertical line at
    u_dim (from the lower floor at low[1] to the upper landing), goings "(n - 1) G @ going = total" on a horizontal
    line at z_dim from the first riser to the last (low = (u, z) of the lower floor at the first riser face)"""
    u0, z0 = low
    dim(sp, P(u_dim, z0), P(u_dim, z0 + n * rise), P(u_dim + (4 if risers_side == "R" else -4) * S, z0), S,
        angle=90, text=f"{n} R @ {rise:.0f} = <>")
    if n > 1:
        dim(sp, P(u0, z0), P(u0 + (n - 1) * going, z0), P(u0, z_dim), S, text=f"{n - 1} G @ {going:.0f} = <>")


# ------------------------------------------------------------------------------------------------ fixed ladders
def ladder_front(sp, P, z0, z1, B, S, pitch, stile=(65.0, 12.0), rung_d=20.0, ext=1100.0, first=None,
                 flare=None, layer="S-STL", break_at=None):
    """fixed ladder seen from the front (climbing side): stiles stile[0] deep x stile[1] thick, clear width B
    between the stiles, rungs Ø rung_d at 'pitch' from the first rung 'first' above z0 (default = pitch) up to the
    arrival level z1, stiles extended 'ext' above z1; flare = (gap, rise) widens the stile extension to 'gap' clear
    over 'rise' (walk-through). break_at = (za, zb): the run between is broken out (long ladders). Returns rung levels"""
    first = pitch if first is None else first
    t = stile[1]
    xs = (-B / 2 - t, B / 2)                             # stile left edges
    rungs = []
    z = z0 + first
    while z <= z1 + 1e-6:
        rungs.append(z)
        z += pitch
    top = z1 + ext

    def stile_line(x, za, zb):
        line(sp, P(x, za), P(x, zb), layer)

    segs = [(z0, top)] if not break_at else [(z0, break_at[0]), (break_at[1], top)]
    for (za, zb) in segs:
        for x0 in xs:
            for x in (x0, x0 + t):
                if flare and zb == top:
                    g, rr = flare
                    k = (g - B) / 2 * (1 if x0 > 0 else -1)
                    zf = z1 + 150.0
                    line(sp, P(x, za), P(x, zf), layer)
                    line(sp, P(x, zf), P(x + k, zf + rr), layer)
                    line(sp, P(x + k, zf + rr), P(x + k, zb), layer)
                else:
                    stile_line(x, za, zb)
            if za == z0:
                line(sp, P(x0, za), P(x0 + t, za), layer)
            if zb == top:
                xx = x0 + ((flare[0] - B) / 2 * (1 if x0 > 0 else -1) if flare else 0.0)
                line(sp, P(xx, zb), P(xx + t, zb), layer)
        if break_at and za == z0:
            member_break(sp, P, (xs[0] - 10, zb), (xs[1] + t + 10, zb), S, over=0.5)
        if break_at and zb == top:
            member_break(sp, P, (xs[0] - 10, za), (xs[1] + t + 10, za), S, over=0.5)
    for z in rungs:
        if break_at and break_at[0] < z < break_at[1]:
            continue
        for d in (rung_d / 2, -rung_d / 2):
            line(sp, P(-B / 2, z + d), P(B / 2, z + d), "S-STL-VIS")
    return rungs


def ladder_side(sp, P, z0, z1, S, rungs, stile=(65.0, 12.0), rung_d=20.0, ext=1100.0, wall_u=None, layer="S-STL",
                goose=None, break_at=None):
    """fixed ladder seen from the side: the stile band stile[0] deep (u = 0 at the climbing face, +u toward the
    wall), every rung as a circle on the stile centre line, the stile extension 'ext' above z1 and, with
    goose = (reach, r), a stile turned over to the landing (gooseneck): up to z1 + ext, then across 'reach' toward
    -u, down to z1. Returns the stile outline segments"""
    d = stile[0]
    top = z1 + ext
    out = []
    spans = [(z0, top)] if not break_at else [(z0, break_at[0]), (break_at[1], top)]
    for za, zb in spans:
        if goose and zb == top:
            reach, rg = goose
            cpath = [(d / 2, za), (d / 2, top - d / 2), (d / 2 - reach, top - d / 2), (d / 2 - reach, z1)]
            c = fillet_path(cpath, rg)
            e1, e2 = _offset(c, d / 2), _offset(c, -d / 2)
            pline(sp, [P(*q) for q in e1], layer)
            pline(sp, [P(*q) for q in e2], layer)
            line(sp, P(*e1[-1]), P(*e2[-1]), layer)
            out += _segs(e1) + _segs(e2)
        else:
            pts = [(0, za), (d, za), (d, zb), (0, zb)]
            pline(sp, [P(*q) for q in pts], layer, close=True)
            out += _segs(pts, True)
        if break_at and za == z0:
            member_break(sp, P, (-10, zb), (d + 10, zb), S, over=0.5)
        if break_at and zb == top:
            member_break(sp, P, (-10, za), (d + 10, za), S, over=0.5)
    for z in rungs:
        if break_at and break_at[0] < z < break_at[1]:
            continue
        sp.add_circle(P(d / 2, z), rung_d / 2, dxfattribs=A("S-STL"))
    return out


def cage_plan(sp, P, B, S, depth=750.0, hoop=(50.0, 6.0), vert=(25.0, 6.0), n_vert=7, stile=(65.0, 12.0),
              rung_d=20.0, layer="S-STL"):
    """section through a ladder cage looking down (plan): the rung and both stiles cut, the hoop (flat bar seen
    from above as a band hoop[1] thick) from stile to stile round a semicircle of inner depth 'depth' measured from
    the rung centre, n_vert vertical flats cut (outline, S4.15) on the inside of the hoop at equal spacing. Origin = rung
    centre; +y away from the wall (toward the climber). Returns the hoop's inner radius and the vertical positions"""
    t = stile[1]
    for sx in (-1, 1):
        x0 = sx * (B / 2) + (0 if sx > 0 else -t)
        pts = [(x0, -stile[0] / 2), (x0 + t, -stile[0] / 2), (x0 + t, stile[0] / 2), (x0, stile[0] / 2)]
        pline(sp, [P(*q) for q in pts], "S-CUT", close=True)
    line(sp, P(-B / 2, rung_d / 2), P(B / 2, rung_d / 2), "S-STL-VIS")
    line(sp, P(-B / 2, -rung_d / 2), P(B / 2, -rung_d / 2), "S-STL-VIS")
    R = B / 2 + t + hoop[1]                              # hoop inner radius: lapped on the stiles' outer faces
    yc = depth - R                                       # semicircle centre so the inner depth is 'depth'
    for rr in (R, R + hoop[1]):
        path = [(-rr, 0.0), (-rr, yc)] + [(-rr * math.cos(math.pi * k / 24), yc + rr * math.sin(math.pi * k / 24))
                                         for k in range(1, 24)] + [(rr, yc), (rr, 0.0)]
        pline(sp, [P(*q) for q in path], layer)
    vs = []
    L_arc = math.pi * R + 2 * yc
    for k in range(n_vert):
        s = L_arc * (k + 0.5) / n_vert
        if s < yc:
            p, n_ = (-R, s), (1.0, 0.0)
        elif s > yc + math.pi * R:
            p, n_ = (R, yc - (s - yc - math.pi * R)), (-1.0, 0.0)
        else:
            a = math.pi - (s - yc) / R
            p, n_ = (R * math.cos(a), yc + R * math.sin(a)), (-math.cos(a), -math.sin(a))
        tx, ty = -n_[1], n_[0]
        w, th = vert
        q = [(p[0] + tx * w / 2, p[1] + ty * w / 2), (p[0] - tx * w / 2, p[1] - ty * w / 2),
             (p[0] - tx * w / 2 + n_[0] * th, p[1] - ty * w / 2 + n_[1] * th),
             (p[0] + tx * w / 2 + n_[0] * th, p[1] + ty * w / 2 + n_[1] * th)]
        pline(sp, [P(*x) for x in q], "S-CUT", close=True)
        vs.append(p)
    return R, vs
