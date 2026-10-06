import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
G=lambda ep,k:(mg.MidasAPI("GET",ep,{}) or {}).get(k,{})
print("existing STLD:",G("/db/STLD","STLD")," BODF:",G("/db/BODF","BODF"))
m=G("/db/MATL","MATL"); print("material 1:",json.dumps(m.get("1"))[:600])
if G("/db/STLD","STLD"): sys.exit("STLD not empty - stop and review")
r=mg.MidasAPI("PUT","/db/STLD",{"Assign":{
  "1":{"NAME":"DL","TYPE":"D","DESC":"Dead load - self weight"},
  "2":{"NAME":"SDL","TYPE":"D","DESC":"Superimposed dead load"},
  "3":{"NAME":"LL","TYPE":"L","DESC":"Live load"}}}); print("PUT STLD",list(r))
r=mg.MidasAPI("PUT","/db/BODF",{"Assign":{"1":{"LCNAME":"DL","GROUP_NAME":"","FV":[0,0,-1]}}}); print("PUT BODF",list(r))
print("STLD now:",G("/db/STLD","STLD")); print("BODF now:",G("/db/BODF","BODF"))
