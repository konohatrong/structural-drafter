"""
Project SPF - steel portal-frame building 26 x 90 m: drawing content (views and sheets), A1.

SPF-ST-0001  general notes, design criteria, connection design summary, assumptions and open items, drawing list
SPF-ST-1001  anchor bolt and column layout plan 1:200, base reactions, base plates
SPF-ST-1002  roof framing plan 1:200: rafters, purlins, sag rods, roof bracing, struts, monitor, canopies
SPF-ST-2001  side-wall elevations 1:200, gable elevations 1:100
SPF-ST-3001  typical portal frame (grids 2 - 9) 1:50, member and plate schedules
SPF-ST-5001  frame connections 1:10: knee and canopy root, column head and splice, rafter splice, ridge
SPF-ST-5002  bases, gable corner, gable rafter splices, post top, eave beam 1:10
SPF-ST-5003  bracing and strut ends, purlin and girt cleats, sag rods, fly braces 1:10 / 1:20
Every size comes from calc_spf.py (through spf_engine.D); nothing is retyped.
"""
import math

from spf_engine import *          # noqa: F401,F403
import spf_engine as SE
import calc_spf as C

doc.objects.set_wipeout_variables(frame=0)
BASE = "SPF-ST_Steel_Portal_Frame_A1_RevA"
SHEETS[:] = [("0001", ["STEEL STRUCTURE", "GENERAL NOTES AND DESIGN CRITERIA"], "N.T.S."),
             ("1001", ["ANCHOR BOLT AND", "COLUMN LAYOUT PLAN"], "AS SHOWN"),
             ("1002", ["ROOF FRAMING PLAN"], "1:200"),
             ("2001", ["SIDE-WALL AND GABLE", "ELEVATIONS"], "AS SHOWN"),
             ("3001", ["TYPICAL PORTAL FRAME", "GRIDS 2 - 9"], "AS SHOWN"),
             ("5001", ["FRAME CONNECTIONS", "KNEE, RAFTER SPLICE, RIDGE"], "1:10"),
             ("5002", ["BASES AND GABLE FRAME", "CONNECTIONS"], "1:10"),
             ("5003", ["BRACING, PURLINS, GIRTS", "AND FLY BRACES"], "AS SHOWN")]

KJ, SP, RJ, CJ, GK = D["KJ1"], D["SP1"], D["RJ1"], D["CJ1"], D["GK1"]
CS, CH = D["CS1"], D["CH1"]                       # column splice below the knee, column head piece
GS1, GS2, EB = D["GS1"], D["GS2"], D["EB1"]
BP1, BP2 = D["BP1"], D["BP2"]
BR, ST1, ST2, GU = D["BR1"], D["ST1"], D["ST2"], D["GU1"]
PU, PU2, GT, GT2, SR, FB1, FB2 = D["PU1"], D["PU2"], D["GT1"], D["GT2"], D["SR1"], D["FB1"], D["FB2"]


def bolt_txt(r, n=None):
    return f"{n or r['n_bolts']}-M{r['db']} {r['grade']}"


# ======================================================================= 0001: notes
GEN = [
    ("1.1", "THESE DRAWINGS SHOW THE STRUCTURAL STEELWORK ONLY. FOUNDATIONS, PEDESTALS, GROUND SLAB AND ALL "
            "REINFORCED CONCRETE ARE BY OTHERS (RC DESIGNER); THE BASE REACTIONS ARE GIVEN ON SPF-ST-1001."),
    ("1.2", "READ WITH THE ARCHITECTURAL DRAWINGS AND THE SPECIFICATION. REPORT ANY DISCREPANCY TO THE ENGINEER "
            "BEFORE FABRICATION. DO NOT SCALE THE DRAWINGS."),
    ("1.3", "DIMENSIONS ARE IN mm AND LEVELS IN m. LEVEL +0.000 = UNDERSIDE OF THE BASE PLATES (THE SUPPORT LEVEL "
            "OF THE ANALYSIS MODEL); THE SITE DATUM IS TBC."),
    ("1.4", "STATUS: FOR REVIEW, NOT FOR CONSTRUCTION. ITEMS MARKED TBC AND TABLE 2 MUST BE CLOSED BEFORE "
            "THE ISSUE FOR CONSTRUCTION."),
]
CRIT = [
    ("2.1", "MEMBERS: DESIGNED BY THE ENGINEER IN MIDAS GEN NX (AISC 360-16 LRFD, DIRECT ANALYSIS); SIZES AS "
            "MODELLED. LOADS: DEAD, SUPERIMPOSED DEAD 0.20 kPa, ROOF LIVE 0.50 kPa, WIND TO ASCE 7 (MWFRS, "
            "CASES 1 - 4), COMBINATIONS 1.4D; 1.2D + 1.6L; 1.2D + 1.6L + 0.5W; 1.2D + 1.0W + 0.5L; 0.9D + 1.0W."),
    ("2.2", "CONNECTIONS: DESIGNED FOR THE FACTORED FORCES OF THE MODEL (TABLE 1). MOMENT END PLATES TO AISC "
            "DESIGN GUIDE 4 (2nd ED.) FOUR-BOLT EXTENDED, THICK-PLATE METHOD, WITH THE COLUMN-SIDE CHECKS; "
            "RANGE CHECKS TO DESIGN GUIDE 16; KNEE PANEL ZONE TO DG16 CH. 5. BRACING CONNECTIONS TO DESIGN "
            "GUIDE 29 / 24. TAPERED MEMBERS: DESIGN GUIDE 25."),
    ("2.3", "PURLINS, GIRTS, SAG RODS AND FLY BRACES ARE NOT IN THE ANALYSIS MODEL: THEIR SIZES ARE PROPOSED "
            "(TBC), SEE TABLE 9 ON SPF-ST-5003."),
]
MAT = [
    ("3.1", "BUILT-UP MEMBERS, END PLATES, STIFFENERS, CONTINUITY PLATES: SM520B (JIS G 3106), Fy 365 MPa "
            "(t <= 16), 355 MPa (16 < t <= 40)."),
    ("3.2", "ROLLED SECTIONS (H 400 x 200, H 100 x 100, PURLINS, GIRTS): SS400 (JIS G 3101) UNLESS NOTED; "
            "WELDED CLEATS, GUSSETS, BASE PLATES: SM400B."),
    ("3.3", "PIPES 'PG': STK490 (JIS G 3444) - TBC (THE MODEL ASSUMED SM520)."),
    ("3.4", "BOLTS AT MOMENT END PLATES: ISO 898-1 GRADE 10.9 WITH GRADE 10 NUTS AND HARDENED WASHERS, "
            "PRETENSIONED (TURN-OF-NUT OR CALIBRATED WRENCH), NOT SLIP-CRITICAL. OTHER BOLTS: GRADE 8.8, SNUG "
            "TIGHT (BEARING), UNLESS NOTED. HOLES = BOLT + 2 mm (M24: + 3 mm) UNLESS NOTED."),
    ("3.5", f"ANCHOR RODS: {C.ROD_GRADE['name']}, HEADED, WITH LEVELLING NUTS AND PLATE WASHERS - TBC."),
    ("3.6", "WELDING ELECTRODES E49XX / E70XX. NON-SHRINK CEMENTITIOUS GROUT UNDER BASE PLATES, 30 mm."),
]
FAB = [
    ("4.1", "WELDING TO AWS D1.1; JIS STEELS ARE NOT LISTED IN D1.1: WPS QUALIFIED BY TEST. WELDERS QUALIFIED "
            "FOR THE PROCESS AND POSITION. NO UNSPECIFIED WELDS."),
    ("4.2", "WEB-TO-FLANGE WELDS OF BUILT-UP MEMBERS: CONTINUOUS FILLET 5 mm (6 mm WEB) / 6 mm (8 mm WEB), ONE "
            "SIDE, BOTH SIDES OVER 500 mm FROM EACH END PLATE AND AT EVERY STIFFENER."),
    ("4.3", "END-PLATE FLANGE WELDS AS SHOWN (CJP OR DOUBLE FILLET); WEB WELD FIRST. NO WELD ACCESS HOLES. "
            "END PLATES FLAT AFTER WELDING; MEMBERS WITH END PLATES ARE NOT CAMBERED."),
    ("4.4", "INSPECTION: 100 % VISUAL; MT ON 20 % OF FILLET WELDS AT END PLATES; UT ON 100 % OF CJP WELDS."),
    ("4.5", "SURFACE PREPARATION SA 2.5, ZINC-RICH PRIMER 75 MICRONS + FINISH TO THE SPECIFICATION (TBC). KEEP "
            "PAINT 50 mm CLEAR OF SITE WELDS. FAYING SURFACES OF END PLATES MAY BE PRIMED (NOT SLIP-CRITICAL)."),
]
ERECT = [
    ("5.1", "THE FRAME IS NOT STABLE UNTIL THE ROOF BRACING (BAYS 1 - 2 AND 9 - 10), THE EAVE BEAMS AND STRUTS, "
            "THE PURLINS AND THE FLY BRACES ARE COMPLETE: ERECT THE BRACED BAYS FIRST AND GUY THE FRAMES."),
    ("5.2", "SET THE ANCHOR RODS BY TEMPLATE. LEVEL ON THE LEVELLING NUTS; GROUT AFTER THE FRAMES ARE PLUMBED, "
            "LINED AND BRACED. WELD THE PLATE WASHERS TO THE BASE PLATES AFTER SETTING (SITE WELD)."),
    ("5.3", "PRETENSION THE END-PLATE BOLTS AFTER THE FRAME IS PLUMB. FINGER SHIMS MAY BE USED AT END PLATES "
            "(MAX. 2 PER JOINT, FULL CONTACT AT THE COMPRESSION FLANGE)."),
    ("5.4", "NO SITE WELDING OTHER THAN SHOWN WITHOUT THE ENGINEER'S APPROVAL."),
]


