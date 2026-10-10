# Symbols Catalogue (all structure types)

One table of every graphic symbol used on the drawings: what it looks like, its layer, the helper that draws it and
the rule behind it. **Draw a symbol only with its helper**, never by hand, so it is the same on every sheet.

- Placement of symbols among the notes: `ANNOTATION_ALIGNMENT_GUIDE.md`.
- Lines, pens, levels, marks, callouts in the EIT standard: `DRAWING_STANDARD_EIT-011006-19.md`.
- Engines:
  - `td` = `drafter/td_engine.py`, the general engine for any set;
  - `steel` = `drafter/steel.py`, the steel layers and helpers on top of `td`;
  - `srt` = `jobs/steel_roof_truss/srt_engine.py`, helpers tied to the SRT truss geometry (chord, branch, branch
    welds).
  A new set imports `td`, and `steel` when it has steel.
- Sizes are **plotted (paper) mm**. Helpers take the view scale `S` and draw at S × the paper size.

General rules:
1. **One meaning per symbol in a set.** If a symbol has more than one form in the set, the key on the general-notes
   sheet explains each form. Examples: the weld key on SRT-ST-1001, the bar-end key on RC sheets.
2. **Symbols are annotation.** They never overlap geometry, dimensions or notes. A symbol in the way of a leader is
   moved; the leader is not bent round it.
3. **Every reference symbol resolves.** A section or callout names the sheet where its view is drawn, and that view's
   title names the parent sheet.

---

## 1. Reference symbols (any structure)

| Symbol | Drawn as | Layer / pen | Helper | Rule |
|---|---|---|---|---|
| **Cutting plane** (section) | EIT: chain 0.25 with a split bubble at each end, its triangle pointing the viewing way. Office (busy views): **end strokes only**, heavy, outside the object, with arrows of 4.5 mm to the viewing side and the label "n/sheet". Sections look left or down | `S-CUTL` 0.25, pen 6 | `steel.cutmark(..., ends_only=True, lab="end"/"side")` | EIT §11; guide §9.4 |
| **Section / detail title** | Underlined title, 2.8 mm bold, "SCALE 1:n" below. A split bubble Ø9.2 at the right end: ID 2.8 bold above, sheet 2.0 below. Filled triangles for a section; none for a detail | `S-TITL` | `td.view_title(..., triangles=)` | EIT §11; guide §6 |
| **Detail callout** | Office (2026-10-03): a **dashed circle** round the enlarged area, and a leader landing on the circle edge in clear space to the note "DETAIL n/sheet - WHAT". EIT alternative, used on dense views (user 2026-10-06): the dashed circle plus a short leader to a split bubble "n / sheet" in clear space | `S-CALL` HIDDENX2, 0.25, pen 6; bubble `S-SYMB` | `steel.detail_callout(..., at=angle)` + `leader()`; dense views: BANWA2 `truss_details.callout_bubble` | EIT §11; guide §9.7 item 6 |
| **Member length bracket** (plans, key sections) | A solid grey line parallel to the member at the size of its 45° end diagonals, the diagonals ending on the member's start and end lines (beam: face at the column face; truss: chord at the post face); the mark (beam text, truss circle, key-section split bubble "mark / sheet") in a gap at the middle. Diagonal = text height for a beam mark, the circle / bubble diameter for a truss mark | `S-BRACKET` colour 8 | BANWA2 `bw_plans.bracket_mark`, `truss_details.key_section` | FP10.2; steel S3.7, S4.12 |
| **Grid line and bubble** | Grid line in the centre linetype (chain), letters on the short direction and numbers on the long, in circles at the line ends | Line `S-CENT` 0.18 (RC) or `S-GRID` grey (steel); bubble `S-SYMB` | `td.grid_bubble()` | EIT §7 |
| **Level mark** | Open datum triangle, apex on the line (2.4 wide, 2.0 high), with the value and description 2.0 mm above the line, **outside** the view. Values in m, 3 decimals (`+0.600 TOP OF WALL`). Benchmark: `TBM` boxed with an upward triangle. On elevations and sections of steel structures the **level line is grey ACI 8 in the grid linetype**, whether it runs across the view (e.g. along all the post bases of a key section) or is a short line beside a support; triangle and value as usual (user, 2026-10-06: "colour 8 grid linetype", then "make the elevation level lines grey too"; BANWA2 S-201 - S-204, `truss_details.level_grey`) | `S-ANNO`, text `S-TEXT`; the steel level line `S-GRID` | `td.level()`; steel: triangle + value, line on `S-GRID` | EIT §9; guide §2.5 |
| **Break line, straight** | A straight line with one Z in the middle, past the object on both sides. For whole views, RC, open sections and plates | `S-BREAK` grey 0.18 | `td.zbreak()` | EIT §0, Table 2.3 |
| **Break, round tube** | One half a single arc bulging toward the broken-away part; the other half a lens. Square to the member axis, sagitta about R/4, no inner-wall loop. Hidden wall lines stop on the break curve | Member layer | `steel.chs_break()`, `steel.break_point()` | Steel S4.5; guide §9 |
| **Match line** | Long dash-dot-dot, 0.35 | `S-MATCH` | – | EIT §0 |
| **Table title** | "TABLE n - NAME" above the table; notes cite "TABLE n" only | `S-TEXT` | `td.TABT()`, `td.TAB()`, `td.tbl(title=)` | guide §6; R2 notes |

