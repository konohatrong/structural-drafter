"""
Project SPF - details for 5002 (bases, gable frame, eave beam) and 5003 (bracing, purlins, girts, fly braces),
1:10 / 1:20, from the calc (spf_engine.D).
"""
import math

from spf_engine import *          # noqa: F401,F403
import spf_engine as SE
import calc_spf as C
from spf_details import bolt_h, face_view, splice_rows

F = SE.Frame
BP1, BP2, GK, GS1, GS2, EB = D["BP1"], D["BP2"], D["GK1"], D["GS1"], D["GS2"], D["EB1"]
BR, ST1, ST2, GU = D["BR1"], D["ST1"], D["ST2"], D["GU1"]
PU, GT, SR, FB1, FB2 = D["PU1"], D["GT1"], D["SR1"], D["FB1"], D["FB2"]
GR = C.GRAF


# --------------------------------------------------------------------------- 1/5002 and 5/5002: base elevations
def base_elev(ox, oy, key):
    """elevation of a pinned base: member bottom (broken), base plate, grout, pedestal top, two rods seen"""
    S = 10
    sp = msp
    b = D[key]
    P = lambda x, z: (ox + x, oy + z)                                            # noqa: E731
    if key == "BP1":
        w0, w1, L, xr = T["C"]["d0"], col_d(700), b["B"], b["sx"] / 2           # column depth seen (frame plane)
        tf = T["C"]["tf"]
    else:
        w0 = w1 = C.GPOST.d
        L, xr, tf = b["B"], b["sx"] / 2, C.GPOST.tf
    zt = 700.0
    for sg in (-1, 1):                                                   # member flanges (seen), broken at zt
        line(sp, P(sg * w0 / 2, 0), P(sg * w1 / 2, zt), "S-STL")
        line(sp, P(sg * (w0 / 2 - tf), 0), P(sg * (w1 / 2 - tf), zt), "S-STL-VIS")
    zbreak(sp, P(-w1 / 2 - 60, zt), P(w1 / 2 + 60, zt), S)
    tp, g_ = b["tp"], b["grout"]
    plate(sp, P, [(-L / 2, 0), (L / 2, 0), (L / 2, -tp), (-L / 2, -tp)])
    hatch(sp, [P(-L / 2 - 60, -tp), P(L / 2 + 60, -tp), P(L / 2 + 60, -tp - g_), P(-L / 2 - 60, -tp - g_)],
          "AR-SAND", pscale("AR-SAND", S, 1.0), layer="S-HATCH")
    pline(sp, [P(-L / 2 - 60, -tp), P(-L / 2 - 60, -tp - g_)], "S-STL-VIS")
    pline(sp, [P(L / 2 + 60, -tp), P(L / 2 + 60, -tp - g_)], "S-STL-VIS")
    ztoc = -tp - g_
    line(sp, P(-L / 2 - 250, ztoc), P(L / 2 + 250, ztoc), "S-CONC")
    hatch(sp, [P(-L / 2 - 250, ztoc), P(L / 2 + 250, ztoc), P(L / 2 + 250, ztoc - 300), P(-L / 2 - 250, ztoc - 300)],
          "AR-CONC", pscale("AR-CONC", S, 1.0), layer="S-HATCH")
    zbreak(sp, P(-L / 2 - 250, ztoc - 300), P(L / 2 + 250, ztoc - 300), S)
    d = b["db"]
    wt = b["washer"]["t"]
    nh = 0.85 * d
    proj = ceil5_(g_ + tp + wt + 2 * nh + 3 * 3)
    for sg in (-1, 1):
        x = sg * xr
        line(sp, P(x - d / 2, ztoc - 300), P(x - d / 2, ztoc + proj), "S-BOLT")
        line(sp, P(x + d / 2, ztoc - 300), P(x + d / 2, ztoc + proj), "S-BOLT")
        line(sp, P(x, ztoc - 330), P(x, ztoc + proj + 30), "S-CENT")
        wb = b["washer"]["b"]
        plate(sp, P, [(x - wb / 2, 0), (x + wb / 2, 0), (x + wb / 2, wt), (x - wb / 2, wt)], layer="S-STL-VIS")
        for z0 in (wt, wt + nh):
            plate(sp, P, [(x - 0.85 * d, z0), (x + 0.85 * d, z0), (x + 0.85 * d, z0 + nh), (x - 0.85 * d, z0 + nh)],
                  layer="S-BOLT")
        plate(sp, P, [(x - 0.85 * d, -tp - nh), (x + 0.85 * d, -tp - nh), (x + 0.85 * d, -tp), (x - 0.85 * d, -tp)],
              layer="S-BOLT")                                                  # levelling nut
    line(sp, P(0, -tp - 50), P(0, zt + 60), "S-GRID")
    note_cfg(xR=P(L / 2 + 330, 0)[0])
    leader(sp, P(L / 2, -tp / 2), (0, 0), f"BASE PL {tp} x {L:.0f} x {b['W']:.0f} SM400B (PLAN: 1001)", S,
           side="R", width=40)
    leader(sp, P(xr + 0.85 * d, wt + nh), (0, 0),
           f"M{d} ROD, 2 NUTS, PLATE WASHER {b['washer']['b']:.0f} x {b['washer']['b']:.0f} x {wt:.0f} SITE-WELDED",
           S, side="R", width=40)
    leader(sp, P(xr + 0.85 * d, -tp - nh / 2), (0, 0), "LEVELLING NUT", S, side="R", width=40)
    leader(sp, P(L / 2 + 30, -tp - g_ / 2), (0, 0), f"NON-SHRINK GROUT {g_:.0f} mm", S, side="R", width=40)
    leader(sp, P(L / 2 + 150, ztoc - 120), (0, 0), "PEDESTAL BY THE RC DESIGNER", S, side="R", width=40)
    weld(sp, P(-w0 / 2, 120), (P(-w0 / 2, 0)[0] - 8 * S, P(0, 430)[1]), S, b["weld"], all_round=True, left=True)
    dim(sp, P(-xr - 2 * d, ztoc), P(-xr - 2 * d, ztoc + proj), P(-L / 2 - 140, 0), S, angle=90)
    level(sp, P(-L / 2 - 720, 0)[0], P(0, 0)[1], fmt_level(0), "U/S PLATE", S, ext=(-6, 10))


