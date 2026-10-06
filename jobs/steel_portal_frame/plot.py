"""
Project SPF - plot the built set: every A1 sheet to PDF, the DWG and one DWG per detail block (library), with
AutoCAD Core Console; without AutoCAD (or with --ezdxf) the PDF is rendered by ezdxf (drafter/ezplot.py).

usage: python plot.py [--ezdxf] [out_dir]
Plot style: the office STRUCT-A1-A2.ctb (EIT 19.2, user 2026-10-04), copied byte for byte into AutoCAD's Plot
Styles folders when missing there - never re-saved, so the office file is not changed. LTSCALE = the office 45 at
1:100 on A1, which is 45 x 25 / 100 = 11.25 in this composition (td_engine.use_paper). Exit code 1 when the plot
fails. A partial set is never merged.
"""
import csv
import shutil
import sys
from pathlib import Path

import ezdxf
from ezdxf.addons import acadctb

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))            # repository root: shared drafter package
from drafter import acad, ezplot, plotting          # noqa: E402

BASE = "SPF-ST_Steel_Portal_Frame_A1_RevA"
args = plotting.args()
OUT = Path(args[0]) if args else HERE / "out"
LIB = HERE / "library"
DXF = OUT / f"{BASE}.dxf"
CTB_NAME = "STRUCT-A1-A2.ctb"
CTB_SRC = Path(r"G:\My Drive\##Workset_Autocad\Structology\Plot Style") / CTB_NAME
LTS = 45 * 25 / 100                                 # td_engine.use_paper(ltscale_equiv=45) with SC = 25
if not DXF.exists():
    sys.exit(f"!! {DXF.name} not built: run python build.py")
if not CTB_SRC.exists():
    sys.exit(f"!! office plot style not found: {CTB_SRC}")
LAYOUTS = [n for n in ezdxf.readfile(DXF).layouts.names_in_taborder() if n != "Model"]
with open(LIB / "INDEX_spf.csv", encoding="utf-8-sig") as f:
    WBLOCKS = [r["block"] for r in csv.DictReader(f) if r["kind"] in ("detail", "title block")]
for p in [*LIB.glob("DET-*.dwg"), *LIB.glob("DET-*.dxf")]:
    if p.stem not in WBLOCKS:
        print("  removed stale library file", p.name)
        p.unlink()

if plotting.use_autocad():
    for d in acad.style_dirs():
        dst = Path(d) / CTB_NAME
        if not dst.exists():
            shutil.copyfile(CTB_SRC, dst)
            print("  installed", dst)
    shutil.copyfile(CTB_SRC, OUT / CTB_NAME)
    acad.plot(DXF, LAYOUTS, CTB_NAME, paper=acad.PAPER_A1,
              setvars=[f"LTSCALE {LTS}", "PSLTSCALE 0", "MSLTSCALE 0", "CELTSCALE 1", "PLINEGEN 1", "LWDISPLAY 1"],
              per_layout=["PSLTSCALE", "0"], wblocks=WBLOCKS, lib=LIB)
else:
    if not plotting.USE_EZDXF:
        print(f"AutoCAD Core Console not found ({acad.ACC}): plotting with ezdxf instead")
    ezplot.plot(DXF, LAYOUTS, acadctb.load(str(CTB_SRC)), wblocks=WBLOCKS, lib=LIB)
