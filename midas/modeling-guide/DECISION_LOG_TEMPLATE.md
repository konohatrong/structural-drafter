# Decision Log Template

Copy this file into the project folder at the start of modelling. Every answer here is a
modelling rule; the scripts should read or quote it, and each review sheet should list the
ones it depends on. Right-hand column: the fire-station (Building B) answers, 2026-09.

## Geometry

| # | Question | Fire station |
|---|---|---|
| G1 | Origin and axes | Grid 1 / F = (0, 0); X along 1→7, Y along F→A |
| G2 | Column node: grid intersection or true centre? | Grid intersection; C2 75 mm offset removed |
| G3 | Floor levels (typical SFL per floor) | Base −1.00, GF +0.35, 2F +4.75, 3F +7.95, RF +11.15, annex roof +3.95 |
| G4 | Local slab steps: model or ignore? | Ignore; slab at beam level |
| G5 | Base support condition and level | Fixed at pile-cap top −1.00 |
| G6 | Column tops (stop-under symbols, missing columns) | Grid 6 to +4.75; E7, F7 to +3.95 |
| G7 | Members to neglect | BX stair trimmers |
| G8 | Curved beams: chord count / max deviation | 6 chords, 32 mm sagitta (8 chords offered) |
| G9 | Drawing anomalies (displaced / duplicated groups) and their meaning | 2F east bay drawn displaced = annex roof at +3.95 |
| G10 | Shared lines at two levels | Grid 6 beams at +3.95 and +4.75 (option A) |
| G11 | Beam vertical offset (centroid at level or top flush) | Centroid at level (open item) |
| G12 | Parts not modelled | Stair roof +14.15 over bays 1–2 |

## Sections and materials

| # | Question | Fire station |
|---|---|---|
| S1 | Concrete grade | C280 (TIS(RC)) |
| S2 | Marks missing from the schedule | B2A → assumed 250×600 |
| S3 | Footing stub section | 350×350 (C1), 350×500 (C2) from base to GF |
| S4 | Rebar grade and design code | SD40 (TIS(RC), fy 390 MPa); ACI 318M-14 kept |

## Slabs

| # | Question | Fire station |
|---|---|---|
| L1 | Mesh size | 0.50 m |
| L2 | Ground slab: on grade or suspended? | Suspended on ground beams (plates) |
| L3 | Opening size below which the opening is ignored | 1 m² |
| L4 | Cantilever extents | 2F S1C 1.725 m; RF S1C south 1.725, east 1.925, north to Y 9.325 |
| L5 | Slab organisation in the works tree | Structure groups `SLAB_<L>` + `SLAB_<L>-Pxx` (not domains) |
| L6 | Modelling order | GB → 2F → 3F → RF → annex; engineer starts each level |

## Pile-supported ground slab (08)

Example answers from BANWA 2 (07 – 08/10/2026), not the fire station.

| # | Question | BANWA 2 |
|---|---|---|
| P1 | Ground floor system | Pile-supported flat slab with drop panels; ground beams on the perimeter and chosen lines only |
| P2 | Slab and drop | FS200; drops 1.2 × 1.2 × 0.35 (DP350); plates at the slab mid-plane, no offset |
| P3 | Pile size, layout limit | 350 × 350; tributary ≤ 8.41 m² (2.90 × 2.90); no pile under a ground beam |
| P4 | Pile in the model | Stub column 0.00 to −1.50 (the pier length), pinned at the foot |
| P5 | Rigid zone | 8 nodes on the pile (or column) face, `RIGD` to the pile head / column node, DOF 111111 |
| P6 | Columns with no ground beam | A drop over each, as over a pile |
| P7 | Ground beams | GB 400 × 900, top at 0.00 (CT offset); rigid joints |
| P8 | Column supports | Pinned |
| P9 | Mesh size (one for all zones) | 0.40 m |
| P10 | Zones and their order | Zones r3 from the engineer's sketches; one revision per zone; tank roof last |
| P11 | Gutters, pits, walls | Gutter strip 2 000 × 500 at ground level on its piles; lift pit an opening; slab joins the tank wall top |
| P12 | Refined size round drops / strips | 0.20 (outlines pre-split; drops and strip meshed at 0.20), slab 0.40 |
| P13 | Build method | Staged over the whole floor: beams, outlines, piles, slab, drops / strip (one revision each) |
| P14 | Pile check basis (layout) | Service DL + LL + SDL ≤ 95 % of the allowable load (SPUN 300, 35 tonf); LL from the client's load map |

## Loads

| # | Question | Fire station |
|---|---|---|
| D1 | Load cases | DL (self-weight via BODF), SDL, LL |
| D2 | SDL | 2.50 kPa over the whole area |
| D3 | LL basis | Ministerial Regulation B.E. 2566, clause 11 table |
| D4 | Special areas | Water-tank area 5 kPa |
| D5 | Combinations | Clause 7 strength (U1–U9), clause 6 service (S1–S13) |
| D6 | Seismic basis | DPT 1301/1302-61 in the model: SDS 0.60, SD1 0.36, I 1.0, R 5 |
