"""
Render detail blocks of a built set to PNG for review (no AutoCAD needed; ezdxf drawing add-on).

usage: python render_block.py <set> <block> [<block> ...]      e.g.  python render_block.py slabs DET-1123-2
Writes out/_blk_<block>.png. Line weights and fonts are approximate - check the plotted PDF for the final look.
"""
import sys
from pathlib import Path

import ezdxf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ezdxf import bbox
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, ColorPolicy

HERE = Path(__file__).resolve().parent
BASES = {"gn": "STR-ST-1001_General_Notes_Concrete_A3_RevB", "columns": "STR-ST-1101_Typical_Column_Details_A3_RevA",
         "beams": "STR-ST-1111_Typical_Beam_Details_A3_RevA", "slabs": "STR-ST-1121_Typical_Slab_Details_A3_RevA"}
doc = ezdxf.readfile(HERE / "out" / f"{BASES[sys.argv[1]]}.dxf")
cfg = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.BLACK, min_lineweight=0.1)
for name in sys.argv[2:]:
    blk = doc.blocks.get(name)
    ext = bbox.extents(blk)
    w, h = ext.size.x, ext.size.y
    fig = plt.figure(figsize=(12, 12 * h / w))
    ax = fig.add_axes([0, 0, 1, 1])
    Frontend(RenderContext(doc), MatplotlibBackend(ax), config=cfg).draw_entities(blk)
    ax.set_xlim(ext.extmin.x, ext.extmax.x)
    ax.set_ylim(ext.extmin.y, ext.extmax.y)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(HERE / "out" / f"_blk_{name}.png", dpi=110)
    plt.close(fig)
    print("rendered", name)
