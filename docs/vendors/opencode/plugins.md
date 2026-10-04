# Plugins

A plugin is a JavaScript or TypeScript module that extends OpenCode with hooks, custom tools, auth methods, and providers. Plugins load from local `plugins/` directories or from npm through the `plugin` config key. This page also covers custom tool files, TUI plugins, and the built-in LSP and formatter integrations, which extend the harness without plugin code.

## Locations and scopes

| Scope | Location | Notes |
| --- | --- | --- |
| Global local | `~/.config/opencode/plugins/` | Loaded automatically at startup ([Plugins](https://opencode.ai/docs/plugins/)). |
| Project local | `.opencode/plugins/` | Same. |
| npm | `plugin` key in any config layer: `"plugin": ["opencode-wakatime", "@my-org/x"]` | Installed with Bun at startup and cached in `~/.cache/opencode/node_modules/` ([Plugins](https://opencode.ai/docs/plugins/)). |
| TUI | `plugin` key in `tui.json[c]` | See [TUI plugins](#tui-plugins). |
| Custom tools | `.opencode/tools/`, `~/.config/opencode/tools/` | See [Custom tools](#custom-tools). |

Any config directory (`~/.config/opencode`, `.opencode` dirs, `~/.opencode`, `OPENCODE_CONFIG_DIR`) contributes its `plugins/` subdirectory ([SRC config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts)); see [configuration.md](configuration.md#config-directories).

### Load order

Global config `plugin`, then project config `plugin`, then the global plugin dir, then the project plugin dir. All hooks run in sequence. The same npm package at the same version loads once ([Plugins](https://opencode.ai/docs/plugins/)).

Across config layers, `plugin` entries are deduped by plugin identity and their origin (global or local) is tracked. Path-like plugin specs resolve relative to the config file that declared them ([SRC config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts)).

### Dependencies

A `package.json` in a config dir (e.g. `.opencode/package.json`) is installed with `bun install` at startup. OpenCode also auto-adds `@opencode-ai/plugin` to each config dir ([Plugins](https://opencode.ai/docs/plugins/); [SRC config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts)).

### CLI and switches

| Command / switch | Effect |
| --- | --- |
| `opencode plugin <module> [-g] [-f]` (alias `plug`) | Installs a plugin and updates the config ([CLI](https://opencode.ai/docs/cli/)). |
| `--pure` | Runs without external plugins ([CLI](https://opencode.ai/docs/cli/)). |
| `OPENCODE_DISABLE_DEFAULT_PLUGINS` | Disables the default plugins ([CLI](https://opencode.ai/docs/cli/)). |

## Format

### V1 plugin API (hooks object)

- Config entry: a string, or a tuple `[spec, {…options}]` ([SRC core plugin.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/plugin.ts)).
- Type: `Plugin = (input: PluginInput, options?: PluginOptions) => Promise<Hooks>`. A `PluginModule` may also be `{ id?, server: Plugin }` ([SRC plugin/src/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts)).
- A module exports async plugin functions. Each receives the input below and returns a hooks object.

| `PluginInput` field | Meaning |
| --- | --- |
| `project` | Current project. |
| `client` | Client object, used e.g. for `client.app.log(...)`. |
| `$` | Shell helper. |
| `directory` | Current directory. |
| `worktree` | Git worktree root. |
| `serverUrl` | Server URL. |
| `experimental_workspace` | Experimental workspace. |

The full hook list and the bus event list are in [hooks.md](hooks.md).

Logging: use `client.app.log({ body: {service, level, message, extra} })` for structured logs ([Plugins](https://opencode.ai/docs/plugins/)).

### V2 plugin API

Added in v1.17.10 ([REL v1.17.10](https://github.com/anomalyco/opencode/releases/tag/v1.17.10); [SRC packages/plugin/src/v2/promise/README.md](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/v2/promise/README.md)):

- Import `define({ id, setup: async (ctx) => {…} })` from `@opencode-ai/plugin/v2/promise`, or the Effect variant from `@opencode-ai/plugin/v2/effect`.
- `setup` registers hooks imperatively and does not return a hooks object.
- Plugin options are available as `ctx.options`.
- Transform hooks: `ctx.agent.transform`, `ctx.catalog.transform`, `ctx.command.transform`, `ctx.integration.transform`, `ctx.reference.transform`, `ctx.skill.transform`.
- Runtime hooks include `ctx.aisdk.sdk`.
- Registrations can be removed with `dispose()`.

### Custom tools

([Custom tools](https://opencode.ai/docs/custom-tools/); [SRC plugin/src/tool.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/tool.ts))

| Aspect | Rule |
| --- | --- |
| Location | `.opencode/tools/` or `~/.config/opencode/tools/`, or returned from a plugin's `tool` hook. |
| Definition | `tool({ description, args, execute })` from `@opencode-ai/plugin`. |
| Naming | Default export: the filename is the tool name. Named exports become `<filename>_<export>`. |
| Arguments | `tool.schema` (Zod) or plain Zod. |
| `execute(args, context)` | `context` has `agent`, `sessionID`, `messageID`, `directory`, `worktree`, `abort`, `metadata()`, `ask()`. |
| Return value | A string, or `{ title?, output, metadata?, attachments?: [{type:"file", mime, url, filename?}] }`. |
| Name clash | A custom tool or plugin tool with the same name as a built-in overrides it. |
| Other languages | Tools can shell out to any language, e.g. with `Bun.$`. |

Tool output beyond 2000 lines or 51200 bytes (configurable in `tool_output`) is truncated and saved to disk ([SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)). Custom tools are gated by name in `permission` like other tools ([permissions-and-sandbox.md](permissions-and-sandbox.md)).

Built-in tools for reference: bash, edit, write, read, grep, glob, list, apply_patch, skill, todowrite, webfetch, websearch, question, task, plus an experimental lsp tool. All are enabled and need no permission by default. `websearch` (Exa or Parallel) is available only with the OpenCode or OpenCode Go provider, or with `OPENCODE_ENABLE_EXA` / `OPENCODE_ENABLE_PARALLEL`. grep and glob use ripgrep and respect `.gitignore`; a `.ignore` file with `!path` re-includes paths ([Tools](https://opencode.ai/docs/tools/)). `experimental.batch_tool` enables a batch tool ([SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)).

### TUI plugins

`@opencode-ai/plugin/tui` exports types built on OpenTUI (Solid renderables, keymaps, slots). `tui.json` accepts plugin specs in its `plugin` key ([SRC packages/plugin/src/tui.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/tui.ts); [SRC config/tui.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/tui.ts)).

### LSP

([LSP](https://opencode.ai/docs/lsp/))

| Setting | Effect |
| --- | --- |
| key omitted | Disabled (default). |
| `"lsp": false` | Disables all. |
| `"lsp": true` | Enables the built-in servers. |
| `"lsp": { … }` | Enables the built-ins with per-server overrides. |

Per-server keys: `disabled`, `command`, `extensions`, `env`, `initialization`. About 35 built-in servers (typescript, pyright, gopls, rust-analyzer, eslint, oxlint, clangd, jdtls, …), many installed automatically. `OPENCODE_DISABLE_LSP_DOWNLOAD` stops the downloads. The agent-facing `lsp` tool requires `OPENCODE_EXPERIMENTAL_LSP_TOOL` or `OPENCODE_EXPERIMENTAL` ([Tools](https://opencode.ai/docs/tools/)).

### Formatters

([Formatters](https://opencode.ai/docs/formatters/))

| Setting | Effect |
| --- | --- |
| key omitted | Disabled (default). |
| `"formatter": true` | Enables the built-in formatters. |
| `"formatter": { … }` | Enables the built-ins with per-formatter overrides. |

Per-formatter keys: `disabled`, `command` (with a `$FILE` placeholder), `environment`, `extensions`. Built-ins include prettier, biome, ruff, gofmt, rustfmt, shfmt, and others.

## Loading and invocation

- **Startup:** local plugin files and npm plugins load at startup; npm plugins and config-dir `package.json` dependencies are installed with Bun first ([Plugins](https://opencode.ai/docs/plugins/)).
- **Runtime:** hooks fire on their events in plugin load order ([hooks.md](hooks.md)).
- **Custom tools** are available to the model next to the built-in tools. The `tool.definition` hook can rewrite any tool's description and parameters ([hooks.md](hooks.md)).
- **LSP:** diagnostics are fed back to the agent ([LSP](https://opencode.ai/docs/lsp/)).
- **Formatters:** run after each write or edit ([Formatters](https://opencode.ai/docs/formatters/)).

## Example

Plugin with hooks:

```ts
// .opencode/plugins/guard.ts
import type { Plugin } from "@opencode-ai/plugin"
export const Guard: Plugin = async ({ $ }) => ({
  "tool.execute.before": async (input, output) => {
    if (input.tool === "read" && output.args.filePath.includes(".env")) throw new Error("no .env")
  },
  event: async ({ event }) => { if (event.type === "session.idle") await $`say done` },
})
```

Custom tool:

```ts
// .opencode/tools/database.ts
import { tool } from "@opencode-ai/plugin"
export default tool({ description: "Query the project database",
  args: { query: tool.schema.string().describe("SQL") },
  async execute(args, ctx) { return `ran ${args.query} in ${ctx.worktree}` } })
```

LSP and formatter config:

```json
{ "lsp": true, "formatter": { "prettier": { "disabled": true } } }
```

## Limits and gotchas

- **Plugin and custom tools override built-ins** with the same name.
- **Load failures are isolated since v1.15.6:** a plugin file that fails to load no longer breaks the remaining plugins ([REL v1.15.6](https://github.com/anomalyco/opencode/releases/tag/v1.15.6)).
- **V2 API is newer and less stable (inference from the notes).** The docs page covers only the V1 hooks-object API; V2 is documented only in the package README.
- **LSP and formatters are opt-in.** Omit the key and they stay disabled. **Gap:** the release that made them opt-in was not found in the v1.0–v1.18 release notes searched.
- **The LSP docs caution** that running lint/typecheck CLIs directly is often better ([LSP](https://opencode.ai/docs/lsp/)).
- **`lsp` permission** is currently non-granular ([permissions-and-sandbox.md](permissions-and-sandbox.md)).
- **Release history:** `dispose` hook added in v1.15.11 ([REL v1.15.11](https://github.com/anomalyco/opencode/releases/tag/v1.15.11)); `shell.env` applies to PTY sessions since v1.17.7 ([REL v1.17.7](https://github.com/anomalyco/opencode/releases/tag/v1.17.7)); V2 API in v1.17.10.
- **Gap:** the user docs do not cover the TUI plugin API; only the type exports were confirmed.
- **Gap:** the `auth` and `provider` hook shapes were not explored in depth.
- **Gap:** `tools.mdx` does not document the `list` tool, although the `list` permission key exists.

## Sources

- https://opencode.ai/docs/plugins/
- https://opencode.ai/docs/custom-tools/
- https://opencode.ai/docs/tools/
- https://opencode.ai/docs/lsp/
- https://opencode.ai/docs/formatters/
- https://opencode.ai/docs/cli/
- https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/tool.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/tui.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/v2/promise/README.md
- https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/plugin.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/tui.ts
- https://github.com/anomalyco/opencode/releases/tag/v1.15.6
- https://github.com/anomalyco/opencode/releases/tag/v1.15.11
- https://github.com/anomalyco/opencode/releases/tag/v1.17.7
- https://github.com/anomalyco/opencode/releases/tag/v1.17.10
