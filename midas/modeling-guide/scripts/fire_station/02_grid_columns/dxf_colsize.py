# -*- coding: utf-8 -*-
import sys, math
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
import ezdxf
from ezdxf.math import Vec3
P=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
doc=ezdxf.readfile(P); msp=doc.modelspace()

# marks in foundation panel
marks=[]
for e in msp:
    if e.dxftype()=="TEXT":
        t=e.dxf.text.strip(); p=e.dxf.insert
        if p[0]<40000 and (",C1" in t or ",C2" in t):
            marks.append((p[0],p[1],t.split(",")[-1]))

# collect candidate column rectangles by exploding inserts (virtual_entities keeps transforms)
rects=[]  # (cx,cy,w,h)
def add_rect(pts):
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    w=max(xs)-min(xs); h=max(ys)-min(ys)
    if 120<=w<=800 and 120<=h<=800 and abs(w-h)<800:
        rects.append(((min(xs)+max(xs))/2,(min(ys)+max(ys))/2,round(w),round(h)))
for e in msp:
    if e.dxftype()=="INSERT":
        try:
            for se in e.virtual_entities():
                if se.dxftype()=="LWPOLYLINE" and se.closed:
                    add_rect([Vec3(x,y) for x,y,*_ in se.get_points()])
                elif se.dxftype()=="LWPOLYLINE":
                    p=[Vec3(x,y) for x,y,*_ in se.get_points()]
                    if len(p)>=4: add_rect(p)
        except Exception: pass
    elif e.dxftype()=="LWPOLYLINE":
        p=[Vec3(x,y) for x,y,*_ in e.get_points()]
        if len(p)>=4: add_rect(p)

# also restrict to foundation panel
rects=[r for r in rects if r[0]<40000]
print("candidate column rects in foundation panel:", len(rects))

# match each mark to nearest rect
res=defaultdict(Counter)
for mx,my,mk in marks:
    best=None; bd=1e9
    for cx,cy,w,h in rects:
        d=math.hypot(cx-mx,cy-my)
        if d<bd: bd=d; best=(w,h,d)
    if best and best[2]<2500:
        res[mk][(min(best[0],best[1]),max(best[0],best[1]))]+=1
for mk in sorted(res):
    print(f"  {mk}: sizes(min,max)->count {dict(res[mk])}")
