# Commands

Slash commands in the Codex TUI are a fixed built-in list; Codex no longer offers user-defined slash commands. The former mechanism, custom prompts (Markdown files in `~/.codex/prompts/` run as `/prompts:<name>`), is deprecated in favor of [skills](skills.md), which are invoked with `$skill-name` or `/skills` ([Custom Prompts](https://learn.chatgpt.com/docs/custom-prompts.md)). Plugins add skills and tools, not slash commands, as far as the docs that were read show.

## Locations and scopes

| Kind | Location | Scope |
|---|---|---|
| Built-in slash commands | Compiled into Codex | CLI TUI. The IDE extension has its own slash-command page ([IDE slash commands](https://learn.chatgpt.com/docs/developer-commands.md?surface=ide)) |
| Custom prompts (deprecated) | Top-level `.md` files in `~/.codex/prompts/` | Local only; not shared through the repository. Subdirectories and non-Markdown files are ignored ([Custom Prompts](https://learn.chatgpt.com/docs/custom-prompts.md)) |
| Skills (replacement) | `.agents/skills`, `~/.agents/skills` and other roots | See [skills.md](skills.md) |

## Format

### Built-in CLI slash commands

Current list from [Slash commands in Codex CLI](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli). The Notes column holds only what the notes record.

| Command | Notes |
|---|---|
| `/permissions` | Live runtime permission override; subagents inherit it ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)) |
| `/ide` | |
| `/keymap` | |
| `/vim` | |
| `/setup-default-sandbox` | Windows only |
| `/sandbox-add-read-dir` | Windows only |
| `/agent` (alias `/subagents`) | Switch between agent threads; see [subagents.md](subagents.md) |
| `/apps` | Inserts `$app-slug` for an app (connector) |
| `/plugins` | Plugin browser, grouped by marketplace; Space toggles an installed plugin; see [plugins.md](plugins.md) |
| `/hooks` | Inspect, trust or disable non-managed hooks; see [hooks.md](hooks.md) |
| `/clear` | |
| `/rename` | |
| `/archive` | |
| `/delete` | |
| `/compact` | |
| `/copy` | |
| `/diff` | |
| `/exit`, `/quit` | |
| `/experimental` | |
| `/approve` | |
| `/memories` | |
| `/skills` | Pick a skill; Codex inserts the selected skill context for the next request |
| `/import` | Migrates Claude Code or Cursor setup, projects and chats into Codex configuration and local files; up to 50 chats from the last 30 days; unavailable in remote/daemon sessions |
| `/feedback` | Turned off by `[feedback] enabled = false` ([Advanced config](https://developers.openai.com/codex/config-advanced)) |
| `/init` | Generates an `AGENTS.md` scaffold in the current directory; see [instructions.md](instructions.md) |
| `/logout` | |
| `/mcp [verbose]` | Lists active MCP servers; `verbose` shows details; see [mcp.md](mcp.md) |
| `/mention` | |
| `/model` | Choose the model; also adjusts reasoning effort ([Models](https://developers.openai.com/codex/models)) |
| `/fast` | |
| `/plan` | |
| `/goal` | Persisted goals and automatic continuation (`goals` feature, stable, on) ([Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md)) |
| `/personality` | |
| `/ps` | |
| `/stop` | |
| `/fork` | |
| `/app` | |
| `/side` (alias `/btw`) | |
| `/raw` | |
| `/resume` | |
| `/new` | |
| `/review` | Working-tree review by a dedicated reviewer; uses `review_model` if set; see [automation.md](automation.md) |
| `/status` | Shows the active model, approval policy, writable roots and context ([CLI reference](https://developers.openai.com/codex/cli/reference)) |
| `/usage` | |
| `/debug-config` | Prints config layer and requirements diagnostics ([CLI reference](https://developers.openai.com/codex/cli/reference)) |
| `/statusline` | |
| `/title` | |
| `/theme` | |
| `/pets` (alias `/pet`) | |

While a turn runs, typing a slash command and pressing `Tab` queues it for the next turn ([Slash commands in Codex CLI](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)).

### Custom prompts (deprecated)

| Element | Format |
|---|---|
| File | Top-level `.md` file in `~/.codex/prompts/` |
| Front matter `description:` | Shown in the command popup |
| Front matter `argument-hint:` | Argument hint shown to the user |
| `$1` – `$9` | Positional arguments |
| `$ARGUMENTS` | All arguments |
| `$FILE`, `$TICKET_ID`, ... | Uppercase named placeholders, filled with `KEY=value` on invocation; quote values that contain spaces |
| `$$` | A literal `$` |
| Invocation | `/prompts:<name>`, for example `/prompts:draftpr FILES="..." PR_TITLE="..."` |

Source: [Custom Prompts](https://learn.chatgpt.com/docs/custom-prompts.md).

## Loading and invocation

- **Built-ins** are always available in the TUI. A slash command typed during a running turn plus `Tab` is queued.
- **Custom prompts** need explicit invocation and a restart or new chat before a new or changed file loads ([Custom Prompts](https://learn.chatgpt.com/docs/custom-prompts.md)). A custom prompt's text enters context only when it is invoked.
- **Replacement with skills.** New work should use skills. Inference: a skill with `policy.allow_implicit_invocation: false` in `agents/openai.yaml` gives prompt-like behavior that runs only when called with `$skill-name` or `/skills` ([skills.md](skills.md)).

## Example

Deprecated custom prompt in `~/.codex/prompts/` (the docs invoke it as `draftpr`; a matching file name `draftpr.md` is assumed here):

```markdown
---
description: Prep a branch, commit, and open a draft PR
argument-hint: [FILES=<paths>] [PR_TITLE="<title>"]
---
Create a branch named `dev/<feature_name>` for this work.
If files are specified, stage them first: $FILES.
```

Invocation: `/prompts:draftpr FILES="..." PR_TITLE="..."`. Source: [Custom Prompts](https://learn.chatgpt.com/docs/custom-prompts.md).

## Limits and gotchas

- **Custom prompts are deprecated.** "Custom prompts are deprecated. Use skills for reusable instructions that Codex can invoke explicitly or implicitly." The llms.txt index labels the page "Deprecated. Use skills for reusable prompts" ([Custom Prompts](https://learn.chatgpt.com/docs/custom-prompts.md); [llms.txt](https://learn.chatgpt.com/llms.txt)).
- **Possibly already removed (unverified).** The current CLI slash-command table does not list `/prompts:`. The installed 0.159.2 binary has no `codex/prompts` or `CustomPrompt` strings other than `OpenReviewCustomPrompt`, which is the `/review` custom-instructions picker in `tui/src/bottom_pane/custom_prompt_view/picker.rs` (local `strings` on the binary). Path strings could be built at runtime, so removal is not proven. **Gap:** the release that removed custom prompts, if any, was not found; GitHub search hit its rate limit, and no official removal note was found.
- **No argument substitution in skills.** Skills have no `$1` or `KEY=value` substitution. The text after `$skill-name` is just part of the user message. Migrating a prompt that relies on placeholders needs the instructions rewritten.
- **Gap: plugin commands.** Plugin "commands" are mentioned in the bundled self-knowledge reference but were not verified in the docs. No documented way exists to define new built-in-style slash commands.
- The IDE extension's slash commands are on a separate page that the notes do not detail ([IDE slash commands](https://learn.chatgpt.com/docs/developer-commands.md?surface=ide)).

## Sources

- https://learn.chatgpt.com/docs/custom-prompts.md
- https://learn.chatgpt.com/llms.txt
- https://learn.chatgpt.com/docs/developer-commands.md?surface=cli
- https://learn.chatgpt.com/docs/developer-commands.md?surface=ide
- https://learn.chatgpt.com/docs/agent-configuration/subagents.md
- https://learn.chatgpt.com/docs/config-file/config-reference.md
- https://developers.openai.com/codex/config-advanced
- https://developers.openai.com/codex/models
- https://developers.openai.com/codex/cli/reference
