# -*- coding: utf-8 -*-
# Building B (Fire Station) calculation report - follows docs/CALC_REPORT_GENERATION.md, plus RC member design pages.
import sys, os, json, shutil, re
sys.stdout.reconfigure(encoding="utf-8")
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)
TPL=r"G:\My Drive\Works\##Calculation Report Template\20230910 - Calculation Report Template.docx"
OUTDIR=r"C:\Workspace\##2026\20260917 - Samutsongkram\calculation report\Building B"
OUT=os.path.join(OUTDIR,sys.argv[1] if len(sys.argv)>1 else "Structural Calculation Report - Building B.docx")
B=json.load(open(SC+"/B_data.json")); E=json.load(open(SC+"/elf_B.json"))
RM=json.load(open(SC+"/fs_rooms.json",encoding="utf-8")); LLJ=json.load(open(SC+"/fs_LL.json",encoding="utf-8"))
IMG=SC+"/Bimg"
def tot(lc,c): return sum(float(r[c]) for r in B["react"][lc])
T={lc:(tot(lc,"FX"),tot(lc,"FY"),tot(lc,"FZ")) for lc in B["react"]}

# ---------- template: copy, clear body, keep sectPr + header/footer ----------
shutil.copyfile(TPL,OUT); doc=Document(OUT); body=doc.element.body; sectPr=body.find(qn('w:sectPr'))
for ch in list(body):
    if ch.tag!=qn('w:sectPr'): body.remove(ch)
for tp in sectPr.findall(qn('w:titlePg')): sectPr.remove(tp)
for hr in sectPr.findall(qn('w:headerReference')): sectPr.remove(hr)
hr=OxmlElement('w:headerReference'); hr.set(qn('w:type'),'default'); hr.set(qn('r:id'),'rId8'); sectPr.insert(0,hr)
foot=next((rid for rid,rel in doc.part.rels.items() if 'footer' in rel.reltype),None)
if foot:
    for fr in sectPr.findall(qn('w:footerReference')): sectPr.remove(fr)
    fr=OxmlElement('w:footerReference'); fr.set(qn('w:type'),'default'); fr.set(qn('r:id'),foot); sectPr.insert(1,fr)
styles={s.name for s in doc.styles}; has=lambda n:n in styles

# ---------- helpers ----------
def para(text="",style=None,bold=False,size=None,align=None,italic=False):
    p=doc.add_paragraph(style=style if (style and has(style)) else None)
    if align is not None: p.alignment=align
    if text:
        r=p.add_run(text); r.bold=bold; r.italic=italic
        if size: r.font.size=Pt(size)
    return p
def body_(t): return para(t,style="Body Text")
FIGN=[0]
def caption(text):
    FIGN[0]+=1; cp=doc.add_paragraph(style="Caption" if has("Caption") else None); cp.alignment=WD_ALIGN_PARAGRAPH.CENTER
    cp.add_run("Figure "); fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),r' SEQ Figure \* ARABIC ')
    r=OxmlElement('w:r'); t=OxmlElement('w:t'); t.text=str(FIGN[0]); r.append(t); fld.append(r); cp._p.append(fld); cp.add_run("  "+text)
def figure(path,cap,width=6.2):
    if not os.path.exists(path): para(f"[missing image {os.path.basename(path)}]",italic=True); return
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(path,width=Inches(width)); caption(cap)
def page_break(): doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
def shade(cell,hexc):
    tcPr=cell._tc.get_or_add_tcPr(); sh=OxmlElement('w:shd'); sh.set(qn('w:val'),'clear'); sh.set(qn('w:fill'),hexc); tcPr.append(sh)
def set_cell(cell,text,bold=False,align='left',size=13,white=False):
    cell.text=""; p=cell.paragraphs[0]
    p.alignment={'left':WD_ALIGN_PARAGRAPH.LEFT,'center':WD_ALIGN_PARAGRAPH.CENTER,'right':WD_ALIGN_PARAGRAPH.RIGHT}[align]
    r=p.add_run(text); r.bold=bold; r.font.size=Pt(size); r.font.name="TH SarabunPSK"; r._element.rPr.rFonts.set(qn('w:cs'),"TH SarabunPSK")
    if white: r.font.color.rgb=RGBColor(255,255,255)
