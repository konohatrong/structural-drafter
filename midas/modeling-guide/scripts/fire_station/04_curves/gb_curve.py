# -*- coding: utf-8 -*-
# Replace GB straight chamfer D6-E7 by the true curved beam, discretised into straight chords.
import sys, json, math
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
NCH=int(sys.argv[1]) if len(sys.argv)>1 else 6

def arc_from_bulge(p1,p2,b):
    th=4*math.atan(b); dx,dy=p2[0]-p1[0],p2[1]-p1[1]; c=math.hypot(dx,dy)
    R=c/(2*math.sin(th/2)); h=c/(2*math.tan(th/2))
    mx,my=(p1[0]+p2[0])/2,(p1[1]+p2[1])/2; nx,ny=-dy/c,dx/c        # left normal (bulge>0 -> CCW)
    return (mx+h*nx,my+h*ny),R,th
ci,Ri,thi=arc_from_bulge((27125,4300),(23667,7873),0.4047)          # inner face (S-HID_BEAM)
co,Ro,tho=arc_from_bulge((27375,4300),(23675,8123),0.4047)          # outer face (WALL)
print(f"inner face : centre=({ci[0]:.0f},{ci[1]:.0f}) R={Ri:.0f}  sweep={math.degrees(thi):.1f}°")
print(f"outer face : centre=({co[0]:.0f},{co[1]:.0f}) R={Ro:.0f}  sweep={math.degrees(tho):.1f}°")
# centreline: midpoints of the two faces at start/end, arc through them with same bulge
p1=((27125+27375)/2,4300); p2=((23667+23675)/2,(7873+8123)/2)
cc,Rc,thc=arc_from_bulge(p1,p2,0.4047)
a0=math.atan2(p1[1]-cc[1],p1[0]-cc[0]); arclen=Rc*thc
sag=Rc*(1-math.cos(thc/NCH/2))
print(f"centreline : centre=({cc[0]:.0f},{cc[1]:.0f}) R={Rc:.0f} sweep={math.degrees(thc):.1f}° arc length={arclen:.0f} mm")
print(f"{NCH} chords: each {2*Rc*math.sin(thc/NCH/2):.0f} mm, max deviation from arc (sagitta) {sag:.0f} mm")
pts=[(round(cc[0]+Rc*math.cos(a0+thc*k/NCH)),round(cc[1]+Rc*math.sin(a0+thc*k/NCH))) for k in range(NCH+1)]
D6=(23550,8000); E7=(27250,4000)
print(f"arc end {pts[-1]} -> snapped to D6 {D6} (shift {math.dist(pts[-1],D6):.0f} mm)")
pts[-1]=D6
poly=[E7]+pts                                                          # E7 -> straight leg -> arc chords -> D6

M=json.load(open(SC+"/fs_beammodel.json")); G=M["GB"]
before=len(G["elems"])
G["elems"]=[e for e in G["elems"] if {tuple(e["a"]),tuple(e["b"])}!={D6,E7}]
for a,b in zip(poly,poly[1:]):
    G["elems"].append({"a":list(a),"b":list(b),"mark":"GB1","src":"text","curve":True})
json.dump(M,open(SC+"/fs_beammodel.json","w"),indent=1)
print(f"GB beams: {before} -> {len(G['elems'])}   curve nodes: {poly}")
