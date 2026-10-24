"""Targeted probes for the fastjsonschema evaluation, in the adoption configuration (fjs_config).

Usage: python -I probes.py <forge checkout> <kb checkout>
Prints one line per probe; urllib.request.urlopen is patched to refuse and count retrieval attempts.
"""
import json, sys, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fastjsonschema  # noqa: E402
import yaml  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402
from jsonschema.exceptions import SchemaError  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

from convert07 import DRAFT7_URI, absolutize, convert  # noqa: E402
from fjs_config import ERRORS, LocalOnly, check_schema, compile_checked  # noqa: E402

forge, kb = Path(sys.argv[1]), Path(sys.argv[2])
attempts = []


def refuse(*args, **kwargs):
    attempts.append(args[0] if args else kwargs)
    raise OSError("retrieval refused by the evaluation")


urllib.request.urlopen = refuse
originals = {}
for path in sorted((forge / "schemas").glob("*.schema.json")):
    schema = json.loads(path.read_text(encoding="utf-8"))
    originals[schema["$id"]] = schema
converted = {sid: convert(s) for sid, s in originals.items()}
store = {sid: absolutize(s) for sid, s in converted.items()}
registry = Registry().with_resources((sid, Resource(s, DRAFT202012)) for sid, s in originals.items())
PRED = "urn:harness-forge:schema:predicate"


def accepts(validate, value):
    try:
        validate(value)
        return True
    except ERRORS:
        return False


print("## 1. Forge's 18 converted schemas against the Draft-07 metaschema")
for sid, s in converted.items():
    check_schema(s)
print("all pass")

print("\n## 2. Scope bug: a local $ref inside a schema reached through a reference (predicate's \"#\")")
outer_open = {"$schema": DRAFT7_URI, "$id": "urn:harness-forge:schema:probe", "type": "object",
              "properties": {"p": {"$ref": PRED}}}
outer_closed = {"$schema": DRAFT7_URI, "type": "object", "properties": {"p": {"$ref": PRED}},
                "additionalProperties": False}
bad, good = {"p": {"all": [{"eq": [1, 2, 3]}]}}, {"p": {"all": [{"eq": ["job", "x"]}]}}
for label, outer in (("open outer schema", outer_open), ("closed outer schema", outer_closed)):
    base = Draft202012Validator({k: v for k, v in outer.items() if k != "$schema"}, registry=registry)
    plain = fastjsonschema.compile(outer, handlers=LocalOnly(converted), use_default=False, use_formats=False)
    fixed = compile_checked(outer, store)
    print(f"{label}: invalid value accepted by jsonschema={base.is_valid(bad)} "
          f"fastjsonschema={accepts(plain, bad)} with-workaround={accepts(fixed, bad)}; "
          f"valid value accepted by jsonschema={base.is_valid(good)} fastjsonschema={accepts(plain, good)} "
          f"with-workaround={accepts(fixed, good)}")

print("\n## 3. Schema definitions: (2020-12 check_schema, Draft-07 metaschema after conversion, compile alone)")
MALFORMED = [{"type": 5}, {"type": "strin"}, {"properties": []}, {"required": "x"}, {"required": [1]},
             {"pattern": "("}, {"minItems": -1}, {"maxLength": "3"}, {"additionalProperties": "no"},
             {"items": 5}, {"enum": "a"}, {"$ref": 5}, {"properties": {"a": 5}}, {"minimum": "1"},
             {"patternProperties": {"(": {}}}, {"uniqueItems": "yes"}, {"oneOf": []}, {"anyOf": {}},
             {"type": "object", "$defs": {"bad": {"required": [1]}}},
             {"type": "array", "items": {"$ref": "#/$defs/n"}, "$defs": {"n": {"minItems": -1}}}]


def judge(schema):
    try:
        Draft202012Validator.check_schema(schema)
        base = "accepts"
    except SchemaError:
        base = "rejects"
    try:
        conv = dict(convert(schema), **{"$schema": DRAFT7_URI})
    except Exception as error:  # noqa: BLE001
        return base, f"conversion refused ({type(error).__name__})", "-"
    try:
        check_schema(conv)
        meta = "accepts"
    except ERRORS:
        meta = "rejects"
    try:
        fastjsonschema.compile(absolutize(conv), handlers=LocalOnly(store), use_default=False, use_formats=False)
        comp = "accepts"
    except Exception:  # noqa: BLE001
        comp = "rejects"
    return base, meta, comp


for schema in MALFORMED:
    print(f"{json.dumps(schema):75s} {judge(schema)}")
catalog = yaml.safe_load((kb / "checks" / "catalog.yaml").read_text(encoding="utf-8"))
results = [judge(c["params"]) for c in catalog["checkers"]]
print(f"KB catalog parameter schemas: {len(results)}, all three accept: "
      f"{all(r == ('accepts', 'accepts', 'accepts') for r in results)}")

print("\n## 4. References in the adoption configuration (LocalOnly): retrieval attempts and outcome")
for ref in ["urn:harness-forge:schema:predicate", "urn:harness-forge:schema:predicate#/definitions/x",
            "urn:harness-forge:schema:nope", "urn:other:thing", "http://example.invalid/s.json",
            "https://example.invalid/s.json", "file:///etc/hosts", "ftp://example.invalid/x",
            "data:application/json,{}", "relative/other.json", "//example.invalid/s"]:
    before = len(attempts)
    schema = {"$schema": DRAFT7_URI, "$id": "urn:harness-forge:schema:probe", "properties": {"a": {"$ref": ref}}}
    try:
        compile_checked(schema, store)
        outcome = "compiled"
    except Exception as error:  # noqa: BLE001
        outcome = f"refused ({type(error).__name__})"
    print(f"{ref:52s} attempts={len(attempts) - before} {outcome}")
before = len(attempts)
try:
    fastjsonschema.compile({"$schema": DRAFT7_URI, "properties": {"a": {"$ref": "urn:harness-forge:schema:predicate"}}},
                           use_default=False, use_formats=False)
except Exception:  # noqa: BLE001
    pass
print(f"default handlers, urn reference: attempts={len(attempts) - before} (fastjsonschema falls back to urlopen)")

print("\n## 5. Error reporting with fast_fail=False")
s = {"$schema": DRAFT7_URI, "type": "object", "properties": {"a": {"type": "string"}, "b": {"type": "integer"},
     "c": {}}, "required": ["a", "b", "c"], "additionalProperties": False}
try:
    compile_checked(s, store)({"a": 1, "b": "x", "z": 0})
except ERRORS as error:
    print([e.message for e in getattr(error, "errors", [error])])