def table(headers,rows,widths=None,totals=None,size=13):
    t=doc.add_table(rows=1,cols=len(headers)); t.style='Table Grid' if has('Table Grid') else None; t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for j,h in enumerate(headers): set_cell(t.rows[0].cells[j],h,bold=True,align='center',size=size,white=True); shade(t.rows[0].cells[j],"305496")
    for row in rows:
        c=t.add_row().cells
        for j,v in enumerate(row): set_cell(c[j],str(v),align='left' if j==0 else 'center',size=size)
    if totals:
        c=t.add_row().cells
        for j,v in enumerate(totals): set_cell(c[j],str(v),bold=True,align='left' if j==0 else 'center',size=size); shade(c[j],"D9E1F2")
    if widths:
        for j,w in enumerate(widths):
            for row in t.rows: row.cells[j].width=Inches(w)
    para(); return t
def h1(t): return doc.add_paragraph(t,style="Heading 1" if has("Heading 1") else None)
def h2(t): return doc.add_paragraph(t,style="Heading 2" if has("Heading 2") else None)
def bullet(t): return doc.add_paragraph(t,style="List Bullet" if has("List Bullet") else None)
def tof():
    doc.add_paragraph("Table of Figures",style="TOC Heading" if has("TOC Heading") else ("Heading 1" if has("Heading 1") else None))
    p=doc.add_paragraph()
    def run(kind=None,txt=None,instr=None):
        r=OxmlElement('w:r')
        if kind: fc=OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'),kind); r.append(fc)
        if instr is not None: it=OxmlElement('w:instrText'); it.set(qn('xml:space'),'preserve'); it.text=instr; r.append(it)
        if txt is not None: tt=OxmlElement('w:t'); tt.set(qn('xml:space'),'preserve'); tt.text=txt; r.append(tt)
        p._p.append(r)
    run('begin'); run(instr=r' TOC \h \z \c "Figure" '); run('separate'); run(txt='Right-click → Update Field to build the list of figures.'); run('end')
f1=lambda v:f"{v:,.1f}"

# ==================== CONTENT ====================
para("Building B – Fire Station",bold=True,size=20,align=WD_ALIGN_PARAGRAPH.CENTER)
para("Finite Element Analysis and RC Member Design (MIDAS GEN NX)",bold=True,size=16,align=WD_ALIGN_PARAGRAPH.CENTER)
para(); tof(); page_break()

# 1 MODEL
h1("1. Structural Model")
body_("Building B is a three-storey reinforced-concrete moment-frame building (fire station) with a single-storey annex. "
      "The structure is modelled in MIDAS GEN NX with beam elements for columns and beams and thick-plate elements for the floor slabs. "
      "Columns stand on pile caps at −1.00 m (fixed supports). Column centrelines are placed on the grid intersections; slabs are modelled "
      "at the level of their supporting beams, meshed at 0.50 m with the boundary beams split at the mesh nodes.")
c=B["counts"]; cols=sum(1 for _ in range(0))
table(["Item","Value"],[
    ["Nodes",f"{c['nodes']:,}"],["Elements (total)",f"{c['elems']:,}"],
    ["  Beam elements (columns, beams)",f"{c['beam']:,}"],["  Plate elements (slabs)",f"{c['plate']:,}"],
    ["Levels","Base −1.00 · GF +0.35 · Annex roof +3.95 · 2F +4.75 · 3F +7.95 · Roof +11.15 m"],
    ["Supports",f"{len(B['sup'])} fixed supports at pile caps (−1.00 m)"],
    ["Columns","C1 250×250, C2 250×400, C3 250×250 (footing stubs 350×350 / 350×500)"],
    ["Beams","GB1/GB1A/GB1C 250×800; B1/B1A/B1C/B2/B2A 250×600"],
    ["Slabs","GS1 200 mm (ground); S1, S1C, RS1 180 mm"],
    ["Concrete","C280 (f'c = 27.5 MPa)"],["Reinforcement","SD40 (fy = 390 MPa), main bars and stirrups"],
    ["Analysis","Linear static; RC design to ACI 318M-14 (MIDAS GEN NX)"]],widths=[2.4,4.2])
figure(IMG+"/geom_iso.png","3D structural model – isometric view")
figure(IMG+"/geom_front.png","Structural model – front elevation")
figure(IMG+"/geom_side.png","Structural model – side elevation")

