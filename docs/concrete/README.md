# Concrete drawings: approach, rules and reading order

Reinforced concrete (in situ and precast), foundations, retaining walls, slabs on ground and stairs. Read this with the
general rules in `docs/general/`, which apply to every structure type.

## 1. How an RC set presents the structure

An RC drawing exists to tell the fixer **where every bar goes**. The concrete outline is only the container. Everything
in the presentation follows from that.

| Topic | RC approach | Rule |
|---|---|---|
| **What the set is** | A construction set per the calculation, not shop drawings. It has general notes, plans (pile, footing, floors, roof), member details and schedules, and office **typical details**. No bar bending schedule | EIT §1, §14 – §15 (`RC_DRAWING_RULES_EIT-011006-19.md`) |
| **Scale** | Plans 1:100. Member details 1:10 – 1:50 (EIT Table 2.2: footings 1:50 / 1:20, members 1:20 / 1:10; 1:25 accepted). **Typical details are N.T.S.**: a dummy 1:25 with member sizes from one catalogue; lengths are shortened with break lines, sections are not | EIT §5; `MODEL_SPACE_SHEETS.md` |
| **Line hierarchy** | **Bars are the heaviest lines**: main bars 0.50, ties and stirrups 0.35, cut concrete 0.35, seen concrete 0.25, annotation 0.18, hatch 0.13 | EIT §19.2 |
| **Concrete in section** | **Not hatched**: the bars are the subject. Only an element that is *not* the subject of the detail is hatched grey, and its bars are grey (focus rule, `nf_hatch`) | EIT §19.6; R2 notes |
| **Bars** | Bars on their centrelines with real bends (R = 3.5 db); dots true size, at least 1.1 mm; stirrups wrap their corner bars; plain bar ends; laps drawn cranked | RC §12, §19.4, §19.7 |
| **Bar notation** | `4-DB16`, `DB12@200`, T / B, NF / FF. Steel grade only in the general notes | RC §12.3 |
| **Identification** | Member marks (F, C, B, S, W, ST + numbering, one system per project). Bar marks in Ø4 bubbles; numbered callouts with a list on dense details | EIT §10; guide §2 |
| **Leaders** | **Standard angle style** (§1 of the guide): an inclined 45° / 60° leg, a run and a 3 mm shelf. In R2 a note level with its target gets one horizontal leader | guide §1, §0 |
| **Terminators** | Arrow on a bar drawn along its length (tip on its edge); an open ring Ø = 2 × dot on a cut bar | guide §2.1 |
| **Dimensions** | Bar zones, laps, cut-offs and covers as dimensions or as rules in the note ("≥ ld", "Sn/4"); a dimension that would sit between the drawing and its notes goes into the note | guide §2.4.1, §5 |
| **Rules carried by tables** | Laps, cover, tie spacing, slab thickness: in numbered tables on the general-notes and typical-detail sheets, cited as "TABLE n" | `GENERAL_NOTES_STRUCTURAL_CONCRETE.md`; `TYPICAL_DETAILS_INSTRUCTION.md` §4C-1 |
| **Units** | Every measured value in a note carries its unit; dimension figures stay bare | guide §2.4.2 |

For how this differs from steel, see the comparison in `docs/README.md`.

## 2. Documents

| File | Use it for |
|---|---|
| `RC_DRAWING_RULES_EIT-011006-19.md` | Reinforcement graphics (§12), required content of RC plans and member details (§14 – §15), office bar rules (§19.4, §19.7) |
| `TYPICAL_DETAILS_INSTRUCTION.md` | Typical-detail sheets 11xx (columns, beams, slabs): numbering, sources, the content of every detail, generator, pitfalls, checklist |
| `STAIRCASE_DRAWING_INSTRUCTION.md` | RC stairs: design checks, views, bar shapes, notes |
| `docs/general/FLOOR_PLAN_DRAWING_INSTRUCTION.md` | Floor and foundation plans of RC buildings (with RC §14 for the required content) |
| `GENERAL_NOTES_STRUCTURAL_CONCRETE.md` | Content of the concrete general notes (office master text and tables). The sheet layout is in `docs/general/GENERAL_NOTES_DRAWING_INSTRUCTION.md` |
| `reference/SPEC_RC_DESIGN_EIT-011008-21.md` | Digest of EIT 011008-21 (RC design) chapters used by the notes and details |
| `reference/SPEC_CONCRETE_EIT-011014-19.md` | Digest of EIT 011014-19 (concrete materials and construction) |
| `reference/SOURCES_COLUMN_DETAILING.md`, `SOURCES_BEAM_DETAILING.md`, `SOURCES_SLAB_DETAILING.md` | Extracts per member from DPT 1301/1302, EIT 011008 and the TATA handbook, with page refs |
| `reference/REVIEW_ACI_MNL66.md` | Review of the set against the ACI Detailing Manual MNL-66(20), decisions D1 – D5 |

## 3. Reading order for a concrete task

1. `docs/general/`: the drawing standard, the annotation guide (§0 says which parts apply), the symbols catalogue and
   drawing production.
2. This README, then `RC_DRAWING_RULES_EIT-011006-19.md`.
3. The instruction for the member or sheet type (typical details, stairs, general notes, floor plans).
4. The source digest for the member, when a rule or value needs checking.
5. The closest example job (`jobs/README.md`):
   - `jobs/standard_set_R2` for typical details;
   - `jobs/nooker_rw` for a complete project set (calc + drawings);
   - `jobs/stair_demo` for stairs.

## 4. Engine helpers for concrete

In `drafter/td_engine.py`:
- bars: `bar`, `strip`, `dot` / `rdot`, `stirrup`, `crosstie`, `lap_crank`, `dist_line`, `dowel_end`;
- symbols: `zigzag` (construction joint), `level`, `zbreak`, `earth_band`, `nf_hatch` (focus rule);
- annotation: `leader(..., ring=db, mark=n)`, `callout`, `callout_list`, `row_label`, `zone` (stirrup positions);
- member sizes: `members.py`.

The full symbol list is in `docs/general/SYMBOLS.md` §3.
