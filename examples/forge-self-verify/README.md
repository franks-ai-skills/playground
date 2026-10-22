# Forge verifies its own skills

harness-verify run on Harness Forge's four skills, as task 14 asks. The
result lives in Forge's repository, where the skills are:
`.harness/`, last written by FORGE PR #35, and the generated
`## Outside controls` section of its README, unchanged since FORGE
PR #28. `claude-code/expected.yaml`
names that sibling checkout (`repository: harness-forge`), and
`tools/check_references.py` replays the result from it.

The result binds the hashes of the Forge code each part declares as a
dependency, so any later change to that code makes this example fail
against Forge `main` until the verification is recorded again.

## How it was run

The agent ran the session on 2026-10-22 under the owner's working mode
(see playground's `AGENTS.md`), playing the user in a headless Claude
Code session, one message per turn: six turns. It confirmed every
contract and answered every proposed requirement there.

- A fresh clone of Forge, loaded as the plugin with `--plugin-dir`, with
  the KB pinned at `5236d06`. It started from the decision, research and
  report of the run before (FORGE PR #28). Turns 1 and 2 ran at Forge
  `7d45551`, turns 3 to 6 at `4db8962` (see below).
- Claude Code 2.1.308, subscription login, the account's default model.
- Four parts, each a local reuse of its skill under `skills/<name>` with
  skill home `plugin`. Each declares Forge's shared code as
  `reuse.dependencies`: `scripts/`, `src/harness_forge/`, `workers/`,
  `templates/`, `schemas/`, `requirements.lock` and the snapshot files
  the code reads. The reviewer judged them with the skill.
- Only harness-research (C) changed since its pin, so C moved its pin to
  `7d45551` and had a new deep pass. build-skill (A) keeps `5ff7fc0`,
  harness-intake (B) and harness-verify (D) keep `93f5285`.
- C's deep pass did not find the sources of four of its six earlier
  requirements again. The new `research --recheck` (FORGE #24) dropped
  every finding at first: the output schema the worker CLI enforces had
  no `requirement_id`, which offline tests had not caught. FORGE PR #34
  fixed that without touching `skills/`, so C kept its pin and deep
  pass, and the second re-check kept three findings that restored the
  lost sources. The session accepted C1 to C7; C4 and C5 now cite only
  the source bound to them, and C7 is new.
- Targets both harnesses, reach public, lethal trifecta set, so Forge's
  `outer-isolation` recommendation applies as a precaution, not as a goal
  dependency. No runtime cases: those for a plugin skill report not-run.
- 23 accepted requirements: 5 for A, 5 for B, 7 for C and 6 for D.
- The first verify run was the recorded one: no review reply was
  rejected and no rule was left unresolved.

## Results

| Part | Skill | Harness result | Goal result |
| --- | --- | --- | --- |
| A | build-skill | verified | met by the verified build |
| B | harness-intake | verified | met by the verified build |
| C | harness-research | verified | met by the verified build |
| D | harness-verify | verified | met by the verified build |

No error rule fails. One warning fails on C:
`skills.references.load-conditions`, because harness-research's
`SKILL.md` points to `references/contract.md` without saying when to
read it.

Earlier results are in Forge's history: the 2026-10-21 result, C not
verified, at `80244fd`; the first 2026-10-22 result, at Forge `5294508`
with all four verified and D's warning failed, at `ca99fae`; the second,
at `93f5285` with no failed rule, at `2c1aa23`.
