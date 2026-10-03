---
name: steel-detailing
description: Design and draw structural steel (hollow-section trusses, connections, bearings) as script-built EIT drawing sets in this repo. Use for any new steel job or change to jobs/steel_roof_truss - member and joint design to AISC 360-16 / DG24, welds to AWS D1.1, weld symbols, marks, bills, camber, anchor rods, erection notes.
---

# Steel detailing (structural-drafter repo)

Steel sets follow the same pipeline as the RC sets:

1. **Design calc**: `calc_*.py`, pure Python + numpy. It is the single source of sizes, geometry, welds and bolts.
2. **Project engine**: `*_engine.py` on top of `jobs/standard_set_R2/td_engine.py`. It holds the layers, steel helpers
   and marks.
3. **Sheets**: `*_sheets.py`.
4. **Build**: `build.py`, which exits 1 on any `!!` layout problem.
5. **Plot**: `plot.py` (AutoCAD Core Console, or the ezdxf fallback with `--ezdxf`).

The reference job is `jobs/steel_roof_truss`.

## Before you start

1. Read `STEEL_DETAILING_INSTRUCTION.md`. Its rules S1-S11 (with S9A fly bracing) say what the drawings must
   contain; cite a rule as "S6.2" in reviews. Then read `ANNOTATION_ALIGNMENT_GUIDE.md` §2.1, §2.4.2 and §9, which
   say where things go: terminators, units, orthogonal leaders, tags, weld symbols, cutting planes, node dimensions,
   detail callouts and labels on the member.
2. Look up a source in `SOURCES_STEEL_DETAILING.md`: AISC *Detailing for Steel Construction*, DG21 and DG24 extracts,
   with PDF page refs, and Part E, the office standard sheet Beca SE-1505 (fly bracing). The other office standard
   steel sheets (SE-1501 to SE-1504: HD bolts, end plates, cleats, bracing) are under
   `G:\My Drive\##Workset_Autocad\400 Standard Details\400 Standard Details\20 - STEELWORK\`; review the matching
   one before detailing that kind of connection.
3. When a code value matters, check it in the code itself:
   - AISC 360-16 Table K3.1A;
   - AWS D1.1:2015 Fig 9.10 / Table 9.5.

   The PDFs are under `G:\My Drive\##Textbook\`. Read them with PyMuPDF: the Read tool cannot render PDFs here.

## Workflow

1. **Calc first.**
   - Size the members, then the joints.
   - Enforce the **K3.1A limits**, including 0.4 ≤ Db/D for gapped K-joints and the chord end distance.
   - Lay out the drawn geometry (e, gaps, θ) **in the calc** and check the joints on that same geometry.
   - Return everything the drawings need (welds by zone, bolt lengths, x_oh, camber ordinates, support movement).
2. **Engine**
   - Marks are generated, never typed: a different section, length or end preparation means a different mark.
   - Every weld goes through `weld()` (symbol) and the `weld_*` hatch helpers (graphics).
3. **Sheets**
   - Weld information goes in symbols. Leaders carry only the part, size and mark.
   - Notes and tables quote calc values. Never retype a number; keep one weight figure.
4. **Build and look**
   - `python build.py`, then `python plot.py --ezdxf` for a quick PDF.
   - Render the pages to PNG and **look at every sheet**: leaders, symbol clutter, views outside the frame.
   - Then plot with AutoCAD.
   - Fix every `!!` warning; do not suppress them.
5. **Tests**: run `python -m pytest -q` at the repo root (`tests/test_build.py` builds every set).
6. If the job is shared, save review PDFs as scratch copies (the user may have `out\*.pdf` open in a viewer).

## Office drawing rules (user, 2026-10-03)

- CHS walls are a fine hidden line in every view, and stop on the pipe break (`break_point`).
- A part behind another is hidden where it is covered (the gusset behind the knife plate).
- Member tags are circled and placed beside the member.
- Centre lines are grey, in the grid linetype; bolt and hole centre marks (S-CENT) are grey too.
- No node numbers on the elevation.
- Leaders are orthogonal and never cross; an L has a vertical leg of at least 3 mm.
- Bolt leaders aim at the bolt centre with an open circle of 1.25 × the hole; plate leaders end on the plate edge.
- Every bare number in notes, leaders, titles and keys carries its unit; table headers carry it for the cells.
- Detail callouts: a dashed circle (S-CALL), a leader landing on its edge in clear space, a note
  "DETAIL n/sheet - WHAT".
- A member with a clear band (a purlin) is named on itself, with no leader.
- Pipe break: one arc and a lens.
- Concrete is hatched AR-CONC and grout AR-SAND.
- Welds are 45° hatch only, with the boundary on Defpoints, drawn as seen: bands plus profiles.

The memory file `steel-drafting-preferences.md` holds the reasons. Ask before changing any of these.

## Environment pitfalls

- **Do not edit source files with PowerShell `Get-Content` / `Set-Content`.** Windows PowerShell 5.1 reads them in
  the Thai ANSI codepage (cp874) and corrupts ≥ ° Ø Ψ µ. Edit with the Edit tool or a Python script that uses
  `encoding="utf-8", newline="\n"`.
- Use the Python that has `ezdxf` installed (`requirements.txt`), not a bare system interpreter.
- Run the AutoCAD plot from PowerShell. Git Bash breaks the Core Console paths.
