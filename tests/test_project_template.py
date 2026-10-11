"""The project template creates the full folder structure with every placeholder filled, and refuses an existing
folder (docs/general/PROJECT_WORKFLOW.md W1)."""
import importlib.util
import sys
from pathlib import Path

import pytest

TEMPLATE = Path(__file__).resolve().parents[1] / "project_template"


def load():
    spec = importlib.util.spec_from_file_location("new_project", TEMPLATE / "new_project.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_new_project(tmp_path):
    np_ = load()
    folder = np_.create("Test Job", "tj", tmp_path, date="20261011", fea_local=tmp_path / "local", git=False)
    assert folder.name == "20261011 - Test Job"
    for d in ["00 Admin", "01 Transfer in", "02 Design basis", "03 FEA/models", "03 FEA/snapshots", "03 FEA/results",
              "04 Code/calc", "05 Calculation", "06 CAD/out", "07 Review/markups", "08 Report/source",
              "09 Publish", "99 Archive"]:
        assert (folder / d).is_dir(), d
    assert (folder / "04 Code" / ".gitignore").is_file()
    assert (tmp_path / "local" / folder.name / "FEA run").is_dir()
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix in {".md", ".py", ".csv"}:
            assert "{{" not in p.read_text(encoding="utf-8"), p
    assert "TJ" in (folder / "04 Code" / "project.py").read_text(encoding="utf-8")

    sys.path.insert(0, str(folder / "04 Code"))
    try:
        import paths
        assert paths.ROOT == folder.resolve()
        assert paths.FEA_RUN == tmp_path / "local" / folder.name / "FEA run"
        import project
        with pytest.raises(SystemExit):
            project.need(project.FONT, "FONT")
    finally:
        sys.path.remove(str(folder / "04 Code"))
        sys.modules.pop("paths", None)
        sys.modules.pop("project", None)

    with pytest.raises(SystemExit):
        np_.create("Test Job", "tj", tmp_path, date="20261011", git=False)
