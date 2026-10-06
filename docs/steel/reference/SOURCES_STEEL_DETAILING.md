# Steel detailing sources: AISC Detailing for Steel Construction, AISC Design Guides 4, 16, 21, 24, 25 and 29 (extracts)

Working extracts behind the steel drawing rules in `STEEL_DETAILING_INSTRUCTION.md` and the steel roof truss set
`jobs/steel_roof_truss` (SRT-ST). Reviewed 2026-10-03.

- Part A: AISC, *Detailing for Steel Construction* (3rd ed.), Ch. 3 - 4 (connections, truss connections, good
  practice, marks, welding, weld symbols). File `C:\Users\Peerapat\Downloads\Documents\Detailing_for_Steel_Construction.pdf`.
- Part B: the same book, Ch. 6 - 8 and Appendices A and D (erection drawings, anchor rods, trusses, camber, field bolt
  summary, detailing errors, checking).
- Part C: AISC Design Guide 21, *Welded Connections - A Primer for Engineers* (2006).
- Part D: AISC Design Guide 24, *Hollow Structural Section Connections* (2010).
- Part F: AISC Design Guide 4, *Extended End-Plate Moment Connections - Seismic and Wind Applications* (2nd ed., 2003).
- Part G: AISC Design Guide 16, *Flush and Extended Multiple-Row Moment End-Plate Connections* (2002).
- Part H: AISC Design Guide 25, *Frame Design Using Web-Tapered Members* (2011).
- Part I: AISC Design Guide 29, *Vertical Bracing Connections - Analysis and Design* (2014).
  Parts F - I reviewed 2026-10-04 for the steel portal-frame job `jobs/steel_portal_frame` (SPF); each has a
  "Use on this project" section with the calc steps, the drawing content and the open questions.
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

---

# Part F. AISC Design Guide 4 - Extended End-Plate Moment Connections (2nd ed.)


Working extract and review for the portal-frame job modelled in MIDAS GEN NX: 26 m gable frames at 10 m centres,
SM520 tapered welded sections, wind-governed (Thailand). The connections to design and detail are the knee
(column to rafter, both about 800 deep), the haunch-to-prismatic rafter splice, the ridge splice and the
canopy-to-column joint. Reviewed 2026-10-04.

**Page convention.** "p.NN" means the **PDF page** of
`Design Guide 04 - Extended End-Plate Moment Connections.pdf` (165 pp.), under
`G:\My Drive\##Textbook\AISC Design Guide\AISC - Steel Design Guides 2016\AISC - Steel Design Guides 2016\`.
Book page = PDF page − 7 (for example, p.38 = book p.31; p.62 = book p.55). PDF pp.1–7 are the cover, copyright,
acknowledgements and contents. The book text ends at p.63. PDF pp.64–165 are the Appendix B preliminary design
tables. Pages 91, 119 and 141 are blank.

**Basis warning.** DG4 2nd ed. is by T.M. Murray and E.A. Sumner, © 2003, first printing April 2004. The PDF
already carries the **errata of 3/3/05** in the yield-line tables (pp.32–36, boxed and marked "Errata").
Its basis is now out of date:
- **AISC LRFD Specification 1999** (3rd ed. Manual 2001): bolt Ft, Fv, bearing and the column web checks;
- **AISC Seismic Provisions 2002**: Ry, the CVN-rated filler metal;
- **AWS D1.1:2002**;
- **FEMA-350/353 (2000)**;
- the **Code of Standard Practice 2000**.

AISC 358 did not exist when DG4 was written. The same three connections were later prequalified in
**AISC 358 Chapter 6** (BUEEP/BSEEP). I checked the following against `a358-22w.pdf` (PDF pp.51–68) and
`a360-16-spec-and-commentary.pdf` (PDF pp.186–190):

| DG4 (2003) | AISC 358-22 Ch.6 / AISC 360-16 |
|---|---|
| Muc, connection design moment at the column face | Mf (358 §2.4.5 / §6.7.1 Step 4) |
| Mpe = 1.1 Ry Fy Zx | Mpr = Cpr Ry Fy Ze, with Cpr = (Fy+Fu)/(2Fy) ≤ 1.2 (358 §2.4.3) |
| Lp, hinge distance | Sh (Eq. 6.7-1 / 6.7-2, same values) |
| Four-bolt **h0 = outer row, h1 = inner row** | **358 renames: h1 = outer, h2 = inner** (Table 6.2). The 8ES numbering h1–h4 is unchanged |
| Ft = 90 ksi (A325), 113 ksi (A490) | Fnt = 90 ksi / 620 MPa (Group A), 113 ksi / 780 MPa (Group B), 360-16 Table J3.2. **Same numbers** |
| Fv = 48 ksi (A325-N), 60 ksi (A490-N), 1999 Table J3.2 | Fnv = 54 / 68 ksi (Group A N / X), 68 / 84 ksi (Group B N / X). **Higher now** |
| Plate thickness with φb = 0.9, bolts with φ = 0.75 | 358: φd = 1.00 for ductile limit states, φn = 0.90 for nonductile; tp,req uses φd |
| Plate shear yield φ = 0.9 | 360-16 J4.2(a): φ = 1.00 |
| Web yielding φCt(6kc + N + 2tp)Fyc twc | 358-22 Eq. 6.7-17: Rn = (6Ct kc + lb)Fyc tcw, lb = tbf + 2w + 2tp. **Ct multiplies only the 6kc term** in 358 |
| Tables 3.1–3.3 (Yp), 3.4–3.5 (Yc) | 358-22 Tables 6.2–6.4 (Yp), 6.5–6.6 (Yc): the same expressions, renamed |
| Tables 3.6 / 3.7, tested ranges | 358-22 Table 6.1: prequalification limits for seismic use only. **4E/4ES d is now limited to 13¾–24 in (350–600 mm)**, 8ES to 18–36 in (460–910 mm) |
| Web crippling, web buckling (1999 K1) | 360-16 J10.3, J10.5. Continuity plates J10.8; panel zone J10.6 |

**Copyright.** Everything below is paraphrased. Equations are restated in my own layout from the printed tables.
Tables are given only where the numbers are needed, in compact metric form.

**Read method.** Text was extracted with PyMuPDF for all 165 pages. Every equation and figure page was rendered and
viewed as an image: Fig. 2.8–2.10, the step pages 28–30, Tables 3.1–3.5 at 150 dpi, all the example pages 41–54
and Appendix B pp.62–65.

Notation (DG4 symbols, kept so that the calc can be checked line by line against the book):
- **Beam side:** d, bf (bfb), tf (tfb), tw (twb) = depth, flange width, flange thickness and web thickness of the
  beam or rafter at the end plate.
- **End plate:** bp, tp = width and thickness; Fyp, Fup = its yield and tensile strength.
- **Bolt layout:**
  - g = bolt gauge (horizontal, between the two bolt columns);
  - pfo, pfi = pitch from the outside / inside face of the tension flange to the nearer bolt row;
  - pb = row-to-row pitch (8ES);
  - de = distance from the outermost bolt row to the end of the plate.
- **Lever arms:** h0, h1 = lever arm from the centreline of the compression flange to the outer / inner bolt row
  (4E, 4ES). For 8ES, h1…h4 run from the outermost row inward.
- **Yield lines:** s = ½√(bp·g) = extent of the yield-line pattern beyond the bolts. Yp, Yc = yield-line parameters
  (length units) of the end plate and the column flange.
- **Bolts:** Pt = Ft·Ab = tensile strength of one bolt; Mnp = bolt moment with no prying.
- **Plate strengths:** Mpl, Mcf = flexural strength of the end plate and of the column flange.
- **Forces:** Muc = connection design moment at the column face; Ffu = Muc/(d − tf) = factored flange force;
  Vu = factored shear.
- **Column:** bfc, tfc, twc, kc, dc = column flange width and thickness, web thickness, k-distance and depth.
- **Column stiffeners:** ts, tsc = end-plate stiffener and column continuity-plate thickness; psi, pso = distance
  from the continuity plate to the inner / outer bolt row; c = pfo + tf + pfi = distance between the two bolt
  rows that straddle the flange.
- **Plate stiffener:** hst, Lst = height and length of the end-plate stiffener.


#### 1. Scope, configurations and applicability (Ch.1, pp.8–14)

- **Definition (p.8).** An end plate is shop-welded to the end of a beam and field-bolted with rows of
  pretensioned high-strength bolts. It joins either two beams (a **splice-plate connection**) or a beam to a column.
  - In a **flush** plate all bolts lie between the flanges. DG4 notes that flush plates are typical for light
    lateral load and **near the inflection points of gable frames**.
  - An **extended** plate projects past the tension flange so that bolts can sit outside it. It is the
    beam-to-column moment connection, with or without a stiffener.
- **The three configurations covered (Fig. 1.1, p.8):**
  - **4E**, four-bolt extended unstiffened: one bolt row each side of the tension flange, 2 bolts per row. It is
    the most common in multi-storey work.
  - **4ES**, four-bolt extended stiffened: as 4E, plus a triangular stiffener in the plane of the web between the
    flange and the extension. The stiffener lets the plate be thinner.
  - **8ES**, eight-bolt extended stiffened: two rows outside and two rows inside each flange, 2 bolts per row,
    with the stiffener. It develops the full moment of most rolled beams with bolts ≤ 1½ in.
  - For a full Mp demand with bolts ≤ 1½ in, 4E/4ES suffice for **less than half** of the rolled beam list, because
    bolt tension governs.
  - The plates are drawn symmetric (extended at both flanges) so that **moment reversal** is carried. This is
    needed for seismic load, and DG4 notes it **may not be needed for wind/gravity** (p.38). On our frames wind
    uplift reverses the moment, so keep them symmetric.
- **Seismic and wind.**
  - The procedures were developed and tested for FR (Type I) connections in **seismic** moment frames.
  - They apply to other loading "with proper adjustment of the required moment" (p.8): for wind/gravity, take Muc
    from the frame analysis (p.26, Step 1 note), as 4E Example B does.
  - For non-seismic work DG4 points to **DG16** (AISC/MBMA, Murray & Shoemaker 2002). DG16 covers 4 flush and
    5 extended layouts, multiple rows, and **snug-tightened bolts**. It has not been verified for high seismic use
    (p.9).
- **Advantages (p.9):** only field bolting (no field welding, so it suits fast erection); all welding is in the
  shop; plumbness is easy to keep if fabrication is accurate; the installed cost is competitive.
- **Disadvantages (p.9):**
  - beam length and end squareness must be accurate;
  - column depth and out-of-square tolerances are absorbed by making the beam short plus finger shims;
  - **end plates warp from the welding heat**;
  - **lamellar tearing** can occur in the plate at the tension-flange weld;
  - bolts are in tension, so prying is possible;
  - a stiffened plate may stand above the floor.
- **Research of interest to us (pp.10–14):**
  - Snug-tight bolts give the **same ultimate strength** with slightly lower initial stiffness, including under
    cyclic wind (Murray et al. 1992; p.11).
  - **Weld access holes** in end-plate beams caused early flange fracture under cyclic load and should not be used
    (Meng & Murray 1997; p.13).
  - **Built-up metal-building members** were tested with flush and extended plates (Boorse & Murray, Ryan & Murray
    1999; p.13). Flush plates could be made ductile. Extended plates should be designed so that the inelasticity
    goes into the beam, not the plate.
  - Prying becomes significant only after about **90 % of the yield-line plate strength** is reached
    (Borgsmiller 1995; p.10). This is the basis of the "thick plate" rule.


#### 2. Basis of the method (Ch.2, pp.16–21)

**2.1 Assumptions (p.16)**
1. All bolts are **pretensioned** to at least the AISC minimum. The connection is **not** slip-critical.
2. The procedure is valid for A325 or A490 bolts.
3. The smallest bolt pitch is the most economical. The minimum is pf = db + ½ in (db ≤ 1 in) or db + ¾ in (larger
   bolts). Many fabricators use a standard pf of 2 or 2½ in for every bolt size.
4. **All shear is carried by the bolts at the compression flange.** Shear is rarely critical.
5. The effective plate width in design is ≤ **bf + 1 in (25 mm)**. This is a judgement value, not a test result.
6. The **gauge must not exceed the beam tension-flange width**.
7. The **web-to-plate weld near the tension bolts develops the web yield stress**, even when the connection is
   designed for less than Mp.
8. Only the web weld **between mid-depth and the compression flange** carries the beam shear. This is a judgement
   value.

DG4 says column web stiffeners are expensive and should be avoided where possible:
- if a stiffener is only marginally needed, a heavier column is often cheaper;
- if the stiffeners are needed for flange bending, lengthen the effective flange instead, by increasing the bolt
  pitch or by going from a two-row layout (4E/4ES) to the four-row 8ES.

**2.2 Design moment for seismic use (pp.16–17, Fig. 2.1–2.2).**
- The philosophy is a strong column, a strong connection and a weak beam. Hinges form in the beam and the panel zone.
- **Expected beam moment:** Mpe = 1.1·Ry·Fy·Zx (Eq. 2.1). Ry = 1.1 for 50 ksi and 1.5 for 36 ksi (2002 values).
- **Hinge distance from the column face:**
  - unstiffened 4E: Lp = min(d/2, 3bf);
  - stiffened 4ES/8ES: Lp = Lst + tp (the hinge forms at the toe of the stiffener).
- **Moment at the column face:** Muc = Mpe + Vu·Lp (Eq. 2.2, 2.3; Eq. 3.1–3.4, p.27).
- **For wind design, Muc is the factored moment from the analysis at the face of the support.**

**2.3 Yield-line theory (pp.17–19, Fig. 2.3–2.4).**
- End-plate and column-flange bending use the virtual-work (upper-bound) yield-line method:
  - internal work Wi = Σ mp(θx·Lx + θy·Ly);
  - plastic moment per unit length mp = Fy·tp²/4;
  - external work We = Mpl·(1/h), where h runs from the compression-flange centreline to the tension edge of
    the plate;
  - s is found by minimising Wi.
- Simplifications:
  - bolt holes are ignored;
  - the web thickness is taken as zero;
  - weld sizes are ignored;
  - the small contribution of the compression zone is ignored.
- Result: Mpl = Fyp·tp²·Yp (nominal). The tables in §3 below give Yp and Yc for each layout.

**2.4 Bolt force model, the "thick plate" rule (pp.19–21, Fig. 2.5–2.6).**
- Kennedy's tee-stub model has three stages: thick (no prying), intermediate, and thin (maximum prying).
  Borgsmiller simplified it to thick or thin only, with the threshold at 90 % of the plate strength.
- DG4 requires the end plate **and** the column flange to stay **thick**. The bolts then see no prying, and the
  connection strength is the static moment of the full bolt strengths about the compression-flange centreline:
  - Mnp = Σ (n·Pt·hi) (Eq. 2.7), with n = bolts per row;
  - Pt = Ft·Ab (Eq. 2.8), with Ab the nominal (gross) bolt area.
- **Thick-plate condition:** φMnp ≤ 0.9·φbMpl and φMnp ≤ 0.9·φbMcf. Equivalently, the plate and the flange must be
  ≥ 1.11 × the bolt moment (Eq. 2.9–2.10, p.21).
- The plate is therefore sized from the **bolt strength actually provided**, not only from the demand.
  Oversizing the bolts makes the plate thicker.
- Thin plate or thin flange: the DG4 procedure does not apply, because bolt rupture with prying becomes a limit
  state. Use DG16 (§3.3, pp.30–31).

**2.5 Limit states to check (p.21):**
1. end-plate flexural yielding near the tension bolts;
2. end-plate shear yielding;
3. shear rupture of an unstiffened extension through the outer bolt line;
4. **bolt tension rupture**, the brittle and most critical one;
5. bolt shear;
6. bearing and tearout of the plate or column flange;
7. tension-flange and web welds;
8. web weld and web metal in shear;
9. column web yielding;
10. column web crippling;
11. column web buckling;
12. column flange bending;
13. continuity plate yielding, buckling or weld;
14. panel zone shear yielding or web buckling.


#### 3. Design procedure and equations (Ch.3, pp.26–37)

Twenty steps (pp.27–30). Units are consistent (N, mm, MPa), since every expression is dimensionally homogeneous.
Resistance factors are as printed in DG4; the current values are in the basis table above.

**Beam (end-plate) side**

1. **Muc**:
   - seismic: Eq. 3.1–3.4, see §2.2 above;
   - wind: from the analysis.
2. **Choose the layout** (4E / 4ES / 8ES) and a trial geometry: g, pfi, pfo, pb, de, bp; then the bolt grade.
   - Lever arms: h0 = d + pfo − tf/2 (outer row) and h1 = d − tf − pfi − tf/2 (inner row) (p.39).
   - 8ES (p.50):
     - h1 = d + pfo + pb − tf/2;
     - h2 = d + pfo − tf/2;
     - h3 = d − tf − pfi − tf/2;
     - h4 = h3 − pb.
3. **Required bolt diameter** (Eq. 3.5 / 3.6, p.27), with φ = 0.75:
   - 4E/4ES: db,req = √[ 2·Muc / (π·φ·Ft·(h0 + h1)) ];
   - 8ES: db,req = √[ 2·Muc / (π·φ·Ft·(h1 + h2 + h3 + h4)) ].
4. **Pick db ≥ db,req** (Eq. 3.7–3.9):
   - Pt = Ft·π·db²/4;
   - 4E/4ES: Mnp = 2·Pt·(h0 + h1);
   - 8ES: Mnp = 2·Pt·(h1 + h2 + h3 + h4);
   - check φMnp ≥ Muc.
5. **Required plate thickness** (Eq. 3.10, p.28), with φ = 0.75 and φb = 0.90:
   tp,req = √[ 1.11·φ·Mnp / (φb·Fyp·Yp) ]. This puts the plate at 111 % of the no-prying bolt moment.
6. Choose **tp ≥ tp,req**.
7. **Flange force:** Ffu = Muc / (d − tf) (Eq. 3.11).
8. **4E only, shear yielding of the extension** (Eq. 3.12): Ffu/2 ≤ φ·0.6·Fyp·bp·tp, φ = 0.9.
9. **4E only, shear rupture of the extension** (Eq. 3.13–3.14): Ffu/2 ≤ φ·0.6·Fup·An, φ = 0.75,
   An = [bp − 2(db + 1/8 in)]·tp (standard holes; metric: hole + 2 mm).
10. **4ES/8ES stiffener** (Eq. 3.15–3.16, p.28):
    - thickness ts ≥ twb·(Fyb/Fys);
    - local buckling hst/ts ≤ 0.56√(E/Fys), i.e. ts ≥ 1.79·hst·√(Fys/E);
    - the welds develop the stiffener in **shear at the flange** and in **tension at the plate**;
    - stiffener-to-plate weld is **CJP if ts > 3/8 in (10 mm)**, fillets otherwise; flange weld is fillet or CJP.
11. **Bolt shear** (Eq. 3.17): Vu ≤ φ·nb·Fv·Ab, with φ = 0.75 and nb = the bolts at **one** (compression) flange:
    4 for 4E/4ES, 8 for 8ES.
12. **Bearing and tearout** of the plate and of the column flange (Eq. 3.18–3.19, p.29):
    - Vu ≤ ni·φRn(inner) + no·φRn(outer), φ = 0.75;
    - Rn = 1.2·Lc·t·Fu ≤ 2.4·db·t·Fu per bolt;
    - Lc = clear distance in the line of force to the next hole or to the edge.
13. **Flange-to-plate and web-to-plate welds**: see §4.3.

**Column side** (beam-to-column only; for a splice the mating end plate replaces the column flange)

14. **Column-flange bending** (Eq. 3.20, p.29): tfc,req = √[ 1.11·φ·Mnp / (φb·Fyc·Yc) ] ≤ tfc.
    - Use **Yc unstiffened** (Tables 3.4 / 3.5) first.
    - If it fails, use a heavier column or **continuity plates**, then recheck with Yc stiffened.
15. **If stiffened, the stiffener force:**
    - φMcf = φb·Fyc·Yc,unstiff·tfc² (Eq. 3.21);
    - φRn = φMcf / (d − tf) (Eq. 3.22).
16. **Web local yielding** (Eq. 3.24): φRn = φ·Ct·(6kc + N + 2tp)·Fyc·twc ≥ Ffu, where:
    - φ = 1.0;
    - **Ct = 0.5 if the beam top flange is less than dc below the column top**, 1.0 otherwise;
    - N = tf + 2 × the groove-weld reinforcement. The example uses N = tf + 0.707w for fillets (p.45); 358-22
      uses lb = tf + 2w + 2tp;
    - **for a built-up column take kc = tfc + flange-to-web weld size** (358-22 wording, "or fillet weld").
17. **Web compression buckling** (Eq. 3.26–3.27, pp.29–30), φ = 0.9:
    - load ≥ dc/2 from the column end: φRn = φ·24·twc³·√(E·Fyc) / h;
    - load < dc/2 from the column end: **12** in place of 24;
    - h = clear distance between flanges less the fillet for rolled shapes, and the **clear distance between
      flanges for welded built-up shapes**.
18. **Web crippling** (Eq. 3.29–3.31, p.30), φ = 0.75:
    - load ≥ dc/2 from the end: φRn = φ·0.80·twc²·[1 + 3(N/dc)(twc/tfc)^1.5]·√(E·Fyc·tfc/twc);
    - load < dc/2 from the end: 0.40 replaces 0.80 when N/dc ≤ 0.2; when N/dc > 0.2 the bracket becomes
      [1 + (4N/dc − 0.2)(twc/tfc)^1.5].
19. **Continuity-plate force:** Fsu = Ffu − min(φRn from Steps 15–18) (Eq. 3.32). The book's text says "Step 5"
    for crippling; this is a typo for Step 18. Design the plates to **DG13**.
20. **Panel-zone shear yielding and web buckling**: to DG13 and the Seismic Provisions. DG4 gives no equation.

**Analysis mode (§3.3, pp.30–31).** For a given geometry:
- compute φbMpl, φbMcf and φMnp;
- **thick** if Mpl > 1.1·Mnp and Mcf > 1.1·Mnp (Eq. 3.33–3.36), and then **φMn = φMnp**;
- if either is thin, the method does not apply (use DG16).

**Large inner pitch (p.26).** If pfi > s, a straight yield line forms between the flange and the inner bolts.
Set pfi = s in Yp (and psi = s in Yc).

##### 3.1 Yield-line parameters, end plate (Tables 3.1–3.3, pp.32–34; errata 3/3/05 included)

s = ½·√(bp·g); if pfi > s, use pfi = s. Then φMpl = φb·Fyp·tp²·Yp with φb = 0.90.

```
4E   (Table 3.1, p.32)
Yp = bp/2·[ h1·(1/pfi + 1/s) + h0·(1/pfo) − 1/2 ] + 2/g·[ h1·(pfi + s) ]

4ES  (Table 3.2, p.33)  Case 1, de ≤ s:
Yp = bp/2·[ h1·(1/pfi + 1/s) + h0·(1/pfo + 1/(2s)) ] + 2/g·[ h1·(pfi + s) + h0·(de + pfo) ]
                        Case 2, de > s:
Yp = bp/2·[ h1·(1/pfi + 1/s) + h0·(1/s + 1/pfo) ]    + 2/g·[ h1·(pfi + s) + h0·(s + pfo) ]

8ES  (Table 3.3, p.34)  Case 1, de ≤ s:
Yp = bp/2·[ h1/(2de) + h2/pfo + h3/pfi + h4/s ]
   + 2/g·[ h1·(de + pb/4) + h2·(pfo + 3pb/4) + h3·(pfi + pb/4) + h4·(s + 3pb/4) + pb² ] + g
                        Case 2, de > s:  as Case 1 with h1/(2de) → h1/s and (de + pb/4) → (s + pb/4)
```

Bolt rupture (same tables): φMnp = φ·2·Pt·(h0 + h1) for four-bolt layouts and φ·2·Pt·(h1 + h2 + h3 + h4) for 8ES,
with φ = 0.75.

##### 3.2 Yield-line parameters, column flange (Tables 3.4–3.5, pp.35–36)

s = ½·√(bfc·g); c = pfo + tf + pfi; if psi > s, use psi = s. Then φMcf = φb·Fyc·tfc²·Yc.

```
4-bolt, unstiffened flange (Table 3.4, p.35)
Yc = bfc/2·[ h1/s + h0/s ] + 2/g·[ h1·(s + 3c/4) + h0·(s + c/4) + c²/2 ] + g/2

4-bolt, stiffened flange (continuity plates in line with both beam flanges)
Yc = bfc/2·[ h1·(1/s + 1/psi) + h0·(1/s + 1/pso) ] + 2/g·[ h1·(s + psi) + h0·(s + pso) ]

8-bolt, unstiffened flange (Table 3.5, p.36)
Yc = bfc/2·[ h1/s + h4/s ]
   + 2/g·[ h1·(pb + c/2 + s) + h2·(pb/2 + c/4) + h3·(pb/2 + c/2) + h4·s ] + g/2

8-bolt, stiffened flange
Yc = bfc/2·[ h1/s + h2/pso + h3/psi + h4/s ]
   + 2/g·[ h1·(s + pb/4) + h2·(pso + 3pb/4) + h3·(psi + pb/4) + h4·(s + 3pb/4) + pb² ] + g
