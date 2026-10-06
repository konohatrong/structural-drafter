# -*- coding: utf-8 -*-
# Live-load classification per room zone (Ministerial Regulation B.E. 2566, clause 11) -> one sheet per floor.
# usage: python ll_plot.py <MAPI_KEY>
import sys, os, json, math, textwrap
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
plt.rcParams["font.family"]=["Leelawadee UI","DejaVu Sans"]
# zone -> (LL kg/m2, clause reference, basis note)
LL={
 "GB-TRUCK":(800,"ข้อ 11 กลุ่ม 7 (1) ลานจอดรถ – รถยนต์บรรทุกเปล่า / รถยนต์โดยสารอื่น","Fire trucks = trucks. Minimum 800; per ข้อ 12 check the loaded fire-truck wheel loads if heavier. No LL reduction (ข้อ 14)."),
 "GB-STAIR":(400,"ข้อ 11 กลุ่ม 7 (2) บันไดหนีไฟ ≥ บันไดของกลุ่มอาคาร (กลุ่ม 6 หอพัก (4) = 400)","Single stair serving the staff sleeping floor."),
 "GB-STORE":(500,"ข้อ 11 กลุ่ม 2 สำนักงาน (4) ห้องเก็บเอกสารและพัสดุ",""),
 "GB-PUMP":(500,"ข้อ 11 กลุ่ม 5 (1) พื้นที่เก็บของ (เทียบเท่า) + น้ำหนักเครื่องสูบน้ำเป็น นค. (ข้อ 10)","Plant room: not listed; engineering judgment."),
 "GB-WC":(250,"ข้อ 11 กลุ่ม 2 สำนักงาน (1) พื้นที่สำนักงาน","Toilet within office-type occupancy."),
 "GB-CCTV":(250,"ข้อ 11 กลุ่ม 2 สำนักงาน (1) พื้นที่สำนักงาน",""),
 "GB-DUTY":(250,"ข้อ 11 กลุ่ม 2 สำนักงาน (1) พื้นที่สำนักงาน",""),
 "GB-RADIO":(250,"ข้อ 11 กลุ่ม 2 สำนักงาน (1) พื้นที่สำนักงาน",""),
 "2F-CMD":(250,"ข้อ 11 กลุ่ม 2 สำนักงาน (1) พื้นที่สำนักงาน","Use 500 (กลุ่ม 2 (3) ห้องเมนเฟรมคอมพิวเตอร์) if server racks are installed."),
 "2F-DUTYOFF":(250,"ข้อ 11 กลุ่ม 2 สำนักงาน (1) พื้นที่สำนักงาน",""),
 "2F-ENFORCE":(250,"ข้อ 11 กลุ่ม 2 สำนักงาน (1) พื้นที่สำนักงาน",""),
 "2F-WCM":(250,"ข้อ 11 กลุ่ม 2 สำนักงาน (1) พื้นที่สำนักงาน","Toilet on the office floor."),
 "2F-WCF":(250,"ข้อ 11 กลุ่ม 2 สำนักงาน (1) พื้นที่สำนักงาน","Toilet on the office floor."),
 "2F-STAIRHALL":(400,"ข้อ 11 กลุ่ม 6 หอพัก (4) ห้องโถง บันได ช่องทางเดิน / กลุ่ม 7 (2)","Office would be 300; 400 governs (serves sleeping floor, escape route)."),
 "2F-CORR":(400,"ข้อ 11 กลุ่ม 6 หอพัก (4) ห้องโถง บันได ช่องทางเดิน","Office would be 300; 400 governs (escape route)."),
 "2F-LEDGE":(100,"ข้อ 11 กลุ่ม 7 (6) กันสาดคอนกรีต","Confirm no access; if an accessible balcony use 400."),
 "2F-CANOPY":(100,"ข้อ 11 กลุ่ม 7 (6) กันสาดคอนกรีต",""),
 "3F-REST":(200,"ข้อ 11 กลุ่ม 6 หอพัก (1) ห้องนอน ห้องนั่งเล่น ห้องน้ำ","Staff sleeping rooms."),
 "3F-WCM":(200,"ข้อ 11 กลุ่ม 6 หอพัก (1) ห้องนอน ห้องนั่งเล่น ห้องน้ำ",""),
 "3F-STAIRHALL":(400,"ข้อ 11 กลุ่ม 6 หอพัก (4) ห้องโถง บันได ช่องทางเดิน",""),
 "3F-ROOF2F":(100,"ข้อ 11 กลุ่ม 7 (6) กันสาดคอนกรีต (หลังคาคอนกรีตไม่มีผู้ใช้งาน)","Non-accessible concrete roof: 100 used (> หลังคา 50)."),
 "RF-TANK":(5000/9.80665,"ข้อ 12 น้ำหนักบรรทุกจรที่มากกว่าข้อ 11 เฉพาะส่วน (ถังเก็บน้ำ 2 x 1.5 ลบ.ม.)","5 kPa over the tank area (tanks + margin 0.3 m), as instructed; replaces the roof-deck 200 there."),
 "RF-DECK":(200,"ข้อ 11 กลุ่ม 7 (7) ดาดฟ้า",""),
 "RF-STAIRHALL":(400,"ข้อ 11 กลุ่ม 6 หอพัก (4) / กลุ่ม 7 (2) บันไดหนีไฟ",""),
 "RF-OVERHANG":(100,"ข้อ 11 กลุ่ม 7 (6) กันสาดคอนกรีต",""),
 "AR-ROOF":(100,"ข้อ 11 กลุ่ม 7 (6) กันสาดคอนกรีต (หลังคาคอนกรีตไม่มีผู้ใช้งาน)","Non-accessible concrete roof: 100 used (> หลังคา 50)."),
}
VC={5000/9.80665:"#3b1f5e",100:"#cfe3f3",200:"#8fd19e",250:"#f7e07e",300:"#f6c177",400:"#f28e5b",500:"#d9534f",800:"#8e2c6e"}
EN="--en" in sys.argv
SHORT={"GB-TRUCK":"Fire-truck parking","GB-STAIR":"Stair","GB-STORE":"Store","GB-PUMP":"Pump room","GB-WC":"Toilet","GB-CCTV":"CCTV room",
 "GB-DUTY":"Duty officer","GB-RADIO":"Radio room","2F-CMD":"Command room","2F-DUTYOFF":"Duty office","2F-ENFORCE":"Enforcement office",
 "2F-WCM":"Men's WC","2F-WCF":"Women's WC","2F-STAIRHALL":"Stair hall","2F-CORR":"Corridor","2F-LEDGE":"Ledge","2F-CANOPY":"Canopy",
 "3F-REST":"Staff rest rooms","3F-WCM":"Men's WC","3F-STAIRHALL":"Stair hall","3F-ROOF2F":"Roof slab","RF-TANK":"Water tanks",
 "RF-DECK":"Roof deck","RF-STAIRHALL":"Stair hall","RF-OVERHANG":"Overhang","AR-ROOF":"Annex roof"}
