# Annotation Alignment Guide: Notes, Leaders, Terminators, Dimensions & Titles

- **Scope: every structural drawing, of any structure type.** This covers:
  - reinforced, precast and prestressed concrete, structural steel, composite, timber and masonry;
  - foundations, retaining walls, earthworks and stairs;
  - general arrangements, plans, elevations, sections and details at any scale.

  The rules are about how annotation is placed and read, so they do not depend on what is drawn. A rule that concerns
  one kind of object only (a reinforcing bar, a bolt, a weld) says so. §0 shows which parts apply to which structure.
- **Companions:**
  - `DRAWING_STANDARD_EIT-011006-19.md` covers *what* to draw: lines, pens, marks, callouts, EIT rules.
  - `SYMBOLS.md` catalogues every symbol: its form, layer, helper and rule.
  - `DRAWING_PRODUCTION.md` covers how a set is built, checked and plotted; `DRAWING_ENGINE.md` is the engine
    reference.
  - CAD setup (linetypes, pens, CTB): EIT §19.2 and `DRAWING_PRODUCTION.md`. The NRW job's own
    `NRW-ST_Linetype_and_Lineweight_Guide.md` is outside the repository (its `Drawings\` folder).
  - This guide covers *where and how* annotation is placed, so every sheet reads as calm, aligned columns of notes.
- **Content rules per structure type** say what a note, mark or table must contain; this guide says only where it
  goes:
  - concrete: `docs/concrete/README.md` (approach), `RC_DRAWING_RULES_EIT-011006-19.md` (bar graphics);
  - RC typical details: `TYPICAL_DETAILS_INSTRUCTION.md`;
  - staircases: `STAIRCASE_DRAWING_INSTRUCTION.md`;
  - general notes: `GENERAL_NOTES_DRAWING_INSTRUCTION.md`;
  - steel: `docs/steel/README.md` (approach), `STEEL_DETAILING_INSTRUCTION.md`.
- **Reference style:** "Life of an Architect" section details. Notes sit in tidy columns beside the detail, with leaders that leave the object at a standard angle and land on a short horizontal shelf.
- **Implementation:** the rules are coded in an *annotation engine*, so they are applied automatically. This document is also the manual rule set for anyone drafting by hand.
  - `jobs/nooker_rw/build_rw.py` is the original engine (NRW-ST).
  - `drafter/td_engine.py` is the current engine. It is used by the R2 typical details (RC) and the steel set SRT, and a new set of any structure type should import it. Its **orthogonal leader mode**, bolt rings and unit-safe wrapping are opt-in, so the R2 sheets are unchanged.
- **History.** The worked examples keep the sheet numbers of the job they came from.
  - §1 – §8 were written for the retaining wall NRW-ST Rev A (RC). Its views are kept as worked examples.
  - §2.4.1 (clean dimensioning) was added on 2026-09-29 on the R2 typical details.
  - On 2026-10-03, §2.4.2 (units on numbers) was added, and §2.1 gained the bolt ring and the arrow on the plate edge.
  - §9 was added on 2026-10-03 on the steel roof truss SRT-ST. Only §9.3 (welds) and the tube-node part of §9.5
    are steel-specific. Orthogonal leaders, tags, cutting planes, fitting views, detail callouts and labels on the
    member apply to every structure type.

## 0. Which rules apply to which structure

| Structure / drawing | Apply |
|---|---|
| **Every drawing** | §1 note columns and rows; §2 sizes, dimensions, clean dimensioning (§2.4.1), units (§2.4.2); §3 – §6; §8 "all drawings"; §9.1 leader style, §9.2 member tags, §9.4 cutting planes, §9.6 fitting views, §9.7 detail callouts, §9.8 labels on the member |
| **Reinforced concrete** (in situ, precast, slabs, beams, columns, walls, footings, stairs) | Bar terminators: an arrow on a bar drawn along its length, a ring on a cut bar (§2.1). Also bar-mark bubbles, bars at small scale (§2.3), construction joints and level marks (§2.5). Cast-in plates and anchors use the steel rows |
| **Structural steel and composite** | Bolt and plate terminators (§2.1), weld symbols (§9.3), dimensions at joints (§9.5). Shear studs and deck are named on themselves where they have a band (§9.8) |
| **Timber** | Bolt, screw and plate terminators (§2.1); members tagged (§9.2) or named on themselves (§9.8). Connector plates are annotated like steel plates |
| **Masonry** | Bar terminators for grouted cores and bed-joint reinforcement; ties and anchors use the bolt row (§2.1); level marks (§2.5) |
| **Foundations, retaining walls, earthworks** | Level marks, excavation slopes, soil and fill labels (§2.5), keep-out zones (§5) |

**Leader style: one per drawing set.**
- **Standard angle** (§1): an inclined 45° / 60° leg, a run and a shelf. Used on NRW, the R2 typical details, the stair
  and the general notes.
  - R2 variant (user, 2026-09-30): the leader form is chosen per target. A note aimed at a vertical line, a corner,
    a dot or an area is placed at its height and gets one horizontal leader. Only a target on a horizontal line gets
    the inclined leg (`_target_kind`, `_snap_tip`; `DRAWING_ENGINE.md` §6).
- **Orthogonal** (§9.1): straight, or an L with a real second leg. Used on SRT.
- A new set of any structure type may use either. The orthogonal style suits views where many targets sit close
  together, such as connections, framing nodes and congested reinforcement.
- Never mix the two styles on one sheet.

---

## 1. The five rules

1. **Text lives in columns (or rows), not at the target.**
   - All notes of a column share **one vertical edge line**.
   - Left column: right-justified. Right column: left-justified. The ragged edge always faces away from the drawing.
   - Rows (above or below a view) share one horizontal line.
2. **Leader = standard-angle leg + horizontal run + shelf.**
   - Target → **inclined leg at 45°** (60° if 45° doesn't fit; rows prefer 60°) → horizontal run → **3 mm shelf** → 1 mm gap → text.
   - **Never a random shallow angle:** a near-flat 5–20° diagonal is the "amateur" look. Standard angles follow ISO 128-22 / US NCS practice.
   - Each note is placed about **3 mm above** its target (`RISE`), so every leader gets a visible inclined leg.
   - A leader is a straight horizontal line only when the target is at text height.
   - The run always approaches the text from the side *away* from it. It never doubles back over its own note; if it would, the leader goes straight to the knee.
   - A horizontal run never lies within **1.5 mm** of a horizontal drawing line (bar, face, level line, ground).
3. **Notes are in the same order as their targets.**
   - Top-to-bottom (columns) or left-to-right (rows), so leaders don't cross. If two paths cross, the engine swaps those notes.
4. **Uniform rhythm.**
   - One text height (2.0 mm), one line pitch (3.33 mm) and a **1.6 mm** gap between notes.
   - Each note sits as close as possible to its target's height. Colliding notes are pushed apart as a group, centred on their targets.
5. **Nothing overlaps.**
   - Notes never sit on geometry, hatch, dimensions, level marks or other notes.
   - Leaders never run along a drawing line, never cross a dimension line, and never end inside a black object.

---

## 2. Annotation dimensions (paper mm)

| Item | Value | Engine constant |
|---|---|---|
| Note text | Arial Narrow **2.0 mm**, ALL CAPS | `TXT_H` |
| Headers, view titles | Arial Narrow Bold **2.8 mm** | – |
| Line pitch | 3.33 mm (MTEXT spacing factor 1.0 = 5/3 × height) | `PITCH` |
| Gap between stacked notes | 1.6 mm | `NGAP` |
| Shelf (horizontal landing) | 3.0 mm | `SHELF` |
| Shelf → bubble / text gap | 1.0 mm | `TGAP` |
| Rise of note above target | 3.0 mm | `RISE` |
| Leg angles | 45°, then 60° (rows: 60°, then 45°) | `LEG_ANGLES` |
| Run clearance from horizontal lines | 1.5 mm | `HLINE_CLEAR` |
| Bar-mark bubble | Ø4.0 mm on `S-SYMB`, number 2.0 bold (1.7 for two digits) | `BUB_R = 2.0` |
| Column width (wrap) | Section A: left 36 mm, right 44–50 mm; details 26–52 mm | per `leader(..., width)` |
| Column clearance | ≥ 5 mm from the drawing; outside dimensions and levels | `note_cfg` |

Text is wrapped using the **real glyph advances** of Arial Narrow (average ≈ 0.65 × height per character), measured from `C:\Windows\Fonts\ARIALN.TTF`. The MTEXT box is set to the measured width, so AutoCAD never re-wraps it.

### 2.1 Leader terminators

| Target | Terminator | Rule |
|---|---|---|
| **Bar drawn along its length** (vertical and horizontal bars, C-bars, U-bars, L-bars, 1:5 strips) | **Filled arrowhead, 2.0 mm long** | Tip on the bar's **edge** (`ARROW = 2.0`) |
| **Bar cut in section** (longitudinal bars, verticals in plan, dowels end-on) | **Open circle ("blank dot"), Ø = 2 × drawn bar-dot diameter**, centred on the bar | Leader starts on the circle's edge (`RING_K = 2.0`). Examples: DB12 at 1:10 → Ø2.4; DB10 at 1:10 → Ø2.2; any bar at 1:20 → Ø2.2. |
| **Bolt, anchor, screw or hole seen end-on** (steel, timber, precast fixings, anchors cast into or drilled into concrete) | **Open circle, Ø = 1.25 × the HOLE size**, centred on the bolt (Ø22 hole → Ø27.5; Ø33 rod hole → Ø41) | Tip given at the bolt **centre**; the leader starts on the circle's edge: `leader(..., bolt=hole Ø)` (`BOLT_RING_K`), user rule 2026-10-03 |
| **Plate, tube, member or panel** (any material: steel plate, cast-in plate, timber member, precast panel) | Filled arrowhead, 2.0 mm | Tip **on the plate edge** or outline, never inside the plate area (user rule 2026-10-03) |
| Concrete edge, surface, line, pipe, fill or soil area | Filled arrowhead, 2.0 mm | Tip on the edge or line, or inside the area for hatched regions |
| Point inside an area (optional) | Filled dot Ø0.7 mm | **Not used for reinforcement** |

### 2.2 Arrow tip on the edge, never inside black

- A tip must never disappear into a filled object: black bar strips, thick bar lines, solid sealant, solid dots.
- The engine (`edge_tip`) slides the tip back along the leader until it leaves every solid fill and every bar line. A bar line counts as centreline ± half its plotted pen. The tip then stops **0.05 mm** outside (`EDGE_GAP`).
- For outline-only objects (plain dowels, pipes), aim at the outline itself, not the middle.

### 2.3 Bars at small scale

- At 1:20 and smaller a bar dot is drawn at the **1.1 mm minimum**, larger than true size.
- Vertical-bar dots are placed **clear** of horizontal bars and bends: dot edge ≥ 0.3–0.4 mm from the bar line.
- Bars at a U-bend or L-bend sit **inside the bend**, touching its inner face, e.g. the free-end verticals at ±60° inside the U (3/5004).
- The view carries a note "… DRAWN OFFSET FOR CLARITY".

### 2.4 Dimensions (dimension style: `dimstyle()` in `td_engine.py`; EIT §19.3)

- **Terminators:** **filled arrowheads, 2.0 mm** (`DIMBLK` closed filled, `DIMASZ 2`, `DIMTSZ 0`). This is a project preference; EIT §3.2.3 permits arrows (its figures show 45° ticks).
- **Colour:** dimension lines and text plot black. **Extension lines are ACI 8 grey** (50 % screened), like grid lines.
- **Extension lines:** 1 mm gap from the object, 2 mm beyond the dimension line.
- **Text:** 2.0 mm, above the line and aligned. In narrow spaces the arrows and text go outside.

### 2.4.1 Clean dimensioning (user rule, 2026-09-29: "avoid crossing each other and making dirty dimensioning")

This applies to every drawing.
- **Tier order:** a dimension whose span lies inside another's sits **nearer the object**. Lap zone inside zone chain inside overall; Ld/3 inside Ld; capital inside drop panel.
  - So no extension line crosses a dimension line. Shared end points (chains, baselines) are fine.
- **Nothing runs through dimension text:** no geometry, centre line, hidden line, bar, tie, or other dimension.
  - A centre line stops before the dimension tiers.
  - Dimensions sit clear of dashed outlines (e.g. below a drop panel outline, not on it).
- **Small dimensions** (text wider than the gap) put their text **outside, on the free side**, in line with the dimension line beyond the arrow tail: `dim(..., tside="L"/"R")`. Never centred over a face line.
- **When two chains interleave** (points of each fall inside the other's spans), no tier order works:
  - reduce one to what it must show, e.g. a single "SPLICE ZONE, CENTRE Hc/2" instead of Hc/4 – Hc/2 – Hc/4;
  - measure it over the full width, e.g. "DROP ≥ L/3 (L/6 EACH WAY)" instead of a half from the centreline;
  - or drop it where the note and another detail already give it (drop panel on 1122 → note + 1123/2).
- **Extension lines start clear of other text.** A long dimension over a chain (e.g. "8125 (FIELD SPLICE)" over the 1250 panels) starts its extension lines just below the chain, not at the object, so they never pass through the chain's text.
- **Requirements belong in the notes, not in dimension text.** Write "≥ 156 (K3.1A)" in the general notes. The dimension shows only the value (159), so it stays short enough to sit between its arrows.
- **One dimension, one place.** If a plan already dimensions a plate and its holes, the elevation and the section do not repeat them. Repeated chains are what end up crossed by leaders.
- **Inclined chains** (e.g. along a diagonal) use `dim(..., angle=member angle)`, with every link offset the same distance from the axis. The check treats collinear links as a chain, not a crossing.
- **Check:** `check_dims()` runs in `capture()` for every view. It prints `!! <view>: extension line of 'A' crosses dimension line 'B'`, `dimension lines 'A' and 'B' cross`, and `<layer> line runs through the dimension text 'A'`.
  - Hatch fill (`S-HATCH`), weld hatch (`S-WELD`) and hatch boundaries on `Defpoints` are not counted as lines.
  - A sheet is not finished while one appears.
  - To review, crop the plotted detail: `python crop_det.py <set> DET-xxxx-n`.

### 2.4.2 Units on numbers (user rule, 2026-10-03: "add unit to all bare number for clear detail presentation")

This applies to every drawing. **Every measured value in a note, leader, title, key or legend carries its unit**:
- mm, m, kN, kPa, MPa, °, t, kg, % and µm;
- e.g. "GROUT 30 mm", "PROJECTION 100 mm", "SLOTTED 12 mm WIDE x 105 mm LONG", "TOP OF CONCRETE = BL - 0.030 m",
  "Fy ≥ 235 MPa, Fu ≥ 400 MPa", "LEG 6 mm, LENGTH 100 mm";
- a range or list carries the unit on each value, or once at the end of a list of the same quantity ("L = 8 / 6 / 5 mm").

These stay bare because a convention already gives the unit:
| Item | Why bare |
|---|---|
| Dimension figures, including labelled ones ("8125 (FIELD SPLICE)", "a = 40") | General note "DIMENSIONS IN mm, LEVELS IN m" |
| Weld symbol sizes and lengths | Weld key: "SIZES = FILLET LEG mm" |
| Section, plate, bolt, bar and hole designations (CHS 76.3 x 2.8, PL 10 x 70, M20, Ø22, DB12@200) | Standard designation form |
| Table cells | The **column header** carries the unit ("LENGTH mm", "e mm (e/D)", "GAP mm", "T kN"). Exception: the weight per length written after a steel section is part of the designation and keeps its unit in the cell, "PG 139.8x4.5 (15.01 kg/m)" (user, 2026-10-07; steel S3.8) |
| Diagram ordinates | The view title carries the unit ("CAMBER DIAGRAM (ORDINATES mm, ...)") |
| Counts, ratios, grades and references | Not measurements: "2 PER TRUSS", "e/D ≤ 0.25", "GRADE 8.8", "TABLE 3", "5002", "AISC 303 7.10" |

Check: before issue, scan the DXF texts for numbers with no unit and no designation in front of them. Every hit must
be one of the bare kinds above.

**A number and its unit never split across two lines** ("PITCH 60 / mm" is wrong).
- `drafter.fonts.wrap(..., keep_units=True)` glues them.
- A project opts in with `td_engine.WRAP_UNITS = True`; SRT does.
- The R2, NRW and other existing sets keep their current wrap until they are revised, so their issued line breaks do
  not move.

### 2.5 Symbols drawn with the notes

The full catalogue, with layers and helpers, is `SYMBOLS.md`. The symbols below are the ones that sit among the notes.

| Symbol | Drawing |
|---|---|
| **Construction joint** | Zig-zag on `S-CJOINT` 0.25, tooth pitch 2.0, amplitude ±0.8 (Section A stem/footing joint, joint-face view, legend on 1001) |
| **Excavation slope** | Dashed grey line (`S-EXCV`) with a slope triangle on the fill side: vertical leg **2** and horizontal leg **1** (unit 50 mm), numbers 2.0 mm next to the legs |
| **Level mark** | Open datum triangle, apex on the line (w 2.4, h 2.0), with value and description 2.0 mm above the line (e.g. `+0.600  TOP OF WALL`), **outside** the section, on the boundary side |
| **Break line** | Straight line with a single Z (EIT Table 2.3) |
| **Section / detail bubble** | Ø9.2 split circle: ID 2.8 bold above, sheet 2.0 below; filled triangles for sections |
| **Cutting plane** (any structure, §9.4) | Heavy end strokes outside the object, arrows to the viewing side, label `n/sheet` |
| **Member tag** (any framed structure, §9.2) | Mark in a circle (Ø ≥ 4.8, fitted to the text), beside its member |
| **Weld symbol** (steel, and welded inserts in any structure, §9.3) | AWS A2.4 reference line + arrow; symbols on `S-ANNO`, text 2.0 |
| **Detail callout** (any structure, §9.7) | Dashed circle (`S-CALL`, 0.25) round the enlarged part; a leader landing on its edge; note "DETAIL n/sheet - WHAT" |

---

## 3. How the leader attaches to the text

| Layout | Text grows | Leader attaches to |
|---|---|---|
| Right column | Downward, left-justified | Middle of the **first** line |
| Left column | Downward, right-justified | Middle of the **first** line |
| Row below the view | Downward | Middle of the **first** line |
| Row above the view | Upward | Middle of the **last** line (nearest the view) |

---

## 4. Choosing a layout

| View shape | Layout | Rule of thumb |
|---|---|---|
| Tall section / detail | **Two columns** (L + R) | Split by the side of the object the target is on |
| All targets near one side | **One column** on that side | – |
| Long, flat detail (horizontal bars, strips, joints in plan) | **Rows** above and/or below | If a column leader would run parallel to the line it points at, use a row |
| Detail with one free quadrant | **Column restricted** to that quadrant (`yminR` / `ymaxR`) | – |
| Long plan / elevation at 1:100 | Hand placed on a common row (`free=True`) | Too long for side columns |

### 4.1 Worked example: layouts on the retaining wall NRW-ST Rev A

The same choices apply to any structure. Steel examples (SRT-ST) are in §9.

| Sheet / view | Scale | Layout | `note_cfg` (model mm, view origin) |
|---|---|---|---|
| 5001 Section A | 1:10 | L + R columns | `xL = −330`, `xR = XRB + 60 = 1710`; `avoidL` bands at the 5 level lines (−8 … +34) |
| 3001 Plan / elevation | 1:100 | hand | `free=True` |
| 3001 Partial elevation at E.J. | 1:25 | rows T + B | `yT = TOW + 330`, `yB = KBOT − 180` |
| 5002 / 5003 E.J. / C.J. plan section | 1:5 | rows T + B | `yT = TS + 120`, `yB = −100`, `xmaxT = xmaxB = L1 + 40` (row kept inside the view width) |
| 5002 Slip dowel | 1:5 | row B | `yB = −110` |
| 5002 E.J. sealant / 5003 groove | 1:2 | column L | `xL = −80` |
| 5003 Joint face | 1:20 | column R | `xR = 1330` |
| 5004 Corner plan | 1:20 | column R, restricted | `xR = 1350`, `yminR = 1330` (free quadrant above leg A) |
| 5004 Corner-block footing | 1:25 | column R + row T | `xR = LA + 150`, `yT = LB + 250` |
| 5004 Free end | 1:20 | column L | `xL = −250` |
| 5005 Bar planes | 1:10 | row B | `yB = −170` |

---

## 5. Conflicts and keep-out zones

- **Level marks** go on the side opposite most notes. If they share a side, reserve a band per level (line −0.8 mm to text top +3.4 mm; `avoidL`).
- **Height dimensions** go on the level extension lines, outside the note column.
- **Dimensions that duplicate another detail** are left off where they would be crossed (e.g. 300/20/300 dowel dimensions appear only on 2/5002).
- **Surcharge, fill lines and side labels** ("RETAINED SIDE", "FILL LEVEL") stay inside the drawing footprint, clear of the column lanes.
- **Labels that don't fit:** if a label can't fit between bands or neighbours, shorten it and move the detail into the general notes or the reinforcement key. For example, (5) is "DB12@200 C-BAR, CLOSED AT TOE" in the section; "top & bottom legs" is in the key.
- **Leaders through reinforcement:** from inside the footing, leaders to the right column must pass **above** the top of the key U-bar (−0.250). Target the top leg of (5) and the rightmost top bar of (6).
- **Keep rows inside their view** (`xmax`) so they never run into the installation-note block beside the view.
- **A leader never crosses a dimension line, an extension line or dimension text** (user rule, 2026-09-29). A leader across a dimension reads as part of it. How to lay out a view:
  - Put every dimension chain on **one side** of the view, and the note column on the other. On beams: chains below, notes right and above the soffit. On columns: chains left, notes right.
  - When chains measure different bars, label each row (`TOP BARS`, `BOTTOM BARS`) instead of splitting them above and below.
  - A dimension that can only go between the drawing and its notes is dropped. Its value goes in the note text instead (e.g. "CLEAR ≥ 25 AND ≥ db").
  - Keep the note rows in the dimension-free band: `note_cfg(yminR=…, upR=True)` packs upward from the lowest tip and never goes below the floor; `ymaxR` sets a ceiling.
  - Keep views far enough apart in model space that no viewport window shows a neighbour's notes.
  - **Check:** `capture()` collects every dimension and extension line. Note rows avoid them, and any leader that still crosses one prints `!! leader crosses a dimension: '<note>'` in the build log. A sheet is not finished while that line appears.

---

## 6. Titles and text blocks

- **View title:** left edge aligned with the **left edge of its view**. Underline 2.8 mm bold, **6 mm below** the view's lowest annotation. "SCALE 1:n" on the next line, then an optional qualifier (e.g. the cover statement). Split bubble at the right end of the underline (EIT Fig 2.9 / 2.10).
- **Spacing:** at least 10 mm between a title and the next view below.
- **Note blocks** (general notes, keys, installation notes, schedules): left-aligned columns on a common top line. Headings 2.8 bold, body 2.0, line spacing 1.1–1.15.

---

## 7. The engine (`build_rw.py`; current: `td_engine.py`)

The calls below are the same in `drafter/td_engine.py`. A new set of any structure type imports that engine
and sets its options (`LEADER_ORTH`, `WRAP_UNITS`) in its own engine module, as `srt_engine.py` does.

1. A view function calls `leader(sp, target, knee_hint, text, S, side, width, mark=…, ring=db)`. Inside `capture()` the note is **collected**, not drawn.
   - `side` = `L` / `R` (columns) or `T` / `B` (rows);
   - `mark` = bar-mark number for the bubble;
   - `ring=db` gives an open-circle terminator for a cut bar of diameter db.
2. `note_cfg(...)` sets the layout once per view:
   - `xL` / `xR`: column lines;
   - `yT` / `yB`: row lines;
   - `avoidL` / `avoidR`: keep-out bands;
   - `yminR` / `ymaxR`: vertical range;
   - `xmaxT` / `xmaxB`: row right limit;
   - `free=True`: hand placement.
3. After the view is drawn, `capture()` collects the view's horizontal line segments, solid fills and bar lines, then `_layout_notes()`:
   - wraps each note with real font metrics;
   - sorts notes by target position;
   - packs them 1-D (clustered around their targets, with `RISE`), avoiding keep-out bands and horizontal-line strips;
   - clamps rows to `xmax`;
   - swaps any pair whose leader paths cross;
   - draws each note: `leader_path` (45° / 60° leg + run), `edge_tip`, terminator (arrow or ring), shelf, bubble, MTEXT.
4. The exact text boxes are added to the view extents, so the viewport and its title clear all annotation.

**To annotate a new view:**
- pick a layout (§4);
- call `note_cfg` once;
- add `leader(...)` calls in any order;
- never hand-place knees in column or row modes.

---

## 8. Checklist (per view, at print size)

**All drawings, any structure type**
- [ ] Notes form straight columns or rows with a common edge; left text right-justified, right text left-justified.
- [ ] One leader style per set (§0): standard angle (45° / 60° leg + horizontal run + 3 mm shelf) or orthogonal
  (straight, or an L with a vertical leg ≥ 3 mm, §9.1). No shallow random angles, no crossings, no run doubling back
  over its text.
- [ ] No leader along or on a drawing line, and none crossing a dimension line or an object it doesn't point at.
- [ ] Note order matches target order; notes sit near their targets.
- [ ] Filled 2 mm arrows on edges, surfaces and outlines, with tips on the **edge**, never inside black or inside a
  plate or panel.
- [ ] Dimensions with filled 2 mm arrows; extension lines grey.
- [ ] Clean dimensioning (§2.4.1):
  - contained dimensions sit on the inner tier;
  - no extension line crosses a dimension line;
  - nothing runs through dimension text, and centre lines stop before the tiers;
  - small dimensions have their text outside (`tside`);
  - no `!! <view>: …` dimension warning in the build log.
- [ ] No text on hatch, geometry, level marks or dimensions.
- [ ] Every measured value in notes, leaders, titles and keys has its unit; table headers carry the units (§2.4.2).
- [ ] Member tags circled and beside their members (§9.2); a cutting plane on the parent view of every section (§9.4).
- [ ] Every enlarged part has a dashed callout, a leader landing on its edge in clear space and a note
  "DETAIL n/sheet - WHAT" (§9.7).
- [ ] Members with a clear band are named on themselves, and no leader runs through that text (§9.8).
- [ ] View title left-aligned to its view, ≥ 6 mm clear of the lowest note; no view outside the drawing area (§9.6,
  `!!` in the build output).

**Reinforced concrete and reinforced masonry**
- [ ] Filled 2 mm arrows on bars drawn along their length; open circles (Ø = 2 × bar dot) on cut bars.
- [ ] No bar dot touching another bar line or bend.
- [ ] Bar-mark bubbles all Ø4, on the shelf.
- [ ] Construction joints drawn zig-zag; excavation slope with its 2 : 1 triangle.

**Steel, timber, fixings and inserts**
- [ ] Bolt, anchor and screw leaders aim at the centre with an open circle of 1.25 × the hole (§2.1).
- [ ] Every weld shown by a symbol, its reference line in free space, none inside the note column; one symbol per
  member mark at a node (§9.3).
- [ ] Set-out and gap dimensions clear of member axes (§9.5).

---

## 9. Orthogonal leaders, tags, symbols and callouts (all structure types; first used on SRT-ST, 2026-10-03)

These rules were developed on the steel roof truss, and the examples cite its sheets. Everything except §9.3 (welds)
and the tube-node part of §9.5 applies to any structure type. Where it helps, an equivalent in another material is
given.

### 9.1 Orthogonal leader mode (`td_engine.LEADER_ORTH = True`)

User rule: leaders never cross. A leader is a single straight segment at 0 / 90 / 180 / 270° where it can be, or a
two-segment orthogonal L. An inclined leg is only the fallback. A project opts in by setting the flag in its engine
module, as `srt_engine.py` does. The R2 sets keep the inclined style of §1. A new set of any structure type may opt in;
keep one style per set (§0).

1. **Shapes, best first** (`_shapes`):
   - one straight segment (target level with the knee, or directly below or above it);
   - an L: a vertical leg from the target, then a horizontal run to the shelf;
   - the §1 standard inclined leg;
   - the direct line.
   - A shape that would run along a drawing line is dropped.
   - **An L must have a real second segment** (user rule, 2026-10-03). Its vertical leg is at least `ORTH_LEG_MIN =
     3.0` mm; a shorter L reads as a hooked line and is not used. A note aimed at a horizontal edge is placed
     `ORTH_RISE = 5.0` mm off it, on the free side away from the object (`_rise`). That is the side with fewer drawing
     lines just beyond the edge: below a chord's bottom outline, above its top outline.
   - When packing still leaves a ringed target (bolt) too close to its note's height for a proper L, the standard 45°
     leg leaves the circle instead.
2. **Routing** (`_route`):
   - Notes are routed shortest leader first.
   - Each takes the first shape that crosses no leader already routed, no dimension or extension line, and no other
     note's text.
   - It may not cross **its own text** either: only the shelf may touch it.
   - If every shape conflicts, the one with the fewest conflicts is drawn, and the build prints `!! leader crosses
     another leader or a note`.
3. **Rows in tiers** (`place_tiers`):
   - In a row above or below a view, every note keeps its knee straight above or below its target, so its leader
     is one vertical line.
   - Notes are placed from the right, each in the nearest tier where its text fits.
   - So a vertical leader only ever passes **left of** the texts of the tiers it crosses, never through them.
4. **Swapping**: after placing, any pair whose previewed paths cross (`_preview`) is swapped and placed again, as in
   §1 rule 3.
5. **What counts as an obstacle**:
   - `capture()` collects the drawing segments for the routing.
   - Hatch fill, viewport frames, weld hatch (`S-WELD`) and hatch boundaries (`Defpoints`) are skipped. A leader may
     cross a weld band; it may not cross a drawing line it runs along.
6. **When a leader still can't be routed**:
   - Move its tip to another visible part of the same object. For example: the knife plate outside the tube rather
     than inside it; the far face of a member on the column side.
   - Or merge the note into a neighbour's. For example, the plate washer note joined the anchor rod note on 4/5002.
   - Do not shorten the rule.

### 9.2 Member tags

This applies to any framed structure: RC beam and column marks (B1, C1), steel members, timber members and precast
units. Use the project's mark scheme; the circle and the placement rules are the same.
- The mark is in a circle (`tag`, radius fitted to the text, at least 2.4 mm), on `S-SYMB`, with the text in bold.
- It is placed **beside** its member, never on its middle (`place_tag`):
  - candidates sit at 30 – 70 % of the member length, both sides, one gap (1.0 mm) clear of the outline;
  - the candidate kept is the one with the largest clearance from every member outline and every tag already placed.
- Trusses: chord tags sit outside the truss, at mid-panel, one per shop-piece mark (TC1, TC2, BC1, BC2). Frames:
  beam tags above or below the beam at mid-span, column tags beside the column at mid-height.
- **No node numbers** on a general elevation (user rule). Tables refer to "panel points counted from the pin end".

### 9.3 Weld symbols (`drafter.steel.weld`): steel, and welded inserts in any structure

This also covers cast-in plates, embeds and anchor plates in concrete, and steel connectors in timber.

What the symbol says is set by `STEEL_DETAILING_INSTRUCTION.md` §S5. Placement rules:

1. **Where the reference line goes**
   - Reference lines are horizontal, in **free space on the side away from the note column**. Notes are usually at
     the right, so welds usually run left (`left=True`).
   - Never put a weld symbol inside the note column or across a dimension tier.
   - Stack several symbols at different heights in the free corner, at least 8 mm apart (paper). One example is the
     cap / V1 / saddle / stiffener group on the left of 4/5002.
2. **The arrow**
   - It runs from the junction to the joint and is never collinear with the reference line.
   - Aim it at the weld itself: a hatch band, the toe of a branch, the edge of a plate.
   - One symbol may carry several arrows (`tip=[...]`) when the same weld occurs at several joints of one view. An
     example is the stiffener to the saddle and to the base plate.
3. **One symbol per member mark at a node**:
   - the first mark from the left gets a symbol at its left toe;
   - the next mark gets one at its right toe.
   - Repeated members carry no symbol of their own (the 5001 notes say the welds apply to every node of that type).
4. **Text**
   - 2.0 mm.
   - Size left of the symbol, length right of it.
   - Test letters ("MT") beyond the length.
   - The tail text ("4/5001", "SEAL", "TYP. BOTH LUGS") stays short. Use "2 EDGES", not "BOTH SLOT EDGES", where space
     is tight.
5. **Leader text does not repeat the weld.** A leader names the part, size and mark ("SADDLE PL 12 x 200 (p2), 120°").
   The symbol carries the weld.
6. **Key**: sheet 1001 shows every symbol form used, with descriptions starting 50 mm from the symbol (clear of the
   tail), and a wrapped footnote for the conventions.

### 9.4 Cutting planes (`drafter.steel.cutmark`)

Every section of any structure type has its cutting plane on the parent view: a wall section on the plan, a beam
section on the frame elevation, a truss section on the truss elevation.

- **End strokes only** (`ends_only=True`): heavy strokes **outside** the object, with arrows of 4.5 × S to the
  viewing side. Sections look left or down. The chain across the view is left out, so it never cuts notes or members.
- **Label placement**:
  - `lab="end"`: "n/sheet" beyond the end of the plane. This is the default; use it when the area beyond the ends is
    free.
  - `lab="side"`: the number above the arrow and the sheet below it, beyond the arrow tip. Use it when the ends are
    close to a dimension tier, as on the 1:50 elevation, where the plane ends between the chord and the panel chain.
- Put the ends past the farthest part of the object (a vertical cut through a bearing ends above the break of the
  vertical and below the RC break), never on a member.
- The section's view title names its parent, e.g. "SECTION 2 (ON 4/5002)".

### 9.5 Dimensions at member joints (worked example: hollow-section truss nodes)

The e, gap and set-out bullets are specific to welded tube trusses. The rest apply to any joint, such as an RC
beam-column joint, a timber connection or a precast connection:
- dimension on the side away from the note column;
- keep one chain per inclined member;
- move the values into the note when a chain would lie between the part and the notes;
- order the tips like the notes;
- dimension a layout once.

- **Eccentricity e:** a vertical dimension left of the branches, from the chord axis to the WP. The text goes inside the
  chord, on the side **away** from the WP: below the axis at a top node, above it at a bottom node. It then clears the
  chord outline.
- **Gaps:** dimensioned on the chord face, inside the chord band (a quarter of D from the face). The text goes on
  whichever side of the gap is farther from every branch axis that runs to the WP. Otherwise an axis line cuts the
  figure.
- **Set-out stations:** each branch axis on the chord face is measured from the panel-point line through the WP. Put
  them on the **far side of the chord**, measured between points on the far face. Their extension lines then never
  cross the gap dimensions. The panel-point line is drawn outside the chord only.
- **Along an inclined member**: one chain, all links at one offset on the side away from the neighbouring member.
  Keep only what the fitter needs (face → bolt, pitch, bolt → tube end). Fold short pieces into one link rather than
  stacking 20 / 40 / 60 figures.
  - If that chain would lie **between the part and the note column**, every leader to the part must cross it. Drop the
    chain and write its values in the note (§5). For example, on 2/5003 the bolt note reads "HOLES ON THE AXIS: FIRST
    90 FROM THE CHORD FACE, PITCH 60; TUBE END 60 BEYOND".
- **Order the tips like the notes.** Choose each tip on its part so the tips run top to bottom in the same order as
  the notes. Use the edge that faces the note column. On 2/5003 the order is tube outline, knife plate upper edge,
  bolt centre, gusset right edge, chord outline. The leaders then stack without crossing.
- **Plate and rod layouts** are dimensioned once, on the plan (3/5002), including the edge distances. On a pair of
  plans side by side, the edge chain goes on one plan only, so the two "40" figures don't meet in the gap.

### 9.6 Fitting views on the sheet

- A view that runs outside the drawing area (`!! detail … outside drawing area`) is fixed **in the view**, not by
  moving the frame. Ways to fix it:
  - shorten the member stubs (verticals cut at 300 instead of 420);
  - shorten the RC block depth;
  - pull the free-corner symbols closer;
  - narrow the note column (`leader(..., width)`);
  - shorten the notes.
- Notes on a busy steel view stay at 6 – 8 lines. Everything else goes in the general notes or the tables, which the
  view cites (TABLE 3, 4/5001).

### 9.7 Detail callouts (user rule, 2026-10-03)

When part of a view is enlarged in another detail, mark it on the parent view like this (`drafter.steel.detail_callout`).
This applies to any structure: a beam-column joint on an RC frame elevation, a pile cap on a foundation plan, a
connection on a steel or timber elevation. A set without the `S-CALL` layer adds it (pen 6, HIDDENX2).
1. **Boundary**:
   - A **dashed circle**, or a rounded rectangle for a long part, round the area enlarged.
   - Layer `S-CALL`: HIDDENX2 dashes (1.9 mm dash, 0.95 mm gap plotted), **0.25 mm**, pen 6.
   - It is not steel and not hidden steel, so it does not share their layers.
   - Size it to hold everything the detail shows, with no more than about 5 mm (paper) of slack.
2. **Leader**:
   - An ordinary note leader whose **arrow lands on the circle's edge**, never in its middle or on a member inside it.
   - Choose the edge point **in clear space**: `detail_callout(..., at=angle)`.
     - Use the right-most point (`at=0`) when the circle's right side is free. That gives one straight horizontal
       leader.
     - When members, break lines or another note's tip crowd that side, use the bottom or top of the circle. For
       example, on 1/5004 the purlin-end circle is reached at `at=-70`, below the purlin, by an L (§9.1).
3. **Note**: `DETAIL n/sheet - WHAT IT SHOWS`, e.g. "DETAIL 2/5004 - FB1 LUG END".
   - The number and sheet match the bubble of that detail's view title.
   - Do not repeat the callout in another note's text. The purlin note says only what the purlin is.
4. **Clearance**:
   - Keep the circle clear of break lines and of other leaders' tips. Extend a broken member past the circle if
     needed (the purlin on 1/5004).
   - Move a nearby note's tip away from the circle edge, so it can't be read as pointing at the callout.
5. **Use**: a section or elevation at 1:20 – 1:50 calls up its connections, enlarged at 1:5 – 1:10 on the same or
   another sheet. Example: 1/5004 calls up 2/5004 (lug end) and 3/5004 (purlin end).
6. **Dense views** (user, 2026-10-06: "detail call out"): where note leaders would cross members or dimension chains -
   a 1:50 truss elevation with a joint every 1.25 m - use the EIT form: the same dashed circle, a **short leader from
   its edge to a split bubble** "n" over "sheet" (radius about 3.4 mm) placed in clear space, preferably inside the
   view, never on a member, a tag or a label. Call out one example of each kind of joint on every view that has it.
   Example: BANWA2 S-202 - S-204, joints 1 - 4, 6, 7 on S-205 (`truss_details.callout_nodes`).

### 9.8 Labels written on the member (user rule, 2026-10-03)

A member that runs across the view with a clear band of its own can be **named on itself**, with no leader. Examples
from any structure type:
- a purlin or girt seen side-on, or a long plate;
- a beam in elevation, or a wall or strip footing on plan;
- a slab band, or a timber joist or rafter.
- The text goes inside the band, left-aligned, starting just clear of the first object in it (on 1/5004: 8 mm past
  the cleat).
- It must sit between the band's lines, clear of hidden lines (lips) and of anything crossing the band.
- It may run to two lines, e.g. "PURLIN C 150 x 65 x 20 x 3.2" / "(BY OTHERS) AT EVERY TOP NODE".
- Every leader that would otherwise cross the band leaves it.
- If a note-column leader would then run along or through the band text, move that note: to a row above or below the
  view, reached by one vertical leader (the cleat note on 1/5004), or to another target point.
