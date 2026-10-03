# Slab detailing sources: DPT 1301/1302-61, EIT 011008-21 and the TATA RC detailing handbook (extracts)

Working extracts behind the typical slab detail sheets STR-ST-1121 ff. (generator `jobs/typical_details/td_slabs.py`, rules in `TYPICAL_DETAILS_INSTRUCTION.md`).

- Part A: DPT 1301/1302-61 - flat slabs in moment frames (5.2.12), gravity slab-column connections, diaphragms. PDF pages.
- Part B: EIT 011008-21 - slab thickness (9.5), reinforcement (7.12, 13.3), Fig 13.3.8, punching (11.11), openings (13.4). PDF pages.
- Part C: TATA handbook - Thai office practice (cut-offs Sn/4, Sn/3, corner bars, openings, steps, slab on ground, flat slab). Printed pages (PDF = printed + 8).

Values are as printed; suspected misprints are flagged in each part.

---

# Part A. DPT 1301/1302-61 (seismic) - slab clauses


Source: `G:\My Drive\##Textbook\DPT\1301-1302-64.pdf` (มยผ. 1301/1302-61, ฉบับปรับปรุงครั้งที่ 1).
Page refs are **PDF pages**. Printed page = PDF − 14 (e.g. PDF 138 = printed 124).
Text comes from `dpt.txt`. Every equation and figure was checked on page renders `dsl_<page>.png` (53–57, 60, 62, 63, 67, 70–74, 77, 114, 137–143, 155). Zoom crops: `dsl_138_fig.png`, `dsl_139_a.png`, `dsl_139_b.png`.
All wording is paraphrased. SI equations are given first; the standard's metric (kgf, cm, ksc) version follows in brackets.
SDC letters: ข = B, ค = C, ง = D.

Search coverage: full-text search for พื้น (excluding พื้นดิน/พื้นที่/พื้นฐาน/พื้นผิว), แผ่นพื้น, พื้นไร้คาน, ไดอะแฟรม, แถบเสา, แถบกลาง, ทะลุ, เจาะช่อง, องค์อาคารเชื่อม, คอร์ด, ทับหน้า/Topping, หล่อสำเร็จ, คานยึดควบ. Every hit is listed below or noted as irrelevant: p.64 (roof-mass exception), p.91 (floor displacements in modal analysis), p.159 (openings in walls, not slabs), p.164 and p.172 (nonstructural items).

---

## 0. Scope and fallback

### 5.2 intro (p.104)
- RC buildings and foundations resisting earthquakes must be designed and detailed to this standard, to the referenced standards, and to the extra rules of Ch. 5.
- **Ch. 5 does NOT cover structural systems built from precast elements, or composite systems. The one exception is precast concrete piles.** So precast planks, topping slabs over precast, and hollow-core diaphragms get no Ch. 5 detailing.

### 5.2.1 Other standards (p.104)
- Detail reinforcement to this standard. **Where this standard is silent, follow ACI 318** or another accepted standard.

### 2.3.1.3 Precast systems (p.57)
- This is a general performance clause only, with no slab details. Precast members and their connections must have enough strength and ductility-oriented detailing for the seismic level. They must carry axial force, shear, flexure and torsion.
- Design must follow accepted standards. A novel form needs study or test evidence that it matches the chosen system's R/Ω0/Cd behaviour.
- Where one direction's strength is much weaker than the other, consider **progressive collapse** and design against it.

---

## 1. Which systems allow flat slab / flat plate frames

### Table 2.3-1 (pp.53–55): R, Ω0, Cd and permitted SDC
**No flat-slab, flat-plate or "slab-column frame" system is listed** (verified on page images `dsl_53–55`). The RC moment frame rows are:

| System (Table 2.3-1 group 3) | R | Ω0 | Cd | B | C | D |
|---|---|---|---|---|---|---|
| Special RC MRF (cast-in-place or precast ++) | 8 | 3 | 5.5 | ✓ | ✓ | ✓ |
| Intermediate RC MRF / "ductile MRF with limited ductility" | 5 | 3 | 4.5 | ✓ | ✓ | * |
| Ordinary RC MRF | 3 | 3 | 2.5 | ✓ | ✗ | ✗ |

Legend: ✓ = permitted, ✗ = prohibited, * = see 2.3.1.2, ++ = see 2.3.1.3.

Other rows that can carry a flat-slab gravity system beside walls:
- Building frame system: special RC shear wall R = 6 (B/C/D ✓); ordinary RC shear wall R = 5 (B, C ✓; D *).
- Bearing wall system: ordinary RC shear wall R = 4 (D *); special RC shear wall R = 5 (all ✓).
- Dual with special MRF, frame carrying at least 25 %: special wall R = 7; ordinary wall R = 6 (D *).
- Dual with intermediate MRF: special wall R = 6.5 (all ✓); ordinary wall R = 5.5 (D *).
- Shear-wall–frame interactive system (ordinary MRF + ordinary wall): R = 4.5, B only.

**Inferences, not stated in DPT:**
- A two-way slab without beams can be part of the SFRS only as the "beam" of an ordinary or intermediate RC MRF. This is confirmed indirectly by 5.2.2(ง), 5.2.7.2 and 5.2.7.4.4, which name flat slabs inside intermediate-frame clauses.
- Special MRF members must satisfy the beam geometry of 5.2.8.1: b_w ≥ lesser of (0.3h, 250 mm), l_n ≥ 4d, and so on. A slab cannot meet this, so DPT has **no special flat-slab frame**. The same holds in ACI.

### 2.3.1.2 Height limits in SDC D (pp.55–56)
- The following may be used in **SDC D** only up to these heights:
  - **40 m**: intermediate/limited-ductility RC MRF and intermediate steel MRF.
  - **60 m**: ordinary RC shear walls.
- For strength design, increase the seismic design forces for members by **40 %**. No increase is needed for deformation (drift) calculations.
- Taller buildings need a limit-state check (strains, shear and so on) under the design and maximum considered earthquake, by accepted methods or test evidence.

### 5.2.2 System requirements (pp.104–105)
- **(ก) SDC B:** ordinary, intermediate or special systems are permitted. Forces and detailing follow the standard for the chosen system.
- **(ข) SDC C:** intermediate or special MRF, or ordinary/intermediate/special RC structural walls.
- **(ค) SDC D:**
  - Use a special MRF, special walls, or the 2.3.1.2 route. Diaphragms, trusses and foundations must also be designed and detailed for seismic resistance.
  - **Members or parts not designed as part of the SFRS** must be designed for gravity load combined with the effects of the **design lateral displacement**.
- **(ง) Intermediate MRF in "watch areas" (บริเวณเฝ้าระวัง, defined on p.18 as areas where earthquakes may affect building stability):**
  - At minimum, comply with 5.2.7.4 (column hoops).
  - **If the member is a two-way slab without beams, 5.2.12 must also be satisfied.**

### 2.3.4 Shared members (p.59)
- A member shared between two lateral systems is detailed to the system with the **highest R**.

### 2.3.5 Dual systems (p.59)
- The MRF must resist at least **25 %** of the total design seismic force.
- Forces are distributed by relative stiffness.

---

## 2. Slab-column frames as gravity-only (non-SFRS) systems

### 2.11.5 Deformation compatibility (p.77)
- **SDC D:** every member not part of the SFRS must be designed for gravity load together with the member forces caused by a storey drift equal to **Δ** (the design storey drift).
- **Members of an RC building frame that are not part of the SFRS must satisfy ACI 318-14 Section 18.14.** DPT cites this explicitly (verified on `dsl_77`).
- ACI 318-14 §18.14 includes the slab-column connection rule §18.14.5 (shear reinforcement v_s ≥ 3.5√f'c psi extending ≥ 4h, unless the drift/gravity-shear limit is met). DPT also restates this rule itself in 5.2.12.1.4, below.
- **Correction to `SOURCES_BEAM_DETAILING.md` §0:** that file calls 5.2.2(ค) "the only provision on non-SFRS members". It is not. **2.11.5 also invokes ACI 318-14 §18.14.**

### Table 2.11-1 Allowable storey drift Δa (p.77)
Values are for Importance Category I–II / III / IV:

| Structure | I–II | III | IV |
|---|---|---|---|
| Not masonry shear wall, ≤ 4 storeys, with partitions, ceilings and exterior walls designed for large drift | 0.025 h_sx | 0.020 h_sx | 0.015 h_sx |
| Cantilever masonry shear wall | 0.010 h_sx | 0.010 h_sx | 0.010 h_sx |
| Other masonry shear wall | 0.007 h_sx | 0.007 h_sx | 0.007 h_sx |
| All other structures | 0.020 h_sx | 0.015 h_sx | 0.010 h_sx |

h_sx = storey height below level x.

### 5.2.12.1.4 Slab-column connections of flat slabs NOT part of the lateral system (p.142), the punching–drift rule
- Provide **slab shear reinforcement with V_s ≥ 0.3 √f'c b0 d** [metric: **0.93 √f'c b0 d**].
- The reinforcement must extend from the support face for at least **4 × slab thickness**.
- The reinforcement may be omitted if **either** of the following is met:
  1. Punching shear stress on the critical section from V_u, plus the stress from unbalanced moment transferred under the **design lateral displacement**, does not exceed the EIT RC strength-design shear strength. Or:
  2. Design storey drift ≤ **the larger of 0.005 h_storey and [0.035 − 0.05 (V_u/φV_c)]**.
- **Design displacement:**
  - When seismic forces follow the Ministerial Regulation (กฎกระทรวง), take the design displacement as the elastic displacement of the lateral system under those forces × **3/K**. K is the Regulation's structural coefficient for horizontal force.
  - When forces are computed at the strength limit state with elastic analysis, multiply displacements by the appropriate deflection amplification factor (C_d).
- V_u and φV_c are computed per 5.2.12.1.2: gravity 1.2D + 1.0L, φ = 0.75, V_c by Eq. 5.2-21…24.
- [FLAG] The metric coefficient 0.93 is slightly below the exact conversion of 0.3 (≈ 0.96). The same constant gives 1/3 → 1.06, which is consistent. The printed value 0.93 is recorded as is.
- ACI analogue: 318-11 §21.13.6 / 318-14 §18.14.5 (3.5√f'c psi ≈ 0.29√f'c MPa; 4h; drift 0.035 − 0.05 v_ug/φv_c ≥ 0.005).

### 5.2.7.4.4 Joint hoops, exception (p.114)
- Column–flat-slab joints need joint hoops **A_v ≥ (1/3) c1 s / f_y** [metric **3.5 c1 s/f_y**] (Eq. 5.2-6). They are placed within the column over a depth ≥ the deepest member framing into the joint.
- **Exception:** a column–slab joint that is **not a main part of the SFRS** and is restrained on all 4 sides by beams or slabs of about equal depth. Full column clause: see `SOURCES_COLUMN_DETAILING.md`.

---

## 3. 5.2.12 Two-way RC slabs without beams (flat slabs / flat plates) (pp.137–143)

**Scope (p.137):** reinforcement in two-way RC slabs without beams that are **considered part of a moment-resisting frame resisting seismic forces** must be detailed as follows (Fig. 5.2-14).
- The clause does not name a frame type. It sits in general 5.2, but 5.2.2(ง) makes it mandatory for intermediate frames in watch areas.
- It corresponds to ACI 318-11 §21.3.6 (intermediate frames).

### 5.2.12 items (1)–(7) (p.138)
1. **All** reinforcement computed to resist **M_s** must be placed within the **column strip**. M_s is the part of the slab moment transferred to the support.
2. Reinforcement resisting the fraction **γ_f M_s** must lie within the **effective width** (Fig. 5.2-14(ก)).
3. **At least one-half** of the column-strip reinforcement at the support must lie within the effective width of the slab.
4. **At least one-quarter** of the column-strip **top** reinforcement at the support must be **continuous over the full span length**. There must also be **at least 2 top bars passing through the column line in each direction** (DPT wording is "วางผ่านแนวเสา", i.e. through the column line; ACI says "through the column core").
5. **Continuous bottom** reinforcement in the column strip must be **≥ one-third** of the column-strip **top** reinforcement at the support.
6. **At least one-half** of the **bottom** reinforcement at **mid-span** must be continuous and able to develop **yield strength at the face of the support**.
7. At **discontinuous slab edges**, top and bottom reinforcement at the support must develop **yield at the face of the support**.

- DPT does not define the column strip or middle strip. Use EIT/ACI: column strip width = 0.25 l1 or 0.25 l2 each side of the column centreline, whichever is smaller.
- DPT gives **no numeric effective-width text**. The effective width is only shown in Fig. 5.2-14(ก).

### Fig. 5.2-14(ก) "Effective width" (p.138), plan view
- A partial slab panel, with break lines top, bottom, left and right, labelled "slab, thickness t" (แผ่นพื้น ความหนา t). A solid grey rectangular **column** (เสา) sits at the centre.
- Column dimensions: **c1** (horizontal) and **c2** (vertical).
- Two dashed vertical lines sit **1.5t** outside each column face in the c1 direction, dimensioned "1.5t | c1 | 1.5t" at the bottom. The band between them is labelled "effective width" (ความกว้างประสิทธิผล) at the top.
- Two dashed horizontal lines sit **1.5t** outside each column face in the c2 direction, dimensioned "1.5t | c2 | 1.5t" on the left. That band is labelled "effective width" (text rotated) on the right.
- **Effective width = c + 1.5t on each side = c2 + 3t** (or c1 + 3t in the other direction). This equals ACI "c2 + 3h".

### Fig. 5.2-14(ข) "Reinforcement details in the column strip" (p.139), elevation
- A slab spans between an **exterior (edge) column** on the left and an interior column on the right. Both columns are drawn with centrelines and break lines above and below. The span has a break at mid-length.
- **Top bars:**
  - At the exterior column, top bars run to the outer face of the column and turn down with a **90° hook**, lying just inside the slab's outer edge.
  - Some top bars stop part-way into the span.
  - One top bar layer is labelled "reinforcement ≥ **A_s/4** (continuous over the full span)". A_s here is the column-strip top steel at the support.
  - Past the mid-span break, the top bar continues to the interior column.
- **Bottom bar:** runs the full span. At the exterior edge it turns up with a **90° hook** at the column's outer face. It is labelled "reinforcement ≥ **A_s/3** (continuous over the full span)".
- A leader to both top and bottom bars at the exterior support reads: "top and bottom bars have sufficient length to develop strength up to the (support face) point". The text ends "…ได้ถึงจุด". The noun that follows is cut off on the page; from item (7) it means the face of the support.

### Fig. 5.2-14(ค) "Reinforcement details in the middle strip" (p.139), elevation
- The same two columns are shown.
- **Top bar:** at the exterior edge it is hooked down 90° and stops a short distance into the span. The top bar resumes near the interior column.
- **Bottom:**
  - A continuous bottom bar runs the full length and is hooked up 90° at the exterior edge. It is labelled "reinforcement ≥ **A_s/2** (continuous over the full span)".
  - A **shorter additional bottom bar** sits around mid-span. A small circle on it is labelled "reinforcement **A_s**", meaning A_s here is the total mid-span bottom steel.
- The same leader note says top and bottom bars must have sufficient embedment to develop strength at the support face.
- [NOTE] Items (6)/(7) and (ค) apply the ½-bottom-continuous rule to the middle strip as drawn. Text item (6) is not limited to one strip.

### 5.2.12.1 Punching shear in two-way slabs without beams (pp.140–142)
- **5.2.12.1.1:** punching shear stress on the critical section around the column from gravity load, plus the stress from **unbalanced moment** transferred between slab and column, must not exceed the shear strength in the **EIT RC strength-design standard**.
- **5.2.12.1.2 Gravity shear ratio limit:**
  - **V_u/φV_c ≤ 0.4.**
  - V_u is the factored shear on the critical section from gravity load **1.2D + 1.0L**.
  - The live-load factor may drop from **1.0 to 0.5** where live load < **4.9 kN/m² (500 kgf/m²)**. This reduction is not allowed for **car parks** or **places of public assembly**.
  - **φ = 0.75.**
  - V_c is computed as follows.
  - (1) **RC flat slab:** V_c = least of:
    - (ก) **V_c = (1 + 2/β_c) √f'c b0 d / 6** (5.2-21) [metric 0.27 (2 + 4/β_c) √f'c b0 d]
    - (ข) **V_c = (α_s d/b0 + 2) √f'c b0 d / 12** (5.2-22) [metric 0.27 (α_s d/b0 + 2) √f'c b0 d]
      - α_s = **40** interior, **30** edge, **20** corner columns.
    - (ค) **V_c = (1/3) √f'c b0 d** (5.2-23) [metric 1.06 √f'c b0 d]
  - (2) **Prestressed flat slab:**
    - **V_c = (β_p √f'c + 0.3 f_pe) b0 d + V_p** (5.2-24) [metric (0.27 β_p √f'c + 0.3 f_pe) b0 d + V_p]
    - β_p = lesser of **0.29** and **(α_s d/b0 + 1.5)/12** [metric: lesser of 3.5 and (α_s d/b0 + 1.5)].
    - α_s is as above.
    - [FLAG] The symbol printed is "f_pe". ACI uses f_pc (average precompression). This is probably a notation slip; recorded as printed.
  - [NOTE] The 1.2D + 1.0L factors are ACI-2008+ style. DPT's own seismic combinations (2.5-1) use 0.75(1.4D + 1.7L) + 1.0E.
