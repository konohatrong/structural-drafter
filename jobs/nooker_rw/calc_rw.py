"""
Nooker retaining wall RW - design check (per metre run). Reproduces sheet 1001 note 3 / sheet 5001 design data.
Units kN, m, kPa; bars mm / MPa. Run: python calc_rw.py
Basis: EIT 1008-38 strength design (U = 1.7 H for earth pressure + surcharge); development and hooks per ACI 318-19.
"""
import math
gc,gs,gw=24.0,18.0,9.81
B,tf,ts,Ht,Df=1.20,0.25,0.20,1.00,0.40   # base, footing thk, stem thk, top of wall to founding, founding depth below front ground
kb,kd=0.25,0.30                            # key at heel end
K0,q,mu,Kp=0.50,10.0,0.40,3.0
hs=Ht-tf
def case(water=False,qv=False,label=''):
    Ps=0.5*K0*gs*Ht**2; Pq=K0*q*Ht; Pw=0.5*gw*Ht**2 if water else 0
    H=Ps+Pq+Pw; Mo=Ps*Ht/3+Pq*Ht/2+Pw*Ht/3
    W=[(ts*hs*gc,ts/2),(B*tf*gc,B/2),((B-ts)*hs*gs,ts+(B-ts)/2),(kb*kd*gc,B-kb/2)]
    if qv: W.append((q*(B-ts),ts+(B-ts)/2))
    V=sum(w for w,_ in W); Mr=sum(w*x for w,x in W)
    Pp=0.5*(Kp/2)*gs*((Df+kd)**2-Df**2)      # half passive over key depth, overburden to founding level
    FSo=Mr/Mo; FSs=(mu*V+Pp)/H
    xb=(Mr-Mo)/V; e=B/2-xb
    qmax=V/B*(1+6*e/B) if abs(e)<=B/6 else 2*V/(3*xb)
    print(f'{label:32s} H={H:5.2f} V={V:5.2f} Mo={Mo:5.2f} Mr={Mr:5.2f} FSot={FSo:4.2f} FSsl={FSs:4.2f} Pp={Pp:4.2f} e={e:+.3f} B/6={B/6:.3f} qmax={qmax:5.1f}')
    return FSo,FSs,qmax,e
print('--- STABILITY (per m) ---')
r1=case(label='K0 + 10 kPa lateral, no vert q')
r2=case(qv=True,label='K0 + 10 kPa incl. vert q on heel')
r3=case(water=True,label='drain blocked (accidental)')
print('--- STEM (EIT 1008-38: U=1.7H) ---')
fc,fy=24.0,390.0
Ms=K0*gs*hs**3/6+K0*q*hs**2/2; Vs=0.5*K0*gs*hs**2+K0*q*hs
Mu,Vu=1.7*Ms,1.7*Vs
d=200-40-6; As=565
a=As*fy/(0.85*fc*1000); phiMn=0.9*As*fy*(d-a/2)/1e6; phiVc=0.75*0.17*math.sqrt(fc)*1000*d/1e3
print(f'hs={hs} Ms={Ms:.2f} Mu={Mu:.2f} phiMn={phiMn:.1f} kNm/m | Vu={Vu:.2f} phiVc={phiVc:.1f} kN/m')
print('--- HEEL (cantilever from stem back face, ignore upward bearing) ---')
L=B-ts; w=hs*gs+q+tf*gc; Mh=w*L**2/2; Vh=w*(L-0.194)
Muh=1.7*Mh; Vuh=1.7*Vh; dh=250-50-6
a=565*fy/(0.85*fc*1000); phiMnh=0.9*565*fy*(dh-a/2)/1e6; phiVch=0.75*0.17*math.sqrt(fc)*1000*dh/1e3
print(f'w={w:.1f} kPa Mh={Mh:.2f} Mu={Muh:.2f} phiMn(DB12@200 T)={phiMnh:.1f} | Vu={Vuh:.1f} phiVc={phiVch:.1f}')
print('--- ANCHORAGE / LAPS (ACI 318-19) ---')
psi_c=fc/105+0.6   # ACI 318-19 Table 25.4.3.2
for db in (10,12):
    ldh=max(fy*1.0*1.0*psi_c/(23*math.sqrt(fc))*db**1.5,8*db,150)
    ld=max(fy*db/(2.1*math.sqrt(fc)),300)
    print(f'DB{db}: ldh={ldh:.0f}  ld={ld:.0f}  lap classB=1.3ld={1.3*ld:.0f}')
print('psi_r = 1.0 (bar spacing 200 >= 6 db). available for (1): T.O.F. -150 to outside of bend -326 = 176 mm')
print('--- MIN STEEL ---')
print('stem horiz ACI 11.6.1 (fy<420): 0.0025*200*1000 =',0.0025*200*1000,'mm2/m; provided DB12@200+DB10@200 =',565+393)
print('stem vert 0.0015*200*1000 = 300; provided DB12@200+DB10@400 =',565+196)
print('footing shrinkage 0.0020*250*1000 = 500 each dir; provided DB12@200 T&B =',2*565)
