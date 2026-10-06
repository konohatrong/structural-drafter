# -*- coding: utf-8 -*-
# Building B (fire station): pull report data from the live model (read-only; runs analysis only if results are missing).
import sys, os, json, math
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
G=lambda ep,k:(lambda r:r.get(k,{}) if isinstance(r,dict) else {})(mg.MidasAPI("GET",ep,{}))
def rows(df): return [dict(zip(df.columns,r)) for r in df.rows()]
def react(lc):
    try: return rows(mg.Result.TABLE.Reaction(loadcase=[lc]))
    except Exception as e: return None
if react("DL(ST)") is None:
    print("no results -> running analysis"); print(mg.MidasAPI("POST","/doc/ANAL",{"Assign":{}}))
N=G("/db/NODE","NODE"); E=G("/db/ELEM","ELEM"); S=G("/db/SECT","SECT"); T=G("/db/THIK","THIK"); ST=G("/db/STOR","STOR")
out={"counts":dict(nodes=len(N),elems=len(E),beam=sum(1 for v in E.values() if v["TYPE"]=="BEAM"),plate=sum(1 for v in E.values() if v["TYPE"]=="PLATE")),
     "stor":ST,"thik":{k:(v["NAME"],v["T_IN"]) for k,v in T.items()},"sect":{k:v["SECT_NAME"] for k,v in S.items()},
     "ltom":G("/db/ltom","LTOM"),"lcom":{v["NAME"]:(v.get("DESC",""),[(c["LCNAME"],c["FACTOR"]) for c in v["vCOMB"]]) for v in G("/db/LCOM-GEN","LCOM-GEN").values()},
     "dcon":G("/db/DCON","DCON"),"matd":G("/db/MATD","MATD")}
R={}
for lc in ["DL(ST)","SDL(ST)","LL(ST)","Ex(ST)","Ey(ST)","U1(CB)","S1(CB)"]:
    r=react(lc)
    if r is None: print("  no reaction table for",lc); continue
    r=[x for x in r if str(x.get("Load","")).strip()!="SUMMATION" and x.get("Node") not in (None,"")]
    R[lc]=r; print(f"  {lc:8} rows {len(r):3}  sum FX {sum(float(x['FX']) for x in r):9.1f}  FY {sum(float(x['FY']) for x in r):9.1f}  FZ {sum(float(x['FZ']) for x in r):10.1f}")
out["react"]=R
sup=sorted({int(x["Node"]) for x in R["DL(ST)"]}); out["sup"]={n:(N[str(n)]["X"],N[str(n)]["Y"],N[str(n)]["Z"]) for n in sup}
# displacements per level (max over nodes at that level) for Ex / Ey and vertical for service
LEV=[(-1.0,"Base"),(0.35,"GF"),(3.95,"Annex roof"),(4.75,"2F"),(7.95,"3F"),(11.15,"Roof")]
D={}
for lc,comp in (("Ex(ST)","DX"),("Ey(ST)","DY"),("S1(CB)","DZ"),("DL(ST)","DZ")):
    try: d=rows(mg.Result.TABLE.Displacement(loadcase=[lc]))
    except Exception as e: print("disp fail",lc,str(e)[:80]); continue
    per={}
    for z,nm in LEV:
        vals=[abs(float(x[comp])) for x in d if str(x.get("Node","")).isdigit() and abs(N[str(x["Node"])]["Z"]-z)<1e-4]
        per[nm]=max(vals) if vals else 0.0
    D[lc]=dict(comp=comp,per=per,max=max(abs(float(x[comp])) for x in d if str(x.get("Node","")).isdigit()))
    print("  disp",lc,comp,{k:round(v*1000,2) for k,v in per.items()},"max",round(D[lc]["max"]*1000,2),"mm")
out["disp"]=D
json.dump(out,open(SC+"/B_data.json","w"),indent=1,default=str)
print("storeys:",json.dumps(ST)[:400]); print("ltom:",out["ltom"]); print("combos:",list(out["lcom"]))
