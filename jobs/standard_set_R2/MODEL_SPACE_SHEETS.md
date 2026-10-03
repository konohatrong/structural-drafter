# Standard set R2: typical details (started 2026-09-30)

> The engine described here (`td_engine.py`, `pens.py`) moved to `drafter/` on 2026-10-03 and is shared by every
> current set; the R2 content modules import it as `from drafter.td_engine import *`. Output unchanged.

R2 is a separate version of the typical-detail sheets. R1 (`jobs/standard_set`) stays frozen. General notes are not part of R2 (they are built in `jobs/standard_set`, `python build.py gn`); R2 cites their tables by number only, for example "TABLE 6".

## R2 rules (user decisions, 2026-09-30)

| Topic | R2 rule |
|---|---|
| Purpose | Typical details show the contractor the general practice where the design drawings give no detail |
| Scale | **Every view N.T.S.**, arranged at one dummy scale 1:25 (`SC` in `td_engine.py`). View titles read "SCALE N.T.S."; the title block reads N.T.S. |
| Members | **One catalogue for every view: `members.py`.** Column 400 × 400 (8-DB20), beam 300 × 600, secondary beam 250 × 450, slab 150, flat slab 200 + 50 drop, footing 1600 × 1600 × 600, cover 40 / 20, bars DB20 / RB9–DB10 / DB12. Only LENGTHS are shortened (break lines): storey 2400 (infill view 2000), span 3600, stubs, lap 600 drawn |
| Model space | Real size (1 unit = 1 mm). Sheet i occupies x = i × 460 × 25; a no-plot sheet edge (`S-SHEET`) and drawing area (`S-TB-AREA`) mark it. Detail blocks `DET-*` are inserted at scale 1 and hold their own annotation (2.0 mm text = 50 units). View titles, tables, notes and keys are paper-size blocks inserted at 25 |
| Paper space | One layout per sheet: the title block `TB-A3-NRW` (attributes) in paper space, one locked viewport at 1:25 |
| Linetypes | AutoCAD **acadiso.lin** definitions, verbatim; the five used are kept in `td_engine.py` (`ACADISO`), so a build needs no AutoCAD profile. **LTSCALE 3.75** (model), **PSLTSCALE 0**, MSLTSCALE 0 (set by plot.py and saved into the DWG). Plotted dash = pattern × 3.75 / 25 = 0.15 × the .lin value. Hidden = HIDDENX2 (1.9 / 0.95 plotted), fine hidden = HIDDEN (0.95 / 0.48), centre / cutting plane = CENTER (4.8 / 0.95 / 0.95 / 0.95), property = PHANTOM. Keep paper-space linetypes continuous: PSLTSCALE 0 applies LTSCALE there too |
| Pens | **By colour**: `PEN` in `td_engine.py` maps each ACI colour to one lineweight; `plot.py` builds `NRW-EIT-R2.ctb` from it. Layer lineweights are generated from the same table (screen only), never set by hand. 1 red 0.50 main bars; 30 orange 0.35 ties / stirrups; 4 cyan 0.35 cut concrete, title; 5 blue 0.25 seen concrete; 6 magenta 0.25 cutting plane, symbols; 3 green 0.18 leaders, centre lines; 2 yellow 0.18 dimensions; 7 white 0.18 text; 10 0.70 frame; greys 8 (0.18), 252 (0.25 hidden), 9 (0.13 hatch) screened 50 % |
| Tables | **Every table has a number and a name, "TABLE n - NAME"**, in one sequence for the standard set: general notes 1 – 10, typical details 11 – 20 in sheet order (11 column ties and splices, 12 max. tie spacing, 13 column call-up, 14 beam schedule, 15 beam reinforcement by frame type, 16 punching shear, 17 trimming bars at openings, 18 slab-on-ground joints and dowels, 19 slab thickness and reinforcement, 20 subgrade, fill and backfill under slabs on ground). Text cites a table by number only, "TABLE 18"; never "TABLE (1126)", "1002 TABLE 6" or "TABLE ABOVE" (user, 2026-09-30). The register is `TABLES` in `td_engine.py`: `TABT(key)` gives the title, `TAB(key)` the citation, and `tbl()` warns about a table without a number. A new table gets the next free number; renumbering means editing only `TABLES` |
| Leader form | **Chosen per target, mixed freely within a detail** (user, 2026-09-30). The target is a vertical line (bar, face, edge), a corner, a bar dot or ring, or an area: the note is placed at the target's height and gets **one horizontal segment**, no inclined leg and no angle at the arrow. The target is a horizontal line only (a slab face, a bar running along the view): the leader cannot run along it, so the note rises `RISE` = 3 mm and gets the **inclined leg** (45° / 60°) + horizontal run. When packing leaves a note within 2 mm of its target height, the arrow slides along a vertical target or inside an area to make the leader exactly horizontal (`_target_kind()`, `_rise()`, `_snap_tip()` in `td_engine.py`) |
| Units in notes | **Every length, depth, spacing, size and tolerance in note text, leaders and table cells carries its unit** ("TIES @ ≤ 150 mm", "THE TOP 150 mm OF THE EXISTING GROUND", "LAYERS ≤ 200 mm THICK AFTER COMPACTION"). The unit goes once after a range ("25 – 75 mm"), and schedule columns carry it in the header ("b × h (mm)", "S1, 2h ZONES (@ mm)"). What stays bare: dimension strings ("DIMENSIONS IN mm"), counts, factors, ratios, code clauses and bar marks. CBR is written as a percentage (user, 2026-09-30) |
| PSLTSCALE pitfall | **PSLTSCALE is stored per layout** (bit 1 of the LAYOUT flags). A layout created by ezdxf defaults to 1, and a `PSLTSCALE 0` typed once in the script only reaches the current layout. Only page 1 of each set plotted correctly; the others plotted every pattern × 25, so centre lines came out solid and hidden lines as 10 – 50 mm dashes (user: "weird linetype scale in 1123"). `finish()` sets `layout_flags = 0` on every layout and `plot.py` sends `PSLTSCALE 0` after each `CTAB`. Check by measuring dash lengths in the PDF on a page other than the first |
| CTB pitfall | ezdxf `PlotStyle.set_lineweight()` appends a new table entry on a float mismatch (0.35, 0.18 …); AutoCAD ignores entries past its 27 standard ones and plotted the ties at maximum width. `plot.py` sets the index of the nearest standard entry |
| Sheets | Same numbers as R1. Columns gained **1104** (column ends, special cases: roof, transfer beam, discontinued wall, masonry infill), because the 1:25 elevations fill 1101; the typical column notes moved to the foot of 1102 |

