# Structural Drawing Standard: sheets, lines, text, dimensions, levels, marks and callouts
### Based on EIT Standard 011006-19 (วสท. 011006-19) *Reinforced Concrete Building Drafting Standard*, Rev. 1, March 2019

> **Scope: every structural drawing set produced here, whatever the material** (concrete, steel, composite, timber,
> masonry). The EIT standard is written for RC buildings, but its sheet, line, lettering, scale, grid, dimension,
> level, mark, callout and numbering rules are the office rules for all structural drawings.
>
> **Material-specific parts:**
> - The RC parts are in `docs/concrete/RC_DRAWING_RULES_EIT-011006-19.md`: §12 reinforcement graphics, §14 – §15
>   required content of RC plans and member details, and §19.4 / §19.7 office bar rules. Section numbers are kept in
>   both files, so a citation such as "EIT §12.2" or "§19.4" still points at one place. A stub is left here.
> - Steel content rules are in `docs/steel/STEEL_DETAILING_INSTRUCTION.md`.
> - Where and how annotation is placed: `docs/general/ANNOTATION_ALIGNMENT_GUIDE.md`. Symbols catalogue:
>   `docs/general/SYMBOLS.md`.
>
> It condenses the EIT standard into rules a drafter (human or program) can apply directly.
>
> **Source tags**, used everywhere below:
> - **[STD]**: stated explicitly in the standard's text or tables (normative).
> - **[FIG]**: observed in the standard's example drawings (Ch. 5–6). I extracted this from the PDF vector data, so the relative pen weights are measured, not guessed.
> - **[DER]**: derived by me from the standard. Examples are the ISO √2 pen scaling it cites and dash ratios measured from Table 2.3.
> - **[REC]**: my recommendation where the standard is silent. Replace it if your office has its own rule.
>
> **Office conventions override:** the conventions adopted on live projects (first applied on NRW-ST Rev A, 28/09/2026) are listed in **§19**. Where §19 differs from §0–§18, §19 governs for new drawings. Where-and-how placement of annotation is in `ANNOTATION_ALIGNMENT_GUIDE.md`.
>
> The standard calls itself **guidance**. Its reinforcement details are examples only and cannot be used as a legal reference (Preface). Where a project specification, building-control law or municipal ordinance conflicts with it, the project or law governs (§2.4.2).

---

## 0. Quick Reference — What line do I draw?

The rows below are the EIT (RC) set. Steel lines (members, hidden steel, welds, centre marks) are in `docs/steel/STEEL_DETAILING_INSTRUCTION.md` S4.

A2 sheet values. For other sheet sizes see §4.3.

| Element | Linetype | Pen (mm) | Source |
|---|---|---|---|
| Dimension line, extension (projection) line, leader | Continuous | **0.18** | [STD] |
| Grid / centre line (เส้นผ่านศูนย์กลาง) | Chain: long dash–dot | **0.18** | [STD] |
| Break line (continuation cut-off) | Continuous with one "Z" zig | **0.18** | [STD] |
| Property / land boundary | Long dash–dot–dot (phantom) | **0.25** | [STD] |
| **Concrete outline**: slab edge, beam, column, wall, **footing edge**, pile cap, stair, in plan, section or elevation | **Continuous** | **0.25** | [STD] |
| **Walls & columns *below* the slab** (hidden in a floor plan) | **Fine dashed** (short dashes) | **0.25** | [STD] |
| **Beams *below* the slab** (hidden in a floor plan) | **Dashed** (medium dashes, 2× the wall/column dash) | **0.25** | [STD] |
| Cutting-plane (section) line | Chain: long dash–dot | **0.25** | [STD] |
| Match line | Long dash–dot–dot | **0.35** | [STD] |
| Reinforcement shown **in plan** | **Long dashed** (long dash, short gap) | **0.35** | [STD] |
| Stirrups (ล.) / ties (ป.) | Continuous | **0.35** | [STD] |
| **Main reinforcement** (longitudinal bars) | Continuous, *very thick* | **0.50** | [STD] |
| Bar cut in section | Filled dot (●) | — | [STD] |
| Drawing frame (border) | Continuous | ≥ 0.7 (A0/A1), ≥ 0.5 (A2–A4) | [STD] |

**Element-specific answers:**

- **Slab edge (floor plan)**: continuous 0.25. Where an edge beam sits under the slab edge, its outer face coincides with the slab edge and is drawn **solid**, and its inner face is **dashed** (beam-below linetype). [STD + FIG]
- **Interior beam (floor plan)**: both faces use the dashed "beam below slab" linetype, 0.25. [STD + FIG]
- **Column in a floor plan**: a column that continues up to support the next floor is drawn **solid**, as its cut section. A column that **ends below** this floor is drawn **dashed**. [STD §5.4(9)] Examples draw the cut column heavier than the slab/beam lines, with a small "+" cross inside. [FIG]
- **Footing edge**:
  - Footing plan and footing detail: continuous 0.25. [STD + FIG]
  - Pile plan: the pile-cap outline is drawn **thin dashed** as a reference outline. [FIG]
  - Floor plans: footings are not drawn. [FIG]
