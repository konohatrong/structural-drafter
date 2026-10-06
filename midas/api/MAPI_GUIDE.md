# Midas API

> **Copied** from [`konohatrong/midas_API`](https://github.com/konohatrong/midas_API/blob/b4155ac/README.md) (`README.md`, commit b4155ac, 2026-10-04) into this repository's `midas/` folder. Paths in the text such as `To midas/…`, `pilot project/…` or the root `README.md` name that repository; the map is in [`midas/README.md`](../README.md).

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/konohatrong/midas_API/blob/b4155ac/LICENSE)

A deep, practical reference for the **MIDAS Open API (MAPI)** — the web API behind
**MIDAS CIVIL NX** and **MIDAS GEN NX** — plus the plug-in built on it in this repo.

> Scope: this document explains the API *architecture and mechanics* in detail so
> you can drive MIDAS from any language. The exhaustive endpoint list lives in
> [`MIDAS_CIVIL_NX_API_Reference.md`](ENDPOINT_REFERENCE.md) and
> [`MIDAS_CIVIL_NX_endpoints.csv`](ENDPOINTS_CIVIL.csv).

---

## Getting started (first time here)

**Just cloned this repo? Start here.**

### What this repo is
- A **reference guide** to the MIDAS Open API (read the sections below), and
- the **MIDAS Python libraries** (`midas-gen-python/`, `midas-civil-python/`),
  vendored so you can read the actual source, and
- the home of a **modeling + load-assignment plug-in** for GEN NX (being built — see §14).

You can read everything here **without** MIDAS installed. You only need MIDAS GEN
NX **running** when you want to *send* commands to a live model.

### Prerequisites
| Need | For |
|------|-----|
| **Python 3.9+** (3.11 tested) | running any script / the library |
| **MIDAS GEN NX**, installed & open | *live* API calls only (not needed to read/learn) |
| **A MAPI-Key** | live calls — GEN NX → **Apps → API Settings → Refresh** |

### Setup
```bash
git clone https://github.com/konohatrong/midas_API.git
cd midas_API
pip install midas-gen          # the GEN NX API library (from PyPI)
```
> The `midas-gen-python/` and `midas-civil-python/` folders are the library
> **source**, kept for reference — you don't have to install them. `pip install
> midas-gen` fetches the same library. (To use the local copy instead:
> `pip install ./midas-gen-python`.)

### Your first command (≈30 seconds)
With GEN NX open and a key copied:
```python
from midas_gen import *
MAPI_KEY("<your key>"); MAPI_BASEURL.autoURL()
Node(0, 0, 0, id=1); Node(6, 0, 0, id=2)
Model.create()                 # two nodes appear in GEN NX
```
No MIDAS handy? You can still read the whole guide and skim the endpoint catalog.

### Where to go next
- **Don't know how the API works yet?** → [Start here — the mental model](#start-here--the-mental-model)
- **Want the full picture?** → the numbered sections (architecture, auth, JSON model, …)
- **Looking for a specific endpoint?** → [`MIDAS_CIVIL_NX_endpoints.csv`](ENDPOINTS_CIVIL.csv)
- **What's in this repo?** → [§17 This repository](#17-this-repository)

---

## Start here — the mental model

New to the API? Read this first; the numbered sections below go deep.

**The one idea:** in *any* programming language, you compute *what* you want, write
it as the **JSON shape a specific MIDAS endpoint expects**, and send it (with your
**MAPI-Key**) to the MIDAS app running on your PC — which performs it on the open
model.

### It's layers, not one thing

A common beginner thought is *"HTML + JS + Python all work together to do it."*
Closer to the truth: they are **layers with different jobs**, and you don't need
all of them.

| Layer | Job | Required? |
|-------|-----|-----------|
| **HTML + JS** | the **UI** — fields/buttons where a human sets parameters | optional (only if you want a UI) |
| **Python / JS / C# / curl** | the **logic** — decide *what* to build and shape the JSON | yes, but **any** HTTP-capable language works |
| **JSON + the API call** | the **message** — the actual instruction to MIDAS | always |

You can do the whole thing in **pure Python with no UI** (a short script using
the `midas-gen` library). The HTML/JS is just an optional friendly front-end on top.

### Every instruction = 3 choices + data

You can't send arbitrary JSON. One call is:

```
  METHOD                +  ENDPOINT   +  JSON body (a fixed shape)        +  MAPI-Key header
  POST/GET/PUT/DELETE      /db/NODE      {"Assign":{"1":{"X":0,"Y":0,"Z":0}}}   (routes to your PC)
