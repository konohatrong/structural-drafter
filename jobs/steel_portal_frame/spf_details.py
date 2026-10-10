"""
Project SPF - connection details (views at 1:10), drawn from the calc (calc_spf.design via spf_engine.D) on the
frame geometry of spf_engine.Frame. Imported by spf_sheets.py, which places the views on the sheets.

5001: knee and canopy root with the column head CH1 and the column splice CS1 (elevation), views on the knee,
      canopy and column-splice plates, rafter splice, view on the splice plate, ridge with the monitor post bases.
"""
import math

from spf_engine import *          # noqa: F401,F403
import spf_engine as SE
import calc_spf as C

F = SE.Frame
K = F.knee()
KJ, SP, RJ, CJ = D["KJ1"], D["SP1"], D["RJ1"], D["CJ1"]
MB = D["MB1"]
TP_K, TP_S, TP_R, TP_C = KJ["tp"], SP["tp"], RJ["tp"], CJ["tp"]
X_SPL = C.X_SPLICE
SB, COS_B = K["sb"], K["cos_b"]                                     # haunch bottom-flange slope (in the frame)
CS = D["CS1"]                                                       # column splice below the knee
TF_IN = D["CH1"]["tf"]                                              # column head CH1: both flanges
TS = KJ["column"]["ts"]                                             # continuity plates


# --------------------------------------------------------------------------- generic pieces
def bolt_h(sp, P, y, x_nut, x_head, d, S, layer="S-BOLT"):
    """bolt seen from the side, axis along x: shank (hidden) from the nut face to the head face, head and nut +
    washer outlines; x_head > x_nut or < x_nut (either direction)"""
    sg = 1 if x_head > x_nut else -1
    hh, nh, w = 0.65 * d, 0.85 * d, 1.7 * d
    line(sp, P(x_nut, y - d / 2), P(x_head, y - d / 2), "S-STL-HIDN")
    line(sp, P(x_nut, y + d / 2), P(x_head, y + d / 2), "S-STL-HIDN")
    pline(sp, [P(x_head, y - w / 2), P(x_head + sg * hh, y - w / 2), P(x_head + sg * hh, y + w / 2),
               P(x_head, y + w / 2)], layer, close=True)
    xn = x_nut - sg * 0.18 * d                                      # washer
    pline(sp, [P(x_nut, y - w / 2 - 0.2 * d), P(xn, y - w / 2 - 0.2 * d), P(xn, y + w / 2 + 0.2 * d),
               P(x_nut, y + w / 2 + 0.2 * d)], layer, close=True)
    pline(sp, [P(xn, y - w / 2), P(xn - sg * nh, y - w / 2), P(xn - sg * nh, y + w / 2), P(xn, y + w / 2)],
          layer, close=True)
    line(sp, P(xn - sg * (nh + 0.3 * d), y), P(x_head + sg * (hh + 0.3 * d), y), "S-CENT")


def face_view(sp, P, ep, rows, members, S, length=None, label_rows=True):
    """view on an end plate: plate bp wide (x) by its length (y), holes on gauge g at the rows (y from the plate
    bottom), the member outline behind it (hidden). members: list of ("flange", y0, y1) / ("web", tw, y0, y1)"""
    bp, g, L = ep["bp"], ep["g"], length or ep["length"]
    plate(sp, P, [(-bp / 2, 0), (bp / 2, 0), (bp / 2, L), (-bp / 2, L)])
    for kind, *v in members:
        if kind == "flange":
            y0, y1, bf = v
            pline(sp, [P(-bf / 2, y0), P(bf / 2, y0), P(bf / 2, y1), P(-bf / 2, y1)], "S-STL-HIDN", close=True)
        else:
            tw, y0, y1 = v
            line(sp, P(-tw / 2, y0), P(-tw / 2, y1), "S-STL-HIDN")
            line(sp, P(tw / 2, y0), P(tw / 2, y1), "S-STL-HIDN")
    for y in rows:
        for x in (-g / 2, g / 2):
            hole(sp, P(x, y), ep["hole"], S)
    # dimensions: gauge and plate width below, the bolt rows along the right edge
    dim(sp, P(-g / 2, 0), P(g / 2, 0), P(0, -9 * S), S)
    dim(sp, P(-bp / 2, 0), P(bp / 2, 0), P(0, -16 * S), S)
    xs = bp / 2 + 10 * S
    pts = [0.0] + sorted(rows) + [L]
    for a, b in zip(pts[:-1], pts[1:]):
        dim(sp, P(bp / 2, a), P(bp / 2, b), P(xs, a), S, angle=90, tside=None)
    dim(sp, P(bp / 2, 0), P(bp / 2, L), P(xs + 8 * S, 0), S, angle=90)
    return P(0, 0)


