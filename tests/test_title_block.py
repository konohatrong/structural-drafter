"""
The title-block field check (td_engine.tb_check, DRAWING_ENGINE.md §3): a value wider than its cell is a "!!"
warning, once per field and value; a value that fits, a field the metrics cannot measure (Thai) and an empty field
are not. Case: RPM R3 (22/10/2026), "FOR SUBMISSION: F1 MID LANDING ON PILES" ran into the date column unchecked.
Runs in its own process: the engine creates its drawing at import.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

SCRIPT = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
from drafter import td_engine as T
T.tb_define()
T.SHEETS[:] = [("1001", ["SHEET ONE"], "N.T.S."), ("1002", ["SHEET TWO"], "N.T.S.")]
out = {"rooms": {k: round(v[0], 2) for k, v in T.TB_FIELDS.items() if k in ("REV_1_DESC", "SCALE", "TITLE_1")}}
def warnings(revs, **extra):
    T.WARNINGS.clear(); T._TB_WARNED.clear()
    T.REVS = revs
    for i, s in enumerate(("1001", "1002")):
        v = T.tb_values(s, ["SHEET"], "1:50", i + 1)
    return [w for w in T.WARNINGS]
out["fits"] = warnings([("R2", "FOR SUBMISSION: SIGNATURES", "17/10/2026")])
out["long"] = warnings([("R3", "FOR SUBMISSION: F1 MID LANDING ON PILES", "22/10/2026")])
T.PROJ["office"] = "พีรภัทร " * 8          # Thai: not measured
out["thai"] = warnings([("R1", "FOR SUBMISSION", "16/10/2026")])
print("JSON" + json.dumps(out))
'''


def run():
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, "-c", SCRIPT, str(REPO)], capture_output=True, text=True, encoding="utf-8",
                       env=env, timeout=300, cwd=REPO)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]
    line = next(ln for ln in r.stdout.splitlines() if ln.startswith("JSON"))
    return json.loads(line[4:])


def test_title_block_fields():
    out = run()
    assert out["rooms"]["REV_1_DESC"] == 36.5                # 38 mm column, text 1 mm in, 0.5 mm clear
    assert out["fits"] == []                                 # "FOR SUBMISSION: SIGNATURES" 36.0 mm
    assert len(out["long"]) == 1, out["long"]                # once for both sheets
    assert "REV_1_DESC" in out["long"][0] and "1001" in out["long"][0]
    assert out["thai"] == []
