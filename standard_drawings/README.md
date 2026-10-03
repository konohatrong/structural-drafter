# Standard drawings: developing and official issue

The office **standard drawings**, the sheets every project refers to:

| Set | Sheets | Generator |
|---|---|---|
| `gn`: general notes, structural concrete | STR-ST-1001 – 1003 | `jobs/standard_set` (`gn_notes.py`) |
| `columns`: typical column details | STR-ST-1101 – 1104 | `jobs/standard_set_R2` (`td_columns.py`) |
| `beams`: typical beam details | STR-ST-1111 – 1116 | `jobs/standard_set_R2` (`td_beams.py`) |
| `slabs`: typical slab details | STR-ST-1121 – 1128 | `jobs/standard_set_R2` (`td_slabs.py`) |

New standard sets (walls 113x, foundations 114x, steel standards) are added to `SETS` in `publish.py` and to this
table. Project sets (`jobs/nooker_rw`, `jobs/steel_roof_truss`) are not standards; they stay in `jobs/` as examples.

The drawings are generated: the source of truth is the generator code and the rules in `docs/`. This folder holds
the **plotted output** at two stages.

| Folder | What it holds | In git |
|---|---|---|
| `developing/<set>/` | The latest review build of each set: PDF, DWG (or the DXF without AutoCAD), detail library, `MANIFEST.json`. **Replaced** on every publish | **No** (local only) |
| `issued/<set>/<stage>-<rev>/` | One folder per **official issue**: PDF, DWG, detail library (one DWG per detail and the title block), block index, `MANIFEST.json`. **Never changed** after it is written | **Yes**, as the permanent record |
| `REGISTER.md` | The issue register: one row per issued revision | Yes |

## 1. Developing (review copies)

```powershell
python standard_drawings/publish.py columns          # build + AutoCAD plot -> developing/STR-ST-1101_Typical_Column_Details/
python standard_drawings/publish.py all --ezdxf      # every set, plotted without AutoCAD
python standard_drawings/publish.py slabs --no-build # copy the current out/ files without rebuilding
```

- Use it to hand a set to the reviewer, or to compare with the last issue.
- The folder is replaced each time and is not in git. Keep a copy elsewhere if a review needs a fixed snapshot.
- `MANIFEST.json` records the commit, whether the generator had uncommitted changes, the plot engine, the drawing
  numbers, status and revision rows, and a SHA-256 for every file.

## 2. Official issue

An official issue is a decision of the engineer (the user), never of an agent on its own.

1. **Finish the review.** The developing copy is approved, every comment is closed, and the open items in the
   set's documents are resolved or stated on the drawings.
2. **Set the revision and status in the generator**:
   - `PROJ["rev"]` (and `PROJ["stage"]` if the stage changes) and `PROJ["date"]`;
   - a row in `REVS` (or `REVS_BY_SHEET`) with the revision's description, e.g. `("B", "ISSUED FOR USE", "dd/mm/yyyy")`;
   - the status stamp `td_engine.STATUS`, e.g. `("STANDARD DETAIL", "ISSUED FOR USE")`. The default is
     `("FOR REVIEW", "NOT FOR CONSTRUCTION")`. (The general notes run on the frozen R1 engine copy in
     `jobs/standard_set`, whose stamp is fixed; change it there only as part of a revision of that set.)
3. **Commit** the generator changes. An issue is refused while `drafter/` or the set's job folder has uncommitted
   changes, so every issue traces to one commit.
4. **Issue:**

   ```powershell
   python standard_drawings/publish.py columns --issue
   ```

   The script builds and plots the set with AutoCAD, checks that the build is clean, the DWG and every library DWG
   exist and every sheet carries the same revision, then writes `issued/<set>/<stage>-<rev>/` and appends a row to
   `REGISTER.md`. It refuses if that revision was issued before.
5. **Commit and push** `standard_drawings/` ("Issue STR-ST-1101 D-B").

## 3. Rules

- **An issued revision is never edited, replaced or deleted.** A correction is a new revision, issued the same way.
- **Only AutoCAD plots are issued.** The ezdxf fallback is for review only (`docs/general/DRAWING_PRODUCTION.md` §7).
- **Issue the whole set**, not single sheets: every sheet of a set carries the same revision.
- **What a project uses** is the latest issued revision in `REGISTER.md`, never a developing copy.
- **Superseded revisions stay** in `issued/` and in the register, so a project issued against an older revision can
  still find it.
- The library DWGs of an issue are the blocks a project inserts (`docs/general/DRAWING_ENGINE.md` §8).

## 4. Current state

Nothing has been issued through this folder yet. The sets were last sent out as "FOR REVIEW" outside it (general
notes Rev B; typical details R2, `jobs/standard_set_R2`). Their first official issue is recorded in `REGISTER.md`
when it is made.
