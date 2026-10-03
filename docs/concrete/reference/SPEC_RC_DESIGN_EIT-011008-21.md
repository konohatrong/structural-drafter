# EIT 011008-21 — RC Buildings by Strength Design (digest of the chapters used in the general notes)

**Source:** วสท. 011008-21 *มาตรฐานสำหรับอาคารคอนกรีตเสริมเหล็ก โดยวิธีกำลัง* / EIT Standard 011008-21, 1st revision, November 2021, 210 pp.
- File: `G:\My Drive\##Textbook\EITA04-64.pdf`.
- Based on **ACI 318-11**, in SI units. The ksc (MKS) forms are in Appendix ก.
- It **replaces EIT 1008-38**.

**Scope of this digest.** The chapters that feed the structural-concrete general notes:
- Ch. 1 General, Ch. 3 Materials, Ch. 4 Durability;
- Ch. 5 Concrete quality, mixing and placing; Ch. 6 Formwork, embedded pipes, joints;
- **Ch. 7 Details of reinforcement (hooks, bends, spacing, cover by element, ties, shrinkage steel, integrity)**;
- **Ch. 12 Development and splices**; Ch. 18 Strength evaluation (load test);
- Ch. 19 Seismic, which only refers to DPT 1301/1302-61;
- Appendix ก, the SI vs ksc equations.

Design chapters 8–11 and 13–17, 20 and 21 are not digested.

**Conventions:** [NOTE] = commentary, or a difference from ACI 318-11 found by the reader. "(calc.)" = a ksc conversion not printed in the standard.

**Related documents:**
- `SPEC_CONCRETE_EIT-011014-19.md`: the materials and construction digest.
- `GENERAL_NOTES_STRUCTURAL_CONCRETE.md`: the notes master.

## Items used on the general-notes sheet

