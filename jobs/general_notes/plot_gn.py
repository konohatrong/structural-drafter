"""
Plot every layout of the generated DXF to PDF with AutoCAD Core Console, save a DWG, merge PDFs.

usage: python plot_gn.py <out_dir>
Needs: AutoCAD 2024 (accoreconsole.exe) and 'DWG To PDF.pc3'. Run from PowerShell or Python:
the console does not execute scripts when launched from Git Bash.

Plot style NRW-EIT.ctb is generated here: every ACI colour plots black, ACI 8 plots 50 % grey
(secondary information), lineweight and linetype = object. A copy is written next to the drawings
and one into AutoCAD's Plot Styles folder so the DWG plots the same way when opened there.
"""
import glob
import os
import subprocess
import sys
from pathlib import Path

import fitz  # PyMuPDF
from ezdxf.addons import acadctb

ACC = r"C:\Program Files\Autodesk\AutoCAD 2024\accoreconsole.exe"
OUT = Path(sys.argv[1]).resolve()
BASE = "STR-ST-1001_General_Notes_Concrete_A3_RevA"
DXF = OUT / f"{BASE}.dxf"
DWG = OUT / f"{BASE}.dwg"
PDF = OUT / f"{BASE}.pdf"
CTB = "NRW-EIT.ctb"
LAYOUTS = ["1001"]
GREY_ACI = 8


STYLE_DIRS = glob.glob(os.path.expandvars(r"%APPDATA%\Autodesk\AutoCAD 2024\*\*\Plotters\Plot Styles"))


def make_ctb(path):
    """Start from AutoCAD's own monochrome.ctb (its black encoding is what AutoCAD honours) and
    screen ACI 8 to 50 % - grey for secondary information, everything else solid black."""
    ctb = acadctb.load(str(Path(STYLE_DIRS[0]) / "monochrome.ctb"))
    ctb.description = "NRW / EIT 011006-19: monochrome, ACI 8 screened 50%, object lineweights"
    ctb[GREY_ACI].screen = 50
    ctb.save(path)


make_ctb(OUT / CTB)
for d in STYLE_DIRS:
    make_ctb(Path(d) / CTB)

lines = ["FILEDIA 0", "CMDDIA 0", "BACKGROUNDPLOT 0", "LTSCALE 1", "PSLTSCALE 1", "MSLTSCALE 1",
         "CELTSCALE 1", "PLINEGEN 1", "LWDISPLAY 1", "-PLOTSTAMP", "OFF", ""]
for lay in LAYOUTS:
    lines += ["CTAB", lay, "REGENALL",
              "-PLOT", "Y", lay, "DWG To PDF.pc3", "ISO full bleed A3 (420.00 x 297.00 MM)", "M", "L", "N",
              "L", "1:1", "0,0", "Y", CTB, "Y", "N", "N", "N",
              '"' + str(OUT / f"_{lay}.pdf") + '"', "Y", "Y"]   # quoted: a space in a script = Enter          # save page setup = Y: DWG keeps NRW-EIT.ctb
lines += ["CTAB", LAYOUTS[0], "SAVEAS", "2018", '"' + str(DWG) + '"', "QUIT", "Y"]
if DWG.exists():
    DWG.unlink()                     # SAVEAS would stop at an overwrite prompt
scr = OUT / "_plot.scr"
scr.write_bytes(("\r\n".join(lines) + "\r\n").encode("ascii"))   # exact CRLF: stray CR = Enter = repeat

res = subprocess.run([ACC, "/i", str(DXF), "/s", str(scr), "/l", "en-US"],
                     capture_output=True, timeout=300)
log = res.stdout.decode("utf-16-le", errors="ignore") if res.stdout[:2] != b"Re" else res.stdout.decode(errors="ignore")
(OUT / "_plot.log").write_text(log.replace("\x00", ""), encoding="utf-8")

merged = fitz.open()
for lay in LAYOUTS:
    p = OUT / f"_{lay}.pdf"
    if not p.exists():
        print("missing plot", p)
        continue
    with fitz.open(p) as d:
        merged.insert_pdf(d)
    p.unlink()
merged.save(PDF)
print("pages", merged.page_count, "->", PDF, "| dwg exists:", DWG.exists())
