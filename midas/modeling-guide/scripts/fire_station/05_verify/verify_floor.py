# -*- coding: utf-8 -*-
# Independent verification of one floor's analytical beams against the DXF.
import sys, json, math, re
from collections import defaultdict, Counter
sys.stdout.reconfigure(encoding="utf-8")
import ezdxf
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
L=sys.argv[1] if len(sys.argv)>1 else "2F"
O={"GB":45778,"2F":91555,"3F":137333,"RF":183111}[L]
SHIFT=(2645,7802) if L=="2F" else None                    # displaced east bay on 2F
doc=ezdxf.readfile(r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf")
msp=doc.modelspace()
M=json.load(open(SC+"/fs_beammodel.json"))[L]; CM=json.load(open(SC+"/fs_colmodel.json"))
BEAMLAY={"S-HID_BEAM","S-CONT_BEAM"}; MARK=re.compile(r"^(GB\d\w*|B\d\w*|BX\w*)$")
def inpanel(x): return -4000<x-O<33000
def loc(x,y):
    x-=O
    if SHIFT and x>25500 and y>7000: return (x-SHIFT[0],y-SHIFT[1],True)
    return (x,y,False)

# ---------- DXF beam centre-lines ----------
dxf=[]   # (x1,y1,x2,y2,src)
for e in msp:
    if e.dxf.layer not in BEAMLAY: continue
    t=e.dxftype()
    if t=="MLINE" and e.vertices and inpanel(e.vertices[0].location.x):
        half=e.dxf.scale_factor/2; sh={0:-half,1:0,2:half}[e.dxf.justification]; V=[v.location for v in e.vertices]
        for a,b in zip(V,V[1:]):
            dx,dy=b.x-a.x,b.y-a.y; Lg=math.hypot(dx,dy); nx,ny=-dy/Lg,dx/Lg
            p=loc(a.x+sh*nx,a.y+sh*ny); q=loc(b.x+sh*nx,b.y+sh*ny)
            dxf.append((p[0],p[1],q[0],q[1],"MLINE"+(" (displaced)" if p[2] else "")))
edges=[]
for e in msp:
    if e.dxf.layer not in BEAMLAY: continue
    if e.dxftype()=="LINE" and inpanel(e.dxf.start.x):
        p=loc(e.dxf.start.x,e.dxf.start.y); q=loc(e.dxf.end.x,e.dxf.end.y); edges.append((p[0],p[1],q[0],q[1]))
    elif e.dxftype()=="LWPOLYLINE":
        pts=list(e.get_points("xyb"))
        if pts and inpanel(pts[0][0]):
            if any(abs(p[2])>1e-6 for p in pts): continue          # arcs handled explicitly (curved beam)
            P=[loc(p[0],p[1]) for p in pts]
            for a,b in zip(P,P[1:]): edges.append((a[0],a[1],b[0],b[1]))
used=set()
for i,a in enumerate(edges):                                       # pair parallel edges 200-300 apart
    if i in used: continue
    ax1,ay1,ax2,ay2=a; La=math.hypot(ax2-ax1,ay2-ay1)
    if La<1: continue
    for j,b in enumerate(edges):
        if j<=i or j in used: continue
        bx1,by1,bx2,by2=b
        if abs(math.sin(math.atan2(ay2-ay1,ax2-ax1)-math.atan2(by2-by1,bx2-bx1)))>0.02: continue
        d=abs((ax2-ax1)*(ay1-by1)-(ax1-bx1)*(ay2-ay1))/La
        if 200<d<300:
            if (bx2-bx1)*(ax2-ax1)+(by2-by1)*(ay2-ay1)<0: b=(bx2,by2,bx1,by1)
            dxf.append(((ax1+b[0])/2,(ay1+b[1])/2,(ax2+b[2])/2,(ay2+b[3])/2,"LINEPAIR")); used|={i,j}; break
# curved beam (bulged polyline) -> dense polyline of its centre-line
for e in msp:
    if e.dxftype()=="LWPOLYLINE" and e.dxf.layer in BEAMLAY:
        pts=list(e.get_points("xyb"))
        if pts and inpanel(pts[0][0]) and any(abs(p[2])>1e-6 for p in pts):
            dxf.append((0,0,0,0,"ARC"))   # marker; arc centre-line is known analytically
marks=[]
for e in msp:
    if e.dxftype()=="TEXT" and MARK.match(e.dxf.text.strip()) and inpanel(e.dxf.insert.x):
        p=loc(e.dxf.insert.x,e.dxf.insert.y); marks.append((p[0],p[1],e.dxf.text.strip(),round(e.dxf.rotation)%180,p[2]))
sfl=[]
for e in msp:
    if e.dxftype()=="INSERT" and e.dxf.name=="Sym-SFL" and inpanel(e.dxf.insert.x):
        v=[a.dxf.text.strip() for a in e.attribs]; p=loc(e.dxf.insert.x,e.dxf.insert.y)
        lv=[t for t in v if t.startswith("+")]; ty=[t for t in v if re.match(r"^[A-Z]+\d",t)]
        if lv: sfl.append((p[0],p[1],lv[0],ty[0] if ty else "",p[2]))

# ---------- geometry helpers ----------
E=M["elems"]; cn={tuple(map(int,map(float,k.split(",")))) for k in M["colnodes"]}
def dseg(px,py,x1,y1,x2,y2):
    dx,dy=x2-x1,y2-y1; L2=dx*dx+dy*dy
    t=0 if L2==0 else max(0,min(1,((px-x1)*dx+(py-y1)*dy)/L2)); return math.hypot(px-x1-t*dx,py-y1-t*dy)
def arcdist(px,py): return abs(math.hypot(px-23550,py-4300)-3700) if (px>23500 and py>4250) else 1e9
real=[s for s in dxf if s[4]!="ARC"]; has_arc=any(s[4]=="ARC" for s in dxf)
def near_dxf(px,py): return min([dseg(px,py,*s[:4]) for s in real]+([arcdist(px,py)] if has_arc else []))
def near_model(px,py): return min(dseg(px,py,*e["a"],*e["b"]) for e in E)

# 1) DXF -> model coverage
unc=[]
for s in real:
    x1,y1,x2,y2,src=s; Lg=math.hypot(x2-x1,y2-y1); n=max(2,int(Lg//250))
    miss=[k for k in range(1,n) if near_model(x1+(x2-x1)*k/n,y1+(y2-y1)*k/n)>200]
    if len(miss)>0.3*(n-1):
        lab=[m[2] for m in marks if dseg(m[0],m[1],x1,y1,x2,y2)<900]
        unc.append((round(x1),round(y1),round(x2),round(y2),src,sorted(set(lab))))
# 2) model -> DXF support
nodxf=[]
for e in E:
    (x1,y1),(x2,y2)=e["a"],e["b"]; Lg=math.dist(e["a"],e["b"]); n=max(2,int(Lg//250))
    bad=[k for k in range(1,n) if near_dxf(x1+(x2-x1)*k/n,y1+(y2-y1)*k/n)>260]
    if len(bad)>0.3*(n-1): nodxf.append((e["id"],e["mark"],e["a"],e["b"]))
# 3) labels vs model marks
lab_issue=[]; lab_unused=[]
for (tx,ty,t,r,disp) in marks:
    best=None; bd=1e9
    for e in E:
        (x1,y1),(x2,y2)=e["a"],e["b"]; Lg=math.dist(e["a"],e["b"]); ux,uy=(x2-x1)/Lg,(y2-y1)/Lg
        diag=abs(ux)>0.05 and abs(uy)>0.05; want=0 if abs(uy)<0.05 else 90
        tt=(tx-x1)*ux+(ty-y1)*uy
        if tt<-150 or tt>Lg+150: continue
        d=abs((tx-x1)*uy-(ty-y1)*ux)+(0 if (diag or r==want or (r in(0,90) and False)) else 3000)
        if d<bd: bd=d; best=e
    if best is None or bd>900:
        lab_unused.append((round(tx),round(ty),t,r))
    elif best["mark"]!=t:
        lab_issue.append((t,best["id"],best["mark"],best["a"],best["b"],round(tx),round(ty)))
# 4) crossings without node / free ends
cross=[]
for i,a in enumerate(E):
    for b in E[i+1:]:
        (x1,y1),(x2,y2)=a["a"],a["b"]; (x3,y3),(x4,y4)=b["a"],b["b"]
        den=(x2-x1)*(y4-y3)-(y2-y1)*(x4-x3)
        if abs(den)<1e-9: continue
        t=((x3-x1)*(y4-y3)-(y3-y1)*(x4-x3))/den; u=((x3-x1)*(y2-y1)-(y3-y1)*(x2-x1))/den
        if 0.001<t<0.999 and 0.001<u<0.999: cross.append((a["id"],b["id"]))
deg=Counter([tuple(e["a"]) for e in E]+[tuple(e["b"]) for e in E])
free=[(p,[e["mark"] for e in E if tuple(e["a"])==p or tuple(e["b"])==p]) for p,c in deg.items() if c==1 and p not in cn]
colused=sum(1 for p in cn if deg.get(p,0)>0); colunused=[p for p in cn if deg.get(p,0)==0]

res={"L":L,"unc":unc,"nodxf":nodxf,"lab_issue":lab_issue,"lab_unused":lab_unused,"cross":cross,"free":free,
     "colunused":colunused,"sfl":sfl,"n_dxf":len(real),"n_model":len(E),"n_marks":len(marks)}
json.dump(res,open(SC+f"/verify_{L}.json","w"),indent=1,default=str)
print(f"=== VERIFY {L}: DXF beam centre-lines {len(real)}{' + curved beam' if has_arc else ''} | model beams {len(E)} | DXF labels {len(marks)}")
print(f"[1] DXF beams NOT in model: {len(unc)}");    [print("     ",u) for u in unc]
print(f"[2] model beams with NO DXF beam: {len(nodxf)}"); [print("     ",u) for u in nodxf]
print(f"[3] label ≠ model mark: {len(lab_issue)}");   [print("     ",u) for u in lab_issue]
print(f"    labels not matched to any beam: {len(lab_unused)}"); [print("     ",u) for u in lab_unused]
print(f"[4] crossings without shared node: {len(cross)} {cross}")
print(f"    free (dangling) beam ends: {free}")
print(f"    column nodes at this level used: {colused}/{len(cn)}   unused: {colunused}")
print(f"[5] SFL tags (x,y,level,slab,displaced):")
for s in sorted(sfl,key=lambda s:(s[1],s[0])): print("     ",(round(s[0]),round(s[1]),s[2],s[3],"displaced" if s[4] else ""))
