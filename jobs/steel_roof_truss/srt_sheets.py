"""
Project SRT - steel roof truss T1: drawing content (views and sheets).

SRT-ST-1001  general notes, design criteria (TABLE 1 design summary, weld symbol key)
SRT-ST-3001  truss T1: half elevation 1:50, shop pieces / bracing key 1:200, member schedule (TABLE 2)
SRT-ST-5001  joint details 1:10: typical top and bottom nodes, centre node, node geometry (TABLE 3)
SRT-ST-5002  end of truss and bearing 1:10: end elevation, section through the bearing, base plates
SRT-ST-5003  site connections: chord flange splice 1:5, loose diagonal 1:10
SRT-ST-5004  fly bracing (after Beca SE-1505): section at a braced node 1:25, lug end and purlin end 1:10, TABLE 6
              (TABLE 4)
Every size, length, gap and eccentricity comes from calc_truss.py through srt_engine.py.
"""
import math

from srt_engine import *          # noqa: F401,F403  (engine + project data + steel helpers)
import srt_engine as SE
import calc_truss as C

doc.objects.set_wipeout_variables(frame=0)
BASE = "SRT-ST_Steel_Roof_Truss_T1_A3_RevA"
SHEETS[:] = [("1001", ["STEEL GENERAL NOTES,", "DESIGN CRITERIA"], "N.T.S."),
             ("3001", ["TRUSS T1", "ELEVATION AND MEMBER SCHEDULE"], "AS SHOWN"),
             ("5001", ["TRUSS T1", "JOINT DETAILS"], "1:10"),
             ("5002", ["TRUSS T1", "END OF TRUSS AND BEARING"], "1:10"),
             ("5003", ["TRUSS T1", "SITE CONNECTIONS"], "AS SHOWN"),
             ("5004", ["TRUSS T1", "FLY BRACING"], "AS SHOWN")]

LD = D["loose"][C.SPLICE_PANELS[0]]                               # loose diagonal connection
SUP = D["support"]
W_CAP, W_SADDLE, W_STIF, W_GUSSET, W_CLEAT, W_LUG = 5, 6, 6, 6, 5, 5   # fillet legs of the plate welds, mm
W_SLOTCAP = 3
SIDE_LEG = {g: WELDS[g]["legs"]["SIDE"] for g in WELDS}
# bearing seat (elevation y from the bottom-chord axis)
SAD_T, SAD_L, STIF_T = 12.0, 200.0, SUP["ts"]
Y_BP = -180.0                                                     # top of the base plate
BP_B, BP_T = SUP["B"], SUP["tp"]
ROD_E = BP_B / 2 - 40                                             # anchor rods 40 from the plate edges
GROUT = 30.0
ROD_PROJ = math.ceil((GROUT + SUP["tp"] + SUP["washer_t"] + 1.6 * SUP["d_rod"] + 7.5) / 10) * 10   # above T.O.C.
PURLIN = "C 150 x 65 x 20 x 3.2"                                   # assumed purlin (by others)


def sname(g):
    return SEC[g].name


def wipe_tag(sp, c, s, S):
    """member mark in a box that masks the lines under it"""
    w = (text_w(s, 2.0, "ANB") + 1.6) * S
    h = 3.6 * S
    sp.add_wipeout([(c[0] - w / 2, c[1] - h / 2), (c[0] + w / 2, c[1] + h / 2)])
    tag(sp, c, s, S)


