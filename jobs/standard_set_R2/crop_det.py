"""
Crop detail blocks out of a set's plotted PDF for review (what AutoCAD actually plotted).

usage: python crop_det.py <set> <block> [<block> ...] [--dpi N]      e.g.  python crop_det.py slabs DET-1123-2
Finds the block's insert in model space (sheet i at x = i * SHEET_DX, paper mm), crops that page to the
insert's extents (+ 4 mm) and writes out/_crop_<block>.png.
"""
import sys
from pathlib import Path

import ezdxf
import pymupdf as fitz
from ezdxf import bbox

HERE = Path(__file__).resolve().parent
BASES = {"columns": "STR-ST-1101_Typical_Column_Details_A3_R2", "beams": "STR-ST-1111_Typical_Beam_Details_A3_R2",
         "slabs": "STR-ST-1121_Typical_Slab_Details_A3_R2"}
SHEET_DX, H, SC = 460.0, 297.0, 25.0              # R2: model space at real size, sheet i at x = i * SHEET_DX * SC
args = [a for a in sys.argv[2:] if not a.startswith("--")]
dpi = int(sys.argv[sys.argv.index("--dpi") + 1]) if "--dpi" in sys.argv else 170
args = [a for a in args if not a.isdigit()]
base = BASES[sys.argv[1]]
doc = ezdxf.readfile(HERE / "out" / f"{base}.dxf")
pdf = fitz.open(HERE / "out" / f"{base}.pdf")
k = 72 / 25.4
for name in args:
    ins = [e for e in doc.modelspace() if e.dxftype() == "INSERT" and e.dxf.name == name]
    if not ins:
        print("no insert", name)
        continue
    ext = bbox.extents([ins[0]])
    i = int(ext.extmin.x / SC // SHEET_DX)
    x0, x1 = ext.extmin.x / SC - i * SHEET_DX - 4, ext.extmax.x / SC - i * SHEET_DX + 4
    y0, y1 = ext.extmin.y / SC - 4, ext.extmax.y / SC + 4
    pdf[i].get_pixmap(dpi=dpi, clip=fitz.Rect(x0 * k, (H - y1) * k, x1 * k, (H - y0) * k)).save(
        HERE / "out" / f"_crop_{name}.png")
    print("cropped", name, "page", i + 1)
