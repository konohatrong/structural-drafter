# General Notes — Structural Concrete (office master)

**Basis:**
- **Design:** EIT 011008-21 (วสท. 011008-21), *Standard for Reinforced Concrete Buildings by Strength Design*, 2021, based on ACI 318-11. Digest: [SPEC_RC_DESIGN_EIT-011008-21.md](SPEC_RC_DESIGN_EIT-011008-21.md).
- **Materials and construction:** EIT 011014-19 (วสท. 011014-19), *Specification on Standard of Materials and Construction for Concrete Structures*, 2019.
- Full clause digest: [SPEC_CONCRETE_EIT-011014-19.md](SPEC_CONCRETE_EIT-011014-19.md).
- EIT 011008-21 replaces EIT 1008-38. Where the two EIT standards differ, the stricter value is used; the drawing tags show both, e.g. `[EIT 011008 7.7.1; EIT 011014 2.5.1.5]`.
- **The A3 sheets are the master text.**
  - Current, issued F-A "ISSUED FOR USE" 03/10/2026: `jobs/standard_set/gn_notes.py`, sheets `STR-ST-1001 – 1003-F-A`, 2.0 mm text, numbered
    tables (`standard_drawings/issued/`). A change is a new revision (`standard_drawings/README.md`).
  - First review print A, frozen: `jobs/general_notes/rev_A/`.

  This file explains the choices behind them. "Rev B" below means review print B, the text that was issued; its
  additions are in **§R**.

**How to use:**
1. Fill in the **project parameters** (§0). Every `⟨…⟩` in the notes refers to them.
2. Copy §1–§14 into the project specification or the general-notes sheet. Delete notes that do not apply (e.g. seismic hooks, fire rating, recycled aggregate).
3. For an A3 general-notes sheet (`…-ST-1001`), use the condensed **sheet text** in §15. It is written in the drawing style: upper case, Arial Narrow 2.0 mm, headers 2.8 mm bold.
4. The `[x.x.x]` tags cite EIT 011014-19 clauses. Keep them in the specification; drop them on drawings.
5. Items marked **(office)** are this office's choices. They are stricter than, or additional to, EIT 011014-19; they are not quotations of it.

---

## 0. Project parameters (fill per project)

| Parameter | Typical value | This project |
|---|---|---|
| Design code | EIT 011008-21 (strength design, based on ACI 318-11); seismic DPT 1301/1302-61 | ⟨ ⟩ |
| Concrete strength f'c (cylinder, 28 d) | 24 MPa (≈ 240 ksc; 240 ksc = 23.5 MPa) general; 28–32 MPa for columns and transfer members | ⟨ ⟩ |
| Lean concrete | 1:3:5 by volume, or f'c ≥ 15 MPa, 50 thk. | ⟨ ⟩ |
| Cement | Portland cement Type I, TIS 15 Part 1 | ⟨ ⟩ |
| Exposure class | Interior / exposed to earth or weather / **corrosion risk** (coastal, chloride, wastewater) / sulfate | ⟨ ⟩ |
| Max. w/b | 0.50 (watertight or moderate risk) / 0.45 (severe risk) | ⟨ ⟩ |
| Max. aggregate size | 20 mm (25 mm where spacing allows) | ⟨ ⟩ |
| Deformed bars | SD40, TIS 24 (fy ≥ 390 MPa / 4,000 ksc) | ⟨ ⟩ |
| Round bars | SR24, TIS 20 (fy ≥ 235 MPa / 2,400 ksc): stirrups and ties only | ⟨ ⟩ |
| Welded wire fabric | TIS 737 | ⟨ ⟩ |
| Seismic zone (Ministerial Regulation) | Yes / No → seismic hooks, §5.6 | ⟨ ⟩ |
| Seismic data (Rev B, sheet Table 1) | Ie, category B / C / D, X / Y systems with R, Ω0, Cd (DPT T2.3-1), site class, S<sub>DS</sub> / S<sub>D1</sub>, analysis method, seismic-system members | ⟨ ⟩ |
| Wind (Rev B, Table 1) | Design wind speed and zone (DPT 1311-50); return period for ultimate design | ⟨ ⟩ |
| Design loads (Rev B, Table 1) | Live loads by use and roof (Ministerial Regulation); superimposed dead load (finishes, services, partitions); live-load reduction; special loads | ⟨ ⟩ |
| Foundations (Rev B, section 14) | Soil report; allowable bearing or pile type / size / safe load / tip; pile tests | ⟨ ⟩ |
| Fire rating required | Yes / No → Table 2.24 covers, §7 | ⟨ ⟩ |

---

## 1. General

1.1 **Standards.**
- Materials, workmanship and testing shall comply with EIT 011014-19, and with the Thai Industrial Standards (TIS) cited below in their current editions [1.2.1].
- Where these notes, the drawings and the specification differ, the most stringent requirement governs. Refer any discrepancy to the engineer before proceeding.

1.2 **Site engineer.** A licensed civil engineer (ภาคี or higher) experienced in concrete construction shall be stationed full-time on site during all concrete work [1.2.3].

1.3 **Construction plan.** Before concrete work starts, the contractor shall submit a construction plan [1.2.4]. It shall cover:
- sequence;
- pour breaks and construction joints;
- formwork and shoring;
- concrete supply and placing method;
- curing;
- quality control and testing;
- responsible persons;
- safety.

1.4 **Performance.** Concrete shall achieve the strength, durability and watertightness assumed in the design [1.2.2, 1.3].

1.5 **Dimensions.** Do not scale from the drawings. Dimensions are in millimetres and levels in metres, unless noted.

---

## 2. Concrete materials

2.1 **Cement:** Portland cement to **TIS 15 Part 1**, Type I unless noted [2.1.1].
- Type III only where high early strength is required. Type V, or a proven pozzolan blend, where sulfate exposure is specified [2.1 REC].
- **Mixed cement (TIS 80) shall not be used** for structural concrete. It is for masonry and plaster only [2.1 REC(2)].
- White cement and masonry cement are for non-structural use only.
- Other cements (e.g. TIS 849) only after trial mixes are approved by the engineer.

