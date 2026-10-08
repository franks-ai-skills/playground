# Configuration

Configuration is the set of layered settings files that control how the harness behaves in a session: model and effort, permissions, MCP servers, plugins, environment, and UI. Layers at different scopes (organization, user, project, single invocation) let each party set what it owns, and a fixed precedence order resolves conflicts. A trust gate keeps a cloned repository from changing behavior before the user accepts it.

This page covers the settings system itself. The permission, MCP, and plugin keys inside it have their own pages: [permissions-and-sandbox](permissions-and-sandbox.md), [mcp](mcp.md), [plugins](plugins.md).

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Format | Strict JSON, no comments; `$schema` available ([CC](../vendors/claude-code/configuration.md#format)) | TOML; versioned config JSON Schema published in 0.160.1 ([Codex](../vendors/codex/configuration.md#limits-and-gotchas)) | JSON or JSONC; `$schema` available ([OC](../vendors/opencode/configuration.md#format)) |
| User file | `~/.claude/settings.json`; `CLAUDE_CONFIG_DIR` relocates `~/.claude` ([CC](../vendors/claude-code/configuration.md#settings-files)) | `~/.codex/config.toml`; `CODEX_HOME` relocates `~/.codex` ([Codex](../vendors/codex/configuration.md#codex-home)) | `~/.config/opencode/opencode.json`; `OPENCODE_CONFIG`, `OPENCODE_CONFIG_DIR` add layers ([OC](../vendors/opencode/configuration.md#layers)) |
| Project file (shared) | `.claude/settings.json` in the primary working directory, no parent fallback ([CC](../vendors/claude-code/configuration.md#settings-files)) | `.codex/config.toml` in every directory from the project root to the cwd; closest wins ([Codex](../vendors/codex/configuration.md#config-layers-values)) | `opencode.json[c]` walked up to the worktree root, plus `.opencode/opencode.json[c]` ([OC](../vendors/opencode/configuration.md#layers)) |
| Project file (personal) | `.claude/settings.local.json` at the git root, auto-added to global git excludes ([CC](../vendors/claude-code/configuration.md#settings-files)) | None | None |
| Invocation overrides | `--settings <file-or-json>` and flags ([CC](../vendors/claude-code/configuration.md#precedence)) | `-c key=value` (TOML-parsed, dotted paths), dedicated flags, `--profile <name>` overlay file ([Codex](../vendors/codex/configuration.md#cli-overrides-and-global-flags)) | `OPENCODE_CONFIG_CONTENT` inline JSON ([OC](../vendors/opencode/configuration.md#layers)) |
| Admin delivery | `managed-settings.json` (+ `managed-settings.d/`), MDM, or server-managed (polled hourly) ([CC](../vendors/claude-code/configuration.md#managed-delivery)) | `requirements.toml` (system file, cloud bundle, MDM); defaults in `/etc/codex/config.toml` or cloud `config.toml`; legacy `managed_config.toml` ([Codex](../vendors/codex/configuration.md#managed-configuration-admins)) | Managed files in a system directory; macOS MDM domain `ai.opencode.managed`; remote `.well-known/opencode` defaults ([OC](../vendors/opencode/configuration.md#layers)) |
| Admin semantics | Managed values have top precedence; managed-only keys (e.g. `availableModels`, `allowManagedPermissionRulesOnly`) ([CC](../vendors/claude-code/configuration.md#managed-only-keys)) | Two stacks: `requirements.toml` constrains allowed values (client falls back to a compatible value); config defaults can be overridden by users ([Codex](../vendors/codex/configuration.md#loading-and-invocation)) | Managed files and MDM are the highest layers; remote org config is the lowest ([OC](../vendors/opencode/configuration.md#layers)) |
| Precedence, highest first | Managed > CLI > local > project > user ([CC](../vendors/claude-code/configuration.md#precedence)) | CLI > project > profile > user > cloud defaults > system > built-in; requirements constrain all; legacy managed defaults override CLI `-c` ([Codex](../vendors/codex/configuration.md#config-layers-values)) | MDM > managed files > inline env > `.opencode` dirs > project > `OPENCODE_CONFIG` > global > remote org ([OC](../vendors/opencode/configuration.md#layers)) |
| Merge | Scalars override; lists such as `permissions.allow` merge; per-key exceptions ([CC](../vendors/claude-code/configuration.md#precedence)) | Same key: closest layer wins; array merging not documented in general ([Codex](../vendors/codex/configuration.md#limits-and-gotchas)) | Deep merge, later wins per key; arrays replaced except `instructions` and `plugin` ([OC](../vendors/opencode/configuration.md#merge-semantics)) |
| Project trust | Workspace trust gates project `permissions.allow`, `additionalDirectories`, most `env`, `extraKnownMarketplaces`, `.mcp.json` servers, and hooks; `deny`/`ask` apply at once. Stored in `~/.claude.json` ([CC](../vendors/claude-code/configuration.md#workspace-trust)) | Untrusted projects skip all project `.codex/` layers: config, hooks, rules. Stored as `[projects."<path>"] trust_level` in user config ([Codex](../vendors/codex/configuration.md#project-trust)) | No trust gate recorded; `OPENCODE_DISABLE_PROJECT_CONFIG` skips project config ([OC](../vendors/opencode/configuration.md#config-directories)) |
| Keys a project cannot set | Keys scoped "User", "Managed", "Global config"; `defaultMode` `auto`/`bypassPermissions` ([CC](../vendors/claude-code/configuration.md#keys-a-repository-cannot-set)) | `model_provider(s)`, `openai_base_url`, `notify`, `profile(s)`, `otel`, and others; ignored with a warning ([Codex](../vendors/codex/configuration.md#keys-that-project-config-cannot-set)) | None recorded |
| Stricter value from any scope wins | Listed keys such as `disableClaudeAiConnectors: true`, `maxEffortLevel` (lowest cap) ([CC](../vendors/claude-code/configuration.md#precedence)) | Requirements are constraints users cannot override ([Codex](../vendors/codex/configuration.md#managed-configuration-admins)) | None recorded |
| Reload | Files watched and hot-reloaded; `model`, `effortLevel` startup-only ([CC](../vendors/claude-code/configuration.md#loading-and-invocation)) | Resolved at startup ([Codex](../vendors/codex/configuration.md#loading-and-invocation)) | Read and merged at startup ([OC](../vendors/opencode/configuration.md#loading-and-invocation)) |
| Invalid config | Error or warning dialog; `-p` skips bad entries silently ([CC](../vendors/claude-code/configuration.md#loading-and-invocation)) | `--strict-config` errors on unrecognized fields; inference: without it they are tolerated ([Codex](../vendors/codex/configuration.md#cli-overrides-and-global-flags)) | Not recorded |
| Diagnostics | `/status` "Setting sources", `claude doctor` ([CC](../vendors/claude-code/configuration.md#loading-and-invocation)) | `/debug-config`, `/status`, `codex doctor` ([Codex](../vendors/codex/configuration.md#loading-and-invocation)) | `opencode debug config` ([OC](../vendors/opencode/configuration.md#layers)) |
| Model selection | `model` key, `--model`, `/model`, `ANTHROPIC_MODEL`; aliases such as `opus`, `sonnet` ([CC](../vendors/claude-code/configuration.md#models-and-aliases)) | `model` key, `-m`, `/model` ([Codex](../vendors/codex/configuration.md#models)) | `model` as `provider/model`; `small_model` ([OC](../vendors/opencode/configuration.md#top-level-opencodejson-keys)) |
| Reasoning effort | `effortLevel`; `low`…`max`; `maxEffortLevel` cap ([CC](../vendors/claude-code/configuration.md#effort)) | `model_reasoning_effort`; levels the model advertises, e.g. `low`…`ultra` ([Codex](../vendors/codex/configuration.md#model-keys)) | Not recorded on the page |
| Subprocess environment | `env` block sets variables for the session and subprocesses; `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` strips credentials ([CC](../vendors/claude-code/configuration.md#environment-variables)) | `[shell_environment_policy]`: `inherit`, `filters`, `set`; KEY/SECRET/TOKEN names pass through by default ([Codex](../vendors/codex/configuration.md#shell_environment_policy)) | `shell` key; `{env:VAR}` substitution in config ([OC](../vendors/opencode/configuration.md#variable-substitution)) |
| UI settings | `statusLine`, `outputStyle`, `language` in settings ([CC](../vendors/claude-code/configuration.md#important-keys)) | `[tui]` table: keymap, theme, notifications, status line items ([Codex](../vendors/codex/configuration.md#tui)) | Separate `tui.json[c]` ([OC](../vendors/opencode/configuration.md#tui-config)) |

## Generalized model

**Layer.** One source of settings. It has a scope, a delivery channel (file, MDM, server, command line), an optional trust requirement, and a set of keys it may set.

**Scopes**, lowest to highest precedence:

1. **Built-in defaults.**
2. **User.** A file in the user's harness home. Personal defaults for every project.
3. **Project.** A committed file in the repository. Shared team settings. Active only after the user trusts the directory.
4. **Invocation.** Flags, inline overrides, or an overlay file passed for one run.
5. **Policy.** Set by an administrator. Users and projects cannot override it.

**Resolution.** For a single-valued key, the highest layer that sets it wins. For collections the semantics are vendor-specific (merge, replace, or undocumented). Safety-related keys break the order on purpose: a stricter value wins from any scope, or a deny rule beats an allow rule wherever each is set.

**Key scope restrictions.** Some keys are ignored in project files: credentials and provider endpoints, notification programs, and modes that remove approvals. A repository can recommend behavior but cannot grant itself more power than the user or administrator allows.

**Trust gate.** A per-directory decision stored in user-level state. Until the user trusts the directory, the project layer is skipped entirely (Codex) or the keys that widen access are held back (Claude Code). Non-interactive runs have their own rules for this; see Portability.

**Policy layer.** Delivered by a system file, MDM, or a vendor server. It either forces values or restricts the allowed values of a key, and it can restrict which sources other settings may come from (for example, managed rules or hooks only).

**Lifecycle.** Layers are read and merged at startup. Some keys are hot-reloaded. Model and effort are fixed at startup and changed in-session with a command.

**Diagnostics.** Each harness has a command that shows which layers loaded and what the resolved values are.

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Settings file | `settings.json` | `config.toml` | `opencode.json[c]` |
| Harness home | `~/.claude` (`CLAUDE_CONFIG_DIR`) | `~/.codex` (`CODEX_HOME`) | `~/.config/opencode` (`OPENCODE_CONFIG_DIR` adds one) |
| User layer | `~/.claude/settings.json` | `~/.codex/config.toml` | `~/.config/opencode/opencode.json` |
| Project layer | `.claude/settings.json` | `.codex/config.toml` | `opencode.json`, `.opencode/opencode.json` |
| Invocation layer | `--settings`, flags | `-c`, flags, `--profile` | `OPENCODE_CONFIG_CONTENT` |
| Policy layer | Managed settings | `requirements.toml` | Managed files, MDM |
| Trust gate | Workspace trust (`hasTrustDialogAccepted`) | Project trust (`trust_level`) | — |
| Model | `model` | `model` | `model` |
| Reasoning effort | `effortLevel` | `model_reasoning_effort` | — |
| Subprocess environment | `env` | `shell_environment_policy` | `{env:...}`, `shell` |
| Diagnostics | `/status`, `claude doctor` | `/debug-config`, `codex doctor` | `opencode debug config` |

## Portability

No harness reads another harness's settings file. Each project needs one file per harness: `.claude/settings.json`, `.codex/config.toml`, `opencode.json`. Keep shared guidance in [instructions](instructions.md) and skills, which do have shared file names, and keep settings files minimal.

Equivalent settings across the leads:

| Intent | Claude Code | Codex |
| --- | --- | --- |
| Pick a model | `"model": "<alias or ID>"` | `model = "<ID>"` |
| Set effort | `"effortLevel": "high"` | `model_reasoning_effort = "high"` |
| Personal project override | `.claude/settings.local.json` | User config, or a `--profile` file; no project-local file |
| One-run override | `--settings '{"...": ...}'` | `-c key=value` |
| Enforce for an organization | Managed settings | `requirements.toml` |

Model IDs differ per vendor and are not portable. The effort level names `low`, `medium`, `high`, `xhigh`, and `max` appear in both lists ([CC](../vendors/claude-code/configuration.md#effort), [Codex](../vendors/codex/configuration.md#model-keys)); Codex accepts only the levels the selected model advertises.

Traps:

- **Untrusted Codex projects ignore the whole `.codex/` folder**, including hooks and rules. In Claude Code, an untrusted project still applies its `deny` and `ask` rules ([Codex](../vendors/codex/configuration.md#project-trust), [CC](../vendors/claude-code/configuration.md#workspace-trust)).
- **Claude Code headless runs never show the trust dialog.** With `-p` or the SDK, project allow rules are not used, but project hooks and `env` are ([CC](../vendors/claude-code/configuration.md#workspace-trust)).
- **A trusted Codex project beats `--profile`** for every key it sets, because profile files sit below project config. Provider, `notify`, and `profile` keys are the exception, since a project cannot set them ([Codex](../vendors/codex/configuration.md#profiles-file-based-since-01340)).
- **In Claude Code, a project scalar beats a user scalar.** A user `false` cannot override a project `true`; use `settings.local.json` ([CC](../vendors/claude-code/configuration.md#limits-and-gotchas)).
- **Array merging differs.** Claude Code merges list keys across files; OpenCode replaces arrays except `instructions` and `plugin`; Codex does not document it ([CC](../vendors/claude-code/configuration.md#precedence), [OC](../vendors/opencode/configuration.md#limits-and-gotchas), [Codex](../vendors/codex/configuration.md#limits-and-gotchas)).
- **Secrets in subprocess environments.** Codex passes variables whose names contain KEY, SECRET, or TOKEN to commands unless `ignore_default_excludes = false` ([Codex](../vendors/codex/configuration.md#limits-and-gotchas)). Claude Code strips credentials only with `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` ([CC](../vendors/claude-code/configuration.md#environment-variables)).
- **Hot reload exists only in Claude Code.** Codex and OpenCode need a new session after a config change.
- **Codex profiles changed in 0.134.0.** `[profiles.<name>]` tables and the `profile =` selector no longer work; use `~/.codex/<name>.config.toml` ([Codex](../vendors/codex/configuration.md#limits-and-gotchas)).
- **Comments.** Claude Code settings are strict JSON. OpenCode accepts JSONC. TOML has comments.

## Dropped from the generalization

- **Personal project settings file, `.claude/settings.local.json`** (Claude Code): Codex has no project-local, uncommitted config layer.
- **Overridable admin defaults** (Codex system and cloud `config.toml`; OpenCode remote org config): Claude Code managed settings are always enforced, with no "default the user may override" layer.
- **Named profile files, `--profile`** (Codex): Claude Code has `--settings <file>`, which is covered as the invocation layer, but no named-profile mechanism.
- **Feature flags, `[features]`** (Codex): Claude Code has no documented feature-flag table in settings.
- **Custom model provider definitions, `[model_providers.<id>]`** (Codex; OpenCode `provider`): the Claude Code page records provider selection only through environment variables and managed `allowedProviders`, not a provider table.
- **Output styles** (Claude Code): replaceable style prompts have no Codex counterpart; Codex `personality` is a fixed enum and shows as removed in the local 0.159.2 flag list.
- **Command-driven status line** (Claude Code): Codex `tui.status_line` selects items and runs no script.
- **Config variable substitution, `{env:}` and `{file:}`** (OpenCode): neither lead has general substitution in settings; Claude Code expands variables only in MCP fields.
- **Stricter-wins key list** (Claude Code): the specific keys are vendor-specific. The principle is kept in the model.
- **Commit attribution and built-in git instructions, `attribution`, `includeGitInstructions`** (Claude Code): no Codex counterpart recorded.
- **Telemetry, `[otel]`** (Codex): the Claude Code page mentions OTel only as environment variables a project cannot set, not as a settings table.
- **`requiredMinimumVersion`, `requiredMaximumVersion`** (Claude Code): no Codex version constraint recorded.
- **Separate TUI config file, `tui.json`** (OpenCode): both leads keep UI keys in the main settings file.

## Sources

- [Claude Code: configuration](../vendors/claude-code/configuration.md)
- [Codex: configuration](../vendors/codex/configuration.md)
- [OpenCode: configuration](../vendors/opencode/configuration.md)
- [Claude Code README](../vendors/claude-code/README.md), [Codex README](../vendors/codex/README.md), [OpenCode README](../vendors/opencode/README.md)
