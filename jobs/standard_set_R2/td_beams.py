"""
Typical beam details - STR-ST-1111 (stirrups and splice zones by frame type), STR-ST-1112 (bar cut-off,
cantilever, anchorage), STR-ST-1113 (sections, supports, openings), STR-ST-1114 (level changes,
beam ends), STR-ST-1115 (beam schedule, keyed placing diagram - ACI MNL-66 BM-1), STR-ST-1116 (stirrup
types, table, notes).
Sources : EIT 011008-21 ch. 7, 8, 10, 11, 12; DPT 1301/1302-61 cl. 5.2.6 - 5.2.8, 5.2.10; TATA RC detailing
          handbook (beam chapter + typical sheets). See SOURCES_BEAM_DETAILING.md.
"""
from drafter.td_engine import *
import issue                     # noqa: F401  title-block issue data (stage, revision, status)
from members import *

BASE = "STR-ST-1111_Typical_Beam_Details_A3_R2"
SHEETS[:] = [("1111", ["TYPICAL BEAM DETAILS (1)", "STIRRUPS AND SPLICE ZONES"], "N.T.S."),
             ("1112", ["TYPICAL BEAM DETAILS (2)", "BAR CUT-OFF AND CANTILEVER"], "N.T.S."),
             ("1113", ["TYPICAL BEAM DETAILS (3)", "SECTIONS, SUPPORTS, OPENINGS"], "N.T.S."),
             ("1114", ["TYPICAL BEAM DETAILS (4)", "LEVEL CHANGES, BEAM ENDS"], "N.T.S."),
             ("1115", ["TYPICAL BEAM DETAILS (5)", "BEAM SCHEDULE"], "N.T.S."),
             ("1116", ["TYPICAL BEAM DETAILS (6)", "STIRRUP TYPES, TABLE, NOTES"], "N.T.S.")]


# ======================================================================= TYPICAL BEAM DETAILS
# Drawing rule: normal (2.0 / 2.8 text). Values are symbolic (2h, s1, d/2, ln/3 ...); numbers are in the table.
COLW = COL                     # column width in the elevation (members.py)
DS_ = DT                       # stirrup RB9 (drawn)
HB = BEAM_H                    # beam depth h
BW = BEAM_B                    # beam width
YB = CVR + DS_ + DBM / 2       # 59  bar centre from the beam face
YS = CVR + DS_ / 2             # 44.5 stirrup centreline from the face
XT_C = CVR + DS_ / 2           # column tie centreline from the column face
LN = SPAN_D                    # clear span (drawn, N.T.S.)
H2 = 2 * HB                    # 2h end zone
LAPD = LAP_D                   # drawn lap length (members.py)
GAP = 45                       # drawn offset of lapped / additional bars
CUP = 150                      # column drawn above / below the beam (a stub only indicates the column)
STUB = 300                     # beam drawn beyond the interior column


def rbar(sp, pts, db=DBM, layer="S-REBR"):
    return bar(sp, pts, db, layer)


def stirrups(sp, P, xs, y0=YS, y1=HB - YS, layer="S-STIR-ELEV"):          # elevation: grey hidden (GD-01)
    for x in xs:
        line(sp, P(x, y0), P(x, y1), layer)


def frame_elev(sp, P):
    """exterior column (left, x -COLW..0), clear span 0..LN, interior column (LN..LN+COLW), beam stub beyond"""
    S = 25
    ytop, ybot = HB + CUP, -CUP
    xe = LN + COLW + STUB
    line(sp, P(-COLW, ybot), P(-COLW, ytop), "S-CONC")
    for x in (0, LN, LN + COLW):
        line(sp, P(x, ybot), P(x, 0), "S-CONC")
        line(sp, P(x, HB), P(x, ytop), "S-CONC")
    for x0, x1 in ((-COLW, 0), (LN, LN + COLW)):
        zbreak(sp, P(x0 - 60, ybot), P(x1 + 60, ybot), S)
        zbreak(sp, P(x0 - 60, ytop), P(x1 + 60, ytop), S)
    for y in (0, HB):
        line(sp, P(0, y), P(LN, y), "S-CONC")
        line(sp, P(LN + COLW, y), P(xe, y), "S-CONC")
    zbreak(sp, P(xe, -80), P(xe, HB + 80), S)
    for x0, x1 in ((-COLW, 0), (LN, LN + COLW)):                    # column hatch, grey (GD-01)
        hatch(sp, [P(x0, ybot), P(x1, ybot), P(x1, ytop), P(x0, ytop)], "ANSI31", pscale("ANSI31", S, 1.6))
    for x in (-COLW + YB, -YB, LN + YB, LN + COLW - YB):                  # column bars: not the subject
        rbar(sp, [P(x, ybot), P(x, ytop)], layer="S-REBR-NF")


