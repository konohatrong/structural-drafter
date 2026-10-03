"""
Typical column details R2 (N.T.S., typical members of members.py, dummy 1:25) - STR-ST-1101 (ties and
splice zones), STR-ST-1102 (size change, joints, footing), STR-ST-1103 (tie types, circular columns, mechanical
splices), STR-ST-1104 (column ends and special cases: roof, transfer beam, discontinued wall, masonry infill).
Sources : EIT 011008-21 ch. 7, 12; DPT 1301/1302-61 cl. 5.2.5 - 5.2.10; TATA RC detailing handbook (column chapter).
"""
from drafter.td_engine import *
import issue                     # noqa: F401  title-block issue data (stage, revision, status)
from members import *

BASE = "STR-ST-1101_Typical_Column_Details_A3_R2"
SHEETS[:] = [("1101", ["TYPICAL COLUMN DETAILS (1)", "TIES AND SPLICE ZONES"], "N.T.S."),
             ("1102", ["TYPICAL COLUMN DETAILS (2)", "SIZE CHANGE, JOINTS, FOOTING"], "N.T.S."),
             ("1103", ["TYPICAL COLUMN DETAILS (3)", "TIE TYPES AND SPLICES"], "N.T.S."),
             ("1104", ["TYPICAL COLUMN DETAILS (4)", "COLUMN ENDS, SPECIAL CASES"], "N.T.S.")]


# ======================================================================= TYPICAL COLUMN DETAILS
# Drawing rule: normal (2.0 / 2.8 text, 2 mm arrows) - these are detail sheets, not the notes sheet.
# Sources: EIT 011008-21 (ch. 7, 12), DPT 1301/1302-61 (5.2.5 - 5.2.10), TATA / Jiravacharadet RC detailing
# handbook (column chapter, typical sheets). Values are symbolic (lo, s0, s) - numbers are in the tables.
# COL, CVR, DT, DBM and the drawn lengths come from members.py (one catalogue for every sheet)
XB = CVR + DT + DBM / 2        # 59  main bar centre from column face
XT = CVR + DT / 2              # 44.5 tie centreline from face
HB = BEAM_H                    # beam depth 600
HC = STOREY_D                  # clear storey height drawn (N.T.S.)
BST = 200                      # beam stub drawn each side
GAP = 50                       # drawn offset of lapped bars (schematic)
LAPD = LAP_D                   # drawn lap length (members.py)
LO = LO_D                      # drawn lo


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
            line(sp, P(-BST, yt), P(0, yt), "S-CONC-VIS")
            line(sp, P(-BST, yb), P(0, yb), "S-CONC-VIS")
            nf_hatch(sp, rect(P, -BST, yb, 0, yt), 25)
            zbreak(sp, P(-BST, yb - 80), P(-BST, yt + 80), 50)
        if right:
            line(sp, P(width, yt), P(width + BST, yt), "S-CONC-VIS")
            line(sp, P(width, yb), P(width + BST, yb), "S-CONC-VIS")
            nf_hatch(sp, rect(P, width, yb, width + BST, yt), 25)
            zbreak(sp, P(width + BST, yb - 80), P(width + BST, yt + 80), 50)


def col_faces(sp, P, spans, width=COL, left=True, right=True):
    for y0, y1 in spans:
        if left:
            line(sp, P(0, y0), P(0, y1), "S-CONC")
        if right:
            line(sp, P(width, y0), P(width, y1), "S-CONC")


