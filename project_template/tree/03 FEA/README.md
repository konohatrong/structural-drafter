# 03 FEA

Analysis models and what was read from them, by **model revision** `rNN` (r01, r02 …). One revision = one change to
the model; the revision number is the same in the model file name, the snapshot, the results and `MODEL_LOG.md`.

| Folder | Holds |
|---|---|
| `models\` | Milestone model files `{{CODE}}_rNN_<what>.mgbx` (the model only, no result files) |
| `snapshots\rNN\` | Read-back of the model after the change (JSON tables): what was written, checked |
| `results\rNN\` | Exported results of the analysed revision (reactions, forces, displacements, CSV/JSON) |

The GEN NX working folder is `{{FEA_RUN}}`. Analyses run there because the result files (`.GAX1`, `.XOUT`) reach
several GB per run; they are rebuilt by running the analysis again and are not kept here.

Rules (`{{DRAFTER}}\midas\MIDAS_GEN_NX_INSTRUCTION.md` M1 – M12):

- Save the model as a new revision before any write; write by script, read it back, compare with the snapshot.
- Never IMPORTMXT, never blind DELETE. The MAPI key is typed on the command line only, never stored in a file.
- A calc or drawing names the model revision its numbers come from.
