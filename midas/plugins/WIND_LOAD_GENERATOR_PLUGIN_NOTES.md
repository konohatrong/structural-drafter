# Wind Load Generator — MIDAS plug-in: notes & future work

> **Copied** from [`konohatrong/midas_API`](https://github.com/konohatrong/midas_API/blob/b4155ac/To%20midas/wind-load-generator/PLUGIN_NOTES.md) (`To midas/wind-load-generator/PLUGIN_NOTES.md`, commit b4155ac, 2026-10-04) into this repository's `midas/` folder. Paths in the text such as `To midas/…`, `pilot project/…` or the root `README.md` name that repository; the map is in [`midas/README.md`](../README.md).

This folder holds the **MIDAS GEN NX plug-in** build of the Wind Load Generator.
The engineering is identical to the desktop tool (`pilot project/wind load
generator/`); only the delivery differs.

## What it is
A **self-contained web plug-in** (no server):
- **`index.html`** — UI + a JS **MAPI layer** (`fetch` to the GEN NX relay) +
  **Pyodide** bootstrap.
- **`windload_pkg.zip`** — the validated `windload` Python package (pure compute:
  asce7 / geometry / loads / classify / members / payload / plugin). Pyodide runs
  it **in the browser**, so the ASCE math is the same tested code as the desktop
  tool (95+ offline tests).
- **`pyodide/`** — Pyodide runtime, bundled locally (the MIDAS webview was unable
  to fetch it from the jsDelivr CDN; loader falls back to CDN if local is missing).
- **`icon.svg`** — plug-in icon (required at the zip root).
- **`readme.md`** — marketplace description.

Scope = the **existing-model workflow**: Connect → Create/Refresh tagging groups →
Preview → Apply. Loads go only to TAGGED elements. Gable / unequal-pitch gable /
monoslope are auto-detected; meshed (subdivided) members are handled.

## Build / publish workflow

**Every file lives in exactly ONE place.** `To midas/` is the home for plug-ins
— **one self-contained folder per plug-in** (a future plug-in gets its own
sibling folder with the same `source/` + `publish/` shape):
```
To midas/
└── wind-load-generator/         everything about THIS plug-in
    ├── PLUGIN_NOTES.md          dev notes (this file, main repo)
    ├── source/                  the upload bundle — mostly GENERATED (v2.1.0+)
    │     tracked:   manifest.json, icon.svg, readme.md
    │     generated: index.html + app.css + app.js + adapter-plugin.js (from the
    │                SHARED UI in "pilot project/wind load generator/ui/" via
    │                make_ui.py), favicon.ico, pyodide/, vendor/, windload_pkg.zip
    └── publish/                 release repo (own git; main ignores
        │                        "To midas/*/publish/")
        ├── releases/<date>_vX.Y.Z/   the upload zips — built DIRECTLY here,
        │                             one folder per VERSION (named by first
        │                             publish date; rebuilds reuse the folder)
        └── validation/               VALIDATION.md + live campaign logs
```

**ONE UI, two targets (v2.1.0).** The desktop GUI and the plug-in are generated
from the SAME source — `pilot project/wind load generator/ui/`:
`index.template.html` (form/markup, capability-gated via `data-cap`) +
`app.css` + `app.js` (all logic, talks only to `window.Backend`) + two thin
adapters (`adapter-server.js` = FastAPI fetches; `adapter-plugin.js` = MAPI
fetch + Pyodide + jsPDF). `make_ui.py` assembles both outputs; `build_plugin.py`
and the dev server's startup call it automatically. **Edit only `ui/`** — a
feature added once appears in BOTH targets, so feature drift between localhost
and the packed plug-in is structurally impossible.
```
cd "pilot project/wind load generator"
run_local_check.bat             # all offline checks must pass first
python build_plugin.py          # -> publish/releases/<date>_vX.Y.Z/*.zip
```
`build_plugin.py` downloads Pyodide + jsPDF if missing, renders favicon.ico,
zips the `windload` source, writes the versioned upload zips straight into the
release folder, and refreshes `publish/validation/`. It also removes legacy
duplicates (loose zips at the To midas/publish roots, the old `publish/plugin/`
mirror) if it finds any.

**Publish repo:** `To midas/wind-load-generator/publish/` is gitignored by the
MAIN repo (`To midas/*/publish/`) and is versioned in its **own** git repo
(release artifacts only). Cycle:
1. develop on the main repo (this engine + UIs), tests green;
2. bump `VERSION` in `build_plugin.py`, run it;
3. update `publish/CHANGELOG.md`, commit/push the publish repo;
4. upload `wind-load-generator-vX.Y.Z.zip` on MIDAS → MyWork.

## Verified working
- Loads in the MIDAS webview; engine ready (Pyodide local).
- **Icon renders in the panel** (v2.0.0 manifest + favicon.ico — confirmed in
  MIDAS 2026-06-11; no more `ol-icon-image` placeholder).
- **Close**: provided by MIDAS via `<div id="midas-controller"></div>` (MIDAS
  injects its own title bar + ✕). Body has `padding-top` so content clears it.
- Connect / Create-groups (non-destructive) / Preview all verified live on a real
  348-element model; Full-set Apply (58 cases / 2420 loads) verified live too.

## ✅ CASE CLOSED: the manifest / icon / "no internet" saga (v2.0.0)

**Fully confirmed in MIDAS GEN NX, 2026-06-11:** plug-in loads, engine boots,
AND the panel icon renders correctly — the `ol-icon-image` placeholder is gone.

**Symptoms over time** (all the same root cause):
1. Controller icon showed the `ol-icon-image` placeholder (no manifest shipped).
2. Adding a manifest made the plug-in **fail to load entirely** (twice).
3. One upload reported **"no internet connection"** at startup.

**Root cause.** MIDAS's plug-in host parses `manifest.json` and expects the
EXACT schema used by the official `@midasit-dev/cra-template-moaui` template's
`public/manifest.json`. Our earlier manifests used a custom schema
(`"icon": "./icon.png"`, `title`, `version`, png/svg icons array) → the host
choked → no icon / failed load / misleading network error.

**The fix (v2.0.0) — copy the template, exactly:**
```json
{ "short_name": "...", "name": "...",
  "icons": [{ "src": "favicon.ico",
              "sizes": "64x64 32x32 24x24 16x16", "type": "image/x-icon" }],
  "start_url": ".", "display": "standalone",
  "theme_color": "#0f1726", "background_color": "#0f1726",
  "width": 800, "height": 900 }
```
- `width`/`height` are **MIDAS-specific** (the plug-in panel size) — keep them.
- The icon must be a real **`favicon.ico`** at the zip root (generated by
  `build_plugin.py:ensure_favicon()`), linked in `<head>` via
  `<link rel="icon" href="./favicon.ico"/>`.
- Load heavy JS (Pyodide, jsPDF) with **static `<script>` tags in `<head>`**,
  bundled in the zip — the template style; never depend on a CDN at runtime.

**How to follow for any new plug-in:** scaffold with
`npx create-react-app my-app --template @midasit-dev/cra-template-moaui` and
mirror its `public/` layout (index.html head, manifest.json schema, favicon.ico,
`<div id="midas-controller">` for the close bar). Deviate from the template's
file conventions and the host fails in non-obvious ways.

## Open items / future work

2. **Auto MAPI-Key from query params.**
   MIDAS passes context to the plug-in via URL query params (the official iframe
   plug-ins forward `window.location.search`). `index.html` already (a) logs
   `MIDAS query params: {…}` to the console and (b) pre-fills the key for common
   param names. TODO: capture the **actual param names** from a real MIDAS run
   (read the console log) and finalize auto key + auto-connect (skip manual paste);
   also prefer the MIDAS-provided base URL (`window.__MIDAS_BASE`).

3. **Generate-new-model path is desktop-only.**
   The plug-in does the existing-model (tag→assign) workflow. Generating a fresh
   frame needs material/section/node/element creation payloads (the MATL/SECT JSON
   schemas). Add pure builders for those if the plug-in should also generate.

4. **Production gate (applies to desktop + plug-in).**
   ASCE 7-22 output is engineering-critical: needs an independent licensed-engineer
   review and ideally a second published-example validation (only G3-1 so far).

## How to capture diagnostics in MIDAS
If anything misbehaves, right-click → Inspect the plug-in panel (if available) and
copy: any red console errors, and the `MIDAS query params: {…}` line. The boot
also reports the failing step, e.g. `Engine failed at [windload_pkg.zip]: …`.