## R2 sheets (all done 2026-09-30)

Every R1 sheet number is kept. Where the 1:25 views no longer fit, a continuation sheet was added and the moved items are cross-referenced.

| Set | Sheets | Changes from R1 |
|---|---|---|
| Columns (4) | 1101 elevations + frame table · 1102 size change, joint, footing + column notes · 1103 tie types, splices · **1104** roof top, transfer beam, discontinued wall, masonry infill | Infill 1101/4 and 1102/7–9 moved to 1104; 1113 note 3 now cites 1104/2 |
| Beams (6) | 1111 three frame elevations · 1112 cut-off, cantilever, bar-end key · 1113 sections, supports, openings · 1114 levels, stepped beam, girder end · 1115 schedule · **1116** stirrup types, frame table, beam notes | Stirrup types 1111/4 moved to 1116/1 and the beam notes to 1116; the frame table moved from 1112. References updated: "1116 DETAIL 1", "1116 NOTE n", "KEY ON 1112". The placing diagram shows the end span and the interior span only |
| Slabs (8) | 1121 section, corner panel (with columns), notes, legend · 1122 flat-slab plan, column head · 1123 punching · 1124 openings + trimming table + notes + legend · 1125 steps, upstands, **cantilever (1125/5, from 1121/3)** + legend · 1126 slab on ground: IJ at a ground beam, thickened edge, joint layout, **slab on lean concrete (1126/4)**, joint / dowel table, notes · **1127** joints SJ / CJ / CJ at an existing slab / EJ + seal details A – C · **1128** slab table (Table 19), **slab on compacted fill (1128/1) + Table 20 subgrade / fill / backfill**; the flat-slab notes were deleted at the user's review | Slab-on-ground joints after Beca (below). The R1 flat-slab strip diagrams (1122) were deleted at the user's review; the later sheets moved up one number. The punching-section dimensions read s0 / s |

**Drawn lengths (N.T.S.; member sizes always from `members.py`):**
- storey 2400; beam span 3600; cut-off spans 3000;
- slab-on-beams plan 1800 × 2000;
- flat-slab bay 2200 (plan), 3000 (strips);
- openings plan 2000; joint-layout bay 1500;
- stubs 100 – 300.

