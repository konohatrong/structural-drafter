# Project workflow: folder structure and stages of a structural project

How a project is organised on disk and how the work moves from received drawings to an issued set and calculation
note. It applies to every project, whatever the structure or material. The drawing pipeline inside the work is
`DRAWING_PRODUCTION.md`; the analysis model is `midas/MIDAS_GEN_NX_INSTRUCTION.md`.

The structure extends the earlier office template (CAD, Calculation, Transfer in, Transfer out) with the folders the scripted work needs. It was written on 11/10/2026 at the user's request, from what
the SSK, BANWA 2 and SPF jobs taught (W9).

## W1. Create the folder

```powershell
python project_template\new_project.py "<name>" --code <PPPP> --root "G:\My Drive\Works\##2026" --fea-local D:\Workspace
```

The script (`project_template/README.md`) copies the template, fills the name, the code and the paths, and makes
`04 Code` a git repository. Then fill `PROJECT.md` §1 – §3 and `02 Design basis\DESIGN_BASIS.md`. Change the template
in `project_template/tree/`, never project by project.

The office copy `G:\My Drive\Works\##Project Structures\` (for copying by hand, with `_HOW TO USE.md`) is generated
from the same template: after a change to `tree/`, refresh it with
`python project_template
ew_project.py --office-template "G:\My Drive\Works\##Project Structures"`. It was
converted on 11/10/2026: the old folders renamed (Transfer in → `01`, Calculation → `05`, CAD → `06`, Transfer out →
`09 Publish`).

## W2. The structure

```
YYYYMMDD - <name>\
├─ PROJECT.md            project card: who, what, codes, drawing settings, where things are
├─ STATUS.md             the resume point: decisions waiting, current state, next steps, open items, log
├─ 00 Admin\             proposal, contract, scope, minutes, correspondence
├─ 01 Transfer in\       everything received, dated folders, RECEIVED.md          (never edited)
├─ 02 Design basis\      DESIGN_BASIS.md, load maps, soil data, approvals
├─ 03 FEA\               MODEL_LOG.md, DECISION_LOG.md; input\ models\ snapshots\rNN\ results\rNN\
├─ 04 Code\              git: project.py, paths.py, model\ calc\ drawings\ report\  (no outputs)
├─ 05 Calculation\       calc outputs, check sheets data, spreadsheets, hand checks
├─ 06 CAD\               xref\ working\ out\
├─ 07 Review\            dated review prints, markups\
├─ 08 Report\            calculation note: source\ figures\ appendix\
├─ 09 Publish\           official issues, one frozen folder each, ISSUE_REGISTER.csv (never edited)
└─ 99 Archive\           superseded material, moved not deleted
```

Each folder has a README that says what goes in it. The rules behind the structure:

1. **Inputs and issues are frozen.** `01 Transfer in` holds what others sent, `09 Publish` what we sent. Neither is
   edited; work happens on copies, and a correction is a new issue.
2. **Code and outputs are apart.** `04 Code` holds scripts only and is a git repository; scripts write through
   `paths.py` into the numbered folders. A build can be rerun at any time; an output is never edited by hand.
3. **One source per value.** Design values are typed once, in `04 Code\project.py`, after the engineer approves them
   in `DESIGN_BASIS.md` (AGENTS.md §2.1). A value not decided stays `None`, and `project.need()` stops the script.
4. **Large analysis files stay local.** A GEN NX run writes `.GAX1` / `.XOUT` result files of several GB (BANWA 2:
   19 GB for one run, 62 GB in the folder). Run GEN NX in a local folder (`--fea-local`, `paths.FEA_RUN`); keep only
   the milestone `.mgbx` models, the snapshots and the exported results in `03 FEA`. The results files are rebuilt by
   analysing again.
5. **Dates first.** Every dated folder and file starts with `YYYYMMDD - `, so names sort in time order (the office
   habit).

## W3. Revisions: three counters, never mixed

| Counter | Form | Where | Moves when |
|---|---|---|---|
| Model revision | `r01`, `r02` … | model file name, `snapshots\rNN`, `results\rNN`, `MODEL_LOG.md` | any write to the model |
| Internal drawing / report revision | `A1`, `A2` … (`B1` … after a submission) | `07 Review` print names, `06 CAD\working` | each review print |
| Issue revision | `A`, `B` … ; `00` tender; `01` … after tender (EIT Table 4.4) | `09 Publish`, title-block revision table | each official issue |

Every calc output, review print, report and issue names its **basis**: the model revision and the date of the inputs
("model r40, AR of 06/10/2026"). With that line the chain issue → calc → model → inputs can be followed back.

## W4. Stages

| Stage | Work | Writes to | Gate (the engineer) |
|---|---|---|---|
| S0 Set up | Create the folder (W1); fill `PROJECT.md`; choose sheet, font, plot style (FP0) | root | Drawing settings chosen |
| S1 Receive | Save each receipt dated; register it; convert copies (DWG → DXF); overlay or read checks of the inputs; list questions | `01`, `06 CAD\xref`, `07 Review` | Questions to the architect sent |
| S2 Design basis | Codes, materials, loads, combinations, foundation data, each with its source | `02`, `04 Code\project.py` | **Design basis approved** |
| S3 Model | Build or change the model by script; save as a new `rNN` first; read back and compare; log | `03 FEA` | Model reviewed before analysis |
| S4 Analyse and design | Analyse; export results to `results\rNN`; run the calcs; check sheets for the engineer | `03 FEA\results`, `05`, `07` | **Design accepted**; failing checks decided |
| S5 Draw | Build the set from the calcs and the project data; look at every sheet; review print | `06 CAD\out`, `07 Review` | Markup returned |
| S6 Review loop | Fix every markup comment; general comments become toolkit rules (AGENTS.md §3); next internal revision | `04 Code`, toolkit `docs\` | **Drawings accepted** |
| S7 Report | Calculation note from the design basis and the calc outputs; figures by model revision | `08 Report` | Report accepted |
| S8 Issue | Copy the PDFs (and CAD if required) to a new `09 Publish` folder; transmittal; register | `09 Publish` | **Issue approved** |
| S9 Changes | A changed input or comment after issue: back to S1 – S5 as needed; a new issue revision | all | as above |
| S10 Close-out | Archive superseded files; keep the final model of each issue; record lessons in the toolkit | `99 Archive`, toolkit | – |

Stages overlap in practice (foundations drawn while the roof is still being designed). The gates do not: nothing is
issued on a basis the engineer has not approved, and engineering decisions are the engineer's (AGENTS.md §4).

### W4.1 Issue (stage S8) step by step

User, 2026-10-12 (CHATAM: "publish this revision", answered "A, 12/10/26, FOR REVIEW", "PDF only"). An issued folder
is frozen, so everything printed on the sheets is settled **before** the copy:

1. **Ask what the revision row says**: revision, date, purpose (FOR REVIEW / FOR APPROVAL / FOR CONSTRUCTION) and the
   contents (PDF only, or PDF + DWG with fonts and CTB). The row is set once in the project's engine (CHATAM
   `ch_engine.REV`), dated the **issue** day, not the day the set was started.
2. Rebuild and plot **every** set with that row, the drawing list last (`DRAWING_PRODUCTION.md` §1.1); a clean build
   (no `!!`) and the AutoCAD plot.
3. Check each page before copying: the revision row and date on every sheet, the drawing list against the sheets.
4. Create `09 Publish\YYYYMMDD - <set> Rev <R> - <purpose>\PDF\`: the merged set (bookmarked) and one PDF per sheet
   named `<CODE>-ST <No.> Rev <R> - <title>.pdf`. The script refuses to run when the folder exists.
5. `TRANSMITTAL.md`: date, issue and purpose, **to whom ("not sent yet" until the engineer sends it)**, the basis (model
   revision and the date of the inputs), the sheet list, the open items still TBC on the sheets.
6. One row per sheet in `ISSUE_REGISTER.csv` the same day; a log row in `STATUS.md`.
7. From then on the next changes are internal revisions (`B1`, `B2` … review prints) and the next issue is `B`.

If the copy fails half way within the same minute, the half-written files are yours: remove them and rerun the
script (CHATAM: a "/" in a sheet title). A folder that was complete is never touched again.

## W5. Every working session

1. **Start**: read `STATUS.md` (decisions waiting, next steps). Check `RECEIVED.md` for anything new.
2. **Work** in small steps that end in a file: a model revision with its log row, a calc output, a review print.
3. **Look** at what was produced (sheets at print size, check plots), not only at the script's exit code.
4. **End**: update `STATUS.md` (state, next steps, the log row), commit `04 Code` with the revision in the message.

## W6. Handing over

`STATUS.md` and `PROJECT.md` are the handover. Before someone else (or another session) takes the project:

1. bring `STATUS.md` up to date: the decisions waiting, with options; what is assumed; what is half done;
2. commit `04 Code`;
3. name in `STATUS.md` the model revision that is live in GEN NX and whether it has been analysed.

### W6.1 Several sessions at once

On CHATAM (12/10/2026) four sessions worked on one project folder at the same time (model and reactions, RC
schedules, foundation and caps, stair and pool). What kept them apart:

- **One owner per module**: each session names the files it owns in its `STATUS.md` rows; a session that must change
  another's module (an engineer's instruction that crosses sets) reads it again first, keeps the other's changes, and
  sends the owner the list of what changed.
- **Engineer's decisions as data in `04 Code\project.py`**, read by every set (CHATAM `CAP_TOP`, `CAP_TOP_AT`,
  `CAP_PILES_ADD`, `POOL_SLAB`): the RC schedule, the foundation plan and the cap details then follow without editing
  each other's code.
- **`STATUS.md` rows appended**, never rewritten; written with literal backslashes (`DRAWING_PRODUCTION.md` §8).
- **Before a merged print or an issue, rebuild every set** (`DRAWING_PRODUCTION.md` §1.1).

A work-transfer package (as BANWA 2 received on 09/10/2026) is received into `01 Transfer in` like any other input,
and is reviewed before anything from it is adopted.

## W7. What never goes into the project folder

- the MAPI key or any password (the command line only);
- copies of the toolkit (`drafter\`, `docs\`): import it through `paths.use_drafter()`;
- standards PDFs and handbooks (they stay in `G:\My Drive\##Textbook\`; cite page references).

