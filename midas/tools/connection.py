"""Connect to MIDAS GEN NX with regional fallback (the autoURL probe is flaky)."""
import sys as _sys

# UTF-8 guard MUST run before midas_gen is imported (banner crashes cp874).
for _s in (_sys.stdout, _sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

REGIONAL = [
    "https://moa-engineers-kr.midasit.com:443/gen",
    "https://moa-engineers.midasit.com:443/gen",
    "https://moa-engineers-us.midasit.com:443/gen",
    "https://moa-engineers-in.midasit.com:443/gen",
    "https://moa-engineers-gb.midasit.com:443/gen",
]


def connect(key: str, base_urls=None) -> str:
    """Set the key, find a working base URL, return it. Raises if none works."""
    import midas_gen as mg
    mg.MAPI_KEY(key)
    for url in (base_urls or REGIONAL):
        mg.MAPI_BASEURL(url)
        try:
            if "PROJECTSTATUS" in mg.MidasAPI("GET", "/ope/PROJECTSTATUS"):
                return url
        except Exception:
            pass
    raise ConnectionError(
        "Could not reach GEN NX. Open it, click Apps > Connect, refresh the key.")
