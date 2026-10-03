# Column detailing sources: DPT 1301/1302-61 and the TATA RC detailing handbook (extracts)

These are the reference extracts behind the typical column details (`STR-ST-1101`, `STR-ST-1102`, `TYPICAL_DETAILS_INSTRUCTION.md`).

| Part | Source | PDF pages |
|---|---|---|
| A | DPT 1301/1302-61 (`G:\My Drive\##Textbook\DPT\1301-1302-64.pdf`) | pp. 49–56 and 104–118 |
| B | DPT 1301/1302-61 | pp. 118–146 |
| C | TATA *Steel Reinforcing Bar Handbook / RC Detailing* by M. Jiravacharadet (2017) | column chapter, hooks, laps, footings, typical sheets |

Notes:
- The wording is paraphrased; the figures are described so they can be redrawn.
- Check the originals before quoting a clause.

---


Source: `G:\My Drive\##Textbook\DPT\1301-1302-64.pdf`. I checked every table, equation and figure against the rendered page images.
Ranges covered: PDF pp. 49–56 (printed pp. 35–42) and PDF pp. 104–118 (printed pp. 90–104).
Wording below is paraphrased. Thai category letters: ก = A, ข = B, ค = C, ง = D. This file keeps the Thai letter and adds the Latin letter in brackets.

Legend: **[COL]** marks a clause that governs columns directly.

---

## 1.6 Seismic design category (PDF p.49–50)

- There are 4 categories: ก [A], ข [B], ค [C] and ง [D].
  - ก [A]: no seismic design is required.
  - ง [D]: the most stringent category.
- The category depends on two inputs:
  - the building importance category (Table 1.5-1);
  - site spectral accelerations S_DS and S_D1 (clause 1.4.4), taken at 5 % damping for all buildings.

**Table 1.6-1: category by S_DS**

| S_DS | Importance I or II | Importance III | Importance IV |
|---|---|---|---|
| S_DS < 0.167 | ก [A] (no design) | ก [A] (no design) | ก [A] (no design) |
| 0.167 ≤ S_DS < 0.33 | ข [B] | ข [B] | ค [C] |
| 0.33 ≤ S_DS < 0.50 | ค [C] | ค [C] | ง [D] |
| 0.50 ≤ S_DS | ง [D] | ง [D] | ง [D] |

**Table 1.6-2: category by S_D1**

| S_D1 | Importance I or II | Importance III | Importance IV |
|---|---|---|---|
| S_D1 < 0.067 | ก [A] (no design) | ก [A] (no design) | ก [A] (no design) |
| 0.067 ≤ S_D1 < 0.133 | ข [B] | ข [B] | ค [C] |
| 0.133 ≤ S_D1 < 0.20 | ค [C] | ค [C] | ง [D] |
| 0.20 ≤ S_D1 | ง [D] | ง [D] | ง [D] |

Rules for choosing between the two tables:

- **Bangkok basin:**
  - S_DS and S_D1 are the equivalent-static design spectral accelerations S_a at T = 0.2 s and T = 1.0 s (5 % damping), from Table 1.4-5.
  - If T ≤ 0.5 s, use Table 1.6-1 only.
  - If T > 0.5 s, use Table 1.6-2 only.
  - T is the fundamental period from Eq. 3.3-1 or 3.3-2.
- **Rest of the country (outside the Bangkok basin):**
  - If the two tables give different categories, use the more severe one.
  - Exception: if T (Eq. 3.3-1 or 3.3-2) < 0.8 T_s, Table 1.6-1 alone may be used. T_s is defined in clause 1.4.5.

---

## 2.1–2.2 General (PDF p.51–52), brief

- **2.1:**
  - Provide both a lateral-load-resisting system and a gravity system, with enough strength, stiffness and energy dissipation for the design earthquake.
  - The design earthquake may act in any horizontal direction.
  - Distribute storey forces per clause 3.4 (or an equivalent proven method).
- **2.2.1:** All members, including members outside the lateral system, must resist the seismic shear, axial force and moment. Connections must develop the forces in the members they connect. Drift is limited per clause 2.11.
- **2.2.2:** Provide a continuous load path.
- **2.2.3:** Where a part of the structure is connected to a diaphragm, design its connection for a horizontal force ≥ **5 %** of the vertical (D + L) support reaction.
- **2.2.4:** Foundations per clause 2.12.
- **2.2.5:** Detail all members, including foundations, per Chapter 5.

## 2.3 Selection of structural system (PDF p.52–56)

### 2.3.1.1 Classification

- The lateral and gravity system must be one of the systems in Table 2.3-1, or a combination per clauses 2.3.2–2.3.4.
- Which systems are permitted depends on the seismic design category.
- R, Ω0 and C_d are taken from Table 2.3-1. They are used for base shear, element design forces and storey drift (Chapters 3 and 4).
- Detailing must follow the referenced standards plus Chapter 5.
- A system not listed in the table must be justified by analysis and/or laboratory tests. The tests must show dynamic behaviour, lateral strength and energy dissipation equivalent to a listed system with the same R, Ω0 and C_d.

### Table 2.3-1: R, Ω0, C_d and permitted categories

Columns ข/ค/ง = categories B, C, D. Symbols: √ = permitted; × = not permitted; * = see 2.3.1.2 (height limit); ++ = see 2.3.1.3 (precast).

| Overall system | Lateral-force-resisting system | R | Ω0 | C_d | ข [B] | ค [C] | ง [D] |
|---|---|---|---|---|---|---|---|
| 1. Bearing wall system | Ordinary RC shear wall | 4 | 2.5 | 4 | √ | √ | * |
| | Special RC shear wall | 5 | 2.5 | 5 | √ | √ | √ |
| | Ordinary precast shear wall ++ | 3 | 2.5 | 3 | √ | × | × |
| | Intermediate precast shear wall ++ | 4 | 2.5 | 4 | √ | √ | × |
| 2. Building frame system | Steel eccentrically braced frame, moment-resisting connections | 8 | 2 | 4 | √ | √ | √ |
| | Steel eccentrically braced frame, non-moment-resisting connections | 7 | 2 | 4 | √ | √ | √ |
| | Special steel concentrically braced frame | 6 | 2 | 5 | √ | √ | √ |
| | Ordinary steel concentrically braced frame | 3.5 | 2 | 3.5 | √ | √ | × |
| | Special RC shear wall | 6 | 2.5 | 5 | √ | √ | √ |
| | Ordinary RC shear wall | 5 | 2.5 | 4.5 | √ | √ | * |
| | Ordinary precast shear wall ++ | 4 | 2.5 | 4 | √ | × | × |
| | Intermediate precast shear wall ++ | 5 | 2.5 | 4.5 | √ | √ | × |
| 3. Moment-resisting frame system | Ductile/special steel MRF | 8 | 3 | 5.5 | √ | √ | √ |
| | Special truss moment frame | 7 | 3 | 5.5 | √ | √ | √ |
| | Intermediate steel MRF | 4.5 | 3 | 4 | √ | √ | * |
| | Ordinary steel MRF | 3.5 | 3 | 3 | √ | √ | × |
| | **Ductile/special RC MRF** (cast-in-place or precast ++) | **8** | **3** | **5.5** | √ | √ | √ |
| | **RC MRF with limited ductility / intermediate RC MRF** | **5** | **3** | **4.5** | √ | √ | * |
| | **Ordinary RC MRF** | **3** | **3** | **2.5** | √ | **×** | **×** |
| 4. Dual system with ductile/special MRF, where the MRF alone resists ≥ 25 % of the total lateral force | + special steel concentrically braced frame | 7 | 2.5 | 5.5 | √ | √ | √ |
| | + steel eccentrically braced frame | 8 | 2.5 | 4 | √ | √ | √ |
| | + special RC shear wall | 7 | 2.5 | 5.5 | √ | √ | √ |
| | + ordinary RC shear wall | 6 | 2.5 | 5 | √ | √ | * |
| 5. Dual system with intermediate / limited-ductility MRF, where the MRF alone resists ≥ 25 % of the total lateral force | + special steel concentrically braced frame | 6 | 2.5 | 5 | √ | √ | × |
| | + special RC shear wall | 6.5 | 2.5 | 5 | √ | √ | √ |
| | + ordinary RC shear wall | 5.5 | 2.5 | 4.5 | √ | √ | * |
| 6. Shear wall–frame interactive system | Ordinary RC MRF + ordinary RC shear wall, without ductile detailing | 4.5 | 2.5 | 4 | √ | × | × |
| 7. Steel systems not specifically detailed for seismic resistance | same | 3 | 3 | 3 | √ | √ | × |

The table has no height-limit column. The only height limits are those in 2.3.1.2.

**What this means for RC frames:**

- Ordinary RC MRF: category ข [B] only.
- Intermediate RC MRF:
  - categories ข [B] and ค [C] without restriction;
  - category ง [D] only with the 2.3.1.2 limits (≤ 40 m, forces +40 %).
- Special RC MRF: all categories.

### 2.3.1.2 Height limits in category ง [D] (the * entries)

The following systems may be used in category ง [D] only up to these heights:

1. **40 m**: intermediate / limited-ductility RC moment frames, and intermediate steel moment frames.
2. **60 m**: ordinary RC shear walls.

Where these are used:

- Increase the seismic forces for member strength design by **40 %**. No increase is needed for drift calculations.
- For taller buildings, verify limit states (concrete and steel strains, shear, etc.) under the design earthquake and the maximum considered earthquake. Use accepted methods, or tests that confirm member performance.

### 2.3.1.3 Precast systems (++)

- Members and joints must have adequate strength and ductility for the seismic level, for axial force, shear, moment and torsion.
- Use accepted design standards.
- A form that has not been tested needs lab evidence of equivalent behaviour, strength, energy dissipation and failure mode.
- Where a member is much weaker in one direction, consider progressive collapse and design to prevent it.

### 2.3.2 Different systems in the two orthogonal directions

Permitted. Use the R, Ω0 and C_d of the system in each direction.

### 2.3.3 Combined systems in one direction

Permitted. Apply the most stringent requirements to all participating systems. The detail continues on PDF p.57, outside this range.

---

## 5.1.3 (end, PDF p.104), brief

In category ง [D]:

- Steel H-piles follow AISC 341.
- The joint between pile cap and a steel pile or unfilled steel pipe pile must resist tension ≥ **10 %** of the pile's compressive capacity.

## 5.2 Reinforced concrete structures (PDF p.104)

- RC buildings, including foundations, must be designed and detailed per this standard, the referenced standards and this chapter.
- Chapter 5 does not cover precast-element systems or composite systems, except precast concrete piles.

### 5.2.1 Related standards

Where this standard is silent, use **ACI 318** (Building Code Requirements for Structural Concrete) or other accepted standards.

### 5.2.2 Seismic-resisting system requirements [COL: system choice]

- **(ก)** Category ข [B]: ordinary, intermediate or special systems are all allowed. Design forces and detail per the relevant design standard.
- **(ข)** Category ค [C]: allowed systems are
  - intermediate or special moment frames;
  - ordinary, intermediate or special RC walls.
- **(ค)** Category ง [D]:
  - Use special moment frames or special walls, or follow 2.3.1.2 (intermediate frames up to 40 m).
  - Diaphragms, trusses and foundations must also be seismically designed and detailed.
  - Members not designed as part of the lateral system: design them for gravity load combined with the effects of the design lateral displacement.
- **(ง)** Intermediate moment frames in "watch" areas (possible stability effects from earthquakes):
  - Follow at least clause **5.2.7.4** (column detailing).
  - If the structure is a flat slab, also follow 5.2.12.

### 5.2.3 Concrete piles, category ค [C] (PDF p.105–107), brief

- **(ก) Concrete and concrete-filled pipe piles:**
  - Anchor to the cap by embedding pile bars ≥ development length, or with dowels that develop yield.
  - Provide confinement near the pile head, measured below the cap underside.
  - Cutting the pile head must not shorten the confined length.
