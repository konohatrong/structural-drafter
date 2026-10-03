"""
Plot a built DXF with AutoCAD Core Console: every layout to PDF, the drawing to DWG, an optional WBLOCK
library, then merge the pages into one PDF. Shared by every job's plot script.

Run from PowerShell or Python: the console does not execute scripts when launched from Git Bash.
Needs AutoCAD 2024 or later (accoreconsole.exe), 'DWG To PDF.pc3' and AutoCAD's monochrome.ctb. The newest
installed version is used; set the environment variable ACCORECONSOLE to the full path of another
accoreconsole.exe to override it.

plot() exits with code 1 when AutoCAD fails or times out, its log shows a rejected command, a sheet did not
plot, the DWG or a library file is missing, or (font_check) a glyph is not Arial Narrow. A partial set is
never merged: a PDF with a sheet missing looks complete.
"""
import glob
import os
import re
import subprocess
import sys
from pathlib import Path

import pymupdf
from ezdxf.addons import acadctb



def _find_acc():
    """ACCORECONSOLE if set, else the newest <Program Files>\\Autodesk\\AutoCAD 20xx\\accoreconsole.exe"""
    if os.environ.get("ACCORECONSOLE"):
        return os.environ["ACCORECONSOLE"]
    pf = os.environ.get("ProgramFiles", r"C:\Program Files")
    found = sorted(glob.glob(os.path.join(pf, "Autodesk", "AutoCAD 20[0-9][0-9]", "accoreconsole.exe")))
    return found[-1] if found else os.path.join(pf, "Autodesk", "AutoCAD 20xx", "accoreconsole.exe")


ACC = _find_acc()
_VER = re.search(r"AutoCAD (20\d\d)", ACC)
VERSION = _VER.group(1) if _VER else None              # e.g. "2026"; None for an unusual ACCORECONSOLE path
STYLE_GLOB = r"%APPDATA%\Autodesk\AutoCAD 20[0-9][0-9]\*\*\Plotters\Plot Styles"
PAPER = "ISO full bleed A3 (420.00 x 297.00 MM)"
# a rejected answer puts every later line of the script out of step: one such message spoils the whole run
REJECTED = re.compile(r"Unknown command|\*Invalid\*|Invalid option keyword|Point or option keyword required|"
                      r"Requires an integer|Value must be|\*Cancel\*")


def q(p):
    """quoted path: a space in a script line = Enter"""
    return '"' + str(p) + '"'


def style_dirs():
    """AutoCAD's Plot Styles folders of every installed version (one per version / release / language), those
    of the plotting version first"""
    dirs = sorted(glob.glob(os.path.expandvars(STYLE_GLOB)), reverse=True)
    return sorted(dirs, key=lambda d: VERSION is None or f"AutoCAD {VERSION}" not in d)


def available():
    """accoreconsole and AutoCAD's monochrome.ctb are both there"""
    return Path(ACC).exists() and any((Path(d) / "monochrome.ctb").exists() for d in style_dirs())


def check_tools():
    if not Path(ACC).exists():
        sys.exit(f"!! AutoCAD Core Console not found: {ACC} - install AutoCAD 2024 or later, or set ACCORECONSOLE")
    if not style_dirs():
        sys.exit(f"!! no AutoCAD Plot Styles folder found (needs monochrome.ctb): {STYLE_GLOB}")


def monochrome():
    """AutoCAD's own monochrome.ctb (the plotting version's first): its black encoding is what AutoCAD honours"""
    for d in style_dirs():
        if (Path(d) / "monochrome.ctb").exists():
            return acadctb.load(str(Path(d) / "monochrome.ctb"))
    sys.exit(f"!! monochrome.ctb not found in any of: {', '.join(style_dirs())}")


def nearest_lineweight(ctb, mm):
    """index of the nearest STANDARD lineweight: only AutoCAD's fixed table is honoured (set_lineweight
    appends a new entry on a float mismatch)"""
    std = list(ctb.lineweights)
    return min(range(len(std)), key=lambda k: abs(std[k] - mm))


def install_ctb(ctb, name, out):
    """write the plot style next to the drawings and into every AutoCAD Plot Styles folder, so the DWG
    plots the same way when opened there"""
    ctb.save(str(Path(out) / name))
    for d in style_dirs():
        ctb.save(str(Path(d) / name))


