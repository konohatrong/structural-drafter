# MIDAS CIVIL NX — API Endpoint Reference

> **Copied** from [`konohatrong/midas_API`](https://github.com/konohatrong/midas_API/blob/b4155ac/MIDAS_CIVIL_NX_API_Reference.md) (`MIDAS_CIVIL_NX_API_Reference.md`, commit b4155ac, 2026-10-04) into this repository's `midas/` folder. Paths in the text such as `To midas/…`, `pilot project/…` or the root `README.md` name that repository; the map is in [`midas/README.md`](../README.md).

> Extracted from the official Python library `MIDASIT-Co-Ltd/midas-civil-python`
> (source verified, not guessed). Codes mirror MIDAS legacy **MCT** command keywords.
> Generated: 2026-06-08

## How a call is made

```python
MidasAPI(method, command, body)
#   method : "POST" | "GET" | "PUT" | "DELETE"
#   command: e.g. "/db/NODE"
#   body   : {"Assign": {"1": {"X":0,"Y":0,"Z":0}}}

# Under the hood:
url     = base_url + command   # https://moa-engineers.midasit.com:443/civil/db/NODE
headers = {"Content-Type": "application/json", "MAPI-Key": <key>}
```

- **Auth:** `MAPI-Key` HTTP header (token from product ribbon -> APPs -> API Settings -> Refresh).
- **Base URL (default):** `https://moa-engineers.midasit.com:443/civil` (5 global regions; `MAPI_BASEURL.autoURL()` auto-picks nearest).
- **Methods:** `POST` create, `GET` read, `PUT` update/assign, `DELETE` remove.
- `UNIT` and `STYP` accept **only GET/PUT**.

Command families: `/db/*` (model data), `/doc/*` (document & analysis ops), `/ope/*` (operations), `/post/*` (results).

---

## /db/* — model database

### Model / global  (_model.py)
| Code | Meaning |
|------|---------|
| STYP | Structure Type (GET/PUT only) |
| UNIT | Unit System (GET/PUT only) |
| PJCF | Project / model config |

### Geometry  (_node.py, _element.py)
| Code | Meaning |
|------|---------|
| NODE | Nodes |
| SKEW | Nodal local-axis / skew |
| ELEM | Elements (truss/beam/plate/solid) |
| ESSF | Element stiffness scale factors |
| VBEM, DOEL | Virtual beam / dummy elements |

### Sections & thickness  (_section/, _thickness.py, _utils.py)
| Code | Meaning |
|------|---------|
| SECT | Sections |
| SECF, VSEC | Section data / value section |
| TSGR | Tapered Section Group |
| OFFS | Section/element offset |
| THIK | Plate thickness |

### Materials  (_material.py)
| Code | Meaning |
|------|---------|
| MATL | Materials |
| TMAT | Time-dependent material (comp. strength) |
| TDME | TD material - creep/shrinkage |
| TDMT, TDMF | TD material type / link |

### Boundaries  (_boundary.py, _BoundaryChangeAssignment.py)
| Code | Meaning |
|------|---------|
| CONS | Supports / constraints |
| RIGD | Rigid link |
| ELNK | Elastic link |
| NLNK | General (nonlinear) link |
| NSPR, GSPR | Point / general spring support |
| FRLS, PSSF | Beam-end release / partial fixity |
| MLFC, BCCT | Misc boundary fns / boundary-change-by-stage |

### Groups  (_group.py)
| Code | Meaning |
|------|---------|
| GRUP | Structure group |
| BNGR | Boundary group |
| LDGR | Load group |
| TDGR | Tendon group |

### Static loads  (_load.py)
| Code | Meaning |
|------|---------|
| STLD | Static load cases |
| CNLD | Nodal (concentrated) loads |
| BMLD | Element beam loads |
| PRES | Pressure loads |
| BODF | Self-weight / body force |
| FBLD, FBLA | Floor load + allocation |
| NMAS | Nodal masses |
| SDSP | Specified displacements |
| PLCB, LTOM, EXLD | Plane-load / lumped mass / external loads |

### Load combinations  (_loadcomb.py)
| Code | Meaning |
|------|---------|
| LCOM | Load combinations |

### Construction stage  (_construction.py)
| Code | Meaning |
|------|---------|
| STAG | Construction stages |
| CSCS, CMCS | Composite section by stage |
| CRPC | Creep coefficient |
| TMLD | Time loads |

### Temperature loads  (_temperature.py)
| Code | Meaning |
|------|---------|
| STMP | System temperature |
| ETMP | Element temperature |
| NTMP | Nodal temperature |
| BTMP | Beam-section temperature |
| GTMP | Temperature gradient |

### Prestress / tendon  (_tendon.py)
| Code | Meaning |
|------|---------|
| TDNA | Tendon profile |
| TDNT | Tendon property |
| TDPL | Tendon prestress load |
| PTNS, PRST | Post-tension / prestress |

### Moving load  (_movingload.py)
| Code | Meaning |
|------|---------|
| MVLD | Moving load case |
| MVHL, MVHC | Vehicle / vehicle class |
| LLAN, SLAN | Traffic line / surface lane |
| MVCD, MVCT | Moving-load code & control |

Country-variant suffixes: `…BS` British, `…CH` China, `…ID` India/IRC, `…EU` Eurocode, `…PL`, `…TR`.
Examples: MVLDBS, MVLDID, MVLDEU, MVLDPL, MVLDCH, MVLDTR, LLANCH, LLANID, MVCTBS, MVCTID.

### Settlement / response spectrum / dynamic
| Code | Meaning |
|------|---------|
| SMLC, SMPT | Support settlement (case / point) |
| SPFC, SPLC | Response-spectrum function / case |
| DYLA, DYNF, DYFG | Dynamic load / function / config |
| NLCT, NLLP | Nonlinear analysis control / load steps |

### Analysis control  (_analysiscontrol.py)
| Code | Meaning |
|------|---------|
| ACTL | Main analysis control |
| BUCK | Buckling analysis control |
| EIGV | Eigenvalue analysis control |
| PDEL | P-Delta analysis control |
| SMCT | Construction-stage analysis control |

### Results / tables / specialty
| Code | Meaning |
|------|---------|
| UTBL | User result table |
| THFC, THIS, THSL, THGA, THGC, THMS, THNL | Time-history function / case / config |
| IEHC, IEHG | Inelastic hinge property / config |
| FIBR | Fiber section |
| SDIS, SDSP, SDST, SDVE, SDVI, SDHY | Seismic device / damper / isolator |
| EPMT, EPSE, EPST | Element pressure / settlement |
| Others (module-inferred) | STRPSSM, SBDO, PZEF, CGLP, CJFG, CLDR, CLWP, CRGR, CUTL, DRLS, EDMP, EWSF, FIMP, FMLD, GRDP, GSTP, HHCT, IMFM, IMPF, MADO, MCON, MLSP, MLSR, NBOF, PJCF, PNLA, PNLD, POSL, POSP, PRLS, PSLT, PZEF, RPSC, SINF, SPFC, SSPS, STBK, STCT, TDCS, TDNA, THGA, TSGR, UTBL |

---

## /doc/* — document & analysis operations
| Command | Action |
|---------|--------|
| /doc/NEW | New model |
| /doc/OPEN | Open model |
| /doc/CLOSE | Close model |
| /doc/SAVE | Save |
| /doc/SAVEAS | Save as |
| /doc/ANAL | Run analysis |
| /doc/IMPORT | Import |
| /doc/EXPORT | Export |
| /doc/IMPORTMXT | Import MCT text |
| /doc/EXPORTMXT | Export MCT text |
| /doc/STAGAS | Save construction-stage |

## /ope/* — operations
| Command | Action |
|---------|--------|
| /ope/PROJECTSTATUS | Model / project status |
| /ope/UTBLTYPES | Available result-table types |

## /post/* — results
| Command | Action |
|---------|--------|
| /post/TABLE | Query result tables (reactions, displacements, member forces, stresses) as JSON |

---

## Worked example (CRUD + analysis)

```python
from midas_civil import *
MAPI_KEY('<your key>'); MAPI_BASEURL.autoURL()

# create nodes
MidasAPI("POST", "/db/NODE", {"Assign": {
    "1": {"X":0,"Y":0,"Z":0},
    "2": {"X":5,"Y":0,"Z":0}}})

MidasAPI("GET",    "/db/NODE")                                    # read all
MidasAPI("PUT",    "/db/NODE", {"Assign":{"2":{"X":6,"Y":0,"Z":0}}})  # update
MidasAPI("DELETE", "/db/NODE", {"Assign":{"2":{}}})              # delete

# beam element
MidasAPI("POST","/db/ELEM",{"Assign":{"1":{
    "TYPE":"BEAM","MATL":1,"SECT":1,"NODE":[1,2]}}})

MidasAPI("POST","/doc/ANAL")                                      # run analysis
```

Response envelope:
- GET  -> `{"<KEYWORD>": {"<id>": {...fields...}}}`
- POST/PUT/DELETE -> `{"<KEYWORD>": {"ASSIGN": "..."}}` or an error block.

---

## Notes
- Full master enumeration of every supported code: `midas-civil-python/midas_civil/_mapi.py`.
- Codes labelled "module-inferred" are reliably handled by the noted module but the source
  does not spell out a long name; read the specific module for exact JSON fields.
- High-level Python wrappers (Node, Element, Material, Section, ...) sit on top of MidasAPI
  and call these same endpoints for you.
