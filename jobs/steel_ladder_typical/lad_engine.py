"""
Typical fixed steel ladder (worked example LAD): project data, options and the ladder basis, on the general engine
(drafter/td_engine.py + drafter/steel.py + drafter/steel_access.py).

Geometry from OSHA 29 CFR 1910.23 and 1910.28 (text checked at osha.gov on 15/10/2026, values converted from
inches and rounded to the safe side). Member sizes, bracket spacing, anchors and the optional cage are ASSUMED
typical values: they are stated on the drawings and listed as open items in README.md; a project designs them.
Model space at real size (1 unit = 1 mm); each view at its own scale S.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))                          # repository root: the drafter package
sys.path.insert(0, str(HERE))

from drafter import td_engine                                      # noqa: E402
from drafter.td_engine import *                                    # noqa: E402,F401,F403

PROJ.update(code="LAD", project="TYPICAL FIXED STEEL LADDER", location="[ BUILDING / LOCATION ]",
            owner="[ OWNER NAME ]", date="15/10/2026", stage="D", rev="A")
td_engine.REVS = [("A", "WORKED EXAMPLE FOR REVIEW", PROJ["date"])]
td_engine.KEYPLAN_2 = "(LADDER LD1)"
td_engine.LEADER_ORTH = True
td_engine.WRAP_UNITS = True
TABLES.clear()
TABLES.update({
    "GEOM": (1, "FIXED LADDER GEOMETRY"),
    "MEMB": (2, "LADDER MEMBERS (ASSUMED)"),
})

from drafter.steel import *                                        # noqa: E402,F401,F403
from drafter.steel_access import *                                 # noqa: E402,F401,F403

# --------------------------------------------------------------------------- basis: OSHA 29 CFR 1910.23 / 1910.28
INCH = 25.4
LIMITS = {                          # key: (value adopted, limit text, reference); limits from inches, safe side
    "pitch": (300.0, "254 - 355, UNIFORM", "1910.23(b)(1), (b)(2)"),
    "width": (450.0, "≥ 407", "1910.23(b)(4)"),
    "toe": (250.0, "≥ 178", "1910.23(d)(2)"),
    "ext": (1100.0, "≥ 1067", "1910.23(d)(4)"),
    "flare": (700.0, "610 - 762", "1910.23(d)(5)"),
    "step": (250.0, "178 - 304", "1910.23(d)(12)(i)"),
    "climb": (800.0, "≥ 762", "1910.23(d)(13)(ii)"),
    "side": (400.0, "≥ 381", "1910.23(d)(13)(i)"),
}
PITCH = LIMITS["pitch"][0]          # rung centres
B = LIMITS["width"][0]              # clear width between the stiles
TOE = LIMITS["toe"][0]              # rung centre line to the wall behind
EXT_UP = LIMITS["ext"][0]           # stiles above the landing
FLARE = LIMITS["flare"][0]          # clear between the stiles at the walk-through
STEP = LIMITS["step"][0]            # rung centre line to the landing edge (through ladder)
CLIMB = LIMITS["climb"][0]          # clear space on the climbing side, from the rung centre line
SIDE = LIMITS["side"][0]            # clear space each side of the ladder centre line
FALL_H = 24 * 12 * INCH             # 1910.28(b)(9): above 24 ft (7315 mm) a ladder safety system or PFAS

H_CLIMB = 4500.0                    # example: ground to landing (roof slab); fits A3 at 1:25 unbroken
N_RUNG = int(round(H_CLIMB / PITCH))
assert abs(N_RUNG * PITCH - H_CLIMB) < 1, "rungs must divide the climb evenly (1910.23(b)(1))"
assert all([254 <= PITCH <= 14 * INCH, B >= 16 * INCH, TOE >= 7 * INCH, EXT_UP >= 42 * INCH,
            24 * INCH <= FLARE <= 30 * INCH, 7 * INCH <= STEP <= 12 * INCH, CLIMB >= 30 * INCH,
            SIDE >= 15 * INCH]), "ladder geometry outside OSHA 1910.23"
assert H_CLIMB <= FALL_H, "climb above 24 ft: add a ladder safety system (1910.28(b)(9)) to this example"

# --------------------------------------------------------------------------- members: ASSUMED typical (open item)
STILE = (75.0, 10.0)                # FL 75 x 10, depth x thickness
RUNG_D = 20.0                       # solid round bar, knurled
HOLE_D = 22.0                       # hole in the stile for the rung (plug weld)
BRK_MAX = 1800.0                    # wall brackets at <= 1800 mm
BRK = (75.0, 10.0)                  # FL 75 x 10 bent bracket
ANCH_D, ANCH_HEF = 16.0, 100.0      # M16 chemical anchor, embedment
BASE_PL = (150.0, 100.0, 10.0)         # base plate length x width x thickness
WALL_T, SLAB_T = 200.0, 150.0       # existing RC wall and roof slab (example)
CAGE = dict(depth=750.0, hoop=(50.0, 6.0), vert=(25.0, 6.0), n_vert=7, start=2200.0, hoop_max=1500.0)
