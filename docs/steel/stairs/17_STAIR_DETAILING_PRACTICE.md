# 17 Steel stair details to the office standard [REC]

**Why:** user, 2026-10-15: "check these folder inside there are finest ladder detail please improve yourself
equivalent to these … write .md for remind future project".
**Reference set:** Beca SE-0501 – SE-0503 (standard steel stair details, 2014, AS 1657-1992 basis). The files are in
`G:\My Drive\##Workset_Autocad\400 Standard Details\400 Standard Details\20 - STEELWORK\SE-0501-0503 Steel Stair Standard Details`.
This note is a digest of the practice in that set; the drawings themselves are not copied. Ladders: `18_LADDER_DETAILING.md`.

## What the set holds

| Sheet | Content |
|---|---|
| SE-0501 | Elevations of a stair with a landing and of a scissor stair at 1:20. They show support frames, WPs, spans, "18 RISERS MAX" and a figure for the 2000 head clearance. Also a landing plan with grating and bracing, the stringer schedule by span, and notes (rise × going product, nosings, isolation of dissimilar metals, design load) |
| SE-0502 | Every stringer joint at 1:10 – 1:20: on a landing beam with and without a landing; dropper; onto a support member; tread connection; base on concrete; into a concrete wall; cantilevered; top and bottom where a concrete floor sits on steelwork |
| SE-0503 | Support frames A – D chosen by H / W, a member schedule, and every joint with an alternative detail |

## How a joint is drawn (pens measured on the PDFs, A1)

- **Pen hierarchy:**
  - 0.35: main steel;
  - 0.25: secondary steel, hidden lines, dimensions and leaders;
  - 0.13 – 0.18: centre lines, bolt crosses and the human figure;
  - 0.05 – 0.08: grating and concrete hatch;
  - 0.50: reference bubbles.
  Our A3 pens already follow the same order (EIT §19.2).
- **Stringer:**
  - seen side-on, with both edges and the flange-toe lines of a channel;
  - the treads behind it are **hidden**, each drawn as its profile;
  - the **nosing line** is a chain line with its label;
  - the **WP** (a circle with two opposite quarters filled) sits at the nosing line / floor intersection.
- **Sections cut or seen end-on** are their actual profiles in outline (fillets, flange taper, corner radii), as
  in the office block library - never solid fills (steel S4.15).
- **Members cut off** end in a break line across the member. Grating in section is a strip with bearing-bar ticks.
- **Dimensions** set the joint out from the WP: 40 to the beam, the first riser, the going, the 15 nosing, and the
  10 kick plate. A limit is written on its dimension: "500 MIN", "750 MIN - 1000 PREFERRED".
- **Annotation:** every member, plate, cleat, bolt (number, size, grade, slot) and anchor (embedment, grout) is
  named on a leader. Welds use weld symbols.
- **General elevation:**
  - each joint is enclosed in a **dashed rounded box** with a split bubble "letter / sheet";
  - spans read "STRINGER SPAN (REFER SCHEDULE)", and the values sit in the schedule.
- **Handrails** are tubes: a double line with a centre line, radiused bends, and posts as double lines.

## Checklist for our stair sets

1. Each flight carries "n R @ r = total" and "(n − 1) G @ g = total", a WP at both ends, and the headroom.
2. Each of these has a 1:10 detail: stringer end, foot, tread, landing support and wall fixing. The detail shows the
   WP, rise, going, nosing line, break lines, and members and bolts as built.
3. Guards are tubes. **Post spacing is measured along the rail** (the calc's span), not in plan.
4. Detail boundaries are rounded boxes with split bubbles, placed in clear space.
5. **Buildability check:** every bolt must be reachable for tightening. A nut inside a closed RHS needs a nut welded
   on in the shop, or the connection changes. Also check galvanizing vents and isolation of dissimilar metals.

## Helpers: `drafter/steel_access.py` (opt-in)

| Need | Helper |
|---|---|
| WP | `wp_point` |
| Detail boundary and reference | `call_box`, `ref_bubble` |
| Break across a member | `member_break` |
| Stringer, treads, nosing | `stringer_side(toe=)`, `treads_behind`, `treads_cut`, `nosing_line`, `flight_dims` |
| Rails and posts | `tube_run` (`fillet_path`), `post_side`, `tube_end_section` |
| Bolts and anchors as built | `bolt_along`, `anchor_in_concrete` |

## Lessons from RPM stair C A3 (2026-10-15)

- When the stringer top *is* the nosing line, the chain line is not drawn over it. The note says "TOP ON THE NOSING
  LINE".
- A2 detail 2/5102 bolted through an end plate into a closed RHS. The nuts could not be reached. This was found only
  when the detail was drawn as built.
- A4 (review of A3): the knee-bracket section showed the wall-plate anchors on the post flange tips (plates widened to
  250 with anchors at 150). The engineer's analytical model (pins, moment release, loads from the stringers) is for
  the calc, not the drawing (review of A4).
- A5 (review of A4): channel stringers (JIS C 200) cranked level at the landings and seated on the bracket arms, which
  sit under the landing frames; no wall post; struts cut to the wall plates and welded all round.
- A7 (review of A6): the engineer's landing framing - stringers continued level across the landings (the upper
  flight's stringers cantilever past the arm and carry the lower flight's stringers by shear connections on fin
  plates), C end beams, angle joists at <= 400 mm, a stiffener plate in the channel at each guard post (DG34 12B).
  The calc became one grillage of the whole stair, because continuity changes every reaction. Joists must frame
  between members at deck level: a joist spanning between arms under 200 deep stringers would sit 135 mm low.
- Deleting a support is a design change: rerun the calc before drawing. RPM CS1 out: L1 corner 20 mm live deflection
  (1.6 mm with it), put to the engineer as a decision.
