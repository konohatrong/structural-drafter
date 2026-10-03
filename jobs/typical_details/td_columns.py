"""
Typical column details - STR-ST-1101 (ties and splice zones), STR-ST-1102 (size change, joints, ends).
Sources : EIT 011008-21 ch. 7, 12; DPT 1301/1302-61 cl. 5.2.5 - 5.2.10; TATA RC detailing handbook (column chapter).
"""
from td_engine import *

BASE = "STR-ST-1101_Typical_Column_Details_A3_RevA"
SHEETS[:] = [("1101", ["TYPICAL COLUMN DETAILS (1)", "TIES AND SPLICE ZONES"], "AS SHOWN"),
             ("1102", ["TYPICAL COLUMN DETAILS (2)", "SIZE CHANGE, JOINTS, ENDS"], "AS SHOWN")]


# ======================================================================= TYPICAL COLUMN DETAILS
# Drawing rule: normal (2.0 / 2.8 text, 2 mm arrows) - these are detail sheets, not the notes sheet.
# Sources: EIT 011008-21 (ch. 7, 12), DPT 1301/1302-61 (5.2.5 - 5.2.10), TATA / Jiravacharadet RC detailing
# handbook (column chapter, typical sheets). Values are symbolic (lo, s0, s) - numbers are in the tables.
COL = 400                      # typical column (drawn) - mm
CVR = 40                       # clear cover to tie
DT = 9                         # tie RB9 (drawn)
DBM = 20                       # main bar DB20 (drawn)
XB = CVR + DT + DBM / 2        # 59  main bar centre from column face
XT = CVR + DT / 2              # 44.5 tie centreline from face
HB = 600                       # beam depth
HC = 3000                      # clear storey height (floor top to beam soffit)
BST = 350                      # beam stub drawn each side
GAP = 50                       # drawn offset of lapped bars (schematic - visible at 1:50)
LAPD = 800                     # drawn lap length (schematic; real value per 1001 table 6)
LO = 500                       # drawn lo


def ties(sp, P, x0, x1, ys, layer="S-REBR-SEC"):
    for y in ys:
        line(sp, P(x0, y), P(x1, y), layer)


def rbar(sp, pts, db=DBM, layer="S-REBR"):
    return bar(sp, pts, db, layer)


def crank(x0, x1, y_top, slope):
    """offset bend ending at y_top: returns the two bend points (vertical legs above / below)"""
    v = abs(x1 - x0) * slope
    return [(x0, y_top - v), (x1, y_top)]


def beams_elev(sp, P, levels, left=True, right=True, width=COL):
    """beam stubs framing into the column in the plane of the elevation; levels = beam soffit levels"""
    for yb in levels:
        yt = yb + HB
        if left:
            line(sp, P(-BST, yt), P(0, yt), "S-CONC")
            line(sp, P(-BST, yb), P(0, yb), "S-CONC")
            zbreak(sp, P(-BST, yb - 80), P(-BST, yt + 80), 50)
        if right:
            line(sp, P(width, yt), P(width + BST, yt), "S-CONC")
            line(sp, P(width, yb), P(width + BST, yb), "S-CONC")
            zbreak(sp, P(width + BST, yb - 80), P(width + BST, yt + 80), 50)


def col_faces(sp, P, spans, width=COL, left=True, right=True):
    for y0, y1 in spans:
        if left:
            line(sp, P(0, y0), P(0, y1), "S-CONC")
        if right:
            line(sp, P(width, y0), P(width, y1), "S-CONC")