# 2 LOADS
page_break(); h1("2. Design Loads")
h2("2.1 Dead load (DL) and superimposed dead load (SDL)")
body_(f"DL is the self-weight of all members, generated by MIDAS (total {f1(T['DL(ST)'][2])} kN). "
      f"SDL of 2.50 kN/m² (finishes, ceiling and services) is applied as a uniform pressure on every slab plate (total {f1(T['SDL(ST)'][2])} kN).")
h2("2.2 Live load (LL)")
body_("Live loads follow the Ministerial Regulation on Structural Design and Materials of Building Structures B.E. 2566 (2023), Clause 11 "
      "(minimum live loads), with Clause 12 applied where the actual load is higher. Room functions were taken from the architectural "
      "floor plans and mapped onto the slab plates; each zone is loaded with a uniform pressure. No live-load reduction is applied (Clause 13/14).")
rows=[]; LVN={"GB":"Ground +0.35","2F":"2F +4.75","3F":"3F +7.95","RF":"Roof +11.15","AR":"Annex roof +3.95"}
REF={"GB-TRUCK":"Cl.11 G7(1) parking – trucks","GB-STAIR":"Cl.11 G7(2) fire-escape stair","GB-STORE":"Cl.11 G2(4) storage","GB-PUMP":"Cl.11 G5(1) storage (equiv.)",
     "2F-STAIRHALL":"Cl.11 G6(4) hall/stair","2F-CORR":"Cl.11 G6(4) corridor","3F-STAIRHALL":"Cl.11 G6(4) hall/stair","RF-STAIRHALL":"Cl.11 G6(4)/G7(2)",
     "3F-REST":"Cl.11 G6(1) bedrooms","3F-WCM":"Cl.11 G6(1) bathroom","RF-DECK":"Cl.11 G7(7) roof deck","RF-TANK":"Cl.12 tank area (5 kPa)"}
for z,v in RM["zones"].items():
    q=LLJ[z]["LL"]; ref=REF.get(z,"Cl.11 G7(6) concrete canopy" if q==100 else "Cl.11 G2(1) office area")
    rows.append([LVN[v["level"]],v["en"].replace(" (confirm)",""),f"{q:.0f}",f"{q*9.80665/1000:.2f}",f"{v['area']:.1f}",ref])
table(["Level","Area / room","kg/m²","kN/m²","m²","Regulation"],rows,widths=[1.0,2.1,0.55,0.55,0.55,1.85],size=11,
      totals=["Total","","","",f"{sum(v['area'] for v in RM['zones'].values()):.1f}",f"ΣLL = {f1(T['LL(ST)'][2])} kN"])
for L,nm in (("GB","ground floor +0.35"),("2F","2nd floor +4.75"),("3F","3rd floor +7.95"),("RF","roof +11.15"),("AR","annex roof +3.95")):
    figure(SC+f"/fs_LL_{L}_en.png",f"Live-load plan – {nm}")
h2("2.3 Seismic load")
body_(f"Equivalent static seismic loads Ex and Ey are applied in MIDAS to DPT 1301/1302-61, with the seismic weight from "
      f"1.0 DL + 1.0 SDL + 0.25 LL (Loads-to-Masses). Base shear from the analysis: {E['Vanal']:.1f} kN in each direction. The ELF calculation is given in Section 6.")
h2("2.4 Load combinations")
body_("Load combinations follow the same Ministerial Regulation: Clause 7 (strength design, used for RC design) and Clause 6 (service, "
      "used for foundation loads and deflection). Dead load D = DL + SDL; seismic E = ±Ex, ±Ey.")
crow=[[n,d.split("  (")[0],d.split("(")[-1].rstrip(")") if "(cl" in d else "", " + ".join(f"{f:g}{c}" for c,f in t).replace("+ -","− ")] for n,(d,t) in B["lcom"].items()]
table(["Name","Combination","Clause","Factors in model"],crow,widths=[0.55,2.3,0.8,3.0],size=11)

# 3 BEHAVIOUR
page_break(); h1("3. Model Behaviour Verification")
D=B["disp"]
body_(f"Displacement contours with the deformed shape confirm that the model is connected and carries load correctly. Under the service gravity "
      f"combination S1 (D + L) the maximum vertical deflection is {D['S1(CB)']['max']*1000:.1f} mm. Under the seismic load cases the structure sways "
      f"smoothly over its height, with a maximum lateral displacement of {D['Ex(ST)']['max']*1000:.1f} mm in X and {D['Ey(ST)']['max']*1000:.1f} mm in Y.")
