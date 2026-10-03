"""
Project SRT (steel roof truss T1) on the general drafting engine (drafter/td_engine.py + drafter/steel.py):
project data, options, and the truss geometry taken from the design (calc_truss.py).

The general engine (drafter/td_engine.py) supplies the document, pens by colour, dimension styles, the annotation
engine (leaders packed in columns / rows), detail blocks captured in model space, model-space sheets with the A3
title block, tables and notes; drafter/steel.py the steel layers and helpers (welds, bolts, breaks, cutting planes,
callouts, tags). This module only sets what belongs to the project: data, options, the design, marks, and the
truss members drawn from the design geometry (chord, branch, branch weld zones).
Drawing rule: normal (2.0 / 2.8 text). Model space at real size (1 unit = 1 mm); each view is drawn at its own
scale S (1:10, 1:50 ...) and placed on its sheet by viewport(ps, key, S, ...).
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))                          # repository root: the drafter package
sys.path.insert(0, str(HERE))

from drafter import td_engine                                      # noqa: E402
from drafter.td_engine import *                                    # noqa: E402,F401,F403
import calc_truss as C                                             # noqa: E402

# --------------------------------------------------------------------------- project data
PROJ.update(code="SRT", project="STEEL ROOF TRUSS T1", location="[ BUILDING / LOCATION ]",
            owner="[ OWNER NAME ]", date="03/10/2026", stage="D", rev="A")
td_engine.REVS = [("A", "ISSUED FOR REVIEW", PROJ["date"])]
td_engine.KEYPLAN_2 = "(TRUSS T1)"
td_engine.LEADER_ORTH = True       # leaders: straight 0 / 90 / 180 / 270 deg or orthogonal L, never crossing
td_engine.WRAP_UNITS = True        # "60 mm" never splits across two lines
TABLES.clear()
TABLES.update({
    "DESIGN": (1, "DESIGN SUMMARY - TRUSS T1"),
    "MEMB": (2, "MEMBER SCHEDULE - ONE TRUSS"),
    "NODES": (3, "NODE GEOMETRY AND WELDS"),
    "CONN": (4, "SITE CONNECTIONS AND FIELD BOLTS - ONE TRUSS"),
    "PLATES": (5, "PLATES AND FITTINGS - ONE TRUSS"),
    "FLY": (6, "FLY BRACING SCHEDULE"),
})

from drafter.steel import *                                        # noqa: E402,F401,F403  steel layers + helpers

DS[200] = td_engine.dimstyle("EIT-200", 200)

# --------------------------------------------------------------------------- design data
def _design():
    """calc_truss.design(), cached in out/ while calc_truss.py is unchanged (the size search takes ~30 s)"""
    import hashlib
    import pickle
    key = hashlib.sha1((HERE / "calc_truss.py").read_bytes()).hexdigest()
    cache = HERE / "out" / f".design_{key[:12]}.pkl"
    if cache.exists():
        return pickle.loads(cache.read_bytes())
    d = C.design()
    cache.parent.mkdir(exist_ok=True)
    for old in cache.parent.glob(".design_*.pkl"):
        old.unlink()
    cache.write_bytes(pickle.dumps(d))
    return d


D = _design()
SEC = D["sec"]
DC, TC_T = SEC["TC"].D, SEC["TC"].t                                # chord: 165.2 x 7.1 (both chords)
L, H, NP, A_P = C.L, C.H, C.NP, C.A_P
NODES = D["nodes"]
ECC, GAPS, THETA = C.layout(SEC, NODES, D["mem"])                 # work-point offsets, gaps and angles as drawn
FACE = {"T": H - DC / 2, "B": DC / 2}                              # chord faces on the web side
X_OH = D["x_oh"]                   # chords run past the end node centre lines (K3.1A end distance), capped
CAP_T = 8.0                        # end cap plates
LOOSE = {f"D{p}" for p in C.SPLICE_PANELS}                          # site-bolted diagonals
X_SPLICE = [(p + 0.5) * A_P for p in C.SPLICE_PANELS]               # chord field splices, mid-panel
WEBS = C.web_list(D["mem"])
WELDS = D["welds"]                                                 # branch weld legs by zone (AWS Fig 9.10)
FL = D["splices"][("BC", C.SPLICE_PANELS[0])]["flange"]           # one flange plate for every chord splice


def wp(node):
    """work point of a node: on the chord axis offset by e away from the web (Table K3.2 eccentricity)"""
    x, y = NODES[node]
    e = ECC.get(node, 0.0)
    return (x, y + e) if node[0] == "T" else (x, y - e)


def axis(name):
    """work points at the two ends of a web member: (top, bottom)"""
    _, _, top, bot = web(name)
    return wp(top), wp(bot)


def web(name):
    return next(w for w in WEBS if w[0] == name)


def branch_lines(name):
    """outline lines of a web member between the chord faces, its axis on the faces, unit vector top -> bottom
    (calc_truss.outline: the same geometry the joint checks use)"""
    return C.outline(SEC, NODES, ECC, web(name))


def group_of(name):
    return C.group_of(D["mem"], name)


def theta_deg(name):
    return THETA[name]


def axis_length(name):
    _, a, _ = branch_lines(name)
    return math.hypot(a[1][0] - a[0][0], a[1][1] - a[0][1])


def node_gaps(node):
    return [g[0] for g in GAPS.get(node, [])]


def branches_at(node):
    return [w[0] for w in WEBS if node in (w[2], w[3])]


def node_type(node):
    """N1 ... N6 (TABLE 3): by side and the groups meeting there"""
    br = sorted(group_of(m) for m in branches_at(node))
    if node in ("B0", f"B{NP}"):
        return "N6"
    if br == ["VM"]:
        return "N5"
    if "VE" in br:
        return "N3"
    if len(br) == 3:
        return "N4"
    return "N1" if "DE" in br else "N2"


def _web_marks():
    """piece marks of the web members (DSC p.95 #24-25: pieces that differ in any way - section, length, end
    preparation - get different marks): V1, V2 ... and D1, D2 ... numbered from the pin end"""
    keys = {}
    for w in sorted(WEBS, key=lambda w: (min(NODES[w[2]][0], NODES[w[3]][0]), w[0])):
        n = w[0]
        k = (n[0], SEC[group_of(n)].name, round(axis_length(n)), n in LOOSE)
        keys.setdefault(k, []).append(n)
    out, count = {}, {"V": 0, "D": 0}
    for k, ns in keys.items():
        count[k[0]] += 1
        for n in ns:
            out[n] = f"{k[0]}{count[k[0]]}"
    return out


WEB_MARK = _web_marks()
# chord tubes: end pieces (SP1 / SP3, capped) and the middle piece (SP2), between the end cap and flange plates
CHORD_MARK = {"T": ("TC1", "TC2"), "B": ("BC1", "BC2")}
CHORD_LEN = (X_SPLICE[0] + X_OH - FL["tp"], X_SPLICE[1] - X_SPLICE[0] - 2 * FL["tp"])


def mark_of(name):
    return WEB_MARK[name]


def marks_at(node):
    return sorted({mark_of(b) for b in branches_at(node)})


NODE_TYPES = {
    "N1": "END-ZONE NODE", "N2": "MIDDLE NODE", "N3": "END TOP NODE", "N4": "CENTRE BOTTOM NODE",
    "N5": "CENTRE TOP NODE", "N6": "SUPPORT NODE (OVER THE BEARING)",
}


# --------------------------------------------------------------------------- truss members (design geometry)
def chord(sp, P, x0, x1, yc, layer="S-STL", cl=True, S=10, walls=True, breaks=(False, False)):
    """CHS chord in elevation between x0 and x1: two outline lines, the inner wall (fine hidden) and the
    centre line (grid chain). breaks = (left, right): a pipe break (chs_break) is drawn there, so the inner walls
    stop on the break curve instead of running through it"""
    line(sp, P(x0, yc + DC / 2), P(x1, yc + DC / 2), layer)
    line(sp, P(x0, yc - DC / 2), P(x1, yc - DC / 2), layer)
    if walls:
        ri = DC / 2 - TC_T
        for yw in (ri, -ri):
            a, b = (x0, yc + yw), (x1, yc + yw)
            if breaks[0]:
                a = break_point((x0, yc), (-1.0, 0.0), DC, -yw)
            if breaks[1]:
                b = break_point((x1, yc), (1.0, 0.0), DC, yw)
            line(sp, P(*a), P(*b), "S-STL-WALL")
    if cl:
        line(sp, P(x0 - 3 * S, yc), P(x1 + 3 * S, yc), "S-GRID")


def branch(sp, P, name, cut=None, layer="S-STL", cl=True, S=10, walls=True):
    """web member outline between the chord faces, its inner wall (fine hidden) and axis. cut = (node, length):
    only the part within 'length' (on the axis) of that node's chord face is drawn; outlines, walls and axis all
    end on ONE section square to the member axis, where the tube break is drawn"""
    lines, a, u = branch_lines(name)
    g = group_of(name)
    Db, tb = SEC[g].D, SEC[g].t
    nv = (-u[1], u[0])
    sides = (1, -1)                                   # lines[0] is offset +Db/2 nv, lines[1] -Db/2 nv
    pts = [list(ln) for ln in lines]
    ax = list(a)

    def wall_on_face(p, sgn):
        """inner-wall point: the outline point moved t inward, slid along the member to the same chord face"""
        q = (p[0] - sgn * tb * nv[0], p[1] - sgn * tb * nv[1])
        t_ = (p[1] - q[1]) / u[1]
        return (q[0] + t_ * u[0], p[1])

    wl = [[wall_on_face(ln[0], sgn), wall_on_face(ln[1], sgn)] for ln, sgn in zip(lines, sides)]
    if cut:
        node, Lc = cut
        k = 0 if node[0] == "T" else 1                 # keep this end
        sg = 1 if k == 0 else -1
        c = (a[k][0] + sg * u[0] * Lc, a[k][1] + sg * u[1] * Lc)          # cut point on the axis
        for q, w, sgn in zip(pts, wl, sides):
            q[1 - k] = (c[0] + sgn * Db / 2 * nv[0], c[1] + sgn * Db / 2 * nv[1])
            w[1 - k] = break_point(c, (sg * u[0], sg * u[1]), Db, sgn * sg * (Db / 2 - tb))
        ax[1 - k] = c
        chs_break(sp, P(*c), (sg * u[0], sg * u[1]), Db, tb, S, layer)
    for p0, p1 in pts:
        line(sp, P(*p0), P(*p1), layer)
    if walls:
        for q0, q1 in wl:
            line(sp, P(*q0), P(*q1), "S-STL-WALL")
    if cl:
        line(sp, P(*ax[0]), P(*ax[1]), "S-GRID")
    return pts, ax


def branch_zones(name, node):
    """legs of the weld round a web member at 'node' as seen in elevation: (left silhouette, band, right
    silhouette). An inclined member leans over its HEEL (acute side, Psi < 60) and shows its TOE (obtuse, gap
    side, Psi > 120) on the other silhouette; a vertical shows SIDE legs (Psi = 90 in the truss plane)"""
    lg = WELDS[group_of(name)]["legs"]
    _, _, u = branch_lines(name)
    into = u if node[0] == "T" else (-u[0], -u[1])     # along the member, away from the chord
    side = lg["SIDE"]
    if abs(into[0]) < 1e-6:
        return side, side, side
    heel, toe = lg.get("HEEL", side), lg.get("TOE", side)
    return (toe, side, heel) if into[0] > 0 else (heel, side, toe)


def weld_branch(sp, P, name, node, S):
    """the weld round a web member at the chord face of 'node', seen in elevation: the profiles at both
    silhouettes (heel / toe legs) and the band across the near face (side leg), one hatched region"""
    wl, wb, wr = (max(v, WELD_MIN * S) for v in branch_zones(name, node))
    lines, a, u = branch_lines(name)
    k = 0 if node[0] == "T" else 1
    into = (u[0], u[1]) if k == 0 else (-u[0], -u[1])  # along the member, away from the chord
    J1, J2 = sorted((ln[k] for ln in lines), key=lambda q: q[0])
    weld_region(sp, P, [(J1[0] - wl, J1[1]), (J2[0] + wr, J2[1]),
                        (J2[0] + into[0] * wr, J2[1] + into[1] * wr), (J2[0] + into[0] * wb, J2[1] + into[1] * wb),
                        (J1[0] + into[0] * wb, J1[1] + into[1] * wb), (J1[0] + into[0] * wl, J1[1] + into[1] * wl)],
                wb, S)
