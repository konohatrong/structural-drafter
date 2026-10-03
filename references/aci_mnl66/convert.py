"""
Convert the ACI MNL-66(20) supplemental DWGs for review: DXF (text / geometry) and PDF (model-space extents,
fit to A3 landscape, monochrome) via AutoCAD Core Console, then PNG pages.

usage (from PowerShell):  python convert.py [substring filter]
The supplemental DWGs (copyrighted, not in the repository) are read from the folder in the environment
variable MNL66_SRC; the default is the author's copy on G:.
"""
import os
import subprocess
import sys
from pathlib import Path

import pymupdf as fitz

SRC = Path(os.environ.get("MNL66_SRC",
           r"G:\My Drive\##Workset_Autocad\supplemental Autocad files to ACI Detailing Manual Manual MNL-66(20) 2020"
           r"\supplemental Autocad files to ACI Detailing Manual Manual MNL-66(20) 2020"))
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))           # repository root: shared drafter package
from drafter.acad import ACC                       # noqa: E402  newest AutoCAD, or ACCORECONSOLE
if not SRC.exists():
    sys.exit(f"!! MNL-66 supplemental files not found: {SRC} - set MNL66_SRC")
flt = sys.argv[1] if len(sys.argv) > 1 else ""
q = lambda p: '"' + str(p) + '"'

for dwg in sorted(SRC.rglob("*.dwg")):
    if flt not in str(dwg):
        continue
    cat = dwg.parent.name
    name = f"{cat}__{dwg.stem}"
    dxf, pdf, png = HERE / "dxf" / f"{name}.dxf", HERE / "pdf" / f"{name}.pdf", HERE / "png" / f"{name}.png"
    if pdf.exists() and dxf.exists():
        continue
    for p in (dxf, pdf):
        if p.exists():
            p.unlink()
    lines = ["FILEDIA 0", "CMDDIA 0", "BACKGROUNDPLOT 0", "TILEMODE 1", "ZOOM E",
             "DXFOUT", q(dxf), "16",
             "-PLOT", "Y", "Model", "DWG To PDF.pc3", "ISO full bleed A3 (420.00 x 297.00 MM)", "M", "L", "N",
             "E", "F", "C", "Y", "monochrome.ctb", "Y", "A", q(pdf), "N", "Y",
             "QUIT", "Y"]
    scr = HERE / "_conv.scr"
    scr.write_bytes(("\r\n".join(lines) + "\r\n").encode("ascii"))
    try:
        subprocess.run([ACC, "/i", str(dwg), "/s", str(scr), "/l", "en-US"], capture_output=True, timeout=240)
    except subprocess.TimeoutExpired:
        print("timeout", name)
    if pdf.exists():
        with fitz.open(pdf) as d:
            d[0].get_pixmap(dpi=110).save(png)
    print(f"{name:32s} dxf {dxf.exists()}  pdf {pdf.exists()}")
