# Forge verifies its own skills

harness-verify run on Harness Forge's four skills, as task 14 asks. The
result lives in Forge's repository, where the skills are:
`.harness/`, last written by FORGE PR #40, and the generated
`## Outside controls` section of its README, unchanged since FORGE
PR #28. `claude-code/expected.yaml`
names that sibling checkout (`repository: harness-forge`), and
`tools/check_references.py` replays the result from it.

The result binds the hashes of the Forge code each part declares as a
dependency, so any later change to that code makes this example fail
against Forge `main` until the verification is recorded again.

## How it was run

The agent ran the session on 2026-10-23 under the owner's working mode
(see playground's `AGENTS.md`), playing the user in a headless Claude
Code session, one message per turn: six turns. It confirmed every
contract and answered every proposed requirement there.

- A fresh clone of Forge at `8b9bb91`, loaded as the plugin with
  `--plugin-dir`, with the KB pinned at `5236d06`. It started from the
  decision, research and report of the run before (FORGE PR #35).
- Claude Code 2.1.309, subscription login, the account's default model.
- Four parts, each a local reuse of its skill under `skills/<name>` with
  skill home `plugin`. Each declares Forge's shared code as
  `reuse.dependencies`: `scripts/`, `src/harness_forge/`, `workers/`,
  `templates/`, `schemas/`, `requirements.lock` and the snapshot files
  the code reads. The reviewer judged them with the skill.
- Since the run before, harness-research (C) changed (FORGE #36: it says
  when to read its worker reference), and so did the shared
  `scripts/setup.py` and `src/harness_forge/environment.py` (FORGE #38:
  Forge rebuilds an environment whose Python no longer starts). So C
  moved its pin to `8b9bb91` and had a new deep pass. build-skill (A)
  keeps `5ff7fc0`, harness-intake (B) and harness-verify (D) keep
  `93f5285`; their changed dependencies were reviewed with them.
- C's deep pass and its re-check of lost sources allowed C1 to C6 as
  recorded. C7 now cites harness-research's `SKILL.md` at `8b9bb91`,
  because no finding at the old pin was kept. C8 (`validated-format`) is
  new. A proposed C9 (`canonical-hash`) was rejected, because hashing is
  Forge's code, not the skill's behavior.
- Targets both harnesses, reach public, lethal trifecta set, so Forge's
  `outer-isolation` recommendation applies as a precaution, not as a goal
  dependency. No runtime cases: those for a plugin skill report not-run.
- 24 accepted requirements: 5 for A, 5 for B, 8 for C and 6 for D.
- The first verify run was the recorded one: no review reply was
  rejected and no rule was left unresolved.
- An earlier attempt on 2026-10-23 stopped in its first turn and
  changed nothing: Forge's environment had been built on a Python that
  Homebrew had since removed. That is FORGE #38.

## Results

| Part | Skill | Harness result | Goal result |
| --- | --- | --- | --- |
| A | build-skill | verified | met by the verified build |
| B | harness-intake | verified | met by the verified build |
| C | harness-research | verified | met by the verified build |
| D | harness-verify | verified | met by the verified build |

No rule fails. The warning `skills.references.load-conditions`, which
failed on C in the run before, passes.

Earlier results are in Forge's history: the 2026-10-21 result, C not
verified, at `80244fd`; the first 2026-10-22 result, at Forge `5294508`
with all four verified and D's warning failed, at `ca99fae`; the second,
at `93f5285` with no failed rule, at `2c1aa23`; the 2026-10-22 result
at `4db8962`, with all four verified and C's warning failed, at
`1e0fba9`.
