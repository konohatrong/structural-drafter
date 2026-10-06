# -*- coding: utf-8 -*-
import sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
import ezdxf
P=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
doc=ezdxf.readfile(P)
msp=doc.modelspace()

# block definitions
print("=== BLOCK DEFINITIONS (name: entity count) ===")
for b in doc.blocks:
    n=b.name
    if n.startswith("*") and n[1] in "DAT": continue
    cnt=Counter(e.dxftype() for e in b)
    if sum(cnt.values())>0:
        print(f"  {n:32} {dict(cnt)}")

def dump_texts(container, tag):
    txts=[]
    for e in container:
        if e.dxftype() in ("TEXT","MTEXT","ATTRIB"):
            try:
                t=e.plain_text() if e.dxftype()=="MTEXT" else e.dxf.text
            except: t=getattr(e.dxf,"text","")
            t=t.strip()
            if t:
                p=e.dxf.insert if hasattr(e.dxf,"insert") else (0,0)
                txts.append((round(p[0],0),round(p[1],0),e.dxf.layer,t))
    return txts

mt=dump_texts(msp,"msp")
print(f"\n=== MODELSPACE TEXT ({len(mt)}) — grouped by X-band (plan columns) ===")
# group by X into ~5 bands to see 5 plans
mt.sort()
for x,y,lay,t in mt:
    print(f"  x={x:>9.0f} y={y:>8.0f} [{lay[:22]:22}] {t[:45]}")
