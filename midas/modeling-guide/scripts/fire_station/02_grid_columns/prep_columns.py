# -*- coding: utf-8 -*-
# Prepare analytical column model for the fire-station building (no MIDAS write).
import sys, json
sys.stdout.reconfigure(encoding="utf-8")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)

GX={"1":0.000,"2":2.250,"3":8.750,"4":12.750,"5":19.250,"6":23.550,"7":27.250}
GY={"F":0.000,"E":4.000,"D":8.000,"C":11.000,"B":12.000,"A":14.300}
LEV=[("BASE",-1.00),("GF",0.35),("2F",4.75),("3F",7.95),("RF",11.15)]
C1=["A1","A2","B1","D1","E1","F1","D6","E6","F6","E7","F7"]
C2=["B2","B3","C4","D2","D3","D4","D5","E2","E3","E4","E5","F2","F3","F4","F5"]
EAST={"D6","E6","F6","E7","F7"}                     # stop under 2F
SEC={"C1":{"stub":102,"col":101},"C2":{"stub":104,"col":103}}

cols=[]
order=sorted(C1+C2,key=lambda g:("FEDCBA".index(g[0]),int(g[1:])))
for i,g in enumerate(order,1):
    mark="C1" if g in C1 else "C2"
    top=2 if g in EAST else 4                        # index into LEV
    cols.append({"idx":i,"grid":g,"mark":mark,"x":GX[g[1:]],"y":GY[g[0]],"top":LEV[top][0]})

nodes={}; elems={}
for c in cols:
    top=[l[0] for l in LEV].index(c["top"])
    for li in range(top+1):
        nid=1000*(li+1)+c["idx"]
        nodes[nid]={"X":c["x"],"Y":c["y"],"Z":LEV[li][1],"grid":c["grid"],"lev":LEV[li][0]}
    for li in range(top):
        eid=1000*(li+1)+c["idx"]
        sect=SEC[c["mark"]]["stub" if li==0 else "col"]
        elems[eid]={"i":1000*(li+1)+c["idx"],"j":1000*(li+2)+c["idx"],"sect":sect,
                    "grid":c["grid"],"mark":c["mark"],"seg":f"{LEV[li][0]}->{LEV[li+1][0]}"}

print(f"columns {len(cols)}  nodes {len(nodes)}  elements {len(elems)}")
print(f"{'grid':5}{'mark':5}{'X':>8}{'Y':>8}  top   segments(sect)")
for c in cols:
    segs=[f"{elems[e]['seg']}({elems[e]['sect']})" for e in sorted(elems) if elems[e]['grid']==c['grid']]
    print(f"{c['grid']:5}{c['mark']:5}{c['x']:8.3f}{c['y']:8.3f}  {c['top']:4}  {', '.join(segs)}")
json.dump({"GX":GX,"GY":GY,"LEV":LEV,"cols":cols,"nodes":nodes,"elems":elems},
          open(SC+"/fs_colmodel.json","w"),indent=1)

# ---- plan figure ----
fig,ax=plt.subplots(figsize=(12,7.2)); fig.patch.set_facecolor("white")
for k,x in GX.items():
    ax.plot([x,x],[-1.2,15.5],color="#9aa3ad",lw=0.7,ls=(0,(8,3,2,3)))
    ax.add_patch(plt.Circle((x,16.3),0.42,fc="white",ec="#333",lw=1)); ax.text(x,16.3,k,ha="center",va="center",fontsize=9,weight="bold")
for k,y in GY.items():
    ax.plot([-1.2,28.5],[y,y],color="#9aa3ad",lw=0.7,ls=(0,(8,3,2,3)))
    ax.add_patch(plt.Circle((-2.0,y),0.42,fc="white",ec="#333",lw=1)); ax.text(-2.0,y,k,ha="center",va="center",fontsize=9,weight="bold")
for c in cols:
    w,h=(0.25,0.25) if c["mark"]=="C1" else (0.25,0.40)
    col="#c0392b" if c["mark"]=="C2" else "#1f5fbf"
    fc=col if c["grid"] not in EAST else "white"
    ax.add_patch(plt.Rectangle((c["x"]-w/2*2,c["y"]-h/2*2),w*2,h*2,fc=fc,ec=col,lw=1.4,zorder=5))
    ax.text(c["x"]+0.45,c["y"]+0.35,c["mark"],fontsize=7.5,color=col,zorder=6)
xs=list(GX.values()); ys=list(GY.values())
for a,b in zip(xs,xs[1:]): ax.text((a+b)/2,-1.9,f"{(b-a)*1000:,.0f}",ha="center",fontsize=7.5,color="#555")
for a,b in zip(ys,ys[1:]): ax.text(29.2,(a+b)/2,f"{(b-a)*1000:,.0f}",va="center",fontsize=7.5,color="#555")
ax.text(0,-3.0,"Analytical column layout — all column centrelines on grid intersections (C2 construction offset of 75 mm removed).  "
        "Symbols drawn 2× size.  Filled = full height to Roof +11.15;  hollow = stops under 2F +4.75.",fontsize=8.5,color="#333")
ax.plot([],[],"s",color="#1f5fbf",label="C1 250×250 (FT 350×350)"); ax.plot([],[],"s",color="#c0392b",label="C2 250×400 (FT 350×500)")
ax.legend(loc="upper right",fontsize=8.5,frameon=False,bbox_to_anchor=(1.0,1.08),ncol=2)
ax.set_xlim(-3,30.5); ax.set_ylim(-3.5,17.2); ax.set_aspect("equal"); ax.axis("off")
fig.savefig(SC+"/fs_col_plan.png",dpi=120,facecolor="white"); print("saved fs_col_plan.png")
