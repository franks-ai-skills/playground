#!/usr/bin/env python3
"""Check the stored reference runs in examples/ against Harness Forge (plan task 14).

Run it with Forge's environment from the playground root:

    ../harness-forge/.venv/bin/python tools/check_references.py [--forge ../harness-forge] [example ...]

An example is a result repository, such as
examples/reproduction-checklist/codex/, with an `expected.yaml`:

    harness: codex
    slug: bug-reproduction-checklist
    cases: runtime-cases.yaml   # the runtime cases verify ran, inside the example
    parts:
      A: {harness_result: verified, goal_result: met by the verified build}

The checker replays Forge's verification instead of trusting the report.
It applies the refusals `forge.py verify` makes before it runs (answers,
accepted requirements and their research, overrides, target harness,
runtime case kinds), prepares the run from the repository as it is now,
and finishes it with Forge's own `finish_run`: selection failures, open
drift, the decision's status, the confirmation of the current contract and
the result precedence all come from Forge. The stored report must be
exactly the report Forge renders from that replay.

What only the live run can know is taken from the report: the reviewer's
verdicts, the runtime observations, the worker evidence and violations,
and the user's choices (the confirmed parts and the rules confirmed not to
apply). On top of Forge's gate, a reference run must have run every
declared case, for parts the decision builds, in the harness
`expected.yaml` names, with every case passing for a verified part, the
part's own skill as the activation and no activation on a passing near
miss; every built skill states only accepted requirements, and the
labels must match `expected.yaml`. Metadata files are read as Forge
reads its inputs: inside the example, through no link.

A Review report, which keeps earlier results the repository no longer
holds, is refused: record a reference run as a first run or an Extensive
review. Exit 0 when every example passes, 1 with each problem listed, 2
without any example.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace

PLAYGROUND = Path(__file__).resolve().parents[1]
HARNESSES = ("claude-code", "codex")
LABELS = ("harness_result", "goal_result")
MAX_BYTES = 1024 * 1024


def _forge(path: Path) -> dict:
    sys.path.insert(0, str(path / "src"))
    specification = importlib.util.spec_from_file_location("forge_cli", path / "scripts" / "forge.py")
    cli = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(cli)
    from harness_forge import build_skill, documents, report, runtime, verify  # noqa: E402
    from harness_forge.checks.outside import check_readme_coverage  # noqa: E402
    return {"cli": cli, "build_skill": build_skill, "documents": documents, "report": report, "runtime": runtime,
            "verify": verify, "coverage": check_readme_coverage}


def _read(root: Path, relative: str, documents) -> str:
    """A metadata file inside the example, as Forge reads its own inputs: no link on the way, at most 1 MiB."""
    path = documents.safe_path(root, relative)
    if not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise ValueError(f"{relative}: not a regular file of at most {MAX_BYTES} bytes")
    return path.read_text(encoding="utf-8")


def _expected(text: str, documents) -> dict:
    expected = documents.parse_yaml(text)
    if not isinstance(expected, dict) or not {"harness", "slug", "parts"} <= set(expected) or \
            set(expected) - {"harness", "slug", "cases", "parts"}:
        raise ValueError("expected.yaml names harness, slug and parts, and optionally cases, and nothing else")
    if expected["harness"] not in HARNESSES:
        raise ValueError(f"expected.yaml: harness is one of {', '.join(HARNESSES)}")
    if not isinstance(expected["slug"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", expected["slug"]):
        raise ValueError("expected.yaml: slug is a lowercase name such as bug-reproduction-checklist")
    if "cases" in expected and not isinstance(expected["cases"], str):
        raise ValueError("expected.yaml: cases is a path inside the example")
    parts = expected["parts"]
    if not isinstance(parts, dict) or not all(
            isinstance(labels, dict) and set(labels) == set(LABELS) and all(isinstance(v, str) for v in labels.values())
            for labels in parts.values()):
        raise ValueError(f"expected.yaml: each part states both {' and '.join(LABELS)}")
    return expected


def _report_data(text: str, documents) -> dict:
    bounds = documents.markdown_section(text, "Report data")
    blocks = re.findall(r"\A## Report data\r?\n\r?\n```json\r?\n(.*?)\r?\n```", text[slice(*bounds)], re.S) if bounds else []
    if len(blocks) != 1:
        raise ValueError("no single report data block")
    data = json.loads(blocks[0])
    documents.validate(data, "report")
    return data


def _differences(recorded: dict, replayed: dict) -> list[str]:
    names = []
    for key in sorted(set(recorded) | set(replayed)):
        if recorded.get(key) == replayed.get(key):
            continue
        if key == "parts" and isinstance(recorded.get(key), list):
            ours = {part["part_id"]: part for part in replayed.get(key, [])}
            for part in recorded[key]:
                theirs = ours.get(part.get("part_id"), {})
                inner = sorted(name for name in set(part) | set(theirs) if part.get(name) != theirs.get(name))
                if inner:
                    names.append(f"part {part.get('part_id')} ({', '.join(inner)})")
            if len(recorded[key]) != len(ours) or not names:
                names.append("parts")
        elif isinstance(recorded.get(key), dict) and isinstance(replayed.get(key), dict):
            inner = sorted(name for name in set(recorded[key]) | set(replayed[key])
                           if recorded[key].get(name) != replayed[key].get(name))
            names.append(f"{key} ({', '.join(inner[:5])})")
        else:
            names.append(key)
    return names


def _review(data: dict, verify, run) -> dict:
    """The reviewer's verdicts as the report records them, in the form the worker returned them.

    A judged rule whose applicability conditions do not hold never reached
    the reviewer: Forge records it as not applicable without a verdict.
    """
    verdicts, goals = [], []
    for part in data["parts"]:
        for item in part["rule_results"]:
            if item["check"] != "judged" or item["result"] == "missing" or \
                    item["rule_id"] in run.not_applicable.get(part["part_id"], {}):
                continue
            # Forge records a reviewer's "not applicable" as such, as unresolved or as an error.
            verdict = item["result"] if item["result"] in ("pass", "fail") else "not-applicable"
            verdicts.append({"part_id": part["part_id"], "rule_id": item["rule_id"], "verdict": verdict,
                             "reason": item["reason"].removesuffix(verify.NEEDS_CONFIRMATION),
                             "citation": item.get("citation", "")})
        if part.get("goal_verdict"):
            goals.append({"part_id": part["part_id"], **part["goal_verdict"]})
    return {"run_id": data["run_id"], "verdicts": verdicts, "goal_verdicts": goals}


def _refused(call, *arguments):
    """Forge's own refusal of these inputs, whatever its type, or None."""
    try:
        return None, call(*arguments)
    except Exception as error:  # noqa: BLE001 - forge.py raises its own input errors
        return str(error) or type(error).__name__, None