```

With continuity plates of thickness ts centred on the flange, the examples take psi = pso = (c − ts)/2 (pp.40, 52).

**Column-end caveat (from 358-22, p.65 of that file):** the Yc tables assume the top bolt row is **more than s
below the column end**. DG4 has no yield-line solution for a flange at the column top. This matters for the knee
(§6).

##### 3.3 Tested parameter ranges (Tables 3.6 cyclic and 3.7 monotonic, p.37), restated in mm

DG4 warns (p.31) that going well outside these ranges may change the failure mechanism. For **wind design use
Table 3.7 (monotonic)**:

| Parameter | 4E min – max | 4ES min – max | 8ES min – max |
|---|---|---|---|
| tp | 9.5 – 57 | 9.5 – 35 | 19 – 64 |
| bp | 127 – 270 | 203 – 270 | 229 – 381 |
| g | 64 – 178 | 70 – 152 | 127 – 152 |
| pf (pfi, pfo) | 32 – 114 | 25 – 137 | 35 – 51 |
| pb | – | – | 70 – 95 |
| d (beam) | 254 – 1622 | 349 – 610 | 467 – 914 |
| tf (beam) | 6.4 – 25.4 | 9.5 – 19 | 15.9 – 25.4 |
| bf (beam) | 102 – 260 | 152 – 229 | 194 – 311 |
| db | 12.7 – 31.8 | 15.9 – 31.8 | 22.2 – 31.8 |

Table 3.6 (cyclic) is narrower:
- 4E: d 635–1397 mm, tf 9.5–19, db 22–32;
- 4ES: d 349–610;
- 8ES: d 467–914, tf 15.9–25.4, db 29–32.

For seismic prequalification, use 358-22 Table 6.1 instead (see the basis table).


#### 4. Detailing and fabrication rules (§2.4, pp.21–25; Fig. 2.7–2.10)

**4.1 Bolt layout (pp.22–23, Fig. 2.7)**
- **Gauge g:**
  - wide enough to install and tighten the bolts and, beam-to-column, to clear the column web-to-flange fillets
    (the "workable gauge");
  - **never wider than the beam flange**, so that the flange force has a direct path to the bolts.
- **Pitch to flange pf** (pfi, pfo, from the flange face to the bolt centreline):
  - absolute minimum **db + 13 mm (½ in) for db ≤ 25 mm**, **db + 19 mm (¾ in) above**;
  - tension-control bolts may need more for the wrench;
  - fabricators often use a standard 50 or 64 mm.
- **Row pitch pb:** ≥ **2⅔·db**, preferably **3·db**.
- **End-plate width:**
  - **bp ≥ beam flange width**, typically bf + 25 mm rounded to a stock width;
  - the extra width gives fit-up tolerance and a weld run-off area;
  - the **effective bp in the calc is ≤ bf + 25 mm**.
- **de**: the examples use 41 mm (1⅝ in) for 1–1¼ in bolts and 32 mm for the 8ES. de also selects Case 1 or
  Case 2 in Tables 3.2/3.3. Also satisfy 360-16 Table J3.4M (M20 26, M22 28, M24 30, M27 34, M30 38 mm).
- Do not camber beams with end plates: the end rotation upsets fit-up (p.21).

**4.2 End-plate stiffener, 4ES/8ES (p.23, Fig. 2.8; 358-22 §6.6.4)**
- **Load path.** The stiffener acts as an extension of the beam web. The flange force spreads into it at **30°**
  (the Whitmore idea).
- **Length** along the flange: **Lst = hst / tan 30° = 1.732·hst** (Eq. 2.11). hst = height of the plate from the
  outside face of the flange to the end of the plate: pfo + de for 4ES, pfo + pb + de for 8ES.
- **Landings** about **25 mm (1 in)** at both ends: at the flange and at the end of the plate. The landings give a
  definite stop for the plate and its welds.
- **Clip** the inside corner to clear the flange-to-plate weld.
- **Thickness:** ts ≥ twb (same grade), else ts ≥ twb·Fyb/Fys; also hst/ts ≤ 0.56√(E/Fys).
  - In the 8ES example (p.51) the buckling criterion governs: hst = 152 mm needs ts ≥ 11.4 mm, and 12.7 mm (½ in)
    is used.
- **Welds:** fillets only if ts ≤ 10 mm (3/8 in); otherwise CJP (single or double bevel) (p.25).

**4.3 Welding the beam to the plate (pp.24–25, Fig. 2.10)**
- The procedure is written for cyclic load and is **recommended, "although not absolutely necessary", for wind
  and low-seismic** work (p.24).
- Filler metal for seismic use: CVN ≥ 27 J (20 ft-lb) at −29 °C (−20 °F) (2002 rule; AISC 341-16 now has its own
  demand-critical rule).
- **Web-to-plate weld:**
  - fillet or CJP, sized to **develop the web in tension near the tension bolts** (assumption 7);
  - a large fillet may be replaced by a CJP;
  - **the web weld is made first**, so that its shrinkage does not stress the flange welds;
  - 358-22 adds: develop the web from the inside face of the flange to 150 mm past the farthest inner bolt row.
- **Flange-to-plate weld:**
  - **CJP if tf > 10 mm (3/8 in)**; double fillets may be used for thinner flanges;
  - the CJP is a full-depth 45° bevel with minimal root opening (similar to AWS prequalified TC-U4b-GF), with the
    **root on the web side**;
  - the root is backed by an **8 mm (5/16 in) fillet on the web side** of the flange, then back-gouged to sound
    metal before the groove is filled;
  - no back-gouge directly over the web, where the backing fillet cannot be placed;
  - **no weld access holes in the web.**
- **Weld sequence (Fig. 2.10):** bevel the flanges → fit up → preheat to AWS → web welds (1) → 8 mm backing
  fillets (2) → back-gouge (3) → flange groove welds.
- **Wind practice (4E Example B, pp.44–45):** fillet welds on a 13 mm flange are accepted.
  - Design force = **max(Ffu, 0.6·Fy·Afb)**. The 0.6FyAfb floor is a judgement value: it keeps small welds off
    stiff beams and allows for uneven force distribution across the flange.
  - Effective length = bf + (bf − tw), both faces.
  - The **1.5 directional factor** for transversely loaded fillets is used.
- **Web weld arithmetic.** The book's shorthand D = 0.6·Fy·tw / (2 × 1.392) (sixteenths, E70) gives the same size
  as φFy·tw with φ = 0.9 against two fillets with the 1.5 directional factor (both 4.04/16 in).
  - Metric, E70/E49XX, two fillets: **w ≥ 0.943·Fy·tw / FEXX**. Then apply the AISC 360 Table J2.4 minimum for
    the plate thickness (5/16 in for a 7/8 in plate in the example).
- **Shear weld:** only the length between mid-depth and the compression flange, or between (inner tension bolts
  + 2db) and the compression flange, whichever is shorter (p.40).

**4.4 Fit-up tolerances and finger shims (p.9, p.24, Fig. 2.9)**
- The column is drilled to the plate pattern, so there is almost no adjustment.
- Cited tolerances:
  - beam length (Code of Standard Practice): 1.6 mm (1/16 in) up to 9 m and 3 mm (1/8 in) beyond;
  - rolled depth (ASTM A6): ±3 mm.
- **Detail the beam 5–10 mm short** and fill the gap with **finger shims**: plates about 1.6 mm (1/16 in) thick, slotted
  to slide over the bolts from the side.
  - A skewed flange or plate is corrected with more shims on one side.
  - Tests showed no adverse effect. 358-22 §6.6.5 permits shims at top and/or bottom, within the RCSC limits.
  - DG4 is inconsistent here: it gives 1/4–3/8 in on p.9 and 3/16–3/8 in on p.24.

**4.5 Composite slab (p.24).** Not used on this job (no slab on the rafters). For record:
- no studs within 1.5d of the column face;
- compressible joint of ≥ 13 mm at the column;
- minimum slab steel within 2d.


#### 5. Tapered, built-up and sloped members: what DG4 says

**DG4 does not address tapered members, haunches, sloped rafters or knee joints.** Its procedure and every example
is a horizontal rolled W-beam meeting a W-column at 90°. The only points that bear on our members:
- **Gable frames:** flush plates are typical near the inflection points of gable frames (p.8).
- **Built-up metal-building members** were tested (p.13).
  - Extended plates on built-up members should be **designed strong** (thick plate), with the yielding in the member.
  - DG16 (AISC/MBMA) is the guide written for metal-building frames: flush and extended, multiple-row, snug or
    pretensioned bolts, wind and low seismic.
- **Built-up column web:** for web buckling, h is the clear distance between flanges (p.30).
  - 358-22 takes kc as tfc + the flange-to-web fillet for welded columns, and (§6.3.1) requires the web-to-flange
    welds of a built-up beam end, within min(d, 3bf), to be CJP or fillets ≥ 0.75·tw (≥ 6 mm).
  - For **wind** use this is a 358 seismic rule; recommended practice, not mandatory.
- **Non-rolled sections.** The yield-line and bolt models use only the local geometry at the plate: d, tf, bf, tw
  at the end, bp, g, pf, pb, de. Nothing in them depends on the member being rolled or prismatic.

**My reading for this project (engineering inference, not DG4 text):**
- **Tapered end:** use the member geometry **at the plate**, i.e. the depth and flanges of the cut end. A taper
  that continues into the stiffener zone does not change Yp.
- **Sloped rafter on a vertical plate (knee):** the rafter flanges meet the plate at 90° ± 18°.
  - Measure d, h0, h1, pf **along the plate** (vertical) between the flange-to-plate intersection points.
    Sloped parallel flanges make the vertical depth = d⊥ / cos 18°.
  - Take moments about the compression-flange intersection.
  - The CJP or fillet flange weld becomes a **skewed T-joint** (dihedral angle about 72° / 108°). Check the AWS
    D1.1 prequalified dihedral-angle and fillet-size rules for skewed T-joints, and show the angle and the
    weld on the detail.
- **Axial force:** DG4 ignores it (beams). Rafters and columns carry it, and at the knee it is the frame thrust.
  - Resolve N and V of the member into components normal and parallel to the plate.
  - Add the normal **tension** component to the bolt demand: M* = Mu + Nu,normal × (distance from the
    compression-flange centreline to the member centroid ≈ (d − tf)/2), taken about the compression flange.
  - Ignore any compression relief, conservatively.
  - The in-plane component adds to the bolt shear (Step 11).
- **Haunch bottom flange at the knee** (if the haunch flange is not parallel to the rafter top flange): its force
  normal to the plate is F·cos α. The parallel component F·sin α goes into the plate as shear and must be carried
  by the web weld and bolt shear. Show the haunch flange angle on the detail.
- **Column side at the knee:** the column top is less than dc above the rafter top flange.
  - Use **Ct = 0.5** (web yielding) and the "< dc/2 from the end" forms of web buckling (12 in place of 24) and
    crippling.
  - The DG4 Yc tables are **not valid** where the outer bolt row is within s of the column top. Provide a cap plate
    and continuity plates, and treat the flange as stiffened (Yc stiffened with pso measured to the cap plate),
    or extend the column above the outer bolts by at least s.
  - This choice is open (§6.5).


#### 6. Worked examples (Ch.4, pp.38–54), with the wind example in full

All examples use a W21×55 beam on a W14×109 column, A992 (Fy 345 MPa), A572 Gr 50 plate, and Vu = 40 kips (178 kN).
The connections are symmetric for reversal.

**6.1 4E Example B, wind / low seismic (pp.43–47).** **Use this one to test the Python calc.** Inputs, with metric
in brackets:
- Beam W21×55: d 20.8 in (528 mm), tw 0.375 (9.5), bf 8.22 (209), tf 0.522 (13.3), Zx 126 in³ (2.065×10⁶ mm³),
  Fy 50 ksi (345 MPa), Fu 65 ksi (448 MPa).
- Column W14×109: dc 14.3 (363), twc 0.525 (13.3), bfc 14.6 (371), tfc 0.860 (21.8), kc 1.46 (37.1), h/tw 21.7.
- **Muc = 4000 k-in (451.9 kN·m)**, taken from analysis. DG4 notes Muc < φMp = 0.9·50·126 = 5670 k-in (640.6 kN·m).
- Plate: bp 9.0 in (229), g 5½ (140), pfi = pfo 2.0 (51), de 1⅝ (41); Fyp 50, Fup 65 ksi.
- Bolts **A325**, Ft 90 ksi (620 MPa). The text of the example says A490, but it uses A325 throughout (book
  inconsistency).

Results, in step order:

| Step | Quantity | Book value | Metric |
|---|---|---|---|
| 2 | h0 = d + pfo − tf/2 ; h1 = d − tf − pfi − tf/2 | 22.54 ; 18.02 in | 572.5 ; 457.7 mm |
| 3 | db,req (Eq. 3.5) | 0.96 in | 24.4 mm |
| 4 | db = 1 in A325: Pt = Ft·Ab | 70.7 kips | 314.5 kN |
| 4 | Mnp = 2Pt(h0 + h1) ; φMnp (φ = 0.75) | 5735 ; 4301 k-in (> 4000 OK) | 648 ; 486 kN·m |
| 5 | s = ½√(bp g) (> pfi, so pfi stays 2.0) | 3.52 in | 89.4 mm |
| 5 | Yp (Table 3.1) | 148.2 in | 3764 mm |
| 5 | tp,req = √(1.11·φMnp / (φb Fyp Yp)) | 0.85 in | 21.6 mm |
| 6 | tp chosen | 7/8 in | 22.2 mm |
| 7 | Ffu = Muc/(d − tf) | 197 kips | 876 kN |
| 8 | Shear yield φRn (≥ Ffu/2 = 98.5 kips) | 213 kips | 947 kN |
| 9 | An = [9.0 − 2(1.125)]·0.875 ; φRn | 6.13 in² ; 179 kips | 3955 mm² ; 796 kN |
| 11 | Bolt shear 4 bolts, Fv 48 ksi (1999 A325-N) | 113 kips (> 40) | 503 kN |
| 12 | Bearing 2.4·db·tp·Fu per bolt ; tearout outer Lc = 3.46 in → 236 kips | 137 kips | 609 kN |
| 12 | Plate total 4 × 0.75 × 137 ; column flange (× tfc/tp) | 411 ; 404 kips | 1828 ; 1797 kN |
| 13 | Flange fillet: max(Ffu = 197, 0.6FyAfb = 129) kips over bf + (bf − tw) = 16.1 in → 5.86/16 | **3/8 in fillet** both faces | 9.5 mm |
| 13 | Web fillet (tension develop.) 4.04/16 ; shear length d/2 − tf = 9.88 in → 1.45/16 | **5/16 in fillet** both faces | 8 mm |
| 14 | Column: s ; c = pfo + tf + pfi | 4.48 ; 4.52 in | 113.8 ; 114.8 mm |
| 14 | Yc unstiffened (Table 3.4) | 170.1 in | 4321 mm |
| 14 | tfc,req (vs tfc 0.860 in) | 0.790 in, OK | 20.1 mm |
| 16 | Web yield, Ct = 1.0, N = tf | 289 kips (> 197) | 1286 kN |
| 17 | Web buckling (h = 11.39 in) | 330 kips | 1468 kN |
| 18 | Web crippling | 268 kips | 1192 kN |
| — | **Result** | PL 7/8 × 9 in, 1 in A325-N in 1-1/16 in holes, no column stiffeners | PL 22 × 229 |

Book typos to ignore when checking:
- Mnp is printed once as "5375" (correct: 5735);
- Step 9 prints "109 ≤ 197" (correct: 98.5 ≤ 179);
- Ex A Step 14 cites "Eq. 3.17" for the flange (correct: 3.20);
- the 4ES example writes Fyc, Yc in Eq. 3.10 (correct: Fyp, Yp).

The final detail is drawn on p.47: plan and elevation with every dimension (bfc, twc, g, bfb, bp; de, pfo, tfb, pfi,
c; tfc, tp; d) plus the bolt callout and the weld symbols. It is a good model for our detail (§7.4).

**6.2 4E Example A, seismic (pp.38–42).**
- Mpe = 1.1·1.1·50·126 = 7623 k-in; Lp = min(d/2, 3bf) = 10.4 in; Muc = 8039 k-in (908 kN·m).
- Bolts: A490, db,req 1.22 → **1¼ in**, φMnp 8438 k-in.
- Plate: Yp 148.2 in → tp,req 1.19 → **1¼ in** plate.
- **Column flange fails unstiffened:** tfc,req 1.11 in > 0.860. With ½ in continuity plates, psi = pso = 2.01 in,
  Yc = 309.1 in and tfc,req = 0.82 in, OK.
- Web yielding 309, buckling 330 and crippling 268 kips are all below Ffu 396 kips, so **Fsu = 396 − 268 = 128 kips**
  (569 kN) for the continuity plates.
- Note how the seismic Muc (× 2 of the wind case) doubles the plate thickness and forces stiffeners.

**6.3 4ES (pp.48–49).** The same as Example A with a stiffener:
- de 1⅝ in < s = 3.52 in, so Case 1;
- Yp = 194.6 in → tp **1⅛ in**;
- stiffener: hst = pfo + de = 3.625 in, Lst = 6.3 → 6½ in, ts = 3/8 in (= tw), hst/ts = 9.7 ≤ 13.5;
- 5/16 in fillets.

**6.4 8ES (pp.50–54).**
- Lp = Lst + tp ≈ 11.5 in, Muc 8083 k-in.
- Geometry: pfi = pfo = 1¾ in, pb = 3 in, de 1¼ in; h1…h4 = 25.29 / 22.29 / 18.27 / 15.27 in.
- Bolts: **1 in A325**, φMnp 8603 k-in. Plate: Yp = 277.6 in → tp **7/8 in**.
- Stiffener: hst = 6.0 in, Lst = 10.4 → 10½ in; ts = ½ in, set by local buckling.
- Column: Yc unstiffened 224.6 in → 0.97 in > 0.860, so stiffened (Yc = 377.7) → 0.75 in OK; Fsu = 399 − 268 =
  131 kips.
- **Lesson:** the 8ES gets the same moment with smaller bolts and a thinner plate than the 4E.

**6.5 Appendix B, preliminary design tables (pp.62–165).**
- Tables 4E / 4ES / 8ES × A325 / A490: φMn, db, bp, tp (36 and 50 ksi plate), and the minimum column flange
  thickness (unstiffened and stiffened) for 10, 12, 14 and 16 in column flanges.
- Basis: Fy 50 ksi rolled beams; pf = db + ½ in (≤ 1 in) or db + ¾ in; 8ES pb = 3 in; de < s; c = 2pf + tf.
- **Imperial W-shapes only.** Not usable for our welded SM520 sections, except as a sanity check of the Python calc.


#### 7. Use on this project

##### 7.1 Bolt grades: how DG4's grades map

| DG4 / AISC | Fu min | Thai/Japanese/ISO equivalent | Fu min | AISC 360-16 group | Fnt to use |
|---|---|---|---|---|---|
| A325 / F3125 Gr A325 (A325M) | 830 MPa (120 ksi) | JIS F8T; ISO 8.8 | 800 / 830 MPa | Group A | 620 MPa (A325M); **0.75·Fu = 600 MPa for F8T** |
| A490 / F3125 Gr A490 (A490M) | 1040 MPa (150 ksi) | **JIS F10T / S10T (TC)**; ISO 10.9 (EN 14399 HR/HV) | 1000 / 1040 MPa | Group B | 780 MPa (A490M); **0.75·Fu = 750 MPa for F10T** |

- AISC sets Fnt = 0.75·Fu on the **gross** area, which allows for the threads. For a non-ASTM bolt apply the same
  ratio to the bolt's own Fu. Take Fnt = **750 MPa for F10T** (conservative against 780) and 0.75 × 1040 = 780 MPa
  for ISO 10.9.
- Shear: Fnv ≈ 0.45·Fu with threads included (N) and ≈ 0.56·Fu with threads excluded (X), following the 360-16
  ratios.
- **Pretension** (DG4 assumption 1; 358 Ch.4): 360-16 Table J3.1M, Group B (A490M):

  | Bolt | M20 | M22 | M24 | M27 | M30 |
  |---|---|---|---|---|---|
  | Group B pretension (kN) | 179 | 221 | 257 | 334 | 408 |
  | Group A (A325M) (kN) | 142 | 176 | 205 | 267 | 326 |

  For comparison, the JIS F10T **standard (installation) bolt tension** that I recall is M20 182, M22 226,
  M24 262 kN (design bolt tension 165 / 205 / 238 kN). **Verify against JIS B 1186 / JASS 6 before use.**
  - Specify pretensioned F10T (or S10T TC bolts) tightened to the JIS standard tension, which meets or exceeds
    the AISC minimum.
  - Not slip-critical; class N (threads in the shear plane) for the shear check.
  - **Hot-dip galvanized F10T is not available in JIS.** If the bolts must be galvanized, use F8T-galv
    (JIS B 1186 HDG) or an ISO 10.9/8.8 HDG set, and redo the calc with the lower Fu.
- 358-22 also prohibits weld access holes and requires pretension for the seismic case. For wind, DG16 permits
  snug-tight bolts. **Recommend pretensioned anyway**: frames are bolted once, the reversing wind load cycles, and
  the "thick plate" model assumes pretension.

##### 7.2 Configuration for each joint

| Joint | Geometry at the plate | Recommended | Why / check |
|---|---|---|---|
| **Knee** (rafter haunch ~800 × 250 × 6 × 12 on column ~800 × 250 × 8 × 14) | sloped rafter (18°) on the vertical column outer flange | **4E, symmetric** (extended above the top flange and below the haunch flange) | Only 4E has d = 800 inside the DG4 tested range (Table 3.7: 254–1622 mm). 4ES is limited to d ≤ 610; 8ES needs tf ≥ 15.9 mm (ours is 12). bp ≤ 270 mm (Table 3.7 max), so use **bp = 270** (bf + 20). If the bolts run out, **8ES with thicker local flanges** or a **multiple-row DG16 layout** (e.g. an extra inner row) |
| **Haunch-to-prismatic splice** at 5.2 m (both ends 350 deep; haunch flange 250 × 12 against prismatic 200 × 10) | plate-to-plate splice, perpendicular to the rafter | **4E symmetric**, or **flush 4-bolt** if the moment is small (DG16) | Moment reverses (gravity hogging vs wind uplift). Gauge g ≤ **the narrower flange (200)**. Size each plate for its own member; the "column flange" check becomes the mating plate (same Yp) |
| **Ridge splice** (350 × 200 × 6 × 10 both sides, 18° each) | vertical plate on the bisector | **4E symmetric** (or flush if small) | Sagging under gravity, hogging under uplift. Both plates are sloped-member plates (skewed flange welds). The extension above the top flange may clash with purlins and the ridge cap: check it |
| **Canopy to column** (H400 × 200 × 6 × 10 to the tapered column flange 250 × 14) | horizontal cantilever on a column partway up the taper | **4E**, extended at least at the top (hogging); symmetric if wind uplift reverses it | Column-side checks (Steps 14–20) on a **14 mm flange and 8 mm web**. Expect continuity plates. The column flange is sloped on the outer face at the canopy level: use a tapered packing or shop-set plate angle, and show the angle |

**Order-of-magnitude check (illustrative only; no design values).** F10T bolts, Fnt 750 MPa, φ = 0.75;
pf = 50 mm at the knee and 45 mm at the splice; SM520 plate Fy = 345 MPa (16 < t ≤ 40 mm).

- **Knee, 4E:**
  - h0 + h1 ≈ (800 + 50 − 6) + (800 − 12 − 50 − 6) = 1576 mm;
  - φMnp ≈ 800 kN·m for M24 (Pt 339 kN); 1015 for M27; 1250 for M30.
  - Plate with bp = 270, g = 140: s = 97 mm, Yp ≈ 6740 mm, so tp,req ≈ 21 mm with M24 (→ 22–25 mm).
  - **Column flange 14 mm fails the thick-flange rule even with continuity plates.** With M24, Yc,unstiff ≈ 5590 mm
    → tfc,req ≈ 22 mm; Yc,stiff ≈ 9280 mm → ≈ 17 mm.
  - Expect to need: a **locally thicker column flange** over the knee (e.g. 20–25 mm, spliced in the welded
    column), or smaller bolts matched to the real demand, or the DG16 thin-flange (prying) design.
  - **This is the main finding for the knee.**
- **Splice and ridge, 350 deep, 4E:**
  - h0 + h1 ≈ 680 mm;
  - φMnp ≈ 240 kN·m (M20) or 345 kN·m (M24);
  - prismatic 350 × 200 × 6 × 10 SM520: Mp ≈ 299 kN·m; its flange b/t = 10 is noncompact for 355 MPa;
  - plate bp 220, g 120: tp,req ≈ 18 mm with M20 (→ 20 mm).

##### 7.3 Calc steps to implement in Python (one function per step, SI units, DG4 equation numbers in docstrings)

1. **Inputs** from the MIDAS results: Mu, Vu, Nu at the plate for every wind and gravity combination, both
   signs. The geometry comes from the member catalogue; never retype it.
   - Resolve N, V into components normal and parallel to the plate (sloped members).
   - M* = |Mu| + max(0, Nu,normal)·(d − tf)/2, with the sign convention stated.
2. **Geometry builder** for 4E / 4ES / 8ES:
   - d measured along the plate; h0, h1 (or h1–h4); s;
   - the pfi = s cap; the de ≤ s case switch;
   - assert the Table 3.7 ranges, and **print a `!!` warning when outside**.
3. `pt(db, Fnt)`, `mnp(layout)`, `db_req(M*)`: Eq. 3.5–3.9.
4. `yp(layout)`: Tables 3.1–3.3. `tp_req = sqrt(1.11*phi*Mnp/(phib*Fyp*Yp))`, with Fyp by plate thickness (SM520:
   355 for t ≤ 16, 345 for t ≤ 40, 335 for t ≤ 75).
5. `ffu = M*/(d − tf)`. For 4E: shear yield and rupture of the extension (Eq. 3.12–3.14). Report both the DG4 φ
   and the 360-16 φ (yield φ = 1.0).
6. Stiffener (4ES/8ES): ts, hst/ts, Lst = hst/tan 30°, landings 25 mm (Eq. 3.15–3.16, 2.11).
7. Bolt shear on the compression-side bolts (Eq. 3.17), using the plate-parallel shear plus the axial component.
   Bearing and tearout of the plate and the column flange (Eq. 3.18–3.19, 360-16 J3.10).
8. **Welds:**
   - flange fillets for max(Ffu, 0.6FyAfb) with the 1.5 directional factor, or CJP when tf > 10 mm (decision §7.5);
   - web: develop φFy·tw near the tension bolts (w ≥ 0.943 Fy tw / FEXX for two fillets), and carry Vu over the
     shear length;
   - skewed-joint adjustments for sloped flanges.
9. **Column side:**
   - `yc(layout, stiffened)` (Tables 3.4–3.5); tfc,req (Eq. 3.20); φRn from the flange (Eq. 3.21–3.22);
   - web yielding (Eq. 3.24) with Ct and kc = tfc + weld leg; web buckling (Eq. 3.26/3.27); web crippling
     (Eq. 3.29–3.31) with the column-end forms at the knee;
   - Fsu (Eq. 3.32) → continuity plates to AISC 360-16 J10.8 / DG13;
   - **panel zone** to 360-16 J10.6, checking the 800 × 8 web for shear buckling (h/tw ≈ 96 > 2.24√(E/Fy)),
     with a diagonal stiffener or doubler if needed.
10. **Thick-plate checks** (Eq. 3.33–3.36): Mpl ≥ 1.1·Mnp and Mcf ≥ 1.1·Mnp; else stop with a `!!` (out of DG4
    scope).
11. **Unit tests:** reproduce 4E Example B (Yp 148.2 in, tp,req 0.85 in, Yc 170.1 in, tfc,req 0.790 in, φMnp
    4301 k-in) and the 8ES example (Yp 277.6 in, Yc,stiff 377.7 in) to 3 significant figures.
12. **Output:** one dict per joint (plate t × b × L, bolt size, grade, count and pretension, g, pf, pb, de,
    stiffener, continuity plates, welds). Drawings read this dict; they never retype the numbers.

##### 7.4 What an end-plate connection detail must show (from the DG4 final-detail sheets, pp.42, 47, 49, 54, and §2.4)

- **Two views:**
  - an **elevation** on the member axis, showing the plate in edge view, the bolt rows, the stiffeners and the
    column continuity plates;
  - a **view on the plate face**, or a section showing the gauge and the plate width.
  - For a sloped rafter, the **angle** of the rafter to the plate (90° ± 18°) and of the haunch flange.
- **Plate:** thickness × width × length, grade (SM520B or C), and plate mark.
  - Length = de + pfo + (vertical depth along the plate) + pfo + de for a symmetric 4E.
  - Note any through-thickness requirement or UT, because of the lamellar-tearing risk in the plate at the
    tension-flange weld.
  - Note any flatness requirement after welding (warping).
- **Bolt pattern dimensions**, all chained to the flange faces:
  - g; pfo and pfi at both flanges; pb (8ES); de; c on the column side;
  - **the vertical depth** used in the calc;
  - hole diameter (standard holes: M20 → 22, M24 → 27 mm per 360-16 Table J3.3M; check the JIS equivalents).
- **Bolt callout:** number, diameter, grade (e.g. "8-M24 F10T"), washer and nut, **"PRETENSIONED"**, and the
  method of tightening (TC / torque / turn-of-nut). Not slip-critical, so the faying surface can be painted.
  Mark the condition of the threads in the shear plane if Fnv,X is relied on.
- **Stiffeners (4ES/8ES):**
  - thickness, height hst and length Lst;
  - the **30°** chamfer;
  - **25 mm landings** at both ends;
  - the corner clip;
  - the welds (fillet if ≤ 10 mm, else CJP).
- **Column side:** continuity plates in line with each rafter flange (thickness, size, clips, welds), the cap plate
  at the knee, any doubler or diagonal stiffener, and any locally thickened column flange with its CJP splice
  location.
- **Welds**, as AWS symbols:
  - flange-to-plate CJP (bevel, root on the web side, 8 mm backing fillet, back-gouge) **or** the double fillet
    size;
  - web-to-plate fillets both sides (size);
  - "NO WELD ACCESS HOLES";
  - weld sequence: web first.
- **Notes:**
  - fabricate the member short (5–10 mm), with finger shims supplied;
  - **no camber on members with end plates**;
  - a reference to the connection calc and its design forces (M*, V, N) for each joint;
  - steel grades;
  - the electrode classification (E70XX / E49XX).
- Bolt-to-weld and wrench clearances (TC bolt tools need a larger pf) are checked at the drawing stage.

##### 7.5 Open questions for the engineer

1. **Design basis for the plates.**
   - DG4 sizes the plate and column flange to 1.11 × the **bolt** moment (thick plate).
   - DG16 is the AISC/MBMA guide meant for wind-governed metal-building frames: it allows designing for the demand,
     snug bolts and thin plates with prying.
   - Which governs? Recommend: DG4 thick-plate for the knee, and to review DG16 before the calc is written (it is
     on the drive).
2. **Seismic category.**
   - If the site needs seismic design (DPT 1302), is the frame an OMF/IMF? Then 358-22 Table 6.1 applies, and the
     knee d = 800 exceeds the 4E/4ES limit of 600.
   - Ry and Cpr would also be needed for SM520 (not in AISC 341).
3. **Knee column flange (14 mm)** fails the thick-flange check even when stiffened, for M24. Options:
   - thicken the column flange locally;
   - extend the column above the outer bolts;
   - a cap plate plus continuity plates;
   - a rafter-over-column (horizontal end plate) detail instead.
4. **Knee arrangement:** rafter end plate on the column face (vertical plate), or column cap plate under a
   continuous rafter (horizontal plate)? This sets which member's flange is checked as the "column" and how the
   18° slope is handled.
5. **Bolt grade and finish:** F10T (black, painted) or galvanized F8T / 10.9 HDG? This affects Fnt, pretension
   and whether bolts must be renewed if reused.
6. **Flange weld:** CJP with backing fillet and back-gouge (DG4 seismic procedure; required for tf > 10 mm), or
   double fillets sized for max(Ffu, 0.6FyAfb) as in the wind example? The rafter tf is 12 mm and the prismatic
   10 mm.
7. **Axial force in the bolts:** confirm adding the normal tension component (frame thrust under uplift) to the
   bolt demand as in §5. DG4 is silent.
8. **Splice location:** keep the haunch-to-prismatic splice at 5.2 m (flange widths 250 / 200 change there), or
   move it to the dead-load inflection point, where a flush plate would do?
9. **Panel zone** of the 800 × 8 column web at the knee: diagonal stiffener or doubler acceptable to the fabricator?
10. **Tolerance:** use finger shims at the knee, or rely on drilled-to-template column flanges? Fix the short-length
    allowance (DG4 gives two different ranges: 5–10 mm or 6–10 mm).

---

# Part G. AISC Design Guide 16 - Flush and Extended Multiple-Row Moment End-Plate Connections


Working extract and review for the MIDAS GEN NX portal-frame job (26 m gable frames at 10 m, SM520, tapered
welded columns and haunched rafters, wind-governed, Thailand). DG16 is the end-plate guide written with and for
the metal-building industry (MBMA co-sponsor). It is the source of the knee, rafter-splice and ridge end-plate
procedures that metal-building manufacturers use. Reviewed 2026-10-04.

**Page convention.** "p.NN" means the **PDF page** of
`Design Guide 16 - Flush and Extended Multiple-Row Moment Connections.pdf` (72 pp.), under
`G:\My Drive\##Textbook\AISC Design Guide\AISC - Steel Design Guides 2016\...`. **Book page = PDF page − 7**
(for example, p.8 = book p.1, p.46 = book p.39). PDF pp.1–7 are the cover, copyright, acknowledgments and contents.

