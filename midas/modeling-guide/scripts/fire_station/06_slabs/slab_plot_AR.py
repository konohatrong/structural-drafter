# -*- coding: utf-8 -*-
# Annex roof slab (+3.95) review sheet. The annex plan is drawn displaced on the 2F sheet by (+2645, +7802).
import sys, json, math, textwrap
sys.stdout.reconfigure(encoding="utf-8")
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import ezdxf, logging; logging.disable(logging.WARNING)
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, TextPolicy, ColorPolicy
from slab_faces import faces, simplify
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
DXF=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
O,SH=91555,(2645,7802); MESH=0.5; L="AR"
A=json.load(open(SC+"/fs_annex.json")); CM=json.load(open(SC+"/fs_colmodel.json"))
doc=ezdxf.readfile(DXF); msp=doc.modelspace()
def inA(x,y): x-=O; return x>25000 and 6500<y<17500 and x<33000
def loc(x,y): return (x-O-SH[0],y-SH[1])
def inside(pt,P):
    x,y=pt; c=False
    for i in range(len(P)):
        (x1,y1),(x2,y2)=P[i-1],P[i]
        if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1: c=not c
    return c
sfl=[]; edges=[]
for e in msp:
    if e.dxftype()=="INSERT" and e.dxf.name=="Sym-SFL" and inA(e.dxf.insert.x,e.dxf.insert.y):
        v=[a.dxf.text.strip() for a in e.attribs]; p=loc(e.dxf.insert.x,e.dxf.insert.y)
        sfl.append((p[0],p[1],[t for t in v if t.startswith("+")][0],[t for t in v if t[:1].isalpha() and t[1:2].isalnum()][-1]))
    if e.dxf.layer=="S-EDGE_SLAB" and e.dxftype()=="LWPOLYLINE":
        P=list(e.get_points("xyb"))
        if all(inA(p[0],p[1]) for p in P): edges.append([loc(p[0],p[1])+(p[2],) for p in P])
print("SFL:",[(round(a),round(b),c,d) for a,b,c,d in sfl]); print("slab edges:",[[tuple(round(v,3) for v in q) for q in P] for P in edges])
F=faces(A["elems"]); F.sort(key=lambda f:min(p[1] for p in f["poly"]))
panels=[]
for k,f in enumerate(F):
    tags=[s for s in sfl if inside((s[0],s[1]),f["poly"])]
    corners=simplify(f["poly"]); rect=len(corners)==4
    panels.append(dict(no=k+1,name=f"AR-P{k+1:02d}",poly=f["poly"],corners=corners,area=round(f["area"],3),edges=f["edges"],
                       type=tags[0][3] if tags else None,levels=sorted({t[2] for t in tags}),mesh="Quadrilateral" if rect else "Quad and Triangle",
                       est=round(f["area"]/MESH**2),opening=False,method="beams"))
