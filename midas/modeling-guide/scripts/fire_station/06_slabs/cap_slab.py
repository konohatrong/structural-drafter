import sys, os, json, base64
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
L=sys.argv[2]
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
act={"ACTIVE_MODE":"Identity","IDENTITY_TYPE":"Group","IDENTITY_LIST":[f"SLAB_{L}",f"BEAM_{L}"]}
for nm,(h,v) in {"top":(0,90),"iso":(-60,25)}.items():
    r=mg.MidasAPI("POST","/view/CAPTURE",{"Argument":{"SET_MODE":"pre","SET_HIDDEN":False,"HEIGHT":1100,"WIDTH":1700,
        "ANGLE":{"HORIZONTAL":h,"VERTICAL":v},"ACTIVE":act}})
    b=r.get("base64String") if isinstance(r,dict) else None
    if b: open(SC+f"/mid_slab_{L}_{nm}.png","wb").write(base64.b64decode(b)); print("saved",nm)
    else: print(nm,json.dumps(r)[:300])
mg.MidasAPI("POST","/view/CAPTURE",{"Argument":{"SET_MODE":"pre","HEIGHT":200,"WIDTH":200,"ACTIVE":{"ACTIVE_MODE":"All"}}})
print("active reset to All")
