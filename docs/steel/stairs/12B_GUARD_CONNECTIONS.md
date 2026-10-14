# 12B Guard and handrail connections (DG34 §7.3, Ex. 10.1.8)

**Fabrication:** shop-weld guard and handrail assemblies to the **largest shippable size**, then field-weld or bolt them to the stringer or support.

## Rail-to-rail joints [DG]

- Rails, posts and pickets are joined with **fillet or butt welds**.
- **Weld finish** is part of the specification: NAAMM Pipe Railing Manual finish levels, smooth wherever hands slide.

## Handrail brackets [DG]

- Shop-made bar or rod, or a bought product.
- **Bought brackets need test documentation:** ASTM E935 test methods with the ASTM E985 criteria (E985 is withdrawn, but still specified), or other tests that show the code load and deflection are met.
- Check the bracket **and its fasteners** for **vertical and lateral** load.

## Post-to-stringer: the most heavily loaded joint [DG]

| Mounting | Design points |
|---|---|
| **Side of the stringer** (face of a plate or HSS, Fig. 7-5) | Bolts or welds for vertical, lateral and **torsional** forces. The **stringer and its end connections must resist the torsion**, or the treads and risers take the force couple |
| **Top of the stringer** (channel or HSS, Fig. 7-6) | Usually welded. The post and weld must **fit on the flange**. Pipe posts: fillet welds are easiest. A **one-sided CJP square-groove butt weld** is **not prequalified without a backing bar**, so the procedure and welders must be qualified (AWS D1.1) |

Anchorage testing of railing systems: ASTM E894.

## Channel flange under a post [DG]

The post moment bends the channel's top flange and web. Effective width, spreading at 2.5 : 1 (from experience and FE analysis):

**B_eff = N + 2(2.5)[(k − t_f/2) + b_f]**  (DG34 Eq. 7-1)

where N = post diameter, k = fillet dimension, t_f = flange thickness, b_f = flange width.

Check the **web as a rectangular bar** of width B_eff:
- Z = B_eff t_w² / 4, S = B_eff t_w² / 6;
- Mn = Fy Z ≤ 1.6 Fy S (AISC 360 F11).

**Ex. 10.1.8** (C12×20.7 A36, HSS1.900 post, 200 lb at 42 in.):
- B_eff = 1.90 + 5[(1.125 − 0.251) + 2.94] = **21.0 in.**
- Z = 0.418 in³; Mn = 15.0 kip-in.
- **LRFD 13.4 ≤ 13.5 kip-in.**, ASD 8.40 ≤ 8.98 kip-in. Adequate, just.

**Rule of thumb [DG]:** a single post on a channel with **web ≤ ¼ in. (6 mm)** gets a **stiffener plate** under the post, unless a finer analysis (frame action, load sharing) shows it is not needed.

## Posts and handrails at concrete, masonry and stud walls [DG]

- **Posts grouted into core-drilled holes:** good indoors, with enough slab depth and distance from edges. Outdoors, **rust at the steel-grout line** becomes a maintenance issue; discuss it with the owner.
- **Wall brackets on concrete or masonry:** approved post-installed screw anchors.
- **Stud walls:** **blocking or backing is required**. Gypsum or sheathing alone rarely carries the code load. Check the screws too.

## Office notes [REC]

- Draw the post base as a detail: weld symbol all round, stiffener plate (size and welds) where the web ≤ 6 mm, and the post centre relative to the stringer face.
- Draw bracket spacing on the handrail elevation, with the anchor type.
- At stud walls, add "PROVIDE BLOCKING BY OTHERS, DESIGN LOAD 0.89 kN ANY DIRECTION".
