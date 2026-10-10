"""
Project SPF - plans and elevations (1:200 / 1:100) from the MIDAS model geometry (calc_spf) and the calc.

Plan convention: plan x = model Y (along the building, grids 1 - 10), plan y = model X (across the span, grid A at
y = 0, grid B at y = 26 000). Wall elevations: side walls looking at the outside face, gable looking at grid 1 from
outside (model X to the right).
"""
import math

from spf_engine import *          # noqa: F401,F403
import spf_engine as SE
import calc_spf as C

F = SE.Frame
BP1, BP2 = D["BP1"], D["BP2"]
PU, PU2, GT, GT2, SR = D["PU1"], D["PU2"], D["GT1"], D["GT2"], D["SR1"]
PURL_X = D["purlin_layout"]["main"]
YS = C.FRAMES_Y
POSTS = C.GABLE_POSTS
LONG = YS[-1]


def plan_grids(sp, P, S, x_ext=(-4_500.0, LONG + 4_500.0), y_ext=(-CAN_A - 2_500, SPAN + CAN_B + 2_500)):
    """numbered grids 1 - 10 (bubbles at both ends) and lettered A, B (bubbles left and right)"""
    for y_, lab in zip(YS, GRID_NUM):
        gridline(sp, P, (y_, y_ext[0]), (y_, y_ext[1]), lab, S, at="a")
        c = (y_, y_ext[1] + 3.5 * S + 2 * S)
        sp.add_circle(P(*c), 3.5 * S, dxfattribs=A("S-SYMB"))
        text(sp, lab, P(*c), 2.8 * S, "S-TEXT", TA.MIDDLE_CENTER, style="ANB")
    for x_, lab in ((0.0, "A"), (SPAN, "B")):
        gridline(sp, P, (x_ext[0], x_), (x_ext[1], x_), lab, S, at="a")
        c = (x_ext[1] + 3.5 * S + 2 * S, x_)
        sp.add_circle(P(*c), 3.5 * S, dxfattribs=A("S-SYMB"))
        text(sp, lab, P(*c), 2.8 * S, "S-TEXT", TA.MIDDLE_CENTER, style="ANB")


def gdim(sp, p1, p2, base, S, angle=0):
    """grid chain dimension: dot terminators (EIT 8.2, FP7)"""
    d = sp.add_linear_dim(base=base, p1=p1, p2=p2, angle=angle, dimstyle=DS[f"G{S}"], dxfattribs=A("S-DIMS"))
    d.render()
    return d


def grid_dims(sp, P, S, y_dim, x_dim, posts=True):
    """bay chain and overall along the building (under the plan, clear above the grid bubbles), span chain left;
    the gable post chain nearest the plan"""
    for a, b in zip(YS[:-1], YS[1:]):
        gdim(sp, P(a, 0), P(b, 0), P(0, y_dim), S)
    gdim(sp, P(YS[0], 0), P(YS[-1], 0), P(0, y_dim - 9 * S), S)
    gdim(sp, P(0, 0), P(0, SPAN), P(x_dim - 9 * S if posts else x_dim, 0), S, angle=90)
    if posts:
        pts = [0.0] + list(POSTS) + [SPAN]
        for a, b in zip(pts[:-1], pts[1:]):
            dim(sp, P(0, a), P(0, b), P(x_dim, 0), S, angle=90)


