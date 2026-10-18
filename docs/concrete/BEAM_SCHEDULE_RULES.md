# RC beam schedule: the office standard

The office RC beam schedule for every project, new or corrected (user, 2026-10-18: "I would like to use this beam
rebar presentation in every project (upcoming project or project that will correct)"). The engineer keeps the bars in a
spreadsheet; the schedule sheet and the strength check are both made from it. This file owns the rules; RC rules §15.3
says what a beam schedule must show, and the form below meets it.

| Item | Where |
|---|---|
| Generator (read / write the spreadsheet, draw the schedule) | `drafter/beam_schedule.py` |
| Tests | `tests/test_beam_schedule.py` |
| Template (example rows): `.xlsx`, `.dxf`, `.dwg` | `project_template/tree/06 CAD/templates/BEAM_SCHEDULE_TEMPLATE.*` |
| Worked example | NSO (`G:\My Drive\Works\##2026\20261017 - Nong Sarai Office Building`): `04 Code\beam_schedule.xlsx`, `04 Code\drawings\nso_beams.py` (sheet NSO-ST-3301), `04 Code\calc\calc_beams_check.py` |

## BS1. The form (one row per mark)

User, 2026-10-18 (the engineer's template drawn in the NSO A38 DWG: "USE THIS TEMPLATE, REFINE AND IMPROVE"; "SLAB
DUMMY SHOWING THAT SLAB IS A PART OF BEAM"; "ADD PROPER BREAK LINE").

1. Columns **NO. | SIZE (mm) | SECTIONS**; under SECTIONS five **fixed** columns: **END SUPPORT | MID SPAN | CONTINUOUS
   SUPPORT | CANTILEVER | ALL SPAN**. A column the mark does not use stays empty (labels kept, no values), so every
   mark reads at the same place.
2. Under each section its own table **TOP | BOT | STIRRUP | SIDE** (label cell, value cell).
3. Which columns a mark uses (RC rules §15.3, user 2026-10-07):
   - support and mid-span bars differ: END SUPPORT, MID SPAN, CONTINUOUS SUPPORT; where the design gives one support
     set, the continuous support repeats the end support and a note says so;
   - the same bars and stirrups throughout: ALL SPAN only;
   - a cantilever mark (`...C`): CANTILEVER.
4. The section is drawn at 1:25 (model space at full size, mm): the cut concrete; the bars as dots at true size, never
   under 1.1 mm plotted; the stirrup wrapping its corner bars with both 135° hooks at one corner (RC rules §19.4).
5. **Slab dummy**: where the level has a slab, the section is a T - the slab of that floor drawn about 300 mm each side
   of the beam, the beam top flush with the slab top, both flange ends closed by the EIT break line past the slab faces
   (`zbreak`). No slab where the level has none (a roof-beam level with every panel open): the plain rectangle.
6. Remarks particular to a mark go into the sheet notes; the lines of each mark stay in the plan member tables.
7. The sheet notes give: concrete and bar grades, cover (general-notes table), strength reduction factors, what `a+b`
   means (BS2.4), the stirrup legs (BS3), the standard details for cut-offs, laps and stirrup zones, what is not yet
   checked.

## BS2. Bar input rules (TOP and BOT)

User rules, 2026-10-18 ("3/3+2 - DB16 define 6+2 DB16 (2 layers - 3DB16 as nominal and 1 layer - 2DB16 as extra at that
section)"; "3+2 define 3+2 DB16"; "3/3/3 define 9-DB16"; "using 2(+1) for extra bar share same layers as nominal";
extra bars in more than one layer: "possible").

1. Layers are counted **from that face, outer layer first**: TOP from the top fibre, BOT from the bottom fibre; the last
   figure is the innermost layer.
2. **`/`** separates layers. **`+`** starts the **extra** bars of that section (additional to the nominal, continuous
   bars); each `/` after the `+` is a further inner layer of extra bars. **`N(+M)`** is one layer holding N nominal and
   M extra bars.
3. Examples:

   | Input | Layers (outer first) | Drawn as |
   |---|---|---|
   | `3/3/3` | 3, 3, 3 nominal | `9 - DB16` |
   | `3+2` | 3 nominal; 2 extra | `3+2 - DB16` |
   | `3/3+2` | 3, 3 nominal; 2 extra | `6+2 - DB16` |
   | `3+3/2` | 3 nominal; 3 extra; 2 extra | `3+5 - DB16` |
   | `2(+1)` | 2 nominal + 1 extra in one layer | `2+1 - DB16` |
   | `3/2(+1)+2` | 3 nominal; 2 nominal + 1 extra; 2 extra | `5+3 - DB16` |
   | `2` | 2 nominal | `2 - DB16` |

4. On the drawing a face reads **nominal total + extra total - DBn** (`6+2 - DB16`), or the nominal total alone when there
   is no extra bar. The dots follow the layers: every layer at its place, layer 2 and on at the clear distance of the
   SETTINGS sheet (25 mm) below (above) the one before.
5. One bar size per face (TOP DB, BOT DB). Mixed sizes in one face: not in this form yet (write the larger size and a
   note, or extend the generator).
6. Rejected with the row number: an empty layer (`3/0`, `0(+2)`, `3+0`), a shared layer among the extra layers
   (`3+2(+1)`: write `3+3`), anything outside the grammar.

## BS3. Stirrup input rules

User rule, 2026-10-18 ("stirrup : 2-RB9@100 (2 refer to 2 legs equal to 1 hoop stirrup if 3-RB9@100 mean 1 hoop + 1
cross ties)").

1. **`n-RBd@s`** (or `DBd`): n legs, bar, spacing in mm. `2-RB9@100` = one closed hoop; `3-RB9@100` = hoop + one
   crosstie; `4-RB9@100` = hoop + an inner hoop. No leg count (`RB9@200`) = 2 legs.
2. The inner legs sit on bars present in **both** the top and the bottom outer layers, the ones nearest the middle
   (RC rules §15.3, user 2026-10-07: "tie as shear reinf. need to place on rebar it could not standalone"). Where no
   such bar exists the build stops with `!!`: rearrange the bars.
3. On the drawing the stirrups read as entered (`3-RB9@100`); the sheet notes define the legs.
4. Side-face bars (SIDE): `2-DB12` = 2 bars on each face, drawn evenly between the top and bottom layers; `-` = none.

## BS4. The spreadsheet

1. Sheet **BEAMS**: one row per mark and section - MARK | b (mm) | h (mm) | SLAB t (mm) | SECTION | TOP | TOP DB | BOT |
   BOT DB | STIRRUP | SIDE | NOTE. A blank MARK / b / h / SLAB t repeats the row above (the other sections of the mark).
   SECTION is picked from the list. The bar and stirrup cells are text (format `@`), so Excel never turns `3/3` into a
   date.
2. Sheet **INSTRUCTIONS**: these rules in short, with the examples - for the engineer who fills the file.
3. Sheet **SETTINGS**: cover (mm, to the stirrup; general notes TABLE 7), layer_clear (mm), flange (mm of slab drawn), hook
   (mm; 0 = 6 db + 25). A project checks the cover against its own design data (`project.py`).
4. In a project the file is `04 Code\beam_schedule.xlsx`, the **one source** of the schedule sheet and of the beam check.
   An edit by the engineer in the DWG is read back (DXFOUT of a copy) and written into the spreadsheet, never kept
   only in the drawing.

## BS5. Using it in a project

1. New project: the template comes with `project_template` (`06 CAD\templates`). Copy
   `BEAM_SCHEDULE_TEMPLATE.xlsx` to `04 Code\beam_schedule.xlsx`, replace the example rows.
2. Existing project: copy the template from the toolkit, or write the file from the project's data with
   `beam_schedule.write_xlsx(path, marks, settings)`.
3. Draw: `marks, settings = beam_schedule.read_xlsx(path)`, then `beam_schedule.draw(msp, marks, settings, S=25,
   txt_layer=<project text layer>)` inside a view function (origin = the schedule's top-left corner), shown at 1:25.
   Alone: `python -m drafter.beam_schedule draw <in.xlsx> <out.dxf>`; the template:
   `python -m drafter.beam_schedule template <folder>` (`.dwg` when AutoCAD's Core Console is installed).
4. Check: read the same file; per layer `beam_schedule.totals(layers)`, area `bar_area(layers, db)`, stirrup legs from
   `parse_stirrup` (NSO `calc_beams_check.py`: flexure with d to the layer centroid, shear with the legs, spacing, Av,min,
   bar fit, As,min, minimum depth).
5. The sheet: one A1 sheet "RC BEAM SCHEDULE", the schedule at 1:25 at the left, the notes and a design summary (the
   check per mark) at the right (NSO-ST-3301).

## BS6. Change log

| Date | Rule | Source |
|---|---|---|
| 2026-10-07 | END / MID / CONTINUOUS columns, ALL SPAN, inner legs on bars | RC rules §15.3 (BANWA2 S-302) |
| 2026-10-18 | Row form with five fixed columns, TOP / BOT / STIRRUP / SIDE tables, slab dummy with break lines | NSO A38 DWG template |
| 2026-10-18 | Spreadsheet source; layers `3/3/2`; stirrups with legs `2-RB9@100` | NSO, engineer |
| 2026-10-18 | Nominal / extra grammar: `/` layers, `+` extra, `N(+M)` shared layer, extra in several layers | NSO, engineer |
