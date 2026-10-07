# RC Drawing Rules: reinforcement graphics, required content of RC plans and details
### Based on EIT Standard 011006-19 (วสท. 011006-19) *Reinforced Concrete Building Drafting Standard*, Rev. 1, March 2019

> The concrete-specific chapters of the EIT digest, split out on 2026-10-03 from
> `docs/general/DRAWING_STANDARD_EIT-011006-19.md`. That file keeps the rules for every structural drawing (sheets,
> lines, text, dimensions, levels, marks, callouts, numbering, office conventions §19). **Section numbers are kept**
> so citations stay valid: §12, §14, §15, §19.4, §19.7.
>
> Source tags are as in the general file: **[STD]** normative text, **[FIG]** observed in the standard's example
> drawings, **[DER]** derived, **[REC]** recommendation. The office conventions (§19.4, §19.7) govern over §12 –
> §15 where they differ.
>
> Related: annotation of bars (terminators, rings, bubbles) in `docs/general/ANNOTATION_ALIGNMENT_GUIDE.md` §2.1 –
> §2.3; typical-detail sheets in `TYPICAL_DETAILS_INSTRUCTION.md`; the concrete presentation approach in
> `docs/concrete/README.md`.

---

## 12. Reinforcement Graphics

### 12.1 Bar symbols [STD Table 3.1]. Draw bars "very thick".

| # | Meaning | Symbol |
|---|---|---|
| 1 | Bar | Thick continuous line |
| 2 | Bar in cross-section | Filled dot ● |
| 3a | Bar with **hook** (180°) | Line ending in a U-return |
| 3b | Bar with **90° bend** | Line ending in a right-angle leg |
| 4 | Bar **without** hook: marks the end of a straight bar lapping another in the same plane | Short **45° tick** at the bar end; or draw the two bars slightly offset and note the gap as `0`. **Office practice (2026-09-30): no tick — plain bar end; a lap is drawn as a cranked bar alongside the other (§19.4)** |
| 5 | 90° bend **away** from the viewer (crowded bars) | Bar end marked **×** (a plain end-dot is also shown) |
| 6 | 90° bend **toward** the viewer (crowded bars) | Bar end marked **○** (open circle) |

### 12.2 Drawing rules [STD Table 3.2]

