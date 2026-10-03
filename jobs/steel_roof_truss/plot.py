"""
Project SRT - plot the built set: every sheet to PDF, the DWG and one DWG per detail block (library), with
AutoCAD Core Console; without AutoCAD (or with --ezdxf) the PDF is rendered by ezdxf (drafter/ezplot.py).

usage: python plot.py [--ezdxf]
Plot style NRW-EIT-R2.ctb from the R2 pens (lineweight by colour, greys screened 50 %), as the R2 sets.
Exit code 1 when the plot fails. A partial set is never merged.
"""
import csv
import sys
from pathlib import Path

import ezdxf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "standard_set_R2"))
sys.path.insert(0, str(HERE.parents[1]))            # repository root: shared drafter package
from drafter import acad, plotting                 # noqa: E402
from pens import PEN, LTS                          # noqa: E402

BASE = "SRT-ST_Steel_Roof_Truss_T1_A3_RevA"
OUT, LIB = HERE / "out", HERE / "library"
DXF = OUT / f"{BASE}.dxf"
CTB = "NRW-EIT-R2.ctb"
if not DXF.exists():
    sys.exit(f"!! {DXF.name} not built: run python build.py")
LAYOUTS = [n for n in ezdxf.readfile(DXF).layouts.names_in_taborder() if n != "Model"]
with open(LIB / "INDEX_srt.csv", encoding="utf-8-sig") as f:
    WBLOCKS = [r["block"] for r in csv.DictReader(f) if r["kind"] in ("detail", "title block")]

ctb = plotting.base_ctb()
ctb.description = "NRW / EIT 011006-19 R2: monochrome, lineweight by colour, greys screened 50%"
for aci, (lw, screen) in PEN.items():
    ctb[aci].lineweight = acad.nearest_lineweight(ctb, lw / 100.0)
    ctb[aci].screen = screen
for p in [*LIB.glob("DET-*.dwg"), *LIB.glob("DET-*.dxf")]:
    if p.stem not in WBLOCKS:
        print("  removed stale library file", p.name)
        p.unlink()

plotting.plot_set(DXF, LAYOUTS, CTB, ctb,
                  setvars=[f"LTSCALE {LTS}", "PSLTSCALE 0", "MSLTSCALE 0", "CELTSCALE 1", "PLINEGEN 1", "LWDISPLAY 1"],
                  per_layout=["PSLTSCALE", "0"], wblocks=WBLOCKS, lib=LIB)
