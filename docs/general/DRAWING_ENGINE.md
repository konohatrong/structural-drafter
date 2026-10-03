# Drawing Engine Reference (`drafter/td_engine.py`, all structure types)

How the shared engine builds a drawing set: the model-space structure, the blocks, the title block, linetypes and
pens, the functions a job calls, the checks, how to work with the output in AutoCAD, and the pitfalls. It applies to
every current set (the R2 typical details, the SRT steel truss) and to every new one.

- The pipeline around the engine (calc → build → look → plot → test → review), commands and environment:
  `DRAWING_PRODUCTION.md`.
- Where annotation goes: `ANNOTATION_ALIGNMENT_GUIDE.md`. Symbols and their helpers: `SYMBOLS.md`.
- History: the engine was written for the standard set R1 (`jobs/standard_set/MODEL_SPACE_SHEETS.md`, 2026-09-29),
  extended for R2 (`jobs/standard_set_R2/MODEL_SPACE_SHEETS.md`, 2026-09-30) and for the steel set SRT
  (2026-10-03), and moved to `drafter/` on 2026-10-03 with the output unchanged.

---

## 1. Using the engine in a job

```python
# <job>/<job>_engine.py
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))          # repository root: the drafter package
sys.path.insert(0, str(HERE))

from drafter import td_engine                     # the module, to set options
from drafter.td_engine import *                   # the helpers
PROJ.update(code="ABC", project="...", date="dd/mm/yyyy", stage="D", rev="A")
td_engine.REVS = [("A", "ISSUED FOR REVIEW", PROJ["date"])]
td_engine.KEYPLAN_2 = "(...)"
td_engine.LEADER_ORTH = True                      # opt-in options (section 6)
td_engine.WRAP_UNITS = True
TABLES.clear(); TABLES.update({"KEY": (1, "NAME"), ...})
from drafter.steel import *                       # steel sets only: steel layers + helpers
```

- **One document per process.** `td_engine` creates its DXF document when it is imported. Build one set per process;
  a driver that builds several sets runs each in its own process (`build.py all` in R2).
- **Set options on the module** (`td_engine.LEADER_ORTH = True`), not on a star-imported copy of the name.
- **Never copy the engine into a job.** Change it in `drafter/`, keep a new behaviour opt-in, and run every test.

| Project data / option | Meaning |
|---|---|
| `PROJ` | Code, owner, project, location, office, date, stage, revision: fills the title block and `dwg_no()` |
| `SHEETS` | `[(series, [title lines], scale text), ...]`, one per sheet, in order |
| `REVS`, `REVS_BY_SHEET` | Revision rows for every sheet, or per sheet (a sheet added at a later revision) |
| `KEYPLAN_2` | Key-plan text, e.g. "(TRUSS T1)" |
| `STATUS` | Title-block status stamp, two lines. Default `("FOR REVIEW", "NOT FOR CONSTRUCTION")`; set for an official issue (`standard_drawings/README.md` §2). A one-line stamp (second line empty) is centred in its box |
| `TABLES` | Table register: key → (number, name). `TABT(key)` gives "TABLE n - NAME", `TAB(key)` the citation "TABLE n" |
| `SC` | Arranging scale of the sheet composition (25) |
| `LEADER_ORTH`, `WRAP_UNITS` | Opt-in options (section 6) |

The build driver (`build.py`) then does: build the views and sheets, `finish()`, delete `Layout1`, audit the DXF
(audit errors go through `warn()`), save the DXF, write the block index (`index_csv`), and exit 1 if
`td_engine.WARNINGS` is not empty. `jobs/steel_roof_truss/build.py` is the shortest example.

## 2. Model space and blocks

**Model space holds every drawing at real size** (1 unit = 1 mm), as blocks.

