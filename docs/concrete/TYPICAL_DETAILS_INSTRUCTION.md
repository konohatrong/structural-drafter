# Typical Details Instruction — Columns, Beams and Slabs (A3)

This file explains how to draw the office typical-detail sheets. **Current set R2: columns (1101–1104), beams (1111–1116) and slabs (1121–1128); walls, footings and stairs will follow.** The frozen R1 set had columns 1101–1103, beams 1111–1115 and slabs 1121–1127. It covers:
- which sources govern;
- what each detail must show;
- the drawing and annotation rules;
- how the generator builds the sheets.

**R2 sheets** (titles as generated, `SHEETS` in `jobs/standard_set_R2/td_*.py`):

| Columns | Beams | Slabs |
|---|---|---|
| 1101 Ties and splice zones | 1111 Stirrups and splice zones | 1121 Slabs on beams |
| 1102 Size change, joints, footing | 1112 Bar cut-off and cantilever | 1122 Flat slab at the column |
| 1103 Tie types and splices | 1113 Sections, supports, openings | 1123 Punching shear reinforcement |
| 1104 Column ends, special cases | 1114 Level changes, beam ends | 1124 Openings |
| | 1115 Beam schedule | 1125 Steps, edges, cantilever |
| | 1116 Stirrup types, table, notes | 1126 Slab on ground |
| | | 1127 Slab-on-ground joints |
| | | 1128 Slab table, fill under slabs |

**R1 reference sheets (frozen; the content of each detail is still described per sheet below, and the R2 changes in the R2 notes of §4):**

| Sheet | Title | Content |
|---|---|---|
| `STR-ST-1101-D-A` | Typical column details (1): ties and splice zones | Column elevations for ordinary / intermediate / special moment frames; comparison table; masonry infill; typical column notes |
| `STR-ST-1102-D-A` | Typical column details (2): size change, joints, ends | Size change (4 cases); edge/corner joint plan and section; starter bars in a footing; column top at the roof; column on a transfer beam; column under a discontinued wall |
| `STR-ST-1103-D-A` | Typical column details (3): tie types and splices | Lettered tie types A – J (4 – 24 bars; perimeter tie + crossties on alternate bars) + high-axial type EH (D5); circular hoop; spiral column; mechanical splices; maximum tie spacing table (ordinary / intermediate lo / special lo); schedule call-up example; notes. Added after the ACI MNL-66 review (COL-20, 101, 201, 202) |
| `STR-ST-1111-D-A` | Typical beam details (1): stirrups and splice zones | Beam elevations for ordinary / intermediate / special moment frames; stirrup and hoop types; typical beam notes |
| `STR-ST-1112-D-A` | Typical beam details (2): cut-off, cantilever, anchorage | Continuous-beam bar cut-off; cantilever; beam end at an exterior column; comparison table by frame type |
| `STR-ST-1113-D-A` | Typical beam details (3): sections, supports, openings | Typical section (layers, side bars); secondary beam on a main beam (hangers) + section A; web opening; notes |
| `STR-ST-1114-D-A` | Typical beam details (4): level changes, beam ends | Beams at a column with (a) different top and soffit levels, (b) different depths / tops flush, (c) different top levels / soffits flush; stepped beam within a span; beam ending at a girder; notes |
| `STR-ST-1115-D-A` | Typical beam details (5): beam schedule | Keyed placing diagram (lettered bars A – E, stirrup zones S1 / S2); key section; beam schedule (example rows + a blank row); notes. ACI MNL-66 BM-1 format, keyed to our 1111 / 1112 rules (added 2026-09-30) |
| `STR-ST-1121-D-A` | Typical slab details (1): slabs on beams | Short-span section (Sn/4, Sn/3 cut-offs, layers, hooks); two-way corner panel plan (L/5 corner bars); cantilever slab; typical slab notes; bar-end key |
| `STR-ST-1122-D-A` | Typical slab details (2): flat slab bar extensions | EIT Fig 13.3.8 as schematic strip diagrams (N.T.S.): column strip without / with drop panels, middle strip; bar-end key |
| `STR-ST-1123-D-A` | Typical slab details (3): flat slab at the column | Strip plan (column / middle strip, drop panel, c2 + 3h band, integrity bars); drop panel and capital section; flat-slab notes (EIT + DPT 5.2.12); slab thickness and reinforcement table |
| `STR-ST-1124-D-A` | Typical slab details (4): punching shear reinforcement | Stirrups and headed stud rails: plans 1:25, sections 1:10; rules table (EIT 11.11.3, 11.11.5) |
| `STR-ST-1125-D-A` | Typical slab details (5): openings | Opening < 600 (diagonals); opening ≥ 600 (trimmers + diagonals); openings in flat slabs by strip zone and the 10h rule; bar-end key; notes |
| `STR-ST-1126-D-A` | Typical slab details (6): steps and edges | Slab step H < t and H > t (1:10); upstand fin / curb, small and large (1:10); bar-end key |
| `STR-ST-1127-D-A` | Typical slab details (7): slab on ground | Slab at a ground beam; thickened free edge; contraction, construction, expansion / isolation joints; joint layout; notes |

- **Generator (working):** `jobs/standard_set_R2/`:
  - `td_engine.py` is the shared engine, `pens.py` the pens by colour and `members.py` the typical member sizes;
  - `td_columns.py`, `td_beams.py` and `td_slabs.py` hold the content;
  - `build.py <set|all>` and `plot.py <set|all>` are the drivers. A build with any `!!` layout problem exits 1.
  - Sheets are laid out in model space from blocks at real size (see `jobs/standard_set_R2/MODEL_SPACE_SHEETS.md`).
  - `jobs/standard_set/` holds the frozen R1 set and the general notes Rev B (`gn_notes.py`); `jobs/typical_details/` is the superseded paper-space version.
- **Output:** `jobs/standard_set_R2/out/`, one DXF / DWG / PDF per set:
  - `STR-ST-1101_Typical_Column_Details_A3_R2.*`;
  - `STR-ST-1111_Typical_Beam_Details_A3_R2.*`;
  - `STR-ST-1121_Typical_Slab_Details_A3_R2.*`.

  The block library (one DWG per detail, plus the title block) is in `jobs/standard_set_R2/library/`. The general notes Rev B are built in `jobs/standard_set/` (`python build.py gn`).
- **Review tools:** `crop_det.py <set> DET-xxxx-n` crops one detail out of the plotted PDF; `render_block.py` renders a block without AutoCAD.
- **Sources:** `SOURCES_COLUMN_DETAILING.md`, `SOURCES_BEAM_DETAILING.md`, `SOURCES_SLAB_DETAILING.md` (`docs/concrete/reference/`).
- **Cross-check:** `REVIEW_ACI_MNL66.md` (ACI Detailing Manual MNL-66(20); material in `references/aci_mnl66/`).

**Read with:**
- `docs/general/DRAWING_STANDARD_EIT-011006-19.md` (§19 office rules) and `docs/concrete/RC_DRAWING_RULES_EIT-011006-19.md` (bar graphics, §19.4 / §19.7);
- `ANNOTATION_ALIGNMENT_GUIDE.md`;
- `GENERAL_NOTES_STRUCTURAL_CONCRETE.md` (sheets `1001 – 1003`, Rev B: laps in TABLE 6 and cover in TABLE 7, both on 1002; tie sizes in TABLE 5);
- `SPEC_RC_DESIGN_EIT-011008-21.md`.

