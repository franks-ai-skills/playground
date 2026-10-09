# playground

A scratch repository for trying things out in the
[franks-ai-skills](https://github.com/franks-ai-skills) organization.

## Content

- [`docs/`](docs/README.md): a knowledge base on configuring coding-agent
  harnesses (Claude Code, Codex, OpenCode). Start with the
  [overview](docs/overview.md); behind it are a condensed guide per
  concept, the full concept and best-practice pages, and a reference
  per harness.
- [`AGENTS.md`](AGENTS.md) and the `agent-harness` skill in
  [`.agents/skills/`](.agents/skills/agent-harness/SKILL.md) make the
  knowledge base available to agents working in this repository.
  `.claude/skills/` holds a symlink to the same skill for Claude Code.

## Harness Forge worker isolation gap

The [Harness Forge design](specs/2026-10-06-harness-forge-design.md) and
[implementation plan](plans/2026-10-07-harness-forge-thin-slice.md) live here.
On 2026-10-09 the owner accepted automated workers in Claude Code and
Codex with weaker isolation (`best-effort-v1`). Available restrictions
will be used, but complete tool absence and prevention of unauthorized
file/context/network access are not guaranteed. Functional live support
is still being implemented; the diagnostics did not certify containment.

Use this mode for trusted projects, and do not rely on it to hide secrets
or contain hostile content. Reports and generated-result READMEs must
disclose the gap even when the built artifact is `verified`. See the
[accepted policy](plans/2026-10-09-harness-forge-decisions.md) and the
sibling [Forge README](../harness-forge/README.md) for the per-harness evidence.

## License

[GNU Affero General Public License v3.0](LICENSE) (AGPL-3.0-only).
