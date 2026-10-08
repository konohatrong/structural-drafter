# MIDAS GEN NX: API, modelling and report guides

This folder holds what this repository needs to **drive MIDAS GEN NX** (the building analysis program) through its
web API (MAPI): building an analysis model from the structural DXF, loading it, running it, and reporting from it.
The drawing side of the repository (`docs/`, `drafter/`, `jobs/`) does not use any of it.

**Start with [`MIDAS_GEN_NX_INSTRUCTION.md`](MIDAS_GEN_NX_INSTRUCTION.md)**: the rules for any MIDAS task (key
handling, write safety, the per-level gates, the known API failures), with a router to the detailed guides below.

## Source

Pulled on 2026-10-04 from the user's repository [`konohatrong/midas_API`](https://github.com/konohatrong/midas_API),
commit `b4155ac` (MIT). The copied documents are unchanged except for a "Copied from" note at the top and their links,
which now point inside this folder or, for parts left behind, to that commit on GitHub. Text that names
`To midas/…`, `pilot project/…` or "the root README" refers to the source repository; this table maps it:

| Here | Source in `midas_API` | What |
|---|---|---|
| [`MIDAS_GEN_NX_INSTRUCTION.md`](MIDAS_GEN_NX_INSTRUCTION.md) | (new) | The rule set for agents, distilled from all the guides |
| [`api/MAPI_GUIDE.md`](api/MAPI_GUIDE.md) | `README.md` | How MAPI works: relay architecture, key, base URLs, methods, JSON `Assign` model, session order, the Python library, analysis and results, clearing, plug-in internals, troubleshooting |
| [`api/CONVENTIONS.md`](api/CONVENTIONS.md) | `docs/CONVENTIONS.md` | Checklist for building a MIDAS tool; when a tool needs the solver |
| [`api/BEAM_LOAD_MAPPING.md`](api/BEAM_LOAD_MAPPING.md) | `pilot project/wind load generator/docs/MIDAS_MAPPING.md` | `/db/BMLD` beam loads verified on a live model: uniform, trapezoidal, partial, directions, signs |
| [`api/ENDPOINT_REFERENCE.md`](api/ENDPOINT_REFERENCE.md), [`api/ENDPOINTS_CIVIL.csv`](api/ENDPOINTS_CIVIL.csv) | `MIDAS_CIVIL_NX_API_Reference.md`, `MIDAS_CIVIL_NX_endpoints.csv` | Endpoint codes grouped and explained (taken from the CIVIL library; GEN shares the codes) |
| [`api/ENDPOINTS_GEN.csv`](api/ENDPOINTS_GEN.csv) | (new) | The 177 commands the GEN library itself uses, with the module that writes each and whether CIVIL has it |
| [`modeling-guide/`](modeling-guide/README.md) | `modeling-guide/` | DXF + AR plan → live model, one level at a time: intake, grid and columns, beams, curved beams, verification gates, slab Auto-mesh, room functions and live load, decision-log template, figures; **08 (new)**: a pile-supported flat slab with drop panels and rigid zones, built zone by zone (BANWA 2) |
| [`modeling-guide/scripts/fire_station/`](modeling-guide/scripts/fire_station/README.md) | same | The archived scripts of the Samut Songkhram fire station (Building B), by stage, with run order and which ones write to the live model |
| [`calc-report/CALC_REPORT_GENERATION.md`](calc-report/CALC_REPORT_GENERATION.md) | `pilot project/wind load generator/docs/CALC_REPORT_GENERATION.md` | Calculation report (`.docx`) from a live model: data, figures, ELF seismic, storey drift, member design pages, gotchas |
| [`plugins/PLUGIN_GUIDE.md`](plugins/PLUGIN_GUIDE.md) | `To midas/README.md` | Mandatory read before packaging a MIDAS plug-in: facts, file set, `manifest.json` schema, Do / Don't, gotchas, checklist |
| [`plugins/WIND_LOAD_GENERATOR_PLUGIN_NOTES.md`](plugins/WIND_LOAD_GENERATOR_PLUGIN_NOTES.md), [`plugins/template/manifest.json`](plugins/template/manifest.json) | `To midas/wind-load-generator/` | The worked plug-in's build history, and its manifest as the template to copy |
| [`tools/connection.py`](tools/connection.py) | `pilot project/wind load generator/src/windload/midas/connection.py` | `connect(key)`: UTF-8 guard, then tries the regional base URLs until `/ope/PROJECTSTATUS` answers |
| [`examples/`](examples/README.md) | `examples/` | Build a portal frame → run the analysis → read reactions, displacements, beam forces |
| [`lib/midas-gen-python/`](lib/README.md) | `midas-gen-python/` | The official `midas-gen` library source (v1.6.6, MIDAS India, MIT), to read |
| [`requirements.txt`](requirements.txt) | (new) | Packages for MIDAS work, kept apart from the drawing toolkit's |

**Left in the source repository** (not needed to work with GEN NX, or a separate product):

- `midas-civil-python/`: the CIVIL NX library. Its endpoint list is kept as `api/ENDPOINTS_CIVIL.csv`.
- `pilot project/wind load generator/`: the ASCE 7-22 wind-load tool (engine, tests, UI, specification, validation
  runs) and `To midas/wind-load-generator/source/`, its plug-in bundle. Only its MIDAS-general knowledge came here:
  the load mapping, the report guide, the plug-in notes and the connection helper. Its live-model lessons are rules
  M5 and M6 of the instruction.

## Setup

```powershell
pip install -r midas\requirements.txt
$env:PYTHONIOENCODING = "utf-8"
python midas\examples\analyze_and_report.py --key "<MAPI-KEY>"     # GEN NX open, a scratch model
```

The key comes from GEN NX → **Apps → API Settings → Refresh** (or Apps → Connect). It is a credential: give it on the
command line only, never in a file (instruction M1). `config.json` is git-ignored under `midas/` for the example's
optional key file, but the command line is the office rule.

## Worked example

`jobs/steel_portal_frame` (2026-10-04): a live GEN NX model read with a read-only script (`pull_model.py`, key on
the command line only), its connections designed from the model's design forces, and the A1 steel construction
set drawn from the snapshot.

`BANWA 2` (2026-10-07 / 08, project folder, not in this repository): the ground floor on 458 piles was built in a
live GEN NX model, first zone by zone (r27 - r33), then rebuilt in stages from the client loads (r34 - r38):
- ground beams, then outlines pre-split at 0.20, then 249 piles with rigid-zone nodes;
- the slab at 0.40 by region, then the drops and gutter strip at 0.20;
- 76 655 plates in all, every stage verified by read-back.

Method: `modeling-guide/08_PILE_SUPPORTED_FLAT_SLAB.md` §2A.

## Relation to the drawing work

The same drawings feed both sides. The floor-plan work (`docs/general/FLOOR_PLAN_DRAWING_INSTRUCTION.md`, job SSK)
already reads grids, SFL tags, columns and beam widths from the office DXF with ezdxf; the modelling guide reads the
same layers (`S-CONT_BEAM`, `S-HID_BEAM`, `S-EDGE_SLAB`, `Sym-SFL` …) for the analysis model, and both take
the structural level from the SFL tags. Keep one source for each value: when a project has both a drafting job and a model,
the grid, levels and sizes come from one extraction, and a value corrected on the drawing is corrected in the model.
