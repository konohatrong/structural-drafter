# 09 Stringer design (DG34 §4.3 – 4.4)

## Member choice [DG]

| Stringer | For | Against |
|---|---|---|
| **Channel** (C, MC) | Many sizes; the flange carries guard posts; standard bolted end connections | Wider; its axis is off the web |
| **Plate** | Available, narrowest, standard bolted ends | Low strength for its weight; weak laterally |
| **Rectangular HSS** | Many sizes; the top face carries posts; clean look | More fabrication; harder end connections; heavier |
| W or built-up | Long or special spans | Bulky, less common |

- **Depth 10 – 15 in. (250 – 380 mm)**, at least **10 in.** to fit the treads. Deeper for long spans.
- Architecture often sets the size: C12×20.7 (commercial example), HSS12×2×¼ (industrial).

## Loads on a sloping member [DG]

- **Sloping-beam method:** split the load into components normal and parallel to the stringer, over the full sloping length. The parallel component gives an axial force.
- **Horizontal-plane method (usual):** apply the vertical load on the horizontal projection, with self-weight × √(R² + T²)/T (1.19 for 7 / 11 in.). The **moment is identical** to the sloping-beam method; the **shear is slightly conservative**.

## Deflection needs a factor [DG]

The horizontal-plane method gives deflections **1.1 – 2 times too small**. Analyse the stringer as a sloping beam, or use:

**FΔ = (√(R² + T²) / T)^x · [cos(tan⁻¹(R/T))]^y**  (Eq. 4-1)

- x = 4 for uniform load, 3 for a mid-span point load.
- y = 2 for vertical, 1 for deflection perpendicular to the stringer, as printed.
- For 7 / 11 in., x = 4: **1.40** (y = 2) and **1.67** (y = 1).

[REC] First principles give Δ⊥ = Δh / cos²θ and Δvert = Δh / cos³θ, the reverse of the printed labels. Use the **larger factor** unless the deflection is worked out exactly.

## Support model [DG]

- **Simple span** (pin and roller): the largest deflection.
- **Frame** (pin and pin): less deflection, but **large horizontal thrust**. Typical of stiff end plates between concrete walls.
- **DG34's rule:**
  - design the **member and its deflection as a simple span**;
  - where the supports are rigid, design the **connections and supporting structure for the frame reactions**, including the thrust.
- Prefer flexible supports: shear tabs, slots, bearings.

## Unbraced length [DG]

- **Welded pan or plate treads and risers covering most of the stringer depth** → the stringer is **fully braced** (Fig. 4-5).
- **Bolted grating treads** → take the stringer as **unbraced** unless proven to AISC 360 Appendix 6.3.
- Anything else → check the treads as braces to Appendix 6.3.

## Checks [REC]

1. Loads on the plan projection: self-weight × slope ratio, + 20 plf of guard on the guard stringer, + tread DL and LL.
2. Mu and Vu with the right unbraced length (AISC 360 F, G).
3. Δ_LL ≤ L/360 and Δ_TL ≤ L/240, **after FΔ**.
4. Axial force: from the parallel component, from seismic drift (04B) and from frame thrust.
5. Weak-axis bending from lateral load (10); interaction H1.
6. The local check under each guard post (12B).