figure(IMG+"/disp_S1.png","Vertical displacement contour (D_Z) with deformed shape – service combination S1 (D + L)")
figure(IMG+"/disp_S1_side.png","Vertical displacement contour (D_Z) with deformed shape – S1, elevation")
figure(IMG+"/disp_Ex.png","Lateral displacement contour (D_X) with deformed shape – seismic Ex")
figure(IMG+"/disp_Ey.png","Lateral displacement contour (D_Y) with deformed shape – seismic Ey")

# 4 REACTIONS
page_break(); h1("4. Support Reactions – Gravity")
body_(f"Base reactions at the {len(B['sup'])} supports. Combination values are taken from the load combinations stored in the model. Units: kN.")
table(["Load case / combination","ΣF_X","ΣF_Y","ΣF_Z"],[
    ["DL – self weight",*[f1(x) for x in T['DL(ST)']]],["SDL – superimposed dead",*[f1(x) for x in T['SDL(ST)']]],
    ["LL – live",*[f1(x) for x in T['LL(ST)']]],["S1 – service D + L",*[f1(x) for x in T['S1(CB)']]],
    ["U1 – 1.4D + 1.7L (Cl.7(1))",*[f1(x) for x in T['U1(CB)']]]],widths=[3.0,1.2,1.2,1.4])
h2("Reaction at each support (kN)")
def rz(lc,n): return next(float(r["FZ"]) for r in B["react"][lc] if int(r["Node"])==n)
rows=[]; s1=u1=0
for n in sorted(B["sup"],key=lambda k:(B["sup"][k][1],B["sup"][k][0])):
    x,y,z=B["sup"][n]; a=rz("S1(CB)",int(n)); b=rz("U1(CB)",int(n)); s1+=a; u1+=b
    rows.append([f"N{n}",f"{x:.2f}",f"{y:.2f}",f"{rz('DL(ST)',int(n))+rz('SDL(ST)',int(n)):.1f}",f"{rz('LL(ST)',int(n)):.1f}",f"{a:.1f}",f"{b:.1f}"])
table(["Support","X (m)","Y (m)","D = DL+SDL","LL","S1 (D+L)","U1"],rows,widths=[0.8,0.75,0.75,1.1,0.9,1.0,1.0],size=11,
      totals=[f"TOTAL ({len(rows)})","","",f1(T['DL(ST)'][2]+T['SDL(ST)'][2]),f1(T['LL(ST)'][2]),f1(s1),f1(u1)])
figure(IMG+"/react_S1.png","Support reactions with values – service combination S1, vertical F_Z (kN)")
figure(IMG+"/react_U1.png","Support reactions with values – factored combination U1, vertical F_Z (kN)")

# 5 LATERAL
page_break(); h1("5. Lateral Analysis – Seismic")
Vx=abs(T['Ex(ST)'][0]); Vy=abs(T['Ey(ST)'][1])
table(["Direction","Base shear V (kN)","Max lateral displacement (mm)","At roof +11.15 (mm)"],
      [["Ex (X)",f1(Vx),f"{D['Ex(ST)']['max']*1000:.1f}",f"{D['Ex(ST)']['per']['Roof']*1000:.1f}"],
       ["Ey (Y)",f1(Vy),f"{D['Ey(ST)']['max']*1000:.1f}",f"{D['Ey(ST)']['per']['Roof']*1000:.1f}"]],widths=[1.2,1.6,2.1,1.7])
h2("Storey drift")
Cd=4.5; I=E["I"]
body_(f"Storey drift is the relative lateral displacement of the two ends of each column divided by its height; the largest value over all "
      f"columns of the storey is reported. The design drift is Δ = Cd·δe/I with Cd = {Cd} (intermediate RC moment frame) and I = {I:.2f}; "
      f"the allowable storey drift of DPT 1301/1302 is 0.020·hsx for risk categories I–II (0.015 for III, 0.010 for IV).")
LBL={"-1.00 to +0.35":"Base → GF","+0.35 to +3.95":"GF → Annex roof","+0.35 to +4.75":"GF → 2F","+3.95 to +4.75":"Annex roof → 2F","+4.75 to +7.95":"2F → 3F","+7.95 to +11.15":"3F → Roof"}
rows=[]
for k in ["+7.95 to +11.15","+4.75 to +7.95","+0.35 to +4.75","+0.35 to +3.95","-1.00 to +0.35"]:
    for lc,dn in (("Ex(ST)","X"),("Ey(ST)","Y")):
        d=E["drift"][lc][k]; des=Cd*d["ratio"]/I
        rows.append([f"{LBL[k]} ({dn})",f"{d['h']:.2f}",f"{d['dmm']:.2f}",f"{100*d['ratio']:.3f}",f"{100*des:.2f}","2.00",("OK" if des<=0.02 else "Exceeds")])