**Read method.** Text pulled with PyMuPDF for all 72 pages. Every page with equations or tables was viewed as an
image (110 dpi; the rotated summary tables 4-3 to 4-6 at 170 dpi, de-rotated). PyMuPDF does not extract the
equations, so every equation below was read from the images. All the Y expressions, Qmax values and φMq values
of the ten worked examples were recomputed in Python from the equations as restated here, and they match the
book (§5).

**Basis warning.** DG16 (Murray and Shoemaker, 2002; second printing October 2003 with "Rev. 3/1/03" errata
bars on pp.18, 48 and 55) is written against **AISC LRFD 1999 / ASD 1989** and RCSC 2000. Here is what changed
for AISC 360-16 (checked in `G:\My Drive\##Textbook\a360-16-spec-and-commentary.pdf`, PDF pp.185–193):
- **Bolt nominal tensile stress is unchanged.** DG16 uses Ft = 90 ksi for A325 and 113 ksi for A490 (LRFD 1999
  Table J3.2). AISC 360-16 Table J3.2 gives Fnt = 90 ksi (620 MPa) for Group A and 113 ksi (780 MPa) for Group B.
  The A325 and A490 grades are now ASTM F3125 grades.
- **φ factors are unchanged.** Bolt rupture φ = 0.75 (360-16 J3.6). Plate flexural yield φb = 0.90. Shear
  φv = 0.90.
- **Pretension table: the large sizes moved.** DG16 Table 2-1 (p.19) gives A325 1⅛ – 1½ in. as 56/71/85/103 kips.
  These are old values from when A325 above 1 in. had a lower Fu. 360-16 Table J3.1 gives **64/81/97/118 kips**,
  and Table J3.1M gives metric values (Group A / Group B, kN): **M16 91/114, M20 142/179, M22 176/221,
  M24 205/257, M27 267/334, M30 326/408, M36 475/595**. Sizes up to 1 in. are unchanged
  (12/19/28/39/51 kips A325).
- **Snug-tight bolts in tension.** 360-16 J3.1(a)(2) still allows snug-tight bolts in tension for **Group A only**,
  where "loosening or fatigue due to vibration or load fluctuations are not design considerations". This is the
  same rule DG16 relied on (p.12 item 1, p.19).
- **The panel-zone shear rules of DG16 Ch.5** cite LRFD 1999 Appendix G3 (tension field). In 360-16 they map to
  **G2.1 / G2.2**: kv = 5 + 5/(a/h)², the Cv2 limits 1.10√(kvE/Fy) and 1.37√(kvE/Fy), and the tension-field
  equation G2-7, which carries extra flange-proportion conditions in 360-16. Re-derive from 360-16 before use.
- **Relation to DG4 2nd ed.** *Extended End-Plate Moment Connections - Seismic and Wind Applications*
  (Murray and Sumner, 2003) is also on the drive. It came out in the same year and from the same research group.
  - It uses the **same yield-line Y and modified-Kennedy prying model** for the 4E, 4ES and 8ES connections.
  - It adds what DG16 leaves out: **column-side checks** (column flange yield line, web yielding, buckling,
    crippling, continuity plates), **end-plate stiffener geometry** (30° "Whitmore" spread,
    Lst = hst / tan30°, about 25 mm landings, ts ≥ tbw·Fyb/Fys; DG4 p.23 = book 16), and a seismic procedure that
    later became AISC 358.
  - **Notation trap.** DG4 2nd ed. writes hᵢ for the distance from the **compression-flange centreline** to a bolt
    row. That is DG16's **dᵢ**. DG16's hᵢ is measured from the **compression-side face**.
  - AISC has since issued a combined end-plate guide (DG39, which supersedes DG4/DG16 for current specifications;
    **not on the drive, so verify the edition before citing**). The physics and the yield-line patterns below do
    not change.

**Copyright.** Everything below is paraphrased. Equations are restated in my own layout and notation, and tables
are restated only where their numbers are needed. No passage is copied.

**Notation** (DG16 Appendix A, pp.68–69, condensed). **Lengths in DG16 are inches; see §2.9 for SI.**
- bp, tp, Fpy: end-plate width, thickness and yield stress. bf, tf: beam (rafter) flange width and thickness.
  tw: beam web. h: total beam depth.
- g: bolt gage, measured horizontally between the two bolt columns.
- pf: distance from a bolt row to the **near face** of the tension flange. pf,i is for the first row inside
  the flange, pf,o for the row outside it.
- pb: pitch between bolt rows.
- pext: plate extension beyond the outer face of the tension flange. de = pext − pf,o is the plate edge
  distance beyond the outer bolt row.
- ps: stiffener-to-bolt distance (four-bolt flush with the stiffener inside the rows). ps,i / ps,o: inner and outer
  stiffener-to-bolt distances when the stiffener is between the rows. ts: stiffener thickness.
- s = ½√(bp·g): distance from the innermost bolt row to the innermost yield line.
- **h0, h1, h2, h3**: distance from the **compression-side face** of the beam to the outer row, the first inner
  row, the second inner row and the third inner row (yield-line work arms).
- **d0, d1, d2, d3**: the same distances measured to the **centre of the compression flange** (bolt lever arms).
  A row that does not exist takes d = 0.
- db: bolt diameter. Pt = Ab·Ft = π·db²·Ft / 4 (bolt "proof" or tensile strength). Tb: pretension
  (snug-tight reduced; §2.6).
- w′ = bp/2 − (db + 1/16 in.): plate width per bolt less the hole.
- aᵢ, aₒ: distance from the bolt line to the prying force (inner and outer bolts). F′ᵢ, F′ₒ: flange force per bolt
  at the thin-plate limit. Qmax,i, Qmax,o: maximum prying force per bolt.
- Y: yield-line mechanism parameter. Mpl = Fpy·tp²·Y (plate yield). Mnp: bolt rupture without prying.
  Mq: bolt rupture with prying.
- γr: rotation factor, 1.25 for flush and 1.00 for extended connections. Mu: required moment (for ASD,
  Mu = 1.5·Mw).
- Configuration names used below: **2F** two-bolt flush, **4F** four-bolt flush, **4FS-b** four-bolt flush with the
  stiffener between the rows, **4FS-i** four-bolt flush with the stiffener inside the rows, **4E** four-bolt
  extended, **4ES** four-bolt extended stiffened, **1/2** and **1/3** multiple-row extended (one row outside, two
  or three inside), **1/3S** stiffened 1/3.


---


#### 1. Scope, configurations and design philosophy (Ch.1 – 2, pp.8–20)

**1.1 Where end-plates are used (pp.8–10, Figs 1-1, 1-2).**
- Low-rise metal buildings pioneered the moment end-plate in the US. It is used at the **rafter-to-column knee**
  and at **rafter-to-rafter splices** (beam-to-beam) in gable frames.
- The examples use built-up (welded plate) shapes. The procedures also apply to hot-rolled shapes inside the tested
  ranges (Tables 3-6 and 4-7).
- The connection is one of the three AISC FR (Type 1) moment connections. FR behaviour is the frame-analysis
  assumption.
- The tension side depends on the moment sign. Under **reversal**, one connection may combine a flush side at
  one flange with an extended side at the other (p.9).
- **Flush plates** (all bolts between the flanges) suit light lateral load or locations **near the inflection
  points** of gable frames. They are also used at the knee when an extension would clash with other members or the
  **roof deck** (p.9).
- **Extended plates** (bolts outside the tension flange) are the normal beam-to-column moment connection.

**1.2 The nine configurations in scope (Figs 1-3, 1-4, pp.9–10).**
- Flush: (a) **2F**; (b) **4F**; (c) **4FS-b**, with web gusset plates on both sides of the web between the two
  tension rows; (d) **4FS-i**, with the stiffener on the inner side of the two rows. In both stiffened types the
  stiffener is welded to the plate and to the beam web.
- Extended: (a) **4E**, which DG16 calls probably the most commonly used configuration; (b) **4ES**, with a
  plate-to-flange stiffener on the extension; (c) **1/2** unstiffened; (d) **1/3** unstiffened; (e) **1/3S**
  stiffened. "1/n" means one row outside the flange and n rows inside.
- Ch.5 adds the **knee-area (panel zone) design** for gable frames.

**1.3 Research basis (pp.10–13).**
- The guide grew out of the split-tee model. Early designs gave thick plates and large bolts.
- Kennedy et al. (1981) defined three plate stages:
  - **thick**: no plastic hinges and no prying;
  - **intermediate**: hinges form at the web or flange toe and prying grows;
  - **thin**: a second set of hinges forms at the bolt line and prying is at its maximum.
- The Oklahoma / Virginia Tech series (Srouji, Hendrick, Morrison, Abel, Borgsmiller, Sumner, 1983–2001) verified
  the **yield-line plate strength** and **modified-Kennedy bolt forces** with full-scale tests of each of the nine
  types.
- Morrison found that the **outer bolts of 4ES and 1/3 do not pry** and carry most of the flange force. For 4E,
  the outer and inner rows share the force about equally (Abel and Murray).
- 1/2 and 1/3S were proprietary MBMA-member tests, included with permission. The guide says to prefer it over
  the earlier reports because it carries updated mechanisms and the LRFD factors (p.12).
- **Snug-tight bolts (p.12).** Under a 50-year US wind-load history (about 8000 cycles; one specimen 80,000),
  snug-tightened A325 end-plates showed no bolt, plate or weld failure, though bolt force fell with cycling.
  Strength is predicted well **if prying is included**.
  - The measured snug pretension scales with diameter. Recommended Tb as a share of the full pretension:
    **≤ ⅝ in. 75 %, ¾ in. 50 %, ⅞ in. 37.5 %, ≥ 1 in. 25 %**.
- **Seismic (p.13).**
  - In 4E tests, specimens without weld access holes gave robust hysteresis. Specimens **with weld access holes
    fractured at the hole** early in the inelastic range, so **do not use weld access holes** in end-plate
    connections.
  - The SAC work led to the FEMA-350 procedure, which became AISC 358.
  - Snug-tight bolts are not recommended for high seismicity.

**1.4 The three design criteria (§2.1 – 2.4, pp.14–16).**
1. **Strength: plate thickness by yield-line theory.** This is the virtual-work method. Of the candidate patterns,
   the governing mechanism is the one giving the **least** upper-bound load (p.14).
2. **Bolt force including prying** by the modified Kennedy method (split-tee analogy, Figs 2-1, 2-2).
3. **Stiffness**, judged by moment-rotation against the FR limit. An FR connection is classically one that
   carries at least 90 % of the fixed-end moment while rotating at most 10 % of the simple-span end rotation θs.
   - With θs = Fy·L / (E·h) at a yield-level end moment and L/h = 24, θs ≈ 3.8×10⁻⁵·Fy rad (Fy in ksi).
   - Against this limit, **flush plates qualify as FR up to 80 % of their capacity** and **extended plates up to
     100 %** (p.16).
   - This is the origin of **γr = 1.25 (= 1/0.8) for flush plates**. Not valid for seismic loads.

**1.5 Thick-plate versus thin-plate behaviour (§2.5, pp.16–17).**
- Borgsmiller and Murray (1995), from 52 tests: prying starts when the applied moment reaches about **90 % of the
  plate strength Mpl**.
- Below 0.9·Mpl the plate is "thick", there is no prying, and the bolts take direct tension. Above it the plate is
  treated as fully "thin", and the bolts take Pt − Qmax.
- The intermediate stage is therefore dropped and only Qmax is needed. This is the **simplified modified-Kennedy**
  method used throughout.
- Two design routes follow:
  - **Procedure 1: thick plate with smaller bolts.** Bolt rupture without prying governs. The plate is made strong
    enough (≥ 1.11 × the bolt moment) that it stays thick.
  - **Procedure 2: thin plate with larger bolts.** Plate yield governs, or bolt rupture with prying. Choose the
    bolt so that φMq ≥ Mu with the maximum prying.
  - **ASD:** set Mu = 1.5·Mw. The procedures are then identical for ASD and LRFD.

**1.6 Limit-state checklist (§2.6, p.20).**
- End-plate flexural yield (not limiting in itself, but bolt forces and rotation then rise quickly).
- End-plate shear yield (rare; reduces flexural strength in combination).
- End-plate shear rupture through the outer holes.
- **Bolt rupture from direct load plus prying.** This is brittle and the most critical limit state.
- Bolt shear or slip at the interface.
- Bearing at the plate and the column flange.
- Rupture of the flange-to-plate weld or the web-to-plate weld in the tension region.
- Shear yield of the web-to-plate weld or the web base metal.
- Column web yielding (tension or compression side), crippling and buckling.
- Column flange yielding at the tension bolts.
- Column stiffener failure.
- Panel-zone shear yield or buckling.
- Excessive rotation.


#### 2. Design procedure step by step (§2.5, Tables 3-1 – 3-5, 4-1 – 4-6, App. B; pp.16–22, 24–28, 38–45, 70–72)

**2.1 Required moment and γr (pp.17, 21).**
- Mu is the factored moment at the plate (for ASD, 1.5·Mw).
- γr = 1.25 for flush and 1.00 for extended. γr multiplies Mu **only in the plate-thickness design**.
- **Axial force (p.20 item 11; Ex 4.2.3):** there are no tests with axial load. Use an effective
  Mu,eff = Mu ± P·(h − tf)/2: plus for tension, minus for compression.

**2.2 Procedure 1: thick plate, smaller bolts (Eqs 2-4 – 2-8, p.17).**
1. Required bolt diameter without prying: **db,req = √[ 2·Mu / (π·φ·Ft·Σdn) ]**, with φ = 0.75 and Σdn the sum of
   all tension-row lever arms. Pick a standard db ≥ db,req.
2. Bolt-rupture moment without prying: **φMnp = φ·2·Pt·Σdn**, with Pt = π·db²·Ft / 4.
3. Required plate: **tp,req = √[ 1.11·γr·φMnp / (φb·Fpy·Y) ]**, with φb = 0.90. Pick a standard tp ≥ tp,req.
   - This comes from setting φMnp = 0.90·φb·Mpl. The 1.11 is 1/0.90, written in the numerator to keep it
     separate from φb.
4. There is no separate prying check, because the plate is thick by construction.

**2.3 Procedure 2: thin plate, larger bolts (Eqs 2-9 – 2-19, pp.18–19).**
1. Plate: **tp,req = √[ γr·Mu / (φb·Fpy·Y) ]**, from γr·Mu = φb·Fpy·tp²·Y.
2. Choose a trial db and compute the maximum prying force per bolt:
   - w′ = bp/2 − (db + 1/16 in.)
   - **aᵢ = 3.682·(tp/db)³ − 0.085** (in inches; the 3.682 coefficient is the 3/1/03 revision)
   - **F′ᵢ = [ tp²·Fpy·(0.85·bp/2 + 0.80·w′) + π·db³·Ft/8 ] / (4·pf,i)**
     (the last term is the bolt-shank bending contribution Mb; for flush plates pf,i = pf)
   - **Qmax,i = (w′·tp² / (4·aᵢ)) · √[ Fpy² − 3·(F′ᵢ / (w′·tp))² ]**
   - Extended plates, outer bolts: **aₒ = min{ 3.682·(tp/db)³ − 0.085 ; pext − pf,o }**.
     F′ₒ uses the same expression with pf,o, or equivalently F′ₒ = F′ᵢ·(pf,i / pf,o). Qmax,o uses aₒ and F′ₒ.
   - **If either radical is negative, combined plate flexure and shear yield governs.** The plate is inadequate,
     so make it thicker (p.18; also Tables 3-1, 4-1).
3. Bolt rupture with prying, **φMq = φ × the largest** of the candidate force combinations (φ = 0.75):
   - **Flush** (2F, 4F, 4FS): max{ 2(Pt − Qmax)(d1 + d2) ; 2·Tb·(d1 + d2) }. For 2F, d2 = 0.
   - **Extended**, general form (1/3 shown; set absent rows to d = 0). Each line is a different assumption
     about which rows have reached Pt − Q and which are still at Tb:
     - 2(Pt − Qo)·d0 + 2(Pt − Qi)·(d1 + d3) + 2·Tb·d2
     - 2(Pt − Qo)·d0 + 2·Tb·(d1 + d2 + d3)
     - 2(Pt − Qi)·(d1 + d3) + 2·Tb·(d0 + d2)
     - 2·Tb·(d0 + d1 + d2 + d3)
   - **Which rows pry** (bolt-force models, Tables 4-2 – 4-6):
     - 4E and 4ES: outer row Pt − Qo, inner row Pt − Qi.
     - **1/2**: row 0 is Pt − Qo, row 1 is Pt − Qi, and **row 2 (the second inner row) carries only Tb**.
     - **1/3 and 1/3S**: row 0 Pt − Qo, rows 1 and 3 Pt − Qi, **row 2 (the middle inner row) only Tb**.
4. Check φMq ≥ Mu. If it fails, increase db.

**2.4 Analysis (given tp and db, find φMn), App. B pp.70–72.**
- Mpl = Fpy·tp²·Y, and Mnp = 2·Pt·Σdn.
- **If Mnp < 0.90·Mpl**, the plate is thick: φMn = min{ φ·Mnp ; φb·Mpl/γr }.
- **Otherwise** the plate is thin: compute Mq. If Mpl/γr < Mq, plate yield governs and φMn = φb·Mpl/γr. If not,
  φMn = φ·Mq.
- Note the small inconsistency: the App. B thick/thin test (Mnp < 0.9·Mpl) omits γr, whereas the Procedure 1
  sizing equation includes it. **Use the App. B logic as the capacity check in code.**

**2.5 Yield-line parameter Y, flush plates** (Tables 3-2 – 3-5, pp.25–28). In all of them s = ½√(bp·g), and
**pf is replaced by s where pf > s**.
- **2F (Table 3-2):** Y = (bp/2)·h1·(1/pf + 1/s) + (2/g)·h1·(pf + s).
- **4F (Table 3-3):** Y = (bp/2)·[ h1/pf + h2/s ] + (2/g)·[ h1·(pf + 0.75·pb) + h2·(s + 0.25·pb) ] + g/2.
- **4FS-b (Table 3-4):** Y = (bp/2)·[ h1·(1/pf + 1/ps,o) + h2·(1/s + 1/ps,i) ]
  + (2/g)·[ h1·(pf + ps,o) + h2·(s + ps,i) ].
- **4FS-i (Table 3-5):** same form as 4F, but with the **upper bound s ≤ ps**.

**2.6 Bolt pretension Tb (Tables 3-1 / 4-1, pp.19, 24, 38).**
- Fully tightened bolts: Tb is the specified minimum pretension (0.70·Fu·As; see the basis warning for the
  360-16 values).
- Snug-tight A325 (Group A only): Tb = 75 % / 50 % / 37.5 % / 25 % of the full pretension for db ≤ ⅝, ¾, ⅞,
  ≥ 1 in. (≈ M16 / M20 / M22 / M24+).
- In the examples, "fully tightened" Tb is taken as the Table J3.1 value (≈ 0.7·Pt).

**2.7 Yield-line parameter Y, extended plates** (Tables 4-2 – 4-6, pp.39–45). In all of them s = ½√(bp·g), and
pf,i is replaced by s where pf,i > s.
- **4E (Table 4-2):** Y = (bp/2)·[ h1·(1/pf,i + 1/s) + h0·(1/pf,o) − ½ ] + (2/g)·h1·(pf,i + s).
- **4ES (Table 4-3)**, with de = pext − pf,o:
  - Case 1, s < de: Y = (bp/2)·[ h1·(1/pf,i + 1/s) + h0·(1/s + 1/pf,o) ]
    + (2/g)·[ h1·(pf,i + s) + h0·(s + pf,o) ]
  - Case 2, s ≥ de: Y = (bp/2)·[ h1·(1/pf,i + 1/s) + h0·(1/pf,o + 1/(2s)) ]
    + (2/g)·[ h1·(pf,i + s) + h0·(de + pf,o) ]
  - The table heading misprints φy for φb.
- **1/2 (Table 4-4):** Y = (bp/2)·[ h1/pf,i + h2/s + h0/pf,o − ½ ]
  + (2/g)·[ h1·(pf,i + 0.75·pb) + h2·(s + 0.25·pb) ] + g/2.
- **1/3 (Table 4-5):** Y = (bp/2)·[ h1/pf,i + h3/s + h0/pf,o − ½ ]
  + (2/g)·[ h1·(pf,i + 1.5·pb) + h3·(s + 0.5·pb) ] + g/2.
- **1/3S (Table 4-6)**:
  - Case 1, s < de: Y = (bp/2)·[ h1/pf,i + h3/s + h0·(1/s + 1/pf,o) ]
    + (2/g)·[ h1·(pf,i + 1.5·pb) + h3·(s + 0.5·pb) + h0·(s + pf,o) ] + g/2
  - Case 2, s ≥ de: replace h0·(1/s + 1/pf,o) with h0·(1/pf,o + 1/(2s)), and h0·(s + pf,o) with h0·(de + pf,o).

**2.8 Remarks for coding.**
- Each table gives one governing mechanism (the guide already chose the least upper bound). There is **no**
  pattern search to do.
- The 1/2 and 1/3 equations assume **equal pitch pb** between the inner rows.
- The 4E "− ½" term is inside the bp/2 bracket, so it contributes −bp/4.
- The flowchart (Fig 2-4, pp.21–22) and App. B restate the same equations, and they are the cleanest source to
  code from.

**2.9 SI use.**
- The equations are homogeneous (force = stress × length²) **except two constants**:
  - **aᵢ is in inches**: in SI, aᵢ [mm] = 25.4·[3.682·(tp/db)³ − 0.085].
  - **w′ uses a 1/16 in. hole allowance**: in SI, w′ = bp/2 − (db + 1.6 mm). Better, use the actual
    hole-minus-bolt clearance: +2 mm for M ≤ 24 and +3 mm above, as in 360-16 Table J3.3M. Record the choice.
- Guard the code:
  - require aᵢ > 0 (aᵢ turns negative when tp/db < 0.285);
  - require the Qmax radicands > 0;
  - flag every input outside Tables 3-6 / 4-7 (§3.1).

**2.10 Column side.** DG16 deliberately **excludes column-side design** (p.20 items 13–14): column web stiffeners,
continuity plates and doublers. It points to DG4 (1st ed.) and DG13. Use **DG4 2nd ed. Ch.3 – 4** (column flange
yield line Yc, web local yielding, buckling, crippling, stiffeners) or AISC 360-16 **J10**. For a gable knee, the
**panel zone** is designed by DG16 **Ch.5** (§4.2 below).


#### 3. Geometric limits, detailing and practice (§2.5.3 pp.19–20, §3.1.2 p.24, §4.1.2 p.38, Tables 3-6 / 4-7 pp.29, 46)

**3.1 Tested parameter ranges.** The equations are validated only inside these ranges. Outside them the mechanism
may change (pp.24, 38).

| Parameter | Flush (Table 3-6) in. | ≈ mm | Extended (Table 4-7) in. | ≈ mm |
|---|---|---|---|---|
| pf (pf,i) | 1 5/16 – 1 7/8 | 33 – 48 | 1 – 2½ ᵃ | 25 – 64 |
| pb | 1 7/8 – 3 | 48 – 76 | (examples use 2½) | (64) |
| pext | – | – | 2½ – 5 1/8 | 64 – 130 |
| g | 2¼ – 3¾ | 57 – 95 | 2¾ – 7 | 70 – 178 |
| h | 16 – 24 (2F: from 8) | 406 – 610 (2F: 203) | 15¾ – 24 (multi-row to 62) ᵇ | 400 – 610 (to 1575) |
| bp | 5 – 6 | 127 – 152 | 6 – 10¼ | 152 – 260 |
| tf | 3/16 – 3/8 | 4.8 – 9.5 | 3/8 – 1 | 9.5 – 25.4 |

ᵃ An inner pitch pf,i of 5 in. (127 mm) was also verified for the 1/2 connection (Sumner and Murray 2001).
ᵇ The 62 in. upper limit applies to the multiple-row extended connections.

**3.2 Rules and assumptions** (§2.5.3, pp.19–20; restated):
- **Snug-tight bolts only for static loading.** Wind, snow and temperature count as static. Not for crane
  runways, machinery supports or heavy fatigue. A490 bolts must be fully tightened.
- γr: 1.25 for flush plates assumed FR, 1.00 for extended (§1.4).
- **Keep pf as small as possible**; it is the most economical choice. Absolute minimum pitch from the flange face:
  **db + ½ in. (≈ db + 13 mm) for db ≤ 1 in.**, and **db + ¾ in. (≈ db + 19 mm) above 1 in.** Tension-control
  bolts need more (wrench clearance). The flange-to-plate weld also needs room.
- **Shear at the interface.**
  - Bearing type (snug-tight or pretensioned): it is common to assume the **compression-side bolts carry all
    the shear**.
  - Slip-critical, only needed for non-static loads: all bolts share the shear, and no tension interaction is
    needed. The moment's bolt tension is offset by the compression on the other side (RCSC commentary).
- **Effective plate width ≤ bf + 1 in. (≈ bf + 25 mm)** in calculations.
- **Gage g ≤ the tension-flange width.**
- **Flange-to-plate weld.**
  - Normally develops the flange **yield** strength, by CJP or by fillets for thin flanges.
  - If Mu is less than the beam's design flexural strength, the weld may be designed for Mu, but **not less than
    60 % of the flange's specified yield** strength.
