"""
Typical details (11xx) - build one set of A3 sheets to DXF.

usage: python build_td.py <out_dir> [columns|beams|slabs]      (default: columns)
    columns -> STR-ST-1101_Typical_Column_Details_A3_RevA.dxf   (1101, 1102)
    beams   -> STR-ST-1111_Typical_Beam_Details_A3_RevA.dxf     (1111 - 1114)
    slabs   -> STR-ST-1121_Typical_Slab_Details_A3_RevA.dxf     (1121 - )
Engine: td_engine.py.  Content: td_columns.py, td_beams.py, td_slabs.py.  Guide: TYPICAL_DETAILS_INSTRUCTION.md
"""
import importlib
import sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("out")
SET = sys.argv[2] if len(sys.argv) > 2 else "columns"
mod = importlib.import_module({"columns": "td_columns", "beams": "td_beams", "slabs": "td_slabs"}[SET])
mod.build()
doc = mod.doc
if "Layout1" in doc.layouts:
    doc.layouts.delete("Layout1")
OUT.mkdir(parents=True, exist_ok=True)
DXF = OUT / f"{mod.BASE}.dxf"
doc.saveas(DXF)
print("saved", DXF)
