"""Record real records as corpus lines: decisions, research, revisions, reports (their report data
block), runtime cases, and the KB's rules, selection, coverage and catalog.

Usage: python -I record_files.py <forge checkout> <out.jsonl> <dir>...
"""
import json, re, sys
from pathlib import Path

sys.path[:0] = [str(Path(sys.argv[1]) / "src")]
from harness_forge import documents  # noqa: E402

REPORT_DATA = re.compile(r"^## Report data\r?\n\r?\n```json\r?\n(.*?)\r?\n```", re.S | re.M)


def classify(rel, path):
    if path.suffix == ".md" and "/.harness/decisions/" in rel:
        return "decision"
    if path.suffix == ".md" and "/.harness/research/" in rel:
        return "research"
    if path.suffix == ".md" and "/.harness/reports/" in rel:
        return "report"
    if rel.endswith(".rules.yaml"):
        return "revision"
    if rel.endswith("/.harness/cases.yaml"):
        return "runtime-cases"
    for name in ("selection", "coverage"):
        if rel.endswith(f"/rules/{name}.yaml"):
            return name
    if rel.endswith("/checks/catalog.yaml"):
        return "catalog"
    if "/rules/" in rel and path.suffix == ".yaml":
        return "rules"
    return None


out, counts = open(sys.argv[2], "w"), {}
for root in map(Path, sys.argv[3:]):
    for path in sorted(root.rglob("*")):
        rel = path.as_posix()
        schema = classify(rel, path) if path.is_file() and ".git" not in path.parts else None
        if not schema:
            continue
        text = path.read_text(encoding="utf-8")
        if schema == "report":
            found = REPORT_DATA.findall(text)
            if len(found) != 1:
                counts["report without one data block"] = counts.get("report without one data block", 0) + 1
                continue
            value = json.loads(found[0])
        else:
            value = documents.parse_yaml(documents.split_frontmatter(text)[0] if path.suffix == ".md" else text)
        errors = documents.schema_errors(value, documents.schema_named(schema))
        out.write(json.dumps({"schema": documents.schema_named(schema), "value": value, "errors": len(errors),
                              "file": rel}) + "\n")
        counts[schema] = counts.get(schema, 0) + 1
print(json.dumps(counts, sort_keys=True))
