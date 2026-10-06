# -*- coding: utf-8 -*-
# Mesh the slab panels of one level with MIDAS /ope/AUTOMESH, one panel per call.
# usage: python slab_build.py <MAPI_KEY> <LEVEL> [panel numbers e.g. 1 or 2-19]   (default: all not yet done)
#        python slab_build.py <MAPI_KEY> <LEVEL> verify
import sys, os, json, math
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
KEY,L=sys.argv[1],sys.argv[2]; ARG=sys.argv[3] if len(sys.argv)>3 else ""
S=json.load(open(SC+f"/fs_slab_{L}.json")); Z=S["z"]
THK={"GS1":1,"S1":2,"S1C":3,"RS1":4}
GRP={"GB":(8,"BEAM_GB",13,"SLAB_GB"),"2F":(9,"BEAM_2F",14,"SLAB_2F"),"3F":(10,"BEAM_3F",15,"SLAB_3F"),
     "RF":(11,"BEAM_RF",16,"SLAB_RF"),"AR":(12,"BEAM_AR",17,"SLAB_AR")}
DONE=SC+f"/fs_slab_{L}_done.json"
done=json.load(open(DONE)) if os.path.exists(DONE) else {}
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(KEY)
import midas_gen as mg
def G(ep,k):
    r=mg.MidasAPI("GET",ep,{}); r=r.get(k,{}) if isinstance(r,dict) else {}; return r if isinstance(r,dict) else {}
def xy(n): return (round(n["X"]*1000),round(n["Y"]*1000))

def level_beams(nodes,elem):
    """horizontal BEAM elements at this level -> {id:(pa,pb)} in mm"""
    out={}
    for k,e in elem.items():
        if e["TYPE"]!="BEAM": continue
        a,b=nodes.get(str(e["NODE"][0])),nodes.get(str(e["NODE"][1]))
        if a and b and abs(a["Z"]-Z)<1e-4 and abs(b["Z"]-Z)<1e-4: out[int(k)]=(xy(a),xy(b))
    return out
def on_seg(p,a,b,tol=2):
    L2=(b[0]-a[0])**2+(b[1]-a[1])**2; t=((p[0]-a[0])*(b[0]-a[0])+(p[1]-a[1])*(b[1]-a[1]))/L2
    e=tol/math.sqrt(L2)                                                     # tolerance also along the segment (rounded node coords)
    return -e<=t<=1+e and math.hypot(p[0]-a[0]-t*(b[0]-a[0]),p[1]-a[1]-t*(b[1]-a[1]))<tol
def boundary_targets(panel,beams):
    P=[tuple(p) for p in panel["poly"]]; segs=list(zip(P,P[1:]+P[:1])); T=[]
    for eid,(pa,pb) in beams.items():
        if any(on_seg(pa,a,b) and on_seg(pb,a,b) for a,b in segs): T.append(eid)
    return T

def put_ok(ep,body):
    r=mg.MidasAPI("PUT",ep,body); return isinstance(r,dict) and "error" not in json.dumps(r)
