# -*- coding: utf-8 -*-
# Load combinations per Ministerial Regulation B.E. 2566:
#   clause 7 (strength / LRFD) -> /db/LCOM-GEN and /db/LCOM-CONC (concrete design)
#   clause 6 (service / ASD)   -> /db/LCOM-GEN only (foundation / pile checks, deflection)
# Dead load นค. = DL (self-weight) + SDL.  Seismic รผ. = Ex, Ey (static ELF cases) in + and - direction.
# usage: python make_combos.py <MAPI_KEY>
import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
G=lambda ep,k:(lambda r:r.get(k,{}) if isinstance(r,dict) else {})(mg.MidasAPI("GET",ep,{}))
ST={v["NAME"] for v in G("/db/STLD","STLD").values()}
need={"DL","SDL","LL","Ex","Ey"}; assert need<=ST, f"load cases missing: {need-ST}"
for ep,k in (("/db/LCOM-GEN","LCOM-GEN"),("/db/LCOM-CONC","LCOM-CONC")):
    ex=G(ep,k)
    if ex: sys.exit(f"STOP: {ep} already has {len(ex)} combinations: {[v['NAME'] for v in ex.values()]}")
def D(f): return [("DL",f),("SDL",f)]
U=[("U1","1.4D + 1.7L  (cl.7(1))",D(1.4)+[("LL",1.7)])]
for e in ("Ex","Ey"):
    for s,sg in ((1,"+"),(-1,"-")):
        U.append((f"U{len(U)+1}",f"0.75(1.4D+1.7L) {sg}1.0{e}  (cl.7(3))",D(1.05)+[("LL",1.275),(e,1.0*s)]))
for e in ("Ex","Ey"):
    for s,sg in ((1,"+"),(-1,"-")):
        U.append((f"U{len(U)+1}",f"0.9D {sg}1.0{e}  (cl.7(3))",D(0.9)+[(e,1.0*s)]))
S=[("S1","D + L  (cl.6(1))",D(1.0)+[("LL",1.0)])]
for e in ("Ex","Ey"):
    for s,sg in ((1,"+"),(-1,"-")): S.append((f"S{len(S)+1}",f"D {sg}0.7{e}  (cl.6(3))",D(1.0)+[(e,0.7*s)]))
for e in ("Ex","Ey"):
    for s,sg in ((1,"+"),(-1,"-")): S.append((f"S{len(S)+1}",f"D {sg}0.525{e} + 0.75L  (cl.6(3))",D(1.0)+[(e,0.525*s),("LL",0.75)]))
for e in ("Ex","Ey"):
    for s,sg in ((1,"+"),(-1,"-")): S.append((f"S{len(S)+1}",f"0.6D {sg}0.7{e}  (cl.6(3))",D(0.6)+[(e,0.7*s)]))
def item(n,d,terms,conc=False):
    it={"NAME":n,"ACTIVE":"ACTIVE","iTYPE":0,"DESC":d,"vCOMB":[{"ANAL":"ST","LCNAME":c,"FACTOR":round(f,4)} for c,f in terms]}
    if conc: it["bES"]=False
    return it
gen={str(i+1):item(*c) for i,c in enumerate(U+S)}
con={str(i+1):item(*c,conc=True) for i,c in enumerate(U)}
for ep,body in (("/db/LCOM-GEN",gen),("/db/LCOM-CONC",con)):
    r=mg.MidasAPI("PUT",ep,{"Assign":body}); print(ep,"PUT ->","OK" if isinstance(r,dict) and "error" not in json.dumps(r) else json.dumps(r)[:300])
# ---- verify ----
for ep,k,want in (("/db/LCOM-GEN","LCOM-GEN",gen),("/db/LCOM-CONC","LCOM-CONC",con)):
    got=G(ep,k); bad=[]
    for i,w in want.items():
        g=got.get(i)
        if not g or g["NAME"]!=w["NAME"] or {(c["LCNAME"],round(c["FACTOR"],4)) for c in g["vCOMB"]}!={(c["LCNAME"],c["FACTOR"]) for c in w["vCOMB"]}: bad.append(i)
    print(f"VERIFY {ep}: {len(got)} combinations, mismatches {bad}")
for n,d,t in U+S: print(f"  {n:4} {d:42} " + " + ".join(f"{f:g}{c}" for c,f in t).replace("+ -","- "))
