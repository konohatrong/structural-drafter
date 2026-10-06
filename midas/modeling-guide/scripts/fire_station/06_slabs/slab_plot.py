# -*- coding: utf-8 -*-
# Slab review sheet for one level: panels = closed faces of the analytical beam graph.
# usage: python slab_plot.py GB   -> fs_slab_GB.png + fs_slab_GB.json
import sys, json, math, textwrap
from collections import Counter
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
L=sys.argv[1]
PAN={"GB":45778,"2F":91555,"3F":137333,"RF":183111}; O=PAN[L]
NAME={"GB":"GROUND FLOOR SLAB","2F":"2ND FLOOR SLAB","3F":"3RD FLOOR SLAB","RF":"ROOF SLAB"}
THK={"GS1":(1,200),"S1":(2,180),"S1C":(3,180),"RS1":(4,180)}
FC={"GS1":"#9fc5e8","S1":"#b6d7a8","S1C":"#f9cb9c","RS1":"#d5a6bd","OPENING":"#ffffff"}
MESH=0.5
# cantilever slab areas with no edge beam (meshed via temporary edge lines). Coordinates on beam centrelines, mm.
CANT={"RF":[dict(name="S1C overhang",type="S1C",poly=[(0,0),(0,-1725),(21175,-1725),(21175,9325),(16379.166666666666,9325),(19250,8000),(19250,0)],
                 free=[((0,0),(0,-1725)),((0,-1725),(21175,-1725)),((21175,-1725),(21175,9325)),((21175,9325),(16379.166666666666,9325))])],
      "2F":[dict(name="S1C wrap",type="S1C",poly=[(0,0),(0,-1725),(25275,-1725),(25275,9725),(15512.5,9725),(19250,8000),(23550,8000),(23550,0)],
                 free=[((0,0),(0,-1725)),((0,-1725),(25275,-1725)),((25275,-1725),(25275,9725)),((25275,9725),(15512.5,9725))])]}
SMALL_OPEN=1.0   # m2: openings smaller than this are not modelled
B=json.load(open(SC+"/fs_beammodel.json"))[L]; CM=json.load(open(SC+"/fs_colmodel.json"))
V=json.load(open(SC+f"/verify_{L}.json"))
sfl=[(float(s[0]),float(s[1]),s[2],s[3]) for s in V["sfl"]]

def inside(pt,P):
    x,y=pt; c=False
    for i in range(len(P)):
        (x1,y1),(x2,y2)=P[i-1],P[i]
        if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1: c=not c
    return c

def parea(P): return abs(sum(P[i-1][0]*P[i][1]-P[i][0]*P[i-1][1] for i in range(len(P))))/2e6
_doc=ezdxf.readfile(DXF); _msp=_doc.modelspace()
def _pts(e): return [(p[0]-O,p[1]) for p in e.get_points("xy")]
_diag=[_pts(e) for e in _msp if e.dxftype()=="LWPOLYLINE" and e.dxf.layer=="S-GRID" and len(list(e.get_points("xy")))==2]
openings=[]
for e in _msp:
    if e.dxftype()!="LWPOLYLINE" or e.dxf.layer!="S-EDGE_SLAB": continue
    P=_pts(e)
    if not P or not all(-4000<x<33000 for x,y in P) or (L=="2F" and any(x>25000 and y>6500 for x,y in P)): continue
    closed=e.closed or (len(P)>=4 and math.dist(P[0],P[-1])<1)
    if P[0]==P[-1]: P=P[:-1]
    if not closed or len(P)<3: continue
    xs=[x for x,y in P]; ys=[y for x,y in P]
    if any(all(min(xs)-5<=x<=max(xs)+5 and min(ys)-5<=y<=max(ys)+5 for x,y in d) for d in _diag) and parea(P)<60:
        openings.append(dict(poly=P,area=round(parea(P),2),small=parea(P)<SMALL_OPEN))
