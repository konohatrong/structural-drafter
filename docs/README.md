# Drawing rules, guides and instructions

The knowledge base an agent (or a drafter) uses to produce structural drawings in this office. Three layers:

1. **`general/`**: rules for **every** structural drawing, whatever the material: sheets, lines, text, dimensions,
   levels, marks, leaders, annotation, symbols, general-notes sheets, and how a set is produced.
2. **`concrete/`** and **`steel/`**: what is specific to each material: what the set must contain, how the material
   is presented, its symbols and its sources.
3. **`../jobs/`**: worked examples. Each job is a complete set built with these rules, and the record of how the
   rules were developed (`jobs/README.md`).

When two documents disagree, follow the precedence in `AGENTS.md` §1: the project and the engineer first, then the
office rules (newest dated rule first, material over general), then the EIT text, then sources. Resolve a conflict in
the documents rather than in one drawing.

## 1. Index

### general/ (any structure type)

| File | Covers |
|---|---|
| `general/DRAWING_STANDARD_EIT-011006-19.md` | EIT 011006-19 digest: sheet set-up, title block, lines and pens, scales, lettering, grids, dimensioning, levels, member marks, section and detail callouts, drawing numbering, CAD layers, QA checklist; **§19 office conventions** (A3, Arial Narrow, pens, dimensions, annotation summary, earthwork graphics) |
| `general/ANNOTATION_ALIGNMENT_GUIDE.md` | Where and how annotation goes: note columns and rows, leaders (standard angle and orthogonal), terminators, clean dimensioning, **units on numbers**, view titles, keep-out zones, member tags, cutting planes, detail callouts, labels on the member, fitting views. §0 maps the rules to structure types |
| `general/SYMBOLS.md` | Catalogue of every symbol: reference, annotation, concrete and steel symbols, with layer, helper and rule |
| `general/GENERAL_NOTES_DRAWING_INSTRUCTION.md` | Layout of a general-notes sheet: sizes (current: normal sizes, flowing over sheets; first review print: × 0.625), anatomy, wording, tables, layout engine, checklist. Its §4.3 lists what a concrete notes sheet must carry; steel equivalents are in the steel instruction S1 and S9 |
| `general/DRAWING_ENGINE.md` | The shared engine (`drafter/td_engine.py`): model space and blocks, title block, linetypes and pens, the functions a job calls, opt-in options, checks, working in AutoCAD, pitfalls |
| `general/DRAWING_PRODUCTION.md` | The pipeline (calc → engine → views → build → look → plot → test → review), the engine, the `!!` checks, requirements, commands, plotting without AutoCAD, environment pitfalls |

### concrete/

| File | Covers |
|---|---|
| `concrete/README.md` | **The RC presentation approach**, documents, reading order, helpers |
| `concrete/RC_DRAWING_RULES_EIT-011006-19.md` | Reinforcement graphics, bar notation, required content of RC plans and member details, office bar rules |
| `concrete/TYPICAL_DETAILS_INSTRUCTION.md` | Typical-detail sheets (columns, beams, slabs) |
| `concrete/STAIRCASE_DRAWING_INSTRUCTION.md` | RC stairs |
| `concrete/GENERAL_NOTES_STRUCTURAL_CONCRETE.md` | Concrete general-notes content (master text and tables) |
| `concrete/reference/` | Digests of EIT 011008-21 and 011014-19; source extracts for columns, beams and slabs; ACI MNL-66 review |

### steel/

| File | Covers |
|---|---|
| `steel/README.md` | **The steel presentation approach**, documents, reading order, helpers |
| `steel/STEEL_DETAILING_INSTRUCTION.md` | Rules S1 – S11 and S9A (fly bracing) |
| `steel/reference/SOURCES_STEEL_DETAILING.md` | AISC DSC, DG21, DG24 and Beca SE-1505 extracts |

Other materials (timber, masonry, composite) have no folder yet. Use `general/` with the closest material rules (bolts
and plates from steel, bars from concrete), and start a folder when the first job of that kind is done.

## 2. Concrete and steel: two ways of presenting a structure

The general rules are shared. The presentation differs because the reader differs: the **fixer** places bars in a
form, the **fabricator** makes pieces in a shop.

| Topic | Reinforced concrete | Structural steel |
|---|---|---|
| Purpose of the drawing | Where every bar goes; the concrete outline is the container | Make and fit every piece without asking; shop-ready |
| Single source of data | Member catalogue / design calc; rules in tables | The design calc (`calc_*.py`): every size, length, weld, bolt |
| Scale | Plans to scale; **typical details N.T.S.** (dummy 1:25) with shortened lengths | **Everything to scale** (1:50 elevation … 1:5 connections, 1:1 weld zones) |
| Heaviest line | **The bars** (main 0.50) | **The steel outline**; walls and hidden parts fine grey dashed |
| The material in section | RC section **not hatched** (bars are the subject); non-subject elements hatched grey | Hollow section a **solid-filled ring**; never cross-hatched |
| Concrete that is not the subject | Hatched grey ANSI31 (focus rule) | Hatched `AR-CONC`, grout `AR-SAND` |
| Identification | Member marks (C, B, S …), bar marks in Ø4 bubbles, numbered callouts | Erection + **generated piece marks**, tags in circles beside members, plate marks p1 … |
| Connection information | Laps, anchorages, hooks: dimensions or rules ("≥ ld") and tables | **Weld symbols** (AWS A2.4) and bolt tables; joint geometry dimensioned from the chord face |
| Leader style | Standard angle (45° / 60° leg + run + shelf) | Orthogonal (straight or L, ≥ 3 mm leg) |
| Leader terminator on the key object | Arrow on a bar's edge; ring 2 × dot on a cut bar | Arrow on a plate edge; ring 1.25 × hole on a bolt |
| Schedules | Lap, cover, tie spacing, slab tables; member schedules | Member schedule, plates and fittings, field bolts, node / weld table; one weight figure |
| Extra content | Bar-end key, cover statement | Camber diagram, erection and lifting notes, weld key |

Both use the same sheets, title block, pens by colour, text, units rule, dimensioning rules, view titles, cutting
planes, detail callouts and the `!!` checks.

## 3. Conventions for these documents

- **Rules are numbered** so a review can cite them: "EIT §19.2", "guide §9.7", "S6.2".
- **A user rule is dated**, for example "(user rule, 2026-10-03)", and quotes the user's words when they are short.
- **Sources are cited** with page or clause: "DSC p.209", "AISC 360-16 Table K3.1A".
- **Write in material-neutral words** in `general/`. Give the worked example from the job where the rule came up, and
  mark a rule as material-specific only when it is.
- **File names are unique** across the repository (apart from the `README.md` files), so a bare name such as
  `SYMBOLS.md` in the text always points at one file. Use the folder path for a README.
