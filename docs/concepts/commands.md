# Commands

Commands are folded into [skills](skills.md) and are not a separate generalized concept. A custom command was a user-invoked prompt template: a Markdown file run as `/name args`. Both leads have retired that mechanism in favor of skills. Claude Code merged custom slash commands into skills in v2.1.3 and keeps `.claude/commands/` only as a legacy form ([commands][cc-commands]). Codex deprecated custom prompts (`~/.codex/prompts/`) with the instruction "Use skills for reusable instructions" ([commands][cx-commands]). What remains generalizable is a skill that only the user can invoke. Built-in slash commands are fixed harness features, not an extension mechanism, so they are not modeled.

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Status of user-defined commands | Legacy; merged into skills in v2.1.3; still work ([commands][cc-commands]) | Custom prompts deprecated ([commands][cx-commands]) | First-class ([commands][oc-commands]) |
| File location | `.claude/commands/<name>.md`; subdirectory → `/dir:name` ([commands][cc-commands]) | Top-level `.md` in `~/.codex/prompts/`; user scope only, not shareable through the repo ([commands][cx-commands]) | `.opencode/commands/`, `~/.config/opencode/commands/`, or the `command` config key ([commands][oc-commands]) |
| Format | Skill frontmatter minus `name` and `paths` ([commands][cc-commands]) | `description`, `argument-hint` ([commands][cx-commands]) | `description`, `agent`, `subtask`, `model`, `variant`; body is the template ([commands][oc-commands]) |
| Arguments | `$ARGUMENTS`, `$N` (0-based), named ([commands][cc-commands]) | `$1`–`$9`, `$ARGUMENTS`, `KEY=value` placeholders ([commands][cx-commands]) | `$ARGUMENTS`, `$1`, `$2`, … ([commands][oc-commands]) |
| Shell and file inclusion | `` !`cmd` ``, `@path` ([commands][cc-commands]) | Not recorded ([commands][cx-commands]) | `` !`cmd` ``, `@path` ([commands][oc-commands]) |
| Invocation | `/name` at message start ([commands][cc-commands]) | `/prompts:<name>` ([commands][cx-commands]) | `/name`; `opencode run --command` ([commands][oc-commands]) |
| Relation to skills | Every skill is a `/name` command; a skill wins a name clash with a command file ([commands][cc-commands]) | Skills replace prompts; invoked with `$name` or `/skills` ([commands][cx-commands]) | Every skill is registered as a command unless a command has the same name ([commands][oc-commands]) |
| Successor for user-only invocation | Skill with `disable-model-invocation: true` ([skills][cc-skills]) | Skill with `policy.allow_implicit_invocation: false` ([commands][cx-commands]) | Command file ([commands][oc-commands]) |
| MCP prompts as commands | `/mcp__<server>__<prompt>` ([commands][cc-commands]) | Not recorded ([commands][cx-commands]) | Yes, arguments mapped to `$1..$n` ([commands][oc-commands]) |

## Generalized model

A **user-invoked skill** is a skill (see [skills.md](skills.md)) with model invocation turned off. It has these properties:

- The user starts it by name with the harness's skill sigil.
- Its description is not in the model's catalog, so it costs no context until it is used.
- Its body enters context only on invocation.
- The text the user types after the name reaches the model as part of the message. No placeholder substitution is portable.

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| User-invoked skill | Skill with `disable-model-invocation: true` (legacy: `.claude/commands/<name>.md`) | Skill with `policy.allow_implicit_invocation: false` (legacy: `~/.codex/prompts/<name>.md`) | Command file in `.opencode/commands/` |
| Invocation | `/name` | `$name` or `/skills` | `/name` |
| User arguments | Appended as `ARGUMENTS: <value>` when no placeholder consumes them | Part of the user message | `$ARGUMENTS` |

Why fold rather than keep a separate concept:

1. Both leads point new work to skills, and their skill mechanisms already cover "run this procedure when I ask for it".
2. The features that still distinguish a command from a skill (argument placeholders, shell injection, run-as-subagent options) exist in Claude Code and OpenCode but not in Codex skills. By the generalization rule they do not generalize.
3. OpenCode keeps commands first-class, but OpenCode does not decide what generalizes.

## Portability

- Write new procedures as skills and follow the [skills portability rules](skills.md#portability).
- Migrate a Claude Code `.claude/commands/<name>.md` file to a skill directory `<name>/SKILL.md`, placed with the canonical-copy-plus-symlink layout in [skills.md](skills.md#directory-layout). Add `disable-model-invocation: true` for Claude Code and `agents/openai.yaml` with `policy.allow_implicit_invocation: false` for Codex.
- Migrate a Codex `~/.codex/prompts/<name>.md` the same way. Codex skills do not substitute `$1` or `KEY=value`, so instructions that rely on placeholders need rewriting ([commands][cx-commands]).
- Trap: Claude Code docs number arguments from `$0` ([commands][cc-commands]), while Codex prompts and OpenCode start at `$1` ([commands][cx-commands], [commands][oc-commands]).
- Trap: in OpenCode a command with the same name as a skill wins the slash name, and the skill is not registered as a command ([commands][oc-commands]).

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| Custom command files (`.claude/commands/`) | Claude Code | Legacy form of skills. |
| Custom prompts (`~/.codex/prompts/`, `/prompts:<name>`) | Codex | Deprecated. |
| Argument placeholders (`$ARGUMENTS`, `$N`, `KEY=value`) | Claude Code, Codex (prompts only), OpenCode | Codex skills, the surviving Codex mechanism, have no substitution. |
| `` !`cmd` `` shell injection and `@path` inclusion in templates | Claude Code, OpenCode | No Codex counterpart. |
| `agent` / `subtask` routing of a command to a subagent | OpenCode | No Codex counterpart; Claude Code's analogue (`context: fork`) is Claude-only as well. |
| Subdirectory namespaces (`/dir:name`, `git/commit`) | Claude Code, OpenCode | No Codex counterpart. |
| MCP prompts exposed as slash commands | Claude Code, OpenCode | Not recorded for Codex. |
| `opencode run --command` | OpenCode | No counterpart in either lead's headless CLI. |
| `command.execute.before` plugin hook | OpenCode | No command lifecycle hook in either lead (Claude Code's `UserPromptExpansion` is Claude-only). |
| Built-in slash commands (`/compact`, `/model`, `/review`, …) | All | Fixed harness features, not user configuration; lists differ per vendor. |

## Sources

- [Claude Code: commands](../vendors/claude-code/commands.md)
- [Claude Code: skills](../vendors/claude-code/skills.md)
- [Codex: commands](../vendors/codex/commands.md)
- [Codex: skills](../vendors/codex/skills.md)
- [OpenCode: commands](../vendors/opencode/commands.md)
- [OpenCode: skills](../vendors/opencode/skills.md)

[cc-commands]: ../vendors/claude-code/commands.md
[cc-skills]: ../vendors/claude-code/skills.md
[cx-commands]: ../vendors/codex/commands.md
[oc-commands]: ../vendors/opencode/commands.md
