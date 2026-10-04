# OpenCode

OpenCode is an AI coding agent harness. It ships a terminal UI (TUI), a CLI, an HTTP server with an OpenAPI 3.1 spec, a JavaScript SDK, and a GitHub Action. The TUI is itself a client of the server ([Server](https://opencode.ai/docs/server/)). These pages describe how OpenCode is configured and extended: instructions, config files, permissions, MCP, skills, commands, agents, hooks, plugins, and automation.

## Research basis

| Item | Value |
| --- | --- |
| Repository | [github.com/anomalyco/opencode](https://github.com/anomalyco/opencode). The old `sst/opencode` URL redirects there ([README](https://github.com/anomalyco/opencode/blob/dev/README.md)). |
| Version researched | v1.18.34, released 2026-09-30 ([Releases](https://github.com/anomalyco/opencode/releases)) |
| Source commit | `907b3bc` (2026-10-02), `packages/opencode/package.json` version `1.18.34` |
| Research date | 2026-10-04 |
| Installed locally | No. Findings come from the official docs at opencode.ai/docs (source in `packages/web/src/content/docs/*.mdx`), a shallow clone of the repo, and GitHub release notes. |
| Source branch | Source links point to `dev`, the branch the docs link to. Source-derived claims describe behavior at commit `907b3bc`. |
| Plugin package | `@opencode-ai/plugin` 1.18.34, exports `.`, `./tool`, `./tui`, `./v2/effect`, `./v2/promise` ([SRC packages/plugin/package.json](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/package.json)) |

OpenCode releases every few days (v1.17.0 on 2026-06-10, v1.18.0 on 2026-07-14, v1.18.34 on 2026-09-30). Details on these pages can change within weeks. Pin a version when you depend on specific behavior.

## Mental model

At startup, OpenCode merges up to eight config layers (remote org defaults, global, `OPENCODE_CONFIG`, project files walked up to the git worktree, `.opencode` directories, `OPENCODE_CONFIG_CONTENT`, managed files, macOS MDM) into one config ([configuration](configuration.md)). It then loads the markdown agents, commands, and legacy modes, and the local and npm plugins it finds in the config directories, installing npm plugins and config-dir `package.json` dependencies with Bun ([plugins](plugins.md)). When it builds the system prompt, it injects the winning `AGENTS.md` (or `CLAUDE.md`) files, the `instructions` entries (URLs are re-fetched on every build), MCP server instructions, and references that have a description ([instructions](instructions.md)). The tool list carries every enabled tool and MCP tool (MCP tools cost context), and the `skill` tool's description lists the name and description of every visible skill ([mcp](mcp.md), [skills](skills.md)). On demand, the model loads a skill's full body through the `skill` tool and starts subagents through the `task` tool ([agents](subagents.md)); the user runs `/name` commands ([commands](commands.md)); and reading a file attaches any nested `AGENTS.md` between that file and the project root. On events, plugin hooks run in sequence: `tool.execute.before/after`, `permission.ask`, `chat.*`, `shell.env`, and the `event` hook, which receives bus events such as `session.idle` or `file.edited` ([hooks](hooks.md)). Configured formatters run after each write or edit, and configured LSP servers feed diagnostics back to the agent. Every tool call passes through the `permission` rules, which map each tool to `allow`, `ask`, or `deny` ([permissions-and-sandbox](permissions-and-sandbox.md)).

## Pages

| Page | Content |
| --- | --- |
| [instructions.md](instructions.md) | `AGENTS.md` / `CLAUDE.md` / `CONTEXT.md` lookup and precedence, the `instructions` config key, lazy nested `AGENTS.md`, `/init`. |
| [configuration.md](configuration.md) | `opencode.json[c]` and `tui.json[c]`, all config layers and merge rules, variable substitution, all top-level keys, providers and models, themes, keybinds, server, references, env vars. |
| [permissions-and-sandbox.md](permissions-and-sandbox.md) | `permission` keys, patterns, defaults, per-agent overrides, `--auto`, legacy `tools` map, and what the notes say about OS-level sandboxing. |
| [mcp.md](mcp.md) | Local and remote MCP servers, config fields, OAuth, CLI, tool naming and gating. |
| [skills.md](skills.md) | `SKILL.md` support, discovery paths including `.claude/skills` and `.agents/skills`, `skills.paths` / `skills.urls`, the `skill` tool, `permission.skill`. |
| [commands.md](commands.md) | Custom slash commands, template syntax, options, built-in commands, MCP prompts and skills as commands. |
| [subagents.md](subagents.md) | Primary agents and subagents, built-in agents, markdown and JSON definitions, all options, the `task` tool, `permission.task`, `subagent_depth`. |
| [hooks.md](hooks.md) | Event and hook mechanisms, which in OpenCode come through plugins: the hook interface and the bus event list. |
| [plugins.md](plugins.md) | Plugin locations, npm plugins, plugin API v1 and V2, custom tools via `tool()`, TUI plugins, LSP servers and formatters. |
| [automation.md](automation.md) | `opencode run`, `opencode serve` and the SDK, the GitHub Action, sharing. |

## Sources

- https://opencode.ai/docs/server/
- https://opencode.ai/docs/github/
- https://github.com/anomalyco/opencode/blob/dev/README.md
- https://github.com/anomalyco/opencode/releases
- https://github.com/anomalyco/opencode/blob/dev/packages/plugin/package.json
