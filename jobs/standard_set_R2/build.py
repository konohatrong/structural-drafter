"""
Standard set R2 (typical details, N.T.S. at a dummy 1:25; model space at real size) - build one set to DXF.

usage: python build.py <set>        set = columns | beams | slabs | all
    columns -> out/STR-ST-1101_Typical_Column_Details_A3_R2.dxf    (1101 - 1104)
    beams   -> out/STR-ST-1111_Typical_Beam_Details_A3_R2.dxf      (1111 - 1116)
    slabs   -> out/STR-ST-1121_Typical_Slab_Details_A3_R2.dxf      (1121 - 1128)
Also writes library/INDEX_<set>.csv (every block: detail, title block, view title, table, notes, key).
Output folders are fixed (next to this file) so a plot can never pick up a stale DXF.
Exit code 1 when the build finds a layout problem ("!!" lines) or the DXF audit reports an error; the DXF is
still written so the problem can be inspected.
Engine: drafter/td_engine.py (docs/general/DRAWING_ENGINE.md).   R2 rules: MODEL_SPACE_SHEETS.md
"""
import importlib
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")          # warnings quote ≥, ℓ, ≈ (the Windows console codepage cannot)
HERE = Path(__file__).resolve().parent
MODS = {"columns": "td_columns", "beams": "td_beams", "slabs": "td_slabs"}
SET = sys.argv[1] if len(sys.argv) > 1 else "all"
if SET != "all" and SET not in MODS:
    sys.exit(f"unknown set '{SET}': use {' | '.join(MODS)} | all")

if SET == "all":
    failed = [k for k in MODS
              if subprocess.run([sys.executable, str(HERE / "build.py"), k]).returncode]   # one document per process
    if failed:
        print("!! build failed:", ", ".join(failed))
    sys.exit(1 if failed else 0)

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))          # repository root: the drafter package (engine, pens)
mod = importlib.import_module(MODS[SET])
from drafter import td_engine                      # noqa: E402  (already loaded by the content module)

mod.build()
mod.finish()
doc = mod.doc
if "Layout1" in doc.layouts:
    doc.layouts.delete("Layout1")
for err in doc.audit().errors:
    td_engine.warn(f"DXF audit: {err.message}")
OUT, LIB = HERE / "out", HERE / "library"
OUT.mkdir(exist_ok=True)
LIB.mkdir(exist_ok=True)
DXF = OUT / f"{mod.BASE}.dxf"
doc.saveas(DXF)
mod.index_csv(LIB / f"INDEX_{SET}.csv")
print("saved", DXF, "|", len(mod.INDEX), "blocks indexed")
if td_engine.WARNINGS:
    print(f"!! {len(td_engine.WARNINGS)} layout problem(s) in {SET} - the DXF is saved for inspection, do not plot it")
    sys.exit(1)
