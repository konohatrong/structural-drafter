"""
Typical fixed steel ladder LD1 (worked example LAD): views and sheets.

LAD-ST-5201  front and side elevations 1:25
LAD-ST-5202  details 1:5: rung to stile (A), wall bracket (B), base (C)
LAD-ST-5203  optional cage 1:20, TABLE 1 geometry (OSHA 1910.23), TABLE 2 members (assumed), notes
Content after the office study of a standard ladder sheet (docs/steel/stairs/18_LADDER_DETAILING.md): every
limit dimensioned with its value, clear zones drawn, connections called out to details drawn as built.
Every value from lad_engine.py.
"""
import math

from lad_engine import *          # noqa: F401,F403

BASE = "LAD-ST_Typical_Fixed_Ladder_A3_RevA"
SHEETS[:] = [("5201", ["TYPICAL FIXED STEEL LADDER LD1", "ELEVATIONS"], "1:25"),
             ("5202", ["TYPICAL FIXED STEEL LADDER LD1", "DETAILS"], "1:5"),
             ("5203", ["TYPICAL FIXED STEEL LADDER LD1", "CAGE (OPTION), GEOMETRY, MEMBERS"], "AS SHOWN")]

D_, T_ = STILE
RC = D_ / 2                                      # rung centre line from the climbing face of the stiles
U_WALL = RC + TOE                                # wall face (and the landing edge: STEP = TOE on this example)
Z_TOP = H_CLIMB
Z_SLAB = H_CLIMB - SLAB_T


def bracket_levels():
    """wall brackets: the top one in the slab edge, the others at equal spaces <= BRK_MAX down to the base"""
    z_top = H_CLIMB - SLAB_T / 2
    n = max(1, math.ceil(z_top / BRK_MAX - 1e-9))
    return [z_top * k / n for k in range(1, n + 1)], z_top / n


def conc_cut(sp, P, pts, S):
    hatch(sp, [P(*q) for q in pts], "AR-CONC", pscale("AR-CONC", S, 2.5))
    pline(sp, [P(*q) for q in pts], "S-CONC", close=True)


# ======================================================================= 5201: elevations 1:25
def front(ox, oy):
    """front elevation from the climbing side: stiles on base plates, rungs, the walk-through flare above the
    landing; the roof slab edge beyond"""
    S = 25
    sp = msp
    P = lambda x, z: (ox + x, oy + z)
    line(sp, P(-900, 0), P(900, 0), "S-CONC")
    hatch(sp, [P(-900, 0), P(900, 0), P(900, -150), P(-900, -150)], "EARTH", pscale("EARTH", S, 4.0))
    xs = (-B / 2 - T_ / 2, B / 2 + T_ / 2)
    for xc in xs:
        pline(sp, [P(*q) for q in [(xc - 50, 0), (xc + 50, 0), (xc + 50, BASE_PL[2]), (xc - 50, BASE_PL[2])]], "S-STL",
              close=True)
    rungs = ladder_front(sp, P, BASE_PL[2], Z_TOP, B, S, PITCH, stile=STILE, rung_d=RUNG_D, ext=EXT_UP,
                         first=PITCH - BASE_PL[2], flare=(FLARE, 300.0))
    # roof slab edge beyond (seen), interrupted by the stiles
    xo = B / 2 + T_
    for a, b in ((-900, -xo), (-B / 2, B / 2), (xo, 900)):
        for z in (Z_TOP, Z_SLAB):
            line(sp, P(a, z), P(b, z), "S-CONC-VIS")
    for x in (-900, 900):
        zbreak(sp, P(x, Z_SLAB - 120), P(x, Z_TOP + 120), S)
    # dimensions
    dim(sp, P(-B / 2, 750), P(B / 2, 750), P(0, 750), S, text="<> CLEAR")
    dim(sp, P(-B / 2 - T_, 0), P(B / 2 + T_, 0), P(0, -9 * S), S)
    k = (FLARE - B) / 2
    dim(sp, P(-B / 2 - k, Z_TOP + EXT_UP), P(B / 2 + k, Z_TOP + EXT_UP), P(0, Z_TOP + EXT_UP + 6 * S), S,
        text="<> CLEAR")
    dim(sp, P(B / 2 + k + T_, Z_TOP), P(B / 2 + k + T_, Z_TOP + EXT_UP), P(B / 2 + k + 12 * S, 0), S, angle=90)
    dim(sp, P(-B / 2 - T_, 0), P(-B / 2 - T_, Z_TOP), P(-B / 2 - 14 * S, 0), S, angle=90,
        text=f"{N_RUNG} @ {PITCH:.0f} = <>")
    dim(sp, P(-B / 2 - T_, 0), P(-B / 2 - T_, rungs[0]), P(-B / 2 - 7 * S, 0), S, angle=90)
    note_cfg(xR=P(900 + 4 * S, 0)[0])
    kr = lambda z: P(900 + 4 * S, z)
    leader(sp, P(B / 2 + T_ / 2, 2400), kr(2400), f"STILES FL {D_:.0f} x {T_:.0f}", S, "R", 20)
    leader(sp, P(B / 2 - 60, rungs[5]), kr(rungs[5] - 300), f"RUNGS Ø{RUNG_D:.0f} AT {PITCH:.0f} mm (A/5202)", S,
           "R", 20)
    leader(sp, P(B / 2 + 40, BASE_PL[2] / 2), kr(400), "BASE PL (C/5202)", S, "R", 20)
    leader(sp, P(700, Z_TOP), kr(Z_TOP - 300), f"LANDING (ROOF SLAB {SLAB_T:.0f}) BEYOND", S, "R", 20)