# ----------------------------------------------------------------------- 1101: column elevations by frame type
def col_elev(ox, oy, kind):
    """one storey of an interior column, beams both sides, for kind ORD / IMF / SMF (N.T.S.)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    ybot, ytop = -HB - 250, HC + HB + 250
    col_faces(sp, P, [(ybot, -HB), (0, HC), (HC + HB, ytop)])
    beams_elev(sp, P, [-HB, HC])
    zbreak(sp, P(-60, ybot), P(COL + 60, ybot), S)
    zbreak(sp, P(-60, ytop), P(COL + 60, ytop), S)
    xl, xr = XB, COL - XB

    if kind == "ORD":                 # lap just above the floor, both faces; lower bars stop at the lap top
        laps = [(0, LAPD), (0, LAPD)]
    elif kind == "IMF":               # mid zone, adjacent laps staggered ~1.0 m
        laps = [(550, 550 + LAPD), (1300, 1300 + LAPD)]
    else:                             # centre half of Hc only
        laps = [(HC / 2 - LAPD / 2, HC / 2 + LAPD / 2)] * 2
    slope = 6 if kind == "ORD" else 10
    for (y0, y1), xf, inw in ((laps[0], xl, 1), (laps[1], xr, -1)):
        xi = xf + inw * GAP
        if kind == "ORD":             # lap at the floor: the LOWER bars are cranked inside the joint (top bend 75
            yk, yk2 = -75, HC + HB - 75                    # below the slab top), the lapped bars run straight
            rbar(sp, [P(xf, ybot), P(xf, yk - GAP * slope), P(xi, yk), P(xi, y1)])            # from below
            rbar(sp, [P(xf, y0), P(xf, yk2 - GAP * slope), P(xi, yk2), P(xi, ytop)])          # this storey
            rbar(sp, [P(xf, HC + HB), P(xf, ytop)])                                         # next storey
            continue
        rbar(sp, [P(xf, ybot), P(xf, y1)])                                    # bar from below, ends at lap top
        (cx0, cy0), (cx1, cy1) = crank(xi, xf, y1 + GAP * slope, slope)
        rbar(sp, [P(xi, y0), P(xi, y1), P(xf, y1 + GAP * slope), P(xf, ytop)])

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
    # all on the LEFT (nothing between the column and its notes). Tiers: a dimension lying inside another's
    # span sits nearer the column, so no extension line crosses a dimension line:
    # lap / splice (inner), then the lo - MID ZONE - lo chain, then Hc (outer)
    xd = -BST - 100
    if kind == "SMF":
        dim(sp, P(0, HC / 4), P(0, 3 * HC / 4), P(xd, 0), S, angle=90, text="SPLICE ZONE, CENTRE Hc/2")
    elif kind == "IMF":
        dim(sp, P(0, laps[0][0]), P(0, laps[1][0]), P(xd, 0), S, angle=90, text="≈ 1.0 m")
    else:
        dim(sp, P(0, 0), P(0, LAPD), P(xd, 0), S, angle=90, text="LAP")
    if kind != "ORD":
        dim(sp, P(0, 0), P(0, LO), P(xd - 180, 0), S, angle=90, text="lo")
        dim(sp, P(0, LO), P(0, HC - LO), P(xd - 180, 0), S, angle=90, text="MID ZONE")
        dim(sp, P(0, HC - LO), P(0, HC), P(xd - 180, 0), S, angle=90, text="lo")
    dim(sp, P(0, 0), P(0, HC), P(xd - (360 if kind != "ORD" else 180), 0), S, angle=90, text="Hc (CLEAR)")

    # ---- notes (right column)
    note_cfg(xR=P(COL + BST + 150, 0)[0], yminR=P(0, ybot)[1])
    kr = P(COL + BST + 150, 0)
    R = lambda tip, s, **kw: leader(sp, P(*tip), kr, s, S, "R", 36, **kw)
    if kind == "ORD":
        R((COL / 2, HC + 150), "TIES CONTINUE THROUGH THE JOINT; MAY STOP 75 mm BELOW THE LOWEST BARS OF THE "
                               "SHALLOWEST BEAM WHERE BEAMS FRAME ON 4 SIDES")
        R((COL / 2, HC - 150), "LAST TIE ≤ s/2 BELOW THE BEAM SOFFIT")
        R((COL / 2, 1500), "TIES @ s ≤ 16 db, 48 dt AND LEAST COLUMN SIZE")
        R((xl + GAP, 400), f"LAP ABOVE THE FLOOR ({TAB('LAPS')}); CLASS B, OR COMPRESSION LAP IF NEVER IN TENSION")
        R((COL / 2, 150), "FIRST TIE ≤ s/2 ABOVE THE FLOOR")
        R((xl + GAP / 2, -75 - GAP * 3), "OFFSET BEND ≤ 1:6 INSIDE THE JOINT, TOP BEND ≤ 75 mm BELOW THE SLAB TOP")
    elif kind == "IMF":
        R((COL / 2, HC + 225), "JOINT HOOPS Av ≥ c1 s / 3fy OVER THE DEEPEST BEAM (OMIT ONLY IF CONFINED ON 4 SIDES "
                               "AND NOT IN THE SEISMIC SYSTEM)")
        R((COL / 2, HC - 75), "FIRST HOOP ≤ s0/2 FROM THE JOINT FACE")
        R((COL / 2, HC - 225), "HOOPS @ s0 WITHIN lo")
        R((xr - GAP, laps[1][1] - 100), "LAPS IN THE MID ZONE ONLY, OUTSIDE lo; ADJACENT LAPS STAGGERED ≈ 1.0 m")
        R((COL / 2, 1225), "HOOPS @ ≤ 2 s0 OUTSIDE lo")
        R((xl + GAP / 2, laps[0][1] + 250), "OFFSET BEND ≤ 1:10")
        R((COL / 2, 75), "FIRST HOOP ≤ s0/2 ABOVE THE FLOOR")
    else:
        R((COL / 2, HC + 250), "JOINT: FULL CONFINING HOOPS; ½ OF THEM AND s ≤ 150 mm WHERE 4 BEAMS ≥ ¾ COLUMN WIDTH")
        R((COL / 2, HC - 250), "CONFINING HOOPS @ s WITHIN lo, FIRST ≤ s/2 FROM THE FACE; Ash PER DPT EQ. 5.2-14, 5.2-15")
        R((xl + GAP, HC / 2), "TENSION LAP (CLASS B) IN THE CENTRE HALF ONLY; HOOPS @ s OVER THE LAP")
        R((COL / 2, 700), "HOOPS @ ≤ 6 db AND 150 OUTSIDE lo")
        R((COL / 2, -HB - 150), "BELOW THE BEAM THE lo ZONE REPEATS; HOOPS ≥ 300 mm INTO A FOOTING")


# ----------------------------------------------------------------------- 1101: columns next to masonry infill
def infill(ox, oy):
    S = 25
    sp = msp
    HC = 2000                                          # storey drawn shorter here (N.T.S.)
    note_cfg(free=True)
    for k, case in enumerate(("PART", "ONE")):
        P = (lambda x, y, k=k: (ox + k * 1800 + x, oy + y))
        ybot, ytop = -HB - 100, HC + HB + 100
        col_faces(sp, P, [(ybot, -HB), (0, HC), (HC + HB, ytop)])
        beams_elev(sp, P, [-HB, HC])
        if case == "PART":
            for x0, x1 in ((-400, 0), (COL, COL + 400)):
                pline(sp, [P(x0, 0), P(x0, 900), P(x1, 900), P(x1, 0)], "S-CONC-VIS")
                hatch(sp, [P(x0, 0), P(x0, 900), P(x1, 900), P(x1, 0)], "AR-BRSTD", 1.0)   # masonry: brick
            ys = rng(75, HC - 75, 150)
            lab = ["(a) PARTIAL-HEIGHT INFILL", "HOOPS @ s0 OVER THE FULL HEIGHT;",
                   "SHEAR FOR THE SHORT COLUMN;", "HOOPS ≥ c1 INTO THE WALL ZONE"]
        else:
            x0, x1 = -400, 0
            pline(sp, [P(x0, 0), P(x0, HC), P(x1, HC), P(x1, 0)], "S-CONC-VIS")
            hatch(sp, [P(x0, 0), P(x0, HC), P(x1, HC), P(x1, 0)], "AR-BRSTD", 1.0)       # masonry: brick
            ys = rng(75, LO, 150) + [HC - y for y in rng(75, LO, 150)] + rng(LO + 300, HC - LO - 150, 250)
            lab = ["(b) FULL INFILL ON ONE SIDE", "lo ZONES @ s0;", "MID ZONE ≤ 2 s0 AND ≤ d/2", ""]
        ties(sp, P, XT, COL - XT, ys)
        for xf in (XB, COL - XB):
            rbar(sp, [P(xf, ybot), P(xf, ytop)])
        for i, t in enumerate(lab):
            if t:
                text(sp, t, P(-400, ybot - 150 - i * 90), 2.0 * S, style="ANB" if i == 0 else "AN")


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
            line(sp, P(x0, 0), P(x1, 0), "S-CONC-VIS")
            line(sp, P(x0, -HB), P(x1, -HB), "S-CONC-VIS")
            nf_hatch(sp, rect(P, x0, -HB, x1, 0), S)
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
        if off < 75:
            h = abs(xi - xl_bar)
            v = 6 * h
            rbar(sp, [P(xl_bar, ybot), P(xl_bar, -v), P(xi, 0), P(xi, LAPD)])
            if side == 1 or case in ("INT_S", "EDGE_S"):
                notes.append(("CRANK", xl_bar + (xi - xl_bar) * 0.5, -v / 2))
        else:
            rbar(sp, [P(xl_bar, ybot), P(xl_bar, -50), P(xl_bar + inw * 200, -50)])  # 50 below the top, hooked in
            rbar(sp, [P(xi, -HB - 450), P(xi, LAPD)], layer="S-REBR")               # dowel
            notes.append(("DOWEL", xi, -HB - 250))
    # ties: lower column (normal s + 2 extra at the bends), joint @ <= 150, upper column
    ties(sp, P, XT, Bl - XT, [-HB - 375, -HB - 150, -HB - 75])
    ties(sp, P, XT, Bl - XT, [-HB + 75, -375, -225, -75])
    ties(sp, P, xu0 + XT, xu0 + Bu - XT, [75, 375, 675])
    # dimension of the offset (at the step)
    # small offset: text outside the extension lines, away from the upper column face
    if case == "INT_S":
        dim(sp, P(0, 150), P(xu0, 150), P(0, 330), S, text="< 75", tside="L")
    elif case == "INT_L":
        dim(sp, P(0, 150), P(xu0, 150), P(0, 330), S, text="≥ 75", tside="L")
    elif case == "EDGE_S":
        dim(sp, P(xu0 + Bu, 150), P(Bl, 150), P(0, 330), S, text="< 75", tside="R")
    else:
        dim(sp, P(xu0 + Bu, 150), P(Bl, 150), P(0, 330), S, text="≥ 75", tside="R")
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
            Rn((Bl - XB, -120), "LOWER BARS STOP 50 mm BELOW THE TOP, 90° HOOK INWARD")
            break
    Rn((Bl / 2, -300), "TIES @ ≤ 150 mm THROUGH THE JOINT")
    if case in ("INT_S", "EDGE_S"):                                          # only where bars are cranked
        Rn((Bl / 2, -HB - 110), "2 EXTRA TIES WITHIN 150 mm OF THE BEND")
    Rn((xu0 + XB + GAP, 500), f"LAP PER {TAB('TIES')}")


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
    ybot, ytop = -HB - 280, 500                                                     # stub below: 2 ties, then the break
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
    # one chain below the column break, clear of the ties; "≤ 50" with its text outside, right
    dim(sp, P(COL, -HB), P(xe - 10, -HB), P(0, ybot - 110), S, text="ldh")
    dim(sp, P(COL, -HB + 30), P(COL + 50, -HB + 30), P(0, ybot - 110), S, text="≤ 50", tside="R")
    note_cfg(xR=P(COL + 1150, 0)[0], yminR=P(0, -HB + 40)[1], upR=True)          # notes above the dimensions
    kr = P(COL + 1150, 0)
    R = lambda tip, s: leader(sp, P(*tip), kr, s, S, "R", 44)
    R((COL + 600, yt_b), "BEAM BARS RUN TO THE FAR SIDE OF THE COLUMN CORE; 90° HOOKS TURNED INTO THE JOINT: TOP "
                         "BARS DOWN, BOTTOM BARS UP")
    R((xe, -300), "HOOK TAILS INSIDE THE FAR-FACE COLUMN BARS")
    R((COL / 2, -225), "COLUMN TIES CONTINUE THROUGH THE JOINT @ ≤ 150 mm (SPECIAL FRAMES: CONFINING HOOPS @ s)")
    R((COL + 50, -HB + 200), "FIRST BEAM STIRRUP ≤ 50 mm FROM THE COLUMN FACE")


# ----------------------------------------------------------------------- 1102: column top at roof
def roof_top(ox, oy):
    S = 25
    sp = msp
    note_cfg(free=True)
    for k, edge in enumerate((False, True)):
        P = (lambda x, y, k=k: (ox + k * 1900 + x, oy + y))
        ybot = -HB - 450
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
        nf_hatch(sp, rect(P, COL, -HB, COL + BST, 0), S)                             # roof beams: not the subject
        if not edge:
            nf_hatch(sp, rect(P, -BST, -HB, 0, 0), S)
        L = 12 * DBM + 60
        yh = -50 - 10
        for xf, d in ((XB, -1), (COL - XB, 1)):
            dd = d if not edge else 1                                                   # edge: both hooks inward
            rbar(sp, [P(xf, ybot), P(xf, yh), P(xf + dd * L, yh)])
        ties(sp, P, XT, COL - XT, [-HB - 150, -HB - 350] + rng(-HB + 150, -150, 150))
        lab = ("(a) INTERIOR: HOOKS OUTWARD" if not edge else "(b) EDGE / CORNER: HOOKS INWARD")
        text(sp, lab, P(-BST, ybot - 150), 2.0 * S, style="ANB")


# ----------------------------------------------------------------------- 1102: column on a transfer beam
def on_beam(ox, oy):
    """column planted on a beam: bars to the beam bottom layer with 90 deg hooks outward, ties continue (1:50)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    Db, Lb = HB, 1800                                  # typical beam 600 (members.py)
    x0 = (Lb - COL) / 2
    line(sp, P(0, 0), P(x0, 0), "S-CONC")
    line(sp, P(x0 + COL, 0), P(Lb, 0), "S-CONC")
    line(sp, P(0, -Db), P(Lb, -Db), "S-CONC")
    zbreak(sp, P(0, -Db - 80), P(0, 80), S)
    zbreak(sp, P(Lb, -Db - 80), P(Lb, 80), S)
    line(sp, P(x0, 0), P(x0, 1000), "S-CONC")
    line(sp, P(x0 + COL, 0), P(x0 + COL, 1000), "S-CONC")
    zbreak(sp, P(x0 - 60, 1000), P(x0 + COL + 60, 1000), S)
    yb = -Db + 60
    nf_hatch(sp, rect(P, 0, -Db, Lb, 0), S)                                         # the beam: not the subject
    rbar(sp, [P(60, yb), P(Lb - 60, yb)], 25, layer="S-REBR-NF")
    rbar(sp, [P(60, -60), P(Lb - 60, -60)], 25, layer="S-REBR-NF")
    L = 12 * DBM + 60
    yh = yb + 45
    for xf, d in ((x0 + XB, -1), (x0 + COL - XB, 1)):
        rbar(sp, [P(xf, 1000), P(xf, yh), P(xf + d * L, yh)])
    ties(sp, P, x0 + XT, x0 + COL - XT, rng(-Db + 150, -150, 150) + rng(75, 900, 300))
    note_cfg(xR=P(Lb + 250, 0)[0])
    kr = P(Lb + 250, 0)
    R = lambda tip, s: leader(sp, P(*tip), kr, s, S, "R", 40)
    R((x0 + COL - XB, -300), "COLUMN BARS TO THE BEAM BOTTOM LAYER, 90° HOOKS OUTWARD ON THE BOTTOM BARS")
    R((x0 + COL / 2, -450), "COLUMN TIES CONTINUE INTO THE BEAM AT THE SAME SPACING")
    R((x0 + COL / 2, 75), "FIRST TIE ≤ s/2 ABOVE THE BEAM")


