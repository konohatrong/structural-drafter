"""
Project SRT (steel roof truss T1) - build the drawing set to DXF.

usage: python build.py            -> out/SRT-ST_Steel_Roof_Truss_T1_A3_RevA.dxf + library/INDEX_srt.csv
The design (calc_truss.py) runs first: every size and connection on the sheets comes from it (about 30 s).
Exit code 1 when the build finds a layout problem ("!!" lines) or the DXF audit reports an error; the DXF is
still written for inspection. Engine: drafter/td_engine.py + drafter/steel.py via srt_engine.py.
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import srt_sheets as mod                            # noqa: E402
from drafter import td_engine                        # noqa: E402  (loaded by srt_engine)

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
mod.index_csv(LIB / "INDEX_srt.csv")
print("saved", DXF, "|", len(mod.INDEX), "blocks indexed")
if td_engine.WARNINGS:
    print(f"!! {len(td_engine.WARNINGS)} layout problem(s) - the DXF is saved for inspection, do not plot it")
    sys.exit(1)
