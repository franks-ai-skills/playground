# Claude Code

Claude Code is Anthropic's agentic coding harness. It runs as an interactive terminal (and IDE) session, as a headless CLI (`claude -p`), and as a library through the Claude Agent SDK. These pages describe how the harness is configured and extended: persistent instructions, settings, permissions, MCP servers, skills, commands, subagents, hooks, plugins, and automation.

- Version researched: Claude Code 2.1.289 (`claude --version`).
- Research date: 2026-10-04.
- Primary sources: the official docs at `code.claude.com/docs` (raw Markdown pages fetched on 2026-10-04), the [anthropics/claude-code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md), the [Agent Skills specification](https://agentskills.io/specification), and local `--help` output of v2.1.289.

## Mental model

Claude Code assembles a session from layered files, most of which can live at managed (organization), user (`~/.claude/`), project (`.claude/`), and local (`.claude/settings.local.json`, `CLAUDE.local.md`) scope. At startup it loads settings (merged by precedence), the CLAUDE.md files of the working directory and its ancestors plus unscoped `.claude/rules/` files, the first 200 lines or 25KB of the auto memory index, the active output style, and short listings: each skill's name and description, each subagent's description, and each MCP server's instructions and tool names. On demand it loads the rest: nested CLAUDE.md files and path-scoped rules when Claude reads matching files, a skill's full body when it is invoked, MCP tool definitions through the `ToolSearch` tool, memory topic files, and subagents, which run in their own context window and return one report. On events, the harness (not the model) runs hooks at about 30 lifecycle points such as `PreToolUse` or `Stop`, the status line command runs on UI updates, and schedulers (`/loop`, desktop tasks, cloud routines) start prompts on a timer or trigger. Permission rules, permission modes, and the OS-level sandbox decide which tool calls run without a prompt. Plugins package skills, agents, hooks, MCP servers, output styles, and workflows for distribution through marketplaces.

## Pages

| Page | Contents |
| :- | :- |
| [instructions.md](instructions.md) | CLAUDE.md hierarchy, `@` imports, CLAUDE.local.md, `.claude/rules/` path-scoped rules, auto memory, AGENTS.md support |
| [configuration.md](configuration.md) | settings.json scopes, precedence and merge rules, important keys, workspace trust, models and effort, output styles, status line, environment variables |
| [permissions-and-sandbox.md](permissions-and-sandbox.md) | Permission rule syntax and evaluation order, permission modes, protected paths, managed policy, OS-level sandbox |
| [mcp.md](mcp.md) | MCP server scopes, transports, `claude mcp` commands, tool naming, tool search, output limits, managed MCP |
| [skills.md](skills.md) | SKILL.md format and all frontmatter fields, locations, discovery, invocation, context cost, relation to the agentskills.io spec |
| [commands.md](commands.md) | Built-in commands vs bundled skills vs custom commands, `.claude/commands/`, arguments |
| [subagents.md](subagents.md) | Subagents, built-in agents, the Agent tool, context isolation, nesting and concurrency, forks, agent teams, background agents |
| [hooks.md](hooks.md) | Hook events, handler types, matchers, input/output JSON, exit codes, configuration locations, security |
| [plugins.md](plugins.md) | Plugin layout and components, plugin.json, marketplace.json, install scopes, path variables, versioning, mods |
| [automation.md](automation.md) | Headless mode, Agent SDK, GitHub Actions, scheduling (`/loop`, desktop tasks, routines), dynamic workflows, worktrees, plan mode, checkpoints |
