# -*- coding: utf-8 -*-
import sys, json
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")
import ezdxf
from ezdxf.math import BoundingBox
P=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
doc=ezdxf.readfile(P); msp=doc.modelspace()
GX={1:0,2:2250,3:8750,4:12750,5:19250,6:23550,7:27250}
GY={"F":0,"E":4000,"D":8000,"C":11000,"B":12000,"A":14300}

cache={}
def vis_info(bn):
    if bn in cache: return cache[bn]
    blk=doc.blocks.get(bn); bb=BoundingBox(); lays=set()
    for e in blk:
        if e.dxf.get("invisible",0): continue
        lays.add(e.dxf.layer)
        try:
            if e.dxftype()=="LWPOLYLINE": bb.extend([(p[0],p[1]) for p in e.get_points()])
            elif e.dxftype()=="LINE": bb.extend([e.dxf.start,e.dxf.end])
        except Exception: pass
    cache[bn]=(bb,lays); return cache[bn]

xr=sorted([e.dxf.insert.x for e in msp if e.dxftype()=="INSERT" and e.dxf.name.startswith("Xr-Grid")])
origins=[x-33 for x in xr]           # grid-1 world x of each panel (foundation panel xref at 33 -> grid1 x=0)
names=["Foundation","Ground-beam +0.35","2nd floor +4.65","3rd floor +7.95","Roof +11.15"]
print("panel grid-1 origins:",[round(o) for o in origins])

res=defaultdict(dict)
for e in msp:
    if e.dxftype()!="INSERT": continue
    bb,lays=vis_info(e.dxf.name) if e.dxf.name in doc.blocks else (None,set())
    if not bb or not bb.has_data: continue
    if not any("col" in L.lower() for L in lays): continue
    x,y=e.dxf.insert.x,e.dxf.insert.y
    pi=min(range(len(origins)),key=lambda i:abs(x-origins[i]-13000))
    lx=x-origins[pi]; ly=y
    gx=min(GX,key=lambda k:abs(GX[k]-lx)); gy=min(GY,key=lambda k:abs(GY[k]-ly))
    dx=lx-GX[gx]; dy=ly-GY[gy]
    w=round(bb.extmax.x-bb.extmin.x); h=round(bb.extmax.y-bb.extmin.y)
    if abs(e.dxf.rotation)%180==90: w,h=h,w
    kind=",".join(sorted(L for L in lays if "col" in L.lower()))
    res[pi][f"{gy}{gx}"]=(w,h,round(dx),round(dy),kind)

allkeys=sorted({k for p in res.values() for k in p},key=lambda k:("FEDCBA".index(k[0]),int(k[1:])))
print(f"\n{'grid':6}"+"".join(f"{names[i][:12]:>26}" for i in range(len(origins))))
for k in allkeys:
    row=f"{k:6}"
    for i in range(len(origins)):
        v=res[i].get(k)
        row+=f"{(f'{v[0]}x{v[1]} d({v[2]},{v[3]}) {v[4][:9]}' if v else '-'):>26}"
    print(row)
json.dump({str(i):res[i] for i in res},open(SC+"/fs_cols_floors.json","w"),indent=1)
