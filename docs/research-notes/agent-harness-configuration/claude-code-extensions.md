# Claude Code extension mechanisms: skills, slash commands, subagents, hooks, workflows/automation (as of Claude Code 2.1.289, 2026-10-04)

Method note: all claims below come from the official docs at code.claude.com (fetched as Markdown on 2026-10-04), the anthropics/claude-code CHANGELOG.md (latest entry 2.1.289), the agentskills.io specification, and the locally installed `claude --help` (version 2.1.289, read-only). Doc URLs are of the form `https://code.claude.com/docs/en/<page>`. Version numbers like "v2.1.218+" are as stated in the docs.

## Skills (SKILL.md format, frontmatter, locations, discovery/invocation, Agent Skills standard)

### Takeaway
A skill is a directory with a `SKILL.md` (YAML frontmatter + Markdown instructions) plus optional supporting files. Only its name and description sit in context until it is invoked (progressive disclosure). The user can invoke it as `/name` and Claude can invoke it through the Skill tool. Claude Code follows the Agent Skills open standard (agentskills.io) and adds many Claude Code-only frontmatter fields (invocation control, `context: fork`, hooks, `paths`, arguments, model and effort overrides). Custom slash commands are now a legacy form of skills.

### Cited Findings

**What it is and what problem it solves**
- "Create a `SKILL.md` file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you can invoke one directly with `/skill-name`." The docs recommend a skill when you keep pasting the same instructions or procedure into chat, or when CLAUDE.md content has become a procedure. "Unlike CLAUDE.md content, a skill's body loads only when it's used." — [Skills](https://code.claude.com/docs/en/skills)
- Claude Code skills "follow the Agent Skills open standard, which works across multiple AI tools. Claude Code extends the standard with additional features like invocation control, subagent execution, and dynamic context injection." — [Skills](https://code.claude.com/docs/en/skills)

**Locations / scopes** (all from [Skills](https://code.claude.com/docs/en/skills))
- Enterprise: `.claude/skills/<skill-name>/SKILL.md` in the managed settings directory. Applies to all users on machines where the organization deploys it.
- Personal: `~/.claude/skills/<skill-name>/SKILL.md`. Loads in all your projects on that machine, but not in Cowork or cloud sessions.
- Project: `.claude/skills/<skill-name>/SKILL.md`. Commit it to share.
- Nested: `<subdir>/.claude/skills/<skill-name>/SKILL.md`. Loads for sessions started in or below `<subdir>`. A session started above it loads the skill only once Claude reads or edits a file in that subdirectory, or after `/add-dir` (v2.1.257+).
- Additional directory: `.claude/skills/` inside an `--add-dir` directory. `permissions.additionalDirectories` grants file access only and loads no skills.
- Plugin: `<plugin>/skills/<skill-name>/SKILL.md`, namespaced as `/plugin-name:skill-name`.
- claude.ai account: skills enabled on the account are synced into `~/.claude/skills/synced/` (v2.1.273+). The folder name `synced` is reserved, and so is the namespace `anthropic-skills:*`.
- Project skills load from the start directory and from every parent directory up to the repo root. A symlinked skill folder is allowed. Adding `.claude-plugin/plugin.json` to a skill folder turns it into a plugin named `<name>@skills-dir`.
- Name precedence: enterprise > personal > project. A skill beats a `.claude/commands/` file with the same name. Your skill replaces a bundled skill or built-in command of the same name, but not its aliases. Plugin skills never collide because they are namespaced.
- Live change detection: edits under `~/.claude/skills/`, the project `.claude/skills/`, and `--add-dir` skills apply mid-session. A top-level skills directory created after startup needs `/reload-skills`. Bare mode does not watch for changes.
- Cloud sessions and routines do not read `~/.claude/skills/`. They load claude.ai-enabled skills plus skills committed to the cloned repo. — [Skills](https://code.claude.com/docs/en/skills)

**Frontmatter reference (Claude Code)** — [Skills](https://code.claude.com/docs/en/skills)
- All fields are optional; `description` is recommended. Unknown fields are ignored silently. Frontmatter is read only if the opening `---` is the first line. If the YAML is invalid, the skill loads with no fields set. Since v2.1.218, booleans accept yes/no/on/off/1/0.
- `name`: the command name; defaults to the directory name.
- `description`: what the skill does and when to use it; defaults to the first non-empty body line. `description` + `when_to_use` are truncated together at 1,536 chars in the listing.
- `when_to_use`: trigger phrases, appended to the description.
- `argument-hint`: autocomplete hint such as `[issue-number]`.
- `arguments`: named positional args for `$name` substitution.
- `disable-model-invocation`: when true, Claude cannot invoke the skill and its description is not in context. It also blocks preloading into subagents and, since v2.1.196, running from a scheduled task.
- `user-invocable`: when false, the skill is hidden from the `/` menu and only Claude can invoke it.
- `allowed-tools`: tools approved without prompting during the invoking turn; the grant clears at the next user message. It does not restrict which tools are available.
- `disallowed-tools`: removes tools while the skill is active.
- `model`: model for the rest of the turn, or `inherit`. With `context: fork` it sets the subagent's model.
- `effort`: low / medium / high / xhigh / max.
- `context`: `fork` runs the skill in a subagent.
- `agent`: the subagent type used for the fork (default `general-purpose`).
- `background`: only with `fork`; default true; v2.1.218+.
- `hooks`: hooks registered on invocation that persist for the rest of the session.
- `paths`: globs that limit auto-activation to matching files.
- `shell`: `bash` (default) or `powershell`.
- `metadata`: free-form map that Claude Code ignores.
- `license` and `compatibility`: Agent Skills spec fields, accepted but not acted on. `compatibility` is at most 500 chars.

**String substitutions** — [Skills](https://code.claude.com/docs/en/skills)
- `$ARGUMENTS`; `$ARGUMENTS[N]` / `$N` (0-based, shell-style quoting); `$name` from `arguments`; `${CLAUDE_SESSION_ID}`; `${CLAUDE_EFFORT}`; `${CLAUDE_SKILL_DIR}`; `${CLAUDE_PROJECT_DIR}` (v2.1.196+); and, in plugin skills only, `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}`.
- If no placeholder receives the arguments, Claude Code appends `ARGUMENTS: <value>`.
- `${CLAUDE_SKILL_DIR}` is also substituted inside `allowed-tools` Bash rules, so a bundled script can run without a prompt, e.g. `allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *)`.
- `${CLAUDE_SKILL_DIR}` was added in v2.1.69. — [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

**Dynamic context injection (Claude Code-only)** — [Skills](https://code.claude.com/docs/en/skills)
- `` !`cmd` `` (at line start or after whitespace) or a fenced ```` ```! ```` block runs the shell command before Claude sees the skill and inlines its output. Output is not re-scanned for further commands.
- A failing command (non-zero exit; exit 1 is tolerated for search/diff commands) aborts the whole invocation.
- Injected commands never prompt. A deny rule, or outside auto mode any non-allow result, aborts the invocation.
- `"disableSkillShellExecution": true` replaces each command with `[shell command execution disabled by policy]`. Bundled and managed skills are exempt.
- Skills synced from claude.ai never run `!` commands locally.

**Loading, context cost, lifecycle** — [Skills](https://code.claude.com/docs/en/skills)
- Default behavior: the description is always in context and the full skill loads on invocation. With `disable-model-invocation: true`, the description is not in context. With `user-invocable: false`, the description stays in context.
- The skill listing's character budget is 1% of the model's context window. On overflow, descriptions of the least-invoked skills are dropped first, but names are always kept. Tunable via `skillListingBudgetFraction`, `SLASH_COMMAND_TOOL_CHAR_BUDGET`, and `skillListingMaxDescChars`.
- `/skill-doctor` (v2.1.252+) reports each skill's cost and usage.
- The rendered SKILL.md enters the conversation as one message and stays there. It is not re-read on later turns. Re-invoking with identical content adds only a note.
- After auto-compaction, the most recent invocation of each skill is re-attached: first 5,000 tokens each, 25,000 tokens combined.
- Tip: keep `SKILL.md` under 500 lines and move detail into supporting files referenced from SKILL.md. Scripts are "executed, not loaded".

**Invocation** — [Skills](https://code.claude.com/docs/en/skills)
- A user runs a skill with `/name` at the start of a message. `/name` after plain text only grants permission.
- Up to six skills can be stacked: `/a /b args`. Since v2.1.199, the trailing text goes to each. — [Commands](https://code.claude.com/docs/en/commands)
- Claude invokes skills via the Skill tool. Permission rules can control this: `Skill` (deny all), `Skill(name)`, `Skill(name *)`.
- The `skillOverrides` setting accepts `on` / `name-only` / `user-invocable-only` / `off` per skill (not for plugin skills).
- `disableBundledSkills` turns off bundled skills.
- Under `allowManagedPermissionRulesOnly` (v2.1.282+), the `allowed-tools` field of project and personal skills is ignored.
- Security: workspace trust does not gate `allowed-tools`. A project skill can grant itself tools even in an untrusted `-p` run.

**`context: fork`** — [Skills](https://code.claude.com/docs/en/skills)
- Starts a new subagent of type `agent` with the skill content as its prompt. The subagent has no conversation history.
- It runs in the background by default (since v2.1.218; before that it blocked). It runs in the foreground in `-p`/SDK runs, with `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`, or when fired by a scheduled task.
- Background forks get the restricted background tool set, and their edits bypass checkpoints.
- This is not a fork of the conversation.
- Added in v2.1.0. — [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

**Bundled skills**
- Bundled skills include `/doctor`, `/code-review`, `/batch`, `/debug`, `/loop`, `/claude-api`, `/run`, `/verify`, `/run-skill-generator`, `/simplify`, `/fewer-permission-prompts`, `/update-config`, `/workflow-authoring` (only when workflows are enabled), `/dataviz`, `/design`, `/slides`, and `/artifact-*`. They are "prompt-based", unlike built-in commands, which "execute fixed logic". — [Skills](https://code.claude.com/docs/en/skills); [Commands](https://code.claude.com/docs/en/commands)
- Since v2.1.286, a local skill named `verify` or `simplify` (non-plugin, model-invocable) makes Claude run it before each commit. — [Skills](https://code.claude.com/docs/en/skills)

**Agent Skills open standard (agentskills.io)** — [Agent Skills specification](https://agentskills.io/specification)
- Directory: `skill-name/SKILL.md` (required) plus optional `scripts/`, `references/`, `assets/`.
- Required frontmatter:
  - `name`: 1–64 chars, lowercase a–z/0–9/hyphen, no leading, trailing, or double hyphen, and it must match the parent directory name.
  - `description`: 1–1024 chars.
- Optional frontmatter: `license`, `compatibility` (≤500 chars), `metadata` (string→string map), and `allowed-tools` (space-separated, "Experimental").
- Progressive disclosure: metadata (~100 tokens) loads at startup; instructions (<5000 tokens recommended) load on activation; resources load as needed.
- Keep SKILL.md under 500 lines and file references one level deep.
- Validate with `skills-ref validate ./my-skill`.
- Distribution limits: claude.ai uploads, the Skills API, and `package_skill.py` from anthropics/skills accept only `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. Other keys cause a hard error ("Unexpected key(s) in SKILL.md frontmatter…"). Dynamic context injection does not work in claude.ai chat or the API. — [Skills](https://code.claude.com/docs/en/skills)

**Minimal example** — [Skills](https://code.claude.com/docs/en/skills)
```yaml
# ~/.claude/skills/summarize-changes/SKILL.md
---
description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
---
## Current changes
!`git diff HEAD`
## Instructions
Summarize the changes above in two or three bullet points, then list any risks.
```

### Inferences
- The spec and Claude Code disagree in a few places:
  - The spec requires `name` and that it match the directory. Claude Code makes `name` optional, defaults it to the directory name, and lets it override the command name.
  - The spec caps `description` at 1024 chars. Claude Code's listing cap is 1,536 chars for `description` + `when_to_use` combined.
  - The spec's `allowed-tools` example uses `Bash(git:*)` syntax. Claude Code docs use permission-rule syntax `Bash(git *)`.
  - For portability, stick to the six spec fields and spec-valid names.
- Two quantitative costs drive context budgeting: the per-skill listing entry (always paid unless `disable-model-invocation` or `name-only` applies) and the persistent body after invocation, which compaction re-attaches.

### Gaps
- The exact pre-v2.1.x history of skills (introduced as "Agent Skills" in 2025) was not traced in the changelog. Only "2.0.43 — skills frontmatter field for subagents" and "2.1.0 — `context: fork`" were confirmed.
- The `skills-ref` tool's behavior and the anthropics/skills repo contents were not fetched.

## Slash commands (built-in vs custom, `.claude/commands`, arguments, frontmatter, bash/file inclusion)

### Takeaway
Custom slash commands were merged into skills in v2.1.3. `.claude/commands/<name>.md` still works and takes the same frontmatter as skills except `name` and `paths`. Skills are preferred because they support a directory of supporting files. Built-in commands (e.g. `/compact`, `/model`) run fixed logic. Bundled skills (e.g. `/loop`, `/batch`) are prompts. The old `slash-commands` docs URL now serves the skills page.

### Cited Findings
- "**Custom commands have been merged into skills.** A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Your existing `.claude/commands/` files keep working." — [Skills](https://code.claude.com/docs/en/skills)
- The changelog for 2.1.3 says "Merged slash commands and skills, simplifying the mental model with no change in behavior". — [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- `https://code.claude.com/docs/en/slash-commands.md` returns byte-identical content to the skills page (verified with `cmp` on 2026-10-04). The Agent SDK "slash-commands" page likewise returns the SDK skills page. — [slash-commands](https://code.claude.com/docs/en/slash-commands); [Agent SDK skills](https://code.claude.com/docs/en/agent-sdk/skills)
- Command files are "the older format and still work". They support the same frontmatter except `name` and `paths`. — [Skills](https://code.claude.com/docs/en/skills)
- Naming: `.claude/commands/deploy.md` gives `/deploy`. Subdirectories give colon namespaces: `.claude/commands/frontend/component.md` gives `/frontend:component`. A skill wins over a command file with the same name. — [Skills](https://code.claude.com/docs/en/skills)
- Arguments work as in skills: `$ARGUMENTS`, `$ARGUMENTS[N]`, `$N` (0-based in current docs, e.g. `$0` is the first argument), and `$name` via `arguments`. A backslash escapes a literal `\$1.00`. — [Skills](https://code.claude.com/docs/en/skills)
- Bash inclusion uses `` !`cmd` `` or ```` ```! ```` blocks. `@path` file references are attached for local skills and command files; for synced skills, `@` references are not attached. — [Skills](https://code.claude.com/docs/en/skills)
- Built-in commands vs bundled skills:
  - "A command is only recognized at the start of your message."
  - The commands table marks bundled prompt-based entries as **Skill** and `/deep-research` as **Workflow**.
  - Examples of built-ins: `/agents`, `/hooks`, `/rewind` (aliases `/checkpoint`, `/undo`), `/plan`, `/tasks`, `/subtask`, `/fork`, `/background` (`/bg`), `/schedule` (`/routines`), `/goal`, `/workflows`, `/reload-skills`, `/skills`, `/skill-doctor`, `/install-github-app`, `/security-review`, `/init`.
  - Commands sent mid-response are queued.
  - Source: [Commands](https://code.claude.com/docs/en/commands)
- A few built-in commands, such as `/init` and `/security-review`, are callable through the Skill tool; others, such as `/compact`, are not. — [Skills](https://code.claude.com/docs/en/skills)
- MCP prompts appear as commands (`/mcp__<server>__<prompt>`). — [Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks); [Skills](https://code.claude.com/docs/en/skills)
- Plugin commands: `commands/<file>.md` gives `/<plugin>:<file>`. They can also be defined inline in `plugin.json` under `commands`, e.g. `{"about": {"content": "...", "description": "..."}}`. "Commands are the older format, and skills supersede them for new work." — [Plugin components](https://code.claude.com/docs/en/plugins/components)
- `--disable-slash-commands` disables all skills (per `claude --help`, v2.1.289). — local `claude --help`

**Minimal example (legacy command)**
```markdown
<!-- .claude/commands/fix-issue.md  ->  /fix-issue 123 -->
---
description: Fix a GitHub issue
argument-hint: [issue-number]
disable-model-invocation: true
---
Fix GitHub issue $ARGUMENTS following our coding standards.
```
(Field set and semantics per [Skills](https://code.claude.com/docs/en/skills).)

### Inferences
- Any tutorial that treats `.claude/commands/` as a distinct feature with its own frontmatter (e.g. a separate `allowed-tools` semantic) should be treated as outdated.

### Gaps
- I did not find documentation of how `$1` was numbered before the merge (0- or 1-based).

## Subagents (`.claude/agents`, frontmatter, built-ins, Agent tool, isolation, nesting, `--agents`, teams, background, forking)

### Takeaway
A subagent is a Markdown file with YAML frontmatter; the body becomes its system prompt. It runs in its own context window and returns one summary to the caller. Scopes: managed > `--agents` > project > user > plugin. The Agent tool (renamed from Task in v2.1.63) spawns subagents.

Current behavior:
- Background by default; fork mode is on by default in interactive sessions.
- Nesting up to 3 layers; at most 20 concurrent subagents.
- `SendMessage` resumes a finished subagent.
- Optional worktree isolation per subagent.

Related multi-agent features:
- Agent teams: experimental, behind an environment flag.
- Agent view and background sessions.
- Dynamic workflows: script-orchestrated fan-out.

### Cited Findings

**Purpose, cost, and context**
- Use a subagent "when a side task would flood your main conversation with search results, logs, or file contents you won't reference again". Each runs "in its own context window with a custom system prompt, specific tool access, and independent permissions".
- Descriptions consume context. A warning appears when combined custom-agent descriptions exceed 15,000 tokens.
- Source: [Subagents](https://code.claude.com/docs/en/sub-agents)

**Built-in subagents**
- **Explore**: read-only (Write and Edit denied). Uses the main model (or the opus alias when the main model is Fable on Anthropic auth). Takes a thoroughness level quick / medium / very thorough. Skips CLAUDE.md and git status.
- **Plan**: read-only, used in plan mode. Skips CLAUDE.md and git status.
- **general-purpose**: every tool available to subagents.
- **claude**: catch-all; also the default for background sessions.
- **statusline-setup** (Sonnet) and **claude-code-guide** (Haiku).
- Controls: `CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1` (v2.1.198+) removes Explore and Plan. `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1` removes all built-ins in `-p`/SDK runs. `permissions.deny: ["Agent(Explore)"]` blocks one type.
- Source: [Subagents](https://code.claude.com/docs/en/sub-agents)

**Locations and priority** — [Subagents](https://code.claude.com/docs/en/sub-agents)
1. Managed settings `.claude/agents/`
2. `--agents` CLI JSON (session only)
3. Project `.claude/agents/`: walks up to the repo root; the closest definition wins
4. User `~/.claude/agents/`
5. Plugin `agents/`

Additional rules:
- Directories are scanned recursively. In project and user scopes, identity comes only from `name`. In plugins, subfolders become part of the ID, e.g. `my-plugin:review:security`.
- The file watcher picks up edits within seconds. A newly created `agents` directory and `--add-dir` agents need a restart.
- On v2.1.197 and earlier, `/agents` was an interactive wizard. Now it only prints a reminder to ask Claude or edit files.

**Frontmatter (camelCase; unknown fields ignored; only `name` and `description` required)** — [Subagents](https://code.claude.com/docs/en/sub-agents)
- `name`: no `:` allowed (v2.1.218+), and must not start with `-`.
- `description`: when Claude should delegate.
- `tools`: allowlist; inherits all subagent tools if omitted.
- `disallowedTools`: denylist, applied first. An entry like `Bash(git push *)` removes the whole tool. MCP patterns `mcp__server` and `mcp__*` are supported.
- `model`: sonnet / opus / haiku / fable / full ID / `inherit`.
- `permissionMode`: default / acceptEdits / auto / dontAsk / bypassPermissions / plan / `manual` (an alias for default).
- `maxTurns`: when hit, output is marked partial (v2.1.246+).
- `skills`: preloads full skill content at startup.
- `mcpServers`: a name reference or an inline definition (stdio / http / sse / ws).
- `hooks`: scoped to the subagent; `Stop` becomes `SubagentStop`.
- `memory`: user / project / local.
- `background`: true keeps the subagent in the background.
- `omitClaudeMd`: v2.1.271+.
- `effort`.
- `isolation`: `worktree`.
- `color`: red / blue / green / yellow / purple / orange / pink / cyan.
- `initialPrompt`: only when the agent runs as the main session.
- `experimental.cacheTtl`: `5m` or `1h` (v2.1.248+).

Files without `name`, without `description`, or with invalid YAML are skipped silently (the reason goes to the debug log). `claude plugin validate .claude/agents` checks them (v2.1.233+).

**Plugin agents** — [Subagents](https://code.claude.com/docs/en/sub-agents); [Plugin components](https://code.claude.com/docs/en/plugins/components)
- For security, `hooks`, `mcpServers`, `permissionMode`, and `initialPrompt` are ignored in plugin agents.

**`--agents` JSON**
- Format: `{"name": {"description","prompt","tools",...}}`.
- Accepts the frontmatter fields `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `omitClaudeMd`, and `isolation`. `color` and `experimental` are ignored.
- In `-p` mode it also accepts a file path (v2.1.281+).
- `--agents` was introduced in 2.0.0.
- Sources: [Subagents](https://code.claude.com/docs/en/sub-agents); [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

**Model resolution** — [Subagents](https://code.claude.com/docs/en/sub-agents)
- Order: per-invocation `model` parameter > frontmatter `model` > `CLAUDE_CODE_SUBAGENT_MODEL` > main model. Before v2.1.251 the environment variable came first.
- `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` (v2.1.257+) forces one model on all subagents, teammates, and workflow agents.
- Subagents inherit the main conversation's extended-thinking setting (v2.1.198+).

**Tools available to subagents** — [Subagents](https://code.claude.com/docs/en/sub-agents)
- Always removed: `AskUserQuestion`, `EndConversation`, `EnterPlanMode`, `ExitPlanMode` (unless `permissionMode: plan`), `ScheduleWakeup`, `WaitForMcpServers`, `Workflow`, and `Agent` at the depth limit.
- Background subagents keep only these built-ins: Read, Grep, Glob, LSP, Bash, PowerShell, Edit, Write, NotebookEdit, WebFetch, WebSearch, TodoWrite, Skill, ToolSearch, EnterWorktree, ExitWorktree, Monitor, TaskStop, SendMessage, Artifact, and SubagentHandback. They keep all MCP tools.
- `Agent(worker, researcher)` in `tools` restricts which agent types can be spawned, but only for an agent running as the main thread via `--agent`.

**Invocation** — [Subagents](https://code.claude.com/docs/en/sub-agents)
- Automatic delegation by description; "use proactively" in a description encourages it.
- Natural language, e.g. "Use the code-reviewer subagent…".
- @-mention: `@"code-reviewer (agent)"` or `@agent-<name>` / `@agent-<plugin>:<name>`.
- Session-wide: `claude --agent <name>` or `"agent": "<name>"` in settings. The agent's prompt replaces the default system prompt; CLAUDE.md still loads.

**Context isolation and results** — [Subagents](https://code.claude.com/docs/en/sub-agents)
- A non-fork subagent starts with:
  - its own system prompt plus environment details (not the Claude Code system prompt);
  - the delegation message;
  - the CLAUDE.md hierarchy, except for Explore/Plan or with `omitClaudeMd`;
  - a git status snapshot;
  - preloaded skills;
  - a sibling roster (v2.1.206+) when it has `SendMessage`.
- It does not get conversation history, the output style, or the main conversation's auto memory.
- Results come back as the final report. The report is scanned for instruction-shaped text (v2.1.210+) and arrives under a header marking it as subagent output with no user authority.
- Transcripts are stored at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`, retained per `cleanupPeriodDays` (default 30 days).

**Foreground vs background** — [Subagents](https://code.claude.com/docs/en/sub-agents)
- With fork mode on (the interactive default since v2.1.232), every spawned subagent runs in the background and `run_in_background` is removed from the tool.
- In `-p` and SDK runs (fork mode off), Claude chooses; the default is background.
- Ctrl+B backgrounds a running task.
- Permission prompts from background subagents surface in the main session.
- `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` forces foreground.

**Nesting and concurrency limits** — [Subagents](https://code.claude.com/docs/en/sub-agents)
- Nesting depth defaults to 3 layers below main, set via `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`; `1` disables nesting.
- History of the depth default: 5 layers, not configurable (v2.1.172–2.1.216); 1 (v2.1.217–218); 3 from v2.1.219.
- Concurrency: 20 running subagents, then "Concurrent subagent limit reached". Set via `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` (v2.1.217+). The limit is not enforced when ultracode is on.

**Resume, SendMessage, forks** — [Subagents](https://code.claude.com/docs/en/sub-agents)
- Claude resumes a finished subagent via `SendMessage` with the agent ID or name; full history is retained.
- Explore and Plan are one-shot and cannot be resumed.
- `SendMessage` does not require agent teams. No agent message counts as user approval.
- A fork (the `fork` subagent type) inherits the full conversation, system prompt, tools, model, and prompt cache. Start one manually with `/subtask` (v2.1.212+; `/fork` on v2.1.161–2.1.211).
- A fork cannot spawn further forks. `Agent(fork)` deny blocks forks. `CLAUDE_CODE_FORK_SUBAGENT=0/1` overrides the default.

**Memory and isolation** — [Subagents](https://code.claude.com/docs/en/sub-agents)
- `memory` stores files at `~/.claude/agent-memory/<name>/` (user), `.claude/agent-memory/<name>/` (project), or `.claude/agent-memory-local/<name>/` (local).
- The first 200 lines / 25KB of `MEMORY.md` are injected. Read, Write, and Edit are auto-enabled.
- `isolation: worktree` creates a temporary worktree from the default branch, auto-removed if unchanged. Git commands that escape to the main checkout are blocked.

**Rename and SDK**
- "In version 2.1.63, the Task tool was renamed to Agent. Existing `Task(...)` references in settings and agent definitions still work as aliases." — [Subagents](https://code.claude.com/docs/en/sub-agents)
- SDK: `agents` option with `AgentDefinition` (Python `claude_agent_sdk.AgentDefinition`; TypeScript `@anthropic-ai/claude-agent-sdk`). Fields mirror the frontmatter, and the Python SDK keeps camelCase keys. — [Agent SDK subagents](https://code.claude.com/docs/en/agent-sdk/subagents)

**Agent teams** — [Agent teams](https://code.claude.com/docs/en/agent-teams)
- Experimental, disabled by default; enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Added as a research preview in v2.1.32 ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- Structure: a lead plus teammates, which are separate Claude Code instances with their own context windows.
- Coordination:
  - Shared task list in `~/.claude/tasks/{team}/` (pending / in progress / completed, with dependencies; claims use file locks).
  - Mailbox at `~/.claude/teams/{team}/inboxes/{agent}.json`.
  - Team config at `~/.claude/teams/{team}/config.json`, removed at session end.
- Claude starts a teammate when it calls the Agent tool with a `name` while teams are enabled, without asking you.
- Interactive only; in `-p`/SDK runs no teammates are spawned.
- Display modes: in-process (default) or split panes (tmux / iTerm2), via `teammateMode` or `--teammate-mode`.
- Subagent definitions can be reused as teammate roles (`tools`, `model`, and body apply; `skills` do not).
- Hooks: `TeammateIdle`, `TaskCreated`, `TaskCompleted`.
- Limitations: no resume of in-process teammates; one team per session; no nested teams; fixed lead; no background subagents from in-process teammates; split panes are not supported in VS Code, Windows Terminal, or Ghostty.

**Other parallel features** — [Run agents in parallel](https://code.claude.com/docs/en/agents); [Agent view](https://code.claude.com/docs/en/agent-view); [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- The docs list five approaches: subagents, agent view, agent teams, dynamic workflows, and projects.
- Agent view (`claude agents`, research preview, added in v2.1.139) manages background sessions started via `claude --bg` or `/background`.
- `/fork` copies the session into a new background session.
- `/batch` splits work into 5–30 worktree-isolated subagents.

**Minimal example** — [Subagents](https://code.claude.com/docs/en/sub-agents)
```markdown
<!-- .claude/agents/code-reviewer.md -->
---
name: code-reviewer
description: Reviews code for quality and best practices. Use proactively after code changes.
tools: Read, Glob, Grep
model: sonnet
---
You are a code reviewer. Analyze the code and give specific, actionable feedback.
```

### Inferences
- Several defaults flipped across 2.1.2xx releases: fork-mode default, background-by-default, nesting depth, and model precedence. Older blog posts on "Task tool", foreground subagents, or "subagents cannot spawn subagents" are outdated.
- Agent teams and subagent naming interact. With teams enabled, any named subagent spawn becomes a teammate. This is a surprising coupling worth calling out to readers.

### Gaps
- I did not read the cross-session messaging page (`/docs/en/cross-session-messaging`) or the details of the agent view page (dispatch, permissions, worktree isolation for background sessions).
- I did not check the exact Agent tool input schema (parameters such as `subagent_type`, `name`, `model`, `isolation`, `run_in_background`) in the tools reference. The parameter names above are inferred from mentions in the subagents page.

## Hooks (events, matchers, handler types, input/output, exit codes, decision control, config locations, security)

### Takeaway
Hooks are deterministic handlers that the harness runs, not the model. They are configured as event → matcher group → handlers. The current release has:
- About 30 events.
- Five JSON-configured handler types: `command`, `http`, `mcp_tool`, `prompt`, and `agent` (experimental). Plugins can also register JavaScript "function hooks" as mods.

Control flows through exit codes (2 = block on blockable events) and JSON stdout (`hookSpecificOutput`, `decision`, `continue`, `additionalContext`, …). Hooks can be configured in settings files (user, project, local, managed), plugin `hooks/hooks.json`, skill frontmatter, and agent frontmatter.

### Cited Findings

**What hooks are**
- "Hooks are user-defined shell commands, HTTP endpoints, MCP tool calls, LLM prompts, or subagents that execute automatically at specific points in Claude Code's lifecycle."
- Plugins can also register JavaScript function hooks; such a plugin is a "mod" and is documented separately.
- Source: [Hooks reference](https://code.claude.com/docs/en/hooks)

**Events** — [Hooks reference](https://code.claude.com/docs/en/hooks)
- Session:
  - `SessionStart`: matchers startup / resume / clear / compact / fork.
  - `Setup`: fires on `--init-only`, or `--init` / `--maintenance` in `-p`; matchers init / maintenance.
  - `SessionEnd`: matchers clear / resume / logout / prompt_input_exit / other.
- Per turn:
  - `UserPromptSubmit`: also fires on turns Claude Code starts itself.
  - `UserPromptExpansion`: when a typed command expands; can block; matcher is the command name.
  - `Stop`.
  - `StopFailure`: on API errors; matchers rate_limit, overloaded, authentication_failed, …, cloud_credential_error, unknown.
- Agentic loop:
  - `PreToolUse`, `PermissionRequest`, `PermissionDenied` (auto-mode denials), `PostToolUse`, `PostToolUseFailure`.
  - `PostToolBatch`: after a parallel batch, before the next model call.
- Agents and tasks: `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `TeammateIdle`.
- Context and config:
  - `InstructionsLoaded`: CLAUDE.md or `.claude/rules` loaded.
  - `ConfigChange`: matchers user_settings, project_settings, local_settings, policy_settings, skills.
  - `CwdChanged`.
  - `DirectoryAdded`: v2.1.219.
  - `FileChanged`: the matcher lists filenames to watch.
  - `PreCompact` / `PostCompact`: matchers manual / auto.
  - `PreModelSwitch` / `PostModelSwitch`: added in v2.1.251.
- Worktrees: `WorktreeCreate` (replaces default git behavior; prints a path), `WorktreeRemove`.
- MCP: `Elicitation`, `ElicitationResult`.
- UI: `Notification`; matchers include permission_prompt, idle_prompt, auth_success, elicitation_*, agent_needs_input, agent_completed, quota_auto_resume_*.
- UI: `MessageDisplay`: display-only rewrite of streamed text; added in v2.1.152.
- Event addition versions are from the [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md).

**Configuration locations** — [Hooks reference](https://code.claude.com/docs/en/hooks)

| Location | Scope |
| :- | :- |
| `~/.claude/settings.json` | All your projects |
| `.claude/settings.json` | Project, shareable |
| `.claude/settings.local.json` | Project, local only |
| Managed policy settings | Organization |
| Plugin `hooks/hooks.json` | While the plugin is enabled |
| Skill frontmatter | Rest of the session once invoked; `once: true` supported |
| Subagent frontmatter | While that subagent runs |

- Hooks merge across levels rather than replacing each other.
- Settings, managed, and plugin hooks also fire inside subagents, with `agent_id` and `agent_type` in the input.
- `/hooks` is a read-only browser of configured hooks.
- `disableAllHooks` turns all hooks off, but cannot disable managed hooks unless set in managed settings.
- `allowManagedHooksOnly` blocks user, project, local, and plugin hooks.
- `allowedHttpHookUrls` and `httpHookAllowedEnvVars` constrain HTTP hooks.

**Matchers** — [Hooks reference](https://code.claude.com/docs/en/hooks)
- `*`, `""`, or omitted matches all.
- Letters, digits, `_`, `-`, space, `,`, and `|` only: exact names or a list (`Edit|Write`, `Edit, Write`).
- Anything else: an unanchored JavaScript regex (`^Notebook`, `mcp__memory__.*`).
- MCP tools are named `mcp__<server>__<tool>`; plugin MCP tools are `mcp__plugin_<plugin>_<server>__<tool>`. `mcp__memory` alone matches nothing.
- Events with no matcher support: UserPromptSubmit, PostToolBatch, Stop, TeammateIdle, TaskCreated, TaskCompleted, WorktreeCreate, WorktreeRemove, MessageDisplay, CwdChanged.
- The per-handler `if` field takes one permission rule, e.g. `"Bash(git *)"` or `"Edit(*.ts)"`. It is evaluated only on tool events and is best-effort; "use the permission system rather than a hook to enforce a hard allow or deny."

**Handler fields** — [Hooks reference](https://code.claude.com/docs/en/hooks)
- Common:
  - `type`.
  - `if`.
  - `timeout`: defaults are 600s for command / http / mcp_tool, 30s for prompt, and 60s for agent. Lowered to 30s on UserPromptSubmit and Pre/PostModelSwitch, and 10s on MessageDisplay. SessionEnd hooks share a 1.5s budget, raised up to 60s if configured.
  - `statusMessage`.
  - `once`: honored only in skill frontmatter.
- `command`:
  - `command`, plus `args` for exec form with no shell.
  - `async`, `asyncRewake` (wakes Claude on exit 2).
  - `shell`: bash or powershell.
  - Placeholders: `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`.
- `http`: `url`, `headers`, and `allowedEnvVars`, which is required for `$VAR` interpolation in headers. HTTP hooks were added in v2.1.63 ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- `mcp_tool`: `server`, `tool`, and `input` with `${tool_input.file_path}`-style substitution. Added in v2.1.118 ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- `prompt` / `agent`: `prompt` (with `$ARGUMENTS` for the input JSON) and `model`. Prompt hooks also accept `continueOnBlock`.
- All matching handlers run in parallel. Identical handlers defined in more than one settings file run once.

**Handler-type support by event** — [Hooks reference](https://code.claude.com/docs/en/hooks)
- All five types: PermissionDenied, PostToolBatch, PostToolUse, PostToolUseFailure, PreToolUse, Stop, SubagentStop, TaskCompleted, TaskCreated, TeammateIdle, UserPromptExpansion, UserPromptSubmit.
- PermissionRequest: everything except `agent`.
- command / http / mcp_tool only: ConfigChange, CwdChanged, DirectoryAdded, Elicitation, ElicitationResult, FileChanged, InstructionsLoaded, MessageDisplay, Notification, PostCompact, PostModelSwitch, PreCompact, PreModelSwitch, SessionEnd, StopFailure, SubagentStart, WorktreeCreate, WorktreeRemove.
- SessionStart and Setup: command and mcp_tool only. mcp_tool is skipped at launch because servers are not yet connected.

**Input JSON** — [Hooks reference](https://code.claude.com/docs/en/hooks)
- Command hooks receive it on stdin; HTTP hooks receive it as the POST body.
- Common fields: `session_id`, `prompt_id` (v2.1.196+), `transcript_path`, `cwd`, `scratchpad_dir` (v2.1.257+), `permission_mode`, `effort.level`, `hook_event_name`, plus `agent_id` / `agent_type` inside subagents or with `--agent`.
- Tool events add `tool_name`, `tool_input`, and `tool_use_id`.
- Stop adds `stop_hook_active`, `last_assistant_message`, `background_tasks`, and `session_crons`.

**Exit codes** — [Hooks reference](https://code.claude.com/docs/en/hooks)
- 0: success, and the code to use when printing JSON. Stdout is added as context only for UserPromptSubmit, UserPromptExpansion, SessionStart, and PostModelSwitch; elsewhere it goes to the debug log.
- 2: blocking error. Stderr (or the JSON reason) is the message, and JSON `allow` cannot override it. Effect by event:
  - PreToolUse blocks the tool call.
  - UserPromptSubmit rejects the prompt.
  - Stop and SubagentStop force Claude to continue.
  - TaskCreated rolls back the task.
  - PreCompact blocks compaction.
  - ConfigChange blocks the change (except policy_settings).
  - PostToolBatch stops the loop.
  - PreModelSwitch blocks the switch.
  - PermissionRequest ignores exit 2.
  - PostToolUse only shows stderr to Claude.
- Other codes are non-blocking errors. "Claude Code treats exit code 1 as a non-blocking error and proceeds… If your hook is meant to enforce a policy, use `exit 2`."
- WorktreeCreate and WorktreeRemove fail on any non-zero exit code.
- A missing script exits 127, which is non-blocking and silently disables the gate.
- A timed-out command hook on PreToolUse does not block. An SDK callback hook that times out does block.

**JSON output and decision control** — [Hooks reference](https://code.claude.com/docs/en/hooks)
- Universal fields:
  - `continue` (false stops Claude).
  - `stopReason`.
  - `systemMessage`.
  - `suppressOutput` (accepted but has no effect).
  - `terminalSequence` (an allowlist of OSC 0/1/2/9/99/777 and BEL).
- `additionalContext` arrives as a system reminder. Each string is capped at 10,000 chars; overflow is saved to a file and a 2,000-char preview is passed instead.
- Top-level `decision: "block"` + `reason`: UserPromptSubmit, UserPromptExpansion, PostToolUse, PostToolUseFailure, PostToolBatch, Stop, SubagentStop, ConfigChange, PreCompact.
- PreToolUse uses `hookSpecificOutput.permissionDecision`:
  - Values allow / deny / ask / defer; precedence deny > defer > ask > allow.
  - Also takes `permissionDecisionReason`, `updatedInput`, and `additionalContext`.
  - The older top-level `decision` / `reason` (`approve` / `block`) are deprecated for PreToolUse.
  - Deny and ask permission rules are still evaluated regardless.
  - `defer` works only in `-p`; the run exits with `stop_reason: "tool_deferred"`.
- PermissionRequest: `decision.behavior` allow/deny, plus `updatedInput`, `updatedPermissions`, `message`, `interrupt`.
- PostToolUse: `updatedToolOutput`, `classifierContext`.
- SessionStart: `additionalContext`, `initialUserMessage`, `sessionTitle`, `watchPaths`, `reloadSkills`.
- WorktreeCreate: prints the path (HTTP hooks return `hookSpecificOutput.worktreePath`).
- PermissionDenied: `retry: true`.
- Stop loop guard: `stop_hook_active` plus a cap of 8 consecutive continuations (`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`).

**Prompt and agent hooks** — [Hooks reference](https://code.claude.com/docs/en/hooks)
- Prompt hooks expect the model to return `{"ok": bool, "reason": "...", "impossible": bool}`. They default to the background model.
- On PreToolUse, `ok: false` denies the call and by default ends the turn (since v2.1.210). Set `continueOnBlock: true` to return the reason to Claude instead.
- Agent hooks are "experimental": a subagent with Read, Grep, Glob, and similar tools, up to 50 turns, returning `{ok}`.

**Async hooks** — [Hooks reference](https://code.claude.com/docs/en/hooks)
- `async: true` (command type only) cannot block.
- Its `additionalContext` and `systemMessage` are delivered on the next turn.
- Async hooks are killed at teardown in `-p`, and there is no deduplication.

**Security** — [Hooks reference](https://code.claude.com/docs/en/hooks)
- "Command hooks execute shell commands with your full user permissions."
- Interactive sessions hold back settings-file hooks until the workspace trust dialog is accepted.
- In `-p` and SDK sessions the folder is treated as trusted, so a repo's `.claude/settings.json` hooks run. Mitigations: use `--bare` or `--settings '{"disableAllHooks": true}'`.
- Frontmatter hooks in project subagents require trust of the agent file's folder (v2.1.218+), and `-p` does not count as trust.
- Best practices: validate input, quote variables, block path traversal, use absolute paths, skip sensitive files.

**SDK hooks** — [Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks)
- The SDK registers callback functions in `options.hooks`, e.g. Python `HookMatcher(matcher="Write|Edit", hooks=[cb])`. They run alongside settings-file command hooks when `settingSources` includes those settings.

**Minimal example** — [Hooks reference](https://code.claude.com/docs/en/hooks)
```json
{ "hooks": { "PostToolUse": [ { "matcher": "Edit|Write",
  "hooks": [ { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/check-style.sh", "args": [] } ] } ] } }
```

### Inferences
- The most common bugs readers will hit:
  - Using exit 1 instead of 2 for a policy gate.
  - Matching `mcp__server` without `__.*`.
  - Expecting `if` to be a hard security boundary.
  - Assuming `-p` respects workspace trust.
- Hooks in skill frontmatter persist for the whole session after invocation, not just the skill's turn. Subagent hooks are scoped to that subagent's lifetime.

### Gaps
- I did not read every per-event input schema in full: PreModelSwitch canonical naming, FileChanged watch semantics, Elicitation fields, MessageDisplay output.
- I skimmed the hooks guide (`/docs/en/hooks-guide`) only through the reference.
- I did not read the mods docs (function hooks in JavaScript) beyond the one-line description.

## Workflows / automation (headless, Agent SDK, GitHub Actions, scheduling, worktrees, plan mode, checkpoints, orchestration)

### Takeaway
Automation surfaces:
- **Headless runs:** `claude -p` with `--output-format text|json|stream-json`, `--json-schema`, `--allowedTools`, and `--permission-mode`. `--bare` is recommended for CI and is slated to become the `-p` default.
- **Agent SDK:** Python and TypeScript libraries that run the same harness.
- **GitHub Actions:** `anthropics/claude-code-action@v1`.

Scheduling:
- `/loop` and cron tools: in-session, 7-day expiry.
- Desktop scheduled tasks: run locally.
- Routines (`/schedule`): cloud; schedule, API, and GitHub triggers; research preview.

In-session safety and parallelism:
- Worktrees (`--worktree`).
- Plan mode.
- Checkpoints (`/rewind`).

Orchestration:
- Dynamic workflows: JavaScript scripts that fan out up to 1,000 agents per run, triggered by `ultracode`.
- Plugins: packaging for skills, agents, hooks, MCP, workflows, and monitors.

### Cited Findings

**Headless / `-p`** — [Headless](https://code.claude.com/docs/en/headless)
- Basic form: `claude -p "…" --allowedTools "Read,Edit,Bash"`. Exit code 0 means success.
- Output formats: `text` (default), `json` (with `result`, `session_id`, `total_cost_usd`), and `stream-json` (NDJSON; add `--verbose --include-partial-messages` for token streaming).
- `--json-schema` puts schema-validated output in `structured_output`. Since v2.1.205, an invalid schema is an error rather than being ignored.
- `--allowedTools` uses permission-rule syntax: `Bash(git diff *)`, where the space before `*` matters.
- `--permission-mode`: auto, dontAsk, acceptEdits, or plan.
- `--permission-prompts none` (v2.1.259+) for unattended runs.
- `--append-system-prompt` / `--system-prompt`.
- `--continue` / `--resume <id>`.
- `--bare`:
  - Skips auto-discovery of hooks, skills, commands, agents, plugins, MCP, auto memory, and CLAUDE.md.
  - Requires `ANTHROPIC_API_KEY` or an `apiKeyHelper`; no OAuth.
  - "is the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release."
- `claude --help` (2.1.289) lists further flags: `--max-budget-usd` (with `--print`), `--input-format`, `--agents <json-or-file>`, `--plugin-dir`, `--setting-sources`, `--safe-mode`, `--bg/--background`, `-w/--worktree`. — local `claude --help`

**Agent SDK**
- "The Claude Code SDK is now the Claude Agent SDK" (2.0.0). — [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- It "gives you the same tools, agent loop, and context management that power Claude Code" in Python and TypeScript.
- Capabilities: built-in tools, hooks (callbacks), subagents (`agents`), MCP, permissions, sessions (resume and fork), skills, commands and memory from `.claude/`, and plugins by local path.
- Third-party products may not offer claude.ai login.
- Source: [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- Imports: TypeScript `import { query } from "@anthropic-ai/claude-agent-sdk"`; Python `from claude_agent_sdk import query, ClaudeAgentOptions`.
- `settingSources` / `setting_sources`: omitting it equals `["user","project","local"]`, so the SDK loads filesystem config like the CLI does. Pass `[]` to isolate.
- Source: [Use Claude Code features in the SDK](https://code.claude.com/docs/en/agent-sdk/claude-code-features)

**GitHub Actions** — [GitHub Actions](https://code.claude.com/docs/en/github-actions)
- Setup: `/install-github-app` (github.com only), or manual setup by installing the app, adding a secret, and copying `examples/claude.yml`.
- Action: `anthropics/claude-code-action@v1`.
- Modes, detected automatically:
  - Interactive: responds to `@claude` in comments.
  - Automation: when a `prompt` input is given, on any event including cron.
- Inputs: `prompt`, `claude_args`, `anthropic_api_key`, `claude_code_oauth_token`, `github_token`, `plugin_marketplaces`, `plugins`, `settings`, `trigger_phrase`, `use_bedrock`, `use_vertex`, `use_foundry`.
- Upgrading from `@beta`: drop `mode`, rename `direct_prompt` to `prompt`, move `max_turns` and `model` into `claude_args`, and turn `custom_instructions` into `--append-system-prompt`.

**Scheduling** — [Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks)
- `/loop [interval] [prompt]` is a bundled skill:
  - A fixed interval (s/m/h/d) is converted to cron.
  - With no interval, Claude self-paces between 1 minute and 1 hour.
  - With no prompt, a built-in maintenance prompt runs, or `.claude/loop.md` / `~/.claude/loop.md` if present.
- Tools: `CronCreate` (5-field cron), `CronList`, `CronDelete`.
- Tasks are session-scoped and restored on `--resume`. Recurring tasks expire after 7 days, and a jitter applies.
- Scheduled fires only run model-invocable skills.
- `/loop` was added in v2.1.71 ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- Comparison of options:

| | Cloud routines | Desktop tasks | `/loop` |
| :- | :- | :- | :- |
| Minimum interval | 1 hour | 1 minute | 1 minute |
| Needs machine on | No | Yes | Yes |
| Needs open session | No | No | Yes |

**Routines** — [Routines](https://code.claude.com/docs/en/routines)
- Research preview.
- A saved prompt + repos + connectors, run on Anthropic cloud (or a self-hosted environment).
- Triggers:
  - Schedule: hourly / daily / weekdays / weekly, custom cron via `/schedule update` (minimum 1 hour), or a one-off run.
  - API: HTTP POST with a per-routine bearer token.
  - GitHub: e.g. `pull_request.opened`; requires the Claude GitHub App.
- Create and manage at claude.ai/code/routines or via `/schedule` (alias `/routines`).
- Runs are autonomous, with no permission picker. They use skills committed to the repo, not `~/.claude/skills`.
- Limits: 100 scheduled runs per hour per account; 30 per hour per routine for Run now / API.
- Plans: Pro, Max, Team, Enterprise.

**Worktrees** — [Worktrees](https://code.claude.com/docs/en/worktrees)
- `claude --worktree <name>` (`-w`) creates `.claude/worktrees/<name>/` on branch `worktree-<name>`.
- `.worktreeinclude` copies gitignored files such as `.env` into the worktree.
- `EnterWorktree` / `ExitWorktree` tools let Claude switch worktrees in-session.
- Subagents can use `isolation: worktree`.
- `WorktreeCreate` / `WorktreeRemove` hooks support non-git version control.
- On exit, Claude checks for unsaved work before removing the worktree.

**Plan mode** — [Permission modes](https://code.claude.com/docs/en/permission-modes)
- Claude "reads files, runs shell commands to explore, and writes a plan, but does not edit your source". Edits stay blocked until the plan is approved.
- Enter with Shift+Tab, `/plan [task]`, or `--permission-mode plan`.
- Shell commands during planning are reviewed by the auto-mode classifier when `useAutoModeDuringPlan` is on (the default).
- The built-in Plan subagent does the research.

**Checkpoints** — [Checkpointing](https://code.claude.com/docs/en/checkpointing)
- A checkpoint is taken before each user prompt that starts a turn. The last 100 checkpoints are kept, and they persist across resume.
- `/rewind` (or Esc twice) offers: restore code and conversation, restore conversation only, restore code only, summarize from here, or summarize up to here.
- Not tracked:
  - Bash-made changes.
  - Background subagent edits.
  - External edits.
  - Symlinked or hard-linked files.
  - Mid-turn messages.
- "Not a replacement for version control."

**Dynamic workflows** — [Workflows](https://code.claude.com/docs/en/workflows)
- "A dynamic workflow is a JavaScript script that orchestrates many subagents at once. Claude writes the script… a runtime executes it in the background."
- Triggers:
  - The `ultracode` keyword in a typed prompt. It was renamed from `workflow` in v2.1.160 ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
  - A direct request in your own words.
  - `/effort ultracode` for a whole session.
- Bundled workflow: `/deep-research`.
- Saving: `/workflows` → `s` saves to `.claude/workflows/` or `~/.claude/workflows/`, runnable as `/<name>`. Plugins ship workflows in `workflows/`.
- Script API:
  - `export const meta = {name, description}` must be the first statement.
  - `agent(prompt, {schema, label})`, `pipeline(items, fn)`, `parallel()`, `phase()`, `log()`, and an `args` global.
  - No `import()`, no direct filesystem or shell access.
  - `Date.now()` and `Math.random()` throw, for deterministic resume.
- Limits: 16 concurrent agents by default (configurable 1–256), 4,096 items per `parallel` / `pipeline`, and 1,000 agents per run. Runs are resumable within the session.
- Disable with `disableWorkflows` or `CLAUDE_CODE_DISABLE_WORKFLOWS=1`.
- Introduced in v2.1.154 ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).

**Plugins (packaging layer)** — [Plugin components](https://code.claude.com/docs/en/plugins/components); [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- Layout: `.claude-plugin/plugin.json`; directories `skills/`, `commands/` (legacy), and `agents/`; `hooks/hooks.json`; `.mcp.json`; LSP servers; executables; default settings; output styles; channels; `monitors/monitors.json`; `workflows/`.
- A `CLAUDE.md` at the plugin root is not loaded.
- The plugin system was released in v2.0.12.

**Other automation-adjacent features**
- Channels (research preview): MCP servers that push events into a running session. — [Channels](https://code.claude.com/docs/en/channels)
- `/goal`: keeps Claude working across turns until a condition is met. — [Commands](https://code.claude.com/docs/en/commands)
- `/batch`: 5–30 worktree-isolated background subagents. — [Commands](https://code.claude.com/docs/en/commands)

**Minimal examples**
```bash
# Headless, structured output
claude --bare -p "List exported functions in src/" --allowedTools "Read,Grep" \
  --output-format json --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```
— [Headless](https://code.claude.com/docs/en/headless)
```javascript
// .claude/workflows/audit-routes.js
export const meta = { name: 'audit-routes', description: 'Audit every route handler for missing auth checks' }
const found = await agent('List every .ts file under src/routes/.', { schema: { type: 'object', required: ['files'], properties: { files: { type: 'array', items: { type: 'string' } } } } })
const audits = await pipeline(found.files, file => agent(`Audit ${file} for missing authentication checks.`, { label: file }))
return audits.filter(Boolean)
```
— [Workflows](https://code.claude.com/docs/en/workflows)

### Inferences
- The orchestration options form a spectrum of "who holds the plan":
  - Skills and subagents: Claude, turn by turn.
  - Agent teams: a lead agent.
  - Workflows: a script.
  - Routines and loops: a scheduler.
- For CI the safest baseline is `--bare` + explicit `--allowedTools` / `--settings`, because default `-p` loads repo hooks and MCP servers without trust prompts.

### Gaps
- Not read in detail: Desktop scheduled tasks, the GitLab CI/CD page, Code Review (managed PR review), ultrareview, the Agent SDK sessions and permissions pages, and the mods pages.
- The exact PyPI and npm install commands for the Agent SDK were not captured, only the import names.
- Projects (claude.ai/code threads) and cross-session messaging were seen only in the overview table.
