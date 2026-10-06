# Fire Station (Building B) — Reference Scripts

> **Copied** from [`konohatrong/midas_API`](https://github.com/konohatrong/midas_API/tree/b4155ac/modeling-guide/scripts/fire_station) (`modeling-guide/scripts/fire_station/`, commit b4155ac, 2026-10-04) into this repository's `midas/` folder, unchanged except this note. Paths such as `pilot project/…` name that repository; the map is in [`midas/README.md`](../../../README.md). The live scripts `chdir` to the wind-load-generator folder of that repository to import `windload.midas.connection.connect`; the same function is [`midas/tools/connection.py`](../../../tools/connection.py) here. To run a script from this repository, replace its `os.chdir(...)` / `sys.path.insert(0, "src")` lines with `sys.path.insert(0, r"<repo>\midas	ools")` and import `from connection import connect`.

The scripts that built the Samut Songkhram fire-station model in the live MIDAS GEN NX, plus
the check and report scripts for Buildings A and B (2026-09-23/24). They are the reference
implementation of the guides in [`modeling-guide/`](../../README.md). They are archived as they
ran, project values included; they are **not** a packaged tool yet.

> **MAPI key.** Every live script takes the key as its **first command-line argument** and
> never stores it. Do not add it to any file.

## Setup

| Item | Value |
|---|---|
| Python packages | `ezdxf`, `matplotlib`, `PyMuPDF` (`fitz`), `python-docx`, `Pillow`, `polars`, `midas_gen` |
| MIDAS connection | Live scripts `chdir` to `pilot project/wind load generator` and import `windload.midas.connection.connect` from its `src/` |
| Working data folder | Set `MG_WORKDIR` to a folder for the JSON / PNG files the stages exchange (default: current directory) |
| Project inputs (hard-coded) | DXF `G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf`; report output under `C:\Workspace\##2026\20260917 - Samutsongkram\calculation report\` |

```bash
set MG_WORKDIR=C:\work\fire_station          # PowerShell: $env:MG_WORKDIR="C:\work\fire_station"
python 03_beams/prep_beams.py                  # offline stage: no key
python 03_beams/build_beams_level.py "<MAPI-KEY>" GB   # live stage: key first
```

## Run order

Offline scripts read the DXF and write JSON/PNG. **Live** scripts (key required) write to the
open MIDAS model; run them only after the level's review sheet is accepted.

| Stage | Script | Live | Produces / does |
|---|---|---|---|
| 01 intake | `dxf_review.py`, `dxf_text.py`, `dxf_titles.py` | | Layers, entities, texts, titles, level tags |
| | `dxf_render.py` | | `dxf_*.png` panel renders |
| 02 grid + columns | `dxf_grid_probe.py`, `dxf_grid_cols.py` | | Grid from the xref → `fs_gridcols.json` |
| | `dxf_cols_levels.py`, `dxf_colsize.py`, `dxf_colvis.py`, `dxf_cols_allfloors.py` | | Column sizes, offsets, tops per floor → `fs_cols_floors.json` |
| | `prep_columns.py` | | `fs_colmodel.json`, `fs_col_plan.png` |
| | `mksections_fs.py` | ✔ | Column sections 101–106 |
| | `build_columns.py` | ✔ | Material, nodes, column elements, supports, groups |
| 03 beams | `dxf_beam_probe.py`, `dxf_beams.py`, `plot_beams_raw.py` | | Raw centre-segments + marks → `fs_beams_raw.json` |
| | `prep_beams.py`, `plot_beams_model.py` | | Clean beam graph → `fs_beammodel.json` (copy to `fs_beammodel_withBX.json` before the next step) |
| | `revise_beams_noBX.py` | | BX removed, pieces merged, connectivity checked |
| | `plot_floor.py [L]` | | IDs assigned; review sheets `fs_beams_<L>.png` |
| | `mk_b2a.py` | ✔ | Section 209 B2A (copy of 207) |
| | `build_beams_level.py <KEY> <L>` | ✔ | One level: pre-checks → write → read-back |
| | `annex.py plot` / `annex.py build <KEY>` | ✔ (build) | Annex roof +3.95: sheet + checks / column split + beams |
| 04 curves | `gb_curve.py [n]` | | Curved GB corner as n chords (default 6) in `fs_beammodel.json`. Run it **before** `plot_floor.py`, which assigns the IDs |
| 05 verify | `verify_floor.py <L>` | | Independent 5-point check → `verify_<L>.json` |
| 06 slabs | `probe_mesh.py` | ✔ | Auto-mesh probe on a test panel |
| | `mk_thik.py` | ✔ | Thickness IDs 1–4 |
| | `slab_faces.py` | | Library: faces of the beam graph |
| | `slab_plot.py <L>`, `slab_plot_AR.py` | | Panel sheets `fs_slab_<L>.png` + `fs_slab_<L>.json` |
| | `slab_build.py <KEY> <L> [n\|a-b\|verify]` | ✔ | Mesh panels, verify, groups |
| | `redo_panel.py`, `fix_slabgb.py`, `panel_groups.py` | ✔ | Re-mesh one panel; group repairs |
| | `cap_slab.py`, `cap_all.py` | ✔ | `/view/CAPTURE` plan and iso views |
| 07 rooms + loads | `mk_loadcases.py` | ✔ | DL / SDL / LL cases, self-weight |
| | `rooms.py <KEY>` | ✔ (read) | Zone per plate → `fs_rooms.json`, `fs_rooms_<L>.png` |
| | `ll_plot.py [--en]` | | LL per regulation → `fs_LL.json`, `fs_LL_<L>(_en).png` |
| | `apply_LL.py`, `apply_SDL.py` | ✔ | `/db/PRES` on every plate |
| | `make_combos.py` | ✔ | Regulation combinations (GEN + CONC) |
| 08 rebar | `rebar_prep.py` | | Rebar payload from the schedules → `rchk_payload.json` |
| | `rebar_mct.py` | | Writes an MCT rebar block to a file only. **Do not import it** (see below) |
| 09 checks + report | `check_model.py`, `check_live.py` | ✔ (read) | Model state check via `/doc/EXPORTMXT` (read-only) |
| | `extract_B.py`, `compute_elf_B.py`, `capture_B.py`, `build_report_B.py` | ✔ | Building B report |
| | `check_A.py`, `extract_A.py`, `drift_A.py`, `capture_A.py`, `compute_elf.py`, `build_report_A.py` | ✔ | Building A report (reuses the B helpers) |

## Deliberately not archived

| Script | Why |
|---|---|
| `rebar_import.py`, `restore.py` | They call `/doc/IMPORTMXT`, which **replaced the whole open model** once. Never import an MCT into a live model through the API |
| `regroup_domains.py` | Domain tables are read-only through the API; it cannot work |
| `*_v1.py`, `patch_*.py`, `dbg*.py`, `probe_*.py` (except `probe_mesh.py`) | Superseded drafts and one-off debugging |

## Hard-coded project values to change for another building

Panel origins `O`/`PAN`, grid `GX`/`GY`, levels `LEV`/`Z`, column lists `C1`/`C2`/`EAST`,
section IDs `SEC`/`SECT`, level-specific fixes in `prep_beams.py`, the curve geometry in
`gb_curve.py` / `annex.py` / `verify_floor.py`, cantilever polygons `CANT` in `slab_plot.py`,
room zones in `rooms.py`. Moving these into one project config file is the next step towards
the Building Model Maker.
