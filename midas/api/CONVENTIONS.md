# Conventions for building a MIDAS tool

> **Copied** from [`konohatrong/midas_API`](https://github.com/konohatrong/midas_API/blob/b4155ac/docs/CONVENTIONS.md) (`docs/CONVENTIONS.md`, commit b4155ac, 2026-10-04) into this repository's `midas/` folder. Paths in the text such as `To midas/…`, `pilot project/…` or the root `README.md` name that repository; the map is in [`midas/README.md`](../README.md).

A checklist to follow when creating a new tool / plug-in in this repo. Grounded in
how MAPI works and the official `midas-gen` library. See the root
[`README.md`](MAPI_GUIDE.md) for the full architecture.

---

## A. API / engine conventions — *always*

1. **Connect first.** Set `MAPI-Key` + base URL (`MAPI_BASEURL.autoURL()` or the
   `/gen` URL). The desktop product must be **open**, API enabled, key fresh.
2. **Build in memory, push once.** Construct objects (`Node`, `Element`,
   `Material`, …) then a single `Model.create()`. Never one HTTP call per object.
3. **Respect dependency order:**
   `material/section → node → element → support → load case → load → analysis`.
   (Elements reference node/section ids; loads reference a load case.)
4. **Deterministic IDs.** Assign explicit, predictable ids (e.g. from grid
   position) so later steps can target objects without reading the model back.
5. **Clear before regenerate.** `DELETE` the tables you own in dependency order
   (`loads → CONS → ELEM → NODE → SECT → MATL`) so re-runs don't collide.
   ⚠️ `Model.clear()` clears **Python memory only**, not the live model.
6. **Offer a dry run.** Build + emit JSON **without** pushing, so the tool is
   testable with no GEN NX running.
7. **Units & signs.** Values follow the model's `/db/UNIT`. Gravity is **−Z**:
   downward loads and the self-weight factor are **negative**.
8. **Windows UTF-8 guard.** Reconfigure stdout/stderr to UTF-8 **before**
   importing `midas_gen` (it prints a Unicode banner that crashes some consoles).
9. **Check the body, not just the status.** A 200 can still carry a per-object
   error — inspect the JSON.
10. **Reuse the library.** Prefer `Section.DB`, `Boundary.Support`, `Load.Beam`…
    over hand-written JSON.

## B. Plug-in packaging — *only if shipping to the Marketplace*

11. **`icon.svg` at the top level of the build folder** (required by the host).
12. **Package the build as a single ZIP** (icon at the ZIP root).
13. **Upload on the MyWork tab**; choose **internal** (company) or **public**.

## C. Project conventions — *this repo*

14. **Never commit the MAPI-Key.** Keep it in `config.json` (git-ignored) or an
    env var (`MIDAS_MAPI_KEY`).
15. **Declare dependencies** in `requirements.txt` (`midas-gen`, …).
16. **Tests + dry run** for engine logic; **commit → push** for backup.
17. **Keep the key out of URLs/logs.** Header only.

---

## D. Does the tool need FEA (analysis)?

You never *implement* FEA — the **desktop product runs the solver**; the API only
**triggers** it and **reads results**.

| The tool's job | FEA needed? |
|---|---|
| Create geometry / materials / sections / supports / loads | ❌ No — just build & push |
| Edit / clean / organize / group the model | ❌ No |
| Report forces, displacements, reactions, stresses | ✅ Yes |
| Design checks, code checks, optimization (iterates on results) | ✅ Yes |

**Rule of thumb:** modeling + load-assignment tools do **not** need FEA. Add it
only when the tool must produce or act on *results*.

### The FEA workflow (when needed)

```
1) (optional) analysis controls   PUT /db/ACTL, /db/EIGV, /db/BUCK, /db/PDEL, /db/SMCT
2) run the solver                  POST /doc/ANAL          (Model.analyse())
3) read results                    POST /post/TABLE        (Result.Reaction/…)
   discover available tables with  GET  /ope/UTBLTYPES
```

Library helpers:
- **Controls:** `AnalysisControl.MainControlData / PDelta / Buckling / EigenValue / Settlement`
- **Run:** `Model.analyse()`  (or `MidasAPI("POST", "/doc/ANAL", {"Assign": {}})`)
- **Results:** `Result.Reaction(...)`, `Result.Displacement(...)`,
  `Result.BeamForce(...)`, `Result.TrussForce/Stress(...)`,
  `Result.UserDefinedTable(...)` with `TableOptions` → return DataFrames.

### Gotchas
- The model must be **complete and solvable** (supports + loads + a valid load
  case) or `/doc/ANAL` errors.
- In results, a static load case **`Dead`** is referenced as **`Dead(ST)`**.
- Read results **only after** a successful analyze; they're stale if the model
  changed.
- Analysis takes time and switches the product into post-processing mode — design
  the UX for a wait.

See [`../examples/analyze_and_report.py`](../examples/analyze_and_report.py) for a
runnable build → analyze → read-results example.