table(["Storey (direction)","h (m)","δe (mm)","δe/h (%)","Cd·δe/(I·h) (%)","Allow. (%)","Check"],rows,widths=[1.8,0.6,0.75,0.8,1.1,0.8,0.75],size=11)

# 6 ELF
page_break(); h1("6. Seismic – Equivalent Lateral Force (ELF) Calculation")
body_("The base shear is V = Cs·W with Cs = Sa·I/R (minimum 0.01), using the seismic parameters entered in the MIDAS model (DPT 1301/1302-61).")
h2("(a) Design seismic parameters (as entered in the model)")
table(["Parameter","Value"],[
    ["Code","DPT 1301/1302-61 (MIDAS: DPT.1301/1302-61:2018)"],["Mapped Ss / S1","0.75 g / 0.30 g"],["Site coefficients Fa / Fv","1.2 / 1.8"],
    ["S_DS = (2/3)·Fa·Ss",f"{E['SDS']:.2f} g"],["S_D1 = (2/3)·Fv·S1",f"{E['SD1']:.2f} g"],
    ["Height H (−1.00 → +11.15)",f"{E['H']:.2f} m"],["Period T = 0.02·H",f"{E['T']:.3f} s"],["Ts = S_D1/S_DS",f"{E['Ts']:.2f} s"],
    ["Sa (T ≤ Ts → Sa = S_DS)",f"{E['Sa']:.2f} g"],["Importance factor I",f"{E['I']:.2f}"],["Response modification R","5 (intermediate RC moment frame)"],
    ["Cs = Sa·I/R",f"{E['Cs']:.4f}"]],widths=[3.2,3.4])
h2("(b) Seismic weight and base shear")
lv=[2,3,4,5]; W=[E["W"][i] for i in lv]; Wdl=[E["Wself"][i]+E["Wsdl"][i] for i in lv]; Wl=[0.25*E["Wll"][i] for i in lv]
Wm=Vx/E["Cs"]; Wt=sum(W); Vc=E["Cs"]*Wt
body_(f"The model's base shear ({Vx:.1f} kN) corresponds to a seismic weight W = V/Cs = {Wm:,.0f} kN. This equals the dead load "
      f"(DL + SDL) of the levels above the ground-floor slab ({sum(Wdl):,.0f} kN, {100*abs(sum(Wdl)-Wm)/Wm:.1f}% difference): the ground-floor slab "
      f"on ground beams (+0.35) acts as the seismic base. Including 0.25 LL of those levels gives W = {Wt:,.0f} kN and V = Cs·W = {Vc:,.0f} kN "
      f"({100*(Vc-Vx)/Vx:.1f}% above the model value).")
hx=[E["LEV"][i]-0.35 for i in lv]; whk=[W[j]*hx[j] for j in range(4)]; S=sum(whk); Fx=[Vc*x/S for x in whk]; Vs=[sum(Fx[j:]) for j in range(4)]
rows=[[E["NAMES"][lv[j]],f"{E['LEV'][lv[j]]:+.2f}",f"{hx[j]:.2f}",f1(Wdl[j]),f1(Wl[j]),f1(W[j]),f"{whk[j]/S:.3f}",f1(Fx[j]),f1(Vs[j])] for j in range(3,-1,-1)]
table(["Level","z (m)","hx (m)","DL+SDL (kN)","0.25LL (kN)","wx (kN)","Cvx","Fx (kN)","Vx (kN)"],rows,widths=[0.95,0.6,0.6,0.85,0.8,0.8,0.55,0.7,0.7],size=11,
      totals=["Σ","","",f1(sum(Wdl)),f1(sum(Wl)),f1(Wt),"1.000",f1(sum(Fx)),"–"])
body_(f"Vertical distribution Fx = Cvx·V, Cvx = wx·hx^k/Σ(wi·hi^k) with k = 1 (T = {E['T']:.3f} s ≤ 0.5 s); hx measured from the ground-floor slab (+0.35). ΣFx = V = {Vc:,.1f} kN.")

