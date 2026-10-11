"""Folder map of the project. Scripts read and write through these names, never through typed paths, so the project
folder can move (local disk, Google Drive) without a code change."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ADMIN = ROOT / "00 Admin"
TRANSFER_IN = ROOT / "01 Transfer in"
BASIS = ROOT / "02 Design basis"
FEA = ROOT / "03 FEA"
MODELS = FEA / "models"
SNAPSHOTS = FEA / "snapshots"
RESULTS = FEA / "results"
CODE = ROOT / "04 Code"
CALC = ROOT / "05 Calculation"
CAD = ROOT / "06 CAD"
XREF = CAD / "xref"
CAD_WORK = CAD / "working"
CAD_OUT = CAD / "out"
REVIEW = ROOT / "07 Review"
MARKUPS = REVIEW / "markups"
REPORT = ROOT / "08 Report"
PUBLISH = ROOT / "09 Publish"
ARCHIVE = ROOT / "99 Archive"

FEA_RUN = Path(r"{{FEA_RUN}}")        # where GEN NX analyses (large result files): local disk, not a synced drive
DRAFTER = Path(r"{{DRAFTER}}")        # the toolkit: rules (docs), drafter engine, midas tools


def use_drafter():
    """Put the toolkit on sys.path: then `from drafter import td_engine`, `from drafter.steel import *`."""
    if not DRAFTER.is_dir():
        raise SystemExit(f"!! toolkit not found at {DRAFTER}: correct DRAFTER in paths.py")
    if str(DRAFTER) not in sys.path:
        sys.path.insert(0, str(DRAFTER))


def snapshot(rev):
    """Read-back folder of model revision rev ("r12")."""
    return SNAPSHOTS / rev


def results(rev):
    """Exported results of model revision rev ("r12")."""
    return RESULTS / rev


def out(folder, *parts):
    """An output path in a numbered folder, created on first use: out(CALC, "piles_r12.json")."""
    p = Path(folder, *parts)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p
