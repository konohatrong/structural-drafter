# delete one panel's plates (and the nodes only they used) so it can be re-meshed
import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
KEY,L,PN=sys.argv[1],sys.argv[2],sys.argv[3]
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(KEY)
import midas_gen as mg
G=lambda ep,k:mg.MidasAPI("GET",ep,{}).get(k,{})
N=G("/db/NODE","NODE"); E=G("/db/ELEM","ELEM"); GR=G("/db/GRUP","GRUP")
json.dump({"NODE":N,"ELEM":E,"GRUP":GR},open(SC+f"/midas_backup_before_redo_{PN}.json","w"))
D=json.load(open(SC+f"/fs_slab_{L}_done.json"))
pl=[e for e in D[PN] if E.get(str(e),{}).get("TYPE")=="PLATE"]
cand={n for e in pl for n in E[str(e)]["NODE"] if n}
others={n for k,e in E.items() if int(k) not in set(pl) for n in e["NODE"] if n}
orphan=sorted(cand-others)
n0,e0=len(N),len(E)
mg.MidasAPI("DELETE","/db/ELEM/"+",".join(map(str,pl)),{}); e1=len(G("/db/ELEM","ELEM"))
print(f"plates deleted {len(pl)}: elements {e0} -> {e1}", "OK" if e0-e1==len(pl) else "UNEXPECTED")
if e0-e1!=len(pl): sys.exit("STOP")
if orphan:
    mg.MidasAPI("DELETE","/db/NODE/"+",".join(map(str,orphan)),{}); n1=len(G("/db/NODE","NODE"))
    print(f"orphan nodes deleted {len(orphan)}: nodes {n0} -> {n1}", "OK" if n0-n1==len(orphan) else "UNEXPECTED")
GR=G("/db/GRUP","GRUP"); left={k:len(set(g.get("E_LIST",[]))&set(pl)) for k,g in GR.items()}
print("deleted plates still listed in groups:",{GR[k]["NAME"]:v for k,v in left.items() if v})
del D[PN]; json.dump(D,open(SC+f"/fs_slab_{L}_done.json","w")); print(PN,"removed from log")
