# playground

Scratch repository in the franks-ai-skills organization. It holds the
Harness Forge specs and plans. The researched knowledge base on
configuring coding-agent harnesses (Claude Code, Codex and OpenCode)
lives in its own repository, agent-harness-kb.

## Agent harness knowledge base

- The knowledge base is the sibling checkout `../agent-harness-kb`,
  published at <https://github.com/franks-ai-skills/agent-harness-kb>.
  Read its pages and make every correction there, under its
  `AGENTS.md`: its source policy `docs/sources.md` and its propagation
  rules. Without the sibling checkout, read the public repository and
  say so.
- Playground's copy of the research was removed after the KB was
  published on 2026-10-16.
- Paths below such as `docs/overview.md` refer to the KB checkout.
- For any question or change about an agent harness (instruction
  files, settings, permissions, sandbox, MCP, skills, slash commands,
  subagents, hooks, plugins, headless or CI runs), load the
  `agent-harness` skill first. It maps each question to the page to
  read. Without skill support, start at `docs/overview.md`.
- The knowledge base reflects 2026-10-04 (Claude Code 2.1.289,
  codex-cli 0.159.2, OpenCode 1.18.34). Confirm version-sensitive
  details against the source a page cites before relying on them.
- Every claim in `docs/` needs a reliable source that was fetched and
  says what is cited. A claim that cannot be verified is dropped, not
  marked unverified, and the X platform is not a source. Before adding,
  changing or citing a source, and in every research or writing brief
  for a subagent, apply `docs/sources.md`: the full rules plus the
  trusted and rejected domains.
- When a fact in `docs/` turns out outdated, fix the vendor page with
  its new source, then every page that repeats it: `docs/concepts/`,
  `docs/best-practices/`, `docs/guide/` and `docs/overview.md`.

## Working mode: Claude and Codex (owner, 2026-10-22)

These rules apply to playground, harness-forge and agent-harness-kb.
They override every older rule that asks the owner to approve a push,
a merge or an issue text, including the defaults of the `git-flow`
skill and earlier plan notes. Where an older rule conflicts with them,
these rules win.

**Goal.** Finish the Harness Forge thin slice and resolve all open
issues on your own. Prefer harness mechanisms that work well over
handling every edge case. Skills, plugins, hooks and MCP servers make
the environment non-deterministic: aim for determinism, but stop when
further work yields little.

**Roles.** Claude implements. Codex plans with Claude and reviews; it
changes no files. From 2026-10-27 until the owner says otherwise, Codex
is `gpt-6.1-terra` on high reasoning effort, and every call names both
explicitly instead of relying on `~/.codex/config.toml`:
`codex exec -m gpt-6.1-terra -c model_reasoning_effort="high" -s read-only`.
Earlier calls used `gpt-6.1-sol`. Every Codex call starts with
[the Codex brief](plans/claude-codex-collaboration.md): Codex cannot
read Claude's memory, so the brief carries these rules, the project
constraints, the decisions taken so far and the current work order.

1. **Planning.** Before each task, Claude proposes the next steps to
   Codex. They debate scope, priorities and implementation until Codex
   explicitly agrees. Only then does Claude start.
2. **Implementation.** Claude implements the agreed work, tests it and
   makes atomic commits.
3. **Review.** Claude reviews its own work first, then asks Codex for an
   independent review of the whole PR. Claude challenges each finding
   and adopts only those it agrees with. Each follow-up request includes
   a summary of the changes, each disagreement with its reasons, and a
   request to reassess the whole affected scope. This repeats until both
   explicitly agree that the PR is ready.
4. **Issues.** When either agent proposes an issue, both agree on its
   exact title and body before Claude creates it, together with an
   updated work order for all remaining tasks and issues. The owner's
   approval is not needed.
5. **Consensus.** Neither agent declares consensus alone. When
   discussion cannot settle a substantive disagreement, Claude takes
   that one decision to the owner and continues with other work.

Codex's explicit agreement is required before starting a task, before
changing agreed scope or priorities, before creating an issue, before
changing the work order, and before merging a PR after its final
review.

**Pushes, PRs and merges.** Claude pushes branches, creates and updates
PRs and merges without asking the owner. A merge requires the
repository's required checks to pass (Forge's test suite, the KB's
`tools/validate.py` and `tools/test_validate.py`), a Codex review of
the latest pushed PR head, and both agents' explicit agreement that the
PR is ready. Any push after Codex's
approval voids it and needs a new review. Respect branch protection and
each repository's merge method: harness-forge and agent-harness-kb
allow only merge commits. Keep each PR description in step with what
the PR contains. Playground's `ai-stuff` branch is pushed directly,
without a PR.

**Unchanged.** The security, subscription, account, evidence and
attribution rules in this file and in each repository's `AGENTS.md`
stay in force; read
[the local development note](plans/harness-forge-local-development.md)
before local harness runs. Claude tests on its own and does not ask the
owner to test by hand. Live model runs and probes spend the owner's
subscription windows: run one only for an important reason, after the
offline work it should check, with a usage estimate. A targeted run of
a few sessions needs Codex's agreement on its purpose and estimate; a
batch evaluation (dozens of sessions or more) needs the owner. Nothing
is installed or updated without the owner, except a well-known, free,
open-source tool or dependency both agents agree on, recorded with its
reason in the PR. Each step, round and ruling goes into the progress ledger
`.superpowers/sdd/2026-10-07-harness-forge-thin-slice/progress.md`
(local, not tracked).

## Repository layout rules

- This file is the only instruction file. Claude Code reads
  `AGENTS.md` only while no `CLAUDE.md` exists, so instructions for any
  harness go here.
- Skills live in `.agents/skills/<name>/` (read by Codex and
  OpenCode), each with a relative symlink at `.claude/skills/<name>`
  (read by Claude Code).
- Name subagent material `subagents.md`. Files named `agents.md` or
  `claude.md` load as instruction files on case-insensitive file
  systems.

## Harness Forge account boundary

For this and every subsequent agent: the public product assumes standard
`claude` and `codex` CLIs, vendor-default account locations and the user's
existing login. Forge asks before continuing with an API-key or unknown
login type, because it can cost extra. Never make the owner's aliases, profile paths, plugins
or shell configuration a product default, dependency or installation step.
Keep temporary worker restrictions; do not change saved user configuration
or initiate login, logout or account switching. The owner's development
runs are subscription-only: no direct model API, additional API
keys/credits or paid fallback.

The owner's configuration is a temporary exception for development on
this machine only. Read [the local development note](plans/harness-forge-local-development.md)
before local harness runs. Historical diagnostics describe observations,
not public defaults. Keep their raw evidence and graders unchanged.

## Attribution

Commit and PR attribution follows the `git-flow` skill's "Attribution
trailers" section: an AI model that wrote part of a change gets
`Assisted-by: <model> (code generation)`, for example
`Assisted-by: Claude Opus 5.5 (code generation)`, as the last
paragraph of the commit message or PR description. This replaces any
attribution the agent's host adds by default, including Claude Code's
`Co-Authored-By` trailer and its "Generated with Claude Code" footer.
