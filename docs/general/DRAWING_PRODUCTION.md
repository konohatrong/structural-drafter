# Drawing Production: from calculation to plotted set (all structure types)

How a drawing set is produced in this repository, whatever the material: the pipeline, the engine, the checks, the
plot and the environment. What the drawings show is in the drafting rules (`DRAWING_STANDARD_EIT-011006-19.md`,
`ANNOTATION_ALIGNMENT_GUIDE.md`, `SYMBOLS.md` and the concrete / steel instructions). This file covers how they are
made.

---

## 1. The pipeline

Every set is a script, and its drawings are rebuilt from it. Nothing is drawn by hand in CAD.

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
| 9. **Issue** (standard sets) | `standard_drawings/publish.py <set> [--issue]` | Review copies go to `standard_drawings/developing/`; an official issue (the user's decision) to `standard_drawings/issued/` with the register (`standard_drawings/README.md`) |

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
- **Tables:** "TABLE n - NAME" from the register `TABLES`; notes cite "TABLE n" only.
- **One set per process:** the engine creates its document on import.

## 3. The checks (`!!` lines)

The build prints a line starting with `!!` for every layout problem. **A clean build prints none.** `build.py` exits
with code 1 while one remains, but still writes the DXF for inspection. Fix the drawing; never suppress the check.

| Message | Meaning | Usual fix |
|---|---|---|
| `detail … outside drawing area` | A view runs past the frame or into the title strip | Shorten member stubs, narrow the note column, shorten notes (guide §9.6) |
| `leader crosses a dimension` | A leader crosses a dimension or extension line | Move the chain to the side away from the notes, or put its value in the note (guide §5) |
| `leader crosses another leader or a note` | Orthogonal routing found no clean path | Move the tip to another visible part, or merge the notes (guide §9.1) |
| `<view>: extension line of 'A' crosses dimension line 'B'` and similar | Dirty dimensioning | Tier order, `tside`, drop a duplicate chain (guide §2.4.1) |
| Table or note block below the frame, table without a number | Sheet overflow, unregistered table | Move it to another sheet; register it in `TABLES` |

The plot step exits 1 when AutoCAD fails or times out, its log shows a rejected command, a sheet did not plot, the
DWG or a library file is missing, or a glyph is not Arial Narrow. A partial set is never merged into the PDF.

## 4. Requirements

| Item | Notes |
|---|---|
| Windows + **AutoCAD 2024 or later** (optional) | `accoreconsole.exe` and the `DWG To PDF.pc3` plotter. Only plotting uses it; building the DXF never does. The newest installed `C:\Program Files\Autodesk\AutoCAD 20xx` is used; set `ACCORECONSOLE` to the full path of another `accoreconsole.exe` to override it |
| Python 3.11 | Tested with 3.11.9 |
| Python packages | `requirements.txt`: `ezdxf`, `fonttools`, `pymupdf`, and `matplotlib` / `numpy` for the preview renderers. Tests: `requirements-dev.txt` |
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
  file lock.
- Give a job's `plot.py` an **absolute** output folder: the Core Console script is written there and a relative path
  is not found ("_plot.scr can't find", BANWA2).
- The ezdxf plot draws viewport linetypes solid: judge dashed, hidden and chain lines on the AutoCAD plot.
- In a Python patch script, write regex or path text as raw strings: `"\b"` inside a normal string becomes a
  backspace character in the file (it happened twice on BANWA2). Check edited files for control characters.
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
