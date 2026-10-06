# Calculation Report Generation from a Live MIDAS GEN NX Model

> **Copied** from [`konohatrong/midas_API`](https://github.com/konohatrong/midas_API/blob/b4155ac/pilot%20project/wind%20load%20generator/docs/CALC_REPORT_GENERATION.md) (`pilot project/wind load generator/docs/CALC_REPORT_GENERATION.md`, commit b4155ac, 2026-10-04) into this repository's `midas/` folder. Paths in the text such as `To midas/…`, `pilot project/…` or the root `README.md` name that repository; the map is in [`midas/README.md`](../README.md).

A repeatable procedure for producing a **structural calculation report** (`.docx`) whose
data is extracted **directly from a live MIDAS GEN NX model** over the MAPI, formatted into
the office calculation-report template with its own fonts, header and figure-table.

The report has two parts:

1. **Analysis part (Sections 1–6), generated from the live model:** model summary, design
   loads, behaviour figures, gravity reactions, lateral results with storey drift, and the
   ELF calculation sheet.
2. **Member design part (Section 7), optional:** the MIDAS GEN NX / MIDAS Design+
   design-result pages that the engineer exports, inserted one page per figure.

Proven on two projects (Samut Songkhram, 2026-09):

| Project | Model | Report |
|---|---|---|
| Building A, office | 22,983 nodes, 25,586 elements, 19 supports | 53 figures, including 44 design pages |
| Building B, fire station | 5,120 nodes, 6,368 elements, 26 supports | 28 figures, including 14 design pages |

---

## 0. Security: MAPI key handling (read first)

> **The MIDAS MAPI key is a credential.** It is passed **only transiently as a command-line
> argument** to the Python scripts. It is **never** written into any file, script, doc,
> log, commit, or memory. Every script reads it from `sys.argv[1]`.

```bash
python script.py "<MAPI-KEY>"      # key supplied at run time only
```

If a key stops working: in MIDAS GEN NX → **Apps → Connect**, confirm the key matches, or
issue a fresh key. A dropped session reports *"GEN NX model is not connected."* The
connection also drops after the model is **saved under a new name or reopened**; reconnect
before extracting.

---

## 1. Prerequisites

| Need | Notes |
|------|-------|
| MIDAS GEN NX running, model open, MAPI connected | `Apps → Connect` |
| Python 3.11 with `midas_gen` (v1.6.6+) | connection helper in `src/windload/midas/connection.py` |
| `python-docx` (`pip install python-docx`) | builds the `.docx` |
| `Pillow` | converts the exported BMP design pages to PNG |
| `PyMuPDF` / `fitz` (`pip install pymupdf`) | reads code PDFs (poppler is **not** installed on this machine) |
| Scratchpad dir for intermediate PNG/JSON | keep temporary artefacts out of the repo |

**Connection boilerplate** (top of every script):

```python
import sys, os
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator")
sys.path.insert(0, "src")
from windload.midas.connection import connect
connect(sys.argv[1])          # MAPI key as argv[1], never hard-coded
import midas_gen as mg
```

The library prints a boxed banner; filter it in the shell with
`... | grep -avE "^[│╭╰┃┏┗]"`. The console is `cp874`, so force UTF-8
(`sys.stdout.reconfigure(encoding="utf-8")`) when printing Thai, and open output files with
`encoding="utf-8"`.

**Extraction is read-only.** GET requests, result tables, `/view/CAPTURE` and
`/doc/EXPORTMXT` do not change the model. Never write to the model while producing a report.

---

## 2. Run the analysis first

Result tables and result figures need analysis results. If they are missing, every result
call returns *"there is no analysis result."*

```python
try:    mg.Result.TABLE.Reaction(loadcase=["DL(ST)"])
except: mg.MidasAPI("POST", "/doc/ANAL", {"Assign": {}})   # ~95 s for a 25k-element model
```

---

## 3. The template

**File:** `G:\My Drive\Works\##Calculation Report Template\20230910 - Calculation Report Template.docx`

**Why copy it rather than rebuild it:** copying the template file carries over, for free:
- the styles;
- the **header/footer parts** (company header + logo `word/media/image1.png`);
- the page setup (A4 portrait, 25.4 mm margins);
- the **Table-of-Figures field**.

Build method:

1. `shutil.copyfile(TEMPLATE, OUTPUT)`
2. Open with `python-docx`, delete every body child **except the final `w:sectPr`**.
3. Re-point that `sectPr`'s `headerReference` (type `default`) to the standard header
   (`rId8` → `header1.xml`) and `footerReference` to the footer. Drop the `titlePg` and
   first-page-only references so the header shows on every page.
4. Append the report content using the template's own styles.

**Template facts worth knowing:**
- The template has bilingual Thai/English boilerplate. The body is cleared, so an English-only
  report has no Thai text left.
- The figure table is a field, **`TOC \h \z \c "Figure"`**. It collects **`SEQ Figure`
  fields**, *not* the Caption style, so captions need real SEQ fields (see §6).

---

## 4. Fonts / styles / sizes

Everything inherits from the template's `styles.xml`. **Do not override the font.** Reuse the
named styles so pasted content matches the master report.

| Element | Style name | Font | Size | Notes |
|---------|-----------|------|------|-------|
| Body default | `Normal` | **TH SarabunPSK** | **14 pt** (`sz` 28) | base font for the whole report |
| Section heading | `Heading 1` | TH SarabunPSK | template | `1. Structural Model` … `7. RC Member Design` |
| Sub-heading | `Heading 2` | TH SarabunPSK | template | `2.1 …`, `(a)`, `7.1 Beams` |
| Body paragraph | `Body Text` | TH SarabunPSK | 14 pt | narrative |
| Figure caption | `Caption` | TH SarabunPSK | template | **must contain a `SEQ Figure` field** |
| Bullet list | `List Bullet` | TH SarabunPSK | 14 pt | notes |
| Tables | `Table Grid` | TH SarabunPSK | 13 pt in cells (10–11 pt for wide tables) | header row shaded `#305496` with white bold text; totals row shaded `#D9E1F2` |

When writing table cells directly, set both the ASCII font and the **complex-script** font
so that Thai renders: `run.font.name = "TH SarabunPSK"` **and**
`run._element.rPr.rFonts.set(qn('w:cs'), "TH SarabunPSK")`.

Title block: centred and bold, 20 pt (building name) and 16 pt (subtitle). A page break
follows the Table of Figures and precedes each main section.

**English-only reports:** figures made in Python must have English labels too. For example,
live-load plans need an `--en` variant with English room names and clause references; do not
reuse the Thai-labelled working sheets.

---

## 5. Data to include (Sections 1–6)

Pull everything from the live model. Units are **kN and m** (the MIDAS default). The
`Result.TABLE.*` calls return polars DataFrames; iterate with
`[dict(zip(df.columns, r)) for r in df.rows()]` and drop the `SUMMATION` rows (keep rows
whose `Node` is numeric).

### 5.1 Section 1: Structural model
- Node and element counts (`/db/NODE`, `/db/ELEM`) and the BEAM/PLATE split.
- Levels (`/db/STOR`), supports (`/db/CONS` or the reaction nodes).
- Column and beam section names (`/db/SECT` `SECT_NAME`), slab thicknesses (`/db/THIK`).
- Concrete and rebar grades (`/db/MATD`: `REBAR_CODENAME`, `MAINREBAR_REBARNAME`, `*_B_FY`).
- Design code (`/db/DCON`).
- Figures: isometric, front and side geometry (`SET_MODE "pre"`, `SET_HIDDEN True`).

### 5.2 Section 2: Design loads
- **DL:** the self-weight total from the DL reaction (`/db/BODF` gives self-weight on DL).
- **SDL and LL:** from `/db/PRES`. Each item has `LCNAME`, and `FORCES[0]` is the uniform
  pressure (negative means downward in GZ). Summarise pressure × plate area:
  - **by level**, when loads are uniform per floor (Building A);
  - **by room zone**, when live loads were assigned per room (Building B). Give each zone its
    regulation clause and include one live-load plan per floor.
- **Live-load basis:** Ministerial Regulation on Structural Design, **B.E. 2566 (2023)**:
  - Clause 11 gives the minimum live loads;
  - Clause 12 requires a higher actual load where one applies (for example a water-tank area
    at 5 kPa);
  - Clauses 13 and 14 govern live-load reduction (none for parking).
- **Seismic:** the static cases (Ex/Ey or EQX/EQY) and the Loads-to-Masses combination
  `/db/ltom` (typically 1.0 DL + 1.0 SDL + 0.25 LL).
- **Load combinations:** read what is stored in the model:
  - `/db/LCOM-GEN` holds the general combinations (`<name>(CB)` in result tables);
  - `/db/LCOM-CONC` holds the concrete-design combinations (`cLCBn`, `<name>(CBC)`).

  Tabulate each combination's name, description and factors. The Regulation's combinations
  (D = DL + SDL, E = ±Ex/±Ey):
  - **Clause 7, strength:** `1.4D + 1.7L`; `0.75(1.4D + 1.7L) ± 1.0E`; `0.9D ± 1.0E`.
    Wind uses `0.75(1.4D + 1.7L) ± 1.6W` and `0.9D ± 1.6W`.
  - **Clause 6, service:** `D + L`; `D ± 0.7E`; `D ± 0.525E + 0.75L`; `0.6D ± 0.7E`.

  ⚠️ The factored gravity combination is **1.4D + 1.7L, not 1.2D + 1.6L.**

### 5.3 Section 3: Behaviour figures (see §6 for the capture code)
- **Displacement contour with the deformed shape**, D_Z, under the **service combination**
  (for example `S1` (CB) or `cLCB12` (CBC)): isometric and side views.
- Displacement contour with the deformed shape for each seismic case: D_X for Ex, D_Y for Ey.
- In the text, give the maximum values from `Result.TABLE.Displacement`.

### 5.4 Section 4: Gravity support reactions
- Totals ΣFx, ΣFy, ΣFz per load case (DL, SDL, LL) and for the service and factored
  combinations. If a combination has no result table, superpose the case results using its
  stored factors.
- A per-support table: Node, X, Y, D = DL + SDL, LL, service, factored, with a totals row.
- **Reaction-force plots with values on** (F_Z) for the service and factored combinations.
  Check that the labels add up to the table total.

### 5.5 Section 5: Lateral (seismic)
- Base shear: ΣFx under Ex, ΣFy under Ey. Maximum displacement overall and at the roof.
- **Storey drift, measured along column lines between STOREY-level nodes.**
  - For each column line (x, y), take the nodes at consecutive storey levels:
    `δe = |d_top − d_bottom|`, `ratio = δe / h`, and report the largest in each storey.
  - ⚠️ Do **not** use per-element drift. Meshed columns (Building A) are split into short
    pieces, so the per-element value is local and wrong.
- **Design drift:** `Δ = Cd·δe / I` with `Cd = 4.5` for an intermediate RC moment frame.
  - Allowable (DPT 1301/1302): `0.020·hsx` for risk categories I–II, `0.015` for III,
    `0.010` for IV.
  - Mark each row **OK** or **Exceeds**. Report the result as it is; don't hide it.

### 5.6 Section 6: ELF calculation sheet (see §7)

---

## 6. Capturing figures

Endpoint **`POST /view/CAPTURE`** returns `base64String` (decode it to PNG). Always pass
`"ACTIVE": {"ACTIVE_MODE": "All"}`, because the ACTIVE state persists in the MIDAS GUI.

```python
from midas_gen import ResultGraphic as RG
body = {"Argument": {"SET_MODE": "post",        # "pre" = geometry (no analysis needed)
                     "SET_HIDDEN": False,
                     "HEIGHT": 1050, "WIDTH": 1600,
                     "ANGLE": {"HORIZONTAL": -55, "VERTICAL": 22},
                     "ACTIVE": {"ACTIVE_MODE": "All"},
                     "RESULT_GRAPHIC": rg}}     # omit for pre/geometry
```

Build `rg`, and set the display singletons **before** building it:

| Figure | Result graphic | Options to set first |
|--------|----------------|----------------------|
| Displacement contour + deformed | `RG.DisplacementContour(typ, lc, "Max", "DZ")` | `RG.Contour(use=True)`, `RG.Deform(use=True, bRealDisp=False)` (automatic, sensible scale), `RG.Legend(use=True)`, `RG.Values(use=False)` |
| Reaction forces with values | `RG.ReactionForcesMoments(typ, lc, "Max", "FZ")` | `RG.Deform(use=False)`, `RG.Values(use=True, num_decimal=1)`, `RG.Legend(use=True)` |

`typ` is `"ST"` for a load case, `"CB"` for a general combination, or **`"CBC"` for a
concrete-design combination**. The CBC form works for both displacement and reaction plots.

**Figure captions must auto-number and feed the Table of Figures.** Use a real field, not
literal text:

```python
cp = doc.add_paragraph(style="Caption")
cp.add_run("Figure ")
fld = OxmlElement('w:fldSimple'); fld.set(qn('w:instr'), r' SEQ Figure \* ARABIC ')
r = OxmlElement('w:r'); t = OxmlElement('w:t'); t.text = str(n); r.append(t); fld.append(r)
cp._p.append(fld)
cp.add_run("  " + caption_text)
```

Also insert a Table-of-Figures field (`TOC \h \z \c "Figure"`) after the title. The reader
right-clicks it and chooses **Update Field** to build the list.

---

## 7. Seismic ELF calculation

MIDAS does **not** expose the seismic coefficients through `/db/posl`, which is empty. Read
them instead from the MCT export (`POST /doc/EXPORTMXT {"Argument": "<path>.mct"}`, which is
read-only), in the `*SEIS` block. Otherwise derive them from the standard. Always
cross-check against the base-shear reaction.

### 7.1 Parameters
- **Building A, DPT 1301/1302-64:** Samut Songkhram is in **Bangkok-Basin Zone 3**. From
  **Table 1.4-5 (5% damping)**, `S_DS = 0.262 g` and `S_D1 = 0.265 g`.
  *(Table 1.4-4 is 2.5% damping; do not use it for a normal RC building.)*
- **Building B, DPT 1301/1302-61, as entered in the model:** Ss 0.75, S1 0.30, Fa 1.2,
  Fv 1.8, giving `S_DS = 0.60 g` and `S_D1 = 0.36 g`.
- Period `T = 0.02·H` (RC, eq. 3.3-1). On the plateau (`T ≤ Ts = S_D1/S_DS`), `Sa = S_DS`.
- `Cs = Sa·I/R` (minimum 0.01), `V = Cs·W`. For an intermediate RC moment frame, `R = 5`.

### 7.2 Seismic weight per level (computed, then reconciled)
- **Beam self-weight:** `L·A·γ`, where `A = H·B` for SB sections (`vSIZE = [H, B]`). Split
  columns 50/50 between their end levels.
- **Plate self-weight:** `area·t·γ`, with the 3D polygon area from Newell's method and `t`
  from `/db/THIK`. Use `γ = 24 kN/m³`, then scale the geometric self-weight to the model's
  exact DL reaction.
- **SDL and 0.25LL:** from the `/db/PRES` items × plate area, assigned to the nearest level.
- **Back-check `I` and `W` from the analysis:** `I_implied = (V_analysis / W) · R / Sa`.
  Building B showed that MIDAS's seismic weight can **exclude the ground-floor slab level**
  (slab on ground beams, acting as the seismic base) **and the 0.25LL**:
  - `V/Cs` matched DL + SDL above GF to within 0.3%.
  - Report both the model value and the code value (W including 0.25LL), with the
    difference in %.
- **Building A check:** the DPT `V` matched the analysis base shear to within **0.4%**.

### 7.3 Vertical distribution
`Fx = Cvx·V`, with `Cvx = wx·hx^k / Σ(wi·hi^k)`. `k = 1` when `T ≤ 0.5 s`. Measure `hx` from
the seismic base. Tabulate `hx`, `DL+SDL`, `0.25LL`, `wx`, `Cvx`, `Fx` and `Vx` for each
level, with `ΣFx = V` as the check.

---

## 8. Section 7: RC member design pages

The engineer runs the design in MIDAS and exports each result page as a BMP. There are two
kinds:
- **MIDAS GEN NX strength-checking pages** (`B10000.bmp`, `C10000.bmp` …): one page per
  section.
- **MIDAS Design+ summaries** (`Summary_RC_<Beam & Girder|Column|Footing>_<name>_<nn>.bmp`):
  several pages per member.

They sit in `…\calculation report\<Building>\Beam | Column | Footing\`.

1. **Convert BMP → PNG** (`Image.open(f).convert("RGB").save(png, optimize=True)`). A 23 MB
   A4 BMP becomes a 0.2–0.3 MB PNG.
2. **Identify each single page before captioning.** Crop the "Design Information" band
   (about 13–20% of the page height), stitch the crops into one image and read off the
   section name and number. Take Design+ names and page numbers from the filename regex
   `Summary_RC_(Beam & Girder|Column|Footing)_(.+?)(?:_(\d+))?$`.
3. **Lay out one page per figure**: page break, picture 5.9 in wide, caption.
   - Captions: `RC beam strength check – GB1 250×800 (section 201)`,
     `Column design summary – C1 300×450 (GF) (page 2 of 5)`.
   - Group the pages under `7.1 Beams`, `7.2 Columns`, `7.3 Footings`.
4. Open Section 7 with one paragraph stating:
   - the design code and software for each page type (GEN NX pages versus Design+ pages can
     differ, e.g. ACI 318M-19 vs ACI 318M-14);
   - the combinations used;
   - the materials.

   Optionally add a table of the rebar input per section, parsed from the `*REBAR-BEAM` and
   `*REBAR-COLUMN` blocks of the MCT export.

---

## 9. Build, verify, deliver

1. Copy the template, clear the body and fix the `sectPr` header/footer (§3).
2. Write the content with the named styles (§4), figures with SEQ captions (§6), and a TOF
   field.
3. **Verify the output programmatically** before delivering:
   - the `Normal` font is `TH SarabunPSK`;
   - there is no Thai text in an English-only report (regex `[\u0e00-\u0e7f]` over
     paragraphs and table cells);
   - the `SEQ Figure` field count equals the number of figures;
   - the key numbers match the model: base shear, DL/SDL/LL totals, factored total.
4. Save as `…\calculation report\<Building>\Structural Calculation Report - <Building>.docx`.
   If the previous file is open in Word, the save throws `PermissionError`; write a new
   filename (`_v2`, …).

Reference scripts (scratchpad, 2026-09):
- **Data extraction:** `extract_B.py`, `extract_A.py`, `drift_A.py`.
- **Figures:** `capture_B.py`, `capture_A.py`.
- **ELF:** `compute_elf_B.py`, `compute_elf.py`.
- **Report builders:** `build_report_B.py`, and `build_report_A.py`, which reuses B's helpers.
- **Live-load plans:** `ll_plot.py` (`--en` for the English version).

---

## 10. Gotchas

**Model access**
- **No analysis results:** run `/doc/ANAL` first.
- **The connection drops after save-as or reopen:** do `Apps → Connect` again.
- **⚠️ Never use `/doc/IMPORTMXT` on a live model.** It **replaced the whole open model** with
  a partial MCT file: 5,120 nodes became 0. Its reply says "command complete" even when
  nothing was applied, and a full-MCT restore through the API did not apply either. Treat
  MCT import as a GUI-only action on a saved copy. `EXPORTMXT` is safe.
- **`/db/RCHK` (rebar for checking) returns 404** in this GEN NX build. Rebar is entered in
  the GUI; read it back from the MCT export.

**Seismic**
- **`/db/posl` is empty.** Take the seismic parameters from the MCT `*SEIS` block, or from
  DPT, and verify them against the base-shear reaction.

**Results and figures**
- **Drift on meshed columns:** measure between storey-level nodes on each column line, not
  per element.
- **Concrete-design combinations** appear as `(CBC)`. `RESULT_GRAPHIC` accepts
  `typ = "CBC"`.
- **Caption style ≠ automatic figure table.** The template TOF keys on `SEQ Figure` fields.

**Word output**
- **Complex-script font:** set the `w:cs` font on runs, or Thai falls back to another font.
- **Section loss:** keep the final `sectPr`; it holds the header reference.

**Loads**
- **Factored gravity is 1.4D + 1.7L** (Ministerial Regulation B.E. 2566, Clause 7), not
  1.2/1.6.

**Tools**
- **PDF reading:** poppler is absent; use PyMuPDF `fitz` (`get_text` and page render). Thai
  text in some PDFs extracts garbled, so render those pages and read them visually.

---

## 11. MAPI quick reference

| Endpoint / call | Purpose |
|-----------------|---------|
| `POST /doc/ANAL` | run the analysis |
| `Result.TABLE.Reaction(loadcase=["DL(ST)"])` | base reactions (kN); `U1(CB)` for a general combination |
| `Result.TABLE.Displacement(loadcase=[...])` | nodal displacements (m) |
| `POST /view/CAPTURE` | geometry / result figure (base64 PNG) |
| `POST /doc/EXPORTMXT {"Argument": path}` | read-only MCT export (`*SEIS`, `*REBAR-*`, `*DGN-*`) |
| `/db/NODE`, `/db/ELEM`, `/db/SECT`, `/db/THIK`, `/db/MATL`, `/db/MATD` | geometry, properties, design materials |
| `/db/STOR` | storey schedule |
| `/db/ltom` | Loads-to-Masses (seismic weight combination) |
| `/db/PRES` | plate pressure loads (SDL, LL): `FORCES[0]` = uniform value |
| `/db/LCOM-GEN`, `/db/LCOM-CONC` | general / concrete-design load combinations |
| `/db/DCON` | RC design code |
| `/db/posl` | seismic parameters (**usually empty**, see §7) |

Related notes: `docs/MIDAS_MAPPING.md`, `docs/SPEC.md`.
