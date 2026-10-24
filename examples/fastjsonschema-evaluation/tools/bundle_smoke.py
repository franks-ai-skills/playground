"""Run with python -I -S: Forge's YAML, Markdown and (converted) schema validation from the bundle alone."""
import json, sys, types
from pathlib import Path
bundle, forge, record = sys.argv[1:4]
sys.path[:0] = [bundle, str(Path(forge) / "src"), str(Path(__file__).parent)]
for name in ("jsonschema", "jsonschema.exceptions", "referencing"):  # documents.py imports them at module level
    stub = types.ModuleType(name); stub.Draft202012Validator = stub.SchemaError = stub.Registry = stub.Resource = object
    sys.modules[name] = stub
import yaml, markdown_it, fastjsonschema
from harness_forge import documents
from convert07 import convert
print("site-packages on path:", any("site-packages" in p for p in sys.path), "| libyaml:", yaml.__with_libyaml__)
print("modules from outside bundle/forge/stdlib:", sorted({m.__name__.split('.')[0] for m in list(sys.modules.values())
      if getattr(m, "__file__", None) and not m.__file__.startswith((bundle, forge, sys.base_prefix, str(Path(__file__).parent)))}))
text = Path(record).read_text(encoding="utf-8")
front, body = documents.split_frontmatter(text)
value = documents.parse_yaml(front)
for bad in ("a: yes\n", "a: 1\na: 2\n", "a: !!python/object/apply:os.system [x]\n"):
    try: documents.parse_yaml(bad); print("  strict YAML accepted", repr(bad))
    except Exception as e: print("  strict YAML rejects", repr(bad), "->", type(e).__name__)
print("date kept as string:", documents.parse_yaml("d: 2026-10-24\n"))
print("markdown anchors:", sorted(documents.heading_anchors("# Title\n\n## Part A: build\n\ntext\n"))[:5])
from fjs_config import compile_checked, ERRORS
from convert07 import absolutize
schemas = {}
for p in (Path(forge) / "schemas").glob("*.schema.json"):
    s = convert(json.loads(p.read_text())); schemas[s["$id"]] = s
store = {k: absolutize(v) for k, v in schemas.items()}
check = compile_checked(schemas["urn:harness-forge:schema:decision"], store)
check(value); print("decision record valid under converted schema: yes")
value["goals"][0] = {"a": "b"}
try: check(value); print("broken goal accepted!")
except ERRORS as e: print("broken goal rejected:", [x.message for x in getattr(e, "errors", [e])])
