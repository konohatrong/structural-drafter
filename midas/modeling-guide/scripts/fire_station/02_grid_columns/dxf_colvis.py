# -*- coding: utf-8 -*-
import sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
import ezdxf
from ezdxf.math import BoundingBox
P=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
doc=ezdxf.readfile(P)
for bn in ["*U115","*U116"]:
    blk=doc.blocks.get(bn)
    base=blk.block.dxf.base_point
    vis=[e for e in blk if not e.dxf.get("invisible",0)]
    inv=[e for e in blk if e.dxf.get("invisible",0)]
    print(f"\n{bn}: base={tuple(round(v,1) for v in base)} total={len(blk)} visible={len(vis)} invisible={len(inv)}")
    print("  visible types:",Counter((e.dxftype(),e.dxf.layer) for e in vis))
    bb=BoundingBox()
    for e in vis:
        try:
            if e.dxftype()=="LWPOLYLINE": bb.extend([(p[0],p[1]) for p in e.get_points()])
            elif e.dxftype()=="LINE": bb.extend([e.dxf.start,e.dxf.end])
            elif e.dxftype()=="HATCH":
                for path in e.paths:
                    if hasattr(path,"vertices"): bb.extend([(v[0],v[1]) for v in path.vertices])
                    else:
                        for ed in path.edges:
                            if hasattr(ed,"start"): bb.extend([ed.start,ed.end])
        except Exception as ex: pass
    if bb.has_data:
        print(f"  visible bbox x[{bb.extmin.x:.0f},{bb.extmax.x:.0f}] y[{bb.extmin.y:.0f},{bb.extmax.y:.0f}]"
              f"  -> size {bb.extmax.x-bb.extmin.x:.0f} (X) x {bb.extmax.y-bb.extmin.y:.0f} (Y)")
# visibility-state info from extension dict of the source dynamic block
for b in doc.blocks:
    if b.name=="Col-Continuous":
        print("\nCol-Continuous block record handle:", b.block_record.dxf.handle)
