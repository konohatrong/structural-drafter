import sys, os, json, difflib
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
g=lambda ep,k:mg.MidasAPI("GET",ep,{}).get(k,{})
N=g("/db/NODE","NODE"); E=g("/db/ELEM","ELEM"); P=g("/db/PRES","PRES")
s=dict(nodes=len(N),elems=len(E),sects=len(g("/db/SECT","SECT")),groups=len(g("/db/GRUP","GRUP")),
       pres_items=sum(len(v["ITEMS"]) for v in P.values()),stld=len(g("/db/STLD","STLD")),dcon=g("/db/DCON","DCON"),memb=len(g("/db/MEMB","MEMB")),thik=len(g("/db/THIK","THIK")))
exp={'nodes': 5120, 'elems': 6368, 'sects': 15, 'groups': 94, 'pres_items': 9550, 'stld': 5, 'dcon': {'1': {'DGNCODE': 'ACI318M-19'}}, 'memb': 196,'thik':4}
print("counts:",s); print("match pre-import snapshot:",s==exp)
# load totals
tot=defaultdict(float)
for e,v in P.items():
    el=E.get(e); 
    if not el: continue
    Q=[(N[str(n)]["X"],N[str(n)]["Y"]) for n in el["NODE"] if n]; a=abs(sum(Q[i-1][0]*Q[i][1]-Q[i][0]*Q[i-1][1] for i in range(len(Q))))/2
    for it in v["ITEMS"]: tot[it["LCNAME"]]+=-it["FORCES"][0]*a
print("pressure totals kN:",{k:round(v,1) for k,v in tot.items()},"  expected LL 3776.5, SDL 2815.8")
m=g("/db/MATD","MATD")["1"]; print("rebar grade:",m["REBAR_CODENAME"],m["MAINREBAR_REBARNAME"],m["MAINREBAR_B_FY"],m["SUBREBAR_B_FY"])
# full text comparison with the backup
out=os.path.join(SC,"fs_export_after_undo.mct"); mg.MidasAPI("POST","/doc/EXPORTMXT",{"Argument":out})
a=[l for l in open(os.path.join(SC,"model_backup_before_rebar.mct"),encoding="utf-8",errors="replace").read().splitlines()]
b=[l for l in open(out,encoding="utf-8",errors="replace").read().splitlines()]
d=[l for l in difflib.unified_diff(a,b,lineterm="",n=0) if not l.startswith(("---","+++","@@"))]
print(f"MCT export vs backup: {len(a)} vs {len(b)} lines, differing lines: {len(d)}")
for l in d[:40]: print("   ",l[:160])
