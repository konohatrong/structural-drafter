"""
drafter.steel.weld(): the V and double-V (X) groove symbol (groove="V"; guide §9.3 item 7, steel S5.7, 2026-10-19).
The engine opens its drawing at import (one set per process, DRAWING_ENGINE.md), so the symbol is drawn in a child
process on a fresh model space and its entities come back as JSON.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}

SCRIPT = r"""
import json, sys
sys.path.insert(0, sys.argv[1])
from drafter.steel import *
import ezdxf
kw = json.loads(sys.argv[2])
sp = ezdxf.new().modelspace()
weld(sp, (0.0, 0.0), (20.0, 15.0), 1.0, "E", **kw)
out = []
for e in sp:
    t = e.dxftype()
    if t == "LINE":
        out.append([t, e.dxf.layer, list(e.dxf.start)[:2], list(e.dxf.end)[:2]])
    elif t == "LWPOLYLINE":
        out.append([t, e.dxf.layer, [list(p[:2]) for p in e.get_points()]])
    elif t == "TEXT":
        out.append([t, e.dxf.layer, e.dxf.text, list(e.dxf.align_point)[:2]])
    else:
        out.append([t, e.dxf.layer])
print(json.dumps(out))
"""


def draw(**kw):
    res = subprocess.run([sys.executable, "-c", SCRIPT, str(ROOT), json.dumps(kw)], env=ENV,
                         capture_output=True, text=True, encoding="utf-8", timeout=120)
    assert res.returncode == 0, res.stdout + res.stderr
    return json.loads(res.stdout.strip().splitlines()[-1])


def close(p, q):
    return abs(p[0] - q[0]) < 1e-9 and abs(p[1] - q[1]) < 1e-9


def test_double_v_groove():
    ents = draw(groove="V", side="both")
    ref, tip, S = (20.0, 15.0), (0.0, 0.0), 1.0
    xs, tri = ref[0] + 7.0 * S, 2.4 * S
    vx = (xs + tri / 2, ref[1])                                          # the V vertex, on the reference line
    assert all(e[1] == ("S-TEXT" if e[0] == "TEXT" else "S-ANNO") for e in ents)
    assert not [e for e in ents if e[0] == "LWPOLYLINE"], "no broken arrow, no fillet triangle"
    lines = [(e[2], e[3]) for e in ents if e[0] == "LINE"]
    assert any(close(a, ref) and close(b, (ref[0] + 16.0 * S, ref[1])) for a, b in lines), "reference line"
    assert any(close(a, ref) and close(b, tip) for a, b in lines), "straight arrow, junction to the joint"
    assert len([e for e in ents if e[0] == "SOLID"]) == 1, "one arrowhead"
    legs = [b for a, b in lines if close(a, vx)]
    assert len(legs) == 4, "two legs each side of the line"
    for sd in (-1, 1):                                                  # each V opens away from the line
        assert any(close(b, (xs, ref[1] + sd * tri)) for b in legs)
        assert any(close(b, (xs + tri, ref[1] + sd * tri)) for b in legs)
    labels = [e for e in ents if e[0] == "TEXT"]
    assert [e[2] for e in labels] == ["(E)", "(E)"], "groove size (E) on both sides"
    assert sorted(e[3][1] > ref[1] for e in labels) == [False, True]


def test_single_v_arrow_side():
    ents = draw(groove="V")
    legs = [e for e in ents if e[0] == "LINE" and close(e[2], (28.2, 15.0))]
    assert len(legs) == 2 and all(e[3][1] < 15.0 for e in legs), "V below the line on the arrow side"


def test_unknown_groove_is_refused():
    with pytest.raises(AssertionError, match="groove="):
        draw(groove="J")
