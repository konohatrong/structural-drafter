# Steel drawings: approach, rules and reading order

Structural steel: hollow-section and open-section members, trusses, connections, bearings, bracing. Composite and
timber connections borrow the bolt, plate and weld rules from here. Read this with the general rules in
`docs/general/`, which apply to every structure type.

## 1. How a steel set presents the structure

A steel drawing exists to let the fabricator **make and fit every piece without asking**. Every size, length, weld
and bolt is given, and the calculation is the single source of all of them.

| Topic | Steel approach | Rule |
|---|---|---|
| **What the set is** | The engineer's design set drawn **shop-ready**: joint information, welding information (size, extent, WPS, inspection), materials, erection and stability, camber, and a bill | S1 (`STEEL_DETAILING_INSTRUCTION.md`) |
| **Scale** | **Drawn to scale**: general elevation 1:50, arrangement sections 1:20, nodes and bearings 1:10, connections 1:5, weld zones 1:1. Not N.T.S. Continuous trusses: a **key section of every truss line at 1:200** leading to the 1:50 elevation of each type | S2, S4.12; SRT, BANWA2 sheets |
| **Geometry** | Working lines on member centroids meeting at work points (WP); set-out from lines the fitter can find on the steel; joint limits (e, gap, θ, β) checked in the calc on the drawn geometry; a concentric analysis model gets one WP offset e per truss type | S2, S2.10 |
| **Line hierarchy** | Steel outline at full weight; hollow-section walls fine hidden grey in every view; centre and work lines grey chain; hidden parts dashed where covered; welds as 45° hatch only | S4 |
| **Concrete** | The support, not the subject: hatched `AR-CONC`, grout `AR-SAND`. (In an RC drawing, the RC section is not hatched) | S4.6 |
| **Identification** | Two levels of mark: erection mark (T1, one per support span of a continuous truss) and piece marks (D1, V2, TC1, p1, w1, FB1), **generated** from section, length and end preparation (or section marks W1 ... on typical elevations, pieces by the fabricator). Members tagged in circles beside the member; no node numbers | S3; guide §9.2 |
| **Welds** | **Every weld has an AWS A2.4 symbol** (size, length, all-round, field flag, NDT, tail reference). Leaders never repeat weld information. A weld key is on the general-notes sheet | S5 – S6; guide §9.3 |
| **Bolts** | Grade, diameter and length from the grip; holes, washers, tightening in a field bolt table; leaders aim at the bolt centre with a ring of 1.25 × the hole | S8; guide §2.1 |
| **Leaders** | **Orthogonal style**: straight or an L with a real second leg (≥ 3 mm), never crossing (`LEADER_ORTH`). Arrows on plate edges | guide §9.1 |
| **References** | Cutting planes with end strokes only, looking left or down; dashed detail callouts with "DETAIL n/sheet - WHAT" (on a dense 1:50 elevation: dashed circle + split bubble n / sheet); members with a clear band named on themselves | guide §9.4, §9.7, §9.8; S4.10 |
| **Bills and tables** | Member schedule, plates and fittings, field bolts, node geometry and weld legs, connections, fly bracing; **every section followed by its weight per length**; the bill covers **all** the structural steel, reconciled with the model, with the weight per plan area; **one weight figure used everywhere** | S1.6, S3, S3.8 |
| **Levels** | Level marks with the line grey in the grid linetype (chord levels at the supports, post start on key sections) | S4.12; `SYMBOLS.md` |
| **Erection** | Stability, lifting weight, sequence, matchmarks, anchor rods and levelling, which end is fixed first | S9 |
| **Units** | Every measured value in a note carries its unit; dimension figures, weld sizes and designations stay bare | guide §2.4.2 |

For how this differs from concrete, see the comparison in `docs/README.md`.

## 2. Documents

| File | Use it for |
|---|---|
| `STEEL_DETAILING_INSTRUCTION.md` | Rules S1 – S11: set content, setting out, marks, graphics, weld symbols, hollow-section welds (AWS D1.1 Fig 9.10), joints and splices, bolts and anchor rods, erection, fly bracing (S9A), checks, and where each rule is coded |
| `reference/SOURCES_STEEL_DETAILING.md` | Extracts with page references: AISC *Detailing for Steel Construction* (Part A), AISC Design Guide 21 welds (B), Design Guide 24 HSS connections (C – D), Beca standard sheet SE-1505 fly bracing (E), Design Guides 4 and 16 moment end plates (F – G), Design Guide 25 web-tapered frames (H), Design Guide 29 bracing connections (I) |
| `.claude/skills/steel-detailing/SKILL.md` | Step-by-step workflow and the office rules, for Claude Code |

Office standard steel sheets (Beca SE-1501 to SE-1505: holding-down bolts, end plates, cleats, bracing, fly bracing)
are outside the repository, at `G:\My Drive\##Workset_Autocad\400 Standard Details\400 Standard Details\20 -
STEELWORK\`. Review the matching sheet before detailing that kind of connection, and summarise it in the sources file.

## 3. Reading order for a steel task

1. `docs/general/`: the drawing standard, the annotation guide (§0 and §9), the symbols catalogue (§4 steel) and
   drawing production.
2. This README, then `STEEL_DETAILING_INSTRUCTION.md`.
3. The sources file, when a code value or detailing practice needs checking. Check the code itself (AISC 360-16,
   AWS D1.1) when the value matters.
4. The closest example job:
   - `jobs/steel_roof_truss` (one welded CHS truss, full shop-ready set: README, `calc_truss.py`, `srt_engine.py`,
     `srt_sheets.py`);
   - `jobs/steel_portal_frame` (portal frame from a live MIDAS GEN NX model, A1 sheets);
   - BANWA2 (outside the repository, see `jobs/README.md`): a steel roof of continuous CHS trusses on an RC frame,
     from a live model - roof plans, key sections, typical elevations, welded joints, posts through the trusses, bill.

## 4. Engine helpers for steel

In `drafter/steel.py`, on top of `drafter/td_engine.py`. Import it with `from drafter.steel import *` after the
project data and options are set; it adds the steel layers to the document:
- members and plates: `chs_section`, `chs_break`, `break_point`, `plate`;
- bolts: `hole`, `slot`, `bolt_side`;
- welds: `weld` (symbol), `weld_region`, `weld_bead`, `weld_band`;
- references: `cutmark`, `detail_callout`, `wp_mark`, `tag`, `place_tag`.

In the example job's `jobs/steel_roof_truss/srt_engine.py` (tied to the truss design geometry): `chord`, `branch`,
`branch_zones`, `weld_branch`, and the marks `_web_marks`, `mark_of`, `marks_at`.

In BANWA2 (`plans/`, job code on the shared engine, the code map is in the steel instruction S11): `truss_details`
(key sections, elevations with adjacent spans hidden, callouts, grey level lines, exact tag clearance), `calc_joints`
and `joint_details` / `post_joints` (joint geometry, welds, typical joint and post details), `bom` (bill, weight per
area), `model_data` (truss marks per support span, purlin rows beside the posts, unit weights).

Generalise a helper in `drafter/steel.py` (for example to open sections) rather than forking it in a job. Keep its
output unchanged for the existing sets (or opt-in), and record the change in `docs/general/SYMBOLS.md`.
