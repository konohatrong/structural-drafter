# MIDAS GEN NX load mapping — VERIFIED on a live model (2026-06-09)

> **Copied** from [`konohatrong/midas_API`](https://github.com/konohatrong/midas_API/blob/b4155ac/pilot%20project/wind%20load%20generator/docs/MIDAS_MAPPING.md) (`pilot project/wind load generator/docs/MIDAS_MAPPING.md`, commit b4155ac, 2026-10-04) into this repository's `midas/` folder. Paths in the text such as `To midas/…`, `pilot project/…` or the root `README.md` name that repository; the map is in [`midas/README.md`](../README.md).

> Verified empirically against **MIDAS GEN NX 2026** (read-back of `/db/BMLD` after
> pushing test loads into an empty model). Units in the test model: kN, m.
> Resolves clarification **#8** (except the visual sign checks noted below).

## Beam (element) loads — `/db/BMLD`

**Request:** `PUT /db/BMLD`
```json
{ "Assign": { "<elemID>": { "ITEMS": [ {
  "ID": 1,
  "LCNAME": "WIND",          // load case name (created via Load_Case)
  "GROUP_NAME": "",          // load group (optional)
  "CMD": "BEAM",
  "TYPE": "UNILOAD",         // uniform OR trapezoidal (see below)
  "DIRECTION": "GX",         // GX/GY/GZ = global, LX/LY/LZ = local (member)
  "USE_PROJECTION": false,   // true = load applied on projected length
  "USE_ECCEN": false,
  "D": [0, 1, 0, 0],         // relative positions along element (i-end=0 … j-end=1)
  "P": [-2, -5, 0, 0],       // magnitude at each D position
  "USE_ADDITIONAL": false, "ADDITIONAL_I_END": 0, "ADDITIONAL_J_END": 0
} ] } } }
```

### Confirmed behaviors
| Need | How | Verified |
|------|-----|----------|
| **Uniform** line load | `TYPE:"UNILOAD"`, `D:[0,1]`, `P:[w,w]` | ✅ |
| **Trapezoidal** (linearly varying) | `TYPE:"UNILOAD"`, `D:[0,1]`, `P:[w_i, w_j]` → ramps w_i (i-end) → w_j (j-end) | ✅ |
| **Global direction** (walls) | `DIRECTION:"GX"`/`"GY"`/`"GZ"` | ✅ |
| **Normal to member** (roof) | `DIRECTION:"LZ"` (local z), `USE_PROJECTION:false` | ✅ |
| **Projected** (roof, global) | `DIRECTION:"GZ"`, `USE_PROJECTION:true` | ✅ |
| **Wind load case** | `Load_Case("W", "WIND")` → `/db/STLD` type `W` | ✅ |

### Mapping to the wind tool
- **Windward wall (height-varying):** push on the column element, `DIRECTION` = global
  horizontal toward/along the wind (GX or GY), `D:[0,1]`, `P:[p_base, p_top]`.
  *Watch the element i→j orientation:* P[0] is the **i-end**; if the column's i-node
  is at the base, P[0] = base pressure.
- **Leeward/side wall (uniform):** same but `P:[w, w]`.
- **Roof (normal pressure):** push on the rafter, `DIRECTION:"LZ"`, `USE_PROJECTION:false`.
- **Per-frame magnitude** = surface pressure × tributary width.

### Zoned / partial-length loads on ONE element — VERIFIED (JSON + visual)
A single element can carry **multiple BMLD items**, each over a **sub-range** via
`D=[d_start, d_end]` (relative 0–1). Verified on a 10 m element with three items:
`D:[0,0.25]→−0.9`, `D:[0.25,0.5]→−0.5`, `D:[0.5,1.0]→−0.3` — GEN NX rendered the
**stepped distribution** correctly. → The low-slope windward-roof **zoning**
(0→h/2, h/2→h, h→2h, >2h) can be applied as partial loads **without re-meshing**
(Option B). For a horizontal member, **−LZ points down** (sign confirmed).

```json
// stepped/zoned load = several ITEMS on the same element, each a D-subrange
{ "Assign": { "1": { "ITEMS": [
  {"ID":1,"TYPE":"UNILOAD","DIRECTION":"LZ","D":[0,0.25],"P":[-0.9,-0.9]},
  {"ID":2,"TYPE":"UNILOAD","DIRECTION":"LZ","D":[0.25,0.5],"P":[-0.5,-0.5]},
  {"ID":3,"TYPE":"UNILOAD","DIRECTION":"LZ","D":[0.5,1.0],"P":[-0.3,-0.3]}
] } } }
```

### Sign conventions — VERIFIED on the gable prototype (2026-06-09)
For wind in **+X** on a gable frame (windward at X=0), confirmed visually in GEN NX:
- **Windward wall** = push **+GX** (into building). `value > 0`, `DIRECTION:"GX"`.
- **Leeward wall** = suction, also acts **+GX** (outward on the downwind face).
  `value > 0`, `DIRECTION:"GX"`. (So both walls → +X; net lateral is correct.)
- **Roof uplift** (negative C_p) = **+LZ** — i.e. **away from the roof top surface**
  for both windward and leeward rafters (MIDAS local +z has a +Z component).
  `value > 0`, `DIRECTION:"LZ"`. ← the prototype initially had this backwards.
- Consistent with the earlier horizontal-beam test (**−LZ = down**, so **+LZ = up**).

> General rule for the engine: compute the **signed** net pressure, then apply the
> magnitude in the axis/direction of the surface's **outward normal** (push = toward
> surface; suction/uplift = along the outward normal).

See [`../prototypes/proto_gable.py`](https://github.com/konohatrong/midas_API/blob/b4155ac/pilot%20project/wind%20load%20generator/prototypes/proto_gable.py) for the worked
prototype (frame + both GCpi cases) that established these.

## Connection (verified)
- `MAPI_BASEURL.autoURL()` selected `https://moa-engineers-kr.midasit.com:443/gen`
  (Korea server) for this key. Product: **MIDAS GEN NX 2026**.
- Read-only health: `GET /ope/PROJECTSTATUS`, `/db/UNIT` (kN, m), `/db/STYP` — all OK.