# ======================================================================= 3001: half elevation 1:50
def elev_half(ox, oy):
    S = 50
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    xr = L / 2 + 350                                              # broken beyond the centre line
    for yc in (0.0, H):
        chord(sp, P, -X_OH, xr, yc, cl=False, S=S)                # outline + inner wall (fine hidden)
        line(sp, P(-X_OH - 3 * S, yc), P(xr, yc), "S-GRID")
        line(sp, P(-X_OH, yc - DC / 2), P(-X_OH, yc + DC / 2), "S-STL")        # end cap
    zbreak(sp, P(xr, -DC / 2 - 150), P(xr, H + DC / 2 + 150), S)
    for w in WEBS:
        n, g, top, bot = w
        xt, xb = NODES[top][0], NODES[bot][0]
        if max(xt, xb) <= xr - 40:
            branch(sp, P, n, layer="S-STL", cl=False, S=S)
            line(sp, P(*wp(top)), P(*wp(bot)), "S-GRID")          # member axis, work point to work point
        elif min(xt, xb) < xr:                                    # crosses the break: keep the part left of it
            lines_, a, u = branch_lines(n)
            keep = bot if xb < xt else top
            lc = abs((xr - 60 - a[1 if keep[0] == "B" else 0][0]) / u[0])
            branch(sp, P, n, cut=(keep, lc), layer="S-STL", cl=False, S=S)
            w0 = wp(keep)
            sg_ = 1 if keep[0] == "B" else -1
            line(sp, P(*w0), P(xr - 60, w0[1] + sg_ * abs((xr - 60 - w0[0]) * u[1] / u[0])), "S-GRID")
    for xs in X_SPLICE[:1]:                                       # chord flange splice
        for yc in (0.0, H):
            for x0, x1 in ((xs - FL["tp"], xs), (xs, xs + FL["tp"])):
                plate(sp, P, [(x0, yc - FL["od"] / 2), (x1, yc - FL["od"] / 2), (x1, yc + FL["od"] / 2),
                              (x0, yc + FL["od"] / 2)])
    # bearing (schematic at this scale) and the RC support
    plate(sp, P, [(-BP_B / 2, Y_BP - BP_T), (BP_B / 2, Y_BP - BP_T), (BP_B / 2, Y_BP), (-BP_B / 2, Y_BP)])
    plate(sp, P, [(-SAD_L / 2, Y_BP), (SAD_L / 2, Y_BP), (SAD_L / 2, -DC / 2), (-SAD_L / 2, -DC / 2)])
    yrc = Y_BP - BP_T - GROUT
    hatch(sp, [P(-300, yrc), P(300, yrc), P(300, yrc - 120), P(-300, yrc - 120)], "AR-CONC",
          pscale("AR-CONC", S, 2.5))                                                    # RC support
    line(sp, P(-300, yrc), P(300, yrc), "S-CONC-VIS")      # RC support, short: clear of the panel dimensions
    for x in (-300, 300):
        line(sp, P(x, yrc), P(x, yrc - 120), "S-CONC-VIS")
    zbreak(sp, P(-340, yrc - 120), P(340, yrc - 120), S)
    # centre line of the truss = line of symmetry
    xc = L / 2
    line(sp, P(xc, -DC / 2 - 700), P(xc, H + DC / 2 + 500), "S-GRID")
    for yy in (-DC / 2 - 640, H + DC / 2 + 440):
        for d_ in (-1, 1):
            line(sp, P(xc - 1.6 * S, yy + d_ * 0.8 * S), P(xc + 1.6 * S, yy + d_ * 0.8 * S), "S-ANNO")
    text(sp, "CL", P(xc, H + DC / 2 + 560), 2.0 * S, align=TA.BOTTOM_CENTER, style="ANB")
    # member marks beside their member: the candidate with the most clearance from every member and tag
    obst = [((-X_OH, yc + sg_ * DC / 2), (xr, yc + sg_ * DC / 2), 0.0) for yc in (0.0, H) for sg_ in (-1, 1)]
    for w in WEBS:
        (xt, yt), (xb, yb) = wp(w[2]), wp(w[3])
        if max(xt, xb) <= xr:
            obst.append(((xt, yt), (xb, yb), SEC[group_of(w[0])].D / 2))
    taken = []
    gap = 1.0 * S
    for w in WEBS:
        n, g, top, bot = w
        (xt, yt), (xb, yb) = wp(top), wp(bot)
        if max(xt, xb) > xr - 40:
            continue
        mk = mark_of(n)
        tw = th = 2 * tag_r(mk) * S
        Lm = math.hypot(xb - xt, yb - yt)
        u = ((xb - xt) / Lm, (yb - yt) / Lm)
        nv = (-u[1], u[0])
        off = SEC[g].D / 2 + gap + (abs(nv[0]) * tw + abs(nv[1]) * th) / 2
        cands = [(xt + f * (xb - xt) + sg_ * off * nv[0], yt + f * (yb - yt) + sg_ * off * nv[1])
                 for f in (0.3, 0.4, 0.5, 0.6, 0.7) for sg_ in (1, -1)]
        c = place_tag(cands, tw, th, [o for o in obst if o[0] != (xt, yt)], taken)
        tag(sp, P(*c), mk, S)
        taken.append((c[0], c[1], tw, th))
    xsp = X_SPLICE[0]
    for mk, x, yc, sg_ in ((CHORD_MARK["T"][0], 2.5 * A_P, H, 1), (CHORD_MARK["T"][1], 7.5 * A_P, H, 1),
                           (CHORD_MARK["B"][0], 3.5 * A_P, 0.0, -1), (CHORD_MARK["B"][1], 8.5 * A_P, 0.0, -1)):
        tag(sp, P(x, yc + sg_ * (DC / 2 + gap + tag_r(mk) * S)), mk, S)   # chords: outside, mid-panel
    # dimensions (DSC p.209: working dimensions outermost): panels, splice from the pin-end bearing, half span
    yd = -DC / 2 - 9.0 * S
    for k in range(NP // 2):
        dim(sp, P(k * A_P, -DC / 2), P((k + 1) * A_P, -DC / 2), P(0, yd), S)
    dim(sp, P(0, yd - 1.5 * S), P(xsp, yd - 1.5 * S), P(0, yd - 7 * S), S, text=f"{xsp:.0f} (FIELD SPLICE)")
    dim(sp, P(0, yd - 1.5 * S), P(L / 2, yd - 1.5 * S), P(0, yd - 14 * S), S,
        text="12500 (HALF SPAN; 25000 C/C BEARINGS)")
    dim(sp, P(xr - 120, 0), P(xr - 120, H), P(xr + 6 * S, 0), S, angle=90)
    dim(sp, P(-X_OH, H), P(0, H), P(0, H + DC / 2 + 4 * S), S, tside="L")
    # section 1/5004 at the braced node B4 / T4, looking along the truss (left)
    xc3 = 4 * A_P + 150
    cutmark(sp, P(xc3, H + DC / 2 + 2.5 * S), P(xc3, -DC / 2 - 2.5 * S), (-1, 0), "1", S, "5004", lab="side")
    # notes: row above, column at the left for the bearing
    note_cfg(yT=P(0, H + DC / 2 + 14 * S)[1], xmaxT=P(xr, 0)[0], xL=P(-X_OH - 8 * S, 0)[0], yminL=P(0, Y_BP - 300)[1])
    kt = lambda x: P(x, H + DC / 2 + 14 * S)
    leader(sp, P(X_SPLICE[0], H + FL["od"] / 2), kt(X_SPLICE[0]), "FIELD SPLICE, BOTH CHORDS (1/5003)", S, "T", 44)
    d3 = f"D{C.SPLICE_PANELS[0]}"
    (xa, ya), (xb_, yb_) = axis(d3)
    leader(sp, P(xa + 0.7 * (xb_ - xa), ya + 0.7 * (yb_ - ya)), kt(xa + 600),
           f"{mark_of(d3)}: LOOSE, SITE-BOLTED BOTH ENDS (2/5003)", S, "T", 44)
    leader(sp, P(L / 2, H + DC / 2), kt(L / 2 - 1600), f"CAMBER {D['camber']:.0f} mm AT MIDSPAN (3/3001)", S, "T", 30)
    leader(sp, P(-X_OH, H), P(-X_OH - 8 * S, H), "PL 8 END CAP (1/5002)", S, "L", 24)
    leader(sp, P(-BP_B / 2, Y_BP - BP_T / 2), P(-X_OH - 8 * S, Y_BP), "PIN BEARING (1/5002)", S, "L", 24)


# ======================================================================= 3001: key 1:200
def key_truss(ox, oy):
    S = 200
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    line(sp, P(0, 0), P(L, 0), "S-STL")
    line(sp, P(0, H), P(L, H), "S-STL")
    for w in WEBS:
        (xt, yt), (xb, yb) = NODES[w[2]], NODES[w[3]]
        line(sp, P(xt, yt), P(xb, yb), "S-STL-HIDN" if w[0] in LOOSE else "S-STL-VIS")
    for k, xs in enumerate(X_SPLICE):                              # field splices FS1, FS2 (matchmarked)
        for yc in (0, H):
            line(sp, P(xs, yc - 220), P(xs, yc + 220), "S-STL")
        text(sp, f"FS{k + 1}", P(xs + 0.8 * S, H / 2), 2.0 * S, align=TA.MIDDLE_LEFT, style="ANB")
    for k in C.BC_BRACE[1:-1]:                                     # fly braces: open triangles under the node
        x = k * A_P
        pline(sp, [P(x, -60), P(x - 1.2 * S, -60 - 2.0 * S), P(x + 1.2 * S, -60 - 2.0 * S)], "S-SYMB", close=True)
    for x, lab in ((0, "PIN"), (L, "SLOTTED")):
        pline(sp, [P(x, 0), P(x - 1.6 * S, -2.8 * S), P(x + 1.6 * S, -2.8 * S)], "S-SYMB", close=True)
        if lab == "SLOTTED":
            line(sp, P(x - 1.8 * S, -3.6 * S), P(x + 1.8 * S, -3.6 * S), "S-SYMB")
        text(sp, lab, P(x, -5.2 * S), 2.0 * S, align=TA.TOP_CENTER)
    xs = [0] + X_SPLICE + [L]
    for k, (a, b) in enumerate(zip(xs, xs[1:])):
        text(sp, f"SHOP PIECE SP{k + 1}", P((a + b) / 2, H + 2.5 * S), 2.0 * S, align=TA.BOTTOM_CENTER, style="ANB")
        dim(sp, P(a, H), P(b, H), P(0, H + 8 * S), S)
    dim(sp, P(0, 0), P(L, 0), P(0, -9 * S), S, text="25000 (SPAN, C/L BEARINGS)")
    line(sp, P(L / 2, -2 * S), P(L / 2, H + 4 * S), "S-GRID")


# ======================================================================= 5001: node details 1:10
def node_detail(ox, oy, node, cuts, end=False):
    """chord around 'node', its branches cut 'cuts[group]' from the chord face, work point, gap and e
    dimensions, weld symbols. Notes: column at the right."""
    S = 10
    sp = msp
    xn, yn = NODES[node]
    P = lambda x, y: (ox + x - xn, oy + y - yn)
    side = node[0]
    sg = -1 if side == "T" else 1                                 # toward the web
    x0, x1 = (xn - X_OH if end else xn - 420), xn + 470
    chord(sp, P, x0, x1, yn, S=S, breaks=(not end, True))
    for x in ((x1,) if end else (x0, x1)):
        chs_break(sp, P(x, yn), (1 if x == x1 else -1, 0), DC, TC_T, S)
    if end:                                                       # end cap
        plate(sp, P, [(x0 - CAP_T, yn - DC / 2), (x0, yn - DC / 2), (x0, yn + DC / 2), (x0 - CAP_T, yn + DC / 2)])
        weld_band(sp, P, (x0, yn - DC / 2), (x0, yn + DC / 2), (1.0, 0.0), W_CAP, S)        # seal fillet
    brs = sorted(branches_at(node), key=lambda b: NODES[web(b)[3 if side == "T" else 2]][0])
    ends = {}
    for b in brs:
        pts, ax = branch(sp, P, b, cut=(node, cuts[group_of(b)]), S=S)
        weld_branch(sp, P, b, node, S)
        k = 0 if side == "T" else 1
        ends[b] = (pts, ax[k])
        line(sp, P(*ax[k]), P(*wp(node)), "S-GRID")            # branch axis on to the work point
    w = wp(node)
    wp_mark(sp, P(*w), S)
    yf = FACE[side]
    # gap(s) on the chord face, inside the chord band
    foot = sorted((min(p[0 if side == "T" else 1][0] for p in ends[b][0]),
                   max(p[0 if side == "T" else 1][0] for p in ends[b][0]), b) for b in brs)
    yg = yn + sg * DC / 4
    axes = [ends[b][1][0] for b in brs] + [wp(node)[0]]              # branch axes run to the WP across the band
    for k, (a, b) in enumerate(zip(foot, foot[1:])):
        off = 3.0 * S + text_w(f"{b[0] - a[1]:.0f}", 2.0) * S / 2
        cands = {"L": a[1] - off, "R": b[0] + off}                  # text beside the gap, clear of the axes
        ts = max(cands, key=lambda k_: min(abs(cands[k_] - x) for x in axes))
        dim(sp, P(a[1], yf), P(b[0], yf), P(a[1], yg), S, tside=ts)
    # eccentricity: chord axis to work point, left of the branches
    xe = foot[0][0] - 90
    dim(sp, P(xe, yn), P(xe, w[1]), P(xe - 60, yn), S, angle=90, tside="L" if side == "T" else "R")
    text(sp, "WP", P(w[0] + 2.2 * S, w[1] - sg * 1.2 * S), 2.0 * S, align=TA.MIDDLE_LEFT)
    # set-out: the branch axes on the chord face from the panel-point line through the WP (DSC Fig 3-43)
    xs_ = sorted({round(ends[b][1][0], 1) for b in brs} - {round(xn, 1)})
    yo = yn - sg * (DC / 2 + 70)
    line(sp, P(xn, yn - sg * (DC / 2 + 90)), P(xn, yn - sg * DC / 2), "S-GRID")    # panel-point line
    yfar = yn - sg * DC / 2
    for xa_ in xs_:
        dim(sp, P(xn, yfar), P(xa_, yfar), P(xn, yo), S, tside="R" if xa_ > xn else "L")
    # weld symbols (one per member mark): side leg, all round, tail to the zone detail 4/5001 where the
    # heel / toe legs and the toe bevel are given (AWS D1.1 Fig 9.10)
    yref = yf + sg * 150
    firsts = []                                                    # one symbol per member mark: the first mark
    for f_ in foot:                                                # at its left toe, the next at its right toe
        if mark_of(f_[2]) not in [mark_of(q[2]) for q in firsts]:
            firsts.append(f_)
    if len(firsts) > 1:
        mk2 = mark_of(firsts[1][2])
        firsts[1] = max((f_ for f_ in foot if mark_of(f_[2]) == mk2), key=lambda f_: f_[1])
    for k, (lo, hi, b) in enumerate(firsts[:2]):
        g = group_of(b)
        if k == 0:
            weld(sp, P(lo, yf), P(lo - 170, yref), S, SIDE_LEG[g], all_round=True, left=True, tail="4/5001")
        else:
            weld(sp, P(hi, yf), P(hi + 260, yf + sg * 70), S, SIDE_LEG[g], all_round=True, tail="4/5001")
    # notes at the right
    xk = x1 + 150
    note_cfg(xR=P(xk, 0)[0], xL=P(x0 - 120, 0)[0])
    kr = P(xk, 0)
    R = lambda tip, s_: leader(sp, P(*tip), kr, s_, S, "R", 32)
    if end:                                                       # the cap note beside the cap, at the left
        leader(sp, P(x0 - CAP_T, yn - DC / 4), P(x0 - 120, 0), f"PL {CAP_T:.0f} END CAP (p1)", S, "L", 24)
        weld(sp, P(x0, yn + DC / 2), P(x0 - 150, yn + DC / 2 + 140), S, W_CAP, all_round=True, left=True,
             tail="SEAL")
    R((x1 - 120, yn + DC / 2 * (1 if side == "T" else -1)), f"{CHORD_MARK[side][0]} {sname('TC')} "
      "CHORD, CONTINUOUS")
    for b in brs:
        pts, a = ends[b]
        g = group_of(b)
        mid = pts[0][1] if side == "T" else pts[0][0]
        Lc = cuts[g]
        _, _, u = branch_lines(b)
        k = 0 if side == "T" else 1
        q = pts[0][k]
        sgn = 1 if side == "T" else -1
        tipb = (q[0] + sgn * u[0] * Lc * 0.6, q[1] + sgn * u[1] * Lc * 0.6)
        R(tipb, f"{mark_of(b)} {sname(g)}" + (f", θ = {theta_deg(b):.1f}°" if g in ('DE', 'DM') else ""))


def node_T(ox, oy):
    node_detail(ox, oy, "T2", {"DE": 520, "DM": 520, "VM": 420, "VE": 420})


def node_B(ox, oy):
    node_detail(ox, oy, "B2", {"DE": 520, "DM": 520, "VM": 420, "VE": 420})


def node_C(ox, oy):
    node_detail(ox, oy, f"B{NP // 2}", {"DE": 520, "DM": 520, "VM": 420, "VE": 420})


# ======================================================================= 5002: end of truss and bearing 1:10
def end_top(ox, oy):
    node_detail(ox, oy, "T0", {"DE": 560, "VE": 460}, end=True)


def anchor_rod(sp, P, x, yrc, S, embed=170):
    """anchor rod seen from the side (DSC 7, Figs 7-6 / 7-7): headed bottom end (nut + plate) in the RC,
    levelling nut under the base plate (in the grout), plate washer on the base plate, nut + lock nut on top"""
    r = SUP["d_rod"] / 2
    ub = Y_BP - BP_T                                               # underside of the base plate
    top = yrc + ROD_PROJ
    line(sp, P(x - r, top), P(x - r, yrc - embed), "S-BOLT")
    line(sp, P(x + r, top), P(x + r, yrc - embed), "S-BOLT")
    line(sp, P(x - r, top), P(x + r, top), "S-BOLT")
    nh, nw = 0.8 * SUP["d_rod"], 1.6 * SUP["d_rod"]                # nut height and width across
    ww, wt = SUP["washer"], SUP["washer_t"]
    for y0 in (Y_BP + wt, Y_BP + wt + nh):                         # nut + lock nut on the plate washer
        plate(sp, P, [(x - nw / 2, y0), (x + nw / 2, y0), (x + nw / 2, y0 + nh), (x - nw / 2, y0 + nh)], "S-BOLT")
    plate(sp, P, [(x - ww / 2, Y_BP), (x + ww / 2, Y_BP), (x + ww / 2, Y_BP + wt), (x - ww / 2, Y_BP + wt)], "S-BOLT")
    plate(sp, P, [(x - nw / 2, ub - nh), (x + nw / 2, ub - nh), (x + nw / 2, ub), (x - nw / 2, ub)], "S-BOLT")
    yb = yrc - embed                                               # head: nut + plate
    plate(sp, P, [(x - nw / 2, yb), (x + nw / 2, yb), (x + nw / 2, yb + nh), (x - nw / 2, yb + nh)], "S-BOLT")
    plate(sp, P, [(x - 30, yb - 8), (x + 30, yb - 8), (x + 30, yb), (x - 30, yb)], "S-BOLT")
    line(sp, P(x, top + 15), P(x, yb - 20), "S-CENT")


def rc_and_grout(sp, P, yrc, half, depth, S):
    hatch(sp, [P(-half, yrc), P(half, yrc), P(half, yrc - depth), P(-half, yrc - depth)], "AR-CONC",
          pscale("AR-CONC", S, 2.5))                                                    # RC support
    hatch(sp, [P(-BP_B / 2 - 20, Y_BP - BP_T), P(BP_B / 2 + 20, Y_BP - BP_T), P(BP_B / 2 + 45, yrc),
               P(-BP_B / 2 - 45, yrc)], "AR-SAND", pscale("AR-SAND", S, 0.5))           # grout
    pline(sp, [P(-BP_B / 2 - 20, Y_BP - BP_T), P(-BP_B / 2 - 45, yrc), P(BP_B / 2 + 45, yrc),
               P(BP_B / 2 + 20, Y_BP - BP_T)], "S-STL-VIS")
    line(sp, P(-half, yrc), P(half, yrc), "S-CONC-VIS")
    for x in (-half, half):
        line(sp, P(x, yrc), P(x, yrc - depth), "S-CONC-VIS")
    zbreak(sp, P(-half - 40, yrc - depth), P(half + 40, yrc - depth), S)


def bearing_elev(ox, oy):
    """bearing at the pin end B0: bottom chord end, end vertical, saddle seat, base plate, rods, 1:10"""
    S = 10
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    xr = 520
    Dv = SEC["VE"].D
    chord(sp, P, -X_OH, xr, 0.0, S=S, breaks=(False, True))
    plate(sp, P, [(-X_OH - CAP_T, -DC / 2), (-X_OH, -DC / 2), (-X_OH, DC / 2), (-X_OH - CAP_T, DC / 2)])
    weld_band(sp, P, (-X_OH, -DC / 2), (-X_OH, DC / 2), (1.0, 0.0), W_CAP, S)               # seal fillet
    chs_break(sp, P(xr, 0), (1, 0), DC, TC_T, S)
    branch(sp, P, "V0", cut=("B0", 300), S=S)
    weld_branch(sp, P, "V0", "B0", S)
    plate(sp, P, [(-SAD_L / 2, -DC / 2 - SAD_T), (SAD_L / 2, -DC / 2 - SAD_T), (SAD_L / 2, -DC / 2 + 18),
                  (-SAD_L / 2, -DC / 2 + 18)], "S-STL-VIS")       # saddle seen (wraps the chord)
    plate(sp, P, [(-SAD_L / 2, Y_BP), (SAD_L / 2, Y_BP), (SAD_L / 2, -DC / 2 - SAD_T),
                  (-SAD_L / 2, -DC / 2 - SAD_T)])                  # stiffener PL 12 in the truss plane
    plate(sp, P, [(-BP_B / 2, Y_BP - BP_T), (BP_B / 2, Y_BP - BP_T), (BP_B / 2, Y_BP), (-BP_B / 2, Y_BP)])
    weld_band(sp, P, (-SAD_L / 2, Y_BP), (SAD_L / 2, Y_BP), (0.0, 1.0), W_STIF, S)          # stiffener - base PL
    weld_band(sp, P, (-SAD_L / 2, -DC / 2 - SAD_T), (SAD_L / 2, -DC / 2 - SAD_T), (0.0, -1.0), W_STIF, S)
    weld_band(sp, P, (-SAD_L / 2, -DC / 2 + 18), (SAD_L / 2, -DC / 2 + 18), (0.0, 1.0), W_SADDLE, S)
    for sg_ in (-1.0, 1.0):                                        # saddle ends round the chord
        weld_band(sp, P, (sg_ * SAD_L / 2, -DC / 2 - SAD_T), (sg_ * SAD_L / 2, -DC / 2 + 18), (sg_, 0.0),
                  W_SADDLE, S)
    yrc = Y_BP - BP_T - GROUT
    for x in (-ROD_E, ROD_E):
        anchor_rod(sp, P, x, yrc, S)
    rc_and_grout(sp, P, yrc, 300, 200, S)
    # dimensions: from the bearing centre line (= work point of B0) and from the underside of the base plate
    line(sp, P(0, DC / 2 + 40), P(0, yrc - 240), "S-GRID")
    dim(sp, P(-X_OH - CAP_T, 0), P(-X_OH - CAP_T, Y_BP - BP_T), P(-X_OH - 330, 0), S, angle=90)
    dim(sp, P(-X_OH, DC / 2), P(-Dv / 2, DC / 2), P(0, DC / 2 + 90), S)
    # section 2/5002 through the saddle, looking left
    cutmark(sp, P(60, 440), P(60, yrc - 215), (-1, 0), "2", S, "5002")
    # weld symbols (DSC p.95 #42: every weld by symbol, never by words)
    weld(sp, P(-X_OH, DC / 2), P(-X_OH - 150, DC / 2 + 190), S, W_CAP, all_round=True, left=True, tail="SEAL")
    weld(sp, P(-Dv / 2, DC / 2 + 30), P(-X_OH + 20, DC / 2 + 300), S, SIDE_LEG["VE"], all_round=True, left=True,
         tail="4/5001")
    weld(sp, P(-SAD_L / 2 + 10, -DC / 2 + 18 + W_SADDLE / 2), P(-X_OH - 60, -30), S, W_SADDLE, all_round=True,
         left=True, tail="SEAL")
    weld(sp, [P(-SAD_L / 2 + 20, Y_BP + 3), P(-SAD_L / 2 + 20, -DC / 2 - SAD_T - 3)], P(-X_OH - 60, -130), S,
         W_STIF, side="both", left=True)
    note_cfg(xR=P(xr + 140, 0)[0])
    kr = P(xr + 140, 0)
    Rf = lambda tip, s_: leader(sp, P(*tip), kr, s_, S, "R", 40)
    Rf((0, 250), f"{mark_of('V0')} {sname('VE')}")
    Rf((xr - 80, DC / 2), f"{CHORD_MARK['B'][0]} {sname('BC')}; END CAP p1")
    Rf((SAD_L / 2, -DC / 2 - SAD_T / 2), f"SADDLE PL {SAD_T:.0f} x {SAD_L:.0f} (p2), 120°, FITTED (GAP ≤ 2 mm), "
       "CENTRED UNDER V1")
    Rf((SAD_L / 2, -DC / 2 - SAD_T - 15), f"STIFFENER PL {STIF_T:.0f} (p3)")
    Rf((BP_B / 2, Y_BP - BP_T / 2), f"BASE PL {BP_B:.0f} x {SUP['N']:.0f} x {BP_T:.0f} (p4); UNDERSIDE = "
       "BEARING LEVEL BL")
    Rf((BP_B / 2 + 32, yrc + 12), f"NON-SHRINK GROUT {GROUT:.0f} mm AFTER LEVELLING; TOP OF CONCRETE = BL - "
       f"{GROUT / 1000:.3f} m")
    Rf((ROD_E + 10, yrc - 120), f"{SUP['n_rod']}-M{SUP['d_rod']} HEADED RODS AR1, PROJECTION {ROD_PROJ:.0f} mm, SET BY "
       f"TEMPLATE; LEVELLING NUT, PL WASHER w1 {SUP['washer']} x {SUP['washer']} x {SUP['washer_t']}, NUT + LOCK "
       "NUT; EMBEDMENT AND RC BY OTHERS")


def bearing_section(ox, oy):
    """section 2 through the saddle, looking along the truss toward the pin end"""
    S = 10
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    chs_section(sp, P(0, 0), DC, TC_T * 0.93)
    Dv = SEC["VE"].D
    line(sp, P(-Dv / 2, math.sqrt((DC / 2) ** 2 - (Dv / 2) ** 2)), P(-Dv / 2, 300), "S-STL-VIS")
    line(sp, P(Dv / 2, math.sqrt((DC / 2) ** 2 - (Dv / 2) ** 2)), P(Dv / 2, 300), "S-STL-VIS")
    chs_break(sp, P(0, 300), (0, 1), Dv, SEC["VE"].t, S, "S-STL-VIS")
    r0, r1 = DC / 2, DC / 2 + SAD_T                                 # saddle: 120 deg wrap under the chord
    sp.add_arc(P(0, 0), r0, 210, 330, dxfattribs=A("S-STL"))
    sp.add_arc(P(0, 0), r1, 210, 330, dxfattribs=A("S-STL"))
    for ang in (210, 330):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        line(sp, P(r0 * c, r0 * s), P(r1 * c, r1 * s), "S-STL")
    plate(sp, P, [(-STIF_T / 2, Y_BP), (STIF_T / 2, Y_BP), (STIF_T / 2, -r1), (-STIF_T / 2, -r1)])
    ys = -math.sqrt(r1 ** 2 - (STIF_T / 2) ** 2)
    for sg_ in (-1.0, 1.0):
        weld_bead(sp, P, (sg_ * STIF_T / 2, Y_BP), (sg_, 0.0), (0.0, 1.0), W_STIF, S)     # to the base plate
        weld_bead(sp, P, (sg_ * STIF_T / 2, ys), (sg_, 0.0), (0.0, -1.0), W_STIF, S)      # to the saddle
    for ang in (210.0, 330.0):                                     # saddle edges to the chord
        c_, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        tang = (-s_, c_) if ang > 270 else (s_, -c_)               # along the chord surface, away from the saddle
        weld_bead(sp, P, (r0 * c_, r0 * s_), (c_, s_), tang, W_SADDLE, S)  # root on the chord surface
    plate(sp, P, [(-BP_B / 2, Y_BP - BP_T), (BP_B / 2, Y_BP - BP_T), (BP_B / 2, Y_BP), (-BP_B / 2, Y_BP)])
    yrc = Y_BP - BP_T - GROUT
    for x in (-ROD_E, ROD_E):
        anchor_rod(sp, P, x, yrc, S)
    rc_and_grout(sp, P, yrc, 240, 200, S)
    line(sp, P(0, 350), P(0, yrc - 240), "S-GRID")
    # welds: saddle edges to the chord (fillet both edges), stiffener to saddle and base plate (both sides)
    a3 = math.radians(210)
    weld(sp, P(r0 * math.cos(a3) - 4, r0 * math.sin(a3) + 6), P(-230, -40), S, W_SADDLE, all_round=True,
         left=True, tail="SEAL")
    weld(sp, [P(-STIF_T / 2 - 3, Y_BP + 4), P(-STIF_T / 2 - 3, ys - 4)], P(-200, -150), S, W_STIF, side="both",
         left=True)
    note_cfg(xR=P(300, 0)[0])
    kr = P(300, 0)
    Rf = lambda tip, s_: leader(sp, P(*tip), kr, s_, S, "R", 34)
    Rf((r1 * math.cos(math.radians(320)), r1 * math.sin(math.radians(320))), f"SADDLE PL {SAD_T:.0f} (p2), 120°")
    Rf((STIF_T / 2, -r1 - 18), f"STIFFENER PL {STIF_T:.0f} (p3)")
    Rf((BP_B / 2, Y_BP - BP_T / 2), f"BASE PL {BP_T:.0f} (p4 / p5)")


def base_plans(ox, oy):
    """base plates, plan: pin end (oversized holes, plate washers welded on site after setting) and sliding end
    (long slots along the truss, loose plate washers, double nuts)"""
    S = 10
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    hole_d, slot_l, ww = SUP["hole"], SUP["slot"], SUP["washer"]
    for k, (xo, kind) in enumerate(((0, "PIN"), (330, "SLIDE"))):
        Q = lambda x, y: P(xo + x, y)
        plate(sp, Q, [(-BP_B / 2, -SUP["N"] / 2), (BP_B / 2, -SUP["N"] / 2), (BP_B / 2, SUP["N"] / 2),
                      (-BP_B / 2, SUP["N"] / 2)])
        plate(sp, Q, [(-SAD_L / 2, -STIF_T / 2), (SAD_L / 2, -STIF_T / 2), (SAD_L / 2, STIF_T / 2),
                      (-SAD_L / 2, STIF_T / 2)], "S-STL-HIDN")
        line(sp, Q(-BP_B / 2 - 40, 0), Q(BP_B / 2 + 40, 0), "S-GRID")
        line(sp, Q(0, -SUP["N"] / 2 - 40), Q(0, SUP["N"] / 2 + 30), "S-GRID")
        for x in (-ROD_E, ROD_E):
            for y in (-ROD_E, ROD_E):
                if kind == "PIN":
                    hole(sp, Q(x, y), hole_d, S)
                else:
                    slot(sp, Q(x, y), hole_d, slot_l, S)
                plate(sp, Q, [(x - ww / 2, y - ww / 2), (x + ww / 2, y - ww / 2), (x + ww / 2, y + ww / 2),
                              (x - ww / 2, y + ww / 2)], "S-STL-VIS")                 # plate washer
                sp.add_circle(Q(x, y), SUP["d_rod"] / 2, dxfattribs=A("S-BOLT"))      # rod
        text(sp, "PIN END (p4)" if kind == "PIN" else "SLIDING END (p5)", Q(0, SUP["N"] / 2 + 150), 2.0 * S,
             align=TA.BOTTOM_CENTER, style="ANB")
        if kind == "PIN":
            dim(sp, Q(-BP_B / 2, SUP["N"] / 2), Q(-ROD_E, SUP["N"] / 2), Q(0, SUP["N"] / 2 + 70), S, tside="L")
        dim(sp, Q(-ROD_E, SUP["N"] / 2), Q(ROD_E, SUP["N"] / 2), Q(0, SUP["N"] / 2 + 70), S)
        dim(sp, Q(-BP_B / 2, SUP["N"] / 2), Q(BP_B / 2, SUP["N"] / 2), Q(0, SUP["N"] / 2 + 120), S)
    dim(sp, P(330 + BP_B / 2, -SUP["N"] / 2), P(330 + BP_B / 2, SUP["N"] / 2), P(330 + BP_B / 2 + 90, 0), S, angle=90)
    text(sp, "TRUSS AXIS HORIZONTAL", P(165, -SUP["N"] / 2 - 60), 2.0 * S, align=TA.TOP_CENTER)
    # pin end: plate washers welded to the base plate on site after the rods are set (shear by the rods)
    weld(sp, P(-ROD_E - ww / 2, ROD_E + ww / 2 - 10), P(-BP_B / 2 - 90, SUP["N"] / 2 + 10), S, 5,
         all_round=True, field=True, left=True, tail="w1")
    note_cfg(yB=P(0, -SUP["N"] / 2 - 200)[1])
    kb = lambda x: P(x, -SUP["N"] / 2 - 200)
    leader(sp, P(-ROD_E, -ROD_E), kb(-ROD_E - 60),
           f"Ø{hole_d} HOLES; PL WASHERS w1 {ww} x {ww} x {SUP['washer_t']}, Ø{SUP['d_rod'] + 2} HOLE, SITE "
           "WELDED AFTER SETTING", S, "B", 34, bolt=hole_d)
    leader(sp, P(330 + ROD_E + slot_l / 2 - 2, -ROD_E), kb(330 + 40),
           f"SLOTS {hole_d} x {slot_l} (±{SUP['move']:.0f} mm: THERMAL ±{SUP['thermal']:.1f} mm + CHORD STRETCH "
           f"{SUP['stretch']:.1f} mm); PL WASHERS w2 AS w1, NOT WELDED; RODS CENTRED; DOUBLE NUTS, SNUG", S, "B", 34)


# ======================================================================= 5003: site connections
def splice_elev(ox, oy):
    """chord flange splice, elevation 1:5 (DG24 5.4, Fig 5-4: a = b)"""
    S = 5
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    tp, od, bc = FL["tp"], FL["od"], FL["bc"]
    xa, xb = -200, 200
    for x0, x1, br in ((xa, -tp, (True, False)), (tp, xb, (False, True))):
        chord(sp, P, x0, x1, 0.0, cl=False, S=S, breaks=br)
    for x in (xa, xb):
        chs_break(sp, P(x, 0), (1 if x == xb else -1, 0), DC, TC_T, S)
    line(sp, P(xa - 15, 0), P(xb + 15, 0), "S-GRID")
    plate(sp, P, [(-tp, -od / 2), (0, -od / 2), (0, od / 2), (-tp, od / 2)])
    plate(sp, P, [(0, -od / 2), (tp, -od / 2), (tp, od / 2), (0, od / 2)])
    wf = FL["weld"]
    for xf, dx in ((-tp, -1.0), (tp, 1.0)):                        # flange-to-chord fillet round the chord
        weld_region(sp, P, [(xf, DC / 2 + wf), (xf + dx * wf, DC / 2), (xf + dx * wf, -DC / 2), (xf, -DC / 2 - wf)],
                    wf, S)
    db = FL["db"]
    for y in (bc / 2, -bc / 2):                                      # bolts seen at top and bottom of the PCD
        hh, nh, w = 0.65 * db, 0.8 * db, 1.6 * db
        plate(sp, P, [(-tp - hh, y - w / 2), (-tp, y - w / 2), (-tp, y + w / 2), (-tp - hh, y + w / 2)], "S-BOLT")
        plate(sp, P, [(tp + 4, y - w / 2), (tp + 4 + nh, y - w / 2), (tp + 4 + nh, y + w / 2), (tp + 4, y + w / 2)],
              "S-BOLT")
        plate(sp, P, [(tp, y - 0.9 * db), (tp + 4, y - 0.9 * db), (tp + 4, y + 0.9 * db), (tp, y + 0.9 * db)],
              "S-BOLT")                                             # hardened washer under the nut
        xe = -tp + FL["bolt_len"]                                  # shank end (length under the head)
        line(sp, P(tp + 4 + nh, y - db / 2), P(xe, y - db / 2), "S-BOLT")
        line(sp, P(tp + 4 + nh, y + db / 2), P(xe, y + db / 2), "S-BOLT")
        line(sp, P(xe, y - db / 2), P(xe, y + db / 2), "S-BOLT")
        line(sp, P(-tp - hh - 8, y), P(xe + 8, y), "S-CENT")
    dim(sp, P(xb - 40, -od / 2), P(xb - 40, od / 2), P(xb + 70, 0), S, angle=90, text=f"Ø{od:.0f}")
    dim(sp, P(xb - 40, -bc / 2), P(xb - 40, bc / 2), P(xb + 40, 0), S, angle=90, text=f"PCD {bc:.0f}")
    dim(sp, P(-tp, -od / 2), P(tp, -od / 2), P(0, -od / 2 - 50), S, tside="R")
    xd = -tp - 70                                                   # a = b: chord face - bolt - plate edge
    dim(sp, P(-tp, DC / 2), P(-tp, bc / 2), P(xd, 0), S, angle=90, tside="L", text=f"b = {FL['b']:.0f}")
    dim(sp, P(-tp, bc / 2), P(-tp, od / 2), P(xd, 0), S, angle=90, tside="R", text=f"a = {FL['a']:.0f}")
    weld(sp, P(tp + wf - 1, -DC / 2 - 1), P(tp + 110, -DC / 2 - 150), S, FL["weld"], all_round=True, ndt="MT",
         tail="TYP. EVERY FLANGE")
    note_cfg(xL=P(xa - 80, 0)[0])
    kl = P(xa - 80, 0)
    Lf = lambda tip, s_: leader(sp, P(*tip), kl, s_, S, "L", 34)
    Lf((-tp / 2, -od / 2 + 20), f"FLANGE PL {tp:.0f}, Ø{od:.0f} (p6), SOLID; FACES MACHINED FLAT AFTER WELDING, "
       "FULL CONTACT; HOLES DRILLED IN PAIRS, MATCHMARKED")
    Lf((-tp - 6, -bc / 2), f"{FL['n']}-M{db} x {FL['bolt_len']} GRADE 8.8, HARDENED WASHER UNDER NUT, FULLY "
       "PRETENSIONED (TABLE 4, 1001)")
    Lf((xa + 60, -DC / 2), f"CHORD {sname('TC')} ({CHORD_MARK['T'][0]} / {CHORD_MARK['T'][1]}, "
       f"{CHORD_MARK['B'][0]} / {CHORD_MARK['B'][1]})")


def flange_face(ox, oy):
    """flange plate seen from the joint face, 1:5"""
    S = 5
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    od, bc = FL["od"], FL["bc"]
    sp.add_circle(P(0, 0), od / 2, dxfattribs=A("S-STL"))
    sp.add_circle(P(0, 0), DC / 2, dxfattribs=A("S-STL-HIDN"))
    sp.add_circle(P(0, 0), bc / 2, dxfattribs=A("S-CENT"))
    for k in range(FL["n"]):
        a = math.radians(k * 360 / FL["n"])
        hole(sp, P(bc / 2 * math.cos(a), bc / 2 * math.sin(a)), FL["db"] + 2, S)
    line(sp, P(-od / 2 - 20, 0), P(od / 2 + 20, 0), "S-GRID")
    line(sp, P(0, -od / 2 - 20), P(0, od / 2 + 20), "S-GRID")
    note_cfg(xR=P(od / 2 + 90, 0)[0])
    kr = P(od / 2 + 90, 0)
    Rf = lambda tip, s_: leader(sp, P(*tip), kr, s_, S, "R", 30)
    leader(sp, P(bc / 2 * math.cos(math.radians(60)), bc / 2 * math.sin(math.radians(60))), kr,
           f"{FL['n']}-Ø{FL['db'] + 2} HOLES ON PCD {bc:.0f}, EQUALLY SPACED, TWO ON THE HORIZONTAL AXIS (SAME ON "
           "EVERY FLANGE)", S, "R", 30, bolt=FL["db"] + 2)
    Rf((DC / 2 * 0.7, -DC / 2 * 0.7), f"CHORD OUTLINE Ø{DC:g} (BEHIND)")


def _hull(pts):
    pts = sorted(set(pts))
    lo, up = [], []
    for q in pts:
        while len(lo) >= 2 and ((lo[-1][0] - lo[-2][0]) * (q[1] - lo[-2][1])
                                - (lo[-1][1] - lo[-2][1]) * (q[0] - lo[-2][0])) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(up) >= 2 and ((up[-1][0] - up[-2][0]) * (q[1] - up[-2][1])
                                - (up[-1][1] - up[-2][1]) * (q[0] - up[-2][0])) <= 0:
            up.pop()
        up.append(q)
    return lo[:-1] + up[:-1]


def _pip(q, poly):
    inside, j = False, len(poly) - 1
    for i in range(len(poly)):
        (xi, yi), (xj, yj) = poly[i], poly[j]
        if (yi > q[1]) != (yj > q[1]) and q[0] < (xj - xi) * (q[1] - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def behind(sp, P, poly, front, layer="S-STL", hidden="S-STL-HIDN"):
    """closed outline 'poly' of a part lying behind the part 'front' (convex): visible where clear of it, hidden
    (dashed) where the front part covers it"""
    for a, b in zip(poly, poly[1:] + poly[:1]):
        ts = [0.0, 1.0]
        for c, d in zip(front, front[1:] + front[:1]):           # cuts at the front part's edges
            den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
            if abs(den) < 1e-12:
                continue
            t = ((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0])) / den
            v = ((c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0])) / den
            if 1e-9 < t < 1 - 1e-9 and -1e-9 <= v <= 1 + 1e-9:
                ts.append(t)
        ts.sort()
        for t0, t1 in zip(ts, ts[1:]):
            if t1 - t0 < 1e-9:
                continue
            p0 = (a[0] + t0 * (b[0] - a[0]), a[1] + t0 * (b[1] - a[1]))
            p1 = (a[0] + t1 * (b[0] - a[0]), a[1] + t1 * (b[1] - a[1]))
            mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
            line(sp, P(*p0), P(*p1), hidden if _pip(mid, front) else layer)


