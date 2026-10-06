# Instructions for AI agents: producing structural drawings

This repository is the **rule book and toolkit** for producing structural drawing sets (DXF → PDF / DWG) by script,
to the Thai drafting standard EIT 011006-19 and the office conventions. It has three parts:

| Part | Folder | Role |
|---|---|---|
| **Rules, guides, instructions** | `docs/` | What a drawing must show and how it is presented: `general/` for every structure type, `concrete/` and `steel/` for each material. Index: `docs/README.md` |
| **Toolkit** | `drafter/` | The drafting engine (`td_engine.py`), pens (`pens.py`), steel helpers (`steel.py`), font metrics, plotting |
| **Worked examples** | `jobs/` | Complete sets built with the rules, and the record of how the rules were developed. Catalogue: `jobs/README.md` |
| **Standard drawings** | `standard_drawings/` | The office standard sets (general notes, typical details) as plotted output: `developing/` review copies (local) and `issued/` official revisions (in git), with the issue register. Rules: `standard_drawings/README.md` |
| **MIDAS GEN NX** | `midas/` | Driving the analysis program through its API (MAPI): building the model from the structural DXF, loads, analysis, results, calculation report, plug-ins. Not used by the drawing toolkit. Start: `midas/MIDAS_GEN_NX_INSTRUCTION.md` |

## 1. Reading order for any drawing task

1. `docs/README.md`: the index, and the comparison of how concrete and steel are presented.
2. `docs/general/`. All of it applies to every structure:
   - `DRAWING_STANDARD_EIT-011006-19.md`: sheets, lines, pens, text, dimensions, levels, marks, callouts, §19 office
     conventions;
   - `ANNOTATION_ALIGNMENT_GUIDE.md`: notes, leaders, terminators, units, tags, cutting planes, callouts. Its §0 says
     which parts apply to which structure;
   - `SYMBOLS.md`: every symbol with its layer, helper and rule;
   - `DRAWING_PRODUCTION.md`: the pipeline, the checks, the commands and the environment;
   - `DRAWING_ENGINE.md`: the shared engine, when writing or changing code.
3. The material folder: `docs/concrete/README.md` or `docs/steel/README.md`, then its instruction files.
4. The closest example job in `jobs/README.md`: its README, then its code.
5. Sources (`docs/*/reference/`) when a rule or value needs checking. Check the code itself when the value matters.

**Precedence** when documents disagree:
1. the project's own requirements, law, and the engineer's instruction in this conversation;
2. **office rules**: the dated user rules, EIT §19 office conventions, the annotation guide, and the material
   instructions. The newest dated rule wins, and a material rule wins over a general one on the same point;
3. the EIT standard text ([STD], then [FIG]) in the EIT digests;
4. [REC] recommendations, handbooks and sources.

Fix the disagreement in the documents, not only in one drawing.

**Task router.** Read §1 – §5 of this list once; for a specific task go straight to:

| Task | Read |
|---|---|
| Start a new set or job | `jobs/README.md` §3, the closest job's README, `DRAWING_PRODUCTION.md` §1, `DRAWING_ENGINE.md` §1 |
| Engine functions, blocks, title block, AutoCAD workflow | `DRAWING_ENGINE.md` |
| Sheet, title block, revision, drawing number | EIT §3, §13, §19.1 |
| Line weight, linetype, layer, colour | EIT §0, §19.2 (current engine), material instruction (steel S4) |
| Place notes and leaders | Guide §0, §1, §3 – §5 (standard angle) or §9.1 (orthogonal), §2.1 terminators |
| Dimensions | Guide §2.4 – §2.4.1, §9.5; EIT §8, §19.3 |
| Units in text | Guide §2.4.2 |
| Any symbol (section, callout, level, break, tag, weld …) | `SYMBOLS.md`, then the rule it cites |
| Bars, ties, laps, bar notation | `RC_DRAWING_RULES_EIT-011006-19.md` §12, §19.4, §19.7; guide §2.1 – §2.3 |
| Welds, bolts, marks, bills, camber, erection | `STEEL_DETAILING_INSTRUCTION.md` S3 – S9 |
| Continuous steel trusses (roof on an RC frame): marks per span, key sections, elevations, joints, posts, purlins | Steel S2.10, S3.7 – S3.8, S4.10 – S4.12, S7.8; `FLOOR_PLAN_DRAWING_INSTRUCTION.md` FP9.2, FP13.5; example BANWA2 (`jobs/README.md`) |
| Bill of materials, steel weight, weight per area | Steel S1.6, S3.8 |
| Tables | Guide §6; `DRAWING_PRODUCTION.md` §2 (register, "TABLE n - NAME") |
| General-notes sheet | `GENERAL_NOTES_DRAWING_INSTRUCTION.md` §0, plus the material content file |
| Floor plans (pile, foundation, floor, roof), A1 project sheets | `FLOOR_PLAN_DRAWING_INSTRUCTION.md` (FP0 project settings first), RC §14 |
| A `!!` build warning | `DRAWING_PRODUCTION.md` §3 |
| Hand a standard set for review, or issue it | `standard_drawings/README.md` |
| Anything with MIDAS GEN NX (API, model from drawings, loads, results, report, plug-in) | `midas/MIDAS_GEN_NX_INSTRUCTION.md` (rules M1 – M12 and its router), then `midas/README.md` |

