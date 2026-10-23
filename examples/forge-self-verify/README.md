# Forge verifies its own skills

harness-verify run on Harness Forge's four skills, as task 14 asks. The
result lives in Forge's repository, where the skills are:
`.harness/`, last written by FORGE PR #42, and the generated
`## Outside controls` section of its README, unchanged since FORGE
PR #28. `claude-code/expected.yaml`
names that sibling checkout (`repository: harness-forge`), and
`tools/check_references.py` replays the result from it.

The result binds the hashes of the Forge code each part declares as a
dependency, so any later change to that code makes this example fail
against Forge `main` until the verification is recorded again.

## How it was run

The agent ran the session on 2026-10-24 under the owner's working mode
(see playground's `AGENTS.md`), playing the user in a headless Claude
Code session, one message per turn: two turns. It confirmed the
contract there.

- A fresh clone of Forge at `f447609` (FORGE #41's branch), loaded as
  the plugin with `--plugin-dir`, with the KB pinned at release `v0.2.0`
  (`c29ac28`). It started from the decision, research and report of the
  run before (FORGE PR #40).
- Claude Code 2.1.309, subscription login, the account's default model.
- Four parts, each a local reuse of its skill under `skills/<name>` with
  skill home `plugin`. Each declares Forge's shared code as
  `reuse.dependencies`: `scripts/`, `src/harness_forge/`, `workers/`,
  `templates/`, `schemas/`, `requirements.lock` and the snapshot files
  the code reads. The reviewer judged them with the skill.
- Since the run before, no skill and no shared code changed. Forge now
  pins KB release 0.2.0 instead of an untagged commit that still said
  0.1.0 (FORGE #41, agent-harness-kb #8): `snapshot/kb-manifest.json`,
  a dependency of every part, names the new version and release
  commit, and every copied snapshot file is unchanged. The decision
  records `kb_version: 0.2.0`. All four parts keep their pins (A
  `5ff7fc0`, B and D `93f5285`, C `8b9bb91`), their research and their
  accepted requirements; Forge needed no new research.
- Targets both harnesses, reach public, lethal trifecta set, so Forge's
  `outer-isolation` recommendation applies as a precaution, not as a goal
  dependency. No runtime cases: those for a plugin skill report not-run.
- 24 accepted requirements: 5 for A, 5 for B, 8 for C and 6 for D.
- The first verify run was the recorded one: no review reply was
  rejected and no rule was left unresolved.

## Results

| Part | Skill | Harness result | Goal result |
| --- | --- | --- | --- |
| A | build-skill | verified | met by the verified build |
| B | harness-intake | verified | met by the verified build |
| C | harness-research | verified | met by the verified build |
| D | harness-verify | verified | met by the verified build |

No rule fails. The reviewer judged A's warning
`security.outbound.minimal-data` not applicable this time (the build
sends no data to an external service), where the run before passed it.

Earlier results are in Forge's history: the 2026-10-21 result, C not
verified, at `80244fd`; the first 2026-10-22 result, at Forge `5294508`
with all four verified and D's warning failed, at `ca99fae`; the second,
at `93f5285` with no failed rule, at `2c1aa23`; the 2026-10-22 result
at `4db8962`, with all four verified and C's warning failed, at
`1e0fba9`; the 2026-10-23 result at `8b9bb91`, with all four verified
and no failed rule, at `703f8a2`.
