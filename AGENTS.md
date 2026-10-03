# Instructions for AI agents: producing structural drawings

This repository is the **rule book and toolkit** for producing structural drawing sets (DXF → PDF / DWG) by script,
to the Thai drafting standard EIT 011006-19 and the office conventions. It has three parts:

| Part | Folder | Role |
|---|---|---|
| **Rules, guides, instructions** | `docs/` | What a drawing must show and how it is presented: `general/` for every structure type, `concrete/` and `steel/` for each material. Index: `docs/README.md` |
| **Toolkit** | `drafter/`, `jobs/standard_set_R2/td_engine.py`, job engines | Font metrics, plotting, the annotation engine and the drawing helpers |
| **Worked examples** | `jobs/` | Complete sets built with the rules, and the record of how the rules were developed. Catalogue: `jobs/README.md` |

## 1. Reading order for any drawing task

1. `docs/README.md`: the index, and the comparison of how concrete and steel are presented.
2. `docs/general/`. All of it applies to every structure:
   - `DRAWING_STANDARD_EIT-011006-19.md`: sheets, lines, pens, text, dimensions, levels, marks, callouts, §19 office
     conventions;
   - `ANNOTATION_ALIGNMENT_GUIDE.md`: notes, leaders, terminators, units, tags, cutting planes, callouts. Its §0 says
     which parts apply to which structure;
   - `SYMBOLS.md`: every symbol with its layer, helper and rule;
   - `DRAWING_PRODUCTION.md`: the pipeline, the engine, the checks, the commands and the environment.
3. The material folder: `docs/concrete/README.md` or `docs/steel/README.md`, then its instruction files.
4. The closest example job in `jobs/README.md`: its README, then its code.
5. Sources (`docs/*/reference/`) when a rule or value needs checking. Check the code itself when the value matters.

Precedence when documents disagree:
1. the project's own requirements and the engineer's instruction in this conversation;
2. a dated user rule;
3. the material instruction;
4. the general rules;
5. the EIT digest;
6. handbooks and sources.

Fix the disagreement in the documents, not only in one drawing.

## 2. Workflow

1. **Data first.**
   - Every size, length, force, weld and bolt comes from one source: the design calc (`calc_*.py`) or the member
     catalogue.
   - Drawings and notes never retype a number.
   - Never invent an engineering value. An assumption is stated on the drawing and listed as an open item in the
     job README.
2. **Engine.** Import `td_engine.py` and add the material helpers. Draw every symbol with its helper (`SYMBOLS.md`).
3. **Views and sheets.**
   - Annotate only through `leader()` / `note_cfg()`; never hand-place notes in column or row modes.
   - Choose one leader style per set (guide §0).
4. **Build.** `python build.py` must print no `!!` line. Fix the drawing; never suppress a check.
5. **Look.**
   - Plot (`plot.py --ezdxf` for speed) and render the pages to PNG.
   - **Look at every sheet at print size**: leaders, clutter, overlaps, views at the frame, units on numbers.
   - The checks do not see readability.
6. **Plot** with AutoCAD (`plot.py`) and confirm `font check OK`.
7. **Test.** Run `pytest -q` at the repository root.
8. **Report** honestly: what changed, what was verified, what is still assumed or open. Send the review PDF.

## 3. How the rules grow

The rules come from the user's reviews of real sets. When the user corrects a drawing:

1. **Fix the job** that showed the problem.
2. **Write the rule into `docs/`**, in the file that owns the topic (table below):
   - in **material-neutral words** if it is about placement or presentation (most annotation rules are);
   - dated, with the user's words when short: "(user rule, 2026-10-03: "...")";
   - with the worked example from the job ("on 1/5004 ...");
   - numbered, so it can be cited.
3. **Put it in the engine** when it can be checked or automated (a helper, an option, a `!!` check), and name the
   helper in the rule.
4. **Record the lesson** in `jobs/README.md` §2 and in the job's own README or development notes.
5. If the rule contradicts an older one, update or remove the older one. Never leave two answers.

| Topic | Owner file |
|---|---|
| Sheet, title block, lines, pens, text, scales, grids, levels, marks, numbering | `docs/general/DRAWING_STANDARD_EIT-011006-19.md` (§19 for office conventions) |
| Notes, leaders, terminators, dimensions placement, units, tags, cutting planes, callouts, labels | `docs/general/ANNOTATION_ALIGNMENT_GUIDE.md` |
| A symbol's form, layer and helper | `docs/general/SYMBOLS.md` |
| Pipeline, engine, checks, plotting, environment | `docs/general/DRAWING_PRODUCTION.md` |
| General-notes sheet layout | `docs/general/GENERAL_NOTES_DRAWING_INSTRUCTION.md` |
| Bars, RC content, typical details, stairs, concrete notes | `docs/concrete/` |
| Steel content, welds, bolts, marks, bills, erection | `docs/steel/STEEL_DETAILING_INSTRUCTION.md` |
| A new material (timber, masonry, composite) | A new `docs/<material>/` with a README modelled on `concrete/` and `steel/` |

## 4. Rules of engagement

- **Engineering decisions belong to the engineer** (the user): design thresholds, cover rules, load assumptions,
  redesign. Propose with reasons, then ask. Open decisions are listed in each job README.
- **Status of jobs** (`jobs/README.md` §4): an **issued** job changes only by a new revision; a **frozen** or
  **superseded** job is not changed.
- **Verify refactors**: build before and after and diff the DXFs. Never change drawing output silently.
- **Commit or push only when asked.**
- **Copyright**: no standards PDFs, handbooks or other offices' details in the repository; only digests and short
  extracts with page references.
- **Encoding**: never edit source files with Windows PowerShell `Get-Content` / `Set-Content` (cp874 corrupts ≥ ° Ø).
  Use an editor or Python with `encoding="utf-8"`.
- **Plot from PowerShell or Python**, not Git Bash; set `PYTHONIOENCODING=utf-8`.

## 5. Quick commands

```powershell
pip install -r requirements.txt            # ezdxf, fonttools, pymupdf, matplotlib, numpy
cd jobs\steel_roof_truss; python build.py; python plot.py --ezdxf
cd jobs\standard_set_R2;  python build.py all; python plot.py all
pytest -q                                  # from the repository root
```

All commands, the checks and the environment: `docs/general/DRAWING_PRODUCTION.md`.
