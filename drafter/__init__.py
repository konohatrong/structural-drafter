"""
Code shared by every job: font measurement (fonts.py) and AutoCAD Core Console plotting (acad.py).

The job scripts add the repository root to sys.path and import from here, e.g.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from drafter.fonts import text_w, wrap
The superseded engine in jobs/typical_details keeps its own copies.
"""
