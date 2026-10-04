# Hooks

The notes record no separate hooks config file and no config key that runs a shell command on an event. Event-driven behavior comes through plugins: a plugin returns a hooks object whose functions run before or after tool calls, on permission requests, on chat requests, and on every bus event. This page lists the hook interface and the event list; loading, packaging, and the plugin API are in [plugins.md](plugins.md).

## Locations and scopes

Hooks live in plugins, so they share the plugin locations ([Plugins](https://opencode.ai/docs/plugins/)):

| Scope | Location |
| --- | --- |
| Global local plugins | `~/.config/opencode/plugins/` |
| Project local plugins | `.opencode/plugins/` |
| npm plugins | `plugin` key in any config layer, e.g. `"plugin": ["opencode-wakatime", "@my-org/x"]` |

Load order: global config `plugin`, then project config `plugin`, then the global plugin dir, then the project plugin dir. All hooks run in sequence ([Plugins](https://opencode.ai/docs/plugins/)). Details in [plugins.md](plugins.md#locations-and-scopes).

Two event-like behaviors are configured without plugins: formatters run after each write or edit, and LSP diagnostics are fed back to the agent ([plugins.md](plugins.md#lsp)).

## Format

A V1 plugin is a function `(input: PluginInput, options?: PluginOptions) => Promise<Hooks>` ([SRC plugin/src/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts)). The returned `Hooks` object can contain the keys below.

### Hook interface

From the current source ([SRC packages/plugin/src/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts); [REL v1.15.11](https://github.com/anomalyco/opencode/releases/tag/v1.15.11)):

| Hook | Signature / fields | Purpose |
| --- | --- | --- |
| `dispose` | | Cleanup. Added in v1.15.11. |
| `event` | `({event})` | Receives every bus event (see below). |
| `config` | `(cfg)` | Receives the config. |
| `tool` | `{name: ToolDefinition}` | Adds tools ([plugins.md](plugins.md#custom-tools)). |
| `auth` | `AuthHook` | Provider auth with OAuth or API methods and a loader. |
| `provider` | `ProviderHook` = `{id, models()}` | Adds a provider. |
| `chat.message` | `input {sessionID, agent, model, messageID, variant}`, `output {message, parts}` | Sees or changes a chat message. |
| `chat.params` | output: `temperature`, `topP`, `topK`, `maxOutputTokens`, `options` | Modifies model parameters. |
| `chat.headers` | | Modifies request headers. |
| `permission.ask` | `output.status` = `ask`, `deny`, or `allow` | Overrides a permission decision ([permissions-and-sandbox.md](permissions-and-sandbox.md)). |
| `command.execute.before` | `input {command, sessionID, arguments}`, `output {parts}` | Rewrites command parts ([commands.md](commands.md)). |
| `tool.execute.before` | `input {tool, sessionID, callID}`, `output {args}` | Changes tool args. Throwing blocks the call. |
| `tool.execute.after` | `input {…, args}`, `output {title, output, metadata}` | Changes tool results. |
| `shell.env` | `input {cwd, sessionID?, callID?}`, `output {env}` | Sets environment variables for shell execution. |
| `tool.definition` | | Rewrites a tool's description and parameters. |
| `experimental.chat.messages.transform` | | Transforms the message list. |
| `experimental.chat.system.transform` | `output.system: string[]` | Transforms the system prompt. |
| `experimental.provider.small_model` | | Chooses the small model. |
| `experimental.session.compacting` | `output.context[]` or `output.prompt` | Adds compaction context, or replaces the default compaction prompt with `output.prompt`. |
| `experimental.compaction.autocontinue` | `output.enabled` | Controls auto-continue after compaction. |
| `experimental.text.complete` | | Post-processes completed text. |

### Bus events for the `event` hook

([Plugins – Events](https://opencode.ai/docs/plugins/))

| Group | Events |
| --- | --- |
| command | `command.executed` |
| file | `file.edited`, `file.watcher.updated` |
| installation | `installation.updated` |
| LSP | `lsp.client.diagnostics`, `lsp.updated` |
| message | `message.part.removed`, `message.part.updated`, `message.removed`, `message.updated` |
| permission | `permission.asked`, `permission.replied` |
| server | `server.connected` |
| session | `session.created`, `session.compacted`, `session.deleted`, `session.diff`, `session.error`, `session.idle`, `session.status`, `session.updated` |
| todo | `todo.updated` |
| shell | `shell.env` |
| tool | `tool.execute.before`, `tool.execute.after` |
| TUI | `tui.prompt.append`, `tui.command.execute`, `tui.toast.show` |

The HTTP server also has an SSE event endpoint at `/global/event` ([Server](https://opencode.ai/docs/server/)); see [automation.md](automation.md#server).

### V2 hooks

The V2 plugin API (v1.17.10) registers hooks imperatively inside `setup(ctx)` instead of returning a hooks object. Transform hooks are `ctx.agent|catalog|command|integration|reference|skill.transform`; runtime hooks include `ctx.aisdk.sdk`. Registrations can be removed with `dispose()` ([SRC packages/plugin/src/v2/promise/README.md](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/v2/promise/README.md); [REL v1.17.10](https://github.com/anomalyco/opencode/releases/tag/v1.17.10)). See [plugins.md](plugins.md#v2-plugin-api).

## Loading and invocation

- Plugins, and with them their hooks, load at startup ([Plugins](https://opencode.ai/docs/plugins/)).
- All hooks run in sequence, in plugin load order.
- `tool.execute.before` runs before every tool call; throwing an error blocks the call. For `apply_patch`, `input.tool === "apply_patch"` and the patch is in `args.patchText` ([Tools](https://opencode.ai/docs/tools/)).
- `shell.env` output also applies to PTY sessions since v1.17.7 ([REL v1.17.7](https://github.com/anomalyco/opencode/releases/tag/v1.17.7)).
- Hooks are JS/TS functions, not shell commands. A hook that needs a shell uses the `$` helper from the plugin input, as in the example below.
- Context cost: hooks add nothing to context by themselves; `experimental.chat.system.transform` and `experimental.chat.messages.transform` can change what the model sees.

## Example

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

## Limits and gotchas

- **No declarative hooks in the notes.** Every hook described is plugin code; the notes record no config key that maps an event to a shell command.
- **Docs event list vs source hook interface.** The docs event list includes `shell.env`, `tool.execute.before`, and `tool.execute.after`, which the source also defines as dedicated hooks. The notes do not clarify whether these also arrive at the `event` hook as bus events.
- **`experimental.*` hooks** are marked experimental in the interface.
- **V2 hooks are newer and less stable (inference from the notes).** They are documented only in the package README, not on the docs page.
- **Release history:** `dispose` added in v1.15.11; a plugin file that fails to load no longer breaks the remaining plugins since v1.15.6 ([REL v1.15.6](https://github.com/anomalyco/opencode/releases/tag/v1.15.6)); `shell.env` applies to PTY sessions since v1.17.7; V2 API added in v1.17.10.
- **Gap:** the `auth` and `provider` hook shapes were not explored in depth.

## Sources

- https://opencode.ai/docs/plugins/
- https://opencode.ai/docs/tools/
- https://opencode.ai/docs/server/
- https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/v2/promise/README.md
- https://github.com/anomalyco/opencode/releases/tag/v1.15.6
- https://github.com/anomalyco/opencode/releases/tag/v1.15.11
- https://github.com/anomalyco/opencode/releases/tag/v1.17.7
- https://github.com/anomalyco/opencode/releases/tag/v1.17.10