def side(ox, oy):
    """side elevation: wall and roof slab cut, stile seen with the rungs, brackets to the wall, base, the clear
    zone on the climbing side and the step-across to the landing"""
    S = 25
    sp = msp
    P = lambda u, z: (ox + u, oy + z)
    # ground and pad, wall and slab cut
    line(sp, P(-1000, 0), P(U_WALL, 0), "S-CONC")
    hatch(sp, [P(-1000, 0), P(U_WALL, 0), P(U_WALL, -150), P(-1000, -150)], "EARTH", pscale("EARTH", S, 4.0))
    conc_cut(sp, P, [(U_WALL, -300), (U_WALL + WALL_T, -300), (U_WALL + WALL_T, Z_SLAB), (U_WALL, Z_SLAB)], S)
    conc_cut(sp, P, [(U_WALL, Z_SLAB), (U_WALL + 1200, Z_SLAB), (U_WALL + 1200, Z_TOP), (U_WALL, Z_TOP)], S)
    zbreak(sp, P(U_WALL - 80, -300), P(U_WALL + WALL_T + 80, -300), S)
    zbreak(sp, P(U_WALL + 1200, Z_SLAB - 100), P(U_WALL + 1200, Z_TOP + 100), S)
    line(sp, P(U_WALL + WALL_T, Z_SLAB), P(U_WALL + 1200, Z_SLAB), "S-CONC")
    # base plate, stile, rungs
    pline(sp, [P(*q) for q in [(0, 0), (BASE_PL[0], 0), (BASE_PL[0], BASE_PL[2]), (0, BASE_PL[2])]], "S-STL", close=True)
    rungs = [PITCH * k for k in range(1, N_RUNG + 1)]
    ladder_side(sp, P, BASE_PL[2], Z_TOP, S, rungs, stile=STILE, rung_d=RUNG_D, ext=EXT_UP)
    # brackets: FL seen side-on from the stile to the wall, its bent leg on the wall edge-on
    lv, sp_ = bracket_levels()
    for z in lv:
        pts = [(D_ - 50, z - BRK[0] / 2), (U_WALL, z - BRK[0] / 2), (U_WALL, z + BRK[0] / 2), (D_ - 50, z + BRK[0] / 2)]
        pline(sp, [P(*q) for q in pts], "S-STL", close=True)
        line(sp, P(U_WALL - BRK[1], z - BRK[0] / 2), P(U_WALL - BRK[1], z + BRK[0] / 2), "S-STL")
    # clear zone on the climbing side; work point of the step-across
    uc = RC - CLIMB
    line(sp, P(uc, 0), P(uc, Z_TOP + EXT_UP), "S-ZONE-DASH")
    text(sp, "CLEAR ZONE", P(uc + 2 * S, 2600), 2.0 * S, "S-TEXT", TA.MIDDLE_CENTER, rot=90)
    # dimensions
    zd = rungs[2]
    dim(sp, P(RC, zd), P(U_WALL, zd), P(0, zd + 7 * S), S)
    dim(sp, P(uc, Z_TOP + 950), P(RC, Z_TOP + 950), P(0, Z_TOP + 950), S, text="<> MIN.")
    dim(sp, P(RC, Z_TOP), P(U_WALL, Z_TOP), P(0, Z_TOP + EXT_UP + 5 * S), S, text="<> (STEP)")
    xd = -9 * S
    prev = 0.0
    for z in lv:
        dim(sp, P(0, prev), P(0, z), P(xd, 0), S, angle=90)
        prev = z
    levels = [(0.0, "±0.000", "GROUND"), (Z_TOP, f"+{Z_TOP / 1000:.3f}", "LANDING")]
    for z, v, lab in levels:
        x, y = P(U_WALL + 1200 + 3 * S, z)
        level(sp, x, y, v, lab, S, ext=(-2, 22))
    note_cfg(xL=P(uc - 4 * S, 0)[0])
    kl = lambda z: P(uc - 4 * S, z)
    leader(sp, P(0, Z_TOP + 600), kl(Z_TOP + 600), f"STILES {EXT_UP:.0f} ABOVE THE LANDING, FLARED TO "
           f"{FLARE:.0f} CLEAR (5201 FRONT)", S, "L", 18)
    note_cfg(xR=P(U_WALL + 1200 + 4 * S, 0)[0])
    kr = lambda z: P(U_WALL + 1200 + 4 * S, z)
    leader(sp, P((D_ + U_WALL) / 2, lv[1] + BRK[0] / 2), kr(lv[1] + 400), f"WALL BRACKETS FL {BRK[0]:.0f} x "
           f"{BRK[1]:.0f} AT ≤ {BRK_MAX:.0f} mm (B/5202)", S, "R", 18)
    leader(sp, P(U_WALL + WALL_T, 1500), kr(1500), f"EXISTING RC WALL {WALL_T:.0f}", S, "R", 18)