- **Web-to-plate weld near the tension bolts.** Develops web yield. If full strength is not needed, at least 60 %
  of web yield.
- **Web shear at the plate.** Count only the web between mid-depth and the inside of the compression flange, or
  between (the inner tension row + 2·db) and the compression flange, whichever is smaller. This is the authors'
  judgement.
- **Stitch bolts** between the tension and compression groups, used in deep connections to limit plate separation
  from weld distortion: **neglect them in strength**.
- **Web and web-stiffener design is not covered.** The tests used thick webs, but strain gauges showed web
  yielding near the tension bolts. Engineering judgement is needed. **This matters for our 6 mm and 8 mm webs**
  (§6.4).
- **Column stiffening is not covered** (DG4, DG13).

**3.3 Stiffeners** (from DG16's figures and examples; DG16 gives no sizing rule):
- 4FS-b and 4FS-i: web gusset plates on **both sides of the web**, welded to the plate and the web (p.9).
- 4ES and 1/3S: the extension stiffener sits on the web centreline, between the outer bolts (Figs 1-4b and e,
  Table 4-3 sketch).
- Sizing and geometry come from **DG4 2nd ed. p.23** (book 16):
  - **ts ≥ tw,beam × (Fy,beam / Fy,stiffener)**;
  - length along the flange **Lst = hst / tan 30°**, where hst is the extension height from the outer flange face
    to the plate end;
  - **about 25 mm (1 in.) landings** at the flange and at the plate end;
  - a corner clip clear of the flange weld.
- Effect in the examples: a stiffener **saves ⅛ in. of plate** with the same bolt size (Ex 4.2.1 vs 4.2.2 and
  Ex 4.2.4 vs 4.2.5).

**3.4 Bolt tightening and quality.** DG16 accepts snug-tight A325 for static (wind) loading **only because prying
is included in the bolt check** (p.12). With fully tensioned bolts, Tb is larger, and the Tb rows of φMq rise. The
tests also show that **bolt pretension decays under cyclic wind loading** without failure (p.12).


#### 4. Gable-frame specifics: knee, splices, slope (Ch.1 figs, Ch.5 pp.58–63)

**4.1 What DG16 shows.**
- Fig 1-1 / 1-2 (p.8) shows end-plates at the beam-to-column knee and at beam-to-beam splices.
- The Ch.5 knee figures (Fig 5-2, p.58) show a **vertical rafter end-plate bolted to the inside face of the
  column flange**:
  - the column runs up to the roof line, and its top forms the panel zone;
  - the rafter's sloping top flange continues as the column cap;
  - the **rafter end-plate acts as the full-depth rafter web stiffener**, on the third side of the panel;
  - a **column web stiffener** aligned with the rafter's inside flange closes the fourth side. It is either full
    depth (welded to both column flanges) or partial depth (welded to the inside column flange only, stopping
    within 1 in. (25 mm) of the outside flange).
- **DG16 does not treat:**
  - the horizontal-plate knee, where the column end-plate sits under the rafter;
  - the plumb-cut ridge plate on a sloping rafter;
  - tapered members at the plate.
- So the plate geometry on a sloping rafter is an **engineering judgement** (§6.2). Every example and every test
  in the guide is a prismatic beam with the plate perpendicular to the beam axis.

**4.2 Panel-zone design (Ch.5, pp.58–63).**
- The panel-zone plate is the knee web, bounded by:
  - the outside column flange;
  - the rafter top flange;
  - the rafter end-plate / web stiffener;
  - the column web stiffener.
- Limit states: elastic or inelastic buckling, post-buckling tension field, and yield. **Plate buckling usually
  governs** in built-up gable knees. The AISC multi-storey panel-zone rule (shear yield only) is therefore not
  appropriate.
- **When tension field action is allowed:**
  - It needs anchorage at both ends of the diagonal, at the outer corner and the inner corner (A and B in
    Fig 5-3).
  - It develops **only for negative (gravity) moment with full-depth column web stiffeners**.
  - **It is not allowed with a partial-depth stiffener, or under positive moment (wind uplift)** (Murray 1986;
    Young and Murray 1996).
- **Required shear (LRFD):** Vu = Mu/h − Pu/2. Here h is the panel depth **at the rafter side**, and Mu, Pu are the
  moment and thrust at the rafter face.
- **Strength (LRFD, φv = 0.90):**
  - Aw = av·tw, where av is the panel width at the column top.
  - kv = 5 + 5/(av/h)².
  - Cv:
    - 1.10√(kvE/Fy) < h/tw ≤ 1.37√(kvE/Fy): Cv = 1.10√(kvE/Fy) / (h/tw)
    - above 1.37√(kvE/Fy): Cv = 1.51·kv·E / ((h/tw)²·Fy)
  - **Negative moment with full-depth stiffener:**
    - h/tw ≤ 1.10√(kvE/Fy): φVn = φv·0.6·Fy·Aw
    - otherwise: **φVn = φv·0.6·Fy·Aw·[ Cv + (1 − Cv) / (1.15·√(1 + (av/h)²)) ]**
  - **Positive moment, or partial-depth stiffener:** φVn = φv·0.6·Fy·Aw (stocky) or φv·0.6·Fy·Aw·Cv (no tension
    field).
- **Stiffeners.**
  - The combined width of the panel-zone stiffeners should be about the rafter flange width, at the **rafter
    flange thickness**.
  - Stiffener-to-column-flange welds develop the stiffener's **yield** on its net contact width (width minus the
    corner clip).
  - Stiffener-to-panel welds develop the stiffener.
- **ASD version (pp.61–63):** fv = V/(av·tw) against Fv = (Fy/2.89)·[...] ≤ 0.40·Fy. It is not needed for our LRFD
  calc.
- **Worked numbers (validation).**
  - Geometry: Mu = 9600 k-in., Pu = 75 k, h = 47.125 in., av = 41.1875 in., A572-50, tw = ¼ in. This gives
    Vu = 166.2 k, h/tw = 188.5, kv = 11.55, Cv = 0.286.
  - **Full-depth stiffener:** **φVn = 209.5 k, so OK**. Stiffener ½×4 in. with a ¾ in. clip: Anet = 1.625 in²,
    φTn = 73.1 k. 3/8 in. fillets: 81.4 k OK (using the 1 + 0.5·sin^1.5θ directional increase at θ = 90°).
    3/16 in. stiffener-to-panel welds: 375.8 k.
  - **Partial-depth stiffener:** the required tw = 0.320 in., so **use ⅜ in.** (h/tw = 125.7 > 112.5, assumption
    OK).
  - ASD Ex 1: V = 108.7 k, fv = 10.56 < Fv = 13.0 ksi OK. But the ⅜ in. fillets at 21 ksi give only 36.2 k
    < 48.75 k, so a **CJP** is needed. ASD Ex 2: tw = 0.325, so ⅜ in.
- **360-16 mapping:** use G2.1 / G2.2 (Cv2, Eq. G2-7 with its flange-proportion conditions), as in the basis
  warning.

**4.3 Splices.**
- Beam-to-beam end-plates (rafter splice, ridge) use the **same tables**. There is no "column flange", so both
  plates are designed as end-plates and the bolts are common to both.
- Flush plates suit splices near inflection points. Extended plates are used where the moment is large.
- With reversal, mix the configurations: for example, extended at the gravity-tension flange and flush at the
  other.


#### 5. Worked examples - inputs and results for calc validation (§3.2 pp.29–36, §4.2 pp.46–56)

All examples: LRFD, A572 Gr 50 plate (Fpy = 50 ksi), A325 bolts (Ft = 90 ksi), bp = bf. Units are inches, kips
and kip-in. The dᵢ / hᵢ pattern is hᵢ = h − tf − (row distance from the tension-flange inner face) and
dᵢ = hᵢ − tf/2. Outer row: h0 = h + pf,o and d0 = h0 − tf/2. "Analysis" is the App. B φMn of the chosen design.

| Ex (pp.) | Type | Mu | Inputs | Y | P1: db → φMnp → tp | P2: tp, db, Qmax, φMq | Analysis φMn P1 / P2 |
|---|---|---|---|---|---|---|---|
| 3.2.1 (29–30) | 2F, snug | 600 | bp 6, tf ¼, g 2¾, pf 1⅜, h 18; d1 16.25, h1 16.375; s 2.03 | 100.5 | 0.59 → ⅝; 673; 0.45 → **½** | 0.41 → 7/16; ¾ in.: w′ 2.19, aᵢ 0.65, F′ 10.2, Q 7.49; Tb 14; max(788, 341) = **788** | 673 (bolt) / 693 (plate) |
| 3.2.2 (30–32) | 4F, snug | 600 | as 3.2.1 + pb 3; d2 13.25, h2 13.375 | 127.1 | 0.44 → ½; 783; 0.436 → **7/16** | 0.36 → ⅜; ½ in.: w′ 2.44, aᵢ 1.47, F′ 6.56, Q 2.83; Tb 9; max(658, 398) = **658** | 783 / 643 (plate) |
| 3.2.3 (32–34) | 4FS-b, full T | 900 | bp 6, tf ¼, g 3, pf 1½, pb 3, ps,o 1⅜, ts ⅜, h 16; ps,i 1.25; d 14.125 / 11.125, h 14.25 / 11.25; s 2.12 | 155.1 | 0.58 → ⅝; 1045; 0.46 → **½** | 0.40 → 7/16; ¾ in.: aᵢ 0.65, F′ 9.35, Q 7.59; Tb 28; max(1220, 1061) = **1220** | 1045 / 1069 (plate) |
| 3.2.4 (34–36) | 4FS-i, full T | 900 | as 3.2.3 with ps 1½, so s = 1.5 (capped) | 105.0 | ⅝; 1045; 0.55 → **9/16** | 0.49 → ½; ⅝ in.: w′ 2.31, aᵢ 1.80, F′ 10.6, Q 3.80; Tb 19; max(901, 720) = **901** | 1045 / 901 (bolt + prying) |
| 4.2.1 (46–48) | 4E, snug | 1750 | bp 8, tf ⅜, g 3, pf,i 1¾, pf,o 2½, pext 5, h 24; d0 26.3125, h0 26.5, d1 21.6875, h1 21.875; s 2.45 | 187.4 | 0.59 → ⅝; 1987; 0.51 → **9/16** | 0.46 → ½; ¾ in.: w′ 3.19, aᵢ = aₒ 1.01, F′ᵢ 12.8, Qᵢ 9.48, F′ₒ 8.75\*, Qₒ 9.69; Tb 14; max(2175, 1644, 1539, 1008) = **2175** | 1987 / 2108 (plate) |
| 4.2.2 (48–50) | 4ES, snug | 1750 | as 4.2.1; de 2.5 > s → Case 1 | 320.1 | ⅝; 1987; 0.39 → **7/16** | 0.35 → ⅜; ¾ in.: aᵢ = aₒ 0.38, F′ᵢ 8.11, Qᵢ 14.3, F′ₒ 5.68, Qₒ 14.6; max(1824, 1450, 1382, 1008) = **1824** | 1987 / 1824 (bolt + prying) |
| 4.2.3 (50–52) | 1/2, full T, + axial | 2200 + 200 = **2400** | as 4.2.1 + pb 2½; d2 19.1875, h2 19.375; Tu 16.9 k → 16.9/2 × 23.625 | 216.1 | 0.58 → ⅝; 2782; 0.56 → **9/16** | 0.50 → ½; ¾ in.: aᵢ 1.01, F′ᵢ 12.8, Qᵢ 9.48, F′ₒ 8.96, Qₒ 9.68; Tb 28; max(2981, 2906, 2897, 2822) = **2981** | 2782 / 2431 (plate) |
| 4.2.4 (52–54) | 1/3, full T | 4600 | bp 8, tf ⅜, g 3, pf,i 1¾, pf,o 2½, pb 2½, pext 5, h 36; d 38.3125 / 33.6875 / 31.1875 / 28.6875; h 38.5 / 33.875 / 31.375 / 28.875 | 380.3\*\* | 0.57 → ⅝; 5460; 0.60 → **⅝** | 0.52 → 9/16; ¾ in.: aᵢ = aₒ 1.47, F′ᵢ 15.6, Qᵢ 8.18, F′ₒ 10.9, Qₒ 8.39; max(6074, 5735, 5878, 5539) = **6074** | 5460 / 5415 (plate) |
| 4.2.5 (54–56) | 1/3S, full T | 4600 | as 4.2.4; de 2.5, s 2.45 → Case 1 | 573.0 | ⅝; 5460; 0.48 → **½** | 0.42 → 7/16; ¾ in.: aᵢ = aₒ 0.65, F′ᵢ 10.3, Qᵢ 11.4, F′ₒ 7.21, Qₒ 11.6; max(5588, 5550, 5576, 5539) = **5588** | 5460 / 4935 (plate) |

Notes on the printed examples, found during the recomputation:
- \* Ex 4.2.1: F′ₒ = 12.8 × 1.75/2.5 = **8.96**, not 8.75. Qₒ changes in the third digit only. Ex 4.2.3 prints the
  correct 8.96.
- \*\* Ex 4.2.4 uses **d3 = 28.6875 in place of h3** in Y (380.3). With h3 = 28.875, Y = **381.1**. A validated calc
  should reproduce 381.1 and note the difference.
- Ex 4.2.3's final check prints "2981 > 2500"; the required moment is 2400.
- Ex 3.2.3 and 3.2.4 compute d1 as "16 − 1.5 − 0.125" in the text, but the printed result 14.125 includes tf.
- The flush examples state that a ⅝ in. bolt was checked and found inadequate in Procedure 2 (not shown).
- Small rounding differences (for example, Qmax 7.49 vs 7.53 in Ex 3.2.1) come from w′ being rounded to two
  decimals in the book.
- Reproduced exactly in Python from the equations of §2: all Y values, s, w′, aᵢ, F′ and Q of every example, and
  the four φMq rows of Ex 4.2.1.
- **Test plan for the calc module:**
  - one pytest per row of this table (US units, tolerance about 1 %);
  - the same tests repeated in SI after unit conversion, to prove the SI constants of §2.9;
  - the panel-zone example of §4.2.


#### 6. Use on this project

Project geometry, from the MIDAS model as briefed. **To be confirmed against the model before any calc.**
- Column: tapered 300 → 800 × 250, web 8, flange 14.
- Rafter haunch: 800 → 350 × 250, web 6, flange 12, over 5.2 m.
- Rafter beyond the haunch: prismatic 350 × 200 × 6 × 10 to the ridge.
- Slope ≈ 18°.
- Canopies: H400×200×6×10.
- Gable rafters: H400×200. Gable posts: H400×150.
- SM520: JIS G3106 gives Fy 365 MPa for t ≤ 16 mm and 355 MPa for 16 < t ≤ 40 mm (confirm with the mill
  certificate); Fu ≈ 520 MPa. The brief uses ≈ 355 MPa.

**6.1 Range check against DG16 (Tables 3-6, 4-7).**

| Joint | h (mm) | bf × tf | Flush range fit | Extended range fit |
|---|---|---|---|---|
| Knee, rafter at the column face | ≈ 800 (≈ 840 measured on a plumb plate) | 250 × 12 | Out: h > 610, bp > 152, tf > 9.5 | **4E/4ES out (h > 610). 1/2, 1/3 and 1/3S in** (h ≤ 1575, bp 250 ≤ 260, tf 12 in 9.5 – 25) |
| Haunch-to-prismatic splice | 350 | 250 × 12 / 200 × 10 | Out: bp, tf, and h < 406 (2F would fit h, but not bp) | 4E/4ES: h 350 is **12 % below** the 400 lower limit; bp, tf, g in range |
| Ridge | 350 (≈ 368 on the plumb plate) | 200 × 10 | Out (bp 200 > 152, tf 10 > 9.5) | 4E: h slightly below range; rest in |
| Canopy to column | 400 | 200 × 10 | Out (bp) | **4E in range** (h = 400 at the lower bound) |
| Gable rafter splices | 400 | 200 × 10 | Out (bp) | **4E in range** |

Conclusions for the engineer:
- **(a) Flush plates fall outside DG16's tested range for all our members**, because our flanges (200 – 250 wide)
  exceed the 5 – 6 in. tested plate width. A flush splice would rest on extrapolation.
- **(b) Extended plates fit**: multiple-row at the 800-deep knee, and 4E/4ES at 350 – 400.
- **(c) The 350-deep rafter is just below the 4E tested depth.** I expect this to be acceptable, since a shallower
  section only shortens the lever arms already in the equations, **but that is the engineer's call**.

**6.2 Recommended configurations (proposal, for the engineer to decide).**
- **Knee.** A vertical rafter end-plate bolted to the column flange, as in DG16 Fig 5-2, with the column running to
  the roof line and a capped panel zone.
  - Gravity (negative) moment puts the outside, top flange in tension. Use **extended multiple-row 1/2 or 1/3**
    at the top, with the **stiffened 1/3S** if the plate gets thick.
  - The extension above the rafter top flange must fit under the roof purlins and sheeting, or the column must
    rise to contain it. **Coordinate with the purlin and eave-strut layout.**
  - **Wind uplift (positive moment)** puts the inside flange in tension. The plate can extend **below** the
    rafter bottom flange along the column flange, so use an extended row there too (a mixed configuration,
    p.9), sized for the reversed moment.
  - Add stitch bolts at mid-depth for the 800 mm plate (neglected in strength).
- **Haunch / prismatic splice at 5.2 m.**
  - Plate perpendicular to the rafter axis.
  - **4E both ways**, or 4E at the gravity-tension flange and a reduced extension at the other. Choose from the
    MIDAS moment envelope at that section (both signs).
  - **Gage g ≤ 200** (narrower flange, rule §3.2).
  - Design each half-plate with its own bf (250 vs 200; effective bp ≤ bf + 25).
  - The haunch bottom flange meets the plate at about 85° (taper ≈ atan(450/5200) ≈ 4.9°). The out-of-square
    flange force component is small, but state it.
- **Ridge.**
  - A **plumb (vertical) plate common to both rafters**, at 72° to each rafter axis.
  - Gravity puts the bottom flange in tension, so use an **extension below the bottom flange** (4E). Uplift puts
    the top flange in tension, where an extension above the top flange clashes with the ridge purlins and
    sheeting, so use flush rows there, or confirm the clearance.
  - **Sloped-plate treatment (judgement; not in DG16).** Two options:
    - Conservative: use dᵢ and hᵢ measured **perpendicular to the rafter axis**, and resolve the rafter N and V
      into the plate's normal and in-plane components.
    - The alternative uses the plumb lever arms (× 1/cos18° ≈ +5 %). I would not take that benefit.
  - The flange-to-plate fillet welds become skewed (dihedral 72° / 108°). Size them with the DG24 / DG21
    skewed-fillet factors (Part C, Part D §1.3).
- **Canopy to column.** 4E (Table 4-2), with tension at the top under gravity and reversal under uplift.
  - The column flange (14 mm) and web (8 mm) need the column-side checks: **DG4 2nd ed. Ch.4, or 360-16 J10**.
  - Stiffeners are likely where the canopy meets the tapered column.
- **Gable rafter splices (H400×200).** 4E, from the moment at the splice.
- **Monitor (H100×100):** not an end-plate moment case. Treat it separately.

**6.3 Calc steps to implement** (`calc_endplate.py`; numbers flow from the MIDAS results, never retyped):
1. **Inputs.**
   - From the member catalogue: h, bf, tf, tw at the section.
   - Plate: Fpy, and the plate material (SM520 or SS400; **engineer to choose**).
   - Bolt grade: ISO 8.8 ≈ Group A (Ft = 0.75·800 = 600 MPa), or 10.9 / JIS F10T ≈ Group B (Ft ≈ 750 – 780 MPa).
   - Bolt pretension Tb: 360-16 Table J3.1M, or 0.70·Fu·As.
   - Tightening: snug or fully tightened.
   - Geometry: g, pf,i, pf,o, pb, pext, de, ts.
   - Forces: Mu (both signs), Nu, Vu at the plate, from the MIDAS envelope.
2. **Geometry derivation.** Compute hᵢ and dᵢ (DG16 definitions, §5 pattern), s, and the pf → s cap.
   **Range-check against Table 4-7 or 3-6 and print a `!!` warning when outside.** Check pf ≥ db + 13 (or 19) mm,
   g ≤ bf, and bp,eff ≤ bf + 25.
3. **Effective moment.** Mu,eff = Mu + Nu·(h − tf)/2 (tension positive). **Whether compression relief may be taken
   is the engineer's decision.**
4. **Y** from the matching table (§2.5 / §2.7), with the Case 1 / Case 2 switch for stiffened types.
5. **Design.** Procedure 1 or 2 (§2.2 / §2.3), then the App. B analysis (§2.4) of the chosen tp and db.
   Report φMpl/γr, φMnp, φMq and the governing mode. Guard the aᵢ > 0 and radicand > 0 checks.
6. **Shear.**
   - Bearing type: compression-side bolts only, with 360-16 J3.6 / J3.7 shear and the tension interaction where
     they share.
   - Slip-critical, if chosen: J3.8.
   - Plate bearing and tear-out: J3.10.
   - Web shear on the restricted length of §3.2.
7. **Plate shear rupture** through the outer holes (360-16 J4.2); plate shear yield.
8. **Welds.**
   - Flange-to-plate: develops Fy·bf·tf, or Mu-based but ≥ 0.6·Fy·bf·tf. Double fillets with the skew
     correction at the knee and ridge, or CJP.
   - Web-to-plate: develops web yield near the tension rows (≥ 60 %), plus shear.
9. **Stiffeners** (4ES / 1/3S, DG4): ts ≥ tw·Fy,b/Fy,s, Lst = hst/tan30°, welds.
10. **Column side** (knee, canopy): flange bending (DG4 2nd ed. Yc), J10 web yielding, crippling and buckling,
    continuity plates.
11. **Knee panel zone** (DG16 Ch.5 mapped to 360-16 G2):
    - Vu = Mu/h − Pu/2 for **both moment signs**. Tension field only for negative moment with a full-depth
      stiffener.
    - Indicative only, geometry to confirm: the column web is 8 mm at about 772 mm clear and h ≈ 840 mm, so
      h/tw ≈ 105. That is about the 1.10 – 1.37√(kvE/Fy) band (≈ 86 – 108 for kv ≈ 11, Fy 355). **The panel is
      near or in the buckling range, so a doubler or a thicker panel plate may be needed under uplift**, where no
      tension field is allowed.
12. **Stiffness.** Extended plates qualify as FR at 100 % of capacity (§1.4), which matches the MIDAS rigid-joint
    assumption. Flush plates need γr = 1.25.
13. **Tests.** The §5 table reproduced in pytest (US units, then SI).

**6.4 What an end-plate detail on the drawings must show** (with the steel detailing instruction S3 – S9):
- Plate: size bp × length × tp, material grade, and the cut relative to the member (perpendicular, or plumb with
  the angle stated).
- Bolts: grade, diameter and number. **Tightening: SNUG-TIGHT or PRETENSIONED stated explicitly** (360-16
  J3.1: anything other than snug must be identified on the design drawings). Hole size. Washer and nut
  requirements.
- Fully dimensioned bolt pattern: g, pf,i, pf,o, pb, pext and de, plus the plate edge distances. **Mirror the
  pattern** on the column flange or the mating plate (match-drilled, as in DG4 p.23 on tolerances).
- Welds:
  - flange-to-plate weld (CJP symbol, or double fillet size, with the skew noted);
  - web-to-plate weld, with a different size near the tension rows if used;
  - **no weld access holes** (p.13).
- Stiffeners: extension stiffener (ts, Lst, 30° slope, landings, clip, welds); flush gusset plates; column
  continuity plates; panel-zone stiffener (full or partial depth, the 25 mm stop from the outer flange for
  partial); doubler plates.
- Stitch bolts where used (noted as "not counted in strength").
- A note on the governing design basis (AISC DG16 / 360-16, LRFD), the mill-scale/paint condition of the faying
  surfaces if slip-critical, and the fit-up tolerance requirement (plate flatness, mill-to-bear contact on the
  compression side).

**6.5 Open questions for the engineer** (to list in the job README):
1. **Tightening:** snug-tight (DG16 accepts it for wind) or fully pretensioned? A fluctuating Thai monsoon/storm
   wind envelope and 360-16 J3.1(a)(2) ("loosening ... not a design consideration") point to pretensioning.
   This is the engineer's decision.
2. **Bolt grade:** 8.8 (Group A, snug allowed) or 10.9 / F10T (Group B, must be pretensioned)?
3. **End-plate material:** SM520 or SS400 / SM400 (Fpy 235 – 245)? This changes tp a lot.
4. **Knee arrangement:** vertical plate on the column flange (DG16 Fig 5-2), or horizontal column-top plate?
   Can the top extension fit under the purlins, or does the column rise above the rafter top?
5. **Ridge plate:** plumb cut (common practice), with the conservative perpendicular lever arms of §6.2?
6. **Rafter splice:** accept 4E at h = 350 mm, 12 % below DG16's tested depth? Or use a deeper splice location,
   or a stiffened 4ES?
7. **Axial compression relief** in Mu,eff: take it, or ignore it (conservative)?
8. **Panel zone under uplift** (no tension field): accept a thicker panel web or a doubler at the knee?
9. **Webs (6 – 8 mm) near the tension bolts:** DG16 gives no rule. Develop web yield in the weld, and check web
   local yielding over the bolt group (judgement)?
10. **Fatigue:** confirm there are no crane loads, so that DG16's static-load scope holds.

---

# Part H. AISC Design Guide 25 - Frame Design Using Web-Tapered Members


Working digest for the tapered portal-frame job (MIDAS GEN NX model: 26 m span gable frames at 10 m centres,
9 bays, SM520 Fy 355 MPa, tapered welded columns and rafter haunches, pinned bases, wind-governed, Thailand).
Reviewed 2026-10-04. File: `G:\My Drive\##Textbook\AISC Design Guide\AISC - Steel Design Guides 2016\AISC - Steel
Design Guides 2016\Design Guide 25 - Frame Design Using Web-Tapered Members.pdf` (225 pp.). Authors Kaehler, White
and Kim; AISC 2011; funded by MBMA and AISI.

**Page convention.** "p.NN" means the **PDF page**. The scan is not a clean book:
- PDF pp.1–37: book page = PDF − 7 (p.8 = book p.1, p.37 = book p.30).
- **PDF pp.38–51 are a duplicate scan of book pp.17–30** (the whole of Chapter 4 a second time). This digest cites
  the first copy, pp.24–37.
- PDF pp.52–225: book page = PDF − 21 (p.52 = book p.31, p.160 = book p.139, p.225 = book p.204).

Read method: text pulled with PyMuPDF for all 225 pages (block mode); the equation-heavy and figure pages were viewed
as images (pp.9, 57, 79, 80, 82, 83, 160, 170). The garbled fractions of the scan were resolved from the numbers
(for example the Example 5.2 holes are 11/16 in., found from Ae = 5.44 − 4(11/16 + 1/16)(1/4) = 4.69 in.²).

**Basis warning.** The Preface (p.4) and §1 (p.8) say DG25 is based on **AISC 360-05**, and that its advice applies
equally to **360-10** with some section and equation numbers changed. It is **not** written against 360-10 as such.
Our calc cites **AISC 360-16**. These items moved or changed; I checked each one in `G:\My Drive\##Textbook\
a360-16-spec-and-commentary.pdf` (PDF pp.82–86, 111–112, 129–131, 296–303):

