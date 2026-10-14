# 11 Anchorage of rods in concrete (DG1 §3.2.2)

DG1 uses ACI 318-02 Appendix D (now Ch. 17) with ASCE 7 load factors. US units: f′c in psi, lengths in in., forces in lb.

## Pullout of a headed rod or nut [CODE]

- **φNp = φ ψ4 Abrg 8 f′c**, φ = 0.70; ψ4 = **1.4 uncracked** at service, else 1.0.
- Abrg = bearing area of the head or heavy hex nut.
- Table 3.2 gives φNp for heavy hex nuts, **without** the 1.4. ¾ in.: 15.2 kips; ⅞: 20.5; 1½: 52.6.
- **Pullout never governs for Fy 36 ksi rods in 4 ksi concrete.** Higher grades may need **washer plates**, kept as small as possible (large ones reduce the pullout resistance).

## Hooked rods [CODE + DG]

- φNp = φ ψ4 (0.9 f′c eh do), φ = 0.70, hook extension **eh ≤ 4.5 do**.
- Hooks fail by **straightening and pulling out** after the concrete above the hook crushes. Use them only when the tension is **small**. Example 4.5: a 3½ in. hook on a ⅞ in. rod gives 8.1 kips against 17.5 needed.

## Concrete breakout (CCD method) [CODE]

- Cone at about **35° (1 : 1.5)**, taken square in plan (Fig. 3.2.1).
- Single anchor: A_No = 9 hef². Group: A_N = projected area of the overlapping cones, limited by edges and thickness (Figs. 3.2.2, 3.2.3).
- hef < 11 in.: **φNcbg = φ ψ3 24 √f′c hef^1.5 (A_N / A_No)**.
- hef ≥ 11 in.: **φNcbg = φ ψ3 16 √f′c hef^(5/3) (A_N / A_No)**.
- φ = 0.70; ψ3 = **1.25 uncracked**, 1.0 cracked. Cracked concrete: use **80 %** of the uncracked values.
- Valid for rod diameter **≤ 2 in.** and hef **≤ 25 in.** (635 mm).
- Example 4.4: one ¾ in. rod, hef 6 in., 4,000 psi uncracked → 19.5 kips, more than the rod's 14.4.

## Side-face blowout [DG]

- Bursting from the head towards a near free edge (Fig. 3.2.4).
- Keep **side cover c1 ≥ 6 rod diameters** for F1554 Gr 36. Washer plates help by increasing the bearing area.

## Piers: develop the rods into the bars [DG]

- In piers, breakout alone **cannot** carry significant tension: the cone is cut off by the pier faces. Example 4.5: 20 in. pier → 25.5 kips against 69.8.
- Then the **vertical pier bars** take the rod force. They must be sized and **developed on both sides of the failure plane** (Fig. 3.2.5). They usually double as the pier's own reinforcement.
- Rod strength may then be taken as **φ Ase Fy** (φ = 0.90): the lap makes it ductile.
- **Embedment = top cover + Ld (or Ldh) + 0.75 g**, g = horizontal offset between rod and bar. **Minimum 17 rod diameters.** Hooks on the bars shorten Ld.
- Example 4.5: 4-#7 corner bars, lap 17.4 in. (Class B, 1.3 Ld) → **hef = 25 in.**

## Seismic [DG]

With R > 3, rods to the Seismic Provisions §8.5; design so concrete breakout does not govern (08).

## Office note [REC]

- For Thai piers and pedestals, the pier-bar method is the normal case: show the rod length reaching past the bar lap, and the ties at the pier top (15).
- The calc gives φNsa, φNp, φNcbg (or the bar-lap check), and side blowout, and reports the governing one and whether it is ductile.
