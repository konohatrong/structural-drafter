# -*- coding: utf-8 -*-
# Remove BX members, merge collinear same-mark pieces at orphaned (non-column) nodes, check connectivity.
import sys, json, math, shutil
from collections import defaultdict, Counter
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
B=json.load(open(SC+"/fs_beammodel_withBX.json"))   # always start from the pre-removal set
for L,d in B.items():
    cn={tuple(map(int,map(float,k.split(",")))) for k in d["colnodes"]}
    E=[dict(a=tuple(e["a"]),b=tuple(e["b"]),mark=e["mark"],src=e["src"]) for e in d["elems"]]
    def trimmer(e):
        (x1,y1),(x2,y2)=e["a"],e["b"]
        onx=lambda v:abs(x1-v)<5 and abs(x2-v)<5
        ony=lambda v:abs(y1-v)<5 and abs(y2-v)<5
        return (onx(1500) or onx(1501) or onx(20926) or ony(4550)
                or (ony(5900) and max(x1,x2)<=3200))
    fixed=0
    for e in E:
        if e["mark"]=="BX" and not trimmer(e): e["mark"]="B1"; e["src"]="rule"; fixed+=1
        elif trimmer(e) and L in("2F","3F"): e["mark"]="BX"
    print(f"{L:3} BX labels corrected to B1: {fixed}")
    nBX=sum(1 for e in E if e["mark"]=="BX")
    E=[e for e in E if e["mark"]!="BX"]
    # re-attach dead-ends left by BX removal to the column node on the same grid line (<=650 mm)
    deg=Counter([e["a"] for e in E]+[e["b"] for e in E]); reat=0
    for e in E:
        for end,other in (("a","b"),("b","a")):
            p=e[end]
            if p in cn or deg[p]!=1: continue
            q=e[other]; vert=abs(p[0]-q[0])<5; horiz=abs(p[1]-q[1])<5
            cands=[c for c in cn if (vert and abs(c[0]-p[0])<5) or (horiz and abs(c[1]-p[1])<5)]
            cands=[c for c in cands if math.dist(c,p)<=650 and math.dist(c,q)>math.dist(p,q)]
            if cands:
                c=min(cands,key=lambda c:math.dist(c,p)); e[end]=c; reat+=1
    print(f"    re-attached dead-ends: {reat}")
    merged=0
    while True:
        adj=defaultdict(list)
        for i,e in enumerate(E): adj[e["a"]].append(i); adj[e["b"]].append(i)
        done=False
        for p,ids in adj.items():
            if p in cn or len(ids)!=2: continue
            e1,e2=E[ids[0]],E[ids[1]]
            if e1["mark"]!=e2["mark"]: continue
            q1=e1["b"] if e1["a"]==p else e1["a"]; q2=e2["b"] if e2["a"]==p else e2["a"]
            cross=(q1[0]-p[0])*(q2[1]-p[1])-(q1[1]-p[1])*(q2[0]-p[0])
            if abs(cross)>1e-6*max(1,math.dist(q1,p)*math.dist(q2,p)): continue   # not collinear
            src="text" if "text" in (e1["src"],e2["src"]) else e1["src"]
            new=dict(a=q1,b=q2,mark=e1["mark"],src=src)
            E=[e for k,e in enumerate(E) if k not in ids]+[new]; merged+=1; done=True; break
        if not done: break
    # connectivity: every beam component must touch a column node
    par={}
    def f(x):
        par.setdefault(x,x)
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for e in E: par[f(e["a"])]=f(e["b"])
    comps=defaultdict(set)
    for e in E: comps[f(e["a"])].update([e["a"],e["b"]])
    floating=[c for c in comps.values() if not (c & cn)]
    newn={p for e in E for p in (e["a"],e["b"])}-cn
    print(f"{L:3} removed BX={nBX:2}  merged={merged:2}  beams={len(E):3}  new nodes={len(newn):2}  "
          f"floating groups={len(floating)}  marks={dict(sorted(Counter(e['mark'] for e in E).items()))}")
    if floating: print("   FLOATING:",floating)
    d["elems"]=[dict(a=list(e["a"]),b=list(e["b"]),mark=e["mark"],src=e["src"]) for e in E]
json.dump(B,open(SC+"/fs_beammodel.json","w"),indent=1)
print("saved fs_beammodel.json (backup: fs_beammodel_withBX.json)")
