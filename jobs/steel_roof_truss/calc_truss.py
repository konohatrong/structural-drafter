"""
Steel roof truss T1 - preliminary design: Pratt truss of circular hollow sections (JIS G 3444 STK400).

    python calc_truss.py            # prints the design report
    from calc_truss import design   # the drawing script takes sizes, nodes and connection data from here

Geometry (user, 2026-10-03): span 25.0 m, depth 1.25 m between chord centre lines, 20 panels of 1.25 m,
a vertical at every node, diagonals at 45 deg sloping down toward midspan (tension under gravity).
Basis (user, 2026-10-03): roof trusses at 6.0 m c/c, metal sheet on purlins at every top-chord node; welded
CHS-to-CHS gap joints, 3 shop pieces joined by bolted flange-plate splices; bottom-chord bearing on RC.
Design: AISC 360-16 LRFD (D tension, E compression, F8 round HSS flexure, H1 interaction, J welds and bolts,
K2 plate-to-round HSS (Table K2.1), K3 round HSS-to-HSS truss joints (Table K3.1, limits Table K3.1A)) with
AISC Design Guide 24 (2010): effective lengths 8.4, unbalanced K + X / Y joints 8.2, flange splice 5.4 (Eqs 5-5 to
5-13), slotted tube end with a knife plate 5.3 / Ex 5.2; branch welds to AWS D1.1:2015 Fig 9.10 (tubular
fillet zones heel / side / toe by the local dihedral angle) developing the branch wall (DG24 2.1, DG21 12);
load combinations ASCE 7-16 2.3. Units N, mm, MPa unless stated (kN, kN.m, kPa in the report).
References in the comments: DG24 = AISC Design Guide 24, DG21 = AISC Design Guide 21, DSC = AISC Detailing for
Steel Construction (3rd ed.); summarised in SOURCES_STEEL_DETAILING.md at the repo root.
"""
import math

import numpy as np

# --------------------------------------------------------------------------- basis
E = 200000.0
FY, FU = 235.0, 400.0              # STK400 (JIS G 3444): YS >= 235, TS >= 400
T_DES = 0.93                       # design wall = 0.93 x nominal (AISC B4.2, ERW pipe; conservative for STK)
FEXX = 490.0                       # E49XX / E70XX electrodes
BOLT_FU = 800.0                    # bolts M20 grade 8.8 (ISO 898-1) - JIS F10T is stronger
ROD_FU = 400.0                     # anchor rods SS400
FC = 24.0                          # concrete under the bearing (RC column / beam top), f'c

L, H, NP = 25000.0, 1250.0, 20     # span, depth (c/c chords), number of panels
A_P = L / NP                       # panel length 1250
S_TRUSS = 6.0                      # m, truss spacing
Q_SDL = 0.30                       # kPa: metal sheet 0.05 + purlins 0.10 + insulation / services 0.15
Q_LR = 0.50                        # kPa: roof live load, Ministerial Regulation No. 6 (B.E. 2527), 50 kg/m2
Q_W = 0.75                         # kPa: net wind uplift on the roof - ASSUMED, verify per DPT 1311
SW_EXTRA = 1.15                    # self-weight x 1.15 for welds, plates, splices
BC_BRACE = (0, 4, 8, 12, 16, 20)   # bottom-chord nodes held laterally by fly braces (5.0 m)
K_CHORD, K_WEB = 0.9, 0.75         # effective length factors of a welded CHS truss (DG24 8.4, p.102)
SPLICE_PANELS = (6, 13)            # field splices in these panels (chords cut mid-panel, that diagonal loose)
CAMBER_ROUND = 5.0
E_TYP = 12.0                       # work-point eccentricity of every K-node (one setting-out rule), mm;
                                   # a node needing more for its minimum gap (end nodes) gets its own, whole mm

# JIS G 3444 sizes (outside diameter mm: wall thicknesses mm) - confirm stock with the supplier (TIS 107)
JIS = {48.6: (2.3, 2.8, 3.2), 60.5: (2.3, 3.2, 4.0), 76.3: (2.8, 3.2, 4.0), 89.1: (2.8, 3.2), 101.6: (3.2, 4.0, 5.0),
       114.3: (3.2, 3.5, 4.5), 139.8: (3.5, 4.0, 4.5, 6.0), 165.2: (4.5, 5.0, 6.0, 7.1),
       190.7: (4.5, 5.3, 6.0, 7.0, 8.2), 216.3: (4.5, 5.8, 6.0, 7.0, 8.0, 8.2), 267.4: (6.0, 6.6, 7.0, 8.0, 9.0)}
CHORD_D = (114.3, 139.8, 165.2, 190.7, 216.3, 267.4)
WEB_D = (48.6, 60.5, 76.3, 89.1, 101.6, 114.3, 139.8)


class CHS:
    def __init__(self, D, t):
        self.D, self.t = D, t
        td = T_DES * t
        self.td = td
        di = D - 2 * td
        self.A = math.pi / 4 * (D ** 2 - di ** 2)
        self.I = math.pi / 64 * (D ** 4 - di ** 4)
        self.r = math.sqrt(self.I / self.A)
        self.S = 2 * self.I / D
        self.Z = (D ** 3 - di ** 3) / 6
        self.kgm = 0.02466 * t * (D - t)           # JIS nominal mass, kg/m

    @property
    def name(self):
        return f"CHS {self.D:g} x {self.t:g}"

    def __repr__(self):
        return self.name


SECTIONS = sorted((CHS(D, t) for D, ts in JIS.items() for t in ts), key=lambda s: s.kgm)


# --------------------------------------------------------------------------- geometry
def geometry():
    """nodes: bottom 'B0'..'B20' at y = 0, top 'T0'..'T20' at y = H. members: (name, group, node i, node j)"""
    nodes = {}
    for k in range(NP + 1):
        nodes[f"B{k}"] = (k * A_P, 0.0)
        nodes[f"T{k}"] = (k * A_P, H)
    mem = []
    for k in range(NP):
        mem.append((f"TC{k}", "TC", f"T{k}", f"T{k + 1}"))
        mem.append((f"BC{k}", "BC", f"B{k}", f"B{k + 1}"))
        top, bot = (f"T{k}", f"B{k + 1}") if k < NP // 2 else (f"T{k + 1}", f"B{k}")
        mem.append((f"D{k}", "DE" if k < 5 or k >= NP - 5 else "DM", top, bot))
    for k in range(NP + 1):
        mem.append((f"V{k}", "VE" if k in (0, NP) else "VM", f"B{k}", f"T{k}"))
    return nodes, mem


GROUPS = {"TC": "TOP CHORD", "BC": "BOTTOM CHORD", "DE": "END DIAGONALS (PANELS 1-5, 16-20)",
          "DM": "MIDDLE DIAGONALS (PANELS 6-15)", "VE": "END VERTICALS (AT SUPPORTS)", "VM": "VERTICALS"}


def length(nodes, i, j):
    (x1, y1), (x2, y2) = nodes[i], nodes[j]
    return math.hypot(x2 - x1, y2 - y1)


