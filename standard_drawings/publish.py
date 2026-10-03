"""
Publish an office standard drawing set (build + plot from its generator, then copy the result).

usage (from the repository root, in PowerShell):
    python standard_drawings/publish.py <set|all> [--ezdxf] [--no-build]
        -> standard_drawings/developing/<set folder>/            local review copy, replaced every time (not in git)
    python standard_drawings/publish.py <set> --issue
        -> standard_drawings/issued/<set folder>/<stage>-<rev>/  official issue, never overwritten (kept in git)
           + a row in standard_drawings/REGISTER.md

sets: gn (general notes 1001 - 1003), columns (1101 - 1104), beams (1111 - 1116), slabs (1121 - 1128)

An official issue is refused unless:
  * the generator code (drafter/ and the set's job folder) has no uncommitted changes, so the issue is traceable to
    a commit;
  * AutoCAD Core Console is installed (an issue is plotted by AutoCAD, never by the ezdxf fallback);
  * the build is clean (no "!!") and the plot succeeds, with the DWG and every library DWG present;
  * the revision on the title block (<stage>-<rev> of the drawing number) has not been issued before.
Rules: standard_drawings/README.md.
"""
import csv
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import ezdxf

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from drafter import acad                            # noqa: E402

SETS = {
    "gn": dict(job="jobs/standard_set", base="STR-ST-1001_General_Notes_Concrete_A3_RevA",
               folder="STR-ST-1001_General_Notes_Concrete", title="GENERAL NOTES - STRUCTURAL CONCRETE"),
    "columns": dict(job="jobs/standard_set_R2", base="STR-ST-1101_Typical_Column_Details_A3_R2",
                    folder="STR-ST-1101_Typical_Column_Details", title="TYPICAL COLUMN DETAILS"),
    "beams": dict(job="jobs/standard_set_R2", base="STR-ST-1111_Typical_Beam_Details_A3_R2",
                  folder="STR-ST-1111_Typical_Beam_Details", title="TYPICAL BEAM DETAILS"),
    "slabs": dict(job="jobs/standard_set_R2", base="STR-ST-1121_Typical_Slab_Details_A3_R2",
                  folder="STR-ST-1121_Typical_Slab_Details", title="TYPICAL SLAB DETAILS"),
}
TB = "TB-A3-NRW"
REGISTER = HERE / "REGISTER.md"


def fail(msg):
    sys.exit(f"!! {msg}")


def run(cmd, cwd):
    print(">", " ".join(cmd), flush=True)
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    if subprocess.run([sys.executable, *cmd], cwd=cwd, env=env).returncode:
        fail(f"{' '.join(cmd)} failed in {cwd}")


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def sheets_of(dxf):
    """title-block data of every layout: drawing no., titles, status, revision rows"""
    out = []
    doc = ezdxf.readfile(dxf)
    names = [n for n in doc.layouts.names_in_taborder() if n != "Model"]
    # current engine: the title block is in each layout; R1 engine (general notes): one per sheet in model space,
    # left to right in sheet order
    found = [(n, i) for n in names for i in doc.layouts.get(n).query(f'INSERT[name=="{TB}"]')]
    if not found:
        msp_tb = sorted(doc.modelspace().query(f'INSERT[name=="{TB}"]'), key=lambda e: e.dxf.insert.x)
        found = list(zip(names, msp_tb)) if len(msp_tb) == len(names) else []
    for name, ins in found:
        a = {at.dxf.tag: at.dxf.text for at in ins.attribs}
        revs = [(a.get(f"REV_{k}", ""), a.get(f"REV_{k}_DESC", ""), a.get(f"REV_{k}_DATE", ""))
                for k in range(1, 5) if a.get(f"REV_{k}")]
        out.append(dict(layout=name, dwg_no=a.get("DWG_NO", ""),
                        title=" ".join(a.get(f"TITLE_{k}", "") for k in (1, 2, 3)).strip(),
                        status=f"{a.get('STATUS_1', '')} / {a.get('STATUS_2', '')}".strip(" /"),
                        revisions=revs))
    if not out:
        fail(f"no title block {TB} found in {dxf.name}")
    return out