def ceil5_(x):
    return 5 * math.ceil(x / 5)


# --------------------------------------------------------------------------- 2/5002: gable corner GK1
def gable_corner(ox, oy):
    """corner column under the continuous gable rafter: the column end plate (along the roof slope) bolted to the
    rafter bottom flange; rafter web stiffeners over the column flanges (seen in the gable plane)"""
    S = 10
    sp = msp
    P = lambda x, z: (ox + x, oy + z - EAVE)                                     # noqa: E731
    top = F.zt                                                       # rafter top in the roof plane
    bot = lambda x: F.zt(x) - GR.d / COS                             # noqa: E731
    xa, xb = -900.0, 1_250.0
    for zf, dn in ((top, -1), (bot, 1)):
        line(sp, P(xa, zf(xa)), P(xb, zf(xb)), "S-STL")
        line(sp, P(xa, zf(xa) + dn * GR.tf / COS), P(xb, zf(xb) + dn * GR.tf / COS), "S-STL-VIS")
    zbreak(sp, P(xa, bot(xa) - 60), P(xa, top(xa) + 60), S)
    zbreak(sp, P(xb, bot(xb) - 60), P(xb, top(xb) + 60), S)
    dtop = col_d(EAVE)
    tp = GK["tp"]
    ext = GK["pf"] + GK["de"]
    # end plate along the slope under the rafter bottom flange, column cut to the slope below it
    pa, pb = -dtop / 2 - ext, dtop / 2 + ext
    q = [(pa, bot(pa)), (pb, bot(pb)), (pb, bot(pb) - tp / COS), (pa, bot(pa) - tp / COS)]
    plate(sp, P, q)
    z0 = EAVE - 1_100.0
    for sg in (-1, 1):
        xf = sg * dtop / 2
        line(sp, P(sg * col_d(z0) / 2, z0), P(xf, bot(xf) - tp / COS), "S-STL")
        line(sp, P(sg * (col_d(z0) / 2 - T["C"]["tf"]), z0),
             P(sg * (dtop / 2 - T["C"]["tf"]), bot(sg * (dtop / 2 - T["C"]["tf"])) - tp / COS), "S-STL-VIS")
        # rafter web stiffener pair over each column flange (vertical, between the rafter flanges)
        xs = sg * (dtop / 2 - T["C"]["tf"] / 2)
        line(sp, P(xs - 8, bot(xs - 8) + GR.tf / COS), P(xs - 8, top(xs - 8) - GR.tf / COS), "S-STL-VIS")
        line(sp, P(xs + 8, bot(xs + 8) + GR.tf / COS), P(xs + 8, top(xs + 8) - GR.tf / COS), "S-STL-VIS")
    zbreak(sp, P(-col_d(z0) / 2 - 60, z0), P(col_d(z0) / 2 + 60, z0), S)
    # bolts square to the plate: 2 rows outside each column flange... shown as rows along the slope
    u = (COS, SIN)
    for xr_ in (-dtop / 2 - GK["pf"], -dtop / 2 + T["C"]["tf"] + GK["pf"], dtop / 2 - T["C"]["tf"] - GK["pf"],
                dtop / 2 + GK["pf"]):
        c = (xr_, bot(xr_))
        n = (-SIN, COS)
        a = (c[0] - n[0] * (tp + 6), c[1] - n[1] * (tp + 6) / COS * COS)
        line(sp, P(c[0] - n[0] * (tp / COS + 30), c[1] - (tp / COS + 30)), P(c[0] + n[0] * (GR.tf + 30),
             c[1] + GR.tf / COS + 30), "S-CENT")
        sp.add_circle(P(c[0], c[1] - tp / COS / 2), GK["db"] * 0.85, dxfattribs=A("S-BOLT"))
    line(sp, P(0, z0 + 100), P(0, top(0) + 300), "S-GRID")
    note_cfg(xR=P(xb + 150, 0)[0])
    leader(sp, P(pb, bot(pb) - tp / COS / 2), (0, 0),
           f"COLUMN END PL {tp} x {GK['bp']:.0f} x {pb - pa:.0f} (ALONG THE SLOPE) SM520B, {GK['n_bolts']}-M{GK['db']} "
           f"GR 10.9 PRETENSIONED", S, side="R", width=56)
    leader(sp, P(dtop / 2 - 8, (bot(dtop / 2) + top(dtop / 2)) / 2), (0, 0),
           f"PAIR RAFTER WEB STIFFENERS PL {GK['column']['ts']} OVER EACH COLUMN FLANGE", S, side="R", width=56)
    leader(sp, P(-dtop / 2 - 200, bot(-dtop / 2 - 200) + GR.tf / 2 / COS), (0, 0),
           f"RAFTER BOTTOM FLANGE PL {GK['column']['tf_used']:g} x {GR.bf:.0f} OVER THE COLUMN (TBC)", S, side="R",
           width=56)
    mtag(sp, P, (-650, top(-650) + 260), "GR1", S)
    mtag(sp, P, (-dtop / 2 - 300, z0 + 250), "C2", S)