# ======================================================================= 5202: details 1:5
def rung_detail(ox, oy):
    """A: rung through the stile, front (stile edge-on) and side (stile face) views"""
    S = 5
    sp = msp
    P = lambda x, z: (ox + x, oy + z)
    r = RUNG_D / 2
    # front: right stile edge-on, rung from the ladder centre side
    pline(sp, [P(0, -150), P(T_, -150), P(T_, 150), P(0, 150)], "S-STL", close=True)
    zbreak(sp, P(-20, 150), P(T_ + 20, 150), S)
    zbreak(sp, P(-20, -150), P(T_ + 20, -150), S)
    line(sp, P(-180, r), P(0, r), "S-STL")
    line(sp, P(-180, -r), P(0, -r), "S-STL")
    for d in (r, -r):
        line(sp, P(0, d), P(T_, d), "S-STL-HIDN")
    for d in (HOLE_D / 2, -HOLE_D / 2):
        line(sp, P(0, d), P(T_, d), "S-STL-HIDN")
    member_break(sp, P, (-180, r), (-180, -r), S, over=1.0)
    line(sp, P(-200, 0), P(T_ + 15, 0), "S-CENT")
    weld(sp, P(0, r), P(-120, 70), S, 5, all_round=True, left=True)
    # side: stile face with the rung end plug-welded flush
    xs = 260.0
    pline(sp, [P(xs, -150), P(xs + D_, -150), P(xs + D_, 150), P(xs, 150)], "S-STL", close=True)
    zbreak(sp, P(xs - 20, 150), P(xs + D_ + 20, 150), S)
    zbreak(sp, P(xs - 20, -150), P(xs + D_ + 20, -150), S)
    sp.add_circle(P(xs + D_ / 2, 0), HOLE_D / 2, dxfattribs=A("S-STL"))
    hatch(sp, [P(xs + D_ / 2 + HOLE_D / 2 * math.cos(k * math.pi / 12), HOLE_D / 2 * math.sin(k * math.pi / 12))
               for k in range(24)], "ANSI31", pscale("ANSI31", S, 0.6), "S-HATCH")
    line(sp, P(xs - 15, 0), P(xs + D_ + 15, 0), "S-CENT")
    line(sp, P(xs + D_ / 2, -40), P(xs + D_ / 2, 40), "S-CENT")
    dim(sp, P(xs, -150), P(xs + D_, -150), P(0, -150 - 8 * S), S)
    dim(sp, P(0, -150), P(T_, -150), P(0, -150 - 8 * S), S, tside="R")
    note_cfg(xL=P(-200 - 4 * S, 0)[0])
    kl = lambda z: P(-200 - 4 * S, z)
    leader(sp, P(-100, -r), kl(-70), f"RUNG Ø{RUNG_D:.0f} SOLID BAR, KNURLED", S, "L", 18)
    note_cfg(xR=P(xs + D_ + 8 * S, 0)[0])
    kr = lambda z: P(xs + D_ + 8 * S, z)
    leader(sp, P(xs + D_ / 2 + 8, 6), kr(70), f"Ø{HOLE_D:.0f} HOLE IN THE STILE, RUNG PLUG-WELDED, GROUND FLUSH",
           S, "R", 20)
    text(sp, "FRONT", P(-60, 190), 2.0 * S, "S-TEXT", TA.BOTTOM_CENTER, style="ANB")
    text(sp, "SIDE", P(xs + D_ / 2, 190), 2.0 * S, "S-TEXT", TA.BOTTOM_CENTER, style="ANB")


