"""FEA example: build a small frame, RUN ANALYSIS, and read results.

Demonstrates the analyze -> results flow described in docs/CONVENTIONS.md:

    build model  ->  POST /doc/ANAL  ->  POST /post/table (Result.*)

Requires a running MIDAS GEN NX and a MAPI-Key. Get the key from
GEN NX -> Apps -> API Settings -> Refresh, then run one of:

    python examples/analyze_and_report.py --key <YOUR_MAPI_KEY>
    set MIDAS_MAPI_KEY=<key>  &&  python examples/analyze_and_report.py
    # or put {"mapi_key": "<key>"} in config.json at the repo root

Note: this needs the live solver, so unlike a dry run it cannot be faked
without GEN NX open.
"""
import argparse
import json
import os
import sys

# --- Windows UTF-8 guard: do this BEFORE importing midas_gen (it prints a
#     Unicode banner that crashes non-UTF-8 consoles). See CONVENTIONS A8.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    except Exception:
        pass

from midas_gen import (  # noqa: E402
    MAPI_KEY, MAPI_BASEURL, MidasAPI,
    Node, Element, Material, Section, Boundary,
    Load, Load_Case, Model, Result, TableOptions,
)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resolve_key(cli_key: str | None) -> str | None:
    if cli_key:
        return cli_key
    if os.environ.get("MIDAS_MAPI_KEY"):
        return os.environ["MIDAS_MAPI_KEY"]
    cfg = os.path.join(REPO_ROOT, "config.json")
    if os.path.exists(cfg):
        with open(cfg, encoding="utf-8") as fh:
            return json.load(fh).get("mapi_key") or None
    return None


def build_portal_frame() -> dict:
    """A single-bay portal frame: 2 columns + 1 beam, fixed at the base.

    Returns the ids we'll query after analysis.
    """
    Model.clear()  # start from a clean Python state

    # material + sections
    Material.STEEL("A992", "ASTM(S)", "A992")            # id 1
    Section.DB("Col-W8x35", "H", "AISC", "W8x35", id=1)
    Section.DB("Bm-W16x67", "H", "AISC", "W16x67", id=2)

    H, L = 3.5, 6.0                                       # height, span (m)
    # nodes: 1,2 = column bases; 3,4 = beam ends (top)
    Node(0, 0, 0, id=1); Node(L, 0, 0, id=2)
    Node(0, 0, H, id=3); Node(L, 0, H, id=4)

    # elements: 2 columns (sect 1), 1 beam (sect 2)
    Element.Beam(1, 3, mat=1, sect=1, group="Columns", id=1)
    Element.Beam(2, 4, mat=1, sect=1, group="Columns", id=2)
    Element.Beam(3, 4, mat=1, sect=2, group="Beam", id=3)

    # fixed supports at the base
    Boundary.Support(1, "fix"); Boundary.Support(2, "fix")

    # load case + a downward UDL on the beam (GZ, negative = down)
    Load_Case("D", "Dead")
    Load.SW("Dead", "Z", -1)                              # self weight
    Load.Beam([3], "Dead", value=-10.0, direction="GZ")  # 10 kN/m down

    Model.create()                                        # push everything

    return {"base_nodes": [1, 2], "beam_elem": [3]}


def main() -> None:
    ap = argparse.ArgumentParser(description="Build, analyze, and report.")
    ap.add_argument("--key", help="MAPI-Key (else MIDAS_MAPI_KEY / config.json)")
    args = ap.parse_args()

    key = resolve_key(args.key)
    if not key:
        sys.exit("No MAPI-Key. Pass --key, set MIDAS_MAPI_KEY, or add config.json.")

    # 1) connect
    MAPI_KEY(key)
    MAPI_BASEURL.autoURL()

    # 2) build
    ids = build_portal_frame()
    print(f"Model built: base nodes {ids['base_nodes']}, beam {ids['beam_elem']}")

    # 3) run the solver  (the desktop product computes; this just triggers it)
    print("Running analysis (/doc/ANAL)...")
    resp = MidasAPI("POST", "/doc/ANAL", {"Assign": {}})
    if isinstance(resp, dict) and ("error" in resp or "message" in resp):
        print("  analysis response:", resp)

    # 4) read results  (load case 'Dead' is 'Dead(ST)' in result tables)
    opts = TableOptions()
    case = ["Dead(ST)"]

    print("\n--- Reactions at base nodes ---")
    try:
        print(Result.Reaction(keys=ids["base_nodes"], loadcase=case, options=opts))
    except Exception as exc:  # noqa: BLE001
        print("  (could not fetch reactions):", exc)

    print("\n--- Displacements (beam top nodes 3,4) ---")
    try:
        print(Result.Displacement(keys=[3, 4], loadcase=case, options=opts))
    except Exception as exc:  # noqa: BLE001
        print("  (could not fetch displacements):", exc)

    print("\n--- Beam member forces (element 3) ---")
    try:
        print(Result.BeamForce(keys=ids["beam_elem"], loadcase=case, options=opts))
    except Exception as exc:  # noqa: BLE001
        print("  (could not fetch beam forces):", exc)

    print("\nDone. (Results are blank if the model didn't solve — check supports/loads.)")


if __name__ == "__main__":
    main()
