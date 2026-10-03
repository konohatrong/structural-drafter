"""
Typical slab details - STR-ST-1121 (slabs on beams), 1122 (flat slabs), 1123 (openings, steps, edges),
1124 (slab on ground).
Sources : EIT 011008-21 ch. 7, 9, 10, 11.11, 13 (Fig 13.3.8); DPT 1301/1302-61 cl. 5.2.12, 2.11.5, 2.9;
          TATA RC detailing handbook ch. 3 + appendix sheets. See SOURCES_SLAB_DETAILING.md.
Rules   : dimensions on one side of a view, notes on the other (no leader crosses a dimension); bar-end key on
          every sheet with bar ends / laps; views >= 8 m apart in model space.
"""
from td_engine import *

BASE = "STR-ST-1121_Typical_Slab_Details_A3_RevA"
SHEETS[:] = [("1121", ["TYPICAL SLAB DETAILS (1)", "SLABS ON BEAMS"], "AS SHOWN"),
             ("1122", ["TYPICAL SLAB DETAILS (2)", "FLAT SLAB BAR EXTENSIONS"], "AS SHOWN"),
             ("1123", ["TYPICAL SLAB DETAILS (3)", "FLAT SLAB AT THE COLUMN"], "AS SHOWN"),
             ("1124", ["TYPICAL SLAB DETAILS (4)", "PUNCHING SHEAR REINFORCEMENT"], "AS SHOWN"),
             ("1125", ["TYPICAL SLAB DETAILS (5)", "OPENINGS"], "AS SHOWN"),
             ("1126", ["TYPICAL SLAB DETAILS (6)", "STEPS AND EDGES"], "AS SHOWN"),
             ("1127", ["TYPICAL SLAB DETAILS (7)", "SLAB ON GROUND"], "AS SHOWN")]

T = 120                        # slab thickness (drawn)
CS = 20                        # cover to slab bars (EIT 011008 7.7.1, not exposed, <= DB16)
DBS = 10                       # slab bar DB10 (drawn)
YB1 = CS + DBS / 2             # 25  bottom outer layer (short-span bars)
YT1 = T - CS - DBS / 2         # 95  top outer layer
BB, HBM = 250, 500             # supporting beam (drawn): width, depth below the slab top
CVB = 40                       # beam cover to stirrup
DTB = 9
DBB = 20


def rbar(sp, pts, db=DBS, layer="S-REBR"):
    return bar(sp, pts, db, layer)


def beam_cut(sp, P, x0, S):
    """supporting beam cut in section under the slab: outline, stirrup, 4 corner bars (top of beam = slab top)"""
    yb = T - HBM
    pline(sp, [P(x0, 0), P(x0, yb), P(x0 + BB, yb), P(x0 + BB, 0)], "S-CONC")
    rb = rdot(DBB, S)
    R_ = rb + DTB / 2
    c = CVB + DTB + DBB / 2
    cor = lambda x, y: (P(x, y)[0], P(x, y)[1], R_)
    ytb = T - c - 20                                  # beam top bars under the slab top mat
    stirrup(sp, cor(x0 + c, ytb), cor(x0 + BB - c, ytb), cor(x0 + BB - c, yb + c), cor(x0 + c, yb + c), 6 * DTB + 25)
    for x in (x0 + c, x0 + BB - c):
        dot(sp, P(x, ytb), rb)
        dot(sp, P(x, yb + c), rb)


def dots(sp, P, x0, x1, y, S, s=200):
    """distribution bars (other direction) seen end-on"""
    r = rdot(DBS, S) * 0.8
    x = x0
    while x <= x1 + 1e-6:
        dot(sp, P(x, y), r)
        x += s