# --------------------------------------------------------------------------- 3/5002: gable rafter splice GS1 (GS2 similar)
def gable_splice(ox, oy):
    S = 10
    sp = msp

    def P(u, v):
        return (ox + u * COS - v * SIN, oy + u * SIN + v * COS)
    ep = GS1
    d = GR.d
    tpl = ep["tp"]
    rows, L = splice_rows(ep, d)
    vb = -d / 2 - ep["pf"] - ep["de"]
    for sg in (-1, 1):
        u0, u1 = sg * tpl, sg * 800.0
        plate(sp, P, [(0, vb), (u0, vb), (u0, vb + L), (0, vb + L)])
        for v, inn in ((d / 2, -1), (-d / 2, 1)):
            line(sp, P(u0, v), P(u1, v), "S-STL")
            line(sp, P(u0, v + inn * GR.tf), P(u1, v + inn * GR.tf), "S-STL-VIS")
        zbreak(sp, P(u1, -d / 2 - 60), P(u1, d / 2 + 60), S)
    for r in rows:
        bolt_h(sp, P, vb + r, -tpl, tpl, ep["db"], S)
    line(sp, P(-900, 0), P(900, 0), "S-GRID")
    weld(sp, P(tpl + 80, d / 2), (P(tpl + 80, d / 2)[0] + 12 * S, P(tpl + 80, d / 2)[1] + 20 * S), S,
         ep["flange_weld"], side="both", tail="BOTH FLANGES, BOTH PLATES")
    note_cfg(xL=P(-800, 0)[0] - 4 * S)
    leader(sp, P(-tpl, vb + L - 20), (0, 0), f"2 END PLATES PL {tpl} x {ep['bp']:.0f} x {L:.0f} SM520B", S,
           side="L", width=46)
    leader(sp, P(-tpl - 0.85 * ep["db"] - 4, vb + rows[2]), (0, 0),
           f"{ep['n_bolts']}-M{ep['db']} GR 10.9 PRETENSIONED", S, side="L", width=46)
    mtag(sp, P, (-500, -d / 2 - 170), "GR1", S)
    mtag(sp, P, (500, -d / 2 - 170), "GR2", S)


