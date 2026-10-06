# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding="utf-8")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
B=json.load(open(SC+"/fs_beams_raw.json")); M=json.load(open(SC+"/fs_colmodel.json"))
GX=M["GX"]; GY=M["GY"]
COL={"GB1":"#1f5fbf","GB1A":"#2a9d8f","GB1C":"#e76f51","B1":"#1f5fbf","B1A":"#2a9d8f","B1C":"#e76f51",
     "B2":"#8e44ad","B2A":"#c0392b","BX":"#d4a017","?":"#000000"}
lv=["GB","2F","3F","RF"]; tops={"GB":"2F","2F":"2F","3F":"RF","RF":"RF"}
fig,axs=plt.subplots(2,2,figsize=(18,11)); fig.patch.set_facecolor("white")
for ax,L in zip(axs.flat,lv):
    for k,x in GX.items():
        ax.plot([x*1000,x*1000],[-1500,16500],color="#c9cdd2",lw=0.6,ls="--"); ax.text(x*1000,17000,k,ha="center",fontsize=8)
    for k,y in GY.items():
        ax.plot([-1500,31000],[y*1000,y*1000],color="#c9cdd2",lw=0.6,ls="--"); ax.text(-2200,y*1000,k,va="center",fontsize=8)
    for c in M["cols"]:
        lvl_ok = not (c["top"]=="2F" and L in("3F","RF"))
        if lvl_ok: ax.plot(c["x"]*1000,c["y"]*1000,"s",ms=5,color="#555")
    for s in B["segs"][L]:
        col=COL.get(s["mark"],"#000")
        ax.plot([s["x1"],s["x2"]],[s["y1"],s["y2"]],color=col,lw=2.2 if s["mark"]!="?" else 1.4,ls="-" if s["mark"]!="?" else ":")
        if s["mark"]=="?": ax.text((s["x1"]+s["x2"])/2,(s["y1"]+s["y2"])/2,"?",fontsize=9,color="k",weight="bold")
    for m in B["marks"].get(L,[]):
        ax.text(m[0],m[1],m[2],fontsize=5.5,color="#444",rotation=m[3])
    ax.set_title(f"{L} — {len(B['segs'][L])} beam segments (raw from DXF)",fontsize=11,loc="left")
    ax.set_xlim(-3000,32000); ax.set_ylim(-2000,18000); ax.set_aspect("equal"); ax.axis("off")
h=[plt.Line2D([],[],color=v,lw=3,label=k) for k,v in COL.items()]
fig.legend(handles=h,loc="lower center",ncol=10,frameon=False,fontsize=9)
fig.savefig(SC+"/fs_beams_raw.png",dpi=95,facecolor="white"); print("saved")