def free_prepare(p):
    """make every polygon vertex a node (splitting a beam if the vertex lies inside it) and add temporary lines on free edges"""
    nodes=G("/db/NODE","NODE"); elem=G("/db/ELEM","ELEM")
    at={xy(v):int(k) for k,v in nodes.items() if abs(v["Z"]-Z)<1e-4}
    nmax=max(int(k) for k in nodes); emax=max(int(k) for k in elem); newn={}; newe={}; split=[]
    def node_at(pt):
        nonlocal nmax
        key=(round(pt[0]),round(pt[1]))
        for q,i in at.items():
            if abs(q[0]-pt[0])<2 and abs(q[1]-pt[1])<2: return i
        nmax+=1; newn[str(nmax)]={"X":pt[0]/1000,"Y":pt[1]/1000,"Z":Z}; at[key]=nmax; return nmax
    beams=level_beams(nodes,elem)
    for v in p["poly"]:
        if any(abs(q[0]-v[0])<2 and abs(q[1]-v[1])<2 for q in at): continue
        host=[k for k,(a,b) in beams.items() if on_seg(v,a,b) and math.dist(v,a)>2 and math.dist(v,b)>2]
        n=node_at(v)
        for k in host:                                            # split host beam at the new node
            e=dict(elem[str(k)]); e["NODE"]=list(e["NODE"]); j=e["NODE"][1]; e["NODE"][1]=n; newe[str(k)]=e
            emax+=1; e2=dict(elem[str(k)]); e2["NODE"]=list(e2["NODE"]); e2["NODE"][0]=n; e2["NODE"][1]=j; newe[str(emax)]=e2; split.append((k,emax))
    tmp=[]
    for a,b in p["free"]:
        have=sum(math.dist(pa,pb) for pa,pb in beams.values() if on_seg(pa,a,b) and on_seg(pb,a,b))
        if abs(have-math.dist(a,b))<5: continue                             # line already there (re-run)
        emax+=1; newe[str(emax)]={"TYPE":"BEAM","MATL":1,"SECT":204,"NODE":[node_at(a),node_at(b)],"ANGLE":0,"STYPE":0}; tmp.append(emax)
    if newn: assert put_ok("/db/NODE",{"Assign":newn})
    if newe: assert put_ok("/db/ELEM",{"Assign":newe})
    if split:                                                     # new beam piece joins the parent's beam group(s)
        g=G("/db/GRUP","GRUP"); upd={}
        for k,k2 in split:
            for gid,gp in g.items():
                if k in gp.get("E_LIST",[]): upd.setdefault(gid,dict(gp,E_LIST=[]))["E_LIST"].append(k2)
        if upd: put_ok("/db/GRUP",{"Assign":upd})
    print(f"   prepared: new nodes {len(newn)}  beams split {split}  temporary free-edge lines {tmp}")
    return tmp
def free_cleanup(p):
    """delete every line element lying on the free edges (temporary lines and their split pieces)"""
    nodes=G("/db/NODE","NODE"); elem=G("/db/ELEM","ELEM"); beams=level_beams(nodes,elem)
    dead=sorted(k for k,(a,b) in beams.items() if any(on_seg(a,f0,f1) and on_seg(b,f0,f1) for f0,f1 in p["free"]))
    n0=len(elem); mg.MidasAPI("DELETE","/db/ELEM/"+",".join(map(str,dead)),{}); n1=len(G("/db/ELEM","ELEM"))
    print(f"   temporary lines deleted: {len(dead)}  elements {n0} -> {n1}  {'OK' if n0-n1==len(dead) else 'UNEXPECTED'}")
    if n0-n1!=len(dead): sys.exit("STOP: temporary line delete mismatch")

def verify(title):
    nodes=G("/db/NODE","NODE"); elem=G("/db/ELEM","ELEM"); grup=G("/db/GRUP","GRUP")
    beams=level_beams(nodes,elem)
    plates={int(k):e for k,e in elem.items() if e["TYPE"]=="PLATE" and all(abs(nodes[str(n)]["Z"]-Z)<1e-4 for n in e["NODE"] if n)}
    area=0; edges=Counter()
    for e in plates.values():
        ns=[n for n in e["NODE"] if n]; P=[xy(nodes[str(n)]) for n in ns]
        area+=abs(sum(P[i][0]*P[i-1][1]-P[i-1][0]*P[i][1] for i in range(len(P))))/2e6
        for i in range(len(ns)): edges[frozenset((ns[i-1],ns[i]))]+=1
    beampairs={frozenset(elem[str(k)]["NODE"][:2]) for k in beams}
    free=[e for e,c in edges.items() if c==1]
    FREE=[f for q in S["panels"] for f in q.get("free",[])]
    def on_free(ed):
        a,b=[xy(nodes[str(n)]) for n in ed]; return any(on_seg(a,f0,f1) and on_seg(b,f0,f1) for f0,f1 in FREE)
    free_nobeam=[tuple(e) for e in free if e not in beampairs and not on_free(e)]
    free_slab_edge=sum(1 for e in free if e not in beampairs and on_free(e))
    # plate edge lying on a beam line but with no beam of the same node pair = not connected
    def on_any_beam(ed):
        a,b=[xy(nodes[str(n)]) for n in ed]
        return any(on_seg(a,pa,pb) and on_seg(b,pa,pb) for pa,pb in beams.values())
    unconnected=[tuple(e) for e in edges if e not in beampairs and on_any_beam(e)]
    lvlnodes=[n for n,v in nodes.items() if abs(v["Z"]-Z)<1e-4]
    dup=[k for k,c in Counter(xy(nodes[n]) for n in lvlnodes).items() if c>1]
    blen=sum(math.dist(a,b) for a,b in beams.values())/1000
    bg=set(grup.get(str(GRP[L][0]),{}).get("E_LIST",[])); miss=[k for k in beams if k not in bg]
    print(f"--- {title}: plates {len(plates)}  area {area:.2f} m²  | beams at level {len(beams)} total length {blen:.3f} m  "
          f"| slab free-edge plate edges {free_slab_edge}  other free plate edges without beam {len(free_nobeam)}  unconnected plate edges on beam lines {len(unconnected)}  "
          f"| duplicate nodes {len(dup)}  | beams not in {GRP[L][1]}: {len(miss)}")
    return dict(plates=plates,area=area,beams=beams,blen=blen,free_nobeam=free_nobeam,unconnected=unconnected,dup=dup,miss=miss,grup=grup,elem=elem)

