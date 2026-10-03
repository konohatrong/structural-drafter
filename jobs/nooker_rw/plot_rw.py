"""
Plot every layout of the generated DXF to PDF with AutoCAD Core Console, save a DWG, merge PDFs.

usage: python plot_rw.py <out_dir> [--ezdxf]
Needs: AutoCAD 2024 or later (newest installed, or ACCORECONSOLE) and 'DWG To PDF.pc3'. Run from PowerShell or Python:
the console does not execute scripts when launched from Git Bash.

Plot style NRW-EIT.ctb is generated here: every ACI colour plots black, ACI 8 plots 50 % grey
(secondary information), lineweight and linetype = object. A copy is written next to the drawings
and one into AutoCAD's Plot Styles folder so the DWG plots the same way when opened there.
Without AutoCAD (or with --ezdxf) the sheets are rendered with ezdxf instead: drafter/ezplot.py.
Exit code 1 when the plot fails: see drafter/acad.py and drafter/ezplot.py. A partial set is never merged.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))    # repository root: shared drafter package
from drafter import acad, plotting                               # noqa: E402

if not plotting.args():
    sys.exit("usage: python plot_rw.py <out_dir>")
OUT = Path(plotting.args()[0]).resolve()
BASE = "NRW-ST_Retaining_Wall_A3_RevB"
DXF = OUT / f"{BASE}.dxf"
CTB = "NRW-EIT.ctb"
LAYOUTS = ["1001", "3001", "5001", "5002", "5003", "5004", "5005"]
GREY_ACI = 8
if not DXF.exists():
    sys.exit(f"!! {DXF} not built: run python build_rw.py {OUT}")

ctb = plotting.base_ctb()                            # screen ACI 8 to 50 %: grey for secondary information
ctb.description = "NRW / EIT 011006-19: monochrome, ACI 8 screened 50%, object lineweights"
ctb[GREY_ACI].screen = 50

plotting.plot_set(DXF, LAYOUTS, CTB, ctb, timeout=300,
          setvars=["LTSCALE 1", "PSLTSCALE 1", "MSLTSCALE 1", "CELTSCALE 1", "PLINEGEN 1", "LWDISPLAY 1"])
