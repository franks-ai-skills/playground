# Hooks

A hook is a handler that the harness itself runs at a fixed point in the agent lifecycle, such as before a tool call or when a turn ends. Hooks enforce policy, add context and trigger side effects deterministically, which instructions to the model cannot guarantee. A hook receives a description of the event, and it can let the action proceed, block it, rewrite its input, or add context for the model.

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Mechanism | Declarative config: event → matcher group → handlers ([hooks][cc-hooks]) | Declarative config with the same three levels ([hooks][cx-hooks]) | JS/TS plugin functions; no declarative hook config recorded ([hooks][oc-hooks]) |
| User config | `~/.claude/settings.json` → `hooks` ([hooks][cc-hooks]) | `~/.codex/hooks.json` or `[hooks]` in `~/.codex/config.toml` ([hooks][cx-hooks]) | `~/.config/opencode/plugins/`, `plugin` config key ([hooks][oc-hooks]) |
| Project config | `.claude/settings.json`, `.claude/settings.local.json` ([hooks][cc-hooks]) | `.codex/hooks.json` or `[hooks]` in `.codex/config.toml`; only for a trusted project layer ([hooks][cx-hooks]) | `.opencode/plugins/` ([hooks][oc-hooks]) |
| Managed | Managed policy settings; cannot be removed ([hooks][cc-hooks]) | System, MDM, cloud, `requirements.toml`; users cannot disable them ([hooks][cx-hooks]) | Not recorded ([hooks][oc-hooks]) |
| Plugin | `hooks/hooks.json` or `hooks` in `plugin.json` ([hooks][cc-hooks]) | `hooks/hooks.json` or manifest `hooks` entry; paths start with `./` ([hooks][cx-hooks]) | The plugin is the hook ([hooks][oc-hooks]) |
| Component-scoped | Skill and subagent frontmatter `hooks` ([hooks][cc-hooks]) | None recorded ([hooks][cx-hooks]) | None ([hooks][oc-hooks]) |
| Layering | All levels merge; identical handlers run once ([hooks][cc-hooks]) | All sources load; no deduplication recorded ([hooks][cx-hooks]) | All plugins load in order ([hooks][oc-hooks]) |
| Events | About 30, grouped as session, turn, tool loop, agents, context/config, worktrees, MCP, UI ([hooks][cc-hooks]) | 12: `SessionStart`, `SubagentStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SubagentStop`, `Stop`, `Interrupt`, `SessionEnd` ([hooks][cx-hooks]) | Hook keys (`tool.execute.before/after`, `permission.ask`, `chat.*`, …) plus bus events via `event` ([hooks][oc-hooks]) |
| Handler types | `command`, `http`, `mcp_tool`, `prompt`, `agent` ([hooks][cc-hooks]) | `command`, `mcp_tool`; `prompt` and `agent` parsed but skipped ([hooks][cx-hooks]) | JS function ([hooks][oc-hooks]) |
| Matcher syntax | Exact name or `\|`/`,` list when only `[A-Za-z0-9_- ,\|]`; otherwise unanchored JS regex ([hooks][cc-hooks]) | Regex; `*`, `""` or omitted match all ([hooks][cx-hooks]) | Code inspects `input.tool` ([hooks][oc-hooks]) |
| Tool names | `Bash`, `Edit`, `Write`, `Agent`, `mcp__<server>__<tool>` ([hooks][cc-hooks]) | `apply_patch` also matches `Edit`/`Write`; shell matches `Bash`; `spawn_agent` matches `Agent`; MCP `mcp__server__tool`; hosted tools never hooked ([hooks][cx-hooks]) | Native tool IDs, e.g. `read`, `apply_patch` ([hooks][oc-hooks]) |
| Input | JSON on stdin (command) or POST body (http) ([hooks][cc-hooks]) | JSON on stdin ([hooks][cx-hooks]) | Function arguments `input`, `output` ([hooks][oc-hooks]) |
| Block | Exit 2 (stderr is the reason) or JSON decision ([hooks][cc-hooks]) | Exit 2 (stderr is the reason) or JSON decision ([hooks][cx-hooks]) | Throw in `tool.execute.before` ([hooks][oc-hooks]) |
| Other exit codes | Non-blocking error, including 1; missing script (127) silently disables the gate ([hooks][cc-hooks]) | Not recorded ([hooks][cx-hooks]) | n/a |
| Default timeout | 600 s for command, http, mcp_tool ([hooks][cc-hooks]) | 600 s; `SessionEnd`/`Interrupt` 1 s, max 3 ([hooks][cx-hooks]) | Not recorded ([hooks][oc-hooks]) |
| Execution | All matching handlers in parallel ([hooks][cc-hooks]) | Matching command hooks launched concurrently ([hooks][cx-hooks]) | Sequential, in plugin load order ([hooks][oc-hooks]) |
| Async | `async: true` (command only); cannot block; context next turn; killed at teardown in `-p` ([hooks][cc-hooks]) | `async: true`; cannot block or rewrite; context at next safe point; max 8 per session ([hooks][cx-hooks]) | n/a |
| Trust gate | Settings-file hooks wait for workspace trust in interactive sessions; `-p` and SDK treat the folder as trusted ([hooks][cc-hooks]) | Each non-managed hook must be trusted by hash via `/hooks`; changed hooks are skipped until re-trusted; `--dangerously-bypass-hook-trust` ([hooks][cx-hooks]) | Not recorded ([hooks][oc-hooks]) |
| Global off switch | `disableAllHooks`; `allowManagedHooksOnly` ([hooks][cc-hooks]) | `[features] hooks = false`; `allow_managed_hooks_only` ([hooks][cx-hooks]) | Not recorded ([hooks][oc-hooks]) |
| Security stance | Runs with full user permissions, outside the sandbox; `if` is best-effort ([hooks][cc-hooks]) | "a useful guardrail, not a complete enforcement boundary" ([hooks][cx-hooks]) | Not recorded ([hooks][oc-hooks]) |
| Context cost | Plain stdout reaches the model only on `UserPromptSubmit`, `UserPromptExpansion`, `SessionStart`, `PostModelSwitch`; `additionalContext` capped at 10,000 chars per string, overflow saved to a file ([hooks][cc-hooks]) | Plain stdout reaches the model only on `SessionStart`, `UserPromptSubmit`, `SubagentStart`; `additionalContext` default limit about 2,500 tokens, overflow spilled to a file ([hooks][cx-hooks]) | Nothing by default; `experimental.chat.*.transform` changes what the model sees ([hooks][oc-hooks]) |

