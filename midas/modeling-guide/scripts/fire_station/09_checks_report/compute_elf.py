# -*- coding: utf-8 -*-
import sys, os, json, math
sys.stdout.reconfigure(encoding="utf-8")
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator")
sys.path.insert(0,"src")
from windload.midas.connection import connect
connect(sys.argv[1])
import midas_gen as mg
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
def G(ep): return mg.MidasAPI("GET",ep,{})

NODE={int(k):(v["X"],v["Y"],v["Z"]) for k,v in G("/db/NODE").get("NODE",{}).items()}
ELEM={int(k):v for k,v in G("/db/ELEM").get("ELEM",{}).items()}
SECT=G("/db/SECT").get("SECT",{})
PRES=G("/db/pres").get("PRES",{})
GAMMA=24.0    # kN/m3 concrete
TSLAB=0.18    # m

# section area (SB rectangle vSIZE=[H,B])
def sect_area(sid):
    sb=SECT.get(str(sid),{}).get("SECT_BEFORE",{})
    v=sb.get("SECT_I",{}).get("vSIZE",[0,0])
    return (v[0]*v[1]) if len(v)>=2 else 0.0

FLOORS=[0.3,3.8,7.5,10.7,13.7]      # slab/mass levels
ZBASE=-1.5
def nearest_floor(z):
    return min(range(len(FLOORS)), key=lambda i:abs(FLOORS[i]-z))

def poly_area(nids):
    pts=[NODE[n] for n in nids if n]
    if len(pts)<3: return 0.0
    # Newell's area for 3D polygon
    nx=ny=nz=0.0
    m=len(pts)
    for i in range(m):
        x1,y1,z1=pts[i]; x2,y2,z2=pts[(i+1)%m]
        nx+=(y1-y2)*(z1+z2); ny+=(z1-z2)*(x1+x2); nz+=(x1-x2)*(y1+y2)
    return 0.5*math.sqrt(nx*nx+ny*ny+nz*nz)

# story weight accumulators
W_self=[0.0]*5; W_sdl=[0.0]*5; W_ll=[0.0]*5

for eid,v in ELEM.items():
    typ=v.get("TYPE"); nds=[n for n in v.get("NODE",[]) if n]
    if typ=="BEAM" and len(nds)==2:
        a,b=NODE[nds[0]],NODE[nds[1]]
        L=math.dist(a,b); A=sect_area(v.get("SECT"))
        w=L*A*GAMMA
        dz=abs(a[2]-b[2]); dh=math.hypot(a[0]-b[0],a[1]-b[1])
        if dz>dh:   # column -> split to floor at each end
            fa=nearest_floor(a[2]); fb=nearest_floor(b[2])
            W_self[fa]+=w/2; W_self[fb]+=w/2
        else:       # beam -> its own floor
            f=nearest_floor((a[2]+b[2])/2); W_self[f]+=w
    elif typ=="PLATE":
        z=sum(NODE[n][2] for n in nds)/len(nds)
        f=nearest_floor(z)
        area=poly_area(nds)
        W_self[f]+=area*TSLAB*GAMMA
        # pressures on this plate
        it=PRES.get(str(eid),{}).get("ITEMS",[])
        for p in it:
            mag=abs(p.get("FORCES",[0])[0])
            if p.get("LCNAME")=="SDL": W_sdl[f]+=mag*area
            elif p.get("LCNAME")=="LL": W_ll[f]+=mag*area

# scale geometric self-weight to the model's exact DL reaction so sheet ties to model
DL_MODEL=9573.1
f=DL_MODEL/sum(W_self)
W_self=[w*f for w in W_self]
print(f"(self-weight scaled by {f:.4f} to match model DL {DL_MODEL} kN)\n")

# seismic weight per story: 1.0 self(DL) + 1.0 SDL + 0.25 LL
Ws=[W_self[i]+W_sdl[i]+0.25*W_ll[i] for i in range(5)]
hx=[FLOORS[i]-ZBASE for i in range(5)]
Wtot=sum(Ws)

