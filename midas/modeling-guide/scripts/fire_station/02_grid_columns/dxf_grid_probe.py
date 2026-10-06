# -*- coding: utf-8 -*-
import sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
import ezdxf
P=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
doc=ezdxf.readfile(P); msp=doc.modelspace()

def walk(entities, depth=0):
    for e in entities:
        if e.dxftype()=="INSERT" and depth<6:
            yield e
            try:
                yield from walk(e.virtual_entities(), depth+1)
            except Exception: pass
        else:
            yield e

# Xr-Grid inserts in modelspace
xr=[e for e in msp if e.dxftype()=="INSERT" and e.dxf.name.startswith("Xr-Grid")]
print("Xr-Grid inserts:", [(round(e.dxf.insert[0]),round(e.dxf.insert[1])) for e in xr])
bl=doc.blocks.get("Xr-Grid-อาคารดับเพลิง")
print("xref block content:", [ (e.dxftype(), getattr(e.dxf,'name','')) for e in bl])

lay=Counter(); txt=[]
for e in walk(xr):
    lay[(e.dxftype(), e.dxf.layer)]+=1
    if e.dxftype() in ("TEXT","ATTRIB","MTEXT"):
        t=(e.plain_text() if e.dxftype()=="MTEXT" else e.dxf.text).strip()
        if t: txt.append((round(e.dxf.insert[0]),round(e.dxf.insert[1]),e.dxf.layer,t))
print("\nentities inside grid xref (type,layer):")
for k,c in lay.most_common(30): print("  ",k,c)
print("\ntexts in grid xref (first 60):")
for t in sorted(txt)[:60]: print("  ",t)

# modelspace S-GRID layer
print("\nS-GRID msp entities:", Counter(e.dxftype() for e in msp if e.dxf.layer=="S-GRID"))
# column layers
for L in ["S-CONT_COL","S-Column_H","S-HID_COL","S-CX_COL","COL","S-Col-continuous"]:
    c=Counter(e.dxftype() for e in walk(msp) if e.dxf.layer==L)
    if c: print(f"layer {L}: {dict(c)}")