def knee_rows():
    """bolt rows of the knee plate (z on the column face line, outer row first), as designed (calc knee_geometry)"""
    return K["rows"]


def face_axes(fx, z0, z1, outward):
    """a plate lying on the tapered face x = fx(z): t along the face (upward), n square to it (outward = +1: +x)"""
    t, _ = unit((fx(z0), z0), (fx(z1), z1))
    n = (t[1], -t[0]) if outward > 0 else (-t[1], t[0])
    return t, n


def face_plate(sp, P, fx, z0, z1, tp, outward, layer="S-STL"):
    """plate of thickness tp on the face x = fx(z) from z0 to z1: faces parallel to the flange, ends square to it
    (STEEL_DETAILING_INSTRUCTION S2.9); returns the outer-face line (point, direction) and n"""
    t, n = face_axes(fx, z0, z1, outward)
    a, b = (fx(z0), z0), (fx(z1), z1)
    plate(sp, P, [a, b, off(b, n, tp), off(a, n, tp)], layer)
    return (off(a, n, tp), t), n


def isect(p, u, q, v):
    """intersection of the lines p + a u and q + b v"""
    den = u[0] * v[1] - u[1] * v[0]
    a = ((q[0] - p[0]) * v[1] - (q[1] - p[1]) * v[0]) / den
    return (p[0] + a * u[0], p[1] + a * u[1])


def bolt_ax(sp, P, c, u, s_nut, s_head, d, layer="S-BOLT"):
    """bolt seen from the side, axis through c along the unit vector u: shank (hidden) between the nut and head
    faces at s_nut and s_head along u, head, washer and nut outlines, centre line"""
    sg = 1 if s_head > s_nut else -1
    v = (-u[1], u[0])
    Q = lambda s, w: P(c[0] + u[0] * s + v[0] * w, c[1] + u[1] * s + v[1] * w)   # noqa: E731
    hh, nh, w = 0.65 * d, 0.85 * d, 1.7 * d
    for k in (-d / 2, d / 2):
        line(sp, Q(s_nut, k), Q(s_head, k), "S-STL-HIDN")
    pline(sp, [Q(s_head, -w / 2), Q(s_head + sg * hh, -w / 2), Q(s_head + sg * hh, w / 2), Q(s_head, w / 2)],
          layer, close=True)
    sn = s_nut - sg * 0.18 * d                                      # washer
    pline(sp, [Q(s_nut, -w / 2 - 0.2 * d), Q(sn, -w / 2 - 0.2 * d), Q(sn, w / 2 + 0.2 * d),
               Q(s_nut, w / 2 + 0.2 * d)], layer, close=True)
    pline(sp, [Q(sn, -w / 2), Q(sn - sg * nh, -w / 2), Q(sn - sg * nh, w / 2), Q(sn, w / 2)], layer, close=True)
    line(sp, Q(sn - sg * (nh + 0.3 * d), 0), Q(s_head + sg * (hh + 0.3 * d), 0), "S-CENT")


def canopy_geom():
    """canopy root: the canopy flanges meeting the outer face of the canopy end plate, which lies on the column
    head outer flange (tapered); the bolt rows (z on the column face line) and the plate ends"""
    t_x = TP_C / math.cos(C.COL_ALPHA)

    def meet(fn):
        x = -col_d(EAVE) / 2
        for _ in range(30):
            x = F.cx(fn(x - t_x), -1)
        return x, fn(x - t_x)
    xt, zt_ = meet(F.zt)
    xb, zb_ = meet(lambda x: F.zt(x) - CAN.d / COS)
    pf, de, tf = CJ["pf"], CJ["de"], CJ["tf"]
    rows = [zt_ + pf / COS, zt_ - (tf + pf) / COS, zb_ + (tf + pf) / COS, zb_ - pf / COS]
    top, bot = rows[0] + de, rows[-1] - de
    return dict(xt=xt, zt=zt_, xb=xb, zb=zb_, rows=rows, top=top, bot=bot,
                length=(top - bot) / math.cos(C.COL_ALPHA))