---

## 1. Numbering and drawing rule

**Series.** Typical details use **11xx**, in the general series 1000–1999 of EIT 011006-19 Ch. 4:
- `1001` general notes;
- `1101–1109` typical column details;
- then 1111+ for beams, 1121+ for slabs, 1131+ for walls, 1141+ for footings, 1151+ for stairs (planned).

**Drawing rule.** The **normal** office rule applies, not the ×0.625 notes-sheet rule:

| Element | Value |
|---|---|
| Text | Arial Narrow 2.0; headers and view titles 2.8 bold |
| Dimensions | 2 mm filled arrows, grey extension lines |
| Leaders | 45° / 60° legs with a 3 mm shelf; tips on edges; bar marks in bubbles |
| Units | Every measured value in a note or leader carries its unit; table headers carry it for the cells; dimension figures stay bare (`ANNOTATION_ALIGNMENT_GUIDE.md` §2.4.2). The R2 sets keep their issued line breaks until revised (`WRAP_UNITS` stays off) |
| Pens | Standard: bars 0.50, ties and secondary bars 0.35, cut concrete 0.35, seen 0.25, annotation 0.18, grey hatch 0.13 |
| View titles | EIT style: underlined bold 2.8, scale below, bubble with detail number / sheet. Title width is **measured** (`text_w`) so the bubble never overlaps |

**Scales:**

| Scale | Used for |
|---|---|
| 1:50 | Storey elevations, roof, footing, transfer beam |
| 1:25 | Size change, joints, tie types, circular hoop, spiral, mechanical splices |
| 1:100 | Small diagrams (masonry infill) |

All are standard EIT scales.

**Symbols, not sizes.** Typical details show *symbols*; the governing numbers are in the table on 1101 and in the design standards:
- zones and spacings: `lo`, `s0`, `s`, `Hc`, `Hc/4`, `ldh`;
- labels: `LAP (TABLE 6, 1002)`.

After any change to the general notes, check that the tables cited by number still sit where they are cited. `build.py gn` prints each table's number and sheet, and warns through `TABLE_REFS`.

The drawn column is a typical 400 × 400 with DB20 bars and RB9 ties, drawn to scale only for proportion. Intermediate and special frames use DB10 hoops (decision D3); the drawn size is not a callout.

---

## 2. Sources and what they govern

| Source | Governs |
|---|---|
| **EIT 011008-21** (design) | Ordinary-frame ties (7.10.5): size by bar, s ≤ 16 db / 48 dt / least dimension, first tie ≤ s/2, may stop 75 below beam bars with beams on 4 sides; offset bars (7.8.1): slope ≤ 1:6, ties within 150 of the bends for 1.5 × thrust, face offset ≥ 75 → dowels; spirals (7.10.4); hooks and bends (7.1, 7.2); laps (12.14–12.16); anchor-bolt ties (7.10.5(ช)) |
| **DPT 1301/1302-61** (seismic) | Frame type allowed by seismic category (T2.3-1); **intermediate** frames (5.2.7.4): lo, s0, first hoop s0/2, 2 s0 outside lo, laps in the mid zone staggered ≈ 1.0 m, joint hoops Av ≥ c1 s / 3fy; **special** frames (5.2.9, 5.2.10): ΣMc ≥ 1.2 ΣMb, ρ 1–6 %, lo, s ≤ min(c/4, 6 db, s0 = 100 + (350 − hx)/3), 6 db / 150 outside lo, tension laps in the centre half only, crossties, joint hoops, ldh, hoops ≥ 300 into the footing; **masonry infill** (5.2.5.1) |
| **TATA / Jiravacharadet RC detailing handbook** (office practice, ACI 315 based) | Size-change cases (2 extra ties below the soffit, dowels, edge columns); lap zones on typical elevations; footing dowels (to the bottom mat, 90° hooks, ties in the footing); roof terminations (interior hooks outward, edge hooks inward); column on a transfer beam; tie patterns; ACI 352 joint practice |

Where sources differ, the stricter value is drawn, and the table names the source:
- **Size-change offset limit:** TATA / Thai sheet 75 mm, ACI 80 mm → **75**. Cranked below 75; 75 or more → separate dowels (EIT 7.8.1.5).
- **First tie:** TATA 50 mm, EIT ≤ s/2 → EIT s/2, with lo zones at s0/2 for seismic frames.

**Design-policy decisions (user, 2026-09-29, after the ACI MNL-66 review):**

| # | Decision |
|---|---|
| D1 | Special-frame beam hoops in 2h: **stricter of DPT and ACI**, s1 ≤ min(d/4, 6 db, 24 dt, 150). DPT prints d/4, 8 db, 24 dt, 300; ACI 318-11 prints d/4, 6 db, 150 |
| D2 | Intermediate-frame beam hooks: **DPT rule kept** (90° + 6 db; 135° or hook-clip in 2h for public / ductile buildings). The 1112 table notes "ACI 318: HOOPS" |
| D3 | **Deformed hoops and crossties, DB10 minimum, in intermediate and special frames**; RB9 allowed in ordinary frames |
| D4 | **Laps at a floor: the lower bars are cranked inside the joint**, top bend ≤ 75 below the slab top, so the lapped bars run straight. Mid-height laps (intermediate / special) keep the crank at the lap |
| D5 | **Option B (2026-09-30): applied only where the design uses ACI 318-19 18.7.5.2(f)** (special, Pu > 0.3 Ag f'c or f'c > 70 MPa): every perimeter bar held, crossties 135° both ends, hx ≤ 200. 1103 note 6 + tie type EH; the schedule marks these columns. Not a blanket office rule |

---

## 3. Sheet 1101 — ties and splice zones

### 3.1 Details 1–3: one storey of an interior column (1:50)

Common geometry:
- **Levels:** floor (beam top) at 0; beam depth 600 below it; clear height Hc (3000) to the upper beam soffit; beam stubs each side with break lines; column broken above and below.
- **Bars:** two face bars drawn; the **lapped bar sits inside the continuing bar**, drawn 50 apart at 1:50 (schematic).
  - **Ordinary (lap at the floor, D4):** the lower-storey bars are cranked 1:6 inside the floor joint, top bend 75 below the slab top. The lap above the floor runs straight. The same crank repeats at the upper joint.
  - **Intermediate / special (mid-height laps):** the upper bar is offset-bent back to the face line above the lap, at 1:10.
- **Ties:** one line per tie across the column, `S-REBR-SEC`.
  - Ties are drawn **only within the view limits**. A tie beyond a break line is an error.
- **Dimensions:** all on the left, tiered so that no extension line crosses a dimension line:
  1. lap or splice innermost: `LAP`, `≈ 1.0 m`, or a single `SPLICE ZONE, CENTRE Hc/2`;
  2. then the `lo – MID ZONE – lo` chain;
  3. then `Hc (CLEAR)` outermost.

  The Hc/4 – Hc/2 – Hc/4 chain was dropped because it interleaves with the lo chain.