def library_files(lib, key, need_dwg):
    """library DWGs (or DXFs without AutoCAD / ODA) of every detail and the title block of the set"""
    with open(lib / f"INDEX_{key}.csv", encoding="utf-8-sig") as f:
        blocks = [r["block"] for r in csv.DictReader(f) if r["kind"] in ("detail", "title block")]
    files, missing = [], []
    for b in blocks:
        p = lib / f"{b}.dwg"
        if not p.exists() and not need_dwg:
            p = lib / f"{b}.dxf"
        (files if p.exists() else missing).append(p)
    if missing:
        fail(f"library files missing: {', '.join(p.stem for p in missing[:8])}{' ...' if len(missing) > 8 else ''}")
    return files + [lib / f"INDEX_{key}.csv"]


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def publish(key, issue, ezdxf_plot, build):
    s = SETS[key]
    job = ROOT / s["job"]
    out, lib = job / "out", job / "library"
    if issue:
        dirty = git("status", "--porcelain", "--", "drafter", s["job"])
        if dirty:
            fail("uncommitted changes in the generator - commit them first, so the issue is traceable:\n" + dirty)
        if not acad.available():
            fail("AutoCAD Core Console not found: an official issue is plotted by AutoCAD, not by ezdxf")
    if build:
        run(["build.py", key], job)
        run(["plot.py", key, *(["--ezdxf"] if ezdxf_plot else [])], job)
    dxf, pdf, dwg = (out / f"{s['base']}{e}" for e in (".dxf", ".pdf", ".dwg"))
    for p in (dxf, pdf):
        if not p.exists():
            fail(f"{p.name} not found: build and plot the set first")
    if pdf.stat().st_mtime < dxf.stat().st_mtime:
        fail(f"{pdf.name} is older than its DXF: plot the set again")
    has_dwg = dwg.exists() and dwg.stat().st_mtime >= dxf.stat().st_mtime
    if issue and not has_dwg:
        fail(f"{dwg.name} missing or older than the DXF: the AutoCAD plot did not complete")
    sheets = sheets_of(dxf)
    stage_rev = "-".join(sheets[0]["dwg_no"].split("-")[-2:])          # e.g. "D-A"
    if any("-".join(sh["dwg_no"].split("-")[-2:]) != stage_rev for sh in sheets):
        fail("the sheets of the set carry different revisions: " + ", ".join(sh["dwg_no"] for sh in sheets))

    if issue:
        target = HERE / "issued" / s["folder"] / stage_rev
        if target.exists():
            fail(f"{target.relative_to(ROOT)} already exists: an issued revision is never overwritten. "
                 "Raise the revision in the generator (PROJ['rev'], REVS) and issue again")
    else:
        target = HERE / "developing" / s["folder"]
        if target.exists():
            shutil.rmtree(target)
    (target / "library").mkdir(parents=True)

    files = [pdf] + ([dwg] if has_dwg else []) + library_files(lib, key, need_dwg=issue)
    if not has_dwg and not issue:
        files.insert(1, dxf)                        # no DWG without AutoCAD / ODA: keep the DXF instead
    copied = []
    for p in files:
        dst = target / ("library" if p.parent == lib else "") / p.name
        shutil.copy2(p, dst)
        copied.append(dict(path=dst.relative_to(target).as_posix(), bytes=dst.stat().st_size, sha256=sha256(dst)))

    rev = stage_rev.split("-")[-1]
    desc = next((d for r, d, _ in sheets[0]["revisions"] if r == rev), "")
    manifest = dict(set=key, title=s["title"], stage_rev=stage_rev, kind="issued" if issue else "developing",
                    date=dt.date.today().isoformat(), commit=git("rev-parse", "HEAD"),
                    generator_clean=not git("status", "--porcelain", "--", "drafter", s["job"]),
                    plotted_with="ezdxf" if (ezdxf_plot or not has_dwg) else "AutoCAD Core Console",
                    revision_description=desc, sheets=sheets, files=copied)
    (target / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    if issue:
        nos = f"{sheets[0]['dwg_no']} … {sheets[-1]['dwg_no']}" if len(sheets) > 1 else sheets[0]["dwg_no"]
        row = (f"| {manifest['date']} | {s['title']} | {nos} | {stage_rev} | {sheets[0]['status']} | {desc} | "
               f"`issued/{s['folder']}/{stage_rev}/` | `{manifest['commit'][:7]}` |\n")
        with open(REGISTER, "a", encoding="utf-8", newline="\n") as f:
            f.write(row)
        print(f"issued {nos} {stage_rev} -> {target.relative_to(ROOT)}; register updated."
              f"\nCommit standard_drawings/ to record the issue.")
    else:
        print(f"developing copy -> {target.relative_to(ROOT)} ({manifest['plotted_with']}, {len(copied)} files)")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    unknown = flags - {"--issue", "--ezdxf", "--no-build"}
    if len(args) != 1 or unknown or (args[0] != "all" and args[0] not in SETS):
        sys.exit(__doc__)
    issue = "--issue" in flags
    if issue and (args[0] == "all" or flags & {"--ezdxf", "--no-build"}):
        fail("--issue takes one set and always builds and plots with AutoCAD (no --ezdxf, no --no-build)")
    for key in (SETS if args[0] == "all" else [args[0]]):
        publish(key, issue, "--ezdxf" in flags, "--no-build" not in flags)


if __name__ == "__main__":
    main()
