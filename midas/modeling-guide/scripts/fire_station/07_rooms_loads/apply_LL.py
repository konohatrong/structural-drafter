# -*- coding: utf-8 -*-
# Apply live load as plate pressure (load case LL, global -Z) zone by zone from fs_rooms.json + fs_LL.json.
# usage: python apply_LL.py <MAPI_KEY>
import sys, os, json
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
R=json.load(open(SC+"/fs_rooms.json",encoding="utf-8")); LL=json.load(open(SC+"/fs_LL.json",encoding="utf-8"))
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
G=lambda ep,k:(lambda r:r.get(k,{}) if isinstance(r,dict) else {})(mg.MidasAPI("GET",ep,{}))
N=G("/db/NODE","NODE"); E=G("/db/ELEM","ELEM"); ST=G("/db/STLD","STLD"); PR=G("/db/PRES","PRES")
# ---- pre-checks ----
assert any(v["NAME"]=="LL" for v in ST.values()), "load case LL missing"
if PR: sys.exit(f"STOP: /db/PRES already has {len(PR)} elements loaded - review before re-applying")
missing=[e for e in R["plates"] if E.get(str(e),{}).get("TYPE")!="PLATE"]
if missing: sys.exit(f"STOP: {len(missing)} mapped plates not found in the model")
allpl={k for k,v in E.items() if v["TYPE"]=="PLATE"}; unm=allpl-set(R["plates"])
print(f"plates in model {len(allpl)}  mapped {len(R['plates'])}  unmapped {len(unm)}")
if unm: sys.exit("STOP: unmapped plates")
kpa={z:round(v["LL"]*9.80665/1000,4) for z,v in LL.items()}
def area(e):
    P=[(N[str(n)]["X"],N[str(n)]["Y"]) for n in E[str(e)]["NODE"] if n]
    return abs(sum(P[i-1][0]*P[i][1]-P[i][0]*P[i-1][1] for i in range(len(P))))/2
# ---- write in batches ----
items={str(e):{"ITEMS":[{"ID":1,"LCNAME":"LL","GROUP_NAME":"","CMD":"PRES","ELEM_TYPE":"PLATE","FACE_EDGE_TYPE":"FACE",
                          "DIRECTION":"GZ","VECTORS":[0,0,1],"FORCES":[-kpa[z],0,0,0,0]}]} for e,z in R["plates"].items()}
keys=list(items); ok=0
for i in range(0,len(keys),800):
    r=mg.MidasAPI("PUT","/db/PRES",{"Assign":{k:items[k] for k in keys[i:i+800]}})
    good=isinstance(r,dict) and "PRES" in r; ok+=good
    print(f"batch {i//800+1}: {len(keys[i:i+800])} plates {'OK' if good else json.dumps(r)[:200]}")
# ---- verify from the model ----
PR=G("/db/PRES","PRES"); byz=defaultdict(lambda:[0,0.0,set()]); bad=[]
for e,z in R["plates"].items():
    it=PR.get(str(e),{}).get("ITEMS",[])
    if len(it)!=1 or it[0]["LCNAME"]!="LL" or it[0]["DIRECTION"]!="GZ" or abs(it[0]["FORCES"][0]+kpa[z])>1e-6: bad.append(e); continue
    a=area(e); byz[z][0]+=1; byz[z][1]+=a*kpa[z]; byz[z][2].add(round(it[0]["FORCES"][0],4))
print(f"\nVERIFY: plates with LL pressure {len(PR)} / {len(R['plates'])}   wrong or missing {len(bad)}")
tot=0
for z in R["zones"]:
    n,f,vals=byz[z]; tot+=f
    print(f"   {z:13} {n:4d} plates  q = {kpa[z]:5.2f} kN/m²  area {R['zones'][z]['area']:7.2f} m²  resultant {f:8.1f} kN")
print(f"   TOTAL LL resultant {tot:.1f} kN  (= {tot/9.80665:.1f} t)")
