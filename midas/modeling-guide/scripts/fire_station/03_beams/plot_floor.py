# -*- coding: utf-8 -*-
import sys, json, math
sys.stdout.reconfigure(encoding="utf-8")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, TextPolicy, ColorPolicy
import logging; logging.disable(logging.WARNING)

SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
DXF=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
B=json.load(open(SC+"/fs_beammodel.json")); CM=json.load(open(SC+"/fs_colmodel.json"))
PAN={"GB":45778,"2F":91555,"3F":137333,"RF":183111}
LD={"GB":2,"2F":3,"3F":4,"RF":5}                     # level digit (matches column node IDs)
NAME={"GB":"GROUND BEAM LEVEL","2F":"2ND FLOOR","3F":"3RD FLOOR","RF":"ROOF"}
SIZE={"GB1":"250×800","GB1A":"250×800","GB1C":"250×800 cant.","B1":"250×600","B1A":"250×600",
      "B1C":"250×600 cant.","B2":"250×600","B2A":"250×600 (assumed)"}
SEC={"GB1":201,"GB1A":202,"GB1C":203,"B1":204,"B1A":205,"B1C":206,"B2":207,"B2A":209}
COL={"GB1":"#1f5fbf","GB1A":"#0f9aa8","GB1C":"#e4572e","B1":"#1f5fbf","B1A":"#0f9aa8","B1C":"#e4572e",
     "B2":"#8e44ad","B2A":"#c0392b"}
GX=CM["GX"]; GY=CM["GY"]

doc=ezdxf.readfile(DXF); msp=doc.modelspace()
cfg=Configuration(text_policy=TextPolicy.IGNORE,color_policy=ColorPolicy.CUSTOM,custom_fg_color="#c9ced4")

