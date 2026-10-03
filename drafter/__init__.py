"""
Code shared by every job:
    fonts.py      font measurement and wrapping
    acad.py       AutoCAD Core Console plotting; ezplot.py / plotting.py: the ezdxf fallback and the choice
    pens.py       pens by colour and LTSCALE (no side effects)
    td_engine.py  the general drafting engine (creates its DXF document at import: one set per process)
    steel.py      steel layers and helpers on top of td_engine (import after the project data is set)

The job scripts add the repository root to sys.path and import from here, e.g.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drafter.fonts import text_w, wrap
The superseded engine in jobs/typical_details keeps its own copies.
"""
