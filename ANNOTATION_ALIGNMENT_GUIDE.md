# Annotation Alignment Guide: Notes, Leaders, Terminators, Dimensions & Titles

- **Companions:**
  - `DRAWING_STANDARD_EIT-011006-19.md` covers *what* to draw: lines, pens, symbols, EIT rules.
  - `NRW-ST_Linetype_and_Lineweight_Guide.md` covers CAD setup.
  - This guide covers *where and how* annotation is placed, so every sheet reads as calm, aligned columns of notes.
- **Reference style:** "Life of an Architect" section details. Notes sit in tidy columns beside the detail, with leaders that leave the object at a standard angle and land on a short horizontal shelf.
- **Implementation:** the rules are coded in `jobs/nooker_rw/build_rw.py` (the *annotation engine*), so they are applied automatically. This document is also the manual rule set for anyone drafting by hand.
- **Status:** matches NRW-ST Rev A as issued.

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

### 2.4 Dimensions (see the CAD guide §5 for all variables)

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
- **Check:** `check_dims()` runs in `capture()` for every view. It prints `!! <view>: extension line of 'A' crosses dimension line 'B'`, `dimension lines 'A' and 'B' cross`, and `<layer> line runs through the dimension text 'A'`.
  - A sheet is not finished while one appears.
  - To review, crop the plotted detail: `python crop_det.py <set> DET-xxxx-n`.

### 2.5 Symbols drawn with the notes

| Symbol | Drawing |
|---|---|
| **Construction joint** | Zig-zag on `S-CJOINT` 0.25, tooth pitch 2.0, amplitude ±0.8 (Section A stem/footing joint, joint-face view, legend on 1001) |
| **Excavation slope** | Dashed grey line (`S-EXCV`) with a slope triangle on the fill side: vertical leg **2** and horizontal leg **1** (unit 50 mm), numbers 2.0 mm next to the legs |
| **Level mark** | Open datum triangle, apex on the line (w 2.4, h 2.0), with value and description 2.0 mm above the line (e.g. `+0.600  TOP OF WALL`), **outside** the section, on the boundary side |
| **Break line** | Straight line with a single Z (EIT Table 2.3) |
| **Section / detail bubble** | Ø9.2 split circle: ID 2.8 bold above, sheet 2.0 below; filled triangles for sections |

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

### 4.1 Layout used on each Rev A view

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

## 7. The engine (`build_rw.py`)

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

- [ ] Notes form straight columns or rows with a common edge; left text right-justified, right text left-justified.
- [ ] Every leader: 45° / 60° leg + horizontal run + 3 mm shelf. No shallow random angles, no crossings, no run doubling back over its text.
- [ ] No leader along or on a drawing line, and none crossing a dimension line or reinforcement it doesn't point at.
- [ ] Note order matches target order; notes sit near their targets.
- [ ] Filled 2 mm arrows on bars drawn along their length, edges and surfaces, with tips on the **edge**, never inside black.
- [ ] Open circles (Ø = 2 × bar dot) on cut bars.
- [ ] No bar dot touching another bar line or bend.
- [ ] Bar-mark bubbles all Ø4, on the shelf.
- [ ] Dimensions with filled 2 mm arrows; extension lines grey.
- [ ] Clean dimensioning (§2.4.1):
  - contained dimensions sit on the inner tier;
  - no extension line crosses a dimension line;
  - nothing runs through dimension text, and centre lines stop before the tiers;
  - small dimensions have their text outside (`tside`);
  - no `!! <view>: …` dimension warning in the build log.
- [ ] Construction joints drawn zig-zag; excavation slope with its 2 : 1 triangle.
- [ ] No text on hatch, geometry, level marks or dimensions.
- [ ] View title left-aligned to its view, ≥ 6 mm clear of the lowest note; no viewport overflow (`!!` in the build output).
