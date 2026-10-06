# -*- coding: utf-8 -*-
import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator")
sys.path.insert(0,"src")
from windload.midas.connection import connect
connect(sys.argv[1])
import midas_gen as mg

def sb(name,H,B):
    return {"SECTTYPE":"DBUSER","SECT_NAME":name,"SECT_BEFORE":{
        "OFFSET_PT":"CC","OFFSET_CENTER":0,"USER_OFFSET_REF":0,"HORZ_OFFSET_OPT":0,
        "USERDEF_OFFSET_YI":0,"VERT_OFFSET_OPT":0,"USERDEF_OFFSET_ZI":0,
        "USE_SHEAR_DEFORM":True,"USE_WARPING_EFFECT":False,
        "SHAPE":"SB","DATATYPE":2,"SECT_I":{"vSIZE":[H,B]}}}

# id: (name, H, B)  vSIZE=[H,B] in metres, label "AxB" -> [A,B]
SECS={
 101:("C1 250x250 (GF)",0.25,0.25),
 102:("C1 350x350 (FT)",0.35,0.35),
 103:("C2 250x400 (GF)",0.25,0.40),
 104:("C2 350x500 (FT)",0.35,0.50),
 105:("C3 250x250 (GF)",0.25,0.25),
 106:("C3 350x350 (FT)",0.35,0.35),
}
assign={str(i):sb(*v) for i,v in SECS.items()}
r=mg.MidasAPI("PUT","/db/SECT",{"Assign":assign})
print("PUT:", "OK" if isinstance(r,dict) and "error" not in r else r)

# verify
sect=mg.MidasAPI("GET","/db/SECT",{}).get("SECT",{})
print("sections now:", len(sect))
for k in sorted(sect,key=lambda x:int(x)):
    sb_=sect[k]["SECT_BEFORE"]
    print(f"  {k}: {sect[k]['SECT_NAME']:<18} {sb_['SHAPE']} {sb_['SECT_I']['vSIZE'][:2]}")
