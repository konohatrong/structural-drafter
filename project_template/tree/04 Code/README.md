# 04 Code

The project's scripts, in a git repository. Code only: every output goes to the numbered folders through
`paths.py`, never into this folder.

| File / folder | Holds | Writes to |
|---|---|---|
| `project.py` | Project data: the single source of every design value, grid, level and drawing setting | – |
| `paths.py` | The folder map and the toolkit path (`use_drafter()`) | – |
| `model\` | GEN NX scripts through MAPI: build from DXF, loads, springs, read-back, result export | `03 FEA` |
| `calc\` | Design calcs `calc_*.py` (member, connection, foundation checks) | `05 Calculation` |
| `drawings\` | The drawing job: `*_engine.py`, `*_sheets.py`, `build.py`, `plot.py` | `06 CAD\out`, `07 Review` |
| `report\` | Calculation-note builder (figures, tables, the document) | `08 Report` |

Rules:

- Import the toolkit, never copy it: `import paths; paths.use_drafter()`, then `from drafter import td_engine`.
  A tool that becomes useful for other projects moves into the toolkit (`{{DRAFTER}}`) with a test.
- A script that reads model results takes the model revision as an argument (`python calc\calc_piles.py r12`) and
  writes it into its output.
- The MAPI key is passed on the command line only. Never write it into a file, a log or a commit.
- Commit when a step is done ("r12 pile springs", "S-101 review A2"); the commit message names the revision.
