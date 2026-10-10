# Steel detailing instruction (structural steel, hollow sections first)

Rules for every steel drawing set produced here, first applied to the steel roof truss `jobs/steel_roof_truss`
(SRT-ST), then to the portal frame `jobs/steel_portal_frame` (SPF) and the BANWA2 steel roof on an RC frame (outside the
repository, `jobs/README.md`). The steel presentation approach is summarised in `docs/steel/README.md`. Sources and page references:
`docs/steel/reference/SOURCES_STEEL_DETAILING.md`. The general rules in `docs/general/` still govern title blocks,
pens, text, dimensions, annotation and symbols (`DRAWING_STANDARD_EIT-011006-19.md`, `ANNOTATION_ALIGNMENT_GUIDE.md`,
`SYMBOLS.md`). Abbreviations:
- DSC = AISC *Detailing for Steel Construction*.
- DG21 / DG24 = AISC Design Guides 21 / 24.
- D1.1 = AWS D1.1:2015.
- 360 = AISC 360-16.

The rules are numbered so a review can cite them, for example "S5.3".

---

## S1. What the set must carry

The set is the engineer's design set, drawn "shop-ready": every size, length, weld and bolt is given. It must
also carry what AISC 303 / D1.1 require of the contract documents:

1. **Joint information** (DSC p.86):
   - member forces, or the joint details themselves;
   - the truss support connection (DSC p.91).
2. **Welding information** (DG21 p.142-144):
   - the size and extent of every weld;
   - static or cyclic loading;
   - the WPS requirement;
   - CVN (stated even when none is needed);
   - filler metal certificates;
   - "no unspecified welds";
   - tack welds;
   - inspection: who, what, how much, and the acceptance criteria.
3. **Materials**, with grades for tubes, plates, bolts, rods and grout.
   - JIS steels are **not listed in D1.1**. State that WPSs are qualified by test or approved with the mill chemistry
     (DG21 p.71).
   - Use SM400B (JIS G 3106) for welded plates; SS400 only where nothing is welded.
4. **Erection and stability** (DSC p.149-155, AISC 303 7.10):
   - whether the frame is stable on its own, and what holds it;
   - the lifting weight;
   - the assembly sequence;
   - matchmarks;
   - anchor rod setting and levelling;
   - which end is fixed first.
5. **Camber**: the value and the diagram (DSC p.209), plus a statement of whether the member lengths include it.
6. **A bill**:
   - members (Table 2);
   - plates and fittings (Table 5);
   - field bolts with lengths and counts (Table 4);
   - **one weight figure used everywhere** (DSC p.244, checker).
   - **All the structural steel of the structure** is in the bill, not only the main members: on a roof, the trusses
     (by type and section, times the number of spans), posts, bracing struts, tie rods, purlins, sag rods and caps
     (user, 2026-10-06: "bill of material including purlin, tie rod, sagrod, truss (all structural steel)"). State
     how the lengths are measured (net, no laps) and what is not included (cleats, plates, bolts, turnbuckles), give
     the unit-weight basis (JIS formula or table) and mark unconfirmed grades TBC; reconcile the totals by section
     with the analysis model. Example: BANWA2 S-206 (`plans/bom.py`).

## S2. Geometry and setting out

1. **Working lines**
   - Welded trusses use the member centroids as working lines (DSC p.204).
   - Branch axes meet at a work point (WP) offset e from the chord axis, away from the web.
   - Mark the WP with a circled cross and draw the axes WP to WP in grey chain.
2. **Gap K-joint limits, AISC 360-16 Table K3.1A**, which is also DG24 Table 8-1A (p.104). Check each one in the calc,
   tabulate them, and state them in the general notes:
   - −0.55 ≤ e/D ≤ 0.25;
   - θ ≥ 30°;
   - **0.4 ≤ Db/D for a gapped K-joint**;
   - 0.2 < Db/D for T, Y and X joints;
   - g ≥ tb1 + tb2;
   - D/t ≤ 50 (X joint: 40);
   - Db/tb ≤ 50, and ≤ 0.05E/Fy for a compression branch;
   - Fy ≤ 360 MPa and Fy/Fu ≤ 0.8;
   - **chord end distance ≥ D(1.25 − β/2)**, measured from the near face of the branch.
3. **Gap**
   - Office rule: ≥ 20 mm, so both toe welds can be made (DG24 Ex 8.3: about 24 mm is comfortable).
   - Where e is held at 0.25D, the gap may drop to max(12, tb1 + tb2). The two toe welds must still fit.
4. **Node details give, from the chord**:
   - e (with e/D in Table 3);
   - the gap on the chord face;
   - θ;
   - the station of each branch axis on the chord face, measured from the panel-point line through the WP (DSC Fig
     3-43). The fitter can then mark the chord without the WP, which lies off the steel.
