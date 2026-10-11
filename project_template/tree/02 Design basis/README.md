# 02 Design basis

The design criteria and the evidence for them: `DESIGN_BASIS.md`, load maps, the soil report digest, pile data,
regulation extracts, and the engineer's approvals.

- Every value in `DESIGN_BASIS.md` has a source (a received document, a code clause, or "engineer, DD/MM/YYYY").
- The approved values are typed once, into `04 Code\project.py`. Scripts, drawings and the report read them from
  there; nothing retypes them.
- A changed value is a new dated row, not an overwrite, so the calcs and drawings made on the old value can be found.
