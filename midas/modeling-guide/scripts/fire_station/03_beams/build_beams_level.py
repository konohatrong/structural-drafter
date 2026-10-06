# -*- coding: utf-8 -*-
# Write one level of beams (nodes, elements, group) to the live MIDAS model.
# usage: python build_beams_level.py <MAPI_KEY> <LEVEL: GB|2F|3F|RF>
import sys, os, json, math
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
KEY,L=sys.argv[1],sys.argv[2]
D=json.load(open(SC+"/fs_beammodel.json"))[L]
GRP={"GB":(8,"BEAM_GB"),"2F":(9,"BEAM_2F"),"3F":(10,"BEAM_3F"),"RF":(11,"BEAM_RF")}
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(KEY)
import midas_gen as mg
def G(ep,key):
    r=mg.MidasAPI("GET",ep,{}).get(key,{}); return r if isinstance(r,dict) else {}
def PUT(ep,body):
    r=mg.MidasAPI("PUT",ep,body); ok=isinstance(r,dict) and "error" not in r and "message" not in r
    print(f"PUT {ep:10} {'OK' if ok else r}"); return ok

z=D["z"]
nodes=G("/db/NODE","NODE"); elem=G("/db/ELEM","ELEM"); sect=G("/db/SECT","SECT")
# ---- pre-checks ----
newn={int(k):v for k,v in D["newnodes"].items()}
clash_n=[i for i in newn if str(i) in nodes]; clash_e=[e["id"] for e in D["elems"] if str(e["id"]) in elem]
missing_sect=sorted({e["sect"] for e in D["elems"]}-{int(k) for k in sect})
colref={e["i"] for e in D["elems"]}|{e["j"] for e in D["elems"]}
missing_col=[n for n in colref if n not in newn and str(n) not in nodes]
badz=[n for n in colref if n not in newn and str(n) in nodes and abs(nodes[str(n)]["Z"]-z)>1e-3]
print(f"level {L}  Z=+{z}  new nodes {len(newn)}  beams {len(D['elems'])}")
print(f"pre-check: node-ID clash {clash_n}  elem-ID clash {clash_e}  missing sections {missing_sect}  "
      f"missing column nodes {missing_col}  column nodes at wrong Z {badz}")
if clash_n or clash_e or missing_sect or missing_col or badz: sys.exit("ABORT: pre-check failed")

# ---- write ----
PUT("/db/NODE",{"Assign":{str(i):{"X":x,"Y":y,"Z":z} for i,(x,y) in newn.items()}})
PUT("/db/ELEM",{"Assign":{str(e["id"]):{"TYPE":"BEAM","MATL":1,"SECT":e["sect"],"NODE":[e["i"],e["j"]],
                                        "ANGLE":0,"STYPE":0} for e in D["elems"]}})
gid,gname=GRP[L]
PUT("/db/GRUP",{"Assign":{str(gid):{"NAME":gname,"P_TYPE":0,"N_LIST":sorted(newn),"E_LIST":sorted(e["id"] for e in D["elems"])}}})

# ---- verify ----
nodes=G("/db/NODE","NODE"); elem=G("/db/ELEM","ELEM"); grup=G("/db/GRUP","GRUP")
ids=[str(e["id"]) for e in D["elems"]]
got=[elem[i] for i in ids if i in elem]
lens=[]
for e in D["elems"]:
    m=elem.get(str(e["id"]))
    if not m: continue
    a,b=nodes[str(m["NODE"][0])],nodes[str(m["NODE"][1])]
    lens.append(abs(math.dist((a["X"],a["Y"],a["Z"]),(b["X"],b["Y"],b["Z"]))-e["len"]))
print(f"\nVERIFY  beams written {len(got)}/{len(ids)}  by section {dict(sorted(Counter(m['SECT'] for m in got).items()))}  "
      f"max length mismatch {max(lens)*1000:.1f} mm")
print(f"        new nodes present {sum(1 for i in newn if str(i) in nodes)}/{len(newn)}  "
      f"all beam nodes at Z={z}: {all(abs(nodes[str(n)]['Z']-z)<1e-6 for m in got for n in m['NODE'][:2])}")
print(f"        model totals: nodes {len(nodes)}  elements {len(elem)}  group '{gname}' "
      f"{len(grup.get(str(gid),{}).get('E_LIST',[]))} elems / {len(grup.get(str(gid),{}).get('N_LIST',[]))} nodes")