**Drawing rules added after the R2 review (user, 2026-09-30):**
- **Row labels of dimension tiers** ("TOP BARS", "BOTTOM BARS", "STIRRUPS") sit directly in front of their row's first dimension, not in a left margin. `row_label()` in `td_engine.py` right-aligns the label before the row's first dimension and steps it left past any extension line of an outer row that rises through the row. Used on 1112/1, 1112/2, 1115/1, 1121/1, 1122/1–3.
- **Additional (extra) bars sit one gap off their main bar, at the same level in every span**: top bars one gap below, bottom bars one gap above. The lap crank of a continuous bar must end clear of the start of the next additional bar, and a lapped bar must start clear of the end of the previous one (1112/1: end-span bottom bars stop 150 past the interior face, the lap starts 250 before it; 1115/1: likewise).

**Beam elevations follow GD-01 (user, 2026-09-30).** Source: `C:\990 - Developing software\102 RC Beam\phase1-mockup\DRAWING_INSTRUCTIONS.md` (sheet GB-01). Applied to 1111/1–3, 1112/1–2 and 1115/1:

| GD-01 rule | R2 implementation |
|---|---|
| Grid bubbles, 7 mm circle, 2.8 mm bold letter, on a centre line through the column | `grid_bubble()`: A, B… on `S-CENT`, circle on `S-SYMB`, above the column stubs (1115: above the top dimensions) |
| Numbered callouts, 4 mm circle, thin leader to the bar or stirrup; the texts in a list | `callout()` + `callout_list()`: top-bar callouts above the beam, bottom-bar and stirrup callouts under the soffit; the list beside the detail replaces the long leader notes. Leaders must not cross (1112/1: callouts 2 and 3 both left of the column) |
| Zone band 3.6 mm high, 8.4 mm under the soffit, grey boxes; dimensions start at the band's bottom edge | `zone_band()` on 1111: STIRRUPS @ s (ordinary), 2h: s1 / MIDDLE: s / 2h: s1 (intermediate, special). The 2h chain dimension is dropped (the band carries it) |
| Column hatch ANSI31, 1.6 mm pitch, grey, the full column height shown | `frame_elev()` and `col_stack()` hatch on `S-HATCH` |
| Stirrups in elevation: hidden line, grey (secondary information) | New layer `S-STIR-ELEV` (ACI 8, 0.18, acadiso HIDDEN); `stirrups()` draws on it. Sections keep solid stirrups |
| Crank 1:6 max. (run = 6 × offset) | `lap_crank()` now 1:6 on every R2 sheet (it was 1:3) |
| Collinear bar ends ≥ 150 apart; extra bars on the cranked-bar level; the crank finishes before the next extra bar | 1112/1 and 1115/1 laps re-set: the end-span bottom bars stop 100 before the interior face's far side, the lapped bar starts 200 before the near face, and the top lap is in the middle third |
| Legend: bars, stirrups, section cut, grid line | The key is now **LEGEND**: plain end, hook, break, cranked lap, stirrups in elevation, grid line + bubble, callout |

Kept from R2 (not GD-01): EIT arrowheads (GD-01 uses ARCHTICK), acadiso linetypes at LTSCALE 3.75, pens by colour, and the TATA / 1112 cut-offs. The one difference is the additional bottom bars: GD-01 stops them Ln/8 from each face, while R2 uses 0.875 L1 at the end span and 0.70 L2 centred at the interior span. Section tags (END / MID / CONT pills) are not used, because the R2 schedule keys bars by letter (1115).

**Focus rule (user, 2026-09-30), every R2 sheet.** Each typical detail is about one element. Everything else is drawn as background:
- its concrete is hatched grey ANSI31 at 1.6 mm pitch (`nf_hatch()`), with a thinner outline where it is a stub;
- its bars go on `S-REBR-NF` (ACI 252, 0.25, grey), drawn solid, not hidden, because hidden already means "concrete below / hidden edge";
- its ties and stirrups seen in elevation go on `S-STIR-ELEV` (grey hidden).

| Set | In focus | Background |
|---|---|---|
| Columns 1101 – 1104 | column, its bars and ties | beam and slab stubs, roof beams, footings (and their mat), the transfer beam and its bars, the wall and beam above a discontinued column |
| Beams 1111 – 1116 | beam | columns (hatched, bars grey, ties grey hidden) |
| Slabs 1121 – 1128 | slab | supporting beams in section (hatched, stirrup and bars grey), column stubs and column bars, the ground beam, the existing slab (1127/3) |