- **(ข) Uncased piles:**
  - At least **4** longitudinal bars, with ρ ≥ **0.0025**.
  - Provide transverse steel over the minimum reinforced length.
  - Extend longitudinal bars beyond that length by the tension development length.
  - Within **3 × pile diameter** below the cap: closed ties or spirals of diameter ≥ **9 mm**, at spacing ≤ **150 mm** or **8 d_b** (longitudinal).
  - Over the rest of the minimum length: spacing ≤ **16 d_b**.
  - Minimum reinforced length = the largest of:
    1. 1/3 of the pile length;
    2. 3 m;
    3. 3 × pile diameter;
    4. the flexural length, i.e. from the cap underside to the point where 0.4 M_cr exceeds the factored moment (seismic + gravity, per 2.5).
- **(ค) Metal-cased piles:** as (ข). A casing ≥ **2.0 mm** thick may replace some or all of the confining steel if it is protected from corrosion.
- **(ง) Concrete-filled pipe piles:** longitudinal ρ ≥ **0.01** at the top, over a length ≥ **2 × the embedment into the cap**.
- **(จ) Precast non-prestressed piles:**
  - Longitudinal ρ ≥ **0.01**.
  - Ties or spirals ≥ **10 mm** diameter.
  - Within **3 × pile diameter** below the cap: spacing ≤ **8 d_b(min)** and ≤ **150 mm**.
  - Elsewhere: spacing ≤ **16 d_b** and ≤ **200 mm**.
  - Reinforce the full pile length.
- **(ฉ) Precast prestressed piles:**
  - Within **6 m** below the cap: spirals with ρ_s ≥ **0.007**, or per Eq. 5.2-1.
  - Over the remaining length: ρ_s ≥ 0.5 × Eq. 5.2-1.
  - **Eq. 5.2-1:** ρ_s = 0.12 f'c / f_yh
    - ρ_s = volume of spiral / volume of core measured to the outside of the spiral;
    - f'c in MPa;
    - f_yh in MPa, ≤ **586 MPa**.

### 5.2.4 Concrete piles, category ง [D] (PDF p.107–110), brief

- **(ก) Site class E or F:**
  - Detail ductility per 5.2.9.4 over ≥ **7 pile diameters** below the cap.
  - Do the same over **7 diameters above and below** each interface between stiff soil and liquefiable or soft-to-medium clay.
- **(ข) Uncased piles:**
  - ≥ **4** longitudinal bars, with ρ ≥ **0.005**.
  - Transverse steel per 5.2.9.4 over the minimum length.
  - Extend longitudinal bars beyond that length by the tension development length.
  - Minimum length = the largest of:
    1. 1/2 of the pile length;
    2. 3 m;
    3. 3 × diameter;
    4. the flexural length as in 5.2.3.
  - Site class E/F: longitudinal steel and confining steel over the full pile length.
    - Tie diameter ≥ **10 mm** for piles ≤ **500 mm** diameter.
    - Tie diameter ≥ **12 mm** for piles > 500 mm.
  - Site class A–D: provide steel over ≥ 7 diameters above and below the soft-clay/liquefiable interface.
  - Outside the minimum length:
    - spirals with ρ_s ≥ **0.06 f'c / f_yh** are allowed;
    - spacing ≤ the least of **12 d_b**, **0.5 × pile diameter** and **300 mm**.
- **(ค) Metal-cased piles:** as 5.2.4(ข). A casing ≥ **2.0 mm** may replace some or all confining steel, if protected (as shown by site investigation).
- **(ง) Precast non-prestressed piles:**
  - Hoops or spirals per 5.2.9.4 within **3 diameters** below the cap.
  - Elsewhere ρ_s ≥ **0.06 f'c / f_yh**.
- **(จ) Precast prestressed piles:** confinement per 5.2.3, plus:
  1. **Ductile length:**
     - If the embedded length ≤ **10 m**, detail the full length for ductility.
     - If > 10 m, the ductile length = the greater of 10 m and (distance from cap underside to the point of zero curvature + 3 × the least pile dimension).
  2. **Spacing** of spirals or hoops in the ductile length ≤ the least of:
     - 1/5 of the least pile dimension;
     - **6 × strand diameter**;
     - **200 mm**.
  3. **Spiral splices:** one full-turn lap, welded, or mechanical. At a lap, spiral ends must have seismic hooks.
  4. **Spirals or circular hoops:**
     - **Eq. 5.2-2:** ρ_s = 0.25 (f'c/f_yh)(A_g/A_ch − 1.0)(0.5 + 1.4P/(f'c A_g))
     - **Eq. 5.2-3:** ρ_s ≥ 0.12 (f'c/f_yh)(0.5 + 1.4P/(f'c A_g))
     - ρ_s need not exceed **0.021**.
     - f'c ≤ **41.4 MPa**; f_yh ≤ **586 MPa**.
     - A_g = gross pile area (mm²); A_ch = core area to the outside of the spiral (mm²).
     - P = axial force from **1.2D + 0.5L + 1.0E** (N).
     - Inner and outer spirals may both be counted.
  5. **Rectangular hoops + cross ties:**
     - **Eq. 5.2-4:** A_sh = 0.3 s h_c (f'c/f_yh)(A_g/A_ch − 1.0)(0.5 + 1.4P/(f'c A_g))
     - **Eq. 5.2-5:** A_sh ≥ 0.12 s h_c (f'c/f_yh)(0.5 + 1.4P/(f'c A_g))
     - A_sh = total transverse steel area, including cross ties, within spacing s (mm²).
     - s = transverse spacing (mm).
     - h_c = core dimension measured centre-to-centre of the hoop (mm).
     - Here f_yh ≤ **483 MPa**.
     - Hoops and cross ties must be deformed bars, or equivalent, with diameter ≥ **10 mm**.
     - Rectangular hoop ends terminate at a corner with seismic hooks.
  6. Outside the ductile length: provide spirals or hoops ≥ **half** of item (4) or (5), as applicable.

### 5.2.5 Infilled masonry walls (brick or block) (PDF p.110–111)

#### 5.2.5.1 Columns adjacent to masonry infill [COL]

These details apply where the design (per 5.2.5.2) ignores frame–infill interaction or the hazardous failure modes the infill can cause. They cover columns next to masonry walls.

- **(ก) Wall shorter than the column clear height** (partial-height infill, Fig 5.2-1(ก)):
  1. Treat the **entire column length as the confined zone**:
     - intermediate MRF: hoops per **5.2.7.4.1** (spacing ≤ s0);
     - special MRF: hoops per **5.2.9.4.1–5.2.9.4.3**.
  2. Design shear for the **reduced (short-column) clear shear span**. Provide shear hoops over the part of the column not in contact with the wall, **plus a further length equal to the larger column section dimension** extending down into the wall-contact zone.
- **(ข) Wall touches the column over the full height on one side only** (Fig 5.2-1(ข)):
  - Intermediate MRF: hoops per **5.2.7.4**. Special MRF: hoops per **5.2.9.4**.
  - Hoops outside l0: intermediate spacing per 5.2.7.4.5 (≤ 2 s0), special per 5.2.9.4.6.
  - **In both cases the spacing outside l0 must also be ≤ d/2** (half the effective depth).
- **Column not adjacent to masonry** (Fig 5.2-1(ค)): detail per 5.2.7.4 (intermediate) or 5.2.9.4 (special).

**Fig 5.2-1: "Detailing of columns adjacent to masonry infill" (PDF p.111)**

Four column elevations sit side by side. In every panel:

- The column is drawn as two thin vertical lines passing through two floor beams, one at the top and one at the bottom. The beams are horizontal bands on both sides of the column, and the column continues above and below.
- Hoops are red horizontal ticks across the column, shown only in the clear height between beam soffit and beam top.
- Dimension arrows are placed on the right of the column.

- **Panel (ก), left pair: "infill height less than column height."**
  - Sketch 1: a low brick wall on **both** sides, about 45 % of the clear height. Above it is a large open (short-column) gap.
  - Sketch 2: a taller brick wall on both sides, about 80 % of the clear height, leaving a short open gap at the top.
  - In both sketches the hoops are **uniformly dense over the whole clear height**. One arrow labelled **S0** runs from the soffit of the upper beam to the top of the lower beam, i.e. the whole clear height is the s0 zone.
- **Panel (ข): "infill touches the column on one side only."**
  - A full-height brick wall on the **left** side only.
  - Hoops are dense in a top zone **S0**, measured from the upper beam soffit, and in a bottom zone **S0**, measured from the lower beam top. These are the l0 zones at spacing s0.
  - The middle zone has visibly wider spacing, with an arrow labelled **S ≤ d/2**.
- **Panel (ค): "no infill."**
  - The frame has no wall.
  - Dense hoops in the top **S0** and bottom **S0** zones. The top zone is shown shorter than in (ข), but it is the same concept.
  - The middle zone has wider spacing and no label. It follows the normal ≤ 2 s0 rule of 5.2.7.4.5.

Note: the figure's "S0" labels mark the **extent of the zone** hooped at spacing s0. In panels (ข) and (ค) that zone equals l0.

#### 5.2.5.2 Moment frames with masonry infill

- Consider frame–infill interaction where the infill acts as part of the main lateral system, especially:
  - irregularity caused by the infill;
  - possible failure modes: flexure, shear, bond/anchorage, and crushing of the wall;
  - interaction forces between frame and wall.
- Where the infill may crack under the design lateral load, model it as an **equivalent compression strut**. Columns act as vertical members, beams as horizontal members, and the wall as the diagonal strut.
- Strut modelling follows Annex ง (Appendix D) or DPT **1303**.

### 5.2.6 Ordinary moment frames (PDF p.112)

- **(ก) Beams, category ข [B]:**
  - At least **2 bars top and 2 bars bottom**, continuous along the whole beam length.
  - Anchored to develop yield in tension.
- **(ข) Columns, category ข [B]** [COL]:
  - Applies to ordinary-MRF columns with **clear height / larger section dimension ≤ 5**.
  - Design these columns for shear per **5.2.7.2**, i.e. capacity-based shear or 2 × E.

No other ordinary-frame column detailing is given. Tie spacing, splices and laps for ordinary frames therefore fall back to ACI 318 / EIT (5.2.1).

### 5.2.7 Intermediate moment frames (RC) (PDF p.112–118)

#### 5.2.7.1 Beams and columns: definitions

- **Beam:** frame member with factored axial load ≤ **0.10 A_g f'c**.
- **Column:** factored axial load > 0.10 A_g f'c.

#### 5.2.7.2 Shear strength [COL]

- The design shear strength of beams, columns and two-way flat slabs for seismic effects must be ≥ **either** of the following (the designer uses one of them):
  - **5.2.7.2.1 Capacity shear:** the shear when both member ends reach their **nominal moment** strengths, plus the gravity shear from factored gravity loads (Fig 5.2-2).
  - **5.2.7.2.2 Amplified-earthquake shear:** the maximum shear from design load combinations with the earthquake taken as **2 ×** the value in the building control law (Ministerial Regulation) on earthquake-resistant construction.

**Fig 5.2-2: "Example of shear strength calculation per 5.2.7.2.1" (PDF p.115)**

The page is rotated 90°. It has three parts.

- **Frame elevation:**
  - A stippled frame with two storeys of columns and beams, showing one bay opening.
  - Labels: "เสา" (column) and "คาน" (beam).
  - Dimensions: **L_c** = beam clear span between column faces; **H_c** = column clear height between beam faces.
- **Beam free body:**
  - Uniform load **W_u** over clear span **L_c**, with end moments **M_n1** (left) and **M_n2** (right) acting in the same sense (sway).
  - Below it is a trapezoidal shear diagram "แรงเฉือนในคาน" (beam shear) with maximum **V_u1** at the left end.
  - Equation: **V_u1 = (M_n1 + M_n2)/L_c + ½ W_u L_c**.
- **Column free body:**
  - Axial load **P_u** at the top and bottom, end moments **M_n3** (top) and **M_n4** (bottom), clear height **H_c**.
  - End shears **V_n2** at the top and bottom, in opposite directions.
  - A uniform rectangular shear diagram labelled "แรงเฉือนในเสา" (column shear), width **V_n2**.
  - The figure implies V = (M_n3 + M_n4)/H_c, but no formula is printed.
- **Note:** W_u and P_u are factored loads from the combination of D, L and E.

#### 5.2.7.3 Beam reinforcement (Fig 5.2-3)

1. **5.2.7.3.1 Moment strength:**
   - At the joint face, +M_n ≥ **1/3** of −M_n at the same face.
   - At any section along the beam, both +M_n and −M_n ≥ **1/5** of the maximum M_n at either joint face.
