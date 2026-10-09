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
or contain hostile content. Forge's README and per-run reports must
disclose the gap even when the built artifact is `verified`. See the
[accepted policy](plans/2026-10-09-harness-forge-decisions.md) and
[M1 report](plans/2026-10-07-harness-forge-m1-results.md) for the evidence.
Forge is currently an unpublished sibling checkout; its local README is
at `../harness-forge/README.md`. Public cross-repository links will be
added at distribution. Generic Forge-build provenance is not mandatory
in every generated README; artifact-specific outside controls still are.

## Forge account setup

The public product assumes standard vendor CLIs and the user's existing
login at vendor-default locations. Users should check that it is a
subscription login: an API-key login can cost extra, and Forge asks
before continuing with one. Temporary worker restrictions remain
required; login management and saved-configuration changes are outside Forge.
The owner's custom setup applies only to temporary development on this
machine. All agents must follow the [local development boundary](plans/harness-forge-local-development.md);
historical profile names are evidence labels, not product requirements.

## License

[GNU Affero General Public License v3.0](LICENSE) (AGPL-3.0-only).
