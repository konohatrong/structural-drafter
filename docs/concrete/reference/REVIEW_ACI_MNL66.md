# Review of the office standard set against ACI Detailing Manual MNL-66(20)

**Date:** 2026-09-29.

**Material:** the manual and its 137 supplemental DWGs, converted and indexed in `references/aci_mnl66/` (see the README there). Four parallel reviews compared ACI's details and design-professional checklists with our sheets:
- beams;
- columns;
- slabs and slab on ground;
- walls, foundations and general notes.

The main claims were checked against our source digests and by eye before anything changed.

**Basis:** our codes stay EIT 011008-21 (ACI 318-11 based), DPT 1301/1302-61 and the TATA handbook. ACI 318-19 is used where it states good practice that is code-independent, or as an explicitly labelled office rule. US bar sizes and imperial values are not adopted.

---

## 1. Changed now

| Sheet / detail | Finding | Change |
|---|---|---|
| 1102/9 (c), 12 bars | Two adjacent side bars unsupported, against EIT 7.10.5.3 (corner and alternate bar). The caption said "overlapping ties" | Outer tie + 2 crossties; caption corrected |
| 1102/1 – 4, size change | "≤ 75" crank, but ≥ 75 needs separate dowels (EIT 7.8.1.5) | Labels "< 75" / "≥ 75" |
| 1102/2, 4 | Terminated lower bars were straight; a "bend" tie note appeared where there is no bend | 90° hook inward drawn and noted; the bend-tie note appears only on the cranked details |
| 1102/6, starter bars | Hooks outward everywhere; no compression embedment | Hooks toward the centre in special frames fixed at the base (ACI 318-11 21.12.2.2); straight ≥ ldc; hoops through the full footing depth at an edge within h/2 |
| 1102/7, roof | "Hook OR ldh" read as a choice | Hook AND ≥ ldh above the soffit |
| 1101 joint note | Tie stop point wording | "Lowest bars of the shallowest beam" |
| 1101 notes | Tie-size note contradicted itself | Office minimum RB9 / DB10 vs the code minimum; corner / alternate / 150 lateral-support rule stated |
| 1101 notes | Couplers and laps too thin | Laps that don't fit the zone, or ρ > 4 %: couplers or laps staggered to alternate floors; a tie above and below each coupler; Type 2 couplers within lo in special frames |
| 1101 notes | Spiral note too thin | Laps 48 db (DB) / 72 db (RB); termination without beams on all sides |
| 1111 note 3 | Perimeter integrity understated | Continuous top ≥ 1/6 of the support top steel and bottom ≥ 1/4 of the midspan steel, Class B, laps placed correctly; closed stirrups over the whole span; bars inside the column core (EIT 7.13.2) |
| 1111 note 5 | Lateral support in special-frame hoop zones not stated | Corner and alternate bars held, ≤ 150 clear (DPT 5.2.8.3.3 → EIT 7.10.5.3) |
| 1111 note 6 | Torsion rules incomplete | Stirrups continued bt + d beyond the point needed; longitudinal torsion bars developed at both ends (EIT 11.5) |
| 1111 note 7 | Side bars "over the tension half" at @ ≤ 300 | Both faces over the full web (the tension face changes along a continuous beam), @ ≤ 250, first bar ≤ 150 below the slab |
| 1111/4 (b) | U-stirrup + cap tie had no limits | "Not for torsion beams" |
| 1112/1 | "≥ 1/4 of the bottom bars into every support" | 1/4, or 1/3 at a simple support (EIT 12.11.1) |
| 1114/2, stepped beam | "≥ 35 db, Ld" for bars past the step | ≥ 1.3 Ld (Class B: non-contact lap) |
| 1126/1, /2, slab steps | Lower bottom bars bent round the re-entrant soffit corner (ACI SLAB-204; also our own rule) | Taken straight up to the upper-slab TOP layer, then Ld (TATA H < T pattern, stair-knee practice). The upper bottom bars cross the corner |
| 1127/4, /5, slab-on-ground dowels | Deformed DB25 dowels lock the joint | Plain dowels RB19 × 400 (t ≤ 150), RB25 × 450 (t ≤ 200), half greased / sleeved @ 300; drawing updated |
| 1127/3 | Mesh "continuous or stopped" | Stopped 50 each side by default; continuous only if designed |
| 1127/5 | Expansion and isolation joints shared one detail | "EXPANSION JOINT"; isolation joint = same filler and sealant, no dowels |
| 1121/3, cantilever | Back length not tied to the cantilever | ≥ Ld, ≥ Lc and ≥ Sn/3 |
| 1121 notes | Hook-fit and free-edge rules missing | Hook fit (≈ 16 db; else a 180° hook or edge U-bars); free edges ≥ 2-DB12 top and bottom |
| 1123 table, notes | Two-way spacing had no cap | ≤ 2h **and 450** (ACI 318-19 cap adopted as an office rule, conservative) |
| 1125/1, /2, openings | Cut bars not replaced below 600; diagonals too short | ≤ 300 re-spaced; 300 – 600 cut area replaced half each side (≥ 1-DB12); diagonals DB12 × 1200 (was 700 / 1000); cut top bars end in a standard hook |
| 1001 Table 1 | Design data incomplete | Placeholders for site class, S<sub>DS</sub>/S<sub>D1</sub>, analysis method, seismic-system members, live loads, superimposed dead load, partitions, live-load reduction and special loads |
| 1002 Table 6 | Only laps and ldh | Straight tension ld and compression ldc rows; applicability note (higher grades; cover / spacing conditions) |
| 1001 note 5.6 | Bar supports and bar dimensions not covered | Footing and ground-beam blocks; top-mat chairs by the contractor (engineer-designed ≥ 1.2 m); bar dimensions out-to-out including hooks |
| 1002 note 6.1, lap detail | Blanket "stagger all laps" | U.N.O. (column / wall verticals may lap at one level per their details) |
| 1002 notes 8.5, 11.5 | Anchor bolts and joints not covered | Anchor bolts and non-shrink grout; joint-layout submittal where joints are not shown |
| 1003 section 14 | No foundation notes | New: foundations and piles (soil report, bearing / piles, pile tests, tolerances, cut-off and embedment, lean concrete, dewatering, fill), as placeholders |