# ----------------------------------------------------------------------- 1102: column under a discontinued wall
def under_wall(ox, oy):
    """column carrying a wall that stops above it (DPT 5.2.9.4.5, ACI COL-104), 1:50: full-height confinement
    below the discontinuity, hoops >= ld into the wall and >= 300 into the footing; storey height broken"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    Tf, yb1, yb2, ybm = FOOT_T, 350, 480, 900         # footing depth; break gap 350 - 480; beam soffit
    Hb, Lw, LDw = HB, 900, 600                        # transfer beam depth; wall / beam drawn left of the column; ld
    ywl, ytop = ybm + Hb, ybm + Hb + 800               # wall base (top of beam); wall drawn to
    # footing
    pline(sp, [P(-350, 0), P(-350, -Tf), P(COL + 350, -Tf), P(COL + 350, 0)], "S-CONC")
    line(sp, P(-350, 0), P(0, 0), "S-CONC")
    line(sp, P(COL, 0), P(COL + 350, 0), "S-CONC")
    zbreak(sp, P(-350, -Tf - 60), P(-350, 60), S)
    zbreak(sp, P(COL + 350, -Tf - 60), P(COL + 350, 60), S)
    pline(sp, [P(-400, -Tf - 50), P(COL + 400, -Tf - 50)], "S-LEAN")
    yf = -Tf + 75 + 8
    rbar(sp, [P(-350, yf), P(COL + 350, yf)], 16, layer="S-REBR-NF")
    nf_hatch(sp, rect(P, -350, -Tf, COL + 350, 0), S)                               # footing, beam, wall: not the
    nf_hatch(sp, rect(P, -Lw, ybm, 0, ytop), S)                                     # subject of the detail
    # column (height broken); transfer beam and wall to the LEFT, so the notes on the right reach the column
    for y0, y1 in ((0, yb1), (yb2, ybm)):
        line(sp, P(0, y0), P(0, y1), "S-CONC")
    line(sp, P(COL, 0), P(COL, yb1), "S-CONC")
    line(sp, P(COL, yb2), P(COL, ytop), "S-CONC")    # outer face: column, beam end and wall end in one line
    for y in (yb1, yb2):
        zbreak(sp, P(-60, y), P(COL + 60, y), S)
    line(sp, P(-Lw, ybm), P(0, ybm), "S-CONC")
    line(sp, P(-Lw, ywl), P(0, ywl), "S-CONC")
    zbreak(sp, P(-Lw, ybm - 60), P(-Lw, ytop + 60), S)
    zbreak(sp, P(-Lw, ytop), P(COL + 60, ytop), S)
    # column bars: hooked in the footing, through the beam, >= ld into the wall
    L = 12 * DBM + 60
    yh = yf + 45
    for xf, d, dy in ((XB, 1, 0), (COL - XB, -1, 45)):  # special frame fixed at the base: hooks toward the centre
        rbar(sp, [P(xf, yb1), P(xf, yh + dy), P(xf + d * L, yh + dy)])
        rbar(sp, [P(xf, yb2), P(xf, ywl + LDw + 100)])
    # hoops at s0 (drawn 100): footing (to 300 down), full height, through the beam, ld into the wall
    ys = [-100, -200, -300] + rng(50, yb1 - 30, 100) + rng(yb2 + 50, ywl + LDw, 100)
    ties(sp, P, XT, COL - XT, ys)
    dim(sp, P(XT, 0), P(XT, -300), P(-200, 0), S, angle=90, text="≥ 300")
    dim(sp, P(0, ywl), P(0, ywl + LDw), P(-250, 0), S, angle=90, text="≥ ld")      # inside the wall
    text(sp, "TRANSFER", P(-Lw + 80, ybm + Hb / 2 + 15), 2.0 * S)
    text(sp, "BEAM", P(-Lw + 80, ybm + Hb / 2 - 15), 2.0 * S, align=TA.TOP_LEFT)
    note_cfg(xR=P(COL + 500, 0)[0])
    kr = P(COL + 500, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 46, **kw)
    R((COL, ytop - 60), "WALL ABOVE, DISCONTINUED BELOW")
    R((COL - XB, ywl + LDw + 50), "COLUMN BARS ≥ ld INTO THE WALL")
    # hoop tips at the hoop end, on a hoop level: the horizontal leader run then crosses no hoop line
    R((COL - XT, ywl + 330), "HOOPS THROUGH THE BEAM, ≥ ld (LARGEST COLUMN BAR) INTO THE WALL")
    R((COL - XT, 730), "HOOPS @ s0 OVER THE FULL HEIGHT OF EVERY STOREY BELOW THE WALL")
    R((COL - XT, -200), "HOOPS ≥ 300 mm INTO THE FOOTING (ON A WALL: ≥ ld)")


# ----------------------------------------------------------------------- 1102: starter bars in footing
def footing(ox, oy):
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    Bf, Tf = FOOT_B, FOOT_T
    xc0 = (Bf - COL) / 2
    pline(sp, [P(0, -Tf), P(Bf, -Tf), P(Bf, 0), P(xc0, 0)], "S-CONC")
    line(sp, P(xc0 + COL, 0), P(Bf, 0), "S-CONC")
    line(sp, P(0, 0), P(xc0, 0), "S-CONC")
    line(sp, P(0, -Tf), P(0, 0), "S-CONC")
    pline(sp, [P(-50, -Tf - 50), P(Bf + 50, -Tf - 50)], "S-LEAN")
    line(sp, P(xc0, 0), P(xc0, 1000), "S-CONC")
    line(sp, P(xc0 + COL, 0), P(xc0 + COL, 1000), "S-CONC")
    zbreak(sp, P(xc0 - 60, 1000), P(xc0 + COL + 60, 1000), S)
    yb1 = -Tf + 75 + 10
    nf_hatch(sp, rect(P, 0, -Tf, Bf, 0), S)                                         # the footing: not the subject
    rbar(sp, [P(75, -Tf + 170), P(75, yb1), P(Bf - 75, yb1), P(Bf - 75, -Tf + 170)], 16, layer="S-REBR-NF")
    for x in rng(150, Bf - 150, 200):
        dot(sp, P(x, yb1 + 26), rdot(16, S), "S-REBR-NF")
    L = 12 * DBM + 60
    yh = yb1 + 50
    for xf, d in ((xc0 + XB, -1), (xc0 + COL - XB, 1)):
        rbar(sp, [P(xf, 1000), P(xf, yh), P(xf + d * L, yh)])
    ties(sp, P, xc0 + XT, xc0 + COL - XT, [-150, -300, -450] + rng(75, 900, 300))
    note_cfg(xR=P(Bf + 350, 0)[0])
    kr = P(Bf + 350, 0)
    R = lambda tip, s: leader(sp, P(*tip), kr, s, S, "R", 44)
    R((xc0 + COL / 2, 75), f"FIRST TIE ≤ s/2 (lo ZONE: ≤ s0/2) ABOVE THE FOOTING; LAP ZONE PER {TAB('TIES')}")
    R((xc0 + COL / 2, -300), "MIN. 3 TIES IN THE FOOTING; SPECIAL FRAMES: HOOPS ≥ 300 mm INTO IT (FULL DEPTH AT AN "
                             "EDGE WITHIN h/2)")
    R((xc0 + COL - XB + L / 2, yh), "DOWELS = COLUMN BARS TO THE BOTTOM MAT, 90° HOOK OUTWARD (INWARD AT A PROPERTY "
                                    "LINE; TOWARD THE CENTRE IN SPECIAL FRAMES FIXED AT THE BASE); STRAIGHT ≥ ldc")


# ----------------------------------------------------------------------- 1103: tie types, circular columns, splices
# Tie types: letter, drawn W x H (mm), bars per top/bottom face (nx), bars per side face (ny), corners included.
# Perimeter tie + crossties on alternate intermediate bars (the first one held): every corner and alternate bar is
# held and, at these sizes, no bar is more than 150 clear from a held bar (EIT 011008 7.10.5.3).
TIE_TYPES = [("A", 300, 300, 2, 2), ("B", 300, 450, 2, 3), ("C", 400, 400, 3, 3), ("D", 400, 600, 3, 4),
             ("E", 500, 500, 4, 4), ("F", 400, 700, 3, 6), ("G", 600, 600, 5, 5), ("H", 700, 700, 6, 6),
             ("J", 800, 800, 7, 7)]
TIE_HIGH = ("EH", 500, 500, 4, 4, True)                 # D5 variant: every perimeter bar held (1103 note 6)


def tie_type(sp, P, W, H, nx, ny, S, allheld=False):
    """one tie type in section: perimeter tie + crossties on alternate intermediate bars; returns no. of crossties.
    allheld (D5, ACI 318-19 18.7.5.2(f)): a crosstie on EVERY intermediate bar, 135 deg hooks at both ends"""
    c = XB
    xs = [c + i * (W - 2 * c) / (nx - 1) for i in range(nx)]
    ys = [c + i * (H - 2 * c) / (ny - 1) for i in range(ny)]
    rb = rdot(DBM, S)
    R_ = rb + DT / 2
    cor = lambda x, y: (P(x, y)[0], P(x, y)[1], R_)
    pline(sp, [P(0, 0), P(W, 0), P(W, H), P(0, H)], "S-CONC", close=True)
    stirrup(sp, cor(c, H - c), cor(W - c, H - c), cor(W - c, c), cor(c, c), 6 * DT + 20)
    hx, hy = (xs[1:-1], ys[1:-1]) if allheld else (xs[1:-1][0::2], ys[1:-1][0::2])
    j = 0
    for x in hx:                                       # crossties top - bottom; 90 deg ends alternate
        a, b = (P(x, H - c), P(x, c)) if j % 2 == 0 else (P(x, c), P(x, H - c))
        crosstie(sp, a, b, R_ + max(DT, 0.5 * S), 6 * DT + 20, both135=allheld)
        j += 1
    for y in hy:                                       # crossties side - side
        a, b = (P(c, y), P(W - c, y)) if j % 2 == 0 else (P(W - c, y), P(c, y))
        crosstie(sp, a, b, R_ + max(DT, 0.5 * S), 6 * DT + 20, both135=allheld)
        j += 1
    bars = {(round(x, 2), round(yy, 2)) for x in xs for yy in (c, H - c)}
    bars |= {(round(xx, 2), round(y, 2)) for y in ys for xx in (c, W - c)}
    for x, y in bars:
        dot(sp, P(x, y), rb)
    return j


def tie_types(ox, oy):
    """1103/1: lettered tie types A - J (1:25), two rows, sections on a common base line, labels below"""
    S = 25
    sp = msp
    note_cfg(free=True)
    y = 0
    for row in (TIE_TYPES[:5], TIE_TYPES[5:] + [TIE_HIGH]):
        hmax = max(t[2] for t in row)
        x = 0
        for L, W, H, nx, ny, *hi in row:
            P = lambda xx, yy, x=x, y=y, hmax=hmax: (ox + x + xx, oy + y - hmax + yy)
            n = tie_type(sp, P, W, H, nx, ny, S, allheld=bool(hi))
            nb = 2 * nx + 2 * ny - 4
            lab = [f"TYPE {L}", f"{nb} BARS ({nx} × {ny})", "TIE" if n == 0 else f"TIE + {n} CROSSTIE" + ("S" if n > 1 else "")]
            if hi:
                lab = [f"TYPE {L} (NOTE 6)", f"{nb} BARS, ALL HELD", f"TIE + {n} CROSSTIES,", "135° BOTH ENDS"]
            for k, t in enumerate(lab):
                text(sp, t, P(0, -170 - k * 110), 2.0 * S, style="ANB" if k == 0 else "AN")
            x += max(W, 900) + 250
        y -= hmax + 650


def circ_hoop(ox, oy):
    """1103/2: circular column with a circular hoop - ends overlapped, 135 deg hooks round a bar (1:25)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    D = 500
    sp.add_circle(P(0, 0), D / 2, dxfattribs=A("S-CONC"))
    rb = rdot(DBM, S)
    rbc = D / 2 - XB                                   # bar centres
    rh = rbc + rb + DT / 2                             # hoop centreline wraps the bars
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        dot(sp, P(rbc * math.cos(a), rbc * math.sin(a)), rb)
    a0, ov = 67.5, 45.0                                # overlap 45 deg = 0.785 x 205 = 160 >= 150
    sp.add_arc(P(0, 0), rh, a0, a0 + 360 - 0.01, dxfattribs=A("S-REBR-SEC"))
    ri = rh - 1.6 * DT                                 # the overlapping end, just inside
    sp.add_arc(P(0, 0), ri, a0, a0 + ov, dxfattribs=A("S-REBR-SEC"))
    leg = 6 * DT + 20
    for ang, r_, sgn in ((a0, rh, 1), (a0 + ov, ri, -1)):  # 135 deg hook tails into the core, round the bar
        t = math.radians(ang)
        ex, ey = r_ * math.cos(t), r_ * math.sin(t)
        d = math.radians(ang + 180 + sgn * 45)
        line(sp, P(ex, ey), P(ex + leg * math.cos(d), ey + leg * math.sin(d)), "S-REBR-SEC")
    note_cfg(xR=P(D / 2 + 250, 0)[0])
    kr = P(D / 2 + 250, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 40, **kw)
    t = math.radians(a0 + ov / 2)
    R((rh * math.cos(t), rh * math.sin(t)), "HOOP ENDS OVERLAP ≥ 150 mm, 135° HOOKS ROUND A BAR; OVERLAPS OF "
                                            "SUCCESSIVE HOOPS STAGGERED ROUND THE COLUMN")
    R((rbc * math.cos(math.radians(-22.5)), rbc * math.sin(math.radians(-22.5))), "≥ 6 BARS, EQUALLY SPACED")


