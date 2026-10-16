r"""Create a new project folder from the office template (docs/general/PROJECT_WORKFLOW.md).

    python project_template\new_project.py "BANWA 3" --code BW3 --root "G:\My Drive\Works\##2026"
    python project_template\new_project.py "BANWA 3" --code BW3 --root "G:\My Drive\Works\##2026" --fea-local D:\Workspace
    python project_template\new_project.py --office-template "G:\My Drive\Works\##Project Structures"
    python project_template\new_project.py --adopt "G:\My Drive\Works\20250908 CHATAM HOTEL" --code CHT --fea-local D:\Workspace

The folder is named "YYYYMMDD - <name>" (today, or --date). The template is `project_template/tree/`: edit it there
to change every future project. The script never writes into an existing project folder.

--office-template refreshes the office copy of the template (the folder copied by hand for a new project) from
`tree/`, so the two never differ.
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
    "03 FEA/input", "03 FEA/models", "03 FEA/snapshots", "03 FEA/results",
    "04 Code/model", "04 Code/calc", "04 Code/drawings", "04 Code/report",
    "06 CAD/xref", "06 CAD/working", "06 CAD/out",
    "07 Review/markups",
    "08 Report/source", "08 Report/figures", "08 Report/appendix",
]
TEXT = {".md", ".py", ".csv", ".txt"}
RENAME = {"gitignore.txt": ".gitignore"}
SYNCED = ("My Drive", "Google Drive", "OneDrive", "Dropbox")

# the office template before 11/10/2026 -> its place in this structure
OFFICE_OLD = [("Transfer in", "01 Transfer in"), ("Calculation", "05 Calculation"), ("CAD", "06 CAD"),
              ("Transfer out", "09 Publish"),
              ("09 Publish/EXAMPLE", "09 Publish/YYYYMMDD - SET Rev A - PURPOSE (example)")]
OFFICE_EXAMPLE = OFFICE_OLD[-1][1]
OFFICE_VALUES = {"PROJECT": "<project name>", "CODE": "<PPPP>", "DATE": "YYYYMMDD", "DATE_TEXT": "DD/MM/YYYY",
                 "STARTED": "DD/MM/YYYY",
                 "DRAFTER": str(DRAFTER), "FEA_RUN": r"D:\Workspace\<YYYYMMDD - project name>\FEA run"}
OFFICE_README = r"""# Office project structure (template)

Create a new project with the script, which names the folder, fills the names and paths and makes `04 Code` a git
repository:

    python "{drafter}\project_template\new_project.py" "<project name>" --code <PPPP> --root "G:\My Drive\Works\##2026" --fea-local D:\Workspace

Or copy this whole folder and rename it `YYYYMMDD - <project name>`; then replace `<project name>`, `<PPPP>` and
`DD/MM/YYYY` in `PROJECT.md`, `STATUS.md` and the READMEs, set `FEA_RUN` in `04 Code\paths.py`, and delete this file.

The workflow (stages, revisions, what goes where): `{drafter}\docs\general\PROJECT_WORKFLOW.md`.