# ----------------------------------------------------------------------- 1111: beam elevations by frame type
def beam_elev(ox, oy, kind):
    """one end span, exterior column left, interior column right (DPT Fig 5.2-3 layout), kind ORD / IMF / SMF"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    frame_elev(sp, P)
    xe = LN + COLW + STUB
    xh = -COLW + YB + 45                                   # hook tails inside the far column bars
    yt, yb = HB - YB, YB
    tail = 12 * DBM                                        # 90 deg hook, 12 db tail
    xb = xh + 45                                           # bottom-bar tail beside the top-bar tail, never on it

    # ---- longitudinal bars and laps
    top_lap = (LN / 2 - LAPD / 2, LN / 2 + LAPD / 2)                       # top bars: lap near midspan
    if kind == "ORD":
        bot_lap = (LN - LAPD, LN + COLW / 2)                               # bottom bars: lap at the support
    else:
        bot_lap = (LN - H2 - LAPD, LN - H2)                                # outside 2h
    rbar(sp, [P(xh, yt - tail), P(xh, yt), P(top_lap[1], yt)])
    rbar(sp, [P(*q) for q in lap_crank(top_lap[0], top_lap[1], yt, -GAP)] + [P(xe, yt)])
    rbar(sp, [P(xb, yb + tail), P(xb, yb), P(bot_lap[1], yb)])
    x2 = bot_lap[0]
    q = lap_crank(x2, bot_lap[1], yb, GAP)
    rbar(sp, [P(*p_) for p_ in q] + [P(xe, yb)] if q[-1][0] < xe - 50 else [P(x2, yb + GAP), P(xe, yb + GAP)])

    # ---- stirrups
    if kind == "ORD":
        s, s1 = 250, 250
        xs = zone(0, LN, s) + zone(LN + COLW, xe - 40, s)
        xs = [x for x in xs if x < LN - 20 or x > LN + COLW]
    else:
        s1, s = 125, 250
        left = zone(0, H2, s1)
        right = zone(LN, LN - H2, s1)
        mid = [x for x in rng(left[-1] + s, right[-1] - s * 0.8, s)]
        stub = zone(LN + COLW, xe - 40, s1)
        xs = left + mid + right + stub
        if kind == "SMF":                                     # hoops over the laps at <= min(d/4, 100)
            for a, b in (top_lap, bot_lap):
                xs = [x for x in xs if not (a - 60 < x < b + 60)] + rng(a - 50, b + 50, 100)
    stirrups(sp, P, sorted(set(round(x, 1) for x in xs)))

    # ---- GD-01 presentation (102 RC Beam instruction): zone band 8.4 mm under the soffit, dimensions from its
    # bottom edge (shortest row first), grid bubbles on the column centres, numbered callouts + list
    near = lambda t: min(xs, key=lambda v: abs(v - t))                 # a stirrup to point at
    zones = ([(0, LN, "STIRRUPS @ s")] if kind == "ORD" else
             [(0, H2, "2h: s1"), (H2, LN - H2, "MIDDLE: s"), (LN - H2, LN, "2h: s1")])
    yband = zone_band(sp, P, zones, -210, S)
    yd = yband - 150
    rows = [[(LN / 4, 3 * LN / 4, "TOP-BAR LAP ZONE ln/2")]] if kind == "ORD" else [[(top_lap[0], top_lap[1], "TOP LAP")]]
    rows += [[(0, LN, "ln (CLEAR SPAN)")]]
    for i, row in enumerate(rows):
        for a, b_, t in row:
            dim(sp, P(a, yband), P(b_, yband), P(0, yd - i * 170), S, text=t)
    dim(sp, P(-COLW, 0), P(-COLW, HB), P(-COLW - 300, 0), S, angle=90, text="h")
    ybub = HB + CUP + 100 + 3.5 * S
    ygb = yd - (len(rows) - 1) * 170 - 120
    grid_bubble(sp, P, -COLW / 2, ybub, ygb, "A", S)
    grid_bubble(sp, P, LN + COLW / 2, ybub, ygb, "B", S)
    ya, yu = HB + 250, -110                                             # callout rows above / below the beam
    hook = ((-COLW - 150, 400), (xh, 400))                              # on the top-bar hook tail in the column
    if kind == "ORD":
        items = ["90° HOOKS IN THE EXTERIOR COLUMN, ldh FROM THE FACE, TAILS INTO THE JOINT",
                 "TOP BARS: ≥ 2 CONTINUOUS; CLASS B LAP NEAR MIDSPAN",
                 "FIRST STIRRUP 50 FROM THE FACE; s ≤ d/2, 600 (d/4, 300 IF Vs > 0.33√f'c bw d)",
                 "BOTTOM BARS: ≥ 2 CONTINUOUS; CLASS B LAP AT OR NEAR THE SUPPORT"]
        cs = [hook, ((top_lap[0] + 150, ya), (top_lap[0] + 150, yt - GAP)),
              ((near(LN / 2 + 125), yu), (near(LN / 2 + 125), HB / 2)),
              ((bot_lap[0] + 200, yu), (bot_lap[0] + 200, yb + GAP))]
    elif kind == "IMF":
        items = ["90° HOOKS AT THE FAR SIDE OF THE COLUMN, ldh FROM THE FACE",
                 "TOP LAP NEAR MIDSPAN, BOTTOM LAP OUTSIDE 2h: NO LAPS WITHIN 2h OF A FACE",
                 "MIDDLE ZONE: STIRRUPS @ ≤ d/2",
                 "2h ZONES: FIRST ≤ 50 mm, s1 ≤ d/4, 8 db, 24 dt, 300 mm; 135° HOOKS (OR 90° + HOOK-CLIP) IN PUBLIC / "
                 "DUCTILE BUILDINGS"]
        cs = [hook, ((top_lap[0] + 150, ya), (top_lap[0] + 150, yt - GAP)),
              ((near(H2 + 150), yu), (near(H2 + 150), HB / 2)),
              ((near(LN - 300), yu), (near(LN - 300), HB / 2))]
    else:
        items = ["HOOKS INSIDE THE CONFINED CORE, ldh ≥ 8 db, 150, fy db / (5.3√f'c)",
                 "LAPS OUTSIDE JOINTS, 2h ZONES AND HINGES; HOOPS @ ≤ d/4, 100 mm OVER THE LAP",
                 "MIDDLE ZONE: STIRRUPS WITH SEISMIC HOOKS BOTH ENDS @ ≤ d/2",
                 "2h ZONES: CLOSED HOOPS, FIRST ≤ 50 mm, s1 ≤ d/4, 6 db, 24 dt, 150 mm; ALSO 2h EACH SIDE OF ANY OTHER HINGE",
                 "BARS THROUGH THE JOINT: COLUMN ≥ 20 db OF THE LARGEST BEAM BAR"]
        cs = [hook, ((top_lap[0] + 150, ya), (top_lap[0] + 150, yt - GAP)),
              ((near(H2 + 150), yu), (near(H2 + 150), HB / 2)),
              ((near(LN - 300), yu), (near(LN - 300), HB / 2)),
              ((LN + COLW + 150, ya), (LN + COLW / 2 + 100, yt))]
    for n, (c, tip) in enumerate(cs, 1):
        callout(sp, P, n, c, tip, S)
    callout_list(sp, P, xe + 250, ybub + 3.5 * S, items, S, width=88)

def col_stack(sp, P, x0, w, yb, yt, S, ytop_beam=HB, ybot_beam=0, outer=True):
    """column from yb to yt; the beam frames in on the inner face (both faces when outer=False)"""
    if outer:
        line(sp, P(x0, yb), P(x0, yt), "S-CONC")
    for x in ((x0 + w,) if outer else (x0, x0 + w)):
        line(sp, P(x, yb), P(x, ybot_beam), "S-CONC")
        line(sp, P(x, ytop_beam), P(x, yt), "S-CONC")
    hatch(sp, [P(x0, yb), P(x0 + w, yb), P(x0 + w, yt), P(x0, yt)], "ANSI31", pscale("ANSI31", S, 1.6))
    zbreak(sp, P(x0 - 60, yb), P(x0 + w + 60, yb), S)
    zbreak(sp, P(x0 - 60, yt), P(x0 + w + 60, yt), S)
    for x in (x0 + YB, x0 + w - YB):                                     # column bars: not the subject
        rbar(sp, [P(x, yb), P(x, yt)], layer="S-REBR-NF")


def cutoff(ox, oy):
    """end span + interior support + part of the interior span: TATA Fig 2.27 cut-off points (clear spans)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L1, L2 = 3000, 3000                                # N.T.S.
    xi0, xi1 = L1, L1 + COLW                        # interior column
    xe = xi1 + 0.45 * L2                            # break in the interior span
    Lg = max(L1, L2)
    col_stack(sp, P, -COLW, COLW, -CUP, HB + CUP, S)
    col_stack(sp, P, xi0, COLW, -CUP, HB + CUP, S, outer=False)
    for y in (0, HB):
        line(sp, P(0, y), P(xi0, y), "S-CONC")
        line(sp, P(xi1, y), P(xe, y), "S-CONC")
    zbreak(sp, P(xe, -80), P(xe, HB + 80), S)
    xh = -COLW + YB + 45
    yt, yb = HB - YB, YB
    tail = 12 * DBM + 60
    g = GAP
    # continuous bars
    rbar(sp, [P(xh, yt - tail), P(xh, yt), P(xe, yt)])                                  # 2 top, continuous
    # bottom lap across the interior support; 1:6 crank ends >= 150 before the interior-span additional bars,
    # the lapped bar starts >= 150 after the end-span additional bars (GD-01 gap rule)
    rbar(sp, [P(xh + 2 * g, yb + tail), P(xh + 2 * g, yb), P(xi1 - 100, yb)])           # 2 bottom, end span
    rbar(sp, [P(*q) for q in lap_crank(xi0 - 200, xi1 - 100, yb, g)] + [P(xe, yb)])         # 2 bottom, next span (lap)
    # additional top bars
    x_a = L1 / 4
    rbar(sp, [P(xh + g, yt - tail + 60), P(xh + g, yt - g), P(x_a, yt - g)])
    xa0, xa1 = xi0 - Lg / 3, xi1 + Lg / 3
    rbar(sp, [P(xa0, yt - g), P(xa1, yt - g)])
    # additional bottom bars
    xb1 = 0.875 * L1
    rbar(sp, [P(-150, yb + g), P(xb1, yb + g)])
    xc0 = xi1 + 0.15 * L2
    rbar(sp, [P(xc0, yb + g), P(xe, yb + g)])                  # same level as the end-span additional bars
    stirrups(sp, P, [50, L1 - 50, xi1 + 50])
    # dimensions: all chains below the beam (row labels TOP / BOTTOM), notes above the soffit
    yd = -CUP - 250
    # tiers: the shorter bottom-bar dimensions lie inside the top-bar ones, so they sit nearer the beam
    rows = [("BOTTOM BARS", [(xb1, xi0, "0.125 L1"), (xi1, xc0, "0.15 L2")]),
            ("TOP BARS", [(0, x_a, "L1/4"), (xa0, xi0, "L/3"), (xi1, xa1, "L/3")]),
            ("", [(0, xi0, "L1 (CLEAR SPAN)")])]
    for i, (lab, row) in enumerate(rows):
        y_ = yd - i * 200
        for a, b, t in row:
            dim(sp, P(a, 0), P(b, 0), P(0, y_), S, text=t)
        if lab:
            row_label(sp, P, rows, i, y_, S, avoid=(-COLW / 2, xi0 + COLW / 2))
    text(sp, "L2 (CLEAR SPAN) →", P(xi1 + 200, yd - 400 + 60), 2.0 * S)
    # grid bubbles and numbered callouts (GD-01)
    ybub = HB + CUP + 100 + 3.5 * S
    ygb = yd - 2 * 200 - 120
    grid_bubble(sp, P, -COLW / 2, ybub, ygb, "A", S)
    grid_bubble(sp, P, xi0 + COLW / 2, ybub, ygb, "B", S)
    ya, yu = HB + 250, -110
    items = ["BOTTOM BARS HOOKED UP AT THE EXTERIOR SUPPORT",
             "STIRRUPS PER THE BEAM SCHEDULE; FIRST 50 mm FROM EACH FACE",
             "BOTTOM BARS INTO EVERY SUPPORT ≥ 150 mm: ≥ 1/4 OF THEM (1/3 AT A SIMPLE SUPPORT), ≥ 2; CONTINUOUS OR "
             "CLASS B LAP (SEISMIC FRAMES: LAPS OUTSIDE 2h, 1111)",
             "ADDITIONAL TOP BARS: L1/4 AT THE EXTERIOR SUPPORT (90° HOOK IN THE COLUMN); L/3 EACH SIDE OF AN "
             "INTERIOR SUPPORT, L = LARGER ADJACENT CLEAR SPAN",
             "≥ 2 TOP BARS CONTINUOUS, LAPPED NEAR MIDSPAN",
             "ADDITIONAL BOTTOM BARS: 0.875 L1 FROM THE EXTERIOR FACE (END SPAN); 0.70 L2 CENTRED (INTERIOR SPAN)"]
    cs = [((-COLW - 150, yb + tail * 0.5), (xh + 2 * g, yb + tail * 0.5)),
          ((L1 - 530, yu), (L1 - 50, HB / 2)),                # 2 and 3 left of the column: parallel leaders
          ((xi0 - 200, yu), (xi0 + 100, yb)),
          ((xa1 - 300, ya), (xa1 - 300, yt - g)),
          ((xe - 250, ya), (xe - 250, yt)),
          ((xe - 170, yu), (xe - 250, yb + g))]
    for n, (c, tip) in enumerate(cs, 1):
        callout(sp, P, n, c, tip, S)
    callout_list(sp, P, xe + 250, ybub + 3.5 * S, items, S, width=62)

def cantilever(ox, oy):
    """cantilever with back span (TATA Figs 2.37 - 2.39)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    LB, LC = 1800, 1800                              # back span drawn, cantilever (from the face), N.T.S.
    x0, x1 = 0, COLW                                 # column
    xs, xt = -LB, COLW + LC                          # break in the back span, tip
    col_stack(sp, P, x0, COLW, -CUP, HB + CUP, S, outer=False)
    for y in (0, HB):
        line(sp, P(xs, y), P(x0, y), "S-CONC")
        line(sp, P(x1, y), P(xt, y), "S-CONC")
    line(sp, P(xt, 0), P(xt, HB), "S-CONC")
    zbreak(sp, P(xs, -80), P(xs, HB + 80), S)
    yt, yb = HB - YB, YB
    g = GAP
    ld = 900                                          # drawn Ld
    xcut = x1 + max(0.5 * LC, ld)
    rbar(sp, [P(xs, yt), P(xt - YB, yt), P(xt - YB, yt - 12 * DBM - 60)])                 # 0.5 Ast to the tip
    rbar(sp, [P(x0 - ld, yt - g), P(xcut, yt - g)])                                     # 0.5 Ast cut
    rbar(sp, [P(xs, yb), P(x1 + 250, yb)])                                              # back-span bottom
    rbar(sp, [P(x0 - ld / 3, yb + g), P(xt - YB, yb + g)])                              # cantilever bottom
    xs_ = [x for x in rng(xs + 100, x0 - 50, 250)] + zone(x1, xt - 60, 200)
    stirrups(sp, P, xs_)
    yd = -CUP - 250                                  # all chains below the beam, notes above the soffit
    # tiers: Ld/3 lies inside Ld, so the bottom-bar row sits nearer the beam
    rows = [("BOTTOM BARS", [(x0 - ld / 3, x0, "Ld/3")]),
            ("TOP BARS", [(x0 - ld, x0, "≥ Ld"), (x1, xcut, "≥ 0.5 Lc, Ld")]),
            ("", [(x1, xt, "Lc (FROM THE FACE)")])]
    for i, (lab, row) in enumerate(rows):
        y_ = yd - i * 200
        for a, b, t in row:
            dim(sp, P(a, 0), P(b, 0), P(0, y_), S, text=t)
        if lab:
            row_label(sp, P, rows, i, y_, S, avoid=(COLW / 2,))
    # grid bubble and numbered callouts (GD-01)
    ybub = HB + CUP + 100 + 3.5 * S
    grid_bubble(sp, P, COLW / 2, ybub, yd - 2 * 200 - 120, "A", S)
    ya, yu = HB + 250, -110
    near = lambda t: min(xs_, key=lambda v: abs(v - t))
    items = ["½ OF THE TOP BARS MAY STOP AT ≥ 0.5 Lc AND ≥ Ld FROM THE FACE; ½ TO THE TIP, 90° HOOK DOWN",
             "INTO THE BACK SPAN ≥ Ld AND ≥ THE INTERIOR-SUPPORT CUT-OFF (1)",
             "STIRRUPS TO THE TIP; FIRST 50 mm FROM THE FACE",
             "BOTTOM BARS ≥ 1/4 OF THE TOP BARS, ≥ 2, Ld/3 INTO THE SUPPORT; TIP ≥ 150 mm DEEP IF TAPERED"]
    cs = [((xcut - 300, ya), (xcut - 300, yt - g)),
          ((x0 - ld + 250, ya), (x0 - ld + 250, yt - g)),
          ((near(xt - 700), yu), (near(xt - 700), HB / 2)),
          ((xt - 1200, yu), (xt - 1200, yb + g))]
    for n, (c, tip) in enumerate(cs, 1):
        callout(sp, P, n, c, tip, S)
    callout_list(sp, P, xt + 300, ybub + 3.5 * S, items, S, width=62)

def end_anchor(ox, oy):
    """beam bars at an exterior column (DPT Fig 5.2-3 / 5.2-12, EIT 12.5)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    C = 500
    yb0, yt0 = -350, HB + 350
    xe = 1100
    col_stack(sp, P, -C, C, yb0, yt0, S)
    for y in (0, HB):
        line(sp, P(0, y), P(xe, y), "S-CONC")
    zbreak(sp, P(xe, -80), P(xe, HB + 80), S)
    yt, yb = HB - YB, YB
    xh = -C + YB + DBM + 15                           # hook tails just inside the column bars
    tail = 12 * DBM
    rbar(sp, [P(xh, yt - tail - 3.5 * DBM), P(xh, yt), P(xe, yt)])
    rbar(sp, [P(xh + 40, yb + tail + 3.5 * DBM), P(xh + 40, yb), P(xe, yb)])
    for y in rng(yb0 + 75, yt0 - 50, 150):
        line(sp, P(-C + XT_C, y), P(-XT_C, y), "S-STIR-ELEV")                # column ties: grey hidden
    stirrups(sp, P, zone(0, xe - 60, 125))
    dim(sp, P(xh - DBM / 2, HB), P(0, HB), P(0, yt0 + 150), S, text="ldh")
    dim(sp, P(xh, yt), P(xh, yt - tail - 3.5 * DBM), P(xh - 220, 0), S, angle=90, text="12 db")
    note_cfg(xR=P(xe + 300, 0)[0], ymaxR=P(0, HB - 70)[1])      # rows below the ldh dimension
    kr = P(xe + 300, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 38, **kw)
    R((xh, yt - 140), f"ldh FROM THE FACE TO THE OUTSIDE OF THE HOOK ({TAB('LAPS')}); SPECIAL: "
                      "≥ 8 db, 150, fy db / (5.3√f'c)")
    R((xh, yt - 250), "TOP BARS 90° DOWN, BOTTOM BARS 90° UP, INSIDE THE COLUMN BARS AT THE FAR SIDE")
    R((-C / 2, yb0 + 225), "COLUMN TIES CONTINUE THROUGH THE JOINT (1101); ≤ 3 db OVER ldh WHERE SIDE COVER < 65 mm")
    R((50 + 125 * 3, HB / 2), "FIRST STIRRUP 50 mm FROM THE FACE")
    R((xe - 200, yb), "WIDE SUPPORT: STRAIGHT BARS ≥ ld (TOP BARS × 1.3) FROM THE FACE MAY REPLACE THE HOOKS")


