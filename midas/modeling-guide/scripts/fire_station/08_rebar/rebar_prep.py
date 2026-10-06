# -*- coding: utf-8 -*-
# Rebar from ST-Detail S2-02 (column schedule) and S2-04 (beam schedule) -> MIDAS /db/RCHK payload (NOT sent).
# Assumptions (to confirm): clear cover beam 40, ground beam 50, column 40, footing stub 50 mm; stirrup/tie DB10;
# layer-2 centre = layer-1 centre + db + 25 mm; column tie spacing = mid-height zone "A" (largest -> governs, shear is
# constant along a column).
import json
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
BAR=lambda d:f"DB{d}"      # bar name - to be matched to the rebar DB MIDAS offers for the chosen code
def lay(cover,db,n_layers,n_per=3,tie=10):
    d1=(cover+tie+db/2)/1000; out=[]
    for k in range(n_layers): out.append(dict(LAYER=k+1,dD=round(d1+k*(db+25)/1000,4),BAR_NUM=n_per,BAR_NAME1=BAR(db),BAR_NAME2=""))
    return out
def beam(cover,db,sup,mid,s_sup,s_mid):
    """sup/mid = (top layers, bottom layers) of 3 bars each"""
    v=[];sub=[]
    for sec,(t,b),s in (("I",sup,s_sup),("M",mid,s_mid),("J",sup,s_sup)):
        v.append(dict(SECTOR=sec,POS_TOP_LAYERS=lay(cover,db,t),POS_BOT_LAYERS=lay(cover,db,b)))
        sub.append(dict(SECTOR=sec,dSUB_BARNUM=2,SUB_BARNAME=BAR(10),dSUB_BARDIST=s,dSUB_BARANGLE=90))
    return dict(MEMBTYPE="BEAM",ENVTYPE=0,BEAM=dict(OPTION_IMJSAME=False,vMAIN=v,vSUB_BAR=sub))
def column(cover,db,p1,p2,s,legs_y,legs_z,tie=10):
    return dict(MEMBTYPE="COLUMN",ENVTYPE=0,COLM=dict(
        vLAYER=[dict(INDEX=1,dDc=round((cover+tie+db/2)/1000,4),vPOSITION=[dict(POSITION="P1",BAR_NUM=p1,BAR_NAME1=BAR(db),BAR_NAME2=""),
                                                                      dict(POSITION="P2",BAR_NUM=p2,BAR_NAME1=BAR(db),BAR_NAME2="")])],
        SUB_BAR=dict(SUBBAR_NAME=BAR(10),SUBBAR_DIST=s,SUBBAR_NUM=legs_y,SUBBAR_NAME_Y=BAR(10),SUBBAR_NAME_Z=BAR(10),SUBBAR_NUM_Y=legs_y,SUBBAR_NUM_Z=legs_z)))
# ---- schedule -> sections (vSIZE [H(z), B(y)]; pos1 = bars on the two faces parallel to local y incl. corners, pos2 = other two faces excl. corners)
R={
 # columns (S2-02).  101/105: 250x250 8-DB20 (3 per face)  103: 250(H) x 400(B) 12-DB20 (3 x 5)
 101:("C1 GF 250x250  8-DB20, ties DB10 @150 mid / @100 ends", column(40,20,6,2,0.15,2,2)),
 105:("C3 GF 250x250  8-DB20, ties DB10 @150 mid / @100 ends", column(40,20,6,2,0.15,2,2)),
 103:("C2 GF 250x400  12-DB20, ties 2-DB10 @200 mid / @100 ends", column(40,20,10,2,0.20,4,4)),
 102:("C1 FT 350x350  12-DB20, ties 3-DB10 @150 / @100", column(50,20,8,4,0.15,4,4)),
 106:("C3 FT 350x350  12-DB20, ties 3-DB10 @150 / @100", column(50,20,8,4,0.15,4,4)),
 104:("C2 FT 350x500  12-DB20, ties 2-DB10 @200 / @100", column(50,20,10,2,0.20,4,4)),
 # beams (S2-04): continuous = supports top 3+3 / bot 3 @150, mid top 3 / bot 3+3 @200
 201:("GB1 250x800 DB20 continuous", beam(50,20,(2,1),(1,2),0.15,0.20)),
 202:("GB1A 250x800 all span top 6-DB20 bot 3-DB20 @150", beam(50,20,(2,1),(2,1),0.15,0.15)),
 203:("GB1C 250x800 cantilever top 6-DB20 bot 3-DB20 @150", beam(50,20,(2,1),(2,1),0.15,0.15)),
 204:("B1 250x600 DB20 continuous", beam(40,20,(2,1),(1,2),0.15,0.20)),
 205:("B1A 250x600 all span top 6-DB20 bot 3-DB20 @150", beam(40,20,(2,1),(2,1),0.15,0.15)),
 206:("B1C 250x600 cantilever top 6-DB20 bot 3-DB20 @150", beam(40,20,(2,1),(2,1),0.15,0.15)),
 207:("B2 250x600 DB16 continuous", beam(40,16,(2,1),(1,2),0.15,0.20)),
 209:("B2A 250x600 = B2 (not in schedule, assumed)", beam(40,16,(2,1),(1,2),0.15,0.20)),
}
payload={"Assign":{str(k):v for k,(n,v) in R.items()}}
json.dump(payload,open(SC+"/rchk_payload.json","w"),indent=1)
json.dump({str(k):n for k,(n,v) in R.items()},open(SC+"/rchk_labels.json","w"),indent=1)
print("prepared /db/RCHK payload for sections:",list(payload["Assign"]))
for k,(n,v) in R.items():
    if v["MEMBTYPE"]=="BEAM":
        I=v["BEAM"]["vMAIN"][0]; M=v["BEAM"]["vMAIN"][1]
        f=lambda L:"+".join(f"{l['BAR_NUM']}" for l in L)+f"-{L[0]['BAR_NAME1']} (d {','.join(str(int(l['dD']*1000)) for l in L)})"
        print(f" {k} {n:48} I/J top {f(I['POS_TOP_LAYERS']):22} bot {f(I['POS_BOT_LAYERS']):16} | M top {f(M['POS_TOP_LAYERS']):16} bot {f(M['POS_BOT_LAYERS']):22} | s {v['BEAM']['vSUB_BAR'][0]['dSUB_BARDIST']}/{v['BEAM']['vSUB_BAR'][1]['dSUB_BARDIST']}")
    else:
        c=v["COLM"]; p=c["vLAYER"][0]
        print(f" {k} {n:48} P1 {p['vPOSITION'][0]['BAR_NUM']} + P2 {p['vPOSITION'][1]['BAR_NUM']} = {p['vPOSITION'][0]['BAR_NUM']+p['vPOSITION'][1]['BAR_NUM']} {p['vPOSITION'][0]['BAR_NAME1']}  Dc {int(p['dDc']*1000)}  ties {c['SUB_BAR']['SUBBAR_NAME']}@{c['SUB_BAR']['SUBBAR_DIST']} legs y/z {c['SUB_BAR']['SUBBAR_NUM_Y']}/{c['SUB_BAR']['SUBBAR_NUM_Z']}")