# ----------------------------------------------------------------------- 1101: column elevations by frame type
def col_elev(ox, oy, kind):
    """one storey of an interior column, beams both sides, for kind ORD / IMF / SMF (1:50)"""
    S = 50
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    ybot, ytop = -1250, HC + HB + 550
    col_faces(sp, P, [(ybot, -HB), (0, HC), (HC + HB, ytop)])
    beams_elev(sp, P, [-HB, HC])
    zbreak(sp, P(-60, ybot), P(COL + 60, ybot), S)
    zbreak(sp, P(-60, ytop), P(COL + 60, ytop), S)
    xl, xr = XB, COL - XB

    if kind == "ORD":                 # lap just above the floor, both faces; lower bars stop at the lap top
        laps = [(0, LAPD), (0, LAPD)]
    elif kind == "IMF":               # mid zone, adjacent laps staggered ~1.0 m
        laps = [(650, 650 + LAPD), (1650, 1650 + LAPD)]
    else:                             # centre half of Hc only
        laps = [(1000, 1000 + LAPD), (1000, 1000 + LAPD)]
    slope = 6 if kind == "ORD" else 10
    for (y0, y1), xf, inw in ((laps[0], xl, 1), (laps[1], xr, -1)):
        rbar(sp, [P(xf, ybot), P(xf, y1)])                                    # bar from below, ends at lap top
        xi = xf + inw * GAP                                                     # bar above sits inside at the lap
        (cx0, cy0), (cx1, cy1) = crank(xi, xf, y1 + GAP * slope, slope)
        rbar(sp, [P(xi, y0), P(xi, y1), P(xf, y1 + GAP * slope), P(xf, ytop)])
        if kind == "ORD":                                                       # next storey lap at the upper floor
            rbar(sp, [P(xi, HC + HB), P(xi, ytop)])

    tx0, tx1 = XT, COL - XT
    if kind == "ORD":
        s = 300
        clear = rng(s / 2, HC - s / 2, s)
        joint = [-HB + 150, -150, HC + 150, HC + 450]
        outside = [-HB - s / 2, -HB - s / 2 - s, HC + HB + s / 2]
        ys = clear + joint + outside
    elif kind == "IMF":
        s0 = 150
        bot = rng(s0 / 2, LO, s0)
        top = [HC - y for y in bot]
        mid = rng(bot[-1] + 2 * s0, top[-1] - s0, 2 * s0)
        joint = rng(-HB + 75, -75, 150) + rng(HC + 75, HC + HB - 75, 150)
        outside = [-HB - 75, -HB - 225, -HB - 375, HC + HB + 75, HC + HB + 225, HC + HB + 375]
        ys = bot + mid + top + joint + outside
    else:
        s = 100
        bot = rng(s / 2, LO, s)
        top = [HC - y for y in bot]
        lap0, lap1 = laps[0]
        mid = rng(bot[-1] + 120, lap0 - 60, 120) + rng(lap0, lap1, s) + rng(lap1 + 120, top[-1] - 60, 120)
        joint = rng(-HB + 50, -50, s) + rng(HC + 50, HC + HB - 50, s)
        outside = [-HB - 50 - k * s for k in range(6)] + [HC + HB + 50 + k * s for k in range(5)]
        ys = bot + mid + top + joint + outside
    ties(sp, P, tx0, tx1, [y for y in ys if ybot < y < ytop])

    # ---- dimensions (left): zones; (right): laps / splice zone
    xd = -BST - 260
    if kind == "ORD":
        dim(sp, P(0, 0), P(0, HC), P(xd, 0), S, angle=90, text="Hc (CLEAR)")
    else:
        dim(sp, P(0, 0), P(0, LO), P(xd, 0), S, angle=90, text="lo")
        dim(sp, P(0, LO), P(0, HC - LO), P(xd, 0), S, angle=90, text="MID ZONE")
        dim(sp, P(0, HC - LO), P(0, HC), P(xd, 0), S, angle=90, text="lo")
        dim(sp, P(0, 0), P(0, HC), P(xd - 260, 0), S, angle=90, text="Hc (CLEAR)")
    # splice dimensions also on the LEFT (outermost column): nothing between the column and its notes
    xl_d = xd - 520 if kind != "ORD" else xd - 260
    if kind == "SMF":
        dim(sp, P(0, 0), P(0, HC / 4), P(xl_d, 0), S, angle=90, text="Hc/4")
        dim(sp, P(0, HC / 4), P(0, 3 * HC / 4), P(xl_d, 0), S, angle=90, text="SPLICE ZONE")
        dim(sp, P(0, 3 * HC / 4), P(0, HC), P(xl_d, 0), S, angle=90, text="Hc/4")
    elif kind == "IMF":
        dim(sp, P(0, laps[0][0]), P(0, laps[1][0]), P(xl_d, 0), S, angle=90, text="≈ 1.0 m")
    else:
        dim(sp, P(0, 0), P(0, LAPD), P(xl_d, 0), S, angle=90, text="LAP")

    # ---- notes (right column)
    note_cfg(xR=P(COL + BST + 250, 0)[0], yminR=P(0, ybot)[1])
    kr = P(COL + BST + 250, 0)
    R = lambda tip, s, **kw: leader(sp, P(*tip), kr, s, S, "R", 46, **kw)
    if kind == "ORD":
        R((COL / 2, HC + 150), "TIES CONTINUE THROUGH THE JOINT; MAY STOP 75 BELOW THE LOWEST BEAM BARS WHERE "
                               "BEAMS FRAME ON 4 SIDES")
        R((COL / 2, HC - 150), "LAST TIE ≤ s/2 BELOW THE BEAM SOFFIT")
        R((COL / 2, 1950), "TIES @ s ≤ 16 db, 48 dt AND LEAST COLUMN SIZE")
        R((xl + GAP, 400), "LAP ABOVE THE FLOOR (TABLE 6, 1001); CLASS B, OR COMPRESSION LAP IF NEVER IN TENSION")
        R((COL / 2, 150), "FIRST TIE ≤ s/2 ABOVE THE FLOOR")
        R((xl + GAP / 2, LAPD + 150), "OFFSET BEND ≤ 1:6", )
    elif kind == "IMF":
        R((COL / 2, HC + 225), "JOINT HOOPS Av ≥ c1 s / 3fy OVER THE DEEPEST BEAM (OMIT ONLY IF CONFINED ON 4 SIDES "
                               "AND NOT IN THE SEISMIC SYSTEM)")
        R((COL / 2, HC - 75), "FIRST HOOP ≤ s0/2 FROM THE JOINT FACE")
        R((COL / 2, HC - 225), "HOOPS @ s0 WITHIN lo")
        R((xr - GAP, 1650 + LAPD - 100), "LAPS IN THE MID ZONE ONLY, OUTSIDE lo; ADJACENT LAPS STAGGERED ≈ 1.0 m")
        R((COL / 2, 1275), "HOOPS @ ≤ 2 s0 OUTSIDE lo")
        R((xl + GAP / 2, 650 + LAPD + 250), "OFFSET BEND ≤ 1:10")
        R((COL / 2, 75), "FIRST HOOP ≤ s0/2 ABOVE THE FLOOR")
    else:
        R((COL / 2, HC + 250), "JOINT: FULL CONFINING HOOPS; ½ OF THEM AND s ≤ 150 WHERE 4 BEAMS ≥ ¾ COLUMN WIDTH")
        R((COL / 2, HC - 250), "CONFINING HOOPS @ s WITHIN lo, FIRST ≤ s/2 FROM THE FACE; Ash PER DPT EQ. 5.2-14, 5.2-15")
        R((xl - GAP * 0 + GAP, 1500), "TENSION LAP (CLASS B) IN THE CENTRE HALF ONLY; HOOPS @ s OVER THE LAP")
        R((COL / 2, 700), "HOOPS @ ≤ 6 db AND 150 OUTSIDE lo")
        R((COL / 2, -HB - 150), "BELOW THE BEAM THE lo ZONE REPEATS; HOOPS ≥ 300 INTO A FOOTING")


