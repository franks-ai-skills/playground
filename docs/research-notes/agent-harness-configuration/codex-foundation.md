# OpenAI Codex harness configuration: foundation layer (AGENTS.md, config.toml, profiles, approvals/sandbox, rules, MCP, plugins, models/providers)

Research date: 2026-10-04. Locally installed: `codex-cli 0.159.2` (Homebrew). The official changelog already lists 0.159.3 and 0.160.0, so the local install is slightly behind the latest release ([Changelog](https://developers.openai.com/codex/changelog)).

Source abbreviations used below (all fetched 2026-10-04):
- AGENTS guide = https://developers.openai.com/codex/guides/agents-md
- Config basics = https://developers.openai.com/codex/config-basic
- Advanced config = https://developers.openai.com/codex/config-advanced
- Config reference = https://developers.openai.com/codex/config-reference
- Sample config = https://developers.openai.com/codex/config-sample
- Security = https://developers.openai.com/codex/agent-approvals-security
- Sandboxing = https://developers.openai.com/codex/concepts/sandboxing
- Permissions = https://developers.openai.com/codex/permissions
- Rules = https://developers.openai.com/codex/rules
- MCP = https://developers.openai.com/codex/mcp
- Plugins = https://developers.openai.com/codex/plugins
- Build plugins = https://developers.openai.com/codex/plugins/build
- Managed config = https://developers.openai.com/codex/enterprise/managed-configuration
- Models = https://developers.openai.com/codex/models
- CLI reference = https://developers.openai.com/codex/cli/reference
- Agents SDK guide = https://developers.openai.com/codex/guides/agents-sdk
- Changelog = https://developers.openai.com/codex/changelog
- Local CLI = output of `codex --help`, `codex mcp add --help`, `codex plugin ... --help`, `codex features list`, `codex execpolicy --help`, `codex debug --help` on codex-cli 0.159.2 (read-only commands, run 2026-10-04)

---

## 1. AGENTS.md: discovery, size limits, fallback filenames, combination

### Takeaway
Codex builds one instruction chain per run: at most one global file from `$CODEX_HOME` (`AGENTS.override.md` wins over `AGENTS.md`), then at most one file per directory from the project root down to the cwd (`AGENTS.override.md` → `AGENTS.md` → `project_doc_fallback_filenames`). It concatenates them root-to-leaf, so files closer to the cwd come later and take precedence, and it stops adding files at `project_doc_max_bytes` (default 32 KiB). The docs disagree on whether that limit applies per file or to the combined total.

### Cited Findings
**What it is / problem solved**
- Codex reads `AGENTS.md` files before doing any work. Layering global guidance with project overrides gives each task the same expectations in any repo — [AGENTS guide](https://developers.openai.com/codex/guides/agents-md)

**Discovery order (precedence)**
- Global scope: in the Codex home (`~/.codex` unless `CODEX_HOME` is set), Codex reads `AGENTS.override.md` if it exists, otherwise `AGENTS.md`. It uses only the first non-empty file at this level — [AGENTS guide](https://developers.openai.com/codex/guides/agents-md)
- Project scope: starting at the project root (typically the Git root), Codex walks down to the cwd. If it can't find a project root, it checks only the cwd. In each directory it checks `AGENTS.override.md`, then `AGENTS.md`, then each name in `project_doc_fallback_filenames`, and includes at most one file per directory — [AGENTS guide](https://developers.openai.com/codex/guides/agents-md)
- Merge: files are concatenated from the root down, joined with blank lines. Files closer to the cwd override earlier guidance because they appear later in the combined prompt — [AGENTS guide](https://developers.openai.com/codex/guides/agents-md)
- Codex stops searching at the cwd. An `AGENTS.md` in the same directory as an `AGENTS.override.md` is ignored — [AGENTS guide](https://developers.openai.com/codex/guides/agents-md)
- Project root detection: by default a directory containing `.git` is the root. `project_root_markers` (default `[".git"]`) customizes this, for example `[".git", ".hg", ".sl"]`. `project_root_markers = []` skips the parent search and treats the cwd as the root — [Advanced config](https://developers.openai.com/codex/config-advanced); default from [Sample config](https://developers.openai.com/codex/config-sample)
- Discovery runs once per run (in the TUI, once per launched session). There is no cache, so restarting Codex picks up changes — [AGENTS guide](https://developers.openai.com/codex/guides/agents-md)
- Project guidance goes into the first turn of a session — [Advanced config](https://developers.openai.com/codex/config-advanced); "embed into first-turn instructions" — [Sample config](https://developers.openai.com/codex/config-sample)

**Size limits and fallbacks**
- Codex skips empty files and stops adding files once the combined size reaches `project_doc_max_bytes` (32 KiB by default). If you hit the cap, raise the limit or split instructions across nested directories — [AGENTS guide](https://developers.openai.com/codex/guides/agents-md)
- `project_doc_max_bytes` (number): "Maximum bytes read from `AGENTS.md` when building project instructions" — [Config reference](https://developers.openai.com/codex/config-reference). Default `32768` — [Sample config](https://developers.openai.com/codex/config-sample)
- Conflict: Advanced Config describes `project_doc_max_bytes` as "how much to read from each `AGENTS.md` file" (per file) — [Advanced config](https://developers.openai.com/codex/config-advanced). The AGENTS guide says the limit is on the combined size — [AGENTS guide](https://developers.openai.com/codex/guides/agents-md)
- `project_doc_fallback_filenames` (array<string>, default `[]`) lists extra filenames to try when `AGENTS.md` is missing at a directory level. Example: `project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]` gives the per-directory order `AGENTS.override.md`, `AGENTS.md`, `TEAM_GUIDE.md`, `.agents.md`. Names not on the list are ignored — [AGENTS guide](https://developers.openai.com/codex/guides/agents-md); default from [Sample config](https://developers.openai.com/codex/config-sample)

**Related instruction keys (config.toml)**
- `model_instructions_file` (path) replaces the built-in instructions instead of `AGENTS.md`. In a project config, relative paths resolve against the `.codex/` folder that contains the `config.toml` — [Config reference](https://developers.openai.com/codex/config-reference); [Advanced config](https://developers.openai.com/codex/config-advanced)
- `developer_instructions` (string) adds developer instructions to the session — [Config reference](https://developers.openai.com/codex/config-reference)
- `instructions` (string) is "Reserved for future use; prefer `model_instructions_file` or `AGENTS.md`" — [Config reference](https://developers.openai.com/codex/config-reference)
- `compact_prompt` / `experimental_compact_prompt_file` override the history-compaction prompt — [Config reference](https://developers.openai.com/codex/config-reference)
- Managed `additional_developer_instructions` (requirements.toml) adds a separate developer message. Codex rejects values over 10,000 estimated tokens — [Config reference](https://developers.openai.com/codex/config-reference)
- For GitHub code review, Codex reads a `## Code Review Rules` section in the `AGENTS.md` closest to the code — [AGENTS guide](https://developers.openai.com/codex/guides/agents-md)

**Tooling / verification**
- `/init` creates an `AGENTS.md` scaffold in the current directory — [CLI reference](https://developers.openai.com/codex/cli/reference)
- To audit which files loaded: `codex -c log_dir=./.codex-log`, then check `./.codex-log/codex-tui.log`, or ask "Show which instruction files are active." — [AGENTS guide](https://developers.openai.com/codex/guides/agents-md)
- Setting `CODEX_HOME` points Codex at a different home directory (global AGENTS.md, config, and so on), for example `CODEX_HOME=$(pwd)/.codex codex exec ...` — [AGENTS guide](https://developers.openai.com/codex/guides/agents-md)

**Minimal example**
```
~/.codex/AGENTS.md                      # global (or AGENTS.override.md to temporarily replace it)
<repo>/AGENTS.md                        # repo-wide
<repo>/services/payments/AGENTS.override.md   # replaces AGENTS.md in that dir; appended last
```
```toml
# ~/.codex/config.toml
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
project_doc_max_bytes = 65536
```
— [AGENTS guide](https://developers.openai.com/codex/guides/agents-md)

### Inferences
- Because each directory contributes at most one file, an `AGENTS.override.md` *replaces* that directory's `AGENTS.md`. It doesn't add to it. Across directories, files accumulate.
- When the byte cap is hit, the files nearest the cwd are the ones dropped, because concatenation runs root-first. Splitting large root files therefore matters.
- Untrusted projects skip `.codex/` layers, but nothing in the docs says untrusted projects skip AGENTS.md. Trust gating is documented only for `.codex/` config, hooks and rules.

### Gaps
- Per-file vs combined semantics of `project_doc_max_bytes` are contradictory in the docs. Source (`codex-rs`) could not be checked: the GitHub API was rate-limited and the guessed raw path `codex-rs/core/src/project_doc.rs` returned 404.
- Whether truncation cuts a file mid-way or drops whole files isn't documented beyond "stops adding files".
- No documented effect of project trust on AGENTS.md loading.

---

## 2. config.toml: scopes, trust, profiles, important keys, CLI overrides, managed config / requirements.toml

### Takeaway
One TOML config system is shared by the CLI, the IDE extension and Codex in the ChatGPT desktop app. Precedence, from highest to lowest: CLI flags / `-c` → project `.codex/config.toml` files (closest to the cwd wins; trusted projects only) → `--profile` file `~/.codex/<name>.config.toml` → user `~/.codex/config.toml` → cloud-managed defaults → system `/etc/codex/config.toml` → built-ins. Two separate admin layers sit on top. `requirements.toml` holds constraints the user can't override (system file → cloud/Agent Security → legacy `managed_config.toml` → macOS MDM). Legacy `managed_config.toml` / MDM `config_toml_base64` holds defaults that override even `-c` at startup. Profiles changed in 0.134.0: they are now separate files, and `[profiles.x]` tables no longer work.

### Cited Findings
**Scopes and precedence**
- User config lives at `~/.codex/config.toml`. Project overrides live in `.codex/config.toml` files and load only when the project is trusted. The CLI and IDE extension share the same config layers — [Config basics](https://developers.openai.com/codex/config-basic)
- Resolution order, highest first: (1) CLI flags and `--config` overrides; (2) project `.codex/config.toml` files from the project root down to the cwd (closest wins; trusted projects only); (3) profile file selected with `--profile` (`~/.codex/<profile>.config.toml`); (4) user `~/.codex/config.toml`; (5) cloud-managed `config.toml` defaults for the signed-in workspace; (6) system `/etc/codex/config.toml` on Unix; (7) built-in defaults — [Config basics](https://developers.openai.com/codex/config-basic)
- Codex walks from the project root to the cwd and loads every `.codex/config.toml` it finds. When files set the same key, the closest one wins — [Advanced config](https://developers.openai.com/codex/config-advanced)
- If a project is untrusted, Codex skips project `.codex/` layers: project-local config, hooks and rules. User and system layers still load — [Config basics](https://developers.openai.com/codex/config-basic); [Advanced config](https://developers.openai.com/codex/config-advanced)
- Trust is stored in user config as `[projects."<abs path>"] trust_level = "trusted" | "untrusted"`. Untrusted projects skip project `.codex/` layers — [Config reference](https://developers.openai.com/codex/config-reference). The local `~/.codex/config.toml` has exactly this shape (`[projects."/path"] trust_level = ...`) — Local CLI (redacted structure inspection)
- Project config is not allowed to set these keys; Codex ignores them with a startup warning: `openai_base_url`, `chatgpt_base_url`, `apps_mcp_product_sku`, `model_provider`, `model_providers`, `notify`, `profile`, `profiles`, `experimental_realtime_ws_base_url`, `otel` — [Advanced config](https://developers.openai.com/codex/config-advanced); [Config reference](https://developers.openai.com/codex/config-reference)
- Cloud-managed and system config can define plugin marketplaces and plugin default-enabled state. These are defaults, not enforced policy — [Config basics](https://developers.openai.com/codex/config-basic); [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)
- `CODEX_HOME` defaults to `~/.codex` and holds `config.toml`, `auth.json` (when file-based credential storage is used, otherwise the OS keychain), `history.jsonl`, logs and caches — [Advanced config](https://developers.openai.com/codex/config-advanced)

**Profiles (changed in 0.134.0)**
- `--profile <name>` loads `~/.codex/config.toml` and then overlays `~/.codex/<name>.config.toml`. Names can use letters, numbers, hyphens and underscores. Keys in the profile file are top-level, not nested under `[profiles.<name>]` — [Advanced config](https://developers.openai.com/codex/config-advanced)
- Deprecated/removed: "In Codex 0.134.0 and later, `--profile` no longer reads `[profiles.profile-name]` from `config.toml`, and the top-level `profile = "profile-name"` selector is no longer supported." Move legacy settings into `~/.codex/<name>.config.toml` — [Advanced config](https://developers.openai.com/codex/config-advanced)
- CLI help confirms the new behavior: `-p, --profile <CONFIG_PROFILE_V2>  Layer $CODEX_HOME/<name>.config.toml on top of the base user config` — Local CLI (`codex --help`, 0.159.2)
- A profile file can override `model_catalog_json` — [Advanced config](https://developers.openai.com/codex/config-advanced)

**CLI overrides**
- `-c/--config key=value`: dotted paths set nested values. The value is parsed as TOML, and if that fails it is used as a literal string. Examples: `-c model="o3"`, `-c shell_environment_policy.inherit=all` — Local CLI (`codex --help`)
- Doc examples: `codex --config model='"gpt-6.1-sol"'`, `codex --config sandbox_workspace_write.network_access=true`, `-c mcp_servers.context7.enabled=false`. Prefer dedicated flags such as `--model` when they exist — [Advanced config](https://developers.openai.com/codex/config-advanced)
- `--enable <FEATURE>` / `--disable <FEATURE>` are equivalent to `-c features.<name>=true|false` — Local CLI (`codex --help`)
- `--strict-config` errors on `config.toml` fields this version doesn't recognize. It is supported on `codex`, `exec`, `review`, `resume`, `fork`, `app-server` and `exec-server` — [CLI reference](https://developers.openai.com/codex/cli/reference)
- `codex exec --ignore-user-config` doesn't load `$CODEX_HOME/config.toml` (auth still uses `CODEX_HOME`). `--ignore-rules` skips user and project `.rules` files — [CLI reference](https://developers.openai.com/codex/cli/reference)
- Other global flags: `-m/--model`, `--oss`, `--local-provider lmstudio|ollama`, `-s/--sandbox`, `-a/--ask-for-approval`, `--add-dir`, `-C/--cd`, `--search`, `--worktree`, `--approve-for-me`, `--dangerously-bypass-approvals-and-sandbox`, `--dangerously-bypass-hook-trust` — Local CLI (`codex --help`)
- `/debug-config` (TUI) prints config layer and requirements diagnostics. `/status` shows the active model, approval policy, writable roots and context — [CLI reference](https://developers.openai.com/codex/cli/reference)
- `codex doctor [--json] [--summary]` diagnoses install, config, auth and runtime health (redacted JSON report) — Local CLI (`codex doctor --help`)

**Important top-level keys (meaning; default where documented)**
- `model` (string), e.g. `gpt-6.1-sol` — [Config reference](https://developers.openai.com/codex/config-reference). `model_provider` (default `openai`) — [Config reference](https://developers.openai.com/codex/config-reference)
- `model_reasoning_effort`: levels the model advertises, e.g. `low|medium|high|xhigh|max|ultra`. `plan_mode_reasoning_effort`: Plan-mode override. `model_reasoning_summary`: `auto|concise|detailed|none`. `model_verbosity`: `low|medium|high` (Responses API only). `model_context_window`; `model_auto_compact_token_limit` with `model_auto_compact_token_limit_scope` (`total` default | `body_after_prefix`); `model_supports_reasoning_summaries`; `model_catalog_json`; `review_model` (for `/review`); `service_tier` (`fast` maps to the request value `priority`); `personality` (`none|friendly|pragmatic`) — [Config reference](https://developers.openai.com/codex/config-reference); [Advanced config](https://developers.openai.com/codex/config-advanced)
- `approval_policy`, `approvals_reviewer`, `sandbox_mode`, `[sandbox_workspace_write]`, `default_permissions`, `[permissions.*]`, `allow_login_shell` (default `true`): see section 3 — [Config reference](https://developers.openai.com/codex/config-reference)
- `[shell_environment_policy]`: `inherit = all|core|none`; `set` (map, applied after exclusions); `filters` (case-insensitive glob map of `include|exclude`, the canonical form); `ignore_default_excludes` (default `true`, meaning names with KEY/SECRET/TOKEN are NOT auto-removed; set `false` to auto-exclude them); legacy `exclude` / `include_only` arrays still work but can't be combined with `filters` in the same layer; `experimental_use_profile`. Order: automatic exclusions → custom exclusions → `set` → include allowlist. Filter keys merge case-insensitively across layers — [Advanced config](https://developers.openai.com/codex/config-advanced); [Config basics](https://developers.openai.com/codex/config-basic); [Config reference](https://developers.openai.com/codex/config-reference)
- `[features]`: boolean feature flags (see the list below) — [Config basics](https://developers.openai.com/codex/config-basic)
- `notify = ["prog", "arg"]` runs an external program with one JSON argument. The only event so far is `agent-turn-complete`; fields include `type`, `thread-id`, `turn-id`, `cwd`, `input-messages`, `last-assistant-message` — [Advanced config](https://developers.openai.com/codex/config-advanced)
- `[tui]`: `notifications` (bool or list of event types), `notification_method` (`auto` default | `osc9` | `bel`), `notification_condition` (`unfocused` default | `always`), `animations` (default true), `alternate_screen` (`auto` default | `always` | `never`), `show_tooltips` (default true), `theme`, `keymap.<context>.<action>` (contexts `global, chat, composer, editor, vim_normal, vim_operator, vim_text_object, pager, list, approval`; `[]` unbinds), `raw_output_mode`, `resume_cwd` (`current|session`), `status_line`, `terminal_title` (default `["spinner","project"]`), `vim_mode_default` — [Config reference](https://developers.openai.com/codex/config-reference); [Advanced config](https://developers.openai.com/codex/config-advanced)
- `[history]`: `persistence = "save-all" | "none"`; `max_bytes` caps `history.jsonl` by dropping the oldest entries — [Config reference](https://developers.openai.com/codex/config-reference); [Advanced config](https://developers.openai.com/codex/config-advanced)
- `[otel]`: `environment` (default `dev`), `exporter = none | otlp-http | otlp-grpc` (table form with `endpoint`, `headers`, `protocol = binary|json`, `tls.*`), `trace_exporter`, `metrics_exporter` (default `statsig`), `log_user_prompt` (default false/redacted). OTel export is off by default — [Config reference](https://developers.openai.com/codex/config-reference); [Advanced config](https://developers.openai.com/codex/config-advanced); [Security](https://developers.openai.com/codex/agent-approvals-security)
- `[analytics] enabled = false` turns off anonymous usage metrics. `[feedback] enabled = false` turns off `/feedback` — [Advanced config](https://developers.openai.com/codex/config-advanced)
- `web_search = disabled | cached (default) | indexed | live`. It defaults to `live` under `--yolo` / full access. `--search` equals `live`. The legacy `features.web_search*` toggles are deprecated. `tools.web_search` (object form) sets `context_size`, `allowed_domains` and `location` — [Config basics](https://developers.openai.com/codex/config-basic); [Config reference](https://developers.openai.com/codex/config-reference)
- Other: `file_opener` (`vscode` default | `vscode-insiders` | `windsurf` | `cursor` | `none`), `log_dir` (default `$CODEX_HOME/log`; setting it explicitly enables `codex-tui.log`), `sqlite_home`, `cli_auth_credentials_store` (`file|keyring|auto|ephemeral`; sample says default `file`), `forced_login_method` (`chatgpt|api`), `forced_chatgpt_workspace_id`, `check_for_update_on_startup`, `hide_agent_reasoning`, `show_raw_agent_reasoning`, `tool_output_token_limit`, `background_terminal_max_timeout` (default 300000 ms; replaces `background_terminal_timeout`), `skills.config[]` / `skills.max_context_tokens` (default 2% of the context window, capped at 10000), `[agents]` (multi-agent roles, `max_concurrent_threads_per_session`, `default_subagent_model`; `agents.max_threads` is a legacy alias), `[hooks]` (inline hooks), `[memories]`, `[desktop.custom_file_handlers.<id>]` (desktop app only, user-level), `[windows] sandbox`, `notice.*` (acknowledgement tracking) — [Config reference](https://developers.openai.com/codex/config-reference); [Sample config](https://developers.openai.com/codex/config-sample)
- `experimental_use_unified_exec_tool` is a legacy name. Prefer `features.unified_exec` — [Config reference](https://developers.openai.com/codex/config-reference)

**Feature flags**
- Documented common flags (default, maturity): `apps` (true, stable), `goals` (true), `hooks` (true; `features.codex_hooks` is a deprecated alias), `fast_mode` (true), `memories` (false), `multi_agent` (true), `personality` (true), `remote_plugin` (true), `shell_snapshot` (true), `shell_tool` (true), `unified_exec` (true except on Windows), `web_search` / `web_search_cached` / `web_search_request` (deprecated). `network_proxy` and `prevent_idle_sleep` are experimental and off — [Config basics](https://developers.openai.com/codex/config-basic); [Config reference](https://developers.openai.com/codex/config-reference)
- `codex features list` prints each flag's stage and effective state. `codex features enable|disable <name>` writes to `config.toml` — Local CLI (`codex features --help`)
- Conflict: the docs list `features.personality` as "Stable, true", but local `codex features list` (0.159.2) shows `personality  removed  false`. The docs list `memories` as Experimental, but the local CLI shows `memories  stable  false`. The local CLI also shows `use_legacy_landlock`, `transcript_v2`, `web_search_cached` and `web_search_request` as `deprecated`, and `use_linux_sandbox_bwrap`, `experimental_windows_sandbox`, `elevated_windows_sandbox` and `js_repl` as `removed` — Local CLI vs [Config basics](https://developers.openai.com/codex/config-basic)

**Managed configuration (admin)**
- Three admin mechanisms: Requirements (constraints users can't override), Configuration defaults (system or cloud-managed `config.toml` that users can override), and Legacy managed defaults (`managed_config.toml`, reapplied at every client start) — [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)
- requirements.toml locations, lowest to highest priority: system `/etc/codex/requirements.toml` (Unix, including macOS) or `%ProgramData%\OpenAI\Codex\requirements.toml` (Windows) → Agent Security requirements in the cloud config bundle → legacy `managed_config.toml` fields reinterpreted as requirements → macOS MDM `com.openai.codex:requirements_toml_base64`. Higher layers override scalars and lists, tables merge by key, and rules, hooks and filesystem restrictions have field-specific composition — [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)
- When a config value conflicts with a requirement, the client falls back to a compatible value and notifies the user — [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)
- Cloud-managed requirements: fetched for ChatGPT sign-ins on supported plans, then cached with a signed, identity-matched entry. If the fetch fails and there's no valid cache, loading errors instead of starting without the layer. Background refresh affects only later starts — [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)
- `managed_config.toml` lives at `/etc/codex/managed_config.toml` (Unix) or `~/.codex/managed_config.toml` (Windows/non-Unix). Precedence: MDM `config_toml_base64` > `managed_config.toml` > user `config.toml`. "CLI `--config key=value` overrides apply to the base, but managed layers override them" — [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)
- Selected `requirements.toml` keys: `allowed_approval_policies`, `allowed_approvals_reviewers`, `allowed_sandbox_modes`, `allowed_permission_profiles.<name>` (Codex ≥0.138.0; once present, omitted profiles are denied), `default_permissions`, `allowed_web_search_modes` (`disabled` is always allowed), `allowed_login_methods` / `allowed_chatgpt_workspaces` / `chatgpt_base_url` (local or MDM only; cloud values are ignored), `[features]` pins, `[rules] prefix_rules` (prompt/forbidden only), `[mcp_servers.<id>.identity]` allowlist, `[plugins.<p>.mcp_servers.<s>.identity]`, `[marketplaces] restrict_to_allowed_sources` + `allowed_sources`, `[experimental_network]`, `permissions.filesystem.deny_read`, `[hooks]` + `hooks.managed_dir`, `allow_managed_hooks_only`, `guardian_policy_config`, `[models.new_thread]` (defaults only), `model_provider` / `model_providers` (full replacement per ID), `enforce_residency = "us"`, `remote_sandbox_config[]`, `windows.allowed_sandbox_implementations`, `additional_developer_instructions`, `[browser_use]`, `[computer_use]` — [Config reference](https://developers.openai.com/codex/config-reference); [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)
- Example requirements file that blocks `never` and `danger-full-access` (including `--yolo`): `allowed_approval_policies = ["untrusted", "on-request"]` and `allowed_sandbox_modes = ["read-only", "workspace-write"]` — [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)

**Minimal example**
```toml
# ~/.codex/config.toml
model = "gpt-6.1-sol"
model_reasoning_effort = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
[sandbox_workspace_write]
network_access = false
[projects."/Users/me/code/app"]
trust_level = "trusted"
```
```toml
# ~/.codex/deep-review.config.toml   (use: codex --profile deep-review)
model_reasoning_effort = "high"
```
— [Config basics](https://developers.openai.com/codex/config-basic); [Advanced config](https://developers.openai.com/codex/config-advanced)

### Inferences
- There are two precedence stacks with different semantics. The "config" stack (user → profile → project → CLI) sets values. The "requirements" stack constrains values. Legacy `managed_config.toml` / MDM `config_toml_base64` is an odd case that sits *above* CLI `-c` at startup. Cloud `config.toml` defaults sit *below* user config.
- Profile files sit below project config. A trusted repo's `.codex/config.toml` therefore beats `--profile` for any key it sets, except the user-only keys (provider, notify, otel and so on), which projects can't set.
- Any automation that uses `[profiles.x]` or a top-level `profile =` key broke silently or with warnings from 0.134.0 on and needs migration.

### Gaps
- No machine-readable JSON Schema URL for config.toml was found in the fetched docs. `codex app-server generate-json-schema` exists but covers the app-server protocol, not config — Local CLI (`codex app-server --help`).
- The exact merge behavior of arrays across layers (replace vs append) isn't stated for config.toml in general. It's documented only for specific fields (shell env filters, permission profiles).
- The fetched "team-config" URL returned an enterprise rollout guide, not the "Team Config" page that Advanced Config references for repo/system skills and rules locations. Its content isn't covered here.

---

## 3. Approval policies, sandbox modes, permission profiles, platform sandboxes, network, rules/execpolicy

### Takeaway
As of late 2026, `approval_policy` accepts only `on-request` (the default), `never`, or a `{ granular = {...} }` table. `untrusted` is retired and can stop the client from starting. `on-failure` is deprecated. The stricter "ask for everything" behavior now comes from `trust_level = "untrusted"` on a project entry. Sandboxing is either the legacy `sandbox_mode` (`read-only` / `workspace-write` / `danger-full-access`) or the beta named permission profiles (`default_permissions`, `[permissions.<name>]`; built-ins `:read-only`, `:workspace`, `:danger-full-access`). The two systems are mutually exclusive. Enforcement uses Seatbelt on macOS, bwrap + seccomp on Linux/WSL2, and a native sandbox on Windows. Network is off by default, and an optional proxy enforces domain rules. Starlark `.rules` files (`prefix_rule`) decide which commands can run outside the sandbox.

### Cited Findings
**Approval policies**
- `approval_policy`: `on-request | never | { granular = { sandbox_approval, rules, mcp_elicitations, request_permissions, skill_approval } }`. "`untrusted` is unsupported, and `on-failure` is deprecated; use `on-request` for interactive runs or `never` for non-interactive runs." — [Config reference](https://developers.openai.com/codex/config-reference)
- `on-request` is the default ("model decides when to ask") — [Sample config](https://developers.openai.com/codex/config-sample). CLI help lists only `on-request` and `never` for `-a/--ask-for-approval` — Local CLI (`codex --help`)
- Retired `untrusted`: "Codex and ChatGPT Work no longer support `approval_policy = "untrusted"`. The retired setting can prevent either client from starting." Remove it from user and project config, profile files, startup scripts and managed defaults. To keep stricter approvals, omit `approval_policy` and set `[projects."/path"] trust_level = "untrusted"` in user config. Commands then need approval unless a rule allows them, and project-local config is disabled. Explicit `on-request` overrides this, and managed `allowed_approval_policies` must include `untrusted` to permit it — [Security](https://developers.openai.com/codex/agent-approvals-security); [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)
- Granular sub-keys, each `true` = the prompt may surface, `false` = auto-reject: `sandbox_approval` (sandbox escalation), `rules` (execpolicy `prompt` rules), `mcp_elicitations`, `request_permissions` (request_permissions tool), `skill_approval` (skill scripts) — [Config reference](https://developers.openai.com/codex/config-reference)
- `approvals_reviewer = "user"` (default) | `"auto_review"`. Auto-review sends eligible approval requests to a reviewer subagent and doesn't change the sandbox boundary. Local policy text goes in `[auto_review].policy` / `extra_policy`. Managed `guardian_policy_config` / `guardian_extra_policy` take precedence. Admins restrict it via `allowed_approvals_reviewers`. Reviewer failures fail closed — [Security](https://developers.openai.com/codex/agent-approvals-security); [Config reference](https://developers.openai.com/codex/config-reference)
- `--approve-for-me` routes approval requests through automatic review using the workspace-write sandbox — Local CLI (`codex --help`)
- Destructive app/MCP tool calls always require approval when the tool advertises a destructive annotation, unless it advertises a read annotation — [Security](https://developers.openai.com/codex/agent-approvals-security)
- `codex exec --full-auto` is a deprecated compatibility flag that prints a warning. Use `--sandbox workspace-write` — [CLI reference](https://developers.openai.com/codex/cli/reference); [Security](https://developers.openai.com/codex/agent-approvals-security)

**Sandbox modes (legacy but still primary in the docs)**
- `sandbox_mode = read-only | workspace-write | danger-full-access` — [Config reference](https://developers.openai.com/codex/config-reference). The sample config comments it as "read-only (default)" — [Sample config](https://developers.openai.com/codex/config-sample)
- Launch defaults: Codex detects version control. Version-controlled folders get `Auto` (workspace-write + on-request) and others get `read-only`. Codex may start in read-only until the directory is trusted. The workspace includes the cwd and temp dirs such as `/tmp` — [Security](https://developers.openai.com/codex/agent-approvals-security)
- `[sandbox_workspace_write]`: `writable_roots` (array), `network_access` (bool, off by default), `exclude_tmpdir_env_var`, `exclude_slash_tmp` — [Config reference](https://developers.openai.com/codex/config-reference); [Advanced config](https://developers.openai.com/codex/config-advanced). CLI `--add-dir <DIR>` adds writable directories — Local CLI
- Protected paths inside writable roots are read-only (recursive): `<root>/.git` (dir or file, plus the resolved gitdir for pointer files), `<root>/.agents` (if a dir), `<root>/.codex` (if a dir) — [Security](https://developers.openai.com/codex/agent-approvals-security). In 0.159.0, `.aws` directories under writable roots also became protected (PR #48176) — [Changelog](https://developers.openai.com/codex/changelog)
- `--dangerously-bypass-approvals-and-sandbox` (alias `--yolo`): no sandbox and no approvals. Intended only for externally sandboxed environments — [Security](https://developers.openai.com/codex/agent-approvals-security); Local CLI

**Permission profiles (beta; Codex ≥0.138.0 for managed allowlists)**
- Built-ins: `:read-only`, `:workspace` (writes in workspace roots and system temp dirs), `:danger-full-access`. Custom profiles use `[permissions.<name>]` plus `default_permissions = "<name>"` — [Permissions](https://developers.openai.com/codex/permissions)
- They don't compose with legacy settings: "Configure either `default_permissions` and `[permissions]`, or `sandbox_mode` / `sandbox_workspace_write`, but not both." If `sandbox_mode` appears in any loaded config, or `--sandbox` is passed, the legacy settings win. The exception is managed `allowed_permission_profiles`, which forces profiles — [Permissions](https://developers.openai.com/codex/permissions)
- Profile keys: `description`, `extends` (`:read-only`, `:workspace` or another named profile; `:danger-full-access` is not allowed, nor are cycles), `workspace_roots."<path>" = true`, `filesystem."<path-or-glob-or-token>" = read|write|deny` (tokens include `:minimal`, `:root`, `:workspace_roots` with nested subpaths), `filesystem.glob_scan_max_depth`, `network.enabled`, `network.domains`, `network.unix_sockets`, `network.mode = limited|full`, `network.proxy_url` (default `http://127.0.0.1:3128`), `network.socks_url` (default `http://127.0.0.1:8081`), `enable_socks5` / `enable_socks5_udp` (default true), `allow_local_binding`, `allow_upstream_proxy`, `dangerously_allow_*` — [Permissions](https://developers.openai.com/codex/permissions); [Config reference](https://developers.openai.com/codex/config-reference)
- Filesystem precedence: more specific paths override broader ones. For the same path, deny > write > read — [Permissions](https://developers.openai.com/codex/permissions)
- Profiles merge across config layers by name. For example, `/etc/codex/config.toml` and `~/.codex/config.toml` can each add `workspace_roots` to the same profile — [Permissions](https://developers.openai.com/codex/permissions)

**Network**
- Network is off by default in `workspace-write`. Turn it on with `[sandbox_workspace_write] network_access = true` — [Security](https://developers.openai.com/codex/agent-approvals-security)
- `features.network_proxy` (experimental, off by default) enforces domain rules but doesn't grant network access. Network off + proxy on: still off. Network on + proxy off: unrestricted direct access. Network on + proxy on: filtered by policy — [Security](https://developers.openai.com/codex/agent-approvals-security)
- Domain rules are allowlist-first: exact host; `*.example.com` = subdomains only; `**.example.com` = apex plus subdomains; `*` = allow-only global. Deny always wins. Local and private destinations are blocked unless `allow_local_binding = true` or an exact `localhost`/IP rule exists. Best-effort DNS-rebinding checks apply — [Security](https://developers.openai.com/codex/agent-approvals-security)
- The proxy doesn't filter web search, apps/connectors, MCP server connections, browser or Computer Use, cloud tasks, or the client's own model and auth requests — [Security](https://developers.openai.com/codex/agent-approvals-security)
- Admin `[experimental_network]` in requirements.toml can start the proxy without the user feature flag, but can't turn on network when the sandbox keeps it off — [Security](https://developers.openai.com/codex/agent-approvals-security)

**Platform implementations**
- macOS: Seatbelt via `sandbox-exec` with a profile matching the mode. A curated macOS platform policy is appended for restricted reads — [Security](https://developers.openai.com/codex/agent-approvals-security)
- Linux: `bwrap` plus `seccomp` by default. WSL2 uses the Linux sandbox. WSL1 was supported through 0.114 and is unsupported from 0.115 (the move to bwrap). Docker containers may block bwrap/seccomp; in that case use `danger-full-access` inside the container — [Security](https://developers.openai.com/codex/agent-approvals-security)
- Install `bubblewrap` on Linux/WSL2. Codex uses the first `bwrap` on `PATH` and warns at startup if it is missing. Ubuntu 25.04+ needs the `bwrap-userns-restrict` AppArmor profile — [Sandboxing](https://developers.openai.com/codex/concepts/sandboxing)
- Feature-flag status: `use_legacy_landlock` deprecated; `use_linux_sandbox_bwrap` removed (bwrap is now the only path) — Local CLI (`codex features list`)
- Windows native: `[windows] sandbox = "elevated"` (recommended) | `"unelevated"` (fallback without admin) | `"mxc"`, plus `sandbox_private_desktop` (default true). Admins can constrain this via `windows.allowed_sandbox_implementations` — [Config basics](https://developers.openai.com/codex/config-basic); [Security](https://developers.openai.com/codex/agent-approvals-security); [Config reference](https://developers.openai.com/codex/config-reference)
- Test the sandbox: `codex sandbox macos|linux|windows [--permissions-profile <name>] [--log-denials] [COMMAND]...` (aliases `seatbelt`, `landlock`; also reachable as `codex debug`) — [Security](https://developers.openai.com/codex/agent-approvals-security). Conflict: on local 0.159.2, `codex sandbox --help` shows no platform subcommands, and `codex sandbox macos --help` tried to exec `macos` under sandbox-exec. `codex debug` lists only `models`, `app-server` and `prompt-input` — Local CLI

**Rules / execpolicy (experimental)**
- Purpose: control which commands Codex can run outside the sandbox. Rules are experimental — [Rules](https://developers.openai.com/codex/rules)
- Location: `rules/*.rules` next to each active config layer, e.g. `~/.codex/rules/default.rules`. Project `<repo>/.codex/rules/` loads only if trusted. Choosing "allow" in the TUI writes to `~/.codex/rules/default.rules`. Smart approvals (default) may propose a `prefix_rule` during escalation — [Rules](https://developers.openai.com/codex/rules)
- Format: Starlark. `prefix_rule(pattern=[...], decision="allow"|"prompt"|"forbidden", justification="...", match=[...], not_match=[...])`. `pattern` elements are literals or unions (`["view","list"]`). `decision` defaults to `allow`. With several matches, the most restrictive wins (forbidden > prompt > allow). `match`/`not_match` are inline tests checked at load — [Rules](https://developers.openai.com/codex/rules)
- Shell wrappers: `bash|zsh|sh -c/-lc` scripts made only of plain words joined by `&& || ; |` are split with tree-sitter, and each command is evaluated. Scripts with redirection, substitution, variables, globs or control flow are evaluated as one invocation — [Rules](https://developers.openai.com/codex/rules)
- Testing: `codex execpolicy check --pretty --rules <file> -- <cmd...>` prints JSON — [Rules](https://developers.openai.com/codex/rules); command present locally — Local CLI (`codex execpolicy --help`)
- Admin rules: in requirements.toml, `[rules] prefix_rules = [{ pattern = [{ token = "rm" }], decision = "forbidden", justification = "..." }]` with `token` or `any_of`. Only `prompt` or `forbidden` are allowed. These merge with `.rules` files, and the most restrictive wins — [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration); [Config reference](https://developers.openai.com/codex/config-reference)

**Minimal examples**
```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"
[sandbox_workspace_write]
network_access = true
```
```toml
default_permissions = "project-edit"
[features]
network_proxy = true
[permissions.project-edit]
extends = ":workspace"
[permissions.project-edit.filesystem.":workspace_roots"]
"**/*.env" = "deny"
[permissions.project-edit.network]
enabled = true
[permissions.project-edit.network.domains]
"api.openai.com" = "allow"
```
```python
# ~/.codex/rules/default.rules
prefix_rule(pattern=["gh", "pr", "view"], decision="prompt", justification="Viewing PRs is allowed with approval")
```
— [Advanced config](https://developers.openai.com/codex/config-advanced); [Permissions](https://developers.openai.com/codex/permissions); [Rules](https://developers.openai.com/codex/rules)

### Inferences
- The task brief lists approval policies "untrusted, on-request, on-failure, never". That is outdated for current Codex: only `on-request`, `never` and `granular` are valid. `untrusted` survives only as a project trust level, and `on-failure` is deprecated.
- Permission profiles look like the intended successor to `sandbox_mode`. Enterprise docs say "use permission profiles ... instead of building new deployments around legacy sandbox-mode restrictions" ([Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)), but user-facing docs still teach `sandbox_mode` first.
- The `.git`/`.codex`/`.agents` protection explains why `git commit` and edits to `.codex/` often trigger approval even in workspace-write.

### Gaps
- No release date was found for the retirement of `approval_policy = "untrusted"` or the deprecation of `on-failure`. The changelog page fetched shows recent releases only.
- The exact default when neither `sandbox_mode` nor `default_permissions` is set is described differently: "read-only (default)" in the sample config vs VCS-detected `Auto` in the security page.
- Discrepancy between the `codex sandbox <platform>` docs and the local 0.159.2 CLI help is unresolved.

---

## 4. MCP: `[mcp_servers]`, stdio / streamable HTTP, `codex mcp`, tool allow/deny, timeouts, OAuth; Codex as an MCP server

### Takeaway
External MCP servers are defined in `[mcp_servers.<name>]` tables in user or (trusted) project config.toml, shared by the CLI, IDE extension and desktop app. Servers are stdio (`command`/`args`/`env`) or streamable HTTP (`url` with bearer, headers, header helper, or OAuth including CIMD/DCR). Per-server settings cover tool allow/deny lists, per-tool approval modes and output limits, a startup timeout (10 s) and a tool timeout (60 s). Hosting Codex *as* an MCP server (`codex mcp-server`) was deprecated on 2026-08-24 and removed on 2026-09-05. The replacement is the experimental app-server JSON-RPC protocol.

### Cited Findings
**Config and transports**
- Configuration lives in `config.toml` (`~/.codex/config.toml` or project `.codex/config.toml`, trusted only). The desktop app, CLI and IDE extension share it — [MCP](https://developers.openai.com/codex/mcp)
- Supported: stdio servers, env vars, streamable HTTP, bearer token auth, OAuth (including CIMD and DCR), ChatGPT session auth for trusted first-party servers, and server `instructions` (Codex reads them; keep the first 512 characters self-contained) — [MCP](https://developers.openai.com/codex/mcp)
- stdio keys: `command` (required), `args`, `env` (map), `env_vars` (allowlist; strings or `{ name, source = "local"|"remote" }`), `cwd`, `experimental_environment = local|remote` — [MCP](https://developers.openai.com/codex/mcp); [Config reference](https://developers.openai.com/codex/config-reference)
- HTTP keys: `url` (required), `auth = oauth (default) | chatgpt`, `bearer_token_env_var`, `http_headers`, `env_http_headers`, `http_headers_helper` (a local command that prints JSON headers; refreshed once on a 401/403; explicit bearer or OAuth wins over the helper's Authorization header), `scopes`, `oauth_resource` (RFC 8707), `[mcp_servers.<id>.oauth] client_id / callback_url / callback_port`. With no credentials Codex connects unauthenticated — [MCP](https://developers.openai.com/codex/mcp); [Config reference](https://developers.openai.com/codex/config-reference)
- Common keys: `startup_timeout_sec` (default 10; alias `startup_timeout_ms`), `tool_timeout_sec` (default 60), `enabled`, `required` (fail startup/resume if the server can't initialize), `enabled_tools` (allowlist), `disabled_tools` (denylist applied after the allowlist), `default_tools_approval_mode = auto|prompt|writes|approve` (`writes` prompts for tools not marked read-only), `tools.<tool>.approval_mode`, `tools.<tool>.output_token_limit` — [MCP](https://developers.openai.com/codex/mcp); [Config reference](https://developers.openai.com/codex/config-reference)
- Global keys: `mcp_optional_startup_grace_ms` (default 1000; `0` waits each server's full startup timeout), `mcp_oauth_callback_port`, `mcp_oauth_callback_url`, `mcp_oauth_credentials_store = auto|file|keyring` — [MCP](https://developers.openai.com/codex/mcp); [Config reference](https://developers.openai.com/codex/config-reference)
- OAuth details: Codex prefers CIMD when the auth server advertises `client_id_metadata_document_supported` and supports `none` token auth, otherwise DCR. A configured client ID skips registration. It uses ChatGPT-hosted CIMD documents (`https://chatgpt.com/oauth/codex/client.json` or a per-server variant). It validates `iss`. It prefers server-advertised `scopes_supported` over configured scopes. Loopback `http://127.0.0.1` callbacks get the active port inserted (RFC 8252) — [MCP](https://developers.openai.com/codex/mcp)

**CLI**
- `codex mcp list [--json] | get | add | remove | login | logout` — Local CLI (`codex mcp --help`)
- `codex mcp add <NAME> (--url <URL> | -- <COMMAND>...)` with `--env KEY=VALUE` (stdio only), `--bearer-token-env-var` (HTTP only), `--oauth-client-id`, `--oauth-client-secret`, `--oauth-client-registration auto|cimd|dcr`, `--oauth-resource` — Local CLI (`codex mcp add --help`)
- `codex mcp login <NAME> [--scopes a,b] [--no-browser] [--oauth-client-registration ...]`. Registration choice applies only to that login and isn't stored — Local CLI; [MCP](https://developers.openai.com/codex/mcp)
- TUI `/mcp` lists active servers (`/mcp verbose` for details). The IDE extension and desktop app have Settings > MCP servers UIs — [MCP](https://developers.openai.com/codex/mcp); [CLI reference](https://developers.openai.com/codex/cli/reference)

**Plugin-bundled MCP servers**
- Plugins ship servers in their manifest/`mcp.json`. Users can't set transport, but can control `plugins."<plugin>@<marketplace>".mcp_servers.<server>.enabled / enabled_tools / disabled_tools / default_tools_approval_mode / tools.<t>.approval_mode`. Plugin `.mcp.json` OAuth uses camelCase `clientId`, `callbackUrl`, `callbackPort` — [MCP](https://developers.openai.com/codex/mcp); [Config reference](https://developers.openai.com/codex/config-reference)

**Admin control**
- requirements.toml `[mcp_servers.<id>] identity = { command = "..." }` or `{ url = "..." }`. Structured matchers (`executable` + ordered `args` with `exact|prefix|regex`; URL `exact|prefix|regex`) are available. Both name and identity must match, or the server is disabled. An empty `mcp_servers` table disables all servers. The same shapes apply under `plugins.<p>.mcp_servers.<s>` — [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration); [Config reference](https://developers.openai.com/codex/config-reference)
- The network proxy doesn't filter MCP server connections. Use the `mcp_servers` allowlist instead — [Security](https://developers.openai.com/codex/agent-approvals-security)

**Codex as an MCP server: removed**
- "The `codex mcp-server` command and the standalone `codex-mcp-server` binary have been removed." Use the Codex app server, a separate JSON-RPC protocol that is not MCP. The app-server is experimental and not supported for production — [Agents SDK guide](https://developers.openai.com/codex/guides/agents-sdk); [CLI reference](https://developers.openai.com/codex/cli/reference)
- Timeline: deprecated 2026-08-24, removed 2026-09-05 — [Changelog](https://developers.openai.com/codex/changelog)
- Locally, `codex mcp-server` isn't a subcommand (the top-level help lists none). `codex app-server` offers `daemon`, `proxy`, `generate-ts` and `generate-json-schema` — Local CLI

**Minimal example**
```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
enabled_tools = ["get_file"]
tool_timeout_sec = 45
```
CLI equivalent: `codex mcp add context7 -- npx -y @upstash/context7-mcp` — [MCP](https://developers.openai.com/codex/mcp)

### Inferences
- Any integration (for example the Agents SDK `MCPServerStdio("codex mcp-server")` pattern) built before September 2026 breaks on current releases.
- A trusted repo can ship `.codex/config.toml` with `[mcp_servers]`, so trust is effectively the gate for repo-supplied MCP servers.

### Gaps
- Merge semantics when the same `mcp_servers.<id>` is defined in both user and project config (whole-table replacement vs per-key merge) aren't documented.
- Exact `codex mcp get` / `logout` flags weren't captured. They exist per `codex mcp --help`.

---

## 5. Plugins / marketplaces / apps (connectors), and models / custom model providers

### Takeaway
Codex has a full plugin system shared with ChatGPT. A plugin bundles skills, MCP servers, hooks, assets and optionally apps. It is distributed via marketplaces: the universal OpenAI directory, plus Git or local marketplaces added with `codex plugin marketplace add`, repo `.agents/plugins/marketplace.json`, or personal `~/.agents/plugins/marketplace.json`. Installed copies are cached in `~/.codex/plugins/cache/...`, and per-plugin enablement lives in config.toml (`[plugins."name@marketplace"]`). Apps/connectors have their own `[apps]` table. Models are chosen with `model` and `-m` / `/model`. Providers default to built-in `openai`. Custom providers go in `[model_providers.<id>]` and support only `wire_api = "responses"`. Built-ins `openai`, `ollama`, `lmstudio` and `amazon-bedrock` are reserved or special.

### Cited Findings
**Plugins**
- Plugins can contain skills, MCP servers, browser extensions and hooks. ChatGPT and Codex share one universal plugin directory. Plugins work in the CLI (plugin browser) and in Codex in the desktop app, but the IDE extension doesn't support plugins — [Plugins](https://developers.openai.com/codex/plugins)
- CLI: `/plugins` opens the plugin browser, grouped by marketplace. Space toggles an installed plugin. Start a new session after installing to use bundled skills and tools — [Plugins](https://developers.openai.com/codex/plugins)
- CLI commands: `codex plugin add <PLUGIN[@MARKETPLACE]> [-m MARKETPLACE] [--json]`, `codex plugin list [-m] [--json] [--available]`, `codex plugin remove <PLUGIN[@MARKETPLACE]>`, `codex plugin marketplace add <SOURCE> [--ref REF] [--sparse PATH]... [--json]` (SOURCE is a local path, `owner/repo[@ref]`, HTTPS Git URL or SSH Git URL), `codex plugin marketplace list | upgrade [name] | remove <name>` — Local CLI (`codex plugin ... --help`)
- Plugin layout: portable root `plugin.json` (schema `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`; kebab-case `name`, `version`, `description`, author and so on), `skills/<name>/SKILL.md`, `mcp.json`, `hooks/`, `assets/`. OpenAI-specific settings go under `extensions.com.openai`. The older `.codex-plugin/plugin.json` remains a supported compatibility fallback — [Build plugins](https://developers.openai.com/codex/plugins/build)
- Marketplace file: JSON with `name`, `interface.displayName` and `plugins[]`. Each entry has `name`, `source` (`{source:"local", path:"./..."}` or a string path; `{source:"url"|"git-subdir", url, path, ref|sha}`; `{source:"npm", package, version, registry}`), plus required `policy.installation` (`AVAILABLE|INSTALLED_BY_DEFAULT|NOT_AVAILABLE`), `policy.authentication` (e.g. `ON_INSTALL`) and `category`. Unresolvable entries are skipped — [Build plugins](https://developers.openai.com/codex/plugins/build)
- Marketplace file locations: repo `$REPO_ROOT/.agents/plugins/marketplace.json`, legacy-compatible `$REPO_ROOT/.claude-plugin/marketplace.json`, personal `~/.agents/plugins/marketplace.json`. Installs go to `~/.codex/plugins/cache/$MARKETPLACE/$PLUGIN/$VERSION/` (`local` for local plugins), and Codex loads from the cache — [Build plugins](https://developers.openai.com/codex/plugins/build)
- config.toml: `[marketplaces.<name>] source_type = git|local, source, ref, sparse_paths`. Marketplaces can be defined in system, cloud-managed, user or trusted-project config. `[plugins."plugin@marketplace"] enabled = bool` is read from the merged config, and trusted-project settings override user, cloud and system — [Config reference](https://developers.openai.com/codex/config-reference); [Build plugins](https://developers.openai.com/codex/plugins/build). The local `~/.codex/config.toml` has `[marketplaces.<name>] source_type/source` and `[plugins."frank@franks-ai-skills"] enabled` — Local CLI (redacted inspection)
- Admin: `features.plugins = false` disables plugins (applies to API-key sign-in too). `[marketplaces] restrict_to_allowed_sources = true` with `allowed_sources.<rule>` (`source = git` + `url`/`ref`, `host_pattern`, or `local` + absolute `path`). The OpenAI-curated catalog `https://github.com/openai/plugins.git` must be allowlisted explicitly — [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)
- Related flags (local): `plugins`, `remote_plugin`, `plugin_sharing` stable/on. `recommended_plugins` stable/off. `plugin_hooks` removed — Local CLI (`codex features list`)

**Apps / connectors**
- `features.apps` (stable, on) enables app (connector) integrations. App traffic isn't governed by the command network proxy — [Config reference](https://developers.openai.com/codex/config-reference)
- `[apps._default]` and `[apps.<id>]` accept `enabled`, `destructive_enabled`, `open_world_enabled`, `default_tools_enabled`, `default_tools_approval_mode = auto|prompt|writes|approve`, `approvals_reviewer`, and `tools.<tool>.enabled / approval_mode`. requirements.toml `apps.<id>.enabled = false` and per-tool `approval_mode` constrain these — [Config reference](https://developers.openai.com/codex/config-reference)
- `tool_suggest.discoverables` / `disabled_tools` (entries `type = "connector"|"plugin"`, `id`) control tool suggestions — [Config reference](https://developers.openai.com/codex/config-reference)

**Models**
- Choose with `model` in config, `-m/--model`, or `/model` in the TUI (which also adjusts reasoning effort) — [Models](https://developers.openai.com/codex/models)
- Current recommendations: GPT-6.1 Sol (`gpt-6.1-sol`) for complex work and `gpt-6-luna` for focused tasks. `gpt-6-astra` is the most capable. GPT-5.6 Sol/Terra/Luna remain available during rollout — [Models](https://developers.openai.com/codex/models)
- Deprecation: GPT-5.5 retires from ChatGPT, Work and Codex on 2026-10-14 on all plans (the API is unaffected). Replace `gpt-5.5` in configs and managed defaults with `gpt-6-sol` (paid) or `gpt-6-luna` (Free/Go) — [Models](https://developers.openai.com/codex/models); [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)
- `codex debug models` renders the raw model catalog as JSON. `model_catalog_json` points at a custom catalog. Admins can set `[models.new_thread] model / model_reasoning_effort / service_tier` as defaults (ignored when the user overrides explicitly) — Local CLI (`codex debug --help`); [Config reference](https://developers.openai.com/codex/config-reference)

**Model providers**
- `model_provider` defaults to `openai`. To point the built-in OpenAI provider at a proxy or data-residency endpoint, use `openai_base_url` instead of defining `[model_providers.openai]`; built-in IDs `openai`, `ollama` and `lmstudio` are reserved — [Advanced config](https://developers.openai.com/codex/config-advanced); [Config reference](https://developers.openai.com/codex/config-reference)
- `[model_providers.<id>]` keys: `name`, `base_url`, `env_key`, `env_key_instructions`, `experimental_bearer_token` (discouraged), `requires_openai_auth` (default false), `http_headers`, `env_http_headers`, `query_params`, `wire_api` (only `responses`, the default), `request_max_retries` (default 4), `stream_max_retries` (default 5), `stream_idle_timeout_ms` (default 300000), `supports_websockets`, `supports_standalone_web_search` (default false), and `[auth]` (`command`, `args`, `cwd`, `timeout_ms` default 5000, `refresh_interval_ms` default 300000; can't be combined with `env_key`, `experimental_bearer_token` or `requires_openai_auth`) — [Config reference](https://developers.openai.com/codex/config-reference); [Advanced config](https://developers.openai.com/codex/config-advanced)
- Built-in `amazon-bedrock` provider: only `[model_providers.amazon-bedrock.aws] profile, region` can be overridden. Without a profile it uses the standard AWS credential chain — [Advanced config](https://developers.openai.com/codex/config-advanced)
- OSS mode: `--oss` with `--local-provider ollama|lmstudio`, or `oss_provider` in config. If neither is set, the TUI prompts and `codex exec` errors — [Advanced config](https://developers.openai.com/codex/config-advanced)
- Provider keys are user-level only (ignored in project config). Admins can enforce `model_provider` / `model_providers` via requirements, which replace whole providers per ID — [Advanced config](https://developers.openai.com/codex/config-advanced); [Config reference](https://developers.openai.com/codex/config-reference)
- Change: `wire_api` accepts only `responses` — [Config reference](https://developers.openai.com/codex/config-reference); [Advanced config](https://developers.openai.com/codex/config-advanced)

**Minimal examples**
```toml
model = "gpt-6.1-sol"
model_provider = "proxy"
[model_providers.proxy]
name = "OpenAI via LLM proxy"
base_url = "https://proxy.example.com/v1"
env_key = "OPENAI_API_KEY"
wire_api = "responses"

[plugins."my-plugin@local-repo"]
enabled = true
```
`codex plugin marketplace add owner/repo --ref main && codex plugin add my-plugin@owner-marketplace`
— [Advanced config](https://developers.openai.com/codex/config-advanced); [Build plugins](https://developers.openai.com/codex/plugins/build); Local CLI

### Inferences
- Codex reads `.claude-plugin/marketplace.json` as a legacy-compatible source and plugin manifests follow the cross-vendor "Agent Plugins" schema. That makes one repo marketplace potentially usable by both Claude Code and Codex, which matters for a shared skills repo.
- Because project `.codex/config.toml` can enable plugins and define marketplaces, plugin activation (like MCP) is gated by project trust.

### Gaps
- Exact `policy.authentication` values beyond `ON_INSTALL` (the docs mention "on install or first use") weren't captured.
- No documented hard limits (plugin count, plugin size, number of MCP servers).
- `[apps]` IDs and how to discover them aren't covered in the fetched pages.
- Whether Chat Completions (`wire_api = "chat"`) support was formally removed, and when, wasn't found in the changelog excerpt fetched.
