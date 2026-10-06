# -*- coding: utf-8 -*-
import sys, math, json
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
import ezdxf
from ezdxf.math import BoundingBox
P=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
doc=ezdxf.readfile(P); msp=doc.modelspace()
XMAX=40000  # foundation panel

def walk(entities, depth=0):
    for e in entities:
        yield e
        if e.dxftype()=="INSERT" and depth<6:
            try: yield from walk(e.virtual_entities(), depth+1)
            except Exception: pass

xr=[e for e in msp if e.dxftype()=="INSERT" and e.dxf.name.startswith("Xr-Grid") and e.dxf.insert[0]<XMAX]
lines=[]; balls=[]; dims=[]
for e in walk(xr):
    L=e.dxf.layer
    if e.dxftype()=="LINE" and L.endswith("$Grid"):
        s,t=e.dxf.start,e.dxf.end; lines.append((s.x,s.y,t.x,t.y))
    elif e.dxftype()=="INSERT" and L.endswith("$BALL"):
        lab=[a.dxf.text.strip() for a in e.attribs if a.dxf.text.strip()]
        # fallback: text inside ball block
        if not lab:
            for v in e.virtual_entities():
                if v.dxftype() in ("TEXT","ATTDEF","MTEXT"):
                    tt=(v.dxf.text if v.dxftype()!="MTEXT" else v.plain_text()).strip()
                    if tt: lab.append(tt)
        balls.append((e.dxf.insert.x,e.dxf.insert.y,lab))
    elif e.dxftype()=="DIMENSION":
        try: m=e.get_measurement()
        except Exception: m=None
        dims.append((round(e.dxf.defpoint.x),round(e.dxf.defpoint.y),m))

vert=[];hor=[]
for x1,y1,x2,y2 in lines:
    if abs(x1-x2)<1: vert.append((round(x1,1),min(y1,y2),max(y1,y2)))
    elif abs(y1-y2)<1: hor.append((round(y1,1),min(x1,x2),max(x1,x2)))
    else: print("  inclined grid line:",(round(x1),round(y1),round(x2),round(y2)))
print("vertical grid lines x:",sorted(v[0] for v in vert))
print("horizontal grid lines y:",sorted(h[0] for h in hor))
print("\nbubbles (x,y,label):")
for b in sorted(balls): print("  ",round(b[0]),round(b[1]),b[2])
print("\ndimensions (defpoint, measurement):")
for d in sorted(dims): print("  ",d)

# ---- columns ----
cols=[]
for e in msp:
    if e.dxftype()=="INSERT" and e.dxf.layer in("S-CONT_COL","S-Column_H") and e.dxf.insert[0]<XMAX:
        bb=BoundingBox()
        for v in walk([e]):
            if v.dxftype() in ("LWPOLYLINE","LINE","HATCH","SOLID"):
                try:
                    if v.dxftype()=="LWPOLYLINE": bb.extend([(p[0],p[1]) for p in v.get_points()])
                    elif v.dxftype()=="LINE": bb.extend([v.dxf.start,v.dxf.end])
                    elif v.dxftype()=="SOLID": bb.extend([v.dxf.vtx0,v.dxf.vtx1,v.dxf.vtx2,v.dxf.vtx3])
                except Exception: pass
        if bb.has_data:
            cx=(bb.extmin.x+bb.extmax.x)/2; cy=(bb.extmin.y+bb.extmax.y)/2
            w=bb.extmax.x-bb.extmin.x; h=bb.extmax.y-bb.extmin.y
            cols.append({"blk":e.dxf.name,"layer":e.dxf.layer,"ins":(round(e.dxf.insert.x,1),round(e.dxf.insert.y,1)),
                         "rot":round(e.dxf.rotation,1),"cx":round(cx,1),"cy":round(cy,1),"w":round(w),"h":round(h)})
print(f"\ncolumns in foundation panel: {len(cols)}")
for c in sorted(cols,key=lambda c:(c['cy'],c['cx'])): print("  ",c)
json.dump({"vert":vert,"hor":hor,"balls":[(b[0],b[1],b[2]) for b in balls],"dims":dims,"cols":cols},
          open(SC+"/fs_gridcols.json","w"),indent=1,default=str)