# ----------------------------------------------------------------------- 1101: columns next to masonry infill
def infill(ox, oy):
    S = 100
    sp = msp
    note_cfg(free=True)
    for k, case in enumerate(("PART", "ONE")):
        P = (lambda x, y, k=k: (ox + k * 4700 + x, oy + y))
        ybot, ytop = -HB - 300, HC + HB + 250
        col_faces(sp, P, [(ybot, -HB), (0, HC), (HC + HB, ytop)])
        beams_elev(sp, P, [-HB, HC])
        if case == "PART":
            for x0, x1 in ((-BST - 250, 0), (COL, COL + BST + 250)):
                pline(sp, [P(x0, 0), P(x0, 1300), P(x1, 1300), P(x1, 0)], "S-CONC-VIS")
                hatch(sp, [P(x0, 0), P(x0, 1300), P(x1, 1300), P(x1, 0)], "ANSI31", pscale("ANSI31", S, 1.2))
            ys = rng(75, HC - 75, 150)
            lab = ["(a) PARTIAL-HEIGHT INFILL", "HOOPS @ s0 OVER THE FULL HEIGHT;",
                   "SHEAR FOR THE SHORT COLUMN;", "HOOPS ≥ c1 INTO THE WALL ZONE"]
        else:
            x0, x1 = -BST - 250, 0
            pline(sp, [P(x0, 0), P(x0, HC), P(x1, HC), P(x1, 0)], "S-CONC-VIS")
            hatch(sp, [P(x0, 0), P(x0, HC), P(x1, HC), P(x1, 0)], "ANSI31", pscale("ANSI31", S, 1.2))
            ys = rng(75, LO, 150) + [HC - y for y in rng(75, LO, 150)] + rng(LO + 300, HC - LO - 150, 250)
            lab = ["(b) FULL INFILL ON ONE SIDE", "lo ZONES @ s0;", "MID ZONE ≤ 2 s0 AND ≤ d/2", ""]
        ties(sp, P, XT, COL - XT, ys)
        for xf in (XB, COL - XB):
            rbar(sp, [P(xf, ybot), P(xf, ytop)])
        for i, t in enumerate(lab):
            if t:
                text(sp, t, P(-BST - 250, ybot - 450 - i * 330), 2.0 * S, style="ANB" if i == 0 else "AN")


