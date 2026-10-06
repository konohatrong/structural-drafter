import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
T={"1":("GS1",0.20),"2":("S1",0.18),"3":("S1C",0.18),"4":("RS1",0.18)}
body={"Assign":{k:{"NAME":f"{n} t={int(t*1000)}","TYPE":"VALUE","bINOUT":False,"T_IN":t,"T_OUT":t,"OFFSET":0,"O_VALUE":0} for k,(n,t) in T.items()}}
print("PUT",mg.MidasAPI("PUT","/db/THIK",body).keys())
for k,v in mg.MidasAPI("GET","/db/THIK",{})["THIK"].items(): print(k,v["NAME"],v["T_IN"],"offset",v.get("OFFSET"),v.get("O_VALUE"))
