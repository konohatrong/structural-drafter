# 03 Gravity loads (DG34 §3.1 – 3.2.3)

The authority having jurisdiction decides the code.

- **IBC 2015 with ASCE/SEI 7-16** is the default, and an IBC stair is accepted almost everywhere.
- **OSHA 1910 Subpart D** only where allowed: industrial or exempt occupancies, or under a waiver.
- Combinations: ASCE 7 Ch. 2 (LRFD 1.2D + 1.6L; ASD D + L).
- Environmental, thermal and integrity loads → `03B_LOADS_OTHER.md`; seismic → 04.

## Dead load [DG]

- Steel framing, treads and risers, guards, handrails, landings, finishes, soffit covers. Stair members sometimes also carry partitions.
- **Allow 5 – 10 psf (0.24 – 0.48 kPa)** where MEP or sprinkler services hang under the stair.
- Typical extras (ASCE 7 Table C3.1-1):
  - tile on mortar bed 16 – 23 psf;
  - normal-weight concrete fill 12 psf per inch;
  - lightweight fill 8 psf per inch;
  - suspended ceiling about 2 psf;
  - stud wall with ½ in. gypsum each side 8 psf.
- **Sloped self-weight:** put on the horizontal projection, multiply the stringer weight by √(R² + T²)/T (1.19 for 7 / 11 in.).
- Example values:
  - 12-ga pan with 2 in. concrete fill, about 30 psf (1.44 kPa);
  - 3 in. slab on deck, 32 psf;
  - ³⁄₁₆ in. checkered-plate tread, 10 psf.
- DG34 adds **20 plf** to the stringer that carries the guard.

## Live load [CODE]

| Element | IBC / ASCE 7 | OSHA 1910 |
|---|---|---|
| Tread | **100 psf (4.79 kPa)** or **300 lb on 4 in² (1.33 kN on 50 × 50 mm)** | 5 × "normal" live load, or **1,000 lb (4.45 kN)** |
| Landing | 100 psf | as tread |
| Guard top rail / handrail | **200 lb (0.89 kN)** or **50 plf (0.73 kN/m)**, any direction | 200 lb down or out |
| Guard infill, intermediate rails | **50 lb on 1 ft² (0.22 kN on 300 × 300 mm)** | 150 lb (infill); toeboard 50 lb |

- The uniform and concentrated loads are **not concurrent**; design for the worse. Some local codes make them concurrent, so confirm.
- **OSHA "normal" load** = the expected users spread over the tread area. For example, one 300 lb worker on a 3 ft × 9-tread flight gives 11 psf, × 5 = 56 psf. **[DG] Also check at least 60 psf (2.87 kPa)**, the ASCE 7 walkway value.
- **Unbalanced patterns** can govern cantilevered stringers and fixed-base cantilever posts.
- Factory, industrial and storage areas closed to the public with ≤ 50 occupants are exempt from the 50 plf guard load (ASCE 7 §4.5.1).
- No allowable-stress increase for guards under ASD (IBC 2009 on).
- **ASTM E985** (withdrawn, but still in many specifications) raises the guard load in assembly buildings: 300 lb where ≥ 50 people use a room, 365 lb with 60 plf in the area the guard protects.

## Office note [REC]

On a Thai project, take the occupancy live loads from the Thai ministerial regulation on building loads (กฎกระทรวง). If the US guard and tread **point loads** are adopted as office practice, say so in the design basis. Thai rules often give no point load.
