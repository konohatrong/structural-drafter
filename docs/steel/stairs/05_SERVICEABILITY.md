# 05 Serviceability (DG34 §3.3, §8.3, §8.4)

Occupant comfort often sizes a stair member more than its strength does.

## Deflection limits [CODE + DG]

| Member | Live load | Total load |
|---|---|---|
| Stringers, landing beams (floor members) | **L/360** | **L/240** |
| Floor members carrying ceramic tile or masonry | **L/600** [DG] | L/240 |
| Cantilever guard post carrying a handrail | **2h/120 = h/60** (h = post height) | – |
| Guard infill rails, handrail, infill panels | **L/120** | – |

- The guard and post limits are DG34's reading of the IBC limits for exterior walls with flexible finishes. The IBC gives no direct guard limit.
- **ASTM E985** allows much more: post h/12, rail h/24 + l/96. [DG] These are too lax for daily use, so use the table above, or the SER's stricter values.
- **OSHA checkered plate:** L/100, the basis of AISC Manual Table 3-18a, may be judged acceptable on OSHA stairs. **On IBC stairs, use the IBC limits.**

## Deflection of sloping stringers [DG]

- Deflection worked out on the **horizontal projection understates** the real vertical deflection by a factor of **1.1 – 2.0**.
- Either analyse the stringer as a sloping beam, or multiply the horizontal-plane result by **FΔ** (09).
- For a 7 / 11 in. stair, FΔ = 1.40 (uniform load, vertical deflection, as DG34 uses it).

Office simple-beam forms:
- DG34 Eq. 10-1, US units: Δ (in.) = w L⁴ / (1,290 I), with w in kip/ft, L in ft, I in in⁴.
- SI: Δ = 5 w L⁴ / (384 E I).
- To size by stiffness, rearrange for I_req = w L⁴ / (1,290 Δ_allow).

## Vibration [DG]

- Long spans, light stairs and **monumental (feature) stairs** are prone to footfall vibration.
- Evaluate them to **AISC Design Guide 11** (2nd ed., 2016), which has a stair chapter.
- Industrial or service stairs of normal span rarely need a check, but a lively stair is a common complaint.

## Long-span stairs [DG]

- Add **plan bracing at the stringer bottom flanges** to stiffen against sideways sway from walking.
- **Camber** the stringers for dead-load deflection where it helps the profile and the handrail line.
- Check vibration (above).
- Check that the stair does not move enough to hurt the fit at the landings or the finishes.

## Other movement checks [DG]

- **Hanger-supported landings on rods or cables:** add lateral restraint so the landing does not swing under foot traffic.
- **Lateral sway under seismic Fp:** about span/50 to span/100 (04B).
- **Rain on long landings:** check that beam deflection does not exceed the drainage slope (03).

## Office note [REC]

- Put the deflection limits in the stair general notes, and in the delegated-design criteria if delegated (14).
- In the calculation, report deflection with FΔ applied, and the governing limit.
- For a feature stair, record the vibration check and its criterion in the design basis.
