# Steel detailing sources: AISC Detailing for Steel Construction, AISC Design Guides 21 and 24 (extracts)

Working extracts behind the steel drawing rules in `STEEL_DETAILING_INSTRUCTION.md` and the steel roof truss set
`jobs/steel_roof_truss` (SRT-ST). Reviewed 2026-10-03.

- Part A: AISC, *Detailing for Steel Construction* (3rd ed.), Ch. 3 - 4 (connections, truss connections, good
  practice, marks, welding, weld symbols). File `C:\Users\Peerapat\Downloads\Documents\Detailing_for_Steel_Construction.pdf`.
- Part B: the same book, Ch. 6 - 8 and Appendices A and D (erection drawings, anchor rods, trusses, camber, field bolt
  summary, detailing errors, checking).
- Part C: AISC Design Guide 21, *Welded Connections - A Primer for Engineers* (2006).
- Part D: AISC Design Guide 24, *Hollow Structural Section Connections* (2010).
  Files under `G:\My Drive\##Textbook\AISC Design Guide\AISC - Steel Design Guides 2016\`.

Page refs are **PDF pages** of each file (each part states its printed-page offset). Everything is paraphrased; no
passage is copied. US values carry metric equivalents where useful. The books are written against AISC 360-05 and
AWS D1.1:2004 - the current numbers are noted where they moved (AISC 360-16: K2 plate-to-HSS, K3 HSS-to-HSS truss
joints, Table K3.1 round / K3.2 rectangular; AWS D1.1:2015 Clause 9 / 2020 Clause 10 tubular).

Two items were checked directly in the codes on the drive and are quoted from there, not from the books:
AISC 360-16 Table K3.1A limits (also printed as DG24 Table 8-1A, p.104: **0.4 <= Db/D for gapped K-joints**), and
AWS D1.1:2015 Fig 9.10 / Table 9.5 (fillet-welded tubular T-, Y-, K-joints: heel / side / toe legs, Z loss).

---

# Part A. Detailing for Steel Construction - Ch. 3 and 4 (PDF pp. 42-133)


Working extract for the SRT (steel roof truss T1) drawing set. All page references are **PDF page numbers**
(book folio = PDF - 41 for Ch.3, e.g. book 3-45 = p.86; book 4-1 = p.94). Everything is paraphrased. US
values are given with an approximate metric equivalent in brackets where useful. The book is US practice
(ASTM A325/A490, AWS D1.1, AISC 360-05 era). Where a value is US-specific, apply the equivalent Thai/ISO
rule.

Read method: text pulled with PyMuPDF for all 92 pages, and every figure-heavy page viewed as an image
(Fig. 3-16, 3-43, 3-47, 3-48, 3-49, 3-50, 4-8, 4-12, 4-20 to 4-30, 4-34, 4-35).




#### 1. Fasteners: types, designations, behaviour (pp.42-49)

- High-strength bolts come in two grades, A325 (carbon) and A490 (alloy Q&T), from 1/2 to 1-1/2 in diameter
  and generally up to 8 in long. Type 1 is plain and Type 3 is weathering. An order that does not state the type
  may be filled with either (p.42).
- F1852 twist-off "TC" bolts are the tension-control equivalent of A325. Other alternative-design fasteners are
  allowed under RCSC 2.8 (p.42). A307 "common" bolts are rarely used now (p.42).
- Designations: **-N** means threads are included in the shear plane, **-X** means threads are excluded, and
  **-SC** means slip-critical. It is the same physical bolt in each case; the letter only records the design
  assumption. Common practice is to design as N, so nobody has to control thread position on site (pp.43, 46).
- If threads must be excluded (X), the thread inside the grip must be shorter than the thinner outside ply. The
  detailer has to give explicit installation instructions on the erection drawings, and may need a longer bolt
  plus an extra hardened washer under the nut (p.48). A325 bolts no longer than 4d are threaded full length
  (p.48).
- **Snug-tight** means the plies are in firm contact, reached with a few impact-wrench blows or the full effort
  of a worker with a spud wrench. Burrs that stop the plies seating must be removed. Paint, oil and galvanizing
  are allowed on faying surfaces of bearing joints (p.48).
- **Slip-critical** joints are designated by the engineer of record (EOR) in the contract documents. Typical
  cases: fatigue or load reversal, oversize holes, slots loaded roughly along the slot, and bolts sharing load
  with welds on one faying surface. Faying surfaces must be clean, with no lubricating coating, or blasted and
  coated with a qualified paint. Galvanized faying surfaces must be wire-brush roughened (p.48). Bearing must
  still be checked (p.49). A slip-critical joint only prevents slip at service load. It costs appreciably more
  because of the faying-surface preparation (p.43).
- The faying surface is the plane of contact between two plies. Surfaces under heads, nuts and washers are
  not faying surfaces (p.43).
- **Stitch bolts** carry no calculable load. They hold parts together and seal edges against moisture.
  Maximum spacing is per AISC J3.5 (pp.43-44).
- Bolt bearing strength depends on the connected material (its Fu), not on the bolt. Where plies have
  different Fu, check each (p.46).
- **Edge distance** is measured in the direction of force from the centre of a standard hole (AISC Table J3.4).
  It is increased per J3.5 for oversize or slotted holes, and J3.5 also limits the **maximum** distance to an
  edge, to keep moisture out (p.47).
- Combined shear and tension is typical at the end connections of bracing diagonals (Fig. 3-5). Shear and
  tension are checked by interaction, not combined as a resultant (p.49). Avoid countersunk heads on bolts in
  tension (p.49).
- Preferred pitch along a line of bolts is 3 in [75 mm] (p.50).

#### 2. Forces in welds, size and length limits (pp.57-65)

- A fillet weld is always designed for shear on its throat. The effective area is 0.707 x leg x effective length
  (pp.58-59).
- LRFD strength is phi Rn = 0.75 x 0.60 FEXX x 0.707 w l. For E70 this is about **1.392 kip/in per 1/16 in of
  leg** (ASD 0.928). Metric equivalent for E49: about 156 N per mm of length per mm of leg (p.60). Table 3-1
  tabulates sizes from 1/8 to 1 in (p.61).
- A transversely loaded fillet gets the (1 + 0.5 sin^1.5 theta) increase (p.62).
- **Minimum effective length is 4 x the leg**, otherwise the effective size is at most L/4. Intermittent
  increments must be at least 1-1/2 in [38 mm] (p.60).
- **Maximum fillet along an edge**: if the material is under 1/4 in [6 mm], the leg may equal the thickness. If it
  is 1/4 in or more, the leg is t - 1/16 in [t - 2 mm], unless the drawing says "build up to full throat". The
  reason is that the edge melts down and rolled toes are rounded (p.60, Fig. 3-18; p.110 Fig. 4-12a/b).
- **Minimum fillet (Table 3-2, p.62)** is set by the thinner part joined:

  | Thinner part | Minimum leg |
  |---|---|
  | to 1/4 in [6 mm] | 1/8 in [3 mm] |
  | over 6 to 13 mm | 3/16 in [5 mm] |
  | over 13 to 19 mm | 1/4 in [6 mm] |
  | over 19 mm | 5/16 in [8 mm] |

  Welds must be single-pass. The weld never needs to exceed the thinner part unless the calculation requires it
  (p.61).
- To develop a plate's tension (A36, E70), the total weld is about 0.97t, which is 0.48t per line with two
  lines. Yield governs rather than rupture (p.62).
- The Whitmore width is Lw = 2 l tan30 + d. Also check shear yield and shear rupture of the base metal along the
  toe and heel of each weld line, and block shear (pp.62-63).
- Shear lag: when only part of the section is connected, U < 1 and the l/d limit applies (AISC D3.3) (p.63).
- CJP groove welds with matching filler are as strong as the base metal. A splice between unequal parts is no
  stronger than the weaker part (p.65).
- PJP strength: compression where finished to bear, 0.60 FEXX on the throat; compression not finished to bear,
  0.90 FEXX; shear or tension normal to the axis, 0.60 FEXX. The effective throat E depends on process, groove
  angle and preparation depth S (AWS D1.1 3.12 / AISC Table J2.1) (p.65).
- Welds larger than **5/16 in [8 mm] need more than one pass**. Avoid them where possible (pp.68, 69).
- **End returns**: return a fillet about 2 x the leg around the top of a seat or angle. The return is not
  counted in the effective length (pp.67, 69).
- **Do not wrap welds** around the end or corner of material: the corner melts into a notch and the full throat
  cannot form (Fig. 3-26, p.70-71). Fillet welds on **opposite sides of a common plane are interrupted at the
  corner** (Fig. 3-25, p.70).
- Single-plate shear tab weld is 3/4 x tp, so the plate yields before the weld. Do not wrap it around the plate
  ends (p.71). For a flexible single-angle or tee weld, weld the toes and the bottom with a return at the top;
  do not weld across the whole top (p.72).
- Where bolts and welds are combined, the design drawings must say so clearly (AISC J1.8, J1.10) (p.72).

#### 3. Clearances, setbacks, shims (pp.52-54, 74-78, 93, 97)

- A beam is normally stopped about 1/2 in [13 mm] short of the support face (setback). Detailers allow for
  about 1/4 in [6 mm] underrun (pp.52, 54).
- Top-angle clearance: 1/8 to 1/4 in, or 1/4 to 3/8 in when the top fitting is shop attached (pp.74-76). Vertical
  slots in a field-bolted top angle remove the need for shims (p.76).
- Knife connection (both angles shop-attached to the support): about 1/16 in erection clearance. With
  high-strength bolts, **shims are required where the measured gap exceeds 1/8 in [3 mm]** (p.76).
- Cumulative shortening of beams in a line must not shorten the building. Shims or slotted holes take up the
  difference (pp.51, 76).
- Shrinkage of a field groove weld is about 1/16 in [1.6 mm] perpendicular to the throat. Compensate by adding
  1/8 in to the centre-to-centre of end holes, or with slotted erection holes (pp.82-83).
- **Shims** (p.93, Fig. 3-50) come in two kinds:
  - **Strip shims** have punched round holes and are cheaper.
  - **Finger shims** have open slots and can be inserted sideways without removing erection bolts. Fully
    inserted, they may be used in slip-critical joints, provided they have the same surface preparation. They
    are not counted as a ply, because they lose less than 25% of the contact area.

  Shims are supplied for simple connections, PR/FR connections, **column base plates** and splices. A
  **filler** sits where load passes across a gap and must be developed per AISC J5 (p.93).
- General allowance: about **1/2 in [13 mm] for shop clearance** and **3/4 to 1 in [19-25 mm] for field
  clearance**, depending on the framing (p.97 #53).

#### 4. Column splices and bearing (pp.83-86)

- Design drawings must show the size, number and arrangement of splice fasteners or welds. The erector supplies
  any special erection forces (p.84).
- Members **finished to bear** may transfer load in bearing. A physical splice is still needed for erection
  stability, moment, net uplift, or construction loads before bracing (p.84).
- Milled bearing strength: phi Rn = 0.75 x 1.8 Fy Apb (p.84). "Milled/finished" means brought to a true plane
  by milling, sawing or similar (p.84).
- Unfinished "pack" fillers are set back at least 1/4 in from the finished end and need only nominal
  attachment (p.85).
- Butt plates are typically 1-1/2 to 2 in. Assume a 45 deg spread of load through the plate. Both faces must be
  flat and true (AISC M2.8) (pp.85-86).
- Groove-welded splices are usually PJP bevel or J. **Erection lugs** hold alignment; they are temporary and the
  construction documents may require their removal (p.84, Fig. 3-40).

#### 5. HSS columns (p.86)

- Connections to HSS are like those to W shapes, except that connection material (angles, seats, shear tabs) is
  normally **shop welded to the HSS**. Beam end plates are field welded to HSS columns. Welded connections suit
  HSS well (pp.66, 86).

#### 6. Truss connections (pp.86-93) - the most relevant section for T1

**Design-drawing duty**
- When trusses are used, the design drawings must **show the truss joint details or give enough information
  for the joints to be designed and detailed**. The book cites AISC Manual p.13-11 (p.86).
- The **truss support connection should be shown on the design drawing** because of its importance (p.91).

**Joint labels**
- Joints are labelled U0, U1, L1, L2, and so on (upper and lower panel points) for convenience on the design
  and example drawings. This is not usually done on the shop drawing of a truss that is fully shop assembled
  (p.86).

**Working points and working lines**
- The **gravity axes of the web members intersect on the neutral axis of the chord** (p.86, Fig. 3-43a).
- Recommended practice is that **all gravity axes meet at one common working point (WP)** at each joint
  (p.88).
- Moving a member off the WP (for example to clear a bracing connection) creates eccentricity and chord moment.
  Small eccentricities may be neglected because the joint is stiff, but **critical eccentricity needs the EOR's
  approval** (p.88).
- Figures 3-43, 3-48 and 3-49 (pp.87, 91-92) show the conventions:
  - the WP is marked with a dot or cross;
  - each member's working line is a chain line through the WP;
  - member ends are located by a dimension along the member axis from the WP;
  - the slope of each member is a **bevel triangle**: run 12 and its rise, e.g. 12 / 9-3/16;
  - k-distances, the neutral axis of the bolt group, and a "horizontal line through W.P." are shown;
  - member size is followed by its **design force in parentheses**, e.g. "2L4x3-1/2x3/8 (170k)".

**Truss-to-column joint**
- With the WP on the column centreline (Fig. 3-48), the gusset, its connection and the chord carry the
  eccentric moment, shared by stiffness.
- Moving the common WP of all three working lines to the **column face** (Fig. 3-49) removes the moment from
  the gusset and connection and saves material. The column then takes the eccentric load, which the EOR must
  check (pp.91-92).

**Web member end details**
- One web member at each joint is carried to the edge of the chord fillet (k) to stiffen the truss. Welds run
  along the heel and toe, starting at the member end (p.86).
- More weld at the heel than at the toe is customary, but balanced welds are permitted (AISC J1.7) (p.86).
- Weld the member ends too if there is clearance (p.86).
- Prefer **square-cut ends** on web members and bracing, because clipped ends add layout and cutting cost.
  Do not swing a member off the WP just to get a square end (p.88).

**Minimum connection strength**
- To cover handling, shipping and erection loads, a common requirement is to design each connection for **at
  least 50% of the member's strength**, or a lower amount set by the engineer. The worked example checks yield
  on Ag and rupture on Ae = U An (pp.86-88).

**Weld amount**
- Lengths may be scaled from the joint drawing if it is drawn accurately to **at least 1 in = 1 ft (1:12)**.
  Otherwise deduct at least 1/2 in from the scaled length (pp.88-89).
- Three working methods are given: force per length available; assume a size and solve for length; or count
  total inches of 1/16 in weld and then split it between size and length (p.89).
- **Material length available must be at least the effective weld length + 2 x the leg**, so the weld can start
  and stop at full size (p.89).
- The chord stem and gusset must also be checked for tension yield, shear yield and shear rupture (p.89).
- Minimum fillet is governed by the thinner part (p.88). The maximum along an angle toe of 1/4 in or more is
  t - 1/16 in (p.88).

**Single-angle webs (light trusses)**
- Single-angle webs give eccentricity out of the truss plane, which the engineer allows for (p.89).
- Put all the single-angle webs **on the same side** of the chord. Staggering them twists the chord, C x e - T
  x e (Fig. 3-46, p.89).
- Purlins placed off the panel points bend the top chord, which is why the chord section in the example is
  larger (p.89).

**AWS joint numbers in the tail**
- Prequalified AWS D1.1 joint designations (e.g. B-U2, TC-L4b) may be placed **in the tail** of the weld
  symbol. The root opening and groove angle are then not repeated (p.89, Fig. 3-47).

**Welded chord splices (pp.89-90, Fig. 3-47)**
- Tension chord splices are usually CJP groove welds.
- Where thicknesses or widths differ, the transition slope is **no steeper than 1 in 2-1/2**, and flatter is
  preferred. Clip the corners and slope the weld face; chamfer the thicker part if needed.
- Splicing tee or W shapes by CJP needs the web cut back for backing bars or back-gouging, plus **extension
  bars** so the full flange width is effective.
- Shapes with flanges over 2 in, or built-up sections with plates over 2 in, that carry primary tension need
  CVN-tested material (A6 S30/S5). Such splices are generally made with splice plates instead (pp.89-90).
- Tension splices are checked on the net section. Whether the access hole is left open or filled is the EOR's
  call (p.90).
- **Chord splices are expensive and should be avoided wherever possible** (p.90).
- **Field chord splices** in shop-welded, field-bolted work use material that is either bolted both sides or
  shop welded on one side and field bolted on the other. Their design is an engineering task (p.91).

**Bottom chord at the support (pp.92-93)**
- Under load the tension chord lengthens, compression members shorten, and **camber is partly or wholly
  lost**. The tension chord of a square-ended truss pushes into its end connection.
- Options:
  - shop-attached connection with **erection clearance plus shims** to fill after loading;
  - **slotted holes** where the end panel carries no computed force;
  - normal hole clearance for small, light spans;
  - reaming for slightly larger misalignment;
  - field welding or field drilling for large movement. These are expensive; avoid them.
- **Estimate the movement as delta = PL/AE for each panel** (E = 29,000 ksi [200 GPa]). Do this for each
  panel on one side of the centreline and **sum the panels to get the movement at the truss end** (p.93).

#### 7. Good detailing practice (Ch.4 list, pp.94-97) - numbered as in the book

**Presentation**
- #1: A **shipping piece** is main material alone or with attached detail material (p.94).
- #2: Near-identical shipping pieces may share a sketch only if the differences are minor and notes do not
  clutter it (p.94).
- #3: Lettering must be neat. Notes must not run into the sketch or its dimensions. **General notes go near the
  title block.** Small letters about **3/32 in [2.4 mm]** and **numbers about 5/32 in [4 mm]**, i.e. figures
  larger than letters. Size and weight follow importance. Notes should be terse and **positive rather than
  negative**. The shop reads drawings in poor light (p.94).
- #4: Text is horizontal, vertical, or parallel to a sloping member, and **reads from the bottom or the right**
  (p.94).
- #5: Give special notes for anything not covered by dimensions or standards. An extra view or section beats
  many notes (p.94).
- #6: Line contrast: light dimension lines, bold object lines (p.94).
- #7: **First dimension line about 5/8 in [16 mm] from the object, then about 3/8 in [10 mm] between lines**
  (p.94).
- #8: Imperial format, e.g. 1'-2 1/2 (not used here).
- #9: **Arrowheads touch the extension line and do not cross it.** Dimension so as to avoid misinterpretation
  (p.94).
- #10: **Sections look to the left or toward the bottom of the sheet**; avoid looking up or to the right
  (p.94).
- #11: **Section views keep the orientation of the cutting plane and are not rotated 90 deg** (p.94).
- #12: **Never cross-hatch elements of sectional views** (p.94).
- #13: **Detail anchor rods, base and setting plates, grillages and embedded items first** (p.94).
- #14: **Avoid one-hole structural connections**, except for rod bracing (p.94).
- #15: **Re-entrant cuts** (copes, gusset notches) are drawn with the **radius shown** (p.94).
- #16: Each shop drawing lists the **erection drawings** where its members are located (p.94).
- #17: Main member lengths need not be drawn to scale; breaks are fine (p.94).
- #18: Ends and edges to be finished are marked **"FIN"** (p.94).
- #19-20: Angle and channel gauges are given from the backs of legs and webs; detail angles looking at their
  backs (p.94).
- #21-23: Detail concrete-filled HSS separately if subcontracted; wood holes may be noted rather than
  dimensioned; check with the fabricator before mixing member types on one sheet (pp.94-95).

**Marks, bills of material, ordering**
- #24: **Every piece of detail material carries an assembly mark** (p.95).
- #25: **Any difference means a different assembly mark** (p.95).
- #26-27: Check material against the advance bill. Verify that sizes and lengths are available; very long
  pieces may need splices; extra-wide plate may not exist (p.95).
- #28: Avoid Universal Mill plate, whose edges may be rounded or wavy (p.95).
- #29: **Order plate to be bent so the bend line is perpendicular to the rolling direction** (p.95).
- #30: **Every assembly mark is billed at least once in the shop bill.** On a repeat, the mark and quantity are
  enough (p.95).

**Beams and columns**
- #31-40 (pp.95-97):
  - give out-to-out and in-to-in dimensions;
  - project sections off the web looking down the column;
  - give angle separation in sixteenths;
  - **extension figures** (#35-36): see section 8.

**Bolting and welding**
- #41: Keep holes on the same gauge lines and **avoid more than one hole size in a web or flange** (p.95).
- #42: **Never write the word "weld" as a symbol.** Every welded joint gets the proper AWS symbol (p.95).
- #43: **Never weld more than needed.** It adds cost and distortion; more weld is not a better joint (p.95).
- #44: Show the weld detail **once for each different assembly piece and once on each shipping piece** (p.95).
- #45: **Do not mix bolt grades of the same diameter.** Use a different diameter for each grade (p.95).
- #46: Where appearance matters, put the bolt heads on the exposed side and add a conspicuous note (pp.95-97).
- #47: Fillets on opposite sides of a common plane are **interrupted at the corner** (p.97).
- #48: **Do not wrap or return fillets around the ends of material** (p.97).
- #49: Avoid shop bolting and shop welding on the same piece; shops separate the two areas (p.97).
- #50: **Use fillet welds wherever possible** (p.97).
- #51: Use **PJP instead of CJP** where the EOR accepts it (p.97).
- #52: **Never use lock washers on high-strength bolts** (p.97).

**Shop, field and clearances**
- #53: Shop clearance about 1/2 in; field clearance 3/4 to 1 in (p.97).
- #54: Make sure there is access to connect to existing work (p.97).
- #55: **OSHA requires shear studs to be welded in the field**; leave the top flange unpainted (p.97).
- #56: Anticipate field adjustment with slots, oversize holes, shims, or field welding where existing steel is
  uncertain. The weldability of existing steel must be verified (p.97).
- #57: Members that could go in upside down: **ask the erector whether to mark "TOP"** (p.97).
- #58: Check that bolts can be **entered and tightened with the installation wrench**, especially on skews. TC
  bolts need more clearance than conventional HS bolts (p.97).
- #59: **Include fastener projection** in erection clearances (p.97).

#### 8. Dimensioning conventions (pp.87-95)

- **Extension (running) figures**: cumulative dimensions from one definite point (the finished bottom of a
  column, or the left end of a beam or girder) locate every connection. Fitters set out from that point and
  inspectors check with a tape.
- The dimension line to the **first** connection must **run unbroken to the origin**. Alternatively, use a short
  left-pointing dimension at the origin labelled **"RD"** (running dimension) (p.95 #35).
- Running figures to web holes are never put on the same line as those to flange holes (p.95 #36).
- Truss joints are dimensioned from the WP along working lines. Member slope is a bevel triangle (12 and its
  rise). Fittings and member ends are located from the WP (pp.87, 91-92).
- Weld length is given in inches on the symbol (mm on our sheets). The default is the full length between
  abrupt changes of the joint (p.120).

#### 9. Tolerances (p.97, also pp.51, 76, 132)

- Mill tolerances are in AISC Manual Part 1 ("Standard Mill Practice"). Shop and erection tolerances are in
  the **AISC Code of Standard Practice**, Manual Part 16 (e.g. section 6.4.1 for framing length, p.51).
  Built-up welded members follow AWS D1.1 (p.97).
- Mill and shop tolerances are absorbed with slotted holes, or by setting lengths so small gaps are left for
  shims (p.97).
- **AESS tolerances** (p.132):
  - fabricated straightness is **one-half the standard ASTM A6 camber and sweep**;
  - erection plumb, level and alignment tolerances are **one-half** of normal;
  - open joints have a uniform **1/8 in [3 mm] gap**, or reasonable contact if shown without a gap;
  - exposed welds are smooth and uniform;
  - no marks on exposed weathering steel;
  - delivery and handling avoid distortion.

#### 10. Sheet numbers and marks (pp.97-98)

- **Sheet numbering**:
  - consecutive from 1;
  - with shipping divisions or sequences, the division is part of the number: division 1 is 101-199, division 13
    starts at 1301. A division holds at most 99 sheets;
  - a long truss on drawing 10 that needs three sheets is numbered **10A/C, 10B/C, 10C/C**.
  - There must always be an **easy cross-reference between shop and erection drawings** (p.98).
- **Shipping/erection marks** follow the fabricator's system. Common forms:
  - drawing number + piece id, e.g. **1B1** (beam B1 detailed on sheet 1);
  - piece letter + sheet suffix, e.g. A3, B3 (sheet 3), for small jobs;
  - tier buildings may add tier, floor, sequence and derrick location (p.98).
- **Assembly marks** are given to all detail material except bolts, nuts, washers and small fasteners. They may
  be:
  - a single letter, restarting at "a" on each drawing; or
  - two letters, where the first says what the part is (framing angle, seat, stiffener, base plate, cap plate,
    plate) and the second runs a, b, c....

  **Letters considered suitable: a, b, c, d, f, g, h, k, m, n, p, t, v, w, x.** The others are avoided because
  they are easily confused. Marks go on the templates and the parts. **Identical parts carry the mark forward**
  from the first drawing where they appear (p.98).

#### 11. Right- and left-hand details (pp.98-102)

- Mirror ("handed") pieces are called Right/Left or Thus/Reverse when they are identical but opposite hand, and
  As-shown/Opposite-hand when they also differ in some fittings or holes (p.99).
- Many fabricators now **restrict this shortcut**. It saves drawing time but **raises the risk of shop errors**,
  and CAD can just as easily draw the other hand as its own piece (p.98).
- Where it is used:
  - an unsymmetrical fitting on the right-hand piece gets a superscript **R** (e.g. aaR); on the left-hand piece
    it is billed as **L** (aaL);
  - two mirror fittings on one piece are marked R and L;
  - symmetric fittings get no R/L;
  - quantities of handed fittings are even, half R and half L;
  - fittings needed on only one hand are drawn right-hand and noted (pp.99-102).

#### 12. Detailing economy (p.102)

- Use **standard connections** and **job standards**: repeated connection material is detailed once on separate
  sheets with standard assembly marks and copied by mark (p.102).
- **Do not cross-note to the point that the drawing becomes a puzzle.** Avoid notes that refer to other notes;
  revising a sketch repeated "by note" is a frequent source of error (p.102).
- **Sub-assembly detailing**: repeat work is detailed once for a run of identical members, then finishing
  details are done per piece. Use it only with the shop's agreement (p.102).

#### 13. Bolts on drawings (pp.102-104)

- Identification head marks: Fig. 4-7 (p.103).
- **Shop bolts** are called out with type, diameter and length. **Field bolts** are specified by general or
  special notes on the **erection drawings** (pp.102-104).
- **Conventional bolt symbols** (Fig. 4-8, p.104):
  - shop bolt, hex or square head: open symbol with a circle and diamond;
  - countersunk shop bolts: near side or far side;
  - **field bolts: filled black dot**, with countersunk variants near side or far side;
  - in section, a field bolt is drawn as a solid shank.
- **Standard hole = bolt diameter + 1/16 in [M20 -> 22 mm per AISC J3.3M].** Oversize and slotted holes need EOR
  approval. Maximum sizes are in AISC Table J3.3/J3.3M (p.104).
- Holes for other trades should, as far as possible, be **the same size as the structural holes** (p.104).
- Holes for **anchor rods** are covered in Chapter 7, which is outside this extract (p.104).
- **Pretensioning methods**: turn-of-nut, calibrated wrench, twist-off TC, and direct tension indicator. Bolts
  are snugged first, then pretensioned (p.104).
- **Shop and erection drawings must show clearly the number and position of washers**, especially special
  washers for slotted holes and bevelled washers for non-parallel faces (RCSC section 6) (p.104).

#### 14. Welding - general, prequalification, processes, electrodes (pp.104-109)

- Welds transfer shear, tension and compression, stitch parts together, and seal contact edges (p.104).
- **Tack welds are not shown**; the shop decides, unless the specifications forbid them. **Temporary shipping
  welds used instead of bolts must be dimensioned and spaced on the drawing** (p.104).
- **Prequalified joints** meet AISC and AWS D1.1 in design, material and workmanship. Joints that are not
  prequalified need qualification by test (p.105).
- Every weld needs a written **WPS** (p.105). A welder's qualification lapses after **6 months** without using the
  process (p.105).
- Prequalification alone does not make a joint suitable. Consider load, thickness, access and position,
  process, distortion and **restraint**. Through-thickness shrinkage in highly restrained joints can cause
  **lamellar tearing** (Fig. 4-9) (p.105).
- Welded details have reduced fatigue strength; use gradual transitions (pp.105-106).
- **Processes** (pp.106-108):
  - SMAW (stick): shop and field;
  - SAW: flat and horizontal only, deep penetration, fast;
  - GMAW: all positions, needs wind screens in the field;
  - FCAW: less wind-sensitive;
  - EGW: vertical, up to 3 in;
  - ESW: vertical, up to 20 in, low distortion;
  - stud welding: **studs are field-welded only, per OSHA** (p.108);
  - resistance welding: joists.
- **Electrodes**: E70XX (A5.1/A5.5), F7XX-EXXX (SAW), ER70S-X (GMAW), E7XT-X (FCAW). "70" means 70 ksi
  [about 490 MPa] minimum tensile strength (pp.108-109).

#### 15. Weld types (pp.109-114)

**Fillet welds**
- A fillet weld has a nominally right-triangle section. The size is the leg; the throat runs from the root
  perpendicular to the face (p.109).
- For a **curved fillet** (e.g. around a tube), the effective length is measured **along the centreline of the
  throat** (p.109).
- The included angle of the deposit may range from **60 deg to 135 deg** (Fig. 4-12). For prequalified
  **skewed tee joints**, the dihedral angle is **60 deg minimum and 135 deg maximum** (Fig. 4-12c/d, p.110).
  When the angle is well above 90 deg, compute the throat from the actual geometry (p.109).

**Groove welds** (p.109)
- Nine types: square, single and double V, single and double bevel, single and double U, single and double J.

**CJP** (p.110)
- Full fusion through the joint, welded from both sides or onto backing or a back weld.
- The **root is gouged to sound metal** before the second side is welded.
- The throat equals the thinner part.
- CJP is costlier to make, inspect and repair than PJP.

**PJP** (pp.110-111, 124-125)
- Used where full strength is not needed or only one side is accessible.
- **Minimum effective throat (AISC Table J2.3, p.124)**, set by the thinner part:

  | Thinner part | Minimum effective throat |
  |---|---|
  | to 1/4 in | 1/8 in [3 mm] |
  | over 1/4 to 1/2 in | 3/16 in [5 mm] |
  | over 1/2 to 3/4 in | 1/4 in [6 mm] |
  | over 3/4 to 1-1/2 in | 5/16 in [8 mm] |
  | over 1-1/2 to 2-1/4 in | 3/8 in [10 mm] |
  | over 2-1/4 to 6 in | 1/2 in [13 mm] |
  | over 6 in | 5/8 in [16 mm] |

- **Effective throat (Table J2.1, p.124)**:
  - SMAW, GMAW or FCAW, any position, with J or U or a 60 deg V/bevel groove: equals the groove depth.
  - SAW, flat position, with J or U or a 60 deg bevel or V: equals the groove depth.
  - GMAW or FCAW, flat or horizontal, with a 45 deg bevel: equals the groove depth.
  - **SMAW any position, or GMAW/FCAW vertical or overhead, with a 45 deg bevel: groove depth minus 1/8 in
    [3 mm].**
- The contract documents give the effective throat E and effective length. **The shop drawing gives the groove
  depth S and geometry**, and some fabricators show both S and E (p.125).
- PJP is not recommended under dynamic or cyclic load (p.125).
- **Intermittent PJP ends are faired at 45 deg minimum** (Fig. 4-29c, p.125).

**Flare welds** (pp.111-112)
- Convex groove faces, such as rounded corners or bars. The effective throat is per AISC Table J2.2, and
  penetration is hard to achieve. Welding reinforcing bar requires knowing its chemistry (A706, AWS D1.4).

**Plug and slot welds** (p.113)
- Proportions per AISC J2.3b (Fig. 4-17).
- **Fillet welds inside holes or slots** are different from plug and slot welds; a slot is preferred over a round
  hole. If the effective area exceeds the hole area, the plug and slot rules govern (p.114).

#### 16. Welding positions and economy (pp.114-115)

- **Positions**: flat (face about horizontal, welded from above); horizontal (horizontal axis); vertical;
  overhead (p.114).
- **Flat is preferred.** A 5/16 in manual fillet takes about **50% longer in the horizontal position**, and
  **vertical or overhead welds can take about 3 times as long** as flat. SAW is flat only (p.114).
- The shop turns work or uses positioners. In the field, plan joints for flat or horizontal welding, e.g. face
  up with backing below to avoid overhead work (Fig. 4-19) (p.114).
- **Cost goes with the square of the leg, strength with the leg.** A 5/8 in fillet uses 4 times the metal of a
  5/16 in fillet for twice the strength, so **prefer smaller, longer welds**. Cost is controlled around the
  5/16 in [8 mm] single-pass limit (p.115).
- Double-sided grooves use less weld metal than single-sided, except on thin edges. Bevels and Vs are
  flame-cut and cheap; J and U grooves need gouging or planing (p.115).

#### 17. Welding symbol grammar (AWS A2.4; pp.115-126, Fig. 4-20 to 4-28)

**Parts** (p.115, Fig. 4-21)
- **Arrow** to the joint, **reference line** carrying the data, **basic weld symbol** (device), and optionally a
  **tail** for references.
- The tail is **omitted when no reference is needed** (Fig. 4-20 note, p.116).

**Tail contents** (p.115, Fig. 4-22)
- Electrode specification (e.g. E7018), process (e.g. ESW), joint detail note ("Note A"), or an AWS or
  fabricator **joint designation** (e.g. B-U2-GF, TC-L4b, B110).
- Electrode or process in the tail is needed only when more than one class or process occurs on the drawing;
  otherwise it belongs in the general notes.
- With an AWS joint number in the tail, the root opening and groove angle need not be shown (pp.89, 123).

**Arrow side and other side** (pp.115-117)
- The device **below** the reference line means the weld is on the **arrow side**. **Above** the line means the
  **other side**. A device on both sides means both sides.
- "Other side" means the other side of the **joint**, not the far side of the assembly (p.117).
- **Only one symbol per joint** on a shop drawing (p.117).

**Drawing rules** (p.117)
- The reference line is horizontal, or vertical reading from the bottom.
- Data reads left to right, like other notes.
- The arrow may leave either end, up or down, at about **45 deg**.
- **The arrowhead is never on the reference line or its straight extension**; there is always an angular break.

**Fillet device** (pp.115, 116)
- An isosceles right triangle with one leg on the reference line. The **perpendicular leg is always on the
  left**, whichever way the arrow points (this also applies to bevel, J and flare-bevel symbols).

**Order along the reference line** (Fig. 4-20 note, p.116)
- **Size, weld symbol, length, pitch, read left to right**, regardless of arrow position or line orientation.
- Size goes left of the device and length right of it, **on the same side of the line as the device** (p.117).

**Both sides** (p.117)
- **Both the arrow-side and other-side sizes must be shown, even if they are equal.** This is the 1976
  change; older drawings may show only one (Fig. 4-24d).
- Arrow-side and other-side welds are the same size unless shown otherwise (p.116).

**Unequal-leg fillets** (p.117)
- AWS has a notation for them, but fabricators prefer a **dimensioned cross-section sketch** (Fig. 4-24e).

**Standard size by note** (p.120)
- "ALL FILLET WELDS 5/16 UNLESS NOTED" lets the size be omitted on the symbols except where it differs.

**Length** (p.120)
- **No length means full length between abrupt changes** in the joint outline toward which the arrow points.
- One arrow applies to that segment only. Use multiple arrows, from either end of the line, for several
  segments (Fig. 4-24f).
- Partial-length welds are located by dimensions (Fig. 4-25), or by placing arrows at abrupt changes so no
  dimensions are needed (Fig. 4-24l) (p.121).

**Weld-all-around** (p.120)
- An open circle at the arrow/reference junction. The device is drawn as the **arrow side**.
- **Do not use it indiscriminately**: it causes excess weld and distortion.
- **Do not use it where the whole perimeter cannot be reached**, or where it would wrap a corner and break the
  rule on opposite sides of a common plane.

**Intermittent welds** (p.121)
- Shown as **length - pitch** (pitch is centre to centre on one side), e.g. "2-6".
- Economical only when the **pitch is more than 2 x the length**.
- **Chain** welds have the triangles directly opposite; **staggered** welds have them offset (Fig. 4-24j).
- A full increment is placed at each end of a run.
- Mixed continuous and intermittent welding: Fig. 4-24k. Hand processes only.

**Obscured joints** (paired stiffeners, double angles, gussets either side of a web) (pp.116, 121-122)
- A symbol for the near-side joint also applies to the coinciding far-side joint, **provided the marking or
  billing shows the far-side piece exists**. The fabricating-industry convention in the Fig. 4-20 note says
  far-side welding duplicates near-side welding when the bill shows a far-side piece.
- Where near and far welds differ, use a **dual welding symbol** with the **piece marks in the tails**
  (Fig. 4-26d).

**"TYP" in the tail** (p.122)
- Several identical pieces welded the same way take one symbol with "Typ" in the tail. An exception gets its
  own symbol (Fig. 4-27), or a different assembly mark plus its own symbol.

**Skewed square-edged plate with a gap** (p.122)
- The fillet size is the design size **plus the gap**. If the gap is too large, use PJP or another joint type.

**Groove symbols** (pp.122-124, Fig. 4-28)
- Square, V, bevel, U, J, flare-V, flare-bevel, and back (back weld or backing).
- The vertical leg of **bevel, J and flare-bevel is always on the left**.
- For unsymmetrical preparations (bevel, J), **the arrow points to the member to be prepared**, emphasised by
  an **extra break in the arrow** (Fig. 4-20, Fig. 4-24m). For symmetric preparations the arrow has no extra
  meaning (Fig. 4-24n).
- All-around works for grooves too, e.g. a tube butt (Fig. 4-24o/p).
- **Back weld** symbol on the opposite side of the line (Fig. 4-24p). CJP made by SMAW, GMAW or FCAW requires
  gouging the root to sound metal before the back weld (p.123).

**Groove dimensions** (p.123)
- **CJP size is not shown**; it is understood to be the full thickness, unless the double groove is
  unsymmetrical or the weld is partial (then size, Fig. 4-24r).
- **Root opening** goes inside the device near the root (Fig. 4-24s).
- **Included groove angle** goes inside the device, on both sides if both are prepared (Fig. 4-24t).
- **Groove radius** of J and U welds is not on the symbol; cover it by standard or sketch.
- **Groove weld length is never on the symbol** (edge to edge is implied), and intermittent grooves do not exist.
- **Thickness or width transitions** (1 in 2-1/2 maximum; for unequal widths, 2 ft radius tangent) are drawn as
  sketches, not by symbol (Fig. 4-24u/v).

**Contour and finish** (p.123, Fig. 4-24w)
- **Flush** (straight line) or **convex** (arc) contour symbol over the device, with a finish letter: **G**
  grind, **M** machine, C chip (fabricator's letters). Flush or convex with no letter means no finishing
  operation.

**Backing and spacer** (p.123, Fig. 4-24x/y)
- The backing symbol is a rectangle on the opposite side. Remove backing **only if the specifications
  require it** (e.g. fatigue).
- Backing material must meet AWS D1.1. Spacer bars are the same material as the base metal and are gouged out.
- **Backing and spacer bars are identified and billed** on the drawing.

**Extension (run-off) bars** (p.123, Fig. 4-24z)
- They continue the groove beyond the edges, matching its geometry. Backing is extended too. They may need to
  be cut flush afterwards.
- **Shop** extension bars follow the shop's own practice. **Field** extension bars must be detailed and supplied
  to the erector.

**Combined symbols** (p.123, Fig. 4-24aa)
- Groove + fillet + back weld + contour may be combined. **Avoid elaborate symbols**: unless they refer to AWS
  prequalified or fabricator standard joints, **draw a dimensioned cross-section** instead (pp.123-124).

**PJP symbols** (pp.124-125, Fig. 4-29)
- **S(E)**: preparation depth S, with the effective throat E in parentheses, to the left of the device.
- A square groove shows only (E).

**Stud symbol** (p.126)
- A circle with an X, arrow side only. Size on the left, pitch on the right, number in parentheses below. In
  plan, studs are shown with an X so they are not mistaken for holes.

**Plug and slot symbol** (p.126)
- A rectangle. Arrow side and other side indicate which part has the hole.
- Plug size is the hole diameter, in **odd sixteenths** to suit standard punches. Slot size is by detail
  reference.
- The weld is completely filled unless a fill depth is shown inside the device; a flush contour may be added.
- Do not use plug or slot symbols for large openings that should be fillet welded around the inside.

**Field weld flag** (p.126, Fig. 4-24ll/mm)
- A small black flag at the arrow/reference junction. Its **point is toward the basic weld symbol**, i.e.
  **toward the tail** (Fig. 4-20 note).
- It may be combined with weld-all-around.
- **Field weld symbols appear only on erection drawings** (or site-alteration sheets), never on shop drawings,
  because the shop does not act on them. **All edge preparation for field grooves is done in the shop** and is
  detailed on the shop drawings.
- Older drawings used a large black dot, before the 1976 change to the flag.

**Symbol size** (p.115)
- Symbols must be **large enough to be recognised easily**. Templates exist.

#### 18. Nondestructive testing symbols (pp.126-127, Fig. 4-30)

- AWS D1.1 requires **visual inspection of all welds**. Specific welds needing NDT (e.g. a tension butt splice)
  are identified **on the shop detail drawings** with symbols (p.126).
- **Methods**: **PT** dye penetrant, **MT** magnetic particle, **RT** radiographic, **UT** ultrasonic, **VT**
  visual (p.126).
- **Elements** (Fig. 4-30a): reference line, arrow, letters, test-all-around circle, tail with
  specification/reference, and number of tests in parentheses.
- Arrow-side and other-side meaning is the same as for weld symbols. Letters **on the line** (centred) mean
  no side significance (p.127, Fig. 4-30b).
- **Combined with the weld symbol** on the same arrow (Fig. 4-30c), e.g. "MT" over a fillet, "UT" over a V, or
  "VT + RT".
- **Extent**: a length after the letters (e.g. "MT 9 in"), a **percentage** (e.g. "MT 25%"), or a dimensioned
  sketch (Fig. 4-30d/e/f). **No extent means the full length** of the weld (p.127).

#### 19. Painting (pp.127-128)

- The contract documents must state:
  - which members are painted;
  - surface preparation;
  - paint specification and the manufacturer's product;
  - **minimum dry film thickness of the shop coat**;
  - members left **unpainted** (for concrete, sprayed fireproofing, etc.) (p.127).
- Surface preparation is deemed accepted unless rejected before priming. The shop coat is for adhesion and
  weathers quickly, so long exposure leads to repair. The fabricator is responsible only for the specified
  preparation and shop coat; field touch-up belongs to others (pp.127-128).
- Preparation is referenced by SSPC codes (SP2, SP3, SP6, ...). Each shop drawing says whether painting is
  required, often in a **paint/cleaning block near the title block** (p.128).
- **Paint omissions**:
  - **Slip-critical faying surfaces (uncoated class)**: no paint within one bolt diameter, and **not less than
    1 in [25 mm], of any hole edge**, nor anywhere inside the bolt pattern. Typical note: "No paint within 1 in
    of perimeter of bolt hole group". Coated SC surfaces need a Class A or B qualified paint (p.128).
  - **Within 2 in [50 mm] of any field weld** (AISC M3.5), and on stud-weld areas. Shop welds are unaffected
    because painting follows welding (p.128).
  - **Under sprayed fireproofing** (adhesion; UL) (p.128).

#### 20. Galvanizing (pp.128-132)

- Hot dip at about 840 F [450 C], roughly 2 oz/sq ft. ASTM **A123** for members and **A153** for hardware. All
  paint, oil, mill scale and slag must be removed first (pp.128-129).
- **Checklist** (p.129): identify the pieces; maximum size; bolted connections; welded connections; **seal
  welding**; galvanized bolts; **drain and vent holes**; field welding precautions.
- Detail galvanized pieces **on separate drawings** if possible; otherwise note "GALVANIZE" on each sketch. Put
  **"GALV" in the Remarks column** of the shop bill (p.129).
- Paint, crayon or chalk marks are removed by pickling. Instead, **stamp marks at least 1/2 in [13 mm] high and
  1/16 in [1.6 mm] deep**, using few characters, or attach **stamped metal tags** (p.129).
- Size the pieces for a **single dip**; double dipping costs considerably more (p.129).
- **Attachments are not bolted on before galvanizing**; they are dipped separately and shipped loose with galv
  bolts. **Holes are not enlarged** for galvanized bolts (p.129).
- Pickling acid can seep into welded joints and bleed out later, so **seal joints with continuous welds** and
  note "All welded joints on galvanized pieces to be sealed" (p.129).
- **Weld porosity in closed spaces can explode in the bath.** Avoid enclosed spaces. **Tubes closed by end plates
  need fill/vent holes at each end** (Fig. 4-34), sized per the galvanizer, and the detailer must show them
  (p.130).
- **Drain holes** are needed where zinc would pool: weld access ("mouse") holes at base and cap plates, and
  clipped stiffener corners (Fig. 4-35, 4-36) (pp.130-132).
- A325 Type 1 and A307 bolts may be galvanized; **A490 may not**. Nuts are tapped after galvanizing (p.132).
- **Avoid welding galvanized steel**, especially in the shop: the fumes are toxic and the zinc must be ground off
  and the area touched up. Repair methods: organic zinc paint, zinc solder, or metallizing (p.132).
- Warping in the bath is possible; repair or replacement is agreed between fabricator and galvanizer (p.132).

#### 21. AESS (p.132)

- Architecturally Exposed Structural Steel is designated in the contract documents. It must be **identified on
  the shop and erection drawings**. Joints that are meant to have a gap are detailed so the gap is achieved
  on site. The tolerances in section 9 above apply (CoSP section 10) (p.132).

#### 22. OSHA and erectability (pp.70, 97, 108, 133)

- OSHA (29 CFR 1926 Subpart R) covers fall protection, **minimum field connections before final
  bolting/welding**, openings, and material handling (p.133).
- **Two bolts** secure a beam to a seat (p.70). Shear studs are welded in the field (pp.97, 108).
- **Erectability**:
  - matching hole patterns at knife connections;
  - room to lower beams between column flanges;
  - avoid awkward shop-attached curb plates and similar parts;
  - check wrench access (pp.97, 133).

#### 23. Common errors to avoid (gathered from the above)

1. Writing "WELD" or "FILLET ALL ROUND" as text instead of an AWS symbol (p.95 #42).
2. Giving only one size on a both-sides symbol (pre-1976 habit) (p.117).
3. Arrowhead on the reference line or collinear with it (p.117).
4. Using all-around where the perimeter cannot be reached, or where it would wrap a corner (p.120, #47-48).
5. A field flag on a shop drawing, or a flag that does not point toward the tail (p.126, Fig. 4-20).
6. A bevel or J symbol without the arrow break pointing to the prepared member (p.122).
7. Putting a groove weld length or intermittent dimensions on a groove symbol (p.123).
8. Elaborate combined symbols where a dimensioned section would be clearer (pp.123-124).
9. The same mark on pieces that differ in any way (p.95 #25).
10. Cross-noting puzzles and notes that refer to other notes (p.102).
11. One-hole structural connections (p.94 #14).
12. Mixing bolt grades in one diameter (p.95 #45).
13. Lock washers on HS bolts (p.97 #52).
14. Washers or slot washers not shown (p.104).
15. Cross-hatched steel in sections, or sections rotated or looking right (p.94 #10-12).
16. Moving members off the WP without EOR approval (p.88).
17. A weld length shorter than effective length + 2w of available material (p.89).
18. Ignoring the chord elongation and camber loss at the truss bearing (pp.92-93).
19. Painting faying surfaces of SC joints, or the zone within 50 mm of field welds (p.128).
20. Closed tubes galvanized without vent holes (p.130).

---

# Part B. Detailing for Steel Construction - Ch. 6 to 8, App. A and D (PDF pp. 146-314)


Working extract for the SRT (steel roof truss T1) drawing set. All text paraphrased; page refs are PDF
page numbers (p.NN), not the book's printed page numbers (printed = chapter-page, e.g. p.146 = 6-1).
Figures were looked at as images; Appendix A pages are scanned large-format sheets (rotated 90 deg).

Legend in Part 2: **[MUST]** = must fix / add before the set can be called shop-ready;
**[IMPR]** = improvement. **(D)** = belongs on the engineer's design drawings; **(S)** = shop
drawing information; **(E)** = erection drawing / field information.




#### 1. Erection drawings: purpose and content (Ch. 6)

1. Every shipping piece (a single member or a sub-assembly shipped as one unit) must appear on a
   drawing so the frame can be erected quickly and correctly. The erection drawing lets the erector
   find a piece's size, length, piece mark and place in the erection sequence (p.146).
2. Erection drawings are line diagrams (plan, elevation, section) carrying principal dimensions,
   erection marks, notes and, where needed, enlarged details, bolt installation requirements and
   field-weld requirements. They should be complete enough that the erector need not study the
   shop drawings to see how members fit together (p.146, p.149).
3. They are NOT meant to show the erection scheme, schedule, rigging, temporary supports or safety
   devices - those are the erector's (p.146).
4. Numbering: erection sheets usually prefixed E (E1, E101); anchor-rod / embedment sheets AR or EB;
   general arrangement sheet A1 on large jobs (gridlines, column splices, used to divide the job
   into sequences) (p.146, p.149).
5. The anchor rod plan, grillage plan and embedment plan are "embedment drawings" (items installed
   to receive steel). They may be combined on one sheet. Concrete trades need them early; anchor rods
   are often "deliver only" items for the fabricator (p.146).
6. Design drawings may be reproduced as erection drawings only with permission (COSP 4.3), and only
   if they print clearly, are at an adequate scale, carry no confusing extraneous information, show
   the extent of each shipping piece by line breaks, and do not identify the design firm. Not
   normally used for anchor-rod/embedment drawings (p.146).
7. Erection drawings should be prepared before detailing starts; they double as the "mark-off" set
   for tracking which pieces have been detailed (p.146, p.149).
8. Material by others attached to the steel is generally not shown; holes for other trades are not
   provided unless the contract documents require them (COSP 7.15) (p.149).
9. Erection drawings show the divisions/sequences into which the structure is split for shipping and
   erection (p.149).

#### 2. Erection drawing rules of thumb (p.149-150)

1. Scale: erection, anchor rod, grillage and embedment plans usually 1/8 in = 1 ft (about 1:100);
   details on them at a larger scale.
2. Anchor rod plans that also show other cast-in items must stay simple for concrete workers.
3. Typical erection drawings: floor/framing plans, roof plans, side and end elevations, **bottom chord
   bracing plans**, crane runway plans, plus sections and details.
4. Show compass north and project north on every plan, oriented as on the design drawings.
5. Elevations/sections: state the viewing direction ("looking east") or the gridline cut.
6. If clearances or details force an erection sequence, the erection drawing must state it.
7. If a supporting member must be shifted temporarily to erect another, say so in a note.
8. Exposed bolt heads side, AESS members: note conspicuously.
9. **Field adjustment: show the method of adjustment and the member's final location.**
10. Line weights: framing in heavy lines contrasting strongly with centre and dimension lines; leave a
    small gap where a member ends at the member it frames into (shows they are separate pieces).
11. Place each mark at the end of the member that corresponds to the marked end on the shop drawing.
12. Give the instructions for every field connection (bolting or welding).
13. Show the starting point of erection if required.
14. Asymmetric shapes (angles, channels): show/note orientation; locate channels to the back, not the
    web centreline.
15. Cut sections and elevations looking the same way wherever possible.
16. **General Notes must give the top-of-steel elevation, steel grade, field welding type, field bolting
    and washer criteria.**
17. Mill buildings: show typical cross-section with heights to bottom of trusses, purlin spacing in a
    roof section, girt spacing and openings, which way bracing shapes turn (p.150).
18. Tier buildings: TOS elevation by general note with exceptions given as +/- offsets; **never use
    ditto marks on plans - repeat every size** (p.150).

#### 3. Field instructions on erection drawings (p.150-151)

1. Field-connection notes go in the General Notes of the first erection sheet; later sheets refer to
   them or repeat them (repeat if a different construction phase) (p.150).
2. Bolts: identify by size, specification and type (e.g. 3/4 in A325-N); use "UN" (unless noted) and
   call out the exceptions where they occur (e.g. slip-critical joints). **If two bolt grades are used
   on one job, make them different diameters; otherwise mark exceptions boldly** (p.150).
3. If threads must be excluded from the shear plane, give a detail like the Manual's (see Fig. 7-81,
   p.236) on the erection drawings (p.150).
4. Avoid joints that need a particular bolt installation sequence; if unavoidable, give the sequence
   on the erection drawing (p.150).
5. Bolting notes must also cover galvanized bolts if any, installation method (snug-tight or
   pretensioned), pretensioning method (turn-of-nut, calibrated wrench, TC bolt, DTI) and washer
   requirements (hardened, plate, bevelled) (p.150).
6. Field welds: size and location by weld symbols, notes and details; field weld details must be on the
   erection drawings when shop drawings go for approval; electrode class in the General Notes of the
   first erection drawing; length need not be given if the full length is welded (p.150-151).
7. If members are deliberately fabricated long (e.g. +1/8 in for weld shrinkage), the erection drawing
   must alert the erector (p.151).
8. When space is short, special connection details may go on separate sheets (Figs 6-6, 6-7) (p.151,
   p.153).

#### 4. Marks and orientation (p.151-154, p.179)

1. Shops paint the erection mark on the **left end** of horizontal/diagonal pieces as detailed and at the
   **bottom** of vertical pieces; marks read right side up. The erection drawing places marks to match,
   so the erector can orient pieces from mark position alone (p.151).
2. Long girders and **trusses that cannot be turned on site** need a compass direction on the
   appropriate end so they ship pointing the right way (p.151).
3. Erection marks shown in bold lettering (p.154).
4. Figure 6-8 (p.154): marks like 101B1, 104D2 written along each member near its marked end; the
   position of the mark (left/right, near/far) tells the viewing direction used for detailing.
5. Figure 6-1b / 7-48b (p.148, p.207): "Assembly diagram for trusses" - a single line diagram of the
   truss with each component shipping piece labelled per truss type (HT1 for T1, HT3 for T2...; BC1,
   BC2...; H1, H2), member sizes along the lines, overall span, plus a **"Note to erector"**: marks
   are painted on the left end as detailed, erect so the mark is where the plan shows it, field
   connection bolt spec.
6. Column "Face A East" style compass marks when orientation is not obvious (p.179).

#### 5. Field-alteration drawings (p.154)

Show only enough of the existing member to locate the new work; locate by gridlines (old shipping
marks will not be visible); show the member in its normal position with view named ("ELEVATION
LOOKING NORTH"); existing material dashed, new work heavy; number FW1, FW104 etc.

#### 6. Temporary support and erection aids (p.154-157)

1. COSP 7.10: the contract documents must identify (a) the lateral-load-resisting system and the
   diaphragm elements that give strength and stability in the completed structure and (b) any special
   erection conditions required by the design concept (shores, jacks, loads to be adjusted to set or
   keep camber, position or prestress). The erector then designs and supplies temporary support
   (p.154-155).
2. If non-steel elements (deck diaphragms, walls) provide lateral resistance, the owner's construction
   representative must state when they will be in place (p.155).
3. Erection seats: clear the supported flange by 1/8-1/4 in; on the first-erected side only if the
   sequence is known (p.155).
4. **Lifting lugs** may be needed for columns, **trusses** and girders above a weight limit or where
   slings are impractical; the erector tells the fabricator what lug/pin/shackle is used so the detailer
   provides the holes or weldments (p.156-157).
5. Column alignment lugs: min 1/2 in plate, min 5/16 in weld, HS bolts, 1/8 in gap between lugs;
   centre-punch marks at column ends for alignment (p.157).

#### 7. Which side of a single plate (p.157, Figs 6-14, 6-15 p.159)

If a member can bolt to either face of a single plate, single angle or tee, the erection drawing must
show which side: a general note ("all beams to east and north faces unless shown") or a short tick /
L / T symbol beside the member at each joint. Alternative: paint stripe on the faying face, called
"STRIPE NS / FS" on the shop drawing (keep paint out of the slip-critical clean zone).

#### 8. Matchmarking (p.157-159)

Pieces too big to ship are split ("knocked down"), often shop-assembled for fitting or reaming; each
field splice is **matchmarked while assembled** so the field reassembles it the same way. Mark is
usually paint with a number (die-stamped if paint not allowed). On the erection drawing: **a diagram
of the whole member with every splice location and its matchmark ID, plus a short explanatory note**;
fix a standard location for the stamped mark on the job.

#### 9. Anchor rod / embedment plans and base plates (Ch. 7, p.160-177)

1. Foundation-related items in the fabricator's scope (anchor rods, leveling plates, base plates,
   grillages, embeds, lintels, curb angles) ship early and are detailed **on drawings separate from the
   rest of the job** (p.160).
2. The design drawing shows typical column base details (example Fig. 7-1c, p.163: elevation with
   finish level reference, grout space dimension, plate thickness t, rod diameter, embedment length,
   2 in typical edge distances, plate B x N, weld symbol to the column, nut welded at rod bottom)
   (p.160, p.163).
3. **Anchor rod plan content** (detailer's): looks like the foundation plan but gives everything for field
   placement - erection marks, **top-of-base-plate and leveling-plate elevations, grout thickness,
   projection of rods above top of concrete**. Elevations must be cross-checked with framing drawings
   and top of footing; column orientation must agree with the tiers above (p.160).
4. Base plates are normally shop welded to the column; preferred weld pattern avoids turning the
   member over (Fig. 7-2 b) (p.160, p.169).
5. **Top of rough concrete typically 1-3 in (25-75 mm) below the underside of base plate** for
   tolerance and grouting (p.160).
6. Leveling methods (p.160-172):
   - leveling plate, normally 1/4 in thick, same size as base plate, good up to ~24 in plates; holes
     standard size if it is also the setting template, or per Manual Table 14-2 if set over installed
     rods; set by the GC/foundation contractor (Figs 7-2c,d);
   - **four or more rods each with leveling nut + heavy washer under the plate**, upper nuts/washers
     after setting; washer stops the nut pushing into the oversize hole;
   - shim stacks (graded, deburred, possibly tack-welded) sized for the pre-grout loads (DG 10);
   - heavy loose plates: shims and wedges, or three-point leveling screws (rounded point, small steel
     pad) - screws/shims are not meant to carry the column; grout promptly after plumbing.
7. Large plates (min dimension about 36 in) need ~3 in grout holes near centre; not needed for dry
   pack (p.170).
8. Anchor rod setting templates (if in contract): 1/4 in plates big enough for the rod pattern, holes
   rod diameter + 1/16 in (p.170).
9. Clip angles for uplift set ~8 in up from the column end; stiffeners cut back ~1 in from the base
   plate for uplift transfer and drainage (p.170).
10. Shear at the base: friction (with the concurrent compression), shear through the rods, or a
    **shear lug in a grout keyway** (Fig. 7-5) (p.170, p.173).
11. **Hole sizes for anchor rods in base plates: AISC Manual Table 14-2**; the oversize holes must be
    covered by **plate (structural) washers sized for the force**; minimum washer sizes in the same
    table (p.170). [Table not reproduced in the book; Manual values from memory, verify: 3/4 in rod ->
    1-5/16 in hole, washer 2 in x 1/4 in; 1 in rod -> 1-13/16 in hole, 3 in x 3/8 in.]
12. Insert sleeves allow small horizontal adjustment; seal against freezing; post-installed wedge
    anchors must not be relied on for erection stability (p.173-175).
13. Base plate finishing (Spec M2.8): <= 2 in thick needs no finishing if bearing is satisfactory; 2-4 in
    straighten or finish; > 4 in finish; underside not finished when grouted. Unfinished base plates
    and leveling plates are noted **"Straighten"** on the shop drawing (p.173).
14. Thickness increments: 1/8 in up to 1-1/4 in, 1/4 in to 3 in, 1/2 in above (p.173). Holes over
    1 in diameter may be flame cut; drilling capacity ~1-1/2 in (p.173).
15. Shop details of base plates (Fig. 7-4, p.172): plate billed as "PL thickness x width x length ~
    mark" (BP1, M1 leveling plate) with "Straighten" under it; holes called out with the diameter in a
    **diamond hole symbol**; hole gauges as chain dimensions plus overall plate dimension in both
    directions; grout holes and lifting holes called out separately.
16. Anchor rods (p.173-175): preferred material ASTM F1554 (Gr 36/55/105); headed bolts stocked only
    to ~8 in, so rods are usually threaded rod with nut; **hooked rods must not be used to resist
    calculated uplift** (only to locate/prevent displacement); no hot bending of high-strength rods; a
    nut on a threaded rod used as the head must be welded so it cannot unwind (if the steel is
    weldable).
17. **Rod projection: length H above concrete must allow the rod to stick out a positive distance E -
    up to about 3 in - above the nut**, to absorb setting inaccuracy; thread length correspondingly
    longer than ordinary bolts (p.174-175, Fig. 7-6 shows E and H).
18. Anchor rod washers: round or square, hole 1/16 in over rod diameter, A36 plate, thickness suited to
    the force; required because of the large base plate holes (p.175).
19. Anchor rod shop detail (Fig. 7-7, p.175): rod may be drawn as a single heavy line, no thread
    symbols; dimension overall length, thread length, embedment/swedge or hook length; billed as
    "Rod dia x length - AR1"; washers detailed as "Bar 4 x 3/8 x 4 - W1 (Washers)" with diamond hole.
20. Embeds: located vertically by top elevation and horizontally to the plate centreline from a
    **working line (WL, usually a gridline)**; slots absorb wall misalignment (p.175-177).

#### 10. General shop-drawing conventions (columns/beams sections, p.177-203)

1. Columns drawn horizontal (bottom to the left) or upright (bottom at bottom); the finished end goes
   at the bottom/left (p.177).
2. Shop bill: preprinted form at right side above the title block or across the bottom (p.178).
   **General notes for the sheet in the lower right near the title block; special notes next to the
   detail** (p.178).
3. Faces/sections: transverse sections always looking toward the bottom of the column; sections
   projected directly from the cut where possible; cutting-plane symbols for isolated details (p.178-179).
4. Combining near-identical pieces on one sketch is acceptable but not for too many; prefer separate
   details over a crowd of exception notes (p.179).
5. Dimension placement (p.181): **overall dimensions and level-locating dimensions outermost**; detail
   dimensions (hole spacing, gauges) closest to the view; checker's figures in between. Extension
   dimensions are measured from a single datum (finished column bottom) even if the line is not drawn
   full length. **Hole spacing in a group is run continuously, not interrupted by edge distances.**
6. Repeated fittings need not be re-dimensioned on the same sheet, but hole spacing in the main member
   is always given (p.181).
7. Edge distances of fittings not shown if symmetric (p.181).
8. **Clearance dimensions** (between outstanding legs, splice plates, fills) are shown so the shop knows
   a fit is critical; tight ones noted "not more / not less" or with a +/- tolerance (p.181).
9. Identification block under the column sketch: mark, section, depth/flange/web data, direction mark,
   **lifting weight** if required (p.183).
10. Assembly marks: one letter per different fitting (a, b, c...) or two-letter system (aa, ab angles;
    pa, pb plates); omit i, l, o; same fitting = same letter on a sheet (p.183).
11. Notes: "CUT SQUARE", "NO PAINT" on faying surfaces of slip-critical field joints and near field
    welds; paint notes from the job specification (p.183).
12. HSS columns with shop base plates and open tops need a **drain hole** at the base (p.183).
13. Field-bolt tightening clearance: ~1-1/4 in from bolt centre for a 3/4 in impact wrench (Manual
    Tables 7-16/7-17 give entering and tightening clearances) (p.186, p.239).
14. Beams (p.188-195): minus "setback" dimensions at each end from the reference line (support
    centreline) to the steel end; the shop is given a length tolerance where possible; dimension to
    centrelines, backs of angles and backs of channels; vertical dimensions to top OR bottom, never
    both; **do not dimension to toes or flange edges**; dimensions should refer to points on the steel;
    long/overall dimensions farthest from the view; cross as few lines as possible; small distances
    may be exaggerated for clarity because dimensions govern, not scale (p.192-193).
15. **Ditto marks are never used on shop drawings; write "ONE", not "1", for a single shipping piece
    in the shop bill** (p.195).
16. Line up notes and dimensions that serve the same purpose (p.195).
17. Opposite-hand pieces are best detailed in full rather than "left of E3" (p.193).
18. **Extension (running) dimensions** from a defined origin at the left end (labelled RD) to every
    line or group of holes; the first one runs unbroken from the origin; milled/zero-tolerance end
    goes left; work points noted **WP**; groups within ~1 ft of an end connection are located from
    that connection, not only by extension figures (p.195-198).
19. General notes per sheet cover hole size, bolt size and paint once, with exceptions on details
    (p.193).
20. Views that carry no positive instruction are omitted (p.192).
21. Welding: a weld for a repeated assembly mark may be shown once with "TYP" in the tail - applies
    to that shipping piece only; electrode class noted (p.201). Welding and bolting are not combined in
    one connection plane except in special cases (p.200). OSHA: min 2 erection bolts (p.200).
22. Wall-bearing / sliding bearings: bearing plates set and grouted first; a detail permitting sliding
    while restraining other movement (Fig. 7-44, p.203); stability of the bearing end by anchorage,
    top-flange restraint or end stiffeners (p.203).

#### 11. Camber (p.203, p.209-210)

1. Camber = the amount a member is built above its geometric profile, **measured unstressed with the
   member lying on its side** (standard shop practice); positive = arch upward and assumed unless
   noted (p.203).
2. Beams: specified on design as "C = x"; on shop drawings as an ordinate at mid-length, note
   "Camber = x" below the sketch; curve not drawn; below 3/4 in impractical; holes square to flange
   (radial after bending) unless "holes normal to chord" is noted (p.203).
3. Trusses: camber compensates construction/loading deflection and **must be given on the construction
   documents**; industry practice: trusses under about **80 ft (24 m) are usually not cambered** (p.209).
4. Truss camber shape: smooth, flat, approximately **parabolic**, mid-span raised by the specified amount
   relative to the ends (p.209).
5. Trusses are **detailed in the flat (uncambered) position, but diagonal lengths and bevels are computed
   and dimensioned for the cambered geometry**. Worked example (Fig. 7-53, p.210): camber ordinates at
   each panel point drawn on an exaggerated vertical scale; a tension end diagonal comes out ~7/16 in
   shorter than in the flat truss; a compression-diagonal arrangement gets longer; bevels barely change
   (p.209-210).
6. Shop drawing note either "Camber has been figured in truss (dimensions)" or, if the shop adjusts,
   "Lengths of members to be adjusted by shop" under the camber diagram (p.209).
7. **The camber diagram must always be included with the truss shop details** so the fitter and
   inspector can check camber during assembly (p.209). Seen on A7-45 (p.256): "CAMBER DIAGRAM" with
   panel points L0-L4 and ordinates at each, note that camber is figured in the truss dimensions.
8. Purlins/girts attached to cambered trusses are detailed for the uncambered truss; end-wall wind
   columns connect with vertical slots (p.209).

#### 12. Trusses - construction and detailing practice (p.204-211)

1. Most building trusses are **shop welded, field bolted**; welded trusses save holes (gross-section
   tension) and gusset material (p.204).
2. **Working lines in welded trusses = gravity axes of the members** (centroids); in bolted trusses the
   gauge lines are the working lines (p.204).
3. Out-of-plane support of the top chord comes from deck/purlins/bracing; with purlins the unbraced
   length is the purlin spacing (p.204-205).
4. Unequal-leg angle orientation must be on the design drawing (LLBB / SLBB symbols) (p.205).
5. Erection marking (p.205, Fig. 7-48a p.206): each fully assembled truss gets one erection mark
   (T1, T2, T3) shown on top- and bottom-chord plans; component shipping pieces (half trusses, bottom
   chords, hangers, knee braces) are identified on the **assembly diagram**; trusses are assembled on
   the ground and field splices fully bolted **before lifting**.
6. Component shipping pieces are usually **detailed in their assembled position** (p.205).
7. **Jack-knifing**: ground-assembled trusses can buckle sideways when lifted, especially at the bottom
   chord splice and at the peak; stiffening angles (Fig. 7-50, p.208) or pick-point arrangement -
   extent decided by the erector (p.205).
8. Shipping piece criteria: stiff enough to handle, within shipping clearances, light enough for the
   cranes, erectable without interference, minimum field fastening (p.205).
9. Layout: first establish work points, compute WP-to-WP distances and bevels; draw an accurate scaled
   joint layout (separate layout sheet ~1-1/2 in = 1 ft, or on the shop drawing at ~1 in = 1 ft; do
   not scale material sizes from anything smaller); **main-member length = WP-to-WP distance minus the
   setbacks from each WP to the member ends** (p.205, p.208).
10. Symmetry/rotation: detail the left half only when halves differ only at the centreline (note the
    differences); a piece may be identical to its partner rotated 180 deg, or opposite hand - holes
    for bracing on one side only can force opposite-hand detailing; a truss may have to be rotated 180
    deg at one end of the building, shown by the truss mark position on the plan (p.208).
11. **Notes must be positive** ("Holes in HT2", "Cut on this line for BC1 and BC3"), never negative
    ("Omit holes for HT1"); refer to the shipping piece, not to the assembly piece (p.208-209).
12. **Truss dimensioning hierarchy** (p.209): working dimensions from the erection drawing (e.g. c/c
    columns) are repeated, placed conspicuously **outside all other dimension lines**; next inward, the
    dimension lines locating panel points and other reference points at working-line intersections;
    where the WP is off the shipping piece, dimension along the working line from the WP to a reference
    point on the piece, from which all detail dimensions are laid out.
13. Bottom (tension) chord **lengthens under load** and pushes on its end connections; compute the
    elongation (Manual Part 13) and provide slots in the support detail; the EOR decides when the
    bolts are tightened (example: 3/16 in each side of centreline) (p.209-210).
14. Stitch fasteners/fills for double angles: min two; within 2 ft of each end when the piece has field
    holes at both ends; welded fills equally spaced if not dimensioned (p.210-211).

#### 13. Observed sample truss drawings (Appendix A)

**Truss 105T6 (A7-45, p.256/275), welded WT-chord truss, half drawn:**
- Half truss drawn with "Sym. abt. CL except for wk and ha"; panel points labelled L0-L4 (bottom),
  U0-U4 (top).
- Bottom dimension strings: panel lengths chained (7'-11 1/4 each, end panel shorter), then half length
  31'-8 3/8, then outermost "62'-4 1/2 back to back of angles".
- Each web member labelled along its axis with quantity-section-length-mark ("2-L3x3x5/16 x 6'-9 1/2
  ~wd"), and its **WP-to-WP length in parentheses**, plus the slope triangle (12 : rise) and a
  dimension from WP to the member end (setback) so the shop can locate the cut.
- Top chord drawn separately above the elevation (plan of top flange) with purlin clips located by
  running dimensions; sections A-A, B-B, C-C; "Detail of pa" (gusset) fully dimensioned.
- Weld symbols with "TYP. B.ENDS" (both ends); corner clips "CLIP 2 1/2 @ 45 (TYP)".
- Lower left: **CAMBER DIAGRAM** with ordinates at L0-L4 and note "camber has been figured in truss
  dimension".
- Title "TRUSS 105T6" with **"Lifting wt = 3 Tons"**; general notes (spec, material, hole size unless
  noted, electrode, paint, "no paint on shop contact surfaces", holes marked "A" for HS bolts with no
  paint within 3 in, grind note); "REQUIRED" box: number, description, mark.
**Truss 110T3 (p.258):** full BILL OF MATERIAL at top: QUAN | MARK | DESCRIPTION | LENGTH (ft, in) |
  WEIGHT | MILL ORDER No | REMARKS; first line "ONE 110T3", then main members (ma, mb) and fittings
  (wa, wb, pa, pb...) with "2=R 2=L" remarks for hands; notes A/B; "No Camber" stated explicitly.
**Fig A7-49 (p.277), bolted half trusses:** half trusses HT1/HT2, bottom chords BC1, hangers H1, knee
  braces KB1 all drawn in assembled position on one sheet; quantities as "2-HALF TRUSSES - HT1";
  top chord "4@7'-10 3/8 = 31'-7 1/2 (WP/WP)"; outermost working dims "59'-0 c/c truss", "60'-0 c/c
  columns"; **R.D.** origins for running dimensions; positive notes "Holes in HT2", "Holes for HT1";
  general notes end with "Camber - None"; "Note: some fabricators would build HT1 & HT2 as shop welded
  assembly".
**Fig A7-51 (p.278), bracing:** pieces drawn in their installed relationship so shared intersection
  points/holes use one set of dimensions; each diagonal shows WP-WP length in parentheses, hole-to-hole
  length, bevel triangle; rods drawn as single lines; washers billed as fills.
**Design drawings A7-52 (p.257) and A7-66 (p.280):** cross-section line diagram of the truss with member
  sizes written along each member, **member forces** (and wind forces in brackets) on the members,
  "6 equal panels @ 7'-11 1/4 = 47'-7 1/2", camber value, elevations (EL. top of base plate), roof
  plan with north arrow and gridlines, sway frame and bottom-chord bracing plans, typical column
  base (base PL size, anchor rod dia, projection "Proj", grout, top of pier), general notes (spec,
  materials, shop welds E70XX, field bolts and the bolts-per-bracing-member rule).
**Column sheet (p.259):** shop BOM: QTY | MARK | SHAPE | LENGTH | WGHT | GRADE | REM, followed by a
  **FIELD BOLTS** block (count - dia - grade x length) on the same sheet; level (EL.) dimensions
  outermost; diamond hole callouts; "NO PAINT" and stripe symbols; identification block "ONE-COLUMN-
  C564-3" with section detailing dimensions.

#### 14. Bracing (p.211-223)

1. Lay out the bracing joints at the same time as the chords they connect to; loose gusset plates are
   marked for separate shipment (p.211).
2. Bracing length and bevel computed from WP coordinates (square root of the sum of squares) (p.211).
3. **Draw (pretension) of light single-angle tension bracing**: deduct nothing up to 10 ft, 1/16 in for
   10-20 ft, 1/8 in for 20-35 ft, 3/16 in over 35 ft; not for heavier shapes (p.215-217).
4. Double-angle bracing: no draw deduction; stitch fills mainly to keep the angles from "windmilling"
   in handling (p.217).
5. Field-welded bracing needs at least one fitting bolt per connection, or a **field assembly diagram**
   with dimensions to edges the erector can reach (Fig. 7-65) (p.221-222).
6. Gussets that help stiffen a truss splice during erection are better shop-attached to the truss than
   to the bracing (p.222).
7. Bracing rods drawn as line diagrams, no thread symbols; turnbuckle data standard (p.222-223).

#### 15. Roof framing (p.228-233)

1. Ridge purlins close to the peak; sag rods carried across the ridge (p.228).
2. Purlins acting as bracing struts marked **PS (purlin strut)**, otherwise P; HS bolts usually used
   for all purlin clips to avoid two bolt types/hole sizes (p.228-229).
3. Channel purlins usually erected flanges up-slope (erector preference) unless the designer wants
   them down-slope (p.230). Gable-end overhangs, eave strut alignment with girts (p.230-231).

#### 16. Field bolt summary (p.233-237)

1. Started when the final shop drawings are issued; prepared by the detailer from the shipping-piece
   drawings; on large jobs it is **the erector's only source** of bolt type, quantity, size and length
   (p.233).
2. Shop ships the quantities listed **plus 2 % of each diameter and length** (COSP 7.8) (p.233).
3. Ways to tell the erector which bolts go where: bolts shown at each joint on the erection drawing;
   bolts listed on the shop drawing of the supporting member; a point-to-point list (p.233).
4. Content (Figs 7-80a/b, p.234-235): line no., count, diameter, type/grade (A325N, A325-TC, A490,
   A307), length, head washer, nut washer type (hardened / bevelled), TC yes/no, remarks
   ("W/N & W" = with nut and washer; "with nut only"); header: job, order no., date, material, sheet.
5. Special installation (e.g. threads excluded) by notes or sketch on the erection drawings; Fig. 7-81
   (p.236) shows grip, ply closest to nut, minimum ply thickness to keep threads out of the shear plane
   (1/4 in for 3/4 and 7/8 in bolts, 3/8 in for 1 in, assuming one washer), stick-through zero minimum.

#### 17. Detailing errors checklist (p.237-243)

Dimensional: sum of chain dimensions not equal to the extension dimension; holes too close to fillets.
Bills of material: billed size/weight differs from the drawing; plate size billed differs from the
detail; piece billed larger than the stock ordered; wrong quantities of pieces.
Missing pieces: a piece without a shop drawing.
Welding clearance: electrode (14-18 in long, up to 3/8 in dia) needs room and the welder must see the
root; preferred electrode ~30 deg to the vertical leg; rule: clear distance from weld root to a
projection >= half the projection height; minimum "shelf" for SMAW fillets about weld size + 5/16 in
(3/16 fillet -> 1/2 in, 1/2 fillet -> 13/16 in) (Fig. 7-84, p.238); do not detail welds where nominal
dimensions leave only 1/8 in of surface (Fig. 7-85).
Bolting clearance: entering and tightening clearances (Manual Tables 7-16/7-17); projecting bolt heads
on the other side may block erection (p.239).
Field clearance: check members can be swung/tilted in (diagonal length vs opening); graphical overlay
method (p.239-242).
Other common errors (p.242-243): hole count mismatch with the supporting connection; wrong hole
diameter; flange gauges not fitting; connections omitted; copes missing/wrong; wrong steel grade;
wrong weld profile; **north arrow wrong or missing on erection drawings**; combining welds and bolts
improperly; **reversed slopes (especially near 45 deg)**; wrong presentation of right/left, as shown/
opposite hand; **wrong shipping marks on erection drawings**; missing bearing stiffeners; missing column
stiffeners/doublers; **paint where field welds go**; paint on members to be fireproofed or encased; **weld
symbols shown incorrectly**; paint on tops receiving field studs.

#### 18. Checking, approval and records (Ch. 8, p.244-251)

1. Advance bills checked for quantities, shape names, material description, lengths, finish needs,
   material spec, special requirements, and completeness against the contract documents (p.244).
2. **Shop drawing checker**: verifies connections against the design drawings, checks the shop bill,
   confirms clarity of presentation, confirms all contract steel is detailed, initials the drawing
   (p.244).
3. **Back-check**: the detailer reviews every checker mark, resolves disagreements, corrects, and
   returns for the checker's final signature (p.245).
4. Approval (COSP 4.4) by the owner's design and construction representatives; discrepancies in the
   contract documents reported immediately (COSP 3.3) - the detailer must report them but is not
   responsible for finding them; changes to connections notified before submittal; approval covers
   suitability of details and connection strength, but **dimension correctness and field fit stay with
   the fabricator** (p.245).
5. **Fit check** after issue to the shop: connections match, copes/gauges right, hole sizes/locations,
   clearances, overall lengths (p.245).
6. Records: logs of design drawings received (number, revision, date, status A preliminary / B bid /
   C mill order / D for construction), specs, every drawing issued/approved/resubmitted, transmittals,
   extras, back-charges, phone/email decisions (p.246-251, Figs 8-1, 8-2).
7. Revisions: contract documents dated and identified by revision; **each design drawing keeps the same
   number for the whole project regardless of revision**; revised areas enclosed in a cloud with the
   revision number in a triangle (some remove old clouds keeping the number, others keep all clouds);
   revision recorded by number and description near the title block; superseded prints marked VOID
   (p.246, p.249).

#### 19. Appendix A and Appendix D

- Appendix A (p.254-282) holds only large-format scanned sheets referenced from Ch. 7 (several pages
  are duplicates): beams (A7-34, A7-40), columns (A7-10, -11, -12, -16, -18, -19, -20), grillage
  (A7-8, p.265), trusses 105T6 / 110T3 (A7-45/46), design drawings (A7-52, A7-66), half trusses (A7-49),
  bracing (A7-51), crane girders (A7-69). No separate text on presentation; the conventions seen are in
  section 13 above.
- Appendix D (p.309-314) SI units: base units m, kg, s, deg C; prefixes M, k, m; stress in N/mm2 (= MPa);
  moments N-m; **round converted dimensions to whole millimetres**; metric bolts designated directly
  (M16, M20, M22, M24, M27, M30, M36) not converted from inches; E = 200 000 N/mm2, G = 77 000 N/mm2;
  conversion tables. Nothing else about drawing presentation.

---

# Part C. AISC Design Guide 21 - Welded Connections, a Primer for Engineers


Working extract and recommendations for the steel roof truss job (`jobs/steel_roof_truss`).

**How to read the page refs.** "p.NN" means the **PDF page** of the 162-page file. The printed page number is PDF minus 11
(for example p.48 is printed page 37). The guide is based on AISC 360-05 and AWS D1.1:2004. Clause numbers in D1.1 have
moved since then: tubular design was "Section 2 Part D" and is now Clause 10 (D1.1:2020), fabrication was Section 5, and
inspection was Section 6. Values in brackets [ ] are SI conversions or values from AISC 360-16 tables that the guide
cites but does not print. Those were added by me and are labelled.

The text extraction lost the AISC fraction font. I checked every fraction below against the rendered page image.


| Ch. | Topic | PDF pp. |
|---|---|---|
| 1 | Codes: AISC 360, AWS D1.1/D1.8/D1.3 | 12-14 |
| 2 | Processes (SMAW, FCAW, SAW, GMAW, ESW/EGW, GTAW, studs, cutting) | 16-41 |
| 3 | Welded connections: joints, CJP, PJP, fillet, plug/slot, details, filler strength, strength, special welds, symbols | 42-68 |
| 4 | Metallurgy: steel groups, weathering, Q&T, old steels, rods, bolts | 70-76 |
| 5 | Cracking: shrinkage/restraint, centerline, HAZ, transverse, lamellar | 78-89 |
| 6 | Distortion | 90-98 |
| 7 | WPS: prequalified vs qualified, variables | 100-105 |
| 8 | Weld quality: discontinuities | 106-111 |
| 9 | Inspection: VT, PT, MT, RT, UT | 112-116 |
| 10 | Seismic | 118-122 |
| 11 | Fatigue | 124-130 |
| 12 | Special: anchor rods, coated steel, heavy and restrained sections, **HSS**, AESS, shop vs field, existing structures, heat shrinking | 132-141 |
| 13 | **Engineer's role: contract documents, approvals, unexpected issues** | 142-149 |
| 14 | **Economy** | 150-157 |
| 15 | Safety | 158 |

---

## 1. EXTRACT

### 1.1 Governing documents and who does what

- AISC 360 J2 brings in all of AWS D1.1 except where AISC says otherwise. AWS D1.1 covers design of connections,
  prequalification, qualification, fabrication, inspection, studs and existing structures (p.12-13).
- **The engineer chooses the welding code** (D1.1, D1.3 for sheet, D1.8 for seismic, D1.5 for bridges). The guide treats
  this as the engineer's most important welding task, and it should not be left to the contractor or inspector (p.142).
- **The contractor's choices (means and methods):** welding process (p.16), groove weld type (bevel, V, U or J) and its
  dimensions (p.45, p.67), PJP depth of preparation S (p.46), and writing the WPSs (p.100).
- **The engineer's choices:** the weld type where it matters (for example "CJP only"), sizes, effective throats E,
  NDT, CVN, static or cyclic loading, and any special sequence (p.143-144).

#### What AWS D1.1 says the engineer must put in the contract documents (8 items, D1.1 Clause 1, p.142)
1. Code requirements that apply only when the engineer specifies them.
2. Any NDT beyond the code.
3. Verification inspection, if wanted.
4. Acceptance criteria other than the code's.
5. CVN requirements for weld metal, base metal or HAZ.
6. Whether the structure is statically or cyclically loaded (for nontubular work).
7. Any other requirement the code does not cover.
8. Responsibilities for OEM work.

#### What the design drawings must show (D1.1 2.2 "Contract Plans and Specifications", p.143)
- The base metal specification.
- The **location, type, size and extent of all welds**.
- Shop welds distinguished from field welds.
- Joints where a particular assembly order, sequence or technique matters (also D1.1 2.2.3, p.147).
- Special joint details, and any special inspection on specific joints.
- A prequalified joint detail only guarantees conditions for sound fusion. It says nothing about suitability for the
  application or about effects beyond the fusion boundary (p.102, p.143).
- **Tubular T-, Y- and K-connections:** D1.1 gives "Z-loss" dimensions (a function of process, groove angle and
  position) and a figure used to find the weld stress (p.143).
- For cyclic loading, give either full details including weld sizes, or the planned cycle life and the range of forces
  (p.143).

### 1.2 Joint types and weld types

- There are five joint types: butt, T, corner, lap and edge. The joint type does not imply a weld type (p.42).
- Weld categories are groove (CJP or PJP), fillet, and plug/slot. The **throat** is the theoretical weakest plane (p.42).
- **Table 3-1, which weld fits which joint (p.54):**
  - Butt: CJP or PJP.
  - T-joint: CJP, PJP, fillet, or a groove/fillet combination.
  - Outside corner: CJP or PJP.
  - Inside corner: CJP, PJP, fillet, or a combination.
  - Lap: fillet or plug/slot.
- **Table 3-2, choice by load (static only, p.55):**
  - T-joints in tension or shear: fillet when lightly loaded. When heavily loaded, use fillet, PJP, PJP+fillet or CJP.
  - Butt joints in heavy tension: CJP.
  - Compression with bearing considered: PJP.
  - Lap joints: fillet or plug/slot.

### 1.3 CJP groove welds (p.42-45)
- The throat equals the thickness of the joined part. A CJP develops the full strength of the joined material when
  statically loaded, so no weld calculation is needed. Writing **"CJP" in the tail** of the symbol is enough (p.43).
- CJPs are often specified where they are not needed. Longitudinal welds of built-up members loaded in shear are the
  classic case where fillet or PJP is cheaper (p.43). CJPs are the most expensive weld type (p.150).
- CJP is the only weld type whose full volume can be checked by RT or UT. Use one where volumetric NDT is truly wanted;
  otherwise prefer a cheaper weld with in-process VT plus MT or PT (p.43).
- Prequalified CJP details need steel backing if welded from one side, or backgouging if welded from both sides.
  **Exception: tubular connections may receive a one-sided CJP without backing** (p.42-43).
- Matching filler metal is required for CJPs loaded in tension normal to the weld axis (p.43, p.59).
- **Backing (p.43-45).** D1.1 requires steel backing to be continuous for the length of the joint; segments must be
  joined by CJP welds. Only code-listed steels may be used as backing.
  - In statically loaded work, backing may stay in place, and its attaching welds need not be full length unless the
    engineer says otherwise.
  - AISC Table J2.5: if backing stays in a T- or corner-joint CJP loaded in tension, the filler must give CVN 20 ft-lb at
    +40 °F [27 J at +4 °C], or the weld is designed as a PJP.
  - Cyclic loading: transverse backing must be removed.
  - Ceramic and copper backing need WPSs qualified by test.
- **Groove preparations (p.45).** Square-edge prequalified joints are limited to thin material
  (3/8 in. [10 mm] maximum, per the page image). V and bevel preparations are cheapest to prepare; U and J need less weld
  metal. Normally the contractor picks the detail.
- **Spacer bars (p.45):** must be continuous and of approved material, with lack-of-fusion planes backgouged. They are
  economical above about 4 in. thickness.

### 1.4 PJP groove welds, including flare welds (p.46-47)
- The throat is less than the thickness. PJPs suit column splices, box corners, and T-joints (p.46).
- **E and S.** The design drawing gives only the **effective throat E**. The fabricator picks the process, position and
  angle, sets the **depth of preparation S**, and shows S with E in parentheses, "S(E)", on the shop drawings. The most
  common error is leaving E off the design drawing (p.46, p.67).
- **AISC J2.1 effective throat:** with SAW at 60° the full preparation depth counts. With SMAW, or at 45°, assume
  1/8 in. [3 mm] is not fused, so E = S − 3 mm (p.46).
- **Minimum effective throat (AISC Table J2.3)** depends on the thinner part and exists to ensure enough heat input, not
  to carry load (p.46). [AISC 360-16 Table J2.3 in SI: thinner part ≤ 6 mm → 3; over 6 to 13 → 5; over 13 to 19 → 6;
  over 19 to 38 → 8; over 38 to 57 → 10; over 57 to 150 → 13; over 150 → 16 mm.]
- There is always an unfused plane at the root. In shear this does not matter; under cyclic tension it does.
  **A single-sided PJP (or fillet) must not be able to rotate about its root.** Rotation is prevented by stiffeners,
  diaphragms or the shape of the member. RT and UT are not recommended on PJPs (p.46).
- Matching or undermatching filler is allowed for all PJPs (p.47).
- **Flare-bevel and flare-V welds (p.47-48).** E depends on the radius R and the process (AISC Table J2.2). For HSS
  corners, R ≈ 2t (approximate only). The table assumes the groove is filled flush; underfill reduces E. SAW gives
  E = R/2 for flare-V.
  - Economy: specify only the throat you need, not "flush" (p.157).

### 1.5 Fillet welds - rules and numbers (p.47-53)
- Specify by **leg size**; strength comes from the throat. For equal legs at 90°, throat = 0.707w (p.47).
- **Skewed joints:** t_w = w·cos(Ψ/2), where Ψ is the dihedral angle (p.61-62).
  - For Ψ < 60°, root fusion becomes unlikely. Apply the **Z-loss** from D1.1 Table 2.2 (process and angle), which
    reduces the throat (p.62).
  - On the obtuse side the throat becomes very small compared with the leg, so PJP becomes the economical choice
    (p.66, p.151).
  - Fig. 3-32 shows fillet use between a 60° minimum and a 135° maximum dihedral angle (p.66).
  - Bead-shape centerline cracking can occur in skewed fillets with an acute side below 70°, especially with
    deep-penetrating processes (p.82).
- **Single-sided fillets:** check that the root cannot rotate. RT and UT are not practical on fillets (p.47-48).
- **Minimum size, AISC Table J2.4.** The minimum exists to guarantee heat input (fusion, slow enough cooling to avoid
  cracking), not strength, and it assumes a single pass. A 1/4 in. [6 mm] fillet needs about 20-30 kJ/in.
  [0.8-1.2 kJ/mm]. Heat input H = 60·E·I/(1000·S) kJ/in. (arc V, amps, travel in./min).
  **The minimum need not exceed the thinner part.** With a very thick part, extra preheat based on the thick part may be
  justified (p.48, p.104).
  - [AISC 360-16 Table J2.4, by the thinner part joined: ≤ 6 mm → 3; over 6 to 13 → 5; over 13 to 19 → 6;
    over 19 → 8 mm. AWS D1.1 base-metal-T rules can differ for non-low-hydrogen work.]
- **Maximum size, AISC J2.2b (p.49).** The rule applies **only along edges** of material 1/4 in. [6 mm] or thicker (lap
  joints and some corner joints). There the maximum is t − 1/16 in. [t − 2 mm]; along thinner edges it is t. It does
  **not** apply to T-joints.
  - The guide's own example: **a tube column welded to a base plate may need a leg larger than the tube wall**. That is
    allowed because the weld is on a surface, not an edge (p.49, Fig. 3-12).
  - An unequal-leg fillet is an inefficient way round the limit: doubling one leg doubles the metal for only +25 %
    strength (p.49).
- **Minimum length (p.49):** at least 4w. If shorter, the effective size is L/4.
- **Maximum effective length, end-loaded welds (p.49):** up to 100w, no reduction. Beyond that, β = 1.2 − 0.002(L/w),
  not more than 1.0, and L_eff = βL. Above 300w, β = 0.6. [AISC 360-16 now uses L_eff = 180w above 300w.]
- **Intermittent welds (p.49-50, p.152):** each segment at least 4w and at least 1-1/2 in. [38 mm]. Their stress range
  is low under cyclic loading. Multipass intermittent welds are never economical. Intermittent welds are only economical
  at the minimum size; if a larger leg is needed, use the minimum size continuous instead.
- **Penetration (p.50):** an increased throat is allowed only if consistent penetration beyond the root is shown by tests
  with the production procedure (AISC J2.2a). Deep penetration raises admixture and centerline-crack risk.
- **Directional strength (p.50-51):** F_w = 0.60·F_EXX·(1.0 + 0.50·sin^1.5 θ), with θ measured from the weld axis.
  - Transverse welds are about 50 % stronger but have **much less deformation capacity** (Fig. 3-17). Where post-yield
    ductility matters, put the welds parallel to the load.
  - **Weld groups mixing longitudinal and transverse welds** use the greater of R_wl + R_wt and
    0.85R_wl + 1.5R_wt, where R_wt is taken without the directional increase. The second governs once the transverse
    weld is at least one third of the longitudinal length, for equal legs (p.51).
- **End returns / boxing (p.51-52):** neither required nor prohibited. They give clean terminations and some resistance
  to prying at the root, and they count in the weld length.
  - At flexible connections (clip angles), returns must be no longer than 4w and no longer than half the part width.
    Fig. 3-20 shows a return of at least 2w and at most 4w.
- **Terminations (p.52-53):**
  - A fillet may run full length or stop about one weld size short. Stopping short is preferred because there is less
    undercut.
  - In lap joints where one part runs past the other's edge, stop at least one weld size from the edge.
  - For transverse stiffeners on girder webs ≤ 3/4 in. [19 mm] not welded to the flange, hold the web weld back between
    4·t_w and 6·t_w from the web-to-flange weld toe.
  - **Do not join welds on opposite sides of a common plane around the edge** (Fig. 3-22).
- **Fit-up (p.53, D1.1 5.22.1):** if the root gap exceeds 1/16 in. [1.6 mm], increase the leg by the gap. This is only
  allowed up to 3/16 in. [5 mm] gap on material under 3 in. thick, and 5/16 in. [8 mm] on thicker material. The worked
  example shows the throat stress rising from 21 to 84 ksi as a 1/4 in. fillet's gap grows from 0 to 3/16 in. (Fig. 3-23).
- **Lap joints (p.66, AISC J2.2b):**
  - With longitudinal welds only, each weld length must be at least the transverse spacing between the welds
    (shear lag).
  - Overlap must be at least 5 × the thinner part.
  - A one-sided weld puts tension at the root; add plug/slot welds or mechanical restraint.

### 1.6 Plug and slot welds (p.53-54, p.62)
- Used in lap joints for shear transfer or to stop buckling, **never for direct tension** (including anchor-rod fixes,
  p.132).
- Hole diameter or slot width must exceed the thickness of the part containing it.
- Fill: completely when the plate is ≤ 5/8 in. [16 mm]. Thicker plates: at least half the thickness and at least 5/8 in.
- A fillet weld inside a large hole is just a fillet, not a plug weld.
- Strength = 0.6·F_EXX × the nominal hole area at the faying plane.
- Plug welds are easy in the flat position and hard out of position. Plugging mislocated holes is usually worse than
  leaving them open or bolting them (p.54, p.148).

### 1.7 Weld details: tabs, access holes, fillers, welds with bolts, combinations, k-area (p.56-59)
- **Weld tabs (p.56):** extend the joint geometry; "end dams" are not tabs. They may stay on static work and must come
  off on cyclic work; if they must come off for appearance, the documents must say so. Rule of thumb: length at least
  the weld throat. Only code steels may be used (no bolt tails, washers or electrode stubs).
- **Weld access holes (p.56-57):** must let the welder see and clean. They also separate the residual-stress fields
  (biaxial instead of triaxial stress). Surfaces must be smooth and free of notches. AISC sets minimum sizes.
- **Fillers (p.57):**
  - Fillers ≥ 1/4 in. [6 mm] extend past the splice plate and are welded to carry the load.
  - Thinner fillers sit flush with the splice plate, and the weld size is increased by the filler thickness.
  - A direct butt weld is usually cheaper.
- **Welds plus bolts (AISC J1.8, p.57-58):** no load sharing in general, because welds are stiffer. Exceptions:
  - Longitudinal fillets plus bearing bolts in standard or short-slotted holes transverse to the load (full weld strength
    plus 50 % of the bolts).
  - Alterations of riveted or slip-critical existing work.
- **Combinations (p.58):** strengths of different weld types in one joint may be added, **except** that a reinforcing
  fillet does not add to a CJP. For a PJP plus reinforcing fillet, the throat is the shortest distance from root to
  face; the two strengths are not simply added (Fig. 3-28).
- **k-area (p.58-59):** applies to rolled W-shapes only and does not affect this job.

### 1.8 Filler metal strength: matching, under- and overmatching (p.59-60)
- Comparisons use **minimum specified tensile strength**. Matching filler metal is usually within about 5 ksi of the
  base metal. Where two steels are joined, match the weaker (p.59).
- AISC Table J2.5 allows filler **one strength level (10 ksi) above matching** and still calls it matching (p.59-60).
- **Matching is required only** for CJPs in tension normal to the weld axis and for CJPs in shear (footnote exceptions).
  Fillets, PJPs and plug/slot welds may undermatch (p.59-60).
- Overmatching is never required. It raises residual stress and cracking risk.
  - Sizing a PJP on the strength of overmatched filler can make the fusion face govern without being checked.
  - For fillets this only matters if the weld is at least about 1.41 × the base metal strength (1/cos 45°) (p.60).
- Because of the throat-versus-fusion-face geometry, the guide (written to AISC 360-05) says no base-metal check is
  needed for fillets with matching or undermatching filler (p.61-62). [AISC 360-10 and -16 J2.4 now require the base
  metal to be checked by J4 as well.]

### 1.9 Strength formulas (p.61-62)
- **CJP:** the base metal governs, so no weld check is needed with matching filler. Undermatched CJPs (Table J2.5 note)
  are checked as welds (p.61).
- **PJP:** F_w = 0.60·F_EXX on A_w = E × L_eff, multiplied by φ (or divided by Ω). The six J2.5 load cases include
  bearing (p.61).
- **Fillet:** F_w = 0.60·F_EXX on A_w = throat × L_eff. **Weld craters count** in the length of a straight weld (p.62).
- **Plug/slot:** 0.60·F_EXX × the hole or slot area (p.62).

### 1.10 Special welds (p.62-65)
- **Arc spot (puddle) welds:** AWS D1.3, with d_e = 0.7d − 1.5t (p.62).
- **Repairs (p.62-63):**
  - Find the cause before repairing.
  - Remove the whole crack plus 2 in. [50 mm], with the extent found by MT.
  - Excavate to a U-groove shape (root radius at least 1/4 in., included angle at least 20°, ends tapered about 2.5 ×
    depth).
  - Get it right the first time. D1.1 5.26 sets when the engineer must be told.
- **Seal welds (p.63-64):** these are not strength welds, so use them with caution.
  - The galvanizers' association (AGA) recommends vent holes and discourages seal welds enclosing large areas.
  - Seal welds can break code rules on termination or minimum size, can create unintended load paths, and can confuse
    UT.
  - **The biggest risk is that they are made carelessly.** The engineer and contractor should agree the details.
- **Tack welds (p.64-65):** same quality as final welds.
  - Good practice: at least 2 in. [50 mm] long, or 4 × the thicker part, whichever is greater.
  - Tacks that will be remelted can be small and long. Tacks that stay in the weld are treated as root passes (made to
    the WPS, at minimum size). Multipass tacks need cascaded ends.
  - Tacks outside the joint may stay on static work unless the engineer requires removal; they must be removed on
    cyclic work.
- **Temporary welds (p.65):** same quality as final welds, and removed without gouging the base metal.
- **Intermixing (p.65):** filler metals and processes may be mixed in one joint. The one caution is FCAW-S where CVN is
  specified (p.27-28).
- **Butt-joint transitions (p.65):** above 1/3 of the nominal tensile stress, taper the thicker part. Show these tapers
  on the design drawings.

### 1.11 Welding symbols - AWS A2.4 (p.66-68, Fig. 3-36)
- A symbol has a reference line and arrow, plus an optional tail. The arrow points to the joint (p.67).
- **Below the line = arrow side; above = other side.** Which way the arrow points does not change this (p.67).
- **Symbols are read right to left**, whichever end the arrow leaves from. A common error is laying them out to read
  from arrow to tail (p.67).
- **Fixed layout (Fig. 3-36, p.68):**
  - S(E) and the weld symbol on the left.
  - Root opening (or plug fill depth) inside, groove angle above or below.
  - Then length and pitch "L-P".
  - Number of spot welds "(N)".
  - Finish and contour symbols.
  - Field flag and all-round circle at the arrow/reference-line junction.
  - Tail "T" for specification, process or a detail reference.
  - These elements stay in the same place when the tail and arrow are reversed.
- **Groove welds on contract drawings:** give only "CJP" or "PJP" in the tail. For a PJP, also give **E**. The
  fabricator adds the type and dimensions on the shop drawings (p.67).
- **A symbol with no dimensions and no "CJP"** means a weld that develops the adjacent base metal in tension and shear
  (D1.1:2004 2.2.5.3). The detailer may then choose CJP, PJP, fillet or a combination. If only CJP is acceptable, say so
  (p.67).
- **The weld-all-around symbol is often misused (p.67-68).** It calls for welds over the full length of every joint the
  arrow touches, including plate edges and corners. That can break hold-back rules and puts welds on edges. Point
  separate arrows at the joints instead.
- Symbols can also call up NDT (p.68).
- **Common mix-ups (p.68):** fillet versus bevel symbol; plug/slot versus backing versus spacer.
- Do not draw very complicated symbols. **Put a sketch of the detail in the tail, or reference one there** (p.68).

### 1.12 Steels and weldability (p.70-76)
- Prequalified WPSs need steels from D1.1 Table 3.1. Approved higher-strength steels (Annex M) need WPS qualification
  (p.71).
- **Unlisted steels (p.71):** D1.1 recognizes **only steels made to U.S. standards** (ASTM, API). Steels to other
  standards "may have excellent properties" but are not listed.
  - D1.1:2004 3.6 still allows a prequalified WPS on an unlisted steel if the engineer approves, if it is only for
    auxiliary attachments, or if its chemistry falls within a listed grade. Otherwise the WPS must be qualified by test.
  - AISC A3.1b allows unidentified steel only for unimportant details.
- Steels with only P and S limits (like ASTM A675 bar) need their weldability investigated (p.75).
- **Do not weld on high-strength bolts or nuts.** Never weld A490 [~F10T, 10.9]; welding A325 or A449 is not
  recommended (p.74-75). Do not weld nuts to anchor rods (p.132).

### 1.13 Cracking, restraint and shrinkage (p.78-89)
- Every weld cracking mechanism needs shrinkage plus restraint (p.78).
- High restraint comes with thickness over 1-1/2 in., yield over 50 ksi, members meeting from three directions (p.79),
  and throats of 2 in. or more over lengths of 1-1/2 ft or more (p.135). **None of this applies to T1's thin walls.**
- **HAZ (hydrogen) cracking needs hydrogen + a susceptible microstructure + stress.**
  - D1.1 requires low-hydrogen SMAW electrodes for prequalified WPSs on steel with Fy ≥ 50 ksi.
  - Cooling is faster in thick sections, with low preheat, and with low heat input (p.83-84).
  - CE formulas (IIW CE, Pcm, CEN) are only comparative (p.85).
- **Ways to reduce shrinkage stress (p.88):**
  - Use the smallest adequate weld.
  - Choose details with the least weld metal.
  - Control fit-up and avoid excessive reinforcement.
  - Use the fewest passes.
  - Use the lowest-strength adequate filler.
  - Don't overweld.
- **Ways to reduce restraint (p.89):**
  - Build in subassemblies.
  - Weld the most-shrinking and the most-rigid parts first.
  - Balance welds about the member.
  - Leave 1/32-1/16 in. [1-1.5 mm] gaps in very tight machined fits.
  - Preset parts.

### 1.14 Distortion (p.90-98)
- **Causes:** non-uniform heating; thin, flexible parts distort and thick, rigid parts crack instead (p.90).
- **General control (p.91):**
  - Use the smallest adequate weld, or intermittent welds where suitable.
  - Use the least weld metal and the fewest passes.
  - Control fit-up, limit reinforcement and penetration, don't overweld.
  - "CJP just to be safe" increases distortion.
  - Spray water or compressed air must not be used to cool welds.
- **Angular distortion (p.92-93):** Δ = 0.02·W·ω^1.3 / t² (inches) or 0.19·W·ω^1.3 / t² (mm), where W = flange width,
  ω = fillet size, t = flange thickness. Remedies are double-sided welds, unequal two-sided grooves, and presetting.
- **Transverse shrinkage (p.93):** Δ ≈ 0.10·A_w / t (about 10 % of the average weld width). It **builds up over a
  series of welds, for example a run of chord splices on a long truss**. Preset the joint wide to allow for it.
- **Longitudinal camber or sweep (p.94):** Δ = 0.005·A_w·L²·d / I, accurate to about ±20 %. Balance welds about the
  neutral axis, or plan the welding sequence or subassemblies so the weld centroid stays on the axis (p.97-98).
- Distortion limits are in D1.1 Section 5. If heavy shrinkage or distortion is expected, D1.1 5.21.3 requires a
  **distortion-control plan** sent to the engineer for comment (p.147).
- Stress relief does not remove the plastic part of distortion (p.89).

### 1.15 WPS, processes and welding positions (p.16-41, p.100-105, p.138)
- **Written WPSs are required for all welding**, including prequalified WPSs. The belief that a prequalified WPS need
  not be written is wrong (p.100).
- The fabricator writes the WPS and the inspector checks it is followed. A prequalified WPS still needs qualified
  welders and code workmanship (p.100-101).
- **Prequalified processes** are SMAW, SAW, GMAW (except **GMAW-S, short-circuit**) and FCAW (p.101).
  - GMAW-S is prone to incomplete fusion ("cold lap"). WPSs for it must be qualified by test; the guide suggests this
    for anything over 3/16 in. [5 mm] (p.18, p.34).
  - In vertical or overhead GMAW without pulsed spray, the transfer mode is effectively short-circuit (p.34).
  - FCAW single-pass electrodes (for example E70T-3, -10, -13, -14, -GS) are excluded from prequalified WPSs (p.18,
    p.26).
  - ESW/EGW and GTAW need qualified WPSs (p.37-38).
- Prequalified status also needs listed steel/filler combinations (D1.1 Table 3.1), the Table 3.2 preheat, and the
  Table 3.7 limits (electrode size, current, pass thickness, **maximum single-pass fillet size by position**) (p.101).
- **Meeting the prequalified limits does not guarantee a good weld.** The example is 800 A on a 3/8 in. plate, which
  burns through: amperage and electrode must suit the material thickness (D1.1 5.3.1.2) (p.101-102).
- **Low-hydrogen electrodes** must be stored in ovens and handed out with exposure limits. Using them lowers the
  required preheat (p.21-22).
- **Filler classification:** E7018 means 70 ksi, all-position, low-hydrogen, 20 ft-lb at −20 °F (p.20). E71T-1C means
  all-position, gas-shielded, multipass (p.25).
- FCAW-G needs wind ≤ 5 mph (D1.8: 3 mph) (p.27).
- **FCAW-S is often used for HSS T-K-Y joints** because the gun is compact and the joint is accessible (p.27, p.138).
- **Positions.** SAW and spray transfer are flat or horizontal only. Pulsed GMAW, FCAW and SMAW work in all positions.
  **HSS work routinely needs all-position welding, and on round HSS the position changes continuously round the joint**
  (p.138).
- **Qualified WPSs:** a PQR plus essential variables (D1.1 Tables 4.5-4.8). The engineer may ask for qualification by
  test on critical welds (p.102-103).
- **Preheat and interpass (p.105):** follow D1.1 minimums. Interpass above 550 °F [290 °C] hurts CVN. Post-heat is
  400-450 °F, 1 h per in.

### 1.16 Quality, inspection and NDT (p.106-116, p.143-144)
- D1.1 is a **workmanship** standard, not fitness-for-purpose. The engineer may set alternative acceptance criteria
  under D1.1 6.8 (stricter or looser, with documentation) (p.106, p.144).
- **Discontinuities (p.106-111):**
  - Planar defects (cracks, incomplete fusion, overlap) are the worst; no cracks are accepted.
  - Undercut and porosity limits are in D1.1 Table 6.1.
  - Concavity matters only if the throat is short. Excess convexity is fixed by grinding the toe as well as the face.
  - Craters must be filled, except at the ends of intermittent fillets.
  - Grind arc strikes.
- **Visual inspection is the most powerful method** and the only one that improves the weld while it is made. It covers
  before, during and after welding, and D1.1 requires it on **all** welds even when NDT is also done (p.112).
  - **Before welding:** drawings, WPS, welder qualification, materials, equipment, base metal, **fit-up**, preheat,
    conditions, recording system.
  - **During welding:** root bead, backgouge, interpass temperature, sequence, each layer, cleaning, WPS compliance
    (p.113).
  - **After welding:** appearance, **size, length, that every required weld is present, that no unauthorized welds were
    added**, distortion (p.113).
- **NDT (p.113-116):**
  - Welds must pass VT before NDT.
  - **If the engineer specifies no NDT, D1.1 and AISC require only VT by the contractor's inspector.** NDT added later
    is paid for by the owner (D1.1 6.6.5) (p.113, p.143).
  - **PT** finds surface defects only; it is slow, messy and must not be used hot, so it is mainly for non-magnetic
    metals.
  - **MT** finds surface and slightly subsurface defects, is faster, works on warm parts, and is **preferred over PT on
    steel**. Use the yoke method (no arc strikes) and scan in two directions. MT is the usual check of fillet or PJP
    repairs (p.114-115).
  - **RT** suits CJP butt joints; it is unsuitable for PJP, fillets, T- and corner joints.
  - **UT** suits CJP in butt, T- and corner joints but not fillets. D1.1 has **no UT acceptance criteria for tubulars;
    the contract documents must give them** (p.115-116, p.138).
- **Verification inspection** (independent of the contractor, reporting to the engineer) is the engineer's decision.
  Inspector qualification can be specified (p.143).
- **CVN:** if the documents give none, no toughness can be assumed for weld, HAZ or base metal (p.144).
- **Materials certification** (filler metal, gas) must be requested if wanted (D1.1 5.3) (p.145).
- **Unspecified welds:** the inspector must check that no unspecified weld was added without the engineer's approval
  (D1.1 6.5.1) (p.147).
- **Defaults for statically loaded structures:** tack welds, backing and weld tabs may stay unless the engineer requires
  removal (p.145).

### 1.17 Fatigue, seismic, AESS, coatings, anchor rods (p.118-141)
- **Fatigue (p.124-130):** not needed below 20,000 cycles of live load (AISC). Ordinary roof trusses are outside its
  scope. If needed:
  - Detail categories A to E′ and F.
  - The ends of longitudinal or intermittent welds are Category E.
  - Root failure of fillet or PJP T-joints uses the reduction factor R_PJP / R_FIL.
- **Seismic (p.118-122):** applies when R > 3. Demand-critical welds need CVN 20 ft-lb at 0/−20 °F plus 40 ft-lb at
  +70 °F. Not applicable to T1.
- **AESS (p.138-139):**
  - The documents must identify AESS members and welds needing special contour or grinding.
  - Set acceptance criteria by viewing distance. **The guide's example is a roof truss 20 ft above the floor, which
    should not be held to eye-level criteria.**
  - Tabs, backing and tacks are usually removed. Avoid welded plugs in access holes.
- **Coatings (p.133-134):**
  - Field welds need surfaces within 2 in. [50 mm] free of coatings that harm welding (AISC M3.5). A thin rust-inhibitive
    primer may remain (D1.1).
  - Zinc from hot-dip galvanizing can cause cracking.
  - Test critical cases with a fillet-break test or a PQR.
- **Anchor rods (p.132-133):**
  - Investigate weldability first.
  - Never weld nuts; plug welds are not for tension.
  - Washer plates may be fillet-welded to rods only if the rod is weldable.

### 1.18 HSS / tubular welding (p.135-138)
- HSS joints are usually welded, at least for attachments (p.136).
- **The connection capacity is rarely governed by weld size.** Other limit states, often in the chord, control.
  **Load on the weld around the joint is non-uniform, so a weld can "unzip"** if that is ignored (p.137).
- **Rectangular HSS (p.137):** step the branch narrower than the chord so a fillet can sit on the flat face. Matched
  widths need flare-bevel welds and may need backing.
- **K-joints (p.137, Fig. 12-4):**
  - **Gapped joints are preferred to overlapped ones** for joint preparation and welding access, even more so for
    round HSS.
  - Overlapped joints are stronger and stiffer.
  - **Keep the acute angle at 30° or more** so the toe can be welded and inspected.
- **Cutting (p.137-138):** round branches need **saddle (profile) cuts with a continuously varying bevel**. CNC plasma or
  laser makes this easy and improves fit-up.
- **Assembly order for round-HSS trusses (p.138, Fig. 12-5):** once both chords are fixed, a cut-to-length branch cannot
  be dropped in between. Plan an "E" assembly (one chord plus webs first, then the other chord) or add an extra splice.
- **Welding (p.138):**
  - All-position welding with a continuously changing position.
  - Clean HSS needs little deoxidizer.
  - Low-spatter processes help where glossy paint follows.
  - Access matters most: SMAW reaches the root; gas nozzles block access at acute angles; FCAW-S is common for T-K-Y.
  - **D1.1 has specific, more demanding welder qualification tests for T-K-Y and tubular work.**
  - D1.1 has no tubular UT criteria; specify them.
- **One-sided CJP without backing is allowed for tubular joints** (p.43). **Z-loss for tubular T-Y-K welds** is in D1.1
  (Table 2.8 in the 2004 edition) (p.143).

### 1.19 Engineer approvals and unexpected conditions (p.145-149)
- **Routine approvals (p.145-147):**
  - Previous welder qualifications and inspector qualifications.
  - WPSs qualified to other standards (ASME IX, AWS B2.1).
  - Alternative acceptance criteria.
  - Repair of cut-edge gouges.
  - Caulking.
  - Die stamping on cyclic members.
  - The distortion-control plan.
- **Unexpected conditions (p.147-149):**
  - Base metal defects (repair welding over 20 % of the plate length needs the engineer).
  - Fit-up outside tolerance.
  - Cracks (the engineer must be told of major cracks).
  - Damaged base metal.
  - Cutting assembled steel (tell the engineer first).
  - Mislocated holes (often best left open).
  - Heat straightening (hot-rolled steel maximum 1,200 °F; Q&T maximum 1,100 °F).

### 1.20 Economy - costly versus economical details (p.150-157)
- **Labor is 75-95 % of weld cost, and a repair costs about 10 times the original weld.** A detail that is hard to make
  well is never cheap (p.150).
- **CJPs cost the most.** Use them only for full-strength butt joints in tension. For corner and T-joints in shear, use
  PJP+fillet or fillets (p.150-151).
- **Fillet or PJP (p.151):**
  - For the same throat, a 45° PJP uses half the metal, but the bevel costs about one pass.
  - Rule of thumb: **fillets up to 1 in. [25 mm] leg, PJP above that**.
  - Skewed (obtuse) T-joints favour PJP.
- **PJP + fillet combination (p.151-152):** about the same metal as PJP alone, a better contour, and often the best
  choice out of the flat position.
- **Longer rather than larger (p.152):** strength scales with length, while metal scales with leg². Design at the
  **minimum size first**, then lengthen, then go intermittent if the length is short. Double-sided fillets halve the
  metal and protect the root.
- **Intermittent welds (p.152-153):** only at the minimum size and single pass. Allow continuous welds if the
  contractor prefers.
- **CJP single or double sided (p.153-156):**
  - Prequalified details do not save 2:1. Double-sided saves about 1.5:1 at 1/2 in. and about 1.03:1 at 6 in.
  - Single-sided is usually simpler unless distortion is the concern.
  - Below 1 in. throat use a small root opening and large angle; at 1 in. and over, the reverse.
  - Spacer bars are economical over about 3 in.
- **Flare welds (p.157):** specify the throat needed, not "flush".
- **Shop or field (p.157):** weld in the shop wherever possible. **"Weld in shop, bolt in field" is not an economic law**;
  a field-welded heavy splice was about 25 % cheaper than the bolted one (p.157).

---

---

# Part D. AISC Design Guide 24 - Hollow Structural Section Connections


Working extract and review for job `jobs/steel_roof_truss` (25 m Pratt roof truss, JIS G3444 STK400 CHS).

**Page convention.** "p.NN" means the **PDF page** of
`Design Guide 24 - Hollow Structural Section Connections.pdf` (153 pp.). Book page = PDF page − 7
(for example, p.58 = book p.51).

**Basis warning.** DG24 is written against **AISC 360-05**. Its section and equation numbers (K1 plates,
K2 truss joints, K3 moment joints, Eq. K2-x) are the 2005 numbers. Our calc cites **AISC 360-16**, in which
the same provisions are renumbered: K2 is plate-to-HSS (Table K2.1 round), K3 is HSS-to-HSS truss
(**Table K3.1 round**, K3.2 rectangular), K4 is moment joints, and K5 covers welds to rectangular HSS.
I checked these numbers against `a360-16-spec-and-commentary.pdf` (PDF pp.210–223).

**Copyright.** Everything below is paraphrased. Equations are restated in my own notation.

Notation: D, t = chord OD and design wall; Db, tb = branch; β = Db/D; γ = D/(2t); θ = branch angle;
g = gap along the chord face between branch toes; e = noding eccentricity (+ away from the branches);
Qf = chord-stress function; U = chord utilisation used in Qf; φ = LRFD resistance factor.




#### 1.1 Scope, materials and design wall thickness (Ch.1, pp.8–11)

- A500 HSS are cold-formed ERW tubes. The external seam bead is removed and the internal bead is
  normally left. Round and rectangular shapes of the same grade have different Fy (Table 1-1, p.9):
  A500 Gr B round 42/58 ksi (290/400 MPa), Gr C round 46/62 ksi (315/425); A53 Gr B pipe 35/60 ksi;
  A501 Gr B 50/70 ksi; CSA 350W 51/65 ksi. Our STK400 (Fy 235, Fu 400) is closest to A53 B or A500 B round.
- **Design wall = 0.93 × nominal t** (p.9). The reason is that ASTM tolerance lets the wall be 10 % under
  nominal, so mills roll under it. AISC B3.12 (2005) / B4.2 (2016) uses 0.93t for all properties
  (A, I, Z, S, D/t). 0.93t does **not** apply to SAW box sections made at full thickness (p.9). → Using
  0.93t for ERW STK400 is consistent with this reasoning, because JIS gives a similar −10 % wall tolerance
  (confirm with the supplier).
- Scope of the AISC/DG24 joint rules (p.10): static loading, single-plane joints, branch axes
  perpendicular to the plane symmetric (no offset members), unfilled and unreinforced HSS. Fatigue,
  seismic, multiplanar, offset and concrete-filled joints are out of scope; DG24 points to AWS D1.1,
  CIDECT and Packer & Henderson for those.
- Notch toughness (p.11): A500 has no CVN requirement; A501 Gr B has 27 J at −18 °C. This is not
  critical for a statically loaded roof.
- **Galvanizing (p.11).** Corner cracking risk applies to rectangular HSS only (corner radius about 2t,
  below the 3t bending radius recommended for galvanizing). Hot-dip galvanizing needs fill, vent and
  drain holes: **vent holes ≥ 13 mm (½ in.) dia., drain holes 25 mm (1 in.) dia.** Adequate hole size
  also limits differential thermal stresses during dipping.
- **Internal corrosion (p.11, after AISC Comm. B3.11).**
  (1) Internal corrosion does not occur inside an enclosed building; it matters only for HSS exposed to weather.
  (2) **A sealed HSS does not corrode internally.**
  (3) Pressure-equalising holes, placed where water cannot run in by gravity, stop capillary or
      aspiration ingress through fine openings such as unwelded plate laps.
  (4) Internal protection is needed only for open HSS with air exchange or water flow, or with a
      temperature gradient that causes condensation.
  Water must not be left inside, because freezing can burst the tube.

#### 1.2 Weld design philosophy (Ch.2 intro, p.12)

Two acceptable bases for branch welds:

1. **Develop the branch wall.** Size the weld for the branch wall's yield strength at every point
   around the branch. This is the upper bound and is conservative; use it when plastic redistribution in
   the joint is needed. Keep the **same effective weld size all round** (the only exception is the hidden
   weld of a partly overlapped K-joint).
2. **Fit for purpose.** Size the weld for the actual branch force. This suits branches sized for
   uniformity or appearance, where forces are low (for example, mid-span webs of a simply supported
   truss). It **must** use effective weld lengths (§2.4). The same effective size is still kept all round,
   and the **whole perimeter is welded**.

#### 1.3 Weld types, preference and skewed joints (§2.1, pp.12–14)

- Order of preference: **fillet → PJP groove → flare-bevel / flare-V → CJP** (p.12).
- Fillet welds are the most economical and should be used wherever practical. **For T-, Y-, K- and
  X-joints, do not use the AISC directional-strength increase (J2-5, the 1 + 0.5 sin^1.5 θ term)**,
  because these welds are not loaded in their own plane (p.12).
- Rectangular HSS: sit the branch on the chord flat (stepped, Bb < B − 2t to 4t) so a fillet can be laid,
  rather than a matched width (Fig 2-1, p.12). Matched joints need flare welds (p.13–14).
- **Skewed joints and the local dihedral angle (Fig 2-2, Table 2-1, pp.12–13).** The theoretical throat
  grows as the dihedral angle Ψ falls below 90° and shrinks above 90°. The equivalent 90° weld size is
  w_eq = factor × w. Factors: Ψ = 60° 1.41; 70° 1.23; 80° 1.10; 90° 1.00; 100° 0.923; 110° 0.863;
  120° 0.816; 130° 0.780. On the obtuse side of a square-cut element there is a root opening, which AWS D1.1
  limits to **3/16 in. (5 mm)** (5.22.1). **The leg is increased by the root opening**
  (Ex 2.1, pp.17–18: opening = tp·sin(skew); leg = w + opening).
- PJP / CJP (p.13). HSS-to-HSS joints can only be welded from one side, so details that need back-gouging
  are impossible. PJP is preferred to CJP. Prequalified PJP gives an effective throat E as a function of
  thickness, groove depth S, process and position (E = S minus the root loss).
  - **The design drawing states the required weld strength; the shop drawing shows S and E.**
  - CJP should use steel backing where possible (it may stay in place under static load). Without backing,
    the open-root CJP needs a **6GR-qualified welder**.
  - On round HSS-to-HSS joints the bevel preparation changes continuously round the perimeter
    (reference: Post 1990).
- Flare-bevel effective throat (p.13), with the weld filled flush and R = 2t:
  - **5/8 R** for GMAW / FCAW-G;
  - **5/16 R** for SMAW / FCAW-S / SAW;
  - reduce by any under-fill.
  This applies only to rectangular corners (not our job).

#### 1.4 Inspection (§2.2, pp.14–15)

- **VT on all welds, including fit-up before welding** (bevels, gaps, alignment).
- PT is for surface cracks and for confirming that gouged repairs are clean.
- MT detects surface defects and subsurface defects to about 2.5 mm deep; use it where restraint is high.
- **UT has limited use on HSS.** Thin walls and changing geometry make the signals hard to read, and UT is
  not suitable for fillets or small PJP welds.
- RT is only practical for butt splices.
- → GN 4.4 (100 % VT, 10 % MT/PT) is consistent with this.

#### 1.5 Effective weld size, base-metal limit (§2.3, pp.15–16)

- Weld metal, per unit length: Rn = 0.60 FEXX × (D/16)·√2/2 (US units). Base metal next to the weld:
  Rn = F_BM·t, where F_BM = 0.6Fy for yielding (φ 1.00) and 0.6Fu for rupture (φ 0.75).
- Equating the two gives an effective weld size that the base metal can support (Eqs 2-3, 2-4).
  **Base-metal yielding governs when Fy/Fu < 0.75.** That is the case for round HSS (A500 B round 0.724)
  and for **STK400 (0.59)**, so use the yielding form.
- In SI, for one shear plane: w_eff = (1.0 × 0.6 Fy t) / (0.75 × 0.6 FEXX × 0.707).
  For STK400/E49 this is **about 0.905 t**.
- Table 2-3 gives the minimum wall thickness needed to develop a given fillet. Two welds on one plate
  share the plate thickness (half each).

#### 1.6 Effective weld length (§2.4, pp.16–17; Ex 8.5 p.129)

- For a **transverse** element on a rectangular HSS face, load concentrates near the sidewalls, so welds
  can "unzip" from the ends. Effective weld length = the effective width b_eoi (AISC K1-x). The same
  reduced length applies to the weld and to the element.
- **Longitudinal** welds on rectangular HSS are fully effective (Ex 2.2).
- AISC K2.3e (2005) gives effective lengths for rectangular T-, Y-, X- and gapped K-joints. For gapped K:
  - θ ≤ 50°: Le = 2(Hb − 1.2tb)/sinθ + 2(Bb − 1.2tb), all four sides effective;
  - θ ≥ 60°: Le = 2(Hb − 1.2tb)/sinθ + (Bb − 1.2tb), heel not effective;
  - interpolate between 50° and 60° (Ex 8.5, p.129; = 360-16 Eqs K5-8, K5-9).
  - For an X-joint, only 3 sides are effective.
  - For overlapped rectangular K-joints, use b_eoi / b_eov.
- **DG24 and AISC 360-16 K5 give no effective-length rule for ROUND branches** (360-16 K5 covers
  rectangular HSS only). The source for round branches is **AWS D1.1:2015 §9.5.4**
  (AWS PDF p.300; Clause 10 in D1.1:2020):
  - weld length L = 2π r Ka, with Ka ≈ (1 + 1/sinθ)/2 for axial load;
  - LRFD fillet capacity Qw = 0.6 tw FEXX per unit length, Φ = 0.8.
  - Examples: 60.5 at 45° → L ≈ 229 mm (perimeter 190); 48.6 at 45° → 184 mm.
- Ex 8.5 closing note (p.129): welds can either be designed this way or be proportioned to develop the
  branch wall all round. The second is the upper limit on the weld size needed for any load.

#### 1.7 Prequalified tubular fillet details (cross-reference used for the drawing recommendations)

DG24 itself gives only Fig 2-2 and Table 2-1. The detail rules for round branches are in
**AWS D1.1:2015 Fig 9.10** (AWS PDF p.342):

- **Zones round the branch:**
  - **TOE** = obtuse side, Ψ > 120°. For a 45° diagonal this is the **gap side**. Ψ ≈ 135°.
  - **SIDE** = Ψ around 90°.
  - **HEEL** = acute side, Ψ < 60°. For a 45° diagonal this is the **outer side**. Ψ ≈ 45°.
- **Minimum leg L for throat E = 0.7t / t / 1.07t:**
  - heel < 60°: 1.5t / 1.5t / max(1.5t, 1.4t + Z);
  - side ≤ 100°: t / 1.4t / 1.5t;
  - side 100–110°: 1.1t / 1.6t / 1.75t;
  - side 110–120°: 1.2t / 1.8t / 2.0t;
  - **toe > 120°: branch edge cut back (bevel) t / 1.4t, or a full-bevel 60–90° groove for 1.07t.**
- Root opening 0–5 mm. **Not prequalified below 30°.** **Below 60°, apply the Z-loss** (AWS Table 9.5).
- E = 1.07t is the "develop the branch" level. Its side leg of 1.5t matches our `weld_leg` (≈1.51t).

#### 1.8 Bolting to HSS (Ch.3, pp.22–35)

- **Access.** Bolting directly to HSS is hard because the inside cannot be reached. Bolts can be used
  near an open end, or through access holes that are later covered and sealed so as to restore the
  section. The usual alternative is to weld attachments and bolt to those (p.22).
- Direct fasteners listed (p.22): through-bolts, blind bolts, threaded studs, flow-drilled bolts, nails,
  screws. Through-bolts are covered by AISC J3.10(c); studs by Table J3.2.
- **Shear (§3.1).** The design is the same as for a W-shape web, with bearing and block shear near the end.
  **Through-bolts use the pin-bearing rule (J7), 1.8 Fy t d**, because the grip is not clamped
  (Ex 3.1, pp.23–25).
  - Bolt length = grip + washer + allowance (Manual Table 7-15).
- **Tension (§3.2), two added HSS limit states:**
  1. **Pull-out of a fastener through the wall:** rn = Fu (0.6 π dw t), where dw is the diameter bearing on
     the inside face. φ = 0.67 (Ω = 2.25) (p.22). For a stud, dw = stud dia. (Ex 3.2).
  2. **Wall distortion:** treat the fastener group as a "branch" (yield-line T-joint, chord plastification,
     with the loaded area circumscribing the fasteners) (pp.23, 27).
  - Prying is checked per Manual Part 9. In Ex 3.3 (pp.29–35), prying cut the bolt strength by about 30 %.
- → Not used on T1. All T1 bolts are in welded plates.

#### 1.9 End connections of tension/compression members (Ch.5, pp.56–79)

**Types (Fig 5-1, pp.56–57).** End tee with a cap plate; **slotted HSS with a gusset/knife plate**;
field-welded gusset; end plate.

**Slotted HSS / knife plate (§5.1, §5.3; Ex 5.2, pp.56–58, 72–79):**

- **Shear lag** concentrates force near the plate, giving circumferential HSS fracture at the weld end in
  tension (Fig 5-2). **Block shear / tear-out** of the HSS is also possible with short slots and short welds.
- **U (AISC Table D3.1 case 5):**
  - U = 1.0 if l ≥ 1.3D;
  - U = 1 − x̄/l with **x̄ = D/π** if D ≤ l < 1.3D;
  - **no U is given for l < D**, so make the weld length ≥ D (p.58).
  - Example: D = 6 in., l = D gives U = 0.682 (p.74).
- **Net area at the slot:** An = A − 2 (tp + clearance)·t (p.74). The slot is cut about **1/16 in.
  (≈1.6–2 mm) wider than the plate**. AWS D1.1 allows a 1/16 in. gap without increasing the weld;
  a larger gap means increasing the leg by the gap (p.58).
- **Do not return the weld round the end of the plate inside the slot** (risk of undercutting the plate)
  (p.58).
- **Field-welded braces:** the slot runs beyond the plate end for erection. The unfilled slot reduces the
  net area and, together with shear lag, can make HSS rupture govern (p.58).
- The slot end need not be machined or drilled to a radius for static load (tests by Martinez-Saucedo &
  Packer 2006; p.72).
- **The gusset must be wider than the HSS** to give a shelf for the fillet welds (p.58).
- **Limit states (Ex 5.2):**
  - HSS gross yielding (φ 0.9);
  - HSS net rupture with U at the slot (φ 0.75);
  - plate yielding and rupture, with An ≤ 0.85Ag for splice-type plates (J4.1b);
  - plate block shear (J4-5);
  - weld metal vs HSS base metal vs plate base metal. Base metal is **shear yielding, φ 1.00**, with two
    shear planes on the plate, A_BM = 2·l·tp. The thinner HSS wall can govern via t_min (Table 2-3);
  - bolt shear;
  - bolt bearing / tear-out, 1.2·Lc·t·Fu ≤ 2.4·d·t·Fu, end and interior bolts separately.

**End tee / stem in compression (§5.2, Fig 5-5, Ex 5.1, pp.57–72):**

- The stem / lapped plate acts as an **eccentrically loaded column**:
  - e = (t_stem + t_gusset)/2;
  - both ends fixed but free to sway, so **K = 1.2** over the length Lc;
  - properties of the thinner plate;
  - Mr = Pr·e/2.
- Interaction (H1):
  - Eq 5-3 (Pr/Pc ≥ 0.2): Pr ≤ 1 / (1/Pc + 4e/(9Mc));
  - Eq 5-4 (Pr/Pc < 0.2): Pr ≤ 2 / (1/Pc + e/Mc).
- Thicker plates are usually cheaper than stiffeners.
- Cap-plate load dispersion is **2.5:1 from each face of the stem**, giving a width of 5tp + N
  (Comm. K1, Fig 7-3, p.90). When 5tp + N ≥ the HSS width, all walls are effective.

**End plate on ROUND HSS — the flange-plate splice (§5.4, pp.57–59).** This is the DG24 basis for our
chord splice. It is **not** "DG24 9.1": Chapter 9 is HSS-to-HSS moment joints, and Example 9.1 is a
round X-joint under in-plane bending.

- Fig 5-4(a), p.57: bolts equally spaced on a circle. **a = b**, where b = distance from the HSS wall to the
  bolt line and a = distance from the bolt line to the plate edge. **b ≥ 1.5 in. (38 mm).**
- Keep b as small as practical, while allowing impact-wrench clearance and J3.3 spacing (p.58).
- Limit states: (1) plate yielding, (2) bolt tension **including prying**, (3) plate-to-HSS weld.
  Method: Packer & Henderson 1997 / Willibald.
  - **Plate:** tp ≥ √( 2 Pr / (φ Fyp π f3) ), φ = 0.90 (Eq 5-5).
  - **Bolts:** n ≥ (Pr/Rc) · [1 − 1/f3 + 1/(f3 ln(r1/r2))], with Rc = φ rn of one bolt in tension
    (Manual Table 7-2) (Eq 5-6).
  - **Weld:** w ≥ Pr √2 / (Fwc π D), with Fwc = 0.75 × 0.60 FEXX (Eq 5-7).
  - Definitions: f3 = [k3 + √(k3² − 4k1)]/(2k1); k1 = ln(r2/r3); k3 = k1 + 2; r1 = D/2 + 2b;
    r2 = D/2 + b; r3 = (D − t)/2 (Eqs 5-8 to 5-13).
  - **Fig 5-6** plots f3 against (D − t)/(D + 2b). It runs from about 1 at 0 to about 10 at 0.8.
- Under compression the force passes uniformly through the plate by bearing (p.57).
- Rectangular end plates, for reference: bolts on 2 sides use a modified T-stub (Eqs 5-14 to 5-22).
  Bolts on 4 sides are checked for no prying with
  t_min = √(4.44 (Pu/n) b′ / (p Fyp)) (Eq 5-23a, p.60). Bolts must not sit beyond the HSS corners.

#### 1.10 Principal limit states and design tips (Ch.6, pp.80–83)

- **Chord plastification.**
  - A round chord behaves as a closed ring, and the whole cross-section ovalises (Fig 6-2a).
  - A longitudinal plate on a round HSS is especially weak and is deformation-limited (Fig 6-2b).
  - Gap K-joints show a push–pull mechanism (p.80).
- **Punching (chord shear yielding).**
  - Governs at mid to high β, and only when Db < D − 2t.
  - AISC uses 0.6Fy with φ = 0.95.
  - For round chords it is applied over the full branch footprint (pp.80–81).
- **Uneven load distribution.** This is local yielding of transverse elements and branch walls; it applies to
  rectangular chords (p.81–82).
- **Chord sidewall failure.** Rectangular chords at β ≈ 1 (p.82).
- Shear-lag local yielding of the chord face behind the heel of a rectangular tension branch is avoided by
  slenderness limits (p.83).
- **Design tips (p.83, repeated p.102):**
  - **Design joints unreinforced** wherever possible.
  - **Stocky chords: 15 ≤ D/t ≤ 30 for round.** Ours: D/t = 25. ✓
  - **Thin, wide branches**, with tb ≤ t. ✓
  - **Prefer gapped K-joints.** They are easier and cheaper than overlapped joints, which for round members
    need complex profiling and careful fit-up.

#### 1.11 Plate-to-round HSS (Ch.7, pp.84–97; Table 7-1 = AISC 360-16 Table K2.1)

- **Transverse plate T/X** (K1-1): Rn = Fy t² · [5.5 / (1 − 0.81 Bp/D)] · Qf, φ 0.90.
  Out-of-plane plate moment: Mn = 0.5 Bp Rn.
- **Longitudinal plate T/Y/X** (K1-8): Rn sinθ = 5.5 Fy t² (1 + 0.25 N/D) Qf, φ 0.90.
  In-plane moment: Mn = N·Rn.
  - For a diagonal brace, check the **component of the plate force normal to the chord** (pp.84–85).
  - Plate-to-HSS joints are deformation-controlled. The same capacity is used for tension and compression
    (p.84–85).
- **Shear tab on a round HSS:** tp ≤ (Fu/Fyp)·t, from K1-10. The tab should yield before the wall punches
  (Eq 7-1, p.90). Requires D/t ≤ 0.11E/Fy.
- **Cap plate:** Rn = 2 Fy t (5tp + N) ≤ A Fy, φ 1.00 (Comm. K1.6) (p.86, Fig 7-3).
- **Functions (round):** Qf = 1 if the chord face is in tension; otherwise Qf = 1 − 0.3U(1 + U), with
  U = |Pr/(A Fc) + Mr/(S Fc)| on the side of the joint with **lower** compression; Fc = Fy (LRFD).
- **Table 7-1A limits (p.87):**
  - θ ≥ 30°;
  - D/t ≤ 50 for T, ≤ 40 for X;
  - D/t ≤ 0.11E/Fy for shear-tab or cap-plate compression;
  - 0.2 < Bp/D ≤ 1.0 for transverse plates;
  - Fy ≤ 52 ksi (360 MPa);
  - Fy/Fu ≤ 0.8.
  - [360-16 Table K2.1A adds an **end distance l_end ≥ D(1.25 − Bp/(2D))** for transverse and longitudinal
    plates under axial load.]
- **Through-plate (p.85):** for rectangular HSS, twice K1-9. For round HSS, use caution, because research
  shows less than twice.
- **Near a member end (p.84):** if a line load acts near an HSS end, the end is assumed to be **capped**,
  which restores similar strength.

#### 1.12 HSS-to-HSS truss joints (Ch.8, pp.98–129; Table 8-1 = AISC 360-16 Table K3.1)

**Classification (§8.3, pp.99–101, Figs 8-3, 8-4; Ex 8.5 p.123):**

- Classification follows how the force is transferred, not how the joint looks.
  - **K:** the branch punching load Pr·sinθ is balanced **within 20 %** by branches on the same side.
    This is checked as **0.8 ≤ ΣPc·sinθc / ΣPt·sinθt ≤ 1.2**.
  - **T/Y:** the punching load is reacted by chord beam shear.
  - **X:** the punching load is reacted by a load or branch on the **opposite face**.
- **Mixed joints:** check each branch by **linear interaction of its K share and its X (or Y) share**.
  Utilisation = (K part / K capacity) + (X part / X capacity) ≤ 1.0 (p.100, Fig 8-4).
- **Example 8.5 (pp.122–129) matches our top nodes:**
  - a roof truss with a purlin/beam load on the opposite face;
  - perpendicular force ratio 1.89 > 1.2;
  - the balanced part is checked as K (utilisation 0.31) and the remainder of the larger branch as an
    X-joint (utilisation 0.41);
  - total 0.72.
- **Very large gap:** if the gap makes e exceed the limit, treat the joint as two Y-joints (p.100).
- **Hidden toe of an overlap:** may be left unwelded (tacked only) if the two normal components differ by
  20 % or less (p.100). Not relevant here, because our joints are gapped.
- **Shared footprint:** for close or overlapping branches in an X-joint, the combined footprint can be
  taken as the loaded area (p.100, Ex 8.3).

**Modelling and member design (§8.4, pp.100–102):**

- Analyse either (1) pin-jointed, or (2) with web members pinned to **continuous chords**, adding stiff stubs
  of length e at each node (Fig 8-5).
- Branch moments from a rigid-frame analysis may be ignored.
- **The eccentricity moment** (ΣΔN·e) **may be ignored for joint design when e is within limits.**
  It **must still be used in chord member design**, shared between the two chord sides in proportion to
  stiffness (Ex 8.2 p.111; Ex 8.5 p.124).
- **Effective lengths permitted** with these joint rules: **chords KL = 0.9L**; **webs KL = 0.75L**
  (L = node to node) (p.102).
- Minimum weight is not minimum cost. Use few member sizes and few joints; Warren trusses suit this (p.102).

**Table 8-1 nominal strengths, round (p.103):**

- **Shear yielding (punching), all T/Y/X/gap-K**, when Db(tens or comp) < D − 2t:
  Pn = 0.6 Fy t π Db (1 + sinθ) / (2 sin²θ), φ 0.95 (K2-4 / K2-9).
- **T/Y chord plastification:** Pn sinθ = Fy t² (3.1 + 15.6β²) γ^0.2 Qf, φ 0.90 (K2-3).
- **X chord plastification:** Pn sinθ = Fy t² · [5.7 / (1 − 0.81β)] · Qf, φ 0.90 (K2-5).
- **K gap or overlap, chord plastification:**
  (Pn sinθ)comp = Fy t² (2.0 + 11.33 Db,comp/D) Qg Qf, and (Pn sinθ)tens = (Pn sinθ)comp, φ 0.90
  (K2-6, K2-8).
  - Qg = γ^0.2 · [1 + 0.024 γ^1.2 / (exp(0.5g/t − 1.33) + 1)] (K2-7).
  - For an **overlap**, use g = −q (negative) (Ex 8.2 p.112).
- Qf = 1 if the chord is in tension; otherwise 1 − 0.3U(1 + U), with U = |Pr/(A Fc) + Mr/(S Fc)| on the
  **lower-compression side**. In Ex 8.1, Fc = Fy (LRFD) or 0.6Fy (ASD) (p.108).

**Table 8-1A limits, round (p.104).** Identical to 360-16 Table K3.1A (spec PDF p.214), which adds an end distance:

- **−0.55 ≤ e/D ≤ 0.25** for K;
- **θ ≥ 30°**;
- **D/t ≤ 50** for T/Y/K and **≤ 40 for X**;
- **Db/tb ≤ 50** for tension (360-16: also compression) branches, and **Db/tb ≤ 0.05 E/Fyb** for
  compression branches;
- **0.2 < Db/D ≤ 1.0** for T, Y, X and overlapped K;
- **0.4 ≤ Db/D ≤ 1.0 for gapped K** (360-16: 0.4 < Db/D);
- **g ≥ tb,comp + tb,tens** for gapped K;
- overlap 25–100 %, with tb,overlapping ≤ tb,overlapped;
- **Fy, Fyb ≤ 52 ksi (360 MPa)**;
- **Fy/Fu ≤ 0.8**;
- **[360-16 only] l_end ≥ D(1.25 − β/2)** for T, Y, X and K, measured from the **near side of the branch
  to the chord end**.

**Geometry formulas (Ex 8.2 p.110; Ex 8.5 p.123):**

- Overlap length on the chord face: q = [Db1/(2 sinθ1) + Db2/(2 sinθ2)] − (e + D/2)·sin(θ1+θ2)/(sinθ1 sinθ2).
  Gap g = −q.
- Overlap Ov = q/p × 100 %, with p = Db,overlapping / sinθ.
- Inverse: e = [Db1/(2 sinθ1) + Db2/(2 sinθ2) + g]·sinθ1 sinθ2 / sin(θ1+θ2) − D/2.
- A gap of about 0.96 in. (24 mm) is described as just enough to weld (Ex 8.3, p.113).

#### 1.13 Rectangular truss joints (Table 8-2, 8-2A, pp.104–106) — for reference only

- Gapped K: Pn sinθ = Fy t² (9.8 βeff γ^0.5) Qf, φ 0.90.
- Plus punching, sidewall shear in the gap, and local yielding of the branch.
- Limits: B/t ≤ 35; Bb/B ≥ 0.1 + γ/50; βeff ≥ 0.35; ζ = g/B ≥ 0.5(1 − βeff); and others.
- Not used on T1.

#### 1.14 HSS-to-HSS moment joints (Ch.9, pp.130–147; = 360-16 Table K4.1)

- Covers T, Y and X joints with branch bending, for Vierendeel or PR/FR frames. **Not for triangulated
  trusses**, which should be analysed so that web moments are zero (p.130).
- Round, in-plane bending:
  - chord plastification: Mn sinθ = 5.39 Fy t² γ^0.5 β Db Qf (φ 0.90);
  - punching: Mn = 0.6 Fy t Db² (1 + 3 sinθ)/(4 sin²θ) (φ 0.95).
- Round, out-of-plane bending:
  - chord plastification: Mn sinθ = Fy t² Db · 3.0/(1 − 0.81β) · Qf;
  - punching: Mn = 0.6 Fy t Db² (3 + sinθ)/(4 sin²θ).
- Interaction: P/φPn + (Mip/φMn,ip)² + Mop/φMn,op ≤ 1.0 (p.132).
- Limits (Table 9-1A, p.133): θ ≥ 30°; D/t ≤ 50 (T/Y) and ≤ 40 (X); Db/tb ≤ 50 and ≤ 0.05E/Fyb;
  0.2 < β ≤ 1.0; Fy ≤ 360 MPa; Fy/Fu ≤ 0.8.
- **DG24 has no flange-plate or bolted chord splice in Ch.9.** Example 9.1 (p.135) is a welded round
  X-joint.

#### 1.15 Cap plate / beam on HSS column (Ch.4, Ex 4.1, pp.36–43) — relevant to the bearing

- Spread the load through the cap plate at **2.5:1**: width = 5tp + N.
- Check HSS wall local yielding and crippling on the loaded walls.
- Size the cap-plate-to-HSS weld assuming at most **45° dispersion**.
- Prying of the cap plate: Manual Part 9, "no prying" t_min.
- The Ch.4 list of beam-to-HSS moment connection types is for columns; not used on T1.

#### 1.16 Topics asked for but NOT in DG24

- **Saddle or stiffened round HSS seats.** No design rule. DG24 recommends unreinforced joints (p.83).
  The only reinforcement discussed is the through-plate (pp.84–85).
- **Seal-plate design.** Only §1.4.3 on sealed HSS.
- **Branch-end profiling or cutting rules.** Only that round overlapped joints need complex profiling and
  careful fit-up (p.83).
- **Effective weld length for round branches.** See AWS §9.5.4 (§1.6 above).
- Prequalified tubular groove/fillet details are referred to AWS D1.1 and Post (1990).

---

# Part E. Beca standard steelwork details, sheet SE-1505 "Fly bracing and purlin cleat connections"

File: `G:\My Drive\##Workset_Autocad\400 Standard Details\400 Standard Details\20 - STEELWORK\SE-1505 Fly Bracing
and Purlin Details\Drawing\1003461-SE-1505 FLY BRACING.pdf`. The sheet is marked "under revision" (plotted
18 Feb 2015); the superseded PDFs in `Drawing\Superseded` are earlier versions of the same details. It is reviewed
here as office practice, not as a code. Summary in my own words:

- **Details on the sheet:** A, typical fly bracing (rafter or column with a purlin or girt); B, the same for concrete
  walls (150 x 10 angle bracket with an M16 ferrule); C, typical purlin cleat; D, roof sheeting expansion joint;
  E, raking girt; F, cleat at an expansion joint (fly bracing on one side only); G, fly brace at haunches and
  rafters; H, at an ILB (lightweight) rafter; J, battened purlins. All at 1:10, each with the note "refer to the
  marking plan for locations (FB)".
- **Fly bracing geometry (A, G, H):**
  - Two equal angles "A", one each side of the member, from a cleat plate "B" (both sides) at the inner flange up
    to the purlin or girt.
  - Their gauge lines meet on the member centre line just beyond the flange.
  - The angle F is measured from the purlin. Connect to the end of the purlin lap when F is 35° – 55°, otherwise
    F = 45°. An extra bolt is needed when the brace does not land at the end of the lap.
  - The purlin lap is dimensioned "refer member schedule".
- **Fly bracing schedule:** member size against angle "A", cleat "B" and bolts "C" (member end / purlin end in the
  lapped zone / purlin end with no lap):

  | Member | Angle "A" | Cleat "B" | Bolts "C" (member / lapped / no lap) |
  |---|---|---|---|
  | ILB, rafter haunches, trusses | 90 x 90 x 8 EA | 10 | 1-M20 / 1-M20 / 2-M20 8.8/S |
  | 530 UB to 700 WB | 75 x 75 x 6 EA | 10 | 1-M20 / 1-M20 / 2-M20 8.8/S |
  | 410 UB to 460 UB | 65 x 65 x 6 EA | 8 | 1-M16 / 1-M16 / 2-M16 8.8/S |
  | 360 UB and smaller | 55 x 55 x 6 EA | 8 | 1-M16 4.6/S at every end |

  The schedule is empirical, for typical portal frames. SRT designs its brace instead (AISC 360-16 App. 6.2; see
  `STEEL_DETAILING_INSTRUCTION.md` S9A). That gives a lighter L 60 x 60 x 5 for this light truss, with the same
  connection pattern.
- **Purlin cleat (C):**
  - The cleat stands on the member's outer flange, parallel to the purlin web, with the purlin bolted to it.
  - Thickness by the cleat length "A": 0 – 250 mm → 8 PL, 250 – 350 mm → 10 PL, 350 – 450 mm → 12 PL, over 450 mm
    → 75 x 6 EA (at an expansion joint: 12 PL plus a stiffener).
  - Bolts are 2-M12 4.6/S, except 2-M16 4.6/S for 300 deep purlins and girts.
- **Expansion joint (F):** 100 mm long slotted holes in an extended cleat, fly bracing on one side only, and a side
  expansion joint in the cladding.
- **Applied on SRT-ST-5004 (2026-10-03):** section 1 at a braced node (1:20), cut from the 3001 elevation, with
  dashed callouts to the lug end (2/5004) and purlin end (3/5004) at 1:5; the purlin named on its own band; Table 6
  as the fly bracing schedule ("A", "B", "C" at each end, F, design force). Rules: `STEEL_DETAILING_INSTRUCTION.md`
  S9A, `ANNOTATION_ALIGNMENT_GUIDE.md` §9.7 – 9.8.