```

- **Endpoint** = *which thing* (`/db/NODE` = nodes, `/db/ELEM` = elements, `/doc/ANAL` = run analysis)
- **Method** = *create / read / update / delete*
- **Body** = must match that endpoint's fields (the `Assign` envelope)
- **MAPI-Key** = tells the relay *which* running MIDAS to deliver to

### Where it actually goes

It is **not** "send to the cloud and the cloud does it." The cloud is just the postman:

```
your code ──REST + JSON──► MIDAS cloud relay ──WebSocket──► MIDAS app open on YOUR PC ──► your model
```

So the desktop app must be **open**, with the API enabled and a **key generated**.

### Analogy: ordering at a restaurant

- **JSON body** = your order on the restaurant's *standard form* (you can't invent your own form)
- **Endpoint + method** = which form (drinks vs mains) and what you're doing (order / change / cancel)
- **MAPI-Key** = your table number, so the food comes back to *you*
- **Cloud relay** = the waiter · **MIDAS on your PC** = the kitchen that cooks it

### It's two-way and sequential

Real workflows are **many calls in order**, not one push — and you read data back too:

```
nodes → elements → supports → load cases → loads → run analysis → read results
```

### Your first call (try it 2 ways)

First install the library:
```powershell
pip install midas-gen
```

**1) With the Python library (the friendly way)** — GEN NX open, key from
Apps → API Settings → Refresh:
```python
from midas_gen import *
MAPI_KEY("<your key>"); MAPI_BASEURL.autoURL()
Node(0, 0, 0, id=1); Node(6, 0, 0, id=2)   # build in memory
Model.create()                              # one push → two nodes appear in GEN NX
```

**2) Raw HTTP (the same thing, no library):**
```bash
curl -X POST "https://moa-engineers.midasit.com:443/gen/db/NODE" \
  -H "MAPI-Key: <your key>" -H "Content-Type: application/json" \
  -d '{"Assign":{"1":{"X":0,"Y":0,"Z":0},"2":{"X":6,"Y":0,"Z":0}}}'
```

Once that clicks, read on for the full architecture. 👇

---

## Table of contents

- [Getting started (first time here)](#getting-started-first-time-here)
0. [Start here — the mental model](#start-here--the-mental-model)
1. [What MIDAS API is](#1-what-midas-api-is)
2. [System architecture](#2-system-architecture)
3. [Authentication — the MAPI-Key](#3-authentication--the-mapi-key)
4. [Servers, base URL and ports](#4-servers-base-url-and-ports)
5. [The request/response model](#5-the-requestresponse-model)
6. [Command families: `/db`, `/doc`, `/ope`, `/post`](#6-command-families)
7. [The JSON data model](#7-the-json-data-model)
8. [Lifecycle of a modeling session](#8-lifecycle-of-a-modeling-session)
9. [Worked examples](#9-worked-examples)
10. [The Python library architecture](#10-the-python-library-architecture)
11. [Running analysis and reading results](#11-running-analysis-and-reading-results)
12. [Deleting / clearing model data](#12-deleting--clearing-model-data)
13. [Plug-in architecture (Marketplace)](#13-plug-in-architecture-marketplace)
14. [Building a MIDAS plug-in (detailed)](#14-building-a-midas-plug-in-detailed)
15. [Error handling & troubleshooting](#15-error-handling--troubleshooting)
16. [Appendix: endpoint families](#16-appendix-endpoint-families)
17. [This repository](#17-this-repository)

---

## 1. What MIDAS API is

MIDAS API (**MAPI**) is a **web-based REST API** that exposes the full data model
and solver of the MIDAS NX structural products. Anything you can build, load, or
analyze in the GUI can be done over the API with **JSON** payloads.

There are **two layers** you can work at:

| Layer | What it is | Audience |
|-------|-----------|----------|
| **MAPI (raw REST)** | JSON-over-HTTP calls that create/read/update/delete model objects and run the solver | Developers (Python, JS, C#, anything with HTTP) |
| **MIDAS Plug-ins** | Packaged mini-apps (API calls + math + UI) distributed through a Marketplace | End users; and developers who publish them |

Both NX products share the *same* API shape; they differ only in the base-URL
segment (`/civil` vs `/gen`) and the set of endpoints each product supports.

---

## 2. System architecture

The defining feature of MAPI: **your code does not connect to the desktop app
directly.** It talks to a MIDAS **cloud relay** over REST; the relay forwards the
call to the **MIDAS product running on your PC** over a **WebSocket** channel that
the product opens when its API is enabled.

```
   ┌─────────────────┐     HTTPS / REST + JSON      ┌──────────────────────┐
   │  Your client    │ ──────────────────────────► │  MIDAS cloud relay    │
   │  (Python / JS / │     header: MAPI-Key         │  moa-engineers...:443 │
   │   curl / app)   │ ◄────────────────────────── │  /civil  or  /gen     │
   └─────────────────┘     JSON response            └──────────┬───────────┘
                                                               │ WebSocket
                                                               │ (opened by the
                                                               ▼  running product)
                                                    ┌──────────────────────┐
                                                    │  MIDAS CIVIL/GEN NX   │
                                                    │  on your local PC     │
                                                    │  (holds the model)    │
                                                    └──────────────────────┘