| Block | What it is | Drawn at | Inserted at |
|---|---|---|---|
| `TB-A3-NRW` | Title block: frame, zones and title strip; project and sheet data are attributes | Paper size | 1, in each **layout** (paper space), not in model space |
| `DET-<sheet>-<id>` (e.g. `DET-1112-2`) | One view or detail: geometry, bars, leaders, notes, dimensions | **Real size**; text and arrows sized for the view scale (2.0 mm × S) | `viewport()` places it at 1/S on the paper-size sheet, which is then scaled by `SC`: SC / S in model space (1 for a 1:25 view, 2.5 for 1:10) |
| `VT-<sheet>-<id>` | View title with bubble and scale text | Paper size | `SC` |
| `TBL-`, `NOTES-`, `KEY-<sheet>-<n>` | Tables, note blocks, keys and legends | Paper size | `SC` |

- **Composing a sheet:** a sheet function works at paper coordinates (0 – 420 × 0 – 297). When the next sheet opens,
  or in `finish()`, everything composed for it is scaled by `SC` and moved to x = i × `SHEET_DX` (460) × `SC`. A
  no-plot sheet edge (`S-SHEET`) and drawing area (`S-TB-AREA`) mark it.
- **Detail id** is the number in its view-title bubble: `DET-1113-A` is section A on sheet 1113. The block's base
  point is the lower-left corner of its extents.
- **Dimensions inside a detail block** measure its real-size geometry, so they read 5000, not 100, at any scale.
- **Paper space:** one layout per sheet (tab named after the series), with the title block attributes and one locked
  viewport onto the sheet's model-space area. Plotting a window straight from model space gives the same result.
- **Views at their own scale:** each view function draws at its own S (steel: 1:50, 1:20, 1:10, 1:5, 1:1). RC
  typical details are N.T.S. and all use S = 25.

## 3. Title block `TB-A3-NRW`

The drawing area is a rectangle on `S-TB-AREA`; the paper edge is on `S-SHEET` (both no-plot). The frame is
`FX0, FY0, FX1, FY1` = 20, 10, 410, 287 (A3; binding margin 20).

| Attribute tags | Content |
|---|---|
| `DWG_NO`, `SHEET`, `SCALE`, `DATE` | Drawing no., "SHEET x OF y \| A3", scale, date |
| `TITLE_1` – `TITLE_3` | Drawing title lines (from `SHEETS`) |
| `PROJECT`, `LOCATION`, `OWNER`, `OFFICE`, `OFFICE_ADDR` | Project data (from `PROJ`) |
| `REV_1` … `REV_4`, with `_DESC` and `_DATE` | Revision rows (REV_1 = top row). A description must fit its 38 mm column, about 30 characters |
| `KEYPLAN_1`, `KEYPLAN_2` | Key-plan text |
| `STATUS_1`, `STATUS_2` | Status stamp ("FOR REVIEW / NOT FOR CONSTRUCTION") |

**A project title block** is a new block with the same attribute tags and an `S-TB-AREA` rectangle. In AutoCAD,
INSERT the project DWG under the name `TB-A3-NRW` and choose to redefine; the attribute values on every sheet are
kept (`ATTSYNC` if needed). The sheet layouts are designed for A3: another drawing area (e.g. A1) needs the sheet
functions changed (positions only; the details do not change).

## 4. Linetypes and pens

- **Linetypes:** AutoCAD `acadiso.lin` definitions, verbatim, kept in `ACADISO` so a build needs no AutoCAD profile.
  - LTSCALE = `LTS` = 3.75 (model), **PSLTSCALE 0**, MSLTSCALE 0 (set by `plot.py` and saved into the DWG).
  - Plotted dash = pattern × 3.75 / 25 = 0.15 × the .lin value.
  - Hidden = HIDDENX2 (1.9 / 0.95 plotted), fine hidden = HIDDEN (0.95 / 0.48), centre and cutting plane = CENTER
    (4.8 / 0.95 / 0.95 / 0.95), property = PHANTOM. Steel adds `EIT_GRID` (12 / 2 / 2 / 2) in `drafter/steel.py`.
  - Keep paper-space linetypes continuous: PSLTSCALE 0 applies LTSCALE there too.