# ----------------------------------------------------------------------- 1121/1: section along the short span (1:25)
def short_section(ox, oy):
    """edge beam | end span Sn | interior beam | part of the next span: TATA Figs 3.4 - 3.10 cut-offs"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    SN = 2700                                          # clear short span (drawn)
    xi0, xi1 = SN, SN + BB                             # interior beam
    xe = xi1 + 1300                                    # break in the next span
    # slab + beams
    line(sp, P(-BB, T), P(xe, T), "S-CONC")
    line(sp, P(0, 0), P(xi0, 0), "S-CONC")
    line(sp, P(xi1, 0), P(xe, 0), "S-CONC")
    line(sp, P(-BB, T), P(-BB, T - HBM), "S-CONC")
    beam_cut(sp, P, -BB, S)
    beam_cut(sp, P, xi0, S)
    zbreak(sp, P(xe, -60), P(xe, T + 60), S)
    # bottom (short-span) bars: full span, into the supports; next span starts over the interior beam
    rbar(sp, [P(-BB + 60, YB1), P(xi0 + 200, YB1)])
    rbar(sp, [P(*q) for q in lap_crank(xi0 + 50, xi0 + 200, YB1, 25)] + [P(xe, YB1)])       # cranked lap
    # top bars: Sn/4 at the edge beam (90 deg hook down), Sn/3 each side of the interior beam
    x_e = SN / 4
    rbar(sp, [P(-BB + 60, YT1 - 150), P(-BB + 60, YT1), P(x_e, YT1)])
    xa0, xa1 = xi0 - SN / 3, xi1 + SN / 3
    rbar(sp, [P(xa0, YT1), P(xa1, YT1)])
    # distribution bars (inside the short-span bars)
    yd_b, yd_t = YB1 + DBS, YT1 - DBS
    dots(sp, P, 100, SN - 100, yd_b, S)
    dots(sp, P, xi1 + 100, xe - 100, yd_b, S)
    dots(sp, P, 100, x_e - 50, yd_t, S)
    dots(sp, P, xa0 + 50, xi0 - 100, yd_t, S)
    dots(sp, P, xi1 + 100, xa1 - 50, yd_t, S)
    # dimensions: all below the beams
    yb = T - HBM
    yd = yb - 280
    rows = [("TOP BARS", [(0, x_e, "Sn/4"), (xa0, xi0, "Sn/3"), (xi1, xa1, "Sn/3")]),
            ("", [(0, xi0, "Sn (CLEAR SHORT SPAN)")])]
    for i, (lab, row) in enumerate(rows):
        y_ = yd - i * 300
        for a, b, t in row:
            dim(sp, P(a, 0), P(b, 0), P(0, y_), S, text=t)
        if lab:
            text(sp, lab, P(-BB - 120, y_), 2.0 * S, align=TA.MIDDLE_RIGHT)
    dim(sp, P(-BB, 0), P(-BB, T), P(-BB - 200, 0), S, angle=90, text="t")
    # notes: right column, above the slab soffit
    note_cfg(xR=P(xe + 400, 0)[0], yminR=P(0, 20)[1], upR=True)
    kr = P(xe + 400, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 80, **kw)
    R((x_e - 250, YT1), "TOP BARS: Sn/4 AT A DISCONTINUOUS EDGE, 90° HOOK DOWN INTO THE EDGE BEAM; Sn/3 EACH SIDE OF "
                        "AN INTERIOR BEAM, Sn = LARGER ADJACENT SPAN")
    R((1500, YB1), "BOTTOM BARS: FULL SPAN, ≥ 150 INTO EACH SUPPORT (TO THE FAR SIDE OF AN EDGE BEAM)")
    R((1100, yd_b), "SHORT-SPAN BARS OUTERMOST, TOP AND BOTTOM; DISTRIBUTION BARS INSIDE THEM")
    R((xa1 - 250, YT1), "ALTERNATE BENT-UP OPTION: CRANK AT Sn/7 (EDGE) AND Sn/4 (INTERIOR) FROM THE FACE, "
                        "EXTRA TOP BARS @ 2 s")
    R((xi0 + BB / 2, T - 60), "SLAB TOP BARS PASS OVER THE BEAM TOP BARS")


# ----------------------------------------------------------------------- 1121/2: two-way corner panel, plan (1:100)
def corner_panel(ox, oy):
    """exterior corner panel: edge beams left and bottom, interior beams right and top. Representative top bars
    in each edge band (with their extent), bottom bars both ways, corner zone L/5 x L/5 (EIT 13.3.6, TATA Fig 3.25)"""
    S = 100
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    SN, LN = 3600, 4800                                # clear spans: short (x), long (y)
    b = BB
    # beams (below the slab: hidden outlines), slab edge = outer face of the edge beams
    for x0 in (-b, SN):
        pline(sp, [P(x0, -b), P(x0 + b, -b), P(x0 + b, LN + 600), P(x0, LN + 600)], "S-CONC-HIDN")
    for y0 in (-b, LN):
        pline(sp, [P(-b, y0), P(SN + b + 600, y0), P(SN + b + 600, y0 + b), P(-b, y0 + b)], "S-CONC-HIDN")
    line(sp, P(-b, -b), P(-b, LN + 600), "S-CONC-VIS")
    line(sp, P(-b, -b), P(SN + b + 600, -b), "S-CONC-VIS")
    zbreak(sp, P(-b - 60, LN + 600), P(SN + b + 600, LN + 600), S)
    zbreak(sp, P(SN + b + 600, -b - 60), P(SN + b + 600, LN + 600), S)
    # corner zone L/5 x L/5 (L = longer clear span)
    c = LN / 5
    pline(sp, [P(0, 0), P(c, 0), P(c, c), P(0, c)], "S-ANNO", close=True)
    hatch(sp, [P(0, 0), P(c, 0), P(c, c), P(0, c)], "ANSI31", pscale("ANSI31", S, 2.0))
    # representative bottom bars (full span each way)
    xm, ym = SN * 0.62, LN * 0.55
    rbar(sp, [P(-b + 60, ym), P(SN + 150, ym)], db=12)                         # short direction, lower layer
    rbar(sp, [P(xm, -b + 60), P(xm, LN + 150)], db=12)                         # long direction
    # representative top bars, one per edge band (plain ends: no end mark)
    yt = LN * 0.35
    rbar(sp, [P(-b + 60, yt), P(SN / 4, yt)], db=12)
    rbar(sp, [P(SN - SN / 3, yt), P(SN + b + 500, yt)], db=12)
    xt = SN * 0.35
    rbar(sp, [P(xt, -b + 60), P(xt, LN / 4)], db=12)
    rbar(sp, [P(xt, LN - LN / 3), P(xt, LN + b + 500)], db=12)
    # dimensions: left and below (notes on the right)
    yd = -b - 350
    for a, b_, t in ((0, SN / 4, "Sn/4"), (SN - SN / 3, SN, "Sn/3")):
        dim(sp, P(a, -b), P(b_, -b), P(0, yd), S, text=t)
    dim(sp, P(0, -b), P(SN, -b), P(0, yd - 350), S, text="Sn")
    xd = -b - 350
    dim(sp, P(-b, 0), P(-b, LN / 4), P(xd, 0), S, angle=90, text="Ln/4")
    dim(sp, P(-b, LN - LN / 3), P(-b, LN), P(xd, 0), S, angle=90, text="Ln/3")
    dim(sp, P(-b, 0), P(-b, LN), P(xd - 350, 0), S, angle=90, text="Ln")
    note_cfg(xR=P(SN + b + 900, 0)[0])
    kr = P(SN + b + 900, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 56, **kw)
    R((SN - SN / 3 + 400, yt), "TOP BARS, EACH DIRECTION: 1/4 OF THE CLEAR SPAN AT EDGE BEAMS (HOOKED DOWN), 1/3 AT "
                               "INTERIOR BEAMS")
    R((SN * 0.85, ym), "BOTTOM BARS: SHORT DIRECTION IN THE LOWER LAYER, LONG DIRECTION ON TOP OF THEM")
    R((c * 0.7, c * 0.3), "EXTERIOR CORNER, EDGE BEAMS αf > 1.0: EXTRA TOP AND BOTTOM BARS OVER L/5 x L/5 "
                          "(L = LONGER CLEAR SPAN), EACH FOR THE MAX. POSITIVE MOMENT; SPACING = SMALLER MIDSPAN SPACING")
    text(sp, "L/5", P(c / 2, c + 120), 2.0 * S, align=TA.BOTTOM_CENTER)
    text(sp, "EDGE BEAM", P(-b / 2, LN * 0.8), 2.0 * S, align=TA.MIDDLE_CENTER, rot=90)


# ----------------------------------------------------------------------- 1121/3: cantilever slab (1:25)
def cant_slab(ox, oy):
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    LC = 1100                                          # cantilever from the beam face
    LB = 1400                                          # back span drawn
    x0 = 0                                             # beam at 0..BB
    xt = BB + LC
    line(sp, P(-LB, T), P(xt, T), "S-CONC")
    line(sp, P(-LB, 0), P(0, 0), "S-CONC")
    line(sp, P(BB, 0), P(xt, 0), "S-CONC")
    line(sp, P(xt, 0), P(xt, T), "S-CONC")
    beam_cut(sp, P, 0, S)
    zbreak(sp, P(-LB, -60), P(-LB, T + 60), S)
    ld = 1100                                          # drawn back length
    rbar(sp, [P(-ld, YT1), P(xt - CS - 5, YT1), P(xt - CS - 5, YB1 + 10)])
    rbar(sp, [P(-LB, YB1), P(BB + 150, YB1)])
    rbar(sp, [P(*q) for q in lap_crank(60, BB + 150, YB1, 25)] + [P(xt - CS - 5, YB1)])       # cranked lap
    dots(sp, P, BB + 100, xt - 100, YT1 - DBS, S)
    dots(sp, P, -ld + 50, -100, YT1 - DBS, S)
    dots(sp, P, -LB + 100, -100, YB1 + DBS, S)
    dots(sp, P, BB + 100, xt - 100, YB1 + DBS, S)
    yb = T - HBM
    yd = yb - 280
    dim(sp, P(-ld, 0), P(0, 0), P(0, yd), S, text="≥ Ld, Lc, Sn/3")
    dim(sp, P(BB, 0), P(xt, 0), P(0, yd), S, text="Lc")
    note_cfg(xR=P(xt + 350, 0)[0], yminR=P(0, 20)[1], upR=True)
    kr = P(xt + 350, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 42, **kw)
    R((-ld + 300, YT1), "TOP BARS INTO THE BACK SPAN ≥ Ld, ≥ THE CANTILEVER LENGTH Lc AND ≥ ITS Sn/3 TOP-BAR "
                        "LENGTH")
    R((xt - CS - 5, YB1 + 60), "TOP BARS TURNED DOWN AT THE FREE EDGE")
    R((BB + 600, YB1), "BOTTOM BARS (≥ MIN. STEEL) ANCHORED INTO THE BEAM")
    R((BB + 400, YT1 - DBS), "DISTRIBUTION BARS INSIDE THE MAIN BARS")


# ----------------------------------------------------------------------- 1122: flat slab strips (EIT Fig 13.3.8)
HF = 200                       # flat slab thickness (real - used on the plan: c2 + 3h band)
HFD = 560                     # slab depth drawn on the strip diagrams (SCHEMATIC - exaggerated so bar groups read)
CF = 500                       # column (drawn)
LNF = 4500                     # clear span (drawn, true proportion along the span)
YBF = 80                       # bottom bars (schematic)
YTF = HFD - 80                 # top bars (schematic)
GF = 75                        # offset between bar groups (schematic)


def fs_frame(sp, P, S, drop=False, columns=True):
    """exterior column (x -CF..0), span 0..LNF, interior column (LNF..LNF+CF), part of the next span.
    Returns xe (break) and the drop-panel extents."""
    xi0, xi1 = LNF, LNF + CF
    xe = xi1 + 0.42 * LNF
    L = LNF + CF                                       # c/c span
    hd = 160                                            # drop projection drawn (>= h/4, schematic)
    xd = (xi0 + CF / 2 - L / 6, xi0 + CF / 2 + L / 6) if drop else None
    xde = -CF / 2 + L / 6 if drop else None
    # slab outline (with drops)
    top = [P(-CF, HFD), P(xe, HFD)]
    line(sp, *top, "S-CONC")
    bot = [P(-CF, HFD), P(-CF, -hd if drop else 0)]
    if drop:
        pts = [P(-CF, -hd), P(xde, -hd), P(xde, 0), P(xd[0], 0), P(xd[0], -hd), P(xd[1], -hd), P(xd[1], 0), P(xe, 0)]
    else:
        pts = [P(-CF, 0), P(xe, 0)]
    pline(sp, bot + pts, "S-CONC")
    zbreak(sp, P(xe, (-hd if drop else 0) - 60), P(xe, HFD + 60), S)
    if columns:                                        # columns below (to the soffit / drop) and above the slab
        y_s = -hd if drop else 0
        yb, yt = y_s - 300, HFD + 300
        for x0 in (-CF, xi0):
            for x in (x0, x0 + CF):
                if not (x == -CF):                     # exterior face: the slab edge line continues it below
                    line(sp, P(x, yb), P(x, y_s), "S-CONC-VIS")
                line(sp, P(x, HFD), P(x, yt), "S-CONC-VIS")
            zbreak(sp, P(x0 - 60, yb), P(x0 + CF + 60, yb), S)
            zbreak(sp, P(x0 - 60, yt), P(x0 + CF + 60, yt), S)
        line(sp, P(-CF, yb), P(-CF, y_s), "S-CONC-VIS")
    else:                                              # middle strip: support faces as grey reference lines
        for x in (0, xi0, xi1):
            line(sp, P(x, -250), P(x, HFD + 250), "S-CENT")
    return xi0, xi1, xe, xd, xde


def col_strip(ox, oy, drop):
    S = 50
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    xi0, xi1, xe, xd, xde = fs_frame(sp, P, S, drop)
    k = 0.33 if drop else 0.30
    xh = -CF + 45                                      # hooks inside the column bars at the slab edge
    tl = 300
    # top: group A (>= 50 %) k ln, group B (rest) 0.20 ln; hooked down at the edge
    rbar(sp, [P(xh, YTF - tl), P(xh, YTF), P(k * LNF, YTF)])
    rbar(sp, [P(xh + GF, YTF - GF - tl + 30), P(xh + GF, YTF - GF), P(0.20 * LNF, YTF - GF)])
    rbar(sp, [P(xi0 - k * LNF, YTF), P(xi1 + k * LNF, YTF)])
    rbar(sp, [P(xi0 - 0.20 * LNF, YTF - GF), P(xi1 + 0.20 * LNF, YTF - GF)])
    # bottom: all continuous; lap only over the interior support; >= 150 into the exterior support
    rbar(sp, [P(-150, YBF), P(xi1 + 350, YBF)])
    rbar(sp, [P(*q) for q in lap_crank(xi0 - 350, xi1 + 350, YBF, GF)] + [P(xe, YBF)])      # cranked lap
    # integrity bars: >= 2 through the column core, hooked up at the exterior edge
    rbar(sp, [P(xh + 2 * GF, YBF + 2 * GF + 100), P(xh + 2 * GF, YBF + 2 * GF), P(xe, YBF + 2 * GF)])
    # dimensions below, labelled rows; notes right, above the soffit
    yd = (-160 if drop else 0) - 300 - 260
    # tiers: 0.20 ln lies inside k ln, so it sits nearer the slab (no extension line crosses a dimension
    # line). The drop panel (>= L/6 from the column centreline) is not dimensioned here: its points fall
    # inside the face-based top-bar dimensions on any tier. It is given in the note and in 1123 (2).
    rows = [("TOP BARS", [(0, 0.20 * LNF, "0.20 ℓn"), (xi0 - 0.20 * LNF, xi0, "0.20 ℓn"),
                          (xi1, xi1 + 0.20 * LNF, "0.20 ℓn")]),
            ("", [(0, k * LNF, f"{k:.2f} ℓn"), (xi0 - k * LNF, xi0, f"{k:.2f} ℓn"), (xi1, xi1 + k * LNF, f"{k:.2f} ℓn")]),
            ("", [(0, xi0, "ℓn (CLEAR SPAN, FACE TO FACE)")])]
    for i, (lab, row) in enumerate(rows):
        y_ = yd - i * 280
        for a, b, t in row:
            dim(sp, P(a, 0), P(b, 0), P(0, y_), S, text=t)
        if lab:
            text(sp, lab, P(-CF - 150, y_), 2.0 * S, align=TA.MIDDLE_RIGHT)
    note_cfg(xR=P(xe + 350, 0)[0], yminR=P(0, 20)[1], upR=True)
    kr = P(xe + 350, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 70, **kw)
    R((k * LNF - 300, YTF), f"≥ 50 % OF THE TOP BARS {k:.2f} ℓn FROM THE FACE, THE REST 0.20 ℓn; "
                                  "HOOKED DOWN AT THE SLAB EDGE")
    R((LNF * 0.35, YBF), "ALL BOTTOM BARS CONTINUOUS OR CLASS B LAPPED OVER THE INTERIOR SUPPORT ONLY; "
                            "≥ 150 INTO THE EXTERIOR SUPPORT")
    R((LNF * 0.62, YBF + 2 * GF), "≥ 2 BOTTOM BARS EACH WAY THROUGH THE COLUMN CORE, ANCHORED AT EXTERIOR "
                                "SUPPORTS (INTEGRITY)")
    if drop:
        R((xd[0] + 150, -80), "DROP PANEL ≥ h/4 BELOW THE SLAB, ≥ L/6 FROM THE COLUMN CENTRELINE "
                                   "EACH WAY (L = c/c SPAN)")


def mid_strip(ox, oy):
    S = 50
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    xi0, xi1, xe, _, _ = fs_frame(sp, P, S, False, columns=False)
    xh = -CF + 45
    tl = 300
    k = 0.22
    rbar(sp, [P(xh, YTF - tl), P(xh, YTF), P(k * LNF, YTF)])
    rbar(sp, [P(xi0 - k * LNF, YTF), P(xi1 + k * LNF, YTF)])
    # bottom: >= 50 % continuous, 150 into the supports; the rest may stop <= 0.15 ln from the interior face
    rbar(sp, [P(-150, YBF), P(xi0 + 150, YBF)])
    rbar(sp, [P(xi1 - 150, YBF), P(xe, YBF)])
    rbar(sp, [P(-150, YBF + GF), P(xi0 - 0.15 * LNF, YBF + GF)])
    rbar(sp, [P(xi1 + 0.15 * LNF, YBF + GF), P(xe, YBF + GF)])
    yd = -250 - 300
    # tiers: the bottom-bar dimensions lie inside the top-bar ones, so they sit nearer the slab
    rows = [("BOTTOM BARS", [(xi0 - 0.15 * LNF, xi0, "≤ 0.15 ℓn"), (xi1, xi1 + 0.15 * LNF, "≤ 0.15 ℓn")]),
            ("TOP BARS", [(0, k * LNF, "0.22 ℓn"), (xi0 - k * LNF, xi0, "0.22 ℓn"), (xi1, xi1 + k * LNF, "0.22 ℓn")]),
            ("", [(0, xi0, "ℓn (CLEAR SPAN, FACE TO FACE)")])]
    for i, (lab, row) in enumerate(rows):
        y_ = yd - i * 280
        for a, b, t in row:
            dim(sp, P(a, 0), P(b, 0), P(0, y_), S, text=t)
        if lab:
            text(sp, lab, P(-CF - 150, y_), 2.0 * S, align=TA.MIDDLE_RIGHT)
    text(sp, "FACE OF SUPPORT", P(xi0 - 60, HFD + 260), 2.0 * S, align=TA.BOTTOM_RIGHT)
    note_cfg(xR=P(xe + 350, 0)[0], yminR=P(0, 20)[1], upR=True)
    kr = P(xe + 350, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 70, **kw)
    R((k * LNF - 300, YTF), "ALL TOP BARS 0.22 ℓn FROM THE FACE; HOOKED DOWN AT THE SLAB EDGE")
    R((LNF * 0.35, YBF), "≥ 50 % OF THE BOTTOM BARS CONTINUOUS, 150 INTO EVERY SUPPORT")
    R((xi0 - 0.15 * LNF - 400, YBF + GF), "THE REST MAY STOP ≤ 0.15 ℓn FROM THE INTERIOR FACE; 150 INTO THE EXTERIOR SUPPORT")


def strip_plan(ox, oy):
    """interior panel between four columns: column / middle strips, drop panels, c2 + 3h band, integrity bars"""
    S = 100
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L1, L2 = 5000, 6000                               # c/c spans (x, y)
    c = CF
    w = 0.25 * min(L1, L2)                            # half column-strip width
    for (x, y) in ((0, 0), (L1, 0), (0, L2), (L1, L2)):
        pts = [P(x - c / 2, y - c / 2), P(x + c / 2, y - c / 2), P(x + c / 2, y + c / 2), P(x - c / 2, y + c / 2)]
        pline(sp, pts, "S-CONC", close=True)
        hatch(sp, pts, "ANSI31", pscale("ANSI31", S, 0.8))
        dx, dy = L1 / 6, L2 / 6                                   # drop panel, >= L/6 each way
        pline(sp, [P(x - dx, y - dy), P(x + dx, y - dy), P(x + dx, y + dy), P(x - dx, y + dy)], "S-CONC-HIDN",
              close=True)
    # strip boundaries (grid lines + strip edges)
    for x in (0, L1):
        line(sp, P(x, -900), P(x, L2 + 900), "S-CENT")
    for y in (0, L2):
        line(sp, P(-900, y), P(L1 + 900, y), "S-CENT")
    for x in (w, L1 - w):
        line(sp, P(x, -600), P(x, L2 + 600), "S-ANNO")
    for y in (w, L2 - w):
        line(sp, P(-600, y), P(L1 + 600, y), "S-ANNO")
    # effective width for moment transfer at the column (c2 + 3h)
    e = c / 2 + 1.5 * HF
    pline(sp, [P(L1 - e, -e), P(L1 + e, -e), P(L1 + e, e), P(L1 - e, e)], "S-ANNO", close=True)
    # integrity bars through the column core (2 each way)
    for d in (-60, 60):
        rbar(sp, [P(L1 - 1300, d), P(L1 + 800, d)], db=12)
        rbar(sp, [P(L1 + d, -800), P(L1 + d, 1300)], db=12)
    text(sp, "COLUMN STRIP", P(L1 / 2, w / 2), 2.0 * S, align=TA.MIDDLE_CENTER)
    text(sp, "MIDDLE STRIP", P(L1 / 2, L2 / 2), 2.0 * S, align=TA.MIDDLE_CENTER)
    text(sp, "COLUMN STRIP", P(w / 2, L2 / 2), 2.0 * S, align=TA.MIDDLE_CENTER, rot=90)
    yd = -L2 / 6 - 400                                # below the drop-panel outline: no line through the texts
    dim(sp, P(0, 0), P(w, 0), P(0, yd), S, text="0.25 L")
    dim(sp, P(w, 0), P(L1 - w, 0), P(0, yd), S, text="MIDDLE STRIP")
    dim(sp, P(L1 - w, 0), P(L1, 0), P(0, yd), S, text="0.25 L")
    dim(sp, P(0, 0), P(L1, 0), P(0, yd - 350), S, text="L1 (c/c)")
    xd = -900 - 300
    dim(sp, P(0, 0), P(0, L2 / 6), P(xd, 0), S, angle=90, text="≥ L2/6", tside="R")   # text beyond, in line
    dim(sp, P(0, 0), P(0, L2), P(xd - 350, 0), S, angle=90, text="L2 (c/c)")
    note_cfg(xR=P(L1 + 1200, 0)[0])
    kr = P(L1 + 1200, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 40, **kw)
    R((L1 + e, e * 0.5), "c2 + 3h BAND: TOP BARS FOR γf Mu CONCENTRATED HERE (≥ ½ OF THE COLUMN-STRIP TOP BARS "
                         "IN SEISMIC FRAMES)")
    R((L1 + 60, 1100), "≥ 2 BOTTOM BARS EACH WAY THROUGH THE COLUMN CORE")
    R((L1 - L1 / 6, L2 / 6 * 0.6), "DROP PANEL (IF ANY) ≥ L/6 EACH WAY FROM THE COLUMN CENTRELINE")
    R((L1 - w, L2 * 0.4), "COLUMN STRIP: 0.25 × SMALLER SPAN EACH SIDE OF THE COLUMN LINE")


# ----------------------------------------------------------------------- 1123: drop panel and column capital (1:50)
def drop_capital(ox, oy):
    """section through an interior column head: drop panel >= h/4 deep and >= L/6 each way (EIT 13.2.5);
    capital sides >= 45 deg, size <= L/4 (TATA p.74); critical sections d/2 from the capital and from the drop edge"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    h, c = HF, CF
    L = 6000                                           # c/c span (for L/6, L/4)
    hd = 120                                           # drop projection (>= h/4 = 50)
    xd = L / 6                                         # drop edge from the column centreline
    hc = 400                                           # capital depth below the drop
    wc = c / 2 + hc                                    # capital half-width at the top (45 deg)
    xs = 1200
    yb = -hd - hc - 250
    # concrete outline: slab + drop + capital + column
    line(sp, P(-xs, h), P(xs, h), "S-CONC")
    pline(sp, [P(-xs, 0), P(-xd, 0), P(-xd, -hd), P(-wc, -hd), P(-c / 2, -hd - hc), P(-c / 2, yb)], "S-CONC")
    pline(sp, [P(xs, 0), P(xd, 0), P(xd, -hd), P(wc, -hd), P(c / 2, -hd - hc), P(c / 2, yb)], "S-CONC")
    for x in (-c / 2, c / 2):
        line(sp, P(x, h), P(x, h + 300), "S-CONC")
    zbreak(sp, P(-xs, -60), P(-xs, h + 60), S)
    zbreak(sp, P(xs, -60), P(xs, h + 60), S)
    zbreak(sp, P(-c / 2 - 60, yb), P(c / 2 + 60, yb), S)
    zbreak(sp, P(-c / 2 - 60, h + 300), P(c / 2 + 60, h + 300), S)
    # bars: slab top and bottom, column bars through the head, capital cage (inclined bars + hoops)
    rbar(sp, [P(-xs, h - 30), P(xs, h - 30)], db=12)
    rbar(sp, [P(-xs, 30), P(xs, 30)], db=12)
    # capital cage: inclined bars PARALLEL to the 45 deg capital face at cover (bar centre ec from the face,
    # measured square to it): leg down inside the column cage, inclined leg, leg up into the drop panel
    ec = 50
    k45 = ec * math.sqrt(2)                           # vertical shift of a 45 deg line offset ec square to it
    xin = lambda y: y + c / 2 + hd + hc - k45         # bar line: x at level y (right side)
    xl = c / 2 - 90                                   # lower leg, inside the column bars
    for sx in (-1, 1):
        rbar(sp, [P(sx * (c / 2 - 60), yb), P(sx * (c / 2 - 60), h - 50)], db=20)
        ylo = xl - c / 2 - hd - hc + k45              # level where the bar line meets the lower leg
        rbar(sp, [P(sx * xl, ylo - 200), P(sx * xl, ylo), P(sx * xin(-hd), -hd), P(sx * xin(-hd), 60)], db=12)
    for y in (-hd - hc + 150, -hd - 150):             # hoops round the inclined bars
        line(sp, P(-xin(y), y), P(xin(y), y), "S-REBR-SEC")
    # critical sections (dashed): d/2 outside the capital top edge, d/2 outside the drop edge
    dd = (h + hd - 40) / 2
    for x in (wc + dd, xd + (h - 40) / 2):
        line(sp, P(x, -hd - 60), P(x, h + 120), "S-CENT")
    # dimensions: below and left; notes right, above the soffit
    yd = yb - 220
    # tiers: the capital lies inside the drop panel, so it sits nearer; the drop panel is dimensioned over its
    # full width (a half-width from the centreline would start inside the capital dimension)
    dim(sp, P(-wc, -hd), P(wc, -hd), P(0, yd), S, text="CAPITAL ≤ L/4")
    dim(sp, P(-xd, -hd), P(xd, -hd), P(0, yd - 260), S, text="DROP ≥ L/3 (L/6 EACH WAY)")
    dim(sp, P(-xd, -hd), P(-xd, 0), P(-xs - 150, 0), S, angle=90, text="≥ h/4")
    dim(sp, P(-xs, 0), P(-xs, h), P(-xs - 150, 0), S, angle=90, text="h")
    line(sp, P(0, yb - 100), P(0, h + 420), "S-CENT")          # centreline stops above the dimensions
    note_cfg(xR=P(xs + 250, 0)[0], yminR=P(0, 20)[1], upR=True)
    kr = P(xs + 250, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 44, **kw)
    R((xd + (h - 40) / 2, h + 60), "CRITICAL SECTIONS: d/2 FROM THE CAPITAL (DROP DEPTH) AND d/2 OUTSIDE THE DROP "
                                   "EDGE (SLAB DEPTH)")
    R((wc - 100, -hd - 60), "CAPITAL: SIDES ≥ 45°, CAGE OF INCLINED BARS AND HOOPS; COLUMN CAST TO THE UNDERSIDE "
                            "OF THE HEAD FIRST")
    R((c / 2 - 60, h - 120), "COLUMN BARS CONTINUE UP THROUGH THE HEAD INTO THE SLAB")
    R((xd - 200, -hd), "DROP PANEL ≥ h/4 BELOW THE SLAB, ≥ L/6 EACH WAY FROM THE COLUMN CENTRELINE")


