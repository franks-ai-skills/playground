# Agents

An agent is a named configuration of prompt, model, and permissions. Primary agents drive the main conversation and the user switches between them with Tab. Subagents run delegated work in child sessions, started by the model through the `task` tool or by the user with `@name`, which keeps the primary context small.

## Locations and scopes

| Scope | Location |
| --- | --- |
| Built-in | `build`, `plan`, `general`, `explore`, `scout` (experimental), and hidden `compaction`, `title`, `summary` |
| Config | `agent` key in any config layer; built-in agents are configured under their keys `plan`, `build`, `general`, `explore`, `title`, `summary`, `compaction` ([SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)) |
| Global markdown | `~/.config/opencode/agents/` |
| Project markdown | `.opencode/agents/` |
| Legacy modes | `{mode,modes}/*.md` in config dirs, loaded as agents with `mode: primary` |

Markdown locations: [Agents](https://opencode.ai/docs/agents/). In source, the scan glob is `{agent,agents}/**/*.md` in every config directory ([configuration.md](configuration.md#config-directories)). Nested directories are allowed; the name is the relative path without extension, e.g. `agents/team/review.md` → `team/review`. Markdown agents merge over JSON-defined agents from earlier layers ([SRC config/agent.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/agent.ts), [SRC config/entry-name.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/entry-name.ts)).

### Built-in agents

| Agent | Mode | Behavior |
| --- | --- | --- |
| Build | primary | Default; all tools. |
| Plan | primary | Restricted: file edits and bash are `ask`. |
| General | subagent | Full tools except todo; can run work in parallel. |
| Explore | subagent | Fast, read-only codebase search. |
| Scout | subagent | Read-only research on external docs and dependencies; clones repos into a managed cache. Gated behind `OPENCODE_EXPERIMENTAL_SCOUT` ([CLI – Experimental](https://opencode.ai/docs/cli/)). |
| compaction, title, summary | primary | Hidden; run automatically. |

Source: [Agents](https://opencode.ai/docs/agents/).

## Format

Markdown: YAML frontmatter holds the options and the body is the prompt. The filename gives the name, e.g. `review.md` → `review` ([Agents](https://opencode.ai/docs/agents/)). JSON: an entry under `agent`, keyed by name.

### Options

| Option | Meaning | Default |
| --- | --- | --- |
| `description` | What the agent does; used for automatic selection. Documented as required. | |
| `mode` | `primary`, `subagent`, or `all`. | `all` |
| `model` | `provider/model`. | Primary agents use the global `model`; subagents inherit the invoking agent's model. |
| `variant` | Default model variant. Applied only when the agent uses its own configured model (schema). | |
| `prompt` | System prompt. Often `{file:...}`, resolved relative to the config file. In markdown, the body. | |
| `temperature` | Sampling temperature. | Model default, typically 0 for most models. |
| `top_p` | Nucleus sampling. | |
| `steps` | Maximum agentic iterations; after that the agent is forced to give a text summary. | |
| `maxSteps` | Deprecated; use `steps`. | |
| `disable` | Disables the agent. | |
| `hidden` | Hides a subagent from `@` autocomplete. The Task tool can still invoke it. | |
| `color` | Hex or a theme color. | |
| `permission` | Per-agent permission rules; merged over the global rules, agent rules win. | |
| `tools` | Deprecated boolean map; use `permission`. | |
| `options` | Provider options (schema). Unknown keys are folded into `options`. | |
| any other key | Passed to the provider, e.g. `reasoningEffort`, `textVerbosity`. | |

Sources: [Agents – Options](https://opencode.ai/docs/agents/); `variant` and `options` from [SRC core/src/v1/config/agent.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/agent.ts). Permission keys are in [permissions-and-sandbox.md](permissions-and-sandbox.md).

### Task tool

Parameters ([SRC tool/task.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/tool/task.ts)):

| Parameter | Meaning |
| --- | --- |
| `description` | 3–5 words. |
| `prompt` | Task for the subagent. |
| `subagent_type` | Subagent name. The permission check matches this value. |
| `task_id` | Optional. Resumes a prior subagent session. |
| `command` | Optional. The command that triggered the task. |

### Related config

| Key | Meaning | Default |
| --- | --- | --- |
| `permission.task` | Globs over subagent names; last match wins. A denied subagent is removed from the Task tool description. | allow |
| `subagent_depth` | How many levels of subagents can nest. `0` disables subagents; `1` means subagents cannot spawn subagents; `2` allows one more level. | `1` |
| `default_agent` | Default primary agent across TUI, `opencode run`, desktop, and the GitHub Action. Must be primary; otherwise falls back to `build` with a warning. | `build` |
| `experimental.primary_tools` | Tools available only to primary agents. | |

Sources: [Agents – Task permissions](https://opencode.ai/docs/agents/); [Config](https://opencode.ai/docs/config/); [REL v1.18.2](https://github.com/anomalyco/opencode/releases/tag/v1.18.2); [SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts).

## Loading and invocation

- **Startup:** markdown agents and legacy modes are loaded from every config directory and merged over JSON agents.
- **Primary agents:** Tab or the `switch_agent` keybind cycles them ([Agents – Usage](https://opencode.ai/docs/agents/)).
- **Subagents by the model:** the model calls the `task` tool with `subagent_type`. Only subagents allowed by `permission.task` appear in the Task tool description, so denied subagents cost no context.
- **Subagents by the user:** `@general …` invokes a subagent manually. Users can `@`-invoke any subagent regardless of `permission.task`; `hidden` removes a subagent from `@` autocomplete only.
- **Child sessions:** `session_child_first` (Leader+Down) enters the first child session, `session_child_cycle` (Right) and `session_child_cycle_reverse` (Left) move between them, `session_parent` (Up) returns ([Agents – Usage](https://opencode.ai/docs/agents/)).
- **Commands:** a command whose `agent` is a subagent runs as a subagent invocation ([commands.md](commands.md)).
- **CLI:** `opencode agent create` creates an agent interactively. It runs non-interactively when given `--path`, `--description`, `--mode`, and `--permissions` (plus optional `-m`); anything not allowed is written as denied. `opencode agent list` lists agents ([CLI](https://opencode.ai/docs/cli/); [Agents](https://opencode.ai/docs/agents/)). `opencode run --agent <name>` picks an agent for a scripted run ([automation.md](automation.md)).
- **Tool defaults:** `todowrite` is disabled for subagents by default ([Tools](https://opencode.ai/docs/tools/)).
- **Background subagents** are behind `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS` ([CLI](https://opencode.ai/docs/cli/)).
- **Plugins:** the V2 plugin API has a `ctx.agent.transform` hook ([plugins.md](plugins.md#v2-plugin-api)).

## Example

```markdown
<!-- .opencode/agents/review.md -->
---
description: Reviews code for quality; use after edits
mode: subagent
model: anthropic/claude-sonnet-4-5
temperature: 0.1
permission: { edit: deny, bash: { "*": ask, "git diff*": allow } }
---
You are a code reviewer. Report issues; do not edit files.
```

## Limits and gotchas

- **`description` required vs optional (contradiction).** The docs say `description` is required; the schema has it optional. It is probably enforced only for agents meant to be selected automatically (subagents) (inference from the notes).
- **Default `mode` is `all`**, so an agent without `mode` is usable both as primary and as subagent.
- **`permission.task` does not restrict the user.** Users can still `@`-invoke denied subagents.
- **Nesting changed in v1.18.2:** `subagent_depth` defaults to `1`, so subagents cannot spawn subagents unless you raise it ([REL v1.18.2](https://github.com/anomalyco/opencode/releases/tag/v1.18.2)).
- **Deprecated:** `tools` (use `permission`, since v1.1.1), `maxSteps` (use `steps`), top-level `mode` config key (use `agent`), `modes/` directory (loaded as primary agents).
- **v1.16.0** added file-based agent loading ([REL v1.16.0](https://github.com/anomalyco/opencode/releases/tag/v1.16.0)).
- **v1.18.20:** `opencode run` answers permission requests raised by subagents ([REL v1.18.20](https://github.com/anomalyco/opencode/releases/tag/v1.18.20)).
- **Gap:** none of the sources document Scout's default model, permission set, or cache location beyond "managed cache".
- **Gap:** the algorithm that merges agent and global permission rules is not documented beyond "agent rules take precedence".

## Sources

- https://opencode.ai/docs/agents/
- https://opencode.ai/docs/config/
- https://opencode.ai/docs/cli/
- https://opencode.ai/docs/tools/
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/agent.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/entry-name.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/agent.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/tool/task.ts
- https://github.com/anomalyco/opencode/releases/tag/v1.16.0
- https://github.com/anomalyco/opencode/releases/tag/v1.18.2
- https://github.com/anomalyco/opencode/releases/tag/v1.18.20
