# -*- coding: utf-8 -*-
# East annex (grids 6-7 x F-D), roof RS1 at +3.95.  Drawn displaced on the 2F panel by (+2645, +7802).
# usage: python annex.py plot            -> fs_annex.json + fs_beams_AR.png + verification printout
#        python annex.py build <MAPI_KEY> -> writes nodes / column changes / beams / groups to MIDAS
import sys, json, math
sys.stdout.reconfigure(encoding="utf-8")
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
DXF=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
O,SH=91555,(2645,7802); Z=3.95; LD=6
SEC={"B1":204,"B2":207}
CM=json.load(open(SC+"/fs_colmodel.json"))
IDX={"F6":6,"F7":7,"E6":13,"E7":14,"D6":20}
XY={"F6":(23550,0),"F7":(27250,0),"E6":(23550,4000),"E7":(27250,4000),"D6":(23550,8000)}
cn={XY[g]:LD*1000+i for g,i in IDX.items()}

# ---------- analytical layout ----------
GB=json.load(open(SC+"/fs_beammodel.json"))["GB"]
curve=[tuple(e["a"]) for e in GB["elems"] if e.get("curve")]+[tuple(e["b"]) for e in GB["elems"] if e.get("curve")]
arc=[(27250,4000),(27250,4300),(27124,5258),(26754,6150),(26166,6916),(25400,7504),(24508,7874),(23550,8000)]
assert all(p in curve for p in arc), "GB curve points changed"
segs=[((23550,0),(27250,0),"B2","row F, labelled B2"),
      ((27250,0),(27250,4000),"B2","grid 7, labelled B2"),
      ((23550,4000),(27250,4000),"B2","row E, labelled B2"),
      ((23550,0),(23550,4000),"B2","grid 6, drawn solid, no label -> mark of 2F beam above"),
      ((23550,4000),(23550,8000),"B1","grid 6, drawn solid, no label -> mark of 2F beam above")]
segs+=[(a,b,"B2","curved edge, labelled B2") for a,b in zip(arc,arc[1:])]
new=sorted({p for a,b,*_ in segs for p in (a,b)}-set(cn),key=lambda p:(p[1],p[0]))
nid={p:LD*1000+101+i for i,p in enumerate(new)}; nid.update(cn)
els=sorted(segs,key=lambda s:((s[0][1]+s[1][1])/2,(s[0][0]+s[1][0])/2))
E=[dict(id=LD*10000+1001+k,a=list(a),b=list(b),i=nid[a],j=nid[b],mark=m,sect=SEC[m],note=n,
        len=round(math.dist(a,b)/1000,3)) for k,(a,b,m,n) in enumerate(els)]
# column changes
colnew=[]; colmod=[]
for g in ("F6","E6","D6"):                        # split GF->2F at +3.95
    i=IDX[g]; colmod.append((2000+i,2000+i,LD*1000+i)); colnew.append((LD*1000+i,LD*1000+i,3000+i,101,g))
for g in ("F7","E7"):                             # column stops under annex roof: top 4.75 -> 3.95
    i=IDX[g]; colmod.append((2000+i,2000+i,LD*1000+i))
deln=[3000+IDX[g] for g in ("F7","E7")]
D=dict(z=Z,colnodes={f"{p[0]/1000},{p[1]/1000}":v for p,v in cn.items()},newnodes={str(nid[p]):[p[0]/1000,p[1]/1000] for p in new},
       elems=E,colmod=colmod,colnew=colnew,delnodes=deln)

