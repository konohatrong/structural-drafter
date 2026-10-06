# -*- coding: utf-8 -*-
import sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
import ezdxf
P=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
doc=ezdxf.readfile(P); msp=doc.modelspace()
O=[0,45778,91555,137333,183111]; N=["FDN","GB","2F","3F","RF"]
def pan(x): return min(range(5),key=lambda i:abs(x-O[i]-13000))

c=Counter()
for e in msp:
    x=None
    try:
        if e.dxftype()=="MLINE": x=e.vertices[0].location.x if e.vertices else None
        elif e.dxftype()=="LINE": x=e.dxf.start.x
        elif e.dxftype()=="LWPOLYLINE": x=list(e.get_points())[0][0]
    except Exception: pass
    if x is None: continue
    c[(N[pan(x)],e.dxftype(),e.dxf.layer)]+=1
for k,v in sorted(c.items()): print(k,v)

print("\n--- sample MLINEs (2F) ---")
n=0
for e in msp:
    if e.dxftype()=="MLINE" and e.vertices and pan(e.vertices[0].location.x)==2:
        pts=[(round(v.location.x-O[2]),round(v.location.y)) for v in e.vertices]
        print(f"  layer={e.dxf.layer} style={e.dxf.style_name} just={e.dxf.justification} scale={e.dxf.scale_factor} pts={pts}")
        n+=1
        if n>12: break
st={}
for s in doc.mline_styles:
    st[s.dxf.name]=[(round(el.offset,1)) for el in s.elements]
print("\nMLINE styles offsets:",st)