- **Pile**:
  - Pile plan: circle with a "+" crosshair, continuous, with a legend symbol. [FIG]
  - Footing plan detail: dashed circle, because the pile is below the cap. [FIG]
  - Section: continuous outline with a wavy/S break at the bottom. The pile head embedded in the cap is shown dashed. [FIG]
- **Opening / shaft in slab**: outline plus two diagonal lines forming an **X** across the void. [STD §5.4(7)]

---

## 1. Scope & General [STD §1.1]

- Applies to structural drawings of RC buildings used as **construction drawings**. For other RC structures (bridges, arches, tanks, silos), apply the relevant parts.
- Covers structural drawings per the calculation. It is **not** at shop-drawing level.
- **Excludes** the bar bending schedule.
- References cited by the standard: EIT 1006-32 (old edition), EIT 1022-51 (drawing set order), TIS/มอก. 440 Vol. 1 & 3 (construction drawing, based on ISO), IStructE *Standard Method of Detailing Structural Concrete*, ACI SP-66.
- **Language** [STD Intro]: use Thai for small jobs with local contractors, and English for medium and large projects.

## 2. Units [STD §1.3]

| Quantity | Unit |
|---|---|
| Dimensions & distances | **millimetres** (ISO). Avoid mixing units. |
| Levels | **metres, 3 decimals** (e.g. `+4.000`), always referenced to a positive datum |
| Weight | kg |
| Bar size | mm only |

> Note: the example plans in the standard write slab levels in mm (`+500`, `SL+3650`), which contradicts §3.4.2. **Follow the text: metres, 3 decimals** [REC], unless the project states otherwise.

---

## 3. Sheet Set-up

### 3.1 Paper sizes [STD Table 2.1, TIS 33-2516]

| Size | W × L (mm) |
|---|---|
| A0 | 841 × 1189 |
| A1 | 594 × 841 |
| A2 | 420 × 594 |
| A3 | 297 × 420 |
| A4 | 210 × 297 |

### 3.2 Frame (border) [STD §2.2.1, Fig 2.1]

| Paper | Margin top/right/bottom | Margin left (binding) | Frame line |
|---|---|---|---|
| A0, A1 | ≥ 15 mm | ≥ 30 mm | ≥ 0.7 mm |
| A2, A3, A4 | ≥ 10 mm | ≥ 20 mm | ≥ 0.5 mm |

### 3.3 Sheet zones [STD §2.2.2, Fig 2.2]
The sheet has five zones:
1. **Drawing area**: one main view goes on the **left**. Multiple views are aligned in rows and columns, and arranged where possible so each part folds to A4.
2. **Text area**: at the **right** or **bottom**, separated from the drawing area by a thin dashed line. [FIG] It holds:
   - (a) *Explanation*: special symbols, names, abbreviations, units.
   - (b) *Instructions*: extra requirements, e.g. materials.
   - (c) *References*: related drawings and documents.
3. **Title block**: at the right.
4. **Revision table**.
5. **Key plan** (location sketch): hatch the area shown on this sheet on a small site plan, building plan or building section. [Fig 2.6]

**Layouts:**
- **Vertical layout (Fig 2.2a)**: title block at the bottom-right corner. Revision table directly **above** it, same width. Key plan above that. Text area runs down the right strip.
- **Horizontal layout (Fig 2.2b)**: title block at the bottom-right. Revision table immediately **left** of it, ≥ 100 mm long. Text area runs along the bottom strip. Key plan above the title block.

### 3.4 Title block [STD §2.2.2.3, Fig 2.3–2.4]
- Width **≤ 100 mm** in the vertical layout, or height **≤ 100 mm** in the horizontal layout (for A1/A2). Scale it proportionally for larger or smaller paper.
- Read direction must be consistent across the set.
- **Contents:**
  1. Owner (with logo)
  2. Project name
  3. Design office
  4. Drawing title
  5. Designers: architect, engineer, checked by, drawn by (with signature lines)
  6. Drawing number
  7. Scale, date
  8. Approved by + date

**Vertical block (100 mm wide), rows top→bottom** [FIG 2.3]:

| Row height | Content |
|---|---|
| 25 | Owner (logo + name) |
| 25 | Project |
| 35 | Design office |
| 35 | Drawing title (large text) |
| 35 | Left: Architect / Engineer / Checked by / Drawn by. Right: Drawing No. (top), Scale \| Date (bottom) |
| 10 | Approved by … Date … |

**Horizontal block (≈ 200 × 80 mm)** [FIG 2.4]:
- Row 1 (25 mm): Owner (100) \| Project (100).
- Row 2 (20 mm): Design office.
- Row 3 (35 mm): Designers (50) \| Drawing title (100) \| Drawing No. + Scale/Date (50).

### 3.5 Revision table [STD §2.2.2.4, Fig 2.5]
- Row height **≥ 5 mm**.
- Columns: **Rev. No. \| Description \| Date \| Signature**.

