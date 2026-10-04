# Skills

A skill is a named, self-contained package of instructions (a directory with a `SKILL.md` file and optional supporting files) that the agent loads only when it is needed. Until then, only the skill's name and a short description sit in context, so a harness can offer many procedures at a small, fixed context cost. Skills replace pasting the same procedure into chat and keep procedural content out of always-loaded instruction files. All three harnesses follow the Agent Skills open standard (agentskills.io) at the core and add their own extensions around it.

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Unit | Directory with `SKILL.md` plus supporting files ([skills][cc-skills]) | Directory with `SKILL.md`, optional `agents/openai.yaml`, `scripts/`, `references/`, `assets/` ([skills][cx-skills]) | Directory with `SKILL.md` (filename must be all caps) ([skills][oc-skills]) |
| Project scope | `.claude/skills/<name>/` in the start directory and every parent up to the repo root; nested `<subdir>/.claude/skills/` loads once Claude reads a file there ([skills][cc-skills]) | `.agents/skills/` in every directory from the cwd up to the repo root; the source also lists `<project>/.codex/skills` ([skills][cx-skills]) | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/`, walking up from the cwd to the git worktree ([skills][oc-skills]) |
| User scope | `~/.claude/skills/<name>/` ([skills][cc-skills]) | `~/.agents/skills`; `$CODEX_HOME/skills` is marked deprecated in source but still read, and `$skill-installer` writes there ([skills][cx-skills]) | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` ([skills][oc-skills]) |
| Admin / managed scope | `.claude/skills/` in the managed settings directory ([skills][cc-skills]) | `/etc/codex/skills` ([skills][cx-skills]) | Not recorded ([skills][oc-skills]) |
| Bundled skills | `/code-review`, `/loop`, `/batch`, `/simplify` and others ([skills][cc-skills]) | System skills `skill-creator`, `skill-installer`, `review-agent`, `imagegen`, `openai-docs` in `~/.codex/skills/.system/` ([skills][cx-skills]) | `customize-opencode` ([skills][oc-skills]) |
| Plugin-provided | `<plugin>/skills/<name>/SKILL.md`, namespaced `/plugin:name` ([skills][cc-skills]) | `skills/<name>/SKILL.md` in a plugin ([skills][cx-skills]) | Not recorded; the V2 plugin API has `ctx.skill.transform` ([skills][oc-skills]) |
| Extra roots | `.claude/skills/` inside `--add-dir` directories ([skills][cc-skills]) | App-server `skills/list` with `perCwdExtraUserRoots` ([skills][cx-skills]) | `skills.paths` (folders) and `skills.urls` (remote `index.json`) ([skills][oc-skills]) |
| Required fields | None; `description` recommended, `name` defaults to the directory name ([skills][cc-skills]) | `description` (empty is an error); `name` required per docs, falls back to the directory name ([skills][cx-skills]) | `name` (spec regex, must match the directory, unique across locations) and `description` ([skills][oc-skills]) |
| Fields acted on | Spec fields plus Claude-only keys (`disable-model-invocation`, `allowed-tools`, `context`, `hooks`, `paths`, …) ([skills][cc-skills]) | `name`, `description`, `metadata.short-description`; everything else ignored. Policy, UI and dependencies live in `agents/openai.yaml` ([skills][cx-skills]) | `name`, `description`, `license`, `compatibility`, `metadata` ([skills][oc-skills]) |
| Unknown fields | Ignored silently; invalid YAML loads the skill with no fields ([skills][cc-skills]) | Ignored; values sanitized to one line; a repair pass tolerates unquoted colons ([skills][cx-skills]) | Ignored ([skills][oc-skills]) |
| Description limit | `description` + `when_to_use` truncated together at 1,536 chars in the listing ([skills][cc-skills]) | 1,024 chars ([skills][cx-skills]) | 1–1,024 chars ([skills][oc-skills]) |
| Catalog in context | Name and description per skill; budget 1% of the context window; on overflow, descriptions of the least-invoked skills drop first, names stay ([skills][cc-skills]) | Name, description and file path per skill; budget 2% of the context window or 8,000 chars, configurable up to 10,000 tokens; descriptions shortened first, then skills omitted with a warning ([skills][cx-skills]) | Name and description per visible skill in the `skill` tool's description; no budget recorded ([skills][oc-skills]) |
| Body loading | On invocation, as one message that stays in context; re-attached after compaction (5,000 tokens each, 25,000 combined) ([skills][cc-skills]) | Full `SKILL.md` read when the skill is selected ([skills][cx-skills]) | Model calls `skill({ name })` ([skills][oc-skills]) |
| Explicit (user) invocation | `/name` at the start of a message ([skills][cc-skills]) | `$name` mention or the `/skills` picker ([skills][cx-skills]) | `/name`, because every skill is also registered as a slash command ([skills][oc-skills]) |
| Implicit (model) invocation | Skill tool, matched on the description ([skills][cc-skills]) | Codex chooses a skill when the task matches its description ([skills][cx-skills]) | `skill` tool ([skills][oc-skills]) |
| Turn off model invocation | `disable-model-invocation: true`; also removes the description from context ([skills][cc-skills]) | `agents/openai.yaml` → `policy.allow_implicit_invocation: false`; not injected into context by default, `$name` still works ([skills][cx-skills]) | No model-only switch recorded; `permission.skill: deny` hides the skill completely ([skills][oc-skills]) |
| Disable without deleting | `skillOverrides` per skill: `on` / `name-only` / `user-invocable-only` / `off` ([skills][cc-skills]) | `[[skills.config]]` with `path` and `enabled = false`; restart required ([skills][cx-skills]) | `permission.skill` pattern: `allow` / `ask` / `deny`, per agent ([skills][oc-skills]) |
| Arguments | `$ARGUMENTS`, `$N`, named `$name`; unconsumed arguments appended ([skills][cc-skills]) | None; text after `$name` is part of the user message ([skills][cx-skills]) | Not recorded for skills ([skills][oc-skills]) |
| Name collisions | Enterprise > personal > project; skill beats a same-named command file ([skills][cc-skills]) | Not merged; both can appear in selectors; no documented precedence ([skills][cx-skills]) | Names must be unique across all locations; a same-named command wins the slash name ([skills][oc-skills]) |
| Symlinked skill folders | Allowed ([skills][cc-skills]) | Followed for user, repo and admin scopes, not system ([skills][cx-skills]) | Not recorded ([skills][oc-skills]) |
| Change detection | Live for existing roots; a new top-level root needs `/reload-skills` ([skills][cc-skills]) | Automatic; restart if a change does not appear ([skills][cx-skills]) | Not recorded; cached remote skills can be refreshed ([skills][oc-skills]) |

