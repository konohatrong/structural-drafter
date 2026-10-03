# Staircase Drawing Instruction (RC stairs, A3 structural drawings)

**Office instruction for drawing reinforced-concrete stairs.**
- It covers:
  - geometry rules;
  - structural systems and design checks;
  - reinforcement detailing;
  - required views, line presentation, annotation and dimensions;
  - bar schedule and notes;
  - the generator code and a pre-issue checklist.
- **Reference job:** stair ST-1, `STR-ST-5101-D-A` (`jobs/stair_demo/`).
- **Read with:**
  - `DRAWING_STANDARD_EIT-011006-19.md`, where §19 office conventions govern;
  - `ANNOTATION_ALIGNMENT_GUIDE.md`;
  - the NRW `NRW-ST_Linetype_and_Lineweight_Guide.md` for the CAD set-up (layers, pens, CTB).

**Tags used:**
- **[STD]** EIT 011006-19 requirement.
- **[REG]** Thai building regulation.
- **[ACI] / [EIT1008]** Design code.
- **[OFF]** Office convention, as used on ST-1.
- **[VERIFY]** Confirm against the current edition before a real issue. Values are quoted from memory of the regulation.

---

## 0. Quick reference

| Item | Rule | Tag |
|---|---|---|
| Views | Plan (every level with a flight) + section along **every** flight + cross-section + support/kink details + bar schedule + notes | [STD §6.7] [OFF] |
| Scales | Section 1:20 (EIT examples 1:25), cross-section and details 1:10, plan 1:50 (1:20 if congested) | [STD] [OFF] |
| Waist | Measured **normal to the soffit**, dimensioned with an aligned dimension | [OFF] |
| Steps | Chain as `n @ R = total` (risers) and `n @ T = total` (treads) | [STD §6.7] |
| Main bars | Run along the span (normally along the slope), 0.50 pen | [OFF] |
| Inside (re-entrant) corner | **Never bend a tension bar around it.** Cross the bars and anchor each one beyond the corner | [ACI practice] |
| Outside (salient) corner | Bar may bend continuously around it | [ACI practice] |
| Top bars at supports | ≥ 0.3 Ln beyond the support face, anchored into the support | [OFF] |
| Bottom bars | ≥ 150 into the support (or full anchorage if continuity is assumed) | [ACI 7.7.3.8] |
| Distribution | ≥ 0.0018 bh; spacing ≤ min(5h, 450); sits **inside** the main bars | [ACI 24.4] |
| Cover | 20 to interior stairs/slabs, 40 where exposed to weather, 75 cast on ground | [OFF] [VERIFY] |
| Mark | `ST1`, `ST2` … on plans, sections and schedule | [STD §10] |

---

## 1. Geometry rules

### 1.1 Terms

| Term | Thai | Meaning |
|---|---|---|
| Riser R | ลูกตั้ง | Vertical rise of one step (finished) |
| Going / tread T | ลูกนอน | Horizontal depth of one step, nosing to nosing (finished) |
| Waist h | ความหนาท้องบันได | Slab thickness **normal to the soffit**, measured from the step roots |
| Pitch θ | ความชัน | `θ = atan(R / T)` |
| Flight | ช่วงบันได | Uninterrupted run of steps between floors or landings |
| Landing | ชานพัก | Horizontal slab between flights or at the ends |
| Headroom | ระยะดิ่งเหนือหัว | Clear vertical height above the pitch line (nosings) |
| Step root | มุมในของขั้น | Inside corner where riser meets tread. The roots lie on one line parallel to the soffit |
| Nosing | จมูกบันได | Outside corner where tread meets riser |

### 1.2 Regulatory limits [REG] [VERIFY]

**Ministerial Regulation No. 55 (B.E. 2543), clauses 22–23:**

| Item | Residential (อาคารอยู่อาศัย) | Public / commercial / office / factory |
|---|---|---|
| Clear width | ≥ 0.80 m | ≥ 1.20 m. Larger occupancies: ≥ 1.50 m, or two stairs ≥ 1.20 m each |
| Riser | ≤ 0.20 m | ≤ 0.18 m |
| Tread (after deducting nosing overlap) | ≥ 0.22 m | ≥ 0.25 m |
| Max. rise of one flight | 3.00 m (then a landing) | 4.00 m (then a landing) |
| Landing length | ≥ stair width | ≥ stair width |
| Headroom | ≥ 1.90 m | ≥ 1.90 m (office: 2.10 m) |

