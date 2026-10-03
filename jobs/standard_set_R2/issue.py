"""
Issue data of the R2 typical-detail sets (title block of every sheet): stage, revision, date, revision rows and
status stamp. Imported by td_columns.py, td_beams.py and td_slabs.py after the engine.

F-A ISSUED FOR USE, 03/10/2026 (user): the first official issue, recorded in standard_drawings/REGISTER.md.
The earlier "D-A ISSUED FOR REVIEW" prints (29/09 - 03/10/2026) were review copies, not issues.
A later change is a new revision: raise "rev", add a row to REVS, then publish with --issue
(standard_drawings/README.md).
"""
from drafter import td_engine
from drafter.td_engine import PROJ

PROJ.update(stage="F", rev="A", date="03/10/2026")
td_engine.REVS = [("A", "ISSUED FOR USE", PROJ["date"])]
td_engine.STATUS = ("ISSUED FOR USE", "")
