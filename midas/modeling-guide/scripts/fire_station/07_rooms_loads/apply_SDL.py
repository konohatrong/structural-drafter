# -*- coding: utf-8 -*-
# Apply SDL 2.50 kN/m2 (global -Z) to every slab plate; keep the existing LL item (ID 1), SDL = item ID 2.
# usage: python apply_SDL.py <MAPI_KEY>
import sys, os, json
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
Q=2.50
R=json.load(open(SC+"/fs_rooms.json",encoding="utf-8"))
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
G=lambda ep,k:(lambda r:r.get(k,{}) if isinstance(r,dict) else {})(mg.MidasAPI("GET",ep,{}))
N=G("/db/NODE","NODE"); E=G("/db/ELEM","ELEM"); ST=G("/db/STLD","STLD"); PR=G("/db/PRES","PRES")
assert any(v["NAME"]=="SDL" for v in ST.values()), "load case SDL missing"
json.dump(PR,open(SC+"/pres_backup_before_SDL.json","w"))
plates=sorted(int(k) for k,v in E.items() if v["TYPE"]=="PLATE")
already=[e for e in plates if any(i["LCNAME"]=="SDL" for i in PR.get(str(e),{}).get("ITEMS",[]))]
if already: sys.exit(f"STOP: {len(already)} plates already carry SDL")
body={}
for e in plates:
    ll=[i for i in PR.get(str(e),{}).get("ITEMS",[]) if i["LCNAME"]=="LL"]
    body[str(e)]={"ITEMS":ll+[{"ID":2,"LCNAME":"SDL","GROUP_NAME":"","CMD":"PRES","ELEM_TYPE":"PLATE","FACE_EDGE_TYPE":"FACE",
                               "DIRECTION":"GZ","VECTORS":[0,0,1],"FORCES":[-Q,0,0,0,0]}]}
keys=list(body)
for i in range(0,len(keys),800):
    r=mg.MidasAPI("PUT","/db/PRES",{"Assign":{k:body[k] for k in keys[i:i+800]}})
    print(f"batch {i//800+1}: {len(keys[i:i+800])} plates {'OK' if isinstance(r,dict) and 'PRES' in r else json.dumps(r)[:200]}")
# ---- verify ----
PR2=G("/db/PRES","PRES")
def area(e):
    P=[(N[str(n)]["X"],N[str(n)]["Y"]) for n in E[str(e)]["NODE"] if n]
    return abs(sum(P[i-1][0]*P[i][1]-P[i][0]*P[i-1][1] for i in range(len(P))))/2
lvl={};
for e,z in R["plates"].items(): lvl[int(e)]=R["zones"][z]["level"]
res=defaultdict(float); resLL=0; bad=[]
for e in plates:
    it=PR2.get(str(e),{}).get("ITEMS",[]); byc={i["LCNAME"]:i for i in it}
    old=[i for i in PR.get(str(e),{}).get("ITEMS",[]) if i["LCNAME"]=="LL"][0]
    if len(it)!=2 or "SDL" not in byc or "LL" not in byc or abs(byc["SDL"]["FORCES"][0]+Q)>1e-9 or byc["LL"]["FORCES"]!=old["FORCES"]: bad.append(e); continue
    a=area(e); res[lvl[e]]+=a*Q; resLL+=-byc["LL"]["FORCES"][0]*a
print(f"\nVERIFY: plates {len(plates)}  with exactly LL + SDL (LL unchanged): {len(plates)-len(bad)}   problems {len(bad)} {bad[:10]}")
for L in ("GB","2F","3F","RF","AR"): print(f"   {L}: SDL resultant {res[L]:8.1f} kN")
print(f"   TOTAL SDL {sum(res.values()):.1f} kN  (= {sum(res.values())/9.80665:.1f} t)   |  LL still {resLL:.1f} kN")
