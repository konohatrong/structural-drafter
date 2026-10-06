# -*- coding: utf-8 -*-
# Build *REBAR-BEAM / *REBAR-COLUMN MCT from the drawing schedules (S2-02 columns, S2-04 beams).
# usage: python rebar_mct.py <out.mct> <sections comma-separated | all>
import sys
out,which=sys.argv[1],sys.argv[2]
# ---- beams: (dT=dB to 1st-layer bar centre, bar, support(top L1,L2, bot L1,L2), mid(...), s_sup, s_mid)
BEAMS={
 201:(0.070,"DB20",(3,3,3,0),(3,0,3,3),0.15,0.20),   # GB1  continuous
 202:(0.070,"DB20",(3,3,3,0),(3,3,3,0),0.15,0.15),   # GB1A all span
 203:(0.070,"DB20",(3,3,3,0),(3,3,3,0),0.15,0.15),   # GB1C cantilever
 204:(0.060,"DB20",(3,3,3,0),(3,0,3,3),0.15,0.20),   # B1   continuous
 205:(0.060,"DB20",(3,3,3,0),(3,3,3,0),0.15,0.15),   # B1A  all span
 206:(0.060,"DB20",(3,3,3,0),(3,3,3,0),0.15,0.15),   # B1C  cantilever
 207:(0.058,"DB16",(3,3,3,0),(3,0,3,3),0.15,0.20),   # B2   continuous
 209:(0.058,"DB16",(3,3,3,0),(3,0,3,3),0.15,0.20),   # B2A  = B2 (assumed)
}
# ---- columns: (bar, total, rows, do, end spacing, end legs y,z, centre spacing, centre legs y,z)
COLS={
 101:("DB20",8,3,0.060,0.10,2,2,0.15,2,2),    # C1 GF 250x250 8-DB20
 105:("DB20",8,3,0.060,0.10,2,2,0.15,2,2),    # C3 GF 250x250 8-DB20
 103:("DB20",12,3,0.060,0.10,4,4,0.20,4,4),   # C2 GF 250x400 12-DB20 (3 x 5), 2 hoops
 102:("DB20",12,4,0.070,0.10,4,4,0.15,4,4),   # C1 FT 350x350 12-DB20 (4 per face), 3 hoops
 106:("DB20",12,4,0.070,0.10,4,4,0.15,4,4),   # C3 FT 350x350
 104:("DB20",12,3,0.070,0.10,4,4,0.20,4,4),   # C2 FT 350x500 12-DB20 (3 x 5), 2 hoops
}
sel=None if which=="all" else {int(s) for s in which.split(",")}
L=["*UNIT","   KN, M, BTU, F",""]
b=[s for s in BEAMS if sel is None or s in sel]; c=[s for s in COLS if sel is None or s in sel]
# importer only accepts rebar for sections declared in the same file -> repeat the model's own *DGN-SECT lines (unchanged)
src=open("model_backup_before_rebar.mct",encoding="utf-8",errors="replace").read().splitlines(); f=False; dg={}
for l in src:
    if l.startswith("*DGN-SECT"): f=True; continue
    if f and l.startswith("*"): break
    if f and l.strip() and not l.startswith(";"): dg[int(l.split(",")[0])]=l
MODE=sys.argv[3] if len(sys.argv)>3 else "SECTION"
def block(tag):
    f=False; d={}
    for l in src:
        if l.startswith("*"+tag+" ") or l.strip()=="*"+tag or l.startswith("*"+tag+"	") or l.startswith("*"+tag+"    "): f=True; continue
        if f and l.startswith("*"): break
        if f and l.strip() and not l.startswith(";"): d[int(l.split(",")[0])]=l
    return d
for tag in MODE.split("+"):
    d=block(tag); L+=["*"+tag]+[d[s] for s in sorted(b+c)]+[""]
if b:
    L.append("*REBAR-BEAM    ; Modify Beam Rebar Data")
    for s in b:
        d,bar,sup,mid,ss,sm=BEAMS[s]
        L.append(f"  {s},    0, DB10, {d}, {d}, 0, 0, , 0, , , YES, YES, YES")
        for (t1,t2,b1,b2),sp in ((sup,ss),(mid,sm),(sup,ss)):
            L.append(f"       0, {t1}, {t2}, {bar}, {bar},   0, {b1}, {b2}, {bar}, {bar},   {sp}, 2, 0")
    L.append("")
if c:
    L.append("*REBAR-COLUMN    ; Modify Column Rebar Data")
    for s in c:
        bar,n,rows,do,se,ey,ez,sc,cy,cz=COLS[s]
        L.append(f"  {s},    0, TIED, {bar}, NO, {bar}, {n}, {rows}, {do}, DB10, {se}, {ey}, {ez}, 0, DB10, {sc}, {cy}, {cz}, NO")
    L.append("")
L.append("*ENDDATA")
open(out,"w",encoding="utf-8").write("\n".join(L)+"\n"); print("\n".join(L))
