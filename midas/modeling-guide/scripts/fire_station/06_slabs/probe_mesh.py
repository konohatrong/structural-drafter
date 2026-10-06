import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
n0=len(mg.MidasAPI("GET","/db/NODE",{}).get("NODE",{})); e0=len(mg.MidasAPI("GET","/db/ELEM",{}).get("ELEM",{}))
for ep in ("/db/THIK","/db/MADO","/db/SBDO","/db/DOEL","/db/UNIT"):
    r=mg.MidasAPI("GET",ep,{}); print(ep,"->",json.dumps(r)[:300])
# harmless probe: target an element ID that does not exist
r=mg.MidasAPI("POST","/ope/AUTOMESH",{"Argument":{"MESHER":{"METHOD":"Line Elements","TARGETS":[999991,999992,999993]},
  "MESH_SIZE":{"LENGTH":0.5},"PROPERTY":{"ELEMENT_TYPE":"Plate","MATERIAL":1,"THICKNESS":1},"DOMAIN_NAME":{"NAME":"PROBE"}}})
print("/ope/AUTOMESH probe ->",json.dumps(r)[:400])
n1=len(mg.MidasAPI("GET","/db/NODE",{}).get("NODE",{})); e1=len(mg.MidasAPI("GET","/db/ELEM",{}).get("ELEM",{}))
print(f"model unchanged: nodes {n0}->{n1}  elems {e0}->{e1}")
