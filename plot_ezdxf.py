"""
Plot any built DXF without AutoCAD: every paper-space layout, in tab order, to one vector PDF next to the DXF,
rendered with ezdxf (drafter/ezplot.py). DWG too when the ODA File Converter is installed.

usage: python plot_ezdxf.py <drawing.dxf> [<plot style.ctb>]

Without a CTB, every colour plots black at the object lineweight (the jobs give each layer its pen's lineweight).
The job plot scripts (plot.py, plot_rw.py, ...) build the job's own CTB and fall back to this renderer by
themselves when AutoCAD is not installed; use them for a full set. This script is for a quick look at one DXF.
"""
import sys
from pathlib import Path

import ezdxf
from ezdxf.addons import acadctb

from drafter import ezplot

args = sys.argv[1:]
if not args or not args[0].lower().endswith(".dxf"):
    sys.exit(__doc__.strip().splitlines()[3])
dxf = Path(args[0]).resolve()
if not dxf.exists():
    sys.exit(f"!! {dxf} not found")
if len(args) > 1:
    ctb = acadctb.load(args[1])
else:
    ctb = acadctb.new_ctb()                        # every colour black, lineweight = object
    for aci in range(1, 256):
        ctb[aci].color = (0, 0, 0)
layouts = [n for n in ezdxf.readfile(dxf).layouts.names_in_taborder() if n != "Model"]
ezplot.plot(dxf, layouts, ctb)
