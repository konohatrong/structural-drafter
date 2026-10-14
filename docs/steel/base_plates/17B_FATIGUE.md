# 17B Fatigue of anchor rods (DG1 App. A1.2)

## Fatigue (A1.2) [DG]

- Design for fatigue when there are **more than 20,000 cycles** of tension or flexure.
- **Category E′ with a threshold FTH = 7 ksi (48 MPa)**, pretensioned or not; tolerant of misalignment up to **1:40**.
- **F_SR = (Cf / N)^0.333 ≥ FTH**, Cf = 3.9 × 10⁸ (ksi units).
- No further check if the rod stays in compression all cycle, or the range is below FTH.
- Stress range from **service** live load, on the **tensile stress area**, by elastic distribution. Include **prying** if the plate is thinner than the rod diameter, and add the bending range. No stress concentration factors.
- Bending of rods is ignored except in **four-rod double-nut joints**, or where the levelling-nut gap exceeds one rod diameter. Then M ≥ rod shear × gap.
- Shear may be ignored for fatigue. Concrete fatigue need not be checked; the rod fails first.
- **Grades above 55 give no fatigue benefit** and are less tough.
- Base plates and nuts need no fatigue check unless the governing specification says so.

## Redundancy [DG]

- In a non-redundant structure, prefer **six, ideally eight rods**, though four may suffice for strength.
- With eight rods, losing one raises the neighbours' range about 25 %, and they last another 35 – 50 % of the first rod's life. **Four-rod joints fail completely soon after the first rod.**
- Circular patterns of six or more: **plate thickness ≥ rod diameter**; rod bending negligible if the levelling-nut gap is less than one diameter.

## Plate thickness for poles [DG]

- A thicker plate cuts the stress at the **pole-to-plate weld**. The FE study shows stresses at 2¼ in. thick about 65 %, and at 3 in. about 60 %, of those at 1¼ in. In Texas tests a 2 in. socket-joint plate outlasted a 1½ in. one.
- **Over 2 in. (50 mm)** is generally adequate; 3 in. is about optimum.
- Protect against **corrosion**: pitting cuts fatigue life. Galvanizing does not reduce fatigue strength significantly.

## Office note [REC]

Poles, signs, masts and machine bases are fatigue jobs: state the cycle count, category and stress range in the calc, and use the 18 installation notes.
