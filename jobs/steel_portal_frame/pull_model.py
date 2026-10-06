"""
Project SPF - read the analysis model from a live MIDAS GEN NX session (READ-ONLY) into model/:

    model/spf_model.json   geometry, sections, material, supports, releases, tapered groups, groups, load cases,
                           the steel-design combinations and the beam loads on one typical frame
    model/spf_forces.json  design forces: per element and end (I / J) the envelope of every component over the
                           active steel-design cases (the NU* static cases), the concurrent forces of every case at
                           each joint node, and the support reactions of every case (factored and service)

usage (PowerShell, GEN NX open with the model, Apps > Connect):
    $env:PYTHONIOENCODING = "utf-8"; python pull_model.py "<MAPI-KEY>"

The key is a credential (midas/MIDAS_GEN_NX_INSTRUCTION.md M1): it is taken from the command line only and never
written anywhere. Nothing is written to the model: only GET /db and POST /post/table (result tables). The library's
Result.* helpers are not used because they PUT /db/UNIT first; the model's own units are read and recorded instead.
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "midas" / "tools"))
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

import urllib.error                                                  # noqa: E402
import urllib.request                                                # noqa: E402

REGIONAL = ["https://moa-engineers-kr.midasit.com:443/gen", "https://moa-engineers.midasit.com:443/gen",
            "https://moa-engineers-us.midasit.com:443/gen", "https://moa-engineers-in.midasit.com:443/gen",
            "https://moa-engineers-gb.midasit.com:443/gen"]
_BASE, _KEY = None, None


def call(method, cmd, body=None, timeout=300):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(_BASE + cmd, data=data, method=method,
                                 headers={"MAPI-Key": _KEY, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        return {"_http_error": e.code}


def connect(key):
    global _BASE, _KEY
    _KEY = key
    for u in REGIONAL:
        _BASE = u
        try:
            if "PROJECTSTATUS" in call("GET", "/ope/PROJECTSTATUS", timeout=20):
                return u
        except Exception:
            pass
    sys.exit("!! could not reach GEN NX: open it, Apps > Connect, check the key")


def table(name):
    r = call("GET", "/db/" + name)
    return r.get(name, {}) if isinstance(r, dict) else {}


def result(kind, case):
    arg = {"TABLE_NAME": "SS", "TABLE_TYPE": kind, "STYLES": {"FORMAT": "Fixed", "PLACE": 3},
           "LOAD_CASE_NAMES": [case + "(ST)"]}
    if kind == "BEAMFORCE":
        arg["PARTS"] = ["PartI", "PartJ"]
    r = call("POST", "/post/table", {"Argument": arg})
    return (r.get("SS") or {}).get("DATA", [])


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    print("connected:", connect(sys.argv[1]))
    m = {k: table(k) for k in ("UNIT", "STYP", "MATL", "SECT", "NODE", "ELEM", "CONS", "FRLS", "TSGR", "GRUP",
                               "STLD", "LCOM-STEEL", "PDEL", "BODF")}
    unit = next(iter(m["UNIT"].values()))
    if (unit["FORCE"], unit["DIST"]) != ("KN", "M"):
        sys.exit(f"!! model units {unit}: this job expects kN, m")
    E = m["ELEM"]
    N = m["NODE"]
    # beam loads of one typical interior frame (Y = 10 m) and one end-wall post: the load basis of the secondary members
    bm = table("BMLD")
    keep = {k for k, e in E.items() if all(abs(N[str(n)]["Y"] - 10.0) < 1e-6 for n in e["NODE"][:2])}
    keep |= {k for k, e in E.items() if e["SECT"] == 102}
    m["BMLD_FRAME10"] = {k: {"ITEMS": [{f: it[f] for f in ("LCNAME", "DIRECTION", "USE_PROJECTION", "D", "P")}
                                       for it in v["ITEMS"] if not it["LCNAME"].startswith("N")]}
                         for k, v in bm.items() if k in keep}     # service cases only (NU* repeat them, factored)

    design = [v["NAME"] for v in m["STLD"].values() if v["NAME"].startswith("NU")]
    active = {c["LCNAME"] for v in m["LCOM-STEEL"].values() if v["ACTIVE"] == "STRENGTH" for c in v["vCOMB"]}
    if set(design) != active:
        print("  note: active steel-design combinations use", sorted(active - set(design)), "too")
    service = [v["NAME"] for v in m["STLD"].values() if v.get("TYPE") in ("D", "L", "W")]

    # joint nodes: supports, member ends (degree 1), and nodes where elements of different sections meet
    deg = collections.defaultdict(set)
    for k, e in E.items():
        for n in e["NODE"][:2]:
            deg[n].add((e["SECT"], k))
    joints = {n for n, s in deg.items() if len({sec for sec, _ in s}) > 1 or len(s) != 2}
    joints |= {int(n) for n in m["CONS"]}

    env = {}                     # "elem/part" -> component -> [max, case, min, case]
    conc = collections.defaultdict(dict)   # "elem/part" at a joint -> case -> [N, Vy, Vz, T, My, Mz]
    reac = {}
    comp = ("N", "Vy", "Vz", "T", "My", "Mz")
    for c in design + service:
        rows = result("BEAMFORCE", c)
        print(f"  {c:16s} {len(rows)} rows")
        if not rows:
            sys.exit(f"!! no results for {c}: run the analysis in GEN NX first")
        for r in rows:
            e, part = r[1], r[3][0]
            node = E[e]["NODE"][0 if part == "I" else 1]
            key = f"{e}/{part}"
            vals = [round(float(x), 2) for x in r[4:10]]
            if node in joints:
                conc[key][c] = vals
            if c in design:
                d = env.setdefault(key, {k: [-1e99, "", 1e99, ""] for k in comp})
                for k, v in zip(comp, vals):
                    if v > d[k][0]:
                        d[k][0:2] = [v, c]
                    if v < d[k][2]:
                        d[k][2:4] = [v, c]
        reac[c] = {r[1]: [round(float(x), 2) for x in r[3:9]] for r in result("REACTIONG", c)}
    forces = {"units": "kN, m", "design_cases": design, "service_cases": service, "components": list(comp),
              "joint_nodes": sorted(joints), "envelope": env, "concurrent": conc, "reactions": reac}
    out = HERE / "model"
    out.mkdir(exist_ok=True)
    (out / "spf_model.json").write_text(json.dumps(m, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    (out / "spf_forces.json").write_text(json.dumps(forces, separators=(",", ":")), encoding="utf-8")
    print(f"model: {len(N)} nodes, {len(E)} elements, {len(m['SECT'])} sections -> {out}")


if __name__ == "__main__":
    main()