5. **Dimension hierarchy on an elevation** (DSC p.209):
   - outermost: the working dimensions (span c/c bearings, half span);
   - then the splice positions from the pin-end bearing;
   - then the panel chain.
   - Every chain must add up to its overall dimension (DSC p.237).
6. **Lengths**
   - Chords: the tube between the end plates.
   - Webs: the axis length between the chord faces, for the flat truss. The note says the fabricator adjusts for
     camber and cuts to fit (DSC p.209).
   - A loose member also gets its hole-to-hole length.
7. **Camber**
   - Parabolic.
   - Ordinates at every panel point, on an exaggerated diagram.
   - Measured with the truss unloaded (DSC p.203, 209-210).
8. **Sliding bearing**: the slot takes ± (thermal + chord stretch under D + Lr). The chord stretch is the roller-node
   displacement from the analysis (DSC p.92-93). State where the rods sit at erection.
9. **A plate on a sloping or tapered face follows that face** (user rule, 2026-10-04: "plate not align to column
   tapered flange alignment").
   - The plate's faces are parallel to the flange it bears on, its ends are square to that flange, and its bolts
     are square to the plate. Do not draw it plumb or with level ends on a tapered member.
   - The connected member's flanges stop on the plate's outer face, intersected line by line.
   - Draw the member as it is fabricated: a tapered flange stays straight to the cap or end plate. Where the
     analysis depth law stops at a work point (the MIDAS taper ends at the eave), continue the taper above it; do
     not put a kink in the flange.
   - Example: on SPF-ST-5001 detail 1, the knee and canopy end plates lie on the tapered column-head flanges
     (`spf_details.face_plate`, `bolt_ax`; the geometry is `calc_spf.knee_geometry` / `col_depth`).
10. **Joints from a concentric analysis model.** An analysis model usually puts the web axes on the chord axis (e = 0).
    Check the gaps that geometry gives at every node before drawing it: on BANWA2 many nodes overlapped by up to 13 mm
    or had g < tb1 + tb2, which is neither a valid gapped nor a valid overlapped (Ov ≥ 25 %) joint.
    - Set **one work-point eccentricity e per truss type** (one setting-out value for the fabricator): the least
      multiple of 5 mm that gives g ≥ 20 mm (S2.3) between every pair of neighbouring branches, capped at 0.25 D;
      where capped, report the least gap (≥ max(12, tb1 + tb2)).
    - Tabulate e (e/D), the least gap, θ and β for every type, with the K3.1A geometry checks; report a type outside
      the limits (BANWA2: β < 0.4 on the 139.8 - 216.3 chords with 48.6 - 76.3 webs) to the engineer, with the
      options (upsize the webs, or check the joints to EN 1993-1-8 / CIDECT, 0.2 ≤ β ≤ 1.0).
    - The moment e × the branch force components is not in a concentric model: the engineer decides whether it is
      added to the chord checks.
    - The joint strength (K3) needs the forces of the **current** analysis; never check joints on forces pulled
      before a redesign.
    - Example: BANWA2 `plans/calc_joints.py` (`e_type`, `nodes_of`, `k31a`), TABLE 10 on S-205.

## S3. Marks and pieces

1. **Two levels of mark**
   - The truss has an erection mark (T1).
   - Members and plates have their own piece marks, which must never repeat the erection mark (DSC p.205).
2. **Pieces that differ in any way get different marks** (DSC p.95 #24-25). Any difference counts:
   - section;
   - length;
   - end preparation.
3. **How the marks are generated**
   - Web marks are generated from (section, length, loose or welded): `srt_engine._web_marks()`.
   - Chords are marked by shop piece: TC1 / TC2, BC1 / BC2.
   - In a design set of many truss types drawn as typical elevations (BANWA2), the web tags W1, W2 ... are **section
     marks** (one per section over the roof, smallest first, with a table of their sections); the piece marks of S3.2
     are then made by the fabricator on the shop drawings, and a note says so.
4. **Plates and fittings** carry assembly marks p1, p2 ..., and washers w1 / w2. Leaders and Table 5 use the same mark.
5. **Shop pieces and splices**
   - Shop pieces are SP1 - SP3.
   - Field splices are FS1 / FS2. They are matchmarked after the shop trial assembly, with the holes drilled in pairs
     (DSC p.157).
   - Positive notes say what differs, for example "SP1 PIN BASE PL p4, SP3 SLIDING p5" (DSC p.208).
   - Stamp PIN END / SLIDING END / TOP on each piece.
6. **No node numbers** on the general elevation (user rule). Tables refer to panel points counted from the pin end.
7. **Truss marks on plans** (user, 2026-10-06: "it cannot be T1 for all; it can mark each support span depending on
   section consistency; use bracket to mark a truss; mark at the middle of truss length")
   - A truss continuous over several supports gets **one mark per support span**.
   - Spans share a mark only when they have the same length and the same sections in every member (chords, webs, end
     verticals); any difference is a new mark. Sub-trusses are marked the same way (ST1, ST2 ...).
   - On the plan: a bracket over the span and the circled mark at its middle, in a gap in the bracket line; edge
     trusses have the bracket on the outside. The bracket is the plan bracket of FLOOR_PLAN_DRAWING_INSTRUCTION FP10.2:
     solid grey, 45° diagonal ends of the mark circle's diameter, ending on the chord at the post faces. A table gives
     each mark's span and sections and the number of spans.
   - Worked example: BANWA2 S-104 (`plans\model_data.truss_spans`): 74 support spans of 13 truss lines in 17 marks.
8. **Weight per length after every section size** (user, 2026-10-07: "always add weight per length after section
   size"). Wherever a table or schedule gives a steel section, the unit weight follows it in brackets, 2 decimals:
   `PG 139.8x4.5 (15.01 kg/m)`, `SHS 200 x 200 x 6 (35.82 kg/m)`, `RB20 (2.47 kg/m)`. One function gives the figure
   for the tables and the bill, so they never differ (JIS formula or table, steel S1.6). A bill that already has a
   kg/m column keeps it. Example: BANWA2 TABLES 5 - 8, 10, 11 (`plans\model_data.sect_w`).

## S4. Graphics (office rules, user 2026-10-03)

Placement of leaders, tags, weld symbols, cutting planes and node dimensions: `ANNOTATION_ALIGNMENT_GUIDE.md` §9.

0. **Units**
   - Every measured value in notes and leaders carries its unit, e.g. "GUSSET PL 10 (p8), 200 mm LONG ON THE CHORD,
     WELDED 10 mm OFF THE TRUSS PLANE".
   - Dimension figures, weld symbol sizes and designations stay bare.
   - Table headers carry the units (`ANNOTATION_ALIGNMENT_GUIDE.md` §2.4.2).
   - Leaders to bolts aim at the bolt centre and end in an open circle of 1.25 × the hole size (`leader(..., bolt=hole)`).
   - A leader to a plate ends with its arrow on the plate edge, never inside the plate.
   - A number and its unit stay on one line (`td_engine.WRAP_UNITS = True`).

1. **Hollow sections**
   - The wall is shown as a fine hidden line (S-STL-WALL, grey ACI 8) in every view, including the 1:50 elevation.
   - A CHS cut in section is a solid-filled ring. Never cross-hatch steel in section (DSC p.94 #12).
2. **Centre and work lines**: grey ACI 8, EIT grid linetype (S-GRID).
   - Bolt, hole, slot and anchor-rod centre lines stay on S-CENT, but in a steel set **S-CENT is grey ACI 8, 0.18**
     (`drafter/steel.py`; user rule 2026-10-03).
   - **Hidden wall lines end on the pipe break.** A tube's inner wall stops where it meets the first break curve from
     the kept side: the single arc on one half, the inner arc of the lens on the other (`break_point`). It never runs
     through the break. Use `chord(..., breaks=(left, right))`; `branch()` and the loose-diagonal tube do the same.
   - **A part behind another is hidden where it is covered.** For example, the gusset behind the knife plate is
     dashed (S-STL-HIDN) where the knife plate covers it and solid elsewhere (`srt_sheets.behind`). Decide which part
     is in front from the lap: here the knife plate is on the truss plane and the gusset is offset behind it.
3. **Member tags**: letters in a circle, placed **beside** the member (`place_tag`), never on its middle.
   - Among thin members (CHS webs at 1:50) check the clearance on the exact geometry: `place_tag` samples 9 points of
     the tag box and lets a thin web pass between them. BANWA2 uses the first candidate whose circle keeps 35 mm clear
     of every member and tag (`truss_details.best_spot`).
4. **Leaders**
   - Never cross.
   - 0/90/180/270° single segments or orthogonal L shapes (`td_engine.LEADER_ORTH = True`).
   - An L has a real second segment: a vertical leg of at least 3 mm (`ORTH_LEG_MIN`), the note 5 mm off the edge.
   - Notes are short. Weld information goes in symbols, not in leader text.
   - A member seen side-on with a clear band (a purlin) is **named on itself**, inside the band, with no leader
     (annotation guide §9.8).
5. **Breaks**
   - Hollow sections use the user's pipe break (`chs_break`): one arc and a lens, square to the member axis.
   - A Z break is only for whole views, RC and open sections.
6. **Hatches**: concrete AR-CONC, grout AR-SAND.
7. **Welds as seen** (`weld_region`, `weld_bead`, `weld_band`, `weld_branch`)
   - 45° hatch only, spaced at 1/3 of the leg, 0.2 - 0.5 mm plotted.
   - The boundary goes on Defpoints, so it never plots.
   - Drawn at true size, but at least 1.0 mm plotted.
   - A weld round a tube or along a plate edge seen face-on is a band plus its profile at the silhouettes.
   - On a branch the profiles use the heel and toe legs and the band uses the side leg (`branch_zones`).
8. **Cutting planes** (`cutmark`)
   - Heavy end strokes outside the object.
   - Arrows look left or down (DSC p.94 #10).
   - Label "n/sheet". The section keeps its orientation.
   - On a busy view, use only the ends.
9. **Plate outlines**: no self-crossing (hull polygons). Check any gusset that is built from points.
10. **Detail callouts** (`detail_callout`, annotation guide §9.7)
    - A dashed circle on layer S-CALL (HIDDENX2, 0.25 mm) round the part enlarged elsewhere.
    - A leader whose arrow lands on the circle edge, at a point in clear space (`at=` angle), never on a member inside.
    - The note reads "DETAIL n/sheet - WHAT", e.g. "DETAIL 2/5004 - FB1 LUG END".
    - On a dense elevation (a 1:50 truss, where leader notes would cross members or dimension chains) use the EIT
      form instead: the dashed circle, a short leader from its edge to a **split bubble "n / sheet"** placed in clear
      space inside the view. Call out one joint of each kind on every elevation that has it (user, 2026-10-06: "detail
      call out"). Example: BANWA2 S-202 - S-204 to S-205 (`truss_details.callout_nodes`).
11. **Steel in plan** (user, 2026-10-06; FLOOR_PLAN_DRAWING_INSTRUCTION FP9.1, FP9.2)
    - Every member is a double line at its **projected width**: CHS outside diameter, SHS width, channel flange width,
      round bar diameter. The wall thickness is not shown in plan.
    - Posts and columns are drawn as their actual section outline. **A post that runs up through the truss to the top of
      the roof trims the truss chords** on every plan of the roof (bottom-chord and top-chord plans): the post outline is
      whole, the chords stop at its faces (user, 2026-10-06).
    - **Tie rods are one line each on the grid linetype** (CENTER) with their own pen (user, 2026-10-06: "tie rod show as
      grid linetype with current lineweight"), never merged with the other rod of a cross (a merged pair is split at the
      crossing and the dashes no longer show).
    - Junctions are clean (union of the member strips); a member below another is left out where covered (a purlin
      over a top chord, a bottom chord over a post).
    - Circled marks over members: the member lines stop at the circle (the geometry is cut). A wipeout is not used: the
      AutoCAD PDF plot of the office set ignored it (BANWA2, 2026-10-06).
12. **Key sections and enlarged elevations of continuous trusses** (user, 2026-10-06: "key section for truss detail
    ... 1:200 then lead to enlarge detail; show dummy top/bot/dia for showing that those are end at post or continue
    to others")
    - Every truss line (lines with the same span sequence grouped) is drawn whole as a **key section at 1:200**:
      member axes as single lines, posts and column stubs, grid lines and bubbles, the support spans dimensioned.
    - The **post (support) start level** is given on every key section: one level mark whose line runs along the post
      bases where they are all at one level, else a level at each post (user, 2026-10-06: "add post start level at
      key section"); the line along the bases is grey in the grid linetype (SYMBOLS.md, level mark); a sheet
      note says where the level comes from (model or column top as built).
    - Each support span carries its mark (S3.7) in a **split bubble, mark over the sheet of its elevation**, sitting in
      a gap of a grey bracket (S-BRACKET) from post face to post face over the top chord; the diagonal of the bracket
      is the bubble diameter (FLOOR_PLAN_DRAWING_INSTRUCTION FP10.2), smaller only where the span is too short.
    - The **enlarged elevation (1:50) of each type** shows, beyond each post, the adjacent span's top chord, bottom
      chord and first web **hidden** (S-STL-HIDN, grey fine dashed; user, 2026-10-06), broken about 0.8 m beyond the
      post, with a leader note "ADJACENT SPAN Tn" ("... WHERE THE LINE CONTINUES" when only some spans of the type
      continue); no "(DUMMY)" in the note (user, 2026-10-06). Where the truss line ends at the post the note reads "END
      OF THE TRUSS LINE".
    - **Each post axis carries its grid bubble** (7 mm, S-GRID axis up to it) where the post is on a grid line (user,
      2026-10-06: "show GL"); an off-grid post has none.
    - The chord levels at both supports (centre lines, model levels) are level marks whose lines are grey in the grid
      linetype, like the key-section post start (SYMBOLS.md, level mark; `truss_details.level_grey`).
    - Every elevation calls out its joints to the welded-joint sheet (S4.10) and its title note gives the type's e
      (S2.10).
    - The span drawn is the one of the type with the most neighbours, so the hidden members are its real ones; when the
      grids or levels differ between the spans of a type, the title note names the span whose grids and levels are
      shown.
    - Worked example: BANWA2 S-201 (key sections K1 - K9), S-202 - S-204 (elevations T1 - T17, ST1, ST2),
      `plans/truss_details.py` (`key_section`, `truss_elev`).

## S5. Weld symbols (AWS A2.4; DSC p.115-127, DG21 Fig 3-36)

1. **Every weld gets a symbol.** Never write "FILLET ALL ROUND" in a note (DSC p.95 #42). Symbols are drawn with
   `drafter.steel.weld()`.
2. **Grammar**
   - Arrow side is below the reference line, other side above.
   - **Both sizes are written for a both-sides weld** (p.117).
   - Order is size, symbol, length, pitch, reading left to right.
   - The perpendicular leg of a fillet, bevel or J symbol is always on the left.
   - The arrow is never collinear with the reference line.
3. **Length**
   - No length means the full joint length (p.120).
   - A partial weld has its length to the right of the symbol, e.g. `3 ▷ 100`, both sides for a knife plate in a slot.
4. **All-round**
   - Use only where the whole perimeter is reachable and intended (tube ends, branches, seals).
   - Never round a plate end that would wrap a corner (DSC p.97 #47-48).
5. **Tail**
   - Holds a reference: typical detail (4/5001), "SEAL", "TYP. BOTH LUGS", or a joint designation.
   - Leave it out when there is nothing to say.
6. **Field weld**
   - The flag points toward the tail.
   - Use it only for welds really made on site. On SRT that is the pin-end plate washers w1. Keep paint 50 mm clear
     of them (DSC p.128).
7. **Groove welds**
   - A bevel symbol has the arrow broken toward the member to be prepared (p.122).
   - The size of a PJP is (E). Never omit E; it is the commonest PJP error (DG21 p.46, 67).
8. **NDT letters** go on the line beyond the symbol ("MT"). No extent means 100 % (DSC p.127).
9. **Weld key**: sheet 1001 explains every symbol form used, with the near-side / far-side and full-length conventions.

## S6. Weld sizes and hollow-section welds

1. **Develop the wall.** Branch and tube-end welds are sized to develop the wall, not the force, so they cannot unzip
   (DG24 2.1, DG21 p.137).
   - Effective throat a = 0.9 Fy t_des / (0.75 × 0.6 FEXX) = **0.89 t** for STK400 / E49.
   - **No directional increase.**
2. **Round branch on a round chord: AWS D1.1 Fig 9.10, column E = t** (`calc_truss.branch_weld`).
   - The local dihedral Ψ is computed round the joint (`dihedral`).
   - **Heel** (Ψ < 60°, acute side): L = 1.5t + Z. Z = 3 mm (Table 9.5, 45-60°, SMAW or V/OH positions).
   - **Side**: L = 1.4t (Ψ ≤ 100°), 1.6t (≤ 110°), 1.8t (≤ 120°).
   - **Toe** (Ψ > 120°, obtuse or gap side): the branch edge is bevelled and L = 1.4t.
   - A 45° diagonal has all three zones. A vertical of β ≈ 0.6 also has toe zones, at its out-of-plane sides (Ψ ≈ 128°).
3. **Where the legs appear**
   - In Table 3, as HEEL / SIDE / TOE for each member mark (BANWA2: TABLE 11 by web mark, the largest legs of all the
     joints of that mark).
   - On the symbol: the side leg, all-round, with tail "4/5001", the typical zone detail (sections at 1:1).
4. **Plate welds**
   - Minimum: Table J2.4, by the thinner part (≤ 6 → 3, ≤ 13 → 5, ≤ 19 → 6).
   - Maximum along a plate edge: t − 2 for t ≥ 6 (DG21 p.49).
   - Fillet legs are standard 3/4/5/6/8/10/12 (`leg_std`).
   - 5 mm on a 2.3 mm wall is over-welding with a burn-through risk (DG21 p.88, 101).
5. **Flange splice weld**: DG24 Eq 5-7 for the design tension, at least the J2.4 minimum. An oversized fillet dishes
   the flange (DG21 p.92), so the flange faces are **machined after welding**.
6. **Fit-up**: gap ≤ 2 mm; above that the leg grows by the gap, up to 5 mm (D1.1 5.22.1).
7. **Seal welds** (caps, slot caps, flanges) are continuous fillets made to the WPS and inspected as structural welds
   (DG21 p.63). A galvanized alternative needs vent and drain holes, Ø13 / Ø25, at both ends of every closed tube
   (DG24 p.11).
8. **Welding notes**
   - Welders are qualified for tubular T-, Y- and K-connections (6GR).
   - Short-circuit GMAW (GMAW-S) needs a WPS qualified by test, and single-pass FCAW is not allowed (DG21 p.18, 34).
   - Assembly: tack the webs to one chord first ("E" assembly, DG21 p.138).
   - Turn the pieces so welds are flat or horizontal (DSC p.114).

## S7. Joints, splices and plate-to-tube connections (calc, `calc_truss.py`)

1. **Member effective lengths**: K = 0.9 for chords and 0.75 for webs in a welded CHS truss (DG24 8.4).
2. **Unbalanced nodes** (DG24 8.2, Fig 8-4)
   - Within 0.8 - 1.2 the joint is pure K.
   - Otherwise the balanced part is K and the rest is X at a top node (purlin load on the opposite face) or T/Y at a
     bottom node. The two utilisations are added.
3. **Bearing node**: an X-joint through the chord to the saddle. The saddle is structural (a bare stiffener is too
   weak); fit it with a gap ≤ 2 mm and centre it under the vertical.
4. **Flange splice**: DG24 5.4 (Eqs 5-5 to 5-13).
   - a = b ≥ 38 mm. Dimension both.
   - Report the **governing** utilisation; the plate usually governs, not the bolts.
   - Check wrench clearance from the bolt to the weld toe.
   - Use one plate for every splice.
5. **Slotted tube with a knife plate** (DG24 5.3, Ex 5.2). Check:
   - bolt shear;
   - bearing and tear-out;
   - knife plate yield and rupture;
   - the tube net section at the slot (slot = tp + 2, U = 1 when l ≥ 1.3D);
   - tube wall shear along the four slot welds;
   - the slot welds;
   - the gusset on **both** chords, with Qf from the chord force (K2.1).
   - The gusset is offset by its thickness so the knife plate and the diagonal stay on the truss plane. Say which
     face (DSC p.157).
6. **Minimum splice capacity**: 25 % of the chord yield strength. Compression is by contact.
7. **Local strengthening at a moment connection** (user rule, 2026-10-04: "separate top part of column and join to
   bottom part with end plate connection ... keep top part with flange thicken on both").
   - When a column flange is too thin for a knee or beam end plate, do not thicken one flange with CJP butt splices
     in the field-length member. Make the connection zone a separate **shop piece** (a column head) with **both**
     flanges thickened, and join it to the member by a bolted end-plate splice.
   - Design the splice for the member forces at its level (take the forces at the upper end of the analysis
     element that holds it, or interpolate with a stated reason). Use the bolt size of the connection above, so
     the head has one bolt size.
   - Place the splice so that there is bolting room (200 mm from the top of the splice plates) below **every**
     plate above it: the end plate outside the flange and the continuity plates inside, which follow a sloping
     haunch flange down to the far flange.
   - The thickened flange must run at least s = ½√(bf·g) past the outer bolt row of the connection (DG4 yield
     line).
   - The head gets its own mark (CH1, CH1A where it carries other fittings); the column below becomes one mark for
     both column lines.
   - Example: SPF CS1 / CH1, `calc_spf.design_joints` (SPF-ST-5001 detail 1 and view D, SPF-ST-3001).
8. **A post running through a truss** (the truss chords cut onto the post faces; user, 2026-10-06: "extent post 50 mm
   above top chord edge for welding area then move purlin on top of post beside instead")
   - The post stops **50 mm above the top of the top chord**, so the chord-end fillet all round has a face to land on
     at the chord crown; the open top is closed by a cap plate with a seal weld (S6.7).
   - The chord ends are square cut onto the post face, fillet all round sized to develop the chord wall (S6.1).
   - The purlin of that line cannot sit on the post: it stands **beside the post**, flange edge on the post face
     (post half width + half the flange off the node), on the down-slope side where the chord continues, else on the
     side that has chord. The whole purlin row moves, on the plan too.
   - Check the post wall under the chord force (face plastification) and the width: a chord wider than the post
     cannot be cut onto its face.
   - Example: BANWA2 S-205 details 6, 7 (`plans/post_joints.py`), `model_data.purlin_rows`.

## S8. Bolts and anchor rods

1. **Bolt lengths**: grip + washers + nut + 3 threads, rounded up to 5 mm (`bolt_length`).
   - List them in a field bolt table with counts per truss, holes, washers, tightening and threads N/X, plus 2 %
     spare of each size (DSC p.233-236).
   - **No lock washers on high-strength bolts.** Lock with double nuts (DSC p.97 #52).
2. **Holes** = bolt + 2 mm unless noted, in a general note. Avoid one-bolt structural connections (DSC p.94 #14).
3. **Grades**: keep one grade per diameter where possible (DSC p.95 #45).
4. **Anchor rods** (DSC Ch. 7)
   - Headed (nut plus plate), because the rods resist uplift.
   - Projection = grout + plate + washer + 2 nuts + 3 threads.
   - Set by template.
   - Oversized holes to AISC Manual Table 14-2 (M20: Ø33), with plate washers sized to cover the hole or slot.
   - Pin end: the washers are site-welded after setting, so the rods take the shear.
   - Sliding end: the washers are loose and the double nuts snug.
   - Levelling nut on every rod; grout after the frame is plumbed and braced.
   - Levels: underside of base plate = bearing level BL; top of concrete = BL − grout.
5. **Base plate plan**: the edge distance, rod spacing and overall size in both directions. The plate and washer marks.

## S9. Erection notes (1001)

1. **Stability**: say that the truss is not laterally stable alone. Keep it braced until the purlins, roof bracing and
   fly braces are complete, and apply no roof load before that (AISC 303 7.10).
2. **Lifting**
   - Ground assembly, matchmarks aligned, bolts pretensioned, then lift as one piece.
   - Use a spreader beam at the nodes.
   - Give the lifting weight from the bill.
   - No lugs are welded to the tubes. A long truss can buckle sideways during the lift (DSC p.205).
3. **Sequence**: fix the pin end first, then the sliding end with the rods centred, then grout.
4. **No other site welding** without the engineer.

## S9A. Fly bracing (Beca SE-1505 "Fly bracing and purlin details" + AISC 360-16 Appendix 6)

Source: the office standard sheet `G:\My Drive\##Workset_Autocad\400 Standard Details\400 Standard Details\20 -
STEELWORK\SE-1505 Fly Bracing and Purlin Details` (Beca, 2015). Summarised in `SOURCES_STEEL_DETAILING.md` Part E.
Applied on SRT-ST-5004.

1. **Design.** A fly brace is a nodal brace of the compression flange or chord (360-16 App. 6.2). Check:
   - strength: Prb = 0.01 Pr, taken along the brace as Prb / cos F;
   - stiffness: βbr = (1 / 0.75) · 8 Pr / Lbr, against the brace's horizontal stiffness EA/L · cos² F;
   - slenderness: a single angle with **KL/r_z ≤ 200**.
   - The calc picks the lightest angle that passes (`calc_truss.fly_brace`). SRT: L 60 x 60 x 5, KL/r 184; the
     first issue's L 50 x 50 x 5 failed at about 220.
   - Fly braces belong to the steelwork, with their own mark (FB1), a row in the member schedule, and bolts in the
     field-bolt table. Only the purlin is by others.
2. **Geometry** (Beca details A / G):
   - Use both braces, symmetrical about the member.
   - The **gauge lines meet at a work point on the member centre line**, below the member.
   - The angle **F is measured from the purlin**. Connect at the end of the purlin lap if F is then 35° – 55°;
     otherwise F = 45°.
   - Draw the work point, both gauge lines (grey chain) and the F dimension.
3. **Connections** (Beca schedule):
   - **Member end on an I-section**: a **cleat plate ("B") each side of the web at the inside flange**, welded to the
     web and the flange (5 mm fillets both faces, the web-flange corner clipped), each brace bolted flat on its cleat
     with one bolt; not a lug under the flange (user, 2026-10-10, markup of SPF 2/5003: "improve fry bracing detail").
     - The gauge lines meet on the member centre line at the outer face of the inside flange.
     - The angle's end is square and clear of the web and the flange by 10 mm; the bolt sits at 25 mm end distance,
       with the cleat edge distances checked.
     - The cleat is in front of the web in the section, hidden where the angle covers it.
     - Calc: `calc_spf.fly_cleat` (bolt shear, tear-out on the angle and the cleat, edges, welds). Worked example:
       SPF 2/5003 (rafter 350 x 200, L 50 x 50 x 5, cleats PL 10 x 97 x 100, 1-M16 8.8/S).
   - **Member end on a CHS**: a lug, one transverse plate under the chord, its top profiled to the tube and welded
     both sides.
   - **Purlin end**: 2 bolts through the purlin web; in the lapped zone, 1 bolt plus the lap bolt.
   - Bolts are 8.8/S (snug); M16 for light members, M20 for heavy rafters or trusses (Beca schedule rows).
   - Confirm the brace holes with the purlin supplier.
4. **Purlin cleat** (Beca detail C):
   - The cleat lies **parallel to the purlin web**, so a section along the truss shows it face-on with its two bolts.
   - Cleat thickness by its length "A": 0 – 250 mm → PL 8; 250 – 350 mm → PL 10; 350 – 450 mm → PL 12; over 450 mm →
     an angle, or a plate plus a 75 x 10 stiffener.
   - Bolts are 2-M12 4.6/S, or 2-M16 for 300 mm deep purlins.
5. **Drawing the angle**:
   - It is seen on its flat leg: heel and toe edges, the outstanding leg's thickness line at the heel, and the gauge
     line through the bolts (`angle_strip`).
   - Its ends are square.
   - Where it is broken, it gets a break line.
   - The lug behind it is hidden where the angle covers it (`hide_under`).
6. **Presentation** (Beca sheet SE-1505):
   - The fly bracing gets its own sheet:
     - the arrangement section across the member (1:20 / 1:25);
     - the two ends at 1:5 / 1:10 (lug end, purlin end), called up from the section with dashed detail callouts
       (S4.10);
     - a **fly bracing schedule** (Table 6: mark, location, angle "A", lug "B", bolts "C" at each end, F, design
       force);
     - notes.
   - Mark the braced nodes on the elevation or plan (open triangles, mark FB1), and put a cutting plane through one
     of them pointing to the arrangement section (1/5004 from 3001).
   - On the arrangement section the purlin is named on its own band (S4.4); the cleat note sits in a row above the
     view, reached by one vertical leader.

## S10. Checks before issue (DSC Ch. 8 and the error list p.237-243)

The build enforces a clean layout (exit code 1 on any `!!`). Before sending a set, also check:
- every chain adds up;
- every piece is in a bill;
- one weight figure is used;
- no repeated marks;
- every weld has a symbol and a size;
- slopes and angles are not reversed;
- cutting planes exist for every section;
- bolt lengths and washers are given;
- the anchor rod hole and washer suit the setting tolerance;
- the camber diagram is present;
- there is no field-weld flag without a site weld;
- paint is kept 50 mm clear of site welds;
- the K3.1A limits are reported and met;
- the calc and the drawing quote the same governing utilisation;
- plates on tapered or sloping faces follow the face, with square ends and bolts (S2.9);
- every bolted splice has bolting room to all the steel above and below it, inside and outside the member (S7.7);
- every steel section in a table is followed by its weight per length, from the same function as the bill (S3.8);
- the bill covers all the structural steel and its totals by section agree with the analysis model (S1.6);
- every key section gives the post start level and every span bubble names the sheet of its elevation (S4.12);
- every detail callout resolves to a detail on the sheet it names (S4.10, SYMBOLS.md rule 3);
- joints from a concentric model: e per type, gaps, β and the K3.1A limits tabulated, and the joint strength checked on
  the current forces or listed as open (S2.10);
- posts through a truss: 50 mm above the top chord, capped, the purlin beside the post (S7.8).

## S11. Where it is implemented (SRT)

| Rule | Code |
|---|---|
| K3.1A limits, e cap, gap relax | `calc_truss.joints`, `_layout`, `g_abs`, `E_MAX`, `G_MIN`, `G_ABS` |
| Weld zones and legs | `calc_truss.dihedral`, `branch_weld`, `weld_leg`, `leg_std`, `j24_min` |
| Splice, knife plate, support, bolt length | `flange_splice`, `loose_diagonal`, `support`, `bolt_length`, `l_end_req` |
| Marks | `srt_engine._web_marks`, `CHORD_MARK`, `CHORD_LEN` |
| Symbols and graphics | `drafter/steel.py`: `weld`, `weld_region` / `weld_band` / `weld_bead`, `cutmark`, `chs_break`, `break_point`, `chs_section`, `hole`, `slot`, `bolt_side`, `place_tag` / `tag`, `detail_callout`, `wp_mark`; `srt_engine`: `chord`, `branch`, `weld_branch` / `branch_zones` |
| Fly braces | `calc_truss.fly_brace`, `FB_*` constants, `ANGLES`; `srt_sheets._fb`, `angle_strip`, `hide_under`, `cross_section`, `fb_lug`, `fb_purlin` |
| Leader engine | `td_engine.LEADER_ORTH`, `ORTH_RISE`, `ORTH_LEG_MIN`, `BOLT_RING_K`, `WRAP_UNITS` (`drafter.fonts.wrap(keep_units=True)`) |
| Views and tables | `srt_sheets`: `node_detail` (set-out, symbols), `branch_weld_detail`, `camber_diagram`, `bearing_elev`, `anchor_rod`, `base_plans`, `loose_conn` (`behind`), tables 1-6 |

BANWA2 (steel roof on an RC frame, outside the repository: `...61005 BANWA 2\Drafter\plans`, see `jobs/README.md`):

| Rule | Code |
|---|---|
| Truss marks per support span (S3.7) | `model_data.truss_spans`, `sub_truss_spans`, `component_sections` |
| Weight per length (S3.8), bill (S1.6) | `model_data.unit_kg`, `sect_w`; `bom.bill`, `roof_area`, `model_check` |
| Key sections, elevations, adjacent spans, callouts, levels (S4.10, S4.12) | `truss_details.key_section`, `truss_elev`, `neighbours`, `drawn_instance`, `callout_nodes`, `level_grey`, `best_spot` |
| Joint geometry and welds (S2.10, S6) | `calc_joints.nodes_of`, `e_type`, `k31a`, `branch_weld`, `web_welds` |
| Joint details, post joints (S7.8) | `joint_details.joint`, `weld_zones`, `joint_rows`, `weld_rows`; `post_joints.post_joint` |
| Purlins beside the posts (S7.8) | `model_data.purlin_rows`, `POST_TOP_ABOVE_TC` |
