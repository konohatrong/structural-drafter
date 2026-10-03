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
