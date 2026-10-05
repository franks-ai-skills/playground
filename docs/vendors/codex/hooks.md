# Hooks and notifications

Hooks run user-defined commands or MCP tool calls at fixed points in the Codex lifecycle, for example before a tool call or when a turn stops. They let you enforce policy, add context and gate completion without changing Codex itself ([Hooks](https://learn.chatgpt.com/docs/hooks.md)). The schema is close to Claude Code's (events with matcher groups, JSON on stdin, exit code 2 or JSON decisions on stdout, `hookSpecificOutput`). Separately, `notify` runs an external program when a turn completes, and `tui.notifications` emits terminal notifications.

## Locations and scopes

Hooks are discovered "next to active config layers", as `hooks.json` or as inline `[hooks]` tables in `config.toml` ([Hooks](https://learn.chatgpt.com/docs/hooks.md)):

| Source | Path | Notes |
|---|---|---|
| User | `~/.codex/hooks.json`, `~/.codex/config.toml` | |
| Project | `<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml` | Load only when the project `.codex/` layer is trusted |
| Plugin | `hooks/hooks.json` in the plugin, or the manifest `hooks` entry | Manifest hook paths must start with `./` and stay inside the plugin root. Not trusted automatically on install |
| Managed | System, MDM, cloud, `requirements.toml` `[hooks]` | Trusted by policy; users cannot disable them |

- **All sources load.** Higher-precedence layers do not replace lower ones. Having both `hooks.json` and inline `[hooks]` in one layer merges them with a warning ([Hooks](https://learn.chatgpt.com/docs/hooks.md)).
- **Feature flag.** `features.hooks` is on by default: "Enable lifecycle hooks loaded from `hooks.json` or inline `[hooks]` config. `features.codex_hooks` is a deprecated alias." Disable with `[features] hooks = false` ([Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md); [Hooks](https://learn.chatgpt.com/docs/hooks.md)). Local 0.159.2: `hooks` stable/true, `plugin_hooks` removed.
- **Managed hooks.** `requirements.toml` can define `[hooks]` with `managed_dir` / `windows_managed_dir` (absolute paths whose scripts are deployed by MDM, not by Codex). `allow_managed_hooks_only = true` skips user, project, session and plugin hooks. Pin `[features].hooks = true` to enforce them. Under cloud orchestration (Work Cloud and dots), only admin `mcp_tool` hooks are supported ([Hooks](https://learn.chatgpt.com/docs/hooks.md)).

## Format

### Structure

Three levels: event → matcher group → `hooks[]` handlers. A matcher is a regex; `"*"`, `""` or an omitted matcher matches everything. `hooks.json` accepts an optional top-level `description` ([Hooks](https://learn.chatgpt.com/docs/hooks.md)).

### Command handler

| Field | Meaning | Default |
|---|---|---|
| `type` | `"command"` | |
| `command` | Shell command to run | |
| `timeout` | Seconds | `600`; `SessionEnd`/`Interrupt`: `1`, max `3` |
| `statusMessage` | Message shown while the hook runs | |
| `additionalContextLimit` | Limit for `additionalContext`; `0` means unlimited | about 2500 tokens |
| `commandWindows` / `command_windows` | Windows-specific command | |
| `async` | Run in the background | `false` |

Sources: [Hooks](https://learn.chatgpt.com/docs/hooks.md); [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md).

### MCP tool handler

| Field | Meaning | Default |
|---|---|---|
| `type` | `"mcp_tool"` | |
| `server` | An already-connected MCP server | |
| `tool` | Tool name | |
| `input` | Argument template with placeholders such as `${tool_input.file_path}`. A placeholder that fills a whole value keeps its JSON type | |
| `timeout` | Seconds | `600` |
| `statusMessage` | Message shown while the hook runs | |

MCP hooks use existing connections only and run synchronously. Errors or missing servers do not block. `SessionEnd` does not support MCP hooks ([Hooks](https://learn.chatgpt.com/docs/hooks.md)). See [mcp.md](mcp.md).

`prompt` and `agent` handler types are parsed but skipped.

### Events and matchers

| Event | When | Matcher matches |
|---|---|---|
| `SessionStart` | Session start | Source: `startup`, `resume`, `clear`, `compact` |
| `SubagentStart` | Subagent start | Agent type |
| `UserPromptSubmit` | During a turn, on prompt submit | Ignores matchers |
| `PreToolUse` | During a turn, before a tool call | Tool name |
| `PermissionRequest` | During a turn, on an approval request | Tool name |
| `PostToolUse` | During a turn, after a tool call | Tool name |
| `PreCompact` | During a turn, before compaction | `manual`, `auto` |
| `PostCompact` | During a turn, after compaction | `manual`, `auto` |
| `SubagentStop` | During a turn, when a subagent stops | Agent type |
| `Stop` | During a turn, when the turn stops | Ignores matchers |
| `Interrupt` | On interrupt; not for subagents | Ignores matchers |
| `SessionEnd` | When the main thread ends; not for subagents | Reason (only `other`) |

Tool-name matching ([Hooks](https://learn.chatgpt.com/docs/hooks.md)):

- `apply_patch` also matches `Edit` or `Write`.
- Shell and `exec_command` match `Bash`.
- MCP tools match `mcp__server__tool`.
- Other local function tools match by name, for example `update_plan`.
- `spawn_agent` also matches `Agent`.
- Hosted tools such as WebSearch are never hooked.

### Input (JSON on stdin)

| Field | Events |
|---|---|
| `session_id` | All. Subagents get the parent's ID |
| `transcript_path` | All. The transcript format is not stable |
| `cwd`, `hook_event_name`, `model` | All |
| `turn_id` | Turn-scoped events |
| `permission_mode` | Most events: `default`, `acceptEdits`, `plan`, `dontAsk`, `bypassPermissions` |
| `source` | `SessionStart` |
| `reason` | `SessionEnd` |
| `agent_id`, `agent_type` | `SubagentStart`, `SubagentStop` |
| `agent_transcript_path`, `stop_hook_active`, `last_assistant_message` | `SubagentStop` |
| `tool_name`, `tool_use_id`, `tool_input` | `PreToolUse`, `PostToolUse` |
| `tool_response` | `PostToolUse` |
| `tool_input.description` | `PermissionRequest` |
| `trigger` | `PreCompact`, `PostCompact` |
| `prompt` | `UserPromptSubmit` |
| `stop_hook_active`, `last_assistant_message` | `Stop` |

Generated wire schemas live at `codex-rs/hooks/schema/generated` ([Hooks](https://learn.chatgpt.com/docs/hooks.md)).

### Output

- Exit `0` with no output means success.
- Common JSON fields `continue`, `stopReason`, `systemMessage` (shown as a UI warning) and `suppressOutput` (parsed but not implemented) apply to `SessionStart`, `PreCompact`, `PostCompact`, `UserPromptSubmit`, `SubagentStop` and `Stop`.
- Plain stdout becomes developer context for `SessionStart`, `UserPromptSubmit` and `SubagentStart` (the latter for the subagent). It is ignored for `PreToolUse`, `PostToolUse`, `PermissionRequest`, `PreCompact` and `PostCompact`. It is invalid for `Stop`, `SubagentStop` and `Interrupt`, which require JSON.

Per-event decisions:

| Event | Supported output | Unsupported |
|---|---|---|
| `PreToolUse` | Deny with `hookSpecificOutput.permissionDecision: "deny"` plus `permissionDecisionReason`, legacy `{"decision":"block","reason":...}`, or exit 2 with the reason on stderr. Rewrite the call with `permissionDecision: "allow"` plus `updatedInput` (Bash and `apply_patch` need a string `command`). Add context with `additionalContext` | `"ask"`, `decision:"approve"`, `continue:false`, `stopReason`: the hook run is marked failed and the tool call proceeds |
| `PermissionRequest` | `hookSpecificOutput.decision.behavior` `allow` or `deny` (with `message`). Any deny wins. No decision: the normal approval prompt appears | `updatedInput`, `updatedPermissions`, `interrupt` "fail closed today" |
| `PostToolUse` | `decision:"block"` or exit 2 replaces the tool result with your feedback (it cannot undo side effects). `continue:false` stops normal processing of the result. `additionalContext` | `updatedMCPToolOutput` not supported yet |
| `UserPromptSubmit` | Block with `decision:"block"` or exit 2, or add context | |
| `Stop`, `SubagentStop` | `decision:"block"` plus `reason` (or exit 2): Codex continues with `reason` as a new prompt. `continue:false` from any hook wins | |
| `PreCompact` | `continue:false` cancels compaction | |
| `SessionStart` | Source `compact` runs after compaction, before the next model request | |
| `Interrupt` | Only `systemMessage` | |

Sources: [Hooks](https://learn.chatgpt.com/docs/hooks.md).

### Plugin hook environment

Plugin hooks receive `PLUGIN_ROOT` and `PLUGIN_DATA`. "Codex also sets `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` for compatibility with existing plugin hooks." ([Hooks](https://learn.chatgpt.com/docs/hooks.md)) See [plugins.md](plugins.md).

### `notify`

| Element | Value |
|---|---|
| Config | `notify = ["python3", "/path/to/notify.py"]` (program plus arguments) |
| Events | Only `agent-turn-complete` |
| Input | One JSON argument (argv) with `type`, `thread-id`, `turn-id`, `cwd`, `input-messages`, `last-assistant-message` |
| Scope | User config only; ignored in project `.codex/config.toml` with a startup warning |

Source: [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced.md).

### TUI notifications

| Key | Meaning | Default |
|---|---|---|
| `tui.notifications` | Bool, or an array of event types such as `agent-turn-complete` or `approval-requested` | |
| `tui.notification_method` | `auto`, `osc9` or `bel`. `auto` prefers OSC 9 and falls back to BEL | `auto` |
| `tui.notification_condition` | `unfocused` or `always` | `unfocused` |

Sources: [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced.md); [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md).

The desktop app has its own notification settings (turn completion: never, background or always; permission and question notifications) and an Activity view. The IDE extension has no notification controls; configure `notify` on the host instead ([Notifications](https://learn.chatgpt.com/docs/notifications.md)).

## Loading and invocation

- **Trust.** "Before a non-managed hook can run, Codex requires you to review and trust the exact hook definition. Codex records trust against the hook's current hash, so new or changed hooks are marked for review and skipped until trusted." Use `/hooks` to inspect, trust or disable hooks. `--dangerously-bypass-hook-trust` skips the trust check for one invocation, in both `codex` and `codex exec` ([Hooks](https://learn.chatgpt.com/docs/hooks.md); local `codex exec --help`).
- **Execution.** "Matching hooks from multiple files all run. Multiple matching command hooks for the same event are launched concurrently." Commands run with the session `cwd`, so the docs recommend Git-root-based paths such as `$(git rev-parse --show-toplevel)/.codex/hooks/...` ([Hooks](https://learn.chatgpt.com/docs/hooks.md)).
- **Context cost.** Hook output enters context only where the event allows it (plain stdout for `SessionStart`, `UserPromptSubmit`, `SubagentStart`; `additionalContext` elsewhere). `additionalContext` over the limit is "spilled" to `<CODEX_HOME>/hook_outputs/...txt`, and the model gets a head-and-tail preview ([Hooks](https://learn.chatgpt.com/docs/hooks.md)).
- **Async hooks** (`async: true`) run in the background and deliver `additionalContext`/`systemMessage` at the next safe point. They cannot block or rewrite. At most 8 run concurrently per session, unfinished ones are cancelled at session end, and `SessionEnd` always runs synchronously ([Hooks](https://learn.chatgpt.com/docs/hooks.md)).
- **Code mode.** A `PreToolUse` block rejects the nested JS tool promise, and `updatedInput` rewrites the call ([Hooks](https://learn.chatgpt.com/docs/hooks.md)).
- **Metrics.** OpenTelemetry `hooks.run` and `hooks.run.duration_ms` ([Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced.md)).

## Example

`~/.codex/hooks.json`:

```json
{"hooks":{"PreToolUse":[{"matcher":"^Bash$","hooks":[{"type":"command","command":"python3 ~/.codex/hooks/policy.py","timeout":30,"statusMessage":"Checking Bash command"}]}]}}
```

Equivalent inline TOML in `config.toml`:

```toml
[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = "python3 ~/.codex/hooks/policy.py"
timeout = 30
statusMessage = "Checking Bash command"
```

Source: [Hooks](https://learn.chatgpt.com/docs/hooks.md). After adding the hook, trust it with `/hooks`.

## Limits and gotchas

- **Not an enforcement boundary.** "Treat tool hooks as a useful guardrail, not a complete enforcement boundary." Hosted tools such as WebSearch are never hooked ([Hooks](https://learn.chatgpt.com/docs/hooks.md)).
- **Unsupported handler types.** `prompt` and `agent` handlers are parsed but skipped.
- **`"ask"` is unsupported** in `PreToolUse`; the hook run fails and the tool call proceeds.
- **New or edited hooks are skipped until trusted**, including plugin hooks after install.
- **`notify` supports only `agent-turn-complete`.** Inference: richer automation (approval requests, stop gating) should use hooks (`PermissionRequest`, `Stop`).
- **Claude Code compatibility.** Inference: hook scripts written for Claude Code largely carry over (same event names for the overlapping set, stdin JSON fields, exit-code-2 semantics, `hookSpecificOutput`, `permissionDecision`, `CLAUDE_PLUGIN_ROOT`). Differences: `prompt`/`agent` handlers are skipped, `"ask"` is unsupported, hash-based trust is required, and Codex has its own events (`Interrupt`, `PermissionRequest` semantics) and fields (`turn_id`, `model`).
- **Deprecated alias.** `features.codex_hooks` is a deprecated alias of `features.hooks`. The `plugin_hooks` flag is removed (local 0.159.2).
- **Gap:** exact behavior when the same hook is defined in several layers is not documented beyond "all load"; nothing indicates deduplication.
- **Gap:** no documented list of TUI notification event types beyond `agent-turn-complete` and `approval-requested`.

## Sources

- https://learn.chatgpt.com/docs/hooks.md
- https://learn.chatgpt.com/docs/config-file/config-reference.md
- https://learn.chatgpt.com/docs/config-file/config-advanced.md
- https://learn.chatgpt.com/docs/notifications.md