| DG25 cites (360-05) | Where it is in 360-16 | Change that matters to us |
|---|---|---|
| Direct analysis method, App. 7 | **Chapter C** (C2 required strengths, C3 available strengths) | DM is now the main method |
| ELM "design by second-order analysis" C2.2a; FOM C2.2b | **Appendix 7** (7.2 ELM, 7.3 FOM) | — |
| B1–B2 amplified first-order, C2.1b | **Appendix 8** | — |
| App. 7.3(1): P-δ on the overall response may be ignored when αPr < 0.15PeL | **C2.1(b)**: may be ignored only when (1) gravity is carried mainly by vertical columns, (2) Δ2nd/Δ1st ≤ 1.7 (reduced stiffness) **and (3) no more than 1/3 of the gravity load is on moment-frame columns** | Condition (3) **fails for a portal frame** (all the gravity is on moment-frame columns). P-δ must be in the analysis (subdivided elements or P-δ elements) |
| Notional load 0.002Yi, additive when Δ2nd/Δ1st > 1.5 (1.71 with reduced stiffness) | **C2.2b**: Ni = 0.002αYi, additive when the ratio > **1.7** (reduced stiffness) | Same in practice |
| τb with Py = AgFy | **C2.3(b)**: τb with **Pns** (= FyAe for slender sections) | — |
| E7 slender elements with **Q = QsQa** | **E7 effective-area method** (Ae from effective widths); no Q | DG25 §5.3.3 Q-steps must be redone in 360-16 terms |
| Table B4.1 | **Table B4.1a** (compression), **B4.1b** (flexure) | — |
| F4-10 rt with ho/d terms | **F4-11** rt = bfc / √[12(1 + aw/6)] | Simpler; slightly different number |
| DG25 extension "Rpc = Rpt = 1 when Iyc/Iy ≤ 0.23" | Now in the Spec (**F4-10**, F4-16) | Adopted |
| G2 unstiffened kv = 5; Cv with elastic branch 1.51kvE/((h/tw)²Fy) | **G2.1**: kv = **5.34**; Cv1 = 1.10√(kvE/Fy)/(h/tw) (no elastic branch) | 360-16 gives a **higher** shear strength for slender webs (see §7.3) |
| G3 tension field; DG25 §5.6.3 flange-size limits as an extension | **G2.2** "interior panels a/h ≤ 3": full TFA when 2Aw/(Afc+Aft) ≤ 2.5 and h/bf ≤ 6 (G2-7), otherwise the "true Basler" form (G2-8) | DG25's extension adopted |
| App. 6 relative / nodal bracing | **App. 6** panel / point bracing; **6.4** beam-columns; **6.3**: inflection point is not a braced point | See §4 |

The member-strength method of DG25 (γe ratios, flange-stress Cb, per-flange checks) has no 360-16 equivalent for
tapered members; 360-16 still has no tapered-member provisions. DG25 Ch.5 remains the method; plug the 360-16 base
equations into it.

**Copyright.** Everything below is paraphrased. Equations are restated in my own notation; tables are reduced to the
numbers we need. No figure or passage is reproduced.

**Notation.** d = overall depth; h = clear web depth; ho = distance between flange centroids; tw, bf, tf = web thickness,
flange width, flange thickness (c = compression flange, t = tension flange; 1 = outside flange, 2 = inside flange);
Pr, Mr, Vr = required strengths (LRFD); fr = required stress at a section; α = 1.0 (LRFD) / 1.6 (ASD);
**γe = elastic buckling multiplier** of a member for a stated mode = (force or stress at elastic buckling) / (required
force or stress) — one number for the whole unbraced length; γeL = in-plane γe with pinned–pinned ends over L;
PeL = γeL·Pr; Peℓ = buckling load of one analysis element of length ℓ; I′ = equivalent moment of inertia (Eq 4.5-4);
Lb = unbraced length of the flange considered; Cb from flange stresses f2 (largest compression at an end), fmid, f0;
Los = full on-slope length of the rafters between columns; Lchord = span between column-top centroids; Q = slender
section factor (360-05); Rpc, Rpg, Rpt = web plastification / bend-buckling factors; FL = flange stress at the
onset of inelastic LTB/FLB; Cv = web shear coefficient; DM / ELM / FOM = direct analysis / effective length /
first-order methods.

US to SI used below: 1 ksi = 6.895 MPa; 1 kip = 4.448 kN; 1 kip-in. = 0.113 kN·m; 1 in. = 25.4 mm.

---

#### 1. Scope, limits and fabrication (Ch.1 – 3, pp.8–22)

##### 1.1 What the Guide covers (pp.8–10, 12–18)

- Member and frame design of web-tapered I-sections, aimed at metal-building proportions but stated to apply to
  similar fabricated members in conventional steelwork (p.8).
- It interprets and extends the AISC Specification; where it goes beyond the Spec it says so. Research base:
  Georgia Tech (White, Kim, Guney, Ozgur) — LTB, in-plane and out-of-plane column buckling, torsional and
  flexural-torsional buckling, local buckling, second-order software benchmarking, base fixity, end restraint
  (p.8).
- Tapered members have the **same limit states** as prismatic ones. "Local" limit states (yield, rupture, local
  buckling, unstiffened web shear buckling) are checked **section by section** with the Spec as written. Only the
  "overall" limit states (in-plane and out-of-plane buckling, LTB, combined force, stiffened-web shear) need the
  adjusted procedures of Ch.4 – 5 (p.12).
- Key difference from the old AISC 1989/1999 tapered appendix (pp.16–18): no equivalent-length charts (g, Kγ, hs,
  hw, B). Instead the elastic buckling load **ratio γe** is found for the real member (by eigenvalue analysis,
  successive approximations, or a closed form), and the AISC prismatic curves map γe·fr at the most-stressed
  section to the design strength. This works for any taper, steps, plate changes and singly symmetric sections.

##### 1.2 Limits of applicability (pp.8–9) — and our frame against them

| DG25 limit | Value | Our frame (SM520, Fy 355 MPa, E 200 000 MPa) |
|---|---|---|
| Fy | ≤ 55 ksi (≈ 380 MPa) | 355 MPa — OK (SM520 Fy = 345 if any plate > 16 mm) |
| Homogeneous | Fyf = Fyw (no hybrids) | OK |
| Web taper | linear or piecewise linear, angle 0° – 15° | column 300→800 over 6 m: 4.8°; haunch 800→350 over 5.2 m: 5.0° — OK |
| Flange thickness | tf ≥ tw | 14 ≥ 8, 12 ≥ 6, 10 ≥ 6 — OK |
| Flange slenderness | bf/2tf ≤ 18 | 8.9 / 10.4 / 10.0 — OK |
| Flange width | bf ≥ h/7 over each Lb (h/9 if Lb ≤ 1.1rt√(E/Fy)) | 250 ≥ 772/7 = 110 — OK |
| Web, no stiffeners or a/h > 1.5 | h/tw ≤ 0.40E/Fy ≤ 260 | 0.40E/Fy = 225; max h/tw = 129 (haunch deep end) — OK |
| Web, stiffeners at a/h ≤ 1.5 | h/tw ≤ 12√(E/Fy) | not needed |

The research focused on Fy = 55 ksi; higher grades and hybrids are "expected" to work but were not studied (p.9).
Parabolic tapers are in principle covered but their elastic buckling loads are outside the Guide (p.9).

##### 1.3 Fabrication of web-tapered members (pp.9–10)

- Typical shop process: cut flanges and web from plate, coil or bar and splice to length → punch holes for bracing,
  purlin and girt bolts → tack the flanges to the web lying flat → **weld both flanges at once from the top side
  only** with an automatic machine running end to end → weld end plates and stiffeners by hand.
- **One-sided web-to-flange fillet welds** are the industry norm and have a long satisfactory record; tests (Chen et
  al. 2001) show they transfer shear. Two-sided welds are needed **only when the required weld strength exceeds a
  one-sided weld**, or at member ends of seismic IMF/SMF frames (manual welds added on one or both sides).
- The weld must carry the shear flow **VQ/I** plus any local concentrated load between web and flange (Q = first
  moment of the flange about the neutral axis, I of the full section) (p.10; repeated as Eq 5.6-12, p.118).
- Automatic welders need **equal flange widths along the whole member**; inside and outside flanges are therefore
  normally the same width (thicknesses may differ). Unequal widths need pull-through or blocked welders and are
  avoided. Unequal flanges make the section singly symmetric (p.10).
- Plate thickness note (p.124): the Steel Construction Manual recommends thicknesses up to 3/8 in. in 1/16 in. steps.
- Splices/joints: DG25 assumes **bolted end-plate connections** between frame members; full-height end plates are
  treated as FR moment connections, partial-height or thin end plates as pins (p.161). Field splices and plate
  transitions inside an unbraced length are allowed for in the method (steps in section) (p.9). Panel zones at
  knees: use AISC DG16 Ch.5 (p.123). Moment end-plate splices may anchor tension-field action in negative-moment
  regions (Murray and Shoemaker 2002) (p.117).

##### 1.4 Design basis (pp.20–22)

LRFD (Ru ≤ φRn) or ASD (Ra ≤ Rn/Ω); ASD and LRFD are calibrated equal at L/D = 3. Second-order analysis for ASD must
be run at **1.6 × ASD combinations** and the results divided by 1.6, which removes much of ASD's advantage in
high-live-load frames (p.21). Stress-format ASD (required stress ≤ allowable stress) is acceptable if converted
consistently (p.22).

#### 2. Analysis of tapered frames (Ch.4, pp.24–37; Ch.6, pp.160–170)

##### 2.1 What every method must include (pp.24–27)

AISC stability design must account for: second-order effects (P-Δ and P-δ), system out-of-plumbness and member
out-of-straightness, stiffness loss from residual stress, flexural/shear/axial deformations, and connection
flexibility (p.26). P-δ in singly symmetric or stepped members includes the offset of the curved or kinked centroid
from the chord; subdividing a member into elements turns member P-δ into element P-Δ (Fig 4-3, p.25). Connection
classification: rigid if secant stiffness ≥ 20EI/L (or ≥ 0.5EI/d at 0.7Mp, Bjorhovde), pin if ≤ 2EI/L (≤ 0.1EI/d at
0.2Mp), using d at the connection for tapered members (pp.26–27).

Clear-span frame behaviour is a **moment-amplification (load–deflection) problem, not a bifurcation problem**; the
buckling load is usually many times the ultimate load. This is why DG25 prefers the DM, which concentrates on
getting the amplified moments right (p.15).

##### 2.2 Choosing the method (pp.27–31)

| Item | DM | ELM | FOM |
|---|---|---|---|
| Allowed when | always | Δ2nd/Δ1st ≤ 1.5 (1.71 reduced stiffness) | Δ2nd/Δ1st ≤ 1.5 and αPr ≤ 0.5Py in all lateral members |
| Analysis | second order, reduced stiffness | second order, nominal stiffness | first order with large notional loads, then × B1 |
| Notional loads | 0.002Yi; minimum (gravity combos only) when Δ ratio ≤ 1.7 reduced, additive otherwise | 0.002Yi minimum in gravity combos | Ni = 2.1(Δ/L)Yi ≥ 0.0042Yi in all combos (Eq 4.6-8) |
| In-plane column length | K = 1 (or Pni = QPy, §2.6) | K from a sway buckling analysis unless Δ ratio ≤ 1.1 | K = 1 |

- Δ2nd/Δ1st is per load combination, at strength level, unreduced stiffness unless stated: < 1.1 negligible,
  1.1 – 1.5 moderate, > 1.5 large (DM only). **Do not use M2nd/M1st** as a proxy: gravity moments hide the sway part
  (p.31).
- **Gable frames (§6.3.3, p.169, Fig 6-7):** under gravity the eaves spread symmetrically, which is not sway. Use the
  **column-top drifts averaged with the column axial loads as weights**. DG25's example: first order −0.80 in. and
  +1.2 in. at columns carrying 15 and 20 kips → (−0.80·15 + 1.2·20)/35 = 0.343 in.; second order −0.70/+1.3 → 0.443
  in.; ratio **1.29**. Using the larger column alone gives 1.3/1.2 = 1.08, a wrong and unsafe answer.

##### 2.3 Notional loads and out-of-plumbness (pp.28–29, 33, 36, 166–168)

- Based on an erection out-of-plumb of **H/500**. Scale linearly for another tolerance: the old MBMA (2002) H/300
  tolerance needs × 1.67 (MBMA 2007 dropped it) (p.28). Explicit out-of-plumb geometry may be used instead and is
  easier for sloping or irregular frames (p.29).
- Notional loads are a share of **all vertical load** in the combination (not only "gravity"), applied **at the top
  of each column in proportion to the vertical load that column receives**, and at any intermediate vertical load on
  a column (crane, mezzanine, canopy) (pp.28, 33, 36).
- Direction: with lateral load, in the direction of the lateral load only; gravity combos with net sway, in the
  sway direction; symmetric gravity combos, **both directions** as separate combinations (pp.28–29, 166).
- Fig 6-4 example (p.166), H/300: column loads 10 and 25 kips → N = 0.0333 and 0.0833 kips. Fig 6-5 (p.167): explicit
  offsets for 20, 23.3, 26.7 and 40 ft columns at H/300 = 0.800, 0.932, 1.07, 1.60 in. Move **all** nodes by 0.0033H
  (bases included) so rafter lengths do not change.
- **Lean-on structures** (lean-tos, mezzanines, tilt-up panels braced by the frame) must be in the second-order model:
  their height, the vertical load they put on the frame, and their notional loads. Example Fig 6-6 (p.168): 25 ft
  tributary width, H/500, Y1 = 30 kips (half the panel weight, since its centroid is at mid-height) → N1 = 0.060
  kips; Y2 = 16.9 kips → N2 = 0.0338 kips; N3 = 0.00375 kips.

##### 2.4 Stiffness reduction for the DM (pp.35, 165)

- Use **0.8EI** (and 0.8EA) in the second-order strength analysis; if αPr/Py > 0.5 use 0.8τbEI with
  τb = 4(αPr/Py)(1 − αPr/Py) (Eq 4.6-7), only over the part of the member where it applies, or keep 0.8EI and add
  notional loads of 0.001Yi (p.35).
- **Recommended: reduce E to 0.8E for all members** rather than editing A and I. This avoids false drift from
  differential shortening between gravity and frame columns and matches the calibration of the DM (pp.35, 165).
- The reduction is for the strength analysis only. Never use it for service deflections, slenderness limits or the
  member resistance equations (E = 200 000 MPa there) (pp.35, 165).
- Rafter stiffness under thrust (p.165): only for amplified-first-order or rectangular-frame idealisations (B1–B2,
  story-stiffness γe, FOM), reduce rafter EI to EI′ = (1 − αPr/Pe(0.5Los))·EI (Eq 6.2-1a; × 0.8τb in DM, Eq 6.2-1b)
  when α/γeL > 0.05. **A general matrix P-Δ analysis with the subdivision of Table 6-3, or elements with P-δ terms,
  captures this automatically.**

##### 2.5 Modelling tapered members and number of elements (pp.32–35, 160–164, 194–196)

- Use either a dedicated tapered element (numerically integrated, accuracy depends on its internal subdivision) or
  **a chain of short prismatic elements with the average properties of each piece** (Fig 6-1), which converges with
  refinement (p.160).
- Unequal flanges: the centroid is off mid-depth and **curved** (toward the heavier flange) — about L/600
  out-of-straightness at 15° taper (Fig 6-2). Put element nodes **on the centroid**, not on a straight line. At plate
  changes the centroid jumps (up to several inches, Fig 6-3): add a short link or shift the axes to a common point
  (pp.160–161). (Our sections are doubly symmetric, so this does not arise.)
- Knee panel zones are normally modelled as at least as stiff as the members (member stiffness carried to the work
  point); DG25 warns a rigid panel **may be somewhat unconservative** (p.161). Shear deformation usually ignored.
- Bases: usually designed pinned; partial fixity may be modelled with springs (Eroz et al. 2008: a realistic base
  reduced service vertical/lateral deflections by about 10 % / 20 %, strength checks changed little) (pp.161, 189).
  Support thrust movement can matter for long-span, short-column frames; keep footing elements that resist lateral
  movement at low stress (p.161).
- **Element subdivision for a P-Δ-only matrix analysis** (5 % on nodal displacement, 3 % on internal force, at up to
  about 0.68 of the elastic buckling load) (pp.162–163). Required number of elements per member, entered with
  αPr/PeL of the member (reduced stiffness in the DM):

| Table 6-1: sway columns, pinned base | Table 6-2: sway columns, both ends restrained | Table 6-3: rafters and non-sway columns |
|---|---|---|
| ≤ 0.05 → 1; ≤ 0.12 → 2; ≤ 0.17 → 3 | ≤ 0.12 → 1; 0.23 → 2; 0.31 → 3; 0.47 → 4; 0.58 → 5; 0.68 → 6 | ≤ 0.05 → 1; 0.20 → 2; 0.36 → 3; 0.50 → 4; 0.61 → 5; 0.67 → 6; 1.18 → 7; 1.35 → 8; 2.12 → 9; 2.42 → 10; 2.65 → 11 |

  "Restrained" means end stiffness ≥ 1.5EI′/L (≥ 1.5·0.8EI′/L in the DM). Sway columns carrying large gravity
  moments must satisfy both Tables 6-2 and 6-3 (p.163). DG25 also recommends subdividing whenever αPr > 0.05PeL in
  a P-Δ-only DM analysis, except restrained sway columns up to 0.12PeL (p.34).
- **Elements with P-δ (cubic) geometric stiffness** need far fewer: sway columns 1 element up to αPr/Pcr = 0.83;
  non-sway members 2 elements up to 0.66; 1 element if αPr/PeL < 0.17 (p.163).
- **Moments between nodes:** element P-δ may be ignored when αPr ≤ 0.02Peℓ. Otherwise amplify within the element:
  δ2 = δ1/(1 − αPr/Peℓ), M = M1 + αPr·δ2 (Eqs 4.6-4, 4.6-5; good to αPr/Peℓ ≤ 0.7, keep ≤ 0.13 for 3 %), or B1 =
  Cm/(1 − αPr/Peℓ) ≥ 1 with a **stress-based** Cm = 0.6 + 0.4(f1/f2), f1 = 2fmid − f2 (Eq 4.6-6). Use Cm = 1.0 when
  there is load between the nodes (pp.32–35, 161).
- Eurocode limit quoted by DG25 for rectangular-idealisation P-Δ methods on pitched frames: roof slope ≤ 26° and
  αPr < 0.09PeL in the rafters with PeL over the **full on-slope length Los**; a direct-stiffness P-Δ analysis does not
  have the slope limit (p.162).
- Eigenvalue buckling needs more elements than load–deflection analysis (Tables B-1 to B-3, pp.195–196): sway
  columns, P-Δ-only, 1/2/3 elements → 22/5/2 % error on γe; rafters 4/6/8/16 elements → 22/10/5/1 %. With P-δ
  elements, a node near mid-span and 2 elements give about 3 %.
- **Benchmark the software first** (Appendix C, pp.198–212): prismatic closed forms (Table C-1) up to αPr/Pcr =
  0.67, then the tapered cases (§6.2). Prismatic-element subdivision is fine in plane but **gives wrong LTB answers
  when torsion matters**, however fine (Andrade and Camotim; Boissonnade and Maquoi; pp.16, 182) — do not trust a
  stepped-prismatic 3D eigen-analysis for LTB of a tapered member.
- Second-order analysis is nonlinear: **run each load combination separately**; do not superpose second-order
  results of load cases (p.165). LRFD combos are run as they are (p.166).

##### 2.6 In-plane column and rafter strength in the DM (pp.36, 59)

Use K = 1 on the actual length with **nominal** stiffness in the strength equations; and **Pni may be taken as the
section strength QPy** (no in-plane buckling check) when any of these holds:
(a) **α/γeL ≤ 0.10** (nominal stiffness) — "many members in a typical single-storey frame" satisfy this;
(b) P-δ is in the analysis **and** member out-of-straightness of 0.001L between supports is modelled;
(c) **gable rafters whose mid-span work point is ≥ Lchord/50 above the chord** between column-top centroids — true for
any pitch ≥ 2:12 between equal columns. Then Pr/Pni = max fr/(QFy) along the member (p.59).

For the ELM, rafter effective lengths: industry K = 1 for rafters works; the "column-to-ridge" design length is not
reliable — the shortening comes from column end restraint, not from the ridge kink. For short columns K on Los is near
0.5, rising with taller columns. Use an eigen-analysis (the rafter mode is usually the **second** eigenvalue) or
successive approximations with real end springs (pp.169, 195–196).

#### 3. Member strength (Ch.5, pp.52–159)

All required forces include second-order effects from §2. Strength ratios Pr/Pc, Mr/Mc are carried into the
interaction equations (p.52).

##### 3.1 Tension (pp.52–54)

Yield on the gross area at the small end (φ 0.90) and rupture on the net area at holes (φ 0.75). For isolated purlin
or brace holes that do not transfer member force, U = 1.0 and net area = gross − holes at (d + 1/16 in.) (p.52).
Example 5.1: rupture at the holes governs (φPn 205 vs 223 kips).

##### 3.2 Axial compression — the γe method (pp.54–59)

Because Fe = γe·fr at every section, the E7 curve becomes (Eq 5.3-9/10): if QFy/(γe fr) ≤ 2.25,
Fcr = Q·0.658^(QFy/(γe fr))·Fy; else Fcr = 0.877γe fr. Steps for **each buckling mode and each unbraced length**:

1. **Elastic ratio γe** (p.56):
   - *In plane*: γex = Pex/Pr over the whole member, pinned ends in the DM/FOM. Not needed in the DM if α/γeL ≤ 0.10 or
     P-δ + out-of-straightness are modelled (§2.6).
   - *Out of plane flexural*: Pey = π²EIy/(KyLb)² with properties at **mid-length** of the unbraced length. Ignore a flange
     plate change within 20 % of Lb from the small end if Iy changes less than ×2; otherwise use successive
     approximations. Ky < 1 only if the neighbour is then checked with Ky > 1.
   - *Torsional* (doubly symmetric): need not be checked when KzL ≤ KyLb (never more than a few % below flexural)
     (Eq 5.3-12). Better J (Eq 5.3-13): J = htw³/3 + Σ bf tf³/3·(1 − 0.63tf/bf).
   - *Flexural-torsional* (singly symmetric): only if flange widths differ or thickness ratio > 1.5 (Eq 5.3-14).
   - **Constrained-axis torsional buckling (CAT)** — applies when **the inside flange brace spacing is longer than the
     girt/purlin spacing on the outside flange** (Eq 5.3-15, Fig 5-2, p.57):
     PeCAT = [π²E(Cw + Iy·as²)/(Kz Lb,inside)² + GJ] / (rx² + ry² + ac²),
     Cw = ho²·Iy1/(Iy1/Iy2 + 1), Iy1 = tf1bf1³/12 (outside), Iy2 = tf2bf2³/12 (inside), ac and as = distances from the
     girt/purlin centroid to the member centroid and shear centre, KzLb,inside = distance between inside-flange
     braces; properties at mid-length of the inside unbraced length.
   Use the **largest Pr** in the unbraced length for the out-of-plane modes (an average is not safe) (p.56).
2. **Fn1** at the section with the highest fr/Fy (small end or a plate change) from the curve with Q = 1 (Eqs 5.3-20,
   5.3-21); γn1 = Fn1/frmax (Eq 5.3-22) (pp.57–58).
3. **Q and the critical section** (p.58): Qa with f = γn1·fr at each section; Qs of the flange(s) in net compression
   (smaller value if both). Critical = max fr/(QFy): with non-slender flanges, the small end or a plate change; with
   slender flanges also the section where **h/tw = 131** (where kc = 4/√(h/tw) reaches its 0.35 floor, so Qs stops
   falling) and the deep end.
   Conservative shortcut: use Fn1 = Fy (or f = Fy everywhere) for Q (p.59).
4. **Fcr** at the critical section (Eq 5.3-23/24) and ratio fr/(φcFcr) (Eq 5.3-26) (pp.58–59).
5. Member axial strength = smallest of the in-plane value and each out-of-plane value per unbraced length; for
   beam-columns combine per unbraced length (p.59).

**360-16:** replace the Q steps by the E7 effective-area method (Pn = Fcr·Ae).

Equivalent I for in-plane PeL (Eq 4.5-4 / A-3, pp.31, 190): for a **single linear taper, constant plates, constant
axial force, pinned ends only**, PeL = π²EI′/L² with I′ = strong-axis I at the depth located
**0.5L·(Ismall/Ilarge)^0.0732 from the small end**. Errors < 0.4 % against successive approximations (Table A-1,
p.191). For varying axial force use γeL = PeL/(Pr)max (conservative). Also usable for Peℓ of one element (p.191).
Method of successive approximations (pp.191–192, Table A-2): iterate P-δ moments → conjugate-beam deflections until
the deflection ratio is uniform; handles steps and load changes; ignore centroid kinks in that analysis.

##### 3.3 Flexure (pp.79–85)

Limit states: compression flange yielding, LTB, compression flange local buckling (FLB), tension flange yielding
(TFY, unequal flanges), tension flange rupture (holes). Check at **both ends and mid-length of each unbraced length,
at every taper or plate change, and at peak stress** (p.79). One combined procedure covers any mix of compact,
noncompact and slender webs and flanges.

- **Cb from flange stresses** (Yura–Helwig, AASHTO form; Eq 5.4-1/2, pp.79–80), separately **for each flange**:
  Cb = 1.0 if fmid/f2 ≥ 1, f2 = 0 or cantilever; otherwise Cb = 1.75 − 1.05(f1/f2) + 0.3(f1/f2)² ≤ 2.3, where
  f1 = f0 if |fmid| < |(f0 + f2)/2|, else f1 = 2fmid − f2 ≥ f0 (compression positive). Fig 5-5 samples:
  f1/f2 = −0.375 → 2.19; 0.375 → 1.40; 0.50 (fmid/f2 0.75) → 1.30; 0.25 (fmid/f2 0.625) → 1.51.
  Do not use the H1.2 tension Cb increase for tapered members (p.80).
- **Rpc** (Eq 5.4-4/5, from F4-9) and **Rpg** (Eq 5.4-6, F5-6): Rpg = 1 − aw/(1200 + 300aw)·(hc/tw − 5.7√(E/Fy))
  ≤ 1, aw = hctw/(bfctfc) ≤ 10. Take Rpc = Rpt = 1 when Iyc/Iy ≤ 0.23. Optional refinement: use Mn(Rpg=1)/Sxc for Fy in
  Rpg (pp.81–82).
- **Compression flange yielding**: Mn = RpcRpgFySxc (Eq 5.4-8); redundant if the LTB cap is checked (p.82).
- **LTB — general procedure** (pp.82–83):
  1. FeLTB from F4-5 with **mid-length** properties and Cb: FeLTB = Cbπ²E/(Lb/rt)²·√(1 + 0.078·J/(Sxc ho)·(Lb/rt)²);
     J = 0 if the web is slender or Iyc/Iy ≤ 0.23 (Eq 5.4-10 to 5.4-12).
  2. γeLTB = FeLTB/fr at the section of **largest compression-flange stress** (Eq 5.4-13).
  3. FL = 0.7Fy; for compact/noncompact webs with Sxt/Sxc < 0.7, FL = FySxt/Sxc ≥ 0.5Fy (Eq 5.4-14/15).
  4. At each section with its fr: if γeLTB·fr/Fy ≥ π²/1.1² = **8.2** → no LTB; if between FL/Fy and 8.2 → inelastic
     Mn = RpgRpcMyc·[1 − (1 − FL/(RpcFy))·(π√(Fy/(γeLTB fr)) − 1.1)/(π√(Fy/FL) − 1.1)] ≤ RpgRpcMyc (Eq 5.4-16);
     if ≤ FL/Fy → elastic Mn = Rpg·γeLTB·fr·Sxc (slender web) or γeLTB·fr·Sxc (Eq 5.4-17/18).
  5. LTB ratio = largest Mr/Mn along the unbraced length. **Check every flange that is in compression anywhere in its
     length; the worse flange governs** (p.82).
- **LTB — single linear taper, plates constant** (more liberal, pp.82–83): compute (γeLTB)Cb=1 and multiply the
  resulting Mn by Cb, capped at RpgRpcMyc (Eqs 5.4-19 to 5.4-21). Kim (2010) found the general procedure closer to
  simulations for deep thin sections (p.187).