def cs_rows():
    """CS1 bolt lines across the column (x from the column centre line, frame plane), outer flange side first"""
    d, pf, tf = CS["d"], CS["pf"], CS["tf"]
    return [-(d / 2 + pf), -(d / 2 - tf - pf), d / 2 - tf - pf, d / 2 + pf]


# --------------------------------------------------------------------------- 1/5001: knee and canopy root
def knee_detail(ox, oy):
    S = 10
    sp = msp
    z_off = EAVE - 900.0
    P = lambda x, z: (ox + x, oy + z - z_off)                                    # noqa: E731
    zs, tps = CS["z"], CS["tp"]                                                   # column splice CS1
    z0 = zs - tps - 350.0                                                         # column C1 broken here
    zo, zi = K["col_top_out"], K["col_top_in"]
    xo = lambda z: F.cx(z, -1)                                                   # noqa: E731
    xi = lambda z: F.cx(z, 1)                                                    # noqa: E731
    # column C1 (flanges 14) up to its splice plate; column head CH1 (both flanges TF_IN) from the upper plate
    zl, zh = zs - tps, zs + tps
    for x_, sg in ((xo, 1), (xi, -1)):
        line(sp, P(x_(z0), z0), P(x_(zl), zl), "S-STL")
        line(sp, P(x_(z0) + sg * F.tf_c, z0), P(x_(zl) + sg * F.tf_c, zl), "S-STL-VIS")
    line(sp, P(xo(zh), zh), P(xo(zo), zo), "S-STL")
    line(sp, P(xo(zh) + TF_IN, zh), P(xo(zo) + TF_IN, zo + TF_IN * SLOPE), "S-STL-VIS")
    line(sp, P(xi(zh), zh), P(xi(zi), zi), "S-STL")
    line(sp, P(xi(zh) - TF_IN, zh), P(xi(zi) - TF_IN, zi - TF_IN * SLOPE), "S-STL-VIS")
    zbreak(sp, P(xo(z0) - 60, z0), P(xi(z0) + 60, z0), S)
    # splice plates CS1 (square to the column axis) and the bolts, nuts below
    Lh = CS["length"] / 2
    for za, zb_ in ((zl, zs), (zs, zh)):
        plate(sp, P, [(-Lh, za), (Lh, za), (Lh, zb_), (-Lh, zb_)])
    for x in cs_rows():
        bolt_ax(sp, P, (x, zs), (0.0, 1.0), -tps, tps, CS["db"], S)
    # cap plate PL 12 along the roof slope
    plate(sp, P, [(xo(zo), zo), (xi(zi), zi), (xi(zi), zi + 12 / COS), (xo(zo), zo + 12 / COS)])
    # continuity plates in line with the rafter flanges (seen edge-on, TS thick)
    cps = []
    for (x0, z0_), sl in (((K["xt"], K["zt"] - KJ["tf"] / COS), SLOPE), ((K["xb"], K["zb"]), SB)):
        a_, b_ = xo(z0_) + TF_IN, xi(z0_) - TF_IN
        q = [(a_, z0_ + (a_ - x0) * sl), (b_, z0_ + (b_ - x0) * sl),
             (b_, z0_ + (b_ - x0) * sl + TS), (a_, z0_ + (a_ - x0) * sl + TS)]
        plate(sp, P, q, layer="S-STL-VIS")
        cps.append(q)
    # knee end plate on the inner flange face: faces parallel to the flange, ends and bolts square to it
    rows = knee_rows()
    ztop, zbot = K["plate_top"], K["plate_bot"]
    (kp, kt), kn = face_plate(sp, P, xi, zbot, ztop, TP_K, 1)
    # rafter haunch from the plate face to x_end (broken): each flange line starts on the plate face
    xe = K["xt"] + 1_600.0
    tfh = KJ["tf"]
    tops = {}
    for zf, d_, cs_ in ((F.zt, -1, COS), (F.zb, 1, COS_B)):
        p0 = (K["xt"], zf(K["xt"]))
        u, _ = unit(p0, (xe, zf(xe)))
        for k_, lay in ((0.0, "S-STL"), (d_ * tfh / cs_, "S-STL-VIS")):
            q0 = (p0[0], p0[1] + k_)
            a = isect(q0, u, kp, kt)
            line(sp, P(*a), P(xe, zf(xe) + k_), lay)
            tops.setdefault(zf, a)
    zbreak(sp, P(xe, F.zb(xe) - 60), P(xe, F.zt(xe) + 60), S)
    for z in rows:                                                                # nut inside the column
        bolt_ax(sp, P, (xi(z), z), kn, -TF_IN, TP_K, KJ["db"], S)
    # canopy root: plate on the head outer flange face, canopy flanges from the plate face, bolts
    cg = canopy_geom()
    (cp_, ct_), cn = face_plate(sp, P, xo, cg["bot"], cg["top"], TP_C, -1)
    xce = cg["xt"] - 1_200.0
    xe_ = K["xt"] + 1_600.0
    note_cfg(xL=P(xce - 150, 0)[0], xR=P(xe_ + 150, 0)[0], yT=P(0, K["plate_top"] + 750)[1])
    for zf, d_ in ((F.zt, -1), (lambda x: F.zt(x) - CAN.d / COS, 1)):
        p0 = (cg["xt"], zf(cg["xt"]))
        u, _ = unit(p0, (xce, zf(xce)))
        for k_, lay in ((0.0, "S-STL"), (d_ * CAN.tf / COS, "S-STL-VIS")):
            a = isect((p0[0], p0[1] + k_), u, cp_, ct_)
            line(sp, P(*a), P(xce, zf(xce) + k_), lay)
    zbreak(sp, P(xce, F.zt(xce) - CAN.d / COS - 60), P(xce, F.zt(xce) + 60), S)
    for z in cg["rows"]:
        bolt_ax(sp, P, (xo(z), z), cn, -TF_IN, TP_C, CJ["db"], S)
    # centre line of the column, work point, eave strut beyond
    line(sp, P(0, z0 - 150), P(0, zi + 300), "S-GRID")
    wp_mark(sp, P(0, EAVE), S)
    sp.add_circle(P(0, EAVE), C.STRUT.D / 2, dxfattribs=A("S-STL-HIDN"))
    # welds (symbols): rafter flanges and web to the plate, continuity plates, splice plates
    fw = KJ["flange_weld"]
    xa = tops[F.zt]
    tip = P(xa[0] + 150 * COS, F.zt(xa[0] + 150 * COS))
    if fw == "CJP":
        weld(sp, tip, (tip[0] + 25 * S, tip[1] + 14 * S), S, "CJP", groove="bevel", ndt="UT")
    else:
        weld(sp, P(xa[0], xa[1] + 4), (P(xa[0], 0)[0] + 18 * S, P(0, ztop)[1] + 12 * S), S, fw, side="both")
    zw = rows[1] - 140
    pw = off((xi(zw), zw), kn, TP_K)
    weld(sp, P(*pw), (P(*pw)[0] + 30 * S, P(0, zw)[1] - 6 * S), S, KJ["web_weld"], side="both", tail="WEB")
    cpm = cps[1][1]
    weld(sp, P(cpm[0] - 40, cpm[1] + TS / 2 - 40 * SB), (P(cpm[0], 0)[0] + 12 * S, P(0, cpm[1])[1] - 12 * S), S,
         KJ["column"]["w_cp"], side="both", tail="CONTINUITY PL, ALL EDGES")
    weld(sp, P(xi(zl) - 2, zl - 2), (P(xi(zl), 0)[0] + 24 * S, P(0, zl)[1] - 9 * S), S, CS["flange_weld"],
         side="both", tail="FLANGES AND WEB, BOTH PLATES" if CS["flange_weld"] == f"{CS['web_weld']}" else
         "FLANGES, BOTH PLATES")
    if CS["flange_weld"] != f"{CS['web_weld']}":
        weld(sp, P(-F.tw_c / 2, zl - 2), (P(0, 0)[0] - 50 * S, P(0, zl)[1] - 12 * S), S, CS["web_weld"],
             side="both", left=True,
             tail="WEB, BOTH PLATES")
    # leaders, packed in a column each side
    plen = K["plate_len"]
    leader(sp, P(*off((xi(ztop - 30), ztop - 30), kn, TP_K)), (0, 0),
           f"KNEE END PLATE PL {TP_K} x {KJ['bp']:.0f} x {plen:.0f} SM520B, SQUARE TO THE COLUMN FLANGE", S,
           side="T", width=54)
    leader(sp, P(*off((xi(rows[0]), rows[0]), kn, -TF_IN - 0.85 * KJ["db"])), (0, 0),
           f"{KJ['n_bolts']}-M{KJ['db']} GR 10.9 PRETENSIONED, HOLES Ø{KJ['hole']}, SQUARE TO THE PLATE", S,
           side="T", width=54)
    zc = (zh + zbot) / 2
    leader(sp, P(xo(zc), zc), (0, 0),
           f"COLUMN HEAD CH1: BOTH FLANGES PL {TF_IN:g} x {F.bf_c:.0f}, WEB PL {F.tw_c:g} (TBC)", S, side="L",
           width=58)
    leader(sp, P(Lh, zs + tps / 2), (0, 0),
           f"COLUMN SPLICE CS1 AT {fmt_level(zs)}: 2 END PLATES PL {tps} x {CS['bp']:.0f} x {CS['length']:.0f} "
           f"SM520B, {CS['n_bolts']}-M{CS['db']} GR 10.9 PRETENSIONED, NUTS BELOW", S, side="R", width=62)
    leader(sp, P(cps[1][0][0], cps[1][0][1] + TS / 2), (0, 0),
           f"PAIR CONTINUITY PL {TS} x {KJ['column']['bst']:.0f}, CORNER CLIPS 20 x 20", S, side="L", width=58)
    cpt = off((xo(cg["top"] - 20), cg["top"] - 20), cn, TP_C)
    leader(sp, P(*cpt), (0, 0),
           f"CANOPY END PLATE PL {TP_C} x {CJ['bp']:.0f} x {cg['length']:.0f}, "
           f"{CJ['n_bolts']}-M{CJ['db']} GR 10.9 PRETENSIONED, SQUARE TO THE COLUMN FLANGE", S, side="L", width=58)
    leader(sp, P(xo(zo) + 40, zo + 40 * SLOPE + 12 / COS), (0, 0),
           "CAP PL 12 x 250, 6 mm FILLET ALL ROUND", S, side="L", width=58)
    for (x, z, s) in ((xi(z0 + 110) + 170, z0 + 110, "C1"), (xo(zh + 110) - 170, zh + 110, "CH1"),
                      (K["xt"] + 1_200, F.zb(K["xt"] + 1_200) - 170, "R1"),
                      (xce + 300, F.zt(xce + 300) - CAN.d / COS - 170, "CN1")):
        mtag(sp, P, (x, z), s, S)
    # plate thickness: in the plate note (bolt rows: on views A, B, D)