ONLY=sys.argv[1:]
ids={}
for L,d in B.items():
    O=PAN[L]; ld=LD[L]
    if ONLY and L not in ONLY: pass
    cn={tuple(map(int,map(float,k.split(",")))):int(v) for k,v in d["colnodes"].items()}
    gridname={}
    for c in CM["cols"]: gridname[(round(c["x"]*1000),round(c["y"]*1000))]=c["grid"]
    # --- assign IDs (stable: sort by y then x) ---
    new=sorted({tuple(p) for e in d["elems"] for p in (e["a"],e["b"])}-set(cn),key=lambda p:(p[1],p[0]))
    nid={p:ld*1000+101+i for i,p in enumerate(new)}; nid.update(cn)
    els=sorted(d["elems"],key=lambda e:((e["a"][1]+e["b"][1])/2,(e["a"][0]+e["b"][0])/2))
    for i,e in enumerate(els):
        e["id"]=ld*10000+1001+i; e["i"]=nid[tuple(e["a"])]; e["j"]=nid[tuple(e["b"])]; e["sect"]=SEC[e["mark"]]
        e["len"]=round(math.dist(e["a"],e["b"])/1000,3)
    d["elems"]=els; d["newnodes"]={str(nid[p]):[p[0]/1000,p[1]/1000] for p in new}
    if ONLY and L not in ONLY: continue
    # --- figure ---
    fig=plt.figure(figsize=(17,11)); fig.patch.set_facecolor("white")
    ax=fig.add_axes([0.03,0.10,0.76,0.82])
    Frontend(RenderContext(doc),MatplotlibBackend(ax),config=cfg).draw_layout(msp,finalize=False)
    for k,x in GX.items():
        X=O+x*1000; ax.plot([X,X],[-2200,16600],color="#7f8c99",lw=0.5,ls=(0,(10,4,2,4)),zorder=2)
        ax.add_patch(plt.Circle((X,17600),480,fc="white",ec="#222",lw=1,zorder=8)); ax.text(X,17600,k,ha="center",va="center",fontsize=10,weight="bold",zorder=9)
    for k,y in GY.items():
        Y=y*1000; ax.plot([O-2200,O+30500],[Y,Y],color="#7f8c99",lw=0.5,ls=(0,(10,4,2,4)),zorder=2)
        ax.add_patch(plt.Circle((O-3100,Y),480,fc="white",ec="#222",lw=1,zorder=8)); ax.text(O-3100,Y,k,ha="center",va="center",fontsize=10,weight="bold",zorder=9)
    xs=sorted(GX.values()); ys=sorted(GY.values())
    for a,b in zip(xs,xs[1:]): ax.text(O+(a+b)*500,16450,f"{(b-a)*1000:,.0f}",ha="center",fontsize=8,color="#555",zorder=9)
    for a,b in zip(ys,ys[1:]): ax.text(O+30900,(a+b)*500,f"{(b-a)*1000:,.0f}",va="center",fontsize=8,color="#555",zorder=9)
    for e in els:
        (x1,y1),(x2,y2)=e["a"],e["b"]; c=COL[e["mark"]]
        ax.plot([O+x1,O+x2],[y1,y2],color=c,lw=3.2,solid_capstyle="butt",zorder=5)
        mx,my=O+(x1+x2)/2,(y1+y2)/2; ang=math.degrees(math.atan2(y2-y1,x2-x1))
        if ang>90: ang-=180
        if ang<=-90: ang+=180
        nx,ny=-math.sin(math.radians(ang)),math.cos(math.radians(ang))
        ax.text(mx+nx*230,my+ny*230,f"{e['mark']}  {e['len']:.2f}",fontsize=6.6,color=c,rotation=ang,
                ha="center",va="center",zorder=7,
                bbox=dict(fc=("#d4f5d4" if e["src"]=="user" else "#fff3b0") if e["src"]!="text" else "white",ec="none",pad=0.4,alpha=0.9))
    for p,i in cn.items():
        ax.plot(O+p[0],p[1],"s",ms=8,color="#222",zorder=6)
    for p in new:
        ax.plot(O+p[0],p[1],"o",ms=6,mfc="white",mec="#c0392b",mew=1.6,zorder=7)
        ax.text(O+p[0]+180,p[1]-420,f"{nid[p]}\n({p[0]/1000:.3f}, {p[1]/1000:.3f})",fontsize=6,color="#c0392b",zorder=9,
                bbox=dict(fc="white",ec="none",pad=0.2,alpha=0.85))
    ax.set_xlim(O-4000,O+31800); ax.set_ylim(-2600,18400); ax.set_aspect("equal"); ax.axis("off")
    # --- side panel ---
    fig.text(0.03,0.955,f"{NAME[L]}   Z = +{d['z']:.2f} m",fontsize=17,weight="bold")
    fig.text(0.03,0.93,"Analytical beam layout on the traced DXF plan (grey). All beams end on column nodes or beam-only nodes; "
             "column centrelines on grid intersections; BX neglected.",fontsize=9.5,color="#444")
    sx=fig.add_axes([0.80,0.10,0.19,0.82]); sx.axis("off"); sx.set_xlim(0,1); sx.set_ylim(0,1)
    from collections import Counter
    cnt=Counter(e["mark"] for e in els)
    sx.text(0,0.98,"BEAMS ON THIS LEVEL",fontsize=11,weight="bold",va="top")
    yy=0.93
    for m in [k for k in SEC if k in cnt]:
        sx.plot([0,0.1],[yy,yy],color=COL[m],lw=4); sx.text(0.13,yy,f"{m}",fontsize=10,va="center",weight="bold",color=COL[m])
        sx.text(0.36,yy,f"{SIZE[m]}   sect {SEC[m]}   × {cnt[m]}",fontsize=9,va="center"); yy-=0.045
    yy-=0.02
    sx.text(0,yy,f"Total beams: {len(els)}",fontsize=10,weight="bold"); yy-=0.04
    sx.text(0,yy,f"Beam elements: {els[0]['id']} – {els[-1]['id']}",fontsize=9); yy-=0.035
    sx.text(0,yy,f"Beam-only nodes: {len(new)}"+(f"  ({min(nid[p] for p in new)} – {max(nid[p] for p in new)})" if new else ""),fontsize=9); yy-=0.035
    sx.text(0,yy,f"Column nodes used: {sum(1 for p in cn if any(tuple(e['a'])==p or tuple(e['b'])==p for e in els))}"
            f"  (IDs {ld}001–{ld}026)",fontsize=9); yy-=0.06
    sx.text(0,yy,"LEGEND",fontsize=10,weight="bold"); yy-=0.04
    sx.plot([0.03],[yy],"s",ms=8,color="#222"); sx.text(0.1,yy,"column node (on grid)",fontsize=9,va="center"); yy-=0.035
    sx.plot([0.03],[yy],"o",ms=6,mfc="white",mec="#c0392b",mew=1.6); sx.text(0.1,yy,"beam-only node  (ID, X, Y in m)",fontsize=9,va="center"); yy-=0.035
    sx.text(0.0,yy,"B1  6.50",fontsize=8,color="#1f5fbf",va="center",bbox=dict(fc="white",ec="#ccc",pad=0.4)); sx.text(0.3,yy,"mark + span (m)",fontsize=9,va="center"); yy-=0.035
    sx.text(0.0,yy,"B1  1.90",fontsize=8,color="#1f5fbf",va="center",bbox=dict(fc="#fff3b0",ec="none",pad=0.4)); sx.text(0.3,yy,"mark inferred (no label on span)",fontsize=9,va="center"); yy-=0.035
    sx.plot([0,0.1],[yy,yy],color="#c9ced4",lw=2); sx.text(0.13,yy,"original DXF drawing",fontsize=9,va="center"); yy-=0.06
    notes={"GB":["Curved corner beam 6–7 / D–E: quarter circle, centre (23.550, 4.300), R 3.700 m, as 0.30 m straight leg from E7 + 6 straight chords (0.97 m, max 32 mm off the arc).","Sloped edge = one straight GB1 A2→D6, carried by GB1C cantilevers from B3 (0.38 m), C4 (0.19 m), D5 (1.27 m).",
                 "Beam level taken at ground-floor SFL +0.35."],
           "2F":["East annex (grids 6–7, roof RS1 +3.95) excluded for now — to be modelled later as its own level. 2F ends at the grid-6 edge beams.","Columns E7, F7 currently end at +4.75 with no beams — to be resolved with the annex.",
                 "Stair BX trimmers removed. Y=5.90 line completed to grid 1 with B1 (per review).",
                 "Local slab drops (+4.60/+4.65) ignored; level +4.75."],
           "3F":["Secondary line unified to Y=5.90 (east part drawn at 5.75).","B1C cantilever strip east of grid 5 to X=22.275, closed by edge beam B2 F→E→(Y=5.90).",
                 "Stair BX trimmers removed. Y=5.90 line completed to grid 1 with B1 (as 2F).","Local steps (+7.80/+7.85) ignored; level +7.95."],
           "RF":["Sloped edge A2→B3→C4→D5 = B2 / B2A / B2.","B2A not in beam schedule — assumed 250×600 (= B2)."]}
    sx.text(0,yy,"NOTES / ASSUMPTIONS",fontsize=10,weight="bold"); yy-=0.035
    import textwrap
    for n in notes[L]:
        w=textwrap.fill("• "+n,38); sx.text(0,yy,w,fontsize=8.5,va="top"); yy-=0.03*(w.count("\n")+1)+0.012
    out=f"{SC}/fs_beams_{L}.png"; fig.savefig(out,dpi=110,facecolor="white"); plt.close(fig); print("saved",out)
json.dump(B,open(SC+"/fs_beammodel.json","w"),indent=1); print("IDs stored in fs_beammodel.json")