1. **Standard bends**: draw hooks and bends to scale with the correct bend radius.
2. **Minimum-radius bends**: may be drawn as straight lines meeting at a corner.
3. **Bundled bars**: draw one line. Show the number of bars as short oblique strokes at each end (e.g. `\\\` … `///`).
4. **Bar set** (same type, size, spacing):
   - Draw **one** representative bar, very thick.
   - Cross it at right angles with a **thin distribution line** spanning the reinforced zone. Put terminators at both ends and a **small circle where it crosses the bar**.
   - Label: type, size, spacing, number (§12.3).
5. **Repeated groups**: sets placed in groups at equal spacing, with the same type, size and spacing. Show one representative and chain the distribution zones.
6. **One-way reinforcement in plan**: double-headed **open arrow** for the bar direction, plus a label.
7. **Two-way reinforcement in plan**: two crossed double-headed arrows, each labelled as for one-way.
8. **Two layers in plan**:
   - Add **T** (top) / **B** (bottom) at the bar ends.
   - If bars in the same layer have different lengths, show the **ends of the shorter bars** (with brackets).
9. **Two faces in wall elevation**:
   - Add **NF** (near face) / **FF** (far face).
   - If bars on one face have different lengths, show the shorter bar ends.
10. **Clarity**: if bars can't be drawn clearly inside the view, draw them **extracted beside** the view.
11. **Stirrups/ties**:
    - Draw them clearly.
    - Where ties overlap (multi-leg), draw each shape separately **with explanatory notes**.
    - Show the hook position.

### 12.3 Bar notation [STD §3.7, §1.2.2]

| Item | Notation | Example |
|---|---|---|
| Bar type (only when needed; otherwise state in notes/spec) | `RB` round, `DB` deformed, `R` re-rolled round | `DB12` |
| Size (no type given) | `φ` + dia (mm) | `φ12` |
| Spacing c/c | `@` + mm | `@150` |
| Number of bars | count + `-` + size | `4-DB16`, `4-φ12` |
| Square mesh, equal both ways | `#` | `5-DB16#` (5 bars each way) |
| Tie (เหล็กปลอก) | `ป.` | `ป. RB9 @150`; double ties `2ป.` |
| Stirrup (เหล็กลูกตั้ง) | `ล.` | `ล. RB9 @125` |
| Top / bottom layer | `T` / `B` | |
| Near face / far face | `NF` / `FF` | |

- **Steel grade** (SR24, SD40, etc.) goes **only** in the general notes and specification, not on each bar label. [STD §3.7.1]

---

## 14. Plan Drawings: Required Content [STD Ch. 5]

General rules:
- Plans are ordered piles → roof, following construction sequence.
- A drawing must be buildable **without guessing**: easy to read, simple, and never self-contradictory.

### 14.1 Pile plan (ผังเสาเข็ม) [STD §5.2, FIG 5.1], typically 1:100

**Must show:**
1. Grid
2. Pile positions in each footing
3. Pile type & size
4. **Pile-head level**
5. **Pile-tip level**
6. Concrete strength (bored piles)
7. Rebar yield strength

**Drawing practice [FIG]:**
- Pile: circle + cross (⊕), explained in the legend (e.g. "⊕ = bored pile Ø350 mm").
- Pile-cap outline: thin dashed, as a reference.
- Pile positions dimensioned from the grid lines (dot terminators on grids).
- **Pile-head level in a box** next to each group (e.g. `−3650`), with the box explained in the legend.
- Pile-tip level, f′c and fy given in the notes.

### 14.2 Footing / foundation plan (ผังฐาน) [STD §5.3, FIG 5.2]

**Must show:**
1. Grid
2. Footing positions & shapes
3. Footing marks `F1, F2…`
4. Footing levels
5. Column positions & marks
6. Basement walls, lift pits and other members, with marks (if any)

**Drawing practice [FIG]:**
- Footing edge: **continuous** (concrete outline).
- Column stub: heavier square with a "+" cross, with its mark (`C2`) beside it.
- Footing mark placed at the footing's lower-right.
- Common top-of-footing level given as a note (e.g. "Top of footing −300 mm").

### 14.3 Floor plans (ผังชั้นต่าง ๆ) [STD §5.4, FIG 5.3–5.5]

**Must show:**
1. Grid
2. **Column, beam and slab outlines**: solid where visible from above, **dashed where hidden** (beams and walls below the slab)
3. Column marks
4. **Beam marks + size** (e.g. `1B4A (200x400)`), written along the beam
5. **Slab marks + thickness**
6. Wall, lift-shaft, stair and other marks
7. **Openings/shafts: X across the void**
8. **Structural slab surface level** (or precast top level including topping)
9. Columns **continuing up**: solid section. Columns **ending below** this floor: **dashed**.
10. Where beams stack in one plan, give **both marks and the level of the lower beam**

**Drawing practice [FIG]:**
- Slab tag:
  - Mark in a **circle** (`1S3`).
  - Slab level in a **box** below it (`+500`).
  - Thickness in brackets where it differs from the typical: `(120 THK.)`.
- Beam tag: mark + `(b x h)` along the beam line. Rotate the text for vertical beams.
- Stairs: outline treads, `UP`/`DN` arrow, stair mark `ST1`.

### 14.4 Roof-deck / roof plan [STD §5.5, FIG 5.6]

**Must show:**
- Items 1–5 of §14.3 plus wall/other member marks
- Structural slab level
- **Slab fall for drainage** (`SLOPE` arrow)
- **Roof drain / rainwater outlet positions**

**Drawing practice [FIG]:**
- Parapets hatched, with size noted (`PARAPET (120x1200)`).
- Gutters indicated.
- Column stubs marked `CK`.

---

## 15. Member Details: Required Content [STD Ch. 6]

Details must be clear, complete, and consistent with the plans (Ch. 5).

### 15.1 Footings [STD §6.2, FIG 6.1–6.2]. At least **one plan + one section**.

**Plan must show:**
- Footing size
- Pile positions
- Reinforcement

**Section must show:**
- Footing size & thickness
- **Pile embedment into the cap**
- Blinding / sub-base thickness & material (lean concrete, compacted sand)
- Pile size & safe load
- Pile dowels (if any)
- Footing reinforcement
- Column / stub bar arrangement (*arrangement only*; bar sizes are not required)
- Notes including **concrete cover**

**Drawing practice [FIG]:**
- Scale 1:25.
- Section title with bubble, and footing title `FOOTING F1 (ฐาน F1)`.
- Dimension chain at the side: footing depth / embedment / blinding / sand.
- Column dowels (`เหล็กเดือย 6-DB12`) shown **dashed** inside the cap.
- Hoop ties `เหล็กรัดรอบ RB9 (2ป)`.
- Mat reinforcement labelled `5-DB16#`.
- Note: cover 50 mm.
- An alternative section is given for footings **not** tied by a ground beam.

### 15.2 Columns [STD §6.3, FIG 6.3–6.4]
Provide a **full-height elevation** (typical: bars and laps) plus a **column schedule**.

**Elevation must show:**
- Column between floors
- Floor levels
- Vertical bars & laps
- Ties
- **Position of first & last tie**
- Column mark
- Column section

**Schedule must show:**
- Floor levels
- Column marks
- Section sketch
- Size
- Vertical bars
- Tie size & spacing

**Drawing practice [FIG]:**
- The schedule is a grid: columns = C1…Cn, rows = floors (top → bottom). Each cell holds a section sketch plus rows for Size / Vertical bars / Ties.
- **Office rule (user, 2026-10-07: "I don't want table with context inside; I would like section put in the table"):
  column and beam schedules are drawn schedules - the member's section is drawn in the table cell, with only the size,
  bars and ties written under it. A text-only schedule table (the Beca template `Detail Schedule\Beam Schedule.dwg`)
  is not used. Reference: K.Nat house, `G:\My Drive\Works\20231129 - K. Nat\CAD\K.Nat_ST_Detail.dwg`, S2-06
  (column schedule) and S2-07 (beam schedule), the base to upgrade from. Worked example of the upgraded form: BANWA2 S-301 (typical
  column arrangement N.T.S. with tie zones A / B / C and Lo, column schedule at 1:25) and S-302 (beam schedule at 1:25,
  one band per level, the section columns of §15.3 per mark, slab drawn where the model has one), all bars read from
  the model's rebar data (`plans/rc_data.py`, `rc_schedules.py`).
- **Scale and the typical arrangement** (user, 2026-10-07: "keep all column, beam detail as 1:25; for column legend
  make it general symbol showing floor like representing, not to scale"): every column and beam section in the
  schedules is drawn at **1:25**; the typical column arrangement beside the schedule is a **generic N.T.S. diagram** -
  one representative storey between an UPPER FLOOR and a LOWER FLOOR (beam and slab), tie zones A / B / C with Lo, the
  lap at mid-height, first tie 50 mm - with no project level or size on it (BANWA2 S-301 view 1, `col_typical`).
- An **open up-arrow (⇧)** in a cell means "same as the floor below".
- In the elevation:
  - First tie **50 mm** from the slab faces.
  - Bars cranked at the lap above the slab.
  - Note: "in seismic zones lap bars at mid-height".

### 15.3 Beams [STD §6.4, FIG 6.5–6.7]
Provide a full-length elevation plus enough sections to show all bars. **Or** use a **beam schedule** when there are many beams.

**Elevation must show:**
- Supports & spans
- Top/bottom main bars (position, number, size)
- Extra bars
- **Cut-off points**
- Stirrup size & spacing
- Section-cut marks
- Beam mark

**Section must show:**
- Size
- Main bars
- Extra bars
- **Stirrup shape**
- Stirrup size & spacing
- Section ID

**Inner stirrup legs sit on bars** (user, 2026-10-07: "tie as shear reinf. need to place on rebar it could not
standalone"): a crosstie (third leg) or an inner stirrup (fourth leg) is shear reinforcement only where it hooks round
a longitudinal bar at both ends. In the drawn section it is placed on a bar position that exists in **both** the top
and the bottom outer layer, the one nearest the middle - never at b/2 when the layers have an even number of bars
(4 bars: on the second or third bar). If the top and bottom layers share no inner bar position, the bars are
rearranged before the section is drawn (a `!!` build warning). Worked example: BANWA2 S-302, B2 (4 + 4 bars, 3 legs)
crosstie on the third bar, B1A (4 legs) inner stirrup on bars 2 and 3 (`rc_schedules.beam_section`).

**Beam schedule** (office form, user 2026-10-07, see §15.2): one column per beam mark and support zone, the **section
drawn in each cell**, then rows for size, top bars, bottom bars, side-face bars and stirrups (K.Nat S2-07).
- **Section columns** (user, 2026-10-07: "add continuous span for all beam that end and middle span has different rebar
  by using end span rebar for continuous span"; "for beam which has same rebar all location collapse to one section as
  ALL SPAN and rebar no need to show + sign"):
  - a beam whose support and mid-span bars differ has three columns: **END SUPPORT | MID SPAN | CONTINUOUS
    SUPPORT** (CANTILEVER added where there is one). Where the design gives one support set per beam (the analysis
    model's I / J ends), the continuous support repeats the end support bars, and a note says so until the design
    check gives its own;
  - a beam with the same bars and stirrups throughout has **one ALL SPAN column**, its bars written as the total
    (`8-DB25`, not `4-DB25 + 4-DB25`): the drawn section shows the layers. Mixed bar sizes keep `a + b`;
  - the other columns keep `a + b` = outer layer + second layer, defined in the notes.
  - Worked example: BANWA2 S-302 (`rc_schedules.zones_of`, `bars_total`): B1, B2, B3, B5, B5A, RB5 in three columns,
    B1A, B6, RB1, RB2, RB5A as ALL SPAN.

**Beam schedule must show:**
- Mark
- Span
- Size
- Top/bottom bars (layer 1 & 2)
- Extra bars
- Stirrup shape / size / spacing
- **Bar-arrangement sketch with cut-off points**
- Remarks

**Typical cut-off diagram [FIG 6.7]**, an example only and not a code requirement:
- **Top bars**:
  - Layer 1 extends **L/3** past the support face (use the larger adjacent span).
  - Layer 2 extends **L/4**.
- **Bottom bars**:
  - Layer 2 stops **L/6** from interior supports and **L/8** from exterior supports.
  - Top-bar laps at mid-span.
- **Stirrup zones**:
  - **S2** (dense) near supports.
  - **S1** mid-span.
  - First stirrup **50 mm** from the column face.
- **Exterior anchorage**: standard hook (50 mm tail) or ℓd/ℓdh if insufficient.

### 15.4 Slabs [STD §6.5, FIG 6.8–6.10]

**One-way slab**:
- No plan reinforcement is needed.
- Show **one section along the short span**.
- Section must show: supports & span, thickness, bar size & spacing, cut-offs, slab mark.

**Two-way slab**:
- No plan reinforcement is needed.
- Show **two sections** (short and long span).
- Sections must show: supports & span, thickness, bars in both directions, cut-offs, slab mark.

**Flat slab** needs a plan plus enough sections.
- If congested, **split the plan into a TOP-bar plan and a BOTTOM-bar plan**.
- Plan must show:
  - Columns & spans
  - **Column-strip / middle-strip widths**
  - **One full-length representative bar per set**, with a distribution line to the outermost bar
  - Section cuts & marks
- Section must show:
  - Columns & spans
  - Thickness
  - Bar size/spacing per strip
  - Cut-offs
  - Section ID

**Drawing practice [FIG]:**
- Slab sections at 1:20.
- Top bars extend **L/4** (or fixed lengths, e.g. 1000 mm).
- Distribution (temperature) bars shown as dots, labelled `เหล็กรองรับ`.
- In flat-slab plans:
  - Show each bar direction in one half of the plan, divided at a symmetry line. Note that the plan shows one direction per half.
  - Draw column-strip and middle-strip bars at **different weights** to tell them apart.

### 15.5 Shear walls / cores [STD §6.6, FIG 6.11]

Plan required. One plan is enough unless bars change with height.

**Plan must show:**
1. Wall dimensions
2. Opening sizes
3. Wall thickness
4. Vertical & horizontal bar size/spacing
5. **Link (cross-tie) details & positions**
6. Other details
7. Wall mark

**Drawing practice [FIG]:**
- Scale 1:25.
- Boundary-element bars enclosed in a **dashed box** and labelled `เหล็กเสริมพิเศษ 8-DB16 (แบบฉบับ)` ("typical").

### 15.6 Stairs [STD §6.7, FIG 6.12–6.13]

- At least one flight in section.
- Spiral or dog-leg stairs also need a plan with the section line.

**Section must show:**
- Span
- Waist thickness, **tread & riser** dimensions (e.g. `9 ลูกตั้ง @ 175 = 1575`, `8 ลูกนอน @ 250 = 2000`)
- Reinforcement
- Handrail fixings (may be on the architectural drawings)
- Stair mark

**Drawing practice [FIG]:**
- Scale 1:25.
- Nosing bar shown.
- Landings with top and bottom mats.

---

## 19. Office conventions for reinforcement (from the general file's §19)

### 19.4 Reinforcement graphics (extend §12)

- Bars are drawn on their centreline with bends at R = 3.5 db, never sharp corners.
- Dots are true size, min. 1.1 mm. At 1:5, bars along their length are true-width filled strips.
- Plain dowels are outline only; end-on they are a circle with a cross.
- **Stirrups and ties wrap their corner bars:**
  - Each stirrup corner is an arc concentric with its corner bar, radius = bar radius + half the stirrup diameter, so the corner bars sit inside the bends and touch the stirrup.
  - Both 135° hooks turn around the **same** corner bar and run into the core at 45°, one on each side of the bar.
  - Hooks never cut across a corner away from the bar.
  - Helper: `stirrup()` in `jobs/general_notes/build_gn.py`.
- **Crossties wrap their bars too:**
  - The 135° and the 90° hook are each an arc concentric with the bar they engage, and the body runs tangent past the bars. A crosstie is never drawn from bar centre to bar centre.
  - Wrap radius is one tie diameter outside the hoop (≥ 0.5 mm on paper), so the 90° tail lies beside the hoop line and does not sit on top of it.
  - The 135° tail turns into the core, away from the hoop's own hooks.
  - Helper: `crosstie()` in `jobs/typical_details/build_td.py`.
- Footings use a closed C-bar at the toe when a 90° hook can't fit the depth.
- **Re-entrant (concave) corners** (stairs, slab steps, haunches, kinks): a tension bar is never bent round one. The bars cross, each anchored past the corner (office rule; ACI SLAB-204; applied on 1126 in 2026-09).
- **Column ties:** every corner and alternate longitudinal bar is held by a tie corner or a crosstie hook, and no bar is > 150 clear from a held bar. A tie leg running past a bar does not hold it (EIT 7.10.5.3; tie types on 1103).
- **Plain dowels** (slab-on-ground joints) are plain RB, half greased. Deformed bars lock the joint.
- Transverse bar sets are placed in alternate planes (shown in a bar-plane view).
- At small scale, dots are drawn clear of other bars, and bars at bends sit inside the bend.
- Spacing is written in mm (`DB12@200`, §3.7.3). Bar marks go in Ø4 bubbles.

### 19.7 Bar ends and lap splices (office rule, user 2026-09-30)
- **Bar ends are plain**: no slash / tick at the end of a straight bar on any drawing. A plain end means the bar stops; a bar drawn to a break line continues; hooks are drawn as bent.
- **Lap splices are drawn cranked**: the lapped bar runs offset alongside the other bar over the lap, passes the other bar's end slightly, then cranks back to its own line (1:3). Two parallel offset bars without a crank are not used for splices.
- Every sheet with elevations carries the bar-end key (plain end, hook, break, cranked lap).
