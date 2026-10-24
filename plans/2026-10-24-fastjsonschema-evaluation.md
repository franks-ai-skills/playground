# Evaluation: fastjsonschema instead of jsonschema, to ship Forge's dependencies in the plugin

Date: 2026-10-24. Baseline: harness-forge `4056c94` (Forge 0.2.0), KB
snapshot 0.2.0. Context: harness-forge#46. Offline only; nothing in the
repositories changed.

**Conclusion.** Shipping all dependencies inside the plugin appears
feasible with fastjsonschema 2.22.2. Adoption requires converting
Forge's schemas to Draft-07, extra validation safeguards (schema checks
against the metaschema, references that fail closed), a workaround for a
fastjsonschema reference bug, and testing on more Python versions and
platforms. It would reverse the packaging decision of 2026-10-09.

## Question

Can Forge ship its runtime dependencies inside the plugin, so that
nothing is downloaded during use? The blocker is `rpds-py`, a compiled
Rust module that `jsonschema` 4.26.0 imports directly, also through
`referencing`. The candidate replacement is fastjsonschema, which is
pure Python.

## Installed for the evaluation

A scratch virtual environment only: Forge's `requirements.lock` plus
`fastjsonschema==2.22.2`. The wheel is `py3-none-any`, sha256
`0fb3915616adac85ccfdd737d26be1089845d2019819505b42d39888458f74d4`,
BSD-3-Clause, with no dependencies. It was installed with
`--require-hashes --only-binary :all:`. Reason: the owner asked to
explore it, and Codex agreed.

## Method

1. **Conversion** (`convert07.py`). Forge's 18 schemas declare Draft
   2020-12, which fastjsonschema does not implement. It implements 04,
   06 and 07. A schema that declares 2020-12 silently gets its 2019
   generator, which is Draft-07 plus a few formats and **ignores
   `prefixItems`**. The converter rewrites copies to Draft-07:
   - `$schema` becomes Draft-07.
   - `prefixItems` + `items` become the array form of `items` +
     `additionalItems`. There are 2 uses, both in `predicate`.
   - `$defs` becomes `definitions`, with every `#/$defs/` reference
     rewritten. Draft-07's metaschema does not look inside `$defs`.

   The converter refuses an enumerated set of 2020-12 keywords and any
   `$ref` with siblings. Forge's schemas have no `$ref` with siblings.
   That set is not every keyword Draft-07 lacks. All 18 converted
   schemas pass Draft-07's metaschema.
2. **Three validators per input** (`compare.py`):
   - `base` is Forge today: `Draft202012Validator` on the original
     schemas with a `referencing.Registry`.
   - `d7` is `Draft7Validator` on the converted schemas. It isolates
     the conversion.
   - `fjs` is fastjsonschema in the configuration an adoption would use
     (`fjs_config.py`): the schema is checked against the Draft-07
     metaschema before compiling; self-references are absolute (the
     workaround below); references resolve only to local schemas
     (`LocalOnly`); `fast_fail=False`; `use_default=False` and
     `use_formats=False`. It isolates the library.
3. **Corpus.**
   - (a) `corpus-suite.jsonl`, 1027 entries, sha256 `3e292f2e…`: every
     value that Forge's test suite passed through
     `documents.schema_errors` in-process and that serializes to JSON.
     The full suite ran with that function instrumented (797 tests OK,
     `record_suite.py`). Calls made in subprocesses were not recorded.
     The corpus covers named schemas and sub-schemas such as KB checker
     parameters.
   - (b) `corpus-files.jsonl`, 80 entries, sha256 `7154c061…`: real
     records (`record_files.py`): 18 decisions, 18 research files, 17
     accepted-requirement revisions, 17 report data blocks and 4
     runtime-case files from Forge's self-verification and the recorded
     test runs, plus the pinned KB snapshot (rules, selection, coverage,
     catalog). All are valid today.
   - (c) Seeded one-step mutations: up to 60 per entry in (a) and up to
     300 per entry in (b). They drop each key; add an extra key; turn a
     string into empty, an int, 50 copies or the string plus a trailing
     newline; a bool into `"true"` or 1; an int into −1, x.5, a float or
     a bool; a list into an empty list or one with a duplicate item; and
     null into a string. The baseline decides whether each result is
     valid.
4. **Targeted probes** (`probes.py`, adoption configuration): schema
   definition checks, the reference bug before and after the
   workaround, reference resolution with `urllib.request.urlopen`
   patched to refuse and count attempts, and error reporting.
5. **Bundle prototype** (`bundle_smoke.py`) under `python -I -S -B`.