- **5.2.12.1.3 Exemption from 5.2.12.1.2:**
  - The 0.4 limit need not be checked when the **factored two-way shear stress at its maximum location** is ≤ **½ φv_n**.
  - That stress is the **part caused by earthquake and transferred by eccentricity of shear**.
  - (1) Without shear reinforcement: **φv_n = φV_c/(b0 d)** (5.2-25).
  - (2) With shear reinforcement other than **shearheads**: **φv_n = φ(V_c + V_s)/(b0 d)** (5.2-26).
  - ACI 318-11 §21.3.6.8 instead waives the 0.4 limit if §21.13.6 is met. DPT's "½ φv_n" exemption has no exact ACI counterpart.
- **5.2.12.1.4:** see §2 above (non-SFRS connections, punching–drift rule).

### 5.2.12.2 Progressive collapse, integrity bottom bars (pp.142–143)
- At **interior supports** of flat slabs, bottom reinforcement must **pass through or be anchored into the column core** in **each direction**. Its area must be at least:
  - **A_sm = 0.5 w_u L1 L2 / (0.9 f_y)** (5.2-27)
  - w_u = uniformly distributed factored load, but **not less than 2 × service dead load**.
  - L1 and L2 are not defined in the clause. Presumably they are the centre-to-centre spans in the two directions. [FLAG: undefined]
- At **edge** supports provide **≥ 2/3 A_sm**; at **corner** supports provide **≥ 1/2 A_sm**. These bars must also pass through or anchor into the column.
- The **continuous column-strip bottom bars of 5.2.12 item (5)** may be counted as part of A_sm.
- This has no ACI 318 counterpart. ACI has only the structural-integrity rule: 2 column-strip bottom bars through the core, 318-11 §13.3.8.5. DPT's rule resembles CSA A23.3 integrity steel in intent [interpretation].

### 5.2.7.2 Shear strength of intermediate-frame members, including flat slabs (p.112)
- The design shear strength of **beams, columns and two-way slabs without beams** resisting earthquake must be ≥ **either**:
  - **5.2.7.2.1:** shear when both member ends reach **nominal moment strength M_n**, plus gravity shear (Fig. 5.2-2); or
  - **5.2.7.2.2:** maximum shear from design combinations with **E doubled (2E)**.
- For a flat slab this is the one-way (beam) shear capacity rule. Punching is governed by 5.2.12.1.

---

## 4. Slab as beam flange: strong-column/weak-beam (5.2.9.2.2, p.124)
- **Σ M_nc ≥ (6/5) Σ M_nb** (5.2-11), taken at the joint faces. Column M_n is taken at the axial load giving the lowest moment.
- For **T-beams whose flange (slab) is in tension**, the slab reinforcement within the **effective slab width** must be included in the beam's M_nb.
- **DPT does not define that effective width.** Fall back to EIT 8.11 / ACI (318-14 §18.7.3.2 → §6.3.2 flange width).
- Column and beam moments are assumed to act in opposite senses.
- 5.2.9.2.1 / 5.2.9.2.3: a column failing 5.2.9.2.2 is ignored for lateral strength and stiffness (treated as non-SFRS). Alternatively, confine it over its full height per 5.2.9.4.1–.3.
- **Drafting consequence:** slab top bars parallel to a special-frame beam near the column are part of the capacity check. Don't add un-scheduled slab top steel there, because it raises M_nb.

## 5. Other slab-adjacent member items
- **5.2.8.3.6 (p.123):** special-frame beam hoops may be a stirrup with seismic hooks plus a crosstie cap. Where the longitudinal bars held by crossties are restrained by a **slab on one side only**, the crossties' **90° hooks must all be on the slab side**. Consecutive crossties otherwise alternate their 90° hooks.
- **Coupling beams (5.2.11.7, Fig. 5.2-13, pp.136–137):** beams only. **No "coupling slab" provision exists.**
- **Annex ข.2 (pp.154–155), advisory, not mandatory:**
  - Slabs and beams spanning between walls may be damaged by wall-to-wall interaction through the floor. That interaction also raises wall shear and axial force.
  - Recommendation: include slab and beam coupling of walls in analysis even when they are not designated as SFRS.
  - **Fig. ข.2-1 (p.155):**
    - Left: an isolated cantilever concrete wall under seismic arrows, base shear **V1**, plastic moment **M_p**.
    - Right: the same wall inside a frame of beams and columns ("considering beam/wall frame effects"). The floors deform in double curvature, with vertical reactions at the outer columns and base shear **V2**, same M_p.
    - Boxed conclusion: **V1 < V2**.
- **2.8.3 Model stiffness (p.70):** where no detailed analysis is made, use I_eff = 0.35 I_g for beams, 0.70 I_g and A_eff = 1.0 A_g for columns, 0.70 I_g for uncracked walls, 0.35 I_g for cracked walls, and **I_eff = 0.25 I_g for flat slabs (แผ่นพื้นไร้คาน)**.

---

## 6. Diaphragms (2.2.3, 2.4.1, 2.4.2, 2.4.3, 2.8.3, 2.9, 2.10, 2.11)

### Definitions (1.2, pp.18–19; symbols p.21–23)
- **Diaphragm:** a horizontal or near-horizontal system that transfers lateral force to the vertical elements of the SFRS. It includes horizontal bracing.
- **Collector (องค์อาคารเชื่อม):** a member transferring lateral force from the diaphragm into the SFRS.
- **Anchorage (สมอยึด):** a part or device connecting a structural wall to the diaphragm.
- Symbols:
  - D_e = diaphragm depth parallel to the force.
  - S = diaphragm length perpendicular to the force.
  - F_px = diaphragm design force (N).
  - w_px = load tributary to the diaphragm at level x.
- "Chord" (คอร์ด) appears only in 2.10.3.1 and is not defined.

### 2.2.3 Support connections (p.52)
- Parts such as secondary beams or trusses that transfer force to other members, or that are attached to a slab acting as a diaphragm, need connections designed for the horizontal force that develops.
- Where the part attaches directly to the diaphragm slab, design it for an in-plane horizontal force ≥ **5 %** of its vertical (D + L) support reaction.

### 2.4.1 Diaphragm flexibility (pp.59–60)
- There are three types: rigid, semi-rigid and flexible. Analysis must reflect relative stiffness, and semi-rigid diaphragms must be modelled.
- **2.4.1.1 Flexible:** untopped steel deck or timber decking may be taken as flexible when:
  1. it sits in a structure with concrete, masonry, steel or composite shear walls, or concrete, steel or composite braced frames; or
  2. it is in a 1–2 storey small residence; or
  3. it is in light-frame construction **without topping**, with drift within limits.
- **2.4.1.2 Rigid:** a **cast-in-place concrete slab** or **concrete-filled metal deck** with **S/D_e ≤ 3** (Fig. 2.4-1), in a plan-regular building.
- **2.4.1.3 Check:** otherwise the diaphragm may be taken as flexible if its maximum in-plane deflection under equivalent static seismic force > **2 × average storey drift** of the attached vertical SFRS.
- **Fig. 2.4-1 (p.60):**
  - An isometric rectangular floor plate on walls. Length **S** runs along the long edge; depth **De** runs across. A seismic force arrow ("แรงแผ่นดินไหว") points along De.
  - The deflected plate is drawn with an arc. One leader marks the "maximum in-plane diaphragm deflection" at mid-length. Another marks the "average storey drift" at the supported ends.

### 2.4.2.1 Horizontal irregularities relevant to slabs (pp.60–63)
- **(2) Re-entrant corner:** a projection beyond the corner > **15 %** of the plan dimension in that direction.
- **(3) Diaphragm discontinuity:**
  - abrupt discontinuity or stiffness change, **including openings > 50 % of the gross floor (diaphragm) area**; or
  - effective diaphragm stiffness changing by > **50 %** from one storey to the next.
- **Fig. 2.4-2 (pp.62–63):**
  - **(ก) Torsional:**
    - Plan: a rectangle rotated about CR. Vertical-element walls (thick lines) are at the left end.
    - δ2 > 1.2 (δ1 + δ2)/2.
    - CR = centre of rigidity, CM = centre of mass, V = seismic force.
  - **(ข) Re-entrant corners:** L, T and cross-shaped plans with isometric sketches.
    - L: a/A > 0.15 or b/B > 0.15.
    - T: a1/A > 0.15 or a2/A > 0.15, and b/B > 0.15.
    - Cross: a1/A or a2/A > 0.15, and b1/B or b2/B > 0.15.
    - Circles mark the re-entrant corners, including on H- and C-shaped plans.
  - **(ค) Diaphragm discontinuity:**
    - Left: a plan whose dotted "rigid diaphragm" region adjoins a cross-hatched "flexible diaphragm" region. Arrows point to the vertical SFRS elements along the perimeter.
    - Right: a rectangular floor X × Y with a central opening x × y, marked **xy > 0.5XY**.
  - **(ง) Out-of-plane offset:** an isometric sketch of shear walls offset between storeys.
  - **(จ) Nonparallel systems:** plans with a diamond opening, a chamfered corner and a trapezoidal plan. Lateral elements are shown as thick lines.

### 2.4.3(4) SDC D irregular buildings, connection force ×1.25 (p.66)
- Applies to SDC D buildings with horizontal irregularity 1ก, 1ข, 2, 3 or 4, or vertical irregularity 4. The following must resist the 2.9.1.1 diaphragm forces **× 1.25**:
  - (ก) diaphragm-to-vertical-element connections;
  - (ข) diaphragm-to-collector connections;
  - (ค) collector-to-vertical-element connections.
- Collectors and collector splices must also resist this force.
- Exception: the element is already designed for gravity + Ω0-amplified equivalent static seismic force.

### 2.8.3 Modelling (p.70)
- Buildings with horizontal irregularity 1ก, 1ข, 4 or 5 need a 3-D model (two horizontal translations plus torsion).
- Diaphragms that are neither rigid nor flexible (2.4) must be modelled with their in-plane stiffness.
- 4.4.2 (p.99), response-history analysis: model diaphragm flexibility where it is not rigid.

### 2.9.1 Diaphragm design (p.71)
- Diaphragms must resist the shear and bending stresses from seismic forces.
- At **discontinuities**, such as **openings** and **re-entrant corners**, forces transferred through the diaphragm must not exceed its **shear and tensile strength**.
- DPT gives **no reinforcement or trim-bar detail** for openings. Fall back to ACI 318-14 §18.12 / §12.
- **2.9.1.1 Design force:**
  - Floors and roofs acting as diaphragms resist analysis forces, but not less than:
  - **F_px = (Σ_{i=x..n} F_i / Σ_{i=x..n} w_i) · w_px** (2.9-1)
    - F_i = equivalent static force at level i (3.4).
    - w_i = effective weight at level i (2.8.2).
    - w_px = effective weight at level x within the tributary area of the SFRS that transfers force through that diaphragm.
  - **F_px ≥ 0.2 S_DS I w_px** (2.9-2).
  - F_px **need not exceed 0.4 S_DS I w_px** (2.9-3).
  - In the Bangkok basin, use S_a at 0.2 s (Figs. 1.4-6/1.4-7, Tables 1.4-4/1.4-5) in place of S_DS.
  - Where the diaphragm **transfers seismic force from columns or walls above to columns or walls below**, for example because of offsets, **add that transfer force** to Eq. 2.9-1.

### 2.9.2 Collectors (p.72)
- Where seismic force must be transferred from part of the building to the SFRS, provide **collector elements** of adequate strength.
- **SDC C and D:** collectors, collector-to-SFRS connections and collector-to-collector connections are designed for the maximum of:
  1. transfer force from equivalent static forces (Ch. 3) × **Ω0**, with gravity per 2.5.3;
  2. transfer force from Eq. 2.9-1 diaphragm forces × **Ω0**, plus gravity;
  3. transfer force from Eq. 2.9-2 diaphragm forces (≤ Eq. 2.9-3), plus gravity.
- 2.5.3 overstrength combinations (p.67):
  - strength design: **0.75(1.4D + 1.7L) + Ω0E**; **0.9D + Ω0E**;
  - ASD: 1.0D + 0.7Ω0E; 1.0D + 0.525Ω0E + 0.75L; 0.6D + 0.7Ω0E (ASD stresses may be raised 20 %, 2.5.4).
- **Fig. 2.9-1 (p.72), plan:**
  - A rectangular floor. On the left edge is a short **shear wall at the stair core** (a stair drawn beside it), with short wall stubs at the top and bottom of that edge.
  - **Dashed lines along the left edge**, running up and down from the stair wall, are labelled "collectors transferring force between diaphragm and wall".
  - On the right edge is a **full-length shear wall**, labelled "no collector required".