# --------------------------------------------------------------------------- 4/5002: gable post top
def post_top(ox, oy):
    """gable post (H 400 x 150, depth along the building) under the gable rafter, seen along the building: the post
    flange (150) seen, cap plate along the slope, 4-M16 through the rafter bottom flange"""
    S = 10
    sp = msp
    P = lambda x, z: (ox + x, oy + z)                                            # noqa: E731
    top = lambda x: SLOPE * x                                       # noqa: E731  rafter top (local, z = 0 at x = 0)
    bot = lambda x: top(x) - GR.d / COS                             # noqa: E731
    for zf, dn in ((top, -1), (bot, 1)):
        line(sp, P(-700, zf(-700)), P(700, zf(700)), "S-STL")
        line(sp, P(-700, zf(-700) + dn * GR.tf / COS), P(700, zf(700) + dn * GR.tf / COS), "S-STL-VIS")
    zbreak(sp, P(-700, bot(-700) - 60), P(-700, top(-700) + 60), S)
    zbreak(sp, P(700, bot(700) - 60), P(700, top(700) + 60), S)
    bf = C.GPOST.bf
    tpc = 12.0
    plate(sp, P, [(-bf / 2 - 40, bot(-bf / 2 - 40)), (bf / 2 + 40, bot(bf / 2 + 40)),
                  (bf / 2 + 40, bot(bf / 2 + 40) - tpc / COS), (-bf / 2 - 40, bot(-bf / 2 - 40) - tpc / COS)])
    zp = bot(0) - 700
    for sg in (-1, 1):
        line(sp, P(sg * bf / 2, zp), P(sg * bf / 2, bot(sg * bf / 2) - tpc / COS), "S-STL")
    line(sp, P(0, zp), P(0, bot(0) - tpc / COS), "S-STL-VIS")                    # web seen edge-on (behind)
    zbreak(sp, P(-bf / 2 - 60, zp), P(bf / 2 + 60, zp), S)
    for sg in (-1, 1):
        x = sg * 55.0
        line(sp, P(x, bot(x) - tpc / COS - 40), P(x, bot(x) + GR.tf / COS + 40), "S-CENT")
    pt = D["post_top"]
    note_cfg(xR=P(800, 0)[0])
    leader(sp, P(bf / 2 + 40, bot(bf / 2 + 40) - tpc / COS / 2), (0, 0),
           f"CAP PL {tpc:.0f} x 230 x 470 SM400B (ALONG THE SLOPE), 4-M16 8.8 AT 110 x 360 THROUGH THE RAFTER "
           f"FLANGE; POST TOP V {pt['V']:.0f} kN", S, side="R", width=52)
    leader(sp, P(bf / 2, zp + 200), (0, 0), "GABLE POST H 400 x 150 x 6 x 10 (GP1 - GP3)", S, side="R", width=52)
    weld(sp, P(-bf / 2, bot(-bf / 2) - tpc / COS - 20), (P(-bf / 2, 0)[0] - 18 * S, P(0, bot(0) - 200)[1]), S, 6,
         all_round=True, left=True)