```

Consequences of this design:

- **The desktop product must be running** with its API enabled, and a **MAPI-Key
  generated**, for any live call to succeed.
- The **MAPI-Key routes the request** from the relay to *your* specific product
  instance — it is both authentication *and* addressing.
- Calls are **stateful against the open model**: a `POST /db/NODE` mutates the
  document currently open in the product, exactly as if you'd typed it in the GUI.
- Latency includes a cloud round-trip; batch your writes (see §10).

---

## 3. Authentication — the MAPI-Key

Every request carries a single header:

```
MAPI-Key: <your personal access token>
Content-Type: application/json
```

**Getting the key (in the product):**

1. Open CIVIL NX / GEN NX.
2. Ribbon → **Apps** tab → **API Settings**.
3. Click **Refresh/Generate** — the key is **blank until you do this**.
4. Copy the **Base URL** and the **MAPI-Key** shown there.

**Properties of the key:**

- It is **per-user / per-instance** and identifies which running product the
  relay should forward to. Treat it like a password.
- Regenerating (Refresh) **invalidates the previous key**. If calls suddenly
  return auth errors, the key was refreshed or the session changed — copy the
  new one.
- Never commit it. In this repo, `config.json` (which holds the key) is
  git-ignored, and the web UI keeps it only in the browser tab.

---

## 4. Servers, base URL and ports

The base URL has the form `https://<relay-host>:443/<product>`:

| Product | Default base URL |
|---------|------------------|
| CIVIL NX | `https://moa-engineers.midasit.com:443/civil` |
| GEN NX | `https://moa-engineers.midasit.com:443/gen` |

**Regional relays** (pick the nearest for lower latency). The GEN library probes
these hosts (suffix `/gen`; CIVIL uses `/civil`):

| Region | Host |
|--------|------|
| India | `moa-engineers-in.midasit.com` |
| Korea | `moa-engineers-kr.midasit.com` |
| Great Britain / EU | `moa-engineers-gb.midasit.com` |
| USA | `moa-engineers-us.midasit.com` |
| China | `moa-engineers.midasit.cn` |

**Auto-selection.** The Python libraries expose `MAPI_BASEURL.autoURL()`, which
pings each relay's lightweight `"/config/ver"` endpoint with your key and locks
onto the first that answers — so you don't have to hard-code a region.

Port is always **443** (HTTPS).

---

## 5. The request/response model

A MAPI call is fully described by three things plus the auth header:

```
<METHOD>  <BASE_URL><COMMAND>
MAPI-Key: <key>
Content-Type: application/json

<JSON body>
```

### HTTP methods and their MIDAS meaning

| Method | Meaning in MIDAS | Typical body |
|--------|------------------|--------------|
| `POST` | **Create** new objects of a type | `{"Assign": { id: {...} }}` |
| `PUT`  | **Create-or-update / assign** (upsert by id) | `{"Assign": { id: {...} }}` |
| `GET`  | **Read** all objects of a type (or one by id) | *(none)* |
| `DELETE` | **Remove** objects of a type (all, or by id) | *(none)* or id filter |

`PUT` is the workhorse for writing — it assigns the given ids whether or not they
already exist. The Python library uses `PUT` for most "create" operations.

### The endpoint path

`<COMMAND>` is a short, lowercase-or-uppercase path like `/db/NODE`, `/db/ELEM`,
`/doc/ANAL`. The full URL is just `base_url + command`. Casing is accepted in
either form by the relay (`/db/node` ≡ `/db/NODE`).

---

## 6. Command families

Endpoints are grouped into four families by their first path segment:

### `/db/*` — the model database  *(the bulk of the API, ~150 endpoints)*

Each `/db/<CODE>` is one **table** of the open model file: nodes, elements,
materials, sections, supports, loads, stages, tendons, etc. The 4-letter `CODE`
mirrors MIDAS's legacy **MCT/MGT** command keywords (e.g. `NODE`, `ELEM`, `MATL`,
`SECT`, `CONS`, `STLD`, `LCOM`).

- Supports `POST`/`GET`/`PUT`/`DELETE` for most tables.
- A few **essential** tables are **`GET`/`PUT` only** — notably `UNIT`
  (unit system) and `STYP` (structure type) — because they always exist.

### `/doc/*` — document & solver operations

Model-file and analysis actions, e.g.:

| Command | Action |
|---------|--------|
| `/doc/NEW`, `/doc/OPEN`, `/doc/CLOSE` | new / open / close model |
| `/doc/SAVE`, `/doc/SAVEAS` | save / save-as |
| `/doc/ANAL` | **run the analysis** |
| `/doc/IMPORT`, `/doc/EXPORT` | import / export |
| `/doc/IMPORTMXT`, `/doc/EXPORTMXT` | import / export MCT text |

### `/ope/*` — operations / queries

Lightweight model queries, e.g. `/ope/PROJECTSTATUS` (is a model open? state) and
`/ope/UTBLTYPES` (which result-table types are available). Good for a cheap
"is my key + product alive?" probe.

### `/post/*` — results

`/post/TABLE` returns post-processing result tables (reactions, displacements,
member forces, stresses, …) as JSON after an analysis.

---

## 7. The JSON data model

### Writing — the `Assign` envelope

Writes are an object keyed by **object id**, wrapped in `Assign`:

```json
{
  "Assign": {
    "1": { "X": 0.0, "Y": 0.0, "Z": 0.0 },
    "2": { "X": 6.0, "Y": 0.0, "Z": 0.0 }
  }
}
```