This folder is generated from `{drafter}\project_template\tree` by `new_project.py --office-template`. Change the
template there, then refresh this copy; do not edit it here.
"""


def fill(text, values):
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def copy_tree(folder, values, overwrite=True):
    """Copy the template into folder with the placeholders filled. Template files are written over (overwrite=False:
    an existing file is kept); nothing else in folder is changed."""
    for src in sorted(TREE.rglob("*")):
        rel = src.relative_to(TREE)
        dst = folder / rel.parent / RENAME.get(rel.name, rel.name)
        if not overwrite and dst.exists() and dst.is_file():
            continue
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


def create(name, code, root, date=None, fea_local=None, git=True):
    date = date or dt.date.today().strftime("%Y%m%d")
    d = dt.datetime.strptime(date, "%Y%m%d")
    folder = Path(root) / f"{date} - {name}"
    if folder.exists():
        raise SystemExit(f"!! {folder} already exists: the template never writes into an existing folder")
    fea_run = Path(fea_local) / folder.name / "FEA run" if fea_local else folder / "03 FEA" / "run"
    values = {"PROJECT": name, "CODE": code.upper(), "DATE": date, "DATE_TEXT": d.strftime("%d/%m/%Y"),
              "STARTED": d.strftime("%d/%m/%Y"), "DRAFTER": str(DRAFTER), "FEA_RUN": str(fea_run)}

    copy_tree(folder, values)
    fea_run.mkdir(parents=True, exist_ok=True)

    left = [str(p.relative_to(folder)) for p in folder.rglob("*") if p.is_file() and p.suffix in TEXT
            and "{{" in p.read_text(encoding="utf-8")]
    if left:
        print("!! placeholders left in: " + ", ".join(left))

    if git:
        init_git(folder / "04 Code", f"{name}: project code from the office template")

    print(f"created {folder}")
    print(f"FEA working folder {fea_run}")
    if not fea_local and any(s in str(folder) for s in SYNCED):
        print("   note: the project is on a synced drive; GEN NX result files reach several GB per run. "
              "Consider --fea-local D:\\Workspace (see PROJECT_WORKFLOW.md W2.4).")
    print("next: fill PROJECT.md sections 1 - 3 and 02 Design basis\\DESIGN_BASIS.md, then STATUS.md")
    return folder


def init_git(code_dir, message):
    if not shutil.which("git") or (code_dir / ".git").exists():
        return
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=code_dir, check=True)
    subprocess.run(["git", "add", "-A"], cwd=code_dir, check=True, capture_output=True)
    res = subprocess.run(["git", "commit", "-q", "-m", message], cwd=code_dir, capture_output=True, text=True)
    if res.returncode:
        print("   note: 04 Code is a git repository, but the first commit was not made (no git user.name / "
              "user.email here?): set them, then commit")


def adopt(folder, code, name=None, fea_local=None, git=True):
    """Bring an existing project folder into the structure, in place (PROJECT_WORKFLOW W8): the old office folders
    are renamed (Transfer in -> 01 ..., Calculation -> 05, CAD -> 06, Transfer out -> 09 Publish), the missing folders
    and template files are added, an existing file is never overwritten, nothing is deleted, the project folder keeps
    its name. Folders that are not part of the structure are listed and left where they are."""
    folder = Path(folder)
    if not folder.is_dir():
        raise SystemExit(f"!! {folder} not found")
    date = folder.name[:8] if folder.name[:8].isdigit() else dt.date.today().strftime("%Y%m%d")
    d = dt.datetime.strptime(date, "%Y%m%d")
    name = name or folder.name[8:].strip(" -") or folder.name
    for old, new in OFFICE_OLD[:-1]:
        o, n = folder / old, folder / new
        if o.is_dir() and not n.exists():
            o.rename(n)
            print(f"renamed {old} -> {new}")
        elif o.is_dir():
            print(f"!! both {old} and {new} exist: merge them by hand")
    fea_run = Path(fea_local) / folder.name / "FEA run" if fea_local else folder / "03 FEA" / "run"
    values = {"PROJECT": name, "CODE": code.upper(), "DATE": date, "STARTED": d.strftime("%d/%m/%Y"),
              "DATE_TEXT": dt.date.today().strftime("%d/%m/%Y"),      # the day the folder was adopted
              "DRAFTER": str(DRAFTER), "FEA_RUN": str(fea_run)}
    copy_tree(folder, values, overwrite=False)
    fea_run.mkdir(parents=True, exist_ok=True)
    known = {p.name for p in TREE.iterdir()} | {"desktop.ini"}
    other = sorted(p.name for p in folder.iterdir() if p.name not in known and p.name != ".gitignore")
    if other:
        print("not part of the structure (left as they are): " + ", ".join(other))
    if git:
        init_git(folder / "04 Code", f"{name}: project code from the office template")
    print(f"adopted {folder}")
    print(f"FEA working folder {fea_run}")
    return folder


def office_template(dest):
    """Refresh the office copy of the template: the old office folders are renamed into the structure, the template
    files written over; nothing else in dest is changed or deleted."""
    dest = Path(dest)
    if not dest.is_dir():
        raise SystemExit(f"!! {dest} not found")
    for old, new in OFFICE_OLD:
        o, n = dest / old, dest / new
        if o.is_dir() and not n.exists():
            o.rename(n)
            print(f"renamed {old} -> {new}")
        elif o.is_dir():
            print(f"!! both {old} and {new} exist: merge them by hand")
    copy_tree(dest, OFFICE_VALUES)
    for sub in ("CAD", "PDF"):
        (dest / OFFICE_EXAMPLE / sub).mkdir(parents=True, exist_ok=True)
    (dest / "_HOW TO USE.md").write_text(OFFICE_README.format(drafter=DRAFTER), encoding="utf-8", newline="\n")
    print(f"office template refreshed: {dest}")
    return dest


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", nargs="?", help='project name, e.g. "BANWA 3"')
    ap.add_argument("--code", help="EIT 13 project abbreviation, 2 - 4 letters (e.g. BW3)")
    ap.add_argument("--root", help=r'parent folder, e.g. "G:\My Drive\Works\##2026"')
    ap.add_argument("--date", help="YYYYMMDD start date (default today)")
    ap.add_argument("--fea-local", help=r"local disk folder for GEN NX runs, e.g. D:\Workspace")
    ap.add_argument("--no-git", action="store_true", help="do not make 04 Code a git repository")
    ap.add_argument("--adopt", metavar="FOLDER",
                    help="bring an existing project folder into the structure in place (with --code)")
    ap.add_argument("--office-template", metavar="FOLDER",
                    help=r'refresh the office copy instead, e.g. "G:\My Drive\Works\##Project Structures"')
    a = ap.parse_args(argv)
    if a.office_template:
        office_template(a.office_template)
        return
    if a.adopt:
        if not a.code:
            ap.error("--adopt needs --code")
        adopt(a.adopt, a.code, a.name, a.fea_local, git=not a.no_git)
        return
    if not (a.name and a.code and a.root):
        ap.error("name, --code and --root are required")
    if not (2 <= len(a.code) <= 4 and a.code.isalnum()):
        raise SystemExit("!! --code must be 2 - 4 letters or digits (EIT 13 PPPP)")
    create(a.name, a.code, a.root, a.date, a.fea_local, git=not a.no_git)


if __name__ == "__main__":
    sys.exit(main())
