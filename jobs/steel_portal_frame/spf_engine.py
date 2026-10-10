"""
Project SPF (steel portal-frame building 26 x 90 m) on the general drafting engine (drafter/td_engine.py +
drafter/steel.py): project data, options, the A1 office sheet, and the frame geometry as drawn, taken from the
MIDAS model through calc_spf.py.

Sheets are A1 (td_engine.use_paper): plot style STRUCT-A1-A2.ctb with the engine colours moved to the office pens
(EIT 19.2, FLOOR_PLAN_DRAWING_INSTRUCTION FP3), dashes as LTSCALE 45 at 1:100 (FP4).

Drawn geometry versus the analysis model (README "Drawn geometry"): the MIDAS work lines are the member centre
lines. Columns are drawn tapered symmetrically about their grid line, as analysed. Rafters keep their TOP flange
straight in the roof plane (purlins sit on one line); the prismatic rafter centre line is the model work line and
the haunch deepens downward from the same top flange. Levels: Z = 0 of the model = underside of the base plates.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))                          # repository root: the drafter package
sys.path.insert(0, str(HERE))

from drafter import td_engine                                      # noqa: E402
td_engine.use_paper("A1", ctb="STRUCT-A1-A2.ctb", colour_map=td_engine.STRUCT_A1_A2, ltscale_equiv=45)
from drafter.td_engine import *                                    # noqa: E402,F401,F403
import calc_spf as C                                               # noqa: E402

# --------------------------------------------------------------------------- project data (placeholder, user 2026-10-04)
PROJ.update(code="SPF", project="STEEL PORTAL FRAME BUILDING 26 x 90 m", location="[ BUILDING / LOCATION ]",
            owner="[ OWNER NAME ]", date="04/10/2026", stage="D", rev="A")
td_engine.REVS = [("A", "ISSUED FOR REVIEW", PROJ["date"])]
td_engine.KEYPLAN_2 = "(STEEL STRUCTURE)"
td_engine.LEADER_ORTH = True
td_engine.WRAP_UNITS = True
TABLES.clear()
TABLES.update({
    "DESIGN": (1, "CONNECTION DESIGN SUMMARY"),
    "OPEN": (2, "ASSUMPTIONS AND OPEN ITEMS (TBC)"),
    "DWGS": (3, "DRAWING LIST"),
    "REAC": (4, "BASE REACTIONS (FACTORED, FROM THE MIDAS MODEL)"),
    "MEMB": (5, "MEMBER SCHEDULE AND BILL - ALL STRUCTURAL STEEL"),
    "PLATE": (6, "TAPERED MEMBER PLATES"),
    "EP": (7, "END PLATE CONNECTIONS"),
    "BOLT": (8, "FIELD BOLTS"),
    "SEC": (9, "SECONDARY FRAMING (PROPOSED - TBC)"),
})

from drafter.steel import *                                        # noqa: E402,F401,F403

for _s in (15, 200):
    DS[_s] = td_engine.dimstyle(f"EIT-{_s}", _s)
for _s in (100, 200):                              # grid chains: dot terminators (EIT 8.2, FP7)
    _g = doc.dimstyles.duplicate_entry(f"EIT-{_s}", f"EIT-{_s}-GRID")
    _g.dxf.dimblk = "DOT"
    _g.dxf.dimasz = 1.2
    DS[f"G{_s}"] = f"EIT-{_s}-GRID"
# tie / sag rods in plan and elevation: one line each on the grid linetype, their own pen (steel S4.11, FP9.2)
_rod = doc.layers.add("S-ROD", color=5, linetype="EIT_GRID")   # the pen of steel seen beyond (0.25), chain
_rod.dxf.lineweight = PEN[5][0]
LAYER_LW["S-ROD"] = PEN[5][0]

D = C.design()
T = C.TAPER
SPAN, BAY, NBAY, EAVE, SLOPE, THETA = C.SPAN, C.BAY, C.NBAY, C.EAVE_Z, C.SLOPE, C.THETA
COS, SIN = math.cos(THETA), math.sin(THETA)
RIDGE = C.RIDGE_X
CAN_A, CAN_B = C.CAN_L
GRID_NUM = [str(i + 1) for i in range(NBAY + 1)]                   # frames 1 - 10 along the building
GRID_LET = ("A", "B")                                              # column lines across the span
RAF = C.RAF
CAN = C.CAN


# --------------------------------------------------------------------------- frame geometry as drawn (mm)
def rafter_top(x):
    """top of the rafter top flange at horizontal x (left half; mirror for the right): the prismatic rafter
    centre line is the model work line, the top flange is d/2 above it (perpendicular)"""
    xx = x if x <= RIDGE else SPAN - x
    return EAVE + SLOPE * xx + RAF.d / 2 / COS


def haunch_d(x):
    """haunch depth (perpendicular) at horizontal x from the column centre line (model law, calc_spf.taper_d)"""
    return C.taper_d("H", x)


def col_d(z):
    """column depth as fabricated (straight flanges to the cap: calc_spf.col_depth)"""
    return C.col_depth(z)


def col_top():
    """top of the column (its cut, along the roof slope) above the rafter top flange at the column outer face:
    the knee end plate runs past the rafter top flange by pf + de (4E), so the column must contain it"""
    kj = D["KJ1"]
    return kj["pf"] + kj["de"]


# --------------------------------------------------------------------------- the typical frame, as drawn
class Frame:
    """left half of a typical frame (grid A at x = 0) in the frame plane (x horizontal, z up, mm); the right half
    is the mirror about the ridge (mx) except the canopy length. All lines are straight segments."""
    tf_c, tw_c, bf_c = T["C"]["tf"], T["C"]["tw"], T["C"]["bf"]
    tf_h, tw_h = T["H"]["tf"], T["H"]["tw"]

    @staticmethod
    def zt(x):
        """top of the rafter / canopy top flange (the roof line) at x (x < 0: canopy, same slope)"""
        xx = x if x <= RIDGE else SPAN - x
        return EAVE + SLOPE * xx + RAF.d / 2 / COS

    @staticmethod
    def dv(x):
        """vertical depth of the rafter at x (haunch to X_SPLICE, then prismatic)"""
        xx = x if x <= RIDGE else SPAN - x
        return (haunch_d(xx) if xx < C.X_SPLICE else RAF.d) / COS

    @classmethod
    def zb(cls, x):
        return cls.zt(x) - cls.dv(x)

    @staticmethod
    def cx(z, side=1):
        """column flange face x at height z: side = -1 outer, +1 inner (left column, centre line x = 0)"""
        return side * col_d(z) / 2

    @classmethod
    def plate_x(cls, z):
        """inner face of the knee end plate (the column inner flange face) at height z"""
        return cls.cx(z, 1)

    @classmethod
    def knee(cls):
        """knee geometry from the calc (calc_spf.knee_geometry): the rafter flanges meeting the knee plate, the
        bolt rows, the plate ends, the column top"""
        return D["KJ1"]["geom"]


# --------------------------------------------------------------------------- drawing primitives
def off(p, n, k):
    return (p[0] + n[0] * k, p[1] + n[1] * k)


def unit(a, b):
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    return ((b[0] - a[0]) / L, (b[1] - a[1]) / L), L


def girder(sp, P, outer_a, outer_b, inner_a, inner_b, tf, layer="S-STL", ends=True, inner_ok=True):
    """welded I-member in elevation from its two outer flange lines (outer_a-outer_b, inner_a-inner_b: each a
    straight line). The flange thickness lines are drawn tf inside each outer line; ends closes the member."""
    for a, b, oa, ob in ((outer_a, outer_b, inner_a, inner_b), (inner_a, inner_b, outer_a, outer_b)):
        line(sp, P(*a), P(*b), layer)
        u, _ = unit(a, b)
        n = (-u[1], u[0])
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        mo = ((oa[0] + ob[0]) / 2, (oa[1] + ob[1]) / 2)
        if (mo[0] - mid[0]) * n[0] + (mo[1] - mid[1]) * n[1] < 0:
            n = (-n[0], -n[1])
        if inner_ok:
            line(sp, P(*off(a, n, tf)), P(*off(b, n, tf)), "S-STL-VIS")
    if ends:
        line(sp, P(*outer_a), P(*inner_a), layer)
        line(sp, P(*outer_b), P(*inner_b), layer)


def hsec(sp, P, c, d, bf, tw, tf, rot=0.0, layer="S-STL", fill=False):
    """H section cut (outline), centre c, web along the local y axis rotated by rot (deg)"""
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    h, b, w = d / 2, bf / 2, tw / 2
    pts = [(-b, h), (b, h), (b, h - tf), (w, h - tf), (w, -h + tf), (b, -h + tf), (b, -h), (-b, -h), (-b, -h + tf),
           (-w, -h + tf), (-w, h - tf), (-b, h - tf)]
    q = [P(c[0] + x * ca - y * sa, c[1] + x * sa + y * ca) for x, y in pts]
    pline(sp, q, layer, close=True)
    if fill:
        hatch(sp, q, "SOLID", 1.0, layer="S-WELD")
    return q


def plate_rect(sp, P, c, w, h, rot=0.0, layer="S-STL"):
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    q = [P(c[0] + x * ca - y * sa, c[1] + x * sa + y * ca) for x, y in pts]
    pline(sp, q, layer, close=True)
    return q


def gridline(sp, P, a, b, label, S, at="a", layer="S-GRID"):
    """grid line from a to b with its bubble (7 mm, bold label) beyond the 'at' end"""
    u, L = unit(a, b)
    r = 3.5 * S
    if at == "a":
        c = off(a, u, -(r + 2 * S))
        line(sp, P(*off(c, u, r)), P(*b), layer)
    else:
        c = off(b, u, r + 2 * S)
        line(sp, P(*a), P(*off(c, u, -r)), layer)
    sp.add_circle(P(*c), r, dxfattribs=A("S-SYMB"))
    text(sp, label, P(*c), 2.8 * S, "S-TEXT", TA.MIDDLE_CENTER, style="ANB")
    return c


def mtag(sp, P, c, s, S):
    """member mark in a circle at c (model coordinates of the view)"""
    tag(sp, P(*c), s, S)


def lv(sp, P, x, y, value, desc, S, ext=(-6, 30)):
    level(sp, x, y, value, desc, S, ext)


def fmt_level(z_mm):
    return f"{'+' if z_mm >= 0 else '-'}{abs(z_mm) / 1000:.3f}"


def n_fmt(v, nd=0):
    return f"{v:,.{nd}f}".replace(",", " ")
