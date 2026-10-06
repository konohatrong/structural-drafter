# -*- coding: utf-8 -*-
import sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
import ezdxf
P=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
doc=ezdxf.readfile(P)
msp=doc.modelspace()
print("DXF version:", doc.dxfversion, "| encoding:", doc.encoding)
print("units (INSUNITS):", doc.header.get("$INSUNITS"))

# layers
print("\n=== LAYERS ===", len(doc.layers))
for lay in sorted(doc.layers, key=lambda l:l.dxf.name):
    print(f"  {lay.dxf.name}")

# entity counts by type
et=Counter(e.dxftype() for e in msp)
print("\n=== ENTITY TYPES (modelspace) ===")
for k,c in et.most_common(): print(f"  {k:14} {c}")

# entity counts by layer
bl=Counter(e.dxf.layer for e in msp)
print("\n=== ENTITIES BY LAYER ===")
for k,c in bl.most_common(): print(f"  {k:28} {c}")

# extents
try:
    ext=doc.header.get("$EXTMIN"), doc.header.get("$EXTMAX")
    print("\nEXTENTS:", ext)
except: pass

# blocks / inserts
ins=Counter(e.dxf.name for e in msp if e.dxftype()=="INSERT")
print("\n=== BLOCK INSERTS ===", sum(ins.values()))
for k,c in ins.most_common(30): print(f"  {k:28} {c}")
