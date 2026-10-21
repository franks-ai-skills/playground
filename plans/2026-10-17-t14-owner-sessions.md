# Task 14: the owner sessions

> **2026-10-21:** the owner asked the agent to run these sessions itself
> and re-focused T14. Part 2 runs in Claude Code only, with each reuse
> source pinned to the reviewed commit and Forge's helpers declared as
> `reuse.dependencies`. See the re-focus note in task 14 of the
> [plan](2026-10-07-harness-forge-thin-slice.md).

What remains of plan task 14 needs the owner: the reference runs, where a
person confirms the contract and accepts requirements, and harness-verify
on Forge's own skills. Two sessions cover both, one in Claude Code and one
in Codex. Everything that can run without them already has:
`tools/test_reference_scenario.py` runs the same scenario through Forge's
CLI with scripted workers, in both harnesses, up to a result that
`tools/check_references.py` accepts.

Each session uses subscription logins only, with Forge installed as the
plugin from `main`. Before starting, follow
[the local development note](harness-forge-local-development.md).

## Part 1: the reference run (per harness)

1. Create the starting repository in a new directory:
   `../harness-forge/.venv/bin/python tools/reference_runs.py start <dir>`.
   It holds a README and the team's existing `bug-report-format` skill in
   `.agents/skills/` with its `.claude/skills` link.
2. Open the harness in `<dir>` and give Forge the idea: "Handle incoming
   bug reports from intake to closing." Split it into the parts below when
   intake asks. The answers are suggestions that select each outcome; the
   owner decides, and a different but honest result is kept, not forced.

   | Part | Goal | Answers that differ from a plain skill | Expected outcome |
   | --- | --- | --- | --- |
   | A1 | Write a reproduction checklist from an approved bug report | none | harness-only, skill |
   | A2 | Check a fix against its reproduction checklist before it merges | must survive a compromised agent: required | outside-alongside, skill plus a gate |
   | A3 | Format incoming bug reports with the team's template | reuse `.agents/skills/bug-report-format` (home: repository) | reuse, local |
   | A4 | Fix the failing CI checks on the fix's pull request | reuse `gh-fix-ci` from openai/skills (Apache-2.0) if research confirms it | reuse, remote |
   | A5 | Close the tracker issue once the fix ships | irreversible | outside-instead |
   | A6 | Label every incoming bug report | must happen every time | nothing-fits |

   A4 depends on live research confirming a public skill's fit, license
   and maintenance; `gh-fix-ci` in openai/skills
   (`skills/.curated/gh-fix-ci`, Apache-2.0) is the prepared candidate.
   If research rejects it, keep that result: a remote reuse confirmed
   live is still missing, which blocks task 14, and a separate short
   session on an idea whose only part is that candidate closes it.
3. Confirm the contract, accept requirements in the deep pass, and let
   Forge build A1 and A2. For verification, the agent writes runtime
   cases (explicit, implicit and a negative near miss per built part) to
   `.harness/cases.yaml`.
4. Verify (first run). A built part is verified only when one of its
   explicit cases passes: an explicit case that stays not-run, as `$name`
   in Codex can, leaves the part not verified, and the checker accepts
   that report as true without counting it as verified. Then break A1 by hand, for example by renaming its
   `name:` in `SKILL.md`, verify again and expect A1 not verified; let
   the builder repair only that file, answer the scope question with
   Review, and verify. Close with an Extensive review: the checker
   refuses a Review report as the stored reference.
5. Collect the result:
   `../harness-forge/.venv/bin/python tools/reference_runs.py collect <dir>
   examples/bug-intake/<harness> --harness <harness> --slug <slug>
   --cases .harness/cases.yaml`. It copies only what Forge reads and
   binds (`.harness/`, README, the cases file, the skills and their
   links), writes `expected.yaml` and runs the checker. The report binds
   every checked file's hash, so remove anything that names local paths
   or accounts before the closing Extensive review, not after it.

In Codex, near misses report not-run, because Codex cannot show a
non-activation, and the checker accepts that. An explicit `$name` that
leaves no signal is different: it keeps the part not verified (step 4).

## Part 2: harness-verify on Forge's own skills (same session)

In a clone of harness-forge with the plugin installed, ask Forge to verify
its own four skills. Suggested answers, for the owner to confirm:

- Targets both harnesses; reach public; the repository is trusted, but
  research fetches untrusted pages while login material and network
  access are present, so the lethal-trifecta fact is set and Forge's
  research-isolation recommendation applies. It is recorded, not marked
  as an installed control or a goal dependency.
- Four parts, one per skill, each reusing the skill in place:
  `skills/<name>` with home `plugin` (beside `plugin.json`), source the
  harness-forge repository, license AGPL-3.0-only, maintained.
- Goals from each skill's description; no runtime cases, since runtime
  cases for a plugin skill report not-run (README, runtime gaps).
- Each reused skill still needs its deep pass and acceptance, even when
  none is accepted: `verify` refuses a part without an accepted revision.

Fix errors Forge reports; keep warnings and contested positions in the
report. Then run `tools/check_references.py`, the Forge suite and the KB's
`tools/validate.py`, and commit with
`test: record portable skills pipeline reference runs`.

## Cost

Each session is a normal interactive Forge run plus its workers: survey
and deep research, source support, two builds, four verifications with a
review worker each and six runtime cases per verification in the
reference run; in the self-verification a survey, four deep passes with
their source-support workers, and one verification. No batch
evaluation runs.
