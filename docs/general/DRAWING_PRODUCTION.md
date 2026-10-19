# Drawing Production: from calculation to plotted set (all structure types)

How a drawing set is produced in this repository, whatever the material: the pipeline, the engine, the checks, the
plot and the environment. What the drawings show is in the drafting rules (`DRAWING_STANDARD_EIT-011006-19.md`,
`ANNOTATION_ALIGNMENT_GUIDE.md`, `SYMBOLS.md` and the concrete / steel instructions). This file covers how they are
made.

---

## 1. The pipeline

Every set is a script, and its drawings are rebuilt from it. Nothing is drawn by hand in CAD.

On a project (`PROJECT_WORKFLOW.md`) the job lives in the project's `04 Code\drawings`, reads its values from
`04 Code\project.py` and the calc outputs in `05 Calculation`, builds into `06 CAD\out`, and each review print is
copied, dated, to `07 Review`. The examples in `jobs/` keep everything in the job folder.

| Step | File (pattern) | Rule |
|---|---|---|
| 1. **Design / data** | `calc_*.py` or a member catalogue (`members.py`) | The **single source** of every size, length, force, weld and bolt. The drawings never retype a number; notes and tables quote the calc |
| 2. **Project engine** | `*_engine.py` | Imports the general engine `drafter/td_engine.py`. It sets the project data (title block, revision, tables register), the opt-in options (`LEADER_ORTH`, `WRAP_UNITS`) and any layers of its own, then imports the material helpers from `drafter/` (bars are in `td_engine.py`, steel in `steel.py`). Only job-specific geometry stays in the job |
| 3. **Views and sheets** | `*_sheets.py` or `td_<member>.py` | One function per view, which draws geometry, dimensions and `leader()` notes. One function per sheet, which places the views with `viewport()`, then tables and notes |
| 4. **Build** | `build.py` | Writes the DXF and the detail index. It prints `!!` for every layout problem and exits 1 if there is any |
| 5. **Look** | `plot.py --ezdxf`, then render the PDF pages to PNG | **Look at every sheet at print size.** Check leaders, clutter, overlaps, and views near the frame. The checks catch geometry, not readability |
| 6. **Plot** | `plot.py` | AutoCAD Core Console to PDF and DWG, plus one DWG per detail block. Finishes with `font check OK` |
| 7. **Test** | `pytest -q` at the repository root | Builds every job without AutoCAD; fails on any `!!`, a non-zero exit or a DXF audit error |
| 8. **Review** | The user reviews the PDF | Every correction is fixed in the job **and** written into the rules (see `AGENTS.md`, "How the rules grow") |
| 9. **Issue** (projects) | Copy to a new `09 Publish\YYYYMMDD - <set> Rev <R> - <purpose>\` folder | Only when the engineer decides; title-block row first, then register and transmittal; never edited afterwards (`PROJECT_WORKFLOW.md` W4.1) |
| 9. **Issue** (standard sets) | `standard_drawings/publish.py <set> [--issue]` | Review copies go to `standard_drawings/developing/`; an official issue (the user's decision) to `standard_drawings/issued/` with the register (`standard_drawings/README.md`) |

### 1.0 Self-review before every review print

(user, 2026-11-23, after the IHR draft prints A1 - C3: "make lesson learn on drawing produce procedure there are many
mistake"; the lessons are in §10.) The engineer's markup should find engineering questions, not rules we already
have. Before a print goes to `07 Review`, go through this list, **reading the rule files, not from memory**:

1. **The system before the detail.** For a new member, write down its structural system: supports, spans, how the
   loads reach the supports, the governing checks (thickness, deflection, torsion). Write the options with numbers
   and ask the engineer **before** drawing bars. Draw from the calc output, never from an assumption in the
   analysis model (§10 L4).
2. **Calc complete.** For each member: flexure, shear, minimum and maximum steel, bar spacing, deflection (with the
   compression steel that is really there), the minimum-thickness table, and torsion when a slab or flight frames on
   one face only (§10 L5). The drawing's notes quote the calc.
3. **Office preferences first.** For bar sizes, nosing bars, minimum mats, leaders and marks, the office rule wins
   over a generic recommendation. Read the material instruction's dated user rules before using a `[REC]` or
   handbook value (§10 L6).
4. **Geometry against the received drawings.** Every member is inside its AR outline: frames inside the stair box,
   stringers inside their flight, perimeter beams flush with the outer column face. Positions are computed from the
   AR edges in code, never typed (§10 L3).
5. **The model as built.** Member orientation (beta angle), support types and the member set agree with the
   drawing. A member the drawing adds (a column on a beam, a landing beam) is listed for the next model revision with
   its loads (§10 L7).
6. **Marks.** A new member takes an existing mark only under the mark rule: same section, and the mark's bars cover
   it with at most one bar more per face (FP10.1). Otherwise it gets a new mark (§10 L13).
7. **The sheet checklists**, every line: EIT §17 and guide §8 for every set, plus the material and sheet ones
   (`FLOOR_PLAN_DRAWING_INSTRUCTION.md` FP17, `STAIRCASE_DRAWING_INSTRUCTION.md` §11, steel S10, typical details §7).
   On IHR the flush perimeter beams, the main-beam brackets and a leader for each layer of dots were rules already
   written, and were still missed (§10 L1).
8. **A clean build**, with no `!!` line.
9. **The AutoCAD plot**, never the ezdxf preview, with `font check OK`. Only AutoCAD prints go to `07 Review`
   (§10 L2).
10. **Look at every changed area at 150 - 200 dpi**, not only the whole sheet. Look at every new label, mark and
    leader: the checks do not see hidden lines, extension lines of plan dimensions, or text over a break line
    (§10 L8).
11. **Records.** STATUS row, decision log entry for every engineering decision, the markup kept in
    `07 Review\markups`, and each correction written as a rule (`AGENTS.md` §3).

### 1.1 A project of several sets: drawing list and merged set

A project's drawings are usually several sets, each a script of its own (CHATAM: plans S1-01 - S1-07, details S2-01 -
S2-03, RC schedules S2-04 - S2-05, pile caps S2-06 - S2-12), often built by different sessions. Before a merged
review print or an issue (user, 2026-10-12: "check drawing numbering then merge all drawing", "add a drawing index
sheet"):

1. **Rebuild every set fresh** and plot it: another session may have changed the shared data (a cap schedule, the
   project values) since a set was last plotted. A merged set made of stale plots mixes revisions.
2. **Check the numbering** across the sets: one series per kind (EIT §19.1), numbers continuous from 01 in each
   series, no number twice, and every sheet a note or callout cites exists ("DETAILS S2-06 - S2-12" on S1-01).
3. **Drawing list S0-01** opens the set (EIT §3.7). It is a set of its own (`index`), built **after** the others and
   **read from their title blocks** (the `DWG_NO`, `TITLE_n`, `SCALE`, `REV_n` attributes of every layout in the built
   DXFs), never typed: the list cannot drift from the sheets. Its build warns on a number used twice or a gap in a
   series, and lists the total. Worked example: CHATAM `04 Code\drawings\ch_index.py`.
4. **Merge** the plotted PDFs in drawing-number order, one bookmark per sheet ("S1-01  FOUNDATION PLAN"), and check
   that the list on S0-01 names exactly the merged sheets. The merged print goes, dated, to `07 Review`.

## 2. How the drawings are built (engine `drafter/td_engine.py`)

The full reference is `DRAWING_ENGINE.md`. In short:

- **Model space at real size.** Every view is a block `DET-<sheet>-<id>`, made by `capture()` and placed on its
  sheet by `viewport()`. Each sheet is one layout with the title block `TB-A3-NRW` and one locked viewport.
- **Scale.**
  - RC typical details are N.T.S., laid out at a dummy 1:25 (`SC`), with member sizes from one catalogue. Only
    lengths are shortened, with break lines.
  - Steel views are drawn to their stated scale (1:50, 1:20, 1:10, 1:5, 1:1). See the presentation approach in
    `docs/concrete/README.md` and `docs/steel/README.md`.
- **Linetypes and pens:** acadiso patterns at LTSCALE 3.75, PSLTSCALE 0 on every layout; pens by colour
  (`drafter/pens.py`), from which the plot scripts write the CTB. (The older NRW engine uses `EIT_*` linetypes at
  LTSCALE 1: EIT §19.2.)
- **Annotation engine:** `leader()` collects the notes and the engine packs them into columns or rows, then routes the
  leaders (`ANNOTATION_ALIGNMENT_GUIDE.md`). Opt-in: orthogonal leaders, bolt rings, unit-safe wrapping.
- **Tables:** "TABLE n - NAME" from the register `TABLES`; notes cite "TABLE n" only. The standard sets use 1 – 20.
  A project set numbers its tables in one sequence from 21, in sheet order (guide §6.1).
- **One set per process:** the engine creates its document on import.

## 3. The checks (`!!` lines)

The build prints a line starting with `!!` for every layout problem. **A clean build prints none.** `build.py` exits
with code 1 while one remains, but still writes the DXF for inspection. Fix the drawing; never suppress the check.

| Message | Meaning | Usual fix |
|---|---|---|
| `detail … outside drawing area` | A view runs past the frame or into the title strip | Shorten member stubs, narrow the note column, shorten notes (guide §9.6) |
| `leader crosses a dimension` | A leader crosses a dimension or extension line | Move the chain to the side away from the notes, or put its value in the note (guide §5) |
| `leader crosses another leader or a note` | Orthogonal routing found no clean path | Move the tip to another visible part, or merge the notes (guide §9.1) |
| `note overlaps another note: '…'` | Two note texts in one view (fixed or packed) overlap or are less than 0.5 mm apart (`NOTE_CLEAR`). Usually a `fixed=True` knee | Move the fixed knee clear of the other note, or let the packer place it (guide §5) |
| `<view>: extension line of 'A' crosses dimension line 'B'` and similar | Dirty dimensioning | Tier order, `tside`, drop a duplicate chain (guide §2.4.1) |
| Table or note block below the frame, table without a number | Sheet overflow, unregistered table | Move it to another sheet; register it in `TABLES` |
| `<dwg no.>: title-block field <TAG> '…' is … mm wide, its cell holds … mm` | A title-block value (revision description, title line, scale, status …) runs past its cell line (`tb_check`, `DRAWING_ENGINE.md` §3) | Shorten the text; for a revision row, the engineer words it (it goes on an issue) |

The plot step exits 1 when AutoCAD fails or times out, its log shows a rejected command, a sheet did not plot, the
DWG or a library file is missing, or a glyph is not Arial Narrow. A partial set is never merged into the PDF.

## 4. Requirements

| Item | Notes |
|---|---|
| Windows + **AutoCAD 2024 or later** (optional) | `accoreconsole.exe` and the `DWG To PDF.pc3` plotter. Only plotting uses it; building the DXF never does. The newest installed `C:\Program Files\Autodesk\AutoCAD 20xx` is used; set `ACCORECONSOLE` to the full path of another `accoreconsole.exe` to override it |
| Python 3.11 | Tested with 3.11.9 |
| Python packages | `requirements.txt`: `ezdxf`, `fonttools`, `pymupdf`, and `matplotlib` / `numpy` for the preview renderers, `shapely` for the steel portal frame job's geometry. Tests: `requirements-dev.txt` |
| Fonts | Arial Narrow (`ARIALN.TTF`, `ARIALNB.TTF`) in `%WINDIR%\Fonts`. Text widths are measured from the font files |
| Plot styles | The plot scripts write their CTB next to the drawings and into the Plot Styles folder of every installed AutoCAD version, so the DWG plots the same way when opened there |

## 5. Build and plot commands

Run the plot step from **PowerShell or Python**: AutoCAD Core Console does not run its script when launched from Git
Bash. The console also needs UTF-8 output, because the notes contain ≥, ℓ and ≈.

```powershell
cd jobs\standard_set_R2
$env:PYTHONIOENCODING = "utf-8"
python build.py slabs      # columns | beams | slabs | all  -> out\*.dxf + library\INDEX_<set>.csv
python plot.py slabs       # -> out\*.pdf, out\*.dwg, library\DET-*.dwg (one DWG per detail block)
```

| Job | Build | Plot |
|---|---|---|
| `jobs/standard_set_R2` | `python build.py <set>` | `python plot.py <set>` (`columns \| beams \| slabs \| all`) |
| `jobs/steel_roof_truss` | `python build.py` (design: `calc_truss.py`) | `python plot.py` |
| `jobs/steel_portal_frame` (A1) | `python build.py` (design: `calc_spf.py`; model: `pull_model.py "<MAPI-KEY>"`, read-only) | `python plot.py` |
| `jobs/standard_set` (general notes, issued F-A; R1 details frozen) | `python build.py gn` | `python plot.py gn` (`gn \| columns \| beams \| slabs \| all`) |
| `jobs/general_notes` | `python build_gn.py out` | `python plot_gn.py out` |
| `jobs/stair_demo` | `python build_stair.py out` | `python plot_stair.py out` |
| `jobs/nooker_rw` | `python build_rw.py <out>` | `python plot_rw.py <out>` (design checks: `calc_rw.py`) |
| `jobs/typical_details` (superseded) | `python build_td.py <out> [set]` | `python plot_td.py <out> [set]` |

Tests, from the repository root:

```bash
pip install -r requirements-dev.txt
pytest -q
```

## 6. Shared code (`drafter/`)

- `drafter/fonts.py`: text widths measured from the Arial Narrow font files (`text_w`, `wrap`).
  `wrap(..., keep_units=True)` keeps a number on the same line as its unit.
- `drafter/acad.py`: the AutoCAD Core Console plot (script, run, checks, PDF merge, font check) and the CTB helpers.
- `drafter/ezplot.py`: the same plot without AutoCAD, rendered by ezdxf.
- `drafter/plotting.py`: picks AutoCAD when it is installed, ezdxf otherwise (or with `--ezdxf`).
- `drafter/td_engine.py`: the drafting engine (document, layers, dimension styles, annotation engine, detail blocks,
  title block, tables, bar graphics). It creates its DXF document at import: one set per process.
- `drafter/pens.py`: pens by colour and LTSCALE, with no side effects (the plot scripts read it).
- `drafter/thai.py`: `cad_thai()`, Thai text shaped for AutoCAD (tone marks to the font's low and left glyphs);
  opt-in, for Thai strings written into the DXF only (§8).
- `drafter/steel.py`: steel layers and helpers on top of the engine (welds, bolts, breaks, cutting planes, callouts,
  tags). Moved out of the job folders on 2026-10-03, with the DXF output unchanged.

Each job script adds the repository root to `sys.path` and imports from it. The superseded `jobs/typical_details`
keeps its own copies.

## 7. Plotting without AutoCAD

Every plot script falls back to ezdxf's own renderer when AutoCAD Core Console is not installed. Add `--ezdxf` to use
it even when AutoCAD is there. For a quick look at any single DXF, run
`python plot_ezdxf.py <drawing.dxf> [<plot style.ctb>]` from the repository root.

- **PDF:** one vector page per layout at 1:1, with the job's CTB (lineweight by colour; screened colours plot as
  their grey). Text is measured and drawn from the Arial Narrow font files. A text style whose font file is missing
  stops the plot.
- **DWG and the detail library:** written through the free ODA File Converter when it is installed. Without it there
  is no DWG, and the library is written as one DXF per detail block.
- **How close it is:** compared page by page with the AutoCAD 2026 plot of every set (2026-10-03), 1 – 3 % of the ink
  differs on most sheets. Long MTEXT paragraphs sit up to about a quarter of a line lower. **AutoCAD's plot stays the
  reference for an issued set.**
- **ezdxf 1.4 workaround:** ezdxf scales a hatch pattern wrongly inside a scaled block. `drafter/ezplot.py` corrects
  it while rendering; the DXF itself is right. Recheck if ezdxf is upgraded.
- **ezdxf 1.4, linetypes in viewports** (found 2026-10-04 on job SSK, user: "wrong linetype scale when plotted?"):
  ezdxf applies the linetype pattern after the viewport transform, in paper mm, and multiplies it by
  1 / viewport scale (`RenderPipeline2d.get_vp_ltype_scale`). With PSLTSCALE 0 (EIT §19.2) AutoCAD plots a model
  dash at pattern × LTSCALE × viewport scale, so ezdxf's dashes come out 10 000 times too long at 1:100 and every
  hidden and centre line plots solid. Measured: factor = viewport scale gives HIDDEN 2.9 mm at LTSCALE 45, 1:100, as
  AutoCAD. The SSK review renderer (`revplot.py`, outside the repository) sets that factor per sheet;
  `drafter/ezplot.py` does not yet, so check viewport sheets rendered without AutoCAD for solid dashed lines.
  Model-space sheets are not affected.

## 8. Environment pitfalls

- **Never edit source files with Windows PowerShell 5.1 `Get-Content` / `Set-Content`.** They read in the ANSI
  codepage (cp874 on a Thai system) and corrupt ≥ ° Ø Ψ µ. Edit with an editor, or with a Python script that uses
  `encoding="utf-8", newline="\n"`.
- Use a Python that has `ezdxf` installed (a venv with `requirements.txt`), not a bare system interpreter.
- The PDF may be open in a viewer while you rebuild. Write review copies under another name instead of fighting the
  file lock: on a project, the dated copy in `07 Review` is the one the engineer opens.
- A PDF made by placing clips of **one big vector page** (all views rendered once, each sheet `show_pdf_page` with a
  clip) carries the whole drawing on every page: CHATAM's markup set had 12.6 MB of vectors behind each A2 page, and
  the 5th floor page came up blank in the viewer (11/10/2026). Render each sheet from its own entities (filter by the
  view's extents) so a page holds only what it shows.
- Give a job's `plot.py` an **absolute** output folder: the Core Console script is written there and a relative path
  is not found ("_plot.scr can't find", BANWA2).
- The ezdxf plot draws viewport linetypes solid: judge dashed, hidden and chain lines on the AutoCAD plot.
- In a Python patch script, write regex or path text as raw strings: `"\b"` inside a normal string becomes a
  backspace character in the file (it happened twice on BANWA2). Check edited files for control characters.
- **Python run from the Bash tool loses backslashes even in a quoted heredoc** (CHATAM, 12/10/2026): `09 Publish\\2026...`
  was written as `\x82` + `61012`, `Calculation\\foundation` as a form feed + `oundation`, in code comments and in
  `STATUS.md` rows that other sessions read. Write the patch script to a file with an editor (or the Write tool) and
  run the file, or build a backslash with `chr(92)`; then scan the file for characters below 32 (except tab and
  newline) and 0x7F - 0x9F.
- **Thai text in AutoCAD: marks are not shaped** (rule 17/10/2026, RPM Staircase title block B3). AutoCAD draws
  Thai TrueType text without shaping: a tone mark or thanthakhat always sits at the high position (TH Sarabun New:
  1.42 - 1.76 x cap height), and on ป ฝ ฟ ฬ the marks and upper vowels are not moved off the stem. In the A3
  signature table (2.2 mm text at 3.6 mm pitch) the mark of "ด้" in "บางด้วน" reached into the line above and read
  as a hook under its letters. Checked with a test plot of TH Sarabun New, SarabunPSK, Leelawadee, Tahoma and
  Angsana New; TEXT and MTEXT behave the same. Write every Thai string meant for AutoCAD through
  `drafter.thai.cad_thai()`: it maps a mark with no upper vowel under it to the font's low glyph (Microsoft Thai
  private-use U+F70A - F70E; low-left U+F705 - F709 after ป ฝ ฟ ฬ), and on ป ฝ ฟ ฬ the upper vowels and high marks
  to their left glyphs (U+F701 - F704, F710 - F712; U+F713 - F717); a mark before sara am stays high. It is opt-in:
  reports, DOCX and any text that is searched or checked stay plain Unicode. A new Thai font must carry the
  private-use set (check with fontTools) and be added to `ALLOWED_FONTS` (`drafter/acad.py`). Look at the plotted
  Thai lines at print size: the PDF text check does not see a floating mark.
- A sheet title is not a file name: "PILE CAP DETAILS F1 / F2" stopped the per-sheet PDF export half way. Replace
  `/ \ : * ? " < > |` when a title becomes a file name.
