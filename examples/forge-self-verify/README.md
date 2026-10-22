# Forge verifies its own skills

harness-verify run on Harness Forge's four skills, as task 14 asks. The
result lives in Forge's repository, where the skills are:
`.harness/` and the generated `## Outside controls` section of its
README, last written by FORGE PR #23. `claude-code/expected.yaml`
names that sibling checkout (`repository: harness-forge`), and
`tools/check_references.py` replays the result from it.

## How it was run

The agent ran the session on 2026-10-22 under the owner's re-focus of
task 14 (see the plan), playing the user in a headless Claude Code
session, one message per turn: five turns, about 27 minutes. It
confirmed every contract and accepted or rejected every proposed
requirement there.

- A fresh clone of Forge at `5294508`, loaded as the plugin with
  `--plugin-dir`. It started from the 2026-10-21 decision, research and
  report, which Forge's main branch holds.
- Claude Code 2.1.308, subscription login, the account's default model.
- Four parts, each a local reuse of its skill under `skills/<name>` with
  skill home `plugin`. Each declares Forge's shared code as
  `reuse.dependencies`: `scripts/`, `src/harness_forge/`, `workers/`,
  `templates/`, `schemas/`, `requirements.lock` and the snapshot files
  the code reads. The reviewer judged them with the skill.
- Only harness-intake (B) and harness-research (C) changed since their
  pins at `5ff7fc0`, so only B and C moved their pins to `5294508`. Forge
  reported both as needing a new deep pass and acceptance, and the
  session showed that unchanged (FORGE #15). build-skill (A) and
  harness-verify (D) keep their `5ff7fc0` pins and requirements.
- Every part was selected again, because the snapshot now lists each
  outside control's gate conditions (FORGE #13). The mechanisms did not
  change.
- Targets both harnesses, reach public, lethal trifecta set, so Forge's
  `outer-isolation` recommendation applies as a precaution, not as a goal
  dependency. No runtime cases: those for a plugin skill report not-run.
- The new deep passes kept 6 findings for each of B and C. Of their 13
  proposed requirements, 10 were accepted. Two that had been accepted
  before were rejected because the new pass kept no finding for their
  sources, and one because its source did not support it.
- The first Extensive review left each part on one unresolved error
  rule, `skills.invocation.side-effects-user-invoked`, judged not
  applicable. The session confirmed that for all four parts. The second
  Extensive review, the one recorded, judged the rule applicable and
  passed it.

## Results

| Part | Skill | Harness result | Goal result |
| --- | --- | --- | --- |
| A | build-skill | verified | met by the verified build |
| B | harness-intake | verified | met by the verified build |
| C | harness-research | verified | met by the verified build |
| D | harness-verify | verified | met by the verified build |

- C passes `idea.forge-self-verify.c.untrusted-marked`, which failed in
  the 2026-10-21 result (FORGE #12 and #14).
- The gate-condition warnings `outside.gate.no-broader-bypass`,
  `outside.merge.no-agent-bypass` and
  `outside.merge.requester-cannot-approve` pass on every part, because
  the README section `forge.py readme` writes now lists them.
- One warning fails: D's `skills.references.load-conditions`.
  harness-verify's SKILL.md repeats the conditions of the `verified` row
  in `references/contract.md`.

The 2026-10-21 result (C not verified) is in Forge's history at
`80244fd`.
