# OpenAI Codex: extension mechanisms (skills, prompts/slash commands, subagents, hooks, workflows)

Scope and provenance:
- Researched 2026-10-04. Locally installed: `codex-cli 0.159.2` (Homebrew cask). Latest stable on GitHub at that date: `rust-v0.160.0` (published 2026-10-01); 0.161/0.162 exist only as alphas. Source: [openai/codex releases](https://github.com/openai/codex/releases), [rust-v0.160.0 notes](https://github.com/openai/codex/releases/tag/rust-v0.160.0).
- **Docs moved:** `https://developers.openai.com/codex/codex-manual.md` now answers HTTP 308 → `https://learn.chatgpt.com/docs/codex-manual.md`. The Codex docs live under `learn.chatgpt.com/docs/...`, and the plugin-builder docs stay under `developers.openai.com/plugins/...`. The manual is one file of about 2.9 MB that combines every page, and each section starts with its own `Source:` URL. The citations below use those per-page URLs. Index: [learn.chatgpt.com/llms.txt](https://learn.chatgpt.com/llms.txt).
- Codex is now presented as part of "ChatGPT" (the desktop app is the "ChatGPT desktop app", and ChatGPT Work shares skills and plugins). The notes below cover only the local Codex harness (CLI, IDE extension, desktop app, cloud).
- "Local" findings come from read-only inspection of `~/.codex/skills/.system`, `codex --help`, `codex exec --help`, `codex features list`, and `strings` on the installed binary. Source-code findings come from the `main` branch of [openai/codex](https://github.com/openai/codex) and may run ahead of 0.159.2.

## Skills: SKILL.md format, locations, openai.yaml metadata, discovery/invocation, agentskills.io relation, installer

### Takeaway
Skills are the primary reusable-workflow mechanism in Codex. A skill is a folder with `SKILL.md`, which needs `name` and `description` frontmatter. Skills follow the open Agent Skills standard (agentskills.io) and are loaded with progressive disclosure: only name, description and path go into a catalog capped at about 2% of the context window, and the full body is read when the skill is used. A skill runs explicitly through `$skill-name` or `/skills`, or implicitly when the task matches its description. An optional `agents/openai.yaml` adds UI metadata, an invocation policy and MCP dependencies. Repo skills live in `.agents/skills` (scanned from cwd up to the repo root), user skills in `~/.agents/skills`, and `$CODEX_HOME/skills` is a deprecated location that still works. Admin skills live in `/etc/codex/skills`, and system skills ship with Codex.

### Cited Findings
**What it is and why**
- A skill "packages instructions, resources, and optional scripts so either product can follow a workflow reliably. Skills build on the open agent skills standard (agentskills.io)." Skills are the authoring format, and plugins are how you distribute them. — [Build skills](https://learn.chatgpt.com/docs/build-skills.md)
- Standalone skills work in the ChatGPT desktop app, Codex CLI and the IDE extension. Skills bundled in plugins also work in ChatGPT Chat and Work on web, desktop and mobile. — [Build skills](https://learn.chatgpt.com/docs/build-skills.md)
- Rule of thumb from the docs: "if you keep reusing the same prompt or correcting the same workflow, it should probably become a skill". Typical uses: log triage, release notes, PR review against a checklist, migration planning, incident summaries. — [Best practices](https://learn.chatgpt.com/docs/codex-manual.md) (section "Turn repeatable work into skills")

**File format / frontmatter**
- `SKILL.md` must include `name` and `description`. Minimal form:
  ```md
  ---
  name: skill-name
  description: Explain exactly when this skill should and should not trigger.
  ---
  Skill instructions for ChatGPT or Codex to follow.
  ```
  — [Build skills](https://learn.chatgpt.com/docs/build-skills.md)
- The Codex parser (`codex-rs/skills/src/parser.rs`) deserializes only `name`, `description` and `metadata.short-description`. It ignores other keys such as `license`, `allowed-tools` and `compatibility`. `name` is at most 64 characters and falls back to a default (the directory name) when missing or empty. An empty `description` is an error (`missing field description`). Values are sanitized to a single line. A "repair" pass tolerates unquoted colons in scalar values such as `description: Build for AWS: ECS`. — [parser.rs](https://github.com/openai/codex/blob/main/codex-rs/skills/src/parser.rs)
- Loader limits (`codex-rs/ext/skills/src/loader/mod.rs`): `MAX_NAME_LEN = 64`, `MAX_DESCRIPTION_LEN = 1024`, `MAX_SCAN_DEPTH = 6`, `MAX_SKILLS_DIRS_PER_ROOT = 2000`, 20,000 entries per root (`discovery.rs`), metadata directory `agents`, metadata filename `openai.yaml`. — [loader/mod.rs](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs)
- The system skills shipped with Codex use `metadata: short-description: "..."` in their frontmatter (for example `skill-creator` and `skill-installer`). — local `~/.codex/skills/.system/*/SKILL.md` (codex-cli 0.159.2)
- Agent Skills spec fields: `name` (required, 1–64 characters, lowercase a–z/0–9/hyphens, no leading, trailing or double hyphens, must match the directory name), `description` (required, 1–1024 characters), `license`, `compatibility` (≤500 characters), `metadata` (string→string map), `allowed-tools` (space-separated, "Experimental"). Optional directories: `scripts/`, `references/`, `assets/`. Progressive disclosure: metadata about 100 tokens, body under 5000 tokens recommended, `SKILL.md` under 500 lines, file references one level deep. Validator: `skills-ref validate ./my-skill`. — [agentskills.io specification](https://agentskills.io/specification)
- Codex docs on resources: `references/` holds policies, schemas and examples, `assets/` holds templates, `scripts/` holds deterministic computation. "Reference supporting files from SKILL.md and explain when to load or run them." — [Build skills (plugins)](https://developers.openai.com/plugins/build/skills.md)

**`agents/openai.yaml` (Codex/OpenAI-specific metadata)**
- Full schema:
  ```yaml
  interface:
    display_name: "Optional user-facing name"
    short_description: "Optional user-facing description"
    icon_small: "./assets/small-logo.svg"
    icon_large: "./assets/large-logo.png"
    brand_color: "#3B82F6"
    default_prompt: "Optional surrounding prompt to use the skill with"
  policy:
    allow_implicit_invocation: false
  dependencies:
    tools:
      - type: "mcp"
        value: "openaiDeveloperDocs"
        description: "OpenAI Docs MCP server"
        transport: "streamable_http"
        url: "https://developers.openai.com/mcp"
  ```
  `allow_implicit_invocation` defaults to `true`. When it is `false`, Codex will not invoke the skill implicitly, but explicit `$skill` still works. — [Build skills](https://learn.chatgpt.com/docs/build-skills.md)
- Bundled field reference: "`agents/openai.yaml` is an extended, product-specific config intended for the machine/harness to read, not the agent". `short_description` should be 25–64 characters. `default_prompt` must mention the skill as `$skill-name`. `dependencies.tools[].type` supports "only `mcp`... for now". With `allow_implicit_invocation: false` the skill "is not injected into the model context by default". — local `~/.codex/skills/.system/skill-creator/references/openai_yaml.md`
- The app-server `skills/list` response example also shows a dependency of `type: "env_var"` (`GITHUB_TOKEN`). The skill-creator reference says only `mcp` is supported, so the two sources disagree. — [Codex App Server](https://learn.chatgpt.com/docs/app-server.md)
- Example from a shipped system skill: `review-agent/agents/openai.yaml` sets `policy.allow_implicit_invocation: false`. — local `~/.codex/skills/.system/review-agent/agents/openai.yaml`

**Locations / scopes**
- Documented scopes: `REPO` `$CWD/.agents/skills`, `$CWD/../.agents/skills` (folders between cwd and repo root), `$REPO_ROOT/.agents/skills`; `USER` `$HOME/.agents/skills`; `ADMIN` `/etc/codex/skills`; `SYSTEM` "Bundled with Codex by OpenAI" (for example skill-creator and plan skills). "Codex scans `.agents/skills` in every directory from your current working directory up to the repository root. If two skills share the same `name`, Codex doesn't merge them; both can appear in skill selectors." Symlinked skill folders are followed. — [Build skills](https://learn.chatgpt.com/docs/build-skills.md)
- Source (`host_roots.rs`): the project config layer adds `<project>/.codex/skills` (Repo scope). The user layer adds `$CODEX_HOME/skills`, commented "Deprecated user skills location (`$CODEX_HOME/skills`), kept for backward compatibility", plus `~/.agents/skills` and the system cache root (System scope). The system config layer adds `<system config folder>/skills` (Admin). The repository root is found through `project_root_markers` (default `.git`). Directory symlinks are followed for User, Repo and Admin scopes and ignored for System. — [host_roots.rs](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/host_roots.rs), [loader/host.rs](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/host.rs)
- Local install: system skills are unpacked to `~/.codex/skills/.system/` with a `.codex-system-skills.marker` file. In 0.159.2 they are `imagegen`, `openai-docs`, `review-agent`, `skill-creator` and `skill-installer`. — local listing of `~/.codex/skills/.system`
- Disable a skill without deleting it:
  ```toml
  [[skills.config]]
  path = "/path/to/skill/SKILL.md"
  enabled = false
  ```
  Restart Codex after changing config. — [Build skills](https://learn.chatgpt.com/docs/build-skills.md). Config reference keys: `skills.config` (array), `skills.config[].path`, `skills.config[].enabled`, `skills.max_context_tokens` ("Token budget for the available-skills catalog. Defaults to 2% of the model's context window. Explicit values are capped at `10000` tokens."). — [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md)
- Custom agent TOML files can carry their own `[[skills.config]]` to disable skills for that subagent. — [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)

**Loading, context cost, progressive disclosure**
- "ChatGPT and Codex start with each skill's name and description, then load the full SKILL.md instructions when they decide to use that skill. In Codex, the initial list also includes each skill's file path. ... this list uses at most 2% of the model's context window, or 8,000 characters when the context window is unknown. If many skills are installed, Codex shortens skill descriptions first. For large skill sets, Codex may omit some skills from the initial list and show a warning." The budget covers only the catalog, and the full SKILL.md is still read on selection. — [Build skills](https://learn.chatgpt.com/docs/build-skills.md)
- Source constants (`render.rs`): `DEFAULT_SKILL_METADATA_CHAR_BUDGET = 8_000`, `MAX_CONFIGURED_SKILL_METADATA_TOKEN_BUDGET = 10_000`, `SKILL_METADATA_CONTEXT_WINDOW_PERCENT = 2`, `MAX_CATALOG_SKILL_DESCRIPTION_CHARS = 1_024`. Catalog line format is `- {name}: {description} ({locator_kind}: {locator})`, where the locator kind is `file`, `executor package`, `cloud package` or `custom resource`. Description space is shared out round-robin. Omitted skills produce "N additional skills omitted from this bounded skills list." and a warning prefix "Exceeded skills context budget. All skill descriptions were removed and...". — [render.rs](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/render.rs)
- Skill changes are picked up automatically: "Codex detects skill changes automatically. If an update doesn't appear, restart Codex." The app-server emits `skills/changed` notifications when watched skill files change. — [Build skills](https://learn.chatgpt.com/docs/build-skills.md); [Codex App Server](https://learn.chatgpt.com/docs/app-server.md)
- OpenTelemetry metrics `thread.skills.enabled_total`, `thread.skills.kept_total` and `thread.skills.truncated` show catalog truncation. — [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced.md)

**Invocation**
- "Explicit invocation: ... In Codex CLI or the IDE extension, run `/skills` or type `$` to mention a skill. Implicit invocation: ... Codex can choose a skill when your task matches the skill `description`." Advice: "Front-load the key use case and trigger words so a host can still match the skill if descriptions are shortened." — [Build skills](https://learn.chatgpt.com/docs/build-skills.md)
- `/skills` lets you pick a skill, and "Codex inserts the selected skill context so the next request follows that skill's instructions." — [Slash commands in Codex CLI](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)
- App-server: send `$skill-name` in the text and add an input item `{ "type": "skill", "name": ..., "path": ".../SKILL.md" }`, which is recommended "so the server injects full skill instructions instead of relying on the model to resolve the name". Related methods: `skills/list` (with `cwds`, `forceReload`, `perCwdExtraUserRoots`) and `skills/config/write` (enable or disable by path). — [Codex App Server](https://learn.chatgpt.com/docs/app-server.md)
- Scheduled tasks in the desktop app can trigger a skill explicitly with `$skill-name` in the task prompt. — [Scheduled tasks](https://learn.chatgpt.com/docs/automations.md)
- Skills (and `AGENTS.md`) can tell Codex to delegate to subagents: "Current local Codex releases delegate when you ask directly or when applicable `AGENTS.md` or skill instructions request it." — [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)

**Creation / installation / distribution**
- `$skill-creator` is the built-in creator. It asks what the skill does, when it should trigger, and whether to stay instruction-only (the default) or include scripts. Record & Replay drafts a skill from a demonstrated workflow. — [Build skills](https://learn.chatgpt.com/docs/build-skills.md)
- `$skill-installer linear` installs curated skills. By default it pulls from `https://github.com/openai/skills/tree/main/skills/.curated` (experimental ones are in `skills/.experimental`) or from another GitHub repo or path, including private ones, into `$CODEX_HOME/skills`. — [Build skills](https://learn.chatgpt.com/docs/build-skills.md); local `~/.codex/skills/.system/skill-installer/SKILL.md`
- The system skill-installer still writes to `$CODEX_HOME/skills`, which the source marks as a deprecated user location. — local skill-installer SKILL.md; [host_roots.rs](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/host_roots.rs)
- For distribution beyond one repo, package skills in a plugin. A plugin has a portable root `plugin.json`, a `skills/` dir, an `mcp.json`, and optional `extensions.com.openai` metadata, with `.codex-plugin/plugin.json` as a compatibility overlay. — [Package your plugin](https://developers.openai.com/plugins/build/plugins.md)
- Admin: ChatGPT workspace Skills, local filesystem skills and plugin skills each have separate lifecycle and access controls. Plugins "aren't available in the IDE extension." — [Skill controls](https://learn.chatgpt.com/docs/enterprise/skills.md)
- The `/import` slash command migrates Claude Code or Cursor setup, projects and chats into Codex configuration and local files. — [Slash commands in Codex CLI](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)

**Feature flags (local `codex features list`, 0.159.2)**
- Skill-related flags: `skill_mcp_dependency_install` (stable, on), `skill_search` (stable, on), `skip_host_skill_discovery` (under development, off), `skill_env_var_dependency_prompt` (removed). — local `codex features list`

### Inferences
- Codex reads only `name`, `description` and `metadata.short-description` from frontmatter. Other Agent Skills fields (`allowed-tools`, `license`, `compatibility`) are kept but have no effect. Codex-specific behavior such as invocation policy, UI and dependencies goes in `agents/openai.yaml`. So a skill written to the agentskills.io spec is portable to Codex, but Claude-specific frontmatter such as `disable-model-invocation` has to be rewritten as `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.
- The installed binary contains a SKILL.md-authoring prompt that mentions Claude-Code-style keys (`argument-hint`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `context: fork`, `$ARGUMENTS`). It looks like part of the memories/import extension, and the parser does not read those keys (local `strings` on the binary versus parser.rs). These keys should not be treated as Codex-supported.
- Codex is less strict than the spec. It does not enforce the spec's lowercase/hyphen name rule or the name-must-match-directory rule (it only checks length), and it accepts slightly malformed YAML.

### Gaps
- Whether 0.159.2 itself already marks `$CODEX_HOME/skills` as deprecated could not be confirmed. The comment was seen on `main`, and the GitHub API rate limit stopped further source checks.
- The meaning of the `skill_search` feature flag (stable, on) is not documented on the pages read.
- No official statement on the precedence or order between scopes beyond "both can appear in skill selectors" for name collisions.

## Custom prompts / slash commands: ~/.codex/prompts, arguments, built-in slash commands, deprecation in favor of skills

### Takeaway
Custom prompts (Markdown files in `~/.codex/prompts/` run as `/prompts:<name>`) are officially deprecated in favor of skills. The docs still describe their format, but the current CLI slash-command table does not list them, and the 0.159.2 binary has no `codex/prompts` string, so they may already be gone (unverified). Codex has no user-defined slash commands anymore. Skills invoked with `$name` or `/skills` take that role, and plugins add more. Built-in slash commands are a fixed list.

### Cited Findings
- "Custom prompts are deprecated. Use skills for reusable instructions that Codex can invoke explicitly or implicitly." The llms.txt index labels the page "Deprecated. Use skills for reusable prompts". — [Custom Prompts](https://learn.chatgpt.com/docs/custom-prompts.md); [llms.txt](https://learn.chatgpt.com/llms.txt)
- Documented (deprecated) format: top-level `.md` files in `~/.codex/prompts/` (subdirectories and non-Markdown files are ignored). They are local only and not shared through the repo, need explicit invocation, and need a restart or new chat to load. YAML front matter `description:` (shown in the popup) and `argument-hint:`. Placeholders: `$1`–`$9` (positional), `$ARGUMENTS` (all), uppercase named `$FILE`/`$TICKET_ID` filled via `KEY=value` (quote values with spaces), and `$$` for a literal `$`. Invoked as `/prompts:draftpr FILES="..." PR_TITLE="..."`. Example:
  ```markdown
  ---
  description: Prep a branch, commit, and open a draft PR
  argument-hint: [FILES=<paths>] [PR_TITLE="<title>"]
  ---
  Create a branch named `dev/<feature_name>` for this work.
  If files are specified, stage them first: $FILES.
  ```
  — [Custom Prompts](https://learn.chatgpt.com/docs/custom-prompts.md)
- Built-in CLI slash commands (current docs): `/permissions`, `/ide`, `/keymap`, `/vim`, `/setup-default-sandbox` and `/sandbox-add-read-dir` (Windows only), `/agent` (alias `/subagents`), `/apps`, `/plugins`, `/hooks`, `/clear`, `/rename`, `/archive`, `/delete`, `/compact`, `/copy`, `/diff`, `/exit`, `/quit`, `/experimental`, `/approve`, `/memories`, `/skills`, `/import`, `/feedback`, `/init`, `/logout`, `/mcp [verbose]`, `/mention`, `/model`, `/fast`, `/plan`, `/goal`, `/personality`, `/ps`, `/stop`, `/fork`, `/app`, `/side` (alias `/btw`), `/raw`, `/resume`, `/new`, `/review`, `/status`, `/usage`, `/debug-config`, `/statusline`, `/title`, `/theme`, `/pets` (alias `/pet`). While a turn runs, a slash command plus `Tab` queues it for the next turn. — [Slash commands in Codex CLI](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)
- Extension-relevant built-ins: `/skills` (pick a skill), `/apps` (inserts `$app-slug`), `/plugins` (plugin browser, Space toggles enabled), `/hooks` (inspect, trust or disable non-managed hooks), `/agent` (switch agent threads), `/review` (working-tree review that uses `review_model` if set), `/init` (generates an `AGENTS.md` scaffold), `/import` (Claude Code/Cursor migration, up to 50 chats from the last 30 days, unavailable in remote/daemon sessions). — [Slash commands in Codex CLI](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)
- The IDE extension has its own slash-command reference page. — [Codex IDE extension slash commands](https://learn.chatgpt.com/docs/developer-commands.md?surface=ide)
- The installed 0.159.2 binary has no `codex/prompts` or `CustomPrompt` strings other than `OpenReviewCustomPrompt`, which is the `/review` custom-instructions picker in `tui/src/bottom_pane/custom_prompt_view/picker.rs`. — local `strings /opt/homebrew/Caskroom/codex/0.159.2/bin/codex`

### Inferences
- `/prompts:` is missing from the built-in table, and the binary has no prompts-directory string. Together these suggest custom prompts are deprecated in the docs and possibly removed from the 0.159.2 TUI. Path strings could be built at runtime, so this is not proven. New work should use skills, with `policy.allow_implicit_invocation: false` to get prompt-like behavior that only runs explicitly. Skills have no `$1`/`KEY=value` argument substitution: the text after `$skill-name` is just part of the user message.

### Gaps
- The release in which custom prompts were removed (if they were) was not found, because GitHub search hit its rate limit. No official removal note was found.
- No documented way to define new built-in-style slash commands, other than plugins (plugin "commands" are mentioned in the bundled self-knowledge reference but were not verified in the docs).

## Subagents / multi-agent: built-in agents, custom agents, [agents] config, spawn tools, Codex as MCP server + Agents SDK, cloud parallel attempts

### Takeaway
Multi-agent ("subagents") is stable and on by default (`features.multi_agent`). The model gets the tools `spawn_agent`, `send_input`, `resume_agent`, `wait_agent` and `close_agent`. It spawns subagents only when the user asks, or when `AGENTS.md` or skill instructions tell it to. Codex ships three built-in agent types (`default`, `worker`, `explorer`). Custom agents are standalone TOML files in `~/.codex/agents/` or `.codex/agents/` that need `name`, `description` and `developer_instructions` and can override any config key. Global limits and defaults live under `[agents]`. The old "Codex as MCP server orchestrated by the Agents SDK" pattern no longer works, because `codex mcp-server` has been removed in favor of the app-server. Codex Cloud supports best-of-N with `--attempts 1-4`.

### Cited Findings
- "Current Codex releases enable subagent workflows by default. Subagent activity appears in the ChatGPT desktop app, Codex CLI, and the IDE extension." Subagents "consume more tokens than comparable single-agent runs." — [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)
- Trigger: "Current local Codex releases spawn agents after a direct request or applicable project or skill instruction" (for example "spawn two agents", "use one agent per point"). Codex handles orchestration, waits for all requested results, and returns one consolidated response. — [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)
- Purpose: keep noisy intermediate output (exploration, logs, tests) off the main thread to avoid "context pollution" and "context rot", and return summaries. Docs recommend parallel agents for read-heavy work and caution with parallel writes. — [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)
- Tools: `features.multi_agent` — "Enable multi-agent collaboration tools (`spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, and `close_agent`) (stable; on by default)." Admins can pin it in `requirements.toml`. — [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md)
- Local flags: `multi_agent` stable/true, `multi_agent_v2` stable/false, `multi_agent_mode` removed, `enable_fanout` removed, `agent_message_board` under development/false. — local `codex features list` (0.159.2)
- Built-in agents: `default` (general-purpose fallback), `worker` (implementation and fixes), `explorer` (read-heavy exploration). A custom agent whose name matches a built-in replaces it. — [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)
- Custom agent files go in `~/.codex/agents/` (personal) or `.codex/agents/` (project), one agent per TOML file. Required: `name` (the source of truth, the filename doesn't matter), `description` (when to use it), `developer_instructions`. Any other `config.toml` key is allowed (`model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config`, ...). Codex loads them "as configuration layers for spawned sessions", and "the format may evolve". — [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)
- Minimal custom agent (`.codex/agents/reviewer.toml`):
  ```toml
  name = "reviewer"
  description = "PR reviewer focused on correctness, security, and missing tests."
  model = "gpt-6.1-sol"
  model_reasoning_effort = "medium"
  sandbox_mode = "read-only"
  developer_instructions = """
  Review code like an owner. Prioritize correctness, security, behavior regressions, and missing test coverage.
  """
  ```
  — [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)
- Model and effort resolution: explicit spawn value, then the `[agents]` default, then the parent's value. A `model` or `model_reasoning_effort` set in the custom agent file wins. If a model is chosen without an effort, that model's default effort applies. Unspecified settings (`sandbox_mode`, `mcp_servers`, `skills.config`) are inherited from the parent. — [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)
- `[agents]` keys: `agents.enabled` (default true), `agents.max_concurrent_threads_per_session` (cap excluding the primary thread, with `agents.max_threads` as a legacy alias), `agents.default_subagent_model`, `agents.default_subagent_reasoning_effort`, `agents.interrupt_message` (default true). The config reference also lists role declarations `agents.<name>.config_file` (a TOML layer path, relative to the declaring config) and `agents.<name>.description`. "Scalar setting names are reserved and can't be used as custom role names." — [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md); [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md)
- Sandbox and approvals: subagents inherit the parent sandbox policy and live runtime overrides (`/permissions`, `--yolo`), "even if the selected custom agent file sets different defaults". In the CLI, approval requests from inactive threads show the source thread label, and `o` opens that thread. In non-interactive flows, an action that needs new approval fails and the error goes back to the parent. — [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)
- UI: `/agent` or `/subagents` switches threads in the CLI. The IDE has a background-agent panel above the composer. `codex agents` ("Browse all agent sessions on the shared local app-server daemon") is the "agent command center" (0.160.0 added history pagination to it). — [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md); local `codex agents --help`; [rust-v0.160.0](https://github.com/openai/codex/releases/tag/rust-v0.160.0)
- Hooks see subagents through `SubagentStart` and `SubagentStop`, and `spawn_agent` also matches `Agent` in `PreToolUse`/`PostToolUse` matchers (see Hooks below). — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- The shipped `review-agent` system skill is meant for delegated reviews: "Use when another agent delegates review of uncommitted changes, a base-branch diff, a commit...". It is read-only and must not delegate further. — local `~/.codex/skills/.system/review-agent/SKILL.md`
- **Removed:** "The `codex mcp-server` command and standalone `codex-mcp-server` binary have been removed. Use the Codex app server for existing integrations." — [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk.md); [CLI command reference](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli). `mcp-server` is also missing from the 0.159.2 `codex --help` command list. — local `codex --help`
- Cloud best-of-N: `codex cloud exec --attempts 1-4` (default 1) is "Number of assistant attempts (best-of-N) Codex cloud should run". It requires `--env ENV_ID`. `codex cloud list --json` returns `attempt_total` per task. `codex cloud` is marked experimental (alias `codex cloud-tasks`), with subcommands `exec`, `status`, `list`, `apply` and `diff`. — [CLI command reference](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli); local `codex cloud --help`
- Worktrees as a parallelism tool: the desktop app runs parallel chats in Git worktrees (detached HEAD by default), with "Handoff" moving a chat between Local and Worktree. The CLI has `--worktree` ("Run the session in a new managed Git worktree"), and the `worktrees` feature is stable and on. — [Worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees.md); local `codex --help`, `codex features list`

### Inferences
- The multi-agent model is "agent types as config layers": a custom agent is a partial `config.toml` plus `name`, `description` and `developer_instructions`. There is no separate tool allowlist field. Tool scope is controlled through `sandbox_mode`, `mcp_servers` and `skills.config`.
- To orchestrate Codex from an external framework (the old Agents SDK + MCP pattern), use the Codex SDK (TS/Python) or the app-server JSON-RPC protocol. Older OpenAI guides showing `codex mcp-server` with the Agents SDK are obsolete.

### Gaps
- The default value of `max_concurrent_threads_per_session` ("Codex chooses the default") and any nesting-depth limit are not documented.
- What `multi_agent_v2` (stable but off) changes is not documented on the pages read.
- The exact JSON schemas of the `spawn_agent`/`send_input`/`wait_agent` tool arguments are not documented publicly.

## Hooks and notifications: hooks.json / [hooks], events, I/O semantics, trust, maturity; notify and TUI notifications

### Takeaway
Codex has a full lifecycle-hooks system. `features.hooks` is stable and on by default (`codex_hooks` is a deprecated alias). Its schema is deliberately close to Claude Code's: events with matcher groups and handlers, JSON on stdin, exit code 2 or JSON decisions on stdout, `hookSpecificOutput`, and `CLAUDE_PLUGIN_ROOT` set for compatibility. There are 12 events. Handlers can be `command` or `mcp_tool`, while `prompt` and `agent` handlers are parsed but skipped. Non-managed hooks need hash-based trust review through `/hooks`. Separately, `notify` runs an external program on `agent-turn-complete`, and `tui.notifications` emits OSC 9 or BEL terminal notifications.

### Cited Findings
**Sources and locations**
- Hooks are discovered "next to active config layers" as `hooks.json` or inline `[hooks]` in `config.toml`. The common locations are `~/.codex/hooks.json`, `~/.codex/config.toml`, `<repo>/.codex/hooks.json` and `<repo>/.codex/config.toml`. All sources load, and higher-precedence layers don't replace lower ones. Having both forms in one layer merges them with a warning. Project-local hooks load only when the project `.codex/` layer is trusted. Plugins can bundle hooks in `hooks/hooks.json` or through the manifest `hooks` entry. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- Execution: "Matching hooks from multiple files all run. Multiple matching command hooks for the same event are launched concurrently." Commands run with the session `cwd`, so docs recommend git-root-based paths (`$(git rev-parse --show-toplevel)/.codex/hooks/...`). — [Hooks](https://learn.chatgpt.com/docs/hooks.md)

**Trust and maturity**
- "Before a non-managed hook can run, Codex requires you to review and trust the exact hook definition. Codex records trust against the hook's current hash, so new or changed hooks are marked for review and skipped until trusted." Use `/hooks` to trust or disable hooks. Managed hooks (system, MDM, cloud, `requirements.toml`) are trusted by policy and can't be disabled by the user. `--dangerously-bypass-hook-trust` skips the trust check for one invocation (in both `codex` and `codex exec`). Plugin hooks are not trusted automatically when the plugin is installed. — [Hooks](https://learn.chatgpt.com/docs/hooks.md); local `codex exec --help`
- `features.hooks` — "Enable lifecycle hooks loaded from `hooks.json` or inline `[hooks]` config. `features.codex_hooks` is a deprecated alias." Hooks are on by default. Disable them with `[features] hooks = false`. — [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md); [Hooks](https://learn.chatgpt.com/docs/hooks.md). Local: `hooks` stable/true, `plugin_hooks` removed. — local `codex features list`

**Config shape and handler fields**
- Three levels: event → matcher group (`matcher` regex; `"*"`, `""` or omitted matches everything) → `hooks[]` handlers. Optional top-level `description` in `hooks.json`. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- Command handler fields: `type: "command"`, `command`, `timeout` (seconds, default 600; `SessionEnd`/`Interrupt` default 1s, max 3s), `statusMessage`, `additionalContextLimit` (default about 2500 tokens; `0` means unlimited), `commandWindows`/`command_windows`, `async` (default false). — [Hooks](https://learn.chatgpt.com/docs/hooks.md); [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md)
- MCP tool handler: `type: "mcp_tool"`, `server` (an already-connected server), `tool`, `input` (argument template with `${tool_input.file_path}`-style placeholders; a placeholder that fills a whole value keeps its JSON type), `timeout` (600), `statusMessage`. It uses existing connections only, runs synchronously, and errors or missing servers don't block. `SessionEnd` doesn't support MCP hooks. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- Minimal example (`~/.codex/hooks.json`):
  ```json
  {"hooks":{"PreToolUse":[{"matcher":"^Bash$","hooks":[{"type":"command","command":"python3 ~/.codex/hooks/policy.py","timeout":30,"statusMessage":"Checking Bash command"}]}]}}
  ```
  Equivalent TOML: `[[hooks.PreToolUse]] matcher = "^Bash$"` + `[[hooks.PreToolUse.hooks]] type = "command" ...`. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)

**Events (12) and matchers**
- During a turn: `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `UserPromptSubmit`, `SubagentStop`, `Stop`. On interrupt: `Interrupt` (not for subagents). At session or subagent start: `SessionStart`, `SubagentStart`. When the main thread ends: `SessionEnd` (not for subagents). — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- Matcher targets: `PreToolUse`/`PostToolUse`/`PermissionRequest` match the tool name. `apply_patch` also matches `Edit` or `Write`, shell and `exec_command` match `Bash`, MCP tools match `mcp__server__tool`, other local function tools match by name (for example `update_plan`), and `spawn_agent` also matches `Agent`. `SessionStart` matches the source (`startup|resume|clear|compact`). `Pre/PostCompact` match `manual|auto`. `SessionEnd` matches the reason (only `other`). `SubagentStart`/`Stop` match the agent type. `UserPromptSubmit`, `Stop` and `Interrupt` ignore matchers. Hosted tools such as WebSearch are never hooked. "Treat tool hooks as a useful guardrail, not a complete enforcement boundary." — [Hooks](https://learn.chatgpt.com/docs/hooks.md)

**Input (stdin JSON)**
- Common fields: `session_id` (subagents get the parent's id), `transcript_path` (format not stable), `cwd`, `hook_event_name`, `model`. Turn-scoped events add `turn_id`. Most events add `permission_mode` (`default|acceptEdits|plan|dontAsk|bypassPermissions`). Event-specific fields: `source` (SessionStart); `reason` (SessionEnd); `agent_id`/`agent_type` (SubagentStart/Stop), plus `agent_transcript_path`, `stop_hook_active` and `last_assistant_message` (SubagentStop); `tool_name`, `tool_use_id`, `tool_input` (Pre/PostToolUse), plus `tool_response` (PostToolUse); `tool_input.description` (PermissionRequest); `trigger` (Pre/PostCompact); `prompt` (UserPromptSubmit); `stop_hook_active` and `last_assistant_message` (Stop). Generated wire schemas live at `codex-rs/hooks/schema/generated`. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)

**Output semantics**
- Exit 0 with no output means success. Common JSON fields `continue`, `stopReason`, `systemMessage` (shown as a UI warning) and `suppressOutput` (parsed but not implemented) apply to SessionStart, Pre/PostCompact, UserPromptSubmit, SubagentStop and Stop. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- Plain stdout becomes developer context for SessionStart, UserPromptSubmit and SubagentStart (the latter for the subagent). It is ignored for Pre/PostToolUse, PermissionRequest and Pre/PostCompact, and is invalid for Stop, SubagentStop and Interrupt, which require JSON. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- `PreToolUse`: deny with `hookSpecificOutput.permissionDecision: "deny"` plus `permissionDecisionReason`, the legacy `{"decision":"block","reason":...}`, or exit 2 with the reason on stderr. Rewrite the call with `permissionDecision: "allow"` plus `updatedInput` (Bash and apply_patch need a string `command`). Add context with `additionalContext`. `"ask"`, `decision:"approve"`, `continue:false` and `stopReason` are unsupported: the hook run is marked failed and the tool call proceeds. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- `PermissionRequest`: return `decision.behavior` `allow` or `deny` (with `message`). Any deny wins. With no decision, the normal approval prompt appears. `updatedInput`, `updatedPermissions` and `interrupt` "fail closed today". — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- `PostToolUse`: `decision:"block"` or exit 2 replaces the tool result with your feedback (it cannot undo side effects). `continue:false` stops normal processing of the result. `additionalContext` is supported. `updatedMCPToolOutput` is not supported yet. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- `UserPromptSubmit`: block with `decision:"block"` or exit 2, or add context. `Stop`/`SubagentStop`: `decision:"block"` plus `reason` (or exit 2) makes Codex continue with `reason` as a new prompt, and `continue:false` from any hook wins. `PreCompact` `continue:false` cancels compaction. `SessionStart` with source `compact` runs after compaction, before the next model request. `Interrupt` accepts only `systemMessage`. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- Large output: `additionalContext` over the limit is "spilled" to `<CODEX_HOME>/hook_outputs/...txt`, and the model gets a head-and-tail preview. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- Async hooks (`async: true`): run in the background and deliver `additionalContext`/`systemMessage` at the next safe point. They can't block or rewrite. At most 8 run concurrently per session, unfinished ones are cancelled at session end, and `SessionEnd` always runs synchronously. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- Code mode: a `PreToolUse` block rejects the nested JS tool promise, and `updatedInput` rewrites the call. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)

**Managed and plugin hooks**
- `requirements.toml` can define `[hooks]` with `managed_dir` / `windows_managed_dir` (absolute paths whose scripts are deployed by MDM, not by Codex). `allow_managed_hooks_only = true` skips user, project, session and plugin hooks. Pin `[features].hooks = true` to enforce them. Under cloud orchestration (Work Cloud and dots), only admin `mcp_tool` hooks are supported. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- Plugin hooks receive the env vars `PLUGIN_ROOT` and `PLUGIN_DATA`, and "Codex also sets `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` for compatibility with existing plugin hooks." Manifest hook paths must start with `./` and stay inside the plugin root. — [Hooks](https://learn.chatgpt.com/docs/hooks.md)
- Metrics: `hooks.run` and `hooks.run.duration_ms` (OTel). — [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced.md)

**Notifications**
- `notify = ["python3", "/path/to/notify.py"]` runs an external program "whenever Codex emits supported events (currently only `agent-turn-complete`)". The program receives one JSON argv argument with `type`, `thread-id`, `turn-id`, `cwd`, `input-messages` and `last-assistant-message`. — [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced.md)
- `notify` is ignored in project `.codex/config.toml` (with a startup warning) and must be set in user config. — [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced.md)
- TUI: `tui.notifications` (bool, or an array of event types such as `agent-turn-complete` or `approval-requested`), `tui.notification_method` (`auto|osc9|bel`; auto prefers OSC 9 and falls back to BEL), `tui.notification_condition` (`unfocused` by default, or `always`). — [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced.md); [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md)
- The desktop app has its own notification settings (turn completion: never, background or always; permission and question notifications) and an Activity view. The IDE extension has no notification controls, so configure `notify` on the host instead. — [Notifications](https://learn.chatgpt.com/docs/notifications.md)

### Inferences
- Hook scripts written for Claude Code largely carry over: same event names for the overlapping set, stdin JSON fields, exit-code-2 semantics, `hookSpecificOutput`, `permissionDecision`, and `CLAUDE_PLUGIN_ROOT`. They differ in a few places: `prompt`/`agent` handler types are skipped, `"ask"` is unsupported, hash-based trust is required, and there are Codex-only events (`Interrupt`, `PermissionRequest` semantics) and fields (`turn_id`, `model`).
- Because `notify` supports only `agent-turn-complete`, richer automation (approval requests, stop gating) should use hooks (`PermissionRequest`, `Stop`) rather than `notify`.

### Gaps
- Exact precedence when the same hook is defined in several layers (it seems all run, as nothing is deduplicated) beyond "all load".
- No documented TUI-notification event list beyond the two examples.

## Workflows / automation: codex exec, SDKs, GitHub Action, code review, cloud tasks/codex cloud, scheduled tasks, worktrees

### Takeaway
Codex offers several automation surfaces. `codex exec` is the headless CLI: read-only by default, with JSONL events, `--output-schema`, resume and fork. `codex review` runs headless reviews. The TypeScript SDK (`@openai/codex-sdk`) and the stable Python SDK (`openai-codex`) drive the local app-server. The app-server JSON-RPC protocol is for custom clients and replaces the removed MCP server. `openai/codex-action@v1` serves GitHub Actions. Cloud surfaces are `@codex review` and automatic GitHub PR reviews, Codex Cloud tasks, and the experimental `codex cloud` CLI. The desktop app adds scheduled tasks (RRULE schedules, local or worktree execution, `$skill` in prompts). The CLI cannot manage scheduled tasks.

### Cited Findings
**`codex exec`**
- Streams progress to stderr and prints only the final message to stdout. The default sandbox is read-only, and `--sandbox workspace-write` or `danger-full-access` widens it. `--full-auto` is "deprecated compatibility flag". `--ephemeral` skips writing rollout files. Without a prompt, or with `-`, it reads the prompt from stdin, and when both are given, stdin is appended as a `<stdin>` block. A Git repo is required unless `--skip-git-repo-check` is set. `--ignore-user-config` and `--ignore-rules` exist. An MCP server with `required = true` that fails makes exec exit with an error. — [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md); local `codex exec --help`
- `--json` (alias `--experimental-json`) turns stdout into JSONL with event types `thread.started`, `turn.started`, `turn.completed` (with `usage`), `turn.failed`, `item.*` and `error`. Item types: agent messages, reasoning, command executions, file changes, MCP tool calls, web searches, plan updates. `-o/--output-last-message <file>` writes the final message to a file. `--output-schema <file>` takes a JSON Schema for the final response. — [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md); [CLI command reference](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)
- Resume: `codex exec resume --last "follow-up"` (scoped to the cwd; `--all` searches all directories) or `codex exec resume <SESSION_ID|name>`. 0.159.2 also has `codex exec fork` and `codex exec review`, plus `--thread-source` and `--worktree`. — [CLI command reference](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli); local `codex exec --help`
- Auth: `CODEX_API_KEY=<key> codex exec ...` works for `codex exec`, `codex review`, the TS SDK and `codex exec-server --remote`. Don't set the key at job level in workflows that run repository code. ChatGPT-managed `auth.json` in CI is "advanced", and not for public repositories. — [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)
- Minimal structured-output example: `codex exec "Extract project metadata" --output-schema ./schema.json -o ./project-metadata.json`. — [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)

**`codex review` and `/review`**
- `codex review [--uncommitted | --base BRANCH | --commit SHA [--title T] | PROMPT|-]`: the targets are mutually exclusive. — [CLI command reference](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli); local `codex review --help`
- `/review` (CLI, IDE, app) "starts a dedicated reviewer that reads the selected diff and reports prioritized, actionable findings without changing your working tree". The presets are base branch and uncommitted changes. It uses the session model unless `review_model` is set. — [Code review](https://learn.chatgpt.com/docs/code-review.md); [Slash commands](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)
- GitHub cloud review: comment `@codex review` on a PR, or turn on Automatic review in Codex settings. In GitHub, Codex flags only P0/P1 issues. Review rules come from a `## Code Review Rules` section in the nearest `AGENTS.md`. GitLab MR review is in preview. — [Review GitHub pull requests with Codex](https://learn.chatgpt.com/docs/third-party/github.md); [Code review](https://learn.chatgpt.com/docs/code-review.md)

**SDKs and app-server**
- TypeScript: `npm install @openai/codex-sdk` (Node 18+). `new Codex().startThread().run(prompt)` returns `result.finalResponse`. Calling `run()` again continues the thread, and `resumeThread(id)` resumes one. — [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk.md)
- Python: `pip install openai-codex` (stable; Python 3.10+). It controls the local app-server over JSON-RPC and pins a Codex CLI runtime. `Codex()`/`AsyncCodex()`, `thread_start(model=..., sandbox=Sandbox.workspace_write)`, `thread.run(...)` returns `.final_response`. Sandbox presets are `read_only`, `workspace_write` and `full_access`, and a per-turn sandbox persists to later turns. — [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk.md)
- The app-server (`codex app-server`, marked experimental in the CLI table) is the protocol for custom clients: threads, turns, `turn/steer`, `turn/interrupt`, `skills/list`, and more. — [Codex App Server](https://learn.chatgpt.com/docs/app-server.md); [CLI command reference](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)

**GitHub Action**
- `openai/codex-action@v1` installs the CLI, starts a Responses API proxy when `openai-api-key` is given, and runs `codex exec`. Inputs: `prompt` or `prompt-file` (exactly one), `codex-args` (JSON array or shell string), `model`, `effort`, `sandbox`, `output-file`, `codex-version`, `codex-home`, `safety-strategy` (default `drop-sudo`; also `unprivileged-user` with `codex-user`, `read-only`, and `unsafe`, which Windows requires), `allow-users`, `allow-bots`. Output: `final-message`. — [Codex GitHub Action](https://learn.chatgpt.com/docs/github-action.md)
- Recommended CI-autofix pattern: the Codex job runs with `contents: read` and produces a patch artifact, and a separate job with write permissions but no API key opens the PR. — [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)

**Cloud**
- Codex Cloud tasks run in published cloud environments (repos, tools, network and secrets), "each task has its own workspace and can keep working while your computer is asleep". Codex Cloud (Legacy) environments still back Code Review and the Linear and GitHub integrations. They use the `universal` image, setup and maintenance scripts, and agent internet access off by default. — [Codex Cloud](https://learn.chatgpt.com/docs/cloud.md); [Codex Cloud (Legacy)](https://learn.chatgpt.com/docs/environments/cloud-environment.md)
- `codex cloud` (experimental): an interactive picker, plus `exec` (`--env` required, `--attempts 1-4`), `list` (`--json`, `--limit 1-20`, `--cursor`, `--env`), `status`, `diff` and `apply`. `codex apply` applies the latest cloud diff locally. — [CLI command reference](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli); local `codex cloud --help`

**Scheduled tasks (formerly "Automations") and worktrees**
- Created and managed in the ChatGPT desktop app or on the web (**Scheduled** page). "Codex CLI doesn't provide the Scheduled management interface", and neither does the IDE extension. — [Scheduled tasks](https://learn.chatgpt.com/docs/automations.md)
- Desktop: a standalone task (new chat per run, can span several projects) or a task inside an existing chat (keeps context, minute-based intervals allowed). Custom cadence uses an RFC 5545 RRULE, for example `RRULE:FREQ=MONTHLY;BYMONTHDAY=1;BYHOUR=9;BYMINUTE=0`. Git projects run either in the local checkout or in a dedicated background worktree. The app must be running and the machine on. Tasks run with `approval_policy = "never"` when policy allows it, otherwise they fall back to the selected permission mode. Prompts can use `$skill-name`, and skills can create or update scheduled tasks. — [Scheduled tasks](https://learn.chatgpt.com/docs/automations.md)
- Event triggers (Gmail, Slack, GitHub PR activity) exist only on ChatGPT web and mobile, not in the desktop app, CLI or IDE, and can't be combined with a time schedule. — [Scheduled tasks](https://learn.chatgpt.com/docs/automations.md)
- Guidance: "skills define the method and scheduled tasks define the schedule." — [Best practices](https://learn.chatgpt.com/docs/codex-manual.md)
- Worktrees: desktop Worktree mode with Handoff, and local environments supply setup scripts for worktrees. Frequent scheduled tasks can pile up worktrees, so archive old runs. — [Worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees.md); [Local environments](https://learn.chatgpt.com/docs/environments/local-environment.md); [Scheduled tasks](https://learn.chatgpt.com/docs/automations.md)
- Other 0.159.2 CLI automation commands seen locally: `codex queue` ("Queue a message for an existing session"), `codex fork`, `codex resume`, `codex remote-control` (experimental), and `codex exec-server` (experimental). The `goals` feature (persisted goals and automatic continuation, `/goal`) is stable and on. — local `codex --help`, `codex features list`; [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md)

### Inferences
- For CI, use `openai/codex-action` with `--output-schema` passed through `codex-args`. For long-running or multi-turn pipelines, use the SDKs, or `codex exec` plus `exec resume`. Recurring local jobs need the desktop app, because the CLI cannot schedule tasks. On a headless machine, plain cron plus `codex exec` is the fallback (not an official feature).

### Gaps
- Not read: the detailed Cloud environments page (setup scripts, secrets, saved state) and the GitHub/Linear/Slack integration triggers beyond `@codex review`.
- No documented way to start scheduled tasks or event triggers from the CLI or an API. Team Tasks run through service accounts and are an admin feature not explored here.