if sys.argv[1]=="plot":
    json.dump(D,open(SC+"/fs_annex.json","w"),indent=1)
    import ezdxf, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, logging; logging.disable(logging.WARNING)
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    from ezdxf.addons.drawing.config import Configuration, TextPolicy, ColorPolicy
    doc=ezdxf.readfile(DXF); msp=doc.modelspace()
    # ---- verification against the displaced DXF drawing ----
    dx=[]; labels=[]; sfl=[]
    for e in msp:
        t=e.dxftype()
        if t=="MLINE" and e.dxf.layer in("S-HID_BEAM","S-CONT_BEAM"):
            V=[(v.location.x-O-SH[0],v.location.y-SH[1]) for v in e.vertices]
            if all(22000<x<28500 and -500<y<8500 for x,y in V) and e.vertices[0].location.x-O>25000:
                half=e.dxf.scale_factor/2; s={0:-half,1:0,2:half}[e.dxf.justification]
                for a,b in zip(V,V[1:]):
                    L=math.dist(a,b); nx,ny=-(b[1]-a[1])/L,(b[0]-a[0])/L
                    dx.append(((a[0]+s*nx,a[1]+s*ny),(b[0]+s*nx,b[1]+s*ny),e.dxf.layer))
        if t=="TEXT" and e.dxf.text.strip() in("B1","B2","B1A","B2A","BX") and 25000<e.dxf.insert.x-O<33000 and 6500<e.dxf.insert.y<17500:
            labels.append((e.dxf.insert.x-O-SH[0],e.dxf.insert.y-SH[1],e.dxf.text.strip()))
        if t=="INSERT" and e.dxf.name=="Sym-SFL" and 25000<e.dxf.insert.x-O<33000 and 6500<e.dxf.insert.y<17500:
            sfl.append((round(e.dxf.insert.x-O-SH[0]),round(e.dxf.insert.y-SH[1]),[a.dxf.text for a in e.attribs]))
    def dseg(p,a,b):
        L2=(b[0]-a[0])**2+(b[1]-a[1])**2; t=max(0,min(1,((p[0]-a[0])*(b[0]-a[0])+(p[1]-a[1])*(b[1]-a[1]))/L2))
        return math.hypot(p[0]-a[0]-t*(b[0]-a[0]),p[1]-a[1]-t*(b[1]-a[1]))
    arcd=lambda p:abs(math.hypot(p[0]-23550,p[1]-4300)-3700) if p[1]>4250 else 1e9
    def near_dx(p): return min([dseg(p,a,b) for a,b,_ in dx]+[arcd(p)])
    def near_m(p): return min(dseg(p,e["a"],e["b"]) for e in E)
    unc=[(a,b,l) for a,b,l in dx if max(near_m((a[0]+(b[0]-a[0])*k/10,a[1]+(b[1]-a[1])*k/10)) for k in range(1,10))>150]
    nod=[e["id"] for e in E if max(near_dx((e["a"][0]+(e["b"][0]-e["a"][0])*k/10,e["a"][1]+(e["b"][1]-e["a"][1])*k/10)) for k in range(1,10))>150]
    lab=[]
    for x,y,t in labels:
        e=min(E,key=lambda e:dseg((x,y),e["a"],e["b"])); lab.append((t,e["id"],e["mark"],round(dseg((x,y),e["a"],e["b"]))))
    from collections import Counter
    deg=Counter([tuple(e["a"]) for e in E]+[tuple(e["b"]) for e in E])
    print(f"=== VERIFY ANNEX ROOF +{Z}: DXF straight beams {len(dx)} + curved beam | model beams {len(E)} | labels {len(labels)}")
    print(f"[1] DXF beams NOT in model: {unc}")
    print(f"[2] model beams with NO DXF beam: {nod}")
    print(f"[3] labels (text, nearest beam, its mark, distance mm): {lab}  mismatches: {[l for l in lab if l[0]!=l[2]]}")
    print(f"[4] free ends: {[p for p,c in deg.items() if c==1 and p not in cn]}   column nodes used {sum(1 for p in cn if deg[p])}/5")
    print(f"[5] SFL: {sfl}")
    print(f"    DXF grid-6 beams layer: {[l for a,b,l in dx if abs(a[0]-23550)<5]}")
    # ---- sheet ----
    cfg=Configuration(text_policy=TextPolicy.IGNORE,color_policy=ColorPolicy.CUSTOM,custom_fg_color="#c9ced4")
    fig=plt.figure(figsize=(15,10)); fig.patch.set_facecolor("white")
    ax=fig.add_axes([0.03,0.07,0.62,0.83])
    Frontend(RenderContext(doc),MatplotlibBackend(ax),config=cfg).draw_layout(msp,finalize=False)
    ox,oy=O+SH[0],SH[1]                                   # model -> displaced drawing coordinates
    for k,x in CM["GX"].items():
        if x<20: continue
        X=ox+x*1000; ax.plot([X,X],[oy-1500,oy+9600],color="#7f8c99",lw=0.6,ls=(0,(10,4,2,4)),zorder=2)
        ax.add_patch(plt.Circle((X,oy+10200),330,fc="white",ec="#222",zorder=8)); ax.text(X,oy+10200,k,ha="center",va="center",fontsize=11,weight="bold",zorder=9)
    for k,y in CM["GY"].items():
        if y>8.5: continue
        Y=oy+y*1000; ax.plot([ox+21500,ox+29000],[Y,Y],color="#7f8c99",lw=0.6,ls=(0,(10,4,2,4)),zorder=2)
        ax.add_patch(plt.Circle((ox+20900,Y),330,fc="white",ec="#222",zorder=8)); ax.text(ox+20900,Y,k,ha="center",va="center",fontsize=11,weight="bold",zorder=9)
    COL={"B1":"#1f5fbf","B2":"#8e44ad"}
    for e in E:
        (x1,y1),(x2,y2)=e["a"],e["b"]; c=COL[e["mark"]]; inf="no label" in e["note"]
        ax.plot([ox+x1,ox+x2],[oy+y1,oy+y2],color=c,lw=3.4,solid_capstyle="butt",zorder=5,ls="-" if not inf else (0,(4,1.5)))
        ang=math.degrees(math.atan2(y2-y1,x2-x1)); ang=ang-180 if ang>90 else (ang+180 if ang<=-90 else ang)
        nx,ny=-math.sin(math.radians(ang)),math.cos(math.radians(ang)); off=-260 if abs(x1-23550)<5 and abs(x2-23550)<5 else 230
        ax.text(ox+(x1+x2)/2+nx*off,oy+(y1+y2)/2+ny*off,f"{e['id']}  {e['mark']} {e['len']:.2f}",fontsize=6.5,color=c,rotation=ang,
                ha="center",va="center",zorder=7,bbox=dict(fc="#fff3b0" if inf else "white",ec="none",pad=0.3,alpha=0.9))
    for p,i in cn.items():
        ax.plot(ox+p[0],oy+p[1],"s",ms=9,color="#222",zorder=6)
        ax.text(ox+p[0]+(250 if p[0]>25000 else -250),oy+p[1]-330,str(i),fontsize=7.5,ha="left" if p[0]>25000 else "right",weight="bold",zorder=9)
    for p in new:
        ax.plot(ox+p[0],oy+p[1],"o",ms=6,mfc="white",mec="#c0392b",mew=1.6,zorder=7)
        ax.text(ox+p[0]-200,oy+p[1]-300,f"{nid[p]}",fontsize=6.5,color="#c0392b",ha="right",zorder=9)
    ax.set_xlim(ox+20300,ox+29200); ax.set_ylim(oy-1600,oy+10700); ax.set_aspect("equal"); ax.axis("off")
    fig.text(0.03,0.95,f"EAST ANNEX ROOF   Z = +{Z:.2f} m   (grids 6–7 × F–D)",fontsize=16,weight="bold")
    fig.text(0.03,0.925,"Analytical beams on the annex plan as drawn in the DXF (shown in its displaced position on the 2F sheet).",fontsize=9.5,color="#444")
    # elevation sketch of column changes
    ex=fig.add_axes([0.68,0.52,0.30,0.36]); ex.set_title("Columns on grids 6 and 7 (elevation)",fontsize=10,weight="bold",loc="left")
    for k,(g,x) in enumerate([("F6/E6/D6",0),("F7/E7",1)]):
        top=4.75 if x==0 else 3.95
        ex.plot([x,x],[-1.0,top],color="#222",lw=4)
        if x==1: ex.plot([x,x],[3.95,4.75],color="#c0392b",lw=4,ls=":"); ex.text(x+0.06,4.35,"removed\n(3.95→4.75)",fontsize=7.5,color="#c0392b",va="center")
        ex.text(x,-1.45,g,ha="center",fontsize=9,weight="bold")
    ex.plot([-0.35,1.25],[3.95,3.95],color="#8e44ad",lw=2.5); ex.text(1.27,3.95,"annex roof +3.95",va="center",fontsize=8,color="#8e44ad")
    ex.plot([-0.35,0],[4.75,4.75],color="#1f5fbf",lw=2.5); ex.text(-0.37,4.75,"2F +4.75",va="center",ha="right",fontsize=8,color="#1f5fbf")
    ex.plot([-0.35,1.25],[0.35,0.35],color="#555",lw=1.5); ex.text(1.27,0.35,"GB +0.35",va="center",fontsize=8)
    ex.plot(0,3.95,"o",ms=7,mfc="white",mec="#c0392b",mew=2); ex.text(0.06,3.75,"new node\n(split)",fontsize=7.5,color="#c0392b",va="top")
    ex.set_xlim(-1.1,2.2); ex.set_ylim(-1.8,5.3); ex.axis("off")
    sx=fig.add_axes([0.68,0.07,0.30,0.42]); sx.axis("off"); sx.set_xlim(0,1); sx.set_ylim(0,1)
    cnt=Counter(e["mark"] for e in E); yy=0.98
    sx.text(0,yy,"BEAMS",fontsize=11,weight="bold",va="top"); yy-=0.07
    for m in cnt:
        sx.plot([0,0.08],[yy,yy],color=COL[m],lw=4); sx.text(0.11,yy,f"{m}  250×600  sect {SEC[m]}  × {cnt[m]}",fontsize=9.5,va="center"); yy-=0.06
    sx.text(0,yy,f"Beams {E[0]['id']}–{E[-1]['id']} · column nodes 6006/6007/6013/6014/6020\ncurve nodes {min(nid[p] for p in new)}–{max(nid[p] for p in new)}",fontsize=8.5,va="top"); yy-=0.11
    import textwrap
    notes=["Column symbols on D6, E6, F6, E7, F7 are all 'column stop under': grid 6 stops under 2F (+4.75), grid 7 stops under the annex roof (+3.95).",
           "Curved edge = same arc and 6 chords as the ground beam below.",
           "Dashed on grid 6 (yellow tags): drawn as a solid beam line with no label on the annex plan. Modelled as a beam at +3.95 so the annex roof has a support line on grid 6 — needs your decision.",
           "Slab RS1 +3.95 (two panels, E–F and D–E)."]
    for n in notes:
        w=textwrap.fill("• "+n,62); sx.text(0,yy,w,fontsize=8.5,va="top"); yy-=0.055*(w.count("\n")+1)+0.02
    fig.savefig(SC+"/fs_beams_AR.png",dpi=110,facecolor="white"); print("saved fs_beams_AR.png")