- The **key is the id** (as a string). You control ids by setting them — this is
  how you build references (an element references node ids).
- The **value is the object's fields** for that table. Field names are the MCT
  field codes for that entity (e.g. a beam element: `TYPE`, `MATL`, `SECT`,
  `NODE`).

Some entities nest an `ITEMS` array (e.g. a support stores a list of constraint
items per node):

```json
{ "Assign": { "1": { "ITEMS": [ { "ID": 1, "CONSTRAINT": "1111111", "GROUP_NAME": "" } ] } } }
```

### Reading — the response envelope

`GET /db/<CODE>` returns the same shape it accepts, keyed by id:

```json
{ "NODE": { "1": { "X": 0.0, "Y": 0.0, "Z": 0.0 }, "2": { "X": 6.0, "Y": 0.0, "Z": 0.0 } } }
```

A successful write typically echoes a small acknowledgement; an error returns an
error object (often under a `"message"` / error block). Always check the HTTP
status **and** the body — a 200 can still carry a per-object error.

### Units & sign convention

Numeric values follow the **model's current unit system** (`/db/UNIT`). Gravity
acts in **−Z**, so downward loads and the self-weight factor are **negative**
(e.g. self-weight factor `−1` = 1.0 g down).

---

## 8. Lifecycle of a modeling session

A typical end-to-end flow:

```
 1. (product running, API enabled, MAPI-Key generated)
 2. Set base URL + MAPI-Key on the client
 3. (optional) GET /ope/PROJECTSTATUS        → confirm connection
 4. (optional) DELETE old tables             → clean slate (avoid id clashes)
 5. PUT /db/UNIT, /db/STYP                    → units & structure type
 6. PUT /db/MATL, /db/SECT                    → materials, sections
 7. PUT /db/NODE                              → geometry: nodes
 8. PUT /db/ELEM                              → geometry: elements
 9. PUT /db/CONS (+ /db/RIGD, /db/ELNK …)     → boundaries
10. PUT /db/STLD                              → static load cases
11. PUT /db/BODF, /db/CNLD, /db/BMLD …        → loads
12. POST /doc/ANAL                            → run solver
13. POST /post/TABLE                          → read results
14. (optional) POST /doc/SAVE
```

The **order matters for references**: nodes before elements (elements name node
ids), load cases before loads (loads name a case), sections/materials before
elements (elements name section/material ids).

---

## 9. Worked examples

### 9a. Raw HTTP with `curl`

```bash
BASE="https://moa-engineers.midasit.com:443/gen"
KEY="<your MAPI-Key>"

# create two nodes
curl -X POST "$BASE/db/NODE" \
  -H "MAPI-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"Assign":{"1":{"X":0,"Y":0,"Z":0},"2":{"X":6,"Y":0,"Z":0}}}'

# read them back
curl -X GET "$BASE/db/NODE" -H "MAPI-Key: $KEY"
```

### 9b. Raw HTTP with Python `requests`

```python
import requests

BASE = "https://moa-engineers.midasit.com:443/gen"
HEADERS = {"MAPI-Key": "<key>", "Content-Type": "application/json"}

def mapi(method, command, body=None):
    url = BASE + command
    r = requests.request(method, url, headers=HEADERS, json=body or {})
    r.raise_for_status()
    return r.json()

mapi("POST", "/db/NODE", {"Assign": {"1": {"X": 0, "Y": 0, "Z": 0},
                                       "2": {"X": 6, "Y": 0, "Z": 0}}})
mapi("POST", "/db/ELEM", {"Assign": {"1": {"TYPE": "BEAM", "MATL": 1,
                                            "SECT": 1, "NODE": [1, 2]}}})
print(mapi("GET", "/db/NODE"))
mapi("POST", "/doc/ANAL")
```

### 9c. With the official Python library (recommended)

```python
from midas_gen import *          # or: from midas_civil import *

MAPI_KEY("<key>")
MAPI_BASEURL.autoURL()

Material.STEEL("A992", "ASTM(S)", "A992")
Section.DB("W8x35", "H", "AISC", "W8x35", id=1)

Node(0, 0, 0, id=1); Node(6, 0, 0, id=2)
Element.Beam(1, 2, mat=1, sect=1, id=1)
Boundary.Support(1, "fix")

Load_Case("D", "Dead")
Load.SW("Dead", "Z", -1)

Model.create()                   # single batched push of everything above
```

---

## 10. The Python library architecture

The official libraries (`midas_civil`, `midas_gen`) are a thin, ergonomic layer
over the raw REST API. Understanding their shape clarifies the whole API.

### Low-level: one function

Everything bottoms out in:

```python
MidasAPI(method, command, body)   # e.g. MidasAPI("PUT", "/db/NODE", {...})
```

which sets `url = base_url + command`, attaches the `MAPI-Key` header, and issues
the matching `requests.{post,put,get,delete}` call.

### High-level: in-memory registries + one batched push

Instead of sending a request per object, the library uses **class-level
registries**. You construct objects in Python (they self-register), then push
**everything at once**:

```
 Node(...)        ─┐
 Element.Beam(...) ├─► accumulate in Node.nodes / Element.elements / ...
 Material.STEEL(...)│
 Load.SW(...)     ─┘
                     Model.create()  ──►  one PUT per table (NODE, ELEM, MATL, …)
```

Key classes (same names in both libraries):

| Concept | Class / call | Endpoint it writes |
|---------|--------------|--------------------|
| Node | `Node(x,y,z,id=…)` | `/db/NODE` |
| Element | `Element.Beam(i,j,…)`, `.Truss`, `.Plate`, `.Wall`, `.Solid` | `/db/ELEM` |
| Material | `Material.STEEL/CONC/USER(…)` | `/db/MATL` |
| Section | `Section.DB(…)`, `Section.DBUSER(…)`, `Section.Tapered(…)` | `/db/SECT` |
| Thickness | `Thickness(…)` | `/db/THIK` |
| Support | `Boundary.Support(node, "fix")` | `/db/CONS` |
| Links | `Boundary.RigidLink/ElasticLink(…)` | `/db/RIGD`, `/db/ELNK` |
| Group | `Group(…)`, `Group.Load/Boundary(…)` | `/db/GRUP`, … |
| Load case | `Load_Case(type, *names)` | `/db/STLD` |
| Self weight | `Load.SW(case, dir, factor)` | self-weight body force |
| Beam load | `Load.Beam(elems, case, value, dir)` | beam (element) load |
| Nodal load | `Load.Nodal(node, case, FZ=…)` | nodal load |
| Push all | `Model.create()` | batched PUTs |
| Wipe Python state | `Model.clear()` | *(memory only)* |

Helpers: `getID(obj)`, `getNodeID(obj)` return assigned ids; `Model.Select.Box(p1,p2)`
selects nodes/elements within a box.

> **Important distinction:** `Model.clear()` clears the **Python registries only**.
> To wipe the **live model**, you must `DELETE` the tables over the API (see §12).

---

## 11. Running analysis and reading results

```python
MidasAPI("POST", "/doc/ANAL")                 # run the solver (blocks until done)

# results table: e.g. reactions / displacements / member forces
res = MidasAPI("POST", "/post/TABLE", { ...table request... })
```

`/ope/UTBLTYPES` lists which result-table types the current model exposes, which
you use to form the `/post/TABLE` request. Results come back as JSON rows you can
load straight into pandas/Polars.

---

## 12. Deleting / clearing model data

A `DELETE` on a `/db` table **wipes that whole table** in the live model:

```python
MidasAPI("DELETE", "/db/ELEM")   # remove all elements
MidasAPI("DELETE", "/db/NODE")   # remove all nodes
```

**Why this matters:** if you regenerate a model that reuses ids `1..N` without
clearing, the new objects collide with the old ones — a "frame crash". The safe
order is **dependents first**:

```
loads (BODF, BMLD, CNLD, STLD) → supports (CONS) → elements (ELEM) → nodes (NODE) → sections (SECT) → materials (MATL)
```

