"""
Plot every layout of a built set to PDF with AutoCAD Core Console, save the DWG, merge the PDFs and
write the block library: one DWG per detail block (DET-*) and the title block (TB-*), via WBLOCK.

usage: python plot.py <set> [--ezdxf]        set = gn | columns | beams | slabs | all
Needs: AutoCAD 2024 or later (newest installed, or ACCORECONSOLE) and 'DWG To PDF.pc3'. Run from PowerShell or Python:
the console does not execute scripts when launched from Git Bash.

Plot style NRW-EIT.ctb is generated here: every ACI colour plots black, ACI 8 plots 50 % grey
(secondary information), lineweight and linetype = object. A copy is written next to the drawings
and one into AutoCAD's Plot Styles folder so the DWG plots the same way when opened there.
Without AutoCAD (or with --ezdxf) the sheets are rendered with ezdxf instead: drafter/ezplot.py.
Exit code 1 when the plot fails: see drafter/acad.py and drafter/ezplot.py. A partial set is never merged.
"""
import csv
import subprocess
import sys
from pathlib import Path

import ezdxf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))           # repository root: shared drafter package
from drafter import acad, plotting                 # noqa: E402

SETS = {"gn": "STR-ST-1001_General_Notes_Concrete_A3_RevA",
        "columns": "STR-ST-1101_Typical_Column_Details_A3_RevA",
        "beams": "STR-ST-1111_Typical_Beam_Details_A3_RevA",
        "slabs": "STR-ST-1121_Typical_Slab_Details_A3_RevA"}
SET = (plotting.args() or ["all"])[0]
if SET != "all" and SET not in SETS:
    sys.exit(f"unknown set '{SET}': use {' | '.join(SETS)} | all")
if SET == "all":
    failed = [k for k in SETS
              if subprocess.run([sys.executable, str(HERE / "plot.py"), k, *plotting.flags()]).returncode]
    if failed:
        print("!! plot failed:", ", ".join(failed))
    sys.exit(1 if failed else 0)

OUT, LIB = HERE / "out", HERE / "library"
DXF = OUT / f"{SETS[SET]}.dxf"
CTB = "NRW-EIT.ctb"
GREY_ACI = 8
if not DXF.exists():
    sys.exit(f"!! {DXF.name} not built: run python build.py {SET}")
LAYOUTS = [n for n in ezdxf.readfile(DXF).layouts.names_in_taborder() if n != "Model"]   # every sheet in the DXF
with open(LIB / f"INDEX_{SET}.csv", encoding="utf-8-sig") as f:
    WBLOCKS = [r["block"] for r in csv.DictReader(f) if r["kind"] in ("detail", "title block")]

ctb = plotting.base_ctb()                            # screen ACI 8 to 50 %: grey for secondary information
ctb.description = "NRW / EIT 011006-19: monochrome, ACI 8 screened 50%, object lineweights"
ctb[GREY_ACI].screen = 50

SERIES = {"gn": "DET-100", "columns": "DET-110", "beams": "DET-111", "slabs": "DET-112"}[SET]
for p in [*LIB.glob(f"{SERIES}*.dwg"), *LIB.glob(f"{SERIES}*.dxf")]:   # details no longer in the drawing
    if p.stem not in WBLOCKS:
        print("  removed stale library file", p.name)
        p.unlink()

plotting.plot_set(DXF, LAYOUTS, CTB, ctb,
          setvars=["LTSCALE 1", "PSLTSCALE 1", "MSLTSCALE 1", "CELTSCALE 1", "PLINEGEN 1", "LWDISPLAY 1"],
          wblocks=WBLOCKS, lib=LIB)
