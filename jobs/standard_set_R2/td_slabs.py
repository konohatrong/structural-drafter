"""
Typical slab details - STR-ST-1121 (slabs on beams), 1122 (flat slabs), 1123 (openings, steps, edges),
1123 (slab on ground). R2: 1121 - 1128, panel grid after Beca SE-12xx (REVIEW_BECA_SLAB.md).
Sources : EIT 011008-21 ch. 7, 9, 10, 11.11, 13 (Fig 13.3.8); DPT 1301/1302-61 cl. 5.2.12, 2.11.5, 2.9;
          TATA RC detailing handbook ch. 3 + appendix sheets. See SOURCES_SLAB_DETAILING.md.
Rules   : dimensions on one side of a view, notes on the other (no leader crosses a dimension); bar-end key on
          every sheet with bar ends / laps; views >= 8 m apart in model space.
"""
from td_engine import *
from members import *

BASE = "STR-ST-1121_Typical_Slab_Details_A3_R2"
SHEETS[:] = [("1121", ["TYPICAL SLAB DETAILS (1)", "SLABS ON BEAMS"], "N.T.S."),
             ("1122", ["TYPICAL SLAB DETAILS (2)", "FLAT SLAB AT THE COLUMN"], "N.T.S."),
             ("1123", ["TYPICAL SLAB DETAILS (3)", "PUNCHING SHEAR REINFORCEMENT"], "N.T.S."),
             ("1124", ["TYPICAL SLAB DETAILS (4)", "OPENINGS"], "N.T.S."),
             ("1125", ["TYPICAL SLAB DETAILS (5)", "STEPS, EDGES, CANTILEVER"], "N.T.S."),
             ("1126", ["TYPICAL SLAB DETAILS (6)", "SLAB ON GROUND"], "N.T.S."),
             ("1127", ["TYPICAL SLAB DETAILS (7)", "SLAB-ON-GROUND JOINTS"], "N.T.S."),
             ("1128", ["TYPICAL SLAB DETAILS (8)", "SLAB TABLE, FILL UNDER SLABS"], "N.T.S.")]

T = SLAB_T                     # slab thickness 150 (members.py)
CS = SLAB_CVR                  # cover to slab bars (EIT 011008 7.7.1, not exposed, <= DB16)
# DBS: slab bar DB12 (members.py)
YB1 = CS + DBS / 2             # 25  bottom outer layer (short-span bars)
YT1 = T - CS - DBS / 2         # 95  top outer layer
BB, HBM = BEAM_B, BEAM_H       # supporting beam 300 x 600 (members.py)
CVB = CVR                      # beam cover to stirrup
DTB = DT
DBB = DBM


def rbar(sp, pts, db=DBS, layer="S-REBR"):
    return bar(sp, pts, db, layer)


def beam_cut(sp, P, x0, S):
    """supporting beam cut in section under the slab: outline, stirrup, 4 corner bars (top of beam = slab top)"""
    yb = T - HBM
    pline(sp, [P(x0, 0), P(x0, yb), P(x0 + BB, yb), P(x0 + BB, 0)], "S-CONC")
    nf_hatch(sp, rect(P, x0, yb, x0 + BB, 0), S)                                    # the beam: not the subject
    rb = rdot(DBB, S)
    R_ = rb + DTB / 2
    c = CVB + DTB + DBB / 2
    cor = lambda x, y: (P(x, y)[0], P(x, y)[1], R_)
    ytb = T - c - 20                                  # beam top bars under the slab top mat
    stirrup(sp, cor(x0 + c, ytb), cor(x0 + BB - c, ytb), cor(x0 + BB - c, yb + c), cor(x0 + c, yb + c), 6 * DTB + 25,
            layer="S-REBR-NF")
    for x in (x0 + c, x0 + BB - c):
        dot(sp, P(x, ytb), rb, "S-REBR-NF")
        dot(sp, P(x, yb + c), rb, "S-REBR-NF")


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
            row_label(sp, P, rows, i, y_, S)
    dim(sp, P(-BB, 0), P(-BB, T), P(-BB - 200, 0), S, angle=90, text="t")
    # notes: right column, above the slab soffit
    note_cfg(xR=P(xe + 400, 0)[0], yminR=P(0, 20)[1], upR=True)
    kr = P(xe + 400, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 80, **kw)
    R((x_e - 250, YT1), "TOP BARS: Sn/4 AT A DISCONTINUOUS EDGE, 90° HOOK DOWN INTO THE EDGE BEAM; Sn/3 EACH SIDE OF "
                        "AN INTERIOR BEAM, Sn = LARGER ADJACENT SPAN")
    R((1500, YB1), "BOTTOM BARS: FULL SPAN, ≥ 150 mm INTO EACH SUPPORT (TO THE FAR SIDE OF AN EDGE BEAM)")
    R((1100, yd_b), "SHORT-SPAN BARS OUTERMOST, TOP AND BOTTOM; DISTRIBUTION BARS INSIDE THEM")
    R((xa1 - 250, YT1), "ALTERNATE BENT-UP OPTION: CRANK AT Sn/7 (EDGE) AND Sn/4 (INTERIOR) FROM THE FACE, "
                        "EXTRA TOP BARS @ 2 s")
    R((xi0 + BB / 2, T - 60), "SLAB TOP BARS PASS OVER THE BEAM TOP BARS")


