# 09 Concentric compression (DG1 §3.1)

The plate must be **large enough** for concrete bearing and **thick enough** not to yield.

## Concrete bearing [CODE]

- Full area: **Pp = 0.85 f′c A1**.
- Support larger on all sides: **Pp = 0.85 f′c A1 √(A2/A1) ≤ 1.7 f′c A1**, so √(A2/A1) ≤ 2.
- A1 = plate area (holes not deducted). A2 = the **largest area geometrically similar to and concentric with the plate** that fits on the concrete top surface. Far from edges, √(A2/A1) = 2.
- φ = 0.60 in AISC 360-05 against **0.65 in ACI 318-02**; DG1 uses **0.65** with Ω = 2.50. [REC] AISC 360-10 onward: φ = 0.65, Ω = 2.31 (01).
- Bearing on grout: use the **concrete f′c** (grout is specified at 2 f′c).

Required area:
- A2 = A1: A1,req = Pu / (φ 0.85 f′c);
- A2 ≥ 4A1: A1,req = Pu / (2 φ 0.85 f′c).

## Plate yielding, W shapes [DG]

Uniform pressure fpu = Pu / (BN). Cantilever l = max(m, n, λn′):
- **m = (N − 0.95d) / 2**;
- **n = (B − 0.8bf) / 2**;
- **λn′ = λ √(d bf) / 4** (yield line between the flanges, Thornton 1990);
- X = [4 d bf / (d + bf)²] · Pu / (φc Pp);
- λ = 2√X / [1 + √(1 − X)] ≤ 1; **λ = 1 is conservative**.

Thickness:
- LRFD: **t_min = l √(2 Pu / (0.9 Fy B N))**;
- ASD: t_min = l √(2 · 1.67 Pa / (Fy B N)).

The thinnest plate comes with **m ≈ n**.

## HSS and pipe [DG]

- Rectangular HSS: yield lines at **0.95 × depth and 0.95 × width**.
- Round HSS and pipe: at **0.8 × diameter**, both ways.
- **No λ term.**

## Sizing procedure (§3.1.4) [DG]

| Case | Condition | Note |
|---|---|---|
| I | A2 = A1 | Simplest, largest plate |
| II | A2 ≥ 4A1 | Smallest plate; footing far from edges |
| III | A1 < A2 < 4A1 | Typical on piers; trial and error |

1. Pu or Pa.
2. A1,req for the case.
3. **N ≈ √A1,req + Δ**, Δ = (0.95d − 0.8bf) / 2; B = A1,req / N. In practice **N = B**.
4. Case II: check A2 ≥ 4A1. Case III: compute A2 for the trial plate and check Pu ≤ φPp; revise until it passes.
5. l and t_min as above.
6. Rods: for gravity columns, sized for **OSHA and practice** only (01, 04).

Fit the **rod locations and wrench clearance** inside the plate when choosing N and B.

## Office note [REC]

- In SI: f′c and Fy in MPa, dimensions in mm, P in N; the formulas are dimensionless in form.
- Write `calc_baseplate.py` per column type: it returns N, B, t, the governing l and the bearing ratio, and is the single source for the base plate schedule (AGENTS.md §2, "data first").
- Round t up to the plate thicknesses in stock (e.g. 20, 25, 32, 40, 50 mm) and keep a few standard plates per job.