def bracket_detail(ox, oy):
    """B: wall bracket, plan section through the bracket: stile and bracket cut, anchor into the wall"""
    S = 5
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    xs = B / 2
    # wall cut
    WD = 110.0
    conc_cut(sp, P, [(xs - 230, U_WALL), (xs + 230, U_WALL), (xs + 230, U_WALL + WD), (xs - 230, U_WALL + WD)], S)
    zbreak(sp, P(xs - 260, U_WALL + WD), P(xs + 260, U_WALL + WD), S)
    # stile cut, rung below seen
    solid_pts = [(xs, 0), (xs + T_, 0), (xs + T_, D_), (xs, D_)]
    pline(sp, [P(*q) for q in solid_pts], "S-CUT", close=True)
    for d in (RC - RUNG_D / 2, RC + RUNG_D / 2):
        line(sp, P(xs - 200, d), P(xs, d), "S-STL-VIS")
    member_break(sp, P, (xs - 200, RC - RUNG_D / 2), (xs - 200, RC + RUNG_D / 2), S, over=1.0)
    # bracket FL cut: along the stile's outer face to the wall, bent leg on the wall
    xb = xs + T_
    leg = 130.0
    pts = [(xb, D_ - 50), (xb + BRK[1], D_ - 50), (xb + BRK[1], U_WALL - BRK[1]), (xb + leg, U_WALL - BRK[1]),
           (xb + leg, U_WALL), (xb, U_WALL)]
    pline(sp, [P(*q) for q in pts], "S-CUT", close=True)
    xa = xb + leg - 45
    anchor_in_concrete(sp, P, (xa, U_WALL), ANCH_HEF, ANCH_D, S, axis=(0.0, 1.0), plate_t=BRK[1], nuts=1)
    weld(sp, P(xb + BRK[1], D_ - 25), P(xb + 150, -15), S, 6, side="both")
    line(sp, P(xs - 230, RC), P(xs + 30, RC), "S-CENT")
    dim(sp, P(xs - 150, RC), P(xs - 150, U_WALL), P(xs - 150 - 0, 0), S, angle=90, text="<> (TOE)")
    dim(sp, P(xb, U_WALL), P(xa, U_WALL), P(0, U_WALL - 12 * S), S)
    note_cfg(xR=P(xs + 260 + 4 * S, 0)[0])
    kr = lambda y: P(xs + 260 + 4 * S, y)
    leader(sp, P(xb + leg, U_WALL - 5), kr(U_WALL - 5), f"BRACKET FL {BRK[0]:.0f} x {BRK[1]:.0f}, BENT, AT ≤ "
           f"{BRK_MAX:.0f} mm", S, "R", 16)
    leader(sp, P(xa + 8, U_WALL + ANCH_HEF - 20), kr(U_WALL + 120), f"M{ANCH_D:.0f} CHEMICAL ANCHOR, hef "
           f"{ANCH_HEF:.0f} mm, NUT AND WASHER", S, "R", 16)
    leader(sp, P(xs + T_ / 2, 15), kr(10), f"STILE FL {D_:.0f} x {T_:.0f}, CUT", S, "R", 16)


