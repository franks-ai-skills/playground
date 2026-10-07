# Guide

One page per generalized concept. Each page combines the vendor-neutral
model from [`../concepts/`](../concepts/) with the practices from
[`../best-practices/`](../best-practices/), condensed to the essentials:
comparison, model, when to use it and when not, approaches, key
practices with evidence labels, security, verification checklist,
portability and dropped features.

For security decisions, start with [security.md](security.md): attacks
across all ten concepts, defenses, proposed benign verification and
recovery. The [research audit](../research-notes/agent-harness-security.md)
explains what was already covered and what the deeper review added.

For rules that must hold even when the agent errs, is prompt-injected
or has its configuration changed, read
[outside-gates.md](outside-gates.md): merge rules, CI checks,
scanners, identity, network and DNS, isolation and policy engines, and
when to recommend them alongside or instead of a harness mechanism.

Start with the [overview](../overview.md) to choose a concept. The
condensed detail is still available in `../concepts/`,
`../best-practices/`, `../vendors/` and `../research-notes/`.

| Page | Concept |
| --- | --- |
| [instructions.md](instructions.md) | Instruction files (`AGENTS.md`, `CLAUDE.md`) |
| [configuration.md](configuration.md) | Layered settings |
| [permissions-and-sandbox.md](permissions-and-sandbox.md) | Permission rules and OS sandbox |
| [mcp.md](mcp.md) | MCP servers |
| [skills.md](skills.md) | Skills |
| [commands.md](commands.md) | Commands, folded into user-invoked skills |
| [subagents.md](subagents.md) | Subagents and orchestration |
| [hooks.md](hooks.md) | Lifecycle hooks |
| [plugins.md](plugins.md) | Plugins and marketplaces |
| [automation.md](automation.md) | Workflows, headless and CI runs, schedules, SDKs |