### 3.6 Reference grid (sheet zoning) [STD §2.3, Fig 2.7]
- Every sheet gets a zone grid in the margin: **letters on the vertical edges** (A, B, C…) and **numbers on the horizontal edges** (1, 2, 3…).
- Numbering starts from the corner **opposite the title block** and is **repeated on the opposite side**.

### 3.7 Drawing set order [STD §2.8]
1. Drawing list
2. General notes & special specifications
3. Typical details
4. **Pile plan**
5. **Foundation plan**
6. Floor plans, lowest floor → roof
7. Footing details
8. Column details
9. Wall details
10. Beam details
11. Slab details
12. Stair details
13. Roof-framing details
14. Enlarged & misc. details

(Chapter 5 adds: plans are ordered by **construction sequence**, piles → roof.)

### 3.8 General notes on the drawings [STD §2.9]
- Put the key specification items on the drawings (short and clear), so the contractor need not keep consulting the separate specification.
- Job-specific or special requirements may be added as separate "special specifications".

---

## 4. Lines: Weights & Types

### 4.1 Principles [STD §2.5.1–2.5.2]
- Line weight and type encode meaning. **One meaning always uses the same weight and type**, consistently across the whole project.
- ISO pen series (mm): **0.13 · 0.18 · 0.25 · 0.35 · 0.50 · 0.70 · 1.00 · 1.40 · 2.00**. Each step is ×√2, matching the A-series paper ratio. Enlarging or reducing a drawing by one paper size shifts every pen by one step.

### 4.2 Table 2.3: Line weights & types for **A2** [STD]

| # | Line meaning (Thai term) | Pen | Linetype |
|---|---|---|---|
| 1 | Dimension line, leader (เส้นแสดงระยะห่าง (มิติ), เส้นชี้บอก) | 0.18 | Continuous |
| 2 | Centre line / grid (เส้นผ่านศูนย์กลาง) | 0.18 | Long dash – dot |
| 3 | Break line, continuity cut (เส้นแสดงการตัดตอนส่วนที่ต่อเนื่องกัน) | 0.18 | Continuous with single Z-break |
| 4 | Property line (เส้นแสดงขอบเขตที่ดิน) | 0.25 | Long dash – dot – dot |
| 5 | **Concrete outline** (เส้นแสดงขอบเขตของคอนกรีต) | 0.25 | Continuous |
| 6 | **Wall & column below slab** (…กำแพงและเสาที่อยู่ใต้แผ่นพื้น) | 0.25 | Fine dashed |
| 7 | **Beam below slab** (…คานที่อยู่ใต้แผ่นพื้น) | 0.25 | Dashed (medium) |
| 8 | Cutting-plane line (เส้นแสดงแนวการตัด) | 0.25 | Long dash – dot |
| 9 | Match line (เส้นแสดงการจับคู่) | 0.35 | Long dash – dot – dot |
| 10 | Reinforcement in plan (เส้นแสดงเหล็กเสริมในผัง) | 0.35 | Long dashed |
| 11 | Stirrup / tie (เส้นแสดงเหล็กปลอกหรือเหล็กลูกตั้ง) | 0.35 | Continuous |
| 12 | **Main reinforcement** (เส้นแสดงเหล็กเสริมหลัก) | 0.50 | Continuous |

§3.5 adds that **rebar symbols are drawn "very thick"** [STD].

### 4.3 Pen table for other sheet sizes [DER from §2.5.2 √2 rule]

| Line class | A3 | **A2 (base)** | A1 | A0 |
|---|---|---|---|---|
| Thin: dims, leaders, grid, break | 0.13 | **0.18** | 0.25 | 0.35 |
| Outline: concrete, hidden, property, cut line | 0.18 | **0.25** | 0.35 | 0.50 |
| Medium: stirrups/ties, rebar in plan, match line | 0.25 | **0.35** | 0.50 | 0.70 |
| Thick: main bars | 0.35 | **0.50** | 0.70 | 1.00 |

The standard allows adjusting "as appropriate" for other paper sizes. The √2 shift above is the ISO-consistent way to do it. For a **half-size print** of an A1 set on A3, keep the A1 pens: the print reduction produces the A3 row automatically.

### 4.4 Linetype patterns [DER]
The standard only shows the patterns graphically. I measured the dash:gap ratios from the vector data of Table 2.3 and normalized them so the grid long-dash = 12 mm (plotted).

| Name | Pattern, plotted mm (dash +, gap −) | Measured ratio | Used for |
|---|---|---|---|
| `EIT_CENTER` | 12, −2, 2, −2 | 6 : 1 : 1 : 1 | Grid / centre line (0.18), cutting plane (0.25) |
| `EIT_PHANTOM` | 10, −2, 2, −2, 2, −2 | 5 : 1 : 1 : 1 : 1 : 1 | Property line (0.25) |
| `EIT_MATCH` | 13, −2.5, 2.5, −2.5, 2.5, −2.5 | 5 : 1 : 1 : 1 : 1 : 1 (≈1.3× phantom) | Match line (0.35) |
| `EIT_HIDDEN_FINE` | 2.4, −1.2 | 2 : 1 | Wall/column below slab |
| `EIT_HIDDEN` | 4.8, −2.4 | 2 : 1 (2× fine) | Beam below slab |
| `EIT_REBAR_PLAN` | 20, −10 | 2 : 1 (long) | Rebar in plan |