- **Notes:** a right-hand leader column; tips on the tie or bar concerned.

| Detail | Ties | Lap | Joint |
|---|---|---|---|
| 1 Ordinary | s throughout; first and last ≤ s/2 from floor and soffit | Just above the floor, both faces at the same level; lower bars cranked 1:6 inside the joint below (D4) | Ties continue (may stop 75 below the lowest bars of the shallowest beam with beams on 4 sides) |
| 2 Intermediate | lo zones at s0 (first ≤ s0/2); ≤ 2 s0 outside | Mid zone only; left and right laps staggered ≈ 1.0 m; offset 1:10 | Av ≥ c1 s / 3fy over the deepest beam |
| 3 Special | lo zones at s (first ≤ s/2); ≤ 6 db / 150 outside; **at s over the lap** | Centre half only (between Hc/4 and 3Hc/4), tension class B | Full hoops; ½ and ≤ 150 with 4 beams ≥ ¾ c |

### 3.2 Table "Column ties and splices by frame type"

- **Rows:** use; section and bars; lo; spacing in lo; first tie; spacing outside lo; hooks and crossties; lap location; lap type; joint; at footing; reference.
- **Format:** text 2.0, rows 5.2 + 3.33 per extra line, every cell **centred on its row**. The item column is left-aligned and bold; the value columns are middle-centred (`tbl(..., align="LCCC")`).
- **Seismic categories** are written **B / C / D**. The Thai letters ข / ค / ง do not exist in Arial Narrow.

### 3.3 Detail 4 — column beside masonry infill (1:100, DPT 5.2.5.1)

- **(a) Partial-height infill:** hoops at s0 over the full clear height; shear for the short column; hoops extend ≥ c1 into the wall zone.
- **(b) Full infill on one side:** lo zones at s0; mid zone ≤ 2 s0 **and ≤ d/2**.
- **Drawing:** the walls are hatched ANSI31 (grey). Captions go below the lowest break line (view bottom = beam soffit − 300).

### 3.4 Typical column notes (7 notes, full width under the table and the infill view)

1. Scope, where the frame type is defined, and a pointer to 1103.
2. Ties: office minimum RB9 (ordinary) or deformed DB10 (intermediate / special); the code minimum by bar size; 135° hooks staggered; every corner and alternate bar held, ≤ 150 clear.
3. Offset bars: 1:6; laps at a floor cranked inside the joint; ties at the bends.
4. Laps and couplers:
   - where a lap doesn't fit its zone, or ρ > 4 %: couplers or alternate-floor laps;
   - a tie just above and just below each coupler;
   - Type 2 couplers within lo in special frames.
5. Anchor-bolt ties.
6. Column on a transfer beam.
7. Spirals: laps 48 / 72 db; termination without beams on all sides.

Each note ends with its clause reference.

---

## 4. Sheet 1102 — size change, joints, ends

| # | Detail | Must show |
|---|---|---|
| 1 | Size change, interior, offset < 75 (1:25) | Lower bars cranked ≤ 1:6 inside the joint depth (bottom bend at the soffit, top bend at the slab top), ending inside the upper bars; lap above; 2 extra ties within 150 of the bottom bend; ties ≤ 150 through the joint; offset dimension "< 75", text outside (`tside`) |
| 2 | Size change, interior, offset ≥ 75 | Lower bars stop 50 below the slab top with a **90° hook inward**; **dowels** on the upper-bar line, lapped below and above; ties ≤ 150 through the joint; "≥ 75". No bend-tie note (no bend) |
| 3 | Size change, edge, < 75 | Exterior face flush (no beam that side); interior bars cranked |
| 4 | Size change, edge, ≥ 75 | Exterior bars continue; interior side dowelled, as 2 |
| 5 | Edge / corner joint, plan (1:25) | Corner column (8 bars, perimeter tie with wrapped 135° hooks); beams from two sides; beam top bars to the far side of the core, ends marked **×** (bent away from the viewer, EIT T3.1 #5); cutting plane A |
| A | Section A (1:25) | Beam top bars hooked **down** and bottom bars **up**, inside the far-face column bars; ldh from the column face; column ties **through the joint** at ≤ 150 (special: hoops at s); first beam stirrup ≤ 50 from the face |
| 6 | Starter bars in footing (1:50) | Dowels = column bars down to the bottom mat with 90° hooks outward. Hooks go inward at a property line, and **toward the centre in special frames fixed at the base** (ACI 318-11 21.12.2.2). Straight length ≥ ldc: a hook doesn't count in compression. Min. 3 ties in the footing; first tie ≤ s/2 (lo zone ≤ s0/2) above the footing. Special: hoops ≥ 300 into the footing, through its full depth at an edge within h/2 |
| 7 | Column top at the roof (1:50) | (a) interior: 90° hooks **outward**; (b) edge / corner: hooks **inward**; a 12 db hook at the top **and** ≥ ldh above the soffit; ties to the top |
| 8 | Column on a transfer beam (1:50) | Bars to the beam bottom layer with 90° hooks outward; ties continue into the beam at the same spacing |
| 9 | Column under a discontinued wall (1:50, added 2026-09-30) | DPT 5.2.9.4.5 / ACI COL-104, special frames with Pu > Ag f'c/10. Wall and transfer beam drawn to the **left** so the notes on the right reach the column; storey height broken. Hoops @ s0 over the **full height of every storey below the wall**, through the beam and **≥ ld (largest column bar) into the wall**; column bars ≥ ld into the wall; hoops **≥ 300 into the footing** (≥ ld into a wall below); dowel hooks toward the centre. (The old 1102/9 tie arrangements moved to **1103/1** on 2026-09-29: the 12-bar "2 overlapping ties" left two adjacent side bars unsupported, EIT 7.10.5.3) |

**Stirrup and tie rule (all sections).** Every corner is concentric with its corner bar, and both 135° hooks wrap the same bar (`stirrup()`).

**Crosstie rule.** A crosstie has a 135° hook at one end and 90° at the other; consecutive crossties alternate ends (`crosstie()`). Legs are the same size as the ties. **Both hooks wrap their bar:** the arcs are concentric with the bar, and the body runs tangent past the bars. Draw the wrap radius one tie diameter outside the hoop (r = bar radius + tie/2 + max(tie, 0.5 mm × scale)) so the 90° tail reads beside the hoop, not on top of it. Turn the 135° tail into the core, away from the hoop's own 135° hooks (top-left corner). A crosstie drawn from bar centre to bar centre is wrong.

---

## 4A. Sheet 1103 — tie types and splices (added 2026-09-29)

| # | Detail | Must show |
|---|---|---|
| 1 | Tie types A – J (1:25) | 4 – 24 bars, square and rectangular (A 2×2 … J 7×7; B 2×3, D 3×4, F 3×6). Perimeter tie + **crossties on alternate intermediate bars, the first one held**, so every corner and alternate bar is held and no bar is > 150 clear from a held bar. Crosstie 90° ends alternate. Label: type, bars (nx × ny), "TIE + n CROSSTIES". Section sizes are illustrative: the type is set by the bars per face. **Type EH** (D5, row 2, last slot): 12 bars, a crosstie on **every** intermediate bar with **135° hooks at both ends** (`crosstie(..., both135=True)`), label on 4 short lines so the view does not widen |
| 2 | Circular hoop (1:25) | Hoop ends overlap ≥ 150 with 135° hooks round a bar; overlaps of successive hoops staggered |
| 3 | Spiral column (1:25) | Clear pitch 25 – 75 (≥ 4/3 max. aggregate), spiral ≥ 9 mm, 1.5 extra turns at each end, laps 48 db (DB) / 72 db (RB); ties above to the slab soffit where beams don't frame on all sides |
| 4 | Mechanical splices (1:25) | Alternate bars spliced at two levels ≥ 600 apart; a tie just above and just below each splice level, none at the coupler; cover measured to the coupler; Type 1 (≥ 1.25 fy) / Type 2 (develops fu) within lo or 2h of a joint in special frames |
| Table | Maximum tie spacing (mm) | By bar size DB16 – DB32. Ordinary: min(16 db, 48 dt) for RB9 / DB10 / DB12, "–" where the tie is below the code minimum. Intermediate lo: min(8 db, 24 dt with DB10, 300). Special lo: min(6 db, 150). Rounded down to 5 |
| Table | Schedule call-up (example) | Mark, size, bars, type letter, ties (lo / elsewhere), frame |
| Notes | Notes to 1103 | Rule for other bar counts; special hx ≤ 350; crosstie hooks; the extra spacing limits (least size, c/2, c/4, s0); spirals; **6: D5 high-axial columns (type EH)** |

---

## 4B. Beam sheets 1111 – 1115

**Sources and what they govern** (extracts in `SOURCES_BEAM_DETAILING.md`):

| Source | Governs |
|---|---|
| **EIT 011008-21** | Cover (7.7); spacing and layers (7.6); stirrup hooks (7.1.3); compression-bar enclosure (7.11); structural integrity — ≥ 2 continuous bars, top laps near midspan, bottom laps near supports, Class B (7.13); T-beam flanges (8.11); minimum depth (T9.1); As,min (10.5); crack-control spacing and side-face bars (10.6); deep beams (10.7, 11.7); stirrup spacing d/2, 600 / d/4, 300 (11.4.4); Av,min (11.4.5); torsion (11.5); cut-off extension max(d, 12 db), 1/3 of top bars past the inflection point by max(d, 12 db, ln/16), ≥ 1/4 of bottom bars ≥ 150 into supports (12.9–12.11); laps (12.13–12.15). **EIT numbers ≠ ACI from 12.9 on — cite EIT numbers.** |
| **DPT 1301/1302-61** | Ordinary: ≥ 2 + 2 continuous (5.2.6). Intermediate (5.2.7.3, Fig 5.2-3): +Mn ≥ ⅓ −Mn at the face, ≥ ⅕ anywhere; 2h zones, first ≤ 50, s1 ≤ min(d/4, 8 db, 24 dt, 300); d/2 elsewhere; no laps within 2h; hooks 90° + 6 db ≥ 75, 135° or hook-clip in 2h for public / ductile buildings (5.2.7.6). Special (5.2.8): ln ≥ 4d, bw ≥ lesser(0.3h, 250); ρ ≤ 0.025; ½ / ¼ moment rules; laps not in joints, 2h zones or hinges, hoops over laps at ≤ min(d/4, 100); hoops over 2h with **8 db** (as printed, not ACI's 6 db); cap-tie hoops with alternating 90° ends; ldh = max(8 db, 150, fy db / (5.3√f'c)) (5.2.10.4) |
| **TATA handbook** | Cut-off points on clear spans (Fig 2.27): top L1/4 at the exterior support, L/3 each side of interior supports (L = larger span); extra bottom 0.875 L1 (end span), 0.70 L2 centred (interior). Bar-end ticks for additional bars (Fig 2.13) — **not used by the office** (user, 2026-09-30: plain bar ends). Cantilevers (Figs 2.37–2.39). Secondary / main beams and hangers (Fig 2.31, p.180). Beams at different levels (Figs 2.40–2.41). Web openings (Figs 2.54–2.58). Side bars when h > 600 (p.176/178) |

