# fastjsonschema evaluation: scripts and outputs

Scripts and outputs behind
[the evaluation report](../../plans/2026-10-24-fastjsonschema-evaluation.md)
(harness-forge#46). The corpora are not published: they hold
hands-on records. Their sha256 hashes are in the `out-*.txt` files.

| File | What it is |
|---|---|
| `tools/convert07.py` | Draft 2020-12 → Draft-07 conversion, and the absolute self-reference workaround |
| `tools/fjs_config.py` | fastjsonschema in the adoption configuration |
| `tools/record_suite.py`, `tools/record_files.py` | Build the corpora |
| `tools/compare.py` | Three-way comparison with mutations |
| `tools/probes.py` | Targeted probes |
| `tools/bundle_smoke.py` | Bundle prototype under `python -I -S -B` |
| `out-suite.txt`, `out-files.txt` | Comparison in the adoption configuration |
| `out-suite-noabs.txt` | Comparison without the workaround, `fast_fail=True` |
| `out-probes.txt` | Probe results |

`fjs_config.py` reads `tools/draft-07.schema.json`, which is not
published. Copy `jsonschema_specifications/schemas/draft7/metaschema.json`
from jsonschema-specifications 2025.9.1 (sha256 `3d5392088261606c559b603f385329c9f1ab45b5d667eb990687453b055d405e`)
to that path.