AutoCAD `.lin` (use with `PSLTSCALE=1`, with viewport scale handling model space, or set `LTSCALE` = drawing scale factor in model space):

```
*EIT_CENTER,EIT centre/grid  ____ . ____ . ____
A,12,-2,2,-2
*EIT_PHANTOM,EIT property line  ____ . . ____ . .
A,10,-2,2,-2,2,-2
*EIT_MATCH,EIT match line  _____ . . _____ . .
A,13,-2.5,2.5,-2.5,2.5,-2.5
*EIT_HIDDEN_FINE,EIT wall/column below slab  - - - - - -
A,2.4,-1.2
*EIT_HIDDEN,EIT beam below slab  -- -- -- --
A,4.8,-2.4
*EIT_REBAR_PLAN,EIT reinforcement in plan  ______  ______
A,20,-10
```

Absolute dash lengths are not specified by the standard. Only the ratios above and the fine-vs-medium distinction between rows 6 and 7 are taken from it. Scale all patterns together if they read too coarse or too fine.

### 4.5 How the example drawings apply weights [FIG]
Pen-width analysis of Figures 5.1–6.13 (relative, lightest → heaviest):

| Rank | Elements drawn at this rank in the examples |
|---|---|
| 1 (thinnest) | Grid lines, dimension & extension lines, leaders, pile-cap reference outline in pile plan, stair treads in plan, hatch, strip boundaries in flat-slab plan |
| 2 | Grid bubbles |
| 3 | Concrete outlines (footing, slab edge, beams-below dashed, beam/column elevation outline), piles, general text |
| 3+ | Flat-slab edge; shear-wall outline in the wall-detail plan |
| 4 | **Cut columns/walls in plan** (with + cross), **stirrups & ties**, slab bars in section, beam longitudinal bars in elevation |
| 5 (heaviest) | **Main bars** in footing/column, drawing titles, cutting-plane arrows |

Takeaway: **dims < concrete outline < stirrups/ties < main bars** is the invariant hierarchy. This matches Table 2.3 (0.18 < 0.25 < 0.35 < 0.50).

The examples also draw cut vertical elements (columns, walls) one step heavier than slab/beam outlines. [REC] Adopting this is optional: use **0.35 for cut columns/walls in plan** while keeping other concrete at 0.25.

---

## 5. Scales [STD Table 2.2]

| Drawing | Scale |
|---|---|
| Site plan | 1:500, 1:200 |
| Pile plan, foundation plan, floor plans, slab-reinforcement plans, building elevations & sections | 1:100, 1:50 |
| Footing elevations/sections; slab & wall details | 1:50, 1:20 |
| Column, beam & slab elevations/sections | 1:20, 1:10 |
| Reinforcement details | 1:10, 1:5 |
| Enlarged details | 1:5, 1:2 |

Rules [STD §2.4]:
- **Every drawing states its scale.** Add a **bar scale** (Fig 2.8) where prints may be reduced.
- Choose the scale for clarity, drafting economy, and **consistency within a job**.
- Project or statutory scale requirements override this table.

> The standard's own examples use **1:25** for footing, column, wall and stair details. This is not in Table 2.2 but is common Thai practice. [FIG]

---

## 6. Lettering [STD §2.6]

- **Heights (mm)**, for Thai characters and capitals: **2.5 · 3.5 · 5 · 7 · 10 · 14 · 20**.
- **Lower-case** height is 10/14 (≈ 7/10) of the capital height.
- Roman text is upright or slanted **15° to the right**.
- **Stroke thickness per height** (Table 2.4):

| Text height | 2.5 | 3.5 | 5 | 7 | 10 | 14 | 20 |
|---|---|---|---|---|---|---|---|
| Stroke (mm) | 0.25 | 0.35 | 0.50 | 0.70 | 1.00 | 1.40 | 2.00 |

- The stroke may be thickened for emphasis.
- Text must stay legible after reduction.

[REC] Typical use on A2:
- Notes and dimensions: 2.5 mm.
- Member marks, grid letters: 3.5 mm.
- View titles: 7 mm.
- Sheet title in the title block: 10 mm.

---

## 7. Grids [STD §3.1, Fig 3.1]

- Every plan has a structural grid through column centres, normally following the architectural column grid.
- **Short direction**: capital letters **A, B, C…**. Sub-grids use **Aa, Ab**.
- **Long direction**: numbers **1, 2, 3…**. Sub-grids use **1.1, 1.2**.
- Labels sit **inside circles** at the grid ends.
- Grid lines use the centre linetype (chain, 0.18).
- Dimension grids with **filled dots** at the grid intersections (see §8.2).

