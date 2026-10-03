"""
Standard set R2 (typical details, N.T.S. at a dummy 1:25; model space at real size) - build one set to DXF.

usage: python build.py <set>        set = columns | beams | slabs | all
    columns -> out/STR-ST-1101_Typical_Column_Details_A3_RevA.dxf    (1101, 1102)
    beams   -> out/STR-ST-1111_Typical_Beam_Details_A3_RevA.dxf      (1111 - 1115)
    slabs   -> out/STR-ST-1121_Typical_Slab_Details_A3_RevA.dxf      (1121 - 1127)
Also writes library/INDEX_<set>.csv (every block: detail, title block, view title, table, notes, key).
Output folders are fixed (next to this file) so a plot can never pick up a stale DXF.
Engine: td_engine.py.   Guide: MODEL_SPACE_SHEETS.md
"""
import importlib
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")          # warnings quote ≥, ℓ, ≈ (the Windows console codepage cannot)
HERE = Path(__file__).resolve().parent
MODS = {"columns": "td_columns", "beams": "td_beams", "slabs": "td_slabs"}
SET = sys.argv[1] if len(sys.argv) > 1 else "all"

if SET == "all":
    for k in MODS:
        subprocess.run([sys.executable, str(HERE / "build.py"), k], check=True)   # one document per process
    sys.exit(0)

sys.path.insert(0, str(HERE))
mod = importlib.import_module(MODS[SET])
mod.build()
mod.finish()
doc = mod.doc
if "Layout1" in doc.layouts:
    doc.layouts.delete("Layout1")
OUT, LIB = HERE / "out", HERE / "library"
OUT.mkdir(exist_ok=True)
LIB.mkdir(exist_ok=True)
DXF = OUT / f"{mod.BASE}.dxf"
doc.saveas(DXF)
mod.index_csv(LIB / f"INDEX_{SET}.csv")
print("saved", DXF, "|", len(mod.INDEX), "blocks indexed")