if ARG=="verify":
    v=verify("VERIFY"); print("free edges w/o beam:",v["free_nobeam"][:10]," unconnected:",v["unconnected"][:10]," dup:",v["dup"][:10]); sys.exit()

# ---- select panels ----
nums=[p["no"] for p in S["panels"]]
if ARG:
    a,_,b=ARG.partition("-"); nums=list(range(int(a),int(b or a)+1))
todo=[p for p in S["panels"] if p["no"] in nums and p["name"] not in done and not p.get("opening")]
nodes=G("/db/NODE","NODE"); elem=G("/db/ELEM","ELEM")
if not done:
    json.dump({"NODE":nodes,"ELEM":elem,"GRUP":G("/db/GRUP","GRUP")},open(SC+f"/midas_backup_before_slab_{L}.json","w"))
    print("backup saved")
v0=verify("BEFORE")
# cantilever corner nodes on beams (and temporary edge lines) FIRST, so every panel meshed later shares those nodes
for p in todo:
    if p.get("free"): free_prepare(p)
for p in todo:
    if p.get("free"): free_prepare(p)
    nodes=G("/db/NODE","NODE"); elem=G("/db/ELEM","ELEM"); beams=level_beams(nodes,elem)
    T=boundary_targets(p,beams)
    cover=sum(math.dist(*beams[t]) for t in T); perim=sum(math.dist(p["poly"][i-1],p["poly"][i]) for i in range(len(p["poly"])))
    if abs(cover-perim)>5: sys.exit(f"STOP {p['name']}: boundary beams cover {cover:.0f} of {perim:.0f} mm")
    body={"Argument":{"MESHER":{"METHOD":"Line Elements","TARGETS":sorted(T),"TYPE":p["mesh"],"MESH_INNER_DOMAIN":False,
                                "INCLUDE_INTERIOR_NODES":{"OPT_CHECK":False},"INCLUDE_INTERIOR_LINES":{"OPT_CHECK":False},
                                "INCLUDE_BOUNDARY_CONNECTIVITY":True},
                      "MESH_SIZE":{"LENGTH":S["mesh"]},
                      "PROPERTY":{"ELEMENT_TYPE":"Plate","ELEMENT_SUB_TYPE":{"TYPE":"Thick"},"MATERIAL":1,"THICKNESS":THK[p["type"]]},
                      "DOMAIN_NAME":{"NAME":p["name"]},
                      "ADDITIONAL_OPTION":{"DELETE_LINE_ELEM":False,"SUBDIVIDE_LINE_ELEM":True}}}
    doms={v.get("NAME") for v in G("/db/MADO","MADO").values()}
    if p["name"] in doms:                                                   # domain name already used (re-mesh): auto-mesh refuses it
        k=2
        while f"{p['name']}-{k}" in doms: k+=1
        body["Argument"]["DOMAIN_NAME"]["NAME"]=f"{p['name']}-{k}"; print("   domain name in use ->",body["Argument"]["DOMAIN_NAME"]["NAME"])
    tries=[(p["mesh"],S["mesh"]),("Quad and Triangle",S["mesh"]),("Quadrilateral",S["mesh"]),("Quad and Triangle",0.4),("Triangle",S["mesh"])]
    for typ,size in tries:                                                  # fallback when the mesher reports failure
        body["Argument"]["MESHER"]["TYPE"]=typ; body["Argument"]["MESH_SIZE"]["LENGTH"]=size
        r=mg.MidasAPI("POST","/ope/AUTOMESH",body)
        if not (isinstance(r,dict) and "error" in r): break
        print(f"   mesher failed with {typ} / {size} m -> retry")
    if (typ,size)!=tries[0]: print(f"   used: {typ} / {size} m")
    after=G("/db/ELEM","ELEM"); new={k:e for k,e in after.items() if k not in elem}      # diff: works also when MIDAS answers with a warning
    warn=r.get("message","") if isinstance(r,dict) else ""
    if not new: sys.exit(f"STOP {p['name']}: nothing created. AUTOMESH returned {json.dumps(r)[:300]}")
    if warn: print("   MIDAS message:",warn[:160])
    nsplit=sum(1 for e in new.values() if e["TYPE"]!="PLATE"); new={k:e for k,e in new.items() if e["TYPE"]=="PLATE"}   # response also lists split beam pieces
    nodes=G("/db/NODE","NODE")
    ar=sum(abs(sum(P[i][0]*P[i-1][1]-P[i-1][0]*P[i][1] for i in range(len(P))))/2e6
           for P in [[xy(nodes[str(n)]) for n in e["NODE"] if n] for e in new.values()])
    zs={round(nodes[str(n)]["Z"],4) for e in new.values() for n in e["NODE"] if n}
    tri=sum(1 for e in new.values() if len([n for n in e["NODE"] if n])==3)
    ok=abs(ar-p["area"])<0.01 and zs=={round(Z,4)}
    print(f"{p['name']} {p['type']:4} boundary beams {len(T):2} -> plates {len(new):3} (tri {tri})  new beam pieces {nsplit:2}  area {ar:6.2f}/{p['area']:6.2f}  Z {zs}  {'OK' if ok else 'CHECK'}")
    if p.get("free"): free_cleanup(p)
    done[p["name"]]=sorted(int(k) for k in new)
    json.dump(done,open(DONE,"w"))
    if not ok: sys.exit("STOP: area or level mismatch")