- **FLB** section by section (p.84): λ = bf/2tf; λpf = 0.38√(E/Fy); λrf = 0.95√(kcE/FL), kc = 4/√(h/tw) within
  0.35 – 0.76. Noncompact: Mn = Rpg[RpcMyc − (RpcMyc − FLSxc)(λ − λpf)/(λrf − λpf)] (Eq 5.4-22). Slender:
  Mn = 0.9RpgEkcSxc/λ² (Eq 5.4-23).
- **TFY** when Sxt < Sxc: Mn = RptFySxt (Eq 5.4-25 to 5.4-29) (p.84).
- **Tension flange rupture** at holes: no check if FuAfn ≥ YtFyAfg (Yt = 1.0 for Fy/Fu ≤ 0.8); otherwise
  Mn = FuAfn/Afg·Sxt (Eq 5.4-30, F13.1) (pp.84–85).
- Ratio Mr/(φbMn), φb = 0.90 (p.85).

##### 3.4 Combined force (pp.103–105)

- **H1-1a/b** with absolute values, all in-plane and out-of-plane limit states, per unbraced length; no Cm term
  (second-order effects are already in Mr) (Eq 5.5-1, p.104).
- **H1.3 (separate in-plane / out-of-plane) — do not use** for tapered or noncompact/slender members (p.105).
- **H2 stress form** (Eq 5.5-5) usable for any member at the flange tips with each flange's own available stress;
  conservative because stresses add at one point (p.105).
- **Tension flange rupture interaction** at hole lines (DG25 extension, Eq 5.5-2 to 5.5-4): Pr/Pc + Mrx/Mcx ≤ 1.0 with
  signs (tension positive), Mn = FuAfn/Afg·Sxt < FyZx if FuAfn < YtFyAfg, else FyZx; check each flange that is in
  tension (p.104).

##### 3.5 Shear (pp.116–118)

- Shear strength varies along the member; check unstiffened webs **section by section** at least at both ends, at
  steps in the shear diagram and at web thickness changes (p.116). Blodgett's "flange vertical component" shear
  reduction is **not** used (no research support) (p.116).
- Unstiffened (stiffeners further apart than 3hmin): Vn = 0.6FyAwCv, Aw = d·tw, kv = 5 (Eqs 5.6-1 to 5.6-5);
  h/tw ≤ 260 (p.116). [360-16: kv = 5.34, Cv1 = 1.10√(kvE/Fy)/(h/tw); see §7.3.]
- Stiffened, no tension field (clear spacing ≤ 3hmin): one Vn for the panel from the **mid-panel** section,
  kv = 5 + 5/(a/havg)²; not less than the unstiffened value at any section; thinner web if the thickness changes. The
  AISC a/h ≤ [260/(h/tw)]² handling limit may be waived if the members can be handled (p.117).
- Tension field (pp.117–118): not in end panels (but an end-plate splice can anchor it in negative-moment regions);
  a/hmin ≤ 3. Full field (Eq 5.6-8, a/hmin in the denominator) when 2Aw/(Afc+Aft) ≤ 2.5 and havg/bf ≤ 6.0
  (smallest flanges in the panel); otherwise "true Basler" (Eq 5.6-11). Valid to 15° taper. Panel stiffeners per
  G2.2/G3.3 with h at the stiffener.
- **Web-to-flange weld: Vrw = VrQ/Ix** (Eq 5.6-12); a larger weld than the minimum may be appropriate near
  connections (p.118).
- Example 5.5 (pp.118–123): web 18→24 in. × 1/8 in., flanges 1/4 × 6 in., 54 in. long, Fy 55 ksi:
  unstiffened Vn = 14.6 kips (18 in. end) and 10.9 kips (24 in. end); stiffened, no TFA, 14.4 kips; with TFA
  34.1 kips (φVn 30.7). Tension field more than doubles the strength of these thin webs.

##### 3.6 Concentrated forces and knees (p.123; bibliography pp.184–188)

J10 limit states with the local section. Web sidesway buckling: use the **average depth** over the unbraced length
(no research available). Knee panel zones: DG16 Ch.5. Tests: Murray (1986) — panel strength from shear yield/buckling
formulas is fine, but tension field only works with a **full-depth column web stiffener** at the rafter inside
flange; Jenner et al. (1985) — panel-zone yielding or buckling governed most knee tests and **knee flexibility made
whole frames fail below prediction** → thicker panel-zone webs; the full-depth stiffener must be **welded to both
column flanges and the web** (pp.184–185, 188); Sumner (1995) — LRFD panel shear provisions over-conservative (p.185).

#### 4. Stability bracing (flange braces) — what DG25 says and what it does not

**DG25 has no chapter on brace design** and no fly-brace detail. Brace strength and stiffness come from **AISC 360-16
Appendix 6**; the office detail is in **Part E** (Beca SE-1505 fly bracing) and `STEEL_DETAILING_INSTRUCTION.md` S9A.
What DG25 does contribute:

- **The braced flange matters.** In metal buildings the outside flange is braced by girts and purlins, the inside
  flange by diagonal flange braces from those girts/purlins; there is one in-plane length and a series of out-of-plane
  lengths per flange (p.55). LTB is checked **for each flange that is in compression anywhere**, with its own Lb and
  its own stress-based Cb (pp.79, 82).
- **One-sided bracing.** When inside braces are further apart than the girts/purlins, columns must be checked for
  **constrained-axis torsional buckling** (§3.2; Examples 5.6 – 5.8). With **no** inside-flange brace on a 12 ft
  column, CAT governed the axial strength (φPn 110 kips vs 125 kips with both flanges braced at the same point in Ex
  5.2) (pp.141, 59–78).
- **Tests:** Forest and Murray (1982) frame 1 failed through an **inadequate rafter compression-flange brace near the
  knee** (p.188). Salter et al. (1980): an intermediate restraint on the **tension** flange only gave torsional
  failures; restraint of the **compression** flange gave much higher loads (p.184). Ozgur et al. (2007): crediting
  end restraint from adjacent segments in the LTB check **raises brace demands** (p.186).
- Members with different brace spacing on the two flanges: check the shorter lengths as usual and the longer lengths
  (between points where both flanges are braced) by CAT (p.56).

**AISC 360-16 Appendix 6, restated (pp.296–303 of the 360-16 PDF)** — point braces, LRFD φ = 0.75:
- Column: Pbr = 0.01Pr; βbr = (1/φ)·8Pr/Lbr.
- Beam lateral brace at or near the compression flange: Pbr = 0.02MrCd/ho; βbr = (1/φ)·10MrCd/(Lbr·ho); Cd = 2.0 for
  the brace nearest an inflection point in double curvature, else 1.0.
- Beam-column (6.4): **add** the column and beam values; Lbr = actual unbraced length. **If the combined stress puts
  both flanges in compression, brace both flanges** (or combine lateral and torsional bracing) (6.4(d)).
- 6.3: an **inflection point is not a braced point**; in double curvature brace **both flanges** at the braced point
  nearest the inflection point (6.3.1(b)). Supports must be restrained against twist.
- 6.1: a system bracing several members is designed for the **sum** of their demands; stiffness must include the
  connections and anchorage (purlin bending, cleat and bolt slip).
- A fly brace is a diagonal from the purlin/girt to the inside flange; its lateral stiffness at the flange is roughly
  (EA/L)·cos²θ in series with the purlin's own flexibility and bolt slip — check βbr with these in series (my note,
  not DG25).

**Where braces are needed on a gable portal (my synthesis of DG25 + App. 6 for our wind-governed frame):**
- Gravity: hogging at the knees → **inside flange compressed** over the column top and the haunch → fly braces along
  the haunch and down the column inside flange; sagging near mid-span → outside flange compressed, held by purlins.
- **Net wind uplift reverses this**: the rafter inside flange is compressed over the middle of the span and the
  column/haunch outside flange near the knee. Wind-governed frames therefore usually need inside-flange braces **along
  most of the rafter and column**, not only near the knee.
- At each inflection point (it moves with the load case) both flanges must be braced at the nearest brace position.
- The knee (rafter–column joint) itself needs the inside flange braced at or very close to the joint.

**On the drawings** this means: every fly-braced purlin/girt is marked "FB" on the frame elevation at its true
position, with the side(s) braced; a fly-brace schedule (angle, cleat, bolts, design force, F angle) per Part E /
S9A; inside-flange cleats or holes shown on the member details; any braces needed on both flanges near inflection
points identified explicitly.

#### 5. Serviceability and connection notes (pp.169–170, 161, 123)

- Serviceability is judged on **first-order deflections with unreduced stiffness** against the traditional empirical
  limits; second-order service deflections only where collision with a neighbouring structure is possible or where a
  specific element is damaged above a stated limit (p.170). **DG25 gives no drift or deflection limits**; it relies on
  "traditional" ones (AISC DG3, MBMA manual, project specification). Choice of limits is the engineer's.
- Partial base fixity reduces service deflections noticeably (≈ 10 % vertical, 20 % lateral in Eroz et al.) but should
  not be counted unless modelled with a justified spring (p.189).
- Knee: full-height end plates are FR; check the panel zone by DG16 Ch.5; full-depth column stiffener at the rafter
  inside flange; rigid-panel modelling slightly unconservative (pp.123, 161, 184–188).
- Web shear in metal-building frames is usually low because sections are deep (p.161) — but the haunch deep end of a
  thin web is the exception (§7.3).

#### 6. Worked examples and numbers to check against

DG25 has **no complete frame design example**. Its examples are member-level (one tapered column/beam reused) plus
small frame illustrations. Full-frame studies are in White and Kim (2006, MBMA report: a clear-span and a modular
frame by DM and ELM) and Kim (2010) (pp.186–189) — not reproduced in DG25.

**Members of Examples 5.1 – 5.5** (Fy 55 ksi, Fu 70 ksi; web 1/8 in.; flanges PL 1/4 × 6 in. both sides):

| Example | Member and load | Result |
|---|---|---|
| 5.1 tension (pp.53–54) | web 12→18 in. over 60 in., 2 holes 11/16 in. per flange at 12 in. | yield φPn 223 kips; rupture at holes φPn **205 kips** (governs) |
| 5.2 column (pp.59–78) | L = 144 in., h 12 (bottom) → 24 in. (top), both flanges braced at 90 in.; Pr = 11.3 kips LRFD (7.5 ASD) | Pex = 3,990 kips by Eq 4.5-4 (I′ = 289 in.⁴ at 64.5 in. from the small end, h = 17.4 in.) vs 3,980 by successive approximations; Pn in-plane 168, out-of-plane lower 139, upper 158 kips → **φPn = 125 kips** (lower out-of-plane governs, ratio 0.090) |
| 5.3 beam (pp.85–103) | same member; Mr linear, 0 at bottom → 1,800 kip-in. (203 kN·m) at top LRFD; holes 11/16 in. at braces | lower length: FLB at top governs, Mn 1,690 kip-in., ratio **0.736**; upper length: LTB Mn 2,450 (0.816), **FLB at top Mn 2,090 kip-in., ratio 0.957** governs |
| 5.4 combined (pp.106–115) | 5.2 + 5.3 | H1-1b: lower **0.781**, upper **0.997** LRFD; H1.1 more liberal than H2 here |
| 5.5 shear (pp.118–123) | see §3.5 | 14.6 / 10.9 / 14.4 / 34.1 kips |

**Examples 5.6 – 5.8** (pp.123–159): same geometry but singly symmetric — outside flange 7/32 × 6 in., inside
5/16 × 6 in.; outside flange braced by an 8 in. girt at 90 in.; **no inside-flange brace**. Axial: in-plane φPn 180
(ratio 0.063), **CAT governs φPn = 110 kips (0.103)**. Flexure (Mr 1,800 kip-in. top): LTB at top Mn 2,580 (0.775),
**TFY at top Mn 2,500 kip-in. (0.800) governs**, flange rupture at girt holes Mn 1,840 (0.676). Combined H1-1b
**0.852** LRFD.

**Frame illustrations (Ch.6):** notional loads and out-of-plumb (§2.3), lean-on loads (§2.3), gable Δ ratio 1.29 vs
wrong 1.08 (§2.2).

**Software benchmarks (Appendix C)** — run these in MIDAS with the same element type and subdivision as the job model:

| Case | Member | Boundary | Key results |
|---|---|---|---|
| C-1 (p.200) | doubly symmetric, h 9.5→24.5 in., PL 1/4 × 6, tw 1/8, L 196.3 in. | pinned base, top rotation fixed, sway free; H = 0.01αPr | **PeL = 1,757 kips, Pcr = 649 kips**, Pyo 230 kips; first order Δ = 0.223H, M = 16.36H (kip-ft); at αPr/Pcr = 0.40 Δ = 0.367H, M = 24.27H |
| C-2 (pp.201–203) | singly symmetric, h 9.125→39.875 in., PL 1/2 × 6 and 3/8 × 6, tw 7/32, L 181.2 in. | as C-1 | PeL = 6,683 kips; Pcr 2,996 (curved axis) / 3,019 (straight axis) kips |
| C-3 (pp.203–204) | propped cantilever rafter, h 8.5→38.5 in., PL 1/4 × 6, tw 3/16, L 480 in., wL/αPr = 0.1 | fixed / pinned | PeL = 547 kips, Pcr = 1,078 kips, Pyo 253 kips |
| C.3.1 (pp.205–208) | Example 5.2 column, successive approximations | pinned–pinned | γeL = 530.5 at Pr = 7.5 kips → PeL ≈ 3,980 kips |
| C.3.2 (pp.208–212) | stepped tapered column, steps in plates and load | pinned–pinned | γeL = 62.8 (9 cycles) vs 64.2 by eigenvalue (2.2 %) |
| A.1 (p.190) | bf 8, tf 1/2, tw 3/16, h 18→36 in., L 360 in. | pinned | I′ = 1,690 in.⁴, PeL = 3,730 kips |

#### 7. Use on this project

Frame data (from the brief): columns 300→800 × 250 (web 8, flanges 14) over 6 m; haunch 800→350 × 250 (web 6,
flanges 12) over 5.2 m; prismatic rafter 350 × 200 × 6 × 10; slope ≈ 18°; pinned bases; SM520. The numbers below are
**my quick checks** (E = 200 000 MPa, Fy = 355 MPa, welds ignored), to be confirmed in the calc.

##### 7.1 Section classification (DG25 §1.2 and Ch.5 limits)

| Section | h/tw | bf/2tf | λpf 9.0 / λrf | Web: λpw 89 / λrw 135 | Notes |
|---|---|---|---|---|---|
| Column 300 (base) | 34 | 8.9 | compact | compact | My ≈ 371 kN·m |
| Column 800 (knee) | 96.5 | 8.9 | compact (just) | **noncompact** | My ≈ 1,232 kN·m |
| Haunch 800 (knee) | **129** | 10.4 | **noncompact** (λrf ≈ 16) | **noncompact, near slender** | My ≈ 1,034 kN·m; FLB likely governs as in Ex 5.3 |
| Haunch 350 (end) | 54 | 10.4 | noncompact | compact | flange width 250 meets rafter 200 here |
| Rafter 350 × 200 | 55 | 10.0 | noncompact | compact | My ≈ 271 kN·m |

##### 7.2 What to check in the MIDAS model

1. **Method.** Use the DM (360-16 Ch.C). For a portal frame P-δ cannot be dropped (360-16 C2.1(b)(3)), so keep the
   members subdivided or use P-δ-capable elements.
2. **Second-order per combination.** Confirm how MIDAS P-Delta builds the geometric stiffness: if a single "P-Delta
   load case" sets the axial forces and the load cases are then superposed, that is one geometric stiffness for all
   combinations. DG25 §6.2.6 needs a separate second-order solution for each combination (at least for the governing
   wind and gravity combinations).
3. **Stiffness.** Strength model with **0.8E for all members** (or MIDAS's DM stiffness option, if used); τb = 1 almost
   certainly (column αPr/Pns ≪ 0.5 — confirm). Service model with full E.
4. **Notional loads.** 0.002Yi at **each column top** in proportion to the vertical load it receives (and at canopy or
   monitor column load points). Gravity combos in **both** directions (symmetric frame). Additive to wind only if
   the **load-weighted average** Δ2nd/Δ1st > 1.7 (reduced stiffness) — compute it as DG25 Fig 6-7, not from one
   column. If the Thai erection tolerance is looser than H/500, scale up.
5. **Subdivision.** Columns 0.67 m (9 elements) and haunch ≈ 1.1 m (≈ 5 elements) are ample for in-plane analysis
   (Table 6-1 needs only 1 – 3 for pinned-base sway columns; element αPr/Peℓ is far below 0.02 — e.g. a 0.67 m
   column element has Peℓ ≈ 690 000 kN). For the **prismatic rafter**, PeL over Los = 2 × 13/cos18° = 27.3 m is
   only ≈ 350 kN (≈ 280 kN at 0.8E), so αPr/PeL may be 0.2 – 0.5 under thrust: keep **≥ 4 elements per rafter between
   columns** (Table 6-3) — any practical mesh (≈ 1 – 1.5 m) satisfies this.
6. **Tapered properties.** If MIDAS tapered sections are used, the strong-axis I must vary as for an I-section (close
   to parabolic/cubic, not linear); if stepped prismatic pieces are used, each piece needs the average properties.
   Verify either way with **benchmark C-1** (PeL 1,757 kips, Pcr 649 kips) built the same way.
7. **Do not take LTB from a 3D eigen-analysis of the stepped model** (prismatic pieces misrepresent torsion). Check
   LTB and CAT by DG25 Ch.5 (spreadsheet) using MIDAS forces.
8. **In-plane strength.** Columns: PeL with I′ (0.5L(Is/Il)^0.0732 = 2.56 m from the base, depth ≈ 513 mm) ≈
   **28 000 kN**, so α/γeL ≈ Pr/28 000 ≪ 0.10 → Pni = QPy (360-16: FyAe). Rafters: mid-span work point is ≈ 4.2 m above
   the chord (≫ 26 m/50 = 0.52 m) → Pni = QPy. In-plane buckling is not a design check; **out-of-plane buckling,
   LTB, FLB and CAT are**.
9. **Design code check.** Confirm what MIDAS's AISC 360-16 check does with tapered members (probably section-by-section
   prismatic equations with user Lb and moment-based Cb). DG25 needs: Lb **per flange** (purlin/girt spacing for the
   outside flange, fly-brace spacing for the inside flange), Cb from **flange stresses** (Eq 5.4-1/2), γe at the most
   stressed section, CAT where inside braces are wider apart. Hand-check at least: column top (knee), haunch deep
   end, haunch–rafter junction, rafter at mid-span under uplift, column under windward pressure.
10. **Base and knee.** Pinned bases as modelled (do not credit fixity for strength); knee panel zone with rigid end
    zones — check the panel (DG16 Ch.5) because DG25 warns rigid modelling is slightly unconservative.

##### 7.3 Shear and welds — quick numbers

- Haunch deep end (h/tw 129): DG25 / 360-10 unstiffened kv = 5 → Cv ≈ 0.25, Vn ≈ 260 kN; **360-16** kv = 5.34 →
  Cv1 = 60.3/129 ≈ 0.47, Vn ≈ 480 kN (Aw = d·tw = 4,800 mm²). Column top (h/tw 96.5): Cv ≈ 0.46 (old) / 0.62
  (360-16). Use 360-16 in the calc; if knee shear governs, add stiffeners (a ≤ 3hmin) or thicken the haunch web near
  the knee.
- Web-flange weld demand VQ/I ≈ **1.0 N/mm per kN of shear** at the 800 mm ends (both members): e.g. 300 kN → ≈ 300
  N/mm, against ≈ 610 N/mm (4 mm) or 760 N/mm (5 mm) for one E70/E49 fillet (φ 0.75). A **one-sided continuous
  fillet** is adequate on strength; the minimum size governs (360-16 Table J2.4 on the thinner part: 3 mm for the
  6 mm web, 5 mm for the 8 mm web — confirm). Two-sided welds only near end plates/knee and under stiffeners or
  concentrated loads (engineer to decide the extent).

##### 7.4 Brace layout to show

