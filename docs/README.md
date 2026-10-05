# Agent harness knowledge base

How to configure and extend an agent harness: the program around a
model that loads instructions, exposes tools, enforces permissions,
runs subagents and hooks, and automates workflows. It covers Claude
Code, OpenAI Codex and OpenCode as of 2026-10-04.

Start with the [overview](overview.md): every concept on one page,
with what it is used for, how and when to use it, and when not to.

The [security research](research-notes/agent-harness-security.md), dated
2026-10-05, audits the existing security coverage and extends it with
attacks across concepts, defensive controls and proposed canary checks.
Use the [security guide](guide/security.md) to apply the findings across
the concepts; the proposed adversarial checks have not yet been run.

## Layout

| Directory | Content |
| --- | --- |
| [`overview.md`](overview.md) | Entry point: all concepts at a glance, with when to use each and when to use something else. |
| [`guide/`](guide/) | One condensed page per concept, combining the generalized model and the best practices. |
| [`best-practices/`](best-practices/) | How to apply each generalized concept: approaches, implementation in Claude Code and Codex, security, verification and a review checklist, with an evidence label on every practice. |
| [`concepts/`](concepts/) | Vendor-neutral version of each concept: a comparison across harnesses, a generalized model, portability guidance and what was dropped. |
| [`vendors/`](vendors/) | One reference section per harness. Every section has the same set of pages, so a concept can be compared by opening the same file name in each. |
| [`sources.md`](sources.md) | Source policy: rules for citing sources, and the trusted and rejected domains. |
| [`research-notes/`](research-notes/) | The raw research notes behind the pages, with a source for each claim. |

## Vendor references

| Page | [Claude Code](vendors/claude-code/) | [Codex](vendors/codex/) | [OpenCode](vendors/opencode/) |
| --- | --- | --- | --- |
| Overview | [README](vendors/claude-code/README.md) | [README](vendors/codex/README.md) | [README](vendors/opencode/README.md) |
| Instructions | [instructions](vendors/claude-code/instructions.md) | [instructions](vendors/codex/instructions.md) | [instructions](vendors/opencode/instructions.md) |
| Configuration | [configuration](vendors/claude-code/configuration.md) | [configuration](vendors/codex/configuration.md) | [configuration](vendors/opencode/configuration.md) |
| Permissions and sandbox | [permissions-and-sandbox](vendors/claude-code/permissions-and-sandbox.md) | [permissions-and-sandbox](vendors/codex/permissions-and-sandbox.md) | [permissions-and-sandbox](vendors/opencode/permissions-and-sandbox.md) |
| MCP | [mcp](vendors/claude-code/mcp.md) | [mcp](vendors/codex/mcp.md) | [mcp](vendors/opencode/mcp.md) |
| Skills | [skills](vendors/claude-code/skills.md) | [skills](vendors/codex/skills.md) | [skills](vendors/opencode/skills.md) |
| Commands | [commands](vendors/claude-code/commands.md) | [commands](vendors/codex/commands.md) | [commands](vendors/opencode/commands.md) |
| Subagents | [subagents](vendors/claude-code/subagents.md) | [subagents](vendors/codex/subagents.md) | [subagents](vendors/opencode/subagents.md) |
| Hooks | [hooks](vendors/claude-code/hooks.md) | [hooks](vendors/codex/hooks.md) | [hooks](vendors/opencode/hooks.md) |
| Plugins | [plugins](vendors/claude-code/plugins.md) | [plugins](vendors/codex/plugins.md) | [plugins](vendors/opencode/plugins.md) |
| Automation | [automation](vendors/claude-code/automation.md) | [automation](vendors/codex/automation.md) | [automation](vendors/opencode/automation.md) |

## Versions researched

| Harness | Version | Notes |
| --- | --- | --- |
| Claude Code | 2.1.289 | Installed locally. |
| Codex CLI | 0.159.2 | Installed locally; 0.160.0 was the latest release. |
| OpenCode | 1.18.34 | Not installed; researched from docs and source at commit `907b3bc`. |

These harnesses change every few weeks. Check a page's sources and the
vendor changelog before relying on a detail that may have moved.

## Naming rule

No page in this knowledge base is named `agents.md` or `claude.md`.
On a case-insensitive file system (the macOS default), the harnesses
would load such a page as an `AGENTS.md` or `CLAUDE.md` instruction
file. Subagent pages are therefore named `subagents.md`.
