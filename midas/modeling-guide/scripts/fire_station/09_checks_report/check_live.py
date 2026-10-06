import sys, os, json
from collections import defaultdict, Counter
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
g=lambda ep,k:(lambda r:r.get(k,{}) if isinstance(r,dict) else {})(mg.MidasAPI("GET",ep,{}))
N=g("/db/NODE","NODE"); E=g("/db/ELEM","ELEM"); P=g("/db/PRES","PRES")
print("counts: nodes",len(N),"elems",len(E),dict(Counter(v["TYPE"] for v in E.values())),"sections",len(g("/db/SECT","SECT")),"groups",len(g("/db/GRUP","GRUP")),"members",len(g("/db/MEMB","MEMB")),"thik",len(g("/db/THIK","THIK")))
tot=defaultdict(float)
for e,v in P.items():
    el=E.get(e)
    if not el: continue
    Q=[(N[str(n)]["X"],N[str(n)]["Y"]) for n in el["NODE"] if n]; a=abs(sum(Q[i-1][0]*Q[i][1]-Q[i][0]*Q[i-1][1] for i in range(len(Q))))/2
    for it in v["ITEMS"]: tot[it["LCNAME"]]+=-it["FORCES"][0]*a
print("pressure totals kN:",{k:round(v,1) for k,v in tot.items()},"(expected LL 3776.5, SDL 2815.8)")
print("load cases:",[v["NAME"] for v in g("/db/STLD","STLD").values()], " self-weight:",g("/db/BODF","BODF"))
print("design code:",g("/db/DCON","DCON"))
m=g("/db/MATD","MATD").get("1",{}); print("concrete/rebar:",m.get("DATA1",{}).get("CODEMATLNAME"),m.get("REBAR_CODENAME"),m.get("MAINREBAR_REBARNAME"),m.get("MAINREBAR_B_FY"),m.get("SUBREBAR_B_FY"))
lg=g("/db/LCOM-GEN","LCOM-GEN"); lc=g("/db/LCOM-CONC","LCOM-CONC")
print("combos GEN:",len(lg),[v["NAME"] for v in lg.values()]); print("combos CONC:",len(lc),[v["NAME"] for v in lc.values()])
print("structure type:",g("/db/STYP","STYP")); print("loads->mass:",g("/db/ltom","LTOM"))
try:
    df=mg.Result.TABLE.Reaction(loadcase=["DL(ST)"]); print("analysis results: PRESENT")
except Exception as ex: print("analysis results:",str(ex)[:100])
exp=os.path.join(SC,"fs_export_check2.mct"); mg.MidasAPI("POST","/doc/EXPORTMXT",{"Argument":exp})
t=open(exp,encoding="utf-8",errors="replace").read().splitlines(); keep=None; rb=Counter()
for l in t:
    if l.startswith("*"): keep=l.split()[0] if l.startswith(("*REBAR-BEAM","*REBAR-COLUMN")) else None; continue
    if keep and l.strip() and not l.startswith(";") and not l.startswith("       "): rb[keep]+=1; print("  ",keep,l.split(",")[0].strip(),"|",l.strip()[:110])
print("rebar sections:",dict(rb))
