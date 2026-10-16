"""
drafter.fullsize: a composed sheet (engine form: a 1:100 view inserted at SC / 100 on a 1:25 frame, a paper-level
title at x 25, the layout's viewport onto the frame) becomes full-size model space with a locked viewport at 1:100.
No AutoCAD needed.
"""
import ezdxf
import pytest

from drafter import fullsize

SC = 25.0


def composition():
    doc = ezdxf.new("R2018", setup=True)
    doc.header["$LTSCALE"] = 3.75
    doc.layers.add("S-SHEET")
    doc.layers.add("S-VPORT")
    msp = doc.modelspace()
    blk = doc.blocks.new("DET-S1-01-A", base_point=(0, 0, 0))
    blk.add_line((0, 0), (29650, 0))                                  # 29.65 m at full size
    blk.add_line((0, 1000), (29650, 1000), dxfattribs={"linetype": "DASHED"})
    msp.add_blockref("DET-S1-01-A", (40 * SC, 100 * SC), dxfattribs={"xscale": SC / 100, "yscale": SC / 100})
    msp.add_text("PLAN", dxfattribs={"insert": (40 * SC, 90 * SC), "height": 4 * SC})
    msp.add_lwpolyline([(0, 0), (420 * SC, 0), (420 * SC, 297 * SC), (0, 297 * SC)], close=True,
                       dxfattribs={"layer": "S-SHEET"})
    lay = doc.layouts.new("S1-01")
    lay.add_viewport(center=(210, 148.5), size=(420, 297), view_center_point=(210 * SC, 148.5 * SC),
                     view_height=297 * SC)
    return doc


def test_full_size_view_and_viewport():
    doc = composition()
    rec = fullsize.convert(doc, sc=SC, pad=0.0)
    ins = [e for e in doc.modelspace().query("INSERT") if e.dxf.name.startswith("DET-")]
    assert len(ins) == 1 and ins[0].dxf.xscale == pytest.approx(1.0)
    assert rec[0]["scale"] == pytest.approx(100.0)
    assert rec[0]["model_size_mm"][0] == 29650
    lay = doc.layouts.get("S1-01")
    vps = [v for v in lay.query("VIEWPORT") if abs(v.dxf.width - 420) > 1e-6]      # the sheet's own viewport aside
    assert len(vps) == 1
    v = vps[0]
    assert v.dxf.view_height / v.dxf.height == pytest.approx(100.0)          # 1:100
    assert v.dxf.flags & fullsize.VP_LOCKED
    assert v.dxf.center.x == pytest.approx(40 + 29650 / 100 / 2)              # where the view was on the sheet


def test_paper_items_and_linetypes():
    doc = composition()
    fullsize.convert(doc, sc=SC)
    lay = doc.layouts.get("S1-01")
    t = next(e for e in lay.query("TEXT"))
    assert t.dxf.insert.x == pytest.approx(40) and t.dxf.height == pytest.approx(4)
    assert not list(doc.modelspace().query("TEXT"))
    assert not [e for e in doc.modelspace() if e.dxf.layer == "S-SHEET"]
    assert doc.header["$LTSCALE"] == pytest.approx(15.0)                       # 3.75 x 100 / 25
    assert doc.header["$PSLTSCALE"] == 0
    dashed = next(e for e in doc.blocks.get("DET-S1-01-A") if e.dxf.get("linetype") == "DASHED")
    assert dashed.dxf.get("ltscale", 1.0) == pytest.approx(1.0)               # a 1:100 view keeps ltscale 1
    assert not fullsize.overlaps(doc)
    assert not doc.audit().has_errors
