---
name: concrete-detailing
description: Draw reinforced concrete (typical details, member details, slabs, stairs, retaining walls, foundations, general notes) as script-built EIT drawing sets in this repo. Use for any new RC job or change to jobs/standard_set_R2, jobs/nooker_rw, jobs/stair_demo or the general notes - bars, ties, laps, bar marks, tables, N.T.S. typical details, focus rule.
---

# Concrete detailing (structural-drafter repo)

RC sets follow the pipeline in `docs/general/DRAWING_PRODUCTION.md`:

1. data (design calc or the member catalogue `members.py`);
2. engine (`jobs/standard_set_R2/td_engine.py`);
3. views and sheets (`td_<member>.py`);
4. `build.py`, which exits 1 on any `!!`;
5. `plot.py`.

Reference jobs:
- `jobs/standard_set_R2`: typical details, current;
- `jobs/nooker_rw`: a complete project set with its calc. It is **issued**, so change it only by a revision;
- `jobs/stair_demo`: a stair.

## Before you start

1. Read `AGENTS.md`, then `docs/general/` (drawing standard, annotation guide, symbols, production).
2. Read `docs/concrete/README.md`, which describes the RC presentation approach, then
   `docs/concrete/RC_DRAWING_RULES_EIT-011006-19.md` (bar graphics and notation §12, required content §14 – §15,
   office bar rules §19.4 / §19.7).
3. Read the instruction for the sheet type:
   - `TYPICAL_DETAILS_INSTRUCTION.md`;
   - `STAIRCASE_DRAWING_INSTRUCTION.md`;
   - `GENERAL_NOTES_STRUCTURAL_CONCRETE.md` with `docs/general/GENERAL_NOTES_DRAWING_INSTRUCTION.md`.
4. Check a value in `docs/concrete/reference/` (EIT 011008 / 011014 digests, DPT / TATA / ACI extracts), and in the
   code itself when the value matters.

## Workflow

1. **Members and values from one source.** Typical details take sizes from `members.py`. Laps, cover and tie spacing
   come from the general-notes tables, cited as "TABLE n".
2. **Bars with the helpers** (`bar`, `strip`, `dot` / `rdot`, `stirrup`, `crosstie`, `lap_crank`, `dist_line`,
   `dowel_end`):
   - real bends at R = 3.5 db;
   - dots true size and at least 1.1 mm;
   - stirrups wrapping their corner bars;
   - plain bar ends and cranked laps.
3. **Focus rule.** Only the subject of a detail is at full weight. Other elements go through `nf_hatch` with grey
   bars. The RC section of the subject is not hatched.
4. **Annotation.**
   - Standard-angle leaders.
   - Rings 2 × dot on cut bars, bar marks in Ø4 bubbles, numbered callouts on dense details.
   - Units on every measured value in notes.
   - Dimensions in tiers, with nothing through their text.
5. **Build, look, plot, test.** Run `python build.py <set>` with no `!!`, then `python plot.py <set> --ezdxf`. Render
   and **look at every sheet**, then plot with AutoCAD and run `pytest -q`.
6. **Record rules.** A user correction is fixed in the job and written into `docs/`, in material-neutral words where it
   is about presentation (`AGENTS.md` §3).

## Office rules to keep (ask before changing)

- A3 originals; Arial Narrow 2.0 / 2.8; EIT pens unreduced; cut concrete 0.35, seen 0.25; greys screened.
- Hidden 3.0 / 1.5 and fine hidden 1.5 / 0.75 (the office values).
- Filled 2 mm arrows on dimensions; grey extension lines.
- Tables numbered "TABLE n - NAME" in one sequence; notes cite the number only.
- Every typical detail N.T.S. at a dummy 1:25; lengths shortened with breaks.
- Bar ends plain, laps cranked, bar-end key on sheets with elevations.

## Environment pitfalls

- Never edit source files with PowerShell `Get-Content` / `Set-Content` (cp874). Use the Edit tool or Python with
  `encoding="utf-8", newline="\n"`.
- Use a Python with `ezdxf` (a venv from `requirements.txt`).
- Plot from PowerShell, not Git Bash. Set `PYTHONIOENCODING=utf-8`.
- PSLTSCALE is per layout, and the CTB lineweights must be standard entries (`jobs/standard_set_R2/MODEL_SPACE_SHEETS.md`).