def loose_conn(ox, oy):
    """loose diagonal to the bottom chord (the top end is the same), 1:10. Gusset PL welded to the chord, 10 off
    the truss plane; knife PL slotted into the tube end (on the truss plane) and lapped on the gusset with 2 bolts
    on the diagonal axis (DG24 5.3, Ex 5.2)"""
    S = 10
    sp = msp
    n = f"D{C.SPLICE_PANELS[0]}"
    _, _, top, bot = web(n)
    xn, yn = NODES[bot]
    P = lambda x, y: (ox + x - xn, oy + y - yn)
    x0, x1 = xn - 420, xn + 380
    chord(sp, P, x0, x1, yn, S=S, breaks=(True, True))
    for x in (x0, x1):
        chs_break(sp, P(x, yn), (1 if x == x1 else -1, 0), DC, TC_T, S)
    v = f"V{int(bot[1:])}"
    branch(sp, P, v, cut=(bot, 380), S=S)
    weld_branch(sp, P, v, bot, S)
    _, a, u = branch_lines(n)
    ua = (-u[0], -u[1])                                            # up the diagonal from the chord
    nv = (-ua[1], ua[0])
    pf = a[1]                                                       # diagonal axis on the chord face
    at = lambda sa, sn=0.0: (pf[0] + sa * ua[0] + sn * nv[0], pf[1] + sa * ua[1] + sn * nv[1])
    tpl, db, e_, hw = LD["tp"], LD["db"], LD["e"], LD["hw"]
    s1 = 90.0                                                       # first bolt from the chord face
    s2 = s1 + LD["s"]
    s_k0 = s1 - e_                                                  # knife plate end at the chord
    s_t0 = s2 + e_ + 20.0                                           # tube end: 20 clear of the gusset
    s_k1 = s_t0 + LD["lw"]                                          # knife plate end inside the tube
    Db = SEC[group_of(n)].D
    tb = SEC[group_of(n)].t
    vleft = NODES[bot][0] - SEC["VM"].D / 2
    # gusset: welded edge LD["lp"] long on the chord face, ending 20 clear of the vertical, + the bolt zone
    xg1 = min(pf[0] + 60, vleft - 20)
    fin = _hull([(xg1 - LD["lp"], FACE["B"]), (xg1, FACE["B"]),
                 at(s_k0, -hw - 5), at(s2 + e_, -hw - 5), at(s2 + e_, hw + 5), at(s_k0, hw + 5)])
    fin = [q for q in fin if q[1] >= FACE["B"] - 1e-6]
    knife_vis = [at(s_k0, -hw), at(s_t0, -hw), at(s_t0, hw), at(s_k0, hw)]        # the knife plate, in front
    behind(sp, P, fin, knife_vis)
    base = sorted(q[0] for q in fin if abs(q[1] - FACE["B"]) < 1e-6)
    xa_, xb_ = base[0], base[-1]
    weld_band(sp, P, (xa_, FACE["B"]), (xb_, FACE["B"]), (0.0, 1.0), W_GUSSET, S)        # gusset - chord
    # knife plate: visible outside the tube, hidden inside it
    k = [at(s_k0, -hw), at(s_t0, -hw), at(s_t0, hw), at(s_k0, hw)]
    pline(sp, [P(*q) for q in (k[1], k[0], k[3], k[2])], "S-STL")
    pline(sp, [P(*at(s_t0, -hw)), P(*at(s_k1, -hw)), P(*at(s_k1, hw)), P(*at(s_t0, hw))], "S-STL-HIDN")
    # tube from its end (sealed by a slotted PL 3 cap) up to a break, with the inner wall
    s_t1 = s_t0 + 520
    pb = at(s_t1)
    for sg_ in (1, -1):
        line(sp, P(*at(s_t0, sg_ * Db / 2)), P(*at(s_t1, sg_ * Db / 2)), "S-STL")
        # nv of the break (toward ua) = (-ua_y, ua_x) = nv here, so the offset keeps its sign
        line(sp, P(*at(s_t0, sg_ * (Db / 2 - tb))), P(*break_point(pb, ua, Db, sg_ * (Db / 2 - tb))), "S-STL-WALL")
    plate(sp, P, [at(s_t0 - 3, -Db / 2), at(s_t0, -Db / 2), at(s_t0, Db / 2), at(s_t0 - 3, Db / 2)])   # cap p9
    chs_break(sp, P(*at(s_t1)), ua, Db, tb, S)
    wk = max(LD["w"], WELD_MIN * S)                                # knife plate - tube: fillets along the slot
    weld_region(sp, P, [at(s_t0, -wk), at(s_t0 + LD["lw"], -wk), at(s_t0 + LD["lw"], wk), at(s_t0, wk)], wk, S)
    for sb in (s1, s2):
        hole(sp, P(*at(sb)), db + 2, S)
    line(sp, P(*at(-30)), P(*at(s_t1 + 40)), "S-GRID")
    # dimensions along the diagonal, on the side away from the chord: face - bolt - bolt - gusset end - tube end,
    # slot weld length
    ang = math.degrees(math.atan2(u[1], u[0]))
    side = -1 if nv[1] < 0 else 1                                  # the normal pointing up, away from the chord
    dim(sp, P(*at(s_t0, -side * Db / 2)), P(*at(s_k1, -side * Db / 2)), P(*at(s_t0, -side * (Db / 2 + 50))), S,
        angle=ang)
    # welds: gusset to the chord both sides; knife plate in the slot both sides, length; tube cap all round
    xl = pf[0] - 250                                               # symbols in the free corner, left
    weld(sp, P(xa_ + 10, FACE["B"] + 1), P(xl + 60, FACE["B"] + 60), S, W_GUSSET, side="both", left=True)
    weld(sp, P(*at(s_t0 - 1.5, -side * (Db / 2 - 4))), P(xl, FACE["B"] + 150), S, W_SLOTCAP, all_round=True,
         left=True, tail="SEAL")
    weld(sp, P(*at(s_t0 + LD["lw"] * 0.6, -side * 2)), P(xl, FACE["B"] + 270), S, LD["w"], side="both",
         length=LD["lw"], left=True, tail="2 EDGES")
    hh = axis_length(n) - 2 * s1                                    # hole to hole of the loose diagonal
    note_cfg(xR=P(x1 + 150, 0)[0])
    kr = P(x1 + 150, 0)
    Rf = lambda tip, s_: leader(sp, P(*tip), kr, s_, S, "R", 34)
    Rf(at((s_t0 + s_t1) / 2, side * Db / 2), f"{mark_of(n)} {sname(group_of(n))}, LOOSE (2 PER TRUSS): SLOTTED "
       f"{LD['slot']} mm WIDE x {LD['lw'] + 5} mm LONG BOTH ENDS; HOLES {hh:.0f} mm C/C END TO END")
    Rf(at(s2 + e_ * 0.5, side * hw), f"KNIFE PL {tpl:.0f} x {2 * hw:.0f} (p7) ON THE TRUSS PLANE; "
       f"TUBE END CAP PL 3 (p9), SLOTTED")
    leader(sp, P(*at(s1)), kr, f"{LD['n']}-M{db} x {LD['bolt_len']} GRADE 8.8 SNUG-TIGHT, Ø{db + 2} HOLES ON THE "
           f"AXIS: FIRST {s1:.0f} mm FROM THE CHORD FACE, PITCH {LD['s']:.0f} mm; TUBE END {s_t0 - s2:.0f} mm "
           "BEYOND",
           S, "R", 34, bolt=db + 2)
    ge = at(s_k0, side * (hw + 5))                                # gusset: its right edge, mid-way
    Rf(((xb_ + ge[0]) / 2, (FACE["B"] + ge[1]) / 2), f"GUSSET PL {tpl:.0f} (p8), {LD['lp']:.0f} mm LONG ON THE CHORD, WELDED {tpl:.0f} mm OFF THE "
       "TRUSS PLANE SO THE KNIFE PL LAPS ON IT; SAME AT THE TOP CHORD")
    Rf((x1 - 100, yn - DC / 2), f"{CHORD_MARK['B'][0]} {sname('BC')}")


