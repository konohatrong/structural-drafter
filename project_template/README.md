# Project template

The office folder structure for a new structural project, and the script that creates it. The workflow that goes with
it is `docs/general/PROJECT_WORKFLOW.md`.

```powershell
python project_template\new_project.py "BANWA 3" --code BW3 --root "G:\My Drive\Works\##2026" --fea-local D:\Workspace
```

| File | What it is |
|---|---|
| `new_project.py` | Copies `tree\` to `<root>\YYYYMMDD - <name>\`, fills the placeholders, creates the empty folders, makes `04 Code` a git repository. Never writes into an existing folder |
| `tree\` | The template. Edit it here to change every future project |
| `new_project.py --adopt <folder> --code <PPPP>` | Brings an existing project in the earlier office folders into the structure in place: renames the old folders, adds the missing ones, never deletes or writes over (`PROJECT_WORKFLOW.md` W8) |
| `new_project.py --office-template <folder>` | Refreshes the office copy `G:\My Drive\Works\##Project Structures\` from `tree\` (renames the old office folders, writes `_HOW TO USE.md`, deletes nothing) |

Placeholders in the template files: `{{PROJECT}}`, `{{CODE}}`, `{{DATE}}`, `{{DATE_TEXT}}` (the day the folder is made), `{{STARTED}}`, `{{DRAFTER}}` (this
repository), `{{FEA_RUN}}` (the GEN NX working folder). `04 Code\gitignore.txt` becomes `.gitignore`.
