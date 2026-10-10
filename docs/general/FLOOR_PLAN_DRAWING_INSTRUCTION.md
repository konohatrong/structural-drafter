# Floor Plan Drawing Instruction: pile, foundation, floor, roof-deck and roof plans

Status: **draft for the engineer's review**, written 2026-10-04 before the SSK plans are drafted (user: "make
instruction for floor plan drawing first; write everything: detail, linetype, scale, weight, plot style, annotation
style"). Rules marked open in FP18 wait for the engineer's decision.

**Scope.** Structural plans of buildings, level by level: pile plan, foundation plan, ground and upper floor plans,
roof-deck and roof plans, at 1:100 (enlarged parts at 1:50), on A1 project sheets. Material-neutral where it can be:
reinforced-concrete content follows `docs/concrete/RC_DRAWING_RULES_EIT-011006-19.md` §14, steel members in a plan
follow `docs/steel/STEEL_DETAILING_INSTRUCTION.md` S1.

**Companions.** EIT digest (`DRAWING_STANDARD_EIT-011006-19.md`: §7 grids, §8 dimensions, §9 levels, §10 marks, §11
callouts, §19 office conventions); `ANNOTATION_ALIGNMENT_GUIDE.md` (where notes and leaders go); `SYMBOLS.md` (every
symbol); `DRAWING_PRODUCTION.md` (pipeline and checks).

**Source of each rule** (precedence: `AGENTS.md` §1):

| Mark | Source |
|---|---|
| [USER] | The engineer's instruction, dated |
| [OFFICE] | Read from the office's own current set: SSK `ST-Plan-อาคารกองศึกษา ฉบับแก้ไข 090969.dwg` (layers, styles, blocks, legend table in its model space) |
| [EIT] | EIT 011006-19 text or figures, through the digest |
| [REC] | Recommendation of this instruction, to be confirmed by use |

**Worked example:** job SSK (Samutsongkram office building 2, outside the repository: `G:\My Drive\Works\20260318 -
Samutsongkram Building Office\Drafter`). Its review of 04/10/2026 is the source of the "never" rules in FP2 – FP15.

---

## FP0. Project settings: decide first, keep in one place

Every value below is **project data**: it lives in the job's `project.py` (SSK: `Drafter\project.py`) and nothing
else retypes it. Ask the engineer for any value the project has not fixed.

