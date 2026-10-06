# Examples

> **Copied** from [`konohatrong/midas_API`](https://github.com/konohatrong/midas_API/blob/b4155ac/examples/README.md) (`examples/README.md`, commit b4155ac, 2026-10-04) into this repository's `midas/` folder. Paths in the text such as `To midas/…`, `pilot project/…` or the root `README.md` name that repository; the map is in [`midas/README.md`](../README.md).

Runnable scripts for the MIDAS GEN NX API. Install the library first:

```bash
pip install midas-gen
```

Get a MAPI-Key from GEN NX → Apps → API Settings → Refresh, then provide it via
`--key`, the `MIDAS_MAPI_KEY` env var, or `config.json` (`{"mapi_key": "..."}`)
at the repo root. **Never commit `config.json`** (it is git-ignored).

| Script | What it shows | Needs GEN NX running? |
|--------|---------------|-----------------------|
| [`analyze_and_report.py`](analyze_and_report.py) | Build a portal frame → **run analysis** (`/doc/ANAL`) → read reactions / displacements / beam forces (`/post/table`) | **Yes** (uses the live solver) |

```bash
python examples/analyze_and_report.py --key <YOUR_MAPI_KEY>
```

See [`../docs/CONVENTIONS.md`](../api/CONVENTIONS.md) for the rules these examples
follow, and the root [`README.md`](../api/MAPI_GUIDE.md) for the full API guide.