def base_detail(ox, oy):
    """C: base of a stile on the ground slab, side view"""
    S = 5
    sp = msp
    P = lambda u, z: (ox + u, oy + z)
    conc_cut(sp, P, [(-120, -160), (300, -160), (300, 0), (-120, 0)], S)
    zbreak(sp, P(-150, -160), P(330, -160), S)
    pline(sp, [P(*q) for q in [(0, 0), (BASE_PL[0], 0), (BASE_PL[0], BASE_PL[2]), (0, BASE_PL[2])]], "S-STL", close=True)
    zt = 420.0
    pline(sp, [P(0, BASE_PL[2]), P(0, zt), P(D_, zt), P(D_, BASE_PL[2])], "S-STL")
    member_break(sp, P, (0, zt), (D_, zt), S, over=1.0)
    sp.add_circle(P(RC, PITCH), RUNG_D / 2, dxfattribs=A("S-STL"))
    xa = BASE_PL[0] - 37.5
    anchor_in_concrete(sp, P, (xa, 0.0), ANCH_HEF, ANCH_D, S, plate_t=BASE_PL[2], nuts=1)
    weld(sp, P(D_, BASE_PL[2] + 4), P(150, 330), S, 6, all_round=True)
    dim(sp, P(0, 0), P(xa, 0), P(0, -160 - 7 * S), S)
    dim(sp, P(0, 0), P(BASE_PL[0], 0), P(0, -160 - 14 * S), S)
    dim(sp, P(-30, 0), P(-30, PITCH), P(-80, 0), S, angle=90, text="<> (FIRST RUNG)")
    note_cfg(xR=P(300 + 4 * S, 0)[0])
    kr = lambda z: P(300 + 4 * S, z)
    leader(sp, P(xa + 14, 40), kr(150), f"M{ANCH_D:.0f} CHEMICAL ANCHOR, hef {ANCH_HEF:.0f} mm", S, "R", 16,
           fixed=True)
    leader(sp, P(BASE_PL[0], BASE_PL[2] / 2), kr(20), f"BASE PL {BASE_PL[0]:.0f} x {BASE_PL[1]:.0f} x "
           f"{BASE_PL[2]:.0f}", S, "R", 16, fixed=True)
    leader(sp, P(250, -80), kr(-80), "GROUND SLAB OR PAD (BY THE PROJECT)", S, "R", 16, fixed=True)


