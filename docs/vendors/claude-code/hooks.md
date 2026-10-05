# Hooks

Hooks are deterministic handlers that the harness runs, not the model, at specific points in Claude Code's lifecycle: "user-defined shell commands, HTTP endpoints, MCP tool calls, LLM prompts, or subagents that execute automatically" ([hooks reference](https://code.claude.com/docs/en/hooks)). They enforce policy, add context, and automate side effects that instructions in CLAUDE.md cannot guarantee. Configuration is event → matcher group → handlers; control flows through exit codes and JSON on stdout. Plugins can also register JavaScript function hooks; such a plugin is a "mod" (see [plugins.md](plugins.md#mods)).

## Locations and scopes

| Location | Scope |
| :- | :- |
| `~/.claude/settings.json` | All your projects |
| `.claude/settings.json` | Project, shareable |
| `.claude/settings.local.json` | Project, local only |
| Managed policy settings | Organization |
| Plugin `hooks/hooks.json` (or `hooks` in `plugin.json`) | While the plugin is enabled |
| Skill frontmatter `hooks` | Rest of the session once the skill is invoked; `once: true` supported |
| Subagent frontmatter `hooks` | While that subagent runs; `Stop` becomes `SubagentStop` |
| Agent SDK `options.hooks` | Callback functions in the SDK host |

