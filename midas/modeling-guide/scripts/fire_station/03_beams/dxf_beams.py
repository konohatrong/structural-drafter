# -*- coding: utf-8 -*-
import sys, math, json, re
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
import ezdxf
P=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
doc=ezdxf.readfile(P); msp=doc.modelspace()
O=[0,45778,91555,137333,183111]; N=["FDN","GB","2F","3F","RF"]
def pan(x): return min(range(5),key=lambda i:abs(x-O[i]-13000))
BEAMLAY={"S-HID_BEAM","S-CONT_BEAM"}
MARK=re.compile(r"^(GB\d\w*|B\d\w*|BX\w*)$")

segs=defaultdict(list)   # panel -> [(x1,y1,x2,y2,src)]
# --- MLINE: centreline from justification (0=top,1=zero,2=bottom) ---
for e in msp:
    if e.dxftype()!="MLINE" or e.dxf.layer not in BEAMLAY or not e.vertices: continue
    p=pan(e.vertices[0].location.x); half=e.dxf.scale_factor/2
    sh={0:-half,1:0.0,2:+half}[e.dxf.justification]
    V=[v.location for v in e.vertices]
    for a,b in zip(V,V[1:]):
        dx,dy=b.x-a.x,b.y-a.y; L=math.hypot(dx,dy)
        if L<1: continue
        nx,ny=-dy/L,dx/L                     # left normal
        segs[p].append((a.x-O[p]+sh*nx,a.y+sh*ny,b.x-O[p]+sh*nx,b.y+sh*ny,"MLINE:"+e.dxf.layer))
# --- LINE / LWPOLYLINE edges on beam layer: pair parallel edges ~250 apart ---
raw=defaultdict(list)
for e in msp:
    if e.dxf.layer not in BEAMLAY: continue
    if e.dxftype()=="LINE":
        s,t=e.dxf.start,e.dxf.end; raw[pan(s.x)].append((s.x,s.y,t.x,t.y))
    elif e.dxftype()=="LWPOLYLINE":
        pts=[(p[0],p[1]) for p in e.get_points()]
        if pts:
            pp=pan(pts[0][0])
            for a,b in zip(pts,pts[1:]): raw[pp].append((a[0],a[1],b[0],b[1]))
unpaired=defaultdict(list)
for p,L in raw.items():
    used=set()
    for i,(a) in enumerate(L):
        if i in used: continue
        ax1,ay1,ax2,ay2=a; da=math.atan2(ay2-ay1,ax2-ax1)
        best=None
        for j,(b) in enumerate(L):
            if j<=i or j in used: continue
            bx1,by1,bx2,by2=b; db=math.atan2(by2-by1,bx2-bx1)
            if abs(math.sin(da-db))>0.02: continue
            # perpendicular distance from b-start to line a
            Lh=math.hypot(ax2-ax1,ay2-ay1)
            d=abs((ax2-ax1)*(ay1-by1)-(ax1-bx1)*(ay2-ay1))/Lh
            if 200<d<300:
                best=j; break
        if best is None: unpaired[p].append(a); continue
        used.add(i); used.add(best); b=L[best]
        # align b direction with a
        if (b[2]-b[0])*(ax2-ax1)+(b[3]-b[1])*(ay2-ay1)<0: b=(b[2],b[3],b[0],b[1])
        segs[p].append(((ax1+b[0])/2-O[p],(ay1+b[1])/2,(ax2+b[2])/2-O[p],(ay2+b[3])/2,"LINEPAIR"))
# --- marks ---
marks=defaultdict(list)
for e in msp:
    if e.dxftype()=="TEXT":
        t=e.dxf.text.strip()
        if MARK.match(t):
            p=pan(e.dxf.insert.x)
            marks[p].append((e.dxf.insert.x-O[p],e.dxf.insert.y,t,round(e.dxf.rotation)%180))

out={}
for p in [1,2,3,4]:
    print(f"\n===== {N[p]} : {len(segs[p])} beam centre-segments, {len(unpaired[p])} unpaired edges, marks {dict(Counter(m[2] for m in marks[p]))}")
    for s in segs[p]:
        x1,y1,x2,y2,src=s
        # nearest mark with matching orientation
        horiz=abs(y2-y1)<abs(x2-x1); want=0 if horiz else 90
        mx=(x1+x2)/2; my=(y1+y2)/2; L=math.hypot(x2-x1,y2-y1)
        best=None; bd=1e9
        for (tx,ty,t,r) in marks[p]:
            if r!=want and abs(x2-x1)>1 and abs(y2-y1)>1: pass
            # distance from text to segment
            ux,uy=(x2-x1)/L,(y2-y1)/L
            s_=(tx-x1)*ux+(ty-y1)*uy
            if s_<-300 or s_>L+300: continue
            d=abs((tx-x1)*uy-(ty-y1)*ux)
            if r!=want: d+=2000
            if d<bd: bd=d; best=t
        mk=best if bd<900 else "?"
        out.setdefault(N[p],[]).append({"x1":x1,"y1":y1,"x2":x2,"y2":y2,"src":src,"mark":mk})
    for u in unpaired[p][:12]: print("   unpaired edge:",tuple(round(v-(O[p] if k%2==0 else 0)) for k,v in enumerate(u)))
json.dump({"segs":out,"marks":{N[p]:marks[p] for p in marks}},open(SC+"/fs_beams_raw.json","w"),indent=1)
for lv,L in out.items():
    print(f"{lv}: marks assigned {dict(Counter(s['mark'] for s in L))}")
