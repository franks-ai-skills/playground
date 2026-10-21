# Bug intake: task 14's reference runs

Two sessions, one per harness, on the idea "Handle incoming bug reports
from intake to closing", from the starting repository
`tools/reference_runs.py start` creates. `claude-code/` and `codex/` hold
each result as `tools/reference_runs.py collect` copies it.

## How they were run

The owner asked an agent to run the sessions in their place
(2026-10-18). Claude Opus 5.5 played the user in headless sessions, one
message per turn, and gave the runbook's answers
([`plans/2026-10-17-t14-owner-sessions.md`](../../plans/2026-10-17-t14-owner-sessions.md)).
It confirmed every contract and accepted or rejected every requirement
there; no confirmation was scripted.

- Forge `7cd81c6`, with the KB pinned at `ec829ae`, loaded as a plugin:
  in Claude Code with `--plugin-dir` for each session, in Codex installed
  from a local marketplace on `main`.
- Claude Code 2.1.302 and codex-cli 0.162.1, subscription logins only.
  The owner's other plugins were turned off for these sessions.
- Claude Code ran with Forge's CLI, a few read-only commands and edits
  inside the repository allowed. Codex kept its workspace-write sandbox
  and sent escalation requests, such as starting Forge's workers, to its
  automatic reviewer.
- The team, its repository `example-team/bug-intake` and its customer
  status page are fictional. The commit that pins the reused
  `bug-report-format` skill was made in the starting repository for that
  purpose.
- The agents' working files were moved out of `.harness/` before the
  closing Extensive review, so the examples name no local paths. Codex's
  `.harness/intake/` keeps the two files its decision record cites.

### Codex, re-verified on 2026-10-21

The owner re-focused task 14 on 2026-10-21 (see the plan) and allowed a
temporary way to observe `$name`. The agent copied the Codex repository,
started a new Codex session with `HARNESS_FORGE_TEMPORARY_CODEX_ROLLOUT=1`
and asked for a closing Extensive review. The session confirmed the
contract again and confirmed that
`skills.invocation.side-effects-user-invoked` does not apply to A1 and D,
as before. The decision, research, skills and cases are unchanged; only
the report is new.

- Forge `d7abb41`, read from a clone at that commit, because the
  installed copy was stale. codex-cli 0.163.0, subscription login.
- With Forge `5ff7fc0`, the first review credited C's explicit case from
  the observer ("instructions injected … (session rollout)"), but its
  reviewer failed C's goal because the required outside gate is not
  verified. The report already shows that dependency separately. Forge
  `d7abb41` tells the reviewer which outside controls a goal needs, and
  the closing review judged C's goal met, so C depends on outside
  controls.
- The 2026-10-18 result is in
  [`../history/2026-10-18-bug-intake-codex/`](../history/2026-10-18-bug-intake-codex/).

## Results

| Part | Outcome | Claude Code | Codex |
| --- | --- | --- | --- |
| A1 format a report | reuse, local (`bug-report-format`, pinned) | verified / met | verified / met |
| A2 label every report | nothing fits | not applicable / not met | not applicable / not met |
| B write the reproduction checklist | harness-only, user-invoked skill | verified / met | verified / met |
| C check the fix against it | outside-alongside, user-invoked skill and a required gate | verified / depends on outside controls | verified / depends on outside controls |
| D diagnose failing CI | harness-only, skill | verified / met | verified / met |
| E close the issue once the fix ships | outside-instead | not applicable / depends on outside controls | not applicable / depends on outside controls |

- In Codex, a `$name` invocation injects the skill without a stream
  event (Codex probe, 2026-10-18). In the closing review, the temporary
  observer credited B's explicit case from the session rollout, and C's
  passed because the model also read `SKILL.md`. Every negative case
  stays not-run in Codex, as do cases whose activation leaves no signal,
  such as A1's this time.
- Each session broke one built skill by renaming its `name:` (B in Claude
  Code, D in Codex), verified it as not verified, let the builder repair
  it, verified with a Review, and closed with an Extensive review.
- D was first a remote reuse of `gh-fix-ci` from `openai/skills`. That
  repository is deprecated ("This repository is deprecated."), found by
  Claude Code's deep research, so D was reselected and built in both
  sessions. The remote reuse is in [`../ui-flow-reuse/`](../ui-flow-reuse/).