REF_EN={"GB-TRUCK":"Cl.11 Group 7(1) parking: empty trucks / other buses","GB-STAIR":"Cl.11 Group 7(2) fire-escape stair (>= stair of the building group, Group 6(4) = 400)",
 "GB-STORE":"Cl.11 Group 2(4) document & supply storage","GB-PUMP":"Cl.11 Group 5(1) storage area (equivalent); pumps as dead load (Cl.10)",
 "GB-WC":"Cl.11 Group 2(1) office area","GB-CCTV":"Cl.11 Group 2(1) office area","GB-DUTY":"Cl.11 Group 2(1) office area","GB-RADIO":"Cl.11 Group 2(1) office area",
 "2F-CMD":"Cl.11 Group 2(1) office area","2F-DUTYOFF":"Cl.11 Group 2(1) office area","2F-ENFORCE":"Cl.11 Group 2(1) office area","2F-WCM":"Cl.11 Group 2(1) office area",
 "2F-WCF":"Cl.11 Group 2(1) office area","2F-STAIRHALL":"Cl.11 Group 6(4) lobby, stair, corridor / Group 7(2)","2F-CORR":"Cl.11 Group 6(4) lobby, stair, corridor",
 "2F-LEDGE":"Cl.11 Group 7(6) concrete canopy","2F-CANOPY":"Cl.11 Group 7(6) concrete canopy","3F-REST":"Cl.11 Group 6(1) bedroom, living room, bathroom",
 "3F-WCM":"Cl.11 Group 6(1) bedroom, living room, bathroom","3F-STAIRHALL":"Cl.11 Group 6(4) lobby, stair, corridor","3F-ROOF2F":"Cl.11 Group 7(6) concrete canopy (non-accessible concrete roof)",
 "RF-TANK":"Cl.12 higher actual load (2 water tanks x 1.5 m3): 5 kPa","RF-DECK":"Cl.11 Group 7(7) roof deck","RF-STAIRHALL":"Cl.11 Group 6(4) / Group 7(2) fire-escape stair",
 "RF-OVERHANG":"Cl.11 Group 7(6) concrete canopy","AR-ROOF":"Cl.11 Group 7(6) concrete canopy (non-accessible concrete roof)"}