# ----------------------------------------------------------------------- 1102: section change
def sec_change(ox, oy, case):
    """change of column size at a floor. case: INT_S / INT_L (interior, offset <= 75 / > 75), EDGE_S / EDGE_L"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    edge = case.startswith("EDGE")
    Bl, Bu, xu0 = {"INT_S": (500, 400, 50), "INT_L": (650, 400, 125),
                   "EDGE_S": (500, 450, 0), "EDGE_L": (600, 400, 0)}[case]
    ybot, ytop = -1050, 900
    # concrete
    line(sp, P(0, ybot), P(0, -HB), "S-CONC")
    line(sp, P(Bl, ybot), P(Bl, -HB), "S-CONC")
    line(sp, P(xu0, 0), P(xu0, ytop), "S-CONC")
    line(sp, P(xu0 + Bu, 0), P(xu0 + Bu, ytop), "S-CONC")
    BS = 180
    for x0, x1, has in ((-BS, 0, not edge), (Bl, Bl + BS, True)):
        if has:
            line(sp, P(x0, 0), P(x1, 0), "S-CONC")
            line(sp, P(x0, -HB), P(x1, -HB), "S-CONC")
            zbreak(sp, P(x1 if x1 > Bl else x0, -HB - 80), P(x1 if x1 > Bl else x0, 80), S)
    if edge:
        line(sp, P(0, -HB), P(0, 0), "S-CONC")                                # exterior face through the floor
        line(sp, P(0, 0), P(xu0, 0), "S-CONC")
    else:
        line(sp, P(0, 0), P(xu0, 0), "S-CONC")                                # top of the lower column (step)
    line(sp, P(xu0 + Bu, 0), P(Bl, 0), "S-CONC")
    zbreak(sp, P(-60, ybot), P(Bl + 60, ybot), S)
    zbreak(sp, P(xu0 - 60, ytop), P(xu0 + Bu + 60, ytop), S)
    # bars: left and right faces
    notes = []
    for side in (0, 1):
        xl_bar = XB if side == 0 else Bl - XB
        xu_bar = xu0 + XB if side == 0 else xu0 + Bu - XB
        inw = 1 if side == 0 else -1
        off = abs(xu_bar - xl_bar)
        xi = xu_bar + inw * GAP                                                    # lapped bar sits inside
        rbar(sp, [P(xu_bar, 0), P(xu_bar, ytop)])                                  # upper column bar
        if off <= 75:
            h = abs(xi - xl_bar)
            v = 6 * h
            rbar(sp, [P(xl_bar, ybot), P(xl_bar, -v), P(xi, 0), P(xi, LAPD)])
            if side == 1 or case in ("INT_S", "EDGE_S"):
                notes.append(("CRANK", xl_bar + (xi - xl_bar) * 0.5, -v / 2))
        else:
            rbar(sp, [P(xl_bar, ybot), P(xl_bar, -50)])                            # stops 50 below slab top
            rbar(sp, [P(xi, -HB - 450), P(xi, LAPD)], layer="S-REBR")               # dowel
            notes.append(("DOWEL", xi, -HB - 250))
    # ties: lower column (normal s + 2 extra at the bends), joint @ <= 150, upper column
    ties(sp, P, XT, Bl - XT, [-HB - 375, -HB - 150, -HB - 75])
    ties(sp, P, XT, Bl - XT, [-HB + 75, -375, -225, -75])
    ties(sp, P, xu0 + XT, xu0 + Bu - XT, [75, 375, 675])
    # dimension of the offset (at the step)
    if case == "INT_S":
        dim(sp, P(0, 150), P(xu0, 150), P(0, 330), S, text="≤ 75")
    elif case == "INT_L":
        dim(sp, P(0, 150), P(xu0, 150), P(0, 330), S, text="> 75")
    elif case == "EDGE_S":
        dim(sp, P(xu0 + Bu, 150), P(Bl, 150), P(0, 330), S, text="≤ 75")
    else:
        dim(sp, P(xu0 + Bu, 150), P(Bl, 150), P(0, 330), S, text="> 75")
    # notes (right column, short)
    note_cfg(xR=P(Bl + BS + 90, 0)[0], yminR=P(0, ybot)[1])
    kr = P(Bl + BS + 90, 0)
    Rn = lambda tip, s, w=25: leader(sp, P(*tip), kr, s, S, "R", w)
    for kind, x, y in notes:
        if kind == "CRANK":
            Rn((x, y), "CRANK ≤ 1:6 IN THE JOINT")
            break
    for kind, x, y in notes:
        if kind == "DOWEL":
            Rn((x, y), "DOWELS = UPPER BARS, LAPPED BELOW AND ABOVE")
            Rn((Bl - XB, -120), "LOWER BARS STOP 50 BELOW THE TOP")
            break
    Rn((Bl / 2, -300), "TIES @ ≤ 150 THROUGH THE JOINT")
    Rn((Bl / 2, -HB - 110), "2 EXTRA TIES WITHIN 150 OF THE BEND")
    Rn((xu0 + XB + GAP, 500), "LAP PER FRAME TYPE (1101)")


# ----------------------------------------------------------------------- 1102: edge / corner joint
def joint_plan(ox, oy):
    """corner column 400 x 400, beams from the right and from above; exterior faces left and bottom (1:25)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    bw = 300
    pline(sp, [P(0, 0), P(COL, 0), P(COL, COL), P(0, COL)], "S-CONC", close=True)
    for (x0, y0, x1, y1) in ((COL, 50, COL + 700, 50 + bw), (50, COL, 50 + bw, COL + 700)):
        if x1 - x0 > y1 - y0:
            line(sp, P(x0, y0), P(x1, y0), "S-CONC")
            line(sp, P(x0, y1), P(x1, y1), "S-CONC")
            zbreak(sp, P(x1, y0 - 60), P(x1, y1 + 60), S)
        else:
            line(sp, P(x0, y0), P(x0, y1), "S-CONC")
            line(sp, P(x1, y0), P(x1, y1), "S-CONC")
            zbreak(sp, P(x0 - 60, y1), P(x1 + 60, y1), S)
    # column bars 8 + perimeter tie + inner diamond tie (hooks staggered)
    c = XB
    pts = [(c, c), (COL / 2, c), (COL - c, c), (COL - c, COL / 2), (COL - c, COL - c), (COL / 2, COL - c),
           (c, COL - c), (c, COL / 2)]
    rb = rdot(DBM, S)
    corner = lambda x, y: (P(x, y)[0], P(x, y)[1], rb + DT / 2)
    stirrup(sp, corner(c, COL - c), corner(COL - c, COL - c), corner(COL - c, c), corner(c, c), 6 * DT + 20)
    for x, y in pts:
        dot(sp, P(x, y), rb)
    # beam top bars to the far side of the column core, turned down (x = bent away from viewer)
    xe = XT + DT / 2 + DBM + 12                                                     # inside the far column bars
    for yy in (100, 200, 300):
        rbar(sp, [P(COL + 700, yy), P(xe, yy)])
        for d in (1, -1):
            line(sp, P(xe - 22, yy - 22 * d), P(xe + 22, yy + 22 * d), "S-REBR")
    for xx in (110, 200, 290):
        rbar(sp, [P(xx, COL + 700), P(xx, xe + 40)])
        for d in (1, -1):
            line(sp, P(xx - 22, xe + 40 - 22 * d), P(xx + 22, xe + 40 + 22 * d), "S-REBR")
    cutmark_simple(sp, P(COL + 450, -250), P(COL + 450, COL + 250), S, "A")
    text(sp, "EXTERIOR", P(-80, COL / 2), 2.0 * S, align=TA.MIDDLE_RIGHT, rot=90)
    note_cfg(free=True)


def cutmark_simple(sp, p1, p2, S, label):
    line(sp, p1, p2, "S-CUTL")
    for p, sg in ((p1, 1), (p2, -1)):
        tip = (p[0] - 5 * S, p[1])
        line(sp, p, tip, "S-SYMB")
        arrowhead(sp, tip, p, 2.0 * S, "S-SYMB")
        text(sp, label, (p[0] - 3 * S, p[1] + sg * -3.2 * S), 2.8 * S, "S-TEXT", TA.MIDDLE_CENTER, style="ANB")


