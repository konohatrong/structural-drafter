"""Create a new project folder from the office template (docs/general/PROJECT_WORKFLOW.md).

    python project_template/new_project.py "BANWA 3" --code BW3 --root "G:\\My Drive\\Works\\##2026"
    python project_template/new_project.py "BANWA 3" --code BW3 --root "G:\\My Drive\\Works\\##2026" --fea-local D:\\Workspace

The folder is named "YYYYMMDD - <name>" (today, or --date). The template is `project_template/tree/`: edit it there
to change every future project. The script never writes into an existing folder.
"""
import argparse
import datetime as dt
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TREE = HERE / "tree"
DRAFTER = HERE.parent

# empty folders the template needs (git keeps no empty folders)
SUBDIRS = [
    "01 Transfer in",
    "03 FEA/models", "03 FEA/snapshots", "03 FEA/results",
    "04 Code/model", "04 Code/calc", "04 Code/drawings", "04 Code/report",
    "06 CAD/xref", "06 CAD/working", "06 CAD/out",
    "07 Review/markups",
    "08 Report/source", "08 Report/figures", "08 Report/appendix",
]
TEXT = {".md", ".py", ".csv", ".txt"}
RENAME = {"gitignore.txt": ".gitignore"}
SYNCED = ("My Drive", "Google Drive", "OneDrive", "Dropbox")


def fill(text, values):
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def create(name, code, root, date=None, fea_local=None, git=True):
    date = date or dt.date.today().strftime("%Y%m%d")
    d = dt.datetime.strptime(date, "%Y%m%d")
    folder = Path(root) / f"{date} - {name}"
    if folder.exists():
        raise SystemExit(f"!! {folder} already exists: the template never writes into an existing folder")
    fea_run = Path(fea_local) / folder.name / "FEA run" if fea_local else folder / "03 FEA" / "run"
    values = {"PROJECT": name, "CODE": code.upper(), "DATE": date, "DATE_TEXT": d.strftime("%d/%m/%Y"),
              "DRAFTER": str(DRAFTER), "FEA_RUN": str(fea_run)}

    for src in sorted(TREE.rglob("*")):
        rel = src.relative_to(TREE)
        dst = folder / rel.parent / RENAME.get(rel.name, rel.name)
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
        elif src.suffix in TEXT:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(fill(src.read_text(encoding="utf-8"), values), encoding="utf-8", newline="\n")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    for sub in SUBDIRS:
        (folder / sub).mkdir(parents=True, exist_ok=True)
    fea_run.mkdir(parents=True, exist_ok=True)

    left = [str(p.relative_to(folder)) for p in folder.rglob("*") if p.is_file() and p.suffix in TEXT
            and "{{" in p.read_text(encoding="utf-8")]
    if left:
        print("!! placeholders left in: " + ", ".join(left))

    if git and shutil.which("git"):
        code_dir = folder / "04 Code"
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=code_dir, check=True)
        subprocess.run(["git", "add", "-A"], cwd=code_dir, check=True, capture_output=True)
        res = subprocess.run(["git", "commit", "-q", "-m", f"{name}: project code from the office template"],
                             cwd=code_dir, capture_output=True, text=True)
        if res.returncode:
            print("   note: 04 Code is a git repository, but the first commit was not made (no git user.name / "
                  "user.email here?): set them, then commit")

    print(f"created {folder}")
    print(f"FEA working folder {fea_run}")
    if not fea_local and any(s in str(folder) for s in SYNCED):
        print("   note: the project is on a synced drive; GEN NX result files reach several GB per run. "
              "Consider --fea-local D:\\Workspace (see PROJECT_WORKFLOW.md W2.4).")
    print("next: fill PROJECT.md sections 1 - 3 and 02 Design basis\\DESIGN_BASIS.md, then STATUS.md")
    return folder


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", help='project name, e.g. "BANWA 3"')
    ap.add_argument("--code", required=True, help="EIT 13 project abbreviation, 2 - 4 letters (e.g. BW3)")
    ap.add_argument("--root", required=True, help=r'parent folder, e.g. "G:\My Drive\Works\##2026"')
    ap.add_argument("--date", help="YYYYMMDD start date (default today)")
    ap.add_argument("--fea-local", help=r"local disk folder for GEN NX runs, e.g. D:\Workspace")
    ap.add_argument("--no-git", action="store_true", help="do not make 04 Code a git repository")
    a = ap.parse_args(argv)
    if not (2 <= len(a.code) <= 4 and a.code.isalnum()):
        raise SystemExit("!! --code must be 2 - 4 letters or digits (EIT 13 PPPP)")
    create(a.name, a.code, a.root, a.date, a.fea_local, git=not a.no_git)


if __name__ == "__main__":
    sys.exit(main())