2.2 **Mixing water** shall be clean and free from oil, acid, alkali, sugar, organic matter and salt. Potable water is acceptable [2.2.1].
- Questionable water is acceptable only if concrete made with it reaches ≥ 90 % of the strength of a clean-water control, and its setting time differs by no more than −1 h / +1.5 h.
- Limits (ppm):

  | Constituent | Limit |
  |---|---|
  | Chloride, RC | ≤ 1,000 |
  | Chloride, prestressed | ≤ 500 |
  | SO₄ | ≤ 3,000 |
  | Alkali (Na₂O + 0.658K₂O) | ≤ 600 |
  | Solids | ≤ 50,000 |

- **Sea water or brackish water shall not be used** [2.2.1, T2.1].

2.3 **Curing water** shall be free of oil, acid and salt in harmful amounts [2.2.2].

2.4 **Aggregates:** clean, hard, durable, well graded, to **TIS 566** [2.3].
- **Sand:** river sand. Sea sand only with the engineer's approval and chloride ≤ 0.02 % (0.03 % as NaCl) by mass of dry sand. Manufactured sand to TIS 566 [2.3 REC].
- **Reactive aggregate:** where alkali–aggregate reaction is suspected, test to ASTM C1260. Then use low-alkali cement (Na₂O eq. ≤ 0.6 %) or a proven pozzolan [2.3 REC(2)].
- **Recycled aggregate:** only with the engineer's approval and within the class limits of 2.3.3.
  - Class 1: no strength limit.
  - Class 2: f'c ≤ 50 MPa, not for chloride or sulfate exposure.
  - Class 3: f'c ≤ 16 MPa, levelling concrete only.

2.5 **Mineral admixtures:**
- **Fly ash:** to TIS 2135, class and dosage by approved trial mix.
- **GGBS and silica fume:** as 2.4.1.
- **Limestone powder** counts as filler, not binder [2.4.1].

2.6 **Chemical admixtures** shall comply with **TIS 733** (Types A–G) and be used only with the engineer's approval [2.4.2].
- The supplier shall declare the main constituents, method of use and maximum dosage.
- Chloride from admixtures shall be ≤ 0.02 % by mass of binder.
- Where more than one admixture is used, or with fly ash (Types D and G may severely delay setting), prove compatibility by trial mix.
- Other admixtures need trial mixes first: waterproofers, corrosion inhibitors, pumping aids, air-entraining and anti-washout agents [2.4.3].

2.7 **Chloride.** The total acid-soluble chloride from all constituents (ASTM C1152) shall not exceed the following, as % by mass of binder [1.3, T1.2]:

| Construction | Limit |
|---|---|
| Prestressed concrete | 0.08 % |
| RC exposed to chloride | 0.20 % |
| Other RC | 0.30 % |
| RC dry or protected | 1.00 % |

---

## 3. Concrete — specification, supply and ready-mixed concrete

3.1 **Strength.** f'c = ⟨ ⟩ MPa, standard cylinder (150 × 300) at 28 days (≈ cube strength − 5 MPa for cubes of 20–50 MPa) [3.2, Fig 3.2].
- **Target mean** = f'c + 1.645 Sn, with Sn from ≥ 30 results.
- **Without data**, the target mean is:
  - f'c + 7 MPa for f'c < 21;
  - f'c + 8.5 MPa for f'c 21–35;
  - f'c + 10 MPa for f'c 35–45 [3.2, T3.1, T3.3].

3.2 **Durability.** Max. w/b [1.3, T1.1]:
- **0.50** for watertight structures (tanks, basements, roof slabs) and for moderate exposure;
- **0.45** for severe exposure (chloride, coastal, wastewater);
- sulfate exposure per MYPH 1332.

  Avoid excessive cement content (heat and shrinkage) [3.5].

3.3 **Max. aggregate size** ≤ the least of [3.6, T3.5]:
- 1/5 of the narrowest member dimension;
- 1/3 of the slab thickness;
- 2/3 of the clear bar spacing.

  Normally **20 mm** (25 mm for general RC; 40 mm for mass or plain concrete). For pumped concrete, ≤ 1/5 of the pipe diameter [6.5 REC].

3.4 **Slump (cm)** at the point of placing, unless noted [3.7, T3.6]:

| Element | Slump (cm) |
|---|---|
| Footings | 5–7.5 |
| Slabs, beams, walls, pavements | 5–10 |
| Columns | 5–12.5 |
| Thin walls, fins | 5–15 |
| Congested reinforcement | 10–15 |

  - Tolerance: ±2.5 cm for 5–15 cm; ±3.5 cm above 15 cm [T5.1].
  - Pumped or flowing concrete: by approved mix.

3.5 **Mix design.** The contractor shall submit the mix design and trial-mix results for approval before use [3.9, 5.1 REC]. The submission shall include:
- mix proportions;
- material sources and test certificates;
- slump;
- 7-day and 28-day strengths.

3.6 **Ready-mixed concrete** shall comply with **TIS 213** [5.1].
- **Plant:** the plant and trucks shall be approved. Weighing equipment is checked daily and calibrated monthly [5.4.2].
- **Batching** is by mass; water and liquid admixtures may be batched by volume. Tolerances [T4.1]:

  | Material | Tolerance |
  |---|---|
  | Water | 1 % |
  | Cement | 1 % (batch ≥ 200 kg) / 2 % |
  | Aggregates | 2 % (batch ≥ 500 kg) / 3 % |
  | Admixtures | 3 % |

- **Delivery ticket** shall show [5.6.5]:
  - plant;
  - ticket and truck numbers;
  - job;
  - concrete class;
  - volume;
  - **batching time and discharge time**;
  - slump;
  - max. aggregate size;
  - admixtures.
