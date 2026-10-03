# Structural Drafter

The rules, guides and instructions for producing **structural drawings by script** (concrete, steel, and any
structure type), together with the toolkit that applies them and the jobs built with them. Drawings follow the Thai
drafting standard **EIT 011006-19** and the office conventions. They are written as DXF with
[ezdxf](https://ezdxf.readthedocs.io/) and plotted with AutoCAD Core Console (or ezdxf) to PDF and DWG.

The repository is written for **AI agents and drafters alike**. An agent starts at [`AGENTS.md`](AGENTS.md).

## Layout

| Folder / file | What it holds |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Entry point for an agent: reading order, workflow, how the rules grow, rules of engagement (`CLAUDE.md` loads it for Claude Code) |
| [`docs/`](docs/README.md) | **The rule book.** `general/` applies to every structure type: drawing standard, annotation guide, symbols, general-notes sheets, drawing production. `concrete/` and `steel/` describe each material's presentation approach and rules, with their sources. The index compares how concrete and steel are presented |
| [`jobs/`](jobs/README.md) | **Worked examples**: complete sets built with the rules, and the record of the reviews that produced them |
| [`standard_drawings/`](standard_drawings/README.md) | **The office standard drawings** (general notes, typical details) as plotted sets: `developing/` review copies (local only) and `issued/` official revisions (kept in git), with the issue register `REGISTER.md` and `publish.py` |
| `drafter/` | **Shared code.** `td_engine.py`, the drafting engine every set imports (model-space blocks, the annotation engine, tables, title block, checks, bar graphics); `pens.py`, pens by colour; `steel.py`, steel layers and helpers; font metrics and wrapping; AutoCAD plotting and the ezdxf fallback |
| `.claude/skills/` | Claude Code skills: `concrete-detailing`, `steel-detailing` |
| `tests/` | Smoke test: builds every job without AutoCAD |
| `references/` | Conversion scripts for third-party reference material (the material itself is not in the repository) |

## Example sets

| Set | Structure | Status | Folder |
|---|---|---|---|
| Steel roof truss T1, SRT-ST (6 sheets) | Steel: CHS Pratt truss, bearings, splices, fly bracing; design + drawings | For review | `jobs/steel_roof_truss` |
| Typical details R2 (columns 1101 – 1104, beams 1111 – 1116, slabs 1121 – 1128) | Concrete | Current, for review | `jobs/standard_set_R2` |
| Retaining wall, NRW-ST (7 sheets) | Concrete: design + drawings | Issued, Rev B | `jobs/nooker_rw` |
| General notes, structural concrete (STR-ST-1001 – 1003, Rev B); typical details R1 | Concrete | Notes current; R1 frozen | `jobs/standard_set` |
| General notes Rev A; staircase ST-1; first typical details | Concrete | Superseded / demonstration | `jobs/general_notes`, `jobs/stair_demo`, `jobs/typical_details` |

All sheets are A3. Title-block fields are placeholders, for example `[ PROJECT NAME ]`.

## Quick start

```bash
pip install -r requirements.txt
```

```powershell
cd jobs\steel_roof_truss
$env:PYTHONIOENCODING = "utf-8"
python build.py             # -> out\*.dxf; exits 1 on any "!!" layout problem
python plot.py              # AutoCAD -> out\*.pdf, *.dwg; add --ezdxf to plot without AutoCAD
```

```bash
pip install -r requirements-dev.txt
pytest -q                   # builds every job
```

Run plots from PowerShell or Python, not Git Bash. Requirements, every job's commands, the checks and the
pitfalls are in [`docs/general/DRAWING_PRODUCTION.md`](docs/general/DRAWING_PRODUCTION.md).

## Not in the repository

- **Generated drawings:** DXF, DWG, PDF, PNG, `out/`, `library/`, CTBs, logs. Rebuild them from the scripts.
- **Third-party reference material:** standards PDFs, handbooks, other offices' standard details. They are
  copyrighted. `docs/*/reference/` holds digests and short extracts with page references.

## Status

- **Typical details R2:** issued **FOR REVIEW – NOT FOR CONSTRUCTION**. Office proposals still to confirm are
  Tables 17, 18 and 20 (`jobs/standard_set_R2/REVIEW_BECA_SLAB.md`).
- **SRT steel truss:** for review. Open items are in its README.
- **Planned:** column and slab schedules, walls 113x, foundations 114x.