**Exceptions**, where the other element's bars are the subject of the detail and stay full weight:
- the edge / corner joint (1102/5, section A);
- secondary beam on a main beam (1113/2, A);
- beam ending at a girder (1114/3);
- slab plans, where columns are cut and hatched as section.

**Masonry** is hatched AR-BRSTD (brick, real size), so it cannot be confused with background concrete (1104/4).

The legend has a row for it: "OTHER ELEMENT (NOT THE SUBJECT OF THE DETAIL): HATCHED GREY, ITS BARS GREY".

**Slab-on-ground content after Beca SE-1210 – 1219 (user, 2026-09-30);** see `REVIEW_BECA_SLAB.md`:
- joint marks SJ / SJD / CJ / EJ / IJ;
- `pour_header()` FIRST / SECOND POUR;
- `detail_ref()` circle + split bubble to seal details A – C;
- joint / dowel and trimming-bar tables by slab thickness;
- slab-on-ground sections at a dummy 1:10 (`SG`) and seal details at 1:2, all titled N.T.S. (in model space the blocks sit at 2.5 and 12.5; linetypes plot at the same dash lengths).

The Beca **panel-grid sheet layout was tried and rejected** by the user ("our style better"). Slab sheets use the column / beam layout:
- views top-aligned in rows from the top-left (`place_row()` in `td_slabs.py`);
- each title 6 under its own view, with a short note wrapped to the view width;
- notes, tables and legend stacked in the free space (`side_blocks()`).

**Layout lesson:** at 1:25 the height of a view is often set by its stacked leader notes, not by its geometry. Widening the note column is the cheapest fix; shorten lengths next; move notes or tables to a continuation sheet last.

---

## R1 guide (inherited, still valid for the block / capture mechanics)

> The text below is the R1 guide, kept as written. Paths and scripts it names are in `jobs/standard_set` (for example `compare_pdf.py`), and its "1002 TABLE 6" citations are R1 style: R2 cites "TABLE 6".

# Standard set: model-space sheets built from blocks

This folder builds the office standard sheets with a new structure. They plot the same as before.

| Set | Sheets | Content module |
|---|---|---|
| `gn` | STR-ST-1001 – 1003 general notes (Rev B) | `gn_notes.py` |
| `columns` | 1101 – 1103 | `td_columns.py` |
| `beams` | 1111 – 1115 | `td_beams.py` |
| `slabs` | 1121 – 1127 | `td_slabs.py` |

The earlier paper-space versions stay unchanged as the reference:
- `jobs/general_notes/` (Rev A frozen in `rev_A/`);
- `jobs/typical_details/`.

The notes, details and layouts themselves follow `TYPICAL_DETAILS_INSTRUCTION.md` and `GENERAL_NOTES_DRAWING_INSTRUCTION.md`. Only the way a sheet is assembled changed.

---

## 1. Structure

**Model space holds every drawing, as blocks.**

- Sheets sit side by side at paper size: 1 unit = 1 mm on the A3 sheet.
- Sheet *i* of a set sits at x = *i* × 460.
- Model space contains only block inserts.

| Block | What it is | Drawn at | Inserted at |
|---|---|---|---|
| `TB-A3-NRW` | Title block: frame, zones and title strip. Project and sheet data are attributes | Paper size | 1 |
| `DET-<sheet>-<id>` (e.g. `DET-1112-2`) | One detail or view: geometry, bars, leaders, notes, dimensions | **Full size, 1:1 mm**. Text and arrows sized for the scale (2.0 mm × scale) | **1/scale** (1:25 → 0.04) |
| `DET-1003-COVER / HOOKS / LAPS` | General-notes details, column-width figures (N.T.S. / 1:10) | Paper size | 1 |
| `VT-<sheet>-<id>` | View title with bubble and scale text | Paper size | 1 |
| `TBL-`, `NOTES-`, `KEY-<sheet>-<n>` | Tables, note blocks, bar-end symbol key | Paper size | 1 |
| `NOTES-1001-1` … `NOTES-1003-1` | Note columns of each general-notes sheet | Paper size | 1 |

**Detail numbering:** `<id>` is the number in the view-title bubble, so `DET-1113-A` is section A on sheet 1113.

