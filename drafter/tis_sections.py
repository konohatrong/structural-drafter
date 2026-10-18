"""
Thai standard steel sections - the catalogue of TIS 1227-2537 (hot-rolled; amended 2539 / 2558: grades and testing
only) and TIS 1228-2561 (cold-formed, Annex A recommended sizes), with each section's true outline for drawings
(user, 2026-10-18: "make structural steel section from these document when we show in drawing we show exact geometry of
structural steel section not just rectangular"; steel S4.15).

Data: drafter/data/tis_steel_sections.json - dimensions, radii, area and mass per section with the table and page it
comes from (a digest of the dimension tables; the standards themselves stay outside the repository).

Names (as written on drawings):
    H 150x150x7x10        rolled H (H x B x t1 x t2), root radius r              TIS 1227 Table 5
    I 200x100x7x10        rolled I, flanges sloped 8 deg (t2 at (B - t1) / 4 from the toe), r1 root, r2 toe   Table 6
    C 150x75x6.5x10       rolled channel, flanges sloped 5 deg (t2 at (B - t1) / 2), r1, r2                   Table 4
    L 65x65x6, L 100x75x7 rolled angle, r1 root, r2 toe                                                    Tables 2, 3
    LC 100x50x20x2.3      cold-formed lipped channel (H x A x C x t)                       TIS 1228 Table A.3
    CC 100x50x50x3.2      cold-formed plain channel (H x A x B x t)                                   Table A.2
    Z 100x50x50x3.2, LZ 100x50x20x2.3, HAT 60x30x25x2.3, CL 50x50x3.2 (cold-formed angle)     Tables A.4, A.5, A.6, A.1
Cold-formed bends: the inner radius is not tabulated; RI_T x t (default 1.0 t) reproduces the tabulated areas
(tests/test_tis_sections.py checks every section's outline area against its table).

    from drafter.tis_sections import section, outline
    outline("H 150x150x7x10")      # closed loops (mm), origin at the centroid of the bounding box
"""
import json
import math
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data" / "tis_steel_sections.json"
SLOPE_C = math.tan(math.radians(5.0))                                 # channel inner flange faces (TIS 1227 Table 4)
SLOPE_I = math.tan(math.radians(8.0))                                 # I-section inner flange faces (Table 6, 98 deg)
RI_T = 1.0                                                            # cold-formed inner bend radius / t (area fit)
_CAT = None


def catalogue():
    global _CAT
    if _CAT is None:
        _CAT = {s["name"]: s for s in json.loads(DATA.read_text(encoding="utf-8"))}
    return _CAT


def section(name):
    """the catalogue entry of a section name ('H 150x150x7x10'); KeyError with the nearest names if unknown"""
    cat = catalogue()
    key = " ".join(name.replace("X", "x").split())
    if key in cat:
        return cat[key]
    pre = key.split()[0]
    near = [n for n in cat if n.startswith(pre + " ") and n.split()[1].split("x")[:2] == key.split()[1].split("x")[:2]]
    raise KeyError(f"{name}: not in TIS 1227 / 1228" + (f" - nearest: {', '.join(near[:6])}" if near else ""))


def _arc(c, r, a0, a1, n=8):
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
             c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def _fillet(p_prev, p, p_next, r, n=6):
    """round the corner p of a polyline with radius r (tangent arc), as points"""
    if r <= 0:
        return [p]
    ax, ay = p_prev[0] - p[0], p_prev[1] - p[1]
    bx, by = p_next[0] - p[0], p_next[1] - p[1]
    la, lb = math.hypot(ax, ay), math.hypot(bx, by)
    ax, ay, bx, by = ax / la, ay / la, bx / lb, by / lb
    cosang = max(-1.0, min(1.0, ax * bx + ay * by))
    ang = math.acos(cosang)
    if ang < 1e-6 or abs(ang - math.pi) < 1e-6:
        return [p]
    d = r / math.tan(ang / 2)
    t1 = (p[0] + ax * d, p[1] + ay * d)
    t2 = (p[0] + bx * d, p[1] + by * d)
    bis = (ax + bx, ay + by)
    lb_ = math.hypot(*bis)
    c = (p[0] + bis[0] / lb_ * r / math.sin(ang / 2), p[1] + bis[1] / lb_ * r / math.sin(ang / 2))
    a0 = math.atan2(t1[1] - c[1], t1[0] - c[0])
    a1 = math.atan2(t2[1] - c[1], t2[0] - c[0])
    da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    return [(c[0] + r * math.cos(a0 + da * k / n), c[1] + r * math.sin(a0 + da * k / n)) for k in range(n + 1)]


def _round(pts, radii):
    """closed polygon pts with a radius per vertex (0 = sharp)"""
    out = []
    n = len(pts)
    for i in range(n):
        out += _fillet(pts[i - 1], pts[i], pts[(i + 1) % n], radii[i])
    return out


def _h(h, b, t1, t2, r):
    x, y, w, f = b / 2, h / 2, t1 / 2, h / 2 - t2
    pts = [(-x, -y), (x, -y), (x, -f), (w, -f), (w, f), (x, f), (x, y), (-x, y), (-x, f), (-w, f), (-w, -f), (-x, -f)]
    return [_round(pts, [0, 0, 0, r, r, 0, 0, 0, 0, r, r, 0])]