- Outside flanges: purlins and girts at their actual spacing are the outside-flange braces (with their own
  anchorage to roof/wall bracing — App. 6.1 sums all frames' brace forces into the purlin line).
- Inside flanges: fly braces (pairs of angles, Part E) at a spacing set by the **inside-flange LTB/CAT check** under
  both gravity (knee region) and **wind uplift** (mid-span rafter, column under suction). Start from every second
  purlin/girt and refine by calc. Always: one at or next to the knee on the column and on the rafter; one at the
  haunch–rafter junction; **both flanges braced at the brace nearest each inflection point** (all governing cases).
- Brace force per point (LRFD): Pbr = 0.02MrCd/ho + 0.01Pr; stiffness βbr = (1/0.75)(10MrCd/(Lbrho) + 8Pr/Lbr)
  including purlin bending and connection slip. Compare with the Part E schedule (rafter haunches: 90 × 90 × 8 EA,
  M20 8.8/S) — App. 6 design may justify a lighter angle, as on SRT.

##### 7.5 Drawing content for tapered members

- **Frame elevation**: grid, levels, slope, work points; member marks; splice and plate-change positions dimensioned
  along the **outside (straight) flange**; depth at each end and at each plate change, measured **perpendicular to
  the outside flange**; every purlin/girt and every FB position.
- **Member/plate schedule** (one row per plate segment): mark · segment from–to · length · depth start/end · web PL
  t · outside flange PL b × t · inside flange PL b × t · grade (SM520) · web–flange weld (size, one/two-sided,
  extent) · remarks (holes, stiffeners, splices). Plate data from the calc/MIDAS section table, never retyped.
- **Haunch–rafter transition**: flange width 250 → 200 and thickness 12 → 10 at the haunch end — either an end-plate
  splice there, or a shop CJP flange butt splice with a width/thickness transition taper; the inside flange also
  changes slope (≈ 5°) at this point, which creates a kink force (≈ 2Ff·sin(Δθ/2)) — check (J10) and provide a pair of
  web stiffeners if needed. (My observation; not in DG25.)
- **Knee**: end plate (FR), column web stiffener in line with the rafter inside flange, full depth, welded to both
  column flanges and the web; panel-zone doubler or diagonal stiffener if the DG16 check needs it.
- **Stiffeners**: knee, haunch end, under concentrated loads (canopy/monitor posts), fly-brace cleats, any shear
  stiffeners from §7.3 — each with size, weld and position.
- **Holes**: purlin, girt and fly-brace holes in the flanges, with hole size (net-area / F13.1 check at those lines).
- **Weld notes**: continuous web–flange fillet, one side unless shown; two sides over the stated lengths at end
  plates; stiffener welds; CJP butt splices with inspection category.

##### 7.6 Open questions for the engineer

1. Analysis method: DM with 0.8E confirmed? Which combinations get notional loads, and is the weighted Δ2nd/Δ1st
   ≤ 1.7 for every combination?
2. Does the MIDAS P-Delta set-up give a second-order solution per combination (DG25 §6.2.6)?
3. Member checks: will the design rely on MIDAS's code check, or on a DG25 Ch.5 spreadsheet for the tapered members
   (recommended at the critical sections listed in §7.2 item 9)?
4. Erection tolerance in the specification (H/500 or looser) → notional load coefficient.
5. Fly-brace positions: governed by uplift as well as gravity — final spacing from the inside-flange LTB/CAT check;
   brace design by App. 6 (force and stiffness) or by the office schedule (Part E)?
6. Knee panel zone and haunch deep-end shear (h/tw 129, 6 mm web): stiffeners, doubler or thicker web?
7. Haunch–rafter junction: splice type and the flange kink stiffener.
8. Web-flange welds: fabricator's process (one-sided automatic SAW or two-sided), sizes and two-sided extents.
9. Serviceability limits (drift under wind, rafter deflection, monitor and canopy limits): DG25 gives none — which
   standard (DG3, MBMA, Thai practice, client spec)? First-order, full stiffness.
10. Base fixity: pinned for strength and deflection — consistent with the anchor-rod detail?
11. Seismic: confirm no IMF/SMF requirement (DG25 notes two-sided welds at member ends for those).
12. Plate thickness > 16 mm anywhere (SM520 Fy drops to 345 MPa)?

---

# Part I. AISC Design Guide 29 - Vertical Bracing Connections


Working extract and review for the longitudinal bracing of the portal-frame building modelled in MIDAS Gen NX
(26 m span gable frames at 10 m centres, 9 bays, eave +6.0 m, tapered SM520 columns 300 -> 800 x 250, pinned
bases; CHS 165.2 x 4.5 X-bracing, CHS 190.7 x 4.5 eave/roof struts, H400x200x8/13 eave beams in some bays).
Reviewed 2026-10-04.

**Page convention.** "p.NN" means the **PDF page** of
`Design Guide 29 - Vertical Bracing Connections.pdf` (Muir and Thornton, AISC 2014; 400 pp.), in
`G:\My Drive\##Textbook\AISC Design Guide\AISC - Steel Design Guides 2016\...`. Book page = PDF page − 8
(for example, p.29 = book p.21; Appendix C starts at p.382 = book p.374).

**Basis warning.** DG29 is written against **AISC 360-10**, the 14th-edition Manual (Part 13 UFM equations
13-1 to 13-6 and 13-17) and **AISC 341-10** for the seismic chapter. Every example is worked in both LRFD and
ASD; only LRFD is quoted here. The provisions it uses carry over to **AISC 360-16** with these labels, checked in
`G:\My Drive\##Textbook\a360-16-spec-and-commentary.pdf`:
- Table D3.1 shear lag: Case 5 round HSS with a single concentric gusset, Case 6 rectangular HSS (360-16 PDF
  p.89). The values are unchanged.
- J2.4 fillet strength: Rn = Fnw·Awe (J2-4) with the directional term Fnw = 0.60FEXX(1.0 + 0.50 sin^1.5 θ) (J2-5)
  (360-16 p.181). DG29 cites the same pair, sometimes as "J2-4", sometimes as "J2-5".
- J3.10 bearing and tearout are separate equations in 360-16: bearing 2.4dtFu (J3-6a) and tearout 1.2lc·t·Fu
  (J3-6c) (p.195). DG29 uses the 2010 combined form, 1.2lc·t·Fu ≤ 2.4dtFu.
- J4.4 connecting elements in compression: Lc/r ≤ 25 gives Pn = FyAg (J4-6); otherwise Chapter E applies (p.197).
  DG29 writes KL/r.
- J4.3 block shear (J4-5) is unchanged.
- Bolt names: DG29 "A325-N/X" and "A490-X" are 360-16 Group A and Group B.
- Seismic: 341-10 F2.5b and F2.6c become 341-16 F2.5b and F2.6c. That material is not needed for this
  wind-governed building.

**Copyright.** Everything below is paraphrased. Equations are restated in my own notation, and the example
results are summarised as numbers. No text or figure is reproduced.

**Read method.** Text was pulled with PyMuPDF for all 400 pages. The method chapters (Ch.1-4, pp.9-50),
Appendices A-D (pp.355-397) and the HSS and base-plate examples were read closely. Equation-heavy and
figure-heavy pages were viewed as images: Figs 2-1, 3-12, 4-3, 4-4, 4-11 to 4-17, 4-22, 4-23, 5-32, 5-34, 6-2,
6-3, 6-4, 6-9, 6-10, C-1 to C-7, and the equation pages of Ex 5.12, 6.1a, 6.1b and Apps B and C. The other
corner examples (5.2-5.8, 5.11, A.1) were skimmed.

**Cross-reference.** Most of the HSS-end material (slotted HSS and knife plate, U for round HSS, end tees and
cap plates, round end-plate splices) is already in **Part D §1.9** (DG24 Ch.5). Here it is only cited, and the
DG29 additions are given: the brace-wall lap length, the rectangular-HSS x̄, the net-section reinforcement and
the Whitmore and block-shear treatment of a slotted HSS.

Notation (mine): P = brace force (+ tension); θ = brace angle **from the vertical** (DG29 convention);
H = P sinθ, V = P cosθ; eb = half beam depth; ec = half column depth (0 for a web connection);
α, β = ideal UFM distances to the centroids of the gusset-to-beam and gusset-to-column connections;
ᾱ, β̄ = actual distances; r = UFM radius; Hb, Vb = gusset-to-beam forces; Hc, Vc = gusset-to-column forces;
tg = gusset thickness; lw = Whitmore width; lb (or l1) = gusset buckling length; l = brace-to-gusset weld (lap)
length; D, t = CHS diameter and wall; B, H = rectangular HSS sizes; x̄ = connection eccentricity for U;
WP = work point.




#### 1. Scope, philosophy and connection configurations (Ch.1-3, pp.9-24)

**1.1 Scope (p.9).** DG29 covers:
- corner connections (brace + beam + column), orthogonal and non-orthogonal;
- centre connections (chevron or V; eccentric braces);
- brace-to-column connections at base plates;
- non-seismic and seismic design.

It does **not** design an X-brace crossing, a horizontal (roof-plane) bracing connection, or a CHS brace. All
of its HSS examples use square HSS. See §7 for how the method is carried over to those cases.

**1.2 Design philosophy: the lower bound theorem (pp.9, 25).**
- A connection is safe if the designer uses any **admissible** force field (one in equilibrium with the applied
  loads) and every limit state is satisfied for it.
- Corner gussets are statically indeterminate, so many admissible fields exist. Different methods give
  different capacities, and all of them are safe.
- Of the admissible fields, the one that gives the highest capacity is taken as closest to the true behaviour.
  On that basis the UFM is preferred (p.25).
- A force field that is **not** in equilibrium voids the theorem. An example is the KISS method used without its
  edge couples (p.25).
- The theorem needs ductility. Most limit states have some. Low-ductility elements, such as transversely loaded
  fillet welds, are given ductility by:
  - flexible supports (a gusset welded to a web), or
  - extra strength (the weld ductility factor, §3.7) (p.9).

**1.3 Frame analysis assumptions (p.11).**
- Concentric braced frames are analysed as pin-jointed trusses. The gravity axes of all members at a joint meet
  at the WP.
- Secondary (rigid-joint) moments may be ignored when the member length exceeds 10 × its depth in the plane
  of distortion (the AASHTO rule).
- For a non-concentric WP, analyse the frame as concentric and superimpose the moment from the WP offset.
- Drawings should show **member orientation** (web or flange to view). DG29 notes that computer-generated
  drawings often omit it (p.11, Fig 2-1).

**1.4 Configurations (Fig 2-1, p.12; Fig 2-5, p.15).**
- Single diagonals in each storey, in the same direction or alternating: (a) to (c).
- X-bracing across one storey: (d).
- Chevron (inverted V and V): (e).
- Bracing that jumps bays, with transfer forces at the columns: (c) and (f).

**1.5 The five connections at a corner (Fig 3-1, p.17):**
- (A) brace to gusset;
- (B) gusset to beam;
- (C) gusset to column;
- (D) beam to column;
- (E) collector or drag beam to column, wherever a transfer force exists.

**Design the brace-to-gusset connection (A) first.** It fixes the minimum gusset size. Only then are the
gusset shape and the other connections sized (p.17). This order is the same for corner and centre gussets.

**1.6 Brace-member arrangements (Ch.3, pp.17-24).**
- W braces use WTs, double angles or "claw" angles. For a brace that can be in compression, use WTs or angles,
  not flat splice plates (p.17).
- Single angles, WTs and flat bars are economical **tension-only** braces. Flat bars are lapped and field bolted.
  They are slender to erect and may vibrate (p.19).
- **HSS braces (§3.6, Fig 3-12, p.24).** The tube is **slotted and field-welded** over the gusset.
  - The slot is made **longer than the weld** so the brace can be swung into place.
  - An **erection bolt** through the tube and the gusset holds it while it is welded.
  - The weld symbol carries the note "adjust for slot gap".
  - HSS cost more per tonne than W shapes, but they buckle better and are lighter for equal compression
    strength. They are the usual choice where tension and compression strengths should be close.

**1.7 Which DG29 cases apply to our building** (my mapping; checked against the geometry, not stated by DG29):

| Our joint | Nearest DG29 case | Notes |
|---|---|---|
| Wall X-brace at the column foot, pinned base | §4.3 brace to base plate, **weak-axis (web) case**, Fig 4-23, Ex 5.12.2 | The gusset lies in the wall plane, perpendicular to the column web, welded to the web and the base plate |
| Wall X-brace at the eave (column + eave strut or eave beam) | Corner connection to a **column web** (Ex 5.5-5.8). With a CHS strut, use Special Case 2 (ΔVb = Vb) or a gusset to the column only (§4.2.4 mirror) | ec = 0 at a web, so Hc = 0. The strut is a "beam" that cannot carry the brace's vertical component |
| Roof X-brace to rafter + roof strut | Same algebra in the roof plane: the rafter is the "column", the strut is the "beam" | DG29 covers vertical bracing only. The UFM is pure statics and can be carried over |
| X crossing of two CHS | **Not covered** | See §7.3 |
| Gable-end or sloped members | §4.2.5 non-orthogonal UFM (γ) | Only if a gusset edge lies on a sloping member in the brace plane |

Frame distortion (§2.9) and the seismic items (§3.9) do not apply: the building is wind-governed with pinned
bases, and the gussets are on column webs.




#### 2. Force distribution: the Uniform Force Method and its special cases (Ch.4, pp.25-49; App A, pp.355-358)

**2.1 The four published corner methods (pp.25-32).**
- **KISS.** Brace H goes to the beam and V to the column. It is valid only **with** the edge couples. It is
  uneconomical and not recommended (pp.25-26, 32).
- **Parallel force method.** Edge forces pass through the edge centroids, and a moment M is needed at the beam
  and column. On a **column web** it puts a large normal force at mid-web and needs heavy stiffening. With M = 0
  it becomes the UFM (pp.26-27; compare Figs 4-10 and 4-12, pp.34, 36).
- **Truss analogy.** It has the same web problem. It also sends most of H to the column and most of V to the
  beam, which makes the beam-to-column joint behave like a moment connection (p.27).
- **UFM** (Thornton, after Richard 1986). It predicted six full-scale failure loads and is in the Manual since
  1992. Applied to the same connection, it gives a capacity at least as high as the other three methods
  (pp.27-29). **DG29 uses the UFM exclusively for corner connections** (p.32).

**2.2 UFM general case (Figs 4-4a and 4-4b, pp.28-29; Eq 4-1, p.32).**
- Three control points:
  - A, on the brace line;
  - B, at the beam centreline on the column face;
  - C, at the column centreline at the level of the gusset-column centroid.
- Rb passes through B, Rc through C, and both meet the brace line at A. The interfaces then carry **only shear
  and normal force, no moment**.
- Geometric constraint (Eq 4-1): α − β·tanθ = eb·tanθ − ec.
- Forces, with r = √[(α + ec)² + (β + eb)²]:

  - Hb = α·P/r
  - Vb = eb·P/r
  - Hc = ec·P/r
  - Vc = β·P/r

- Equilibrium checks: Vb + Vc = P cosθ and Hb + Hc = P sinθ.
- At the beam-to-column interface: Vb is added to the beam reaction, Hc is an axial force (plus or minus any
  transfer force), and Hb goes into the beam.
- **At a column web, ec ≈ 0, so Hc = 0.** The column web then receives only Vc (shear along the gusset weld),
  and nothing normal to the web.

**2.3 When the ideal geometry cannot be met (p.33; Eqs 4-2 to 4-4, pp.33-35).**
1. Best: lay out the gusset so that ᾱ = α and β̄ = β. There is then no moment anywhere.
2. Otherwise, give the moment to the **stiffer** interface:
   - keep β̄ = β and accept Mb = Vb(α − ᾱ) on the gusset-to-beam edge (4-2); or
   - keep ᾱ = α and accept Mc = Hc(β − β̄) on the gusset-to-column edge (4-3).
   The sign of each couple is given for a first-quadrant gusset in tension.
   - In Ex 6.1b, both edges are welded and the shorter edge (to the column) is taken as the flexible one. Its
     moment is set to zero and Mb goes to the longer beam edge (p.311).
3. If the relative stiffness is unknown, minimise ξ = ((α − ᾱ)/ᾱ)² + ((β − β̄)/β̄)² subject to Eq 4-1. With
   K = eb·tanθ − ec, K' = ᾱ(tanθ + ᾱ/β̄) and D = tan²θ + (ᾱ/β̄)²:
   - α = [K'·tanθ + K(ᾱ/β̄)²] / D;
   - β = (K' − K·tanθ) / D (4-4, p.35).

**2.4 Special Case 1: non-concentric WP (§4.2.2, Figs 4-13 and 4-14, pp.37-38).**
- The WP is moved to the gusset corner or to any point (x, y) measured from the beam-flange / column-face
  corner.
- Offset of the brace line from the gravity-axis WP: e = (eb − y)sinθ − (ec − x)cosθ, and M = P·e.
- Use the concentric UFM forces (at the true bevel) and superimpose:
  - H' = (1 − η)M / (β̄ + eb) (4-5);
  - V' = (M − H'β̄)/ᾱ (4-6).
- η is the share of M taken by the beam:
  - ultimate: η = Zbeam / (Zbeam + ΣZcol) (4-8);
  - service: η from the I/L ratios (4-9).
- **At a column web, η = 1.** All of M goes into the beam, because the web distorts (Gross 1990 tests).
- The beam is checked for ηM and the column for (1 − η)M/2, above and below the joint.
- DG29 prefers this field to the Manual's Special Case 1 field, which is admissible but disagrees with
  Richard's analyses (p.37; Ex 5.2, p.88).
- Moving the WP to the gusset corner **shrinks the gusset and the connection demand**, at the cost of member
  moments. The engineer weighs the two (p.155). A practical WP for layout is the column-web centre at the
  beam top-flange level, because the real gusset corner moves with the setback (p.156).

**2.5 Special Case 2: reduced brace V in the beam-to-column connection (§4.2.3, Fig 4-15, pp.39-40).**
- Typical case: a large brace and a column, with a "beam" that is only a light strut. This is common in outer
  walls, where computer models join all members at one node.
- A ΔVb is moved from the gusset-to-beam edge to the gusset-to-column edge:
  - column edge carries Vc + ΔVb;
  - beam edge carries Vb − ΔVb;
  - beam edge moment Mb = Vb(α − ᾱ) + ΔVb·ᾱ (4-10).
- With **ΔVb = Vb** (the Manual's Special Case 2), the beam-to-column joint carries no brace vertical, and
  Mb = Vb·α = Hb·eb (4-11).
- Hc still acts as an axial force at the beam-to-column interface.
- → This is the natural case for our eave, where the "beam" is the CHS 190.7 strut.

**2.6 Special Case 3: gusset to the beam only (§4.2.4, Fig 4-16, pp.40-41).**
- Used for shallow braces, θ > about 60°. Set β = 0, so α = eb·tanθ − ec.
- If ᾱ ≠ α, the beam edge carries Mb = V(ᾱ − α).
- The beam-to-column connection also carries the brace V and a moment **Mbc = V·ec**. Mbc is zero only at a
  column web.
- **For steep braces (θ < about 30°), the mirror case, a gusset to the column only, is set up the same way.**
- Both cases follow from statics alone (p.41).
- Example: Ex 5.4 (pp.106-125), a flat-bar gusset to the beam only. Buckling is checked with **K = 1.2** for
  sidesway of the free gusset (p.111).

**2.7 Non-orthogonal corners (§4.2.5, Fig 4-17, p.41; Ex 5.10, pp.213-244).**
- γ = the column (or beam) slope from orthogonal; positive when the beam-column angle is below 90°.
- Constraint: α − β(cosγ·tanθ − sinγ) = eb(tanθ − tanγ) − ec/cosγ.
- With r = √[(α + eb·tanγ + β·sinγ + ec/cosγ)² + (eb + β·cosγ)²]:
  - Vb = eb·P/r;
  - Hb = (α + eb·tanγ)P/r;
  - Vc = β·cosγ·P/r;
  - Hc = (β·sinγ + ec/cosγ)P/r;
  - Q = Hc − P·cosθ·tanγ, an extra beam-to-column force.
- The column-edge forces are then resolved normal and tangential to the sloping member (p.220).
- For us this applies only if a gusset edge lies on a member that slopes **in the brace plane**. The column
  taper is in the frame plane, normal to the wall bracing, so it does not make the wall bracing non-orthogonal
  (see §7.1).

**2.8 Generalised UFM (App A, pp.355-358; Ex A.1, pp.359-370).**
- Eq 4-1 is not needed to avoid interface moments. It only follows from using (0, eb) as a control point.
- The general derivation gives moment-free interfaces for **any** geometry, so the α/ᾱ distinction disappears.
- Moving part of the vertical force between the interfaces still creates a moment. Put it on the stiffer
  (welded) gusset-to-beam edge.
- For a weak-axis brace on an **extended single plate**, ec may be taken as the distance from the WP to the
  bolt-group centre. The bolt eccentricity then becomes a couple carried by Hc, which is more economical
  (p.358).

**2.9 Frame distortion (§4.2.6, pp.42-45).**
- Real joints are not pins, so the frame drift adds distortional forces.
- The beam moment MD can be estimated (Eq 4-12) and is capped by the plastic moments (4-13).
- MD gives:
  - HD = MD/(eb + β̄) (4-14);
  - VD = HD·β̄/ᾱ (4-15);
  - a gusset-corner force FD = √(HD² + VD²) (4-16).
  FD is **compressive when the brace is in tension** ("gusset pinching").
- Controls: a pin, a shear splice or an RBS in the beam.
- **At a column web, the web distorts and HD = VD = MD = 0** (Gross 1990).
- Distortional forces are normally ignored for wind and low-seismic (R ≤ 3) design, with no known problems.
  They matter only at the 2-2.5 % drifts of high-seismic design (pp.44-45, 299).
- → Ignore for our building.

**2.10 Chevron (centre) gussets (§4.1.2, Figs 4-5 to 4-7, pp.29-31; Ex 5.9).**
- The connection is statically determinate. The control interface is Section a-a, the gusset-to-beam edge.
- Forces on Section a-a:
  - N = V1 + V2;
  - V = H1 − H2;
  - M = M1 − M2, with M1 = H1·e + V1·Δ and M2 = H2·e − V2·Δ.
- The internal Section b-b (vertical, at mid-gusset) carries N', V' and M'. They are checked for gusset shear,
  for normal stress, and for free-edge buckling (§3.5).
- Do **not** cut the gusset at b-b into two separate gussets. That puts all the vertical shear through the beam
  web, which then needs doublers, and loses the tension brace's restraint of the compression side (p.30).

**2.11 Brace to column base plate (§4.3, Figs 4-22 to 4-24, pp.45-49).**
- Recommended WP: **at the top of the base plate (e = 0)**. Any e > 0 puts a shear Hc and a moment Hc·e on the
  column (p.45).
- A WP at the underside of the plate (e = −tbp) is common because the bevels can then be set out without
  knowing the plate thickness (p.46).
- If e is large, connect the gusset to the column only.
- Admissible field. β̄ is the height of the centroid of the gusset-to-column weld above the plate. The whole of
  V goes into the column edge, and H is split:
  - Hb = [H(β̄ − e) − V·ec]/β̄, along the base-plate edge;
  - Hc = (H·e + V·ec)/β̄, normal to the column face.

  The gusset is clipped at the column-plate corner. An extension plate is added if the gusset overruns the base
  plate; better, trim the gusset to avoid one.
- **Weak axis (gusset to the column web, ec = 0):** Hc = H·e/β̄ acts **normal to the web**. It is resisted by:
  - an optional top stiffener, which takes Hc/2, with Hb increased by Hc/2 at the plate; or
  - the web's yield-line capacity (Fig 4-24, Abolitz and Warner): Mn = k·mp·L, with
    mp = Fy·tw²/4 and k = 4 + 2√2 + 6(L/h) + (h/L),

  where L is the gusset depth and h the clear web depth between fillets. k is the average of the pinned-flange
  and fixed-flange values: the flanges are fixed at the base plate and free to rotate higher up. With k = 16:
  **Hc ≤ φ·4Fy·tw²·L/β̄** (4-20; φ = 0.9). For HSS columns use the fixed-flange k (p.49).
- **Weld ductility at the web (p.49).** Web flexibility rotates the gusset about its toe, point A, which can tear
  the gusset-to-base-plate fillet. Either:
  - size the two-sided fillet to **(5/8)·tg** (the Manual single-plate rule), so the gusset yields first; or
  - fit the top stiffener.
- **Exit of the forces at the base (Ex 5.12, pp.290, 296).**
  - Hb is already in the base plate.
  - The gusset-to-column V becomes **axial tension between the column and the base plate**. It must reach the
    anchor rods. With rods near the flanges, V/2 goes through each flange-to-plate weld, combined with Hc/2 as
    shear.
  - The web-to-plate weld takes the horizontal shear.
  - The DG29 force path **assumes the anchor rods are near the flanges**, to limit base-plate bending under
    uplift (p.290). → Our pinned bases probably have the rods near the web; see §7.4.
- **Two directions at one base (p.297).** Strong-axis and weak-axis bracing at the same base need not be
  combined, because wind does not act in both directions at once. Some codes require 100 % in one direction plus
  30 % in the other.




#### 3. Gusset plate design (Ex 5.1, 5.9, 5.10, 5.12, 6.1a/b; App B and C)

**3.1 Limit states, in the order DG29 checks them (Ex 5.1, pp.52-85; Ex 6.1b, pp.331-352).**

Brace and brace-to-gusset:
1. brace yield and rupture;
2. the lap and the welds or bolts;
3. block shear in the brace and the gusset;
4. bolt bearing and tearout.

Gusset:

5. Whitmore yield;
6. Whitmore buckling.

Then the UFM forces, and for each gusset edge:

7. gusset shear and normal yield along the edge;
8. edge weld (with the ductility factor) or edge bolts;
9. web local yielding and crippling of the receiving member;
10. member shear (beam web, column panel);
11. beam-to-column connection for Vb + R and Hc ± the transfer force.

**3.2 Whitmore section (AISC Manual Part 9; pp.59, 203-204, 217, 307, 334).**
- Width: lw = (connection width at the start of the joint) + 2·l·tan30°.
  - For a slotted HSS, the start width is the brace width B (or D), so lw = B + 2l·tan30° (p.203).
  - For bolts, it is the outer gauge.
- **lw may spread across the joint into an adjacent element, such as the beam web or column web.** Each part is
  used at its own thickness and Fy. For example, Ex 6.1b uses (36 ksi)(21.9 − 4.06 in)(½ in) for the gusset plus
  (50 ksi)(4.06 in)(½ in) for the web (pp.59, 335).
- If lw runs into "air" past a free edge, trim it. Ex 5.10 trims **symmetrically**, 2 in off each side
  (p.217).
- Strength: φRn = 0.90·Fy·Aw.
- **The spread angle may be anywhere from 0° to 30°** (p.311).
  - With the full 30° fitted, the plate is thinnest.
  - Smaller gussets look better and clash less with services, but they are thicker. They can also force CJP
    edge welds, a field weld and web doublers.

**3.3 Block shear in the gusset under a slotted HSS (pp.203, 218, 332).**
- The failure path runs along the two weld lines (shear, Agv = Anv = 2·tg·l) and across the brace width
  (tension, Ant = tg·B).
- Ubs = 1. Rn = min(0.6FuAnv, 0.6FyAgv) + Ubs·Fu·Ant.

**3.4 Gusset buckling: the line-of-action method, LOAM (App C.1, Table C-1, Figs C-1 to C-4, pp.382-384).**
- Thornton's "pseudo-column" (1984): a strip of the Whitmore width, of length lb, in compression along the
  brace line.
  - lb = l1, from the centre of the Whitmore section to the gusset edge along the brace line; or
  - lb = lavg = (l1 + l2 + l3)/3.
  - The strip is checked to J4.4 / Chapter E with r = tg/√12.
- **K history:**
  - 0.65 in Thornton's original method;
  - 0.50 from the Gross (1990) tests, used in the Manual from 1992 to 2005 and in Ex 5.1;
  - now Dowswell's (2006) values (Table C-1), which DG29 uses in its later examples.

| Gusset configuration (Fig C-2) | K | Buckling length |
|---|---|---|
| Compact corner | - (yield governs; buckling not a limit state) | - |
| Non-compact corner | 1.0 | lavg |
| Extended corner (edges extended beyond the brace end) | 0.6 | l1 |
| Single brace (gusset attached on one edge only) | 0.7 | l1 |
| Chevron | 0.65 | l1 |

- **Compactness (Fig C-4).** tβ = 1.5·√(Fy·c³/(E·l1)), where c is the distance from the brace end (the corner
  of the HSS at the Whitmore line) to the nearest supported gusset edge. The gusset is compact if tg ≥ tβ.
  - Ex 6.1a: tβ = 0.49 in < 1 in (p.307).
  - Ex 6.1b: tβ = 0.06 in < ½ in (p.335).
- DG29 still runs the J4.4 check for completeness.
- **Free gussets.** Where the gusset can sway out of plane (a gusset on one edge only, a flat bar, or a chevron
  with both braces in compression), use **K = 1.2** (Commentary Table C-A-7.1) (pp.111, 189, 211).
- Lc/r ≤ 25 means yield governs (J4-6). Examples: Ex 5.1 KL/r = 16.9; Ex 5.9 KL/r = 24.0.

**3.5 Free-edge buckling (App C.2 to C.5, pp.382-390).**
- AASHTO (bridges, high-cycle fatigue): unstiffened free edge a_max = 2.06·√(E/Fy)·t (C-1). This comes from
  elastic plate buckling with k ≈ 0.5 at a/b = 3, and can be unconservative for a/b < 3.
- Astaneh-Asl (low-cycle, seismic): (a/t)max = 0.75·√(E/Fy) (C-5). It was in the 1st-edition Seismic Design
  Manual and was **dropped** in the 2nd. The 341-10 Commentary F2.6c found that edge stiffeners give no benefit.
- **The free-edge check never replaces the LOAM check** (p.387).
- **If edge stiffeners are used, never weld them to the beam or column.** That destroys the UFM force field and
  invites local fracture. A thicker plate is usually cheaper (p.387).
- **Admissible force maintenance method, AFMM (C.4, pp.388-389).** Check that a gusset edge can carry the
  compression the admissible field puts on it:
  - Fcr = Q·Fy (C-6), with Q = 1 for λ ≤ 0.7; Q = 1.34 − 0.486λ for 0.7 < λ ≤ 1.41; Q = 1.3/λ² above that;
  - λ = (b/t)·√Fy / [5·√(475 + 1120/(a/b)²)] (C-7, Fy in ksi). This is the Manual's double-coped-beam
    formula.
- The authors have **never seen the AFMM govern a corner gusset**. LOAM governs compression and block shear
  governs tension. It can govern the long free edge of a **chevron** gusset when both braces act in the same
  direction (Ex 5.9) (p.389).

**3.6 Gusset edge stresses (pp.204-205, 287-288, 339).**
- On each welded edge, treat the plate as a section of length L:
  - fv = V/(tg·L), limited to φ0.6Fy with φ = 1.0;
  - fn = N/(tg·L) + M/(tg·L²/4), limited to φFy with φ = 0.9.

  The plastic modulus tg·L²/4 is used.

**3.7 Gusset-to-member welds and the ductility factor (Manual Part 13, Hewitt and Thornton 2004; pp.65-66,
205-207, 322-324, 340; App B pp.379-381).**
- Per unit length of a two-sided fillet:
  - fa = N/(2L);
  - fb = 2M/L² (plastic, per weld line);
  - fv = V/(2L).
- Combine them:
  - f_peak = √[(fa + fb)² + fv²];
  - f_avg = ½{√[(fa − fb)² + fv²] + √[(fa + fb)² + fv²]}.
- **Design the weld for max(f_peak, 1.25·f_avg).** The 1.25 is the "weld ductility factor". It is really an
  overstrength allowance that lets the edge force redistribute before a fillet tears (p.65).
  - Simplified form: apply 1.25 to the resultant (Ex 5.12, p.288) or to the peak (p.180). Both are
    conservative.
  - The directional increase (1 + 0.5 sin^1.5 θ) may be used, with θ = atan(fn/fv).
- **App B.** Taking the directional increase at the side where N and M add, and using that size along the whole
  edge, overstresses the far end by at most **3.4 %**. DG29 accepts this.
- **Where DG29 leaves the 1.25 out:**
  - gusset welded to a flexible end plate (pp.70, 98);
  - welds carrying shear only (p.163);
  - a tab with slip-critical or bolted redistribution on its other side (p.259);
  - gusset to a **column web**, where web flexibility redistributes (Ex 5.12.2, p.294);
  - a uniform, statically determinate weld stress, such as a flat bar (p.192).
- At the weak-axis base, the **(5/8)·tg** rule replaces the 1.25 (§2.11).
- **The "1.4" factor:** I found no 1.4 ductility factor anywhere in DG29. The DG uses 1.25 only. A 1.4 value
  appears in older practice, so do not apply it for DG29-based work unless the engineer asks.
- **Gusset corner clip.** A clip (¾ in × ¾ in typical) **separates the gusset-to-beam and gusset-to-column
  welds. No weld passes through the clip** (p.86).

**3.8 Receiving members (pp.66-67, 212-213, 289, 295, 341-347).**
- **Web local yielding.**
  - Force more than d from the member end: J10-2, Rn = Fy·tw(5k + lb).
  - Force within d of the end: J10-3, Rn = Fy·tw(2.5k + lb).
- **Web crippling.**
  - Force at least d/2 from the end: J10-4.
  - Closer to the end: J10-5.
- The concentrated force is the equivalent normal force from §3.7, N + 4M/L.
- Beam web shear over the gusset length. "Any length up to about half the span" may be used to deliver it
  (pp.212, 342).
- Column web or panel shear at the beam-flange level.
- At the weak-axis base: the web yield-line check (§2.11).

**3.9 Seismic gusset rules, NOT required for this building (Ch.6, pp.299-328).**
- SCBF (R = 6) connections are designed for the brace's **expected** strength (Ry·Fy·Ag in tension;
  1.14·Fcre·Ag in compression), not the analysis force. They need a **2t linear clearance** ("bending zone",
  Fig 6-2, p.303) so the gusset can hinge clear of the beam and column.
  - Pull-off dimension = L + 2t, where L² = [eb·tanθ + a·sinθ·tanθ]² + (eb + a·sinθ)² and
    a = d/2 + l'·tan30°, l' = l + 2t (pp.303, 311).
- The **elliptical (8t) clearance** alternative is **not** in DG29. It is a later SCBF option and is not needed
  here.
- Seismic detailing raised the steel cost by **30-40 %** for the same loads in Ex 6.1a vs 6.1b (p.353).
- **R = 3 ("not specifically detailed") and wind design: the connection is designed for the same force as the
  brace**, and no hinge zone is needed (p.329). → This is our case.




#### 4. HSS brace-to-gusset connections (§3.6; Ex 5.9, 5.10, 6.1a, 6.1b)

DG24 background (U, slot gap, no weld return at the slot end, gusset wider than the HSS, end tees and cap
plates, bolted end plates) is in **Part D §1.9**. DG29 adds the following.

**4.1 Arrangement (Fig 3-12, p.24; Fig 6-3, p.309).**
- The gusset (knife) is **shop-welded to the column or beam**. The HSS is **slotted and field-welded** with four
  longitudinal fillets, two each side of the gusset.
- Slot length = lap length l **+ erection clearance x**. The brace is slid on, held by an erection bolt, then
  welded.
- **Slot width = tg + 1/16 in (≈ 1.6-2 mm) each side** (pp.202, 215, 307, 331). Ex 5.10 uses tg + 1/8 in
  overall.
- **Gap and weld size (p.201, AWS D1.1 cl.5.22.1).** The fabricator adds the root gap to the leg:
  - a ¼ in called-out fillet becomes 5/16 in (one pass);
  - a 5/16 in called-out fillet becomes 3/8 in (multi-pass).

  Calling out the smallest adequate leg saves passes. Keep the slot tight.

**4.2 Lap (weld) length: the brace-wall shear check (pp.201, 216, 304, 332).**
- The four weld lines tear four shear planes in the HSS wall: Pu ≤ φ·0.6·F·t·(4l).
- DG29 uses two versions:
  - **shear rupture**, F = Fu, φ = 0.75: Ex 5.9 gives l ≥ 5.95 in; Ex 5.10 gives l ≥ 10.8 in;
  - **shear yielding**, F = Fy, φ = 1.00: Ex 6.1a and 6.1b. Ex 6.1b gives l ≥ 5.84 in.
- → Use the larger of the two (both are J4.2 limit states).
- Then size the weld: Pu ≤ 4·(1.392·D·l) [kip, sixteenths, in]. In SI: 4·φ·0.6·FEXX·0.707·w·l.
  - No directional increase (the welds are longitudinal).
  - Apply the J2.2b length reduction if l > 100w. Ex 5.10: 19 in < 31.3 in, so there is no reduction
    (p.216).
- The weld cannot be thicker than the wall allows. In 360-16 J2.2b, the maximum fillet along the edge of
  material less than ¼ in (6 mm) thick is that thickness. → This matters for our t = 4.5 mm wall; see §7.

**4.3 Net section and shear lag (pp.202, 215-217, 307-310, 331-332).**
- An = Ag − 2·t·(slot width). Use the **design wall** (A500: 0.93t, so tdes = 0.465 in for a ½ in wall).
- Then U from Table D3.1:
  - **Rectangular HSS, single concentric gusset (Case 6), l ≥ H:** U = 1 − x̄/l with
    x̄ = (B² + 2BH)/[4(B + H)]. Square 8 in gives x̄ = 3.00 in; square 10 in gives x̄ = 3.75 in.
  - **Round HSS (Case 5):** U = 1.0 if l ≥ 1.3D; U = 1 − x̄/l with x̄ = D/π if D ≤ l < 1.3D; nothing is given
    for l < D (Part D §1.9).
- Rupture: φRn = 0.75·Fu·An·U.
- Ae is often the governing brace check, so choose l with U in mind, not only the weld.
- **Net-section reinforcement (Ex 6.1a, pp.308-310, Figs 6-3 and 6-4).**
  - Weld plates of area Ar to the two HSS faces that are **not** slotted, centred on the slot end.
  - x̄ becomes (2BHt + B²t + 2Ar·B)/[4(Bt + Ht + Ar)].
  - An = An(HSS) + 2Ar.
  - Each plate must be attached over a length **a on each side of the net section**. With longitudinal and
    transverse fillets (J2-10b: 0.85 longitudinal, 1.5 transverse), a = 12 in with ½ in fillets for Ar = 5 in²
    (Ry·Fy·Ar = 275 kips).
  - Reinforcement is mandatory in SCBF, where Ae ≥ Ag is required. In R = 3 or wind design it is needed only
    when φFuAe < Pu. Ex 6.1b: no plates needed (p.332).

**4.4 End caps and capped-end tabs.** DG29 does not treat end caps, tees or cap plates. All of its HSS braces
are slotted. See Part D §1.9 (DG24): cap-plate dispersion 2.5:1 (5tp + N); an end tee in compression as an
eccentric column with K = 1.2 and e = (t_stem + t_gusset)/2.

**4.5 Bolted alternatives.**
- DG29's bolted brace connections are all W and angle braces: Ex 5.1 (double angles, 2 × 7 bolts) and Ex 5.12
  (W12 with four angles). The checks carry straight over to a knife-plate (tab) end on a CHS bolted to a
  gusset:
  - bolt shear, single or double;
  - bearing and tearout, end and interior bolts summed separately (p.58);
  - block shear in the tab and the gusset;
  - Whitmore from the outer gauge.
- DG29 shows a **lapped single-plate bolted joint only for tension-only flat bars**. For compression, use the
  eccentric-stem check of Part D §1.9.
- **Do not mix bolt grades of the same diameter in one connection** (p.52).




#### 5. Detailing rules and good practice for drawings (pp.11, 24, 45-46, 60, 86, 155-156, 302-311, 383-397)

**Geometry and set-out**
1. Show the **WP** at every bracing joint, and the **brace bevel** (rise/run, in mm per 1000 or as the 12-on-n
   triangle). DG29 states bevels to the WP as 12 on n.
   - Gravity-axis WP: no member moments.
   - Gusset-corner WP: a smaller gusset, but members carry P·e (§2.4).
   - The WP is chosen **before** the connection is designed, so use a known point, not the as-built gusset
     corner, which moves with the setback (p.156).
2. **At bases, put the WP on the top of the base plate**, or on its underside if bevels must be fixed before
   the plate thickness is known (§2.11).
3. Draw the **brace centreline (line of action)** and keep it through the gusset. The HSS slot, the weld group
   and the Whitmore section are all symmetric about it.
4. **Gusset dimensions** follow from ᾱ and β̄: the edge length on each member is 2ᾱ (or 2β̄) less the clip and
   any end-plate thickness.
   - Ex 5.1: lh = 2(17.5) − 1 − ¾ = 32.3 in (p.60).
   - Square off the gusset where it helps the bolts. Trim (shape) excess corners, as shown by the broken lines
     in Ex 5.1.
5. **Corner clip** where the gusset meets the beam-column re-entrant corner. No weld runs through it (p.86).
   Base-plate gussets also get a clip (¾ × ¾ in in Ex 5.12).
6. **Brace pull-off and cut length.** The fabricator sets the cut length from the pull-off dimension (WP to the
   brace end) plus the **erection clearance x** at the slot (pp.302, 310).

**Arrange the connection so the assumed load path happens (p.86)**
7. Do not add welds the design did not assume. Ex 5.1 warns against welding the beam flanges to the end plate
   "because it looks better": that concentrates load in the bolts near the flanges.
8. Gusset edge stiffeners, if used, must not touch the beam or column (§3.5).

**What the design drawings must carry (App D, pp.391-397)**
9. Under the Code of Standard Practice, when the fabricator designs the connections, the design drawings must
   give loads **sufficient** to complete them: shears, moments, axial forces and **transfer forces**.
10. **Transfer force** = a force passed between members through the connection that cannot be found from the
    maximum member end forces. Assuming all the maxima act together gave transfer forces about **8 × too
    large** in the DG29 example (p.391).
11. Two acceptable presentations:
    - **(a) a matrix of statically consistent load cases** at each joint: the cases giving the maximum tension
      and compression in each member and the maximum transfer force, with all member forces for each case, at
      most 2(n + 1) cases. Equilibrium is guaranteed and it gives the most economical connections, but it is
      a large volume of data;
    - **(b) maximum tension and compression per member plus a stated transfer force.** This is the common
      method. It is simpler and invites checking, but the fabricator loses the load-path information.
12. A fabricator given forces that are not in equilibrium must guess: tension in one brace and compression in
    the other is the usual guess, but not always correct. DG29 shows a chevron supporting a column where three
    plausible guesses give three different critical cases (pp.394-395).
13. **Nodal loads in the analysis model** (wind applied directly at a node) hide a transfer that some real
    member must carry. Say on the drawings how the load reaches the braced bay (p.396).

**Design drawings vs shop drawings (DG29 practice, inferred from the examples and App D)**

| Design (EOR) drawings | Shop / connection drawings |
|---|---|
| Bracing elevations with member orientation, WP, bevel | Gusset outline, clips, trims, slot length, erection clearance, cut length (pull-off) |
| Member sizes and grades; connection type (slotted HSS, field-welded) | Weld sizes allowing for the slot gap; bolt layout, edge distances |
| Brace design forces (tension and compression), transfer forces or consistent load cases | Final gusset thickness and plate grades if delegated |
| Required gusset thickness, edge welds, slot lap, where the EOR designs the connection (our case) | Erection bolt, fit-up |

Our office sets designed by the EOR show both columns: the connection is fully designed by us, not delegated.




#### 6. Worked examples relevant to our case (inputs -> results)

Units as in DG29 (LRFD), with SI in brackets. 1 kip = 4.448 kN; 1 in = 25.4 mm; 1 ksi = 6.895 MPa.

**6.1 Ex 6.1b: slotted square HSS to a corner gusset, R = 3 (pp.329-354). The closest analogue to our wind
bracing.**
- **Inputs:**
  - brace HSS8×8×½ (A500 Gr B, Fy 46 ksi), tdes = 0.465 in;
  - 24 ft WP-to-WP;
  - Pu = ±300 kips [1335 kN]. This equals the brace buckling capacity, so the connection is designed for the
    brace force;
  - beam W16×100, column W14×283 (flange);
  - gusset A36;
  - 1 in A490-X bolts; E70.
- **Brace:**
  - φPn (compression) = 306 kips;
  - tension yield 559 kips;
  - slot 1/16 in each side of a ½ in gusset, An = 12.9 in²;
  - x̄ = 3.00 in, l = 12 in, U = 0.75, Ae = 9.68 in² [6245 mm²];
  - φFuAe = 421 kips > 300, so **no reinforcement**.
- **Lap:** wall shear yield gives l ≥ 5.84 in. The weld needs 4.49 sixteenths over 12 in, so
  **5/16 in [8 mm] × 12 in [305 mm], four lines**.
- **Gusset ½ in [12.7 mm]:**
  - Whitmore lw = 21.9 in [556 mm], with 4.06 in in the beam web, φRn = 380 kips;
  - **tβ = 0.060 in, compact**;
  - LOAM check anyway: K = 0.5, lb = 10.375 in, KL/r = 35.9, φFcr = 30.3 ksi, φPn = 332 kips.
- **UFM:**
  - eb = 8.50, ec = 8.35, tanθ = 12/8 (θ = 56.3°);
  - β = β̄ = 9.75 in (bolted single plate to the column); α = 19.0 in; ᾱ = 13.3 in; r = 32.9 in;
  - Vuc = 88.9, Vub = 77.5, Huc = 76.2, Hub = 173 kips;
  - **Mub = Vub(α − ᾱ) = 442 kip-in**, on the stiffer welded beam edge.
- **Gusset-to-beam weld (L = 25 in):**
  - fa = 1.55, fb = 1.41, fv = 3.46 kip/in;
  - f_peak = 4.55, f_avg = 4.01, 1.25·f_avg = 5.03 kip/in, which governs;
  - θ = 40.5°, so D = 2.86;
  - **3/16 in both sides**.
  - Edge stresses: fn = 11.9 ksi, fv = 13.9 ksi.
- **Gusset-to-column:** ¾ in A36 single plate, bolted, designed as an extended Part 10 plate.
  - Edge bolts were short of bearing, so the plate was thickened rather than reducing the bolt strength
    (pp.343-344).
- **Result (Fig 6-9, p.330):** a ½ in gusset, 25 in long on the beam; 12 in lap; 5/16 in brace welds; 3/16 in
  gusset-beam welds; ¾ in plates.

**6.2 Ex 6.1a, for contrast: the same joint as an SCBF, R = 6 (pp.300-328).**
- Brace upsized to **HSS8×8×5/8** for b/t, with Ry = 1.4.
- Lap 19 in; 1 in gusset.
- Whitmore 29.9 in; tβ = 0.49 in, compact; extended corner, K = 0.6, lb = 27.7 in, KL/r = 57.6.
- Ae = 12.7 in² < Ag = 16.4 in², so **4 × 1¼ in A572-50 reinforcing plates** are added; Ae then = 20.7 in².
- 2t hinge zone sets the gusset size.
- **About 30-40 % more steel cost.**
- → Shows what we avoid by staying with wind / R ≤ 3 detailing.

**6.3 Ex 5.9: chevron, two HSS8×8×½ to a W27×114 beam (pp.197-213).**
- **Inputs:** Pu = ±289 kips [1286 kN] each, at 45°; WP on the beam axis, e = 13.65 in; gusset L = 64 in,
  h = 18 in.
- **Brace connection:**
  - wall shear rupture gives l ≥ 5.95 in; weld 10.4 in needed, **5/16 in × 12 in**;
  - U = 0.750, Ae = 9.53 in², φRn = 415 kips;
  - gusset ¾ in Gr 50: block shear 698 kips; Whitmore 21.9 in (2 in in the beam web), Aw = 16.1 in²,
    φRn = 725 kips;
  - **K = 0.65 (chevron), L = 8 in, KL/r = 24, so yield governs.**
- **Section a-a:** V = 408 kips, N = 0, M = 5560 kip-in [628 kN·m]. Weld 3.07 sixteenths (Table 8-4) or 2.98
  (App B method), so **¼ in both sides** (the minimum).
- **Section b-b:** V' = −30.3 kips.
- **Both-compression check:**
  - AFMM free edge with a ¾ in plate: 37.3 > 30.2 ksi, n.g. A 7/8 in plate passes. So does ¾ in, if M' is
    treated as a free vector (29.9 < 36.5 ksi);
  - Whitmore buckling with K = 1.2, KL/r = 31.4, φPn = 675 kips;
  - gusset sidesway φRn = 2010 kips. This assumes the beam bottom flange is braced.
- Beam: web local yielding 2040 kips; crippling 1310 kips; web shear yielding over the gusset length 1090 kips;
  transverse web shear at Section b-b 467 kips > 174 kips.

**6.4 Ex 5.10: non-orthogonal, HSS10×10×½ to a column web (pp.213-244).**
- **Inputs:** Pu = ±525 kips [2335 kN]; beam W18×50; column W14×342 (web, ec = 0); γ = 9.46°, θ = 41.9°.
- **Brace connection:**
  - wall shear rupture gives l ≥ 10.8 in; **5/16 in × 19 in, four lines**;
  - x̄ = 3.75 in, U = 0.803, An = 16.5 in², Ae = 13.2 in², φRn = 574 kips;
  - gusset 5/8 in A36: Whitmore 31.9 in, trimmed symmetrically to 27.9 in (4 in in the beam web),
    Aw = 16.4 in², **φRn = 531 kips vs 525 kips (governs)**; block shear 658 kips; compact, so no buckling.
- **UFM:**
  - eb = 9.0 in, β = 13.5 in, α = 16.3 in, r = 30.0 in;
  - Vub = 158, Vuc = 233, Hub = 312, Huc = 38.7 kips; Q = −26.6 kips;
  - resolved on the column: N ≈ 0, T = 236 kips;
  - bolts through double angles on the web.

**6.5 Ex 5.12.1: gusset to a base plate, strong axis (pp.276-291).**
- **Inputs:** brace W12×65 with 4L4×4×½ and 7/8 in A325-N bolts; Pu = ±180 kips [801 kN] (H = 109, V = 143);
  column W21×83 (flange); WP **e = 6 in above the base plate**.
- **Gusset PL 5/8 × 14½ × 36 in (A36):**
  - Whitmore 11.9 in, φRn = 241 kips;
  - extended corner, K = 0.6, lb = 8.32 in, φPn = 231 kips;
  - block shear 261 kips.
- **Forces:** β̄ = 18.375 in, ec = 10.7 in.
  - **Hb = −9.86 kips** (small, reversed);
  - **Hc = 119 kips**;
  - Vc = 143 kips.
- **Welds:**
  - gusset to column flange, R = 186 kips at 39.8°, with the 1.25 on the resultant: 1.88 sixteenths, so
    ¼ in;
  - gusset to base plate: ¼ in minimum.
- **Column to base plate:** shear goes to the web welds (11 in × ¼ in each side); the axial tension goes to the
  flange welds (5/16 in). Base plate 1¾ × 13½ × 30 in.
- Web local yielding and crippling were checked at β̄ (J10-3, J10-4).

**6.6 Ex 5.12.2: gusset to a base plate, weak axis (column web) (pp.292-298). The template for our column
foot.**
- **Inputs:** same brace, bevel 12/10⅛; H = 116, V = 138 kips; column web tw = 0.515 in; **ec = 0**;
  e = 6 in; gusset PL 5/8 × 16½ × 25 in; β̄ = 12.875 in.
- Gusset buckling: K = 0.6, lb = 14 in.
- **Forces:** Hb = H(β̄ − e)/β̄ = **61.9 kips** into the base plate; Hc = H·e/β̄ = **54.1 kips normal to the
  web**; V = 138 kips along the web.
- **Web yield line:** φ·4Fy·tw²·L/β̄ = 4(0.9)(50)(0.515²)(25)/12.875 = **92.7 kips > 54.1 kips, so no
  stiffener**.
- **Welds:**
  - gusset to web: ¼ in minimum, **no 1.25 factor** (the web is flexible);
  - gusset to base plate: 3.87 sixteenths for strength, but the **ductility minimum (5/8)(5/8 in)·16 =
    6.25 sixteenths, so 7/16 in**. A top stiffener would avoid this.
- **Column to base plate:** V/2 = 69.0 kips axial and Huc/2 = 27.1 kips shear per flange, R = 74.1 kips at 68.6°,
  so **5/16 in × 4 in outside plus 2 × 2 in inside each flange**. The web weld is nominal.
- **Note:** with e = 0 (WP on the plate), Hc = 0. All of H then goes to the plate, and both the web check and the
  large weld disappear.

**6.7 Ex 5.1: UFM demonstration only (pp.51-85).** 2L8×6×1 brace, 840 kips, W21×83 beam to a W14×90 flange.
- β̄ = 12 in was chosen, giving α = (10.7 + 12)(1.08) − 7 = 17.5 in; r = 33.4 in; Vc = 302, Vb = 269 kips.
- Whitmore 23.8 in, 4.70 in of it in the beam web; K = 0.5, L = 9.76 in, KL/r = 16.9.
- The gusset-to-end-plate weld needs no 1.25 factor, because the end plate is flexible.




#### 7. Use on this project

**7.1 Brace connection types to use** (my proposal, for the engineer's decision; tie-in with the MIDAS model)

| Mark | Joint | Proposed detail | DG29 basis |
|---|---|---|---|
| BC1 | CHS 165.2 wall brace at the column foot | **Gusset in the wall plane, shop-welded to the column web and the base plate; CHS slotted and field-welded (knife-plate type).** WP on the column centreline at the top of the base plate (e = 0) | §4.3 weak axis, Ex 5.12.2 |
| BC2 | CHS wall brace at the eave, with a CHS 190.7 strut or H400 eave beam | Gusset welded to the column web only, as in Special Case 2 with ΔVb = Vb or "gusset to column only". The strut connects by its own end plate or knife plate to the column. The H400 eave beam may take part of Hb through a gusset edge if the beam is designed for it | §4.2.3, §4.2.4, column-web examples |
| BC3 | X crossing of two CHS 165.2 | Not in DG29. Options: (a) one brace continuous, the other cut and joined through a plate passing through a slot in the continuous tube; (b) both braces lapped on a single centre plate (both slotted); (c) no connection (the tension diagonal only, no mid-length restraint) | §7.3 |
| BC4 | Roof brace to rafter (with strut) | Gusset in the roof plane, welded to the rafter web below the top flange (purlin clearance); slotted CHS. UFM in the roof plane with the rafter as "column" and the strut as "beam" | UFM by analogy |
| BC5 | Strut CHS 190.7 to column or rafter | Slotted CHS on a knife plate, or a capped end with a bolted tab | Part D §1.9 |

- **Why the slotted, field-welded tube (knife plate) for BC1, BC2 and BC4:**
  - it is the only HSS brace detail DG29 develops;
  - it is concentric, so there is no stem eccentricity;
  - with l ≥ 1.3D, U = 1.0.
- **Keep a bolted alternative for erection** (shop-welded tab on the tube, field-bolted to the gusset). It is
  checked as a lapped plate in compression (Part D §1.9). Raise it with the engineer if site welding is
  unwanted.

**7.2 Geometry facts to settle before calculating**
- **Brace angle.** A diagonal across a full 10 m bay from the base to the 6 m eave has length 11.66 m and
  **θ = 59.0° from the vertical**, so H = 0.857P and V = 0.515P. That is at DG29's "shallow" limit (about 60°).
  If the wall bracing is split into two tiers, θ changes. Take it from the model.
- **Brace plane vs the tapered column.** The wall-brace plane is vertical, at a fixed distance from the outer
  flange. The column centroid moves from about 150 mm (base, 300 deep) to about 400 mm (eave, 800 deep) from
  the outer face. **A single brace plane cannot pass through the column centroid at both ends.**
  - Choose the plane:
    - at the base centroid, so BC1 is concentric and BC2 is eccentric by about 250 mm; or
    - at a constant offset, eccentric at both ends.
  - The eccentricity times V gives an in-plane moment on the portal column. The eccentricity times H gives a
    torsion on the column.
  - DG29 does not cover this out-of-plane offset (its Special Case 1 is in-plane). Model the gusset offset in
    MIDAS or check it by hand.
- **ec = 0 at web gussets.** With the WP on the column centreline in the brace plane, Hc = 0 at the eave (UFM)
  and at the base if e = 0. Nothing then acts normal to the thin tapered web. This is the main reason to use
  web gussets and to place the WP as recommended.

**7.3 X crossing (BC3) - outside DG29**
- DG29 has no crossing detail. Decide first whether the crossing **must restrain the compression diagonal**
  (L/r of CHS 165.2 at 11.66 m ≈ 205 full length, ≈ 103 at half length, with r ≈ 56.8 mm).
- If it must, the crossing must transfer the restraint force, and its design rule must come from another source
  (AISC 360-16 Appendix 6 brace stiffness and strength, or the tension-compression X-brace literature). This is
  an engineering decision.
- If the bracing is designed **tension-only**, a non-structural crossing (a spacer or a simple clamp, with a
  drain and vent if the tube is cut) is enough.
- The 3D braces (wall to roof) need their own crossing geometry. Raise this with the engineer.

**7.4 Calculation steps to implement (Python, job module `calc_brace_conn.py`; data from the MIDAS export and
the member catalogue only)**
1. **Inputs per joint:**
   - Pu tension and Pu compression, the transfer force, and consistent load cases (App D);
   - θ, eb, ec, e (WP);
   - CHS D, t (design t, per the decision on 0.93t, see Part D §1.1), Fy, Fu;
   - gusset grade, tg;
   - FEXX (E70 / E49);
   - column tw and the clear web depth h at the gusset level (taper);
   - base plate tbp and the anchor-rod layout.
2. **Brace end, slotted CHS:**
   1. `slot_width = tg + 2*gap` (gap 2 mm);
   2. `An = Ag - 2*t*slot_width`;
   3. lap length from `max(Pu/(phi*0.6*Fu*4*t) [phi 0.75], Pu/(1.0*0.6*Fy*4*t))`;
   4. weld: `4*phi*0.6*FEXX*0.707*w*l >= Pu`, with w ≤ t (J2.2b, t < 6 mm), plus the slot-gap increase on the
      drawing, and the l/w > 100 reduction;
   5. `U` round HSS (l ≥ 1.3D → 1.0; D ≤ l < 1.3D → 1 − (D/π)/l; l < D not permitted);
   6. `phi*Fu*An*U >= Pu` and `0.9*Fy*Ag >= Pu`. If this fails, lengthen l before adding plates.
   - Illustration (not a design value): CHS 165.2 × 4.5 (nominal t), Ag = 2272 mm², x̄ = D/π = 52.6 mm,
     1.3D = 215 mm. A 12 mm gusset with 2 mm gaps (slot 16 mm) gives An = 2128 mm². For Fu = 400 MPa, the
     wall-rupture capacity is 0.75·0.6·400·4.5·4 = 3.24 kN per mm of lap.
3. **Gusset (brace-to-gusset):**
   1. block shear: 2 weld lines in shear plus width D in tension;
   2. `lw = D + 2*l*tan(30°)`, trimmed symmetrically to the gusset or spread into the web at its own t and Fy;
      `phi*Fy*Aw`;
   3. `t_beta = 1.5*sqrt(Fy*c**3/(E*l1))`. If tg ≥ tβ the gusset is compact. Otherwise use the LOAM with K from
      Table C-1 (extended 0.6, single-edge 0.7, sway 1.2) and J4.4 / Chapter E with r = tg/√12.
4. **Interface forces:**
   - `ufm(P, theta, eb, ec, alpha_bar, beta_bar, case)` returns Hb, Vb, Hc, Vc and the edge moments;
   - cases: general; moment on the stiffer edge (4-2 / 4-3); Special Case 2 (ΔVb); Special Case 3 /
     column-only; the non-orthogonal γ form; the base-plate form (§2.11);
   - **assert ΣV = P cosθ and ΣH = P sinθ** (the admissibility check, as DG29 does in every example).
5. **Gusset edges:**
   - fv and fn on tg·L with Z = tg·L²/4;
   - weld: `f_peak`, `f_avg`, `max(f_peak, 1.25*f_avg)` (omit the 1.25 for a web or flexible support, as in
     §3.7), with the directional factor 1 + 0.5 sin^1.5 θ;
   - minimum fillet per J2.4;
   - at the web-to-base-plate toe, the ductility weld w ≥ (5/8)·tg, two-sided.
6. **Column web:**
   - yield line Hc ≤ φ·4Fy·tw²·L/β̄ (L = gusset depth). If it fails, add a top stiffener or set e = 0;
   - web local yielding and crippling for the edge normal force;
   - web shear along the gusset for V.
7. **Base:**
   - V (uplift when the brace pulls) from the column to the anchor rods;
   - Hb to the anchor rods in shear, or to a shear lug;
   - check the base plate in bending for the uplift with the **actual rod positions**;
   - check the rods for tension + shear, and the concrete breakout (ACI 318 Ch.17);
   - add the frame's own pinned-base reactions from the same load combination.
8. **Report** every check in `!!`-style pass/fail lines. **No retyped numbers**: the drawing pulls tg, w, l,
   slot length and the gusset outline from the calc output.

**7.5 Drawing content (per brace connection detail)**
- Bracing elevations (walls, roof):
  - WP and bevel;
  - member marks and orientation;
  - design forces (T / C) per brace and the **transfer forces** at the eave-strut joints, or a statement that
    the connections are designed by the EOR;
  - the brace plane offset from the column outer flange (§7.2).
- **Gusset:**
  - thickness and grade;
  - outline dimensioned from the WP and the member faces (2ᾱ, 2β̄);
  - corner clip and trims;
  - weld to the column web and base plate (size, length, both sides), with the ductility size where it applies.
- **Brace end:**
  - slot width (tg + 2 × 2 mm) and **slot length = lap l + erection clearance x**;
  - lap length l from the brace end;
  - four-line fillet size (note "increase leg by root gap; gap ≤ 2 mm");
  - no weld return round the slot end (Part D §1.9);
  - erection bolt hole (size and position) through the tube and the gusset;
  - seal or vent the tube end against the weather (Part D §1.1).
- Brace cut length from the pull-off dimension. Tolerances.
- Optional: a top stiffener at the web, if the yield-line check fails; a stiffened or extended base plate if the
  gusset overruns it.
- At the X crossing: the chosen BC3 detail.
- Notes: the electrode; that the field welds are fillet welds made in the flat or horizontal position where
  possible; inspection level.

**7.6 Open questions for the engineer**
1. **Brace design basis:** tension-only, or tension and compression with the X crossing as a restraint? This
   decides BC3 and the gusset compression checks.
2. **Brace plane location** relative to the tapered columns, and whether the resulting eccentricity (up to
   about 250 mm at the eave if set at the base centroid) is taken into the column design or removed by a
   different gusset position.
3. **WP at the base:** top of the base plate (e = 0, recommended by DG29) or a raised WP to keep the brace end
   above the floor slab or plinth.
4. **Eave joint:** does the CHS 190.7 strut (or the H400 eave beam, where present) take any brace vertical
   (general UFM), or none (Special Case 2 / column-only gusset)?
5. **Anchor rods:** position and number at the braced-bay columns. DG29's path assumes rods near the flanges.
   Our pinned bases likely have rods near the web, which needs the base-plate uplift check. Also: shear lug or
   rods in shear for the longitudinal base shear.
6. **Material and design thickness of the "PG" CHS** (grade, Fy, Fu, whether 0.93t applies), and the gusset
   grade (SS400 / SM400 / SM520).
7. **Field welding vs a bolted tab end** for erection in this region. Site-weld quality and painting or
   galvanizing of the field welds.
8. **Load presentation:** will the drawings carry consistent load-case matrices or max forces plus transfer
   forces (App D)? This applies especially to the eave-strut joints that collect roof bracing.
9. **Minimum design force for the bracing connections** (for example a nominal minimum or a fraction of the
   brace capacity) if wind forces are small. DG29 designs R ≤ 3 connections for the analysis force only.
