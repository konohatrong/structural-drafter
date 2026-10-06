# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, TextPolicy
P=r"G:\My Drive\Works\20260318 - Samutsongkram Building Office\CAD\for tracing\ST-Plan-อาคารดับเพลิง.dxf"
OUT=__import__("os").environ.get("MG_WORKDIR", ".")
doc=ezdxf.readfile(P); msp=doc.modelspace()
CFG=Configuration(text_policy=TextPolicy.IGNORE)

def render(clip,name,w=16,h=6):
    fig=plt.figure(figsize=(w,h)); ax=fig.add_axes([0,0,1,1]); ax.set_facecolor("white")
    ctx=RenderContext(doc); be=MatplotlibBackend(ax)
    Frontend(ctx,be,config=CFG).draw_layout(msp,finalize=False)
    if clip:
        ax.set_xlim(clip[0],clip[2]); ax.set_ylim(clip[1],clip[3])
    ax.set_aspect("equal"); ax.axis("off")
    fig.savefig(f"{OUT}/{name}.png",dpi=130,facecolor="white"); plt.close(fig)
    print("saved",name)

render(None,"dxf_full",22,4)
render((-2000,-8000,30000,17000),"dxf_foundation",13,9)   # panel 1
render((44000,-8000,74000,17000),"dxf_groundbeam",13,9)   # panel 2