---

## 8. Dimensioning [STD §3.2]

### 8.1 Lines
- Dimension and extension lines are **thin and continuous**.
- Extension lines start a **small gap** from the object, run perpendicular to the dimension line, and extend **≈ 2 mm** beyond it. [Fig 3.2]
- Place the chain (continuous) dimensions and the overall dimension **close together**, in parallel tiers. **Never let dimension lines cross.** [Fig 3.3/3.4]
- Dimension only what is needed for construction. Never scale off prints.

### 8.2 Terminators [STD §3.2.3, Fig 3.5]
- Allowed types: closed arrow, open arrow, **45° oblique tick**, filled dot, open circle.
- Arrows are the general choice. Whatever you choose must mean the same thing across the whole set. If you use more than one type, explain each in the legend.
- **Recommended combination** (Fig 3.5b, used in every example):
  - **Filled dot** where the dimension meets a **grid / centre line**.
  - **45° tick** where it meets a **member edge / face**.

### 8.3 Text placement
- **Plans**: text parallel to the dimension line (reads along the plan). [Fig 3.6]
- **Sections/elevations**: parallel or perpendicular is allowed. **Perpendicular is recommended in sections.** [Fig 3.7]
- **Narrow spaces**: put the text **outside** the extension lines. [Fig 3.8]
- **Inclined dimensions**: text reads from the bottom or right. Avoid the 30° sector left of vertical. [Fig 3.9]
- **Angles**: per Fig 3.10.

---

## 9. Levels [STD §3.4, Fig 3.12]

- Datum (ระดับกำหนด) should make **all levels positive**. Shown in **metres, 3 decimals**.
- When more than one kind of level appears (existing vs. required), distinguish them by symbol.
- Finished floor level = `FFL. +4.000`.
- **In sections and elevations**, place level marks **outside** the view:
  - A horizontal extension line with an open **datum triangle** (▽) under the label.
  - Benchmark: `TBM` with the value **boxed**, `±0.000`, and an upward triangle.
- Structural slab level in details: `SL+3650` with a filled triangle [FIG] (see the unit note in §2).

---

## 10. Member Marks

### 10.1 Letters [STD §2.7.1, §1.2.2]

| Mark | Member |
|---|---|
| **F** | Footing (ฐาน) |
| **C** | Column (เสา) |
| **B** | Beam (คาน) |
| **S** | Slab (แผ่นพื้น) |
| **W** | RC wall (ผนัง/กำแพง) |
| **ST** | Stair (บันได) |

### 10.2 Numbering systems (both appear in the standard, so pick **one** per project)
- **System A [STD §2.7.1]**: floor/level prefix + letter + number. Examples:
  - `GB1` = ground beam
  - `2B1` = 2nd-floor beam
  - `RB1` = roof beam
- **System B [STD §3.3, Fig 3.11]**: letter + (floor digit) + sequence.
  - Columns and walls run full height, so they carry no floor digit: `C01, C02, W01`.
  - Beams and slabs carry the floor: `B101, B102, S101` (1st floor), `B401` (4th floor).
  - Footings: `F01, F02`.
- **As used in the example plans [FIG]**:
  - `1B4A`, `2S3`, `RS1`, `RB4G`: floor prefix + letter + number, plus a suffix letter for variants of one beam type.
  - Footings `F1…F4`, columns `C1…C4`, stairs `ST1`.
  - Roof column stubs are marked `CK`.

### 10.3 Discipline letters for drawing titles [STD §2.7.2]

| Code | Discipline |
|---|---|
| AR | Architectural |
| CE | Civil |
| **ST** | **Structural** |
| EE | Electrical & comms |
| ME | Mechanical (lifts, escalators) |
| AC | Air-conditioning & ventilation |
| SN | Plumbing & sanitary |

---

## 11. Section & Detail Callouts [STD §2.10, Fig 2.9–2.10]

**Section cut:**
- Draw a chain line (0.25).
- Mark each end with either:
  - an arrow plus the section letter, or
  - a **circle bubble split horizontally** with a filled triangular "hat" pointing in the view direction. The upper half holds the section ID. The lower half holds the **sheet number** where the section is drawn, or "–" if it is on the same sheet.
- The opposite end is a filled half-arrow wedge.

**Section title:**
- `SECTION` text, underlined, with `SCALE 1:50` under the line.
- The same split bubble with triangles, at the right end of the underline.
- The lower half gives the **sheet the cut is taken from**.

**Detail callout:**
- Draw a **chain-line circle** around the area.
- Add a leader to a split bubble (no triangles): upper = detail ID, lower = sheet where it is drawn.

**Detail title:**
- `DETAIL` text, underlined, with the scale, plus a split bubble (no triangles).
- The lower half gives the source sheet.

**View titles in the examples [FIG]:**
- Large underlined title, bilingual, e.g. `FOOTING PLAN (ผังฐาน)`.
- Left under the line: `SCALE (มาตราส่วน)`. Right under the line: `1 : 100`.