v=verify("AFTER")
if abs(v["blen"]-v0["blen"])>0.001: print(f"!! beam total length changed {v0['blen']:.3f} -> {v['blen']:.3f}")
# ---- groups: split beam pieces -> BEAM_<L>; plates -> SLAB_<L> ----
bg,bn,sg,sn=GRP[L]; grup=v["grup"]; upd={}
if v["miss"]:
    g=dict(grup[str(bg)]); g["E_LIST"]=sorted(set(g["E_LIST"])|set(v["miss"])); upd[str(bg)]=g
allpl=sorted({e for ids in done.values() for e in ids if v["elem"].get(str(e),{}).get("TYPE")=="PLATE"})
upd[str(sg)]={"NAME":sn,"P_TYPE":0,"N_LIST":[],"E_LIST":allpl}
# one structure group per panel (user's choice instead of domains): SLAB_<L>-Pxx, id = level base + panel no.
BASE={"GB":100,"2F":200,"3F":300,"RF":400,"AR":500}[L]
for name,ids in done.items():
    upd[str(BASE+int(name.split("-P")[1]))]={"NAME":f"SLAB_{name}","P_TYPE":0,"N_LIST":[],
        "E_LIST":sorted(e for e in ids if v["elem"].get(str(e),{}).get("TYPE")=="PLATE")}
# NOTE: PUT /db/GRUP MERGES E_LIST into an existing group - never write beams into a slab group
mg.MidasAPI("PUT","/db/GRUP",{"Assign":upd}); print("groups updated:",{k:(g["NAME"],len(g["E_LIST"])) for k,g in upd.items()})
verify("FINAL")
