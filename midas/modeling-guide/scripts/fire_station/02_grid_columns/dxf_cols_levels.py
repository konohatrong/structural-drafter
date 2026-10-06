# -*- coding: utf-8 -*-
import sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
import ezdxf
from ezdxf.math import Vec3
P=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
doc=ezdxf.readfile(P); msp=doc.modelspace()

# ---- column marks (F#,C#) positions in foundation panel (x<40000) ----
colmarks=[]
for e in msp:
    if e.dxftype()=="TEXT":
        t=e.dxf.text.strip(); p=e.dxf.insert
        if p[0]<40000 and (",C1" in t or ",C2" in t):
            colmarks.append((p[0],p[1],t.split(",")[-1]))
cc=Counter(m[2] for m in colmarks)
print("column marks in foundation panel:", dict(cc))

# ---- measure red column solids/geometry near each mark ----
# gather small closed rectangles (SOLID + LWPOLYLINE) on column-ish layers, in foundation panel
def bbox_of(e):
    try:
        pts=[]
        if e.dxftype()=="SOLID":
            pts=[e.dxf.vtx0,e.dxf.vtx1,e.dxf.vtx2,e.dxf.vtx3]
        elif e.dxftype()=="LWPOLYLINE":
            pts=[Vec3(x,y) for x,y,*_ in e.get_points()]
        elif e.dxftype()=="HATCH":
            return None
        if not pts: return None
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        return min(xs),min(ys),max(xs),max(ys)
    except: return None

# explode column INSERTs to get actual column rectangles
cands=[]
for e in msp:
    if e.dxftype()=="INSERT" and ("Col" in e.dxf.name or e.dxf.name.startswith("*U11")):
        try:
            for se in e.explode():
                pass
        except: pass
# simpler: look at SOLID entities (red columns often SOLID)
sol=[e for e in msp if e.dxftype()=="SOLID"]
print(f"\nSOLID entities: {len(sol)}")
sizes=Counter()
for e in sol:
    b=bbox_of(e)
    if b:
        w=round(b[2]-b[0]); h=round(b[3]-b[1])
        if 100<=w<=700 and 100<=h<=700:
            sizes[(min(w,h),max(w,h))]+=1
print("SOLID sizes (w,h) in col range:", dict(sizes))

# ---- also measure Col-Continuous block internal column rects ----
for bn in ["Col-Continuous","Col-Break"]:
    if bn in doc.blocks:
        blk=doc.blocks[bn]
        sz=Counter()
        for e in blk:
            b=bbox_of(e)
            if b:
                w=round(b[2]-b[0]); h=round(b[3]-b[1])
                if 100<=w<=700 and 100<=h<=700: sz[(min(w,h),max(w,h))]+=1
        print(f"block {bn} rect sizes:", dict(list(sz.items())[:20]))

# ---- floor levels from Sym-SFL / sym_slab attribs, grouped by panel(X band) ----
print("\n=== LEVEL TAGS (SFL) by panel ===")
lv=defaultdict(list)
for e in msp:
    if e.dxftype()=="INSERT" and e.dxf.name in ("Sym-SFL","sym_slab 2","Sym-LEVEL"):
        vals=[a.dxf.text.strip() for a in e.attribs if a.dxf.text and a.dxf.text.strip()]
        x=e.dxf.insert[0]
        panel=int(x//40000)
        for v in vals:
            if v.startswith("+") or v.startswith("%%P") or v[0].isdigit(): lv[panel].append(v)
for pn in sorted(lv):
    c=Counter(lv[pn])
    print(f"  panel {pn} (x~{pn*40}-{pn*40+40}m): {dict(c)}")
