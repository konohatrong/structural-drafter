# Jobs: worked examples

Each folder is a complete drawing set built by script with the rules in `docs/`. The jobs are kept as **examples of
what has been done**, and as the record of how the rules were developed. Most rules in `docs/` came from a review of
one of these sets.

Use a job to:
- **copy a pattern**: the closest job is the starting point for a new set (engine module, view functions, sheet
  functions, tables, notes);
- **see a rule applied**: the docs cite a job's sheet as a worked example ("1/5004", "Section A on 5001");
- **understand why a rule exists**: the job's README or development notes record the review comment behind it.

The office standard sets built here (general notes, typical details) are published to `standard_drawings/`:
`developing/` for review copies, `issued/` for official revisions. Other generated output (`out/`, `library/`) is
not in the repository. Rebuild it with the commands in
`docs/general/DRAWING_PRODUCTION.md` §5.

## 1. Catalogue

| Job | Structure | Status | What it shows | Read first |
|---|---|---|---|---|
| `steel_portal_frame` (SPF-ST, 8 sheets, **A1**) | **Steel**: 26 x 90 m portal-frame building with tapered members, canopies, roof monitor, gable frames and roof bracing, from a live MIDAS GEN NX model | For review (Rev A) | A set driven by the analysis model: read-only MAPI snapshot (`pull_model.py`), connection design from the model's design forces (DG4 / DG16 end plates with the column side, DG29 bracing ends), proposed secondary framing, A1 office sheets (`td_engine.use_paper`) | `steel_portal_frame/README.md` |
| `steel_roof_truss` (SRT-ST, 6 sheets) | **Steel**: 25 m CHS Pratt roof truss with bearings, splices, loose diagonal and fly bracing | For review (Rev A) | Calc-driven steel set: AISC 360-16 / DG24 design in the calc, generated piece marks, AWS weld symbols and branch weld zones, bills, camber, anchor rods, erection notes, orthogonal leaders, detail callouts | `steel_roof_truss/README.md` |
| `standard_set_R2` (STR-ST 11xx) | **Concrete**: typical details, columns 1101 – 1104, beams 1111 – 1116, slabs 1121 – 1128 | **Issued** F-A (ISSUED FOR USE, 03/10/2026); changes only by revision | N.T.S. typical details from one member catalogue, model-space blocks, pens by colour, numbered tables, focus rule, clean dimensioning, leader form per target | `standard_set_R2/MODEL_SPACE_SHEETS.md` (R2 rules and history) |
| `nooker_rw` (NRW-ST, 7 sheets) | **Concrete**: cantilever retaining wall with joints, corners and bar schedule | **Issued** (Rev B); change only by revision | A complete project set with its design calc (`calc_rw.py`); the origin of the annotation engine and the office conventions | `nooker_rw/README.md` |
| `standard_set` (STR-ST 1001 – 1003, R1 11xx) | **Concrete**: general notes; typical details R1 | General notes **issued** F-A (ISSUED FOR USE, 03/10/2026); R1 details **frozen** | The first model-space set from blocks; general notes flowing over sheets at the normal text size | `standard_set/MODEL_SPACE_SHEETS.md` |
| `general_notes` (STR-ST-1001 Rev A) | **Concrete** general notes, one sheet | Superseded by the notes in `standard_set` (issued F-A) | The Rev A notes sheet (× 0.625 sizes, one sheet, balanced band), replaced by Rev B (normal sizes, flowing sheets) | `docs/general/GENERAL_NOTES_DRAWING_INSTRUCTION.md` |
| SSK (outside the repository: `G:\My Drive\Works\20260318 - Samutsongkram Building Office\Drafter`) | **Concrete**: 4-storey office building 2, floor plans (real project, client files) | Started 04/10/2026; floor-plan drafting study, level by level | AR overlay check: both sets brought to grid coordinates (grid fit from the bubbles), structural plan drawn over the architectural plan, automated grid / level / column checks, numbered findings and report | its `README.md` |
| BANWA2 (outside the repository: `D:\Workspace\##Satobkk\##2026\20261005 BANWA 2\Drafter\plans`) | **RC frame + steel roof trusses**: 70 x 87 m factory extension, structural plans S-102 - S-105 (2nd floor, column top / RC roof, truss bottom-chord bracing, purlins) and the roof trusses S-201 - S-206 (key sections 1:200, elevations 1:50, welded joint details 1:10 / 1:1, bill of materials), A1 on the Sato Kogyo title block, from a live MIDAS GEN NX model (real project, client files) | Rev A for review (06 - 07/10/2026) | Plans driven by the analysis model with the AR levels where the model is simplified; beams as one member per column bay with length brackets; truss marks per support span by section consistency; steel in plan as double lines at projected width; key sections leading to typical elevations with the adjacent spans hidden; joints from a concentric model (one WP offset per type); posts through the trusses with the purlins beside them; a bill of all the steel with weight per area; a project title block mapped onto the engine's attribute tags in job code | its `README.md` |
| `stair_demo` (ST-1, 1 sheet) | **Concrete** stair | Demonstration | Stair views, flight bar shapes, fixed leaders in the empty triangles | `docs/concrete/STAIRCASE_DRAWING_INSTRUCTION.md` |
| `typical_details` | **Concrete** typical details, first version | **Superseded**, kept unchanged | Paper-space viewports, the first `stirrup` / `crosstie` helpers | – |