## Results

### Accept/reject agreement (adoption configuration)

82,439 checks: 58,889 on (a) and 23,550 on (b). Under the baseline,
24,854 were valid and 57,585 invalid.

- **Conversion** (`base` vs `d7`): **0 differences.**
- **Library** (`d7` vs `fjs`): **one kind of difference only, 4,520
  cases (2,919 + 1,601): a string with a trailing newline.**
  - jsonschema accepts `"abc\n"` for `^[a-z]+$`, because Python's `$`
    also matches before a final newline.
  - fastjsonschema rejects it, because it rewrites `$` to `\Z`. It is
    the stricter one.
  - Side finding: Forge today accepts IDs, slugs and digests with a
    trailing newline. That is a separate issue, independent of the
    validator.
- fastjsonschema never modified an input. This was checked on every
  case.

### A fastjsonschema bug, and a workaround

Inside a schema reached through a reference, fastjsonschema 2.22.2
resolves that schema's own local references (`"$ref": "#"`) against the
**outer** schema, not the referenced one. Probe 2 ([`out-probes.txt`](../examples/fastjsonschema-evaluation/out-probes.txt)):

- With an open outer schema, it **accepts** `{"all":[{"eq":[1,2,3]}]}`,
  which Forge rejects.
- With a closed outer schema, it **rejects** a valid predicate.
- With every local `$ref` written as an absolute reference to the
  schema's own `$id` (`urn:…:predicate#…`), both cases match Forge.

On the corpus, without the workaround and with `fast_fail=True`
([`out-suite-noabs.txt`](../examples/fastjsonschema-evaluation/out-suite-noabs.txt)), there were 3,858 differences instead of 2,919.
The extra 939 are 747 non-newline cases and 192 more newline cases. 49
of the non-newline cases are on recorded suite values. The extra cases
are all in KB checker parameter schemas that reference
`urn:harness-forge:schema:predicate`.

Upstream: no report of this bug was found. The related regression
horejsek/python-fastjsonschema#218 (relative references in
handler-loaded schemas resolved twice) was fixed on `master` by PR #219
(`c9a311e`, 2026-08-23). `master` is 12 commits ahead of the latest tag,
`v2.22.2`, so that fix is unreleased. So is "Fix numeric keywords being
applied to booleans" (`3926b2e`); its effect did not appear in this
corpus. Whether `master` fixes the scope bug was not tested.

### Schema definitions

fastjsonschema has no `check_schema`. Compiling a schema is **not** a
substitute: 8 of 20 malformed schemas compiled without error (probe 3).
Validating the converted schema against the Draft-07 metaschema with
fastjsonschema itself (`use_formats=True`, so `pattern` regexes are
checked) rejected all 18 schemas that the converter accepted. That
includes malformed definitions under `$defs`, once these are converted
to `definitions`. Without that conversion they would pass, because
Draft-07's metaschema does not look inside `$defs`.

The converter crashed on the other 2 (`{"properties": []}`,
`{"$ref": 5}`). After adoption the schemas would be stored as Draft-07
and nothing would be converted at run time, but Forge itself would
have to reject such input cleanly.

All 14 KB checker parameter schemas pass all three checks. Forge would
ship the Draft-07 metaschema (see Bundle) and check every schema it
compiles.

### References and retrieval

With fastjsonschema's default handlers, every reference whose scheme
has no handler goes to `urllib.request.urlopen`, including a `urn:`
reference. These are retrieval attempts; for `file:` and `data:` they
are not network access. With the `LocalOnly` handler mapping, all 11
probed references made 0 retrieval attempts: local IDs resolved, and
unknown `urn:`, http(s), file, ftp, data, relative and scheme-relative
references were refused (probe 4). `LocalOnly` relies on fastjsonschema
checking `scheme in handlers` before it falls back to `urlopen`, so a
Forge test must pin that behavior.

### Error reporting

With `fast_fail=False`, fastjsonschema reports every error, as Forge
does today; on all 1027 recorded suite values Codex confirmed no
accept/reject difference in that mode. The wording and path form
differ: `data.goals[0] must be string` versus
`goals/0: … is not of type 'string'`. One Forge test asserts jsonschema
wording (`is not one of`). fastjsonschema also refuses some
unsatisfiable schemas when compiling, for example a required property
that `additionalProperties: false` forbids.

### Bundle prototype

A component prototype, not a working bundled Forge command line:
`documents.py` still imports jsonschema, so the test puts stand-in
modules in its place, and it uses the converter and `fjs_config` from
the evaluation's tools directory.

