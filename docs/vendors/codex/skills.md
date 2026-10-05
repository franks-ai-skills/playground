# Skills

A skill is a folder with a `SKILL.md` file that "packages instructions, resources, and optional scripts so either product can follow a workflow reliably" ([Build skills](https://learn.chatgpt.com/docs/build-skills.md)). Skills are the main reusable-workflow mechanism in Codex and replace the deprecated custom prompts ([commands.md](commands.md)). They follow the open Agent Skills standard (agentskills.io) and load with progressive disclosure: only a short catalog entry is in context until a skill is used.

The docs' rule of thumb: "if you keep reusing the same prompt or correcting the same workflow, it should probably become a skill". Typical uses are log triage, release notes, PR review against a checklist, migration planning and incident summaries ([Best practices](https://learn.chatgpt.com/docs/codex-manual.md), section "Turn repeatable work into skills"). Skills are the authoring format; plugins are how you distribute them ([plugins.md](plugins.md)).

## Locations and scopes

Documented scopes ([Build skills](https://learn.chatgpt.com/docs/build-skills.md)):

| Scope | Path | Notes |
|---|---|---|
| REPO | `$CWD/.agents/skills` | Current working directory |
| REPO | `$CWD/../.agents/skills` | Every folder between the cwd and the repository root |
| REPO | `$REPO_ROOT/.agents/skills` | Repository root |
| USER | `$HOME/.agents/skills` | Personal skills |
| ADMIN | `/etc/codex/skills` | System-wide |
| SYSTEM | Bundled with Codex by OpenAI | For example skill-creator and plan skills |

Additional roots found in the source (`host_roots.rs`, `main` branch) ([host_roots.rs](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/host_roots.rs); [loader/host.rs](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/host.rs)):

| Config layer | Root | Scope |
|---|---|---|
| Project | `<project>/.codex/skills` | Repo |
| User | `$CODEX_HOME/skills` | User. Commented "Deprecated user skills location (`$CODEX_HOME/skills`), kept for backward compatibility" |
| User | `~/.agents/skills` | User |
| User | System cache root | System |
| System | `<system config folder>/skills` | Admin |

- **Repository root** is found through `project_root_markers` (default `.git`) ([host_roots.rs](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/host_roots.rs)).
- **Symlinks.** Symlinked skill folders are followed ([Build skills](https://learn.chatgpt.com/docs/build-skills.md)). The source follows directory symlinks for User, Repo and Admin scopes and ignores them for System ([host_roots.rs](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/host_roots.rs)).
- **System skills on disk.** System skills are unpacked to `~/.codex/skills/.system/` with a `.codex-system-skills.marker` file. In 0.159.2 they are `imagegen`, `openai-docs`, `review-agent`, `skill-creator` and `skill-installer` (local listing).
- **Plugin skills.** Plugins bundle skills in `skills/<name>/SKILL.md` ([Build plugins](https://developers.openai.com/codex/plugins/build)). Skills bundled in plugins also work in ChatGPT Chat and Work on web, desktop and mobile; standalone skills work in the ChatGPT desktop app, Codex CLI and the IDE extension ([Build skills](https://learn.chatgpt.com/docs/build-skills.md)).
- **Name collisions.** "If two skills share the same `name`, Codex doesn't merge them; both can appear in skill selectors." ([Build skills](https://learn.chatgpt.com/docs/build-skills.md))
- **Admin controls.** ChatGPT workspace Skills, local filesystem skills and plugin skills each have separate lifecycle and access controls ([Skill controls](https://learn.chatgpt.com/docs/enterprise/skills.md)).

## Format

### Folder layout

```text
my-skill/
  SKILL.md              # required
  agents/openai.yaml    # optional, Codex/OpenAI-specific metadata
  scripts/              # deterministic computation
  references/           # policies, schemas, examples
  assets/               # templates
```

"Reference supporting files from SKILL.md and explain when to load or run them." ([Build skills (plugins)](https://developers.openai.com/plugins/build/skills.md))

### SKILL.md frontmatter that Codex reads

The Codex parser deserializes only three fields ([parser.rs](https://github.com/openai/codex/blob/main/codex-rs/skills/src/parser.rs); [loader/mod.rs](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs)):

| Field | Required | Rules in Codex |
|---|---|---|
| `name` | Yes per docs | At most 64 characters. Falls back to the directory name when missing or empty |
| `description` | Yes | An empty value is an error (`missing field description`). At most 1024 characters (`MAX_DESCRIPTION_LEN`) |
| `metadata.short-description` | No | Short description. The shipped system skills (`skill-creator`, `skill-installer`) use it (local `~/.codex/skills/.system/*/SKILL.md`) |

Values are sanitized to a single line. A "repair" pass tolerates unquoted colons in scalar values such as `description: Build for AWS: ECS`. Other keys such as `license`, `allowed-tools` and `compatibility` are ignored ([parser.rs](https://github.com/openai/codex/blob/main/codex-rs/skills/src/parser.rs)).

### Comparison with the Agent Skills specification

| Field | agentskills.io spec ([specification](https://agentskills.io/specification)) | Codex |
|---|---|---|
| `name` | Required; 1–64 characters; lowercase a–z, 0–9 and hyphens; no leading, trailing or double hyphens; must match the directory name | Read; only the length is checked |
| `description` | Required; 1–1024 characters | Read; must be non-empty; max 1024 |
| `license` | Optional | Ignored |
| `compatibility` | Optional; max 500 characters | Ignored |
| `metadata` | Optional string-to-string map | Only `metadata.short-description` is read |
| `allowed-tools` | Optional; space-separated; "Experimental" | Ignored |

The spec also defines optional `scripts/`, `references/` and `assets/` directories, recommends metadata of about 100 tokens, a body under 5000 tokens, `SKILL.md` under 500 lines and file references one level deep, and provides the validator `skills-ref validate ./my-skill` ([agentskills.io specification](https://agentskills.io/specification)).

### `agents/openai.yaml`

An optional, OpenAI-specific file. "`agents/openai.yaml` is an extended, product-specific config intended for the machine/harness to read, not the agent" (local `~/.codex/skills/.system/skill-creator/references/openai_yaml.md`).

| Field | Meaning | Default |
|---|---|---|
| `interface.display_name` | User-facing name | |
| `interface.short_description` | User-facing description; should be 25–64 characters | |
| `interface.icon_small` | Path to a small icon, for example `./assets/small-logo.svg` | |
| `interface.icon_large` | Path to a large icon | |
| `interface.brand_color` | Hex color, for example `#3B82F6` | |
| `interface.default_prompt` | Surrounding prompt used with the skill; must mention the skill as `$skill-name` | |
| `policy.allow_implicit_invocation` | `false`: Codex does not invoke the skill implicitly and does not inject it into the model context by default; explicit `$skill` still works | `true` |
| `dependencies.tools[].type` | Dependency type; only `mcp` is supported "for now" | |
| `dependencies.tools[].value` | Dependency identifier, for example an MCP server name | |
| `dependencies.tools[].description` | Description | |
| `dependencies.tools[].transport` | For example `streamable_http` | |
| `dependencies.tools[].url` | Server URL | |

Sources: [Build skills](https://learn.chatgpt.com/docs/build-skills.md); local `skill-creator/references/openai_yaml.md`.

### Enabling and disabling (`config.toml`)

| Key | Meaning | Default |
|---|---|---|
| `skills.config` | Array of per-skill entries | |
| `skills.config[].path` | Path to the skill's `SKILL.md` | |
| `skills.config[].enabled` | `false` disables the skill without deleting it | |
| `skills.max_context_tokens` | "Token budget for the available-skills catalog. Defaults to 2% of the model's context window. Explicit values are capped at `10000` tokens." | 2% of context window |

Sources: [Build skills](https://learn.chatgpt.com/docs/build-skills.md); [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md). Custom agent TOML files can carry their own `[[skills.config]]` to disable skills for that subagent ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)); see [subagents.md](subagents.md).

## Loading and invocation

### Discovery

- Codex scans `.agents/skills` in every directory from the cwd up to the repository root ([Build skills](https://learn.chatgpt.com/docs/build-skills.md)).
- Loader limits: `MAX_SCAN_DEPTH = 6`, `MAX_SKILLS_DIRS_PER_ROOT = 2000`, 20,000 entries per root (`discovery.rs`) ([loader/mod.rs](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs)).
- "Codex detects skill changes automatically. If an update doesn't appear, restart Codex." ([Build skills](https://learn.chatgpt.com/docs/build-skills.md)). After changing `skills.config`, restart Codex. The app-server emits `skills/changed` notifications when watched skill files change ([Codex App Server](https://learn.chatgpt.com/docs/app-server.md)).

### Context cost (catalog budget)

- "ChatGPT and Codex start with each skill's name and description, then load the full SKILL.md instructions when they decide to use that skill. In Codex, the initial list also includes each skill's file path. ... this list uses at most 2% of the model's context window, or 8,000 characters when the context window is unknown. If many skills are installed, Codex shortens skill descriptions first. For large skill sets, Codex may omit some skills from the initial list and show a warning." ([Build skills](https://learn.chatgpt.com/docs/build-skills.md))
- The budget covers only the catalog. The full `SKILL.md` is still read when a skill is selected.
- Source constants (`render.rs`): `DEFAULT_SKILL_METADATA_CHAR_BUDGET = 8_000`, `MAX_CONFIGURED_SKILL_METADATA_TOKEN_BUDGET = 10_000`, `SKILL_METADATA_CONTEXT_WINDOW_PERCENT = 2`, `MAX_CATALOG_SKILL_DESCRIPTION_CHARS = 1_024` ([render.rs](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/render.rs)).
- Catalog line format: `- {name}: {description} ({locator_kind}: {locator})`. The locator kind is `file`, `executor package`, `cloud package` or `custom resource`. Description space is shared out round-robin. Omitted skills produce "N additional skills omitted from this bounded skills list." and the warning prefix "Exceeded skills context budget. All skill descriptions were removed and..." ([render.rs](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/render.rs)).
- OpenTelemetry metrics `thread.skills.enabled_total`, `thread.skills.kept_total` and `thread.skills.truncated` show catalog truncation ([Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced.md)).

### Invocation

| Path | How |
|---|---|
| Explicit (CLI, IDE) | Run `/skills` or type `$` to mention a skill. With `/skills`, "Codex inserts the selected skill context so the next request follows that skill's instructions" ([Build skills](https://learn.chatgpt.com/docs/build-skills.md); [Slash commands](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)) |
| Implicit | "Codex can choose a skill when your task matches the skill `description`." Disabled by `policy.allow_implicit_invocation: false` ([Build skills](https://learn.chatgpt.com/docs/build-skills.md)) |
| App-server | Send `$skill-name` in the text and add an input item `{ "type": "skill", "name": ..., "path": ".../SKILL.md" }`, recommended "so the server injects full skill instructions instead of relying on the model to resolve the name". Related methods: `skills/list` (with `cwds`, `forceReload`, `perCwdExtraUserRoots`) and `skills/config/write` (enable or disable by path) ([Codex App Server](https://learn.chatgpt.com/docs/app-server.md)) |
| Scheduled tasks | A desktop-app scheduled task can trigger a skill with `$skill-name` in the task prompt ([Scheduled tasks](https://learn.chatgpt.com/docs/automations.md)); see [automation.md](automation.md) |

- Advice for descriptions: "Front-load the key use case and trigger words so a host can still match the skill if descriptions are shortened." ([Build skills](https://learn.chatgpt.com/docs/build-skills.md))
- Skills can tell Codex to delegate to subagents: "Current local Codex releases delegate when you ask directly or when applicable `AGENTS.md` or skill instructions request it." ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md))
- Skill scripts can require approval; `approval_policy.granular.skill_approval = false` rejects them automatically ([Config reference](https://developers.openai.com/codex/config-reference)); see [permissions-and-sandbox.md](permissions-and-sandbox.md).

### Creation and installation

- **`$skill-creator`** is the built-in creator. It asks what the skill does, when it should trigger, and whether to stay instruction-only (the default) or include scripts. Record & Replay drafts a skill from a demonstrated workflow ([Build skills](https://learn.chatgpt.com/docs/build-skills.md)).
- **`$skill-installer`**, for example `$skill-installer linear`, installs curated skills. By default it pulls from `https://github.com/openai/skills/tree/main/skills/.curated` (experimental skills are in `skills/.experimental`), or from another GitHub repository or path, including private ones. It installs into `$CODEX_HOME/skills` ([Build skills](https://learn.chatgpt.com/docs/build-skills.md); local `skill-installer/SKILL.md`).
- **Plugins.** For distribution beyond one repository, package skills in a plugin with a portable root `plugin.json`, a `skills/` directory, an `mcp.json` and optional `extensions.com.openai` metadata ([Package your plugin](https://developers.openai.com/plugins/build/plugins.md)); see [plugins.md](plugins.md).
- **`/import`** migrates Claude Code or Cursor setup, projects and chats into Codex configuration and local files ([Slash commands](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)).

### Feature flags

Local `codex features list` (0.159.2): `skill_mcp_dependency_install` (stable, on), `skill_search` (stable, on), `skip_host_skill_discovery` (under development, off), `skill_env_var_dependency_prompt` (removed).

## Example

```md
<!-- .agents/skills/release-notes/SKILL.md -->
---
name: release-notes
description: Explain exactly when this skill should and should not trigger.
---
Skill instructions for ChatGPT or Codex to follow.
```

```yaml
# .agents/skills/release-notes/agents/openai.yaml
interface:
  display_name: "Release notes"
  default_prompt: "Use $release-notes to draft notes for the last tag"
policy:
  allow_implicit_invocation: false
```

```toml
# ~/.codex/config.toml: disable a skill without deleting it
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

Sources: [Build skills](https://learn.chatgpt.com/docs/build-skills.md). The `openai.yaml` values are illustrative; the field names come from the documented schema.

## Limits and gotchas

- **Codex is less strict than the spec.** Inference: it does not enforce the spec's lowercase/hyphen name rule or the name-must-match-directory rule (it only checks length), and it accepts slightly malformed YAML ([parser.rs](https://github.com/openai/codex/blob/main/codex-rs/skills/src/parser.rs)).
- **Unread spec fields have no effect.** Inference: `allowed-tools`, `license` and `compatibility` are kept but do nothing. Codex-specific behavior (invocation policy, UI, dependencies) goes in `agents/openai.yaml`. Claude-specific frontmatter such as `disable-model-invocation` has to be rewritten as `policy.allow_implicit_invocation: false`.
- **Claude-Code-style keys in the binary are not supported.** Inference: the installed binary contains a SKILL.md-authoring prompt that mentions `argument-hint`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `context: fork` and `$ARGUMENTS`. The parser does not read those keys (local `strings` vs [parser.rs](https://github.com/openai/codex/blob/main/codex-rs/skills/src/parser.rs)).
- **Gap: argument substitution.** No `$1` or `KEY=value` substitution is documented for skills (see [commands.md](commands.md)).
- **Contradiction: dependency types.** The skill-creator reference says only `type: mcp` is supported. The app-server `skills/list` response example shows a dependency of `type: "env_var"` (`GITHUB_TOKEN`) ([Codex App Server](https://learn.chatgpt.com/docs/app-server.md); local `openai_yaml.md`).
- **Deprecated location still used by the installer.** `skill-installer` writes to `$CODEX_HOME/skills`, which the `main`-branch source marks as a deprecated user location ([host_roots.rs](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/host_roots.rs)). **Gap:** whether 0.159.2 already marks it deprecated could not be confirmed; the GitHub API rate limit stopped further source checks.
- **Catalog truncation.** With many skills, descriptions are shortened first and skills can be omitted from the catalog. Put trigger words at the start of the description.
- **Gap:** the meaning of the `skill_search` flag is not documented on the pages read.
- **Gap:** no official statement on precedence or order between scopes, beyond "both can appear in skill selectors" for name collisions.

## Sources

- https://learn.chatgpt.com/docs/build-skills.md
- https://learn.chatgpt.com/docs/codex-manual.md
- https://learn.chatgpt.com/docs/developer-commands.md?surface=cli
- https://learn.chatgpt.com/docs/app-server.md
- https://learn.chatgpt.com/docs/automations.md
- https://learn.chatgpt.com/docs/agent-configuration/subagents.md
- https://learn.chatgpt.com/docs/config-file/config-reference.md
- https://learn.chatgpt.com/docs/config-file/config-advanced.md
- https://learn.chatgpt.com/docs/enterprise/skills.md
- https://developers.openai.com/plugins/build/skills.md
- https://developers.openai.com/plugins/build/plugins.md
- https://developers.openai.com/codex/plugins/build
- https://developers.openai.com/codex/config-reference
- https://agentskills.io/specification
- https://github.com/openai/codex/blob/main/codex-rs/skills/src/parser.rs
- https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs
- https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/host.rs
- https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/host_roots.rs
- https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/render.rs