# --------------------------------------------------------------------------- 6/5002: eave beam EB1 (plan at the eave)
def eave_beam(ox, oy):
    """plan at the eave level: the column (seen in section, 800 deep at the eave), the shop-welded stub of the eave
    beam on the column web with backing stiffeners, the field end-plate splice EB1, the beam beyond"""
    S = 10
    sp = msp
    P = lambda x, y: (ox + x, oy + y)                                            # noqa: E731
    dc, bf, tw, tf = col_d(EAVE), T["C"]["bf"], T["C"]["tw"], D["CH1"]["tf"]   # in the column head CH1A
    hsec(sp, P, (0, 0), dc, bf, tw, tf, rot=90, layer="S-STL")              # column: web along x (across the span)
    eb = C.EAVEB
    stub = 500.0
    y0 = tw / 2
    # stub: flanges seen from above as one band (top flange), web below it (hidden), along +y
    for x in (-eb.bf / 2, eb.bf / 2):
        line(sp, P(x, y0), P(x, y0 + stub), "S-STL")
    line(sp, P(-eb.tw / 2, y0), P(-eb.tw / 2, y0 + stub), "S-STL-HIDN")
    line(sp, P(eb.tw / 2, y0), P(eb.tw / 2, y0 + stub), "S-STL-HIDN")
    tpl = EB["tp"]
    plate(sp, P, [(-EB["bp"] / 2, y0 + stub), (EB["bp"] / 2, y0 + stub), (EB["bp"] / 2, y0 + stub + tpl),
                  (-EB["bp"] / 2, y0 + stub + tpl)])
    plate(sp, P, [(-EB["bp"] / 2, y0 + stub + tpl), (EB["bp"] / 2, y0 + stub + tpl),
                  (EB["bp"] / 2, y0 + stub + 2 * tpl), (-EB["bp"] / 2, y0 + stub + 2 * tpl)])
    ye = y0 + stub + 2 * tpl + 900
    for x in (-eb.bf / 2, eb.bf / 2):
        line(sp, P(x, y0 + stub + 2 * tpl), P(x, ye), "S-STL")
    zbreak(sp, P(-eb.bf / 2 - 60, ye), P(eb.bf / 2 + 60, ye), S)
    for x in (-EB["g"] / 2, EB["g"] / 2):
        bolt_h_y(sp, P, x, y0 + stub, y0 + stub + 2 * tpl, EB["db"], S)
    # backing stiffeners on the other side of the column web, in line with the stub flanges
    plate(sp, P, [(-dc / 2 + tf, -tw / 2), (dc / 2 - tf, -tw / 2), (dc / 2 - tf, -bf / 2 + 5),
                  (-dc / 2 + tf, -bf / 2 + 5)], layer="S-STL-VIS")
    line(sp, P(0, -bf / 2 - 200), P(0, ye + 200), "S-GRID")
    note_cfg(xR=P(dc / 2 + 250, 0)[0], xL=P(-dc / 2 - 250, 0)[0])
    leader(sp, P(eb.bf / 2, y0 + stub / 2), (0, 0),
           f"STUB H 400 x 200 x 8 x 13, {stub:.0f} LONG, FLANGES CJP AND WEB 6 mm FILLETS TO THE COLUMN WEB (SHOP)",
           S, side="R", width=50)
    leader(sp, P(EB["bp"] / 2, y0 + stub + tpl), (0, 0),
           f"EB1 SPLICE: 2 END PLATES PL {tpl} x {EB['bp']:.0f} x {EB['length']:.0f} SM520B, {EB['n_bolts']}-M"
           f"{EB['db']} GR 10.9 PRETENSIONED", S, side="R", width=50)
    leader(sp, P(-dc / 2 + tf + 60, -bf / 4), (0, 0),
           f"BACKING STIFFENERS PL {EB['tf'] + 3:.0f} x {(bf - tw) / 2 - 5:.0f} (PAIR, IN LINE WITH THE STUB FLANGES), "
           f"6 mm FILLETS ALL EDGES; COORDINATE WITH THE KNEE CONTINUITY PLATES", S, side="L", width=52)
    mtag(sp, P, (-eb.bf / 2 - 200, ye - 200), "EB1", S)
    mtag(sp, P, (-dc / 2 - 150, 150), "CH1A", S)