# --------------------------------------------------------------------------- 1/1001: anchor bolt and column plan
def anchor_plan(ox, oy):
    S = 200
    sp = msp
    note_cfg(free=True)
    P = lambda x, y: (ox + x, oy + y)                                            # noqa: E731
    plan_grids(sp, P, S, y_ext=(-5_400.0, SPAN + 2_500.0))
    c0 = T["C"]
    for y_ in YS:
        for x_ in (0.0, SPAN):                                              # frame columns: BP1
            hsec(sp, P, (y_, x_), c0["d0"], c0["bf"], c0["tw"], c0["tf"], rot=90, layer="S-STL", fill=True)
            plate_rect(sp, P, (y_, x_), BP1["W"], BP1["B"], layer="S-STL-VIS")
    for y_ in (YS[0], YS[-1]):
        for x_ in POSTS:                                                     # gable posts: BP2 (web along Y)
            g = C.GPOST
            hsec(sp, P, (y_, x_), g.d, g.bf, g.tw, g.tf, rot=-90, layer="S-STL", fill=True)
            plate_rect(sp, P, (y_, x_), BP2["B"], BP2["W"], layer="S-STL-VIS")
    for (y_, x_, s) in ((YS[1] + 900, 800, "BP1"), (YS[0] + 900, POSTS[1] + 700, "BP2")):     # beside a base
        mtag(sp, P, (y_, x_), s, S)
    grid_dims(sp, P, S, -1_500, -1_200)
    text(sp, f"BP1: FRAME COLUMNS, 20 No.   BP2: GABLE POSTS, 10 No.   PEDESTALS BY THE RC DESIGNER",
         P(LONG / 2, SPAN + 6_500), 2.0 * S, align=TA.MIDDLE_CENTER)


def base_plan(ox, oy, key):
    """plan of one base plate at 1:10: plate, column, rods, set-out from the grid lines"""
    S = 10
    sp = msp
    b = D[key]
    P = lambda x, y: (ox + x, oy + y)                                            # noqa: E731
    if key == "BP1":
        c0 = T["C"]
        d, bf, tw, tf, rot = c0["d0"], c0["bf"], c0["tw"], c0["tf"], 0.0     # column depth along plan y (X)
        W, H_ = b["W"], b["B"]                                              # plate: W along x (Y), B along y (X)
        rods = [(sx * b["sy"] / 2, sy * b["sx"] / 2) for sx in (-1, 1) for sy in (-1, 1)]
    else:
        g = C.GPOST
        d, bf, tw, tf, rot = g.d, g.bf, g.tw, g.tf, 90.0
        W, H_ = b["B"], b["W"]
        rods = [(sx * b["sx"] / 2, sy * b["sy"] / 2) for sx in (-1, 1) for sy in (-1, 1)]
    plate_rect(sp, P, (0, 0), W, H_)
    hsec(sp, P, (0, 0), d, bf, tw, tf, rot=rot, layer="S-STL")
    for x, y in rods:
        sp.add_circle(P(x, y), b["db"] / 2, dxfattribs=A("S-BOLT"))
        sp.add_circle(P(x, y), b["hole"] / 2, dxfattribs=A("S-STL-HIDN"))
        wb = b["washer"]["b"]
        plate_rect(sp, P, (x, y), wb, wb, layer="S-STL-VIS")
        line(sp, P(x - wb / 2 - 30, y), P(x + wb / 2 + 30, y), "S-CENT")
        line(sp, P(x, y - wb / 2 - 30), P(x, y + wb / 2 + 30), "S-CENT")
    line(sp, P(-W / 2 - 50, 0), P(W / 2 + 50, 0), "S-GRID")
    line(sp, P(0, -H_ / 2 - 50), P(0, H_ / 2 + 50), "S-GRID")
    xs = sorted({x for x, _ in rods})
    ys = sorted({y for _, y in rods})
    dim(sp, P(-W / 2, -H_ / 2), P(xs[0], -H_ / 2), P(0, -H_ / 2 - 80), S)
    dim(sp, P(xs[0], -H_ / 2), P(xs[1], -H_ / 2), P(0, -H_ / 2 - 80), S)
    dim(sp, P(xs[1], -H_ / 2), P(W / 2, -H_ / 2), P(0, -H_ / 2 - 80), S)
    dim(sp, P(-W / 2, -H_ / 2), P(W / 2, -H_ / 2), P(0, -H_ / 2 - 160), S)
    dim(sp, P(W / 2, -H_ / 2), P(W / 2, ys[0]), P(W / 2 + 80, 0), S, angle=90)
    dim(sp, P(W / 2, ys[0]), P(W / 2, ys[1]), P(W / 2 + 80, 0), S, angle=90)
    dim(sp, P(W / 2, ys[1]), P(W / 2, H_ / 2), P(W / 2 + 80, 0), S, angle=90)
    dim(sp, P(W / 2, -H_ / 2), P(W / 2, H_ / 2), P(W / 2 + 160, 0), S, angle=90)
    note_cfg(xL=P(-W / 2 - 300, 0)[0])
    leader(sp, P(xs[0], ys[1]), (0, 0), f"{b['rods']}-M{b['db']} ANCHOR RODS, HOLES Ø{b['hole']}, PLATE WASHERS "
           f"{b['washer']['b']:.0f} x {b['washer']['b']:.0f} x {b['washer']['t']:.0f} (HOLE Ø{b['washer']['hole']:.0f})"
           f", SITE WELDED", S, side="L", width=48, bolt=b["hole"])
    leader(sp, P(-W / 2, ys[0] - 40), (0, 0), f"BASE PL {b['tp']} x {W:.0f} x {H_:.0f} SM400B", S, side="L",
           width=48)