## 2. Annotation symbols (any structure)

| Symbol | Drawn as | Layer / pen | Helper | Rule |
|---|---|---|---|---|
| **Leader arrow** | Filled arrowhead 2.0 mm, its tip on the edge (never inside black, never inside a plate) | `S-ANNO` | `td.leader()`, `td.edge_tip()` | guide §2.1 – §2.2 |
| **Ring on a cut bar** | Open circle Ø = 2 × the drawn bar dot, round the dot; the leader starts on the ring | `S-ANNO` | `leader(..., ring=db)` | guide §2.1 |
| **Ring on a bolt / anchor / hole end-on** | Open circle Ø = 1.25 × the hole, centred on the bolt; the leader starts on the ring | `S-ANNO` | `leader(..., bolt=hole)` (`BOLT_RING_K`) | guide §2.1 |
| **Dot terminator** | Filled dot Ø0.7, for a point inside an area. Not used for reinforcement | `S-ANNO` | `leader(..., dot_tip=True)` | guide §2.1 |
| **Bar-mark bubble** | Circle Ø4.0 on the shelf, number 2.0 bold (1.7 for two digits) | `S-SYMB` | `leader(..., mark=n)` | guide §2 |
| **Numbered callout** | 4 mm circle with a thin leader to the bar or stirrup; the texts in a list beside the detail | `S-SYMB` | `td.callout()`, `td.callout_list()` | R2 `MODEL_SPACE_SHEETS.md` |
| **Member tag** | The mark in a circle (radius fitted to the text, at least 2.4), bold text, placed **beside** the member | Circle `S-SYMB`, text `S-TEXT` | `steel.tag()`, `steel.place_tag()` | guide §9.2 |
| **Label on the member** | Text inside the member's own band, no leader | `S-TEXT` | `td.text()` | guide §9.8 |

## 3. Concrete symbols

Full rules: `docs/concrete/RC_DRAWING_RULES_EIT-011006-19.md` §12, §19.4, §19.7.

