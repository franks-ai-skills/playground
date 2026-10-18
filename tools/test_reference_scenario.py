"""Plan task 14's reference scenario, run offline with Forge's scripted workers before the owner runs it live.

One idea split into six parts, one per selection outcome: two built skills
(harness-only and outside-alongside), a reused skill already in the
repository, a reused remote skill, a part an outside control does instead,
and one where nothing fits. The run verifies, breaks and fixes a built
skill, reviews the fix, closes with an Extensive review, and the stored
result must pass tools/check_references.py. Scripted workers prove the
plumbing only: the live run regenerates research, judgments and choices.

    ../harness-forge/.venv/bin/python -m unittest discover -s tools -p test_reference_scenario.py
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

PLAYGROUND = Path(__file__).resolve().parents[1]
FORGE = PLAYGROUND.parent / "harness-forge"
sys.path[:0] = [str(FORGE), str(FORGE / "src"), str(PLAYGROUND / "tools")]

import reference_runs  # noqa: E402
from harness_forge.adapters.base import Completed  # noqa: E402
from harness_forge.contracts import load_decision, split_part, write_decision  # noqa: E402
from harness_forge.runtime import BASELINE_PROMPT  # noqa: E402
from tests.builders import decision, part  # noqa: E402
from tests.test_cli_live import Cli  # noqa: E402
from tests.test_adapters import FakeRunner, codex_stream  # noqa: E402
from tests.test_pipeline import ScriptedRunner, staged_request  # noqa: E402
from tests.test_runtime import claude_run  # noqa: E402

SLUG = "bug-intake"
DATE = "2026-10-17"
DECISION = f".harness/decisions/{DATE}-{SLUG}.md"
REPORT = f".harness/reports/{SLUG}.md"
REVISION = f".harness/research/{SLUG}.rules.yaml"
CASES = ".harness/cases.yaml"  # inside .harness/, as the runbook asks, so collection must not copy it twice
EXISTING = reference_runs.EXISTING
NEAR_MISS = "no bug report is involved"

# The confirmed answers of the pinned reference-reproduction-checklist selection fixture: a skill, harness only.
ANSWERS = yaml.safe_load((FORGE / "snapshot/fixtures/selection/reference-reproduction-checklist.yaml")
                         .read_text(encoding="utf-8"))["answers"]

# Goal, slug and answers per part: the answers select each outcome (harness-forge snapshot selection rules).
PARTS = {
    "A1": ("Write a reproduction checklist from an approved bug report", "reproduction-checklist", {}),
    "A2": ("Check a fix against its reproduction checklist before it merges", "fix-check",
           {"must_survive_compromise": "required"}),
    "A3": ("Format incoming bug reports with the team's template", EXISTING, {}),
    "A4": ("Fix the failing CI checks on the fix's pull request", "gh-fix-ci", {}),
    "A5": ("Close the tracker issue once the fix ships", "close-issue", {"irreversible": True}),
    "A6": ("Label every incoming bug report", "label-reports", {"every_time": "always"}),
}
CANDIDATES = {
    "A3": {"name": EXISTING, "source": "https://example.com/team/bug-report-format", "license": "MIT",
           "maintenance": "maintained", "fit": "confirmed", "concept": "skills"},
    # A public skill a live survey can find: openai/skills, Apache-2.0 (checked 2026-10-17).
    "A4": {"name": "gh-fix-ci", "source": "https://github.com/openai/skills/tree/main/skills/.curated/gh-fix-ci",
           "license": "Apache-2.0", "maintenance": "maintained", "fit": "confirmed", "concept": "skills"},
}
DESCRIPTIONS = {
    "A1": "Turns an approved bug report into a reproduction checklist with environment, steps, expected and "
          "observed behavior. Use when asked for reproduction steps for an approved bug. Not for fixing the bug.",
    "A2": "Compares a fix branch with the bug's reproduction checklist and reports each step the fix does not "
          "cover. Use when a fix for a reported bug is ready for review. Not for writing the checklist.",
}
PROCEDURES = {
    "A1": "1. Read the approved bug report.\n2. Write the environment, the steps, and the expected and observed "
          "behavior.\n",
    "A2": "1. Read the bug's reproduction checklist.\n2. Check each step against the fix and list the steps it "
          "does not cover.\n",
}


def runtime_cases() -> dict:
    """An explicit, an implicit and a near-miss case for each built part."""
    fixture = {"bug-report.md": "# Bug 42 (approved)\nExporting an empty date range crashes the app on macOS 15.\n"
                                "Expected: an empty export. Observed: the app quits.\n"}
    tools = {"claude-code": ["Skill", "Read"], "codex": ["command_execution"]}
    fix = {"checklist.md": "1. Open the export dialog.\n2. Choose an empty date range.\n3. Export.\n",
           "fix.diff": "--- a/export.py\n+++ b/export.py\n+    if not rows:\n+        return []\n"}
    # Each built skill's own requests: a case another skill's prompt would answer hides a routing miss.
    prompts = {"A1": ("Use the reproduction-checklist skill on the bug report in bug-report.md.",
                      "The bug report in bug-report.md is approved; how do I reproduce it step by step?", fixture),
               "A2": ("Use the fix-check skill on fix.diff and checklist.md.",
                      "Does the fix in fix.diff cover every step of checklist.md before it merges?", fix)}
    cases = []
    for part_id, (explicit, implicit, fixtures) in prompts.items():
        prefix = part_id.lower()
        cases += [
            {"id": f"{prefix}-explicit", "part_id": part_id, "mode": "explicit", "expected": "activates",
             "prompt": explicit, "permitted_tools": tools, "fixtures": fixtures},
            {"id": f"{prefix}-implicit", "part_id": part_id, "mode": "implicit", "expected": "activates",
             "prompt": implicit, "permitted_tools": tools, "fixtures": fixtures},
            {"id": f"{prefix}-near-miss", "part_id": part_id, "mode": "negative", "expected": "does-not-activate",
             "prompt": f"Rename the variables in utils.py; {NEAR_MISS}.", "permitted_tools": tools,
             "fixtures": {"utils.py": "x = 1\n"}},
        ]
    # A JSON round trip unshares the objects, which would otherwise dump as YAML anchors Forge refuses.
    return json.loads(json.dumps({"cases": cases}))


class ScenarioRunner(ScriptedRunner):
    """The scripted workers, with each runtime case activating the one skill staged in its workspace."""

    def __call__(self, command, *, cwd, env, stdin, timeout):
        launched = len(self.worker_calls)
        answer = super().__call__(command, cwd=cwd, env=env, stdin=stdin, timeout=timeout)
        if len(self.worker_calls) == launched or stdin == BASELINE_PROMPT or "```json" in stdin:
            return answer
        staged = sorted(path.name for path in (Path(cwd) / ".agents" / "skills").iterdir())
        return Completed(0, claude_run(skills=staged, skill_call=None if NEAR_MISS in stdin else staged[0]), "", False)


class CodexScenarioRunner(FakeRunner):
    """Codex workers as scripted processes: a passing review, and each runtime case reading the staged skill's
    SKILL.md unless it is the near miss."""

    def __call__(self, command, *, cwd, env, stdin, timeout):
        launched = len(self.worker_calls)
        answer = super().__call__(command, cwd=cwd, env=env, stdin=stdin, timeout=timeout)
        if len(self.worker_calls) == launched:
            return answer
        if "```json" in stdin:
            request = staged_request(stdin)
            output = {"run_id": request["run_id"],
                      "verdicts": [{"part_id": rule["part_id"], "rule_id": rule["rule_id"], "verdict": "pass",
                                    "reason": "Meets it.", "citation": "SKILL.md"} for rule in request["inputs"]["rules"]],
                      "goal_verdicts": [{"part_id": goal["part_id"], "verdict": "met", "reason": "It does the job."}
                                        for goal in request["inputs"]["goals"]]}
            return Completed(0, codex_stream(output), "", False)
        events = [{"type": "thread.started", "thread_id": "x"}]
        if NEAR_MISS not in stdin:
            skill = sorted((Path(cwd) / ".agents" / "skills").iterdir())[0]
            events.append({"type": "item.completed", "item": {
                "id": "read", "type": "command_execution", "command": f"cat .agents/skills/{skill.name}/SKILL.md",
                "exit_code": 0, "status": "completed", "aggregated_output": (skill / "SKILL.md").read_text()}})
        events.append({"type": "turn.completed"})
        return Completed(0, "\n".join(json.dumps(event) for event in events), "", False)


class Scenario:
    """Runs the scenario's commands through Forge's CLI in ``root``."""

    def __init__(self, root: Path):
        self.root = root
        self.cli = Cli(ScenarioRunner(), root)
        self.cli.parts = list(PARTS)

    def ok(self, *arguments, code=0):
        returned, output, stderr = self.cli(*arguments)
        assert returned == code, f"{arguments[0]} returned {returned}: {stderr} {output}"
        return output

    def start(self):
        root = self.root
        reference_runs.start(root)
        record = decision(part("A", "Handle incoming bug reports from intake to closing", slug=SLUG))
        self.facts = record.record["facts"]
        record = split_part(record, "A", [goal for goal, _, _ in PARTS.values()])
        record.record.update(split_confirmed=True, survey_findings_used=[])
        self.decision = write_decision(root, record, slug=SLUG, date=DATE)
        self.workers = self.cli.write("workers.json", self.ok("workers", "--harness", "claude-code"))
        self.ok("research", "--decision", self.decision, "--pass", "survey", "--harness", "claude-code",
                "--evidence", self.workers, "--relay", self.cli.confirm(self.decision, "intake-1"), "--root", root,
                "--slug", SLUG, "--write")

    def choose(self):
        record = load_decision(self.decision)
        for part_id, (_, slug, changes) in PARTS.items():
            answers = {**ANSWERS, **changes}
            candidates = [CANDIDATES[part_id]] if part_id in CANDIDATES else []
            chosen = self.ok("select", "--input", self.cli.write("select.json", {
                "answers": answers, "whole_idea": self.facts, "candidates": candidates}))
            controls = [{"control": control["id"], "prerequisites": control["prerequisites"],
                         "availability": control["availability"], "required_for_goal": control["required_for_goal"]}
                        for control in chosen["controls"]]
            record.part(part_id).update(slug=slug, answers=answers, outcome=chosen["outcome"],
                                        recommended=chosen["mechanism"], chosen=chosen["mechanism"],
                                        outside_controls=controls)
            if part_id in CANDIDATES:
                reuse = {key: CANDIDATES[part_id][key] for key in ("name", "source", "license", "maintenance")}
                if part_id == "A3":
                    reuse.update(path=f".agents/skills/{EXISTING}", skill_home="repository")
                record.part(part_id)["reuse"] = reuse
        write_decision(self.root, record, slug=SLUG, date=DATE)
        self.ok("readme", "--decision", self.decision, "--root", self.root)
        return {part_id: record.part(part_id)["outcome"] for part_id in PARTS}

    def build(self):
        revision = self.root / REVISION
        # Every checked part needs its accepted requirements, a reused one too, even when none is accepted.
        for part_id in ("A1", "A2", "A3"):
            self.ok("research", "--decision", self.decision, "--pass", "deep", "--part", part_id, "--harness",
                    "claude-code", "--evidence", self.workers,
                    "--relay", self.cli.confirm(self.decision, f"deep-{part_id}",
                                                *(["--revision", revision] if revision.exists() else [])),
                    "--root", self.root, "--slug", SLUG, "--write",
                    *(["--revision", revision] if revision.exists() else []))
            requirement = f"idea.{SLUG}.{part_id.lower()}.platform"
            proposed = [] if part_id == "A3" else [
                {"id": requirement, "concept": "idea", "kind": "must", "severity": "error", "check": "judged",
                 "statement": "The result names the platform the bug occurs on",
                 "applies_to": {"harnesses": ["claude-code", "codex"]}, "evidence": "Vendor",
                 "sources": ["https://docs.example-vendor.com/repro/platforms"], "contested": False}]
            self.ok("accept", "--decision", self.decision, "--part", part_id,
                    "--proposed", self.cli.write("proposed.json", {"requirements": proposed}),
                    "--choices", self.cli.write("choices.json", {r["id"]: "accept" for r in proposed}),
                    "--root", self.root, "--slug", SLUG)
        for part_id in ("A1", "A2"):
            self.build_part(part_id)

    def build_part(self, part_id, *extra, code=0):
        revision = self.root / REVISION
        return self.ok("build", "--decision", self.decision, "--part", part_id, "--revision", revision,
                       "--evidence", self.workers,
                       "--relay", self.cli.confirm(self.decision, f"build-{part_id}", "--revision", revision),
                       "--description", self.cli.write("description.txt", DESCRIPTIONS[part_id]),
                       "--procedure", self.cli.write("procedure.md", PROCEDURES[part_id]), "--root", self.root,
                       *extra, code=code)

    def verify(self, run_id, *extra, code=0, refresh=None):
        """An Extensive review unless ``refresh`` gives the scope choice for the run's relay."""
        revision = self.root / REVISION
        cases = self.root / CASES
        if not cases.exists():
            cases.write_text(yaml.safe_dump(runtime_cases()), encoding="utf-8")
        relay = self.cli.confirm(self.decision, run_id, "--revision", revision)
        return self.ok("verify", "--decision", self.decision, "--root", self.root, "--revision", revision,
                       "--evidence", self.workers, "--relay", relay, "--harness", "claude-code",
                       "--cases", cases, "--slug", SLUG, "--write", *extra, *(refresh(relay) if refresh else []),
                       code=code)

    def review_choice(self, relay, fixed):
        """The scope question's Review option, as the user would choose it."""
        options = self.ok("scope", "--harness", "claude-code", "--decision", self.decision, "--root", self.root,
                          "--revision", self.root / REVISION, "--evidence", self.workers, "--relay", relay,
                          "--slug", SLUG, "--fixed", fixed, "--cases", self.root / CASES)["options"]
        review = options[0]  # the Review option comes first, the Extensive review after it
        self.reviewed_parts = review["parts"]
        chosen = self.cli.write("scope.json", {"choice": "review", "displayed_digest": review["digest"],
                                               "run_id": json.loads(Path(relay).read_text())["run_id"]})
        return ["--scope", "review", "--fixed", fixed, "--scope-relay", chosen]


class ReferenceScenarioTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="reference-scenario-")
        self.root = Path(self.directory.name) / "repository"
        self.root.mkdir()
        self.scenario = Scenario(self.root)

    def tearDown(self):
        self.directory.cleanup()

    def test_the_six_outcomes_verify_break_fix_review_and_replay(self):
        scenario = self.scenario
        scenario.start()
        self.assertEqual(scenario.choose(), {"A1": "harness-only", "A2": "outside-alongside", "A3": "reuse",
                                             "A4": "reuse", "A5": "outside-instead", "A6": "nothing-fits"})
        scenario.build()
        output = scenario.verify("verify-1")
        self.assertEqual(results(output), EXPECTED)
        self.assertEqual([case["result"] for case in output["runtime"]], ["pass"] * 6)

        # The break: A1's skill names itself wrongly, and nothing claims success.
        skill = self.root / ".agents/skills/reproduction-checklist/SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8").replace("name: reproduction-checklist", "name: Broken_Name"),
                         encoding="utf-8")
        broken = scenario.verify("verify-2", code=1)
        self.assertEqual(results(broken)["A1"], ("not verified", "not met"))

        # The fix: the builder shows the diff, replaces only that file, and a Review checks it.
        self.assertIn("-name: Broken_Name", scenario.build_part("A1", code=1)["diff"])
        scenario.build_part("A1", "--replace", ".agents/skills/reproduction-checklist/SKILL.md")
        reviewed = scenario.verify("verify-3", refresh=lambda relay: scenario.review_choice(relay, "A1"))
        self.assertEqual(results(reviewed), EXPECTED)
        self.assertEqual(reviewed["judged_parts"], scenario.reviewed_parts)
        self.assertIn("A1", scenario.reviewed_parts)
        self.assertLess(len(scenario.reviewed_parts), len(PARTS), "a Review keeps the parts the fix cannot affect")

        # The closing Extensive review judges every part again; the reference checker replays it.
        closing = scenario.verify("verify-4")
        self.assertEqual((results(closing), closing["kept_parts"]), (EXPECTED, []))
        example = Path(self.directory.name) / "example"
        (self.root / ".env").write_text("TOKEN=not-for-the-example\n", encoding="utf-8")
        self.assertEqual(reference_runs.collect(self.root, example, harness="claude-code", slug=SLUG, cases=CASES), [])
        self.assertFalse((example / ".env").exists())
        self.assertFalse((example / ".scratch" / "workers.json").exists(), "the agent's scratch files stay behind")

    def test_a_result_without_runtime_cases_is_collected_without_them(self):
        """A run that built nothing has no cases file; collected without one, a built part's missing cases show."""
        scenario = self.scenario
        scenario.start()
        scenario.choose()
        scenario.build()
        scenario.verify("verify-1")
        example = Path(self.directory.name) / "example"
        problems = reference_runs.collect(self.root, example, harness="claude-code", slug=SLUG, cases=None)
        self.assertNotIn("cases", yaml.safe_load((example / "expected.yaml").read_text(encoding="utf-8")))
        self.assertIn("part A1 is a built skill: its runtime cases are missing", problems)

    def test_collect_refuses_a_path_outside_the_repository_before_writing(self):
        reference_runs.start(self.root)
        outside = Path(self.directory.name) / "cases.yaml"
        outside.write_text("cases: []\n", encoding="utf-8")
        example = Path(self.directory.name) / "example"
        for cases in ("../cases.yaml", "/etc/hosts", ".claude/skills/../../cases.yaml"):
            with self.subTest(cases=cases), self.assertRaises(ValueError):
                reference_runs.collect(self.root, example, harness="claude-code", slug=SLUG, cases=cases)
            self.assertFalse(example.exists())

    def test_the_same_result_verified_from_codex_replays(self):
        """Codex as the second target: a first run there over the result, near misses unobservable."""
        scenario = self.scenario
        scenario.start()
        scenario.choose()
        scenario.build()
        scenario.verify("verify-1")
        (self.root / REPORT).unlink()
        codex = Cli(CodexScenarioRunner(), self.root)
        codex.parts = list(PARTS)
        code, workers, stderr = codex("workers", "--harness", "codex")
        self.assertEqual(code, 0, stderr)
        workers = codex.write("workers.json", workers)
        revision = self.root / REVISION
        code, output, stderr = codex(
            "verify", "--decision", scenario.decision, "--root", self.root, "--revision", revision,
            "--evidence", workers, "--relay", codex.confirm(scenario.decision, "codex-1", "--revision", revision),
            "--harness", "codex", "--cases", self.root / CASES, "--slug", SLUG, "--write")
        self.assertEqual(code, 0, (output, stderr))
        self.assertEqual(results(output), EXPECTED)
        self.assertEqual({case["case_id"]: case["result"] for case in output["runtime"] if "near-miss" in case["case_id"]},
                         {"a1-near-miss": "not-run", "a2-near-miss": "not-run"})
        example = Path(self.directory.name) / "example"
        self.assertEqual(reference_runs.collect(self.root, example, harness="codex", slug=SLUG, cases=CASES), [])


EXPECTED = {"A1": ("verified", "met by the verified build"), "A2": ("verified", "depends on outside controls"),
            "A3": ("verified", "met by the verified build"), "A4": ("not checked", "not assessed"),
            "A5": ("not applicable", "depends on outside controls"), "A6": ("not applicable", "not met")}


def results(output: dict) -> dict:
    return {part["part_id"]: (part["harness_result"], part["goal_result"]) for part in output["parts"]}


if __name__ == "__main__":
    unittest.main()
