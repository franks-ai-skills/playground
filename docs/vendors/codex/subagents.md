# Agents (subagents)

Codex can spawn subagents: separate agent threads that do part of a task and return a summary to the main thread. This keeps noisy intermediate output (exploration, logs, tests) out of the main thread to avoid "context pollution" and "context rot" ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)). Multi-agent is stable and on by default; Codex ships three built-in agent types, and custom agents are standalone TOML files that act as configuration layers for the spawned session.

## Locations and scopes

| Item | Location | Notes |
|---|---|---|
| Personal custom agents | `~/.codex/agents/*.toml` | One agent per file |
| Project custom agents | `.codex/agents/*.toml` | One agent per file |
| Role declarations | `[agents.<name>]` in `config.toml` with `config_file` and `description` | `config_file` is a TOML layer path, relative to the declaring config ([Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md)) |
| Global limits and defaults | `[agents]` in `config.toml` | See Format |
| Feature flag | `features.multi_agent` | Admins can pin it in `requirements.toml` ([Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md)) |

Sources: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md).

### Built-in agent types

| Type | Purpose |
|---|---|
| `default` | General-purpose fallback |
| `worker` | Implementation and fixes |
| `explorer` | Read-heavy exploration |

A custom agent whose `name` matches a built-in replaces it ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)).

## Format

### Spawn tools

`features.multi_agent`: "Enable multi-agent collaboration tools (`spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, and `close_agent`) (stable; on by default)." ([Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md))

| Tool | Notes |
|---|---|
| `spawn_agent` | Starts a subagent. In hook matchers it also matches `Agent` ([Hooks](https://learn.chatgpt.com/docs/hooks.md)) |
| `send_input` | |
| `resume_agent` | |
| `wait_agent` | |
| `close_agent` | |

The JSON schemas of the tool arguments are not documented publicly (see Limits and gotchas).

### Custom agent file

| Key | Required | Meaning |
|---|---|---|
| `name` | Yes | The agent name. It is the source of truth; the file name does not matter |
| `description` | Yes | When to use this agent |
| `developer_instructions` | Yes | Instructions for the agent |
| Any other `config.toml` key | No | For example `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config` |

Codex loads these files "as configuration layers for spawned sessions", and "the format may evolve" ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)).

### `[agents]` config

| Key | Meaning | Default |
|---|---|---|
| `agents.enabled` | Enable subagents | `true` |
| `agents.max_concurrent_threads_per_session` | Cap on concurrent threads, excluding the primary thread. `agents.max_threads` is a legacy alias | "Codex chooses the default" |
| `agents.default_subagent_model` | Default model for subagents | |
| `agents.default_subagent_reasoning_effort` | Default reasoning effort for subagents | |
| `agents.interrupt_message` | | `true` |
| `agents.<name>.config_file` | Role declaration: path to a TOML layer, relative to the declaring config | |
| `agents.<name>.description` | Role description | |

"Scalar setting names are reserved and can't be used as custom role names." Sources: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md); [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md).

## Loading and invocation

### When Codex spawns

- "Current local Codex releases spawn agents after a direct request or applicable project or skill instruction", for example "spawn two agents" or "use one agent per point" ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)). See [instructions.md](instructions.md) and [skills.md](skills.md).
- Codex handles orchestration, waits for all requested results, and returns one consolidated response ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)).
- The docs recommend parallel agents for read-heavy work and caution with parallel writes ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)).
- Context cost: subagents "consume more tokens than comparable single-agent runs" ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)).

### Model, effort and setting resolution

1. A `model` or `model_reasoning_effort` set in the custom agent file wins.
2. Otherwise: the explicit value passed at spawn, then the `[agents]` default, then the parent's value.
3. If a model is chosen without an effort, that model's default effort applies.
4. Unspecified settings (`sandbox_mode`, `mcp_servers`, `skills.config`) are inherited from the parent.

Source: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md).

### Sandbox and approvals

- Subagents inherit the parent sandbox policy and live runtime overrides (`/permissions`, `--yolo`), "even if the selected custom agent file sets different defaults" ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)). See [permissions-and-sandbox.md](permissions-and-sandbox.md).
- In the CLI, approval requests from inactive threads show the source thread label, and `o` opens that thread. In non-interactive flows, an action that needs new approval fails and the error goes back to the parent ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)).

### UI