# ======================================================================= 5203: cage option 1:20
def cage_detail(ox, oy):
    """optional cage, plan section looking down (dimensions ASSUMED: the client's standard governs)"""
    S = 20
    sp = msp
    P = lambda x, y: (ox + x, oy + y)
    conc_cut(sp, P, [(-500, -TOE - WALL_T), (500, -TOE - WALL_T), (500, -TOE), (-500, -TOE)], S)
    for x in (-500, 500):
        zbreak(sp, P(x, -TOE - WALL_T - 30), P(x, -TOE + 30), S)
    R, vs = cage_plan(sp, P, B, S, depth=CAGE["depth"], hoop=CAGE["hoop"], vert=CAGE["vert"], n_vert=CAGE["n_vert"],
                      stile=STILE, rung_d=RUNG_D)
    line(sp, P(0, -TOE - 30), P(0, CAGE["depth"] + 80), "S-CENT")
    dim(sp, P(0, 0), P(0, CAGE["depth"]), P(-R - 10 * S, 0), S, angle=90, text="<> (ASSUMED)")
    dim(sp, P(0, 0), P(0, -TOE), P(R + 8 * S, 0), S, angle=90)
    dim(sp, P(-R, 0), P(R, 0), P(0, -TOE - WALL_T - 8 * S), S)
    note_cfg(xR=P(R + 18 * S, 0)[0])
    kr = lambda y: P(R + 18 * S, y)
    leader(sp, P(R * 0.7, CAGE["depth"] - R + R * 0.72), kr(CAGE["depth"]), f"HOOPS FL {CAGE['hoop'][0]:.0f} x "
           f"{CAGE['hoop'][1]:.0f} AT ≤ {CAGE['hoop_max']:.0f} mm, FIRST HOOP {CAGE['start']:.0f} mm ABOVE THE BASE",
           S, "R", 22)
    leader(sp, P(*vs[-1]), kr(250), f"{CAGE['n_vert']} VERTICALS FL {CAGE['vert'][0]:.0f} x {CAGE['vert'][1]:.0f} "
           "INSIDE THE HOOPS", S, "R", 22)


# ======================================================================= tables
def geom_rows():
    names = {"pitch": "RUNG SPACING", "width": "CLEAR WIDTH BETWEEN STILES", "toe": "RUNG C/L TO THE WALL BEHIND",
             "ext": "STILES ABOVE THE LANDING", "flare": "WALK-THROUGH CLEAR WIDTH",
             "step": "RUNG C/L TO THE LANDING EDGE", "climb": "CLEAR, CLIMBING SIDE (FROM RUNG C/L)",
             "side": "CLEAR EACH SIDE OF THE LADDER C/L"}
    rows = [[names[k], f"{v[0]:.0f}", v[1], v[2]] for k, v in LIMITS.items()]
    rows.append(["FALL PROTECTION", f"CLIMB {H_CLIMB / 1000:.1f} m", f"> {FALL_H / 1000:.1f} m: LADDER SAFETY "
                 "SYSTEM OR PFAS (NOT A CAGE)", "1910.28(b)(9)"])
    return rows


def memb_rows():
    lv, s = bracket_levels()
    return [["STILES", f"FL {D_:.0f} x {T_:.0f}", "-"],
            ["RUNGS", f"Ø{RUNG_D:.0f} SOLID BAR, KNURLED, IN Ø{HOLE_D:.0f} HOLES", "A/5202"],
            ["WALL BRACKETS", f"FL {BRK[0]:.0f} x {BRK[1]:.0f} BENT, {len(lv)} No. AT {s:.0f} (≤ {BRK_MAX:.0f})",
             "B/5202"],
            ["ANCHORS", f"M{ANCH_D:.0f} CHEMICAL, hef {ANCH_HEF:.0f} mm", "B, C/5202"],
            ["BASE PLATES", f"PL {BASE_PL[0]:.0f} x {BASE_PL[1]:.0f} x {BASE_PL[2]:.0f}", "C/5202"],
            ["CAGE (OPTION)", f"HOOPS FL {CAGE['hoop'][0]:.0f} x {CAGE['hoop'][1]:.0f}, VERTICALS FL "
             f"{CAGE['vert'][0]:.0f} x {CAGE['vert'][1]:.0f}", "1/5203"]]


