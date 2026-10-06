# -*- coding: utf-8 -*-
import sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
import ezdxf
P=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
doc=ezdxf.readfile(P)
msp=doc.modelspace()

# 1) larger title texts (S-40Txt, 40Txt, S-TH, S-Txt 4.0) and any text height>200
print("=== TITLE-ish / big TEXT ===")
rows=[]
for e in msp:
    if e.dxftype() in ("TEXT","MTEXT"):
        try: t=(e.plain_text() if e.dxftype()=="MTEXT" else e.dxf.text).strip()
        except: t=""
        h=getattr(e.dxf,"height",0) or getattr(e.dxf,"char_height",0)
        lay=e.dxf.layer
        if t and (h>=150 or "40Txt" in lay or "S-TH" in lay or "Txt 4" in lay):
            p=e.dxf.insert; rows.append((round(p[0]),round(p[1]),round(h),lay,t))
for x,y,h,lay,t in sorted(rows):
    print(f"  x={x:>9} y={y:>7} h={h:>4} [{lay[:16]:16}] {t[:55]}")

# 2) INSERT attributes (marks, footing tags, titles)
print("\n=== INSERT + ATTRIB (block, attrib text) ===")
attrs=defaultdict(list)
for e in msp:
    if e.dxftype()=="INSERT":
        for a in e.attribs:
            v=(a.dxf.text or "").strip()
            if v: attrs[e.dxf.name].append(v)
for bn,vals in sorted(attrs.items()):
    c=Counter(vals)
    print(f"  {bn:22} -> {dict(list(c.items())[:12])}")

# 3) modelspace text on marks layer beyond x=90000
print("\n=== marks x>90000 (remaining panels) ===")
seen=set()
for e in msp:
    if e.dxftype()=="TEXT":
        p=e.dxf.insert
        if p[0]>90000:
            t=e.dxf.text.strip()
            if t and (round(p[0]/1000),t) not in seen:
                seen.add((round(p[0]/1000),t))
# group unique marks by coarse X band
band=defaultdict(Counter)
for e in msp:
    if e.dxftype()=="TEXT":
        p=e.dxf.insert; t=e.dxf.text.strip()
        if not t: continue
        b=int(p[0]//20000)   # 20m bands
        band[b][t]+=1
for b in sorted(band):
    x0=b*20; items=", ".join(f"{k}×{v}" for k,v in band[b].most_common(14))
    print(f"  X {x0}-{x0+20}m: {items}")
