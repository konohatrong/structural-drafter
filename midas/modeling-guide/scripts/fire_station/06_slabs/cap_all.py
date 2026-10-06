import sys, os, json, base64
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
r=mg.MidasAPI("POST","/view/CAPTURE",{"Argument":{"SET_MODE":"pre","SET_HIDDEN":True,"HEIGHT":1100,"WIDTH":1700,
     "ANGLE":{"HORIZONTAL":-55,"VERTICAL":22},"ACTIVE":{"ACTIVE_MODE":"All"}}})
open(SC+"/mid_model_iso.png","wb").write(base64.b64decode(r["base64String"])); print("saved iso")
N=mg.MidasAPI("GET","/db/NODE",{})["NODE"]; E=mg.MidasAPI("GET","/db/ELEM",{})["ELEM"]; G=mg.MidasAPI("GET","/db/GRUP",{})["GRUP"]
print("model: nodes",len(N),"elements",len(E),dict(Counter(e["TYPE"] for e in E.values())))
print("plates by thickness:",dict(Counter(e["SECT"] for e in E.values() if e["TYPE"]=="PLATE")))
for k in ("13","14","15","16","17"): print("  ",G[k]["NAME"],len(G[k]["E_LIST"]))