## Generalized model

### Entities

- **Skill package.** A directory whose name is the skill name. It contains `SKILL.md` and, optionally, `scripts/` (executed, not loaded into context), `references/` (read on demand), and `assets/` (templates). `SKILL.md` holds YAML frontmatter and a Markdown body with the instructions.
- **Frontmatter.** Two portable fields carry the model: `name` (identifier, also the user-facing invocation name) and `description` (what the skill does and when to use it). `license`, `compatibility` and `metadata` (string-to-string map) are optional, informational fields from the standard.
- **Harness extension metadata.** Each harness keeps its own extra settings for a skill. One places them as extra frontmatter keys; the other places them in a sidecar file inside the skill directory. Both ignore what they do not understand.
- **Skill root.** A directory the harness scans for `<name>/SKILL.md`. Every root has a scope.
- **Catalog.** The per-session list of skills that the model sees: name, description, and in one harness the file path.

### Scopes

| Scope | Meaning | Discovery |
| --- | --- | --- |
| Project | Committed with the repository | Every directory from the cwd up to the repository root is scanned |
| User | Personal, all projects on one machine | Fixed directory under the home directory |
| Admin / managed | Organization-wide | Fixed system or managed-settings directory |
| Bundled | Ships with the harness | Built in |
| Plugin | Ships inside an installed plugin | Plugin's `skills/` directory |

Precedence between scopes on a name collision is not portable: one lead defines an order, the other shows both entries.

### Lifecycle

1. **Discover.** At session start, the harness scans all roots.
2. **List.** It renders the catalog into context under a budget proportional to the context window. On overflow it shortens descriptions first, then drops entries. Trigger words at the start of a description survive truncation longest.
3. **Activate.** Either the user names the skill explicitly, or the model matches the task against descriptions and activates it.
4. **Load.** The full body enters context. Resources load only when the body tells the model to read or run them.
5. **Persist.** The body stays in context for the rest of the session in the harness that documents this (Claude Code). Codex and OpenCode pages do not record what happens after loading.
6. **Reload.** Edits to existing skills are picked up during the session; new roots or config changes may need a reload or restart.

### Invocation policy

Each skill carries two invocation flags and one enablement flag:

| Flag | Default | Effect when off |
| --- | --- | --- |
| Model-invocable | on | The model cannot activate the skill on its own, and the description leaves the catalog. Explicit user invocation still works |
| User-invocable | on | Hidden from the user's menu; only the model can activate it (one lead only, see Dropped) |
| Enabled | on | The skill is neither listed nor invocable |

