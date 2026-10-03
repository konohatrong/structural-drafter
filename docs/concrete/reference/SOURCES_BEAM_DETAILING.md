# Beam detailing sources: DPT 1301/1302-61, EIT 011008-21 and the TATA RC detailing handbook (extracts)

Working extracts behind the typical beam detail sheets STR-ST-1111 / 1112 / 1113 (generator `jobs/typical_details/td_beams.py`, rules in `TYPICAL_DETAILS_INSTRUCTION.md`).

- Part A: DPT 1301/1302-61 - seismic beam detailing by frame type (5.2.6 - 5.2.8, 5.2.10). Page refs = PDF pages.
- Part B: EIT 011008-21 - general beam detailing (ch. 7, 8, 10, 11, 12). EIT clause numbers differ from ACI 318-11 from 12.9 on; cite EIT numbers. Page refs = PDF pages.
- Part C: TATA handbook - Thai office practice (cut-offs, cantilevers, secondary beams, steps, openings). Page refs = printed pages (PDF = printed + 8).

Values are as printed; suspected misprints are flagged in each part and summarised in part B's flag table.

---

# Part A. DPT 1301/1302-61 (seismic) - beam clauses


Source: `G:\My Drive\##Textbook\DPT\1301-1302-64.pdf` (มยผ. 1301/1302-61, ฉบับปรับปรุงครั้งที่ 1).
Page refs = **PDF page** (printed page = PDF − 14 in this range, e.g. PDF 116 = printed 102).
Text taken from decoded `dpt.txt`, cross-checked against page renders `db_112…db_137.png` (all figures and all equation lines viewed as images; zooms `db_116_rotL/R.png`, `db_131_z.png`, `db_131_zp.png`, `db_137_z.png`).
Wording paraphrased. SI equations given, metric (kgf, cm, ksc) in brackets.

**Seismic design category letters (Table 1.6-1/1.6-2, PDF p.49–50):** ก = A (no seismic design required), ข = B, ค = C, ง = D. Below: written as B / C / D with the Thai letter where helpful.

Column-only items (5.2.7.4, 5.2.9 etc.) are NOT repeated — see `SOURCES_COLUMN_DETAILING.md`. Joint items are repeated only where they govern beam bars.

---


> **Correction (2026-09-29, from the slab extract):** DPT 2.11.5 (p.77) also requires members of an RC building frame that are NOT part of the seismic force-resisting system in SDC D to satisfy **ACI 318-14 §18.14**. 5.2.2(ค) is therefore not the only non-SFRS provision. See SOURCES_SLAB_DETAILING.md Part A §2.

## 0. Which frame type may be used (context for the sheet title block)

| Frame | Permitted SDC | Clause |
|---|---|---|
| Ordinary RC MRF (R=3) | B only | Table 2.3-1 (p.53–54), 5.2.2(ก) (p.104) |
| Intermediate RC MRF (R=5) | B, C; D only if height ≤ 40 m and member strength forces +40 % | Table 2.3-1, 2.3.1.2, 5.2.2(ข)(ค) |
| Special RC MRF (R=8) | B, C, D | Table 2.3-1, 5.2.2 |

- 5.2.2(ง) (p.105): intermediate frames in "watch areas" must meet at least 5.2.7.4 (column clause) — no additional beam item.
- 5.2.2(ค) (p.104–105): in SDC D, members NOT designed as part of the seismic-force-resisting system must be designed for gravity load combined with the effects of the design lateral displacement. **This is the only provision on non-SFRS members for beams** (there is no ACI-18.14-style detailing clause in DPT). → Detail per EIT/ACI 318 (5.2.1 fallback).
- 5.2.1 (p.104): where DPT is silent, use ACI 318 or other accepted standards.

---

## 1. 5.2.5.2 Moment frames with masonry infill (PDF p.111)

- No beam detailing rule. Only an analysis rule: where infill acts in the main lateral system, consider frame–infill interaction (irregularity, flexure/shear/anchorage/crushing failure modes, interaction forces); cracked infill may be modelled as an **equivalent compression strut** (columns = vertical, **beams = horizontal members**, wall = diagonal strut), per Annex ง or DPT 1303.
- 5.2.5.1 (infill next to columns) is column-only; its one "≤ d/2" item applies to columns.

---

## 2. 5.2.6 Ordinary moment frames — beams (PDF p.112)

- **5.2.6(ก)** SDC B (ข): beams of ordinary MRF must have **at least 2 main bars top and 2 bottom, continuous over the full beam length**, anchored enough to develop **yield in tension** (fy).
- 5.2.6(ข) is column shear only (clear height / long side ≤ 5 → 5.2.7.2).
- Nothing else for ordinary beams: stirrups, hooks, laps, first stirrup → EIT / ACI 318 (5.2.1).

---

## 3. 5.2.7 Intermediate moment frames — beams (PDF p.112–121)

### 5.2.7.1 Definition (p.112)
- **Beam** = frame member with factored axial load **≤ 0.10 A_g f'c**; above that it is a column.

### 5.2.7.2 Shear strength (beam part) (p.112, Fig 5.2-2 p.115)
Design shear strength of beams (also columns, flat slabs) for seismic effects ≥ **either one** of:
- **5.2.7.2.1** Shear when both member ends reach **nominal moment strength M_n**, plus shear from factored gravity load (Fig 5.2-2);
- **5.2.7.2.2** Maximum shear from design load combinations with the earthquake effect taken as **2 × E** (E as in the Ministerial Regulation on seismic construction).

**Fig 5.2-2 "Example of shear calculation per 5.2.7.2.1" (p.115, printed rotated)**
- Left: stippled 2-bay/2-storey frame elevation; labels "เสา" (column), "คาน" (beam); **L_c** = beam clear span between column faces; **H_c** = column clear height between beam faces.
- Beam free body: bar of length L_c with uniform load **W_u** (downward arrows), end moments **M_n1** (left) and **M_n2** (right) both acting in the same rotational (sway) sense. Under it a trapezoidal shear diagram "แรงเฉือนในคาน", max **V_u1** at left end.
  - **V_u1 = (M_n1 + M_n2)/L_c + ½ W_u L_c**
- Column free body: axial **P_u** both ends, end moments **M_n3**, **M_n4**, clear height H_c, end shears **V_n2** (rectangular shear diagram "แรงเฉือนในเสา").
- Note: W_u and P_u are factored loads from the D + L + E combination.
- For special frames (5.2.8.4.1) the same figure is used with M_pr in place of M_n.

### 5.2.7.3 Beam reinforcement (p.112–113, Fig 5.2-3 p.116)
- **5.2.7.3.1 Moment strength**
  - At the joint face: **+M_n ≥ (1/3)(−M_n)** at that same face.
  - At any section along the beam: both +M_n and −M_n **≥ (1/5)** of the maximum moment strength at the faces of either end joint.
- **5.2.7.3.2 End zone:** within **2h** (2 × total beam depth) from the support face, stirrup spacing ≤ least of:
  1. **d/4**;
  2. **8 d_b** of the smallest longitudinal bar;
  3. **24 d_b** of the stirrup (hoop) bar;
  4. **300 mm**.
  - **First stirrup ≤ 50 mm** from the support face.
- **5.2.7.3.3 Elsewhere:** stirrup spacing ≤ **d/2**.
- **5.2.7.3.4 Laps:** lapping top **and** bottom longitudinal bars **should be avoided** within **2h** from the support face (advisory wording "ควร").
- No min-bar-count / ρmax rule for intermediate beams in DPT (→ EIT/ACI).

**Fig 5.2-3 "Beam reinforcement details" (p.116; page printed rotated 90°, described in reading orientation)**
- **Layout:** elevation of a beam of total depth **h** (vertical dimension at far left), spanning from an **exterior column** ("เสา", left) to an **interior column** ("เสา", right); beam continues beyond the interior column to the right (break line); a break line also at midspan of the first bay. Columns continue above and below the beam with break lines.
- **Exterior joint (left):**
  - Top bar runs into the column almost to the outer column face and turns **90° down**; bottom bar runs in and turns **90° up**. The two short vertical tails sit just inside the outer face, pointing toward each other, **not overlapping** (gap at mid-depth).
  - Dimension **l_dh** from the **inner (beam-side) column face** to the **outer side of the vertical hook tail**.
- **Interior joint (right):** top and bottom bars run **straight and continuous** through the column. No joint hoops drawn.
- **Stirrup zones:** at the exterior column face and on **both sides** of the interior column: dimension **2h** from the column face, labelled "เหล็กปลอก ระยะเรียง ≤ s1" (stirrups at spacing ≤ s1). Only the first and last stirrup of each zone are drawn (schematic).
  - Leader "**≤ 50 มม.**" (≤ 50 mm) from each column face to the first stirrup — at the exterior face and at both faces of the interior column.
- **Middle zone** between 2h zones: "เหล็กปลอก ระยะเรียง ≤ d/2".
- A thin mid-depth horizontal line with small circles where it meets each drawn stirrup (drafting reference; not explained in the figure).
- **Moment labels:** −M_nl (leader to top bar) and +M_nl (to bottom bar) at the left face; −M_nr and +M_nr at the left face of the interior column.
- **Notes printed on figure:**
  - ก) s1 ≤ least of (1) ¼ effective depth; (2) 8 × smallest longitudinal bar dia.; (3) 24 × stirrup dia.; (4) 300 mm.
  - ข) (1) +M_nl ≥ (1/3)(−M_nl); (2) +M_nr ≥ (1/3)(−M_nr); (3) +M_n and −M_n at any section ≥ (1/5) of the larger of −M_nl and −M_nr.
- **What to draw:** 2h zones at every column face (both sides of interior columns), first stirrup ≤ 50 mm, s1 in zone, d/2 outside; exterior-column hooks turned in (top down, bottom up) at far side of column with l_dh; bars continuous through interior joints; keep laps out of 2h zones.
- Note: l_dh for intermediate frames is not given a formula in 5.2.7 — use EIT/ACI (or 5.2.10.4 conservatively).

### 5.2.7.5 Joint (beam-relevant only) (p.118–120)
- V_j ≤ φV_n, φ = 0.85; V_j = (A_s1 + A_s2) f_y − V_col with both beams at M_n in the same sway sense (Fig 5.2-5).
- V_n = 1.7 / 1.25 / 1.0 √f'c A_j (SI) [5.4 / 4.0 / 3.2 metric] for joints confined on 4 faces / 3 faces or 2 opposite faces / others (Eq. 5.2-8…10, Fig 5.2-6).
- **A face counts as confined by a beam only if beam width ≥ ¾ column width at that face AND beam depth ≥ ¾ of the deepest beam at the joint** (p.119) → beam sizing rule a draftsman may need to flag.
- A_j: depth = column dimension parallel to the beam bars; effective width ≤ b + h and ≤ b + 2x (x = smaller offset of beam side face to column side face) (Fig 5.2-7, p.120).
- Joint hoops A_v ≥ c1 s /(3 f_y) over the deepest beam depth (5.2.7.4.4) — column item, see column file.

### 5.2.7.6 Seismic hooks — intermediate frames (p.121, Fig 5.2-8)
- Hooks of stirrups and hoops **may generally be 90°** with extension **≥ 6 d_b** (of the stirrup bar).
- **Public buildings** (theatres, assembly halls, hotels, hospitals, schools etc.) **or buildings designed for ductility**: hooks **should be 135°**, or if 90° hooks are used they **should be restrained by a hook-clip** holding the 90° legs, **in the zones near joints** — i.e. within **2h** of Fig 5.2-3 (beams) or l0 of Fig 5.2-4 (columns).
- No crosstie rule for intermediate beams in DPT.

**Fig 5.2-8 "Hook detail for seismic resistance, intermediate moment frames" (p.121)**
- Two portrait rectangular closed stirrups with rounded corners; the hook is at the **top-left corner**; dashed circle marked **D** = inside bend diameter (value not given).
- (ก) "90° hook (for general buildings)": one end turns around the top-left corner and continues horizontally along the top side as a straight tail dimensioned **6d_b (≥ 75 mm)**; the other end is the vertical leg closing at the corner.
- (ข) "135° hook (for public buildings)": both ends bend at the top-left corner **135°** (angle marked from the vertical leg) and the tails point diagonally into the core, each **6d_b (≥ 75 mm)** long.
- The **≥ 75 mm** minimum appears only in the figure, not in the clause text.

---

## 4. 5.2.8 Special moment frame BEAMS (PDF p.121–123)

5.2.8 **supplements 5.2.7**; where both apply, the stricter governs. **No figure is dedicated to special beams** (DPT reuses Fig 5.2-2 for shear; Figs 5.2-9…11 are column hoops; Fig 5.2-12 shows the joint).

### 5.2.8.1 Scope / geometry (p.121)
- **5.2.8.1.1** Factored axial compression **P_u ≤ A_g f'c / 10**.
- **5.2.8.1.2** Clear span **l_n ≥ 4 d** (d = effective depth, as printed).
- **5.2.8.1.3** Width **b_w ≥ the lesser of 0.3h and 250 mm** (as printed "ค่าที่น้อยกว่า" = lesser; same wording as ACI 318-14 18.6.2.1(b)). Note: task brief said "0.3h and 250" — the standard says *lesser*.
- **5.2.8.1.4** Beam projection beyond the column side face, **on each side ≤ lesser of the column width and ¾ of the column depth** (column depth = dimension parallel to the beam).

### 5.2.8.2 Longitudinal reinforcement (p.122)
- **5.2.8.2.1**
  - At any section, top and bottom steel each **≥ 1.4 b_w d / f_y** [14 b_w d / f_y metric], unless the steel provided exceeds the calculated requirement by 1/3 (i.e. ≥ 4/3 × required).
  - **ρ ≤ 0.025**.
  - **At least 2 bars continuous at both top and bottom.**
- **5.2.8.2.2**
  - At the joint face: **+M_n ≥ ½ (−M_n)** at that face.
  - At any section along the member: +M_n and −M_n **≥ ¼** of the maximum moment strength at the joint faces.
- **5.2.8.2.3 Lap splices of flexural bars**
  - Permitted only where **hoops or spirals enclose the full lap length**, at spacing **≤ lesser of d/4 and 100 mm**.
  - Laps **not permitted**:
    1. within joints;
    2. within **2h** (twice member depth) of the joint face;
    3. where analysis shows flexural yielding from inelastic lateral sway (plastic hinge regions).
  - (No mechanical-splice clause for beams in DPT → ACI.)

### 5.2.8.3 Transverse reinforcement (p.122–123)
- **5.2.8.3.1 Hoops required over:**
  1. **2h** from the support face toward midspan, at **both ends**;
  2. **2h on both sides** of any section where flexural yielding may occur from inelastic sway.
- **5.2.8.3.2**
  - **First hoop ≤ 50 mm** from the support face.
  - Hoop spacing ≤ least of:
    1. **d/4**;
    2. **8 d_b** of the smallest longitudinal bar (**8 d_b as printed — NOT 6 d_b** of ACI 318-14; verified on image p.122);
    3. **24 d_b** of the hoop bar;
    4. **300 mm**.
- **5.2.8.3.3** In hoop zones, perimeter longitudinal bars must have **lateral support per the accepted RC code** (DPT gives no numbers; it does not point to 5.2.9.4). [Reference, not DPT: ACI 318-14 18.6.4.3 → 25.7.2.3: every corner bar and alternate bar supported by a hoop corner or crosstie hook with included angle ≤ 135°; no unsupported bar > 150 mm clear from a supported bar.]
- **5.2.8.3.4** Where hoops are not required: **stirrups with seismic hooks at both ends**, spacing **≤ d/2**.
- **5.2.8.3.5** Stirrups or ties required to resist shear must be **hoops** over the lengths of members specified in 5.2.8.3, 5.2.9.4 and 5.2.10.2.
- **5.2.8.3.6 Two-piece hoop** permitted: a **stirrup with seismic hooks at both ends, closed by a crosstie** (cap tie).
  - Consecutive crossties engaging the same longitudinal bars must have their **90° hooks at opposite sides** of the member (alternate).
  - If the longitudinal bars held by the crossties are confined by a slab on **one side only**, the crossties' **90° hooks must all be on that (slab) side**.
- "Seismic hook" is not defined numerically in DPT text; figures for columns (5.2-10/5.2-11, p.126–127) show **135°, extension 6d_b ≥ 75 mm**; crosstie 135° one end / 90° with 6d_b the other. Use the same for beam hoops/crossties.

### 5.2.8.4 Shear (p.123)
- **5.2.8.4.1** Design shear **V_e** from the beam between joint faces with **probable moment M_pr at both faces acting in opposite sense** (double curvature/sway), plus factored ("ultimate") gravity load on the span — as Fig 5.2-2 with M replaced by M_pr (text prints "replace M_u by M_pr"; figure uses M_n).
  - **M_pr computed with bar stress 1.25 f_y.**
  - V_e = (M_pr1 + M_pr2)/l_n + w_u l_n /2 (by analogy with Fig 5.2-2).
