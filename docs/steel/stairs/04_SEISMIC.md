# 04 Seismic force on stairs (DG34 §3.2.5)

Most stairs are **not** part of the seismic force-resisting system (SFRS). Design them as **nonstructural components** to ASCE/SEI 7-16 Ch. 13. A freestanding stair tower is designed to Ch. 12 or Ch. 15 instead, outside DG34.

Drift between floors and sliding connections → `04B_SEISMIC_DRIFT.md`.

## Horizontal force [CODE]

**Fp = 0.4 ap SDS Wp (1 + 2 z/h) / (Rp / Ip)**, ASCE 7 Eq. 13.3-1

- z/h ≤ 1.0; z = 0 at or below the base.
- Apply at the **centre of gravity**, in **two orthogonal horizontal directions**, each taken separately.
- **Bounds:** 0.3 SDS Ip Wp ≤ Fp ≤ 1.6 SDS Ip Wp.
- **Concurrent vertical force:** Fpv = ± 0.2 SDS Wp.
- **Ip = 1.5:** egress stairs must remain usable after an earthquake (§13.1.3).
- **ρ = 1.0** for stair members. The building SFRS Ωo does **not** apply to them.

## Coefficients (ASCE 7 Table 13.5-1 as given by DG34) [CODE]

| Item | ap | Rp | Ωo for anchorage to concrete or masonry |
|---|---|---|---|
| Egress stair, not part of the SFRS: stringers, beams, posts, landings, connection plates | 1 | 2.5 | **2**: applied in the design of the supporting concrete or masonry member |
| Fasteners and attachments: bolts, welds, dowels | 2.5 | 2.5 | **2.5**: embeds, studs, cast-in and post-installed anchors |

## Anchorage [CODE]

- Design to ASCE 7 §13.4 plus **ACI 318** (concrete) or **TMS 402** (masonry).
- Anchors must be **prequalified for seismic use** (ACI 355.2).
- Redundancy and overstrength for the anchorage differ from those for the stair members. Keep two sets of combinations: one for the members, one with Ωo for the anchorage.

## Worked values: DG34 Ex. 10.2 (industrial stair, southern California) [DG]

- SDS = 0.66g; attachment at z = 9.92 ft; roof h = 19.8 ft; ap = 1; Rp = 2.5; Ip = 1.5.
- **Fp = 0.317 Wp**, within 0.297 Wp – 1.58 Wp. Fpv = ± 0.132 Wp.
- Member combinations (LRFD), with Ev = 0.2 SDS D = 0.132 D:
  - 1.33D + 1.0QE + L + 0.2S;
  - 0.768D + 1.0QE.
- Anchorage combinations use Ωo = 2.5: 1.33D + 2.5QE + L + 0.2S, and so on.
- Result: the HSS12×2×¼ stringer under weak-axis seismic + gravity had **interaction 0.12**. Seismic **force** rarely governs members; **drift** and **anchorage** do.

## Design sequence [REC]

1. Get **SDS** and the SDC, and the attachment heights, from the SER or the building model.
2. Wp = the dead load of the flight or landing, with its share of the guard.
3. Compute Fp and check it against the bounds. Add Fpv.
4. Check the members: Fp in both directions, combined with gravity (10 for the load path).
5. Check the connections with the attachment coefficients (ap 2.5).
6. Check the anchors and embeds with Ωo.
7. Then accommodate drift (04B).

## Office note [REC]

For Thai projects, take the seismic parameters from **DPT 1301/1302** (the SER's design basis). Map its nonstructural-component provisions onto the method above, and record the mapping in the calculation.