def joint_elev(ox, oy):
    """section A-A through the edge joint: beam from the right, exterior face left (1:25)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    ybot, ytop = -HB - 380, 500
    line(sp, P(0, ybot), P(0, ytop), "S-CONC")                                      # exterior face
    line(sp, P(COL, ybot), P(COL, -HB), "S-CONC")
    line(sp, P(COL, 0), P(COL, ytop), "S-CONC")
    line(sp, P(COL, 0), P(COL + 900, 0), "S-CONC")
    line(sp, P(COL, -HB), P(COL + 900, -HB), "S-CONC")
    zbreak(sp, P(COL + 900, -HB - 80), P(COL + 900, 80), S)
    zbreak(sp, P(-60, ybot), P(COL + 60, ybot), S)
    zbreak(sp, P(-60, ytop), P(COL + 60, ytop), S)
    for xf in (XB, COL - XB):
        rbar(sp, [P(xf, ybot), P(xf, ytop)])
    xe = XB + DBM + 15                                                               # hook tails inside the far bars
    yt_b = -50 - 10                                                                  # beam top bar
    yb_b = -HB + 50 + 10
    L = 12 * DBM
    rbar(sp, [P(COL + 900, yt_b), P(xe, yt_b), P(xe, yt_b - L - 80)])
    rbar(sp, [P(COL + 900, yb_b), P(xe + 35, yb_b), P(xe + 35, yb_b + L + 80)])
    ties(sp, P, XT, COL - XT, [-HB + 75, -HB + 225, -375, -225, -75] + [-HB - 75, -HB - 225, 75, 225, 375])
    for x in rng(COL + 50, COL + 850, 150):                                          # beam stirrups
        line(sp, P(x, -HB + 45), P(x, -45), "S-REBR-SEC")
    dim(sp, P(COL, -HB), P(xe - 10, -HB), P(0, -HB - 200 + 0), S, text="ldh")
    dim(sp, P(COL, -HB + 30), P(COL + 50, -HB + 30), P(0, -HB - 320), S, text="≤ 50")
    note_cfg(xR=P(COL + 1150, 0)[0], yminR=P(0, -HB + 40)[1], upR=True)          # notes above the dimensions
    kr = P(COL + 1150, 0)
    R = lambda tip, s: leader(sp, P(*tip), kr, s, S, "R", 44)
    R((COL + 600, yt_b), "BEAM BARS RUN TO THE FAR SIDE OF THE COLUMN CORE; 90° HOOKS TURNED INTO THE JOINT: TOP "
                         "BARS DOWN, BOTTOM BARS UP")
    R((xe, -300), "HOOK TAILS INSIDE THE FAR-FACE COLUMN BARS")
    R((COL / 2, -225), "COLUMN TIES CONTINUE THROUGH THE JOINT @ ≤ 150 (SPECIAL FRAMES: CONFINING HOOPS @ s)")
    R((COL + 50, -HB + 200), "FIRST BEAM STIRRUP ≤ 50 FROM THE COLUMN FACE")


# ----------------------------------------------------------------------- 1102: column top at roof
def roof_top(ox, oy):
    S = 50
    sp = msp
    note_cfg(free=True)
    for k, edge in enumerate((False, True)):
        P = (lambda x, y, k=k: (ox + k * 2700 + x, oy + y))
        ybot = -HB - 650
        line(sp, P(0, ybot), P(0, -HB), "S-CONC")
        line(sp, P(COL, ybot), P(COL, -HB), "S-CONC")
        if edge:
            line(sp, P(0, -HB), P(0, 0), "S-CONC")
        line(sp, P(0 if edge else -BST, 0), P(COL + BST, 0), "S-CONC")
        line(sp, P(COL, -HB), P(COL + BST, -HB), "S-CONC")
        zbreak(sp, P(COL + BST, -HB - 80), P(COL + BST, 80), S)
        if not edge:
            line(sp, P(-BST, -HB), P(0, -HB), "S-CONC")
            zbreak(sp, P(-BST, -HB - 80), P(-BST, 80), S)
        zbreak(sp, P(-60, ybot), P(COL + 60, ybot), S)
        L = 12 * DBM + 60
        yh = -50 - 10
        for xf, d in ((XB, -1), (COL - XB, 1)):
            dd = d if not edge else 1                                                   # edge: both hooks inward
            rbar(sp, [P(xf, ybot), P(xf, yh), P(xf + dd * L, yh)])
        ties(sp, P, XT, COL - XT, [-HB - 150, -HB - 450, -HB - 750] + rng(-HB + 150, -150, 150))
        lab = ("(a) INTERIOR: HOOKS OUTWARD" if not edge else "(b) EDGE / CORNER: HOOKS INWARD")
        text(sp, lab, P(-BST, ybot - 280), 2.0 * S, style="ANB")


# ----------------------------------------------------------------------- 1102: column on a transfer beam
def on_beam(ox, oy):
    """column planted on a beam: bars to the beam bottom layer with 90 deg hooks outward, ties continue (1:50)"""
    S = 50
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    Db, Lb = 800, 1800
    x0 = (Lb - COL) / 2
    line(sp, P(0, 0), P(x0, 0), "S-CONC")
    line(sp, P(x0 + COL, 0), P(Lb, 0), "S-CONC")
    line(sp, P(0, -Db), P(Lb, -Db), "S-CONC")
    zbreak(sp, P(0, -Db - 80), P(0, 80), S)
    zbreak(sp, P(Lb, -Db - 80), P(Lb, 80), S)
    line(sp, P(x0, 0), P(x0, 1300), "S-CONC")
    line(sp, P(x0 + COL, 0), P(x0 + COL, 1300), "S-CONC")
    zbreak(sp, P(x0 - 60, 1300), P(x0 + COL + 60, 1300), S)
    yb = -Db + 60
    rbar(sp, [P(60, yb), P(Lb - 60, yb)], 25)
    rbar(sp, [P(60, -60), P(Lb - 60, -60)], 25)
    L = 12 * DBM + 60
    yh = yb + 45
    for xf, d in ((x0 + XB, -1), (x0 + COL - XB, 1)):
        rbar(sp, [P(xf, 1300), P(xf, yh), P(xf + d * L, yh)])
    ties(sp, P, x0 + XT, x0 + COL - XT, rng(-Db + 150, -150, 150) + rng(75, 1200, 300))
    note_cfg(xR=P(Lb + 250, 0)[0])
    kr = P(Lb + 250, 0)
    R = lambda tip, s: leader(sp, P(*tip), kr, s, S, "R", 40)
    R((x0 + COL - XB, -300), "COLUMN BARS TO THE BEAM BOTTOM LAYER, 90° HOOKS OUTWARD ON THE BOTTOM BARS")
    R((x0 + COL / 2, -450), "COLUMN TIES CONTINUE INTO THE BEAM AT THE SAME SPACING")
    R((x0 + COL / 2, 75), "FIRST TIE ≤ s/2 ABOVE THE BEAM")


# ----------------------------------------------------------------------- 1102: starter bars in footing
def footing(ox, oy):
    S = 50
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    Bf, Tf = 1600, 600
    xc0 = (Bf - COL) / 2
    pline(sp, [P(0, -Tf), P(Bf, -Tf), P(Bf, 0), P(xc0, 0)], "S-CONC")
    line(sp, P(xc0 + COL, 0), P(Bf, 0), "S-CONC")
    line(sp, P(0, 0), P(xc0, 0), "S-CONC")
    line(sp, P(0, -Tf), P(0, 0), "S-CONC")
    pline(sp, [P(-50, -Tf - 50), P(Bf + 50, -Tf - 50)], "S-LEAN")
    line(sp, P(xc0, 0), P(xc0, 1500), "S-CONC")
    line(sp, P(xc0 + COL, 0), P(xc0 + COL, 1500), "S-CONC")
    zbreak(sp, P(xc0 - 60, 1500), P(xc0 + COL + 60, 1500), S)
    yb1 = -Tf + 75 + 10
    rbar(sp, [P(75, -Tf + 170), P(75, yb1), P(Bf - 75, yb1), P(Bf - 75, -Tf + 170)], 16)
    for x in rng(150, Bf - 150, 200):
        dot(sp, P(x, yb1 + 26), rdot(16, S))
    L = 12 * DBM + 60
    yh = yb1 + 50
    for xf, d in ((xc0 + XB, -1), (xc0 + COL - XB, 1)):
        rbar(sp, [P(xf, 1500), P(xf, yh), P(xf + d * L, yh)])
    ties(sp, P, xc0 + XT, xc0 + COL - XT, [-150, -300, -450] + rng(75, 1400, 300))
    note_cfg(xR=P(Bf + 350, 0)[0])
    kr = P(Bf + 350, 0)
    R = lambda tip, s: leader(sp, P(*tip), kr, s, S, "R", 44)
    R((xc0 + COL / 2, 75), "FIRST TIE ≤ s/2 (lo ZONE: ≤ s0/2) ABOVE THE FOOTING; LAP ZONE PER FRAME TYPE (DETAILS 1 - 3, 1101)")
    R((xc0 + COL / 2, -300), "MIN. 3 TIES IN THE FOOTING; SPECIAL FRAMES: CONFINING HOOPS ≥ 300 INTO THE FOOTING")
    R((xc0 + COL - XB + L / 2, yh), "DOWELS = COLUMN BARS, DOWN TO THE BOTTOM MAT, 90° HOOK OUTWARD (INWARD AT A "
                                    "PROPERTY-LINE FOOTING)")


def tie_sets(ox, oy):
    S = 25
    sp = msp
    note_cfg(free=True)
    rb = rdot(DBM, S)

    def section(cx, cy, B, n_face, kind, label):
        P = lambda x, y: (ox + cx + x, oy + cy + y)
        pline(sp, [P(0, 0), P(B, 0), P(B, B), P(0, B)], "S-CONC", close=True)
        c = XB
        pos = [c + i * (B - 2 * c) / (n_face - 1) for i in range(n_face)]
        bars = set()
        for p_ in pos:
            for q in (c, B - c):
                bars.add((round(p_, 3), q))
                bars.add((q, round(p_, 3)))
        R_ = rb + DT / 2
        cor = lambda x, y: (P(x, y)[0], P(x, y)[1], R_)
        if kind != "OVERLAP":
            stirrup(sp, cor(c, B - c), cor(B - c, B - c), cor(B - c, c), cor(c, c), 6 * DT + 20)
        if kind == "OVERLAP":                                       # two overlapping hoops (Thai practice)
            stirrup(sp, cor(pos[1], B - c), cor(B - c, B - c), cor(B - c, c), cor(pos[1], c), 6 * DT + 20)
            stirrup(sp, cor(c, B - c), cor(pos[-2], B - c), cor(pos[-2], c), cor(c, c), 6 * DT + 20)
        if kind == "CROSS":                                         # crossties on every other intermediate bar
            j = 0
            for k, p_ in enumerate(pos[1:-1]):
                if k % 2 == 0:                                      # every other intermediate bar
                    a, b = (P(p_, B - c), P(p_, c)) if j % 2 == 0 else (P(p_, c), P(p_, B - c))
                    crosstie(sp, a, b, R_ + max(DT, 0.5 * S), 6 * DT + 20)
                    a, b = (P(c, p_), P(B - c, p_)) if j % 2 == 0 else (P(B - c, p_), P(c, p_))
                    crosstie(sp, a, b, R_ + max(DT, 0.5 * S), 6 * DT + 20)
                    j += 1
        for x, y in bars:
            dot(sp, P(x, y), rb)
        for i, t in enumerate(label):
            text(sp, t, P(0, -170 - i * 110), 2.0 * S / 2.2 if False else 2.0 * S, style="ANB" if i == 0 else "AN")

    def spiral(cx, cy, D, label):
        P = lambda x, y: (ox + cx + x, oy + cy + y)
        sp.add_circle(P(D / 2, D / 2), D / 2, dxfattribs=A("S-CONC"))
        sp.add_circle(P(D / 2, D / 2), D / 2 - XT, dxfattribs=A("S-REBR-SEC"))
        r = D / 2 - XB
        for k in range(8):
            a = 2 * math.pi * k / 8
            dot(sp, P(D / 2 + r * math.cos(a), D / 2 + r * math.sin(a)), rb)
        for i, t in enumerate(label):
            text(sp, t, P(0, -170 - i * 110), 2.0 * S, style="ANB" if i == 0 else "AN")

    g = 950
    section(0, 900, 400, 2, "ONE", ["(a) 4 BARS", "1 TIE"])
    section(g, 900, 400, 3, "CROSS", ["(b) 8 BARS", "TIE + 2 CROSSTIES"])
    section(2 * g, 900, 500, 4, "OVERLAP", ["(c) 12 BARS", "2 OVERLAPPING TIES"])
    section(0, 0, 600, 5, "CROSS", ["(d) 16 BARS, SPECIAL", "CROSSTIES, hx ≤ 350"])
    spiral(g + 150, 50, 500, ["(e) SPIRAL", "≥ 6 BARS"])


# ======================================================================= place model views
def views():
    EXT.update({
        "ORD": capture(col_elev, 0, 0, "ORD"),
        "IMF": capture(col_elev, 8000, 0, "IMF"),
        "SMF": capture(col_elev, 16000, 0, "SMF"),
        "INF": capture(infill, 26000, 0),
        "SC1": capture(sec_change, 0, -12000, "INT_S"),
        "SC2": capture(sec_change, 4000, -12000, "INT_L"),
        "SC3": capture(sec_change, 8000, -12000, "EDGE_S"),
        "SC4": capture(sec_change, 12000, -12000, "EDGE_L"),
        "JP": capture(joint_plan, 0, -20000),
        "JE": capture(joint_elev, 4000, -20000),
        "RF": capture(roof_top, 0, -30000),
        "TB": capture(on_beam, 8000, -30000),
        "TS": capture(tie_sets, 16000, -30000),
        "FT": capture(footing, 18000, -20000),
    })


# ======================================================================= sheet 1101
TIE_TABLE = [
    ["USE (DPT T2.3-1)", "SEISMIC CATEGORY B ONLY (R = 3)", "CATEGORY B, C; D ONLY ≤ 40 m, FORCES + 40 % (R = 5)", "ALL CATEGORIES (R = 8)"],
    ["SECTION, BARS", "ρ 1 – 8 %; ≥ 4 BARS (≥ 6 IN SPIRAL)", "ρ 1 – 6 %", "LEAST SIDE ≥ 300, SHORT/LONG ≥ 0.4; ρ 1 – 6 %; "
                                                                            "ΣMc ≥ 1.2 ΣMb"],
    ["END ZONE lo", "–", "≥ max (Hc/6, c1, 500)", "≥ max (Hc/6, c1, 500)"],
    ["SPACING IN lo", "s (AS BELOW)", "s0 ≤ min (8 db, 24 dt, c2/2, 300)",
     "s ≤ min (c2/4, 6 db, s0); s0 = 100 + (350 − hx)/3, 100 – 150"],
    ["FIRST TIE / HOOP", "≤ s/2 FROM FLOOR AND SOFFIT", "≤ s0/2 FROM THE JOINT FACE", "≤ s/2 FROM THE JOINT FACE"],
    ["SPACING OUTSIDE lo", "s ≤ min (16 db, 48 dt, LEAST SIZE)", "≤ 2 s0 (≤ d/2 BESIDE FULL-HEIGHT INFILL)",
     "≤ min (6 db, 150)"],
    ["HOOKS, CROSSTIES", "135° + 6 db ≥ 75; EVERY CORNER AND ALTERNATE BAR HELD, ≤ 150 CLEAR",
     "135° + 6 db ≥ 75 (90° ONLY WITH HOOK-CLIP)", "135° + 6 db ≥ 75; CROSSTIES 135° / 90° ALTERNATING; hx ≤ 350"],
    ["LAP LOCATION", "ANY LEVEL, NORMALLY JUST ABOVE THE FLOOR", "MID ZONE ONLY, OUTSIDE BOTH lo",
     "CENTRE HALF OF Hc ONLY"],
    ["LAP TYPE", "CLASS B (TABLE 6, 1001)", "CLASS B; ADJACENT LAPS STAGGERED ≈ 1.0 m", "CLASS B TENSION; HOOPS @ s OVER THE LAP"],
    ["JOINT", "TIES CONTINUE; MAY STOP 75 BELOW BEAM BARS IF BEAMS ON 4 SIDES",
     "Av ≥ c1 s / 3fy OVER THE DEEPEST BEAM", "FULL HOOPS; ½ AND s ≤ 150 IF 4 BEAMS ≥ ¾ c"],
    ["AT FOOTING", "MIN. 3 TIES IN THE FOOTING", "MIN. 3 TIES; lo ZONE ABOVE THE FOOTING", "HOOPS ≥ 300 INTO THE FOOTING"],
    ["REFERENCE", "EIT 011008 7.10, 12.14", "DPT 1301/1302 5.2.5, 5.2.7", "DPT 1301/1302 5.2.9, 5.2.10"],
]


COL_NOTES = [
    ("1.", "THESE DETAILS APPLY WHERE THE COLUMN DRAWINGS DO NOT SHOW OTHERWISE. FRAME TYPE (ORDINARY / INTERMEDIATE / "
           "SPECIAL) AND SEISMIC CATEGORY: SEE THE DESIGN CRITERIA. TIES AND SPLICES: 1101."),
    ("2.", "TIES RB9 / DB10 MIN. (6 mm FOR ≤ DB12, 9 FOR DB16 – DB20, 10 FOR DB25 – DB28, 12 FOR ≥ DB32), CLOSED WITH "
           "135° + 6 db ≥ 75 HOOKS; HOOKS OF SUCCESSIVE TIES AT DIFFERENT CORNERS. [EIT 011008 7.10.5]"),
    ("3.", "OFFSET BARS: SLOPE ≤ 1:6, BENT BEFORE PLACING; TIES WITHIN 150 OF EACH BEND TAKE 1.5 x THE HORIZONTAL "
           "THRUST. FACE OFFSET ≥ 75: DOWELS LAPPED WITH BOTH COLUMNS. [EIT 011008 7.8.1]"),
    ("4.", "LAPS PER 1001 TABLE 6; NO LAPS FOR BARS > DB36. COUPLERS ≥ 1.25 fy, STAGGERED, 2 EXTRA TIES PER SET. "
           "[EIT 011008 12.13 – 12.16]"),
    ("5.", "ANCHOR BOLTS AT A COLUMN TOP: ≥ 2-DB12 OR 3-DB10 TIES WITHIN 125 OF THE TOP, AROUND ≥ 4 BARS. "
           "[EIT 011008 7.10.5]"),
    ("6.", "COLUMN ON A TRANSFER BEAM: BARS TO THE BEAM BOTTOM LAYER WITH 90° HOOKS OUTWARD; COLUMN TIES CONTINUE "
           "INTO THE BEAM AT THE SAME SPACING."),
    ("7.", "SPIRAL COLUMNS: SPIRAL ≥ 9 mm, CLEAR PITCH 25 – 75, 1.5 EXTRA TURNS AT EACH END, FROM THE SLAB TOP TO THE "
           "LOWEST BEAM BARS ABOVE. [EIT 011008 7.10.4]"),
]


def sheet_1101():
    ps = new_sheet(0)
    top = FY1 - 3
    x = FX0 + 1
    names = [("ORD", "COLUMN - ORDINARY MOMENT FRAME"), ("IMF", "COLUMN - INTERMEDIATE MOMENT FRAME"),
             ("SMF", "COLUMN - SPECIAL MOMENT FRAME")]
    for i, (k, nm) in enumerate(names):
        px, pw, ph = viewport(ps, k, 50, x, top)
        view_title(ps, None, top - ph - 6, nm, "1:50", (str(i + 1), "1101"))
        x = px + pw + 3
    ytab = top - ph - 22
    yb = tbl(ps, FX0 + 3, ytab, [30, 58, 62, 70],
             ["ITEM", "ORDINARY (1)", "INTERMEDIATE (2)", "SPECIAL (3)"], TIE_TABLE, "LCCC",
             title="COLUMN TIES AND SPLICES BY FRAME TYPE")
    xi = FX0 + 3 + 220 + 6
    px, pw, ph2 = viewport(ps, "INF", 100, xi, ytab + 4)
    view_title(ps, None, ytab + 4 - ph2 - 6, "COLUMN BESIDE MASONRY INFILL", "1:100", ("4", "1101"),
               note="DPT 1301/1302 5.2.5.1 (FRAMES 2, 3)")
    notes_block(ps, FX0 + 3, yb - 6, 220, "TYPICAL COLUMN NOTES", COL_NOTES)
    print(f"  table bottom {yb:.1f}")


# ======================================================================= sheet 1102
def sheet_1102():
    ps = new_sheet(1)
    top = FY1 - 3
    x = FX0 + 1
    titles = [("SC1", "SIZE CHANGE - INTERIOR, ≤ 75"), ("SC2", "SIZE CHANGE - INTERIOR, > 75"),
              ("SC3", "SIZE CHANGE - EDGE, ≤ 75"), ("SC4", "SIZE CHANGE - EDGE, > 75")]
    hmax = 0
    for i, (k, nm) in enumerate(titles):
        px, pw, ph = viewport(ps, k, 25, x, top)
        hmax = max(hmax, ph)
        view_title(ps, px + 2, top - ph - 6, nm, "1:25", (str(i + 1), "1102"))
        x = px + max(pw, 76) + 2
    top2 = top - hmax - 18
    x = FX0 + 1
    px, pw, ph1 = viewport(ps, "JP", 25, x, top2)
    view_title(ps, None, top2 - ph1 - 6, "EDGE / CORNER JOINT", "1:25", ("5", "1102"))
    x = px + pw + 3
    px, pw, ph2 = viewport(ps, "JE", 25, x, top2)
    view_title(ps, None, top2 - ph2 - 6, "SECTION A", "1:25", ("A", "1102"), triangles=True)
    x = px + pw + 3
    px, pw, ph3 = viewport(ps, "FT", 50, x, top2)
    view_title(ps, None, top2 - ph3 - 6, "STARTER BARS IN FOOTING", "1:50", ("6", "1102"))
    top3 = top2 - max(ph1, ph2, ph3) - 18
    px, pw, ph4 = viewport(ps, "RF", 50, FX0 + 1, top3)
    view_title(ps, None, top3 - ph4 - 6, "COLUMN TOP AT ROOF", "1:50", ("7", "1102"),
               note="90° HOOK 12 db AT THE ROOF TOP (OR ldh FROM THE SOFFIT); TIES TO THE TOP")
    px, pw, ph5 = viewport(ps, "TB", 50, px + pw + 10, top3)
    view_title(ps, None, top3 - ph5 - 6, "COLUMN ON A TRANSFER BEAM", "1:50", ("8", "1102"))
    px, pw, ph6 = viewport(ps, "TS", 25, px + pw + 6, top3 + 8)
    view_title(ps, None, top3 + 8 - ph6 - 6, "TYPICAL TIE ARRANGEMENTS", "1:25", ("9", "1102"),
               note="CORNER + ALTERNATE BARS HELD; CROSSTIES 135° / 90° ALTERNATING")


def build():
    views()
    sheet_1101()
    sheet_1102()