def splice_plan(ox, oy):
    """view D: on the CS1 plate of the column C1 (head CH1 removed), looking down; the column section below hidden"""
    S = 10
    sp = msp
    P = lambda x, y: (ox + x, oy + y)                                            # noqa: E731
    Lh, bp, g = CS["length"] / 2, CS["bp"], CS["g"]
    d, tf, tw, bf = CS["d"], F.tf_c, F.tw_c, F.bf_c
    plate(sp, P, [(-Lh, -bp / 2), (Lh, -bp / 2), (Lh, bp / 2), (-Lh, bp / 2)])
    for x0, x1 in ((-d / 2, -d / 2 + tf), (d / 2 - tf, d / 2)):
        pline(sp, [P(x0, -bf / 2), P(x1, -bf / 2), P(x1, bf / 2), P(x0, bf / 2)], "S-STL-HIDN", close=True)
    for y in (-tw / 2, tw / 2):
        line(sp, P(-d / 2 + tf, y), P(d / 2 - tf, y), "S-STL-HIDN")
    xs = cs_rows()
    for x in xs:
        for y in (-g / 2, g / 2):
            hole(sp, P(x, y), CS["hole"], S)
    line(sp, P(0, -bp / 2 - 60), P(0, bp / 2 + 60), "S-GRID")
    pts = [-Lh] + xs + [Lh]
    for a, b in zip(pts[:-1], pts[1:]):
        dim(sp, P(a, bp / 2), P(b, bp / 2), P(a, bp / 2 + 9 * S), S, tside=None)
    dim(sp, P(-Lh, bp / 2), P(Lh, bp / 2), P(-Lh, bp / 2 + 17 * S), S)
    dim(sp, P(Lh, -g / 2), P(Lh, g / 2), P(Lh + 9 * S, 0), S, angle=90)
    dim(sp, P(Lh, -bp / 2), P(Lh, bp / 2), P(Lh + 17 * S, 0), S, angle=90)
    note_cfg(xL=P(-Lh - 120, 0)[0])
    leader(sp, P(xs[0], -g / 2), (0, 0), f"{CS['n_bolts']}-M{CS['db']} IN HOLES Ø{CS['hole']}", S,
           side="L", width=30, bolt=CS["hole"])