**Before issue**, run every checklist that applies:
- every set: EIT §17 (sheet) and guide §8 (annotation);
- steel: S10;
- typical details: `TYPICAL_DETAILS_INSTRUCTION.md` §7;
- stairs: `STAIRCASE_DRAWING_INSTRUCTION.md` §11;
- general notes: `GENERAL_NOTES_DRAWING_INSTRUCTION.md` §10;
- floor plans: `FLOOR_PLAN_DRAWING_INSTRUCTION.md` FP17.

## 2. Workflow

1. **Data first.**
   - Every size, length, force, weld and bolt comes from one source: the design calc (`calc_*.py`) or the member
     catalogue.
   - Drawings and notes never retype a number.
   - Never invent an engineering value. An assumption is stated on the drawing and listed as an open item in the
     job README.
2. **Engine.** In the job's engine module: `from drafter import td_engine`, `from drafter.td_engine import *`,
   set the project data and options, then `from drafter.steel import *` for steel. Draw every symbol with its helper (`SYMBOLS.md`).
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
| Pipeline, checks, plotting, environment | `docs/general/DRAWING_PRODUCTION.md` |
| Engine mechanics, functions, options, engine pitfalls | `docs/general/DRAWING_ENGINE.md` |
| General-notes sheet layout | `docs/general/GENERAL_NOTES_DRAWING_INSTRUCTION.md` |
| Floor / framing plans: presentation, layers, pens, linetypes, text, tags, coordination | `docs/general/FLOOR_PLAN_DRAWING_INSTRUCTION.md` |
| Bars, RC content, typical details, stairs, concrete notes | `docs/concrete/` |
| Steel content, welds, bolts, marks, bills, erection | `docs/steel/STEEL_DETAILING_INSTRUCTION.md` |
| A new material (timber, masonry, composite) | A new `docs/<material>/` with a README modelled on `concrete/` and `steel/` |

## 4. Rules of engagement

- **Engineering decisions belong to the engineer** (the user): design thresholds, cover rules, load assumptions,
  redesign. Propose with reasons, then ask. Open decisions are listed in each job README.
- **Status of jobs** (`jobs/README.md` §4): an **issued** job changes only by a new revision; a **frozen** or
  **superseded** job is not changed.
- **The standard sets are issued** (general notes and typical details, F-A "ISSUED FOR USE", 03/10/2026). Any change
  to them is a new revision, with its revision row, issued through `standard_drawings/publish.py --issue`.
- **Official issue of a standard drawing is the engineer's decision.** Publish review copies to
  `standard_drawings/developing/` freely; run `publish.py <set> --issue` only when the user asks for the issue.
  Never edit, replace or delete anything in `standard_drawings/issued/`.
- **Shared code is in `drafter/`.** `td_engine.py` (the engine), `pens.py` and `steel.py` are imported by every
  current set, so a change there is a change to all of them. Job folders hold only the job's own data, views and
  sheets.
  - Keep new options opt-in (off by default), as `LEADER_ORTH` and `WRAP_UNITS` are.
  - Run the full `pytest -q` after any change to them.
- **Verify refactors**: build before and after and diff the DXFs. Never change drawing output silently.
- **Commit or push only when asked.**
- **Copyright**: no standards PDFs, handbooks or other offices' details in the repository; only digests and short
  extracts with page references.
- **Encoding**: never edit source files with Windows PowerShell `Get-Content` / `Set-Content` (cp874 corrupts ≥ ° Ø).
  Use an editor or Python with `encoding="utf-8"`.
- **Plot from PowerShell or Python**, not Git Bash; set `PYTHONIOENCODING=utf-8`.

## 5. Quick commands

From the repository root, in PowerShell:

```powershell
pip install -r requirements.txt                       # ezdxf, fonttools, pymupdf, matplotlib, numpy
$env:PYTHONIOENCODING = "utf-8"
python jobs\steel_roof_truss\build.py                 # these write to the job's own out folder
python jobs\steel_roof_truss\plot.py --ezdxf
python jobs\standard_set_R2\build.py all
python jobs\standard_set_R2\plot.py all
pytest -q
```

All commands, the checks and the environment: `docs/general/DRAWING_PRODUCTION.md`.