- **Several sessions on one project** write the same files (`project.py`, a shared plan module, `STATUS.md`). Before
  editing a module another session owns, read it again; after editing, tell that session what changed (names, values,
  sheets rebuilt). Never write over another session's change to fix your own (`PROJECT_WORKFLOW.md` W6.1).
- **Revisions:** an issued job (for example `jobs/nooker_rw`) is changed only by a new revision, with its revision row
  and drawing numbers updated. A frozen set (`jobs/standard_set` R1, `jobs/typical_details`) is not changed. Verify a
  refactor by building both versions and diffing the DXFs, ignoring the header timestamps, CLASSES order and the ezdxf
  stamp. Never change drawing output silently.

## 9. Not in the repository

- **Generated drawings:** DXF, DWG, PDF and PNG files, the `out/` and `library/` folders, CTB plot styles, logs and
  `.scr` files. Rebuild them with the commands above.
- **Third-party reference material:** standards PDFs, handbooks, other offices' standard details and the ACI MNL-66
  supplemental drawings. They are copyrighted. The `docs/*/reference/` files are digests and extracts with page
  references; `references/aci_mnl66/` keeps only a conversion script and its notes.

## 10. Lessons learned

Each lesson has the same parts: what went wrong, why, and what now prevents it, with the file that holds the rule.
The checks are in §1.0.