def _activations(harness: str, directory: str) -> set[str]:
    """Every activation signal the harness's observer writes for the skill in ``directory``."""
    name = directory.rsplit("/", 1)[-1]
    if harness == "codex":
        return {f"read {directory}/SKILL.md"}
    return {f"Skill tool called for {name}", f"read SKILL.md from the {name} skill", f"/{name} was invoked"}


def check_example(root: Path, forge: dict) -> list[str]:
    """Every problem with one stored reference run; empty when it passes."""
    cli, documents, verify = forge["cli"], forge["documents"], forge["verify"]
    root = root.resolve()
    problem, text = _refused(_read, root, "expected.yaml", documents)
    if problem:
        return [f"expected.yaml: {problem}"]
    expected = _expected(text, documents)
    slug, harness = expected["slug"], expected["harness"]
    problem, directory = _refused(documents.safe_path, root, ".harness/decisions")
    if problem:
        return [f"decisions: {problem}"]
    decisions = sorted(directory.glob("*.md"))
    for path in decisions:
        problem = _refused(_read, root, path.relative_to(root).as_posix(), documents)[0]
        if problem:
            return [f"decision: {problem}"]
    if len(decisions) != 1:
        return [f"expected one decision record, found {len(decisions)}"]
    problem, recorded = _refused(lambda: cli.load_decision(decisions[0], root=root))
    if problem:
        return [f"forge refuses the decision: {problem}"]
    # The requirements file is passed exactly when the decision records accepted requirements, as verify requires.
    revision_path = root / ".harness" / "research" / f"{slug}.rules.yaml"
    arguments = SimpleNamespace(decision=str(decisions[0]),
                                revision=str(revision_path) if recorded.record.get("accepted_revision") else None)
    problem, loaded = _refused(cli._decision_and_revision, arguments, root)
    if problem:
        return [f"forge refuses the decision or its requirements: {problem}"]
    decision, revision = loaded
    every = [part["id"] for part in decision.record["parts"]]
    covered = [part["id"] for part in decision.record["parts"]
               if verify.part_kind(part) in ("build", "local-reuse")]
    problems = []
    stale = cli._stale_requirements(decision, revision, covered)
    if stale:
        problems.append(f"forge refuses the accepted requirements: {stale}")
    for part_id in covered if revision and not stale else []:
        own = SimpleNamespace(rules=[entry for entry in revision.rules if entry["part_id"] == part_id])
        provenance = cli._provenance_problem(root, slug, part_id, revision.brief_digests[part_id], own)
        if provenance:
            problems.append(f"part {part_id}: {provenance}")
    problem = _refused(cli._require_target, decision, harness)[0]
    if problem:
        problems.append(problem)
    problem, checked = _refused(cli._checked_overrides, root)
    if problem:
        return problems + [f"overrides: {problem}"]
    overrides = checked[0]
    files, symlinks = cli.collect_target(root, decision)
    cases = []
    if "cases" in expected:
        problem, path = _refused(documents.safe_path, root, expected["cases"])
        problem, cases = (problem, None) if problem else _refused(forge["runtime"].load_cases, path)
        if problem:
            return problems + [f"runtime cases: {problem}"]
    for case in cases:
        if harness not in case["permitted_tools"]:
            problems.append(f"case {case['id']} names no permitted tools for {harness}")
    built = {part["id"]: f".agents/skills/{part['slug']}" for part in decision.record["parts"]
             if verify.part_kind(part) == "build"}
    for case in cases:
        if case["part_id"] not in built:
            problems.append(f"case {case['id']} names part {case['part_id']}, which the decision does not build")
    for part_id in sorted(set(built) | {case["part_id"] for case in cases}):
        kinds = {(case["mode"], case["expected"]) for case in cases if case["part_id"] == part_id}
        if not {("explicit", "activates"), ("negative", "does-not-activate")} <= kinds:
            problems.append(f"part {part_id} needs an explicit invocation and a near miss among its cases")
    # Accepted requirements only, in every built skill, confirmed or not.
    for part_id, directory in sorted(built.items()):
        skill = files.get(f"{directory}/SKILL.md", b"").decode("utf-8")
        bounds = documents.markdown_section(skill, "Requirements")
        stated = [line for line in skill[slice(*bounds)].splitlines()[1:] if line.strip()] if bounds else []
        requirements = [entry["rule"] for entry in (revision.rules if revision else []) if entry["part_id"] == part_id]
        wanted = [f"{number}. {forge['build_skill']._rule_line(rule)}." for number, rule in enumerate(requirements, 1)]
        if stated != wanted:
            problems.append(f"part {part_id}: SKILL.md requirements {stated} are not the accepted {wanted}")
    if sorted(expected["parts"]) != sorted(every):
        problems.append(f"expected.yaml names parts {sorted(expected['parts'])}, the decision {sorted(every)}")

    problem, report_text = _refused(_read, root, f".harness/reports/{slug}.md", documents)
    if problem:
        return problems + [f"report: {problem}"]
    data = _report_data(report_text, documents)
    if data["scope_parts"] is not None:
        return problems + ["the report is a Review, whose kept results rest on an earlier report; record a reference "
                           "run as a first run or an Extensive review"]
    labels = {f"First run: judged {', '.join(sorted(every))}",
              f"Extensive review (rarely needed): judged {', '.join(sorted(every))}"}
    if data["scope"] not in labels:
        problems.append(f"the report's scope {data['scope']!r} is not a first run or an Extensive review of every part")
    if not data["contract_digest"]:
        problems.append("the report names no confirmed contract; a live verification always runs under one")

    drift = cli._drift(root)
    unresolved = [entry for entry in drift if cli.drift_state(entry, decision.record, overrides) == "open"]
    # verify reports the approved worker evidence, then what the review worker it ran observed.
    stored = data["worker_evidence"]
    split = next((count for count in range(len(stored), -1, -1)
                  if _refused(lambda: cli.render_contract(decision, revision, overrides, worker_evidence=stored[:count],
                                                          drift=drift).digest)[1] == data["contract_digest"]), None)
    if split is None:
        problems.append("the report's contract digest is not the current contract's for any approved workers it lists")
        split = len(stored)
    approved, observed = stored[:split], stored[split:]
    if len(observed) > 1 or any(evidence["role"] != "review" for evidence in observed):
        problems.append("the report lists worker evidence after the approved workers that is not one review worker's")
    confirmation = cli.Confirmation(run_id=data["run_id"], contract_digest=data["contract_digest"] or "",
                                    part_ids=sorted(data["confirmed_parts"]))
    rules = cli.effective_rules(cli._pinned_rules(), overrides, confirmation)
    problem, run = _refused(lambda: verify.prepare_run(
        decision, files, rules, confirmation, symlinks=symlinks, revision=revision, overrides=overrides,
        kb_version=cli._kb_version(), worker_evidence=approved,
        scope_label=data["scope"] if data["scope"] in labels else sorted(labels)[0], recorded_drift=drift,
        cases=cases))
    if problem:
        return problems + [f"forge cannot prepare the run: {problem}"]
    run.worker_violations = list(data["worker_violations"])
    problem, review = _refused(verify.validate_review, run, _review(data, verify, run))
    if problem:
        return problems + [f"the report's verdicts are not ones the reviewer could return: {problem}"]
    exclusions = {(part["part_id"], item["rule_id"], verify.exclusion_token(run, part["part_id"], item["rule_id"]))
                  for part in data["parts"] for item in part["rule_results"]
                  if item["check"] == "judged" and item["result"] == "not-applicable"
                  and item["rule_id"] not in run.not_applicable.get(part["part_id"], {})}
    selection_rules = cli.effective_rules(cli._selection_rules(), overrides, confirmation)
    failures, _ = verify.selection_failures(decision, selection_rules, domains=cli._domains(cli._selection_document()))
    required = {part["id"]: {case["id"] for case in cases if case["part_id"] == part["id"]
                             and case["mode"] == "explicit" and case["expected"] == "activates"}
                for part in run.parts if verify.part_kind(part) == "build" and part["id"] in run.confirmed_parts
                and harness in run.targets}
    runtime = [forge["runtime"].RuntimeResult(**item) for item in data["runtime_results"]]
    problem, results = _refused(lambda: verify.finish_run(
        run, review, runtime, dict(run.frozen_inputs), confirmed_exclusions=frozenset(exclusions),
        worker_observations=observed,
        required_activation=required, drift=unresolved, selection=failures,
        cited=verify.selection_citations(decision, selection_rules)))
    if problem:
        return problems + [f"forge refuses the report's runtime results: {problem}"]
    replayed = forge["report"].report_data(run, results)
    changed = _differences(data, replayed)
    if changed:
        problems.append(f"the report differs from Forge's replay of this repository: {', '.join(changed)}")
    elif forge["report"].render_report(run, results) != report_text:
        problems.append("the report's text is not what Forge renders for its data")

    for result in results:
        labels = expected["parts"].get(result.part_id)
        for key in LABELS:
            if labels and getattr(result, key) != labels[key]:
                problems.append(f"part {result.part_id}: Forge gives {key} {getattr(result, key)!r}, expected.yaml "
                                f"{labels[key]!r}")
    for item in runtime:
        if item.harness != harness:
            problems.append(f"case {item.case_id} ran in {item.harness}, not in the reference's {harness}")
        if item.expected == "does-not-activate" and item.result == "pass" and item.observed_activation:
            problems.append(f"case {item.case_id} passed although it observed an activation "
                            f"({item.observed_activation!r})")
    by_part = {result.part_id: result for result in results}
    for part in decision.record["parts"]:
        part_id = part["id"]
        if verify.part_kind(part) != "build" or part_id not in run.confirmed_parts:
            continue
        declared = {case["id"]: case for case in cases if case["part_id"] == part_id}
        evidence = [item for item in runtime if item.part_id == part_id]
        if sorted(item.case_id for item in evidence) != sorted(declared):
            problems.append(f"part {part_id}: runtime results for {sorted(item.case_id for item in evidence)}, "
                            f"declared cases {sorted(declared)}")
        for item in evidence:
            case = declared.get(item.case_id)
            if case and (item.prompt, item.expected) != (case["prompt"], case["expected"]):
                problems.append(f"part {part_id}: case {item.case_id} ran another prompt or expectation than declared")
            if item.expected == "activates" and item.result == "pass" and \
                    item.observed_activation not in _activations(harness, run.part_dirs[part_id]):
                problems.append(f"part {part_id}: case {item.case_id} activated {item.observed_activation!r}, "
                                f"not the skill in {run.part_dirs[part_id]}")
            if by_part[part_id].harness_result == "verified" and item.result != "pass":
                problems.append(f"part {part_id}: verified with case {item.case_id} {item.result}; a reference run "
                                "passes every case")

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
        except (OSError, ValueError, KeyError, TypeError) as error:
            problems = [f"unreadable: {error}"]
        label = root.resolve().relative_to(PLAYGROUND) if root.resolve().is_relative_to(PLAYGROUND) else root
        for problem in problems:
            print(f"{label}: {problem}")
        print(f"{label}: {'pass' if not problems else f'{len(problems)} problem(s)'}")
        failed = failed or bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
