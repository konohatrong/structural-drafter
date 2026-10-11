@AGENTS.md

## Claude Code

- Skills in `.claude/skills/`:
  - `concrete-detailing` for RC sets (typical details, member details, stairs, retaining walls, general notes);
  - `steel-detailing` for steel sets (members, connections, welds, bolts, bearings, bracing).

  Load the matching skill before starting a drawing task.
- A new project starts with its folder from `project_template\new_project.py` (workflow
  `docs/general/PROJECT_WORKFLOW.md`); on an existing project read its `STATUS.md` first.
- Reference PDFs (codes, handbooks, AISC guides) are outside the repository under `G:\My Drive\##Textbook\`, and the
  office standard details under `G:\My Drive\##Workset_Autocad\400 Standard Details\`. Read the PDFs with PyMuPDF.