2. **5.2.7.3.2 End zones:** within **2h** of the support face, hoop spacing ≤ the least of:
   1. **d/4**;
   2. **8 d_b** of the smallest longitudinal bar;
   3. **24 d_b** of the hoop bar;
   4. **300 mm**.
   - The first hoop is ≤ **50 mm** from the support face.
3. **5.2.7.3.3 Elsewhere:** hoop spacing ≤ **d/2**.
4. **5.2.7.3.4 Laps:** avoid lapping top and bottom bars within **2h** of the support face.

**Fig 5.2-3: "Beam reinforcement details" (PDF p.116, drawn rotated)**

- **Layout:** an elevation of a continuous beam of depth **h**, with an exterior column "เสา" on the left, an interior column "เสา" at the right, and a break line at midspan.
- **Exterior joint:**
  - The top bar bends down and the bottom bar bends up into the column with **90° standard hooks**. The hook tails face each other near the outer column face.
  - The embedment **l_dh** is dimensioned from the inner column face to the outer vertical (tail) of the hook.
- **Hoop zones:**
  - At each column face (left end, both sides of the interior column), a zone **2h** long is labelled "เหล็กปลอก ระยะเรียง ≤ s1" (hoops at spacing ≤ s1).
  - Between those zones the label reads "เหล็กปลอก ระยะเรียง ≤ d/2".
  - Leaders mark the first hoop at **≤ 50 mm** from each column face.
- **Moment labels:** −M_nl and +M_nl at the left support; −M_nr and +M_nr at the right support.
- **Figure notes:**
  - (ก) s1 ≤ the least of: (1) 1/4 of the effective depth; (2) 8 × smallest longitudinal bar diameter; (3) 24 × hoop diameter; (4) 300 mm.
  - (ข) Moment capacity: (1) +M_nl ≥ (1/3)(−M_nl); (2) +M_nr ≥ (1/3)(−M_nr); (3) +M_n and −M_n at any section ≥ (1/5) of the greater of −M_nl and −M_nr.

#### 5.2.7.4 Column reinforcement [COL] (Fig 5.2-4)

- **5.2.7.4.1 Hoop spacing s0 in the end zone l0:**
  - Where rectilinear (tied) hoops are used, spacing ≤ **s0** over length **l0**, measured from each joint face.
  - s0 ≤ the least of:
    1. **8 d_b** of the smallest longitudinal bar;
    2. **24 d_b** of the hoop bar;
    3. **½ of the smallest column section dimension**;
    4. **300 mm**.
  - The **first hoop is ≤ 0.5 s0 from the joint face**.
- **5.2.7.4.2 Length l0:** l0 ≥ the largest of:
  1. **1/6 of the column clear height** (face to face);
  2. **the largest column section dimension**;
  3. **500 mm**.
- **5.2.7.4.3 Spiral columns:** follow the compression-member requirements of the EIT standard for RC buildings by strength design.
- **5.2.7.4.4 Joint (beam–column or slab–column in flat slabs) transverse steel:**
  - **Eq. 5.2-6:** **A_v ≥ (1/3) c1 s / f_y** (SI units), or **A_v ≥ 3.5 c1 s / f_y** (metric kgf/cm² units).
    - A_v = hoop area within spacing s.
    - s = hoop spacing within the joint.
    - f_y = hoop yield strength.
    - c1 = column dimension; per Fig 5.2-4, c1 is the larger side, with c1 > c2.
  - Provide this steel over a depth ≥ the **depth of the deepest beam** framing into the joint.
  - **Exception:** joints that are not part of the primary seismic system **and** are confined on all **4 sides** by beams or slabs of roughly equal depth.
- **5.2.7.4.5 Outside l0:** tied-hoop spacing ≤ **2 s0**.
- **5.2.7.4.6 Longitudinal ratio:**
  - A_s / A_g ≥ **1 %** (0.01).
  - A_s / A_g should not exceed **6 %** (0.06).
- **5.2.7.4.7 Splice location:**
  - Column bar splices should be in the **middle region of the column height**.
  - Splice method per the EIT RC strength-design standard.
- **5.2.7.4.8 Splice stagger:**
  - Splices of adjacent bars must not be at the same level. Stagger them by about **1.00 m**.
  - Avoid splicing where it is not necessary.

**Fig 5.2-4: "Column reinforcement details (for the case with no masonry infill)" (PDF p.117)**

*Elevation.* One storey of column, clear height **H_c**, between a lower beam "คานล่าง" and an upper beam "คานชั้นบน". The column continues below the lower beam, with a break line and cross-section below.

- **At the top (upper beam = roof or top storey):**
  - The outer longitudinal bars run up into the upper beam and end with **standard 90° hooks bent outward**. The left bar hooks left and the right bar hooks right, with the horizontal tails lying near the top of the beam.
  - Dimension **l_dh** runs from the underside (soffit) of the upper beam up to the hook level.
  - Callout: "standard 90° hook, or embedment sufficient to develop yield".
- **Upper l0 zone:**
  - Dimension **l0** from the upper beam soffit.
  - The first hoop is at **≤ 0.5 s0** below the soffit.
  - Hoops at **≤ s0** in this zone. Two hoops are drawn: the first near the soffit and one at the lower end of l0.
- **Middle zone** (between the two l0 zones): callout "hoops at spacing ≤ 2 s0".
- **Splice:**
  - Callout at mid-height (a circle on the H_c dimension line at H_c/2): "column bar splice zone (splices: see note ค)".
  - **Two laps are drawn, one per side, staggered in height.**
    - Left-side lap: roughly from just above mid-height to below it.
    - Right-side lap: lower, from about mid-height down toward the lower l0 zone.
  - In each lap the spliced bar has an **offset (crank) bend** so it sits beside the continuing bar. Callout: "**slope of offset ≤ 1:10**".
  - Both laps lie entirely within the middle zone and outside both l0 zones.
- **Lower l0 zone:**
  - Dimension **l0** from the top of the lower beam.
  - Hoops at **≤ s0** ("see note ก").
  - The last hoop is **≤ 0.5 s0** above the beam top.
- **Joint (within the lower beam depth):**
  - About 3 hoops are drawn inside the joint.
  - Callout: "amount of shear reinforcement **A_v = (1/3) c1 s / f_y**".
- **Below the lower beam** (next storey):
  - The first hoop is **≤ 0.5 s0** below the beam soffit.
  - Zone **l0** with hoops **≤ s0**.
- **Linework:** the elevation shows the column faces, the two outer longitudinal bars, and a centre vertical line with small circles at each hoop.

*Cross-section below the elevation.*

- A rectangle **c1** (vertical dimension) × **c2** (horizontal), with the note **c1 > c2**.
- **4 corner bars** in one closed rectangular hoop.
- The hoop closes at the top-left corner with a hook shown bent into the core, i.e. a 135° seismic hook.

*Notes printed on the figure.*

- **ก)** s0 ≤ the least of: (1) 8 × smallest longitudinal bar diameter; (2) 24 × hoop diameter; (3) c2/2; (4) 300 mm.
- **ข)** l0 ≥ the largest of: (1) H/6; (2) c1; (3) 500 mm.
- **ค)** Splice column bars in the mid-height region of the column.
- **ง)** Column A_s/A_g ≥ 1 % and should not exceed 6 %.

#### 5.2.7.5 Beam–column joint design (PDF p.118; continues on p.119, outside range)

- The joint must be large enough that the internal joint force does not exceed joint strength.
- **5.2.7.5.1:** **V_j ≤ φV_n** (Eq. 5.2-7), with φ = **0.85** for the joint.
- **5.2.7.5.2:** V_j is the maximum horizontal joint shear when the beam sections at both sides of the joint reach their nominal moments in the same sway direction (Fig 5.2-5).
- **5.2.7.5.3:** V_n of the joint:
  - (1) Joint confined by beams on **all 4 sides** (Fig 5.2-6(ก)): **V_n = 1.7 √f'c A_j** (Eq. 5.2-8, SI), or **5.4 √f'c A_j** (metric).
  - The remaining cases are on p.119, outside this range.

**Fig 5.2-5: "Maximum horizontal joint shear" (PDF p.118)**

- **(ก) Moment-frame elevation:**
  - A beam across three columns.
  - The interior joint is shaded inside a dashed box, labelled "ดูรูปขยายข้อต่อ" (see joint detail).
- **(ข) Joint enlargement:**
  - Column with V_col at the top and at the bottom, in opposite directions.
  - Left beam: moment M_n1; top compression block C1 = T1; bottom tension T1 = A_s1 f_y pulled out to the left.
  - Right beam: moment M_n2; top tension T2 = A_s2 f_y to the right; bottom compression C2 = T2.
  - V_j acts on the horizontal mid-plane of the stippled joint.
- **Boxed equation:** V_j = C1 + T2 − V_col = T1 + T2 − V_col = (A_s1 f_y + A_s2 f_y) − V_col.

---

## Summary: column detailing requirements by frame type

Special MRF column rules are in 5.2.9.4, which is outside this range. The special column gives only the pointers found here.

| Item | Ordinary RC MRF | Intermediate RC MRF | Special RC MRF |
|---|---|---|---|
| Permitted category (Table 2.3-1) | ข [B] only (× in ค [C] and ง [D]); R = 3, Ω0 = 3, C_d = 2.5 | ข [B], ค [C]; ง [D] only if height ≤ 40 m with strength forces +40 % (2.3.1.2); R = 5, Ω0 = 3, C_d = 4.5 | ข [B], ค [C], ง [D]; R = 8, Ω0 = 3, C_d = 5.5 |
| Column definition | per ACI 318 / EIT | P_u > 0.10 A_g f'c (5.2.7.1) | 5.2.9 (out of range) |
| Longitudinal ratio ρ = A_s/A_g | ACI 318 / EIT (typically 1–8 %) | ≥ 1 %, should be ≤ 6 % (5.2.7.4.6) | 5.2.9 (out of range) |
| Splice location | ACI 318 / EIT | Mid-height region of the column, outside both l0 zones (5.2.7.4.7, Fig 5.2-4 note ค) | 5.2.9 (out of range) |
| Splice type / stagger | ACI 318 / EIT | Lap per EIT strength standard. Adjacent bars staggered about 1.00 m. Avoid unnecessary splices (5.2.7.4.8). Offset-bent bar slope ≤ 1:10 (Fig 5.2-4) | 5.2.9 (out of range) |
| End-zone length l0 | not specified | ≥ max(H_c/6, largest section dimension c1, 500 mm) (5.2.7.4.2) | 5.2.9.4 (out of range) |
| End-zone hoop spacing s0 | not specified; ACI tie spacing | ≤ min(8 d_b long. smallest, 24 d_b hoop, ½ smallest dimension c2, 300 mm) (5.2.7.4.1) | 5.2.9.4 (out of range) |
| First hoop position | ACI (≤ s/2 typical) | ≤ 0.5 s0 from the joint face (beam soffit or beam top), at both ends (5.2.7.4.1) | 5.2.9.4 (out of range) |
| Mid-zone hoop spacing | ACI tie spacing | ≤ 2 s0 (5.2.7.4.5) | 5.2.9.4.6 (out of range) |
| Hooks | ACI | Hoop closed with a 135° hook into the core, as drawn in Fig 5.2-4. Top-storey column bars end with standard 90° hooks bent outward into the roof beam, or straight embedment ≥ yield development, with l_dh measured from the beam soffit (Fig 5.2-4) | 5.2.9 (out of range) |
| Joint transverse steel | ACI | A_v ≥ (1/3) c1 s / f_y (SI) [3.5 c1 s / f_y metric] over a depth ≥ the deepest beam. Waived for non-seismic-system joints confined on 4 sides by roughly equal-depth members (5.2.7.4.4). Joint shear: V_j ≤ 0.85 V_n, with V_n = 1.7√f'c A_j for a 4-side-confined joint (5.2.7.5) | 5.2.9 (out of range) |
| Shear design | If H_c / largest dimension ≤ 5 (category ข [B]): capacity shear or 2E per 5.2.7.2 (5.2.6(ข)) | Capacity shear (M_n at both ends + gravity) or 2 × E (5.2.7.2) | 5.2.9 (out of range) |
| Column next to partial-height infill | not covered | Whole clear height hooped at ≤ s0. Design shear for the short clear length. Shear hoops extend a further (larger column dimension) into the wall zone (5.2.5.1(ก), Fig 5.2-1(ก)) | Whole height per 5.2.9.4.1–5.2.9.4.3 (5.2.5.1(ก)) |
| Column with full-height infill on one side | not covered | l0 zones at s0 per 5.2.7.4. Middle zone ≤ 2 s0 **and ≤ d/2** (5.2.5.1(ข), Fig 5.2-1(ข)) | 5.2.9.4; mid zone per 5.2.9.4.6 **and ≤ d/2** |
| Column with no infill | ACI | Standard 5.2.7.4 (Fig 5.2-1(ค), Fig 5.2-4) | 5.2.9.4 |
| Watch zones | — | Intermediate frames must follow at least 5.2.7.4. Flat slabs also follow 5.2.12 (5.2.2(ง)) | — |

