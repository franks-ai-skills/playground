# Forge verifies its own skills

harness-verify run on Harness Forge's four skills, as task 14 asks. The
result lives in Forge's repository, where the skills are:
`.harness/`, last written by FORGE PR #80 (the 0.3.0 release), and the
generated `## Outside controls` section of its README.
`claude-code/expected.yaml` names that sibling checkout (`repository:
harness-forge`) and the run's cases (`.harness/cases.yaml`), and
`tools/check_references.py` replays the result from it.

The result binds the hashes of the Forge code each part declares as a
dependency, so any later change to that code makes this example fail
against Forge `main` until the verification is recorded again.

## How it was run

The agent ran the session on 2026-10-26 under the owner's working mode
(see playground's `AGENTS.md`), playing the user in a headless Claude
Code session, one message per turn: three turns. It confirmed the
contract there, and in the third turn confirmed that
`skills.invocation.side-effects-user-invoked` does not apply to any
part, on the reviewer's reasons (development evidence).

- A fresh clone of Forge at `fe9154a` (`release/0.3.0-rc2`), loaded as
  the plugin with `--plugin-dir`, with the KB pinned at release `v0.6.0`.
  Driver `t14-runs/drive030d.py` (local), profile `claude-f1`.
- Claude Code 2.1.310, subscription login, the account's default model.
- Four parts, each a local reuse of its skill under `skills/<name>` with
  skill home `plugin`. Each declares Forge's shared code as
  `reuse.dependencies`: `scripts/`, `src/harness_forge/`, `workers/`,
  `templates/`, `schemas/`, `vendor/` and the snapshot files the code
  reads. The reviewer judged them with the skill. Pins: A `3767d7e`,
  B, C and D `112a631`.
- Targets both harnesses, reach public, lethal trifecta set, so Forge's
  `outer-isolation` recommendation applies as a precaution, not as a goal
  dependency. The session wrote 12 activation cases (explicit, implicit
  and near miss per skill); all report not-run, because Forge runs no
  runtime case for a skill shipped in a plugin.
- 24 accepted requirements: 5 for A, 5 for B, 8 for C and 6 for D.
- Review scope judging all four parts, so nothing is kept from an
  earlier report. The first verify run of the session left the
  side-effects rule unresolved for every part; the recorded run is the
  second, with the confirmations.

## Results

| Part | Skill | Harness result | Goal result |
| --- | --- | --- | --- |
| A | build-skill | verified | met by the verified build |
| B | harness-intake | verified | met by the verified build |
| C | harness-research | verified | met by the verified build |
| D | harness-verify | verified | met by the verified build |

One warning fails: D `skills.body.no-time-bound-statements` ("whose
runtime cases cannot run yet"). The owner released 0.3.0 with it; FORGE
#81 decides whether the finding is valid.

The release's earlier attempts found FORGE #71, #72, #73, #76 and #78;
their evidence is in `t14-runs/forge-self-verify-030*` (local).

Earlier results are in Forge's history: the 2026-10-21 result, C not
verified, at `80244fd`; the first 2026-10-22 result, at Forge `5294508`
with all four verified and D's warning failed, at `ca99fae`; the second,
at `93f5285` with no failed rule, at `2c1aa23`; the 2026-10-22 result
at `4db8962`, with all four verified and C's warning failed, at
`1e0fba9`; the 2026-10-23 result at `8b9bb91`, with all four verified
and no failed rule, at `703f8a2`; the 2026-10-24 result at `f447609`,
with all four verified and no failed rule, at `f24d15d`.
