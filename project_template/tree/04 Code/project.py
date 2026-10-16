"""{{PROJECT}}: project data, the single source for the model, the calcs, the drawings and the report.

Every value is the engineer's, or comes from a received document: say which in a comment. A value not decided yet
stays None, and the script that needs it stops with a message; nothing is invented to fill a gap.
Units: m, kN (or tonf: say which), MPa.
"""

NAME = "{{PROJECT}}"
CODE = "{{CODE}}"                     # EIT §13 project abbreviation (PPPP)
STARTED = "{{STARTED}}"
STAGE = None                          # EIT Table 4.3: "P" preliminary, "T" tender, "F" construction ...

# --- design basis (02 Design basis\DESIGN_BASIS.md, approved by the engineer on ____) -------------------------
UNITS = None                          # e.g. ("kN", "m") or ("tonf", "m"): the model's units
CONCRETE = {}                         # e.g. {"default": 24.0} MPa cylinder, per member group
REBAR = {}                            # e.g. {"DB": ("SD40", 392.0), "RB": ("SR24", 235.0)} MPa
STEEL = {}                            # e.g. {"plates": "SM400B", "CHS": "STK400"}
LOADS = {}                            # e.g. {"SDL_floor": 1.5, "LL_office": 2.5} kN/m2, source in the comment
COMBINATIONS = {}
PILES = {}                            # e.g. {"SPUN 350": {"safe_load": 45.0}} tonf

# --- grids and levels (from the received architectural drawings: name the file) ------------------------------
GRIDS_X = {}                          # name -> coordinate (m)
GRIDS_Y = {}
LEVELS = {}                           # name -> level (m), structural (SFL) or finished (FFL): say which

# --- drawing settings (FLOOR_PLAN_DRAWING_INSTRUCTION FP0: the engineer chooses) -----------------------------
SHEET = None                          # "A1" / "A3"
FONT = None                           # font per project: ask the engineer
PLOT_STYLE = None                     # CTB file
LTSCALE = None


def need(value, what):
    """Stop with a clear message when a project value has not been decided yet."""
    if value in (None, {}, ""):
        raise SystemExit(f"!! {what} is not set in project.py: the engineer's value is needed")
    return value