def bolt_h_y(sp, P, x, y_nut, y_head, d, S):
    """bolt seen from above, axis along y"""
    w = 1.7 * d
    line(sp, P(x - d / 2, y_nut), P(x - d / 2, y_head), "S-STL-HIDN")
    line(sp, P(x + d / 2, y_nut), P(x + d / 2, y_head), "S-STL-HIDN")
    plate(sp, P, [(x - w / 2, y_head), (x + w / 2, y_head), (x + w / 2, y_head + 0.65 * d), (x - w / 2, y_head + 0.65 * d)],
          layer="S-BOLT")
    plate(sp, P, [(x - w / 2, y_nut), (x + w / 2, y_nut), (x + w / 2, y_nut - 0.85 * d), (x - w / 2, y_nut - 0.85 * d)],
          layer="S-BOLT")


# --------------------------------------------------------------------------- 1/5003: brace node (roof plane)
def brace_node(ox, oy):
    """plan in the roof plane at a braced-bay rafter node (frame 2, x = 4.5 m): the rafter, gusset GU1 welded to
    the web below the top flange with a full-depth stiffener, two braces BR1 and the strut ST1 on knife plates"""
    S = 10
    sp = msp
    P = lambda x, y: (ox + x, oy + y)                                            # noqa: E731
    bf = T["H"]["bf"]
    L = 1_400.0
    for x in (-bf / 2, bf / 2):                                               # rafter top flange (plan, along x)
        line(sp, P(-L, x), P(L, x), "S-STL")
    line(sp, P(-L, 0), P(L, 0), "S-GRID")
    zbreak(sp, P(-L, -bf / 2 - 60), P(-L, bf / 2 + 60), S)
    zbreak(sp, P(L, -bf / 2 - 60), P(L, bf / 2 + 60), S)
    tg = GU["tg"]
    gy0 = 3.0                                                                 # gusset from the web face (below flange)
    gus = [(-260.0, gy0), (260.0, gy0), (420.0, 420.0), (-420.0, 420.0)]
    q = [P(*v) for v in gus]
    pline(sp, q, "S-STL-HIDN", close=True)                                    # below the top flange where covered
    for a_, b_ in ((gus[1], gus[2]), (gus[2], gus[3]), (gus[3], gus[0])):
        pass
    line(sp, P(-bf / 2 * 0, bf / 2), P(0, bf / 2), "S-STL")
    # members: strut along +y (bay direction), braces at +/- angle
    ang = math.atan2(BAY, 4_500.0)                                            # brace angle from the rafter (plan)
    mems = [("ST1", (0.0, 1.0), C.BRACE.D, ST1), ("BR1", (math.cos(ang), math.sin(ang)), C.BRACE.D, BR),
            ("BR1", (-math.cos(ang), math.sin(ang)), C.BRACE.D, BR)]
    for mk, u, D_, rr in mems:
        n = (-u[1], u[0])
        s0 = 420.0 / u[1] + 40                                                # tube end beyond the gusset edge
        s1 = s0 + 900
        c0, c1 = (u[0] * s0, u[1] * s0), (u[0] * s1, u[1] * s1)
        for sg in (-1, 1):
            line(sp, P(c0[0] + sg * n[0] * D_ / 2, c0[1] + sg * n[1] * D_ / 2),
                 P(c1[0] + sg * n[0] * D_ / 2, c1[1] + sg * n[1] * D_ / 2), "S-STL")
        line(sp, P(c0[0] - n[0] * D_ / 2, c0[1] - n[1] * D_ / 2), P(c0[0] + n[0] * D_ / 2, c0[1] + n[1] * D_ / 2), "S-STL")
        chs_break(sp, P(*c1), u, D_, C.BRACE.t, S)
        # knife plate: lap inside the slotted tube, out over the gusset to the bolts (gap 10 to the tube end)
        s_k = s0 - rr["gap"] - (rr["n"] - 1) * rr["p"] - 2 * rr["e1"]
        kb = rr["bk"] / 2
        S_ = lambda s, w: (u[0] * s + n[0] * w, u[1] * s + n[1] * w)            # noqa: E731
        pline(sp, [P(*S_(s_k, kb)), P(*S_(s0, kb))], "S-STL-VIS")
        pline(sp, [P(*S_(s_k, -kb)), P(*S_(s0, -kb))], "S-STL-VIS")
        line(sp, P(*S_(s_k, kb)), P(*S_(s_k, -kb)), "S-STL-VIS")
        for w in (kb, -kb):
            line(sp, P(*S_(s0, w)), P(*S_(s0 + rr["lap"], w)), "S-STL-HIDN")
        line(sp, P(*S_(s0 + rr["lap"], kb)), P(*S_(s0 + rr["lap"], -kb)), "S-STL-HIDN")
        for k in range(rr["n"]):
            s_b = s_k + rr["e1"] + k * rr["p"]
            hole(sp, P(u[0] * s_b, u[1] * s_b), rr["hole"], S)
        rr["_bolt0"] = (u[0] * (s_k + rr["e1"]), u[1] * (s_k + rr["e1"]))
        line(sp, P(0, 0), P(*c1), "S-GRID")
    note_cfg(xR=P(L + 150, 0)[0], xL=P(-L - 150, 0)[0])
    leader(sp, P(*ST1["_bolt0"]), (0, 0), f"{ST1['n']}-M{ST1['db']} 8.8 (BEARING) PER MEMBER, HOLES "
           f"Ø{ST1['hole']}", S, side="R", width=48, bolt=ST1["hole"])
    leader(sp, P(420, 420), (0, 0), f"GUSSET GU1 PL {tg:.0f} SM400B IN THE ROOF PLANE, {GU['weld']:.0f} mm FILLETS "
           f"BOTH SIDES TO THE RAFTER WEB, FULL-DEPTH WEB STIFFENER PL {GU['stiffener']['t']:.0f} OPPOSITE", S,
           side="R", width=48)
    leader(sp, P(-260, gy0 + 30), (0, 0), f"KNIFE PL {BR['tk']:.0f} x {BR['bk']:.0f} SHOP-WELDED IN THE TUBE SLOT, "
           f"4 x {BR['weld']:.0f} mm FILLETS x {BR['lap']:.0f} LONG (SLOT {BR['slot']:.0f} WIDE)", S, side="L",
           width=48)
    mtag(sp, P, (-L + 300, -bf / 2 - 160), "R1A", S)
    for mk, u, D_, rr in mems:
        s = 420.0 / u[1] + 700
        mtag(sp, P, (u[0] * s + 140 * (1 if u[0] >= 0 else -1), u[1] * s), mk, S)


