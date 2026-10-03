# ACI Detailing Manual MNL-66(20): review material

This folder holds working material for reviewing our office standard sheets against the ACI Detailing Manual MNL-66(20), which is based on ACI 318-19.
- **Source:** `G:\My Drive\##Workset_Autocad\supplemental Autocad files to ACI Detailing Manual Manual MNL-66(20) 2020\`, the manual PDF plus about 137 supplemental DWGs.
- **Copyright:** the manual is licensed material. Keep this folder internal and do not redistribute it. Office sheets adopt practices, not ACI text.

| Path | Contents |
|---|---|
| `convert.py` | DWG → DXF (`dxf/`) and model-space PDF (`pdf/`, A3, fit) through AutoCAD Core Console, then PNG (`png/`). Run from PowerShell: `python convert.py [filter]`; files already converted are skipped |
| `png/<Category>__<ID>.png` | One image per ACI detail. Categories: Beams, Columns, Slabs, Slab-on-ground, Walls, Foundation |
| `txt/manual.txt` | Full text of the manual by PDF page (`=== PDF PAGE n ===`) |
| `txt/checklists/<ID>.txt` | The design-professional checklist for each detail (112 extracted). For the few missing, grep `manual.txt` for `FIGURE <ID>` |
| `txt/ch5.txt` | Chapter 5, designing for constructability: foundations, walls, columns, beams, slabs |
| `ours/` | Our current sheets rendered for side-by-side review |

**Manual layout:**

| Section | PDF pages | Contents |
|---|---|---|
| Section 1 (ACI 315R-18 text) | ~13 – 60 | Chapter 4 on structural drawings and general notes sheets; chapter 5 on constructability |
| Section 2 | ~62 – 400 | Details, each with its checklist: slabs, beams, columns, walls, foundations, slab-on-ground |
| Section 3 | ~400 – 490 | "Detailing Corner" articles |
| Section 4 | ~490 – 502 | Appendix tables: web widths, development lengths … |

The review findings and the changes made are recorded in `REVIEW_ACI_MNL66.md` in the project root.
