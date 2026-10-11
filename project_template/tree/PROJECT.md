# {{PROJECT}}

Project card: what the project is and where everything lives. Fill it on the first day and keep it current. The
day-to-day state (decisions waiting, next steps, log) is in `STATUS.md`.

Created {{DATE_TEXT}} from the office project template (`{{DRAFTER}}\project_template`, workflow in
`docs\general\PROJECT_WORKFLOW.md`).

## 1. Project

| Item | Value |
|---|---|
| Name | {{PROJECT}} |
| Project code (EIT §13 `PPPP`) | {{CODE}} |
| Client | |
| Architect / other consultants | |
| Location | |
| Structure (type, storeys, materials) | |
| Scope of our work | |
| Stage (EIT Table 4.3: I C P D T F S A) | |
| Engineer in charge | |
| Started | {{DATE_TEXT}} |

## 2. Design basis (summary; full text and sources in `02 Design basis\DESIGN_BASIS.md`)

| Item | Value | Source / approved |
|---|---|---|
| Codes | | |
| Concrete / reinforcement / steel | | |
| Live loads | | |
| Wind / seismic | | |
| Foundation (piles, bearing) | | |
| Units of the model | | |

## 3. Drawing settings (FLOOR_PLAN_DRAWING_INSTRUCTION FP0; the engineer chooses)

| Item | Value |
|---|---|
| Sheet size | |
| Font, height, width factor | |
| Plot style (CTB), LTSCALE | |
| Title block | |
| Drawing number format (EIT §13) | {{CODE}}-ST-SSSS-G-RR |

## 4. Where things are

| What | Where |
|---|---|
| Project folder | this folder (map in §5) |
| FEA working folder (GEN NX runs, large result files) | `{{FEA_RUN}}` |
| Toolkit and rules | `{{DRAFTER}}` |
| Current model revision | (see `03 FEA\MODEL_LOG.md`) |
| Latest review print | (see `07 Review\`) |
| Latest issue | (see `09 Publish\ISSUE_REGISTER.csv`) |

## 5. Folder map

| Folder | Holds | Rule |
|---|---|---|
| `00 Admin` | Proposal, contract, scope, fee, meeting minutes, correspondence | |
| `01 Transfer in` | Everything received, in dated folders; register `RECEIVED.md` | Never edited: work on copies |
| `02 Design basis` | Codes, materials, loads, soil data, load maps, the engineer's approvals | Values go into `04 Code\project.py` |
| `03 FEA` | Milestone models, read-back snapshots and exported results, by revision `rNN`; `MODEL_LOG.md` | One revision per change |
| `04 Code` | Scripts (git repository): project data, model, calcs, drawings, report | No outputs in here |
| `05 Calculation` | Calc outputs (JSON, CSV, review sheets), spreadsheets, hand checks | Each names its model revision |
| `06 CAD` | Xrefs, working DXF/DWG, build output `out\` | |
| `07 Review` | Dated review prints and the returned markups | Internal revisions A1, A2 … |
| `08 Report` | Calculation note: source, figures, appendices | The issued PDF goes to `09 Publish` |
| `09 Publish` | Official issues only, one frozen folder per issue; `ISSUE_REGISTER.csv` | Never edited after issue |
| `99 Archive` | Superseded material | Moved here, not deleted |