(That is exactly what this repo's `engine.clear_gen_model()` does before a rebuild.)

---

## 13. Plug-in architecture (Marketplace)

A **Plug-in** packages MAPI calls + math + a UI so a non-programmer can run a
workflow from a button. Distribution is through a **Marketplace** inside the
product.

```
   Plug-in (UI) ──► MIDAS in-product API bridge ──► open model
        ▲
        └─ packaged as a ZIP with icon.svg at the build-folder root,
           uploaded on the Marketplace "MyWork" tab (internal or public)
```

Mechanics:

- The host looks for **`icon.svg` at the top level of the build folder**.
- You **build** the front-end, **zip** the build (icon at the ZIP root), and
  upload it on the **MyWork** tab; choose **internal** (company) or **public**.
- Updates are immediate — users don't wait for a product release.

Marketplace areas: **Market Place** (MIDAS-provided), **Saved** (installed),
**MyWork** (your uploads), **Bookmarks**.

> The "in-product API bridge" is just the plug-in's webview making the **same
> HTTPS calls to the MAPI relay** that the Python library makes (with the
> `MAPI-Key` header). See **§14** for the full build guide — especially **§14.3**,
> the `#midas-controller` mount that gives your plug-in its **close button**.

---

## 14. Building a MIDAS plug-in (detailed)

> **MANDATORY pre-read:** [`To midas/README.md`](../plugins/PLUGIN_GUIDE.md) — the
> condensed Do/Don't, gotcha table, folder structure, and pre-upload checklist
> every agent must read before preparing a plug-in package. This section is the
> deep companion to it.
>
> A **complete, working** plug-in lives in this repo:
> [`To midas/wind-load-generator/`](https://github.com/konohatrong/midas_API/tree/b4155ac/To%20midas/wind-load-generator) (the
> ASCE 7-22 Wind Load Generator — `source/` is the bundle, `publish/` the release repo). This section is the hard-won field guide that
> built it — read it before making your own. Open items and the build script are
> in [`To midas/wind-load-generator/PLUGIN_NOTES.md`](../plugins/WIND_LOAD_GENERATOR_PLUGIN_NOTES.md).

### 14.1 What a plug-in *actually* is

A MIDAS plug-in is **NOT** a Python program. It is a **static web bundle**
(HTML + JS + CSS + assets) that MIDAS loads in an **embedded browser (webview)
panel** floating over the model. Consequences you must design around:

- **No server, no Python process** runs inside the plug-in. (Our tool reuses its
  validated Python via **Pyodide/WebAssembly** — see §14.6 — but that still runs
  *in the browser*.)
- It talks to the model the same way the Python library does: **HTTPS `fetch` to
  the MAPI relay** with the `MAPI-Key` header. There is no magic local bridge.
- The webview has a **restricted network policy** — it can reach the MIDAS relay,
  but external CDNs may be blocked (see §14.6, §14.8).

### 14.2 Required files & ZIP layout

```
your-plugin/                 ← zip THIS folder; folder name must be unique
├── icon.svg                 ← REQUIRED, at the build-folder/ZIP root
├── index.html               ← entry point MIDAS loads in the webview
├── manifest.json            ← REQUIRED for the panel icon/title — must follow the
│                              official template's EXACT schema (see §14.8)
├── favicon.ico              ← the icon manifest.json points at
├── readme.md                ← shown as the plug-in description
└── (your js/css/assets…)
```
Build → zip the folder (icon at the ZIP root) → upload on the Marketplace
**MyWork** tab (internal or public). Updates are immediate.

### 14.3 ⭐ Making the plug-in closeable (the `#midas-controller` mount)

This is the single most important and least-obvious piece. **The plug-in does
not draw its own close/exit button — MIDAS does.** MIDAS injects its panel chrome
(the **title bar, drag handle, and ✕ close button**) into a specific element:

```html
<body>
  <!-- MIDAS injects its title bar + ✕ close button into this div -->
  <div id="midas-controller"></div>

  <!-- your app content goes below -->
  ...
</body>
```

Rules that follow from this:

- **You MUST include `<div id="midas-controller"></div>`** (typically the first
  element in `<body>`). Without it there is **no close button** and the panel
  can't be exited from inside.
- **Do NOT roll your own exit.** `window.close()` does **nothing** in the webview;
  a custom button that merely hides your content leaves MIDAS's **opaque webview
  background covering the model** (a black box). Let MIDAS own the chrome.
- **Leave room for the bar.** MIDAS's injected controller overlays the top of the
  page, so push your content down or it hides behind the bar:
  ```css
  body { padding-top: 54px; }   /* clear MIDAS's controller bar */
  ```
  (Our plug-in also measures the controller height at runtime and adjusts, with
  54px as the default.)
- The bar's **title** comes from the document `<title>` (or a manifest — see
  §14.8). Don't duplicate a big `<h1>` of the same name in your body.

### 14.4 Getting the key & talking to the model from JS

MIDAS launches the plug-in URL with **context in the query string** (the official
iframe plug-ins forward `window.location.search` to their hosted app). So you can
often **auto-fill the MAPI-Key** instead of asking the user to paste it:

```js
const p = new URLSearchParams(location.search);
console.log("MIDAS query params:", Object.fromEntries(p));   // discover the names
// pre-fill from common names (confirm the exact ones from the log above):
const key = p.get("mapiKey") || p.get("key") || /* … */ "";
```

Then call the model with a tiny `fetch` wrapper (the JS equivalent of the Python
`MidasAPI`). Probe regional base URLs and confirm with `/ope/PROJECTSTATUS`:

```js
const REGIONAL = [
  "https://moa-engineers-kr.midasit.com:443/gen",
  "https://moa-engineers.midasit.com:443/gen",
  "https://moa-engineers-us.midasit.com:443/gen", /* …in, gb */ ];
let BASE = null, KEY = null;

async function mapi(method, cmd, body) {
  const r = await fetch(BASE + cmd, {
    method,
    headers: { "Content-Type": "application/json", "MAPI-Key": KEY },
    body: body ? JSON.stringify(body) : undefined,
  });
  const j = await r.json().catch(() => ({}));
  if (j && j.error) throw new Error(j.error.message || "API error");
  return j;
}
async function connect(key) {                       // returns the working base URL
  KEY = key;
  for (const u of REGIONAL) {
    BASE = u;
    try { if ((await mapi("GET", "/ope/PROJECTSTATUS")).PROJECTSTATUS) return u; }
    catch (e) {}
  }
  throw new Error("Could not reach GEN NX — open it, enable the API, refresh the key.");
}
```
From here it's plain MAPI: `GET /db/NODE|ELEM|GRUP|UNIT`, `PUT /db/STLD|BMLD|GRUP`,
etc. — exactly the tables in §12 / the Appendix, just over `fetch`.

### 14.5 Two ways to build the app