**Decisions (flag to the user when changed):**
- **Frame-type elevations (1111)** follow DPT Fig 5.2-3: exterior column left (hooks), interior column right (bars continuous), 2h zones on every face.
- **Cut-offs (1112/1)** use the TATA clear-span rules, valid for uniform load, adjacent spans within 20 %, LL ≤ 3 DL (EIT 8.3.3); otherwise per design.
- **Secondary beam top bars pass OVER the main-beam top bars** (TATA Fig 2.31; the secondary beam is in hogging over the main beam). TATA p.180 cranks them under — conflict noted.
- **Side-face bars at h > 600** (TATA). EIT 10.6.7 prints "web depth > 400" (ACI: 900), a probable misprint to confirm with the user. Since the ACI review they go **on both faces over the full web depth**, because the tension face changes along a continuous beam. Spacing @ ≤ 250 (crack control EIT 10.6.4); the first bar ≤ 150 below the slab. Now 1113 note 7.
- **Additional main-beam stirrups at a secondary beam: min. 3 each side @ 50 unless shown** — office default, not from a source.
- **Perimeter beams (1111 note 3, EIT 7.13.2):**
  - continuous top bars ≥ 1/6 of the support top bars, lapped at midspan;
  - continuous bottom bars ≥ 1/4 of the midspan bottom bars, lapped at the support;
  - Class B laps; closed stirrups over the whole span; integrity bars inside the column bars.
- **Torsion (1113 note 6):** closed stirrups continued bt + d past the point needed; longitudinal bars developed (hooked) at both ends. A U-stirrup + cap tie (1111/4 b) is **not for torsion beams**.
- **Hoops in special frames:** D1 (stricter of DPT and ACI); every corner and alternate bar held (1111 note 5, DPT 5.2.8.3.3 → EIT 7.10.5.3). Hoops and crossties are DB10 in intermediate / special frames (D3).
- **Bottom bars into supports (1112/1):** ≥ 1/4, or 1/3 at a simple support (EIT 12.11.1).
- **Openings (1113/3):** d0 ≤ h/4 in the middle third, ≥ h/2 clear of supports / loads / other openings (TATA); "not in 2h zones of seismic frames" is an office addition.
- **Level changes at a column (1114/1):** never crank a continuous bar through the level change (TATA Fig 2.40). Bars that stay at one level run straight (≥ Ld into the other beam, plain end); bars that would leave the concrete stop with a 90° hook inside the column at the far face. (c) soffits flush is the mirror of (b) tops flush: bottom bars continuous, lower-beam top bars Ld into the higher beam, higher-beam top bars 90° down.
- **Stepped beam within a span (1114/2, TATA Fig 2.43):** same depth h each side, shift Δ ≤ h. A step zone ≥ h long and h + Δ deep (upper soffit dropped over the zone) carries the transfer. Upper top bars to the step face and 90° down through the zone; lower top bars straight through the zone **≥ 1.3 Ld (Class B, a non-contact lap)** into the upper part (was 35 db / Ld before the ACI review); upper bottom bars ≥ 1.3 Ld into the lower part; lower bottom bars to the far end of the zone, 90° up; closed full-depth stirrups in the zone: a double stirrup (two at 30) just inside each face and equal spaces ≤ 100 between them; the bent-down upper top bar sits at 59 from the step face, clear of the stirrups. Step up or down = same detail mirrored. Δ > h: per design (step block or stub column, TATA Figs 2.44 / 2.45).
- **Beam ending at a girder (1114/3, added 2026-09-30; ACI BM-204, TATA p.180 case 3):** section along the secondary beam, girder cut. Top bars **over the girder top bars** (girder top bars one bar lower, as 1113), to the far side, **90° down inside the girder bars**, "≥ ldh" from the girder face; **≥ 2 bottom bars to the far side, 90° up** (others ≥ 150 in), the up-leg 45 inside the top bar's down-leg; first stirrup 50 from the face (a dimension, not a leader); girder stirrups closed with 135° hooks, **hanger stirrups each side of the beam (min. 3 @ 50, as 1113/2)**. 1114 note 6: the girder must hold ldh (else smaller or headed bars per design); a slab continuing beyond the girder lets the top bars run on Ld past the far face; girder torsion per design.