- **Fire escape stairs:** further rules apply (Ministerial Regulations No. 39 / 47 and the high-rise rules). The architect governs.
- **Structural drawings follow the architectural stair geometry.** The structural engineer only checks it and flags non-compliance. Never re-design risers on the structural sheet.

### 1.3 Comfort and consistency checks [OFF]

- **Blondel rule:** `2R + T = 600 – 640 mm`. Pitch 25°–38° for normal stairs.
- **Equal risers:** all *finished* risers in a flight must be equal (tolerance ±5 mm). All treads must be equal.
- **Structural vs finished levels:** the structural profile is drawn, not the finishes.
  - SFL = FFL − floor finish thickness.
  - If the tread finish `t_s` differs from the floor finishes `t_lo` (bottom) and `t_up` (top), only the first and last structural risers change:
    - first structural riser = `R + t_lo − t_s`;
    - last structural riser = `R + t_s − t_up`;
    - all others = R.
  - Note this on the drawing (ST-1 note 8).
- **Riser count:** `NR = round(ΔFFL / R_target)`, then `R = ΔFFL / NR`. There are `NR − 1` treads per flight **between floors**, because the last "tread" is the upper floor or landing.
- **Headroom:** check it graphically on the section. Draw a line 1.90 m (or 2.10 m) above the pitch line and confirm that no beam or slab soffit crosses it.

### 1.4 Geometry formulas (use these in code and hand checks)

```
θ      = atan(R/T)            cosθ = T/√(R²+T²)
root line (through step roots):          y = (R/T)·x                          (x=0 at the first riser)
soffit:                                  y = (R/T)·x − h/cosθ
line d above soffit (normal distance d): y = (R/T)·x − (h − d)/cosθ
line d below root line:                  y = (R/T)·x − d/cosθ
vertical depth at any x (root → soffit) = h/cosθ     (ST-1: 150/0.827 = 181)
inclined length of a horizontal run Lx  = Lx / cosθ
```

---

## 2. Structural systems — choose before drawing

The system decides the main-bar direction, which face is in tension, and where the kinks are.

| Type | Support | Span / main bars | Tension face | Typical waist |
|---|---|---|---|---|
| **A. Waist slab between beams** (ST-1) | Beams at bottom and top of the flight | Along the slope, beam to beam | Soffit (sagging); top at supports (partial fixity) | L/20 simply supported |
| **B. Flight + landing(s) as one slab** (dog-leg / straight with landing) | Beams or walls at the far ends of the landings | Along the folded slab, horizontal span = flight + landing(s) | Soffit, **including the kinks** (§4.4) | L/20 – L/24 |
| **C. Landing spans across** (landing on side beams/walls) | Landing supported on its long edges; flights bear on the landing | Landing: across the stair; flight: along slope to the landing | Soffit | Landing L/28 continuous |
| **D. Stringer (edge beams)** | Inclined beams along the flight edges | **Across** the flight (step to step); stringers along the slope | Step soffit, transverse | 100–120 + steps |
| **E. Cantilever steps** | Wall or central spine beam | Across, cantilever from the wall | **Top** face (hogging) | Cantilever L/10 |
| **F. On grade** | Ground | Nominal (mesh) | — | 100–150 |

**Rules:**
- **Span for moments:** the horizontal projection, with the load per horizontal m² (§3). Span for the thickness check: the inclined length, which is conservative.
- **Mark every support:** show and tag each supporting beam or wall on the section (`B1 200x400 – SEE BEAM SCHEDULE`). A stair must never "float".
- **Landings in type B:** a landing is part of the span and needs top and bottom mats [STD FIG 6.12–6.13].
- **Transverse main bars (types D/E):** the section across the flight becomes the main reinforcement view. The plan shows the bar direction with the EIT one-way arrow [STD §12.2-6].

---

## 3. Design basis and minimum checks

### 3.1 Loads [REG] [VERIFY]

- **Live load (Ministerial Regulation No. 6, B.E. 2527):**
  - stairs in residential buildings 300 kg/m² (3.0 kPa);
  - offices, commercial and schools 400 kg/m²;
  - assembly, markets and department stores 500 kg/m².
- **Superimposed dead load:** finishes 1.0 kPa (tile or granite on mortar). Add the balustrade as a line load if it is heavy.
- **Self-weight** per horizontal m² (γc = 24 kN/m³):