## Generalized model

### Entities

- **Registration.** `event → [matcher group] → [handler]`. A matcher group has an optional `matcher` pattern and a list of handlers. Both leads use the same nested JSON shape: `{"hooks": {"<Event>": [{"matcher": "...", "hooks": [{"type": "...", ...}]}]}}`.
- **Event.** A named lifecycle point. Each event defines its matcher target, its input fields, and the decisions it accepts.
- **Matcher.** A pattern over the event's target (tool name, session source, compaction trigger, agent type). Empty, `*` or omitted matches everything. Some events ignore the matcher.
- **Handler.** One action. Two types are portable:
  - `command`: a shell command. Fields: `command`, `timeout` (seconds), `statusMessage`, `async`.
  - `mcp_tool`: a call to a tool on an already-connected MCP server. Fields: `server`, `tool`, `input` (template with `${tool_input.<field>}` placeholders), `timeout`, `statusMessage`.
- **Input.** A JSON object on the handler's stdin.
- **Output.** An exit code, plus optional plain text or a JSON object on stdout, plus stderr.

### Scopes and loading

| Scope | Notes |
| --- | --- |
| User | Always loaded |
| Project | Loaded only after the user trusts the project (and, in one lead, each hook definition) |
| Managed | Always loaded; cannot be disabled by the user; a policy switch can restrict hooks to managed ones only |
| Plugin | Loaded while the plugin is enabled |

Hooks from all scopes add up. No scope replaces another's hooks. All matching handlers for an event run, concurrently.

### Shared events

Both leads use identical event names for the overlap, so the generalized model keeps those names.