- CLI: `/agent` or `/subagents` switches threads.
- IDE extension: a background-agent panel above the composer.
- `codex agents` ("Browse all agent sessions on the shared local app-server daemon") is the "agent command center". 0.160.0 added history pagination to it.
- Subagent activity appears in the ChatGPT desktop app, Codex CLI and the IDE extension.

Sources: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md); local `codex agents --help`; [rust-v0.160.0](https://github.com/openai/codex/releases/tag/rust-v0.160.0).

### Hooks

Hooks see subagents through `SubagentStart` and `SubagentStop` (matcher: agent type), and `spawn_agent` also matches `Agent` in `PreToolUse`/`PostToolUse` matchers. `Interrupt` and `SessionEnd` do not fire for subagents, and subagents get the parent's `session_id` ([Hooks](https://learn.chatgpt.com/docs/hooks.md)). See [hooks.md](hooks.md).

### Shipped review agent

The `review-agent` system skill is meant for delegated reviews: "Use when another agent delegates review of uncommitted changes, a base-branch diff, a commit...". It is read-only, must not delegate further, and sets `policy.allow_implicit_invocation: false` (local `~/.codex/skills/.system/review-agent/`).

### Cloud best-of-N

`codex cloud exec --attempts 1-4` (default 1) is "Number of assistant attempts (best-of-N) Codex cloud should run". It requires `--env ENV_ID`. `codex cloud list --json` returns `attempt_total` per task ([CLI command reference](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli); local `codex cloud --help`). See [automation.md](automation.md).

### Worktrees for parallel work

The desktop app runs parallel chats in Git worktrees (detached HEAD by default), and "Handoff" moves a chat between Local and Worktree. The CLI has `--worktree` ("Run the session in a new managed Git worktree"), and the `worktrees` feature is stable and on ([Worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees.md); local `codex --help`, `codex features list`).

### External orchestration

The old pattern of running Codex as an MCP server orchestrated by the Agents SDK no longer works, because `codex mcp-server` was removed ([Codex SDK](https://learn.chatgpt.com/docs/codex-sdk.md)). Inference: use the Codex SDK (TypeScript/Python) or the app-server JSON-RPC protocol instead; see [automation.md](automation.md) and [mcp.md](mcp.md).

## Example

```toml
# .codex/agents/reviewer.toml
name = "reviewer"
description = "PR reviewer focused on correctness, security, and missing tests."
model = "gpt-6.1-sol"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"
developer_instructions = """
Review code like an owner. Prioritize correctness, security, behavior regressions, and missing test coverage.
"""
```

Source: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md). Subagents inherit the parent sandbox policy and live runtime overrides "even if the selected custom agent file sets different defaults", so the file's `sandbox_mode` may not take effect.

## Limits and gotchas

- **No tool allowlist field.** Inference: a custom agent is a partial `config.toml` plus `name`, `description` and `developer_instructions`. Tool scope is controlled through `sandbox_mode`, `mcp_servers` and `skills.config`.
- **Parent sandbox wins over the agent file.** Subagents inherit the parent sandbox policy and live runtime overrides even when the agent file sets different defaults ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)).
- **No implicit spawning by default.** Codex spawns only on a direct request or an `AGENTS.md`/skill instruction.
- **Agents SDK + `codex mcp-server` is obsolete.** Older OpenAI guides that show this pattern no longer apply ([Codex SDK](https://learn.chatgpt.com/docs/codex-sdk.md)).
- **Feature flags (local 0.159.2):** `multi_agent` stable/true, `multi_agent_v2` stable/false, `multi_agent_mode` removed, `enable_fanout` removed, `agent_message_board` under development/false.
- **Gap:** the default of `max_concurrent_threads_per_session` ("Codex chooses the default") and any nesting-depth limit are not documented.
- **Gap:** what `multi_agent_v2` changes is not documented on the pages read.
- **Gap:** the JSON schemas of the `spawn_agent`, `send_input` and `wait_agent` tool arguments are not documented publicly.
- **Format stability.** The custom agent file format "may evolve" ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)).

## Sources

- https://learn.chatgpt.com/docs/agent-configuration/subagents.md
- https://learn.chatgpt.com/docs/config-file/config-reference.md
- https://learn.chatgpt.com/docs/hooks.md
- https://learn.chatgpt.com/docs/developer-commands.md?surface=cli
- https://learn.chatgpt.com/docs/environments/git-worktrees.md
- https://learn.chatgpt.com/docs/codex-sdk.md
- https://github.com/openai/codex/releases/tag/rust-v0.160.0
