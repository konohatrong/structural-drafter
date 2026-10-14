# 01 Scope, behaviour and code changes (DG1 §1, §3 intro)

Base plates and anchor rods are often the **last steel items designed and the first needed on site**. Accurate anchor rod placement is one of the keys to erecting and plumbing the frame safely. Design for constructability, not only strength.

## Components [DG Fig. 1.1]

Column, base plate, column-to-plate weld, anchor rods with washers and nuts, grout bed, concrete footing or pier. Shear lugs, plate washers and stools are added where needed.

## Load cases [DG §3]

| Case | Section | Note file |
|---|---|---|
| Concentric compression | 3.1 | 09 |
| Uplift (tension) | 3.2 | 10, 11 |
| Small moment (no rod tension) | 3.3 | 12 |
| Large moment (rods in tension) | 3.4 | 13 |
| Shear | 3.5 | 14, 15 |

Shear and moment are usually designed **independently**, assuming no significant interaction.

## Behaviour [DG]

- The base stays elastic until one of these happens: a hinge in the column, a mechanism in the plate, concrete crushing, rod yielding in tension, or **concrete pullout or breakout of the rod group**.
- If the concrete strength exceeds the lowest steel limit state, the behaviour is **ductile**.
- For static loads with ample strength, a concrete limit state may govern.
- For **seismic** frames the concrete limit states should **not** govern (08).
- Most building columns carry compression only. Their rods are needed for **erection stability**, not for the permanent structure.

## Analysis model [DG]

- Bases are modelled pinned or fixed. A wrong stiffness distorts drift:
  - stiffness overestimated → **unrecognised second-order moments**;
  - stiffness underestimated → **oversized first-storey columns**.
- Where accuracy matters, model the base rotational stiffness (and, for seismic, its cyclic behaviour).

## OSHA Subpart R [CODE]

- **At least four anchor rods** per column, except posts under 300 lb (1.3 kN).
- Column, base and foundation must resist **300 lb (1.3 kN) at 18 in. (450 mm) from the outer face** of the column, in each direction.
- Four ¾ in. rods at a 4 in. square easily meet it: 306 kip-in. available against 12.0 kip-in. required for a 14 in. deep column.

## Code changes since 2006 [REC: verify before use]

| DG1 (2006) | Current practice |
|---|---|
| ACI 318-02 **Appendix D** | ACI 318 **Chapter 17** (since 318-14); the equations keep their form, but modifiers are renamed (ψ3 → ψc,N, ψ4 → ψc,P) and φ depends on supplementary reinforcement |
| AISC J8 bearing φ = 0.60; DG1 uses ACI's 0.65 | AISC 360-10 onward: **φ = 0.65, Ω = 2.31**, so the conflict DG1 notes is gone |
| Threaded rod shear Fnv = 0.40Fu (N) / 0.50Fu (X) | AISC 360-16: **0.450Fu / 0.563Fu** |
| AISC Seismic Provisions 2005 §8.5 | AISC 341 current edition |
| — | A newer edition of DG1 has been published; use it when available |

Thai projects: concrete anchorage to the current ACI 318 as adopted by EIT standards; loads to the Thai ministerial regulation and DPT 1311 (wind) and DPT 1301/1302 (seismic).

## Office note [REC]

State in the design basis whether each base is **pinned or fixed**, and check that the base detail, rod layout and foundation match that assumption.