**Detail base point:** the lower-left corner of the detail's extents.

**Layouts:** each sheet has one thin layout (tab `1111`, `1112` …) holding a single locked 1:1 viewport onto its model-space sheet. The layouts are used for:
- PDF plotting;
- sheet sets and publishing.

If you prefer, plot a window straight from model space; the result is the same.

**Dimensions inside a detail block** measure the block's full-size geometry. They read 5000, not 100, at any insert scale.

**Line types (tested in AutoCAD 2024):** AutoCAD draws a scaled block's line types at world size. Entity line-type scale therefore stays 1, and hidden or centre lines plot with their EIT dash lengths (3 mm, 8.5 mm …) at every detail scale.

---

## 2. Title block `TB-A3-NRW`

The drawing area is a rectangle on layer `S-TB-AREA`. The paper edge is on `S-SHEET`. Both layers are set to no-plot.

The block has these attribute tags, filled per sheet by the generator from `PROJ` and `SHEETS`:

| Tag | Content |
|---|---|
| `DWG_NO`, `SHEET`, `SCALE`, `DATE` | Drawing no., "SHEET x OF y \| A3", scale, date |
| `TITLE_1` – `TITLE_3` | Drawing title lines |
| `PROJECT`, `LOCATION`, `OWNER`, `OFFICE`, `OFFICE_ADDR` | Project data |
| `REV_1` … `REV_4`, with `_DESC` and `_DATE` | Revision rows (REV_1 = top row) |
| `KEYPLAN_1`, `KEYPLAN_2` | Key-plan text |
| `STATUS_1`, `STATUS_2` | Status stamp ("FOR REVIEW / NOT FOR CONSTRUCTION") |

**A project title block** is a new block with the **same attribute tags** and an `S-TB-AREA` rectangle.

In AutoCAD, redefine `TB-A3-NRW` with the project block: INSERT the project DWG under the name `TB-A3-NRW` and choose to redefine. The attribute values already on every sheet are kept (run `ATTSYNC` if needed). Then move the `DET` / `VT` / `TBL` / `NOTES` blocks into the new drawing area where needed.

**The sheet layouts are designed for A3.** A title block with a different drawing area (e.g. A1) needs the sheet layout in the content module (`sheet_11xx()`) changed. That is a positions-only edit: the details do not change.

---

## 3. Working in AutoCAD

| Task | How |
|---|---|
| Edit a detail | BEDIT `DET-1112-2`. Every sheet that uses it updates |
| Move a detail to another sheet or title block | Move the `DET` insert together with its `VT` title |
| Use a detail in a project drawing | INSERT `library/DET-xxxx-x.dwg` at 1/scale (scale in `library/INDEX_<set>.csv`) into a paper-size sheet. For full-size model work insert at 1 and set LTSCALE for the line types |
| New title block for a project | See section 2 |
| Change a detail's scale | Change it in the generator: the view's `S` and its `viewport(…, scale, …)` call. Scaling a block by hand scales its text and arrows too |

---

## 4. Build, plot, check

Build a set, or `all`. This writes `out/<set>.dxf` and `library/INDEX_<set>.csv`:
```bash
python build.py all
```
Plot every layout to PDF, save the DWG, and write the library DWGs (`-WBLOCK` of every `DET-*` and `TB-*` block). Run it from **PowerShell**, not Git Bash:
```bash
python plot.py all
```
Compare with the former paper-space PDF:
```bash
python compare_pdf.py out/STR-ST-1111_Typical_Beam_Details_A3_RevA.pdf ../typical_details/out/STR-ST-1111_Typical_Beam_Details_A3_RevA.pdf
```

**Result at the switch (2026-09-29):**
- 1001 was pixel-identical (before the change to 2.0 / 2.8 mm text, section 6).
- 1101 – 1127: no unmatched ink beyond anti-aliasing specks on grey lines (at most ~160 px per page at 150 dpi, all dash-phase or 1 px shifts).
- All four sets pass the Arial Narrow font check.

`compare_pdf.py` writes `_diff_p<n>.png`:
- red = ink only in the new PDF;
- blue = ink only in the reference.

---

## 5. Engine notes (`td_engine.py`)