| Event | When | Matcher target | Can block or steer |
| --- | --- | --- | --- |
| `SessionStart` | Session starts, resumes, is cleared, or restarts after compaction | Source: `startup`, `resume`, `clear`, `compact` | Plain stdout becomes model context |
| `UserPromptSubmit` | User submits a prompt | None | Reject the prompt; add context |
| `PreToolUse` | Before a tool call | Tool name | Deny; rewrite input; add context |
| `PermissionRequest` | An approval prompt is about to appear | Tool name | Allow or deny on the user's behalf |
| `PostToolUse` | After a tool call | Tool name | Feed back a block reason; add context |
| `PreCompact` | Before context compaction | `manual`, `auto` | Cancel compaction (output differs per lead, see Portability) |
| `PostCompact` | After compaction | `manual`, `auto` | — |
| `SubagentStart` | A subagent starts | Agent type (Codex; not recorded for Claude Code) | — |
| `SubagentStop` | A subagent finishes | Agent type (Codex; not recorded for Claude Code) | Force the subagent to continue |
| `Stop` | The main agent's turn ends | None | Force the agent to continue with a reason |
| `SessionEnd` | Session ends | Reason | — |

### Decision contract (shared subset)

| Output | Meaning |
| --- | --- |
| Exit 0, no output | Proceed |
| Exit 0, plain stdout | Context for the model on `SessionStart` and `UserPromptSubmit` |
| Exit 2, reason on stderr | Block: deny the tool call (`PreToolUse`), reject the prompt (`UserPromptSubmit`), feed the reason back (`PostToolUse`), continue the agent (`Stop`, `SubagentStop`) |
| `hookSpecificOutput.permissionDecision: "deny"` + `permissionDecisionReason` | Deny a tool call with a reason (`PreToolUse`) |
| `permissionDecision: "allow"` + `updatedInput` | Rewrite the tool input |
| `additionalContext` | Extra model context on `PreToolUse` in both leads; other events vary per lead |
| `{"decision": "block", "reason": "..."}` | Block on `UserPromptSubmit`, `PostToolUse`, `Stop`, `SubagentStop` |
| `{"decision": {"behavior": "allow" \| "deny", "message": "..."}}` | Answer a `PermissionRequest` |
| `continue: false`, `stopReason`, `systemMessage` | Stop processing; reason; user-visible message. Codex accepts these only on `SessionStart`, `PreCompact`, `PostCompact`, `UserPromptSubmit`, `SubagentStop`, `Stop` |

### Shared input fields