NAME={"GB":"GROUND FLOOR  +0.35","2F":"2ND FLOOR  +4.75","3F":"3RD FLOOR  +7.95","RF":"ROOF  +11.15","AR":"ANNEX ROOF  +3.95"}
Rm=json.load(open(SC+"/fs_rooms.json",encoding="utf-8"))
os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
from windload.midas.connection import connect; connect(sys.argv[1])
import midas_gen as mg
N=mg.MidasAPI("GET","/db/NODE",{})["NODE"]; E=mg.MidasAPI("GET","/db/ELEM",{})["ELEM"]
byL=defaultdict(list)
for e,z in Rm["plates"].items():
    L=Rm["zones"][z]["level"]; P=[(N[str(n)]["X"]*1000,N[str(n)]["Y"]*1000) for n in E[str(e)]["NODE"] if n]; byL[L].append((P,z))
summary=[]
for L,items in byL.items():
    zs=[k for k,v in Rm["zones"].items() if v["level"]==L and v["plates"]]
    fig=plt.figure(figsize=(17,10.5)); fig.patch.set_facecolor("white")
    ax=fig.add_axes([0.02,0.06,0.58,0.84])
    for P,z in items: ax.add_patch(Polygon(P,closed=True,fc=VC[LL[z][0]],ec="white",lw=0.2))
    xs=[p[0] for P,_ in items for p in P]; ys=[p[1] for P,_ in items for p in P]
    for x,n in [(0,"1"),(2250,"2"),(8750,"3"),(12750,"4"),(19250,"5"),(23550,"6"),(27250,"7")]:
        if min(xs)-500<=x<=max(xs)+500:
            ax.plot([x,x],[min(ys)-400,max(ys)+400],color="#888",lw=0.6,ls=(0,(8,4)),zorder=0)
            ax.add_patch(plt.Circle((x,max(ys)+1000),380,fc="white",ec="#333",zorder=5)); ax.text(x,max(ys)+1000,n,ha="center",va="center",fontsize=10,weight="bold",zorder=6)
    for y,n in [(0,"F"),(4000,"E"),(8000,"D"),(11000,"C"),(12000,"B"),(14300,"A")]:
        if min(ys)-500<=y<=max(ys)+500:
            ax.plot([min(xs)-400,max(xs)+400],[y,y],color="#888",lw=0.6,ls=(0,(8,4)),zorder=0)
            ax.add_patch(plt.Circle((min(xs)-1100,y),380,fc="white",ec="#333",zorder=5)); ax.text(min(xs)-1100,y,n,ha="center",va="center",fontsize=10,weight="bold",zorder=6)
    for z in zs:
        pts=[(sum(p[0] for p in P)/len(P),sum(p[1] for p in P)/len(P)) for P,zz in items if zz==z]
        cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts); b=min(pts,key=lambda p:math.dist(p,(cx,cy)))
        v=LL[z][0]; zz=Rm["zones"][z]
        ax.text(b[0],b[1],f"{(SHORT.get(z,zz['en']) if EN else zz['th'])}\n{v:.0f} kg/m²"+(f" ({v*9.80665/1000:.1f} kPa)" if z=="RF-TANK" else ""),ha="center",va="center",fontsize=8,weight="bold",zorder=9,
                bbox=dict(fc="white",ec="#444",lw=0.6,pad=0.3,alpha=0.93))
    for t in Rm["extra"].get(L,[]):
        for p in t["pts"]:
            ax.add_patch(plt.Circle(p,850,fc="none",ec="white",lw=1.8,ls=(0,(4,2)),zorder=8)); ax.text(p[0],p[1]+550,"TANK",ha="center",fontsize=7,color="white",weight="bold",zorder=9)
    ax.set_xlim(min(xs)-1800,max(xs)+900); ax.set_ylim(min(ys)-900,max(ys)+1700); ax.set_aspect("equal"); ax.axis("off")
    fig.text(0.02,0.955,f"LIVE LOAD PLAN  -  {NAME[L]}",fontsize=18,weight="bold")
    if EN: fig.text(0.02,0.927,"Ministerial Regulation on Structural Design and Materials of Building Structures B.E. 2566 (2023) - Clause 11 minimum live loads",fontsize=10,color="#444")
    else: fig.text(0.02,0.927,"กฎกระทรวง กำหนดการออกแบบโครงสร้างอาคารและลักษณะและคุณสมบัติของวัสดุที่ใช้ในงานโครงสร้างอาคาร พ.ศ. 2566  -  ข้อ 11 น้ำหนักบรรทุกจรขั้นต่ำ",fontsize=10,color="#444")
    # side table
    sx=fig.add_axes([0.62,0.06,0.37,0.84]); sx.axis("off"); sx.set_xlim(0,1); sx.set_ylim(0,1); yy=0.98
    sx.text(0,yy,"ZONE   /   LIVE LOAD   /   REGULATION",fontsize=10.5,weight="bold",va="top"); yy-=0.045
    for z in sorted(zs,key=lambda k:-LL[k][0]):
        v,ref,note=LL[z]; zz=Rm["zones"][z]
        sx.add_patch(plt.Rectangle((0,yy-0.022),0.035,0.03,fc=VC[v],ec="#555",lw=0.5))
        if EN: ref=REF_EN[z]; note=""
        sx.text(0.05,yy,(zz['en'].replace(" (confirm)","") if EN else f"{zz['th']}  ({zz['en']})"),fontsize=8.8,weight="bold",va="center")
        sx.text(0.05,yy-0.027,f"{v:.0f} kg/m² = {v*9.80665/1000:.2f} kN/m²     {zz['area']:.1f} m²",fontsize=8.5,va="center",color="#222")
        w=textwrap.fill(ref,70); sx.text(0.05,yy-0.05,w,fontsize=7.8,va="top",color="#444"); yy-=0.05+0.022*(w.count("\n")+1)
        if note:
            w=textwrap.fill("Note: "+note,78); sx.text(0.05,yy-0.004,w,fontsize=7.6,va="top",color="#a03020",style="italic"); yy-=0.024*(w.count("\n")+1)+0.004
        yy-=0.022
        summary.append((L,z,zz["th"],zz["en"],v,zz["area"],ref))
    fig.savefig(SC+f"/fs_LL_{L}{'_en' if EN else ''}.png",dpi=110,facecolor="white"); plt.close(fig); print("saved",f"fs_LL_{L}.png")
if not EN: json.dump({z:dict(LL=LL[z][0],ref=LL[z][1],note=LL[z][2]) for z in LL},open(SC+"/fs_LL.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
tot=sum(s[4]*s[5] for s in summary)/1000
print("total LL on slabs:",round(tot,1),"t")
