"""
Project SPF (steel portal-frame building 26 x 90 m) - build the drawing set to DXF.

usage: python build.py            -> out/SPF-ST_Steel_Portal_Frame_A1_RevA.dxf + library/INDEX_spf.csv
The design (calc_spf.py, from the MIDAS snapshot in model/) runs first. Exit code 1 when the build finds a layout
problem ("!!" lines) or the DXF audit reports an error; the DXF is still written for inspection.
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import spf_sheets as mod                            # noqa: E402
from drafter import td_engine                        # noqa: E402  (loaded by spf_engine)

mod.build()
mod.finish()
doc = mod.doc
if "Layout1" in doc.layouts:
    doc.layouts.delete("Layout1")
for err in doc.audit().errors:
    td_engine.warn(f"DXF audit: {err.message}")
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "out"
LIB = HERE / "library"
OUT.mkdir(exist_ok=True)
LIB.mkdir(exist_ok=True)
DXF = OUT / f"{mod.BASE}.dxf"
doc.saveas(DXF)
mod.index_csv(LIB / "INDEX_spf.csv")
print("saved", DXF, "|", len(mod.INDEX), "blocks indexed")
if td_engine.WARNINGS:
    print(f"!! {len(td_engine.WARNINGS)} layout problem(s) - the DXF is saved for inspection, do not plot it")
    sys.exit(1)