- **`capture(fn, …)`** draws a view in model space and runs the leader layout as before. It then moves everything the view drew into a block `DET-TMP…`, with the base at the lower-left of its extents.
- **`viewport(ps, key, scale, px, py_top)`** now **inserts** that block at 1/scale. It uses the same window as the former viewport (extents + PAD), so every sheet layout call is unchanged.
- **`view_title(…)`** renames the detail just placed to `DET-<sheet>-<id>` and stores the title as `VT-<sheet>-<id>`.
- **`tbl`, `table`, `notes_block`, `bar_end_legend`** are wrapped by `group()`: what they draw becomes one block `TBL-` / `NOTES-` / `KEY-<sheet>-<n>`.
  - Content modules can wrap their own drawing the same way: `group("DET-1001-COVER", fn, …, g_kind="detail", g_title=…, g_scale=…)`.
  - The `g_` prefix keeps the index keywords apart from the drawing function's own. An earlier `title=` keyword silently swallowed `tbl(title=…)`.
- **`new_sheet(i)`** inserts `TB-A3-NRW` with its attributes and returns model space. The content module draws at paper coordinates (0 – 420, 0 – 297). When the next sheet opens, or in `finish()`, the sheet's inserts move to x = *i* × `SHEET_DX`.
- **`finish()`** closes the last sheet and adds the thin layouts. `build.py` calls it.
- **New layers:**
  - `S-DET`: detail inserts;
  - `S-SHEET`: paper edge, no plot;
  - `S-TB-AREA`: drawing area, no plot.

**Opt-in options (added 2026-10-03 for the steel set SRT; off by default, so the R2 sheets are unchanged):**
- `LEADER_ORTH = True`: straight or orthogonal L leaders, routed so none crosses another leader, a note or a dimension
  (ANNOTATION_ALIGNMENT_GUIDE §9.1). `ORTH_RISE` = 5 mm puts the note off a horizontal edge on the free side;
  `ORTH_LEG_MIN` = 3 mm is the shortest vertical leg an L may have.
- `leader(..., bolt=hole Ø)`: the tip is the bolt centre and the leader starts on an open circle of `BOLT_RING_K` =
  1.25 × the hole (§2.1).
- `WRAP_UNITS = True`: notes wrap with `drafter.fonts.wrap(..., keep_units=True)`, so a number never leaves its unit
  on the next line (§2.4.2).
- `check_dims()` ignores weld hatch (`S-WELD`) and hatch boundaries (`Defpoints`), and treats collinear dimension
  lines as one chain rather than a crossing.

**Review and checks:**
- `check_dims()` runs in `capture()` for every view and flags dirty dimensioning (ANNOTATION_ALIGNMENT_GUIDE §2.4.1).
- `dim(..., tside="L"/"R")` puts a small dimension's text outside its extension lines.
- `python crop_det.py <set> <DET-…>` crops a detail out of the plotted PDF for review.
- `render_block.py` renders a block without AutoCAD; its dimension text placement is approximate.
- `build.py` prints in UTF-8, because the warnings quote ≥, ℓ, ≈.
- **Layout guards:** `notes_block` warns when a block runs below the frame; `tbl` warns when a table runs into the title strip; `viewport` warns when a detail leaves the drawing area; `view_title` warns when its note falls below the frame. A text change on one view can push a neighbour out, so rebuild the whole set and read every `!!`.
- `plot.py` removes library DWGs of details that no longer exist in the set (e.g. `DET-1102-9` after the tie arrangements moved to 1103).

**Pitfalls:**
- Do not set an entity `ltscale` inside detail blocks: dashes would plot scale × too long, and short dashed lines become continuous.
- Keep one set per process. `td_engine` creates its document on import, and `build.py all` runs each set separately.

---

## 6. General notes at the normal text size (2026-09-29)

> **Issued as Rev B** (`out/STR-ST-1001_General_Notes_Concrete_A3_RevB.*`, drawing nos. STR-ST-1001-D-B … 1003-D-B).
> - Revision rows are set in `build()` from the sheet count. 1001 shows A "ISSUED FOR REVIEW" and B "TEXT 2.0 mm, n SHEETS"; 1002 onwards show only B "FIRST ISSUE (FROM 1001 REV A)".
> - Set in `gn_notes.py` (`PROJ["rev"]`, `REV_A_DATE`; the engine reads `td_engine.REVS` and `REVS_BY_SHEET`).
> - A revision description must fit its 38 mm column (about 30 characters at 2.0 mm).