def knee_plate_face(ox, oy):
    """view A on the knee end plate (looking at the column flange, rafter removed)"""
    S = 10
    sp = msp
    rows = knee_rows()
    zbot = rows[-1] - KJ["de"]
    L = rows[0] + KJ["de"] - zbot
    P = lambda x, y: (ox + x, oy + y)                                            # noqa: E731
    ys = [z - zbot for z in rows]
    face_view(sp, P, KJ, ys, [("flange", K["zt"] - zbot - KJ["tf"] / COS, K["zt"] - zbot, KJ["bf"]),
                               ("flange", K["zb"] - zbot, K["zb"] - zbot + KJ["tf"] / COS_B, KJ["bf"]),
                               ("web", KJ["tw"], K["zb"] - zbot, K["zt"] - zbot)], S, length=L)
    note_cfg(xL=P(-KJ["bp"] / 2 - 120, 0)[0])
    leader(sp, P(-KJ["g"] / 2, ys[1]), (0, 0), f"{KJ['n_bolts']}-M{KJ['db']} IN HOLES Ø{KJ['hole']}", S,
           side="L", width=30, bolt=KJ["hole"])


def canopy_plate_face(ox, oy):
    S = 10
    sp = msp
    cg = canopy_geom()
    P = lambda x, y: (ox + x, oy + y)                                            # noqa: E731
    ys = [z - cg["bot"] for z in cg["rows"]]
    L = cg["top"] - cg["bot"]
    face_view(sp, P, CJ, ys, [("flange", cg["zt"] - cg["bot"] - CAN.tf / COS, cg["zt"] - cg["bot"], CAN.bf),
                               ("flange", cg["zb"] - cg["bot"], cg["zb"] - cg["bot"] + CAN.tf / COS, CAN.bf),
                               ("web", CAN.tw, cg["zb"] - cg["bot"], cg["zt"] - cg["bot"])], S, length=L)


