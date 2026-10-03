# Review: Beca standard concrete details (SE-12xx) → R2 slab sheets (2026-09-30)

**Source:** `G:\My Drive\##Workset_Autocad\400 Standard Details\400 Standard Details\10 - CONCRETE\`. The folder holds Beca standard drawings 1003461-SE-1200 to SE-1220, Rev A (2013–14), on A1 sheets.

The slab sheets reviewed:

| Sheet | Content |
|---|---|
| SE-1210 / 1211 | Slab on ground, internal, **hard** wheels: construction joints 1A–1F, sawn joint, joint-filling details, dowel table, expansion-joint metalwork |
| SE-1212 / 1213 | Slab on ground, internal, **general / soft** wheels: CJ 2A–2D (incl. against an existing slab), sawn joints, infill strip, dowel table, EJ |
| SE-1214 / 1215 | Slab on ground, **external**: CJ 3A–3C, sawn joint, isolation joint at a building, infill strip, EJ with sealant detail |
| SE-1218 / 1219 | RC details: wall tee / corner / end junctions, wall-to-slab, **slab–beam junctions**, opening endings, opening trimming, **trimming-bar table by thickness**, embedded plates |

The piling (1200–1202), floor drain (1216), plinth (1217) and stair (1220) sheets were not part of this review.

## 1. How Beca presents a standard detail

| # | Beca convention | What it does for the reader |
|---|---|---|
| B1 | **Panel grid.** The sheet is divided into framed cells, one detail per cell; a band at the cell foot names the catalogue type ("CONSTRUCTION JOINT – TYPE 1A") | Every detail has the same place and weight; details can be copied cell by cell |
| B2 | **"SUGGESTED USE" box** under each detail (red, designer note): when to choose it (movement, traffic, internal / external, thickness) | The reader knows which variant applies before reading the detail |
| B3 | **Joint catalogue marks** (CJx, SJx, EJx, IJx) in the titles, used on the plans | The plan points at a detail by mark, not by description |
| B4 | **FIRST POUR / SECOND POUR header**: a line with arrows, a dot on the joint and a tick down to it | The pour sequence, and so which side is bonded, is read at a glance |
| B5 | **Notes on both sides** of a section, leaders fanned left and right, above and below | The view stays compact; no leader crosses the section |
| B6 | **Enlarged detail reference**: a circle round the joint top + a split bubble (A / sheet), drawn out at 1:2 – 1:5 as "JOINT FILLING DETAIL" / "DETAIL A" | Sealant, backer rod and saw-cut sizes are legible |
| B7 | **Joint sections at 1:10**, detail A at 1:2, 1:5 or 1:20 | A 20 filler or a 6 saw cut shows at its real proportion |
| B8 | **Table by slab thickness** (dowel type × 150 / 175 / 200 / 225) and **trimming bars by wall / slab thickness** | One detail covers a range; the size is read from the table |
| B9 | **Staged notes** (PHASE 1 saw within 8 h; PHASE 2 seal ≥ 28 days) and **EQ \| EQ** dowel dimensions | Timing and dowel centring are explicit |
| B10 | Slab on ground drawn with a dashed polythene membrane on a sand bed, concrete stipple and break lines both ends | The build-up is part of every section |
| B11 | Word dimensions ("STANDARD LAP LENGTH", "200 OR MORE") and variants side by side by thickness | N.T.S. details stay general |
| B12 | "Beam reinforcement not shown for clarity"; "xxx THICK CONCRETE SLAB" note box as a template | Background is suppressed; the slab spec is a template for the plans |

## 2. Adopted in R2 (1121 – 1128)

| Beca | R2 implementation |
|---|---|
| B1 panel grid | **Tried, then rejected by the user (2026-09-30: "our style better").** The slab sheets keep the R2 column / beam layout: views in rows, each titled under itself, notes and tables in the free space |
| B2 suggested use | Tried as a "USE: …" line under every title; withdrawn with the panel grid. The short descriptive note under a title (R2 style) carries the applicability where it matters ("ISOLATION JOINT (IJ): THE SAME WITHOUT DOWELS", "SJD: DOWELLED, WHERE MARKED ON PLAN") |
| B3 joint marks | **SJ / SJD / CJ / EJ / IJ** in the titles (1127) and tagged on the joint-layout plan (1126/3); slab-on-ground note 2 defines them |
| B4 pour header | `pour_header()`: FIRST POUR / SECOND POUR on 1127/2 and 1127/4, EXISTING SLAB / NEW SLAB on 1127/3. A sawn joint (one pour) has none |
| B5 notes both sides | Slab-on-ground sections use `L` and `R` note columns (1126/1, 1127/1–4); the seal details put all notes left and all dimensions right |
| B6 enlarged detail | `detail_ref()`: dashed circle + split bubble. The joint sections point to **1127 A / B / C** |
| B7 scales | **R2 exception:** slab-on-ground sections at a dummy **1:10** (`SG`), seal details at **1:2**, all titled N.T.S. The rest of the set stays at 1:25. All slab-on-ground sections share 1:10, so the slab thickness still reads the same across 1126 – 1127 |
| B8 tables | **TABLE 18 - SLAB-ON-GROUND JOINTS AND DOWELS** (1126): t = 150 / 175 / 200 → sawn-joint spacing, initial saw cut, plain dowel, spacing. **TABLE 17 - MINIMUM TRIMMING BARS AT SLAB OPENINGS** (1124): slab t → opening ≤ 300 / 300–600 / ≥ 600 / diagonals |
| B9 timing, EQ | Saw cut 4 – 12 h, seal ≥ 28 days (A), fill ≥ 60 days (B); dowels dimensioned EQ \| EQ about the joint |
| B10 build-up | `sand_bed()` now draws the 0.2 polyethylene sheet (`S-MEMB`, fine hidden) on the sand bed; slab-on-ground note 4 |

**New content (1127):**
- construction joint at an existing slab: drilled, epoxy-grouted dowels; damaged edge sawn back (Beca CJ 2D / 3C, infill 2A / 3A);
- dowel baskets under SJD dowels;
- Detail A: sealant on a backer rod (foot and pneumatic-tyre traffic);
- Detail B: semi-rigid filler, full depth (hard wheels);
- Detail C: expansion / isolation joint seal.

**Re-numbered:**
- slab on ground is now 1126 (IJ at a ground beam, thickened edge, joint layout, table, notes) and **1127** (joints, seals);
- the slab table and flat-slab notes moved to **1128**;
- references updated: 1121 note 7, 1122/2 USE line.

## 3. Not adopted

| Beca | Why not |
|---|---|
| Red catalogue band and red suggested-use box | Designer-template devices (deleted before issue). R2 is issued to the contractor: EIT title + bubble + USE line instead |
| Centred titles | EIT 2.10 left-aligned title with the split bubble is kept |
| Concrete stipple (AR-CONC) in joint sections | R2 focus rule: hatch means "not the subject". The slab stays clear; only the background (ground beam, existing slab) is hatched |
| Diamond / square plate dowels, Danley armouring, expansion-joint metalwork | Proprietary, and not common in Thai practice. Plain round RB dowels are kept (TATA, ACI 302.1R) |
| "xxx THICK CONCRETE SLAB" template box | A plan-drawing device, not a typical detail |
| Wall junction details (SE-1218) | Belong to the walls set (113x, not started) |

## 4. Values to confirm (proposed, not from a code table)

| Where | Value | Basis |
|---|---|---|
| Table 18 | SJ spacing 4.5 / 5.0 / 6.0 m for t = 150 / 175 / 200 | ≤ 30 t (ACI 302.1R: 24 – 36 t); 175 rounded down |
| Table 18 | Plain dowels RB19 × 400 (t = 150), RB25 × 450 (175, 200) @ 300 | TATA; ACI 302.1R dowel table (¾", 1" dia. for 5 – 8" slabs). t > 200: per design |
| Table 17 | Minimum trimmers: ≤ 125 one mat 1-DB12 / 2-DB12 central; 150 – 200: 1-DB12 / 2-DB16 T & B; 225 – 300: 2-DB12 / 2-DB20 T & B; diagonals 2-DB12 × 1200 | Beca SE-1219 layout (N12 central / EF / N20 EF by thickness), mapped to the R2 bars. **Office values: please confirm** |
| 1127 A–C | Reservoir 6 × 20; backer rod Ø8 (A), Ø25 (C); sealant 20 × 10 in EJ; cap strip ≈ 30 | ACI 302.1R joint-filling guidance, sealant makers' practice |

## 5. Review comments (user, 2026-09-30, `out/STR-ST-1121_Typical_Slab_Details_A3_R2_comment.pdf`)

| Comment | Change |
|---|---|
| 1121/2 "need to show column symbol? how beam supported without column?" | Columns (400, cut, hatched) at the four beam intersections: edge columns flush with the outer beam faces, interior columns centred on the beams. The L/5 corner zone is clipped round the corner column |
| 1122 "DELETE THESE DETAIL" (the three flat-slab strip diagrams) | Sheet deleted. The later sheets moved up one number: flat slab 1122 – 1123, openings 1124, steps / edges 1125, slab on ground 1126 – 1127, tables 1128. The bar extensions are cited as EIT 011008 Fig. 13.3.8 and the 1128 slab table |
| Joint layout "improve column drawing on plan: how column larger than diamond cut area" | The isolation diamond's half-diagonal is now column + 150, so it stays ≈ 100 clear of the column corners. Joint lines stop at the diamond corners, and the bay is drawn 2000 |
| 1126/1 and 1126/2 "hatch should be filled close to bottom edge of slab" | `sand_bed()` fills the sand right up to the soffit (the polyethylene line is drawn inside it) and follows the thickened-edge profile at constant depth. On 1126/1 the sand now runs to the ground-beam face |
| "re-arrange panel layout of typical slab keep it as same as others column and beam typical detail not following beca style our style better" | Panel frames and USE lines removed; the slab sheets are laid out like the column / beam sheets (`place_row()`, `side_blocks()`). The Beca content stays: joint catalogue, pour header, seal details, tables, 1:10 slab-on-ground sections |
| 1126/2 (image) sand under the thickening crossed out: "no need here" | The thickened edge sits on the subgrade: the sand bed and polyethylene sheet run only under the slope and the normal slab, down to a level subgrade (`sand_bed()` keeps the subgrade flat at the bed depth) |
| "polyethelene sheet not consistent offset from slab edge" (1126/2 slope) | `offset_below()` offsets the sheet square to each soffit face (it was a vertical shift, 0.7 × on the 45° slope) |
| "where bed sand hatched?" | The sand stipple was on the 0.13 / 50 % hatch pen and did not show; it now has its own layer `S-HATCH-SAND` (ACI 7, 0.18) and is denser |
| "add a detail if lean concrete used instead of membrane sheet" | New **1126/4 SLAB ON LEAN CONCRETE**: 50 lean concrete (f'c ≥ 15 MPa or 1:3:5, top ± 10) on 50 – 100 compacted sand, slab cast directly on it, dampened before the pour; mesh and joints as 1 and 1127. Slab-on-ground note 4 cites it |
| "also add specification of fill soil in condition fillback is need also compacted condition for subgrade" | New **1128/1 SLAB ON COMPACTED FILL** (fill in ≤ 200 layers on a compacted subgrade, sand bed, sheet, slab) and **TABLE 20 - SUBGRADE, FILL AND BACKFILL UNDER SLABS ON GROUND**. The table covers subgrade, fill, backfill against walls / beams and the sand bed: material, placing, compaction ≥ 95 % modified Proctor (ASTM D1557), OMC ± 2 % and field density tests. Notes to Table 20: no clay / silt fill; fill > 1.0 m or over soft clay goes to the geotechnical report; test methods. Slab-on-ground note 1 and details 1126/1 and 4 cite Table 20. **Values proposed, to confirm:** 95 % modified Proctor, PI ≤ 10, CBR ≥ 10, layer 200 / 150, test frequency |
| 1128 FLAT SLAB NOTES crossed out | Deleted (FLAT_NOTES). The references were re-pointed: 1121 note 7 now ends "FILL UNDER SLABS ON GROUND: 1128", the 1122/2 note no longer cites them, and Table 16 (punching) is cited under the 1123 plan titles. Sheet 1128 is now "SLAB TABLE, FILL UNDER SLABS" |
| "review the document (มยผ มาตรฐานงานทาง) and refine fill / fill back specification" | Table 20 and its notes were rewritten to the DPT road-works standards (below) |

## 6. Table 20 after the DPT road-works standards (มยผ. 2101 – 2225 - 57, 2014)

Source: `G:\My Drive\##Textbook\DPT\มยผ มาตรฐานงานทาง.pdf` (256 pages).

