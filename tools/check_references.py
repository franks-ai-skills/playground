#!/usr/bin/env python3
"""Check the stored reference runs in examples/ against Harness Forge (plan task 14).

Run it with Forge's environment from the playground root:

    ../harness-forge/.venv/bin/python tools/check_references.py [--forge ../harness-forge] [example ...]

An example is a result repository, such as
examples/reproduction-checklist/codex/, with an `expected.yaml`:

    harness: codex
    slug: bug-reproduction-checklist
    cases: runtime-cases.yaml   # the runtime cases verify ran, relative to the example
    parts:
      A: {harness_result: verified, goal_result: met by the verified build}

The checker uses Forge's own code, not the report's word, for what the
run rests on: it collects the repository's files and links itself, checks
the overrides as Forge adopts them, and requires the report's bound inputs
(decision, files, links, rules, overrides, revision, checkers, worker
configurations, runtime cases) to equal what Forge computes now. It then
checks every part of the decision: exactly the rules Forge applies, fresh
script results, result labels that follow Forge's precedence and match
`expected.yaml`, only accepted requirements in each built skill, the
Outside controls section, and runtime evidence that Forge itself would
keep for each built part (every declared case, explicit activation of the
part's own skill, these files). Exit 0 when every example passes, 1 with
each problem listed, 2 without any example.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

PLAYGROUND = Path(__file__).resolve().parents[1]


def _forge(path: Path) -> dict:
    sys.path.insert(0, str(path / "src"))
    specification = importlib.util.spec_from_file_location("forge_cli", path / "scripts" / "forge.py")
    cli = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(cli)
    from harness_forge import build_skill, documents, overrides, research, runtime, scope, verify  # noqa: E402
    from harness_forge.checks.outside import check_readme_coverage  # noqa: E402
    from harness_forge.contracts import load_decision  # noqa: E402
    return {"cli": cli, "build_skill": build_skill, "documents": documents, "overrides": overrides,
            "research": research, "runtime": runtime, "scope": scope, "verify": verify,
            "coverage": check_readme_coverage, "load_decision": load_decision}


def _report_data(text: str, documents) -> dict:
    bounds = documents.markdown_section(text, "Report data")
    blocks = re.findall(r"\A## Report data\r?\n\r?\n```json\r?\n(.*?)\r?\n```", text[slice(*bounds)], re.S) if bounds else []
    if len(blocks) != 1:
        raise ValueError("no single report data block")
    data = json.loads(blocks[0])
    documents.validate(data, "report")
    return data


def _differences(recorded: dict, current: dict) -> list[str]:
    names = []
    for key in sorted(set(recorded) | set(current)):
        if recorded.get(key) == current.get(key):
            continue
        if isinstance(recorded.get(key), dict) and isinstance(current.get(key), dict):
            inner = sorted(name for name in set(recorded[key]) | set(current[key])
                           if recorded[key].get(name) != current[key].get(name))
            names.append(f"{key} ({', '.join(inner[:5])})")
        else:
            names.append(key)
    return names


def check_example(root: Path, forge: dict) -> list[str]:
    """Every problem with one stored reference run; empty when it passes."""
    cli, documents, verify = forge["cli"], forge["documents"], forge["verify"]
    expected = documents.parse_yaml((root / "expected.yaml").read_text(encoding="utf-8"))
    slug, harness = expected["slug"], expected["harness"]
    decisions = sorted((root / ".harness" / "decisions").glob("*.md"))
    if len(decisions) != 1:
        return [f"expected one decision record, found {len(decisions)}"]
    decision = forge["load_decision"](decisions[0], root=root)
    research = root / ".harness" / "research" / f"{slug}.md"
    if research.is_file():
        forge["research"].load_research(research, root=root)
    accepted = decision.record.get("accepted_revision")
    revision = (forge["research"].load_revision(root / ".harness" / "research" / f"{slug}.rules.yaml", root=root)
                if accepted else None)
    report_text = (root / ".harness" / "reports" / f"{slug}.md").read_text(encoding="utf-8")
    report = _report_data(report_text, documents)
    earlier, parts = forge["scope"].earlier_run(report_text)
    cases = forge["runtime"].load_cases(root / expected["cases"]) if expected.get("cases") else []
    problems = []

    if (accepted or {}).get("digest") != (revision.digest if revision else None) or \
            report["revision_digest"] != (revision.digest if revision else None):
        problems.append("the decision, the rules file and the report name different accepted revisions")
    try:
        overrides, _ = cli._checked_overrides(root)
    except Exception as error:  # forge.py's own refusal, whatever its type
        return problems + [f"overrides: {error}"]
    adopted = [{"rule_id": override["rule_id"], "digest": documents.canonical_digest(override)}
               for override in overrides]
    if sorted(report["overrides"], key=str) != sorted(adopted, key=str):
        problems.append("the report's adopted overrides are not the repository's")
    rules = forge["overrides"].apply_overrides(cli._pinned_rules(), overrides)
    files, symlinks = cli.collect_target(root, decision)
    current = verify.bound_inputs(decision, files, rules, symlinks=symlinks, revision=revision, overrides=overrides,
                                  kb_version=cli._kb_version(), worker_evidence=report["worker_evidence"], cases=cases)
    changed = _differences(report.get("bound_inputs") or {}, current)
    if changed:
        problems.append(f"bound inputs differ from the repository now: {', '.join(changed)}")

    every = [part["id"] for part in decision.record["parts"]]
    if len(report["parts"]) != len(parts) or sorted(parts) != sorted(every):
        problems.append(f"the report's parts {sorted(parts)} are not the decision's {sorted(every)}")
    if sorted(expected["parts"]) != sorted(every):
        problems.append(f"expected.yaml names parts {sorted(expected['parts'])}, the decision {sorted(every)}")
    run = verify.prepare_run(decision, files, rules, None, symlinks=symlinks, revision=revision,
                             kb_version=cli._kb_version(), worker_evidence=report["worker_evidence"], cases=cases)
    fresh = {(result.part_id, result.rule_id): result.status for result in run.static_results}
    for part in decision.record["parts"]:
        part_id, kind = part["id"], verify.part_kind(part)
        result = parts.get(part_id)
        if result is None:
            continue
        considered = set(run.applicable_rules.get(part_id, [])) | set(run.not_applicable.get(part_id, {}))
        recorded = {item["rule_id"]: item for item in result["rule_results"]}
        kb_rules = {rule_id for rule_id in recorded if rule_id in run.rule_index}
        if kb_rules != considered:
            problems.append(f"part {part_id}: rules differ from those Forge applies: missing "
                            f"{sorted(considered - kb_rules)}, unexplained {sorted(kb_rules - considered)}")
        for (owner, rule_id), status in fresh.items():
            if owner == part_id and rule_id in recorded and recorded[rule_id]["result"] != status:
                problems.append(f"part {part_id}: {rule_id} is {recorded[rule_id]['result']} in the report, "
                                f"{status} now")
        if result["harness_result"] == "verified":
            blocking = [rule_id for rule_id, item in recorded.items() if item["result"] in ("error", "unresolved")
                        or (item["result"] == "fail" and run.rule_index.get(rule_id, {}).get("severity", "error")
                            == "error")]
            goal = result.get("goal_verdict") or {}
            if blocking or goal.get("verdict") != "met" or report["worker_violations"] or part_id not in \
                    report["confirmed_parts"]:
                problems.append(f"part {part_id}: verified despite {blocking or 'its goal verdict, confirmation or '
                                'worker violations'}")
        goal_result = verify._goal_result(kind, result["status"], result["harness_result"],
                                          result["outside_dependencies"], False)
        if result["goal_result"] != goal_result:
            problems.append(f"part {part_id}: goal result {result['goal_result']!r}, Forge gives {goal_result!r}")
        labels = expected["parts"].get(part_id, {})
        for key in ("harness_result", "goal_result"):
            if labels and result[key] != labels.get(key):
                problems.append(f"part {part_id}: {key} is {result[key]!r}, expected {labels.get(key)!r}")
        if kind != "build":
            continue
        skill = files.get(f".agents/skills/{part['slug']}/SKILL.md", b"").decode("utf-8")
        bounds = documents.markdown_section(skill, "Requirements")
        stated = [line for line in skill[slice(*bounds)].splitlines()[1:] if line.strip()] if bounds else []
        requirements = [entry["rule"] for entry in (revision.rules if revision else []) if entry["part_id"] == part_id]
        wanted = [f"{number}. {forge['build_skill']._rule_line(rule)}." for number, rule in enumerate(requirements, 1)]
        if stated != wanted:
            problems.append(f"part {part_id}: SKILL.md requirements {stated} are not the accepted {wanted}")
        if result["harness_result"] == "verified" and not cli._runtime_holds(earlier, part_id, current, run, harness,
                                                                              cases):
            problems.append(f"part {part_id}: verified without runtime evidence Forge would keep for these files "
                            "and cases")
        for evidence in earlier.runtime_results:
            if evidence.part_id == part_id and evidence.expected == "activates" and evidence.result == "pass" and \
                    part["slug"] not in (evidence.observed_activation or ""):
                problems.append(f"part {part_id}: case {evidence.case_id} activated {evidence.observed_activation!r}, "
                                f"not the skill {part['slug']}")

    controls = [{"part_id": part["id"], "control": control["control"]}
                for part in decision.record["parts"] for control in part["outside_controls"]]
    status, reason = forge["coverage"](files, {"outside_controls": controls},
                                       {"heading": "Outside controls", "status": "recommended, not verified"})
    if status != "pass":
        problems.append(f"README.md: {reason}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--forge", type=Path, default=PLAYGROUND.parent / "harness-forge")
    parser.add_argument("examples", nargs="*", type=Path)
    arguments = parser.parse_args(argv)
    forge = _forge(arguments.forge.resolve())
    examples = arguments.examples or sorted(path.parent for path in (PLAYGROUND / "examples").glob("*/*/expected.yaml"))
    failed = False
    if not arguments.examples:
        for path in sorted(path for path in (PLAYGROUND / "examples").glob("*/*") if (path / ".harness").is_dir()):
            if not (path / "expected.yaml").is_file():
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
