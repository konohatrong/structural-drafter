# 06 CAD

| Folder | Holds |
|---|---|
| `xref\` | Grid, title block and background xrefs, converted from `01 Transfer in` (name the source file) |
| `working\` | Working DXF/DWG edited by hand or by script, internal revisions `<name>_A1.dxf`, `_A2` …, with `REVISIONS.md` |
| `out\` | Build output of `04 Code\drawings\build.py` and `plot.py` (rebuilt at any time; not edited by hand) |
| `templates\` | Office drawing templates: `BEAM_SCHEDULE_TEMPLATE` (.xlsx data with example rows, .dxf / .dwg drawn from it at full size, plot 1:25): the office RC beam schedule (RC rules §15.3). Copy the .xlsx to `04 Code\beam_schedule.xlsx` and draw it with `drafter.beam_schedule` |

- Backgrounds from other disciplines plot on colour 9 (EIT §19.2).
- A DWG received from outside is converted to DXF through the AutoCAD Core Console before scripts read it.
- A review print is copied from `out\` to `07 Review`; an issue is copied to `09 Publish`. Nobody works from `out\`.
