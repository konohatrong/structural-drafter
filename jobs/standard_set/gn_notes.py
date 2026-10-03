"""
General notes - structural concrete, STR-ST-1001 ... (office master) - model-space sheets built from blocks.

Content : GENERAL_NOTES_STRUCTURAL_CONCRETE.md (EIT 011014-19 materials & construction, ACI 318-19 / ACI 301 refs).
Source  : jobs/general_notes/build_gn.py (Rev A, frozen in jobs/general_notes/rev_A) - notes, tables and details
          unchanged; engine = td_engine.py (title-block block, model-space sheets).
Sheets  : the notes flow column by column over as many A3 sheets as they need (1001, 1002, ...); the typical
          details band sits on the last sheet under columns 2 .. NCOL.
Blocks  : NOTES-100x-1 (the note columns of one sheet with their tables), HDR-100x-1 (details band heading),
          DET-100x-COVER / -HOOKS / -LAPS (details drawn at paper size, insert scale 1), x = last sheet.
Rule    : normal drawing rule, K = 1 (2026-09-29, user: text 2.0 mm, headers x 1.4 = 2.8 mm). Rev A (frozen in
          jobs/general_notes/rev_A) used K = 1.25/2.00 on one sheet. Guide: MODEL_SPACE_SHEETS.md sec. 6
"""
import td_engine
from td_engine import *

BASE = "STR-ST-1001_General_Notes_Concrete_A3_RevB"
SHEETS[:] = []              # set by build(): one entry per sheet the notes need
td_engine.KEYPLAN_2 = "(GENERAL NOTES)"
# Rev A (jobs/general_notes/rev_A): one sheet, text 1.25 / 1.75. Rev B: normal text 2.0 / 2.8, two sheets.
PROJ["rev"] = "B"
REV_A_DATE = "29/09/2026"      # revision rows are set in build(), once the number of sheets is known

# Project design data (note 2.5) - fill in per project; "[ ... ]" = to be completed
DESIGN_DATA = [
    ("LOCATION", "[ PROVINCE / DISTRICT ]"),
    ("SEISMIC ZONE", "[ ZONE ] (MINISTERIAL REGULATION)"),
    ("SEISMIC IMPORTANCE FACTOR Ie", "[ 1.0 / 1.25 / 1.5 ]"),
    ("SEISMIC DESIGN CATEGORY", "[ B / C / D ]"),
    ("SEISMIC-RESISTING SYSTEM, X-DIR.", "[ SYSTEM ]; R = [ ], Ω0 = [ ], Cd = [ ]"),
    ("SEISMIC-RESISTING SYSTEM, Y-DIR.", "[ SYSTEM ]; R = [ ], Ω0 = [ ], Cd = [ ]"),
    ("SITE CLASS; SDS, SD1", "[ ]; SDS = [ ] g, SD1 = [ ] g"),
    ("SEISMIC ANALYSIS", "[ EQUIVALENT STATIC / RESPONSE SPECTRUM ]"),
    ("MEMBERS OF THE SEISMIC SYSTEM", "[ FRAMES / WALLS ON GRIDS ... ]"),
    ("DESIGN WIND SPEED", "V = [ ] m/s, WIND ZONE [ ]"),
    ("WIND RETURN PERIOD, ULTIMATE DESIGN", "[ ] YEARS"),
    ("LIVE LOADS (kg/m²)", "[ USE: ... ] (MINISTERIAL REGULATION); ROOF [ ]"),
    ("SUPERIMPOSED DEAD LOAD (kg/m²)", "FINISHES [ ], SERVICES [ ], PARTITIONS [ ]"),
    ("LIVE-LOAD REDUCTION; SPECIAL LOADS", "[ USED / NOT USED ]; [ EQUIPMENT, TANKS ... ]"),
]



# ======================================================================= GENERAL NOTES - layout engine
# Every line of text is placed as its own TEXT entity at a measured position, so the plotted sheet
# matches the layout exactly (no MTEXT re-wrapping in AutoCAD).
# Every annotation size = general drawing rule x K. K = 1 since 2026-09-29 (Rev A used 1.25 / 2.00).
# NOT scaled: sheet frame, zone grid, title strip (set-wide furniture) and pen weights (plot pens).
K = 1.0
TB = TXT_H * K               # 2.0   body text              (rule 2.0)
TH = 2.8 * K                 # 2.8   headers, bold          (rule 2.8 = 1.4 x body)
LP = PITCH * K               # 3.33  body line pitch        (rule 3.33 = 5/3 x text)
TLP = LP                     # 3.33  extra line in a wrapped table cell
TRH = 5.2 * K                # 5.2   single-line table row  (rule 5.2)
HP = TH + 2.0 * K            # 4.8   header + gap below     (rule 2.0)
PG = NGAP * K                # 1.6   gap after a note       (rule 1.6)
SG = 3.0 * K                 # 3.0   gap before a header    (rule 3.0)
NCOL = 3
CGAP = 8.0 * K               # 8.0   column gap             (rule 8.0)
CX0, CX1 = FX0 + 3.5, TBX - 3.5
COLW = (CX1 - CX0 - (NCOL - 1) * CGAP) / NCOL
CY1 = FY1 - 3.5
IND = 8.0 * K                # 8.0   hanging indent for note numbers ("12.10")  (rule 8.0)
CPAD = 1.2 * K               # 1.2   text inset in a table cell (rule 1.2)

_gds = doc.dimstyles.get(DS[1]).dxf  # dimensions on this sheet: rule dimstyle x K
_gds.dimtxt, _gds.dimasz, _gds.dimexe = 2.0 * K, 2.0 * K, 2.0 * K        # text / arrow / extension
_gds.dimexo, _gds.dimgap, _gds.dimdli = 1.0 * K, 0.6 * K, 5.0 * K        # offset / gap / baseline step


def wrap_s(s, h, width, style="AN"):
    out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if cur and text_w(t, h, style) > width:
            out.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out or [""]


