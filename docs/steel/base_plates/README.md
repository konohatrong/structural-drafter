# Column base plates and anchor rods: router

Study notes on **AISC Design Guide 1, *Base Plate and Anchor Rod Design*, 2nd edition** (James M. Fisher and Lawrence A. Kloiber, AISC 2006; 69 pages): materials, fabrication, rod layout, tolerances, erection, grouting, repairs, and design for compression, uplift, moment and shear, plus Appendices A (special joints) and B (triangular pressure).

**Source:** `Design Guide 01 - Column Base Plates and Anchor Design_2nd Ed.pdf` under `G:\My Drive\##Textbook\AISC Design Guide\AISC - Steel Design Guides 2016\`, outside the repository. § numbers are DG1's.

## How to use

- One topic per file, at most 500 words. Read this router, then only the files you need.
- DG1 (2006) follows **AISC 360-05, ACI 318-02 Appendix D and OSHA Subpart R**. Factors changed since are listed in 01; check current codes before using a value.
- US units, SI in brackets. Tags: **[DG]** the guide; **[CODE]** a code value it quotes; **[REC]** an office note.

## Files

| # | File | Read it for |
|---|---|---|
| 01 | `01_SCOPE_BEHAVIOUR.md` | Load cases, limit states, ductility, pinned or fixed, OSHA, code changes since 2006 |
| 02 | `02_MATERIALS.md` | Plate and rod grades (Tables 2.1, 2.2), F1554, nuts, headed vs hooked, galvanizing |
| 03 | `03_PLATE_FABRICATION_WELDING.md` | Minimum thickness, cutting, milling and bearing, column-to-plate welds |
| 04 | `04_HOLES_WASHERS_LAYOUT.md` | Hole and washer sizes (Table 2.3), rod size, pattern, edge distance, piers |
| 05 | `05_PLACEMENT_TOLERANCES.md` | Layout drawing, templates, AISC vs ACI tolerances, drilled-in rods |
| 06 | `06_ERECTION_GROUTING.md` | Setting methods, large plates, grout |
| 07 | `07_REPAIRS.md` | Rods misplaced, bent, short, long or rotated |
| 08 | `08_SEISMIC.md` | Bases in the seismic system, braced and moment frame bases |
| 09 | `09_AXIAL_COMPRESSION.md` | Bearing, A2/A1, m, n, λn′, thickness, Cases I – III, HSS |
| 10 | `10_ANCHOR_TENSION.md` | Uplift procedure, rod strength (Table 3.1), plate bending from rod tension |
| 11 | `11_CONCRETE_ANCHORAGE.md` | Pullout, hooks, breakout cones, side blowout, lapping with pier bars |
| 12 | `12_SMALL_MOMENT.md` | Uniform bearing, e vs e_crit, bearing length, thickness |
| 13 | `13_LARGE_MOMENT.md` | Rod tension and bearing length, real-solution check, tension-side thickness |
| 14 | `14_SHEAR_FRICTION_LUGS.md` | Friction, bearing on embedment, shear lugs |
| 15 | `15_SHEAR_ANCHOR_RODS_HAIRPINS.md` | Shear in rods, welded washers, breakout in shear, hairpins, tie rods |
| 16 | `16_EXAMPLES.md` | Results of Examples 4.1 – 4.11 |
| 16B | `16B_EXAMPLES_MISPRINTS_LESSONS.md` | Misprints found in DG1, lessons from the examples |
| 17 | `17_DOUBLE_NUT_STOOLS_SLEEVES.md` | Double-nut joints, stools, sleeves, pretensioned rods, rods in compression |
| 17B | `17B_FATIGUE.md` | Fatigue category and threshold, redundancy, pole plate thickness |
| 18 | `18_PRETENSION_INSTALLATION.md` | When to pretension, Tm, verification torque, turn-of-nut, installation steps |
| 18B | `18B_INSPECTION_MAINTENANCE.md` | Sleeved joints, inspection after installation and after earthquakes |
| 19 | `19_TRIANGULAR_PRESSURE.md` | Appendix B: kern, small and large moment with triangular pressure |
| 20 | `20_DRAWING_CHECKLIST.md` | [REC] What our base plate and anchor rod drawings and notes must show |

## Quick answers

| Question | Go to |
|---|---|
| Hole and washer size for a rod? | 04 |
| Does the base need anchor rods in tension? | 12 (e ≤ e_crit) or 13 |
| How deep must the rods go? On a pier? | 11 |
| How is the shear carried? | 14, 15 |
| Grout strength and thickness; plate for axial load? | 06; 09 |
| A rod is in the wrong place on site | 07 |
| Light pole, sign or machine base | 17, 17B, 18 |

## Related

`STEEL_DETAILING_INSTRUCTION.md` S8 (anchor rods), S9 (erection); `stairs/11B_CONNECTIONS_CONCRETE_MASONRY.md` (embeds, post-installed anchors).