Contents: 121 files, 585,011 bytes without `__pycache__`. Only
pure-Python files, no compiled module:

| Content | Bytes | License |
|---|---|---|
| PyYAML 6.0.3: `lib/yaml` from the sdist, sha256 checked against `requirements.lock` | 217,506 | MIT |
| markdown-it-py 4.2.0, with dist-info | 244,684 | MIT |
| mdurl 0.1.2, with dist-info | 23,308 | MIT |
| fastjsonschema 2.22.2, with dist-info | 93,593 | BSD-3-Clause |
| Draft-07 metaschema (`draft7/metaschema.json` from jsonschema-specifications 2025.9.1, sha256 `3d539208…`) | 4,819 | to verify before shipping |
| licence files | 1,101 | |

PyYAML's libyaml extension is optional. Forge's strict loader already
uses the pure-Python `SafeLoader`, so its speed does not change.
`jsonschema`, `referencing`, `rpds-py`, `attrs`,
`jsonschema-specifications` and `typing-extensions` would no longer be
needed.

Run with `python3.14 -I -S -B`, without site-packages, the prototype
worked:
- Strict YAML: rejects `yes`, duplicate keys and Python tags; dates
  stay strings.
- Markdown: heading anchors.
- Validation: a real decision record passed against the converted
  schema in the adoption configuration, and a broken goal was rejected.

No module from outside the bundle, Forge, the evaluation tools and the
standard library was loaded. Python 3.11–3.13 were not available
locally and are untested. The packages require Python ≥3.10; Forge
needs ≥3.11.

## What adoption would take

1. **An owner decision.** It reverses `packaging/assessment.md`
   (2026-10-09), which kept Draft 2020-12 and forbade changing formats
   to ease packaging.
2. **Forge:**
   - The 18 schemas move to Draft-07, with `definitions` and absolute
     self-references.
   - `documents.py` moves to fastjsonschema with `LocalOnly`, a
     metaschema check before every compile, `fast_fail=False` and a
     compile cache, and rejects malformed schema input cleanly.
   - Tests for the reference bug, retrieval failing closed, the
     metaschema check of `definitions`, and the newline behavior.
   - `test_dependency_conformance.py` is rewritten, and the one wording
     test is updated.
   - A vendored directory with licence files, the metaschema with its
     provenance, and a script that refreshes it from hash-checked
     downloads.
   - `setup.py`, `requirements.lock` and the environment switch in
     `forge.py` are removed or reduced to a fallback.
   - The README dependency section (#46).
3. **KB:** its six byte-identical schema copies change. That means a KB
   release (0.4.0), a Forge re-pin and a new self-verification record.
4. **Risks to accept:**
   - fastjsonschema turns each schema into Python source and executes
     it. Forge would compile its own schemas and the pinned snapshot's
     checker parameter schemas, after the metaschema check. The public
     `forge.py validate-kb --kb <directory>` command, however, would
     compile parameter schemas from whatever directory it is given.
     fastjsonschema escapes the values it writes into generated code,
     but that path would need its own review or a restriction to the
     pinned snapshot.
   - fastjsonschema's next release carries 12 unreleased commits,
     including reference-resolution changes. Re-run this evaluation
     before any upgrade.

## Not covered

Python 3.11–3.13 and other platforms; Codex as the host harness; the
`--wheelhouse` path; values checked in subprocesses; fastjsonschema
`master`; live runs (none needed). Agreement on this corpus shows
compatibility for these cases, not complete equivalence.

## Reproduce

Scripts and outputs are in [`examples/fastjsonschema-evaluation/`](../examples/fastjsonschema-evaluation/). Run the scripts with a venv that has Forge's
`requirements.lock` plus fastjsonschema 2.22.2, and copy
`jsonschema_specifications/schemas/draft7/metaschema.json` to
`tools/draft-07.schema.json`.

```
python -I tools/record_suite.py <forge> corpus-suite.jsonl          # in the Forge checkout; runs the suite
python -I tools/record_files.py <forge> corpus-files.jsonl <dirs>   # .harness/ and snapshot directories
python -I tools/compare.py <forge> corpus-suite.jsonl --out r.json --mutations 60
python -I tools/compare.py <forge> corpus-files.jsonl --out r.json --mutations 300
python -I tools/compare.py <forge> corpus-suite.jsonl --out r.json --mutations 60 --no-absolutize --fast-fail
python -I tools/probes.py <forge> <kb>
python3.14 -I -S -B tools/bundle_smoke.py <bundle> <forge> <decision record>
```

The corpora contain hands-on records and are not published. Their
sha256 hashes are in the outputs (`out-*.txt`).