if sys.argv[1]=="build":
    import os
    D=json.load(open(SC+"/fs_annex.json"))
    os.chdir("C:/990 - Developing software/midas API/pilot project/wind load generator"); sys.path.insert(0,"src")
    from windload.midas.connection import connect; connect(sys.argv[2])
    import midas_gen as mg
    def G(ep,k): r=mg.MidasAPI("GET",ep,{}).get(k,{}); return r if isinstance(r,dict) else {}
    def PUT(ep,body):
        r=mg.MidasAPI("PUT",ep,body); ok=isinstance(r,dict) and "error" not in r and "message" not in r
        print(f"PUT {ep:10} {'OK' if ok else r}"); return ok
    nodes=G("/db/NODE","NODE"); elem=G("/db/ELEM","ELEM"); grup=G("/db/GRUP","GRUP"); sect=G("/db/SECT","SECT")
    json.dump({"NODE":nodes,"ELEM":elem,"GRUP":grup},open(SC+"/midas_backup_before_annex.json","w"))
    # ---- pre-checks ----
    cnodes=list(D["colnodes"].values()); nn={int(k):v for k,v in D["newnodes"].items()}
    allnew=cnodes+list(nn); newel=[e["id"] for e in D["elems"]]+[c[0] for c in D["colnew"]]
    uses=lambda n:[k for k,v in elem.items() if n in v["NODE"][:2]]
    chk={"node ID clash":[i for i in allnew if str(i) in nodes],
         "elem ID clash":[i for i in newel if str(i) in elem],
         "missing sections":sorted({e["sect"] for e in D["elems"]}-{int(k) for k in sect}),
         "column elems to modify missing":[m[0] for m in D["colmod"] if str(m[0]) not in elem],
         "nodes to delete used elsewhere":{n:uses(n) for n in D["delnodes"] if set(uses(n))-{"2007","2014"}}}
    for m in D["colmod"]:
        e=elem.get(str(m[0]))
        if e and not (abs(nodes[str(e["NODE"][1])]["Z"]-4.75)<1e-6): chk.setdefault("column top not at +4.75",[]).append(m[0])
    print("pre-check:",chk)
    if any(chk.values()): sys.exit("ABORT: pre-check failed")
    # ---- nodes ----
    XYc={v:k for k,v in D["colnodes"].items()}
    PUT("/db/NODE",{"Assign":{**{str(n):{"X":float(XYc[n].split(",")[0]),"Y":float(XYc[n].split(",")[1]),"Z":D["z"]} for n in cnodes},
                              **{str(i):{"X":x,"Y":y,"Z":D["z"]} for i,(x,y) in nn.items()}}})
    # ---- columns: re-point tops, add upper stubs ----
    mod={}
    for eid,_,newj in D["colmod"]:
        e=dict(elem[str(eid)]); e["NODE"]=list(e["NODE"]); e["NODE"][1]=newj; mod[str(eid)]=e
    for eid,i,j,s,g in D["colnew"]:
        e=dict(elem[str(2000+eid%1000)]); e["NODE"]=list(e["NODE"]); e["NODE"][0]=i; e["NODE"][1]=j; e["SECT"]=s; mod[str(eid)]=e
    PUT("/db/ELEM",{"Assign":mod})
    # ---- delete orphaned 2F nodes of F7/E7 (one at a time, count-checked) ----
    for n in D["delnodes"]:
        before=len(G("/db/NODE","NODE")); r=mg.MidasAPI("DELETE",f"/db/NODE/{n}",{}); after=len(G("/db/NODE","NODE"))
        print(f"DELETE node {n}: {before} -> {after}", "OK" if after==before-1 else f"UNEXPECTED {r}")
        if after!=before-1: sys.exit("STOP: node delete did not behave as expected (backup saved)")
    # ---- beams ----
    PUT("/db/ELEM",{"Assign":{str(e["id"]):{"TYPE":"BEAM","MATL":1,"SECT":e["sect"],"NODE":[e["i"],e["j"]],"ANGLE":0,"STYPE":0} for e in D["elems"]}})
    # ---- groups ----
    stubs=[c[0] for c in D["colnew"]]; upd={}
    for k,gp in grup.items():
        el=gp.get("E_LIST",[]); nl=[n for n in gp.get("N_LIST",[]) if n not in D["delnodes"]]
        add=[s for s in stubs if 2000+s%1000 in el]                     # stub joins every group its parent column is in
        addn=[c for c in cnodes if 2000+c%1000 in el] if nl else []    # node groups that hold the GF->2F column
        if add or nl!=gp.get("N_LIST",[]) or addn:
            g2=dict(gp); g2["E_LIST"]=sorted(set(el+add)); g2["N_LIST"]=sorted(set(nl+addn)); upd[k]=g2
    upd["12"]={"NAME":"BEAM_AR","P_TYPE":0,"N_LIST":sorted(cnodes+list(nn)),"E_LIST":sorted(e["id"] for e in D["elems"])}
    PUT("/db/GRUP",{"Assign":upd}); print("groups updated:",{k:v["NAME"] for k,v in upd.items()})
    # ---- verify ----
    nodes=G("/db/NODE","NODE"); elem=G("/db/ELEM","ELEM"); grup=G("/db/GRUP","GRUP")
    Zt=lambda e:(nodes[str(elem[str(e)]["NODE"][0])]["Z"],nodes[str(elem[str(e)]["NODE"][1])]["Z"])
    print("\nVERIFY columns (Z bottom -> top):")
    for g,i in IDX.items():
        segs=[(e,Zt(e)) for e in (2000+i,LD*1000+i) if str(e) in elem]; print(f"   {g}: {segs}")
    bad=[e["id"] for e in D["elems"] if str(e["id"]) not in elem or
         abs(math.dist(*[(nodes[str(n)]["X"],nodes[str(n)]["Y"],nodes[str(n)]["Z"]) for n in elem[str(e["id"])]["NODE"][:2]])-e["len"])>1e-3]
    print(f"   beams written {sum(str(e['id']) in elem for e in D['elems'])}/{len(D['elems'])}  length/position mismatches {bad}")
    print(f"   nodes 3007/3014 gone: {all(str(n) not in nodes for n in D['delnodes'])}")
    print(f"   totals: nodes {len(nodes)}  elements {len(elem)}")
    for k,gp in sorted(grup.items(),key=lambda x:int(x[0])): print(f"   group {k:>2} {gp['NAME']:12} elems {len(gp.get('E_LIST',[])):3} nodes {len(gp.get('N_LIST',[])):3}")
