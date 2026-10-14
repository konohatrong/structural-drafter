# 15 Design workflow and worked examples (DG34 Ch. 10)

**DG34's caution:** members are often chosen for architecture, fabrication and erection, not strength. Pick them for those reasons, then verify them.

## Workflow [DG order]

1. **Criteria:** code, occupancy, class, geometry (06), loads (03, 03B, 04), deflection limits (05).
2. **Opening:** W_open × L_open (07), agreed with the architect and SER.
3. **Treads:** uniform load or point load, not concurrent (08).
4. **Stringers:** horizontal-plane loads, simple span, unbraced length, deflection with FΔ (09).
5. **Landing beams:** header beam (the stringer reactions) and rear beam.
6. **Landing posts and hangers**, with the fit-up minimum sizes (08).
7. **Guards and handrails:** rails, posts, infill, brackets (12).
8. **Local checks:** post on flange (12B), kink joint (11).
9. **Lateral:** flight, diaphragm or bracing; drift isolation (10, 04B).
10. **Connections and anchorage**, with Ωo where seismic (11, 11B).
11. **Non-steel checks** (DG34 §10.3):
    - pans to AISI S100 and AWS D1.3;
    - deck and slab to SDI and ACI 318;
    - embeds and anchors to ACI 318 and their evaluation reports;
    - brackets by ASTM testing.

## Ex. 10.1: commercial stair, office, IBC, gravity only [DG]

**Criteria:** 44 in. egress; risers 7 in., treads 11 in.; filled pans with closed risers; A36 channels; A500 Gr C round HSS guards. Loads: stair DL 35 psf, landing DL 37 psf; LL 100 psf or 300 lb; guard 50 plf or 200 lb.

| Element | Result |
|---|---|
| Opening | 8 ft 11 in. × 13 ft 7½ in. (2.72 × 4.15 m) |
| Stringer (9 ft 8 in., braced by the welded pans) | **C12×20.7**: Mu 4.96 vs φMn 69.1 kip-ft; Δ_LL 0.014 in. (with FΔ 1.40) vs 0.32 in. Size set by depth, not strength |
| Header beam | **C10×15.3**: Mu 13.4 vs 42.9 kip-ft |
| Rear beam | C10×15.3 |
| Post (≈ 6.5 ft) | **HSS3×3×³⁄₁₆**: 5.8 vs 60.4 kips |
| Hanger | **L3×3×³⁄₁₆**: 1.7 vs 35 kips |
| Guard | HSS1.900×0.145 rails and posts, HSS1.660×0.140 handrail, ½ in. bar pickets. Post 1.12 vs 1.45 kip-ft |
| Post on channel | 13.4 vs 13.5 kip-in. OK |

## Ex. 10.2: industrial stair, warehouse, OSHA, SDS 0.66 [DG]

**Criteria:** 36 in. wide; open risers; ³⁄₁₆ in. checkered plate; A500 Gr C rectangular HSS; A53 pipe guards. LL **60 psf or 1,000 lb**. Platform at 9 ft 11 in.

| Element | Result |
|---|---|
| Seismic | Fp 0.317 Wp; Fpv ± 0.132 Wp; anchorage Ωo 2.5 |
| Tread | Bent plate, 3 ft span: adequate (A786 Fy ≈ 26.7 ksi assumed; verify) |
| Stringer (14 ft 8 in.) | **HSS12×2×¼**: 5.89 vs 75.4 kip-ft; seismic interaction **0.12** |

**Lesson:** at normal spans strength rarely governs. The work is in **deflection, local checks, fit-up sizes, the lateral path and drift**.

## Office template [REC]

Write one `calc_stair.py` per stair, in this order. It is the single source for the member sizes and drawing schedules (AGENTS.md §2, "data first").
