# Skills

A skill is a directory with a `SKILL.md` file (YAML frontmatter plus Markdown instructions) and optional supporting files. Only its name and description sit in context until it is invoked, by the user as `/name` or by Claude through the Skill tool. Skills solve the problem of repeatedly pasting the same procedure into chat, and of CLAUDE.md content that has grown into a procedure: "Unlike CLAUDE.md content, a skill's body loads only when it's used" ([skills](https://code.claude.com/docs/en/skills)). Claude Code follows the Agent Skills open standard and adds Claude Code-only features such as invocation control, subagent execution, and dynamic context injection. Custom slash commands are a legacy form of skills; see [commands.md](commands.md).

## Locations and scopes

| Scope | Path | Notes |
| :- | :- | :- |
| Enterprise | `.claude/skills/<skill-name>/SKILL.md` in the managed settings directory | All users on machines where the organization deploys it |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects on that machine; not in Cowork or cloud sessions |
| Project | `.claude/skills/<skill-name>/SKILL.md` | Commit to share. Loads from the start directory and every parent directory up to the repo root |
| Nested | `<subdir>/.claude/skills/<skill-name>/SKILL.md` | Loads for sessions started in or below `<subdir>`. A session started above it loads the skill once Claude reads or edits a file in that subdirectory, or after `/add-dir` (v2.1.257+) |
| Additional directory | `.claude/skills/` inside an `--add-dir` directory | `permissions.additionalDirectories` grants file access only and loads no skills |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Namespaced as `/plugin-name:skill-name`; see [plugins.md](plugins.md) |
| claude.ai account | `~/.claude/skills/synced/` | Skills enabled on the account are synced here (v2.1.273+) |

Source: [skills](https://code.claude.com/docs/en/skills)

- Name precedence: enterprise > personal > project. A skill beats a `.claude/commands/` file with the same name. Your skill replaces a bundled skill or built-in command of the same name, but not its aliases. Plugin skills never collide because they are namespaced ([skills](https://code.claude.com/docs/en/skills)).
- A symlinked skill folder is allowed. Adding `.claude-plugin/plugin.json` to a skill folder turns it into a plugin named `<name>@skills-dir` ([skills](https://code.claude.com/docs/en/skills)).
- Reserved: the folder name `synced` and the namespace `anthropic-skills:*` ([skills](https://code.claude.com/docs/en/skills)).
- Cloud sessions and routines do not read `~/.claude/skills/`. They load claude.ai-enabled skills plus skills committed to the cloned repo ([skills](https://code.claude.com/docs/en/skills)).
- Subagents can preload skills through the `skills` frontmatter field; see [subagents.md](subagents.md).

## Format

Directory layout: `skill-name/SKILL.md` plus any supporting files. The Agent Skills spec names optional `scripts/`, `references/`, and `assets/` directories ([Agent Skills spec](https://agentskills.io/specification)).

Parsing rules ([skills](https://code.claude.com/docs/en/skills)):

- All fields are optional; `description` is recommended.
- Unknown fields are ignored silently.
- Frontmatter is read only if the opening `---` is the first line.
- If the YAML is invalid, the skill loads with no fields set.
- Since v2.1.218, booleans accept yes/no/on/off/1/0.

### Frontmatter fields (Claude Code)

| Field | Meaning | Default |
| :- | :- | :- |
| `name` | Command name | Directory name |
| `description` | What the skill does and when to use it | First non-empty body line |
| `when_to_use` | Trigger phrases, appended to the description | — |
| `argument-hint` | Autocomplete hint, e.g. `[issue-number]` | — |
| `arguments` | Named positional arguments for `$name` substitution | — |
| `disable-model-invocation` | `true`: Claude cannot invoke the skill and its description is not in context. Also blocks preloading into subagents and, since v2.1.196, running from a scheduled task | `false` |
| `user-invocable` | `false`: hidden from the `/` menu; only Claude can invoke it | `true` |
| `allowed-tools` | Tools approved without prompting during the invoking turn; the grant clears at the next user message. Does not restrict which tools are available | — |
| `disallowed-tools` | Tools removed while the skill is active | — |
| `model` | Model for the rest of the turn, or `inherit`. With `context: fork`, the subagent's model | — |
| `effort` | `low` / `medium` / `high` / `xhigh` / `max` | — |
| `context` | `fork` runs the skill in a subagent | — |
| `agent` | Subagent type used for the fork | `general-purpose` |
| `background` | Only with `context: fork` (v2.1.218+) | `true` |
| `hooks` | Hooks registered on invocation; persist for the rest of the session. See [hooks.md](hooks.md) | — |
| `paths` | Globs that limit auto-activation to matching files | — |
| `shell` | Shell for `!` commands: `bash` or `powershell` | `bash` |
| `metadata` | Free-form map; Claude Code ignores it | — |
| `license` | Agent Skills spec field; accepted, not acted on | — |
| `compatibility` | Agent Skills spec field; accepted, not acted on; at most 500 chars | — |

Source: [skills](https://code.claude.com/docs/en/skills)

### String substitutions

| Placeholder | Value |
| :- | :- |
| `$ARGUMENTS` | All arguments |
| `$ARGUMENTS[N]`, `$N` | Argument N, 0-based, shell-style quoting |
| `$name` | Named argument from `arguments` |
| `${CLAUDE_SESSION_ID}` | Session ID |
| `${CLAUDE_EFFORT}` | Current effort level |
| `${CLAUDE_SKILL_DIR}` | The skill's directory (added in v2.1.69) |
| `${CLAUDE_PROJECT_DIR}` | Project root (v2.1.196+) |
| `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}` | Plugin skills only; see [plugins.md](plugins.md#format) |

Sources: [skills](https://code.claude.com/docs/en/skills); [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

- If no placeholder receives the arguments, Claude Code appends `ARGUMENTS: <value>` ([skills](https://code.claude.com/docs/en/skills)).
- A backslash escapes a literal, e.g. `\$1.00` ([skills](https://code.claude.com/docs/en/skills)).
- `${CLAUDE_SKILL_DIR}` is also substituted inside `allowed-tools` Bash rules, so a bundled script can run without a prompt, e.g. `allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *)` ([skills](https://code.claude.com/docs/en/skills)).
- `@path` file references are attached for local skills and command files; for synced skills they are not attached ([skills](https://code.claude.com/docs/en/skills)).

### Dynamic context injection (Claude Code-only)

From [skills](https://code.claude.com/docs/en/skills):

- `` !`cmd` `` (at line start or after whitespace) or a fenced ```` ```! ```` block runs the shell command before Claude sees the skill and inlines its output. Output is not re-scanned for further commands.
- A failing command (non-zero exit; exit 1 is tolerated for search/diff commands) aborts the whole invocation.
- Injected commands never prompt. A deny rule, or outside auto mode any non-allow result, aborts the invocation.
- `"disableSkillShellExecution": true` replaces each command with `[shell command execution disabled by policy]`. Bundled and managed skills are exempt.
- Skills synced from claude.ai never run `!` commands locally.

### Relation to the Agent Skills spec (agentskills.io)

From the [Agent Skills specification](https://agentskills.io/specification) unless noted:

| Aspect | Agent Skills spec | Claude Code |
| :- | :- | :- |
| `name` | Required; 1–64 chars, lowercase a–z/0–9/hyphen, no leading, trailing, or double hyphen; must match the parent directory name | Optional; defaults to the directory name and can override the command name ([skills](https://code.claude.com/docs/en/skills)) |
| `description` | Required; 1–1024 chars | Recommended; `description` + `when_to_use` truncated together at 1,536 chars in the listing ([skills](https://code.claude.com/docs/en/skills)) |
| Optional fields | `license`, `compatibility` (≤500 chars), `metadata` (string→string map), `allowed-tools` (space-separated, "Experimental") | All spec fields accepted, plus the Claude Code-only fields above |
| `allowed-tools` syntax | Example uses `Bash(git:*)` | Docs use permission-rule syntax `Bash(git *)` |
| Progressive disclosure | Metadata (~100 tokens) at startup; instructions (<5000 tokens recommended) on activation; resources as needed | Listing at startup; body on invocation |
| Size guidance | SKILL.md under 500 lines; file references one level deep | SKILL.md under 500 lines; detail in supporting files ([skills](https://code.claude.com/docs/en/skills)) |
| Validation | `skills-ref validate ./my-skill` | No skill-specific validator recorded; `claude plugin validate` checks plugins ([plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference)) |

- Distribution limits: claude.ai uploads, the Skills API, and `package_skill.py` from anthropics/skills accept only `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. Other keys cause a hard error ("Unexpected key(s) in SKILL.md frontmatter…"). Dynamic context injection does not work in claude.ai chat or the API ([skills](https://code.claude.com/docs/en/skills)).
- Inference (from the research notes): for portability, use only the six spec fields and spec-valid names.

### Related settings

| Key / flag | Effect |
| :- | :- |
| `skillOverrides` | Per skill: `on` / `name-only` / `user-invocable-only` / `off` (not for plugin skills) |
| `disableBundledSkills` | Turns off bundled skills |
| `skillListingBudgetFraction`, `skillListingMaxDescChars`, `SLASH_COMMAND_TOOL_CHAR_BUDGET` | Listing budget tuning |
| `disableSkillShellExecution` | Disables `!` command injection |
| `--disable-slash-commands` | Disables all skills (local `claude --help`) |

Source: [skills](https://code.claude.com/docs/en/skills) unless noted

## Loading and invocation

### Discovery and context cost

From [skills](https://code.claude.com/docs/en/skills):

- Default: the description is always in context, and the full skill loads on invocation. With `disable-model-invocation: true`, the description is not in context. With `user-invocable: false`, the description stays in context.
- The listing's character budget is 1% of the model's context window. On overflow, descriptions of the least-invoked skills are dropped first; names are always kept.
- The rendered SKILL.md enters the conversation as one message and stays there. It is not re-read on later turns. Re-invoking with identical content adds only a note.
- After auto-compaction, the most recent invocation of each skill is re-attached: first 5,000 tokens each, 25,000 tokens combined.
- Supporting scripts are "executed, not loaded".
- Inference (from the research notes): two costs drive context budgeting. The per-skill listing entry is always paid unless `disable-model-invocation` or `name-only` applies. The body persists after invocation, and compaction re-attaches it.
- `/skill-doctor` (v2.1.252+) reports each skill's cost and usage.
- Live change detection: edits under `~/.claude/skills/`, the project `.claude/skills/`, and `--add-dir` skills apply mid-session. A top-level skills directory created after startup needs `/reload-skills`. Bare mode does not watch for changes.

### Invocation

- User: `/name` at the start of a message. `/name` after plain text only grants permission ([skills](https://code.claude.com/docs/en/skills)).
- Up to six skills can be stacked: `/a /b args`. Since v2.1.199, the trailing text goes to each ([commands](https://code.claude.com/docs/en/commands)).
- Claude: through the Skill tool. Permission rules: `Skill` (deny all), `Skill(name)`, `Skill(name *)` ([skills](https://code.claude.com/docs/en/skills)).
- `paths` limits auto-activation to matching files ([skills](https://code.claude.com/docs/en/skills)).
- Scheduled fires only run model-invocable skills ([scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks)).

### `context: fork`

From [skills](https://code.claude.com/docs/en/skills):

- Starts a new subagent of type `agent` with the skill content as its prompt. The subagent has no conversation history. This is not a fork of the conversation (compare forks in [subagents.md](subagents.md)).
- Runs in the background by default since v2.1.218 (before that it blocked). Runs in the foreground in `-p`/SDK runs, with `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`, or when fired by a scheduled task.
- Background forks get the restricted background tool set, and their edits bypass checkpoints.
- Added in v2.1.0 ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).

### Bundled skills

- Include `/doctor`, `/code-review`, `/batch`, `/debug`, `/loop`, `/claude-api`, `/run`, `/verify`, `/run-skill-generator`, `/simplify`, `/fewer-permission-prompts`, `/update-config`, `/workflow-authoring` (only when workflows are enabled), `/dataviz`, `/design`, `/slides`, and `/artifact-*`. They are "prompt-based", unlike built-in commands, which "execute fixed logic" ([skills](https://code.claude.com/docs/en/skills); [commands](https://code.claude.com/docs/en/commands)).
- Since v2.1.286, a local skill named `verify` or `simplify` (non-plugin, model-invocable) makes Claude run it before each commit ([skills](https://code.claude.com/docs/en/skills)).

## Example

`~/.claude/skills/summarize-changes/SKILL.md` ([skills](https://code.claude.com/docs/en/skills)):

```markdown
---
description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
---
## Current changes
!`git diff HEAD`
## Instructions
Summarize the changes above in two or three bullet points, then list any risks.
```

## Limits and gotchas

- `allowed-tools` grants, it does not restrict. To remove tools, use `disallowed-tools` ([skills](https://code.claude.com/docs/en/skills)).
- Security: workspace trust does not gate `allowed-tools`. A project skill can grant itself tools even in an untrusted `-p` run ([skills](https://code.claude.com/docs/en/skills)).
- Under `allowManagedPermissionRulesOnly` (v2.1.282+), the `allowed-tools` field of project and personal skills is ignored ([skills](https://code.claude.com/docs/en/skills)).
- `hooks` in skill frontmatter persist for the whole session after invocation, not just the skill's turn ([skills](https://code.claude.com/docs/en/skills); [hooks](https://code.claude.com/docs/en/hooks)).
- Contradiction (spec vs Claude Code): `name` is required and must match the directory in the spec, but optional in Claude Code; `description` caps differ (1024 vs 1,536 combined with `when_to_use`); `allowed-tools` syntax differs (`Bash(git:*)` vs `Bash(git *)`) ([Agent Skills spec](https://agentskills.io/specification); [skills](https://code.claude.com/docs/en/skills)).
- Claude Code-only frontmatter keys cause a hard error when uploaded to claude.ai, the Skills API, or `package_skill.py` ([skills](https://code.claude.com/docs/en/skills)).
- A plugin's `CLAUDE.md` is not loaded; put plugin instructions in a skill ([plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference)).
- The old `slash-commands` docs URL serves the skills page ([slash-commands](https://code.claude.com/docs/en/slash-commands)).
- Gap (research notes): the pre-v2.1.x history of skills (introduced as "Agent Skills" in 2025) was not traced in the changelog. Only "2.0.43 — skills frontmatter field for subagents" and "2.1.0 — `context: fork`" were confirmed ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- Gap (research notes): the `skills-ref` tool's behavior and the anthropics/skills repo contents were not fetched.

## Sources

- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/slash-commands
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/scheduled-tasks
- https://code.claude.com/docs/en/plugins/manifest-reference
- https://agentskills.io/specification
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- Local CLI help: `claude --help` (v2.1.289)