```
w_self = γc · ( h / cosθ + R / 2 )         (waist + half step)
ST-1:  24 × (0.150/0.8269 + 0.170/2) = 4.35 + 2.04 = 6.39 kPa
```

### 3.2 Strength [EIT1008] [ACI]

- **Load factors:** U = 1.4D + 1.7L (EIT 1008-38). Flexure φ = 0.90; shear φ = 0.85.
- **Simply supported moment:** `Mu = wu·L²/8`, with L = horizontal span between the support centres.
- **Effective depth:** `d = h − cover − db/2`.
- **Capacity check:** `As` from `Mu ≤ φ As fy (d − a/2)`, with `a = As fy / (0.85 fc' b)`.
- **Shear:** rarely governs; check `Vu ≤ φ 0.53√fc' b d` (ksc units).

**ST-1 worked example:**
```
wu = 1.4(6.39 + 1.0) + 1.7(3.0) = 15.45 kPa         L = 2.45 m (c/c beams, horizontal)
Mu = 15.45 × 2.45² / 8 = 11.6 kN·m/m
d  = 150 − 20 − 6 = 124 mm ;  DB12@200 → As = 565 mm²/m
a  = 565×390 / (0.85×23.5×1000) = 11.0 mm
φMn = 0.9×565×390×(124 − 5.5) = 23.5 kN·m/m  ≥ 11.6  OK
```

### 3.3 Minimums and serviceability [ACI]

| Check | Rule | ST-1 |
|---|---|---|
| Min. thickness, simply supported | h ≥ L/20 (one end continuous L/24, both L/28, cantilever L/10); fy 390 → ×0.96 | 150 ≥ 2963/20 = 148 |
| Min. main steel | ≥ 0.0018 bh | 565 ≥ 270 |
| Distribution steel | ≥ 0.0018 bh | DB10@200 = 393 ≥ 270 |
| Main bar spacing | ≤ min(3h, 450) | 200 |
| Distribution spacing | ≤ min(5h, 450) | 200 |
| Top bars at a "simple" support built monolithic | ≥ As,min, extended ≥ 0.3 Ln | DB12@200, 700 ≥ 675 |
| Bottom bar into support | ≥ 150 | 150 |

**Rules:**
- Put the design summary in the sheet notes (ST-1 note 4) so the checker sees the basis without the calculation sheet.
- Keep the calculation file with the job.
- Minimum bar size [OFF]: main DB12, distribution DB10.

---

## 4. Reinforcement detailing

### 4.1 Bar layers and covers (type A/B)

Numbered from the soffit upward:

1. **(1) Bottom main**, along the span. Centre = cover + db/2 above the soffit (ST-1: 20 + 6 = 26).
2. **(4) Bottom distribution**, across, sitting **on** (1). Centre = cover + db1 + db4/2 (ST-1: 37).
3. **(4) Top distribution**, across, **under** the top bars.
4. **(2)/(3) Top bars** at the supports, along the span. Centre = cover + db/2 below the **step-root line** (not below the treads).

**Rules:**
- **Distribution position:** distribution bars always go **inside** the main bars, so the main bars get the full effective depth.
- **Steps are unreinforced concrete** by default.
- **Nosing bar** [STD FIG]: EIT examples show a nosing bar. Provide `1-DB10` per step, tied to an `RB6` hairpin anchored in the waist, when:
  - the steps are wider than 1.5 m;
  - the stair is external;
  - the architect specifies a cast nosing.
  
  If omitted, say so in the notes (ST-1: not provided).

### 4.2 Ends at supports

| End condition | Bottom bars | Top bars |
|---|---|---|
| Monolithic with a beam (ST-1) | Straight ≥ 150 into the beam, stop 50 from the far face | ≥ 0.3 Ln from the face; anchored with a 90° hook (≥ 12 db) turned **down into the beam** |
| Bearing on a wall | Straight to 50 from the far face | As above, hooked into the wall/bond beam |
| Continuous into a floor slab or landing | See kinks §4.4 | Lap with the slab top bars (class B) |
| Cast later than the floor (construction joint at the beam face) | Starter bars left in the beam: same size and spacing, lap class B | Same |

**Rules:**
- **Bar ends inside a beam:** keep them clear of the beam cage.
  - Bar ends stop ≥ 50 from the far face.
  - Hook legs sit ≥ 15 clear of stirrup legs and corner bars.
  - At ST-1 B2, (3) stops 70 from the far face so its bend clears the upper slab's bottom bars.
