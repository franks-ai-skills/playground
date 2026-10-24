"""Run Forge's unittest suite in-process and record every value checked by documents.schema_errors.

Usage: python -I record_suite.py <forge checkout> <out.jsonl>
"""
import hashlib, json, sys, unittest
from pathlib import Path

forge, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
sys.path[:0] = [str(forge / "src"), str(forge)]
from harness_forge import documents  # noqa: E402

seen, sink = set(), out.open("w", encoding="utf-8")
original = documents.schema_errors


def recording(value, schema):
    result = original(value, schema)
    try:
        line = json.dumps({"schema": schema, "value": value, "errors": len(result)}, sort_keys=True)
    except (TypeError, ValueError):
        return result
    key = hashlib.sha256(line.encode()).hexdigest()
    if key not in seen:
        seen.add(key)
        sink.write(line + "\n")
    return result


documents.schema_errors = recording
suite = unittest.defaultTestLoader.discover(str(forge / "tests"), top_level_dir=str(forge))
result = unittest.TextTestRunner(stream=sys.stderr, verbosity=0).run(suite)
sink.close()
print(json.dumps({"tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
                  "skipped": len(result.skipped), "recorded": len(seen)}))
