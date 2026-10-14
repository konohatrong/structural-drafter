# 10 Uplift and anchor rod tension (DG1 §3.2, §3.2.1)

## Four steps [DG]

1. **Maximum net uplift** from the analysis: wind uplift greater than roof dead load, or overturning in rigid bents and braced bays.
2. **Rod grade, number and size** (02, below).
3. **Plate thickness and welds** to carry the uplift into the rods.
4. **Anchorage in the concrete** (11).

**Prying** is normally neglected: the plate is designed as a cantilever about the web or flanges, and long rods are flexible compared with steel-to-steel joints.

## Rod strength [CODE]

The strength of the rods is the **lesser** of the sum of the steel strengths of the rods in tension and the **concrete strength of the group** (11).

Two equivalent ways to treat the threads:
- **AISC**, on the nominal (body) area Ab: **Rn = 0.75 Fu Ab**; LRFD φ = 0.75 → **0.5625 Fu Ab**; ASD Ω = 2.00 → **0.375 Fu Ab**.
- **ACI Appendix D**, on the tensile stress area Ats = 0.7854 (D − 0.9743/n)²: φ Fu Ats with φ = 0.75.

Stay within one system for a calculation; the results agree.

## Table 3.1 extract: rod-only strength, kips (kN) [DG]

| Dia. in. | Ab in² | LRFD Gr 36 | LRFD Gr 55 | ASD Gr 36 |
|---|---|---|---|---|
| ⅝ | 0.307 | 10.0 (44) | 12.9 (57) | 6.7 (30) |
| ¾ | 0.442 | 14.4 (64) | 18.6 (83) | 9.6 (43) |
| ⅞ | 0.601 | 19.6 (87) | 25.4 (113) | 13.1 (58) |
| 1 | 0.785 | 25.6 (114) | 33.1 (147) | 17.1 (76) |
| 1¼ | 1.23 | 40.0 (178) | 51.8 (230) | 26.7 (119) |
| 1½ | 1.77 | 57.7 (257) | 74.6 (332) | 38.4 (171) |
| 2 | 3.14 | 103 (458) | 133 (592) | 68.3 (304) |

The full table runs ⅝ – 4 in. and includes Gr 105.

## Plate bending from rod tension [DG]

- **One-way:** cantilever about the **web** or the **flanges**, the rod force times its lever arm to the face. If the web takes the load, **check the web and its weld**.
- **Two-way** (rods inside the flanges): bending about web and flanges together, with moments compatible with the plate's deformation.
- **Effective width:** a **45° spread** from the rod centreline to the face of the flange or web. Example 4.5: rod 2 in. from the web centre, tw 0.35 in. → b_eff = 2(2 − 0.175) = 3.65 in.
- Thickness: t = √(4 Mu / (φ b_eff Fy)), φ = 0.90.
- Weld: force per unit length = T / b_eff each side; check the web stress too.

## Office note [REC]

- Use the uplift combination with **0.9D** (LRFD) or **0.6D** (ASD) and the full wind.
- Report T per rod, the rod check, the plate bending check with b_eff, the weld and the web, then the concrete checks (11), all in `calc_baseplate.py`.
- For M-size rods: Fu of the specified grade, Ab = π d² / 4, and the same 0.75 factor.
