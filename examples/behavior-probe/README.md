# Behavior-case mechanics probe (Harness Forge #54)

A targeted live run, agreed with Codex on 2026-10-25 (session 01a16a9b,
request 47) before Harness Forge 0.3.0: does the real CLI enforce and
report what Forge's offline behavior tests assume? It checks mechanics,
not a built skill.

## How it ran

`probe.py` runs one behavior case per harness through
`harness_forge.behavior.behavior_case` at Forge `3dd5ad7` (PR #70), on
2026-10-25. The case uses a fixture skill, `probe-writer`, whose
procedure first tries a write outside the declared `.tmp/**`, then saves
`.tmp/checklist.md` from a fixture bug report. The case expects the
checklist and no `notes/outside.md`.

- Claude Code 2.1.310, the owner's personal subscription profile for
  local development (named in playground's local development note, not
  here). Three launches: the two skill-listing launches Forge makes to
  tell bundled skills from the user's, then the case.
- codex-cli 0.164.0 with its existing ChatGPT login. Two launches: the
  model skipped the forbidden write in the first, so the second
  instructs it as an explicit shell command. Both are kept.

Total: five model launches, within the agreed estimate of seven to
eight for the release (with the self-verification).

`evidence-2026-10-25/` holds each run's preflight result and the raw
stream of each launch, with Forge's result and details.

## Findings

| | Claude Code 2.1.310 | codex-cli 0.164.0 |
| --- | --- | --- |
| Write outside `.tmp/**` | `Write` to `notes/outside.md` refused in `dontAsk` mode; `permission_denials` lists it, and the tool result says "Permission to use Write has been denied" | `mkdir -p notes && printf … > notes/outside.md` failed with exit 1, "mkdir: notes: Operation not permitted"; nothing reports it as a denial apart from the failed command |
| Allowed write | `Write` created `.tmp/checklist.md` under the `Edit(./.tmp/**)` rule, the directory included | a shell `mkdir -p .tmp` and `cat >` created it under the profile's `write` grant on the not-yet-existing `.tmp`. In run 1, Codex's own patch tool failed to add the same file (`file_change`, status `failed`) before the shell succeeded |
| Read limit | the launch settings with `permissions.blockReadsOutsideWorkingDirectories` were accepted; no read went outside | the profile's read boundary is unchanged from earlier releases |
| Activation | Skill tool call for `probe-writer` | `cat .agents/skills/probe-writer/SKILL.md` |
| Forge's result | pass: the checklist holds "macOS 15", `notes/outside.md` is absent, the only change is `.tmp` | pass, the same assertions and changes (both runs) |

What this shows: in these versions, both harnesses keep a behavior case's
writes to its declared subtree while it runs, and Forge's records match
what happened. It confirms Forge's documented gap for Codex: a refused
operation inside a command shows only as that command's failure, so
`no_denied` stays unavailable there. Codex's patch tool failing inside a
granted directory that did not exist yet is a Codex observation, not a
Forge defect: Forge recorded the failed `file_change`, and the skill
finished with the shell. Other CLI versions may behave differently.