# ----------------------------------------------------------------------- 1113: typical section (1:20)
def typ_section(ox, oy):
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    B, H, T, SL = 350, 700, 150, 260
    pline(sp, [P(0, H - T), P(0, 0), P(B, 0), P(B, H - T)], "S-CONC")
    line(sp, P(-SL, H), P(B + SL, H), "S-CONC")
    for x0, x1 in ((-SL, 0), (B, B + SL)):
        line(sp, P(x0, H - T), P(x1, H - T), "S-CONC")
    zbreak(sp, P(-SL, H - T - 40), P(-SL, H + 40), S)
    zbreak(sp, P(B + SL, H - T - 40), P(B + SL, H + 40), S)
    rb = rdot(DBM, S)
    R_ = rb + DS_ / 2
    xs = [YB + i * (B - 2 * YB) / 3 for i in range(4)]
    lay = DBM + 25                                     # centre-to-centre of layers: db + clear 25
    cor = lambda x, y: (P(x, y)[0], P(x, y)[1], R_)
    stirrup(sp, cor(xs[0], H - YB), cor(xs[-1], H - YB), cor(xs[-1], YB), cor(xs[0], YB), 6 * DS_ + 25)
    for x in xs:
        dot(sp, P(x, H - YB), rb)
        dot(sp, P(x, YB), rb)
    for x in (xs[0], xs[-1]):
        dot(sp, P(x, H - YB - lay), rb)
        dot(sp, P(x, YB + lay), rb)
    for x in (YB - 2, B - YB + 2):                     # side-face bars
        dot(sp, P(x, H / 2 - 60), rdot(12, S))
    # dimensions on the left and below only; the notes (right) stay above the b dimension
    dim(sp, P(0, 0), P(B, 0), P(0, -170), S, text="b")
    dim(sp, P(-SL, 0), P(-SL, H), P(-SL - 150, 0), S, angle=90, text="h")
    note_cfg(xR=P(B + SL + 420, 0)[0], yminR=P(0, 40)[1], upR=True)
    kr = P(B + SL + 420, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 44, **kw)
    R((xs[1], H - YB), "TOP BARS, 1ST LAYER", ring=DBM)
    R((xs[-1], H - YB - lay), "2ND LAYER (IF ANY) DIRECTLY BELOW THE 1ST, CLEAR ≥ 25 mm AND ≥ db", ring=DBM)
    R((B - YB + 2, H / 2 - 60), "SIDE-FACE BARS WHERE h > 600 mm (NOTE 7)", ring=12)
    R((B, H / 2 - 200), "STIRRUP: 40 mm CLEAR COVER (TYP.)")
    R((xs[-1], YB + lay), "2ND LAYER (IF ANY) DIRECTLY ABOVE THE 1ST, CLEAR ≥ 25 mm AND ≥ db", ring=DBM)
    R((xs[2], YB), "BOTTOM BARS, 1ST LAYER", ring=DBM)


# ----------------------------------------------------------------------- 1113: secondary beam on a main beam (1:25)
# SEC_H, SEC_B: secondary beam 250 x 450 (members.py)
DROP = 25                      # main-beam top bars set lower where the secondary top bars pass over them


def sec_on_main(ox, oy):
    """section along the main beam at a secondary beam: hanger bars + additional stirrups (TATA Fig 2.31)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L = 1450
    for y in (0, HB):
        line(sp, P(-L, y), P(L, y), "S-CONC")
    zbreak(sp, P(-L, -80), P(-L, HB + 80), S)
    zbreak(sp, P(L, -80), P(L, HB + 80), S)
    ys = HB - SEC_H
    pline(sp, [P(-SEC_B / 2, HB), P(-SEC_B / 2, ys), P(SEC_B / 2, ys), P(SEC_B / 2, HB)], "S-CONC-HIDN")
    yt, yb = HB - YB - DROP, YB
    rbar(sp, [P(-L, yt), P(L, yt)])
    rbar(sp, [P(-L, yb), P(L, yb)])
    rb = rdot(DBM, S)
    for x in (-SEC_B / 2 + YB, SEC_B / 2 - YB):                        # secondary bars in section
        dot(sp, P(x, HB - YB), rb)
        dot(sp, P(x, ys + YB), rb)
    # hanger: cradles the secondary bottom bars, 60 deg up, top legs 1.5 d beyond the secondary faces
    d = HB - YB
    yh0 = ys + YB - DBM / 2 - DBM / 2 - 3
    yh1 = yt - DBM - 5
    run = (yh1 - yh0) / math.tan(math.radians(60))
    xa = SEC_B / 2 + 20
    xe = SEC_B / 2 + 1.5 * d
    rbar(sp, [P(-xe, yh1), P(-xa - run, yh1), P(-xa, yh0), P(xa, yh0), P(xa + run, yh1), P(xe, yh1)])
    # stirrups: additional each side, then normal
    extra = [SEC_B / 2 + 50 + k * 50 for k in range(3)]
    normal = rng(extra[-1] + 200, L - 60, 200)
    xs_ = extra + normal
    stirrups(sp, P, [x for x in xs_] + [-x for x in xs_] + [0])
    dim(sp, P(SEC_B / 2, HB), P(xe, HB), P(0, HB + 200), S, text="1.5 d")
    dim(sp, P(-SEC_B / 2, HB), P(SEC_B / 2, HB), P(0, HB + 200), S, text="b2")
    note_cfg(xR=P(L + 300, 0)[0])
    kr = P(L + 300, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 46, **kw)
    R((SEC_B / 2 - YB, HB - YB), "SECONDARY TOP BARS PASS OVER THE MAIN-BEAM TOP BARS", ring=DBM)
    R((xe - 150, yh1), "HANGER BARS, ONE EACH SIDE INSIDE THE STIRRUPS (MIN. 2-DB16), UNDER THE SECONDARY "
                       "BOTTOM BARS, 60°")
    R((extra[1], HB / 2 - 120), "ADDITIONAL MAIN-BEAM STIRRUPS EACH SIDE (MIN. 3 @ 50 mm) UNLESS SHOWN")
    R((SEC_B / 2 - YB, ys + YB), "SECONDARY BOTTOM BARS ON THE MAIN-BEAM BOTTOM BARS OR ON THE HANGERS", ring=DBM)
    R((L - 300, yb), "MAIN-BEAM BARS")


def sec_end(ox, oy):
    """section along the secondary beam through the main beam (continuous secondary beam)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    BM = 300                                          # main beam width (cut)
    L = 1100
    ys = HB - SEC_H
    pline(sp, [P(-L, ys), P(0, ys), P(0, 0), P(BM, 0), P(BM, ys), P(BM + L, ys)], "S-CONC")
    line(sp, P(-L, HB), P(BM + L, HB), "S-CONC")
    zbreak(sp, P(-L, ys - 80), P(-L, HB + 80), S)
    zbreak(sp, P(BM + L, ys - 80), P(BM + L, HB + 80), S)
    rb = rdot(DBM, S)
    R_ = rb + DS_ / 2
    cor = lambda x, y: (P(x, y)[0], P(x, y)[1], R_)
    yt_m = HB - YB - DROP
    stirrup(sp, cor(YB, yt_m), cor(BM - YB, yt_m), cor(BM - YB, YB), cor(YB, YB), 6 * DS_ + 25)
    for x in (YB, BM - YB):
        dot(sp, P(x, yt_m), rb)
        dot(sp, P(x, YB), rb)
    ysb = ys + YB
    rbar(sp, [P(-L, HB - YB), P(BM + L, HB - YB)])                      # secondary top, continuous over
    rbar(sp, [P(-L, ysb), P(BM + 400, ysb)])                            # secondary bottom, lapped through
    rbar(sp, [P(*q) for q in lap_crank(-400, BM + 400, ysb, 30)] + [P(BM + L, ysb)])
    for x in (YB + 45, BM - YB - 45):                                   # hangers (cut)
        dot(sp, P(x, ysb - DBM - 3), rdot(16, S))
    xs_ = zone(0, -L + 60, 150) + zone(BM, BM + L - 60, 150)
    stirrups(sp, P, xs_, y0=ys + YS)
    dim(sp, P(BM, ys), P(BM + 400, ys), P(0, ys - 220), S, text="LAP")
    note_cfg(xR=P(BM + L + 300, 0)[0], yminR=P(0, ys + 20)[1], upR=True)       # rows above the LAP dimension
    kr = P(BM + L + 300, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 46, **kw)
    R((BM + 700, HB - YB), "SECONDARY TOP BARS CONTINUOUS OVER THE MAIN-BEAM TOP BARS")
    R((BM - YB, yt_m), "MAIN-BEAM TOP BARS ONE BAR LOWER", ring=DBM)
    R((BM - YB - 45, ysb - DBM - 3), "HANGER BARS", ring=16)
    R((BM + 250, ysb), "BOTTOM BARS THROUGH THE MAIN BEAM, LAPPED; ENDING BEAM: TO THE FAR SIDE ≥ 150 mm IN")
    R((BM + 50, ys + 150), "FIRST STIRRUP 50 mm FROM THE MAIN-BEAM FACE")