---

## 12. Reinforcement Graphics: moved

Bar symbols, drawing rules and bar notation are concrete-specific: see `docs/concrete/RC_DRAWING_RULES_EIT-011006-19.md` §12.

---

## 13. Drawing Numbering [STD Ch. 4, based on EIT 1022-51]

```
Sheet number:          PPPP-BB-DD-SSSS-G-RR
Digital file name:     PPPP-BB-DD-SSSS-G-RR-DDMMYY
```

| Field | Width | Meaning |
|---|---|---|
| `PPPP` | 2–4 letters | Project abbreviation (e.g. `RAH` = Rajbumrung Hospital) |
| `BB` | 2 letters | Building (`BA`, `BB`, …). Omit for a single-building project. |
| `DD` | 2 letters | Discipline, see below |
| `SSSS` | 4 digits | Series number, see below |
| `G` | 1 letter | Design stage, see below |
| `RR` | 1–2 chars | Revision code, see below |
| `DDMMYY` | 6 digits | Reference date (latest revision). Written `29/05/61` in text. It is part of the **file name only**, not the sheet number. |

**Discipline codes (Table 4.1):**

| Code | Discipline | Code | Discipline |
|---|---|---|---|
| GN | General | EE | Electrical & comms |
| AR | Architectural | CE | Civil |
| **ST** | **Structural** | **PL** | **Piling** |
| SN | Plumbing & sanitary | SE | Special equipment |
| FP | Fire protection | IT | IT systems |
| AC | HVAC | IN | Interiors |
| ME | Mechanical | LS | Landscape |

**Series (Table 4.2)** (may be adapted per discipline):

| Range | Content |
|---|---|
| 0001–0999 | Drawing list, location plan, site plan |
| 1000–1999 | General & particular specs, symbols, abbreviations |
| 2000–2999 | Schedules, equipment lists, load diagrams |
| 3000–3999 | Floor plans |
| 4000–4999 | Elevations, sections, related plans |
| 5000–6999 | Enlarged details |
| 7000–9999 | Others |

**Stage (Table 4.3):**

| Code | Stage |
|---|---|
| I | Inception |
| C | Conceptual |
| P | Preliminary |
| D | Draft final |
| T | For tender |
| F | For construction |
| S | Shop drawing |
| A | As-built |

**Revision (Table 4.4):**

| Code | Meaning |
|---|---|
| `A1, A2…` | Internal revisions |
| `A` | 1st submission to owner |
| `B1, B2…` | Internal revisions after submission |
| `B, C…` | Later submissions |
| `00` | Tender issue |
| `01, 02…` | Post-tender revisions |

---

## 14. – 15. Plan drawings and member details (required content): moved

What RC plans (pile, footing, floor, roof) and RC member details must show: see `docs/concrete/RC_DRAWING_RULES_EIT-011006-19.md` §14 – §15.
Steel sets: `docs/steel/STEEL_DETAILING_INSTRUCTION.md` S1.

---

## 16. Recommended CAD Layer / Pen Table [REC]

Built on Table 2.3 for **A2**. Scale the pens per §4.3 for other sizes.

| Layer | Content | Linetype | Pen A2 | Colour (suggestion) |
|---|---|---|---|---|
| `S-GRID` | Grid lines | EIT_CENTER | 0.18 | 8 grey |
| `S-GRID-BUBL` | Grid bubbles & text | Continuous | 0.25 | 3 green |
| `S-DIMS` | Dimensions | Continuous | 0.18 | 8 |
| `S-ANNO-LEAD` | Leaders, notes | Continuous | 0.18 | 5 |
| `S-ANNO-BRK` | Break lines | Continuous | 0.18 | 8 |
| `S-CONC` | Concrete outline: slab edge, footing edge, beams/columns seen | Continuous | 0.25 | 5 blue |
| `S-CONC-CUT` | Columns/walls cut in plan (optional emphasis) | Continuous | 0.35 | 4 cyan |
| `S-CONC-HIDN-WALL` | Walls/columns below slab | EIT_HIDDEN_FINE | 0.25 | 5 |
| `S-CONC-HIDN-BEAM` | Beams below slab | EIT_HIDDEN | 0.25 | 5 |
| `S-FTNG-REF` | Pile-cap outline on pile plan | EIT_HIDDEN | 0.18 | 8 |
| `S-PILE` | Piles | Continuous | 0.25 | 5 |
| `S-OPNG` | Openings (outline + X) | Continuous | 0.18 | 8 |
| `S-CUTL` | Section cut lines | EIT_CENTER | 0.25 | 6 magenta |
| `S-MATCH` | Match lines | EIT_MATCH | 0.35 | 6 |
| `S-PROP` | Property line | EIT_PHANTOM | 0.25 | 1 |
| `S-REBR-PLAN` | Rebar in plan | EIT_REBAR_PLAN | 0.35 | 30 orange |
| `S-REBR-STIR` | Stirrups & ties | Continuous | 0.35 | 30 |
| `S-REBR-MAIN` | Main bars (+ dots in section) | Continuous | 0.50 | 1 red |
| `S-HATC` | Hatch (blinding, sand, parapets) | Continuous | 0.13 | 8 |
| `S-TEXT` | General text | — | per Table 2.4 | 5 |
| `S-TITL` | View titles | — | per Table 2.4 | 1 |
| `S-SHEET` | Frame, title block | Continuous | 0.5 / 0.7 | 7 |

