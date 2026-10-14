# 10 Lateral load path: bracing and diaphragms (DG34 Ch. 5)

Wind, seismic Fp (04) and the stability or notional loads (03B) must travel from every tread and landing back to the building's lateral system. **Landings are where the path usually breaks.**

## Flight assembly (stringers + treads + risers) [DG]

| Model | When |
|---|---|
| **Each stringer takes half** the load in weak-axis shear and bending | Simplest. Often enough for stability loads and SDC A – B. Uses the unbraced length from 09 |
| **Horizontal built-up beam** (the whole flight) | Welded tread and riser construction. Thin pans may fail the local-buckling limits; checkered plate works better |
| **Horizontal Vierendeel truss** | Open risers: the treads act as verticals |

**Plate stringers** are weak about their minor axis. Detail a clear load path to the supports.

## Landing diaphragm [DG]

A landing that acts as a diaphragm gives the flights a lateral support.

| Diaphragm | Basis |
|---|---|
| **Concrete on metal deck** (most common) | Ample capacity at normal sizes. Large landings need more side-lap and support fasteners. SDI Diaphragm Design Manual |
| Concrete on stiffened plate | AISC Design Guide 20 principles |
| **Checkered plate** | AISC Design Guide 20 principles |
| Grating | Not a diaphragm: brace it |

## Bracing alternatives (DG34 Table 5-1) [DG]

| System | For | Against |
|---|---|---|
| **Tension-only** (rod, cable, angle, flat) | Small; hides in walls or under landings | More members and connections |
| **Tension-compression** (HSS, angles, pipe) | Fewer members and connections; can be hidden | Heavier; splices where the braces cross |
| **Moment frame** | Nothing crosses the path of travel; the beam also supports the landing | More drift; costlier connections (HSS joints: AISC Design Guide 24) |

Design to AISC 360, including the slenderness limits. Bracing connections: Manual Part 13 and AISC Design Guide 29 (DG34 Fig. 6-7: a single-angle brace under a landing).

## Typical paths [REC]

1. **Steel frame:** the landing deck, or plan bracing, carries the load to hangers or posts, which are braced to the floor beams. Flight ends bear on the floor beams.
2. **Concrete or masonry core:** the landing beams are anchored to the walls, and the walls resist. Check the anchors with Ωo (04).
3. **Sliding end** (04B): the lateral path goes through the **fixed end only**. The sliding end takes vertical load only.

## Checks [REC]

- Fp at the centre of gravity, both directions, with gravity (H1). Ex. 10.2.3 interaction was 0.12, so this rarely governs.
- The load component along the flight puts axial force in the stringers. Combine it; DG34's example omits it.
- Landing diaphragm shear, chords, and the connections to the supports.
- Brace slenderness and connections, and how the brace lands on its beam without torsion (08).