def weld_key(ps, x, y_top):
    text(ps, "WELD SYMBOLS (AWS A2.4)", (x, y_top - 2.8), 2.8, "S-TITLE", style="ANB")
    rows = [(dict(), 6, "FILLET, ARROW SIDE (BELOW THE LINE), LEG 6 mm"),
            (dict(side="both"), 6, "FILLET BOTH SIDES, LEG 6 mm EACH SIDE"),
            (dict(side="both", length=170), 4, "FILLET BOTH SIDES, LEG 4 mm, LENGTH 170 mm"),
            (dict(all_round=True), 6, "FILLET ALL ROUND"),
            (dict(groove="bevel", ndt="UT"), "CJP", "COMPLETE-JOINT-PENETRATION BEVEL, UT TESTED"),
            (dict(field=True), 6, "SITE WELD (FLAG)")]
    y = y_top - 10
    for kw, sz, desc in rows:
        weld(ps, (x + 4, y - 4), (x + 10, y), 1, sz, rl=26, **kw)
        text(ps, desc, (x + 50, y), 2.0, align=TA.MIDDLE_LEFT)
        y -= 8
    return y


weld_key = SE.td_engine._grouped("KEY", weld_key)


def design_rows():
    """one row per connection: governing utilisation from the calc checks"""
    rows = []
    util = {}
    for item, name, dem, cap, r, note, unit in C.CHECKS:
        if note == "MODEL MEMBER":
            continue
        k = item.split()[0]
        util[k] = max(util.get(k, 0.0), r)
    for k in ("KJ1", "CS1", "SP1", "RJ1", "CJ1", "GK1", "GS1", "GS2", "EB1"):
        r = D[k]
        f = r["forces"]
        rows.append([k, r["name"].split(" ", 1)[1].upper(), f"{f['M_neg']:.0f} / {f['M_pos']:.0f}", f"{f['V']:.0f}",
                     f"{bolt_txt(r)}, PL {r['tp']}", f"{util[k]:.2f}"])
    for k in ("BP1", "BP2"):
        b = D[k]
        rows.append([k, b["name"].split(" ", 1)[1].upper(), f"N {b['Pu']:.0f} / T {b['Tu']:.0f}", f"{b['Vu']:.0f}",
                     f"{b['rods']}-M{b['db']} RODS, PL {b['tp']}", f"{util[k]:.2f}"])
    for k in ("BR1", "ST1", "ST2"):
        b = D[k]
        rows.append([k, b["name"].split(" ", 1)[1].upper(), f"T {b['Pt']:.0f} / C {-b['Pc']:.0f}", "-",
                     f"{b['n']}-M{b['db']} 8.8, PL {b['tk']:g}", f"{util[k]:.2f}"])
    return rows


def open_rows():
    items = list(C.OPEN)
    items += [
        "Drawn geometry: columns tapered symmetrically about the grid line as analysed, the flanges straight from "
        f"the base to the cap (the taper continues above the work point: {C.TAPER['C']['d1']:.0f} at +6.000, "
        f"{CH['d1']:.0f} at the cap); rafter top flange straight in the roof plane (haunch deepens downward). "
        "Confirm, or move the column outer flange plumb.",
        "No wall bracing in the model: longitudinal stability by the eave beams H 400 x 200 in bays 1 - 2 and "
        "9 - 10 acting with the columns about their weak axis. Confirm the intent and the column weak-axis check.",
        "The MIDAS P-Delta set-up uses DL + SDL only, not each combination (DG25 6.2.6): confirm.",
        "Ridge strut CHS 190.7 x 4.5: 238 kN compression (NU2) against about 178 kN buckling over 10 m. "
        "Engineer to check (member size, grade, or the load path).",
        "Text font of the set: Arial Narrow (repository default). The office A1 font is a project setting - "
        "confirm (e.g. cordia.shx 0.90).",
        "Project name, location, drawing numbers and the site datum are placeholders.",
    ]
    return [[f"{i + 1}", fix_units(s.upper())] for i, s in enumerate(items)]


def dwg_rows():
    return [[dwg_no(s), " ".join(t), sc] for s, t, sc in SHEETS]