# --------------------------------------------------------------------------- 2/5001: rafter splice SP1
def splice_rows(ep, d):
    """rows along a perpendicular splice plate, measured from the plate bottom (4E symmetric)"""
    de, pf, tf = ep["de"], ep["pf"], ep["tf"]
    return [de, de + pf + tf + pf, de + pf + d - tf - pf, de + pf + d + pf], 2 * (de + pf) + d


def splice_detail(ox, oy):
    """the splice in the rafter plane, drawn at its true slope: local u along the rafter, v up (perpendicular)"""
    S = 10
    sp = msp
    xc, zc = X_SPL, C.roof_z(X_SPL)

    def P(u, v):
        return (ox + u * COS - v * SIN, oy + u * SIN + v * COS)
    d = RAF.d
    h = T["H"]
    tpl = TP_S
    rows, L = splice_rows(SP, d)
    vb = -d / 2 - SP["pf"] - SP["de"]                                 # plate bottom in v
    for sg, fl_t, bf_name in ((-1, h["tf"], "HAUNCH"), (1, RAF.tf, "RAFTER")):
        u0 = sg * tpl
        u1 = sg * 900.0
        plate(sp, P, [(0, vb), (u0, vb), (u0, vb + L), (0, vb + L)])
        for v, inn in ((d / 2, -1), (-d / 2, 1)):
            line(sp, P(u0, v), P(u1, v), "S-STL")
            line(sp, P(u0, v + inn * fl_t), P(u1, v + inn * fl_t), "S-STL-VIS")
        zbreak(sp, P(u1, -d / 2 - 60), P(u1, d / 2 + 60), S)
    for r in rows:
        bolt_h(sp, P, vb + r, -tpl, tpl, SP["db"], S)
    line(sp, P(-1_000, 0), P(1_000, 0), "S-GRID")
    tw_ = P(-tpl - 80, d / 2)                                       # haunch side: the slope falls away under the text
    weld(sp, tw_, (tw_[0] - 6 * S, tw_[1] + 26 * S), S, SP["flange_weld"], side="both", left=True,
         tail="TYP. BOTH FLANGES, BOTH PLATES")
    tw2 = P(tpl, -d / 4)                                            # web weld: symbol below the rafter, clear of it
    weld(sp, tw2, (tw2[0] + 10 * S, P(tpl, -d / 2)[1] - 16 * S), S, SP["web_weld"], side="both", tail="WEB")
    note_cfg(xL=P(-900, 0)[0] - 4 * S)
    leader(sp, P(-tpl, vb + L - 20), (0, 0),
           f"2 END PLATES PL {tpl} x {SP['bp']:.0f} x {L:.0f} SM520B, SQUARE TO THE RAFTER", S, side="L", width=56)
    leader(sp, P(-tpl - 0.85 * SP["db"] - 4, vb + rows[2]), (0, 0),
           f"{SP['n_bolts']}-M{SP['db']} GR 10.9 PRETENSIONED, HOLES Ø{SP['hole']}", S, side="L", width=56)
    mtag(sp, P, (-600, -d / 2 - 180), "R1", S)
    mtag(sp, P, (600, -d / 2 - 180), "R2", S)
    for a, b in zip([vb] + [vb + r for r in rows], [vb + r for r in rows] + [vb + L]):
        pass
    text(sp, f"HAUNCH FLANGE {h['tf']:.0f} x {h['bf']:.0f}  |  RAFTER FLANGE {RAF.tf:.0f} x {RAF.bf:.0f}",
         P(0, vb - 200), 2.0 * S, align=TA.TOP_CENTER)