At the user's request, the general notes use the **normal drawing rule** (`K = 1` in `gn_notes.py`):
- body text **2.0 mm**;
- headers **2.8 mm** (× 1.4);
- pitch 3.33 mm, table rows 5.2 mm, dimensions 2.0 mm.

Rev A (frozen in `jobs/general_notes/rev_A`) used K = 0.625 on a single sheet.

**The notes now take two sheets.**

| Sheet | Notes | Tables |
|---|---|---|
| **1001** | Sections 1 – 6.1 | Concrete schedule, sulfate exposure, hooks and bends, column ties |
| **1002** | Section 6 (from the lap table) to the abbreviations; the typical-details band under columns 2 – 3 (*two-sheet stage, before note 2.5*) | Lap and anchorage (table in section 6), cover (section 7), form removal, tolerances |

**How the flow works:**
- `Flow` runs column by column over sheets. Running column *c* = sheet *c* // 3, column *c* % 3.
- *(Superseded, see "Column layout on 1003" below.)* `plan()` took the fewest sheets that held the notes plus a details band ≥ `H_BAND` (55 mm), then raised the band line as far as the notes allowed. The build now takes the fewest sheets that hold the plain column flow.
- A table never splits. If it does not fit, it moves whole to the next column; that is why column 3 of 1001 ends early.
- `build.py gn` prints which sheet each table lands on.
- If the notes grow, a third sheet is added automatically.

**Details band** (1002, 206 × ~63 mm; *superseded by the column figures below*), relaid for 2.0 mm text:
- text is placed in measured sequence, not at fixed offsets;
- the cover section is 250 × 300 at 1:10;
- the lap stagger is drawn wider so "≥ 1.0 m CLEAR" fits between its extension lines;
- the band has no separate heading: each detail carries its own title.

**Cross-references:** the detail sheets cite general-notes tables by sheet, e.g. "LAPS PER 1002 TABLE 6" or "COVER … SEE 1002". "TABLE 6" means the table in note section 6. The lap and cover tables moved to 1002, so these references were updated.

**Whenever the general notes change pagination,** check `build.py gn`'s table list and grep the content modules for `100x TABLE` / `SEE 100x`.

**Project design data (note 2.5, added 2026-09-29).** `DESIGN_DATA` at the top of `gn_notes.py` holds the table rows; fill them in per project. `[ … ]` marks a value to complete.

| Item | Placeholder |
|---|---|
| Location | Province / district |
| Seismic zone | Per the ministerial regulation |
| Seismic importance factor Ie | 1.0 / 1.25 / 1.5 |
| Seismic design category | B / C / D |
| Seismic-resisting system, X and Y directions | System, R, Ω0, Cd (DPT 1301/1302-61 Table 2.3-1) |
| Design wind speed and wind zone | DPT 1311-50 |
| Wind return period for ultimate design | Years |

**Effect on pagination:** with the table, the notes take **3 sheets**:

| Sheet | Contents |
|---|---|
| 1001 | Sections 1 – 5, with the design data, concrete schedule, sulfate and hooks tables |
| 1002 | Column ties, lap, cover, form removal and tolerance tables; the notes run to section 12 |
| 1003 | Sections 13 – 14 (inspection; foundations and piles) and the abbreviations (three column lists), then the three typical details as column figures from column 2. The rest is free for project notes |

The lap (section 6) and cover (section 7) tables stay on 1002, so the "1002 TABLE 6" / "SEE 1002" references in the detail sets are still correct.


**Column layout on 1003** (2026-09-29, user: "as column" / "column align"):
- **Abbreviations** are a column list (`Flow.terms`): the term in bold at the column edge, the meaning 22 mm in, one per line.
- **Typical details** are column-width figures in the note flow (`Flow.detail`), after the abbreviations. The former band under columns 2 – 3, with its own widths, is gone, and so are `H_BAND` / `plan()` band balancing.
  - Each detail is measured once at the column width (`detail_h`) and placed whole, with 6 mm above it.
  - Each is drawn afterwards as its own block `DET-<sheet>-COVER / -HOOKS / -LAPS` at its flow position, so its edges sit on the note-column grid.
  - There is no separate "TYPICAL DETAILS" heading: each detail has its own underlined title.
- Column rules are drawn only between the columns a sheet actually uses.

**Abbreviations** (2026-09-29, user: add rebar position and general detailing terms): three titled column lists in `gn_notes.py`.