F=faces(B["elems"])
F.sort(key=lambda f:(min(p[1] for p in f["poly"]),min(p[0] for p in f["poly"])))
panels=[]
for k,f in enumerate(F):
    cx,cy=sum(p[0] for p in f["poly"])/len(f["poly"]),sum(p[1] for p in f["poly"])/len(f["poly"])
    op=next((o for o in openings if not o["small"] and inside((cx,cy),o["poly"])),None)
    tags=[s for s in sfl if inside((s[0],s[1]),f["poly"])]
    typ=Counter(t[3] for t in tags).most_common(1)[0][0] if tags else None
    near=None
    if not tags:                                            # tag drawn just outside a small / sloped panel
        def dpoly(s): return min(math.dist((s[0],s[1]),p) for p in f["poly"])
        s=min(sfl,key=dpoly); near=(round(dpoly(s)),s[2],s[3]); typ=s[3] if dpoly(s)<3000 else None
        tags=[s] if typ else []
    corners=simplify(f["poly"]); rect=len(corners)==4 and all(abs(a[0]-b[0])<1 or abs(a[1]-b[1])<1 for a,b in zip(corners,corners[1:]+corners[:1]))
    panels.append(dict(no=k+1,name=f"{L}-P{k+1:02d}",poly=f["poly"],corners=corners,area=round(f["area"],2),edges=f["edges"],
                       type=typ,levels=sorted({t[2] for t in tags}),mesh="Quadrilateral" if rect else "Quad and Triangle",
                       est=0 if op else round(f["area"]/MESH**2),tag_outside=near,opening=bool(op),method="beams"))
    if op: panels[-1]["type"]="OPENING"
for c in CANT.get(L,[]):
    panels.append(dict(no=len(panels)+1,name=f"{L}-P{len(panels)+1:02d}",poly=[list(p) for p in c["poly"]],corners=c["poly"],area=round(parea(c["poly"]),2),
                       edges=[],type=c["type"],levels=["cantilever"],mesh="Quad and Triangle",est=round(parea(c["poly"])/MESH**2),
                       tag_outside=None,opening=False,method="beams+temporary free edges",free=c["free"]))
json.dump(dict(level=L,z=B["z"],mesh=MESH,panels=panels),open(SC+f"/fs_slab_{L}.json","w"),indent=1)
for p in panels: print(p["name"],p["type"],p["levels"],p["area"],p["mesh"],"~",p["est"],"plates  corners",len(p["corners"]))
print("slab area",round(sum(p["area"] for p in panels if not p["opening"]),2),"  openings",[p["name"] for p in panels if p["opening"]],
      "  no slab tag:",[p["name"] for p in panels if not p["type"]])
print("DXF openings:",[(o["area"],"small-ignored" if o["small"] else "modelled") for o in openings])