def spiral_elev(ox, oy):
    """1103/3: spiral column elevation between floors (1:25), front turns only"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    D, Hs, ts = 500, 1200, 200                          # column dia., clear height drawn, slab
    r = D / 2
    rs = r - CVR - 5                                   # spiral centreline
    for yy in (0, Hs):                                  # slabs above and below
        y0, y1 = (yy - ts, yy) if yy == 0 else (yy, yy + ts)
        for y_ in (y0, y1):
            face = (yy == Hs and y_ == y0) or (yy == 0 and y_ == y1)     # slab face against the column
            line(sp, P(-r - 250, y_), P(-r, y_) if face else P(r + 250, y_), "S-CONC")
            if face:
                line(sp, P(r, y_), P(r + 250, y_), "S-CONC")
        zbreak(sp, P(-r - 250, y0 - 50), P(-r - 250, y1 + 50), S)
        nf_hatch(sp, rect(P, -r - 250, y0, -r, y1), S)                              # slabs: not the subject
        nf_hatch(sp, rect(P, r, y0, r + 250, y1), S)
        zbreak(sp, P(r + 250, y0 - 50), P(r + 250, y1 + 50), S)
    line(sp, P(-r, 0), P(-r, Hs), "S-CONC")
    line(sp, P(r, 0), P(r, Hs), "S-CONC")
    line(sp, P(-r, -ts), P(-r, -ts - 250), "S-CONC")
    line(sp, P(r, -ts), P(r, -ts - 250), "S-CONC")
    line(sp, P(-r, Hs + ts), P(-r, Hs + ts + 250), "S-CONC")
    line(sp, P(r, Hs + ts), P(r, Hs + ts + 250), "S-CONC")
    zbreak(sp, P(-r - 60, -ts - 250), P(r + 60, -ts - 250), S)
    zbreak(sp, P(-r - 60, Hs + ts + 250), P(r + 60, Hs + ts + 250), S)
    for x in (-(r - XB), 0, r - XB):                    # longitudinal bars
        rbar(sp, [P(x, -ts - 250), P(x, Hs + ts + 250)])
    pitch = 85                                         # clear 75 + spiral dia.
    y = -1.5 * pitch                                   # 1.5 extra turns below the slab top ...
    top = Hs + 1.5 * pitch                             # ... and above the soffit (to the lowest bars above)
    while y < top:
        line(sp, P(-rs, y), P(rs, y + pitch / 2), "S-REBR-SEC")   # front half-turn
        y += pitch
    dim(sp, P(r, 600), P(r, 600 + pitch), P(r + 120, 0), S, angle=90, text="s", tside="R")
    note_cfg(xR=P(r + 500, 0)[0], yminR=P(0, -ts)[1], upR=True)
    kr = P(r + 500, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 40, **kw)
    R((0, Hs + 1.5 * pitch - 20), "1.5 EXTRA TURNS AT EACH END; UP TO THE LOWEST BARS OF THE MEMBERS ABOVE "
                                  "(NO BEAMS ON ALL SIDES: TIES ON TO THE SLAB SOFFIT)")
    R((rs * 0.5, 850 + pitch * 0.25), "SPIRAL ≥ 9 mm, CLEAR PITCH s 25 – 75 mm AND ≥ 4/3 MAX. AGGREGATE")
    R((-rs * 0.3, 350 + pitch * 0.35), "LAPS 48 db (DB) / 72 db (RB), OR A MECHANICAL / WELDED SPLICE")
    R((0, -1.5 * pitch + 30), "1.5 EXTRA TURNS FROM THE SLAB TOP")


def couplers(ox, oy):
    """1103/4: mechanical splices in a column (elevation of one face, 1:25)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    W, top, ts = 500, 1700, 200
    line(sp, P(0, 0), P(0, top), "S-CONC")
    line(sp, P(W, 0), P(W, top), "S-CONC")
    for x0, x1 in ((-250, 0), (W, W + 250)):            # floor slab
        line(sp, P(x0, 0), P(x1, 0), "S-CONC")
        line(sp, P(x0, -ts), P(x1, -ts), "S-CONC")
        zbreak(sp, P(x0 if x0 < 0 else x1, -ts - 50), P(x0 if x0 < 0 else x1, 50), S)
        nf_hatch(sp, rect(P, x0, -ts, x1, 0), S)                                    # floor slab: not the subject
    line(sp, P(0, -ts), P(0, -ts - 250), "S-CONC")
    line(sp, P(W, -ts), P(W, -ts - 250), "S-CONC")
    zbreak(sp, P(-60, -ts - 250), P(W + 60, -ts - 250), S)
    zbreak(sp, P(-60, top), P(W + 60, top), S)
    c = XB
    xs = [c + i * (W - 2 * c) / 3 for i in range(4)]
    lv = [500, 1100]                                   # splice levels: alternate bars, staggered >= 600
    cw, cl = 34, 70                                    # coupler outside dia. / length (drawn)
    for i, x in enumerate(xs):
        yc = lv[i % 2]
        rbar(sp, [P(x, -ts - 250), P(x, yc - cl / 2)])
        rbar(sp, [P(x, yc + cl / 2), P(x, top)])
        pline(sp, [P(x - cw / 2, yc - cl / 2), P(x + cw / 2, yc - cl / 2), P(x + cw / 2, yc + cl / 2),
                   P(x - cw / 2, yc + cl / 2)], "S-REBR", close=True)
    ys = [y for y in rng(75, top - 50, 150) if all(abs(y - l_) > 90 for l_ in lv)]
    ys += [l_ + sg * (cl / 2 + 30) for l_ in lv for sg in (-1, 1)]                 # a tie just above / below
    ties(sp, P, XT, W - XT, sorted(ys))
    dim(sp, P(0, lv[0]), P(0, lv[1]), P(-250, 0), S, angle=90, text="≥ 600")
    dim(sp, P(0, lv[0]), P(c - cw / 2, lv[0]), P(0, lv[0] - 180), S, text="COVER", tside="L")
    note_cfg(xR=P(W + 450, 0)[0], yminR=P(0, -ts)[1], upR=True)
    kr = P(W + 450, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 40, **kw)
    R((xs[1] + cw / 2, lv[1]), "MECHANICAL SPLICE ≥ 1.25 fy (TYPE 1); SPECIAL FRAMES WITHIN lo OR 2h OF A JOINT "
                               "FACE: TYPE 2 (DEVELOPS fu)")
    R((W / 2, lv[1] + cl / 2 + 30), "A TIE JUST ABOVE AND JUST BELOW EACH SPLICE LEVEL; NONE AT THE COUPLERS; "
                                    "SPACING OTHERWISE AS FOR THE ZONE")
    R((xs[0] + cw / 2, lv[0]), "ADJACENT SPLICES STAGGERED ≥ 600 mm")
    R((W / 2, 150), "COVER MEASURED TO THE COUPLER")