- **Hook legs are drawn vertical**, not normal to the bar. A vertical leg stays inside a rectangular beam and is easy to fix. The bend angle is then 90° ± θ.

### 4.3 Hooks, bends and laps [ACI] [OFF]

- **Bends:** inside diameter 6 db (drawn at centreline R = 3.5 db). 90° hook extension ≥ 12 db. 180° hook ≥ 4 db and ≥ 65.
- **Tension laps (class B, fc' 240, SD40), office values:**
  - DB10 = 500;
  - DB12 = 600;
  - DB16 = 800 (about 50 db).
  
  Stagger 50 %. **No laps in the flight main bars** when the flight is shorter than stock length (10 m). State "NO LAPS" on the bar label.

### 4.4 Kinks — flight/landing and flight/floor junctions (the critical detail)

A kink is where the inclined flight meets a horizontal slab (landing or floor). At every kink, one face turns an **inside (re-entrant) corner** and the other face turns an **outside (salient) corner**.
- **Why it matters:** a tension bar bent around an inside corner tries to straighten. The resultant pushes outward through the cover and spalls it off.
- **Rule:** at an inside corner the bars must **cross**. Each bar runs straight past the corner and is anchored (≥ ld, or hooked) in the other member.
- The same rule was applied to the slab steps on sheet 1126 (2026-09-29, ACI SLAB-204). There, the lower bottom bars run up the haunch and straight on to the upper-slab top layer, and the upper bottom bars cross the corner.

```
 LOWER KINK (floor/landing → flight going up)       UPPER KINK (flight → floor/landing above)

            /  flight top                              landing top ___________
 _________ /  ← TOP face = INSIDE corner                          |  ← TOP face = OUTSIDE corner
 landing    \   (top bars must CROSS)                  ___________/
 ___________ \                                        /  ← SOFFIT = INSIDE corner
             ↑ SOFFIT = OUTSIDE corner               /     (bottom bars must CROSS — critical,
               (bottom bar may bend round)          /       they carry the span moment)
```

| Kink | Inside-corner face | Bars that must cross | Outside-corner face (bars may bend) |
|---|---|---|---|
| Lower (landing/floor → flight up) | **Top** | Landing top bars run straight up into the flight; flight top bars run straight into the landing/beam | Soffit: bottom bar may follow the soffit around the corner |
| Upper (flight → landing/floor above) | **Soffit** | Flight bottom bars run straight into the landing, anchored ld to the landing **top**; landing bottom bars run straight into the flight, anchored ld | Top: top bar may bend over the nosing line |

**ST-1:**
- At B1 the top face is an inside corner at x = 0. Bar (2) therefore runs straight on down into B1 and hooks, instead of bending along the floor.
- At B2 both faces end in the beam, so both (1) and (3) terminate in B2.
- Write the rule as a note (ST-1 note 6).

**Drawing a kink detail:**
- Scale 1:10.
- Show both crossing bars with their anchorage lengths dimensioned from the corner.
- Label each bar at its crossing.

### 4.5 Bar marks (ST-1 numbering, keep for new stairs)

| Mark | Bar | Content |
|---|---|---|
| (1) | DB12@200 | Bottom main, along the slope |
| (2) | DB12@200 | Top at the lower support |
| (3) | DB12@200 | Top at the upper support |
| (4) | DB10@200 | Distribution, bottom and top (one mark, both layers) |
| (5)… | — | Landing bars, nosing bars, starter bars, crossing bars at kinks |

**Rules:**
- **Count across the flight:** `n = (WID − 2·edge)/s + 1`. ST-1 has the first bar at 100 from the edge (`5 @ 200 = 1000` + 100 + 100 = 6 bars).
- **Distribution count:** along the slope at @s from 100 inside each beam face. Bottom layer over the full clear slope length; top layer only under (2) and (3).

---

## 5. Required views and sheet layout

### 5.1 Content [STD §6.7] + [OFF]

1. **Stair plan** at each level with a flight, 1:50 (1:20 for complex stairs). It must show:
   - flight outline;
   - one line per nosing, in thin seen concrete;
   - riser numbers `1 … NR` from the bottom;
   - walking line with a start circle and an arrowhead, plus `UP` (on upper-level plans `DN` from the same end);
   - supporting beams **hidden** (dashed grey) with `B1 (BELOW)`;
   - floor/landing levels `FFL ±0.000`;
   - cutting planes for every section;
   - dimensions: `n @ T = total` going, beam widths, flight width;
   - stair mark `ST1`.
2. **Longitudinal section along each flight**, 1:20 (EIT examples 1:25). It must show:
   - span;
   - waist;
   - tread and riser chain;
   - all reinforcement;
   - supports with their tags;
   - levels;
   - handrail fixings, or "SEE ARCH.";
   - stair mark.
3. **Cross-section** normal to the flight or vertical at mid-tread, 1:10. It must show:
   - bar spacing across the width;
   - top/bottom layers;
   - edge distances;
   - flight width.
4. **Kink and support details**, 1:10, wherever bars cross or anchor in congested beams (§4.4).
5. **Bar schedule** for one flight (§8).
6. **Notes:** materials, cover, design basis, kink rule, finishes, construction joints (§9).
7. **Legend** of lines and bar symbols, recommended on stand-alone stair sheets.

### 5.2 ST-1 sheet arrangement (A3, one sheet)

```
┌──────────────────────────────────────────────┬──────────────────┬──────┐
│ SECTION A-A  1:20  (≈224 × 128)               │ BAR SCHEDULE     │ TITLE│
│                                              │ NOTES 1–9        │ STRIP│
├──────────────┬───────────────────────────────┤                  │ 70 mm│
│ PLAN 1:50    │ SECTION B-B 1:10              │                  │      │
├──────────────┴───────────────────────────────┴──────────────────┤      │
│ LEGEND – LINES & REINFORCEMENT (two columns)                      │      │
└───────────────────────────────────────────────────────────────────┴──────┘
```

**Rules:**
- **Titles:** view titles sit 6 mm below each viewport, left-aligned [§19.5].
- **Bubbles:** the section bubble has triangles, with the letter on top and the sheet number below.
- **Plan title note:** carries the step totals (`10 RISERS @ 170 = 1700, 9 TREADS @ 250`) when the plan is too small for them.

---

## 6. Line presentation

### 6.1 Pens and layers (A3 originals; plot `NRW-EIT.ctb`)

| What | Layer | Pen | Linetype | Plotted |
|---|---|---|---|---|
| Stair bars along their length: (1), (2), (3) | `S-REBR` | **0.50** | Continuous | Black |
| Distribution bars (4); bars of beams/slabs by others; beam stirrups | `S-REBR-SEC` | 0.35 | Continuous | Black |
| Concrete **cut**: flight profile, beams, slab stubs in section | `S-CONC` | **0.35** | Continuous | Black |
| Concrete **seen**: nosing lines and edges in plan | `S-CONC-VIS` | 0.25 | Continuous | Black |
| Beams below, in plan | `S-CONC-HIDN` | 0.25 | `EIT_HIDDEN` 3.0/1.5 | Grey |
| Cutting plane | `S-CUTL` + `S-CUTL-END` | 0.25 + **0.50** end strokes (5 mm) | `EIT_CENTER` | Black |
| Cut arrows, bar-mark bubbles, section bubbles | `S-SYMB` | 0.25 | Continuous | Black |
| Leaders, walking line, level marks | `S-ANNO` | 0.18 | Continuous | Black |
| Dimensions | `S-DIMS` | 0.18 (extension lines grey, ACI 8) | Continuous | Black / grey |
| Break lines | `S-BREAK` | 0.18 | Continuous (single Z) | Grey |
| Text | `S-TEXT` / `S-TITLE` | — | Arial Narrow 2.0 / 2.8 bold | Black |

**Hierarchy check** (it must read at a glance):
- stair bars 0.50 > cut concrete 0.35 = secondary bars 0.35 > seen 0.25 > annotation 0.18 > grey;
- **stair steel must stand out from the beam steel** of the supports.

### 6.2 What to draw, and how

- **Step profile:** draw the **structural** profile only, as one continuous 0.35 polyline from the lower slab break to the upper slab break. Draw the soffit and beam outlines as a second polyline.
  - Do not draw finishes or nosing strips on the structural section.
  - Do not hatch RC [§19.6].
- **Supports:**
  - Draw the supporting beams complete in section: outline, plus an RB6 stirrup with R = 3.5 db corners and 4 corner dots, all in 0.35.
  - Break floor slabs 700–900 beyond the beam, with a single-Z break line.
  - Show the slab top and bottom bars thin, labelled `FLOOR SLAB (BY OTHERS)`.
- **Bars along their length:**
  - Draw on the bar centreline.
  - Bends filleted at R = 3.5 db (the `bar()` helper), never sharp.
  - Hook legs vertical.
- **Bars cut in section:**
  - Filled dots, true size, min. 1.1 mm plotted.
  - **At 1:20**, a distribution dot at its true position would merge with the 0.50 main-bar line. Draw it `r + pen/2 + 0.4 mm` clear of the main bar instead, i.e. schematic position [§19.4].
  - At 1:10 true positions are fine.
- **Cross-section at 1:10:**
  - main bars as dots;
  - distribution bars as continuous lines, from cover + 5 to the opposite cover + 5;
  - top and bottom layers both shown;
  - note "STEPS BEYOND NOT SHOWN" if they are omitted.
- **Plan:**
  - nosing lines: one per riser, thin continuous;
  - flight edges continuous;
  - beams below dashed grey;
  - walking line: start circle Ø1.6 mm, 2.5 mm arrowhead at the top, `UP` in 2.8 bold;
  - riser numbers 2.0 mm, just right of each nosing line, near the far edge;
  - no reinforcement in plan unless the bar direction changes (types D/E).
- **Cutting planes:** chain line through the stair, 5 mm heavy end strokes, 5 mm arrows pointing the **viewing** direction, letter 2.8 bold beyond each end.
  - Section A-A is cut along the flight, viewed from the side.
  - Section B-B is cut across mid-tread, looking **up** the flight.

---

## 7. Annotation and dimensions

### 7.1 Notes and leaders (see `ANNOTATION_ALIGNMENT_GUIDE.md`)

- **Leaders:** 45°/60° leg + horizontal run + 3 mm shelf, then a Ø4 bar-mark bubble, then the text.
- **Terminators:**
  - 2 mm filled arrow with its tip on the **edge** of a bar drawn along its length;
  - open ring Ø = 2 × dot on a bar cut in section.
- **Units:** every measured value in a note carries its unit ("COVER 20 mm"); dimension figures stay bare
  (`ANNOTATION_ALIGNMENT_GUIDE.md` §2.4.2, user rule 2026-10-03).
- **Where the notes go on a stair section** — the flight fills a diagonal band, so use the two empty triangles:

| Zone | Use for | Engine setting (ST-1) |
|---|---|---|
| Above the lower floor, left of the first riser | Top bars and top distribution at the **lower** support | `L` column, `xL = −110`, `yminL = +90` (clear of the level mark) |
| Under the soffit, between the beams | Bottom main (1), bottom distribution (4) | `B` row, `yB = −140`, `xmaxB = XTOP − 80` |
| Above the steps, left of the upper floor | Top bars at the **upper** support | **fixed** note, knee (1700, 1660), side `L` |
| Beside each beam | Beam tag `B1 200x400 / SEE BEAM SCHEDULE` (plain text, no leader) | Under the lower slab / right of the upper beam |

**Rules:**
- **Clear space:** never run note text across the steps or the flight. Leader legs may cross an outline once.
- **Where to point:** label each bar mark **once** per view, on the most open part of the bar. Label (4) once for each layer.
- **Label contents:** size@spacing, position (TOP/BOTTOM/DIST.), extent (`700 BEYOND FACE OF B1`), anchorage (`HOOKED 150 INTO B1`, `150 INTO B1 & B2`), `NO LAPS`.
- **Cross-section:** a right-hand column, one line per bar, with rings on the end bars.

### 7.2 Dimensions

| Dimension | How | ST-1 |
|---|---|---|
| Support widths + clear span | Horizontal chain below the beams, then an overall dimension on a second tier | `200 | 2250 CLEAR | 200`, `2650` |
| Typical step | One tread and one riser at a mid-flight step, suffix `TYP.`; totals as `n @ R = total` | `250 TYP.`, `170` |
| Waist | **Aligned** dimension normal to the soffit, at a mid-span point clear of the top bars | `150` |
| Levels | EIT triangle on each floor/landing surface: `±0.000 FFL`, `+1.700 FFL` (m, 3 dp) | — |
| Bar extents | In the bar label (`700 BEYOND FACE`) or by dimension on a 1:10 detail | — |
| Cross-section | Edge → first bar → `n @ s = total` → edge; then `WID FLIGHT WIDTH` | `100 | 5 @ 200 = 1000 | 100`, `1200` |
| Plan | Beam widths + `n @ T = total` going chain; flight width | `200 | 9 @ 250 = 2250 | 200`, `1200` |

**Rule:** do not dimension derived values, such as the vertical depth at a cut. They confuse the setting-out.

---

## 8. Bar schedule

- **Columns:** `MARK | BAR | SHAPE | DIM. (mm) | NO. | CUT m | kg | REMARKS`, 92 mm wide in the right column.
- **Title:** `BAR SCHEDULE – ONE FLIGHT`, followed by a total line with kg per bar size and the flight total.
- **Dimensions** out-to-out:
  - inclined straight lengths are `A = horizontal extent / cosθ`;
  - hook legs `B` are **vertical** legs;
  - cut length = ΣA,B (indicative; state it).
- **Shapes:** `–` straight; `J` inclined with a vertical hook. Draw the sketches in `S-REBR`.
- **Nominal mass (TIS 24):** DB10 0.617, DB12 0.888, DB16 1.578 kg/m.

**ST-1 values:**

| Mark | Bar | Dims | No. | Cut (m) | kg |
|---|---|---|---|---|---|
| 1 | DB12 | A = 3060 | 6 | 3.06 | 16.3 |
| 2 | DB12 | A = 1030, B = 150 | 6 | 1.18 | 6.3 |
| 3 | DB12 | A = 1005, B = 150 | 6 | 1.15 | 6.1 |
| 4 | DB10 | A = 1160 | 21 (13 B + 8 T) | 1.16 | 15.0 |
| Total | | | | | 43.8 kg / flight |

---

## 9. Notes block (template — edit the numbers per job)

1. Scope, and "CONFIRM LEVELS, RISERS AND WIDTH WITH THE ARCHITECTURAL DRAWINGS".
2. Concrete fc' ≥ 240 ksc (cylinder, 28 d), ready-mixed to TIS 213; deformed bars SD40 to TIS 24; round bars SR24 to TIS 20.
3. Clear cover: 20 stair and slabs, 30 beam stirrups (exposed: 40).
4. Design basis: LL, finishes, load factors, span, Mu ≤ φMn, waist check.
5. Distribution steel ratio.
6. Kink rule: "TOP BARS … RUN STRAIGHT PAST THE RE-ENTRANT CORNERS … DO NOT BEND BARS AROUND AN INSIDE CORNER."
7. Bends on a 6 db mandrel; laps (or "NO LAPS").
8. Structural step profile; finishes by the architect; equal finished risers.
9. Casting sequence: monolithic with the supports, or starter bars; no construction joint in a flight.
10. (When applicable) Handrail/balustrade fixings: cast-in plates or post-drilled anchors to the architect's detail; keep anchors ≥ 50 from the bars and the nosing.

---

## 10. Generator (`jobs/stair_demo/`)

### 10.1 Files

| File | Purpose |
|---|---|
| `build_stair.py` | Builds `out/STR-ST_Stair_ST-1_A3_RevA.dxf`. The engine (helpers, dimension styles, annotation engine, title block) is copied from `jobs/nooker_rw/build_rw.py`, with two additions: `leader(..., fixed=True)` and `dim(..., text=...)` |
| `plot_stair.py` | Runs accoreconsole: plots to PDF with `NRW-EIT.ctb`, SAVEAS a 2018 DWG. **Script paths are quoted** |
| `_render.py` | Renders `out/_p.png` (and optional clips `name:x0,y0,x1,y1:dpi` in sheet mm from the top-left) for visual checks |

**Build** (from PowerShell, never from Git Bash — accoreconsole will not run scripts from there):

```bash
python build_stair.py out
```
```bash
python plot_stair.py out
```
```bash
python _render.py
```

### 10.2 Parameters (top of the "STAIR ST-1 geometry" block)

| Name | ST-1 | Meaning |
|---|---|---|
| `NR`, `RH`, `TG` | 10, 170, 250 | Risers, riser height, going |
| `WS`, `WID` | 150, 1200 | Waist (normal), flight width |
| `C_SL` | 20 | Clear cover |
| `B1X0/B1X1/B1YB`, `B2X0/B2X1/B2YB` | beams 200×400, 200×500 | Support beams (x from the first riser, y from the lower FFL) |
| `HS`, `XL`, `XR` | 120, −900, XTOP+900 | Slab stub thickness and break-line positions |
| `LTOP`, `HOOK` | 700, 150 | Top-bar extent beyond the face, hook leg |
| `XE1`, `XE2` | B1X0+50, B2X1−70 | Bar-end positions inside the beams |
| `D1`, `D2`, `D4` | 26, 26, 37 | Bar centre distances (normal) |
| `XBB` | 375 | Position of cross-section B-B |

**What updates automatically when you change a parameter:**
- all geometry, bars, dimensions and levels;
- distribution-dot positions (`S4B`, `S4T1`, `S4T2`);
- bar counts (`N_ACROSS`) and schedule cut lengths;
- plan nosings and riser numbers.

**What must be edited by hand:**
- the text in `NOTES` (design numbers, Mu, φMn, span, thickness check); re-run the design check first (§3);
- the level strings `±0.000` / `+1.700` in `section_aa`;
- the beam tags `B1 200x400`, `B2 200x500`;
- the note **tip x-positions** (350, 700, 2150) and the **fixed knee** `(1700, 1660)` in `section_aa`. They must stay in the free triangle above the steps and left of the upper floor, at about `(XTOP − 550, FFL1 − 40)`;
- the typical-step index `i = 5` and the waist-dimension position `xw = 1250`. Keep them mid-flight and clear of the top bars;
- the sheet layout in `sheet_5101()` if a view grows (watch the printed `vp` sizes; the viewport must stay left of `TBX` = 340).

### 10.3 Pitfalls met on ST-1

- **Spaces in the output path:** a space in an AutoCAD script is Enter. An unquoted `C:\990 - Developing software\…` path hangs the plot at the file-name prompt. Quote every path.
- **Missing dimension styles:** `DS` must contain every view scale used, including 1 (legend samples on paper) and 50 (plan). A missing one raises `KeyError`.
- **Override text:** use `dim(..., text="5 @ 200 = 1000")`. An `override={"text": ...}` is silently ignored.
- **Fixed notes:** in the original NRW engine, `free=True` notes are drawn before the bars are collected, so their arrow tips can land inside bar lines. In `build_stair.py`, `free=True` views and `fixed=True` notes are both drawn after collection, so the edge rule applies. Use `fixed=True` to pin one note while the rest of the view is packed automatically.
- **Section B-B width:** B-B at 1:10 is about 170 mm wide with its note column. Plan at 1:25 does not fit beside it on A3, so use 1:50.

---

## 11. Pre-issue checklist (stairs)

**Geometry**
- [ ] Risers equal (finished) and within the regulation; treads equal; 2R + T in range; headroom checked on the section.
- [ ] First and last structural risers adjusted for finish differences, and noted.
- [ ] Levels (FFL) on every floor and landing, in m with 3 dp; they agree with the architectural drawings.

**Structure**
- [ ] Every support shown and tagged; the span shown as a dimension; the design summary is in the notes.
- [ ] Waist ≥ L/20 (or L/24, L/28); main steel ≥ φMn demand; distribution ≥ 0.0018 bh.

**Reinforcement**
- [ ] Main bars along the span with correct cover; distribution **inside** the main bars.
- [ ] Top bars at each support ≥ 0.3 Ln and anchored; bottom bars ≥ 150 into the supports.
- [ ] **Every inside corner has crossing bars; no bar bent around an inside corner.**
- [ ] Hook legs inside the beam cage; bar ends ≥ 50 from the far face; no clash with beam or slab bars.
- [ ] Bar marks consistent across the section, cross-section and schedule; each mark labelled once per view.
- [ ] Schedule counts and lengths match the drawing; total mass given.

**Presentation**
- [ ] Pens: stair bars 0.50 > concrete cut 0.35 / secondary bars 0.35 > seen 0.25 > annotation 0.18; grey for hidden, breaks and extension lines.
- [ ] RC not hatched; finishes not drawn on the structural section.
- [ ] Leaders at 45°/60° with shelves; arrow tips on bar edges; rings on cut bars; no text over the flight.
- [ ] Waist dimension aligned normal to the soffit; step chains `n @ R = total`.
- [ ] Plan: nosings, riser numbers, walking line + `UP`/`DN`, hidden beams, cutting planes with arrows and letters, stair mark.
- [ ] Section bubbles reference the correct sheet; title block, revision and status stamp complete.