- **5.2.8.4.2** Over the 5.2.8.3.1 hoop lengths, design transverse steel with **V_c = 0** when **both**:
  1. the earthquake-induced part of V_e ≥ the **maximum required shear strength within the member** (as printed — ACI says "≥ one-half"; DPT column clause 5.2.9.5.3 says "≥ half"; **probable omission of "½" — flag, uncertain**);
  2. factored axial compression incl. EQ **P_u < A_g f'c / 20**.

---

## 5. 5.2.10 Joints of special moment frames — beam bar items (PDF p.129–131)

- **5.2.10.1.1** Beam bar force at the joint uses **1.25 f_y**.
- **5.2.10.1.2** Joint φ = **0.85**.
- **5.2.10.1.3** Beam longitudinal bars terminating in a column should **extend to the far face of the confined column core** and be anchored: tension per 5.2.10.4; compression per the column/RC code.
- **5.2.10.1.4** Beam bars passing **through** the joint: column dimension parallel to those bars **≥ 20 d_b** of the largest beam bar (normal-weight); **≥ 26 d_b** (lightweight). → Drafting check: max beam bar dia ≤ h_col/20.
- **5.2.10.2** Joint hoops (column confinement 5.2.9.4) through the joint, reduced to **½** amount with spacing up to **150 mm** within the depth of the **shallowest** beam only when beams frame into **all 4 faces** and each beam width ≥ **¾ column width**; where a face has no beam, full 5.2.9.4 hoops are required to confine the beam bars (5.2.10.2.3).
- **5.2.10.3** Joint V_n per 5.2.7.5.3; lightweight ≤ ¾ of that.
- **5.2.10.4.1 Hooked bars (standard 90° hook), d_b 9–32 mm, normal-weight:**
  - **l_dh ≥ max{ 8 d_b, 150 mm, f_y d_b / (5.3 √f'c) }** — Eq. 5.2-17 [metric: f_y d_b / (17 √f'c)].
  - **Denominator is 5.3 (verified on image p.130), not 5.4.**
  - Lightweight: l_dh ≥ max{10 d_b, 200 mm, 1.25 × Eq. 5.2-17}.
  - **The 90° hook must be located within the confined column core** (or boundary element).
- **5.2.10.4.2 Straight bars (9–32 mm):** l_d ≥
  - **2.5 l_dh** if the concrete cast in one lift beneath the bar ≤ 250 mm (bottom bars);
  - **3.25 l_dh** if > 250 mm (top bars).
- **5.2.10.4.3** Straight bars terminating at a joint must pass through the confined column core; any part of l_d **outside the confined core × 1.6**.
- **5.2.10.4.4** Epoxy-coated: apply accepted-code factor.

**Fig 5.2-12 "Example of bar hooking at a joint" (p.131)** — exterior/corner joint
- **Left, plan "แนวแปลน (เหล็กเสริมบน)" (top steel):**
  - Rectangular column, 14 bars (5 top row, 5 bottom row, 2 intermediate each side). Left and bottom faces are free (exterior). One beam enters from the top of the plan, the main beam from the right; **the bars of both beams run across the column to the far side** (bars from the right beam reach the left face region, bars from the top beam reach the bottom face region), passing between column bars.
  - Three joint hoops, colour-coded: yellow perimeter hoop (135° hooks at bottom-right corner), brown inner hoop around middle bars of top/bottom rows (hooks top-right), green hoop around the side intermediate bars (hooks top-left) → hook corners staggered.
  - Section A-A cut along the right-hand beam.
- **Right, elevation "แนวระดับ (รูปตัด A-A)":**
  - Column continuous above and below (break lines); beam frames in from the right; beam top face shown by a step in the outline.
  - Beam **top bar** runs to the far (left) side of the column, just inside the far-face column bars, and bends **90° down**; **bottom bar** bends **90° up** at the same place. The two vertical tails **overlap side by side** over the middle of the joint depth.
  - Dimension **≥ l_dh** from the **column face on the beam side** to the **outside of the hook tail** at the far side.
  - Transverse-beam bars appear as dots: the top layer sits just **above** the main top bar (transverse top bars outermost); the bottom layer sits just **above** the main bottom bar (main bottom bar lowest). Read from the drawing; the standard gives no layering rule.
  - **Joint hoops** (three colours) continue at regular spacing through the whole joint depth — about 6 levels shown, the top one just above the beam top (in the column), the lowest just above the bottom bar layer.
  - Two blue beam hoops shown just outside the column face; the first is very close to the face (consistent with ≤ 50 mm, 5.2.8.3.2).
- **What to draw (exterior special joint):** bars to far side of confined core, hooks inside column cage (top hook down, bottom hook up), l_dh from column face, joint hoops through full beam depth, first beam hoop ≤ 50 mm.

---

## 6. 5.2.11.7 Coupling beams (special walls) (PDF p.136–137, Fig 5.2-13) — brief

- **5.2.11.7.1** **l_n/h ≥ 4** → design as a special-frame beam per **5.2.8**; 5.2.8.1.3 (b_w) and 5.2.8.1.4 (width vs column) may be waived if analysis shows adequate lateral stability.
- **5.2.11.7.2** **l_n/h < 4** → **two intersecting groups of diagonal bars**, symmetric about midspan, **permitted**.
- **5.2.11.7.3** **l_n/h < 2** with V_u "**< 0.34 √f'c A_cw**" (SI) [1.06 metric] (as printed) → diagonal reinforcement required, unless loss of coupling-beam stiffness/strength is shown not to impair gravity capacity, egress, or integrity of non-structural parts and their connections. **Uncertain:** the "<" is likely a misprint of ">" (ACI 318: diagonal required when V_u > 0.33 √f'c A_cw).
- **5.2.11.7.4** Diagonally reinforced coupling beams:
  1. Each diagonal group **≥ 4 bars**, forming a core whose sides, measured to the outside of the transverse steel, are **≥ b_w/2** (perpendicular to the beam plane) and **≥ b_w/5** (in the beam plane, perpendicular to the diagonal).
  2. **V_n = 2 A_vd f_y sin α ≤ 0.85 √f'c A_cw** (Eq. 5.2-20) [metric 2.65 √f'c A_cw]; α = angle between diagonal bars and beam axis; A_vd = total area of bars in each diagonal group.
  3. Transverse steel around each diagonal group per **5.2.9.4.1–5.2.9.4.3** (column confinement rules).
  4. Diagonals anchored to develop **f_y in tension** (into the walls).
  5. Diagonal steel counts toward M_n.
  6. Provide longitudinal and transverse bars in the beam at least the **deep-beam minimum**.
- **5.2.11.4.5** (p.134): V_n of horizontal wall segments and coupling beams **≤ 0.85 √f'c A_cw** [2.65 metric].

**Fig 5.2-13 "Example of diagonal reinforcement in a coupling beam" (p.137)**
- Elevation "รูปด้าน": a short deep beam between two wall piers (wavy break outlines). Two diagonal bar groups (each drawn as two parallel lines) cross at midspan (centreline ℄ marked) in an X, running from the bottom of one wall to the top of the other, each **extending well into the walls** (anchorage). Along the diagonals within the beam, closely spaced **ties perpendicular to the diagonal** (confining hoops) are drawn; they stop at the wall faces (diagonals continue unconfined into the wall).
- Also within the beam: a grid of vertical stirrups (closely spaced, full beam depth) and 4 horizontal longitudinal bars (top, bottom and two intermediate) — the deep-beam minimum steel of item (6).
- Label: "total area of bars in each diagonal group, **A_vd**" pointing to an ellipse around one group where it enters the right wall; **α** measured from horizontal to the diagonal.
- **Section A-A** (right): tall narrow rectangle; outer closed stirrup with corner bars and side bars; inside, **two small rectangular hoops, each with 4 bars** (one upper, one lower) = the two diagonal cores.

---

## 7. Diaphragm collectors — brief (clause 2.9.2, PDF p.72)

- Where seismic force must be transferred from part of the building to the lateral system, provide **collector elements** with adequate strength.
- SDC C and D: collectors, their connections to the lateral system and to each other are designed for the maximum of:
  1. transferred force from equivalent static forces (Ch. 3) × **Ω0** + gravity (2.5.3);
  2. transferred force from diaphragm force Eq. 2.9-1 × **Ω0** + gravity;
  3. transferred force from diaphragm force Eq. 2.9-2 (≥ 0.2 S_DS I w_px, ≤ 0.4 S_DS I w_px, Eq. 2.9-3) + gravity.
- Fig 2.9-1: plan showing collectors transferring diaphragm force into a stair-core shear wall; a full-length shear wall needs no collector.
- **No detailing (bars, hoops, splices) is prescribed for collector beams** → ACI 318 (5.2.1).
- 2.2.3 (p.52): connections of any part to the diaphragm designed for ≥ **5 %** of its D+L reaction.

---

## 8. Items NOT found in DPT (fall back to EIT/ACI 318 per 5.2.1)
- Beam minimum steel / ρmax / min bars for intermediate beams; ordinary-beam stirrup spacing and hooks.
- l_dh formula for intermediate frames (Fig 5.2-3 shows l_dh without an equation).
- Seismic-hook definition (only figures show 135° / 6d_b ≥ 75 mm).
- Mechanical/welded splices in beams; beam skin (side-face) bars; T-beam slab bar counting (only in 5.2.9.2.2 for strong-column check).
- Explicit detailing of beams not part of the SFRS (only the SDC-D design-displacement rule 5.2.2(ค)).

---

## SUMMARY TABLE — beam detailing by frame type

