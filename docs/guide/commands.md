# Commands

Commands are folded into [skills](skills.md) and are not a separate generalized concept. A custom command was a user-invoked prompt template, a Markdown file run as `/name args`; both leads have retired it in favor of skills. Claude Code merged custom slash commands into skills in v2.1.3 and keeps `.claude/commands/` as a legacy form ([CC][cc-commands]); Codex deprecated custom prompts (`~/.codex/prompts/`) with "Use skills for reusable instructions" ([Codex][cx-commands]). Built-in slash commands are fixed harness features and are not modeled.

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Status of user-defined commands | Legacy, still work ([CC][cc-commands]) | Custom prompts deprecated ([Codex][cx-commands]) | First-class ([OC][oc-commands]) |
| Location | `.claude/commands/<name>.md` ([CC][cc-commands]) | `~/.codex/prompts/`, user scope only ([Codex][cx-commands]) | `.opencode/commands/`, `~/.config/opencode/commands/`, `command` config key ([OC][oc-commands]) |
| Arguments | `$ARGUMENTS`, `$N` (0-based), named ([CC][cc-commands]) | `$1`–`$9`, `$ARGUMENTS`, `KEY=value` ([Codex][cx-commands]) | `$ARGUMENTS`, `$1`, `$2`, … ([OC][oc-commands]) |
| Successor for user-only invocation | Skill with `disable-model-invocation: true` ([CC][cc-skills]) | Skill with `policy.allow_implicit_invocation: false` ([Codex][cx-commands]) | Command file ([OC][oc-commands]) |

## Generalized model

A **user-invoked skill** is a skill with model invocation turned off. The user starts it by name; its description is not in the model's catalog, so it costs no context until used; its body enters context only on invocation; the text after the name reaches the model as part of the message. No placeholder substitution is portable.

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| User-invoked skill | Skill with `disable-model-invocation: true` | Skill with `policy.allow_implicit_invocation: false` | Command file in `.opencode/commands/` |
| Invocation | `/name` | `$name` or `/skills` | `/name` |
| User arguments | Appended as `ARGUMENTS: <value>` when no placeholder consumes them | Part of the user message | `$ARGUMENTS` |

## When to use it and when not

Use a user-invoked skill when:

- The procedure has side effects or timing the model should not decide: "You don't want Claude deciding to deploy because your code looks ready" ([Claude Code skills](https://code.claude.com/docs/en/skills)).
- A rarely needed skill should cost no catalog context.

Do not use it, and use instead:

| Situation | Use instead | Cost of a user-invoked skill |
| --- | --- | --- |
| The agent should apply the knowledge on its own | A model-invoked [skill](skills.md) | The model never activates it |
| A rule must hold every time | [Hooks](hooks.md) | It runs only when someone invokes it |
| A Claude Code schedule must run it | A model-invocable [skill](skills.md) | In Claude Code the flag also blocks scheduled tasks and subagent preloading |

## Portability

- Write new procedures as skills and follow the [skills portability rules](skills.md#portability).
- Migrate `.claude/commands/<name>.md` or `~/.codex/prompts/<name>.md` to `<name>/SKILL.md` in the shared skill layout. Add `disable-model-invocation: true` and `agents/openai.yaml` with `policy.allow_implicit_invocation: false`.
- Codex skills do not substitute `$1` or `KEY=value`. Rewrite the body to read inputs from the user's message.
- Claude Code numbers arguments from `$0` ([CC][cc-commands]); Codex prompts and OpenCode start at `$1` ([Codex][cx-commands], [OC][oc-commands]).
- In OpenCode a command with the same name as a skill wins the slash name ([OC][oc-commands]).

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| Custom command files, custom prompts (`/prompts:<name>`) | Claude Code, Codex | Legacy or deprecated forms of skills |
| Argument placeholders, `` !`cmd` `` injection, `@path` inclusion, `/dir:name` namespaces | Claude Code, OpenCode (placeholders also Codex prompts) | Codex skills have none of these |
| `agent` / `subtask` routing, `opencode run --command`, `command.execute.before` | OpenCode | No counterpart in either lead |
| MCP prompts as slash commands | Claude Code, OpenCode | Not recorded for Codex |
| Built-in slash commands | All | Fixed harness features; lists differ per vendor |

## Sources

- [Claude Code: commands](../vendors/claude-code/commands.md), [Claude Code: skills](../vendors/claude-code/skills.md)
- [Codex: commands](../vendors/codex/commands.md), [Codex: skills](../vendors/codex/skills.md)
- [OpenCode: commands](../vendors/opencode/commands.md), [OpenCode: skills](../vendors/opencode/skills.md)

[cc-commands]: ../vendors/claude-code/commands.md
[cc-skills]: ../vendors/claude-code/skills.md
[cx-commands]: ../vendors/codex/commands.md
[oc-commands]: ../vendors/opencode/commands.md