# ----------------------------------------------------------------------- 1103: tables
def _tie_min(db):
    """code minimum tie diameter for a longitudinal bar (1101 note 2)"""
    return 6 if db <= 12 else 9 if db <= 20 else 10 if db <= 28 else 12


def _dn(v):
    return int(v // 5 * 5)


SPACING_DB = [16, 20, 25, 28, 32]
TIE_SPACING = [[f"DB{d}"] + [(str(_dn(min(16 * d, 48 * t))) if t >= _tie_min(d) else "–") for t in (9, 10, 12)]
               + [str(_dn(min(8 * d, 24 * max(10, _tie_min(d)), 300)))]
               + [str(_dn(min(6 * d, 150)))] for d in SPACING_DB]
CALL_UP = [["C1", "400 × 400", "8-DB20", "C", "RB9 @ 300", "ORDINARY"],
           ["C2", "500 × 500", "12-DB25", "E", "DB10 @ 200 (lo) / @ 400", "INTERMEDIATE"],
           ["C3", "600 × 600", "16-DB25", "G", "DB12 @ 125 (lo) / @ 150", "SPECIAL"]]   # Ash: 4 legs DB12 = 452 >= 0.3 s bc (Ag/Ach - 1) fc/fyt = 389
TIE_NOTES = [
    ("1.", f"THE COLUMN SCHEDULE CALLS UP A TIE TYPE BY ITS LETTER ({TAB('CALL')}). OTHER BAR COUNTS: THE SAME RULE - PERIMETER TIE, "
           "CROSSTIES ON ALTERNATE INTERMEDIATE BARS - SO THAT EVERY CORNER AND ALTERNATE BAR IS HELD AND NO BAR IS "
           "> 150 mm CLEAR FROM A HELD BAR. [EIT 011008 7.10.5.3]"),
    ("2.", "SPECIAL FRAMES: CROSSTIES OR HOOP LEGS AT hx ≤ 350 mm ACROSS THE SECTION (ADD CROSSTIES ON THE OTHER "
           "INTERMEDIATE BARS WHERE NEEDED). INTERMEDIATE AND SPECIAL FRAMES: DEFORMED HOOPS AND CROSSTIES, DB10 MIN."),
    ("3.", "CROSSTIES: 135° + 6 db ≥ 75 mm AT ONE END, 90° + 6 db AT THE OTHER, ENGAGING THE PERIMETER BARS; THE 90° "
           "ENDS ALTERNATE BETWEEN SUCCESSIVE TIES AND BETWEEN OPPOSITE FACES. HOOKS OF SUCCESSIVE PERIMETER TIES AT "
           "DIFFERENT CORNERS."),
    ("4.", f"SPACING: {TAB('TIESP')}, ALSO ≤ THE LEAST COLUMN SIZE (ORDINARY), ≤ c/2 (INTERMEDIATE lo), ≤ c/4 AND "
           "s0 = 100 + (350 − hx)/3, 100 – 150 (SPECIAL lo). OUTSIDE lo: INTERMEDIATE ≤ 2 s0, SPECIAL ≤ 6 db AND 150. "
           "ZONES: 1101."),
    ("5.", "SPIRALS: CONTINUOUS BAR, SPACERS TO HOLD THE PITCH; RATIO PER DESIGN (ρs ≥ 0.45 (Ag/Ach − 1) f'c/fyt). "
           "[EIT 011008 7.10.4]"),
    ("6.", "SPECIAL FRAMES WHERE THE DESIGN APPLIES ACI 318-19 18.7.5.2(f) (Pu > 0.3 Ag f'c OR f'c > 70 MPa): EVERY "
           "PERIMETER BAR HELD BY A HOOP CORNER OR A CROSSTIE WITH 135° HOOKS AT BOTH ENDS, hx ≤ 200 mm - TYPE EH. "
           "THE COLUMN SCHEDULE MARKS THESE COLUMNS; OTHERWISE NOTES 1 – 2 GOVERN (EIT 011008)."),
]


# ======================================================================= place model views# ======================================================================= place model views
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
        "TT": capture(tie_types, 0, -40000),
        "CH": capture(circ_hoop, 10000, -40000),
        "SP": capture(spiral_elev, 0, -50000),
        "MS": capture(couplers, 8000, -50000),
        "FT": capture(footing, 18000, -20000),
        "UW": capture(under_wall, 18000, -30000),
    })


