# Nooker Retaining Wall: Handover & Reproduction Guide

**Drawing set:** NRW-ST, 7 sheets, A3, stage **D** (draft final), revision **A**, "ISSUED FOR APPROVAL", dated 28/09/2026.
**Status:** for client and local-authority approval. **Not for construction.**
**Purpose of this document:** anyone who picks up this job can understand the design, regenerate the drawings exactly as issued, and make the next revision in the same style.

---

## 0. Document map (read in this order)

| # | Document | Location | What it covers |
|---|---|---|---|
| 1 | **This README** | `902 Structural Drafter\jobs\nooker_rw\README.md` (copy: `Drawings\NRW-ST_Handover_README.md`) | Design basis, geometry, reinforcement, sheet contents, how to build, plot and revise, open items |
| 2 | `DRAWING_STANDARD_EIT-011006-19.md` | repo root | EIT 011006-19 drafting standard in full, plus the project deviations in §19 |
| 3 | `NRW-ST_Linetype_and_Lineweight_Guide.md` | `Drawings\` | CAD setup: units, linetypes, layers, pens, text and dimension styles, hatches, CTB, plotting, reinforcement drawing conventions |
| 4 | `ANNOTATION_ALIGNMENT_GUIDE.md` | repo root (copy in `Drawings\`) | Where and how notes, leaders, terminators and titles are placed, and the annotation engine |

| File | Location | Role |
|---|---|---|
| **Source copy** | `G:\My Drive\Works\##2026\20260928 - Nooker RW\Source\` | Snapshot of the three scripts + this README exactly as used for Rev A (the job folder is self-contained) |
| `build_rw.py` | `jobs\nooker_rw\` | Generates the whole set as one DXF: geometry, notes, layouts and viewports |
| `plot_rw.py` | `jobs\nooker_rw\` | Builds the CTB, plots every layout via AutoCAD, saves the DWG, merges the PDF |
| `calc_rw.py` | `jobs\nooker_rw\` | Design checks: stability, flexure, shear, anchorage, minimum steel |
| `NRW-ST_Retaining_Wall_A3_RevA.pdf / .dwg / .dxf` | `G:\My Drive\Works\##2026\20260928 - Nooker RW\Drawings\` | Issued set |
| `NRW-EIT.ctb` | same `Drawings\` folder | Plot style; required to plot the DWG correctly |
| `RW.pdf` | job root | Original client sketch (input, superseded) |
| `RW-1_Structural_Drawings_A3_RevB.pdf` | job root | Earlier RW-1 set by others. **Superseded — withdraw; do not issue.** |

---

## 1. Project and origin

- **Client sketch (RW.pdf):**
  - L-shaped cantilever wall retaining **0.60 m max.** of fill;
  - stem 200 thick, no toe, heel under the fill;
  - "DB12@200 EF", a weep pipe discharging onto the neighbour, no cover, no joints.
- **Review findings that drove the redesign:**
  - the footing width was mislabelled (shown as 200, drawn about 820);
  - no cover or blinding;
  - sliding failed under vehicle surcharge;
  - weep water drained onto the adjacent land;
  - the hook did not fit a 200 mm footing;
  - the exposed face had no crack-control steel;
  - no movement joints.
- **Decisions confirmed by the client (28/09/2026):**
  1. **Surcharge:** vehicles / driveway → 10 kPa.
  2. **Boundary:** the front face of the wall is on the property line. No weep holes; a subsoil drain goes to the owner's drainage.
  3. **Section:** revised per the review (footing 250 thick, founding at −0.400/−0.450, lean concrete, exposed-face bars, chamfers).
  4. **Wall length:** "typical, length varies": a typical 24 m panel is shown, and joints are set out on site.
  5. **Numbering:** a new independent set numbered to EIT (NRW-ST-…). RW-1 Rev B is to be withdrawn.

---

## 2. Design basis (sheet 1001 notes 2–3)

| Item | Value |
|---|---|
| Codes | Building Control Act B.E. 2522 (as amended); RC design **EIT 1008-38** strength design, **U = 1.7 H** on earth pressure and surcharge; development, hooks and laps **ACI 318-19** |
| Retained height | 0.60 m max. above adjacent ground; design height **H = 1.00 m** (top of wall +0.600 to founding −0.400) |
| Soil | γ = 18 kN/m³; **K0 = 0.50** (compacted backfill, at-rest); base friction μ = 0.40; passive resistance at the shear key only: 0.5 Kp, Kp = 3.0 |
| Surcharge | **q = 10 kPa** uniform, retained side (cars / pick-ups). No trucks or plant within 1.5 m. |
| Bearing | qa ≥ 50 kPa at −0.450. **To be verified on site.** |
| Groundwater | Below −0.700; wall designed as fully drained |
| Seismic | Not considered (retained height ≤ 1.0 m) |
| Concrete | fc' = 240 ksc (24 MPa) cylinder |
| Steel | SD40 (fy 390 MPa) DB10/DB12; SR24 RB16 dowels |

### 2.1 Results (`python calc_rw.py`)

Values are per metre run.

| Check | Result | Limit |
|---|---|---|
| Lateral H = ½K0γH² + K0qH | 4.50 + 5.00 = **9.50 kN** | – |
| Vertical V (stem + footing + key + soil on heel) | 26.10 kN (36.10 with q on heel) | – |
| Overturning Mr / Mo | 16.06 / 4.00 = **4.02** | ≥ 2.0 |
| Sliding (μV + Pp)/H, Pp = 4.45 kN over the key | **1.57** | ≥ 1.5 |
| Sliding, drain blocked (full water, accidental) | **1.03** | ≥ 1.0 |
| Bearing qmax (resultant in middle third, e = 0.072–0.138 < B/6 = 0.200) | 36.7–**40.9 kPa** | ≤ 50 (verify) |
| Stem at footing, hs = 0.75 m | Mu = 3.47 ≤ φMn = 29.5 kN·m/m; Vu = 10.7 ≤ φVc = 96.2 kN/m | – |
| Heel cantilever (w = 29.5 kPa, L = 1.0 m, no upward bearing) | Mu = 25.1 ≤ φMn = 37.4 kN·m/m; Vu = 40.4 ≤ φVc = 121.2 kN/m | – |
| Hook of (1) into footing, ldh (ψr = 1.0, spacing ≥ 6db) | required 150, available **176** (T.O.F. to outside of bend) | – |
| Class B laps (1.3 ld) | DB10 493 → **500**; DB12 591 → **600** | – |
| Minimum steel | stem horiz. 958 ≥ 500; vert. 761 ≥ 300; footing 1130 ≥ 500 mm²/m | – |

---

## 3. Geometry (all mm; levels in m to site datum)

**Datum ±0.000** = existing ground of the adjacent land at the wall line. Origin for the section: x = 0 at the exposed face (= property line), +x into the fill.

| Element | Value | Constant in `build_rw.py` |
|---|---|---|
| Stem thickness | 200 | `TS` |
| Top of wall | **+0.600** (= max. fill level) | `TOW` |
| Top of footing (construction joint) | **−0.150** | `TOF` |
| Bottom of footing | **−0.400** | `BOF` |
| Footing width / thickness | 1200 / 250 | `B`, `TF` |
| Lean concrete | 50 thick, bottom at **−0.450** (founding level) | `LEAN` |
| Shear key | 250 wide × 300 deep at the heel end (x 950–1200); bottom **−0.700** | `KB`, `KD`, `KX0`, `KBOT` |
| Drainage stone | 300 wide behind the stem, from T.O.F. to +0.300 | `DRN_W`, `DRN_TOP` |
| Subsoil drain | PVC Ø100 (OD 114), centre at x 350, 20 above T.O.F. | `PIPE_C`, `PIPE_R` |
| Chamfer | 20×20 on exposed edges | `CH` |
| Excavation (retained side) | 150 working space at −0.450, then **2:1 (V:H)** up to existing ground ±0.000 (top of cut x = 1575) | `EXC_WS`, `EXC_V`, `EXC_H` |
| Adjacent land | not excavated below −0.450 without the engineer's approval | note 6.1 |

**Clear cover:**
- 40 on both stem faces;
- 50 on top of the heel and on lean concrete;
- **75 cast against earth** (footing ends, shear key).

At the boundary, where forms can't be stripped, permanent fibre-cement formwork keeps the 40 cover; otherwise provide 75.

### 3.1 Joints

| Joint | Spacing / location | Detail |
|---|---|---|
| **E.J.** expansion, 20 gap, full section incl. key | ≤ 24.0 m; at corners, wall ends against other structures, changes of direction or height | 1/5002 |
| **C.J.** contraction, tight, bond breaker | ≤ 6.0 m, equal bays between E.J.; alternate-bay casting, ≥ 48 h | 1/5003 |
| Construction joint | horizontal at T.O.F. −0.150 only, roughened 5 mm (zig-zag symbol) | A/5001 |

- **Dowels:** RB16 SR24 L = 600 @300, sleeved and greased on one side; the E.J. adds a 25 void end cap.
- **Dowel positions:** 2 in the stem centre line at +0.450 / +0.150; 4 in the footing at −0.275, positioned at x 150, 450, 750, 1050.
- **Sealants:** E.J. PU sealant 20×14 on a Ø25 backer rod; C.J. sealed groove 16×15.
- **Geotextile strip:** 500 wide (E.J.) or 300 wide (C.J.), bonded one side only.

---

## 4. Reinforcement (Rev A)

| Mark | Bar | Description | Shape (out-to-out) | Planes / spacing |
|---|---|---|---|---|
| (1) | DB12@200 | Stem vertical, **soil face** (outer layer), top leg 100 to the front, 90° hook, **tail 300 seated on (6)**, no laps | Z: A100 B885 C305 | 50 + 200n from joint face |
| (2) | DB12@200 | Stem horizontal, soil face, inside (1): 4 levels at −0.075, +0.125, +0.325, +0.525 | straight 5900 | – |
| (3) | DB10@400 | Stem vertical, **exposed face**, tail 200 | Z: A100 B860 C205 | 100 + 400n |
| (4) | DB10@200 | Stem horizontal, exposed face, inside (3), same 4 levels | straight 5900 | – |
| (5) | DB12@200 | Footing **C-bar closed at the toe**: top and bottom legs, toe return at 75 cover, straight ends at x = 1105 | C: A1030 B150 C1030 | 150 + 200n |
| (6) | 6+6-DB12 | Footing longitudinal T & B inside (5), x = 102, 300, 500, 700, 900, 1100 | straight 5900 | – |
| (7) | DB12@200 | Shear key U-bar, legs up to −0.250 into the footing cage | U: A375 B100 C375 | 50 + 200n |
| (8) | 2-DB12 | Shear key longitudinal, in the U bottom | straight 5900 | – |
| (9) | 4-DB12 per corner | Corner L-bar, soil face, at the levels of (2), lap 600 | L: 750 × 750 | – |
| (10) | 4-DB10 per corner | Corner L-bar, exposed face, lap 500 with (4) | L: 650 × 650 | – |
| (11) | 4-DB12 per free end | Free-end U-bar (horizontal), lap 600 with (2)/(4) | U: A605 B100 C605 | – |
| (D) | RB16 SR24 | Slip dowel L = 600: 6 per joint (2 stem + 4 footing) | straight 600 | @300 |

**Bar centreline coordinates (section, mm):**

| Bar or layer | Coordinate |
|---|---|
| (1) soil-face vertical | x = 154 |
| (3) exposed-face vertical | x = 45 |
| (2) soil-face horizontal | x = 142 |
| (4) exposed-face horizontal | x = 55 |
| (1) top leg | z = 554 |
| (5) C-bar top leg | z = −206 |
| (5) C-bar bottom leg | z = −344 |
| (6) longitudinal, top / bottom | z = −218 / −332 |
| (1) tail | z = −320 |
| (3) tail | z = −309 (own plane) |
| (7) key U-bar legs | x = 1031 / 1119, bottom z = −619 |

- **Bends:** 6 db mandrel; drawn at R = 3.5 db on the centreline.
- **Stock:** 10 m bars; no bar is longer than 6.0 m.
- **Weight:** about **231 kg per 6 m bay (38.6 kg/m)**. Full schedule on 1/5005.
- **Corners:** the corner block (1200 × 1200) is cast with leg A, and the E.J. in leg B sits on the line of the leg A heel. Leg A C-bars and longitudinal bars run through; leg B C-bars are placed at 90° (a two-way cage).
- **Free end:** U-bars (11) with 2 end verticals of shape (1) **inside the U-bend** (tied).

---

## 5. Sheet-by-sheet contents

Sheet number format **`NRW-ST-<series>-D-A`** (EIT 011006-19 Ch. 4: project, discipline, series, stage, revision). Every sheet has the A3 frame, zone grid, title strip, revision table, key plan and "FOR APPROVAL / NOT FOR CONSTRUCTION" stamp (§7).

| Sheet | Title | Views (scale, viewport size in paper mm) | Other content |
|---|---|---|---|
| **1001** | General notes, design criteria & legend | none (N.T.S.) | Notes 1–8 in three 100 mm columns; design summary table (note 3); line legend; abbreviations; drawing list |
| **3001** | Typical plan & longitudinal elevation | 1 Typical plan, joint layout, 1:100 (290 × 66); 2 Longitudinal elevation from adjacent land, 1:100 (301 × 33); 3 Partial elevation at E.J., 1:25 (160 × 90) | Layout notes; joint schedule (E.J. / C.J. / construction) |
| **5001** | Section A, typical wall section | A Section 1:10 (318 × 208) | Reinforcement key (1)–(8); bar-drawing convention note; cover in the view title |
| **5002** | Expansion joint details | 1 E.J. plan section at +0.300, 1:5; 2 Slip dowel, 1:5; 3 E.J. sealant, 1:2 | E.J. installation notes 1–6 |
| **5003** | Contraction joint & joint plane | 1 C.J. plan section at +0.300, 1:5; 2 Joint plane, view on joint face, 1:20; 3 C.J. sealed groove, 1:2 | C.J. installation notes 1–4; joint-plane note |
| **5004** | Corner & wall end details | 1 Typical corner plan at +0.300, 1:20; 3 Wall free end plan at +0.300, 1:20; 2 Corner block footing plan at −0.275, 1:25 | Corner and end notes 1–6 |
| **5005** | Reinforcement schedule & bar planes | 2 Bar planes from a joint face, plan, 1:10 | 1 Bar schedule per 6.00 m bay + additional bars (per corner / free end / joint); schedule notes; fixing reference |

**Section A shows**, left to right:
- **Boundary side:**
  - adjacent ground ±0.000 with a soil band;
  - level marks (+0.600, ±0.000, −0.150, −0.400, −0.700);
  - height dimension chain on the level lines;
  - the left note column.
- **The wall itself:**
  - chamfers;
  - the stem with (1)–(4);
  - the zig-zag construction joint;
  - the heel with the C-bar (5) and longitudinal bars (6);
  - the shear key with (7) and (8);
  - lean concrete and compacted subgrade.
- **Retained side:**
  - the drainage stone zone (gravel hatch) with the pipe and geotextile;
  - selected fill (AR-SAND stipple) to +0.600, with the surcharge arrows;
  - the 2:1 excavation with the slope triangle and break line;
  - the right note column.
- **Bottom:** dimensions 200 / 750 / 250 and the 1200 overall.

---

## 6. Reproducing the set

### 6.1 Prerequisites (Windows)

| Item | Version / note |
|---|---|
| Python | 3.11 with **ezdxf 1.4.x**, **PyMuPDF (fitz)**, **fontTools** (`pip install ezdxf pymupdf fonttools`) |
| AutoCAD | **2024**. `accoreconsole.exe` is used for plotting. Needs `DWG To PDF.pc3` and `monochrome.ctb` (standard). |
| Fonts | `C:\Windows\Fonts\ARIALN.TTF`, `ARIALNB.TTF` (Arial Narrow). The engine measures text with them. |
| Shell | **PowerShell** (or Python subprocess). `accoreconsole` does **not** run scripts when launched from Git Bash. |

### 6.2 Build and plot

```powershell
cd "C:\990 - Developing software\902 Structural Drafter\jobs\nooker_rw"
$o = "C:\temp\rwout"            # any empty output folder
python build_rw.py $o           # -> $o\NRW-ST_Retaining_Wall_A3_RevA.dxf (prints viewport sizes; "!!" = view overflows sheet)
python plot_rw.py  $o           # -> NRW-EIT.ctb, $o\...RevA.dwg, $o\...RevA.pdf (7 pages)
python calc_rw.py               # design check printout
```

Then copy `…RevA.pdf/.dwg/.dxf` and `NRW-EIT.ctb` into the job `Drawings\` folder.

**`plot_rw.py` does the following, in order:**
1. Writes `NRW-EIT.ctb`: AutoCAD's `monochrome.ctb` with ACI 8 screened 50 %. It saves it next to the output and into `%APPDATA%\Autodesk\AutoCAD 2024\*\*\Plotters\Plot Styles`.
2. Writes `_plot.scr` with **exact CRLF** line endings.
3. For each layout (`1001, 3001, 5001, 5002, 5003, 5004, 5005`): `-PLOT` with DWG To PDF.pc3, ISO full bleed A3, landscape, layout area, 1:1, `NRW-EIT.ctb`, object lineweights, and the page setup saved.
4. Turns the plot stamp off, then runs `SAVEAS 2018` to the DWG and `QUIT`.
5. Merges the per-layout PDFs into one file.
6. Writes a log to `_plot.log`.

### 6.3 Known pitfalls (all handled in the scripts; keep them)

| Pitfall | Handling |
|---|---|
| A stray `\r` in the script acts as Enter and repeats the last command, so the console hangs | Script written as bytes with exact CRLF |
| `SAVEAS` stops at the overwrite prompt | Existing DWG deleted first |
| The console hangs forever when a prompt answer is wrong | 300 s timeout; check `_plot.log` for the last prompt |
| A CTB built from scratch by ezdxf plots in colour | CTB derived from AutoCAD's own `monochrome.ctb` |
| `$MSLTSCALE` is rejected by ezdxf | Not set in the DXF; set in the plot script instead |
| ezdxf under-measures multi-line MTEXT extents | The engine adds true text boxes to the view extents |

### 6.4 Verify after every build

1. Build output has **no `!!` lines** (every viewport inside the drawing area x 20–340, y 10–287).
2. The PDF has 7 pages, each 420 × 297 mm.
3. Rasterise and inspect at print size. Minimum check list: `ANNOTATION_ALIGNMENT_GUIDE.md` §8.
4. `calc_rw.py` results match sheet 1001 note 3.

---

## 7. Sheet furniture (paper mm)

| Item | Value |
|---|---|
| Sheet / frame | 420 × 297; frame 20 left, 10 elsewhere (EIT A2–A4); frame pen 0.70 |
| Zone grid | 8 columns (1–8) × 6 rows (A–F) in the margin, both sides; ACI 8, 0.18 |
| Title strip | right side, **70 wide** (x 340–410), full height |
| Title strip, bottom to top | approved-by row (7); designers + drawing no. / sheet / scale / date (32); drawing title (20, 2.8 bold); design office (18); project (20); owner (14); local authority approval + stamp (20); owner / client approval (16); revision table (5 rows × 5 mm: REV / DESCRIPTION / DATE / SIGN); key plan (32); status stamp (12); sheet notes 1–4 at the top |
| Placeholders to fill | `[ OWNER NAME ]`, location, `[ DESIGN OFFICE NAME ]`, address, key plan, designer / checker / engineer names, **COE licence no.**, signatures, permit no. |
| Drawing area | x 20–340 (320 wide), y 10–287 |
| View title | 2.8 mm bold, underlined, left-aligned with its view, 6 mm below it; "SCALE 1:n" below; split bubble (view ID / sheet), with triangles for sections |

Project data is in the `PROJ` dict at the top of `build_rw.py`. Change it there, never in the DWG.

---

## 8. How to make the next revision

1. **Set the new revision and stage** in `PROJ`:
   - `rev` = `"B"` (internal changes before resubmission: `B1`, `B2`; tender issue: `00`; after tender: `01`, `02`);
   - `stage` = `"T"` for tender or `"F"` for construction.
2. **Add a row to `revs`** in `title_block()` with the description and date. Keep the earlier rows.
3. **Output file names:** the file base name in both scripts contains `RevA`. Update `DXF` in `build_rw.py` and `BASE` in `plot_rw.py`.
4. **Geometry:** change it through the constants in §3 / §4. Bar positions, the bar schedule and the bar-plane view derive from them.
   - After changing a bar, check the schedule on 5005 and the key on 5001.
   - If design values change, re-run `calc_rw.py` and update sheet 1001 note 3 (the `rows` in `sheet_1001`).
5. **Notes:** add them via `leader()` in the view function. Never place text by hand; the engine lays them out (see the annotation guide §7).
6. **Rebuild, plot and verify** (§6.4). Move the "FOR APPROVAL" stamp text to "FOR CONSTRUCTION" only after the permit is granted.
7. **Cloud revised areas:** revision clouds are not automated yet; add them in AutoCAD on a copy if the authority requires them.

---

## 9. Open items and assumptions (must be closed before "FOR CONSTRUCTION")

- [ ] **Site verification:**
  - allowable bearing ≥ 50 kPa at −0.450;
  - soil parameters γ 18, K0 0.50, μ 0.40;
  - groundwater below −0.700.
- [ ] Surveyed property line; the front face of the wall is on it.
- [ ] **Title block placeholders:** owner, location, design office, key plan, names, COE licence, signatures.
- [ ] **Standard editions:** confirm the TIS numbers (24, 20, 213, 15, 2594, 733, 409, 17) and DOH test methods (DH-T 107, 108, 603), and whether a newer EIT 1008 edition applies.
- [ ] Data sheets for the materials without a TIS (geotextile, joint filler, PU sealant, backer rod).
- [ ] Wall length and alignment from the site plan; joints set out from ends and corners.
- [ ] **Calculation sheet:** a รายการคำนวณ for the authority, if requested, based on `calc_rw.py`.
- [ ] **RW-1 Rev B:** withdraw it so two sets don't circulate.

---

## 10. Change history (Rev A development, 28/09/2026)

1. **Base drawing:** review of RW.pdf, redesign, and the first set (6 sheets, EIT format, Arial Narrow 2.0 / 2.8).
2. **Linetype guide review:** EIT A2 pens used unreduced; cut 0.35 / seen 0.25; ACI 8 grey via `NRW-EIT.ctb`; PLINEGEN; `EIT_*` linetypes.
3. **Reinforcement guide review:**
   - filleted bars (R = 3.5 db);
   - true-width strips at 1:5;
   - outline dowels;
   - closed C-bar footing;
   - bar marks with bubbles;
   - alternate bar planes;
   - corner-block cage;
   - new sheet **5005** (bar schedule).
4. **Annotation engine:** aligned note columns and rows; ordered notes; no crossings.
5. **Terminators:** 2 mm filled arrows; open circle Ø = 2 × bar dot on cut bars; arrows (not dots) on bars along their length.
6. **Leaders:** 45° / 60° standard legs + horizontal run; zig-zag construction joint.
7. **Arrow tips** on object edges (never inside black fills); selected-fill hatch; excavation; free-end bars moved inside the U-bend; corner dots cleared.
8. **Final changes:** excavation **2:1 (V:H)**; dimension terminators **filled 2 mm arrows**; extension lines **ACI 8 grey**.