Unreadable: none. All values in these ranges were legible in the page images.


---

Source PDF pages 118–131, 143–146 (printed pages 104–117, 129–132). All page images viewed.
Units: equations in SI (N, mm, MPa); DPT also gives a "metric" (kgf, cm, ksc) version, shown in brackets.
Symbols: f'c = concrete strength; fy = long. bar yield; fyh = hoop yield; db = bar dia.; Ag = gross area; Ach = core area; s = hoop spacing; bc = core dimension.

---

## 5.2.7.5 Beam-column joints — INTERMEDIATE moment frames (p.118–120)

Joint must be large enough that joint forces do not exceed joint strength.

**5.2.7.5.1** Vj ≤ φVn  **(5.2-7)**, φ (joint) = **0.85**.

**5.2.7.5.2** Maximum horizontal joint shear Vj is the value when the beam sections at both sides of the joint reach their nominal flexural strengths acting in the same sense (sway), see Fig 5.2-5.

**Fig 5.2-5 — Computation of maximum horizontal joint shear** (p.118)
- (a) "Moment frame": elevation of 3 columns and a continuous beam; the interior joint is circled (dashed box, "see joint enlargement").
- (b) "Joint enlargement" (free body): column above and below, beams left and right.
  - Left beam: top bars in compression → force C1 = T1 acting into joint at top; bottom bars in tension T1 = As1·fy pulling out to the left at bottom; moment Mn1 (curved arrow).
  - Right beam: top bars in tension T2 = As2·fy pulling out to the right at top; bottom compression C2 = T2 pushing into joint at bottom; moment Mn2.
  - Column shear Vcol at top (acting leftwards) and bottom (rightwards); Vj shown acting on the horizontal mid-plane of the joint (dash-dot line). Hatched blocks = joint core.
- Boxed equation: **Vj = C1 + T2 − Vcol = T1 + T2 − Vcol = (As1·fy + As2·fy) − Vcol**.
  (For special frames 5.2.10.1.1 replaces fy by 1.25fy.)

**5.2.7.5.3** Nominal joint shear strength Vn:

| Joint type (Fig 5.2-6) | SI (N, MPa, mm²) | Metric (kgf, ksc, cm²) | Eq. |
|---|---|---|---|
| (1) Confined by beams on all 4 faces [(ก)] | Vn = 1.7 √f'c · Aj | Vn = 5.4 √f'c · Aj | 5.2-8 |
| (2) Confined on 3 faces, or on 2 opposite faces [(ข)] | Vn = 1.25 √f'c · Aj | Vn = 4.0 √f'c · Aj | 5.2-9 |
| (3) Others [(ค)] | Vn = 1.0 √f'c · Aj | Vn = 3.2 √f'c · Aj | 5.2-10 |

- Aj = effective horizontal shear area of joint (Fig 5.2-7).
- A face counts as "confined by a beam" only if that beam width ≥ **3/4 of the column width** at that face AND beam depth ≥ **3/4 of the depth of the deepest beam** framing into the joint.
- Special frames, lightweight concrete: Vn ≤ 3/4 of above (5.2.10.3).

**Fig 5.2-6 — Joint types for Vn** (p.119), isometric sketches, joint top face hatched, beam ends hatched:
- (ก) Interior joint: column continuous above/below, 4 beams on all 4 faces (cross shape).
- (ข) Left: 3 beams (T-shape in plan) = exterior/edge joint; right: 2 beams on opposite faces (straight through column).
- (ค) "Other joints": left: 2 beams on adjacent faces (L in plan, corner joint); right: 1 beam only (knee/corner with single beam). In both the column is shown ending at the joint top (roof-type).
→ Edge column (3 beams) = type (2) 1.25; corner column (2 adjacent beams) = type (3) 1.0.

**Fig 5.2-7 — Effective joint shear area Aj** (p.120)
- Upper: isometric of joint with beams on 4 sides; direction of shear-producing force = along one beam axis (arrow). Front beam section shows top bars (3) and bottom bars (2) = "reinforcement producing shear". Hatched horizontal plane at joint mid-depth = Aj.
- Joint depth **h = column dimension in the plane of the shear-producing reinforcement** (parallel to beam bars).
- Effective joint width **≤ b + h and ≤ b + 2x1**, where b = width of beam (in the loading direction), x1 = smaller distance from beam side face to column side face.
- Lower (plan "รูปด้านบน"): column square outline (thick), beam width b entering from bottom, x1 (right, smaller) and x2 (left) are the offsets between beam faces and column faces; note "x1 < x2". Hatched rectangle = Aj = (effective width) × h. Load direction arrow vertical (downwards, along beam).

---

## 5.2.7.6 Seismic hooks (Intermediate frames) (p.121)

- Hooks on stirrups and hoops may generally be bent **90°** with extension ≥ **6 db** of the hoop bar (Fig 5.2-8).
- For **public buildings** (theatres, assembly halls, hotels, hospitals, schools, etc.) or buildings designed for ductility: hooks **should be 135°**; or if 90° hooks are used, they **should be restrained with a hook-clip** holding the 90° legs, in the zones near joints (distance **2h** in Fig 5.2-3 [beam], or **l0** in Fig 5.2-4 [column]) — figs 5.2-3/5.2-4 are outside this range.

**Fig 5.2-8 — Hook detail, intermediate moment frames** (p.121). Two rectangular (portrait) hoops with rounded corners; hook shown at the top-left corner; dashed circle at corner marked **D** (inside bend diameter, value not given here).
- (ก) 90° hook ("for general buildings"): the hoop end turns 90° at the top-left corner and continues along the top side; extension dimensioned horizontally **6db (≥ 75 mm)** from the vertical leg; the other hoop end laps along the top side.
- (ข) 135° hook ("for public buildings"): both ends bend at the top-left corner into the core at 135° (angle measured from the vertical leg); straight tail **6db (≥ 75 mm)** measured along the tail, pointing diagonally into the core.

---

## 5.2.8 Beams of SPECIAL moment frames (column/joint-relevant items only) (p.121–123)

Supplements 5.2.7; the more stringent governs.
- 5.2.8.1.1 Pu ≤ Ag f'c/10.
- 5.2.8.1.2 Clear span ln ≥ 4 d.
- 5.2.8.1.3 bw ≥ lesser of 0.3h and 250 mm (as printed).
- 5.2.8.1.4 Beam projection beyond each column side face ≤ lesser of column width and 3/4 column depth.
- 5.2.8.2.1 As,min = 1.4 bw d/fy [14 bw d/fy metric], unless As provided exceeds calculated by 1/3; ρ ≤ **0.025**; ≥ **2 bars continuous** top and bottom.
- 5.2.8.2.2 M+ at joint face ≥ ½ M− at that face; M+ and M− anywhere ≥ ¼ max moment strength at joint faces.
- 5.2.8.2.3 Lap splices only where hoops/spirals enclose the lap, spacing ≤ lesser of **d/4 and 100 mm**. **No laps: (1) within joints; (2) within 2h from joint face; (3) where analysis indicates flexural yielding from inelastic sway.**
- 5.2.8.3.1 Hoops required over (1) **2h from support face** toward midspan at both ends; (2) 2h each side of any potential plastic hinge section.
- 5.2.8.3.2 **First hoop ≤ 50 mm from support (column) face**; spacing ≤ min(d/4, 8 db smallest long. bar, 24 d hoop, 300 mm).
- 5.2.8.3.3 Perimeter long. bars in hoop zone laterally supported per accepted RC code.
- 5.2.8.3.4 Outside hoop zones: stirrups with seismic hooks both ends, s ≤ d/2.
- 5.2.8.3.5 Stirrups/ties resisting shear must be hoops over member length in 5.2.8.3, 5.2.9.4, 5.2.10.2.
- 5.2.8.3.6 Beam hoop may be 2 pieces: stirrup with seismic hooks both ends + cross tie cap. Consecutive crossties engaging the same long. bar: 90° hooks at opposite sides. If long. bars held by the crosstie are confined by a slab on one side only, the 90° hooks go on that (slab) side.
- 5.2.8.4.1 Ve from Mpr at both faces (opposite sense) + factored gravity; Mpr with bar stress **1.25 fy**.
- 5.2.8.4.2 Vc = 0 over 5.2.8.3.1 zones if (1) seismic shear ≥ max required shear strength in span, and (2) Pu < Ag f'c/20.

---

## 5.2.9 COLUMNS of SPECIAL moment frames (p.124–129)

### 5.2.9.1 Scope
Supplements 5.2.7 (stricter governs). Applies to frame members that (1) resist earthquake and (2) have factored axial force > **Ag f'c/10**. Section limits:
- (ก) Shortest cross-section dimension (through centroid) ≥ **300 mm**.
- (ข) Ratio shortest dimension / perpendicular dimension ≥ **0.4**.

### 5.2.9.2 Minimum flexural strength (strong column–weak beam)
- 5.2.9.2.1 Must satisfy 5.2.9.2.2 or 5.2.9.2.3. Columns not satisfying 5.2.9.2.2 are ignored for lateral strength/stiffness (treated as not part of the seismic system).
- 5.2.9.2.2 **ΣMnc ≥ (6/5) ΣMnb  (5.2-11)**
  - ΣMnc = sum of nominal column moment strengths at joint faces, using the axial force giving the lowest moment strength.
  - ΣMnb = sum of beam nominal moment strengths at joint faces; for T-beams with flange in tension include slab reinforcement within effective slab width.
  - Column moments summed opposing the beam moments.
- 5.2.9.2.3 If 5.2.9.2.2 not met: provide transverse reinforcement per 5.2.9.4.1–5.2.9.4.3 over the **full column height** of columns supporting that joint.

### 5.2.9.3 Longitudinal reinforcement
- 5.2.9.3.1 **0.01 Ag ≤ Ast ≤ 0.06 Ag**.
- 5.2.9.3.2 Mechanical and welded splices per the applicable standard. **Lap splices only within the middle portion (center half region) of the column height**, designed as **tension lap splices**, and enclosed by transverse reinforcement per **5.2.9.4.2–5.2.9.4.3** (i.e. confinement spacing over the lap).

