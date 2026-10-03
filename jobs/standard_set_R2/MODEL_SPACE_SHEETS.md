# Standard set R2: typical details (started 2026-09-30)

> This file records the R2 set: its rules, sheets and the review decisions behind them. The engine it was built with
> (`drafter/td_engine.py`, `drafter/pens.py`) is shared by every current set and documented in
> `docs/general/DRAWING_ENGINE.md`: model space and blocks, title block, linetypes and pens, functions, options,
> checks, working in AutoCAD and pitfalls. The R1 guide it started from is `jobs/standard_set/MODEL_SPACE_SHEETS.md`.

R2 is a separate version of the typical-detail sheets. R1 (`jobs/standard_set`) stays frozen. General notes are not part of R2 (they are built in `jobs/standard_set`, `python build.py gn`); R2 cites their tables by number only, for example "TABLE 6".

## R2 rules (user decisions, 2026-09-30)

| Topic | R2 rule |
|---|---|
| Purpose | Typical details show the contractor the general practice where the design drawings give no detail |
| Scale | **Every view N.T.S.**, arranged at one dummy scale 1:25 (`SC` in the engine). View titles read "SCALE N.T.S."; the title block reads N.T.S. |
| Members | **One catalogue for every view: `members.py`.** Column 400 × 400 (8-DB20), beam 300 × 600, secondary beam 250 × 450, slab 150, flat slab 200 + 50 drop, footing 1600 × 1600 × 600, cover 40 / 20, bars DB20 / RB9–DB10 / DB12. Only LENGTHS are shortened (break lines): storey 2400 (infill view 2000), span 3600, stubs, lap 600 drawn |
| Engine | Model space at real size with detail blocks, one layout per sheet, acadiso linetypes at LTSCALE 3.75 / PSLTSCALE 0, pens by colour, and the PSLTSCALE and CTB pitfalls met on R2 (user decisions, 2026-09-30). Now the shared engine: `docs/general/DRAWING_ENGINE.md` §2 – §4, §9 |
| Tables | **Every table has a number and a name, "TABLE n - NAME"**, in one sequence for the standard set: general notes 1 – 10, typical details 11 – 20 in sheet order (11 column ties and splices, 12 max. tie spacing, 13 column call-up, 14 beam schedule, 15 beam reinforcement by frame type, 16 punching shear, 17 trimming bars at openings, 18 slab-on-ground joints and dowels, 19 slab thickness and reinforcement, 20 subgrade, fill and backfill under slabs on ground). Text cites a table by number only, "TABLE 18"; never "TABLE (1126)", "1002 TABLE 6" or "TABLE ABOVE" (user, 2026-09-30). The register is `TABLES` in `td_engine.py`: `TABT(key)` gives the title, `TAB(key)` the citation, and `tbl()` warns about a table without a number. A new table gets the next free number; renumbering means editing only `TABLES` |
| Leader form | **Chosen per target, mixed freely within a detail** (user, 2026-09-30). The target is a vertical line (bar, face, edge), a corner, a bar dot or ring, or an area: the note is placed at the target's height and gets **one horizontal segment**, no inclined leg and no angle at the arrow. The target is a horizontal line only (a slab face, a bar running along the view): the leader cannot run along it, so the note rises `RISE` = 3 mm and gets the **inclined leg** (45° / 60°) + horizontal run. When packing leaves a note within 2 mm of its target height, the arrow slides along a vertical target or inside an area to make the leader exactly horizontal (`_target_kind()`, `_rise()`, `_snap_tip()` in `td_engine.py`) |
| Units in notes | **Every length, depth, spacing, size and tolerance in note text, leaders and table cells carries its unit** ("TIES @ ≤ 150 mm", "THE TOP 150 mm OF THE EXISTING GROUND", "LAYERS ≤ 200 mm THICK AFTER COMPACTION"). The unit goes once after a range ("25 – 75 mm"), and schedule columns carry it in the header ("b × h (mm)", "S1, 2h ZONES (@ mm)"). What stays bare: dimension strings ("DIMENSIONS IN mm"), counts, factors, ratios, code clauses and bar marks. CBR is written as a percentage (user, 2026-09-30) |
| Sheets | Same numbers as R1. Columns gained **1104** (column ends, special cases: roof, transfer beam, discontinued wall, masonry infill), because the 1:25 elevations fill 1101; the typical column notes moved to the foot of 1102 |

## R2 sheets (all done 2026-09-30)

