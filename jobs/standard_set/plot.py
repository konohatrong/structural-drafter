"""
Plot every layout of a built set to PDF with AutoCAD Core Console, save the DWG, merge the PDFs and
write the block library: one DWG per detail block (DET-*) and the title block (TB-*), via WBLOCK.

usage: python plot.py <set>        set = gn | columns | beams | slabs | all
Needs: AutoCAD 2024 (accoreconsole.exe) and 'DWG To PDF.pc3'. Run from PowerShell or Python:
the console does not execute scripts when launched from Git Bash.

Plot style NRW-EIT.ctb is generated here: every ACI colour plots black, ACI 8 plots 50 % grey
(secondary information), lineweight and linetype = object. A copy is written next to the drawings
and one into AutoCAD's Plot Styles folder so the DWG plots the same way when opened there.
"""
import csv
import glob
import os
import subprocess
import sys
from pathlib import Path

import fitz  # PyMuPDF
import ezdxf
from ezdxf.addons import acadctb

HERE = Path(__file__).resolve().parent
ACC = r"C:\Program Files\Autodesk\AutoCAD 2024\accoreconsole.exe"
SETS = {"gn": "STR-ST-1001_General_Notes_Concrete_A3_RevB",
        "columns": "STR-ST-1101_Typical_Column_Details_A3_RevA",
        "beams": "STR-ST-1111_Typical_Beam_Details_A3_RevA",
        "slabs": "STR-ST-1121_Typical_Slab_Details_A3_RevA"}
SET = sys.argv[1] if len(sys.argv) > 1 else "all"
if SET == "all":
    for k in SETS:
        subprocess.run([sys.executable, str(HERE / "plot.py"), k], check=True)
    sys.exit(0)

OUT, LIB = HERE / "out", HERE / "library"
BASE = SETS[SET]
DXF = OUT / f"{BASE}.dxf"
DWG = OUT / f"{BASE}.dwg"
PDF = OUT / f"{BASE}.pdf"
CTB = "NRW-EIT.ctb"
GREY_ACI = 8
LAYOUTS = [n for n in ezdxf.readfile(DXF).layouts.names_in_taborder() if n != "Model"]   # every sheet in the DXF
with open(LIB / f"INDEX_{SET}.csv", encoding="utf-8-sig") as f:
    WBLOCKS = [r["block"] for r in csv.DictReader(f) if r["kind"] in ("detail", "title block")]


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

q = lambda p: '"' + str(p) + '"'          # quoted: a space in a script = Enter
lines = ["FILEDIA 0", "CMDDIA 0", "BACKGROUNDPLOT 0", "LTSCALE 1", "PSLTSCALE 1", "MSLTSCALE 1",
         "CELTSCALE 1", "PLINEGEN 1", "LWDISPLAY 1", "-PLOTSTAMP", "OFF", ""]
for lay in LAYOUTS:
    lines += ["CTAB", lay, "REGENALL",
              "-PLOT", "Y", lay, "DWG To PDF.pc3", "ISO full bleed A3 (420.00 x 297.00 MM)", "M", "L", "N",
              "L", "1:1", "0,0", "Y", CTB, "Y", "N", "N", "N",
              q(OUT / f"_{lay}.pdf"), "Y", "Y"]          # save page setup = Y: DWG keeps NRW-EIT.ctb
lines += ["CTAB", "Model"]
for b in WBLOCKS:                                        # library: one DWG per block, base point = block base
    lines += ["-WBLOCK", q(LIB / f"{b}.dwg"), b]
lines += ["CTAB", LAYOUTS[0], "SAVEAS", "2018", q(DWG), "QUIT", "Y"]
for p in [DWG] + [LIB / f"{b}.dwg" for b in WBLOCKS]:
    if p.exists():
        p.unlink()                   # SAVEAS / WBLOCK would stop at an overwrite prompt
SERIES = {"gn": "DET-100", "columns": "DET-110", "beams": "DET-111", "slabs": "DET-112"}[SET]
for p in LIB.glob(f"{SERIES}*.dwg"):                     # details of this set no longer in the drawing
    if p.stem not in WBLOCKS:
        print("  removed stale library file", p.name)
        p.unlink()
scr = OUT / "_plot.scr"
scr.write_bytes(("\r\n".join(lines) + "\r\n").encode("ascii"))   # exact CRLF: stray CR = Enter = repeat

res = subprocess.run([ACC, "/i", str(DXF), "/s", str(scr), "/l", "en-US"],
                     capture_output=True, timeout=600)
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
lib_ok = sum((LIB / f"{b}.dwg").exists() for b in WBLOCKS)
print("pages", merged.page_count, "->", PDF, "| dwg exists:", DWG.exists(), f"| library {lib_ok}/{len(WBLOCKS)} DWG")

# font check: every glyph must come from Arial Narrow. Anything else (e.g. CordiaNew) means a
# symbol was mis-encoded or is missing from the font - see TYPICAL_DETAILS_INSTRUCTION.md sec. 6.
fonts = {f[3] for pg in merged for f in pg.get_fonts()}
bad = sorted(f for f in fonts if not f.startswith("ArialNarrow"))
print("fonts:", ", ".join(sorted(fonts)), "| !! NON-ARIAL-NARROW FONTS: " + ", ".join(bad) if bad else "| font check OK")
