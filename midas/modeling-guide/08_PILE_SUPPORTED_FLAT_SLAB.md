# 08 · Pile-supported flat slab with drop panels: staged build (and zone by zone)

How a ground floor carried by piles is built in a live GEN NX model:
- a flat slab with a drop panel over every pile and over every column that has no ground beam;
- ground beams;
- rigid zones at the pile heads;
- a gutter strip foundation.

Two methods were used on BANWA 2 (07 – 08/10/2026, 70 × 62 m ground floor). They are written generically, with BANWA 2
values as the worked example.
- **The staged build (current, §2A)** writes the whole floor one *kind of object* at a time:
  1. beams;
  2. outlines;
  3. piles;
  4. slab;
  5. drops and strip.

  The drop and strip outlines are pre-split finely so the slab refines around them. Used for the final model (layout r9,
  249 piles, r34 – r38).
- **The zone method (§2 – §3)** writes the floor one *area* at a time, each zone complete. Used for the first builds
  (layout r7, 458 piles, r27 – r33). It is kept for very large floors, or when only part of a floor is modelled.

Every write is verified the same way (§7).

The auto-mesh request format (voids, interior nodes and lines) is in [06 §4.1](06_SLAB_AUTOMESH.md). This chapter
is the method around it.

## 1. The system and the decisions to take first

Each line is an engineering decision; record the project's answers in the decision log (`DECISION_LOG_TEMPLATE.md`,
section "Pile-supported ground slab").

| Item | BANWA 2 decision (engineer) |
|---|---|
| Slab | Flat slab **FS200** (0.20), plates on the slab mid-plane at 0.00, no offset |
| Drop panel | **1.2 × 1.2, DP350** (0.35 = 0.20 slab + 0.15 below), plates on the same mid-plane (no offset) |
| Pile | Modelled as a **stub column** from 0.00 to −1.50 (the pier length, as the column pedestals), **pinned** at the foot (`CONS` `1110000`). Layout r7: 350 × 350. Layout r9: **SPUN 300 as a solid round dia 300**, allowable 35 tonf |
| Pile layout | r7: tributary area ≤ 8.41 m² per pile. **r9 (client loads):** each pile's load ≤ 95 % of 35 tonf on service DL + LL + SDL, from its Voronoi cell split by the load areas (LL 3.0 / 1.5 t/m²); pile panels near square (sides within 1 : 1.5); 244 drop piles + 5 under the gutter |
| Rigid zone | **8 nodes** on the pile face at the slab level (3 a side: corners and mid-sides; ±0.15 for dia 300), `RIGD` master = pile head, `DOF 111111`, written after the plates have taken the nodes |
| Column with no ground beam | A drop panel over it as over a pile: 1.2 × 1.2 DP350, 8 nodes on the **column face** (500 pedestal), master = the column node at 0.00 (engineer, 07/10: added after three zones were written, see §8) |
| Ground beams | GB 400 × 900, top at 0.00: **CT section offset** like the floor beams, nodes at 0.00; column to column; members meet with rigid joints |
| Supports | All column supports pinned (were fixed) |
| Material | C280 for slab, drops, beams and piles |
| Mesh | Slab **0.40 m**; drops and gutter strip **0.20 m**, their outlines pre-split at 0.20 (staged build, §2A). The zone builds used 0.40 everywhere (§6.1) |
| Gutter | A U-gutter (walls 200, clear 1 200 × 800, base 1 600 × 500) on 4 piles, modelled at ground level as a **2 000 × 500 strip** of plates (GS500), §5.4 |
| Openings | Lift pit: no slab, an opening bounded by its beams (assumed, open with the engineer) |

## 2A. The staged build (current method)

The engineer's improvement (08/10/2026): *"make outline dummy for drop panel; mesh outline dummy making refine meshed size
to drop panel - this will force meshed slab refine around drop panel; fill drop with finest mesh size (we can test first);
keep column rigid zone same methodology"*. Then: *"start build ground beam first"*, and stage by stage after that.

**Stages:** each stage is one script, one dry run, one model revision and one snapshot. The next stage checks the live
model against that snapshot before it writes.

| Stage | What it writes | BANWA 2 |
|---|---|---|
| 1. Ground beams (`ground_beams_r9.py`) | Every ground beam split at each column, pier and beam end on it; new piers (pedestal + pinned support); existing transfer-beam elements split where a ground beam lands between their nodes (the second piece copies the element and joins its member and groups); orphan nodes deleted | r34: 90 GB pieces, 499.00 m; 2 piers; TB split × 2 |
| 2. Outlines (`outlines_r9.py`) | Dummy line elements, **pre-split at the refined size**: each drop square (6 × 0.20 a side); the gutter strip edges; and the beams under the strip ends, split at 0.20 over the strip width. Temporary sections and groups | r35: 5 856 + 130 pieces; 2 GB elements split |
| 3. Piles (`piles_r9.py`) | Pile stubs (solid round dia 300, 0.00 to −1.50, pinned) and the **8 rigid-zone nodes** on each pile face (±0.15) at 0.00; no links yet | r36: 249 stubs, 2 490 nodes |
| 4. Slab (`slab_r9.py`) | FS200 at 0.40, **region by region between the beams**. Each region's loop is its beam / TB / strip-edge pieces; its drop outlines are inner loops left void. Openings get no region; a wall top is closed by temporary lines between the wall's nodes | r37: 10 regions, 67 098 plates, 3 938.46 m² |
| 5. Drops and strip (`drops_strip_r9.py`) | DP350 at 0.20 on each region's drop outlines through the pile heads + 8 nodes (one call per region); the strip GS500 at 0.20 through its piles' nodes; **rigid links** (head → 8 nodes); the outlines deleted once plates lie on both sides | r38: 8 784 drop + 773 strip plates, 249 links; 76 655 ground plates |

**Why stage by stage instead of zone by zone:**
- No seams: every region is closed by beams, so no temporary seam lines or ownership rules are needed.
- The outline pre-split controls the mesh. A piece no longer than the mesh size is never re-split (§6.1). So:
  - the slab refines around each drop and the strip by itself;
  - the drops and the strip fill at the fine size;
  - every interface shares its nodes.
- Each stage is small to check and to undo: reopen the previous revision.

**The refined size, by test** (a throwaway copy, slab 0.40):

| Outline / fill size | Drop plates under 45° / over 135° | Slab ring under 45° | Plates (12 × 12 m bay, 9 drops) |
|---|---|---|---|
| 0.40 (the zone builds) | 11 % / 17 % | 5.5 % | 777 + 310 |
| 0.30 | 17 % / 33 % | 0.7 % | 1 168 + 216 |
| **0.20 (chosen)** | **0 % / 0 %** | 1.3 % | 2 024 + 324 |
| 0.15 | 0 % / 0 % (exact 8 × 8 grid) | 0.6 % | 3 114 + 576 |

For the gutter strip (2.0 m wide on 5 piles), 0.20 gave 0.3 % under 45°. At 0.25 more plates are stretched; at 0.10
there are 3.4 × the plates. With piles about 3 m apart the refinement does not relax between drops, so the whole piled
area becomes fine.

**Rules learned in the staged build:**
- **A pre-split piece must not be longer than the mesh size around it.** Divide with `ceil(L / size)`, never `round`:
  13 m at 0.40 gave 0.406 m pieces, which the slab mesh split again, and the strip then failed to mesh.
- **A beam meets a support or another beam only at a node.** Split every beam at each column, pier and beam end on it
  before writing. An existing element (the engineer's transfer beam) is split explicitly, and its member list and
  groups are updated.
- **Re-read the node table after every mesh call** before checking plates: the mesh creates nodes. A stale table
  stopped the first r38 run; the unsaved revision was set aside, the previous one reopened, and the stage re-run.
- **Compare coordinates at the precision they were written** (4 decimals). Half-millimetre positions (43.7895) round
  differently at 3 decimals.
- **Probe on a throwaway copy without losing the live state.** `SAVEAS` the open model to a probe file (it holds the
  exact live state), test there, then `OPEN` the saved revision and compare it with its snapshot.

## 2. Zoning (the zone method)

A whole ground floor is too big to write and check in one go, so it is divided into zones. Each zone is written as
**one model revision**.

- **Zones** follow beams or rows of columns or piles, and are written in a fixed order (BANWA 2 zones r3, from the
  engineer's sketches: Z1 … Z7 with Z3 the gutter strip and Z8 the tank roof last). Start with a small pilot to prove
  the method (§8).
- **Ownership.** An item shared by two zones belongs to the **first zone in the order**: a pile on the boundary
  row, the drop over it, a beam on the shared edge. The later zone meets it.
- **Zone edges in the model** are on the beam axes, not on the column faces. The 0.225 m from the axis to the column
  face is carried by the beam, with no plates.
- **Each edge is one of:**
  - **a ground beam**: the beam pieces are the boundary;
  - **an open edge**: a temporary **seam** line (section `TEMP_SEAM`, 0.05 × 0.05), kept after the zone is meshed.
    The next zone meshes against the seam's nodes, so the two meshes share nodes. The seam pieces are deleted by ID
    once plates lie on both sides of them;
  - **an existing seam or existing beam pieces** left by a meshed zone: joined as they are;
  - **an existing wall top** (the tank wall): temporary lines between the wall's existing top nodes, deleted after
    the mesh.
- **A drop on an open edge** is owned by the zone that owns its pile or column, and that zone meshes it whole:
  - the slab loop goes round the drop's inner half;
  - the outer half is seam;
  - the next zone meets that outer half.

## 3. The flow of one zone

Script: `<project>\Drafter\scripts\ground_model.py` (project folder, rule M9); `build <zone>` is the dry run,
`write <zone> "<key>"` the write. Inputs: the pile layout (`ground/layout_r7.json`), the zones
(`ground/zones_r3.json`) and a snapshot of the live model.

**Dry run (`build`), offline:**

1. **Plan the zone in 2D:**
   - the zone rectangle on the beam axes;
   - the piles and columns it owns, each with its drop square and 8 nodes;
   - the beams inside it or along its edges;
   - each edge split into beam / seam / drop detour / wall stretches.

   Beams are split where another beam lands on them (T-junctions); beams that are not on an edge are **interior
   lines**. Every beam end touching an edge is a breakpoint there, so the next zone finds a node.
2. **Payload:**
   - new nodes and elements, with IDs above the model's;
   - existing nodes reused when the coordinates match (column tops, wall tops, the existing 0.40 beam nodes);
   - existing beam and seam pieces collected as boundary targets.
3. **Pre-write checks** against the snapshot (§7.1).
4. **Review sheet:** what will be written, with counts, the expected areas and the open items. The engineer says Go.

**Write (`write`), live, after Go:**

1. Connect. If the zone starts from an older file, `POST /doc/OPEN` that file.
2. **The live model must equal the snapshot** (NODE, ELEM, CONS, SECT, THIK): the model is the state that was
   reviewed.
3. **Pre-checks again**, on the live tables.
4. `POST /doc/SAVEAS <project>\BANWA2_ground_slab_<zone>_rXX.mgbx`. Abort if that file exists. The earlier file
   keeps the state before the write.
5. **Backup** of the tables the write touches → `backup\midas_backup_before_ground_<zone>_<stamp>.json`.
6. `PUT` the sections and thicknesses (only those not yet in the model), the nodes, the elements and the supports:
   - nodes: pile feet and heads, the 8 nodes per drop, drop corners;
   - elements: pile stubs, new beams, seams, drop outlines, wall-top lines;
   - supports: pile feet pinned, and every column support set to pinned on the first zone.
7. **Slab:**
   - `AUTOMESH` FS200 at the zone's mesh size. Targets: new beams + seams + drop outlines (the inner halves on
     edges) + existing seam / beam pieces + wall-top lines.
   - Interior lines: the interior beams (`"OPTION":"User"`). No interior nodes (the reserved nodes stay inside the
     voids).
   - An opening (lift pit): delete the plates whose centroid lies inside it, then the mesh nodes left inside it,
     by ID.
8. **Slab checks** (§7.2). The most important: **no existing boundary piece was split** (§6.1).
9. **Drops:**
   - re-read `ELEM` and find each drop's outline pieces geometrically: they were split by the slab mesh, and the
     first piece keeps the old ID;
   - **one** `AUTOMESH` DP350 on all the outline pieces, with every drop's 8 nodes + master as `"User"` interior
     nodes (BANWA 2 Z7: 1 656 lines, 1 242 nodes, 138 drops in one call);
   - check each drop: plates inside it, area 1.44 m², all 9 nodes used. If the single call fails, delete its plates
     and mesh one drop per call.
10. **Rigid links:** `PUT /db/RIGD` per drop (master → 8 nodes), then read back and compare.
11. **Clean-up, all by ID** (never a blind DELETE):
    - delete the drop outlines and the wall-top lines;
    - delete each existing seam piece whose node pair is now an edge of **two** plates.

    If a seam piece is not between two plates, stop: the meshes do not connect.
12. **Groups:** `BANWA2_GF_PILE`, `…_GB_400x900`, `…_SLAB_FS200`, `…_DROP_DP350`, `…_SEAM_TEMP`,
    `…_PILE_HEAD_NODES`, `…_GUTTER_STRIP_GS500`. A later zone merges its members into the existing groups (read,
    union, PUT).
13. **Read-back** (§7.3), plan plot of the zone mesh from the read-back data, plan + iso capture.
14. If every check passes: `POST /doc/SAVE`, then a read-only **snapshot `snapshot_rXX`** of the saved model. It is
    the reviewed state the next zone is checked against (step 2).
    Any failed check: stop, **leave the revision unsaved**, write the log. The earlier revisions on disk are
    untouched.

Zones can run **in a chain** (`for z in zones: write(z)`) in the background, with a monitor on the log. The chain
stops at the first failed check (BANWA 2: Z1 … Z7 written as r27 … r32 in one evening).

## 4. Rigid zones

- Pile: 8 nodes at ±0.175 m round the pile node (the 350 pile face), on the slab plane at 0.00. Column: 8 nodes at
  ±0.25 m (the 500 pedestal face), master the existing column node.
- They are **interior nodes of the drop mesh only**: the slab mesh never takes them (checked), the drop mesh must
  take all 9 (checked).
- The drop mesh makes a 4-quad patch inside the 8 nodes; those plates lie in the rigid zone, which is accepted.
- `PUT /db/RIGD {"Assign":{"<master>":{"ITEMS":[{"ID":1,"GROUP_NAME":"","DOF":111111,"S_NODE":[…8…]}]}}}`; the
  table is keyed by the master node. Read it back; existing entries must stay unchanged.

## 5. Special cases met on BANWA 2

### 5.1 Beam partly in the zone
A layout beam along a zone edge that runs past the zone is split at the zone corner. The piece beside the slab joins
the loop; the piece outside is created as a plain beam, beside no slab (`gb_out`, exempt from the "beam on a plate
edge" check). A beam already in the model (pieces on its line) is not created again: its existing pieces join the
loop.

### 5.2 Snapping to existing nodes
A new line must end on a node that already exists where it meets a meshed beam or seam. A new node on a meshed piece
would leave the plates on the other side with a hanging node.
- The set-back edge beam drawn at Y 1.25 was modelled at **Y 1.20**, the existing 0.40 node on the grid 3 beam
  (engineer's Go).
- The gutter strip was modelled **2 000** wide (X 54 – 56, existing nodes), not 1 600.

### 5.3 Interior beams and openings (lift pit)
- The pit beams (X 64 full height, Y 40.6 and X 66.6 meeting at T-junctions) are `INCLUDE_INTERIOR_LINES` of the
  slab mesh. The plates follow them.
- The pit (X 66.6 – 70, Y 40.6 – 43.3) is meshed with the rest, then its plates are deleted by ID, then its loose
  nodes (48).
- The beam pieces along the pit edge have no plate beside them by design: exempt them, in every zone (a neighbour's
  check reaches them too).

### 5.4 Gutter strip foundation at ground level
- **Actual:** U-gutter, walls 200 (= slab), inside clear 1 200 × 800, base 1 600 × 500 (−0.80 to −1.30).
- **Modelled:** a 2 000 × 500 plate strip (GS500) at 0.00 on 4 piles (each with its 8-node rigid zone, no drop).
  1.00 m²/m of concrete against 1.12 actual; the U-section's stiffness is not modelled.
- **Meshed in one call:**
  - the whole bay inside its beams;
  - the strip edges as interior lines;
  - the pile nodes as interior nodes.

  The plates inside the strip are then switched to GS500 by `PUT /db/ELEM`.
- Plan: `review/ground_Z3_gutter_strip_plan_20261008.pdf`.
- Open: where the gutter crosses the 900 deep ground beams, and the gutter pile load against the pile capacity.

### 5.5 Slab meeting a wall top
The tank south wall (T250 plates from an earlier revision) has nodes every 0.40 m along its top at 0.00.
- Temporary lines between those nodes join the slab loop.
- The slab mesh keeps them unsplit (same size).
- They are deleted after the mesh. The slab and wall plates then share the top nodes.

## 6. Mesh

### 6.1 One mesh size for all zones
A boundary piece longer than the mesh size is split again by the next mesh, and the plates already beside it do not
get the new node.
- Probe: a 0.40 zone against 0.50 seam pieces split **all 12 pieces**, and none of the 12 edges on the far side was
  shared.
- Pieces equal to the mesh size are **not** split: 0.40 pieces at 0.40 held in every zone (167, 273 and 254 seam
  pieces, 96 beam pieces).
- So the mesh size is chosen **before the first zone** and kept. BANWA 2 chose 0.40, which also lines up with the
  1.2 m drop sides (the 0.50 pilot was redone).

### 6.2 Quality
Reported on every zone, not a pass criterion:
- smallest and largest plate angle;
- aspect ratio;
- number of triangles;
- plates under 45° or over 135°.

Most zones had about 3 % of plates under 45°, all round the drops. In Z2 and Z7 most drops came out dense and
distorted: about 38 plates a drop against about 15, and 958 and 1 743 plates under 45°. The cause is not established
(likely uneven splitting of the drop sides by the slab mesh). The engineer accepted it for now.

## 7. Verification

### 7.1 Before the write (dry run and live)
- No node, element, section or thickness ID clash; a section or thickness that exists with the same name is reused.
- No element at 0.00 inside the zone that is not ground-slab work: members of the `BANWA2_GF_*` groups and vertical
  members (column pedestals) are exempt.
- No ground plate of an earlier zone inside this zone, apart from a neighbour's drop halves.
- An existing-seam edge has seam pieces; every column drop has its column node; no `RIGD` master exists already; no
  domain name in use; no two drops overlap.
- The live model equals the snapshot the dry run used.

### 7.2 After the slab mesh
- The slab area equals the zone area minus every drop square (the neighbours' too) and the openings, within
  0.01 m².
- No plate inside a drop or an opening.
- None of the reserved nodes taken.
- **No existing seam, beam or wall-top piece changed or split.**

### 7.3 Read-back (all must pass, then save)

| Check | Pass |
|---|---|
| Areas | slab and drops as expected (± 0.01 m²); drops = n × 1.44 |
| Level | every plate node at 0.00 |
| Free edges | every edge of the zone's plates used by one plate only (counted over **all** plates, the neighbours and the tank walls included) has a line element on it (beam or seam) |
| Non-manifold | no edge of the zone's plates used by more than two plates (zone plates only: the tank's wall junctions are legitimately three-way) |
| Beams on the mesh | every ground beam piece is a plate edge, except pieces beside no slab (`gb_out`, opening edges) |
| Clean-up | no temporary outline or wall-top line left; the closed seams deleted |
| Nodes | no orphan node, no two nodes at the same point (a known orphan excepted) |
| Untouched | every other element and node as before the write, except deliberate deletions |
| Supports | all pinned; count = before + the new piles |
| Rigid links | existing kept; one new per drop |
| Tables | thicknesses, sections and groups present |

A check that fails on something legitimate is fixed **in the check** (with the reason in the script), and the model
is saved only after the fixed check passes. On BANWA 2:
- the tank's three-way wall edges failed the non-manifold check;
- the column pedestals failed the "element inside the zone" pre-check;
- the pit nodes were left loose;
- the pit-edge beam pieces were caught by the neighbour zone's check;
- the beam piece beside the no-slab strip failed the beam-on-mesh check.

None of these was a model error.

## 8. Lessons (BANWA 2)

The staged build's own rules are in §2A. The lessons below come from the zone builds and still hold.

1. **Probe first, on a throwaway copy.** Save the open model as `…_probe.mgbx`, build one bay away from the building,
   try the request variants, then `POST /doc/OPEN` the real file again. The void, interior-node, rigid-link and
   delete-by-ID behaviour were proven this way (06 §4.1), and the seam test of §6.1.
2. **A pilot zone** (16 × 6 m) proved the full flow before the big zones; it was not kept, because the mesh size
   changed after it.
3. **Check the layout for every support type before the first zone.** The drops over the columns with no ground beam
   were missed until three zones were written. The ground floor was rebuilt from the tank revision (r22) with the
   column drops (r27 – r33); r23 – r26 stay on disk as records. A plan of all columns with no beam
   (`ground_zones_cols.py`) is now part of the preparation.
4. **Snap new geometry to existing nodes** where it meets a meshed zone (§5.2).
5. **Delete by ID only.** `DELETE /db/ELEM/<ids>` and `DELETE /db/NODE/<ids>` with the body `{}`, 200 IDs per call. A
   DELETE without IDs would wipe the table.
6. **One revision per zone, a snapshot after each.** A failed check leaves the zone unsaved and nothing earlier is
   touched. Restarting a zone means reopening its base revision.
7. Run long chains in the background with a monitor; keep reports short. In PowerShell, `| Select-Object -First n`
   stops the piped process: a snapshot was cut off that way.

## 9. Result on BANWA 2 (08/10/2026)

| Zone | Revision | FS200 plates / m² | DP350 plates / m² | Rigid links | Note |
|---|---|---|---|---|---|
| Z1 (G – F) | r27 | 2 042 / 306.96 | 567 / 53.28 | 37 | 8 column drops on row F |
| Z2 (F – E) | r28 | 3 475 / 565.84 | 2 470 / 97.92 | 68 | dense drop mesh, accepted |
| Z4 (chiller bays) | r29 | 1 197 / 185.52 | 316 / 30.24 | 21 | set-back beam at Y 1.20 |
| Z5 (E – D) | r30 | 5 379 / 870.72 | 1 989 / 192.96 | 134 | 12 column drops |
| Z6 (D – C) | r31 | 3 426 / 517.26 | 1 282 / 123.84 | 86 | lift pit opening, 10 column drops |
| Z7 (C – B) | r32 | 6 980 / 1 095.16 | 4 654 / 198.72 | 138 | meets the tank wall top |
| Z3 (gutter) | r33 | 330 / 52.00 | GS500 187 / 26.00 | 4 | strip on 4 piles |

Totals: FS200 22 829 plates (3 593.46 m²), DP350 11 278 plates (696.96 m², 454 pile drops + 30 column drops),
GS500 187 plates (26.00 m²), 488 rigid links, 563 supports all pinned, no seam left. Z8 (tank roof) is still to do.

### 9.1 The staged build (layout r9, 08/10/2026): the current model

| Stage | Revision | Result |
|---|---|---|
| Ground beams | r34 `BANWA2_ground_beams_r34` | 90 GB pieces, 499.00 m; piers (52, 12.5), (64, 38.65); TB split at Y 1.25 and 40.6 |
| Outlines 0.20 | r35 `BANWA2_outlines_r35` | 244 drop squares (5 856 pieces); strip edges 130 pieces; row F / E beams split over the strip |
| Piles | r36 `BANWA2_piles_r36` | 249 SPUN 300 stubs, 2 490 nodes; 357 supports, all pinned |
| Slab 0.40 | r37 `BANWA2_slab_r37` | 10 regions, 67 098 plates, 3 938.46 m², drops void |
| Drops + strip 0.20 | r38 `BANWA2_drops_strip_r38` | 8 784 drop plates (36 a drop, 351.36 m²), 773 strip plates (26.00 m²), 249 rigid links, outlines deleted |

The ground floor has 76 655 plates. The read-back of every stage passed:
- areas;
- unconnected edges only on beams;
- no three-way edges;
- no stray nodes;
- beam lengths kept;
- nothing outside the stage changed.

## 10. Scripts (in the project folder `Drafter\scripts\`)

| Script | Role |
|---|---|
| `ground_slab_layout_r7.py`, `ground_slab_pie.py` | Pile layout with drops, tributary (Voronoi) check, efficiency charts |
| `ground_zones.py`, `ground_zones_cols.py` | Zones and their order; the columns with no ground beam |
| `automesh_probe.py`, `automesh_seam_test.py` | Probes on a throwaway copy: drop flow, seam splitting |
| `ground_model.py` | `build` / `write` per zone: plan, payload, checks, write, read-back, save, snapshot; `write_strip` for the gutter |
| `gutter_strip_plan.py` | Gutter strip plan and sections, actual and as modelled |
| `ground_load_map.py`, `ground_load_map_r2.py` | Live-load map by area from the AR uses, for the engineer's comments |
| `ground_slab_layout_r8.py`, `ground_slab_layout_r9.py` | Pile layout from the client loads: each pile ≤ 95 % of capacity (Voronoi load), panels near square |
| `automesh_drop_refine_test.py`, `automesh_gutter_strip_test.py` | Tests of the outline division (drops, gutter strip) on a throwaway copy |
| `ground_beams_r9.py`, `outlines_r9.py`, `piles_r9.py`, `slab_r9.py`, `drops_strip_r9.py` | **The staged build**, `build` (dry run) / `write <key>` each (§2A) |
