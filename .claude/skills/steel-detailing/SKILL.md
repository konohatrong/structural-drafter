---
name: steel-detailing
description: Design and draw structural steel (hollow-section trusses, continuous roof trusses on RC frames, portal frames, connections, bearings) as script-built EIT drawing sets in this repo. Use for any new steel job or change to jobs/steel_roof_truss or jobs/steel_portal_frame - member and joint design to AISC 360-16 / DG24, welds to AWS D1.1, weld symbols, marks, key sections, joint details, bills, camber, anchor rods, erection notes.
---

# Steel detailing (structural-drafter repo)

Steel sets follow the same pipeline as the RC sets:

1. **Design calc**: `calc_*.py`, pure Python + numpy. It is the single source of sizes, geometry, welds and bolts.
2. **Project engine**: `*_engine.py` on top of `drafter/td_engine.py` and `drafter/steel.py` (steel layers and
   helpers). It holds the project data, options, the design geometry and the marks.
3. **Sheets**: `*_sheets.py`.
4. **Build**: `build.py`, which exits 1 on any `!!` layout problem.
5. **Plot**: `plot.py` (AutoCAD Core Console, or the ezdxf fallback with `--ezdxf`).

Reference jobs: `jobs/steel_roof_truss` (one welded CHS truss, shop-ready), `jobs/steel_portal_frame` (portal frame
from a live MIDAS model) and BANWA2 (outside the repository, `jobs/README.md`: continuous CHS roof trusses on an RC
frame - roof plans, key sections, typical elevations, welded joints, posts through the trusses, bill of all steel).

## Before you start

0. Read `AGENTS.md`, `docs/general/` (drawing standard, annotation guide, symbols, production) and
   `docs/steel/README.md`, which describes the steel presentation approach.
1. Read `docs/steel/STEEL_DETAILING_INSTRUCTION.md`. Its rules S1-S11 (with S9A fly bracing) say what the drawings must
   contain; cite a rule as "S6.2" in reviews. Then read `docs/general/ANNOTATION_ALIGNMENT_GUIDE.md` §2.1, §2.4.2 and §9, which
   say where things go: terminators, units, orthogonal leaders, tags, weld symbols, cutting planes, node dimensions,
   detail callouts and labels on the member.
2. Look up a source in `docs/steel/reference/SOURCES_STEEL_DETAILING.md`: AISC *Detailing for Steel Construction*, DG21 and DG24 extracts,
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
   - Geometry from a concentric analysis model: check the gaps first; set one WP offset e per truss type for gaps
     ≥ 20 mm; report β < 0.4 and the e-moment to the engineer; check joint strength on the **current** forces only
     (S2.10).
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

## Office rules from BANWA2 (user, 2026-10-06 / 07)

- Continuous trusses: one mark per support span, shared only by spans of the same length and sections; on plans a
  grey bracket with the circled mark at mid-span (S3.7, FP10.2).
- Steel in plan: double lines at projected width, posts as actual section trimming the chords, tie rods one line each
  on the grid linetype (S4.11, FP9.2).
- A key section of every truss line at 1:200, span bubbles "mark / sheet" to the 1:50 elevations, post start level
  (S4.12).
- Elevations: the adjacent span hidden beyond each post ("ADJACENT SPAN Tn") or "END OF THE TRUSS LINE"; a grid
  bubble on every post axis on a grid; level lines grey in the grid linetype; joint callouts as dashed circle + split
  bubble (S4.10, S4.12).
- A post through a truss runs 50 mm above the top chord and is capped; the purlin stands beside it (S7.8).
- Every section in a table is followed by its weight per length; the bill covers all the structural steel, with the
  weight per plan area (S3.8, S1.6).

The rules and their reasons are written in `docs/steel/STEEL_DETAILING_INSTRUCTION.md` S4 and
`docs/general/ANNOTATION_ALIGNMENT_GUIDE.md` §2.1, §2.4.2 and §9. Ask before changing any of these.

## Environment pitfalls

- **Do not edit source files with PowerShell `Get-Content` / `Set-Content`.** Windows PowerShell 5.1 reads them in
  the Thai ANSI codepage (cp874) and corrupts ≥ ° Ø Ψ µ. Edit with the Edit tool or a Python script that uses
  `encoding="utf-8", newline="\n"`.
- Use the Python that has `ezdxf` installed (`requirements.txt`), not a bare system interpreter.
- Run the AutoCAD plot from PowerShell. Git Bash breaks the Core Console paths. Give `plot.py` an **absolute** output
  folder (a relative one fails: "_plot.scr can't find").
- The ezdxf plot draws viewport linetypes solid: judge dashed and chain lines on the AutoCAD plot.
- A wipeout does not plot in AutoCAD's PDF of these sets: cut the geometry instead.
- In a Python patch script, write regex text as raw strings: a `"\b"` inside a normal triple-quoted string becomes a
  backspace character in the file.
