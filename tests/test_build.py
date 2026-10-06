"""
Smoke test: every job builds its DXF without AutoCAD, prints no "!!" layout problem and exits 0; the ezdxf
plot fallback renders whole sets without AutoCAD.

    pip install -r requirements-dev.txt
    pytest -q

Plotting with AutoCAD Core Console is not tested here. Each build runs in its own process, because the engines
create their drawing at import (one set per process, see docs/general/DRAWING_ENGINE.md).
"""
import os
import subprocess
import sys
from pathlib import Path

import ezdxf
import pytest

JOBS = Path(__file__).resolve().parents[1] / "jobs"
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}


def run(job, *args, cwd=None):
    res = subprocess.run([sys.executable, *args], cwd=cwd or JOBS / job, env=ENV,
                         capture_output=True, text=True, encoding="utf-8", timeout=300)
    out = res.stdout + res.stderr
    problems = [ln.strip() for ln in out.splitlines() if ln.lstrip().startswith("!!")]
    assert res.returncode == 0, f"{job} {' '.join(args)} exited {res.returncode}:\n{out[-3000:]}"
    assert not problems, f"{job} {' '.join(args)} reported layout problems:\n" + "\n".join(problems)
    return out


def check_dxf(path, min_layouts):
    assert path.exists(), f"{path} not written"
    doc = ezdxf.readfile(path)
    assert not doc.audit().has_errors, f"{path.name}: DXF audit errors"
    sheets = [n for n in doc.layouts.names() if n != "Model"]
    assert len(sheets) >= min_layouts, f"{path.name}: {len(sheets)} sheets, expected >= {min_layouts}"


@pytest.mark.parametrize("set_, base, sheets", [
    ("columns", "STR-ST-1101_Typical_Column_Details_A3_R2", 4),
    ("beams", "STR-ST-1111_Typical_Beam_Details_A3_R2", 6),
    ("slabs", "STR-ST-1121_Typical_Slab_Details_A3_R2", 8),
])
def test_standard_set_r2(set_, base, sheets):
    run("standard_set_R2", "build.py", set_)
    job = JOBS / "standard_set_R2"
    check_dxf(job / "out" / f"{base}.dxf", sheets)
    assert (job / "library" / f"INDEX_{set_}.csv").exists()


def test_general_notes_rev_b():
    run("standard_set", "build.py", "gn")
    check_dxf(JOBS / "standard_set" / "out" / "STR-ST-1001_General_Notes_Concrete_A3_RevA.dxf", 3)


@pytest.mark.parametrize("job, script, dxf, sheets", [
    ("general_notes", "build_gn.py", "STR-ST-1001_General_Notes_Concrete_A3_RevA.dxf", 1),
    ("stair_demo", "build_stair.py", "STR-ST_Stair_ST-1_A3_RevA.dxf", 1),
    ("nooker_rw", "build_rw.py", "NRW-ST_Retaining_Wall_A3_RevB.dxf", 7),
])
def test_job(tmp_path, job, script, dxf, sheets):
    run(job, str(JOBS / job / script), str(tmp_path), cwd=tmp_path)
    check_dxf(tmp_path / dxf, sheets)


@pytest.mark.parametrize("job, build, plot, pdf, pages", [
    ("stair_demo", ["build_stair.py"], ["plot_stair.py"], "STR-ST_Stair_ST-1_A3_RevA.pdf", 1),
    ("standard_set_R2", ["build.py", "slabs"], ["plot.py", "slabs"], "STR-ST-1121_Typical_Slab_Details_A3_R2.pdf", 8),
])
def test_plot_without_autocad(tmp_path, job, build, plot, pdf, pages):
    """the ezdxf fallback plots a whole set (slabs: hatches in scaled detail blocks, stair: a blank-text dimension)"""
    import pymupdf
    if job == "standard_set_R2":                   # fixed output folders next to the scripts
        run(job, *build)
        run(job, *plot, "--ezdxf")
        out = JOBS / job / "out"
    else:
        run(job, str(JOBS / job / build[0]), str(tmp_path), cwd=tmp_path)
        run(job, str(JOBS / job / plot[0]), str(tmp_path), "--ezdxf", cwd=tmp_path)
        out = tmp_path
    with pymupdf.open(out / pdf) as d:
        assert d.page_count == pages
        assert all(pg.get_drawings() for pg in d), "an empty page"


def test_steel_roof_truss():
    """design (every member and joint passes) and the five SRT sheets"""
    run("steel_roof_truss", "build.py")
    check_dxf(JOBS / "steel_roof_truss" / "out" / "SRT-ST_Steel_Roof_Truss_T1_A3_RevA.dxf", 5)


def test_steel_portal_frame(tmp_path):
    """connection calc from the MIDAS snapshot (no connection check fails) and the eight A1 SPF sheets"""
    out = run("steel_portal_frame", "calc_spf.py")
    assert "!! FAIL" not in out
    run("steel_portal_frame", str(JOBS / "steel_portal_frame" / "build.py"), str(tmp_path), cwd=tmp_path)
    check_dxf(tmp_path / "SPF-ST_Steel_Portal_Frame_A1_RevA.dxf", 8)


def test_retaining_wall_calc():
    out = run("nooker_rw", "calc_rw.py")
    assert "FSot=" in out and "psi_t = 1.3" in out
