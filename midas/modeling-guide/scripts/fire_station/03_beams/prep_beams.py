# -*- coding: utf-8 -*-
# Build analytical beam set (no MIDAS write). Units: mm in processing, m in output.
import sys, json, math
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
R=json.load(open(SC+"/fs_beams_raw.json")); CM=json.load(open(SC+"/fs_colmodel.json"))
GX=sorted(v*1000 for v in CM["GX"].values()); GY=sorted(v*1000 for v in CM["GY"].values())
LV={"GB":("GF",0.35),"2F":("2F",4.75),"3F":("3F",7.95),"RF":("RF",11.15)}
SECT={"GB1":201,"GB1A":202,"GB1C":203,"B1":204,"B1A":205,"B1C":206,"B2":207,"BX":208,"B2A":209}
def P(g): return (CM["GX"][g[1:]]*1000, CM["GY"][g[0]]*1000)

out={}; notes=[]
for L,(clev,z) in LV.items():
    colnodes={(round(v["X"]*1000),round(v["Y"]*1000)):int(k) for k,v in CM["nodes"].items() if v["lev"]==clev}
    segs=[dict(x1=s["x1"],y1=s["y1"],x2=s["x2"],y2=s["y2"],mark=s["mark"]) for s in R["segs"][L]]
    marks=R["marks"].get(L,[])
    # ---------------- level-specific fixes ----------------
    if L=="2F":   # displaced east bay -> shift back
        for s in segs:
            if min(s["x1"],s["x2"])>25500 and min(s["y1"],s["y2"])>7000:
                s["x1"]-=2645; s["x2"]-=2645; s["y1"]-=7802; s["y2"]-=7802
        marks=[(m[0]-2645,m[1]-7802,m[2],m[3]) if (m[0]>25500 and m[1]>7000) else m for m in marks]
        segs.append(dict(x1=27250,y1=4000,x2=23550,y2=8000,mark="B2",fixed=True))          # chamfer E7-D6
    if L=="GB":   # replace partial edge by full straight edge A2->D6 + GB1C stubs + chamfer
        segs=[s for s in segs if not (abs(s["x1"]-s["x2"])>5 and abs(s["y1"]-s["y2"])>5)]   # drop diag
        segs=[s for s in segs if not (abs(s["x1"]-8750)<5 and min(s["y1"],s["y2"])>12050)]   # drop B3 stub piece
        ax,ay=P("A2"); dx_,dy_=P("D6"); k=(dy_-ay)/(dx_-ax)
        segs.append(dict(x1=ax,y1=ay,x2=dx_,y2=dy_,mark="GB1",fixed=True))
        for g in ["B3","C4","D5"]:
            gx,gy=P(g); ey=ay+k*(gx-ax)
            segs=[s for s in segs if not (abs(s["x1"]-gx)<5 and abs(s["x2"]-gx)<5 and min(s["y1"],s["y2"])>gy+50)]
            segs.append(dict(x1=gx,y1=gy,x2=gx,y2=ey,mark="GB1C",fixed=True,force="GB1C"))
        ex,ey=P("E7"); segs.append(dict(x1=dx_,y1=dy_,x2=ex,y2=ey,mark="GB1",fixed=True))
    if L=="3F":   # rebuild secondary line at y=5900 (unify 5750->5900), trim edge B2 tail
        keep=[]
        for s in segs:
            h=abs(s["y1"]-s["y2"])<5
            if h and 5700<s["y1"]<5950: continue
            if abs(s["x1"]-22275)<5 and abs(s["x2"]-22275)<5:
                s["y1"],s["y2"]=0,4000;
            keep.append(s)
        segs=keep+[dict(x1=0,y1=5900,x2=22275,y2=5900,mark="?")]
        marks=[(m[0],5900 if 5650<m[1]<6100 and m[3]==0 else m[1],m[2],m[3]) for m in marks]
    # ---------------- cross-axis snapping ----------------
    def snap(v,G,tol=200):
        g=min(G,key=lambda a:abs(a-v)); return g if abs(g-v)<=tol else v
    for s in segs:
        if s.get("fixed"): continue
        if abs(s["y1"]-s["y2"])<5:  s["y1"]=s["y2"]=snap((s["y1"]+s["y2"])/2,GY)
        elif abs(s["x1"]-s["x2"])<5: s["x1"]=s["x2"]=snap((s["x1"]+s["x2"])/2,GX)
    # cluster off-grid positions (30 mm)
    for key in [("x1","x2",lambda s:abs(s["x1"]-s["x2"])<1),("y1","y2",lambda s:abs(s["y1"]-s["y2"])<1)]:
        a,b,f=key; vals=sorted({round(s[a]) for s in segs if f(s)})
        rep={}
        for v in vals:
            c=[w for w in vals if abs(w-v)<=30]; rep[v]=round(sum(c)/len(c))
        for s in segs:
            if f(s): s[a]=s[b]=rep[round(s[a])]
    # ---------------- along-axis end extension ----------------
    H=[s for s in segs if abs(s["y1"]-s["y2"])<1 and not s.get("fixed")]; V=[s for s in segs if abs(s["x1"]-s["x2"])<1 and not s.get("fixed")]
    D=[s for s in segs if s not in H and s not in V and not s.get("fixed")]
    def vlines_at(y):   # x of vertical members passing y (beams or columns)
        xs={s["x1"] for s in V if min(s["y1"],s["y2"])-350<=y<=max(s["y1"],s["y2"])+350}
        xs|={x for (x,yy) in colnodes if abs(yy-y)<5}
        return xs
    def hlines_at(x):
        ys={s["y1"] for s in H if min(s["x1"],s["x2"])-350<=x<=max(s["x1"],s["x2"])+350}
        ys|={yy for (xx,yy) in colnodes if abs(xx-x)<5}
        return ys
    for s in H:
        for e in ("x1","x2"):
            c=vlines_at(s["y1"]); cc={x for (x,yy) in colnodes if abs(yy-s["y1"])<5}
            if c:
                n=min(c,key=lambda v:abs(v-s[e]))
                if abs(n-s[e])<=350: s[e]=n; continue
            if cc:
                n=min(cc,key=lambda v:abs(v-s[e]))
                if abs(n-s[e])<=650: s[e]=n
    for s in V:
        for e in ("y1","y2"):
            c=hlines_at(s["x1"]); cc={yy for (xx,yy) in colnodes if abs(xx-s["x1"])<5}
            if c:
                n=min(c,key=lambda v:abs(v-s[e]))
                if abs(n-s[e])<=350: s[e]=n; continue
            if cc:
                n=min(cc,key=lambda v:abs(v-s[e]))
                if abs(n-s[e])<=650: s[e]=n
    allnodes=set(colnodes)
    for s in D:
        for ex,ey in (("x1","y1"),("x2","y2")):
            n=min(allnodes,key=lambda p:math.hypot(p[0]-s[ex],p[1]-s[ey]))
            if math.hypot(n[0]-s[ex],n[1]-s[ey])<=600: s[ex],s[ey]=n
    # ---------------- split at junctions ----------------
    pts=set(colnodes)
    for s in segs: pts.add((round(s["x1"]),round(s["y1"]))); pts.add((round(s["x2"]),round(s["y2"])))
    # crossing points H x V
    for h in H:
        for v in V:
            x,y=v["x1"],h["y1"]
            if min(h["x1"],h["x2"])+1<x<max(h["x1"],h["x2"])-1 and min(v["y1"],v["y2"])+1<y<max(v["y1"],v["y2"])-1:
                pts.add((round(x),round(y)))
    elems=[]
    for s in segs:
        x1,y1,x2,y2=s["x1"],s["y1"],s["x2"],s["y2"]; Lg=math.hypot(x2-x1,y2-y1)
        if Lg<1: continue
        ux,uy=(x2-x1)/Lg,(y2-y1)/Lg
        on=[]
        for (px,py) in pts:
            t=(px-x1)*ux+(py-y1)*uy; d=abs((px-x1)*uy-(py-y1)*ux)
            if -1<t<Lg+1 and d<5: on.append((t,(px,py)))
        on=sorted(set(on))
        for (t0,a),(t1,b) in zip(on,on[1:]):
            if t1-t0>1: elems.append({"a":a,"b":b,"pmark":s["mark"],"force":s.get("force")})
    # dedupe
    uniq={}
    for e in elems:
        k=tuple(sorted([e["a"],e["b"]]))
        if k not in uniq or uniq[k]["pmark"]=="?": uniq[k]=e
    elems=list(uniq.values())
    # ---------------- marks per span ----------------
    for e in elems:
        (x1,y1),(x2,y2)=e["a"],e["b"]; Lg=math.hypot(x2-x1,y2-y1); ux,uy=(x2-x1)/Lg,(y2-y1)/Lg
        diag=abs(ux)>0.05 and abs(uy)>0.05; want=0 if abs(uy)<0.05 else 90
        best=None; bd=1e9
        for (tx,ty,t,r) in marks:
            tt=(tx-x1)*ux+(ty-y1)*uy
            if tt<-100 or tt>Lg+100: continue
            d=abs((tx-x1)*uy-(ty-y1)*ux)+(0 if (diag or r==want) else 3000)
            if d<bd: bd=d; best=t
        e["mark"]=best if bd<900 else e["pmark"]
        e["src"]="text" if bd<900 else "parent"
    # resolve '?' from collinear neighbour on same line
    for e in elems:
        if e["mark"]!="?": continue
        (x1,y1),(x2,y2)=e["a"],e["b"]
        for f in elems:
            if f is e or f["mark"]=="?": continue
            if {e["a"],e["b"]}&{f["a"],f["b"]}:
                (u1,v1),(u2,v2)=f["a"],f["b"]
                if abs((x2-x1)*(v2-v1)-(y2-y1)*(u2-u1))<1e-3*max(1,abs(x2-x1)+abs(y2-y1))*max(1,abs(u2-u1)+abs(v2-v1)):
                    e["mark"]=f["mark"]; e["src"]="neighbour"; break
    for e in elems:
        (x1,y1),(x2,y2)=e["a"],e["b"]
        if e.get("force"): e["mark"]=e["force"]; e["src"]="text"; continue
        if L in("2F","3F") and abs(y1-5900)<5 and abs(y2-5900)<5 and max(x1,x2)<=3200 and min(x1,x2)>=1400:
            e["mark"]="BX"; e["src"]="rule"                     # stair header continuation
        elif e["src"]!="text" and e["mark"]=="B1A" and not (8700<=min(x1,x2) and max(x1,x2)<=12800):
            e["mark"]="B1"; e["src"]="rule"                     # typical span
    out[L]={"z":z,"clev":clev,"elems":elems,"colnodes":{f"{k[0]},{k[1]}":v for k,v in colnodes.items()}}
    c=Counter(e["mark"] for e in elems); newn={p for e in elems for p in (e["a"],e["b"])}-set(colnodes)
    print(f"{L:3} z=+{z:<5}  beams={len(elems):3}  new nodes={len(newn):2}  marks={dict(sorted(c.items()))}  "
          f"inferred={sum(1 for e in elems if e['src']!='text')}")

# serialise
ser={L:{"z":d["z"],"clev":d["clev"],"elems":[{"a":list(e["a"]),"b":list(e["b"]),"mark":e["mark"],"src":e["src"]} for e in d["elems"]],
        "colnodes":d["colnodes"]} for L,d in out.items()}
json.dump(ser,open(SC+"/fs_beammodel.json","w"),indent=1)
print("saved fs_beammodel.json")