Every R1 sheet number is kept. Where the 1:25 views no longer fit, a continuation sheet was added and the moved items are cross-referenced.

| Set | Sheets | Changes from R1 |
|---|---|---|
| Columns (4) | 1101 elevations + frame table · 1102 size change, joint, footing + column notes · 1103 tie types, splices · **1104** roof top, transfer beam, discontinued wall, masonry infill | Infill 1101/4 and 1102/7–9 moved to 1104; 1113 note 3 now cites 1104/2 |
| Beams (6) | 1111 three frame elevations · 1112 cut-off, cantilever, bar-end key · 1113 sections, supports, openings · 1114 levels, stepped beam, girder end · 1115 schedule · **1116** stirrup types, frame table, beam notes | Stirrup types 1111/4 moved to 1116/1 and the beam notes to 1116; the frame table moved from 1112. References updated: "1116 DETAIL 1", "1116 NOTE n", "KEY ON 1112". The placing diagram shows the end span and the interior span only |
| Slabs (8) | 1121 section, corner panel (with columns), notes, legend · 1122 flat-slab plan, column head · 1123 punching · 1124 openings + trimming table + notes + legend · 1125 steps, upstands, **cantilever (1125/5, from 1121/3)** + legend · 1126 slab on ground: IJ at a ground beam, thickened edge, joint layout, **slab on lean concrete (1126/4)**, joint / dowel table, notes · **1127** joints SJ / CJ / CJ at an existing slab / EJ + seal details A – C · **1128** slab table (Table 19), **slab on compacted fill (1128/1) + Table 20 subgrade / fill / backfill**; the flat-slab notes were deleted at the user's review | Slab-on-ground joints after Beca (below). The R1 flat-slab strip diagrams (1122) were deleted at the user's review; the later sheets moved up one number. The punching-section dimensions read s0 / s |

**Drawn lengths (N.T.S.; member sizes always from `members.py`):**
- storey 2400; beam span 3600; cut-off spans 3000;
- slab-on-beams plan 1800 × 2000;
- flat-slab bay 2200 (plan), 3000 (strips);
- openings plan 2000; joint-layout bay 1500;
- stubs 100 – 300.

**Drawing rules added after the R2 review (user, 2026-09-30):**
- **Row labels of dimension tiers** ("TOP BARS", "BOTTOM BARS", "STIRRUPS") sit directly in front of their row's first dimension, not in a left margin. `row_label()` in `td_engine.py` right-aligns the label before the row's first dimension and steps it left past any extension line of an outer row that rises through the row. Used on 1112/1, 1112/2, 1115/1, 1121/1, 1122/1–3.
- **Additional (extra) bars sit one gap off their main bar, at the same level in every span**: top bars one gap below, bottom bars one gap above. The lap crank of a continuous bar must end clear of the start of the next additional bar, and a lapped bar must start clear of the end of the previous one (1112/1: end-span bottom bars stop 150 past the interior face, the lap starts 250 before it; 1115/1: likewise).

**Beam elevations follow GD-01 (user, 2026-09-30).** Source: `C:\990 - Developing software\102 RC Beam\phase1-mockup\DRAWING_INSTRUCTIONS.md` (sheet GB-01). Applied to 1111/1–3, 1112/1–2 and 1115/1:

| GD-01 rule | R2 implementation |
|---|---|
| Grid bubbles, 7 mm circle, 2.8 mm bold letter, on a centre line through the column | `grid_bubble()`: A, B… on `S-CENT`, circle on `S-SYMB`, above the column stubs (1115: above the top dimensions) |
| Numbered callouts, 4 mm circle, thin leader to the bar or stirrup; the texts in a list | `callout()` + `callout_list()`: top-bar callouts above the beam, bottom-bar and stirrup callouts under the soffit; the list beside the detail replaces the long leader notes. Leaders must not cross (1112/1: callouts 2 and 3 both left of the column) |
| Zone band 3.6 mm high, 8.4 mm under the soffit, grey boxes; dimensions start at the band's bottom edge | `zone_band()` on 1111: STIRRUPS @ s (ordinary), 2h: s1 / MIDDLE: s / 2h: s1 (intermediate, special). The 2h chain dimension is dropped (the band carries it) |
| Column hatch ANSI31, 1.6 mm pitch, grey, the full column height shown | `frame_elev()` and `col_stack()` hatch on `S-HATCH` |
| Stirrups in elevation: hidden line, grey (secondary information) | New layer `S-STIR-ELEV` (ACI 8, 0.18, acadiso HIDDEN); `stirrups()` draws on it. Sections keep solid stirrups |
| Crank 1:6 max. (run = 6 × offset) | `lap_crank()` now 1:6 on every R2 sheet (it was 1:3) |
| Collinear bar ends ≥ 150 apart; extra bars on the cranked-bar level; the crank finishes before the next extra bar | 1112/1 and 1115/1 laps re-set: the end-span bottom bars stop 100 before the interior face's far side, the lapped bar starts 200 before the near face, and the top lap is in the middle third |
| Legend: bars, stirrups, section cut, grid line | The key is now **LEGEND**: plain end, hook, break, cranked lap, stirrups in elevation, grid line + bubble, callout |