- **Time limit** from batching to completion of placing: **≤ 2 h** with a retarding admixture, **≤ 1 h** without. Concrete exceeding these limits or showing initial set shall be rejected [5.3 REC, 4.2.3(5)].
- **Truck loading:** ≤ 80 % of drum volume (central-mixed); 50–65 % (truck-mixed) [5.5 REC].
- **No water shall be added on site.** Slump may be restored only with superplasticizer at the supplier's stated dose, followed by ≥ 30 drum revolutions at mixing speed [5.6.3 REC].
- **Site-mixed concrete:** by mass-batched mixers of approved type [4.1–4.2]. Butter the mixer first, set the mixing time by trial, and do not re-temper concrete that has begun to set.

---

## 4. Testing and acceptance of concrete

4.1 **Sampling** at the point of placing, per concrete class. Take **at least 1 set per day and per pour** [5.6.4(2), 12.3.1]. In addition:
- **1 set per 50 m³** for pours over 50 m³;
- **1 set per 250 m²** for slabs and walls.
- Test slump on every truck sampled and at random [5.6.3 REC].

4.2 **Specimens.** One set = **3 standard cylinders** (or cubes, if specified), tested to **TIS 409** at 28 days [5.6.4(1), 12.3.1].
- Add extra cylinders for 7-day testing and for field-cured specimens where early stripping or loading is intended [12.2.2.3].
- Pozzolan-rich concrete may be accepted at 56 or 91 days only if specified [12.2.2 REC].

4.3 **Acceptance** [5.6.4(3), 12.4.2]:
- **(a)** the average of each set ≥ f'c, and **every cylinder ≥ 0.85 f'c**;
- **(b)** for ≥ 30 results, x̄ ≥ f'c + 1.65 Sn (< 5 % of results below f'c).

4.4 **Non-conformance.** The engineer may order any of the following at the contractor's cost [5.6.4 REC(2), 12.4.4]:
- **cores** to ASTM C42;
- **ultrasonic pulse velocity** to ASTM C597;
- a **load test** per EIT 011008-21 Ch. 18: at ≥ 56 days, test load 0.85(1.4D + 1.7L) held for 24 h, flexural members only. It passes if deflection ≤ lt²/(20,000 h) or recovery ≥ 75 % within 24 h; a retest is allowed after 72 h, needing ≥ 80 % recovery;
- extended curing;
- strengthening;
- removal.

  The mix shall be corrected immediately.

4.5 **Reporting.** Test results shall be reported to the engineer **immediately** and plotted on control charts [12.2.4, 12.3.1(4)].

---

## 5. Reinforcement

5.1 **Material** [2.5.1.1]:
- Deformed bars **SD40 to TIS 24** (DB).
- Round bars **SR24 to TIS 20** (RB): for stirrups, ties, distribution bars and crack-control bars only, never main bars in important members [2.5.1.1 REC].
- Welded wire fabric to **TIS 737**.
- Structural sections and pipes to **TIS 116** / ASTM A36.
- Non-TIS steel may be used only on the basis of test results accepted in the design.

5.2 **Mill certificates** for every delivery. Bars are sampled and tensile-tested to TIS 20 / TIS 24 before use; for deformed bars, the rib geometry is also checked [12.2.3].

5.3 **Storage.** Store bars under cover, off the ground on sleepers, separated by size and grade [2.6.5].

5.4 **Condition.** Bars shall be clean at placing, free from loose or pitting rust, mud, oil, paint and form oil [2.5.1.3, 7.1.1.1].

