# 04B Drift between floors and seismic slip connections (DG34 §3.3.2, §6.4)

A stair ties two floors that sway differently.

- **Parallel to the stringers**, the drift pushes or pulls axial force through the flight.
- **Across them**, it causes weak-axis bending, shear and **torsion at the end connections**.

Either the stair is detailed to move, or it is modelled as part of the building.

## Displacement to accommodate [CODE]

- **Dp I = Dp Ie** (ASCE 7 Eq. 13.3-6), with **Dp = δxA − δyA**: the elastic-amplified deflections of the two attachment levels (§12.8.6, Eq. 12.8-15).
- Linear dynamic analysis (§12.9) may be used instead.
- **The SER must supply δx or Dp to a delegated stair designer.**
- Dp need not exceed **(hx − hy) ΔaA / hsx**, the allowable-drift bound. [DG] Using it as the design value is safe for delegated design but makes costly connections.

## Three accepted ways (ASCE 7 §13.5.10) [CODE]

| Option | Movement to accommodate | Conditions |
|---|---|---|
| **(a) Sliding with a secured element**: slotted or oversized holes with a keeper or end stop, or deforming metal attachments | **Dp I, at least ½ in. (13 mm)** in any horizontal direction | Vertical support kept, after the event too; **no compression forced into the stair** |
| **(b) Sliding without a secured element** | **1.5 Dp I, at least 1 in. (25 mm)** | Vertical support kept |
| **(c) Supports with rotation capacity** (connections or frames) | **1.5 Dp I, at least 1 in.** | Vertical support kept; **no brittle failure mode** (bolt shear, weld rupture) may govern |

All fasteners and attachments are still designed for the §13.3.1 forces with the Table 13.5-1 coefficients (04).

## If the stair is not isolated [CODE]

- **Include it in the building model** (§12.7.3) with its real stiffness and strength.
- Design its members with the **SFRS Ωo, not less than 2.5**.
- Expect forces from the building to flow through the stair; analyse and detail with care.

## Stair sway check [DG]

Under Fp at the centre of gravity, check the stair's own lateral displacement. Allowable drift from ASCE 7 Table 12.12-1 ("all other structures") works out to about **span/50 – span/100**, depending on risk category.

## Typical details (DG34 Figs 6-18 to 6-20) [DG]

- **Stringer foot sliding on a slab on grade or slab on deck:** a bearing plate with an **oversized or slotted hole**, the anchor trapped by a keeper plate. Versions without the keeper are possible (option b).
- **Fixed landing + sliding flight**, with an **expansion joint and cover plate** at the gap.
- **The usual pattern:** fix one end, let the other slide, and make the slot ≥ the required movement in both directions.

## On the drawings [REC]

- State **Dp I** and the required movement: ½ in. / 1 in. minimum, or 1.5 Dp I.
- Mark the **fixed** and **sliding** ends on plan and section.
- Dimension the **slot length and direction**. Show the keeper plate, low-friction pad or bearing finish, and "NO FIELD WELD / NO GROUT AT SLIDING END".
- The lateral path must pass through the fixed end only (10).
- Get δx from the MIDAS model storey drifts (`midas/`) and cite them in the calculation.
