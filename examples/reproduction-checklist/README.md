# Reproduction checklist: hands-on reference runs

The owner ran Harness Forge by hand once per harness on 2026-10-11, from
the same starting idea: "I want a skill that turns approved bug reports
into reproduction checklists." Each folder holds the result repository
as the session left it: the decision, research and accepted
requirements under `.harness/`, the built skill, and the README with its
`Outside controls` section. The trial repositories' `AGENTS.md`, which
names local paths, and the agent's own scratch files are left out.

Both sessions ran Forge `4b8348f` with the KB pinned at `1b1310f`, on
subscription logins, with the account's default model.

| | Claude Code | Codex |
| --- | --- | --- |
| Harness | Claude Code 2.1.296 | codex-cli 0.162.1 |
| Targets and reach | both harnesses, public | Codex, this repository |
| Mechanism | skill, chosen over the recommended subagent | skill, as recommended |
| Accepted requirements | 9 | 2 |
| Harness result | not verified | verified |
| Goal result | not met | met by the verified build |
| Runtime cases | explicit, implicit and near miss pass | explicit and implicit pass; no near miss written |
| Confirmed not applicable | `skills.invocation.side-effects-user-invoked` | `skills.invocation.side-effects-user-invoked` |

The Claude Code result is not verified because the reviewer failed
`skills.goal.no-must-hold-rule-in-skill`: it read "no implementation
edits" in the goal as a rule that must hold on every edit. The user had
answered that the part may occasionally be skipped, and an earlier
reviewer in the same session passed the rule.

## Fixed after these sessions

Forge `63ba1cf`..`4512819` and KB `f1f14b5`:

- A build over a changed skill showed its diff instead of crashing.
- Requirements are numbered and stated once, with one period. The
  reference file gives each one's rule id and sources.
- `must-not` requirements name the forbidden behavior, so "Never:" no
  longer reads as a double negative.
- `forge.py readme` writes the Outside controls section with each
  condition spelled out instead of rule ids.
- A worker that does not complete says why. In Codex, it also says to
  rerun the command outside the session's sandbox.
- The must-hold rule applies only when the user answered that the part
  must hold every time.
- The bypass question asks about the agent's permission prompts, not
  about a skill asking the user questions.
- Intake asks in the user's terms, with lettered choices.
- Verify needs an explicit and a near-miss runtime case per part.

These folders keep the sessions' original output, from before the
fixes. Claude Code discovers `.claude/skills/` folders below the
working directory, so a session that works on files in `claude-code/`
can list `repro-checklist` as a skill.

## Checked reference runs

`tools/check_references.py` replays Forge's verification of a stored run
instead of trusting its report. It applies the refusals `forge.py verify`
makes before it runs, prepares the run from the repository as it is now
and finishes it with Forge's own code, then requires the stored report to
be exactly the report Forge renders. Only what the live run alone knows
comes from the report: the reviewer's verdicts, the runtime observations,
the worker evidence and the user's choices. A reference run must also
pass every declared runtime case with its own skill activated, and match
the labels in its `expected.yaml`, which names its runtime cases file.
`tools/test_check_references.py` records a run with Forge's scripted
workers and checks that each kind of tampering is refused.

A Review report is refused, because its kept results rest on an earlier
report; record a reference run as a first run or an Extensive review.
These two folders predate Forge's current report format and have no
`expected.yaml`, so the checker fails on them until the plan's task 14
records new reference runs here.