# ======================================================================= sheet 1101
TIE_TABLE = [
    ["USE (DPT T2.3-1)", "SEISMIC CATEGORY B ONLY (R = 3)", "CATEGORY B, C; D ONLY ≤ 40 m, FORCES + 40 % (R = 5)", "ALL CATEGORIES (R = 8)"],
    ["SECTION, BARS", "ρ 1 – 8 %; ≥ 4 BARS (≥ 6 IN SPIRAL)", "ρ 1 – 6 %", "LEAST SIDE ≥ 300 mm, SHORT/LONG ≥ 0.4; ρ 1 – 6 %; "
                                                                            "ΣMc ≥ 1.2 ΣMb"],
    ["END ZONE lo", "–", "≥ max (Hc/6, c1, 500)", "≥ max (Hc/6, c1, 500)"],
    ["SPACING IN lo", "s (AS BELOW)", "s0 ≤ min (8 db, 24 dt, c2/2, 300)",
     "s ≤ min (c2/4, 6 db, s0); s0 = 100 + (350 − hx)/3, 100 – 150"],
    ["FIRST TIE / HOOP", "≤ s/2 FROM FLOOR AND SOFFIT", "≤ s0/2 FROM THE JOINT FACE", "≤ s/2 FROM THE JOINT FACE"],
    ["SPACING OUTSIDE lo", "s ≤ min (16 db, 48 dt, LEAST SIZE)", "≤ 2 s0 (≤ d/2 BESIDE FULL-HEIGHT INFILL)",
     "≤ min (6 db, 150)"],
    ["HOOKS, CROSSTIES", "135° + 6 db ≥ 75 mm; EVERY CORNER AND ALTERNATE BAR HELD, ≤ 150 mm CLEAR",
     "135° + 6 db ≥ 75 mm (90° ONLY WITH HOOK-CLIP)", "135° + 6 db ≥ 75 mm; CROSSTIES 135° / 90° ALTERNATING; hx ≤ 350 mm"],
    ["LAP LOCATION", "ANY LEVEL, NORMALLY JUST ABOVE THE FLOOR", "MID ZONE ONLY, OUTSIDE BOTH lo",
     "CENTRE HALF OF Hc ONLY"],
    ["LAP TYPE", f"CLASS B ({TAB('LAPS')})", "CLASS B; ADJACENT LAPS STAGGERED ≈ 1.0 m", "CLASS B TENSION; HOOPS @ s OVER THE LAP"],
    ["JOINT", "TIES CONTINUE; MAY STOP 75 mm BELOW BEAM BARS IF BEAMS ON 4 SIDES",
     "Av ≥ c1 s / 3fy OVER THE DEEPEST BEAM", "FULL HOOPS; ½ AND s ≤ 150 mm IF 4 BEAMS ≥ ¾ c"],
    ["AT FOOTING", "MIN. 3 TIES IN THE FOOTING", "MIN. 3 TIES; lo ZONE ABOVE THE FOOTING", "HOOPS ≥ 300 mm INTO THE FOOTING"],
    ["REFERENCE", "EIT 011008 7.10, 12.14", "DPT 1301/1302 5.2.5, 5.2.7", "DPT 1301/1302 5.2.9, 5.2.10"],
]


