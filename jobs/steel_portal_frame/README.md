# Steel portal-frame building 26 x 90 m (project SPF)

**Drawing set:** SPF-ST, 8 sheets, **A1**, stage **D**, revision **A** "ISSUED FOR REVIEW", 04/10/2026.
**Status:** for review, **not for construction**. Project name, location and numbers are placeholders (user,
2026-10-04).

The structural steelwork of a building that the engineer designed in **MIDAS GEN NX** (live model read through the
MAPI, 2026-10-04): plans, elevations, the typical frame, and every member connection. The RC part (pedestals,
footings, slab) is by others; the base reactions are on SPF-ST-1001.

## 1. How it is built

| Step | File | What |
|---|---|---|
| Read the model | `pull_model.py "<MAPI-KEY>"` | **Read-only** (GET /db, POST /post/table). Writes `model/spf_model.json` (geometry, sections, supports, releases, tapered groups, load cases, combinations, beam loads of a typical frame) and `model/spf_forces.json` (envelopes of every element end over the 35 active steel-design cases NU*, concurrent forces at joint nodes, reactions). The key is a command-line argument only (`midas/MIDAS_GEN_NX_INSTRUCTION.md` M1) |
| Design | `calc_spf.py` | Connections, bases, bracing ends and the proposed secondary framing from the snapshot; prints every check; exit 1 if a connection check fails |
| Draw | `spf_engine.py`, `spf_sheets.py`, `spf_details.py`, `spf_details2.py`, `spf_plans.py` | A1 sheets on the shared engine (`td_engine.use_paper("A1", ...)`) |
| Build / plot | `python build.py`, `python plot.py [--ezdxf]` | DXF, then PDF + DWG with AutoCAD and the office **STRUCT-A1-A2.ctb** (copied byte for byte into AutoCAD's Plot Styles if missing), LTSCALE equivalent to 45 at 1:100 |

## 2. The model (as read, 2026-10-04)

| Item | Value |
|---|---|
| Frames | 26 m span, **9 bays x 10 m = 90 m** (grids 1 - 10), eave work point +6.000, slope 0.325 (18.0 deg), ridge +10.224; pinned bases (1110001) |
| Columns | Tapered welded 300 -> 800 x 250 x 8 x 14 (tapered group C1) |
| Rafters | Haunch 800 -> 350 x 250 x 6 x 12 over 5.2 m (group R1), then 350 x 200 x 6 x 10 to the ridge |
| Canopies | 400 x 200 x 6 x 10: 3.3 m at grid A, 4.2 m at grid B |
| Roof monitor | H 100 x 100 posts at 1.0 m each side of the ridge, rafters to 10.75 m |
| Gable frames | Corner columns as C1; posts H 400 x 150 x 6 x 10 at 4.5 / 8.5 / 13 / 17.5 / 21.5 m; continuous rafter 400 x 200 x 6 x 10; eave ties H 200 x 100 |
| Bracing | Roof X-bracing PG 165.2 x 4.5 in bays 1 - 2 and 9 - 10; struts PG 165.2 (braced bays), PG 190.7 (eaves, ridge); eave beams H 400 x 200 x 8 x 13 in the end bays (no wall bracing) |
| Material | SM520 for every member (JIS); E 205 000 |
| Loads | DL (self-weight), SDL 0.20 kPa, LL 0.50 kPa, ASCE 7 wind (cases 1 - 4, roof and wall pressures as beam loads); 35 factored static cases NU* = the active steel-design combinations; P-Delta on DL + SDL |

## 3. Design summary (`python calc_spf.py`)

| Mark | Connection | Result |
|---|---|---|
| KJ1 | Knee, 4E end plate on the tapered inner flange of the column head CH1 | 8-M24 10.9, PL 22 x 270; Mu* 749 kN.m (NU2); the column flange needs 17.1 mm, so **the column head CH1 has both flanges PL 20 (proposed)**; continuity plates PL 16; panel zone OK (tension field under gravity) |
| CS1 | Column splice between the column C1 and the head CH1, +4.950, 4E plates square to the column axis | 8-M24 10.9, PL 22 x 270; Mu* 615 kN.m (envelope at the element end above the splice, conservative); 232 mm bolting room under the continuity plate (200 required) |
| CJ1 | Canopy root, on the outer flange of the column head CH1 | 8-M20 10.9, PL 20 x 220 |
| SP1 | Haunch / rafter splice at 5.2 m | 8-M20 10.9, PL 20 x 220 (d 350 just below DG16's tested 400) |
| RJ1 | Ridge, plumb plates | 8-M20 10.9, PL 20 x 220 |
| GK1 | Gable corner, column cap under the continuous gable rafter | 8-M20 10.9, PL 16; **rafter bottom flange PL 16 over the column (proposed)** |
| GS1 / GS2 | Gable rafter splices (6.5 m, ridge post) | 8-M20 10.9, PL 20 |
| EB1 | Eave beam end-plate splice on a stub welded to the column web | 8-M20 10.9, PL 20 |
| BP1 / BP2 | Pinned bases | PL 20, 4-M24 / 4-M20 rods, plate washers site-welded |
| BR1 / ST1 / ST2 | Slotted CHS on knife plates, field-bolted to gussets GU1 | 2 / 2 / 3-M20 8.8 |
| PU1, GT1, GT2, SR1, FB1, FB2 | **Proposed** (not in the model): H 175 x 90 purlins at 1.17 m, H 175 x 90 side girts and H 125 x 60 gable girts at 1.5 m, sag rods Ø12 at third points, fly braces L 50 x 50 x 5 | TBC |

Basis: AISC DG4 (2nd ed.) 4E thick-plate with the column side, DG16 range checks and knee panel zone, DG29 / DG24 for
the bracing ends, DG25 for the tapered members (digests: `docs/steel/reference/SOURCES_STEEL_DETAILING.md` Parts F -
I). Bolts: ISO 898 10.9 pretensioned at moment end plates, 8.8 elsewhere (user, 2026-10-04).

## 4. Drawn geometry versus the analysis model

- Columns are tapered **symmetrically about the grid line**, as analysed (both flanges slope 2.4 deg). The
  flanges are straight from the base to the cap: the model taper stops at the work point (800 at +6.000), and the
  drawing continues it to 835 at the cap (`calc_spf.col_depth`).
- The column is two pieces (user, 2026-10-04): C1 from the base to the splice CS1 at +4.950, and the head CH1 / CH1A
  from the splice to the cap, with both flanges PL 20. The knee and canopy end plates lie on the tapered head flanges
  with square ends and bolts (STEEL_DETAILING_INSTRUCTION S2.9, S7.7).
- Rafters keep the **top flange in the roof plane** (purlins on one line); the prismatic rafter centre line is the
  model work line and the haunch deepens downward; the canopy and gable rafter top flanges are in the same plane.
- Levels: model Z = 0 = underside of the base plates.

## 5. Findings and open items (also TABLE 2 on SPF-ST-0001)

1. **Ridge strut CHS 190.7 x 4.5 overstressed?** 238 kN compression (NU2) against about 178 kN buckling over 10 m
   (KL/r 152). The member is the engineer's; check the model's code check, grade and load path.
2. **No wall bracing:** longitudinal stability relies on the end-bay eave beams acting with the columns about their
   weak axis. Confirm the intent and the column weak-axis checks.
3. **P-Delta** is set on DL + SDL only, not per combination (DG25 6.2.6).
4. The column head CH1 (both flanges PL 20) and splice CS1 at the knee, and the gable-rafter flange thickening at
   GK1, change the members: engineer to confirm, or use a DG16 thin-plate design.
5. Pipes taken as STK490 (the model used SM520); pedestal f'c 24 MPa assumed; anchor rods F1554 Gr 36 / SS400.
6. Secondary framing proposed from the model's MWFRS pressures; ASCE 7 components-and-cladding not checked.
7. Font (Arial Narrow, the repository default) vs the office A1 project font; placeholder project data and datum.

## 6. Sheets

| Sheet | Content |
|---|---|
| SPF-ST-0001 | General notes, design criteria, materials, fabrication, erection, weld key; TABLE 1 connection summary, TABLE 2 open items, TABLE 3 drawing list |
| SPF-ST-1001 | Anchor bolt and column layout plan 1:200; BP1 / BP2 plans 1:10; TABLE 4 base reactions |
| SPF-ST-1002 | Roof framing plan 1:200; TABLE 9 secondary framing |
| SPF-ST-2001 | Side-wall elevation 1:200, gable elevation 1:100 |
| SPF-ST-3001 | Typical frame (grids 2 - 9) 1:50; TABLE 5 member schedule, TABLE 6 tapered plates |
| SPF-ST-5001 | Knee + canopy root with the column head and splice CS1, rafter splice, ridge + monitor bases, views on the end plates (A - D), 1:10 |
| SPF-ST-5002 | Base elevations, gable corner, gable splice, post top, eave beam, 1:10 |
| SPF-ST-5003 | Braced-bay node, section at a fly-braced purlin 1:10; TABLE 7 end plates, TABLE 8 field bolts |
