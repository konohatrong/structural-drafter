# 16 Steel stair drawings: what the set must show [REC]

This applies DG34's design advice to our drawings. DG34 is a design guide, not a drafting standard. The steel rules (S1 – S11) and the annotation guide govern presentation.

## Sheets [REC]

| Sheet | Content | Scale (steel S2) |
|---|---|---|
| Stair plan at every level | Opening outline with **W_open × L_open** (07); flights with UP arrows, tread count and numbering; landing framing; support beams, posts and hangers; slab-edge angles; guard lines; marks | 1:50 |
| Stair sections and elevations | Floor and landing levels; **rise × going per flight** (e.g. "11 R @ 178 = 1,960"); headroom; guard and handrail heights from the nosing line; supports | 1:50 or 1:20 |
| Stringer elevation per type | Kink, tread and riser positions, carrier angles or pan welds, guard post positions, end connections, camber | 1:20 |
| Details | Stringer end connections (fixed and sliding), kink joint, tread connections, landing beam to wall (embed, pocket, anchors), post-to-stringer with stiffener (12B), handrail bracket, slab-edge angle with adjustment | 1:5 – 1:10 |
| Guard and handrail elevation | Post spacing, rails, infill spacing, opening limits, extensions, toe plate | 1:20 |
| Schedules and notes | Member schedule with weights (S3); bolts (S8); **TABLE n - STAIR DESIGN CRITERIA** (14); loads; deflection limits; tolerances; finishes | – |

## Notes the set must carry [REC]

1. **Governing code** for the geometry (Thai law and the architect) and for the loads. Live loads with **"NOT CONCURRENT"** where that applies (03).
2. **Deflection limits:** L/360 live, L/240 total, guard post h/60, rails L/120 (05).
3. **Seismic:** Ip, Fp basis, **Dp and the slot length**, which end is **fixed** and which **slides**, "NO FIELD WELD AT SLIDING END" (04, 04B).
4. **Tread type** and whether the treads brace the stringers. With bolted grating, the stringers are designed as unbraced (09).
5. **Tolerances and gaps:** ¼ – ½ in. (6 – 13 mm) to walls; "VERIFY OPENING ON SITE BEFORE FABRICATION"; riser uniformity ⅜ in. (10 mm) (13).
6. **Material grades:** stringers (A36 / SS400 or HSS grade), round HSS rails (A500 Gr C or equivalent), checkered plate (verify the yield), anchors (approved, seismic-rated where required).
7. **Finish:** class (02), galvanizing (vent holes, no field welds), AESS category if any.
8. **Delegated items**, if any: what is delegated, the criteria (14), the submittal content, and the review responsibility.

## Presentation reminders from the rule book [REC]

- Every dimension has its unit in notes; dimension figures stay bare (guide §2.4.2).
- Members are tagged with marks in circles; piece marks are generated from the calc (S3).
- Every weld has an AWS symbol and every bolt is in the bolt table (S5, S8). No weld information in leaders.
- Concrete supports are hatched as background (`AR-CONC`); the stair steel is drawn full weight (S4.6).
- Tables are numbered "TABLE n - NAME" and cited by number (`DRAWING_PRODUCTION.md` §2).
- Before issue: steel S10, guide §8, and the RC stair checklist (`STAIRCASE_DRAWING_INSTRUCTION.md` §11) for the items shared with stairs (rise and going consistency, headroom, nosing line).

## Data flow [REC]

All sizes, rises, goings, opening dimensions, loads and drifts come from one `calc_stair.py` (15). The drawing script reads it and never retypes a number.