---

## 17. Pre-issue QA Checklist

- [ ] Correct paper size, frame margins (left binding margin) and frame line weight
- [ ] Title block complete: owner, project, office, title, designers, number, scale, date, approval
- [ ] Revision table filled in (No., description, date, signature)
- [ ] Key plan hatched; zone grid (letters vertical, numbers horizontal) present
- [ ] Every view has a title, a scale, and a bar scale where prints may be reduced
- [ ] Line hierarchy correct: dims 0.18 < concrete 0.25 < stirrups 0.35 < main bars 0.50 (A2)
- [ ] Hidden beams use medium dashes; hidden walls/columns use fine dashes; columns ending below are dashed
- [ ] Openings crossed with an X
- [ ] Grid: letters on the short side, numbers on the long side, in circles
- [ ] Dimensions in mm, no crossing, dots on grids, 45° ticks on edges
- [ ] Levels in m with 3 decimals, positive datum, triangle marks outside sections
- [ ] Member marks consistent (one numbering system) across plans, details and schedules
- [ ] Every beam labelled with mark + (b×h); every slab with mark, level, thickness
- [ ] Bar labels: `n-DBxx`, `DBxx @sss`, T/B, NF/FF; steel grades only in the notes
- [ ] Section and detail bubbles reference the correct sheet numbers
- [ ] Sheet number format `PPPP-BB-ST-SSSS-G-RR`; sheets in the §3.7 order
- [ ] General notes: concrete strength, steel grades, cover, pile data

---

## 18. Known Inconsistencies in the Source (resolved choices)

| Issue | Standard text | Example figures | Choice here |
|---|---|---|---|
| Level units | m, 3 decimals | mm (`+500`, `SL+3650`) | **m, 3 dp** [REC] |
| Detail scale | 1:50/1:20 footing, 1:20/1:10 members | 1:25 used | Table 2.2 preferred; 1:25 acceptable |
| Rebar in plan | Long-dashed 0.35 | Continuous, with hooks drawn | **Long-dashed** per Table 2.3; continuous only with a legend note |
| Member numbering | §2.7 (`2B1`) vs §3.3 (`B201`, `C01`) | `1B4A`, `1S1`, `C1` | Choose one per project and state it in the general notes |
| Cut column weight | Not distinguished from concrete outline | Drawn heavier | Optional `S-CONC-CUT` at 0.35 |

---

## 19. Office Conventions Adopted (first used on NRW-ST Rev A, 28/09/2026)

These conventions were agreed with the engineer during NRW-ST Rev A and apply to all new drawings, whatever the material. Steel sets add their own layers and graphics on top (`docs/steel/STEEL_DETAILING_INSTRUCTION.md` S4). Where they differ from §0–§18, **they govern**. EIT allows each of them: it calls itself guidance, and §2.5.3 and §3.2.3 permit adjusting pens and choosing terminators.

### 19.1 Sheet and text

| Item | Convention | EIT reference |
|---|---|---|
| Paper | A3 (420 × 297) originals; frame 20 left / 10 elsewhere, 0.70 | §2.2.1 (≥ 0.5 for A2–A4) |
| Title strip | Right side, 70 wide (EIT 100 × 0.7 for A3), full height; revision table above the title block; key plan; status stamp | §2.2.2 |
| Zone grid | 8 × 6 (numbers 1–8 horizontal, letters A–F vertical), both sides | §2.3 |
| Font | **Arial Narrow**: 2.0 mm body, **2.8 mm** bold headers and titles | §2.6 (2.5 / 3.5 series adapted) |
| Drawing number | `<PROJ>-ST-<series>-<stage>-<rev>`, e.g. `NRW-ST-5001-D-A` | Ch. 4 |
| **General-notes sheets** | All annotation = the rules below **× 0.625** (1.25/2.00): text 1.25 / 1.75, pitch 2.08, dimensions 1.25. Frame, title strip and pens are not scaled. See `GENERAL_NOTES_DRAWING_INSTRUCTION.md` | – |

### 19.2 Pens and lines (supersede §4.3 / §16 for A3 originals)