def hide_under(sp, P, pts, fronts, layer, hidden="S-STL-HIDN", closed=False):
    """polyline 'pts' of a part lying behind the convex parts 'fronts': solid where clear, hidden where covered"""
    segs = list(zip(pts, pts[1:] + (pts[:1] if closed else [])))
    for a, b in segs:
        ts = [0.0, 1.0]
        for front in fronts:
            for c, d in zip(front, front[1:] + front[:1]):
                den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
                if abs(den) < 1e-12:
                    continue
                t = ((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0])) / den
                v = ((c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0])) / den
                if 1e-9 < t < 1 - 1e-9 and -1e-9 <= v <= 1 + 1e-9:
                    ts.append(t)
        ts.sort()
        for t0, t1 in zip(ts, ts[1:]):
            if t1 - t0 < 1e-9:
                continue
            p0 = (a[0] + t0 * (b[0] - a[0]), a[1] + t0 * (b[1] - a[1]))
            p1 = (a[0] + t1 * (b[0] - a[0]), a[1] + t1 * (b[1] - a[1]))
            mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
            line(sp, P(*p0), P(*p1), hidden if any(_pip(mid, f) for f in fronts) else layer)


def angle_strip(sp, P, o, u, s0, s1, b, t, g, layer="S-STL-VIS", cut0=False, cut1=False, S=10):
    """equal angle seen on its flat leg (the other leg toward the viewer): heel and toe edges, the thickness line
    of the outstanding leg at the heel, square ends (a broken end - cut0 / cut1 - gets a break line instead);
    o = a point on the gauge line (g from the heel), u = unit vector along it. Returns the outline"""
    n = (-u[1], u[0])                                              # heel side
    Q = lambda s, off: (o[0] + s * u[0] + off * n[0], o[1] + s * u[1] + off * n[1])
    out = [Q(s0, g), Q(s1, g), Q(s1, g - b), Q(s0, g - b)]
    line(sp, P(*out[0]), P(*out[1]), layer)
    line(sp, P(*out[3]), P(*out[2]), layer)
    line(sp, P(*Q(s0, g - t)), P(*Q(s1, g - t)), layer)           # outstanding leg, seen edge-on
    for s, cut, (a, c) in ((s0, cut0, (out[0], out[3])), (s1, cut1, (out[1], out[2]))):
        if cut:
            zbreak(sp, P(*Q(s, g + 12)), P(*Q(s, g - b - 12)), S)
        else:
            line(sp, P(*a), P(*c), layer)
    return out