COL_NOTES = [
    ("1.", "THESE DETAILS APPLY WHERE THE COLUMN DRAWINGS DO NOT SHOW OTHERWISE. FRAME TYPE (ORDINARY / INTERMEDIATE / "
           f"SPECIAL) AND SEISMIC CATEGORY: SEE THE DESIGN CRITERIA; TIES AND SPLICES BY FRAME TYPE: {TAB('TIES')}. TIE "
           "TYPES, SPIRALS, COUPLERS: 1103."),
    ("2.", "TIES: OFFICE MINIMUM RB9 IN ORDINARY FRAMES; INTERMEDIATE AND SPECIAL FRAMES: DEFORMED HOOPS AND "
           "CROSSTIES, DB10 MIN. (CODE MINIMUM 6 mm FOR ≤ DB12, 9 mm FOR DB16 – DB20, 10 mm FOR DB25 – DB28, "
           "12 mm FOR ≥ DB32), CLOSED WITH 135° + 6 db ≥ 75 mm HOOKS; HOOKS OF SUCCESSIVE TIES AT DIFFERENT CORNERS. EVERY "
           "CORNER AND ALTERNATE BAR HELD BY A TIE CORNER OR CROSSTIE, NO BAR > 150 mm CLEAR FROM A HELD BAR. "
           "[EIT 011008 7.10.5]"),
    ("3.", "OFFSET BARS: SLOPE ≤ 1:6, BENT BEFORE PLACING; LAPS AT A FLOOR: THE LOWER BARS ARE CRANKED INSIDE THE "
           "JOINT, TOP BEND ≤ 75 mm BELOW THE SLAB TOP, SO THE LAPPED BARS RUN STRAIGHT. TIES WITHIN 150 mm OF EACH BEND TAKE "
           "1.5 x THE HORIZONTAL THRUST. FACE OFFSET ≥ 75 mm: DOWELS LAPPED WITH BOTH COLUMNS. [EIT 011008 7.8.1]"),
    ("4.", f"LAPS PER {TAB('LAPS')}; NO LAPS FOR BARS > DB36. WHERE A LAP DOES NOT FIT ITS ZONE, OR ρ > 4 % AT A "
           "LAP: COUPLERS OR LAPS STAGGERED TO ALTERNATE FLOORS. COUPLERS ≥ 1.25 fy, STAGGERED, A TIE JUST ABOVE AND "
           "BELOW EACH; SPECIAL FRAMES WITHIN lo: COUPLERS DEVELOPING fu (TYPE 2). [EIT 011008 12.13 – 12.16; "
           "ACI 318-11 21.1.6]"),
    ("5.", "ANCHOR BOLTS AT A COLUMN TOP: ≥ 2-DB12 OR 3-DB10 TIES WITHIN 125 mm OF THE TOP, AROUND ≥ 4 BARS. "
           "[EIT 011008 7.10.5]"),
    ("6.", "COLUMN ON A TRANSFER BEAM: BARS TO THE BEAM BOTTOM LAYER WITH 90° HOOKS OUTWARD; COLUMN TIES CONTINUE "
           "INTO THE BEAM AT THE SAME SPACING."),
    ("7.", "SPIRAL COLUMNS: SPIRAL ≥ 9 mm, CLEAR PITCH 25 – 75 mm, 1.5 EXTRA TURNS AT EACH END, FROM THE SLAB TOP TO THE "
           "LOWEST BEAM BARS ABOVE (NO BEAMS ON ALL SIDES: TIES ON TO THE SLAB SOFFIT); LAPS 48 db (DB), 72 db (RB). "
           "[EIT 011008 7.10.4]"),
]