json.dump(dict(level=L,z=A["z"],mesh=MESH,panels=panels),open(SC+"/fs_slab_AR.json","w"),indent=1)
for p in panels: print(p["name"],p["type"],p["levels"],p["area"],p["mesh"],"~",p["est"])
# ---- sheet ----
cfg=Configuration(text_policy=TextPolicy.IGNORE,color_policy=ColorPolicy.CUSTOM,custom_fg_color="#c9ced4")
fig=plt.figure(figsize=(15,10)); fig.patch.set_facecolor("white")
ax=fig.add_axes([0.03,0.07,0.62,0.83])
Frontend(RenderContext(doc),MatplotlibBackend(ax),config=cfg).draw_layout(msp,finalize=False)
ox,oy=O+SH[0],SH[1]
for p in panels:
    ax.add_patch(Polygon([(ox+x,oy+y) for x,y in p["poly"]],closed=True,fc="#d5a6bd",ec="none",alpha=0.55,zorder=3))
    xs=[x for x,y in p["poly"]]; ys=[y for x,y in p["poly"]]; poly=Polygon([(ox+x,oy+y) for x,y in p["poly"]],closed=True,transform=ax.transData)
    for gx in range(int(min(xs)//500)*500,int(max(xs))+1,500):
        ln,=ax.plot([ox+gx]*2,[oy+min(ys),oy+max(ys)],color="white",lw=0.6,zorder=4); ln.set_clip_path(poly)
    for gy in range(int(min(ys)//500)*500,int(max(ys))+1,500):
        ln,=ax.plot([ox+min(xs),ox+max(xs)],[oy+gy]*2,color="white",lw=0.6,zorder=4); ln.set_clip_path(poly)
    cx=sum(xs)/len(xs); cy=sum(ys)/len(ys)
    ax.text(ox+cx,oy+cy,f"P{p['no']:02d}\n{p['type']}  {p['area']:.2f} m²"+("\nquad+tri" if p["mesh"]!="Quadrilateral" else ""),ha="center",va="center",
            fontsize=9,weight="bold",zorder=9,bbox=dict(fc="white",ec="#555",lw=0.5,pad=0.3,alpha=0.9))
for e in A["elems"]:
    (x1,y1),(x2,y2)=e["a"],e["b"]; ax.plot([ox+x1,ox+x2],[oy+y1,oy+y2],color="#1f3b73",lw=2,zorder=6)
for k,v in A["colnodes"].items():
    x,y=[float(t)*1000 for t in k.split(",")]; ax.plot(ox+x,oy+y,"s",ms=9,color="#222",zorder=7)
for s in sfl: ax.plot(ox+s[0],oy+s[1]-250,"v",ms=8,color="#2e7d32",zorder=8)
for k,x in CM["GX"].items():
    if x<20: continue
    X=ox+x*1000; ax.plot([X,X],[oy-1500,oy+9600],color="#7f8c99",lw=0.6,ls=(0,(10,4,2,4)),zorder=2)
    ax.add_patch(plt.Circle((X,oy+10200),330,fc="white",ec="#222",zorder=8)); ax.text(X,oy+10200,k,ha="center",va="center",fontsize=11,weight="bold",zorder=9)
for k,y in CM["GY"].items():
    if y>8.5: continue
    Y=oy+y*1000; ax.plot([ox+21500,ox+29000],[Y,Y],color="#7f8c99",lw=0.6,ls=(0,(10,4,2,4)),zorder=2)
    ax.add_patch(plt.Circle((ox+20900,Y),330,fc="white",ec="#222",zorder=8)); ax.text(ox+20900,Y,k,ha="center",va="center",fontsize=11,weight="bold",zorder=9)
ax.set_xlim(ox+20300,ox+29200); ax.set_ylim(oy-1600,oy+10700); ax.set_aspect("equal"); ax.axis("off")
fig.text(0.03,0.95,f"EAST ANNEX ROOF SLAB   Z = +{A['z']:.2f} m   (grids 6–7 × F–D)",fontsize=16,weight="bold")
fig.text(0.03,0.925,"Slab panels = closed bays of the annex roof beams (dark blue), on the annex plan as drawn in the DXF (displaced on the 2F sheet). White grid = 0.50 m.",fontsize=9.5,color="#444")
sx=fig.add_axes([0.68,0.07,0.30,0.83]); sx.axis("off"); sx.set_xlim(0,1); sx.set_ylim(0,1); yy=0.98
sx.text(0,yy,"SLAB PANELS",fontsize=11,weight="bold",va="top"); yy-=0.06
sx.add_patch(plt.Rectangle((0,yy-0.012),0.07,0.024,fc="#d5a6bd",ec="#555",lw=0.5)); sx.text(0.1,yy,f"RS1  t = 180 mm  (thickness 4)  × {len(panels)}",fontsize=10,va="center"); yy-=0.05
sx.text(0,yy,f"Slab {sum(p['area'] for p in panels):.2f} m²   ~{sum(p['est'] for p in panels)} plates at 0.50 m",fontsize=10,weight="bold"); yy-=0.04
sx.text(0,yy,"Thick plate, C280, no offset, at beam level +3.95",fontsize=9.5); yy-=0.07
sx.text(0,yy,"NOTES / ASSUMPTIONS",fontsize=10,weight="bold"); yy-=0.04
for n in ["Two RS1 panels, both tagged +3.95: F–E rectangle and the E–D bay with the curved edge (same 6 chords as the ground beam; the 0.30 m straight leg at E7 included).",
          "No overhang: the DXF slab edge follows the outer faces of the annex beams (row F, grid 7, curve) and stops at the far face of the grid-6 beam.",
          "Grid-6 edge is the +3.95 grid-6 beam added for the annex roof (your option A); the 2F beam at +4.75 above is not connected to this slab.",
          "No openings."]:
    w=textwrap.fill("• "+n,58); sx.text(0,yy,w,fontsize=9,va="top"); yy-=0.033*(w.count("\n")+1)+0.02
fig.savefig(SC+"/fs_slab_AR.png",dpi=110,facecolor="white"); print("saved fs_slab_AR.png")
