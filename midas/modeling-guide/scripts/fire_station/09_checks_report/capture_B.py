# -*- coding: utf-8 -*-
# Building B report figures (read-only captures). ACTIVE is reset to All at the end.
import sys, os
from base64 import b64decode
sys.stdout.reconfigure(encoding="utf-8")
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
from midas_gen import ResultGraphic as RG
OUT=__import__("os").environ.get("MG_WORKDIR", ".")+"/Bimg"
os.makedirs(OUT,exist_ok=True)
def cap(name, rg=None, h=-55, v=22, hidden=False, mode="post", w=1600, ht=1050):
    a={"SET_MODE":mode,"SET_HIDDEN":hidden,"HEIGHT":ht,"WIDTH":w,"ANGLE":{"HORIZONTAL":h,"VERTICAL":v},"ACTIVE":{"ACTIVE_MODE":"All"}}
    if rg is not None: a["RESULT_GRAPHIC"]=rg
    r=mg.MidasAPI("POST","/view/CAPTURE",{"Argument":a})
    if isinstance(r,dict) and "base64String" in r:
        open(f"{OUT}/{name}.png","wb").write(b64decode(r["base64String"])); print("  OK",name); return True
    print("  FAIL",name,str(r)[:200]); return False
def contour():
    RG.Contour(use=True, num_color=12, color='rgb')
    RG.Deform(use=True, scale=1.0, bRealDeform=False, bRealDisp=False, bRelativeDisp=False)
    RG.Legend(use=True, position='right', bExponent=False, num_decimal=2); RG.Values(use=False)
def reaction():
    RG.Deform(use=False); RG.Legend(use=True, position='right', bExponent=False, num_decimal=1)
    RG.Values(use=True, bExpo=False, num_decimal=1, orient_angle=0)
cap("geom_iso",mode="pre",hidden=True)
cap("geom_front",mode="pre",hidden=True,h=0,v=0)
cap("geom_side",mode="pre",hidden=True,h=90,v=0)
for lc,typ,comp,nm,h,v in (("S1","CB","DZ","disp_S1",-55,22),("S1","CB","DZ","disp_S1_side",0,0),("Ex","ST","DX","disp_Ex",-55,15),("Ey","ST","DY","disp_Ey",-55,15)):
    contour()
    if not cap(nm,RG.DisplacementContour(typ,lc,"Max",comp),h=h,v=v) and typ=="CB":
        contour(); cap(nm,RG.DisplacementContour("ST","DL","Max",comp),h=h,v=v)
reaction(); cap("react_S1",RG.ReactionForcesMoments("CB","S1","Max","FZ"),h=-55,v=30)
reaction(); cap("react_U1",RG.ReactionForcesMoments("CB","U1","Max","FZ"),h=-55,v=30)
print("done")