- All events: `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `permission_mode` (most events in Codex).
- Tool events: `tool_name`, `tool_input`, `tool_use_id`.
- `Stop`: `stop_hook_active` (true when the agent is already continuing because of a stop hook; use it to avoid loops), `last_assistant_message`.

### Mapping

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Hook config file | `settings.json` → `hooks` | `hooks.json` or `config.toml` → `[hooks]` | Plugin module |
| Command handler | `type: "command"` | `type: "command"` | Function using the `$` shell helper |
| MCP tool handler | `type: "mcp_tool"` | `type: "mcp_tool"` | — |
| `SessionStart` | `SessionStart` | `SessionStart` | `event` hook, `session.created` (approximate) |
| `UserPromptSubmit` | `UserPromptSubmit` | `UserPromptSubmit` | `chat.message` (approximate) |
| `PreToolUse` | `PreToolUse` | `PreToolUse` | `tool.execute.before` |
| `PermissionRequest` | `PermissionRequest` | `PermissionRequest` | `permission.ask` |
| `PostToolUse` | `PostToolUse` | `PostToolUse` | `tool.execute.after` |
| `PreCompact` | `PreCompact` | `PreCompact` | `experimental.session.compacting` (approximate) |
| `PostCompact` | `PostCompact` | `PostCompact` | `event` hook, `session.compacted` |
| `SubagentStart` / `SubagentStop` | `SubagentStart` / `SubagentStop` | `SubagentStart` / `SubagentStop` | — |
| `Stop` | `Stop` | `Stop` | `event` hook, `session.idle` (approximate; observe only) |
| `SessionEnd` | `SessionEnd` | `SessionEnd` | — |
| Block | Exit 2 / JSON | Exit 2 / JSON | Throw |
| Project trust | Workspace trust dialog | Project layer trust plus per-hook hash trust | — |
| Disable all | `disableAllHooks` | `[features] hooks = false` | — |
| Managed only | `allowManagedHooksOnly` | `allow_managed_hooks_only` | — |

"Approximate" marks an OpenCode hook or bus event whose name and timing fit, but whose blocking and output semantics the pages do not confirm.

## Portability

### One script, two registrations

The leads read hooks from different files, but the `hooks` object has the same shape. Write the handler as one script in the repository and register it in both places:

- Claude Code: `.claude/settings.json` → `"hooks": {...}`.
- Codex: `.codex/hooks.json` with the same `{"hooks": {...}}` object, or `[[hooks.<Event>]]` tables in `.codex/config.toml`. Do not use both forms in one layer; Codex merges them with a warning ([hooks][cx-hooks]).

Plugins are the one place with the same path in both leads: `hooks/hooks.json`. Codex sets `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` for compatibility with Claude Code plugin hooks, in addition to its own `PLUGIN_ROOT` and `PLUGIN_DATA` ([hooks][cx-hooks]).

### Safe subset

- **Events:** the eleven shared events above.
- **Handler types:** `command` and `mcp_tool`. The `mcp_tool` fields `server`, `tool`, `input` and the `${tool_input.<field>}` placeholder are the same in both ([hooks][cc-hooks], [hooks][cx-hooks]).
- **Matchers:** `Bash`, `Edit|Write`, `Agent`, `mcp__<server>__.*`. Codex maps its own tool names onto these ([hooks][cx-hooks]). Inference: anchored patterns such as `^(Edit|Write)$` are regexes in both leads, so they match the same way; plain `Edit|Write` is an exact list in Claude Code and a regex in Codex, whose anchoring the pages do not record.
- **Paths:** Codex runs hooks with the session `cwd` and recommends `$(git rev-parse --show-toplevel)/...` ([hooks][cx-hooks]). That form also works in Claude Code's shell commands. `${CLAUDE_PROJECT_DIR}` is a Claude Code placeholder only.
- **Decisions:** exit 2 with a reason on stderr; `permissionDecision: "deny"` with `permissionDecisionReason`; `permissionDecision: "allow"` with `updatedInput`; `decision: "block"` with `reason` on `UserPromptSubmit`, `PostToolUse`, `Stop`, `SubagentStop`; `hookSpecificOutput.decision.behavior` on `PermissionRequest`; `additionalContext`.
- **Timeouts:** set `timeout` explicitly. Defaults agree at 600 s, but `SessionEnd` budgets differ (Claude Code 1.5 s shared, Codex 1 s, max 3).

### Traps

- **Codex fails open on unsupported `PreToolUse` output.** `"ask"`, `decision: "approve"`, `continue: false` and `stopReason` mark the hook run as failed, and the tool call proceeds ([hooks][cx-hooks]). A policy gate that answers `ask` blocks nothing in Codex.
- **Exit 1 is not a block.** Claude Code treats exit 1 as a non-blocking error and proceeds ([hooks][cc-hooks]). Codex behavior for exit codes other than 0 and 2 is not recorded. Use exit 2 for a `PreToolUse` gate, or its JSON deny decision. Claude Code ignores exit 2 on `PermissionRequest`; use `hookSpecificOutput.decision.behavior: "deny"` there ([hooks][cc-hooks], [hooks][cx-hooks]).
- **`allow` means different things.** In Claude Code a `PreToolUse` `allow` can approve the call, but never overrides deny or ask rules ([hooks][cc-hooks]). In Codex `allow` is documented only as the way to rewrite input ([hooks][cx-hooks]). Return `allow` only to rewrite input, not to approve.
- **Rewriting input needs per-tool shapes.** Codex requires a string `command` in `updatedInput` for Bash and `apply_patch` ([hooks][cx-hooks]). Inference: a hook that reads `tool_input.file_path` from `Edit`/`Write` in Claude Code may find a patch instead of a path when Codex sends `apply_patch`; the `apply_patch` input schema is not recorded.
- **Cancelling compaction differs.** Claude Code blocks it with exit 2 or `decision: "block"`; Codex cancels it with `continue: false` ([hooks][cc-hooks], [hooks][cx-hooks]). No single output does both.
- **`PostToolUse` block has different effects.** Claude Code shows the stderr to the model; Codex replaces the tool result with the feedback ([hooks][cc-hooks], [hooks][cx-hooks]). Neither undoes the tool's side effects.
- **Trust differs in headless runs.** Claude Code `-p` and SDK runs treat the folder as trusted, so repository hooks run without a prompt ([hooks][cc-hooks]). Codex skips new or changed hooks until they are trusted by hash, also in `codex exec`, unless `--dangerously-bypass-hook-trust` is set ([hooks][cx-hooks]). Editing a shared hook definition requires re-trusting it in Codex.
- **Plain stdout.** Only `SessionStart` and `UserPromptSubmit` turn plain stdout into context in both leads. Codex requires JSON for `Stop` and `SubagentStop`. Keep stdout free of stray output such as shell-profile messages ([hooks][cc-hooks], [hooks][cx-hooks]).
- **Subagent context in input.** Codex subagents share the parent's `session_id`, and `agent_id`/`agent_type` appear only on subagent events; Claude Code adds them to every hook that fires inside a subagent ([hooks][cx-hooks], [hooks][cc-hooks]).
- **Hosted tools are invisible in Codex.** Hosted tools such as WebSearch are never hooked ([hooks][cx-hooks]).
- **Not a security boundary.** Both vendors say this. Use permission rules and the sandbox for hard limits.
- **OpenCode needs an adapter.** OpenCode has no shell-command hooks. Inference: reusing a shared script means a plugin that builds the JSON input and calls the script through the `$` helper, then maps exit 2 to a thrown error in `tool.execute.before` ([hooks][oc-hooks]).

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| Events `Setup`, `UserPromptExpansion`, `StopFailure`, `PermissionDenied`, `PostToolUseFailure`, `PostToolBatch` | Claude Code | No Codex counterpart. |
| Events `TaskCreated`, `TaskCompleted`, `TeammateIdle` | Claude Code | Tied to agent teams, which Codex lacks. |
| Events `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `DirectoryAdded`, `FileChanged`, `PreModelSwitch`, `PostModelSwitch` | Claude Code | No Codex counterpart. |
| Events `WorktreeCreate`, `WorktreeRemove` | Claude Code | No Codex counterpart. |
| Events `Elicitation`, `ElicitationResult` | Claude Code | No Codex counterpart. |
| Events `Notification`, `MessageDisplay` | Claude Code | No Codex counterpart; for turn-complete alerts use `Stop` in both leads. |
| Event `Interrupt` | Codex | No Claude Code counterpart. |
| Handler types `http`, `prompt`, `agent` | Claude Code | Codex has no `http` type and skips `prompt` and `agent`. |
| Handler fields `if`, `once`, `args`, `shell`, `asyncRewake`, `continueOnBlock` | Claude Code | No Codex counterpart. |
| Handler fields `additionalContextLimit`, `commandWindows` | Codex | No Claude Code counterpart. |
| `permissionDecision: "ask"` and `"defer"` | Claude Code | Codex does not support them and fails open. |
| `updatedPermissions`, `interrupt` on `PermissionRequest` | Claude Code | Codex fails closed on them. |
| `updatedToolOutput`, `classifierContext` on `PostToolUse` | Claude Code | Codex does not support replacing MCP tool output yet. |
| `terminalSequence`, SessionStart extras (`initialUserMessage`, `sessionTitle`, `watchPaths`, `reloadSkills`), `retry` | Claude Code | No Codex counterpart. |
| Hooks in skill or subagent frontmatter | Claude Code | Codex has no component-scoped hooks. |
| SDK callback hooks (`options.hooks`) | Claude Code | The Codex SDK pages record no hook callbacks. |
| Mods (JavaScript function hooks in plugins) | Claude Code | No Codex counterpart; OpenCode's plugin hooks are similar but do not decide. |
| Hash-based per-hook trust | Codex | Claude Code trusts per workspace, not per hook; treated as a portability trap, not a model element. |
| `notify` program on `agent-turn-complete` | Codex | Overlaps `Stop`, which both leads have. |
| `tui.notifications` | Codex | Terminal UI setting, not a hook. |
| `allowedHttpHookUrls`, `httpHookAllowedEnvVars` | Claude Code | Depend on `http` handlers. |
| OpenCode `chat.params`, `chat.headers`, `shell.env`, `tool.definition`, `auth`, `provider`, `experimental.*` transforms | OpenCode | No lead counterpart. |

## Sources

- [Claude Code: hooks](../vendors/claude-code/hooks.md)
- [Codex: hooks](../vendors/codex/hooks.md)
- [OpenCode: hooks](../vendors/opencode/hooks.md)
- [Research notes: Claude Code extensions](../research-notes/agent-harness-configuration/claude-code-extensions.md)
- [Research notes: Codex extensions](../research-notes/agent-harness-configuration/codex-extensions.md)

[cc-hooks]: ../vendors/claude-code/hooks.md
[cx-hooks]: ../vendors/codex/hooks.md
[oc-hooks]: ../vendors/opencode/hooks.md