**Engine:** `notes_block` now warns when a block runs below the frame. The warning caught the column notes, which were widened to fit.

---

## 2. Design-policy decisions

**Decided by the user (2026-09-29) and applied:**
- **D1, special-frame beam hoops:** the stricter of DPT and ACI, s1 ≤ min(d/4, 6 db, 24 dt, 150), with both sources cited. Applied to 1111/3, the 1112 table and 1111 note 5.
- **D2, intermediate-frame hooks:** the DPT rule is kept (90° + 6 db; 135° or hook-clip for public / ductile buildings). The 1112 table notes "ACI 318: HOOPS".
- **D3, hoops and crossties:** DB10 minimum, deformed, in intermediate and special frames; RB9 stays for ordinary frames. Applied to 1101 note 2, 1111 note 5 and the 1002 Table 5 note.
- **D4, laps at a floor:** the lower bars are cranked inside the joint, with the top bend ≤ 75 below the slab top, so the lapped bars run straight. 1101/1 redrawn; 1101 note 3 updated. This matches 1102/1.
- **D5, ACI 318-19 high-axial rule (2026-09-30, option B):** not a blanket office rule. 1103 note 6 applies it where the design uses ACI 318-19 18.7.5.2(f) (special frames, Pu > 0.3 Ag f'c or f'c > 70 MPa): every perimeter bar held by a hoop corner or a crosstie with 135° hooks at both ends, hx ≤ 200. Tie **type EH** (12 bars, all held) is drawn on 1103/1; the column schedule marks these columns. Otherwise EIT 011008 (notes 1 – 2) governs.

To keep the sheets clear, notes 6 and 7 of 1111 (edge / torsion beams, side-face bars) moved to 1113 notes 6 – 7. 1113 no longer repeats the bar-end key; it is on 1112 and 1114.

### Original decision table

| # | Item | Options |
|---|---|---|
| D1 | Special-frame beam hoop spacing in 2h | DPT 5.2.8.3.2 prints d/4, **8 db, 24 dt, 300** (verified on the page image). ACI 318-11 21.5.3.2 onward prints d/4, **6 db, 150**. Our rule "draw the stricter" argues for min(DPT, ACI) |
| D2 | Intermediate-frame 2h zone hooks | DPT 5.2.7.6 allows 90° + 6 db (135° / hook-clip only for public or ductile buildings). ACI 318-11 21.3.4.2 requires hoops in every intermediate frame |
| D3 | Tie material | ACI allows plain bars only for spirals. Keep RB9 ties, or DB10 minimum for intermediate / special hoops and crossties |
| D4 | Column offset bend position | Ours (1101/1 – 2): upper bars cranked above the floor lap. ACI and 1102/1: lower bars cranked inside the joint, top bend ≤ 75 below the slab top. The set should use one rule |
| D5 | ACI 318-19 high-axial rule | Pu > 0.3 Ag f'c: every perimeter bar supported, hx ≤ 200. Adopt as an office rule for special columns? |

---

## 3. Proposed next work (larger additions)