Kept from R2 (not GD-01): EIT arrowheads (GD-01 uses ARCHTICK), acadiso linetypes at LTSCALE 3.75, pens by colour, and the TATA / 1112 cut-offs. The one difference is the additional bottom bars: GD-01 stops them Ln/8 from each face, while R2 uses 0.875 L1 at the end span and 0.70 L2 centred at the interior span. Section tags (END / MID / CONT pills) are not used, because the R2 schedule keys bars by letter (1115).

**Focus rule (user, 2026-09-30), every R2 sheet.** Each typical detail is about one element. Everything else is drawn as background:
- its concrete is hatched grey ANSI31 at 1.6 mm pitch (`nf_hatch()`), with a thinner outline where it is a stub;
- its bars go on `S-REBR-NF` (ACI 252, 0.25, grey), drawn solid, not hidden, because hidden already means "concrete below / hidden edge";
- its ties and stirrups seen in elevation go on `S-STIR-ELEV` (grey hidden).

| Set | In focus | Background |
|---|---|---|
| Columns 1101 – 1104 | column, its bars and ties | beam and slab stubs, roof beams, footings (and their mat), the transfer beam and its bars, the wall and beam above a discontinued column |
| Beams 1111 – 1116 | beam | columns (hatched, bars grey, ties grey hidden) |
| Slabs 1121 – 1128 | slab | supporting beams in section (hatched, stirrup and bars grey), column stubs and column bars, the ground beam, the existing slab (1127/3) |

**Exceptions**, where the other element's bars are the subject of the detail and stay full weight:
- the edge / corner joint (1102/5, section A);
- secondary beam on a main beam (1113/2, A);
- beam ending at a girder (1114/3);
- slab plans, where columns are cut and hatched as section.

**Masonry** is hatched AR-BRSTD (brick, real size), so it cannot be confused with background concrete (1104/4).

The legend has a row for it: "OTHER ELEMENT (NOT THE SUBJECT OF THE DETAIL): HATCHED GREY, ITS BARS GREY".

**Slab-on-ground content after Beca SE-1210 – 1219 (user, 2026-09-30);** see `REVIEW_BECA_SLAB.md`:
- joint marks SJ / SJD / CJ / EJ / IJ;
- `pour_header()` FIRST / SECOND POUR;
- `detail_ref()` circle + split bubble to seal details A – C;
- joint / dowel and trimming-bar tables by slab thickness;
- slab-on-ground sections at a dummy 1:10 (`SG`) and seal details at 1:2, all titled N.T.S. (in model space the blocks sit at 2.5 and 12.5; linetypes plot at the same dash lengths).

The Beca **panel-grid sheet layout was tried and rejected** by the user ("our style better"). Slab sheets use the column / beam layout:
- views top-aligned in rows from the top-left (`place_row()` in `td_slabs.py`);
- each title 6 under its own view, with a short note wrapped to the view width;
- notes, tables and legend stacked in the free space (`side_blocks()`).

**Layout lesson:** at 1:25 the height of a view is often set by its stacked leader notes, not by its geometry. Widening the note column is the cheapest fix; shorten lengths next; move notes or tables to a continuation sheet last.

---

## Engine and R1 history

- The block / capture mechanics, title block, AutoCAD workflow, engine functions, options, checks and pitfalls are
  in `docs/general/DRAWING_ENGINE.md` (moved out of this file on 2026-10-03; this file used to carry a copy of the R1
  guide).
- The R1 guide itself, with the R1 build / plot / compare results and the general notes at the normal text size
  (Rev B), is `jobs/standard_set/MODEL_SPACE_SHEETS.md`.