# 7 MEMBER DESIGN
page_break(); h1("7. RC Member Design")
body_("Beams and columns are checked in MIDAS GEN NX to ACI 318M-14 with the strength combinations U1–U9 (Clause 7), concrete C280 "
      "(f'c = 27.46 MPa) and SD40 reinforcement (fy = fys = 390 MPa). The reinforcement input for the check, per section, is listed below; the "
      "MIDAS strength-checking result for each section follows.")
mct=open(SC+"/fs_export_check2.mct",encoding="utf-8",errors="replace").read().splitlines()
SN={k:v for k,v in B["sect"].items()}; rb=[]; cur=None; buf=[]
for l in mct+["*END"]:
    if l.startswith("*"):
        cur=l.split()[0] if l.startswith(("*REBAR-BEAM","*REBAR-COLUMN")) else None; continue
    if cur and l.strip() and not l.startswith(";"): rb.append((cur,[x.strip() for x in l.split(",")]))
rows=[]; i=0
while i<len(rb):
    kind,f=rb[i]
    if kind=="*REBAR-BEAM":
        I_,M_=rb[i+1][1],rb[i+2][1]
        bars=lambda r:"+".join(x for x in (r[1],r[2]) if x!="0")+f"-{r[3]}"; bb=lambda r:"+".join(x for x in (r[6],r[7]) if x!="0")+f"-{r[8]}"
        rows.append([SN[f[0]],"Beam",f"top {bars(I_)} / bot {bb(I_)}",f"top {bars(M_)} / bot {bb(M_)}",f"{I_[12]}-{f[2]} @{I_[10]} / @{M_[10]}",f"{float(f[3])*1000:.1f}"]); i+=4
    else:
        rows.append([SN[f[0]],"Column",f"{f[6]}-{f[3]} ({f[7]} rows)","–",f"{f[11]}-{f[9]} @{f[10]} (ends) / @{f[15]} (centre)",f"{float(f[8])*1000:.1f}"]); i+=1
table(["Section","Type","Main bars – ends (I/J)","Main bars – mid","Stirrups / ties","Cover to bar c.l. (mm)"],rows,widths=[1.35,0.6,1.5,1.25,1.4,0.7],size=10)
PAGES=[("B10000","GB1 250×800 (section 201)"),("B10001","GB1A 250×800 (section 202)"),("B10002","GB1C 250×800 (section 203)"),
       ("B10003","B1 250×600 (section 204)"),("B10004","B1A 250×600 (section 205)"),("B10005","B1C 250×600 (section 206)"),
       ("B10006","B2 250×600 (section 207)"),("B10007","B2A 250×600 (section 209)"),
       ("C10000","C1 250×250, ground floor (section 101)"),("C10001","C1 350×350, footing stub (section 102)"),
       ("C10002","C2 250×400, ground floor (section 103)"),("C10003","C2 350×500, footing stub (section 104)"),
       ("C10004","C3 250×250, ground floor (section 105)"),("C10005","C3 350×350, footing stub (section 106)")]
for fn,nm in PAGES:
    page_break()
    figure(SC+f"/dsgn/{fn}.png",("RC beam strength check – " if fn[0]=="B" else "RC column strength check – ")+nm,width=5.9)

# NOTES
page_break(); h2("Notes")
for n in ["All model data and results are extracted from the live MIDAS GEN NX model after linear static analysis.",
          "Units: kN, m unless stated. Supports are fixed at the pile caps (−1.00 m).",
          "Slabs are modelled at the level of their supporting beams; local slab steps shown on the drawings are not modelled.",
          "Live loads per Ministerial Regulation B.E. 2566 Clause 11 (Clause 12 for the roof water-tank area, 5 kPa); SDL 2.50 kPa on all slabs.",
          "Load combinations per the same Regulation, Clause 7 (strength) and Clause 6 (service); D = DL + SDL.",
          f"Seismic: DPT 1301/1302-61 parameters as entered in the model (S_DS = {E['SDS']:.2f} g, S_D1 = {E['SD1']:.2f} g, I = {E['I']:.2f}, R = 5).",
          "Member design pages are the MIDAS GEN NX RC strength-checking results (ACI 318M-14) for each beam and column section."]:
    bullet(n)
doc.save(OUT); print("SAVED",OUT,"figures",FIGN[0])