def plot(dxf, layouts, ctb, *, setvars, per_layout=(), wblocks=(), lib=None, timeout=600, font_check=True):
    """Plot every layout of dxf to <dxf dir>/<base>.pdf, save <base>.dwg and, with wblocks, one DWG per block
    into lib. setvars: system variables set once ("LTSCALE 1", ...); per_layout: script lines run after CTAB
    on each layout (e.g. PSLTSCALE, which is stored per layout)."""
    dxf = Path(dxf)
    out = dxf.parent
    dwg, pdf = dxf.with_suffix(".dwg"), dxf.with_suffix(".pdf")
    libfiles = [Path(lib) / f"{b}.dwg" for b in wblocks]
    lines = ["FILEDIA 0", "CMDDIA 0", "BACKGROUNDPLOT 0", *setvars, "-PLOTSTAMP", "OFF", ""]
    for lay in layouts:
        lines += ["CTAB", lay, *per_layout, "REGENALL",
                  "-PLOT", "Y", lay, "DWG To PDF.pc3", PAPER, "M", "L", "N",
                  "L", "1:1", "0,0", "Y", ctb, "Y", "N", "N", "N",
                  q(out / f"_{lay}.pdf"), "Y", "Y"]          # save page setup = Y: the DWG keeps the CTB
    if wblocks:
        lines += ["CTAB", "Model"]
        for b, f in zip(wblocks, libfiles):                   # library: one DWG per block, base point = block base
            lines += ["-WBLOCK", q(f), b]
    lines += ["CTAB", layouts[0], "SAVEAS", "2018", q(dwg), "QUIT", "Y"]
    for p in [dwg, pdf, *libfiles, *out.glob("_*.pdf")]:
        if p.exists():
            try:
                p.unlink()           # SAVEAS / WBLOCK would stop at an overwrite prompt; old pages never merge
            except PermissionError:
                sys.exit(f"!! {p} is open in another program - close it and plot again")
    scr = out / "_plot.scr"
    scr.write_bytes(("\r\n".join(lines) + "\r\n").encode("ascii"))   # exact CRLF: stray CR = Enter = repeat

    try:
        res = subprocess.run([ACC, "/i", str(dxf), "/s", str(scr), "/l", "en-US"],
                             capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        sys.exit(f"!! AutoCAD Core Console timed out after {timeout} s - nothing merged")
    raw = res.stdout
    log = raw.decode("utf-16-le", errors="ignore") if raw[:2] != b"Re" else raw.decode(errors="ignore")
    log = log.replace(chr(0), "")
    logfile = out / "_plot.log"
    logfile.write_text(log, encoding="utf-8")

    problems = []
    if res.returncode:
        problems.append(f"accoreconsole exit code {res.returncode}")
    problems += [f"log: {ln.strip()}" for ln in log.splitlines() if REJECTED.search(ln)][:10]
    missing = [lay for lay in layouts if not (out / f"_{lay}.pdf").exists()]
    if missing:
        problems.append("sheets not plotted: " + ", ".join(missing))
    if not dwg.exists():
        problems.append(f"{dwg.name} not saved")
    lib_missing = [f.stem for f in libfiles if not f.exists()]
    if lib_missing:
        problems.append(f"library: {len(lib_missing)}/{len(libfiles)} DWG missing, e.g. {', '.join(lib_missing[:5])}")
    if missing:
        for p in problems:
            print("  !!", p)
        sys.exit(f"!! plot of {dxf.name} failed - see {logfile}")

    merged = pymupdf.open()
    for lay in layouts:
        p = out / f"_{lay}.pdf"
        with pymupdf.open(p) as d:            # re-written first: a page plotted with a substituted SHX font
            src = pymupdf.open("pdf", d.tobytes(garbage=1))   # carries object numbers insert_pdf rejects
        merged.insert_pdf(src)
        p.unlink()
    merged.save(pdf)
    msg = f"pages {merged.page_count} -> {pdf} | dwg exists: {dwg.exists()}"
    if libfiles:
        msg += f" | library {len(libfiles) - len(lib_missing)}/{len(libfiles)} DWG"
    print(msg, f"| AutoCAD {VERSION or ACC}")

    if font_check:
        # every glyph must come from Arial Narrow. Anything else (e.g. CordiaNew) means a symbol was
        # mis-encoded or is missing from the font - see TYPICAL_DETAILS_INSTRUCTION.md sec. 6.
        fonts = {f[3] for pg in merged for f in pg.get_fonts()}
        bad = sorted(f for f in fonts if not f.startswith("ArialNarrow"))
        if bad:
            problems.append("non-Arial-Narrow fonts: " + ", ".join(bad))
        print("fonts:", ", ".join(sorted(fonts)), "| font check OK" if not bad else "")
    for p in problems:
        print("  !!", p)
    if problems:
        sys.exit(f"!! plot of {dxf.name} finished with {len(problems)} problem(s) - see {logfile}")