# --------------------------------------------------------------------------- 1/1002: roof framing plan
BRACED = ((0.0, 10_000.0), (80_000.0, 90_000.0))                   # roof bracing bays (model Y)
BR_X = (0.0, 4_500.0, 8_500.0, RIDGE, 17_500.0, 21_500.0, SPAN)    # bracing nodes across the span (model X)


def roof_plan(ox, oy):
    """roof framing plan, 1:200 (steel S4.11, FP9.2): every member a double line at its projected width - rafters
    (haunch 250, rafter / canopy / gable 200), purlins H 175 x 90 (90), struts CHS 165.2 / 190.7, braces L 90 x 90
    (90; one brace of each X over the other); the purlins lie over the rafters, struts and braces, so those are left
    out where covered; sag rods one line each on the rod linetype; member marks named on the member, the lines cut
    at the circle"""
    from shapely.geometry import LineString, Point, box
    from shapely.ops import unary_union
    S = 200
    sp = msp
    note_cfg(free=True)
    P = lambda x, y: (ox + x, oy + y)                                            # noqa: E731
    plan_grids(sp, P, S, y_ext=(-CAN_A - 5_600.0, SPAN + CAN_B + 2_500.0))

    def strip(a, b, w):
        return LineString([a, b]).buffer(w / 2, cap_style=2, join_style=2)

    purl = PURL_X + [SPAN - x for x in PURL_X]
    can = [-CAN_A + 300 + i * 1_100 for i in range(int((CAN_A - 600) // 1_100) + 1)]
    can += [SPAN + CAN_B - 300 - i * 1_100 for i in range(int((CAN_B - 600) // 1_100) + 1)]
    pur = unary_union([strip((0, x_), (LONG, x_), PU["sec"].bf) for x_ in purl + can])
    raf = []
    for k, y_ in enumerate(YS):
        if k in (0, len(YS) - 1):
            raf.append(strip((y_, -CAN_A), (y_, SPAN + CAN_B), C.GRAF.bf))
            continue
        h = T["H"]["bf"]
        for xa, xb, w in ((-CAN_A, 0.0, CAN.bf), (0.0, C.X_SPLICE, h), (C.X_SPLICE, SPAN - C.X_SPLICE, RAF.bf),
                          (SPAN - C.X_SPLICE, SPAN, h), (SPAN, SPAN + CAN_B, CAN.bf)):
            raf.append(strip((y_, xa), (y_, xb), w))
    raf = unary_union(raf)
    st2 = unary_union([strip((0, x_ + 250), (LONG, x_ + 250), C.STRUT.D) for x_ in (0.0, RIDGE, SPAN)])
    st1 = unary_union([strip((y0, x_), (y1, x_), C.BRACE.D) for y0, y1 in BRACED
                       for x_ in (4_500.0, 8_500.0, 17_500.0, 21_500.0)])
    br_top, br_bot = [], []
    for y0, y1 in BRACED:
        for xa, xb in zip(BR_X[:-1], BR_X[1:]):
            br_top.append(strip((y0, xa), (y1, xb), C.BRACE_L.b))
            br_bot.append(strip((y0, xb), (y1, xa), C.BRACE_L.b))
    br_top, br_bot = unary_union(br_top), unary_union(br_bot)
    rods = []
    for y0, y1 in zip(YS[:-1], YS[1:]):
        for yy in (y0 + BAY / 3, y0 + 2 * BAY / 3):
            rods.append(LineString([(yy, PURL_X[0]), (yy, PURL_X[-1])]))
            rods.append(LineString([(yy, SPAN - PURL_X[-1]), (yy, SPAN - PURL_X[0])]))
    # member marks on their members (office: a member with a clear band is named on itself); lines cut at the circle
    bay = BAY
    tags = [((bay * 4.5, purl[3]), "PU1"), ((bay * 3.5, can[1]), "PU2"), ((bay * 0.25, None), "BR1"),
            ((bay * 0.72, 4_500.0), "ST1"), ((bay * 2.5, 250.0), "ST2"), ((YS[4], RIDGE - 1_300), "MR1"),
            ((bay * 5 + BAY / 3, (PURL_X[1] + PURL_X[2]) / 2), "SR1"), ((YS[2], 2_600.0), "R1"),
            ((YS[2], 9_000.0), "R2")]
    a0, b0 = BR_X[0], BR_X[1]
    tags[2] = ((bay * 0.25, a0 + (b0 - a0) * 0.25), "BR1")                    # a quarter along the first brace
    holes = unary_union([Point(*c).buffer((tag_r(s) + 0.6) * S) for c, s in tags])
    under_pur = lambda g: g.difference(pur)                                  # noqa: E731
    lay = [(raf, "S-STL", True), (st2, "S-STL-VIS", True), (st1, "S-STL-VIS", True),
           (br_bot.difference(br_top), "S-STL-VIS", True), (br_top, "S-STL-VIS", True), (pur, "S-STL-VIS", False)]
    for g, layer, covered in lay:
        edge = g.boundary
        if covered:
            edge = edge.difference(pur.buffer(1.0))
        draw_geom(sp, P, edge.difference(holes), layer)
    for r_ in rods:
        draw_geom(sp, P, r_.difference(holes), "S-ROD")
    for x_ in (10_750.0, SPAN - 10_750.0):                                   # monitor roof edges above
        draw_geom(sp, P, LineString([(0, x_), (LONG, x_)]).difference(holes), "S-STL-HIDN")
    for c, s in tags:
        mtag(sp, P, c, s, S)
    grid_dims(sp, P, S, -CAN_A - 1_400, -2_200, posts=False)
    pts = [-CAN_A, 0.0, RIDGE, SPAN, SPAN + CAN_B]
    for a, b in zip(pts[:-1], pts[1:]):
        dim(sp, P(LONG, a), P(LONG, b), P(LONG + 2_600, 0), S, angle=90)


def draw_geom(sp, P, g, layer):
    """shapely lines -> polylines (model coordinates of the view)"""
    if g.is_empty:
        return
    for part in getattr(g, "geoms", [g]):
        if part.geom_type == "LineString" and part.length > 1.0:
            pline(sp, [P(*q) for q in part.coords], layer)
        elif hasattr(part, "geoms"):
            draw_geom(sp, P, part, layer)


# --------------------------------------------------------------------------- 2001: elevations
def side_elev(ox, oy):
    """side wall, grid A, looking at the outside face: plan x = model Y"""
    S = 200
    sp = msp
    note_cfg(free=True)
    P = lambda x, z: (ox + x, oy + z)                                            # noqa: E731
    for y_, lab in zip(YS, GRID_NUM):
        gridline(sp, P, (y_, -3_400), (y_, F.zt(0) + 1_200), lab, S, at="a")
        w = col_d(EAVE)
        line(sp, P(y_ - T["C"]["bf"] / 2, 0), P(y_ - T["C"]["bf"] / 2, EAVE), "S-STL")
        line(sp, P(y_ + T["C"]["bf"] / 2, 0), P(y_ + T["C"]["bf"] / 2, EAVE), "S-STL")
        cs = D["CS1"]                                                       # column splice CS1 (plates edge-on)
        plate(sp, P, [(y_ - cs["bp"] / 2, cs["z"] - cs["tp"]), (y_ + cs["bp"] / 2, cs["z"] - cs["tp"]),
                      (y_ + cs["bp"] / 2, cs["z"] + cs["tp"]), (y_ - cs["bp"] / 2, cs["z"] + cs["tp"])])
    for z in D["girt_z"]:
        line(sp, P(0, z), P(LONG, z), "S-STL-VIS")
    line(sp, P(0, EAVE), P(LONG, EAVE), "S-PROP")                          # eave strut ST2
    for y0, y1 in BRACED:
        for zz in (EAVE - C.EAVEB.d / 2, EAVE + C.EAVEB.d / 2):              # eave beams EB1 in the end bays
            line(sp, P(y0, zz), P(y1, zz), "S-STL")
    line(sp, P(-CAN_A * 0, F.zt(0)), P(LONG, F.zt(0)), "S-STL-VIS")       # roof line / canopy root above
    for y0, y1 in zip(YS[:-1], YS[1:]):                                     # girt sag rods at third points
        for yy in (y0 + BAY / 3, y0 + 2 * BAY / 3):
            line(sp, P(yy, D["girt_z"][0]), P(yy, EAVE), "S-ROD")
    for a, b in zip(YS[:-1], YS[1:]):
        gdim(sp, P(a, 0), P(b, 0), P(0, -1_200), S)
    zs = [0.0] + D["girt_z"] + [EAVE]
    for a, b in zip(zs[:-1], zs[1:]):
        dim(sp, P(LONG, a), P(LONG, b), P(LONG + 2_500, 0), S, angle=90)
    level(sp, ox + LONG + 4_500, oy + 0, fmt_level(0), "", S, ext=(-6, 12))
    level(sp, ox + LONG + 4_500, oy + EAVE, fmt_level(EAVE), "", S, ext=(-6, 12))
    for (y_, z, s) in ((BAY * 4.5, D["girt_z"][1] + 700, "GT1"), (BAY * 0.5, EAVE + 1_000, "EB1"),
                       (BAY * 4.5, EAVE + 1_000, "ST2"), (BAY * 2 - 1_400, 3_000, "C1")):
        mtag(sp, P, (y_, z), s, S)


def gable_elev(ox, oy):
    """gable, grid 1, looking from outside: model X to the right (grid A left)"""
    S = 100
    sp = msp
    note_cfg(free=True)
    P = lambda x, z: (ox + x, oy + z)                                            # noqa: E731
    g = GRAF = C.GRAF
    zt = F.zt
    top = zt                                   # every rafter top flange in the roof plane (purlins level)
    for x_, lab in ((0.0, "A"), (SPAN, "B")):
        gridline(sp, P, (x_, -3_300), (x_, top(x_) + 1_800), lab, S, at="a")
    # gable rafter (continuous, canopy to canopy, splices GS1 / GS2)
    for xa, xb in ((-CAN_A, RIDGE), (RIDGE, SPAN + CAN_B)):
        line(sp, P(xa, top(xa)), P(xb, top(xb)), "S-STL")
        line(sp, P(xa, top(xa) - g.d / COS), P(xb, top(xb) - g.d / COS), "S-STL")
    for xs in (6_500.0, RIDGE, SPAN - 6_500.0):
        line(sp, P(xs, top(xs) + 100), P(xs, top(xs) - g.d / COS - 100), "S-STL")
    # corner columns (tapered, in the gable plane), posts (H 400 x 150, flange seen), eave ties, girts
    for x_ in (0.0, SPAN):
        sgn = 1 if x_ == 0 else -1
        zc = top(x_) - g.d / COS
        line(sp, P(x_ - sgn * col_d(0) / 2, 0), P(x_ - sgn * col_d(zc) / 2, zc), "S-STL")
        line(sp, P(x_ + sgn * col_d(0) / 2, 0), P(x_ + sgn * col_d(zc) / 2, zc), "S-STL")
    for x_ in POSTS:
        zc = top(x_) - g.d / COS
        bf = C.GPOST.bf
        line(sp, P(x_ - bf / 2, 0), P(x_ - bf / 2, zc), "S-STL")
        line(sp, P(x_ + bf / 2, 0), P(x_ + bf / 2, zc), "S-STL")
    for xa, xb in zip((col_d(EAVE) / 2,) + POSTS, POSTS + (SPAN - col_d(EAVE) / 2,)):
        zz = EAVE
        if xa >= POSTS[0] - 1 and xb <= POSTS[-1] + 1:
            line(sp, P(xa + 75, zz - 100), P(xb - 75, zz - 100), "S-STL")       # eave tie ET1 (H 200 x 100)
            line(sp, P(xa + 75, zz + 100), P(xb - 75, zz + 100), "S-STL")
        for z in D["girt_z"]:
            line(sp, P(xa + 125, z), P(xb - 125, z), "S-STL-VIS")
    # monitor end frame (posts and rafters)
    for x_ in C.MON_X:
        line(sp, P(x_, zt(x_)), P(x_, 10_950), "S-STL-VIS")
    line(sp, P(10_750, 10_544), P(RIDGE, 11_275), "S-STL-VIS")
    line(sp, P(RIDGE, 11_275), P(SPAN - 10_750, 10_544), "S-STL-VIS")
    # dims and levels
    pts = [0.0] + list(POSTS) + [SPAN]
    for a, b in zip(pts[:-1], pts[1:]):
        dim(sp, P(a, 0), P(b, 0), P(0, -800), S)
    dim(sp, P(-CAN_A, 0), P(0, 0), P(0, -1_700), S)
    gdim(sp, P(0, 0), P(SPAN, 0), P(0, -1_700), S)
    dim(sp, P(SPAN, 0), P(SPAN + CAN_B, 0), P(0, -1_700), S)
    level(sp, ox - CAN_A - 300, oy + 0, fmt_level(0), "", S, ext=(-6, 14))
    level(sp, ox - CAN_A - 300, oy + EAVE, fmt_level(EAVE), "", S, ext=(-6, 14))
    for (x_, z, s) in ((POSTS[0] - 700, 2_200, "GP1"), (POSTS[1] - 700, 2_200, "GP2"), (POSTS[2] - 700, 2_200, "GP3"),
                       (2_600, F.zt(2_600) + 900, "GR1"), (9_600, F.zt(9_600) + 900, "GR2"),
                       ((POSTS[0] + POSTS[1]) / 2, EAVE + 500, "ET1"), (2_300, D["girt_z"][1] + 400, "GT2"),
                       (-500, 2_200, "C2")):
        mtag(sp, P, (x_, z), s, S)
    # detail callouts: vertical leaders from the top of each circle to notes above the roof, clear of the members
    for c, n_, sh, what, ky, side in (((0, EAVE), "2", "5002", "GABLE CORNER GK1", 11_600, "L"),
                                      ((6_500, F.zt(6_500)), "3", "5002", "GABLE RAFTER SPLICE GS1", 12_400, "L"),
                                      ((POSTS[1], F.zt(POSTS[1]) - 300), "4", "5002", "POST TOP / GS2 SIMILAR",
                                       13_200, "R")):
        tip = detail_callout(sp, P, c, 600, S, at=90)
        leader(sp, P(*tip), P(tip[0], ky), f"DETAIL {n_}/{sh} - {what}", S, side=side, width=58)
