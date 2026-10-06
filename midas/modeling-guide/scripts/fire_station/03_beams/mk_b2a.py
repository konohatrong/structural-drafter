import sys, os, json, copy
sys.stdout.reconfigure(encoding="utf-8")
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
S=mg.MidasAPI("GET","/db/SECT",{})["SECT"]
if "209" in S: print("209 exists:",S["209"].get("SECT_NAME")); sys.exit()
s=copy.deepcopy(S["207"]); s["SECT_NAME"]="B2A"
print("template 207:",json.dumps(S["207"])[:400])
r=mg.MidasAPI("PUT","/db/SECT",{"Assign":{"209":s}}); print("PUT",r if "error" in str(r) else "OK")
S=mg.MidasAPI("GET","/db/SECT",{})["SECT"]; print("209:",json.dumps(S.get("209"))[:400])