def sheet_0001():
    ps = new_sheet(0)
    top = FY1 - 4
    colw, gap = 150.0, 8.0
    xs = [FX0 + 4 + k * (colw + gap) for k in range(4)]
    y = notes_block(ps, xs[0], top, colw, "1. GENERAL", GEN)
    y = notes_block(ps, xs[0], y - 3, colw, "2. DESIGN CRITERIA", CRIT)
    y = notes_block(ps, xs[0], y - 3, colw, "3. MATERIALS", MAT)
    y1 = notes_block(ps, xs[1], top, colw, "4. FABRICATION, WELDING AND PROTECTION", FAB)
    y1 = notes_block(ps, xs[1], y1 - 3, colw, "5. ERECTION", ERECT)
    yk = weld_key(ps, xs[1], y1 - 4)
    yt = tbl(ps, xs[2], top - 6, [14, 44, 30, 14, 40, 12],
             ["MARK", "CONNECTION", "M- / M+ kN.m", "V kN", "BOLTS, PLATE", "UTIL."], design_rows(),
             "LLCCLC", title=TABT("DESIGN"))
    tbl(ps, xs[0], min(y, yk) - 12, [60, 150, 22], ["DRAWING No.", "TITLE", "SCALE"], dwg_rows(), "LLC",
        title=TABT("DWGS"))
    tbl(ps, xs[2], yt - 12, [8, TBX - xs[2] - 12], ["No.", "ASSUMPTION / OPEN ITEM"], open_rows(), "CL",
        title=TABT("OPEN"))


def fix_units(s):
    """units back to their case after upper(): whole words only (KNEE stays KNEE)"""
    import re
    for a, b in ((r"\bKN\.M\b", "kN.m"), (r"\bKN\b", "kN"), (r"\bMM\b", "mm"),
                 (r"\bMPA\b", "MPa"), (r"\bKPA\b", "kPa")):
        s = re.sub(a, b, s)
    return s


# ======================================================================= the frame as drawn
F = SE.Frame
K = F.knee()
TP_K, TP_S, TP_R, TP_C = KJ["tp"], SP["tp"], RJ["tp"], CJ["tp"]
X_SPL = C.X_SPLICE
PURL_X = D["purlin_layout"]["main"]
FB_X = [x for i, x in enumerate(PURL_X) if x <= X_SPL + 100 or i % 2 == 0]     # fly-braced purlins (rafter)


def splice_line(x0):
    """the splice plane through the model node at x0, perpendicular to the rafter: (top point, bottom point)"""
    zc = C.roof_z(x0)
    n = (-SIN, COS)                                   # along the plane, upward
    up = RAF.d / 2
    return (x0 + n[0] * up, zc + n[1] * up), (x0 - n[0] * up, zc - n[1] * up)