| Requirement | Ordinary MRF | Intermediate MRF | Special MRF |
|---|---|---|---|
| Permitted SDC | B only (Table 2.3-1) | B, C; D ≤ 40 m with +40 % forces (2.3.1.2) | B, C, D |
| Beam definition | ACI/EIT | P_u ≤ 0.10 A_g f'c (5.2.7.1) | P_u ≤ A_g f'c/10 (5.2.8.1.1) |
| Geometry limits | — | — (joint "confining" beam: b ≥ ¾ col. width, depth ≥ ¾ deepest, 5.2.7.5.3) | l_n ≥ 4d; b_w ≥ lesser(0.3h, 250 mm); projection each side ≤ lesser(col. width, ¾ col. depth) (5.2.8.1.2–.4) |
| Continuous bars | ≥ 2 top + 2 bottom full length, anchored for f_y (5.2.6(ก)) | ACI/EIT | ≥ 2 top + 2 bottom continuous (5.2.8.2.1) |
| As,min / ρmax | ACI/EIT | ACI/EIT | As ≥ 1.4 b_w d/f_y (unless 4/3 × req'd); ρ ≤ 0.025 (5.2.8.2.1) |
| +M_n at joint face | ACI/EIT | ≥ ⅓ (−M_n) (5.2.7.3.1) | ≥ ½ (−M_n) (5.2.8.2.2) |
| M_n at any section | ACI/EIT | ≥ ⅕ max face M_n (5.2.7.3.1) | ≥ ¼ max face M_n (5.2.8.2.2) |
| Lap splice location | ACI/EIT | should avoid within 2h of support face (5.2.7.3.4) | not in joints, not within 2h of face, not in plastic-hinge regions (5.2.8.2.3) |
| Lap confinement | ACI/EIT | — | hoops over full lap, s ≤ min(d/4, 100 mm) (5.2.8.2.3) |
| End zone length | — | 2h from support face (5.2.7.3.2) | 2h from face, both ends + 2h each side of other hinge sections (5.2.8.3.1) |
| First stirrup/hoop | ACI/EIT | ≤ 50 mm from face (5.2.7.3.2) | ≤ 50 mm from face (5.2.8.3.2) |
| End-zone spacing | ACI/EIT | ≤ min(d/4, 8d_b long., 24d_b stirrup, 300) (5.2.7.3.2) | ≤ min(d/4, 8d_b long., 24d_b hoop, 300) (5.2.8.3.2) — closed hoops |
| Spacing outside end zone | ACI/EIT (d/2) | ≤ d/2 (5.2.7.3.3) | ≤ d/2, stirrups with seismic hooks both ends (5.2.8.3.4) |
| Stirrup type in end zone | ACI/EIT | stirrup; 90° + 6d_b allowed; 135° or 90°+hook-clip within 2h for public/ductile buildings (5.2.7.6, Fig 5.2-8) | hoops; may be stirrup (seismic hooks) + crosstie cap, 90° crosstie hooks alternate sides or all on slab side (5.2.8.3.6); perimeter bars laterally supported per ACI (5.2.8.3.3) |
| Hook detail | ACI/EIT | 90°: 6d_b ≥ 75 mm; 135°: 6d_b ≥ 75 mm (Fig 5.2-8) | seismic hook 135°, 6d_b ≥ 75 mm (per Figs 5.2-10/11; not defined in text) |
| Shear design | ACI/EIT (no DPT beam rule) | capacity (M_n both ends + gravity) or 2E (5.2.7.2, Fig 5.2-2) | V_e from M_pr (1.25 f_y) both faces, opposite sense, + gravity; V_c = 0 in 2h zones if EQ shear large and P_u < A_g f'c/20 (5.2.8.4) |
| Exterior-joint anchorage | anchored for f_y (5.2.6(ก)) | 90° hooks at far side of column, l_dh from face (Fig 5.2-3; formula per ACI/EIT) | to far face of confined core; 90° hook inside core; l_dh ≥ max(8d_b, 150, f_y d_b/(5.3√f'c)); straight 2.5/3.25 l_dh, ×1.6 outside core (5.2.10.1.3, 5.2.10.4, Fig 5.2-12) |
| Bars through interior joint | ACI/EIT | continuous (Fig 5.2-3) | column dim. ∥ bars ≥ 20 d_b (26 d_b LW) (5.2.10.1.4) |
| Joint hoops | ACI/EIT | A_v ≥ c1 s/(3f_y) over deepest beam depth (5.2.7.4.4) | 5.2.9.4 hoops; ½ and s ≤ 150 mm only if 4 beams each ≥ ¾ col. width (5.2.10.2) |
| Coupling beams | — | — | l_n/h ≥ 4 → 5.2.8; < 4 diagonals permitted; < 2 diagonals required (threshold misprint?) (5.2.11.7) |

**Uncertain readings flagged:** (1) 5.2.8.4.2(1) lacks "½" relative to ACI and to 5.2.9.5.3; (2) 5.2.11.7.3 prints "V_u < 0.34√f'c A_cw" (probably ">"); (3) Fig 5.2-3 mid-depth line with circles is unexplained; (4) Fig 5.2-12 exact vertical order of transverse-beam dots vs main bars is approximate. All numbers otherwise verified on page images.

---

# Part B. EIT 011008-21 (design) - beam clauses


**Source:** วสท. 011008-21 (ACI 318-11 basis, SI: MPa, mm).
- PDF: `G:\My Drive\##Textbook\EIT\10104-64.pdf`.
- Page numbers are **PDF pages** (book page = PDF page − 12). This is the same convention the existing digest uses.

**Existing digest:** `SPEC_RC_DESIGN_EIT-011008-21.md` (below: "DIGEST").
- It already covers ch. 7 and ch. 12 in full. For those chapters this file cites DIGEST and only adds the beam view and newly found issues.
- Ch. 8, 10, 11 (and the beam row of ch. 9) are new here.

**Clause numbering vs ACI 318-11.** Several chapters are shifted, so always cite the EIT number:

| Topic | EIT | ACI 318-11 |
|---|---|---|
| T-beams | 8.11 | 8.12 |
| Joists | 8.12 | 8.13 |
| Shear-reinforcement spacing limits | 11.4.4 | 11.4.5 |
| Minimum shear reinforcement | 11.4.5 | 11.4.6 |
| Shear-reinforcement design | 11.4.6 | 11.4.7 |
| Flexural development, general | 12.9 | 12.10 |
| Positive-moment bars | 12.10 | 12.11 |
| Negative-moment bars | 12.11 | 12.12 |
| Web reinforcement | 12.12 | 12.13 |
| Splices, general | 12.13 | 12.14 |
| Tension splices | 12.14 | 12.15 |
| Compression splices | 12.15 | 12.16 |

Chapter 7 and 10 numbering matches ACI.

**Figures:** the standard has **no typical beam-detail figures**. I checked PDF pp. 55–121 for drawings and searched the text for "รูปที่". The only detailing figure is Fig. 13.3.8 (p.123), the minimum bar extensions for two-way slabs, which is out of scope. Every rule below is text-only. The office sheet must draw its own diagrams.

---

## CHAPTER 7 — Details of reinforcement (beam view; full text in DIGEST §7.1–7.13)

### 7.1–7.3 Hooks and bends (pp.55–56) — DIGEST lines 529–560
**Stirrup hooks (7.1.3):**
- 90° + 6db for 6–16 mm bars.
- 90° + 12db for 20–25 mm bars.
- 135° + 6db for 6–25 mm bars.

**Main-bar hooks (7.1.1–7.1.2):** 180° + 4db (≥ 60 mm), or 90° + 12db.

**Seismic hooks (7.1.4):** refers to ch. 19, which delegates to DPT 1301/1302-61.

**Bends:**
- Stirrups ≤ 16 mm: inside diameter ≥ 4db (7.2.2).
- Other bars: Table 7.1 — 6db (6–25 mm), 8db (28–36 mm), 10db (43, 57 mm).
- Bend cold (7.3.1). No field bending of bars partly embedded in concrete (7.3.2).

**Beam implications:**
- The 90° stirrup hook is allowed only where closed stirrups are not required.
- Closed stirrups with 135° hooks are **mandatory** in three cases:
  - torsion (11.5.4(ข)(1));
  - perimeter-beam integrity steel (7.13.2(ค));
  - stress reversal or torsion at supports (7.11.2, closed ties/stirrups).

### 7.5 Placing tolerances (p.56) — DIGEST lines 567–582
| Item | Tolerance |
|---|---|
| d, for d ≤ 200 mm | ±10 mm (printed "±100", misprint) |
| d, for d > 200 mm | ±13 mm |
| Cover, for d ≤ 200 mm | −10 mm |
| Cover, for d > 200 mm | −13 mm |
| Cover, absolute limit | Never more than 1/3 of the specified cover |
| Location of bends and bar ends | ±50 mm |
| Discontinuous ends of members | ±25 mm |
| Discontinuous ends of brackets and corbels | ±13 mm |

No tack welding of crossing bars without the engineer's approval (7.5.4).

### 7.6 Spacing (p.57) — DIGEST lines 584–596
- **7.6.1:** Clear spacing in a layer ≥ db and ≥ 25 mm. Also ≥ 1.5 × max aggregate size (3.3.3: aggregate ≤ 2/3 of clear spacing).
- **7.6.2:** Two or more layers — bars stacked directly above the bottom layer; clear distance between layers ≥ 25 mm.
- **7.6.4:** The limits also apply between a contact lap splice and adjacent splices or bars.
- **7.6.6 Bundles:**
  - Deformed bars only, ≤ 4 bars per bundle, enclosed by stirrups.
  - No bundling of bars > 36 mm in beams.
  - Bars cut off within the span stagger ≥ 40db.
  - For spacing and cover, a bundle counts as one bar of equivalent area.

### 7.7 Cover (pp.57–59) — DIGEST lines 598–650
- Cast-in-place beams not exposed: **40 mm to stirrups** (7.7.1(ค)(1)). Cover is measured to the outermost stirrup.
- Exposed to earth or weather: 50 mm (bars ≥ 20 mm) or 40 mm (≤ 16 mm).
- Cast against earth: 75 mm.
- Bundles: cover ≥ equivalent diameter (need not exceed 50 mm), and 75 mm against earth.
- Fire cover per the building code governs if larger (7.7.5).
- Precast beams (plant controlled): main bars db (need not exceed 40 mm); stirrups 15 mm.

### 7.10.5 Ties (pp.60–61) — used by 7.11.1 for beam compression steel; DIGEST lines 698–717
**Minimum tie size, by longitudinal bar size:**

| Longitudinal bars | Tie diameter |
|---|---|
| ≤ 12 mm | 6 mm |
| 16–20 mm | 9 mm |
| 25–28 mm | 10 mm |
| ≥ 32 mm or bundled | 12 mm |

**Spacing:** ≤ 16db(long), ≤ 48db(tie), ≤ least member dimension.

**Lateral support:** every corner bar and every alternate bar is held by a tie corner with an included angle ≤ 135°. No unsupported bar is more than 150 mm clear from a supported bar.

### 7.11 Lateral reinforcement for flexural members (p.62) — DIGEST line 719
- **7.11.1:** Beam compression reinforcement shall be enclosed by ties or stirrups that meet the **7.10.5 size and spacing limits** above. They are required throughout the length where compression steel is required.
  - Drafting consequence: in zones where the design relies on top/bottom compression steel, s ≤ 16db(main) and 48db(stirrup), and the stirrup size follows the table above.
- **7.11.2:** Framing members with stress reversal, or torsion at supports, need **closed** ties, closed stirrups or spirals around the flexural steel.
- **7.11.3:** Ways to form a closed stirrup:
  - one piece, with overlapping standard hooks around a longitudinal bar;
  - one or two pieces lap-spliced **Class B (1.3ℓd)**;
  - anchored "per 12.13".
  - [FLAG] The "12.13" reference is stale ACI numbering. In EIT, web-reinforcement anchorage is **12.12**; 12.13 is general splices.

### 7.12 Shrinkage and temperature (p.62) — DIGEST lines 724–740
Relevant to beams only through:
- T-beam flange transverse steel (8.11.5);
- joist slabs (8.12.5(ค), 8.12.6(ข)).

Ratios are 0.0025 (SR24), 0.0020 (SD30) and 0.0018 (SD40), always ≥ 0.0014. Spacing ≤ 5h and ≤ 400 mm (ACI allows 450 mm).

### 7.13 Structural integrity (p.63) — full detail
This clause is re-read here from the text (p.63). It is consistent with DIGEST lines 742–754.
- **7.13.1:** Members shall be effectively tied together through reinforcement and connection detailing.
- **7.13.2 Cast-in-place (minimum requirements):**
  - **(ก) Joists:**
    - At least **one bottom bar** is continuous, or spliced by a Class B tension lap or a mechanical/welded splice per 12.14.4.
    - At non-continuous supports the bar ends in a **standard hook**.
  - **(ข) Perimeter beams (คานปริมณฑล)** need continuous reinforcement of at least:
    - (1) **Top:** ≥ **1/6** of the negative-moment tension steel required at the support, and **≥ 2 bars**.
    - (2) **Bottom:** ≥ **1/4** of the positive-moment tension steel required at midspan, and **≥ 2 bars**.
  - **(ค) Enclosure of that continuous steel,** by either:
    - **U-stirrups with hooks ≥ 135°** around the top bars; or
    - **one-piece closed stirrups with hooks ≥ 135°** around a top bar.
    - These stirrups **need not be continued through the column**.
  - **(ง) Splice locations** where continuity needs a splice:
    - **top bars at or near midspan**;
    - **bottom bars at or near the support**.
    - Splice type: **Class B tension lap**, or a mechanical/welded splice per 12.14.4. That clause requires a full mechanical or full welded splice (≥ 1.25fy, 12.13.3(ข)/(ง)) where As provided < 2 × required.
  - **(จ) Beams other than perimeter beams,** when the transverse reinforcement is not provided:
    - ≥ **1/4** of the midspan positive-moment steel, and **≥ 2 bars**, shall be continuous, or spliced **over or near the support** (Class B, or mechanical/welded per 12.14.4).
    - At non-continuous supports these bars end in a **standard hook**.
    - [FLAG] The text says "transverse reinforcement as defined in 7.13.2(ง)"; it logically means (ค). DIGEST already notes this.
  - **(ฉ) Two-way slabs:** see 13.3.8(จ).
- **7.13.3 Precast:** tension ties in the transverse, longitudinal and vertical directions and around the perimeter, per 16.5.
- [NOTE] (ข) does not state an end-anchorage rule for perimeter-beam bars at non-continuous (end) supports; (ก) and (จ) require hooks. Recommended office practice: hook the continuous top and bottom perimeter bars into end columns, standard hook, developed from the column face.

---

## CHAPTER 8 — Analysis and design, general considerations (beam items)

### 8.3.3 Approximate moments and shears (p.66) — same as ACI 318-11 8.3.3
**Conditions for use:**
- (ก) ≥ 2 spans.
- (ข) Spans roughly equal: the longer of two adjacent spans ≤ 1.2 × the shorter.
- (ค) Uniformly distributed load.
- (ง) Live load ≤ 3 × dead load.
- (จ) Prismatic members.

**Span to use:** ℓn = clear span. For negative moment, use the average of the adjacent clear spans.

**Positive moment:**

| Location | Moment |
|---|---|
| End span, discontinuous end unrestrained | wuℓn²/11 |
| End span, discontinuous end integral with support | wuℓn²/14 |
| Interior span | wuℓn²/16 |

**Negative moment:**

| Location | Moment |
|---|---|
| Exterior face of first interior support, 2 spans | wuℓn²/9 |
| Exterior face of first interior support, > 2 spans | wuℓn²/10 |
| Other interior faces | wuℓn²/11 |
| All supports, slabs with span ≤ 3.0 m | wuℓn²/12 |
| All supports, beams where Σcolumn stiffness / beam stiffness > 8 | wuℓn²/12 |
| Interior face of exterior support (integral), support is a spandrel beam | wuℓn²/24 |
| Interior face of exterior support (integral), support is a column | wuℓn²/16 |

**Shear:** 1.15wuℓn/2 at the face of the first interior support; wuℓn/2 at other supports.

[NOTE] **No bar-cutoff rules are given** with the coefficients. EIT, like ACI 318-11, has no "standard cutoff points" clause. Cutoffs must come from 12.9–12.11. For coefficient-designed beams, the office's typical cutoff lengths (e.g. ℓn/4, ℓn/3 for top bars) are office practice. Check them against 12.11.3: ≥ 1/3 of the top steel extends past the point of inflection by max(d, 12db, ℓn/16).

Also on these pages:
- **8.4 (pp.66–67):** redistribution of negative moment ≤ 1000εt %, max 20 %, allowed only if εt ≥ 0.0075.
- **8.8.3 (p.68):** beams integral with supports may be designed for the moment at the support face.

### 8.11 T-beam construction (= ACI 8.12) (pp.69–70)
- **8.11.1:** Flange and web are cast monolithically or effectively bonded.
- **8.11.2 Interior T-beam:**
  - Effective flange width ≤ **span/4**.
  - Each overhang ≤ **8hf** and ≤ **½ the clear distance to the next web**.
- **8.11.3 Slab on one side only (L/edge beam):** overhang ≤ **span/12**, ≤ **6hf**, ≤ **½ the clear distance to the next web**.
- **8.11.4 Isolated T-beam** (flange added for compression area): hf ≥ **bw/2**; effective flange width ≤ **4bw**.
- **8.11.5 Flange transverse reinforcement:** applies where the slab's primary flexural reinforcement is **parallel to the beam** (not joist construction). Transverse bars go in the **top of the slab**.
  - (ก) Design the overhang as a cantilever under factored load:
    - isolated beams: the full overhang width;
    - other T-beams: only the effective overhang.
  - (ข) Spacing ≤ **5 × slab thickness** and ≤ **400 mm**.
  - [FLAG] ACI 318-11 8.12.5.2 allows 450 mm. EIT uses 400 mm, consistent with its 7.12.2(ข) limit.

### 8.12 Joist construction (= ACI 8.13) (p.70) — brief
- **8.12.1:** Monolithic slab plus ribs at regular spacing, in one or two directions.
- **8.12.2:** Rib width ≥ **100 mm**; rib depth ≤ **3.5 × minimum rib width**.
- **8.12.3:** Clear spacing between ribs ≤ **750 mm**.
- **8.12.4:** Joist systems that do not meet 8.12.1–8.12.3 are designed as slabs and beams.
- **8.12.5 Permanent fillers** with strength ≥ f'c:
  - (ก) Vertical shells of the fillers in contact with ribs may count for shear and negative moment.
  - (ข) Slab ≥ **ℓclear/12** and ≥ **40 mm**.
  - (ค) One-way joists: slab steel perpendicular to ribs per 7.12.
- **8.12.6 Removable forms or non-conforming fillers:**
  - (ก) Slab ≥ ℓclear/12 and ≥ **50 mm**.
  - (ข) Slab steel perpendicular to ribs designed for flexure, including concentrated loads, and ≥ 7.12.
- **8.12.7:** Embedded conduits (per 6.3) need ≥ **25 mm** concrete cover and must not significantly impair strength.
- **8.12.8:** Vc for joists may be taken **10 % higher** than ch. 11 values.
- Joists are exempt from Av,min (11.4.5(ก)(3)).
- Integrity: ≥ 1 continuous bottom bar (7.13.2(ก)).
- Joist stirrups ≤ 12 mm need a standard hook (12.12.2(จ)).

### (ch. 9 items useful on a beam sheet)
- **9.4 (p.73):** Design fy and fyt ≤ **560 MPa**. [FLAG] ACI 318-11 9.4 uses 550 MPa (80 ksi).
- **9.5.2 Table 9.1 (p.73):** Minimum h for beams / one-way ribbed slabs when deflection is not computed:

| Case | Minimum h |
|---|---|
| Simply supported | ℓ/16 |
| One end continuous | ℓ/18.5 |
| Both ends continuous | ℓ/21 |
| Cantilever | ℓ/8 |

  - Table values are for normalweight concrete and SD40.
  - For fy ≠ 400 MPa, multiply by (0.4 + fy/700).
  - For lightweight concrete (wc 1500–2000 kg/m³), multiply by (1.65 − 0.0003wc) ≥ 1.09.

---

## CHAPTER 10 — Flexure and axial loads (beam items)

### 10.3.6 (p.80)
For nonprestressed flexural members, and members with Pu < 0.1f'cAg, εt at nominal strength ≥ **0.004**.
- For SD40 the compression-controlled strain limit may be taken as 0.002 (10.3.3).
- Tension-controlled means εt ≥ 0.005 (10.3.4).

### 10.4 Lateral support (p.81)
- **10.4.1:** Lateral supports of a beam spaced ≤ **50b**, where b = least width of the compression flange or face.
- **10.4.2:** Consider eccentricity of lateral load.

### 10.5 Minimum flexural reinforcement (p.81) — same as ACI 318-11 10.5
- **10.5.1:** At every section where analysis needs tension steel:
  **As,min = (0.25√f'c / fy) bw d ≥ (1.4 / fy) bw d**  (10-3)
  - (calc.) 1.4/fy governs for f'c ≤ 31.4 MPa. That gives As,min = 0.0047bwd for SD30 and 0.0035bwd for SD40.
- **10.5.2:** Statically determinate members with the **flange in tension**: in Eq. 10-3, replace bw by the smaller of **2bw** and the flange width.
- **10.5.3:** Exemption from 10.5.1 and 10.5.2.
  - As printed: 10.5.1 and 10.5.2 need not apply if As at every section is "not less than **1/3 of** the amount required by analysis".
  - **[FLAG — misprint]** ACI 318-11 says "at least **one-third greater than**" required, i.e. **As,prov ≥ 4/3 As,req**. The literal EIT wording would make the exemption meaningless. Adopt 4/3.
- **10.5.4:** Uniform-thickness slabs and footings: As,min in the span direction per 7.12.2(ก). Maximum spacing ≤ **3h** and ≤ **450 mm**.

### 10.6 Distribution of flexural reinforcement / crack control, beams and one-way slabs (pp.81–82)
- **10.6.1:** Scope — crack control for beams and one-way slabs.
- **10.6.2:** Two-way slabs: see 13.3.
- **10.6.3:** Tension steel is distributed over the zone of maximum tension, per 10.6.4.
- **10.6.4:** Spacing s of the bars nearest the tension face:
  **s ≤ 380(280/fs) − 2.5cc**  (10-4), **and ≤ 300(280/fs)**
  - cc = least distance from the **surface of the reinforcement** to the tension face.
  - If only one bar is nearest the tension face, s = the width of that face.
  - fs = service stress from unfactored moment, or take **fs = (2/3)fy**.
  - (calc., fs = 2/3fy):
    - SD40: fs = 267 MPa, s ≤ 399 − 2.5cc ≤ 315. With cc = 50 mm (40 cover + 10 stirrup), **s ≤ 274 mm**.
    - SD30: fs = 200 MPa, s ≤ 532 − 2.5cc ≤ 420. With cc = 50 mm, s ≤ 407 mm.
- **10.6.5:** 10.6.4 is not sufficient for severe exposure or watertight design. These need special investigation.
- **10.6.6:** T-beam flange in tension:
  - Distribute the tension steel over the effective flange width (8.11) or **span/10**, whichever is smaller.
  - If the effective width exceeds span/10, add some longitudinal steel in the outer flange.
- **10.6.7 Skin (side-face) reinforcement:**
  - Threshold: web/joist depth **> 400 mm** (as printed; verified on page image eb_82.png).
  - Place longitudinal skin bars uniformly along **both side faces** within **h/2 from the tension face**.
  - Spacing s per 10.6.4, with cc = least distance from the skin-bar surface to the **side face**.
  - Skin bars may be counted in strength only with a strain-compatibility analysis.
  - No minimum skin-bar area is given; nor does ACI 318-11 give one.
  - **[FLAG]** ACI 318-11 10.6.7 uses h > **900 mm (36 in)**. EIT's 400 mm is either a deliberate tightening or a misprint. As printed, it makes skin bars mandatory for most floor beams deeper than 400 mm, e.g. 2 × DB12 each face for h = 500–700 mm. Confirm the intent before adopting it as a typical note. Conservative adoption: follow it.

### 10.7 Deep beams (pp.82–83)
- **10.7.1:** A deep beam is loaded on one face and supported on the opposite face, so that compression struts can form, **and** either:
  - (ก) **ℓn ≤ 4h**; or
  - (ข) regions with concentrated loads within **2h** of the support face.
  - Design for non-linear strain distribution, or by ch. 20 (strut-and-tie). See 11.7.1 and 12.9.6.
- **10.7.2:** Shear per 11.7.
- **10.7.3:** As,min per 10.5.
- Deep-beam anchorage: see 12.10.4 and 12.11.4 in ch. 12 below.

---

## CHAPTER 11 — Shear and torsion (beam items)

### 11.1 General (p.91)
- φVn ≥ Vu, with Vn = Vc + Vs (11-1, 11-2).
- Web openings shall be considered in Vn (11.1.1(ก)).
- **11.1.2:** √f'c ≤ 8.3 MPa. Higher values are allowed for Vc in RC beams and joists that have minimum web reinforcement.
  - [FLAG] The cross-references "11.4.6(ค), 11.4.6(ง), 11.5.5(ข)" are stale ACI numbering. The intended clauses are 11.4.5(ค) and 11.5.5(ข).
- **11.1.3:** Sections closer than **d** to the support face may be designed for Vu at d when all of these hold:
  - the reaction induces compression in the end region;
  - loads are applied at or near the top;
  - there is no concentrated load within that distance.
- Basic Vc = 0.17λ√f'c bw d (Eq. 11-3; see DIGEST Appendix table, line 1061).

### 11.4.1–11.4.3 Types, yield strength, extent (p.93)
- **11.4.1(ก) Types of shear reinforcement:**
  - stirrups perpendicular to the axis;
  - welded wire with wires perpendicular to the axis;
  - spirals, circular ties or hoops.
- **11.4.1(ข) Nonprestressed members may also use:**
  - stirrups at ≥ 45° to the longitudinal tension steel;
  - bent-up bars at ≥ **30°**;
  - combinations of stirrups and bent bars.
- **11.4.2:** Design fyt ≤ **420 MPa**, or ≤ 550 MPa for welded deformed wire.
- **11.4.3:** Stirrups and other shear bars extend to a distance **d from the extreme compression fiber**. Both ends are anchored to develop fyt, "per 12.13".
  - [FLAG] "12.13" should read EIT **12.12**.

### 11.4.4 Spacing limits for shear reinforcement (= ACI 11.4.5) (pp.93–94)
- **(ก)** Stirrups perpendicular to the axis: s ≤ **d/2** (nonprestressed) and ≤ **600 mm** (printed "60 ซม.").
- **(ข)** Inclined stirrups and bent bars: every 45° line drawn from mid-depth d/2 toward the reaction, down to the tension steel, must cross at least one line of shear reinforcement.
- **(ค)** Where **Vs > 0.33√f'c bw d**, halve the maximum spacings: **s ≤ d/4 and ≤ 300 mm**.
  - [FLAG] The text cites "11.5.4(ก) and 11.5.4(ข)"; it must mean 11.4.4(ก) and (ข).
- Upper limit on Vs: **Vs ≤ 0.66√f'c bw d** (11.4.6(ฌ), p.95). Otherwise enlarge the section.

### 11.4.5 Minimum shear reinforcement (= ACI 11.4.6) (p.94)
**(ก)** Av,min is required in all RC flexural members wherever **Vu > 0.5φVc**, except:
1. Slabs and footings.
2. Hollow-core units with total depth (excluding topping) ≤ **320 mm**; and hollow-core units with Vu ≤ 0.5φVcw.
3. Joist construction per 8.12.
4. **Beams with h ≤ 250 mm** (printed "25 ซม.").
5. Floor-plus-beam total depth ≤ **2.5 × flange thickness and ≤ 0.5 × web width**.
   - [FLAG] ACI 318-11 11.4.6.1(d) reads: beams integral with slabs, h ≤ 600 mm **and** h ≤ the **larger of** 2.5tf or 0.5bw. EIT drops the 600 mm cap and turns "larger of" into "and". As printed, EIT is more restrictive.
6. Steel-fiber-reinforced normalweight beams, h ≤ **600 mm** and Vu ≤ φ0.17√f'c bw d. The concrete strength is printed as f'c "**exceeding 420 MPa**".
   - [FLAG — misprint] ACI requires f'c **not exceeding 40 MPa**. Verified on page image eb_94.png.

**(ข)** The Av,min requirement may be waived if tests show Mn and Vn are adequate without it. The tests must consider differential settlement, creep, shrinkage and temperature.

**(ค)** Where Av,min is required, or where 11.5.1 lets torsion be neglected:
**Av,min = 0.062√f'c bw s / fyt ≥ 0.35 bw s / fyt**  (11-9)
- (calc.) 0.35 governs for f'c ≤ 31.9 MPa.
- Example: bw = 250, s = 200, SR24 (fyt = 240) gives Av,min = 73 mm². A 2-leg RB9 (127 mm²) is OK; a 2-leg RB6 (56.5 mm²) is **not**.

### 11.4.6 Design of shear reinforcement (= ACI 11.4.7) (pp.94–95)
- **(ก)** Where Vu > φVc, provide Vs per (ข)–(ซ).
- **(ข)** Perpendicular stirrups: **Vs = Av fyt d / s**  (11-10). Av = all legs within s.
- **(ค)** Circular ties, hoops or spirals in round members: Av = 2 × bar area; d per 11.2.3 (0.8D).
- **(ง)** Inclined stirrups: **Vs = Av fyt (sin α + cos α) d / s**  (11-11).
- **(จ)** A single bent bar, or a group bent up at the same distance from the support: **Vs = Av fy sin α ≤ 0.25√f'c bw d**  (11-12).
- **(ฉ)** Series of bent bars at different distances: use 11-11.
- **(ช)** Only the **centre 3/4 of the inclined portion** of a bent bar is effective.
- **(ซ)** Several types in the same zone: sum their Vs.
- **(ฌ)** **Vs ≤ 0.66√f'c bw d.**

### 11.5 Torsion (pp.95–99) — detailing-relevant parts
- **11.5.1 Threshold:** torsion may be neglected if **Tu < φ0.083λ√f'c (Acp²/pcp)**  (11-13).
  - With axial force, see Eq. 11-14.
  - For monolithic slabs, the overhang width in Acp and pcp is per 13.2.4. Ignore the flanges if they reduce Acp²/pcp.
- **11.5.2 Design torque:**
  - (ก) Equilibrium torsion: design for full Tu.
  - (ข) Compatibility torsion in indeterminate structures: Tu may be reduced to the cracking torque φ0.33λ√f'c(Acp²/pcp) (11-15).
- **11.5.3 Strength:**
  - (ก) Section limits: Eq. 11-17 (solid) and 11-18 (hollow), with the 0.66√f'c term.
  - (ง) **fy, fyt ≤ 420 MPa** for torsion steel.
  - (ฉ) **Tn = (2Ao At fyt / s) cot θ**  (11-20), with Ao = 0.85Aoh and θ = 45° for nonprestressed members.
  - (ช) **Aℓ = (At/s) ph (fyt/fy) cot²θ**  (11-21).
  - (ซ) Torsion steel is **added** to the steel for shear, flexure and axial load. Spacing and placement follow the **most restrictive** requirement.
  - (ฌ) In the flexural compression zone, Aℓ may be reduced by Mu/(0.9d fy), but not below 11.5.5(ค) or 11.5.6(ข).
- **11.5.4 Details:**
  - (ก) Torsion steel = longitudinal bars plus one or more of:
    - (1) **closed stirrups or closed ties** perpendicular to the axis;
    - (2) closed cages of welded wire;
    - (3) spirals (nonprestressed beams).
  - (ข) Transverse torsion steel is anchored by one of:
    - (1) a **135° standard hook** per 7.1.3(ค), or a seismic hook per 7.1.4, **around a longitudinal bar**; or
    - (2) per 12.12.2(ก)/(ข)/(ค), only where the surrounding concrete is restrained against spalling by a flange, slab or similar member.
    - Drafting consequence: spandrel/edge beams with slab on one side may use a 90° hook on the slab side only. Otherwise use 135° hooks both ends.
  - (ค) Longitudinal torsion bars shall be **anchored at both ends**.
  - (ง) Hollow sections: distance from the centreline of the transverse torsion steel to the inside wall face ≥ **0.5Aoh/ph**.
- **11.5.5 Minimum torsion reinforcement** (wherever Tu exceeds the 11.5.1 threshold):
  - (ข) **(Av + 2At) ≥ 0.062√f'c bw s / fyt ≥ 0.35 bw s / fyt**  (11-22).
  - (ค) **Aℓ,min = 0.42√f'c Acp / fy − (At/s) ph (fyt/fy)**  (11-23), with **At/s ≥ 0.175bw/fyt**.
- **11.5.6 Spacing of torsion steel:**
  - (ก) Closed stirrups: **s ≤ ph/8 and ≤ 300 mm**.
  - (ข) Longitudinal torsion bars:
    - distributed around the perimeter of the closed stirrups at **≤ 300 mm** spacing;
    - placed **inside** the stirrups;
    - **at least one bar in each stirrup corner**;
    - bar diameter ≥ **s/24** (= 0.042s, s = stirrup spacing) and **≥ 10 mm**.
  - (ค) Torsion steel extends **≥ (bt + d)** beyond the point theoretically required.
- **11.5.7:** Alternative design is allowed for h/bt ≥ 3 if backed by analysis and tests. 11.5.4 and 11.5.6 still apply.

### 11.7 Deep beams (pp.100–101)
- **11.7.1 Scope:** ℓn ≤ 4h, or regions with concentrated loads within 2h of the support. Loaded on one face and supported on the other, so struts can form. See 12.9.6.
- **11.7.2:** Design by non-linear analysis or ch. 20. Minimum distributed steel per 11.7.4 in all cases.
- **11.7.3:** **Vu ≤ φ0.83√f'c bw d.**
- **11.7.4:** Distributed reinforcement is required on **both faces**:
  - (ก) Vertical (perpendicular to axis): **Av ≥ 0.0025bw s**, with **s ≤ d/5 and ≤ 300 mm**.
  - (ข) Horizontal (parallel to axis): **Avh ≥ 0.0025bw s2**, with **s2 ≤ d/5 and ≤ 300 mm**.
  - **[FLAG]** ACI 318-11 11.7.4.2 requires **0.0015bw s2**. EIT prints 0.0025 (verified on page image eb_101.png). As printed it is conservative; possibly a misprint.
- **11.7.5:** Strut-and-tie reinforcement per ch. 20 may replace 11.7.4.
  - [FLAG] The text self-cites "11.7.4 and 11.7.5"; it means 11.7.4(ก) and (ข).
- Deep-beam anchorage: see 12.10.4 and 12.11.4 in ch. 12 below.

(11.8 brackets/corbels and 11.9 walls: skipped as instructed. 11.11 slabs: out of scope.)

---

## CHAPTER 12 — Development and splices (beam view; full text in DIGEST lines 769–961)

EIT numbers are one lower than ACI from 12.9 on. PDF pages: 12.9 on p.114; 12.10–12.11.3 on p.115; 12.11.4–12.12.4 on p.116; 12.12.5–12.14.1 on p.117; 12.14.2–12.15 on p.118.

### Development lengths (pp.109–112) — see DIGEST 12.2–12.5
- **ℓd simplified (12.2.2):** fy ψt ψe/(2.1λ√f'c) db for ≤ 20 mm bars, or /(1.7λ√f'c) db for ≥ 22 mm bars, when:
  - cover ≥ db, clear spacing ≥ db, and minimum stirrups are present; **or**
  - cover ≥ db and clear spacing ≥ 2db.
- Other cases: /1.4 and /1.1. Always ≥ 300 mm.
- **ψt = 1.3 for top bars** (more than 300 mm of fresh concrete cast below) — applies to most beam top bars when h > ~350 mm.
- **ℓdh = fy ψe/(4.2λ√f'c) db ≥ max(8db, 150 mm)** (12.5.2).
  - × 0.7 for cover (side ≥ 65 mm; 90° tail cover ≥ 50 mm).
  - × 0.8 for ties at ≤ 3db.
  - 12.5.4: at discontinuous beam ends where both side and top/bottom cover over the hook are < 65 mm, the hook **must** be enclosed by ties at ≤ 3db, the first within 2db of the bend. The 0.8 factor is then not used. This is typical for beam end hooks into exterior columns.

### 12.9 Development of flexural reinforcement — general (= ACI 12.10) (p.114)
- **12.9.1:** Tension steel may be developed by bending across the web and anchoring, or by making it continuous with the steel on the opposite face.
- **12.9.2:** Critical sections are:
  - points of maximum stress;
  - points within the span where adjacent bars terminate or are bent (see 12.10.3).
- **12.9.3:** Bars extend beyond the point where no longer needed for flexure by **max(d, 12db)**. Exceptions: supports of simple spans and free ends of cantilevers.
- **12.9.4:** Continuing bars have embedment ≥ **ℓd** beyond the point where bent or terminated bars are no longer needed.
- **12.9.5:** No cutoff in a **tension zone** unless one of:
  - (ก) Vu ≤ (2/3)φVn at the cutoff;
  - (ข) extra stirrups beyond those for shear and torsion, over **3/4d** from the cutoff, with area ≥ 0.41bw s/fyt and s ≤ d/(8βb). The text prints "not exceeding"; the ACI sense "not less than" is adopted, per DIGEST;
  - (ค) bars ≤ 36 mm: continuing steel = **2 ×** that required at the cutoff, **and** Vu ≤ (3/4)φVn.
- **12.9.6:** Special anchorage where steel stress is not proportional to moment: sloped, stepped or tapered footings, brackets, **deep flexural members**, and tension steel not parallel to the compression face.

### 12.10 Positive-moment reinforcement (= ACI 12.11) (p.115)
- **12.10.1:** At least **1/3** (simple members) or **1/4** (continuous members) of the positive steel extends along the same face into the support. In **beams**, at least **150 mm** into the support.
- **12.10.2:** If the beam is part of the primary lateral-load-resisting system, those bars are anchored to develop **fy at the face of the support**. This means hooked or straight ℓd past the face.
- **12.10.3:** At simple supports and points of inflection, limit the bar size so that **ℓd ≤ Mn/Vu + ℓa**  (12-6).
  - At a support, ℓa = embedment past the support centreline.
  - At a point of inflection, ℓa ≤ max(d, 12db).
  - Mn/Vu may be increased by 30 % where the bar ends are confined by a compressive reaction.
  - Not required for bars ending past the centreline of a simple support in a standard hook or equivalent mechanical anchorage.
  - [FLAG] The text says "need not satisfy Eq. (**12-5**)"; it must mean (12-6). The definition list prints Mu for Mn (already in DIGEST).
- **12.10.4:** Deep beams:
  - At simple supports, develop fy at the support face (or use 20.4.3 if designed by strut-and-tie).
  - At interior supports, positive steel is continuous or spliced with the adjacent span.

### 12.11 Negative-moment reinforcement (= ACI 12.12) (pp.115–116)
- **12.11.1:** Anchor in or through the supporting member by embedment, hooks or mechanical anchorage. Applies to continuous, restrained and cantilever members, and any rigid-frame member.
- **12.11.2:** Embedment into the span per 12.1 and 12.9.3.
- **12.11.3:** At least **1/3** of the total negative steel at a support extends beyond the **point of inflection** by at least **max(d, 12db, ℓn/16)**. The printed "อย่างน้อยในสาม" has a dropped "หนึ่ง".
- **12.11.4:** Deep beams: negative steel continuous with the adjacent spans at interior supports.

### 12.12 Web reinforcement anchorage (= ACI 12.13) (pp.116–117) — DIGEST lines 887–898
- **12.12.1:** Stirrups run as close to the compression and tension faces as cover and other bars permit.
- **12.12.2 End anchorage:**
  - (ก) Standard hook around a longitudinal bar is enough for:
    - bars ≤ 16 mm and deformed wire ≤ 16 mm;
    - 20/22/25 mm bars with fyt ≤ 280 MPa.
    - Covers all RB6/RB9 (SR24) and DB10–DB16 stirrups.
  - (ข) 20/22/25 mm stirrups with fyt > 280 MPa: stirrup hook **plus** embedment from mid-depth to the outside end of the hook ≥ fyt db/(5.9λ√f'c).
  - (ค), (ง) Welded wire U-stirrups and single-leg stirrups: see DIGEST.
  - (จ) Joist bars or wire ≤ 12 mm: standard hook.
    - [FLAG] The text cites "8.11" for joists; EIT joists are **8.12**.
- **12.12.3:** Each bend in the continuous part of a U-stirrup encloses a longitudinal bar.
- **12.12.4:** Bent-up bars:
  - into a tension zone: continuous with the longitudinal steel;
  - into a compression zone: anchored beyond d/2 by ℓd.
- **12.12.5:** U-stirrup pairs or ties forming a closed unit are properly spliced with a **1.3ℓd** lap.
  - In members ≥ **500 mm** deep with Ab fyt ≤ **40 kN per leg**, legs extending the full available depth are adequate.
  - ACI uses 450 mm.

### 12.13–12.15 Splices (= ACI 12.14–12.16) (pp.117–118) — DIGEST lines 900–940
- **No laps of bars > 36 mm** (12.13.2(ก)).
- Bundles: individual-bar laps +20 % / +33 %, not overlapping; whole-bundle laps prohibited (12.13.2(ข)).
- **Non-contact laps** in flexural members: transverse spacing ≤ min(lap/5, 150 mm) (12.13.2(ค)).
- **Full mechanical or full welded splice ≥ 1.25fy** (12.13.3).
- **Tension laps (12.14.1):** Class A = 1.0ℓd, Class B = 1.3ℓd, both ≥ 300 mm. ℓd is taken without the As,req/As,prov reduction.
  - **Class B is the default.**
  - Class A only if As,prov ≥ 2As,req over the whole lap **and** ≤ 50 % of the bars are spliced within the lap length (12.14.2).
- Different bar sizes: the larger of ℓd(larger bar) and the lap of the smaller bar (12.14.3).
- Where As,prov < 2As,req, mechanical/welded splices must be full splices (12.14.4).
- Partial-strength splices: only ≤ 16 mm bars, staggered ≥ 600 mm (12.14.5).
- **Splice location:** EIT (like ACI 318-11) has **no general rule** for where beam laps go, other than:
  - 7.13.2(ง): integrity steel — top at or near midspan, bottom at or near the support;
  - the Class A/B conditions, which in effect push laps to low-stress zones;
  - 12.13.1: splices only where shown on the drawings or approved by the engineer. The typical sheet should therefore **show lap zones explicitly**.
- **Compression laps (12.15.1):** 0.071fy db (fy ≤ 420 MPa), ≥ 300 mm; +1/3 if f'c < 21 MPa.

---

## Consolidated list of new flags (not already in DIGEST)

| # | Clause (PDF p.) | As printed | ACI 318-11 / adopted reading |
|---|---|---|---|
| 1 | 10.6.7 (p.82) | Skin steel when web depth > **400 mm** | ACI: h > **900 mm**. Deliberate tightening or misprint; confirm. Conservative: use 400 mm |
| 2 | 11.4.4(ค) (p.94) | Halve spacing of "11.5.4(ก),(ข)" | 11.4.4(ก),(ข), i.e. d/4 and 300 mm |
| 3 | 11.4.5(ก)(6) (p.94) | Fiber concrete f'c "**exceeding 420 MPa**" | f'c **≤ 40 MPa** |
| 4 | 11.4.5(ก)(5) (p.94) | ≤ 2.5tf **and** ≤ 0.5bw; no 600 mm cap | h ≤ 600 mm and ≤ the **larger of** 2.5tf, 0.5bw |
| 5 | 11.7.4(ข) (p.101) | Avh ≥ **0.0025**bw s2 | ACI **0.0015**bw s2. EIT is conservative; possible misprint |
| 6 | 11.7.5 (p.101) | Refers to "11.7.4 and 11.7.5" | 11.7.4(ก),(ข) |
| 7 | 11.4.3 (p.93), 7.11.3 (p.62) | Stirrup anchorage "per 12.13" | EIT **12.12** (web reinforcement); 12.13 is splices |
| 8 | 11.1.2 (p.91) | Refers to 11.4.6(ค),(ง) | 11.4.5(ค) (stale ACI numbering) |
| 9 | 12.10.3 (p.115) | "need not satisfy Eq. (12-5)" | Eq. (12-6) |
| 10 | 12.12.2(จ) (p.116) | Joists "per 8.11" | 8.12 (8.11 is T-beams) |
| 11 | 8.11.5(ข) (p.70) | Flange transverse bars ≤ 5h, **400 mm** | ACI 450 mm. Deliberate, matches EIT 7.12 |
| 12 | 9.4 (p.73) | fy, fyt ≤ **560 MPa** | ACI 550 MPa |
| 14 | 10.5.3 (p.81) | Exempt if As ≥ "1/3 of" required | ≥ 4/3 of required ("one-third greater") |
| 13 | 12.11.3 (p.115) | "อย่างน้อยในสาม" | "อย่างน้อยหนึ่งในสาม" (1/3) |

DIGEST flags that still apply to beams:
- 7.5.2 d tolerance "±100" should be ±10 mm.
- 7.13.2(จ) cross-reference (ง) should be (ค).
- 12.9.5(ข) "not exceed" should be "not less than".
- 12.12.5 uses 500 mm vs ACI 450 mm.

---

## Beam detailing quick table

| Item | Rule | Clause (PDF p.) |
|---|---|---|
| Cover, interior beam | 40 mm to stirrup | 7.7.1(ค)(1) (p.58) |
| Cover, exposed / against earth | 50 (≥ 20 mm bars) or 40 (≤ 16 mm); 75 cast against earth | 7.7.1(ก),(ข) (p.57–58) |
| Cover tolerance | −10 (d ≤ 200) / −13 (d > 200); ≤ 1/3 of cover | 7.5.2(ก) (p.56) |
| Bar-end / bend location tolerance | ±50; ±25 at discontinuous ends | 7.5.2(ข) (p.56) |
| Clear spacing in a layer | ≥ db, ≥ 25 mm, ≥ 1.5 × aggregate | 7.6.1, 3.3.3 (p.57) |
| Layers | Bars directly above each other; clear ≥ 25 mm | 7.6.2 (p.57) |
| Bundles | ≤ 4 deformed bars; none > 36 mm in beams; cutoffs staggered 40db; inside stirrups | 7.6.6 (p.57) |
| Stirrup hook | 90° + 6db (6–16 mm), 90° + 12db (20–25 mm), 135° + 6db (6–25 mm) | 7.1.3 (p.55) |
| Stirrup bend diameter | ≥ 4db (≤ 16 mm); else Table 7.1 (6db / 8db / 10db) | 7.2.2, T7.1 (p.55) |
| Main-bar hook | 180° + 4db ≥ 60 mm; 90° + 12db | 7.1.1–7.1.2 (p.55) |
| Compression steel ties | Size per 7.10.5 table; s ≤ 16db, 48dt, least dimension, over the zone where compression steel is needed | 7.11.1, 7.10.5 (p.60–62) |
| Closed stirrups | Required for stress reversal or torsion at supports; hooks overlapped, or Class B (1.3ℓd) lap | 7.11.2–7.11.3 (p.62) |
| Perimeter beam, integrity steel | Top ≥ 1/6 As(−) at support, ≥ 2 bars; bottom ≥ 1/4 As(+) at midspan, ≥ 2 bars; continuous | 7.13.2(ข) (p.63) |
| Perimeter beam stirrups | U-stirrup with ≥ 135° hooks round top bars, or one-piece closed stirrup with 135° hooks; need not pass through column | 7.13.2(ค) (p.63) |
| Integrity splice location | Top at or near midspan; bottom at or near support; Class B or full mechanical/welded | 7.13.2(ง) (p.63) |
| Other beams without closed stirrups | ≥ 1/4 As(+), ≥ 2 bars, continuous or Class B lapped near support; hooked at discontinuous end | 7.13.2(จ) (p.63) |
| T-beam flange width | ≤ span/4; overhang ≤ 8hf, ≤ ½ clear to next web | 8.11.2 (p.69) |
| L-beam flange | Overhang ≤ span/12, 6hf, ½ clear to next web | 8.11.3 (p.69) |
| Isolated T-beam | hf ≥ bw/2; b ≤ 4bw | 8.11.4 (p.69) |
| Flange transverse top steel | Design overhang as cantilever; s ≤ 5hf, ≤ 400 mm | 8.11.5 (p.69–70) |
| Joists | Rib ≥ 100 wide, depth ≤ 3.5 × width; clear ≤ 750; slab ≥ ℓ/12 and ≥ 40 (fillers) or 50; Vc +10 % | 8.12 (p.70) |
| Min. h without deflection check | ℓ/16 simple, ℓ/18.5 one end continuous, ℓ/21 both, ℓ/8 cantilever; × (0.4 + fy/700) | 9.5.2, T9.1 (p.73) |
| Lateral bracing | ≤ 50b of compression flange | 10.4.1 (p.81) |
| As,min | 0.25√f'c bw d/fy ≥ 1.4bw d/fy; flange in tension (determinate): bw → min(2bw, bf); waived if As ≥ 4/3 As,req | 10.5.1–10.5.3 (p.81) |
| Tension-bar max spacing | s ≤ 380(280/fs) − 2.5cc ≤ 300(280/fs); fs = 2/3fy. SD40, cc = 50: ≈ 275 mm | 10.6.4 (p.82) |
| T-flange in tension | Spread bars over min(beff, span/10); extra bars outside | 10.6.6 (p.82) |
| Skin reinforcement | Web depth > 400 mm (as printed; ACI 900): both faces within h/2 of tension face, s per 10.6.4 with cc to side face | 10.6.7 (p.82) |
| Deep beam definition | ℓn ≤ 4h, or concentrated load within 2h of support | 10.7.1, 11.7.1 (p.82, 100) |
| Deep beam web steel | Av ≥ 0.0025bw s, s ≤ d/5, ≤ 300; Avh ≥ 0.0025bw s2 (ACI 0.0015), s2 ≤ d/5, ≤ 300; both faces; Vu ≤ φ0.83√f'c bw d | 11.7.3–11.7.4 (p.100–101) |
| Stirrup yield for design | fyt ≤ 420 MPa | 11.4.2 (p.93) |
| Stirrup extent | To d from compression face; anchored both ends per 12.12 | 11.4.3 (p.93) |
| Critical shear section | At d from support face (if conditions met) | 11.1.3 (p.91) |
| Max stirrup spacing | d/2 and 600 mm | 11.4.4(ก) (p.93) |
| Max stirrup spacing, high shear | d/4 and 300 mm when Vs > 0.33√f'c bw d | 11.4.4(ค) (p.94) |
| Section limit | Vs ≤ 0.66√f'c bw d | 11.4.6(ฌ) (p.95) |
| Av,min | Where Vu > 0.5φVc: Av ≥ 0.062√f'c bw s/fyt ≥ 0.35bw s/fyt; exempt: slabs, joists, h ≤ 250 mm beams, etc. | 11.4.5 (p.94) |
| Bent-up bars | ≥ 30°; centre 3/4 of incline effective; Vs ≤ 0.25√f'c bw d for a single bent group | 11.4.1, 11.4.6(จ),(ช) (p.93–95) |
| Torsion threshold | Tu < φ0.083λ√f'c Acp²/pcp → ignore | 11.5.1 (p.95) |
| Torsion stirrups | Closed, 135° hooks round a longitudinal bar (90° allowed only where slab/flange restrains spalling) | 11.5.4(ก),(ข) (p.98) |
| Torsion stirrup spacing | ≤ ph/8 and ≤ 300 mm | 11.5.6(ก) (p.98) |
| Torsion longitudinal bars | Around perimeter at ≤ 300; inside stirrups; one in each corner; dia ≥ s/24 and ≥ 10 mm; anchored both ends; extend bt + d past theoretical point | 11.5.4(ค), 11.5.6(ข),(ค) (p.98) |
| Torsion minimum steel | (Av + 2At) ≥ 0.062√f'c bw s/fyt ≥ 0.35bw s/fyt; Aℓ,min = 0.42√f'c Acp/fy − (At/s)ph fyt/fy, At/s ≥ 0.175bw/fyt; fy ≤ 420 | 11.5.5, 11.5.3(ง) (p.97–98) |
| Bar extension past cutoff | ≥ max(d, 12db) | 12.9.3 (p.114) |
| Continuing bars | ≥ ℓd past the point where cut bars are no longer needed | 12.9.4 (p.114) |
| Cutoff in tension zone | Only if Vu ≤ 2/3φVn, or extra stirrups over 3/4d, or (≤ 36 mm) 2 × As and Vu ≤ 3/4φVn | 12.9.5 (p.114) |
| Bottom bars into support | ≥ 1/3 (simple) or ≥ 1/4 (continuous) of As(+), ≥ 150 mm into support; develop fy at face if part of the lateral system | 12.10.1–12.10.2 (p.115) |
| Bar size at simple support / point of inflection | ℓd ≤ Mn/Vu + ℓa (×1.3 if confined by reaction); waived if hooked past centreline | 12.10.3 (p.115) |
| Top bars past point of inflection | ≥ 1/3 of As(−) extend max(d, 12db, ℓn/16) | 12.11.3 (p.115) |
| Top bars at support | Anchored in or through support by ℓd, hook or mechanical device | 12.11.1 (p.115) |
| Stirrup anchorage | Standard hook round a longitudinal bar (≤ 16 mm; 20–25 mm if fyt ≤ 280); each U-bend encloses a bar | 12.12.2–12.12.3 (p.116) |
| Two-piece closed stirrup | Lap 1.3ℓd; or full-depth legs if h ≥ 500 and Ab fyt ≤ 40 kN/leg | 12.12.5 (p.117) |
| End hooks at discontinuous ends | Side and top cover < 65 mm → ties ≤ 3db over ℓdh, first within 2db of bend | 12.5.4 (p.112) |
| ℓd, top-bar factor | ψt = 1.3 if > 300 mm of concrete cast below | 12.2.4(ก) (p.110) |
| Tension lap | Class B 1.3ℓd (default); Class A 1.0ℓd only if As ≥ 2As,req and ≤ 50 % spliced; ≥ 300 mm | 12.14.1–12.14.2 (p.117–118) |
| Lap limits | None for bars > 36 mm; non-contact lap spacing ≤ min(lap/5, 150); bundles per bar +20/33 % | 12.13.2 (p.117) |
| Mechanical/welded splice | Full ≥ 1.25fy; partial only ≤ 16 mm, staggered 600 mm | 12.13.3, 12.14.5 (p.117–118) |
| Compression lap | 0.071fy db ≥ 300 mm (fy ≤ 420); +1/3 if f'c < 21 MPa | 12.15.1 (p.118) |
| Seismic beam detailing | Not in this standard; see DPT 1301/1302-61 | 19.1 |

---

# Part C. TATA RC detailing handbook (M. Jiravacharadet) - beam chapter and appendix sheets


Source: `Steel_Reinforcing_Bar_Handbook_TATA_by_DRMK.pdf`. Chapter 2 "RC Beams" is printed pp. 21–49 (PDF 29–57; PDF 58 is blank). The beam-related appendix typical drawings are printed pp. 174–182, 185–186, 188 and 193–194 (PDF 182–190, 193–194, 196, 201–202).
Citation format: (TATA p.<printed page>, Fig x.y). Printed page = PDF page − 8.
Units as used in the book: Chapter 2 uses cm and m (Thai practice). The appendix sheets use mm. "D" in the appendix and "db" both mean the bar diameter. "L" means clear span unless the figure says otherwise.
Thai abbreviations used in callouts:
- ป. = stirrup
- สพศ. = extra (additional) bar
- ค.ม. = bent-up (cranked) bar
- เหล็กลูกตั้ง = stirrup
- เหล็กลูกตั้งคู่ = double (paired) stirrups

In this file, [UNCERTAIN] marks a point I could not confirm.

---

## 1. General / terminology

- Main beams frame over the column heads. Secondary beams span between main beams. Beams sit at slab edges or under walls. (TATA p.21, Fig 2.1: example floor plan with beams B1–B6, columns C1–C3, slabs S.)
- A simply supported beam has tension at the bottom, so its main bars go at the bottom. (TATA p.22, Figs 2.2–2.3)
- Old practice with plain round bars (RB) used 180° end hooks on the bottom bars. With deformed bars (DB), no end hook is needed for a simple beam. Fig 2.4(a) shows an RB bottom bar with 180° hooks at both ends. Fig 2.4(b) shows a straight DB bottom bar. (TATA p.22, Fig 2.4)
- Continuous or cantilever beams need bottom bars at midspan (sagging) and top bars over supports (hogging). (TATA p.23, Fig 2.5)
- Every beam has at least 4 longitudinal bars, one in each corner, to hold the stirrup cage during casting. (TATA p.27)
- A beam must always have stirrups, even when shear is very small or zero. (TATA p.27)
- Stirrups are normally small closed stirrups ("closed loop stirrups"): RB6, RB9 or DB10. They are placed closer together where shear is high. (TATA p.27, Fig 2.16)

## 2. Flexural reinforcement: bent-up (cranked) bars, legacy method

- **Fig 2.6 (TATA p.23), continuous beam with bent-up bars at L/5.**
  - L1 and L2 are the clear spans (face to face of supports).
  - In each span, the bent-up bar lies at the bottom over the middle portion. It rises at 45° (approx., as drawn) and runs along the top over the supports.
  - The incline ends at a point L/5 from each support face. The bottom horizontal part runs between the two L/5 points, and the bar reaches the top near the support face.
  - At the exterior supports the top portion runs to the outer face and turns down with a short 90° hook.
  - A straight bottom bar also runs through, and the top corner bars are continuous.
- **Fig 2.7 (TATA p.23), section-only notation.**
  - Section 0.20 × 0.40 m.
  - Top: 2-DB12. Bottom: 2-DB12.
  - Stirrup label: ป. 1-RB6 @ 0.20.
  - Extra bottom bar label: "1-DB12 ค.ม. L/5" = one DB12 bent up at L/5. It is shown in red at bottom centre.
- The book notes that bent-up bars are no longer popular. Closed stirrups are used for shear instead. (TATA p.27)
- **Fig 2.15 (TATA p.27).**
  - Bent-up bars near the supports cross the 45° diagonal shear cracks.
  - The bar runs along the bottom at midspan, is cranked up near each support, runs along the top, and has 90° down hooks at the beam ends.

## 3. Extra ("สพศ.") top/bottom bars and cut-off rules

### 3.1 Notation
- **Fig 2.8 (TATA p.24), beam B3 (3-span continuous).**
  - Section 0.20 × 0.40. Continuous bars 2-DB12 top and 2-DB12 bottom. Stirrups ป. 1-RB6 @ 0.20.
  - Midspan section: extra bottom bar "1-DB12 สพศ. L = 3.0" (red dot at bottom centre).
  - Support ("column head") section: extra top bar "1-DB12 สพศ. L = 2.5" (red dot at top centre).
  - Convention: สพศ. is followed by the total length of the extra bar in m.
- Usually there are more extra top bars than extra bottom bars. (TATA p.24)

### 3.2 Development length concept
- **Fig 2.9 (TATA p.24).**
  - Extra-bar length is set by the development length, measured from the point of maximum bar stress to the bar end.
  - Maximum stress is at midspan for bottom bars and at the support face for top bars.
  - The figure shows red stress arrows, with development lengths on both sides of each peak.
  - At the beam end, where the straight length is not enough, the bar is bent (hooked) to form an anchorage. The label reads "anchored by bending the bar".

### 3.3 Standard bar cut-offs (ACI Detailing Manual 2004), uniformly loaded beams with similar adjacent spans
The book gives two variants: non-perimeter (interior) beams and perimeter (edge/spandrel) beams, both with closed stirrups. (TATA p.25, Fig 2.10) Both panels are dimensioned identically:
- **Top bars at the exterior (end) support.** The extra top bars run from the exterior column into the span to **0.25L** from the interior face of the exterior support. At the outer end they turn down with a 90° hook.
- **Top bars at an interior support.** Extra top bars extend **0.3L or 0.3L1, whichever is greater**, each side of the support, measured from each support face. L and L1 are the clear spans on either side.
- **Bottom bars at the exterior support.** Bottom bars run into the support. The bar end sits **5 cm clear** from the outer face of the exterior support. The **15 cm** dimension is drawn between the bar end region and the support face; I read it as a minimum embedment of 15 cm into the support. [UNCERTAIN whether 15 cm is measured from the inner support face to the bar end or to the hook.]
- **Bottom bars at an interior support.** Some bottom bars (drawn in blue as the cut bars) stop **0.125L** short of the interior support face. The next span's bars start **0.125L1** beyond the other face. The remaining bottom bars (drawn grey) run continuously through the support.
- **Interior vs perimeter beam.**
  - Interior beam: T-section with slab on both sides.
  - Perimeter beam: L-section with slab on one side. In the perimeter beam the continuous bottom bar is hooked up 90° at the exterior support. That is the only drawn difference.
  - To avoid confusion on site, the book recommends always hooking the bottom bar end. (TATA p.25)
- Section sketches show the closed stirrup with a 135° hook at the top corner and 2 top + 3 bottom bars (the centre bottom bar is the cut bar).

### 3.4 Drafting conventions for overlapping extra bars
- **Fig 2.11 (TATA p.25), ACI convention.**
  - The extra bars are drawn offset from the continuous bars, with a dimension "0" between them. The 0 means they actually lie in the same layer.
  - Section A–A shows the extra bars in the same layer as the corner bars.
  - The book says this is not used in Thailand: workers may lift the extra bar, and it conflicts with a real second layer.
- **Fig 2.12 (TATA p.26).** The Thai alternative draws each extra bar with short 90° turned-up (or down) ends so its extent is visible. If a worker actually bends them, no harm is done, only some waste.
- **Fig 2.13 (TATA p.26), recommended.** Draw a **small inclined tick at each end of an extra bar**, only where it overlaps another bar line. This is the same "bar-end tick" used in Figs 2.26, 2.27 and 2.31.

### 3.5 Generic parametric typical beam elevation (for tabular beam schedule)
**Fig 2.27 (TATA p.32)** is the book's "typical RC beam detail". Distances are variables, and the reader computes actual lengths. Two spans L1 (end span) and L2 (interior span), dimensioned face to face:
- **First stirrup at 0.05 m from the support face.**
- End span, exterior end: extra top bar to **L1/4** from the exterior support face. Continuous top bar hooked down at the exterior column. Bottom bar hooked up.
- Interior support: extra top bars **L/3 each side** of the support, measured from the faces, where **L = the greater of L1 and L2** (note printed under the figure).
- End-span extra bottom bar: length **0.875 L1**, measured from the exterior support face. It therefore stops **0.125 L1** short of the interior face.
- Interior-span extra bottom bar: length **0.70 L2**, centred, so it stops **0.15 L2** from each face.
- Stirrup zones: **a** = dense zone at the exterior end of the end span. **b** = dense zones at each side of each interior support. The mid-zone is lighter. Zone lengths come from the schedule (Fig 2.28).
- Extra-bar ends are marked with small inclined ticks.

### 3.6 Appendix standard: continuous beam (TATA p.176, rotated sheet, "Standard reinforcement in continuous beam")
Spans L1, L2 and L3 are measured **grid to grid (column centreline)**, not clear span.
- **Extra top bars at interior supports:** **L1/3 or L2/3 each side of the grid line (use the greater L)**. The same applies at the next support with L2/3 or L3/3.
- **Extra bottom bars:** stop **L1/8** from the grid line (span 1 side) and **L2/8** (span 2 side). Equivalently, in each span the extra bottom bar stops L/8 from the grid at interior supports. At the exterior support the extra bottom bar runs into the support.
- **Continuous bottom bars at interior supports:** bottom bars of adjacent spans extend **≥ 150 mm into the support** (past the face). They are drawn joggled (cranked) so they overlap inside the column.
- **Exterior support:**
  - The top bar runs to the far face and hooks down 90°.
  - The bottom bar extends into the support (≥ 150 mm from the face) and hooks up near the far face.
  - A "100" dimension appears at the top between the grid line and a point on the column. [UNCERTAIN: purpose not legible, possibly the bar-hook position relative to the grid.]
- **First stirrup 50 mm from each support face** (both sides of every support).
- **Section A:**
  - T-beam with closed stirrup (135° hook), top and bottom bars.
  - Note: "When D > 600 mm, provide side-face bars, at least 2RB9" (one each face at mid-depth).
  - Note: "Side bars of size DB12 and larger must be embedded into the support 40 × bar diameter."
- Labels: เหล็กเสริมพิเศษบน = extra top bars. เหล็กเสริมพิเศษล่าง = extra bottom bars.

## 4. Anchorage of beam bars at supports (TATA p.177, "Reinforcement at beam ends at supports")
Two options are drawn:
1. **Straight embedment** into a large support (a deep or wide support). The top bar is embedded **52D** from the support face. The bottom bar is embedded **40D** from the support face.
2. **Hooked into the column.**
   - The top bar turns down 90° and the bottom bar turns up 90° inside the column.
   - The embedment is measured along the bar from the support face, including the hook: **top ≥ 52D, bottom ≥ 40D**.
   - The top hook leg is drawn on the outside, going down. The bottom hook leg is inside, going up, and short.

- Notes:
  1. Top bars must be anchored into the support (column) not less than **52 × bar diameter**.
  2. Bottom bars must be anchored into the support (column) not less than **40 × bar diameter**.

## 5. Cantilever beams

- **Short cantilever, with backspan (TATA p.39, Fig 2.37).**
  - Top tension bars must have at least **Ld** each side, measured from the column face (the point of maximum stress).
  - If the cantilever length is **≤ Ld**, the top bar gets a **90° down hook at the tip** to help anchorage.
  - The backspan side shows the top bar extending **Ld** beyond the column face, ending with an inclined bar-end tick.
  - The bottom bar is continuous. Stirrups run throughout.
- **Long cantilever, with backspan (TATA p.40, Fig 2.38).**
  - L = cantilever length, measured to the column centreline.
  - Top steel Ast: **half (0.5 Ast) may be stopped** at a distance ≥ the greater of **0.5L or Ld** from the column face. The remaining 0.5 Ast runs to the tip and has a 90° down hook.
  - The depth may taper towards the tip, with a **minimum tip depth of 15 cm**.
  - Bottom bars: **0.25 Ast (MIN.), at least 2 bars**, follow the sloping soffit. They extend past the column face into the column by **Ld/3**, drawn lapping with the backspan bottom bar.
  - Stirrups continue to the tip.
- **Cantilever from a column with no backspan (TATA p.40, Fig 2.39).**
  - The top bars (Ast) pass through the column and bend down 90° at the far side. The anchorage length **Ld** is measured from the column face along the bar, down the hook.
  - 0.5 Ast is cut at ≥ max(0.5L, Ld) from the face. The other 0.5 Ast runs to the tip with a 90° down hook.
  - Bottom bars: **0.25 Ast (MIN.), at least 2 bars**, extend **Ld/3** past the column face into the column.
  - Constant depth is drawn.

## 6. Shear reinforcement (stirrups)

### 6.1 Notation and zoning
- **Fig 2.17 (TATA p.27), small building with 4 corner bars and uniform stirrups.**
  - Section 0.20 × 0.40, 2-DB12 top, 2-DB12 bottom.
  - "ป. 1-RB6 @ 0.20" means one RB6 stirrup at 0.20 m spacing along the whole beam.
  - The elevation shows stirrups at 0.20 spacing.
- **Fig 2.18 (TATA p.28), elevation conventions.**
  - (a) Each stirrup is drawn with spacing arrows.
  - (b) Preferred: draw only the **first and last stirrup**, connect them with a dimension arrow, and label "ป. RB9 @ 0.20 ม.".
- **Fig 2.19 (TATA p.28), multi-zone stirrups.**
  - Each zone is labelled with stirrup size, spacing and zone length: **DB10@0.15 m over 1.40 m | RB9@0.20 m over 2.60 m | DB10@0.15 m over 1.40 m**.
  - Stirrups are denser and heavier at the ends and lighter at midspan.
  - The first stirrup is drawn essentially at the support face.
  - At the exterior support, the top bar hooks down and the bottom bar hooks up (C-shape, with a gap between the hook legs).
- **Complete beam detail (Fig 2.26, TATA p.32).**
  - Clear span 5.50 m, section 0.30 × 0.50 m.
  - Stirrups: DB10@0.15 m over 1.40 m, then RB9@0.20 m over 2.60 m, then DB10@0.15 m over 1.40 m.
  - Top bars:
    - Left end (A-A): 3-DB25 (2 continuous + 1 extra). The extra top bar ends **1.38 m** (= 0.25 × 5.50) from the left face.
    - Midspan (B-B): 2-DB25.
    - Right, interior support (C-C): 5-DB25 (3 extra). The extra top bars start **1.84 m** (≈ 5.50/3) from the right face and continue over the support.
  - Bottom bars: 3-DB25 throughout. One bottom bar ends **0.70 m** (≈ 0.125 × 5.50) from the right face, with an end tick.
  - Section stirrups: A-A DB10@0.15, B-B RB9@0.20, C-C DB10@0.15.
  - At the exterior end, the top bars hook down and the bottom bars hook up in the column.
  - The book says a complete detail = elevation (continuous bars, extra bars, stirrups, with positions and lengths) + sections where the steel changes, normally left end, midspan and right end. (TATA p.32)

### 6.2 Stirrup configurations
- **Fig 2.20 (TATA p.28), stirrups named by number of vertical legs.**
  - **1-leg:** a single vertical bar in a T-beam web with 180° hooks around one top bar and one bottom bar.
  - **2-leg (three drawn variants):**
    - (i) Open U-stirrup with 180° hooks around the two top bars.
    - (ii) Closed stirrup with **135° hooks** at one top corner.
    - (iii) Closed stirrup closed with a **90° hook** overlap at a top corner.
  - **4-leg:** outer closed stirrup + one inner narrow closed stirrup, each with 135° hooks. Drawn with 3 bars top and bottom.
  - **6-leg:** outer closed stirrup + two inner narrow closed stirrups.
  - Normal rectangular beams use 2-leg closed stirrups. More legs are used when more shear capacity is needed. (TATA p.28)
- **Appendix stirrup types (TATA p.179, T-beams):**
  - TYPE I: closed stirrup. Single closed loop, 135° hooks at the top corner.
  - TYPE II: double closed stirrup. Outer closed stirrup + one narrow closed stirrup at the centre.
  - TYPE III: stirrup with cap. U-stirrup + separate top cap tie, with 135° hooks at the top.
  - TYPE IV: two-layer closed stirrup. Two nested closed stirrups, one inside the other.
  - TYPE V: multiple closed stirrups. Outer + two overlapping inner closed stirrups.
- **Torsion (TATA pp.31–32, Fig 2.25).**
  - ACI requires closed stirrups for beams under torsion, such as edge (spandrel) beams.
  - Under torsion, the cover concrete at the corners spalls from the diagonal compressive stresses. It spalls especially at the outer corners not restrained by a slab; the slab side is "spalling restrained by slab".
  - A U-stirrup with a lap at the top would lose anchorage when the corner spalls, hence closed stirrups with 135° hooks.
  - In Thailand, closed stirrups are generally used in all beams anyway.

### 6.3 Standard hooks (TATA p.174, "Standard hooks" sheet)
**Main bars, minimum inside bend diameter D:**
- D = 6db for bars 6–25 mm.
- D = 8db for bars 28–36 mm.
- D = 10db for bars 44–57 mm.

**Hook geometry:**
- 180° hook: extension 4db ≥ 60 mm.
- 90° hook: extension 12db.
- G = hook allowance (length added). J = overall hook dimension, as drawn.

| Bar | D (mm) | 180° G | 180° J | 90° G | 90° J |
|---|---|---|---|---|---|
| RB9 | 55 | 110 | 73 | 120 | 150 |
| DB10 | 60 | 120 | 80 | 130 | 160 |
| DB12 | 75 | 130 | 99 | 160 | 200 |
| DB16 | 100 | 160 | 132 | 210 | 260 |
| DB20 | 120 | 190 | 160 | 260 | 320 |
| DB25 | 150 | 240 | 200 | 320 | 400 |
| DB28 | 225 | 330 | 281 | 380 | 550 |
| DB32 | 255 | 370 | 319 | 430 | 620 |
| DB36 | 290 | 420 | 362 | 480 | 800 |

**Stirrup hooks (90° and 135°):**
- 90° stirrup hook extension H = 6db for RB6–DB16, and H = 12db for DB20–DB25.
- 135° stirrup hook extension = **6db** (drawn).
- Stirrup bend diameter D = 4db for RB6–DB16, and D = 6db for DB20–DB25.
- Table (mm). The column headers are printed as "180°" and "90°". Since the drawn stirrup hooks are 90° and 135°, the first pair probably belongs to the 135° hook. [UNCERTAIN: header labelling in source]

| Bar | D | "180°" G | "180°" J | 90° G | 90° J |
|---|---|---|---|---|---|
| RB6 | 25 | 40 | 60 | 50 | 45 |
| RB9 | 35 | 60 | 80 | 70 | 65 |
| DB10 | 40 | 70 | 90 | 80 | 75 |
| DB12 | 50 | 80 | 110 | 100 | 90 |
| DB16 | 65 | 100 | 150 | 130 | 120 |
| DB20 | 120 | 260 | 320 | 180 | 170 |
| DB25 | 150 | 320 | 400 | 230 | 210 |

**Seismic stirrup hook:** 135° hook with **10db** extension. Table header is printed "180°" [UNCERTAIN, presumably 135°].

| Bar | D | G | J |
|---|---|---|---|
| DB10 | 40 | 120 | 100 |
| DB12 | 50 | 150 | 120 |
| DB16 | 65 | 190 | 160 |
| DB20 | 120 | 260 | 220 |
| DB25 | 150 | 330 | 280 |

## 7. Minimum depth (Table 2.1, TATA p.29)
Minimum h for non-prestressed one-way members, unless deflections are calculated:

| Member | Simply supported | One end continuous | Both ends continuous | Cantilever |
|---|---|---|---|---|
| One-way slab | L/20 | L/24 | L/28 | L/10 |
| Beam | L/16 | L/18.5 | L/21 | L/8 |

- The values assume normal-weight concrete wc = 2,320 kg/m³ and SD40 steel.
- Lightweight concrete (wc 1,500–2,000 kg/m³): multiply by (1.65 − 0.0003 wc), but not less than 1.09.
- For fy other than 4,000 ksc: multiply by (0.4 + fy/7,000), with fy in ksc.

## 8. Bar spacing, beam width, cover, layers, bundles

- **Clear horizontal spacing** between parallel bars ≥ the greatest of 2.5 cm, db, and 4/3 × maximum aggregate size. (TATA p.29, Fig 2.21)
  - Common aggregate 3/8" (0.95 cm) or 3/4" (1.9 cm) gives 1.3 or 2.5 cm, so in practice use 2.5 cm or db.
- **Clear vertical spacing between layers** ≥ **2.5 cm**. (TATA p.29, Fig 2.21, which shows 2.5 cm between the layers and s_min between the bars.)
- **Appendix typical section (TATA p.179):**
  - Clear distance between bar layers = **1 × bar diameter, or at least 25 mm**.
  - Cover **40 mm CLR. (TYP.)** from the beam face to the stirrup.
  - Labels:
    - top bars, 1st layer
    - top bars, 2nd layer (if any)
    - slab thickness = t
    - side-face bars (if any), at about mid-depth each side
    - bottom bars, 2nd layer (if any)
    - bottom bars, 1st layer
    - stirrup
    - WIDTH, DEPTH
  - The drawing shows 4 bars per layer, top 2 layers, bottom 2 layers, and side bars 2 per face.
  - The book's minimum-width table (Table 2.2) instead assumes **2 cm side cover** (cast-in-place, not exposed to earth or weather). The appendix sheet says 40 mm. Use the project's spec.
- **Minimum beam width: 20 cm, with at least 2 bars.** Typical sizes b × h (cm): 20×40, 20×50, 30×50, 30×60, 40×70, 40×80. (TATA p.30)
- **Fig 2.22 (TATA p.30), width computation.**
  - b = 2 × side cover + 2 × stirrup diameter + n·db + (n−1)·s.
  - Side cover = **2 cm** (label: cover = bar size, but not less than 2 cm).
  - Stirrup = **9 mm**.
  - Clear bar spacing = **2.5 cm** or db if db > 25 mm (label: clear spacing = bar size, but not less than 2.5 cm).
  - Example: 4-DB16 gives b = 2(2.0) + 2(0.9) + 4(1.6) + 3(2.5) = **19.7 cm**. (TATA p.31)
- **Table 2.2 (TATA p.30): minimum beam width (cm) by number of bars in one layer.**

| Bar | 2 | 3 | 4 | 5 | 6 | 7 | 8 | add per bar |
|---|---|---|---|---|---|---|---|---|
| DB12 | 10.7 | 14.4 | 18.1 | 21.8 | 25.5 | 29.2 | 32.9 | 3.7 |
| DB16 | 11.5 | 15.6 | 19.7 | 23.8 | 27.9 | 32.0 | 36.1 | 4.1 |
| DB20 | 12.3 | 16.8 | 21.3 | 25.8 | 30.3 | 34.8 | 39.3 | 4.5 |
| DB25 | 14.3 | 19.3 | 24.3 | 29.3 | 34.3 | 39.3 | 44.3 | 5.0 |
| DB28 | 15.8 | 21.4 | 27.0 | 32.6 | 38.2 | 43.8 | 49.4 | 5.6 |
| DB32 | 17.8 | 24.2 | 30.6 | 37.0 | 43.4 | 49.8 | 56.2 | 6.4 |

  The 20 cm absolute minimum still governs.
- **Many bars (TATA p.31, Figs 2.23–2.24).**
  - When the bars do not fit in one layer, place them in several layers. If that is still insufficient, **bundle** them. ACI allows at most **4 bars per bundle**.
  - Fig 2.23 bundle shapes: 2-bar (side by side, or stacked), 3-bar (L-shape or triangle), 4-bar (square).
  - Fig 2.24 arrangements, all in 2 layers. Bars and bundles are aligned vertically.
    - (1) 3 single bars per layer.
    - (2) 3 horizontal 2-bar pairs per layer.
    - (3) 3 vertical 2-bar pairs per layer, which effectively gives 4 rows.
    - (4) Bottom layer of 4-bar square bundles, upper layer of 3-bar triangular bundles.
  - Horizontal clear gap **a** = greatest of 2.5 cm, db, and 4/3 × aggregate size. Vertical clear gap **b = 2.5 cm**.
- **Spacer bar between layers:** the book does not name a separate "spacer bar". Only the 25 mm / 1db clear layer spacing is specified.

## 9. Laps and splices (TATA pp.35–38; appendix p.175)

- Bars are supplied in **10 m** lengths, so continuous beams need splices. Splice away from the points of maximum tension, and stagger splices so that not all bars are spliced at one section. (TATA pp.35–36)
- Fig 2.32 shows stress transfer in a lap: each bar's stress runs from fy to 0 over the lap length. (TATA p.36)
- **Splice rules (EIT 1008-38, quoted on TATA p.36):**
  - Lap splices are allowed for bars **≤ DB36**.
  - Tension lap: Class A = **1.0 ld**, Class B = **1.3 ld**, in all cases **≥ 30 cm**.
  - Basic ld = 0.06 Ab fy / √f'c (cm, ksc).
  - **Table 2.3**, basic ld (cm) for f'c = 240 ksc and SD40:

| Bar | Area (cm²) | ld (cm) |
|---|---|---|
| DB10 | 0.785 | 12.2 |
| DB12 | 1.13 | 17.5 |
| DB16 | 2.01 | 31.1 |
| DB20 | 3.14 | 48.6 |
| DB25 | 4.91 | 76.1 |
| DB28 | 6.16 | 95.4 |
| DB32 | 8.04 | 125 |
| DB36 | 10.18 | 158 |

  - Traditional simple rule: deformed-bar lap **≥ 36 db and ≥ 30 cm**. (TATA p.37)
  - Use Class B for deformed bars in tension. Class A is allowed only if both conditions hold:
    - (1) As provided ≥ 2 × As required over the whole splice length, and
    - (2) no more than half of the bars are spliced within the lap length. (TATA p.37)
- **Where to splice (Fig 2.33, TATA p.37).**
  - Splice tension bars away from high tension, where As provided ≥ 2 × As required.
  - In ordinary beams: **top bars are lapped at midspan**, and **bottom bars are lapped near the supports**.
  - The 3-D figure shows the bottom lap A located within about **L/3–L/4** from the support. A = lap length, L = beam span.
- **Bundled-bar laps (TATA p.38):** use the individual-bar lap length **+20% for 3-bar bundles, +33% for 4-bar bundles**.
- **Non-contact laps (TATA p.38):** clear spacing between the lapped bars ≤ 1/5 of the lap length and ≤ 15 cm.
- **Staggered laps (Fig 2.34, TATA p.38):**
  - Clear gap between the two lapped bars **≤ 4db or ≤ 5 cm**. If larger, increase the lap by the excess.
  - Longitudinal offset between adjacent laps **≥ 0.3 × lap length** (0.3A).
  - Clear gap between adjacent lapped pairs **≥ 2db or ≥ 2 cm**.
- **Welded splices and mechanical couplers (Figs 2.35–2.36, TATA pp.38–39; appendix p.175):**
  - A full splice must develop **≥ 1.25 fy** (125% of the bar's tensile strength). Use welded splices where As provided < 2 × As required.
  - Weld types shown:
    - Metal-arc butt weld with double-V preparation.
    - Lapped bars 15 × bar size with 2 metal-arc fillet welds, each 5 × bar size long.
    - Butt weld with a splice bar fillet-welded over 10 × bar size.
  - Appendix butt weld in tension: 45° bevel, 3 mm root gap. Chip the weld slag off, and inspect or clean both sides after welding.
  - Couplers: when splicing with couplers, the bar cross-section must not be reduced. [paraphrase; Thai text partly garbled]
  - Fig 2.36 shows coupler types 1a/1b/2/3/4/5/6/7: threaded, tapered-thread, grout/lock-nut, swaged sleeve, wedge, and lockshear bolt couplers.

## 10. Main-beam / secondary-beam junctions and hanger bars

- **Fig 2.29 (plan) and Fig 2.30 (elevation) (TATA pp.33–34).**
  - Detail A is B1 × B2 crossing at a column. The elevation must show which beam's bars are on top and which are below. As drawn, B2's top bars sit just **below** B1's top bars and B2's bottom bars just **above** B1's bottom bars.
  - Detail B: B3 is a secondary beam framing into main beam B1.
    - B3's top bars sit **on top of** B1's top bars, so the top and bottom covers of the secondary beam are unequal.
    - B3's bottom bars rest on B1's bottom bars.
    - A cranked **hanger bar** (red) cradles B3's bottom bars and rises into the B1 top on both sides.
  - The text: provide hanger bars when the load from the secondary beam is large. (TATA p.33)
- **Fig 2.31 (TATA p.35), main–secondary beam junction.** Both beams are drawn at the same top level.
  - **Wrong way:** B2 (secondary) cage sits inside B1 with its top bars under B1's top bars, and there are no hangers.
  - **Right way (Detail A):**
    - *"Secondary beam top reinf. bars on top of primary beam top reinf. bars"* (the primary beam top bars are lowered to avoid the clash).
    - *"2-DB16 hanger bars, one on each side of primary beam (inside stirrups)."* The hangers are bent up at **60°**, run under B2's bottom bars, and rise to the top of B1. Their horizontal top legs extend **1.5d** beyond each face of B2, where d = effective depth of B1.
    - **Dense stirrups** in B1 around the junction (additional stirrups on each side of B2).
- **Appendix: secondary beam to main beam (TATA p.180).** Three cases. All crank the secondary-beam bars at a slope **1:12**.
  1. **Main and secondary beams of different sizes (secondary shallower):**
     - Secondary top bars are cranked down at 1:12 to pass **under** the main-beam top bars. They are continuous across.
     - Secondary bottom bars are straight, above the main-beam bottom bars. Bars from each side overlap through the main beam and end with bar-end ticks in the adjacent secondary span.
  2. **Main and secondary beams of the same size:**
     - Top bars are cranked down at 1:12 under the main-beam top bars.
     - Bottom bars are cranked up at 1:12 to pass **over** the main-beam bottom bars. The bottom bars from both sides lap through the main beam and end with ticks.
  3. **Main beam supports the end of a secondary beam:**
     - Top bars are cranked down at 1:12 under the main top bars and continue to the far side of the main beam. There they turn **down 90°** with a long vertical leg, nearly the full depth.
     - Bottom bars are cranked up at 1:12 over the main bottom bars and run straight to the far side of the main beam.
  - Note: this appendix sheet puts the secondary top bars **below** the main top bars, while Fig 2.31 says **on top**. Flag this for the office standard; the choice depends on which beam governs.

## 11. Beams at different levels / different depths / haunches

- **Beams at different levels over a column (Fig 2.40, TATA p.41).**
  - **Wrong:** cranking the continuous bars through the level change. The tension in the kinked bar pushes outward and cracks the concrete; red arrows show the outward thrust.
  - **Right:** use **separate bars**, each anchored with a **90° bend** inside the column.
    - The higher beam's top bar crosses the column and turns down.
    - The lower beam's top bar extends straight into the higher beam.
    - The higher beam's bottom bar extends straight into the lower beam's span.
    - The lower beam's bottom bar turns up into the column.
- **Beams of different depth, tops flush (Fig 2.41, TATA p.41).**
  - The top bars are continuous.
  - The shallower beam's bottom bar extends straight into the deeper beam.
  - The deeper beam's bottom bar turns up 90° inside the column.
- **Step within a span, small step (< h) (Fig 2.42, TATA p.41).**
  - The main bars (designed for the stepped beam) run straight through at the lower level.
  - Add **crack-control bars** in the higher part: an extra top bar, hooked down at both ends, in the raised portion, with the stirrups extended up to it.
  - Double stirrups are drawn at the step face.
- **Step larger but ≤ h (Fig 2.43, TATA p.42).**
  - The lower beam's top bar extends into the higher beam. The higher beam's bottom bar extends back into the lower beam.
  - **Overlap zone ≥ h** ("h or more"), with embedment **≥ 35D**.
  - A **closed loop** bar ties the higher top to the lower bottom in the step zone.
  - The higher beam's top bar hooks down at its far end. Stirrups are full height in the overlap.
- **Step > h (Fig 2.44, TATA p.42).**
  - The step region acts as a short column-like block, width **h or more**.
  - The lower beam's bars end in closed U-loops. The upper beam's bars loop down.
  - Horizontal ties (stirrups laid horizontally) run across the step block.
- **Alternative for a step > h: two-level beam (Fig 2.45, TATA p.42).** A short stub column (post) on the lower beam supports the upper-level beam. The post bars are hooked into the bottom of the lower beam and the top of the upper beam, with ties along the post.
- **Appendix (TATA p.178), "Bar placement in beams".**
  - **Bottom bars continuous in beams with different soffit levels** (small step at the column):
    - Crank the bottom bar at a slope **≥ 6:1** (1 vertical in ≥ 6 horizontal) within the column.
    - Put **double stirrups (paired stirrups)** at each end of the crank.
  - **Larger soffit difference:** use separate bars.
    - The lower-soffit beam's bottom bar is bent up at the step and continues **Ld** beyond, along the higher bottom.
    - The higher-soffit beam's bottom bar extends straight across the column into the lower beam **Ld** beyond the bend.
    - Ld = additional embedment length.
  - **Haunched soffit (beam with a deepened soffit at the support):**
    - The inclined bottom bar follows the haunch and extends **Ld** past its intersection with the span bottom bar.
    - The span bottom bar extends **Ld** past the haunch kink.
    - Double stirrups at the kinks.
  - **Beam section:** "When H exceeds 600 mm, add at least 2DB12 [side bars], continuous with staggered laps." Compare p.176: "at least 2RB9 when D > 600 mm". [Inconsistent in the source: 2DB12 vs 2RB9.]

## 12. Beam supporting a column (planted column / transfer)
- **Fig 2.46 (TATA p.43).**
  - Extend the column bars down to the beam's bottom bars. They end with **90° hooks turned horizontally outward**, resting on the bottom bars.
  - Column ties continue through the beam depth.
  - Put **dense stirrups** in the beam around the column to confine and transfer the load to the top of the beam.
  - For heavy loads, add **bent-up (cranked) bars** under the column. They run from the beam top on each side down under the column.
  - Beam stirrup spacing is s. **First stirrup at s/2 from the column face; the label also says "or less than 5 cm"** [wording ambiguous: "s/2 or less than 5 cm from the column face"].
- **Appendix: typical column-to-transfer-beam (TATA p.188).**
  - A column standing on a beam: **column ties must continue into the beam at the same spacing throughout**.
  - The column bars go down to the beam bottom and bend 90° horizontally. The anchorage is **40D**, measured from the beam top along the bar to the hook end.
  - The transfer beam's top and bottom bars hook into the exterior column (C-shape).

## 13. Notched / recessed beams
- **Fig 2.47 (TATA p.43).**
  - For a beam with a recess (a notch in the soffit or top at midspan), bending the main bars around the notch is **wrong**. A kinked tension bar cracks the re-entrant corner.
  - **Right:** use separate bars, each extended past the corner and anchored (drawn as two crossing straight bars at the re-entrant corner, with one turned 90°).

## 14. Deep beams and side-face (skin) reinforcement
- **Definition (TATA p.44, Fig 2.48).** A deep beam is loaded on one face and supported on the opposite face, and either:
  - (a) **Ln/h ≤ 4** (Ln = clear span between support faces), or
  - (b) a concentrated load acts within **2h** of the support face (x < 2h).
- **Stress behaviour (Fig 2.49, TATA p.45).**
  - The elastic stress distribution is nonlinear: c ≈ 0.75h, lever arm y ≈ (0.6–0.8)h.
  - The figure also shows stress trajectories, the crack pattern (vertical/inclined cracks from the soffit), and a truss (strut-and-tie) model for a point load.
  - Main tension steel is placed in the **bottom one-fifth of the depth**. Both horizontal and vertical web reinforcement are required.
- **Side-face bars (Fig 2.50, TATA p.46).**
  - ACI recommends longitudinal skin bars on the vertical faces of the **tension zone, over h/2**.
    - For positive moment: the bottom h/2, above the bottom bars.
    - For negative moment: the top h/2, below the top bars.
  - Spacing s is more important than size. Use **9–16 mm bars or welded wire**, with **≥ 2.15 cm² per metre of depth** (per face as given).
- **Example (Fig 2.51, TATA p.46): transfer deep beam.**
  - Length 10.8 m, depth 3.6 m, width 0.6 m.
  - Supported on 60 × 60 cm columns at the ends. Two 60 × 60 cm columns bear on the top at the third points (3.6 m + 3.6 m + 3.6 m).
  - Web mesh **DB12@0.15 m # each face**.
  - Main bottom steel **17-DB36 with 90° hooks in 5 layers**, hooked up at both supports.
  - The section shows the mesh on both faces and the 5-layer bottom steel.
- **Appendix: side bars in ordinary beams.**
  - D > 600 mm: at least 2RB9 side bars (p.176), or at least 2DB12, continuous with staggered laps (p.178).
  - Side bars ≥ DB12 are anchored 40D into the supports (p.176).

## 15. Openings in beams (TATA pp.47–49)
- Openings let services pass through beams and save storey height (Fig 2.52). Shapes (Fig 2.53): circular, rectangular, diamond, triangular, trapezoidal, irregular. Circular and rectangular are the most common. Round the corners of rectangular openings to reduce stress concentration.
- **Small openings (Fig 2.54, TATA p.48).**
  - Circular with diameter **d ≤ 0.25h**. Square with side ≤ d, drawn with the same d.
  - These may be treated as not reducing strength (designed as a solid beam). Still add extra bars around them against cracking.
- **Opening location (Fig 2.55, TATA p.48).** Section A–A: the opening lies below the flexural compression block βc (clear top chord ≥ βc) and its depth is ≤ h/2.
  1. In T-beams the opening lies below the flange. In rectangular beams it normally lies at mid-depth, and may be offset if enough concrete remains for flexural compression and for shear reinforcement.
  2. Clear distance from the **support face, concentrated loads, and adjacent openings ≥ h/2**.
  3. Opening depth **≤ h/2**.
  4. Opening length is limited by chord stability and deflection. Prefer several small openings to one large one.
  5. Multiple openings: spacing **≥ h/2**.
- **Circular opening reinforcement (Figs 2.56–2.57, TATA p.49).**
  - Two failure modes: (a) beam-type failure, with a diagonal crack through the opening, and (b) frame-type failure, with cracks in the chords above and below.
  - **Diagonal bars** (X-pattern, on both sides of the opening) should resist **at least 50% of the applied shear**. Their purpose is crack control.
  - **Short stirrups** in the chords above and below the opening resist frame-type failure.
  - **Full-depth long stirrups** on each side of the opening resist beam-type failure.
  - **Additional horizontal bars** above and below the opening anchor the stirrups.
  - The section shows the top chord h_t and bottom chord h_b, each with its own closed stirrup, and the opening d0 between them.
- **Rectangular opening (Fig 2.58, TATA p.49).**
  - Same scheme: diagonal bars at the four corners (cranked, forming an X-pattern at each end) and horizontal bars above and below the opening.
  - Short closed stirrups in the top and bottom chords, and full-depth stirrups at each end.
  - Section A-A shows two separate closed stirrups (top chord and bottom chord).

## 16. Tabular beam schedule
- **Fig 2.28 (TATA p.33).** Used for large buildings with many beams. The typical parametric elevation (Fig 2.27) is combined with a table.
  - One column per beam (e.g. B1), with sub-columns: **exterior support / midspan / interior support**.
  - Each sub-column has a section sketch. Rows: **section size, top bars, bottom bars, stirrups**.
  - Example B1, section 0.30 × 0.50:

| | Exterior support | Midspan | Interior support |
|---|---|---|---|
| Top bars | 3-DB20 | 3-DB20 | 5-DB20 |
| Bottom bars | 3-DB20 | 3-DB20 | 2-DB20 |
| Stirrups | DB10@0.15, **a = 1.5 m** | RB9@0.20 | DB10@0.15, **c = 2.0 m** |

  - The interior-support sketch shows the 5-DB20 as 3 bars in the first layer + 2 bars in a second layer below the corner bars. The stirrup is closed with a 135° hook.
  - Special beams are detailed separately. (TATA p.33)

## 17. Other related appendix items
- **Upstand and downstand ribs (curbs/fins), when not specified on drawings (TATA p.182):**
  - Thickness 70 mm, height 300–500: 1DB12 at the free edge, **2RB9** longitudinal, **RB6@200** hairpin/U-bars anchored **300 mm** into the supporting beam or slab. The downstand is a mirror image.
  - Thickness 100 mm, height 500–1000: 1DB16 at the free edge, **RB9@250** longitudinal (pairs, both faces), **RB6@200** U-bars anchored **300 mm**.
- **Sunshade fins at slab edges (TATA p.181):**
  - Up to 100 thick and ≤ 300 high: 1DB12 at the edge, 1DB10 at the root, **1DB10@250** U-bars. Anchorage leg **400** into the slab.
  - Over 100 thick or > 300 high: 2DB12 + 2DB10 longitudinal, 1DB10@250 closed/U bars, 400 anchorage.
  - Same for the downward fin (1DB12 at the bottom edge).
- **Slab steps H < T and H > T (TATA p.181):** slab, not beam. Bars lap Ld each side of the step. For H > T an inclined bar is added, with Ld each side.
- **Beam–column joints (TATA pp.183–186).** Column-focused sheets; the beam-related points are:
  - First column tie **50 mm** above the slab/beam top and **50 mm** below the beam soffit or flat-slab soffit.
  - Column lap zone "750 to Lc/2".
  - At the roof, column bars end with a **standard 90° hook** into the beam/slab top.
  - For spiral columns, **horizontal ties at ≤ 150 mm** through the beam depth. The spiral stops at the level of the lowest beam bottom bars.
- **Composite column (TATA p.194).** Where a steel section blocks the stirrups, weld the stirrups to the steel section. Beam bars of the frame or continuous beams that meet the steel section transfer force through a **"transferred steel plate"** welded to the section, with strength ≥ the bar strength. Plan and section show the plates at the beam top-bar and bottom-bar levels.
- **Steel beam at lift wall (TATA p.193), if not specified.** H 100×100×6×8 mm (17.2 kg/m) @ 2000 mm, on a PL 150×150×6 mm embedded plate with **2-DB16 welded** anchors. The dimension "150 mm" is also given as "if not specified". [the exact location of the 150 mm dimension is uncertain]

---

## Drawing-ready typical details (candidates for an office "Typical Beam Details" sheet)

1. **Typical beam section / stirrup types** (from p.179 and Fig 2.20).
   - Layer labels: top 1st/2nd, bottom 1st/2nd, side bars.
   - Clear layer spacing = max(db, 25 mm).
   - Cover 40 mm clear (TYP.), or per the project spec.
   - Stirrup TYPES I–V: closed, double closed, cap, two-layer nested, multiple.
   - 1-, 2-, 4- and 6-leg arrangements. 135° hooks at the top corner.
2. **Standard hook & bend table** (p.174).
   - Main bars: D = 6/8/10 db, 180° hook 4db ≥ 60 mm, 90° hook 12db.
   - Stirrups: 90° hook 6db (RB6–DB16) / 12db (DB20–DB25); 135° hook 6db; seismic 135° hook 10db; D = 4db / 6db.
   - G/J tables.
3. **Continuous beam standard elevation, grid-based** (p.176).
   - Extra top bars L/3 each side of the grid (greater adjacent L).
   - Extra bottom bars stop L/8 from the interior grid.
   - Bottom bars ≥ 150 mm into supports.
   - First stirrup 50 mm from the face.
   - Side bars when D > 600 (2RB9 or 2DB12), with DB12+ side bars anchored 40D.
4. **Alternative ACI clear-span cut-off elevation** (Fig 2.10 / 2.27), interior and perimeter beams.
   - Top: 0.25L at the exterior support; 0.3L (or L/3) each side at interior supports, using the greater span.
   - Bottom cut bars stop 0.125L from the interior face. Bottom extra 0.875L1 (end span) and 0.70L2 (interior span).
   - 5 cm clear at the end, 15 cm minimum into the support.
   - First stirrup 0.05 m from the face.
   - Perimeter beam: bottom bar hooked up at the exterior support.
5. **Beam-end anchorage at supports** (p.177). Top 52D, bottom 40D, either straight or hooked (top hook down, bottom hook up).
6. **Stirrup zoning/labelling convention** (Figs 2.18–2.19, 2.26). Zone label = size@spacing + zone length. Draw only the first and last stirrup with an arrow.
7. **Extra-bar end convention** (Fig 2.13). Small inclined tick at the bar ends where bars overlap. Callouts: สพศ. with length; ค.ม. L/5 for bent-up bars.
8. **Tabular beam schedule** (Fig 2.28). Columns exterior support / midspan / interior support. Rows size / top / bottom / stirrups, plus zone lengths a and c.
9. **Cantilever beams** (Figs 2.37–2.39).
   - Short: Ld each side, tip hook if the cantilever ≤ Ld.
   - Long: 0.5 Ast cut at ≥ max(0.5L, Ld); tip depth ≥ 15 cm; bottom 0.25 Ast min, ≥ 2 bars, into the column Ld/3.
   - No backspan: top bars hooked down into the column with Ld.
10. **Secondary-to-main beam connection** (p.180, three cases, 1:12 cranks) **+ hanger bars** (Fig 2.31).
    - 2-DB16 hangers each side of the main beam, inside the stirrups, bent at 60°, extending 1.5d beyond the secondary beam faces.
    - Dense stirrups in the main beam at the junction.
    - Decide the top-bar hierarchy: secondary on top per Fig 2.31, or under per p.180.
11. **Beam–beam crossing at a column** (Figs 2.29–2.30). Show which bars are over or under in both directions.
12. **Beams at different levels / depths at a column** (Figs 2.40–2.41). Separate bars with 90° bends, no cranked continuous bars.
13. **Soffit-level change / haunch bottom bars** (p.178).
    - Crank slope ≥ 1:6 with double stirrups at the bends, or separate bars lapped Ld.
    - Haunch: bars extended Ld past the kinks.
14. **Step within a span** (Figs 2.42–2.45).
    - < h: crack-control bars.
    - ≤ h: overlap ≥ h, embedment ≥ 35D, closed loop.
    - > h: step block of width ≥ h with horizontal ties, or a stub column (two-level beam).
15. **Beam supporting a column / column on a transfer beam** (Fig 2.46; p.188).
    - Column bars down to the beam bottom with 90° horizontal hooks (40D).
    - Column ties continue through the beam.
    - Dense beam stirrups, first at s/2 (≤ 5 cm, wording ambiguous) from the column face.
    - Optional bent-up bars.
16. **Notched beam** (Fig 2.47). Separate bars at the re-entrant corner, not bent around it.
17. **Openings in beams** (Figs 2.54–2.58).
    - Limits: d ≤ 0.25h for "small"; depth ≤ h/2; ≥ h/2 from supports, point loads and other openings; below the compression block.
    - Reinforcement: diagonal bars for ≥ 50% of V, short chord stirrups, full-depth stirrups each side, extra horizontal bars. Circular and rectangular versions.
18. **Deep beam / side-face bars** (Figs 2.48–2.51).
    - Deep if Ln/h ≤ 4 or a point load is within 2h.
    - Main steel in the bottom h/5.
    - Skin bars over the tension half-depth, 9–16 mm, ≥ 2.15 cm²/m.
    - Web mesh each face (example DB12@0.15).
19. **Lap splice rules note block.**
    - Lap Class A 1.0 ld / Class B 1.3 ld, ≥ 30 cm (or the traditional 36db ≥ 30 cm); ld table.
    - Top bars lapped at midspan, bottom bars near the supports (L/4–L/3 zone).
    - Bundles +20% / +33%.
    - Non-contact laps ≤ lap/5 and ≤ 15 cm.
    - Stagger ≥ 0.3 lap.
    - Welds and couplers ≥ 1.25 fy.
20. **Width/spacing note block.**
    - Minimum b = 20 cm, ≥ 2 bars.
    - Clear spacing ≥ max(2.5 cm, db, 4/3 aggregate). Layers ≥ 2.5 cm apart.
    - Table 2.2 of minimum widths.
    - Minimum depth Table 2.1 (L/16, L/18.5, L/21, L/8), with the fy and lightweight-concrete modifiers.
21. **Upstand/downstand rib defaults** (p.182) and **sunshade fin defaults** (p.181), for "unless otherwise noted" details.

---

## Pages viewed / legibility

- **Chapter 2 (PDF 29–58 = printed 21–50):** all pages were rendered (tb_29…tb_58.png) and viewed, with the text read from tata.txt. Zoom crops were made of Figs 2.6, 2.10, 2.11, 2.19, 2.20, 2.24, 2.26, 2.27, 2.28, 2.30, 2.31, 2.33, 2.37–2.39, 2.40–2.44, 2.46, 2.55, 2.57/2.58. PDF 58 (printed 50) is blank.
- **Appendix (PDF 179–208):**
  - Viewed as images: PDF 182 (p.174 hooks), 183 (p.175 couplers/weld), 184 (p.176 continuous beam, rotated sheet rendered rotated), 185 (p.177 beam-end anchorage, rotated), 186 (p.178 bar placement), 187 (p.179 section/stirrup types), 188 (p.180 secondary/main beam), 189 (p.181 slab step/sunshade), 190 (p.182 ribs), 191–194 (pp.183–186 beam–column joints, column-focused), 195 (p.187 column size change, no beam content), 196 (p.188 coupler in column + column on transfer beam), 201 (p.193 wall joint + steel beam at lift wall), 202 (p.194 composite column with beam bars).
  - Checked from text only, and skipped as non-beam: PDF 179 (stair), 180 (blank), 181 (appendix cover), 197–200 (waterproofing, walls, wall openings), 203–205 (column dowels in footings, pile splices), 206 (blank), 207–208 (safety chapter, out of scope).
- **Unreadable / uncertain:**
  - Appendix Thai text in tata.txt is badly garbled (missing glyphs). I translated appendix notes from the rendered images instead.
  - Stirrup-hook table headers on p.174 read "180°/90°", while the drawings show 90°/135° hooks. The seismic table header also reads "180°" for a 135° hook.
  - The "100" dimension at the exterior support on p.176: purpose unclear.
  - The exact reference line of the "15 cm" dimension in Fig 2.10.
  - The first-stirrup wording in Fig 2.46 ("s/2 or less than 5 cm").
  - Location of the "L/3–L/4" bottom-lap dimension in the 3-D Fig 2.33: it is measured from the support, but whether from the column face or the centreline is unclear.
  - Side-bar requirement conflict: 2RB9 (p.176) vs 2DB12 (p.178) for depth > 600 mm.
  - Secondary top-bar hierarchy conflict: Fig 2.31 (on top of the primary bars) vs p.180 (cranked under them).

---

## D. Cross-check against the ACI Detailing Manual MNL-66(20) (2026-09-29)

Material is in `references/aci_mnl66/` (drawings BM-1_x … BM-209 and their checklists); findings are in `REVIEW_ACI_MNL66.md`. MNL-66 follows ACI 318-19; EIT 011008 follows ACI 318-11. **Always compare the ACI 318-11 value** before taking an ACI number.

| Topic | DPT / EIT / TATA (Parts A – C) | ACI | Decision / sheet |
|---|---|---|---|
| Special-frame hoop spacing in 2h | DPT 5.2.8.3.2: d/4, 8 db, 24 dt, 300 (verified on the page) | 318-11 21.5.3.2 / 318-19 18.6.4.4: d/4, 6 db, 150. The MNL-66 BM-104 checklist prints the outdated 318-08 values (8 db, 24 dt, 12") | **D1: the stricter of both**, min(d/4, 6 db, 24 dt, 150) (1111/3, 1112 table) |
| Intermediate-frame hooks in 2h | DPT 5.2.7.6: 90° + 6 db; 135° / hook-clip for public or ductile buildings | 318-11 21.3.4.2: hoops in every intermediate frame | **D2: DPT kept**; the 1112 table says "ACI 318: HOOPS" |
| Hoop material | EIT allows RB | ACI: plain bars only for spirals | **D3: DB10 minimum, deformed, in intermediate / special frames** |
| Perimeter integrity | EIT 7.13.2.2 (= 318-11 7.13.2.2) | BM-2 / BM-100: continuous top ≥ 1/6 of the support As⁻ (lap at midspan), bottom ≥ 1/4 of the midspan As⁺ (lap at the support), closed stirrups, bars inside the column core | Added to 1111 note 3 |
| Torsion | EIT 11.5 | BM-102: closed stirrups bt + d past the point needed; longitudinal bars developed at both ends | 1113 note 6 |
| Side-face bars | EIT 10.6.7 (tension half, h > 900 / prints 400); TATA h > 600 | BM-1_3: both faces, full web depth | Both faces, full depth, @ ≤ 250, first bar ≤ 150 below the slab (1113 note 7) |
| U-stirrup + cap tie | DPT 5.2.8.3.6 allows two-piece hoops | Not a closed stirrup for torsion / integrity (318-19 25.7.1.6) | "Not for torsion beams" (1111/4 b) |
| Bottom bars into supports | EIT 12.11.1 | BM checklist: 1/3 simple, 1/4 continuous | 1112/1 note |
| Bars past a beam step | TATA "35 db, Ld" | BM-207: Class B lap where in tension | ≥ 1.3 Ld (1114/2) |
| Lateral support in special hoop zones | DPT 5.2.8.3.3 → the code | EIT 7.10.5.3: corner and alternate bar, ≤ 150 clear | 1111 note 5 |
| Secondary beam ending at a girder | TATA p.180 case 3 (top bars 90° down at the far side), Fig 2.31 (top bars over, hangers) | BM-204: top bars hooked to the far side; ≥ 2 bottom bars hooked; hanger stirrups (min. 4) | **1114/3** (2026-09-30) + 1114 note 6 |
| Beam schedule, lettered bars | — (TATA / DPT give no schedule format) | BM-1: schedule (mark, B × H, top A / L4 / B / C / L5, bottom E / F, side bars, ties TR / rest, types) + placing diagrams; 315R 4.10.2, 5.2.6 | **1115** (2026-09-30): letters A – E, SB, S1 / S2; cut-offs = 1112/1 instead of scheduled L4 / L5 |
| Large step (BM-206) | — | BM-206 | Proposed next work |