- **Schedules:**
  - ~~beam schedule and keyed placing diagram (lettered bars)~~ — **done 2026-09-30: 1115** (ACI BM-1 format, letters A – E / SB / S1 – S2 keyed to 1112/1);
  - column schedule template: COL-1;
  - one-way / two-way slab schedules with lettered bars on 1122: SLAB-1 / 2.x;
  - stud-rail schedule: MNL Fig 4.10.1.
- **New typical details:**
  - ~~secondary beam ending at a girder or spandrel~~ — **done 2026-09-30: 1114/3** (BM-204; TATA p.180 case 3);
  - large beam step: BM-206;
  - ~~column supporting a discontinued wall~~ — **done 2026-09-30: 1102/9** (COL-104; DPT 5.2.9.4.5);
  - ~~a tie-type sheet 1103~~ — **done 2026-09-29** (see §4);
  - dropped balcony / wet-area slab with drip and falls: SLAB-100 / 207;
  - slab at an RC wall;
  - corner-panel bar options: SLAB-200 / 201;
  - support-bar and chair sketch;
  - sloped slab / ramp;
  - stud rails at edge and corner columns;
  - slab-on-ground re-entrant and T-joint bars, bars at column-diamond corners, thickened slab under walls, depressions and pits, vapour retarder.
- **Presentation:**
  - bar letters on the typical elevations and strip diagrams;
  - sections in the end zone and middle zone on 1111;
  - dimensioned first hoop 50, embedment 150, lap zones and "0 TYP";
  - zone / s/2 dimensions on the column elevations;
  - a graphic legend in the general notes.
- **Walls 113x:**
  1. 1131 schedule and typical wall (ρ<sub>v</sub> 0.0015 / ρ<sub>h</sub> 0.0025 for SD40, two curtains above 250 mm);
  2. 1132 connections (footing, slab, roof, thickness change, waterstop);
  3. 1133 corners, intersections and openings;
  4. 1134 joints and embeds;
  5. 1135 cantilever retaining wall (from nooker_rw);
  6. 1136 boundary elements and coupling beams.
- **Foundations 114x:**
  1. 1141 footing schedule, isolated / combined / strap footings (L1, L2 checks, band γ<sub>s</sub>);
  2. 1142 pile caps with 1 – 6 piles (Thai pile types, head cut-off and anchorage);
  3. 1143 ground / tie beams (EIT 21.12.3);
  4. 1144 mat and pits;
  5. 1145 pedestals, anchor bolts, pipes, slab-on-ground dowels.

**Not applicable (US-specific):**
- imperial bar sizes and dimensions;
- SDC letters (map to DPT);
- Grade 80 rules and ASTM / AWS references;
- frost, CMU / brick / precast / stud details;
- expansive-soil carton forms (the Bangkok-clay equivalent is fill settling away from pile-supported slabs and beams).

---

## 4. Done after the review

**STR-ST-1103, tie types and splices (2026-09-29).**
- **Tie types A – J** for 4 – 24 bars: a perimeter tie plus crossties on alternate intermediate bars.
- **Details:** a circular hoop (overlap ≥ 150, hooks round a bar, overlaps staggered); a spiral column (pitch, 1.5 extra turns, laps 48 / 72 db); mechanical splices (Type 1 / 2, staggered ≥ 600, a tie above and below, cover to the coupler).
- **Tables:** maximum tie spacing by bar and tie size for the ordinary, intermediate lo and special lo zones, with DB10 hoops per D3 and special = min(6 db, 150); a schedule call-up example.
- **Notes to 1103.**

The old tie arrangements (1102/9) were removed, so there is one place to maintain. 1101 note 1 points to 1103.

**Engine:** `tbl` now warns when a table runs into the title strip.

---

## 5. Lessons from this review

- **Verify before changing.** Every agent claim was checked against our digests or the drawing. Most held; the MNL-66 BM-104 checklist itself prints outdated special-frame values.
- **Code lineage matters.** EIT 011008 = ACI 318-11, DPT 1301/1302-61 = its own values, MNL-66 = ACI 318-19. A difference between them is a decision for the user (D1 – D5), not a silent edit.
- **The biggest findings were geometric, not numeric:**
  - unsupported bars in a tie arrangement;
  - tension bars bent round a re-entrant corner;
  - deformed dowels at a slab-on-ground joint.

  Review drawings for load path and bar behaviour, not only for values.
- **One place per rule.** The tie arrangements moved to 1103, the bar-end key is on 1112 and 1114 only, and general-note rules carry "U.N.O." where a detail departs from them.
- **Text changes ripple.** Adding notes pushed notes blocks, tables and title notes off several sheets. The engine now warns for notes blocks and tables as well as views and titles.
