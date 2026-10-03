# Steel Roof Truss T1 (project SRT)

**Drawing set:** SRT-ST, 6 sheets, A3, stage **D**, revision **A** "ISSUED FOR REVIEW", 03/10/2026.
**Status:** preliminary design, for review. **Not for fabrication.**

A Pratt roof truss of circular hollow sections, designed and drawn by script: `calc_truss.py` sizes every member
and connection, and the drawing scripts take every size, length, gap and eccentricity from it.

## 1. Design basis (assumed 2026-10-03, to confirm)

| Item | Value |
|---|---|
| Geometry | Pratt, parallel chords; span 25.0 m between bearings; depth 1.25 m between chord centre lines; 20 panels of 1.25 m; a vertical at every node; diagonals slope down toward midspan (tension under gravity) |
| Use | Roof trusses at 6.0 m; metal sheet on purlins at every top node |
| Loads | Dead 0.30 kPa (sheet, purlins, services) + self-weight x 1.15; roof live 0.50 kPa (Ministerial Regulation No. 6), also on half the span; wind **net uplift 0.75 kPa, assumed** |
| Combinations | ASCE 7-16 2.3: 1.4D; 1.2D + 1.6Lr; 1.2D + 1.6Lr (half span); 0.9D + 1.0W |
| Code | AISC 360-16 LRFD: members D, E, F8, H1; HSS-to-HSS joints K3 (Table K3.1, limits Table K3.1A); plate on round HSS K2 (Table K2.1); welds and bolts J. AISC Design Guide 24: effective lengths 8.4, unbalanced joints 8.2, flange splice 5.4, slotted tube end 5.3. Branch welds to AWS D1.1:2015 Fig 9.10 |
| Material | JIS G 3444 STK400 (Fy 235, Fu 400 MPa); design wall 0.93 x nominal (AISC B4.2); welded plates SM400B; bolts grade 8.8; anchor rods SS400, headed |
| Restraint | Top chord at every node (purlins + roof bracing, by others); bottom chord by fly braces at B4, B8, B12, B16 (5.0 m) |
| Analysis | Pin-jointed plane truss on the node centre lines (direct stiffness, `numpy`); K = 0.9 chords, 0.75 webs (DG24 8.4); the work-point eccentricity moments are added to the chord checks |

## 2. Results (`python calc_truss.py`, revised 2026-10-03 after the DG24 / DG21 / DSC review)

| Mark | Members | Section | Governing | Utilisation |
|---|---|---|---|---|
| TC1 / TC2, BC1 / BC2 | Top / bottom chord (one section) | CHS 165.2 x 7.1 | -492 / +487 kN | 0.72 / 0.71 |
| D1 / D2 | Diagonals, panels 1 - 5 and 16 - 20 (D1 = end panel) | CHS 76.3 x 3.2 | +132 kN | 0.91 |
| D3 / D4 | Diagonals, panels 6 - 15 (D4 = loose, panels 7 and 14) | CHS 76.3 x 2.8 | +63 / -17 kN | 0.49 |
| V1 | End verticals (over the bearings) | CHS 101.6 x 3.2 | -98 kN | 0.94 (cross joint at the bearing) |
| V2 | Verticals | CHS 76.3 x 2.8 | -93 kN | 0.78 |

- **Why the webs grew:** AISC 360-16 Table K3.1A (= DG24 Table 8-1A) allows a gapped K-joint only for Db/D >= 0.4. The
  first issue had 60.5 and 48.6 webs on the 165.2 chord (0.37 / 0.29), outside the limits. All webs are now >= 76.3
  (0.46).
- **Joints:** welded gap K-joints, e = 35 mm (e/D 0.21), gaps 20 - 21 mm as drawn. At the end top nodes e is held at
  the 0.25D limit (41 mm) and the gap is 13 mm (>= 12 and >= tb1 + tb2). Unbalanced nodes are checked as K + X (top)
  or K + Y (bottom). The highest K-joint utilisation is 0.73; the support X-joint governs at 0.94. The chords run 210
  mm past the end nodes for the K3.1A end distance (156 mm beyond V1).
- **Branch welds:** AWS D1.1 Fig 9.10 zones from the computed dihedral angle. Legs HEEL / SIDE / TOE: D1 / D2 8 / 6 / 5,
  D3 8 / 5 / 4, V1 - / 6 / 5, V2 - / 5 / -. The toe edge of the diagonals and the out-of-plane sides of V1 are
  bevelled. The heel includes the 3 mm Z loss.
- **Splices:** three shop pieces SP1 - SP3. Bolted flange plates FS1 / FS2: PL 16, Ø325, 6-M20 x 65 grade 8.8 on PCD
  245, a = b = 40 (DG24 5.4). The plate governs at 0.95 (bolts 0.73). The flange weld is 6 mm (DG24 Eq 5-7), down from
  11. The loose diagonal D4 is a knife plate in the slotted tube end, lapped on a gusset offset 10 mm from the truss
  plane, 2-M20 x 50. The top-chord gusset governs at 0.72.
