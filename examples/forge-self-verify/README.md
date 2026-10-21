# Forge verifies its own skills

harness-verify run on Harness Forge's four skills, as task 14 asks. The
result lives in Forge's repository, where the skills are:
`.harness/` and the generated `## Outside controls` section of its
README, added by FORGE PR #11. `claude-code/expected.yaml` names that
sibling checkout (`repository: harness-forge`), and
`tools/check_references.py` replays the result from it.

## How it was run

The agent ran the session on 2026-10-21 under the owner's re-focus of
task 14 (see the plan), playing the user in a headless Claude Code
session, one message per turn. It confirmed every contract and accepted,
edited or rejected every proposed requirement there.

- A fresh clone of Forge, loaded as the plugin with `--plugin-dir`.
  Intake, research and acceptance ran at `5ff7fc0`, the verification at
  `d7abb41`. Only `src/`, `schemas/`, `workers/` and `tests/` changed
  between the two, and the verification reviewed those files.
- Claude Code 2.1.306, subscription login, the account's default model.
- Four parts, each a local reuse of its skill under `skills/<name>` with
  skill home `plugin`, pinned to `5ff7fc0`. Each declares Forge's shared
  code as `reuse.dependencies`: `scripts/`, `src/harness_forge/`,
  `workers/`, `templates/`, `schemas/`, `requirements.lock` and the
  snapshot files the code reads. The reviewer judged them with the skill.
- Targets both harnesses, reach public, lethal trifecta set, so Forge's
  `outer-isolation` recommendation applies as a precaution, not as a goal
  dependency. No runtime cases: those for a plugin skill report not-run.
- A survey, a deep pass per part and 19 accepted requirements, two of
  them edited. Three were rejected: one about a library Forge does not
  use, one outside intake's goal and one duplicate.

## Results

| Part | Skill | Harness result | Goal result |
| --- | --- | --- | --- |
| A | build-skill | verified | met by the verified build |
| B | harness-intake | verified | met by the verified build |
| C | harness-research | not verified | not met |
| D | harness-verify | verified | met by the verified build |

- C fails `idea.forge-self-verify.c.untrusted-marked`: harness-research
  keeps fetched content apart from the user's input, but never marks it
  as untrusted where it shows findings or drift. The error is deferred
  as a failure, as the re-focus allows. Fixing it changes the skill, so
  its pin, brief and deep pass would change too.
- Warnings on every part come from the README section `forge.py readme`
  writes: `outside.gate.no-broader-bypass`, `outside.merge.no-agent-bypass`
  and `outside.merge.requester-cannot-approve` find conditions it does
  not list for the CODEOWNERS control.
- B warns on `security.untrusted-input.as-data`: harness-intake does not
  say to treat research findings and records as data. build-skill and
  harness-verify do.
