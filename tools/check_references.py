#!/usr/bin/env python3
"""Check the stored reference runs in examples/ against Harness Forge (plan task 14).

Run it with Forge's environment from the playground root:

    ../harness-forge/.venv/bin/python tools/check_references.py [--forge ../harness-forge] [example ...]

An example is a result repository, such as
examples/reproduction-checklist/codex/, with an `expected.yaml`:

    harness: codex
    slug: bug-reproduction-checklist
    parts:
      A: {harness_result: verified, goal_result: met by the verified build}

Each example must hold schema-valid decision, research, revision and report
records; one accepted revision bound by the decision and the report; file
hashes and links as the report recorded them; only accepted requirements in
each built SKILL.md; an Outside controls section that lists every control;
per part exactly the rules Forge applies today; the expected result labels;
and, for a built skill, runtime cases of this run and these files that
activate it and one that must not. Exit 0 when every example passes, 1 with
each problem listed, 2 without any example.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

PLAYGROUND = Path(__file__).resolve().parents[1]


def _forge(path: Path):
    sys.path.insert(0, str(path / "src"))
    from harness_forge import build_skill, documents, overrides, research, scope, verify  # noqa: E402
    from harness_forge.checks.outside import check_readme_coverage  # noqa: E402
    from harness_forge.contracts import load_decision  # noqa: E402
    from harness_forge.models import Rule  # noqa: E402
    return {"build_skill": build_skill, "documents": documents, "overrides": overrides, "research": research,
            "scope": scope, "verify": verify, "coverage": check_readme_coverage, "load_decision": load_decision,
            "Rule": Rule, "snapshot": path / "snapshot"}


def _report_data(text: str, documents) -> dict:
    bounds = documents.markdown_section(text, "Report data")
    blocks = re.findall(r"\A## Report data\r?\n\r?\n```json\r?\n(.*?)\r?\n```", text[slice(*bounds)], re.S) if bounds else []
    if len(blocks) != 1:
        raise ValueError("no single report data block")
    data = json.loads(blocks[0])
    documents.validate(data, "report")
    return data


def _one(paths: list[Path], what: str) -> Path:
    if len(paths) != 1:
        raise ValueError(f"expected one {what}, found {len(paths)}")
    return paths[0]


def check_example(root: Path, forge: dict) -> list[str]:
    """Every problem with one stored reference run; empty when it passes."""
    documents = forge["documents"]
    expected = documents.parse_yaml((root / "expected.yaml").read_text(encoding="utf-8"))
    slug, harness = expected["slug"], expected["harness"]
    decision = forge["load_decision"](_one(sorted((root / ".harness" / "decisions").glob("*.md")), "decision record"),
                                      root=root)
    forge["research"].load_research(root / ".harness" / "research" / f"{slug}.md", root=root)
    revision = forge["research"].load_revision(root / ".harness" / "research" / f"{slug}.rules.yaml", root=root)
    report_text = (root / ".harness" / "reports" / f"{slug}.md").read_text(encoding="utf-8")
    report = _report_data(report_text, documents)
    _, parts = forge["scope"].earlier_run(report_text)
    problems = []

    recorded = (decision.record.get("accepted_revision") or {}).get("digest")
    if not (recorded == revision.digest == report["revision_digest"]):
        problems.append(f"revision digests differ: decision {recorded}, rules file {revision.digest}, "
                        f"report {report['revision_digest']}")

    for path, digest in report["file_hashes"].items():
        target = root / path
        if target.is_symlink() or not target.is_file():
            problems.append(f"{path}: recorded in the report but not a file")
        elif hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            problems.append(f"{path}: changed since the report")
    for path, link in report["symlinks"].items():
        if not (root / path).is_symlink() or os.readlink(root / path) != link:
            problems.append(f"{path}: not the link {link} the report recorded")

    accepted: dict[str, list[dict]] = {}
    for entry in revision.rules:
        accepted.setdefault(entry["part_id"], []).append(entry["rule"])
    for part in decision.record["parts"]:
        if forge["verify"].part_kind(part) != "build":
            continue
        skill = root / ".agents" / "skills" / part["slug"] / "SKILL.md"
        text = skill.read_text(encoding="utf-8") if skill.is_file() else ""
        bounds = documents.markdown_section(text, "Requirements")
        stated = [line for line in text[slice(*bounds)].splitlines()[1:] if line.strip()] if bounds else []
        wanted = [f"{number}. {forge['build_skill']._rule_line(rule)}."
                  for number, rule in enumerate(accepted.get(part["id"], []), 1)]
        if stated != wanted:
            problems.append(f"part {part['id']}: SKILL.md requirements {stated} are not the accepted {wanted}")

    controls = [{"part_id": part["id"], "control": control["control"]}
                for part in decision.record["parts"] for control in part["outside_controls"]]
    readme = {"README.md": (root / "README.md").read_bytes()} if (root / "README.md").is_file() else {}
    status, reason = forge["coverage"](readme, {"outside_controls": controls},
                                       {"heading": "Outside controls", "status": "recommended, not verified"})
    if status != "pass":
        problems.append(f"README.md: {reason}")

    pinned = []
    for name in ("skills", "security", "outside-controls"):
        pinned += [forge["Rule"].from_dict(rule)
                   for rule in documents.load_document(forge["snapshot"] / "rules" / f"{name}.yaml", "rules")]
    rules = forge["overrides"].apply_overrides(pinned, forge["overrides"].load_overrides(root))
    files = {path: (root / path).read_bytes() for path in report["file_hashes"] if (root / path).is_file()}
    run = forge["verify"].prepare_run(decision, files, rules, None, symlinks=report["symlinks"], revision=revision)
    for part_id, result in parts.items():
        judged = {item["rule_id"] for item in result["rule_results"]}
        # The report lists every rule Forge considered: those that apply and those it found not applicable.
        applicable = set(run.applicable_rules.get(part_id, [])) | set(run.not_applicable.get(part_id, {}))
        if judged != applicable:
            problems.append(f"part {part_id}: the report's rules differ from the rules Forge applies: "
                            f"missing {sorted(applicable - judged)}, unexplained {sorted(judged - applicable)}")

    for part_id, labels in expected["parts"].items():
        result = parts.get(part_id)
        if result is None:
            problems.append(f"part {part_id}: not in the report")
            continue
        for key in ("harness_result", "goal_result"):
            if result[key] != labels[key]:
                problems.append(f"part {part_id}: {key} is {result[key]!r}, expected {labels[key]!r}")
    for part in decision.record["parts"]:
        if forge["verify"].part_kind(part) != "build":
            continue
        cases = [case for case in report["runtime_results"] if case["part_id"] == part["id"]]
        bound = [case for case in cases if case["run_id"] == report["run_id"] and case["harness"] == harness
                 and all(report["file_hashes"].get(path) == digest for path, digest in case["file_hashes"].items())]
        if len(bound) != len(cases):
            problems.append(f"part {part['id']}: runtime results of another run, harness or file state")
        if not any(case["expected"] == "activates" and case["result"] == "pass" for case in bound):
            problems.append(f"part {part['id']}: no passing runtime case that activates the skill")
        if not any(case["expected"] != "activates" and case["result"] == "pass" for case in bound):
            problems.append(f"part {part['id']}: no passing near-miss runtime case")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--forge", type=Path, default=PLAYGROUND.parent / "harness-forge")
    parser.add_argument("examples", nargs="*", type=Path)
    arguments = parser.parse_args(argv)
    forge = _forge(arguments.forge.resolve())
    examples = arguments.examples or sorted(path.parent for path in (PLAYGROUND / "examples").glob("*/*/expected.yaml"))
    candidates = sorted(path for path in (PLAYGROUND / "examples").glob("*/*") if (path / ".harness").is_dir())
    missing = [path for path in candidates if not (path / "expected.yaml").is_file()]
    failed = False
    for path in missing:
        print(f"{path.relative_to(PLAYGROUND)}: no expected.yaml; not a checked reference run")
        failed = True
    if not examples:
        print("no reference run to check")
        return 2
    for root in examples:
        try:
            problems = check_example(root.resolve(), forge)
        except (OSError, ValueError, KeyError) as error:
            problems = [f"unreadable: {error}"]
        label = root.resolve().relative_to(PLAYGROUND) if root.resolve().is_relative_to(PLAYGROUND) else root
        for problem in problems:
            print(f"{label}: {problem}")
        print(f"{label}: {'pass' if not problems else f'{len(problems)} problem(s)'}")
        failed = failed or bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
