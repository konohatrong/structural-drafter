# Vendored library: `midas-gen` (MIDAS GEN NX Python)

`midas-gen-python/` is the source of the official MIDAS GEN NX Python library, **v1.6.6**, by MIDAS India
(`MIDASIT-Co-Ltd/midas-gen-python`), MIT licence (`midas-gen-python/LICENSE`). It came here through
`konohatrong/midas_API` (commit b4155ac, 2026-10-04); only its `.github/` workflow and `.gitignore` were left out.

It is kept **to read**: which endpoint each class writes, which fields it sends, how `MidasAPI()` handles errors. To
use the library, install it from PyPI (`pip install midas-gen`, see `../requirements.txt`) or from this copy
(`pip install ./midas-gen-python`). Do not edit it here; a fix belongs upstream or in our own helper in `../tools/`.

Where to look:

| File | Holds |
|---|---|
| `midas_gen/_mapi.py` | `MidasAPI(method, command, body)`, `MAPI_KEY`, `MAPI_BASEURL` (`autoURL()`), the full command list |
| `midas_gen/_model.py` | `Model.create()`, `Model.analyse()`, `/doc/*`, `/ope/PROJECTSTATUS`, `/view/CAPTURE` |
| `midas_gen/_node.py`, `_element.py`, `_boundary.py`, `_group.py` | Nodes, elements, supports and links, groups |
| `midas_gen/_material.py`, `_section/`, `_thickness.py` | Materials, sections (`DB`, `DBUSER`, tapered, composite), plate thickness |
| `midas_gen/_load.py`, `_loadcomb.py` | Load cases, self weight, nodal / beam / pressure loads, combinations (`LCOM-GEN`, `LCOM-CONC` …) |
| `midas_gen/_result_table.py` | `Result.*` tables through `/post/TABLE` |

The endpoints it uses are listed in `../api/ENDPOINTS_GEN.csv`.
