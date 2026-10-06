# Building MIDAS Plug-ins — READ THIS FIRST

> **Copied** from [`konohatrong/midas_API`](https://github.com/konohatrong/midas_API/blob/b4155ac/To%20midas/README.md) (`To midas/README.md`, commit b4155ac, 2026-10-04) into this repository's `midas/` folder. Paths in the text such as `To midas/…`, `pilot project/…` or the root `README.md` name that repository; the map is in [`midas/README.md`](../README.md).

**Every agent (human or AI) must read this file before preparing a MIDAS plug-in
package.** It is the distilled, field-tested knowledge from building and shipping
the Wind Load Generator plug-in (v2.0.0, confirmed working in GEN NX) — every
rule below was paid for with a real failure. The deep build guide is root
[`README.md` §14](../api/MAPI_GUIDE.md#14-building-a-midas-plug-in-detailed); per-plugin
history lives in each plug-in's `PLUGIN_NOTES.md`.

---

## 1. Facts — what a MIDAS plug-in actually is

- A plug-in is a **static web bundle** (HTML/JS/CSS + assets) zipped and uploaded
  on MIDAS Marketplace → MyWork. MIDAS serves it **locally** inside a Chromium
  **webview panel** in GEN NX / CIVIL NX. There is **no server side** — if you
  need compute, it runs in the browser (see Pyodide technique, §6).
- MIDAS **injects its own title bar** (drag + ✕ close) into
  `<div id="midas-controller"></div>` — you do NOT implement close/drag yourself.
  `window.close()` does nothing in the webview.
- The plug-in talks to the model via **MAPI over HTTPS**
  (`https://moa-engineers.midasit.com:443/gen` + `MAPI-Key` header) — the cloud
  relay forwards to the MIDAS app open on the same PC. Plain `fetch()` works.
- MIDAS passes context (key, base URL) via **URL query params** — log
  `window.location.search` to discover the actual names.
- The webview **blocks external CDNs** unreliably. Anything you need at runtime
  must be **inside the zip**.
- The host **parses `manifest.json` strictly** (panel icon, title, size). Wrong
  schema = plug-in fails to load with **misleading** errors (§5 case study).

## 2. Where to build — folder structure (one folder per plug-in)

```
To midas/
├── README.md                    ← this guide
└── <plugin-name>/               ← EVERYTHING about one plug-in, self-contained
    ├── PLUGIN_NOTES.md          dev notes: decisions, open items, case history
    ├── source/                  the upload bundle — mostly GENERATED
    │   ├── index.html           GENERATED from the shared ui/ (see below)
    │   ├── app.css/app.js/adapter-plugin.js   GENERATED shared UI files
    │   ├── manifest.json        EXACT template schema (§3) — tracked
    │   ├── icon.svg             marketplace icon, required at zip root — tracked
    │   ├── readme.md            marketplace description — tracked
    │   └── (generated, gitignored: favicon.ico, pyodide/, vendor/, *_pkg.zip)
    └── publish/                 release repo — its OWN git (main repo ignores
        │                        "To midas/*/publish/")
        ├── README.md            public-facing: features, load-case reference, V&V
        ├── CHANGELOG.md         one entry per version
        ├── releases/<first-publish-date>_vX.Y.Z/   the upload zips — built
        │                        DIRECTLY here; ONE folder per VERSION (rebuilds
        │                        reuse it; new folder only on version bump)
        └── validation/          evidence (VALIDATION.md + live campaign logs)
```

Rules of the layout:
- **Every file exists in exactly ONE place.** No unzipped mirror of the bundle in
  `publish/` — the zips ARE the release artifact. No loose zips outside
  `releases/`.
- The **build script lives with the engine** (e.g. `pilot project/wind load
  generator/build_plugin.py`), not in `To midas/` — it pulls the validated source
  in, generates artifacts, zips, and syncs `publish/`.
- A new plug-in = a new sibling folder with the same `source/` + `publish/` shape.

**ONE UI, two targets — the anti-drift rule.** If the same tool also has a
desktop/localhost GUI, do NOT maintain two HTML files (features WILL drift —
learned the hard way). Keep one shared UI source (`ui/`: markup template +
`app.js` that talks only to a `window.Backend` interface) and two thin adapters
(server-fetch vs MAPI+Pyodide); an assembler (`make_ui.py`) generates both
outputs. Capability differences (e.g. generate-path is desktop-only) are
declared by the adapter (`Backend.can.*`) and gated in markup with `data-cap`
attributes — never by forking the page.

## 3. The required file set (zip root)

| File | Why | Tracked? |
|---|---|---|
| `index.html` | the app; `<div id="midas-controller">` in body; `body{padding-top:~54px}` to clear MIDAS's injected bar | yes |
| `manifest.json` | panel icon/title/size — **EXACT schema below, no deviation** | yes |
| `favicon.ico` | the icon `manifest.json` points at; also `<link rel="icon" href="./favicon.ico"/>` in head | generated |
| `icon.svg` | marketplace listing icon, must be at zip root | yes |
| `readme.md` | marketplace description | yes |
| runtime libs (`pyodide/`, `vendor/`…) | the webview blocks CDNs — bundle everything | generated |

**The one true `manifest.json` schema** (from the official
`@midasit-dev/cra-template-moaui` template — copy it field-for-field):
```json
{ "short_name": "Plug-in Name", "name": "Plug-in Name",
  "icons": [{ "src": "favicon.ico",
              "sizes": "64x64 32x32 24x24 16x16", "type": "image/x-icon" }],
  "start_url": ".", "display": "standalone",
  "theme_color": "#0f1726", "background_color": "#0f1726",
  "width": 800, "height": 900 }
```
`width`/`height` are **MIDAS-specific** (panel size in px) — keep them.

## 4. Do / Don't

| ✅ Do | ❌ Don't |
|---|---|
| Mirror the official template's `public/` layout **exactly** (`npx create-react-app my-app --template @midasit-dev/cra-template-moaui`) | Invent your own manifest fields (`"icon"`, `"title"`, `"version"`, png/svg icon arrays) — the host chokes with unrelated-looking errors |
| Load heavy JS (Pyodide, jsPDF…) with **static `<script>` tags in `<head>`**, files bundled in the zip | Depend on a CDN at runtime (jsDelivr/cdnjs get blocked → "Failed to fetch" / "no internet connection") |
| Let MIDAS own close/drag via `#midas-controller` | Build your own ✕ button or window chrome (`window.close()` is a no-op; custom frames leave black boxes) |
| Keep compute in a **pure, unit-tested package** and run the SAME code in the browser (Pyodide) and on the desktop | Re-implement engineering math in JS — two sources of truth WILL diverge |
| Share ONE UI source between desktop and plug-in (Backend-adapter pattern, §2) | Maintain a second hand-ported index.html — every release will "miss some feature from local" |
| Write to the model **non-destructively**: GET existing → merge your own cases only → PUT | Blind `PUT`/`DELETE` on `/db/BMLD`, `/db/GRUP`, `/db/STLD` — you will wipe the user's Dead/Live/EQ loads or their group structure |
| **Chunk large PUTs** (≤ ~1500 items per request) | One huge PUT — MIDAS **silently drops it** (no error, loads just missing) |
| Clamp/sanitize numerics (e.g. relative distance D to [0,1] — float noise like `-8e-17` is **rejected**, failing the WHOLE payload) | Trust raw floating-point output in payloads |
| Give the boot sequence **step labels** ("Engine failed at [pyodide.js]: …") | A bare spinner — in-MIDAS debugging is nearly blind without step reporting |
| Version with `VERSION` in the build script; ship zips named `…-vX.Y.Z.zip` into the dated release folder | Hand-zip folders ad hoc; keep multiple copies of the same artifact |
| Build a `-no-manifest` fallback zip alongside (insurance against host changes) | Assume the host behaves the same across MIDAS versions |

## 5. Gotchas — symptom → root cause → fix

| Symptom in MIDAS | Root cause | Fix |
|---|---|---|
| `ol-icon-image` text instead of the panel icon | no `manifest.json` (or icon file missing) | template-schema manifest + `favicon.ico` (§3) |
| Plug-in **fails to load entirely** | `manifest.json` in a custom schema | use the EXACT template schema |
| **"No internet connection"** at startup | runtime fetch of a blocked CDN, or a malformed manifest | bundle libs locally + static script tags; fix manifest |
| `TypeError: Failed to fetch` during boot | webview blocked jsDelivr/cdnjs | bundle Pyodide/jsPDF in the zip |
| Exit button does nothing / black box remains | `window.close()` no-op; custom chrome conflicts with host | delete custom chrome; `#midas-controller` only |
| Loads applied but some elements silently missing | single huge `/db/BMLD` PUT | chunk ≤1500 items |
| "Loading Point has(have) been incorrectly entered" — whole PUT rejected | one degenerate item (e.g. D = `-8e-17`) poisons the batch | clamp D to [0,1], skip zero-length segments |
| User's existing loads/groups vanished | destructive PUT replaced the table | GET → merge (only your own case names) → PUT |
| Plug-in worked locally, breaks uploaded | relative paths / files not at zip ROOT | zip the *contents* of `source/` (files at root), verify the content listing |

**Case study (the manifest saga — found → fixed).** Three different symptoms
over days (placeholder icon; total load failure; "no internet connection") were
ONE root cause: our hand-written `manifest.json` didn't match the host's
expected schema. Found by reading the official template's `public/manifest.json`
on disk instead of guessing. Fixed by copying it field-for-field (incl. the
undocumented `width`/`height`). Lesson: **when the host misbehaves, diff your
bundle against the official template before debugging your own code.**

## 6. Techniques that work

- **Pyodide pattern** — zip the pure Python package (`*_pkg.zip`), bundle the
  Pyodide runtime (5 core files), boot with a static script tag, then
  `unpackArchive` + import. The browser runs the *same tested code* as the
  desktop tool. Keep the package import-clean of any desktop-only deps
  (verify: `import <pkg>` must not pull `midas_gen` — gate it in CI).
- **JS↔Python bridge** — tiny `py*` wrapper functions taking/returning JSON
  strings; all MAPI `fetch` stays in JS (Pyodide can't do native sockets).
- **In-plug-in PDF** — build the report data in Python (one source of truth),
  render with bundled jsPDF + autotable; `doc.save()` triggers the download.
- **Boot diagnostics** — wrap each boot step, surface `Engine failed at [step]`.
- **Local-first, CDN-fallback** — static local tag; only if
  `typeof loadPyodide === 'undefined'` try the CDN.
- **Self-cleaning build** — the build script removes legacy duplicates (loose
  zips, old mirrors) so layout drift heals itself.

## 7. Pre-upload checklist (run every time)

1. `run_local_check.bat` — full offline gate (tests, Pyodide-import safety,
   bundle build) must PASS.
2. `python build_plugin.py` — read the printed **zip content listing**; confirm
   `index.html / manifest.json / favicon.ico / icon.svg / readme.md` at root
   (the script asserts this) and the release folder is `releases/<date>_vX.Y.Z/`.
3. Serve `source/` locally, open in a browser: engine boots, no console errors.
4. Upload the versioned zip (MIDAS → Marketplace → MyWork).
5. In MIDAS: icon renders (no `ol-icon-image`), panel opens, ✕ closes, boot says
   ready; run one end-to-end action against a **scratch model** first.
6. Update `publish/CHANGELOG.md`; commit/push the publish repo.

## 8. Pointers

- Deep guide: root [`README.md` §14](../api/MAPI_GUIDE.md#14-building-a-midas-plug-in-detailed)
  (webview anatomy, close mechanism, Pyodide engine pattern, performance tips).
- Worked example: [`wind-load-generator/`](https://github.com/konohatrong/midas_API/tree/b4155ac/To%20midas/wind-load-generator) — source,
  notes ([`PLUGIN_NOTES.md`](WIND_LOAD_GENERATOR_PLUGIN_NOTES.md)), publish repo.
- Official scaffold: `npx create-react-app my-app --template @midasit-dev/cra-template-moaui`.
- MAPI reference: root README §1–§9 + `MIDAS_CIVIL_NX_endpoints.csv`.
