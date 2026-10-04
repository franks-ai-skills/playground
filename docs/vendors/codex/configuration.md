# Configuration (config.toml)

Codex reads its settings from layered TOML files named `config.toml`. One config system is shared by the CLI, the IDE extension and Codex in the ChatGPT desktop app ([Config basics](https://developers.openai.com/codex/config-basic)). It sets the model and provider, approvals and sandboxing, MCP servers, plugins, feature flags and UI behavior, and admins constrain it with a separate `requirements.toml`.

## Locations and scopes

### Config layers (values)

Resolution order, highest precedence first ([Config basics](https://developers.openai.com/codex/config-basic)):

| # | Layer | Path | Notes |
|---|---|---|---|
| 1 | CLI flags and `-c/--config` overrides | command line | Dedicated flags (`--model` and so on) are preferred over `-c` when they exist ([Advanced config](https://developers.openai.com/codex/config-advanced)) |
| 2 | Project config | `.codex/config.toml` in every directory from the project root down to the cwd | Trusted projects only. When files set the same key, the one closest to the cwd wins ([Advanced config](https://developers.openai.com/codex/config-advanced)) |
| 3 | Profile file | `~/.codex/<profile>.config.toml`, selected with `--profile` | See Profiles below |
| 4 | User config | `~/.codex/config.toml` (`$CODEX_HOME/config.toml`) | |
| 5 | Cloud-managed defaults | `config.toml` defaults for the signed-in workspace | Users can override them |
| 6 | System config | `/etc/codex/config.toml` (Unix) | Users can override it |
| 7 | Built-in defaults | | |

Two admin layers sit outside this stack (see Managed configuration below):

- **`requirements.toml`** holds constraints that users cannot override.
- **Legacy `managed_config.toml`** and macOS MDM `config_toml_base64` hold defaults that are reapplied at every client start and override even CLI `-c` overrides ([Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)).

### Codex home

`CODEX_HOME` defaults to `~/.codex`. It holds `config.toml`, `auth.json` (when file-based credential storage is used; otherwise credentials go to the OS keychain), `history.jsonl`, logs and caches ([Advanced config](https://developers.openai.com/codex/config-advanced)). It also holds the global `AGENTS.md` ([instructions.md](instructions.md)), `rules/`, `hooks.json`, `agents/`, profile files and the plugin cache.

### Project trust

- Trust is stored in the user config as `[projects."<absolute path>"] trust_level = "trusted" | "untrusted"` ([Config reference](https://developers.openai.com/codex/config-reference)). A local `~/.codex/config.toml` has exactly this shape (local CLI, redacted inspection).
- If a project is untrusted, Codex skips the project `.codex/` layers: project-local config, hooks and rules. User and system layers still load ([Config basics](https://developers.openai.com/codex/config-basic); [Advanced config](https://developers.openai.com/codex/config-advanced)).
- `trust_level = "untrusted"` is also the current way to get stricter "ask for everything" approvals; see [permissions-and-sandbox.md](permissions-and-sandbox.md).
- Inference: because trusted project config can define `[mcp_servers]`, `[marketplaces]` and `[plugins]`, project trust is effectively the gate for repository-supplied MCP servers and plugins.

### Keys that project config cannot set

Codex ignores these keys in project `.codex/config.toml` and prints a startup warning: `openai_base_url`, `chatgpt_base_url`, `apps_mcp_product_sku`, `model_provider`, `model_providers`, `notify`, `profile`, `profiles`, `experimental_realtime_ws_base_url`, `otel` ([Advanced config](https://developers.openai.com/codex/config-advanced); [Config reference](https://developers.openai.com/codex/config-reference)).

### Profiles (file-based since 0.134.0)

- `--profile <name>` (`-p`) loads `~/.codex/config.toml` and then overlays `~/.codex/<name>.config.toml`. Names can use letters, numbers, hyphens and underscores. Keys in the profile file are top-level, not nested under `[profiles.<name>]` ([Advanced config](https://developers.openai.com/codex/config-advanced)).
- CLI help: `-p, --profile <CONFIG_PROFILE_V2>  Layer $CODEX_HOME/<name>.config.toml on top of the base user config` (local CLI, `codex --help`, 0.159.2).
- A profile file can override `model_catalog_json` ([Advanced config](https://developers.openai.com/codex/config-advanced)).
- Inference: profile files sit below project config, so a trusted repository's `.codex/config.toml` beats `--profile` for every key it sets, except the user-only keys listed above.

## Format

TOML. Dotted tables (`[sandbox_workspace_write]`, `[mcp_servers.<id>]`, `[projects."<path>"]`) group related keys.

### CLI overrides and global flags

| Flag | Effect |
|---|---|
| `-c/--config key=value` | Sets any key. Dotted paths set nested values. The value is parsed as TOML; if that fails, it is used as a literal string. Examples: `-c model="o3"`, `-c shell_environment_policy.inherit=all` (local CLI, `codex --help`); `--config model='"gpt-6.1-sol"'`, `--config sandbox_workspace_write.network_access=true`, `-c mcp_servers.context7.enabled=false` ([Advanced config](https://developers.openai.com/codex/config-advanced)) |
| `--enable <FEATURE>` / `--disable <FEATURE>` | Same as `-c features.<name>=true|false` (local CLI) |
| `-p/--profile <name>` | Overlay `~/.codex/<name>.config.toml` |
| `--strict-config` | Errors on `config.toml` fields this version does not recognize. Supported on `codex`, `exec`, `review`, `resume`, `fork`, `app-server`, `exec-server` ([CLI reference](https://developers.openai.com/codex/cli/reference)) |
| `codex exec --ignore-user-config` | Does not load `$CODEX_HOME/config.toml`; auth still uses `CODEX_HOME` ([CLI reference](https://developers.openai.com/codex/cli/reference)) |
| `codex exec --ignore-rules` | Skips user and project `.rules` files ([CLI reference](https://developers.openai.com/codex/cli/reference)) |
| Other global flags | `-m/--model`, `--oss`, `--local-provider lmstudio|ollama`, `-s/--sandbox`, `-a/--ask-for-approval`, `--add-dir`, `-C/--cd`, `--search`, `--worktree`, `--approve-for-me`, `--dangerously-bypass-approvals-and-sandbox`, `--dangerously-bypass-hook-trust` (local CLI, `codex --help`) |

### Model keys

| Key | Meaning / values | Default |
|---|---|---|
| `model` | Model ID, for example `gpt-6.1-sol` | |
| `model_provider` | Provider ID from `model_providers` | `openai` |
| `model_reasoning_effort` | Levels the model advertises, for example `low|medium|high|xhigh|max|ultra` | |
| `plan_mode_reasoning_effort` | Reasoning-effort override for Plan mode | |
| `model_reasoning_summary` | `auto|concise|detailed|none` | |
| `model_verbosity` | `low|medium|high`; Responses API only | |
| `model_context_window` | Context window size | |
| `model_auto_compact_token_limit` | Token count that triggers automatic compaction | |
| `model_auto_compact_token_limit_scope` | `total` or `body_after_prefix` | `total` |
| `model_supports_reasoning_summaries` | Whether the model supports reasoning summaries | |
| `model_catalog_json` | Path to a custom model catalog | |
| `review_model` | Model used by `/review` | session model |
| `service_tier` | `fast` maps to the request value `priority` | |
| `personality` | `none|friendly|pragmatic` | |

Sources: [Config reference](https://developers.openai.com/codex/config-reference); [Advanced config](https://developers.openai.com/codex/config-advanced).

### Approval, sandbox and instruction keys

`approval_policy`, `approvals_reviewer`, `sandbox_mode`, `[sandbox_workspace_write]`, `default_permissions`, `[permissions.*]` and `allow_login_shell` (default `true`) are described in [permissions-and-sandbox.md](permissions-and-sandbox.md) ([Config reference](https://developers.openai.com/codex/config-reference)). Instruction keys (`project_doc_*`, `model_instructions_file`, `developer_instructions`) are in [instructions.md](instructions.md).

### `[shell_environment_policy]`

Controls which environment variables reach commands Codex runs ([Advanced config](https://developers.openai.com/codex/config-advanced); [Config basics](https://developers.openai.com/codex/config-basic); [Config reference](https://developers.openai.com/codex/config-reference)).

| Key | Meaning | Default |
|---|---|---|
| `inherit` | `all`, `core` or `none` | |
| `set` | Map of variables to set; applied after exclusions | |
| `filters` | Case-insensitive glob map of `include` or `exclude`; the canonical form | |
| `ignore_default_excludes` | `true` means names containing KEY, SECRET or TOKEN are NOT removed automatically; set `false` to exclude them | `true` |
| `exclude`, `include_only` | Legacy arrays; still work, but cannot be combined with `filters` in the same layer | |
| `experimental_use_profile` | Experimental | |

Processing order: automatic exclusions, then custom exclusions, then `set`, then the include allowlist. Filter keys merge case-insensitively across layers.

### `[tui]`

| Key | Meaning | Default |
|---|---|---|
| `notifications` | Bool, or a list of event types | |
| `notification_method` | `auto`, `osc9` or `bel` | `auto` |
| `notification_condition` | `unfocused` or `always` | `unfocused` |
| `animations` | Bool | `true` |
| `alternate_screen` | `auto`, `always` or `never` | `auto` |
| `show_tooltips` | Bool | `true` |
| `theme` | UI theme | |
| `keymap.<context>.<action>` | Key bindings. Contexts: `global`, `chat`, `composer`, `editor`, `vim_normal`, `vim_operator`, `vim_text_object`, `pager`, `list`, `approval`. `[]` unbinds | |
| `raw_output_mode` | Raw output mode | |
| `resume_cwd` | `current` or `session` | |
| `status_line` | Status line items | |
| `terminal_title` | Title items | `["spinner","project"]` |
| `vim_mode_default` | Start in vim mode | |

Sources: [Config reference](https://developers.openai.com/codex/config-reference); [Advanced config](https://developers.openai.com/codex/config-advanced). Notifications are covered in [hooks.md](hooks.md).

### Other tables

| Table / key | Meaning | Default |
|---|---|---|
| `[history] persistence` | `save-all` or `none` | |
| `[history] max_bytes` | Caps `history.jsonl` by dropping the oldest entries | |
| `[otel] environment` | Environment label | `dev` |
| `[otel] exporter` | `none`, `otlp-http` or `otlp-grpc`; table form with `endpoint`, `headers`, `protocol = binary|json`, `tls.*` | off |
| `[otel] trace_exporter`, `metrics_exporter` | Trace and metrics exporters | `metrics_exporter = statsig` |
| `[otel] log_user_prompt` | Log user prompts | `false` (redacted) |
| `[analytics] enabled` | `false` turns off anonymous usage metrics | |
| `[feedback] enabled` | `false` turns off `/feedback` | |
| `web_search` | `disabled`, `cached`, `indexed` or `live`. `live` under `--yolo` / full access. `--search` equals `live` | `cached` |
| `tools.web_search` | Object form: `context_size`, `allowed_domains`, `location` | |
| `notify` | External program run on `agent-turn-complete`; user config only. See [hooks.md](hooks.md) | |
| `[features]` | Boolean feature flags, see below | |
| `[mcp_servers.<id>]` | MCP servers, see [mcp.md](mcp.md) | |
| `[marketplaces.<name>]`, `[plugins."<p>@<m>"]`, `[apps.*]` | Plugins and connectors, see [plugins.md](plugins.md) | |
| `[agents]` | Multi-agent settings, see [subagents.md](subagents.md) | |
| `[hooks]` | Inline hooks, see [hooks.md](hooks.md) | |
| `skills.config[]`, `skills.max_context_tokens` | Skill enablement and catalog budget (2% of the context window, capped at 10000), see [skills.md](skills.md) | |
| `[memories]` | Memories settings | |
| `[desktop.custom_file_handlers.<id>]` | Desktop app only, user level | |
| `[windows] sandbox` | Windows sandbox implementation, see [permissions-and-sandbox.md](permissions-and-sandbox.md) | |
| `notice.*` | Acknowledgement tracking | |
| `file_opener` | `vscode`, `vscode-insiders`, `windsurf`, `cursor` or `none` | `vscode` |
| `log_dir` | Log directory; setting it explicitly enables `codex-tui.log` | `$CODEX_HOME/log` |
| `sqlite_home` | SQLite state location | |
| `cli_auth_credentials_store` | `file`, `keyring`, `auto` or `ephemeral` | `file` (per sample config) |
| `forced_login_method` | `chatgpt` or `api` | |
| `forced_chatgpt_workspace_id` | Pin a ChatGPT workspace | |
| `check_for_update_on_startup` | Update check | |
| `hide_agent_reasoning`, `show_raw_agent_reasoning` | Reasoning display | |
| `tool_output_token_limit` | Tool output limit | |
| `background_terminal_max_timeout` | Replaces `background_terminal_timeout` | `300000` ms |
| `oss_provider` | `ollama` or `lmstudio` for `--oss` | |
| `tool_suggest.discoverables`, `tool_suggest.disabled_tools` | Tool suggestions, see [plugins.md](plugins.md) | |

Sources: [Config reference](https://developers.openai.com/codex/config-reference); [Sample config](https://developers.openai.com/codex/config-sample); [Advanced config](https://developers.openai.com/codex/config-advanced); [Config basics](https://developers.openai.com/codex/config-basic); [Security](https://developers.openai.com/codex/agent-approvals-security) (OTel off by default).

### Feature flags (`[features]`)

Documented common flags ([Config basics](https://developers.openai.com/codex/config-basic); [Config reference](https://developers.openai.com/codex/config-reference)), compared with local `codex features list` on 0.159.2 where the notes record it:

| Flag | Documented default / maturity | Local 0.159.2 | Purpose |
|---|---|---|---|
| `apps` | true, stable | | App (connector) integrations |
| `goals` | true | stable, on | Persisted goals and automatic continuation (`/goal`) |
| `hooks` | true | stable, true | Lifecycle hooks; `codex_hooks` is a deprecated alias |
| `fast_mode` | true | | |
| `memories` | false, experimental | stable, false | |
| `multi_agent` | true, stable | stable, true | Subagent tools |
| `multi_agent_v2` | | stable, false | Not documented |
| `personality` | true, stable | removed, false | |
| `remote_plugin` | true | stable, on | |
| `plugins` | | stable, on | `false` disables plugins |
| `plugin_sharing` | | stable, on | |
| `recommended_plugins` | | stable, off | |
| `shell_snapshot` | true | | |
| `shell_tool` | true | | |
| `unified_exec` | true except on Windows | | Replaces legacy `experimental_use_unified_exec_tool` |
| `worktrees` | | stable, on | |
| `skill_mcp_dependency_install`, `skill_search` | | stable, on | Skills |
| `skip_host_skill_discovery` | | under development, off | Skills |
| `agent_message_board` | | under development, false | |
| `network_proxy` | experimental, off | | Domain-filtering proxy |
| `prevent_idle_sleep` | experimental, off | | |
| `web_search`, `web_search_cached`, `web_search_request` | deprecated | `web_search_cached`, `web_search_request` deprecated | Replaced by top-level `web_search` |
| `use_legacy_landlock`, `transcript_v2` | | deprecated | |
| `use_linux_sandbox_bwrap`, `experimental_windows_sandbox`, `elevated_windows_sandbox`, `js_repl`, `plugin_hooks`, `multi_agent_mode`, `enable_fanout`, `skill_env_var_dependency_prompt` | | removed | |

`codex features list` prints each flag's stage and effective state. `codex features enable|disable <name>` writes to `config.toml` (local CLI, `codex features --help`).

### Models

- Choose a model with `model` in config, `-m/--model`, or `/model` in the TUI, which also adjusts reasoning effort ([Models](https://developers.openai.com/codex/models)).
- Recommendations at research time: GPT-6.1 Sol (`gpt-6.1-sol`) for complex work, `gpt-6-luna` for focused tasks, `gpt-6-astra` as the most capable. GPT-5.6 Sol/Terra/Luna remain available during rollout ([Models](https://developers.openai.com/codex/models)).
- `codex debug models` prints the raw model catalog as JSON (local CLI). `model_catalog_json` points at a custom catalog ([Config reference](https://developers.openai.com/codex/config-reference)).
- Admins can set `[models.new_thread] model / model_reasoning_effort / service_tier` in `requirements.toml` as defaults; they are ignored when the user overrides them explicitly ([Config reference](https://developers.openai.com/codex/config-reference)).

### Model providers

`model_provider` defaults to `openai`. To point the built-in OpenAI provider at a proxy or data-residency endpoint, set `openai_base_url` instead of defining `[model_providers.openai]`. The built-in IDs `openai`, `ollama` and `lmstudio` are reserved ([Advanced config](https://developers.openai.com/codex/config-advanced); [Config reference](https://developers.openai.com/codex/config-reference)).

`[model_providers.<id>]` keys ([Config reference](https://developers.openai.com/codex/config-reference); [Advanced config](https://developers.openai.com/codex/config-advanced)):

| Key | Meaning | Default |
|---|---|---|
| `name` | Display name | |
| `base_url` | API base URL | |
| `env_key` | Environment variable that holds the API key | |
| `env_key_instructions` | Help text for setting the key | |
| `experimental_bearer_token` | Inline bearer token (discouraged) | |
| `requires_openai_auth` | Use OpenAI auth | `false` |
| `http_headers`, `env_http_headers` | Static headers and headers read from environment variables | |
| `query_params` | Extra query parameters | |
| `wire_api` | Only `responses` is accepted | `responses` |
| `request_max_retries` | Request retries | `4` |
| `stream_max_retries` | Stream retries | `5` |
| `stream_idle_timeout_ms` | Stream idle timeout | `300000` |
| `supports_websockets` | WebSocket support | |
| `supports_standalone_web_search` | Standalone web search support | `false` |
| `[auth]` `command`, `args`, `cwd` | Command that produces credentials | |
| `[auth]` `timeout_ms` | Command timeout | `5000` |
| `[auth]` `refresh_interval_ms` | Refresh interval | `300000` |

`[auth]` cannot be combined with `env_key`, `experimental_bearer_token` or `requires_openai_auth`.

- **Amazon Bedrock.** The built-in `amazon-bedrock` provider allows overriding only `[model_providers.amazon-bedrock.aws] profile, region`. Without a profile it uses the standard AWS credential chain ([Advanced config](https://developers.openai.com/codex/config-advanced)).
- **OSS mode.** `--oss` with `--local-provider ollama|lmstudio`, or `oss_provider` in config. If neither is set, the TUI prompts and `codex exec` errors ([Advanced config](https://developers.openai.com/codex/config-advanced)).
- **Scope.** Provider keys are user-level only; project config ignores them. Admins can enforce `model_provider` / `model_providers` through requirements, which replace whole providers per ID ([Advanced config](https://developers.openai.com/codex/config-advanced); [Config reference](https://developers.openai.com/codex/config-reference)).

### Managed configuration (admins)

Three admin mechanisms exist ([Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)):

| Mechanism | File | User can override? |
|---|---|---|
| Requirements | `requirements.toml` | No. Constraints |
| Configuration defaults | System `/etc/codex/config.toml` or cloud-managed `config.toml` | Yes |
| Legacy managed defaults | `managed_config.toml` | Reapplied at every client start; overrides user config and CLI `-c` |

`requirements.toml` locations, lowest to highest priority:

1. System file: `/etc/codex/requirements.toml` (Unix, including macOS) or `%ProgramData%\OpenAI\Codex\requirements.toml` (Windows).
2. Agent Security requirements in the cloud config bundle.
3. Legacy `managed_config.toml` fields reinterpreted as requirements.
4. macOS MDM `com.openai.codex:requirements_toml_base64`.

Higher layers override scalars and lists, tables merge by key, and rules, hooks and filesystem restrictions have field-specific composition ([Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)).

`managed_config.toml` lives at `/etc/codex/managed_config.toml` (Unix) or `~/.codex/managed_config.toml` (Windows and other non-Unix). Precedence: MDM `config_toml_base64` > `managed_config.toml` > user `config.toml`. "CLI `--config key=value` overrides apply to the base, but managed layers override them" ([Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)).

Selected `requirements.toml` keys ([Config reference](https://developers.openai.com/codex/config-reference); [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)):

| Key | Effect |
|---|---|
| `allowed_approval_policies` | Allowed `approval_policy` values |
| `allowed_approvals_reviewers` | Allowed `approvals_reviewer` values |
| `allowed_sandbox_modes` | Allowed `sandbox_mode` values |
| `allowed_permission_profiles.<name>` | Codex 0.138.0 and later. Once present, profiles not listed are denied |
| `default_permissions` | Default permission profile |
| `allowed_web_search_modes` | `disabled` is always allowed |
| `allowed_login_methods`, `allowed_chatgpt_workspaces`, `chatgpt_base_url` | Local or MDM only; cloud values are ignored |
| `[features]` | Pins feature flags |
| `[rules] prefix_rules` | Admin execpolicy rules (`prompt` or `forbidden` only) |
| `[mcp_servers.<id>.identity]` | MCP server allowlist, see [mcp.md](mcp.md) |
| `[plugins.<p>.mcp_servers.<s>.identity]` | Allowlist for plugin MCP servers |
| `[marketplaces] restrict_to_allowed_sources`, `allowed_sources` | Marketplace allowlist, see [plugins.md](plugins.md) |
| `[experimental_network]` | Starts the network proxy |
| `permissions.filesystem.deny_read` | Filesystem read denials |
| `[hooks]`, `hooks.managed_dir`, `allow_managed_hooks_only` | Managed hooks, see [hooks.md](hooks.md) |
| `guardian_policy_config` | Auto-review policy |
| `[models.new_thread]` | Model defaults only |
| `model_provider`, `model_providers` | Full replacement per provider ID |
| `enforce_residency = "us"` | Data residency |
| `remote_sandbox_config[]` | Remote sandbox config |
| `windows.allowed_sandbox_implementations` | Windows sandbox constraint |
| `additional_developer_instructions` | Extra developer message, max 10,000 estimated tokens |
| `apps.<id>.enabled`, per-tool `approval_mode` | Connector constraints |
| `[browser_use]`, `[computer_use]` | Browser and Computer Use |

## Loading and invocation

- Codex resolves the layers at startup. Discovery of project `.codex/config.toml` walks from the project root to the cwd and loads every file it finds ([Advanced config](https://developers.openai.com/codex/config-advanced)).
- When a config value conflicts with a requirement, the client falls back to a compatible value and notifies the user ([Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)).
- Cloud-managed requirements are fetched for ChatGPT sign-ins on supported plans and cached with a signed, identity-matched entry. If the fetch fails and there is no valid cache, loading errors instead of starting without the layer. A background refresh affects only later starts ([Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)).
- Cloud-managed and system config can define plugin marketplaces and plugin default-enabled state. These are defaults, not enforced policy ([Config basics](https://developers.openai.com/codex/config-basic); [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)).
- Diagnostics: `/debug-config` (TUI) prints config layer and requirements diagnostics; `/status` shows the active model, approval policy, writable roots and context ([CLI reference](https://developers.openai.com/codex/cli/reference)); `codex doctor [--json] [--summary]` diagnoses install, config, auth and runtime health as a redacted report (local CLI).
- Inference: there are two precedence stacks with different semantics. The config stack sets values; the requirements stack constrains them. Legacy `managed_config.toml` / MDM `config_toml_base64` sits above CLI `-c` at startup, while cloud `config.toml` defaults sit below user config.

## Example

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

```toml
# custom provider (user config only)
model = "gpt-6.1-sol"
model_provider = "proxy"

[model_providers.proxy]
name = "OpenAI via LLM proxy"
base_url = "https://proxy.example.com/v1"
env_key = "OPENAI_API_KEY"
wire_api = "responses"
```

```toml
# /etc/codex/requirements.toml: blocks never and danger-full-access (including --yolo)
allowed_approval_policies = ["untrusted", "on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
```

Sources: [Config basics](https://developers.openai.com/codex/config-basic); [Advanced config](https://developers.openai.com/codex/config-advanced); [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration).

## Limits and gotchas

- **Profiles changed in 0.134.0.** "In Codex 0.134.0 and later, `--profile` no longer reads `[profiles.profile-name]` from `config.toml`, and the top-level `profile = "profile-name"` selector is no longer supported." Move legacy settings into `~/.codex/<name>.config.toml` ([Advanced config](https://developers.openai.com/codex/config-advanced)). Inference: automation that uses `[profiles.x]` or `profile =` broke silently or with warnings from 0.134.0 on.
- **Contradiction: feature flag status.** The docs list `personality` as stable and `true`; local 0.159.2 shows `personality  removed  false`. The docs list `memories` as experimental; local 0.159.2 shows `memories  stable  false` (local CLI vs [Config basics](https://developers.openai.com/codex/config-basic)).
- **`untrusted` in `allowed_approval_policies`.** The managed-config example still lists `"untrusted"`, although `approval_policy = "untrusted"` is retired. The security docs say managed `allowed_approval_policies` must include `untrusted` to permit the stricter trust-level behavior ([Security](https://developers.openai.com/codex/agent-approvals-security); [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)); see [permissions-and-sandbox.md](permissions-and-sandbox.md).
- **Model retirement.** GPT-5.5 retires from ChatGPT, Work and Codex on 2026-10-14 on all plans; the API is unaffected. Replace `gpt-5.5` in configs and managed defaults with `gpt-6-sol` (paid plans) or `gpt-6-luna` (Free/Go) ([Models](https://developers.openai.com/codex/models); [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)).
- **`wire_api`.** Only `responses` is accepted. The docs also say `model_verbosity` is ignored by "Chat Completions providers", which suggests Chat Completions wire support was dropped ([Config reference](https://developers.openai.com/codex/config-reference); [Advanced config](https://developers.openai.com/codex/config-advanced)). **Gap:** whether and when `wire_api = "chat"` was formally removed was not found in the changelog excerpt.
- **Legacy and renamed keys.** `experimental_use_unified_exec_tool` is a legacy name for `features.unified_exec`. `background_terminal_timeout` is replaced by `background_terminal_max_timeout`. `features.codex_hooks` is a deprecated alias of `features.hooks`. The `features.web_search*` toggles are deprecated in favor of `web_search` ([Config reference](https://developers.openai.com/codex/config-reference); [Config basics](https://developers.openai.com/codex/config-basic)).
- **`ignore_default_excludes` defaults to `true`.** Variables whose names contain KEY, SECRET or TOKEN are passed through unless you set it to `false` ([Advanced config](https://developers.openai.com/codex/config-advanced)).
- **Gap: no config JSON Schema.** No machine-readable schema URL for `config.toml` was found. `codex app-server generate-json-schema` covers the app-server protocol, not config (local CLI, `codex app-server --help`).
- **Gap: array merging.** Whether arrays replace or append across layers is not stated in general. It is documented only for specific fields (shell environment filters, permission profiles).
- **Gap: Team Config.** Advanced Config references a "Team Config" page for repository and system skill and rule locations. The fetched URL returned an enterprise rollout guide instead, so that content is not covered.

## Sources

- https://developers.openai.com/codex/config-basic
- https://developers.openai.com/codex/config-advanced
- https://developers.openai.com/codex/config-reference
- https://developers.openai.com/codex/config-sample
- https://developers.openai.com/codex/enterprise/managed-configuration
- https://developers.openai.com/codex/agent-approvals-security
- https://developers.openai.com/codex/models
- https://developers.openai.com/codex/cli/reference