# ----------------------------------------------------------------------- 1124: punching shear reinforcement
DP = 160                        # effective depth d of the flat slab (h = 200)


def punch_plan(ox, oy, kind):
    """interior column, plan (1:25). kind STIR: closed stirrups in 4 arms (EIT 11.11.3);
    STUD: headed stud rails, orthogonal + diagonal (EIT 11.11.5)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    c = CF
    h2 = c / 2
    pts = [P(-h2, -h2), P(h2, -h2), P(h2, h2), P(-h2, h2)]
    pline(sp, pts, "S-CONC", close=True)
    hatch(sp, pts, "ANSI31", pscale("ANSI31", S, 1.0))
    e = h2 + DP / 2                                  # critical section d/2 from the face
    pline(sp, [P(-e, -e), P(e, -e), P(e, e), P(-e, e)], "S-ZONE-DASH", close=True)    # notional line: fine dashed
    s0, s = DP / 4, DP / 2 if kind == "STIR" else 0.75 * DP     # first line d/4 (<= d/2): clear of the d/2 section
    n = 5
    lines_ = [h2 + s0 + k * s for k in range(n)]
    reach = lines_[-1]
    if kind == "STIR":
        wa = c - 2 * 60                              # arm (beam) width: stirrup legs over the column width
        for ang in (0, 90, 180, 270):
            ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            R_ = lambda u, v: P(u * ca - v * sa, u * sa + v * ca)
            for u in lines_:
                line(sp, R_(u, -wa / 2), R_(u, wa / 2), "S-REBR-SEC")       # stirrup (seen from above)
            for v in (-wa / 2, wa / 2):
                rbar(sp, [R_(h2 - 60, v), R_(reach + 150, v)], db=12)        # arm longitudinal bars
    else:
        for ang in range(0, 360, 45):
            ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            if ang % 90:
                r0 = h2 * math.sqrt(2)
            else:
                r0 = h2
            u0 = r0 + s0 - (0 if ang % 90 == 0 else 0)
            us = [u0 + k * s for k in range(n)]
            line(sp, P((r0 + 20) * ca, (r0 + 20) * sa), P((us[-1] + 40) * ca, (us[-1] + 40) * sa), "S-REBR-SEC")
            for u in us:
                sp.add_circle(P(u * ca, u * sa), 22, dxfattribs=A("S-REBR"))
    # dimensions (below + left) and notes (right)
    note_cfg(xR=P(reach + 450, 0)[0])
    kr = P(reach + 450, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 46, **kw)
    if kind == "STIR":
        R((lines_[2], c / 2 - 60), "CLOSED STIRRUP LINES @ ≤ d/2, FIRST ≤ d/2 FROM THE FACE; LEGS ≤ 2d APART")
        R((reach + 100, c / 2 - 60), "≥ 4 BARS PER ARM, ENGAGED BY THE STIRRUPS")
    else:
        R((lines_[2], 0), "STUD LINES: FIRST ≤ d/2; s ≤ 0.75d (vu ≤ φ0.5√f'c) ELSE 0.5d; ≤ 2d APART ON THE FIRST LINE")
    R((e, e * 0.6), "CRITICAL SECTION d/2 FROM THE FACE")
    R((reach, (c / 2 - 60) if kind == "STIR" else 0), "LINES CONTINUE UNTIL vu ≤ φ0.17√f'c AT d/2 BEYOND THE OUTERMOST LINE")


def punch_section(ox, oy, kind):
    """section through the slab at the column (1:10): stirrup cage or stud rail with the flexural bars"""
    S = 10
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    h, c = HF, CF
    L = 640
    line(sp, P(-c / 2 - 60, h), P(L, h), "S-CONC")
    line(sp, P(c / 2, 0), P(L, 0), "S-CONC")
    for x in (-c / 2, c / 2):
        line(sp, P(x, -300), P(x, 0 if x > 0 else -300), "S-CONC-VIS")
        line(sp, P(x, h), P(x, h + 250), "S-CONC-VIS")
    line(sp, P(-c / 2, -300), P(-c / 2, h + 250), "S-CONC-VIS")
    zbreak(sp, P(L, -60), P(L, h + 60), S)
    zbreak(sp, P(-c / 2 - 60, -300), P(c / 2 + 60, -300), S)
    zbreak(sp, P(-c / 2 - 60, h + 250), P(c / 2 + 60, h + 250), S)
    yt, yb = h - CS - 6, CS + 6
    rb = rdot(12, S)
    rbar(sp, [P(-c / 2 - 60, yt), P(L, yt)], db=12)
    rbar(sp, [P(-c / 2 + 40, yb), P(L, yb)], db=12)
    s0, s = DP / 2, DP / 2 if kind == "STIR" else 0.75 * DP
    xs = [c / 2 + s0 + k * s for k in range(4 if kind == "STIR" else 3)]
    if kind == "STIR":
        for x in xs:
            pline(sp, [P(x - 4, yb - 10), P(x - 4, yt + 10)], "S-REBR-SEC")
            dot(sp, P(x + 8, yt - 12), rb)
            dot(sp, P(x + 8, yb + 12), rb)
    else:
        yr = CS                                            # base rail on the bottom cover
        rbar(sp, [P(xs[0] - 40, yr), P(xs[-1] + 40, yr)], db=8, layer="S-REBR-SEC")
        for x in xs:
            line(sp, P(x, yr), P(x, yt - 12), "S-REBR-SEC")
            pline(sp, [P(x - 15, yt - 12), P(x + 15, yt - 12)], "S-REBR")
    dim(sp, P(c / 2, 0), P(xs[0], 0), P(0, -120), S, text="≤ d/2")
    dim(sp, P(xs[0], 0), P(xs[1], 0), P(0, -120), S, text="≤ d/2" if kind == "STIR" else "s")
    if len(xs) > 2:
        dim(sp, P(xs[1], 0), P(xs[2], 0), P(0, -120), S, text="≤ d/2" if kind == "STIR" else "s")
    note_cfg(xR=P(L + 250, 0)[0], yminR=P(0, 20)[1], upR=True)
    kr = P(L + 250, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 42, **kw)
    if kind == "STIR":
        R((xs[1] - 4, h / 2), "CLOSED STIRRUPS ROUND THE TOP AND BOTTOM BARS; ONLY WHERE d ≥ 150 AND ≥ 16 × "
                              "STIRRUP DIA.")
    else:
        R((xs[1], h / 2), "HEADED STUDS WELDED TO A BASE RAIL; HEIGHT = h − COVERS − ½ db")
        R((xs[2], CS), "HEADS AND RAIL: SAME COVER AS THE FLEXURAL BARS")
    R((L - 100, yt), "TOP FLEXURAL BARS OVER THE COLUMN")


# ----------------------------------------------------------------------- 1125: openings (plans)
def mesh_lines(sp, P, x0, x1, y0, y1, s, hole, layer="S-REBR-SEC"):
    """slab bars both ways at spacing s, interrupted at the opening hole = (hx0, hy0, hx1, hy1) with 20 cover"""
    hx0, hy0, hx1, hy1 = hole
    y = y0 + s / 2
    while y < y1:
        if hy0 - 20 < y < hy1 + 20:
            line(sp, P(x0, y), P(hx0 - 20, y), layer)
            line(sp, P(hx1 + 20, y), P(x1, y), layer)
        else:
            line(sp, P(x0, y), P(x1, y), layer)
        y += s
    x = x0 + s / 2
    while x < x1:
        if hx0 - 20 < x < hx1 + 20:
            line(sp, P(x, y0), P(x, hy0 - 20), layer)
            line(sp, P(x, hy1 + 20), P(x, y1), layer)
        else:
            line(sp, P(x, y0), P(x, y1), layer)
        x += s


def diag_bars(sp, P, cx, cy, sx, sy, L, S, n=2, gap=50, off=80):
    """n bars of length L across an opening corner (perpendicular to its diagonal), gap apart, off from the corner"""
    ux, uy = sx * 0.7071, sy * 0.7071                  # outward along the corner diagonal
    vx, vy = -uy, ux                                   # bar direction
    for k in range(n):
        d = off + k * gap
        mx, my = cx + ux * d, cy + uy * d
        rbar(sp, [P(mx - vx * L / 2, my - vy * L / 2), P(mx + vx * L / 2, my + vy * L / 2)], db=12)


def opening_small(ox, oy):
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    a = 500                                            # opening (< 600)
    W = 1700
    pline(sp, [P(-W / 2, -W / 2), P(W / 2, -W / 2), P(W / 2, W / 2), P(-W / 2, W / 2)], "S-BREAK", close=True)
    hole = (-a / 2, -a / 2, a / 2, a / 2)
    pline(sp, [P(-a / 2, -a / 2), P(a / 2, -a / 2), P(a / 2, a / 2), P(-a / 2, a / 2)], "S-CONC", close=True)
    line(sp, P(-a / 2, -a / 2), P(a / 2, a / 2), "S-CONC-VIS")
    line(sp, P(-a / 2, a / 2), P(a / 2, -a / 2), "S-CONC-VIS")
    mesh_lines(sp, P, -W / 2 + 40, W / 2 - 40, -W / 2 + 40, W / 2 - 40, 200, hole)
    for sx in (-1, 1):
        for sy in (-1, 1):
            diag_bars(sp, P, sx * a / 2, sy * a / 2, sx, sy, 1200, S)
    dim(sp, P(-a / 2, -W / 2), P(a / 2, -W / 2), P(0, -W / 2 - 200), S, text="< 600")
    note_cfg(xR=P(W / 2 + 350, 0)[0])
    kr = P(W / 2 + 350, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 46, **kw)
    R((a / 2 + 80 * 0.7071 + 150 * 0.7071, a / 2 + 80 * 0.7071 - 150 * 0.7071),
      "2-DB12 × 1200 DIAGONAL BARS @ 50, TOP AND BOTTOM, AT EVERY CORNER (UNLESS SHOWN)")
    R((a / 2 + 20, -150), "≤ 300: BARS RE-SPACED ROUND THE OPENING; 300 – 600: CUT BARS STOP WITH COVER, THEIR AREA "
                          "ADDED HALF EACH SIDE (≥ 1-DB12), TOP AND BOTTOM")


def opening_large(ox, oy):
    S = 50
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    a, b = 1200, 1000                                  # opening (>= 600)
    ex = 800                                           # trimmer extension past the corners (>= Ld)
    W, Hh = a + 2 * ex + 600, b + 2 * ex + 400
    pline(sp, [P(-W / 2, -Hh / 2), P(W / 2, -Hh / 2), P(W / 2, Hh / 2), P(-W / 2, Hh / 2)], "S-BREAK", close=True)
    pline(sp, [P(-a / 2, -b / 2), P(a / 2, -b / 2), P(a / 2, b / 2), P(-a / 2, b / 2)], "S-CONC", close=True)
    line(sp, P(-a / 2, -b / 2), P(a / 2, b / 2), "S-CONC-VIS")
    line(sp, P(-a / 2, b / 2), P(a / 2, -b / 2), "S-CONC-VIS")
    for sgn in (-1, 1):                                # trimmers: 2 bars each side, 100 apart
        for k in (1, 2):
            yy = sgn * (b / 2 + 60 + (k - 1) * 100)
            rbar(sp, [P(-a / 2 - ex, yy), P(a / 2 + ex, yy)], db=16)
            xx = sgn * (a / 2 + 60 + (k - 1) * 100)
            rbar(sp, [P(xx, -b / 2 - ex), P(xx, b / 2 + ex)], db=16)
    for sx in (-1, 1):
        for sy in (-1, 1):
            diag_bars(sp, P, sx * a / 2, sy * b / 2, sx, sy, 1000, S, off=300)
    yd = -Hh / 2 - 250
    dim(sp, P(-a / 2, -Hh / 2), P(a / 2, -Hh / 2), P(0, yd), S, text="≥ 600")
    dim(sp, P(a / 2, -Hh / 2), P(a / 2 + ex, -Hh / 2), P(0, yd), S, text="≥ 800, Ld")
    note_cfg(xR=P(W / 2 + 350, 0)[0])
    kr = P(W / 2 + 350, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 50, **kw)
    R((a / 2 + ex - 200, b / 2 + 160), "TRIMMER BARS 2-DB16 @ 100 EACH SIDE, TOP AND BOTTOM, ≥ 800 AND ≥ Ld PAST THE "
                                       "CORNERS (UNLESS SHOWN)")
    R((a / 2 + 300 * 0.7071 + 250 * 0.7071, b / 2 + 300 * 0.7071 - 250 * 0.7071),
      "2-DB12 × 1200 DIAGONAL BARS AT EVERY CORNER, TOP AND BOTTOM")
    R((a / 2 + 160, -b / 2 - ex + 150), "EACH SIDE: ADDED AREA ≥ ½ OF THE BARS CUT BY THE OPENING, IN EACH DIRECTION")


def opening_flat(ox, oy):
    """openings in flat slabs by strip zone (EIT 13.4.2) and near columns (11.11.6): plan N.T.S."""
    S = 100
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L = 6000
    w = 0.25 * L
    for (x, y) in ((0, 0), (L, 0), (0, L), (L, L)):
        pts = [P(x - 250, y - 250), P(x + 250, y - 250), P(x + 250, y + 250), P(x - 250, y + 250)]
        pline(sp, pts, "S-CONC", close=True)
        hatch(sp, pts, "ANSI31", pscale("ANSI31", S, 0.8))
    for v in (0, L):
        line(sp, P(v, -700), P(v, L + 700), "S-CENT")
        line(sp, P(-700, v), P(L + 700, v), "S-CENT")
    for v in (w, L - w):
        line(sp, P(v, -500), P(v, L + 500), "S-ANNO")
        line(sp, P(-500, v), P(L + 500, v), "S-ANNO")
    # zone hatches: middle x middle (any size), column x middle, column x column
    hatch(sp, [P(w, w), P(L - w, w), P(L - w, L - w), P(w, L - w)], "ANSI31", pscale("ANSI31", S, 3.0))
    # example openings
    def box(x0, y0, x1, y1):
        pline(sp, [P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)], "S-CONC", close=True)
        line(sp, P(x0, y0), P(x1, y1), "S-CONC-VIS")
        line(sp, P(x0, y1), P(x1, y0), "S-CONC-VIS")
    box(2400, 2600, 3600, 3400)                        # middle x middle
    box(2700, 350, 3300, 800)                          # column x middle
    box(600, 450, 800, 650)                            # near the column (within 10h), column x column
    for (tx, ty) in ((600, 650), (800, 450)):          # tangents from the column centre (ineffective perimeter)
        line(sp, P(0, 0), P(tx * 1.6, ty * 1.6), "S-ANNO")
    note_cfg(xR=P(L + 1100, 0)[0])
    kr = P(L + 1100, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 52, **kw)
    R((3600, 3000), "MIDDLE ∩ MIDDLE STRIP: ANY SIZE; THE PANEL'S TOTAL BARS KEPT (INTERRUPTED BARS ADDED AT THE SIDES)")
    R((3300, 600), "COLUMN ∩ MIDDLE STRIP: ≤ 1/4 OF THE BARS OF EITHER STRIP INTERRUPTED; ADD THEM AT THE SIDES")
    R((800, 600), "COLUMN ∩ COLUMN STRIP: ≤ 1/8 OF THE COLUMN-STRIP WIDTH; ADD THE INTERRUPTED BARS AT THE SIDES")
    R((1100, 900), "WITHIN 10h OF A COLUMN (OR IN A COLUMN STRIP): PUNCHING PERIMETER BETWEEN THE TANGENTS FROM THE "
                   "COLUMN CENTRE IS INEFFECTIVE")


# ----------------------------------------------------------------------- 1125: slab steps (sections, 1:20)
def slab_step(ox, oy, big):
    """TATA p.181. big=False: H < T, thickened zone T wide; big=True: H > T, the lower-slab soffit runs t past
    the step face, then a 45 deg haunch up to the upper soffit (TATA, mirrored: upper slab left)"""
    S = 10
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    t = 150
    H = 80 if not big else 260
    L = 700 if not big else 900
    ld = 480 if not big else 420                       # drawn Ld
    c = 25
    if not big:
        pline(sp, [P(-L, t + H), P(0, t + H), P(0, t), P(L, t)], "S-CONC")
        pline(sp, [P(-L, H), P(-t, H), P(-t, 0), P(L, 0)], "S-CONC")
    else:
        pline(sp, [P(-L, t + H), P(0, t + H), P(0, t), P(L, t)], "S-CONC")
        pline(sp, [P(-L, H), P(-t - H, H), P(-t, 0), P(L, 0)], "S-CONC")
    zbreak(sp, P(-L, H - 60), P(-L, t + H + 60), S)
    zbreak(sp, P(L, -60), P(L, t + 60), S)
    ut, ub = t + H - c, H + c                          # upper slab bars
    lt, lb = t - c, c                                  # lower slab bars
    xz = -t + c if not big else -H + c
    # upper top: to the step face, down, along the lower bottom for Ld
    rbar(sp, [P(-L, ut), P(-c, ut), P(-c, lb + 14), P(ld, lb + 14)])
    if not big:
        # lower top: straight into the upper slab for Ld
        rbar(sp, [P(L, lt), P(-ld, lt)])
        # lower bottom: to the far side of the zone, up to the upper-slab TOP layer, Ld (TATA; not bent at the
        # re-entrant soffit corner)
        rbar(sp, [P(L, lb), P(xz, lb), P(xz, ut - 30), P(-ld - 200, ut - 30)])
        # upper bottom: straight into the lower slab for Ld
        rbar(sp, [P(-L, ub), P(ld - 150, ub)])
    else:
        # No bar follows the re-entrant corner at the haunch top: the upper bottom bars run straight past it.
        r2 = math.sqrt(2)
        k_lb = -t + c * r2                             # lower bottom along the haunch: x + y = k_lb (cover c)
        # lower bottom: along the soffit, up the haunch parallel to it and straight on past the re-entrant corner
        # to the upper-slab TOP layer, Ld (crossing bars, as at a stair waist / landing)
        x1, x2 = k_lb - lb, k_lb - (ut - 30)
        rbar(sp, [P(L, lb), P(x1, lb), P(x2, ut - 30), P(x2 - ld, ut - 30)])
        # lower top: into the step, cranked 45 deg up (80 clear of the haunch bars) to the upper-slab top, Ld
        xk = k_lb + 80 * r2 - lt
        x3 = xk + lt - (ut - 14)
        rbar(sp, [P(L, lt), P(xk, lt), P(x3, ut - 14), P(x3 - ld, ut - 14)])
        # upper bottom: straight past the haunch corner into the step block, 90 deg hook down at the step face
        rbar(sp, [P(-L, ub), P(-c - 40, ub), P(-c - 40, lt + 45)])       # hook stops clear of the lower top bars
    yd = -150
    dim(sp, P(-c, 0), P(ld, 0), P(0, yd), S, text="Ld")
    dim(sp, P(-L, H), P(-L, t + H), P(-L - 150, 0), S, angle=90, text="t")
    xh_ = -t if not big else -t - H                    # H measured at the soffit step, dimension line at the left
    dim(sp, P(-t, 0), P(xh_, H), P(-L - 150, 0), S, angle=90, text="H < t" if not big else "H > t")
    dim(sp, P(-t, 0), P(0, 0), P(0, yd), S, text="t")
    note_cfg(xR=P(L + 250, 0)[0], yminR=P(0, 10)[1], upR=True)
    kr = P(L + 250, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 44 if not big else 60, **kw)
    R((-c, (ut + lb) / 2 if not big else ut - 60), "UPPER TOP BARS DOWN THE STEP FACE, THEN Ld ALONG THE "
                                                   "LOWER-SLAB BOTTOM")
    R((L - 120, lt), "LOWER TOP BARS STRAIGHT, Ld INTO THE UPPER SLAB" if not big else
      "LOWER TOP BARS INTO THE STEP, CRANKED 45° UP TO THE UPPER-SLAB TOP, Ld BEYOND THE CRANK")
    R((L - 200, lb), "LOWER BOTTOM BARS " + ("UP AT THE FAR SIDE OF THE THICKENED ZONE TO THE UPPER-SLAB TOP, Ld"
                                             if not big else "UP THE 45° HAUNCH AND STRAIGHT ON TO THE UPPER-SLAB "
                                                             "TOP, Ld; NOT BENT AT THE SOFFIT CORNER"))
    R((-L + 150, ub), "UPPER BOTTOM BARS " + ("STRAIGHT, Ld INTO THE LOWER SLAB" if not big else
                                             "STRAIGHT PAST THE HAUNCH CORNER (NOT BENT ROUND IT), "
                                             "90° HOOK DOWN AT THE STEP FACE"))


# ----------------------------------------------------------------------- 1126: slab-edge upstands (sections, 1:10)
def edge_upstand(ox, oy, big):
    """TATA p.181 / 182 (unless shown): upstand fin or curb on a slab edge. big=False: <= 100 thick, <= 300 high,
    single L-bars; big=True: > 100 thick or > 300 high, hairpins both faces. Downstands: the same, mirrored."""
    S = 10
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    t = 150
    bw, hh = (100, 300) if not big else (150, 500)
    L = 480
    x0 = -bw                                           # fin on the slab edge, x -bw..0
    pline(sp, [P(L, t), P(0, t), P(0, t + hh), P(x0, t + hh), P(x0, 0), P(L, 0)], "S-CONC")
    zbreak(sp, P(L, -60), P(L, t + 60), S)
    c = 25
    rbar(sp, [P(x0 + c, t - c), P(L, t - c)], db=10)                 # slab top bars
    rbar(sp, [P(x0 + c, c), P(L, c)], db=10)                         # slab bottom bars
    anc = 400
    if not big:
        xv = x0 + bw / 2
        rbar(sp, [P(xv, t + hh - c), P(xv, c + 12), P(xv + anc, c + 12)], db=10)     # L-bar into the slab bottom
        dot(sp, P(xv, t + hh - c - 20), rdot(12, S))                               # 1DB12 at the tip
        dot(sp, P(xv + 25, t + 25), rdot(10, S))                                    # 1DB10 at the root
    else:
        xa, xb = x0 + c + 6, -c - 6
        rbar(sp, [P(xa + anc * 0 + anc, c + 12), P(xa, c + 12), P(xa, t + hh - c), P(xb, t + hh - c), P(xb, t - c - 12),
                  P(xb + anc, t - c - 12)], db=10)                               # hairpin, both faces
        for x in (xa + 14, xb - 14):
            dot(sp, P(x, t + hh - c - 22), rdot(12, S))
            dot(sp, P(x, t + 30), rdot(10, S))
    dim(sp, P(x0, t), P(x0, t + hh), P(x0 - 150, 0), S, angle=90, text="≤ 300" if not big else "> 300")
    dim(sp, P(x0, 0), P(0, 0), P(0, -150), S, text="≤ 100" if not big else "> 100")
    dim(sp, P(0, 0), P(anc - c, 0), P(0, -150), S, text="400")
    note_cfg(xR=P(L + 200, 0)[0], yminR=P(0, 10)[1], upR=True)
    kr = P(L + 200, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 40, **kw)
    if not big:
        R((xv, t + hh * 0.6), "DB10 @ 250 L-BARS, 400 INTO THE SLAB")
        R((xv, t + hh - c - 20), "1-DB12 AT THE TIP, 1-DB10 AT THE ROOT", ring=12)
    else:
        R((xb, t + hh * 0.6), "DB10 @ 250 HAIRPINS, BOTH FACES, 400 INTO THE SLAB")
        R((xb - 14, t + hh - c - 22), "2-DB12 AT THE TIP, 2-DB10 AT THE ROOT", ring=12)
    R((L - 150, t - c), "SLAB BARS TO THE FAR FACE OF THE UPSTAND")


# ----------------------------------------------------------------------- 1127: slab on ground (TATA 3.26 - 3.43)
TG = 150                        # slab-on-ground thickness (drawn)
MESH = 40                       # mesh below the top surface (30 - 50, <= t/2)


def sand_bed(sp, P, x0, x1, S, depth=100):
    line(sp, P(x0, -depth), P(x1, -depth), "S-SOIL")
    hatch(sp, [P(x0, 0), P(x1, 0), P(x1, -depth), P(x0, -depth)], "AR-SAND", pscale("AR-SAND", S, 1.0))


def mesh_section(sp, P, x0, x1, y, S, s=200):
    rbar(sp, [P(x0, y), P(x1, y)], db=9, layer="S-REBR-SEC")
    r = rdot(9, S) * 0.8
    x = x0 + 60
    while x < x1 - 30:
        dot(sp, P(x, y - 9), r)
        x += s


def sog_at_beam(ox, oy):
    """interior slab against a ground beam: isolation gap with filler, single mesh near the top, sand bed"""
    S = 20
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    gb, gh = 300, 600
    L = 1000
    g = 20                                              # isolation gap
    pline(sp, [P(-gb, TG + 50), P(0, TG + 50), P(0, TG + 50 - gh), P(-gb, TG + 50 - gh)], "S-CONC")
    line(sp, P(-gb, TG + 50), P(-gb, TG + 50 - gh), "S-CONC")
    pline(sp, [P(g, TG), P(L, TG)], "S-CONC")
    pline(sp, [P(g, 0), P(L, 0)], "S-CONC")
    line(sp, P(g, 0), P(g, TG), "S-CONC")
    hatch(sp, [P(0, 0), P(g, 0), P(g, TG - 15), P(0, TG - 15)], "ANSI31", pscale("ANSI31", S, 0.5))
    pline(sp, [P(0, TG - 15), P(g, TG - 15), P(g, TG), P(0, TG)], "S-JFILL", close=True)
    zbreak(sp, P(L, -60), P(L, TG + 60), S)
    sand_bed(sp, P, g, L, S)
    mesh_section(sp, P, g + 30, L, TG - MESH, S)
    yd = -250
    dim(sp, P(0, 0), P(g, 0), P(0, yd), S, text="20 – 25", tside="L")     # text over the beam, off the face
    note_cfg(xR=P(L + 300, 0)[0], yminR=P(0, -90)[1], upR=True)
    kr = P(L + 300, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 40, **kw)
    R((L - 300, TG - MESH), "SINGLE MESH 30 – 50 BELOW THE TOP, NEVER BELOW t/2, ON CHAIRS")
    R((g / 2, TG / 2), "ISOLATION JOINT: FULL-DEPTH COMPRESSIBLE FILLER, SEALANT ON TOP; SLAB FREE OF THE BEAM")
    R((L - 200, -60), "COMPACTED MOIST SAND 50 – 100 ON COMPACTED SUBGRADE")
    R((-gb / 2, TG - 200), "GROUND BEAM")


def sog_edge(ox, oy):
    """thickened free edge: +50..100 deep, 100 flat then 45 deg; mesh turned down into the thickening"""
    S = 20
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L = 900
    dt = 100                                            # extra depth
    pline(sp, [P(L, TG), P(0, TG), P(0, -dt), P(100, -dt), P(100 + dt, 0), P(L, 0)], "S-CONC")
    zbreak(sp, P(L, -60), P(L, TG + 60), S)
    sand_bed(sp, P, 100 + dt, L, S)
    rbar(sp, [P(40, -dt + 50), P(40, TG - MESH), P(L, TG - MESH)], db=9, layer="S-REBR-SEC")
    r = rdot(9, S) * 0.8
    x = 260
    while x < L - 30:
        dot(sp, P(x, TG - MESH - 9), r)
        x += 200
    xl = -150
    dim(sp, P(0, -dt), P(0, 0), P(xl, 0), S, angle=90, text="50 – 100")
    dim(sp, P(0, 0), P(0, TG), P(xl, 0), S, angle=90, text="t")
    dim(sp, P(0, -dt), P(100, -dt), P(0, -dt - 200), S, text="100")
    note_cfg(xR=P(L + 300, 0)[0], yminR=P(0, -90)[1], upR=True)
    kr = P(L + 300, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 40, **kw)
    R((40, 20), "MESH TURNED DOWN 90° INTO THE THICKENED EDGE")
    R((100 + dt / 2, -dt / 2), "EDGE THICKENED 50 – 100, 100 FLAT THEN 45°, AGAINST WASH-OUT OF THE SUBGRADE")


def sog_joint(ox, oy, kind):
    """joints (1:10): SAW contraction, CONS construction, EXP expansion / isolation with dowels"""
    S = 10
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L = 420
    g = 20 if kind == "EXP" else 0
    for sx in (-1, 1):
        x0 = sx * g / 2
        pline(sp, [P(x0, 0), P(x0, TG), P(sx * L, TG)], "S-CONC")
        line(sp, P(x0, 0), P(sx * L, 0), "S-CONC")
        zbreak(sp, P(sx * L, -60), P(sx * L, TG + 60), S)
        rbar(sp, [P(x0 + sx * 50, TG - MESH), P(sx * L, TG - MESH)], db=9, layer="S-REBR-SEC")
    line(sp, P(-L, 0), P(L, 0), "S-CONC")
    if kind == "SAW":
        pline(sp, [P(-2, TG), P(-2, TG - TG / 4), P(2, TG - TG / 4), P(2, TG)], "S-CONC")
        line(sp, P(0, 0), P(0, TG - TG / 4), "S-CONC-HIDN")
    if kind == "CONS":
        pass
    if kind == "EXP":
        hatch(sp, [P(-g / 2, 0), P(g / 2, 0), P(g / 2, TG - 15), P(-g / 2, TG - 15)], "ANSI31",
              pscale("ANSI31", S, 0.5))
        pline(sp, [P(-g / 2, TG - 15), P(g / 2, TG - 15), P(g / 2, TG), P(-g / 2, TG)], "S-JFILL", close=True)
    # dowel at mid-depth: bonded half left, debonded half right (sleeve / paint), cap on the free end (EXP)
    if kind in ("CONS", "EXP", "SAW"):
        hd = 225                                         # plain dowel 450 long (RB25, t <= 200), half each side
        rbar(sp, [P(-hd, TG / 2), P(hd, TG / 2)], db=25)
        pline(sp, [P(0, TG / 2 - 16), P(hd, TG / 2 - 16)], "S-DWL-SLV")
        pline(sp, [P(0, TG / 2 + 16), P(hd, TG / 2 + 16)], "S-DWL-SLV")
        if kind == "EXP":
            pline(sp, [P(hd, TG / 2 - 20), P(hd + 50, TG / 2 - 20), P(hd + 50, TG / 2 + 20), P(hd, TG / 2 + 20)],
                  "S-DWL-SLV")
    dim(sp, P(-225, 0), P(225, 0), P(0, -120), S, text="400 – 450")
    note_cfg(xR=P(L + 200, 0)[0], yminR=P(0, 10)[1], upR=True)
    kr = P(L + 200, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 38, **kw)
    if kind == "SAW":
        R((2, TG - 20), "SAW CUT 3 WIDE × t/4 DEEP (OR TOOLED GROOVE), FILLED; CUT AS SOON AS THE SURFACE ALLOWS")
        R((200, TG / 2), "DOWELS WHERE LOAD TRANSFER IS NEEDED (AS CONSTRUCTION JOINT)")
    elif kind == "CONS":
        R((0, TG * 0.8), "DAY-WORK JOINT AGAINST A CLEAN BULKHEAD, ON A JOINT LINE")
        R((200, TG / 2), "PLAIN DOWELS @ 300 AT t/2 (UNLESS SHOWN): RB19 × 400 (t ≤ 150), RB25 × 450 (t ≤ 200); "
                         "HALF BONDED, HALF GREASED / SLEEVED")
    else:
        R((0, TG * 0.4), "20 COMPRESSIBLE FILLER, FULL DEPTH, SEALANT ON TOP")
        R((325, TG / 2 + 20), "PLAIN DOWELS (AS THE CONSTRUCTION JOINT) @ 300, HALF GREASED, CAP WITH 25 FREE "
                              "TRAVEL")
    R((L - 100, TG - MESH), "MESH STOPS 50 FROM THE JOINT" if kind != "SAW" else "MESH STOPPED 50 EACH SIDE "
                                                                               "(CONTINUOUS ONLY IF DESIGNED)")


def sog_layout(ox, oy):
    """joint layout plan N.T.S.: joints on column lines and mid-bay, <= 30 t apart; diamond isolation at columns"""
    S = 200                                             # built at its plotted scale (1:200)
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    a = 8000
    cols = [(x, y) for x in (0, a) for y in (0, a)]
    pline(sp, [P(-1200, -1200), P(a + 1200, -1200), P(a + 1200, a + 1200), P(-1200, a + 1200)], "S-CONC", close=True)
    for x, y in cols:
        pts = [P(x - 200, y - 200), P(x + 200, y - 200), P(x + 200, y + 200), P(x - 200, y + 200)]
        pline(sp, pts, "S-CONC", close=True)
        hatch(sp, pts, "ANSI31", pscale("ANSI31", S, 0.8))
        pline(sp, [P(x, y - 700), P(x + 700, y), P(x, y + 700), P(x - 700, y)], "S-JOINT", close=True)
    for v in (0, a / 2, a):
        line(sp, P(v if v else 0, -1200), P(v, a + 1200), "S-CONC-HIDN")
        line(sp, P(-1200, v), P(a + 1200, v), "S-CONC-HIDN")
    note_cfg(xR=P(a + 2000, 0)[0])
    kr = P(a + 2000, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 50, **kw)
    R((a / 2, a * 0.75), "CONTRACTION OR CONSTRUCTION JOINTS ON THE COLUMN LINES AND AT MID-BAY, ≤ 30 t APART "
                         "(≈ 4.5 m FOR t = 150)")
    R((a + 350, a + 350), "ISOLATION JOINT ROUND EACH COLUMN (DIAMOND, JOINTS INTO ITS CORNERS); INFILL CAST AFTER "
                          "THE COLUMN LOAD")
    R((a + 1200, a * 0.35), "ISOLATION JOINT ALONG WALLS, BEAMS AND MACHINE BASES")


# ======================================================================= tables and notes
SLAB_TABLE = [
    ["MIN. THICKNESS (NO DEFLECTION CHECK, SD40)", "ℓ/20 SIMPLE, ℓ/24 ONE END CONT., ℓ/28 BOTH CONT., ℓ/10 CANTILEVER; "
     "× (0.4 + fy/700) FOR OTHER STEEL", "EQ. 9-11 / 9-12 (αfm, β); ≥ 125 (αfm ≤ 2), ≥ 90 (αfm > 2); +10 % AT AN "
     "EDGE WITHOUT A STIFF BEAM", "ℓn/30 – ℓn/36 (TABLE 9.3); ≥ 125, ≥ 100 WITH DROP PANELS"],
    ["MAIN-BAR SPACING", "≤ 3h AND 450", "≤ 2h AND 450", "≤ 2h AND 450"],
    ["MIN. STEEL (EACH WAY, ON b × h)", "0.0025 SR24 / 0.0020 SD30 / 0.0018 SD40", "SAME", "SAME"],
    ["DISTRIBUTION (S&T) BARS", "SAME RATIO, PERPENDICULAR TO THE MAIN BARS, ≤ 5h AND 400", "–", "–"],
    ["TOP BARS AT SUPPORTS", "Sn/4 AT EDGES, Sn/3 AT INTERIOR SUPPORTS", "Sn/4, Sn/3 AND Ln/4, Ln/3",
     "FIG. 13.3.8: 0.30 / 0.20 ℓn COLUMN STRIP, 0.22 ℓn MIDDLE STRIP (1122)"],
    ["BOTTOM BARS", "FULL SPAN, ≥ 150 INTO SUPPORTS", "SAME; SHORT DIRECTION IN THE LOWER LAYER",
     "COLUMN STRIP CONTINUOUS; ≥ 2 EACH WAY THROUGH THE COLUMN CORE (1122)"],
    ["DISCONTINUOUS EDGE", "TOP BARS 90° HOOK INTO THE EDGE BEAM", "SAME + CORNER BARS L/5 × L/5",
     "TOP HOOKED, BOTTOM ≥ 150; DEVELOP fy AT THE FACE"],
    ["REFERENCE", "EIT 011008 7.6, 7.12, 9.5.2, 10.5.4, 12.10; TATA 3", "EIT 011008 9.5.3, 13.3; TATA 3",
     "EIT 011008 9.5.3, 13.3.8; DPT 5.2.12"],
]


SLAB_NOTES = [
    ("1.", "THESE DETAILS APPLY WHERE THE SLAB DRAWINGS DO NOT SHOW OTHERWISE. SLAB MARKS: S = CAST IN PLACE, "
           "PS = PRECAST, GS = ON GROUND; ARROWS SHOW THE SPAN DIRECTION."),
    ("2.", "COVER: 20 (≤ DB16) / 30 (≥ DB20) INTERIOR; 40 / 50 EXPOSED TO WEATHER; 75 CAST AGAINST EARTH. SEE 1002."),
    ("3.", "LAPS PER 1002 TABLE 6: TOP BARS LAPPED NEAR MIDSPAN, BOTTOM BARS OVER THE SUPPORTS. WELDED MESH LAP "
           "≥ ONE MESH SPACING + 25 AND ≥ 300."),
    ("4.", "BOTTOM MAT ON MORTAR SPACERS; TOP MAT ON DB12 CHAIRS @ 1.0 – 1.5 m EACH WAY."),
    ("5.", "PIPES IN SLABS: OUTSIDE DIA. ≤ h/3, ≥ 3 DIA. APART, BETWEEN THE TOP AND BOTTOM MATS. [EIT 011008 6.3]"),
    ("6.", "A 90° TOP-BAR HOOK NEEDS ≈ 16 db BETWEEN THE COVERS; WHERE IT DOES NOT FIT, USE A 180° HOOK OR EDGE "
           "U-BARS. FREE SLAB EDGES: ≥ 2-DB12 TOP AND BOTTOM ALONG THE EDGE."),
    ("7.", "BAR ENDS AND LAPS: SEE THE KEY. FLAT SLABS 1122 – 1124; OPENINGS 1125; STEPS AND EDGES 1126; SLAB ON GROUND 1127."),
]


PUNCH_TABLE = [
    ["WHERE", "d ≥ 150 AND ≥ 16 × STIRRUP DIA.; CLOSED STIRRUPS ENGAGE THE FLEXURAL BARS", "ANY SLAB DEPTH"],
    ["STRENGTH LIMITS", "Vc ≤ 0.17√f'c bo d; Vn ≤ 0.5√f'c bo d", "Vc ≤ 0.25√f'c bo d; Vn ≤ 0.66√f'c bo d; "
     "Av fyt / (bo s) ≥ 0.17√f'c"],
    ["FIRST LINE FROM THE FACE", "≤ d/2", "≤ d/2"],
    ["SPACING OF LINES", "≤ d/2", "CONSTANT; ≤ 0.75d IF vu ≤ φ0.5√f'c, ELSE ≤ 0.5d"],
    ["ALONG THE FIRST LINE", "LEGS ≤ 2d APART", "STUDS ≤ 2d APART"],
    ["EXTENT", "UNTIL vu ≤ φ0.17√f'c AT d/2 BEYOND THE LAST LINE", "SAME"],
    ["ANCHORAGE / COVER", "STANDARD HOOKS ROUND LONGITUDINAL BARS (EIT 12.12)",
     "HEIGHT = h − COVERS − ½ db; HEADS AND RAIL WITH THE FLEXURAL-BAR COVER"],
    ["REFERENCE", "EIT 011008 11.11.3", "EIT 011008 11.11.5; ACI 318-11 7.7.5"],
]


OPENING_NOTES = [
    ("1.", "OPENINGS, SLEEVES AND CORED HOLES ONLY WHERE SHOWN ON THE STRUCTURAL DRAWINGS OR APPROVED BY THE ENGINEER; "
           "OPENINGS CUT LATER MUST BE TRIMMED TO RESTORE THE CUT STEEL."),
    ("2.", "BARS CUT BY AN OPENING STOP WITH COVER AT ITS EDGE (TOP BARS WITH A STANDARD HOOK DOWN); THEIR AREA IS ADDED BESIDE THE OPENING, HALF EACH SIDE, "
           "IN EACH DIRECTION, EXTENDED ≥ Ld PAST THE CORNERS. EXAMPLE: DB12 @ 150, 800 OPENING: 5.3 BARS CUT = 6.0 cm² "
           "→ 2-DB16 (4.0 cm²) EACH SIDE."),
    ("3.", "PRECAST HOLLOW-CORE PLANKS: HOLES ≤ Ø150 (OR ≤ 150 WIDE) ONLY THROUGH A CORE, ≤ 3 IN ONE CROSS-SECTION; "
           "LARGER OPENINGS ON STEEL-ANGLE TRIMMERS SEATED ON THE ADJACENT PLANKS."),
    ("4.", "OPENINGS THROUGH BEAMS: 1113. PIPES EMBEDDED IN SLABS: 1121 NOTE 5."),
]


SOG_NOTES = [
    ("1.", "SLAB ON GROUND (GS) ON A LEVELLED, COMPACTED SUBGRADE WITH 50 – 100 COMPACTED SAND; THICKNESS 150 – 300 "
           "UNLESS SHOWN. COVER 75 WHERE CAST AGAINST EARTH (LEAN CONCRETE OR MEMBRANE BELOW: 40)."),
    ("2.", "JOINT SPACING ≤ 30 t; PANELS AS SQUARE AS POSSIBLE (≤ 1.5 : 1); RE-ENTRANT CORNERS: 2 DIAGONAL BARS."),
    ("3.", "POUR IN LONG STRIPS WITH CONTRACTION JOINTS SAWN ACROSS THEM (ACI 302.1R), NOT IN A CHECKERBOARD."),
    ("4.", "SLABS UNDER BASEMENTS OR WATER PRESSURE, AND SLABS CARRYING RACKS OR MACHINES: PER DESIGN."),
]


FLAT_NOTES = [
    ("1.", "COLUMN STRIP = 0.25 × THE SMALLER SPAN EACH SIDE OF THE COLUMN LINE; MIDDLE STRIP BETWEEN. UNEQUAL SPANS: "
           "TOP-BAR LENGTHS FROM THE LONGER ℓn. BENT BARS ONLY IF THE BEND ≤ 45°. [EIT 011008 13.2, 13.3.8]"),
    ("2.", "MAIN-BAR SPACING ≤ 2h AND 450; MIN. STEEL EACH WAY 0.0018 bh (SD40); BOTTOM BARS AT A DISCONTINUOUS EDGE ≥ 150 "
           "INTO THE SUPPORT, TOP BARS HOOKED AND DEVELOPED AT THE FACE. [EIT 011008 13.3]"),
    ("3.", "FLAT SLAB IN AN INTERMEDIATE MOMENT FRAME (DPT 5.2.12): ALL Ms BARS IN THE COLUMN STRIP, γf Ms AND ≥ ½ OF "
           "THE COLUMN-STRIP TOP BARS WITHIN c2 + 3h; ≥ ¼ OF THE TOP BARS CONTINUOUS, ≥ 2 THROUGH THE COLUMN LINE EACH "
           "WAY; CONTINUOUS BOTTOM ≥ 1/3 OF THE COLUMN-STRIP TOP; ≥ ½ OF THE MIDSPAN BOTTOM CONTINUOUS; fy DEVELOPED "
           "AT THE FACE OF DISCONTINUOUS EDGES. GRAVITY SHEAR Vu/φVc ≤ 0.4."),
    ("4.", "SEISMIC CATEGORY D, FLAT SLAB NOT IN THE SEISMIC SYSTEM: SHEAR REINFORCEMENT Vs ≥ 0.3√f'c bo d TO ≥ 4h "
           "FROM THE COLUMN FACE, UNLESS THE DRIFT ≤ max (0.005, 0.035 − 0.05 Vu/φVc). [DPT 5.2.12.1.4, 2.11.5]"),
    ("5.", "INTEGRITY: BOTTOM BARS THROUGH OR ANCHORED IN THE COLUMN CORE EACH WAY ≥ Asm = 0.5 wu L1 L2 / (0.9 fy) "
           "(EDGE ≥ 2/3, CORNER ≥ ½ Asm). [DPT 5.2.12.2; EIT 011008 13.3.8]"),
    ("6.", "COLUMN TIES CONTINUE THROUGH THE SLAB DEPTH AT EDGE AND CORNER COLUMNS. [EIT 011008 11.10.2]"),
    ("7.", "STIRRUPS IN SLABS ONLY WHERE d ≥ 150 AND ≥ 16 × STIRRUP DIA.; OTHERWISE STUD RAILS (1124). OPENINGS NEAR "
           "COLUMNS: 1125."),
]


def build():
    EXT.update({
        "SS": capture(short_section, 0, 0),
        "CP": capture(corner_panel, 0, -10000),
        "CS": capture(cant_slab, 24000, -10000),
        "FA": capture(col_strip, 0, -20000, False),
        "FB": capture(col_strip, 0, -28000, True),
        "FC": capture(mid_strip, 0, -36000),
        "FP": capture(strip_plan, 20000, -28000),
        "DC": capture(drop_capital, 20000, -40000),
        "PSP": capture(punch_plan, 0, -48000, "STIR"),
        "PSS": capture(punch_section, 8000, -48000, "STIR"),
        "PRP": capture(punch_plan, 0, -56000, "STUD"),
        "PRS": capture(punch_section, 8000, -56000, "STUD"),
        "OS": capture(opening_small, 0, -66000),
        "OL": capture(opening_large, 8000, -66000),
        "OF": capture(opening_flat, 24000, -66000),
        "T1": capture(slab_step, 0, -76000, False),
        "T2": capture(slab_step, 0, -84000, True),
        "E1": capture(edge_upstand, 0, -92000, False),
        "E2": capture(edge_upstand, 8000, -92000, True),
        "G1": capture(sog_at_beam, 0, -100000),
        "G2": capture(sog_edge, 8000, -100000),
        "J1": capture(sog_joint, 0, -108000, "SAW"),
        "J2": capture(sog_joint, 8000, -108000, "CONS"),
        "J3": capture(sog_joint, 0, -116000, "EXP"),
        "GL": capture(sog_layout, 8000, -120000),
    })
    sheet_1121()
    sheet_1122()
    sheet_1123()
    sheet_1124()
    sheet_1125()
    sheet_1126()
    sheet_1127()


# ======================================================================= sheet 1121
def sheet_1121():
    ps = new_sheet(0)
    top = FY1 - 3
    px, pw, ph = viewport(ps, "SS", 25, FX0 + 1, top)
    view_title(ps, None, top - ph - 6, "SLAB ON BEAMS - SECTION ALONG THE SHORT SPAN", "1:25", ("1", "1121"),
               note="ONE-WAY AND TWO-WAY SLABS; UNIFORM LOAD, ADJACENT SPANS WITHIN 20 %; OTHERWISE PER DESIGN")
    top2 = top - ph - 24
    px, pw, ph2 = viewport(ps, "CP", 100, FX0 + 1, top2)
    view_title(ps, None, top2 - ph2 - 6, "TWO-WAY SLAB - CORNER PANEL", "1:100", ("2", "1121"),
               note="PLAN; EDGE BEAMS LEFT AND BELOW; ONE BAR SHOWN PER BAND")
    px3, pw3, ph3 = viewport(ps, "CS", 25, px + pw + 6, top2)
    view_title(ps, None, top2 - ph3 - 6, "CANTILEVER SLAB", "1:25", ("3", "1121"))
    top3 = top2 - max(ph2, ph3) - 24
    yn = notes_block(ps, FX0 + 3, top3, 200, "TYPICAL SLAB NOTES", SLAB_NOTES)
    xl = FX0 + 3 + 200 + 10
    yl = bar_end_legend(ps, xl, top3, TBX - xl - 3)
    print(f"  notes bottom {yn:.1f}, legend bottom {yl:.1f}")


# ======================================================================= sheet 1122
def sheet_1122():
    ps = new_sheet(1)
    top = FY1 - 3
    y = top
    for i, (k, nm, note) in enumerate((("FA", "COLUMN STRIP - WITHOUT DROP PANELS", None),
                                       ("FB", "COLUMN STRIP - WITH DROP PANELS", None),
                                       ("FC", "MIDDLE STRIP", "WITH OR WITHOUT DROP PANELS"))):
        px, pw, ph = viewport(ps, k, 50, FX0 + 1, y)
        view_title(ps, None, y - ph - 6, nm, "N.T.S.", (str(i + 1), "1122"),
                   note=("SCHEMATIC: SLAB DEPTH EXAGGERATED, LENGTHS IN PROPORTION" + ("; " + note if note else "")))
        y = y - ph - 22
    bar_end_legend(ps, 282, 118, TBX - 282 - 2)


# ======================================================================= sheet 1123
def sheet_1123():
    ps = new_sheet(2)
    top = FY1 - 3
    px, pw, ph1 = viewport(ps, "FP", 100, FX0 + 1, top)
    view_title(ps, None, top - ph1 - 6, "FLAT SLAB - STRIPS AND COLUMN ZONE", "1:100", ("1", "1123"),
               note="PLAN OF AN INTERIOR PANEL")
    px2, pw2, ph2 = viewport(ps, "DC", 25, px + pw + 6, top)
    view_title(ps, None, top - ph2 - 6, "DROP PANEL AND COLUMN CAPITAL", "1:25", ("2", "1123"),
               note="SECTION THROUGH AN INTERIOR COLUMN HEAD")
    yn = notes_block(ps, FX0 + 3, top - max(ph1, ph2) - 22, TBX - FX0 - 6, "FLAT SLAB NOTES", FLAT_NOTES)
    yb = tbl(ps, FX0 + 3, yn - 8, [40, 90, 90, 96], ["ITEM", "ONE-WAY SLAB", "TWO-WAY SLAB ON BEAMS",
             "FLAT SLAB / FLAT PLATE"], SLAB_TABLE, "LCCC", title="SLAB THICKNESS AND REINFORCEMENT")
    print(f"  1123 table bottom {yb:.1f}")


# ======================================================================= sheet 1124
def sheet_1124():
    ps = new_sheet(3)
    top = FY1 - 3
    y = top
    for k, (kp, ks, nm) in enumerate((("PSP", "PSS", "PUNCHING SHEAR - STIRRUPS"),
                                       ("PRP", "PRS", "PUNCHING SHEAR - HEADED STUD RAILS"))):
        px, pw, php = viewport(ps, kp, 25, FX0 + 1, y)
        view_title(ps, None, y - php - 6, nm, "1:25", (str(1 + k), "1124"), note="PLAN AT AN INTERIOR COLUMN")
        px2, pw2, phs = viewport(ps, ks, 10, px + pw + 6, y)
        view_title(ps, None, y - phs - 6, "SECTION", "1:10", ("AB"[k], "1124"), triangles=True)
        y = y - max(php, phs) - 26
    yb = tbl(ps, FX0 + 3, y + 4, [44, 136, 136], ["ITEM", "STIRRUPS (BARS)", "HEADED STUD RAILS"], PUNCH_TABLE,
             "LCC", title="PUNCHING SHEAR REINFORCEMENT RULES")
    print(f"  1124 bottom {yb:.1f}")


# ======================================================================= sheet 1125
def sheet_1125():
    ps = new_sheet(4)
    top = FY1 - 3
    px, pw, ph1 = viewport(ps, "OS", 25, FX0 + 1, top)
    view_title(ps, None, top - ph1 - 6, "OPENING < 600", "1:25", ("1", "1125"), note="SLAB ON BEAMS OR WALL")
    px2, pw2, ph2 = viewport(ps, "OL", 50, px + pw + 6, top)
    view_title(ps, None, top - ph2 - 6, "OPENING ≥ 600", "1:50", ("2", "1125"),
               note="LARGER OPENINGS / NOT ON THE DRAWINGS: ENGINEER'S APPROVAL")
    top2 = top - max(ph1, ph2) - 24
    px, pw, ph3 = viewport(ps, "OF", 100, FX0 + 1, top2)
    view_title(ps, None, top2 - ph3 - 6, "OPENINGS IN FLAT SLABS", "1:100", ("3", "1125"),
               note="PLAN OF A PANEL: PERMITTED OPENINGS WITHOUT ANALYSIS (EIT 011008 13.4, 11.11.6)")
    xl = px + pw + 8
    yl = bar_end_legend(ps, xl, top2, TBX - xl - 3)
    notes_block(ps, xl, yl - 8, TBX - xl - 3, "NOTES TO 1125", OPENING_NOTES)


# ======================================================================= sheet 1126
def sheet_1126():
    ps = new_sheet(5)
    top = FY1 - 3
    y = top
    for i, (k, nm) in enumerate((("T1", "SLAB STEP, H < t"), ("T2", "SLAB STEP, H > t"))):
        px, pw, ph = viewport(ps, k, 10, FX0 + 1, y)
        view_title(ps, None, y - ph - 6, nm, "1:10", (str(i + 1), "1126"))
        if i == 0:
            xl = px + pw + 8
            bar_end_legend(ps, xl, y, TBX - xl - 3)
        y = y - ph - 20
    px, pw, ph3 = viewport(ps, "E1", 10, FX0 + 1, y)
    view_title(ps, None, y - ph3 - 6, "UPSTAND ≤ 100 × 300", "1:10", ("3", "1126"),
               note="FIN OR CURB AT A SLAB EDGE, UNLESS SHOWN; DOWNSTAND MIRRORED")
    px2, pw2, ph4 = viewport(ps, "E2", 10, px + pw + 6, y)
    view_title(ps, None, y - ph4 - 6, "UPSTAND > 100 OR > 300", "1:10", ("4", "1126"),
               note="HIGHER THAN 1000: PER DESIGN")
    print(f"  1126 bottom {y - max(ph3, ph4):.1f}")


# ======================================================================= sheet 1127
def sheet_1127():
    ps = new_sheet(6)
    top = FY1 - 3
    px, pw, ph1 = viewport(ps, "G1", 20, FX0 + 1, top)
    view_title(ps, None, top - ph1 - 6, "SLAB AT A GROUND BEAM", "1:20", ("1", "1127"))
    px2, pw2, ph2 = viewport(ps, "G2", 20, px + pw + 6, top)
    view_title(ps, None, top - ph2 - 6, "THICKENED FREE EDGE", "1:20", ("2", "1127"))
    y = top - max(ph1, ph2) - 22
    px, pw, ph3 = viewport(ps, "J1", 10, FX0 + 1, y)
    view_title(ps, None, y - ph3 - 6, "CONTRACTION JOINT", "1:10", ("3", "1127"))
    px2, pw2, ph4 = viewport(ps, "J2", 10, px + pw + 6, y)
    view_title(ps, None, y - ph4 - 6, "CONSTRUCTION JOINT", "1:10", ("4", "1127"))
    y = y - max(ph3, ph4) - 22
    px, pw, ph5 = viewport(ps, "J3", 10, FX0 + 1, y)
    view_title(ps, None, y - ph5 - 6, "EXPANSION JOINT", "1:10", ("5", "1127"),
               note="ISOLATION JOINT: SAME FILLER AND SEALANT, NO DOWELS")
    px2, pw2, ph6 = viewport(ps, "GL", 200, px + pw + 6, y)
    view_title(ps, None, y - ph6 - 6, "JOINT LAYOUT", "1:200", ("6", "1127"), note="PLAN, ONE BAY")
    yn = y - max(ph5, ph6) - 22
    yb = notes_block(ps, FX0 + 3, yn, TBX - FX0 - 6, "SLAB-ON-GROUND NOTES", SOG_NOTES)
    print(f"  1127 bottom {yb:.1f}")
