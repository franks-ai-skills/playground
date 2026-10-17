"""check_references.py against a reference run that Forge's own CLI recorded with scripted workers.

Run it with Forge's environment from the playground root:

    ../harness-forge/.venv/bin/python -m unittest discover -s tools

The repository comes from Forge's offline pipeline (its tests' scripted
research, review and runtime workers) up to the first verification, so it
is exactly what `forge.py verify --write` leaves behind. Every other test
changes one thing in a copy and expects the checker to refuse it.
"""

from __future__ import annotations

import copy
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

PLAYGROUND = Path(__file__).resolve().parents[1]
FORGE = PLAYGROUND.parent / "harness-forge"
sys.path[:0] = [str(FORGE), str(FORGE / "src"), str(PLAYGROUND / "tools")]

import check_references  # noqa: E402
from harness_forge.contracts import load_decision, split_part, write_decision  # noqa: E402
from tests.builders import ANSWERS, decision, part  # noqa: E402
from tests.test_build_skill import DESCRIPTION, NAME, PROCEDURE  # noqa: E402
from tests.test_cli_live import Cli  # noqa: E402
from tests.test_workflow import ResearchRunner, finding  # noqa: E402

REPORT = ".harness/reports/repro.md"
DECISION = ".harness/decisions/2026-10-12-repro.md"
CASES = ".scratch/cases.yaml"


def record_reference(root: Path) -> None:
    """Forge's offline pipeline, as tests/test_full_pipeline.py runs it, up to the first verification."""
    (root / "README.md").write_text("# Repro\n", encoding="utf-8")
    cli = Cli(ResearchRunner([finding()]), root)
    cli.parts = ["A1", "A2"]

    def ok(*arguments):
        code, output, stderr = cli(*arguments)
        assert code == 0, f"{arguments[0]}: {stderr}"
        return output

    record = decision(part("A", "Turn approved bug reports into checklists and publish them", slug=NAME))
    facts = record.record["facts"]
    record = split_part(record, "A", ["Write a reproduction checklist when asked",
                                      "Publish the checklist to the tracker"])
    record.record.update(split_confirmed=True, survey_findings_used=[])
    path = write_decision(root, record, slug="repro", date="2026-10-12")
    workers = cli.write("workers.json", ok("workers", "--harness", "claude-code"))
    ok("research", "--decision", path, "--pass", "survey", "--harness", "claude-code", "--evidence", workers,
       "--relay", cli.confirm(path, "intake-1"), "--root", root, "--slug", "repro", "--write")

    def select(answers):
        return ok("select", "--input", cli.write("select.json", {"answers": answers, "whole_idea": facts}))

    def recorded(controls):
        return [{"control": control["id"], "prerequisites": control["prerequisites"],
                 "availability": control["availability"], "required_for_goal": control["required_for_goal"]}
                for control in controls]

    checklist, publishing = select(dict(ANSWERS)), select({**ANSWERS, "irreversible": True})
    record = load_decision(path)
    record.part("A1").update(slug=NAME, answers=dict(ANSWERS), outcome="harness-only", recommended="skills",
                             chosen="skills", outside_controls=recorded(checklist["controls"]))
    record.part("A2").update(slug="publish-checklist", answers={**ANSWERS, "irreversible": True},
                             outcome="outside-instead", recommended=None, chosen=None,
                             connects_to=[{"to": "A1", "how": "uses"}], outside_controls=recorded(publishing["controls"]))
    write_decision(root, record, slug="repro", date="2026-10-12")
    ok("readme", "--decision", path, "--root", root)
    ok("research", "--decision", path, "--pass", "deep", "--part", "A1", "--harness", "claude-code",
       "--evidence", workers, "--relay", cli.confirm(path, "intake-2"), "--root", root, "--slug", "repro", "--write")
    proposed = cli.write("proposed.json", {"requirements": [
        {"id": "idea.repro.a1.platform", "concept": "idea", "kind": "must", "severity": "error", "check": "judged",
         "statement": "The checklist names the platform the reproducer runs on",
         "applies_to": {"harnesses": ["claude-code", "codex"]}, "evidence": "Vendor",
         "sources": ["https://docs.example-vendor.com/repro/platforms"], "contested": False}]})
    ok("accept", "--decision", path, "--part", "A1", "--proposed", proposed,
       "--choices", cli.write("choices.json", {"idea.repro.a1.platform": "accept"}), "--root", root, "--slug", "repro")
    revision = root / ".harness/research/repro.rules.yaml"
    ok("build", "--decision", path, "--part", "A1", "--revision", revision, "--evidence", workers,
       "--relay", cli.confirm(path, "build-1", "--revision", revision),
       "--description", cli.write("description.txt", DESCRIPTION), "--procedure", cli.write("procedure.md", PROCEDURE),
       "--root", root)
    cases = yaml.safe_load((FORGE / "evals/smoke/vertical.yaml").read_text(encoding="utf-8"))
    for case in cases["cases"]:
        case["part_id"] = "A1"
    cases_path = cli.write("cases.yaml", yaml.safe_dump(cases))
    ok("verify", "--decision", path, "--root", root, "--revision", revision, "--evidence", workers,
       "--relay", cli.confirm(path, "verify-1", "--revision", revision), "--harness", "claude-code",
       "--cases", cases_path, "--slug", "repro", "--write")


class CheckReferencesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix="reference-")
        cls.reference = Path(cls.directory.name) / "recorded"
        cls.reference.mkdir()
        record_reference(cls.reference)
        cls.forge = check_references._forge(FORGE)
        data = check_references._report_data((cls.reference / REPORT).read_text(encoding="utf-8"),
                                             cls.forge["documents"])
        cls.labels = {part["part_id"]: {"harness_result": part["harness_result"], "goal_result": part["goal_result"]}
                      for part in data["parts"]}
        (cls.reference / "expected.yaml").write_text(yaml.safe_dump(
            {"harness": "claude-code", "slug": "repro", "cases": CASES, "parts": cls.labels}), encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="tampered-")
        self.root = Path(self.scratch.name) / "example"
        shutil.copytree(self.reference, self.root, symlinks=True)

    def tearDown(self):
        self.scratch.cleanup()

    def problems(self):
        return check_references.check_example(self.root, self.forge)

    def refused(self, *expected):
        problems = self.problems()
        self.assertTrue(problems, "the checker accepted it")
        for text in expected:
            self.assertTrue(any(text in problem for problem in problems), f"{text!r} not in {problems}")

    def report(self, change):
        """Edit the report's data block, as someone editing the stored report would."""
        path = self.root / REPORT
        text = path.read_text(encoding="utf-8")
        match = re.search(r"(## Report data\n\n```json\n)(.*?)(\n```)", text, re.S)
        data = json.loads(match.group(2))
        change(data)
        path.write_text(text[:match.start(2)] + json.dumps(data, indent=2, sort_keys=True) + text[match.end(2):],
                        encoding="utf-8")

    def expected(self, change):
        path = self.root / "expected.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(yaml.safe_dump(data), encoding="utf-8")

    def cases(self, change):
        path = self.root / CASES
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(yaml.safe_dump(data), encoding="utf-8")

    def decision(self, change):
        record = load_decision(self.root / DECISION)
        change(record)
        write_decision(self.root, record, slug="repro", date="2026-10-12")

    @staticmethod
    def part(data, part_id="A1"):
        return next(part for part in data["parts"] if part["part_id"] == part_id)

    def test_the_recorded_run_passes(self):
        self.assertEqual(self.labels["A1"], {"harness_result": "verified", "goal_result": "met by the verified build"})
        self.assertEqual(self.problems(), [])

    def test_a_goal_changed_after_verification(self):
        self.decision(lambda record: record.part("A1").update(goal="Publish every log instead"))
        self.refused()

    def test_an_unsupported_override_that_retires_a_rule(self):
        (self.root / ".harness/overrides").mkdir(exist_ok=True)
        (self.root / ".harness/overrides/skills.description.length.yaml").write_text(yaml.safe_dump(
            {"rule_id": "skills.description.length", "finding_id": "F9", "reason": "Not needed.", "retired": True,
             "link": None}), encoding="utf-8")
        self.refused("overrides")

    def test_a_changed_skill_or_an_unrecorded_helper(self):
        skill = self.root / f".agents/skills/{NAME}/SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8").replace("## Procedure", "## Procedure\n\nDelete logs."),
                         encoding="utf-8")
        self.refused("not name exactly the part's frozen files")
        skill.write_text((self.reference / f".agents/skills/{NAME}/SKILL.md").read_text(encoding="utf-8"),
                         encoding="utf-8")
        (skill.parent / "helper.py").write_text("print('never verified')\n", encoding="utf-8")
        self.refused("not name exactly the part's frozen files")

    def test_verified_over_failed_results_or_an_unmet_goal(self):
        def failed(data):
            item = next(item for item in self.part(data)["rule_results"] if item["rule_id"] == "skills.name.format")
            item["result"] = "fail"
            self.part(data)["goal_verdict"]["verdict"] = "not-met"
        self.report(failed)
        self.refused("part A1")

    def test_a_judgment_left_out_or_excluded_against_its_fixed_applicability(self):
        def missing(data):
            item = next(item for item in self.part(data)["rule_results"] if item["rule_id"] == "idea.repro.a1.platform")
            item.update(result="missing", reason="no valid verdict")
            item.pop("citation")
        self.report(missing)
        self.refused("part A1")
        shutil.copy(self.reference / REPORT, self.root / REPORT)

        def excluded(data):
            item = next(item for item in self.part(data)["rule_results"] if item["rule_id"] == "idea.repro.a1.platform")
            item["result"] = "not-applicable"
        self.report(excluded)
        self.refused("part A1")

    def test_parts_left_out_of_the_report_or_expected_labels(self):
        self.report(lambda data: data.update(parts=[part for part in data["parts"] if part["part_id"] != "A1"]))
        self.refused("parts")
        shutil.copy(self.reference / REPORT, self.root / REPORT)
        self.expected(lambda data: data["parts"].pop("A1"))
        self.refused("expected.yaml names parts")
        shutil.copy(self.reference / "expected.yaml", self.root / "expected.yaml")
        self.expected(lambda data: data["parts"].update(A1={}))
        with self.assertRaisesRegex(ValueError, "states both"):
            self.problems()

    def test_a_blocked_decision_or_a_stale_selection(self):
        self.decision(lambda record: record.part("A1").update(status="blocked"))
        self.refused("bound_inputs")
        shutil.copy(self.reference / DECISION, self.root / DECISION)
        self.decision(lambda record: record.part("A1").update(recommended="subagents"))
        self.refused()

    def test_a_report_without_a_confirmed_contract(self):
        self.report(lambda data: data.update(contract_digest=None))
        self.refused("no confirmed contract")

    def test_runtime_evidence_for_other_prompts_expectations_or_skills(self):
        def other_prompt(data):
            for item in data["runtime_results"]:
                item.update(prompt="/harness-intake", expected="does-not-activate", observed_activation=None)
        self.report(other_prompt)
        self.refused("another prompt or expectation")
        shutil.copy(self.reference / REPORT, self.root / REPORT)

        def other_skill(data):
            for item in data["runtime_results"]:
                if item["observed_activation"]:
                    item["observed_activation"] = f"Skill tool called for other-{NAME}"
        self.report(other_skill)
        self.refused(f"not the skill in .agents/skills/{NAME}")
        shutil.copy(self.reference / REPORT, self.root / REPORT)
        self.report(lambda data: [item.update(file_hashes={}) for item in data["runtime_results"]])
        self.refused("runtime")

    def test_a_near_miss_left_out_or_not_run(self):
        self.cases(lambda data: data.update(cases=[case for case in data["cases"] if case["mode"] == "explicit"]))
        self.refused("near miss")
        shutil.copy(self.reference / CASES, self.root / CASES)

        def not_run(data):
            item = next(item for item in data["runtime_results"] if item["expected"] == "does-not-activate")
            item.update(result="not-run", reason="timed out")
        self.report(not_run)
        self.refused("a reference run passes every case")

    def test_outside_dependencies_removed_to_claim_the_goal(self):
        def hidden(data):
            for part in data["parts"]:
                part["outside_dependencies"] = []
                part["goal_result"] = "met by the verified build"
        self.report(hidden)
        self.expected(lambda data: [labels.update(goal_result="met by the verified build")
                                    for labels in data["parts"].values()])
        self.refused("outside_dependencies")

    def test_a_cases_path_outside_the_example(self):
        outside = Path(self.scratch.name) / "outside.yaml"
        outside.write_text("canary-value\n", encoding="utf-8")
        self.expected(lambda data: data.update(cases=str(outside)))
        problems = self.problems()
        self.assertTrue(any("runtime cases" in problem for problem in problems), problems)
        self.assertFalse(any("canary" in problem for problem in problems), "the file outside was read")

    def test_accepted_requirements_without_their_research(self):
        (self.root / ".harness/research/repro.md").unlink()
        self.refused("deep research")

    def test_an_invented_rule_result(self):
        self.report(lambda data: self.part(data)["rule_results"].append(
            {"rule_id": "invented.unspecified.rule", "check": "judged", "result": "pass", "reason": "Meets it.",
             "citation": "SKILL.md"}))
        self.refused("not requested")

    def test_report_metadata_that_contradicts_its_bound_inputs(self):
        self.report(lambda data: data.update(file_hashes={}, symlinks={}, decision_digest="0" * 64,
                                             idea_digest="0" * 64, rules_digest="0" * 64))
        self.refused("decision_digest", "file_hashes", "idea_digest", "rules_digest", "symlinks")

    def test_report_text_that_contradicts_its_data(self):
        path = self.root / REPORT
        path.write_text(path.read_text(encoding="utf-8").replace("- Harness result: verified",
                                                                 "- Harness result: verified, and great"),
                        encoding="utf-8")
        self.refused("text is not what Forge renders")

    def test_metadata_linked_from_outside_the_example(self):
        outside = Path(self.scratch.name) / "outside.yaml"
        outside.write_text('secret: "SYNTHETIC_PRIVATE_CANARY\n', encoding="utf-8")
        for name in ("expected.yaml", REPORT):
            with self.subTest(name=name):
                shutil.rmtree(self.root)
                shutil.copytree(self.reference, self.root, symlinks=True)
                (self.root / name).unlink()
                (self.root / name).symlink_to(outside)
                problems = self.problems()
                self.assertTrue(any("symbolic link" in problem for problem in problems), problems)
                self.assertFalse(any("CANARY" in problem for problem in problems), "the linked file was read")

    def test_runtime_evidence_from_another_harness(self):
        def codex(data):
            for item in data["runtime_results"]:
                item["harness"] = "codex"
                if item["observed_activation"]:
                    item["observed_activation"] = f"read .agents/skills/{NAME}/SKILL.md"
        self.report(codex)
        self.refused("ran in codex")

    def test_a_passing_near_miss_that_activated(self):
        def activated(data):
            item = next(item for item in data["runtime_results"] if item["expected"] == "does-not-activate")
            item["observed_activation"] = f"Skill tool called for {NAME}"
        self.report(activated)
        self.refused("passed although it observed an activation")

    def test_a_case_for_a_part_the_decision_does_not_build(self):
        def extra(data):
            case = copy.deepcopy(data["cases"][0])
            case.update(id="extra", part_id="A9", mode="implicit")
            data["cases"].append(case)
        self.cases(extra)
        self.refused("case extra names part A9")

    def test_an_unaccepted_requirement_in_an_unconfirmed_build(self):
        skill = self.root / f".agents/skills/{NAME}/SKILL.md"
        text = skill.read_text(encoding="utf-8")
        line = next(line for line in text.splitlines() if line.startswith("1. "))
        skill.write_text(text.replace(line, line + "\n2. Must: Attach every log."), encoding="utf-8")
        self.report(lambda data: data.update(confirmed_parts=["A2"]))
        self.refused("SKILL.md requirements")

    def test_an_activation_through_a_tool_the_case_does_not_permit(self):
        self.cases(lambda data: [case["permitted_tools"].update({"claude-code": ["Read"]}) for case in data["cases"]])
        self.refused("through a tool the case does not permit")

    def test_a_local_reuse_part_may_own_runtime_cases(self):
        """A reused skill installed in the repository is tested like a build, under its own path."""
        from tests.builders import decision as make_decision, part as make_part
        reused = make_decision(make_part("A1", "Reuse a checklist skill", outcome="reuse", recommended="skills",
                                         chosen="skills", reuse={"name": NAME, "path": f"vendor/skills/{NAME}"}))
        cases = [{"id": "explicit", "part_id": "A1", "mode": "explicit", "expected": "activates",
                  "permitted_tools": {"claude-code": ["Skill"]}},
                 {"id": "near-miss", "part_id": "A1", "mode": "negative", "expected": "does-not-activate",
                  "permitted_tools": {"claude-code": ["Skill"]}}]
        owners = check_references._case_owners(reused, self.forge["verify"])
        self.assertEqual(owners, {"A1": f"vendor/skills/{NAME}"})
        self.assertEqual(check_references._case_problems(owners, cases), [])
        self.assertEqual(check_references._case_problems({}, cases)[0],
                         "case explicit names part A1, which the decision neither builds nor reuses locally")

    def test_a_review_report_is_not_a_reference_run(self):
        self.report(lambda data: data.update(scope_parts=["A1"]))
        self.refused("is a Review")


if __name__ == "__main__":
    unittest.main()