| Symbol | Drawn as | Layer / pen | Helper | Rule |
|---|---|---|---|---|
| **Bar along its length** | Thick line on the bar centreline, bends filleted at R = 3.5 db. At 1:5 and larger, a true-width filled strip | `S-REBR` 0.50 main / 0.35 secondary | `td.bar()`, `td.strip()` | RC §12.1, §19.4 |
| **Bar cut in section** | Filled dot, true size, at least 1.1 mm | `S-REBR` | `td.dot()`, `td.rdot()` | RC §12.1, §19.4 |
| **Stirrup / tie / crosstie** | On the centreline, corners concentric with the corner bars, 135° hooks round one bar | `S-REBR-SEC` 0.35 | `td.stirrup()`, `td.crosstie()` | RC §19.4 |
| **Bar end, hook, lap** | Plain end (no tick); hooks drawn as bent; a lap splice drawn **cranked** alongside the other bar | `S-REBR` | `td.lap_crank()` | RC §19.7 |
| **Distribution line** (bar set) | Thin line across one representative bar, with 45° end ticks and a circle where it crosses the bar | `S-ANNO` | `td.dist_line()` | RC §12.2-4 |
| **Plain dowel end-on** | Open circle with a cross (a deformed bar is a filled dot) | `S-DWL` | `td.dowel_end()` | RC §19.4 |
| **Construction joint** | Zig-zag, tooth pitch 2.0, amplitude ±0.8 | `S-CJOINT` 0.25 | `td.zigzag()` | guide §2.5 |
| **Opening in a slab** | Outline plus an X across the void | `S-OPNG` 0.18 | – | EIT §0 |
| **One-way / two-way bars in plan** | Double-headed open arrow per direction, with the label | `S-ANNO` | – | RC §12.2-6, -7 |
| **Excavation slope** | Dashed grey line with a slope triangle on the fill side (legs 2 and 1, numbers 2.0) | `S-EXCV` grey | – | guide §2.5; EIT §19.6 |
| **Soil, fill, stone** | Undisturbed soil an `EARTH` band; selected fill `AR-SAND`; drainage stone `GRAVEL` | `S-HATCH` grey 0.13 | `td.earth_band()`, `td.hatch()` | EIT §19.6 |
| **Concrete** | In an RC drawing the RC section is **not hatched**: the bars are the subject. An element that is not the subject of the detail (beam stubs in a column detail, columns in a beam detail) is hatched grey ANSI31 at 1.6 mm pitch, and its bars are grey (focus rule) | `S-HATCH`; bars `S-REBR-NF` | `td.nf_hatch()` | EIT §19.6; `docs/concrete/README.md` |

## 3A. Plan symbols (floor, foundation and roof plans)

Full rules: `FLOOR_PLAN_DRAWING_INSTRUCTION.md`. Office blocks from the SSK structural file; no engine helper yet.

| Symbol | Drawn as | Layer / pen (STRUCT-A1-A2.ctb) | Office block | Rule |
|---|---|---|---|---|
| **Column, continuous** | Outline solid filled | `S-CONT_COL` 1 → 0.25 | `Col-Continuous` | FP9.1 |
| **Column sits on beam** | Outline half filled on the diagonal | `S-CX_COL` 1 → 0.25 | – | FP9.1 |
| **Column stops under** | Outline with an X (office) or hidden HIDDEN2 (EIT) | `S-HID_COL` 2 → 0.35 | `Col-Break` | FP9.1, D6 |
| **Slab tag** | Box: slab mark on top, `SFL. | +7.50` below; thickness where it differs | text 2 → 0.35, 2.0 mm | `Sym-SFL` | FP10.3 |
| **One-way / precast slab (plank)** | Span arrow 9.88 mm, half heads on opposite sides; mark over (`HC1`), level under (`SFL+5.95`); one per panel | text 2 → 0.35, 2.0 mm | `Plank_sym` (office); BANWA2 `bw_plans.plank_sym` | FP10.3a |
| **Step in a slab** | Step line with the step height and `UPPER FLOOR` / `LOWER FLOOR` | `S-EDGE_SLAB` | `Sym-Step` | FP9.5 |
| **Footing + column tag** | `F4,C1` at the footing's lower right | text 2 → 0.35 | – | FP10.4 |
| **Pile** | Office pile symbols, explained in the legend; under a pile cap the pile is **hidden** (user, 2026-10-08) | `S_Pile_I` 8 → grey 0.18; under a cap `S-PILE-I` HIDDEN2 | `hexagonal_pile`, `I-Pile` | FP13.1, FP13.2 |
| **Opening / void** | Outline plus X, labelled | `S-EDGE_SLAB` | – | FP9.4 |
| **Existing structure** | Outline, grey ANSI31 hatch, label | `S-HATCH` 8 | – | FP9.7 |
| **View title** | Thai (and English) title 4.0 underlined, `มาตราส่วน` / `1:100` below | `S-T200` 1, `S-TH` 7 | dynamic title block on `S-40Txt` | FP1.4 |
| **North arrow** | On every plan sheet, same size and place | – | – | FP14.3 |

