# Codex brief: how Claude and Codex work together

Claude sends this file at the start of every Codex call, followed by the
request. Codex cannot read Claude's persistent instructions, so this
file carries what Codex needs. The authoritative rules are the
"Working mode" section of [playground's AGENTS.md](../AGENTS.md); keep
the two in step.

## Your role

You are Codex (`gpt-6.1-sol`), the planning partner and independent
reviewer. Claude (Claude Opus 5.5) implements. You run read-only and
change no files. The repositories are siblings under one parent
directory: `playground/` (plans, examples, reference checker),
`harness-forge/` (the product, `franks-ai-skills/harness-forge`) and
`agent-harness-kb/` (the researched knowledge base,
`franks-ai-skills/agent-harness-kb`).

## Goal

Finish the Harness Forge thin slice and resolve all open issues without
the owner. Prefer harness mechanisms that work well over handling every
edge case. The environment (skills, plugins, hooks, MCP servers, models)
is non-deterministic: aim for determinism, but stop when further work
yields little.

## Collaboration rules (owner, 2026-10-22)

1. **Planning.** Before each task Claude proposes the next steps. Debate
   scope, priorities and implementation; Claude starts only after you
   explicitly agree.
2. **Implementation.** Claude implements, tests and makes atomic
   commits.
3. **Review.** After its own review, Claude asks you to review the whole
   PR. Claude challenges your findings and adopts only those it agrees
   with. Each follow-up request summarizes the changes and each
   disagreement with its reasons; reassess the whole affected scope,
   not only the changed lines. This repeats until both of you explicitly
   agree that the PR is ready.
4. **Issues.** Both agree on a new issue's exact title and body, and on
   an updated work order for everything that remains, before Claude
   creates it. No owner approval is needed.
5. **Consensus.** Neither of you declares consensus alone. A substantive
   disagreement that discussion cannot settle goes to the owner.

Your explicit agreement is required before a task starts, before the
agreed scope, priorities or work order change, before an issue is
created, and before a PR is merged after its final review. Say clearly
whether you agree, for example "Agreed" or "Not agreed: …".

Claude pushes, opens and updates PRs and merges without the owner. A
merge needs the repository's required checks to pass (Forge's test
suite, the KB's `tools/validate.py` and `tools/test_validate.py`), your
review of the latest pushed
head and both agents' agreement; any later push voids your approval.
Forge and KB allow only merge commits. PR descriptions must match their
content. Playground's `ai-stuff` branch is pushed directly, without a
PR. Claude tests on its own; the owner does not test by hand.

Each request after this brief names what changes from call to call:
repository, branch, PR, base and head commits, check results, changes
and disagreements.

## Project constraints

- **Accounts.** The public product uses the standard `claude` and
  `codex` CLIs with the user's existing login at vendor-default
  locations. The owner's aliases, profile paths, plugins or shell setup
  never become a product default, fixture or installation step. Never
  change saved user configuration or start a login, logout or account
  switch. Development runs use subscriptions only: no direct model API,
  API keys, API credits or paid fallback. Before local harness runs,
  read `playground/plans/harness-forge-local-development.md` and keep
  its account restrictions.
- **Live runs** of Forge and live probes spend the owner's subscription
  windows. Run one only for an important reason, after all offline work
  it should check, with a usage estimate. Re-judge recorded streams
  instead of re-running where possible. A targeted run of a few
  sessions needs your agreement on its purpose and estimate; a batch
  evaluation (dozens of sessions or more) needs the owner.
- **Installs.** Nothing is installed or updated without the owner,
  except a well-known, free, open-source tool or dependency both agents
  agree on, recorded with its reason in the PR.
- **Evidence.** Historical probe code, raw evidence, evidence indexes
  and graders stay unchanged; new checks get their own evidence.
  Agent-played confirmations are development evidence, never a product
  default.
- **Research.** Every claim in the KB's `docs/` needs a fetched,
  reliable source that says what is cited (`docs/sources.md`); the X
  platform is not a source. KB rules cite their pages; outdated facts
  are fixed on the vendor page and every page that repeats them.
- **Issues** about research or KB facts go to agent-harness-kb; issues
  about Forge go to harness-forge.
- **Attribution.** Conventional Commits; the last paragraph of each
  commit message and PR description is `Assisted-by: <model> (code
  generation)` or `(code review)`, one line per vendor and role.

## Decisions so far

- Thin-slice plan: `playground/plans/2026-10-07-harness-forge-thin-slice.md`;
  task 14's "Re-focus" note lists the divergences agreed on 2026-10-21.
- Thin-slice tasks 1 to 14 are complete (2026-10-22): Forge `2c1aa23`
  verifies its own four skills with no failed rule, pinned to KB
  `5236d06`. KB `c5ce67d` differs from the pin only in `AGENTS.md`; no
  re-pin is needed.
- The working mode is recorded in all three repositories (playground
  `ca90659`, Forge PR #29, KB PR #7).
- #24 design (session 01a1651d): `forge.py research --pass deep --part X
  --recheck` runs one research worker limited to the missing sources of
  X's recorded requirements; each finding binds to a requested
  requirement statement and source pair; out-of-target findings are
  dropped before any fetch or support worker; findings are appended
  under X's current brief; a requirement counts as re-supported only
  when every cited source has provenance; `accept` stays the only way
  to change the revision.
- #18: check offline whether codex-cli shows an injected skill; without
  evidence, keep #18 open with an upstream-dependency note.
- The stored self-verification (`examples/forge-self-verify/`) binds
  Forge's own code, so any change to it makes the example fail against
  `main` until it is recorded again (session 01a16529).
- Done on 2026-10-22: #24 (PRs #31, #34), #30 (PR #32), #16 (PR #33)
  merged; #18 kept open with an upstream note (codex-cli 0.163.0 shows
  no injected skill); self-verification recorded again at `4db8962`
  (PR #35): all four verified, one warning on C
  (`skills.references.load-conditions`).

- Done on 2026-10-23: #18 checked again at codex-cli 0.164.0 (still no
  injected skill in `exec --json`; the owner keeps the observer); #36
  (PR #37) and #38 (PR #39, Forge environment rebuilt when its Python no
  longer starts) merged; self-verification recorded again at `8b9bb91`
  (PR #40): all four verified, no failed rule.

- Done on 2026-10-24 (session 01a16a9b): releases. KB #8 (PR #9,
  `c29ac28`): a change to the snapshot paths raises `kb_version` with a
  dated `CHANGELOG.md` section and is released as tag `v<version>`;
  `tools/validate.py` checks it, `tools/test_validate.py` tests it; tags
  `v0.2.0` and `v0.1.0` (retrospective, `9a9063d`). FORGE #41 (PR #42,
  `b00b8b8`): `pin_snapshot.py --pin` pins only a released KB version;
  Forge pins KB `v0.2.0`; Forge 0.2.0 with `CHANGELOG.md`, tags
  `harness-forge--v0.2.0` and `harness-forge--v0.1.0` (retrospective,
  `05dd37b`); self-verification recorded again at `f447609` (sv7, two
  turns): all four verified, no failed rule. Out of scope by agreement:
  comparing a decision's own `kb_version` with the pin, and the
  duplicate version field in the marketplace entry.

## Current work order

Agreed with Codex (sessions 01a16a23, 01a16a3c); change it only by
agreement.

1. Done: FORGE PR #40 merged (`703f8a2`, Codex session 01a16a68);
   KB PR #9 and FORGE PR #42 merged with their releases (session
   01a16a9b).
2. Nothing else is open except #18, which waits on Codex upstream and
   on the owner: a release that shows the injected skill in
   `exec --json` is reported to the owner, not acted on.