1. **Thin iframe shell** (what MIDAS's own plug-ins do): `index.html` is a few
   lines that embed an `<iframe>` pointing at a **web app you host** (Streamlit/
   React on your server), forwarding `location.search`. Simple, but you must host
   and maintain a server and data leaves the machine.
2. **Self-contained bundle** (what this repo does): everything ships in the ZIP
   and runs in the webview. No hosting, nothing leaves the machine. See §14.6.

The official template (`@midasit-dev/cra-template-moaui`) is **React + PyScript +
moaui** — i.e., Python-in-the-browser is a *supported* pattern, which is why the
self-contained approach below works.

### 14.6 Self-contained, reusing validated Python (Pyodide)

Re-implementing engineering math in JS is risky. Instead, run the **same validated
Python** in the browser with **Pyodide** (CPython on WebAssembly), and use JS only
for the HTTP:

```
index.html ──loads──► Pyodide (WASM)  ──runs──►  windload_pkg.zip (pure Python:
     │                                            asce7/geometry/loads/classify…)
     └── JS MAPI (fetch) ◄── payloads ◄── Python builds /db JSON; JS PUTs it
```
Pattern:
- Bundle the **pure** modules (no `midas_gen`, stdlib only) as `windload_pkg.zip`;
  `pyodide.unpackArchive(buf, "zip")` into the FS, then `import` them.
- Python takes raw `/db` JSON in and returns JSON payloads out; **role maps and
  objects never cross to JS** — only plain JSON does.
- **Bundle Pyodide locally** in the ZIP (`pyodide/` ≈ 13 MB) and
  `loadPyodide({ indexURL: "./pyodide/" })`. The webview blocked the jsDelivr CDN,
  so a CDN-only load fails with `TypeError: Failed to fetch`. Keep a CDN fallback
  and **report which step failed** so you can tell a network issue from a code one.

[`build_plugin.py`](https://github.com/konohatrong/midas_API/blob/b4155ac/pilot%20project/wind%20load%20generator/build_plugin.py)
automates all of this (downloads Pyodide if missing, zips the package, packs the
upload zip with `icon.svg` at the root).

### 14.7 Engine pattern (for a *generate* plug-in)

If your plug-in also builds geometry (not just reads it), follow the desktop
pattern, but emit **raw `/db` JSON** from Python and `PUT` it from JS:
- **Connect** → `MAPI-Key` + base URL, confirm `/ope/PROJECTSTATUS`.
- **Clear** → §12 DELETE sequence to avoid id collisions.
- **Build** → nodes/elements/sections/supports with **deterministic ids** so loads
  can target roles.
- **Loads** → load cases + beam/nodal loads (one `PUT` per `/db` table; build the
  payload purely, then PUT — don't rely on stateful library buffers).
- **Analyze** (optional) → `/doc/ANAL`, then read `/post/TABLE`.

Follow [`docs/CONVENTIONS.md`](CONVENTIONS.md) for the full checklist (API,
packaging, FEA flow); a runnable FEA example is in
[`examples/analyze_and_report.py`](../examples/analyze_and_report.py).

### 14.8 Gotchas — what does **not** work (learned the hard way)

| Symptom | Cause | Fix |
|---|---|---|
| No exit / can't close | Missing `#midas-controller` | Add `<div id="midas-controller"></div>` (§14.3) |
| ✕ leaves a black box | Custom close just hid content; webview bg is opaque | Use MIDAS's controller close, not your own |
| Content hidden under the bar | Controller overlays the top | `body { padding-top: 54px }` |
| `TypeError: Failed to fetch` / "no internet connection" on load | Webview blocked an external CDN, or a malformed `manifest.json` | **Bundle Pyodide/jsPDF locally** with static `<script>` tags; fix the manifest (below) |
| `ol-icon-image` text instead of icon | No `manifest.json` (or its icon file missing) | Ship the template-schema manifest + `favicon.ico` (below) |
| Plug-in won't load at all | `manifest.json` in a **custom** schema | Use the official template's **exact** schema (below) |

**`manifest.json` — SOLVED (v2.0.0; fully confirmed in MIDAS 2026-06-11: loads
cleanly AND the panel icon renders, no `ol-icon-image` placeholder).** The host
parses `manifest.json` and expects the EXACT schema of the official
`@midasit-dev/cra-template-moaui` template's `public/manifest.json`:
```json
{ "short_name": "...", "name": "...",
  "icons": [{ "src": "favicon.ico",
              "sizes": "64x64 32x32 24x24 16x16", "type": "image/x-icon" }],
  "start_url": ".", "display": "standalone",
  "theme_color": "#0f1726", "background_color": "#0f1726",
  "width": 800, "height": 900 }
```
`width`/`height` are MIDAS-specific (panel size). The icon must be a real
`favicon.ico` at the zip root, also linked in `<head>`. Custom schemas
(`"icon": "./x.png"`, `title`, `version`, png/svg icon arrays) make the plug-in
fail to load with misleading errors. **Rule: mirror the template's `public/`
layout exactly** — full story in
[`To midas/wind-load-generator/PLUGIN_NOTES.md`](../plugins/WIND_LOAD_GENERATOR_PLUGIN_NOTES.md).

### 14.9 Performance & robustness tips

- **Reuse, don't re-implement.** Pyodide lets you ship code that's already tested
  offline — the browser runs the *same* engine, so correctness travels with it.
- **One `PUT` per table, built purely.** Construct the full `{"Assign": {…}}`
  payload in code and PUT once; never depend on the Python library's class-level
  buffers (they leak across calls in a long-lived page).
- **Clamp/sanitise before sending.** Beam-load positions must be `0 ≤ D ≤ 1`;
  float noise (e.g. `-8e-17`) makes MIDAS reject the *whole* `PUT`
  (`Loading Point … incorrectly entered`). Clamp at the edge.
- **Be tag-aware on pull.** When the model already has Structure-Group tags, act
  **only** on tagged elements; fall back to geometry guessing **only** when nothing
  is tagged — otherwise you load unrelated members.
- **Non-destructive writes.** Merge into existing `/db/GRUP`, `/db/STLD` (keep the
  user's groups/cases); never blind-`PUT` a table you don't fully own.
- **Lazy-load the heavy bits.** Pyodide + WASM is ~13 MB; show a "loading engine…"
  state and only block the buttons that need it (geometry input/preview can render
  immediately).

---

## 15. Error handling & troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Auth / key errors on every call | Key blank, refreshed, or product restarted | Re-copy the key (Apps → API Settings → **Refresh**) |
| Connection refused / timeout | Product not running, or API not enabled | Open CIVIL/GEN NX; enable the API; check base URL/region |
| New model collides / duplicated objects | Re-pushed ids over an existing model | `DELETE` tables first (§12) |
| `UnicodeEncodeError` on import (Windows) | The Python lib prints a Unicode banner; console codepage can't encode it | Switch stdout to UTF-8 before import (this repo's `engine/__init__.py` does this) |
| 200 but object missing | Per-object error inside a 200 response | Inspect the JSON body, not just the status |

A cheap health check: `GET /ope/PROJECTSTATUS` — succeeds only when key + relay +
running product all line up.

---

## 16. Appendix: endpoint families

| Family | Purpose | Methods | Examples |
|--------|---------|---------|----------|
| `/db/*` | model database tables (~150) | POST/GET/PUT/DELETE¹ | `NODE`, `ELEM`, `MATL`, `SECT`, `CONS`, `STLD`, `LCOM`, `STAG`, `TDNA` |
| `/doc/*` | document & solver ops | POST | `ANAL`, `NEW`, `OPEN`, `SAVE`, `IMPORT`, `EXPORTMXT` |
| `/ope/*` | queries | GET/POST | `PROJECTSTATUS`, `UTBLTYPES` |
| `/post/*` | results | POST | `TABLE` |

¹ `UNIT` and `STYP` are GET/PUT only.

The **complete** list (≈176 commands, with the handling module for each) is in
[`MIDAS_CIVIL_NX_endpoints.csv`](ENDPOINTS_CIVIL.csv); grouped, annotated
tables are in [`MIDAS_CIVIL_NX_API_Reference.md`](ENDPOINT_REFERENCE.md).

> Sourced from the official MIDAS Python libraries
> (`MIDASIT-Co-Ltd/midas-civil-python`, `midas-gen-python`) and MIDAS support
> documentation. Endpoint codes follow the MCT/MGT command vocabulary.

---

## 17. This repository

| Path | What |
|------|------|
| [`midas-gen-python/`](../lib/midas-gen-python/) | **MIDAS GEN NX** Python library (vendored from `MIDASIT-Co-Ltd/midas-gen-python`). The one your plug-in code uses. |
| [`midas-civil-python/`](https://github.com/konohatrong/midas_API/tree/b4155ac/midas-civil-python) | **MIDAS CIVIL NX** Python library (vendored from `MIDASIT-Co-Ltd/midas-civil-python`). Reference / comparison. |
| [`MIDAS_CIVIL_NX_API_Reference.md`](ENDPOINT_REFERENCE.md) | Grouped, annotated MAPI endpoint reference. |
| [`MIDAS_CIVIL_NX_endpoints.csv`](ENDPOINTS_CIVIL.csv) | All ~176 endpoints as CSV (family, code, command, handler module). |

> A complete **plug-in** lives in [`To midas/wind-load-generator/`](https://github.com/konohatrong/midas_API/tree/b4155ac/To%20midas/wind-load-generator)
> (ASCE 7-22 Wind Load Generator) — see §14 for how it's built and packaged.
> (The vendored libraries are MIT-licensed; their `LICENSE` files are included.)

### Quick start (the library)

```powershell
pip install midas-gen          # the GEN NX API library (PyPI)
```
```python
from midas_gen import *
MAPI_KEY("<your key>"); MAPI_BASEURL.autoURL()   # key: GEN NX → Apps → API Settings → Refresh
Node(0, 0, 0, id=1); Node(6, 0, 0, id=2)
Model.create()                                   # two nodes appear in GEN NX
```

### Notes

- **MAPI-Key** comes from GEN NX → Apps → API Settings → Refresh; never commit it.
- Targets **MIDAS GEN NX** (`/gen`); the Civil library/reference applies to the
  sibling NX product.
