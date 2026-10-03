# Structural Drafter

Python generators that produce **structural drawings** (reinforced concrete and, since SRT, structural steel) to the Thai drafting standard **EIT 011006-19**. They write the drawings with [ezdxf](https://ezdxf.readthedocs.io/), then plot them with AutoCAD Core Console to PDF and DWG.

The repository holds the generators, their drafting instructions and the source reviews behind the content. It does not hold the drawings themselves; they are rebuilt from the scripts.

| Set | Sheets | Folder |
|---|---|---|
| General notes, structural concrete | STR-ST-1001 – 1003 | `jobs/standard_set` (Rev B), `jobs/general_notes` (Rev A) |
| **Typical details R2** (current) | Columns 1101 – 1104, beams 1111 – 1116, slabs 1121 – 1128 | `jobs/standard_set_R2` |
| Typical details R1 (frozen) | Columns 1101 – 1103, beams 1111 – 1115, slabs 1121 – 1127 | `jobs/standard_set` |
| Staircase ST-1 (demonstration) | 1 sheet | `jobs/stair_demo` |
| Retaining wall, NRW-ST (issued job, Rev B) | 7 sheets | `jobs/nooker_rw` |
| **Steel roof truss T1, SRT-ST** (CHS Pratt truss with fly bracing, design + drawings, for review) | 6 sheets | `jobs/steel_roof_truss` |
| Typical details, first version (superseded) | – | `jobs/typical_details` |

All sheets are A3 and every detail is N.T.S. The title-block fields are placeholders, for example `[ PROJECT NAME ]`.

---

## Requirements

| Item | Notes |
|---|---|
| Windows + **AutoCAD 2024 or later** (optional) | `accoreconsole.exe` and the `DWG To PDF.pc3` plotter. Only plotting uses it, and without it the plot scripts fall back to ezdxf (see "Plotting without AutoCAD"); building the DXF never needs it. The newest installed `C:\Program Files\Autodesk\AutoCAD 20xx` is used; set `ACCORECONSOLE` to the full path of another `accoreconsole.exe` to override it |
| Python 3.11 | Tested with 3.11.9 |
| Python packages | `requirements.txt`: `ezdxf`, `fonttools`, `pymupdf`, and `matplotlib` / `numpy` for the preview renderers |
| Fonts | Arial Narrow (`ARIALN.TTF`, `ARIALNB.TTF`) in `%WINDIR%\Fonts`. Text widths are measured from the font files |
| Plot styles | The plot scripts write their CTB next to the drawings and into the Plot Styles folder of every installed AutoCAD version (`%APPDATA%\Autodesk\AutoCAD 20xx\...\Plotters\Plot Styles`), so the DWG plots the same way when opened there |

```bash
pip install -r requirements.txt
```

## Build and plot

Run the plot step from **PowerShell or Python**: AutoCAD Core Console does not run its script when launched from Git Bash. The Windows console also needs UTF-8 output, because the notes contain ≥, ℓ and ≈.

Typical details R2:

```powershell
cd jobs\standard_set_R2
$env:PYTHONIOENCODING = "utf-8"
python build.py slabs      # columns | beams | slabs | all  -> out\*.dxf + library\INDEX_<set>.csv
python plot.py slabs       # -> out\*.pdf, out\*.dwg, library\DET-*.dwg (one DWG per detail block)
```

The other jobs follow the same pattern:

| Job | Build | Plot |
|---|---|---|
| `jobs/standard_set` (R1, general notes Rev B) | `python build.py gn` | `python plot.py gn` (`gn \| columns \| beams \| slabs \| all`) |
| `jobs/general_notes` | `python build_gn.py out` | `python plot_gn.py out` |
| `jobs/stair_demo` | `python build_stair.py out` | `python plot_stair.py out` |
| `jobs/nooker_rw` | `python build_rw.py <out>` | `python plot_rw.py <out>` (design checks: `calc_rw.py`; full guide: `jobs/nooker_rw/README.md`) |
| `jobs/typical_details` (superseded) | `python build_td.py <out> [set]` | `python plot_td.py <out> [set]` |
| `jobs/steel_roof_truss` | `python build.py` (design: `calc_truss.py`) | `python plot.py` (full guide: `jobs/steel_roof_truss/README.md`) |

The build prints a line starting with `!!` for every layout problem it finds: a detail outside the drawing area, a leader crossing a dimension, a table without a number, a table or note running off the sheet. **A clean build prints none.** In R2, `build.py` then exits with code 1 (the DXF is still written for inspection), and so does `build.py all` if any set failed.

The plot step finishes with `font check OK`. Every plot script exits with code 1 when AutoCAD fails or times out, its log shows a rejected command, a sheet did not plot, the DWG or a library file is missing, or a glyph is not Arial Narrow. A partial set is never merged into the PDF.

## Tests

The smoke test builds every job without AutoCAD and fails on any `!!` line, a non-zero exit or a DXF audit error:

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Shared code

`drafter/` holds the code the jobs share:
- `drafter/fonts.py`: text widths measured from the Arial Narrow font files (`text_w`, `wrap`; `wrap(..., keep_units=True)` keeps a number on the same line as its unit);
- `drafter/acad.py`: the AutoCAD Core Console plot (script, run, checks, PDF merge, font check) and the CTB helpers;
- `drafter/ezplot.py`: the same plot without AutoCAD, rendered by ezdxf;
- `drafter/plotting.py`: picks AutoCAD when installed, ezdxf otherwise (or with `--ezdxf`).

Each job script adds the repository root to `sys.path` and imports from it. The superseded `jobs/typical_details` keeps its own copies.

## Plotting without AutoCAD

Every plot script (`plot.py`, `plot_rw.py`, `plot_stair.py`, `plot_gn.py`) falls back to ezdxf's own renderer when AutoCAD Core Console is not installed. Add `--ezdxf` to use it even when AutoCAD is there, for example `python plot.py slabs --ezdxf`. For a quick look at any single DXF, `python plot_ezdxf.py <drawing.dxf> [<plot style.ctb>]` from the repository root.

- **PDF:** one vector page per layout at 1:1, with the job's CTB (lineweight by colour; screened colours plot as their grey). Text is measured and drawn from the Arial Narrow font files. A text style whose font file is missing stops the plot.
- **DWG and the detail library:** written through the free [ODA File Converter](https://www.opendesign.com/guestfiles/oda_file_converter) when it is installed. Without it there is no DWG, and the library is written as one DXF per detail block.
- **How close it is:** compared page by page with the AutoCAD 2026 plot of every set (2026-10-03), 1 – 3 % of the ink differs on most sheets: antialiasing, slightly lighter greys, and a page 0.2 mm smaller. Long MTEXT paragraphs (the retaining-wall and stair notes) sit up to about a quarter of a line lower as they run down the column. **AutoCAD's plot stays the reference for an issued set.**
- **ezdxf 1.4 workaround:** ezdxf scales a hatch pattern wrongly inside a scaled block (by the new pattern scale instead of the change), which made the slab-on-ground sheets millions of strokes. `drafter/ezplot.py` corrects it while rendering; the DXF itself is right.

## How the drawings are made (R2)

- **Model space at real size.** Every detail is a block (`DET-<sheet>-<id>`). Each sheet is one paper-space layout, with the title block `TB-A3-NRW` (attributes) and one locked viewport.
- **Every detail is N.T.S.** The details are laid out at a dummy 1:25 (`SC`). Slab-on-ground sections use 1:10 and seal details 1:2. Member sizes come from one catalogue, `members.py`: column 400, beam 300 × 600, slab 150 and so on. Only lengths are shortened, with break lines.
- **Linetypes:** `acadiso.lin`, with LTSCALE 3.75, PSLTSCALE 0 (set on every layout) and MSLTSCALE 0.
- **Pens by colour:** the `PEN` table in `pens.py` maps each colour to a lineweight. `plot.py` writes the matching CTB, `NRW-EIT-R2.ctb`.
- **Annotation engine:** notes are packed into aligned columns. A note pointing at a vertical line, a point or an area gets one horizontal leader; a note pointing at a horizontal line gets an inclined leg. Leaders never cross dimensions.
  - Opt-in modes used by the steel set (off in R2): orthogonal leaders (`LEADER_ORTH`), bolt rings (`leader(..., bolt=)`), unit-safe wrapping (`WRAP_UNITS`).
- **Tables:** every table is "TABLE n - NAME", numbered in one sequence: general notes 1 – 10, typical details 11 – 20. Notes cite "TABLE n", never a drawing number.
- **Units:** every measured value in a note, leader, title or key carries its unit; table headers carry it for the cells. Dimension strings and designations stay bare ("DIMENSIONS IN mm"). Rule for all drawings: `ANNOTATION_ALIGNMENT_GUIDE.md` §2.4.2.
- **Focus rule:** only the subject of a detail is drawn at full weight. Other elements are hatched grey and their bars are grey.

The full rules and the pitfalls behind them are in `jobs/standard_set_R2/MODEL_SPACE_SHEETS.md`.

## Documents

| File | Content |
|---|---|
| `DRAWING_STANDARD_EIT-011006-19.md` | EIT 011006-19 drafting standard, plus the office conventions (§19: pens, bar ends, laps) |
| `ANNOTATION_ALIGNMENT_GUIDE.md` | Annotation placement for **every structure type** (RC, steel, composite, timber, masonry, foundations; §0 maps which rules apply to which). Note columns, leaders, terminators (bar and bolt rings, plate edges), view titles, clean dimensioning, units on numbers (§2.4.2); §9 orthogonal leaders and steel annotation (tags, weld symbols, cutting planes, node dimensions, fitting views, detail callouts, labels on the member) |
| `TYPICAL_DETAILS_INSTRUCTION.md` | Typical-detail sheets: numbering, sources, decisions per sheet (R2, including the R1 history) |
| `GENERAL_NOTES_STRUCTURAL_CONCRETE.md`, `GENERAL_NOTES_DRAWING_INSTRUCTION.md` | General-notes content and layout |
| `STAIRCASE_DRAWING_INSTRUCTION.md` | Staircase drawing rules |
| `SPEC_RC_DESIGN_EIT-011008-21.md`, `SPEC_CONCRETE_EIT-011014-19.md` | Digests of the EIT design and concrete standards used for the notes |
| `SOURCES_COLUMN_DETAILING.md`, `SOURCES_BEAM_DETAILING.md`, `SOURCES_SLAB_DETAILING.md` | Source review per member (EIT, DPT, TATA, ACI) |
| `REVIEW_ACI_MNL66.md` | Review against the ACI Detailing Manual MNL-66(20), decisions D1 – D5 |
| `STEEL_DETAILING_INSTRUCTION.md` | Steel drawing rules S1 – S11: set content, setting out, marks, graphics, weld symbols, hollow-section welds (AWS D1.1 Fig 9.10 zones), joints, bolts and anchor rods, erection, fly bracing (S9A), checks |
| `SOURCES_STEEL_DETAILING.md` | Extracts behind the steel rules: AISC *Detailing for Steel Construction*, AISC Design Guides 21 (welds) and 24 (HSS connections), with page refs; Part E, the office standard sheet Beca SE-1505 (fly bracing) |
| `.claude/skills/steel-detailing/SKILL.md` | Claude Code skill: the steel workflow and checklist for this repo |
| `jobs/standard_set_R2/REVIEW_BECA_SLAB.md` | Slab-on-ground and fill details: Beca standard-detail review, DPT road-works fill specification, review-comment log |

## Not in the repository

- **Generated drawings:** DXF, DWG, PDF and PNG files, the `out/` and `library/` folders, CTB plot styles, logs and `.scr` files. Rebuild them with the commands above.
- **Third-party reference material:** the ACI MNL-66 supplemental drawings, other offices' standard details and the standards PDFs. They are copyrighted. `references/aci_mnl66/` keeps only the conversion script and its notes.

## Status

The typical details R2 are issued **FOR REVIEW – NOT FOR CONSTRUCTION**. Some table values are office proposals that still need confirming: minimum trimming bars (Table 17), slab-on-ground joints and dowels (Table 18), seal sizes and parts of the fill specification (Table 20). They are listed in `jobs/standard_set_R2/REVIEW_BECA_SLAB.md`.

Planned next: column and slab schedules, walls 113x, foundations 114x.