def splice_plate_face(ox, oy):
    S = 10
    sp = msp
    d = RAF.d
    rows, L = splice_rows(SP, d)
    vb = SP["pf"] + SP["de"]
    P = lambda x, y: (ox + x, oy + y)                                            # noqa: E731
    face_view(sp, P, SP, rows, [("flange", vb, vb + RAF.tf, RAF.bf), ("flange", vb + d - RAF.tf, vb + d, RAF.bf),
                                ("web", RAF.tw, vb, vb + d)], S, length=L)


# --------------------------------------------------------------------------- 3/5001: ridge and monitor post bases
def ridge_detail(ox, oy):
    S = 10
    sp = msp
    P = lambda x, z: (ox + x - RIDGE, oy + z - C.roof_z(RIDGE))                  # noqa: E731
    note_cfg(xL=P(RIDGE - 1_250, 0)[0] - 4 * S, xR=P(RIDGE + 1_250, 0)[0] + 4 * S)
    d = RAF.d
    ext = (RJ["pf"] + RJ["de"]) / COS
    for sg in (-1, 1):                                                  # left (-1) and right rafters
        xr = RIDGE + sg * TP_R
        xe = RIDGE + sg * 1_250.0
        zt = lambda x: F.zt(x)                                         # noqa: E731
        zb = lambda x: F.zt(x) - d / COS                               # noqa: E731
        plate(sp, P, [(RIDGE, zt(xr) + ext), (xr, zt(xr) + ext), (xr, zb(xr) - ext), (RIDGE, zb(xr) - ext)])
        for zf, dn in ((zt, -1), (zb, 1)):
            line(sp, P(xr, zf(xr)), P(xe, zf(xe)), "S-STL")
            line(sp, P(xr, zf(xr) + dn * RAF.tf / COS), P(xe, zf(xe) + dn * RAF.tf / COS), "S-STL-VIS")
        zbreak(sp, P(xe, zb(xe) - 60), P(xe, zt(xe) + 60), S)
        # monitor post on its base plate (MB1)
        xm = RIDGE + sg * 1_000.0
        m = C.MON
        z_tf = zt(xm)
        bpl = MB["B"]
        q = [(xm - bpl / 2, zt(xm - bpl / 2)), (xm + bpl / 2, zt(xm + bpl / 2)),
             (xm + bpl / 2, zt(xm + bpl / 2) + MB["tp"] / COS), (xm - bpl / 2, zt(xm - bpl / 2) + MB["tp"] / COS)]
        plate(sp, P, q)
        ztop = z_tf + 450
        for xx in (xm - m.d / 2, xm + m.d / 2):
            line(sp, P(xx, zt(xx) + MB["tp"] / COS), P(xx, ztop), "S-STL")
        zbreak(sp, P(xm - m.d / 2 - 40, ztop), P(xm + m.d / 2 + 40, ztop), S)
        for xb_ in (xm - MB["s"] / 2, xm + MB["s"] / 2):
            line(sp, P(xb_, zt(xb_) - RAF.tf / COS - 30), P(xb_, zt(xb_) + MB["tp"] / COS + 30), "S-CENT")
    rows = [RJ["de"], RJ["de"] + RJ["pf"] + RJ["tf"] + RJ["pf"]]
    zt0 = F.zt(RIDGE) + ext
    zr = [zt0 - RJ["de"], zt0 - RJ["de"] - (RJ["pf"] * 2 + RJ["tf"]) / COS]
    zb0 = F.zt(RIDGE) - d / COS - ext
    zr += [zb0 + RJ["de"] + (RJ["pf"] * 2 + RJ["tf"]) / COS, zb0 + RJ["de"]]
    for z in zr:
        bolt_h(sp, P, z, RIDGE - TP_R, RIDGE + TP_R, RJ["db"], S)
    line(sp, P(RIDGE, zb0 - 300), P(RIDGE, zt0 + 600), "S-GRID")
    weld(sp, P(RIDGE + TP_R + 120, F.zt(RIDGE + TP_R + 120)),
         (P(RIDGE + 400, 0)[0], P(0, zt0 + 380)[1]), S, RJ["flange_weld"], side="both",
         tail="BOTH FLANGES, BOTH PLATES")
    leader(sp, P(RIDGE - TP_R, zt0 - 15), (0, 0),
           f"2 PLUMB END PLATES PL {TP_R} x {RJ['bp']:.0f} x {zt0 - zb0:.0f} SM520B", S, side="L", width=44)
    leader(sp, P(RIDGE + TP_R + 0.65 * RJ["db"] + 4, zr[2]), (0, 0),
           f"{RJ['n_bolts']}-M{RJ['db']} GR 10.9 PRETENSIONED", S, side="R", width=40)
    xm = RIDGE - 1_000.0
    leader(sp, P(xm - MB["B"] / 2, F.zt(xm - MB["B"] / 2) + MB["tp"] / COS / 2), (0, 0),
           f"MB1: POST BASE PL {MB['tp']} x {MB['B']:.0f} x {MB['B']:.0f}, 4-M{MB['db']} 8.8 THROUGH THE RAFTER "
           f"FLANGE AT {MB['s']:.0f} x {MB['s']:.0f}", S, side="L", width=44)
    mtag(sp, P, (RIDGE - 1_000, F.zt(RIDGE - 1_000) + 330), "MP1", S)
    mtag(sp, P, (RIDGE - 700, F.zt(RIDGE - 700) - d / COS - 160), "R2", S)