NOTES = [
    ("1.", "WORKED EXAMPLE OF A TYPICAL FIXED LADDER (THROUGH LADDER ONTO A ROOF SLAB). DIMENSIONS IN mm, LEVELS IN m."),
    ("2.", "GEOMETRY TO OSHA 29 CFR 1910.23 (TABLE 1). THE ENGINEER CONFIRMS THE GOVERNING CODE FOR EACH PROJECT "
           "(THAI LAW, CLIENT STANDARD)."),
    ("3.", "MEMBER SIZES, BRACKET SPACING, ANCHORS AND THE CAGE ARE ASSUMED TYPICAL VALUES (TABLE 2): DESIGN THEM "
           "FOR THE PROJECT LOADS."),
    ("4.", "RUNGS EQUAL AND LEVEL; FIRST RUNG ONE SPACE ABOVE THE BASE; TOP RUNG LEVEL WITH THE LANDING."),
    ("5.", "STEEL SS400 / S275; WELDS 6 mm FILLET UNLESS SHOWN; HOT-DIP GALVANIZED AFTER FABRICATION."),
]


# ======================================================================= build
def build():
    EXT.update({
        "FR": capture(front, 0, 0),
        "SD": capture(side, 10000, 0),
        "A": capture(rung_detail, 20000, 0),
        "B": capture(bracket_detail, 22000, 0),
        "C": capture(base_detail, 24000, 0),
        "CG": capture(cage_detail, 26000, 0),
    })
    ps = new_sheet(0)
    top = FY1 - 3
    px, pw, ph = viewport(ps, "FR", 25, FX0 + 1, top)
    view_title(ps, None, top - ph - 6, "FRONT ELEVATION (CLIMBING SIDE)", "1:25", ("1", "5201"))
    px2, pw2, ph2 = viewport(ps, "SD", 25, px + pw + 8, top)
    view_title(ps, px + pw + 8, top - ph2 - 6, "SIDE ELEVATION", "1:25", ("2", "5201"))
    ps = new_sheet(1)
    pa, wa, ha = viewport(ps, "A", 5, FX0 + 1, top)
    view_title(ps, None, top - ha - 6, "RUNG TO STILE", "1:5", ("A", "5202"))
    pb, wb, hb = viewport(ps, "B", 5, pa + wa + 8, top)
    view_title(ps, pa + wa + 8, top - hb - 6, "WALL BRACKET - PLAN SECTION", "1:5", ("B", "5202"))
    y2 = top - max(ha, hb) - 20
    pc, wc, hc = viewport(ps, "C", 5, FX0 + 1, y2)
    view_title(ps, None, y2 - hc - 6, "BASE OF A STILE", "1:5", ("C", "5202"))
    ps = new_sheet(2)
    pg, wg, hg = viewport(ps, "CG", 20, FX0 + 1, top)
    view_title(ps, None, top - hg - 6, "CAGE (OPTION) - PLAN SECTION", "1:20", ("1", "5203"))
    x2 = pg + wg + 10
    y = tbl(ps, x2, top - 6, [52, 16, 34, 26], ["ITEM", "mm", "LIMIT (mm)", "OSHA 29 CFR"], geom_rows(), "LCCC",
            title=TABT("GEOM"))
    y = tbl(ps, x2, y - 10, [30, 70, 18], ["MEMBER", "SIZE", "DETAIL"], memb_rows(), "LLC", title=TABT("MEMB"))
    notes_block(ps, x2, y - 4, 128, "NOTES", NOTES)