def _fb():
    """fly-brace geometry (calc_truss.fly_brace): right brace gauge line from the lug hole L0 at F, purlin bolts B1,
    B2, the work point WP where the two gauge lines meet on the truss centre line, cleat and lug outlines"""
    FB = D["fly"]
    R = DC / 2
    th = math.radians(FB["F"])
    u = (math.cos(th), math.sin(th))
    hx = C.FB_HOLE_X
    L0 = (hx, FB["y_h"])
    B1 = (L0[0] + u[0] * FB["Lg"], L0[1] + u[1] * FB["Lg"])
    B2 = (B1[0] + u[0] * C.FB_PITCH, B1[1] + u[1] * C.FB_PITCH)
    yb = H + R + C.PURLIN_GAP
    cw, ctop = 50.0, H + R + 165.0
    arc_t = [(x, H + math.sqrt(R * R - x * x)) for x in [-cw + 10 * k for k in range(11)]]
    lw, ld = 75.0, L0[1] - 35.0
    arc_b = [(x, -math.sqrt(R * R - x * x)) for x in [lw - 15 * k for k in range(11)]]
    return dict(FB=FB, R=R, th=th, u=u, uL=(-u[0], u[1]), hx=hx, L0=L0, L0l=(-hx, L0[1]), B1=B1, B2=B2,
                WP=(0.0, L0[1] - hx * math.tan(th)), yb=yb, cw=cw, ctop=ctop, arc_t=arc_t,
                cleat=arc_t + [(cw, ctop), (-cw, ctop)], lw=lw, ld=ld, arc_b=arc_b,
                lug=arc_b + [(-lw, ld + 20), (-lw + 20, ld), (lw - 20, ld), (lw, ld + 20)])


def _fb_angle_F(sp, P, g, rr, S):
    """angle F between the brace gauge line and the purlin direction, measured at the work point"""
    WP, F = g["WP"], g["FB"]["F"]
    line(sp, P(WP[0] + 0.12 * rr, WP[1]), P(WP[0] + rr * 1.2, WP[1]), "S-ANNO")
    sp.add_arc(P(*WP), rr, 0, F, dxfattribs=A("S-ANNO"))
    for a0, a1 in ((0.0, 4.0), (F, F - 4.0)):
        tip = (WP[0] + rr * math.cos(math.radians(a0)), WP[1] + rr * math.sin(math.radians(a0)))
        frm = (WP[0] + rr * math.cos(math.radians(a1)), WP[1] + rr * math.sin(math.radians(a1)))
        arrowhead(sp, P(*tip), P(*frm), 2.0 * S)
    am = math.radians(F / 2)
    text(sp, f"F = {F:.0f}°", P(WP[0] + (rr + 1.2 * S) * math.cos(am), WP[1] + (rr + 1.2 * S) * math.sin(am)),
         2.0 * S, align=TA.MIDDLE_LEFT)


def cross_section(ox, oy):
    """section 3 at a braced node (B4 / T4), looking along the truss toward the pin end, symmetrical about the
    truss centre line (right half; the left brace broken off). After Beca SE-1505 details A / G: fly brace FB1
    from a lug under the bottom chord to the purlin web at F = 45 deg, gauge lines meeting at the work point on
    the truss centre line. The two ends are detailed at 1:5 on 2 / 3. 1:20"""
    S = 20
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    g = _fb()
    FB, R, u, uL = g["FB"], g["R"], g["u"], g["uL"]
    xe = g["B2"][0] + 330                                          # purlin broken clear of the callout circle
    chs_section(sp, P(0, H), DC, TC_T * 0.93)
    chs_section(sp, P(0, 0), DC, TC_T * 0.93)
    Dv = SEC["VM"].D
    for x in (-Dv / 2, Dv / 2):
        line(sp, P(x, R), P(x, H - R), "S-STL-VIS")
    pline(sp, [P(*q) for q in g["cleat"]], "S-STL", close=True)
    briR = angle_strip(sp, P, g["L0"], u, -C.FB_EDGE, FB["Lg"] + C.FB_PITCH + C.FB_EDGE, FB["b"], FB["t"],
                       FB["gauge"], S=S)
    briL = angle_strip(sp, P, g["L0l"], uL, -C.FB_EDGE, 420.0, FB["b"], FB["t"], FB["b"] - FB["gauge"], cut1=True,
                       S=S)
    hide_under(sp, P, g["lug"], [briR, briL], "S-STL", closed=True)
    yb = g["yb"]
    for y in (yb, yb + 150):
        hide_under(sp, P, [(-300, y), (xe, y)], [g["cleat"], briR], "S-STL-NF")
    for x in (-300, xe):
        zbreak(sp, P(x, yb - 10), P(x, yb + 160), S)
    # the purlin is named on itself, in its web band between the cleat and the callout (annotation guide 9.8)
    for k, s_ in enumerate((f"PURLIN {PURLIN}", "(BY OTHERS) AT EVERY TOP NODE")):
        text(sp, s_, P(g["cw"] + 8 * S, yb + 75 + (0.5 - k) * 3.33 * S), 2.0 * S, align=TA.MIDDLE_LEFT)
    WP = g["WP"]
    mid = (g["L0l"][0] + uL[0] * 420, g["L0l"][1] + uL[1] * 420)
    line(sp, P(*WP), P(g["B2"][0] + u[0] * 60, g["B2"][1] + u[1] * 60), "S-GRID")
    line(sp, P(*WP), P(*mid), "S-GRID")
    line(sp, P(0, WP[1] - 60), P(0, g["ctop"] + 60), "S-GRID")
    wp_mark(sp, P(*WP), S)
    _fb_angle_F(sp, P, g, 340.0, S)
    # the two ends, enlarged on 2 / 3: dashed callout circles, leaders onto their edges
    cl_lug = detail_callout(sp, P, (g["L0"][0] + 40, g["L0"][1] + 30), 230, S)
    cl_pur = detail_callout(sp, P, (g["B1"][0] + 10, g["B1"][1] + 30), 230, S, at=-70.0)   # bottom, clear
    note_cfg(xR=P(xe + 150, 0)[0], yT=P(0, g["ctop"] + 12 * S)[1], xmaxT=P(xe, 0)[0])
    kr = P(xe + 150, 0)
    Rf = lambda tip, s_: leader(sp, P(*tip), kr, s_, S, "R", 28)
    nR = (-u[1], u[0])
    Rf(cl_pur, "DETAIL 3/5004 - FB1 PURLIN END")
    leader(sp, P(-g["cw"] + 15, g["ctop"]), P(-g["cw"] + 15, g["ctop"] + 12 * S), "CLEAT PL 8 x 100 x 180 (p10), "
           "FACE-ON, BASE PROFILED TO THE CHORD; 2-M12 4.6/S (PURLIN BY OTHERS)", S, "T", 60)
    mb = (g["L0"][0] + u[0] * FB["Lg"] * 0.55 + nR[0] * FB["gauge"],
          g["L0"][1] + u[1] * FB["Lg"] * 0.55 + nR[1] * FB["gauge"])
    Rf(mb, f"FLY BRACE FB1 {FB['name']} (TABLE 2), BOTH SIDES OF THE TRUSS AT EVERY 4TH BOTTOM PANEL POINT; "
       "AT THE END OF THE PURLIN LAP IF F IS 35° - 55°, OTHERWISE F = 45° AS SHOWN")
    Rf((Dv / 2, H / 2), f"{mark_of('V4')} {sname('VM')}")
    Rf(cl_lug, "DETAIL 2/5004 - FB1 LUG END")


def fb_lug(ox, oy):
    """2/5004: fly braces to the lug under the bottom chord, 1:5"""
    S = 5
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    g = _fb()
    FB, R, u, uL = g["FB"], g["R"], g["u"], g["uL"]
    chs_section(sp, P(0, 0), DC, TC_T * 0.93)
    sr = 200.0
    briR = angle_strip(sp, P, g["L0"], u, -C.FB_EDGE, sr, FB["b"], FB["t"], FB["gauge"], cut1=True, S=S)
    briL = angle_strip(sp, P, g["L0l"], uL, -C.FB_EDGE, sr, FB["b"], FB["t"], FB["b"] - FB["gauge"], cut1=True,
                       S=S)
    hide_under(sp, P, g["lug"], [briR, briL], "S-STL", closed=True)
    weld_region(sp, P, g["arc_b"] + [(q[0], q[1] - W_LUG) for q in reversed(g["arc_b"])], W_LUG, S)
    for c in (g["L0"], g["L0l"]):
        hole(sp, P(*c), FB["db"] + 2, S)
    WP = g["WP"]
    for o, uu in ((g["L0"], u), (g["L0l"], uL)):
        line(sp, P(*WP), P(o[0] + uu[0] * (sr + 30), o[1] + uu[1] * (sr + 30)), "S-GRID")
    line(sp, P(0, WP[1] - 40), P(0, R + 40), "S-GRID")
    wp_mark(sp, P(*WP), S)
    _fb_angle_F(sp, P, g, 170.0, S)
    ld = g["ld"]
    dim(sp, P(0, ld), P(g["hx"], ld), P(0, ld - 50), S, tside="R")
    dim(sp, P(-g["lw"], ld), P(g["lw"], ld), P(0, ld - 115), S)
    dim(sp, P(-g["lw"] - 30, -R), P(-g["lw"] - 30, g["L0"][1]), P(-g["lw"] - 60, 0), S, angle=90, tside="L")
    weld(sp, P(-g["lw"] + 6, -math.sqrt(R * R - (g["lw"] - 6) ** 2) - 2), P(-g["lw"] - 110, 40), S, W_LUG,
         side="both", left=True)
    note_cfg(xR=P(sr + 90, 0)[0])
    kr = P(sr + 90, 0)
    leader(sp, P(*g["L0"]), kr, f"1-M{FB['db']} x {C.bolt_length(FB['t'] + 8, FB['db'], 1)} 8.8/S PER BRACE, "
           f"Ø{FB['db'] + 2} HOLES", S, "R", 26, bolt=FB["db"] + 2)
    leader(sp, P(g["lw"], ld + 30), kr, f"LUG PL 8 x {2 * g['lw']:.0f} x {-ld - R:.0f} (p11), TOP PROFILED TO THE "
           "CHORD", S, "R", 26)
    nR = (-u[1], u[0])
    leader(sp, P(g["L0"][0] + u[0] * 200 + nR[0] * FB["gauge"], g["L0"][1] + u[1] * 200 + nR[1] * FB["gauge"]),
           kr, f"FB1 {FB['name']}, GAUGE LINE {FB['gauge']} mm FROM THE HEEL", S, "R", 26)
    leader(sp, P(R * 0.7, R * 0.7), kr, f"{CHORD_MARK['B'][0]} {sname('BC')}", S, "R", 26)


def fb_purlin(ox, oy):
    """3/5004: fly brace to the purlin web (purlin by others), 1:5"""
    S = 5
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    g = _fb()
    FB, R, u = g["FB"], g["R"], g["u"]
    B1, B2, yb = g["B1"], g["B2"], g["yb"]
    s_end = FB["Lg"] + C.FB_PITCH + C.FB_EDGE
    s_cut = FB["Lg"] - 230
    briR = angle_strip(sp, P, g["L0"], u, s_cut, s_end, FB["b"], FB["t"], FB["gauge"], cut0=True, S=S)
    x0, x1 = B1[0] - 330, B2[0] + 120
    for y in (yb, yb + 150):
        hide_under(sp, P, [(x0, y), (x1, y)], [briR], "S-STL-NF")
    for y in (yb + 20, yb + 130):
        line(sp, P(x0, y), P(x1, y), "S-STL-HIDN")
    for x in (x0, x1):
        zbreak(sp, P(x, yb - 10), P(x, yb + 160), S)
    for c in (B1, B2):
        hole(sp, P(*c), FB["db"] + 2, S)
    line(sp, P(B1[0] - u[0] * 260, B1[1] - u[1] * 260), P(B2[0] + u[0] * 60, B2[1] + u[1] * 60), "S-GRID")
    nv = (-u[1], u[0])
    dim(sp, P(x0 + 40, yb), P(x0 + 40, B1[1]), P(x0 - 10, yb), S, angle=90, tside="L")
    note_cfg(xR=P(x1 + 120, 0)[0])
    kr = P(x1 + 120, 0)
    leader(sp, P(*B1), kr, f"2-M{FB['db']} x {C.bolt_length(FB['t'] + 3.2, FB['db'], 1)} 8.8/S THROUGH THE PURLIN "
           f"WEB @ {C.FB_PITCH:.0f} mm ON THE GAUGE LINE, Ø{FB['db'] + 2} HOLES; IN A LAPPED ZONE 1 BOLT + THE LAP BOLT", S, "R", 30, bolt=FB["db"] + 2)
    leader(sp, P(x1 - 30, yb + 150), kr, f"PURLIN {PURLIN} (BY OTHERS)", S, "R", 30)


