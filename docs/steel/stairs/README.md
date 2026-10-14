# Steel-framed stairways: router

Study notes on **AISC Design Guide 34, *Steel-Framed Stairway Design*** (Adam D. Friedman, AISC 2018; 114 pages). They cover egress, service, commercial and industrial steel stairs: layout, loads, members, connections, guards, tolerances and delegated design.

**Source file:** `G:\My Drive\##Textbook\AISC Design Guide\DG34.pdf`, outside the repository. Section numbers below (§) are DG34's.

## How to use

- Each file is one topic and at most 500 words. Read this router, then only the files your task needs.
- The values are US codes (IBC 2015, OSHA 1910 Subpart D, ASCE/SEI 7-16, AISC 360-16), with SI in brackets.
- **On a Thai project, egress geometry comes from Thai law** (กฎกระทรวง / fire code) and the architect. The structural method, the checks and the detailing advice transfer directly.
- Tags:
  - **[DG]** the guide's rule or recommendation;
  - **[CODE]** a US code value quoted by the guide;
  - **[REC]** an office note added here.

## Files

| # | File | Read it for |
|---|---|---|
| 01 | `01_SCOPE_ROLES_PITFALLS.md` | Roles (architect, SER, SSE, fabricator), the five recurring problems, what a stair design must settle early |
| 02 | `02_TYPES_CLASSES_TERMS.md` | Stair types, the four classes (industrial → architectural), names of the parts |
| 03 | `03_LOADS.md` | Dead and live loads (IBC / OSHA / ASTM E985), not-concurrent cases, unbalanced patterns |
| 03B | `03B_LOADS_OTHER.md` | Wind, snow, rain and ice on exterior stairs; thermal (guard runs); integrity and notional loads |
| 04 | `04_SEISMIC.md` | Fp for stairs as nonstructural components, coefficients, anchorage Ωo, worked values |
| 04B | `04B_SEISMIC_DRIFT.md` | Drift between floors (Dp), sliding or rotation details, when the stair must be modelled |
| 05 | `05_SERVICEABILITY.md` | Deflection limits, vibration, long spans, camber |
| 06 | `06_LAYOUT_GEOMETRY.md` | Code geometry: widths, risers, treads, headroom, landings, guards, handrails |
| 07 | `07_OPENING_SIZE.md` | Sizing the floor opening (Wopen, Lopen), gaps, coordination |
| 08 | `08_TREADS_LANDINGS.md` | Tread and riser types and connections, landing construction and support |
| 09 | `09_STRINGER_DESIGN.md` | Stringer types, sloping vs horizontal-plane method, deflection factor, support model, bracing |
| 10 | `10_LATERAL_BRACING.md` | Lateral load path: flight assembly, landing diaphragms, braces, moment frames |
| 11 | `11_CONNECTIONS.md` | Steel-to-steel connections, slab-edge angle, erection aids, kinked stringers |
| 11B | `11B_CONNECTIONS_CONCRETE_MASONRY.md` | Embeds, beam pockets, post-installed anchors, thickened slab, grouted cores |
| 12 | `12_GUARDS_HANDRAILS.md` | Guard and handrail members and parts, infill openings, toe plate |
| 12B | `12B_GUARD_CONNECTIONS.md` | Rail joints, brackets, post-to-stringer, channel flange check (Eq. 7-1), walls |
| 13 | `13_TOLERANCES_FINISHES.md` | Steel, concrete and masonry tolerances, galvanizing, AESS, erection |
| 14 | `14_DELEGATED_DESIGN.md` | Who provides what, submittals, the Appendix A checklists |
| 15 | `15_DESIGN_WORKFLOW_EXAMPLES.md` | Step-by-step design order and the results of DG34's two worked examples |
| 16 | `16_DRAWING_CHECKLIST.md` | [REC] What our steel-stair drawings must show, using the rule book |

## Quick answers

| Question | Go to |
|---|---|
| How big must the stair opening be? | 07 |
| Live load on a tread? On a guard? | 03 (exterior loads: 03B) |
| Deflection limit for a stringer or guard post? | 05 |
| Can the treads brace the stringer? | 09 §4.4 note |
| Stair in a seismic zone: fixed or sliding? | 04, 04B |
| Channel stringer under a guard post: does it need a stiffener? | 12B |
| What gap to leave against a concrete or masonry wall? | 07, 13; anchors and embeds: 11B |
| What must the architect or SER put on the drawings? | 14 |

## Related rule-book files

- `docs/steel/STEEL_DETAILING_INSTRUCTION.md`: welds, bolts, marks and bills for any steel set.
- `docs/concrete/STAIRCASE_DRAWING_INSTRUCTION.md`: RC stairs (the ST-1 job), for presentation conventions.
- `docs/general/ANNOTATION_ALIGNMENT_GUIDE.md`: notes, leaders and units on the drawings.