### Mapping

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Skill package | Skill directory | Skill folder | Skill folder |
| Project root | `.claude/skills/` | `.agents/skills/` | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` |
| User root | `~/.claude/skills/` | `~/.agents/skills/` | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` |
| Admin root | Managed settings `.claude/skills/` | `/etc/codex/skills` | — |
| Bundled skill | Bundled skill | System skill | Built-in skill |
| Harness extension metadata | Extra frontmatter keys | `agents/openai.yaml` | — |
| Catalog | Skill listing | Skill catalog / "available skills" list | `<available_skills>` in the `skill` tool description |
| Catalog budget | 1% of context window (`skillListingBudgetFraction`) | 2% of context window (`skills.max_context_tokens`) | — |
| Explicit invocation | `/name` | `$name`, `/skills` | `/name` |
| Implicit invocation | Skill tool | Description match | `skill` tool |
| Model-invocable = off | `disable-model-invocation: true` | `policy.allow_implicit_invocation: false` | — |
| Enabled = off | `skillOverrides: off` | `[[skills.config]] enabled = false` | `permission.skill: deny` |

## Portability

### Directory layout

The two leads share no skill directory. Claude Code never reads anything under `.agents/` ([instructions][cc-instructions]). Codex's documented and source-listed roots do not include `.claude/skills` ([skills][cx-skills]). OpenCode reads both `.claude/skills` and `.agents/skills` ([skills][oc-skills]).

Author once with one canonical copy and symlinks:

