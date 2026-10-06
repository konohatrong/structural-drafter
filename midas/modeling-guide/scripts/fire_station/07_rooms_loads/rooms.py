# -*- coding: utf-8 -*-
# Room-function zones from the architectural plans (B - Floor Plan.pdf, A1-01..A1-04) mapped onto the slab plates in MIDAS.
# usage: python rooms.py <MAPI_KEY>   -> fs_rooms.json (zone per plate + areas) + fs_rooms_<L>.png
import sys, os, json, math
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
R=lambda x0,x1,y0,y1:[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
BIG=99999
# zones are tested in order; first match wins. "panels" = slab panel groups; "rects" = plan rectangles (mm, beam-centreline grid)
ZONES={
 "GB":[dict(id="GB-STAIR",en="Stair (first flight, +0.50)",th="บันได",rects=[R(0,2250,12000,BIG)]),
       dict(id="GB-STORE",en="Storage room",th="ห้องเก็บของ",rects=[R(0,2250,10800,12000)]),
       dict(id="GB-PUMP",en="Water pump room",th="ห้องปั๊มน้ำ",rects=[R(0,2250,8000,10800)]),
       dict(id="GB-WC",en="Toilet",th="ห้องน้ำ 1",rects=[R(0,2250,4000,8000)]),
       dict(id="GB-CCTV",en="CCTV room",th="ห้อง CCTV",rects=[R(0,2250,0,4000)]),
       dict(id="GB-DUTY",en="Duty officer room (annex)",th="เจ้าหน้าที่เวร",rects=[R(23550,BIG,0,4000)]),
       dict(id="GB-RADIO",en="Community radio room (annex)",th="ห้องวิทยุชุมชน",rects=[R(23550,BIG,4000,BIG)]),
       dict(id="GB-TRUCK",en="Fire-truck parking",th="จอดรถดับเพลิง",rects=[R(2250,23550,-BIG,BIG)])],
 "2F":[dict(id="2F-CANOPY",en="Canopy (S1C, no access)",th="กันสาด",panels=["2F-P26"]),
       dict(id="2F-WCM",en="Men's toilet",th="ห้องน้ำชายชั้น 2",rects=[R(0,3175,0,5900)]),
       dict(id="2F-DUTYOFF",en="Duty staff office",th="ห้องทำงานเจ้าหน้าที่เวร",rects=[R(3175,8750,0,5900)]),
       dict(id="2F-CMD",en="Command room",th="ห้อง COMMAND ROOM",rects=[R(8750,19250,0,5900)]),
       dict(id="2F-WCF",en="Women's toilet",th="ห้องน้ำหญิงชั้น 2",rects=[R(19250,22426,0,5900)]),
       dict(id="2F-LEDGE",en="Exterior ledge east of women's toilet (confirm)",th="ส่วนยื่นภายนอก (ยืนยัน)",rects=[R(22426,23550,0,5900)]),
       dict(id="2F-STAIRHALL",en="Stair hall",th="โถงบันได",rects=[R(0,3875,5900,8000),R(2250,3875,8000,BIG)]),
       dict(id="2F-ENFORCE",en="Municipal enforcement office",th="ห้องเทศกิจ",rects=[R(3875,11280,8000,BIG)]),
       dict(id="2F-CORR",en="Corridor / veranda",th="ระเบียง",rects=[R(3875,23550,5900,8000),R(11280,12750,8000,BIG)])],
 "3F":[dict(id="3F-WCM",en="Men's toilet",th="ห้องน้ำชายชั้น 3",rects=[R(0,3175,0,5900)]),
       dict(id="3F-STAIRHALL",en="Stair hall",th="โถงบันได",rects=[R(0,3875,5900,8000),R(2250,3875,8000,BIG)]),
       dict(id="3F-ROOF2F",en="Roof slab over 2F toilet (no access)",th="SLAB (R1)",rects=[R(19250,BIG,-BIG,BIG)]),
       dict(id="3F-REST",en="Staff rest / sleeping rooms",th="ห้องพักเจ้าหน้าที่",rects=[R(3175,19250,-BIG,BIG)])],
 "RF":[dict(id="RF-OVERHANG",en="Roof overhang (S1C)",th="SLAB (กันสาด)",panels=["RF-P15"]),
       dict(id="RF-STAIRHALL",en="Stair hall at roof (under stair roof +14.15)",th="โถงบันได",rects=[R(0,2250,5200,8000)]),
       dict(id="RF-TANK",en="Water-tank area (2 x 1.5 m³ tanks)",th="พื้นที่ถังเก็บน้ำ",rects=[R(3100,7600,0,2600)]),
       dict(id="RF-DECK",en="Accessible roof deck (parapet 1.0 m)",th="พื้นหลังคาดาดฟ้า",rects=[R(-BIG,BIG,-BIG,BIG)])],
 "AR":[dict(id="AR-ROOF",en="Annex roof (no access)",th="SLAB (R1)",rects=[R(-BIG,BIG,-BIG,BIG)])]}
EXTRA={"RF":[dict(what="2 water tanks, 1.5 m³ each (approx. centres)",th="ถังเก็บน้ำ 1.5 ลบ.ม. 2 ถัง",pts=[(4370,1360),(6300,1360)])]}
Z={"GB":0.35,"2F":4.75,"3F":7.95,"RF":11.15,"AR":3.95}
GID={"GB":(13,100),"2F":(14,200),"3F":(15,300),"RF":(16,400),"AR":(17,500)}

def inside(pt,P):
    x,y=pt; c=False
    for i in range(len(P)):
        (x1,y1),(x2,y2)=P[i-1],P[i]
        if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1: c=not c
    return c

os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
N=mg.MidasAPI("GET","/db/NODE",{})["NODE"]; E=mg.MidasAPI("GET","/db/ELEM",{})["ELEM"]; G=mg.MidasAPI("GET","/db/GRUP",{})["GRUP"]
name2panel={}
for k,g in G.items():
    if g["NAME"].startswith("SLAB_") and "-P" in g["NAME"]:
        for e in g["E_LIST"]: name2panel[e]=g["NAME"][5:]
out={"zones":{},"plates":{},"extra":EXTRA}
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
PAL=["#4e79a7","#f28e2b","#59a14f","#e15759","#76b7b2","#edc948","#b07aa1","#ff9da7","#9c755f","#bab0ac"]
for L,zs in ZONES.items():
    lvl=G[str(GID[L][0])]["E_LIST"]; area=defaultdict(float); cnt=defaultdict(int); pan=defaultdict(set); polys=[]
    for e in lvl:
        el=E[str(e)]; P=[(N[str(n)]["X"]*1000,N[str(n)]["Y"]*1000) for n in el["NODE"] if n]
        c=(sum(p[0] for p in P)/len(P),sum(p[1] for p in P)/len(P))
        a=abs(sum(P[i-1][0]*P[i][1]-P[i][0]*P[i-1][1] for i in range(len(P))))/2e6
        z=next((z["id"] for z in zs if (name2panel.get(e) in z.get("panels",[])) or any(inside(c,r) for r in z.get("rects",[]))),"UNASSIGNED")
        area[z]+=a; cnt[z]+=1; pan[z].add(name2panel.get(e,"?")); out["plates"][e]=z; polys.append((P,z))
    for z in zs: out["zones"][z["id"]]=dict(level=L,z=Z[L],en=z["en"],th=z["th"],plates=cnt[z["id"]],area=round(area[z["id"]],2),
                                             panels=sorted(pan[z["id"]]))
    if cnt["UNASSIGNED"]: print(L,"UNASSIGNED plates:",cnt["UNASSIGNED"])
    # map
    col={z["id"]:PAL[i%len(PAL)] for i,z in enumerate(zs)}
    fig,ax=plt.subplots(figsize=(14,8.2)); fig.patch.set_facecolor("white")
    for P,z in polys: ax.add_patch(Polygon(P,closed=True,fc=col.get(z,"#000"),ec="white",lw=0.15,alpha=0.85))
    xs=[p[0] for P,_ in polys for p in P]; ys=[p[1] for P,_ in polys for p in P]
    for z in zs:
        pts=[(sum(p[0] for p in P)/len(P),sum(p[1] for p in P)/len(P)) for P,zz in polys if zz==z["id"]]
        if not pts: continue
        cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
        best=min(pts,key=lambda p:math.dist(p,(cx,cy)))
        ax.text(best[0],best[1],f"{z['id']}\n{area[z['id']]:.1f} m²",ha="center",va="center",fontsize=8,weight="bold",
                bbox=dict(fc="white",ec=col[z["id"]],lw=1,pad=0.25,alpha=0.92))
    for x in [0,2250,8750,12750,19250,23550,27250]: ax.axvline(x,color="#999",lw=0.5,ls=(0,(8,4)),zorder=0)
    for y,n in [(0,"F"),(4000,"E"),(8000,"D"),(11000,"C"),(12000,"B"),(14300,"A")]:
        ax.axhline(y,color="#999",lw=0.5,ls=(0,(8,4)),zorder=0); ax.text(min(xs)-900,y,n,va="center",fontsize=10,weight="bold")
    for t in EXTRA.get(L,[]):
        for p in t["pts"]: ax.add_patch(plt.Circle(p,850,fc="none",ec="#c0392b",lw=1.6)); ax.text(p[0],p[1],"TANK",ha="center",va="center",fontsize=6.5,color="#c0392b",weight="bold")
    handles=[plt.Rectangle((0,0),1,1,fc=col[z["id"]]) for z in zs if cnt[z["id"]]]
    ax.legend(handles,[f"{z['id']}  {z['en']}" for z in zs if cnt[z["id"]]],loc="upper left",bbox_to_anchor=(1.01,1),fontsize=8.5,frameon=False)
    ax.set_xlim(min(xs)-1500,max(xs)+800); ax.set_ylim(min(ys)-800,max(ys)+800); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"{L}  slab at +{Z[L]:.2f}  -  room functions from architectural plan (plates coloured by zone)",loc="left",fontsize=12,weight="bold")
    fig.tight_layout(); fig.savefig(SC+f"/fs_rooms_{L}.png",dpi=105,facecolor="white"); plt.close(fig)
json.dump(out,open(SC+"/fs_rooms.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
print(f"{'zone':14} {'plates':>6} {'area m²':>8}  function")
for k,z in out["zones"].items(): print(f"{k:14} {z['plates']:6d} {z['area']:8.2f}  {z['en']} | {z['th']}  panels {','.join(p.split('-')[1] for p in z['panels'])}")
print("total plates classified:",len(out["plates"]))
