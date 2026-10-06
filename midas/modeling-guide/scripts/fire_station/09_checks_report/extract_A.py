# -*- coding: utf-8 -*-
# Building A (office): report data from the live model (read-only).
import sys, os, json, math
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
G=lambda ep,k:(lambda r:r.get(k,{}) if isinstance(r,dict) else {})(mg.MidasAPI("GET",ep,{}))
def rows(df): return [dict(zip(df.columns,r)) for r in df.rows()]
N=G("/db/NODE","NODE"); E=G("/db/ELEM","ELEM"); S=G("/db/SECT","SECT"); P=G("/db/PRES","PRES")
LEV=[-1.5,0.3,3.8,7.5,10.7,13.7]; NAMES=["Base","2F (GF slab)","3F","4F","5F","Roof"]
out={"counts":dict(nodes=len(N),elems=len(E),beam=sum(1 for v in E.values() if v["TYPE"]=="BEAM"),plate=sum(1 for v in E.values() if v["TYPE"]=="PLATE")),
     "sect":{k:(v["SECT_NAME"],v["SECT_BEFORE"]["SECT_I"]["vSIZE"][:2]) for k,v in S.items()},"stor":G("/db/STOR","STOR"),
     "lcom_conc":{v["NAME"]:(v.get("DESC",""),[(c["LCNAME"],c["FACTOR"],c.get("ANAL","ST")) for c in v["vCOMB"]]) for v in G("/db/LCOM-CONC","LCOM-CONC").values()},
     "dcon":G("/db/DCON","DCON"),"ltom":G("/db/ltom","LTOM")}
for k,(d,c) in out["lcom_conc"].items(): print(f"  {k:7} {d:30} " + " + ".join(f"{f:g}{n}" for n,f,a in c))
# slab loads by level and value
def lev(z): return min(range(len(LEV)),key=lambda i:abs(LEV[i]-z))
pa=defaultdict(float)
for e,v in P.items():
    el=E.get(e); ns=[n for n in el["NODE"] if n]; Q=[(N[str(n)]["X"],N[str(n)]["Y"]) for n in ns]
    a=abs(sum(Q[i-1][0]*Q[i][1]-Q[i][0]*Q[i-1][1] for i in range(len(Q))))/2; L=NAMES[lev(N[str(ns[0])]["Z"])]
    for it in v["ITEMS"]: pa[(L,it["LCNAME"],-it["FORCES"][0])]+=a
out["slabload"]=[[k[0],k[1],k[2],round(a,1)] for k,a in sorted(pa.items())]
for r in out["slabload"]: print("  slab load",r)
R={}
for lc in ["DL(ST)","SDL(ST)","LL(ST)","EQX(ST)","EQY(ST)"]:
    r=[x for x in rows(mg.Result.TABLE.Reaction(loadcase=[lc])) if str(x.get("Node","")).isdigit()]
    R[lc]=r; print(f"  {lc:8} rows {len(r)} FX {sum(float(x['FX']) for x in r):9.1f} FY {sum(float(x['FY']) for x in r):9.1f} FZ {sum(float(x['FZ']) for x in r):10.1f}")
out["react"]=R; out["sup"]={int(x["Node"]):(N[str(x['Node'])]["X"],N[str(x['Node'])]["Y"],N[str(x['Node'])]["Z"]) for x in R["DL(ST)"]}
D={}
for lc,comp in (("EQX(ST)","DX"),("EQY(ST)","DY"),("DL(ST)","DZ"),("SDL(ST)","DZ"),("LL(ST)","DZ")):
    d={int(x["Node"]):float(x[comp]) for x in rows(mg.Result.TABLE.Displacement(loadcase=[lc])) if str(x.get("Node","")).isdigit()}
    D[lc]=d
svc={n:D["DL(ST)"][n]+D["SDL(ST)"][n]+D["LL(ST)"][n] for n in D["DL(ST)"]}
out["disp"]={"EQX":max(abs(v) for v in D["EQX(ST)"].values()),"EQY":max(abs(v) for v in D["EQY(ST)"].values()),"SVC_DZ":max(abs(v) for v in svc.values()),
             "EQX_roof":max(abs(D["EQX(ST)"][int(n)]) for n,v in N.items() if abs(v["Z"]-13.7)<1e-3),"EQY_roof":max(abs(D["EQY(ST)"][int(n)]) for n,v in N.items() if abs(v["Z"]-13.7)<1e-3)}
print("  disp",{k:round(v*1000,2) for k,v in out["disp"].items()})
# drift by column line
cols=[]
for eid,v in E.items():
    if v["TYPE"]!="BEAM": continue
    a,b=v["NODE"][:2]; A,Bn=N[str(a)],N[str(b)]
    if abs(A["Z"]-Bn["Z"])>0.01 and math.hypot(A["X"]-Bn["X"],A["Y"]-Bn["Y"])<1e-3: cols.append((a,b) if A["Z"]<Bn["Z"] else (b,a))
dr={}
for lc in ("EQX(ST)","EQY(ST)"):
    per={}
    for lo,hi in cols:
        zl,zh=N[str(lo)]["Z"],N[str(hi)]["Z"]; key=(lev(zl),lev(zh))
        if key[0]==key[1]: continue
        # accumulate over storey: use nodes at storey levels only
        dd=abs(D[lc][hi]-D[lc][lo]); h=zh-zl; r=dd/h
        if r>per.get(key,(0,))[0]: per[key]=(r,dd*1000,h)
    dr[lc]={f"{NAMES[k[0]]} -> {NAMES[k[1]]}":dict(ratio=v[0],dmm=v[1],h=v[2]) for k,v in sorted(per.items())}
    for k,v in dr[lc].items(): print(f"  drift {lc} {k}: {v['dmm']:.2f} mm / {v['h']:.2f} = {100*v['ratio']:.3f}%")
out["drift"]=dr
json.dump(out,open(SC+"/A_data.json","w"),indent=1,default=str); print("saved A_data.json")