# ----------------------------------------------------------------------- 1114: beams at different levels (1:50)
def levels(ox, oy):
    S = 25
    sp = msp
    note_cfg(free=True)
    for k, case in enumerate(("TOP", "DEPTH", "SOFFIT")):
        P = (lambda x, y, k=k: (ox + k * 2600 + x, oy + y))
        C = COL
        yb0, yt0 = -500, HB + 300
        Lb = 1000
        # left (higher / deeper) beam: 0..HB ; right beam: TOP -> -300..300 (both levels differ),
        # DEPTH -> 150..600 (tops flush), SOFFIT -> 0..450 (soffits flush, lower top)
        rt, rbot = {"TOP": (300, -300), "DEPTH": (HB, HB - SEC_H), "SOFFIT": (SEC_H, 0)}[case]
        line(sp, P(0, yb0), P(0, 0), "S-CONC")
        line(sp, P(C, yb0), P(C, rbot), "S-CONC")
        line(sp, P(0, HB), P(0, yt0), "S-CONC")
        line(sp, P(C, rt), P(C, yt0), "S-CONC")
        zbreak(sp, P(-60, yb0), P(C + 60, yb0), S)
        zbreak(sp, P(-60, yt0), P(C + 60, yt0), S)
        nf_hatch(sp, rect(P, 0, yb0, C, yt0), S)                        # the column: not the subject
        for x in (YB, C - YB):
            rbar(sp, [P(x, yb0), P(x, yt0)], layer="S-REBR-NF")
        for y in (0, HB):
            line(sp, P(-Lb, y), P(0, y), "S-CONC")
        for y in (rbot, rt):
            line(sp, P(C, y), P(C + Lb, y), "S-CONC")
        zbreak(sp, P(-Lb, -80), P(-Lb, HB + 80), S)
        zbreak(sp, P(C + Lb, rbot - 80), P(C + Lb, rt + 80), S)
        xin, xfar = YB + 45, C - YB - 45
        tl = 12 * DBM + 60
        if case == "TOP":
            rbar(sp, [P(-Lb, HB - YB), P(xfar, HB - YB), P(xfar, HB - YB - tl)])          # higher top: down
            rbar(sp, [P(C + Lb, rt - YB), P(-700, rt - YB)])                             # lower top: into higher
            rbar(sp, [P(-Lb, YB), P(C + 700, YB)])                                       # higher bottom: into lower
            rbar(sp, [P(C + Lb, rbot + YB), P(xin, rbot + YB), P(xin, rbot + YB + tl)])   # lower bottom: up
            lab = ["(a) DIFFERENT TOP AND SOFFIT LEVELS", "SEPARATE BARS, NOT CRANKED THROUGH;",
                   "STRAIGHT BARS Ld INTO THE", "OTHER BEAM, HOOKED BARS 90° IN THE COLUMN"]
        elif case == "SOFFIT":
            rbar(sp, [P(-Lb, HB - YB), P(xfar, HB - YB), P(xfar, HB - YB - tl)])          # higher top: down
            rbar(sp, [P(C + Lb, rt - YB), P(-700, rt - YB)])                             # lower top: into higher
            rbar(sp, [P(-Lb, YB), P(C + Lb, YB)])                                        # soffits flush: continuous
            lab = ["(c) DIFFERENT TOP LEVELS, SOFFITS FLUSH", "BOTTOM BARS CONTINUOUS; LOWER-BEAM TOP",
                   "BARS Ld INTO THE HIGHER BEAM; HIGHER-", "BEAM TOP BARS 90° DOWN AT THE FAR FACE"]
        else:
            rbar(sp, [P(-Lb, HB - YB), P(C + Lb, HB - YB)])                              # tops flush: continuous
            rbar(sp, [P(C + Lb, rbot + YB), P(-700, rbot + YB)])                         # shallow bottom: into deep
            rbar(sp, [P(-Lb, YB), P(xfar, YB), P(xfar, YB + tl)])                          # deep bottom: up
            lab = ["(b) DIFFERENT DEPTHS, TOPS FLUSH", "TOP BARS CONTINUOUS; SHALLOW-BEAM", "BOTTOM BARS Ld INTO THE",
                   "DEEPER BEAM; DEEP-BEAM BARS HOOKED UP"]
        for i, t in enumerate(lab):
            text(sp, t, P(-Lb, yb0 - 150 - i * 90), 2.0 * S, style="ANB" if i == 0 else "AN")


# ----------------------------------------------------------------------- 1114: stepped beam within a span (1:25)
STEP = 300                     # level shift drawn (step <= h)


def stepped_beam(ox, oy):
    """same depth h both sides, level shifted by STEP within the span (TATA Fig 2.43): step zone >= h long and
    h + step deep; bars are never cranked through the step - each set is anchored past the step zone"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L = 1900                                        # beam drawn each side of the step face
    Z = HB                                          # step zone length (>= h)
    lo = -STEP                                      # soffit of the lower part
    # concrete: upper part (0..HB) left, lower part (lo..HB+lo) right; step zone -Z..0 full depth lo..HB
    pline(sp, [P(-L, HB), P(0, HB), P(0, HB + lo), P(L, HB + lo)], "S-CONC")
    pline(sp, [P(-L, 0), P(-Z, 0), P(-Z, lo), P(L, lo)], "S-CONC")
    zbreak(sp, P(-L, -80), P(-L, HB + 80), S)
    zbreak(sp, P(L, lo - 80), P(L, HB + lo + 80), S)
    ut, ub = HB - YB, YB                           # upper part bars
    lt, lb = HB + lo - YB, lo + YB                 # lower part bars
    tl = 12 * DBM
    ext = 35 * DBM                                  # >= 35 db (and >= Ld) past the step zone (drawn)
    xz = -Z + YB + 45                               # far end of the step zone (inside the stirrups)
    # upper top bars: to the step face, 90 deg down through the step zone
    rbar(sp, [P(-L, ut), P(-YB, ut), P(-YB, lb + 60)])
    # lower top bars: straight through the step zone into the upper part
    rbar(sp, [P(L, lt), P(-Z - ext, lt)])
    # upper bottom bars: straight into the lower part
    rbar(sp, [P(-L, ub), P(ext, ub)])
    # lower bottom bars: through the step zone to its far end, 90 deg up
    rbar(sp, [P(L, lb), P(xz, lb), P(xz, lb + tl)])
    # stirrups. Step zone: full depth h + delta, a DOUBLE stirrup (2 at 30) just inside each face, uniform
    # spacing <= 100 between them; the bent-down upper top bar (at 59 from the step face) stays clear of them.
    # Upper and lower parts: normal spacing, first stirrup 100 from the zone faces.
    dL = [-Z + 45, -Z + 75]                             # double at the soffit step (x = -Z)
    dR = [-125, -95]                                   # double at the top step (x = 0), clear of the bar leg
    n_in = max(1, math.ceil((dR[0] - dL[1]) / 100))     # equal spaces <= 100 between the doubles
    zn = dL + [dL[1] + k * (dR[0] - dL[1]) / n_in for k in range(1, n_in)] + dR
    up = [x for x in rng(-L + 100, -Z - 100, 200)]
    dn = zone(0, L - 60, 200, first=100)
    stirrups(sp, P, up, y0=YS, y1=HB - YS)
    stirrups(sp, P, zn, y0=lo + YS, y1=HB - YS)
    stirrups(sp, P, dn, y0=lo + YS, y1=HB + lo - YS)
    # dimensions
    # dimensions: chains below the lower soffit, Δ and h on the left - the space above the beam is for notes
    dim(sp, P(0, lo), P(ext, lo), P(0, lo - 220), S, text="≥ 1.3 Ld")
    dim(sp, P(-Z - ext, 0), P(-Z, lo), P(0, lo - 550), S, text="≥ 1.3 Ld")
    dim(sp, P(-Z, lo), P(0, lo), P(0, lo - 550), S, text="≥ h")
    text(sp, "BOTTOM BARS", P(-80, lo - 220), 2.0 * S, align=TA.MIDDLE_RIGHT)
    text(sp, "TOP BARS", P(-Z - ext - 80, lo - 550), 2.0 * S, align=TA.MIDDLE_RIGHT)
    dim(sp, P(-Z, lo), P(-Z, 0), P(-Z - 250, 0), S, angle=90, text="Δ ≤ h")
    dim(sp, P(-L, 0), P(-L, HB), P(-L - 180, 0), S, angle=90, text="h")
    note_cfg(xR=P(L + 450, 0)[0], yminR=P(0, lo + 60)[1], upR=True)
    kr = P(L + 450, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 72, **kw)
    R((zn[3], HB / 2 + 80), "STEP ZONE ≥ h, DEPTH h + Δ: FULL-DEPTH CLOSED STIRRUPS @ ≤ 100 mm, DOUBLE AT "
                            "EACH FACE")
    R((-YB, ut - 200), "UPPER TOP BARS: TO THE STEP FACE, 90° DOWN")
    R((-Z - ext + 250, lt), "LOWER TOP BARS: THROUGH THE STEP ZONE, ≥ 1.3 Ld (CLASS B) INTO THE UPPER PART")
    R((ext - 250, ub), "UPPER BOTTOM BARS: ≥ 1.3 Ld (CLASS B) INTO THE LOWER PART")
    R((xz, lb + 200), "LOWER BOTTOM BARS: TO THE FAR END OF THE STEP ZONE, 90° UP")


# ----------------------------------------------------------------------- 1114: beam ending at a girder (1:25)
def girder_end(ox, oy):
    """secondary beam NOT continuous at a girder / spandrel (ACI MNL-66 BM-204; TATA p.180 case 3): section along
    the secondary beam, girder cut. Top bars over the girder top bars to the far side, 90 deg down inside the
    girder bars (ldh from the face); >= 2 bottom bars to the far side, 90 deg up; hanger stirrups in the girder"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    BG, L = 400, 1300                                  # girder width (cut); secondary beam drawn
    ys = HB - SEC_H
    pline(sp, [P(-L, ys), P(0, ys), P(0, 0), P(BG, 0), P(BG, HB), P(-L, HB)], "S-CONC")
    zbreak(sp, P(-L, ys - 80), P(-L, HB + 80), S)
    rb = rdot(DBM, S)
    R_ = rb + DS_ / 2
    cor = lambda x, y: (P(x, y)[0], P(x, y)[1], R_)
    yt_m = HB - YB - DROP                              # girder top bars one bar lower
    stirrup(sp, cor(YB, yt_m), cor(BG - YB, yt_m), cor(BG - YB, YB), cor(YB, YB), 6 * DS_ + 25)
    for x in (YB, BG - YB):
        dot(sp, P(x, yt_m), rb)
        dot(sp, P(x, YB), rb)
    tl = 12 * DBM + 60                                 # 90 deg hook tail (drawn)
    xt = BG - YB - 30                                  # top-bar hook leg, just inside the far girder bars
    xb = xt - 45                                       # bottom-bar hook leg, inside the top one
    ysb = ys + YB
    rbar(sp, [P(-L, HB - YB), P(xt, HB - YB), P(xt, HB - YB - tl)])        # top: over, to the far side, down
    rbar(sp, [P(-L, ysb), P(xb, ysb), P(xb, ysb + tl)])                    # bottom: to the far side, up
    stirrups(sp, P, zone(0, -L + 60, 150), y0=ys + YS)
    dim(sp, P(0, HB), P(xt + DBM / 2, HB), P(0, HB + 200), S, text="≥ ldh")
    dim(sp, P(-L, ys), P(-L, HB), P(-L - 180, 0), S, angle=90, text="h")
    note_cfg(xR=P(BG + 350, 0)[0])
    kr = P(BG + 350, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 50, **kw)
    dim(sp, P(-50, ys), P(0, ys), P(0, ys - 150), S, text="50", tside="L")       # first stirrup from the face
    # tips on the vertical legs, highest first: each horizontal run crosses only vertical lines
    R((BG - YB, yt_m), "GIRDER TOP BARS ONE BAR LOWER", ring=DBM)
    R((xt, 440), "TOP BARS OVER THE GIRDER TOP BARS, TO THE FAR SIDE, 90° DOWN INSIDE THE GIRDER BARS")
    R((BG - YS, 360), "GIRDER: HANGER STIRRUPS EACH SIDE OF THE BEAM (MIN. 3 @ 50 mm, AS 1113 DETAIL 2); "
                      "CLOSED, 135° HOOKS (TORSION)")
    R((xb, 280), "≥ 2 BOTTOM BARS TO THE FAR SIDE, 90° UP; OTHERS ≥ 150 mm INTO THE GIRDER")