# ======================================================================= 5001: branch weld zones 1:1
def branch_weld_detail(ox, oy):
    """typical weld round a round branch (AWS D1.1:2015 Fig 9.10, column E = t): local sections square to the
    weld at the heel (acute side), the side and the toe (obtuse side, branch edge bevelled), 1:1, drawn for D2
    (t 3.2). Legs by member mark in TABLE 3"""
    S = 1
    sp = msp
    g = "DE"
    t, tc = SEC[g].t, TC_T
    lg = WELDS[g]["legs"]
    zones = (("HEEL", 47.0, "ACUTE SIDE, Ψ < 60°", "L = 1.5t + Z"),
             ("SIDE", 90.0, "Ψ 60° - 120°", "L = 1.4t ... 1.8t"),
             ("TOE", 133.0, "OBTUSE (GAP) SIDE, Ψ > 120°", "EDGE BEVELLED, L = 1.4t"))
    for k, (nm, psi, sub, rule) in enumerate(zones):
        cx = ox + k * 48.0
        P = lambda x, y: (cx + x, oy + y)
        Lw = lg.get(nm, lg["SIDE"])
        # chord wall (cut)
        pline(sp, [P(-16, -tc), P(24, -tc)], "S-STL")
        line(sp, P(-16, 0), P(24, 0), "S-STL")
        for xb in (-16, 24):
            line(sp, P(xb, 1.5), P(xb, -tc - 1.5), "S-BREAK")
        a = math.radians(psi)
        d = (math.cos(a), math.sin(a))                              # outer face of the branch wall
        nrm = (-math.sin(a), math.cos(a))                           # toward the inside of the wall
        s_in = -nrm[1] * t / d[1]
        fi = (nrm[0] * t + d[0] * s_in, 0.0)                        # inner face foot, on the chord surface
        Lb = 20.0
        far_o = (d[0] * Lb, d[1] * Lb)
        far_i = (far_o[0] + nrm[0] * t, far_o[1] + nrm[1] * t)
        if nm == "TOE":                                             # edge cut back: bevel from the inner foot
            bv = (d[0] * 1.5 * t, d[1] * 1.5 * t)
            plate(sp, P, [fi, bv, far_o, far_i])
            weld_region(sp, P, [fi, bv, (bv[0] + 0.6 * Lw, bv[1] - 0.1 * Lw), (Lw, 0.0)], Lw, S)
            line(sp, P(*fi), P(*bv), "S-STL")
        else:
            plate(sp, P, [fi, (0.0, 0.0), far_o, far_i])
            weld_region(sp, P, [(0.0, 0.0), (Lw, 0.0), (d[0] * Lw, d[1] * Lw)], Lw, S)
            if nm == "HEEL":                                        # Z loss at the root (unfused, not counted)
                z = C.Z_LOSS
                pline(sp, [P(0, 0), P(z, 0), P(d[0] * z, d[1] * z)], "S-STL-HIDN", close=True)
        dim(sp, P(0.0 if nm != "TOE" else 0.0, 0), P(Lw, 0), P(0, -tc - 4), S, text="L")
        text(sp, nm, P(4, -tc - 9), 2.8, align=TA.TOP_CENTER, style="ANB")
        text(sp, sub, P(4, -tc - 13.5), 2.0, align=TA.TOP_CENTER)
        text(sp, rule, P(4, -tc - 17), 2.0, align=TA.TOP_CENTER)
    text(sp, f"DRAWN FOR D2 (t = {t:g} mm): HEEL / SIDE / TOE L = " + " / ".join(str(lg.get(z, "-")) for z in
         ("HEEL", "SIDE", "TOE")) + " mm; Z (HIDDEN) = ROOT NOT FUSED, AWS D1.1 TABLE 9.5",
         (ox - 16, oy - tc - 22), 2.0, align=TA.TOP_LEFT)


# ======================================================================= 3001: camber diagram
CAMBER_EX = 25.0                   # vertical exaggeration of the camber diagram


def camber_diagram(ox, oy):
    """camber ordinates at every panel point (DSC p.209-210: the diagram is always given with the truss), 1:200
    along, ordinates exaggerated"""
    S = 200
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    ys = D["camber_y"]
    line(sp, P(0, 0), P(L, 0), "S-GRID")
    pline(sp, [P(k * A_P, CAMBER_EX * y) for k, y in enumerate(ys)], "S-STL")
    for k, y in enumerate(ys):
        line(sp, P(k * A_P, 0), P(k * A_P, CAMBER_EX * y), "S-ANNO")
        text(sp, f"{y:.0f}", P(k * A_P, CAMBER_EX * max(y, 0) + 1.2 * S), 2.0 * S, align=TA.MIDDLE_LEFT, rot=90)
    for x, lab in ((0, "PIN END"), (L, "SLIDING END")):
        text(sp, lab, P(x, -2.0 * S), 2.0 * S, align=TA.TOP_CENTER)
    text(sp, "CL", P(L / 2, -2.0 * S), 2.0 * S, align=TA.TOP_CENTER, style="ANB")


# ======================================================================= notes
GEN = [
    ("1.", "THESE DRAWINGS SHOW STEEL ROOF TRUSS T1 (PRATT, 25.0 m SPAN, 1.25 m DEEP) OF CIRCULAR HOLLOW SECTIONS. "
           "READ WITH THE ARCHITECTURAL AND ROOF FRAMING DRAWINGS (BY OTHERS)."),
    ("2.", "DIMENSIONS IN mm, LEVELS IN m. DO NOT SCALE. WORK POINTS (WP) OF THE NODES ARE THE SETTING-OUT POINTS, "
           "e FROM THE CHORD AXIS (TABLE 3); BRANCH ENDS ARE CUT TO FIT THE CHORDS."),
    ("3.", "STATUS: FOR REVIEW - PRELIMINARY DESIGN. NOT FOR FABRICATION UNTIL RE-ISSUED."),
    ("4.", "BOLT HOLES = BOLT DIAMETER + 2 mm UNLESS NOTED; ANCHOR ROD HOLES 5002."),
]
CRIT = [
    ("1.", "DESIGN: AISC 360-16 LRFD (MEMBERS CH. D, E, F8, H1; HSS-TO-HSS JOINTS TABLE K3.1, LIMITS TABLE K3.1A; "
           "PLATE TO HSS TABLE K2.1); AISC DESIGN GUIDE 24 (EFFECTIVE LENGTHS 8.4, UNBALANCED JOINTS 8.2, FLANGE "
           "SPLICE 5.4, SLOTTED TUBE END 5.3). LOAD COMBINATIONS ASCE 7-16 2.3: 1.4D, 1.2D + 1.6Lr (FULL AND HALF "
           "SPAN), 0.9D + 1.0W."),
    ("2.", f"TRUSSES @ {C.S_TRUSS:.1f} m; PURLINS AT EVERY TOP NODE. DEAD LOAD {C.Q_SDL:.2f} kPa (SHEET, PURLINS, "
           f"SERVICES) + SELF-WEIGHT x {C.SW_EXTRA:.2f}. ROOF LIVE LOAD {C.Q_LR:.2f} kPa (MINISTERIAL REGULATION NO. 6)."),
    ("3.", f"WIND: NET UPLIFT {C.Q_W:.2f} kPa ASSUMED - TO BE CONFIRMED BY THE WIND ASSESSMENT (DPT 1311) BEFORE "
           "CONSTRUCTION."),
    ("4.", "LATERAL RESTRAINT: TOP CHORD AT EVERY NODE BY THE PURLINS AND THE ROOF BRACING (BY OTHERS); BOTTOM CHORD BY "
           f"FLY BRACES FB1 {D['fly']['name']} AT EVERY 4TH BOTTOM PANEL POINT (5.0 m; OPEN TRIANGLES ON 2/3001; "
           "5004), DESIGNED AS NODAL BRACES (AISC 360-16 APP. 6.2: 1 % OF THE CHORD FORCE AND THE BRACE STIFFNESS; "
           "KL/r ≤ 200)."),
    ("5.", "JOINT LIMITS CHECKED (TABLE K3.1A): -0.55 ≤ e/D ≤ 0.25; θ ≥ 30°; 0.4 ≤ Db/D (GAPPED K); g ≥ tb1 + tb2 "
           f"(≥ {C.G_MIN:.0f} mm, ≥ {C.G_ABS:.0f} mm AT THE END TOP NODES); D/t ≤ 50 (X: 40); COMPRESSION Db/tb ≤ 0.05E/Fy; "
           f"CHORD END ≥ D(1.25 - β/2) = {D['l_end']:.0f} mm BEYOND V1. THE e-MOMENTS ARE INCLUDED IN THE CHORD CHECKS."),
    ("6.", f"DEFLECTION (D + Lr) {sum(D['defl']):.0f} mm = L/{L / sum(D['defl']):.0f} (LIMIT L/240); CAMBER "
           f"{D['camber']:.0f} mm AT MIDSPAN (3/3001)."),
    ("7.", "SUPPORT REACTIONS PER TRUSS (FACTORED): "
           f"{max(r[0] for r in D['reac'].values()) / 1000:.0f} kN DOWN, "
           f"{max(-r[1] for r in D['reac'].values()) / 1000:.0f} kN UPLIFT; ONE END PINNED, THE OTHER SLIDING. "
           "STRUCTURE STATICALLY LOADED (AWS D1.1); NO FATIGUE."),
]
MAT = [
    ("1.", "HOLLOW SECTIONS: JIS G 3444 STK400 (Fy ≥ 235 MPa, Fu ≥ 400 MPa) OR TIS 107 EQUIVALENT, MILL CERTIFICATES."),
    ("2.", "PLATES: JIS G 3106 SM400B (WELDED PLATES), JIS G 3101 SS400 ONLY FOR WASHERS AND UNWELDED PARTS."),
    ("3.", "BOLTS: ISO 898-1 GRADE 8.8 (OR JIS B 1186 F10T) WITH GRADE 8 NUTS AND HARDENED WASHERS. NO LOCK "
           "WASHERS."),
    ("4.", "ANCHOR RODS: SS400, M20, HEADED; NUTS, LOCK NUTS, LEVELLING NUTS, PL WASHERS (5002). GROUT: NON-SHRINK, "
           "≥ 40 MPa."),
    ("5.", "WELDING CONSUMABLES: LOW-HYDROGEN, MATCHING E43XX / E60XX OR E49XX / E70XX (AWS A5.1 E7016 / E7018; "
           "A5.18 ER70S-6; A5.20 E71T-1). CERTIFICATES TO BE SUBMITTED. SHORT-CIRCUIT GMAW ONLY WITH A WPS QUALIFIED "
           "BY TEST; SINGLE-PASS FCAW ELECTRODES NOT PERMITTED."),
]
FAB = [
    ("1.", "FABRICATION TO AWS D1.1 (CLAUSE 9, TUBULAR STRUCTURES) AND AISC 303; TOLERANCES AISC 303, SWEEP ≤ L/1000, "
           "CAMBER -0 / +10 mm. SHOP DRAWINGS AND WRITTEN WPSs FOR ALL WELDS FOR APPROVAL."),
    ("2.", "STK400 / SM400B ARE NOT LISTED IN AWS D1.1: WPSs QUALIFIED BY TEST (AWS D1.1 CL. 4 OR ISO 15614-1), OR "
           "SUBMITTED WITH THE MILL CHEMISTRY FOR THE ENGINEER'S APPROVAL. PREHEAT PER THE WPS."),
    ("3.", "BRANCH ENDS CNC PROFILE-CUT TO THE CHORD; FIT-UP GAP ≤ 2 mm (ABOVE 2 mm INCREASE THE LEG BY THE GAP, "
           "MAX 5 mm). GAP JOINTS ONLY: BRANCHES CLEAR EACH OTHER BY THE GAP IN TABLE 3. TACK WEBS TO ONE CHORD, THEN "
           "FIT THE OTHER CHORD."),
    ("4.", "BRANCH WELDS ALL ROUND, AWS D1.1 FIG 9.10 PREQUALIFIED TUBULAR DETAILS: LEGS BY ZONE IN TABLE 3, TOE "
           "ZONE WITH THE BRANCH EDGE BEVELLED (4/5001). WELDERS QUALIFIED FOR TUBULAR T-, Y-, K-CONNECTIONS (AWS D1.1 "
           "6GR). NO UNSPECIFIED WELDS, TACKS TO THE WPS. TURN THE SHOP PIECES SO NODE WELDS ARE FLAT OR HORIZONTAL."),
    ("5.", "INSPECTION: 100 % VT BY THE FABRICATOR'S QC (CWI OR EQUIVALENT): FIT-UP, ROOT, SIZE; MT (YOKE) 10 % OF "
           "BRANCH WELDS INCLUDING HEEL AND TOE ZONES, 100 % OF FLANGE WELDS; ACCEPTANCE AWS D1.1 STATIC TUBULAR."),
    ("6.", "THREE SHOP PIECES SP1 - SP3 (2/3001), CAMBERED (3/3001); TRIAL ASSEMBLY OF THE SPLICES IN THE SHOP, "
           "FLANGE HOLES DRILLED IN PAIRS AND MATCHMARKED FS1 / FS2. FLANGE FACES MACHINED AFTER WELDING."),
]
PROT = [
    ("1.", "ENDS OF EVERY HOLLOW SECTION SEALED BY CONTINUOUS FILLET WELDS (CAPS p1 / p9, FLANGES), MADE AND "
           "INSPECTED AS STRUCTURAL WELDS: NO INTERNAL PAINT. IF HOT-DIP GALVANIZED INSTEAD: VENT AND DRAIN HOLES "
           "(≥ Ø13 mm / Ø25 mm) AT BOTH ENDS OF EVERY CLOSED TUBE, DETAILS TO BE REVISED."),
    ("2.", "BLAST CLEAN Sa 2½; ZINC-RICH EPOXY PRIMER 75 µm + EPOXY MIO 100 µm (SHOP); POLYURETHANE TOP COAT 50 µm "
           "(SITE, AFTER TOUCH-UP). FLANGE CONTACT FACES: PRIMER ONLY. NO PAINT WITHIN 50 mm OF THE SITE WELDS (w1)."),
    ("3.", "FIRE PROTECTION: NONE REQUIRED UNLESS SHOWN BY THE ARCHITECT. NOT AESS."),
]
ERECT = [
    ("1.", "ASSEMBLE SP1 - SP3 ON THE GROUND, MATCHMARKS FS1 / FS2 ALIGNED, PRETENSION THE FLANGE BOLTS, BOLT THE "
           "LOOSE DIAGONALS, THEN LIFT AS ONE TRUSS WITH A SPREADER BEAM AT NODES (LIFTING PLAN BY THE ERECTOR). "
           "LIFTING WEIGHT ABOUT {LIFT} t (3001). NO LIFTING LUGS ON THE TUBES."),
    ("2.", "THE TRUSS IS NOT LATERALLY STABLE ALONE: KEEP IT BRACED UNTIL THE PURLINS, ROOF BRACING AND FLY BRACES "
           "ARE COMPLETE; NO ROOF LOAD BEFORE THAT (AISC 303 7.10)."),
    ("3.", "SET THE ANCHOR RODS BY TEMPLATE; LEVEL ON THE LEVELLING NUTS; FIX THE PIN END FIRST AND SITE-WELD ITS "
           "PLATE WASHERS w1; SET THE SLIDING END WITH THE RODS CENTRED IN THE SLOTS, DOUBLE NUTS SNUG; GROUT."),
    ("4.", "BOLTS: TABLE 4 (+2 % SPARE OF EACH SIZE). NO OTHER SITE WELDING ON THE TRUSS WITHOUT THE ENGINEER'S "
           "APPROVAL."),
]