def sheet_1101():
    ps = new_sheet(0)
    top = FY1 - 3
    x = FX0 + 1
    names = [("ORD", "COLUMN - ORDINARY MOMENT FRAME"), ("IMF", "COLUMN - INTERMEDIATE MOMENT FRAME"),
             ("SMF", "COLUMN - SPECIAL MOMENT FRAME")]
    hmax = 0
    for i, (k, nm) in enumerate(names):
        px, pw, ph = viewport(ps, k, 25, x, top)
        hmax = max(hmax, ph)
        view_title(ps, None, top - ph - 6, nm, "N.T.S.", (str(i + 1), "1101"))
        x = px + pw + 3
    ytab = top - hmax - 22                             # below the tallest of the three elevations
    yb = tbl(ps, FX0 + 3, ytab, [30, 90, 95, 99],
             ["ITEM", "ORDINARY (1)", "INTERMEDIATE (2)", "SPECIAL (3)"], TIE_TABLE, "LCCC",
             title=TABT("TIES"))
    print(f"  table bottom {yb:.1f}")


# ======================================================================= sheet 1102
def sheet_1102():
    ps = new_sheet(1)
    top = FY1 - 3
    x = FX0 + 1
    titles = [("SC1", "SIZE CHANGE - INTERIOR, < 75 mm"), ("SC2", "SIZE CHANGE - INTERIOR, ≥ 75 mm"),
              ("SC3", "SIZE CHANGE - EDGE, < 75 mm"), ("SC4", "SIZE CHANGE - EDGE, ≥ 75 mm")]
    hmax = 0
    for i, (k, nm) in enumerate(titles):
        px, pw, ph = viewport(ps, k, 25, x, top)
        hmax = max(hmax, ph)
        view_title(ps, px + 2, top - ph - 6, nm, "N.T.S.", (str(i + 1), "1102"))
        x = px + max(pw, 76) + 2
    top2 = top - hmax - 18
    x = FX0 + 1
    px, pw, ph1 = viewport(ps, "JP", 25, x, top2)
    view_title(ps, None, top2 - ph1 - 6, "EDGE / CORNER JOINT", "N.T.S.", ("5", "1102"))
    x = px + pw + 3
    px, pw, ph2 = viewport(ps, "JE", 25, x, top2)
    view_title(ps, None, top2 - ph2 - 6, "SECTION A", "N.T.S.", ("A", "1102"), triangles=True)
    x = px + pw + 3
    px, pw, ph3 = viewport(ps, "FT", 25, x, top2)
    view_title(ps, None, top2 - ph3 - 6, "STARTER BARS IN FOOTING", "N.T.S.", ("6", "1102"))
    # R2: the 1:25 elevations fill 1101, so the typical column notes sit here, full width
    notes_block(ps, FX0 + 3, top2 - max(ph1, ph2, ph3) - 22, TBX - FX0 - 6, "TYPICAL COLUMN NOTES", COL_NOTES)



# ======================================================================= sheet 1104 (R2: the 1:25 views need a 4th sheet)
def sheet_1104():
    ps = new_sheet(3)
    top = FY1 - 3
    px, pw, ph1 = viewport(ps, "RF", 25, FX0 + 1, top)
    view_title(ps, None, top - ph1 - 6, "COLUMN TOP AT ROOF", "N.T.S.", ("1", "1104"),
               note="90° HOOK 12 db AT THE ROOF TOP AND ≥ ldh ABOVE THE SOFFIT; TIES TO THE TOP")
    px, pw, ph2 = viewport(ps, "TB", 25, px + pw + 8, top)
    view_title(ps, None, top - ph2 - 6, "COLUMN ON A TRANSFER BEAM", "N.T.S.", ("2", "1104"))
    top2 = top - max(ph1, ph2) - 24
    px, pw, ph3 = viewport(ps, "UW", 25, FX0 + 1, top2)
    view_title(ps, None, top2 - ph3 - 6, "COLUMN UNDER A DISCONTINUED WALL", "N.T.S.", ("3", "1104"),
               note="SPECIAL FRAMES, Pu > Ag f'c/10")
    px, pw, ph4 = viewport(ps, "INF", 25, px + pw + 8, top2)
    view_title(ps, None, top2 - ph4 - 6, "COLUMN BESIDE MASONRY INFILL", "N.T.S.", ("4", "1104"),
               note="DPT 1301/1302 5.2.5.1 (FRAMES 2, 3)")



def sheet_1103():
    ps = new_sheet(2)
    top = FY1 - 3
    px, pw, ph1 = viewport(ps, "TT", 25, FX0 + 1, top)
    view_title(ps, None, top - ph1 - 6, "TIE TYPES", "N.T.S.", ("1", "1103"),
               note="SECTION SIZES ILLUSTRATIVE; THE TYPE IS SET BY THE BARS PER FACE")
    xr = px + pw + 6                                               # right-hand column
    if TBX - xr - 3 < 80:
        warn(f"1103 right-hand column only {TBX - xr - 3:.0f} mm wide (tie types view grew)")
    px2, pw2, ph2 = viewport(ps, "CH", 25, xr, top)
    view_title(ps, None, top - ph2 - 6, "CIRCULAR HOOP", "N.T.S.", ("2", "1103"))
    wr = TBX - xr - 3
    yb = tbl(ps, xr + 1, top - ph2 - 20, [16, 16, 16, 16, 18, wr - 82], ["BAR", "ORD. RB9", "DB10", "DB12", "INT. lo",
             "SPEC. lo"], TIE_SPACING, "LCCCCC", title=TABT("TIESP"))
    yb = tbl(ps, xr + 1, yb - 8, [11, 18, 15, 9, wr - 65, 12], ["MARK", "SIZE (mm)", "BARS", "TYPE", "TIES (@ mm)", "FRAME"],
             [r[:5] + [r[5][:3] + "."] for r in CALL_UP], "LCCCLL", title=TABT("CALL"))
    notes_block(ps, xr + 1, yb - 8, wr, "NOTES TO 1103", TIE_NOTES)
    top2 = top - ph1 - 22
    px, pw, ph3 = viewport(ps, "SP", 25, FX0 + 1, top2)
    view_title(ps, None, top2 - ph3 - 6, "SPIRAL COLUMN", "N.T.S.", ("3", "1103"))
    px, pw, ph4 = viewport(ps, "MS", 25, px + pw + 4, top2)
    view_title(ps, None, top2 - ph4 - 6, "MECHANICAL SPLICES", "N.T.S.", ("4", "1103"))
    if px + pw > xr - 3:
        warn(f"1103 second row runs into the right-hand column: {px + pw:.0f} > {xr - 3:.0f}")


def build():
    views()
    sheet_1101()
    sheet_1102()
    sheet_1103()
    sheet_1104()