# ---- DPT 1301/1302-64 base shear (Bangkok Basin Zone 3 = Samut Songkhram) ----
# Table 1.4-5 (5% damping), Zone 3:
SDS=0.262   # Sa(0.2s) g
SD1=0.265   # Sa(1.0s) g
Igb=1.00    # importance factor (given)
Rf=5.0      # response modification, intermediate ductile RC moment frame (given)
Hbldg=13.4  # m, ground floor +0.30 to roof +13.70
T=0.02*Hbldg               # eq 3.3-1 (RC), Method A
Ts=SD1/SDS                 # plateau corner period
Sa=SDS if T<=Ts else SD1/T # design spectral accel at T (plateau since T<Ts)
Cs=max(Sa*Igb/Rf, 0.01)    # eq 3.2-2, min 0.01
Vcode=Cs*Wtot              # eq 3.2-1
Vanal=729.76               # base shear from analysis (kN), same X & Y
print(f"DPT: Zone3 SDS={SDS} SD1={SD1} T=0.02H={T:.3f}s Ts={Ts:.3f}s Sa={Sa:.3f}g "
      f"I={Igb} R={Rf} -> Cs={Cs:.4f}  Vcode={Vcode:.1f}kN  (analysis {Vanal}kN)")

V=Vcode    # use code base shear for ELF distribution
k=1.0      # T=0.27s <=0.5s -> k=1
whk=[Ws[i]*hx[i]**k for i in range(5)]
S=sum(whk)
Fx=[V*whk[i]/S for i in range(5)]
# story shear (cumulative from top)
Vx=[0.0]*5
acc=0.0
for i in range(4,-1,-1):
    acc+=Fx[i]; Vx[i]=acc

names=["2F","3F","4F","5F","Roof"]
print(f"{'Story':6}{'z(m)':>7}{'hx(m)':>7}{'Wself':>10}{'SDL':>9}{'LL':>9}{'Wseis':>10}{'w*h':>11}{'Cvx':>7}{'Fx':>9}{'Vx':>9}")
for i in range(4,-1,-1):
    print(f"{names[i]:6}{FLOORS[i]:>7.2f}{hx[i]:>7.2f}{W_self[i]:>10.1f}{W_sdl[i]:>9.1f}{W_ll[i]:>9.1f}{Ws[i]:>10.1f}{whk[i]:>11.1f}{whk[i]/S:>7.3f}{Fx[i]:>9.1f}{Vx[i]:>9.1f}")
print(f"{'SUM':6}{'':>7}{'':>7}{sum(W_self):>10.1f}{sum(W_sdl):>9.1f}{sum(W_ll):>9.1f}{sum(Ws):>10.1f}{S:>11.1f}{'':>7}{sum(Fx):>9.1f}")
print(f"\nDL(self) total = {sum(W_self):.1f} kN  (model DL reaction 9573.1)")
print(f"SDL total      = {sum(W_sdl):.1f} kN  (model SDL reaction 3506.8)")
print(f"LL total       = {sum(W_ll):.1f} kN  (model LL reaction 3635.1)")
print(f"Seismic weight W = {sum(Ws):.1f} kN ;  V(code) = {V:.1f} kN ;  Cs = {Cs:.4f}")

json.dump({"names":names,"z":FLOORS,"hx":hx,"Wself":W_self,"Wsdl":W_sdl,"Wll":W_ll,
           "Wseis":Ws,"whk":whk,"Fx":Fx,"Vx":Vx,"V":V,"Vanal":Vanal,"k":k,"Wtot":Wtot,
           "Cs":Cs,"DL":sum(W_self),"SDL":sum(W_sdl),"LL":sum(W_ll),
           "SDS":SDS,"SD1":SD1,"I":Igb,"R":Rf,"H":Hbldg,"T":T,"Ts":Ts,"Sa":Sa,"zone":3},
          open(SC+"/elf.json","w"),indent=1)
print("saved elf.json")
