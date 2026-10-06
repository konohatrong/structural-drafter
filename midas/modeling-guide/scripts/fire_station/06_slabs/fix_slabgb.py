import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
G=lambda:mg.MidasAPI("GET","/db/GRUP",{})["GRUP"]
g=G(); el=mg.MidasAPI("GET","/db/ELEM",{})["ELEM"]
json.dump(g,open(SC+"/grup_backup_before_fix.json","w"))
old=set(g["13"]["E_LIST"]); plates=sorted(e for e in old if el[str(e)]["TYPE"]=="PLATE"); beams=old-set(plates)
bg=set(g["8"]["E_LIST"]); print("beam pieces in SLAB_GB:",len(beams)," of them also in BEAM_GB:",len(beams&bg))
n0=len(g); r=mg.MidasAPI("DELETE","/db/GRUP/13",{}); g=G()
print("delete group 13:",n0,"->",len(g),"groups","OK" if len(g)==n0-1 and "13" not in g else f"UNEXPECTED {r}")
if len(g)!=n0-1: sys.exit("STOP")
mg.MidasAPI("PUT","/db/GRUP",{"Assign":{"13":{"NAME":"SLAB_GB","P_TYPE":0,"N_LIST":[],"E_LIST":plates}}}); g=G()
pan=set().union(*[set(g[str(k)]["E_LIST"]) for k in range(101,120)])
print("SLAB_GB now",len(g["13"]["E_LIST"]),"all plates:",all(el[str(e)]["TYPE"]=="PLATE" for e in g["13"]["E_LIST"]),
      "| equals union of panel groups:",set(g["13"]["E_LIST"])==pan,"| groups total",len(g))
