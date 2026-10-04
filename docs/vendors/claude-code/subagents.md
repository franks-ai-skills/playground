# Subagents

A subagent is a Markdown file with YAML frontmatter whose body becomes its system prompt. It runs in its own context window with its own tools and permissions, and returns one final report to the caller. Use one "when a side task would flood your main conversation with search results, logs, or file contents you won't reference again" ([subagents](https://code.claude.com/docs/en/sub-agents)). The Agent tool (renamed from Task in v2.1.63) spawns subagents. Related multi-agent features covered here: forks, background agents, agent teams, and agent view; script-driven orchestration is in [automation.md](automation.md#dynamic-workflows).

## Locations and scopes

Priority, highest first ([subagents](https://code.claude.com/docs/en/sub-agents)):

| Priority | Source | Notes |
| :- | :- | :- |
| 1 | Managed settings `.claude/agents/` | Organization |
| 2 | `--agents` CLI JSON | Session only |
| 3 | Project `.claude/agents/` | Walks up to the repo root; the closest definition wins |
| 4 | User `~/.claude/agents/` | All projects |
| 5 | Plugin `agents/` | See [plugins.md](plugins.md) |

- Directories are scanned recursively. In project and user scopes, identity comes only from `name`. In plugins, subfolders become part of the ID, e.g. `my-plugin:review:security` ([subagents](https://code.claude.com/docs/en/sub-agents)).
- `--add-dir` directories also load agents ([permissions](https://code.claude.com/docs/en/permissions)).
- SDK: `agents` option with `AgentDefinition` (Python `claude_agent_sdk.AgentDefinition`; TypeScript `@anthropic-ai/claude-agent-sdk`). Fields mirror the frontmatter; the Python SDK keeps camelCase keys ([Agent SDK subagents](https://code.claude.com/docs/en/agent-sdk/subagents)).

### Built-in subagents

| Agent | Behavior |
| :- | :- |
| Explore | Read-only (Write and Edit denied). Uses the main model (or the `opus` alias when the main model is Fable on Anthropic auth). Takes a thoroughness level: quick / medium / very thorough. Skips CLAUDE.md and git status. One-shot; cannot be resumed |
| Plan | Read-only, used in plan mode. Skips CLAUDE.md and git status. One-shot; cannot be resumed |
| general-purpose | Every tool available to subagents |
| claude | Catch-all; also the default for background sessions |
| statusline-setup | Sonnet |
| claude-code-guide | Haiku |
| fork | Inherits the full conversation (see [Forks](#forks)) |

Source: [subagents](https://code.claude.com/docs/en/sub-agents)

Controls: `CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1` (v2.1.198+) removes Explore and Plan. `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1` removes all built-ins in `-p`/SDK runs. `permissions.deny: ["Agent(Explore)"]` blocks one type ([subagents](https://code.claude.com/docs/en/sub-agents)).

## Format

Markdown file with YAML frontmatter. Keys are camelCase; unknown fields are ignored; only `name` and `description` are required ([subagents](https://code.claude.com/docs/en/sub-agents)).

| Field | Meaning | Default |
| :- | :- | :- |
| `name` | Identifier. No `:` allowed (v2.1.218+); must not start with `-` | Required |
| `description` | When Claude should delegate | Required |
| `tools` | Allowlist | All subagent tools |
| `disallowedTools` | Denylist, applied first. An entry like `Bash(git push *)` removes the whole tool. MCP patterns `mcp__server` and `mcp__*` supported | — |
| `model` | `sonnet` / `opus` / `haiku` / `fable` / full ID / `inherit` | See model resolution |
| `permissionMode` | `default` / `acceptEdits` / `auto` / `dontAsk` / `bypassPermissions` / `plan` / `manual` (alias for default) | — |
| `maxTurns` | Turn cap; when hit, output is marked partial (v2.1.246+) | — |
| `skills` | Preloads full skill content at startup | — |
| `mcpServers` | Name reference or inline definition (stdio / http / sse / ws) | — |
| `hooks` | Scoped to the subagent; `Stop` becomes `SubagentStop` | — |
| `memory` | `user` / `project` / `local` | — |
| `background` | `true` keeps the subagent in the background | — |
| `omitClaudeMd` | Skip the CLAUDE.md hierarchy (v2.1.271+) | — |
| `effort` | Effort level | — |
| `isolation` | `worktree` | — |
| `color` | red / blue / green / yellow / purple / orange / pink / cyan | — |
| `initialPrompt` | Used only when the agent runs as the main session | — |
| `experimental.cacheTtl` | `5m` or `1h` (v2.1.248+) | — |

Source: [subagents](https://code.claude.com/docs/en/sub-agents)

- Files without `name`, without `description`, or with invalid YAML are skipped silently; the reason goes to the debug log. `claude plugin validate .claude/agents` checks them (v2.1.233+) ([subagents](https://code.claude.com/docs/en/sub-agents)).
- Plugin agents ignore `hooks`, `mcpServers`, `permissionMode`, and `initialPrompt` for security ([subagents](https://code.claude.com/docs/en/sub-agents); [plugin components](https://code.claude.com/docs/en/plugins/components)).

### `--agents` JSON

- Format: `{"name": {"description", "prompt", "tools", ...}}` ([subagents](https://code.claude.com/docs/en/sub-agents)).
- Accepted fields: `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `omitClaudeMd`, `isolation`. `color` and `experimental` are ignored ([subagents](https://code.claude.com/docs/en/sub-agents)).
- In `-p` mode it also accepts a file path (v2.1.281+). `--agents` was introduced in 2.0.0 ([subagents](https://code.claude.com/docs/en/sub-agents); [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).

### Subagent memory

- `memory` stores files at `~/.claude/agent-memory/<name>/` (user), `.claude/agent-memory/<name>/` (project), or `.claude/agent-memory-local/<name>/` (local) ([subagents](https://code.claude.com/docs/en/sub-agents)).
- The first 200 lines / 25KB of that `MEMORY.md` are injected. Read, Write, and Edit are auto-enabled ([subagents](https://code.claude.com/docs/en/sub-agents)).

## Loading and invocation

### Context cost

- Agent descriptions consume context. A warning appears when combined custom-agent descriptions exceed 15,000 tokens ([subagents](https://code.claude.com/docs/en/sub-agents)).
- The file watcher picks up edits within seconds. A newly created `agents` directory and `--add-dir` agents need a restart ([subagents](https://code.claude.com/docs/en/sub-agents)).

### Invocation

From [subagents](https://code.claude.com/docs/en/sub-agents):

- Automatic delegation by description; "use proactively" in a description encourages it.
- Natural language, e.g. "Use the code-reviewer subagent…".
- @-mention: `@"code-reviewer (agent)"`, `@agent-<name>`, or `@agent-<plugin>:<name>`.
- Session-wide: `claude --agent <name>` or `"agent": "<name>"` in settings. The agent's prompt replaces the default system prompt; CLAUDE.md still loads.
- Permission rules: `Agent(Name)`; `Agent(model:opus)` matches a parameter ([permissions](https://code.claude.com/docs/en/permissions)).
- `Agent(worker, researcher)` in `tools` restricts which agent types can be spawned, but only for an agent running as the main thread via `--agent`.

### Model resolution

From [subagents](https://code.claude.com/docs/en/sub-agents):

- Order: per-invocation `model` parameter > frontmatter `model` > `CLAUDE_CODE_SUBAGENT_MODEL` > main model. Before v2.1.251 the environment variable came first.
- `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` (v2.1.257+) forces one model on all subagents, teammates, and workflow agents.
- Subagents inherit the main conversation's extended-thinking setting (v2.1.198+).

### Context isolation and results

From [subagents](https://code.claude.com/docs/en/sub-agents):

- A non-fork subagent starts with: its own system prompt plus environment details (not the Claude Code system prompt); the delegation message; the CLAUDE.md hierarchy (except for Explore/Plan or with `omitClaudeMd`); a git status snapshot; preloaded skills; and a sibling roster (v2.1.206+) when it has `SendMessage`.
- It does not get conversation history, the output style, or the main conversation's auto memory.
- Results come back as the final report. The report is scanned for instruction-shaped text (v2.1.210+) and arrives under a header marking it as subagent output with no user authority.
- Transcripts: `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`, retained per `cleanupPeriodDays` (default 30 days).
- Settings, managed, and plugin hooks also fire inside subagents, with `agent_id` and `agent_type` in the input ([hooks](https://code.claude.com/docs/en/hooks)).

### Tools available to subagents

From [subagents](https://code.claude.com/docs/en/sub-agents):

- Always removed: `AskUserQuestion`, `EndConversation`, `EnterPlanMode`, `ExitPlanMode` (unless `permissionMode: plan`), `ScheduleWakeup`, `WaitForMcpServers`, `Workflow`, and `Agent` at the depth limit.
- Background subagents keep only these built-ins: Read, Grep, Glob, LSP, Bash, PowerShell, Edit, Write, NotebookEdit, WebFetch, WebSearch, TodoWrite, Skill, ToolSearch, EnterWorktree, ExitWorktree, Monitor, TaskStop, SendMessage, Artifact, and SubagentHandback. They keep all MCP tools.

### Foreground vs background

From [subagents](https://code.claude.com/docs/en/sub-agents):

- With fork mode on (the interactive default since v2.1.232), every spawned subagent runs in the background and `run_in_background` is removed from the tool.
- In `-p` and SDK runs (fork mode off), Claude chooses; the default is background.
- Ctrl+B backgrounds a running task.
- Permission prompts from background subagents surface in the main session.
- `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` forces foreground.

### Nesting and concurrency

From [subagents](https://code.claude.com/docs/en/sub-agents):

| Limit | Default | Variable |
| :- | :- | :- |
| Nesting depth below main | 3 layers; `1` disables nesting | `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` |
| Concurrent running subagents | 20, then "Concurrent subagent limit reached"; not enforced when ultracode is on | `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` (v2.1.217+) |

### Resume and SendMessage

- Claude resumes a finished subagent via `SendMessage` with the agent ID or name; full history is retained ([subagents](https://code.claude.com/docs/en/sub-agents)).
- Explore and Plan are one-shot and cannot be resumed ([subagents](https://code.claude.com/docs/en/sub-agents)).
- `SendMessage` does not require agent teams. No agent message counts as user approval ([subagents](https://code.claude.com/docs/en/sub-agents)).

### Forks

- A fork (the `fork` subagent type) inherits the full conversation, system prompt, tools, model, and prompt cache. Start one manually with `/subtask` (v2.1.212+; `/fork` on v2.1.161–2.1.211) ([subagents](https://code.claude.com/docs/en/sub-agents)).
- A fork cannot spawn further forks. `Agent(fork)` deny blocks forks. `CLAUDE_CODE_FORK_SUBAGENT=0/1` overrides the default ([subagents](https://code.claude.com/docs/en/sub-agents)).
- Forks receive auto memory ([memory](https://code.claude.com/docs/en/memory)) and the output style ([output styles](https://code.claude.com/docs/en/output-styles)); other subagents do not.
- `context: fork` in a skill is not a conversation fork; it starts a fresh subagent ([skills](https://code.claude.com/docs/en/skills)). See [skills.md](skills.md#context-fork).

### Worktree isolation

- `isolation: worktree` creates a temporary worktree from the default branch, auto-removed if unchanged. Git commands that escape to the main checkout are blocked ([subagents](https://code.claude.com/docs/en/sub-agents)). See [automation.md](automation.md#worktrees).

### Agent teams

From [agent teams](https://code.claude.com/docs/en/agent-teams):

- Experimental, disabled by default; enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Added as a research preview in v2.1.32 ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- Structure: a lead plus teammates, which are separate Claude Code instances with their own context windows.
- Coordination: shared task list in `~/.claude/tasks/{team}/` (pending / in progress / completed, with dependencies; claims use file locks); mailbox at `~/.claude/teams/{team}/inboxes/{agent}.json`; team config at `~/.claude/teams/{team}/config.json`, removed at session end.
- Claude starts a teammate when it calls the Agent tool with a `name` while teams are enabled, without asking you.
- Interactive only; in `-p`/SDK runs no teammates are spawned.
- Display modes: in-process (default) or split panes (tmux / iTerm2), via `teammateMode` or `--teammate-mode`.
- Subagent definitions can be reused as teammate roles (`tools`, `model`, and body apply; `skills` do not).
- Hooks: `TeammateIdle`, `TaskCreated`, `TaskCompleted` (see [hooks.md](hooks.md)).

### Other parallel features

From [run agents in parallel](https://code.claude.com/docs/en/agents), [agent view](https://code.claude.com/docs/en/agent-view), and the [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md):

- The docs list five approaches: subagents, agent view, agent teams, dynamic workflows, and projects.
- Agent view (`claude agents`, research preview, added in v2.1.139) manages background sessions started via `claude --bg` or `/background`.
- `/fork` copies the session into a new background session.
- `/batch` splits work into 5–30 worktree-isolated subagents.

## Example

`.claude/agents/code-reviewer.md` ([subagents](https://code.claude.com/docs/en/sub-agents)):

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices. Use proactively after code changes.
tools: Read, Glob, Grep
model: sonnet
---
You are a code reviewer. Analyze the code and give specific, actionable feedback.
```

## Limits and gotchas

- Rename: "In version 2.1.63, the Task tool was renamed to Agent. Existing `Task(...)` references in settings and agent definitions still work as aliases" ([subagents](https://code.claude.com/docs/en/sub-agents)).
- `/agents` was an interactive wizard on v2.1.197 and earlier; it now only prints a reminder to ask Claude or edit files ([subagents](https://code.claude.com/docs/en/sub-agents)).
- Nesting depth history: 5 layers, not configurable (v2.1.172–2.1.216); 1 (v2.1.217–218); 3 from v2.1.219 ([subagents](https://code.claude.com/docs/en/sub-agents)).
- Inference (from the research notes): several defaults flipped across 2.1.2xx releases (fork-mode default, background-by-default, nesting depth, model precedence). Older material about the "Task tool", foreground subagents, or "subagents cannot spawn subagents" is outdated.
- Inference (from the research notes): with agent teams enabled, any named subagent spawn becomes a teammate.
- Agent team limitations: no resume of in-process teammates; one team per session; no nested teams; fixed lead; no background subagents from in-process teammates; split panes not supported in VS Code, Windows Terminal, or Ghostty ([agent teams](https://code.claude.com/docs/en/agent-teams)).
- Background forks from skills (`context: fork`) and background subagent edits bypass checkpoints ([skills](https://code.claude.com/docs/en/skills); [checkpointing](https://code.claude.com/docs/en/checkpointing)).
- Frontmatter hooks in project subagents require trust of the agent file's folder (v2.1.218+); `-p` does not count as trust ([hooks](https://code.claude.com/docs/en/hooks)).
- Gap (research notes): the cross-session messaging page and agent view details (dispatch, permissions, worktree isolation for background sessions) were not read.
- Gap (research notes): the exact Agent tool input schema was not checked. Parameter names such as `subagent_type`, `name`, `model`, `isolation`, and `run_in_background` are inferred from mentions in the subagents page.

## Sources

- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/agent-sdk/subagents
- https://code.claude.com/docs/en/agent-teams
- https://code.claude.com/docs/en/agents
- https://code.claude.com/docs/en/agent-view
- https://code.claude.com/docs/en/permissions
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/output-styles
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/checkpointing
- https://code.claude.com/docs/en/plugins/components
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
