# Worked example LAD: typical fixed steel ladder LD1

A through ladder from the ground onto a roof slab (climb 4.5 m), drawn to the office standard of detail after the
study of the Beca SE-0504 ladder sheet (user, 2026-10-15). Three A3 sheets:

| Sheet | Content |
|---|---|
| LAD-ST-5201 | Front elevation (climbing side) and side elevation 1:25: rungs, flared walk-through, wall brackets, wall and slab cut, clear zone, step-across, levels |
| LAD-ST-5202 | Details 1:5: A rung to stile (plug weld), B wall bracket (plan section, chemical anchor), C base of a stile |
| LAD-ST-5203 | Optional cage, plan section 1:20; TABLE 1 geometry with the OSHA limits; TABLE 2 members; notes |

## Basis

- Geometry from **OSHA 29 CFR 1910.23 / 1910.28** (text checked on osha.gov, 15/10/2026), in `lad_engine.LIMITS`.
  The engine **asserts** every value against its limit and the climb against the 24 ft (7.3 m) fall-protection
  threshold: a change that breaks a limit stops the build.
- Comparison with AS 1657 (the Beca sheet) and the rest of the practice: `docs/steel/stairs/18_LADDER_DETAILING.md`.

## Open items (ASSUMED on the drawings)

1. Governing code for a project: Thai law and the client's standard, decided by the engineer.
2. Member sizes (stiles FL 75 x 10, rungs Ø20, brackets FL 75 x 10), bracket spacing ≤ 1800, anchors M16 hef 100,
   base PL 150 x 100 x 10: typical values, **not designed**. Add a calc (maximum intended load, 1910.23(d)(1)).
3. Cage dimensions (depth 750, hoops FL 50 x 6 at ≤ 1500, first hoop 2200, 7 verticals FL 25 x 6): assumed; a cage
   is not fall protection for new ladders above 7.3 m under OSHA.

## Commands

```powershell
$env:PYTHONIOENCODING = "utf-8"
python jobs\steel_ladder_typical\build.py
python jobs\steel_ladder_typical\plot.py --ezdxf
```

Engine: `drafter/td_engine.py` + `drafter/steel.py` + `drafter/steel_access.py` (ladder_front, ladder_side,
cage_plan, anchor_in_concrete, member_break).