# ----------------------------------------------------------------------- 1121/2: two-way corner panel, plan (1:100)
def corner_panel(ox, oy):
    """exterior corner panel: edge beams left and bottom, interior beams right and top. Representative top bars
    in each edge band (with their extent), bottom bars both ways, corner zone L/5 x L/5 (EIT 13.3.6, TATA Fig 3.25)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    SN, LN = 1800, 2000                                # clear spans drawn: short (x), long (y) - N.T.S.
    b = BB
    # beams (below the slab: hidden outlines), slab edge = outer face of the edge beams
    E = 450                                            # beams drawn this far past the far beams (break line)
    for x0 in (-b, SN):
        pline(sp, [P(x0, -b), P(x0 + b, -b), P(x0 + b, LN + E), P(x0, LN + E)], "S-CONC-HIDN")
    for y0 in (-b, LN):
        pline(sp, [P(-b, y0), P(SN + b + E, y0), P(SN + b + E, y0 + b), P(-b, y0 + b)], "S-CONC-HIDN")
    line(sp, P(-b, -b), P(-b, LN + E), "S-CONC-VIS")
    line(sp, P(-b, -b), P(SN + b + E, -b), "S-CONC-VIS")
    zbreak(sp, P(-b - 60, LN + E), P(SN + b + E, LN + E), S)
    zbreak(sp, P(SN + b + E, -b - 60), P(SN + b + E, LN + E), S)
    # columns under the beam intersections (cut, hatched as in every slab plan): edge columns flush with the
    # outer beam face, interior columns centred on the beam
    cx = (-b, SN + b / 2 - COL / 2)
    cy = (-b, LN + b / 2 - COL / 2)
    for x in cx:
        for y in cy:
            pts = [P(x, y), P(x + COL, y), P(x + COL, y + COL), P(x, y + COL)]
            pline(sp, pts, "S-CONC", close=True)
            hatch(sp, pts, "ANSI31", pscale("ANSI31", S, 0.8))
    # corner zone L/5 x L/5 (L = longer clear span)
    c = LN / 5
    k = COL - b                                        # corner column inside the beam faces
    zone = [P(k, 0), P(c, 0), P(c, c), P(0, c), P(0, k), P(k, k)]
    pline(sp, zone, "S-ANNO", close=True)
    hatch(sp, zone, "ANSI31", pscale("ANSI31", S, 2.0))
    # representative bottom bars (full span each way)
    xm, ym = SN * 0.62, LN * 0.55
    rbar(sp, [P(-b + 60, ym), P(SN + 150, ym)], db=12)                         # short direction, lower layer
    rbar(sp, [P(xm, -b + 60), P(xm, LN + 150)], db=12)                         # long direction
    # representative top bars, one per edge band (plain ends: no end mark)
    yt = LN * 0.35
    rbar(sp, [P(-b + 60, yt), P(SN / 4, yt)], db=12)
    rbar(sp, [P(SN - SN / 3, yt), P(SN + b + 250, yt)], db=12)
    xt = SN * 0.35
    rbar(sp, [P(xt, -b + 60), P(xt, LN / 4)], db=12)
    rbar(sp, [P(xt, LN - LN / 3), P(xt, LN + b + 250)], db=12)
    # dimensions: left and below (notes on the right)
    yd = -b - 250
    for a, b_, t in ((0, SN / 4, "Sn/4"), (SN - SN / 3, SN, "Sn/3")):
        dim(sp, P(a, -b), P(b_, -b), P(0, yd), S, text=t)
    dim(sp, P(0, -b), P(SN, -b), P(0, yd - 200), S, text="Sn")
    xd = -b - 250
    dim(sp, P(-b, 0), P(-b, LN / 4), P(xd, 0), S, angle=90, text="Ln/4")
    dim(sp, P(-b, LN - LN / 3), P(-b, LN), P(xd, 0), S, angle=90, text="Ln/3")
    dim(sp, P(-b, 0), P(-b, LN), P(xd - 200, 0), S, angle=90, text="Ln")
    note_cfg(xR=P(SN + b + 650, 0)[0])
    kr = P(SN + b + 650, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 52, **kw)
    R((SN - SN / 3 + 400, yt), "TOP BARS, EACH DIRECTION: 1/4 OF THE CLEAR SPAN AT EDGE BEAMS (HOOKED DOWN), 1/3 AT "
                               "INTERIOR BEAMS")
    R((SN * 0.85, ym), "BOTTOM BARS: SHORT DIRECTION IN THE LOWER LAYER, LONG DIRECTION ON TOP OF THEM")
    R((SN + b / 2, LN + b / 2 + COL / 2 - 60), "COLUMNS UNDER THE BEAM INTERSECTIONS (CUT)")
    R((c * 0.7, c * 0.3), "EXTERIOR CORNER, EDGE BEAMS αf > 1.0: EXTRA TOP AND BOTTOM BARS OVER L/5 x L/5 "
                          "(L = LONGER CLEAR SPAN), EACH FOR THE MAX. POSITIVE MOMENT; SPACING = SMALLER MIDSPAN SPACING")
    text(sp, "L/5", P(c / 2, c + 120), 2.0 * S, align=TA.BOTTOM_CENTER)
    text(sp, "EDGE BEAM", P(-b / 2, LN * 0.8), 2.0 * S, align=TA.MIDDLE_CENTER, rot=90)


# ----------------------------------------------------------------------- 1121/3: cantilever slab (1:25)
def cant_slab(ox, oy):
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    LC = 900                                           # cantilever from the beam face (N.T.S.)
    LB = 1100                                          # back span drawn
    x0 = 0                                             # beam at 0..BB
    xt = BB + LC
    line(sp, P(-LB, T), P(xt, T), "S-CONC")
    line(sp, P(-LB, 0), P(0, 0), "S-CONC")
    line(sp, P(BB, 0), P(xt, 0), "S-CONC")
    line(sp, P(xt, 0), P(xt, T), "S-CONC")
    beam_cut(sp, P, 0, S)
    zbreak(sp, P(-LB, -60), P(-LB, T + 60), S)
    ld = 900                                           # drawn back length
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
    note_cfg(xR=P(xt + 250, 0)[0], yminR=P(0, 20)[1], upR=True)
    kr = P(xt + 250, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 40, **kw)
    R((-ld + 300, YT1), "TOP BARS INTO THE BACK SPAN ≥ Ld, ≥ THE CANTILEVER LENGTH Lc AND ≥ ITS Sn/3 TOP-BAR "
                        "LENGTH")
    R((xt - CS - 5, YB1 + 60), "TOP BARS TURNED DOWN AT THE FREE EDGE")
    R((BB + 600, YB1), "BOTTOM BARS (≥ MIN. STEEL) ANCHORED INTO THE BEAM")
    R((BB + 400, YT1 - DBS), "DISTRIBUTION BARS INSIDE THE MAIN BARS")


# ----------------------------------------------------------------------- 1122: flat slab strips (EIT Fig 13.3.8)
HF = FLAT_T                    # flat slab thickness 200 (members.py; used on the plan: c2 + 3h band)
HFD = 400                      # slab depth drawn on the strip diagrams (SCHEMATIC - 2 x, so the bar groups read)
CF = COL                       # column 400 (members.py)
LNF = 3000                     # clear span drawn (N.T.S.)
YBF = 70                       # bottom bars (schematic)
YTF = HFD - 70                 # top bars (schematic)
GF = 60                        # offset between bar groups (schematic)


def strip_plan(ox, oy):
    """interior panel between four columns: column / middle strips, drop panels, c2 + 3h band, integrity bars"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L1, L2 = 2200, 2200                               # c/c spans drawn (x, y) - N.T.S.
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
        line(sp, P(x, -400), P(x, L2 + 400), "S-CENT")
    for y in (0, L2):
        line(sp, P(-400, y), P(L1 + 400, y), "S-CENT")
    for x in (w, L1 - w):
        line(sp, P(x, -350), P(x, L2 + 350), "S-ANNO")
    for y in (w, L2 - w):
        line(sp, P(-350, y), P(L1 + 350, y), "S-ANNO")
    # effective width for moment transfer at the column (c2 + 3h)
    e = c / 2 + 1.5 * HF
    pline(sp, [P(L1 - e, -e), P(L1 + e, -e), P(L1 + e, e), P(L1 - e, e)], "S-ANNO", close=True)
    # integrity bars through the column core (2 each way)
    for d in (-60, 60):
        rbar(sp, [P(L1 - 900, d), P(L1 + 450, d)], db=12)
        rbar(sp, [P(L1 + d, -450), P(L1 + d, 900)], db=12)
    text(sp, "COLUMN STRIP", P(L1 / 2, w / 2), 2.0 * S, align=TA.MIDDLE_CENTER)
    text(sp, "MIDDLE STRIP", P(L1 / 2, L2 / 2), 2.0 * S, align=TA.MIDDLE_CENTER)
    text(sp, "COLUMN STRIP", P(w / 2, L2 / 2), 2.0 * S, align=TA.MIDDLE_CENTER, rot=90)
    yd = -L2 / 6 - 250                                # below the drop-panel outline: no line through the texts
    dim(sp, P(0, 0), P(w, 0), P(0, yd), S, text="0.25 L")
    dim(sp, P(w, 0), P(L1 - w, 0), P(0, yd), S, text="MIDDLE STRIP")
    dim(sp, P(L1 - w, 0), P(L1, 0), P(0, yd), S, text="0.25 L")
    dim(sp, P(0, 0), P(L1, 0), P(0, yd - 220), S, text="L1 (c/c)")
    xd = -400 - 250
    dim(sp, P(0, 0), P(0, L2 / 6), P(xd, 0), S, angle=90, text="≥ L2/6", tside="R")   # text beyond, in line
    dim(sp, P(0, 0), P(0, L2), P(xd - 220, 0), S, angle=90, text="L2 (c/c)")
    note_cfg(xR=P(L1 + 700, 0)[0])
    kr = P(L1 + 700, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 44, **kw)
    R((L1 + e, e * 0.5), "c2 + 3h BAND: TOP BARS FOR γf Mu CONCENTRATED HERE (≥ ½ OF THE COLUMN-STRIP TOP BARS "
                         "IN SEISMIC FRAMES)")
    R((L1 + 60, 750), "≥ 2 BOTTOM BARS EACH WAY THROUGH THE COLUMN CORE")
    R((L1 + L1 / 6, -L2 / 6 * 0.5), "DROP PANEL (IF ANY) ≥ L/6 EACH WAY FROM THE COLUMN CENTRELINE")
    R((L1 - w, L2 * 0.4), "COLUMN STRIP: 0.25 × SMALLER SPAN EACH SIDE OF THE COLUMN LINE")