- DPT gives **no collector bar, splice or confinement detailing**. For slab-embedded collectors use ACI 318-14 §18.12.7 (transverse reinforcement when compressive stress > 0.2 f'c, splice and anchorage rules).

### 2.10 Structural walls and anchorage to diaphragms (pp.72–75)
- **2.10.1:** walls and their anchorage, including infill walls in frames, are designed for out-of-plane force **0.4 S_DS I × wall weight**, not less than **10 %** of wall weight. Connections must be ductile or have enough rotation capacity or strength for shrinkage, temperature and differential settlement.
- **2.10.2 Anchorage force (p.73):**
  - **F_p = 0.4 S_DS k_a I W_p ≥ 0.2 k_a I W_p** (2.10-1).
  - **k_a = 1.0 + L_f/100 ≤ 2.0**. This equation is also numbered "2.10-1"; [FLAG] it should be 2.10-2.
  - L_f = span (m) of a flexible diaphragm between vertical supports; **L_f = 0 for rigid diaphragms**.
  - W_p = tributary weight of the anchor.
  - Below roof level, F_p may be multiplied by **(1 + 2z/h)/3**.
  - Walls must be designed for bending between anchors where anchor spacing > **1.2 m**.
- **Fig. 2.10-1 (p.74):** a section of a cantilever wall from a hatched base with a floor/roof slab framing into it. An arrow on the slab points away from the wall. A dashed red circle marks the "anchorage point" (จุดยึด). The label reads "floor or roof bracing the wall".
- **2.10.3 Extra requirements for diaphragms in SDC C and D (pp.74–75):**
  - **2.10.3.1:**
    - Provide **reinforcement or devices giving continuous force transfer along the diaphragm edges or chords**, to distribute anchorage forces into the diaphragm. Transfer may be by bond, welding or mechanical devices.
    - **Sub-diaphragms** may be formed by adding **chords**. Their **length/width ratio must be ≤ 2.5:1**.
    - Embedment of bars or devices must be enough to transfer the force into the diaphragm.
  - **2.10.3.2:** design forces for steel elements of wall-anchorage systems × **1.4**. Bolts and reinforcing bars are excepted.
  - **2.10.3.3:** timber diaphragms (not relevant).
  - **2.10.3.4:** metal-deck diaphragms. The deck itself may not serve as the continuous tie perpendicular to its span.
  - **2.10.3.5:** embedded straps between diaphragm and concrete wall must engage the main reinforcement so force passes into the bars.
  - **2.10.3.6:** eccentric or non-perpendicular anchorage must be designed for the eccentricity.
  - **2.10.3.7:** where pilasters are used, anchorage forces on the floor/roof must not be reduced because of the pilaster design.

### 2.11.2 Diaphragm in-plane deflection (p.75)
- The in-plane diaphragm deflection under the design earthquake must not exceed the permissible deflection of the attached elements. That is the deflection at which they keep structural integrity and design capacity.

### 2.11.4 Members spanning between buildings (p.76)
- Vertical-support connections must accommodate the relative displacement given by the sum of:
  1. Eq. 3.7-1 displacement × 1.5 R/C_d;
  2. torsional displacement including accidental-torsion amplification;
  3. **diaphragm deflection**;
  4. the absolute sum, assuming the buildings move in opposite directions.
- This governs seat widths or slip joints of slabs spanning to an adjacent block.

### Topping slabs over precast
- **Not covered** (5.2 intro excludes precast systems).
- DPT mentions topping only in the diaphragm-flexibility context: untopped deck or light-frame without topping may be flexible (2.4.1.1); concrete-filled metal deck may be rigid (2.4.1.2).
- For composite or non-composite topping (thickness ≥ 50 / 65 mm, minimum steel, and so on) use **ACI 318-14 §18.12.4–18.12.7**.

---

## 7. What DPT does NOT cover for slabs → ACI 318 / EIT (per 5.2.1, 2.11.5)
1. Definition of column strip and middle strip, and slab moment distribution (DDM/EFM) → EIT Ch. 13 / ACI 318 Ch. 8 (-14).
2. Numeric effective-width text for 5.2.12 (figure only: c + 1.5t each side). γ_f and γ_v formulas → EIT 13.5.3 / ACI 8.4.2.3.
3. Slab minimum thickness, minimum/shrinkage steel, bar spacing, cover → EIT 9.5.3, 7.12, 13.3; EIT cover table.
4. Standard bar extensions and cut-off points for two-way slabs → EIT Fig. 13.3.8 / ACI Fig. 8.7.4.1.3a.
5. Structural-integrity bars for gravity flat slabs outside 5.2.12.2 → EIT 13.3.8.5 / ACI 8.7.4.2.
6. Punching shear reinforcement detailing: stirrup/stud layout, spacing ≤ d/2, first line ≤ d/2, shearheads → EIT 11.11 / ACI 22.6, 8.7.6–8.7.7.
7. Drop panels and shear caps: dimensions, h ≥ 1.25 h_slab, extent ≥ l/6 → EIT 13.2.5 / ACI 8.2.4.
8. Openings in slabs (sizes permitted in column/middle strip intersections, replacement bars) → EIT 13.4 / ACI 8.5.4. Diaphragm trim bars at openings → ACI 18.12.
9. Diaphragm reinforcement:
   - minimum thickness (ACI 18.12.6: ≥ 50 mm topping or cast-in-place);
   - minimum steel (shrinkage/temperature);
   - chord and collector bar detailing, splices;
   - boundary transverse reinforcement at σ > 0.2 f'c;
   - diaphragm shear strength V_n = A_cv(0.17λ√f'c + ρ_t f_y);
   - → ACI 318-14 §18.12 (and §12).
10. Topping slabs over precast (composite/non-composite) → ACI 18.12.4–18.12.5, 18.12.10 (-14).
11. Non-SFRS gravity frames in SDC D, all items except the slab-column punching rule restated in 5.2.12.1.4 → ACI 318-14 §18.14 (explicitly by 2.11.5).
12. Slab steps, slab-edge beams, cantilever slab detailing, joist slabs, post-tensioned slab tendon layout (except the 5.2-24 V_c equation) → EIT/ACI.
13. Slab flange effective width for 5.2.9.2.2 → EIT 8.11 / ACI 6.3.2 (-14).
14. Coupling slabs: no provision → none in ACI either; use analysis (Annex ข.2 advisory).
15. Special-MRF flat slabs: not possible under 5.2.8. No SDC-D flat-slab SFRS except via an intermediate MRF ≤ 40 m (+40 % forces, 2.3.1.2).

---

## SUMMARY TABLE: slab detailing requirement × frame category

"Ordinary / gravity-only" = ordinary MRF (SDC B) or slabs not in the SFRS. "Intermediate" = flat slab as part of an intermediate MRF. "Special" = slabs in buildings whose SFRS is a special MRF or special walls (the slab itself is non-SFRS or a diaphragm).

| Requirement | Ordinary / gravity-only | Intermediate (flat slab in MRF) | Special system |
|---|---|---|---|
| Flat-slab frame as SFRS permitted? | Ordinary MRF in SDC B only (Table 2.3-1). No separate flat-slab row. | SDC B, C; SDC D only ≤ 40 m with +40 % forces (2.3.1.2, 5.2.2) | Not possible (5.2.8.1 beam geometry) [inference] |
| Column-strip / effective-width bar placement | EIT/ACI | M_s all in column strip; γ_f M_s within c + 1.5t each side; ≥ ½ column-strip support steel within effective width (5.2.12 (1)–(3), Fig. 5.2-14(ก)) | n/a (slab non-SFRS → ACI 18.14) |
| Continuous top bars | EIT/ACI (no seismic rule) | ≥ ¼ column-strip top continuous full span; ≥ 2 top bars through column line each way (5.2.12 (4)) | ACI |
| Continuous bottom, column strip | EIT integrity 13.3.8.5 | ≥ ⅓ column-strip top at support (5.2.12 (5)) | ACI |
| Bottom at mid-span | EIT/ACI | ≥ ½ continuous, develop f_y at support face (5.2.12 (6), Fig. 5.2-14(ค)) | ACI |
| Discontinuous edge anchorage | EIT/ACI | top and bottom develop f_y at support face; 90° hooks shown (5.2.12 (7), Fig. 5.2-14(ข)(ค)) | ACI |
| Gravity punching ratio | EIT shear strength only | V_u/φV_c ≤ 0.4 (1.2D + 1.0L, L factor 0.5 if LL < 4.9 kPa except car parks/assembly; φ = 0.75); waived if seismic eccentric-shear stress ≤ ½ φv_n (5.2.12.1.2–.3) | — |
| Punching with moment transfer | EIT (5.2.12.1.1 in general) | EIT strength incl. unbalanced moment (5.2.12.1.1) | — |
| Punching–drift (non-SFRS slab-column) | **SDC D:** V_s ≥ 0.3√f'c b0 d extending ≥ 4t, unless punching OK under design drift or drift ≤ max(0.005h, 0.035 − 0.05 V_u/φV_c) (5.2.12.1.4, 2.11.5 → ACI 18.14.5). SDC B/C: not required [DPT scope ambiguous: 5.2.12.1.4 does not name an SDC] | same | same (gravity flat slabs in special-MRF or special-wall buildings) |
| Integrity bottom bars through column (progressive collapse) | Clause is under 5.2.12 (SFRS flat slabs). For gravity slabs use EIT 13.3.8.5 [scope ambiguous] | A_sm = 0.5 w_u L1 L2/(0.9 f_y), w_u ≥ 2 D_service; edge ≥ ⅔, corner ≥ ½; 5.2.12 (5) bars count (5.2.12.2) | ACI |
| One-way (capacity) shear of slab | EIT/ACI | ≥ shear at M_n both ends + gravity, or 2E combos (5.2.7.2) | — |
| Column–slab joint hoops | EIT/ACI | A_v ≥ c1 s/(3 f_y) over deepest member depth; exempt if not main SFRS and restrained 4 sides (5.2.7.4.4) | 5.2.10 (special joints, column file) |
| Slab steel in beam flange (SCWB) | — | — | include slab bars within effective width in ΣM_nb; ΣM_nc ≥ 1.2 ΣM_nb (5.2.9.2.2); width → EIT/ACI |
| Beam crossties next to slab | — | — | 90° crosstie hooks on slab side if slab on one side only (5.2.8.3.6) |
| Stiffness for analysis | I_eff = 0.25 I_g flat slab (2.8.3) | same | same |
| Diaphragm force | F_px Eq. 2.9-1, 0.2 ≤ F_px/(S_DS I w_px) ≤ 0.4, plus transfer forces (2.9.1.1). Applies to all SDC. | same | same |
| Diaphragm openings / re-entrant corners | transferred force ≤ diaphragm shear and tension strength (2.9.1); openings > 50 % area = irregularity 3 (2.4.2.1). No trim-bar rule → ACI | same | same |
| Collectors | design only (2.9.2 for SDC C, D: Ω0 forces) | same | same; SDC D irregular: connections ×1.25 (2.4.3(4)) |
| Chords / wall anchorage ties | SDC C, D: continuous edge/chord reinforcement; sub-diaphragm ≤ 2.5:1; anchor F_p Eq. 2.10-1; steel anchorage parts ×1.4 (2.10.2–2.10.3) | same | same |
| Diaphragm connection of attached members | ≥ 5 % of D + L reaction in-plane (2.2.3) | same | same |
| Rigid diaphragm criterion | cast-in-place slab / concrete-filled deck with S/D_e ≤ 3, regular plan (2.4.1.2) | same | same |
| Topping over precast | not covered (5.2 intro) → ACI 18.12 | same | same |
| Coupling slabs | not covered (Annex ข.2 advisory only) | same | same |

### Not in DPT → ACI / EIT
- Column-strip and middle-strip definitions, moment distribution, γ_f/γ_v → EIT Ch. 13 / ACI 8.
- Slab thickness, minimum and shrinkage steel, spacing, cover, bar extensions (Fig. 13.3.8) → EIT 7.7, 7.12, 9.5.3, 13.3.
- Punching shear reinforcement layout (stirrups/studs, spacing, extent), shearheads, drop panels, shear caps → EIT 11.11 / ACI 22.6, 8.7.
- Slab openings and trim bars → EIT 13.4 / ACI 8.5.4, 18.12.
- Diaphragm thickness, minimum steel, V_n, chord/collector bar detailing, splices, confinement → ACI 318-14 §18.12.
- Precast diaphragms and topping slabs → ACI 318-14 §18.12.4–.5 (DPT Ch. 5 excludes precast).
- Non-SFRS frame members in SDC D (beyond 5.2.12.1.4) → ACI 318-14 §18.14 (required by DPT 2.11.5).
- Effective slab width for SCWB → EIT 8.11 / ACI 6.3.2.
- Integrity steel for gravity flat slabs → EIT 13.3.8.5.
- Slab steps, cantilevers, edge details, PT tendon detailing → EIT/ACI (and office handbooks).

### Uncertain readings / flags
1. 5.2.12.1.4 metric coefficient **0.93** vs the exact conversion ≈ 0.96 of the SI 0.3.
2. 5.2-24 uses **f_pe**; ACI uses f_pc. Probably notation.
3. 5.2.12.2: **L1, L2 undefined** (presumably spans).
4. Eq. 2.10-1 number printed twice (the k_a equation should be 2.10-2).
5. 5.2.12 item (4): "through the column line" vs ACI "through the column core". DPT wording is looser.
6. Fig. 5.2-14 leader text ends "…ถึงจุด" with the next word missing. Meaning taken from item (7): develop yield at the support face.
7. Scope of 5.2.12.1.4 and 5.2.12.2 by SDC is not stated. 5.2.12.1.4 is logically tied to SDC D through 2.11.5 and 5.2.2(ค).
8. 5.2.12.1.3's "½ φv_n" exemption has no exact ACI counterpart.
9. The table's classification of flat slabs under IMF, and "no special flat slab", are inferences.

---

# Part B. EIT 011008-21 (design) - slab clauses


**Source:** วสท. 011008-21 (ACI 318-11 basis, SI: MPa, mm).
- PDF: `G:\My Drive\##Textbook\EIT\10104-64.pdf`.
- Page numbers are **PDF pages** (book page = PDF page − 12).
- Values were read from the decoded text and checked on page images where the text was garbled: p.76 (Table 9.3, Eq. 9-11/9-12) and p.123 (Fig. 13.3.8).

**Related documents (not repeated here):**
- **DIGEST** = `SPEC_RC_DESIGN_EIT-011008-21.md`. It covers ch. 7 and ch. 12 in full.
- **BEAM** = `SOURCES_BEAM_DETAILING.md` Part B. It covers ch. 8, 10 and 11 for beams.

This file adds the slab view, plus **ch. 9 (slab thickness), 11.11 (punching) and ch. 13 (two-way slabs)**, which neither document covers.

**Clause numbering vs ACI 318-11:**
- Same as ACI: ch. 7, 9, 10 and 13; **11.10 (moment transfer to columns) and 11.11 (slabs and footings)**.
- Shifted:
  - ch. 8 from 8.7: EIT 8.8 span length = ACI 8.9; EIT 8.11 T-beams = ACI 8.12; EIT 8.12 joists = ACI 8.13.
  - ch. 11.4 (see BEAM).
  - ch. 12 from 12.9: EIT 12.10 positive-moment bars = ACI 12.11; EIT 12.12 web reinforcement = ACI 12.13; EIT 12.13 splices general = ACI 12.14; EIT 12.14 tension splices = ACI 12.15.
- Equation numbers are shifted by −1 in ch. 9 (EIT 9-11/9-12 = ACI 9-12/9-13) and by −1 in 11.11 (EIT 11-30…11-32 = ACI 11-31…11-33).

**Figures:** the whole standard (ch. 7–13, PDF pp.55–131) has **one** detailing figure, **Fig. 13.3.8** (p.123). There are no figures for:
- punching-shear reinforcement layouts;
- corner reinforcement;
- openings.

The office sheet must draw these from the text.

---

## CHAPTER 7 — Details of reinforcement (slab view)

### 7.5 Placing (p.56) — DIGEST lines 567–582
- **7.5.2 Tolerances:**
  - d ≤ 200 mm (almost every slab): d ± 10 mm (printed "± 100", a DIGEST flag); cover −10 mm.
  - Cover tolerance ≤ 1/3 of the specified cover.
  - Bar ends and bends ± 50 mm; ± 25 mm at discontinuous ends.
- **7.5.3:** Welded wire reinforcement (wire ≤ 6 mm) in slabs with span ≤ 3 m may be draped from near the top over the support to near the bottom at midspan. It must be continuous over, or anchored at, the support.

### 7.6.5 Spacing of primary flexural bars in slabs and walls (p.57)
- Spacing ≤ **3h** and ≤ **450 mm**. This does not apply to joist slabs, where 7.12 governs the topping.
- Same as ACI 318-11 7.6.5.
- Minimum clear spacing (7.6.1) ≥ db and ≥ 25 mm.
- Max. aggregate ≤ 1/3 slab depth (3.3.3, DIGEST).

### 7.7 Cover for slabs (pp.57–58) — DIGEST lines 598–650

| Case | Bar size | Min. cover (mm) | Clause |
|---|---|---|---|
| Cast against earth (slab on grade underside, footing) | all | **75** | 7.7.1(ก) |
| Exposed to earth or weather (roof top, exposed soffit, balcony) | ≥ 20 mm | **50** | 7.7.1(ข) |
| Exposed to earth or weather | ≤ 16 mm and WWR | **40** | 7.7.1(ข) |
| Not exposed: slabs, walls, joists | ≥ 20 mm | **30** | 7.7.1(ค)(2) |
| Not exposed: slabs, walls, joists | ≤ 16 mm and WWR | **20** | 7.7.1(ค)(2) |
| Precast (plant), not exposed: slabs | ≥ 20 / ≤ 16 mm | 25 / 15 | 7.7.2(ข)(2) |

- Increase cover for fire (7.7.5) and corrosive exposure (7.7.4).
- [NOTE] EIT ≥ 20 mm slab bars = 30 mm is stricter than ACI (ACI 20 mm up to No.11).
- [FLAG] ACI 318-11 7.7.5 (cover to heads and base rails of **headed shear studs** ≥ the cover of the flexural bars) is **not in EIT**. Adopt the ACI rule on stud-rail details.

### 7.12 Shrinkage and temperature (S&T) reinforcement (p.62) — DIGEST lines 724–740
- **7.12.1:** In one-way structural slabs, provide S&T steel **perpendicular** to the main bars.
  - Where S&T movement is significantly restrained, consider 8.2.4 and 9.2.6.
- **7.12.2(ก):** Minimum As/**Ag (gross, b × h)**, and never < **0.0014**:

| Steel | Ratio |
|---|---|
| SR24 | **0.0025** |
| SD30 | **0.0020** |
| SD40, or WWR | **0.0018** |
| fy > 400 MPa (at ε = 0.35 %) | 0.0018 × 400/fy |

- **7.12.2(ข):** Spacing ≤ **5h** and ≤ **400 mm**.
  - [FLAG, deliberate] ACI 318-11 uses 450 mm.
- **7.12.2(ค):** Develop S&T bars for fy wherever they are required (ch. 12).
- The same minimum is used as:
  - As,min for **main** bars in slabs of uniform thickness (10.5.4);
  - the two-way slab minimum (13.3.1);
  - joist-slab topping steel (8.12.5(ค), 8.12.6(ข)).

(calc.) Minimum As per metre width (mm²/m) and the resulting bar spacing, with the spacing limit min(5h, 400) = 400 mm for h ≥ 80:

| h (mm) | SR24 0.0025 | SD30 0.0020 | SD40 0.0018 | RB9 @ (SR24) | DB10 @ (SD40) | DB12 @ (SD40) |
|---|---|---|---|---|---|---|
| 100 | 250 | 200 | 180 | 250 | 400 (436) | 400 |
| 120 | 300 | 240 | 216 | 200 (212) | 350 (363) | 400 |
| 150 | 375 | 300 | 270 | 150 (170) | 275 (291) | 400 (419) |
| 180 | 450 | 360 | 324 | 125 (141) | 225 (242) | 325 (349) |
| 200 | 500 | 400 | 360 | 125 (127) | 200 (218) | 300 (314) |
| 250 | 625 | 500 | 450 | 100 (102) | 150 (174) | 250 (251) |

- Bracketed values are the exact maximum spacing. Bar areas used: RB9 = 63.6, DB10 = 78.5, DB12 = 113.1 mm².
- For main bars in two-way slabs, the 2h limit (13.3.2) governs instead of 400 mm.

### 7.13 Structural integrity (p.63) — DIGEST lines 742–756, BEAM lines 409–435
- **7.13.2(ฉ):** For two-way slab construction, see **13.3.8(จ)** (below).
- **7.13.2(ก):** Joist slabs need at least one bottom bar continuous, or spliced with a Class B lap or a mechanical/welded splice per 12.14.4. At non-continuous supports the bar ends in a standard hook.
- [NOTE] There is **no integrity rule for one-way solid slabs** or for two-way slabs **with beams**.
  - For one-way slabs, 12.10.1 still requires ≥ 1/4 of positive bars (continuous spans), or ≥ 1/3 (simple spans), to extend into the support.
  - The 150 mm embedment in 12.10.1 is stated **for beams only**.

---

## CHAPTER 8 — Analysis (slab items; brief, see BEAM lines 437–507)

- **8.3.3 Approximate coefficients (p.66):** apply to one-way slabs under the same conditions as beams:
  - ≥ 2 spans;
  - adjacent spans differ by ≤ 20 %;
  - uniform load;
  - L ≤ 3D;
  - prismatic.
  - Coefficients (full table in BEAM):
    - positive: wuℓn²/11 (end span, discontinuous end unrestrained), /14 (end span, integral), /16 (interior);
    - negative: /9 (2 spans), /10 (> 2 spans) at the first interior support, /11 at other interior supports;
    - **slabs with spans ≤ 3.0 m: wuℓn²/12 at all supports**;
    - interior face of exterior support: /24 on a spandrel beam, /16 on a column.
  - Shear: 1.15wuℓn/2 at the first interior support, wuℓn/2 elsewhere.
  - No cut-off points are given. Cut-offs follow 12.9–12.11 (see Fig. 13.3.8 for flat slabs only).
- **8.8 Span length (= ACI 8.9) (p.68):**
  - **8.8.1:** Members not built integrally with supports: span = clear span + h, but ≤ c/c of supports.
  - **8.8.2:** Continuous frames: c/c.
  - **8.8.3:** Moments may be taken at the support face.
  - **8.8.4:** **Solid or ribbed slabs with clear span ≤ 3.00 m**, built integrally with supports, may be analysed as continuous on knife-edge supports. Span = clear span, and beam widths are ignored.
- **8.11 Effective flange (slab acting with beams, = ACI 8.12) (pp.69–70):**
  - Interior beam: width ≤ span/4; overhang ≤ 8hf and ≤ ½ clear distance to the next web.
  - Edge beam: overhang ≤ span/12, 6hf, ½ clear distance.
  - Isolated T-beam: hf ≥ bw/2; width ≤ 4bw.
  - **8.11.5:** Where the slab's main bars run **parallel** to the beam, place **transverse top bars** in the flange.
    - Design them as a cantilever: the full overhang for isolated beams, the effective overhang otherwise.
    - Spacing ≤ **5h** and ≤ **400 mm** (ACI 450).
  - This is a standard "top bars across the beam" note on one-way slab-beam sections.
- **8.12 Joists (= ACI 8.13) (p.70):**
  - Rib ≥ 100 mm wide; depth ≤ 3.5 × minimum rib width; clear rib spacing ≤ **750 mm**.
  - Topping ≥ ℓclear/12 and ≥ 40 mm (permanent fillers with strength ≥ f'c), or ≥ 50 mm (removable forms).
  - Topping steel perpendicular to the ribs ≥ 7.12.
  - Conduits need ≥ 25 mm cover (8.12.7).
  - Vc + 10 % (8.12.8).
  - Joists and slabs are exempt from Av,min (11.4.5(ก)(1),(3), p.94).
- **8.13 Floor finish (p.70):**
  - A finish not placed monolithically is not structural (unless designed per ch. 17).
  - All concrete floor finish **may count as cover** or as non-structural thickness.

---

## CHAPTER 9 — Minimum thickness (deflection control)

### 9.4 (p.73)
Design fy, fyt ≤ **560 MPa** (ACI 550; BEAM flag 12).

### 9.5.2 One-way members — Table 9.1 (p.73)
**9.5.2(ก):** Table 9.1 applies to one-way members that do **not** support, and are not attached to, partitions or other construction likely to be damaged by large deflection. A lesser thickness is allowed only if computed deflections show no adverse effect.

**Table 9.1** — minimum h when deflection is not computed:

| Member | Simply supported | One end continuous | Both ends continuous | Cantilever |
|---|---|---|---|---|
| **Solid one-way slab** | **ℓ/20** | **ℓ/24** | **ℓ/28** | **ℓ/10** |
| Beam or one-way ribbed (joist) slab | ℓ/16 | ℓ/18.5 | ℓ/21 | ℓ/8 |

- The values are for normalweight concrete and **SD40**.
- Modifiers:
  - (1) Lightweight concrete, wc 1,500–2,000 kg/m³: × (1.65 − 0.0003wc) ≥ 1.09.
  - (2) fy ≠ 400 MPa: × **(0.4 + fy/700)**.
    - (calc.) SD30: × 0.829. SR24: × 0.743. For example, a both-ends-continuous SD30 slab needs ℓ/33.8.
- Identical to ACI 318-11 Table 9.5(a).
- **9.5.2(ข)–(ฉ) (pp.73–74):**
  - Ie per Eq. 9-7, with Mcr per 9-8 and fr = 0.62λ√f'c (9-9).
  - Long-term multiplier λΔ = ξ/(1 + 50ρ′) (9-10), with ξ = 2.0 (≥ 5 yr), 1.4 (1 yr), 1.2 (6 mo), 1.0 (3 mo).
  - Limits in **Table 9.2 (p.75):**
    - flat roofs: ℓ/180 (immediate L);
    - floors: ℓ/360 (immediate L);
    - supporting or attached to non-structural elements likely to be damaged: ℓ/480 (part after attachment);
    - not likely to be damaged: ℓ/240.

### 9.5.3 Two-way members (pp.75–77)
**(ก) Scope (p.75):**
- Two-way slabs designed to ch. 13 with **long/short panel ratio ≤ 2** (13.6.1(ข)).
- Slabs **without interior beams** (spanning between supports on all sides): satisfy (ข) or (ง).
- Slabs **with beams** between supports on all sides: satisfy (ค) or (ง).

**(ข) Slabs without interior beams, ℓlong/ℓshort ≤ 2 (p.75):**
- Use Table 9.3, and not less than:
  - (1) without drop panels (as defined in 13.2.5): **125 mm**;
  - (2) with drop panels (13.2.5): **100 mm**.

**Table 9.3** (p.76) — minimum h, ℓn = clear span in the **long** direction, face to face of supports:

| fy (MPa) | No drop panel: exterior panel, no edge beam | No drop panel: exterior panel, with edge beam# | No drop panel: interior panel | With drop panel: exterior, no edge beam | With drop panel: exterior, with edge beam# | With drop panel: interior |
|---|---|---|---|---|---|---|
| 300 | ℓn/33 | ℓn/36 | ℓn/36 | ℓn/36 | ℓn/40 | ℓn/40 |
| 400 | **ℓn/30** | **ℓn/33** | **ℓn/33** | **ℓn/33** | **ℓn/36** | **ℓn/36** |
| 500 | ℓn/28 | ℓn/31 | ℓn/31 | ℓn/31 | ℓn/34 | ℓn/34 |

- Table notes:
  - \* Interpolate linearly for fy between the tabulated values.
  - "Drop panel" as defined in 13.2.5.
  - \# Edge beams between columns along exterior edges need **αf ≥ 0.8**.
- [FLAG] ACI 318-11 Table 9.5(c) gives the same ratios at fy = **280 / 420 / 520 MPa**. EIT moves them to 300 / 400 / 500:
  - slightly unconservative for SD30 (300 vs 280);
  - conservative for SD40 (400 vs 420).
  - Deliberate adaptation; adopt as printed.
- The table title is misprinted "ตามรางที่" (for ตารางที่), which is trivial.
- (calc.) Flat plate, SD40, ℓn = 6.0 m: exterior panel without edge beam 200 mm; interior 182 mm. With drop panels: 182 / 167 mm.

**(ค) Slabs with beams on all sides (p.76):**
- (1) **αfm ≤ 0.2:** use (ข) (as if without beams).
- (2) **0.2 < αfm ≤ 2.0:**
  **h ≥ ℓn(0.8 + fy/1,400) / [36 + 5β(αfm − 0.2)]**  (9-11), and **≥ 125 mm**.
- (3) **αfm > 2.0:**
  **h ≥ ℓn(0.8 + fy/1,400) / (36 + 9β)**  (9-12), and **≥ 90 mm**.
- (4) At **discontinuous edges**, provide an edge beam with **αf ≥ 0.8**, or increase the minimum h from (9-11)/(9-12) by **≥ 10 %** in that panel.
- Definitions:
  - ℓn = clear span in the **long** direction, face to face of beams;
  - β = long/short clear-span ratio;
  - αf = EcbIb/(EcsIs) (13-3);
  - αfm = average αf of the beams on the panel edges.
- [FLAG — misprint] The definitions line says ℓn and β apply "in (2) and (4)". It should read **(2) and (3)** (ACI 318-11 9.5.3.3: "in (b) and (c)").
- (calc.) SD40: 0.8 + 400/1,400 = 1.086. Example, ℓn = 6.0 m, β = 1.0, αfm > 2: h = 6,000 × 1.086 / 45 = 145 mm.

**(ง) (p.77):** Thinner slabs are allowed if computed deflections satisfy Table 9.2. The calculation considers:
- panel size and shape;
- support conditions and edge restraint;
- Ec per 8.5.1 and Ie per Eq. 9-7;
- long-term deflection per 9.5.2(จ).

**13.1.4 (p.121):** Minimum thickness of ch. 13 slabs is per 9.5.3.

---

## CHAPTER 10 — Flexure (slab items)

- **10.5.4 (p.81):** For **slabs and footings of uniform thickness**:
  - As,min in the direction of the span = S&T minimum of **7.12.2(ก)** (on b × h, not 10.5.1);
  - **maximum spacing ≤ 3h and ≤ 450 mm**.
  - Same as ACI 318-11 10.5.4. See BEAM lines 537–545.
- **10.6 Crack control (pp.81–82):**
  - Applies to beams and **one-way slabs**. Eq. 10-4: s ≤ 380(280/fs) − 2.5cc ≤ 300(280/fs), with fs = (2/3)fy allowed.
  - (calc.) SD40, cc = 20 mm: s ≤ 399 − 50 = **349 mm** (≤ 315 → **315 mm**). For cc = 30: 315 mm. For SD30 (fs = 200): s ≤ 532 − 50 = 482 → cap 420. The 3h / 450 limits (7.6.5) may then govern.
  - **10.6.2:** For **two-way slabs**, distribution is per **13.3**.
- **10.6.6 T-beam flange in tension (p.82):**
  - Distribute the tension steel over the effective flange width or span/10, whichever is smaller.
  - Add some longitudinal bars in the outer flange if the flange is wider.

---

## CHAPTER 11 — Shear in slabs (11.10–11.11, pp.104–108)

### 11.4.5(ก)(1) (p.94)
**Slabs and footings are exempt from Av,min.**
- Exemptions also cover hollow-core slabs with h ≤ 320 mm, or Vu ≤ 0.5φVcw (item (2)).

### 11.10 Transfer of moments to columns (p.104) — brief
- **11.10.1:** Shear from moment transfer at slab/beam–column joints must be considered in the column transverse reinforcement.
- **11.10.2:** Provide column ties through the joint, over the depth of the deepest framing member, ≥ Eq. (11-9), per 7.9.
  - Exception: joints not part of the primary seismic system that are restrained on all four sides by beams **or slabs** of about equal depth.
  - For flat-plate edge and corner columns, this means column ties continue through the slab depth.

### 11.11.1 Critical sections (p.104)
Shear near columns, concentrated loads or reactions is governed by the more severe of two conditions.
- **(ก) Beam (one-way) action:** critical section across the full width, designed per 11.1–11.4 (at d from the face, 11.1.3).
- **(ข) Two-way action:** critical section of perimeter **bo**, located so bo is a minimum, but **not closer than d/2** to:
  - (1) edges or corners of the column, concentrated load or reaction area;
  - (2) changes in slab thickness: edges of capitals, **drop panels** or **shear caps**.
  - Design per 11.11.2–11.11.6.
- **(ค)** For square or rectangular columns, loads or reaction areas, the critical section may have **four straight sides**.
- (detailing) With a drop panel, check two sections:
  - d/2 from the column face, using the drop-panel d;
  - d/2 outside the drop-panel edge, using the slab d.

### 11.11.2 Vc for two-way action, nonprestressed (pp.104–105)
Vn = Vc + Vs (11-1, 11-2). Vc is the **least** of:
- **Vc = 0.17(1 + 2/βc)λ√f'c bo d**  (11-30)
  - βc = long/short side of the column, load or reaction area.
- **Vc = 0.083(αs d/bo + 2)λ√f'c bo d**  (11-31)
  - αs = **40** interior, **30** edge, **20** corner column.
- **Vc = 0.33λ√f'c bo d**  (11-32)

Notes:
- Shearheads → 11.11.4. Moment transfer → 11.11.7.
- Identical to ACI 318-11 Eq. 11-31 to 11-33. EIT has no prestressed two-way clause (ACI 11.11.2.2).

### 11.11.3 Bar/wire and stirrup shear reinforcement (p.105)
Single- or multi-leg stirrups, bars or wires are permitted in slabs and footings only if **d ≥ 150 mm** and **d ≥ 16 × (shear-bar diameter)**.
- (calc.) DB10 stirrups need d ≥ 160 mm; RB9 needs d ≥ 150 mm; DB12 needs d ≥ 192 mm.
- **(ก) Strength:**
  - Vn per (11-2) with **Vc ≤ 0.17λ√f'c bo d**.
  - Vs per 11.4 (Eq. 11-10). **Av = all legs on one peripheral line** geometrically similar to the column perimeter.
- **(ข) Upper limit:** **Vn ≤ 0.5√f'c bo d**.
- **(ค) Layout:**
  - Column face to the **first line of stirrup legs ≤ d/2**.
  - Spacing between adjacent legs **in the first line ≤ 2d**, measured parallel to the column face.
  - Spacing of **successive lines ≤ d/2**, measured perpendicular to the column face.
- **(ง) Anchorage:**
  - Stirrups are anchored per **12.12** (EIT numbering; = ACI 12.13, see DIGEST 12.12). Stirrup hooks engage longitudinal bars (7.1.3, 12.12).
  - They must **engage the longitudinal flexural bars** in the direction considered.
- Extent: continue the lines until the shear stress at the section **d/2 outside the outermost line** ≤ φ0.17λ√f'c. This limit is stated in 11.11.7(ข)(2), and the same limit is written in 11.11.5(ง) for studs.

### 11.11.4 Shearheads (structural-steel I or channel sections) (pp.105–106)
For gravity shear at **interior** columns: items (ก)–(ฌ). With moment transfer, see 11.11.7(ค).
- **(ก) Arms:** identical arms at right angles, joined by full-penetration welds; arms continuous through the column section.
- **(ข) Depth:** ≤ **70 tw** (web thickness).
- **(ค) Arm ends:** may be cut at **≥ 30°** to horizontal, if the plastic moment capacity of the tapered part is adequate.
- **(ง) Compression flanges:** all within **0.3d** of the slab compression face.
- **(จ) Stiffness:** αv (arm stiffness / cracked composite slab section of width c2 + d) ≥ **0.15**.
- **(ฉ) Required plastic moment per arm:**
  **Mp = (Vu / (2φn))[hv + αv(ℓv − c1/2)]**  (11-33)
  - n = number of arms;
  - ℓv = minimum arm length needed for (ช) and (ซ).
- **(ช) Critical section:** perpendicular to the slab plane, crossing each arm at **¾(ℓv − c1/2)** from the column face.
  - At the minimum-bo location, but not closer than the d/2 perimeter of 11.11.1(ข)(1).
- **(ซ) Limits:**
  - Vn ≤ **0.33√f'c bo d** on the (ช) section;
  - with a shearhead, Vn ≤ **0.58√f'c bo d** on the d/2 section of 11.11.1(ข)(1).
- **(ฌ) Moment resisted by the shearhead in each column strip:**
  **Mv = (φαvVu / (2n))(ℓv − c1/2)**  (11-34)
  - Mv is not more than the least of: 30 % of the column-strip factored moment; the change in column-strip moment over ℓv; Mp from (11-33).
- **(ญ)** With unbalanced moment, the shearhead must be anchored to transfer Mp to the column.
- [NOTE] EIT does **not** carry ACI 318-11 13.3.8.6, which says that where bottom integrity bars cannot pass through the column (shearheads, lift slabs), ≥ 2 bonded bottom bars each way pass through the shearhead as close to the column as practicable, continuous or Class B spliced, anchored at the shearhead at exterior columns. Adopt it on shearhead details.

### 11.11.5 Headed shear stud reinforcement (pp.106–107)
Studs perpendicular to the slab plane are permitted. Overall stud-assembly height:
- **Top tension steel (slabs):** ≥ h − [cover above the top flexural bars + cover below the base rail + ½ flexural-bar diameter].
- **Bottom tension steel (footings):** ≥ h − [cover below the bottom bars + cover above the stud heads + ½ bottom-bar diameter].

Requirements:
- **(ก) Strength:**
  - Vn per (11-2) with **Vc ≤ 0.25λ√f'c bo d** and **Vn ≤ 0.66√f'c bo d** (d/2 section).
  - Vs per (11-10), with Av = all studs on one peripheral line approximately parallel to the column perimeter, and s = spacing of peripheral lines.
  - **Av fyt/(bo s) ≥ 0.17√f'c**.
- **(ข) Spacing of lines:**
  - Column face to first peripheral line **≤ d/2**.
  - Spacing of peripheral lines, measured perpendicular to any column face, **constant**:
    - **≤ 0.75d** if the maximum factored shear stress ≤ φ0.5√f'c (at the d/2 section, from Vu and unbalanced moment);
    - **≤ 0.5d** if > φ0.5√f'c.
    - Prestressed per 11.11.2(ข): ≤ 0.75d. [FLAG] This is a stale ACI cross-reference; EIT 11.11.2(ข) is the αs equation. It does not matter for RC.
- **(ค) Tangential spacing:** between adjacent studs along the **first** peripheral line ≤ **2d**.
- **(ง) Outer check:** the shear stress from factored shear and moment ≤ **φ0.17λ√f'c** at the section **d/2 outside the outermost peripheral line**.

### 11.11.6 Openings in slabs (p.107)
**Trigger:**
- an opening is **closer than 10h (10 × slab thickness)** to a concentrated load or reaction area (column); **or**
- an opening in a **flat slab** lies **within a column strip** (ch. 13).

In either case, modify the critical sections of 11.11.1(ข) and 11.11.4(ช):
- **(ก) Without shearheads:** the part of the perimeter enclosed by straight lines **projected from the column (load/reaction) centroid, tangent to the opening boundaries**, is ineffective.
- **(ข) With shearheads:** the ineffective part is **half** of that in (ก).
- Same as ACI 318-11 11.11.6. Pair with 13.4 (bar replacement) on the sheet.

### 11.11.7 Moment transfer at slab–column connections (pp.107–108) — detailing-relevant parts
- **(ก)** Unbalanced moment Mu is split:
  - γfMu goes by **flexure** (13.5.3);
  - **γv = 1 − γf** (11-35) goes by eccentric shear about the centroid of the d/2 critical section.
- **(ข)** Shear stress varies linearly about that centroid. vu ≤ φvn, where:
  - (1) without shear reinforcement, vn = Vc/(bo d) (11-36);
  - (2) with bars/stirrups or studs, vn = (Vc + Vs)/(bo d) (11-37).
    - Vc, Vs per 11.11.3(ก).
    - The design considers the variation of shear stress around the column.
    - Stress ≤ φ0.17λ√f'c at d/2 beyond the outermost line of stirrup legs.
- **(ค) With shearheads:** stresses (shearhead section of 11.11.4(ช) + moment-transfer eccentric shear about the 11.11.1(ข)(1)/(ค) section) ≤ **φ0.33λ√f'c**.

---

## CHAPTER 12 — Development (slab view; DIGEST lines 769–961)

- **12.10.1 (= ACI 12.11.1) (p.115):** ≥ **1/3** (simple spans) or ≥ **1/4** (continuous) of positive-moment steel extends along the same face into the support. The **150 mm** minimum is stated for beams.
  - Fig. 13.3.8 cites 12.10.1 for bars entering supports.
- **12.11.3 (= ACI 12.12.3) (p.115):** ≥ 1/3 of the negative steel at a support extends past the point of inflection by ≥ max(d, 12db, ℓn/16).
  - This governs top-bar cut-offs for one-way slabs designed by 8.3.3 (office cut-offs such as ℓn/4, ℓn/3 must satisfy it).
- **Mechanical/welded splices** where continuity is required: EIT **12.14.4** (it points to 12.13.3(ข)/(ง)).
- **Welded wire reinforcement (pp.119–120):**
  - Deformed WWR laps (12.17): ≥ 1.3ℓd and ≥ 200 mm; overlap between outermost cross wires ≥ 50 mm.
  - Plain WWR laps (12.18): ≥ one cross-wire spacing + 50 mm, ≥ 1.5ℓd and ≥ 150 mm (As < 2 × required); or ≥ 1.5ℓd and ≥ 150 mm (As ≥ 2 × required).

---

## CHAPTER 13 — Two-way slab systems (pp.121–131)

### 13.1 Scope (p.121)
- **13.1.1:** Slabs reinforced for flexure in more than one direction, with or without beams between supports.
- **13.1.2:** Supports are columns or walls. For columns, c1, c2 and ℓn are based on the **effective support area**. This is the intersection of the slab soffit (or drop-panel soffit) with the largest right circular cone, right pyramid or tapered wedge that:
  - lies within the column and capital or bracket; and
  - makes **≤ 45°** with the column axis.
- **13.1.3:** Solid slabs, and slabs with recesses or pockets (permanent or removable fillers between ribs in two directions, i.e. waffle slabs), are included.
- **13.1.4:** Minimum thickness per 9.5.3.

### 13.2 Definitions (p.121)
- **13.2.1 Column strip:**
  - Width on **each side** of the column centreline = **0.25ℓ2 or 0.25ℓ1, whichever is less**.
  - Beams in the strip are included.
  - (Total column-strip width = the lesser of ℓ1/2 and ℓ2/2.)
- **13.2.2 Middle strip:** the design strip bounded by two column strips.
- **13.2.3 Panel:** bounded on all four sides by column, beam or wall centrelines.
- **13.2.4 Beam (monolithic or fully composite):** includes the slab on each side, extending a distance equal to the beam projection **above or below** the slab (whichever is greater), but **≤ 4h** (h = slab thickness).
- **13.2.5 Drop panel:** used to reduce negative steel over the column or to reduce the required slab thickness.
  - **Projection below the slab ≥ ¼ of the adjacent slab thickness.**
  - **Extends from the support centreline, in each direction, ≥ 1/6 of the c/c span in that direction.**
  - (So the total drop width ≥ ℓ/3 when the adjacent spans are equal.)
- [FLAG — omission] ACI 318-11 **13.2.6 shear cap** is not defined in EIT. The ACI rule: a projection below the slab used to enlarge the critical shear section must extend horizontally from the column face ≥ its projection below the soffit.
  - EIT uses the term "หมวกรับแรงเฉือน" in 11.11.1(ข)(2) without defining it. Adopt the ACI definition for shear caps that do not meet 13.2.5.

### 13.3 Slab reinforcement (pp.121–123)
- **13.3.1:** As in each direction comes from the moments at critical sections, and is **≥ 7.12** (0.0025 / 0.0020 / 0.0018 × b × h).
- **13.3.2:** **Spacing at critical sections ≤ 2h.**
  - Exception: cellular or ribbed portions. The topping over cells or between ribs gets 7.12 steel.
  - (Stricter than one-way slabs, where the limit is 3h / 450 mm. There is no 450 mm cap here; 2h governs for h ≤ 225 mm.)
- **13.3.3:** **Positive (bottom) bars perpendicular to a discontinuous edge** extend **to the edge of the slab**. They are embedded, **straight or hooked, ≥ 150 mm** into spandrel beams, columns or walls.
- **13.3.4:** **Negative (top) bars perpendicular to a discontinuous edge** are **bent, hooked or otherwise anchored** in spandrel beams, columns or walls. They must be **developed at the face of support** per ch. 12. (Typical detail: a standard 90° hook down into the edge beam, ℓdh from the face.)
- **13.3.5:** Where there is **no spandrel beam or wall** at a discontinuous edge, or where the slab **cantilevers** beyond the support, bars may be **anchored within the slab**.
- **13.3.6 Corner reinforcement:** applies at **exterior corners** of slabs supported by edge walls or edge beams with **αf > 1.0**. Provide **top and bottom** special reinforcement:
  - **(ก) Amount:** top and bottom steel each resist a moment per unit width equal to the **maximum positive moment per unit width in the panel**.
  - **(ข) Moment axes:**
    - top steel: about an axis **perpendicular to the diagonal** from the corner;
    - bottom steel: about an axis **parallel to the diagonal**.
  - **(ค) Extent:** from the corner, in each direction, **1/5 of the longer span** of the panel.
  - **(ง) Placement:**
    - top bars **parallel to the diagonal** in a band;
    - bottom bars **perpendicular to the diagonal**;
    - **alternatively**, top and bottom bars each in **two layers parallel to the slab edges**.
  - Same as ACI 318-11 13.3.6.
  - (Detailing) With the parallel-to-edges option, the typical detail is an extra top and bottom mesh of ℓlong/5 × ℓlong/5 at each exterior corner. Each direction is sized for the max positive moment. The existing bottom bars may be counted toward the bottom mesh.
- **13.3.7 Drop panels in flat slabs:** dimensions per 13.2.5. In computing slab reinforcement, the drop projection below the slab is taken as **≤ ¼ of the distance from the drop-panel edge to the face of the column or capital**.
- **13.3.8 Details for slabs without beams (flat plates and flat slabs):**
  - **(ก)** In addition to 13.3, bar extensions shall be at least those in **Fig. 13.3.8**.
  - **(ข)** Where adjacent spans are unequal, the extension of negative bars beyond the support face is based on the **longer span**.
  - **(ค)** **Bent (cranked) bars** are permitted only where the depth/span ratio allows bends of **≤ 45°**.
  - **(ง)** Where the two-way slab is part of the primary lateral-load-resisting frame, bar lengths come from analysis but are **not less than Fig. 13.3.8**.
  - **(จ) Integrity:**
    - **All bottom bars or wires in the column strip, in each direction,** are **continuous**, or spliced with **Class B tension laps**, or mechanical/welded splices ("per 12.14.3", see flag).
    - Splices are located as shown in Fig. 13.3.8.
    - **At least two column-strip bottom bars or wires in each direction** pass **within the region bounded by the column longitudinal bars** (through the column core) and are **anchored at exterior supports**.
  - [FLAG — misprint] "12.14.3" is ACI numbering. In EIT, 12.14.3 is laps of different bar sizes. Read as **12.14.4** (mechanical/welded splice), as in 7.13.2.
  - [FLAG — omission] ACI 318-11 13.3.8.6 (bottom bars through shearheads or lifting collars) is missing; see 11.11.4 note.

#### Fig. 13.3.8 — Minimum extensions for reinforcement in slabs without beams (p.123)
The caption says to see 12.10.1 for bars extending into supports. The figure is a table:
- **Rows:** strip (column / middle) × location (top / bottom), with a column for the **minimum As at the section** (% of the strip steel).
- **Two drawing panels:** **without drop panels** (left) and **with drop panels** (right).
- **Bottom band:** the span geometry. It shows c1, the clear span **ℓn** face to face of supports, and the c/c span.
  - Supports, from left to right: an **exterior support (slab discontinuous)**, an **interior support (slab continuous)**, and a second **exterior support**.
  - All extensions are measured **from the face of support**.
  - ℓn is the clear span. For unequal spans at interior supports, use the longer ℓn (13.3.8(ข)).

**Column strip — TOP:**

| Bars | Without drop panels | With drop panels |
|---|---|---|
| **≥ 50 %** of the top steel (longer bars) | extend **0.30ℓn** beyond the face of support | extend **0.33ℓn** |
| **Remainder** (shorter bars) | extend **0.20ℓn** | extend **0.20ℓn** |

- At interior supports the bars run continuously across the column, reaching the stated distance into **each** adjacent span.
- At **exterior (discontinuous) supports**, both top-bar groups end in a **hook turned down** into the support (column or edge), per 13.3.4. They extend 0.30ℓn/0.20ℓn (0.33ℓn/0.20ℓn with drop) into the span.

**Column strip — BOTTOM (100 % of the steel in this row):**
- All bars are shown as **continuous bars** ("เหล็กเส้นต่อเนื่อง").
- At each exterior support the bars extend **150 mm** past the face of support into the support.
- **Splices are permitted in the region over the interior support.** The region is marked by dashed lines at the ends of the column-strip top bars on each side: 0.30ℓn (0.33ℓn with drop) from the interior support faces.
- A second bottom bar line is drawn **hooked (turned up) at both exterior supports**. It is labelled "at least two bars or wires, per 13.3.8(จ)". These are the integrity bars that pass through the column core and are anchored at exterior supports.

**Middle strip — TOP (100 % of the steel in this row):**
- All top bars extend **0.22ℓn** beyond the face of support, both sides of interior supports.
- At exterior supports the bars are **hooked down** and extend 0.22ℓn into the span.
- The value is the same with or without drop panels.

**Middle strip — BOTTOM:**
- **≥ 50 %** of the bottom steel runs **continuous** to the supports:
  - **150 mm** past the face at exterior supports;
  - at the interior support, the bars reach the support and extend **150 mm** into it (a break symbol at the interior centreline marks the bar ends from each side).
- The **remainder** extends **150 mm** into the exterior support and may be stopped short of the interior support, **no more than 0.15ℓn** from the interior support face ("สูงสุด 0.15ℓn", maximum 0.15ℓn).

The content is identical to ACI 318-11 Fig. 13.3.8.

(calc.) Example, ℓn = 6.0 m, no drop panels:
- column-strip top bars 1.80 m / 1.20 m from the face;
- middle-strip top bars 1.32 m;
- middle-strip bottom remainder may stop up to 0.90 m from the interior face;
- bottom bars 150 mm into supports.

### 13.4 Openings in slab systems (p.123)
- **13.4.1:** Openings of **any size** are allowed if analysis shows that strength (9.2, 9.3) and serviceability, including deflection limits, are satisfied.
- **13.4.2:** Instead of analysis, openings in **slabs without beams** are permitted only as follows:
  - **(ก) Middle strip ∩ middle strip:** openings of **any size**. The **total** reinforcement required for the panel without the opening is maintained.
  - **(ข) Column strip ∩ column strip:** openings **≤ 1/8 of the column-strip width** in either span. The interrupted reinforcement is **added on the sides of the opening**, in each direction.
  - **(ค) Column strip ∩ middle strip:** **≤ 1/4 of the reinforcement in either strip** may be interrupted. The interrupted amount is **added on the sides of the opening**, in each direction.
  - **(ง)** Shear per **11.11.6**: perimeter reduction if the opening is within 10h of the column or anywhere in a flat-slab column strip.
- [NOTE] EIT gives no rule for openings in two-way slabs **with beams**, or in one-way slabs. The common office practice is to replace interrupted bars at the sides and add diagonal corner bars. This is office practice, not an EIT rule.

### 13.5 Design procedures (pp.124–125) — brief, detailing-relevant parts
- **13.5.1:** Any method satisfying equilibrium and compatibility may be used. Direct Design (13.6) or Equivalent Frame (13.7) may be used for gravity loads.
- **13.5.3 Moment transfer:**
  - **γf** of the unbalanced moment is carried by flexure within an **effective width = column or capital width + 1.5h each side** (h of the slab or drop panel):
    **γf = 1 / [1 + (2/3)√(b1/b2)]**  (13-1)
  - **(ค) Adjustment:**
    - γf may be taken as **1.0** at edge columns (moment about an axis parallel to the edge) if Vu ≤ **0.75φVc** (edge) or ≤ **0.5φVc** (corner).
    - At interior supports, and at edge columns with moment about the axis perpendicular to the edge, γf may be increased by up to **25 %** if Vu ≤ **0.4φVc**, with the net tensile strain εt limited.
  - **(ง) Detailing:** reinforcement over the column must be concentrated, by **closer spacing or additional bars**, to resist γfMu within the **c2 + 3h** effective width. Show this on typical flat-slab column-head details.
  - [FLAG — misprint] 13.5.3(ค)(2) prints εt "**not exceed** 0.010". ACI 318-11 13.5.3.3(b) says εt **not less than** 0.010. Adopt "≥ 0.010".
  - [FLAG — stale reference] 13.5.3(ก) refers to "**11.12.7**" (ACI 318-08 numbering). Read as **11.11.7**.

### 13.6 Direct Design Method (pp.125–129) — brief (coefficients not needed)
- **Limits (13.6.1):**
  - ≥ 3 continuous spans each way;
  - rectangular panels with long/short ≤ 2 (c/c);
  - adjacent spans differ by ≤ 1/3 of the longer;
  - column offset ≤ 10 % of the span;
  - gravity, uniform load only;
  - panels with beams: 0.2 ≤ αf1ℓ2²/(αf2ℓ1²) ≤ 5.0 (13-2), with αf per 13-3;
  - no 8.4 redistribution (13.6.7 allows ±10 % instead).
  - [FLAG] 13.6.1(จ) prints "load ≤ 2 × unfactored load", which drops the words live and dead. ACI 318-11 13.6.1.5 is "unfactored **L ≤ 2 D**".
- **13.6.2:** Mo = qu ℓ2 ℓn²/8 (13-4), with ℓn ≥ 0.65ℓ1. Circular or polygonal supports are taken as squares of equal area.
- **13.6.3:** Negative moment at the face of rectangular supports.
  - Interior span: 0.65 / 0.35.
  - End-span table: exterior negative 0 / 0.16 / 0.26 / 0.30 / 0.65 for (1)–(5).
  - The **edge beam or slab edge is designed for torsion** from the exterior negative moment ((จ)).
  - Gravity moment transferred to the edge column = **0.3Mo** ((ฉ)).
- **13.6.4–13.6.6:**
  - Column-strip and middle-strip distribution.
  - Beams take **85 %** of the column-strip moment if αf1ℓ2/ℓ1 ≥ 1.0 (linear to 0).
  - A middle strip adjacent to a wall-supported edge takes **2 ×** the half-middle-strip moment.
- **13.6.8:** Beams with αf1ℓ2/ℓ1 ≥ 1.0 carry shear from the tributary area bounded by **45° lines** from panel corners (linear interpolation below 1.0).
- **13.6.9:** Moments in columns and walls (13-7).

### 13.7 Equivalent Frame Method (pp.129–131) — brief
- **13.7.2:** Frames along column lines in both directions. Each frame has a row of columns plus the slab-beam strip bounded by the panel centrelines. Edge frames run from the edge to the panel centreline.
- Columns attach through **torsional members** (13.7.5).
- Live-load patterning per 13.7.6.
- No detailing rules beyond Fig. 13.3.8 (13.3.8(ง)).

---

## Consolidated flags (slab clauses; not already in DIGEST or BEAM)

| # | Clause (PDF p.) | As printed | ACI 318-11 / adopted reading |
|---|---|---|---|
| S1 | 9.5.3(ค) last para (p.76) | ℓn, β defined "in (2) and (4)" | **(2) and (3)** (Eq. 9-11/9-12) |
| S2 | Table 9.3 (p.76) | fy rows 300 / 400 / 500 MPa | ACI 280 / 420 / 520 MPa, same ratios. Deliberate; adopt as printed |
| S3 | Table 9.3 title (p.76) | "ตามรางที่ 9.3" | ตารางที่ 9.3 (typo) |
| S4 | 13.3.8(จ) (p.122) | Mechanical/welded splice "per 12.14.3" | EIT **12.14.4** (EIT 12.14.3 = laps of different sizes) |
| S5 | 13.5.3(ก) (p.124) | Eccentric shear "per 11.12.7" | **11.11.7** |
| S6 | 13.5.3(ค)(2) (p.124) | εt "not exceed" 0.010 | εt **≥ 0.010** |
| S7 | 13.6.1(จ) (p.125) | "Load ≤ 2 × unfactored load" | Unfactored **L ≤ 2D** |
| S8 | 13.2 (p.121) | No shear-cap definition (ACI 13.2.6), but the term is used in 11.11.1(ข)(2) | Adopt ACI: cap extends from the column face ≥ its projection below the soffit |
| S9 | 13.3.8 (p.122) | ACI 13.3.8.6 (integrity bars through shearheads or lift collars) omitted | Adopt ACI on shearhead details |
| S10 | 7.7 (DIGEST) | ACI 7.7.5 headed-stud cover omitted | Stud heads and base rails get the same cover as the flexural bars |
| S11 | 11.11.5(ข) (p.107) | Prestressed spacing "per 11.11.2(ข)" | Stale reference (ACI 11.11.2.3); irrelevant for RC |
| — | 7.12.2(ข), 8.11.5(ข) | S&T and flange-bar spacing ≤ 400 mm | ACI 450. Deliberate EIT tightening (already in DIGEST and BEAM) |

---

## Slab detailing quick table

| Item | Rule | Clause (PDF p.) |
|---|---|---|
| Cover: slab, not exposed | 20 mm (≤ 16 mm bars) / 30 mm (≥ 20 mm bars) | 7.7.1(ค)(2) (p.58) |
| Cover: slab exposed to weather or earth | 40 (≤ 16) / 50 (≥ 20) mm; cast against earth 75 mm | 7.7.1(ก),(ข) (p.57) |
| Floor finish | Monolithic concrete finish may count as cover | 8.13.2 (p.70) |
| Placing tolerance (d ≤ 200) | d ± 10 mm (printed ±100); cover −10 mm, ≤ 1/3 cover | 7.5.2 (p.56) |
| Min. clear bar spacing | ≥ db, ≥ 25 mm | 7.6.1 (p.57) |
| Max. spacing, main bars, one-way slab | ≤ 3h, ≤ 450 mm (+ crack control 10.6.4) | 7.6.5 (p.57), 10.5.4 (p.81) |
| Max. spacing, two-way slab at critical sections | ≤ 2h | 13.3.2 (p.122) |
| Min. As, main bars, uniform slab | = S&T ratio on b·h | 10.5.4 (p.81), 13.3.1 (p.121) |
| S&T steel (one-way, perpendicular to main) | 0.0025 SR24 / 0.0020 SD30 / 0.0018 SD40 or WWR, ≥ 0.0014; ≤ 5h, ≤ 400 mm | 7.12 (p.62) |
| Crack control, one-way slab | s ≤ 380(280/fs) − 2.5cc ≤ 300(280/fs); fs = 2/3 fy | 10.6.4 (p.81) |
| One-way min. h (SD40, NW) | ℓ/20 simple, ℓ/24 one end cont., ℓ/28 both cont., ℓ/10 cantilever; × (0.4 + fy/700) | 9.5.2, T9.1 (p.73) |
| Ribbed one-way slab min. h | ℓ/16, ℓ/18.5, ℓ/21, ℓ/8 | T9.1 (p.73) |
| Two-way, no interior beams (SD40) | ℓn/30 ext. no edge beam; ℓn/33 ext. with edge beam or interior; with drops ℓn/33, ℓn/36; min. 125 mm (no drop) / 100 mm (drop); edge beam αf ≥ 0.8 | 9.5.3(ข), T9.3 (pp.75–76) |
| Two-way with beams | αfm ≤ 0.2 → T9.3; 0.2–2.0 → Eq. 9-11, ≥ 125 mm; > 2.0 → Eq. 9-12, ≥ 90 mm; discontinuous edge: αf ≥ 0.8 or h + 10 % | 9.5.3(ค) (p.76) |
| Coefficients, slabs ≤ 3 m | Negative wuℓn²/12 at all supports | 8.3.3 (p.66) |
| Short slabs ≤ 3 m | Analyse on knife-edge supports, span = clear span | 8.8.4 (p.68) |
| Slab-beam flange | ≤ span/4; overhang ≤ 8hf, ½ clear; edge beam ≤ span/12, 6hf | 8.11.2–8.11.3 (p.69) |
| Top bars across beam (main bars parallel to beam) | Design as cantilever; ≤ 5h, ≤ 400 mm | 8.11.5 (pp.69–70) |
| Joist slab | Rib ≥ 100 mm, depth ≤ 3.5 bw, clear spacing ≤ 750 mm; topping ≥ ℓc/12 and 40/50 mm; ≥ 1 continuous bottom bar, hooked at non-continuous ends | 8.12 (p.70), 7.13.2(ก) (p.63) |
| Pipes in slab | OD ≤ h/3; ≥ 3Ø c/c; between top and bottom bars; cover 35 / 20 mm; 0.002Ac normal to pipes | 6.3 (DIGEST) |
| Positive bars into support (one-way) | ≥ 1/4 (continuous) or 1/3 (simple) extend into support | 12.10.1 (p.115) |
| Negative bar cut-off | ≥ 1/3 of top steel beyond point of inflection ≥ max(d, 12db, ℓn/16) | 12.11.3 (p.115) |
| Two-way: bottom bars at discontinuous edge | Extend to the slab edge; ≥ 150 mm straight or hooked into edge beam, column or wall | 13.3.3 (p.122) |
| Two-way: top bars at discontinuous edge | Hook or anchor into edge beam, column or wall; develop at face | 13.3.4 (p.122) |
| No edge beam, or cantilever | Bars may anchor within the slab | 13.3.5 (p.122) |
| Corner reinforcement | Exterior corners, edge beam or wall αf > 1.0: top + bottom for max. positive moment; extent ℓlong/5 each way; top parallel to diagonal and bottom perpendicular, or two layers parallel to edges | 13.3.6 (p.122) |
| Drop panel | Projection ≥ h/4 below slab; extent ≥ ℓ/6 each way from support centreline; design depth ≤ ¼ distance from drop edge to column face | 13.2.5 (p.121), 13.3.7 (p.122) |
| Column strip | 0.25 × min(ℓ1, ℓ2) each side of column centreline | 13.2.1 (p.121) |
| Beam in two-way system | Includes slab each side = projection, ≤ 4h | 13.2.4 (p.121) |
| Flat slab, column-strip top | 50 % ≥ 0.30ℓn (0.33ℓn with drop), rest ≥ 0.20ℓn from face; hooked at exterior | Fig. 13.3.8 (p.123) |
| Flat slab, middle-strip top | 100 % ≥ 0.22ℓn from face; hooked at exterior | Fig. 13.3.8 |
| Flat slab, column-strip bottom | 100 % continuous; 150 mm into exterior support; splices only over interior support zone | Fig. 13.3.8 |
| Flat slab, middle-strip bottom | 50 % continuous, 150 mm into supports; rest may stop ≤ 0.15ℓn from interior face, 150 mm into exterior support | Fig. 13.3.8 |
| Unequal spans | Top-bar extensions based on longer span | 13.3.8(ข) (p.122) |
| Bent bars (flat slab) | Only if bend ≤ 45° | 13.3.8(ค) (p.122) |
| Flat-slab integrity | All column-strip bottom bars continuous or Class B lap / mechanical splice; ≥ 2 bottom bars each way through the column core, anchored at exterior supports | 13.3.8(จ) (p.122), 7.13.2(ฉ) (p.63) |
| Moment-transfer band | Concentrate top bars within c2 + 3h (1.5h each side) for γfMu; γf = 1/[1 + (2/3)√(b1/b2)] | 13.5.3(ข),(ง) (pp.124–125) |
| Openings, flat slab | Middle∩middle any size (keep total bars); column∩column ≤ 1/8 column-strip width; column∩middle ≤ 1/4 of strip bars interrupted; replace interrupted bars at sides | 13.4.2 (p.123) |
| Openings near columns (shear) | Within 10h of column, or in column strip: remove perimeter inside tangents from column centroid (half with shearhead) | 11.11.6 (p.107) |
| Punching critical section | d/2 from column face, and d/2 from drop-panel or cap edge; rectangular perimeter allowed | 11.11.1(ข),(ค) (p.104) |
| Vc punching | min[0.17(1 + 2/βc), 0.083(αs d/bo + 2), 0.33] λ√f'c bo d; αs 40/30/20 | 11.11.2 (pp.104–105) |
| Stirrups in slab | d ≥ 150 mm and ≥ 16 × stirrup dia.; Vc ≤ 0.17λ√f'c bo d; Vn ≤ 0.5√f'c bo d; first line ≤ d/2; lines ≤ d/2; legs ≤ 2d along first line; anchor per 12.12, engage flexural bars | 11.11.3 (p.105) |
| Headed stud rails | Vc ≤ 0.25, Vn ≤ 0.66 λ√f'c bo d; Av fyt/(bo s) ≥ 0.17√f'c; first line ≤ d/2; line spacing ≤ 0.75d (vu ≤ φ0.5√f'c) or 0.5d; ≤ 2d along first line; height = h − covers − ½db | 11.11.5 (pp.106–107) |
| End of shear reinforcement | Stress ≤ φ0.17λ√f'c at d/2 beyond the outermost line | 11.11.5(ง), 11.11.7(ข)(2) (pp.107–108) |
| Shearheads | Depth ≤ 70tw; compression flange within 0.3d; ends cut ≥ 30°; αv ≥ 0.15; Vn ≤ 0.58√f'c bo d | 11.11.4 (pp.105–106) |
| Column ties through slab joint | Required unless restrained on 4 sides by beams or slabs of similar depth (non-seismic system) | 11.10.2 (p.104) |
| Min. shear reinforcement | Not required in slabs and footings | 11.4.5(ก)(1) (p.94) |

---

# Part C. TATA RC detailing handbook (M. Jiravacharadet) - slab chapter and appendix sheets


Source: Mongkol Jiravacharadet, *RC DETAILING* (TATA Tiscon handbook), 214 pp.
Citations are (TATA p.<printed page>, Fig x.y). PDF page = printed page + 8.
Units: m and cm (Thai drafting practice) unless marked mm. Bar marks: RB = round plain bar, DB = deformed bar; "#" after a spacing = mesh (both ways); "T&B" = top and bottom.
[UNCERTAIN] marks values or readings I could not confirm from the page. Paraphrased; no long verbatim quotes.

---

## 0. General rules found (incl. Ch.1 items used by slab details)

| Rule | Value | Source |
|---|---|---|
| Min cover, slab/wall/joist, not exposed to weather or ground | 2 cm | TATA p.8, Table 1.7 (Ch.1, outside Ch.3) |
| Min cover, exposed to weather or ground (cast against formwork): DB20 and larger / DB16 and smaller | 5 cm / 4 cm | TATA p.8, Table 1.7 |
| Min cover, cast against and permanently in contact with ground (slab on ground, footing) | 7.5 cm | TATA p.8, Table 1.7 and Fig 1.8(c) |
| Min clear bar spacing | largest of db, 2.5 cm, 1.33 x max aggregate size; clear distance between layers ≥ 2.5 cm | TATA p.7–8, Fig 1.7 |
| Extra top cover on car parks and factory floors, to allow for wear | mentioned, no value given | TATA p.7 |
| Welded wire mesh (TIS 737-2549): cold-drawn wire 4–16 mm | lap = larger of (mesh pitch S + 2.5 cm) or 30 cm | TATA p.11, Fig 1.11 |
| Two-way slab, flat slab: max bar spacing | 2 x slab thickness. The printed text says "not less than", which must be a typo for "not more than" [UNCERTAIN wording] | TATA p.76 |
| Flat slab: bottom bars at a discontinuous edge | extend into the edge beam, column or wall; embed or hook at least 15 cm | TATA p.76, Figs 3.51/3.52 |
| Min flexural steel in two-way slabs, As,min (ACI 318-14), placed at the tension face | deformed bars with fy < 4,200 ksc: 0.0020 Ag. Deformed bars or wire mesh with fy ≥ 4,200 ksc: larger of 0.0018 x 4,200/fy x Ag and 0.0014 Ag | TATA p.82, Table 3.3 |
| Distinction noted by the book | shrinkage/temperature steel is spread over the whole section; As,min flexural steel sits at the tension face | TATA p.82 |
| Min bend diameter D | 6db for 6–25 mm, 8db for 28–36 mm, 10db for 44–57 mm | TATA p.174 (appendix) |
| Standard hook extensions | 180° hook: 4db ≥ 60 mm. 90° hook: 12db | TATA p.174 |

**Standard hook table** (TATA p.174), mm. D = bend diameter; G = overall hook length; J = hook depth:

| Bar | D | 180° G | 180° J | 90° G | 90° J |
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

**Not found in the source (do not attribute to TATA):**
- no min-thickness table for beam-supported one-way or two-way slabs (ln/20, ln/24, ln/28, ln/10)
- no "3h or 450 mm" / "5h or 450 mm" spacing rule
- no 0.0025 ratio
- no minimum slab bar size
- no named shrinkage/temperature ratio for one-way slabs. Only Table 3.3 above gives ratios.

---

## 1. Slab designation on plans (TATA p.51–52, Figs 3.1–3.3)

- Slab marks:
  - S1, S2, … = cast-in-place one-way or two-way slab
  - SP or PS = precast slab
  - GS or SG = slab on ground (p.51, 56, 63)
- Symbol: slab mark written in a circle, with arrows showing the span direction:
  - one-way slab: a single double-headed arrow parallel to the SHORT span S (the load-carrying direction) (Fig 3.3)
  - two-way slab: arrows in both directions (cross) (p.54, S2)
  - precast slab: single arrow parallel to the direction the planks span (p.56, Fig 3.13)
- Fig 3.1 is a sample floor plan: PS bays with arrows, an S2 two-way bay, an S1 one-way bay and a void (X).
- One-way slab definition: long side L > 2 x short side S. The slab carries load in the short direction and behaves like a beam supported on the two long edges (p.51, Figs 3.2/3.3).
- Two-way slab definition: L ≤ 2S, supported on all four edges (p.54, Fig 3.8).

---

## 2. One-way slab (TATA p.51–54, Figs 3.4–3.7)

### 2.1 Typical section drawn along the short span (Fig 3.4, p.52)
- Detail drawings usually show only the section along the short span.
- Short-direction main bars are drawn as lines, like beam bars:
  - bottom bars run the full span into both supports
  - top bars are placed over the supports
- Long-direction (distribution / anti-crack) bars are drawn as dots. They tie the short bars into a mesh.
- Layer order in the figure:
  - bottom layer: short bar is lowest (outermost); long-direction dots sit on top of it
  - top layer: short bar is uppermost (outermost); long-direction dots sit under it
- Exterior support: the top short bar ends in a 90° hook turned DOWN into the edge beam. The bottom bar runs straight into the beam.
- Interior support: the top bar runs continuously over the beam into the next span.

### 2.2 Separate top and bottom mats (Fig 3.5, p.53)
- The bottom mat sits on mortar spacer blocks.
- The top mat is carried on chairs ("crow's-foot" bars):
  - DB12 at 1.00–1.50 m spacing each way
  - chair feet about 0.30 m long [dimension read from figure]
- hc = distance between the outer faces of the top and bottom mats. It sets the chair height.

### 2.3 Alternate bent-up bars (Figs 3.6, 3.7; p.53–54)
- Method: every second bottom bar is cranked up (the Thai name translates as "horse-neck, alternate bar") to become a top bar over the support. It also supports the top layer.
- Extra top bars are added between the cranked bars, at twice the main spacing. Top steel at the support then equals the bottom steel at midspan.
  - Example: RB9 @ 0.10 alternate bent-up, plus RB9 @ 0.20 extra top. This gives RB9 @ 0.10 effective, As = 6.36 cm²/m.
- **Worked example (Fig 3.7):**
  - clear span 3.7 m; t = 12 cm
  - main bars: RB9 @ 0.08 m alternate bent-up
  - extra top: RB9 @ 0.16 m
  - distribution (anti-crack) bars: RB9 @ 0.20 m
  - Exterior (discontinuous) support:
    - top bar extends 0.95 m from the support face (≈ ln/4), with a 90° hook down at the beam
    - crank of the bent-up bar starts 0.55 m from the face (≈ ln/7)
  - Interior (continuous) support:
    - top bars extend 1.25 m from the face (≈ ln/3)
    - crank point is 0.95 m from the face (≈ ln/4)
    - the label reads "RB9 @ 0.08 alternate bent-up + extra"
- The same fractions are used for two-way slabs (Fig 3.10).

---

## 3. Two-way slab (TATA p.54–55, Figs 3.8–3.11)

- Bottom mat in both directions. Short-direction bars go BELOW the long-direction bars, for greater effective depth, because the short direction carries the larger moment (Fig 3.9).
- In each section, bars in one direction are drawn as lines and bars in the other as dots.
- Top bars in each direction are either an independent mat or alternate bent-up bars as in one-way slabs (p.55).
- **Standard cut-off fractions (Fig 3.10).** Measured from the support face, using the clear span of that direction (Sn for the short-span section, Ln for the long-span section):

| Location | Top-bar extension from face | Bent-up crank point from face |
|---|---|---|
| Discontinuous (exterior) edge | Sn/4 (Ln/4) | Sn/7 (Ln/7) |
| Continuous (interior) edge | Sn/3 (Ln/3) | Sn/4 (Ln/4) |

- The top bar at the exterior edge is hooked down 90° into the edge beam.

- **Worked example (Fig 3.11):**
  - beams 0.20 m wide, 0.50 m deep; slab 0.10 m thick
  - main bars DB10 @ 0.20 alternate bent-up; extra top bars DB10 @ 0.40 at each support
  - Short direction, clear span 3.80 m:
    - exterior: top extends 0.95, crank at 0.55
    - interior: top extends 1.30, crank at 0.95
  - Long direction, clear span 4.80 m:
    - exterior: top extends 1.20, crank at 0.70
    - interior: top extends 1.60, crank at 1.20
  - These match the Sn/4, Sn/7, Sn/3, Sn/4 fractions, rounded up.

---

## 4. Corner (torsion) reinforcement at exterior corners (TATA p.61–63, Figs 3.23–3.25)

- Twisting moments Mxx and Myy peak at slab corners. Without enough capacity, diagonal cracks form on the top surface across the corner diagonal, and on the bottom surface (Fig 3.24).
- **Rule:** at exterior building corners, add top and bottom corner bars over a square L/5 x L/5 measured from the corner.
  - L = the LONGER clear span between supports (p.62).
  - Spacing = that of the midspan bottom bars in whichever direction has the smaller spacing (p.62).
- Two alternative layouts (Fig 3.25):
  - **(a) Option 1, diagonal bars:**
    - TOP bars parallel to the corner diagonal
    - BOTTOM bars perpendicular to the diagonal
    - both confined to the L/5 x L/5 zone
  - **(b) Option 2, orthogonal bars:** a mesh of As in both directions, top and bottom, over the L/5 x L/5 zone.
- **Amount (ACI 318-14):** corner steel is needed when the edge beams have αf > 1.0. As = the steel for the maximum positive moment per unit width of the slab (p.63).

---

## 5. Slab openings (TATA p.59–61, Figs 3.19–3.22)

- Openings in slabs without trimmer beams have high stress at the corners, so diagonal bars go at every corner, top and bottom (p.59).
- **Small openings, < 0.60 m, in slabs or RC walls, unless shown otherwise (Fig 3.19):**
  - 2-DB12 x 0.70 m diagonal bars @ 0.05 m, T&B, at every corner
  - bars at 45°, ends drawn hooked
- **Large openings, ≥ 0.60 m, unless shown otherwise (Fig 3.20):**
  - Trimmer bars along each side: 2-DB16 @ 0.10 m (T&B), parallel to each opening edge. They extend 0.80 m beyond the opening corner in each direction, dimensioned 0.80 m past the corner both vertically and horizontally.
  - Diagonal bars: 2-DB12 x 1.0 m at every corner (T&B), labelled "@ 0.5 m". This is probably a misprint for @ 0.05 m, as in Fig 3.19 [UNCERTAIN].
  - Openings cut later that are not on the structural drawings (e.g. aircon pipe sleeves) need bars around the opening that restore the strength of the concrete removed (p.59).
- **EIT rules: openings with no strength check needed (p.59):**
  1. Opening within the area common to two intersecting MIDDLE strips: allowed, provided the total reinforcement equals that of the slab without the opening.
  2. Opening width limited to ≤ 1/8 of the column-strip width in that direction. The Thai text says "intersection of two middle strips" here too. By ACI/EIT this clause is the intersection of two COLUMN strips; the text is likely a typo [UNCERTAIN].
  3. Opening in the area common to one column strip and one middle strip:
     - bars interrupted in each direction must be ≤ 1/4 of the bars in that strip
     - the interrupted steel is re-placed alongside the opening, in each direction
- **Worked replacement example (p.59):**
  - Given: bottom bars DB12 @ 0.15 m # (As = 1.13 cm² per bar); opening 0.80 x 0.80 m.
  - Bars cut = 80/15 = 5.33.
  - Area lost = 1.13 x 5.33 = 6.02 cm².
  - Required each side = 6.02/2 = 3.01 cm², so provide 2-DB16 (4.02 cm²) on EACH side, in each direction.
  - The sketch shows the extra bars in pairs on all four sides, running past the opening.
- **Precast (hollow-core) slabs:**
  - Small openings (Fig 3.21, p.60): round Ø ≤ 150 mm, or rectangular with width ≤ 150 mm, may be cut only at a hollow core. No more than 3 openings in the same plank cross-section.
  - Large openings (Fig 3.22, p.61): a full-plank-width opening uses steel angle trimmers.
    - One angle frames the cut plank ends.
    - Transverse angles sit on the adjacent full planks and carry the cut planks' load to them.

---

## 6. Precast plank slabs (PS/SP) (TATA p.56–58, Figs 3.12–3.18)

- **Plank types (Fig 3.12):**
  - Solid plank: 30–35 cm wide x 5 cm thick, prestressed wires to design; for small works.
  - Hollow core: 60 cm wide x 10–15 cm thick; for large works.
- Erection (Fig 3.13): planks are lifted onto the supporting beams, then the topping mesh is laid and the topping cast.
- Planks span one way. Alternate the span direction bay-by-bay so load goes to beams in both directions (Fig 3.15 plan, p.57).
- **Topping (Fig 3.14):**
  - cast-in-place topping 5 cm
  - mesh RB6 @ 0.20 m, or 4 mm welded wire mesh
  - plank bears about 0.05 m on the beam
  - at the edge beam: RB9 @ 0.40 m top bars extend 0.50 m into the slab and are hooked down into the beam. Figure shows 0.25 vertically [UNCERTAIN: which point the 0.50 is measured from; 0.25 is probably the hook depth or the beam-to-topping depth]
  - plank + topping drawn as 0.05 + 0.05 m
- **Support details for hollow-core planks.** Common features: topping 0.05 m over plank depth T; topping mesh RB9 @ 0.20 m #.
  - **Rule (p.58):** to stop cracking at plank ends due to deflection, add top bars over a length L/10, where L = plank span. At end spans, anchor the bars into the supporting beam.
  - **Section 1-1, interior beam between plank ends (Fig 3.15 second, p.57):**
    - plank ends stop 0.05 m each side of the beam centreline; the 10 cm gap is filled with concrete
    - extra top bars RB9 @ 0.20 m run L/10 each side of the beam CL
    - vertical RB9 @ 0.20 m bars go 0.30 m down into the RC beam and tie into the topping
  - **Section 2-2, end joint at an edge beam (Fig 3.16, p.58):**
    - top bars RB9 @ 0.20 m # over L/10 from the beam
    - the bar turns down at 0.05 m from the outer face and goes 0.30 m into the beam as RB9 @ 0.20 m
  - **Section 3-3, side joint where the plank runs parallel to the edge beam (Fig 3.17):**
    - a cast-in-place strip fills between the last plank and the beam edge, depth T + 0.05
    - RB9 @ 0.20 m # top and bottom in the strip, closed at the edge with the top bar hooked down and the bottom bar hooked up
    - a beam bar rises 0.30 m into the strip
    - topping mesh laps over the plank
  - **L-shaped (rebated) edge beam to reduce floor depth (Fig 3.18):**
    - plank bears on a 0.10 m ledge
    - top RB9 @ 0.20 m # over L/10, hooked down into the beam
    - the figure shows the beam's cage

---

## 7. Slab on ground (GS/SG) (TATA p.63–72, Figs 3.26–3.43)

### 7.1 General
- Build on competent soil: level and compact the subgrade, then blind with coarse sand and lean concrete (p.63).
- Typical thickness 15–30 cm (p.63).
- Small houses may bear the floor directly on the ground if the allowable soil bearing is ≥ 5 t/m² (p.63, Fig 3.27).
- Joints and their spacing control cracking from shrinkage and temperature (Fig 3.28).
- **Joint spacing:**
  - rule of thumb: max joint spacing ≈ 30 x slab thickness; e.g. t = 15 cm gives 4.5 m (p.65)
  - Fig 3.29 chart of max joint spacing band vs thickness, values read off the curve [approximate]:

| t | Max joint spacing |
|---|---|
| 5 cm | ≈ 2–3 m |
| 10 cm | ≈ 3.6–4.6 m |
| 15 cm | ≈ 4.7–7 m |
| 20 cm | ≈ 5.7–8 m |
| 25 cm | ≈ 6.2–8.7 m |

- Edges against beams or walls: leave a gap so the slab moves freely without loading the structure, then seal with an elastic material such as bitumen. External slab edges are thickened to keep the subgrade from washing out (p.65).

### 7.2 Typical SOG sections (Fig 3.30, p.65)
- **Interior slab between ground beams (GB):**
  - single mesh placed 3–5 cm below the top surface, and never deeper than t/2
  - 2–2.5 cm isolation gap with filler against each GB face
  - bar ends hooked (180°)
  - base: compacted moist sand 5–10 cm
- **Exterior slab:**
  - thickened edges 5–10 cm deeper than the slab soffit
  - 10 cm flat bearing width at the outer edge, then a 45° slope up to the soffit
  - mesh bars turned down 90° into the thickening at both edges
  - on compacted moist sand 5–10 cm
- **Exterior slab, mixed edges:** one edge is a thickened free edge with a hooked mesh; the other abuts a GB with an isolation gap.

### 7.3 Joint types (p.65–68)
1. **Expansion joint (Fig 3.33, p.67):**
   - full separation of concrete and reinforcement
   - compressible filler 2 cm wide, sealant on top (e.g. bitumen)
   - dowel bars at mid-depth t/2; default if not specified: **DB25, 0.60 m long, @ 0.30 m**
   - half the dowel fully bonded; the other half coated with bitumen or paint (debonded, "lubricated")
   - heavy-traffic slabs: an expansion cap on the free end, about 5 cm long with 2.5 cm free travel
2. **Contraction joint (Fig 3.34, p.67; the caption wrongly repeats "Expansion joint"):**
   - induces the crack along a set line
   - dowel at t/2, half bonded and half lubricated, length L
   - top groove/sealant about 2 cm wide [UNCERTAIN whether 2 cm is the groove width]
   - no filler through the depth
3. **Crack-control joint (Fig 3.35, p.68):**
   - groove tooled into fresh concrete, or saw cut after hardening, then joint-filled
   - 0.3 cm wide, depth t/4
   - creates a weakened plane
4. **Construction joint (Fig 3.36, p.68):**
   - day-work stop against a clean bulkhead form
   - dowels may pass through the bulkhead to transfer load
   - Day 1 / Day 2 pours

### 7.4 Pour sequence (p.66)
- Fig 3.31, alternate-bay (checkerboard) pouring:
  - bays 6–10 m x 4.5 m
  - dowels at 0.30 m c/c across the bay joints
- Fig 3.32, ACI 302.1R-04: recommends long-strip pouring instead of checkerboard.
  - strips are cast first, then infill strips
  - contraction joints (dashed) run across the strips; construction joints separate the strips
  - Reasons: early shrinkage is too slow for checkerboard to help; access is harder; joints may misalign.

### 7.5 Road / pavement slab (Figs 3.37–3.39, p.69–70)
- **Plan (Fig 3.37):**
  - transverse joints every 10.00 m; longitudinal joint at lane width
  - mesh RB9 @ 0.20 m and RB9 @ 0.40 m. Which bar runs which way is [UNCERTAIN]; the figure shows @ 0.20 dimensioned across the lane and @ 0.40 along it.
- **Transverse (expansion) joint (Fig 3.38):**
  - dowels **DB25 x 0.50 m @ 0.30 m c/c** at T/2
  - one half painted and greased, with an end cap
  - joint filler, joint sealer on top
  - mesh stops either side of the joint, placed in the lower part of the slab [position read from figure]
  - build-up: 10 cm compacted sand, 15 cm subbase, compacted subgrade
- **Longitudinal joint (Fig 3.39):**
  - DB25 x 0.50 m @ 0.30 m c/c at T/2, bonded both sides (tie bar)
  - formed/cracked joint with joint sealer at the top
  - same build-up as the transverse joint

### 7.6 SOG inside buildings (Figs 3.40–3.43, p.70–72)
- **Isolation joints** separate the floor slab from beams, columns, walls and machine bases. They release horizontal and vertical movement.
  - Full-depth compressible filler, with the top recess sealed (bitumen).
  - Fig 3.42: the column base is encased in concrete poured separately; the slab is isolated from the encasement.
  - Fig 3.43: around machine bases the joint is sealant over elastic filler. It also isolates vibration.
- **Joint layout (Fig 3.41):**
  - contraction or construction joints on the column grid lines and at mid-bay
  - isolation joint around each column and around equipment foundations, and along perimeter walls
  - **corner bars at re-entrant corners** (2 diagonal bars) where a slab panel has a re-entrant corner, e.g. at an equipment base
- **Column isolation shapes (Fig 3.41 plan, p.71):**
  - a diamond (square rotated 45°) or a circle around the column
  - contraction joints run into the diamond's points, or tangent to the circle
  - the concrete inside the diamond or circle is poured after the slab and column carry their dead load
- Fig 3.40 3D view: slab thickness on compacted granular subbase; isolation joints at the interior columns; contraction joints on the column lines.

---

## 8. Flat slab & flat plate (TATA p.72–83, Figs 3.44–3.59; plus p.97–98 Figs 4.17–4.20)

### 8.1 Systems and economic spans (Table 3.1, p.73)

| System | Span |
|---|---|
| Flat plate | 6–9 m |
| Flat slab with column capitals | 8–11 m |
| Flat slab with drop panels | 9–12 m |
| Slab with slab bands | 8–14 m |

### 8.2 Minimum thickness, EIT 1008-38 (Table 3.2, p.74). L = span.
- Absolute minimum: 12.5 cm without drop panels; 10.0 cm with drop panels.

| fy (ksc) | No drop: exterior, no edge beam | No drop: exterior, with edge beam | No drop: interior | Drop: exterior, no edge beam | Drop: exterior, with edge beam | Drop: interior |
|---|---|---|---|---|---|---|
| 3,000 | L/33 | L/36 | L/36 | L/36 | L/40 | L/40 |
| 4,000 | L/30 | L/33 | L/33 | L/33 | L/36 | L/36 |

### 8.3 Drop panels and capitals (p.74, Fig 3.44)
- **Drop panel:**
  - extends ≥ L/6 of the span in each direction, measured from the support centreline
  - projection below the slab ≥ t/4
- **Column capital:**
  - cone or pyramid sloping at ≥ 45° to the horizontal
  - overall size ≤ L/4
  - at least 4 cm vertical thickness at its top edge
- Head types (Fig 4.17, p.97): capital only; capital + drop panel; drop panel only. Square and round heads shown (Fig 4.18).
- **Capital reinforcement (p.98):** capitals are normally cast with the column.
  - Square capital (Fig 4.19): a cage following the capital shape, with bars in both directions:
    - inclined bars along the sloping faces, hooked into the slab
    - horizontal perimeter hoops
    - a central grid over the column
  - Circular capital (Fig 4.20):
    - column splice bars run up through the head into the slab
    - "firm cage" of inclined bars with horizontal circular hoops
    - a 50 mm step at the head/slab junction
    - column concrete is cast up to the underside of the head before the head cage is placed
    - the last column stirrup sits just below that level

### 8.4 Column strip / middle strip (p.74–76, Figs 3.45–3.47)
- **Column strip:** width on EACH side of the column line = 1/4 of the SHORTER span L1. Total = L1/2, in both directions (Figs 3.45, 3.46).
- **Middle strip:** the band between two column strips.
- With drop panels, the column-strip width = drop-panel size (Fig 3.47).
- Design splits each strip into midspan zones (positive moment, bottom bars) and column zones (negative moment, top bars). Bars in the other direction complete the top and bottom meshes (Fig 3.48).

### 8.5 Bar layout plans (Figs 3.49, 3.50, p.77)
- **Bottom mat (Fig 3.49):** continuous mesh over the whole bay in both directions.
- **Top mat (Fig 3.50):** zoned.
  - Column zone (column strip x column strip) over each column: main bars both ways.
  - Column strip x middle strip bands between columns:
    - "main bars" perpendicular to the column line, i.e. the negative steel of the crossing strip
    - lighter "tie/distribution bars" (the Thai term reads "supporting/tie bars") in the other direction
  - Middle x middle zone at bay centre: no top bars.
  - [UNCERTAIN: which way the main bars run in each yellow band, read from the tick-mark convention]
- **Fig 3.59 (p.83):** top flexural bars at As,min concentrated over the column, gridded in both directions, extending into the column strips.

### 8.6 Minimum bar extensions (ACI-type figure; Figs 3.51 & 3.52, p.78)
Ln = clear span (face to face), L = centre-to-centre span. Extensions are from the support face unless stated.
- **Middle strip, top (both figures):**
  - 100% As extends 0.22Ln from the face at exterior and interior supports
  - exterior end hooked down 90°
- **Middle strip, bottom:**
  - 50% As stops within a max of 0.125L from the interior support centreline
  - the other 50% As runs into the support and 7.5 cm past the support centreline, lapping with the next span's bars
  - exterior edge: bars extend at least 15 cm into the support
- **Column strip, top, WITHOUT drop panels (Fig 3.51):**
  - 50% As extends 0.30Ln; the remaining 50% As extends 0.20Ln
  - exterior ends hooked down
- **Column strip, top, WITH drop panels (Fig 3.52):**
  - 50% As extends 0.33Ln; the remaining 50% As extends 0.20Ln
- **Column strip, bottom:**
  - 50% As stops within a max of 0.125L of the centreline
  - 50% As continues 7.5 cm past the centreline
  - 15 cm into the exterior support; lower bar drawn with an upturn at the exterior edge
  - With drop panels: the bottom bars that stop short must extend at least **24db or 30 cm** into the drop panel, past its edge.

### 8.7 Punching shear (p.79–82, Figs 3.53–3.58)
- Failure surface is a truncated cone or pyramid around the column or drop. Crack angle θ = 20°–45° to the horizontal, depending on slab steel (Figs 3.53, 3.54).
- **Critical section** at d/2 from the column face:
  - interior, edge and corner columns; square and circular shapes (Fig 3.55)
  - other column shapes: the shortest perimeter b0 at d/2 from the effective loaded area; β = a/b for re-entrant shapes (Fig 3.56)
- **With drop panels: two critical sections (Fig 3.57):**
  - dd/2 from the column face, using the drop depth dd
  - d/2 from the drop-panel edge, using the slab depth d
- **Punching shear reinforcement types (Fig 3.58, p.81–82):**
  - (a) Shearheads: welded I or W steel sections embedded in the slab, crossing over the column, to enlarge the perimeter.
  - (b) Bent-up bars at 45° through the column, crossing the crack line and anchored as bottom bars with enough length.
  - (c) Stirrups with horizontal bars (beam-like cages) projecting from the column in both directions.
  - (d) Headed shear studs welded to a steel strip, in rails. Easy to install and effective.

---

## 9. Appendix typical-drawing sheets relevant to slabs

### 9.1 Slab steps (TATA p.181, sheet "slab reinforcement at a change of level")
Both slabs have thickness T; H = step height.
- **Step with H < T:**
  - Geometry: the upper slab's top rises by H. The lower slab's soffit continues a width T past the step face, then steps up to the upper soffit. This leaves a local thickened zone of width T and depth T + H.
  - Bars:
    - upper-slab top bar: runs to the step face, turns down vertically inside the face, then continues along the bottom of the lower slab for Ld (measured from the step face)
    - lower-slab bottom bar: runs to the far side of the thickened zone, turns up vertically, then continues into the upper slab near its top for Ld (measured from that inner face)
    - lower-slab top bar: runs straight through the step and continues Ld beyond the step face into the upper slab
    - upper-slab bottom bar: runs straight into the lower slab for Ld
  - All four sets: Ld = development length.
- **Step with H > T** (the sheet's own label inside the figure still reads "H < T", likely a copy error [UNCERTAIN]):
  - Geometry: the soffit under the step is sloped at about 45° (haunch).
  - Bars:
    - upper-slab top bar: turned down at the step face and run along the lower-slab bottom for Ld
    - upper-slab bottom bar: bent down at the step face into the lower slab
    - lower-slab top and bottom bars: both cranked up at 45° parallel to the sloping soffit, then continued Ld into the upper slab
  - [UNCERTAIN: exact start/end points of each Ld dimension]

### 9.2 Sunshade / edge fin on a slab edge (TATA p.181, "reinforcement in sun-shading panels")
Upstand (above slab) and downstand (below slab) fins at a slab edge. The fin's vertical bar anchors 400 mm into the slab with a horizontal leg.
- **Thin/short fin: thickness ≤ 100 mm, height ≤ 300 mm:**
  - one layer of 1DB10 @ 250 vertical (L-bar)
  - 1DB12 longitudinal at the free tip; 1DB10 longitudinal at the root
  - upstand: the leg turns into the slab bottom; downstand: the leg turns into the slab top
- **Thick/tall fin: thickness > 100 mm, height > 300 mm:**
  - 1DB10 @ 250 closed U/hairpin bars, both faces
  - 2DB12 at the free tip; 2DB10 at the root
  - 400 mm anchorage legs into the slab

### 9.3 Upstand and hanging ribs / curbs, when not specified (TATA p.182)
Cast onto a supporting member (slab or beam, shown hatched).

| Rib | Width | Height | Stirrup / anchorage | Tip bar | Longitudinal bars |
|---|---|---|---|---|---|
| Small | 70 mm | 300–500 mm | single RB6 @ 200 vertical, hooked both ends, embedded 300 mm into the support | 1DB12 | 2RB9 |
| Large | 100 mm | 500–1000 mm | RB6 @ 200 hairpins (both faces), embedded 300 mm | 1DB16 | RB9 @ 250 each face |

- Same arrangement mirrored for hanging (downstand) ribs.

### 9.4 Basement slab / wall waterproofing (TATA p.189)
- **Base slab build-up, top down:**
  - 1.5 mm polyethylene vapour barrier
  - lean concrete ≥ 50 mm
  - compacted sand ≥ 100 mm
- Base slab: top and bottom bars joined by U-bars at the slab edge.
- Wall starters: U-shaped, down to the bottom mat.
- **Wall kicker joint above the base slab:**
  - PVC waterstop 4" for 100 mm walls, 6" for 150 mm walls, 8" for 200 mm walls
  - waterstop wired to the bars before concreting
- Outer wall face: 1.5 mm polyethylene sheet, with brick protection against the soil.
- Roof/ground slab at the wall top: wall bars looped into the slab.

### 9.5 Wall–slab junctions (TATA p.190, wall sheet)
- **Exterior wall to top slab:**
  - wall bars turned into the slab as a U/loop
  - slab top bars lap Ls with the wall bar leg
- **Interior wall under a continuous slab:** wall bars form a U inside the slab depth.
- **Wall to base slab:**
  - wall bars end in a 90° standard hook at the bottom mat of the base slab, anchored Ld
  - kicker with waterstop
  - wall bar lap Ls above the kicker
  - at an interior wall, base-slab bars run past it by Ld

### 9.6 Opening trimming, wall sheet (TATA p.191); relevant because p.59 applies the opening rule to "slab or wall"
- Trimmer bars run ≥ 36db or 750 mm (min) past the opening.
- Diagonal bars 2DB16 at the corners, length 2B or 1200 mm (min), where B = opening size.
- Sheet applies to openings up to 1000 mm max.
- Replacement bars at 75 mm spacing, not fewer than 4DB16.
- Interrupted bars stop at the opening with a 90° standard hook, or are bent at a right angle.
- Note: the strength of the pierced element must not be less than the original.

### 9.7 Other appendix items touching slabs
- **Column sheets (TATA p.183–186):** column ties start 50 mm below the underside of beam or flat slab, and 50 mm above the slab. For spiral columns into a flat slab, horizontal ties at max 150 mm spacing through the joint.
- **Beam section sheet (TATA p.179):** shows slab thickness t on T-beams; 40 mm clear cover to beam stirrups. Beam only.
- **Stair (TATA p.171, Fig 7.36, floating-landing stair; chapter page, not appendix):**
  - landing/flight reinforced with main bars top and bottom
  - closed transverse stirrups around the full width B and thickness t
  - the landing is not treated as an ordinary slab

---

## 10. Drawing-ready typical details (candidates for typical slab sheets)

1. **One-way slab typical section**
   - Short-span section showing main bars as lines and distribution bars as dots.
   - Top bars: ln/4 at a discontinuous end (hooked down into the edge beam); ln/3 at a continuous end.
   - Crank points at ln/7 and ln/4 for the alternate bent-up option.
   - Distribution RB9 @ 0.20.
   - (Figs 3.4, 3.6, 3.7; p.52–54)
2. **Two-way slab typical sections, short and long directions**
   - Same fractions: Sn/4, Sn/7, Sn/3, Sn/4 and Ln/4, Ln/7, Ln/3, Ln/4.
   - Short bars outermost; hook at exterior beams.
   - Two options: separate top mat, or alternate bent-up bars + extras at 2 x spacing.
   - (Figs 3.9–3.11; p.54–55)
3. **Chair / spacer detail:** DB12 chairs @ 1.00–1.50 m each way, feet about 0.30 m; mortar spacers under the bottom mat; hc definition. (Fig 3.5; p.53)
4. **Exterior corner reinforcement (plan)**
   - L/5 x L/5 zone, L = longer span.
   - Option 1: diagonal top bars parallel to the diagonal, bottom bars perpendicular.
   - Option 2: orthogonal As both ways, T&B.
   - Spacing = the smaller midspan bottom spacing.
   - (Fig 3.25; p.62–63)
5. **Small opening < 0.60 m:** 2-DB12 x 0.70 m @ 0.05 T&B diagonals at each corner. (Fig 3.19; p.59)
6. **Large opening ≥ 0.60 m:** 2-DB16 @ 0.10 T&B trimmers extending 0.80 m past the corners; 2-DB12 x 1.0 m diagonals at each corner [spacing UNCERTAIN]. Include a note on the bar-replacement calculation and the EIT middle-strip / column-strip opening rules. (Fig 3.20; p.59–60)
7. **Precast hollow-core plank details**
   - Interior support: L/10 top bars, 10 cm infill gap, RB9 @ 0.20 into beam 0.30 m.
   - End support and side joint strip.
   - L-ledge beam with 0.10 m bearing.
   - Topping 5 cm with RB6 @ 0.20 or 4 mm mesh.
   - Plank opening limits: ≤ 150 mm, max 3 per section; angle trimmers for large openings.
   - (Figs 3.14–3.18, 3.21, 3.22; p.56–61)
8. **Slab-on-ground sections**
   - Interior slab between GBs: mesh 3–5 cm ≤ t/2 from top; 2–2.5 cm isolation filler; 5–10 cm compacted sand.
   - Thickened free edge: +5–10 cm, 10 cm flat, 45° slope.
   - (Fig 3.30; p.65)
9. **SOG joint details**
   - Expansion joint: 2 cm filler, DB25 x 0.60 @ 0.30 dowels at t/2, half debonded, cap for heavy traffic.
   - Contraction joint: dowelled, sealed groove.
   - Saw-cut joint: 3 mm x t/4.
   - Construction joint: bulkhead with dowels.
   - (Figs 3.33–3.36; p.67–68)
10. **SOG joint layout plan**
    - Joint spacing ≈ 30t (chart Fig 3.29); bay size example 6–10 m x 4.5 m with dowels @ 0.30.
    - Isolation joints at columns (diamond or circle, infill later), walls and equipment bases.
    - Re-entrant corner bars.
    - Strip pouring per ACI 302.1R.
    - (Figs 3.29, 3.31, 3.32, 3.41, 3.42, 3.43)
11. **External pavement / driveway slab**
    - Transverse joints @ 10 m with DB25 x 0.50 @ 0.30 greased and capped dowels.
    - Longitudinal joint with DB25 x 0.50 @ 0.30 bonded tie bars.
    - Mesh RB9 @ 0.20 / @ 0.40.
    - Build-up: 10 cm sand, 15 cm subbase.
    - (Figs 3.37–3.39; p.69–70)
12. **Flat slab typical sheet**
    - Min thickness table (EIT 1008-38): 12.5 cm without drop, 10 cm with drop.
    - Drop panel ≥ L/6 each side of the CL and ≥ t/4 deep.
    - Capital ≥ 45°, ≤ L/4, 4 cm vertical edge.
    - Strip widths L1/4 each side, or drop size.
    - Bar extension diagram: middle strip top 0.22Ln; column strip top 0.30Ln/0.20Ln (no drop) or 0.33Ln/0.20Ln (drop); bottom 50% stop ≤ 0.125L from the CL, 50% continuous + 7.5 cm; 15 cm into the edge support; 24db/30 cm into the drop.
    - Max spacing 2h; As,min table.
    - (Table 3.2, Figs 3.44–3.52, Table 3.3; p.74–82)
13. **Punching shear reinforcement options:** critical perimeters at d/2 and dd/2; shearhead, bent bars, stirrup cage, stud rail. (Figs 3.55–3.58; p.79–82)
14. **Column capital cages**, square and circular: splice bars, 50 mm step, cast column to the underside of the head first. (Figs 4.19, 4.20; p.98)
15. **Slab step details:** H < T with a thickened T-wide zone and Z/L bars lapped Ld; H > T with a 45° haunch and cranked bars + Ld. (p.181)
16. **Sunshade / edge fin:** ≤ 100 x ≤ 300 single-leg vs > 100 x > 300 hairpin; DB10 @ 250; 400 mm anchorage into the slab. (p.181)
17. **Upstand and hanging ribs / curbs:** 70 x 300–500 and 100 x 500–1000, with the bars in 9.3. (p.182)
18. **Basement base slab:** membrane + lean concrete + sand; U-bar edge; waterstop sizes. (p.189)
19. **Slab–wall junctions:** exterior U-loop with Ls lap; interior U; base-slab 90° hook + Ld. (p.190)
20. **General notes block:**
    - cover: 2 cm interior slabs; 4/5 cm exposed; 7.5 cm against earth
    - clear spacing ≥ max(db, 2.5 cm, 1.33 agg)
    - wire-mesh lap ≥ max(S + 2.5 cm, 30 cm)
    - hook table
    - (p.8, 11, 174)

---

## 11. Pages viewed and gaps

**Rendered and viewed (PDF page numbers):**
- Chapter 3: 59–92, every page. Zoom crops of all figures on 60–68, 69, 70, 72, 73, 77, 78, 79, 80, 82, 85, 86, 106, 189, 190, 197, 198. PDF 92 (printed 84) is blank.
- Chapter 4: 104–107 (printed 96–99; flat-slab column heads are on printed 97–98) and 111–116 (printed 103–108).
  - The brief pointed to printed pp.105–106, but those pages are brackets/corbels with no slab content.
  - The flat-slab column-head section "เหล็กเสริมหัวเสาในพื้นไร้คาน" (flat-slab column-head reinforcement) is at printed p.97–98 (PDF 105–106) and is extracted above.
- Appendix: 179–206, all viewed (some as 2 x 2 montages).
  - Slab-relevant sheets: PDF 182, 189, 190, 197, 198, 199.
  - Beam, column, footing or pile only: PDF 183–188, 191–196, 200–205.
  - Blank: PDF 180, 206.
  - PDF 181 is the appendix cover.
- Chapter 1 checks: PDF 15–16 (cover table, text only) and PDF 19 (wire-mesh lap figure).

**Unreadable or uncertain:**
- Appendix text layer is garbled; all appendix values were read from images.
- Fig 3.20 diagonal spacing "@ 0.5 m" (likely 0.05).
- Opening rule 2 wording (middle vs column strips).
- Flat-slab spacing sentence says "not less than 2h" (typo for "not more than").
- Fig 3.14: reference point of 0.50 / 0.25.
- Fig 3.29: values are chart readings.
- Fig 3.34: meaning of "2 cm" and the wrong caption.
- Fig 3.37: mesh direction assignment.
- Fig 3.50: main vs tie bar direction in each band.
- p.181: H > T sketch labelled "H < T", and exact Ld start/end points.
- Duplicate figure number 3.15 (plan and joint detail, both p.57).

---

## D. Cross-check against the ACI Detailing Manual MNL-66(20) (2026-09-29)

Material is in `references/aci_mnl66/` (SLAB-1 … SLAB-208, SOG-100 … SOG-204); findings are in `REVIEW_ACI_MNL66.md`.

| Topic | Our source | ACI | Decision / sheet |
|---|---|---|---|
| Bars at a re-entrant (concave) corner | TATA p.181 H > T bends the lower bottom bars at the haunch top | SLAB-204: lap or cross separate bars at a re-entrant corner; bend continuous bars only at a salient corner | **1126/1, /2:** lower bottom bars go straight to the upper-slab top layer (stair-knee practice, as TATA's own H < T figure); upper bottom bars cross the corner |
| Slab-on-ground dowels | TATA "DB25 × 600 @ 300" | SOG-100 / 101: smooth dowels, greased one side (a deformed bar locks the joint) | Plain RB19 × 400 (t ≤ 150), RB25 × 450 (t ≤ 200) @ 300 (1127/4, /5) |
| Contraction joint mesh | "Continuous or stopped" | SOG-101: stopped | Stopped 50 each side by default (1127/3) |
| Expansion vs isolation joint | One detail for both | Separate | "EXPANSION JOINT"; isolation joint without dowels (1127/5) |
| Cantilever back length | Office rule (≥ Ld, ≥ Sn/3) | SLAB-2.3: tied to the cantilever length | + ≥ Lc (1121/3) |
| Hooks at discontinuous edges | EIT 13.3.3 | §5.7.1: check the hook fits the depth, else an alternative | ≈ 16 db needed; else a 180° hook or U-bars; free edges ≥ 2-DB12 (1121 note 6) |
| Openings | TATA: diagonals DB12 × 700 / 1000; < 600 diagonals only | SLAB-202 / 203: re-space ≤ 300, replace cut bars 300 – 600, diagonals 1200 | 1125 updated |
| Two-way spacing | EIT 13.3.2: ≤ 2h | 318-19 8.7.2.2 adds 450 | ≤ 2h **and 450** (office) |
| Punching / one-way shear size effect, As,min at columns, openings within 4h | EIT = 318-11 | 318-19 λs, 8.6.1.2, 4h | Not adopted (EIT governs); our 10h is conservative |
| Slab schedules, dropped balcony / wet area (SLAB-100, 207), slab at a wall (SLAB-200), corner options, ramps, slab-on-ground corner / T-joint / column-diamond bars, depressions (SOG-105 … 107, 201 … 204) | — | Various | Proposed next work |
