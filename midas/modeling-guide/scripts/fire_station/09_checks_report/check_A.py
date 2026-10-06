import sys, os, json
from collections import defaultdict, Counter
sys.stdout.reconfigure(encoding="utf-8")
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
g=lambda ep,k:(lambda r:r.get(k,{}) if isinstance(r,dict) else {})(mg.MidasAPI("GET",ep,{}))
N=g("/db/NODE","NODE"); E=g("/db/ELEM","ELEM"); P=g("/db/PRES","PRES"); S=g("/db/SECT","SECT")
print("counts: nodes",len(N),"elems",len(E),dict(Counter(v["TYPE"] for v in E.values())),"sections",len(S),"groups",len(g("/db/GRUP","GRUP")),"thik",g("/db/THIK","THIK"))
print("sections:",{k:v["SECT_NAME"] for k,v in S.items()})
print("load cases:",[(v["NAME"],v["TYPE"]) for v in g("/db/STLD","STLD").values()])
pv=defaultdict(Counter)
for e,v in P.items():
    for it in v["ITEMS"]: pv[it["LCNAME"]][round(it["FORCES"][0],3)]+=1
print("pressure values by case:",{k:dict(c) for k,c in pv.items()})
print("floor loads:",json.dumps(g("/db/FBLA","FBLA"))[:300]," beam loads:",len(g("/db/BMLD","BMLD")))
print("design code:",g("/db/DCON","DCON")); m=g("/db/MATD","MATD"); print("MATD:",{k:(v.get("NAME"),v.get("REBAR_CODENAME"),v.get("MAINREBAR_REBARNAME"),v.get("MAINREBAR_B_FY")) for k,v in m.items()})
print("MATL:",{k:v.get("NAME") for k,v in g("/db/MATL","MATL").items()})
lg=g("/db/LCOM-GEN","LCOM-GEN"); lc=g("/db/LCOM-CONC","LCOM-CONC")
print("combos GEN:",len(lg),[(v["NAME"],[(c["LCNAME"],c["FACTOR"]) for c in v["vCOMB"]]) for v in lg.values()][:30])
print("combos CONC:",len(lc),[v["NAME"] for v in lc.values()])
print("stories:",[(v["STORY_NAME"],v["STORY_LEVEL"]) for v in g("/db/STOR","STOR").values()])
print("ltom:",g("/db/ltom","LTOM")); print("supports:",len(g("/db/CONS","CONS")))
try: mg.Result.TABLE.Reaction(loadcase=["DL(ST)"]); print("analysis results: PRESENT")
except Exception as ex: print("analysis results:",str(ex)[:100])
