# Forge verifies its own skills

harness-verify run on Harness Forge's four skills, as task 14 asks. The
result lives in Forge's repository, where the skills are:
`.harness/` and the generated `## Outside controls` section of its
README, last written by FORGE PR #28. `claude-code/expected.yaml`
names that sibling checkout (`repository: harness-forge`), and
`tools/check_references.py` replays the result from it.

## How it was run

The agent ran the session on 2026-10-22 under the owner's re-focus of
task 14 (see the plan), playing the user in a headless Claude Code
session, one message per turn: eight turns, about 48 minutes of session
time. It confirmed every contract and accepted every proposed
requirement there.

- A fresh clone of Forge at `93f5285`, loaded as the plugin with
  `--plugin-dir`, with the KB pinned at `5236d06`. It started from the
  decision, research and report of the run before (FORGE PR #23).
- Claude Code 2.1.308, subscription login, the account's default model.
- Four parts, each a local reuse of its skill under `skills/<name>` with
  skill home `plugin`. Each declares Forge's shared code as
  `reuse.dependencies`: `scripts/`, `src/harness_forge/`, `workers/`,
  `templates/`, `schemas/`, `requirements.lock` and the snapshot files
  the code reads. The reviewer judged them with the skill.
- harness-intake (B) and harness-verify (D) changed since their pins, so
  B and D moved their pins to `93f5285`. build-skill (A) keeps `5ff7fc0`
  and harness-research (C) `5294508`.
- The snapshot asks the new part fact `side_effects` (KB #4), which every
  part answers false. That changed every part's research brief, so all
  four had a new deep pass. D's first pass kept no finding from
  harness-verify's `SKILL.md`, so its two requirements on runtime results
  could not be proposed (FORGE #24); a rerun of D's pass found them
  again.
- Targets both harnesses, reach public, lethal trifecta set, so Forge's
  `outer-isolation` recommendation applies as a precaution, not as a goal
  dependency. No runtime cases: those for a plugin skill report not-run.
- 22 accepted requirements: 5 for A, 5 for B, 6 for C and 6 for D.
- The first review left `skills.invocation.side-effects-user-invoked`
  unresolved on every part, judged not applicable; the session confirmed
  that for all four. Of the four verify runs after it, two review replies
  were rejected by Forge's review validation (a misspelled rule id, a
  duplicate verdict) and one review worker stopped at the subscription's
  usage limit. The last run is the one recorded.

## Results

| Part | Skill | Harness result | Goal result |
| --- | --- | --- | --- |
| A | build-skill | verified | met by the verified build |
| B | harness-intake | verified | met by the verified build |
| C | harness-research | verified | met by the verified build |
| D | harness-verify | verified | met by the verified build |

No rule fails at any severity. The warning
`skills.references.load-conditions` on D, failed in the run before,
passes after FORGE PR #25.

Earlier results are in Forge's history: the 2026-10-21 result, C not
verified, at `80244fd`; the first 2026-10-22 result, at Forge `5294508`
with all four verified and D's warning failed, at `ca99fae`.
