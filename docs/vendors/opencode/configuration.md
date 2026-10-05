# Configuration

OpenCode uses two config files: `opencode.json[c]` for the server and runtime, and `tui.json[c]` for the terminal UI. Config comes from up to eight layers (org, global, project, managed) that are deep-merged, so a project or an admin can override single keys without copying the whole file. Config also selects providers and models, defines agents, commands, MCP servers, permissions, and plugins, and configures the HTTP server.

## Locations and scopes

### Layers

Later layers override earlier ones on conflicting keys ([Config – Precedence](https://opencode.ai/docs/config/)).

| # | Layer | Location | Notes |
| --- | --- | --- | --- |
| 1 | Remote org config | `.well-known/opencode`, fetched when you authenticate with a provider that supports it | Organizational defaults. Response shape is `{ config?, remote_config? }` ([SRC core/src/v1/config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)). |
| 2 | Global | `~/.config/opencode/opencode.json` | Source reads `config.json`, then `opencode.json`, then `opencode.jsonc` from the global config dir. A legacy TOML `config` file is migrated ([SRC config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts)). |
| 3 | Custom file | Path in `OPENCODE_CONFIG` | |
| 4 | Project | `opencode.json` / `opencode.jsonc` | Found by walking up from the cwd to the git worktree root. Merged from outermost to innermost, so the closest file wins ([SRC config/paths.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/paths.ts); [Config](https://opencode.ai/docs/config/)). |
| 5 | `.opencode` directories | See "Config directories" below | Agents, commands, plugins, and a nested `opencode.json[c]`. |
| 6 | Inline | JSON in `OPENCODE_CONFIG_CONTENT` | |
| 6a | OpenCode Console org | `<console-url>/api/config` | Source only: merged after `OPENCODE_CONFIG_CONTENT` when you are logged into a Console account with an active org ([SRC config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts)). |
| 7 | Managed files | `/Library/Application Support/opencode/` (macOS), `/etc/opencode/` (Linux), `%ProgramData%\opencode` (Windows) | Writing requires admin rights. |
| 8 | macOS managed preferences | `.mobileconfig` via MDM, preference domain `ai.opencode.managed` | Highest priority; users cannot override it. Plist keys map 1:1 to `opencode.json` fields; `Payload*` metadata keys are stripped ([Config – Managed settings](https://opencode.ai/docs/config/)). |

`opencode debug config` prints the resolved config ([Config – Managed settings](https://opencode.ai/docs/config/)).

### Config directories

Scanned in this order ([SRC config/paths.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/paths.ts), [SRC config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts)):

1. `~/.config/opencode`
2. Every `.opencode` dir from the cwd up to the worktree
3. `~/.opencode`
4. `OPENCODE_CONFIG_DIR`

In each directory, a `.opencode/opencode.json[c]` is merged, then the directory's `commands/`, `agents/`, `modes/`, and `plugins/` are loaded. `OPENCODE_CONFIG_DIR` is searched like `.opencode` and loaded after the global config and `.opencode` dirs, so it can override them ([Config](https://opencode.ai/docs/config/)).

Subdirectory names are plural: `agents/`, `commands/`, `modes/`, `plugins/`, `skills/`, `tools/`, `themes/`. Singular names still work for backwards compatibility ([Config](https://opencode.ai/docs/config/)).

`OPENCODE_DISABLE_PROJECT_CONFIG` skips project `opencode.json`, project `.opencode` dirs, and the project `AGENTS.md` lookup ([SRC config/paths.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/paths.ts), [SRC session/instruction.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts)).

### TUI config

| Scope | Location |
| --- | --- |
| Global | `~/.config/opencode/tui.json` |
| Project | Next to `opencode.json` |
| Custom | Path in `OPENCODE_TUI_CONFIG` |

Sources: [TUI](https://opencode.ai/docs/tui/); [Config](https://opencode.ai/docs/config/); [SRC config/tui.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/tui.ts).

### Themes

Custom themes are JSON files, loaded in this order: built-in themes, `~/.config/opencode/themes/*.json`, `<project-root>/.opencode/themes/*.json`, `./.opencode/themes/*.json` ([Themes](https://opencode.ai/docs/themes/)).

### Merge semantics

- Configs are merged with remeda `mergeDeep`: objects merge deeply and later sources win per key ([SRC config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts)).
- `instructions` arrays are concatenated across sources and deduplicated (same source).
- `plugin` entries are deduped by plugin identity, and their origin (global or local) is tracked. Path-like plugin specs resolve relative to the config file that declared them (same source).
- Markdown agents merge over JSON-defined agents from earlier layers ([SRC config/agent.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/agent.ts)).

## Format

JSON and JSONC (JSON with comments) are both supported. Schemas: `https://opencode.ai/config.json` for `opencode.json[c]`, `https://opencode.ai/tui.json` for `tui.json[c]` ([Config](https://opencode.ai/docs/config/)).

### Top-level `opencode.json` keys

From the schema source ([SRC core/src/v1/config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts); [Config](https://opencode.ai/docs/config/)).

| Key | Meaning | Default / notes | Page |
| --- | --- | --- | --- |
| `$schema` | JSON schema reference for validation. | | |
| `shell` | Default shell for the terminal and the bash tool. | | |
| `logLevel` | `DEBUG`, `INFO`, `WARN`, or `ERROR`. | | |
| `server` | Settings for `opencode serve` / `opencode web`: `port`, `hostname`, `mdns`, `mdnsDomain`, `cors`. | `mdnsDomain` default `opencode.local` | [automation](automation.md) |
| `command` | Custom commands. | | [commands](commands.md) |
| `skills` | `{ paths?: string[], urls?: string[] }`: extra skill folders and skill URLs. | | [skills](skills.md) |
| `references` | Named git or local directory references. | | See [References](#references) |
| `reference` | Deprecated; use `references`. | Deprecated in v1.17.1 | |
| `watcher.ignore` | Glob patterns the file watcher ignores. | | |
| `snapshot` | Internal-git snapshots that make undo/revert possible. | `true` | |
| `plugin` | Array of `string` or `[string, options]`. | | [plugins](plugins.md) |
| `share` | `manual`, `auto`, or `disabled`. | `manual` | [automation](automation.md) |
| `autoshare` | Deprecated; use `share`. | | |
| `autoupdate` | `true`, `false`, or `"notify"`. | | |
| `disabled_providers` | Provider deny list. | Wins over `enabled_providers` when both name a provider. | |
| `enabled_providers` | Provider allow list. | | |
| `model` | Main model, format `provider/model`. | | |
| `small_model` | Model for light tasks such as title generation, format `provider/model`. | OpenCode tries a cheaper model from the same provider. | |
| `default_agent` | Default primary agent. | Must be a primary agent; otherwise falls back to `build` with a warning. | [agents](subagents.md) |
| `subagent_depth` | Non-negative integer; how deep subagents can nest. | `1` | [agents](subagents.md) |
| `username` | Name shown in conversations instead of the system username. | | |
| `mode` | Deprecated; use `agent`. | | [agents](subagents.md) |
| `agent` | Agent definitions, including the built-in keys `plan`, `build`, `general`, `explore`, `title`, `summary`, `compaction`. | | [agents](subagents.md) |
| `provider` | Custom provider configs and model overrides. | | See [Providers and models](#providers-and-models) |
| `mcp` | MCP server definitions. | | [mcp](mcp.md) |
| `formatter` | Omit or `false` disables; `true` enables the built-ins; an object enables the built-ins with overrides. | Disabled | [plugins](plugins.md#formatters) |
| `lsp` | Same semantics as `formatter`. | Disabled | [plugins](plugins.md#lsp) |
| `instructions` | Extra instruction files, globs, or URLs. | | [instructions](instructions.md) |
| `layout` | Deprecated; the stretch layout is always used. | | |
| `permission` | Permission rules. | | [permissions-and-sandbox](permissions-and-sandbox.md) |
| `tools` | Deprecated boolean map; use `permission`. | | [permissions-and-sandbox](permissions-and-sandbox.md) |
| `attachment.image` | `auto_resize`, `max_width`, `max_height`, `max_base64_bytes`. | | |
| `enterprise.url` | Enterprise URL. | | |
| `tool_output` | `max_lines`, `max_bytes`. Larger output is truncated and saved to disk. | `max_lines` 2000, `max_bytes` 51200 | |
| `compaction` | `auto`, `prune`, `tail_turns`, `preserve_recent_tokens`, `reserved`. | `auto` `true`, `prune` `false` | |
| `experimental` | `disable_paste_summary`, `batch_tool`, `openTelemetry`, `primary_tools`, `continue_loop_on_deny`, `mcp_timeout`, `policies`. | | See below |

### `experimental` keys described in the notes

| Key | Meaning | Source |
| --- | --- | --- |
| `batch_tool` | Enables a batch tool. | [SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts) |
| `primary_tools` | Tools available only to primary agents. | same |
| `continue_loop_on_deny` | Keeps the agent loop running after a denied tool call. | same |
| `mcp_timeout` | MCP request timeout. | same |
| `policies` | Entries like `{effect:"deny", action:"provider.use", resource:"openai"}`. | [Config – Policies](https://opencode.ai/docs/config/) |
| `disable_paste_summary`, `openTelemetry` | Listed in the schema; the notes give no description. | [SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts) |

### Variable substitution

| Syntax | Effect |
| --- | --- |
| `{env:VAR}` | Substitutes an environment variable. An unset variable becomes an empty string. |
| `{file:path}` | Substitutes a file's contents. The path is relative to the config file's directory, or absolute when it starts with `/` or `~`. |

Typical uses are API keys, prompt files (for example `"prompt": "{file:./prompts/build.txt}"`), and shared snippets ([Config – Variables](https://opencode.ai/docs/config/)).

### Providers and models

- Model IDs use the `provider/model-id` format ([Config – Models](https://opencode.ai/docs/config/)).
- `opencode auth login` stores credentials in `~/.local/share/opencode/auth.json`. Providers come from Models.dev. Env vars and a project `.env` are also read. `opencode models [provider] [--refresh] [--verbose]` lists models ([CLI](https://opencode.ai/docs/cli/)).

Provider `options` ([Config](https://opencode.ai/docs/config/)):

| Option | Meaning | Default |
| --- | --- | --- |
| `timeout` | Timeout; `false` disables it. | 300000 ms |
| `headerTimeout` | Header timeout. | 300000 ms |
| `chunkTimeout` | Chunk timeout; `false` disables it. | 300000 ms |
| `setCacheKey` | Listed without description in the notes. | |
| `apiKey` | API key. | |
| `baseURL` | Base URL. | |
| `region`, `profile`, `endpoint` | Bedrock-specific. | |

### `tui.json[c]` keys

([TUI](https://opencode.ai/docs/tui/); [Keybinds](https://opencode.ai/docs/keybinds/); [SRC config/tui.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/tui.ts))

| Key | Meaning | Default |
| --- | --- | --- |
| `theme` | Theme name. | |
| `keybinds` | Merged with the built-in defaults. `"none"` unbinds a key. | `leader` is `ctrl+x` |
| `leader_timeout` | Leader key timeout. | 2000 |
| `scroll_speed` | Scroll speed. | |
| `scroll_acceleration.enabled` | Scroll acceleration. | |
| `diff_style` | `auto` or `stacked`. | |
| `cursor.style`, `cursor.blinking` | Cursor appearance. | |
| `mouse` | Mouse setting (no description in the notes). | |
| `attention` | `enabled`, `notifications`, `sound`, `volume`, `sound_pack`, `sounds`. | `enabled` `false` |
| `plugin` | TUI plugin specs. | See [plugins](plugins.md#tui-plugins) |

Theme colors can be hex, ANSI 0–255, references to `defs`, `{dark, light}` variants, or `"none"` for the terminal default ([Themes](https://opencode.ai/docs/themes/)).

### Server

`server.port`, `server.hostname`, `server.mdns`, `server.mdnsDomain` (default `opencode.local`), `server.cors` (full origins) ([Config – Server](https://opencode.ai/docs/config/)). CLI flags and defaults are in [automation.md](automation.md#server).

### References

`references: { alias: "../path" | "owner/repo" | { path | repository, branch?, description?, hidden? } }` ([References](https://opencode.ai/docs/references/)).

- Git repos are cloned into a cache and refreshed asynchronously.
- References show up in `@` autocomplete as `@alias` or `@alias/file`.
- References that have a `description` are injected into agent system context.
- Reference dirs are allowed through the `external_directory` permission automatically. Normal tool permissions still apply.

### Environment variables

Selection from [CLI – Environment variables](https://opencode.ai/docs/cli/):

| Group | Variables |
| --- | --- |
| Config | `OPENCODE_CONFIG`, `OPENCODE_TUI_CONFIG`, `OPENCODE_CONFIG_DIR`, `OPENCODE_CONFIG_CONTENT`, `OPENCODE_PERMISSION` (inline JSON permissions) |
| Behavior toggles | `OPENCODE_DISABLE_AUTOUPDATE`, `OPENCODE_DISABLE_AUTOCOMPACT`, `OPENCODE_DISABLE_DEFAULT_PLUGINS`, `OPENCODE_DISABLE_LSP_DOWNLOAD` |
| Claude Code compatibility | `OPENCODE_DISABLE_CLAUDE_CODE`, `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT`, `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS` |
| Web search | `OPENCODE_ENABLE_EXA`, `OPENCODE_ENABLE_PARALLEL` |
| Server auth | `OPENCODE_SERVER_PASSWORD`, `OPENCODE_SERVER_USERNAME` |
| Experimental | e.g. `OPENCODE_EXPERIMENTAL_LSP_TOOL`, `OPENCODE_EXPERIMENTAL_SCOUT`, `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS`, `OPENCODE_EXPERIMENTAL_WORKSPACES`, `OPENCODE_EXPERIMENTAL_PLAN_MODE` |

Other variables mentioned elsewhere in the notes: `OPENCODE_DISABLE_PROJECT_CONFIG` (this page), `OPENCODE_DISABLE_EXTERNAL_SKILLS` ([skills](skills.md)), `OPENCODE_AUTO_SHARE` ([automation](automation.md)), `OPENCODE_EXPERIMENTAL` ([plugins](plugins.md)).

## Loading and invocation

- All layers are read and merged at startup. Each `.opencode` dir and `OPENCODE_CONFIG_DIR` also contributes `commands/`, `agents/`, `modes/`, and `plugins/` ([SRC config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts)).
- The remote `.well-known/opencode` layer is fetched when you authenticate with a provider that supports it ([Config](https://opencode.ai/docs/config/)).
- Git references are cloned into a cache and refreshed asynchronously ([References](https://opencode.ai/docs/references/)).
- The legacy `theme`, `keybinds`, and `tui` keys in `opencode.json` are migrated to `tui.json` automatically when possible ([Config](https://opencode.ai/docs/config/)).

## Example

```jsonc
// opencode.jsonc (project root)
{ "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "instructions": ["CONTRIBUTING.md"],
  "permission": { "bash": "ask" },
  "provider": { "anthropic": { "options": { "apiKey": "{env:ANTHROPIC_API_KEY}" } } } }
```

## Limits and gotchas

- **Gap: array merging.** Only `instructions` (concatenated and deduplicated) and `plugin` (deduplicated by plugin identity) have documented merge behavior across layers. How other arrays, such as `watcher.ignore` or `disabled_providers`, merge is not documented.
- **Docs and source differ on layer 5 (inference from the notes).** The docs list `.opencode` directories before `OPENCODE_CONFIG_CONTENT`. In source, `OPENCODE_CONFIG_DIR` and `~/.opencode` are also scanned at that step. The docs do not mention `~/.opencode`; treat it as an implementation detail.
- **OpenCode Console org config** (`<console-url>/api/config`) is a source-only layer not in the documented precedence list.
- **Deprecated keys:** `reference` (use `references`, since v1.17.1), `autoshare` (use `share`), `mode` (use `agent`), `layout` (stretch layout always used), `tools` (use `permission`, since v1.1.1), and `theme` / `keybinds` / `tui` in `opencode.json` (moved to `tui.json`).
- **Recent changes:** header and chunk timeouts were raised to a 5-minute default in v1.18.27 ([REL v1.18.27](https://github.com/anomalyco/opencode/releases/tag/v1.18.27)). v1.17.1 added reference `description` and `hidden` and deprecated `reference` ([REL v1.17.1](https://github.com/anomalyco/opencode/releases/tag/v1.17.1)). v1.17.12 added reference autocomplete ([REL v1.17.12](https://github.com/anomalyco/opencode/releases/tag/v1.17.12)).
- **`default_agent`** falls back to `build` with a warning if it names a non-primary agent.
- **`disabled_providers` wins** over `enabled_providers`.
- **Gap:** the generated `https://opencode.ai/config.json` was not fetched; the key list comes from the Effect schema source.
- **Gap:** the full built-in keybind list (about 100 entries in keybinds.mdx) is not reproduced in the notes.
- **Gap:** the release in which LSP and formatters became opt-in was not found. Current docs and schema both say "Omit or set to false to disable".
- **Gap:** the notes did not check for a successor org or fork beyond anomalyco.

## Sources

- https://opencode.ai/docs/config/
- https://opencode.ai/docs/tui/
- https://opencode.ai/docs/keybinds/
- https://opencode.ai/docs/themes/
- https://opencode.ai/docs/references/
- https://opencode.ai/docs/cli/
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/paths.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/tui.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/agent.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts
- https://github.com/anomalyco/opencode/releases/tag/v1.17.1
- https://github.com/anomalyco/opencode/releases/tag/v1.17.12
- https://github.com/anomalyco/opencode/releases/tag/v1.18.27
