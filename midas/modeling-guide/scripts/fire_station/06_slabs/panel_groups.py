# -*- coding: utf-8 -*-
# One structure group per slab panel: SLAB_<L>-Pxx (plates only). IDs: level base + panel no. (GB 101.., 2F 201.., 3F 301.., RF 401.., AR 501..)
# usage: python panel_groups.py <MAPI_KEY> <LEVEL>
import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
KEY,L=sys.argv[1],sys.argv[2]; BASE={"GB":100,"2F":200,"3F":300,"RF":400,"AR":500}[L]
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(KEY)
import midas_gen as mg
G=lambda ep,k:mg.MidasAPI("GET",ep,{}).get(k,{})
el=G("/db/ELEM","ELEM"); grup=G("/db/GRUP","GRUP")
done=json.load(open(SC+f"/fs_slab_{L}_done.json"))
upd={}
for name,ids in sorted(done.items()):
    gid=str(BASE+int(name.split("-P")[1])); pl=sorted(e for e in ids if el.get(str(e),{}).get("TYPE")=="PLATE")
    if gid in grup and grup[gid]["NAME"]!=f"SLAB_{name}": sys.exit(f"STOP: group id {gid} already used by {grup[gid]['NAME']}")
    upd[gid]={"NAME":f"SLAB_{name}","P_TYPE":0,"N_LIST":[],"E_LIST":pl}
mg.MidasAPI("PUT","/db/GRUP",{"Assign":upd})
grup=G("/db/GRUP","GRUP")
ok=all(grup.get(k,{}).get("E_LIST")==v["E_LIST"] and grup[k]["NAME"]==v["NAME"] for k,v in upd.items())
lvl={"GB":"13"}.get(L); tot=sum(len(v["E_LIST"]) for v in upd.values())
allp=set().union(*[set(v["E_LIST"]) for v in upd.values()])
print(f"panel groups written {len(upd)}  all match: {ok}  plates {tot} (distinct {len(allp)})",
      f"| same set as SLAB_{L}: {allp==set(grup.get(lvl,{}).get('E_LIST',[]))}" if lvl else "")
for k in sorted(upd,key=int): print(f"   {k} {grup[k]['NAME']:14} {len(grup[k]['E_LIST']):4} plates")