- **Fly braces FB1:** L 60 x 60 x 5 at F = 45° to the purlin, both sides at B4, B8, B12, B16; nodal braces to AISC 360-16 App. 6.2 (1.9 kN, KL/r 184 <= 200); 1-M16 8.8/S at the lug, 2-M16 8.8/S at the purlin web.
- **Bearings:** reactions 99 kN down, 27 kN up (factored). Saddle seat, base PL 220 x 220 x 16, 4-M20 headed rods in
  Ø33 holes with PL 80 x 80 x 8 washers. Pin end: the washers are site-welded after setting. Sliding end: slots 33 x
  60 for +-12.6 mm (thermal +-4.5 + bottom-chord stretch 8.1), double nuts.
- **Deflection, camber and weight:** D + Lr 68.5 mm = L/365 (limit L/240). Camber 35 mm at midspan, ordinates on
  3/3001. About 1.9 t per truss: tubes 1688 kg + plates 162 kg + 2 %.

## 3. Sheets

| Sheet | Content |
|---|---|
| SRT-ST-1001 | General notes: design criteria with the K3.1A limits, materials, fabrication and welding (WPS, welder qualification, inspection), protection, erection (stability, lifting); TABLE 1 design summary; weld symbol key |
| SRT-ST-3001 | Half elevation 1:50 with member marks, the fly-braced nodes and cutting plane 1/5004; assembly diagram 1:200 (shop pieces, FS1 / FS2); camber diagram; TABLE 2 member schedule (marks, grade, length, end preparation); TABLE 5 plates and fittings |
| SRT-ST-5001 | Typical top and bottom nodes, centre node 1:10 (WP, e, gap, set-out stations, weld symbols); typical branch weld zones 1:1; TABLE 3 node geometry and weld legs |
| SRT-ST-5002 | End top node, section 2 through the saddle, bearing elevation 1:10 (anchor rods, levelling nuts, washers, levels); base plates (pin and sliding) |
| SRT-ST-5003 | Chord flange splice and flange plate 1:5; loose diagonal 1:10 |
| SRT-ST-5004 | Fly bracing (after Beca SE-1505): section 1 at a braced node 1:20, with dashed callouts to the lug end (2) and purlin end (3) at 1:5 and the purlin named on its own band; TABLE 6 fly bracing schedule; notes. TABLE 4 (site connections and field bolts) is on 1001 |

Drawing rules: `docs/steel/STEEL_DETAILING_INSTRUCTION.md`; sources: `docs/steel/reference/SOURCES_STEEL_DETAILING.md`; general rules: `docs/general/`.

## 4. Build and plot

From PowerShell, in this folder:

```powershell
python calc_truss.py        # design report
python build.py             # -> out\SRT-ST_Steel_Roof_Truss_T1_A3_RevA.dxf (+ library\INDEX_srt.csv)
python plot.py              # -> out\...pdf / .dwg, library\DET-*.dwg  (AutoCAD; --ezdxf or no AutoCAD: ezdxf PDF)
```

The build runs the design first and caches it in `out\.design_<hash>.pkl` while `calc_truss.py` is unchanged; the first build takes about 30 - 50 s. Like every R2 build, it exits with code 1 on any `!!` layout problem.

| File | Role |
|---|---|
| `calc_truss.py` | Design: loads, analysis, sizing by search over the JIS G 3444 sizes, member and joint checks, connections, the drawn node geometry (`layout`, `outline`) |
| `srt_engine.py` | Project data and options on the drafting engine (`drafter/td_engine.py`, with `LEADER_ORTH` and `WRAP_UNITS` on) and the steel helpers (`drafter/steel.py`); the design, marks and the truss members drawn from it (chords and branches with walls trimmed at pipe breaks, branch welds) |
| `srt_sheets.py` | The views and the six sheets, notes and tables |
| `build.py`, `plot.py` | Drivers |

To change the design (span, loads, spacing, sizes, splice panels), edit the constants at the top of `calc_truss.py` and rebuild: the sheets follow. For a new revision, set `rev` in `srt_engine.py` (`PROJ`), add a row to `td_engine.REVS` there, and change `BASE` in `srt_sheets.py` and `plot.py`.

## 5. Open items (before "FOR FABRICATION")

- [ ] **Wind:** replace the assumed 0.75 kPa uplift with the project wind assessment (DPT 1311); it governs the bottom chord in compression, the reversal of the diagonals and the anchor rods.
- [ ] **Roof framing by others:** purlin size (C 150 x 65 x 20 x 3.2 assumed for the cleat and fly-brace holes) and the roof bracing layout. Confirm the fly-brace holes in the purlin web with the purlin supplier (S9A.3).
- [ ] **RC supports:** anchor rod embedment and edge distances (ACI 318 Ch. 17) and the bearing level, by the RC designer.
- [ ] **Sections:** confirm the JIS G 3444 / TIS 107 sizes and grades with the supplier, and the camber method with the fabricator.
- [ ] **Shop drawings:** cut lengths adjusted for camber, saddle profiles, WPSs (STK400 / SM400B are not D1.1-listed
  steels) and the trial assembly of the splices, by the fabricator.
- [ ] **Bearing level BL** and the anchor rod setting plan with the RC designer.
- [ ] **Title block:** owner, location, design office, names and signatures.