# --------------------------------------------------------------------------- 2/5003: section at a purlin: cleat, sag rod, fly brace
def purlin_section(ox, oy):
    """section across the rafter (prismatic, 350 deep) at a fly-braced purlin, 1:10, looking along the rafter: the
    rafter cut, the purlin seen along its length on the rafter top flange, the cleat face-on with 2 bolts, the sag
    rod hole, the two fly braces FB1 (45 deg) from the purlin web to the lug under the rafter bottom flange"""
    S = 10
    sp = msp
    P = lambda x, y: (ox + x, oy + y)                                            # noqa: E731
    r = RAF
    hsec(sp, P, (0, -r.d / 2), r.d, r.bf, r.tw, r.tf, layer="S-STL")          # rafter cut (top flange at y = 0)
    pu = PU["sec"]
    Lp = 1_100.0
    for y in (0.0, pu.d):                                                     # purlin flanges seen along the length
        line(sp, P(-Lp, y), P(Lp, y), "S-STL")
    for y in (pu.tf, pu.d - pu.tf):
        line(sp, P(-Lp, y), P(Lp, y), "S-STL-VIS")
    for x in (-Lp, Lp):
        zbreak(sp, P(x, -40), P(x, pu.d + 40), S)
    # cleat PL 10 x 100 (parallel to the purlin web), face-on, behind the purlin web: 2 bolts
    cw, ch = 100.0, pu.d - 2 * pu.tf - 10
    plate(sp, P, [(r.bf / 2 - cw, 0), (r.bf / 2, 0), (r.bf / 2, ch), (r.bf / 2 - cw, ch)], layer="S-STL-HIDN")
    for y in (ch * 0.35, ch * 0.75):
        hole(sp, P(r.bf / 2 - cw / 2, y), 18, S)
    hole(sp, P(-Lp + 250, pu.d / 2), SR["d"] + 2, S)                           # sag rod hole (third point side)
    # fly braces: both sides, gauge line from the purlin web (near its bottom flange) to the lug, F = 45 deg
    yb = -r.d - 50.0
    ytop = pu.tf + 40
    dx = ytop - yb                                                             # 45 deg: run = rise
    for sg in (-1, 1):
        a, b_ = (sg * dx, ytop), (0.0, yb)
        u = ((b_[0] - a[0]) / math.hypot(dx, ytop - yb), (b_[1] - a[1]) / math.hypot(dx, ytop - yb))
        n = (-u[1] * sg, u[0] * sg)
        for w in (-25.0, 25.0):
            line(sp, P(a[0] + n[0] * w, a[1] + n[1] * w), P(b_[0] + n[0] * w + u[0] * -30, b_[1] + n[1] * w - u[1] * 30),
                 "S-STL-VIS")
        line(sp, P(*a), P(*b_), "S-GRID")
        hole(sp, P(a[0] + u[0] * 30, a[1] + u[1] * 30), 18, S)
    plate(sp, P, [(-40, -r.d), (40, -r.d), (40, yb - 60), (-40, yb - 60)])  # lug under the bottom flange
    line(sp, P(0, yb - 120), P(0, pu.d + 150), "S-GRID")
    note_cfg(xR=P(Lp + 150, 0)[0], xL=P(-Lp - 150, 0)[0])
    leader(sp, P(Lp - 200, pu.d), (0, 0), f"PU1 {pu.name} (TBC)", S, side="R", width=44)
    leader(sp, P(r.bf / 2, ch * 0.9), (0, 0), "PURLIN CLEAT PL 10 x 100 SM400B, 5 mm FILLETS TO THE RAFTER FLANGE, "
           "2-M16 8.8 TO THE PURLIN WEB", S, side="R", width=44)
    leader(sp, P(-Lp + 250, pu.d / 2), (0, 0), f"SAG ROD Ø{SR['d']} IN HOLE Ø{SR['d'] + 2} (THIRD POINTS)", S,
           side="L", width=40, bolt=SR["d"] + 2)
    leader(sp, P(-dx * 0.55, ytop - (ytop - yb) * 0.55), (0, 0),
           f"FB1 {FB1['angle']} BOTH SIDES AT 45 deg, {FB1['bolts']} (TBC)", S, side="L", width=40)
    leader(sp, P(40, yb - 30), (0, 0), "LUG PL 10 x 80 x 100 UNDER THE BOTTOM FLANGE, 5 mm FILLETS", S, side="R",
           width=44)
    mtag(sp, P, (-160, yb - 40), "R2", S)
