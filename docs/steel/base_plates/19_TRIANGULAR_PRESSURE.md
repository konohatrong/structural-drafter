# 19 Triangular pressure distribution (DG1 App. B)

The body of DG1 assumes **uniform** bearing (12, 13), as ACI does. Appendix B gives the **triangular** alternative. Neither is "elastic" or "ASD": both are approximations, valid for LRFD and ASD. Triangular pressure usually gives a **slightly thicker plate and slightly smaller rods**, because the pressure centroid is nearer the cantilever edge.

## Thickness from a moment per unit width [DG]

**t = √(4 Mpl / (φ Fy))** with φ = 0.90; ASD √(4 Mpl Ω / Fy), Ω = 1.67. Mpl in kip-in. per in. of plate.

## Kern [DG]

- fpa = P / (B N); fpb = M / S_pl, with S_pl = B N² / 6.
- Zero pressure at the edge when fpa = fpb → **e_kern = N / 6**.
- **e ≤ N/6:** small moment, all bearing. **e > N/6:** large moment, rods in tension.

## Small moment (B.4.1) [DG]

1. Trial N ≥ d + 6 in., B ≥ bf + 6 in. (four rods).
2. m = (N − 0.95d)/2, n = (B − 0.8bf)/2.
3. P, M; e = M/P ≤ N/6.
4. **fp(max) = (P / BN)(1 + 6e/N) ≤ fp,avail** = φ 0.85 f′c (√(A2/A1) where it applies); fp(min) = (P / BN)(1 − 6e/N).
5. Pressure at the m line: fpm = fp(max) − 2 fpb (m / N).
6. **Mpl = fpm m² / 2 + (fp(max) − fpm) m² / 3.**
7. Bending about the n line: DG1 uses the **axial pressure only**, Mpl = fpa n² / 2, for small moments. Large moments need a more refined analysis.
8. t from the larger Mpl.

**Example B.5** (the data of Ex. 4.6): 19 × 19 in.; e 2.5 < 3.17 in.; fp(max) 1.86 ksi, fpm 1.56 ksi; Mpl at m 10.6, at n **11.1 kip-in./in.** → t 1.17 in. → **1¼ in.** (uniform method: 1½ in.).

## Large moment (B.4.2) [DG]

- A′ = distance from the rods to the column centre; N′ = distance from the rods to the far (compression) edge; A = bearing length.
- Equilibrium: T + P = fp A B / 2, and P A′ + M = (fp A B / 2)(N′ − A/3).
- **A = [f′ − √(f′² − 4 (fp B / 6)(P A′ + M))] / (2 fp B / 6)**, with f′ = fp B N′ / 2 (smallest positive root).
- **T = fp A B / 2 − P.**
- Use fp = the available bearing stress: φ 0.85 f′c √(A2/A1) ≤ φ 1.7 f′c (φ 0.60 here).
- If A approaches N′, bearing reaches the rods and they cannot develop tension: **enlarge the plate**.
- Mpl is the larger of the bearing moment and the rod moment. For the rods, spread each rod force at 45° to the critical section at 0.95d, unless the spread meets the plate edge (Fig. B.5).

**Example B.5.2:** W8×31; Pu 90 kips, Mu 720 kip-in.; f′c 3 ksi; A2/A1 = 4; plate 14 × 14 in.; e 8.0 > 2.33 in.; φfp 3.06 ksi; A = 5.27 in.; Tu 22.8 kips (11.4 kips per rod). Bearing Mpl 12.5 kip-in./in. governs over the rods' 11.4 → **14 × 14 × 1¼ in.**

## Choosing [REC]

- **One method per project**, named in the design basis. Default: uniform (12, 13); triangular for checking older designs or software.
- Report e against its own limit (e_crit or N/6); do not mix them.
