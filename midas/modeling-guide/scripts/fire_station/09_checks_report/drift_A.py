import sys, os, json, math
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
N=mg.MidasAPI("GET","/db/NODE",{})["NODE"]; E=mg.MidasAPI("GET","/db/ELEM",{})["ELEM"]
LEV=[-1.5,0.3,3.8,7.5,10.7,13.7]; NAMES=["Base","2F (GF slab)","3F","4F","5F","Roof"]
colnodes=set()
for v in E.values():
    if v["TYPE"]!="BEAM": continue
    a,b=v["NODE"][:2]; A,B=N[str(a)],N[str(b)]
    if abs(A["Z"]-B["Z"])>0.01 and math.hypot(A["X"]-B["X"],A["Y"]-B["Y"])<1e-3: colnodes|={a,b}
at={}
for n in colnodes:
    p=N[str(n)]
    for i,z in enumerate(LEV):
        if abs(p["Z"]-z)<1e-3: at[(round(p["X"],3),round(p["Y"],3),i)]=n
rows=lambda df:[dict(zip(df.columns,r)) for r in df.rows()]
out={}
for lc,comp in (("EQX(ST)","DX"),("EQY(ST)","DY")):
    d={int(x["Node"]):float(x[comp]) for x in rows(mg.Result.TABLE.Displacement(loadcase=[lc])) if str(x.get("Node","")).isdigit()}
    per={}
    for (x,y,i),n in at.items():
        # nearest lower storey on the same column line
        lower=[j for j in range(i) if (x,y,j) in at]
        if not lower: continue
        j=max(lower); m=at[(x,y,j)]; h=LEV[i]-LEV[j]; r=abs(d[n]-d[m])/h; k=f"{NAMES[j]} -> {NAMES[i]}"
        if r>per.get(k,{}).get("ratio",0): per[k]=dict(ratio=r,dmm=abs(d[n]-d[m])*1000,h=h,x=x,y=y)
    out[lc]=per
    for k,v in per.items(): print(f"{lc} {k:22} {v['dmm']:6.2f} mm / {v['h']:.2f} m = {100*v['ratio']:.3f} %  (col {v['x']},{v['y']})")
A=json.load(open(SC+"/A_data.json")); A["drift"]=out; json.dump(A,open(SC+"/A_data.json","w"),indent=1,default=str)
