# 20 Base plate and anchor rod drawings: what the set must show [REC]

DG1's advice applied to our drawings (S8.4 follows DG1 since 2026-10-14). The steel rules (S1 – S11) and the annotation guide govern presentation; S8.4 – S8.5 already fix the anchor rod and base plate basics.

## Sheets [REC]

| Sheet | Content |
|---|---|
| **Anchor rod layout plan** (own sheet, issued "for construction" before the foundations are cast) | Grids; every rod group with its **mark**; group centre dimensioned to the grids; rod pattern; **top-of-rod and top-of-concrete levels**; orientation of non-symmetric patterns and lugs; special settings at walls and moment bases (05) |
| **Base plate details** (1:10) | Plan: N × B, rod spacing and edge distances both ways, hole size, column outline, weld faces. Section: plate thickness, **grout thickness**, levelling nuts or shims, washers, lug and grout pocket, rod embedment to the pier bars, pier ties |
| **Schedules** | Base plate schedule (mark, size, grade, holes, weld); **anchor rod schedule** (mark, grade, diameter, total length, thread length, projection, embedment, head or nut, washer size and thickness, quantity) |
| **Foundation drawings** | The same rod marks and levels, cross-referenced; pier bars lapping the rods (11) |

## General notes [REC]

1. **Materials:** plate grade (SS400 / A36); rods **F1554 Gr 36** or the stated equivalent; **heavy hex nuts**; galvanized rods and nuts by one process, one supplier, preassembled (02).
2. **Holes** to AISC Table 14-2 / DG1 Table 2.3; plate washers sized to cover the hole, not welded except where noted (04).
3. **Tolerances:** AISC 303 §7.5.1 values listed in mm; "ACI 117 TOLERANCES DO NOT APPLY TO ANCHOR RODS" (05).
4. **Setting:** by template from the released layout drawing; survey after the pour; report out-of-tolerance rods to the engineer before erection (05).
5. **Erection:** setting method (levelling nuts, shims or setting plate); nuts tight before release of the crane; columns braced until the frame is stable (06, steel S9).
6. **Grout:** non-shrink, f′c ≥ 2 × foundation concrete, 25 – 50 mm, by the concrete contractor, promptly after the erector's notice (06).
7. **Repairs:** no field bending, heating, cutting or welding of rods without the engineer's written approval (07).
8. **Extra thread** of 75 mm beyond the detail requirement (04).
9. **Pretensioned or fatigue joints:** Tm, turn-of-nut, Tv, 48-hour check, locking device (18).

## Design data on the drawings [REC]

- Base type for each column: **pinned or fixed** (01).
- Governing reactions per base type (P, V, M, uplift), from the calc.
- Concrete f′c and grout strength used in the design.

## Presentation reminders [REC]

- Units in notes; dimension figures bare (guide §2.4.2). Tables "TABLE n - NAME" (`DRAWING_PRODUCTION.md` §2).
- AWS weld symbols (S5); **no weld-all-around on W columns** (03). Concrete hatched as background (S4.6).

## Data flow [REC]

All plate sizes, rod sizes, lengths and levels come from one `calc_baseplate.py` (09 – 15). The drawing script reads it and never retypes a number (AGENTS.md §2).

## Before issue [REC]

- Every rod mark is on the layout, schedule and foundation drawing.
- Projection = grout + plate + washer + nuts + 3 threads, and embedment reaches the pier-bar lap.
- Wrench clearance; steel S10 and guide §8 checklists.
