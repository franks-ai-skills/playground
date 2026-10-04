# OpenAI Codex

Codex is OpenAI's coding agent. This section describes how its agent harness is configured and extended: instructions, configuration, permissions, MCP, skills, commands, subagents, hooks, plugins and automation.

## Surfaces

| Surface | What it is | Shares local config? |
|---|---|---|
| Codex CLI (`codex`) | Terminal UI (TUI) plus subcommands such as `codex exec`, `codex review`, `codex mcp`, `codex plugin`, `codex cloud` | Yes: `~/.codex/config.toml` and project `.codex/config.toml` ([Config basics](https://developers.openai.com/codex/config-basic)) |
| IDE extension | Codex inside the editor, with its own slash-command page and a background-agent panel | Yes: the CLI and IDE extension share the same config layers ([Config basics](https://developers.openai.com/codex/config-basic)). It does not support plugins ([Plugins](https://developers.openai.com/codex/plugins)) |
| Desktop app | Codex in the "ChatGPT desktop app"; adds worktrees with Handoff, scheduled tasks and its own notification settings | Yes: one TOML config system covers the CLI, IDE extension and Codex in the ChatGPT desktop app. MCP config is shared by all three ([MCP](https://developers.openai.com/codex/mcp)) |
| Codex Cloud | Tasks that run in published cloud environments, each with its own workspace; also backs GitHub code review (`@codex review`) | The notes do not say that cloud tasks read local `config.toml`. Cloud environments carry their own repos, tools, network and secrets ([Codex Cloud](https://learn.chatgpt.com/docs/cloud.md)) |

Codex is now presented as part of "ChatGPT". ChatGPT Work shares skills and plugins with Codex. These pages cover only the local Codex harness (CLI, IDE extension, desktop app) and Codex Cloud.

## Version researched

- Researched on 2026-10-04.
- Locally installed: `codex-cli 0.159.2` (Homebrew cask).
- Latest stable release on that date: `0.160.0` (`rust-v0.160.0`, published 2026-10-01). The changelog also lists 0.159.3. Versions 0.161 and 0.162 existed only as alphas ([openai/codex releases](https://github.com/openai/codex/releases), [rust-v0.160.0](https://github.com/openai/codex/releases/tag/rust-v0.160.0), [Changelog](https://developers.openai.com/codex/changelog)).
- Facts marked "local CLI" come from read-only inspection of the 0.159.2 install (`codex --help` and subcommand help, `codex features list`, `~/.codex/skills/.system`, `strings` on the binary). Facts from the `openai/codex` `main` branch may run ahead of 0.159.2.

## Documentation location

The Codex docs moved. `https://developers.openai.com/codex/codex-manual.md` now answers HTTP 308 and redirects to `https://learn.chatgpt.com/docs/codex-manual.md`. Codex docs live under `learn.chatgpt.com/docs/...`, and the plugin-builder docs stay under `developers.openai.com/plugins/...`. The manual is one file of about 2.9 MB that combines every page; each section starts with its own `Source:` URL. The page index is [learn.chatgpt.com/llms.txt](https://learn.chatgpt.com/llms.txt).

The research notes cite both hosts. Pages fetched from `developers.openai.com/codex/...` and from `learn.chatgpt.com/docs/...` are cited with the URL that was fetched. Both refer to the same documentation set.

## Mental model

At startup Codex resolves one configuration from layered `config.toml` files (built-ins, system, cloud-managed defaults, user, `--profile` file, trusted project `.codex/` folders, CLI flags), checks the result against admin `requirements.toml` constraints, and loads the hooks, Starlark rules and MCP servers defined next to those layers; untrusted projects skip their `.codex/` layers. Also at startup it builds the instruction chain from `AGENTS.md` files (global, then project root down to the current directory) and puts it into the first turn, and it adds a bounded skill catalog of name, description and path for every discovered skill, including skills from enabled plugins, which load from a local cache. On demand, Codex reads a skill's full `SKILL.md` when the user names it with `$skill-name` or `/skills` or when the task matches its description, spawns subagents when the user or an `AGENTS.md`/skill instruction asks for them (each custom agent TOML file is applied as a config layer for the spawned session), and calls MCP tools as the model needs them. On events, lifecycle hooks run (for example `SessionStart`, `PreToolUse`, `Stop`), the `notify` program runs on `agent-turn-complete`, the TUI emits terminal notifications, and outside an interactive session `codex exec`, the SDKs, the GitHub Action, `@codex review` and desktop-app scheduled tasks start runs.

## Pages

| Page | Contents |
|---|---|
| [instructions.md](instructions.md) | `AGENTS.md` discovery, override files, fallback filenames, size limit, combination order, `## Code Review Rules` |
| [configuration.md](configuration.md) | `config.toml` scopes and precedence, `-c` overrides, project trust, file-based profiles, important keys, managed config and `requirements.toml`, models and custom providers, feature flags |
| [permissions-and-sandbox.md](permissions-and-sandbox.md) | Approval policies (current and retired), sandbox modes, permission profiles (beta), platform sandboxes, network proxy, Starlark execpolicy rules |
| [mcp.md](mcp.md) | MCP client config, stdio and streamable HTTP, `codex mcp` commands, tool allow/deny lists, timeouts, OAuth, removal of `codex mcp-server` |
| [skills.md](skills.md) | `SKILL.md` fields Codex reads, `agents/openai.yaml`, locations, discovery and invocation, catalog budget, system skills, relation to agentskills.io |
| [commands.md](commands.md) | Built-in slash commands; deprecated custom prompts (`~/.codex/prompts`) |
| [subagents.md](subagents.md) | Subagents: spawn tools, built-in agent types, custom agent TOML files, `[agents]` config, cloud best-of-N |
| [hooks.md](hooks.md) | Lifecycle hooks (events, handlers, locations, I/O, trust, async and managed hooks), `notify`, TUI notifications |
| [plugins.md](plugins.md) | Plugins and marketplaces: manifest, marketplace file, CLI commands, cache, enablement, apps/connectors |
| [automation.md](automation.md) | `codex exec`, `codex review`, SDKs, app-server, GitHub Action, cloud tasks, scheduled tasks, worktrees |

## Sources

- https://github.com/openai/codex/releases
- https://github.com/openai/codex/releases/tag/rust-v0.160.0
- https://developers.openai.com/codex/changelog
- https://developers.openai.com/codex/config-basic
- https://developers.openai.com/codex/plugins
- https://developers.openai.com/codex/mcp
- https://learn.chatgpt.com/docs/cloud.md
- https://learn.chatgpt.com/docs/codex-manual.md
- https://learn.chatgpt.com/llms.txt