| Topic | EIT 011008-21 | Clause |
|---|---|---|
| Min. f'c | 18 MPa | 1.1.1 |
| Drawings must show | Loads, f'c by part and age, bar grade, development and lap lengths and locations, welded/mechanical splices, joints | 1.2.1 |
| Records | Keep ≥ 2 years; temperature record when above 35 °C | 1.3.3, 1.3.4, 3.1.2 |
| Round bars (TIS 20) | Spirals, ties, stirrups only | 3.5.1, 3.5.4 |
| Max. aggregate | 1/5 form width, 1/3 slab, 2/3 clear bar spacing | 3.3.3 |
| f'cr | max(f'c + 1.34 ss, f'c + 2.33 ss − 3.5); no data: + 7.0 / + 8.3 / 1.1 f'c + 5.0 | 5.3.2, T5.2 |
| Sulfate | T5.4: w/cm 0.50 / 0.45 / 0.40; T5.5 magnesium | 5.5.1 |
| Chloride | 0.08 / 0.20 / 1.00 / 0.30 % of cementitious material | T5.6 |
| Sampling | ≥ 1/day, 1/50 m³, 1/250 m²; ≥ 5 batches | 5.7.1 |
| Acceptance | Mean of 3 consecutive tests ≥ f'c; none < f'c − 3.5 MPa | 5.7.2 |
| Cores | 3 per low test; mean ≥ 0.85 f'c, none < 0.75 f'c | 5.7.4 |
| Curing | Moist, > 10 °C, ≥ 7 d (3 d high early strength); pozzolan longer | 5.8.5 |
| Pipes | OD ≤ t/3, ≥ 3 Ø c/c, ≤ 4 % of column area; cover 35 / 20; 0.002 Ac normal to pipes | 6.3 |
| Construction joints | Middle third; girders ≥ 2 × secondary-beam width from the intersection; floor after columns harden | 6.4 |
| Hooks | 180° + 4 db ≥ 60; 90° + 12 db; stirrups 90° + 6/12 db, 135° + 6 db | 7.1 |
| Bends | 6 db (≤ 25), 8 db (28–36), 10 db (43/57); stirrups ≤ 16: 4 db | 7.2, T7.1 |
| **Cover by element** | Earth 75; exposed 50 (≥ 20) / 40 (≤ 16); beams and columns 40; slabs, walls, joists 30 / 20; shells 20 / 15 | **7.7.1** |
| Ties | 6 (≤ 12), 9 (16–20), 10 (25–28), 12 (≥ 32) mm; spacing ≤ 16 db, 48 dt, least dimension | 7.10.5 |
| Shrinkage steel | 0.0025 SR24 / 0.0020 SD30 / 0.0018 SD40, ≥ 0.0014; spacing ≤ 5h, ≤ 400 | 7.12 |
| ld (simplified) | fy ψt ψe / (2.1 λ √f'c) db for ≤ 20 mm, / 1.7 for ≥ 22 mm | 12.2.2 |
| Laps | Class A 1.0 ld / B 1.3 ld ≥ 300; none > 36 mm; compression 0.071 fy db ≥ 300 | 12.13–12.15 |
| Load test | ≥ 56 d, 0.85(1.4D + 1.7L), 24 h; Δ ≤ lt²/(20,000 h) or recovery ≥ 75 % | 18.3–18.4 |

## Misprints found in the source (reading adopted)

| Clause | As printed | Adopted |
|---|---|---|
| Eq. 5-2 | f'c + 2.33 ss − 35 | − 3.5 MPa |
| 6.3.8 | Water in pipes ≤ 300 °C | Probably 30–32 °C: confirm |
| 7.5.2 | d tolerance ± 100 mm (d ≤ 200) | ± 10 mm |
| 7.10.4(จ)(1.5) | Spiral lap 43 db | 48 db (ACI) |
| 7.7.1(ค)(1) | "เหล็กปลอกเดียว" | Spiral |
| 12.3.2 | Constant 0.0003 mm²/N | 0.043 (as in the equation) |
| 12.9.5(b) | Extra stirrups "not exceed" 0.41 bw s / fyt | "Not less than" (ACI) |

---

## PART 1 — GENERAL (หมวด 1 ทั่วไป) / CHAPTER 1 GENERAL REQUIREMENTS (บทที่ 1 ข้อกำหนดทั่วไป)

### 1.1 Scope (ขอบข่าย)
- **1.1.1** Sets minimum requirements for design, material specification and construction of RC structural members, including strength evaluation of existing structures, subject to the Building Control Act, the Engineer Act and related laws.
  - **Specified compressive strength of concrete (กำลังอัดที่กำหนดของคอนกรีต, f'c) shall be not less than 18 MPa** (≈ 183 ksc calc.). Upper limit governed by specific provisions of the standard.
  - [DIFF vs ACI 318-11 1.1.1: ACI minimum f'c = 17 MPa (2500 psi); Thai = 18 MPa.]
- **1.1.2** Special structures (arches, bins, tanks/reservoirs, silos, blast-resistant structures, chimneys, etc.): standard applies only where applicable.
- **1.1.3** Does NOT cover design/driving/boring of concrete piles, nor concrete piers (ตอม่อ) transferring load to soil.
  - [DIFF: ACI 318-11 1.1.6 covers portions of piles/drilled piers embedded in ground; Thai excludes piles and piers entirely.]
- **1.1.4** Does NOT cover design/construction of slabs-on-grade (แผ่นพื้นวางบนดิน), unless the slab transmits vertical or lateral loads from other structure to soil.
- **1.1.5** Seismic design/construction provisions shall be used together with the Building Control law and relevant Department of Public Works and Town & Country Planning (กรมโยธาธิการและผังเมือง, DPT / มยผ.) standards.

### 1.2 Permits and construction drawings (การขออนุญาตและแบบก่อสร้าง)
- **1.2.1** Where a building permit is required, the designer shall prepare drawings (แบบแปลน) and specifications (รายการประกอบแบบแปลน) showing at least:
  - (ก/a) Name of laws, regulations, standards and other criteria used in design.
  - (ข/b) Live load and other loads used in design.
  - (ค/c) Specified compressive strength of concrete at stated ages or stages of construction, for each part of the structure.
  - (ง/d) Specified strength or grade (ชั้นคุณภาพ) of reinforcement.
  - (จ/e) Size and location of structural elements and reinforcement.
  - (ฉ/f) Provisions for dimensional changes from creep, shrinkage and temperature.
  - (ช/g) Anchorage (development) length of reinforcement; location and length of lap splices (การต่อทาบ).
  - (ซ/h) Type and location of welded splices and mechanical connections (ข้อต่อเชิงกล) of reinforcement.
  - (ฌ/i) Details and location of contraction joints (รอยต่อเผื่อร้าว) and expansion joints (รอยต่อขยาย).
  - Where the building falls under controlled engineering practice (งานวิชาชีพวิศวกรรมควบคุม) per the Engineer Act, the calculator/designer shall hold a Civil Engineering professional license (ใบอนุญาตผู้ประกอบวิชาชีพวิศวกรรมควบคุม สาขาวิศวกรรมโยธา) with qualifications per Council of Engineers regulations, and shall sign/certify drawings, specifications and calculations.
  - [DIFF vs ACI 318-11 1.2.1: Thai list omits ACI items on code date, anchors in (e), prestressing force magnitude/location, min f'c at post-tensioning, stressing sequence, and slab-on-grade-as-diaphragm statement. Thai says "contraction and expansion joints" (ACI: contraction or isolation joints). Adds Thai licensed-engineer signature requirement.]
- **1.2.2** Calculations shall be submitted with drawings for permit. If computer/tables/charts used, attach them with design assumptions, input data and results. Model-analysis methods may supplement calculations.

### 1.3 Inspection (การตรวจงาน)
- **1.3.1** Concrete construction shall be inspected per Building Control law, manuals and standards; absent these, inspect throughout all stages by or under supervision of the supervising engineer (วิศวกรควบคุมงาน) or a qualified/authorized inspector.
- **1.3.2** Inspector shall verify conformance with permitted drawings/specifications. Unless otherwise required by law, inspection records (ระเบียนการควบคุมงาน) shall cover:
  - (a) Quantity and proportions of materials, and strength of concrete;
  - (b) Formwork erection, removal and shoring (การค้ำยัน);
  - (c) Placement of reinforcement;
  - (d) Mixing, placing and curing of concrete;
  - (e) Sequence of erection, installation and connection of precast members;
  - (f) Significant construction loads placed on completed floors, members or walls;
  - (g) General progress of work.
- **1.3.3** When temperature during concreting **exceeds 35 °C**, keep a detailed record of temperatures and protective measures used during placing and curing.
  - [DIFF: ACI 318-11 1.3.3 also requires records when ambient falls below 4 °C (40 °F); Thai standard has hot-weather trigger only.]
- **1.3.4** Records per 1.3.2 and 1.3.3 kept by the supervisor during construction and for **at least 2 years** after.
- **1.3.5** For ductile moment-resisting frames (โครงต้านแรงดัดที่มีความเหนียว) designed for earthquake per **Chapter 19**, reinforcement placement and concreting shall be **continuously inspected** by a qualified inspector under the responsible design engineer or an engineer experienced in such supervision.
  - [DIFF: seismic chapter is Ch.19 (ACI 318-11 = Ch.21).]

### 1.4 Approval of special design/construction systems (การพิจารณารับรองการคำนวณออกแบบหรือการก่อสร้างระบบพิเศษ)
- Designer may propose design/construction methods differing from this standard, provided adequacy is shown by successful use, analysis or tests to a committee appointed by the relevant government agency (experts in building structural design). Committee may require tests/other actions; once approved, the method is deemed compliant with this standard.

---

## CHAPTER 2 — SELECTED SYMBOLS AND DEFINITIONS (บทที่ 2 สัญลักษณ์และนิยาม) — cover/reinforcement/material-relevant only

### 2.1 Symbols (units mm, MPa)
- **c_b** — lesser of (a) distance from bar/wire center to nearest concrete surface, (b) half c/c spacing of bars/wires being developed, mm.
- **c_c** — clear cover of reinforcement (ระยะหุ้มว่างของเหล็กเสริม), mm.
- **d_b** — nominal diameter of bar/wire, mm.
- **f'c** — specified compressive strength of concrete, MPa; **f'cr** — required average compressive strength used for mix proportioning, MPa; **f_ct** — average splitting tensile strength of lightweight concrete, MPa; **f_r** — modulus of rupture, MPa.
- **f_y** — specified yield strength of reinforcement, MPa; **f_yt** — specified yield strength of transverse reinforcement, MPa; **f_ya / f_uta** — specified yield / tensile strength of anchor steel, MPa.
- **E_s** — modulus of elasticity of reinforcement and structural steel, MPa; **E_c** — of concrete, MPa.
- **ψ_e** — development-length factor for reinforcement coating (การเคลือบผิว); **ψ_s** — for bar size; **ψ_t** — for bar location.

### 2.2 Definitions (นิยาม)
- **Yield strength (กำลังคราก)** — specified minimum yield strength or yield point of reinforcement, from tension test per **TIS 24 (มอก.24)** or accepted international standard, per clause 3.5.
- **Specified compressive strength of concrete (f'c)** — used in design and evaluation per Chapter 5; in MPa (also under square root).
- **Splitting tensile strength (กำลังดึงแยก, f_ct)** — per **ASTM C496M** as described in **ASTM C330M**.
- **Concrete (คอนกรีต)** — mixture of portland or other hydraulic cement, fine aggregate, coarse aggregate and water, with/without admixtures.
- **Structural concrete** — all concrete for structural purposes, incl. plain and reinforced.
- **Structural lightweight concrete** — contains lightweight aggregate per 3.3, air-dry unit weight per **ASTM C567M ≤ 1,800 kg/m³**. "All-lightweight" = no natural sand; "sand-lightweight" = all fine aggregate is normal-weight sand.
- **Lightweight aggregate (มวลรวมเบา)** — dry loose unit weight **< 1,100 kg/m³**.
- **Aggregate (มวลรวม)** — granular material (sand, gravel, crushed stone, iron blast-furnace slag) used with cementing material to form concrete or mortar.
- **Cementitious material (วัสดุซีเมนต์)** — materials per Ch.3 having cementing value in concrete, alone (portland cement, hydraulic cement, expansive cement) or combined with fly ash, pozzolans, natural calcined/raw, silica fume, ground granulated blast-furnace slag.
- **Admixture (สารผสมเพิ่ม)** — material other than water, aggregate or cement, added before/during mixing to modify properties.
- **Plain concrete (คอนกรีตล้วน)** — no reinforcement or less than minimum for RC. **Reinforced concrete** — at least minimum reinforcement per this standard, designed assuming both materials act together. **Precast concrete** — cast elsewhere than final position.
- **Reinforcement (เหล็กเสริม)** — material conforming to 3.5.
- **Deformed reinforcement (เหล็กเสริมข้ออ้อย)** — deformed bars, bar mats, deformed wire, deformed welded wire fabric conforming to 3.5.3.
- **Plain reinforcement (เหล็กเสริมผิวเรียบ)** — round bars or reinforcement not meeting the definition of deformed.
- **Tie (เหล็กปลอก)** — loop of bar/wire enclosing longitudinal bars; circular, rectangular or polygonal. **Spiral (เหล็กปลอกเกลียว)** — continuously wound cylindrical helix. **Stirrup (เหล็กลูกตั้ง)** — resists shear/torsion; bars, wire or welded wire fabric (plain or deformed), single leg or bent L, U or rectangular, perpendicular or angled to longitudinal bars ("stirrup" usually for flexural members, "tie" for compression members).
- **Development length (ระยะฝังพอ)** — embedment required to develop design strength at a critical section. **Embedment length (ระยะฝัง)** — embedment provided beyond a critical section.
- **Column (เสา)** — height-to-least-lateral-dimension ratio **≥ 3**, primarily axial compression. **Pedestal (แท่นตอม่อ)** — upright compression member, ratio **< 3**.
- **Wall (กำแพง)** — member, usually vertical, used to enclose or separate spaces.
- **Ductile steel element** — ASTM tensile-test elongation **≥ 14%** and reduction of area **≥ 30%**; **brittle steel element** — elongation < 14% or reduction of area < 30% or both.
- **Tension-controlled section** — net tensile strain in extreme tension steel at nominal strength **≥ 0.005**. **Compression-controlled section** — ≤ compression-controlled strain limit (net tensile strain at balanced strain conditions).
- **Extreme tension steel** — reinforcement farthest from extreme compression fiber. **Effective depth d** — extreme compression fiber to centroid of tension reinforcement.
- **Dead / live / service load** — per the building regulations (ประมวลข้อบังคับอาคาร), unfactored. **Factored load** — multiplied by load factors for strength design.
- **Anchor definitions**: anchor group (spacing < 3× embedment); cast-in anchor (headed bolt, headed stud, hooked J/L bolt installed before casting); post-installed (expansion, undercut, adhesive); **adhesive anchor** hole diameter **≤ 1.5 × anchor diameter**; anchor reinforcement vs. supplementary reinforcement; edge distance; ICC-ES evaluation reports (anchors evaluated per ACI standards).
- **Five-percent fractile** — 90% confidence that 95% of actual strengths exceed nominal.
- [NOTE: No definitions of "cover", "exposure category/class" appear in Ch.2 (pp.28–32).]

---

## PART 2 — MATERIALS (หมวด 2 บทกำหนดสำหรับวัสดุก่อสร้าง) / CHAPTER 3 MATERIALS (บทที่ 3 วัสดุก่อสร้าง)

### 3.1 Testing of materials (การทดสอบวัสดุ)
- **3.1.1** Responsible engineer may order testing of any material at any time to verify conformance.
- **3.1.2** Tests of concrete and other materials per Thai Industrial Standards (มาตรฐานผลิตภัณฑ์อุตสาหกรรม, TIS/มอก.) or other accepted standards. Complete test records kept available for inspection during construction and **≥ 2 years** after completion.

### 3.2 Cementitious materials (วัสดุประสาน)
| Clause | Material | Standard |
|---|---|---|
| 3.2.1 | Portland cement (ปูนซีเมนต์ปอร์ตแลนด์) | TIS 15 (มอก.15) |
| 3.2.2 | Portland pozzolan cement (ปูนซีเมนต์ปอร์ตแลนด์ปอซโซลาน) | TIS 849 |
| 3.2.3 | Portland blast-furnace slag cement (ปูนซีเมนต์ปอร์ตแลนด์กากถลุงจากเตาถลุงแบบพ่นลม) | TIS 2587 |
| 3.2.4 | Hydraulic cement (ปูนซีเมนต์ไฮดรอลิก) | TIS 2594 |
| 3.2.5 | Coal fly ash (เถ้าลอยจากถ่านหิน) | TIS 2135-2545 |
| 3.2.5 [sic, duplicate no.] | Silica fume (ซิลิกาฟูม) | ASTM C1240 |
(Table compiled from clause text; not a table in the source.)
- **3.2.6** Cementitious materials used in the work shall correspond to those on which mix proportioning was based (clause 5.2).
- [DIFF: ACI 318-11 3.2.1 uses ASTM C150/C595/C1157/C618/C989/C1240; Thai substitutes TIS equivalents; no separate GGBFS (ASTM C989) clause.]

### 3.3 Aggregates (มวลรวมที่ใช้เป็นส่วนผสมของคอนกรีต)
- **3.3.1** Aggregates per **TIS 566 (มอก.566)**. [ACI: ASTM C33 / C330.]
- **3.3.2** Clean, hard, durable; free of harmful chemicals and excessive clay/fine dust coatings that impair hydration strength gain or paste-aggregate bond.
- **3.3.3** Nominal maximum aggregate size shall not exceed:
  - (a) **1/5** of narrowest dimension between sides of forms;
  - (b) **1/3** of slab depth (thickness);
  - (c) **2/3** of minimum clear spacing between individual bars or bundles.
  - May be waived if concrete can be consolidated without honeycomb or voids.
  - [DIFF: ACI 318-11 3.3.2(c) = **3/4** of minimum clear spacing (also includes tendons/ducts); Thai = **2/3** — stricter.]

### 3.4 Water (น้ำ)
- **3.4.1** Mixing water clean, per **DPT 1212 (มยผ. 1212)**. [ACI: ASTM C1602.]
- **3.4.2** Mixing water, incl. water from aggregate free moisture, for prestressed concrete or concrete with embedded aluminum shall not contain deleterious chloride amounts; see clause 5.5.2. [NOTE: cross-ref 5.5.2 is outside this range.]

### 3.5 Reinforcement (เหล็กเสริม)
- **3.5.1** Main reinforcement shall be **deformed bars (เหล็กข้ออ้อย)**; **round/plain bars (เหล็กเส้นกลม) permitted for spirals, individual ties and stirrups**. Structural steel shapes, steel pipe or tubing may be used as specified in this standard.
  - [DIFF: ACI 318-11 3.5.1 permits plain reinforcement only for spirals (and prestressing steel); Thai also allows plain bars for ties and stirrups.]
- **3.5.2** Where welding is used, **type and location of welds shall be shown on drawings**, together with the welding procedure standard. [ACI refers to AWS D1.4; Thai does not name a welding standard here.]
- **3.5.3 Deformed bars (เหล็กข้ออ้อย)**
  - (a) Shall conform to **TIS 24 (มอก.24)**.
  - (b) Yield strength determination:
    - Specified f_y **< 400 MPa**: f_y = stress corresponding to strain of **0.5%**.
    - Specified f_y **> 400 MPa**: f_y = stress corresponding to strain of **0.35%**.
  - [DIFF: ACI 318-11 3.5.3.2 threshold is 420 MPa (60 ksi) for 0.35% strain; Thai threshold 400 MPa. The standard does not list bar grades (e.g. SD30/SD40/SD50) in this range; grade designations come from TIS 24 itself. Case f_y exactly 400 MPa not explicitly addressed.]
- **3.5.4 Round (plain) bars (เหล็กเส้นกลม)**
  - (a) Use **only** for spirals, ties and stirrups.
  - (b) Shall conform to **TIS 20 (มอก.20)**.
- **3.5.5** Welded steel wire fabric (ตะแกรงลวดเหล็กเชื่อม) per **TIS 737**.
- **3.5.6** Structural steel shapes or steel pipe per **TIS 1227**.
- [NOTE: no clauses on epoxy-coated/galvanized bars, low-alloy weldable bars (ASTM A706), headed bars, or steel fibers — these ACI 318-11 3.5 items are absent.]

### 3.6 Admixtures (สารผสมเพิ่ม)
- **3.6.1** Every use of admixtures requires prior approval of the engineer or inspector.
- **3.6.2** Admixture shall maintain the same composition and performance throughout the work as the product used to establish mix proportions per clause 5.2.
- **3.6.3** **Calcium chloride or chloride-containing admixtures prohibited** in: prestressed concrete; concrete with embedded aluminum; concrete cast against stay-in-place galvanized steel forms.
- **3.6.4** Air-entraining admixtures (สารกระจายกักฟองอากาศ) per **TIS 874**. [ACI: ASTM C260.]
- **3.6.5** Water-reducing, retarding and accelerating admixtures per **TIS 733, ASTM C494**.
- **3.6.6** Admixtures for flowing concrete (คอนกรีตไหล) per **TIS 985, ASTM C1017**.
- [NOTE: no fly ash/pozzolan/slag admixture clauses here (covered as cementitious in 3.2).]

### 3.7 Storage of materials (การเก็บรักษาวัสดุก่อสร้าง)
- Cement and aggregates stored to prevent deterioration or contamination. Deteriorated or contaminated material shall never be used in concrete.
- [NOTE — footnote p.35: Further details for this chapter per **EIT 1014-46 (วสท. 1014-46)** "Standard Specification for Materials and Construction of Concrete Structures".]

---

## PART 3 — CONSTRUCTION CRITERIA (หมวด 3 เกณฑ์กำหนดในการก่อสร้าง) / CHAPTER 4 DURABILITY (บทที่ 4 ข้อกำหนดสมบัติของคอนกรีตตลอดอายุการใช้งาน — "Requirements for concrete properties over service life")

**KEY FINDING — [DIFF, major]: This chapter does NOT adopt ACI 318-11 Chapter 4. There are NO exposure categories/classes (F, S, P, C), NO tables, NO numeric limits for max w/cm, min f'c, air content, chloride-ion content, or sulfate/cement type.** It is qualitative guidance only and defers to other standards.

### 4.1 Scope (ขอบเขต)
- Requirements in this chapter are **general recommendations only (คำแนะนำทั่วไป)**. Details and requirements shall be taken from **EIT 1014 (วสท. 1014), Chapter 1**, and **DPT 1332 (มยผ. 1332)**.

### 4.2 Concrete property requirements over service life
Plant-produced or site-mixed concrete should have properties in each state as follows ("should" — advisory):
- **4.2.1 Fresh concrete (คอนกรีตสด)** — good workability and form-filling, acceptable slump/workability loss; i.e. (a) placeability/flow suitable to the construction; (b) no segregation causing non-uniform quality; (c) no blocking by aggregate at forms or reinforcement during placing.
- **4.2.2 Plastic concrete (คอนกรีตในสถานะพลาสติก)** — (a) no or little bleeding; (b) no or little plastic settlement; (c) no plastic-shrinkage cracking; (d) easy finishing.
- **4.2.3 Early-age concrete (คอนกรีตอายุต้น)** — (a) no or little autogenous shrinkage, not causing cracking from restraint stress; (b) no thermal cracking; (c) adequate early compressive strength.
- **4.2.4 Hardened concrete (คอนกรีตที่แข็งตัวแล้ว)** — required long-term properties:
  - (a) **Mechanical**: compressive strength sufficient for design-load stresses with appropriate safety factor; modulus of elasticity not less than value used in structural design.
  - (b) **Durability**: depends on exposure environment; concrete shall be of high quality, **low permeability, and with adequate cover to reinforcement (ระยะหุ้มเหล็กเสริม) for each environment type and severity**, to resist deterioration and prevent reinforcement corrosion. Consider:
    1. **Expansion under wet exposure** — expansion by standard test not so high as to damage adjacent members.
    2. **Drying shrinkage** — not excessive to cause visible cracks; limit depends on restraint, tensile strength/crack resistance, and other properties (e.g. fatigue).
    3. **Carbonation** — carbonation depth by standard accelerated test not exceeding specified value; carbonation front **shall not reach the outermost reinforcement before the design maintenance-free service life**.
    4. **Reinforcement corrosion** — low permeability to limit ingress of water, gases, solutions, ions; may be assessed by water-permeability test with specified maximum; permissible permeability may vary with cover (greater cover → higher permeability allowed); also **water-soluble chloride at outermost reinforcement shall not exceed specified value** [no number given].
    5. **Alkali-aggregate reaction** — no risk of alkali-silica, alkali-silicate or alkali-carbonate reaction; if risk exists, cement alkali content shall not exceed specified limit; otherwise use other cementitious materials (e.g. fly ash) to reduce alkalinity.
    6. **Abrasion** — no severe abrasion within design life; test method for abrasion resistance should exist; requirement depends on member type and environment.
    7. **Sulfate exposure** — concrete shall be sulfate resistant; expansion (% of initial specimen length) and/or mass loss from standard sulfate expansion/weight-loss test not exceeding specified value within specified period [no numbers given].
    8. **Other chemicals** (acids, salts) — % mass loss vs. initial not exceeding specified value in specified period.
    9. **Freeze–thaw** — for very cold environments (below freezing), concrete shall resist freeze–thaw cycles with loss of modulus of elasticity not exceeding a specified % of initial.
    10. **Biological deterioration** — % loss of compressive strength vs. initial by specified accelerated degradation test not exceeding specified value.
- [NOTE: all "specified values" in 4.2.4 are left to EIT 1014 / DPT 1332; none are given in this standard. For a General Notes drawing, exposure-based limits (w/cm, min f'c, chloride, cover by exposure) must be sourced from EIT 1014 Ch.1 and DPT 1332, or from ACI 318 if the office adopts it.]

---

## Summary of differences vs ACI 318-11 (pp.13–40)
| Item | EIT 011008-21 | ACI 318-11 |
|---|---|---|
| Min f'c | 18 MPa | 17 MPa (2500 psi) |
| Piles / piers | Excluded | Partially covered (1.1.6) |
| Temperature records | > 35 °C only | < 4 °C or > 35 °C |
| Seismic chapter | Ch.19 | Ch.21 |
| Cement / aggregate / water stds | TIS 15, 849, 2587, 2594, 2135; TIS 566; DPT 1212 | ASTM C150, C595, C1157, C618, C989; C33/C330; C1602 |
| Max aggregate vs bar clear spacing | 2/3 | 3/4 |
| Plain bars permitted | Spirals, ties, stirrups (TIS 20) | Spirals only |
| Deformed bars | TIS 24 | ASTM A615/A706 etc. |
| f_y at 0.35% strain threshold | > 400 MPa (else 0.5% strain) | > 420 MPa |
| WWF / structural steel | TIS 737 / TIS 1227 | ASTM A1064 etc. / A36 etc. |
| Admixtures | TIS 874, TIS 733 + ASTM C494, TIS 985 + ASTM C1017 | ASTM C260, C494, C1017 |
| Durability / exposure | Qualitative only; refers to EIT 1014 & DPT 1332; no tables | Exposure categories F/S/P/C, Tables 4.2.1, 4.3.1 |
| Record retention (inspection & tests) | ≥ 2 years | 2 years |

---

## Chapter 5: Concrete quality, mixing and placing (คุณภาพของคอนกรีต การผสม และการเทคอนกรีต)

### 5.1 General
- **5.1.1** Proportion concrete for a required average compressive strength (กำลังอัดเฉลี่ยที่ต้องการ) f'cr not less than that in 5.3.2; satisfy durability of Chapter 4; control production so strength test results below the specified strength (กำลังอัดที่กำหนด) f'c occur as rarely as possible, per 5.7.2.
- **5.1.2** Drawings used for building permit or construction must clearly show f'c of the structural concrete.
- **5.1.3** f'c is based on tests of **cylinders 150 mm diameter x 300 mm high**, per 5.7.2.
  - ACI diff: ACI 318-11 also permits 100 x 200 mm cylinders; EIT specifies only 150 x 300 mm.
- **5.1.4** Unless otherwise specified, f'c is based on **28-day** tests. If a different test age is intended, it must be stated clearly on drawings and specifications.
- **5.1.5** Where 11.2 and 12.2.4(d) permit use of splitting tensile strength (กำลังดึงแยก) fct of lightweight-aggregate concrete, fct must be established by tests per **ASTM C330** (printed "ASTM 330") to obtain fct corresponding to f'c.
- **5.1.6** Splitting tensile tests shall **not** be used as a basis for field acceptance of concrete.

### 5.2 Selection of concrete proportions (การเลือกส่วนผสมของคอนกรีต)
- **5.2.1** Proportions shall give:
  - (a) workability and consistency so concrete fills the forms and surrounds reinforcement under the placing conditions, without segregation or excessive bleeding;
  - (b) durability per Chapter 4;
  - (c) conformance to strength-test requirements of 5.7.
- **5.2.2** Where different materials are used for different portions of the work, each combination shall be evaluated.
- **5.2.3** Proportions, including water-cement ratio, shall be established from field experience and/or trial mixtures with the job materials per 5.3, except as permitted in 5.4 or 5.5.

### 5.3 Proportioning based on field experience and/or trial mixtures

#### 5.3.1 Standard deviation (ความเบี่ยงเบนมาตรฐาน)
- (a) Where a concrete production facility (หน่วยผลิตคอนกรีต) has test records, compute standard deviation from records that:
  - (1) represent materials, QC procedures and conditions similar to those expected; changes in materials/proportions within the record shall not be more restricted than for the proposed work;
  - (2) represent concrete produced to meet a specified strength **within 7 MPa** [≈ 70 ksc] of f'c for the proposed work;
  - (3) consist of **at least 30 consecutive tests**, or **two groups of consecutive tests totalling at least 30 tests** (test as defined in 5.7.1), except as in 5.3.1(b).
- (b) Where no records per (a) exist but a record of **15 to 29 consecutive tests** exists, standard deviation = calculated s x modification factor from Table 5.1.

**Table 5.1 Modification factor for standard deviation (แฟกเตอร์ปรับค่าความเบี่ยงเบนมาตรฐาน)**

| Number of tests | Modification factor for standard deviation* |
|---|---|
| Fewer than 15 | Use Table 5.2 |
| 15 | 1.16 |
| 20 | 1.08 |
| 25 | 1.03 |
| 30 or more | 1.00 |

\* The modified standard deviation is used to determine f'cr per 5.3.2(a). (Interpolate for intermediate numbers of tests: not stated in EIT; ACI 318-11 permits interpolation.)

Test records are acceptable when they satisfy 5.3.1(a) and 5.3.1(b) and come from a single record of consecutive tests spanning **not less than 45 days**.

#### 5.3.2 Required average compressive strength for mix design
- (a) f'cr = the larger of:

  - (5-1) f'cr = f'c + 1.34 ss
  - (5-2) f'cr = f'c + 2.33 ss − 35 (as printed)

  where ss = standard deviation (MPa) from 5.3.1(a) or 5.3.1(b); f'c, f'cr in MPa.
  - [NOTE/probable typo] "− 35" is dimensionally inconsistent with MPa; ACI 318-11 (SI) uses **− 3.5 MPa** (≈ 35 ksc; the "35" appears carried over from the older ksc edition). Interpret as −3.5 MPa.
  - ACI diff: ACI 318-11 Table 5.3.2.1 applies Eq. (5-2) only for f'c ≤ 35 MPa and uses f'cr = 0.90 f'c + 2.33 ss for f'c > 35 MPa; EIT gives no separate high-strength equation.
- (b) Where no field strength records exist for computing ss per 5.3.1(a)/(b), take f'cr from Table 5.2, with documentation per 5.3.3.

**Table 5.2 Required average compressive strength when data are not available to establish a standard deviation**

| Specified compressive strength f'c (MPa) | Required average compressive strength f'cr (MPa) |
|---|---|
| Less than 21 | f'c + 7.0 |
| 21 to 35 | f'c + 8.3 |
| Over 35 | 1.1 f'c + 5.0 |

(Same as ACI 318-11 Table 5.3.2.2.)

#### 5.3.3 Documentation of average compressive strength (การเก็บหลักฐาน)
Documentation that proposed proportions produce average strength ≥ f'cr shall consist of at least one field strength test record, several strength test records, or laboratory trial mixtures. Records shall be **not more than 2 years old**.
- (a) Several strength test records may be used where materials and conditions are similar to those expected; changes in materials/proportions/conditions not more restricted than for the proposed work. Records may have fewer than 30 tests but **not fewer than 10 consecutive tests** over **not less than 45 days**. Required proportions may be established by interpolation between strengths and proportions of **two or more** test records.
- (b) Where no acceptable field record exists, proportions may be established by trial mixtures meeting:
  - (1) materials identical to those for the proposed work;
  - (2) trial mixtures with a range of proportions producing strengths encompassing f'cr, and meeting durability of Chapter 4;
  - (3) slump within the range specified for the work; for air-entrained concrete (คอนกรีตกักกระจายฟองอากาศ), air content within the specified tolerance;
  - (4) for each proportion, at least **3 standard cylinders** made and cured per **TIS 409 (มอก. 409)**, tested for f'c at **28 days** or the designated test age;
  - (5) proportions selected from the test results shall give f'cr and satisfy Chapter 4 durability.
  - ACI diff: ACI 318-11 5.3.3.2 requires at least three mixtures (range of w/cm) and slump within ±20 mm of max permitted, air within ±0.5%; EIT gives no numeric tolerances here. ACI references ASTM C192/C39; EIT references TIS 409.

### 5.4 Proportioning by water-cementitious material ratio (อัตราส่วนน้ำต่อวัสดุประสาน)
- **5.4.1** If data per 5.3 are not available, proportions may be based on the w/cm ratios of Table 5.3, **if approved by the engineer**.

**Table 5.3 Recommended water-cementitious material ratios for concrete mix design**

| Specified compressive strength f'c (MPa) | w/cm by weight: non-air-entrained concrete | w/cm by weight: air-entrained concrete |
|---|---|---|
| 18 | 0.67 | 0.54 |
| 21 | 0.58 | 0.46 |
| 24 | 0.51 | 0.40 |
| 28 | 0.44 | 0.35 |
| 32 | 0.38 | * |
| 35 | * | * |

\* Use the method of 5.3.

- **5.4.2** Table 5.3 applies only to concrete made with portland cement per **TIS 15 (มอก. 15)** or hydraulic cement per **TIS 2594 (มอก. 2594)**; it shall **not** be used for lightweight-aggregate concrete or concrete with any admixture other than air-entraining agent. Otherwise use 5.3.
- **5.4.3** Proportions by Table 5.3 must satisfy Chapter 4 durability and the strength evaluation/acceptance of 5.7.
- ACI diff: ACI 318-11 has no w/cm-vs-strength table (removed after ACI 318-89); ACI 318-11 5.4 uses Table 5.3.2.2 instead. Table 5.3 is an EIT-specific provision.

### 5.5 Requirements for concrete in special exposure conditions (สภาวะพิเศษ)
- **5.5.1** Concrete exposed to sulfate-containing solutions or soils shall comply with Table 5.4 (sodium sulfate) and Table 5.5 (magnesium sulfate).

**Table 5.4 Requirements for concrete resistant to sodium sulfate (โซเดียมซัลเฟต)**

| Exposure severity | Sulfate (SO4) in water (ppm) | Water-soluble sulfate in soil (% by weight of soil) | Cement type / cementitious materials to use | Max w/cm |
|---|---|---|---|---|
| Normal (สภาวะทั่วไป) | < 150 | < 0.1 | No restriction | - |
| Moderate (ปานกลาง) | 150 – 1,500 | 0.1 – 0.2 | Type 2 or 5, or Type 1 with pozzolan | 0.50 |
| Severe (รุนแรง) | 1,500 – 10,000 | 0.2 – 2.0 | Type 5, or Type 1 with pozzolan | 0.45 |
| Very severe (รุนแรงมาก) | > 10,000 | > 2.0 | Type 5 with pozzolan, or Type 1 with pozzolan | 0.40 |

**Table 5.5 Requirements for concrete resistant to magnesium sulfate (แมกนีเซียมซัลเฟต)**

| Exposure severity | Magnesium sulfate in water (ppm) | Cement type / cementitious materials to use | Max w/cm |
|---|---|---|---|
| Normal | < 300 | No restriction | - |
| Moderate | 300 – 1,000 | Type 1, 2 or 5 | 0.50 |
| Severe | 1,000 – 3,000 | Type 5 | 0.45 |
| Very severe | 3,000 – saturation | Type 5 | 0.40 |

(Cement types are Thai TIS 15 portland cement types 1/2/5, corresponding to ASTM C150 Types I/II/V.)

[NOTE] Recommendations (ข้อแนะนำ):
1. Pozzolan should not partially replace cement in concrete exposed to magnesium sulfate, as it deteriorates faster than plain-cement concrete.
2. Where w/cm < 0.35 is required, the mix designer must consider autogenous shrinkage.

ACI diff: ACI 318-11 places sulfate requirements in Ch. 4 (Table 4.3.1, classes S0–S3) with same sulfate thresholds but max w/cm 0.50/0.45/0.45 and minimum f'c (28/31/31 MPa); EIT uses 0.40 for very severe, has no min f'c here, and adds a separate magnesium-sulfate table.

- **5.5.2** To protect reinforcement from chloride corrosion, the maximum initial chloride ion content in the concrete mix (excluding chloride from the environment) shall not exceed Table 5.6.

**Table 5.6 Maximum total chloride content permitted in concrete mix**

| Type of construction | Max acid-soluble chloride ion (Cl⁻) in concrete mix (% by weight of cementitious material) |
|---|---|
| Prestressed concrete | 0.08 |
| Reinforced concrete exposed to chloride in service, e.g., sea-retaining wall | 0.20 |
| Reinforced concrete that will be dry or protected from moisture in service | 1.00 |
| Other reinforced concrete | 0.30 |

Remark (หมายเหตุ): acid-soluble chloride testing per **ASTM C1152/C1152M** (Standard test method for acid-soluble chloride in mortar and concrete).
[NOTE] Recommendation: in practice, total chloride may be measured on fresh concrete together with the slump test, or on hardened concrete per ASTM C1152/C1152M.

ACI diff: ACI 318-11 Table 4.3.1 limits **water-soluble** chloride by weight of **cement** (ASTM C1218): 0.06 prestressed, 0.15 (C2), 1.00 (C0), 0.30 (C1). EIT uses acid-soluble by weight of cementitious material with 0.08 / 0.20.

### 5.6 Reduction of required average strength f'cr
If data during construction show f'cr substantially exceeds f'c, f'cr may be reduced provided:
- **5.6.1** at least **30 tests** are available with average exceeding that required by 5.3.2(a) using ss per 5.3.1(a); or
- **5.6.2** **15 to 29 tests** are available with average exceeding 5.3.2(a) using ss per 5.3.1(b); and
- **5.6.3** durability requirements of Chapter 4 are met.

### 5.7 Evaluation and acceptance of concrete (การประเมินผลและการยอมรับงานคอนกรีต)

#### 5.7.1 Frequency of testing
- (a) Samples for strength tests of each class of concrete: **not less than once per day** concrete is placed, **nor less than once per 50 m³** of concrete, **nor less than once per 250 m²** of slab or wall surface area placed. Sampling per **ASTM C172**.
  - ACI diff: ACI 318-11 5.6.2.1 uses once per 110 m³ (150 yd³) and once per 460 m² (5000 ft²); EIT is more stringent.
- (b) If total number of tests for a class per (a) would be **fewer than 5**, tests shall be made from **at least 5 randomly selected batches**, or from each batch if fewer than 5 are used.
- (c) If total quantity of a class is **less than 30 m³**, the supervising engineer may waive strength tests if adequate evidence of satisfactory strength is provided.
  - ACI diff: ACI 318-11 5.6.2.3 threshold is 38 m³ (50 yd³).
- (d) A strength test (ผลการทดสอบแต่ละครั้ง) = **average of at least 2 cylinders** from the same batch, tested at **28 days** or the designated age.
  - ACI diff: ACI 318-11 5.6.2.4: two 150 x 300 mm or three 100 x 200 mm cylinders.

#### 5.7.2 Standard-cured specimens and acceptance criteria
- Specimens: prepared and cured per **DPT 1208 (มยผ. 1208)** (making and curing cylinders in the field); tested per **DPT 1210 (มยผ. 1210)** (compressive strength of cylinders).
- Strength of each class is satisfactory when **both**:
  1. every arithmetic average of any **3 consecutive strength tests ≥ f'c**; and
  2. **no individual strength test falls below f'c by more than 3.5 MPa** [≈ 35 ksc].
- ACI diff: ACI 318-11 5.6.3.3(b) uses 3.5 MPa for f'c ≤ 35 MPa and 0.10 f'c for f'c > 35 MPa; EIT uses 3.5 MPa for all strengths. ACI references ASTM C31/C39.

#### 5.7.3 Field-cured specimens (แท่งทรงกระบอกที่บ่มในสนาม)
- The supervising engineer may require strength tests of field-cured cylinders to check adequacy of curing and protection. Field-cured cylinders per DPT 1208, from the same sample and moulded at the same time as the laboratory-cured cylinders.
- If field-cured strength < **85%** of companion laboratory-cured strength, curing/protection procedures shall be improved. The 85% limit need not apply if field-cured strength exceeds f'c by **more than 3.5 MPa** [≈ 35 ksc].

#### 5.7.4 Investigation of low-strength test results
If laboratory-cured strength falls below f'c by more than 3.5 MPa, or field-cured tests (5.7.3) indicate deficient curing, steps shall be taken to ensure load-carrying capacity is not jeopardized, in this order:
- (a) If low strength is confirmed and calculations indicate load-carrying capacity is significantly reduced, drill cores from the area in question and test per DPT 1210; **3 cores for each strength test** below the criterion.
- (b) Concrete in the area is considered structurally adequate if the **average of 3 cores ≥ 85% of f'c** and **no single core < 75% of f'c**.
- (c) If (b) is not met and structural adequacy remains in doubt, the responsible engineer may order load tests or take other appropriate action.
- ACI diff: ACI 318-11 5.6.5 cores per ASTM C42 with moisture conditioning and permits retesting of erratic core locations; EIT references DPT 1210 and omits conditioning/retest provisions.

### 5.8 Preparation, mixing and placing of concrete

#### 5.8.1 Preparation before placing
- (a) Clean all mixing and conveying equipment; remove all debris from forms; coat form faces with oil or suitable release agent; wet masonry fillers in contact with concrete; reinforcement clean and free of deleterious coatings.
- (b) Remove water from place of deposit before placing, unless concrete is placed underwater by tremie or approved by the engineer.
- (c) Before placing new concrete against hardened concrete, remove laitance and unsound material.

#### 5.8.2 Mixing
- (a) Mix until uniform distribution of materials; discharge completely before remixing the mixer.
- (b) Ready-mixed concrete shall be mixed and delivered per **TIS 213 (มอก. 213)**.
- (c) Job-mixed concrete: approved mixer, rotated at manufacturer's recommended speed; mixing **at least 1½ minutes** after all materials are in the drum, unless a shorter time is shown satisfactory by TIS 213 mixer-uniformity tests. Keep records of: number of batches, proportions of materials, approximate location of final deposit, date and time of mixing and placing.

#### 5.8.3 Conveying
- (a) Convey from mixer to place of deposit by methods preventing segregation or loss of materials.
- (b) Conveying equipment shall be efficient, not cause segregation, and not cause interruptions long enough to allow loss of plasticity between successive increments (cold joints).

#### 5.8.4 Depositing (การเทคอนกรีต)
- (a) Deposit as near final position as practicable to avoid segregation from rehandling or flowing. Place at a rate such that concrete remains plastic and flows readily between bars and into all parts of the form. Do **not** use concrete that has partially hardened, is contaminated by foreign material, or has been retempered/remixed after initial set, unless approved by the engineer.
- (b) Once placing starts, carry it on as a continuous operation until a panel or section is completed, or to predetermined joints; no stopping unless permitted by the engineer or per 6.4. Where joints are required, comply with 6.4.
- (c) Consolidate thoroughly by suitable means around reinforcement and embedded items and into form corners.

#### 5.8.5 Curing (การบ่มคอนกรีต)
- (a) Maintain concrete **above 10 °C** and in a moist condition for **at least 7 days** after placement; **high-early-strength concrete at least 3 days**, unless accelerated curing per (b). Concrete containing pozzolan (e.g., fly ash) shall be cured longer than plain portland-cement concrete (no duration specified).
- (b) Accelerated curing (high-pressure steam, atmospheric-pressure steam, heat and moisture, or other accepted process) may be used to accelerate strength gain and reduce curing time. Compressive strength at the load stage considered shall be at least the design strength required at that stage, and durability at least equivalent to curing per (a).
- (c) Where required to ensure satisfactory curing, the engineer may require supplementary strength tests per 5.7.3.
- EIT adds the pozzolan note (not in ACI 318-11 5.11).

#### 5.8.6 Hot-weather requirements (อากาศร้อน)
During hot weather, give proper attention to ingredients, production, conveying, placing, protection and curing to prevent excessive concrete temperature or water evaporation that could impair required strength, serviceability or durability. No numerical temperature limits given.
- ACI diff: EIT has **no cold-weather clause** (ACI 318-11 5.12). Hot-weather clause corresponds to ACI 318-11 5.13.

---

## Chapter 6: Formwork, embedded pipes and construction joints (แบบหล่อคอนกรีต ท่อที่ฝัง และรอยต่อก่อสร้าง)

### 6.1 Design of formwork
- **6.1.1** Forms shall produce members conforming to shapes, lines and dimensions on drawings and specifications; be substantial and sufficiently tight to prevent mortar leakage; be properly braced/tied to maintain position and shape during placing.
- **6.1.2** Formwork design shall consider:
  - (a) rate and method of placing concrete;
  - (b) construction loads, including vertical, horizontal and impact loads from placing;
  - (c) lateral pressure of fresh concrete on forms;
  - (d) selection of materials;
  - (e) deflection and camber allowance;
  - (f) shoring/bracing: vertical, horizontal and diagonal;
  - (g) splicing of shores;
  - (h) loads on the ground or on previously placed concrete structure.
  - ACI diff: items (d)–(h) are EIT additions/expansions of ACI 318-11 6.1.6 (which lists rate/method, construction loads, and special requirements for shells/folded plates etc.).

### 6.2 Removal of forms and shores (การถอดแบบหล่อคอนกรีตและค้ำยัน)*
- **6.2.1** During construction, no construction loads shall be placed on, nor forms/shores removed from, any part of the structure until that part, together with remaining forms and shoring, has sufficient strength to safely support its own weight and loads. Strength may be shown by structural analysis using field-cured cylinder test data, the loads, and strength of forms and shoring system.
- **6.2.2** No construction load exceeding the design value shall be placed on any unshored portion unless analysis shows adequate strength for the additional load.
- **6.2.3** Remove forms considering safety and serviceability; concrete must have sufficient strength not to be damaged by form removal or afterwards.
- **6.2.4** Prestressed concrete: forms not removed until sufficient prestress has been applied to carry dead load and construction loads.
- \* [NOTE] Footnote: further details on formwork and shoring design in **EIT 1014-19 (วสท. 1014-19)**.
- No minimum stripping times/strengths are specified. ACI diff: ACI 318-11 6.2.2 also requires the construction/removal/reshoring procedure to be defined (6.2.2.1); EIT does not explicitly mention reshoring.

### 6.3 Embedded pipes and conduits (ท่อที่ฝังในคอนกรีต)
- **6.3.1** With engineer's approval, pipes of any material not harmful to concrete and complying with 6.3 may be embedded; they shall **not** be considered to replace displaced concrete structurally (except per 6.3.6).
- **6.3.2** **Aluminum** conduits/pipes shall not be embedded unless coated or covered to prevent aluminum–concrete and aluminum–steel reaction.
- **6.3.3** Conduits, pipes and sleeves passing through slabs, walls or beams shall not significantly impair member strength.
- **6.3.4** Conduits, pipes and fittings embedded in columns shall not displace more than **4% of the column cross-sectional area** used for strength calculation or required for fire protection.
- **6.3.5** Unless shown on structural drawings, pipes embedded in slab, wall or beam shall be located and sized so as not to impair the structure: **outside diameter ≤ 1/3 of overall thickness** of slab, wall or beam; **spacing ≥ 3 x pipe diameter centre-to-centre**; not located so as to significantly impair strength.
  - Same in effect as ACI 318-11 6.3.4 (ACI says "outside dimension" and "3 diameters or widths").
- **6.3.6** Pipes may be considered to replace displaced concrete in compression only if: protected from rust/corrosion by adequate embedment; galvanized or uncoated **steel pipe not thinner than ASTM A120 Schedule 40**; **inside diameter ≤ 50 mm**; **spacing ≥ 3 diameters centre-to-centre**.
  - ACI diff: ACI 318-11 6.3.5 references ASTM A53 Schedule 40 (A120 is withdrawn) and nominal diameter ≤ 50 mm (2 in.).
- **6.3.7** Pipes and fittings shall be designed to resist effects of material, pressure and temperature on their own, before concrete reaches design strength.
- **6.3.8** No liquid, gas or vapour shall be placed in pipes until concrete attains design strength, **except water not exceeding 300 °C (as printed) and 0.35 MPa** [≈ 3.5 ksc] pressure.
  - [NOTE/probable typo] "300 °C" is impossible for water at 0.35 MPa; ACI 318-11 6.3.8 limit is 90 °F (**32 °C**) and 50 psi (0.34 MPa). Likely intended 30 °C (or 32 °C). Confirm with EIT before placing on drawings.
- **6.3.9** In solid slabs, piping shall be placed **between top and bottom reinforcement**.
  - ACI diff: ACI 318-11 6.3.9 permits exception for radiant heating/snow-melt pipes; EIT has no exception.
- **6.3.10** Concrete cover for pipes and fittings: **≥ 35 mm** for concrete exposed to earth or weather; **≥ 20 mm** for concrete not exposed to earth or weather.
  - ACI diff: ACI 318-11 6.3.10 uses 40 mm (1-1/2 in.) exposed, 20 mm (3/4 in.) not exposed.
- **6.3.11** Reinforcement **≥ 0.2% of concrete cross-sectional area** (0.002 Ac) shall be provided **normal to** the piping.
- **6.3.12** Reinforcement shall not be cut, bent or displaced from its proper location to install pipes/fittings, unless the design is revised (re-calculated).

### 6.4 Construction joints (รอยต่อก่อสร้าง)*
- **6.4.1** Concrete surface at construction joints shall be clean and free of laitance.
- **6.4.2** Immediately before new concrete is placed, all construction joints shall be **wetted** and **standing water removed**.
- **6.4.3** Construction joints shall be located so as not to impair structural strength, and designed to transfer shear and other forces through the joint.
  - ACI diff: ACI 318-11 6.4.3 refers explicitly to shear-friction 11.6.9; EIT gives no clause reference.
- **6.4.4** Construction joints in floors (slab) shall be within the **middle portion of the span, not less than 1/3 of the span from the support face** (i.e., within the middle third) of slabs, secondary beams (คานซอย) and beams.
- **6.4.5** Construction joints in main girders (คานหลักใหญ่) shall be offset **not less than 2 x width of the intersecting secondary beam** from the intersection.
- **6.4.6** Beams, girders or slabs supported by columns or walls shall not be cast until concrete in the supporting column/wall has hardened.
  - ACI diff: ACI 318-11 6.4.6 wording is "no longer plastic".
- **6.4.7** Beams, girders, drop panels (แป้นหัวเสา), column capitals (หัวเสา) and haunches (คานขยายความลึกที่ปลาย) that are part of a floor system shall be placed **monolithically** with the floor system, unless otherwise shown on drawings.
- \* [NOTE] Footnote: further details on construction joints in **EIT 1014-19 (วสท. 1014-19)**.

---

## 7.1 Standard hooks (ของอมาตรฐาน) — p.55
A standard hook is a bar end meeting any one of:

| Clause | Application | Bend angle | Straight extension beyond bend | Bar size range |
|---|---|---|---|---|
| 7.1.1 | Main bars | 180° | 4d_b, but not less than **60 mm** | (all) |
| 7.1.2 | Main bars | 90° | 12d_b | (all) |
| 7.1.3(ก) | Stirrups & ties | 90° | 6d_b | **6 mm to 16 mm** |
| 7.1.3(ข) | Stirrups & ties | 90° | 12d_b | **20 mm to 25 mm** |
| 7.1.3(ค) | Stirrups & ties | 135° | 6d_b | **6 mm to 25 mm** |

- 7.1.4 Hooks for seismic-resisting reinforcement: see clause 19.1.
- [NOTE] vs ACI 318-11 7.1: 180° hook min. extension 65 mm (2-1/2 in) in ACI vs **60 mm** in EIT. Stirrup/tie bands: ACI No.5 and smaller → EIT 6–16 mm; ACI No.6–No.8 → EIT 20–25 mm; ACI 135° hook No.8 and smaller → EIT 6–25 mm. Seismic hooks: ACI Ch.21 → EIT Ch.19.

## 7.2 Minimum bend diameters (เส้นผ่านศูนย์กลางที่เล็กที่สุดของวงโค้งที่ดัด) — p.55
- 7.2.1 Inside bend diameter shall not be less than Table 7.1, except stirrups and ties of size 6 mm to 16 mm.
- 7.2.2 Stirrups and ties: inside bend diameter ≥ **4d_b** for bars not larger than **16 mm**; for bars larger than 16 mm, per Table 7.1.
- 7.2.3 Welded wire reinforcement (ลวดตะแกรงเหล็กเชื่อม) used as stirrups/ties: inside bend diameter ≥ **4d_b** for deformed wire larger than **7 mm**, and ≥ **2d_b** for other wires. Bend shall start not less than **4d_b** from the nearest welded intersection.

**Table 7.1 Minimum diameters of bend (ตารางที่ 7.1)**

| Bar size (ขนาดของเหล็กเส้น) | Minimum bend diameter (inside) |
|---|---|
| 6 mm to 25 mm | 6d_b |
| 28 mm to 36 mm | 8d_b |
| 43 mm and 57 mm | 10d_b |

- [NOTE] ACI Table 7.2: No.3–No.8 → 6d_b; No.9–No.11 → 8d_b; No.14 & No.18 → 10d_b. ACI 7.2.3 wire threshold "larger than D6" → EIT "larger than 7 mm".

## 7.3 Bending (การดัดเหล็กเสริม) — p.56
- 7.3.1 All reinforcement shall be bent **cold**, unless the engineer specifies otherwise.
- 7.3.2 Reinforcement partially embedded in concrete shall not be field-bent (projecting end), except as shown on the drawings or specially permitted by the engineer.

## 7.4 Surface conditions (สภาพผิวของเหล็กเสริม) — p.56
- 7.4.1 At time of concreting, reinforcement shall be free of mud, oil, dirt or other coatings that reduce bond.
- 7.4.2 Reinforcement with light rust, mill scale, or both, may be accepted if minimum dimensions and weight of a (wire-brushed) test specimen comply with the มอก. (TIS) standards listed in clause 3.5.
- [NOTE] ACI 7.4.3 (prestressing steel surface) is not included.

## 7.5 Placing reinforcement (การจัดวางเหล็กเสริม) — p.56
- 7.5.1 Before concreting, reinforcement shall be accurately placed, adequately supported and secured against displacement within the tolerances of 7.5.2.
- 7.5.2 Unless otherwise specified by the engineer, placing tolerances:
  - (ก) Tolerance on effective depth d and on minimum concrete cover in flexural members, compression members and walls:

| Depth d | Tolerance on effective depth d | Tolerance on specified minimum cover |
|---|---|---|
| d ≤ 200 mm | **± 100 mm** (as printed) | −10 mm |
| d > 200 mm | ± 13 mm | −13 mm |

    - Note (หมายเหตุ, printed under table): tolerance on cover shall not exceed the tabulated value and shall not exceed **1/3 of the specified minimum cover** shown on the drawings/specifications.
    - [NOTE] "± 100 mm" for d ≤ 200 mm is almost certainly a misprint for **± 10 mm** (ACI 318-11 7.5.2.1: ±3/8 in = ±10 mm). Verified on page image: printed as "± 100 มม.".
  - (ข) Tolerance for longitudinal location of bends and bar ends: **± 50 mm**, except **± 13 mm** at discontinuous ends of brackets and corbels, and **± 25 mm** at discontinuous ends of other members. The cover tolerance of 7.5.2(ก) also applies at discontinuous ends of members.
- 7.5.3 Welded wire reinforcement (wire size not greater than **6 mm**) used in slabs with span not exceeding **3 m** may be curved from a point near the top of slab over the support to a point near the bottom of slab at midspan, provided it is continuous over, or securely anchored at, the support.
- 7.5.4 Welding of crossing bars (tack welding) for assembly of reinforcement is not permitted unless considered and approved by the engineer.
- [NOTE] ACI 7.5.3: WWR "D5 or W5 or smaller", span ≤ 10 ft → EIT 6 mm, 3 m.

## 7.6 Spacing limits for reinforcement (การกำหนดระยะห่างระหว่างเหล็กเสริม) — p.57
- 7.6.1 Minimum clear spacing between parallel bars in a layer: ≥ **d_b** and ≥ **25 mm**. See also 3.3.3 (aggregate size).
- 7.6.2 Beams with two or more layers: bars in upper layers placed directly above bars in bottom layer; clear distance between layers ≥ **25 mm**.
- 7.6.3 Compression members with spirals or ties: clear distance between longitudinal bars ≥ **1.5d_b** and ≥ **40 mm**. See also 3.3.3.
- 7.6.4 Clear-distance limits apply also to the clear distance between a contact lap splice and adjacent splices or bars.
- 7.6.5 Walls and slabs other than concrete joist construction: primary flexural reinforcement spacing ≤ **3 × wall/slab thickness** and ≤ **450 mm**.
- 7.6.6 Bundled bars (เหล็กเส้นที่มัดรวมกันเป็นกำ):
  - (ก) Parallel bars bundled to act as a unit shall all be **deformed bars**, max **4 bars per bundle**.
  - (ข) Bundled bars shall be enclosed within stirrups or ties.
  - (ค) Bars larger than **36 mm** shall not be bundled in beams.
  - (ง) Individual bars within a bundle terminated within the span of flexural members shall terminate at different points with at least **40d_b** stagger.
  - (จ) Where spacing limits and minimum cover are based on d_b, a bundle is treated as a single bar of diameter derived from the equivalent total area.
- [NOTE] ACI 7.6.6.3 "bars larger than No.11" → EIT ">36 mm". ACI 7.6.7 (prestressing tendon/duct spacing) not included.

## 7.7 Concrete protection for reinforcement (คอนกรีตที่หุ้มเหล็กเสริม) — pp.57–59
Definition: concrete cover is measured from the concrete surface to the **outermost surface of ties, spirals or stirrups**; where these are absent, to the outer surface of the outermost bar.

### 7.7.1 Cast-in-place concrete (คอนกรีตหล่อในที่)
Minimum cover as follows, but not less than required by 7.7.5 (fire protection):

| Item | Condition / element | Bar-size band | Min. cover (mm) |
|---|---|---|---|
| (ก) | Concrete cast against and permanently exposed to earth | all | **75** |
| (ข) | Concrete exposed to earth or weather | bars **20 mm and larger** | **50** |
| (ข) | Concrete exposed to earth or weather | bars and welded wire reinforcement **16 mm and smaller** | **40** |
| (ค)(1) | Not exposed to weather or in contact with ground — beams and columns | primary reinforcement, stirrups, ties, or spirals (printed "เหล็กปลอกเดียว") | **40** |
| (ค)(2) | Not exposed — slabs, walls, joists | bars **20 mm and larger** | **30** |
| (ค)(2) | Not exposed — slabs, walls, joists | bars and welded wire reinforcement **16 mm and smaller** | **20** |
| (ค)(3) | Not exposed — shells and folded plate members | bars **20 mm and larger** | **20** |
| (ค)(3) | Not exposed — shells and folded plate members | bars and welded wire reinforcement **16 mm and smaller** | **15** |

- [NOTE] Bands are "20 mm and larger" / "16 mm and smaller"; intermediate sizes (e.g. 18/19 mm) are not explicitly assigned.
- [NOTE] Differences vs ACI 318-11 7.7.1: exposed-to-weather bands ACI No.6–No.18 (50) / No.5 & smaller (40) → EIT ≥20 / ≤16 mm (same values). Slabs/walls/joists: ACI No.14 & No.18 = 40, No.11 & smaller = 20 → **EIT ≥20 mm = 30, ≤16 mm = 20** (EIT more stringent for mid-size bars). Shells: ACI No.6+ = 20, No.5 & smaller = 13 → EIT 20 / **15**.
- [NOTE] ACI 7.7.2 (cast-in-place **prestressed** concrete cover) and ACI 7.7.5 (headed shear stud cover) are **not included** in EIT Ch.7 — there is no prestressed cover clause in this chapter.

### 7.7.2 Precast concrete (manufactured under plant control conditions) (คอนกรีตหล่อสำเร็จ)

| Item | Condition / element | Bar-size band | Min. cover (mm) |
|---|---|---|---|
| (ก)(1) | Exposed to earth or weather — other members (องค์อาคารชนิดอื่น) | bars **20 mm and larger** | **40** |
| (ก)(1) | Exposed to earth or weather — other members | bars and welded wire reinforcement **16 mm and smaller** | **30** |
| (ก)(2) | Exposed to earth or weather — wall panels | bars **20 mm and larger** | **30** |
| (ก)(2) | Exposed to earth or weather — wall panels | bars and welded wire reinforcement **16 mm and smaller** | **20** |
| (ข)(1) | Not exposed — beams and columns | primary reinforcement | **d_b, but need not exceed 40** |
| (ข)(1) | Not exposed — beams and columns | stirrups, ties or spirals | **15** |
| (ข)(2) | Not exposed — slabs, walls, joists | bars **20 mm and larger** | **25** |
| (ข)(2) | Not exposed — slabs, walls, joists | bars and welded wire reinforcement **16 mm and smaller** | **15** |
| (ข)(2) | Not exposed — slabs, walls, joists | welded wire reinforcement **16 mm and smaller** | **d_b, but not less than 15** (printed as a separate line; overlaps preceding line) |
| (ข)(3) | Not exposed — shells and folded plate members | bars **20 mm and larger** | **15** |
| (ข)(3) | Not exposed — shells and folded plate members | bars and welded wire reinforcement **16 mm and smaller** | **10** |

- [NOTE] Differences vs ACI 318-11 7.7.3: ACI wall panels No.14/18 = 40, No.11 & smaller = 20; other members No.14/18 = 50, No.6–11 = 40, No.5 & smaller = 30 → EIT two-band values above. Not exposed slabs: ACI No.14/18 = 30, No.11 & smaller = 16 → EIT 25 / 15. Beam/column primary: ACI "d_b but ≥ 16 mm and need not exceed 40" → EIT omits the 16 mm lower bound. Ties/stirrups: ACI 10 → **EIT 15**. Shells: ACI No.6+ = 16, No.5 & smaller = 10 → EIT 15 / 10.

### 7.7.3 Bundled bars
- Minimum cover = equivalent diameter of a single bar of area equal to the bundle, but need not exceed **50 mm**.
- For concrete cast against and permanently exposed to earth: minimum cover not less than **75 mm**.

### 7.7.4 Corrosive environments
- In corrosive environments or other severe exposure, cover shall be suitably increased; consider denser, less permeable concrete or other protection.

### 7.7.5 Fire protection
- Where the building code (ประมวลข้อบังคับอาคาร) requires a fire-protection cover thicker than the minimum cover of 7.7, the larger cover shall be used.

### 7.7.6 Future extensions
- Exposed reinforcement, inserts and plates intended for bonding with future extensions shall be protected from corrosion.

- [NOTE] Clause order differs from ACI 318-11 (ACI: 7.7.6 corrosive, 7.7.7 future extensions, 7.7.8 fire).

## 7.8 Special reinforcement details for columns (รายละเอียดพิเศษสำหรับเหล็กเสริมในเสา) — p.59
### 7.8.1 Offset bars (เหล็กเส้นที่เยื้องกัน / ดุ้ง)
- (ก) Slope of inclined portion of an offset bar with respect to column axis ≤ **1 in 6**.
- (ข) Portions of bar above and below the offset shall be parallel to column axis.
- (ค) Horizontal support at offset bends by ties, spirals, or parts of floor construction, designed for **1½ times** the horizontal component of the force in the inclined portion. Ties or spirals, if used, placed not more than **150 mm** from points of bend.
- (ง) Offset bars shall be bent before placement in the forms (see 7.3).
- (จ) Where a column face is offset **75 mm or more**, longitudinal bars shall not be offset-bent; use separate dowels lap-spliced with the longitudinal bars adjacent to the offset faces. Splices per clause **12.15** (as printed; ACI 318-11 refers to 12.17).

### 7.8.2 Steel cores (แกนเหล็กโครงสร้างรูปพรรณ) — load transfer in structural steel cores of composite compression members
- (ก) Ends of structural steel cores shall be accurately finished to bear at end-bearing splices, with positive provision for alignment of one core above the other in concentric contact.
- (ข) At end-bearing splices, bearing shall be considered effective to transfer not more than **50%** of the total compressive stress in the steel core.
- (ค) Transfer of stress between column base and footing designed per clause **15.8**.
- (ง) Base of steel core designed to transfer the total load from the entire composite member to the footing; or, where the concrete section is adequate to transfer the reinforced-concrete portion, designed to transfer the load from the steel core only.

## 7.9 Connections (จุดต่อ) — p.59
- 7.9.1 At connections of principal framing elements (e.g. beams and columns), enclosure shall be provided for splices of continuing reinforcement and for anchorage of reinforcement terminating in such connections.
- 7.9.2 Enclosure at connections may consist of external concrete or internal closed ties, stirrups, or spirals.

## 7.10 Lateral reinforcement for compression members (เหล็กเสริมทางขวางสำหรับองค์อาคารรับแรงอัด) — pp.60–61
- 7.10.1 Lateral reinforcement for compression members shall conform to 7.10.4 and 7.10.5; shear and torsion reinforcement per Chapter 11.
- 7.10.2 Lateral reinforcement for composite compression members: per clause 10.13.
- 7.10.3 Lateral reinforcement per 7.10 and 10.13 may be waived where tests and structural analysis show adequate strength and feasibility of construction.

### 7.10.4 Spirals (เหล็กปลอกเกลียว) — also per 10.9.3
- (ก) Continuous bar or wire of uniform size, evenly spaced, rigidly assembled to hold size and spacing during handling and placing.
- (ข) Cast-in-place construction: spiral diameter not less than **9 mm**.
- (ค) Clear spacing between spirals ≤ **75 mm** and ≥ **25 mm**. See also 3.3.3.
- (ง) Anchorage: **1½ extra turns** of spiral bar/wire at each end of the spiral unit.
- (จ) Splices of spirals (d_b = spiral bar diameter), by one of:
  - (1) Lap splices not less than the following, and not less than **300 mm**:

| Item | Spiral bar/wire type | Lap length |
|---|---|---|
| (1.1) | Deformed uncoated bar or wire | 48d_b |
| (1.2) | Plain uncoated bar or wire | 72d_b |
| (1.3) | Epoxy-coated deformed bar or wire | 72d_b |
| (1.4) | Plain uncoated bar or wire with a stirrup/tie standard hook (per 7.1.3) at the ends of lapped spiral; hooks embedded within the core confined by the spiral | 48d_b |
| (1.5) | Epoxy-coated deformed bar or wire with a stirrup/tie standard hook (per 7.1.3) at ends; hooks within the core confined by the spiral | **43d_b** (as printed) |

    - [NOTE] ACI 318-11 7.10.4.5(e) gives **48d_b** for item (1.5); "43d_b" appears to be a misprint in EIT (verified on page image).
  - (2) Full mechanical splice or full welded splice per clause **12.14.4** (ACI: 12.14.3).
- (ฉ) Spirals shall extend from top of footing or slab in any story to the level of the lowest horizontal reinforcement in members supported above.
- (ช) Where beams or brackets do not frame into all sides of a column, ties (เหล็กปลอกเดี่ยว) shall extend above termination of spiral to bottom of slab or drop panel.
- (ซ) In columns with capitals, spiral shall extend to a level at which the diameter or width of capital is **2 times** that of the column.
- (ฌ) Spirals shall be held firmly in place and true to line.

### 7.10.5 Ties (เหล็กปลอก)
- (ก) All non-prestressed longitudinal bars shall be enclosed by lateral ties of diameter at least:

| Item | Longitudinal bar diameter | Minimum tie diameter |
|---|---|---|
| (1) | 12 mm or smaller | **6 mm** |
| (2) | 16 mm and 20 mm | **9 mm** |
| (3) | 25 mm and 28 mm | **10 mm** |
| (4) | 32 mm and larger, and bundled longitudinal bars | **12 mm** |

  - [NOTE] ACI 318-11 7.10.5.1 has only two bands: No.3 ties for No.10 and smaller longitudinal bars; No.4 ties for No.11, 14, 18 and bundled bars; and permits deformed wire/WWR of equivalent area. EIT uses four mm-based bands (sizes typical of Thai RB6/RB9/DB10/DB12, though not labeled RB/DB) and does not mention the wire/WWR alternative.
- (ข) Vertical tie spacing shall not exceed the least of:
  - (1) **16d_b** of longitudinal bars;
  - (2) **48d_b** of tie bars;
  - (3) least dimension of the compression member.
- (ค) Ties arranged so every corner bar and alternate longitudinal bar has lateral support by the corner of a tie with an included angle not more than **135°**; no bar shall be farther than **150 mm** clear on each side along the tie from such a laterally supported bar. Where longitudinal bars are located around a circle, a complete circular tie is permitted.
- (ง) Circular ties around circularly arranged longitudinal bars: tie ends shall overlap not less than **150 mm** and terminate with standard hooks engaging a longitudinal bar; overlaps at ends of adjacent circular ties shall be staggered around the perimeter. [NOTE] Not in ACI 318-11 (appears in ACI 318-14 25.7.2.4.1).
- (จ) Ties located vertically not more than **one-half tie spacing** above top of footing or slab in any story, and not more than one-half tie spacing below the lowest horizontal reinforcement in slab or drop panel above.
- (ฉ) Where beams or brackets frame from **four directions** into a column, ties may be terminated not more than **75 mm** below the lowest reinforcement in the shallowest of such beams or brackets.
- (ช) Where anchor bolts are placed in the top of columns or pedestals, they shall be enclosed by lateral reinforcement that also surrounds at least **four** vertical bars of the column or pedestal. This lateral reinforcement shall be distributed within **125 mm** of the top of column/pedestal and consist of at least **two 12 mm** bars or **three 10 mm** bars. [NOTE] ACI 318-11 7.10.5.6: two No.4 or three No.3 bars within 5 in.

## 7.11 Lateral reinforcement for flexural members (เหล็กเสริมตามขวางสำหรับองค์อาคารรับแรงดัด) — p.62
- 7.11.1 Compression reinforcement in beams shall be enclosed by ties or stirrups satisfying the size and spacing limits of **7.10.5**, provided throughout the distance where compression reinforcement is required.
- 7.11.2 Lateral reinforcement for flexural framing members subject to stress reversals or to torsion at supports shall consist of closed ties, closed stirrups, or spirals extending around the flexural reinforcement.
- 7.11.3 Closed ties or stirrups shall be formed in one piece by overlapping standard stirrup or tie end hooks around a longitudinal bar, or formed in one or two pieces lap spliced with a **Class B** splice (lap length **1.3ℓ_d**), or anchored per clause **12.13**.

## 7.12 Shrinkage and temperature reinforcement (เหล็กเสริมต้านการยืดหด) — p.62
- 7.12.1 Structural slabs where flexural reinforcement extends in one direction only: shrinkage and temperature reinforcement shall be provided perpendicular to the principal reinforcement.
  - (ก) Per 7.12.2.
  - (ข) Where shrinkage and temperature movements are significantly restrained, requirements of clauses **8.2.4 and 9.2.6** shall be considered (as printed).
- 7.12.2 Requirements:
  - (ก) Ratio of S&T reinforcement area to **gross** concrete area not less than the following, and not less than **0.0014**:

| Item | Slab reinforcement type | Minimum ratio (A_s / A_g) |
|---|---|---|
| (1) | Plain round bars grade **SR 24** | **0.0025** |
| (2) | Deformed bars grade **SD 30** | **0.0020** |
| (3) | Deformed bars grade **SD 40**, or welded wire reinforcement (plain or deformed/indented) | **0.0018** |
| (4) | Reinforcement with yield strength exceeding **400 MPa** measured at a yield strain of **0.35%** | **0.0018 × 400 / f_y** |

  - (ข) S&T reinforcement spacing ≤ **5 × slab thickness** and ≤ **400 mm**.
  - (ค) At all sections where required, S&T reinforcement shall be developed for the specified yield strength f_y in tension per Chapter 12.
- [NOTE] Differences vs ACI 318-11 7.12.2.1: ACI has no plain-bar (SR24, 0.0025) item; Grade 40/50 → EIT SD30 (0.0020); Grade 60 → EIT SD40 (0.0018); fy > 60 ksi → 0.0018×400/fy. Max spacing ACI 5h and **450 mm (18 in)** → EIT **400 mm**. ACI 7.12.3 (prestressed S&T tendons) not included.

## 7.13 Requirements for structural integrity (เกณฑ์กำหนดสำหรับความมั่นคงแข็งแรงของโครงสร้าง) — p.63
- 7.13.1 In detailing reinforcement and connections, members shall be effectively tied together to improve integrity of the overall structure.
- 7.13.2 Cast-in-place construction — minimum requirements:
  - (ก) Joist construction: at least one bottom bar shall be continuous, or spliced with a **Class B** tension lap splice, or a mechanical or welded splice per **12.14.4**; at non-continuous supports, bars shall terminate with a standard hook.
  - (ข) Perimeter beams shall have continuous reinforcement consisting of:
    - (1) at least **one-sixth** of the tension reinforcement required for negative moment at the support, but not less than **two bars**; and
    - (2) at least **one-quarter** of the tension reinforcement required for positive moment at midspan, but not less than **two bars**.
  - (ค) Continuous reinforcement per (ข)(1) and (ข)(2) shall be enclosed by U-stirrups with hooks of not less than **135°** around the top bars, or by one-piece closed stirrups with not less than **135°** hooks around a top bar. Transverse reinforcement need not be extended through the column.
  - (ง) Where splices are needed for continuity: top reinforcement spliced at or near **midspan**; bottom reinforcement spliced at or near the **support**. Splices shall be Class B tension lap splices, or mechanical or welded splices per 12.14.4.
  - (จ) Beams other than perimeter beams, when transverse reinforcement as defined in 7.13.2 (ง) [as printed; logically (ค)] is not provided: at least **one-quarter** of positive-moment reinforcement required at midspan, but not less than **two bars**, shall be continuous or spliced over or near the support with Class B tension lap splice or mechanical/welded splice per 12.14.4; at non-continuous supports terminate with a standard hook.
  - (ฉ) Two-way slab construction: see clause **13.3.8 (จ)**.
- 7.13.3 Precast construction: tension ties shall be provided in transverse, longitudinal and vertical directions and around the perimeter to effectively tie elements together; per clause **16.5**.
- [NOTE] EIT splice clause reference 12.14.4 corresponds to ACI 318-11 12.14.3.

---

## Printing issues flagged (verified on page images)
1. 7.5.2(ก) table: tolerance on d for d ≤ 200 mm printed "± 100 มม." — likely should be ± 10 mm.
2. 7.10.4(จ)(1.5): lap printed "43d_b" — ACI gives 48d_b.
3. 7.7.1(ค)(1): "เหล็กปลอกเดียว" — intended "เหล็กปลอกเกลียว" (spirals).
4. 7.7.2(ข)(2): two overlapping lines for WWR ≤16 mm (15 mm, and "d_b but ≥ 15 mm").
5. 7.13.2(จ): cross-reference "7.13.2 (ง)" — logically 7.13.2 (ค).

No unreadable values.

---

## CHAPTER 12 — DEVELOPMENT AND SPLICES OF REINFORCEMENT

### 12.1 Development of reinforcement — general
- **12.1.1** Tension or compression in reinforcement at each side of a section shall be developed by embedment length, hook, headed bar or mechanical device, or a combination. Hooks and heads shall **not** be used to develop bars in compression.
- **12.1.2** √fc′ used in this chapter shall not exceed **8.3 MPa** (MKS: 26.5 ksc — see Appendix; Appendix row for 11.1.2 gives 27 ksc).

### 12.2 Development of deformed bars and deformed wire in tension
- **12.2.1** ℓd from 12.2.2 **or** 12.2.3 with modification factors of 12.2.4 and 12.2.5; **ℓd ≥ 300 mm**.
- **12.2.2** Simplified ℓd (SI, fy and fc′ in MPa):

| Condition | Bars/wires **20 mm and smaller** | Bars **22 mm and larger** |
|---|---|---|
| (i) Clear cover ≥ db, **and** clear spacing of bars developed or spliced ≥ db, **and** stirrups/ties throughout ℓd not less than code minimum; **or** (ii) clear cover ≥ db **and** clear spacing of bars developed or spliced ≥ 2db | ℓd = [fy ψt ψe / (2.1 λ √fc′)] db | ℓd = [fy ψt ψe / (1.7 λ √fc′)] db |
| Other cases | ℓd = [fy ψt ψe / (1.4 λ √fc′)] db | ℓd = [fy ψt ψe / (1.1 λ √fc′)] db |

MKS (ksc) equivalents from Appendix A: denominators **6.6, 5.3, 4.4, 3.5** respectively (same order: ≤20 mm good / ≥22 mm good / ≤20 mm other / ≥22 mm other).
[NOTE] Same as ACI 318M-11 12.2.2 (ACI SI: 1/2.1, 1/1.7, 1/1.4, 1/1.1).

- **12.2.3** General equation:

  **ℓd = [ fy / (1.1 λ √fc′) ] · [ ψt ψe ψs / ((cb + Ktr)/db) ] · db**   (12-1)
  MKS: denominator 3.5 λ √fc′ instead of 1.1 λ √fc′.

  Confinement term (cb + Ktr)/db ≤ **2.5**.

  **Ktr = 40 Atr / (s n)**   (12-2)
  n = number of bars or wires being spliced or developed along the plane of splitting. Ktr = 0 permitted as a design simplification even if transverse reinforcement is present.
  [NOTE] cb, Atr, s not redefined on these pages (per ACI: cb = smaller of distance from bar center to nearest concrete surface and one-half c/c spacing of bars developed; Atr = total transverse reinforcement area within spacing s crossing potential splitting plane; s = c/c spacing of transverse reinforcement within ℓd).

- **12.2.4** Factors:
  - (a) ψt (casting position): horizontal reinforcement placed so that **more than 300 mm** of fresh concrete is cast below the development length or splice → **ψt = 1.3**; other → **1.0**.
  - (b) ψe (coating): epoxy-coated, zinc+epoxy dual-coated bars, or epoxy-coated wire with cover < **3db** or clear spacing < **6db** → **ψe = 1.5**; all other epoxy/dual-coated → **1.2**; uncoated and zinc-coated (galvanized) → **1.0**. Product **ψt ψe need not exceed 1.7**.
  - (c) ψs (size): bars/wires **20 mm and smaller → 0.8**; bars **22 mm and larger → 1.0**.
  - (d) λ: lightweight concrete → λ **not exceeding 0.75** unless fct is specified (see 8.6.1); normalweight → **λ = 1.0**.
  [NOTE] ACI 318-11 12.2.4(d) sets λ = 0.75 for lightweight; EIT wording "not exceeding 0.75". 8.6.1 (Appendix): λ = fct/(0.56√fc′) ≤ 1.0 (MKS: fct/(1.78√fc′)).
- **12.2.5** Excess reinforcement: ℓd may be reduced by factor **(As required)/(As provided)** when flexural reinforcement exceeds that required by analysis, **except** where anchorage/development for fy is specifically required, or where reinforcement is designed under **seismic** provisions.
  [NOTE] ACI 318-11 exception refers to 21.1.1.6; EIT refers generically to earthquake design requirements.

### 12.3 Development of deformed bars and deformed wire in compression
- **12.3.1** ℓdc from 12.3.2 times applicable factors of 12.3.3; **ℓdc ≥ 200 mm**.
- **12.3.2** ℓdc = greater of **(fy / (4.2 λ √fc′)) db** and **(0.043 fy) db**; λ per 12.2.4(d); constant 0.043 in mm²/N.
  [NOTE] The printed text states "constant **0.0003** in mm²/N" while the equation shows 0.043 — the 0.0003 is the ACI in-lb constant left in by error; 0.043 governs (matches ACI 318M-11: 0.24fy/(λ√fc′) ≈ fy/(4.2λ√fc′) and 0.043fy).
  MKS: (fy/(13.3 λ √fc′)) db ≥ (0.0044 fy) db.
- **12.3.3** Multiply ℓdc by:
  - (a) Excess reinforcement: **(As required)/(As provided)**.
  - (b) Spirals and ties: reinforcement enclosed within spiral of diameter **≥ 6 mm** and pitch **≤ 100 mm**, or within **12 mm** ties per 7.10.5 spaced **≤ 100 mm** c/c → **0.75**.

### 12.4 Development of bundled bars
- **12.4.1** ℓd of individual bars in a bundle (tension or compression) = ℓd of individual bar increased **20% for 3-bar bundle** and **33% for 4-bar bundle**.
- **12.4.2** For factors in 12.2, a bundle is treated as a single bar of diameter derived from the equivalent total area.

### 12.5 Development of standard hooks in tension
- **12.5.1** ℓdh for deformed bars in tension terminating in a standard hook (see 7.1): from 12.5.2 × factors of 12.5.3; **ℓdh ≥ max(8db, 150 mm)**.
- **12.5.2** **ℓdh = [ fy ψe / (4.2 λ √fc′) ] db**   (12-3)
  ψe = **1.2** epoxy-coated; λ = **0.75** lightweight; otherwise ψe = λ = **1.0**.
  MKS: denominator **13.3 λ √fc′**.
  [NOTE] ACI 318M-11: 0.24ψe fy/(λ√fc′) — equivalent.
- **12.5.3** Multiply ℓdh by:
  - (a) Concrete cover: bars **≤ 36 mm** with side cover (normal to plane of hook) **≥ 65 mm**, and for 90° hook with cover on bar extension beyond hook **≥ 50 mm** → **0.7**.
  - (b) 90° hooks: bars **≤ 36 mm** enclosed within ties or stirrups **perpendicular or parallel** to the bar being developed, spaced **≤ 3db** along ℓdh → **0.8**.
  - (c) 180° hooks: bars **≤ 36 mm** enclosed within ties or stirrups **perpendicular** to the bar being developed, spaced **≤ 3db** along ℓdh → **0.8**.
  - (d) Excess reinforcement (where anchorage/development for fy not specifically required): **(As required)/(As provided)**.
  In (b) and (c), db = diameter of hooked bar; the first tie or stirrup shall enclose the bent portion of the hook within **2db** of the outside of the bend.
- **12.5.4** Bars developed by standard hook at **discontinuous ends** of members with both side cover and top (or bottom) cover over hook **< 65 mm**: hooked bar shall be enclosed within ties or stirrups **perpendicular** to the bar, spaced **≤ 3db** along ℓdh; first tie/stirrup to enclose the bent portion within **2db** of outside of bend. The 0.8 factors of 12.5.3(b),(c) shall **not** be applied.
- **12.5.5** Hooks shall not be considered effective in developing bars in compression.

### 12.6 Development of headed and mechanically anchored deformed bars in tension
- **12.6.1** ℓdt per 12.6.2. Heads permitted only when all of: (a) **fy ≤ 420 MPa**; (b) bar size **≤ 36 mm**; (c) **normalweight** concrete; (d) net bearing area of head **Abrg ≥ 4Ab**; (e) clear cover for bar **≥ 2db**; (f) clear spacing between bars **≥ 4db**.
- **12.6.2** Headed deformed bars satisfying 3.5.9:
  **ℓdt = [ fy ψe / (5.3 λ √fc′) ] db**   (12-4)
  fc′ used **≤ 40 MPa**; ψe = **1.2** epoxy-coated, **1.0** otherwise; **ℓdt ≥ max(8db, 150 mm)**.
  MKS: denominator **16.7 λ √fc′**.
  [NOTE] ACI 318M-11 12.6.2: ℓdt = (0.19ψe fy/√fc′)db — no λ (normalweight only). EIT includes λ (=1.0 in effect since 12.6.1(c) requires normalweight).
- **12.6.3** Heads not considered effective in compression.
- **12.6.4** Any mechanical attachment/device capable of developing fy is permitted, provided test results show adequacy or the device is officially approved. Development may be by combination of mechanical anchorage plus additional embedment between critical section and the anchorage/device.

### 12.7 Development of welded deformed wire reinforcement in tension
- **12.7.1** ℓd measured from critical section to end of wire = ℓd from 12.2.2 or 12.2.3 × wire-fabric factor ψw (12.7.2 or 12.7.3). Reduction per 12.2.5 permitted when applicable. **ℓd ≥ 200 mm** except in computing lap splices by 12.18 [sic — ACI refers to splice clause 12.18 = EIT 12.17]. When ψw from 12.7.2 is used, ψe = **1.0** may be used for epoxy-coated welded wire reinforcement in 12.2.2 and 12.2.3.
- **12.7.2** Welded deformed wire with ≥ 1 cross wire within ℓd located **≥ 50 mm** from critical section:
  ψw = greater of **(fy − 240)/fy** and **5db/s**, but need not exceed **1.0**; s = spacing between wires being developed.
  MKS: (fy − 2,460)/fy.
- **12.7.3** No cross wires within ℓd, or single cross wire **< 50 mm** from critical section: ψw = **1.0**; ℓd as for deformed wire.
- **12.7.4** Plain wire, or deformed wires **larger than 16 mm**, in direction of development: develop per 12.8.

### 12.8 Development of welded plain wire reinforcement in tension
Yield strength considered developed by embedment of **two cross wires**, the closer one **≥ 50 mm** from critical section. ℓd not less than:
**ℓd = 3.3 (Ab / s) · fy / (λ √fc′)**   (12-5)
ℓd measured from critical section to outermost cross wire; s = spacing between wires being developed; λ per 12.2.4(d). Reduction per 12.2.5 permitted. **ℓd ≥ 150 mm** except in computing lap splices by 12.18.
MKS: ℓd = (Ab/s) · fy/(λ√fc′) (coefficient 1.0).

### 12.9 Development of flexural reinforcement — general  (= ACI 12.10)
- **12.9.1** Tension reinforcement may be developed by bending across the web to be anchored or made continuous with reinforcement on the opposite face.
- **12.9.2** Critical sections: points of maximum stress and points within the span where adjacent reinforcement terminates or is bent. Provisions of 12.10.3 shall be satisfied.
- **12.9.3** Reinforcement shall extend beyond the point where no longer required to resist flexure a distance **≥ max(d, 12db)**, except at supports of simple spans and at free ends of cantilevers.
- **12.9.4** Continuing reinforcement shall have embedment **≥ ℓd** beyond the point where bent or terminated tension reinforcement is no longer required.
- **12.9.5** Flexural reinforcement shall not be terminated in a tension zone unless one of:
  - (a) **Vu ≤ (2/3) φVn** at the cutoff point;
  - (b) Stirrup area in excess of that required for shear and torsion is provided along each terminated bar or wire over a distance **(3/4)d** from the termination point; excess stirrup area **0.41 bw s / fyt** [see NOTE]; spacing **s ≤ d/(8βb)**;
    [NOTE] EIT text reads "area shall **not exceed** 0.41bws/fyt"; ACI 318-11 12.10.5.2 requires excess stirrup area **not less than** 0.41bws/fyt — EIT wording appears to be a translation error; use as a minimum. βb = ratio of area of reinforcement cut off to total tension reinforcement at the section. MKS: 4.2 bws/fyt.
  - (c) For bars **≤ 36 mm**: continuing reinforcement provides **double** the area required for flexure at the cutoff point **and Vu ≤ (3/4) φVn**.
- **12.9.6** Adequate anchorage for tension reinforcement in flexural members where reinforcement stress is not directly proportional to moment (sloped, stepped or tapered footings, brackets, deep flexural members, members where tension reinforcement is not parallel to compression face). For deep flexural members see 12.10.4 and 12.11.4.

### 12.10 Development of positive moment reinforcement  (= ACI 12.11)
- **12.10.1** At least **1/3** of positive moment reinforcement in simple members and **1/4** in continuous members shall extend along the same face into the support. In beams, such reinforcement shall extend into the support **≥ 150 mm**.
- **12.10.2** Where a flexural member is part of the primary lateral-load-resisting system, positive moment reinforcement required by 12.10.1 to be extended into the support shall be anchored to develop **fy in tension at the face of support**.
- **12.10.3** At simple supports and at points of inflection, positive moment tension reinforcement shall be limited to a diameter such that ℓd (for fy, per 12.2) satisfies Eq. (12-6); Eq. (12-6) need not be satisfied for reinforcement terminating beyond the centerline of simple supports by a standard hook or a mechanical anchorage at least equivalent to a standard hook.

  **ℓd ≤ Mn/Vu + ℓa**   (12-6)

  Mn = nominal flexural strength assuming all reinforcement at the section stressed to fy (text prints "Mu" in the definition list — typo); Vu = factored shear at the section; ℓa at a support = embedment length beyond center of support; ℓa at a point of inflection = limited to the greater of **d or 12db**. Value **Mn/Vu may be increased 30%** when ends of reinforcement are confined by a compressive reaction.
- **12.10.4** At simple supports of **deep beams**, positive moment tension reinforcement shall be anchored to develop **fy in tension at the face of support**, except that if designed using Chapter 20 (strut-and-tie), anchorage per **20.4.3**. At interior supports of deep beams, positive moment tension reinforcement shall be continuous or spliced with that of adjacent spans.

### 12.11 Development of negative moment reinforcement  (= ACI 12.12)
- **12.11.1** Negative moment reinforcement in continuous, restrained or cantilever members, or any member of a rigid frame, shall be anchored in or through the supporting member by embedment length, hooks or mechanical anchorage.
- **12.11.2** Negative moment reinforcement shall have embedment length into the span per 12.1 and 12.9.3.
- **12.11.3** At least **1/3** of total tension reinforcement provided for negative moment at a support shall have embedment beyond the point of inflection **≥ max(d, 12db, ℓn/16)**.
- **12.11.4** At interior supports of deep flexural members, negative moment tension reinforcement shall be continuous with that of adjacent spans.

### 12.12 Development of web reinforcement  (= ACI 12.13)
- **12.12.1** Web reinforcement shall be as close to compression and tension surfaces as cover requirements and proximity of other reinforcement permit.
- **12.12.2** Ends of single-leg, simple U- or multiple U-stirrups anchored by one of:
  - (a) Bars **16 mm** and deformed wire **16 mm** and smaller, and bars **20, 22, 25 mm** with **fyt ≤ 280 MPa**: standard hook around longitudinal reinforcement.
  - (b) Stirrups **20, 22, 25 mm** with **fyt > 280 MPa**: standard stirrup hook around a longitudinal bar **plus** embedment between mid-height of member and outside end of hook **≥ (fyt / (5.9 λ √fc′)) db**. (MKS: fyt/(18.9 λ√fc′) db.) [NOTE] ACI 318M-11: 0.17db fyt/(λ√fc′).
  - (c) Each leg of welded plain wire reinforcement forming simple U-stirrups: either (1) two longitudinal wires spaced at **50 mm** along member at top of U; or (2) one longitudinal wire located **≤ d/4** from compression face and a second wire closer to compression face spaced **≥ 50 mm** from the first; second wire may be on stirrup leg beyond a bend, or on a bend with inside diameter **≥ 8db**.
  - (d) Each end of single-leg stirrup of welded plain or deformed wire reinforcement: two longitudinal wires at minimum spacing **50 mm**, inner wire at least **max(d/4, 50 mm)** from d/2; outer longitudinal wire at tension face not farther from the face than the portion of primary flexural reinforcement closest to the face.
  - (e) Joist construction per 8.11: for bars **12 mm** or welded wire **12 mm** and smaller, a standard hook shall be provided.
- **12.12.3** Between anchored ends, each bend in the continuous portion of a simple or multiple U-stirrup shall enclose a longitudinal bar.
- **12.12.4** Longitudinal bars bent to act as shear reinforcement: if extended into a tension region, continuous with longitudinal reinforcement; if extended into a compression region, anchored beyond mid-depth d/2 as specified for development length in 12.2 for that part of fyt required to satisfy Eq. (11-12).
- **12.12.5** Pairs of U-stirrups or ties placed to form a closed unit are properly spliced when lap length is **1.3ℓd**. In members at least **500 mm** deep, such splices with **Ab fyt ≤ 40 kN per leg** are adequate if stirrup legs extend the full available depth of member.
  [NOTE] ACI 318M-11 12.13.5 uses 450 mm (18 in.) depth; EIT uses 500 mm.

### 12.13 Splices of reinforcement — general  (= ACI 12.14)
- **12.13.1** Splices only as required or permitted by design drawings or specifications, or as authorized by the engineer.
- **12.13.2** Lap splices:
  - (a) Lap splices **shall not be used for bars larger than 36 mm**, except as provided in **12.15.2** and **15.8.2(c)**.
  - (b) Lap splices of bundled bars based on lap splice length required for individual bars within the bundle, increased per 12.4. Individual bar splices within a bundle shall not overlap. Entire bundles shall **not** be lap spliced (bold "prohibited").
  - (c) Bars spliced by noncontact lap splices in flexural members shall not be spaced transversely farther apart than the smaller of **one-fifth the required lap splice length** and **150 mm**.
- **12.13.3** Mechanical and welded splices:
  - (a) Mechanical and welded splices permitted.
  - (b) A **full mechanical splice** shall develop in tension or compression at least **1.25 fy** of the bar.
  - (c) Except as provided in this standard, welding shall conform to other applicable requirements for welding of reinforcing bars in structures. [NOTE] ACI refers to AWS D1.4.
  - (d) A **full welded splice** shall have bars butted and welded to develop in tension at least **1.25 fy** of the bar.
  - (e) Mechanical or welded splices not meeting 12.13.3(b) or 12.13.3(c) [sic — should read (d)] permitted only for bars **16 mm and smaller**, per 12.14.4 [sic — requirements are in 12.14.5].

### 12.14 Splices of deformed bars and deformed wire in tension  (= ACI 12.15)
- **12.14.1** Minimum tension lap length per Class A or B, but **≥ 300 mm**:
  | Splice | Length |
  |---|---|
  | Class A | 1.0 ℓd |
  | Class B | 1.3 ℓd |
  ℓd per 12.2 for fy, **without** the 12.2.5 (excess reinforcement) factor.
- **12.14.2** Lap splices of deformed bars and wire in tension shall be **Class B**, except **Class A** is allowed when **both**: (a) As provided ≥ **2 ×** As required by analysis over the entire splice length; **and** (b) **≤ 1/2** of total reinforcement is spliced within the required lap length.
- **12.14.3** Bars of different size lap spliced in tension: splice length = larger of ℓd of larger bar and tension lap splice length of smaller bar.
- **12.14.4** Mechanical or welded splices per 12.13.3(b) and 12.13.3(d) shall be used where As provided < 2 × As required by analysis.
- **12.14.5** Mechanical or welded splices not meeting 12.13.3(b) or (d) permitted only for bars **16 mm and smaller**, and:
  - (a) Splices shall be staggered at least **600 mm**;
  - (b) In computing tensile forces developed at each section, spliced reinforcement stress = specified splice strength but **≤ fy**; unspliced reinforcement stress = fy × ratio of shortest length embedded beyond the section to ℓd, but **≤ fy**;
  - (c) Total tensile force developed at each section shall be at least **2 ×** that required by analysis, and at least **140 MPa × total area of reinforcement** provided.
- **12.14.6** Splices in tension tie members: full mechanical or full welded splices per 12.13.3(b) or (d); splices in adjacent bars staggered at least **750 mm**.

### 12.15 Splices of deformed bars in compression  (= ACI 12.16)
- **12.15.1** Compression lap splice length:
  - **0.071 fy db** for **fy ≤ 420 MPa**;
  - **(0.13 fy − 24) db** for **fy > 420 MPa**;
  - but **≥ 300 mm**. For **fc′ < 21 MPa**, lap length increased by **one-third**.
  - MKS: 0.0073 fy db; (0.013 fy − 24) db.
- **12.15.2** Bars of different size lap spliced in compression: length = larger of ℓdc of larger bar and compression lap length of smaller bar. Bars **44 mm and 57 mm** may be lap spliced to bars **36 mm and smaller**.
- **12.15.3** Mechanical or welded splices in compression per 12.13.3(b) or 12.13.3(d).
- **12.15.4** End-bearing splices:
  - (a) Only for bars required for compression only; compressive stress transmitted by bearing of square-cut ends held in concentric contact by a suitable device.
  - (b) Bar ends shall terminate in flat surfaces within **1.5°** of a right angle to the bar axis and fitted within **3°** of full bearing after assembly.
  - (c) Only in members containing closed ties, closed stirrups or spirals.

### 12.16 Special splice requirements for columns  (= ACI 12.17)
- **12.16.1** Lap, butt-welded, mechanical or end-bearing splices used subject to 12.16.2–12.16.4. A splice shall satisfy requirements for **all factored load combinations** for the column.
- **12.16.2** Lap splices in columns:
  - (a) Bar stress due to factored loads **compressive**: lap splices per 12.15.1, 12.15.2, and where applicable 12.16.2(d) or 12.16.2(e) [text prints "12.16.2.5(จ)" — typo].
  - (b) Bar stress tensile and **≤ 0.5fy**: **Class B** if more than half the bars are spliced at any section; **Class A** if half or fewer are spliced at any section **and** alternate splices are staggered by **ℓd**.
  - (c) Bar stress tensile and **> 0.5fy**: **Class B** tension lap.
  - (d) Tied compression members where ties throughout the lap length have effective area **≥ 0.0015 h s** in both directions: lap length may be multiplied by **0.83**, but **≥ 300 mm**. Tie legs perpendicular to dimension h used in computing effective area.
  - (e) Spirally reinforced compression members: lap length of bars within a spiral may be multiplied by **0.75**, but **≥ 300 mm**.
- **12.16.3** Mechanical or welded splices in columns per 12.13.3(b) or 12.13.3(d).
- **12.16.4** End-bearing splices per 12.15 may be used for column bars stressed in compression provided splices are staggered or additional bars provided at splice locations. Continuing bars in each face of the column shall have tensile strength **≥ 0.25 fy × area of vertical reinforcement in that face**.

### 12.17 Splices of welded deformed wire reinforcement in tension  (= ACI 12.18)
- **12.17.1** Minimum lap length measured between ends of each sheet **≥ 1.3ℓd** and **≥ 200 mm**; overlap measured between outermost cross wires of each sheet **≥ 50 mm**. ℓd per 12.7 for fy.
- **12.17.2** Lap splices of welded deformed wire reinforcement without cross wires within the lap splice length: determined as for deformed wire.
- **12.17.3** Where plain wires, or deformed wires **larger than 16 mm**, are present in the direction of the lap splice, or where welded deformed wire is lap spliced to welded plain wire, splice per 12.18.

### 12.18 Splices of welded plain wire reinforcement in tension  (= ACI 12.19)
- **12.18.1** Where As provided **< 2 ×** required by analysis at splice location: overlap measured between outermost cross wires of each sheet **≥ the largest of (one spacing of cross wires + 50 mm), 1.5ℓd, and 150 mm**; ℓd per 12.8 for fy.
- **12.18.2** Where As provided **≥ 2 ×** required: overlap between outermost cross wires **≥ 1.5ℓd**, and **≥ 150 mm**; ℓd per 12.8.
  [NOTE] ACI 318M-11 12.19.2 minimum is 50 mm (2 in.); EIT prints 150 mm.

---

## CHAPTER 18 — STRENGTH EVALUATION OF EXISTING STRUCTURES (Part 6 "Special considerations")
(= ACI 318-11 Chapter 20, abridged)

### 18.1 Strength evaluation — general
If there is doubt about the strength of a structure or member (from design, deterioration, or material tests showing concrete or reinforcement strength lower than specified, indicating a significant reduction in load capacity), the **engineer may order a load test**.

### 18.2 Analytical investigation — general
- **18.2.1** If strength evaluation is by analysis: field survey of dimensions and details of members; size and location of reinforcement by **sampling** to confirm drawing details; concrete compressive strength **should be obtained from tests of cores** taken from the structure.
- **18.2.2** Analysis based on 18.2.1 per engineer's requirements; load factors and strength reduction factors per the requirements and intent of this standard; see 18.6.
[NOTE] No separate core-acceptance criteria or increased φ factors (ACI 318-11 20.2.3–20.2.5) are given in this chapter.

### 18.3 Load tests — general
- **18.3.1** Load test supervised by a qualified engineer accepted by a government agency or reliable institution.
- **18.3.2** Load test not before the portion of structure to be loaded is **at least 56 days (8 weeks)** old, unless owner, contractor and all parties agree to earlier testing.
- **18.3.3** When only a portion is tested, test adequately in regions of suspected weakness; select test area and load arrangement to produce **maximum deflection and critical stresses**; more than one load arrangement may be used for maximum effect.

### 18.4 Load test of flexural members
- **18.4.1** Applies to flexural members incl. beams and slabs.
- **18.4.2** Initial reading (datum for deflection measurement) made **not more than 1 hour** before application of test load.
- **18.4.3** Total test load (including dead load already in place) = **0.85 (1.4D + 1.7L)**. L may be reduced as permitted by the applicable building regulation.
  [NOTE] Differs from ACI 318-11 20.3.2 (larger of 1.15D+1.5L+0.4(Lr/S/R), 1.15D+0.9L+1.5(Lr/S/R), 1.3D); EIT retains the older ACI 318-99 form.
- **18.4.4** Test load applied in **not fewer than 4 approximately equal increments**, without impact, and avoiding arching of test-load materials that would cause nonuniform distribution.
- **18.4.5** Deflection recorded after the total test load has been in place **24 hours**.
- **18.4.6** Remove test load immediately after the 24-h reading; final deflection recorded **24 hours after** removal.
- **18.4.7** If the tested portion shows visible evidence of failure (particularly cracking/spalling of compression concrete, or shear), it **fails** and **retest is not permitted**.
- **18.4.8** If no visible evidence of failure, the tested portion **passes** if:
  - (a) maximum measured deflection of beam, floor or roof **≤ ℓt² / (20,000 h)**; or
  - (b) if maximum deflection **> ℓt² / (20,000 h)**, recovery within **24 h** after removal of test load **≥ 75%** of maximum deflection.
- **18.4.9** In 18.4.8(a),(b): for cantilevers, ℓt = **2 ×** distance from support to cantilever end; deflection adjusted for support movement.
  [NOTE] General definition of ℓt (ACI: shorter span, smaller of c/c supports and clear span + h) not restated in this range; h = overall member thickness.
- **18.4.10** Members with recovery **< 75%** per 18.4.8(b) may be retested **not earlier than 72 hours** after removal of the first test load. Passes if: (a) no visible evidence of failure in retest, **and** (b) recovery from the second test load **≥ 80%** of maximum deflection in the second test.

### 18.5 Members other than flexural members
Analytical investigation should be selected for members other than flexural members.

### 18.6 Provision for lower load rating
If the structure does not satisfy 18.2, 18.4.8 or 18.4.10, a lower load rating based on load test or analysis may be permitted **if approved by the engineer**.

### 18.7 Safety
- **18.7.1** Load tests conducted so as to provide for safety of life and structure during the test.
- **18.7.2** Safety measures shall not interfere with load test procedures or affect results.

(PDF p.154 / book p.142 is blank.)

---

## CHAPTER 19 — SPECIAL PROVISIONS FOR EARTHQUAKE-RESISTANT STRUCTURES

Only clause 19.1 exists (PDF p.155); PDF p.156 is blank. **No detailing rules (hooks, seismic hooks, lap-splice location limits, hoop/tie spacing, confinement) are given in this standard** — they are delegated to the DPT seismic standard.

### 19.1 General
- **19.1.1 Scope**
  - (a) Chapter 19 covers design and construction of RC members of structures designed for earthquake forces, analysed on the basis of **energy dissipation in the nonlinear response range**.
  - (b) Design and structural analysis shall conform to **มยผ. 1301/1302-61** — "Standard for Seismic Resistant Building Design" of the **Department of Public Works and Town & Country Planning (DPT), Ministry of Interior**.
  - (c) An RC structural system not satisfying this chapter may be approved if supported by test evidence demonstrating strength and toughness equal to or exceeding a comparable monolithic RC system designed per this chapter.
- **19.1.2 Analysis and proportioning of structural members**
  - (a) Interaction of all structural and nonstructural members that affect linear and nonlinear response to earthquake shall be considered.
  - (b) Rigid members not part of the seismic-force-resisting system are permitted provided their effect on the response is considered and accommodated in design.
  - (c) Structural members below base of structure required to transmit earthquake forces to the foundation shall comply with the requirements of this chapter consistent with the seismic-force-resisting system above the base.

Related seismic references in Ch.12 of this range: 12.2.5 (no ℓd reduction for excess reinforcement when designed under seismic provisions).

---

## APPENDIX ก (A) — COMPARISON OF VALUES AND EQUATIONS: SI-metric (MPa) vs MKS-metric (kg/cm²)
(PDF p.177–182, book p.165–170; read from images only.) Table reproduced in full.

### Unit basis
| Item | SI-metric (MPa) | MKS-metric (kg/cm²) |
|---|---|---|
| — | 1 MPa | 10 kg/cm² |
| — | fc′ = 21 MPa | fc′ = 210 kg/cm² |
| — | fy = 300 MPa | fy = 3,000 kg/cm² |
| — | √fc′ MPa | 3.18 √fc′ kg/cm² |

### Chapters 5, 7, 8, 9, 10
| Clause / Eq. / Table | SI-metric | MKS-metric |
|---|---|---|
| Eq. (5-1) | fcr′ = fc′ + 1.34 ss | fcr′ = fc′ + 1.34 ss |
| Eq. (5-2) | fcr′ = fc′ + 2.33 ss − 3.5 | fcr′ = fc′ + 2.33 ss − 35 |
| Table 5.2 | fcr′ = fc′ + 7.0; fcr′ = fc′ + 8.3; fcr′ = 1.10 fc′ + 5.0 | fcr′ = fc′ + 70; fcr′ = fc′ + 84; fcr′ = 1.10 fc′ + 50 |
| 7.12.2 (a)(4) | 0.0018 × 400 / fy | 0.0018 × 4,000 / fy |
| 8.4.5 | ρb = 0.85 β1 (fc′/fy) · 600/(600 + fy) | ρb = 0.85 β1 (fc′/fy) · 6,000/(6,000 + fy) |
| 8.5.1 | Ec = wc^1.5 · 0.043 √fc′ ; Ec = 4,700 √fc′ | Ec = wc^1.5 · 0.14 √fc′ ; Ec = 15,100 √fc′ |
| 8.6.1 | λ = fct / (0.56 √fc′) ≤ 1.0 | λ = fct / (1.78 √fc′) ≤ 1.0 |
| Eq. (9-9) | fr = 0.62 λ √fc′ | fr = 2 λ √fc′ |
| Eq. (9-11) | h = ℓn (0.8 + fy/1,400) / [36 + 5β(αfm − 0.2)] ≥ 125 mm | h = ℓn (0.8 + fy/14,000) / [36 + 5β(αfm − 0.2)] ≥ 125 mm |
| Eq. (9-12) | h = ℓn (0.8 + fy/1,400) / (36 + 9β) ≥ 90 mm | h = ℓn (0.8 + fy/14,000) / (36 + 9β) ≥ 90 mm |
| Eq. (10-3) | As,min = (0.25 √fc′ / fy) bw d ≥ (1.4/fy) bw d | As,min = (0.8 √fc′ / fy) bw d ≥ (14/fy) bw d |
| Eq. (10-4) | s = 380 (280/fs) − 2.5 cc ≤ 300 (280/fs) | s = 380 (2,800/fs) − 2.5 cc ≤ 30 (2,800/fs) [as printed; MKS row mixes 380 and 30 — inconsistent units] |
| Eq. (10-17) | M2,min = Pu (15 + 0.03h) [mm] | M2,min = Pu (1.5 + 0.03h) [cm] |

### Chapter 11 (shear and torsion)
| Clause / Eq. | SI-metric | MKS-metric |
|---|---|---|
| 11.1.2 | √fc′ ≤ 8.3 MPa | √fc′ ≤ 27 kg/cm² |
| Eq. (11-3) | Vc = 0.17 λ √fc′ bw d | Vc = 0.53 λ √fc′ bw d |
| Eq. (11-4) | Vc = 0.17 (1 + Nu/(14Ag)) λ √fc′ bw d | Vc = 0.53 (1 + Nu/(140Ag)) λ √fc′ bw d |
| Eq. (11-5) | Vc = (0.16 λ √fc′ + 17 ρw Vu d/Mu) bw d ≤ 0.29 λ √fc′ bw d | Vc = (0.5 λ √fc′ + 176 ρw Vu d/Mu) bw d ≤ 0.93 λ √fc′ bw d |
| Eq. (11-7) | Vc = 0.29 λ √fc′ bw d √(1 + Nu/(3.5Ag)) | Vc = 0.93 λ √fc′ bw d √(1 + Nu/(35Ag)) |
| Eq. (11-8) | Vc = 0.17 (1 + Nu/(3.5Ag)) λ √fc′ bw d ≥ 0 | Vc = 0.53 (1 + Nu/(35Ag)) λ √fc′ bw d ≥ 0 |
| 11.4.4 (c) | 0.33 √fc′ bw d | 1.1 √fc′ bw d |
| 11.4.5 (a)(6) | φ 0.17 √fc′ bw d | φ 0.53 √fc′ bw d |
| Eq. (11-9) | Av,min = 0.062 √fc′ bw s/fyt ≥ 0.35 bw s/fyt | Av,min = 0.2 √fc′ bw s/fyt ≥ 3.5 bw s/fyt |
| Eq. (11-12) | Vs = Av fy sin α ≤ 0.25 √fc′ bw d | Vs = Av fy sin α ≤ 0.8 √fc′ bw d |
| 11.4.6 (i) | 0.66 √fc′ bw d | 2.2 √fc′ bw d |
| Eq. (11-13) | Tu < φ 0.083 λ √fc′ (Acp²/pcp) | Tu < φ 0.27 λ √fc′ (Acp²/pcp) |
| Eq. (11-14) | Tu < φ 0.083 λ √fc′ (Acp²/pcp) √(Nu/(0.33 Ag λ √fc′)) [SI printed without "1 +" — likely typo] | Tu < φ 0.27 λ √fc′ (Acp²/pcp) √(1 + Nu/(Ag λ √fc′)) |
| Eq. (11-15) | Tu = φ 0.33 λ √fc′ (Acp²/pcp) | Tu = φ λ √fc′ (Acp²/pcp) |
| Eq. (11-16) | Tu = φ 0.33 λ √fc′ (Acp²/pcp) √(1 + Nu/(0.33 Ag λ √fc′)) | Tu = φ λ √fc′ (Acp²/pcp) √(1 + Nu/(Ag λ √fc′)) |
| Eq. (11-17) | √[(Vu/(bw d))² + (Tu ph/(1.7 Aoh²))²] ≤ φ (Vc/(bw d) + 0.66 √fc′) | √[(Vu/(bw d))² + (Tu ph/(1.7 Aoh²))²] ≤ φ (Vc/(bw d) + 2 √fc′) |
| Eq. (11-18) | (Vu/(bw d)) + (Tu ph/(1.7 Aoh²)) ≤ φ (Vc/(bw d) + 0.66 √fc′) | (Vu/(bw d)) + (Tu ph/(1.7 Aoh²)) ≤ φ (Vc/(bw d) + 2 √fc′) |
| Eq. (11-22) | (Av + 2At) = 0.062 √fc′ bw s/fyt ≥ 0.35 bw s/fyt | (Av + 2At) = 0.2 √fc′ bw s/fyt ≥ 3.5 bw s/fyt |
| Eq. (11-23) | Aℓ,min = 0.42 √fc′ Acp/fy − (At/s) ph (fyt/fy); At/s ≥ 0.175 bw/fyt | Aℓ,min = 1.33 √fc′ Acp/fy − (At/s) ph (fyt/fy); At/s ≥ 1.75 bw/fyt |
| 11.6.5 | (3.3 + 0.08 fc′) Ac ; 11 Ac ; 5.5 Ac | (34 + 0.08 fc′) Ac ; 110 Ac ; 55 Ac |
| 11.7.3 | φ 0.83 √fc′ bw d | φ 2.65 √fc′ bw d |
| 11.8.3 | (3.3 + 0.08 fc′) bw d ; 11 bw d | (34 + 0.08 fc′) bw d ; 110 bw d |
| 11.8.3 (b)(2) | (5.5 − 1.9 av/d) bw d | (55 − 20 av/d) bw d |
| 11.9.3 | 0.83 √fc′ h d | 2.65 √fc′ h d |
| 11.9.5 | 0.17 λ √fc′ h d | 0.53 λ √fc′ h d |
| Eq. (11-26) | Vc = 0.27 λ √fc′ h d + Nu d/(4ℓw) | Vc = 0.88 λ √fc′ h d + Nu d/(4ℓw) |
| Eq. (11-27) | Vc = [0.05 λ √fc′ + ℓw (0.1 λ √fc′ + 0.2 Nu/(ℓw h)) / (Mu/Vu − ℓw/2)] h d | Vc = [0.16 λ √fc′ + ℓw (0.33 λ √fc′ + 0.2 Nu/(ℓw h)) / (Mu/Vu − ℓw/2)] h d |
| Eq. (11-30) | Vc = 0.17 (1 + 2/β) λ √fc′ bo d | Vc = 0.53 (1 + 2/β) λ √fc′ bo d |
| Eq. (11-31) | Vc = 0.083 (αs d/bo + 2) λ √fc′ bo d | Vc = 0.27 (αs d/bo + 2) λ √fc′ bo d |
| Eq. (11-32) | Vc = 0.33 λ √fc′ bo d | Vc = λ √fc′ bo d |
| 11.11.3 (a) | 0.17 λ √fc′ bo d | 0.53 λ √fc′ bo d |
| 11.11.3 (b) | 0.5 √fc′ bo d | 1.6 √fc′ bo d |
| 11.11.4 (g) | 0.33 √fc′ bo d ; 0.58 √fc′ bo d | 1.1 √fc′ bo d ; 1.9 √fc′ bo d |
| 11.11.5 (a) | 0.25 λ √fc′ bo d ; 0.66 λ √fc′ bo d ; 0.17 √fc′ bo d | 0.8 λ √fc′ bo d ; 2.1 λ √fc′ bo d ; 0.53 √fc′ [bo d omitted as printed] |
| 11.11.5 (b) | φ 0.5 √fc′ | φ 1.6 √fc′ |
| 11.11.5 (d) | φ 0.17 λ √fc′ | φ 0.53 λ √fc′ |
| 11.11.7 (b)(2) | φ 0.17 λ √fc′ | φ 0.53 λ √fc′ |
| 11.11.7 (c) | φ 0.33 λ √fc′ | φ 1.1 λ √fc′ |

### Chapter 12 (development and splices)
| Clause / Eq. | SI-metric | MKS-metric |
|---|---|---|
| 12.1.2 | √fc′ ≤ 8.3 MPa | √fc′ ≤ 26.5 kg/cm² |
| 12.2.2 (≤20 mm, good conditions) | ℓd = [fy ψt ψe / (2.1 λ √fc′)] db | ℓd = [fy ψt ψe / (6.6 λ √fc′)] db |
| 12.2.2 (≥22 mm, good conditions) | ℓd = [fy ψt ψe / (1.7 λ √fc′)] db | ℓd = [fy ψt ψe / (5.3 λ √fc′)] db |
| 12.2.2 (≤20 mm, other cases) | ℓd = [fy ψt ψe / (1.4 λ √fc′)] db | ℓd = [fy ψt ψe / (4.4 λ √fc′)] db |
| 12.2.2 (≥22 mm, other cases) | ℓd = [fy ψt ψe / (1.1 λ √fc′)] db | ℓd = [fy ψt ψe / (3.5 λ √fc′)] db |
| Eq. (12-1) | ℓd = [fy / (1.1 λ √fc′)] · ψt ψe ψs / ((cb + Ktr)/db) · db | ℓd = [fy / (3.5 λ √fc′)] · ψt ψe ψs / ((cb + Ktr)/db) · db |
| 12.3.2 | ℓdc = (fy / (4.2 λ √fc′)) db ≥ (0.043 fy) db | ℓdc = (fy / (13.3 λ √fc′)) db ≥ (0.0044 fy) db |
| Eq. (12-3) | ℓdh = [fy ψe / (4.2 λ √fc′)] db | ℓdh = [fy ψe / (13.3 λ √fc′)] db |
| Eq. (12-4) | ℓdt = [fy ψe / (5.3 λ √fc′)] db | ℓdt = [fy ψe / (16.7 λ √fc′)] db |
| 12.7.2 | (fy − 240)/fy | (fy − 2,460)/fy |
| Eq. (12-5) | ℓd = 3.3 (Ab/s) fy/(λ √fc′) | ℓd = (Ab/s) fy/(λ √fc′) |
| 12.9.5 (b) | 0.41 bw s / fyt | 4.2 bw s / fyt |
| 12.12.2 (b) | (fyt / (5.9 λ √fc′)) db | (fyt / (18.9 λ √fc′)) db |
| 12.15.1 | 0.071 fy db ; (0.13 fy − 24) db | 0.0073 fy db ; (0.013 fy − 24) db |

Note: the Ktr expression (12-2), ℓ limits (300 mm, 200 mm, 150 mm) and factors (ψ, λ) are unit-independent/length-only and are not repeated in the MKS table; length units remain mm in both columns.

### Chapters 17 and 21
| Clause / Eq. | SI-metric | MKS-metric |
|---|---|---|
| 17.5.3 (a) and 17.5.3 (b) | 0.55 bv d | 5.6 bv d |
| 17.5.3 (c) | (1.8 + 0.6 ρv fy) λ bv d ≤ 3.5 bv d | (18 + 0.6 ρv fy) λ bv d ≤ 35 bv d |
| Eq. (21-6) | Nb = kc λa √fc′ hef^1.5 ; kc = 10 or 7 | Nb = kc λa √fc′ hef^1.5 ; kc = 10 or 7 |
| Eq. (21-7) | Nb = 3.9 λa √fc′ hef^(5/3) | Nb = 5.8 λa √fc′ hef^(5/3) |
| Eq. (21-33) | Vb = 0.6 (ℓe/da)^0.2 √da λa √fc′ (ca1)^1.5 | Vb = 1.9 (ℓe/da)^0.2 √da λa √fc′ (ca1)^1.5 |
| Eq. (21-34) | Vb = 3.7 λa √fc′ (ca1)^1.5 | Vb = 3.8 λa √fc′ (ca1)^1.5 |
| Eq. (21-35) | Vb = 0.66 [(ℓe/da)^0.2 √da] λa √fc′ (ca1)^1.5 | Vb = 2.1 [(ℓe/da)^0.2 √da] λa √fc′ (ca1)^1.5 |

[NOTE] Appendix conversion uses 1 MPa ≈ 10 ksc for linear terms and 3.18 (≈√10.2) for √fc′ terms; some coefficients are rounded inconsistently (e.g. 12.1.2 gives 26.5 vs 11.1.2 gives 27; 21-34 converts 3.7→3.8 while 21-6 kc is unchanged; kc should strictly change with units). Values above are reproduced as printed.

---

## Summary of differences from ACI 318-11 noted in this range
1. Clause numbering in Ch.12 shifted by −1 from 12.9 onward (ACI 12.9 strand development omitted).
2. 12.2.4(d): λ "not exceeding 0.75" (ACI: 0.75).
3. 12.3.2: text states constant "0.0003 mm²/N" (typo from ACI in-lb); equation uses 0.043.
4. 12.6.2: λ included in headed-bar ℓdt equation (ACI has no λ).
5. 12.9.5(b): wording "shall not exceed 0.41bws/fyt" vs ACI "not less than" (likely translation error).
6. 12.12.5: closed-stirrup splice depth limit 500 mm (ACI 450 mm/18 in.).
7. 12.18.2: minimum overlap 150 mm (ACI 50 mm/2 in.).
8. 18.4.3: test load 0.85(1.4D + 1.7L) (ACI 318-99 form; ACI 318-11 uses 1.15D+1.5L+... / 1.3D).
9. Ch.18: no core-based acceptance criteria or φ increase (ACI 20.2.3–20.2.5).
10. Ch.19: only scope clauses; all seismic analysis/design/detailing delegated to DPT มยผ. 1301/1302-61 (ACI Ch.21 detailing not reproduced).
11. Cross-reference typos: 12.13.3(e) cites (c) for (d) and 12.14.4 for 12.14.5; 12.16.2(a) cites "12.16.2.5(e)"; 12.10.3 definition list prints Mu for Mn.