def _i(h, b, t1, t2, r1, r2):
    o = (b - t1) / 2                                                  # flange outstand
    y_toe = t2 - SLOPE_I * (o / 2)                                    # t2 at (B - t1) / 4, mid-outstand (Table 6 figure)
    y_web = y_toe + SLOPE_I * o
    x, y, w = b / 2, h / 2, t1 / 2
    pts = [(-x, -y), (x, -y), (x, -y + y_toe), (w, -y + y_web), (w, y - y_web), (x, y - y_toe), (x, y), (-x, y),
           (-x, y - y_toe), (-w, y - y_web), (-w, -y + y_web), (-x, -y + y_toe)]
    return [_round(pts, [0, 0, r2, r1, r1, r2, 0, 0, r2, r1, r1, r2])]


def _c(h, b, t1, t2, r1, r2):
    """rolled channel, back of the web on x = 0, flanges toward +x; t2 at (B - t1) / 2 from the toe"""
    o = b - t1
    y_toe = t2 - SLOPE_C * (o / 2)
    y_web = y_toe + SLOPE_C * o
    y = h / 2
    pts = [(0, -y), (b, -y), (b, -y + y_toe), (t1, -y + y_web), (t1, y - y_web), (b, y - y_toe), (b, y), (0, y)]
    return [[(px - b / 2, py) for px, py in _round(pts, [0, 0, r2, r1, r1, r2, 0, 0])]]


def _l(a, b, t, r1, r2):
    """rolled angle, heel at (0, 0), legs along +x (length b) and +y (length a)"""
    pts = [(0, 0), (b, 0), (b, t), (t, t), (t, a), (0, a)]
    return [_round(pts, [0, 0, r2, r1, r2, 0])]


def _bent(path, t, ri):
    """a cold-formed section: centre-line path (open), thickness t, inner bend radius ri at every corner -> closed
    outline (the path offset by +-t/2, corners rounded ri / ri + t)"""
    rm = ri + t / 2
    cl = [path[0]]
    for i in range(1, len(path) - 1):
        cl += _fillet(path[i - 1], path[i], path[i + 1], rm, 8)
    cl.append(path[-1])

    def offset(pts, d):
        out = []
        for i, p in enumerate(pts):
            a = pts[max(i - 1, 0)]
            b_ = pts[min(i + 1, len(pts) - 1)]
            dx, dy = b_[0] - a[0], b_[1] - a[1]
            L = math.hypot(dx, dy) or 1.0
            out.append((p[0] - dy / L * d, p[1] + dx / L * d))
        return out
    return [offset(cl, t / 2) + offset(cl, -t / 2)[::-1]]


def _cf(kind, d, t):
    ri = RI_T * t
    h = d[0]
    if kind == "LC":                                                  # H x A x C: web on x = 0, flanges to +x, lips in
        _, a, c = d
        p = [(a - t / 2, h / 2 - c), (a - t / 2, h / 2 - t / 2), (t / 2, h / 2 - t / 2), (t / 2, -h / 2 + t / 2),
             (a - t / 2, -h / 2 + t / 2), (a - t / 2, -h / 2 + c)]
    elif kind == "CC":                                                # H x A x B
        _, a, b = d
        p = [(a, h / 2 - t / 2), (t / 2, h / 2 - t / 2), (t / 2, -h / 2 + t / 2), (b, -h / 2 + t / 2)]
    elif kind == "Z":                                                 # H x A x B: top flange to -x, bottom to +x
        _, a, b = d
        p = [(-a + t / 2, h / 2 - t / 2), (0, h / 2 - t / 2), (0, -h / 2 + t / 2), (b - t / 2, -h / 2 + t / 2)]
    elif kind == "LZ":                                                # H x A x C
        _, a, c = d
        p = [(-a + t / 2, h / 2 - c), (-a + t / 2, h / 2 - t / 2), (0, h / 2 - t / 2), (0, -h / 2 + t / 2),
             (a - t / 2, -h / 2 + t / 2), (a - t / 2, -h / 2 + c)]
    elif kind == "HAT":                                               # H x A x C: crown A, flanges C each side
        _, a, c = d
        x = a / 2 - t / 2
        p = [(-x - c - t / 2, -h / 2 + t / 2), (-x, -h / 2 + t / 2), (-x, h / 2 - t / 2), (x, h / 2 - t / 2),
             (x, -h / 2 + t / 2), (x + c + t / 2, -h / 2 + t / 2)]          # C from the web's outer face
    elif kind == "CL":                                                # A x B
        a, b = d[0], d[1]
        p = [(b, t / 2), (t / 2, t / 2), (t / 2, a)]
    else:
        raise KeyError(kind)
    return _bent(p, t, ri)


def outline(name):
    """closed outline loops (mm) of a TIS section, ready for steel_access.draw_profile"""
    s = section(name)
    k, d = s["kind"], s["dims"]
    if k == "H":
        return _h(*d, s["r"])
    if k == "I":
        return _i(*d, s["r1"], s["r2"])
    if k == "C":
        return _c(*d, s["r1"], s["r2"])
    if k == "L":
        return _l(*d, s["r1"], s["r2"])
    return _cf(k, d[:-1], d[-1])


def area(loops):
    """mm2 of the outline (shoelace)"""
    tot = 0.0
    for lp in loops[:1]:
        for (x0, y0), (x1, y1) in zip(lp, lp[1:] + lp[:1]):
            tot += x0 * y1 - x1 * y0
    return abs(tot) / 2