5.5 **Cutting and bending** shall be done **cold**, by machine, to the bar schedule. **Heating is prohibited.** Bent bars shall not be straightened and re-bent (except starter bars bent at the largest practicable radius with the engineer's approval), and no bend shall be made within 10 db of a weld [2.5.1.2].

5.6 **Standard hooks** (unless detailed otherwise) [2.5.1.2]:

| Bar | Hook |
|---|---|
| Main bars, deformed; round ≥ 15 mm | 90° + **12 db** |
| Main bars, round < 15 mm | 180° + **4 db**, ≥ 65 mm |
| Stirrups and ties, db ≤ 25 | 135° + **6 db** |
| Stirrups and ties, db ≤ 16 | 90° + 6 db permitted (non-seismic) |
| Stirrups and ties, db 19–25 | 90° + 12 db permitted (non-seismic) |
| **Seismic areas** (Ministerial Regulation No. 49, B.E. 2540) | Stirrups and ties **135° + 6 db, ≥ 75 mm** |

5.7 **Bend radius.** The minimum inside **radius** is [T2.19]:
- 2 db for ≤ DB16;
- 3 db for DB20–DB25;
- 4 db for DB28–DB36;
- 5 db for ≥ DB40.

  Welded fabric: 2 × wire diameter (deformed wire ≥ 7 mm), otherwise 1 × wire diameter. Bends tighter than 4 × wire diameter must be ≥ 4 × wire diameter from the nearest weld.

  **(office)** Main-bar bends and hooks use an inside **diameter of 6 db** (R = 3 db; ACI 318 Table 25.3.1), which satisfies the table above.

5.8 **Fixing** [2.5.1.3]:
- Tie with soft annealed wire **≥ 0.9 mm** (office: 1.25 mm) at every intersection in congested zones and at splices, and alternately elsewhere.
- Cages shall be rigid enough not to move during placing.
- Provide erection bars where needed, even if not shown.
- Tack welding of bars is **not** permitted without the engineer's approval (it reduces fatigue strength).

5.9 **Spacers** [2.5.1.3 REC(3)]:
- Precast concrete or mortar spacers, of strength **not less than the concrete**, at ≤ 1.0 m centres each way (office), to give the specified cover.
- Plastic or stainless-steel spacers only with the engineer's written approval.
- No plain-steel chairs against exposed or corrosion-risk faces.
- No timber, brick or stone spacers.

5.10 **Placing tolerances** [2.5.1.3 REC, T2.20]:

| Item | Tolerance |
|---|---|
| Effective depth d, for d ≤ 200 | ±10 |
| Effective depth d, for d > 200 | ±13 |
| Cover, for d ≤ 200 | −10 |
| Cover, for d > 200 | −13 |
| Cover under bottom bars | −6 |

- In no case shall cover be less than **2/3 of the specified cover**.
- Position of bends and bar ends: ±50 (±25 at discontinuous ends; ±13 at ends of corbels and brackets).

5.11 **Other reinforcement.** Fibres or FRP reinforcement only after testing approved by the engineer [2.5.2].

---

## 6. Splices

6.1 **Laps.** Splices are only where shown on the drawings. Any other location or method needs the engineer's approval [EIT 011014 2.5.1.4(1); EIT 011008 12.13.1].
- **Class B** tension laps (1.3 ld). **Class A** (1.0 ld) is allowed only where As provided ≥ 2 × As required **and** ≤ 50 % of the bars are spliced within the lap [EIT 011008 12.14.2].
- **No lap splices for bars larger than DB36** [EIT 011008 12.13.2].
- Lapped bars shall be in contact and wired together (wire ≥ 0.9 mm) [EIT 011014 2.5.1.4(3)].

6.2 **Lap and anchorage lengths (default, unless the drawings show otherwise).** Basis: f'c 240 ksc (23.5 MPa), SD40, uncoated bars, normalweight concrete, clear cover ≥ db and clear spacing ≥ 2 db; values rounded **up** to 50 mm. Computed in `build_gn.py` (`lap_len`, `lap_comp`, `ldh`).

| mm | DB10 | DB12 | DB16 | DB20 | DB25 | DB28 | DB32 |
|---|---|---|---|---|---|---|---|
| Tension lap (class B) | 500 | 600 | 800 | 1000 | 1550 | 1750 | 2000 |
| Tension lap, top bars * | 650 | 800 | 1050 | 1300 | 2000 | 2250 | 2600 |
| Compression lap | 300 | 350 | 450 | 600 | 700 | 800 | 900 |
| Standard hook ldh | 200 | 250 | 350 | 400 | 500 | 550 | 650 |

- **ld** = fy ψt ψe / (2.1 λ √f'c) · db for bars **≤ 20 mm**, and / (1.7 λ √f'c) for **≥ 22 mm**; ld ≥ 300 [EIT 011008 12.2.2].
  - EIT puts DB20 in the small-bar group; ACI 318 puts 20 mm in the large-bar group. That is why the DB20 lap is 1000, not the 1250 used before.
- **\*** Top bars: horizontal bars with more than 300 mm of fresh concrete below the lap, ψt = 1.3 [EIT 011008 12.2.4].
- **Compression lap** = 0.071 fy db ≥ 300; + 1/3 when f'c < 21 MPa [EIT 011008 12.15.1].
- **ldh** = fy / (4.2 λ √f'c) · db ≥ 8 db ≥ 150 [EIT 011008 12.5.2]. Multiply by 0.7 with side cover ≥ 65 mm, or by 0.8 inside ties at ≤ 3 db [12.5.3].

6.3 **Staggering.** Laps of adjacent bars shall be staggered by **≥ 1.0 m**. Splice bars only where necessary [2.5.1.4(6)].
- No more than 50 % of the bars are spliced at one section (office).
- No laps in zones marked "NO LAPS".
- Seismic frames: no laps in plastic-hinge zones or within beam–column joints (office).

6.4 **Welded splices** shall develop **≥ 125 % of the specified yield strength** (1.25 fy) [2.5.1.4(5)].
- Welding procedure and tests are by an approved institution before work starts; submit **3 copies** of the results.
- Weld to AWS D1.4 by qualified welders (office).

6.5 **Mechanical couplers** shall develop **≥ 125 % of fy** in tension. Approved type only, with test certificates [2.5.1.4(8), 12.2.3].

6.6 **Starter bars** left for later splicing shall be protected from damage and rust. Any protective coating shall be fully removed before splicing and concreting [2.5.1.4(4)].

6.7 **Inspection.** Every splice shall be inspected and approved by the engineer before concreting. Unapproved splices may be rejected [2.5.1.4(7)].

---

## 7. Concrete cover

7.1 **Definition.** Cover is measured from the concrete surface to the **outermost bar**, including stirrups, ties and spirals [EIT 011008 7.7; EIT 011014 2.5.1.5].

7.2 **Minimum cover by structural element** (cast in place). This table is on the sheet [EIT 011008 7.7.1].

| Element | Condition | ≤ DB16 | ≥ DB20 |
|---|---|---|---|
| Footings, pile caps | Cast against earth (bottom, sides) | 75 | 75 |
| Footings, caps, slabs on ground | Cast on lean concrete or a membrane (bottom) | 40 | 50 |
| Footings, pile caps | Formed faces in contact with earth | 40 | 50 |
| Ground beams, suspended ground slabs | In contact with earth | 40 | 50 |
| Columns, beams | Interior (to ties / stirrups) | 40 | 40 |
| Columns, beams | Exposed to weather | 40 | 50 |
| Slabs, joists, stairs | Interior | 20 | 30 |
| Slabs, roof decks, canopies | Exposed to weather | 40 | 50 |
| Walls | Interior | 20 | 30 |
| Retaining, basement walls, tanks | Earth or weather face | 40 | 50 |
| Shells, folded plates | Interior | 15 | 20 |

- **Bar size** means the size of the bar the cover is measured to.
- **On lean concrete or a membrane** (office rule): the concrete is not cast against earth, so the "exposed to earth" cover of 7.7.1(ข) applies, 40 / 50. Used by the slab-on-ground details (R2 1126) and the retaining wall (50 on lean concrete).
- **Bundled bars:** cover = equivalent diameter ≤ 50; 75 when cast against earth [7.7.3].
- **Embedded pipes and fittings:** 35 exposed, 20 interior [6.3.10].
- **Precast (plant-controlled):** per EIT 011008 7.7.2.
- **Same values in both standards:** EIT 011014 T2.22 (general) gives the same covers, with α = 1.0 for f'c 21–40 MPa.

7.3 **Recommendation — cover by environment.** Use this where the project is coastal, or exposed to chloride, sewage, sulfate or chemicals. On the sheet it is a recommendation, not a minimum [EIT 011008 7.7.4 requires suitably increased cover, without numbers].

```
c ≥ α · c0 , rounded UP to the next 5 mm                       [EIT 011014 2.5.1.5, T2.21 – T2.24; DPT 1332]
c0 = corrosion risk (T2.23): slabs and walls 50, other members 65 (precast 40 / 50)
α  = 1.2 (f'c < 20 or w/b > 0.65) · 1.0 (20 < f'c ≤ 40) · 0.9 (f'c > 40 or w/b ≤ 0.45); α = 1.0 where c0 ≤ 20
```

| Member | f'c < 20 | 21 – 40 | > 40 |
|---|---|---|---|
| Corrosion risk: slabs, walls | 60 | 50 | 45 |
| Corrosion risk: other members | 80 | 65 | 60 |

- Use denser concrete as well: w/b ≤ 0.45; sulfate classes per EIT 011008 T5.4 / T5.5.
- **Fire:** where regulations require more cover, the larger governs [EIT 011008 7.7.5]. EIT 011014 T2.24: columns and beams ≥ 300 wide: 40; slabs ≥ 115 thick: 20.
- **Service life:** the designer may specify more cover (DPT 1332), never less.

---

## 8. Formwork and shoring

8.1 **Responsibility.** Formwork and shoring are designed, erected and removed under the contractor's responsibility [10.1, 10.3].
- They shall resist the loads of placing and vibration, and keep the concrete within the tolerances of §11.
- For important structures, or where the specification requires it, submit drawings and calculations for approval.
- Excavated faces shall not be used as forms without the engineer's approval.

8.2 **Design loads** [10.2 REC]:
- concrete 2,400 kg/m³ plus reinforcement 150 kg/m³;
- construction live load 60–250 kg/m²;
- horizontal load at the top of the shores ≥ 150 kg/m of edge, or 2 % of the dead load;
- lateral pressure of fresh concrete by Eqs. 10.1–10.3, capped at 15,000 kg/m² (columns) and 10,000 kg/m² (walls), or full hydrostatic 2,400 H for SCC.

8.3 **Stiffness.** Visible form-face deflection ≤ span/240 [10.3.1(2)].
- Forms shall be mortar-tight.
- Chamfer exposed corners 20 × 20 unless noted.
- Provide clean-out openings at the bottom of column and wall forms, and placing windows in tall forms [10.3.1, 10.4].

8.4 **Shores** [10.3.2]:
- Braced diagonally, on firm bearing.
- Adjustable by wedges or jacks.
- Spliced only as permitted: ≤ every other shore under slabs; ≤ every third under beams; one splice per shore; timber splice pieces ≥ 1 m.
- Camber as calculated [10.4(4)].

8.5 **Preparation.** Clean the forms and coat them with a release agent that does not stain or affect the concrete. Keep release agent off reinforcement and construction joints [10.4].

8.6 **Stripping** (general structures, unless specified) [10.5, T10.1, T10.2]:

| Form | Min. strength of field-cured cylinders | Or min. age without tests |
|---|---|---|
| Sides of columns, beams, walls, footings | 5 MPa | 2 days |
| Soffits of slabs and beams, including shores | 14 MPa | 14 days |

- Cantilevers, transfer members, long spans and members carrying construction loads: stripping only by the engineer's instruction (office).
- Strip without shock.
- Do not stockpile materials on newly stripped members.

8.7 **Reshoring** only to a plan approved by the engineer [10.6].
- Reshore immediately after stripping.
- Keep reshores until the specified strength is confirmed.
- No live load on unshored members until their capacity is checked.

---

## 9. Placing and compaction

9.1 **Hold point before every pour.** The engineer shall inspect and approve the following in writing [7.1.1, 2.5.1.3, 2.5.1.4(7)]:
- formwork;
- reinforcement (number, size, position, cover, laps, spacers);
- splices;
- embedded items;
- construction joints.

  If placing is delayed, re-inspect and re-clean the reinforcement [2.5.1.3(5)].

9.2 **Preparation.** Remove debris and standing water. Pre-wet the forms and absorbent surfaces, but leave no ponding. Prevent water from flowing into excavations during placing [7.1.1].

9.3 **Placing** [7.1.2, 5.7]:
- Place continuously, as close as possible to the final position, vertically, without segregation.
- **Free fall ≤ 1.5 m**; use chutes, tremies or pumps for greater heights.
- Place each layer before the one below has set, levelling each layer.
- Rate of rise in columns and walls: about **2–3 m/h**.
- Do not use vibrators to move concrete sideways.
- Stop and remove bleed water before placing the next layer.
- Concrete that has begun to set shall not be placed [4.2.3(5)].

9.4 **Slabs and beams monolithic with walls or columns:** pause **1–2 h** after placing the vertical member to allow settlement, then place the slab or beam. Do the same at changes of section and at cantilevers [7.2.4 REC].

9.5 **Compaction.** Use internal vibrators, inserted vertically at **450–750 mm** centres for **5–15 s** [7.2 REC]:
- Penetrate ~100 mm into the layer below.
- Withdraw slowly.
- Do not vibrate the reinforcement or over-vibrate.
- Keep a standby vibrator on site (office).
- Re-vibrate only while the poker still sinks under its own weight.

  Close plastic-shrinkage or settlement cracks by re-floating before set [7.2.4].

9.6 **Pumping.** Prime the pipeline with mortar of the concrete's mortar fraction. Avoid 90° bends. Anchor pipes rigidly [6.5 REC, 7.1.1 REC].

9.7 **Hot and windy weather** (office, since EIT 011014 gives no limits):
- Keep the concrete temperature at placing ≤ 35 °C.
- Protect fresh surfaces from sun and wind.
- Begin curing as soon as the surface allows.

---

## 10. Curing

10.1 **Timing.** Start curing immediately after finishing [8.1]. Protect the concrete from drying, extreme temperature, rain wash-out, vibration, impact and overload [8.1, 8.6].

10.2 **Wet curing.** Keep the surfaces continuously wet (wet hessian, ponding or spraying) for at least [8.2]:
- **7 days** with Type I cement;
- **3 days** with Type III;
- **longer than 7 days** with fly ash or slag above 10–15 % of the binder: up to **21 days** for high replacement (Table 8.1).

  Formed faces left in their forms count as cured, but keep the forms wet (office).

10.3 **Curing compounds** only where wet curing is impracticable and only with the engineer's approval [8.5]:
- Apply in **two or more coats** as soon as the surface water has gone.
- Keep them off reinforcement and construction joints.

10.4 **Controlled or accelerated curing** (mass concrete, precast, steam) only to an approved procedure [8.3, 8.4, 8.6].
- For mass concrete, limit the internal–surface temperature difference.
- Limit the curing temperature (risk of delayed ettringite formation, DEF).

---

## 11. Construction tolerances (formed concrete) [10.7]

| Item | Tolerance (mm) |
|---|---|
| Plumb — columns, piers, walls | 6 per 3 m; 25 max. over full height |
| Plumb — exposed corner columns and conspicuous lines | 6 per 3 m; 12 max. |
| Level — slab and beam soffits (before removing shores) | 6 per 3 m; 10 per bay or 6 m; 20 max. |
| Level — lintels, sills, parapets, exposed lines | 6 per bay or 6 m; 12 max. |
| Building lines; column and wall position | 12 per bay or 6 m; 25 max. |
| Openings in slabs and walls — size and position | 6 |
| Cross-section of columns and beams; thickness of slabs and walls | −5 / +10 |
| Footings — plan dimensions | −12 / +50 |
| Footings — eccentricity | ≤ 2 % of footing width in that direction, ≤ 50 |
| Footings — thickness | −5 % / +100 |
| Stairs — riser / tread within one flight | 4 / 6 |
| Stairs — riser / tread between adjacent steps | 2 / 4 |

---

## 12. Joints

12.1 **Construction joints** only where shown or approved [9, 9.1]:
- **Location:** at minimum shear, normal to the member axis or compression.
- **Slabs and beams:** near mid-span (office: within the middle third); in a beam, **> 2 × joist width** from any joist framing in, with 45° shear bars across the joint [9.1.4].
- **Columns and walls:** just below the soffit of the floor system and at the top of the footing or slab. Haunches, capitals, drop panels and cantilevers are cast with the floor [9.1.3].
- **Dowels** across a high-shear joint: ≥ **20 db** each side, hooked if plain bars [9.1 REC].

12.2 **Joint preparation** [9.1.1–9.1.2]:
- Remove laitance and loose material by green-cutting (air–water jet), wire brush or sandblast, to expose the coarse aggregate. Office: roughen to ~5 mm amplitude.
- Clean, then keep the surface saturated surface-dry.
- Just before placing, apply grout or mortar with a lower w/c than the concrete (or an approved bonding agent).
- Compact thoroughly and re-vibrate at the right time.
- Stop-ends must be rigid; expanded mesh (5 mm) may be left in place [9.1.2 REC].

12.3 **Column concrete stronger than floor concrete.** Where the column f'c exceeds **1.4 ×** the floor f'c, place column-grade concrete in the floor at each column, over **4 × the column area**, monolithically, before the floor concrete sets. Alternatively, design the column to the effective strength (0.75 f'c,col + 0.35 f'c,floor, for columns braced on four sides) [9.1.3 REC].

12.4 **Expansion joints** separate the structure completely (reinforcement discontinuous unless detailed) and are filled with a preformed joint filler. Provide water stops and sealant where watertightness is needed [9.2].

12.5 **Crack-control (contraction) joints** are formed or sawn at the locations shown [9.3]:
- Groove depth 0.1–0.15 × thickness each face, leaving ≈ 0.8 × thickness.
- Water stop in water-retaining structures.

12.6 **Placing against old concrete from below** (underpinning, infills) follows the direct, filling or injection method of Fig. 9.1, with an expansive admixture [9.1.1 REC].

---

## 13. Surface finishing and repairs

13.1 **Unformed surfaces** [11.2]:
- Screed, then wait until the bleed water has gone before trowelling.
- Do not over-trowel, and do not finish in rain.
- **Roof slabs, canopies and roof decks shall not be steel-trowelled smooth** unless specified.

13.2 **Formed and exposed surfaces** [11.3]:
- Remove fins.
- Honeycomb, cracks and defects are repaired only with the engineer's approval of the method:
  - chip back to sound concrete;
  - wet;
  - repair with an approved mortar, concrete or proprietary repair material.
- Bug holes may be rubbed with 1 cement : 2.5 fine sand.
- Structural defects need the engineer's instructions.

13.3 **Abrasion-resistant floors:** low w/b, thorough compaction, prolonged curing [11.4].

13.4 **Special finishes** shall not reduce the section or the capacity [11.5].

---

## 14. Quality control and records

14.1 **Materials** [12.2.2.1, 2.6]:
- Test the materials before mix design.
- Test aggregate grading and moisture ≥ 2 × per day at the start of the work.
- Store cement dry and off the floor (≤ 10 bags high, 30 cm from walls), first-in first-out.
- Do not use lumpy cement.
- Re-test cement, fly ash and admixtures stored for long periods (> 1 year for admixtures).

14.2 **Test methods.** Use TIS where available, otherwise ASTM, BS or JIS [12.2.1].

14.3 **Inspection after completion.** Check the members for dimensions, position and defects. Repair defects as the engineer instructs before the structure is used [12.5.1].

14.4 **Records** [13.1]. Keep daily handwritten records, completed at the end of each period and retained **≥ 2 years after completion**. They shall cover:
- materials received and used;
- mix proportions;
- batching;
- delivery tickets;
- placing (date, time, location on drawing, volume, weather);
- test specimens and results;
- curing;
- formwork erection and stripping;
- shoring and reshoring;
- reinforcement approvals;
- deviations and remedies;
- progress photographs.

---

## 15. Sheet text (for the general-notes sheet `…-ST-1001`)

> **The full A3 sheets are generated:** the issued sheets (F-A) from `jobs/standard_set/gn_notes.py`, 1001 – 1003 at 2.0 mm text; review print A (frozen) from `jobs/general_notes/build_gn.py`, one sheet at 1.25 mm. Drawing rules are in `GENERAL_NOTES_DRAWING_INSTRUCTION.md` (§0 for the current method). The condensed text below is only for adding a short concrete-notes block to another sheet.

This is the condensed upper-case version for an A3 sheet at 2.0 mm (≈ 2 columns at 100 mm width).
- Paste each block into the sheet generator's `notes([...])` lists, using `hdr()` for headers.
- Replace the `⟨ ⟩` parameters.
- Delete non-applicable lines.

```
C1. CONCRETE (EIT 011014-19)
C1.1  MATERIALS AND WORKMANSHIP TO EIT 011014-19 AND CURRENT TIS. A LICENSED ENGINEER SHALL BE ON SITE FULL-TIME DURING CONCRETE WORK.
C1.2  STRUCTURAL CONCRETE f'c = ⟨24⟩ MPa (⟨240⟩ ksc) STANDARD CYLINDER AT 28 DAYS, READY-MIXED TO TIS 213. PORTLAND CEMENT TYPE I TO TIS 15 PART 1. MIXED CEMENT (TIS 80) NOT PERMITTED.
C1.3  MAX. w/b ⟨0.50⟩ (0.45 WHERE EXPOSED TO CHLORIDE / SEVERE EXPOSURE). MAX. AGGREGATE ⟨20⟩ mm TO TIS 566. ADMIXTURES TO TIS 733 WITH ENGINEER'S APPROVAL. TOTAL ACID-SOLUBLE Cl⁻ ≤ 0.30 % OF BINDER (0.20 % IF EXPOSED TO CHLORIDE).
C1.4  SLUMP AT PLACING (cm): FOOTINGS 5-7.5, SLABS/BEAMS/WALLS 5-10, COLUMNS 5-12.5, CONGESTED 10-15; TOLERANCE ±2.5. NO WATER SHALL BE ADDED ON SITE.
C1.5  PLACE WITHIN 2 h OF BATCHING (1 h WITHOUT RETARDER). FREE FALL ≤ 1.5 m. COMPACT WITH INTERNAL VIBRATORS AT 450-750 c/c, 5-15 s. PAUSE 1-2 h BETWEEN COLUMNS/WALLS AND THE FLOOR ABOVE.
C1.6  TESTS: 1 SET OF 3 CYLINDERS PER DAY, PER POUR, PER 50 m³ AND PER 250 m² OF SLAB/WALL, TESTED TO TIS 409. ACCEPT: SET MEAN ≥ f'c AND EACH CYLINDER ≥ 0.85 f'c. NON-CONFORMANCE: CORES (ASTM C42) / LOAD TEST AT CONTRACTOR'S COST.
C1.7  WET CURE ≥ 7 DAYS (TYPE I), ≥ 3 DAYS (TYPE III), LONGER WITH FLY ASH. CURING COMPOUND ONLY WITH ENGINEER'S APPROVAL, 2 COATS.
C1.8  STRIP SIDE FORMS AT ≥ 5 MPa OR 2 DAYS; SOFFITS AND SHORES AT ≥ 14 MPa OR 14 DAYS (FIELD-CURED CYLINDERS). RESHORING ONLY TO AN APPROVED PLAN. FORM DEFLECTION ≤ SPAN/240. 20x20 CHAMFER TO EXPOSED CORNERS.
C1.9  CONSTRUCTION JOINTS ONLY WHERE SHOWN OR APPROVED: AT MID-SPAN OF SLABS AND BEAMS, ROUGHENED, CLEAN AND SATURATED SURFACE-DRY. WHERE COLUMN f'c > 1.4 x FLOOR f'c, POUR COLUMN CONCRETE IN THE FLOOR OVER 4 x THE COLUMN AREA.
C1.10 TOLERANCES TO EIT 011014-19 CL. 10.7: SECTIONS -5/+10 mm; PLUMB 6 mm PER 3 m, 25 mm MAX.; LEVEL OF SOFFITS 20 mm MAX.

C2. REINFORCEMENT
C2.1  DEFORMED BARS SD40 TO TIS 24 (DB); ROUND BARS SR24 TO TIS 20 (RB) FOR STIRRUPS AND TIES ONLY; WELDED FABRIC TO TIS 737. MILL CERTIFICATES AND TENSILE TESTS PER DELIVERY.
C2.2  CUT AND BEND COLD - NO HEATING, NO RE-BENDING. MIN. INSIDE BEND DIAMETER 6 db. HOOKS: MAIN BARS 90° + 12 db; STIRRUPS AND TIES 135° + 6 db (≥ 75 mm IN SEISMIC AREAS).
C2.3  CLEAR COVER TO OUTERMOST BAR BY ELEMENT (EIT 011008-21 CL. 7.7.1): FOOTINGS CAST AGAINST EARTH 75; FACES IN CONTACT WITH EARTH OR WEATHER 40 (≤ DB16) / 50 (≥ DB20); INTERIOR BEAMS AND COLUMNS 40; INTERIOR SLABS, WALLS, STAIRS 20 (≤ DB16) / 30 (≥ DB20). RECOMMENDED FOR CORROSIVE EXPOSURE: SLABS/WALLS 50, OTHER MEMBERS 65 (EIT 011014-19 CL. 2.5.1.5). U.N.O.
C2.4  CONCRETE SPACERS OF STRENGTH NOT LESS THAN THE CONCRETE AT ≤ 1.0 m EACH WAY; PLASTIC OR STAINLESS ONLY WITH APPROVAL. TIE WITH ≥ 0.9 mm (1.25 mm) ANNEALED WIRE. NO TACK WELDING.
C2.5  PLACING TOLERANCE: d ±10 (d ≤ 200) / ±13; COVER -10 / -13, NEVER LESS THAN 2/3 OF SPECIFIED; BOTTOM COVER -6.
C2.6  LAPS ONLY WHERE SHOWN OR APPROVED, STAGGERED ≥ 1.0 m, ≤ 50 % AT ONE SECTION U.N.O. (COLUMN / WALL VERTICALS PER THEIR DETAILS). TENSION LAPS (f'c 24, SD40): DB10 500, DB12 600, DB16 800, DB20 1000, DB25 1550 (TOP BARS x 1.3); NO LAPS FOR BARS > DB36. WELDED SPLICES AND COUPLERS ≥ 1.25 fy, TESTED BY AN APPROVED LABORATORY (3 COPIES OF RESULTS).
C2.7  HOLD POINT: ENGINEER TO INSPECT AND APPROVE FORMWORK, REINFORCEMENT, SPLICES AND EMBEDDED ITEMS BEFORE EACH POUR.
```

---

## R. Rev B additions (2026-09-29): sources and reasons

These were made after the user's requests and the ACI Detailing Manual MNL-66(20) review (`REVIEW_ACI_MNL66.md`). The wording is on the sheets (`gn_notes.py`).

| Item on the sheet | Content | Why / source |
|---|---|---|
| Table 1, project design data | Location; seismic zone, Ie, category, X / Y systems with R / Ω0 / Cd, site class, S<sub>DS</sub> / S<sub>D1</sub>, analysis, seismic-system members; wind speed, zone, return period; live loads, superimposed dead load, partitions, live-load reduction, special loads | User request (seismic, wind); ACI MNL-66 §4.4.2 (design loads on the notes sheet), and §4.4.7 (the seismic-system list drives the inspection notes). DPT 1301/1302-61 (seismic), DPT 1311-50 (wind) |
| Table 6 rows | Straight tension ld; compression ldc = 0.24 fy db / √f'c ≥ 0.043 fy db ≥ 200 | EIT 011008 12.2.2, 12.3.2. Footing, pile-cap and wall dowels depend on ldc; a hook does not count in compression. ACI MNL-66 §4.4.5.2, §5.1.2 |
| Table 6 note | Values apply conservatively to higher concrete grades; where the cover / spacing conditions are not met, ld per EIT 12.2.3 | The table is computed for f'c 240 ksc and the simplified 12.2.2 conditions |
| Note 5.6 | Footing and ground-beam bottom bars on precast blocks; top mats on chairs designed by the contractor, engineer-designed for mats ≥ 1.2 m; bar dimensions out-to-out including hooks | ACI MNL-66 §4.4.5.3, §5.3.3 (mat supports), §4.4.5.5 (bar dimensioning) |
| Note 6.1 and the lap detail | Stagger and "≤ 50 % at one section" are U.N.O.; column / wall verticals may lap at one level | ACI MNL-66 §5.2.1 warns against a blanket "stagger all laps"; our column details (1101) lap all bars at one level |
| Note 8.5 | Anchor bolts with templates; non-shrink grout 25 – 50 under base plates, strength ≥ the supporting concrete | ACI MNL-66 FND-101 – 104; needed before the pedestal / anchor-bolt details (114x) |
| Note 11.5 | Joint-layout submittal where joints are not shown | ACI MNL-66 §5.1.4, WALL-200 |
| Section 14, foundations and piles | Soil report and bearing / pile data; pile tests; position tolerances; pile heads cut to sound concrete, embedment and anchorage per the details, cap bars above the pile heads; lean concrete; dewatering by the contractor; fill compaction | ACI MNL-66 §4.4 and §4.11 (foundation notes before the foundation sheets). Placeholders; values per project |
| Table 5 note | Intermediate and special frames: deformed hoops and crossties, DB10 minimum | User decision D3 (ACI allows plain bars only for spirals) |
| Abbreviations | Three column lists: general, rebar position and call-outs, symbols in the details | User request. Sn = slab clear short span only; "ss" = standard deviation |

**Not adopted:** ACI 318-19 values that EIT 011008 (ACI 318-11 based) does not require, unless stated as an office rule (e.g. two-way slab spacing ≤ 450 on the slab sheets).

---

## 16. Checklist — before issuing drawings with these notes

- [ ] §0 parameters filled; f'c stated as a **cylinder** strength, with the ksc equivalent in brackets.
- [ ] The exposure class matches the cover table used on the sections (corrosion risk → 50 / 65).
- [ ] Every section states its clear cover, or refers to the cover table (C2.3).
- [ ] Hook, bend and lap lengths on the bar schedule match §5–§6.
- [ ] Construction joints on the drawings are at locations consistent with §12.1.
- [ ] Seismic hook requirements included, or deleted, per the project location.
- [ ] Non-applicable notes deleted (recycled aggregate, fire rating, underwater concrete).
- [ ] Rev B: Table 1 filled (seismic, wind, loads); section 14 filled (soil report, bearing or pile data, tests); detail-sheet references to "1002 TABLE 6" still valid.
