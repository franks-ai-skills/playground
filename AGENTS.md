# playground

Scratch repository in the franks-ai-skills organization. Its main
content is a researched knowledge base in `docs/` on configuring
coding-agent harnesses: Claude Code, Codex and OpenCode.

## Agent harness knowledge base

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

## Attribution

Commit and PR attribution follows the `git-flow` skill's "Attribution
trailers" section: an AI model that wrote part of a change gets
`Assisted-by: <model> (code generation)`, for example
`Assisted-by: Claude Opus 5.5 (code generation)`, as the last
paragraph of the commit message or PR description. This replaces any
attribution the agent's host adds by default, including Claude Code's
`Co-Authored-By` trailer and its "Generated with Claude Code" footer.