| Line | Pen | Linetype | Colour (plotted) |
|---|---|---|---|
| Main bars, dowels | **0.50** | Continuous | Black |
| Concrete **cut** | **0.35** | Continuous | Black |
| Secondary bars (DB10), title lines, view-title underline | 0.35 | Continuous | Black |
| Concrete **seen**, property line, cutting plane (`S-CUTL`), ground, drain, joints | 0.25 | Continuous / phantom / centre | Black |
| Centre, grid and reference lines (`S-CENT`) | 0.18 | `EIT_CENTER` 12 / 2 / 2 / 2 | Black |
| Hidden concrete, hidden drain, excavation | 0.25 | `EIT_HIDDEN` **3.0 / 1.5** (office value, user 2026-09-30) | **Grey (ACI 8)** |
| Notional lines: punching critical section, zone limits (`S-ZONE-DASH`) | 0.18 | `EIT_HIDDEN_FINE` **1.5 / 0.75** (office value) | Grey |
| Construction joint | 0.25 | **Zig-zag**, pitch 2.0, amplitude ±0.8 | Black |
| Dimensions, leaders, lean concrete, geotextile | 0.18 | Continuous / `EIT_HIDDEN_FINE` | Black |
| Breaks, arris, inner title lines, zone grid | 0.18 | Continuous | Grey |
| Hatch | 0.13 | – | Grey |

**Rules:**
- EIT Table 2.3 A2 pens are used **unreduced on A3 originals**, and cut concrete is one step heavier than seen.
- ACI 8 is secondary information, screened 50 % by `NRW-EIT.ctb` (derived from `monochrome.ctb`).
- Linetypes use project names `EIT_*` so `acadiso.lin` can't overwrite them.
- `LTSCALE = PSLTSCALE = MSLTSCALE = 1`, entity ltscale 1. Office patterns (plotted mm): **centre 12 / 2 / 2 / 2, phantom 10 / 2 / 2 / 2 / 2 / 2, match 13 / 2.5 … (= §4.4)**; **hidden 3.0 / 1.5 and fine hidden 1.5 / 0.75** (the user keeps these shorter office values; §4.4 would be 4.8 / 2.4 and 2.4 / 1.2). The old 8.5 / 1.4 chain read as solid and was raised to §4.4 on 2026-09-30.
- AutoCAD draws the linetype of an entity inside a scaled detail block at **sheet size** in both the Model tab and the layouts (tested 2026-09-30 for PSLTSCALE 0 and 1). So detail blocks keep entity ltscale 1; ltscale = scale makes the dashes 25× too long, and they read as solid.
- Short closed notional outlines, such as a 26 mm critical-section square, use the fine hidden line, not a chain: a 12 mm chain dash leaves only fragments. Never let a notional line coincide with a bar or stirrup line; move the first stirrup line to d/4.

### 19.3 Dimensions (supersede §8.2)

- **Terminators:** filled arrowheads, **2.0 mm** (instead of 45° ticks and dots).
- **Extension lines:** **grey ACI 8**, 1 mm gap from the object, 2 mm beyond the dimension line.
- **Dimension line and text:** black, 2.0 mm, text above and aligned.
- **Placement:** height chains sit on the level extension lines, outside the note column.
- **Tiers (office rule, 2026-09-29):** a dimension whose span lies inside another's goes on the tier nearer the object, so no extension line crosses a dimension line.
  - Nothing may run through dimension text: no geometry, centre line or other dimension.
  - A small dimension whose text does not fit puts its text outside, in line with the dimension line.
  - Details: `ANNOTATION_ALIGNMENT_GUIDE.md` §2.4.1; the engine check is `check_dims()`.

### 19.4 Reinforcement graphics: moved to `docs/concrete/RC_DRAWING_RULES_EIT-011006-19.md` §19.4

### 19.5 Annotation (summary; full rules in `ANNOTATION_ALIGNMENT_GUIDE.md`)

- Notes sit in aligned columns or rows; leaders have a **45° / 60° leg + horizontal run + 3 mm shelf**, with no shallow random angles and no crossings.
- **Terminators:**
  - 2.0 mm filled arrow on edges and on bars drawn along their length, with the tip on the object's **edge**, never inside black;
  - **open circle Ø = 2 × bar dot** on bars cut in section;
  - steel: open circle Ø = 1.25 × the hole on a bolt or hole seen end-on, and the arrow on the plate edge on a plate.
- **Units on every bare number** in notes, leaders, titles and keys ("GROUT 30 mm"); dimension figures, designations and table cells stay bare, and table headers carry the unit (guide §2.4.2, user rule 2026-10-03).
- Steel sets use orthogonal leaders (straight, or an L with a vertical leg ≥ 3 mm), dashed detail callouts and labels written on the member (guide §9).
- View titles are left-aligned to their view, 6 mm below the lowest annotation.

### 19.6 Earthwork graphics

- **Excavation:** a dashed grey line with working space and the stated slope (NRW: **2:1 V:H**), plus a slope triangle labelled with its V and H legs.
- **Soil and fill:** undisturbed soil gets an `EARTH` band; selected fill gets an `AR-SAND` stipple; drainage stone gets `GRAVEL`.
- **Concrete:** RC sections are **not** hatched.

### 19.7 Bar ends and lap splices: moved to `docs/concrete/RC_DRAWING_RULES_EIT-011006-19.md` §19.7
