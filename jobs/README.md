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
| `steel_roof_truss` (SRT-ST, 6 sheets) | **Steel**: 25 m CHS Pratt roof truss with bearings, splices, loose diagonal and fly bracing | For review (Rev A) | Calc-driven steel set: AISC 360-16 / DG24 design in the calc, generated piece marks, AWS weld symbols and branch weld zones, bills, camber, anchor rods, erection notes, orthogonal leaders, detail callouts | `steel_roof_truss/README.md` |
| `standard_set_R2` (STR-ST 11xx) | **Concrete**: typical details, columns 1101 – 1104, beams 1111 – 1116, slabs 1121 – 1128 | **Issued** F-A (ISSUED FOR USE, 03/10/2026); changes only by revision | N.T.S. typical details from one member catalogue, model-space blocks, pens by colour, numbered tables, focus rule, clean dimensioning, leader form per target | `standard_set_R2/MODEL_SPACE_SHEETS.md` (R2 rules and history) |
| `nooker_rw` (NRW-ST, 7 sheets) | **Concrete**: cantilever retaining wall with joints, corners and bar schedule | **Issued** (Rev B); change only by revision | A complete project set with its design calc (`calc_rw.py`); the origin of the annotation engine and the office conventions | `nooker_rw/README.md` |
| `standard_set` (STR-ST 1001 – 1003, R1 11xx) | **Concrete**: general notes; typical details R1 | General notes **issued** F-A (ISSUED FOR USE, 03/10/2026); R1 details **frozen** | The first model-space set from blocks; general notes flowing over sheets at the normal text size | `standard_set/MODEL_SPACE_SHEETS.md` |
| `general_notes` (STR-ST-1001 Rev A) | **Concrete** general notes, one sheet | Superseded by the Rev B notes in `standard_set` | The Rev A notes sheet (× 0.625 sizes, one sheet, balanced band), replaced by Rev B (normal sizes, flowing sheets) | `docs/general/GENERAL_NOTES_DRAWING_INSTRUCTION.md` |
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
- **Issued**: sent out under a revision. Change it only by a new revision (revision row, drawing numbers, change
  history), and regenerate exactly as issued otherwise.
- **Frozen**: kept as a reference; do not change it.
- **Superseded**: replaced by a newer job; kept for its history and helpers.
- **Demonstration**: a sample to show a drawing type; not a real project.