## 4. Steel symbols

Full rules: `docs/steel/STEEL_DETAILING_INSTRUCTION.md` S4 – S5.

| Symbol | Drawn as | Layer / pen | Helper | Rule |
|---|---|---|---|---|
| **Weld symbol** | AWS A2.4: reference line, arrow (never collinear with it), basic symbol (arrow side below, other side above), size left and length right. Also all-round circle, field flag toward the tail, NDT letters, a tail reference, and a broken arrow for a bevel | `S-ANNO`, text 2.0 | `steel.weld()` | Steel S5; guide §9.3 |
| **Weld as seen** | 45° hatch only (ANSI31), spacing 1/3 of the leg; boundary on Defpoints (never plotted). A band along the joint plus the profile triangles at the silhouettes | `S-WELD` | `steel.weld_region()`, `weld_bead()`, `weld_band()`; `srt.weld_branch()` | Steel S4.7 |
| **Work point** | Small cross in a circle, "WP" | `S-SYMB` | `steel.wp_mark()` | Steel S2.1 |
| **Centre / work line** | Grey chain, EIT grid linetype, work point to work point | `S-GRID` grey 0.18 | `srt.chord(cl=True)`, `branch(cl=True)` | Steel S4.2 |
| **Bolt, hole, slot** | Hole: circle + centre mark; slot: two arcs + straight sides; centre marks grey | `S-BOLT`; `S-CENT` grey 0.18 | `steel.hole()`, `steel.slot()`, `steel.bolt_side()` | Steel S4.2, S8 |
| **Hollow section in section** | Outer + inner circle, the wall solid-filled. Never cross-hatched | Member layer | `steel.chs_section()` | Steel S4.1 |
| **Hollow-section wall in elevation** | Fine hidden line, grey, in every view; stops on the break | `S-STL-WALL` grey 0.18, fine hidden | `srt.chord(walls=True)`, `branch()` | Steel S4.1 – S4.2 |
| **Hidden steel** | A part behind another is dashed where it is covered | `S-STL-HIDN` grey 252, fine hidden | `srt_sheets.behind()`, `hide_under()` | Steel S4.2 |
| **Fly-braced node** | Open triangle under the node, mark FB1 | `S-SYMB` | `srt_sheets` (half elevation) | Steel S9A.6 |
| **Bearing on the elevation** | Triangle under the bearing; the sliding end has a line under its triangle. Labels PIN / SLOTTED | `S-SYMB` | `srt_sheets` (half elevation) | Steel S2.8 |
| **Concrete support, grout** | In a steel drawing the concrete is the support, not the subject: hatched `AR-CONC`; grout `AR-SAND` (finer) | `S-HATCH` | `td.hatch()` | Steel S4.6 |
| **Camber diagram** | Exaggerated profile with ordinates at every panel point; units in the title | – | `srt_sheets.camber_diagram()` | Steel S2.7 |

---

## 5. Adding a symbol

1. Check this catalogue and the EIT digest first. Do not invent a second form of an existing symbol.
2. Write a helper in the engine with a docstring that says what it draws, its sizes and the rule it follows.
3. Add a row here: drawn as, layer / pen, helper, rule.
4. If the set uses the symbol, put it in the key on the general-notes sheet.