# ----------------------------------------------------------------------- 1122: drop panel and column capital (1:50)
def drop_capital(ox, oy):
    """section through an interior column head: drop panel >= h/4 deep and >= L/6 each way (EIT 13.2.5);
    capital sides >= 45 deg, size <= L/4 (TATA p.74); critical sections d/2 from the capital and from the drop edge"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    h, c = HF, CF
    L = 3600                                           # c/c span drawn (for L/6, L/4) - N.T.S.
    hd = DROP_H                                        # drop projection 50 (>= h/4, members.py)
    xd = L / 6                                         # drop edge from the column centreline
    hc = 300                                           # capital depth below the drop
    wc = c / 2 + hc                                    # capital half-width at the top (45 deg)
    xs = 900
    yb = -hd - hc - 100
    # concrete outline: slab + drop + capital + column
    line(sp, P(-xs, h), P(xs, h), "S-CONC")
    pline(sp, [P(-xs, 0), P(-xd, 0), P(-xd, -hd), P(-wc, -hd), P(-c / 2, -hd - hc), P(-c / 2, yb)], "S-CONC")
    pline(sp, [P(xs, 0), P(xd, 0), P(xd, -hd), P(wc, -hd), P(c / 2, -hd - hc), P(c / 2, yb)], "S-CONC")
    for x in (-c / 2, c / 2):
        line(sp, P(x, h), P(x, h + 200), "S-CONC")
    zbreak(sp, P(-xs, -60), P(-xs, h + 60), S)
    zbreak(sp, P(xs, -60), P(xs, h + 60), S)
    zbreak(sp, P(-c / 2 - 60, yb), P(c / 2 + 60, yb), S)
    nf_hatch(sp, rect(P, -c / 2, yb, c / 2, -hd - hc), S)                          # column: not the subject
    nf_hatch(sp, rect(P, -c / 2, h, c / 2, h + 200), S)
    zbreak(sp, P(-c / 2 - 60, h + 200), P(c / 2 + 60, h + 200), S)
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
        rbar(sp, [P(sx * (c / 2 - 60), yb), P(sx * (c / 2 - 60), h - 50)], db=20, layer="S-REBR-NF")
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
    dim(sp, P(-xd, -hd), P(xd, -hd), P(0, yd - 200), S, text="DROP ≥ L/3 (L/6 EACH WAY)")
    dim(sp, P(-xd, -hd), P(-xd, 0), P(-xs - 150, 0), S, angle=90, text="≥ h/4", tside="L")
    dim(sp, P(-xs, 0), P(-xs, h), P(-xs - 150, 0), S, angle=90, text="h")
    line(sp, P(0, yb - 100), P(0, h + 420), "S-CENT")          # centreline stops above the dimensions
    note_cfg(xR=P(xs + 250, 0)[0], yminR=P(0, 20)[1], upR=True)
    kr = P(xs + 250, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 64, **kw)
    R((xd + (h - 40) / 2, h + 60), "CRITICAL SECTIONS: d/2 FROM THE CAPITAL (DROP DEPTH) AND d/2 OUTSIDE THE DROP "
                                   "EDGE (SLAB DEPTH)")
    R((wc - 100, -hd - 60), "CAPITAL: SIDES ≥ 45°, CAGE OF INCLINED BARS AND HOOPS; COLUMN CAST TO THE UNDERSIDE "
                            "OF THE HEAD FIRST")
    R((c / 2 - 60, h - 120), "COLUMN BARS CONTINUE UP THROUGH THE HEAD INTO THE SLAB")
    R((xd - 200, -hd), "DROP PANEL ≥ h/4 BELOW THE SLAB, ≥ L/6 EACH WAY FROM THE COLUMN CENTRELINE")


# ----------------------------------------------------------------------- 1123: punching shear reinforcement
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
    S = 25
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
    nf_hatch(sp, rect(P, -c / 2, -300, c / 2, 0), S)                                # column: not the subject
    nf_hatch(sp, rect(P, -c / 2, h, c / 2, h + 250), S)
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
    # below the column stub break (no column line through the texts); texts outside the short spans
    dim(sp, P(c / 2, 0), P(xs[0], 0), P(0, -420), S, text="s0", tside="L")
    dim(sp, P(xs[0], 0), P(xs[1], 0), P(0, -420), S, text="s", tside="R")
    note_cfg(xR=P(L + 250, 0)[0], yminR=P(0, 20)[1], upR=True)
    kr = P(L + 250, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 42, **kw)
    if kind == "STIR":
        R((xs[1] - 4, h / 2), "CLOSED STIRRUPS ROUND THE TOP AND BOTTOM BARS; ONLY WHERE d ≥ 150 mm AND ≥ 16 × "
                              "STIRRUP DIA.")
    else:
        R((xs[1], h / 2), "HEADED STUDS WELDED TO A BASE RAIL; HEIGHT = h − COVERS − ½ db")
        R((xs[2], CS), "HEADS AND RAIL: SAME COVER AS THE FLEXURAL BARS")
    R((L - 100, yt), "TOP FLEXURAL BARS OVER THE COLUMN")


# ----------------------------------------------------------------------- 1124: openings (plans)
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
      "2-DB12 × 1200 mm DIAGONAL BARS @ 50 mm, TOP AND BOTTOM, AT EVERY CORNER (UNLESS SHOWN)")
    R((a / 2 + 20, -150), "≤ 300 mm: BARS RE-SPACED ROUND THE OPENING; 300 – 600 mm: CUT BARS STOP WITH COVER, THEIR AREA "
                          "ADDED HALF EACH SIDE (≥ 1-DB12), TOP AND BOTTOM")


def opening_large(ox, oy):
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    a, b = 900, 700                                    # opening drawn (>= 600) - N.T.S.
    ex = 600                                           # trimmer extension drawn past the corners (>= 800, Ld)
    W, Hh = a + 2 * ex + 200, b + 2 * ex + 200
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
            diag_bars(sp, P, sx * a / 2, sy * b / 2, sx, sy, 800, S, off=250)
    yd = -Hh / 2 - 250
    dim(sp, P(-a / 2, -Hh / 2), P(a / 2, -Hh / 2), P(0, yd), S, text="≥ 600")
    dim(sp, P(a / 2, -Hh / 2), P(a / 2 + ex, -Hh / 2), P(0, yd), S, text="≥ 800, Ld")
    note_cfg(xR=P(W / 2 + 350, 0)[0])
    kr = P(W / 2 + 350, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 40, **kw)
    R((a / 2 + ex - 200, b / 2 + 160), "TRIMMER BARS 2-DB16 @ 100 mm EACH SIDE, TOP AND BOTTOM, ≥ 800 mm AND ≥ Ld PAST THE "
                                       "CORNERS (UNLESS SHOWN)")
    R((a / 2 + 250 * 0.7071 + 250 * 0.7071, b / 2 + 250 * 0.7071 - 250 * 0.7071),
      "2-DB12 × 1200 mm DIAGONAL BARS AT EVERY CORNER, TOP AND BOTTOM")
    R((a / 2 + 160, -b / 2 - ex + 150), "EACH SIDE: ADDED AREA ≥ ½ OF THE BARS CUT BY THE OPENING, IN EACH DIRECTION")


def opening_flat(ox, oy):
    """openings in flat slabs by strip zone (EIT 13.4.2) and near columns (11.11.6): plan N.T.S."""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L = 2000                                           # c/c span drawn - N.T.S.
    w = 0.25 * L
    for (x, y) in ((0, 0), (L, 0), (0, L), (L, L)):
        pts = [P(x - CF / 2, y - CF / 2), P(x + CF / 2, y - CF / 2), P(x + CF / 2, y + CF / 2), P(x - CF / 2, y + CF / 2)]
        pline(sp, pts, "S-CONC", close=True)
        hatch(sp, pts, "ANSI31", pscale("ANSI31", S, 0.8))
    for v in (0, L):
        line(sp, P(v, -350), P(v, L + 350), "S-CENT")
        line(sp, P(-350, v), P(L + 350, v), "S-CENT")
    for v in (w, L - w):
        line(sp, P(v, -250), P(v, L + 250), "S-ANNO")
        line(sp, P(-250, v), P(L + 250, v), "S-ANNO")
    # zone hatches: middle x middle (any size), column x middle, column x column
    hatch(sp, [P(w, w), P(L - w, w), P(L - w, L - w), P(w, L - w)], "ANSI31", pscale("ANSI31", S, 3.0))
    # example openings
    def box(x0, y0, x1, y1):
        pline(sp, [P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)], "S-CONC", close=True)
        line(sp, P(x0, y0), P(x1, y1), "S-CONC-VIS")
        line(sp, P(x0, y1), P(x1, y0), "S-CONC-VIS")
    box(800, 870, 1200, 1130)                          # middle x middle
    box(900, 260, 1100, 420)                           # column x middle
    box(300, 280, 400, 380)                            # near the column (within 10h), column x column
    for (tx, ty) in ((300, 380), (400, 280)):          # tangents from the column centre (ineffective perimeter)
        line(sp, P(0, 0), P(tx * 1.6, ty * 1.6), "S-ANNO")
    note_cfg(xR=P(L + 500, 0)[0])
    kr = P(L + 500, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 52, **kw)
    R((1200, 1000), "MIDDLE ∩ MIDDLE STRIP: ANY SIZE; THE PANEL'S TOTAL BARS KEPT (INTERRUPTED BARS ADDED AT THE SIDES)")
    R((1100, 340), "COLUMN ∩ MIDDLE STRIP: ≤ 1/4 OF THE BARS OF EITHER STRIP INTERRUPTED; ADD THEM AT THE SIDES")
    R((400, 330), "COLUMN ∩ COLUMN STRIP: ≤ 1/8 OF THE COLUMN-STRIP WIDTH; ADD THE INTERRUPTED BARS AT THE SIDES")
    R((520, 520), "WITHIN 10h OF A COLUMN (OR IN A COLUMN STRIP): PUNCHING PERIMETER BETWEEN THE TANGENTS FROM THE "
                   "COLUMN CENTRE IS INEFFECTIVE")


# ----------------------------------------------------------------------- 1124: slab steps (sections, 1:20)
def slab_step(ox, oy, big):
    """TATA p.181. big=False: H < T, thickened zone T wide; big=True: H > T, the lower-slab soffit runs t past
    the step face, then a 45 deg haunch up to the upper soffit (TATA, mirrored: upper slab left)"""
    S = 25
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


# ----------------------------------------------------------------------- 1125: slab-edge upstands (sections, 1:10)
def edge_upstand(ox, oy, big):
    """TATA p.181 / 182 (unless shown): upstand fin or curb on a slab edge. big=False: <= 100 thick, <= 300 high,
    single L-bars; big=True: > 100 thick or > 300 high, hairpins both faces. Downstands: the same, mirrored."""
    S = 25
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
    dim(sp, P(x0, 0), P(0, 0), P(0, -150), S, text="≤ 100" if not big else "> 100", tside="L")
    dim(sp, P(0, 0), P(anc - c, 0), P(0, -150), S, text="400")
    note_cfg(xR=P(L + 200, 0)[0], yminR=P(0, 10)[1], upR=True)
    kr = P(L + 200, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 40, **kw)
    if not big:
        R((xv, t + hh * 0.6), "DB10 @ 250 mm L-BARS, 400 mm INTO THE SLAB")
        R((xv, t + hh - c - 20), "1-DB12 AT THE TIP, 1-DB10 AT THE ROOT", ring=12)
    else:
        R((xb, t + hh * 0.6), "DB10 @ 250 mm HAIRPINS, BOTH FACES, 400 mm INTO THE SLAB")
        R((xb - 14, t + hh - c - 22), "2-DB12 AT THE TIP, 2-DB10 AT THE ROOT", ring=12)
    R((L - 150, t - c), "SLAB BARS TO THE FAR FACE OF THE UPSTAND")


# ----------------------------------------------------------------------- 1126 / 1127: slab on ground
# Presentation after Beca SE-1210 - 1215 (joint catalogue, FIRST / SECOND POUR header, enlarged seal details,
# joint table by slab thickness); content TATA 3.26 - 3.43, ACI 302.1R / 360R. See REVIEW_BECA_SLAB.md.
SG = 10                         # R2 exception: slab-on-ground SECTIONS at a dummy 1:10 (a 20 filler or a 3 saw cut
                                # is invisible at 1:25). All slab-on-ground sections share it; plans stay 1:25.
TG = 150                        # slab-on-ground thickness (drawn)
MESH = 40                       # mesh below the top surface (30 - 50, <= t/2)
SAND = 100                      # compacted sand bed drawn
PE = 8                          # polyethylene sheet drawn just under the slab
HD = 200                        # half dowel length drawn (RB19 x 400 for t = 150; table on 1126)


def offset_below(pts, d):
    """polyline (left to right) offset d square to each segment, on its lower side; mitred corners"""
    segs = []
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        nx, ny = (y1 - y0) / L * d, -(x1 - x0) / L * d          # right-hand normal = below for left-to-right
        segs.append(((x0 + nx, y0 + ny), (x1 + nx, y1 + ny)))
    out = [segs[0][0]]
    for (a0, a1), (b0, b1) in zip(segs[:-1], segs[1:]):
        dax, day = a1[0] - a0[0], a1[1] - a0[1]
        dbx, dby = b1[0] - b0[0], b1[1] - b0[1]
        den = dax * dby - day * dbx
        if abs(den) < 1e-9:
            out.append(a1)
            continue
        t = ((b0[0] - a0[0]) * dby - (b0[1] - a0[1]) * dbx) / den
        out.append((a0[0] + t * dax, a0[1] + t * day))
    out.append(segs[-1][1])
    return out


def sand_bed(sp, P, x0, x1, S, depth=SAND, prof=None, sheet=True):
    """compacted sand bed filled right up to the slab soffit (user 2026-09-30), the 0.2 polyethylene sheet drawn
    just inside it, the subgrade line below. prof = soffit points left to right (default flat at y = 0 from x0
    to x1); the subgrade stays level at y = -depth, so a thickened edge (prof down to -depth) sits on the
    subgrade with no sand under it (user 2026-09-30: "no need here")"""
    prof = prof or [(x0, 0), (x1, 0)]
    low = [(prof[0][0], -depth), (prof[-1][0], -depth)]
    hatch(sp, [P(*q) for q in prof + low[::-1]], "AR-SAND", pscale("AR-SAND", S, 0.6), layer="S-HATCH-SAND")
    pline(sp, [P(*q) for q in low], "S-SOIL")
    if not sheet:                                       # lean concrete above instead of the sheet (1126/4)
        return
    pe = offset_below(prof, PE)                         # parallel to the soffit, also on a slope (user 2026-09-30)
    (xa, ya), (xb, yb) = pe[0], pe[1]
    if ya < -depth < yb:                                # start the sheet where it meets the subgrade
        pe[0] = (xa + (xb - xa) * (-depth - ya) / (yb - ya), -depth)
    pline(sp, [P(*q) for q in pe], "S-MEMB")


def mesh_section(sp, P, x0, x1, y, S, s=200, layer="S-REBR-SEC"):
    rbar(sp, [P(x0, y), P(x1, y)], db=9, layer=layer)
    r = rdot(9, S) * 0.8
    x = x0 + 60
    while x < x1 - 30:
        dot(sp, P(x, y - 9), r, layer)
        x += s


def slab_piece(sp, P, x0, x1, S, face=None):
    """slab on ground between x0 < x1: top, bottom, formed / joint face at x = face, break lines at the other ends"""
    line(sp, P(x0, TG), P(x1, TG), "S-CONC")
    line(sp, P(x0, 0), P(x1, 0), "S-CONC")
    for xe in (x0, x1):
        if face is not None and abs(xe - face) < 1e-6:
            line(sp, P(xe, 0), P(xe, TG), "S-CONC")
        else:
            zbreak(sp, P(xe, -SAND - 40), P(xe, TG + 40), S)


def dowel(sp, P, x0, x1, y, S, free=None, cap=False):
    """plain round dowel x0 -> x1 at y; free = (xa, xb): greased / sleeved length (grey sleeve lines); cap on
    the free end with 25 travel (expansion joints)"""
    rbar(sp, [P(x0, y), P(x1, y)], db=19, layer="S-DWL")
    if free:
        xa, xb = free
        for dy in (-15, 15):
            line(sp, P(xa, y + dy), P(xb, y + dy), "S-DWL-SLV")
        if cap:
            pline(sp, [P(xb, y - 15), P(xb + 30, y - 15), P(xb + 30, y + 15), P(xb, y + 15)], "S-DWL-SLV")


def basket(sp, P, x, y, S):
    """dowel basket / chair leg under a dowel: inverted V to the slab soffit"""
    pline(sp, [P(x - 45, 12), P(x, y - 12), P(x + 45, 12)], "S-REBR-SEC")


def detail_ref(sp, P, c, r, top, bot, S, to):
    """Beca enlarged-detail reference: dashed circle round the area + split bubble (detail / sheet) on a line"""
    sp.add_circle(P(*c), r, dxfattribs=A("S-ZONE-DASH"))
    br = 4.6 * S
    bx, by = P(*to)
    cx, cy = P(*c)
    L = math.hypot(bx - cx, by - cy)
    line(sp, (cx + (bx - cx) / L * r, cy + (by - cy) / L * r), (bx - (bx - cx) / L * br, by - (by - cy) / L * br),
         "S-ANNO")
    sp.add_circle((bx, by), br, dxfattribs=A("S-SYMB"))
    line(sp, (bx - br, by), (bx + br, by), "S-SYMB")
    text(sp, top, (bx, by + 2.1 * S), (2.8 if len(top) < 2 else 2.2) * S, "S-TEXT", TA.MIDDLE_CENTER, style="ANB")
    text(sp, bot, (bx, by - 2.2 * S), 2.0 * S, "S-TEXT", TA.MIDDLE_CENTER)


# ----------------------------------------------------------------------- 1126/1: isolation joint at a ground beam
def sog_at_beam(ox, oy):
    """interior slab against a ground beam (IJ): full-depth filler, sealed top, slab free of the beam"""
    S = SG
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    gb, gh = 250, 600
    L = 520
    g = 20                                              # isolation gap
    pline(sp, [P(-gb, TG + 50), P(0, TG + 50), P(0, TG + 50 - gh), P(-gb, TG + 50 - gh)], "S-CONC")
    zbreak(sp, P(-gb, TG + 90), P(-gb, TG + 10 - gh), S)
    nf_hatch(sp, rect(P, -gb, TG + 50 - gh, 0, TG + 50), S)                        # ground beam: not the subject
    slab_piece(sp, P, g, L, S, face=g)
    hatch(sp, [P(0, 0), P(g, 0), P(g, TG - 33), P(0, TG - 33)], "ANSI31", pscale("ANSI31", S, 0.6))
    pline(sp, [P(0, 0), P(g, 0), P(g, TG - 33), P(0, TG - 33)], "S-JFILL", close=True)
    sand_bed(sp, P, 0, L, S)
    mesh_section(sp, P, g + 50, L, TG - MESH, S)
    detail_ref(sp, P, (g / 2, TG - 10), 50, "C", "1127", S, (200, TG + 170))
    dim(sp, P(0, TG + 50), P(g, TG + 50), P(0, TG + 130), S, text="20", tside="R")
    note_cfg(xR=P(L + 100, 0)[0], xL=P(-gb - 100, 0)[0])
    kr, kl = P(L + 100, 0), P(-gb - 100, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 36, **kw)
    Lf = lambda tip, s_, **kw: leader(sp, P(*tip), kl, s_, S, "L", 30, **kw)
    R((L - 200, TG - MESH), "SINGLE MESH 30 – 50 mm BELOW THE TOP, NEVER BELOW t/2, ON CHAIRS; STOPPED 50 mm FROM THE JOINT")
    R((L - 100, -PE), "0.2 mm POLYETHYLENE SHEET, LAPS 150 mm TAPED")
    R((L - 280, -60), f"COMPACTED MOIST SAND 50 – 100 mm THICK ON COMPACTED SUBGRADE ({TAB('FILL')})")
    Lf((g / 2, TG * 0.4), "ISOLATION JOINT (IJ): 20 mm COMPRESSIBLE FILLER, FULL DEPTH; SLAB FREE OF THE BEAM; "
                          "SEAL: DETAIL C")
    Lf((-gb / 2, TG - 250), "GROUND BEAM, WALL OR PILE CAP")


# ----------------------------------------------------------------------- 1126/2: thickened free edge
def sog_edge(ox, oy):
    """thickened free edge: +50..100 deep, 100 flat then 45 deg; mesh turned down into the thickening"""
    S = SG
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L = 560
    dt = 100                                            # extra depth
    pline(sp, [P(L, TG), P(0, TG), P(0, -dt), P(100, -dt), P(100 + dt, 0), P(L, 0)], "S-CONC")
    zbreak(sp, P(L, -SAND - 40), P(L, TG + 40), S)
    sand_bed(sp, P, 100, L, S, depth=dt, prof=[(100, -dt), (100 + dt, 0), (L, 0)])      # thickening on the subgrade
    line(sp, P(-60, -dt), P(100, -dt), "S-SOIL")
    rbar(sp, [P(50, -dt + 50), P(50, TG - MESH), P(L, TG - MESH)], db=9, layer="S-REBR-SEC")
    r = rdot(9, S) * 0.8
    x = 260
    while x < L - 30:
        dot(sp, P(x, TG - MESH - 9), r, "S-REBR-SEC")
        x += 200
    xl = -130
    dim(sp, P(0, -dt), P(0, 0), P(xl, 0), S, angle=90, text="50 – 100")
    dim(sp, P(0, 0), P(0, TG), P(xl, 0), S, angle=90, text="t")
    dim(sp, P(0, -dt), P(100, -dt), P(0, -dt - 160), S, text="100")
    note_cfg(xR=P(L + 100, 0)[0])
    kr = P(L + 100, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 32, **kw)
    R((50, 30), "MESH TURNED DOWN 90° INTO THE THICKENED EDGE")
    R((100 + dt / 2, -dt / 2), "EDGE THICKENED 50 – 100 mm, 100 mm FLAT THEN 45°, AGAINST WASH-OUT OF THE SUBGRADE")
    R((L - 120, -60), "SAND BED AND POLYETHYLENE SHEET: SEE 1")


# ----------------------------------------------------------------------- 1126/4: slab on lean concrete
def sog_lean(ox, oy):
    """alternative base (user 2026-09-30): 50 lean concrete on the sand bed instead of the polyethylene sheet"""
    S = SG
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L = 520
    lt = LEAN_T                                         # 50 (members.py)
    slab_piece(sp, P, 0, L, S)
    lean = [P(0, 0), P(L, 0), P(L, -lt), P(0, -lt)]
    line(sp, P(0, -lt), P(L, -lt), "S-LEAN")
    hatch(sp, lean, "AR-CONC", pscale("AR-CONC", S, 2.5), layer="S-HATCH-SAND")          # aggregate, unlike the sand
    sand_bed(sp, P, 0, L, S, depth=lt + SAND, prof=[(0, -lt), (L, -lt)], sheet=False)
    mesh_section(sp, P, 0, L, TG - MESH, S)
    xl = -120
    dim(sp, P(0, 0), P(0, TG), P(xl, 0), S, angle=90, text="t")
    dim(sp, P(0, -lt), P(0, 0), P(xl, 0), S, angle=90, text="50")
    dim(sp, P(0, -lt - SAND), P(0, -lt), P(xl, 0), S, angle=90, text="50 – 100")
    note_cfg(xR=P(L + 80, 0)[0])
    kr = P(L + 80, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 32, **kw)
    R((L - 120, TG - MESH), "MESH AND JOINTS AS 1 AND 1127 (TABLE 18)")
    R((L - 200, -lt / 2), "LEAN CONCRETE 50 mm (f'c ≥ 15 MPa OR 1:3:5), TOP ± 10 mm, INSTEAD OF THE SHEET; DAMPEN "
                          "BEFORE THE POUR")
    R((L - 330, -lt - 60), f"COMPACTED SAND 50 – 100 mm THICK ON COMPACTED SUBGRADE ({TAB('FILL')})")


# ----------------------------------------------------------------------- 1128/1: slab on compacted fill
def sog_fill(ox, oy):
    """where the floor is raised above the stripped ground (user 2026-09-30): compacted subgrade, selected fill in
    layers, sand bed, sheet, slab. Two fill layers drawn, a break in the fill for any depth; spec in TABLE 20"""
    S = SG
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L = 700
    lay = 200                                           # fill layer, <= 200 compacted (DPT 2114 5.1.5)
    yf = -SAND - 2 * lay                                # underside of the fill = top of the compacted subgrade
    slab_piece(sp, P, 0, L, S)
    sand_bed(sp, P, 0, L, S)
    mesh_section(sp, P, 0, L, TG - MESH, S)
    fill = [P(0, -SAND), P(L, -SAND), P(L, yf), P(0, yf)]
    hatch(sp, fill, "GRAVEL", pscale("GRAVEL", S, 0.6))                              # outlines: the grey pen reads
    line(sp, P(0, -SAND - lay), P(L, -SAND - lay), "S-ZONE-DASH")                  # layer joint
    line(sp, P(0, yf), P(L, yf), "S-SOIL")
    earth_band(sp, [P(0, yf), P(L, yf)], 150, S)                                   # compacted subgrade (existing)
    for xe in (0, L):
        line(sp, P(xe, -SAND), P(xe, yf - 150), "S-BREAK")
    xl = -120
    dim(sp, P(0, 0), P(0, TG), P(xl, 0), S, angle=90, text="t")
    dim(sp, P(0, -SAND), P(0, 0), P(xl, 0), S, angle=90, text="50 – 100")
    dim(sp, P(0, -SAND - lay), P(0, -SAND), P(xl, 0), S, angle=90, text="≤ 200")
    dim(sp, P(0, yf), P(0, -SAND - lay), P(xl, 0), S, angle=90, text="≤ 200")
    note_cfg(xR=P(L + 100, 0)[0])
    kr = P(L + 100, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 40, **kw)
    R((L - 150, TG - MESH), "SLAB, MESH, SHEET AND SAND BED AS 1126/1 (OR LEAN CONCRETE, 1126/4)")
    R((L - 250, -SAND - lay / 2), f"FILL (SOIL AGGREGATE OR SAND) IN LAYERS ≤ 200 mm THICK AFTER COMPACTION, EACH ≥ 95 % "
                                  f"MODIFIED PROCTOR ({TAB('FILL')})")
    R((L - 400, -SAND - lay), "EACH LAYER TESTED AND ACCEPTED BEFORE THE NEXT")
    R((L - 300, yf - 70), f"SUBGRADE: TOPSOIL, ROOTS, ORGANIC AND SOFT MATERIAL REMOVED; SURFACE WETTED, THE TOP 150 mm "
                          f"OF THE EXISTING GROUND COMPACTED ≥ 95 % STANDARD PROCTOR ({TAB('FILL')})")


# ----------------------------------------------------------------------- 1127/1 - 4: joints (1:10)
def sog_joint(ox, oy, kind):
    """SJ sawn (contraction) joint with dowel baskets (SJD), CJ construction joint, CJE against an existing slab,
    EJ expansion joint. Each: FIRST / SECOND POUR header (Beca), EQ | EQ dowel dimensions, seal detail bubble."""
    S = SG
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L = 320
    g = 20 if kind == "EJ" else 0
    yd = TG / 2
    xa, xb = -g / 2, g / 2                              # joint faces
    if kind == "SJ":                                    # one pour: an induced crack under the saw cut
        line(sp, P(-L, TG), P(-1.5, TG), "S-CONC")
        line(sp, P(1.5, TG), P(L, TG), "S-CONC")
        line(sp, P(-L, 0), P(L, 0), "S-CONC")
        for xe in (-L, L):
            zbreak(sp, P(xe, -SAND - 40), P(xe, TG + 40), S)
        pline(sp, [P(-1.5, TG), P(-1.5, TG - 40), P(1.5, TG - 40), P(1.5, TG)], "S-CONC")
        line(sp, P(0, 0), P(0, TG - 40), "S-CONC-HIDN")
        mesh_section(sp, P, -L, xa - 50, TG - MESH, S)
    elif kind == "CJE":                                 # existing slab: not the subject -> hatched grey
        line(sp, P(-L, TG), P(xa, TG), "S-CONC")
        line(sp, P(-L, 0), P(xa, 0), "S-CONC")
        line(sp, P(xa, 0), P(xa, TG), "S-CONC")
        zbreak(sp, P(-L, -SAND - 40), P(-L, TG + 40), S)
        nf_hatch(sp, rect(P, -L, 0, xa, TG), S)
        mesh_section(sp, P, -L, xa - 60, TG - 50, S, layer="S-REBR-NF")
        slab_piece(sp, P, xb, L, S, face=xb)
    else:
        slab_piece(sp, P, -L, xa, S, face=xa)
        slab_piece(sp, P, xb, L, S, face=xb)
        mesh_section(sp, P, -L, xa - 50, TG - MESH, S)
    sand_bed(sp, P, -L, L, S)
    mesh_section(sp, P, xb + 50, L, TG - MESH, S)
    if kind == "EJ":
        hatch(sp, [P(xa, 0), P(xb, 0), P(xb, TG - 33), P(xa, TG - 33)], "ANSI31", pscale("ANSI31", S, 0.6))
        pline(sp, [P(xa, 0), P(xb, 0), P(xb, TG - 33), P(xa, TG - 33)], "S-JFILL", close=True)
    if kind in ("CJ", "CJE"):                           # sawn reservoir along the formed joint
        pline(sp, [P(-3, TG), P(-3, TG - 20), P(3, TG - 20), P(3, TG)], "S-CONC")
    # dowel: bonded half in the first pour (or drilled + epoxied into the existing slab), free half greased
    dowel(sp, P, -HD, HD, yd, S, free=(xb, HD), cap=(kind == "EJ"))
    if kind == "SJ":
        for x in (-120, 120):
            basket(sp, P, x, yd, S)
    if kind == "CJE":
        pline(sp, [P(xa, yd - 16), P(-HD - 20, yd - 16), P(-HD - 20, yd + 16), P(xa, yd + 16)], "S-DWL-SLV")
    if kind != "SJ":                                    # pour header (Beca); a sawn joint is one pour
        lt, rt = ("EXISTING SLAB", "NEW SLAB") if kind == "CJE" else ("FIRST POUR", "SECOND POUR")
        pour_header(sp, P, 0, -L + 30, L - 30, TG + 260, S, lt, rt, y_joint=TG + 110)
    seal = "C" if kind == "EJ" else "A, B"
    detail_ref(sp, P, (0, TG - 10), 50, seal, "1127", S, (130, TG + 150))
    dim(sp, P(-HD, -SAND), P(0, -SAND), P(0, -SAND - 100), S, text="EQ")
    dim(sp, P(0, -SAND), P(HD, -SAND), P(0, -SAND - 100), S, text="EQ")
    note_cfg(xR=P(L + 70, 0)[0], xL=P(-L - 70, 0)[0])
    kr, kl = P(L + 70, 0), P(-L - 70, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 30, **kw)
    Lf = lambda tip, s_, **kw: leader(sp, P(*tip), kl, s_, S, "L", 30, **kw)
    if kind == "SJ":
        Lf((-1.5, TG - 30), f"SAW CUT 3 mm WIDE × t/4 DEEP ({TAB('SOG')}) 4 – 12 HOURS AFTER THE POUR, AS SOON AS THE EDGES "
                            "DO NOT RAVEL; SEAL: DETAIL A OR B")
        Lf((-L + 120, TG - MESH), "MESH STOPPED 50 mm EACH SIDE OF THE JOINT LINE (CONTINUOUS ONLY IF DESIGNED)")
        R((150, yd), f"SJD (DOWELLED, WHERE MARKED): DOWELS PER {TAB('SOG')} CENTRED ON THE CUT, ON WELDED BASKETS "
                     "FIXED TO THE SUBGRADE; SJ: NO DOWELS")
        R((95, 25), "BASKET SPACER WIRES CUT AFTER FIXING, BEFORE THE POUR")
    elif kind == "CJ":
        Lf((0, TG * 0.35), "BULKHEAD ON A PLANNED JOINT LINE; FACE STRAIGHT AND VERTICAL; DEBONDING COAT BEFORE THE "
                           "SECOND POUR")
        Lf((-L + 120, TG - MESH), "MESH STOPPED 50 mm EACH SIDE")
        R((HD - 60, yd), f"PLAIN ROUND DOWEL PER {TAB('SOG')} AT MID-DEPTH, THROUGH HOLES IN THE BULKHEAD; "
                         "SECOND-POUR HALF GREASED OR SLEEVED")
        R((3, TG - 10), "SAWN RESERVOIR 6 × 20 mm ALONG THE JOINT; SEAL: DETAIL A OR B")
    elif kind == "CJE":
        Lf((-L + 80, TG * 0.75), "EXISTING SLAB: DAMAGED EDGE SAWN BACK ≥ 50 mm TO SOUND CONCRETE")
        Lf((-HD + 40, yd), "DOWEL DRILLED 200 mm INTO THE EXISTING SLAB AT MID-DEPTH (HOLE Ø + 6 mm), EPOXY GROUTED, LEVEL "
                           "AND SQUARE TO THE JOINT")
        R((HD - 60, yd), f"FREE HALF GREASED OR SLEEVED; DOWELS PER {TAB('SOG')}")
        R((L - 80, TG - MESH), "NEW MESH STOPPED 50 mm FROM THE JOINT")
    else:
        Lf((xa, TG * 0.35), "EXPANSION JOINT (EJ): 20 mm COMPRESSIBLE FILLER, FULL DEPTH, FIXED TO THE FIRST POUR; "
                            "SEAL: DETAIL C")
        Lf((-L + 120, TG - MESH), "MESH STOPPED 50 mm FROM EACH FACE")
        R((HD - 60, yd), f"DOWEL PER {TAB('SOG')}, SECOND-POUR HALF GREASED WITH A CAP: 25 mm FREE TRAVEL; ISOLATION "
                         "JOINT (IJ): THE SAME WITHOUT DOWELS")


# ----------------------------------------------------------------------- 1127/A - C: joint seals (1:2)
def sog_seal(ox, oy, kind):
    """top 75 of the slab at a joint, enlarged: A elastomeric sealant on a backer rod; B semi-rigid filler, full
    depth of the cut (hard wheels); C expansion / isolation joint: filler, backer rod, sealant"""
    S = 2
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    L = 30
    yb = -70                                            # slab top at y = 0, piece 70 deep, break below
    hw = 10 if kind == "C" else 3                       # half width of the joint at the surface
    for sx in (-1, 1):
        line(sp, P(sx * hw, 0), P(sx * L, 0), "S-CONC")
        zbreak(sp, P(sx * L, 5), P(sx * L, yb - 5), S)
    zbreak(sp, P(-L - 5, yb), P(L + 5, yb), S)
    if kind in ("A", "B"):
        cut = 38                                        # t/4 for t = 150
        prof = [P(-3, 0), P(-3, -20), P(-1.5, -20), P(-1.5, -cut), P(1.5, -cut), P(1.5, -20), P(3, -20), P(3, 0)]
        pline(sp, prof, "S-CONC")
        line(sp, P(0, -cut), P(0, yb), "S-CONC-HIDN")
        if kind == "A":
            sp.add_circle(P(0, -11.5), 3, dxfattribs=A("S-JFILL"))                               # backer rod
            hatch(sp, [P(-3, -3), P(3, -3), P(3, -8.5), P(-3, -8.5)], "SOLID", 1)                  # sealant
        else:
            hatch(sp, prof, "SOLID", 1)
        dim(sp, P(-3, 0), P(3, 0), P(0, 16), S, text="6")
        dim(sp, P(L, 0), P(L, -20), P(L + 12, 0), S, angle=90, text="20")
        dim(sp, P(L, 0), P(L, -cut), P(L + 24, 0), S, angle=90, text="t/4")
    else:
        line(sp, P(-10, 0), P(-10, yb), "S-CONC")
        line(sp, P(10, 0), P(10, yb), "S-CONC")
        hatch(sp, [P(-10, -33), P(10, -33), P(10, yb), P(-10, yb)], "ANSI31", pscale("ANSI31", S, 0.6))
        line(sp, P(-10, -33), P(10, -33), "S-JFILL")
        sp.add_ellipse(P(0, -23), major_axis=(0, 11.5), ratio=10 / 11.5, dxfattribs=A("S-JFILL"))   # rod, squeezed
        hatch(sp, [P(-10, -3), P(10, -3), P(10, -13), P(-10, -13)], "SOLID", 1)
        dim(sp, P(-10, 0), P(10, 0), P(0, 16), S, text="20")
        dim(sp, P(L, 0), P(L, -3), P(L + 12, 0), S, angle=90, text="3", tside="R")
        dim(sp, P(L, -3), P(L, -13), P(L + 12, 0), S, angle=90, text="10")
        dim(sp, P(L, 0), P(L, -33), P(L + 24, 0), S, angle=90, text="≈ 30")
    note_cfg(xL=P(-L - 12, 0)[0])
    kl = P(-L - 12, 0)
    R = Lf = lambda tip, s_, **kw: leader(sp, P(*tip), kl, s_, S, "L", 36, **kw)
    if kind == "A":
        Lf((-1, -5), "POLYURETHANE SEALANT, 3 mm BELOW THE SURFACE, AS LATE AS POSSIBLE (≥ 28 DAYS)")
        Lf((-3, -11.5), "CLOSED-CELL BACKER ROD Ø8, PRESSED IN")
        R((-1.5, -30), "INITIAL CUT 3 mm × t/4; RESERVOIR 6 × 20 mm SAWN BEFORE SEALING")
    elif kind == "B":
        Lf((-1, -8), "SEMI-RIGID EPOXY OR POLYUREA FILLER, FULL DEPTH OF THE CUT, FLUSH; NO BACKER ROD; AS LATE AS "
                     "POSSIBLE (≥ 60 DAYS), LATER GAPS TOPPED UP")
        R((-1.5, -30), "INITIAL CUT 3 mm × t/4; RESERVOIR 6 × 20 mm")
    else:
        Lf((-5, -7), "POLYURETHANE SEALANT 20 × 10 mm, 3 mm BELOW THE SURFACE")
        Lf((-7, -23), "CLOSED-CELL BACKER ROD Ø25, PRESSED ONTO THE FILLER")
        R((-10, -50), "FILLER WITH A REMOVABLE CAP STRIP (≈ 30 mm), TAKEN OUT BEFORE SEALING")


# ----------------------------------------------------------------------- 1126/3: joint layout plan (1:25)
def sog_layout(ox, oy):
    """joint layout plan N.T.S.: joint marks (Beca catalogue), joints on column lines and mid-bay, <= 30 t apart,
    diamond isolation round each column, clear of the column corners (user 2026-09-30)"""
    S = 25
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    a = 2000                                            # bay drawn (N.T.S.)
    M = 550                                             # slab edge past the column centres
    Rd = COL + 150                                      # diamond half-diagonal: 150 / sqrt 2 clear of the corners
    h = COL / 2
    pline(sp, [P(-M, -M), P(a + M, -M), P(a + M, a + M), P(-M, a + M)], "S-CONC", close=True)
    for x in (0, a):
        for y in (0, a):
            pts = [P(x - h, y - h), P(x + h, y - h), P(x + h, y + h), P(x - h, y + h)]
            pline(sp, pts, "S-CONC", close=True)
            hatch(sp, pts, "ANSI31", pscale("ANSI31", S, 0.8))
            pline(sp, [P(x, y - Rd), P(x + Rd, y), P(x, y + Rd), P(x - Rd, y)], "S-JOINT", close=True)
    for v in (0, a):                                    # joints on the column lines stop at the diamond corners
        for q0, q1 in ((-M, -Rd), (Rd, a - Rd), (a + Rd, a + M)):
            line(sp, P(v, q0), P(v, q1), "S-JOINT")                        # CJ: ends of a pour strip
            line(sp, P(q0, v), P(q1, v), "S-CONC-HIDN")                    # SJ across the strips
    line(sp, P(-M, a / 2), P(a + M, a / 2), "S-CONC-HIDN")
    line(sp, P(a / 2, -M), P(a / 2, a + M), "S-CONC-HIDN")
    tag = lambda s, x, y, rot=0: text(sp, s, P(x, y), 2.0 * S, "S-TEXT", TA.BOTTOM_CENTER, rot=rot, style="ANB")
    tag("CJ", -40, a / 2 + 250, 90)
    tag("SJ", a / 2 - 40, a / 2 + 250, 90)
    tag("SJ", a * 0.3, a / 2 + 40)
    tag("IJ", Rd * 0.5 + 120, a + Rd * 0.5 + 60)
    note_cfg(xR=P(a + M + 250, 0)[0])
    kr = P(a + M + 250, 0)
    R = lambda tip, s_, **kw: leader(sp, P(*tip), kr, s_, S, "R", 40, **kw)
    R((a / 2, a * 0.3), f"SJ / SJD SAWN JOINTS ACROSS EACH POUR STRIP AT MID-BAY, ≤ 30 t APART ({TAB('SOG')})")
    R((a, a * 0.5), "CJ CONSTRUCTION JOINTS AT THE ENDS OF A POUR STRIP, ON THE COLUMN LINES")
    R((a + Rd / 2, a + Rd / 2), "IJ ISOLATION JOINT ROUND EACH COLUMN: DIAMOND ≥ 100 mm CLEAR OF THE COLUMN CORNERS, "
                                "JOINTS INTO ITS CORNERS; INFILL CAST AFTER THE COLUMN LOAD")
    R((a + M, a * 0.1), "IJ ALONG WALLS, GROUND BEAMS AND MACHINE BASES; EJ WHERE SHOWN")


# ======================================================================= tables and notes
SLAB_TABLE = [
    ["MIN. THICKNESS (NO DEFLECTION CHECK, SD40)", "ℓ/20 SIMPLE, ℓ/24 ONE END CONT., ℓ/28 BOTH CONT., ℓ/10 CANTILEVER; "
     "× (0.4 + fy/700) FOR OTHER STEEL", "EQ. 9-11 / 9-12 (αfm, β); ≥ 125 mm (αfm ≤ 2), ≥ 90 mm (αfm > 2); +10 % AT AN "
     "EDGE WITHOUT A STIFF BEAM", "ℓn/30 – ℓn/36 (EIT 011008 TABLE 9.3); ≥ 125 mm, ≥ 100 mm WITH DROP PANELS"],
    ["MAIN-BAR SPACING", "≤ 3h AND 450 mm", "≤ 2h AND 450 mm", "≤ 2h AND 450 mm"],
    ["MIN. STEEL (EACH WAY, ON b × h)", "0.0025 SR24 / 0.0020 SD30 / 0.0018 SD40", "SAME", "SAME"],
    ["DISTRIBUTION (S&T) BARS", "SAME RATIO, PERPENDICULAR TO THE MAIN BARS, ≤ 5h AND 400 mm", "–", "–"],
    ["TOP BARS AT SUPPORTS", "Sn/4 AT EDGES, Sn/3 AT INTERIOR SUPPORTS", "Sn/4, Sn/3 AND Ln/4, Ln/3",
     "FIG. 13.3.8: 0.30 / 0.20 ℓn COLUMN STRIP, 0.22 ℓn MIDDLE STRIP"],
    ["BOTTOM BARS", "FULL SPAN, ≥ 150 mm INTO SUPPORTS", "SAME; SHORT DIRECTION IN THE LOWER LAYER",
     "COLUMN STRIP CONTINUOUS; ≥ 2 EACH WAY THROUGH THE COLUMN CORE"],
    ["DISCONTINUOUS EDGE", "TOP BARS 90° HOOK INTO THE EDGE BEAM", "SAME + CORNER BARS L/5 × L/5",
     "TOP HOOKED, BOTTOM ≥ 150 mm; DEVELOP fy AT THE FACE"],
    ["REFERENCE", "EIT 011008 7.6, 7.12, 9.5.2, 10.5.4, 12.10; TATA 3", "EIT 011008 9.5.3, 13.3; TATA 3",
     "EIT 011008 9.5.3, 13.3.8; DPT 5.2.12"],
]


SLAB_NOTES = [
    ("1.", "THESE DETAILS APPLY WHERE THE SLAB DRAWINGS DO NOT SHOW OTHERWISE. SLAB MARKS: S = CAST IN PLACE, "
           "PS = PRECAST, GS = ON GROUND; ARROWS SHOW THE SPAN DIRECTION."),
    ("2.", f"COVER: 20 mm (≤ DB16) / 30 mm (≥ DB20) INTERIOR; 40 / 50 mm EXPOSED TO WEATHER; 75 mm CAST AGAINST EARTH ({TAB('COVER')})."),
    ("3.", f"LAPS PER {TAB('LAPS')}: TOP BARS LAPPED NEAR MIDSPAN, BOTTOM BARS OVER THE SUPPORTS. WELDED MESH LAP "
           "≥ ONE MESH SPACING + 25 mm AND ≥ 300 mm."),
    ("4.", "BOTTOM MAT ON MORTAR SPACERS; TOP MAT ON DB12 CHAIRS @ 1.0 – 1.5 m EACH WAY."),
    ("5.", "PIPES IN SLABS: OUTSIDE DIA. ≤ h/3, ≥ 3 DIA. APART, BETWEEN THE TOP AND BOTTOM MATS. [EIT 011008 6.3]"),
    ("6.", "A 90° TOP-BAR HOOK NEEDS ≈ 16 db BETWEEN THE COVERS; WHERE IT DOES NOT FIT, USE A 180° HOOK OR EDGE "
           "U-BARS. FREE SLAB EDGES: ≥ 2-DB12 TOP AND BOTTOM ALONG THE EDGE."),
    ("7.", f"BAR ENDS AND LAPS: SEE THE LEGEND (1121, 1124, 1125). FLAT SLABS 1122 – 1123 (BAR EXTENSIONS: EIT 011008 "
           f"FIG. 13.3.8 AND {TAB('SLAB')}); OPENINGS 1124; STEPS, EDGES AND CANTILEVERS 1125; SLAB ON GROUND 1126 – "
           f"1127; SLAB THICKNESS AND REINFORCEMENT: {TAB('SLAB')}; FILL UNDER SLABS ON GROUND: 1128."),
]


PUNCH_TABLE = [
    ["WHERE", "d ≥ 150 mm AND ≥ 16 × STIRRUP DIA.; CLOSED STIRRUPS ENGAGE THE FLEXURAL BARS", "ANY SLAB DEPTH"],
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
           "IN EACH DIRECTION, EXTENDED ≥ Ld PAST THE CORNERS, NOT LESS THAN " f"{TAB('TRIM')}. EXAMPLE: DB12 @ 150 mm, 800 mm OPENING: 5.3 BARS CUT = 6.0 cm² "
           "→ 2-DB16 (4.0 cm²) EACH SIDE."),
    ("3.", "PRECAST HOLLOW-CORE PLANKS: HOLES ≤ Ø150 mm (OR ≤ 150 mm WIDE) ONLY THROUGH A CORE, ≤ 3 IN ONE CROSS-SECTION; "
           "LARGER OPENINGS ON STEEL-ANGLE TRIMMERS SEATED ON THE ADJACENT PLANKS."),
    ("4.", "OPENINGS THROUGH BEAMS: 1113. PIPES EMBEDDED IN SLABS: 1121 NOTE 5."),
]


SOG_NOTES = [
    ("1.", f"SLAB ON GROUND (GS) ON A LEVELLED, COMPACTED SUBGRADE OR FILL ({TAB('FILL')}, 1128/1) WITH 50 – 100 mm "
           "COMPACTED SAND; SLAB THICKNESS 150 – 300 mm "
           "UNLESS SHOWN. COVER 75 mm WHERE CAST AGAINST EARTH (LEAN CONCRETE OR MEMBRANE BELOW: 40 mm)."),
    ("2.", "JOINTS ON PLAN BY MARK (1127): SJ SAWN, SJD SAWN WITH DOWELS, CJ CONSTRUCTION, EJ EXPANSION, IJ "
           f"ISOLATION. SJ SPACING ≤ 30 t ({TAB('SOG')}); PANELS AS SQUARE AS POSSIBLE (≤ 1.5 : 1); RE-ENTRANT CORNERS: "
           "2 DIAGONAL BARS."),
    ("3.", "POUR IN LONG STRIPS WITH CONTRACTION JOINTS SAWN ACROSS THEM (ACI 302.1R), NOT IN A CHECKERBOARD."),
    ("4.", "0.2 mm POLYETHYLENE SHEET UNDER THE SLAB, LAPS 150 mm TAPED, TURNED UP AT WALLS AND BEAMS; OR 50 mm LEAN "
           "CONCRETE WHERE SHOWN (DETAIL 4)."),
    ("5.", "DOWELS: PLAIN ROUND, STRAIGHT, NO BURRS, PARALLEL TO THE SURFACE AND THE JOINT DIRECTION WITHIN 3 mm IN 300 mm, "
           "ON BASKETS OR CHAIRS. t > 200 mm, RACKING OR HEAVY WHEEL LOADS: JOINTS AND DOWELS PER DESIGN."),
    ("6.", "SLABS UNDER BASEMENTS OR WATER PRESSURE, AND SLABS CARRYING RACKS OR MACHINES: PER DESIGN."),
]


def build():
    EXT.update({
        "SS": capture(short_section, 0, 0),
        "CP": capture(corner_panel, 0, -10000),
        "CS": capture(cant_slab, 24000, -10000),
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
        "G4": capture(sog_lean, 24000, -100000),
        "GF": capture(sog_fill, 32000, -100000),
        "GL": capture(sog_layout, 16000, -100000),
        "J1": capture(sog_joint, 0, -108000, "SJ"),
        "J2": capture(sog_joint, 8000, -108000, "CJ"),
        "J3": capture(sog_joint, 0, -116000, "CJE"),
        "J4": capture(sog_joint, 8000, -116000, "EJ"),
        "SA": capture(sog_seal, 0, -124000, "A"),
        "SB": capture(sog_seal, 2000, -124000, "B"),
        "SC": capture(sog_seal, 4000, -124000, "C"),
    })
    for f in (sheet_1121, sheet_1122, sheet_1123, sheet_1124, sheet_1125, sheet_1126, sheet_1127,
              sheet_1128):
        f()


# Sheet layout: the R2 column / beam style (user 2026-09-30: "our style better" than the Beca panel grid). Views
# top-aligned in rows from the top-left, each title under its own view, notes / tables / legend in the free space.
SLAB_KEY = ("END", "HOOK", "BREAK", "LAP", "NF")      # legend rows used on the slab sheets
V = lambda key, name, bubble, note=None, **kw: dict(key=key, name=name, bubble=bubble, note=note, **kw)


def place_row(ps, y_top, views, x0=FX0 + 1, gap=8.0):
    """views side by side from x0, tops at y_top, each title 6 under its view (note wrapped to the view width).
    Returns (y under the lowest title block, x right of the last view)."""
    x, low = x0, y_top
    for v in views:
        px, pw, ph = viewport(ps, v["key"], v.get("scale", SC), x, y_top)
        yt = y_top - ph - 6
        nw = max(pw - 2 * PAD, 70.0)
        view_title(ps, None, yt, v["name"], "N.T.S.", v["bubble"], v.get("triangles", False), note=v["note"],
                   note_w=nw)
        n = len(wrap_s(v["note"], 2.0, nw)) if v["note"] else 0
        low = min(low, yt - (6.2 + (n - 1) * LPN + 2.0 if n else 4.6))
        x = px + pw + gap
    return low, x


def side_blocks(ps, x, y, blocks):
    """notes / legend / tables stacked down from (x, y) to the title strip"""
    w = TBX - x - 3
    for b in blocks:
        if b[0] == "notes":
            y = notes_block(ps, x, y, w, b[1], b[2]) - 6
        elif b[0] == "key":
            y = bar_end_legend(ps, x, y, w, SLAB_KEY) - 6
        else:
            y = tbl(ps, x, y - 6, b[1], b[2], b[3], b[4], title=b[5]) - 8
    print(f"  side blocks bottom {y:.1f}")
    return y


# ======================================================================= sheet 1121
def sheet_1121():
    ps = new_sheet(0)
    top = FY1 - 3
    y, _ = place_row(ps, top, [V("SS", "SLAB ON BEAMS - SECTION ALONG THE SHORT SPAN", ("1", "1121"),
                                 "ONE-WAY AND TWO-WAY SLABS; UNIFORM LOAD, ADJACENT SPANS WITHIN 20 %; OTHERWISE "
                                 "PER DESIGN")])
    y -= 8
    _, x = place_row(ps, y, [V("CP", "TWO-WAY SLAB - CORNER PANEL", ("2", "1121"),
                               "PLAN; EDGE BEAMS LEFT AND BELOW; ONE BAR SHOWN PER BAND")])
    side_blocks(ps, x, y, [("notes", "TYPICAL SLAB NOTES", SLAB_NOTES), ("key",)])


# ======================================================================= sheet 1122
def sheet_1122():
    ps = new_sheet(1)
    top = FY1 - 3
    y, _ = place_row(ps, top, [V("FP", "FLAT SLAB - STRIPS AND COLUMN ZONE", ("1", "1122"),
                                 "PLAN OF AN INTERIOR PANEL")])
    place_row(ps, y - 8, [V("DC", "DROP PANEL AND COLUMN CAPITAL", ("2", "1122"),
                            "SECTION THROUGH AN INTERIOR COLUMN HEAD")])


# ======================================================================= sheet 1123
def sheet_1123():
    ps = new_sheet(2)
    y = FY1 - 3
    for k, (kp, ks, nm) in enumerate((("PSP", "PSS", "PUNCHING SHEAR - STIRRUPS"),
                                       ("PRP", "PRS", "PUNCHING SHEAR - HEADED STUD RAILS"))):
        y, _ = place_row(ps, y, [V(kp, nm, (str(1 + k), "1123"), f"PLAN AT AN INTERIOR COLUMN; RULES: {TAB('PUNCH')}"),
                                 V(ks, "SECTION", ("AB"[k], "1123"), triangles=True)])
        y -= 8
    yb = tbl(ps, FX0 + 3, y - 4, [44, 136, 136], ["ITEM", "STIRRUPS (BARS)", "HEADED STUD RAILS"], PUNCH_TABLE,
             "LCC", title=TABT("PUNCH"))
    print(f"  1123 bottom {yb:.1f}")


# ======================================================================= sheet 1124
TRIM_TABLE = [
    ["≤ 125 mm (ONE MAT)", "BARS RE-SPACED ROUND IT", "1-DB12 CENTRAL", "2-DB12 CENTRAL", "1-DB12 × 1200"],
    ["150 – 200", "BARS RE-SPACED ROUND IT", "1-DB12 T & B", "2-DB16 T & B", "2-DB12 × 1200 T & B"],
    ["225 – 300", "BARS RE-SPACED ROUND IT", "2-DB12 T & B", "2-DB20 T & B", "2-DB12 × 1200 T & B"],
]


def sheet_1124():
    ps = new_sheet(3)
    top = FY1 - 3
    y, _ = place_row(ps, top, [V("OS", "OPENING < 600 mm", ("1", "1124"), "SLAB ON BEAMS OR WALL"),
                               V("OL", "OPENING ≥ 600 mm", ("2", "1124"),
                                 "LARGER OPENINGS / NOT ON THE DRAWINGS: ENGINEER'S APPROVAL")])
    y -= 8
    _, x = place_row(ps, y, [V("OF", "OPENINGS IN FLAT SLABS", ("3", "1124"),
                               "PLAN OF A PANEL: PERMITTED OPENINGS WITHOUT ANALYSIS (EIT 011008 13.4, 11.11.6)")])
    side_blocks(ps, x, y, [("tbl", [22, 26, 22, 22, 36], ["SLAB t (mm)", "OPENING ≤ 300 mm", "300 – 600 mm, EACH SIDE",
                                                          "≥ 600 mm, EACH SIDE", "DIAGONAL, EACH CORNER (L mm)"],
                            TRIM_TABLE, "CCCCC", TABT("TRIM")),
                           ("notes", "NOTES TO 1124", OPENING_NOTES), ("key",)])


# ======================================================================= sheet 1125
def sheet_1125():
    ps = new_sheet(4)
    top = FY1 - 3
    y, _ = place_row(ps, top, [V("T1", "SLAB STEP, H < t", ("1", "1125")),
                               V("T2", "SLAB STEP, H > t", ("2", "1125"), "DEEPER THAN 2 t: A BEAM PER DESIGN")])
    y -= 8
    y2, x = place_row(ps, y, [V("CS", "CANTILEVER SLAB", ("5", "1125"), "BALCONIES AND CANOPIES; LOADS PER DESIGN")])
    side_blocks(ps, x, y, [("key",)])
    place_row(ps, y2 - 8, [V("E1", "UPSTAND ≤ 100 × 300 mm", ("3", "1125"),
                             "FIN OR CURB AT A SLAB EDGE, UNLESS SHOWN; DOWNSTAND MIRRORED"),
                           V("E2", "UPSTAND > 100 mm OR > 300 mm", ("4", "1125"), "HIGHER THAN 1000 mm: PER DESIGN")])


# ======================================================================= sheet 1126
# Subgrade, fill and backfill after DPT road-works standards (มยผ. 2101 - 2225 - 57, user 2026-09-30):
# 2101 embankment material, 2104 selected material, 2112 clearing, 2114 embankment construction, 2115 excavation,
# 2201 / 2202 standard / modified compaction, 2203 CBR, 2204 field density (sand cone). See REVIEW_BECA_SLAB.md.
FILL_TABLE = [
    ["SUBGRADE (EXISTING GROUND)", "TOPSOIL, ROOTS, ORGANIC, SOFT AND UNSTABLE MATERIAL REMOVED (DPT 2112, 2115); ROOTS "
     "≥ 300 mm BELOW THE UNDERSIDE OF THE WORK; HOLES REFILLED WITH FILL AND COMPACTED",
     "SURFACE WETTED EVENLY; THE TOP 150 mm OF THE EXISTING GROUND COMPACTED. ON A SLOPE OR CUT: THE TOP 200 mm "
     "LOOSENED FIRST FOR BOND (DPT 2114)",
     "≥ 95 % STANDARD PROCTOR (DPT 2201)", "1 PER 500 m², ≥ 3 PER AREA"],
    ["FILL: SOIL AGGREGATE / LATERITE (DEFAULT)", "DPT 2101 4.2: MAX. SIZE 50 mm; ≤ 35 % PASSING 0.075 mm; CBR ≥ 8 % AT "
     "95 % MODIFIED; SWELL ≤ 3 %; NO ROOTS OR ORGANIC MATTER",
     "LAYERS ≤ 200 mm THICK AFTER COMPACTION; MIXED AND WATERED TO EVEN MOISTURE; EACH LAYER TESTED BEFORE THE NEXT",
     "≥ 95 % MODIFIED PROCTOR (DPT 2202)", "1 PER 500 m² PER LAYER, ≥ 3"],
    ["FILL: SAND", "DPT 2101 4.3: NON-PLASTIC; MAX. SIZE 9.5 mm; ≤ 20 % PASSING 0.075 mm; CBR ≥ 10 % AT 95 % MODIFIED; "
     "NO CLAY LUMPS, TOPSOIL OR ORGANIC MATTER", "LAYERS ≤ 200 mm THICK AFTER COMPACTION; ON SOFT GROUND NO VIBRATORY COMPACTION "
     "(NOTE 3)", "≥ 95 % MODIFIED PROCTOR (DPT 2202)", "1 PER 500 m² PER LAYER, ≥ 3"],
    ["FILL: SOIL (ONLY WHERE APPROVED)", "DPT 2101 4.1: CBR ≥ 4 % AT 95 % STANDARD; SWELL ≤ 4 %; NO ROOTS OR ORGANIC "
     "MATTER", "LAYERS ≤ 200 mm THICK AFTER COMPACTION", "≥ 95 % STANDARD PROCTOR (DPT 2201)", "1 PER 500 m² PER LAYER, ≥ 3"],
    ["BACKFILL AGAINST GROUND BEAMS, WALLS, PITS", "AS THE FILL", "LAYERS ≤ 200 mm THICK AFTER COMPACTION, SMALL PLATE OR "
     "RAMMER (METHOD APPROVED); BOTH SIDES OF A WALL AT ONE LEVEL (DPT 2114 5.1.7)", "AS THE FILL",
     "1 PER 50 m RUN PER LAYER"],
    ["SAND BED UNDER THE SLAB", "SAND AS ABOVE (DPT 2101 4.3)", "50 – 100 mm THICK, MOISTENED, PLATE COMPACTOR",
     "≥ 95 % MODIFIED PROCTOR (DPT 2202)", "1 PER 500 m²"],
]
FILL_NOTES = [
    ("1.", "FILL UNDER SLABS: SOIL AGGREGATE OR SAND UNLESS SHOWN; SOIL FILL ONLY WHERE THE ENGINEER APPROVES. EACH "
           "SOURCE TESTED BEFORE USE: GRADING (DPT 2208), LL / PL (2205, 2206), CBR AND SWELL (2203), CLAY LUMPS "
           "(2211). SOFT CLAY, MUD AND HIGHLY ORGANIC SOIL ARE REMOVED, NEVER USED AS FILL (DPT 2115 4.3)."),
    ("2.", "PONDS, DITCHES, STANDING WATER: PUMP OUT AND REMOVE THE MUD; THE FIRST LAYER OF SOIL AGGREGATE OR SAND ≤ "
           "200 mm ABOVE THE WATER, ≥ 95 % MODIFIED PROCTOR (DPT 2114 5.2)."),
    ("3.", "SOFT GROUND (CBR < 2 %): SAND FILL; THE FIRST LAYER LEFT ≥ 45 DAYS BEFORE FINAL COMPACTION UNLESS SHOWN; LIGHT "
           "PLANT, NO VIBRATORY COMPACTION (DPT 2114 5.3). FILL DEEPER THAN 1.0 m OR OVER SOFT CLAY: SETTLEMENT PER THE "
           "GEOTECHNICAL REPORT; A PILE-SUPPORTED GROUND SLAB MAY BE REQUIRED."),
    ("4.", "FIELD DENSITY BY SAND CONE (DPT 2204); EACH LAYER ACCEPTED BEFORE THE NEXT, THE LAST BEFORE THE SAND BED. "
           "DPT 2201 / 2202 ≈ ASTM D698 / D1557."),
    ("5.", "FINISHED FORMATION: WITHIN 10 mm UNDER A 3 m STRAIGHTEDGE; NOT MORE THAN 15 mm BELOW AND NEVER ABOVE THE DESIGN "
           "LEVEL (DPT 2114 6)."),
]


SOG_TABLE = [
    ["150", "4.5 m", "3 × 40", "RB19 × 400", "300"],
    ["175", "5.0 m", "3 × 45", "RB25 × 450", "300"],
    ["200", "6.0 m", "3 × 50", "RB25 × 450", "300"],
]


def sheet_1126():
    ps = new_sheet(5)
    top = FY1 - 3
    y, _ = place_row(ps, top, [V("G1", "SLAB AT A GROUND BEAM", ("1", "1126"),
                                 "ALSO AT WALLS, PILE CAPS AND MACHINE BASES", scale=SG),
                               V("G2", "THICKENED FREE EDGE", ("2", "1126"), "EDGE WITHOUT A GROUND BEAM", scale=SG)])
    y -= 8
    _, x = place_row(ps, y, [V("GL", "JOINT LAYOUT", ("3", "1126"),
                               "PLAN, ONE BAY; JOINT MARKS SJ / SJD / CJ / EJ / IJ: 1127")])
    yb = side_blocks(ps, x, y, [("tbl", [18, 26, 24, 26, 18], ["SLAB t (mm)", "SJ SPACING ≤ 30 t", "SAW CUT W × D (mm)",
                                                               "PLAIN DOWEL Ø × L (mm)", "DOWELS @ (mm)"],
                                 SOG_TABLE, "CCCCC", TABT("SOG")),
                                ("notes", "SLAB-ON-GROUND NOTES", SOG_NOTES)])
    place_row(ps, yb, [V("G4", "SLAB ON LEAN CONCRETE", ("4", "1126"),
                         None, scale=SG)], x0=x)     # no title note: the leader says "INSTEAD OF THE SHEET"


# ======================================================================= sheet 1127
def sheet_1127():
    ps = new_sheet(6)
    y = FY1 - 3
    for row in ((("J1", "SAWN JOINT (SJ, SJD)", "1", "SJD: DOWELLED, WHERE MARKED ON PLAN"),
                 ("J2", "CONSTRUCTION JOINT (CJ)", "2", "END OF A POUR STRIP, ON A PLANNED JOINT LINE")),
                (("J3", "CONSTRUCTION JOINT AT AN EXISTING SLAB (CJ)", "3", "EXTENSIONS AND INFILL STRIPS"),
                 ("J4", "EXPANSION JOINT (EJ)", "4", "ISOLATION JOINT (IJ): THE SAME WITHOUT DOWELS"))):
        y, _ = place_row(ps, y, [V(k, nm, (n, "1127"), note, scale=SG) for k, nm, n, note in row])
        y -= 8
    place_row(ps, y, [V("SA", "DETAIL A - SEALED JOINT", ("A", "1127"), "FOOT AND PNEUMATIC-TYRE TRAFFIC", scale=2),
                      V("SB", "DETAIL B - FILLED JOINT", ("B", "1127"), "HARD-WHEELED TRAFFIC", scale=2),
                      V("SC", "DETAIL C - EXPANSION JOINT SEAL", ("C", "1127"), "EJ AND IJ", scale=2)])


# ======================================================================= sheet 1128 (tables and notes)
def sheet_1128():
    ps = new_sheet(7)
    top = FY1 - 3
    yb = tbl(ps, FX0 + 3, top - 8, [40, 90, 90, 96], ["ITEM", "ONE-WAY SLAB", "TWO-WAY SLAB ON BEAMS",
             "FLAT SLAB / FLAT PLATE"], SLAB_TABLE, "LCCC", title=TABT("SLAB"))
    y2, x = place_row(ps, yb - 8, [V("GF", "SLAB ON COMPACTED FILL", ("1", "1128"),
                                     "WHERE THE FLOOR IS RAISED ABOVE THE STRIPPED GROUND", scale=SG)])
    yn = side_blocks(ps, x, yb - 8, [("notes", f"NOTES TO {TAB('FILL')}", FILL_NOTES)])
    yf = tbl(ps, FX0 + 3, min(y2, yn) - 14, [34, 86, 78, 64, 52], ["LAYER", "MATERIAL", "PLACING", "COMPACTION",
             "FIELD DENSITY TESTS"], FILL_TABLE, "LLLLL", title=TABT("FILL"))
    print(f"  1128 bottom {yf:.1f}")
