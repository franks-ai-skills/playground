# Slash commands

A slash command is anything typed as `/name` at the start of a message. Claude Code has three kinds: built-in commands that run fixed logic (e.g. `/compact`, `/model`), bundled skills that are prompts (e.g. `/loop`, `/batch`), and custom commands. Custom slash commands were merged into [skills](skills.md) in v2.1.3: a `.claude/commands/<name>.md` file still works, but skills are preferred because they support a directory of supporting files ([skills](https://code.claude.com/docs/en/skills); [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).

## Locations and scopes

| Kind | Location | Command name |
| :- | :- | :- |
| Custom command (legacy) | `.claude/commands/<name>.md` | `/<name>` |
| Custom command in a subdirectory | `.claude/commands/frontend/component.md` | `/frontend:component` |
| Skill | `.claude/skills/<name>/SKILL.md` (and other skill scopes; see [skills.md](skills.md)) | `/<name>` |
| Plugin command | `<plugin>/commands/<file>.md`, or inline in `plugin.json` under `commands` | `/<plugin>:<file>` |
| Plugin skill | `<plugin>/skills/<name>/SKILL.md` | `/<plugin>:<name>` |
| MCP prompt | MCP server | `/mcp__<server>__<prompt>` or `/servername:promptname (MCP)` |
| Saved workflow | `.claude/workflows/` or `~/.claude/workflows/` | `/<name>` (see [automation.md](automation.md#dynamic-workflows)) |
| Built-in command | Harness | Fixed names |
| Bundled skill | Harness | Fixed names |

Sources: [skills](https://code.claude.com/docs/en/skills); [plugin components](https://code.claude.com/docs/en/plugins/components); [MCP](https://code.claude.com/docs/en/mcp); [scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks); [workflows](https://code.claude.com/docs/en/workflows)

Precedence ([skills](https://code.claude.com/docs/en/skills)):

- A skill wins over a `.claude/commands/` file with the same name.
- A user skill replaces a bundled skill or built-in command of the same name, but not its aliases.
- Plugin commands and skills are namespaced and never collide.

## Format

### Custom command files

- Markdown with optional YAML frontmatter. They "are the older format and still work" ([skills](https://code.claude.com/docs/en/skills)).
- Frontmatter: the same fields as skills except `name` and `paths`. See the field table in [skills.md](skills.md#frontmatter-fields-claude-code) ([skills](https://code.claude.com/docs/en/skills)).
- Plugin inline form: `plugin.json` → `"commands": {"about": {"content": "...", "description": "..."}}`. "Commands are the older format, and skills supersede them for new work" ([plugin components](https://code.claude.com/docs/en/plugins/components)).

### Arguments

Same as skills ([skills](https://code.claude.com/docs/en/skills)):

| Placeholder | Value |
| :- | :- |
| `$ARGUMENTS` | All arguments |
| `$ARGUMENTS[N]`, `$N` | Argument N, 0-based (`$0` is the first argument) |
| `$name` | Named argument declared in `arguments` |

- `argument-hint` provides the autocomplete hint ([skills](https://code.claude.com/docs/en/skills)).
- A backslash escapes a literal, e.g. `\$1.00` ([skills](https://code.claude.com/docs/en/skills)).
- If no placeholder receives the arguments, Claude Code appends `ARGUMENTS: <value>` ([skills](https://code.claude.com/docs/en/skills)).
- MCP prompt arguments are whitespace-split: `/mcp__server__prompt arg1 arg2` ([MCP](https://code.claude.com/docs/en/mcp)).

### Bash and file inclusion

- `` !`cmd` `` or a ```` ```! ```` block runs a shell command and inlines its output before Claude sees the prompt ([skills](https://code.claude.com/docs/en/skills)). Rules are in [skills.md](skills.md#dynamic-context-injection-claude-code-only).
- `@path` file references are attached for local skills and command files; for synced skills they are not attached ([skills](https://code.claude.com/docs/en/skills)).

## Loading and invocation

- "A command is only recognized at the start of your message." Commands sent mid-response are queued ([commands](https://code.claude.com/docs/en/commands)).
- Up to six skills/commands can be stacked: `/a /b args`. Since v2.1.199, the trailing text goes to each ([commands](https://code.claude.com/docs/en/commands)).
- The commands table marks bundled prompt-based entries as **Skill** and `/deep-research` as **Workflow** ([commands](https://code.claude.com/docs/en/commands)).
- Some built-in commands, such as `/init` and `/security-review`, can be called through the Skill tool; others, such as `/compact`, cannot ([skills](https://code.claude.com/docs/en/skills)).
- Context cost of custom commands and skills is described in [skills.md](skills.md#discovery-and-context-cost).
- `--disable-slash-commands` disables all skills (local `claude --help`, v2.1.289).

### Built-in commands mentioned in the research

| Command | Purpose |
| :- | :- |
| `/agents` | Now only prints a reminder to ask Claude or edit agent files (was an interactive wizard on v2.1.197 and earlier); see [subagents.md](subagents.md) |
| `/hooks` | Read-only browser of configured hooks |
| `/rewind` (aliases `/checkpoint`, `/undo`) | Restore checkpoints |
| `/plan [task]` | Enter plan mode |
| `/tasks`, `/subtask`, `/fork`, `/background` (`/bg`) | Background work and forks |
| `/schedule` (`/routines`), `/goal`, `/workflows` | Automation |
| `/reload-skills`, `/skills`, `/skill-doctor` | Skills |
| `/install-github-app`, `/security-review`, `/init` | Setup and review |
| `/memory`, `/import` | Instructions and memory |
| `/config`, `/status`, `/permissions`, `/sandbox`, `/model`, `/effort`, `/output-style`, `/statusline` | Configuration |
| `/mcp`, `/plugin`, `/reload-plugins` | MCP and plugins |
| `/add-dir`, `/cd`, `/context`, `/compact` | Session and context |

Sources: [commands](https://code.claude.com/docs/en/commands); [subagents](https://code.claude.com/docs/en/sub-agents); [hooks](https://code.claude.com/docs/en/hooks); [settings](https://code.claude.com/docs/en/settings); [memory](https://code.claude.com/docs/en/memory); [permissions](https://code.claude.com/docs/en/permissions)

Bundled skills (prompt-based) are listed in [skills.md](skills.md#bundled-skills).

## Example

Legacy command `.claude/commands/fix-issue.md`, invoked as `/fix-issue 123` (field set per [skills](https://code.claude.com/docs/en/skills)):

```markdown
---
description: Fix a GitHub issue
argument-hint: [issue-number]
disable-model-invocation: true
---
Fix GitHub issue $ARGUMENTS following our coding standards.
```

## Limits and gotchas

- Merge: the v2.1.3 changelog says "Merged slash commands and skills, simplifying the mental model with no change in behavior" ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- `https://code.claude.com/docs/en/slash-commands.md` returns byte-identical content to the skills page (verified with `cmp` on 2026-10-04). The Agent SDK "slash-commands" page likewise returns the SDK skills page ([slash-commands](https://code.claude.com/docs/en/slash-commands); [Agent SDK skills](https://code.claude.com/docs/en/agent-sdk/skills)).
- Command files do not support `name` or `paths` ([skills](https://code.claude.com/docs/en/skills)).
- `/name` after plain text only grants permission; it does not invoke ([skills](https://code.claude.com/docs/en/skills)).
- Inference (from the research notes): tutorials that treat `.claude/commands/` as a separate feature with its own frontmatter semantics are outdated. In current docs `$0` is the first argument, so older tutorials that used `$1` for the first argument may now mean the second. Gap: how `$1` was numbered before the merge was not found; the claim that numbering changed is unverified.
- `/fork` meaning changed: on v2.1.161–2.1.211 it started a conversation fork, now done by `/subtask` (v2.1.212+); `/fork` now copies the session into a new background session ([subagents](https://code.claude.com/docs/en/sub-agents); [run agents in parallel](https://code.claude.com/docs/en/agents)).

## Sources

- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/slash-commands
- https://code.claude.com/docs/en/agent-sdk/skills
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/plugins/components
- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/scheduled-tasks
- https://code.claude.com/docs/en/workflows
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/agents
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/permissions
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- Local CLI help: `claude --help` (v2.1.289)
