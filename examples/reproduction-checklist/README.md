# Reproduction checklist: hands-on reference runs

The owner ran Harness Forge by hand once per harness on 2026-10-11, from
the same starting idea: "I want a skill that turns approved bug reports
into reproduction checklists." Each folder holds the result repository
as the session left it: the decision, research and accepted
requirements under `.harness/`, the built skill, and the README with its
`Outside controls` section. The trial repositories' `AGENTS.md`, which
names local paths, and the agent's own scratch files are left out.

Both sessions ran Forge `78a5678` with the KB pinned at `31f7664`, on
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

Forge `68f31e4`..`db79bfd` and KB `a631de5`:

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