### IHR Ihara Office Canteen, draft set A1 - C3 (2026-11-20 - 23)

The first project set drawn after the BANWA 2 and NSO reviews. It ran to 21 internal prints: A1 - A9, B1 - B9, C1 - C3.
Several of the engineer's markups pointed at rules already in this repository (L1, L2). Most of the others were
engineering choices that should have been put to the engineer before drawing (L4).

| # | What went wrong | Why | What prevents it now |
|---|---|---|---|
| L1 | Rules already written were missed. Perimeter beams were not flush with the outer column face (FP9.2, a BANWA 2 rule). Main beams were not marked once with a bracket (FP10.2). Distribution dots had no ring leader for each layer (STAIRCASE §7.1, "Label (4) once for each layer"). Every bar set lacked a leader | The sheets were drawn from memory of the rules. The checklists were not run line by line before the print | §1.0 item 7. Each miss is now cited with the IHR example in its rule |
| L2 | The first review print was the ezdxf preview: dashes too short, scaled per view | The quick preview was treated as the print | §1.0 item 9; FP3. Only AutoCAD plots go to `07 Review` |
| L3 | Members were placed outside the AR geometry. The stair 2 frame stood past the AR stair box (markup of A3), and its inner stringers sat in the 200 mm well between the flights (markup of B4) | Positions were typed from the model lines and never checked against the AR outlines | §1.0 item 4; FP9.2 (steel stair frame and stringers inside the box and the flights). Positions computed from the AR edges in code (`proposal.py` `X_IN_W / X_IN_E`) |
| L4 | ST-1 went through six designs in one day: folded slab 250, then 200 with DB12@100, then the engineer's columns and landing beams, then DB12@200, then a 0.0018bh top mat, then all bars DB12. Each design was drawn, plotted and printed | Bars were detailed before the structural system was agreed. The first design took the analysis model's assumption (waist 150, folded slab on two beams), which fails the thickness table and the deflection check | §1.0 item 1. Write the system and its options with numbers, ask, then draw. Use the "dummy arrangement" (STAIRCASE §5.1) when the bars are not decided |
| L5 | The calc was incomplete. The long-term deflection ignored the compression steel actually present (lambda = 2 always). The landing-edge beam had torsion above the threshold (flights on one face) that the first pass did not check | No checklist of the checks a member needs | §1.0 item 2. `calc\stair1_design.py` uses lambda = 2 / (1 + 50 rho'); `calc\landing_beams.py` checks the torsion threshold and designs hoops and Al |
| L6 | Generic recommendations were used where the office does otherwise: nosing bars on steps over 1.5 m wide, DB10 distribution, top bars larger than the minimum | The instruction's `[REC]` / `[STD FIG]` text was followed as if it were office practice | §1.0 item 3. STAIRCASE §3.3 (DB12 for every stair bar) and §4.1 (no nosing bars by default; 0.0018bh top mat both ways) |
| L7 | The model and the drawing disagreed and were found late. The stair 2 posts had their web along X (beta 0), so the 1.06 m cantilever side beams frame into the weak axis; this came up only at connection design. Members added on the drawings (C4, landing beams, stair 2 moves, the yard) were in the layout data but not in the model | Orientation and member set were not checked against the model before detailing | §1.0 item 5. Each addition goes onto the next-model list in STATUS (IHR D-M4) |
| L8 | Labels overlapped things on the plans. "UP" sat on a landing beam line; SB3 marks crossed the hidden pile cap outline; the C4 mark sat on a plan dimension's extension line; a slab tag and a level text crossed a break line | The placement check (`put()` against the boxes and the member bodies) does not see hidden lines, dimension extension lines or break lines | §1.0 item 10. Render every changed area at 150 - 200 dpi. Possible engine work: add those lines to the placement check |
| L9 | Revision descriptions ran past their title-block cell with no `!!` line. The title block shows only the last 4 revision rows | The fit check (`tb_check`) measures only fields given a room through `att(..., room=)`. The IHR Sato frame is a project title block and records no rooms, so none of its fields are measured (`DRAWING_ENGINE.md` §3). Separately, the IHR job imports the **main checkout's** `drafter` (`paths.DRAFTER`), not the worktree copy, so toolkit changes made in a worktree do not reach the project until merged | Keep revision text to about 28 characters (the RPM limit) and look at the title block on the plot. A project title block's code gives its fields rooms with `att(..., room=)` so the check covers them. Before relying on a toolkit check or changing shared code, confirm which `drafter` the project imports |
| L10 | Scripted edits broke text. A rule inserted by string matching landed in the middle of a sentence (FLOOR_PLAN FP9.2, markup of B3). Python run from Bash lost backslashes three times: a project path in `jobs/README.md`, and a `"\n"` in a calc's `write_text` that became a real line break and a syntax error | Patch scripts matched a line inside a paragraph. Backslashes went through a Bash heredoc (§8) | Edit docs with the Edit tool, then re-read the whole paragraph. Never pass paths or escapes through a Bash heredoc: write the script with the Write tool, or use `chr(92)` / `chr(10)`. Scan every edited file for control characters and 0x7F - 0x9F (§8) |
| L11 | A section view outgrew the frame after a tag and notes were added (ST-1 B-B into the title block) | Added content was not budgeted on the sheet | The build's "outside drawing area" check caught it. Re-check the stack of views when a view gets taller. Remove duplicate tags (one tag per member per sheet) |
| L12 | Plan labels were placed by a list of candidate positions. When all of them failed, the mark was dropped silently (C4 on grid A, the stair 2 side beams) | The placer skips a failed label without a warning | After a plan change, check that every member mark is present. Give a dropped mark a fallback position (IHR `ihr_plans.py`: slide along the member, or a fixed position). Possible engine work: warn on a dropped mark |
| L13 | A new member was about to take an existing mark (landing-edge beam as B3) whose support bars exceed the need by two bars | The mark rule was not checked for added members | §1.0 item 6; FP10.1 |

**Process:** a correction that applies a written rule costs a full review cycle: build, plot, print and the
engineer's markup. Twenty-one prints in four days is the measure to bring down. Run §1.0 before every print, and put
open engineering choices to the engineer in one question round, before drawing.