- **Beam schedule (1115, added 2026-09-30; ACI MNL-66 BM-1 / 315R 4.10.2, 5.2.6):**
  - **Letters** (= schedule columns): **A** continuous top (hooked at the exterior support, lapped near midspan), **B** additional top at the exterior support (L1/4, 90° hook), **C** additional top at interior supports (L/3 each side, L = larger adjacent clear span), **D** continuous bottom (hooked up at the exterior support, lapped at the interior supports), **E** additional bottom (0.875 L1 from the exterior face; 0.70 L2 centred), **SB** side-face bars each face, **S1 / S2** stirrups in the 2h zones / the rest. Cut-off points are those of 1112/1 (TATA Fig 2.27) so the two sheets never disagree.
  - **Placing diagram (1115/1):** end span + interior span + part of the next, spans 4000 drawn at **1:40, titled N.T.S.** (the only 1:40 view; `DS` now has a 1:40 dimension style). Letter tags: dot on the bar, 60° leg, short shelf, bold letter (`_tag`), top letters above the beam and bottom letters below, clear of the dimension tiers. Tiers: top = bar lengths (L1/4, LAP, L/3); bottom, nearest first = bottom-bar cut-offs (0.125 L1, 0.15 L2), stirrup zones (S1: 2h / S2 chain), clear spans.
  - **Key section (1115/2):** an 800-deep beam so SB shows; leaders ordered so none runs through a bar (B / C first, rising diagonally, then A level). No "b" dimension: its extension lines blocked the D leader, and the schedule gives b × h.
  - **Schedule columns:** MARK, b × h, FRAME (ORD. / INT. / SPE.), A, B, C, D, E, SB, S1 (2h ZONES), S2 (REST), TYPE ((a) – (d) of 1111/4), REMARKS. Example rows are checked against our rules (B2 INT.: s1 125 ≤ d/4 = 135; B3 SPE.: s1 100 ≤ min(d/4, 6 db, 150); B3 h = 800 → SB). A blank row is left for use.
  - **Notes 1 – 8:** letters and cut-offs; mark = one section over all spans, else B1-1, B1-2 …; "DB10 @ 125" = spacing, "n-DB10 @ 125" = number of stirrups, not spaces (315R 5.2.6); frame and lap rules; A / D ≥ 2 and the perimeter integrity fractions; SB and torsion; special beams named in REMARKS; the contractor's bar-bending schedule is prepared from it and submitted.

**Drawing conventions for beams:**
- Elevations at 1:50 (spans), anchorage / secondary beams / openings at 1:25, sections at 1:20 – 1:25.
- **Bar ends (office standard, user 2026-09-30, all drawings):** a bar end is drawn **plain, with no end mark**: no slash or tick (the TATA Fig 2.13 slash looked messy and was removed from every sheet; `tick()` is gone). Additional (extra) bars are drawn offset from the continuous bar; their plain ends show where they stop.
- **Lap splices (office standard, user 2026-09-30, all drawings):** draw a lap as a **cranked bar**: the lapped bar runs offset alongside the other bar from its own end, passes the other bar's end by 100, then cranks back to its main line at 1:3 (`lap_crank(x_end, x_other, y, dy)` in `td_engine.py`). Never draw two parallel offset bars for a splice. Used on 1111/1 – 3, 1112/1, 1113/A, 1115/1, 1121/1, 1121/3, 1122/1, the GN lap-splice figure and the bar-end key. Keep a crank clear of the start of an additional bar on the offset line (move the lap, e.g. 1115/1 top lap at L/2 − 600 … L/2 + 200), or the crank reads as that bar's start. Column laps keep the D4 crank inside the joint.
- Lapped bars drawn offset by `GAP` (45) with a short crank; laps are schematic (real lengths in 1001 table 6).
- Stirrups drawn at their real centreline; in 1112/1 only the first stirrup at each face is drawn ("STIRRUPS PER THE BEAM SCHEDULE").
- Stirrup types: closed (`stirrup`), U + cap tie (`ustirrup` + `crosstie`, 90° end on the slab side), two closed stirrups (4 legs), 90° hook (`stirrup90`, DPT Fig 5.2-8(a)).

---

## 4C. Slab sheets 1121 – 1127 (R2: 1121 – 1128)

Sources in `SOURCES_SLAB_DETAILING.md` (A: DPT, B: EIT 011008, C: TATA).

| Source | Governs |
|---|---|
| **EIT 011008-21** | Cover 20/30 interior, 40/50 exposed, 75 on earth (7.7); main-bar spacing 3h / 450 one-way (7.6.5, 10.5.4), **2h two-way** (13.3.2); min. and S&T steel 0.0025 / 0.0020 / 0.0018 on b·h, S&T ≤ 5h / 400 (7.12); min. thickness Table 9.1 (ℓ/20, 24, 28, 10), Table 9.3 and Eq. 9-11 / 9-12 (9.5.3); bottom bars ≥ 150 into supports and top bars hooked at discontinuous edges (13.3.3 – 13.3.5); corner bars L/5 (13.3.6); drop panel ≥ h/4, ≥ L/6 (13.2.5); **Fig 13.3.8** extensions and integrity bars (13.3.8); openings by strip zone (13.4) and the 10h punching rule (11.11.6); punching stirrups and stud rails (11.11.3, 11.11.5) |
| **DPT 1301/1302-61** | Flat slab in an intermediate moment frame (5.2.12): column-strip placement, c2 + 3h, ¼ top continuous, ⅓ / ½ bottom continuous, Vu/φVc ≤ 0.4; SDC D non-SFRS slab-column shear reinforcement 4h unless the drift limit is met (5.2.12.1.4, 2.11.5 → ACI 18.14); integrity Asm (5.2.12.2) |
| **DPT road-works standards (มยผ. 2101 – 2225 - 57)** | Subgrade, fill and backfill under slabs on ground (Table 20, 1128): fill classes 2101 4.1 – 4.3, clearing 2112, embankment construction 2114 (layers ≤ 20 cm compacted, 95 % standard for soil / modified for soil aggregate and sand, top 15 cm of the existing ground, soft ground, ponds), field density 2204. Review: `REVIEW_BECA_SLAB.md` §6 |
| **TATA handbook** | Slabs on beams: top bars Sn/4 (edge) and Sn/3 (interior), bent-up option Sn/7 / Sn/4; short bars outermost; chairs DB12 @ 1.0 – 1.5 m; openings < 600 / ≥ 600 (diagonals, trimmers 800 past corners); slab steps (p.181); upstand fins and curbs (p.181 – 182); flat-slab capitals; slab on ground (mesh 30 – 50 below the top, isolation gap 20 – 25, thickened edge, joints ≤ 30t, plain RB dowels @ 300 (RB19 × 400 for t ≤ 150, RB25 × 450 for t ≤ 200; deformed bars lock the joint, ACI SOG-100), saw cut 3 × t/4) |

