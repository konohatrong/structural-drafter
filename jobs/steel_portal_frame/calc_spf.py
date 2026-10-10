"""
Project SPF - steel portal-frame building 26 x 90 m: connection design and secondary framing, from the MIDAS GEN NX
model (model/spf_model.json, model/spf_forces.json, written by pull_model.py). The members themselves are the
engineer's design in MIDAS (sizes, code check); this calc designs what the model does not hold:

  * moment end plates: knee, haunch splice, ridge, canopy roots, gable rafter knee and splices
    (AISC DG4 2nd ed. 4E thick-plate method with the column side; DG16 for the range checks; AISC 360-16)
  * knee panel zone (DG16 Ch.5 mapped to 360-16 G2), continuity plates (DG4 step 19, 360-16 J10)
  * base plates and anchor rods (pinned bases), eave-beam and strut / brace end connections (DG29 / DG24 knife plate)
  * purlins, girts, sag rods and fly braces: PROPOSED sizes (not in the model), marked TBC on the drawings

Every number on the drawings comes from design(); nothing is retyped. Units: N, mm, MPa unless a name says kN, kN.m.
Sources: docs/steel/reference/SOURCES_STEEL_DETAILING.md Parts F (DG4), G (DG16), H (DG25), I (DG29), D (DG24).

usage: python calc_spf.py        prints the design report and every check; exit 1 if a check fails without a note
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL = json.loads((HERE / "model" / "spf_model.json").read_text(encoding="utf-8"))
FORCES = json.loads((HERE / "model" / "spf_forces.json").read_text(encoding="utf-8"))

# =========================================================================== basis (assumed: open items in README)
E = 200_000.0                       # AISC 360-16 (the MIDAS model uses 205 000 for the analysis)
FEXX = 490.0                        # E49XX / E70 electrodes
FC_PED = 24.0                       # pedestal concrete f'c, MPa (RC by others: ASSUMED, confirm)
BOLT_GRADE_MOMENT = "10.9"          # user 2026-10-04: ISO 898 grade 8.8 / 10.9 - 10.9 pretensioned at moment end plates
BOLT_GRADE_SHEAR = "8.8"            # 8.8 bearing type (snug) for bracing, struts, purlins, girts, fly braces
ROD_GRADE = dict(name="ASTM F1554 GR 36 (OR JIS SS400 ROUND BAR)", Fy=250.0, Fu=400.0)   # anchor rods: ASSUMED
CHECKS = []                         # (item, check, demand, capacity, ratio, note)
OPEN = []                           # assumptions / open items raised by the calc


def fy_sm520(t):
    """JIS G 3106 SM520: 365 MPa for t <= 16, 355 for 16 < t <= 40, 335 for 40 < t <= 75"""
    return 365.0 if t <= 16 else 355.0 if t <= 40 else 335.0


FU_SM520 = 520.0
SS400 = dict(Fy=245.0, Fu=400.0)    # rolled secondary sections (purlins, girts, angles): SS400, Fy 245 (t <= 16)
SM400 = dict(Fy=245.0, Fu=400.0)    # welded cleats and gussets of the secondary framing (S1.3: SM400B)
STK = dict(name="STK490 (JIS G 3444)", Fy=315.0, Fu=490.0)   # pipes "PG": STK490 ASSUMED; the model used SM520

# 360-16 Table J3.1M pretension (kN), J3.3M standard hole, J3.4M minimum edge distance
PRETENSION = {"10.9": {16: 114, 20: 179, 22: 221, 24: 257, 27: 334, 30: 408},   # Group B
              "8.8": {12: 50, 16: 91, 20: 142, 22: 176, 24: 205, 27: 267, 30: 326}}
HOLE = {12: 14, 16: 18, 20: 22, 22: 24, 24: 27, 27: 30, 30: 33}
EDGE_MIN = {12: 18, 16: 22, 20: 26, 22: 28, 24: 30, 27: 34, 30: 38}
BOLT = {"10.9": dict(Fu=1040.0, Fnt=0.75 * 1040, Fnv=0.45 * 1040),          # Fnt 780, Fnv(N) 468 MPa
        "8.8": dict(Fu=830.0, Fnt=0.75 * 830, Fnv=0.45 * 830)}               # Fnt 622, Fnv(N) 374 MPa
PLATES = (10, 12, 16, 20, 22, 25, 28, 32, 36, 40)
LEGS = (5, 6, 8, 10, 12)


def check(item, name, demand, capacity, note="", unit=""):
    r = abs(demand) / capacity if capacity else float("inf")
    CHECKS.append((item, name, round(demand, 1), round(capacity, 1), round(r, 3), note, unit))
    return r


def ceil5(x):
    return 5 * math.ceil(x / 5 - 1e-9)


def pick(options, need):
    for o in options:
        if o >= need - 1e-9:
            return o
    return options[-1]


# =========================================================================== sections
class I:
    """doubly symmetric welded or rolled I-section (mm); r = root fillet (0 for welded)"""

    def __init__(self, name, d, bf, tw, tf, r=0.0, Fy=None):
        self.name, self.d, self.bf, self.tw, self.tf, self.r = name, d, bf, tw, tf, r
        self.Fy = Fy or fy_sm520(max(tf, tw))
        h = d - 2 * tf
        self.A = 2 * bf * tf + h * tw + (4 - math.pi) * r * r
        self.Ix = (bf * d ** 3 - (bf - tw) * h ** 3) / 12
        self.Iy = (2 * tf * bf ** 3 + h * tw ** 3) / 12
        self.Sx = self.Ix / (d / 2)
        self.Zx = bf * tf * (d - tf) + tw * h * h / 4
        self.Zy = tf * bf * bf / 2 + h * tw * tw / 4
        self.ry = math.sqrt(self.Iy / self.A)
        self.J = (2 * bf * tf ** 3 + h * tw ** 3) / 3
        self.ho = d - tf
        self.Cw = self.Iy * self.ho ** 2 / 4
        self.kg_m = self.A * 7.85e-3

    def __repr__(self):
        return self.name


def sec_from_model(sid):
    s = MODEL["SECT"][str(sid)]
    v = s["SECT_BEFORE"].get("SECT_I", {}).get("vSIZE")
    if v:
        d, bf, tw, tf = (x * 1000 for x in v[:4])
        return I(s["SECT_NAME"], d, bf, tw, tf)
    return None


# JIS rolled shapes used by the model (DB sections) and by the proposed secondary framing: d, bf, tw, tf, r
JIS_H = {"H 400x200x8/13": (400, 200, 8, 13, 16), "H 100x100x6/8": (100, 100, 6, 8, 8),
         "H 125x60x6x8": (125, 60, 6, 8, 8), "H 150x75x5x7": (150, 75, 5, 7, 8),
         "H 175x90x5x8": (175, 90, 5, 8, 9), "H 200x100x5.5x8": (200, 100, 5.5, 8, 11),
         "H 250x125x6x9": (250, 125, 6, 9, 12)}
PIPES = {"PG 165.2x4.5": (165.2, 4.5), "PG 190.7x4.5": (190.7, 4.5)}


def jis(name, Fy=None):
    d, bf, tw, tf, r = JIS_H[name]
    return I(name.replace("x", " x ").replace("/", " x ").replace("H ", "H "), d, bf, tw, tf, r, Fy)


class Pipe:
    def __init__(self, name):
        self.name = name
        self.D, self.t = PIPES[name]
        self.A = math.pi * (self.D - self.t) * self.t
        self.I = math.pi / 64 * (self.D ** 4 - (self.D - 2 * self.t) ** 4)
        self.r = math.sqrt(self.I / self.A)
        self.kg_m = self.A * 7.85e-3


# members of the model (names as in MIDAS; the drawn sizes follow them)
TAPER = {"C": dict(d0=300.0, d1=800.0, bf=250.0, tw=8.0, tf=14.0, L=6000.0),         # column, base -> top
         "H": dict(d0=800.0, d1=350.0, bf=250.0, tw=6.0, tf=12.0, Lx=5200.0)}         # haunch, knee -> splice
RAF = sec_from_model(2102)          # prismatic rafter 350 x 200 x 6 x 10
CAN = sec_from_model(203)           # canopy rafter 400 x 200 x 6 x 10 (frames 2 - 9); gable rafter 204 the same
GRAF = sec_from_model(204)
GPOST = sec_from_model(102)         # gable post 400 x 150 x 6 x 10
GTIE = sec_from_model(301)          # gable eave tie 200 x 100 x 4 x 6
EAVEB = jis("H 400x200x8/13")       # eave beam, end bays (302)
MON = jis("H 100x100x6/8")          # monitor posts (401) and rafters (402)
BRACE = Pipe("PG 165.2x4.5")        # braced-bay struts (901); the model's roof X-bracing (902) too
STRUT = Pipe("PG 190.7x4.5")        # eave and ridge struts (903)


class Angle:
    """equal-leg angle, JIS G 3192: b, t, A (mm2), c (centroid from the heel, mm), rx, rz (mm), kg/m"""
    TABLE = {"L 90x90x6": (90.0, 6.0, 1055.0, 24.2, 27.7, 17.8, 8.28),
             "L 90x90x7": (90.0, 7.0, 1222.0, 24.6, 27.6, 17.8, 9.59),
             "L 100x100x7": (100.0, 7.0, 1362.0, 27.1, 30.8, 19.8, 10.7)}

    def __init__(self, name):
        self.name = name
        self.b, self.t, self.A, self.c, self.rx, self.rz, self.kg_m = self.TABLE[name]


# roof X-bracing BR1 (engineer, 10/10/2026, markup of 1/5003: "try roof brace as this detail"): single angles
# L 90 x 90 x 6 bolted straight to an enlarged gusset GU1, no knife plates; one brace of each X on top of the gussets,
# the other below them, bolted back to back at the crossing through a packing the gusset's thickness
BRACE_L = Angle("L 90x90x6")
GAUGE = {90: 50.0, 100: 55.0}       # bolt gauge from the heel (JIS standard gauge g1)


def taper_d(kind, s):
    """depth of the tapered column (s = height above the base) or haunch (s = horizontal distance from the column
    centre line), as modelled: linear between the end depths (MIDAS tapered group, linear)"""
    t = TAPER[kind]
    L = t["L"] if kind == "C" else t["Lx"]
    return t["d0"] + (t["d1"] - t["d0"]) * min(max(s / L, 0.0), 1.0)


def col_depth(z):
    """depth of the column as fabricated: its flanges are straight from the base to the cap, so the model taper
    (300 at the base, 800 at the work point Z 6.000) continues above the work point into the knee"""
    t = TAPER["C"]
    return t["d0"] + (t["d1"] - t["d0"]) * max(z, 0.0) / t["L"]


# =========================================================================== geometry from the model
N = {int(k): (v["X"] * 1000, v["Y"] * 1000, v["Z"] * 1000) for k, v in MODEL["NODE"].items()}
ELEM = {int(k): v for k, v in MODEL["ELEM"].items()}
SPAN = 26_000.0
BAY = 10_000.0
NBAY = 9
FRAMES_Y = [i * BAY for i in range(NBAY + 1)]                  # grid 1 .. 10
EAVE_Z = 6_000.0
RIDGE_X = SPAN / 2
SLOPE = (max(p[2] for p in N.values() if abs(p[0] - RIDGE_X) < 1 and abs(p[1] - 10_000) < 1
             and p[2] < 10_500) - EAVE_Z) / RIDGE_X
THETA = math.atan(SLOPE)                                       # roof slope from the model work lines
X_SPLICE = 5_200.0                                             # haunch / prismatic rafter joint (model node)
CAN_L = (3_300.0, 4_200.0)                                     # canopy projections at grid A, grid B
MON_X = (12_000.0, 14_000.0)                                   # monitor posts
GABLE_POSTS = (4_500.0, 8_500.0, 13_000.0, 17_500.0, 21_500.0)


def roof_z(x):
    """model work line of the rafter (centre line) at x (0 .. SPAN)"""
    return EAVE_Z + SLOPE * (x if x <= RIDGE_X else SPAN - x)


def find_elem(sect, pred):
    return [k for k, e in ELEM.items() if e["SECT"] == sect and pred(N[e["NODE"][0]], N[e["NODE"][1]])]


def at(p, x=None, y=None, z=None, tol=2.0):
    return all(v is None or abs(c - v) < tol for c, v in zip(p, (x, y, z)))


# =========================================================================== forces at joints
COMP = FORCES["components"]          # N, Vy, Vz, T, My, Mz (kN, kN.m), element local axes
DESIGN_CASES = FORCES["design_cases"]


def end_forces(elem, node):
    """concurrent design forces {case: dict(N, V, M, ...)} at the end of 'elem' that sits on 'node'"""
    e = ELEM[elem]
    part = "I" if e["NODE"][0] == node else "J"
    rows = FORCES["concurrent"].get(f"{elem}/{part}", {})
    return {c: dict(zip(COMP, v)) for c, v in rows.items() if c in DESIGN_CASES}


def joint_cases(pairs):
    """[(elem, node), ...] -> list of (case, N, V, M) over all design cases and all the listed element ends"""
    out = []
    for el, nd in pairs:
        for c, f in end_forces(el, nd).items():
            out.append((c, f["N"], f["Vz"], f["My"], el))
    return out


def node_at(x, y, z, tol=5.0):
    for k, p in N.items():
        if at(p, x, y, z, tol):
            return k
    raise KeyError((x, y, z))


def ends_at(node, sects):
    return [k for k, e in ELEM.items() if e["SECT"] in sects and node in e["NODE"][:2]]


# =========================================================================== end plates (DG4 4E, thick plate)
def yp_4e(bp, g, pfi, pfo, h0, h1):
    """DG4 Table 3.1 / DG16 Table 4-2, four-bolt extended unstiffened"""
    s = 0.5 * math.sqrt(bp * g)
    pfi = min(pfi, s)
    return bp / 2 * (h1 * (1 / pfi + 1 / s) + h0 / pfo - 0.5) + 2 / g * h1 * (pfi + s), s


def yc_4bolt(bfc, g, pfi, pfo, tf, h0, h1, ts=None):
    """DG4 Table 3.4 column flange, four-bolt: unstiffened, or stiffened by continuity plates ts thick"""
    s = 0.5 * math.sqrt(bfc * g)
    c = pfo + tf + pfi
    if ts is None:
        return bfc / 2 * (h1 / s + h0 / s) + 2 / g * (h1 * (s + 3 * c / 4) + h0 * (s + c / 4) + c * c / 2) + g / 2
    ps = (c - ts) / 2
    psi = min(ps, s)
    return bfc / 2 * (h1 * (1 / s + 1 / psi) + h0 * (1 / s + 1 / ps)) + 2 / g * (h1 * (s + psi) + h0 * (s + ps))


def endplate(name, d, bf, tf, tw, cases, *, column=None, bp=None, g=None, grade=BOLT_GRADE_MOMENT, note="",
             db_min=20):
    """Four-bolt extended end plate, symmetric (extended at both flanges: the moment reverses), DG4 thick-plate
    procedure. d, tf: depth and flange measured PERPENDICULAR to the member axis at the plate (conservative for a
    plumb or sloped plate, DG16 digest 6.2). cases: [(case, N kN, V kN, M kN.m, elem)]; N > 0 tension.
    column: dict(bfc, tfc, twc, dc, top) for the beam-to-column side (DG4 steps 14 - 19); None for a splice
    (the mating plate is the same plate)."""
    bp = bp or bf + 20.0
    g = g or (140.0 if bf >= 240 else 110.0 if bf >= 190 else 90.0)
    # effective moment: |M| + tension x (d - tf)/2 (DG16 2.1, DG4 digest 5); compression relief ignored
    worst = max(cases, key=lambda c: abs(c[3]) * 1e3 + max(0.0, c[1]) * (d - tf) / 2)
    Mu = abs(worst[3]) * 1e6 + max(0.0, worst[1]) * 1e3 * (d - tf) / 2      # N.mm
    Vu = max(abs(c[2]) for c in cases) * 1e3
    Fnt = BOLT[grade]["Fnt"]
    out = None
    for db in (d_ for d_ in (16, 20, 22, 24, 27, 30) if d_ >= db_min):      # M20 minimum in moment end plates
        pf = ceil5(max(db + (13 if db <= 24 else 19), 1.75 * db, tf + 25.0))   # flange face -> bolt (DG4 4.1, wrench)
        de = ceil5(max(EDGE_MIN[db] + 4, 1.5 * db))
        h0 = d + pf - tf / 2
        h1 = d - tf - pf - tf / 2
        Pt = Fnt * math.pi * db * db / 4
        phiMnp = 0.75 * 2 * Pt * (h0 + h1)
        if phiMnp >= Mu:
            out = dict(db=db, pf=pf, de=de, h0=h0, h1=h1, Pt=Pt, phiMnp=phiMnp)
            break
    if out is None:
        raise SystemExit(f"!! {name}: no bolt size up to M30 for Mu = {Mu / 1e6:.0f} kN.m")
    db, pf, de, h0, h1 = out["db"], out["pf"], out["de"], out["h0"], out["h1"]
    Yp, s = yp_4e(min(bp, bf + 25), g, pf, pf, h0, h1)
    tp = None
    for t in PLATES:
        tpr = math.sqrt(1.11 * out["phiMnp"] / (0.9 * fy_sm520(t) * Yp))
        if t >= tpr:
            tp, tp_req = t, tpr
            break
    if tp is None:
        raise SystemExit(f"!! {name}: end plate thicker than 40 mm")
    Fyp = fy_sm520(tp)
    Ffu = Mu / (d - tf)
    # 4E extension: shear yield and rupture (DG4 Eq 3.12 - 3.14; 360-16 J4.2 phi 1.0 / 0.75)
    check(name, "extension shear yield", Ffu / 2 / 1e3, 1.0 * 0.6 * Fyp * bp * tp / 1e3, unit="kN")
    An = (bp - 2 * (HOLE[db] + 2)) * tp
    check(name, "extension shear rupture", Ffu / 2 / 1e3, 0.75 * 0.6 * FU_SM520 * An / 1e3, unit="kN")
    # bolt shear on the compression-side 4 bolts (DG4 Eq 3.17) and bearing / tear-out (Eq 3.18 - 3.19)
    Ab = math.pi * db * db / 4
    check(name, "bolt shear (4 compression-side bolts)", Vu / 1e3, 0.75 * 4 * BOLT[grade]["Fnv"] * Ab / 1e3, unit="kN")
    Lc_o = de - HOLE[db] / 2
    rn_o = min(1.2 * Lc_o * tp * FU_SM520, 2.4 * db * tp * FU_SM520)
    rn_i = 2.4 * db * tp * FU_SM520
    check(name, "bolt bearing / tear-out on the plate", Vu / 1e3, 0.75 * (2 * rn_o + 2 * rn_i) / 1e3, unit="kN")
    check(name, "bolt tension (no prying)", Mu / 1e6, out["phiMnp"] / 1e6, unit="kN.m")
    # thick-plate condition (DG4 3.3): Mpl >= 1.1 Mnp
    Mpl = Fyp * tp * tp * Yp
    check(name, "plate thick (1.11 phiMnp <= phib Mpl)", 1.11 * out["phiMnp"] / 1e6, 0.9 * Mpl / 1e6, unit="kN.m")
    # welds: flange max(Ffu, 0.6 Fy Af) double fillet over bf + (bf - tw) with the 1.5 transverse factor, or CJP
    Ff = max(Ffu, 0.6 * fy_sm520(tf) * bf * tf)
    w_f_req = Ff / ((bf + bf - tw) * 0.75 * 0.6 * FEXX * 1.5 * 0.707)
    leg = pick(LEGS, max(w_f_req, 5 if tf <= 13 else 6))
    flange_weld = f"{leg:g}" if leg <= min(tf - 2, 10) and w_f_req <= leg else "CJP"   # DG4 wind practice / CJP
    w_w_req = 0.943 * fy_sm520(tw) * tw / FEXX          # develop the web near the tension bolts (DG4 4.3)
    w_web = pick(LEGS, max(w_w_req, 5 if tp <= 13 else 6 if tp <= 19 else 8))
    L_shear = d / 2 - tf
    check(name, "web-to-plate weld in shear (two fillets)", Vu / 1e3,
          0.75 * 0.6 * FEXX * 0.707 * w_web * 2 * L_shear / 1e3, unit="kN")
    res = dict(name=name, d=d, bf=bf, tf=tf, tw=tw, bp=bp, g=g, tp=tp, tp_req=tp_req, Fyp=Fyp, Yp=Yp, s=s,
               db=db, grade=grade, pf=pf, de=de, h0=h0, h1=h1, n_bolts=8, Mu=Mu / 1e6, Vu=Vu / 1e3,
               N_case=worst[1], case=worst[0], Ffu=Ffu / 1e3, phiMnp=out["phiMnp"] / 1e6,
               flange_weld=flange_weld, w_flange_req=w_f_req, web_weld=w_web, hole=HOLE[db],
               pretension=PRETENSION[grade][db], length=2 * (de + pf) + d, note=note)
    # DG4 tested range (Table 3.7, monotonic), DG16 Table 4-7
    if not (254 <= d <= 1622 and 6.4 <= tf <= 25.4 and 102 <= bf <= 260 and 127 <= bp <= 270 and 64 <= g <= 178):
        res["range"] = "OUTSIDE DG4 TABLE 3.7"
    if d < 400:
        res["range_dg16"] = f"d = {d:.0f} mm below DG16 Table 4-7 (400 - 610): extrapolated, engineer to accept"
    if column:
        res["column"] = column_side(name, res, column)
    return res


def column_side(name, ep, col):
    """DG4 steps 14 - 19 on the column flange and web that receive the end plate; continuity plates; the flange is
    thickened locally when even the stiffened flange is too thin (proposal)"""
    bfc, tfc, twc, dc = col["bfc"], col["tfc"], col["twc"], col["dc"]
    Fyc = fy_sm520(tfc)
    g, pf, h0, h1 = ep["g"], ep["pf"], ep["h0"], ep["h1"]
    phiMnp = ep["phiMnp"] * 1e6
    ts = pick(PLATES, max(ep["tf"], 10))                             # continuity plate >= rafter flange (DG16 4.2)
    Yu = yc_4bolt(bfc, g, pf, pf, ep["tf"], h0, h1)
    Ys = yc_4bolt(bfc, g, pf, pf, ep["tf"], h0, h1, ts=ts)
    req_u = math.sqrt(1.11 * phiMnp / (0.9 * Fyc * Yu))
    req_s = math.sqrt(1.11 * phiMnp / (0.9 * Fyc * Ys))
    tf_used = tfc
    thick = None
    if req_s > tfc:                                                  # proposal: local flange plate at the knee
        tf_used = pick(PLATES, req_s)
        thick = tf_used
        if col.get("head"):                                          # user 2026-10-04: separate column head piece
            OPEN.append(f"{name}: {col['what']} {tfc:g} mm < {req_s:.1f} mm required with stiffeners (DG4 Eq 3.20, "
                        f"4E thick flange). PROPOSED: column head piece {col['head']} with BOTH flanges PL "
                        f"{tf_used:g} (shop piece), bolted to the column by the end-plate splice CS1 below the knee - "
                        f"changes the member, engineer to confirm")
        else:
            OPEN.append(f"{name}: {col['what']} {tfc:g} mm < {req_s:.1f} mm required with stiffeners (DG4 Eq 3.20, "
                        f"4E thick flange). PROPOSED: that flange made PL {tf_used:g} over the connection zone, CJP "
                        f"butt splices to the {tfc:g} mm flange - changes the member, engineer to confirm (or a DG16 "
                        f"thin-flange design)")
    Fyc = fy_sm520(tf_used)
    check(name, "column flange bending, stiffened (DG4 Eq 3.20)", req_s, tf_used, unit="mm")
    Ffu = ep["Ffu"] * 1e3
    kc = tf_used + 6.0                                               # built-up: flange + flange-to-web weld
    N_ = ep["tf"] + 2 * 8.0
    Ct = 0.5 if col.get("top") else 1.0
    Rwy = 1.0 * Ct * (6 * kc + N_ + 2 * ep["tp"]) * Fyc * twc
    h = dc - 2 * tf_used
    Rwb = 0.9 * (12 if col.get("top") else 24) * twc ** 3 * math.sqrt(E * Fyc) / h
    k_ = 0.40 if col.get("top") else 0.80
    Rwc = 0.75 * k_ * twc ** 2 * (1 + 3 * (N_ / dc) * (twc / tf_used) ** 1.5) * math.sqrt(E * Fyc * tf_used / twc)
    Mcf = 0.9 * Fyc * Yu * tf_used ** 2
    Rcf = Mcf / (ep["d"] - ep["tf"])
    Rmin = min(Rwy, Rwb, Rwc, Rcf)
    Fsu = max(0.0, Ffu - Rmin)
    # continuity plates (pair, one each side of the web): yield on the contact width less the clip
    clip = 20.0
    bst = (bfc - twc) / 2 - 5.0
    for ts in [p_ for p_ in PLATES if p_ >= ts]:                     # thicken until the pair carries Fsu
        Ast = 2 * (bst - clip) * ts
        if 0.9 * fy_sm520(ts) * Ast >= Fsu and (bst / ts) <= 0.56 * math.sqrt(E / fy_sm520(ts)):
            break
    check(name, "continuity plates (DG4 Eq 3.32) in compression / tension", Fsu / 1e3, 0.9 * fy_sm520(ts) * Ast / 1e3,
          unit="kN")
    w_cp = pick(LEGS, max(5.0, 0.6 * fy_sm520(ts) * ts / (0.75 * 0.6 * FEXX * 0.707 * 1.5 * 2)))
    return dict(Yc_unstiff=Yu, Yc_stiff=Ys, tfc_req_unstiff=req_u, tfc_req_stiff=req_s, tf_used=tf_used,
                thickened=thick, ts=ts, bst=bst, clip=clip, Fsu=Fsu / 1e3, R_web_yield=Rwy / 1e3,
                R_web_buckling=Rwb / 1e3, R_web_crippling=Rwc / 1e3, R_flange=Rcf / 1e3, Ct=Ct, w_cp=w_cp,
                twc=twc, bfc=bfc, dc=dc)


def panel_zone(name, Mu_kNm, Pu_kN, h, av, tw, negative):
    """DG16 Ch.5 (LRFD) mapped to 360-16 G2: Vu = Mu/h - Pu/2; tension field only for negative (gravity) moment with
    a full-depth column web stiffener"""
    Fy = fy_sm520(tw)
    Vu = Mu_kNm * 1e6 / h - Pu_kN * 1e3 / 2
    Aw = av * tw
    kv = 5 + 5 / (av / h) ** 2
    lam = h / tw
    a1, a2 = 1.10 * math.sqrt(kv * E / Fy), 1.37 * math.sqrt(kv * E / Fy)
    Cv = 1.0 if lam <= a1 else a1 / lam if lam <= a2 else 1.51 * kv * E / (lam ** 2 * Fy)
    if negative and lam > a1:
        Vn = 0.6 * Fy * Aw * (Cv + (1 - Cv) / (1.15 * math.sqrt(1 + (av / h) ** 2)))
    else:
        Vn = 0.6 * Fy * Aw * Cv
    phiVn = 0.9 * Vn
    check(name, f"panel zone shear ({'gravity, tension field' if negative else 'uplift, no tension field'})",
          Vu / 1e3, phiVn / 1e3, unit="kN")
    return dict(Vu=Vu / 1e3, phiVn=phiVn / 1e3, Cv=Cv, kv=kv, h_tw=lam)


def envelope_cases(pairs):
    """element ends that are not joint nodes: the design envelope as pseudo-cases (max and min moment, each with
    the largest |V| and the largest tension of the envelope: conservative, not concurrent)"""
    out = []
    for el, nd in pairs:
        e = ELEM[el]
        part = "I" if e["NODE"][0] == nd else "J"
        env = FORCES["envelope"][f"{el}/{part}"]
        V = max(abs(env["Vz"][0]), abs(env["Vz"][2]))
        Nt = max(env["N"][0], 0.0)
        out += [(env["My"][1] + " (env)", Nt, V, env["My"][0], el), (env["My"][3] + " (env)", Nt, V, env["My"][2], el)]
    return out


def coll(xs, zf, sects, frames, tol=30.0):
    """element ends of the given sections at the nodes (x, y, zf(x)) of the listed frames"""
    pairs = []
    for y in frames:
        for x in xs:
            n = node_at(x, y, zf(x), tol)
            pairs += [(e, n) for e in ends_at(n, sects)]
    return pairs


def forces_of(pairs):
    cs = joint_cases(pairs)
    return cs if cs else envelope_cases(pairs)


def summary(cases):
    mx = max(cases, key=lambda c: c[3])
    mn = min(cases, key=lambda c: c[3])
    return dict(M_pos=mx[3], case_pos=mx[0], M_neg=mn[3], case_neg=mn[0], V=max(abs(c[2]) for c in cases),
                N_t=max(c[1] for c in cases), N_c=min(c[1] for c in cases))


INT = FRAMES_Y[1:-1]                 # interior frames, grids 2 - 9
END = (FRAMES_Y[0], FRAMES_Y[-1])    # gable frames, grids 1 and 10


def E6(x):
    return EAVE_Z


# =========================================================================== knee geometry as drawn (left frame half)
def roof_top(x):
    """top of the rafter / canopy top flange at x (left half; x < 0 on the canopy): the prismatic rafter centre
    line is the model work line, the top flange d/2 above it, the haunch deepens downward"""
    return EAVE_Z + SLOPE * x + RAF.d / 2 / math.cos(THETA)


def rafter_bot(x):
    return roof_top(x) - (taper_d("H", x) if x < X_SPLICE else RAF.d) / math.cos(THETA)


def col_face(z, side=1):
    """column flange outer face x at height z: side +1 inner, -1 outer (column tapered about its centre line)"""
    return side * col_depth(z) / 2


COL_ALPHA = math.atan((TAPER["C"]["d1"] - TAPER["C"]["d0"]) / 2 / TAPER["C"]["L"])   # flange slope from vertical


def knee_geometry(kj):
    """the rafter flanges meeting the outer face of the knee end plate, which lies on the tapered column inner
    flange (iterated); x = the column face at that level. The knee bolt rows (z, outer row first), the plate ends,
    the column top (cap, along the roof slope)"""
    t_x = kj["tp"] / math.cos(COL_ALPHA)                            # plate thickness measured horizontally

    def meet(fn):
        x = col_face(EAVE_Z)
        for _ in range(30):
            x = col_face(fn(x + t_x))
        return x, fn(x + t_x)
    xt, zt = meet(roof_top)
    xb, zb = meet(rafter_bot)
    sb = (rafter_bot(X_SPLICE - 1) - zb) / (X_SPLICE - 1 - xb)     # haunch bottom-flange slope
    cos, cos_b = math.cos(THETA), math.cos(math.atan(sb))
    pf, tf, de = kj["pf"], kj["tf"], kj["de"]
    rows = [zt + pf / cos, zt - (tf + pf) / cos, zb + (tf + pf) / cos_b, zb - pf / cos_b]
    top = zt + (pf + de) / cos
    return dict(xt=xt, zt=zt, xb=xb, zb=zb, sb=sb, cos_b=cos_b, rows=rows, plate_top=rows[0] + de,
                plate_bot=rows[-1] - de, plate_len=(rows[0] - rows[-1] + 2 * de) / math.cos(COL_ALPHA),
                ext=pf + de, col_top_in=top,
                col_top_out=top + (col_face(top, -1) - xt) * SLOPE)


def col_pairs_at(z, frames):
    """(element, upper node) of the column element that holds level z, both columns of each frame: the forces at
    the upper end bound those at z (the column moment grows from the pinned base towards the knee)"""
    pairs = []
    for y in frames:
        for x in (0.0, SPAN):
            for e in find_elem(1101, lambda a, b: at(a, x=x, y=y, tol=5) and at(b, x=x, y=y, tol=5)):
                lo, hi = sorted(ELEM[e]["NODE"][:2], key=lambda n: N[n][2])
                if N[lo][2] - 1 <= z <= N[hi][2] + 1:
                    pairs.append((e, hi))
                    break
    return pairs


CLR_SPLICE = 200.0                  # top of the column splice plates -> the steel above (bolt and wrench room)


def design_joints(D):
    cos = math.cos(THETA)
    # ---------------------------------------------------------------- knee KJ1 (interior frames, both eaves)
    raf = forces_of(coll((0, SPAN), E6, (2101,), INT))
    col = forces_of(coll((0, SPAN), E6, (1101,), INT))
    xf = TAPER["C"]["d1"] / 2                                      # column inner face from its centre line
    d_face = taper_d("H", xf)                                      # haunch depth at the column face (perpendicular)
    KJ = endplate("KJ1 knee", d_face, TAPER["H"]["bf"], TAPER["H"]["tf"], TAPER["H"]["tw"], raf, bp=270,
                  column=dict(bfc=TAPER["C"]["bf"], tfc=TAPER["C"]["tf"], twc=TAPER["C"]["tw"],
                              dc=TAPER["C"]["d1"], top=True, what="column inner flange", head="CH1"),
                  note="vertical end plate on the column inner flange; lever arms perpendicular to the rafter")
    KJ["forces"] = summary(raf)
    KJ["column_forces"] = summary(col)
    KJ["d_plumb"] = d_face / cos
    h_pz = d_face / cos                                            # panel depth along the column at the rafter side
    av = TAPER["C"]["d1"] - 2 * KJ["column"]["tf_used"]
    KJ["panel_neg"] = panel_zone("KJ1 knee", abs(KJ["forces"]["M_neg"]), 0.0, h_pz, av, TAPER["C"]["tw"], True)
    KJ["panel_pos"] = panel_zone("KJ1 knee", abs(KJ["forces"]["M_pos"]), 0.0, h_pz, av, TAPER["C"]["tw"], False)
    D["KJ1"] = KJ
    KG = knee_geometry(KJ)
    KJ["geom"] = KG
    # ---------------------------------------------------------------- column head CH1 and column splice CS1
    # user 2026-10-04: instead of thickening one column flange with CJP splices, the column top is a separate shop
    # piece CH1 with BOTH flanges thickened, bolted to the column C1 by an end-plate splice CS1 below the knee
    tfh = KJ["column"]["tf_used"]
    # lowest steel above the splice: the knee plate bottom (outside the inner flange) or the bottom continuity
    # plate, which follows the haunch bottom flange down to the outer flange (inside the column)
    x_cp = col_face(KG["zb"], -1) + tfh
    KG["cp_low"] = KG["zb"] + (x_cp - KG["xb"]) * KG["sb"]
    z_room = min(KG["plate_bot"], KG["cp_low"])
    zs = 50 * math.floor((z_room - CLR_SPLICE - 25.0) / 50)                 # splice interface level (Z = 0 base)
    for _ in range(10):
        cs = forces_of(col_pairs_at(zs, INT))
        CS = endplate("CS1 column splice", col_depth(zs), TAPER["C"]["bf"], tfh, TAPER["C"]["tw"], cs, bp=270,
                      g=140, db_min=KJ["db"],               # the knee bolt size: one bolt size at the column head
                      note="plates square to the column axis (horizontal); 4E, extended at both flanges")
        if z_room - (zs + CS["tp"]) >= CLR_SPLICE:
            break
        zs -= 50
    CS["forces"] = summary(cs)
    CS["z"] = zs
    check("CS1 column splice", "splice plate top -> knee plate / continuity plate (bolting room)", CLR_SPLICE,
          z_room - zs - CS["tp"], unit="mm")
    s_yl = 0.5 * math.sqrt(TAPER["C"]["bf"] * KJ["g"])
    check("CH1 column head", "thick flange past the bottom knee bolt >= s (DG4 yield line)", s_yl,
          KG["rows"][-1] - zs - CS["tp"], unit="mm")
    D["CS1"] = CS
    D["CH1"] = dict(tf=tfh, tw=TAPER["C"]["tw"], bf=TAPER["C"]["bf"], z0=zs + CS["tp"], zs=zs,
                    d0=col_depth(zs), top_in=KG["col_top_in"], top_out=KG["col_top_out"],
                    d1=col_depth(KG["col_top_in"]))
    # ---------------------------------------------------------------- haunch / rafter splice SP1 (x = 5.2 m)
    sp = forces_of(coll((X_SPLICE, SPAN - X_SPLICE), roof_z, (2102,), INT))
    SP = endplate("SP1 rafter splice", RAF.d, RAF.bf, TAPER["H"]["tf"], RAF.tw, sp, bp=RAF.bf + 20, g=110,
                  note="plates perpendicular to the rafter; haunch plate on the 250 mm flange, rafter plate on the 200")
    SP["forces"] = summary(sp)
    D["SP1"] = SP
    # ---------------------------------------------------------------- ridge RJ1 (plumb plates)
    rj = forces_of(coll((RIDGE_X,), roof_z, (2102,), INT))
    RJ = endplate("RJ1 ridge", RAF.d, RAF.bf, RAF.tf, RAF.tw, rj, bp=RAF.bf + 20, g=110,
                  note="plumb plates; lever arms perpendicular to the rafter (conservative)")
    RJ["forces"] = summary(rj)
    RJ["angle"] = math.degrees(THETA)
    D["RJ1"] = RJ
    # ---------------------------------------------------------------- canopy roots CJ1 (both sides, one design)
    cj = forces_of(coll((0, SPAN), E6, (203,), INT))
    CJ = endplate("CJ1 canopy root", CAN.d, CAN.bf, CAN.tf, CAN.tw, cj, bp=CAN.bf + 20, g=110,
                  column=dict(bfc=TAPER["C"]["bf"], tfc=D["CH1"]["tf"], twc=TAPER["C"]["tw"],
                              dc=TAPER["C"]["d1"], top=True, what="column head CH1 outer flange"),
                  note="canopy end plate on the column outer flange, opposite the knee plate")
    CJ["forces"] = summary(cj)
    D["CJ1"] = CJ
    # ---------------------------------------------------------------- gable corner GK1 (rafter over column)
    gc = forces_of(coll((0, SPAN), E6, (1101,), END))
    GK = endplate("GK1 gable corner (column cap)", TAPER["C"]["d1"], TAPER["C"]["bf"], TAPER["C"]["tf"],
                  TAPER["C"]["tw"], gc, bp=270,
                  column=dict(bfc=GRAF.bf, tfc=GRAF.tf, twc=GRAF.tw, dc=GRAF.d, top=False,
                              what="gable rafter bottom flange"),
                  note="horizontal cap plate on the column, bolted to the underside of the continuous gable rafter")
    GK["forces"] = summary(gc)
    D["GK1"] = GK
    # ---------------------------------------------------------------- gable rafter splices GS1 (x 6.5 / 19.5), GS2 ridge
    for key, xs in (("GS1", (6_500.0, SPAN - 6_500.0)), ("GS2", (RIDGE_X,))):
        cs = forces_of(coll(xs, roof_z, (204,), END))
        r = endplate(f"{key} gable rafter splice", GRAF.d, GRAF.bf, GRAF.tf, GRAF.tw, cs, bp=GRAF.bf + 20, g=110,
                     note="plumb plates on the ridge post" if key == "GS2" else "plates perpendicular to the rafter")
        r["forces"] = summary(cs)
        D[key] = r
    # ---------------------------------------------------------------- eave beam EB1 (bays 1 - 2 and 9 - 10)
    eb = forces_of(coll((0, SPAN), E6, (302,), FRAMES_Y))
    EB = endplate("EB1 eave beam", EAVEB.d, EAVEB.bf, EAVEB.tf, EAVEB.tw, eb, bp=EAVEB.bf + 20, g=110,
                  note="end plate on a stiffened stub across the column web (weak axis)")
    EB["forces"] = summary(eb)
    D["EB1"] = EB
    D["post_top"] = summary(forces_of(coll(GABLE_POSTS, roof_z, (102,), END)))
    mon = summary(forces_of(coll(MON_X, roof_z, (401,), FRAMES_Y)))
    # monitor post base MB1: H 100 x 100 on a plate bolted to the rafter top flange, 4 bolts at the corners
    db, s_ = 16, 120.0                                             # bolt pitch both ways (rafter flange 200 wide)
    Mm = max(abs(mon["M_pos"]), abs(mon["M_neg"]))
    T_b = Mm * 1e3 / s_ / 2 + max(0.0, mon["N_t"]) / 4            # kN per bolt: moment couple + uplift share
    phiT = 0.75 * BOLT[BOLT_GRADE_SHEAR]["Fnt"] * math.pi * db * db / 4 / 1e3
    check("MB1 monitor post base", f"4-M{db} {BOLT_GRADE_SHEAR} tension", T_b, phiT, unit="kN")
    a = s_ / 2 - MON.bf / 2 + 10                                    # bolt to the post flange line
    t_req = math.sqrt(4 * T_b * 1e3 * a / (0.9 * SM400["Fy"] * 2 * a + 1e-9))
    tp = pick((10, 12, 16, 20), max(t_req, 12))
    check("MB1 monitor post base", "base plate bending (bolt cantilever)", t_req, tp, unit="mm")
    D["MB1"] = dict(db=db, s=s_, tp=tp, B=s_ + 2 * 35, n=4, T=T_b, forces=mon, weld=5)


# =========================================================================== bases (pinned)
def reactions(xs, frames):
    """support reactions over the design cases at the nodes (x, y, 0): list of (case, Fx, Fy, Fz) in kN.
    Fz > 0 = compression into the base; Fz < 0 = uplift"""
    out = []
    for y in frames:
        for x in xs:
            n = str(node_at(x, y, 0.0))
            for c in DESIGN_CASES:
                r = FORCES["reactions"][c].get(n)
                if r:
                    out.append((c, r[0], r[1], r[2]))
    return out


def base_plate(name, col_d, col_bf, col_tf, col_tw, reac, *, B=None, W=None, rods=4, db=24, sx=150.0, sy=200.0):
    """Pinned base: plate B (along the column depth) x W, 4 rods at sx x sy centred on the column (between the
    flanges, either side of the web). Bearing (AISC DG1 / 360-16 J8, A2/A1 = 1), plate bending in bearing (DG1
    m, n, lambda n') and under uplift (rod cantilever to the nearest weld line, 45 deg spread), rods in tension +
    shear (J3.7, threads included, plate washers site-welded so all rods share the shear)"""
    B = B or ceil5(col_d + 100)
    W = W or ceil5(col_bf + 100)
    Pu = max(r[3] for r in reac) * 1e3
    Tu = max(0.0, -min(r[3] for r in reac)) * 1e3
    Vu = max(math.hypot(r[1], r[2]) for r in reac) * 1e3
    case_T = min(reac, key=lambda r: r[3])[0]
    case_V = max(reac, key=lambda r: math.hypot(r[1], r[2]))[0]
    # bearing
    A1 = B * W
    phiPp = 0.65 * 0.85 * FC_PED * A1
    check(name, "concrete bearing (J8, A2/A1 = 1)", Pu / 1e3, phiPp / 1e3, unit="kN")
    m = (B - 0.95 * col_d) / 2
    n = (W - 0.8 * col_bf) / 2
    X = (4 * col_d * col_bf / (col_d + col_bf) ** 2) * Pu / phiPp
    lam = min(1.0, 2 * math.sqrt(X) / (1 + math.sqrt(1 - X))) if X < 1 else 1.0
    lnp = lam * math.sqrt(col_d * col_bf) / 4
    l_ = max(m, n, lnp)
    Fyp = 245.0                                               # base plate SM400B (S1.3), t <= 40: 235 - 245
    t_bear = l_ * math.sqrt(2 * Pu / (0.9 * Fyp * B * W))
    # uplift: each rod a cantilever to the nearest weld line (web or flange), effective width 2a
    a_web = sy / 2 - col_tw / 2 - 6.0
    a_fl = (col_d - 2 * col_tf) / 2 - sx / 2 - 6.0
    a = max(25.0, min(a_web, a_fl))
    Tr = Tu / rods
    t_upl = math.sqrt(4 * Tr * a / (0.9 * Fyp * 2 * a)) if Tu else 0.0
    tp = pick((16, 20, 25, 28, 32, 36, 40), max(t_bear, t_upl, 20.0))
    check(name, "base plate bending (bearing / uplift)", max(t_bear, t_upl), tp, unit="mm")
    # rods: tension + shear interaction (J3.7), threads included
    Ab = math.pi * db * db / 4
    Fnt, Fnv = 0.75 * ROD_GRADE["Fu"], 0.45 * ROD_GRADE["Fu"]
    frv = Vu / (rods * Ab)
    check(name, "anchor rods in shear (plate washers welded)", Vu / 1e3, 0.75 * rods * Fnv * Ab / 1e3, unit="kN")
    Fnt_ = min(Fnt, 1.3 * Fnt - Fnt / (0.75 * Fnv) * frv)
    check(name, "anchor rods in tension with shear (J3-3a)", Tu / 1e3, 0.75 * rods * Fnt_ * Ab / 1e3, unit="kN")
    # column to base plate: fillet all round, uplift on the flanges + shear on the web
    L_fl = 2 * (2 * col_bf - col_tw)
    w_req = max(Tu / (L_fl * 0.75 * 0.6 * FEXX * 0.707 * 1.5), Vu / (2 * (col_d - 2 * col_tf) * 0.75 * 0.6 * FEXX * 0.707))
    w = pick(LEGS, max(w_req, 6.0))
    hole = {20: 33, 24: 40, 27: 46, 30: 52}[db]               # AISC Manual Table 14-2 oversized base-plate holes
    washer = dict(b=hole + 2 * 25, t=pick((8, 10, 12), db / 3 + 1), hole=db + 2)
    return dict(name=name, B=B, W=W, tp=tp, t_bear=t_bear, t_upl=t_upl, rods=rods, db=db, sx=sx, sy=sy, Pu=Pu / 1e3,
                Tu=Tu / 1e3, Vu=Vu / 1e3, case_T=case_T, case_V=case_V, weld=w, hole=hole, washer=washer,
                Fyp=Fyp, grout=30.0, embed=ceil5(max(12 * db, 300)), col_d=col_d, col_bf=col_bf)


def design_bases(D):
    c0 = TAPER["C"]
    D["BP1"] = base_plate("BP1 frame column base", c0["d0"], c0["bf"], c0["tf"], c0["tw"],
                          reactions((0.0, SPAN), FRAMES_Y), sx=150.0, sy=160.0)
    D["BP2"] = base_plate("BP2 gable post base", GPOST.d, GPOST.bf, GPOST.tf, GPOST.tw,
                          reactions(GABLE_POSTS, END), db=20, W=280.0, sx=150.0, sy=180.0)


# =========================================================================== bracing and struts
def member_axial(sects, frames=None):
    """max tension, max compression (kN) of the listed sections over the design envelope"""
    t, c = 0.0, 0.0
    for key, env in FORCES["envelope"].items():
        el = int(key.split("/")[0])
        if ELEM[el]["SECT"] in sects:
            t = max(t, env["N"][0])
            c = min(c, env["N"][2])
    return t, c


def knife_end(name, pipe, Pt, Pc, *, mat=STK, n_bolts=None, db=20):
    """CHS slotted on a shop-welded knife plate (tab), field-bolted to a gusset (DG29 4.1 - 4.3 / 4.5; DG24 5.3).
    Bolts 8.8 bearing type, single shear."""
    Pu = max(Pt, -Pc) * 1e3
    Ab = math.pi * db * db / 4
    phi_b = 0.75 * BOLT[BOLT_GRADE_SHEAR]["Fnv"] * Ab
    n = n_bolts or max(2, math.ceil(Pu / phi_b))
    for tk in (12.0, 16.0, 20.0):                                   # knife plate: thicken for the lap in compression
        KLr_ = 1.2 * 60.0 / (tk / math.sqrt(12))
        Fe_ = math.pi ** 2 * E / KLr_ ** 2
        Fcr_ = (0.658 ** (SM400["Fy"] / Fe_)) * SM400["Fy"]
        if 0.9 * Fcr_ * ceil5(max(2 * EDGE_MIN[db], 3 * db, 90)) * tk >= -Pc * 1e3:
            break
    hole = HOLE[db]
    e1, p = ceil5(max(EDGE_MIN[db] + 5, 1.5 * db)), ceil5(3 * db)
    rn_end = min(1.2 * (e1 - hole / 2) * tk * SM400["Fu"], 2.4 * db * tk * SM400["Fu"])
    rn_int = min(1.2 * (p - hole) * tk * SM400["Fu"], 2.4 * db * tk * SM400["Fu"])
    check(name, f"{n}-M{db} {BOLT_GRADE_SHEAR} single shear", Pu / 1e3, n * phi_b / 1e3, unit="kN")
    check(name, "bearing / tear-out on the knife plate", Pu / 1e3, 0.75 * (rn_end + (n - 1) * rn_int) / 1e3, unit="kN")
    # knife plate: tension yield / rupture, compression as an eccentric lap (K 1.2 over the free length)
    bk = ceil5(max(2 * EDGE_MIN[db] + 0, 3 * db, 90))
    check(name, "knife plate tension yield", Pt, 0.9 * SM400["Fy"] * bk * tk / 1e3, unit="kN")
    check(name, "knife plate net-section rupture", Pt, 0.75 * SM400["Fu"] * (bk - hole - 2) * tk / 1e3, unit="kN")
    Lfree = 60.0
    KLr = 1.2 * Lfree / (tk / math.sqrt(12))
    Fe = math.pi ** 2 * E / KLr ** 2
    Fcr = (0.658 ** (SM400["Fy"] / Fe)) * SM400["Fy"] if KLr <= 4.71 * math.sqrt(E / SM400["Fy"]) else 0.877 * Fe
    check(name, "knife plate in compression (lap, K 1.2)", -Pc, 0.9 * Fcr * bk * tk / 1e3, unit="kN")
    # tube: lap length (wall shear, 4 lines), U, net section; slot welds w <= t (J2.2b)
    t = pipe.t
    l_wall = max(Pu / (0.75 * 0.6 * mat["Fu"] * 4 * t), Pu / (1.0 * 0.6 * mat["Fy"] * 4 * t))
    lap = ceil5(max(l_wall, pipe.D))                                      # l >= D for U (360-16 Table D3.1 case 5)
    U = 1.0 if lap >= 1.3 * pipe.D else 1 - (pipe.D / math.pi) / lap
    An = pipe.A - 2 * t * (tk + 4.0)
    check(name, "tube net section at the slot", Pt, 0.75 * mat["Fu"] * An * U / 1e3, unit="kN")
    w = min(math.floor(t), 4.0)
    check(name, f"slot welds 4 x {w:g} mm x {lap:g} mm", Pu / 1e3, 4 * 0.75 * 0.6 * FEXX * 0.707 * w * lap / 1e3,
          unit="kN")
    Pn_wall = 0.75 * 0.6 * mat["Fu"] * 4 * t * lap
    check(name, "tube wall shear along the welds", Pu / 1e3, Pn_wall / 1e3, unit="kN")
    return dict(name=name, pipe=pipe.name, Pt=Pt, Pc=Pc, n=n, db=db, hole=hole, e1=e1, p=p, tk=tk, bk=bk, lap=lap,
                slot=tk + 4.0, weld=w, U=U, gap=10.0)


def strut_check(name, pipe, Pt, Pc, L, mat=STK):
    """CHS strut in compression (E3, K = 1.0 over the bay, no intermediate restraint)"""
    KLr = L / pipe.r
    Fe = math.pi ** 2 * E / KLr ** 2
    Fcr = (0.658 ** (mat["Fy"] / Fe)) * mat["Fy"] if KLr <= 4.71 * math.sqrt(E / mat["Fy"]) else 0.877 * Fe
    phiPn = 0.9 * Fcr * pipe.A / 1e3
    r = check(name, f"member compression, KL/r {KLr:.0f} (E3, {mat['name'].split()[0]})", -Pc, phiPn,
              note="MODEL MEMBER", unit="kN")
    if r > 1.0:
        OPEN.append(f"{name}: compression {-Pc:.0f} kN > phiPn {phiPn:.0f} kN ({pipe.name}, L {L / 1e3:.1f} m, "
                    f"KL/r {KLr:.0f}) - member is the engineer's design in MIDAS: check the model's code check and "
                    f"the pipe grade; the connection is detailed for the model force")
    return dict(KLr=KLr, phiPn=phiPn)


def angle_end(name, ang, Pt, *, db=20, tg=12.0, mat=SS400):
    """single angle, one leg bolted to the gusset (tension only), bolts 8.8 bearing type in single shear;
    360-16 D2 (yield, rupture with U from Table D3.1 case 2 / case 8), J3.6 bolts, J3.10 bearing / tear-out
    on the angle and the gusset, J4.3 block shear on the angle"""
    Pu = Pt * 1e3
    Ab = math.pi * db * db / 4
    phi_b = 0.75 * BOLT[BOLT_GRADE_SHEAR]["Fnv"] * Ab
    hole = HOLE[db]
    e1, p = ceil5(max(EDGE_MIN[db] + 5, 1.5 * db)), ceil5(3 * db)
    g = GAUGE[int(ang.b)]
    t = ang.t
    for n in range(2, 7):
        l = (n - 1) * p
        U = max(1 - ang.c / l, 0.80 if n >= 4 else (0.60 if n == 3 else 0.0))
        An = ang.A - (hole + 2) * t
        rn_end = min(1.2 * (e1 - hole / 2) * t * mat["Fu"], 2.4 * db * t * mat["Fu"])
        rn_int = min(1.2 * (p - hole) * t * mat["Fu"], 2.4 * db * t * mat["Fu"])
        Agv = (e1 + l) * t
        Anv = Agv - (n - 0.5) * (hole + 2) * t
        Ant = (ang.b - g - (hole + 2) / 2) * t
        bs = min(0.6 * mat["Fu"] * Anv, 0.6 * mat["Fy"] * Agv) + mat["Fu"] * Ant
        caps = [n * phi_b, 0.75 * (rn_end + (n - 1) * rn_int), 0.75 * mat["Fu"] * An * U, 0.75 * bs]
        if min(caps) >= Pu:
            break
    check(name, f"{n}-M{db} {BOLT_GRADE_SHEAR} single shear", Pt, n * phi_b / 1e3, unit="kN")
    check(name, f"bearing / tear-out on the angle (t {t:g})", Pt, caps[1] / 1e3, unit="kN")
    check(name, f"angle tension yield ({ang.name})", Pt, 0.9 * mat["Fy"] * ang.A / 1e3, unit="kN")
    check(name, f"angle net-section rupture (U {U:.2f})", Pt, caps[2] / 1e3, unit="kN")
    check(name, "block shear on the angle", Pt, caps[3] / 1e3, unit="kN")
    # gusset: bearing / tear-out (edge 40 beyond the last bolt) and Whitmore section, 30 deg from the first bolt
    rg_end = min(1.2 * (40.0 - hole / 2) * tg * SM400["Fu"], 2.4 * db * tg * SM400["Fu"])
    rg_int = min(1.2 * (p - hole) * tg * SM400["Fu"], 2.4 * db * tg * SM400["Fu"])
    check(name, f"bearing / tear-out on the gusset (PL {tg:g})", Pt, 0.75 * (rg_end + (n - 1) * rg_int) / 1e3,
          unit="kN")
    Lw = 2 * (n - 1) * p * math.tan(math.radians(30))
    check(name, "gusset Whitmore section, tension yield", Pt, 0.9 * SM400["Fy"] * Lw * tg / 1e3, unit="kN")
    return dict(name=name, sec=ang.name, ang=ang, Pt=Pt, Pc=0.0, n=n, db=db, hole=hole, e1=e1, p=p, g=g, U=U,
                tk=ang.t, grip=ang.t + tg)


def brace_node_geometry(D, BRr, STr, tg):
    """plan of the braced-bay node in the roof plane (work point at the rafter centre line, x along the rafter,
    y along the bay): angle ends clear of the top flange, bolts on the gauge line, the ST1 knife plate beyond the
    angles; the gusset = hull of the bolt groups (40 mm edges, the angle legs over the lap) and the knife plate,
    cut at the web face, vertices to 5 mm"""
    from shapely.geometry import LineString, Polygon, MultiPoint, box
    bf = TAPER["H"]["bf"]
    ang = math.atan2(BAY, 4_500.0)
    ax = BRr["ang"]
    heel, toe = BRr["g"], ax.b - BRr["g"]            # from the bolt line: heel on the near side, toe outside
    side = {}
    brs = []
    for sgn in (1, -1):                              # +x brace on top of the gusset, -x brace below it
        u = (sgn * math.cos(ang), math.sin(ang))
        nrm = (-math.sin(ang), math.cos(ang)) if sgn > 0 else (math.sin(ang), math.cos(ang))   # toward the strut
        # angle end: every corner of the leg footprint beyond the flange edge + 20
        s_end = 0.0
        while True:
            corners = [(u[0] * s_end + nrm[0] * w, u[1] * s_end + nrm[1] * w) for w in (-heel, toe)]
            if min(c[1] for c in corners) >= bf / 2 + 20:
                break
            s_end += 5.0
        bolts = [s_end + BRr["e1"] + k * BRr["p"] for k in range(BRr["n"])]
        s_lap = bolts[-1] + 40.0                     # the gusset edge: 40 beyond the last bolt
        foot = Polygon([(u[0] * s + nrm[0] * w, u[1] * s + nrm[1] * w)
                        for s, w in ((s_end, -heel), (s_lap, -heel), (s_lap, toe), (s_end, toe))])
        brs.append(dict(sgn=sgn, u=u, n=nrm, s_end=s_end, bolts=bolts, s_lap=s_lap, foot=foot,
                        face="TOP" if sgn > 0 else "BOTTOM"))
    # ST1 knife plate along +y, its bolts beyond the angle footprints (60 clear)
    kb = STr["bk"] / 2
    y0 = max(b["foot"].bounds[3] for b in brs)
    y_k = 0.0
    while any(b["foot"].buffer(30).intersects(box(-kb - 10, y_k - STr["e1"], kb + 10, y_k + 400)) for b in brs):
        y_k += 5.0
    st_bolts = [y_k + k * STr["p"] for k in range(STr["n"])]
    knife = box(-kb, y_k - STr["e1"], kb, st_bolts[-1] + STr["e1"])
    gy0 = TAPER["H"]["tw"] / 2
    pts = []
    for b in brs:
        pts += list(b["foot"].buffer(10, join_style=2).exterior.coords)
    pts += list(knife.buffer(15, join_style=2).exterior.coords)
    xs = [q[0] for q in pts]
    pts += [(min(xs), gy0), (max(xs), gy0)]
    hull = MultiPoint(pts).convex_hull.intersection(box(-5_000, gy0, 5_000, 5_000))
    poly = [(round(x / 5) * 5, gy0 if y < gy0 + 2.5 else round(y / 5) * 5)
            for x, y in list(hull.simplify(4.0).exterior.coords)[:-1]]
    base = [x for x, y in poly if y == gy0]
    return dict(braces=brs, st_bolts=st_bolts, y_k=y_k, knife=knife, poly=poly, gy0=gy0,
                web_len=max(base) - min(base))


def design_bracing(D):
    t2, c2 = member_axial((902,))
    t1, c1 = member_axial((901,))
    t3, c3 = member_axial((903,))
    # BR1: tension-only angles. The model's braces are CHS acting in tension and compression; with the compression
    # brace neglected the tension brace of the X takes the panel shear of both: bounded here by T + |C| of the
    # envelope (same geometry both ways) until the model is re-run with tension-only braces.
    Tbr = t2 - c2
    D["BR1"] = angle_end("BR1 roof brace end", BRACE_L, Tbr)
    Lbr = math.hypot(BAY, 4_500.0) / math.cos(THETA * 0.5)
    D["BR1"]["member"] = dict(L=Lbr, LrX=Lbr / 2 / BRACE_L.rz, Lr=Lbr / BRACE_L.rz)
    check("BR1 roof brace (L 90x90x6)", "slenderness L/r, half length (crossing) / rz <= 300 (D1 user note)",
          Lbr / 2 / BRACE_L.rz, 300.0, note="MODEL MEMBER")             # the engineer's member (markup)
    OPEN.append(f"BR1 changed to {BRACE_L.name} tension-only (engineer's markup, 10/10/2026): designed for "
                f"T {Tbr:.0f} kN = T {t2:.0f} + |C| {-c2:.0f} kN of the CHS model; re-run the model with tension-only "
                f"angle braces and recheck; L/r {Lbr / 2 / BRACE_L.rz:.0f} over half the length (D1 recommends 300); "
                f"install the braces taut")
    D["ST1"] = knife_end("ST1 braced-bay strut end", BRACE, t1, c1)
    D["ST1"]["member"] = strut_check("ST1 strut (CHS 165.2)", BRACE, t1, c1, BAY)
    D["ST2"] = knife_end("ST2 eave / ridge strut end", STRUT, t3, c3)
    D["ST2"]["member"] = strut_check("ST2 eave / ridge strut (CHS 190.7)", STRUT, t3, c3, BAY)
    # gusset on the rafter web, in the roof plane, with a full-depth web stiffener taking the force normal to the web
    Pmax = max(Tbr, t1, -c1, t3, -c3)
    tg = 12.0
    geo = brace_node_geometry(D, D["BR1"], D["ST1"], tg)
    Lw = geo["web_len"]
    w_g = pick(LEGS, max(5.0, Pmax * 1e3 / (2 * Lw * 0.75 * 0.6 * FEXX * 0.707)))
    check("GU1 brace gusset", "gusset-to-web welds (two fillets)", Pmax, 2 * Lw * 0.75 * 0.6 * FEXX * 0.707 * w_g / 1e3,
          unit="kN")
    D["GU1"] = dict(tg=tg, L=Lw, weld=w_g, P=Pmax, stiffener=dict(t=10.0, weld=5.0), geo=geo)


# =========================================================================== secondary framing (PROPOSED, TBC)
LOADS = {}


def roof_loads():
    """kPa from the model's beam loads on a typical interior frame (10 m tributary): SDL, LL and the governing
    MWFRS roof suction (W_Roof_Gov), wall pressure (W_X_wall) and gable pressure (W_Y_wall on the posts)"""
    bm = MODEL["BMLD_FRAME10"]

    def q(elem_sect, case, direction=None):
        vals = []
        for k, v in bm.items():
            if ELEM[int(k)]["SECT"] != elem_sect:
                continue
            for it in v["ITEMS"]:
                if it["LCNAME"] == case and (direction is None or it["DIRECTION"] == direction):
                    vals.append(abs(it["P"][0]))
        return max(vals) if vals else 0.0
    LOADS.update(SDL=q(2102, "SDL") / BAY * 1e3, LL=q(2102, "LL") / BAY * 1e3,
                 W_up=q(2102, "W_Roof_Gov") / BAY * 1e3, W_can=q(203, "W_Roof_Gov") / BAY * 1e3,
                 W_wall=q(1101, "W_X_wall") / BAY * 1e3)
    trib_post = 4_250.0                                                 # gable posts at about 4.0 - 4.5 m
    LOADS["W_gable"] = q(102, "W_Y_wall") / trib_post * 1e3
    return LOADS                                                         # kN/m2 = kPa


def beam_member(name, sec, L, wD, wL, wW_up, s_trib, slope=0.0, sag=3, defl_lim=240.0):
    """simple span L with sag rods at third points: strong axis under gravity (1.2D + 1.6L) and uplift
    (0.9D + 1.0W; bottom flange compressed, Lb = L/3), weak axis from the slope component between sag rods
    (continuous over the rods: wL^2/10 on L/3), H1-1; deflection under L <= L/defl_lim"""
    Fy = sec.Fy
    sw = sec.kg_m * 9.81e-3                                            # kN/m
    wd = wD * s_trib + sw
    wl = wL * s_trib
    ww = wW_up * s_trib
    c, s_ = math.cos(slope), math.sin(slope)
    res = {}
    for combo, wn, wt, Lb in (("1.2D+1.6L", (1.2 * wd + 1.6 * wl) * c, (1.2 * wd + 1.6 * wl) * s_, L / sag),
                              ("0.9D+1.0W", ww - 0.9 * wd * c, 0.9 * wd * s_, L / sag)):
        Mx = abs(wn) * (L / 1e3) ** 2 / 8                                # kN.m
        My = abs(wt) * (L / sag / 1e3) ** 2 / 10
        Mp = Fy * sec.Zx / 1e6
        rts = math.sqrt(math.sqrt(sec.Iy * sec.Cw) / sec.Sx)
        Lp = 1.76 * sec.ry * math.sqrt(E / Fy)
        Lr = 1.95 * rts * E / (0.7 * Fy) * math.sqrt(sec.J / (sec.Sx * sec.ho) + math.sqrt(
            (sec.J / (sec.Sx * sec.ho)) ** 2 + 6.76 * (0.7 * Fy / E) ** 2))
        Cb = 1.0
        if Lb <= Lp:
            Mn = Mp
        elif Lb <= Lr:
            Mn = min(Mp, Cb * (Mp - (Mp - 0.7 * Fy * sec.Sx / 1e6) * (Lb - Lp) / (Lr - Lp)))
        else:
            Fcr = Cb * math.pi ** 2 * E / (Lb / rts) ** 2 * math.sqrt(1 + 0.078 * sec.J / (sec.Sx * sec.ho) *
                                                                       (Lb / rts) ** 2)
            Mn = min(Mp, Fcr * sec.Sx / 1e6)
        Mny = min(Fy * sec.Zy, 1.6 * Fy * sec.Iy / (sec.bf / 2)) / 1e6
        ratio = Mx / (0.9 * Mn) + My / (0.9 * Mny)
        res[combo] = dict(Mx=Mx, My=My, phiMn=0.9 * Mn, phiMny=0.9 * Mny, ratio=ratio, Lb=Lb)
        check(name, f"{sec.name} bending {combo} (Lb {Lb / 1e3:.2f} m, H1-1)", ratio, 1.0, unit="ratio")
    defl = 5 * (wl * c) * L ** 4 / (384 * E * sec.Ix)                    # wl kN/m = N/mm
    check(name, f"{sec.name} deflection under L (<= L/{defl_lim:.0f})", defl, L / defl_lim, unit="mm")
    return dict(sec=sec, L=L, s=s_trib, res=res, defl=defl, wD=wd, wL=wl, wW=ww)


def lightest(name, cands, L, *args, **kw):
    """the lightest candidate that passes every check (the checks of the rejected candidates are discarded)"""
    for nm in cands:
        n0, o0 = len(CHECKS), len(OPEN)
        r = beam_member(name, jis(nm, SS400["Fy"]), L, *args, **kw)
        if all(c[4] <= 1.0 for c in CHECKS[n0:]):
            return r
        del CHECKS[n0:]
        del OPEN[o0:]
    return beam_member(name, jis(cands[-1], SS400["Fy"]), L, *args, **kw)


PURLIN_CANDS = ("H 125x60x6x8", "H 150x75x5x7", "H 175x90x5x8", "H 200x100x5.5x8", "H 250x125x6x9")


def purlin_layout():
    """purlin lines on one roof slope, by horizontal x from the column centre line: eave purlin 200 mm inside the
    eave strut, equal spacing <= 1.2 m along the slope to the last purlin before the monitor post; the monitor
    roof and the canopies are laid out separately"""
    x0, x1 = 600.0, MON_X[0] - 250.0
    n = math.ceil((x1 - x0) / math.cos(THETA) / 1200.0)
    sp = (x1 - x0) / n
    main = [x0 + i * sp for i in range(n + 1)]
    return dict(main=main, spacing_h=sp, spacing_slope=sp / math.cos(THETA))


def design_secondary(D):
    L = roof_loads()
    pl = purlin_layout()
    s = pl["spacing_slope"] / 1e3                                       # tributary width, m
    D["loads"] = dict(L)
    D["purlin_layout"] = pl
    D["PU1"] = lightest("PU1 roof purlin (PROPOSED)", PURLIN_CANDS, BAY, L["SDL"], L["LL"], L["W_up"], s,
                        slope=THETA)
    D["PU2"] = lightest("PU2 canopy purlin (PROPOSED)", PURLIN_CANDS, BAY, L["SDL"], L["LL"], L["W_can"], 1.1,
                        slope=THETA)
    girt_z = [1_500.0, 3_000.0, 4_500.0]                                # side walls: girts at 1.5 m to the eave strut
    D["girt_z"] = girt_z
    D["GT1"] = lightest("GT1 side-wall girt (PROPOSED)", PURLIN_CANDS, BAY, 0.0, 0.0, L["W_wall"], 1.5,
                        slope=math.pi / 2)
    D["GT2"] = lightest("GT2 gable girt (PROPOSED)", PURLIN_CANDS, 4_500.0, 0.0, 0.0, L["W_gable"], 1.5,
                        slope=math.pi / 2, sag=2)
    # sag rods: Ø12 round bar between purlins at third points; the slope component of the gravity load collects
    # down the slope to the eave tie
    wpar = (1.2 * (L["SDL"] * s + D["PU1"]["sec"].kg_m * 9.81e-3) + 1.6 * L["LL"] * s) * math.sin(THETA)
    T = wpar * BAY / 1e3 / 3 * len(pl["main"])                          # kN at the eave end of one sag-rod line
    dr = 12
    for dr in (12, 16, 20):
        if 0.75 * 0.75 * SS400["Fu"] * math.pi * dr * dr / 4 / 1e3 >= T:
            break
    check("SR1 sag rods (PROPOSED)", f"Ø{dr} round bar tension (threads, 0.75 Fu)", T,
          0.75 * 0.75 * SS400["Fu"] * math.pi * dr * dr / 4 / 1e3, unit="kN")
    D["SR1"] = dict(d=dr, T=T)
    # fly braces: angle from the purlin / girt to the inside flange at 45 deg; App. 6 nodal brace force and stiffness
    D["FB1"] = fly_brace("FB1 rafter fly brace (PROPOSED)", d_member=TAPER["H"]["d0"],
                         Mr=abs(D["KJ1"]["forces"]["M_neg"]), Lbr=2 * pl["spacing_slope"], purlin_d=D["PU1"]["sec"].d,
                         member=(RAF.bf, RAF.tw, RAF.tf))
    D["FB2"] = fly_brace("FB2 column fly brace (PROPOSED)", d_member=TAPER["C"]["d1"],
                         Mr=abs(D["KJ1"]["column_forces"]["M_neg"]), Lbr=girt_z[1] - girt_z[0],
                         purlin_d=D["GT1"]["sec"].d, member=(TAPER["C"]["bf"], TAPER["C"]["tw"], TAPER["C"]["tf"]))


ANGLES = {"L 50x50x5": (50, 5, 9.8, 4.80), "L 60x60x5": (60, 5, 11.7, 5.80), "L 65x65x6": (65, 6, 12.7, 7.53),
          "L 75x75x6": (75, 6, 14.6, 8.73)}                              # b, t, rz (mm), A (cm2)


def fly_brace(name, d_member, Mr, Lbr, purlin_d, F=45.0, member=None):
    """360-16 App. 6.3.2a nodal beam brace on the compression flange (S9A): Pbr = 0.02 Mr Cd / ho, Cd = 1;
    stiffness beta = (1/0.75) 10 Mr Cd / (Lbr ho) against EA/L cos^2 F of one angle; KL/rz <= 200"""
    ho = d_member - 12.0
    Pbr = 0.02 * Mr * 1e6 / ho / 1e3                                     # kN, horizontal at the flange
    beta = (1 / 0.75) * 10 * Mr * 1e6 / (Lbr * ho)                       # N/mm
    Lfb = (d_member + purlin_d / 2) / math.sin(math.radians(F))         # along the brace
    for nm, (b, t, rz, A) in ANGLES.items():
        KLr = Lfb / rz
        Fe = math.pi ** 2 * E / KLr ** 2
        Fcr = 0.877 * Fe if KLr > 4.71 * math.sqrt(E / SS400["Fy"]) else (0.658 ** (SS400["Fy"] / Fe)) * SS400["Fy"]
        phiPn = 0.9 * Fcr * A * 100 / 1e3
        k = E * A * 100 / Lfb * math.cos(math.radians(F)) ** 2
        if KLr <= 200 and phiPn >= Pbr / math.cos(math.radians(F)) and k >= beta:
            break
    check(name, f"{nm} strength (App. 6, along the brace)", Pbr / math.cos(math.radians(F)), phiPn, unit="kN")
    check(name, f"{nm} stiffness (App. 6, one angle)", beta, k, unit="N/mm")
    check(name, f"{nm} slenderness KL/rz <= 200", KLr, 200.0, unit="")
    out = dict(angle=nm, L=Lfb, Pbr=Pbr, KLr=KLr, F=F, bolts=f"1-M16 {BOLT_GRADE_SHEAR}/S EACH END")
    out["cleat"] = fly_cleat(name, nm, Pbr / math.cos(math.radians(F)), F, member)
    return out


def fly_cleat(name, ang_name, Pa, F, member, db=16, tc=10.0, h=100.0):
    """member end of the fly brace (engineer's markup of 2/5003, 10/10/2026; Beca SE-1505 cleat "B"): a cleat
    plate each side of the web at the inside flange, welded to the web and the flange, the angle bolted flat on it.
    Work point of the two gauge lines on the member centre line at the outer face of the inside flange (just beyond
    the flange); the angle end square, clear of the web and the flange by 10; 1 bolt, end distance 25.
    Coordinates in the section: x from the web centre line, y from the outer face of the inside flange (into the
    member). Returns the geometry for the drawing and checks the bolt, bearing / tear-out and the welds."""
    b, ta, rz, A = ANGLES[ang_name]
    bf, tw, tf = member
    g = 28.0 if b <= 50 else GAUGE.get(int(b), b / 2 + 5)            # gauge from the heel
    heel, toe = g, b - g
    c, s_ = math.cos(math.radians(F)), math.sin(math.radians(F))
    s_end = 0.0
    while True:                                                       # every corner of the angle clear by 10
        pts = [((s_end - w) * c if False else s_end * c - w * s_, s_end * s_ + w * c) for w in (-heel, toe)]
        if all(x >= tw / 2 + 10 and y >= tf + 10 for x, y in pts):
            break
        s_end += 5.0
    e = 25.0
    s_b = s_end + e
    xb, yb = s_b * c, s_b * s_
    w_c = (bf - tw) / 2
    clip = 15.0
    cham = ceil5(max(0.0, 0.3 * w_c))
    edge_top = tf + h - yb
    edge_out = bf / 2 - xb
    hole = HOLE[db]
    Ab = math.pi * db * db / 4
    check(name + " cleat", f"1-M{db} {BOLT_GRADE_SHEAR} single shear", Pa, 0.75 * BOLT[BOLT_GRADE_SHEAR]["Fnv"] * Ab / 1e3,
          unit="kN")
    check(name + " cleat", f"tear-out on the angle (t {ta:g}, e {e:g})", Pa,
          0.75 * min(1.2 * (e - hole / 2), 2.4 * db) * ta * SS400["Fu"] / 1e3, unit="kN")
    lc = min(edge_top, edge_out) * 1.41 - hole / 2                    # along the brace towards the cleat corner
    check(name + " cleat", f"tear-out on the cleat PL {tc:g}", Pa,
          0.75 * min(1.2 * max(lc, 0.0), 2.4 * db) * tc * SM400["Fu"] / 1e3, unit="kN")
    check(name + " cleat", "edge distances on the cleat (top / outer)", EDGE_MIN[db], min(edge_top, edge_out),
          unit="mm")
    wl = (h - clip) + (w_c - clip)                                    # web + flange welds, both faces 5 mm
    check(name + " cleat", "cleat welds 5 mm both faces (web + flange)", Pa,
          2 * wl * 0.75 * 0.6 * FEXX * 0.707 * 5.0 / 1e3, unit="kN")
    return dict(t=tc, h=h, w=w_c, clip=clip, cham=cham, weld=5.0, db=db, hole=hole, g=g, heel=heel, toe=toe,
                s_end=s_end, s_bolt=s_b, e=e, F=F, member=member, angle_t=ta, b=b)


def design():
    D = {"open": OPEN, "checks": CHECKS}
    design_joints(D)
    design_bases(D)
    design_bracing(D)
    design_secondary(D)
    OPEN.append("Purlins, girts, sag rods and fly braces are not in the MIDAS model: sizes PROPOSED by this calc from the "
                "model's MWFRS pressures; ASSUMED simple spans with sag rods at third points, SS400; ASCE 7 "
                "components-and-cladding pressures (roof zones, wall edge zones) NOT checked - TBC")
    OPEN.append(f"Pedestal concrete f'c {FC_PED:g} MPa ASSUMED for the base-plate bearing; anchor-rod embedment, "
                "breakout and the pedestals are by the RC designer (rod forces on the drawings)")
    OPEN.append("Pipes 'PG' taken as STK490 (Fy 315 MPa) for the connection checks; the MIDAS model used SM520 for "
                "every member - confirm the pipe grade")
    return D


JOINTS = ("KJ1", "CS1", "SP1", "RJ1", "CJ1", "GK1", "GS1", "GS2", "EB1")


def report(D):
    print("=" * 100)
    print("SPF - connection design from the MIDAS model (model/spf_*.json)")
    print(f"roof slope {math.degrees(THETA):.2f} deg ({SLOPE:.4f}); span {SPAN:.0f}; bays {NBAY} x {BAY:.0f}")
    for k in JOINTS:
        r = D[k]
        f = r["forces"]
        print(f"\n{r['name']}: M+ {f['M_pos']:.1f} ({f['case_pos']}), M- {f['M_neg']:.1f} ({f['case_neg']}), "
              f"V {f['V']:.1f} kN, N {f['N_c']:.0f}..{f['N_t']:.0f} kN")
        print(f"   d {r['d']:.0f}  Mu* {r['Mu']:.1f} kN.m ({r['case']})  -> 8-M{r['db']} {r['grade']}  "
              f"PL {r['tp']} x {r['bp']:.0f} x {r['length']:.0f}  (tp req {r['tp_req']:.1f}, Yp {r['Yp']:.0f})  "
              f"g {r['g']:.0f} pf {r['pf']:.0f} de {r['de']:.0f}  phiMnp {r['phiMnp']:.0f}  flange weld "
              f"{r['flange_weld']} web {r['web_weld']}")
        for k2 in ("range", "range_dg16"):
            if k2 in r:
                print("   NOTE:", r[k2])
        if "column" in r:
            c = r["column"]
            print(f"   column side: tfc req {c['tfc_req_unstiff']:.1f} unstiffened / {c['tfc_req_stiff']:.1f} with "
                  f"PL {c['ts']} continuity plates; used {c['tf_used']}; Fsu {c['Fsu']:.0f} kN")
    for k in ("panel_neg", "panel_pos"):
        p = D["KJ1"][k]
        print(f"KJ1 {k}: Vu {p['Vu']:.0f} kN, phiVn {p['phiVn']:.0f} kN, h/tw {p['h_tw']:.0f}, Cv {p['Cv']:.2f}")
    print("\nchecks:")
    bad = 0
    for item, name, dem, cap, r, note, unit in CHECKS:
        member = note == "MODEL MEMBER"                     # the engineer's member: reported, raised as an open item
        flag = "OK" if r <= 1.0 else "MEMBER?" if member else "!! FAIL"
        bad += r > 1.0 and not member
        print(f"  {flag:7s} {item:32s} {name:52s} {dem:9.1f} / {cap:9.1f} {unit:5s} = {r:5.2f} {note}")
    print("\nsecondary framing (PROPOSED):")
    for k in ("PU1", "PU2", "GT1", "GT2"):
        r = D[k]
        print(f"  {k}: {r['sec'].name} span {r['L']:.0f} at {r['s']:.2f} m, "
              + ", ".join(f"{c} {v['ratio']:.2f}" for c, v in r["res"].items()) + f", deflection {r['defl']:.0f} mm")
    print(f"  purlins: {len(D['purlin_layout']['main'])} lines per slope at {D['purlin_layout']['spacing_slope']:.0f} "
          f"mm on the slope; sag rods Ø{D['SR1']['d']} ({D['SR1']['T']:.1f} kN); fly braces {D['FB1']['angle']} / "
          f"{D['FB2']['angle']}")
    print("  loads (kPa):", {k: round(v, 3) for k, v in D["loads"].items()})
    for k in ("BP1", "BP2"):
        b = D[k]
        print(f"  {k}: PL {b['tp']} x {b['B']} x {b['W']}, {b['rods']}-M{b['db']} rods, Pu {b['Pu']:.0f} "
              f"Tu {b['Tu']:.0f} Vu {b['Vu']:.0f} kN, weld {b['weld']}")
    b = D["BR1"]
    print(f"  BR1: {b['sec']} tension-only T {b['Pt']:.0f} kN -> {b['n']}-M{b['db']} at {b['p']:g} (e {b['e1']:g}, "
          f"g {b['g']:g}), U {b['U']:.2f}; gusset GU1 PL {D['GU1']['tg']:g}, web weld length {D['GU1']['L']:.0f}, "
          f"outline {D['GU1']['geo']['poly']}")
    for k in ("ST1", "ST2"):
        b = D[k]
        print(f"  {k}: {b['pipe']} T {b['Pt']:.0f} C {b['Pc']:.0f} kN -> {b['n']}-M{b['db']}, knife PL {b['tk']:g} x "
              f"{b['bk']:g}, lap {b['lap']:g}, slot welds {b['weld']:g}")
    print("\nopen items raised by the calc:")
    for o in OPEN:
        print("  -", o)
    return bad


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(1 if report(design()) else 0)