def weld_key(ps, x, y_top):
    """key to the weld symbols used (AWS A2.4), paper size"""
    text(ps, "WELD SYMBOLS (AWS A2.4)", (x, y_top - 2.8), 2.8, "S-TITLE", style="ANB")
    rows = [(dict(), 6, "FILLET, ARROW SIDE (BELOW THE LINE), LEG 6 mm"),
            (dict(side="both"), 6, "FILLET BOTH SIDES, LEG 6 mm EACH SIDE"),
            (dict(side="both", length=100), 3, "FILLET BOTH SIDES, LEG 3 mm, LENGTH 100 mm"),
            (dict(all_round=True, tail="4/5001"), 6, "FILLET ALL ROUND; TAIL = DETAIL"),
            (dict(all_round=True, ndt="MT"), 6, "FILLET ALL ROUND, MT TESTED"),
            (dict(groove="bevel"), "E", "BEVEL (PJP), THROAT E; BREAK: PART BEVELLED"),
            (dict(all_round=True, field=True), 5, "SITE WELD ALL ROUND (FLAG) - w1 ONLY")]
    y = y_top - 10
    for kw, sz, desc in rows:
        weld(ps, (x + 4, y - 4), (x + 10, y), 1, sz, rl=26, **kw)
        text(ps, desc, (x + 50, y), 2.0, align=TA.MIDDLE_LEFT)
        y -= 8
    for ln in SE.td_engine.wrap_s("SIZES = FILLET LEG mm. NO LENGTH = FULL LENGTH OF THE JOINT. A SYMBOL ON A "
                                  "NEAR-SIDE PIECE APPLIES TO THE SAME FAR-SIDE PIECE. ALL WELDS ARE SHOP WELDS "
                                  "UNLESS FLAGGED.", 2.0, 96):
        text(ps, ln, (x, y + 2), 2.0, align=TA.TOP_LEFT)
        y -= 3.6
    return y - 6


weld_key = SE.td_engine._grouped("KEY", weld_key)


# ======================================================================= tables
def design_rows():
    rows = []
    for g, desc in C.GROUPS.items():
        ms = [m for m in D["mem"] if m[1] == g]
        t = max(D["env"][m[0]][0] for m in ms) / 1000
        c = -min(D["env"][m[0]][1] for m in ms) / 1000
        u = max(D["members"][m[0]] for m in ms)
        mk = "/".join(CHORD_MARK[g[0]]) if g in ("TC", "BC") else \
            "/".join(sorted({mark_of(m[0]) for m in ms if m[0] not in LOOSE}))
        rows.append([mk, sname(g), f"{t:.0f}", f"{c:.0f}", f"{u:.2f}"])
    ju = max(j["util"] for j in D["joints"].values())
    rows.append(["JOINTS", f"TABLE K3.1 ({len(D['joints'])} NODES)", "-", "-", f"{ju:.2f}"])
    rows.append(["SPLICE", f"PL {FL['tp']}, {FL['n']}-M{FL['db']} 8.8", "-", "-", f"{FL['util']:.2f}"])
    rows.append([mark_of(f"D{C.SPLICE_PANELS[0]}"), "LOOSE DIAGONAL ENDS", "-", "-", f"{LD['util']:.2f}"])
    return rows


def member_rows():
    rows = []
    for side, g in (("T", "TC"), ("B", "BC")):
        for k, (mk, ln) in enumerate(zip(CHORD_MARK[side], CHORD_LEN)):
            prep = "SQUARE; CAP p1 / FLANGE p6" if k == 0 else "SQUARE; FLANGE p6 BOTH ENDS"
            n = 2 if k == 0 else 1
            rows.append([mk, sname(g), "STK400", f"{ln:.0f}", prep, str(n), f"{SEC[g].kgm:.2f}",
                         f"{SEC[g].kgm * ln / 1000 * n:.0f}"])
    marks = {}
    for w in WEBS:
        marks.setdefault(mark_of(w[0]), []).append(w[0])
    for mk in sorted(marks, key=lambda m: (m[0] != "V", int(m[1:]))):
        ns = marks[mk]
        g = group_of(ns[0])
        sec = SEC[g]
        ln = axis_length(ns[0])
        if ns[0] in LOOSE:
            prep = "SLOTTED BOTH ENDS; CAP p9"
        else:
            prep = "PROFILE-CUT BOTH ENDS" + ("; TOE BEVELLED" if WELDS[g]["bevel"] else "")
        rows.append([mk, sec.name, "STK400", f"{ln:.0f}", prep, str(len(ns)), f"{sec.kgm:.2f}",
                     f"{sec.kgm * ln / 1000 * len(ns):.0f}"])
    FB = D["fly"]                                                  # fly braces, loose (Beca SE-1505 schedule)
    nfb = 2 * (len(C.BC_BRACE) - 2)
    rows.append(["FB1", FB["name"], "SS400", f"{FB['length']:.0f}", "SQUARE; 1 HOLE / 2 HOLES, LOOSE", str(nfb),
                 f"{FB['kgm']:.2f}", f"{FB['kgm'] * FB['length'] / 1000 * nfb:.0f}"])
    return rows


def plate_rows():
    """TABLE 5: plates and fittings of one truss (DSC p.183, p.237: every piece billed), kg at 7850 kg/m3"""
    rho = 7.85e-6
    Dv = SEC["VE"].D
    sad_w = (DC / 2 + SAD_T / 2) * 2 * math.pi / 3                   # developed width of the 120 deg saddle
    stif_h = -DC / 2 - SAD_T - Y_BP
    n = f"D{C.SPLICE_PANELS[0]}"
    kn = LD["s"] + 2 * LD["e"] + 20 + LD["lw"]                       # knife plate length
    rows = [("p1", f"END CAP PL {CAP_T:.0f} x Ø{DC:g}", 4, CAP_T * math.pi * DC ** 2 / 4),
            ("p2", f"SADDLE PL {SAD_T:.0f} x {SAD_L:.0f} x {sad_w:.0f} (BENT 120°)", 2, SAD_T * SAD_L * sad_w),
            ("p3", f"STIFFENER PL {STIF_T:.0f} x {SAD_L:.0f} x {stif_h:.0f}", 2, STIF_T * SAD_L * stif_h),
            ("p4", f"BASE PL {BP_T:.0f} x {BP_B:.0f} x {SUP['N']:.0f}, Ø{SUP['hole']} HOLES (PIN)", 1,
             BP_T * BP_B * SUP["N"]),
            ("p5", f"BASE PL {BP_T:.0f} x {BP_B:.0f} x {SUP['N']:.0f}, SLOTS {SUP['hole']} x {SUP['slot']}", 1,
             BP_T * BP_B * SUP["N"]),
            ("p6", f"FLANGE PL {FL['tp']} x Ø{FL['od']:.0f}", 8, FL["tp"] * math.pi * FL["od"] ** 2 / 4),
            ("p7", f"KNIFE PL {LD['tp']} x {2 * LD['hw']:.0f} x {kn:.0f}", 4, LD["tp"] * 2 * LD["hw"] * kn),
            ("p8", f"GUSSET PL {LD['tp']} x {LD['lp']:.0f} x 180 (ABOUT)", 4, LD["tp"] * LD["lp"] * 180),
            ("p9", f"TUBE CAP PL 3 x Ø{SEC[group_of(n)].D:g}, SLOTTED", 4, 3 * math.pi * SEC[group_of(n)].D ** 2 / 4),
            ("p10", "PURLIN CLEAT PL 8 x 100 x 180", NP + 1, 8 * 100 * 180),
            ("p11", f"FLY-BRACE LUG PL 8 x 150 x {-D['fly']['y_h'] + 35 - DC / 2:.0f}", len(C.BC_BRACE) - 2,
             8 * 150 * (-D["fly"]["y_h"] + 35 - DC / 2)),
            ("w1 / w2", f"PL WASHER {SUP['washer_t']} x {SUP['washer']} x {SUP['washer']}, Ø{SUP['d_rod'] + 2}", 8,
             SUP["washer_t"] * SUP["washer"] ** 2)]
    return [[m, d, str(q), f"{q * v * rho:.1f}"] for m, d, q, v in rows]


