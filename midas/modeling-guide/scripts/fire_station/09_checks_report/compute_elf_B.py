# -*- coding: utf-8 -*-
# Building B ELF sheet (DPT 1301/1302-61 as input in the model) + storey drift by column line. Read-only.
import sys, os, json, math
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
G=lambda ep,k:(lambda r:r.get(k,{}) if isinstance(r,dict) else {})(mg.MidasAPI("GET",ep,{}))
B=json.load(open(SC+"/B_data.json"))
NODE={int(k):(v["X"],v["Y"],v["Z"]) for k,v in G("/db/NODE","NODE").items()}
ELEM={int(k):v for k,v in G("/db/ELEM","ELEM").items()}
SECT=G("/db/SECT","SECT"); PRES=G("/db/PRES","PRES"); THK={int(k):v["T_IN"] for k,v in G("/db/THIK","THIK").items()}
GAMMA=24.0
LEV=[-1.0,0.35,3.95,4.75,7.95,11.15]; NAMES=["Base","GF","Annex roof","2F","3F","Roof"]
def lev(z): return min(range(len(LEV)),key=lambda i:abs(LEV[i]-z))
def area3(ns):
    P=[NODE[n] for n in ns]; nx=ny=nz=0
    for i in range(len(P)):
        (x1,y1,z1),(x2,y2,z2)=P[i],P[(i+1)%len(P)]; nx+=(y1-y2)*(z1+z2); ny+=(z1-z2)*(x1+x2); nz+=(x1-x2)*(y1+y2)
    return 0.5*math.sqrt(nx*nx+ny*ny+nz*nz)
Ws=[0.0]*6; Wsdl=[0.0]*6; Wll=[0.0]*6
for eid,v in ELEM.items():
    ns=[n for n in v["NODE"] if n]
    if v["TYPE"]=="BEAM":
        a,b=NODE[ns[0]],NODE[ns[1]]; vs=SECT[str(v["SECT"])]["SECT_BEFORE"]["SECT_I"]["vSIZE"]; w=math.dist(a,b)*vs[0]*vs[1]*GAMMA
        if abs(a[2]-b[2])>0.01: Ws[lev(a[2])]+=w/2; Ws[lev(b[2])]+=w/2
        else: Ws[lev(a[2])]+=w
    else:
        A=area3(ns); f=lev(NODE[ns[0]][2]); Ws[f]+=A*THK[v["SECT"]]*GAMMA
        for it in PRES.get(str(eid),{}).get("ITEMS",[]):
            (Wsdl if it["LCNAME"]=="SDL" else Wll)[f]+=abs(it["FORCES"][0])*A
DLm=sum(float(r["FZ"]) for r in B["react"]["DL(ST)"]); sc=DLm/sum(Ws); Ws=[w*sc for w in Ws]
W=[Ws[i]+Wsdl[i]+0.25*Wll[i] for i in range(6)]
lv=range(1,6)                                  # seismic weight above the base (support) level
Wt=sum(W[i] for i in lv); hx=[LEV[i]-LEV[0] for i in range(6)]
Vanal=abs(sum(float(r["FX"]) for r in B["react"]["Ex(ST)"]))
SDS,SD1,R,Hb=0.60,0.36,5.0,LEV[-1]-LEV[0]; T=0.02*Hb; Ts=SD1/SDS; Sa=SDS if T<=Ts else SD1/T
Cs_model=Vanal/Wt; I_impl=Cs_model*R/Sa
I=round(I_impl*4)/4 if abs(I_impl-round(I_impl*4)/4)<0.03 else I_impl
Cs=max(Sa*I/R,0.01); V=Cs*Wt
k=1.0; whk=[W[i]*hx[i]**k for i in lv]; S=sum(whk); Fx=[V*x/S for x in whk]; Vx=[sum(Fx[j:]) for j in range(len(Fx))]
print(f"self-weight scale {sc:.4f} (model DL {DLm:.1f})  SDL {sum(Wsdl):.1f}  LL {sum(Wll):.1f}")
print(f"W above base {Wt:.1f} kN  Vanal {Vanal:.1f}  Cs(model)={Cs_model:.4f}  T={T:.3f} Ts={Ts:.3f} Sa={Sa:.2f}  implied I={I_impl:.3f} -> I={I}  V(code)={V:.1f}")
for j,i in enumerate(lv): print(f"  {NAMES[i]:10} z {LEV[i]:6.2f} hx {hx[i]:6.2f} W {W[i]:8.1f} Fx {Fx[j]:7.1f} Vx {Vx[j]:7.1f}")
# ---- storey drift by column line ----
cols={}
for eid,v in ELEM.items():
    if v["TYPE"]!="BEAM": continue
    a,b=v["NODE"][:2]
    if abs(NODE[a][2]-NODE[b][2])>0.01 and math.hypot(NODE[a][0]-NODE[b][0],NODE[a][1]-NODE[b][1])<1e-3:
        lo,hi=(a,b) if NODE[a][2]<NODE[b][2] else (b,a); cols[eid]=(lo,hi)
drift={}
for lc,comp in (("Ex(ST)","DX"),("Ey(ST)","DY")):
    d={int(r["Node"]):float(r[comp]) for r in [dict(zip(df.columns,x)) for df in [mg.Result.TABLE.Displacement(loadcase=[lc])] for x in df.rows()] if str(r.get("Node","")).isdigit()}
    per=defaultdict(lambda:(0,None))
    for eid,(lo,hi) in cols.items():
        h=NODE[hi][2]-NODE[lo][2]; dd=abs(d[hi]-d[lo]); key=(round(NODE[lo][2],2),round(NODE[hi][2],2))
        if dd/h>per[key][0]: per[key]=(dd/h,dict(elem=eid,dmm=dd*1000,h=h,x=NODE[lo][0],y=NODE[lo][1]))
    drift[lc]={f"{k[0]:+.2f} to {k[1]:+.2f}":dict(ratio=v[0],**v[1]) for k,v in sorted(per.items())}
    for k,v in drift[lc].items(): print(f"  {lc} {k}: {v['dmm']:.2f} mm / {v['h']:.2f} m = {100*v['ratio']:.3f} %  (col at {v['x']:.2f},{v['y']:.2f})")
json.dump(dict(LEV=LEV,NAMES=NAMES,Wself=Ws,Wsdl=Wsdl,Wll=Wll,W=W,Wt=Wt,hx=hx,whk=whk,Fx=Fx,Vx=Vx,V=V,Vanal=Vanal,Cs=Cs,Cs_model=Cs_model,
               I=I,I_impl=I_impl,SDS=SDS,SD1=SD1,R=R,H=Hb,T=T,Ts=Ts,Sa=Sa,k=k,DL=DLm,SDL=sum(Wsdl),LL=sum(Wll),drift=drift),
          open(SC+"/elf_B.json","w"),indent=1)
print("saved elf_B.json")