# ----------------------------------------------------------------------- 1115: beam schedule (ACI MNL-66 BM-1)
def _tag(sp, P, x, ybar, ytag, letter, S):
    """bar letter of the schedule: dot on the bar, 60 deg leg, short shelf, bold letter"""
    dx = abs(ytag - ybar) / math.tan(math.radians(60))
    k = P(x + dx, ytag)
    dot(sp, P(x, ybar), 0.45 * S, "S-ANNO")
    line(sp, P(x, ybar), k, "S-ANNO")
    line(sp, k, P(x + dx + 120, ytag), "S-ANNO")
    text(sp, letter, P(x + dx + 170, ytag), 2.0 * S, align=TA.MIDDLE_LEFT, style="ANB")


PD_SCALE = 25


def placing(ox, oy):
    """1115/1: keyed placing diagram - end span and interior span, break before the next support (N.T.S.).
    Letters = schedule columns; cut-off points as 1112/1 (TATA Fig 2.27); stirrup zones S1 / S2"""
    S = PD_SCALE
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L = 3000                                         # clear spans drawn (N.T.S.)
    c1 = L                                           # left face of the interior column
    xe = c1 + COLW + 0.9 * L                         # break near the end of the interior span
    col_stack(sp, P, -COLW, COLW, -CUP, HB + CUP, S)
    col_stack(sp, P, c1, COLW, -CUP, HB + CUP, S, outer=False)
    for x0, x1 in ((0, c1), (c1 + COLW, xe)):
        line(sp, P(x0, 0), P(x1, 0), "S-CONC")
        line(sp, P(x0, HB), P(x1, HB), "S-CONC")
    zbreak(sp, P(xe, -80), P(xe, HB + 80), S)
    xh = -COLW + YB + 45
    yt, yb = HB - YB, YB
    tail = 12 * DBM + 60
    g = GAP
    L3 = L / 3
    # A: continuous top, hooked at the exterior support, lapped near midspan (cranked lap, lap_crank)
    xl0, xl1 = L / 2 - 550, L / 2 - 50               # top lap in the middle third; 1:6 crank ends >= 150 before C
    rbar(sp, [P(xh, yt - tail), P(xh, yt), P(xl1, yt)])
    rbar(sp, [P(*q) for q in lap_crank(xl0, xl1, yt, -g)] + [P(xe, yt)])
    # B: additional top at the exterior support, L1/4, 90 deg hook
    rbar(sp, [P(xh + g, yt - tail + 60), P(xh + g, yt - g), P(L / 4, yt - g)])
    # C: additional top at the interior support, L/3 each side
    rbar(sp, [P(c1 - L3, yt - g), P(c1 + COLW + L3, yt - g)])
    # D: continuous bottom, hooked at the exterior support, lapped (cranked) at the interior support
    xd1 = c1 + COLW - 100                            # end of the end-span bars (1:6 crank clear of E)
    rbar(sp, [P(xh + 2 * g, yb + tail), P(xh + 2 * g, yb), P(xd1, yb)])
    rbar(sp, [P(*q) for q in lap_crank(c1 - 200, xd1, yb, g)] + [P(xe, yb)])      # starts >= 150 after E
    # E: additional bottom - 0.875 L1 from the exterior face; 0.70 L2 centred (clear of the lap crank)
    for a, b_ in ((-150, 0.875 * L), (c1 + COLW + 0.15 * L, c1 + COLW + 0.85 * L)):
        rbar(sp, [P(a, yb + g), P(b_, yb + g)])               # additional bars one gap off the main bars
    # stirrups: S1 over 2h from each face (first 50), S2 between
    h2 = 2 * HB
    xs = zone(0, h2, 150) + zone(c1, c1 - h2, 150) + rng(h2 + 200, c1 - h2 - 100, 300)
    xs += zone(c1 + COLW, c1 + COLW + h2, 150) + rng(c1 + COLW + h2 + 200, xe - 80, 300)
    stirrups(sp, P, xs)
    # letters (schedule columns)
    yT, yB = HB + 260, -260
    for x, yy, t in ((400, yt - g, "B"), (900, yt, "A"), (2300, yt - g, "C"), (c1 + COLW + 1500, yt, "A")):
        _tag(sp, P, x, yy, yT, t, S)
    for x, yy, t in ((1100, yb, "D"), (1900, yb + g, "E"), (c1 + COLW + 900, yb, "D"),
                     (c1 + COLW + 1600, yb + g, "E")):
        _tag(sp, P, x, yy, yB, t, S)
    # dimensions - top: bar lengths; bottom: bottom-bar cut-offs, stirrup zones, clear span (nearest = shortest)
    yd = HB + CUP + 200
    top_rows = [("TOP BARS", [(0, L / 4, "L1/4"), (xl0, xl1, "LAP"), (c1 - L3, c1, "L/3"),
                              (c1 + COLW, c1 + COLW + L3, "L/3")])]
    for a, b, t in top_rows[0][1]:
        dim(sp, P(a, HB), P(b, HB), P(0, yd), S, text=t)
    row_label(sp, P, top_rows, 0, yd, S, avoid=(-COLW / 2, c1 + COLW / 2))
    ybub = yd + 250 + 3.5 * S                                           # grid bubbles above the top dimensions
    yd = -CUP - 250
    rows = [("BOTTOM BARS", [(0.875 * L, c1, "0.125 L1"), (c1 + COLW, c1 + COLW + 0.15 * L, "0.15 L2")]),
            ("STIRRUPS", [(0, h2, "S1: 2h"), (h2, c1 - h2, "S2"), (c1 - h2, c1, "S1: 2h"),
                          (c1 + COLW, c1 + COLW + h2, "S1: 2h")]),
            ("", [(0, c1, "L1 (CLEAR SPAN)")])]
    for i, (lab, row) in enumerate(rows):
        y_ = yd - i * 200
        for a, b, t in row:
            dim(sp, P(a, 0), P(b, 0), P(0, y_), S, text=t)
        if lab:
            row_label(sp, P, rows, i, y_, S, avoid=(-COLW / 2, c1 + COLW / 2))
    text(sp, "L2 (CLEAR SPAN) →", P(c1 + COLW + 200, yd - 400 + 60), 2.0 * S)
    grid_bubble(sp, P, -COLW / 2, ybub, yd - 2 * 200 - 120, "A", S)
    grid_bubble(sp, P, c1 + COLW / 2, ybub, yd - 2 * 200 - 120, "B", S)

