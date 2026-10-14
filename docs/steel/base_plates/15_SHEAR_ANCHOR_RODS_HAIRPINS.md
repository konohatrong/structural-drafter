# 15 Shear in anchor rods, hairpins and tie rods (DG1 §3.5.3 – §3.5.5)

## Getting the shear into the rods [DG]

- With Table 2.3 holes the plate **slips** up to ¾ in. (19 mm) before bearing, and the rods **do not share equally**.
- **Cautious approach: only two rods carry the shear**, unless the load is equalised.
- To share it equally:
  - **plate washers welded to the base plate**, with holes **1/16 in. (2 mm) over the rod**;
  - or a **setting plate** of suitable thickness, field-welded to the base plate after erection.
- [REC] This matches steel S8.4: welded washers at the pin end, loose washers at a sliding end.

## Rod bending [DG]

- With welded washers, the rods **bend within the plate thickness**. Lever arm = **half the distance from the washer bearing centre to the top of the grout**, reverse curvature.
- With only two rods bearing on the hole edge, the shear stays within the plate: **neglect rod bending**.
- No bending within the grout (shear friction).
- **Built-up grout pad:** ACI 318-02 multiplies anchor shear by **0.8**. The authors skip it when the AISC combined bending, shear and tension check is made and the rod ends up at least 20 % larger. Example 4.11 uses a **1.25 multiplier on the shear** instead.

## Rod steel strength [CODE + DG]

- Nominal 0.40 Fu Ab with threads in the shear plane, 0.50 Fu Ab with threads excluded. Combine with tension by AISC J3.7: F′nt = 1.3 Fnt − (Fnt / φFnv) fv ≤ Fnt.
- [REC] Two misprints in §3.5.3:
  - it attaches 0.4 to "threads not excluded" and 0.5 to "threads included"; the 0.4 – included, 0.5 – excluded pairing is correct;
  - it gives φ = 0.55, Ω = 2.75, while Examples 4.10 and 4.11 use **φ = 0.75**. Use the current AISC 360 values (01).

## Concrete breakout in shear [CODE]

- Cone towards the edge in the direction of load, distance c1 (Fig. 3.5.2). A_vo = **4.5 c1²**; A_v = projected area of the group.
- Simplified for cast-in rods: **φVcbg = 10.4 ψ6 (A_v / A_vo) √do √f′c c1^1.5** (lb, in., psi), with φ 0.70, ψ7 1.4 and ℓ/do = 8 built in. **do ≤ 1.25 in.** in the root term.
- Check breakout from the **back rods** (with the front rods carrying the same share) and from the **front rods** carrying all the shear (Fig. 3.5.3).
- **Pryout** rarely governs; tension-shear interaction per ACI.
- Short edge distances need **reinforcement**. **Ties at the pier top** (ACI 318 7.10.5.6) can carry the shear.
- Example 4.10: four ¾ in. rods at 4 in. → 30.8 kips; needs **c1 ≈ 14 in. (355 mm)** in plain 4 ksi concrete.

## Hairpins and tie rods [DG]

- **Hairpins** move the shear by bearing into the **floor slab**, which uses its friction on the subgrade.
  - Avoid eccentricity and rod bending (Fig. 3.5.5), or use lugs.
  - Plan slab **joints** so the load path is not cut, while letting the slab move.
  - **No vapour barrier** under that slab.
- **Tie rods** through the slab to the opposite column take rigid-frame thrust: allow for their **elongation**; remove **sag** before casting.
- Place both **as close to the slab top** as cover allows.
