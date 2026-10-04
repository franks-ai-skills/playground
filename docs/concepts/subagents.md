# Subagents

A subagent is a separate agent instance that the main agent starts for a delegated task. It runs in its own context window, does the work, and returns one result (a report or summary) to its caller. Subagents keep noisy intermediate output such as search results, logs and test runs out of the main context, and they allow independent tasks to run in parallel. A subagent definition is a named, reusable configuration (instructions, model and capability scope) that the harness applies when it spawns that kind of subagent.

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Definition format | Markdown with YAML frontmatter; body is the system prompt ([subagents][cc-sub]) | TOML file; `developer_instructions` holds the prompt; the file is applied as a config layer for the spawned session ([subagents][cx-sub]) | Markdown with YAML frontmatter (body is the prompt), or JSON under the `agent` config key ([subagents][oc-sub]) |
| Project location | `.claude/agents/`, recursive, walking up to the repo root; closest wins ([subagents][cc-sub]) | `.codex/agents/*.toml` ([subagents][cx-sub]) | `.opencode/agents/` (`{agent,agents}/**/*.md` in config dirs) ([subagents][oc-sub]) |
| User location | `~/.claude/agents/` ([subagents][cc-sub]) | `~/.codex/agents/*.toml` ([subagents][cx-sub]) | `~/.config/opencode/agents/` ([subagents][oc-sub]) |
| Other sources | Managed settings, `--agents` JSON (session only), plugins, `--add-dir` dirs, SDK `agents` option ([subagents][cc-sub]) | `[agents.<name>]` role declarations in `config.toml` pointing to a `config_file` ([subagents][cx-sub]) | `agent` key in any config layer ([subagents][oc-sub]) |
| Identity | `name` field; in plugins, subfolders join the ID ([subagents][cc-sub]) | `name` field; filename does not matter ([subagents][cx-sub]) | Relative path without extension, e.g. `team/review` ([subagents][oc-sub]) |
| Required fields | `name`, `description`; invalid files skipped silently ([subagents][cc-sub]) | `name`, `description`, `developer_instructions` ([subagents][cx-sub]) | `description` (docs say required; schema optional) ([subagents][oc-sub]) |
| Model / effort | `model` (alias, full ID or `inherit`), `effort` ([subagents][cc-sub]) | `model`, `model_reasoning_effort` ([subagents][cx-sub]) | `model` (`provider/model`), `variant`, provider options ([subagents][oc-sub]) |
| Capability scope | `tools` allowlist, `disallowedTools` denylist, `permissionMode` ([subagents][cc-sub]) | No tool allowlist; `sandbox_mode`, `mcp_servers`, `skills.config`. Parent sandbox and runtime overrides win over the file ([subagents][cx-sub]) | `permission` rules merged over global rules ([subagents][oc-sub]) |
| Per-agent MCP servers | `mcpServers` (reference or inline) ([subagents][cc-sub]) | `mcp_servers` ([subagents][cx-sub]) | Not recorded beyond permission rules ([subagents][oc-sub]) |
| Built-in types | Explore (read-only), Plan (read-only), general-purpose, claude, fork, statusline-setup, claude-code-guide ([subagents][cc-sub]) | `default`, `worker`, `explorer` ([subagents][cx-sub]) | General, Explore (read-only), Scout (experimental) ([subagents][oc-sub]) |
| Override a built-in | Not recorded ([subagents][cc-sub]) | A custom agent with the same `name` replaces it ([subagents][cx-sub]) | Configure under the built-in's key ([subagents][oc-sub]) |
| Spawn mechanism | Agent tool (formerly Task) ([subagents][cc-sub]) | `spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, `close_agent` ([subagents][cx-sub]) | `task` tool with `subagent_type` ([subagents][oc-sub]) |
| When the model delegates | Automatically by description ("use proactively" encourages it), or on request ([subagents][cc-sub]) | Only on a direct request or an `AGENTS.md`/skill instruction ([subagents][cx-sub]) | By description through the `task` tool ([subagents][oc-sub]) |
| User invocation | Natural language, `@agent-<name>` mention ([subagents][cc-sub]) | Direct request ("spawn two agents") ([subagents][cx-sub]) | `@name` ([subagents][oc-sub]) |
| What the subagent receives | Own prompt plus environment, delegation message, CLAUDE.md (except Explore/Plan), git status, preloaded skills; no conversation history ([subagents][cc-sub]) | Not recorded beyond inheritance of unspecified settings from the parent ([subagents][cx-sub]) | Not recorded ([subagents][oc-sub]) |
| Result | Final report, marked as subagent output with no user authority ([subagents][cc-sub]) | Summary; Codex waits for all requested results and returns one consolidated response ([subagents][cx-sub]) | Work runs in a child session; result format not recorded ([subagents][oc-sub]) |
| Model resolution | Spawn parameter > frontmatter > `CLAUDE_CODE_SUBAGENT_MODEL` > main model ([subagents][cc-sub]) | Agent file > spawn value > `[agents]` default > parent ([subagents][cx-sub]) | Own `model`, else the invoking agent's model ([subagents][oc-sub]) |
| Foreground / background | Background by default in interactive sessions; Claude chooses in `-p`/SDK ([subagents][cc-sub]) | Not recorded; threads switchable with `/agent` ([subagents][cx-sub]) | Background subagents behind an experimental flag ([subagents][oc-sub]) |
| Resume a finished subagent | `SendMessage` with agent ID or name ([subagents][cc-sub]) | `resume_agent`, `send_input` ([subagents][cx-sub]) | `task_id` parameter ([subagents][oc-sub]) |
| Nesting | Depth 3 below main by default; `1` disables nesting ([subagents][cc-sub]) | Not documented ([subagents][cx-sub]) | `subagent_depth`, default `1` (subagents cannot spawn subagents) ([subagents][oc-sub]) |
| Concurrency | 20 running subagents by default ([subagents][cc-sub]) | `agents.max_concurrent_threads_per_session`; default not documented ([subagents][cx-sub]) | Not recorded ([subagents][oc-sub]) |
| Approvals inside subagents | Background subagent prompts surface in the main session ([subagents][cc-sub]) | Prompts from inactive threads are labeled; in non-interactive runs the action fails and the error returns to the parent ([subagents][cx-sub]) | `opencode run` answers subagent permission requests since v1.18.20 ([subagents][oc-sub]) |
| Restrict which agents the model may spawn | `Agent(Name)` permission rules ([subagents][cc-sub]) | Not recorded ([subagents][cx-sub]) | `permission.task` globs; denied agents leave the tool description ([subagents][oc-sub]) |
| Context cost of definitions | Descriptions in context; warning above 15,000 tokens combined ([subagents][cc-sub]) | Not recorded; subagent runs "consume more tokens than comparable single-agent runs" ([subagents][cx-sub]) | Allowed subagents listed in the `task` tool description ([subagents][oc-sub]) |
| Hook events | `SubagentStart`, `SubagentStop` ([hooks][cc-hooks]) | `SubagentStart`, `SubagentStop` (matcher: agent type) ([subagents][cx-sub]) | None recorded ([hooks][oc-hooks]) |

## Generalized model

### Entities

- **Subagent definition.** A named, reusable configuration stored as one file per definition:

  | Field | Meaning | Required |
  | --- | --- | --- |
  | name | Identifier the spawn call and the user refer to | Yes |
  | description | When to use this subagent; the main agent reads it to choose a type | Yes |
  | instructions | System or developer prompt for the subagent | Yes |
  | model | Model override | No |
  | reasoning effort | Effort override | No |
  | capability scope | Which tools, sandbox level or permission mode apply | No |
  | MCP servers | Servers available to this subagent only | No |

- **Built-in types.** Each harness ships at least a general-purpose type and a read-only exploration type.
- **Subagent instance.** A running agent created from a definition (or a built-in type) plus a delegation message. It has its own context window and an ID.
- **Result.** The single message the instance returns to its caller.

### Scopes

Project (committed with the repository) and user (all projects on one machine) in both leads. Managed, plugin and session-only definitions exist in Claude Code only.

### Lifecycle

1. **Load definitions** at session start; edits are picked up during the session in Claude Code, not recorded for Codex.
2. **Spawn.** The main agent calls a spawn tool with a type and a delegation message. The harness resolves the model and settings and starts the instance.
3. **Run.** The instance works in its own context. It does not see the caller's conversation history. Approval requests it raises surface to the user through the main session, or fail back to the parent in non-interactive runs.
4. **Return.** The instance returns one result. The caller sees the result, not the intermediate output.
5. **Resume (optional).** The caller can send a follow-up message to a finished instance by ID; its history is retained.
6. **Close.** The instance ends; in Codex an explicit close tool exists.

### Invocation model

- **Model-initiated.** The main agent decides to delegate. Trigger policy differs: Claude Code delegates automatically based on descriptions; Codex delegates only when the user or an instruction file or skill asks for it.
- **User-initiated.** The user names the subagent or asks for delegation in the prompt.
- **Parallelism.** The main agent can spawn several instances at once, bounded by a concurrency limit, and waits for their results.

### Inheritance

Settings a definition leaves unspecified come from the parent session. Permissions are the main conflict point: in Claude Code the definition's `tools` and `permissionMode` apply; in Codex the parent's sandbox policy and live overrides win over the definition file.

### Mapping

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Subagent definition | Subagent file (`.claude/agents/*.md`) | Custom agent file (`.codex/agents/*.toml`) | Agent with `mode: subagent` (`.opencode/agents/*.md`) |
| name | `name` | `name` | File path |
| description | `description` | `description` | `description` |
| instructions | Markdown body | `developer_instructions` | Markdown body / `prompt` |
| model | `model` | `model` | `model` |
| reasoning effort | `effort` | `model_reasoning_effort` | `variant` / provider options |
| capability scope | `tools`, `disallowedTools`, `permissionMode` | `sandbox_mode` (parent wins) | `permission` |
| MCP servers | `mcpServers` | `mcp_servers` | — |
| Spawn tool | Agent tool | `spawn_agent` | `task` |
| Resume | `SendMessage` | `resume_agent` / `send_input` | `task_id` |
| General-purpose built-in | general-purpose | `default` (also `worker`) | General |
| Read-only exploration built-in | Explore | `explorer` | Explore |
| Concurrency limit | `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` | `agents.max_concurrent_threads_per_session` | — |
| Default subagent model | `CLAUDE_CODE_SUBAGENT_MODEL` | `agents.default_subagent_model` | Invoking agent's model |
| Start / stop hook events | `SubagentStart` / `SubagentStop` | `SubagentStart` / `SubagentStop` | — |

## Portability

No definition file is shared. Each harness reads its own format from its own directory: Markdown in `.claude/agents/`, TOML in `.codex/agents/`, Markdown in `.opencode/agents/`. The OpenCode pages record no reading of `.claude/agents/` ([subagents][oc-sub]). A portable subagent needs one file per harness, generated from a single source or kept in sync by hand. Symlinks do not help because the formats differ.

Fields that carry over with a rename:

- `name`, `description`: identical in both leads. OpenCode takes the name from the file path, so name the file after the agent.
- Instructions: Markdown body (Claude Code, OpenCode) ↔ `developer_instructions` string (Codex).
- Model and effort: the values are vendor model names, so they do not port as values, only as fields.
- MCP servers: `mcpServers` ↔ `mcp_servers`; server definitions follow each harness's MCP format.

Traps:

- **Delegation does not happen by itself in Codex.** A description that says "use proactively" triggers automatic delegation in Claude Code but not in Codex. To get delegation in both, name the subagent explicitly in the instruction file or skill that should trigger it ([subagents][cx-sub]).
- **Read-only definitions are not enforced the same way.** Claude Code honors a restricted `tools` list. In Codex, `sandbox_mode = "read-only"` in the agent file may not apply, because the parent sandbox and runtime overrides win ([subagents][cx-sub]). Do not rely on a definition file alone to keep a Codex subagent from writing.
- **Model precedence is reversed.** In Claude Code a model passed at spawn time beats the definition; in Codex the definition beats the spawn value ([subagents][cc-sub], [subagents][cx-sub]).
- **Nesting limits differ.** Claude Code allows 3 levels by default; OpenCode allows none beyond the first by default; Codex documents no limit ([subagents][cc-sub], [subagents][oc-sub], [subagents][cx-sub]). Design delegation trees one level deep if they must run everywhere.
- **Hook payloads differ.** Codex subagents receive the parent's `session_id`, and `agent_id`/`agent_type` appear only in subagent events. In Claude Code all hooks inside a subagent carry `agent_id` and `agent_type` ([hooks][cx-hooks], [hooks][cc-hooks]).
- **Name collisions with built-ins.** In Codex a custom agent named `default`, `worker` or `explorer` replaces the built-in ([subagents][cx-sub]); Claude Code's behavior for such a collision is not recorded.
- **Format stability.** Codex states that the custom agent file format "may evolve" ([subagents][cx-sub]).

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| Forks (subagent inheriting the full conversation, `/subtask`) | Claude Code | Codex subagents do not inherit conversation context; Codex `/fork` copies a session, not a subagent. |
| Agent teams (lead, teammates, shared task list, mailbox) | Claude Code | Experimental; Codex's `agent_message_board` is under development and off. |
| Subagent `memory` directories | Claude Code | No per-agent persistent memory in Codex. |
| `isolation: worktree` per subagent | Claude Code | Codex worktrees are per session, not per subagent. |
| `background` field, Ctrl+B backgrounding | Claude Code | Codex records no foreground/background control. |
| `maxTurns` | Claude Code | No turn cap in Codex agent files; OpenCode's `steps` is the only counterpart. |
| `skills` preloading | Claude Code | Codex `skills.config` disables skills; it does not preload them. |
| `skills.config` per agent | Codex | Claude Code subagent files have no skill filter. |
| `hooks` scoped to a subagent | Claude Code | Codex agent files are not documented to carry hooks. |
| `omitClaudeMd`, `initialPrompt`, `color`, `experimental.cacheTtl` | Claude Code | No Codex counterparts. |
| Session-wide agent (`claude --agent`, settings `agent`) | Claude Code | No Codex way to run the main session as a custom agent; OpenCode primary agents do not decide. |
| `--agents` JSON, SDK `agents` option (session-only definitions) | Claude Code | No Codex counterpart. |
| `Agent(Name)` spawn restriction rules | Claude Code | No Codex counterpart recorded. |
| Sibling roster, scanning results for instruction-shaped text | Claude Code | Harness internals with no Codex counterpart recorded. |
| `[agents.<name>] config_file` role declarations | Codex | No Claude Code counterpart. |
| `agents.interrupt_message` | Codex | No Claude Code counterpart. |
| `close_agent`, `wait_agent` as explicit tools | Codex | Claude Code has no separate wait or close tool recorded; kept only as lifecycle steps. |
| Agent view (`claude agents`) and `codex agents` | Claude Code, Codex | UI for browsing sessions, not a configuration concept. |
| Primary agents, `mode`, Tab switching | OpenCode | Neither lead has primary agents. |
| `temperature`, `top_p`, `steps`, `hidden`, `permission.task` | OpenCode | No lead counterpart (or only one lead for `steps`). |
| Scout built-in | OpenCode | Experimental, OpenCode only. |

## Sources

- [Claude Code: subagents](../vendors/claude-code/subagents.md)
- [Claude Code: hooks](../vendors/claude-code/hooks.md)
- [Codex: subagents](../vendors/codex/subagents.md)
- [Codex: hooks](../vendors/codex/hooks.md)
- [OpenCode: subagents](../vendors/opencode/subagents.md)
- [OpenCode: hooks](../vendors/opencode/hooks.md)
- [Research notes](../research-notes/agent-harness-configuration/)

[cc-sub]: ../vendors/claude-code/subagents.md
[cc-hooks]: ../vendors/claude-code/hooks.md
[cx-sub]: ../vendors/codex/subagents.md
[cx-hooks]: ../vendors/codex/hooks.md
[oc-sub]: ../vendors/opencode/subagents.md
[oc-hooks]: ../vendors/opencode/hooks.md