Sources: [hooks reference](https://code.claude.com/docs/en/hooks); [plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference); [subagents](https://code.claude.com/docs/en/sub-agents); [Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks)

- Hooks merge across levels rather than replacing each other. Managed hooks cannot be removed ([hooks reference](https://code.claude.com/docs/en/hooks); [settings reference](https://code.claude.com/docs/en/settings-reference)).
- Settings, managed, and plugin hooks also fire inside subagents, with `agent_id` and `agent_type` in the input ([hooks reference](https://code.claude.com/docs/en/hooks)).
- Identical handlers defined in more than one settings file run once ([hooks reference](https://code.claude.com/docs/en/hooks)).
- `disableAllHooks` turns all hooks off, but cannot disable managed hooks unless set in managed settings. `allowManagedHooksOnly` blocks user, project, local, and plugin hooks. `allowedHttpHookUrls` and `httpHookAllowedEnvVars` constrain HTTP hooks ([hooks reference](https://code.claude.com/docs/en/hooks)).
- SDK callback hooks (e.g. Python `HookMatcher(matcher="Write|Edit", hooks=[cb])`) run alongside settings-file command hooks when `settingSources` includes those settings ([Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks)).

## Format

Shape in settings: `"hooks": { "<Event>": [ { "matcher": "...", "hooks": [ { "type": "...", ... } ] } ] }` ([settings reference](https://code.claude.com/docs/en/settings-reference)).

### Events

From the [hooks reference](https://code.claude.com/docs/en/hooks); addition versions from the [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md):

| Group | Event | Matcher values / notes |
| :- | :- | :- |
| Session | `SessionStart` | startup / resume / clear / compact / fork |
| Session | `Setup` | Fires on `--init-only`, or `--init` / `--maintenance` in `-p`; matchers init / maintenance |
| Session | `SessionEnd` | clear / resume / logout / prompt_input_exit / other |
| Turn | `UserPromptSubmit` | No matcher. Also fires on turns Claude Code starts itself |
| Turn | `UserPromptExpansion` | When a typed command expands; can block; matcher is the command name |
| Turn | `Stop` | No matcher |
| Turn | `StopFailure` | On API errors; rate_limit, overloaded, authentication_failed, …, cloud_credential_error, unknown |
| Agentic loop | `PreToolUse` | Tool event (matches tool names, see [Matchers](#matchers)) |
| Agentic loop | `PermissionRequest` | Tool event |
| Agentic loop | `PermissionDenied` | Fires on auto-mode denials |
| Agentic loop | `PostToolUse` | Tool event |
| Agentic loop | `PostToolUseFailure` | Tool event |
| Agentic loop | `PostToolBatch` | No matcher. After a parallel batch, before the next model call |
| Agents and tasks | `SubagentStart`, `SubagentStop` | Matcher values not recorded |
| Agents and tasks | `TaskCreated`, `TaskCompleted`, `TeammateIdle` | No matcher |
| Context and config | `InstructionsLoaded` | CLAUDE.md or `.claude/rules` loaded |
| Context and config | `ConfigChange` | user_settings, project_settings, local_settings, policy_settings, skills |
| Context and config | `CwdChanged` | No matcher |
| Context and config | `DirectoryAdded` | v2.1.219 |
| Context and config | `FileChanged` | Matcher lists filenames to watch |
| Context and config | `PreCompact`, `PostCompact` | manual / auto |
| Context and config | `PreModelSwitch`, `PostModelSwitch` | Added in v2.1.251 |
| Worktrees | `WorktreeCreate` | No matcher. Replaces default git behavior; prints a path |
| Worktrees | `WorktreeRemove` | No matcher |
| MCP | `Elicitation`, `ElicitationResult` | — |
| UI | `Notification` | permission_prompt, idle_prompt, auth_success, elicitation_*, agent_needs_input, agent_completed, quota_auto_resume_* |
| UI | `MessageDisplay` | No matcher. Display-only rewrite of streamed text; added in v2.1.152 |

### Handler types and support by event

| Event set | Supported handler types |
| :- | :- |
| PermissionDenied, PostToolBatch, PostToolUse, PostToolUseFailure, PreToolUse, Stop, SubagentStop, TaskCompleted, TaskCreated, TeammateIdle, UserPromptExpansion, UserPromptSubmit | All five: `command`, `http`, `mcp_tool`, `prompt`, `agent` |
| PermissionRequest | All except `agent` |
| ConfigChange, CwdChanged, DirectoryAdded, Elicitation, ElicitationResult, FileChanged, InstructionsLoaded, MessageDisplay, Notification, PostCompact, PostModelSwitch, PreCompact, PreModelSwitch, SessionEnd, StopFailure, SubagentStart, WorktreeCreate, WorktreeRemove | `command`, `http`, `mcp_tool` |
| SessionStart, Setup | `command`, `mcp_tool` (mcp_tool is skipped at launch because servers are not yet connected) |

Source: [hooks reference](https://code.claude.com/docs/en/hooks)

### Matchers

From the [hooks reference](https://code.claude.com/docs/en/hooks):

- `*`, `""`, or omitted matches all.
- Only letters, digits, `_`, `-`, space, `,`, and `|`: exact names or a list (`Edit|Write`, `Edit, Write`).
- Anything else: an unanchored JavaScript regex (`^Notebook`, `mcp__memory__.*`).
- MCP tools are named `mcp__<server>__<tool>`; plugin MCP tools are `mcp__plugin_<plugin>_<server>__<tool>`. `mcp__memory` alone matches nothing.
- Events with no matcher support: UserPromptSubmit, PostToolBatch, Stop, TeammateIdle, TaskCreated, TaskCompleted, WorktreeCreate, WorktreeRemove, MessageDisplay, CwdChanged.

### Handler fields

| Field | Applies to | Meaning | Default |
| :- | :- | :- | :- |
| `type` | All | `command`, `http`, `mcp_tool`, `prompt`, `agent` | — |
| `if` | All | One permission rule, e.g. `"Bash(git *)"` or `"Edit(*.ts)"`. Evaluated only on tool events; best-effort | — |
| `timeout` | All | Seconds | 600 for command / http / mcp_tool; 30 for prompt; 60 for agent. Lowered to 30 on UserPromptSubmit and Pre/PostModelSwitch, 10 on MessageDisplay. SessionEnd hooks share a 1.5 s budget, raised up to 60 s if configured |
| `statusMessage` | All | Status text | — |
| `once` | All | Run once; honored only in skill frontmatter | — |
| `command` | command | Shell command | — |
| `args` | command | Exec form with no shell | — |
| `async` | command | Run without blocking | `false` |
| `asyncRewake` | command | Async hook that wakes Claude on exit 2 | — |
| `shell` | command | `bash` or `powershell` | — |
| `url` | http | Endpoint (input JSON is the POST body) | — |
| `headers` | http | Request headers | — |
| `allowedEnvVars` | http | Required for `$VAR` interpolation in headers | — |
| `server`, `tool`, `input` | mcp_tool | MCP tool to call; `input` supports `${tool_input.file_path}`-style substitution | — |
| `prompt` | prompt, agent | Prompt; `$ARGUMENTS` is the input JSON | — |
| `model` | prompt, agent | Model | Background model (prompt hooks) |
| `continueOnBlock` | prompt | On PreToolUse, return the reason to Claude instead of ending the turn | `false` |

Source: [hooks reference](https://code.claude.com/docs/en/hooks)

Command placeholders: `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`. Plugin hooks also get `CLAUDE_PLUGIN_OPTION_<KEY>` for `userConfig` values ([hooks reference](https://code.claude.com/docs/en/hooks); [plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference)).

### Input JSON

From the [hooks reference](https://code.claude.com/docs/en/hooks):

- Command hooks receive it on stdin; HTTP hooks receive it as the POST body.
- Common fields: `session_id`, `prompt_id` (v2.1.196+), `transcript_path`, `cwd`, `scratchpad_dir` (v2.1.257+), `permission_mode`, `effort.level`, `hook_event_name`, plus `agent_id` / `agent_type` inside subagents or with `--agent`.
- Tool events add `tool_name`, `tool_input`, and `tool_use_id`.
- Stop adds `stop_hook_active`, `last_assistant_message`, `background_tasks`, and `session_crons`.

### Exit codes

From the [hooks reference](https://code.claude.com/docs/en/hooks):

| Exit code | Meaning |
| :- | :- |
| 0 | Success; use this when printing JSON. Stdout is added as context only for UserPromptSubmit, UserPromptExpansion, SessionStart, and PostModelSwitch; elsewhere it goes to the debug log |
| 2 | Blocking error. Stderr (or the JSON reason) is the message; JSON `allow` cannot override it |
| Other (incl. 1) | Non-blocking error; Claude Code proceeds |
| 127 (missing script) | Non-blocking; silently disables the gate |

Effect of exit 2 by event:

| Event | Effect |
| :- | :- |
| PreToolUse | Blocks the tool call |
| UserPromptSubmit | Rejects the prompt |
| Stop, SubagentStop | Forces Claude to continue |
| TaskCreated | Rolls back the task |
| PreCompact | Blocks compaction |
| ConfigChange | Blocks the change (except policy_settings) |
| PostToolBatch | Stops the loop |
| PreModelSwitch | Blocks the switch |
| PermissionRequest | Ignored |
| PostToolUse | Only shows stderr to Claude |

- On events where exit 2 blocks, JSON cannot override that block; valid fields are still read. For other exit codes in the standard decision model, valid JSON determines the decision. `PermissionRequest` uses its separate decision object ([hooks reference](https://code.claude.com/docs/en/hooks), rechecked 2026-10-05).
- WorktreeCreate and WorktreeRemove fail on any non-zero exit code.
- A timed-out `PreToolUse` command, HTTP or MCP hook continues normal permission flow; an SDK callback timeout blocks. `PermissionRequest` ignores exit 2 and needs structured JSON denial. Security semantics rechecked 2026-10-05 ([hooks reference](https://code.claude.com/docs/en/hooks)).

### JSON output and decision control

From the [hooks reference](https://code.claude.com/docs/en/hooks):

| Field | Applies to | Meaning |
| :- | :- | :- |
| `continue` | All | `false` stops Claude |
| `stopReason` | All | Reason shown when stopping |
| `systemMessage` | All | Message to the user |
| `suppressOutput` | All | Accepted but has no effect |
| `terminalSequence` | All | Allowlist of OSC 0/1/2/9/99/777 and BEL |
| `additionalContext` | Several | Arrives as a system reminder. Each string capped at 10,000 chars; overflow is saved to a file and a 2,000-char preview is passed |
| `decision: "block"` + `reason` | UserPromptSubmit, UserPromptExpansion, PostToolUse, PostToolUseFailure, PostToolBatch, Stop, SubagentStop, ConfigChange, PreCompact | Block |
| `hookSpecificOutput.permissionDecision` | PreToolUse | `allow` / `deny` / `ask` / `defer`; precedence deny > defer > ask > allow. Also `permissionDecisionReason`, `updatedInput`, `additionalContext` |
| `hookSpecificOutput.decision.behavior` | PermissionRequest | `allow` / `deny`, plus `updatedInput`, `updatedPermissions`, `message`, `interrupt` |
| `updatedToolOutput`, `classifierContext` | PostToolUse | Replace tool output; context for the classifier |
| `additionalContext`, `initialUserMessage`, `sessionTitle`, `watchPaths`, `reloadSkills` | SessionStart | Session setup |
| Path on stdout / `hookSpecificOutput.worktreePath` (HTTP) | WorktreeCreate | Worktree location |
| `retry: true` | PermissionDenied | Retry |

- PreToolUse: deny and ask permission rules are still evaluated regardless of the hook decision. `defer` works only in `-p`; the run exits with `stop_reason: "tool_deferred"`.
- Stop loop guard: `stop_hook_active` plus a cap of 8 consecutive continuations (`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`).

### Prompt and agent hooks

From the [hooks reference](https://code.claude.com/docs/en/hooks):

- Prompt hooks expect the model to return `{"ok": bool, "reason": "...", "impossible": bool}`. They default to the background model.
- On PreToolUse, `ok: false` denies the call and by default ends the turn (since v2.1.210). `continueOnBlock: true` returns the reason to Claude instead.
- Agent hooks are "experimental": a subagent with Read, Grep, Glob, and similar tools, up to 50 turns, returning `{ok}`.

## Loading and invocation

- All matching handlers for an event run in parallel ([hooks reference](https://code.claude.com/docs/en/hooks)).
- Settings files are hot-reloaded, including `hooks` ([settings](https://code.claude.com/docs/en/settings)).
- Interaction with permissions: PreToolUse hooks run before the permission prompt. They can deny, force ask, or allow, but never override deny or ask rules. Exit 2 blocks even when an allow rule matches ([permissions](https://code.claude.com/docs/en/permissions)). See [permissions-and-sandbox.md](permissions-and-sandbox.md).
- Async hooks (`async: true`, command type only) cannot block. Their `additionalContext` and `systemMessage` are delivered on the next turn. They are killed at teardown in `-p`, and there is no deduplication ([hooks reference](https://code.claude.com/docs/en/hooks)).
- Hooks run outside the sandbox ([sandboxing](https://code.claude.com/docs/en/sandboxing)).
- `/hooks` is a read-only browser of configured hooks ([hooks reference](https://code.claude.com/docs/en/hooks)).
- Context cost: stdout reaches Claude only on UserPromptSubmit, UserPromptExpansion, SessionStart, and PostModelSwitch; elsewhere context arrives only through fields such as `additionalContext` ([hooks reference](https://code.claude.com/docs/en/hooks)).

## Example

`.claude/settings.json` ([hooks reference](https://code.claude.com/docs/en/hooks)):

```json
{ "hooks": { "PostToolUse": [ { "matcher": "Edit|Write",
  "hooks": [ { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/check-style.sh", "args": [] } ] } ] } }
```

## Limits and gotchas

- Security: "Command hooks execute shell commands with your full user permissions" ([hooks reference](https://code.claude.com/docs/en/hooks)).
- Interactive sessions hold back settings-file hooks until the workspace trust dialog is accepted. In `-p` and SDK sessions the folder is treated as trusted, so a repo's `.claude/settings.json` hooks run. Mitigations: `--bare` or `--settings '{"disableAllHooks": true}'` ([hooks reference](https://code.claude.com/docs/en/hooks)).
- Frontmatter hooks in project subagents require trust of the agent file's folder (v2.1.218+); `-p` does not count as trust ([hooks reference](https://code.claude.com/docs/en/hooks)).
- Plugin agents ignore their `hooks` field ([subagents](https://code.claude.com/docs/en/sub-agents)).
- Exit 1 does not block: "Claude Code treats exit code 1 as a non-blocking error and proceeds… If your hook is meant to enforce a policy, use `exit 2`" ([hooks reference](https://code.claude.com/docs/en/hooks)).
- The `if` field is best-effort: "use the permission system rather than a hook to enforce a hard allow or deny" ([hooks reference](https://code.claude.com/docs/en/hooks)).
- The top-level `decision` / `reason` (`approve` / `block`) are deprecated for PreToolUse; use `hookSpecificOutput.permissionDecision` ([hooks reference](https://code.claude.com/docs/en/hooks)).
- Hooks in skill frontmatter persist for the whole session after invocation, not just the skill's turn ([hooks reference](https://code.claude.com/docs/en/hooks)).
- An AGENTS.md loaded through the "Project instructions" setting does not fire `InstructionsLoaded` ([memory](https://code.claude.com/docs/en/memory)).
- Mods (v2.1.287+) answering `tool.check` can override ask rules and non-managed hook blocks ([permissions](https://code.claude.com/docs/en/permissions)).
- Version history: HTTP hooks added in v2.1.63; `mcp_tool` hooks in v2.1.118; `MessageDisplay` in v2.1.152; `DirectoryAdded` in v2.1.219; `PreModelSwitch`/`PostModelSwitch` in v2.1.251 ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- Inference (from the research notes), common mistakes: exit 1 instead of 2 for a policy gate; matching `mcp__server` without `__.*`; treating `if` as a security boundary; assuming `-p` respects workspace trust.
- Best practices from the docs: validate input, quote variables, block path traversal, use absolute paths, skip sensitive files ([hooks reference](https://code.claude.com/docs/en/hooks)).
- Gap (research notes): not every per-event input schema was read in full (PreModelSwitch naming, FileChanged watch semantics, Elicitation fields, MessageDisplay output).
- Gap (research notes): the hooks guide (`/docs/en/hooks-guide`) was only skimmed through the reference, and the mods docs (JavaScript function hooks) were not read beyond the one-line description.

## Sources

- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/agent-sdk/hooks
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/settings-reference
- https://code.claude.com/docs/en/permissions
- https://code.claude.com/docs/en/sandboxing
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/plugins/manifest-reference
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
