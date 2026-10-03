"""
Choose the plotter for a job's plot script: AutoCAD Core Console when it is installed (the reference), otherwise
ezdxf (drafter/ezplot.py). Add --ezdxf to a plot script's command line to use ezdxf even with AutoCAD installed.
"""
import sys
from pathlib import Path

from ezdxf.addons import acadctb

from drafter import acad, ezplot

USE_EZDXF = "--ezdxf" in sys.argv


def args():
    """the script's arguments without the --ezdxf flag"""
    return [a for a in sys.argv[1:] if a != "--ezdxf"]


def flags():
    """flags to pass on to a sub-process plot"""
    return ["--ezdxf"] if USE_EZDXF else []


def use_autocad():
    return not USE_EZDXF and acad.available()


def base_ctb():
    """the plot style to start from: AutoCAD's monochrome.ctb, or without AutoCAD an all-black table (the
    ezdxf renderer only reads its pens and screens)"""
    if use_autocad():
        return acad.monochrome()
    ctb = acadctb.new_ctb()
    for aci in range(1, 256):
        ctb[aci].color = (0, 0, 0)
    return ctb


def plot_set(dxf, layouts, ctb_name, ctb, *, setvars, per_layout=(), wblocks=(), lib=None, timeout=600):
    """plot with AutoCAD (installs ctb as ctb_name first) or, without it, with ezdxf"""
    if use_autocad():
        acad.install_ctb(ctb, ctb_name, Path(dxf).parent)
        acad.plot(dxf, layouts, ctb_name, setvars=setvars, per_layout=per_layout, wblocks=wblocks, lib=lib,
                  timeout=timeout)
    else:
        if not USE_EZDXF:
            print(f"AutoCAD Core Console not found ({acad.ACC}): plotting with ezdxf instead")
        ezplot.plot(dxf, layouts, ctb, wblocks=wblocks, lib=lib)
