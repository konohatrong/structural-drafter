# 18 Fixed steel ladders: content, limits, drawing [REC]

**Reference set:** Beca SE-0504 (standard ladder details, AS 1657-1992 basis), in
`G:\My Drive\##Workset_Autocad\400 Standard Details\400 Standard Details\20 - STEELWORK\SE-0504 Steel Ladder Details`.
**Code text checked:** OSHA 29 CFR 1910.23 and 1910.28 on osha.gov (2026-10-15).
**Worked example:** `jobs/steel_ladder_typical` (LAD-ST 5201 – 5203).
**The governing code is the engineer's decision** on each project (Thai law, client standard).

## What a ladder sheet shows (SE-0504)

- Ladder elevation with the rung pitch, clear width and overall width.
- Side views of a sloping and a vertical ladder: stile extensions (loops or goosenecks), wall brackets, the landing
  edge gap, and the limits of slope.
- A section at the landing: infill plate or grating, 50 hand clearance to the stile.
- A cage elevation (hoop spacing, clearance to the first hoop). Cage sections: options A, B and side entry.
- A step ladder at 60 – 70°: step spacing, handrail height, clearance measured square to the slope.
- Details:
  - rung through a hole in the stile, plug-welded and ground flush, fillet all round inside;
  - feet on concrete (chemical anchor, grout) and on grating (bolt).
- A note box "UNLESS NOTED OTHERWISE": plates 10, bolts M20 8.8/S, shop welds 6, site welds 8, at least 2 bolts.

## Limits compared

| Item | SE-0504 (AS 1657) | OSHA 1910.23 / .28 |
|---|---|---|
| Rung pitch | 250 – 300, 250 preferred | 254 – 356 (10 – 14 in), uniform |
| Clear width between stiles | 375 – 525 | ≥ 406 (16 in) |
| Rung c/l to the object behind | 200 min | ≥ 178 (7 in) |
| Stiles above the landing | handrail 900 min (1000 preferred) on step ladders | ≥ 1067 (42 in); walk-through 610 – 762 clear |
| Step-across to the landing | no gap, or 50 – 100 | 178 – 305 (7 – 12 in), through ladder |
| Climbing-side clearance | – | ≥ 762 (30 in) from the rung c/l; ≥ 381 (15 in) each side |
| Slope | 70 – 90°, 75° preferred | ≤ 90° |
| Cage | hoops 50 × 5 at ≤ 2000, verticals 25 × 5, first hoop 2000 – 2200 above the base | Over 7.3 m (24 ft): ladder safety system or PFAS. A cage alone is not accepted on new ladders (from 19/11/2018) or on any ladder after 18/11/2036 |
| Flight length | 6000 max | caged sections ≤ 15.2 m between platforms |

## Members in SE-0504 (typical, to be designed per project)

- Stiles FL 75 × 10; rungs Ø20; brackets FL 75 × 10, 6 fillet, 1-M20.
- Base FL 90 × 10 × 90 with 1-M16 chemical anchor, 125 embedment.
- Step ladder: stiles PL 100 × 10, treads 6 floor plate.

## How it is drawn

- **Front view:** rungs as double lines.
- **Side view:** rungs as circles on the stile centre line.
- **Clear zones:** drawn as dashed boundaries and dimensioned "MIN".
- **Limits:** every limit is a dimension carrying its value or range; options are drawn side by side.
- **Details:** the hole, the plug weld and the anchors are drawn as built (steel S8.4).
- **Helpers:**
  - `steel_access.ladder_front` (with `flare`), `ladder_side` (with `goose`) and `cage_plan`;
  - `anchor_in_concrete` and `member_break`.
- **Checks in the job:** the LAD engine asserts the geometry against the OSHA limits, so a change that breaks a limit
  stops the build.

## Open in the worked example

- Member sizes, bracket spacing (≤ 1800), anchors and the cage dimensions are ASSUMED.
- The design loads (OSHA (d)(1): maximum intended load) are not checked. Add a calc before using it on a project.