1. Put the skill in `.agents/skills/<name>/` (Codex's project root).
2. Symlink `.claude/skills/<name>` to it. Claude Code allows symlinked skill folders; Codex follows symlinked folders in repo, user and admin scopes.
3. Repeat at user scope with `~/.agents/skills/<name>/` and `~/.claude/skills/<name>`.

The reverse direction (canonical in `.claude/skills/`, symlink in `.agents/skills/`) relies on the same two facts.

Traps:

- **OpenCode sees two copies.** With both directories populated, OpenCode discovers the skill twice, and it requires names to be unique across all locations ([skills][oc-skills]). Whether it deduplicates a symlinked duplicate is not recorded. `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1` stops OpenCode from reading Claude Code skills ([skills][oc-skills]).
- **Cloud runs ignore user scope.** Claude Code cloud sessions and routines do not read `~/.claude/skills/`; they load skills committed to the repository plus account-synced skills ([skills][cc-skills]). Commit skills that automation needs.
- **Installer location.** Codex's `$skill-installer` writes to `$CODEX_HOME/skills`, which the source marks as deprecated, so a skill installed that way is not visible to Claude Code ([skills][cx-skills]).
- **Plugins.** Both leads load `skills/<name>/SKILL.md` from plugins. Plugin packaging is covered in the vendor plugin pages ([Claude Code plugins][cc-plugins], [Codex plugins][cx-plugins]).

### Frontmatter

| Field | Status | Rule for portable skills |
| --- | --- | --- |
| `name` | Safe | Use spec-valid names: 1–64 chars, lowercase `a-z`, `0-9`, single hyphens, equal to the directory name. OpenCode enforces this; Claude Code and Codex accept it ([skills][oc-skills], [skills][cc-skills], [skills][cx-skills]) |
| `description` | Safe | Non-empty (Codex errors on empty), at most 1,024 chars (Codex, OpenCode and the spec), key use case and trigger words first (both leads truncate). Codex collapses values to one line ([skills][cx-skills]) |
| `license`, `compatibility` | Safe, informational | Accepted by all three; acted on by none ([skills][cc-skills], [skills][cx-skills]) |
| `metadata` | Safe | String-to-string map. Codex reads only `metadata.short-description` ([skills][cx-skills]) |
| `allowed-tools` | Claude Code only | Ignored by Codex and OpenCode. In Claude Code it grants, not restricts ([skills][cc-skills]) |
| All other Claude Code keys | Claude Code only | Ignored by Codex and OpenCode. They cause a hard error when uploaded to claude.ai, the Skills API or `package_skill.py` ([skills][cc-skills]) |
| `agents/openai.yaml` | Codex only | A separate file; it does not touch `SKILL.md` frontmatter |

### Invocation policy in both leads

To make a skill user-invoked only, set it in both places in the same folder:

- `disable-model-invocation: true` in `SKILL.md` frontmatter (Claude Code).
- `policy.allow_implicit_invocation: false` in `agents/openai.yaml` (Codex).

Trap: in Claude Code this flag also blocks the skill from scheduled tasks and from subagent preloading ([skills][cc-skills], [automation][cc-automation]). In Codex the skill still runs when a scheduled task prompt names it with `$name` ([automation][cx-automation]). A skill meant to run from a schedule in Claude Code must stay model-invocable.

### Body

- **No argument placeholders.** Codex does not substitute `$ARGUMENTS` or `$1`; the user's text after `$name` is part of the message ([skills][cx-skills]). Write the body to read its inputs from the conversation.
- **No shell injection.** `` !`cmd` `` runs before the model sees the skill only in Claude Code ([skills][cc-skills]). Gap: OpenCode registers a skill as a command whose template is the skill body, and command templates run `` !`cmd` `` ([commands][oc-commands]); whether that applies to skill-backed commands is not recorded.
- **Resource paths.** Codex lists each skill's file path in the catalog ([skills][cx-skills]); OpenCode appends "Base directory for this skill: <dir>" to skill-backed commands ([skills][oc-skills]); Claude Code offers `${CLAUDE_SKILL_DIR}` ([skills][cc-skills]). `${CLAUDE_SKILL_DIR}` is literal text in the other harnesses. Gap: the pages do not say whether Claude Code tells the model the skill directory without that placeholder.
- **Size.** Keep `SKILL.md` under 500 lines and move detail into `references/`; the spec and Claude Code docs agree ([skills][cc-skills]).
- **Script approval.** Claude Code can pre-approve bundled scripts through `allowed-tools`; Codex gates skill scripts through `approval_policy.granular.skill_approval` ([skills][cx-skills]). There is no shared way to pre-approve a script.

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| `user-invocable: false` (model-only skill) | Claude Code | Codex has no switch that hides a skill from the user but keeps it for the model. |
| `when_to_use` | Claude Code | Codex reads only `description`; fold trigger phrases into `description`. |
| `argument-hint`, `arguments`, `$ARGUMENTS`/`$N` substitution | Claude Code | Codex skills have no argument substitution. |
| `allowed-tools`, `disallowed-tools` | Claude Code | Codex ignores both; no per-skill tool scope exists there. |
| `model`, `effort` per skill | Claude Code | No per-skill model or effort override in Codex. |
| `context: fork`, `agent`, `background` (run skill as subagent) | Claude Code | Codex skills cannot run themselves in a subagent; they can only instruct delegation. |
| `hooks` in skill frontmatter | Claude Code | Codex has no skill-scoped hooks. |
| `paths` (file-glob activation) | Claude Code | No counterpart in Codex. |
| `shell`, `` !`cmd` `` dynamic context injection, `@path` attachments | Claude Code | Codex does not preprocess the skill body. |
| `${CLAUDE_SKILL_DIR}`, `${CLAUDE_SESSION_ID}` and other placeholders | Claude Code | No substitution in Codex. |
| Nested `<subdir>/.claude/skills/` loaded on file access | Claude Code | Codex scans only from the cwd upward. |
| `skillOverrides` modes `name-only`, `user-invocable-only` | Claude Code | Codex has only enabled/disabled. |
| Auto-run of local `verify`/`simplify` skills before commits | Claude Code | Harness behavior tied to two skill names; no Codex counterpart. |
| `/skill-doctor`, `disableSkillShellExecution`, account-synced skills | Claude Code | Tooling and account features with no Codex counterpart. |
| `agents/openai.yaml` `interface.*` (display name, icons, brand color, `default_prompt`) | Codex | UI metadata with no Claude Code counterpart. |
| `agents/openai.yaml` `dependencies.tools` (MCP dependencies) | Codex | Claude Code skills cannot declare MCP dependencies. |
| `metadata.short-description` | Codex | Read only by Codex; harmless elsewhere but has no general meaning. |
| `$skill-installer`, `$skill-creator`, Record & Replay | Codex | Bundled authoring and install tooling, not part of the skill model. |
| App-server `skill` input item, `skills/list`, `skills/config/write` | Codex | Client protocol with no Claude Code counterpart. |
| `approval_policy.granular.skill_approval` | Codex | Codex-only approval gate for skill scripts. |
| `skills.urls` (remote skills), `skills.paths` | OpenCode | No counterpart in either lead. |
| `permission.skill: ask` | OpenCode | Neither lead prompts before loading a skill. |

## Sources

- [Claude Code: skills](../vendors/claude-code/skills.md)
- [Claude Code: instructions](../vendors/claude-code/instructions.md)
- [Claude Code: automation](../vendors/claude-code/automation.md)
- [Claude Code: plugins](../vendors/claude-code/plugins.md)
- [Codex: skills](../vendors/codex/skills.md)
- [Codex: automation](../vendors/codex/automation.md)
- [Codex: plugins](../vendors/codex/plugins.md)
- [OpenCode: skills](../vendors/opencode/skills.md)
- [OpenCode: commands](../vendors/opencode/commands.md)
- [Research notes](../research-notes/agent-harness-configuration/)

[cc-skills]: ../vendors/claude-code/skills.md
[cc-instructions]: ../vendors/claude-code/instructions.md
[cc-automation]: ../vendors/claude-code/automation.md
[cc-plugins]: ../vendors/claude-code/plugins.md
[cx-skills]: ../vendors/codex/skills.md
[cx-automation]: ../vendors/codex/automation.md
[cx-plugins]: ../vendors/codex/plugins.md
[oc-skills]: ../vendors/opencode/skills.md
[oc-commands]: ../vendors/opencode/commands.md
