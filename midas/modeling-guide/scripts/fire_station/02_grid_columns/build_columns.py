# -*- coding: utf-8 -*-
import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
M=json.load(open(SC+"/fs_colmodel.json"))
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator")
sys.path.insert(0,"src")
from windload.midas.connection import connect
connect(sys.argv[1])
import midas_gen as mg
def PUT(ep,body):
    r=mg.MidasAPI("PUT",ep,body)
    ok=isinstance(r,dict) and "error" not in r and "message" not in r
    print(f"PUT {ep:10} {'OK' if ok else r}")
    return r

# 1) material
PUT("/db/MATL",{"Assign":{"1":{"TYPE":"CONC","NAME":"C280","DAMP_RAT":0.05,
    "PARAM":[{"P_TYPE":1,"STANDARD":"TIS(RC)","CODE":"","DB":"C280"}]}}})
# 2) nodes
PUT("/db/NODE",{"Assign":{k:{"X":v["X"],"Y":v["Y"],"Z":v["Z"]} for k,v in M["nodes"].items()}})
# 3) elements
PUT("/db/ELEM",{"Assign":{k:{"TYPE":"BEAM","MATL":1,"SECT":v["sect"],"NODE":[v["i"],v["j"]],
    "ANGLE":0,"STYPE":0} for k,v in M["elems"].items()}})
# 4) fixed supports at base
base=[int(k) for k,v in M["nodes"].items() if v["lev"]=="BASE"]
PUT("/db/CONS",{"Assign":{str(n):{"ITEMS":[{"ID":1,"CONSTRAINT":"1111111","GROUP_NAME":""}]} for n in base}})
# 5) structure groups
E=M["elems"]
def el(cond): return sorted(int(k) for k,v in E.items() if cond(v))
groups={
 "COL_C1":      ([],el(lambda v:v["mark"]=="C1")),
 "COL_C2":      ([],el(lambda v:v["mark"]=="C2")),
 "COL_FT_STUB": ([],el(lambda v:v["seg"]=="BASE->GF")),
 "COL_GF-2F":   ([],el(lambda v:v["seg"]=="GF->2F")),
 "COL_2F-3F":   ([],el(lambda v:v["seg"]=="2F->3F")),
 "COL_3F-RF":   ([],el(lambda v:v["seg"]=="3F->RF")),
 "NODE_BASE":   (sorted(base),[]),
}
PUT("/db/GRUP",{"Assign":{str(i):{"NAME":n,"P_TYPE":0,"N_LIST":nl,"E_LIST":elst}
                           for i,(n,(nl,elst)) in enumerate(groups.items(),1)}})

# ---- verify ----
def G(ep,key):
    r=mg.MidasAPI("GET",ep,{}).get(key,{}); return r if isinstance(r,dict) else {}
nodes=G("/db/NODE","NODE"); elem=G("/db/ELEM","ELEM"); cons=G("/db/CONS","CONS")
matl=G("/db/MATL","MATL"); grup=G("/db/GRUP","GRUP")
print(f"\nVERIFY nodes={len(nodes)} elements={len(elem)} supports={len(cons)} materials={len(matl)} groups={len(grup)}")
from collections import Counter
print("elements by section:",dict(sorted(Counter(v["SECT"] for v in elem.values()).items())))
print("elements by material:",dict(Counter(v["MATL"] for v in elem.values())))
zs=Counter(round(v["Z"],2) for v in nodes.values()); print("nodes by Z:",dict(sorted(zs.items())))
print("material 1:",matl.get("1",{}).get("NAME"),matl.get("1",{}).get("PARAM"))
for k,v in grup.items(): print(f"  group {k}: {v['NAME']:12} nodes={len(v.get('N_LIST',[]))} elems={len(v.get('E_LIST',[]))}")