## 2. What each job taught (rules it produced)

| Job | Rules that came from it | Where they are now |
|---|---|---|
| `nooker_rw` Rev A (2026-09-28) | Aligned note columns and rows, ordered notes, no crossings; 45° / 60° legs + shelf; terminators (arrows on edges, rings on cut bars); EIT pens unreduced on A3, cut 0.35 / seen 0.25, grey ACI 8; Arial Narrow 2.0 / 2.8; filleted bars, true-width strips, bar-mark bubbles; zig-zag construction joint; 2:1 excavation | guide §1 – §8; EIT §19.1 – §19.3, §19.6; RC §19.4 |
| `nooker_rw` Rev B (2026-10-03) | Top-bar factor ψt for laps in walls cast in one lift | Job README §10 |
| `general_notes` / `standard_set` gn (2026-09-29) | Notes-sheet sizes; Rev B notes at the normal size flowing over sheets; keep-with-next headers; numbered tables | `GENERAL_NOTES_DRAWING_INSTRUCTION.md` §0 |
| `standard_set` R1 (2026-09-29) | Model space at real size with detail blocks; the block library; clean dimensioning (tier order, `tside`, `check_dims`) | `docs/general/DRAWING_ENGINE.md`; `standard_set/MODEL_SPACE_SHEETS.md`; guide §2.4.1 |
| `standard_set_R2` (2026-09-30) | N.T.S. with one member catalogue; pens by colour; acadiso linetypes and the PSLTSCALE / CTB pitfalls; one table sequence "TABLE n - NAME"; units in notes; leader form per target; focus rule; plain bar ends and cranked laps; slab-on-ground and fill details after the Beca review | `docs/general/DRAWING_ENGINE.md`; `standard_set_R2/MODEL_SPACE_SHEETS.md`; RC §19.7; `standard_set_R2/REVIEW_BECA_SLAB.md` |
| `steel_roof_truss` (2026-10-03) | The steel instruction S1 – S11 and S9A; orthogonal leaders with a real second leg; tags beside members; bolt rings 1.25 × hole; arrows on plate edges; units on every bare number (all drawings); hidden parts and wall lines trimmed at breaks; grey centre marks; dashed detail callouts; labels written on the member; the annotation guide made structure-neutral | `docs/steel/`; guide §2.1, §2.4.2, §9 |
| `steel_portal_frame` (2026-10-04) | Drawings driven by a live MIDAS GEN NX model through a read-only snapshot (never the key in a file); A1 sheets on the shared engine with the office plot style (`use_paper`); DG4 thick-plate end plates expose thin column flanges at the knee; rafter top flanges kept in one roof plane; model findings reported to the engineer, not "fixed" in the drawings | `docs/general/DRAWING_ENGINE.md` §6; `midas/MIDAS_GEN_NX_INSTRUCTION.md`; `docs/steel/reference/SOURCES_STEEL_DETAILING.md` Parts F - I |
| `steel_portal_frame` review (2026-10-04) | Plates on a tapered flange were drawn plumb or with level ends, and the drawn column taper stopped at the model work point (a kink under the knee plate): plates now follow the face, with square ends and bolts, and the flanges run straight to the cap. One thickened knee flange with CJP splices replaced by a shop column head CH1 (both flanges thick) on a bolted end-plate splice CS1, placed with bolting room under the sloping continuity plate | `docs/steel/STEEL_DETAILING_INSTRUCTION.md` S2.9, S7.7, S10 |
| SSK (2026-10-04, outside the repository) | A1 project sheets plot with `STRUCT-A1-A2.ctb` at LTSCALE 45; other disciplines' backgrounds on colour 9; the font is a project setting (SSK `cordia.shx` 0.90, 2.00 mm); the floor-plan instruction FP0 – FP19 written before drafting, from the office's own SSK file and the SSK review (stale title-block text, copied levels, pasted old AR plans, colliding bubbles); the AR overlay check | EIT §19.1, §19.2; `docs/general/FLOOR_PLAN_DRAWING_INSTRUCTION.md` |

