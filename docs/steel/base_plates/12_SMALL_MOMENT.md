# 12 Base plates with small moments (DG1 §3.3)

Method of Drake and Elkin (1999), revised by Doyle and Fisher (2005). It assumes a **uniform bearing stress** over a length Y, and works for LRFD or ASD with Pr, Mr. The triangular alternative is in 19.

## Small or large? [DG]

- Bearing resultant q·Y with **q = fp × B**; maximum **q_max = fp(max) × B**.
- Equivalent eccentricity **e = Mr / Pr**.
- Critical eccentricity: **e_crit = N/2 − Pr / (2 q_max)**.
- **e ≤ e_crit → small moment:** bearing alone holds the moment; **no rod tension**.
- **e > e_crit → large moment:** rods in tension (13).

## Bearing [DG]

- **Y = N − 2e**, centred under the resultant.
- **fp = Pr / (B Y)** ≤ fp(max); equivalently q = Pr / Y ≤ q_max.
- fp(max) = φ 0.85 f′c √(A2/A1) (LRFD) or ÷ Ω (ASD), as in 09.

## Plate thickness at the bearing side [DG]

Cantilever m = (N − 0.95d)/2 for strong-axis bending:

| | LRFD | ASD |
|---|---|---|
| Y ≥ m | **t = 1.5 m √(fp / Fy)** | t = 1.83 m √(fp / Fy) |
| Y < m | **t = 2.11 √(fp Y (m − Y/2) / Fy)** | t = 2.58 √(fp Y (m − Y/2) / Fy) |

- The constants come from φ = 0.90 / Ω = 1.67 on Mn = Fy t²/4 per unit width.
- **If n > m, substitute n for m.** When n governs, yield-line analysis or triangular pressure (19) may give a thinner plate.
- **No tension interface check:** with e ≤ e_crit the rods carry nothing.

## Procedure (§3.3.4) [DG]

1. Pr and Mr for each combination.
2. Trial N × B. For four rods: **N ≥ d + 6 in. (150 mm), B ≥ bf + 6 in.**
3. e and e_crit. If e > e_crit, go to 13.
4. Y = N − 2e; check fp.
5. t from the table, with m and n.
6. Rods for OSHA and practice (01, 04).

## Example 4.6 [DG]

W12×96 (d 12.7 in., bf 12.2 in.); D 100 + L 160 kips; moments 250 + 400 kip-in.; f′c 4 ksi; A2 = A1; Fy 36 ksi.
- LRFD: Pu 376 kips, Mu 940 kip-in. → e = 2.50 in.
- Plate 19 × 19 in.: q_max = 42.0 kips/in.; e_crit = 5.02 in. → small moment.
- Y = 14 in.; fp = 1.41 ksi.
- m = 3.47 in. → t = 1.03 in.; **n = 4.62 in. governs → 1.36 in.** (ASD 1.39).
- **Use 1½ × 19 × 19 in.** (38 × 480 × 480 mm), four ¾ in. Gr 36 rods.

## Office note [REC]

- Check **every** load combination: one with low axial load may turn a small-moment base into a large one, often the wind uplift case.
- Pinned bases carry no moment by design, but OSHA erection moment still applies (01).
