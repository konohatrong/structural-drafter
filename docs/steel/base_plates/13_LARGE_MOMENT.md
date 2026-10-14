# 13 Base plates with large moments (DG1 §3.4)

Large moment: **e > e_crit = N/2 − Pr / (2 q_max)**. Bearing alone cannot hold the moment, so the rods on the tension side pull (Fig. 3.4.1). Typical for **rigid frames under wind or seismic load**.

## Bearing length and rod force [DG]

- Bearing at its limit: **q = q_max = fp(max) B**.
- **f** = distance from the plate centreline to the tension rods.
- Vertical equilibrium: **T = q_max Y − Pr**.
- Moments about the rods give the quadratic:
  **Y = (f + N/2) − √[(f + N/2)² − 2 Pr (e + f) / q_max]** (take the smaller root).
- **A real solution exists only if (f + N/2)² ≥ 2 Pr (e + f) / q_max** (Eq. 3.4.4). If not, **enlarge the plate**.
- Check: at e = e_crit the formula gives Y = Pr / q_max and T = 0, matching 12.

## Thickness at the bearing side [DG]

fp = fp(max), and the 12 formulas apply:
- Y ≥ m: t = 1.5 m √(fp(max) / Fy) (LRFD), 1.83 (ASD);
- Y < m: t = 2.11 √(fp(max) Y (m − Y/2) / Fy) (LRFD), 2.58 (ASD);
- substitute n where n > m.

## Thickness at the tension side [DG]

- Cantilever from the rod line to the **centre of the column flange**: **x = f − d/2 + tf/2**.
- Moment per unit width Mpl = T x / B.
- **t = 2.11 √(Tu x / (B Fy))** (LRFD); **2.58 √(Ta x / (B Fy))** (ASD).
- Alternatively use the bending lines of Fig. 3.1.1.

**Use the larger of the two thicknesses.**

## Procedure (§3.4.4) [DG]

1. Pr, Mr.
2. Trial N × B (N ≥ d + 6 in., B ≥ bf + 6 in.).
3. e > e_crit? Check Eq. 3.4.4; enlarge if it fails.
4. Y, then T.
5. t at bearing and at tension; take the larger.
6. Rods: number and size for T, then pullout and breakout (11).

## Example 4.7 [DG]

W12×96; D 100 + L 160 kips; moments 1,000 + 1,500 kip-in.; f′c 4 ksi; A2 = A1; rods 1½ in. from the edge at first.
- LRFD: Pu 376 kips, Mu 3,600 kip-in. → e = 9.57 in.
- 19 × 19 plate: Eq. 3.4.4 fails (315 > 306).
- **20 × 20 plate:** q_max 44.2 kips/in.; f = 8.5 in.; 324 < 342 → real solution. **Y = 12.0 in., Tu = 156 kips.**
- Thickness: bearing with m = 3.97 in. → 1.48 in.; tension, x = 2.15 in. → 1.44 in.; **bearing with n = 5.12 in. governs, 1.90 in.** → **2 in. plate**.
- Rods: three per side, 52 kips each → **1½ in. Gr 36** (57.7 kips). Pullout 52.6 kips OK.
- The 2 5/16 in. holes need the edge distance raised from 1½ to **2¼ in.**; the rods still work.
- **hef 18 in.**, rods 6 in. apart: A_N 2,590 in² against A_No 972 → φNcbg = 295 kips.
- Under the ACI-02 seismic factor 0.75: rod 43.1 kips < 52 → **larger rods needed**.

## Office note [REC]

- f is set by the **rod edge distance**, which depends on the hole size (04). Fix the hole and edge distance before solving, or the result changes, as in this example.
- Large-moment bases are where the **anchor rod layout, pier size and pier bars** must be agreed with the foundation designer at the same time (11).