| BANWA2 plans (2026-10-06, outside the repository) | Main beam marked once per column bay with a length bracket; opening X on the grid linetype in grey; no moment-release symbols on plans; steel framing as double lines at projected width, posts as their actual section; truss marks per support span, shared only by spans of the same length and sections; tags cut the member lines (a wipeout did not plot in AutoCAD's PDF) | `FLOOR_PLAN_DRAWING_INSTRUCTION.md` FP9.1, FP9.2, FP9.4, FP10.2, FP10.5; `STEEL_DETAILING_INSTRUCTION.md` S3.7, S4.11 |
| BANWA2 truss details (2026-10-06, outside the repository) | Continuous trusses: a 1:200 key section of every truss line, each span's split bubble (mark / sheet) leading to the 1:50 elevation of its type; the elevation shows the adjacent span hidden (grey dashed) or "END OF THE TRUSS LINE" at each post, a grid bubble on every post axis, level lines grey in the grid linetype, the post start level on the key sections; the engine's `place_tag` samples 9 points of the tag box and lets a thin web cross it - use exact geometry for tags among thin members | `STEEL_DETAILING_INSTRUCTION.md` S4.12 |
| BANWA2 joints and bill (2026-10-06, outside the repository) | A concentric analysis model gives overlapping or too-small gaps at many CHS truss nodes: set one work-point offset e per truss type for gaps >= 20 mm; posts through a truss stop 50 mm above the top chord, purlins move beside them; dense elevations use EIT split-bubble callouts; the bill covers all structural steel, is reconciled with the model and gives the weight per plan area; every section in a table carries its weight per length (2026-10-07) | `STEEL_DETAILING_INSTRUCTION.md` S1.6, S2.10, S3.8, S4.10, S7.8; `SYMBOLS.md` level mark |
| BANWA2 plans and RC schedules (2026-10-07, outside the repository) | Perimeter beams flush with the outer column face; solid / hidden beam faces decided per face on every level (beams round a void are seen); a bracket only where a beam frames in, not where the model splits a beam; one-way hollow core slabs carry the office plank symbol in every panel, placed clear of marks, brackets and grid lines; a crosstie or inner stirrup is drawn only on a bar present in both the top and bottom layers; beam schedule columns END SUPPORT / MID SPAN / CONTINUOUS SUPPORT (continuous = end bars when the model has one set) or one ALL SPAN column with total bar counts; reading drawn entities back for placement must never skip an entity silently | `FLOOR_PLAN_DRAWING_INSTRUCTION.md` FP9.2, FP10.2, FP10.3a; `RC_DRAWING_RULES_EIT-011006-19.md` §15.3; `SYMBOLS.md`; `DRAWING_ENGINE.md` §9 |

## 3. Starting a new job

1. Pick the closest job above and copy its structure: `calc_*.py` (if there is a design), `*_engine.py`,
   `*_sheets.py`, `build.py`, `plot.py`.
2. Import the engine from `drafter/` (`td_engine`, and `steel` for steel) as `srt_engine.py` does; never copy it.
   Set the project data and options in the job's own engine module.
3. Write the job's `README.md` from the start, with:
   - the drawing set, stage and status;
   - the design basis and its assumptions;
   - results;
   - the sheets;
   - build and plot commands;
   - files;
   - open items before construction or fabrication;
   - change history.
4. Add the job to `tests/test_build.py` so every build is smoke-tested.
5. Add it to the catalogue above. When a review produces a rule, add a row to §2 and write the rule into `docs/`.

## 4. Status words

- **Current**: the set being developed; changes are normal.
- **Issued** standard sets (general notes, typical details): changed only by a new revision issued through
  `standard_drawings/publish.py --issue`; the issued folders are never edited.
- **Issued**: sent out under a revision. Change it only by a new revision (revision row, drawing numbers, change
  history), and regenerate exactly as issued otherwise.
- **Frozen**: kept as a reference; do not change it.
- **Superseded**: replaced by a newer job; kept for its history and helpers.
- **Demonstration**: a sample to show a drawing type; not a real project.