**Decisions:**
- **Strip diagrams (1122) are schematic, N.T.S.** — slab depth exaggerated so the bar groups read; lengths in proportion. EIT Fig 13.3.8 is itself schematic.
- **Middle-strip bottom cut-off:** EIT 0.15 ℓn from the interior face adopted (TATA's older 0.125 L from the centreline not used); column-strip bottom bars all continuous (EIT), TATA's "50 % may stop" not used.
- **Cantilever slab back length:** "≥ Ld, ≥ the cantilever length Lc and ≥ the back span's Sn/3 top-bar length". This is an office rule consistent with the beam cantilever (1112/2); ≥ Lc was added after the ACI review (SLAB-2.3).
- **Top-bar hooks** need ≈ 16 db between the covers. Where they don't fit, use a 180° hook or edge U-bars. Free edges: ≥ 2-DB12 top and bottom (1121 note 6).
- **Two-way main-bar spacing:** ≤ 2h **and 450**. The ACI 318-19 cap is adopted as office practice.
- **Strip diagrams:**
  - 0.20 ℓn rows sit nearer the slab than the 0.30 / 0.33 ℓn rows;
  - the drop-panel dimension row was removed from 1122/2 because it cannot be tiered cleanly; it is given in the note and in 1123/2.
- **1123/2 capital:**
  - the inclined bars are parallel to the 45° face at 50 cover, with a leg down inside the column bars and a leg up into the drop;
  - the drop panel is dimensioned over its full width, "≥ L/3 (L/6 EACH WAY)";
  - the centreline stops above the dimensions.
- **Slab on ground (1127):**
  - dowels are **plain** RB19 × 400 (t ≤ 150) or RB25 × 450 (t ≤ 200), half greased @ 300; deformed bars lock the joint;
  - contraction-joint mesh stops 50 each side by default;
  - the expansion joint is separate from the isolation joint (filler and sealant only, no dowels).
- **Slab on ground, R2 (after the Beca review, 2026-09-30; `REVIEW_BECA_SLAB.md`):**
  - two sheets: 1126 (isolation joint at a ground beam, thickened edge, joint layout with marks, joint / dowel table by t = 150 / 175 / 200, notes) and 1127 (sawn joint SJ / SJD on baskets, construction joint, construction joint at an existing slab with drilled epoxy dowels, expansion joint, seal details A / B / C). The slab table moved to 1128 (the flat-slab notes were later deleted at the user's review; 1128 also holds the slab on compacted fill and Table 20);
  - base: 0.2 polyethylene sheet on compacted sand (1126/1, 2), or 50 lean concrete instead of the sheet (1126/4, user 2026-09-30). The sand is hatched on `S-HATCH-SAND` (full 0.18 pen) and the sheet is offset square to the soffit;
  - sections at a dummy 1:10, seal details at 1:2 (N.T.S.); FIRST / SECOND POUR header; dowels dimensioned EQ | EQ; a 0.2 polyethylene sheet on the sand bed in every section;
  - seals: A = polyurethane on a Ø8 backer rod in a 6 × 20 reservoir, ≥ 28 days (foot / pneumatic tyres); B = semi-rigid epoxy / polyurea full depth, flush, ≥ 60 days (hard wheels); C = 20 filler with a ≈ 30 cap strip, Ø25 rod, sealant 20 × 10, 3 below the surface.
- **Openings, R2:** a MINIMUM TRIMMING BARS table by slab thickness (Beca SE-1219 layout) on 1124; note 2's replaced-area rule governs where it gives more. Table values are office proposals, to be confirmed.
- **R2 review (2026-09-30):** the flat-slab strip diagrams (R1 1122) were deleted at the user's request and the later sheets renumbered 1122 – 1128; the corner-panel plan shows the columns; the joint-layout diamonds clear the column corners; the sand bed is hatched up to the soffit.
- **Slab sheet layout, R2:** same as the column and beam sheets (views in rows, each titled under itself). A Beca panel grid was tried and rejected by the user on 2026-09-30.
- **Slab steps:**
  - **H < t:** separate bars, each anchored Ld (TATA p.181).
  - **H > t:** TATA p.181, mirrored (corrected 2026-09-29 after the user flagged a "mess rebar arrangement"). The lower-slab soffit runs t past the step face, then a 45° haunch rises to the upper soffit.
    - Upper top bars go down the step face, then Ld along the lower bottom.
    - Upper bottom bars run straight past the haunch corner to the step face, with a 90° hook down.
    - Lower bottom bars go up the haunch parallel to it at cover, then straight on to the upper-slab TOP layer, then Ld. After the ACI review they are no longer bent at the re-entrant corner. H < t does the same: lower bottom bars go up to the top layer.
    - Lower top bars are cranked 45° up, 80 clear of the haunch bars, to the upper top, then Ld.
    - No bar follows the re-entrant corner, and no two sets share a path.
- **Openings:**
  - ≤ 300: bars re-spaced round the hole;
  - 300 – 600: the cut bars' area is added half each side (≥ 1-DB12), top and bottom;
  - ≥ 600: trimmers + diagonals.
  - Diagonals DB12 × 1200 (ACI SLAB-202; TATA's 700 / 1000 is shorter than Ld each side).
  - Cut top bars end in a standard hook down.
  - Openings not on the drawings need the engineer's approval.

---

## 4C-1. Table numbering (R2, 2026-09-30)

Every table carries "TABLE n - NAME". The general notes hold Tables 1 – 10; the typical details continue from 11 (register: `TABLES` in `td_engine.py`). Notes and leaders cite "TABLE n" only; a drawing number is never part of a table reference.

| No. | Name | Sheet |
|---|---|---|
| 11 | COLUMN TIES AND SPLICES BY FRAME TYPE | 1101 |
| 12 | MAXIMUM TIE SPACING (mm) | 1103 |
| 13 | COLUMN SCHEDULE CALL-UP (EXAMPLE) | 1103 |
| 14 | BEAM SCHEDULE (EXAMPLE) | 1115 |
| 15 | BEAM REINFORCEMENT BY FRAME TYPE | 1116 |
| 16 | PUNCHING SHEAR REINFORCEMENT RULES | 1123 |
| 17 | MINIMUM TRIMMING BARS AT SLAB OPENINGS | 1124 |
| 18 | SLAB-ON-GROUND JOINTS AND DOWELS | 1126 |
| 19 | SLAB THICKNESS AND REINFORCEMENT | 1128 |
| 20 | SUBGRADE, FILL AND BACKFILL UNDER SLABS ON GROUND | 1128 |

Cited from the general notes: Table 4 (hooks and bends), 6 (lap and anchorage length), 7 (minimum clear cover).

---

## 4D. ACI MNL-66(20) review (2026-09-29)

Four parallel reviews compared the ACI Detailing Manual (ACI 318-19 based) with our sets: beams, columns, slabs and slab on ground, and walls / foundations / general notes. The main claims were checked against our code digests before anything changed.

| Kind | What |
|---|---|
| Real errors fixed | 12-bar tie arrangement (unsupported bars); slab-step bars bent round the re-entrant soffit corner; deformed slab-on-ground dowels; perimeter-beam integrity understated |
| Tightened | Size-change hooks and the 75 limit; footing dowels; torsion; side bars; openings; cantilever back length; joints; general notes (design data, ld / ldc, bar supports, foundations) |
| Decisions | D1 – D5 as in §2 above (D5: option B, 2026-09-30) |
| Added | Sheet 1103 |

`REVIEW_ACI_MNL66.md` holds the full list and the proposed next work:
- beam, column and slab schedules with lettered bars;
- ~~secondary beam ending at a girder~~ (1114/3, 2026-09-30);
- ~~column supporting a discontinued wall~~ (1102/9, 2026-09-30);
- dropped balcony / wet-area slab;
- slab-on-ground corner and joint bars;
- the wall (113x) and foundation (114x) sheet plans.

**What we learned about using ACI here:**
- Apply ACI only where it states code-independent good practice, or label it as an office rule.
- Always compare with ACI 318-11, which EIT is based on, not only 318-19. The MNL-66 checklists sometimes print outdated values: its BM-104 item gives the ACI 318-08 SMF hoop spacing.
- DPT prints some values less strict than ACI (8 db / 300 beam hoops, 90° hooks). Such differences are the user's call (D1 – D5), never a silent change.

## 5. How the generator builds a sheet

> **Since 2026-09-29 the working generator is `jobs/standard_set/`** (model-space sheets built from blocks: each view is a `DET-<sheet>-<id>` block, the title block `TB-A3-NRW` carries attributes, one thin 1:1 layout per sheet; general notes 1001 included). Content modules and sheet layouts are written exactly as below; see `jobs/standard_set/MODEL_SPACE_SHEETS.md` for what changed. `jobs/typical_details/` is kept as the paper-space reference.

1. **Engine (`td_engine.py`):**
   - layers and pens, dimension styles;
   - the leader engine (`leader`, `note_cfg`, `capture`);
   - `bar`, `dot`, `zbreak`, `stirrup`, `crosstie`;
   - the title-block block and model-space sheets (`new_sheet`, `finish`);
   - `viewport` (inserts the detail block at 1/scale), `view_title`, `tbl`, `notes_block`, `wrap_s` / `glue`.

   `SHEETS` and `EXT` live here and are filled by the content module.

   **Checks built in**, each printing `!!` in the build log:
   - `check_dims` (clean dimensioning);
   - leader crossing a dimension;
   - detail outside the drawing area;
   - view-title note below the frame;
   - notes block below the frame;
   - table into the title strip.
2. **Content modules** (`gn_notes.py`, `td_columns.py`, `td_beams.py`, `td_slabs.py`): each sets `BASE` (the output file name) and `SHEETS`, defines the view functions, and has a `build()` that captures the views into `EXT` and calls the `sheet_xxxx()` functions.
3. **Views.** Each detail is a function drawing in **model space at full size**. Examples:
   - columns: `col_elev`, `sec_change`, `joint_plan`, `tie_types`, `circ_hoop`, `spiral_elev`, `couplers`;
   - beams: `beam_elev`, `stirrup_types`, `cutoff`, `cantilever`, `end_anchor`, `typ_section`, `sec_on_main`, `sec_end`, `levels`, `stepped_beam`, `web_opening`;
   - slabs: `short_section` … `sog_layout`.

   `capture(fn, ox, oy)` runs the function, lays out its leader notes, checks its dimensions and stores it as a block. Views sit 8 m apart in model space.
4. **Sheets** insert each detail block at its scale (`viewport(ps, key, scale, x, top)`), then titles, tables (`tbl`) and notes blocks (`notes_block`). The build log prints every placement and flags problems; adjust the view limits or panel widths until there is no `!!` line.
5. **Build and plot.** Plot from PowerShell, because the console cannot run scripts from Git Bash.

```bash
python build.py all
```
```bash
python plot.py all
```

The plot writes one PDF page per layout, a DWG, and one library DWG per detail block, and prints `font check OK` (or lists any non-Arial-Narrow font).

**To add a set** (e.g. walls 1131+): write `td_walls.py` on the pattern of `td_slabs.py` (`from td_engine import *`, `BASE`, `SHEETS[:] = [...]`, views, `build()`). Then add it to `MODS` in `build.py`, and add its `BASE` to `SETS` and its detail prefix to `SERIES` in `plot.py`.

---

## 6. Pitfalls met on 1101 / 1102

| Problem | Fix |
|---|---|
| Stray tie lines above or below a break line | Keep tie levels inside the view limits (filter to `ybot < y < ytop`) |
| Thai category letters print as garbage | Write B / C / D |
| View title overlapping its bubble | Title width from `text_w()` (patched in `view_title`) |
| Captions crossing a beam break line | View bottom must lie below the lowest beam soffit; captions below the view bottom |
| Four 1:25 panels wider than the sheet | Beam stubs 180, note width 25, lower column 650 in case 2; step panels by max(width, 76) |
| Notes spilling off a narrow view | Short leader texts (≤ 25 mm wide); longer rules go in the sheet notes or the table |
| Symbols (≤ ≥ ° – ρ Σ) print as Thai characters in CordiaNew | The source .py was re-saved through PowerShell 5.1 `Get-Content`/`Set-Content`, which reads UTF-8 as cp874. Edit sources only as UTF-8, and after plotting check that the PDF uses only ArialNarrow and ArialNarrow-Bold |
| Table cell breaks inside an expression (`(R = / 5)`, `hx ≤ / 350`) | `wrap_s` uses `glue()`, which keeps a relation (= ≤ ≥ ≈ + – ×) together with its operands |
| Plot shows an old drawing | Build with `python build_td.py out`; without the argument the DXF goes to the cwd and the plot reads the stale file in `out/` |
| View text at half (or double) size | The view function's `S` must equal the viewport scale it is placed at (e.g. a plan built with `S = 100` but placed at 1:200). Check every `capture` / `viewport` pair |
| Thai clause letters (จ, ค …) or ⊥ in note text | Not in Arial Narrow — they print in CordiaNew or blank. Write "13.3.8", "PERPENDICULAR TO". The plot's font check flags CordiaNew; a blank glyph is only seen by eye |
| Multi-line scripted edits through PowerShell arrays lost lines | Make edits with the Edit tool or a Python script file (`os.replace` from a `.tmp`) — never PowerShell `@(...)` arrays with `+` concatenated strings |
| ⅓, ⅕, ∅ print in another font | Not in Arial Narrow — write 1/3, 1/5, Ø. ¼ ½ ¾ ℓ √ ρ Σ φ ≤ ≥ ≈ are available (check new symbols with fontTools `getBestCmap()`) |
| `AttributeError: text_midpoint` in `capture` | A dimension with blank text (`text=" "`) — omit the dimension instead |
| A source file became empty | A script opened it for writing and then failed. Write to `file.tmp` and `os.replace()`, or use the Edit tool |
| Extension line crosses another dimension line; a centre line runs through dimension text (user comment on 1123/2) | Tier order: contained dimensions nearer the object; interleaved chains reduced, measured over the full width, or dropped; centre lines stop before the tiers; small dimensions with `tside`. `check_dims()` prints every case (ANNOTATION_ALIGNMENT_GUIDE §2.4.1) |
| Notes pushed far below the view, long diagonal leaders (1102/9 first draft) | The packer forbids a leader run on any horizontal drawing line between tip and knee: tips inside a tie / stirrup zone, or geometry (a wall) between the member and the note column | Put the tip **at the end of a tie, on a tie level**, or on a vertical leg; draw the other members on the side away from the notes |
| Leader of a lower note pushed far below a section (1115/2, D) | A dimension's extension lines lie in the band the run must cross | Remove or move the dimension if the data is given elsewhere (the schedule gives b × h) |
| A new label widened a view and pushed a neighbour's table into the title block (1103, type EH) | One long label line | Short label lines; 1103 now warns when its right-hand column is < 80 mm |
| Leader crosses a dimension (user comment on 1113/1 and 1114/2) | All chains on one side, notes on the other, rows held in the dimension-free band (`yminR` + `upR=True`, or `ymaxR`); see ANNOTATION_ALIGNMENT_GUIDE §5. The build log prints `!! leader crosses a dimension` for any that remain |
| Top and bottom 90° hook tails drawn on one line, so they read as a closed loop (user comment on 1111) | Tails side by side, each 12 db: bottom-bar tail 45 mm inside the top-bar tail (DPT Fig 5.2-12). A third hooked bar (e.g. an additional top bar) gets its own offset (`xh`, `xh + g`, `xh + 2g`) |
| View-title note touching the detail bubble (user comment on 1112/1) | `view_title` sets the note line below the bubble (`y − r − 1.6`); the log warns if it drops below the frame |
| Slash at a bar end not understood, then "messy" (user comments) | **Removed 2026-09-30**: bar ends are plain. The **BAR-END SYMBOLS** key (`bar_end_legend`) now shows: plain end = the bar stops; 90° hook; bar to a break line = continues; lap = cranked bar. 1111 note 7 and slab note 7 say the same |
| Dashed lines read as solid on screen and in print (user, 2026-09-30) | Chain linetypes at 0.7× the EIT patterns (centre 8.5 / 1.4) | Centre 12 / 2 / 2 / 2, phantom 10 / 2 …, match 13 / 2.5 … (= DRAWING_STANDARD §4.4); **hidden 3.0 / 1.5 and fine hidden 1.5 / 0.75 kept at the office values (user)**; centre / grid / reference lines on `S-CENT` 0.18, cutting planes on `S-CUTL` 0.25; notional lines (critical section) on `S-ZONE-DASH` fine hidden. Keep entity ltscale 1 |
| Laps drawn as two parallel bars (user: use a crank at the splice zone) | Offset bars without a crank | `lap_crank()` everywhere; see "Lap splices" above |
| Notes of the next view show inside a viewport | Views too close in model space - keep 8 m between view origins |
| Beam detail runs into the title strip | Narrow the view (shorter beam stub, note width 40 – 46) or move it to a row with more room; the log flags it with `!!` |
| Stacked dimensions cross; text hides behind a line (user comment on 1123/2) | See the clean-dimensioning row above; small dimensions use `dim(tside=...)` |
| 12-bar "two overlapping ties" left two side bars unsupported (ACI review) | A tie leg running past a bar does not hold it; only a tie corner or a crosstie hook does. Use the 1103 types (crossties on alternate bars) |
| Tension bars bent round a re-entrant (concave) corner (slab step, ACI SLAB-204) | The pull straightens the bar through the cover. Cross the bars instead: continue straight past the corner and anchor in the far face / top layer (stair-knee practice). Check every haunch, step and kink |
| Deformed dowels at slab-on-ground joints | They lock the joint. Use plain RB dowels, half greased or sleeved |
| A longer note or bigger view pushes a neighbour off the sheet (1102 title note, 1101 / 1111 / 1113 notes) | Every text change can ripple. Rebuild the whole set and read every `!!`; shorten wording, widen the notes block, or move notes to the sheet they belong with |
| A "*" in a table explained in a note on another sheet | Put the reason in the cell, or in a note on the same sheet |
| A table or notes block silently ran past the frame or into the title strip | `tbl` and `notes_block` now warn; do not ignore them |
| Build log crashes printing ≥ / ℓ / ≈ | The Windows console is cp874. `build.py` reconfigures stdout to UTF-8; use `PYTHONIOENCODING=utf-8` for ad-hoc scripts |
| A general-notes rule contradicts a detail (e.g. "stagger all laps" vs column laps at one level) | Write the exception into the general note ("U.N.O. …") when a detail departs from it |

---

## 7. Checklist before issue

- [ ] Every value in the table matches its source clause (EIT 011008 / DPT 1301/1302); symbols on the details match the table.
- [ ] No tie, bar or text crosses a break line, a viewport edge or the title strip; no `!!` in the build log (includes `leader crosses a dimension`).
- [ ] No leader crosses a dimension line, an extension line or dimension text (check by eye too: the log does not see dimension text).
- [ ] Clean dimensioning (ANNOTATION_ALIGNMENT_GUIDE §2.4.1):
  - dimensions contained in others sit nearer the object;
  - no extension line crosses a dimension line;
  - nothing runs through dimension text;
  - small dimensions use `tside`.
  - The build log shows no `!! <view>: …` dimension lines.
- [ ] Laps drawn inside the correct zone for each frame type; ties at s over special-frame laps.
- [ ] Stirrups wrap their corner bars; crosstie 90°/135° hooks wrap their bars and alternate; no tail clashes with the hoop hooks.
- [ ] View titles, bubbles (detail / sheet) and scales correct; references between 1101 and 1102 are right.
- [ ] PDF text contains no `?` (missing glyphs); the plot prints `font check OK`.
- [ ] Beams: 2h zones at every column face, first stirrup ≤ 50; laps outside 2h in seismic frames; bar ends plain (no slash); laps drawn cranked (`lap_crank`); cut-off points match the notes; hooks inside the column bars at the far side.
- [ ] Every tie arrangement holds every corner and alternate bar (tie corner or crosstie hook), and no bar is > 150 clear from a held bar.
- [ ] No tension bar is bent round a re-entrant corner (steps, haunches, kinks); crossing bars anchor past it.
- [ ] Values follow decisions D1 – D4. Anything taken from ACI is either code-independent or labelled as an office rule.
- [ ] Cross-references to the general notes (`1002 TABLE 6`, `SEE 1002`) still match: `build.py gn` lists the tables and sheets, and `TABLE_REFS` warns.
- [ ] Review each changed detail in the plotted PDF (`crop_det.py`), not only the build log.