class Flow:
    """sequential column flow over sheets: running column c = sheet c // NCOL, column c % NCOL.
    draw=False only measures; page = draw only that sheet's columns (the flow itself always runs whole,
    so every sheet breaks at the same place)."""
    def __init__(self, ps, bottom, draw=True, page=None):
        """bottom: function of the running column index -> bottom line of that column"""
        self.ps, self.draw, self.bottom, self.page = ps, draw, bottom, page
        self.col, self.y = 0, CY1
        self.tables = []                                    # (title, sheet index)
        self.pending = None                                 # header waiting for the item it belongs to
        self.tn = 0                                         # tables numbered in flow order: TABLE 1, 2 ...

    @property
    def on(self):
        return self.draw and (self.page is None or self.col // NCOL == self.page)

    @property
    def x(self):
        return CX0 + (self.col % NCOL) * (COLW + CGAP)

    def need(self, h):
        if self.y - h < self.bottom(self.col) and self.y < CY1 - 0.01:
            self.col += 1
            self.y = CY1

    def gap(self, g):
        if self.y < CY1 - 0.01:
            self.y -= g

    def header(self, s):
        """keep with next: the header is placed by the next item, in the column where that item starts"""
        self.pending = s

    def _head(self, h):
        """place a pending header where the following h (its first lines / whole table / figure) also fits"""
        if self.pending is None:
            return
        self.gap(SG)
        self.need(HP + h)
        if self.on:
            text(self.ps, self.pending, (self.x, self.y - TH), TH, "S-TEXT", style="ANB")
        self.y -= HP
        self.pending = None

    def para(self, num, body, level=0):
        x_num = self.x + level * IND
        lines = wrap_s(body, TB, COLW - (level + 1) * IND)
        self._head(min(2, len(lines)) * LP)
        self.need(min(2, len(lines)) * LP)                  # no single orphan line at a column foot
        for k, ln in enumerate(lines):
            self.need(LP)
            if self.on:
                if k == 0 and num:
                    text(self.ps, num, (self.x + level * IND, self.y - TB), TB, "S-TEXT")
                text(self.ps, ln, (self.x + (level + 1) * IND, self.y - TB), TB, "S-TEXT")
            self.y -= LP
        self.y -= PG

    def table(self, title, widths, heads, rows, note=None, align=None):
        """widths in fractions of the column width; cells wrap; first row = heads (bold).
        align: one letter per column, "L" = middle-left, "C" = middle-centre (numbers, sizes, values).
        Every cell is centred vertically on its row (AutoCAD MIDDLE alignment = middle of the cap height);
        a wrapped cell is centred as a block."""
        ws = [f * COLW for f in widths]
        align = (align or "L" * len(ws)).upper()
        allrows = [heads] + rows
        cells = [[wrap_s(c, TB, w - 1.4, "ANB" if r == 0 else "AN") for c, w in zip(row, ws)]
                 for r, row in enumerate(allrows)]
        rhs = [TRH + (max(len(c) for c in row) - 1) * TLP for row in cells]
        nl = wrap_s(note, TB, COLW) if note else []
        tot = LP + 0.6 * K + sum(rhs) + len(nl) * LP + 1.6 * K + (PG if nl else 0.0)
        self._head(PG + tot)
        self.gap(PG)
        self.need(tot)
        self.tn += 1
        name, title = title, f"TABLE {self.tn} - {title}"
        self.tables.append((self.tn, name, self.col // NCOL))
        if text_w(title, TB, "ANB") > COLW:
            print(f"  !! table title wider than the column: {title}")
        if self.on:
            ps, x0 = self.ps, self.x
            text(ps, title, (x0, self.y - TB), TB, "S-TEXT", style="ANB")
            yt = self.y - LP - 0.6 * K
            xs = [x0]
            for w in ws:
                xs.append(xs[-1] + w)
            y = yt
            for r, (row, rh) in enumerate(zip(cells, rhs)):
                line(ps, (xs[0], y), (xs[-1], y), "S-TTLB" if r <= 1 else "S-TTLB-THIN")
                ym = y - rh / 2                                     # row centre line
                for c, (cl, cx) in enumerate(zip(row, xs)):
                    centre = align[c] == "C"
                    tx = cx + ws[c] / 2 if centre else cx + CPAD
                    for k, ln in enumerate(cl):
                        ty = ym + ((len(cl) - 1) / 2 - k) * TLP
                        text(ps, ln, (tx, ty), TB, "S-TEXT", TA.MIDDLE_CENTER if centre else TA.MIDDLE_LEFT,
                             style="ANB" if r == 0 else "AN")
                y -= rh
            line(ps, (xs[0], y), (xs[-1], y), "S-TTLB")
            for cx in xs:
                line(ps, (cx, yt), (cx, y), "S-TTLB-THIN")
            for k, ln in enumerate(nl):
                text(ps, ln, (x0, y - 1.6 * K - TB - k * LP), TB, "S-TEXT")
        self.y -= tot

    def terms(self, rows, tw=22.0 * K, title=None):
        """definition list in the column: term at the column edge, meaning beside it (wrapped); one per line.
        title: bold sub-title (body size), kept with the first row"""
        if title:
            first = len(wrap_s(rows[0][1], TB, COLW - tw)) * LP
            self._head(LP + first)
            self.gap(PG)
            self.need(LP + first)
            if self.on:
                text(self.ps, title, (self.x, self.y - TB), TB, "S-TEXT", style="ANB")
            self.y -= LP
        for term, meaning in rows:
            lines = wrap_s(meaning, TB, COLW - tw)
            self._head(len(lines) * LP)
            self.need(len(lines) * LP)
            if self.on:
                text(self.ps, term, (self.x, self.y - TB), TB, "S-TEXT", style="ANB")
                for k, ln in enumerate(lines):
                    text(self.ps, ln, (self.x + tw, self.y - TB - k * LP), TB, "S-TEXT")
            self.y -= len(lines) * LP
        self.y -= PG

    def detail(self, fn):
        """typical detail as a column-width figure: its edges on the note-column grid. Placed like a table
        (whole, header kept with it); drawn later as its own block DET-<sheet>-<tag> (see build)."""
        h = detail_h(fn)
        self._head(DET_GAP + h)
        self.gap(DET_GAP)
        self.need(h)
        if self.on:
            FIGS.append((self.col // NCOL, fn, self.x, self.y))
        self.y -= h

    def figure(self, h, fn):
        self._head(PG + h)
        self.gap(PG)
        self.need(h)
        if self.on:
            fn(self.ps, self.x, self.y)
        self.y -= h


# ======================================================================= GENERAL NOTES - data
# Design standard: EIT 011008-21 (based on ACI 318-11). Materials & construction: EIT 011014-19.
FC_LAP = 23.5                # MPa (240 ksc) - basis of the lap / anchorage table
FY_LAP = 390.0               # SD40


def rup(v, step=50):
    return int(math.ceil(v / step - 1e-9) * step)


def ld_simple(db, top=False):
    """EIT 011008 12.2.2 simplified ld (clear cover >= db and clear spacing >= 2 db, or cover >= db, spacing >= db
    with minimum stirrups): fy psi_t psi_e / (2.1 lambda sqrt f'c) db for bars <= 20 mm, 1.7 for >= 22 mm;
    uncoated (psi_e = 1), normalweight (lambda = 1), psi_t = 1.3 for top bars; ld >= 300"""
    k = 2.1 if db <= 20 else 1.7
    return max(300.0, FY_LAP * (1.3 if top else 1.0) / (k * math.sqrt(FC_LAP)) * db)


def lap_len(db, top=False):
    """class B tension lap = 1.3 ld >= 300 (EIT 011008 12.14.1), rounded up to 50"""
    return max(300, rup(1.3 * ld_simple(db, top)))


def lap_comp(db):
    """compression lap 0.071 fy db >= 300 (fy <= 420 MPa) (EIT 011008 12.15.1), rounded up to 50"""
    return max(300, rup(0.071 * FY_LAP * db))


def ldc(db):
    """compression development 0.24 fy / (lambda sqrt f'c) db >= 0.043 fy db >= 200 (EIT 011008 12.3.2), up to 50"""
    return rup(max(0.24 * FY_LAP / math.sqrt(FC_LAP) * db, 0.043 * FY_LAP * db, 200))


def ldh(db):
    """standard-hook development fy / (4.2 lambda sqrt f'c) db >= 8 db >= 150 (EIT 011008 12.5.2), up to 50"""
    return rup(max(FY_LAP / (4.2 * math.sqrt(FC_LAP)) * db, 8 * db, 150))


def cov(c0, alpha):
    a = 1.0 if c0 <= 20 else alpha
    return int(math.ceil(a * c0 / 5.0 - 1e-9) * 5)


LAP_DB = [10, 12, 16, 20, 25, 28, 32]
# cover by structural element - EIT 011008-21 7.7.1 (cast in place): (element, condition, <= DB16, >= DB20)
COVER_ELEM = [
    ("FOOTINGS, PILE CAPS", "CAST AGAINST EARTH (BOTTOM, SIDES)", "75", "75"),
    ("FOOTINGS, PILE CAPS", "FORMED FACES IN CONTACT WITH EARTH", "40", "50"),
    ("GROUND BEAMS, SUSPENDED GROUND SLABS", "IN CONTACT WITH EARTH", "40", "50"),
    ("COLUMNS, BEAMS", "INTERIOR (TO TIES / STIRRUPS)", "40", "40"),
    ("COLUMNS, BEAMS", "EXPOSED TO WEATHER", "40", "50"),
    ("SLABS, JOISTS, STAIRS", "INTERIOR", "20", "30"),
    ("SLABS, ROOF DECKS, CANOPIES", "EXPOSED TO WEATHER", "40", "50"),
    ("WALLS", "INTERIOR", "20", "30"),
    ("RETAINING, BASEMENT WALLS, TANKS", "EARTH OR WEATHER FACE", "40", "50"),
    ("SHELLS, FOLDED PLATES", "INTERIOR", "15", "20"),
]
# recommendation - exposure based, EIT 011014-19 2.5.1.5 (T2.23 corrosion risk) with alpha by f'c
COVER_ENV = [("CORROSION RISK: SLABS, WALLS", 50), ("CORROSION RISK: OTHER MEMBERS", 65)]


def content(f):
    H, P, T = f.header, f.para, f.table
    E8, E14 = "EIT 011008", "EIT 011014"          # citation prefixes: design / materials & construction

    H("1. GENERAL")
    P("1.1", "THESE NOTES APPLY TO ALL STRUCTURAL CONCRETE WORK UNLESS NOTED OTHERWISE (U.N.O.) ON THE DRAWINGS. "
             "READ WITH THE ARCHITECTURAL AND MEP DRAWINGS AND THE SPECIFICATION. WHERE DOCUMENTS DIFFER, THE MORE "
             "STRINGENT REQUIREMENT GOVERNS; REFER ANY DISCREPANCY TO THE ENGINEER BEFORE PROCEEDING.")
    P("1.2", "DIMENSIONS ARE IN MILLIMETRES AND LEVELS IN METRES U.N.O. DO NOT SCALE FROM THE DRAWINGS.")
    P("1.3", f"THE WORK SHALL BE INSPECTED THROUGHOUT BY A LICENSED CIVIL ENGINEER (SUPERVISING ENGINEER) STATIONED "
             f"ON SITE; DUCTILE MOMENT FRAMES DESIGNED FOR EARTHQUAKE REQUIRE CONTINUOUS INSPECTION OF REINFORCEMENT "
             f"AND CONCRETING. [{E8} 1.3.1, 1.3.5; {E14} 1.2.3]")
    P("1.4", f"BEFORE WORK STARTS THE CONTRACTOR SHALL SUBMIT FOR APPROVAL: CONSTRUCTION PLAN AND POUR SEQUENCE; "
             f"CONCRETE MIX DESIGNS WITH TRIAL-MIX RESULTS; MATERIAL CERTIFICATES; FORMWORK AND SHORING DESIGN; BAR "
             f"BENDING SCHEDULES. [{E14} 1.2.4, 3.1, 10.3]")
    P("1.5", f"NO OPENING, SLEEVE, CHASE OR EMBEDDED ITEM NOT SHOWN ON THE STRUCTURAL DRAWINGS SHALL BE MADE WITHOUT "
             f"THE ENGINEER'S APPROVAL. [{E8} 6.3.1]")

    H("2. DESIGN BASIS AND STANDARDS")
    P("2.1", f"DESIGN: EIT 011008-21, RC BUILDINGS BY STRENGTH DESIGN (BASED ON ACI 318-11). SEISMIC: DPT 1301/1302-61 "
             f"WHERE REQUIRED BY MINISTERIAL REGULATION. LOADS: MINISTERIAL REGULATIONS UNDER THE BUILDING CONTROL ACT "
             f"B.E. 2522; LIVE LOADS AS SHOWN ON THE DESIGN CRITERIA / FRAMING PLANS. [{E8} 1.1, 1.2.1, 19.1]")
    P("2.2", "MATERIALS AND CONSTRUCTION: EIT 011014-19. DRAFTING: EIT 011006-19. WHERE THESE ARE SILENT: ACI 301 AND "
             "ACI 318.")
    P("2.3", "TIS (CURRENT EDITIONS): 15, 849, 2587, 2594 CEMENTS; 566 AGGREGATES; 733, 874, 985 ADMIXTURES; 2135 "
             "FLY ASH; 213 READY-MIXED CONCRETE; 409 COMPRESSION TEST; 20 ROUND BARS; 24 DEFORMED BARS; 737 WELDED WIRE "
             "FABRIC; 1227 STRUCTURAL STEEL. DPT: 1208 / 1210 CYLINDERS; 1212 MIXING WATER; 1332 DURABILITY.")
    P("2.4", "ACI GUIDES FOR WORKMANSHIP: ACI 117 TOLERANCES; ACI 304 PLACING; ACI 305 HOT WEATHER; ACI 308 "
             "CURING; ACI 309 CONSOLIDATION; ACI 347 FORMWORK.")
    P("2.5", "PROJECT DESIGN DATA: SEE TABLE 1. SEISMIC TO DPT 1301/1302-61 (SYSTEMS, R, Ω0, Cd: TABLE 2.3-1); "
             "WIND TO DPT 1311-50.")
    T("PROJECT DESIGN DATA", [0.46, 0.54], ["ITEM", "VALUE"], [list(r) for r in DESIGN_DATA], align="LL")

    H("3. CONCRETE")
    T("CONCRETE SCHEDULE (U.N.O. ON DRAWINGS)", [0.37, 0.24, 0.12, 0.14, 0.13],
      ["ELEMENT", "f'c CYL. 28 d", "MAX. w/b", "SLUMP cm", "MAX. AGG."],
      [["LEAN CONCRETE 50 THK.", "150 ksc (15 MPa)", "–", "5 – 10", "20"],
       ["FOOTINGS, PILE CAPS, GROUND BEAMS", "240 ksc (23.5 MPa)", "0.50", "5 – 7.5", "25"],
       ["COLUMNS, WALLS", "240 ksc (23.5 MPa)", "0.50", "5 – 12.5", "20"],
       ["BEAMS, SLABS, STAIRS", "240 ksc (23.5 MPa)", "0.50", "5 – 10", "20"],
       ["WATER-RETAINING, ROOF SLABS", "280 ksc (27.5 MPa)", "0.50", "7.5 – 10", "20"],
       ["SEVERE EXPOSURE (CHLORIDE, SEWAGE)", "320 ksc (31.5 MPa)", "0.45", "7.5 – 10", "20"],
       ["CONGESTED REINFORCEMENT", "AS ABOVE", "AS ABOVE", "10 – 15", "20"]],
      note=f"STRUCTURAL CONCRETE f'c ≥ 18 MPa. SLUMP TOLERANCE ±2.5 cm (±3.5 cm ABOVE 15 cm). "
           f"[{E8} 1.1.1; {E14} T1.1, T3.5, T3.6, T5.1]", align="LCCCC")
    P("3.1", f"f'c IS THE SPECIFIED STRENGTH OF STANDARD CYLINDERS Ø150 x 300 AT 28 DAYS, U.N.O. (CUBE ≈ CYLINDER + "
             f"5 MPa FOR 20 – 50 MPa). [{E8} 5.1.3, 5.1.4; {E14} FIG. 3.2]")
    P("3.2", f"CEMENT: PORTLAND CEMENT TYPE I TO TIS 15 U.N.O.; TIS 849, 2587, 2594 ONLY WITH APPROVAL. MIXED CEMENT "
             f"(TIS 80) SHALL NOT BE USED FOR STRUCTURAL CONCRETE. [{E8} 3.2; {E14} 2.1]")
    P("3.3", f"AGGREGATES TO TIS 566: CLEAN, HARD AND DURABLE. SEA SAND ONLY WITH APPROVAL (Cl ≤ 0.02 % OF DRY SAND). "
             f"MAX. SIZE ≤ 1/5 OF THE NARROWEST FORM DIMENSION, 1/3 OF THE SLAB THICKNESS AND 2/3 OF THE CLEAR BAR "
             f"SPACING. [{E8} 3.3; {E14} 2.3]")
    P("3.4", f"WATER: CLEAN, TO DPT 1212. SEA OR BRACKISH WATER SHALL NOT BE USED. [{E8} 3.4; {E14} 2.2]")
    P("3.5", f"ADMIXTURES (TIS 733, 874, 985) AND FLY ASH (TIS 2135) ONLY WITH APPROVAL AND BY TRIAL MIX. CALCIUM "
             f"CHLORIDE OR CHLORIDE ADMIXTURES ARE PROHIBITED IN PRESTRESSED CONCRETE, WITH EMBEDDED ALUMINIUM OR "
             f"AGAINST GALVANIZED FORMS; Cl FROM ADMIXTURES ≤ 0.02 % OF BINDER. [{E8} 3.6; {E14} 2.4]")
    P("3.6", f"MAX. ACID-SOLUBLE CHLORIDE (ASTM C1152), % OF CEMENTITIOUS MATERIAL: RC 0.30; RC EXPOSED TO CHLORIDE "
             f"0.20; RC DRY OR PROTECTED 1.00; PRESTRESSED 0.08. [{E8} T5.6; {E14} T1.2]")
    T("SULFATE EXPOSURE", [0.19, 0.17, 0.17, 0.33, 0.14],
      ["SEVERITY", "SO4 WATER ppm", "SO4 SOIL %", "CEMENT", "MAX. w/cm"],
      [["NORMAL", "< 150", "< 0.1", "NO RESTRICTION", "–"],
       ["MODERATE", "150 – 1,500", "0.1 – 0.2", "TYPE 2 OR 5, OR 1 + POZZOLAN", "0.50"],
       ["SEVERE", "1,500 – 10,000", "0.2 – 2.0", "TYPE 5, OR 1 + POZZOLAN", "0.45"],
       ["VERY SEVERE", "> 10,000", "> 2.0", "TYPE 5 OR 1, WITH POZZOLAN", "0.40"]],
      note=f"MAGNESIUM SULFATE: TYPE 5, NO POZZOLAN REPLACEMENT, PER {E8} T5.5. [{E8} 5.5.1, T5.4]",
      align="LCCLC")
    P("3.7", f"MIX DESIGN BY THE SUPPLIER FOR f'cr ≥ THE LARGER OF f'c + 1.34 ss AND f'c + 2.33 ss − 3.5 MPa (ss FROM "
             f"≥ 30 TESTS, OR 15 – 29 x FACTOR); WITHOUT DATA f'cr = f'c + 7.0 (f'c < 21), f'c + 8.3 (21 – 35), "
             f"1.1 f'c + 5.0 (> 35) MPa. [{E8} 5.3, T5.1, T5.2]")
    P("3.8", f"READY-MIXED CONCRETE TO TIS 213 FROM AN APPROVED PLANT; SITE MIXING IN AN APPROVED MIXER ≥ 1.5 min "
             f"AFTER ALL MATERIALS ARE IN. DELIVERY TICKETS SHALL SHOW PLANT, TICKET AND TRUCK NO., CLASS, VOLUME, "
             f"BATCHING AND DISCHARGE TIMES, SLUMP, MAX. AGGREGATE AND ADMIXTURES. [{E8} 5.8.2; {E14} 5.1, 5.6.5]")
    P("3.9", f"DISCHARGE WITHIN 2 h OF BATCHING (1 h WITHOUT A RETARDER). NO WATER SHALL BE ADDED ON SITE; SLUMP MAY "
             f"BE RESTORED ONLY WITH SUPERPLASTICIZER AND ≥ 30 DRUM REVOLUTIONS. CONCRETE THAT HAS BEGUN TO SET OR IS "
             f"RETEMPERED SHALL NOT BE USED. [{E8} 5.8.4; {E14} 5.3, 5.6.3]")

    H("4. TESTING AND ACCEPTANCE")
    P("4.1", f"SAMPLE AT THE POINT OF PLACING (ASTM C172), PER CLASS: ≥ ONCE PER DAY, PER 50 m³ AND PER 250 m² OF "
             f"SLAB OR WALL; ≥ 5 RANDOM BATCHES WHERE FEWER TESTS RESULT. 1 SET = 3 CYLINDERS (DPT 1208), TESTED TO "
             f"TIS 409 / DPT 1210 AT 28 DAYS; ADD 7-DAY AND FIELD-CURED SETS FOR EARLY STRIPPING OR LOADING. SLUMP "
             f"TEST EVERY SAMPLED TRUCK. [{E8} 5.7.1; {E14} 5.6.4, 12.3]")
    P("4.2", "ACCEPTANCE - ALL OF:")
    P("(a)", f"MEAN OF ANY 3 CONSECUTIVE TESTS ≥ f'c, AND NO TEST BELOW f'c − 3.5 MPa. [{E8} 5.7.2]", 1)
    P("(b)", f"EACH SET MEAN ≥ f'c AND EVERY CYLINDER ≥ 0.85 f'c. [{E14} 5.6.4]", 1)
    P("(c)", f"WITH ≥ 30 RESULTS: MEAN ≥ f'c + 1.65 Sn. [{E14} 12.4]", 1)
    P("4.3", f"FIELD-CURED CYLINDERS BELOW 85 % OF THE COMPANION LAB-CURED STRENGTH (AND NOT ABOVE f'c + 3.5 MPa): "
             f"IMPROVE CURING AND PROTECTION. [{E8} 5.7.3]")
    P("4.4", f"LOW STRENGTH: 3 CORES PER DEFICIENT TEST (DPT 1210); ADEQUATE IF THE CORE MEAN ≥ 0.85 f'c AND NO CORE "
             f"< 0.75 f'c. OTHERWISE LOAD TEST AT ≥ 56 DAYS WITH 0.85 (1.4D + 1.7L) FOR 24 h: ACCEPT IF DEFLECTION ≤ "
             f"lt² / (20,000 h) OR RECOVERY ≥ 75 % IN 24 h. STRENGTHENING OR REMOVAL AT THE CONTRACTOR'S COST. "
             f"[{E8} 5.7.4, 18.3.2, 18.4]")
    P("4.5", f"REPORT RESULTS TO THE ENGINEER IMMEDIATELY; KEEP CONTROL CHARTS. [{E14} 12.2.4, 12.3]")

    H("5. REINFORCEMENT")
    P("5.1", f"DEFORMED BARS (DB) SD40 TO TIS 24, fy ≥ 390 MPa (4,000 ksc). ROUND BARS (RB) SR24 TO TIS 20, fy ≥ 235 "
             f"MPa (2,400 ksc), FOR STIRRUPS, TIES AND SPIRALS ONLY. WELDED WIRE FABRIC TO TIS 737. MILL CERTIFICATE "
             f"AND TENSILE TEST PER DELIVERY AND SIZE. [{E8} 3.5; {E14} 2.5.1.1, 12.2.3]")
    P("5.2", f"STORE UNDER COVER, OFF THE GROUND, BY SIZE AND GRADE. AT CONCRETING BARS SHALL BE FREE OF MUD, OIL AND "
             f"LOOSE RUST; LIGHT RUST OR MILL SCALE IS ACCEPTABLE. [{E8} 7.4; {E14} 2.6.5]")
    P("5.3", f"BEND COLD, BY MACHINE, TO THE APPROVED SCHEDULE. NO HEATING, RE-BENDING OR FIELD BENDING OF BARS "
             f"PARTLY EMBEDDED IN CONCRETE, U.N.O. NO BEND WITHIN 10 db OF A WELD. [{E8} 7.3; {E14} 2.5.1.2]")
    T("HOOKS AND BENDS", [0.36, 0.42, 0.22],
      ["BAR", "STANDARD HOOK", "MIN. INSIDE BEND Ø"],
      [["MAIN BARS DB10 – DB25", "90° + 12 db  /  180° + 4 db ≥ 65", "6 db"],
       ["MAIN BARS DB28 – DB36", "90° + 12 db", "8 db"],
       ["STIRRUPS, TIES RB6 – DB16", "135° + 6 db  (90° + 6 db)", "4 db"],
       ["STIRRUPS, TIES DB20 – DB25", "135° + 6 db  (90° + 12 db)", "6 db"]],
      note=f"90° STIRRUP HOOKS ONLY WHERE DETAILED; SEISMIC FRAMES: 135° + 6 db ≥ 75 (MIN. REG. NO. 49, DPT 1302). "
           f"[{E8} 7.1, 7.2, T7.1; {E14} 2.5.1.2]", align="LCC")
    P("5.4", f"CLEAR SPACING ≥ db AND ≥ 25 mm; LAYERS ALIGNED, ≥ 25 mm APART; COLUMN BARS ≥ 1.5 db AND ≥ 40 mm; MAIN "
             f"BARS IN SLABS AND WALLS ≤ 3 h AND ≤ 450 mm. BUNDLES: ≤ 4 DB, NONE > DB36 IN BEAMS, CUTOFFS STAGGERED "
             f"40 db. [{E8} 7.6]")
    P("5.5", f"FIX BARS RIGIDLY WITH ≥ 0.9 mm (USE 1.25 mm) ANNEALED WIRE; ERECTION BARS AND CHAIRS AS NEEDED. NO "
             f"TACK WELDING WITHOUT APPROVAL. [{E8} 7.5.1, 7.5.4; {E14} 2.5.1.3]")
    P("5.6", f"SPACERS: PRECAST CONCRETE OR MORTAR OF STRENGTH ≥ THE CONCRETE, AT ≤ 1.0 m EACH WAY. PLASTIC OR "
             f"STAINLESS ONLY WITH APPROVAL; NO TIMBER, BRICK OR STONE. BOTTOM BARS OF FOOTINGS AND GROUND BEAMS ON "
             f"PRECAST BLOCKS; TOP MATS ON STEEL CHAIRS DESIGNED BY THE CONTRACTOR (MATS ≥ 1.2 m DEEP: SUPPORT SYSTEM "
             f"DESIGNED BY AN ENGINEER AND APPROVED). BAR DIMENSIONS ARE OUT-TO-OUT, INCLUDING HOOKS. [{E14} 2.5.1.3]")
    P("5.7", f"PLACING TOLERANCE: d ±10 mm (d ≤ 200) / ±13 mm; COVER −10 / −13 mm AND ≤ 1/3 OF THE SPECIFIED COVER; "
             f"BENDS AND BAR ENDS ±50 mm (±25 mm AT DISCONTINUOUS ENDS, ±13 mm AT CORBELS). [{E8} 7.5.2; {E14} T2.20]")
    T("COLUMN TIES", [0.50, 0.50],
      ["LONGITUDINAL BAR", "MIN. TIE"],
      [["≤ DB12", "RB6"],
       ["DB16 – DB20", "RB9"],
       ["DB25 – DB28", "DB10"],
       ["≥ DB32, BUNDLES", "DB12"]],
      note=f"TIE SPACING ≤ LEAST OF 16 db (MAIN BAR), 48 db (TIE) AND THE LEAST COLUMN DIMENSION. EVERY CORNER AND ALTERNATE BAR IN A TIE CORNER ≤ 135°, NO BAR > 150 CLEAR FROM A SUPPORTED BAR; FIRST TIE "
           f"≤ s/2 FROM SLAB. INTERMEDIATE AND SPECIAL FRAMES: DEFORMED HOOPS AND CROSSTIES, DB10 MIN. SPIRALS ≥ 9 mm, CLEAR PITCH 25 – 75, 1.5 EXTRA TURNS, LAP 48 db (DEFORMED) / 72 db "
           f"(PLAIN) ≥ 300. ANCHOR BOLTS: ≥ 2-DB12 OR 3-DB10 TIES WITHIN 125 OF THE TOP. [{E8} 7.10.4, 7.10.5]",
      align="CC")
    P("5.8", f"BEAMS: COMPRESSION BARS ENCLOSED BY TIES AS FOR COLUMNS; CLOSED STIRRUPS WHERE TORSION OR STRESS "
             f"REVERSAL, WITH 135° HOOKS ROUND A BAR OR CLASS B LAPS. [{E8} 7.11]")
    P("5.9", f"SHRINKAGE AND TEMPERATURE BARS: As/Ag ≥ 0.0025 (SR24), 0.0020 (SD30), 0.0018 (SD40) AND ≥ 0.0014, "
             f"AT ≤ 5 h AND ≤ 400 mm. [{E8} 7.12]")
    P("5.10", f"INTEGRITY: PERIMETER BEAMS CONTINUOUS WITH ≥ 1/6 OF TOP SUPPORT BARS AND ≥ 1/4 OF BOTTOM MIDSPAN BARS "
              f"(≥ 2 BARS EACH), IN CLOSED STIRRUPS WITH 135° HOOKS; SPLICE TOP BARS AT MIDSPAN, BOTTOM BARS NEAR "
              f"SUPPORTS, CLASS B. [{E8} 7.13]")
    P("5.11", f"PROTECT STARTER BARS AND FUTURE-EXTENSION ITEMS FROM CORROSION; REMOVE COATINGS BEFORE CONCRETING. "
              f"[{E8} 7.7.6; {E14} 2.5.1.4]")

    H("6. DEVELOPMENT AND SPLICES")
    P("6.1", f"LAP ONLY WHERE SHOWN OR APPROVED. TENSION LAPS CLASS B (CLASS A ONLY WHERE As ≥ 2 x REQUIRED AND "
             f"≤ 50 % IS SPLICED); ADJACENT LAPS STAGGERED ≥ 1.0 m U.N.O. (COLUMN AND WALL VERTICAL BARS MAY LAP AT "
             f"ONE LEVEL PER THE COLUMN / WALL DETAILS); NO LAPS FOR BARS LARGER THAN DB36 OR IN BEAM-COLUMN JOINTS. "
             f"[{E8} 12.13, 12.14; {E14} 2.5.1.4]")
    T(f"LAP AND ANCHORAGE LENGTH (mm), f'c 240 ksc, SD40",
      [0.23] + [0.77 / len(LAP_DB)] * len(LAP_DB),
      ["BAR"] + [f"DB{d}" for d in LAP_DB],
      [["TENSION ld (STRAIGHT)"] + [str(rup(ld_simple(d))) for d in LAP_DB],
       ["TENSION LAP"] + [str(lap_len(d)) for d in LAP_DB],
       ["TENSION LAP, TOP *"] + [str(lap_len(d, True)) for d in LAP_DB],
       ["COMPRESSION ldc"] + [str(ldc(d)) for d in LAP_DB],
       ["COMPRESSION LAP"] + [str(lap_comp(d)) for d in LAP_DB],
       ["STANDARD HOOK ldh"] + [str(ldh(d)) for d in LAP_DB]],
      note=f"CLASS B = 1.3 ld, ld PER {E8} 12.2.2 (CLEAR COVER ≥ db, CLEAR SPACING ≥ 2 db, UNCOATED, NORMALWEIGHT). "
           f"* HORIZONTAL BARS WITH > 300 mm OF FRESH CONCRETE BELOW. COMPRESSION LAP 0.071 fy db ≥ 300 (+ 1/3 IF "
           f"f'c < 21 MPa). ldc = 0.24 fy db / √f'c ≥ 0.043 fy db ≥ 200 (DOWELS: STRAIGHT LENGTH; A HOOK DOES NOT "
           f"COUNT IN COMPRESSION). ldh ≥ 8 db ≥ 150 (x 0.7 WITH SIDE COVER ≥ 65; x 0.8 WITHIN TIES AT ≤ 3 db). "
           f"VALUES APPLY CONSERVATIVELY TO HIGHER CONCRETE GRADES; WHERE THE COVER / SPACING CONDITIONS ARE NOT MET, "
           f"ld PER {E8} 12.2.3. [{E8} 12.2, 12.3, 12.5, 12.14, 12.15]", align="L" + "C" * len(LAP_DB))
    P("6.2", f"U.N.O.: ≥ 1/3 (SIMPLE) OR 1/4 (CONTINUOUS) OF BOTTOM BARS EXTEND ≥ 150 INTO THE SUPPORT; ≥ 1/3 OF TOP "
             f"BARS EXTEND BEYOND THE POINT OF INFLECTION ≥ d, 12 db AND ln/16. [{E8} 12.10, 12.11]")
    P("6.3", f"WELDED SPLICES AND MECHANICAL COUPLERS SHALL DEVELOP ≥ 1.25 fy, TESTED BY AN APPROVED LABORATORY BEFORE "
             f"USE (3 COPIES OF RESULTS); WELD TYPE AND LOCATION AS SHOWN. [{E8} 3.5.2, 12.13.3; {E14} 2.5.1.4]")
    P("6.4", f"EVERY SPLICE SHALL BE INSPECTED AND APPROVED BY THE ENGINEER BEFORE CONCRETING. [{E14} 2.5.1.4]")

    H("7. CONCRETE COVER")
    T("MINIMUM CLEAR COVER BY STRUCTURAL ELEMENT (mm)", [0.36, 0.38, 0.13, 0.13],
      ["ELEMENT", "CONDITION", "≤ DB16", "≥ DB20"],
      [list(r) for r in COVER_ELEM],
      note=f"CAST IN PLACE; COVER FROM THE CONCRETE SURFACE TO THE OUTERMOST BAR (STIRRUP, TIE OR SPIRAL); "
           f"BAR SIZE = SIZE OF THAT BAR. BUNDLES: EQUIVALENT DIAMETER ≤ 50 (75 AGAINST EARTH). EMBEDDED PIPES: 35 "
           f"EXPOSED / 20 INTERIOR. PRECAST: PER {E8} 7.7.2. [{E8} 7.7.1, 7.7.3, 6.3.10]", align="LLCC")
    P("7.1", "RECOMMENDATION - ENVIRONMENT (WHERE THE PROJECT REQUIRES IT):")
    T("RECOMMENDED COVER, AGGRESSIVE EXPOSURE (mm)", [0.55, 0.15, 0.15, 0.15],
      ["MEMBER", "f'c < 20", "21 – 40", "> 40"],
      [[m, str(cov(c0, 1.2)), str(cov(c0, 1.0)), str(cov(c0, 0.9))] for m, c0 in COVER_ENV],
      note=f"COASTAL, CHLORIDE, SEWAGE, SULFATE OR CHEMICAL EXPOSURE: INCREASE COVER TO c = α · c0 (ROUNDED UP TO 5; "
           f"α 1.2 / 1.0 / 0.9 BY f'c) AND USE DENSER CONCRETE (w/b ≤ 0.45). FIRE: WHERE REGULATIONS NEED MORE COVER "
           f"THE LARGER GOVERNS (COLUMNS, BEAMS ≥ 300: 40; SLABS ≥ 115: 20). "
           f"[{E8} 7.7.4, 7.7.5; {E14} 2.5.1.5, T2.21, T2.23, T2.24; DPT 1332]", align="LCCC")

    H("8. FORMWORK, SHORING AND EMBEDDED ITEMS")
    P("8.1", f"DESIGNED, ERECTED AND REMOVED BY THE CONTRACTOR (ACI 347), FOR PLACING RATE, CONSTRUCTION AND IMPACT "
             f"LOADS, FRESH-CONCRETE PRESSURE, DEFLECTION, BRACING AND SHORE SPLICES; SUBMIT WHERE REQUIRED. LOADS: "
             f"CONCRETE 2,400 + STEEL 150 kg/m³; CONSTRUCTION 60 – 250 kg/m²; LATERAL ≥ 150 kg/m OR 2 % DL. "
             f"[{E8} 6.1; {E14} 10.1 – 10.3]")
    P("8.2", f"FORMS MORTAR-TIGHT; VISIBLE DEFLECTION ≤ SPAN/240; 20 x 20 CHAMFER ON EXPOSED CORNERS; CLEAN-OUTS AT "
             f"COLUMN AND WALL BASES; RELEASE AGENT KEPT OFF BARS AND JOINTS. [{E14} 10.3.1, 10.4]")
    P("8.3", f"SHORES BRACED, ON A FIRM BASE, WEDGE OR JACK ADJUSTED; SPLICED ≤ EVERY 2ND SHORE UNDER SLABS, 3RD UNDER "
             f"BEAMS. NO CONSTRUCTION LOAD ON ANY PART UNTIL IT CAN CARRY IT. [{E8} 6.2.1, 6.2.2; {E14} 10.3.2]")
    T("FORM REMOVAL (GENERAL STRUCTURES)", [0.52, 0.26, 0.22],
      ["FORMWORK", "FIELD-CURED f'c", "OR AGE"],
      [["SIDES OF COLUMNS, BEAMS, WALLS, FOOTINGS", "≥ 5 MPa", "2 DAYS"],
       ["SOFFITS OF SLABS AND BEAMS, INCL. SHORES", "≥ 14 MPa", "14 DAYS"]],
      note=f"CANTILEVERS, TRANSFER MEMBERS AND LONG SPANS ONLY ON THE ENGINEER'S INSTRUCTION. RESHORE ONLY TO AN "
           f"APPROVED PLAN, IMMEDIATELY AFTER STRIPPING. [{E8} 6.2; {E14} T10.1, T10.2, 10.6]", align="LCC")
    P("8.4", f"EMBEDDED PIPES AND CONDUITS ONLY WITH APPROVAL; NO ALUMINIUM. OUTSIDE Ø ≤ 1/3 OF THE MEMBER THICKNESS, "
             f"≥ 3 Ø C/C, IN SLABS BETWEEN THE TOP AND BOTTOM BARS; IN COLUMNS ≤ 4 % OF THE AREA. PROVIDE 0.002 Ac "
             f"NORMAL TO PIPING; DO NOT CUT OR DISPLACE BARS. [{E8} 6.3]")
    P("8.5", "ANCHOR BOLTS: SET WITH TEMPLATES AND FIXED BEFORE CONCRETING, POSITION TOLERANCE PER THE STEEL "
             "SPECIFICATION. BASE PLATES ON NON-SHRINK GROUT, 25 – 50 THICK, STRENGTH ≥ THE SUPPORTING CONCRETE.")
    T("CONSTRUCTION TOLERANCES (mm)", [0.58, 0.42],
      ["ITEM", "TOLERANCE"],
      [["PLUMB: COLUMNS, WALLS", "6 PER 3 m; 25 MAX."],
       ["PLUMB: EXPOSED CORNERS, CONSPICUOUS LINES", "6 PER 3 m; 12 MAX."],
       ["LEVEL: SLAB AND BEAM SOFFITS (BEFORE STRIPPING)", "6 PER 3 m; 10 PER BAY; 20 MAX."],
       ["BUILDING LINES; COLUMN AND WALL POSITION", "12 PER BAY; 25 MAX."],
       ["OPENINGS: SIZE AND POSITION", "± 6"],
       ["SECTIONS; SLAB AND WALL THICKNESS", "− 5 / + 10"],
       ["FOOTINGS: PLAN / ECCENTRICITY", "− 12 / + 50;  ≤ 2 % ≤ 50"],
       ["FOOTINGS: THICKNESS", "− 5 % / + 100"],
       ["STAIRS: RISER / TREAD IN FLIGHT (ADJACENT)", "4 / 6  (2 / 4)"]],
      note=f"[{E14} 10.7; ACI 117]", align="LC")

    H("9. PLACING AND COMPACTION")
    P("9.1", f"HOLD POINT: THE ENGINEER SHALL APPROVE FORMWORK, REINFORCEMENT, SPLICES, COVER AND EMBEDDED ITEMS "
             f"IN WRITING BEFORE EACH POUR. [{E14} 7.1.1, 2.5.1.4]")
    P("9.2", f"CLEAN EQUIPMENT AND FORMS; REMOVE STANDING WATER; PRE-WET WITHOUT PONDING; REMOVE LAITANCE FROM "
             f"HARDENED CONCRETE. [{E8} 5.8.1; {E14} 7.1.1]")
    P("9.3", f"DEPOSIT NEAR THE FINAL POSITION, CONTINUOUSLY TO A PANEL END OR A PLANNED JOINT, WITHOUT SEGREGATION. "
             f"FREE FALL ≤ 1.5 m; COLUMNS AND WALLS ≤ 2 – 3 m/h RISE; EACH LAYER BEFORE THE LOWER ONE SETS. DO NOT MOVE "
             f"CONCRETE WITH VIBRATORS. [{E8} 5.8.3, 5.8.4; {E14} 7.1.2]")
    P("9.4", f"INTERNAL VIBRATORS AT 450 – 750 mm CENTRES FOR 5 – 15 s, 100 mm INTO THE LAYER BELOW; KEEP A STANDBY "
             f"VIBRATOR. [{E14} 7.2; ACI 309]")
    P("9.5", f"BEAMS AND SLABS SHALL NOT BE CAST UNTIL THE SUPPORTING COLUMNS AND WALLS HAVE HARDENED (PAUSE 1 – 2 h "
             f"MIN.). [{E8} 6.4.6; {E14} 7.2.4]")
    P("9.6", f"HOT WEATHER: CONCRETE ≤ 35 °C AT PLACING; PROTECT FROM SUN AND WIND; ABOVE 35 °C RECORD TEMPERATURES "
             f"AND MEASURES TAKEN. [{E8} 1.3.3, 5.8.6; ACI 305]")

    H("10. CURING")
    P("10.1", f"CURE IMMEDIATELY: KEEP MOIST AND ABOVE 10 °C ≥ 7 DAYS (TYPE I), ≥ 3 DAYS (HIGH EARLY STRENGTH); "
              f"LONGER WITH FLY ASH OR SLAG (UP TO 21 DAYS). PROTECT FROM DRYING, RAIN, VIBRATION AND OVERLOAD. "
              f"[{E8} 5.8.5; {E14} 8.2, 8.6]")
    P("10.2", f"CURING COMPOUND ONLY WITH APPROVAL, ≥ 2 COATS, KEPT OFF BARS AND JOINTS. [{E14} 8.5]")

    H("11. JOINTS")
    P("11.1", f"CONSTRUCTION JOINTS ONLY WHERE SHOWN OR APPROVED: SLABS AND BEAMS IN THE MIDDLE THIRD OF THE SPAN; "
              f"GIRDERS ≥ 2 x THE SECONDARY-BEAM WIDTH FROM ITS INTERSECTION; COLUMNS AND WALLS AT THE TOP OF THE "
              f"FOOTING OR SLAB AND BELOW THE FLOOR SOFFIT. DROP PANELS, CAPITALS AND HAUNCHES ARE CAST WITH THE "
              f"FLOOR. [{E8} 6.4.3 – 6.4.7; {E14} 9.1]")
    P("11.2", f"REMOVE LAITANCE TO EXPOSE THE AGGREGATE (≈ 5 mm AMPLITUDE); CLEAN, WET, REMOVE STANDING WATER; GROUT "
              f"WITH w/c LOWER THAN THE CONCRETE. [{E8} 6.4.1, 6.4.2; {E14} 9.1.1, 9.1.2]")
    P("11.3", f"WHERE COLUMN f'c > 1.4 x FLOOR f'c, PLACE COLUMN CONCRETE IN THE FLOOR OVER 4 x THE COLUMN AREA, "
              f"MONOLITHIC WITH THE FLOOR. [{E14} 9.1.3]")
    P("11.4", f"EXPANSION AND CONTRACTION JOINTS AS DETAILED, WITH FILLER, SEALANT AND WATER STOP WHERE SHOWN. "
              f"[{E8} 1.2.1; {E14} 9.2, 9.3]")
    P("11.5", "WHERE JOINTS ARE NOT SHOWN (WALLS, SLABS ON GROUND, RETAINING WALLS), THE CONTRACTOR SUBMITS A JOINT "
              "LAYOUT FOR APPROVAL BEFORE FORMWORK STARTS.")

    H("12. FINISHING AND REPAIR")
    P("12.1", f"DO NOT TROWEL WITH BLEED WATER PRESENT OR IN RAIN. ROOF SLABS SHALL NOT BE STEEL-TROWELLED SMOOTH "
              f"U.N.O. [{E14} 11.2]")
    P("12.2", f"HONEYCOMB AND DEFECTS ARE REPAIRED ONLY BY AN APPROVED METHOD: CUT BACK TO SOUND CONCRETE, WET, "
              f"REPAIR WITH APPROVED MORTAR OR CONCRETE. STRUCTURAL DEFECTS PER THE ENGINEER. [{E14} 11.3]")

    H("13. INSPECTION AND RECORDS")
    P("13.1", f"KEEP RECORDS OF MATERIALS, MIXES, DELIVERY TICKETS, POURS (DATE, TIME, LOCATION, VOLUME, WEATHER), "
              f"TESTS, CURING, FORMWORK AND SHORING, REINFORCEMENT APPROVALS, CONSTRUCTION LOADS, DEVIATIONS AND "
              f"PHOTOGRAPHS; RETAIN ≥ 2 YEARS AFTER COMPLETION. [{E8} 1.3.2 – 1.3.4, 3.1.2; {E14} 13.1]")
    P("13.2", f"INSPECT COMPLETED MEMBERS; REPAIR DEFECTS AS INSTRUCTED BEFORE THE STRUCTURE IS USED. [{E14} 12.5.1]")

    H("14. FOUNDATIONS AND PILES")
    P("14.1", "DESIGN BASED ON THE SOIL INVESTIGATION REPORT [ REF., DATE ]. SPREAD FOOTINGS: ALLOWABLE BEARING "
              "[ ] t/m² AT [ ] m BELOW GROUND; PILES: TYPE [ ], SIZE [ ], SAFE LOAD [ ] t / PILE, TIP LEVEL [ ].")
    P("14.2", "PILE TESTS: [ STATIC / DYNAMIC ] LOAD TEST ON [ ] PILES AND INTEGRITY TEST ON [ ] % OF THE PILES; "
              "RESULTS TO THE ENGINEER BEFORE THE CAPS ARE CAST.")
    P("14.3", "PILE POSITION AND PLUMBNESS WITHIN THE SPECIFIED TOLERANCES; PILES OUT OF TOLERANCE, DAMAGED OR SHORT "
              "ARE REPORTED TO THE ENGINEER BEFORE THE CAP IS FORMED.")
    P("14.4", "PILE HEADS CUT TO SOUND CONCRETE; PILE EMBEDMENT AND ANCHORAGE INTO THE CAP PER THE FOUNDATION DETAILS. "
              "CAP BOTTOM BARS CLEAR ABOVE THE PILE HEADS.")
    P("14.5", "LEAN CONCRETE 50 UNDER FOOTINGS, CAPS AND GROUND BEAMS. EXCAVATIONS KEPT DRY; DEWATERING AND SHORING "
              "DESIGNED BY THE CONTRACTOR. FILL UNDER SLABS ON GROUND COMPACTED IN LAYERS TO THE SPECIFIED DENSITY.")

    H("ABBREVIATIONS")
    f.terms(ABBR_GENERAL, title="GENERAL")
    f.terms(ABBR_REBAR, title="REBAR POSITION AND BAR CALL-OUTS")
    f.terms(ABBR_SYMBOLS, title="SYMBOLS IN THE DETAILS")

    for fn in DETAILS:                                   # each carries its own underlined title
        f.detail(fn)


def stirrup(ps, tl, tr, br, bl, leg, layer="S-REBR-SEC"):
    """closed stirrup on its centreline. Each corner is an arc concentric with its corner bar
    (corner = (cx, cy, R), R = bar radius + half stirrup diameter), so the stirrup wraps the bars.
    Both 135 deg hooks are at the top-left bar: one end wraps from the top edge round to 225 deg, the other
    from the left edge round to 45 deg; the two legs run into the core at 45 deg, one each side of the bar."""
    def pt(c, ang):
        return (c[0] + c[2] * math.cos(math.radians(ang)), c[1] + c[2] * math.sin(math.radians(ang)))
    b = lambda deg: math.tan(math.radians(deg) / 4)          # bulge of a CCW arc of 'deg'
    d = (0.7071, -0.7071)                                     # hook legs: 45 deg down into the core
    p45, p225 = pt(tl, 45), pt(tl, 225)
    pts = [(p45[0] + leg * d[0], p45[1] + leg * d[1], 0),    # hook end 1
           (*p45, b(135)), (*pt(tl, 180), 0),                 # wrap TL bar 45 -> 180
           (*pt(bl, 180), b(90)), (*pt(bl, 270), 0),
           (*pt(br, 270), b(90)), (*pt(br, 0), 0),
           (*pt(tr, 0), b(90)), (*pt(tr, 90), 0),
           (*pt(tl, 90), b(135)), (*p225, 0),                 # wrap TL bar 90 -> 225
           (p225[0] + leg * d[0], p225[1] + leg * d[1], 0)]  # hook end 2
    e = ps.add_lwpolyline(pts, format="xyb", dxfattribs=A(layer))
    e.dxf.flags = e.dxf.flags | 128
    return e


# ======================================================================= typical details band
def ptitle(ps, x, y, name, scale):
    """view title of the general rule (view_title) x K: bold title on an underline, scale text below"""
    yl = y - TH - 0.9 * K
    text(ps, name, (x, yl + 0.9 * K), TH, "S-TEXT", style="ANB")
    line(ps, (x, yl), (x + text_w(name, TH, "ANB") + 3.0 * K, yl), "S-TITLE")
    text(ps, scale, (x, yl - 1.2 * K), TB, "S-TEXT", align=TA.TOP_LEFT)


def note_lines(ps, x, y, s, width):
    """wrapped text from y (top) down; returns the y below the last line"""
    lines = wrap_s(s, TB, width)
    for k, ln in enumerate(lines):
        text(ps, ln, (x, y - TB - k * LP), TB, "S-TEXT")
    return y - len(lines) * LP


DET_TOP = 14.0               # drawing starts this far below a detail title's top: clear of its scale line


def det_cover(ps, x, y, w):
    """typical beam section 250 x 300 at 1:10 - clear cover to the stirrup; notes beside, in sequence"""
    ptitle(ps, x, y, "TYPICAL COVER - BEAM SECTION", "SCALE 1:10")
    k = 0.1
    B, D = 250, 300
    bx, bh = B * k, D * k
    x0, y0 = x + 8, y - DET_TOP - bh
    pline(ps, [(x0, y0), (x0 + bx, y0), (x0 + bx, y0 + bh), (x0, y0 + bh)], "S-CONC", close=True)
    c, ds = 40, 9
    rb, rt = 10, 8                                               # 3-DB20 bottom, 2-DB16 top
    ib, it = c + ds + rb, c + ds + rt                            # bar centre insets (mm)
    corner = lambda px, py, r: (x0 + px * k, y0 + py * k, (r + ds / 2) * k)
    tl, tr = corner(it, D - it, rt), corner(B - it, D - it, rt)
    bl, br = corner(ib, ib, rb), corner(B - ib, ib, rb)
    stirrup(ps, tl, tr, br, bl, max(6 * ds, 75) * k)
    for cx in (ib, B / 2, B - ib):
        dot(ps, (x0 + cx * k, y0 + ib * k), rb * k)
    for cx in (it, B - it):
        dot(ps, (x0 + cx * k, y0 + (D - it) * k), rt * k)
    dim(ps, (x0, y0), (x0 + bx, y0), (0, y0 - 4.5), 1, text=str(B))
    dim(ps, (x0 + bx, y0), (x0 + bx, y0 + bh), (x0 + bx + 4.5, 0), 1, angle=90, text=str(D))
    dim(ps, (x0, y0), (x0, y0 + c * k), (x0 - 4.5, 0), 1, angle=90, text="c")
    dim(ps, (x0, y0 + bh), (x0 + c * k, y0 + bh), (0, y0 + bh + 3), 1, text="c")
    tx = x0 + bx + 10
    tw = w - (tx - x)
    yy = note_lines(ps, tx, y0 + bh + 2, "c = CLEAR COVER TO THE OUTERMOST BAR: THE STIRRUP IN BEAMS, THE TIE OR "
                    "SPIRAL IN COLUMNS, THE OUTER LAYER IN SLABS AND WALLS. VALUES BY ELEMENT: TABLE 7 (INTERIOR "
                    "BEAMS AND COLUMNS 40).", tw)
    note_lines(ps, tx, yy - PG, "STIRRUP CORNERS WRAP THE CORNER BARS; BOTH 135° HOOKS ROUND THE SAME BAR. "
               "SPACERS UNDER THE STIRRUP AT ≤ 1.0 m. [EIT 011008 7.7.1]", tw)


def det_hooks(ps, x, y, w):
    """standard hooks - N.T.S., stacked; each row = symbol + bold name + extension, rows sized by their text"""
    ptitle(ps, x, y, "STANDARD HOOKS", "N.T.S.")
    dbd = 0.55
    tx = x + 21
    tw = w - 21
    r = y - DET_TOP + 2.0

    def label(r, name, ext):
        text(ps, name, (tx, r - TB), TB, "S-TEXT", style="ANB")
        return note_lines(ps, tx, r - LP, ext, tw)

    bar(ps, [(x + 2, r - 1), (x + 13, r - 1), (x + 13, r - 8)], dbd)              # 90 deg
    text(ps, "12 db", (x + 14, r - 7.5), TB * 0.9, "S-TEXT")
    r = min(label(r, "90° - MAIN BARS", "EXTENSION 12 db"), r - 9) - 2.0
    bar(ps, [(x + 2, r - 1), (x + 12, r - 1), (x + 12, r - 5), (x + 8, r - 5)], dbd)  # 180 deg
    r = min(label(r, "180° - MAIN BARS", "EXTENSION 4 db ≥ 65"), r - 6) - 2.0
    s_, rd, rs = 9.0, 0.7, 0.3                                   # 135 deg stirrup / tie
    cn = [(x + 4 + rd, r - rd), (x + 4 + s_ - rd, r - rd), (x + 4 + s_ - rd, r - s_ + rd), (x + 4 + rd, r - s_ + rd)]
    stirrup(ps, *[(cx, cy, rd + rs) for cx, cy in cn], 3.6, "S-REBR")
    for cx, cy in cn:
        dot(ps, (cx, cy), rd)
    label(r, "135° - STIRRUPS, TIES", "EXTENSION 6 db ≥ 75. BENDS: TABLE 4 [EIT 011008 7.1, 7.2]")


def det_laps(ps, x, y, w):
    """lap splices staggered - N.T.S."""
    ptitle(ps, x, y, "TYPICAL LAP SPLICES - STAGGER", "N.T.S.")
    xa, xb = x + 2, x + w - 3
    L = 13.0
    G = 24.0                                                     # drawn stagger: room for "≥ 1.0 m CLEAR"
    y1 = y - DET_TOP - 4.0
    rows = [(y1, xa + 7), (y1 - 5, xa + 7 + L + G), (y1 - 10, xa + 7)]
    for yy, xl in rows:                                          # cranked lap (office standard, lap_crank)
        line(ps, (xa, yy), (xl + L, yy), "S-REBR")
        pline(ps, lap_crank(xl, xl + L, yy, 1.0, past=1.0) + [(xb, yy)], "S-REBR")
    (y1, xl1), (y2, xl2) = rows[0], rows[1]
    dim(ps, (xl1, y1 + 1.0), (xl1 + L, y1 + 1.0), (0, y1 + 4.5), 1, text="LAP (TABLE 6)")
    yd = rows[2][0] - 5.0
    dim(ps, (xl1 + L, y2), (xl2, y2), (0, yd), 1, text="≥ 1.0 m CLEAR")
    note_lines(ps, x + 2, yd - 4.0, "LAPS OF ADJACENT BARS STAGGERED ≥ 1.0 m CLEAR; ≤ 50 % OF THE BARS LAPPED AT "
               "ONE SECTION U.N.O. (COLUMN BARS: 1101); BARS IN CONTACT, TIED WITH ≥ 0.9 mm WIRE. LAP ONLY WHERE SHOWN OR APPROVED; NO LAPS FOR "
               "BARS > DB36 OR IN BEAM-COLUMN JOINTS. [EIT 011008 12.13, 12.14; EIT 011014 2.5.1.4]", w - 3)


# ----------------------------------------------------------------------- abbreviations (column lists)
ABBR_GENERAL = [
    ("DB, RB", "DEFORMED BAR, ROUND BAR"),
    ("f'c, f'cr", "SPECIFIED CYLINDER STRENGTH, REQUIRED MEAN STRENGTH"),
    ("fy", "YIELD STRENGTH OF REINFORCEMENT"),
    ("w/b, w/cm", "WATER-BINDER RATIO"),
    ("ss", "STANDARD DEVIATION OF STRENGTH TESTS"),
    ("ksc", "kg/cm² (1 MPa ≈ 10.2 ksc)"),
    ("TYP., SIM.", "TYPICAL, SIMILAR"),
    ("U.N.O.", "UNLESS NOTED OTHERWISE"),
    ("N.T.S.", "NOT TO SCALE"),
    ("C/C, CLR.", "CENTRE TO CENTRE, CLEAR"),
    ("CL", "CENTRE LINE"),
    ("THK., DIA., Ø", "THICKNESS, DIAMETER"),
    ("MIN., MAX.", "MINIMUM, MAXIMUM"),
    ("EL., FFL, SFL", "LEVEL; FINISHED / STRUCTURAL FLOOR LEVEL"),
    ("CJ, EJ", "CONSTRUCTION JOINT, EXPANSION JOINT"),
    ("SOG", "SLAB ON GROUND"),
    ("EIT 011008", "EIT STANDARD 011008-21 (DESIGN)"),
    ("EIT 011014", "EIT STANDARD 011014-19 (MATERIALS AND CONSTRUCTION)"),
    ("DPT", "DEPARTMENT OF PUBLIC WORKS AND TOWN & COUNTRY PLANNING STANDARD"),
]
ABBR_REBAR = [
    ("n-DBxx", "n BARS OF DIAMETER xx mm, e.g. 4-DB20"),
    ("DBxx @ s", "BARS OF DIAMETER xx mm AT s mm CENTRES, e.g. DB12 @ 200"),
    ("T, B", "TOP, BOTTOM"),
    ("T1, T2", "TOP BARS: OUTER LAYER, SECOND LAYER"),
    ("B1, B2", "BOTTOM BARS: OUTER LAYER, SECOND LAYER"),
    ("EF", "EACH FACE"),
    ("NF, FF", "NEAR FACE, FAR FACE"),
    ("IF, OF", "INNER FACE, OUTER FACE (WALLS, TANKS)"),
    ("EW", "EACH WAY"),
    ("ES", "EACH SIDE"),
    ("ADD.", "ADDITIONAL BARS (ADDED TO THE CONTINUOUS BARS)"),
    ("CONT.", "CONTINUOUS"),
    ("ALT.", "ALTERNATE (ALTERNATE BARS / HOOKS)"),
    ("STR., TIE", "STIRRUP (BEAMS), TIE (COLUMNS); HOOP = CLOSED TIE WITH SEISMIC HOOKS"),
]
ABBR_SYMBOLS = [
    ("ℓn", "CLEAR SPAN, FACE TO FACE OF SUPPORTS"),
    ("L1, L2", "SPANS OF ADJACENT BAYS, AS DIMENSIONED"),
    ("Lc", "CANTILEVER LENGTH FROM THE SUPPORT FACE"),
    ("Sn", "CLEAR SHORT SPAN OF A SLAB PANEL"),
    ("h", "OVERALL DEPTH OF A BEAM; THICKNESS OF A SLAB"),
    ("d", "EFFECTIVE DEPTH"),
    ("bw", "WEB WIDTH OF A BEAM"),
    ("c", "CLEAR COVER (TABLE 7)"),
    ("c1, c2", "COLUMN SIZE IN, ACROSS THE SPAN DIRECTION"),
    ("Hc", "CLEAR HEIGHT OF A COLUMN"),
    ("lo", "LENGTH OF THE COLUMN END ZONE (CONFINEMENT)"),
    ("s", "SPACING OF BARS, TIES OR STIRRUPS"),
    ("s0, s1", "TIE SPACING IN THE COLUMN END ZONE; STIRRUP SPACING IN THE BEAM 2h ZONE"),
    ("hx", "MAX. CENTRE SPACING OF HOOP LEGS OR CROSSTIES"),
    ("db, dt", "DIAMETER OF THE MAIN BAR, OF THE TIE OR STIRRUP"),
    ("Ld, ldh", "DEVELOPMENT LENGTH, STRAIGHT / HOOKED (TABLE 6)"),
]

# tables cited by number: title start -> (number, sheet cited with it or None). "1002 TABLE 6" is cited on
# 1101 - 1127; TABLE 4 / 6 / 7 in the details and abbreviations here; TABLE 1 in note 2.5.
TABLE_REFS = {"PROJECT DESIGN DATA": (1, None), "HOOKS AND BENDS": (4, None),
              "LAP AND ANCHORAGE LENGTH": (6, "1002"), "MINIMUM CLEAR COVER": (7, None)}

DETAILS = [det_cover, det_hooks, det_laps]           # order in the flow (after the abbreviations)
DET_BLK = {"det_cover": ("COVER", "TYPICAL COVER - BEAM SECTION", "1:10"),
           "det_hooks": ("HOOKS", "STANDARD HOOKS", "N.T.S."),
           "det_laps": ("LAPS", "TYPICAL LAP SPLICES - STAGGER", "N.T.S.")}
FIGS = []                                            # (sheet index, fn, x, y_top) filled by Flow.detail
DET_GAP = 6.0 * K                                    # clear space above a detail (its title is a heading)
_DET_H = {}


def detail_h(fn):
    """height of a detail drawn at the column width (measured once, in a scratch block)"""
    if fn.__name__ not in _DET_H:
        blk = doc.blocks.new("_MEASURE")
        fn(blk, 0.0, 0.0, COLW)
        _DET_H[fn.__name__] = -bbox.extents(blk).extmin.y + 1.0
        doc.blocks.delete_block("_MEASURE", safe=False)
    return _DET_H[fn.__name__]


def bottom(c):
    return FY0 + 3.0                                  # every column runs to the foot of its sheet


def fits(npage):
    f = Flow(None, bottom, draw=False)
    content(f)
    return f.col < npage * NCOL


def notes_columns(ps, page, npage):
    f = Flow(ps, bottom, page=page)
    content(f)
    used = NCOL if page < npage - 1 else f.col - page * NCOL + 1
    for k in range(1, used):                                  # thin grey rules between the used columns
        xr = CX0 + k * (COLW + CGAP) - CGAP / 2
        line(ps, (xr, FY0 + 3.0), (xr, CY1), "S-TTLB-THIN")
    return f


def build():
    npage = 1
    while not fits(npage):
        npage += 1
    td_engine.REVS = [("A", "ISSUED FOR REVIEW", REV_A_DATE),
                      ("B", f"TEXT 2.0 mm, {npage} SHEETS", PROJ["date"])]
    td_engine.REVS_BY_SHEET = {str(1001 + p): [("B", "FIRST ISSUE (FROM 1001 REV A)", PROJ["date"])]
                               for p in range(1, npage)}
    SHEETS[:] = [(str(1001 + p), [f"GENERAL NOTES ({p + 1})" if npage > 1 else "GENERAL NOTES",
                                  "STRUCTURAL CONCRETE"], "N.T.S.") for p in range(npage)]
    print(f"  notes: K = {K:.3f}: text {TB:.2f} / {TH:.2f}, pitch {LP:.2f}, table row {TRH:.2f}; "
          f"{npage} sheets, column width {COLW:.1f} mm")
    FIGS.clear()
    for p in range(npage):
        ps = new_sheet(p)
        sheet = SHEETS[p][0]
        f = group(f"NOTES-{sheet}-1", notes_columns, ps, p, npage, g_kind="notes",
                  g_title=f"GENERAL NOTES ({p + 1})")
        for pg, fn, x, y in FIGS:
            if pg == p:
                tag, title, scale = DET_BLK[fn.__name__]
                group(f"DET-{sheet}-{tag}", fn, ps, x, y, COLW, g_kind="detail", g_title=title, g_scale=scale)
                print(f"    {sheet}: detail {title} (column {int(round((x - CX0) / (COLW + CGAP))) + 1})")
    for n, title, pg in f.tables:
        print(f"    {SHEETS[pg][0]}: TABLE {n} - {title}")
    for key, (n, sheet) in TABLE_REFS.items():
        hit = [(tn, SHEETS[pg][0]) for tn, title, pg in f.tables if title.startswith(key)]
        if hit != [(n, sheet or hit[0][1] if hit else None)]:
            print(f"  !! table cited as TABLE {n}{' on ' + sheet if sheet else ''} is now {hit}: {key} "
                  f"- update the references (gn_notes.py, td_*.py)")