## W8. Existing projects

Projects with scripts of their own (SSK, BANWA 2, SPF) keep their folders; moving them would break the paths in their
scripts and READMEs. Apply W2 – W5 to new work in them where it does not mean moving files, and use the template for
every new project.

A project kept in the earlier office folders (CAD, Calculation, Transfer in, Transfer out) and with no scripts is
brought into the structure in place when the engineer asks:

```powershell
python project_template
ew_project.py --adopt "<project folder>" --code <PPPP> --fea-local D:\Workspace
```

The old folders are renamed (Transfer in → `01`, Calculation → `05`, CAD → `06`, Transfer out → `09 Publish`), the
missing folders and files are added, nothing is deleted or written over, and the project folder keeps its name. A
folder outside the structure is listed and left for the engineer to place (CHATAM HOTEL, 11/10/2026: `Revit` moved to
`06 CAD\Revit`). Xrefs in the same folder still resolve after the rename; a link by full path (Revit, a DWG xref
with a full path) is reloaded once.

## W9. Where the rules came from

| Problem seen | Project | Rule |
|---|---|---|
| Model files and 19 GB result files at the project root; 30 snapshot folders beside the scripts | BANWA 2 | W2.4, `03 FEA` layout, W3 |
| Received DWG and the converted DXF confused; an outdated plan used as the source | SSK, 04/10/2026 | W2.1, `01 Transfer in` README |
| Review PDF locked in a viewer while rebuilding | SPF, BANWA 2 | outputs in `06 CAD\out`, review copies in `07 Review` |
| Work handed between sessions with decisions buried in long notes | BANWA 2, 09 – 10/10/2026 | `STATUS.md` §0, W6 |
| A weight typed in two places and different | BANWA 2 purlins, 10/10/2026 | W2.3 |
