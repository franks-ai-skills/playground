# Commands

Commands are reusable prompt templates the user runs as `/name args` in the TUI or with `opencode run --command`. A command can inject arguments, shell output, and file contents into its template, and can run on a specific agent or model, optionally as a subagent task. Custom commands come from markdown files or the `command` config key; MCP prompts and skills are also exposed as commands.

## Locations and scopes

| Scope | Location |
| --- | --- |
| Global | `~/.config/opencode/commands/` |
| Project | `.opencode/commands/` |
| Config | `command` key in any config layer ([configuration.md](configuration.md)) |
| MCP | Prompts from configured MCP servers ([mcp.md](mcp.md)) |
| Skills | Every discovered skill ([skills.md](skills.md)) |
| Built-in | `/init`, `/review`, and the TUI commands listed below |

Sources: [Commands](https://opencode.ai/docs/commands/); [SRC command/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/command/index.ts).

In source, markdown commands are found with the glob `{command,commands}/**/*.md` in every config directory. Nested paths become names such as `git/commit` ([SRC config/command.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/command.ts)).

### Registry order and precedence

([SRC command/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/command/index.ts))

1. Built-in `init` ("guided AGENTS.md setup") and `review` ("review changes [commit|branch|pr], defaults to uncommitted", `subtask: true`).
2. Config commands (markdown files and the `command` key).
3. MCP server prompts (`source: "mcp"`), with their arguments mapped to `$1..$n`.
4. Skills (`source: "skill"`), unless a command already has that name. Template: the skill body plus "Base directory for this skill: <dir>".

A custom command with the same name as a built-in overrides it ([Commands](https://opencode.ai/docs/commands/)).

## Format

Markdown file: YAML frontmatter holds the options and the body is the template. The filename (path) gives the name. In the `command` JSON key, the template goes in `template`. Invalid frontmatter raises an `InvalidError` ([SRC config/command.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/command.ts)).

### Options

| Option | Meaning | Default |
| --- | --- | --- |
| `template` | Prompt template. Required (the markdown body in file form). | |
| `description` | Shown in the TUI. | |
| `agent` | Agent that runs the command. If it names a subagent, the command runs as a subagent invocation. | Current agent |
| `subtask` | `true` forces a subagent run, which keeps the primary context clean. `false` disables the automatic subagent run for a subagent `agent`. | |
| `model` | Model override. | |
| `variant` | Model variant (schema only). | |

Sources: [Commands – Options](https://opencode.ai/docs/commands/); `variant` from [SRC core/src/v1/config/command.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/command.ts).

### Template syntax

| Syntax | Effect |
| --- | --- |
| `$ARGUMENTS` | The whole argument string. |
| `$1`, `$2`, … | Positional arguments. Quoted strings are kept together. |
| `` !`command` `` | Runs the command in the project root and injects its output. |
| `@path/to/file` | Includes the file's content. |

Source: [Commands](https://opencode.ai/docs/commands/).

### Built-in commands

`/init`, `/undo`, `/redo`, `/share`, `/help`, `/connect`, `/compact`, `/details`, `/editor`, `/exit`, `/export`, `/models`, `/new`, `/sessions`, `/themes`, `/thinking`, `/unshare` ([Commands](https://opencode.ai/docs/commands/); [TUI](https://opencode.ai/docs/tui/)), plus `review` in the source registry ([SRC command/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/command/index.ts)). See [instructions.md](instructions.md#init) for `/init` and [automation.md](automation.md#sharing) for `/share`.

## Loading and invocation

- Command files are loaded from the config directories at startup ([configuration.md](configuration.md#config-directories)).
- The user invokes `/name args` in the TUI ([Commands](https://opencode.ai/docs/commands/)).
- `opencode run --command <name> [args]` runs a command non-interactively ([CLI](https://opencode.ai/docs/cli/)).
- The Task tool has an optional `command` parameter that records the command that triggered a subagent task ([SRC tool/task.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/tool/task.ts)).
- Plugins can rewrite command parts through the `command.execute.before` hook (`input {command, sessionID, arguments}`, `output {parts}`). The bus emits `command.executed` ([SRC plugin/src/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts); [Plugins – Events](https://opencode.ai/docs/plugins/)). See [hooks.md](hooks.md).
- Context cost: with `subtask: true` (or a subagent `agent`), the command runs as a subagent and the primary context stays clean ([Commands – Options](https://opencode.ai/docs/commands/)).

## Example

```markdown
<!-- .opencode/commands/review-changes.md -->
---
description: Review recent changes
agent: plan
subtask: true
---
Recent commits:
!`git log --oneline -10`
Review these, focusing on $ARGUMENTS.
```

## Limits and gotchas

- **Custom commands override built-ins** with the same name.
- **Skills lose to commands** on a name clash: the skill is not registered as a command.
- **Invalid frontmatter** raises an `InvalidError`.
- **`description` is shown in the TUI**; the notes do not say the model sees it.
- **Gap:** none of the sources say whether `` !`cmd` `` respects `bash` permissions. The docs only say the command runs in the project root.

## Sources

- https://opencode.ai/docs/commands/
- https://opencode.ai/docs/tui/
- https://opencode.ai/docs/cli/
- https://opencode.ai/docs/plugins/
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/command/index.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/command.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/command.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/tool/task.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts
