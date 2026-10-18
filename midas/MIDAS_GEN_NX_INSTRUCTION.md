# MIDAS GEN NX instruction (for agents)

Rules for any task that reads or writes a MIDAS GEN NX model through the MAPI: building a model from drawings,
assigning loads, running the analysis, extracting results, or making a plug-in. They are distilled from the guides in
this folder, which give the method and the worked examples; every rule names its source. The fire-station values
quoted are examples, not defaults.

**Task router**

| Task | Read |
|---|---|
| First contact with the API, or any endpoint question | `api/MAPI_GUIDE.md` §0 – §12, `api/ENDPOINTS_GEN.csv`, `api/ENDPOINT_REFERENCE.md` |
| Writing a script or tool that talks to GEN NX | M1 – M6 below, `api/CONVENTIONS.md`, `tools/connection.py` |
| Model a building from the structural DXF and AR plan | M7 – M9, then `modeling-guide/README.md` and 01 – 07 in order |
| Ground floor on piles (flat slab, drop panels, rigid zones; staged build or zones) | M7.5 - M7.6, M8, `modeling-guide/08_PILE_SUPPORTED_FLAT_SLAB.md` (§2A staged), `06` §4.1 |
| Beam loads (line, trapezoidal, partial, local / global) | `api/BEAM_LOAD_MAPPING.md` |
| Plate loads, live load from room functions | `modeling-guide/07_AR_PLAN_ROOM_MAPPING.md`, M10 |
| Run the analysis, read results, write the calculation report | M10, `calc-report/CALC_REPORT_GENERATION.md`, `examples/` |
| Make or package a plug-in | `plugins/PLUGIN_GUIDE.md` (mandatory), `api/MAPI_GUIDE.md` §13 – §14 |
| How the library writes an object | `lib/midas-gen-python/midas_gen/` (`lib/README.md` says where) |

---

## M1. The MAPI key is a credential

1. Pass it **only on the command line** (`sys.argv[1]`, first argument) at run time. Never write it into a script,
   file, document, log, commit, URL, chat summary or memory (`modeling-guide/README.md`,
   `calc-report/…` §0).
2. Get it from GEN NX → **Apps → API Settings → Refresh** (blank until refreshed). Refreshing invalidates the old key.
3. The connection **drops** when the model is saved under a new name or reopened. Reconnect (Apps → Connect) before
   the next call. "GEN NX model is not connected" means exactly that.
4. The user runs GEN NX and owns the key. Ask for it when a live step is reached; do not ask earlier.

## M2. Connecting

1. Import through [`tools/connection.py`](tools/connection.py): `connect(key)` sets stdout / stderr to UTF-8
   **before** importing `midas_gen` (its banner crashes a cp874 console), then tries the regional base URLs until
   `GET /ope/PROJECTSTATUS` answers. `MAPI_BASEURL.autoURL()` alone is unreliable (wind-load README, "Live-MIDAS
   gotchas").
2. `midas_gen` calls `sys.exit(0)` with a red box when the connection is refused, so **exit code 0 does not mean the
   script reached GEN NX**. Check the output, or probe `/ope/PROJECTSTATUS` first.
3. Run from PowerShell or Python with `PYTHONIOENCODING=utf-8`, as for plotting (`AGENTS.md` §4).

## M3. Data, units and IDs

1. **Units.** Drawings and processing in **mm**; MIDAS written in **m**, converting only at the write step. Read
   `/db/UNIT` before the first write and state the units used. Gravity is **−Z**: downward loads and the self-weight
   factor are negative (`MAPI_GUIDE.md` §7).
2. **One source per value**, as in the drawing workflow (`AGENTS.md` §2): sizes from the schedule, levels from the SFL
   tags, grids from the grid xref. Intermediate results are JSON files per stage, so every stage re-runs offline
   (`modeling-guide/README.md`, "Conventions").
3. **Deterministic IDs** from a readable scheme, so a re-run gives the same numbers and later steps can target objects
   without reading back (`02` §5, `03` §9):

   | Item | Scheme (fire station) |
   |---|---|
   | Column node | level digit × 1000 + column index |
   | Column element | lower level digit × 1000 + column index |
   | Beam-only node | level digit × 1000 + 101 + i, sorted by (Y, X) |
   | Beam element | level digit × 10000 + 1001 + i, sorted by midpoint (Y, X) |
   | Panel group | level base (100, 200 …) + panel number |

   **Material, section and thickness IDs and section names** (user rule, 2026-10-18, NSO):

   | Item | RC column | RC beam | Steel column / stub | Steel beam | Slab |
   |---|---|---|---|---|---|
   | Material ID | 1xx | 2xx | 3xx | 4xx | 5xx |
   | Section ID | 1xx | 2xx | 3xx | 4xx | - |
   | Thickness ID | - | - | - | - | 1xx (general slab) |

   The slab material takes **5xx** (engineer, NSO r02, 18/10/2026: "slab material 501 RC SLAB FC240"); thickness IDs
   run per slab mark (101 S1, 102 S2, 103 S3).

   Section names, one section per drawing mark:
   - RC beam: `BXX - width x depth`, e.g. `B1 - 250x600`, `RB4 - 200x400` (the mark as drawn, B / RB / ...C / ...A);
   - RC column: `CXX - width x depth`, e.g. `C1 - 300x300`;
   - steel H, channel or other rolled shape: `SBXX - shape depth x width x web thk x flange thk - weight per length`
     (TIS names and masses from `drafter.tis_sections`; a steel column or stub uses its own mark, SC / ...);
   - RHS and SHS: `<mark> - RHS / SHS width x depth x wall thk - weight per length`;
   - CHS: `<mark> - CHS OD x wall thk - weight per length`;
   - a size not yet given: `<mark> - TBC`, never a guessed section.

   **GEN NX takes at most 28 characters in a section name** (NSO r01, 18/10/2026: "[Error] The possible number of
   characters that can be entered in Section Name is 28"; the whole `SECT` table was refused). Steel names are
   therefore written without spaces, the same parts in the same order: `SB1-H300x150x6.5x9-36.7kg/m` (27),
   `SC1-H150x150x7x10-31.5kg/m`, `SB10-H588x300x12x20-151kg/m`. RC names keep the spaces (`B1 - 250x600`). The writer
   asserts the length before any write.

   IDs run in mark order inside each block (101, 102 …). Material names stay within the 16-character limit (M5); their
   wording is the engineer's (proposal: the use, with the grade once given, e.g. `RC COLUMN`, `STEEL BEAM`). Worked
   example: NSO r01 (written 18/10/2026), `04 Code\model\proto_model.py` `number_sections`, `gen_r01.py`.

4. **Dependency order**: material / section → node → element → support → load case and load group → load →
   analysis. An element names its nodes and section; a load names its case (`MAPI_GUIDE.md` §8).
5. **No invented engineering values** (`AGENTS.md` §2). A mark missing from the schedule, a level, a support
   condition or a load is a decision item for the engineer (`modeling-guide/DECISION_LOG_TEMPLATE.md`).

## M4. Write safety

A write changes the user's open model at once, with no undo through the API.

1. **`PUT` on an existing ID overwrites it silently**: a node moves, an element changes. Before writing, read the live
   tables and **abort** on any node or element ID clash, missing section, missing referenced node, or referenced node
   off the level Z by more than 1 mm (`05`, Gate 4).
2. **Back up** the tables a stage touches to JSON before its first write (`midas_backup_before_<stage>.json`); for a
   big change also have the user save the model under a new name.
   A new revision can be made through the API: `POST /doc/SAVEAS {"Argument": "<full path>.mgbx"}` writes the file
   and the open model continues in it, so the earlier file keeps the state before the write; `POST /doc/SAVE` after
   the read-back stores the change (user rule, 2026-10-07: "save model as new RXX (XX - revision)"; BANWA 2
   `..._r21` -> `BANWA2_underground_tank_walls_r22.mgbx` before the tank walls). Never overwrite an existing file.
   In a project folder the revision is `<CODE>_rNN_<what>.mgbx` in the GEN NX working folder (`paths.FEA_RUN`),
   with its row in `03 FEA\MODEL_LOG.md` (M9).
3. **Never blind-`PUT` or `DELETE` a table you do not wholly own.** Read, merge your own items, write back:
   - `PUT /db/BMLD` **replaces** an element's whole `ITEMS` list: read-merge or you delete the user's other loads;
   - `PUT /db/GRUP` **merges** `E_LIST`: to remove members, delete the group and put it again (or have the user
     remove them in GEN NX). The reply echoes the shorter list as if it were stored; only the read-back shows the
     merge (05/10/2026: 16 elements moved to new groups stayed in their old ones);
   - `PUT /db/PRES` merges by item ID: check what is there before adding a case.
   A blanket `DELETE` (order: loads → `CONS` → `ELEM` → `NODE` → `SECT` → `MATL`, and `GRUP`) is only for a fresh model
   the script generated itself (`MAPI_GUIDE.md` §12).
4. **Build each table's payload in full, then one `PUT` per table**. Do not rely on the library's class-level
   registries in a long-lived process; they keep objects from earlier calls (`MAPI_GUIDE.md` §14.9).
5. **Chunk large writes**: a single `PUT /db/BMLD` of several thousand items fails **silently** (nothing written, no
   error). Write about 1 500 items per request.
6. **Sanitise numbers**: beam-load positions `D` must lie in [0, 1]; float noise such as −8e-17 makes MIDAS reject the
   **whole** request. Skip zero-length segments.
7. **Check the body, not only the status**: a 200 reply can carry a per-object error. A write that reports success
   is confirmed only by reading the table back (M6).
8. The library merges coincident nodes; an element built on a merged-away node fails with
   `'NoneType' object has no attribute 'X'`. Create nodes with `merge=False` where coincidence is possible, or
   dedupe first.

## M5. Calls that must not be used, and API limits

| Call | Behaviour | Rule |
|---|---|---|
| `POST /doc/IMPORTMXT` | **Replaced the whole open model** with a partial MCT (5 120 nodes → 0) and still replied "command complete" | **Never** on a live model. MCT import is a GUI action on a saved copy. `/doc/EXPORTMXT` (read-only) is safe |
| `/db/MADO`, `/db/SBDO`, `/db/DOEL` | Domain tables are read-only through the API | Organise with structure groups (`SLAB_<L>`, `SLAB_<L>-Pxx`) |
| `/db/RCHK` | 404 in the current GEN NX | Enter rebar in the GUI; read it back from the MCT export |
| `/db/posl` | Usually empty | Seismic parameters from the MCT `*SEIS` block, checked against the base shear |
| `/db/BMLD` with a case or load group that does not exist | `Error: Wrong Field` | `PUT /db/STLD` and `/db/LDGR` first |
| `POST /ope/AUTOMESH` | The reply also lists split beams; a warning-only reply still makes the mesh; a used `DOMAIN_NAME` fails | Find new plates by diffing `ELEM` before and after; check `/db/MADO` for names (`06` §4). Voids, interior nodes / lines (`"OPTION":"User"`), drop panels and `/db/RIGD`: `06` §4.1 |
| `POST /ope/AUTOMESH` on a boundary line longer than the mesh size | The line is split again; plates already meshed beside it do not get the new node (no connection) | One mesh size for every zone of a floor; new lines end on existing nodes (`08` §5.2, §6.1). Pre-split pieces: `ceil(L / size)`, never `round` (13 m at 0.40 → 0.406 m pieces, split again, the next mesh failed) |
| `POST /ope/AUTOMESH` creates nodes | A node table read before the call misses them | Re-read `NODE` after every mesh call before checking plates (`08` §2A) |
| `DELETE /db/ELEM/<ids>`, `DELETE /db/NODE/<ids>` | Deletes exactly those IDs (body `{}`); without IDs it would wipe the table | Delete by ID only, 200 IDs per call; check the IDs first (`08` §8) |
| `Result.TABLE.*` (library) | Calls `Model.units()` first: a `PUT /db/UNIT` to kN-m on the user's model, not restored (FSK 11/10/2026: the engineer's model was in N-m) | For a read-only extraction call `POST /post/TABLE` directly; the reply carries `FORCE` / `DIST`, convert in the script |
| `PUT /db/SECT` with a name over 28 characters | The whole table refused ("possible number of characters … in Section Name is 28"); the tables before it stay written | Section names ≤ 28 characters (M3: steel names without spaces); assert before writing (NSO r01, 18/10/2026) |
| `PUT /db/MATL` with a name over 16 characters | Rejected ("possible number of characters … is 16"); the other tables still write, so the elements point to a missing material | Material names ≤ 16 characters; treat any error reply as fatal and check `MATL` in the read-back (FSK r01, 11/10/2026) |
| `PUT /db/SECT` / `PUT /db/ELEM` re-sectioning; `DELETE /db/SECT/<id>` | The section stiffness scale factors (`/db/SECF`: cracked Ixx / Iyy / Izz) are keyed by the **section ID**: they stay with the ID when it is redefined under another mark, and go with it when it is deleted. The read-back of `SECT` and `ELEM` shows nothing; only the moments change (NSO r06 - r09, 18/10/2026: SECF on every RC section but 201, so whichever beams held ID 201 stayed uncracked; GF line 7 at F -69 / -108 / -50 kN m in three revisions with the same geometry and loads) | Before any re-sectioning read `SECF` (and the other per-section tables) and carry it by mark, not by ID; check that every section of one kind has the same factors; diff all `/db` tables of the old and new file when results move without a reason (`r1_tables.py`) |
| `PUT /db/RIGD` | Keyed by the master node: `{"<master>":{"ITEMS":[{"ID":1,"GROUP_NAME":"","DOF":111111,"S_NODE":[…]}]}}` | Read back and compare; existing masters stay unchanged (`08` §4) |

Commands the guides use that are not in the library list: `/ope/AUTOMESH`, `/db/MEMB`, `/db/STOR`, `/db/DCON`,
`/db/MATD`.

## M6. Verify every write

1. After each write, **read back** and print: counts written against expected, count by section, maximum length
   difference against the approved sheet (fire station ≤ 0.5 mm), all nodes at their level Z, group membership.
2. Capture a plan and an isometric view (`POST /view/CAPTURE`) and show them beside the approved sheet. On a large
   model the whole-model capture hides a small or buried part (BANWA 2 tank under the roof): render the written part
   from the read-back data as well.
3. A summary message is not evidence: the read-back is. Report the read-back numbers.
4. For a meshed floor, check the areas, the free and three-way plate edges, the beams on plate edges, orphan and
   duplicate nodes, the boundary pieces not split, and that nothing outside the written part changed (`08` §7). A
   check that fails on something legitimate is corrected in the check with its reason; the model is saved only after
   every check passes.

## M7. Modelling from drawings: the gates

Work **one level at a time**, with four gates before each write (`05`):

1. **Independent check** against the DXF by a script that shares no clean-up code with the tracer: DXF beams covered,
   no invented beams, labels match marks, topology (crossings share nodes, no dangling ends, every column used),
   levels.
2. **Review sheet** over the grey drawing: beams coloured by mark with mark and span, inferred marks in yellow,
   engineer's marks in green, new nodes with ID and coordinates, a notes panel listing every level-specific fix and
   assumption. **The sheet is the contract**: what the engineer approves is what is written.
3. **The engineer says "Go"** for that level, after numbered questions with a recommendation each. Do not start the
   next level until asked.
4. **Pre-write checks** on the live model (M4.1), then write, then read back (M6).

5. **A floor too big for one write is built in zones** (`08` §2 – §3):
   - each zone is a dry run, then the engineer's Go, then a write saved as its own revision with a snapshot after
     it;
   - the next zone starts only if the live model equals that snapshot;
   - shared items belong to the first zone in the order;
   - open edges are temporary seams;
   - probe new request formats on a throwaway copy first (`automesh_probe.py`).

   Zones may run in a chain on the engineer's word; the chain stops at the first failed check.

6. **Or build in stages, one kind of object at a time over the whole floor** (`08` §2A, BANWA 2 r34 - r38):
   1. beams;
   2. outlines pre-split at the refined size;
   3. piles and rigid-zone nodes;
   4. slab region by region between the beams;
   5. drops / strips at the refined size, then rigid links, then the outlines deleted.

   Each stage is its own revision and snapshot, and the next stage checks the live model against that snapshot. This
   is the current method: no seams, and the mesh refinement is controlled by the pre-split outlines.

Start from the intake (`01`): layers, panel origins, marks, SFL tags, displaced groups, the section table, and the
decision list sent to the engineer **before** extracting geometry that depends on an answer.

## M8. Modelling rules (confirm per project)

These were the engineer's answers on the fire station. Use them as the proposal and record each project's answers in
its decision log (`DECISION_LOG_TEMPLATE.md`), since they are engineering decisions (`AGENTS.md` §4).

| Topic | Fire-station rule | Guide |
|---|---|---|
| Column position | Node on the grid intersection; construction offsets removed (or a section offset, node kept on grid) | 02 §3 |
| Floor level | Typical SFL of the plan (majority of tags); local steps ignored | 02 §4 |
| Slab level | Slab at the **beam level**, not the local SFL step | 03, 06 |
| Beam line | Centreline. MLINE vertices are the justification line: shift by half the width | 03 §1 |
| Edge pairs | Pair only within the width window of the scheduled widths; unpaired edges are listed | 03 §1 |
| Curved beam | Bulged LWPOLYLINE; chords on the centreline arc, sagitta ≤ b/8, chord ≈ 2 × mesh size; same points on every level | 04 |
| Neglected members | Only by the engineer's decision (BX stair trimmers); re-attach dead ends, check connectivity | 03 §7 |
| Mesh | 0.50 m, thick plates; openings under 1 m² ignored; cantilever vertices prepared on the whole level before meshing any panel | 06 |
| Model input from an AR plan (CHATAM, user 11/10/2026) | Slab boundary read off the AR and checked edge by edge on every floor (each edge on AR linework); a lift shaft opening on the **centre lines of the lift corner columns**; the review sheet draws every slab edge, openings included, as one **heavy** line (0.70 mm), and nothing else that reads as an edge (an undecided wall outline is left off) | project `slab_columns.py`, `PROJECT_WORKFLOW.md` |
| Pile-supported ground slab (BANWA 2 answers) | FS200 + DP350 drops at the mid-plane; pile stubs to −1.50 pinned (r9: SPUN 300 as solid round dia 300); 8-node rigid zone at each pile (and at a column with no ground beam); GB 400 × 900 CT; all supports pinned; slab 0.40, drops and gutter strip 0.20 by pre-split outlines | 08 |

Drawing-reading lessons carried over from the drafting side: column size from **visible** dynamic-block entities only;
grid lines and bubbles inside the grid xref; a plan may hold a displaced copy of a bay; Thai text in AR and regulation
PDFs does not extract cleanly, so render the pages and read them as images (`01`, `07`).

## M9. Where project data lives

- Project inputs, intermediate JSON, review sheets, backups and reports belong to the **project folder**, not to
  this repository. New projects use the office structure (`docs/general/PROJECT_WORKFLOW.md`):
  - model scripts in `04 Code\model\`, taking the model revision as an argument;
  - GEN NX runs in a local folder (`paths.FEA_RUN`): the result files reach several GB per run;
  - one row per revision in `03 FEA\MODEL_LOG.md`; the milestone `.mgbx` copied to `03 FEA\models\`;
  - read-back snapshots in `03 FEA\snapshots\rNN\`, the JSON backups before a write in the snapshot folder of
    the revision they protect, exported results in `03 FEA\results\rNN\`;
  - the decision log (`modeling-guide/DECISION_LOG_TEMPLATE.md`) in `03 FEA\`.
- Projects started before the template keep their folders (SSK and BANWA 2: `<project>\Drafter\`). Set
  `MG_WORKDIR` for the archived scripts.
- MIDAS model files (`.mgb`, `.mcb`), exported MCT text and result dumps are not committed.
- A reusable tool graduates into this folder (`midas/tools/`) with tests that run without GEN NX (a dry run that
  builds the payloads, `CONVENTIONS.md` A6).

## M10. Loads, analysis and results

1. Load cases and load groups before loads (M5). Self weight as a body force with factor −1.
2. Live load per use from the **Ministerial Regulation B.E. 2566, clause 11** table, mapped from the AR room
   functions; no reduction for parking (clauses 13 / 14). Equipment loads and anything not in the table are the
   engineer's values (`07` §4 – §5).
3. Strength combinations per **clause 7** (1.4D + 1.7L), not 1.2 / 1.6. Service combinations per clause 6
   (`calc-report/…` §10).
4. Check each case's reaction total against Σ(q × area) after the analysis.
5. Results only after a successful `POST /doc/ANAL`; they are stale once the model changes. A force file pulled
   earlier is kept with its date and is **not used for design or joint checks after the model has changed** (BANWA 2:
   the forces of 05/10 predate the engineer's redesign of 06/10; the joint strength check waits for a fresh pull).
   **Probe once before asking for result tables** (`POST /post/table`): without results GEN NX answers every
   request with "[R] Cannot generate table data as there is no analysis result" and shows each one in its message
   window. A read-only snapshot that asked for 171 reaction tables filled the engineer's screen and looked like a
   failed write (BANWA 2, 05/10/2026). Stop after the first such reply. In result tables a static
   case `DL` is named `DL(ST)`, a general combination `U1(CB)`, a concrete-design combination `(CBC)`, a steel-design combination `(CBS)` (`sLCB1(CBS)`; also the `TYPE` of a result graphic).
   That is the name in the request (`LOAD_CASE_NAMES`); the reply's `Load` column gives the bare name (`SW`, `U1`):
   match on the name before `(` (BCR r01, 12/10/2026).
6. Storey drift on meshed columns: between storey-level nodes on each column line, not per element.

## M11. Plug-ins

Read [`plugins/PLUGIN_GUIDE.md`](plugins/PLUGIN_GUIDE.md) in full before packaging. In short: a plug-in is a static
web bundle in a webview; `<div id="midas-controller">` gives the close button; `manifest.json` must copy the official
template schema field for field ([`plugins/template/manifest.json`](plugins/template/manifest.json)); bundle every
runtime library (the webview blocks CDNs); write non-destructively and in chunks (M4).

## M12. How these rules grow

As for the drawing rules (`AGENTS.md` §3): when a live run teaches something, fix the script, write the rule here or
in the guide that owns the topic (dated, with the case), and add a line to the technique log in
`modeling-guide/README.md`. The copied guides may be edited here from now on; note the change in the file.
