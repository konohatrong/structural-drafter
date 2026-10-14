# 14 Shear by friction, bearing and lugs (DG1 §3.5.1, §3.5.2)

Three ways to move base shear into concrete:
1. **friction** between plate and grout or concrete;
2. **bearing** of the column, plate or a **shear lug** against concrete;
3. **shear in the anchor rods** (15).

## Friction [CODE + DG]

- Usually enough in ordinary bases.
- **φVn = φ μ Pu ≤ 0.2 f′c Ac**, with the **least favourable compression consistent with the shear** being checked (e.g. 0.9D with wind, not D + L).
- **μ = 0.55 steel on grout, 0.70 steel on concrete.**
- [REC] No friction where the column has net uplift in that combination.

## Bearing on an embedded column or plate [CODE]

- Against an embedded plate or column near the surface (ACI 318-02): **φP_brg = 0.55 f′c A_brg** (Fig. 3.5.1).
- Example 4.8: W12×50, Vu 100 kips: plate edge 68.8 kips + flange 31.2 kips → **embed 4 in.** (100 mm).

## Shear lugs (ACI 349-01 App. B) [CODE + DG]

Mechanism: shear first goes by bearing helped by **confinement** from the tension anchors and external axial load, then by shear friction.

- Lug bearing: φ1.3 f′c A1 with φ 0.60 → **φP_brg ≈ 0.80 f′c A_lug**. A_lug is the **embedded** area only, not the part in the grout.
- Confinement: φ Kc (Ny − Pa) with φ 0.75, Kc 1.6 → **1.2 (Ny − Pa)**; Ny = n Ase Fy of the tension anchors; Pa positive in tension. Count compression only if it is surely present with the shear.

Totals:
- lug: **φPn = 0.80 f′c A_lug + 1.2 (Ny − Pa)**;
- column or plate side: **φPn = 0.55 f′c A_brg + 1.2 (Ny − Pa)**.

## Lug checks and rules [DG]

1. **Concrete in front of the lug, towards a free edge:** uniform tension **4φ√f′c** (psi), φ = 0.75, on the area of a **45° plane** from the lug's bearing edge to the free surface, **less the lug's own bearing area**. This often governs on piers.
2. **Plate bending from the lug**, especially for large bracing shears about the column's weak axis. **Base plate at least as thick as the lug.**
3. **Multiple lugs** for large shear, spaced per ACI 349 App. B.
4. **Grout pockets** large enough to fill; **flowable non-shrink grout**; grout holes (06).
5. Lug moment: cantilever from mid-embedment, **M = V (G + d/2)**, G = grout thickness, d = embedded depth.
6. Lug welds: heavy fillets, sized for the shear and the moment couple.

## Example 4.9 [DG]

W10×45 on a 20 in. pier; wind shear 23 kips → **Vu 36.8 kips**; f′c 4 ksi; confinement ignored.
- Required bearing area 11.5 in²; lug 9 in. wide → **embedment 1½ in.** below the 2 in. grout.
- Front shear area 207 in² → 39.2 kips ≥ 36.8. OK.
- M = 36.8 (2 + 0.75) = 101 kip-in. → **lug 1¼ in. thick**, base plate ≥ 1¼ in.
- Welds: 5/16 in. fillets fail (7.98 > 6.96 kips/in.) → **⅜ in. fillets**.
- The text says "the W10×45 of Example 4.6"; it is **Example 4.5**.

## Office note [REC]

Show the lug size, embedment below grout, grout pocket and weld on the base detail.