| DPT | Rule | Where it went |
|---|---|---|
| 2112 3.2 | Roots removed ≥ 30 cm below the natural ground, or below the underside of a structure | Table 20, subgrade |
| 2114 5.1.3 / 5.1.4 | Existing ground after stripping: top 15 cm compacted to ≥ 95 % **standard** Proctor; wetted evenly before the first layer | Table 20, subgrade (was "top 300 … ≥ 95 % modified", an office proposal) |
| 2114 5.1.9 | On a slope or cut, the existing ground is loosened ≥ 20 cm for bond | Table 20, subgrade |
| 2114 5.1.5 | Layers ≤ 20 cm **compacted** | Table 20: all fill layers "≤ 200 COMPACTED" (was 200 / 150 loose) |
| 2114 5.1.7 | Near pipes and structures: small compactors, method approved, layers ≤ 20 cm | Table 20, backfill |
| 2101 4.1 | Soil fill: CBR ≥ 4 at 95 % standard, swell ≤ 4 %, no organic matter | Table 20, "FILL: SOIL (ONLY WHERE APPROVED)", ≥ 95 % standard |
| 2101 4.2 | Soil aggregate: max. 50, ≤ 35 % passing No. 200, CBR ≥ 8 at 95 % modified, swell ≤ 3 % | Table 20, "FILL: SOIL AGGREGATE / LATERITE (DEFAULT)", ≥ 95 % modified |
| 2101 4.3 | Sand: non-plastic, max. 9.5, ≤ 20 % passing No. 200, CBR ≥ 10 at 95 % modified | Table 20, "FILL: SAND" and the sand bed (was "≤ 10 % passing", an office value) |
| 2114 5.2 | Ponds / mud: pump out, remove the mud, first layer ≤ 20 cm above the water, 95 % modified | Note 2 |
| 2114 5.3 | Soft ground (CBR < 2): sand fill, ≥ 45 days before final compaction, light plant, no vibratory compaction | Note 3 |
| 2115 4.3 | Organic, soft, unstable soil is excavated and removed | Note 1 |
| 2204 | Field density by sand cone | Note 4 (ASTM D1556 / D6938 dropped) |
| 2114 6 | Level within 1 cm over 3 m; not more than 1.5 cm below and never above the design level | Note 5 |
| 2203, 2205, 2206, 2208, 2211 | CBR / swell, LL, PL, grading, clay lumps | Note 1 (source tests) |

**Not from DPT (office choices, to confirm):**
- *Soil aggregate or sand is the default fill under slabs; soil fill only where approved.* DPT's road default is soil (2114 4.1). Granular fill is chosen under building slabs against shrink-swell and settlement.
- *Test frequencies* (1 per 500 m² per layer, ≥ 3; 1 per 50 m run for backfill): the DPT road standards give none.
- *The fill > 1.0 m / soft clay → geotechnical report / piled slab note.*
- *DPT 2104 selected material* (type A: LL ≤ 40, PI ≤ 20, CBR ≥ 8; type B: CBR ≥ 6) was not used: it is a road layer between embankment and subbase. Soil aggregate (2101 4.2) is used instead; its grading is close to type B.
| "is TOP 150 mean FROM TOP 150 MM. BELOW? … put clearly unit of the no." | Every depth / thickness / size in the fill and slab-on-ground text now carries its unit and says what it is measured on ("THE TOP 150 mm OF THE EXISTING GROUND", "LAYERS ≤ 200 mm THICK AFTER COMPACTION", "0.2 mm POLYETHYLENE SHEET, LAPS 150 mm") |
