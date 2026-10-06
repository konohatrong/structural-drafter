# -*- coding: utf-8 -*-
import sys, json, math
sys.stdout.reconfigure(encoding="utf-8")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
B=json.load(open(SC+"/fs_beammodel.json")); CM=json.load(open(SC+"/fs_colmodel.json"))
COL={"GB1":"#1f5fbf","GB1A":"#17a2b8","GB1C":"#e76f51","B1":"#1f5fbf","B1A":"#17a2b8","B1C":"#e76f51",
     "B2":"#8e44ad","B2A":"#c0392b","BX":"#d4a017","?":"#000"}
fig,axs=plt.subplots(2,2,figsize=(18,11.5)); fig.patch.set_facecolor("white")
for ax,(L,d) in zip(axs.flat,B.items()):
    for k,x in CM["GX"].items():
        ax.plot([x,x],[-1.2,15.6],color="#d5d9de",lw=0.6,ls="--"); ax.text(x,16.1,k,ha="center",fontsize=8,weight="bold")
    for k,y in CM["GY"].items():
        ax.plot([-1.2,28.6],[y,y],color="#d5d9de",lw=0.6,ls="--"); ax.text(-1.9,y,k,va="center",fontsize=8,weight="bold")
    cn={tuple(map(float,k.split(","))) for k in d["colnodes"]}
    for (x,y) in cn: ax.plot(x/1000,y/1000,"s",ms=6,color="#444",zorder=5)
    newp=set()
    for e in d["elems"]:
        (x1,y1),(x2,y2)=e["a"],e["b"]; c=COL.get(e["mark"],"#000")
        ax.plot([x1/1000,x2/1000],[y1/1000,y2/1000],color=c,lw=2.3,solid_capstyle="butt")
        mx,my=(x1+x2)/2000,(y1+y2)/2000; ang=math.degrees(math.atan2(y2-y1,x2-x1))
        if ang>90: ang-=180
        if ang<-90: ang+=180
        ax.text(mx,my,e["mark"],fontsize=5.8,color=c,rotation=ang,ha="center",va="bottom",
                fontweight="bold" if e["src"]!="text" else "normal",
                bbox=dict(fc="#fff3b0",ec="none",pad=0.5) if e["src"]!="text" else None)
        for p in (e["a"],e["b"]):
            if tuple(map(float,p)) not in cn: newp.add(tuple(p))
    for (x,y) in newp: ax.plot(x/1000,y/1000,"o",ms=3.5,mfc="white",mec="#c0392b",zorder=6)
    ax.set_title(f"{L}  (Z = +{d['z']:.2f})  —  {len(d['elems'])} beams, {len(newp)} new nodes",fontsize=11,loc="left")
    ax.set_xlim(-2.5,29.5); ax.set_ylim(-1.8,16.8); ax.set_aspect("equal"); ax.axis("off")
h=[plt.Line2D([],[],color=v,lw=3,label=k) for k,v in COL.items() if k!="?"]
h+= [plt.Line2D([],[],marker="s",ls="",color="#444",label="column node"),
     plt.Line2D([],[],marker="o",ls="",mfc="white",mec="#c0392b",label="new beam node")]
fig.legend(handles=h,loc="lower center",ncol=12,frameon=False,fontsize=9)
fig.text(0.5,0.035,"Yellow-highlighted marks were inferred (from the drawn segment or its collinear neighbour), not read from a label on that span.",
         ha="center",fontsize=9,color="#555")
fig.savefig(SC+"/fs_beams_model.png",dpi=95,facecolor="white"); print("saved")