- **Pens by colour** (`drafter/pens.py`, `PEN`): each ACI colour is one lineweight, and the plot scripts build the CTB
  (`NRW-EIT-R2.ctb`) from it. Layer lineweights are generated from the same table (screen only), never set by hand.

  | Colour | Pen | Used for |
  |---|---|---|
  | 1 red | 0.50 | Main bars, dowels |
  | 30 orange | 0.35 | Ties, stirrups, secondary bars |
  | 4 cyan | 0.35 | Concrete cut, steel outline (cut / subject), title text |
  | 5 blue | 0.25 | Concrete seen, steel seen beyond, joints, soil |
  | 6 magenta | 0.25 | Cutting plane, symbols, bolts, detail callouts |
  | 3 green | 0.18 | Leaders, centre lines |
  | 2 yellow | 0.18 | Dimensions |
  | 7 white | 0.18 | Text, detail inserts |
  | 10 | 0.70 | Sheet frame |
  | 8 grey | 0.18, screened 50 % | Breaks, zone grid, dimension extension lines, steel centre lines and hollow-section walls |
  | 252 grey | 0.25, screened 50 % | Hidden concrete and steel, background elements |
  | 9 grey | 0.13, screened 50 % | Hatch, weld hatch, viewport, sheet edge |

## 5. Functions a job calls