# ---- sheet ----
doc=ezdxf.readfile(DXF); msp=doc.modelspace()
cfg=Configuration(text_policy=TextPolicy.IGNORE,color_policy=ColorPolicy.CUSTOM,custom_fg_color="#c9ced4")
fig=plt.figure(figsize=(17,11)); fig.patch.set_facecolor("white")
ax=fig.add_axes([0.03,0.10,0.76,0.82])
Frontend(RenderContext(doc),MatplotlibBackend(ax),config=cfg).draw_layout(msp,finalize=False)
for p in panels:
    c=FC.get(p["type"],"#eeeeee")
    ax.add_patch(Polygon([(O+x,y) for x,y in p["poly"]],closed=True,fc=c,ec="#999" if p["opening"] else "none",alpha=0.55,zorder=3,
                         hatch="xx" if p["opening"] else None))
    if p["opening"]:
        xs=[x for x,y in p["poly"]]; ys=[y for x,y in p["poly"]]
        ax.text(O+sum(xs)/len(xs),sum(ys)/len(ys),f"P{p['no']:02d}\nOPENING\nnot meshed",ha="center",va="center",fontsize=7.5,weight="bold",color="#555",zorder=9,
                bbox=dict(fc="white",ec="#999",lw=0.5,pad=0.25)); continue
    # mesh preview grid (0.5 m) clipped to panel
    xs=[x for x,y in p["poly"]]; ys=[y for x,y in p["poly"]]
    poly=Polygon([(O+x,y) for x,y in p["poly"]],closed=True,transform=ax.transData)
    for gx in range(int(min(xs)//500)*500,int(max(xs))+1,500):
        ln,=ax.plot([O+gx,O+gx],[min(ys),max(ys)],color="#ffffff",lw=0.5,zorder=4); ln.set_clip_path(poly)
    for gy in range(int(min(ys)//500)*500,int(max(ys))+1,500):
        ln,=ax.plot([O+min(xs),O+max(xs)],[gy,gy],color="#ffffff",lw=0.5,zorder=4); ln.set_clip_path(poly)
    cx=sum(xs)/len(xs); cy=sum(ys)/len(ys)
    if p.get("free"):
        for a,b in p["free"]: ax.plot([O+a[0],O+b[0]],[a[1],b[1]],color="#e67e22",lw=2.2,ls=(0,(6,3)),zorder=6)
        cx,cy=12000,-860
    elif not inside((cx,cy),p["poly"]): cx,cy=[(x,y) for x,y in [(sum(xs)/len(xs),y) for y in range(int(min(ys)),int(max(ys)),100)] if inside((x,y),p["poly"])][0]
    lab=f"P{p['no']:02d}\n{p['type'] or '?'}  {p['area']:.1f} m²" + ("\nquad+tri" if p["mesh"]!="Quadrilateral" else "")
    ax.text(O+cx,cy,lab,ha="center",va="center",fontsize=7.5,weight="bold",zorder=9,bbox=dict(fc="white",ec="#555",lw=0.5,pad=0.25,alpha=0.9))
for e in B["elems"]:
    (x1,y1),(x2,y2)=e["a"],e["b"]; ax.plot([O+x1,O+x2],[y1,y2],color="#1f3b73",lw=1.6,zorder=6)
for o in openings:
    if o["small"]:
        P=o["poly"]; ax.add_patch(Polygon([(O+x,y) for x,y in P],closed=True,fc="none",ec="#c0392b",lw=1.2,zorder=8))
        xs=[x for x,y in P]; ys=[y for x,y in P]
        ax.annotate(f"{o['area']:.2f} m² opening\n(not modelled)",(O+sum(xs)/len(xs),max(ys)),xytext=(O+sum(xs)/len(xs),max(ys)+900),
                    fontsize=6.5,color="#c0392b",ha="center",arrowprops=dict(arrowstyle="-",color="#c0392b",lw=0.6),zorder=9)
cn={tuple(map(int,map(float,k.split(",")))) for k in B["colnodes"]}
for p in cn: ax.plot(O+p[0],p[1],"s",ms=7,color="#222",zorder=7)
for s in sfl:
    off=[l for l in [s[2]] if l!=f"+{B['z']:.2f}"]
    ax.plot(O+s[0],s[1]-250,"v",ms=7,color="#c0392b" if off else "#2e7d32",zorder=8)
    if off: ax.text(O+s[0]+200,s[1]-550,f"{s[3]} {s[2]}",fontsize=7,color="#c0392b",weight="bold",zorder=9)
for k,x in CM["GX"].items():
    X=O+x*1000; ax.plot([X,X],[-2200,16600],color="#7f8c99",lw=0.5,ls=(0,(10,4,2,4)),zorder=2)
    ax.add_patch(plt.Circle((X,17600),480,fc="white",ec="#222",lw=1,zorder=8)); ax.text(X,17600,k,ha="center",va="center",fontsize=10,weight="bold",zorder=9)
for k,y in CM["GY"].items():
    Y=y*1000; ax.plot([O-2200,O+30500],[Y,Y],color="#7f8c99",lw=0.5,ls=(0,(10,4,2,4)),zorder=2)
    ax.add_patch(plt.Circle((O-3100,Y),480,fc="white",ec="#222",lw=1,zorder=8)); ax.text(O-3100,Y,k,ha="center",va="center",fontsize=10,weight="bold",zorder=9)
ax.set_xlim(O-4000,O+31800); ax.set_ylim(-2600,18400); ax.set_aspect("equal"); ax.axis("off")
fig.text(0.03,0.955,f"{NAME[L]}   Z = +{B['z']:.2f} m",fontsize=17,weight="bold")
fig.text(0.03,0.93,"Slab panels = closed bays of the analytical beams (dark blue). White grid = 0.50 m target mesh. Panels are meshed one by one with MIDAS Auto-mesh; boundary beams are split at the mesh nodes.",fontsize=9.5,color="#444")
sx=fig.add_axes([0.80,0.10,0.19,0.82]); sx.axis("off"); sx.set_xlim(0,1); sx.set_ylim(0,1)
yy=0.98; sx.text(0,yy,"SLAB PANELS",fontsize=11,weight="bold",va="top"); yy-=0.05
cnt=Counter(p["type"] for p in panels)
for t,n in cnt.items():
    if t=="OPENING": continue
    tid,th=THK.get(t,(None,None))
    sx.add_patch(plt.Rectangle((0,yy-0.012),0.08,0.024,fc=FC.get(t,"#eee"),ec="#555",lw=0.5))
    sx.text(0.11,yy,f"{t}  t = {th} mm  (thickness {tid})  × {n}",fontsize=9.5,va="center"); yy-=0.045
yy-=0.01
sx.text(0,yy,f"Panels: {sum(not p['opening'] for p in panels)} slab + {sum(p['opening'] for p in panels)} opening    slab {sum(p['area'] for p in panels if not p['opening']):.1f} m²",fontsize=10,weight="bold"); yy-=0.035
sx.text(0,yy,f"Mesh 0.50 m → about {sum(p['est'] for p in panels):,} plates",fontsize=9); yy-=0.03
sx.text(0,yy,f"Quadrilateral: {sum(p['mesh']=='Quadrilateral' and not p['opening'] for p in panels)}   Quad+triangle: {sum(p['mesh']!='Quadrilateral' and not p['opening'] for p in panels)} (non-rectangular)",fontsize=9); yy-=0.03
sx.text(0,yy,"Thick plate, C280, no offset (mid-plane at level)",fontsize=9); yy-=0.055
sx.text(0,yy,"LEGEND",fontsize=10,weight="bold"); yy-=0.04
sx.plot([0.04],[yy],"v",ms=7,color="#2e7d32"); sx.text(0.1,yy,f"slab tag at +{B['z']:.2f}",fontsize=9,va="center"); yy-=0.035
sx.plot([0.04],[yy],"v",ms=7,color="#c0392b"); sx.text(0.1,yy,"slab tag at another level (step)",fontsize=9,va="center"); yy-=0.035
if CANT.get(L):
    sx.plot([0,0.08],[yy,yy],color="#e67e22",lw=2.2,ls=(0,(6,3))); sx.text(0.1,yy,"free slab edge, no beam",fontsize=9,va="center"); yy-=0.035
yy-=0.02
notes={"RF":["Openings (crossed in DXF): bays 1–2 × D–B and B–A, not meshed (as on 2F and 3F).",
             "Bay 4–5 north of D is roof slab (tagged RS1).",
             "S1C overhang with no edge beam (P15): south 1.725 m and east 1.925 m past the beam centrelines, north edge at Y=9.325 (1.325 m past D5), ending on sloped beam C4–D5 at X=16.38. Meshed with temporary free-edge lines, deleted afterwards.",
             "East overhang clear span 1.80 m (south 1.60 m) exceeds the 1.50 m max in the S1C detail - modelled as drawn.",
             "All roof tags at +11.15: no steps."],
       "3F":["Openings (crossed in DXF): bays 1–2 × D–B and B–A (stair/shaft), not meshed. Two small openings (0.15, 0.20 m²) next to row E not modelled.",
             "East strip beyond grid 5 (X 19.25–22.275, F to Y=5.90) is closed by beams (B1C cantilevers + edge beam B2), so it is meshed like any bay; no free-edge cantilever on this floor.",
             "Bay 4–5 north of D is slab on 3F (tagged S1 +7.95) - unlike 2F where it is a void.",
             "Steps +7.80 (bays 1–2 south, east strip) and +7.85 (bay 1–2, 5.9–D) ignored: all at +7.95."],
       "2F":["Openings (crossed in DXF): bays 1–2 × D–B and B–A (stair/shaft) and the triangle 4–5 north of D (void under the sloped edge): not meshed.",
             "Three small openings (0.15–0.43 m²) next to row E are not modelled at a 0.5 m mesh.",
             "S1C cantilever 1.725 m from beam centreline (1.60 m clear) along row F, east of grid 6 and north of D5–D6, ending on sloped beam C4–D5 at X=15.51. Free edges have no beam: meshed with temporary edge lines, deleted afterwards.",
             "Steps +4.65 (strip 5.9–D) and +4.60 (bays 1–2 and 5–6 south, S1C) ignored: all at +4.75."],
       "GB":["Whole footprint is GS1 (200 mm) on ground beams; no openings. The slab edge in the DXF follows the outer faces of the edge beams, so no slab projects past a beam.",
             "Annex bays 6–7 (P06, P12) are tagged +0.45 (100 mm step up): ignored, modelled at +0.35 like the other steps.",
             "P17 and P19 have their GS1 tag drawn just outside the sloped edge beam (nearest tag used). P12 is bounded by the 6 curved-beam chords; P15–P17, P19 are cut by the sloped edge beam."]}
sx.text(0,yy,"NOTES / ASSUMPTIONS",fontsize=10,weight="bold"); yy-=0.035
for n in notes.get(L,[]):
    w=textwrap.fill("• "+n,40); sx.text(0,yy,w,fontsize=8.5,va="top"); yy-=0.029*(w.count("\n")+1)+0.012
fig.savefig(SC+f"/fs_slab_{L}.png",dpi=110,facecolor="white"); print("saved",f"fs_slab_{L}.png")