| Setting | SSK value | Rule |
|---|---|---|
| Paper | A1, 841 × 594 mm | FP2 |
| Plan scale | 1:100 (enlarged parts 1:50) | FP1.3 |
| Plot style | `STRUCT-A1-A2.ctb` (`G:\My Drive\##Workset_Autocad\Structology\Plot Style\`) | FP3 [USER 2026-10-04] |
| LTSCALE | **45 on A1 paper, 30 on A2 paper**, PSLTSCALE 0, entity ltscale 1, acadiso linetypes | FP4 [USER 2026-10-04] |
| **Text font** | **`cordia.shx`, width factor 0.90** | FP6. **The font is a project setting: it may change from project to project at the engineer's choice** [USER 2026-10-04]. Never hard-code a font in shared code |
| Text height | **2.00 mm plotted** (200 in model at 1:100) | FP6 [USER 2026-10-04] |
| Architectural background | Current AR plan, **colour 9** | FP15 [USER 2026-10-04] |
| Units of dimensions and levels | **open, D1** (SSK sets use metres) | FP11, FP12 |
| Grid | `project.GRID_X / GRID_Y` (SSK: 1 – 15 and A – D) | FP8 |
| Levels and finish allowance | AR FFL − ST SFL = `project.FINISH` (SSK 50 mm) | FP11 |
| Member numbering | One system per project (EIT §10.2) | FP10 |
| Drawing numbers | Project series (SSK: S1-01 …) **open, D4** | FP2 |

---

## FP1. The plan set

### FP1.1 Which plans, in what order [EIT, RC §14]
1. Pile plan (when piles are not shown on the foundation plan).
2. Foundation plan: footings, piles, ground and tie beams, lift pits.
3. Ground floor plan (its beams are the ground beams of a slab on beams).
4. Each upper floor plan, bottom up.
5. Roof-deck plan, then roof plan (and lift overrun, water tank slabs, canopies at the level where they are cast).

One plan per structural level. A level with two slab heights (a step, a mezzanine, a double-height void) is one plan
with step and void symbols (FP9.5, FP11.3), not two plans.

### FP1.2 Plans on a sheet [OFFICE]
- Up to **two plans per A1 sheet**, one above the other, as SSK S1-02 and S1-03 do. A long building at 1:100 fills
  the width; a third plan never fits.
- **Every plan of the set sits at the same place relative to its grid**, sheet after sheet: grid 1 / grid A at the
  same paper position in the upper slot and in the lower slot. Plans then overlay sheet to sheet, and the grid
  bubbles and grid dimensions line up across the set.
- Plans are drawn in model space at full size (1 unit = 1 mm) and each plan has its own model-space place; the sheet
  shows it through a viewport at 1:100, or the plan is drawn at sheet position for a model-space sheet. Never move,
  rotate or rescale one plan relative to its grid.
- A sheet with one plan keeps the empty slot for the legend, notes and key plan; it does not enlarge the plan.

### FP1.3 Scale [EIT §5]
- Plans 1:100. An enlarged part (stair core, lift pit, a congested corner) 1:50, as its own view with a title and a
  callout from the plan (FP13.6).
- Every view states its scale in its title. Add a bar scale where prints may be reduced (A3 half-size prints of A1).

### FP1.4 View title [EIT §11, OFFICE]
- Thai title, underlined: `แปลนพื้นชั้นสาม` (office dynamic block on layer `S-40Txt`, texts on `S-T200` colour 1 and
  `S-TH` colour 7); English below or after it when the project is bilingual: `3RD FLOOR PLAN`.
- Under the line: `มาตราส่วน` (SCALE) at the left, `1:100` at the right.
- Title height **4.0 mm**; the office block writes the scale line at 2.5 mm, against the 2.0 mm rule (open, D3).
- Placed **below the plan, clear of every grid line, dimension and bubble**. Never on a grid line (SSK S1-01: the
  foundation title sat on grid line D).

---

## FP2. Sheet, title block and sheet furniture

- **Sheet**: A1 841 × 594, the office A1 title block (`Xr-Title Block-A1.dwg`) as an xref, frame per the title
  block. EIT §3 for the content of the title block.
- **Title block fields are filled once and only once.** The drawing title and drawing number come from one source
  (the layout's attributes or the job's sheet table). Never leave text from another sheet in the xref under the
  sheet's own title (SSK: "ข้อกำหนดทั่วไป, รายละเอียดทั่วไป 2" and "S0-02" printed under every plan sheet's title and
  number). JOB NO., DATE, FILE NAME and TOTAL are real values, never placeholders ("5", "6").
- **Revision rows** record every issue (No., description, date, by). A file name saying "ฉบับแก้ไข 090969" without a
  revision row is a missing record.
- **Drawing numbers**: the project's series (SSK `S1-01 … S1-04`, ST discipline) or EIT §13
  `PPPP-ST-3xxx-G-RR`: one scheme per set (open, D4).
- **Furniture on every plan sheet**: north arrow (FP14.3), legend (FP14.1), plan notes (FP14.2), key plan when the
  building has parts or phases. Placed in the free slot, never over the plan.

---

## FP3. Plot style and pens [USER 2026-10-04; EIT §19.2]

Plot every A1 sheet with **`STRUCT-A1-A2.ctb`**. Line weight comes **from the colour** through the plot style; layer
and entity lineweights stay ByLayer / Default and are never used to set a pen.

| ACI colour | Plots as | Use on plans (FP5) |
|---|---|---|
| 1 red | black **0.25** | Columns cut (outline and solid fill), grid bubbles, view titles, steel plates |
| 2 yellow | black **0.35** | Slab edges, beams seen, footings, member text and tags |
| 3 green | black **0.45** | Heaviest: kept for emphasis (none on a plan by default) |
| 4 cyan | black **0.20** | Light lines |
| 5 blue | black **0.40** | Match lines |
| 6 magenta | black **0.35** | Cutting planes, callouts |
| 7 white | black **0.20** | Hidden beams, dimensions, leaders |
| **8 grey** | **grey 128, 0.18** | Grid lines, hatch, secondary information |
| **9 light grey** | **object colour (light grey), 0.13** | **Architectural background** (FP15) |
| 10 – 254 | black, object lineweight | Not used on plans |

- **Hierarchy on a plan**: background 0.13 < grid 0.18 < hidden beams, dims 0.20 < columns, bubbles, titles 0.25 <
  slab edges, beams seen, member text 0.35. The structure reads first, the AR background last.
- **Open, D2**: the legend table kept in the office's SSK model space lists older pens per colour (A1/A2: 7 = 0.18,
  2 = 0.30, 1 = 0.20, 5 = 0.35, 3 = 0.50, 8 = 0.15). The CTB above governs until the engineer says otherwise; the
  legend table must then be corrected so that the two never disagree.
- Plot from AutoCAD (`plot.py`) for issue; the ezdxf render (`--ezdxf`, or the job's overlay renderer) applies the
  same CTB for review prints.

---

## FP4. Linetypes and LTSCALE [USER 2026-10-04; EIT §4.4, §19.2]

- **acadiso.lin** patterns, **LTSCALE 45 when plotted on A1, 30 on A2** (user, 2026-10-04: "30 for A2"),
  **PSLTSCALE 0**, MSLTSCALE 0, **entity linetype scale 1** everywhere. A
  plan whose dashes look wrong is fixed by its linetype choice, never by an entity scale.
- Plotted length = pattern × 45 / 100 at 1:100:

| Linetype | Pattern (mm) | Plotted at 1:100 (mm) | Use on plans |
|---|---|---|---|
| CENTER | 31.75, −6.35, 6.35, −6.35 | 14.3 / 2.9 / 2.9 / 2.9 | Grid lines; centre lines of steel members |
| CENTER2 | 19.05, −3.175, 3.175, −3.175 | 8.6 / 1.4 / 1.4 / 1.4 | Short centre lines (in 1:50 views) |
| HIDDEN | 6.35, −3.175 | 2.9 / 1.4 | **Beams below the slab**; footing outline on a pile plan |
| HIDDEN2 | 3.175, −1.5875 | 1.4 / 0.7 | **Columns and walls below** (stopping under), fine hidden outlines |
| DASHED | 12.7, −6.35 | 5.7 / 2.9 | Outlines of items above or by others (canopy above, future work) [REC] |
| PHANTOM | 31.75, −6.35, 6.35, −6.35, 6.35, −6.35 | 14.3 / 2.9 / 2.9 / 2.9 / 2.9 / 2.9 | Boundary, match line, scope limit |
| DASHDOT2 | 6.35, −3.175, 0, −3.175 | 2.9 / 1.4 / 0 / 1.4 | Not used on structural plans |

- At **1:50** (enlarged views in the same model space) the same LTSCALE gives dashes half as long on paper: use the
  next longer type (HIDDENX2 for HIDDEN, CENTER for CENTER2) if they read as solid [REC].
- A short hidden outline (a 400 mm column) must show at least two dashes on each side: HIDDEN2, not HIDDEN.

---

## FP5. Layers [OFFICE, mapped to FP3 / FP4]

The office's layer names (SSK), with the colour that gives the pen. One meaning per layer; no other layer carries
structure.

| Layer | Content | Colour → pen | Linetype |
|---|---|---|---|
| `S-GRID` | Grid lines | 8 → grey 0.18 | CENTER |
| Grid xref `BALL` | Grid bubbles and labels | 1 → 0.25 | Continuous |
| `S-DIM`, grid xref `Dim` | Dimensions, extension lines grey via the dimension style | 7 → 0.20 | Continuous |
| `S-CONT_COL` | Columns and RC walls **cut and continuing** (outline + solid fill) | 1 → 0.25 | Continuous |
| `S-CX_COL` | Columns **starting on a beam** (sit on beam) | 1 → 0.25 | Continuous |
| `S-HID_COL` | Columns and walls **below that stop under** this floor | 2 → 0.35 | HIDDEN2 |
| `S-CONT_BEAM` | Beams **seen from above** (upturned, at a slab edge or step, beams with no slab over) | 2 → 0.35 | Continuous |
| `S-HID_BEAM` | Beams **below the slab** | 7 → 0.20 | HIDDEN |
| `S-EDGE_SLAB` | Slab edges, slab steps, opening edges | 2 → 0.35 | Continuous |
| `S-OPEN` | The cross over an opening or void (FP9.4) | 8 → grey 0.18 | CENTER (the grid linetype) |
| `S-Footing` | Footings / pile caps (foundation plan) | 2 → 0.35 | Continuous |
| `S_Pile_I` | Piles | 8 → grey 0.18 | Continuous |
| `S-PILE-I` | Piles below, for reference | 8 → grey 0.18 | HIDDEN2 |
| `S-WF`, `S-ST` | Steel members in plan (stair, frames; on a steel roof plan: struts, purlins / posts) | 2 / 1 | Continuous |
| `S-WF-THIN` | Steel members drawn lighter on a steel roof plan (truss chords under the subject members) | 7 → 0.20 | Continuous |
| `S-ROD` | Tie rods, one line each (FP9.2, steel S4.11) | 1 → 0.25 | CENTER (the grid linetype) |
| `S-SAG` | Sag rods between purlins | 7 → 0.20 | DASHED |
| `S-BRACKET` | Member length brackets of beam and truss marks (FP10.2) | 8 → grey 0.18 | Continuous |
| `S-HATCH` | Hatch: existing structure, fill concrete | 8 → grey 0.18 | Continuous |
| `S-TXT_2.5_MM`, `Slab_Txt`, `SYM_TXT` | Member marks, tags, notes (the layer names are historical: the height is FP6's) | 2 → 0.35 | Continuous |
| `S-40Txt` (block), `S-T200`, `S-TH` | View titles: title and scale text, underline | 1 → 0.25; 7 → 0.20 | Continuous |
| `MATCH_LINE` | Match lines | 5 → 0.40 | PHANTOM |
| `BOUNDARY` | Scope / property boundary | 2 → 0.35 | PHANTOM |
| `Defpoints`, `DEFPOINT` | Construction points | not plotted | – |
| `AR-…` (xref layers) | Architectural background | **9** | as the AR file, all forced to colour 9 (FP15) |

- A new layer is added only for a new meaning, with its row here.
- Layers that belong to the AR file (`WALL`, `FUR`, `DOOR-WINDOW`, `COL`, …) never hold structural content in the ST
  drawing, and AR plans are never pasted into the ST file as blocks (SSK revised file: four old AR plans pasted under
  the structure, plotting in their own colours) (FP15).

---

## FP6. Text and annotation style [USER 2026-10-04; OFFICE]

### FP6.1 Font
- **Project font: `cordia.shx`, width factor 0.90** for SSK (the office text styles `Standard`, `DIM`, `Cordia`,
  `Heading` all use it). **The font changes per project at the engineer's choice**: it is `project.TEXT_FONT` /
  `TEXT_WIDTH`, and every style of the job takes it from there.
- One text style for the job (office name `Cordia`, set current); its height is 0, so each text carries its own
  height. No second font on a sheet except inside the title block xref.
- Thai and English in the same font. SHX fonts plot with the colour's pen (FP3): text on colour 2 strokes at 0.35.

### FP6.2 Heights (plotted mm; model = plotted × 100 at 1:100)

| Text | Height | Source |
|---|---|---|
| **All notes, marks, tags, dimensions, slab tags, legend, leader notes** | **2.0** | [USER 2026-10-04] |
| Grid bubble labels | 3.3 in a bubble of Ø 6.6 | [OFFICE] (open, D3) |
| View titles | 4.0, underlined; scale line 2.5 in the office block | [OFFICE] (open, D3) |
| Sheet title, drawing number | per the title block | title block |

- The office slab-tag block `Sym-SFL` carries 1.5 mm text: below the 2.0 rule. Rescale the block or redefine its
  attributes at 2.0 [USER rule wins; open, D3].
- A text that does not fit at 2.0 means the annotation must move, never shrink.

### FP6.3 Leaders and notes [EIT §19.5; guide §0, §9.1]
- **One leader style per set.** Plans: **orthogonal** leaders (straight or one L, ≥ 3 mm leg) [REC: plan targets are
  dense, and the office's plan leaders are straight, e.g. "FLOOR ABOVE LANDING"].
- Filled arrow 2.0 on an edge; a dot terminator for a point inside an area (guide §2.1).
- Notes in aligned columns beside the plan or in the bay they describe; never across a grid line, a beam line or a
  dimension (guide §1, §3 – §5).
- **Units on every bare number** in notes and leaders ("JOINT 25 mm"); dimension figures and tag values stay bare
  (guide §2.4.2).

---

## FP7. Dimension style [OFFICE; EIT §8, §19.3]

The office style **`a-100-a`** (plans at 1:100); `a-50-a` … for other scales by DIMSCALE only.

| Variable | Value | Meaning |
|---|---|---|
| DIMSCALE | 100 (= scale) | Everything below is plotted mm |
| DIMTXT | **2.0** | Text height (= FP6.2) |
| DIMTXSTY | the job text style (FP6.1) | Font and width from the project |
| DIMASZ | 2.0 | Terminator size |
| DIMBLK | closed filled arrow for member dimensions; **dot** (office `DOT1`, grid style `C-C-100`) for grid chains | EIT §8.2: dots on grid lines, arrows or ticks on faces |
| DIMEXO / DIMEXE | 2.0 / 1.25 | Gap from the object / extension beyond the dimension line |
| DIMGAP | 1.0 | Text clearance |
| DIMTAD | 1 | Text above the line, aligned with it |
| DIMCLRE | 8 | Extension lines grey (EIT §19.3) |
| DIMCLRT | 2 | Text 0.35 |
| DIMCLRD | ByLayer (`S-DIM`, 7) | Dimension line 0.20 |
| DIMDEC / DIMLFAC | per the unit decision D1 | One unit and one precision per set |

---

## FP8. Grid [EIT §7; OFFICE]

- **One grid source**: the grid xref (SSK `Xr-Grid-อาคารกองศึกษา.dwg`) or the job's grid data
  (`project.GRID_X / GRID_Y`). Plans never redraw grid lines by hand. The AR grid must agree: checked by the overlay
  (FP16; SSK: every ST bubble within 0.3 mm).
- Letters on the short direction (A, A', B, C, D), numbers on the long direction (1 – 15). Sub-grids `A'` or `1.1`
  per EIT §7, one style per project.
- Grid lines run **past the outermost structure** by at least one bubble, to the bubbles.
- **Bubbles** at the top and the left of every plan [OFFICE]; also at the bottom and right when the plan is wider
  than the reader can follow from one side [REC]. Same bubble size and position on every plan of the set (FP1.2).
- **Close grids**: bubbles of grids closer than one bubble diameter + 1 mm (SSK 8 and 9 at 0.50 m) are **staggered**
  outward (the second bubble moved out one bubble and joined by a short leader), never overlapping (SSK S1-0x: 8 and
  9 touching).
- **Grid dimensions**: a chain of bay dimensions between the bubbles and the plan, and an overall dimension outside
  it, on the top and on the left. Dot terminators on grid lines. Dimension text never on a bubble (SSK: "17.875"
  across bubble C).

---

## FP9. What a plan shows, and how [EIT §4.2 Table 2.3, RC §14.3; OFFICE legend]

A floor plan is the view **looking down on the floor just above its slab**. Everything cut by that view or seen from
above is continuous; what lies below the slab is hidden.

### FP9.1 Columns and walls (office legend, on every plan sheet)

| State at this floor | Symbol | Layer |
|---|---|---|
| **Continuous column** (runs through this floor) | Outline **solid filled** | `S-CONT_COL` |
| **Column sits on a beam** (starts at this floor) | Outline half filled on the diagonal | `S-CX_COL` |
| **Column stops under** (from below, ends at this floor) | Outline with an **X**, or the outline hidden (HIDDEN2) | `S-HID_COL` |
| RC wall cut | Outline filled as a column | `S-CONT_COL` |

- Column size drawn true; the column mark beside it (FP10).
- On the foundation plan the column stub is shown in its footing with the column mark (FP13.2).
- **Classify every vertical member by comparing below and above the cut** (user correction, 2026-10-09, BANWA2 ground
  plan R01, which showed only the columns rising above the floor and left out 13 lower-only supports, 11 of them under
  the grid 1 transfer beams): continuing = solid; lower-only (stopping under) = hidden outline with an X; upper-only
  (starting on a beam) = half filled. A change of section at the same centre (pier 500 to column 450) is a continuing
  column, not a lower-only support. Piles are not columns. Transfer-beam spans and their dimensions follow the lower
  supports, not the upper columns loading the beam. Reconcile the symbol counts with the model coordinates.
- **RC walls in plan** (user, 2026-10-09: "finer wall hatch"; BANWA2 S-106 R08): the wall strip, at its true
  thickness, carries a **fine grey diagonal hatch** (ANSI31, about 0.35 mm plotted spacing through `pscale`, pen 0.10,
  grey screened) so it reads as a wall, not as two beam faces. Hatch only the wall strip: subtract the column
  footprints, respect openings, never hatch a beam strip or a whole slab or tank area. The wall outline keeps its own
  pen and linetype and stays stronger than the hatch; if the plotted strip looks solid, change the hatch spacing or
  pen, never the outline.
- **Steel columns and posts are drawn as their actual section** (user, 2026-10-06: "show as actual section for steel
  post"): the projected outline at true size (SHS 200 x 200: a 200 mm square), no wall thickness; where a member above
  covers part of it, that part is left out. Worked example: BANWA2 S-103 / S-104, posts on the column tops.

### FP9.2 Beams
- **Below the slab: hidden** (`S-HID_BEAM`, HIDDEN), both faces drawn, mitred at the columns they frame into.
- **Seen**: upturned beams, beams at a slab edge or a step where the face shows, beams with no slab over them:
  continuous (`S-CONT_BEAM`). Decide it per face, on every plan level, not per sheet: on a floor with voids (double
  height) the beams round the void are seen while the beams under the slab are hidden (user, 2026-10-07: "don't
  forget linetype rules when to use solid or hidden"; BANWA2 S-102 had every 2F beam hidden, B6 round the double-height
  areas now continuous, `draw_beams(seen=True)`).
- **Perimeter beams flush with the column face** (user, 2026-10-07: "align building perimeter beam edge to column
  edge"): a beam on the building outline has its outer face on the outer face of the columns - its axis moves out by
  (column - beam width) / 2 - so the facade line is straight; inner beams stay centred on the grid. The outer face is
  then the slab edge (continuous), the inner face hidden under the slab. State it in the plan notes. Worked example:
  BANWA2 S-102 / S-103 (`bw_plans.building_outline`, `flush`: C1 450, B 400 out by 25 mm, B6 / RB1 300 by 75 mm).
- Steel beams in an RC plan: by their outline or centre line with the section designation (steel S1).
- **Steel framing plans** (truss chords, bracing, purlins): every member as a **double line at its projected width**
  (CHS outside diameter, SHS / box width, channel flange width, round bar diameter), **no wall thickness** (user,
  2026-10-06: "show as double line showing project dimension (no need to show wall thickness)"); junctions clean as
  for RC beams (union of the member strips), a member below another left out where covered (steel S4.11).
  - A post that runs up through the truss **trims the chords** on every roof plan (FP9.1, steel S4.11).
  - **Tie rods**: one line each on the grid linetype with their own pen (`S-ROD`), never merged with the other rod of a
    cross (user, 2026-10-06).
  - **Purlins on a row with a post** stand **beside the post**, flange edge on the post face, on the down-slope side
    (eave and line ends: inside); the whole row moves (user, 2026-10-06; steel S7.8). The purlin spacing chain still
    gives the node spacing and a plan note gives the offset. Worked example: BANWA2 S-105 (`model_data.purlin_rows`).
- **No moment-release (hinge) symbols on framing plans** (user, 2026-10-06: "no need to show moment release
  symbol"). End conditions belong to the design and the beam details, not to the plan.
- **Clean junctions** [USER 2026-10-04: "dirty line when beam across each others; join, trim, fillet (90 deg. join
  each others), extend, any make it tidy"]:
  - beams that cross form a clean "+": neither beam's faces run through the other;
  - a beam framing into another stops at its face (T), and the through beam's face is broken there;
  - corners close at 90 degrees, outer faces meeting outer faces;
  - beam faces stop at column faces, slab edges and crossing beams: no overshoot, no gap;
  - a hidden face is not drawn on top of a continuous line (an edge beam's outer face is the slab edge);
  - nothing is drawn that the design does not have: a missing face is a question for the engineer, not a line to
    invent.
  Job SSK tidies existing plans with `tidy_beams.py` (strips, union, outline; working revision A2).

### FP9.3 Slabs
- Slab edges, cantilever edges and the edges of openings: continuous (`S-EDGE_SLAB`).
- **The slab edge is the formwork outline at the physical faces of the outermost columns and beams**, not the edge of
  the analysis mesh (which sits on the member centre lines) (user correction, 2026-10-09, BANWA2 ground plan R01 / R02:
  the edge was moved to the outer member faces, including the south-east set-back and the return round the corner
  column). Build it from the projected member widths, keep set-backs and openings, close orthogonal corners without
  nibs, and do not draw a hidden beam face on top of it.
- Each slab panel carries a slab tag (FP10.3). Cantilevers and canopies are slab panels with their own tag.

### FP9.4 Openings and voids
- Outline plus an **X** across the void, and a label: `OPENING`, `LIFT`, `STAIR`, `VOID (DOUBLE HEIGHT)`, `SHAFT`
  [EIT; REC labels]. A void without a label is a question on site.
- The outline is the slab edge (`S-EDGE_SLAB`, continuous); **the X is on the grid linetype in grey** (`S-OPEN`,
  CENTER, colour 8) (user, 2026-10-06: "add cross symbol for opening area with grid line linetype colour 8").

### FP9.5 Steps in a slab
- The line of the step continuous, the **step symbol** (office `Sym-Step`: the step height, `UPPER FLOOR` /
  `LOWER FLOOR`) across it, both slab levels tagged.

### FP9.6 Stairs, lifts, ramps
- Stair outline (flights, landings), `UP`/`DN` arrow, stair mark `ST-1` and the sheet of its detail. RC stairs:
  `STAIRCASE_DRAWING_INSTRUCTION.md`. Steel stairs: member designations by note, detail callout.
- Lift: shaft outline with X (FP9.4), lift pit on the foundation plan, overrun slab and lift roof on their levels
  (SSK: AR +12.38 and +14.80 missing from the ST plans).

### FP9.7 Existing structure and joints
- Existing structure (not in this scope): outline continuous, **hatched grey** (`S-HATCH`, ANSI31) and **labelled**
  ("EXISTING BUILDING, GRIDS 1 – 6 / A – C, NOT IN THIS CONTRACT", or as the engineer words it). A hatch without a
  label is unexplained (SSK).
- Movement or isolation joints: drawn on **every plan** where they occur, with the width ("ISOLATION JOINT 25 mm") and
  a callout to the joint detail (SSK: joint at grids 6 – 7 labelled on the ground floor only).

### FP9.8 What a structural plan does not show
- Furniture, doors, sanitary fittings, room names: only as the AR background (FP15), never as structural lines.
- Reinforcement: on slab-reinforcement plans or details, not on the framing plan (RC §14).

---

## FP10. Marks and tags [EIT §10; RC §14.3; guide §9.2, §9.8]

### FP10.1 Numbering
- One system per project (EIT §10.2), stated in the general notes: SSK uses `C1…`, `F1…`, `B1, B1A, B2C…`, `S1`,
  `ST-1`. A suffix letter is a variant of one type (`B1A`).
- The same mark means the same member type on every plan, detail and schedule.

### FP10.2 Beams
- Mark (and size `(b×h)` when the project shows sizes on plan, RC §14.3) **along the beam**, centred in its span,
  inside the bay, above a horizontal beam and left of a vertical one, reading from the bottom or the right.
- Never on the beam line or another tag; never at a column. A beam that changes type changes mark at the column.
- **The mark stays at the midpoint of its reference span** (user correction, 2026-10-09, BANWA2 S-106 R08): the span
  between the two physical supports, found from the supports and the connectivity, not from the analysis elements
  (several mesh elements make one span). It is not moved to 40 % or 60 % of the span to clear something else. Where
  the midpoint falls on a grid line, the grid line is interrupted locally under the text.
- **A main beam is one member from column to column**, even where secondary beams frame into it and the analysis model
  splits it at every joint. It is marked **once, with a bracket over its length** and the mark at the middle of the
  bracket (user, 2026-10-06: "this is main beam use bracket to present length of main beam avoid misunderstanding").
  An edge beam has its bracket on the outside of the slab. A beam with no beam framing into it keeps the plain mark at
  mid-span - a split of the beam in the analysis model (mesh nodes) is not a beam framing in (BANWA2 secondaries B1,
  B2, B3, B5, RB5 lost their brackets, 07/10/2026; `beam_marks` tests the beam directions at the inner nodes).
- **Which spans get a bracket** (user correction, 2026-10-09, superseding a ground-plan revision that bracketed every
  beam and wall): only
  1. a **main beam receiving a beam that frames in between its ends** (a beam meeting it only at a span end does not
     count), and
  2. a **transfer beam carrying a column that starts on it** (CX) between its supports: its span runs between the
     **lower** supports and the bracket continues past the carried column (the model node there is not a support).
  A designation alone (TB1, TB2) does not decide it: check each span. Ordinary beams and **walls never get a
  bracket**; a bracket is not a placement aid.
- **Anchors and offsets** (same correction):

  | Mark | Text anchor | Offset |
  |---|---|---|
  | Bracketed beam mark | **MIDDLE_CENTER**, in the gap of the bracket, at the reference-span midpoint | anchor **one plotted text height from the physical member edge** (2.0 mm: 400 mm at 1:200), i.e. b/2 + h·S from the centre line |
  | Plain beam or wall mark | **BOTTOM_CENTER** above / left of the member, **TOP_CENTER** below / right (the text grows away from it); vertical members rotated 90° | a small visible gap from the member face (BANWA2 R08: 0.4 h = 0.8 mm) |

  Walls are marked at the midpoint of each reference wall span; a type mark is repeated per span where needed.
- **Collisions**: first take the other permitted side (or another column corner, FP10.4); keep the midpoint, the
  bracket decision, the anchor and the bracket offset. Never increase a bracket offset, change an anchor or clip a
  member to make a check pass; genuinely unresolved crowding goes to an enlarged view or a review item. A secondary
  beam framing in at the middle of a main beam is cleared by putting the bracket on the other side (this replaces the
  earlier "middle of the nearest clear segment").
- **The bracket** (user, 2026-10-06, second review): a **solid grey line** (colour 8, layer `S-BRACKET`) parallel to
  the member; **both ends a 45° diagonal** whose size is the **text height** (dx = dy = 2.0 mm plotted) for a beam
  mark, or the **mark circle's diameter** for a circled (truss) mark; the diagonals **end on the member's start and end
  lines** (a beam: its face at the column face; a truss: its chord at the post face); the mark sits **in a gap in the
  bracket line**, centred on it (`bw_plans.bracket_mark` of job BANWA2).
  Worked example: BANWA2 S-102, B1A edge girders of the chiller floor (one mark per column bay, not one per joist).

### FP10.3 Slabs: the slab tag
- Office block **`Sym-SFL`**: a box with the slab mark on top (`S1`) and `SFL. | +7.50` below; thickness added where
  it differs from the typical (`(150 THK.)`, RC §14.3).
- One tag per panel, **placed in its slab panel** where it reads best (normally near the centre), clear of beam tags,
  hidden beam lines and the AR background text. It **does not need to line up with the AR room tag** (user,
  2026-10-04: "ST floor tag could be place in slab panel no need to align with AR tag"): the ST tag belongs to a
  slab panel, the AR tag to a room, and the two seldom coincide. A slab at a different level (toilet, balcony, step)
  has its own tag.
- Text 2.0 mm (FP6.2).
- **Slab tags are transparent** (user, 2026-10-09: "remove the white background from slab tags and make them
  transparent"): border and text only; no wipeout, no white fill and no clipping of the geometry under the tag (the
  drop-panel outlines clipped round a tag made it look opaque). The lines under a tag stay drawn.

### FP10.3a One-way and precast slabs: the plank symbol
- A one-way slab, hollow core or plank floor carries the office block **`Plank_sym`** (K.Nat plan legend "Plank No."):
  an **arrow in the span direction**, 9.88 mm long, with a **half head at each end on opposite sides**, the slab mark
  over it (`HC1`, bold) and the level under it (`SFL+5.95`, the block's own form without a space), text 2.0 mm (user,
  2026-10-07: "use HC1 (hollow core slab as one way slab) use proper symbol place on every slab panel").
- **One symbol in every slab panel** (the slab between the beam faces), the arrow across the panel's short side - the
  span onto the supporting beams.
- Placement, like the slab tag (FP10.3): in its panel, nearest the centre, clear of marks, brackets, symbols and grid
  lines; a spot 5 mm clear of marks is preferred, 0.4 mm from lines and 1 mm from text is the least. A span up the
  sheet: the arrow vertical and the two lines beside it, reading from the bottom. A panel narrower than the level
  text: the level in two lines under the arrow (`SFL` / `+5.95`). The arrow shortens (to 5 mm) where a bracket
  leaves less room; never across a beam face.
- Legend entry and a plan note: what the mark is (precast hollow core, one-way), who designs it (depth, topping,
  bearing), and that the analysis model's slab must transfer its load one way onto the supporting beams.
- Worked example: BANWA2 S-102, 2F slabs HC1 in all 82 panels; the RC roof keeps its cast-in-place slab tag
  (`bw_plans.slab_panels`, `hc_panels`, `plank_sym`).

### FP10.4 Columns and footings
- Floor plans: column mark beside each column, outside the slab tag area, consistent position (lower right) [REC].
- **The column mark sits at a corner of the column symbol** (user correction, 2026-10-09, BANWA2 S-106 R08): above
  right = BOTTOM_LEFT, above left = BOTTOM_RIGHT, below right = TOP_LEFT, below left = TOP_RIGHT, with the same
  clearance. Take the first clear corner of the four, checking the whole text box against brackets, wall marks, grid
  lines, dimensions and the neighbouring marks; never a free-floating label in the bay. The mark does not change the
  symbol's state (continuing, lower-only, CX).
- Foundation plan: footing and column together at the footing's lower right, `F4,C1` [OFFICE; EIT §14.2].
- Every footing has its column, or a note of what it carries (SSK S1-01: an F2 in bay 12 – 13 with no column).

### FP10.5 Other members
- Stairs `ST-n`, lift walls `W-n`, steel members by designation ("H 200x200x8x12 - 49.90 kg./m."), canopy and tank
  slabs by their slab tag. In every table and schedule a steel section is followed by its weight per length,
  `PG 139.8x4.5 (15.01 kg/m)` (user, 2026-10-07; steel S3.8).
- **Trusses on a plan**: one erection mark per **support span**, marks shared only by spans of the same length and the
  same sections, each with a bracket over the span and the circled mark at its middle (steel S3.7).

---

## FP11. Levels [EIT §9; OFFICE; USER rule on finish]

### FP11.1 Datum
- Every plan set states the datum once, on the general-notes sheet and in each plan's notes: "±0.000 = … (e.g. top
  of road at the entrance) = MSL +x.xxx". SSK AR: ±0.00 = public road; the ST model space carries "REFERENCE LEVEL
  +73.00 = FFL +0.000", which disagrees and must be settled (open, D5).

### FP11.2 Structural levels [USER 2026-10-04]
- Floor levels on structural plans are drawn as **SFL, structural floor level**: the top of the structural slab
  (user, 2026-10-04: "usually for floor level we draw as SFL which stand for structural floor level"). The
  architect's level is **FFL, finished floor level**, on the AR plans only.
- **SFL = FFL − 50 mm** as the usual rule (user, 2026-10-04: "usually −50 mm from FFL"): `project.FINISH` = 50.
  Where a floor's finish is thicker or thinner (wet areas, raised floors, roof decks with screed and waterproofing),
  the engineer sets that finish (`FINISH_BY_CODE` per AR finish code) and the SFL follows it. Every SFL that is not
  FFL − finish is deliberate and shows as a step (FP9.5).
- Never copy a plan to the next floor without re-reading every level against that floor's AR plan (SSK 4th floor:
  bay 12 – 13 tagged +7.45, the 3rd-floor toilet level, under an AR roof deck of +10.70).
- Units and decimals: one choice per set (open, D1). EIT: metres, 3 decimals (`+7.500`); SSK sets: metres,
  2 decimals (`+7.50`).

### FP11.3 Level changes
- Slab steps: step symbol (FP9.5). Ramps: arrow with the levels at each end. Roof falls: `SLOPE` arrow with the
  fall (RC §14.4).

---

## FP12. Dimensions on plans [EIT §8; guide §2.4, §2.4.1]

Dimension what is needed to build and nothing twice:
1. **Grids** (FP8): chain and overall, top and left.
2. **Members off the grid**: column faces or centres that are not on a grid, eccentric beams, beams between grids,
   from the nearest grid.
3. **Slab edges and cantilevers** from the grid (SSK 3rd floor: the 1.225 m overhang north of A was not dimensioned
   on the ST plan).
4. **Openings**: size and position from the grid.
5. **Steps and level changes**: position from the grid.
6. **Joints**: position and width.

Rules: tiers in order from the object outward (shortest chain nearest), never crossing, never through text; outside
the plan where possible; inside a bay only for an item that has no edge outside (guide §2.4.1). Dimension text 2.0,
parallel to the line, reading from the bottom or right (EIT §8.3).

---

## FP13. By type of plan

### FP13.1 Pile plan [RC §14.1]
Grid; every pile with its type symbol (office `hexagonal_pile`, `I-Pile`, explained in the legend); pile-cap outline
hidden for reference; pile positions dimensioned from the grid; **pile cut-off level** and **pile tip level** (boxed
or in the notes); pile type, size and capacity in the notes.

### FP13.2 Foundation plan [RC §14.2; OFFICE]
- **Piles under a pile cap are hidden** (user correction, 2026-10-08, BANWA2 SG02): a thin hidden pen (`S-PILE-I`,
  HIDDEN2) under the continuous, heavier cap outline, on the foundation plan and on the cap plan details. Check the
  plotted dashes on the small circles at 1:200 and on the details at 1:25 / 1:50; a layer named HIDDEN is not proof.
- **Pile arrangements in caps** follow the standard patterns (user, 2026-10-08, with the CRSI Design Guide for Pile Caps
  Fig. 4.4): 2 in a row; 3 in a clipped triangle with a flat head; 4 at square corners; 5 at four corners plus the
  centre; 6 in two rows of three; 7 staggered 2-3-2 and 8 staggered 3-2-3 in a rectangular cap; 9 in a 3 x 3 grid.
  Not a compact polygon chosen to reduce the cap area. Spacing and edge distance are project values (BANWA2: 3D and
  the engineer's edge distance). Reconcile cap areas and quantities across plan, details and schedules.
- **Every support is classified once**, beam, wall and slab connectivity checked (BANWA2: 17 tank-wall supports were
  missed by a column-only test); a wall load already in a support reaction is not added again.

Grid; footings (outline continuous, `S-Footing`) with piles inside; footing + column mark `F4,C1` at the lower right;
column stubs solid; **tie beams / ground beams** (mark `FB1`, `GB1`) where they are at this level; **lift pit**,
sumps and pits; top-of-footing level by note or tag; water-tank and equipment foundations (SSK: two 3 m³ tanks
beyond grid 15 with no support shown).

### FP13.3 Ground floor plan [RC §14.3]
The ground floor slab on beams (its beams are the ground beams): beam marks, slab tags, slab-on-grade panels (`GS`)
and fill concrete (office hatch, legend); steps to entrances and porches; link-way slabs and their boundary.

### FP13.4 Upper floor plans [RC §14.3]
All of FP9 – FP12. Column states change with each floor (FP9.1). Cantilevers, canopies at the level they are cast,
link bridges to their supports.

### FP13.5 Roof-deck and roof plans [RC §14.4]
Slab falls and drain positions, parapets with size, upstands, lift overrun slab and lift roof, column stubs (`CK`)
for future floors, roof structure by others (steel roof: steel S1).

A **steel roof** on an RC frame is drawn as its own plans, each at the plan scale with the sheet layout of FP1.2:
the column-top / RC roof framing plan (posts on the column tops, actual section), the **truss bottom-chord bracing
plan** (chords, struts, tie rods, truss marks per support span with brackets, FP10.5) and the **top-chord purlin
plan** (purlins, sag rods, ridge, slope arrows). The trusses themselves follow on key sections, elevations, joint
details and the bill (steel S4.12, S7.8, S1.6). Worked example: BANWA2 S-103 - S-105, then S-201 - S-206.

### FP13.6 Enlarged views
Stair cores, lift pits, congested corners at 1:50 with a callout on the plan ("DETAIL n/sheet", guide §9.7) and the
view title naming the parent sheet (`SYMBOLS.md` rule 3).

---

## FP14. Legend, notes and north arrow

### FP14.1 Legend (every plan sheet, same place) [OFFICE]
Column states (FP9.1), slab tag (FP10.3), structural floor level, step symbol, fill concrete hatch, existing-structure
hatch, pile symbols (foundation sheets), linetypes used (hidden beam, column below, joint). Only symbols that appear
on the set.

### FP14.2 Plan notes [REC]
`NOTE` block beside the legend: reference to the general notes and typical details (sheet numbers), the datum
(FP11.1), "SFL = top of structural slab", "Dimensions in …" (D1), scope notes (existing building, works by others),
joints.

### FP14.3 North arrow and key plan [EIT §3]
North arrow on every plan sheet, same size and place; the plan always drawn in the same orientation as the AR plans
(SSK: no north arrow on S1-01 – S1-04).

---

## FP15. Architectural background and coordination [USER 2026-10-04]

- The **current** AR plan of each floor is **xref'd** under the structural plan, all its layers forced to **colour 9**
  (light grey 0.13). It is never pasted or bound as blocks into the ST drawing: a pasted copy silently stays at the
  version it was pasted from (SSK revised file: AR plans of 4-3-69 and 5-3-69 under the 24-8-69 tender AR).
- AR layers that do not help the reader are frozen in the plan viewport (furniture, sanitary fittings, hatch patterns,
  dimensions) [REC]; walls, doors, windows, stairs and room names stay.
- The AR plan is placed by the grid (grid 1 / grid A on grid 1 / grid A), at its own scale (metres → × 1000).
- **Before every review and every issue, run the overlay check** (FP16): ST over AR, level by level, grid, levels and
  columns compared, findings numbered. Every finding is either fixed or answered.

---

## FP16. Production and checks

1. **Data first**: grid, levels, finish, marks and plan positions in `project.py`; sizes and marks from the design
   (never invented, AGENTS.md §2).
2. Draw with the engine and helpers (`DRAWING_ENGINE.md`); symbols only through their helpers (`SYMBOLS.md`).
3. **Overlay check** (SSK `overlay.py`): every plan against the current AR plan of its floor:
   - GRID: every bubble on its grid line (tolerance 5 mm);
   - LEVEL: AR FFL − ST SFL = finish ± 5 mm. Tags are compared by **area**, not by position (FP10.3): an AR tag with
     the ST tags of its bay, or the nearest ST tag within 6 m in the same row band (between the same two row grids)
     when its bay has none, and the same the other way; an ST tag with no AR tag near it is counted in a note, not
     reported as a finding (its room is tagged elsewhere);
   - COLUMN: position (50 mm), size, columns in one set only.
   Sheets `out\SSK_overlay_L<level>.pdf` and `OVERLAY_REPORT.md`.
4. Plot with the CTB (FP3) and LTSCALE 45 (FP4); **look at every sheet at print size** (AGENTS.md §2.5): text
   collisions, tags on lines, bubbles, dimensions on the plan, the title on a grid line.
5. Run the checklists: FP17, EIT §17, guide §8.

---

## FP17. Checklist (every plan sheet)

**Sheet**
- [ ] A1, office title block, title and number filled once, no stale text under them, revision row for this issue
- [ ] Plot style `STRUCT-A1-A2.ctb`, LTSCALE 45, PSLTSCALE 0, entity ltscale 1
- [ ] Project font (FP6.1) in every style, width factor as set, text 2.0 mm; no text below 2.0 mm
- [ ] North arrow, legend, plan notes, datum statement

**Grid and dimensions**
- [ ] Grid from the one source; bubbles top and left; close bubbles staggered; grid chain and overall dimensions
- [ ] Off-grid members, slab edges, cantilevers, openings, steps and joints dimensioned; no dimension crossing or on text

**Members**
- [ ] Column states correct for this floor (continuous / sits on beam / stops under), as in the legend
- [ ] Beams below the slab hidden, beams seen continuous; every beam marked along its span
- [ ] Every slab panel tagged with mark and SFL (and thickness where it differs); cantilevers and canopies too
- [ ] Openings and voids crossed and labelled; stairs and lifts marked with their detail sheets
- [ ] Existing structure hatched and labelled; joints shown with width on every floor
- [ ] Every footing has its column or a note; lift pit and equipment foundations on the foundation plan
- [ ] Steel framing plans: double lines at projected width, posts as actual section trimming the chords, tie rods one
  line each on `S-ROD`, purlins beside the posts, truss marks per support span with brackets (FP9.2, FP10.5)
- [ ] Tables: every steel section followed by its weight per length (FP10.5)
- [ ] Every vertical member classified below / above the cut; lower-only supports shown (FP9.1); walls hatched fine grey
- [ ] Slab edge at the physical member faces, not the mesh edge (FP9.3); slab tags transparent (FP10.3)
- [ ] Brackets only on receiving main beams and CX-carrying transfer beams; marks at span midpoints with the FP10.2
  anchors and offsets; column marks at symbol corners (FP10.4)
- [ ] Foundation plans: piles under caps hidden, standard pile patterns, every support in one cap (FP13.2); cap
  sections numbered on the cap plans with the exact cut-bar counts (RC §15.1)

**Coordination**
- [ ] Overlay check run against the current AR; every finding fixed or answered
- [ ] Every SFL = AR FFL − finish, or a deliberate step shown
- [ ] AR background xref'd, colour 9, current version; no pasted AR blocks

**Readability (at print size)**
- [ ] No tag, mark or note on a line; title clear of grid lines; nothing overlapping

---

## FP18. Open decisions (for the engineer)

| # | Question | Options | Until decided |
|---|---|---|---|
| D1 | Units on plans | EIT: dimensions mm, levels m 3 dp (`+7.500`) / SSK sets: metres, dimensions 2 dp (`5.00`) and levels 2 dp (`+7.50`) | Follow the existing project set (SSK: metres) and state it in the notes |
| D2 | Pens | `STRUCT-A1-A2.ctb` (FP3) / the legend table in the office model space (different values) | The CTB governs |
| D3 | Heights other than 2.0 mm | Grid bubble 3.3 (Ø 6.6), view title 4.0 and its scale line 2.5, slab tag block 1.5 | Office values for bubble and title; slab tag and scale line at 2.0 |
| D4 | Drawing numbers | Project series `S1-01` / EIT `PPPP-ST-3xxx-G-RR` | Project series |
| D5 | Datum | "±0.00 = public road" (AR) / "REFERENCE LEVEL +73.00 = FFL +0.000" (ST model space) | Ask before the first issue |
| D6 | Column stopping under | X in the outline (office legend) / hidden outline (EIT) | Office X |
| D7 | Hidden beam pen | 0.20 (colour 7, office) / one step heavier, as the slab edge (EIT Table 2.3 at A1) | Office 0.20 |

---

## FP19. History

| Date | Change |
|---|---|
| 2026-10-04 | Written for job SSK before its plans are drafted: office practice read from the SSK structural file, the user's rules of the day (plot style, LTSCALE 45, colour 9 background, cordia.shx 0.90 at 2.00 mm with the font a project setting), the SSK review findings as "never" rules, open decisions D1 – D7 |
| 2026-10-04 | FP11.2 SFL = FFL − 50 mm as the usual rule, and FP10.3 slab tags placed in their panel, not aligned with AR tags (user); the overlay check compares levels by area |
| 2026-10-06 | Review of the BANWA2 plans (user): main beams marked once per column bay with a length bracket (FP10.2); opening cross on the grid linetype, colour 8 (FP9.4, `S-OPEN`); no moment-release symbols on plans and steel framing as double lines at projected width (FP9.2); steel posts as their actual section (FP9.1); truss marks per support span (FP10.5, steel S3.7) |
| 2026-10-06 | Second BANWA2 review (user): the bracket solid grey with 45° ends of the text height / mark diameter, ending on the member's start and end lines (FP10.2, `S-BRACKET`); chords trimmed by the posts on every roof plan; tie rods one line each on the grid linetype (FP9.2, `S-ROD`); layers added to FP5 |
| 2026-10-06 | BANWA2: purlins on post rows beside the post (FP9.2, steel S7.8); steel roof plan set described (FP13.5) |
| 2026-10-07 | Weight per length after every steel section in tables (FP10.5, steel S3.8); FP17 steel items |
| 2026-10-10 | From the user's corrections of 08 - 09/10 recorded in the BANWA2 work transfer R01 of 09/10/2026, `instructions/PLAN_ANNOTATION_IMPROVEMENT.md` and `DRAWING_QUALITY_LESSONS.md`: vertical members classified below / above the cut, RC walls with a fine grey hatch (FP9.1); slab edge at the physical member faces (FP9.3); mark at the reference-span midpoint, bracket only for receiving main beams and transfer beams carrying CX columns, MIDDLE_CENTER bracketed / BOTTOM-TOP_CENTER plain anchors, collision order (FP10.2); transparent slab tags (FP10.3); column marks at symbol corners (FP10.4); piles under caps hidden, standard pile patterns, every support classified once (FP13.2) |