| Group | Functions |
|---|---|
| **Views** | `capture(fn, ox, oy)` runs a view function at a model-space origin (views sit far apart, e.g. 10 m), lays out its leader notes, checks its dimensions, stores its extents in `EXT[key]` and turns it into a `DET-TMP…` block |
| **Sheets** | `new_sheet(i)` (0-based) inserts the title block and returns paper coordinates 0 – 420 × 0 – 297; `viewport(ps, key, scale, px, py_top)` inserts the view block at the given scale (returns x, width, height); `view_title(ps, x, y, name, scale_txt, (id, sheet))` titles the view just placed and renames it `DET-<sheet>-<id>` (x = None aligns to that view); `finish()` closes the last sheet and adds the layouts |
| **Paper blocks** | `tbl(ps, x, y_top, widths, heads, rows, align, title=TABT(key))`, `table`, `notes_block`, `bar_end_legend`; `group(prefix, fn, …, g_kind=, g_title=, g_scale=)` turns anything a job draws on the sheet into a block (the `g_` prefix keeps the index keywords apart from the function's own) |
| **Annotation** | `note_cfg(...)` per view; `leader(sp, tip, knee, text, S, side, width, mark=, ring=, bolt=, dot_tip=, fixed=)`; `callout`, `callout_list`; `level`; `TABT`, `TAB` |
| **Dimensions** | `dim(sp, p1, p2, base, S, angle=, text=, tside=)`, `row_label` (tier labels), `zone_band` (stirrup zones) |
| **Drawing** | `line`, `pline`, `text`, `mtext`, `hatch` / `pscale`, `dot`, `arrowhead`, `zbreak`, `zigzag`, `earth_band`, `nf_hatch`; bars `bar`, `strip`, `rdot`, `stirrup`, `crosstie`, `lap_crank`, `dist_line`, `dowel_end`; `grid_bubble`, `pour_header`; steel helpers in `drafter/steel.py` |
| **Checks** | `warn(msg)` records a `!!` problem; `check_dims()` runs inside `capture()` |
| **Output** | `index_csv(path)`: every block with its kind, sheet, title and scale (the library index) |

The full symbol list with layers is in `SYMBOLS.md`.

## 6. Opt-in options

Off by default, so a set that does not set them is unchanged. SRT sets both.

- `LEADER_ORTH = True`: straight or orthogonal L leaders, routed so none crosses another leader, a note or a dimension
  (guide §9.1). `ORTH_RISE` = 5 mm puts the note off a horizontal edge on the free side; `ORTH_LEG_MIN` = 3 mm is the
  shortest vertical leg an L may have.
- `leader(..., bolt=hole Ø)`: the tip is the bolt centre and the leader starts on an open circle of `BOLT_RING_K` =
  1.25 × the hole (guide §2.1).
- `WRAP_UNITS = True`: notes wrap with `drafter.fonts.wrap(..., keep_units=True)`, so a number never leaves its unit
  on the next line (guide §2.4.2).

Without `LEADER_ORTH` the leader form is chosen per target (the R2 rule): a target on a vertical line, a corner, a dot
or an area gets one horizontal leader at its height; a target on a horizontal line gets the inclined 45° / 60° leg
(`_target_kind`, `_rise`, `_snap_tip`).

## 7. Checks and review tools

- `check_dims()` flags dirty dimensioning in every view (guide §2.4.1). It ignores weld hatch (`S-WELD`) and hatch
  boundaries (`Defpoints`), and treats collinear dimension lines as one chain.
- **Layout guards:** `notes_block` warns when a block runs below the frame; `tbl` when a table runs into the title
  strip or has no number; `viewport` when a detail leaves the drawing area; `view_title` when its note falls below the
  frame. A text change on one view can push a neighbour out, so rebuild the whole set and read every `!!`.
- `build.py` prints in UTF-8, because the warnings quote ≥, ℓ, ≈.
- Review a single detail: `python jobs/standard_set_R2/crop_det.py <set> DET-xxxx-n` crops it from the plotted PDF;
  `render_block.py` renders a block without AutoCAD (its dimension text placement is approximate).
- The plot scripts remove library DWGs of details that no longer exist in the set.

## 8. Working with the output in AutoCAD

| Task | How |
|---|---|
| Edit a detail | BEDIT `DET-1112-2`; every sheet that uses it updates. A change that should last goes into the generator, or it is lost on the next build |
| Move a detail to another sheet or title block | Move the `DET` insert together with its `VT` title |
| Use a detail in a project drawing | INSERT `library/DET-xxxx-x.dwg` at 1/scale (scale in `library/INDEX_<set>.csv`) into a paper-size sheet. For full-size model work insert at 1 and set LTSCALE for the line types |
| New title block for a project | Section 3 |
| Change a detail's scale | In the generator: the view's `S` and its `viewport(…, scale, …)` call. Scaling a block by hand scales its text and arrows too |

## 9. Pitfalls (all met on real sets)

- **PSLTSCALE is stored per layout** (bit 1 of the LAYOUT flags). A layout created by ezdxf defaults to 1, and a
  `PSLTSCALE 0` typed once only reaches the current layout: only page 1 plotted right and the other pages plotted
  every pattern × 25 (R2, "weird linetype scale in 1123"). `finish()` sets `layout_flags = 0` on every layout and the
  plot script sends `PSLTSCALE 0` after each `CTAB`. Check dash lengths on a page other than the first.
- **CTB lineweights:** ezdxf `PlotStyle.set_lineweight()` appends a new table entry on a float mismatch (0.35, 0.18 …),
  and AutoCAD ignores entries past its 27 standard ones (the ties plotted at maximum width). The plot scripts set the
  index of the nearest standard entry.
- **Never set an entity `ltscale` inside a detail block:** dashes would plot scale × too long, and short dashed lines
  become continuous.
- **One set per process** (section 1).
- **A keyword that collides with a wrapper's own:** an early `title=` keyword of `group()` silently swallowed
  `tbl(title=…)`; wrapper keywords now start with `g_`.
- **Layout is set by the notes:** at 1:25 the height of a view is often set by its stacked leader notes, not by its
  geometry. Widening the note column is the cheapest fix; shorten lengths next; move notes or tables to a
  continuation sheet last.