# --------------------------------------------------------------------------- analysis
def solve(nodes, mem, sec, loads):
    """pin-jointed plane truss, direct stiffness. loads {node: (Fx, Fy)} in N. Pin at B0, roller at B20.
    returns axial forces {member: N} (tension +), reactions {node: (Rx, Ry)}, displacements {node: (ux, uy)}"""
    idx = {n: k for k, n in enumerate(nodes)}
    K = np.zeros((2 * len(nodes), 2 * len(nodes)))
    geo = {}
    for name, g, i, j in mem:
        (x1, y1), (x2, y2) = nodes[i], nodes[j]
        Lm = math.hypot(x2 - x1, y2 - y1)
        c, s = (x2 - x1) / Lm, (y2 - y1) / Lm
        k = E * sec[g].A / Lm
        geo[name] = (i, j, c, s, k)
        dofs = [2 * idx[i], 2 * idx[i] + 1, 2 * idx[j], 2 * idx[j] + 1]
        v = np.array([-c, -s, c, s])
        K[np.ix_(dofs, dofs)] += k * np.outer(v, v)
    F = np.zeros(2 * len(nodes))
    for n, (fx, fy) in loads.items():
        F[2 * idx[n]] += fx
        F[2 * idx[n] + 1] += fy
    fixed = [2 * idx["B0"], 2 * idx["B0"] + 1, 2 * idx[f"B{NP}"] + 1]
    free = [d for d in range(len(F)) if d not in fixed]
    u = np.zeros(len(F))
    u[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
    R = K @ u - F
    forces = {}
    for name, (i, j, c, s, k) in geo.items():
        forces[name] = k * ((u[2 * idx[j]] - u[2 * idx[i]]) * c + (u[2 * idx[j] + 1] - u[2 * idx[i] + 1]) * s)
    reac = {n: (R[2 * idx[n]], R[2 * idx[n] + 1]) for n in ("B0", f"B{NP}")}
    disp = {n: (u[2 * idx[n]], u[2 * idx[n] + 1]) for n in nodes}
    return forces, reac, disp


def load_cases(nodes, mem, sec):
    """unfactored nodal loads (N, +y up): D (roof SDL + self-weight), Lr full, Lr left half, W uplift"""
    trib = {k: (0.5 if k in (0, NP) else 1.0) * A_P / 1000 * S_TRUSS for k in range(NP + 1)}   # m2 per top node
    D, Lr, LrL, W = ({n: (0.0, 0.0) for n in nodes} for _ in range(4))

    def add(case, n, fy):
        case[n] = (case[n][0], case[n][1] + fy)

    for k in range(NP + 1):
        add(D, f"T{k}", -Q_SDL * trib[k] * 1000)
        add(Lr, f"T{k}", -Q_LR * trib[k] * 1000)
        if k * A_P <= L / 2 + 1:
            add(LrL, f"T{k}", -Q_LR * trib[k] * 1000 * (0.5 if k == NP // 2 else 1.0))
        add(W, f"T{k}", +Q_W * trib[k] * 1000)
    sw = 0.0
    for name, g, i, j in mem:
        w = sec[g].kgm * 9.81 * length(nodes, i, j) / 1000 * SW_EXTRA   # N
        sw += w
        add(D, i, -w / 2)
        add(D, j, -w / 2)
    return {"D": D, "Lr": Lr, "LrL": LrL, "W": W}, sw


COMBOS = {"1.4D": {"D": 1.4},
          "1.2D+1.6Lr": {"D": 1.2, "Lr": 1.6},
          "1.2D+1.6Lr(half)": {"D": 1.2, "LrL": 1.6},
          "0.9D+1.0W": {"D": 0.9, "W": 1.0}}


def analyse(sec):
    nodes, mem = geometry()
    cases, sw = load_cases(nodes, mem, sec)
    unit = {c: solve(nodes, mem, sec, cases[c]) for c in cases}
    res = {}
    for cn, fac in COMBOS.items():
        f = {m: sum(fac[c] * unit[c][0][m] for c in fac) for m in unit["D"][0]}
        r = {n: tuple(sum(fac[c] * unit[c][1][n][a] for c in fac) for a in (0, 1)) for n in unit["D"][1]}
        res[cn] = (f, r)
    return nodes, mem, cases, unit, res, sw


# --------------------------------------------------------------------------- member strength (AISC 360-16)
def phi_pc(s, KL):
    """E3: flexural buckling, nonslender round HSS (D/t <= 0.11 E/Fy, B4.1a)"""
    Fe = math.pi ** 2 * E / (KL / s.r) ** 2
    Fcr = 0.658 ** (FY / Fe) * FY if FY / Fe <= 2.25 else 0.877 * Fe
    return 0.9 * Fcr * s.A


def phi_pt(s):
    """D2: yielding of the gross section; rupture with U = 1 (welded all round) does not govern for STK400"""
    return min(0.9 * FY * s.A, 0.75 * FU * s.A)


def phi_mn(s):
    """F8: round HSS, compact if D/t <= 0.07 E/Fy, else noncompact (F8-2)"""
    lam = s.D / s.td
    Mn = FY * s.Z if lam <= 0.07 * E / FY else (0.021 * E / lam + FY) * s.S
    return 0.9 * Mn


def interaction(Pr, Pc, Mr, Mc):
    """H1-1a / H1-1b"""
    if Pr / Pc >= 0.2:
        return Pr / Pc + 8 / 9 * Mr / Mc
    return Pr / (2 * Pc) + Mr / Mc


def unbraced(name, g, nodes, i, j):
    """(in-plane, out-of-plane) unbraced lengths: top chord held at every node by purlins + roof bracing; bottom
    chord out of plane only at BC_BRACE nodes; web members their full length"""
    Lm = length(nodes, i, j)
    if g == "BC":
        k = int(name[2:])
        a = max(b for b in BC_BRACE if b <= k)
        b = min(b for b in BC_BRACE if b >= k + 1)
        return Lm, (b - a) * A_P
    return Lm, Lm


def k_eff(g):
    return K_CHORD if g in ("TC", "BC") else K_WEB


# --------------------------------------------------------------------------- joints (AISC 360-16 K3, Table K3.1)
def node_branches(mem, node):
    return [(n, g, i, j) for n, g, i, j in mem if node in (i, j) and g not in ("TC", "BC")]


def theta(nodes, i, j):
    (x1, y1), (x2, y2) = nodes[i], nodes[j]
    return math.degrees(math.atan2(abs(y2 - y1), abs(x2 - x1)))


def gap_ecc(D, b1, th1, b2, th2, g):
    """eccentricity e of the branch work point from the chord axis (+ away from the branches) for a gap g between
    two branches (Packer & Henderson / CIDECT): e = (d1/2sin1 + d2/2sin2 + g) sin1 sin2 / sin(1+2) - D/2"""
    s1, s2 = math.sin(math.radians(th1)), math.sin(math.radians(th2))
    s12 = math.sin(math.radians(th1 + th2))
    return (b1 / (2 * s1) + b2 / (2 * s2) + g) * s1 * s2 / s12 - D / 2


# --------------------------------------------------------------------------- drawn geometry (work points)
G_MIN = 20.0                       # gap between branch toes on the chord face: >= tb1 + tb2 (K3.1A), >= 20 to weld
G_ABS = 12.0                       # least gap accepted where e is held at E_MAX D (both toe welds still fit)
E_MAX = 0.25                       # e / D <= 0.25 (Table K3.1A; the e-moment is then still added to the chords)


def web_list(mem):
    """[(name, group, top node, bottom node)] of the diagonals and verticals"""
    out = []
    for n, g, i, j in mem:
        if g not in ("TC", "BC"):
            out.append((n, g, i, j) if i[0] == "T" else (n, g, j, i))
    return out


def outline(sec, nodes, ecc, w):
    """web member w between the chord faces, its axis through the two work points (node offset by e away
    from the web): (two outline lines [(p_top, p_bot)], axis points on the faces, unit vector top -> bottom)"""
    n, g, top, bot = w
    D = sec["TC"].D
    (xt, yt), (xb, yb) = nodes[top], nodes[bot]
    yt, yb = yt + ecc.get(top, 0.0), yb - ecc.get(bot, 0.0)
    Lm = math.hypot(xb - xt, yb - yt)
    u = ((xb - xt) / Lm, (yb - yt) / Lm)
    nv = (-u[1], u[0])
    ft, fb = H - D / 2, D / 2

    def at(p, y):
        t = (y - p[1]) / u[1]
        return (p[0] + t * u[0], p[1] + t * u[1])

    lines = []
    for sgn in (1, -1):
        p = (xt + sgn * sec[g].D / 2 * nv[0], yt + sgn * sec[g].D / 2 * nv[1])
        lines.append((at(p, ft), at(p, fb)))
    return lines, (at((xt, yt), ft), at((xt, yt), fb)), u


def geometry_gaps(sec, nodes, mem, ecc):
    """{node: [gaps between neighbouring branch toes on the chord face]} and {member: theta deg} as drawn"""
    webs = web_list(mem)
    th, foot = {}, {}
    for w in webs:
        lines, _, u = outline(sec, nodes, ecc, w)
        th[w[0]] = math.degrees(math.atan2(abs(u[1]), abs(u[0])))
        for k, node in ((0, w[2]), (1, w[3])):
            xs = [ln[k][0] for ln in lines]
            foot.setdefault(node, []).append((min(xs), max(xs), w[0]))
    gaps = {}
    for node, iv in foot.items():
        iv.sort()
        gaps[node] = [(b[0] - a[1], a[2], b[2]) for a, b in zip(iv, iv[1:])]
    return gaps, th


_LAYOUT = {}


def layout(sec, nodes, mem):
    """cached per set of web / chord sections (the size search calls it for every trial)"""
    key = tuple(sec[g].name for g in GROUPS)
    if key not in _LAYOUT:
        try:
            _LAYOUT[key] = _layout(sec, nodes, mem)
        except LayoutError as ex:
            _LAYOUT[key] = ex
    if isinstance(_LAYOUT[key], LayoutError):
        raise _LAYOUT[key]
    return _LAYOUT[key]


class LayoutError(Exception):
    pass


def g_abs(tb1, tb2):
    """absolute minimum gap where e is at its limit: Table K3.1A g >= tb1 + tb2, and an office floor of 12 mm
    so the two toe welds can still be made (DG24 Ex 8.3: about 24 mm is comfortably weldable)"""
    return max(G_ABS, tb1 + tb2)


def _layout(sec, nodes, mem):
    """work-point eccentricities: one value E_TYP for every K-node, the end top nodes (large end vertical) their
    own; both raised in whole mm until every gap as drawn is >= max(G_MIN, tb1 + tb2). e never exceeds
    E_MAX D (Table K3.1A); a class held at that limit accepts gaps down to g_abs instead of G_MIN"""
    webs = web_list(mem)
    count = {}
    for w in webs:
        for nd in w[2:]:
            count[nd] = count.get(nd, 0) + 1
    ends = {nd for w in webs if w[1] == "VE" for nd in w[2:] if nd[0] == "T"}
    D = sec["TC"].D
    e_cap = math.floor(E_MAX * D)

    def est(ws):                                    # closed form at 45 deg (gap_ecc), a start for the search
        return max([gap_ecc(D, sec[a].D, 90, sec[b].D, 45, max(G_MIN, sec[a].t + sec[b].t)) for a, b in ws] or [0])
    e_typ = min(e_cap, max(E_TYP, math.floor(est([("VM", "DE"), ("VM", "DM")]))))
    e_end = min(e_cap, max(e_typ, math.floor(est([("VE", "DE")]))))
    for _ in range(200):
        ecc = {nd: (e_end if nd in ends else e_typ) if c > 1 else 0.0 for nd, c in count.items()}
        gaps, th = geometry_gaps(sec, nodes, mem, ecc)
        short = []
        for nd, gs in gaps.items():
            capped = (e_end if nd in ends else e_typ) >= e_cap
            for g in gs:
                t1, t2 = sec[group_of(mem, g[1])].t, sec[group_of(mem, g[2])].t
                need = g_abs(t1, t2) if capped else max(G_MIN, t1 + t2)
                if g[0] < need - 1e-6:
                    short.append((nd, capped))
        if not short:
            return ecc, gaps, th
        if any(c for _, c in short):
            raise LayoutError(f"gap below the minimum with e at its limit {e_cap} mm (e/D {E_MAX})")
        if any(nd in ends for nd, _ in short):
            e_end += 1
        if any(nd not in ends for nd, _ in short):
            e_typ += 1
    raise LayoutError("no eccentricity gives the minimum gaps")


def group_of(mem, name):
    return next(g for n, g, *_ in mem if n == name)


def qg(D, t, g):
    gam = D / (2 * t)
    return gam ** 0.2 * (1 + 0.024 * gam ** 1.2 / (math.exp(0.5 * g / t - 1.33) + 1))


def qf(chord, Pro, Mro):
    """chord stress interaction: 1.0 for a chord in tension; Pro = force on the side with lower compression"""
    if Pro >= 0:
        return 1.0
    U = abs(Pro / (FY * chord.A)) + abs(Mro / (FY * chord.S))
    return 1 - 0.3 * U * (1 + U)


def joints(sec, nodes, mem, res):
    """every chord node: geometry (gap, eccentricity), limits of applicability (Table K3.1A), strength per
    combination (Table K3.1). An unbalanced node (DG24 8.2, Fig 8-4): the balanced part acts as a K-joint, the
    rest as an X-joint at a top node (purlin load on the opposite face) or a T/Y-joint at a bottom node, the two
    utilisations added. returns {node: dict} with utilisation and messages"""
    out = {}
    try:
        ecc, ggeo, thg = layout(sec, nodes, mem)
    except LayoutError as ex:
        return {"layout": dict(branches=[], gaps=[], e=0.0, util=9.99, msgs=[str(ex)])}
    gam_max = 0.05 * E / FY                                              # compression branch Db/tb (K3.1A)
    for node in nodes:
        side = node[0]
        chord = sec["TC" if side == "T" else "BC"]
        br = node_branches(mem, node)
        if not br:
            continue
        info = []
        for n, g, i, j in br:
            other = j if i == node else i
            info.append(dict(name=n, g=g, sec=sec[g], th=thg[n], dx=nodes[other][0] - nodes[node][0]))
        info.sort(key=lambda b: b["dx"])
        gaps = [g[0] for g in ggeo.get(node, [])]                      # as drawn (work points offset by e)
        e = ecc.get(node, 0.0)
        support = node in ("B0", f"B{NP}")
        msgs, util = [], 0.0
        # Table K3.1A limits of applicability
        if FY > 360 or FY / FU > 0.8:
            msgs.append("material outside Fy <= 360, Fy/Fu <= 0.8")
        if chord.D / chord.td > (40 if support else 50):
            msgs.append(f"chord D/t {chord.D / chord.td:.0f} > {40 if support else 50}")
        if gaps and not -0.55 <= e / chord.D <= E_MAX:
            msgs.append(f"e/D {e / chord.D:.2f} outside -0.55..{E_MAX}")
        for b in info:
            s = b["sec"]
            beta = s.D / chord.D
            lo = 0.4 if gaps else 0.2                                  # gapped K: 0.4 <= Db/D
            if not lo <= beta <= 1.0:
                msgs.append(f"{b['name']} Db/D {beta:.2f} outside {lo}..1.0")
            if s.D / s.td > 50:
                msgs.append(f"{b['name']} Db/tb > 50")
            if any(r[0][b["name"]] < 0 for r in res.values()) and s.D / s.td > gam_max:
                msgs.append(f"{b['name']} compression Db/tb {s.D / s.td:.0f} > 0.05E/Fy {gam_max:.0f}")
            if s.t > chord.t:
                msgs.append(f"{b['name']} tb > chord t (office rule)")
            if b["th"] < 30:
                msgs.append(f"{b['name']} theta < 30")
        # strength per combination
        chs = [m for m in mem if m[1] in ("TC", "BC") and node in (m[2], m[3]) and m[1][0] == side]
        gam = chord.D / (2 * chord.td)
        for cn, (f, _) in res.items():
            cf = [f[m[0]] for m in chs]
            dN = abs(cf[0] - cf[1]) if len(cf) == 2 else abs(cf[0])
            Mro = dN * abs(e) / 2                                     # eccentricity moment, half to each side
            Pro = max(cf) if all(c < 0 for c in cf) else 1.0          # lower compression side (max of negatives)
            Q = qf(chord, Pro, Mro)
            perp = [f[b["name"]] * math.sin(math.radians(b["th"])) for b in info]
            uk = 0.0
            for b in info:
                s, th = b["sec"], math.radians(b["th"])
                P = abs(f[b["name"]])
                # shear yielding (punching), phi 0.95, when Db < D - 2t
                if s.D < chord.D - 2 * chord.td:
                    pn = 0.6 * FY * chord.td * math.pi * s.D * (1 + math.sin(th)) / (2 * math.sin(th) ** 2)
                    util = max(util, P / (0.95 * pn))
                if len(info) > 1:                                      # gap K: chord plastification (K3-6)
                    comp = [x["sec"].D for x in info if f[x["name"]] < 0] or [s.D]
                    pn = (FY * chord.td ** 2 * (2.0 + 11.33 * min(comp) / chord.D)
                          * qg(chord.D, chord.td, min(gaps) if gaps else G_MIN) * Q / math.sin(th))
                    uk = max(uk, P / (0.9 * pn))
            net = abs(sum(perp))
            big = max(abs(p) for p in perp)
            if support:                                               # the end vertical's load passes through
                beta = info[0]["sec"].D / chord.D                     # the chord to the bearing saddle below:
                pn_sin = FY * chord.td ** 2 * 5.7 / (1 - 0.81 * beta) * Q        # X-joint (K3-3)
                util = max(util, uk, net / (0.9 * pn_sin))
                continue
            if len(info) > 1 and net <= 0.2 * big:                    # balanced within 0.8 - 1.2: pure K
                util = max(util, uk)
                continue
            sgn = 1 if sum(perp) > 0 else -1                          # the branch carrying the remainder
            carrier = max(info, key=lambda b: sgn * f[b["name"]] * math.sin(math.radians(b["th"])))
            beta = carrier["sec"].D / chord.D
            if side == "T":                                           # X: the purlin load opposite (DG24 Ex 8.5)
                pn_sin = FY * chord.td ** 2 * 5.7 / (1 - 0.81 * beta) * Q
            else:                                                     # T/Y (K3-4)
                pn_sin = FY * chord.td ** 2 * (3.1 + 15.6 * beta ** 2) * gam ** 0.2 * Q
            u_xy = net / (0.9 * pn_sin)
            util = max(util, uk, uk * (1 - net / big) + u_xy if len(info) > 1 else u_xy)
        out[node] = dict(branches=info, gaps=gaps, e=e, util=util, msgs=msgs)
    return out


def gap_from_e(D, b1, th1, b2, th2, e):
    s1, s2 = math.sin(math.radians(th1)), math.sin(math.radians(th2))
    s12 = math.sin(math.radians(th1 + th2))
    return (e + D / 2) * s12 / (s1 * s2) - b1 / (2 * s1) - b2 / (2 * s2)


# --------------------------------------------------------------------------- member checks
def member_checks(sec, nodes, mem, res, jt):
    """utilisation per member: tension, compression (both planes), compression + eccentricity moment (chords)"""
    out = {}
    for name, g, i, j in mem:
        s = sec[g]
        Lx, Ly = unbraced(name, g, nodes, i, j)
        pc = phi_pc(s, k_eff(g) * max(Lx, Ly))
        pt, mc = phi_pt(s), phi_mn(s)
        u = 0.0
        for cn, (f, _) in res.items():
            N = f[name]
            M = 0.0
            if g in ("TC", "BC"):
                M = max((abs(jt[n]["e"]) * chord_dN(mem, f, n) / 2 if n in jt else 0.0) for n in (i, j))
            u = max(u, interaction(abs(N), pt if N >= 0 else pc, M, mc))
        out[name] = u
    return out


def chord_dN(mem, f, node):
    side = node[0]
    cf = [f[m[0]] for m in mem if m[1] in ("TC", "BC") and m[1][0] == side and node in (m[2], m[3])]
    return abs(cf[0] - cf[1]) if len(cf) == 2 else abs(cf[0])


# --------------------------------------------------------------------------- sizing
def size(sw_guess_sec=None):
    """lightest JIS sections, by group: chords first, webs member-minimal, then upgraded until every joint passes.
    Iterates on self-weight until the sizes no longer change."""
    sec = sw_guess_sec or {g: CHS(165.2, 6.0) if g in ("TC", "BC") else CHS(76.3, 3.2) for g in GROUPS}
    for _ in range(4):
        nodes, mem, cases, unit, res, sw = analyse(sec)
        best = None
        chords = [s for s in SECTIONS if s.D in CHORD_D]
        webs = [s for s in SECTIONS if s.D in WEB_D]
        for ch in chords:                                          # one chord section, top and bottom: one
            trial = dict(sec, TC=ch, BC=ch)                        # flange splice, one set of node details
            trial = pick_webs(trial, webs, nodes, mem, res)
            if trial is None:
                continue
            w = weight(trial, nodes, mem)
            if best is None or w < best[0]:
                best = (w, trial)
        new = best[1]
        if all(new[g].name == sec[g].name for g in GROUPS):
            return new
        sec = new
    return sec


def pick_webs(sec, webs, nodes, mem, res):
    """web groups: lightest section passing the member checks, then upgrade the branches of failing joints"""
    sec = dict(sec)
    d_min = 0.4 * max(sec["TC"].D, sec["BC"].D)                      # gapped K: Db/D >= 0.4 (Table K3.1A)
    for g in ("DE", "DM", "VE", "VM"):
        ok = [s for s in webs if s.D >= d_min and member_ok(s, g, nodes, mem, res)]
        if not ok:
            return None
        sec[g] = ok[0]
    for _ in range(40):
        jt = joints(sec, nodes, mem, res)
        if "layout" in jt:
            return None                                            # e at its limit and the gaps still short
        mu = member_checks(sec, nodes, mem, res, jt)
        bad_j = [n for n, d in jt.items() if d["util"] > 1.0 or d["msgs"]]
        bad_m = [m for m, u in mu.items() if u > 1.0]
        if not bad_j and not bad_m:
            return sec
        if any(m[:2] in ("TC", "BC") for m in bad_m):
            return None                                            # chord members fail: next chord pair
        chord_rule = [m for n in bad_j for m in jt[n]["msgs"] if "chord" in m or "e/D" in m or "tb >" in m]
        if chord_rule:
            return None
        # upgrade the web group with the most failing joints to the next heavier, larger-diameter section
        count = {}
        for n in bad_j:
            for b in jt[n]["branches"]:
                count[b["g"]] = count.get(b["g"], 0) + 1
        g = max(count, key=count.get)
        nxt = [s for s in webs if s.kgm > sec[g].kgm and s.D >= sec[g].D and member_ok(s, g, nodes, mem, res)]
        if not nxt:
            return None
        sec[g] = nxt[0]
    return None


def member_ok(s, g, nodes, mem, res):
    for name, gg, i, j in mem:
        if gg != g:
            continue
        Lx, Ly = unbraced(name, g, nodes, i, j)
        for f, _ in res.values():
            N = f[name]
            if N >= 0 and N > phi_pt(s):
                return False
            if N < 0 and -N > phi_pc(s, k_eff(g) * max(Lx, Ly)):
                return False
    return True


def weight(sec, nodes, mem):
    return sum(sec[g].kgm * length(nodes, i, j) / 1000 for _, g, i, j in mem)


# --------------------------------------------------------------------------- welds
LEGS = (3, 4, 5, 6, 8, 10, 12)     # fillet legs used, mm
Z_LOSS = 3.0                       # AWS D1.1 Table 9.5, 60 > Psi >= 45 deg, SMAW / any process in V or OH


def leg_std(x):
    """smallest standard leg >= x (0.1 mm tolerance: 1.5 x 4.0 = 6.0 stays 6)"""
    return next(v for v in LEGS if v >= x - 0.1)


def j24_min(t_thin):
    """AISC 360-16 Table J2.4 minimum fillet by the thinner part joined"""
    return 3 if t_thin <= 6 else 5 if t_thin <= 13 else 6 if t_thin <= 19 else 8


def throat_wall(t):
    """effective throat that develops a wall t in tension: 0.9 Fy t_des = 0.75 x 0.6 FEXX a (DG24 2.1 philosophy 1,
    DG21 12: HSS welds are sized to the wall, not the force, so they cannot unzip). No directional increase."""
    return 0.9 * FY * T_DES * t / (0.75 * 0.6 * FEXX)


def weld_leg(t):
    """fillet leg developing a wall t in a plain T-joint (dihedral about 90 deg): a / 0.707, standard size,
    >= J2.4 minimum"""
    return max(j24_min(t), leg_std(throat_wall(t) * math.sqrt(2)))


def dihedral(d, D, th_deg, n=72):
    """local dihedral angle Psi (deg) round a round branch d on a round chord D at th_deg (AWS D1.1 Fig 9.10):
    Psi = acos(-n_branch . n_chord) at points of the intersection curve, outward surface normals"""
    th = math.radians(th_deg)
    R, r = D / 2, d / 2
    a = np.array([math.cos(th), math.sin(th), 0.0])
    e1 = np.array([-math.sin(th), math.cos(th), 0.0])
    e2 = np.array([0.0, 0.0, 1.0])
    out = []
    for ph in np.linspace(0, 2 * math.pi, n, endpoint=False):
        nb = math.cos(ph) * e1 + math.sin(ph) * e2
        b = r * nb
        A, B, Cc = a[1] ** 2, 2 * b[1] * a[1], b[1] ** 2 + b[2] ** 2 - R * R
        p = b + (-B + math.sqrt(B * B - 4 * A * Cc)) / (2 * A) * a
        out.append(math.degrees(math.acos(-nb @ (np.array([0.0, p[1], p[2]]) / R))))
    return out


def branch_weld(b, chord, th_deg):
    """AWS D1.1:2015 Fig 9.10 fillet-welded tubular joint, column E = t (the wall needs E >= 0.89 t, throat_wall):
    zones present round this branch and their minimum legs L (mm). heel (Psi < 60): 1.5t, + Z loss (Table 9.5);
    side Psi <= 100: 1.4t, 100 - 110: 1.6t, 110 - 120: 1.8t; toe (Psi > 120): branch edge bevelled, L = 1.4t."""
    t = b.t
    assert throat_wall(t) <= t + 1e-9
    psi = dihedral(b.D, chord.D, th_deg)
    lo, hi = min(psi), max(psi)
    z = {}
    if lo < 60:
        z["HEEL"] = 1.5 * t + Z_LOSS
    side_hi = min(hi, 120.0)
    z["SIDE"] = 1.4 * t if side_hi <= 100 else 1.6 * t if side_hi <= 110 else 1.8 * t
    if hi > 120:
        z["TOE"] = 1.4 * t
    legs = {k: max(j24_min(t), leg_std(v)) for k, v in z.items()}
    return dict(psi=(lo, hi), legs=legs, E=t, bevel="TOE" in legs)


# --------------------------------------------------------------------------- bolts
def bolt_length(grip, d, washers=1):
    """bolt length: grip + hardened washers (4 mm for M20) + heavy nut (0.8d) + 3 threads stick-out, up to 5 mm"""
    need = grip + 4 * washers + 0.8 * d + 3 * 2.5
    return int(math.ceil(need / 5) * 5)


# --------------------------------------------------------------------------- connections
def flange_splice(chord, Tu, n_bolts=6, db=20, e1=40.0):
    """DG24 5.4 (Eqs 5-5 to 5-13, Fig 5-4) / CIDECT DG7: circular flange plates, bolts on a circle, a = b = e1 >= 38.
    Tu = factored design tension (N). Weld: DG24 Eq 5-7 for Tu, >= J2.4 minimum; compression by contact."""
    r3 = chord.D / 2 - chord.td / 2
    r2 = chord.D / 2 + e1
    r1 = chord.D / 2 + 2 * e1
    k1 = math.log(r2 / r3)
    k3 = k1 + 2
    f3 = (k3 + math.sqrt(k3 ** 2 - 4 * k1)) / (2 * k1)
    tp_req = math.sqrt(2 * Tu / (0.9 * FY * math.pi * f3))
    tp = max(16, math.ceil(tp_req / 2) * 2)
    ab = math.pi * db ** 2 / 4
    phi_rn = 0.75 * 0.75 * BOLT_FU * ab                              # J3: Fnt = 0.75 Fu
    per_bolt = Tu / n_bolts * (1 - 1 / f3 + 1 / (f3 * math.log(r1 / r2)))
    w_req = Tu * math.sqrt(2) / (0.75 * 0.6 * FEXX * math.pi * chord.D)          # DG24 Eq 5-7
    weld = max(j24_min(min(chord.t, tp)), leg_std(w_req))
    u = dict(plate=(tp_req / tp) ** 2, bolts=per_bolt / phi_rn)
    return dict(tp=tp, tp_req=tp_req, n=n_bolts, db=db, bc=2 * r2, od=2 * r1, a=e1, b=e1, f3=f3,
                per_bolt=per_bolt, phi_rn=phi_rn, utils=u, util=max(u.values()), gov=max(u, key=u.get),
                weld=weld, w_req=w_req, clear=e1 - weld, bolt_len=bolt_length(2 * tp, db, 2))


def loose_diagonal(diag, chord_t, chord_b, P, F_tc, F_bc, db=20, tp=10, n=2, e_=40.0, s_=60.0, hw=35.0):
    """site-bolted diagonal: knife plate PL tp x 2hw slotted into the CHS end and lapped on a gusset plate welded
    to the chord (DG24 5.3, Ex 5.2). P = max |force|; F_tc / F_bc = most compressive chord forces at the two
    nodes (Qf of the plate-on-chord check). Bolts J3.6 (threads included), bearing / tear-out J3.10, knife plate
    J4, tube net section (slot tp + 2) D3 with U = 1 (lw >= 1.3D), tube wall shear at the slot welds J4.2,
    weld J2, gusset on the chord K2-1 (longitudinal plate, Table K2.1) on both chords"""
    ab = math.pi * db ** 2 / 4
    dh = db + 2
    cap = {}
    cap["bolt shear"] = n * 0.75 * 0.45 * BOLT_FU * ab
    lc = min(e_ - dh / 2, s_ - dh)
    cap["bearing / tear-out"] = n * 0.75 * min(1.2 * lc * tp * FU, 2.4 * db * tp * FU)
    ag, an = 2 * hw * tp, min((2 * hw - dh) * tp, 0.85 * 2 * hw * tp)
    cap["knife PL yield"] = 0.9 * FY * ag
    cap["knife PL rupture"] = 0.75 * FU * an
    lw = math.ceil(max(1.3 * diag.D, 100) / 10) * 10                 # weld length into the slot: U = 1
    cap["tube net section"] = 0.75 * FU * (diag.A - 2 * (tp + 2) * diag.td)
    cap["tube wall shear"] = 1.0 * 0.6 * FY * diag.td * 4 * lw
    w = max(j24_min(diag.t), leg_std(1.0 * 0.6 * FY * diag.td / (0.75 * 0.6 * FEXX) * math.sqrt(2)))
    cap["slot welds"] = 0.75 * 0.6 * FEXX * 0.707 * w * 4 * lw
    lp = s_ * (n - 1) + 2 * e_ + 2 * 30                               # gusset length along the chord, raised
    while True:                                                        # in 20s until both chords carry it

        def k2(ch, F):
            return 0.9 * 5.5 * FY * ch.td ** 2 * (1 + 0.25 * lp / ch.D) * qf(ch, F, 0.0) / math.sin(math.radians(45))
        if P <= 0.95 * min(k2(chord_b, F_bc), k2(chord_t, F_tc)) or lp >= 400:
            break
        lp += 20
    cap["gusset on B1"] = k2(chord_b, F_bc)                             # K2-1: longitudinal plate, Rn sin theta
    cap["gusset on T1"] = k2(chord_t, F_tc)
    ut = {k: P / v for k, v in cap.items()}
    return dict(P=P, n=n, db=db, tp=tp, lp=lp, lw=lw, w=w, e=e_, s=s_, hw=hw, slot=tp + 2, caps=cap, utils=ut,
                util=max(ut.values()), gov=max(ut, key=ut.get), bolt_len=bolt_length(2 * tp, db, 1))


# --------------------------------------------------------------------------- fly braces
# equal angles (JIS G 3192 / TIS 1227): (leg, t): area mm2, r_z (minor) mm, kg/m
ANGLES = {(50, 5): (480, 9.8, 3.77), (60, 5): (582, 11.7, 4.57), (65, 6): (753, 12.7, 5.91),
          (75, 6): (873, 14.6, 6.85), (90, 8): (1390, 17.6, 10.9)}
FB_F = 45.0                        # brace angle to the purlin, deg (Beca SE-1505: 35 - 55 deg at the lap end, else 45)
FB_LUG = 55.0                      # lug hole below the chord soffit, mm (the brace heel clears the chord)
FB_HOLE_X = 45.0                   # lug holes either side of the truss plane, mm
PURLIN_GAP = 20.0                  # purlin underside above the top of the top chord, mm
FB_PB = 45.0                       # first purlin-web bolt above the purlin underside, mm
FB_PITCH, FB_EDGE = 50.0, 30.0     # bolt pitch and end distance along the brace, mm
SLENDER_MAX = 200.0                # KL/r of a compression brace (AISC 360-16 E2 user note)


def fly_brace(Pr, Lbr, D, H_, db=16):
    """fly brace from a lug under the bottom chord to the purlin web (both sides of the truss), AISC 360-16
    Appendix 6.2 nodal bracing of the compression chord: strength Prb = 0.01 Pr, stiffness
    beta = (1 / 0.75) 8 Pr / Lbr; the brace is a pin-ended single angle, KL = L about z, KL/r <= 200, single-angle
    compression E5 simplified to E3 on r_z (conservative). Geometry: gauge line at FB_F through the lug hole."""
    th = math.radians(FB_F)
    y_h = -D / 2 - FB_LUG                                    # lug hole
    y_p = H_ + D / 2 + PURLIN_GAP + FB_PB                     # first purlin bolt
    run = (y_p - y_h) / math.tan(th)
    Lg = (y_p - y_h) / math.sin(th)                           # lug hole to first purlin bolt
    length = Lg + FB_PITCH + 2 * FB_EDGE
    prb = 0.01 * Pr
    P = prb / math.cos(th)                                    # axial force in the brace for a horizontal Prb
    beta_req = 1 / 0.75 * 8 * Pr / Lbr
    for (b, t), (A, rz, kgm) in sorted(ANGLES.items(), key=lambda kv: kv[1][2]):
        lam = Lg / rz
        if lam > SLENDER_MAX:
            continue
        Fe = math.pi ** 2 * E / lam ** 2
        Fcr = 0.658 ** (FY / Fe) * FY if FY / Fe <= 2.25 else 0.877 * Fe
        phi_pn = 0.9 * Fcr * A
        beta = E * A / Lg * math.cos(th) ** 2                  # horizontal stiffness of one brace
        if phi_pn >= P and beta >= beta_req:
            ab = math.pi * db ** 2 / 4
            return dict(b=b, t=t, A=A, rz=rz, kgm=kgm, name=f"L {b} x {b} x {t}", F=FB_F, y_h=y_h, y_p=y_p,
                        run=run, Lg=Lg, length=length, lam=lam, P=P, prb=prb, phi_pn=phi_pn, beta=beta,
                        beta_req=beta_req, util=max(P / phi_pn, beta_req / beta), db=db,
                        bolt=0.75 * 0.45 * BOLT_FU * ab, gauge=round(0.55 * b / 5) * 5)
    raise RuntimeError("no angle meets KL/r <= 200")


ROD_HOLE = 33                      # anchor rod holes, M20 (AISC Manual Table 14-2, 3/4 in rod: 1 5/16 in)
ROD_WASHER = 8                     # plate washers, mm thick


def support(R_down, R_up, move, n_rod=4, d_rod=20, B=220, N=220, ts=12):
    """bearing: base plate B x N on the RC top, stiffener plate ts under the chord, n_rod anchor rods with oversized
    holes and plate washers (DSC 7: setting tolerance; DG1). move = horizontal movement to take at the sliding end
    each way (thermal + bottom-chord stretch), mm"""
    A1 = B * N
    bearing = 0.65 * 0.85 * FC * A1
    l = (B - ts) / 2                                                   # plate cantilever from the stiffener
    fp = R_down / A1
    tp = max(16, math.ceil(l * math.sqrt(2 * fp / (0.9 * FY)) / 2) * 2)
    ab = math.pi * d_rod ** 2 / 4
    rod = 0.75 * 0.75 * ROD_FU * ab
    slot_len = int(math.ceil((ROD_HOLE + 2 * move) / 5) * 5)
    washer = int(max(50, math.ceil((slot_len + 20) / 10) * 10))         # covers the slot in every rod position
    return dict(B=B, N=N, tp=tp, ts=ts, n_rod=n_rod, d_rod=d_rod, hole=ROD_HOLE, slot=slot_len, washer=washer,
                washer_t=ROD_WASHER, bearing_util=R_down / bearing, rod_util=R_up / n_rod / rod if R_up > 0 else 0.0,
                move=move)


def l_end_req(chord, b):
    """Table K3.1A: chord end distance from the near side of the branch, >= D (1.25 - beta / 2)"""
    return chord.D * (1.25 - b.D / chord.D / 2)


# --------------------------------------------------------------------------- design
THERMAL = 1.2e-5 * 30 * L / 2      # +- movement for a 30 C range, mm


def design():
    sec = size()
    nodes, mem, cases, unit, res, sw = analyse(sec)
    jt = joints(sec, nodes, mem, res)
    mu = member_checks(sec, nodes, mem, res, jt)
    env = {m: (max(f[m] for f, _ in res.values()), min(f[m] for f, _ in res.values())) for m, *_ in mem}
    reac = {n: (max(r[n][1] for _, r in res.values()), min(r[n][1] for _, r in res.values())) for n in ("B0", f"B{NP}")}
    ecc, gaps, th = layout(sec, nodes, mem)
    # splices: chord forces in the splice panels; design tension >= 25 % of the chord yield strength
    spl = {}                       # one flange plate for every splice: designed for the largest tension
    tu = max(max(max(env[f"{g}{p}"][0], 0.0), 0.25 * phi_pt(sec[g])) for g in ("TC", "BC") for p in SPLICE_PANELS)
    for p in SPLICE_PANELS:
        for g in ("TC", "BC"):
            t_max = max(env[f"{g}{p}"][0], 0.0)
            c_max = -min(env[f"{g}{p}"][1], 0.0)
            spl[(g, p)] = dict(T=t_max, C=c_max, flange=flange_splice(sec[g], tu))
    loose = {}
    for p in SPLICE_PANELS:
        _, _, i, j = next(m for m in mem if m[0] == f"D{p}")
        top, bot = (i, j) if i[0] == "T" else (j, i)
        f_c = lambda nd: min(min(env[m[0]][1] for m in mem if m[1] in ("TC", "BC") and nd in (m[2], m[3])), 0.0)
        loose[p] = loose_diagonal(sec[mem_group(mem, f"D{p}")], sec["TC"], sec["BC"],
                                  max(abs(env[f"D{p}"][0]), abs(env[f"D{p}"][1])), f_c(top), f_c(bot))
    # sliding end: thermal + bottom-chord stretch under D + Lr (the roller node moves outward)
    stretch = abs(unit["D"][2][f"B{NP}"][0] + unit["Lr"][2][f"B{NP}"][0])
    sup = support(max(r[0] for r in reac.values()), max(-r[1] for r in reac.values()), THERMAL + stretch)
    sup.update(thermal=THERMAL, stretch=stretch)
    # chord end distance (Table K3.1A) at the end nodes: the chords run X_OH past the node centre lines
    l_end = max(l_end_req(sec[c], sec["VE"]) for c in ("TC", "BC"))
    x_oh = math.ceil((sec["VE"].D / 2 + l_end) / 10) * 10
    # branch welds, AWS D1.1 Fig 9.10 zones, by group (the flattest member of the group)
    welds = {}
    for g in ("DE", "DM", "VE", "VM"):
        th_g = min(th[m[0]] for m in mem if m[1] == g)
        welds[g] = branch_weld(sec[g], sec["TC"], th_g)
    # service deflection at midspan (unfactored) and camber (parabolic, measured with the truss unloaded)
    mid = f"B{NP // 2}"
    dD = -unit["D"][2][mid][1]
    dL = -unit["Lr"][2][mid][1]
    camber = math.ceil(dD / CAMBER_ROUND) * CAMBER_ROUND
    cam_y = [camber * 4 * (k * A_P) * (L - k * A_P) / L ** 2 for k in range(NP + 1)]
    # fly braces: nodal bracing of the bottom chord against its largest compression (wind uplift)
    pr_bc = -min(env[m[0]][1] for m in mem if m[1] == "BC")
    lbr = max(b - a for a, b in zip(BC_BRACE, BC_BRACE[1:])) * A_P
    fly = fly_brace(pr_bc, lbr, sec["BC"].D, H)
    fly.update(Pr=pr_bc, Lbr=lbr)
    return dict(sec=sec, nodes=nodes, mem=mem, res=res, env=env, joints=jt, members=mu, reac=reac, sw=sw,
                splices=spl, loose=loose, support=sup, defl=(dD, dL), cases=cases, camber=camber, camber_y=cam_y,
                welds=welds, x_oh=x_oh, l_end=l_end, fly=fly)


def mem_group(mem, name):
    return next(g for n, g, *_ in mem if n == name)


# --------------------------------------------------------------------------- report
def report(d):
    sec, nodes, mem = d["sec"], d["nodes"], d["mem"]
    kN = 1e-3
    print("STEEL ROOF TRUSS T1 - PRATT, CHS JIS G 3444 STK400 - PRELIMINARY DESIGN (AISC 360-16 LRFD)")
    print(f"span {L / 1000:.2f} m, depth {H / 1000:.2f} m c/c chords, {NP} panels @ {A_P / 1000:.2f} m, "
          f"trusses @ {S_TRUSS:.1f} m; Fy {FY:.0f} / Fu {FU:.0f} MPa, design wall 0.93 t (B4.2)")
    print("\n--- LOADS (kPa on plan; nodal on the top chord, end nodes half) ---")
    print(f"SDL {Q_SDL:.2f} (sheet 0.05 + purlins 0.10 + services 0.15); Lr {Q_LR:.2f} (MR No. 6, 50 kg/m2); "
          f"W net uplift {Q_W:.2f} ASSUMED - verify per DPT 1311")
    print(f"self-weight x {SW_EXTRA:.2f} = {d['sw'] * kN:.1f} kN ({d['sw'] / 9.81:.0f} kg) per truss")
    print("combinations (ASCE 7-16 2.3.1): " + ", ".join(COMBOS) + " - '(half)' = Lr on the left half only")
    print("\n--- SECTIONS ---")
    print(f"{'group':4s} {'section':16s} {'kg/m':>6s} {'D/t':>5s} {'Db/D':>5s}  max T (kN)   max C (kN)   util  governing")
    for g, desc in GROUPS.items():
        ms = [m for m in mem if m[1] == g]
        t = max(d["env"][m[0]][0] for m in ms)
        c = min(d["env"][m[0]][1] for m in ms)
        gov = max(ms, key=lambda m: d["members"][m[0]])
        print(f"{g:4s} {sec[g].name:16s} {sec[g].kgm:6.2f} {sec[g].D / sec[g].td:5.1f} {sec[g].D / sec['TC'].D:5.2f}  "
              f"{t * kN:9.1f}  {c * kN:11.1f}  {d['members'][gov[0]]:5.2f}  {gov[0]}   {desc}")
    print("unbraced lengths: top chord 1.25 m (purlin + roof bracing at every node); bottom chord 1.25 m in plane, "
          f"{4 * A_P / 1000:.1f} m out of plane (fly braces at nodes {', '.join(map(str, BC_BRACE))}); webs full "
          f"length; K = {K_CHORD} chords, {K_WEB} webs (DG24 8.4)")
    print("\n--- JOINTS (Table K3.1: gap K, X / T-Y chord plastification, shear yielding; limits Table K3.1A; "
          "unbalanced nodes K + X / Y, DG24 8.2) ---")
    worst = sorted(d["joints"].items(), key=lambda kv: -kv[1]["util"])
    for n, j in worst[:8]:
        b = " + ".join(f"{x['name']} {x['sec'].D:g}@{x['th']:.0f}" for x in j["branches"])
        gp = "/".join(f"{g:.0f}" for g in j["gaps"]) or "-"
        print(f"{n:4s} {b:34s} gap {gp:>9s}  e {j['e']:+6.1f} (e/D {j['e'] / sec['TC' if n[0] == 'T' else 'BC'].D:+.2f})"
              f"  util {j['util']:.2f}  {'; '.join(j['msgs']) or 'limits OK'}")
    print(f"... {len(d['joints'])} joints, max util {worst[0][1]['util']:.2f}")
    print(f"chord end distance (K3.1A) >= {d['l_end']:.0f} mm from the near face of V1 -> chords run {d['x_oh']:.0f} "
          "past the end node centre lines")
    print("\n--- BRANCH WELDS (AWS D1.1:2015 Fig 9.10, column E = t; wall needs E = "
          f"{throat_wall(1.0):.2f} t; E49XX, no directional increase) ---")
    for g, w in d["welds"].items():
        z = ", ".join(f"{k} {v}" for k, v in w["legs"].items())
        print(f"{g}: {sec[g].name}  Psi {w['psi'][0]:.0f} - {w['psi'][1]:.0f} deg  legs {z}"
              + ("  (toe: branch edge bevelled)" if w["bevel"] else ""))
    print(f"heel legs include the Z loss {Z_LOSS:.0f} mm (AWS Table 9.5, 45 <= Psi < 60)")
    print("\n--- FIELD SPLICES (bolted circular flange plates, DG24 5.4) ---")
    for (g, p), s in d["splices"].items():
        f = s["flange"]
        print(f"{g} panel {p + 1}: T {s['T'] * kN:6.1f} C {s['C'] * kN:6.1f} kN -> PL {f['tp']} (needs {f['tp_req']:.1f}) "
              f"OD {f['od']:.0f}, {f['n']}-M{f['db']}x{f['bolt_len']} 8.8 on PCD {f['bc']:.0f}, bolt "
              f"{f['per_bolt'] * kN:.1f}/{f['phi_rn'] * kN:.1f} kN; util plate {f['utils']['plate']:.2f}, bolts "
              f"{f['utils']['bolts']:.2f}; weld {f['weld']} (Eq 5-7 {f['w_req']:.1f}), {f['clear']:.0f} clear to the bolt")
    print("design tension >= 25 % of the chord yield strength (minimum splice capacity); compression by contact")
    for p, c in d["loose"].items():
        print(f"loose diagonal D{p} (panel {p + 1}): P {c['P'] * kN:.1f} kN -> {c['n']}-M{c['db']}x{c['bolt_len']} 8.8 "
              f"single shear, knife PL {c['tp']} x {2 * c['hw']:.0f}, gusset {c['lp']:.0f} long, slot {c['slot']} x "
              f"{c['lw'] + 5}, slot welds {c['w']} x {c['lw']} (4 lines); util {c['util']:.2f} ({c['gov']})")
        print("    " + "; ".join(f"{k} {v:.2f}" for k, v in c["utils"].items()))
    f = d["fly"]
    print(f"fly braces FB1 (AISC 360-16 App. 6.2 nodal, bottom chord Pr {f['Pr'] * kN:.0f} kN, Lbr {f['Lbr']:.0f}): "
          f"{f['name']}, F {f['F']:.0f} deg, L {f['Lg']:.0f} (hole to hole) KL/rz {f['lam']:.0f} <= {SLENDER_MAX:.0f}; "
          f"P {f['P'] * kN:.2f} / {f['phi_pn'] * kN:.1f} kN, stiffness {f['beta'] / 1000:.1f} >= {f['beta_req'] / 1000:.2f} kN/mm")
    print("\n--- SUPPORTS (bottom chord bearing; pin at B0, slotted at B20) ---")
    for n, (rd, ru) in d["reac"].items():
        print(f"{n}: max down {rd * kN:.1f} kN, max uplift {max(-ru, 0) * kN:.1f} kN")
    s = d["support"]
    print(f"base PL {s['B']}x{s['N']}x{s['tp']}, stiffener PL {s['ts']}, {s['n_rod']}-M{s['d_rod']} SS400 rods in "
          f"{s['hole']} holes, plate washers {s['washer']}x{s['washer']}x{s['washer_t']}; bearing util "
          f"{s['bearing_util']:.2f}, rod tension util {s['rod_util']:.2f}")
    print(f"sliding end: thermal +-{s['thermal']:.1f} + bottom-chord stretch (D + Lr) {s['stretch']:.1f} = "
          f"+-{s['move']:.1f} mm -> slots {s['hole']} x {s['slot']}")
    print("anchorage into the RC (ACI 318 Ch. 17 breakout / pull-out) by the RC designer")
    dD, dL = d["defl"]
    print("\n--- SERVICE DEFLECTION AT MIDSPAN (pin-jointed, unfactored) ---")
    print(f"D {dD:.1f} mm, Lr {dL:.1f} mm, D + Lr {dD + dL:.1f} mm = L/{L / (dD + dL):.0f} (limit L/240); "
          f"Lr alone L/{L / dL:.0f} (limit L/360); camber {d['camber']:.0f} mm at midspan (= D)")
    print("camber ordinates, panel points 0 - 10: " + ", ".join(f"{y:.0f}" for y in d["camber_y"][:NP // 2 + 1]))
    w = weight(sec, nodes, mem)
    print(f"\nsteel weight: members {w:.0f} kg, with connections ({SW_EXTRA:.2f}) about {w * SW_EXTRA:.0f} kg per truss")


if __name__ == "__main__":
    report(design())