| List | Contents |
|---|---|
| `ABBR_GENERAL` | Materials, drawing terms (TYP., SIM., N.T.S., C/C, CLR., CL, THK., EL., FFL / SFL, CJ / EJ, SOG), standards |
| `ABBR_REBAR` | Call-outs n-DBxx, DBxx @ s; positions T / B, T1 / T2, B1 / B2, EF, NF / FF, IF / OF, EW, ES; ADD., CONT., ALT., STR. / TIE / HOOP |
| `ABBR_SYMBOLS` | Symbols used on 1101 – 1127: ℓn, L1 / L2, Lc, Sn, h, d, bw, c, c1 / c2, Hc, lo, s, s0 / s1, hx, db / dt, Ld / ldh |

Two terms were fixed so no abbreviation carries two meanings:
- `Sn` now means only the slab clear short span (the old "ss, Sn = standard deviation" entry is now "ss").
- `EQ.` is not listed, because the notes use it for equation numbers.

**When a new detail set introduces a symbol or position mark, add it to these lists.** The details now start in column 2 of 1003.

**Table numbers** (2026-09-29, user): every table is titled "TABLE n - NAME", numbered by `Flow.table` in flow order.

| No. | Table | Sheet |
|---|---|---|
| 1 | Project design data | 1001 |
| 2 | Concrete schedule | 1001 |
| 3 | Sulfate exposure | 1001 |
| 4 | Hooks and bends | 1001 |
| 5 | Column ties | 1002 |
| 6 | Lap and anchorage length | 1002 |
| 7 | Minimum clear cover | 1002 |
| 8 | Recommended cover, aggressive exposure | 1002 |
| 9 | Form removal | 1002 |
| 10 | Construction tolerances | 1002 |

Where the old references pointed:
- The old "TABLE 6" (lap) and "TABLE 7" (cover), which meant the table in section 6 or 7, are Tables 6 and 7 in sequence as well. The references on 1101 – 1127 are therefore unchanged.
- "BENDS: TABLE IN 5" is now "TABLE 4".
- Note 2.5 cites "TABLE 1".

`TABLE_REFS` in `gn_notes.py` lists every table cited by number, with the sheet cited alongside it: "1002 TABLE 6" on the detail sheets. The build prints `!! table cited as TABLE n …` if a table's number or sheet changes; then update the references.

**Headers keep with next** (2026-09-29, user: "7. CONCRETE COVER" was left alone at a column foot):
- `Flow.header()` only records the header.
- The next paragraph, table or figure places it (`_head(h)`), in the column where its own first lines, or the whole table, also fit.
- A header therefore never ends a column.

Tables are still never split. A column can end short when the next table is taller than the space left (for example 1002 column 1, before the cover table).

**Additions after the ACI MNL-66 review (2026-09-29):** see `REVIEW_ACI_MNL66.md` in the root.

| Where | Addition |
|---|---|
| Table 1 | Site class, S<sub>DS</sub> / S<sub>D1</sub>; analysis method; members of the seismic system; live loads by use and roof; superimposed dead load (finishes, services, partitions); live-load reduction and special loads. All `[ ]` placeholders; still Table 1, so nothing renumbers |
| Table 6 | Rows for straight tension ld and compression ldc = 0.24 fy db / √f'c ≥ 0.043 fy db ≥ 200. The note says hooks do not count in compression, the values apply conservatively to higher grades, and ld per EIT 12.2.3 where the cover / spacing conditions are not met |
| Note 5.6 | Footing and ground-beam bottom bars on blocks; top-mat chairs by the contractor (engineer-designed for mats ≥ 1.2 m); bar dimensions out-to-out including hooks |
| Note 6.1 and the lap detail | "Stagger laps ≥ 1.0 m" and "≤ 50 % lapped" are U.N.O.; column and wall verticals may lap at one level per their details |
| Note 8.5 | Anchor bolts set with templates; non-shrink grout 25 – 50 under base plates |
| Note 11.5 | Joint-layout submittal where joints are not shown |
| Section 14 (new, appended) | Foundations and piles: soil report and bearing / pile data, pile tests, tolerances, heads and embedment, lean concrete, dewatering, fill. Appended so no section or table renumbers |
| Table 5 note | Intermediate and special frames: deformed hoops and crossties, DB10 minimum (decision D3) |

**Rule learned:** add general-notes content without renumbering whenever possible, by extending an existing table or appending a section. Then check `build.py gn`'s table list against `TABLE_REFS`.