def key_section(ox, oy):
    """1115/2: key section - where each lettered bar group sits (1:25)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    B, H, T, SL = BW, HB + 200, 120, 200            # an 800-deep beam: side bars shown
    pline(sp, [P(0, H - T), P(0, 0), P(B, 0), P(B, H - T)], "S-CONC")
    line(sp, P(-SL, H), P(B + SL, H), "S-CONC")
    for x0, x1, xz in ((-SL, 0, -SL), (B, B + SL, B + SL)):
        line(sp, P(x0, H - T), P(x1, H - T), "S-CONC")
        zbreak(sp, P(xz, H - T - 40), P(xz, H + 40), S)
    rb = rdot(DBM, S)
    R_ = rb + DS_ / 2
    cor = lambda x, y: (P(x, y)[0], P(x, y)[1], R_)
    stirrup(sp, cor(YB, H - YB), cor(B - YB, H - YB), cor(B - YB, YB), cor(YB, YB), 6 * DS_ + 25)
    for x in (YB, B / 2, B - YB):
        dot(sp, P(x, H - YB), rb)
        dot(sp, P(x, YB), rb)
    ysb = H / 2 - 60
    for x in (YB - 2, B - YB + 2):
        dot(sp, P(x, ysb), rdot(12, S))
    dim(sp, P(0, 0), P(0, H), P(-250, 0), S, angle=90, text="h")
    note_cfg(xR=P(B + SL + 200, 0)[0])
    kr = P(B + SL + 200, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 40, **kw)
    R((B / 2, H - YB), "B / C - ADDITIONAL TOP BARS", ring=DBM)          # first: its leg rises clear of bar A
    R((B - YB, H - YB), "A - CONTINUOUS TOP BARS (CORNERS)", ring=DBM)
    R((B - YS, H - 250), "S1 / S2 - STIRRUPS, TYPE (a) – (d), 1116 DETAIL 1")
    R((B - YB + 2, ysb), "SB - SIDE-FACE BARS, EACH FACE (h > 600 mm)", ring=12)
    R((B / 2, YB), "E - ADDITIONAL BOTTOM BARS", ring=DBM)
    R((B - YB, YB), "D - CONTINUOUS BOTTOM BARS (CORNERS)", ring=DBM)


# ----------------------------------------------------------------------- 1113: opening in the web (1:25)
def web_opening(ox, oy):
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L = 1150
    D0 = 150                                   # opening dia (h/4)
    yc = HB / 2
    for y in (0, HB):
        line(sp, P(-L, y), P(L, y), "S-CONC")
    zbreak(sp, P(-L, -80), P(-L, HB + 80), S)
    zbreak(sp, P(L, -80), P(L, HB + 80), S)
    sp.add_circle(P(0, yc), D0 / 2, dxfattribs=A("S-CONC"))
    yt, yb = HB - YB, YB
    rbar(sp, [P(-L, yt), P(L, yt)])
    rbar(sp, [P(-L, yb), P(L, yb)])
    le = 700                                   # extra horizontal bars: >= ld beyond the opening (drawn)
    for y in (yc + D0 / 2 + 45, yc - D0 / 2 - 45):
        rbar(sp, [P(-le, y), P(le, y)], db=12)
    for sx in (-1, 1):                         # diagonal bars each side of the opening
        c = sx * (D0 / 2 + 120)
        for sy in (-1, 1):
            rbar(sp, [P(c - 170 * sy, yc - 170), P(c + 170 * sy, yc + 170)], db=12)
    xs_ = [D0 / 2 + 40, D0 / 2 + 90] + rng(D0 / 2 + 300, L - 60, 200)
    stirrups(sp, P, xs_ + [-x for x in xs_])
    for x in (-40, 40):                        # short chord stirrups above / below
        line(sp, P(x, yc + D0 / 2 + 20), P(x, HB - YS), "S-REBR-SEC")
        line(sp, P(x, YS), P(x, yc - D0 / 2 - 20), "S-REBR-SEC")
    dim(sp, P(-D0 / 2, yc), P(D0 / 2, yc), P(0, HB + 200), S, text="d0 ≤ h/4")
    dim(sp, P(-L, 0), P(-L, HB / 3), P(-L - 150, 0), S, angle=90, text="h/3")
    dim(sp, P(-L, HB / 3), P(-L, 2 * HB / 3), P(-L - 150, 0), S, angle=90, text="h/3")
    dim(sp, P(-L, 2 * HB / 3), P(-L, HB), P(-L - 150, 0), S, angle=90, text="h/3")
    note_cfg(xR=P(L + 300, 0)[0])
    kr = P(L + 300, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 46, **kw)
    R((le - 100, yc + D0 / 2 + 45), "2-DB12 ABOVE AND BELOW, ≥ ld PAST THE OPENING")
    R((D0 / 2 + 120 + 100, yc + 100), "DIAGONAL BARS EACH SIDE, EACH FACE (≥ 50 % OF V)", )
    R((D0 / 2 + 90, HB / 2 - 150), "2 FULL-DEPTH STIRRUPS EACH SIDE, CLOSE TO THE OPENING")
    R((40, YS + 60), "SHORT STIRRUPS IN THE CHORDS")
    R((L - 300, HB / 2), "OPENING IN THE MIDDLE THIRD; ≥ h/2 CLEAR FROM SUPPORT FACES, POINT LOADS AND OTHER "
                         "OPENINGS; NOT IN 2h ZONES OF SEISMIC FRAMES")


# ----------------------------------------------------------------------- 1111: stirrup and hoop types (1:25)
def ustirrup(sp, tl, tr, br, bl, leg, layer="S-REBR-SEC"):
    """open U-stirrup with 135 deg seismic hooks round both top corner bars, tails into the core"""
    def pt(c, a):
        return (c[0] + c[2] * math.cos(math.radians(a)), c[1] + c[2] * math.sin(math.radians(a)))
    b = lambda deg: math.tan(math.radians(deg) / 4)
    pl, pr = pt(tl, 45), pt(tr, 135)
    pts = [(pl[0] + leg * 0.7071, pl[1] - leg * 0.7071, 0), (*pl, b(135)), (*pt(tl, 180), 0),
           (*pt(bl, 180), b(90)), (*pt(bl, 270), 0), (*pt(br, 270), b(90)), (*pt(br, 0), 0),
           (*pt(tr, 0), b(135)), (*pr, 0), (pr[0] - leg * 0.7071, pr[1] - leg * 0.7071, 0)]
    return sp.add_lwpolyline(pts, format="xyb", dxfattribs=A(layer))


def stirrup90(sp, tl, tr, br, bl, leg, gap, layer="S-REBR-SEC"):
    """closed stirrup with 90 deg hooks at the top-left bar (DPT Fig 5.2-8 (a)): one end bends round the bar and
    runs along the top as a 6 db tail; the other (drawn 'gap' outside) bends round and runs down the left side"""
    def pt(c, a, r=None):
        r = c[2] if r is None else r
        return (c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))
    b = lambda deg: math.tan(math.radians(deg) / 4)
    r2 = tl[2] + gap
    p90 = pt(tl, 90)
    pts = [(p90[0] + leg, p90[1], 0), (*p90, b(90)), (*pt(tl, 180), 0),
           (*pt(bl, 180), b(90)), (*pt(bl, 270), 0), (*pt(br, 270), b(90)), (*pt(br, 0), 0),
           (*pt(tr, 0), b(90)), (*pt(tr, 90, r2), 0), (*pt(tl, 90, r2), b(90)), (*pt(tl, 180, r2), 0),
           (pt(tl, 180, r2)[0], pt(tl, 180, r2)[1] - leg, 0)]
    return sp.add_lwpolyline(pts, format="xyb", dxfattribs=A(layer))


def stirrup_types(ox, oy):
    S = 25
    sp = msp
    note_cfg(free=True)
    rb = rdot(DBM, S)
    R_ = rb + DS_ / 2
    leg = 6 * DS_ + 25                     # 6 db >= 75 (drawn)
    B, H, T, SL = BW, HB, 120, 150          # section, slab, slab stub drawn

    def section(cx, cy, n, kind, label, slab="BOTH", B=B):
        P = lambda x, y: (ox + cx + x, oy + cy + y)
        left = slab in ("BOTH", "L")
        right = slab in ("BOTH", "R")
        outline = [P(0, H - T) if left else P(0, H), P(0, 0), P(B, 0), P(B, H - T) if right else P(B, H)]
        pline(sp, outline, "S-CONC")
        xl = -SL if left else 0
        xr = B + SL if right else B
        line(sp, P(xl, H), P(xr, H), "S-CONC")
        if left:
            line(sp, P(-SL, H - T), P(0, H - T), "S-CONC")
            zbreak(sp, P(-SL, H - T - 40), P(-SL, H + 40), S)
        if right:
            line(sp, P(B, H - T), P(B + SL, H - T), "S-CONC")
            zbreak(sp, P(B + SL, H - T - 40), P(B + SL, H + 40), S)
        xs = [YB + i * (B - 2 * YB) / (n - 1) for i in range(n)]
        cor = lambda x, y: (P(x, y)[0], P(x, y)[1], R_)
        tl, tr, br, bl = cor(xs[0], H - YB), cor(xs[-1], H - YB), cor(xs[-1], YB), cor(xs[0], YB)
        if kind == "CLOSED":
            stirrup(sp, tl, tr, br, bl, leg)
        elif kind == "CAP":
            ustirrup(sp, tl, tr, br, bl, leg)
            crosstie(sp, P(xs[0], H - YB), P(xs[-1], H - YB), R_ + max(DS_, 0.5 * S), leg)
        elif kind == "DOUBLE":
            stirrup(sp, tl, tr, br, bl, leg)
            stirrup(sp, cor(xs[1], H - YB), cor(xs[2], H - YB), cor(xs[2], YB), cor(xs[1], YB), leg)
        elif kind == "HOOK90":
            stirrup90(sp, tl, tr, br, bl, leg, max(DS_, 0.5 * S))
        for x in xs:
            dot(sp, P(x, H - YB), rb)
            dot(sp, P(x, YB), rb)
        for i, t in enumerate(label):
            if t:
                text(sp, t, P(xl, -150 - i * 105), 2.0 * S, style="ANB" if i == 0 else "AN")

    g = 1000
    section(0, 1100, 3, "CLOSED", ["(a) CLOSED STIRRUP", "135° + 6 db ≥ 75 mm", "ALL BEAMS, TORSION, SPANDREL"])
    section(g, 1100, 3, "CAP", ["(b) U-STIRRUP + CAP TIE", "SEISMIC HOOKS; 90° END OF", "THE CAP ON THE SLAB SIDE",
                                "NOT FOR TORSION BEAMS"],
            slab="R")
    section(-30, 0, 4, "DOUBLE", ["(c) 4 LEGS: 2 CLOSED", "STIRRUPS (≥ 4 BARS)", ""], B=360)
    section(g, 0, 3, "HOOK90", ["(d) 90° + 6 db ≥ 75 mm", "ORDINARY / INTERMEDIATE,", "NOT IN 2h OF PUBLIC BLDGS"])


# ======================================================================= tables and notes
BEAM_TABLE = [
    ["USE (DPT T2.3-1)", "SEISMIC CATEGORY B ONLY (R = 3)", "CATEGORY B, C; D ONLY ≤ 40 m, FORCES + 40 % (R = 5)",
     "ALL CATEGORIES (R = 8)"],
    ["SECTION", "h ≥ ℓ/16, ℓ/18.5, ℓ/21, ℓ/8 (NO DEFLECTION CHECK)", "AS ORDINARY",
     "ln ≥ 4 d; bw ≥ LESSER OF 0.3 h AND 250 mm; WIDTH ≤ COLUMN + LESSER OF c2, ¾ c1 EACH SIDE"],
    ["LONGITUDINAL BARS", "≥ 2 TOP + 2 BOTTOM CONTINUOUS; As ≥ 1.4 bw d / fy",
     "+Mn AT FACE ≥ 1/3 −Mn; ANY SECTION ≥ 1/5 MAX", "≥ 2 TOP + 2 BOTTOM CONTINUOUS; ρ ≤ 0.025; +Mn AT FACE ≥ ½ −Mn; "
                                                     "ANY SECTION ≥ ¼ MAX"],
    ["END ZONE", "–", "2h FROM EACH FACE", "2h FROM EACH FACE AND EACH SIDE OF ANY HINGE"],
    ["FIRST STIRRUP", "50 mm FROM THE FACE", "≤ 50 mm FROM THE FACE", "≤ 50 mm FROM THE FACE"],
    ["SPACING IN 2h", "–", "s1 ≤ min (d/4, 8 db, 24 dt, 300)", "CLOSED HOOPS, s1 ≤ min (d/4, 6 db, 24 dt, 150): STRICTER OF DPT AND ACI 318"],
    ["SPACING ELSEWHERE", "s ≤ d/2, 600 (d/4, 300 IF Vs > 0.33√f'c bw d)", "≤ d/2",
     "≤ d/2, SEISMIC HOOKS BOTH ENDS"],
    ["HOOKS", "90° + 6 db (≤ DB16); 135° + 6 db FOR CLOSED / TORSION STIRRUPS",
     "90° + 6 db ≥ 75 mm; 135° OR HOOK-CLIP IN 2h FOR PUBLIC / DUCTILE BUILDINGS (DPT; ACI 318: HOOPS)",
     "135° + 6 db ≥ 75 mm; CAP TIE 135° / 90°, 90° ENDS ALTERNATE (ALL ON THE SLAB SIDE IF ONE SLAB)"],
    ["LAP LOCATION", "TOP NEAR MIDSPAN; BOTTOM AT OR NEAR THE SUPPORT", "AS ORDINARY, BUT NOT WITHIN 2h",
     "NOT IN JOINTS, 2h ZONES OR HINGES; HOOPS @ ≤ d/4, 100 mm OVER THE LAP"],
    ["EXTERIOR JOINT", "BARS ANCHORED FOR fy: 90° HOOK, ldh FROM THE FACE",
     "90° HOOKS AT THE FAR SIDE, ldh FROM THE FACE", "TO THE FAR FACE OF THE CORE; ldh ≥ 8 db, 150, fy db / (5.3√f'c)"],
    ["REFERENCE", "EIT 011008 7.13, 9.5, 11.4, 12.9 – 12.14; DPT 5.2.6", "DPT 1301/1302 5.2.7.3, 5.2.7.6",
     "DPT 1301/1302 5.2.8, 5.2.10"],
]


BEAM_NOTES = [
    ("1.", f"THESE DETAILS APPLY WHERE THE BEAM DRAWINGS DO NOT SHOW OTHERWISE. FRAME TYPE AND SEISMIC CATEGORY: "
           f"SEE THE DESIGN CRITERIA; REINFORCEMENT BY FRAME TYPE: {TAB('BFRAME')}."),
    ("2.", f"COVER TO STIRRUPS: 40 mm INTERIOR; 50 mm (≥ DB20) / 40 mm (≤ DB16) EXPOSED; 75 mm CAST AGAINST EARTH ({TAB('COVER')})."),
    ("3.", "AT LEAST ONE BAR IN EACH CORNER; ≥ 2 TOP AND 2 BOTTOM BARS CONTINUOUS OVER THE FULL LENGTH, "
           "ANCHORED AT END SUPPORTS. PERIMETER BEAMS: CONTINUOUS TOP ≥ 1/6 OF THE SUPPORT TOP BARS (LAP AT "
           "MIDSPAN), CONTINUOUS BOTTOM ≥ 1/4 OF THE MIDSPAN BOTTOM BARS (LAP AT THE SUPPORT), CLASS B, CLOSED "
           "STIRRUPS OVER THE WHOLE SPAN; INTEGRITY BARS PASS INSIDE THE COLUMN BARS. [EIT 011008 7.13.2; DPT 5.2.6]"),
    ("4.", "CLEAR SPACING ≥ db, 25 mm AND 4/3 MAX. AGGREGATE. LAYERS DIRECTLY ABOVE EACH OTHER, CLEAR ≥ 25 mm AND ≥ db. "
           "[EIT 011008 7.6]"),
    ("5.", "STIRRUPS CLOSED, HOOKS AT THE TOP (SLAB SIDE); FIRST STIRRUP 50 mm FROM THE SUPPORT FACE. "
           "STIRRUPS ENCLOSE COMPRESSION BARS AT s ≤ 16 db, 48 dt. SPECIAL-FRAME HOOP ZONES: EVERY CORNER AND "
           "ALTERNATE BAR HELD BY A HOOP CORNER OR CROSSTIE, NO BAR > 150 mm CLEAR FROM A HELD BAR. INTERMEDIATE AND "
           "SPECIAL FRAMES: DEFORMED HOOPS AND CROSSTIES, DB10 MIN. SPECIAL-FRAME HOOPS: THE STRICTER OF DPT 5.2.8.3.2 "
           "(d/4, 8 db, 24 dt, 300) AND ACI 318-11 21.5.3.2 (d/4, 6 db, 150). [EIT 011008 7.11, 7.10.5.3; DPT 5.2.8.3.3]"),
    ("6.", f"LAPS: CLASS B PER {TAB('LAPS')}, ADJACENT LAPS STAGGERED ≥ 1.0 m; NO LAPS FOR BARS > DB36. "
           "COUPLERS ≥ 1.25 fy. [EIT 011008 12.13, 12.14]"),
    ("7.", "BAR ENDS ON THE ELEVATIONS: A PLAIN END (NO MARK) MEANS THE BAR STOPS THERE (END OF AN "
           "ADDITIONAL OR LAPPED BAR); NO MARK AT A BREAK LINE MEANS THE BAR CONTINUES. KEY ON 1112."),
    ("8.", "CUT-OFF AND CANTILEVER: 1112. SECTIONS, EDGE AND TORSION BEAMS, SIDE-FACE BARS, SECONDARY BEAMS, END ANCHORAGE AND OPENINGS: 1113. LEVEL CHANGES AND STEPS: 1114. SCHEDULE: 1115. "
           "NO CORING OR SLEEVES THROUGH BEAMS WITHOUT THE ENGINEER'S APPROVAL."),
]


SEC_NOTES = [
    ("1.", "BEAMS CROSSING AT A COLUMN: THE DRAWINGS STATE WHICH BARS ARE OUTERMOST; DEFAULT - MAIN (DEEPER) BEAM "
           "BARS OUTSIDE, OTHER DIRECTION INSIDE THEM, TOP AND BOTTOM."),
    ("2.", "SECONDARY BEAM ON A MAIN BEAM: SECONDARY TOP BARS OVER THE MAIN TOP BARS; SECONDARY BOTTOM BARS ON THE "
           "MAIN BOTTOM BARS OR ON THE HANGERS (DETAIL 2, SECTION A)."),
    ("3.", "BEAM SUPPORTING A COLUMN: COLUMN BARS TO THE BOTTOM LAYER, 90° HOOKS; COLUMN TIES THROUGH THE BEAM; "
           "SEE 1104 DETAIL 2."),
    ("4.", "DEEP BEAMS (ln ≤ 4 h OR A POINT LOAD WITHIN 2h OF A SUPPORT): PER DESIGN; WEB BARS BOTH FACES, "
           "s ≤ d/5 AND 300. [EIT 011008 10.7, 11.7]"),
    ("5.", "LEVEL CHANGES, STEPPED BEAMS, BEAM ENDING AT A GIRDER: 1114."),
    ("6.", "EDGE AND TORSION BEAMS: CLOSED STIRRUPS, 135° HOOKS, s ≤ ph/8 AND 300 mm, CONTINUED bt + d BEYOND THE "
           "POINT NEEDED; LONGITUDINAL BARS AROUND THE PERIMETER @ ≤ 300 mm, ONE IN EACH CORNER, ≥ DB10, DEVELOPED "
           "(HOOKED) AT BOTH ENDS. [EIT 011008 11.5]"),
    ("7.", "SIDE-FACE BARS WHERE h > 600 mm: DB12 BOTH FACES OVER THE FULL WEB DEPTH (THE TENSION FACE CHANGES "
           "ALONG A CONTINUOUS BEAM), @ ≤ 250 mm, THE FIRST ≤ 150 mm BELOW THE SLAB; LAPPED AND ANCHORED 40 db INTO "
           "SUPPORTS. [TATA; EIT 011008 10.6.4]"),
]


SCHED_HEADS = ["MARK", "b × h (mm)", "FRAME", "A TOP CONT.", "B TOP EXT.", "C TOP INT.", "D BOT. CONT.", "E BOT. ADD.",
               "SB EACH FACE", "S1, 2h ZONES (@ mm)", "S2, REST (@ mm)", "TYPE", "REMARKS"]
SCHED_ROWS = [
    ["B1", "300 × 600", "ORD.", "2-DB20", "1-DB20", "2-DB20", "2-DB20", "1-DB20", "–", "–", "RB9 @ 200", "(a)", ""],
    ["B2", "300 × 600", "INT.", "2-DB20", "2-DB16", "2-DB20", "3-DB20", "–", "–", "DB10 @ 125", "DB10 @ 250", "(a)", ""],
    ["B3", "400 × 800", "SPE.", "3-DB25", "2-DB25", "3-DB25", "3-DB25", "2-DB25", "2-DB12", "DB10 @ 100", "DB10 @ 200",
     "(a)", "PERIMETER: A, D INTEGRITY BARS"],
    ["CB1", "300 × 500", "ORD.", "3-DB20", "–", "–", "2-DB16", "–", "–", "–", "RB9 @ 150", "(a)", "CANTILEVER, 1112 DETAIL 2"],
    ["", "", "", "", "", "", "", "", "", "", "", "", ""],
]
SCHED_NOTES = [
    ("1.", "EACH BAR GROUP IS GIVEN BY ITS LETTER ON THE PLACING DIAGRAM (DETAIL 1) AND THE KEY SECTION (DETAIL 2). "
           "CUT-OFF POINTS AS DETAIL 1 (= 1112 DETAIL 1) UNLESS THE SCHEDULE GIVES A LENGTH. NUMBER OF BARS PER "
           "SECTION, ONE LAYER UNLESS \"(2ND)\" IS ADDED; L = THE LARGER ADJACENT CLEAR SPAN."),
    ("2.", "MARKS AS ON THE FRAMING PLANS. ONE MARK = ONE SECTION AND ONE SET OF BARS OVER ALL ITS SPANS; WHERE SPANS "
           "DIFFER, LIST THEM AS B1-1, B1-2 … (SPANS NUMBERED FROM THE LEFT OR THE BOTTOM OF THE PLAN)."),
    ("3.", "STIRRUPS: \"DB10 @ 125 mm\" GIVES THE SPACING; \"n-DB10 @ 125 mm\" GIVES THE NUMBER OF STIRRUPS, NOT SPACES. "
           "FIRST STIRRUP 50 mm FROM EACH FACE. S1 OVER 2h FROM EACH FACE (INTERMEDIATE, SPECIAL); ORDINARY: S2 "
           "THROUGHOUT UNLESS S1 IS GIVEN. TYPE (a) – (d): 1116 DETAIL 1."),
    ("4.", "FRAME: ORD. / INT. / SPE. MOMENT FRAME PER THE DESIGN CRITERIA; ZONES, LAPS AND HOOPS PER 1111. A LAPPED "
           "NEAR MIDSPAN, D AT OR NEAR THE SUPPORTS (NOT WITHIN 2h IN INTERMEDIATE AND SPECIAL FRAMES), CLASS B PER "
           f"{TAB('LAPS')}."),
    ("5.", "A AND D: ≥ 2 BARS EACH, CONTINUOUS. PERIMETER BEAMS: A ≥ 1/6 OF (A + C), D ≥ 1/4 OF (D + E), CLOSED "
           "STIRRUPS OVER THE WHOLE SPAN (1116 NOTE 3)."),
    ("6.", "SB WHERE h > 600 mm (1113 NOTE 7). TORSION BEAMS: \"T\" IN REMARKS - CLOSED STIRRUPS TYPE (a), BARS "
           "DEVELOPED AT BOTH ENDS (1113 NOTE 6)."),
    ("7.", "CANTILEVERS, BEAMS ENDING AT A GIRDER, STEPPED BEAMS: NAMED IN REMARKS; THE TYPICAL DETAIL (1112, 1114) "
           "GOVERNS THE BAR SHAPES. VALUES IN THE EXAMPLE ROWS ARE ILLUSTRATIVE ONLY."),
    ("8.", "THE CONTRACTOR'S BAR-BENDING SCHEDULE (BAR MARKS, SHAPES, LENGTHS) IS PREPARED FROM THIS SCHEDULE AND "
           "SUBMITTED FOR REVIEW BEFORE FABRICATION."),
]


LEVEL_NOTES = [
    ("1.", "NEVER CRANK A CONTINUOUS TENSION BAR THROUGH A CHANGE OF LEVEL OR A RE-ENTRANT CORNER: USE SEPARATE BARS, "
           "EACH ANCHORED Ld (STRAIGHT) OR BY A 90° HOOK."),
    ("2.", "SMALL SOFFIT DIFFERENCE AT A COLUMN: BOTTOM BARS MAY BE CRANKED INSIDE THE COLUMN AT ≤ 1:6, WITH DOUBLE "
           "STIRRUPS AT EACH BEND; OTHERWISE SEPARATE BARS LAPPED Ld."),
    ("3.", "HAUNCHED SOFFIT: SLOPED AND SPAN BOTTOM BARS EACH EXTEND Ld PAST THE KINK; DOUBLE STIRRUPS AT THE KINKS."),
    ("4.", "STEP Δ > h: STEP BLOCK ≥ h WIDE WITH HORIZONTAL TIES, OR A STUB COLUMN CARRYING THE UPPER BEAM - "
           "PER DESIGN."),
    ("5.", "NOTCHED OR RECESSED BEAMS: SEPARATE BARS ANCHORED PAST EACH RE-ENTRANT CORNER."),
    ("6.", "BEAM ENDING AT A GIRDER (DETAIL 3): THE GIRDER MUST HOLD ldh OF THE TOP BARS - OTHERWISE SMALLER OR "
           "HEADED BARS PER DESIGN. SLAB CONTINUOUS BEYOND THE GIRDER: THE TOP BARS MAY RUN ON INTO THE SLAB, Ld PAST "
           "THE FAR FACE. GIRDER TORSION FROM THE BEAM END: PER DESIGN, 1113 NOTE 6. [ACI MNL-66 BM-204]"),
]


def build():
    EXT.update({
        # views sit 8 m apart in model space so no viewport window shows a neighbour's notes
        "ORD": capture(beam_elev, 0, 0, "ORD"),
        "IMF": capture(beam_elev, 0, -8000, "IMF"),
        "SMF": capture(beam_elev, 0, -16000, "SMF"),
        "ST": capture(stirrup_types, 20000, 0),
        "CB": capture(cutoff, 0, -24000),
        "CT": capture(cantilever, 0, -32000),
        "EA": capture(end_anchor, 20000, -24000),
        "TX": capture(typ_section, 0, -40000),
        "SM": capture(sec_on_main, 6000, -40000),
        "SE": capture(sec_end, 0, -48000),
        "WO": capture(web_opening, 20000, -48000),
        "LV": capture(levels, 0, -56000),
        "SB": capture(stepped_beam, 0, -64000),
        "GE": capture(girder_end, 0, -72000),
        "PD": capture(placing, 0, -80000),
        "KS": capture(key_section, 20000, -80000),
    })
    sheet_1111()
    sheet_1112()
    sheet_1113()
    sheet_1114()
    sheet_1115()
    sheet_1116()


# ======================================================================= sheet 1111
def sheet_1111():
    ps = new_sheet(0)
    top = FY1 - 3
    names = [("ORD", "BEAM - ORDINARY MOMENT FRAME"), ("IMF", "BEAM - INTERMEDIATE MOMENT FRAME"),
             ("SMF", "BEAM - SPECIAL MOMENT FRAME")]
    hs = [(EXT[k][3] - EXT[k][1]) / 25 + 2 * PAD for k, _ in names]
    gap = max(0.0, (top - (FY0 + 3) - sum(hs) - 3 * 18) / 2)       # spread the three views down the sheet
    y = top
    for i, (k, nm) in enumerate(names):
        px, pw, ph = viewport(ps, k, 25, FX0 + 1, y)
        view_title(ps, None, y - ph - 6, nm, "N.T.S.", (str(i + 1), "1111"))
        y = y - ph - 18 - gap


# ======================================================================= sheet 1112
def sheet_1112():
    ps = new_sheet(1)
    top = FY1 - 3
    px, pw, ph1 = viewport(ps, "CB", 25, FX0 + 1, top)
    view_title(ps, None, top - ph1 - 6, "CONTINUOUS BEAM - BAR CUT-OFF", "N.T.S.", ("1", "1112"),
               note="UNIFORM LOAD, ADJACENT SPANS WITHIN 20 %, LL ≤ 3 DL (EIT 011008 8.3.3); OTHERWISE PER DESIGN")
    top2 = top - ph1 - 16 - 8
    px, pw, ph3 = viewport(ps, "CT", 25, FX0 + 1, top2)
    view_title(ps, None, top2 - ph3 - 6, "CANTILEVER BEAM", "N.T.S.", ("2", "1112"),
               note="NO BACK SPAN: TOP BARS THROUGH THE COLUMN, 90° DOWN AT THE FAR FACE, Ld FROM THE FACE")
    bar_end_legend(ps, FX0 + 3, top2 - ph3 - 22, 200)            # the bar-end key of the beam sheets


# ======================================================================= sheet 1113
def sheet_1113():
    ps = new_sheet(2)
    top = FY1 - 3
    x = FX0 + 1
    px, pw, ph1 = viewport(ps, "TX", 25, x, top)
    view_title(ps, None, top - ph1 - 6, "TYPICAL BEAM SECTION", "N.T.S.", ("1", "1113"))
    px, pw, ph2 = viewport(ps, "SM", 25, px + pw + 4, top)
    view_title(ps, None, top - ph2 - 6, "SECONDARY BEAM ON A MAIN BEAM", "N.T.S.", ("2", "1113"),
               note="SECTION ALONG THE MAIN BEAM; SECONDARY BEAM DASHED")
    top2 = top - max(ph1, ph2) - 22
    px, pw, ph3 = viewport(ps, "SE", 25, FX0 + 1, top2)
    view_title(ps, None, top2 - ph3 - 6, "SECTION ALONG THE SECONDARY BEAM", "N.T.S.", ("A", "1113"), triangles=True)
    xn = px + pw + 8
    notes_block(ps, xn, top2, TBX - xn - 3, "NOTES TO 1113", SEC_NOTES)   # full width (bar-end key: 1112, 1114)
    top3 = top2 - ph3 - 22
    px, pw, ph4 = viewport(ps, "WO", 25, FX0 + 1, top3)
    view_title(ps, None, top3 - ph4 - 6, "OPENING THROUGH THE WEB", "N.T.S.", ("3", "1113"),
               note="LARGER OPENINGS (DEPTH ≤ h/2): PER DESIGN")
    px, pw, ph5 = viewport(ps, "EA", 25, px + pw + 4, top3 + 4)
    view_title(ps, None, top3 + 4 - ph5 - 6, "BEAM END AT AN EXTERIOR COLUMN", "N.T.S.", ("4", "1113"))


# ======================================================================= sheet 1114
def sheet_1114():
    ps = new_sheet(3)
    top = FY1 - 3
    px, pw, ph1 = viewport(ps, "LV", 25, FX0 + 1, top)
    view_title(ps, None, top - ph1 - 6, "BEAMS AT DIFFERENT LEVELS AT A COLUMN", "N.T.S.", ("1", "1114"),
               note="LEVEL DIFFERENCE > h: PER DESIGN (STEP BLOCK OR STUB COLUMN)")
    top2 = top - ph1 - 22
    px, pw, ph2 = viewport(ps, "SB", 25, FX0 + 1, top2)
    view_title(ps, None, top2 - ph2 - 6, "STEPPED BEAM WITHIN A SPAN", "N.T.S.", ("2", "1114"),
               note="SAME DEPTH h EACH SIDE, LEVEL SHIFT Δ ≤ h; NO BAR CRANKED THROUGH THE STEP; "
                    "STEP UP OR DOWN: SAME DETAIL, MIRRORED")
    top3 = top2 - ph2 - 24
    px, pw, ph3 = viewport(ps, "GE", 25, FX0 + 1, top3)
    view_title(ps, None, top3 - ph3 - 6, "BEAM ENDING AT A GIRDER", "N.T.S.", ("3", "1114"),
               note="SECTION ALONG THE BEAM; NOT CONTINUOUS AT THE GIRDER")
    xn = px + pw + 8
    notes_block(ps, xn, top3, TBX - xn - 3, "NOTES TO 1114", LEVEL_NOTES)


# ======================================================================= sheet 1115
def sheet_1115():
    ps = new_sheet(4)
    top = FY1 - 3
    px, pw, ph1 = viewport(ps, "PD", 25, FX0 + 1, top)
    if px + pw > TBX - 1:
        warn(f"1115 placing diagram runs into the title strip: {px + pw:.0f} > {TBX - 1:.0f}")
    view_title(ps, None, top - ph1 - 6, "BEAM BARS PLACING DIAGRAM", "N.T.S.", ("1", "1115"),
               note=f"LETTERS = COLUMNS OF {TAB('BSCHED')}; SPANS SCHEMATIC")
    ytab = top - ph1 - 24                                          # schedule under the diagram, full width
    w = [12, 19, 13, 18, 18, 18, 18, 18, 17, 22, 22, 11]
    yb = tbl(ps, FX0 + 3, ytab, w + [TBX - FX0 - 7 - sum(w)], SCHED_HEADS, SCHED_ROWS, "LCCCCCCCCCCCL",
             title=TABT("BSCHED"))
    top3 = yb - 12                                                 # key section + notes
    px2, pw2, ph2 = viewport(ps, "KS", 25, FX0 + 1, top3)
    view_title(ps, None, top3 - ph2 - 6, "KEY SECTION", "N.T.S.", ("2", "1115"))
    xn = px2 + pw2 + 8
    notes_block(ps, xn, top3, TBX - xn - 3, "NOTES TO 1115", SCHED_NOTES)


# ======================================================================= sheet 1116 (R2: 1111 is filled by the 1:25 elevations)
def sheet_1116():
    ps = new_sheet(5)
    top = FY1 - 3
    px, pw, ph = viewport(ps, "ST", 25, FX0 + 1, top)
    view_title(ps, None, top - ph - 6, "STIRRUP AND HOOP TYPES", "N.T.S.", ("1", "1116"))
    xn = px + pw + 10
    notes_block(ps, xn, top, TBX - xn - 3, "TYPICAL BEAM NOTES", BEAM_NOTES)
    ytab = top - ph - 26
    yb = tbl(ps, FX0 + 3, ytab, [30, 88, 90, 106], ["ITEM", "ORDINARY", "INTERMEDIATE", "SPECIAL"], BEAM_TABLE,
             "LCCC", title=TABT("BFRAME"))
    print(f"  table bottom {yb:.1f}")
