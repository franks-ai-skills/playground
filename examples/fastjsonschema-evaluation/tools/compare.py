"""Compare jsonschema (Draft 2020-12, as Forge uses it) with Draft-07 conversions under jsonschema and fastjsonschema.

Usage: python -I compare.py <forge checkout> <corpus.jsonl>... --out <report.json>

Validators per input:
  base  Draft202012Validator, original schema, registry of Forge's original schemas (Forge today)
  d7    Draft7Validator, converted schema, registry of converted schemas (isolates the conversion)
  fjs   fastjsonschema via fjs_config.compile_checked: metaschema check, absolute self-references,
        LocalOnly references, fast_fail=False (isolates the library). --no-absolutize and --fast-fail
        reproduce the earlier configuration.
"""
from __future__ import annotations

import argparse, copy, hashlib, json, random, sys
from collections import Counter, defaultdict
from pathlib import Path

import fastjsonschema
from jsonschema import Draft7Validator, Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT7, DRAFT202012

sys.path.insert(0, str(Path(__file__).parent))

from convert07 import DRAFT7_URI, absolutize, convert  # noqa: E402
from fjs_config import ERRORS, compile_checked  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("forge")
    parser.add_argument("corpus", nargs="+")
    parser.add_argument("--out", required=True)
    parser.add_argument("--mutations", type=int, default=40)
    parser.add_argument("--no-absolutize", action="store_true")
    parser.add_argument("--fast-fail", action="store_true")
    args = parser.parse_args()
    forge = Path(args.forge)

    originals = {}
    for path in sorted((forge / "schemas").glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        originals[schema["$id"]] = schema
    converted = {sid: convert(schema) for sid, schema in originals.items()}
    fjs_store = {sid: (schema if args.no_absolutize else absolutize(schema)) for sid, schema in converted.items()}

    base_registry = Registry().with_resources((sid, Resource(s, DRAFT202012)) for sid, s in originals.items())
    d7_registry = Registry().with_resources((sid, Resource(s, DRAFT7)) for sid, s in converted.items())
    for sid, s in converted.items():
        Draft7Validator.check_schema(s)

    cache = {}

    def validators(schema):
        key = json.dumps(schema, sort_keys=True)
        if key not in cache:
            conv = convert(schema)
            if "$schema" not in conv:
                conv = dict(conv, **{"$schema": DRAFT7_URI})
            entry = {"base": Draft202012Validator(schema, registry=base_registry),
                     "d7": Draft7Validator(conv, registry=d7_registry)}
            try:
                entry["fjs"] = compile_checked(conv, fjs_store, absolute=not args.no_absolutize,
                                               fast_fail=args.fast_fail)
            except Exception as error:  # noqa: BLE001 - reported
                entry["fjs_error"] = f"{type(error).__name__}: {error}"[:300]
            cache[key] = entry
        return cache[key]

    def run(schema, value):
        v = validators(schema)
        base = not any(True for _ in v["base"].iter_errors(value))
        d7 = not any(True for _ in v["d7"].iter_errors(value))
        if "fjs" not in v:
            return base, d7, "compile-error", None
        before = json.dumps(value, sort_keys=True)
        try:
            v["fjs"](value)
            fjs = True
        except ERRORS:
            fjs = False
        except Exception as error:  # noqa: BLE001 - reported
            return base, d7, f"crash {type(error).__name__}: {error}"[:200], None
        changed = json.dumps(value, sort_keys=True) != before
        return base, d7, fjs, changed

    rng = random.Random(4056)

    def mutations(value):
        """Paths to every node, then one-step changes; the baseline decides validity."""
        nodes = []

        def walk(node, path):
            nodes.append((path, node))
            if isinstance(node, dict):
                for k, sub in node.items():
                    walk(sub, path + [k])
            elif isinstance(node, list):
                for i, sub in enumerate(node):
                    walk(sub, path + [i])
        walk(value, [])

        def replaced(path, new, delete=False):
            out = copy.deepcopy(value)
            if not path:
                return new
            target = out
            for step in path[:-1]:
                target = target[step]
            if delete:
                del target[path[-1]]
            else:
                target[path[-1]] = new
            return out

        result = []
        for path, node in nodes:
            if path and isinstance(path[-1], str):
                result.append(("drop " + "/".join(map(str, path)), replaced(path, None, delete=True)))
            if isinstance(node, dict):
                result.append(("extra key at /" + "/".join(map(str, path)), replaced(path, dict(node, zz_extra=1))))
            if isinstance(node, str):
                result += [("newline " + "/".join(map(str, path)), replaced(path, node + "\n")),
                           ("empty " + "/".join(map(str, path)), replaced(path, "")),
                           ("int " + "/".join(map(str, path)), replaced(path, 7)),
                           ("long " + "/".join(map(str, path)), replaced(path, node * 50 + "x"))]
            elif isinstance(node, bool):
                result += [("str-bool " + "/".join(map(str, path)), replaced(path, "true")),
                           ("int-bool " + "/".join(map(str, path)), replaced(path, 1))]
            elif isinstance(node, int):
                result += [("neg " + "/".join(map(str, path)), replaced(path, -1)),
                           ("float " + "/".join(map(str, path)), replaced(path, node + 0.5)),
                           ("float-int " + "/".join(map(str, path)), replaced(path, float(node))),
                           ("bool-int " + "/".join(map(str, path)), replaced(path, True))]
            elif isinstance(node, list):
                result.append(("empty list " + "/".join(map(str, path)), replaced(path, [])))
                if node:
                    result.append(("dup item " + "/".join(map(str, path)), replaced(path, node + [node[0]])))
            elif node is None:
                result.append(("null->str " + "/".join(map(str, path)), replaced(path, "x")))
        rng.shuffle(result)
        return result

    stats = Counter()
    mismatches = defaultdict(list)
    compile_errors = {}
    changed_inputs = 0
    entries = []
    for corpus in args.corpus:
        for line in Path(corpus).read_text(encoding="utf-8").splitlines():
            entries.append(json.loads(line))

    for entry in entries:
        schema, value = entry["schema"], entry["value"]
        sid = schema.get("$id", "(sub-schema " + hashlib.sha256(json.dumps(schema, sort_keys=True).encode()).hexdigest()[:8] + ")")
        cases = [("recorded", value)]
        cases += mutations(value)[: args.mutations]
        for label, case in cases:
            try:
                base, d7, fjs, changed = run(schema, case)
            except Exception as error:  # noqa: BLE001
                stats["harness-error"] += 1
                mismatches["harness-error"].append({"schema": sid, "case": label, "error": str(error)[:200]})
                continue
            if fjs == "compile-error":
                compile_errors[sid] = validators(schema)["fjs_error"]
                stats["fjs-compile-error"] += 1
                continue
            stats["checked"] += 1
            stats["base-valid" if base else "base-invalid"] += 1
            if changed:
                changed_inputs += 1
            if base != d7:
                kind = "conversion"
            elif d7 != fjs:
                kind = "library"
            else:
                continue
            stats[kind] += 1
            stats[f"{kind}-by-schema:{sid}"] += 1
            if label == "recorded":
                stats[f"{kind}:recorded"] += 1
            stats[f"{kind}:{label.split(' ')[0]}:{(base, d7, fjs)}"] += 1
            if len(mismatches[kind]) < 400 and not label.startswith("newline"):
                mismatches[kind].append({"schema": sid, "case": label, "base": base, "d7": d7, "fjs": fjs,
                                         "value": json.dumps(case, sort_keys=True)[:400]})
    report = {"configuration": {"absolutize": not args.no_absolutize, "fast_fail": args.fast_fail,
                                "mutations": args.mutations, "corpus": [
                                    {"file": Path(c).name, "sha256": hashlib.sha256(Path(c).read_bytes()).hexdigest()}
                                    for c in args.corpus]},
              "entries": len(entries), "stats": dict(stats), "inputs_changed_by_fjs": changed_inputs,
              "compile_errors": compile_errors,
              "schemas_seen": sorted({e["schema"].get("$id", "(sub-schema)") for e in entries}),
              "mismatches": mismatches}
    Path(args.out).write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("configuration", "entries", "stats", "inputs_changed_by_fjs")}, indent=1))
    print("compile errors:", json.dumps(compile_errors, indent=1)[:2000])
    for kind, items in mismatches.items():
        print(f"== {kind}: {len(items)} (first shown)")
        by = Counter((m["schema"], m["case"].split(" ")[0]) for m in items)
        for (s, c), n in by.most_common(25):
            print(f"   {n:4d}  {s}  {c}")


if __name__ == "__main__":
    main()
