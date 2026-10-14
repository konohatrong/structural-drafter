# 08 Bases in the seismic force-resisting system (DG1 §2.12, §3)

## When it applies [CODE]

- The AISC Seismic Provisions (2005; now AISC 341) govern members and connections of the seismic load-resisting system (SLRS) where **R > 3**, whatever the seismic design category.
- Column base strength for SLRS columns: Seismic Provisions **§8.5** (2005 numbering). Its Commentary is the recommended source on SLRS bases.
- Concrete elements of the base: ACI 318 Appendix D (now Ch. 17), **without** its extra seismic requirements, because §8.5 already sets the required strength at a higher force level. [REC] Check the current ACI 318 and AISC 341 on this point; the rules have changed since 2005.

## Ductility [DG]

- SLRS frames must behave in a **ductile** way. Design the foundation and base so the **concrete tension and shear limit states of the rod group do not govern** (ACI 318-02 D3.3.4).
- Example 4.7 shows the effect: with the ACI-02 seismic factor of 0.75 on anchor strength, 1½ in. rods became too small.

## Braced-frame bases [DG]

Design for the required strength of the elements connected:
- the column's required tension and compression;
- the **brace connection's required strength**;
- the base fixity or bending resistance for the moments at the **design storey drift**.

Alternatively, where permitted, use the **amplified seismic load** combinations of the building code.

## Moment-frame bases [DG]

- Designed as **fully restrained (FR)**, truly **pinned**, or, more accurately, **partially restrained (PR)**.
- Detail them **consistent with the expected behaviour**, allowing for the stiffness and strain capacity of the column, rods, plate, grout and concrete.
- The base must either keep its assumed fixity, or provide the shear strength while allowing the expected rotation.
- Details: Fig. 2.6, an exposed moment base; Fig. 2.7, an **embedded** base.
- Seismic shear is sometimes taken by **embedding the column base** and transferring it into the floor, with reinforcement around the column to spread the force.

## Differences from beam-to-column joints [DG, from the Commentary]

1. Long embedded rods **strain much more** than high-strength bolts or welds.
2. Plates bear on **grout and concrete**, which are more compressible than a column flange.
3. Bases carry more **longitudinal** load in the flange plane and less transverse load.
4. The **shear mechanism** against grout or concrete differs from an end plate on a flange.
5. Anchor rod **holes are larger** than standard bolt holes.
6. **Foundation rocking and rotation**, especially on isolated footings.

Research on bases under high seismic load is limited, but they matter greatly to the SLRS. Design them with care.

## Office note [REC]

- On Thai projects, check DPT 1301/1302 for the seismic zone and the R used. If R > 3 with an AISC 341 system, record in the design basis which base limit state governs and show that it is a ductile one (rod yielding or plate yielding, not concrete breakout).
- For these bases, use **Table 2.3 holes with welded plate washers** where the rods take shear (15), and show the stretch length of the rods if a ductile rod mechanism is intended.