def node_rows():
    rows = []
    seen = {}
    for node in sorted(D["joints"], key=lambda n: (int(n[1:]), n[0])):
        seen.setdefault(node_type(node), []).append(node)
    for t in ("N1", "N2", "N3", "N4", "N5", "N6"):
        ns = seen.get(t, [])
        if not ns:
            continue
        n0 = ns[0]
        brs = branches_at(n0)
        gaps = node_gaps(n0)
        legs = []
        for mk in sorted({mark_of(b) for b in brs}):
            g = group_of(next(b for b in brs if mark_of(b) == mk))
            lg = WELDS[g]["legs"]
            legs.append(f"{mk}: " + " / ".join(str(lg.get(z, "-")) for z in ("HEEL", "SIDE", "TOE")))
        loc = []
        for side, word in (("T", "TOP"), ("B", "BOTTOM")):
            ks = [int(n[1:]) for n in ns if n[0] == side and int(n[1:]) <= NP // 2]
            if ks:
                loc.append(f"{word} {ks[0]}" + (f" - {ks[-1]}" if len(ks) > 1 else ""))
        nn = ", ".join(loc)
        e = ECC.get(n0, 0) if gaps else 0
        rows.append([t, SE.NODE_TYPES[t], nn + (" (+ MIRROR)" if any(int(n[1:]) > NP // 2 for n in ns) else ""),
                     " + ".join(marks_at(n0)), f"{e:.0f} ({e / DC:.2f})",
                     " / ".join(f"{g:.0f}" for g in gaps) or "-", "; ".join(legs),
                     f"{max(D['joints'][n]['util'] for n in ns):.2f}"])
    return rows


def conn_rows():
    """TABLE 4: site connections and field bolt summary (DSC p.233-236), one truss"""
    nl = len(C.SPLICE_PANELS)
    return [["FLANGE SPLICES FS1, FS2", f"{FL['n']}-M{FL['db']} x {FL['bolt_len']} 8.8 PER SPLICE",
             f"{FL['n'] * 2 * nl}", f"Ø{FL['db'] + 2}", "HARDENED UNDER NUT", "FULLY PRETENSIONED (TURN-OF-NUT)",
             f"{FL['util']:.2f}"],
            [f"LOOSE DIAGONAL {mark_of(f'D{C.SPLICE_PANELS[0]}')}", f"{LD['n']}-M{LD['db']} x {LD['bolt_len']} 8.8 "
             "PER END", f"{LD['n'] * 2 * nl}", f"Ø{LD['db'] + 2}", "HARDENED UNDER NUT",
             "SNUG-TIGHT, THREADS INCLUDED", f"{LD['util']:.2f}"],
            ["PURLIN CLEAT p10", "2-M12 GRADE 4.6 (BY OTHERS)", f"{2 * (NP + 1)}", "Ø14", "-", "SNUG-TIGHT", "-"],
            ["FLY BRACE FB1 AT THE LUG p11", f"1-M16 x {C.bolt_length(D['fly']['t'] + 8, 16, 1)} 8.8/S PER BRACE",
             f"{2 * (len(C.BC_BRACE) - 2)}", "Ø18", "HARDENED UNDER NUT", "SNUG-TIGHT", f"{D['fly']['util']:.2f}"],
            ["FLY BRACE FB1 AT THE PURLIN", f"2-M16 x {C.bolt_length(D['fly']['t'] + 3.2, 16, 1)} 8.8/S PER BRACE",
             f"{4 * (len(C.BC_BRACE) - 2)}", "Ø18", "HARDENED UNDER NUT", "SNUG-TIGHT", "-"],
            ["ANCHOR RODS AR1", f"{SUP['n_rod']}-M{SUP['d_rod']} SS400 HEADED PER BEARING", f"{2 * SUP['n_rod']}",
             f"Ø{SUP['hole']} / SLOT", "PL w1 / w2", "PIN: TIGHT; SLIDING: DOUBLE NUT SNUG", f"{SUP['rod_util']:.2f}"]]


# ======================================================================= build
def build():
    EXT.update({
        "EL": capture(elev_half, 0, 0),
        "KEY": capture(key_truss, 0, -20000),
        "CAM": capture(camber_diagram, 0, -40000),
        "NT": capture(node_T, 60000, 0),
        "NB": capture(node_B, 70000, 0),
        "NC": capture(node_C, 80000, 0),
        "BW": capture(branch_weld_detail, 90000, 0),
        "END": capture(end_top, 100000, 0),
        "BRG": capture(bearing_elev, 105000, 0),
        "SEC": capture(bearing_section, 110000, 0),
        "BP": capture(base_plans, 120000, 0),
        "SPL": capture(splice_elev, 140000, 0),
        "FF": capture(flange_face, 150000, 0),
        "LD": capture(loose_conn, 160000, 0),
        "XS": capture(cross_section, 175000, 0),
        "FBL": capture(fb_lug, 185000, 0),
        "FBP": capture(fb_purlin, 190000, 0),
    })
    sheet_1001()
    sheet_3001()
    sheet_5001()
    sheet_5002()
    sheet_5003()
    sheet_5004()


def truss_kg():
    """tubes + plates + 2 % welds and bolts, one truss (TABLES 2 and 5)"""
    return (sum(float(r[-1]) for r in member_rows()) + sum(float(r[-1]) for r in plate_rows())) * 1.02


def sheet_1001():
    ps = new_sheet(0)
    erect = [(n, t.replace("{LIFT}", f"{truss_kg() / 1000:.1f}")) for n, t in ERECT]
    top = FY1 - 3
    colw, gap = 98.0, 6.0
    xs = [FX0 + 3 + k * (colw + gap) for k in range(3)]
    y = notes_block(ps, xs[0], top, colw, "1. GENERAL", GEN)
    y = notes_block(ps, xs[0], y - 2, colw, "2. DESIGN CRITERIA", CRIT)
    y0 = tbl(ps, xs[0], y - 8, [24, 38, 12, 12, 12], ["MARK", "SECTION", "T kN", "C kN", "UTIL."], design_rows(),
             "LCCCC", title=TABT("DESIGN"))
    y = notes_block(ps, xs[1], top, colw, "3. MATERIALS", MAT)
    y1 = notes_block(ps, xs[1], y - 2, colw, "4. FABRICATION AND WELDING", FAB)
    tbl(ps, xs[0], min(y0, y1) - 10, [40, 46, 10, 18, 28, 50, 10],
        ["CONNECTION", "BOLTS", "No.", "HOLES", "WASHERS", "TIGHTENING", "UTIL."], conn_rows(), "LLCCLLC",
        title=TABT("CONN"))
    y = notes_block(ps, xs[2], top, colw, "5. CORROSION PROTECTION", PROT)
    y = notes_block(ps, xs[2], y - 2, colw, "6. ERECTION", erect)
    weld_key(ps, xs[2], y - 4)


def sheet_3001():
    ps = new_sheet(1)
    top = FY1 - 3
    px, pw, ph = viewport(ps, "EL", 50, FX0 + 1, top)
    view_title(ps, None, top - ph - 6, "TRUSS T1 - HALF ELEVATION (SYMMETRICAL ABOUT CL)", "1:50", ("1", "3001"))
    y2 = top - ph - 20
    px2, pw2, ph2 = viewport(ps, "KEY", 200, FX0 + 1, y2)
    view_title(ps, None, y2 - ph2 - 6, "ASSEMBLY DIAGRAM: SHOP PIECES, SPLICES, BRACING", "1:200", ("2", "3001"))
    px3, pw3, ph3 = viewport(ps, "CAM", 200, px2 + pw2 + 10, y2)
    view_title(ps, px2 + pw2 + 10, y2 - ph3 - 6, f"CAMBER DIAGRAM (ORDINATES mm, VERTICAL x{CAMBER_EX:.0f})",
               "1:200", ("3", "3001"))
    yt = y2 - max(ph2, ph3) - 22
    rows = member_rows()
    yb = tbl(ps, FX0 + 3, yt, [12, 32, 16, 18, 52, 8, 13, 12],
             ["MARK", "SECTION", "GRADE", "LENGTH mm", "END PREPARATION", "No.", "kg/m", "kg"], rows, "LCCCLCCC",
             title=TABT("MEMB"))
    pr = plate_rows()
    xp = FX0 + 3 + 163 + 6
    tbl(ps, xp, yt, [12, 72, 9, 12], ["MARK", "PLATE / FITTING (SM400B)", "No.", "kg"], pr, "LLCC",
        title=TABT("PLATES"))
    tot_m = sum(float(r[-1]) for r in rows)
    tot_p = sum(float(r[-1]) for r in pr)
    notes_block(ps, FX0 + 3, yb - 6, 163, "NOTES TO 3001", [
        ("1.", f"WEIGHT PER TRUSS: TUBES {tot_m:.0f} kg + PLATES {tot_p:.0f} kg + WELDS AND BOLTS (ABOUT 2 %) = ABOUT "
               f"{(tot_m + tot_p) * 1.02:.0f} kg. SHOP PIECES SP1 / SP3 AND SP2 ABOUT "
               f"{(tot_m + tot_p) * 1.02 * (CHORD_LEN[0] / (2 * CHORD_LEN[0] + CHORD_LEN[1])) / 1000:.2f} / "
               f"{(tot_m + tot_p) * 1.02 * (CHORD_LEN[1] / (2 * CHORD_LEN[0] + CHORD_LEN[1])) / 1000:.2f} t."),
        ("2.", "MARKS (TABLES 2, 5): EVERY PIECE THAT DIFFERS HAS ITS OWN MARK. SP1 (PIN BASE PL p4) AND SP3 "
               "(SLIDING BASE PL p5) ARE OTHERWISE THE SAME; STAMP 'PIN END' / 'SLIDING END' AND 'TOP' ON EACH."),
        ("3.", "LENGTHS: CHORDS = TUBE BETWEEN END PLATES; WEB MEMBERS ON THE AXIS BETWEEN THE CHORD FACES, FOR THE "
               "FLAT TRUSS - THE FABRICATOR ADJUSTS THEM FOR THE CAMBER (3/3001) AND CUTS TO FIT."),
        ("4.", "JOINT TYPES N1 - N6: 5001, 5002 AND TABLE 3 (PANEL POINTS COUNTED FROM THE PIN END). OPEN TRIANGLE "
               "BELOW A NODE = FLY BRACE FB1, BOTH SIDES (5004)."),
    ])


def sheet_5001():
    ps = new_sheet(2)
    top = FY1 - 3
    px, pw, ph = viewport(ps, "NT", 10, FX0 + 1, top)
    view_title(ps, None, top - ph - 6, "TYPICAL TOP NODE (N1; N2 SIMILAR)", "1:10", ("1", "5001"))
    px2, pw2, ph2 = viewport(ps, "NB", 10, px + pw + 4, top)
    view_title(ps, None, top - ph2 - 6, "TYPICAL BOTTOM NODE (N1; N2 SIMILAR)", "1:10", ("2", "5001"))
    y2 = top - max(ph, ph2) - 20
    px3, pw3, ph3 = viewport(ps, "NC", 10, FX0 + 1, y2)
    view_title(ps, None, y2 - ph3 - 6, "CENTRE BOTTOM NODE (N4)", "1:10", ("3", "5001"))
    xw = px3 + pw3 + 8
    px4, pw4, ph4 = viewport(ps, "BW", 1, xw, y2)
    view_title(ps, xw, y2 - ph4 - 6, "TYPICAL BRANCH WELD - ZONES (AWS D1.1 FIG 9.10)", "1:1", ("4", "5001"))
    yn = y2 - ph4 - 20
    notes_block(ps, xw, yn, TBX - xw - 3, "NOTES TO 5001", [
        ("1.", "GAP K-JOINTS: BRANCH AXES MEET AT THE WORK POINT, e FROM THE CHORD AXIS AWAY FROM THE WEB; GAPS "
               "BETWEEN BRANCH TOES ON THE CHORD SURFACE PER TABLE 3. SET OUT FROM THE PANEL-POINT LINE THROUGH THE WP."),
        ("2.", "BRANCH WELDS ALL ROUND, CONTINUOUS THROUGH THE ZONES; LEGS HEEL / SIDE / TOE IN TABLE 3 (Z LOSS "
               "INCLUDED). WELDS SHOWN APPLY TO EVERY NODE OF THE SAME TYPE ON SP1 - SP3."),
        ("3.", "N5 (CENTRE TOP NODE): V ON THE CHORD AXIS. N3, N6: 5002."),
    ])
    yt = min(y2 - ph3 - 22, yn - 34)
    tbl(ps, FX0 + 3, yt, [10, 50, 62, 22, 18, 16, 116, 12],
        ["TYPE", "NODE", "PANEL POINTS (LEFT HALF)", "MEMBERS", "e mm (e/D)", "GAP mm", "WELD LEGS HEEL / SIDE / TOE mm",
         "UTIL."], node_rows(), "LLLCCCLC", title=TABT("NODES"))


def sheet_5002():
    ps = new_sheet(3)
    top = FY1 - 3
    px, pw, ph = viewport(ps, "END", 10, FX0 + 1, top)
    view_title(ps, None, top - ph - 6, "END TOP NODE (N3)", "1:10", ("1", "5002"))
    px2, pw2, ph2 = viewport(ps, "SEC", 10, px + pw + 6, top)
    view_title(ps, None, top - ph2 - 6, "SECTION 2 (ON 4/5002)", "1:10", ("2", "5002"))
    y2 = top - max(ph, ph2) - 20
    px3, pw3, ph3 = viewport(ps, "BRG", 10, FX0 + 1, y2)
    view_title(ps, None, y2 - ph3 - 6, "BEARING AT THE PIN END (N6; SLIDING END: BASE PL p5)", "1:10", ("4", "5002"))
    px4, pw4, ph4 = viewport(ps, "BP", 10, px3 + pw3 + 6, y2)
    view_title(ps, None, y2 - ph4 - 6, "BASE PLATES - PLAN", "1:10", ("3", "5002"))


def sheet_5003():
    ps = new_sheet(4)
    top = FY1 - 3
    px, pw, ph = viewport(ps, "SPL", 5, FX0 + 1, top)
    view_title(ps, None, top - ph - 6, "CHORD FLANGE SPLICE FS1 / FS2", "1:5", ("1", "5003"))
    px2, pw2, ph2 = viewport(ps, "FF", 5, px + pw + 4, top)
    view_title(ps, None, top - ph2 - 6, "FLANGE PLATE p6", "1:5", ("1A", "5003"))
    y2 = top - max(ph, ph2) - 20
    px3, pw3, ph3 = viewport(ps, "LD", 10, FX0 + 1, y2)
    view_title(ps, None, y2 - ph3 - 6, f"LOOSE DIAGONAL {mark_of(f'D{C.SPLICE_PANELS[0]}')} - BOTTOM END (TOP END "
               "SIMILAR)", "1:10", ("2", "5003"))


def fly_rows():
    """TABLE 6 (after the Beca SE-1505 fly bracing schedule): one row per fly-brace type"""
    FB = D["fly"]
    nodes = ", ".join(f"B{k}" for k in C.BC_BRACE[1:-1])
    return [["FB1", f"BOTTOM {nodes} (+ MIRROR), BOTH SIDES", FB["name"], "PL 8 (p11)",
             f"1-M{FB['db']} 8.8/S", f"2-M{FB['db']} 8.8/S (1 + LAP BOLT)", f"{FB['F']:.0f}°",
             f"{FB['P'] / 1000:.1f} kN; KL/r {FB['lam']:.0f}"]]


def sheet_5004():
    ps = new_sheet(5)
    top = FY1 - 3
    px, pw, ph = viewport(ps, "XS", 20, FX0 + 1, top)
    view_title(ps, None, top - ph - 6, "SECTION 1 (ON 1/3001): FLY BRACE FB1", "1:20", ("1", "5004"),
               note="SYMMETRICAL ABOUT THE TRUSS CENTRE LINE")
    px2, pw2, ph2 = viewport(ps, "FBL", 5, px + pw + 8, top)
    view_title(ps, px + pw + 8, top - ph2 - 6, "FLY BRACE FB1 - LUG END", "1:5", ("2", "5004"))
    y3 = top - max(ph, ph2) - 26
    px3, pw3, ph3 = viewport(ps, "FBP", 5, FX0 + 1, y3)
    view_title(ps, None, y3 - ph3 - 6, "FLY BRACE FB1 - PURLIN END", "1:5", ("3", "5004"))
    yt = y3 - ph3 - 22
    yb = tbl(ps, FX0 + 3, yt, [12, 58, 22, 18, 24, 44, 10, 34],
             ["MARK", "LOCATION", 'ANGLE "A"', 'LUG "B"', 'BOLTS "C" LUG', 'BOLTS "C" PURLIN', '"F"',
              "DESIGN FORCE"], fly_rows(), "LLCCCCCC", title=TABT("FLY"))
    xn = px3 + pw3 + 10                                            # beside the purlin-end detail
    notes_block(ps, xn, y3, TBX - xn - 3, "NOTES TO 5004", [
        ("1.", "FLY BRACES ARE NODAL BRACES OF THE BOTTOM CHORD (AISC 360-16 APP. 6.2): DESIGN FORCE 1 % OF THE "
               "CHORD COMPRESSION, STIFFNESS ≥ 8 Pr / (0.75 Lbr), SINGLE ANGLE KL/r ≤ 200."),
        ("2.", "BRACE AT F = 45° TO THE PURLIN; AT THE END OF THE PURLIN LAP INSTEAD IF F IS THEN 35° - 55° (BECA "
               "SE-1505). BOTH GAUGE LINES MEET ON THE TRUSS CENTRE LINE (WP)."),
        ("3.", "IN A LAPPED PURLIN ZONE ONE BRACE BOLT PLUS THE LAP BOLT; ELSEWHERE 2 BOLTS. PURLIN SIZE, LAPS AND "
               "HOLES BY THE PURLIN SUPPLIER: CONFIRM THE BRACE HOLES WITH THEM."),
        ("4.", "MARK FB1 AT THE OPEN TRIANGLES ON 2/3001; FLY BRACES SHIP LOOSE WITH THEIR BOLTS (TABLE 4, 1001)."),
    ])