### 5.2.9.4 Transverse reinforcement
**5.2.9.4.1** Provide per (1)–(5) unless 5.2.9.5 (shear) requires more:
- (1) Spiral volumetric ratio ρs ≥ both:
  - **ρs = 0.12 f'c/fyh  (5.2-12)**
  - **ρs = 0.45 [(Ag/Ach) − 1] (f'c/fyh)  (5.2-13)**
- (2) Rectangular hoop total area Ash (each direction) ≥ both:
  - **Ash = 0.3 (s·bc·f'c/fyh) [(Ag/Ach) − 1]  (5.2-14)**
  - **Ash = 0.09 s·bc·f'c/fyh  (5.2-15)**
  - Ash = total cross-sectional area of transverse legs (hoops + crossties) in the direction of the earthquake force, within spacing s; bc = core dimension measured centre-to-centre of hoop bars, perpendicular to the legs counted; Ach = area inside the outside perimeter of the hoop.
- (3) Single or overlapping hoops permitted; **crossties** of same bar size and spacing as hoops permitted. Each crosstie end must engage a peripheral longitudinal bar. Consecutive crossties should **alternate their end hooks** along the longitudinal bars.
- (4) If design strength of the column core alone resists the seismic load combination, Eq. 5.2-15 need not be met.
- (5) If concrete cover outside the confining hoops > **100 mm**, add transverse reinforcement at spacing ≤ **300 mm** with cover to it ≤ **100 mm**.

**Fig 5.2-9 — Definition of variables** (p.126)
- Left: square column, thick outer line = concrete face. 8 bars (3 top, 3 bottom, 1 each side middle). Perimeter hoop with 135° hooks at top-left corner; a second (cross) arrangement: vertical crosstie through middle top/bottom bars (135° hook at top engaging the middle top bar) and a horizontal crosstie through middle side bars (135° hook at right end). Shaded area inside hoop = Ach ("hatched area"). Earthquake force direction vertical (double arrow) → Ash = three vertical legs cut by a horizontal section (left hoop leg, middle crosstie, right hoop leg, ellipses marked). bc dimension horizontal across the core (between hoop leg centres), h = overall column dimension (vertical).
- Right: circular column with 8 bars in a spiral; bc = core diameter; h = overall diameter; shaded Ach = area inside outer surface of spiral.
- Labels: "bc: column core dimension measured between steel centres"; "Ach: area inside perimeter of hoop measured to its outside surface".

**Fig 5.2-10 — Example column longitudinal bars and hoops** (p.126). Rectangular column (landscape), bc1 horizontal, bc2 vertical. 16 bars: 7 top row, 7 bottom row, 1 at mid-height on each short side.
- Perimeter hoop with **135° hooks at the top-left corner**, extensions labelled "**6db ≥ 75 mm (7.5 cm) Extension**".
- Two vertical crossties engaging top-row bars 3 and 5 (counting from left) and the bottom bars below them: crosstie at bar 3 has 135° hook at top (6db ≥ 75 mm) and 90° hook at bottom; crosstie at bar 5 has **90° hook at top with "6db Extension"** (horizontal tail along the top) and 135° hook at bottom → 90° hooks alternate top/bottom.
- One horizontal crosstie at mid-height engaging the two side bars: 90° hook at left end (tail turned along the side), 135° hook at right end.
- Label: "Crossties engaging the same longitudinal bar: alternate the 90° hook locations."
- Dimensions: bc1 split into 3 equal xi; bc2 split into 2 xi. Notes: "**xi ≤ 350 mm (35 cm)**"; "**xi (hx) = maximum xi over all faces**" (used in Eq. 5.2-16).
- Every corner bar and alternate/all intermediate bars are engaged by a hoop corner or crosstie (here every other top/bottom bar: 1,3,5,7 engaged).

**Fig 5.2-11 — Example overlapping hoops** (p.127)
- Detail A: closed rectangular hoop, both ends with **135° hooks at one top corner**, extension **6db ≥ 75 mm (7.5 cm)**.
- Detail B: crosstie ("cap tie") drawn horizontally: **135° hook at one end** (left, bending down) and **90° hook at the other end with 6db extension** (right, bending down).
- Detail C: U-shaped hoop (open top) with **135° hooks at both top corners**, each tail pointing into the core, 6db ≥ 75 mm.
- Section (left): square column, 8 bars (4 top, 4 bottom). Two **overlapping Detail-A hoops**: left hoop encloses bars 1–3, right hoop encloses bars 2–4; hook of left hoop at its top-left corner, of right hoop at its top-right corner.
- Section (right): 8 bars (4 top, 4 bottom). Two overlapping **Detail-C U-hoops** (left over bars 1–3, right over bars 2–4) closed on top by **Detail-B crossties**; label: crossties engaging the same longitudinal bar alternate 90° hook positions.
- Legend: Detail = รายละเอียด; Extension = ระยะยื่น.

**5.2.9.4.2** Spacing s of transverse reinforcement (within l0) ≤ least of:
1. **1/4 of smallest column cross-section dimension**;
2. **6 db** of longitudinal bar;
3. **s0 = 100 + (350 − xi)/3 mm  (5.2-16)** [metric: s0 = 10 + (35 − xi)/3 cm], with **100 mm ≤ s0 ≤ 150 mm**. (xi = max centre-to-centre spacing of hoop legs/crossties, Fig 5.2-10.)

**5.2.9.4.3** Horizontal spacing of crossties or legs of overlapping hoops ≤ **350 mm** c/c.

**5.2.9.4.4** Confinement per 5.2.9.4.1–5.2.9.4.3 placed over length **l0 from each joint face** (both ends) and on both sides of any section where flexural yielding may occur. **l0 ≥ largest of**:
1. largest column cross-section dimension;
2. **1/6 of clear column height** (face to face);
3. **500 mm**.

**5.2.9.4.5** Columns supporting reactions from discontinued stiff members (e.g. walls): confinement per 5.2.9.4.1–5.2.9.4.3 over **full height below the discontinuity** when factored axial compression (incl. EQ) exceeds [threshold value missing in source — blank line, p.128; ACI equivalent is Ag f'c/10].
- That confinement extends into the discontinued member ≥ **development length in tension of the largest column longitudinal bar**.
- If column bottom ends on a wall: extend confinement into the wall ≥ **ld** of the largest longitudinal bar.
- **If column terminates on a footing (foundation): extend confinement into the footing ≥ 300 mm.**

**5.2.9.4.6** Outside the confined regions (where full-height confinement is not provided): spirals or hoops at c/c spacing ≤ lesser of **6 db (long. bar)** and **150 mm**.

### 5.2.9.5 Shear strength (p.129)
- 5.2.9.5.1 Design shear Ve from maximum end forces: probable moment strength Mpr at both column ends together with factored axial load Pu (acting together); Ve ≥ factored shear from analysis.
- 5.2.9.5.2 Mpr computed with bar tensile stress **1.25 fy**.
- 5.2.9.5.3 Over **l0**, design transverse reinforcement with **Vc = 0** when (1) EQ-induced shear (per 5.2.9.5.1) ≥ ½ max factored shear, AND (2) Pu (incl. EQ) < **Ag f'c/20**.

---

## 5.2.10 Joints of SPECIAL moment frames (p.129–131)

### 5.2.10.1 General (supplements 5.2.7; stricter governs)
- .1 Forces in beam longitudinal bars at joint computed with stress **1.25 fy**.
- .2 Joint strength reduction factor φ = **0.85**.
- .3 Beam longitudinal bars terminating in a column **extend to the far face of the confined column core** and are anchored: tension per 5.2.10.4; compression per column/RC code.
- .4 Beam bars passing through the joint: column dimension parallel to those bars ≥ **20 db** of the largest beam bar (normal-weight concrete); ≥ **26 db** (lightweight).

### 5.2.10.2 Transverse reinforcement in joint
- .1 Provide hoops per **5.2.9.4** in the joint unless confined by beams per .2.
- .2 Beams on **all 4 faces**, each beam width ≥ **3/4 column width**: transverse reinforcement ≥ **½** of 5.2.9.4.1 within depth h of the **shallowest** framing beam, and spacing of 5.2.9.4.2 may be relaxed to **150 mm**.
- .3 Where no beam frames into the joint (face), provide transverse reinforcement per 5.2.9.4 in the joint to confine the beam longitudinal bars.
→ Edge and corner joints (not 4-sided) require FULL column confinement (5.2.9.4) through the joint depth.

### 5.2.10.3 Shear strength
Vn per 5.2.7.5.3 (1.7 / 1.25 / 1.0 √f'c Aj) for normal-weight; lightweight ≤ **3/4** of those values.

### 5.2.10.4 Development of bars in tension
**5.2.10.4.1** Standard **90° hook**, bar dia. 9–32 mm, normal-weight:
**ldh ≥ max{ 8 db, 150 mm, fy·db/(5.3√f'c) }  (5.2-17)** [metric: ldh = fy·db/(17√f'c), fy, f'c in ksc].
- Lightweight: ldh ≥ max{ 10 db, 200 mm, 1.25 × Eq. 5.2-17 }.
- The **90° hook must be located within the confined column core** or within a boundary element.

**5.2.10.4.2** Straight bars (9–32 mm): ld ≥ larger of
- (1) **2.5 × ldh** (5.2.10.4.1) if concrete cast in one lift beneath the bar ≤ **250 mm**;
- (2) **3.25 × ldh** if concrete below bar > **250 mm** (top bars).

**5.2.10.4.3** Straight bars terminating at a joint must pass through the confined column core (or boundary element); any part of ld **not within the confined core is increased by 1.6×**.

**5.2.10.4.4** Epoxy-coated bars: multiply 5.2.10.4.1–.3 lengths by the appropriate factor of the accepted code.

**Fig 5.2-12 — Example of bar hooking at joint** (p.131) — edge/corner (exterior) joint
- Left, **plan (top reinforcement)**: rectangular column; left face and bottom face are free (exterior) faces; a beam enters from the **top** (bars running vertically in plan, ending near the far/bottom face) and the main beam enters from the **right** (bars running horizontally, ending near the far/left face) → beam bars from both directions extend to the far side of the column core. Column bars: 14 (5 top row, 5 bottom row, 2 intermediate on each side). Three joint hoops per layer drawn in colours:
  - yellow = perimeter hoop around all corner bars, 135° hooks at the **bottom-right** corner;
  - brown = inner hoop enclosing the middle 3×2 bars (top/bottom rows, bars 2–4), 135° hooks at its **top-right** corner;
  - green = inner hoop enclosing the side intermediate bars (full width, middle rows), 135° hooks at its **top-left** corner.
  → hook locations are staggered to different corners. Section A-A cut horizontally through the main (right) beam.
- Right, **elevation Section A-A**: column continuous above and below (break lines); beam from right. Beam **top bars bend down 90°** and **bottom bars bend up 90°** at the far (left) side of the column; the vertical hook tails lie just inside the far-face column bars and overlap each other vertically. Dimension **≥ ldh** measured from the column face on the beam side (critical section) to the outside of the hook tail at the far side. Perpendicular beam bars appear as dots (top layer slightly above main top bars, bottom layer below). **Joint hoops (all three hoop types, colour-coded) continue through the full joint depth** at regular spacing (≈6 layers shown, one above the beam top bars, one just above the bottom bars). Beam stirrups (blue) start close to the column face (first at ≤ 50 mm per 5.2.8.3.2).

---

## 5.2.13 Building foundations (p.143)
- Designer must account for transfer of seismic forces from the superstructure into the foundation, in addition to other loads.
- Pile foundations: account for seismic force transfer from footing/pile cap into piles, e.g. specify the amount of reinforcement in the pile portion embedded in the cap, and check lateral capacity of each pile.
- **No numeric requirements** in this clause — no provisions on tie beams between footings, dowel/starter bars, or pile-cap detailing. (Only related numeric item: 5.2.9.4.5 — column confinement hoops extend ≥ 300 mm into the footing.)
- p.142–143 (start) is 5.2.12 flat-slab (not in scope); p.144 blank; p.145–146 bibliography (EIT 1008-2558, ACI 318-14, ASCE 7-05/10, etc.).

---

## SUMMARY — Special moment frame column + joint detailing

| Item | Requirement | Clause |
|---|---|---|
| Applicability | EQ-resisting members with Pu > Ag f'c/10 | 5.2.9.1 |
| Min. column dimension | ≥ 300 mm (shortest, through centroid) | 5.2.9.1(ก) |
| Aspect ratio | short/long ≥ 0.4 | 5.2.9.1(ข) |
| Strong column | ΣMnc ≥ 1.2 ΣMnb | 5.2.9.2.2 |
| Long. steel ratio | 1% ≤ ρg ≤ 6% | 5.2.9.3.1 |
| Lap splice location | Middle (center) region of clear height only; tension lap; confined per 5.2.9.4.2–.3 over lap | 5.2.9.3.2 |
| Mechanical/welded splice | Per applicable standard | 5.2.9.3.2 |
| Ash (rect. hoops) | ≥ 0.3 s bc f'c/fyh (Ag/Ach − 1) and ≥ 0.09 s bc f'c/fyh | 5.2-14, 5.2-15 |
| ρs (spiral) | ≥ 0.12 f'c/fyh and ≥ 0.45 (Ag/Ach − 1) f'c/fyh | 5.2-12, 5.2-13 |
| Confined length l0 (each end + potential hinges) | ≥ max(largest column dim., clear height/6, 500 mm) | 5.2.9.4.4 |
| Hoop spacing in l0 | ≤ min(b_min/4, 6 db, s0); s0 = 100 + (350 − hx)/3, 100 ≤ s0 ≤ 150 mm | 5.2.9.4.2 |
| hx / xi (leg spacing) | ≤ 350 mm c/c (crossties or overlapping-hoop legs) | 5.2.9.4.3, Fig 5.2-10 |
| Hoop spacing outside l0 | ≤ min(6 db, 150 mm) | 5.2.9.4.6 |
| Cover > 100 mm | extra ties @ ≤ 300 mm, cover ≤ 100 mm | 5.2.9.4.1(5) |
| Hoop hooks | 135°, extension 6db ≥ 75 mm | Fig 5.2-10/11 |
| Crossties | same size/spacing as hoops; 135° one end, 90° (6db) other end; alternate 90° ends on consecutive ties (and along each bar) | 5.2.9.4.1(3), Figs 5.2-10/11 |
| Hoops fail SCWB | confinement full height | 5.2.9.2.3 |
| Column on footing | confinement extends ≥ 300 mm into footing | 5.2.9.4.5 |
| Column on wall / under discontinued wall | confinement extends ≥ ld (largest bar) into wall; full height below discontinuity | 5.2.9.4.5 |
| Column shear | Ve from Mpr (1.25fy) at both ends; Vc = 0 in l0 if EQ shear ≥ ½Vu and Pu < Ag f'c/20 | 5.2.9.5 |
| Joint hoops | Full 5.2.9.4 confinement through joint; if 4 beams each ≥ ¾ col. width: ½ amount within shallowest beam depth, s ≤ 150 mm | 5.2.10.2 |
| Joint shear | φ = 0.85; Vn = 1.7 / 1.25 / 1.0 √f'c Aj (4-side / 3-side or opposite / other) | 5.2.7.5.3, 5.2.10.3 |
| Aj | h (col. depth ∥ bars) × eff. width ≤ min(b + h, b + 2x1) | Fig 5.2-7 |
| Through beam bars | column dim. ∥ bars ≥ 20 db (NW), 26 db (LW) | 5.2.10.1.4 |
| Beam bar anchorage | extend to far face of confined core; 90° hook within core | 5.2.10.1.3, 5.2.10.4.1 |
| ldh (90° hook) | ≥ max(8 db, 150 mm, fy db/(5.3√f'c)) [LW: max(10db, 200, 1.25×)] | 5.2-17 |
| Straight ld | 2.5 ldh (≤ 250 mm below) / 3.25 ldh (> 250 mm below); portion outside core ×1.6 | 5.2.10.4.2–.3 |
| Beam laps | none within joint or within 2h of joint face | 5.2.8.2.3 |
| Beam first hoop | ≤ 50 mm from column face; hoop zone 2h | 5.2.8.3.1–.2 |
| Intermediate frames hooks | 90° + 6db (≥ 75 mm) allowed generally; 135° (or 90° + hook-clip) near joints for public/ductile buildings | 5.2.7.6 |

## Items relevant to EDGE / CORNER columns
1. Joint shear coefficient: edge joint (3 beams) → 1.25√f'c Aj; corner joint (2 adjacent beams) or single-beam knee → 1.0√f'c Aj (Fig 5.2-6). Beam counts only if width ≥ ¾ column width and depth ≥ ¾ deepest beam.
2. Edge/corner joints do NOT qualify for the 4-sided reduction → full column confinement (5.2.9.4 Ash, s ≤ s0) must continue through the entire joint depth (5.2.10.2.1/.3).
3. Beam bars terminating at edge/corner column: extend to far face of confined core, 90° hooks (top bars turned down, bottom bars turned up) located inside the column core within the column bar cage; ldh ≥ max(8db, 150 mm, fy db/(5.3√f'c)), measured from column face (beam side) to outside of hook (Fig 5.2-12).
4. Both beams at a corner hook toward the far faces (Fig 5.2-12 plan); stagger hoop hook corners between the perimeter and inner hoops.
5. Joint Aj effective width ≤ b + 2x1 matters where beam is flush with the exterior face (x1 small/zero).
6. Column dimension parallel to any beam bars passing through ≥ 20 db.
7. Straight-bar anchorage in exterior joints: portion outside confined core × 1.6; 2.5/3.25 × ldh.

## Items relevant to FOOTINGS
1. Column confinement hoops (5.2.9.4.1–.3) extend ≥ **300 mm into the footing** (5.2.9.4.5).
2. l0 confinement zone applies at the column base (joint face = top of footing/tie beam) per 5.2.9.4.4.
3. 5.2.13: design for seismic force transfer into foundation and piles; specify pile reinforcement embedded in pile cap; check lateral capacity of each pile. No tie-beam or dowel numeric rules in this standard's range.


---


Page refs = PDF page (book page = PDF − 8). All figures were viewed as images (zoomed where needed).
Codes cited by the book: ACI 315 (bar/tie arrangement), ACI 318-14 (tie hooks), ACI 352 (joints), EIT/วสท. 1008-38 (hooks, bends, laps). Appendix sheets (p.181–206) are EIT-style Thai typical drawings (no explicit code cited; 750-to-Lc/2 splice zone is the Thai seismic practice).
Where the book's figure has an evident typo it is flagged **[BOOK TYPO?]**.

---

## 1. SECTION CHANGE — bigger column below → smaller column above

### 1.1 Rule summary (text p.102, p.104; appendix p.195)
- Main bars come in 10 m stock → splice every 2–3 storeys (p.102).
- Similar-size columns: crank (offset-bend) the LOWER bars, slope **≤ 1:6**, lap with upper bars just above the floor. Large bars/columns may use mechanical splices instead (p.102).
- Offset limit for cranking: book text p.102 / Fig 4.10 = **80 mm (3")** (ACI 315 value). Appendix sheet p.195 = **75 mm**. Use 75 mm on the drawing (EIT/Thai sheet), note 80 mm is the ACI 3" origin.
- Offset > limit (or crank would be steeper than 1:6): stop lower bars in the joint and use separate **DOWEL BARS** lapped into both columns (p.102, p.104–105).
- Eccentric columns: if one side's crank ≤ 1:6 crank that side normally; on the side with large offset use dowels (Fig 4.16, p.105).

### 1.2 Fig 4.10(a) p.102 — "Splice of columns of similar section" (ACI 315 standard; lap splice, offset < 3" (80 mm))
View: vertical elevation through floor slab + beam, sections A-A (above) and B-B (below).
- Lower column wider than upper by a small offset each side. Dashed line above floor = extension of lower column face; label "LAP SPLICE IF THIS OFFSET IS LESS THAN 3" (80 mm)".
- Lower bars run straight up to below the beam, then **"BOTTOM BEND"** begins below beam soffit; inclined portion "SLOPE 1:6 MAX" rises through beam depth; top bend at slab top level; bars then continue vertically inside the upper column (lapping with upper bars — Section A-A shows lower bar and upper bar side by side at each corner, 4 + 4 bars).
- Beam bottom bars shown as dots (label "BOT. OF MAIN BARS") near beam soffit.
- Ties below floor, dimension chain (right side, top→down): from bottom of beam main bars **"3" (80 mm) MAX."** to first tie; next tie at **"S MAX."**; ties at the bottom bend placed within **"6" (150 mm) MAX."** of the bend point (3 close ties drawn around the bottom bend).
- Above the floor: first tie of upper column **"½ S MAX."** above top of slab.
- Section B-B: 4-bar square tie, lower column. Section A-A: smaller square, 4 corner bars + 4 lapped lower bars.

### 1.3 Fig 4.10(b) p.102 — "Splice of columns of very different section" (dowel splice)
- Lower column bars run straight up and stop just below the slab top (under top cover), no crank.
- **DOWEL BAR**s (inside upper column line) embedded down into the lower column (ends ~one lap below beam soffit) and projecting up into the upper column to lap with upper bars.
- Lower-column ties continue up through the beam depth (joint) at normal spacing.
- First upper-column tie **½ S MAX.** above slab top.
- Section C-C: small upper column, 4 corner bars (upper + dowel side by side, "LOWER BAR / UPPER BAR" labels). Section D-D: wide lower column, 6 bars (3 per face) with one perimeter tie.

### 1.4 Fig 4.11 p.103 — offset (cranked) bar mechanics and extra ties (ACI 318 rule)
Elevation of one bar at column face, cover shown.
- Crank slope **1 : 6** (triangle: 6 vertical, 1 horizontal).
- Point of lower bend = "A". Horizontal thrust at the bends shown with red arrows.
- Note: "1.5 TIMES THE HORIZONTAL COMPONENT OF THE FORCE IN THE INCLINED PORTION OF THE BAR TO BE TAKEN BY ADDITIONAL TIES, PLACED NOT MORE THAN **8Ø** FROM THE POINT OF BEND AT A".
- Dimension "8Ø + 8Ø" on both sides of bend A: "ADDITIONAL TIES TO BE WITHIN THIS ZONE" (total 16Ø zone centred on the bend).

### 1.5 Fig 4.14(a) p.103 — edge (perimeter) column splice
- Exterior face flush above and below (left side). Interior face steps in.
- Exterior (flush-side) lower bar: small 1:6 crank within beam depth, continues up alongside upper bar; lap length = **"COMP. LAP OF BAR ABOVE"** measured up from slab top.
- Interior (offset) side: lower bar stops straight just below slab top; upper-column bar extends down into lower column a length **"COMP. LAP OF BAR BELOW"** measured down from slab top (acts as dowel).
- Label: "> 80 MM = LAP SPLICE / ≥ 80 MM = DOWEL SPLICE" **[BOOK TYPO?]** — intended "< 80 mm = lap (cranked) splice; ≥ 80 mm = dowel splice".
- 3 closely spaced ties just below beam soffit (at the crank); normal spacing elsewhere.

### 1.6 Fig 4.14(b) p.103 — circular spiral column with flared capital
- Bars cranked **1:6 MAX.** within the capital / slab, then straight into the upper (smaller) column.
- Spiral of lower column stops at the level (dashed line) where capital width = **2D MIN.** (D = column diameter). Upper column spiral starts above slab.
- Lap above slab: "COMP. LAP OF BAR ABOVE". Section A-A: 8 bars on circle within spiral.

### 1.7 Fig 4.15 p.104 — five splice-arrangement variants (elevations, beam + slab)
(a) Edge column, same size: upper bars joggled (cranked inward ~1:6) at their lower end to sit inside the lower bars; lower bars project above floor; lap zone just above slab with 4 closely-spaced ties.
(b) Interior column (beams both sides), same as (a).
(c) Near-same size (lower slightly wider): upper bars stop just above slab, lower bars stop at slab top; separate straight splice bars (dowels) span the floor lapping both; closer ties within/below joint.
(d) Edge column, lower larger and eccentric (outer face flush): lower bars cranked (steeper on the offset side) through beam depth, continuing up to lap with upper bars above slab.
(e) Interior column, upper smaller concentric: lower bars cranked both sides at 1:6 starting below beam soffit to reach upper bar line at slab top; lap above slab; extra ties at the bends below soffit.

### 1.8 Fig 4.16 p.105 — large eccentric offset
- Left side (large offset, "ความเอียง > 1:6"): lower bar rises to top of slab and terminates with a **90° hook turned horizontally inward** (toward column centre) under top cover; a separate straight dowel placed on the upper column bar line, embedded down into lower column (~lap) and up into upper column.
- Right side (small offset, "ความเอียง < 1:6"): lower bar cranked through slab/beam depth and continues up (normal lap).
- Dashed box marks the joint region; lower-column ties to slab soffit.

### 1.9 Appendix p.195 — "การเสริมเหล็กในเสาที่มีการเปลี่ยนขนาด" (4 panels, EIT-style) — **most drawing-ready**
Panel 1 — interior, change **< 75 mm**:
- Lower bars cranked in beam depth, slope label "ความลาดเอียงสูงสุด 1:6" (max 1:6); bend starts ~mid-beam depth, top bend at slab top; bars continue up into upper column (lap with upper bars; upper bars themselves cranked again higher up for the next splice).
- Below beam soffit: **"เหล็กปลอกเรียงเพิ่มจากระยะเรียงปกติ จำนวน 2 ปลอก"** = 2 additional ties over and above normal spacing; first tie **75 mm** below beam soffit, 2nd at **75 mm**.
Panel 2 — interior, change **> 75 mm**:
- Lower bars straight, stop **50 mm** below slab top (cover).
- **DOWEL BARS (เหล็กเดือย)** on upper-column bar line; embedment below slab top = "ระยะต่อทาบเหล็กเสริมยืนที่ด้านล่าง" (lap length of lower column bars); project up into upper column.
- Ties continue through the joint: first tie 50 mm below slab top, then spacing **S**; tie 75 mm below soffit.
Panel 3 — edge column (สำหรับเสาต้นนอก), change < 75 mm:
- Exterior face flush (straight bar); interior-side bar cranked 1:6 in beam depth.
- Ties within the joint at **S ≤ 150 mm**; 2 extra ties at 75 mm below soffit; normal S below.
Panel 4 — edge column, change > 75 mm:
- Exterior bar continuous; interior-side lower bar stops 50 mm below slab top; dowel embedded a lower-bar lap length below slab top; ties 50 mm then S through joint.

---

## 2. SPLICE (LAP) ZONES ALONG COLUMN HEIGHT

### 2.1 Appendix p.191 — interior tied column (จุดต่อคาน-เสาสำหรับเสาปลอกเดี่ยวภายใน), 3-storey elevation
- **Lc** = clear height from top of floor to underside of beam or flat slab ("ใต้ท้องคานหรือแผ่นพื้นไร้คาน").
- Lap ("ระยะทาบ") starts at **"750 ถึง Lc/2"** above floor top (i.e. between 750 mm and Lc/2) → splice in middle of clear height, NOT at floor level.
- Upper bars joggled inward (short crank) just above the lap; lower bars straight.
- Ties: first tie **50 mm** above floor top, then **S**; last tie **50 mm** below beam soffit; "เหล็กปลอกทุกระยะ S" throughout; note the tie S shown also at the first interval above 50.
- No ties drawn inside beam depth (interior joint confined by 4 beams).
- Roof: bars end with **standard 90° hook (ของอมาตรฐาน 90°)** at top of roof slab/beam, both hooks turned **outward** (into the beams).
### 2.2 Appendix p.192 — exterior tied column
- Same Lc, 750-to-Lc/2 lap start, 50 mm first/last tie, S spacing.
- Roof hooks: both bars' 90° hooks turned **toward the interior** (into beam/slab span), none toward the exterior face.
### 2.3 Appendix p.193 — interior spiral column
- Lap zone 750-to-Lc/2 above floor; bars joggled above lap.
- Spiral: **bottom turn at top of floor slab** ("วงล่างของเหล็กปลอกเกลียว"); **top of spiral at level of lowest horizontal reinforcement of beam/flat slab** above ("ยอดของเหล็กปลอกเกลียวสำหรับเสาข้างล่างนี้"; Lc measured to the beam bottom bars "เหล็กล่างของคาน").
- Roof: 90° standard hooks outward.
### 2.4 Appendix p.194 — exterior spiral column
- As p.193 plus: inside the joint above the spiral top, **horizontal ties "เหล็กปลอกในแนวนอน ระยะห่างสูงสุด 150 มม."** (max 150 mm) up to top of beam. Roof hooks turned inward.
### 2.5 Lap rules (p.44–46, p.100, p.103)
- Lap splices used for bars ≤ DB36 (EIT 1008-38). Tension lap: Class A = 1.0 ld, Class B = 1.3 ld, ≥ 30 cm; Class B is default. ld = 0.06·Ab·fy/√f'c; table (f'c 240 ksc, SD40): DB10 12.2, DB12 17.5, DB16 31.1, DB20 48.6, DB25 76.1, DB28 95.4, DB32 125, DB36 158 cm.
- Traditional simple rule: deformed-bar lap ≥ **36 db and ≥ 30 cm** (p.45).
- Column figures label laps as **"COMP. LAP OF BAR ABOVE / BELOW"** (ACI: compression lap), i.e. lap of larger bar governs by its own size (p.103).
- Bundled bars: +20% (3-bar bundle), +33% (4-bar bundle) (p.46).
- Non-contact lap: clear spacing ≤ 1/5 lap and ≤ 15 cm. Staggered laps (Fig 2.34 p.46): spacing between lapped bars ≤ 4Ø or 5 cm; longitudinal stagger ≥ 0.3 × lap; clear gap between adjacent laps ≥ 2Ø or 2 cm.
- Welded / mechanical splices: ≥ 1.25 fy (p.46, p.100, p.183). TempCore (SD40T/SD50T) bars: do not cut threads by turning the bar down; use soft cold-forged (upset) threads; preheat/post-heat when welding (p.15).
- Spiral laps (Table 4.3 p.100): plain uncoated 72db (no hook) / 48db (std hook); deformed uncoated 48db; epoxy 72db / 48db hooked; ≥ 30 cm. Mechanical/welded spiral splice ≥ 1.25 fy.

### 2.6 Mechanical couplers in column — p.196 (upper) and Figs 4.12/4.13 p.103
- p.196: couplers ("ข้อต่อเชิงกลหรือปลอกท่อ") above the floor, **staggered** — adjacent bars' couplers at different heights; extra ties **"เรียงเพิ่มจำนวนชุดละ 2 ปลอก หรือตามที่วิศวกรกำหนด"** (2 additional ties per coupler set, or as engineer specifies). Ties continue through the joint.
- Fig 4.12: sleeve coupler, bars **square cut both ends**, **"2 ADDITIONAL TIES PROVIDED AT EACH END"** (one tie just above and one just below the sleeve drawn).
- Fig 4.13: butt weld, square cut both ends.
- p.183: coupler/sleeve ≥ 125% of bar tensile strength; do not use couplers that require reducing the bar section. Butt weld in tension: 45° single-V prep, 3 mm root gap, weld ≥ 125% bar strength, grind flush both sides.

---

## 3. BEAM-COLUMN JOINTS — interior, exterior (edge), corner, T

### 3.1 Fig 4.21/4.22 p.107 — definitions
Joint = the part of the column within the depth h of the deepest framing beam. Six joint types shown (isometric): (ก) interior, (ข) exterior, (ค) corner, (ง) roof interior, (จ) roof exterior, (ฉ) roof corner. ACI 352: Type 1 (gravity/normal wind) vs Type 2 (inelastic reversals, seismic) — book covers Type 1 (p.108).
### 3.2 Fig 4.25 p.109 — interior joint
- Plan: 8-bar column (square tie + diamond tie, 135° hooks at a corner), beam bars in both directions pass through between column bars; top bars of one direction above the other.
- Section A-A: column ties **continue through the joint** between beam top and bottom layers. Beam bars run continuous, no anchorage needed; only check clashes of column and beam bars.
### 3.3 Fig 4.26 p.110 — exterior joint
- Plan: same 8-bar column; through-beam bars one way; terminating beam from one side.
- Section A-A: terminating beam **top bar hooked 90° down** inside the column core, placed inside the far-face column bars; bottom bar straight into joint beyond column centre (to far side). Column ties continue through joint.
### 3.4 Fig 4.27 p.110 — end column (rigid exterior joint)
- End column elevation, beam framing one side. Beam top bar: horizontal into column, **90° bend down** near far face; **Ld** measured along bar from column face.
- **U-TYPE BARS** (hairpins, 3 layers drawn in red) horizontal, closed end inside column at exterior side, legs into beam.
- Beam SHEAR STIRRUPS closely spaced near column face; **COLUMN TIES** continuous above, through and below joint.
### 3.5 Fig 4.31 p.112 — roof corner joint
- Column outer bar runs up and bends 90° into the beam top (continuous L); beam top bar bends down into the column; **Ld** measured from beam soffit level along the bar into the beam top (dimension drawn from beam-soffit level round the corner). U-type hairpins (3) at joint; stirrups with 135° hooks close to face; column ties continuous right up to beam top.
### 3.6 Fig 4.30 p.112 — corner-joint efficiency under opening moment (test results)
(ก) bars each bent inward crossing at inner corner 32%; (ข) straight crossing bars with end anchors 68%; (ค) top bar looped round 77%; (ง) looped + overlapping legs 87%; (จ) loops plus diagonal bar across the re-entrant corner 115%. Lesson: corner detail needs continuous loops and a diagonal bar.
### 3.7 Fig 4.32/4.33 p.113 — T joint
(ก) vertical bars hooked outward into flanges: 24–40% efficiency. (ข) vertical bars bent to **cross over** (hooks turned toward opposite flange): 82–110%.
### 3.8 Appendix p.185 — beam bar anchorage into column (support)
- Beam top bars embedded into column ≥ **52 db**; bottom bars ≥ **40 db**, measured from column face.
- Alternative ("หรือ") for shallow support: top bar goes in, turns down at far face and returns (U), 52D along bar; bottom bar 40D.
### 3.9 Appendix p.196 (lower) — column planted on transfer beam
- Column bars go down to beam bottom layer and turn **90° outward** (away from column centreline), resting on beam bottom bars; anchorage **40D** measured from beam top along the bar incl. hook.
- Note: "เสาตั้งบนคาน เหล็กปลอกจะต้องเข้าไปในคาน โดยใช้ระยะห่างของเหล็กปลอกเท่ากันโดยตลอด" — column ties must continue into the beam at the same spacing all the way down.
### 3.10 Appendix p.202 — composite column (steel section inside RC column)
- Where the steel section blocks ties, weld ties to the steel section.
- Beam bars passing the steel core transfer force via **TRANSFERRED STEEL PLATES** (welded to steel section, bars lapped/welded to plates) with strength ≥ bars; plan + section A drawn.
### 3.11 Flat-slab heads (brief) p.105–106
Fig 4.17: without drop panel (capital), with drop panel+capital, drop panel only. Fig 4.19: square capital cage – radiating bars both ways + horizontal hoops. Fig 4.20 (circular): "CONCRETE CAST TO HERE BEFORE PLACING COLUMN HEAD CAGE" at capital base; "LAST COLUMN STIRRUP" just below; "SPLICE BARS" through head; "FIRM CAGE"; 50 mm step at capital edge.
### 3.12 Corbels/brackets (brief) p.113–116
Main steel anchored into column with 90° bend down at column far side; outer end welded to steel angle; closed stirrups/hoops distributed over **2d/3** below main steel; outer-edge depth **≥ d/2**; framing bars. If av/d > 1 use vertical stirrups as cantilever (Fig 4.39).
### 3.13 Effective slab width at exterior flat-slab joint (p.108–109): be = 2ct + bc (edge), ct + bc + min(ct, dist. to slab edge) (corner), ct ≤ hc, be ≤ L/12. 45° crack lines drawn from column corners.

---

## 4. TIES — configurations, hooks, spacing

### 4.1 Minimum bars (p.94, Fig 4.3): rectangular ≥ 4 bars (one per corner) in a closed tie; circular ≥ 6 bars in spiral; column side ≥ 20 cm; ρ = 0.01–0.08 Ag; main bars ≥ 12 mm.
### 4.2 Fig 4.4 p.95 — ACI 315 tie patterns (rule: clear gap s between longitudinal bars > 15 cm → the intermediate bar needs a crosstie/extra tie; s < 15 cm → no support needed). Inset: s measured as clear gap along face.
- 4 bars: one square tie, 135° hooks at one corner.
- 6 bars (3 on two opposite faces): s<15 → single tie; s>15 → two overlapping rectangular ties (each enclosing 4 bars). Also "Tie bar" = crosstie with 135° hook one end, 90° other.
- 8 bars (3 per face): s<15 → single tie; s>15 → square + **diamond tie** (hooks at mid-side bar), or square tie + 2 crossties (one with 90° hook one end, 135° other; arrows show crosstie orientation).
- 10 bars (4 on long faces, 1 mid on short): single tie; tie + crosstie; 3 overlapping ties.
- 12 bars: 2 overlapping rectangular + 1 crosstie; alternatively bundled bars in corners (3-bar bundles) with single tie.
- 14 bars: 3 rectangular overlapping ties; or bundles + 1 crosstie.
### 4.3 Fig 4.5 p.96–97 — Thai practice: all closed overlapping ties (no crossties)
(ก) 4 bars/1 tie; (ข) 6 bars/2 ties (two overlapping rectangles, either direction); (ค) 8 bars/2 ties (two rectangles, or square + diamond with diamond hooks at mid-side bar); (ง) T- and cross-shaped columns 8 bars/2 rectangles; (จ) 10 bars/3 ties; (จ) 12 bars/3 ties; (ฉ) 14 bars/3 ties; (ช) 16 bars/3 or 4 ties (incl. octagon/diamond set); (ซ) 18 bars/3 ties; (ฌ) 20 bars/3 ties (incl. diamond). Each tie drawn separately beside the section; **135° hooks of successive ties placed at different corners** (hooks staggered around the section).
### 4.4 Fig 4.6 + Table 4.1 p.98 (ACI 318-14) — tie hook
- Thai practice: closed tie, both ends **135°** hooks, extension **6db ≥ 7.5 cm**, inside bend dia **4db** (DB10–16). Tie sizes used: RB6, RB9, DB10, DB12.
- Table 4.1: 90° hook DB10–16: D=4db, Lext = max(6db, 7.5 cm); DB20–25: D=6db, Lext=12db. 135°: DB10–16 4db, DB20–25 6db, Lext max(6db, 7.5 cm). 180°: 4db/6db, Lext max(4db, 5 cm).
- Elevation: ties at uniform spacing s.
### 4.5 Tie spacing/size (p.99)
- Clear spacing between ties ≥ 4/3 max aggregate. Spacing ≤ min(**16 db main**, **48 db tie**, least column dimension).
- Tie ≥ **DB10** for main bars ≤ DB32; ≥ **DB12** for DB36 and larger or bundles.
### 4.6 Spiral (p.99–100): ≥ 6 bars; spiral ≥ 9 mm; clear pitch ≥ 4/3 agg and ≥ 2.5 cm, ≤ **7.5 cm**; anchor at each end by **1½ extra turns**. ρs ≥ 0.45(Ag/Acore − 1) f'c/fy; ρs = 4Ab/(hcore·s).
### 4.7 Hook table (Appendix p.182, in mm) — for bar-bending/cut list
- Main bars D: 6db (6–25 mm), 8db (28–36), 10db (44–57). 180°: ext 4db ≥ 60 mm; 90°: ext 12db.
- G/J (mm), 180° | 90°: RB9 55: 110/73 | 120/150; DB10 60: 120/80 | 130/160; DB12 75: 130/99 | 160/200; DB16 100: 160/132 | 210/260; DB20 120: 190/160 | 260/320; DB25 150: 240/200 | 320/400; DB28 225: 330/281 | 380/550; DB32 255: 370/319 | 430/620; DB36 290: 420/362 | 480/800.
- **Tie hooks** (90° and 135°): H = 6db (RB6–DB16), 12db (DB20–25, 90° only); D = 4db (RB6–DB16), 6db (DB20–25). Table (D, G, J pairs as printed under headings "180°"/"90°" — headings evidently mean 135°/90° **[BOOK TYPO?]**): RB6 25: 40/60 | 50/45; RB9 35: 60/80 | 70/65; DB10 40: 70/90 | 80/75; DB12 50: 80/110 | 100/90; DB16 65: 100/150 | 130/120; DB20 120: 260/320 | 180/170; DB25 150: 320/400 | 230/210.
- **Seismic tie 135° hook**: extension **10db**; DB10 D40 G120 J100; DB12 50/150/120; DB16 65/190/160; DB20 120/260/220; DB25 150/330/280.
### 4.8 Tie arrangement along column height (appendix p.191–195, Fig 4.10)
- First tie 50 mm above floor/footing top (p.191–192) — ACI version: ½S (Fig 4.10) / S/2 above footing (p.203).
- Last tie 50 mm below beam soffit; ties omitted inside interior joints (p.191) but continued in joints of edge columns at section change (S ≤ 150, p.195) and in exterior spiral columns (≤ 150 mm, p.194); ACI figs 4.25/4.26 show ties through all joints.
- Extra ties: 2 extra ties @75 mm below soffit at cranks (p.195); ties within 8Ø each side of bend (Fig 4.11); first tie ≤ 80 mm below beam bottom bars and bend ties within 150 mm (Fig 4.10a); 2 per coupler set (p.196).
### 4.9 Tie-wire types (Fig 1.9 p.18): Type C saddle tie and Type D wrap-and-saddle tie are used to tie column ties to vertical bars.

---

## 5. STARTER BARS / DOWELS FROM FOOTINGS

### 5.1 Appendix p.203 — footing cast in one pour ("เทฐานรากครั้งเดียว")
- Column **DOWELS (เหล็กเดือยเสา), same size as column main bars**, go down to the footing bottom mat and end in **90° hooks turned outward**, hook level **75 mm** above footing soffit (on top of bottom mat). Hook leg "ของอ 90°".
- **Staggered embedment**: 50% of column bars ("ล้วงถึงเหล็กฐานราก") go down to the footing steel; the other 50% extend into the footing **≥ 50D** (50 × column bar Ø) measured from footing top.
- Shear key (trapezoidal recess) in footing top under column.
- Column ties: spacing S in column; **first tie S/2 above footing top**; ties continue inside the footing at spacing S down to the hooks (≥ 3 ties drawn in footing).
- Mass-concrete notes: placing temp ≤ 36 °C; core ≤ 77 °C; core–surface difference ≤ 20 °C (e.g. cooling pipes); crack-control method to be submitted.
### 5.2 Appendix p.204 — footing cast in two layers ("เทฐานรากสองชั้น", thickness > 2 m)
- **100%** of column bars/dowels go down to footing bottom steel, 90° hooks outward, 75 mm from soffit. Ties S in footing, first S/2 above top.
- Layer 1 (first pour) gets extra top mesh **DB16@250#**; stitch bars **DB16×1300 @500**, embedded 300 mm into layer 1 and 1000 mm into layer 2; joint surface roughened + BONDING AGENT.
### 5.3 Fig 6.5 p.139 — isolated footing example
- Column bars extend down to bottom mat and **splay/bend outward** (90° legs) on top of mat — plan shows legs radiating diagonally from column corners. Footing 2.50×2.50×0.50 m, 7 DB20 # both ways, 1.00 m to ground, 5 cm lean concrete + 5 cm compacted sand. Column ties continue into footing.
### 5.4 Fig 6.8 p.140 — eccentric (property-line) footing
- Column at footing edge; column bars go down to bottom and bend **90° inward** (toward footing interior); column ties continue into footing; footing with top & bottom bars closed by vertical legs at ends; 5 cm lean + 5 cm sand.
### 5.5 Cover (Table 1.7 p.16 / Table 4.2 p.99): cast against earth 7.5 cm; exposed DB20–60 5 cm, DB16 and smaller 4 cm; interior columns (main bars, ties, spirals) 4 cm (spiral column: 4 cm to outside of spiral, Fig 1.8). Bar clear spacing ≥ max(db, 2.5 cm, 4/3 agg).
### 5.6 Pile cap (p.142): piles at 3D, edge 1.5D; bottom reinforcement bent up at ends. (No column dowel detail drawn for pile caps.)

---

## 6. COLUMN TOP TERMINATION
- Appendix p.191/193 (interior): column bars run to top of roof slab (under cover) and end with **standard 90° hook**, hooks turned **outward** over beams on both sides.
- Appendix p.192/194 (exterior/edge): 90° hooks turned **inward** (toward interior span), none over the exterior face; exterior spiral column also gets horizontal ties ≤ 150 mm through the roof joint.
- Fig 4.31 (roof corner): outer column bar bent 90° into beam top and lapped (Ld) with beam top bar, plus U-bars; ties continued to beam top.
- Fig 4.20: column head in flat slab — column concreted to base of capital before placing head cage; last column stirrup just below.

---

## 7. SCHEDULE / SECTION PRESENTATION
### Fig 4.9 p.101 — column schedule examples
- Table form: column marks C1, C2, C3… across; level bands down ("ELEV. +3.70 / +0.20 / −1.50" with arrow from lower to upper level; top labelled หลังคา = roof, bottom ฐานราก = footing).
- Each cell: section with dimension lines (e.g. 300 wide × 200 deep), bars and tie shape drawn, text "6 DB12", "ป RB6 @ 200" (single tie) or "2-ป RB6 @ 200" (two ties). Examples: 300×200 6DB12; 300×200 8DB16 2 ties; 200×200 4DB16; 300×300 8DB16 with square+diamond ties (2-ป).
- Second (older) style: sizes in metres (0.20, 0.25), "4 Ø 12 มม.", "ป Ø 6 มม. @ 0.20 ม.", levels +7.80/+4.30/+0.30/−1.50.
- Text: detailed drawings should add elevations and splice details where column section changes (p.101).

## 8. OTHER USEFUL ITEMS
- Bend diameters (EIT 1008-38, Table 1.9 p.20): 6db (6–25 mm), 8db (28–36), 10db (44–57); stirrups/ties 6–16 mm: 4db. Heat-treated SD40T/SD50T bending same.
- Beam lap location (Fig 2.33 p.45): top bars spliced at midspan, bottom near supports (L/3–L/4); lap ≈ A.
- Appendix p.184: beam first stirrup 50 mm from column face.

## Pages with no column-relevant content (viewed)
p.14 (bar tables), 19, 43 (primary/secondary beam), 137–138, 141, 181 (title), 186–190, 197–201, 205 (pile splice), 206 (blank).

## Unreadable
None — all figures in range were legible at 200–700 dpi crops.

---

## ACI Detailing Manual MNL-66(20) cross-check (2026-09-29)

Material is in `references/aci_mnl66/` (COL-1, COL-20, COL-100 … 104, COL-200 … 202, the Detailing Corner column articles); findings are in `REVIEW_ACI_MNL66.md`. MNL-66 follows ACI 318-19; EIT 011008 follows ACI 318-11.

| Topic | Our source | ACI | Decision / sheet |
|---|---|---|---|
| Lateral support of bars | EIT 7.10.5.3 | 318-11 7.10.5.3 = 318-19 25.7.2.3; COL-20. A tie leg running past a bar does **not** hold it | The old 1102/9 (c) left two adjacent side bars unsupported, **fixed**. Tie types A – J on **1103/1**: crossties on alternate intermediate bars |
| Offset bars at a floor | EIT 7.8.1 (1:6, ties within 150, ≥ 75 → dowels) | COL-100 / 200 and Detailing Corner: lower bars bent inside the slab / beam depth, top bend ≤ 75 below the slab top | **D4: lower bars cranked inside the joint** (1101/1). Offset labels "< 75" / "≥ 75" (1102) |
| Terminated lower bars at a size change ≥ 75 | TATA: stop 50 below the top | COL-200 (d): hooked into the slab | 90° hook inward (1102/2, 4) |
| Footing dowels | TATA: 90° hook outward | 318-11 21.12.2.2: hooks toward the column centre in special frames fixed at the base; confinement through the footing depth at an edge within h/2; compression embedment ldc (a hook does not count) | 1102/6 notes |
| Roof termination | TATA: hook, "or ldh" | Hook **and** ldh above the soffit | 1102/7 |
| Laps that do not fit their zone; ρ > 4 % at a lap | DPT zones | R10.6.1.1 (about 4 %); couplers, Type 1 / 2 (318-11 21.1.6) | 1101 note 4 |
| Tie material | EIT allows RB | Deformed ties (plain only for spirals) | **D3: DB10 minimum in intermediate / special frames** (1101 note 2) |
| Spirals | EIT 7.10.4 | Laps 48 db / 72 db; ties above the spiral where beams do not frame on all sides | 1101 note 7; 1103/3 |
| Tie types, circular hoops, couplers, tie-spacing table | TATA sheets (partial) | COL-20, COL-201, COL-202, Detailing Corner tables | **New sheet 1103** |
| High axial (Pu > 0.3 Ag f'c): every perimeter bar held, hx ≤ 200 | Not in 318-11 or DPT | 318-19 18.7.5.2 (COL-103) | **D5 = option B (2026-09-30):** 1103 note 6 + type EH where the design applies 18.7.5.2(f); not a blanket rule |
| Column supporting a discontinued wall | DPT 5.2.9.4.5 (threshold blank in the source) | COL-104; 318-11 21.6.4.6: Pu > Ag f'c/10 | **1102/9** (2026-09-30): hoops full height, ≥ ld into the wall, ≥ 300 into the footing |