def frame_half(sp, P, side, S, can_L, detail=False):
    """one half of the typical frame, drawn in the left-half coordinates and mirrored by P for side 1"""
    import spf_details as DT
    k = K
    # ---------------- column C1, splice CS1, column head CH1 (both flanges thickened)
    zo, zi = k["col_top_out"], k["col_top_in"]
    zs, tps = CS["z"], CS["tp"]
    zl, zh = zs - tps, zs + tps
    girder(sp, P, (F.cx(0, -1), 0), (F.cx(zl, -1), zl), (F.cx(0, 1), 0), (F.cx(zl, 1), zl), F.tf_c)
    girder(sp, P, (F.cx(zh, -1), zh), (F.cx(zo, -1), zo), (F.cx(zh, 1), zh), (F.cx(zi, 1), zi), CH["tf"])
    Lh = CS["length"] / 2
    for za, zb_ in ((zl, zs), (zs, zh)):
        plate(sp, P, [(-Lh, za), (Lh, za), (Lh, zb_), (-Lh, zb_)])
    line(sp, P(0, -300), P(0, zi + 300), "S-GRID") if detail else None
    plate(sp, P, [(F.cx(zo, -1), zo), (F.cx(zi, 1), zi), (F.cx(zi, 1), zi + 12), (F.cx(zo, -1), zo + 12)])  # cap PL 12
    # base plate (seen) and grout line
    B = BP1["B"]
    plate(sp, P, [(-B / 2, 0), (B / 2, 0), (B / 2, -BP1["tp"]), (-B / 2, -BP1["tp"])])
    # ---------------- knee end plate (on the column inner flange face)
    DT.face_plate(sp, P, F.plate_x, k["plate_bot"], k["plate_top"], TP_K, 1)
    # continuity plates (seen edge-on in the column) in line with the rafter flanges (sloped with them)
    sb = (F.zb(X_SPL - 1) - F.zb(k["xb"])) / (X_SPL - 1 - k["xb"])      # haunch bottom-flange slope
    for (x0, z0), sl in (((k["xt"], k["zt"] - F.tf_h / COS / 2), SLOPE), ((k["xb"], k["zb"] + F.tf_h / 2), sb)):
        xo_, xi_ = F.cx(z0, -1) + CH["tf"], F.cx(z0, 1) - CH["tf"]
        line(sp, P(xo_, z0 + (xo_ - x0) * sl), P(xi_, z0 + (xi_ - x0) * sl), "S-STL-VIS")
    # ---------------- haunch: plate face -> splice plane
    (sx_t, sz_t), (sx_b, sz_b) = splice_line(X_SPL)
    u = (COS, SIN)
    x0t, x0b = k["xt"] + TP_K, k["xb"] + TP_K
    girder(sp, P, (x0t, F.zt(x0t)), (sx_t - TP_S * u[0], sz_t - TP_S * u[1]),
           (x0b, F.zb(x0b)), (sx_b - TP_S * u[0], sz_b - TP_S * u[1]), F.tf_h)
    for sg in (-1, 1):                                # the two splice plates
        e = TP_S * sg
        a, b = (sx_t, sz_t), (sx_b, sz_b)
        ext = SP["pf"] + SP["de"]
        nrm = (-SIN, COS)
        plate(sp, P, [off(a, nrm, ext), off(b, nrm, -ext), off(off(b, nrm, -ext), u, e), off(off(a, nrm, ext), u, e)])
    # ---------------- prismatic rafter: splice -> ridge (plumb plates)
    xr = RIDGE - TP_R
    girder(sp, P, (sx_t + TP_S * u[0], sz_t + TP_S * u[1]), (xr, F.zt(xr)),
           (sx_b + TP_S * u[0], sz_b + TP_S * u[1]), (xr, F.zb(xr)), RAF.tf)
    ext_r = (RJ["pf"] + RJ["de"]) / COS
    plate(sp, P, [(xr, F.zt(xr) + ext_r), (RIDGE, F.zt(RIDGE) + ext_r), (RIDGE, F.zb(RIDGE) - ext_r),
                  (xr, F.zb(xr) - ext_r)])
    # ---------------- canopy (end plate on the column outer flange)
    cg = DT.canopy_geom()
    (cp_, ct_), _ = DT.face_plate(sp, P, lambda z: F.cx(z, -1), cg["bot"], cg["top"], TP_C, -1)
    zt_end = F.zt(-can_L)
    u_c = (-COS, -SIN)
    a_t = DT.isect((-can_L, zt_end), u_c, cp_, ct_)
    a_b = DT.isect((-can_L, zt_end - CAN.d / COS), u_c, cp_, ct_)
    girder(sp, P, a_t, (-can_L, zt_end), a_b, (-can_L, zt_end - CAN.d / COS), CAN.tf)
    # ---------------- monitor post and rafter (H 100 x 100)
    xm = C.MON_X[0]
    zr_top = F.zt(xm)
    zm = 10_950.0                                     # model monitor eave node
    m = C.MON
    for xx in (xm - m.d / 2, xm + m.d / 2):
        line(sp, P(xx, F.zt(xx)), P(xx, zm - m.d / 2 / COS + (xx - xm) * SLOPE), "S-STL")
    zmt = lambda x: zm + SLOPE * (x - xm) + m.d / 2 / COS                         # noqa: E731
    girder(sp, P, (10_750.0, zmt(10_750.0)), (RIDGE, zmt(RIDGE)), (10_750.0, zmt(10_750.0) - m.d / COS),
           (RIDGE, zmt(RIDGE) - m.d / COS), m.tf)
    # ---------------- purlins (on the roof line, web square to the roof) and canopy purlins
    pd = PU["sec"]
    rot = math.degrees(THETA)                         # web square to the roof (P mirrors the right half)
    nrm = (-SIN, COS)
    pts = []
    for x in PURL_X + [-can_L + 300 + i * 1_100 for i in range(int((can_L - 600) // 1_100) + 1)]:
        c = off((x, F.zt(x)), nrm, pd.d / 2 + 6)
        hsec(sp, P, c, pd.d, pd.bf, pd.tw, pd.tf, rot=rot, layer="S-STL-VIS")
        pts.append(c)
    # ---------------- girts (on cleats, in one vertical wall line outside the column)
    g = GT["sec"]
    xw = F.cx(EAVE, -1) - 30 - g.d / 2
    for z in D["girt_z"]:
        hsec(sp, P, (xw, z), g.d, g.bf, g.tw, g.tf, rot=90, layer="S-STL-VIS")
        line(sp, P(F.cx(z, -1), z - 40), P(xw + g.d / 2, z - 40), "S-STL-VIS")     # cleat
    # ---------------- eave strut end-on (beyond)
    sp.add_circle(P(0, EAVE), C.STRUT.D / 2, dxfattribs=A("S-STL-HIDN"))
    # ---------------- fly braces: open triangles at the braced inside-flange points
    for x in FB_X:
        zb = F.zb(x)
        q = [P(x, zb), P(x - 60, zb - 100), P(x + 60, zb - 100)]
        pline(sp, q, "S-SYMB", close=True)
    for z in D["girt_z"]:
        xi = F.cx(z, 1)
        pline(sp, [P(xi, z), P(xi + 100, z + 60), P(xi + 100, z - 60)], "S-SYMB", close=True)
    return pts


def frame_elev(ox, oy):
    """TYPICAL FRAME, GRIDS 2 - 9, 1:50"""
    S = 50
    sp = msp
    note_cfg(free=True)
    P0 = lambda x, z: (ox + x, oy + z)                                           # noqa: E731
    P1 = lambda x, z: (ox + SPAN - x, oy + z)                                    # noqa: E731
    frame_half(sp, P0, 0, S, CAN_A)
    frame_half(sp, P1, 1, S, CAN_B)
    # grids
    for x, lab in ((0.0, "A"), (SPAN, "B")):
        gridline(sp, P0, (x, F.zt(0) + 2_200), (x, -1_400), lab, S, at="b")
    # levels
    level(sp, ox - CAN_A + 300, oy + 0, fmt_level(0), "U/S BASE PLATE", S, ext=(-6, 26))
    level(sp, ox - CAN_A + 300, oy + EAVE, fmt_level(EAVE), "EAVE (WORK POINT)", S, ext=(-6, 26))
    level(sp, ox + 1_000, oy + CS["z"], fmt_level(CS["z"]), "COLUMN SPLICE CS1", S, ext=(-6, 26))
    level(sp, ox + RIDGE + 1_600, oy + C.roof_z(RIDGE), fmt_level(C.roof_z(RIDGE)), "RIDGE (WORK POINT)", S, ext=(-36, 8))
    # dimensions
    yd = -2_300
    dim(sp, P0(-CAN_A, 0), P0(0, 0), P0(0, yd), S)
    dim(sp, P0(0, 0), P0(SPAN, 0), P0(0, yd), S)
    dim(sp, P0(SPAN, 0), P0(SPAN + CAN_B, 0), P0(0, yd), S)
    dim(sp, P0(0, 0), P0(X_SPL, 0), P0(0, yd + 900), S)
    dim(sp, P0(SPAN - X_SPL, 0), P0(SPAN, 0), P0(0, yd + 900), S)
    dim(sp, P0(X_SPL, 0), P0(RIDGE, 0), P0(0, yd + 900), S)
    dim(sp, P0(RIDGE, 0), P0(SPAN - X_SPL, 0), P0(0, yd + 900), S)
    dim(sp, P0(-CAN_A - 300, 0), P0(-CAN_A - 300, EAVE), P0(-CAN_A - 300, 0), S, angle=90)
    # slope triangle
    xs_, zs_ = 8_000.0, F.zt(8_000.0) + 900
    line(sp, P0(xs_, zs_), P0(xs_ + 1_000, zs_), "S-ANNO")
    line(sp, P0(xs_ + 1_000, zs_), P0(xs_ + 1_000, zs_ + SLOPE * 1_000), "S-ANNO")
    line(sp, P0(xs_, zs_), P0(xs_ + 1_000, zs_ + SLOPE * 1_000), "S-ANNO")
    text(sp, f"{SLOPE * 1000:.0f}", P0(xs_ + 1_100, zs_ + SLOPE * 500), 2.0 * S, align=TA.MIDDLE_LEFT)
    text(sp, "1000", P0(xs_ + 500, zs_ - 120), 2.0 * S, align=TA.TOP_CENTER)
    # member tags
    for x, z, s in ((-800, 2_600, "C1"), (SPAN + 800, 2_600, "C1"), (-650, CS["z"] + 150, "CH1"),
                    (SPAN + 650, CS["z"] + 150, "CH1"), (2_600, F.zb(2_600) - 900, "R1"),
                    (SPAN - 2_600, F.zb(2_600) - 900, "R1"), (9_000, F.zb(9_000) - 700, "R2"),
                    (SPAN - 9_000, F.zb(9_000) - 700, "R2"), (-1_900, F.zb(-1_900) - 700, "CN1"),
                    (SPAN + 2_300, F.zb(-2_300) - 700, "CN2"), (10_100, 11_200, "MR1"), (12_400, 10_300, "MP1")):
        mtag(sp, P0, (x, z), s, S)
    # detail callouts
    call = [((300, F.zt(0) - 300), 1_500, "1", "5001", "KNEE AND CANOPY ROOT", 90, (300, 9_300)),
            ((X_SPL, C.roof_z(X_SPL)), 700, "2", "5001", "RAFTER SPLICE SP1", 90, (X_SPL, 9_900)),
            ((RIDGE, C.roof_z(RIDGE)), 800, "3", "5001", "RIDGE RJ1 AND MONITOR", 0, (RIDGE + 1_600, 11_700)),
            ((0, 0), 700, "1", "5002", "BASE BP1", 0, (1_500, -900))]
    for c, r, n_, sh, what, at_, kn in call:
        tip = detail_callout(sp, P0, c, r, S, at=at_)
        leader(sp, P0(*tip), P0(*kn), f"DETAIL {n_}/{sh} - {what}", S, width=64)
    xp = SPAN - PURL_X[3]
    leader(sp, P0(xp, F.zt(xp) + 2 * PU["sec"].d), P0(xp, F.zt(xp) + 1_900),
           f"PU1 PURLINS {PU['sec'].name} (TBC), SEE 1002", S, width=70)
    leader(sp, P0(F.cx(D["girt_z"][1], -1) - 520, D["girt_z"][1]), P0(-1_100, D["girt_z"][1]),
           f"GT1 GIRTS {GT['sec'].name} (TBC)", S, side="L", width=46)
    leader(sp, P0(FB_X[2], F.zb(FB_X[2]) - 100), P0(FB_X[2] + 300, F.zb(FB_X[2]) - 1_300),
           "FLY BRACE FB1 (BOTH SIDES), SEE 5003", S, width=56)


def build():
    views()
    for i, (s, _, _) in enumerate(SHEETS):
        fn = globals().get(f"sheet_{s}")
        if fn:
            fn()
        else:
            new_sheet(i)                           # sheet still to be drawn


def views():
    """capture every view at its own model-space origin (views 100 m apart)"""
    import spf_details as DT
    import spf_plans as PL
    import spf_details2 as D2
    EXT.update({
        "FRAME": capture(frame_elev, 0.0, 0.0),
        "KNEE": capture(DT.knee_detail, 100_000.0, 0.0),
        "KFACE": capture(DT.knee_plate_face, 110_000.0, 0.0),
        "CFACE": capture(DT.canopy_plate_face, 115_000.0, 0.0),
        "CSFACE": capture(DT.splice_plan, 118_000.0, 0.0),
        "SPL": capture(DT.splice_detail, 120_000.0, 0.0),
        "SFACE": capture(DT.splice_plate_face, 125_000.0, 0.0),
        "RIDGE": capture(DT.ridge_detail, 130_000.0, 0.0),
        "APLAN": capture(PL.anchor_plan, 200_000.0, 0.0),
        "BP1P": capture(PL.base_plan, 320_000.0, 0.0, "BP1"),
        "BP2P": capture(PL.base_plan, 325_000.0, 0.0, "BP2"),
        "RPLAN": capture(PL.roof_plan, 400_000.0, 0.0),
        "SIDE": capture(PL.side_elev, 520_000.0, 0.0),
        "GABLE": capture(PL.gable_elev, 640_000.0, 0.0),
        "BP1E": capture(D2.base_elev, 700_000.0, 0.0, "BP1"),
        "BP2E": capture(D2.base_elev, 705_000.0, 0.0, "BP2"),
        "GK1": capture(D2.gable_corner, 710_000.0, 0.0),
        "GS1": capture(D2.gable_splice, 720_000.0, 0.0),
        "PTOP": capture(D2.post_top, 725_000.0, 0.0),
        "EB1": capture(D2.eave_beam, 730_000.0, 0.0),
        "BRN": capture(D2.brace_node, 740_000.0, 0.0),
        "PSEC": capture(D2.purlin_section, 750_000.0, 0.0),
    })


EXT_KEYS = {}


# ======================================================================= schedules
def girder_kg(L, d0, d1, bf, tw, tf):
    """mass of a welded tapered I-member: two flanges + the web at the mean depth (kg)"""
    dm = (d0 + d1) / 2
    return (2 * bf * tf + (dm - 2 * tf) * tw) * L * 7.85e-6


def pieces():
    """main members (one building): mark, description, section text, length (mm), number, kg each"""
    k = K
    Lc = CS["z"]                                       # base -> splice interface
    Lh = k["col_top_in"] - CS["z"]                     # splice interface -> cap (inner face)
    LR1 = (X_SPL - k["xt"]) / COS
    LR2 = (RIDGE - X_SPL) / COS
    h = T["H"]
    c0 = T["C"]
    Lc_d1 = col_d(Lc)
    out = [
        ("C1", "COLUMN, FRAMES 2 - 9 (+ SPLICE PLATE CS1)",
         f"{c0['d0']:.0f}-{Lc_d1:.0f} x {c0['bf']:.0f} x {c0['tw']:.0f} x {c0['tf']:.0f}",
         Lc, 16, girder_kg(Lc, c0["d0"], Lc_d1, c0["bf"], c0["tw"], c0["tf"])),
        ("CH1", "COLUMN HEAD, FRAMES 3 - 8 (KNEE, CANOPY ROOT)",
         f"{CH['d0']:.0f}-{CH['d1']:.0f} x {CH['bf']:.0f} x {CH['tw']:.0f} x {CH['tf']:.0f}", Lh, 12,
         girder_kg(Lh, CH["d0"], CH["d1"], CH["bf"], CH["tw"], CH["tf"])),
        ("CH1A", "COLUMN HEAD, FRAMES 2 AND 9 (+ EAVE-BEAM STUB, GUSSET)", "AS CH1", Lh, 4,
         girder_kg(Lh, CH["d0"], CH["d1"], CH["bf"], CH["tw"], CH["tf"])),
        ("R1", "RAFTER HAUNCH, FRAMES 3 - 8", f"{haunch_d(k['xt']):.0f}-{h['d1']:.0f} x {h['bf']:.0f} x {h['tw']:.0f} "
         f"x {h['tf']:.0f}", LR1, 12, girder_kg(LR1, haunch_d(k["xt"]), h["d1"], h["bf"], h["tw"], h["tf"])),
        ("R1A", "RAFTER HAUNCH, FRAMES 2 AND 9 (+ GUSSETS GU1)", "AS R1", LR1, 4,
         girder_kg(LR1, haunch_d(k["xt"]), h["d1"], h["bf"], h["tw"], h["tf"])),
        ("R2", "RAFTER, FRAMES 3 - 8", f"{RAF.d:.0f} x {RAF.bf:.0f} x {RAF.tw:.0f} x {RAF.tf:.0f}", LR2, 12,
         RAF.kg_m * LR2 / 1e3),
        ("R2A", "RAFTER, FRAMES 2 AND 9 (+ GUSSETS GU1)", "AS R2", LR2, 4, RAF.kg_m * LR2 / 1e3),
        ("CN1", "CANOPY, GRID A, FRAMES 2 - 9", f"{CAN.d:.0f} x {CAN.bf:.0f} x {CAN.tw:.0f} x {CAN.tf:.0f}",
         CAN_A / COS, 8, CAN.kg_m * CAN_A / COS / 1e3),
        ("CN2", "CANOPY, GRID B, FRAMES 2 - 9", f"{CAN.d:.0f} x {CAN.bf:.0f} x {CAN.tw:.0f} x {CAN.tf:.0f}",
         CAN_B / COS, 8, CAN.kg_m * CAN_B / COS / 1e3),
        ("MP1", "MONITOR POST, FRAMES 1 - 10", "H 100 x 100 x 6 x 8", 10_950 - 9_899, 20,
         C.MON.kg_m * 1.05),
        ("MR1", "MONITOR RAFTER, FRAMES 1 - 10", "H 100 x 100 x 6 x 8", (RIDGE - 10_750) / COS, 20,
         C.MON.kg_m * (RIDGE - 10_750) / COS / 1e3),
        ("EB1", "EAVE BEAM, BAYS 1 - 2 AND 9 - 10", "H 400 x 200 x 8 x 13", BAY - 800, 4,
         C.EAVEB.kg_m * (BAY - 800) / 1e3),
        ("ST1", "STRUT, BRACED BAYS", C.BRACE.name, BAY - 300, 8, C.BRACE.kg_m * (BAY - 300) / 1e3),
        ("ST2", "EAVE AND RIDGE STRUT", C.STRUT.name, BAY - 300, 27, C.STRUT.kg_m * (BAY - 300) / 1e3),
        ("BR1", "ROOF BRACING (X)", C.BRACE.name, math.hypot(BAY, 4_500 / COS) - 300, 24,
         C.BRACE.kg_m * (math.hypot(BAY, 4_500 / COS) - 300) / 1e3),
    ]
    return out


def member_rows():
    rows, tot = [], 0.0
    for mk, desc, sec, L, n, kg in pieces():
        rows.append([mk, desc, sec, f"{L:.0f}", f"{n}", f"{kg:.0f}", f"{n * kg:.0f}"])
        tot += n * kg
    rows.append(["", "TOTAL MAIN FRAMING (WITHOUT GABLE FRAMES, CONNECTIONS + 5 %)", "", "", "", "",
                 f"{tot * 1.05:.0f}"])
    return rows


def plate_rows():
    """TABLE 6: plates of the tapered members, one row per segment (depth perpendicular to the outer flange)"""
    c0, h = T["C"], T["H"]
    k = K
    return [["C1", "BASE -> SPLICE CS1", f"{CS['z']:.0f}", f"{c0['d0']:.0f} -> {col_d(CS['z']):.0f}",
             f"PL {c0['tw']:.0f}", f"PL {c0['tf']:.0f} x {c0['bf']:.0f}", f"PL {c0['tf']:.0f} x {c0['bf']:.0f}",
             "STRAIGHT TAPER BOTH FLANGES; CS1 PLATE SQUARE TO THE AXIS"],
            ["CH1 / CH1A", "SPLICE CS1 -> CAP", f"{k['col_top_in'] - CS['z']:.0f}",
             f"{CH['d0']:.0f} -> {CH['d1']:.0f}", f"PL {CH['tw']:.0f}", f"PL {CH['tf']:.0f} x {CH['bf']:.0f}",
             f"PL {CH['tf']:.0f} x {CH['bf']:.0f}", "SAME TAPER AS C1; BOTH FLANGES THICKENED (TBC)"],
            ["R1 / R1A", "KNEE PLATE -> SPLICE", f"{(X_SPL - k['xt']) / COS:.0f}",
             f"{haunch_d(k['xt']):.0f} -> {h['d1']:.0f}", f"PL {h['tw']:.0f}", f"PL {h['tf']:.0f} x {h['bf']:.0f}",
             f"PL {h['tf']:.0f} x {h['bf']:.0f}", "TOP FLANGE STRAIGHT, BOTTOM FLANGE TAPERED"],
            ["R2 / R2A", "SPLICE -> RIDGE", f"{(RIDGE - X_SPL) / COS:.0f}", f"{RAF.d:.0f}", f"PL {RAF.tw:.0f}",
             f"PL {RAF.tf:.0f} x {RAF.bf:.0f}", f"PL {RAF.tf:.0f} x {RAF.bf:.0f}", "PRISMATIC"]]


def sheet_3001():
    ps = new_sheet(4)
    top = FY1 - 8
    px, pw, ph = viewport(ps, "FRAME", 50, FX0 + 2, top)
    view_title(ps, None, top - ph - 6, "TYPICAL PORTAL FRAME - GRIDS 2 TO 9", "1:50", ("1", "3001"),
               note="FRAMES 2 AND 9: MARKS CH1A, R1A, R2A (BRACED BAYS); OPPOSITE HAND AT GRID B EXCEPT CN2.",
               note_w=200)
    y = top - ph - 28
    y1 = tbl(ps, FX0 + 4, y, [14, 92, 62, 18, 10, 16, 20],
             ["MARK", "MEMBER", "SECTION (mm)", "LENGTH mm", "No.", "kg EACH", "kg TOTAL"], member_rows(),
             "LLLCCCC", title=TABT("MEMB"))
    tbl(ps, FX0 + 250, y, [18, 32, 18, 26, 14, 24, 24, 110],
        ["MARK", "SEGMENT", "LENGTH mm", "DEPTH mm", "WEB", "OUTER FLANGE", "INNER FLANGE", "REMARKS"],
        plate_rows(), "LLCCCCCL", title=TABT("PLATE"))


def sheet_5001():
    ps = new_sheet(5)
    top = FY1 - 10
    px, pw, ph = viewport(ps, "KNEE", 10, FX0 + 2, top)
    view_title(ps, None, top - ph - 6, "KNEE KJ1 AND CANOPY ROOT CJ1 (GRID A; GRID B OPPOSITE HAND)", "1:10",
               ("1", "5001"))
    x2 = px + pw + 6
    px2, pw2, ph2 = viewport(ps, "KFACE", 10, x2, top)
    view_title(ps, None, top - ph2 - 6, "VIEW ON KNEE PLATE", "1:10", ("A", "5001"))
    x3 = px2 + pw2 + 6
    px3, pw3, ph3 = viewport(ps, "CFACE", 10, x3, top)
    view_title(ps, None, top - ph3 - 6, "VIEW ON CANOPY PLATE", "1:10", ("B", "5001"))
    y4 = min(top - ph2, top - ph3) - 24
    _, _, ph4 = viewport(ps, "CSFACE", 10, x2, y4)
    view_title(ps, None, y4 - ph4 - 6, "VIEW ON COLUMN SPLICE PLATE CS1 (C1 PLATE, CH1 REMOVED)", "1:10",
               ("D", "5001"))
    y2 = min(top - ph - 26, top - ph2 - 26, top - ph3 - 26)
    qx, qw, qh = viewport(ps, "SPL", 10, FX0 + 2, y2)
    view_title(ps, None, y2 - qh - 6, "RAFTER SPLICE SP1", "1:10", ("2", "5001"))
    rx, rw, rh = viewport(ps, "SFACE", 10, qx + qw + 6, y2)
    view_title(ps, None, y2 - rh - 6, "VIEW ON SPLICE PLATE", "1:10", ("C", "5001"))
    sx, sw, sh_ = viewport(ps, "RIDGE", 10, rx + rw + 8, y2)
    view_title(ps, None, y2 - sh_ - 6, "RIDGE RJ1 AND MONITOR POST BASES MB1", "1:10", ("3", "5001"))


def reaction_rows():
    rows = []
    for key, xs, frames in (("BP1", (0.0, SPAN), C.FRAMES_Y), ("BP2", C.GABLE_POSTS, C.END)):
        r = C.reactions(xs, frames)
        mx = max(r, key=lambda q: q[3])
        mn = min(r, key=lambda q: q[3])
        hx = max(r, key=lambda q: abs(q[1]))
        hy = max(r, key=lambda q: abs(q[2]))
        rows.append([key, f"{mx[3]:.0f} ({mx[0]})", f"{-mn[3]:.0f} ({mn[0]})" if mn[3] < 0 else "-",
                     f"{abs(hx[1]):.0f} ({hx[0]})", f"{abs(hy[2]):.0f} ({hy[0]})"])
    return rows


def sheet_1001():
    ps = new_sheet(1)
    top = FY1 - 10
    px, pw, ph = viewport(ps, "APLAN", 200, FX0 + 2, top)
    view_title(ps, None, top - ph - 6, "ANCHOR BOLT AND COLUMN LAYOUT PLAN", "1:200", ("1", "1001"),
               note="BASE PLATES CENTRED ON THE GRID INTERSECTIONS (COLUMNS) AND ON THE POST SET-OUT LINES.",
               note_w=200)
    x2 = TBX - 158
    qx, qw, qh = viewport(ps, "BP1P", 10, x2, top)
    view_title(ps, None, top - qh - 6, "BP1 - FRAME COLUMN BASE (PLAN)", "1:10", ("2", "1001"))
    rx, rw, rh = viewport(ps, "BP2P", 10, x2, top - qh - 30)
    view_title(ps, None, top - qh - 30 - rh - 6, "BP2 - GABLE POST BASE (PLAN)", "1:10", ("3", "1001"))
    y = min(top - ph - 30, top - qh - 30 - rh - 26)
    tbl(ps, FX0 + 4, y, [16, 62, 62, 62, 62],
        ["BASE", "MAX. COMPRESSION kN (CASE)", "MAX. UPLIFT kN (CASE)", "MAX. SHEAR X kN (CASE)",
         "MAX. SHEAR Y kN (CASE)"], reaction_rows(), "LCCCC", title=TABT("REAC"))
    notes_block(ps, FX0 + 300, y, 300, "ANCHOR ROD NOTES", [
        ("1", "REACTIONS ARE FACTORED (LRFD) FROM THE MIDAS MODEL, X ACROSS THE SPAN, Y ALONG THE BUILDING; FOR THE "
              "PEDESTAL, FOOTING AND ANCHORAGE DESIGN BY THE RC DESIGNER."),
        ("2", f"ANCHOR RODS {C.ROD_GRADE['name']}, HEADED, EMBEDMENT AND EDGE DISTANCES BY THE RC DESIGNER "
              f"(MIN. {BP1['embed']:.0f} mm); SET BY TEMPLATE, TOLERANCE +/- 3 mm IN PLAN, +/- 10 mm IN LEVEL."),
        ("3", "LEVELLING NUTS UNDER THE PLATE; GROUT 30 mm AFTER PLUMBING AND BRACING."),
    ])


def sheet_1002():
    ps = new_sheet(2)
    top = FY1 - 10
    px, pw, ph = viewport(ps, "RPLAN", 200, FX0 + 2, top)
    view_title(ps, None, top - ph - 6, "ROOF FRAMING PLAN", "1:200", ("1", "1002"),
               note="PHANTOM LINES = ROOF BRACING AND STRUTS; DASHED = SAG RODS; HIDDEN = MONITOR ROOF EDGE ABOVE.",
               note_w=220)
    y = top - ph - 34
    tbl(ps, FX0 + 4, y, [16, 80, 52, 56],
        ["MARK", "MEMBER", "SECTION", "REMARK"], roof_rows(), "LLLL", title=TABT("SEC"))


def roof_rows():
    pl = D["purlin_layout"]
    return [["PU1", "ROOF PURLIN, SIMPLE SPAN 10 m", PU["sec"].name, f"AT {pl['spacing_slope']:.0f} mm ON SLOPE - TBC"],
            ["PU2", "CANOPY PURLIN", PU2["sec"].name, "AT ABOUT 1100 mm - TBC"],
            ["GT1", "SIDE-WALL GIRT, SIMPLE SPAN 10 m", GT["sec"].name, "AT 1500 mm - TBC"],
            ["GT2", "GABLE GIRT, BETWEEN POSTS", GT2["sec"].name, "AT 1500 mm - TBC"],
            ["SR1", "SAG ROD AT THIRD POINTS", f"ROUND BAR Ø{SR['d']}", "THREADED BOTH ENDS - TBC"],
            ["FB1 / FB2", "FLY BRACE, RAFTER / COLUMN", f"{FB1['angle']} / {FB2['angle']}", "SEE 5003 - TBC"],
            ["BR1", "ROOF X-BRACING", C.BRACE.name, "BAYS 1 - 2 AND 9 - 10"],
            ["ST1 / ST2", "STRUTS: BRACED BAYS / EAVE AND RIDGE", f"{C.BRACE.name} / {C.STRUT.name}", ""]]


def sheet_2001():
    ps = new_sheet(3)
    top = FY1 - 10
    px, pw, ph = viewport(ps, "SIDE", 200, FX0 + 2, top)
    view_title(ps, None, top - ph - 6, "SIDE-WALL ELEVATION - GRID A (GRID B SIMILAR)", "1:200", ("1", "2001"))
    y2 = top - ph - 30
    qx, qw, qh = viewport(ps, "GABLE", 100, FX0 + 2, y2)
    view_title(ps, None, y2 - qh - 6, "GABLE ELEVATION - GRID 1 (GRID 10 SIMILAR, OPPOSITE HAND)", "1:100",
               ("2", "2001"))


# ======================================================================= 5002, 5003 and their tables
def bolt_len(d, grip):
    """grip + 2 washers (4 mm) + nut (0.8 d) + 3 thread pitches, rounded up to 5 mm (S8.1)"""
    pitch = {12: 1.75, 16: 2.0, 20: 2.5, 22: 2.5, 24: 3.0, 27: 3.0, 30: 3.5}[d]
    return 5 * math.ceil((grip + 8 + 0.8 * d + 3 * pitch) / 5)


def ep_rows():
    rows = []
    where = {"KJ1": "KNEE, FRAMES 2 - 9 (16 No.)", "CS1": "COLUMN SPLICE, FRAMES 2 - 9 (16 No.)",
             "CJ1": "CANOPY ROOT, FRAMES 2 - 9 (16 No.)",
             "SP1": "RAFTER SPLICE, FRAMES 2 - 9 (16 No.)", "RJ1": "RIDGE, FRAMES 2 - 9 (8 No.)",
             "GK1": "GABLE CORNER (4 No.)", "GS1": "GABLE RAFTER SPLICE (4 No.)", "GS2": "GABLE RIDGE (2 No.)",
             "EB1": "EAVE BEAM SPLICE (4 No.)"}
    for k, w in where.items():
        r = D[k]
        Lp = r["length"]
        if k == "KJ1":
            Lp = K["plate_len"]
        if k == "CJ1":
            import spf_details as DT
            Lp = DT.canopy_geom()["length"]
        rows.append([k, w, f"{r['tp']} x {r['bp']:.0f} x {Lp:.0f}", bolt_txt(r), f"{r['g']:.0f}",
                     f"{r['pf']:.0f} / {r['de']:.0f}", r["flange_weld"], f"{r['web_weld']}",
                     f"{r['Mu']:.0f} ({r['case']})"])
    return rows


def bolt_rows():
    """field bolts, one building (+ 2 % spare to be supplied)"""
    def grip(k):
        r = D[k]
        if k == "KJ1":
            return r["tp"] + r["column"]["tf_used"]
        if k == "CJ1":
            return r["tp"] + CH["tf"]
        if k == "GK1":
            return r["tp"] + r["column"]["tf_used"]
        return 2 * r["tp"]
    n_of = {"KJ1": 16, "CS1": 16, "CJ1": 16, "SP1": 16, "RJ1": 8, "GK1": 4, "GS1": 4, "GS2": 2, "EB1": 4}
    rows = []
    for k, n in n_of.items():
        r = D[k]
        rows.append([k, f"M{r['db']} x {bolt_len(r['db'], grip(k))}", "10.9 / NUT 10 / 2 HARDENED WASHERS",
                     f"{r['n_bolts'] * n}", f"{r['hole']}", "PRETENSIONED"])
    for k, n, desc in (("BR1", 48, "BR1 ENDS"), ("ST1", 16, "ST1 ENDS"), ("ST2", 54, "ST2 ENDS")):
        r = D[k]
        rows.append([k, f"M{r['db']} x {bolt_len(r['db'], r['tk'] + D['GU1']['tg'])}", "8.8 / NUT 8 / 1 WASHER",
                     f"{r['n'] * n}", f"{r['hole']}", "SNUG TIGHT"])
    rows.append(["MB1", f"M{D['MB1']['db']} x {bolt_len(D['MB1']['db'], D['MB1']['tp'] + C.RAF.tf)}",
                 "8.8 / NUT 8 / 1 WASHER", f"{4 * 20}", "18", "SNUG TIGHT"])
    rows.append(["POST TOP", f"M16 x {bolt_len(16, 12 + C.GRAF.tf)}", "8.8 / NUT 8 / 1 WASHER", "40", "18", "SNUG TIGHT"])
    return rows


def sheet_5002():
    ps = new_sheet(6)
    top = FY1 - 10
    px, pw, ph = viewport(ps, "BP1E", 10, FX0 + 2, top)
    view_title(ps, None, top - ph - 6, "BASE BP1 - FRAME COLUMN", "1:10", ("1", "5002"))
    qx, qw, qh = viewport(ps, "BP2E", 10, px + pw + 8, top)
    view_title(ps, None, top - qh - 6, "BASE BP2 - GABLE POST", "1:10", ("5", "5002"))
    tx, tw_, th = viewport(ps, "PTOP", 10, qx + qw + 8, top)
    view_title(ps, None, top - th - 6, "GABLE POST TOP", "1:10", ("4", "5002"))
    y2 = min(top - ph, top - qh, top - th) - 24
    rx, rw, rh = viewport(ps, "GK1", 10, FX0 + 2, y2)
    view_title(ps, None, y2 - rh - 6, "GABLE CORNER GK1 (RAFTER OVER COLUMN)", "1:10", ("2", "5002"))
    ux, uw, uh = viewport(ps, "EB1", 10, rx + rw + 10, y2)
    view_title(ps, None, y2 - uh - 6, "EAVE BEAM EB1 AT THE COLUMN (PLAN AT THE EAVE)", "1:10", ("6", "5002"))
    y3 = min(y2 - rh, y2 - uh) - 24
    sx, sw, sh_ = viewport(ps, "GS1", 10, FX0 + 2, y3)
    view_title(ps, None, y3 - sh_ - 6, "GABLE RAFTER SPLICE GS1 (GS2 AT THE RIDGE POST SIMILAR, PLUMB)", "1:10",
               ("3", "5002"))


def sheet_5003():
    ps = new_sheet(7)
    top = FY1 - 10
    px, pw, ph = viewport(ps, "BRN", 10, FX0 + 2, top)
    view_title(ps, None, top - ph - 6, "BRACED-BAY NODE: BR1 / ST1 ON GUSSET GU1 (ROOF PLANE)", "1:10", ("1", "5003"),
               note="ST2 (EAVE AND RIDGE STRUTS) SIMILAR: 3 BOLTS, KNIFE PL AS TABLE 8; AT THE EAVE ON A FIN PL "
                    "WELDED TO THE COLUMN WEB.", note_w=150)
    y2 = top - ph - 36
    qx, qw, qh = viewport(ps, "PSEC", 10, FX0 + 2, y2)
    view_title(ps, None, y2 - qh - 6, "SECTION AT A FLY-BRACED PURLIN (GIRTS AND FB2 SIMILAR)", "1:10",
               ("2", "5003"))
    y = y2 - qh - 30
    y1 = tbl(ps, FX0 + 4, y, [12, 58, 30, 30, 12, 18, 14, 10, 40],
             ["MARK", "LOCATION", "PLATE t x b x L mm", "BOLTS", "g mm", "pf / de mm", "FLANGE WELD", "WEB",
              "Mu* kN.m (CASE)"], ep_rows(), "LLCCCCCCC", title=TABT("EP"))
    tbl(ps, FX0 + 4, y1 - 14, [16, 26, 64, 14, 16, 30],
        ["MARK", "BOLT mm", "GRADE / NUT / WASHERS", "No.", "HOLE Ø", "TIGHTENING"], bolt_rows(), "LCLCCC",
        title=TABT("BOLT"))
    notes_block(ps, FX0 + 360, y, 300, "CONNECTION NOTES", [
        ("1", "BOLT No. = ONE BUILDING; SUPPLY 2 % SPARE OF EACH SIZE. NO LOCK WASHERS ON HIGH-STRENGTH BOLTS."),
        ("2", "END PLATES: FLANGE WELDS CJP WHERE SHOWN, UT 100 %; DOUBLE FILLETS OTHERWISE. NO WELD ACCESS HOLES. "
              "WEB WELD FIRST."),
        ("3", "SECONDARY FRAMING (PURLINS, GIRTS, SAG RODS, FLY BRACES, CLEATS) IS PROPOSED - TBC (TABLE 9, 1002)."),
        ("4", "FLY BRACES FB1 AT EVERY PURLIN OVER THE HAUNCH AND AT EVERY SECOND PURLIN BEYOND; FB2 AT EVERY GIRT "
              "(INSIDE FLANGE OF THE COLUMNS), BOTH SIDES."),
    ])
