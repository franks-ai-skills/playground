# Configuration

Configuration is the set of layered settings files that control how the harness behaves in a session: model and effort, permissions, MCP servers, plugins, environment, and UI. Layers at different scopes (organization, user, project, single run) let each party set what it owns, and a fixed precedence order resolves conflicts. A trust gate keeps a cloned repository from changing behavior before the user accepts it.

This page covers the settings system itself and which layer a setting belongs in. What a permission rule, MCP server or plugin entry should contain is on [permissions-and-sandbox](permissions-and-sandbox.md), [mcp](mcp.md) and [plugins](plugins.md).

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Format | Strict JSON, no comments; `$schema` available ([CC](../vendors/claude-code/configuration.md#format)) | TOML; no config JSON Schema found ([Codex](../vendors/codex/configuration.md#format)) | JSON or JSONC; `$schema` available ([OC](../vendors/opencode/configuration.md#format)) |
| User file | `~/.claude/settings.json`; `CLAUDE_CONFIG_DIR` relocates `~/.claude` ([CC](../vendors/claude-code/configuration.md#settings-files)) | `~/.codex/config.toml`; `CODEX_HOME` relocates `~/.codex` ([Codex](../vendors/codex/configuration.md#codex-home)) | `~/.config/opencode/opencode.json` ([OC](../vendors/opencode/configuration.md#layers)) |
| Project file | `.claude/settings.json` in the primary working directory, no parent fallback ([CC](../vendors/claude-code/configuration.md#settings-files)) | `.codex/config.toml` in every directory from the project root to the cwd; closest wins ([Codex](../vendors/codex/configuration.md#config-layers-values)) | `opencode.json[c]` walked up to the worktree root, plus `.opencode/opencode.json[c]` ([OC](../vendors/opencode/configuration.md#layers)) |
| Personal project file | `.claude/settings.local.json`, auto-added to global git excludes ([CC](../vendors/claude-code/configuration.md#settings-files)) | None | None |
| Run overrides | `--settings <file-or-json>` and flags ([CC](../vendors/claude-code/configuration.md#precedence)) | `-c key=value`, dedicated flags, `--profile <name>` overlay file ([Codex](../vendors/codex/configuration.md#cli-overrides-and-global-flags)) | `OPENCODE_CONFIG_CONTENT` inline JSON ([OC](../vendors/opencode/configuration.md#layers)) |
| Admin layer | Managed settings (`managed-settings.json`, MDM, server-managed); always enforced ([CC](../vendors/claude-code/configuration.md#managed-delivery)) | `requirements.toml` constrains allowed values; managed `config.toml` sets defaults users can override ([Codex](../vendors/codex/configuration.md#managed-configuration-admins)) | Managed files, macOS MDM, remote org defaults ([OC](../vendors/opencode/configuration.md#layers)) |
| Precedence, highest first | Managed > CLI > local > project > user ([CC](../vendors/claude-code/configuration.md#precedence)) | CLI > project > profile > user > cloud defaults > system > built-in; requirements constrain all ([Codex](../vendors/codex/configuration.md#config-layers-values)) | MDM > managed files > inline env > `.opencode` dirs > project > `OPENCODE_CONFIG` > global > remote org ([OC](../vendors/opencode/configuration.md#layers)) |
| Merge | Scalars override; lists such as `permissions.allow` merge ([CC](../vendors/claude-code/configuration.md#precedence)) | Closest layer wins; array merging not documented ([Codex](../vendors/codex/configuration.md#limits-and-gotchas)) | Deep merge; arrays replaced except `instructions` and `plugin` ([OC](../vendors/opencode/configuration.md#merge-semantics)) |
| Project trust | Trust holds back project `allow` rules, `additionalDirectories`, most `env`, `.mcp.json` servers, hooks; `deny`/`ask` apply at once ([CC](../vendors/claude-code/configuration.md#workspace-trust)) | Untrusted projects skip all `.codex/` layers: config, hooks, rules ([Codex](../vendors/codex/configuration.md#project-trust)) | No trust gate; `OPENCODE_DISABLE_PROJECT_CONFIG` skips project config ([OC](../vendors/opencode/configuration.md#config-directories)) |
| Keys a project cannot set | User-, managed- and global-scoped keys; `defaultMode` `auto`/`bypassPermissions` ([CC](../vendors/claude-code/configuration.md#keys-a-repository-cannot-set)) | `model_provider(s)`, `openai_base_url`, `notify`, `profile(s)`, `otel` and others ([Codex](../vendors/codex/configuration.md#keys-that-project-config-cannot-set)) | None recorded |
| Reload | Hot-reloaded; `model`, `effortLevel` startup-only ([CC](../vendors/claude-code/configuration.md#loading-and-invocation)) | Resolved at startup ([Codex](../vendors/codex/configuration.md#loading-and-invocation)) | Startup only ([OC](../vendors/opencode/configuration.md#loading-and-invocation)) |
| Subprocess environment | `env` block; `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` strips credentials ([CC](../vendors/claude-code/configuration.md#environment-variables)) | `[shell_environment_policy]`: `inherit`, `filters`, `set` ([Codex](../vendors/codex/configuration.md#shell_environment_policy)) | `shell` key; `{env:VAR}` substitution ([OC](../vendors/opencode/configuration.md#variable-substitution)) |
| Diagnostics | `/status`, `claude doctor` ([CC](../vendors/claude-code/configuration.md#loading-and-invocation)) | `/debug-config`, `/status`, `codex doctor`, `--strict-config` ([Codex](../vendors/codex/configuration.md#loading-and-invocation)) | `opencode debug config` ([OC](../vendors/opencode/configuration.md#layers)) |

## Generalized model

**Layer.** One source of settings. It has a scope, a delivery channel (file, MDM, server, command line), an optional trust requirement, and a set of keys it may set.

**Scopes**, lowest to highest precedence:

1. **Built-in defaults.**
2. **User.** A file in the user's harness home. Personal defaults for every project.
3. **Project.** A committed file in the repository. Shared team settings. Active only after the user trusts the directory.
4. **Invocation.** Flags, inline overrides or an overlay file for one run.
5. **Policy.** Set by an administrator. Users and projects cannot override it.

**Resolution.** For a single-valued key, the highest layer that sets it wins. For collections the semantics are vendor-specific (merge, replace, or undocumented). Safety-related keys break the order on purpose: a stricter value wins from any scope, and a deny rule beats an allow rule wherever each is set.

**Key scope restrictions.** Project files cannot set credentials, provider endpoints, notification programs, or modes that remove approvals. A repository can recommend behavior but cannot grant itself more power than the user or administrator allows.

**Trust gate.** A per-directory decision stored in user-level state. Until the user trusts the directory, the project layer is skipped entirely (Codex) or the keys that widen access are held back (Claude Code). Non-interactive runs follow their own rules; see [Portability](#portability).

**Policy layer.** Delivered by a system file, MDM or a vendor server. It forces values or restricts the allowed values of a key, and it can restrict which sources other settings may come from (for example, managed rules or hooks only).

**Lifecycle.** Layers are read and merged at startup. Claude Code hot-reloads most keys. Model and effort are fixed at startup and changed in-session with a command.

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Settings file | `settings.json` | `config.toml` | `opencode.json[c]` |
| Harness home | `~/.claude` (`CLAUDE_CONFIG_DIR`) | `~/.codex` (`CODEX_HOME`) | `~/.config/opencode` |
| Project layer | `.claude/settings.json` | `.codex/config.toml` | `opencode.json`, `.opencode/opencode.json` |
| Invocation layer | `--settings`, flags | `-c`, flags, `--profile` | `OPENCODE_CONFIG_CONTENT` |
| Policy layer | Managed settings | `requirements.toml` | Managed files, MDM |
| Trust gate | Workspace trust (`hasTrustDialogAccepted`) | Project trust (`trust_level`) | — |
| Model | `model` | `model` | `model` (`provider/model`) |
| Reasoning effort | `effortLevel` | `model_reasoning_effort` | — |
| Subprocess environment | `env` | `shell_environment_policy` | `{env:...}`, `shell` |
| Diagnostics | `/status`, `claude doctor` | `/debug-config`, `codex doctor` | `opencode debug config` |

## When to use it and when not

Configuration stores every other control. The decision is mostly which layer holds a setting; what the setting should be is decided on the concept's own page.

| Use it when | Layer |
| --- | --- |
| Model, effort, environment or UI should be the same for everyone on a repository | Project |
| You want personal defaults for every project | User |
| You want to try a setting before sharing it, or override one project value for yourself | Claude Code local file; in Codex, user config or a `--profile` file |
| A protection must not be weakened by users or repositories | Policy |
| One run needs a different preset (review, CI) | Invocation |

| Do not use it for | Use instead | Why |
| --- | --- | --- |
| Conventions, style, workflow the model should follow | [instructions.md](instructions.md), [skills.md](skills.md) | Settings files are not shared between harnesses; instruction and skill files are. Keep settings minimal. |
| Allow, ask or deny a specific action | [permissions-and-sandbox.md](permissions-and-sandbox.md) | Stored in config, but the rule design and its limits live there |
| An action that must run at a lifecycle point | [hooks.md](hooks.md) | Hooks are registered in config, but their design and failure modes differ |
| Which MCP servers or plugins may load | [mcp.md](mcp.md), [plugins.md](plugins.md), with allowlists in the policy layer | `.mcp.json` is not the full list of servers |
| A merge gate independent of agent settings | CI, see [automation.md](automation.md) | Any committed agent config can be changed by a pull request |
| Secrets and API keys | A secret manager, short-lived tokens | Committed config is readable by everyone, and repository-set endpoints have leaked keys (CVE-2026-21852) |

## Approaches

### Scope split

**What.** Each setting goes into the layer whose owner should control it. **When.** Every setup; the other approaches build on it.

| Layer | Put here | Keep out |
| --- | --- | --- |
| User | Secret-path read denies, destructive-command denies or asks, personal MCP servers, telemetry opt-outs, a bypass-mode lock | Team rules other people need |
| Project (committed) | Narrow allow rules for build and test, ask rules for `git push` and deploys, project hooks, sandbox write paths and domains the build needs | Secrets, provider endpoints, credential helpers, broad allow rules |
| Project-local (Claude Code only) | Experiments before promoting them; personal per-project overrides | Anything the team needs |
| Policy | Sandbox required, bypass disabled, MCP allowlist, telemetry destination, secret-path denies | Preferences users should be able to change |

**Claude Code.** User, project, local and managed files as in the [comparison](#comparison). A project scalar beats a user scalar; list keys merge; a deny at any level blocks an allow at any other level. **Codex.** No project-local layer; use user config or a `--profile` overlay for personal overrides. **Trade-off.** In Claude Code a trusted project file can add allow rules and sandbox `allowWrite` and `allowedDomains` entries, because lists merge (inference).

### Task profiles

**What.** An overlay chosen per run, so review, normal work and CI use different presets without editing the base config. **When.** Recurring tasks with different risk.

- **Codex:** `--profile <name>` loads `~/.codex/<name>.config.toml` above the user config. Vendor presets: standard `--sandbox workspace-write --ask-for-approval on-request`; read-only `--sandbox read-only --ask-for-approval on-request`; CI `--sandbox read-only --ask-for-approval never` ([Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security)).
- **Claude Code:** `--settings <file-or-json>` is the closest equivalent; there are no named profiles. CI example: `-p --permission-mode dontAsk --allowedTools "Bash(npm test)" "Read"` ([CC permission modes](https://code.claude.com/docs/en/permission-modes)). Starter files: [anthropics/claude-code examples/settings](https://github.com/anthropics/claude-code/tree/main/examples/settings).

**Trade-off.** A trusted Codex project beats `--profile` for every key it sets, except keys a project cannot set.

### Policy layer

**What.** An administrator layer that forces or constrains values and can restrict where other settings come from. **When.** Teams and fleets; individuals can use parts of it (see [practice 4](#practices)).

- **Claude Code:** managed settings via file, MDM or server. Source restrictions: `allowManagedPermissionRulesOnly`, `allowManagedHooksOnly`, `allowManagedReadPathsOnly`, `allowManagedDomainsOnly` ([CC permissions](https://code.claude.com/docs/en/permissions)).
- **Codex:** `requirements.toml` "enforces admin-controlled constraints users cannot override": approval policy, reviewer, sandbox mode, permission profiles, web search mode, managed hooks, allowed MCP servers, plugin marketplace sources. Delivery: cloud console (signed bundles), macOS MDM, `/etc/codex/requirements.toml` ([Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration)).

**Trade-off.** A managed-settings file copied in by a repository Dockerfile can be changed by anyone with write access ([CC devcontainer](https://code.claude.com/docs/en/devcontainer)). Claude Code on native Windows exits under `failIfUnavailable`, so sandbox policy has to be delivered per OS.

### Restricted loading for untrusted repositories

**What.** Start the harness with the project layer skipped. **When.** Batch or CI runs over cloned or forked repositories.

- **Claude Code:** `--setting-sources user` or `--bare`, plus `--settings '{"disableAllHooks": true}'` and `disabledMcpjsonServers` ([CC permissions](https://code.claude.com/docs/en/permissions)).
- **Codex:** leave the project untrusted; the whole `.codex/` layer is skipped.
- **OpenCode:** `OPENCODE_DISABLE_PROJECT_CONFIG`.

**Trade-off.** The run also loses the team's deny and ask rules.

## Practices

1. **Assign each setting to the scope that owns it.**
   - Why: Layers differ in reach and trust; policy cannot be overridden.
   - How: Follow the [scope split](#scope-split). Trail of Bits keeps global MCP servers in the user layer and sets `enableAllProjectMcpServers: false`, because "a compromised repo could ship malicious MCP servers".
   - Evidence: [Vendor] [CC settings](https://code.claude.com/docs/en/settings), [Codex advanced config](https://learn.chatgpt.com/codex/config-advanced); [Practitioner] [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config).

2. **Keep secrets, endpoints and credential helpers out of committed config.**
   - Why: A project-set `ANTHROPIC_BASE_URL` sent the API key to an attacker before trust (CVE-2026-21852). Codex refuses provider and base-URL keys in project config; Claude Code ignores project and local `sandbox.credentials` entries since v2.1.246.
   - How: Load keys from a secret manager; in dev containers, do not mount `~/.ssh` or cloud credentials, pass short-lived tokens via `containerEnv`, Codespaces secrets or workload identity.
   - Evidence: [Advisory] [Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/); [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing), [CC devcontainer](https://code.claude.com/docs/en/devcontainer).

3. **Review harness config as executable code.**
   - Why: Hooks, MCP definitions, environment variables and config redirects in repository files have run code or leaked credentials in both leads (see [Security](#security)).
   - How: Inspect `.claude/`, `.codex/` and `.mcp.json` before opening a project; require owner review (for example CODEOWNERS, inference) on those paths, `.agents/`, `AGENTS.md`, `.devcontainer/` and CI workflows; read the trust dialog's list of rules; in Claude Code, audit in-session changes with `ConfigChange` hooks.
   - Evidence: [Advisory] [Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/); [Vendor] [CC security](https://code.claude.com/docs/en/security).

4. **Put protections that must not be weakened in the policy layer.**
   - Why: User and project files can be edited by whoever controls them; s1ngularity malware launched agent CLIs with bypass flags (Aug 2025).
   - How: Claude Code managed `{"sandbox": {"enabled": true, "failIfUnavailable": true, "allowUnsandboxedCommands": false}}`, `permissions.disableBypassPermissionsMode: "disable"`, managed-only switches; Codex `allowed_approval_policies = ["on-request"]`, `allowed_sandbox_modes = ["read-only","workspace-write"]`, admin `prefix_rules` (`prompt` or `forbidden` only). Individuals can set `disableBypassPermissionsMode` in their own user settings. Deliver by MDM or server, not a repository file.
   - Evidence: [Vendor] [CC permissions](https://code.claude.com/docs/en/permissions), [Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration); [Advisory] [Wiz on s1ngularity](https://wiz.io/blog/s1ngularity-supply-chain-attack).

5. **Filter secrets from subprocess environments explicitly.**
   - Why: Claude Code sandboxed commands inherit variables "including any secrets". The Codex sources disagree: the docs summary says names containing KEY, SECRET or TOKEN are removed by default; the [vendor notes](../vendors/codex/configuration.md#shell_environment_policy) record `ignore_default_excludes` defaulting to `true`, so they pass through.
   - How: Claude Code `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`, no secrets in the `env` block; Codex set `ignore_default_excludes = false` and `exclude`/`include_only` filters ("Includes don't restore variables that were already excluded").
   - Evidence: [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing), [Codex advanced config](https://learn.chatgpt.com/codex/config-advanced).

6. **Use task profiles instead of editing the base config.**
   - Why: CI needs no prompts and no network; review needs no writes.
   - How: See [task profiles](#task-profiles); keep the CI profile read-only or an exact allowlist, no network (inference). Move old Codex `[profiles.<name>]` tables to `~/.codex/<name>.config.toml`.
   - Evidence: [Vendor] [Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security), [CC permission modes](https://code.claude.com/docs/en/permission-modes).

7. **Turn off repository config for headless runs over untrusted repositories.**
   - Why: Claude Code `-p` and SDK runs never show the trust dialog; hooks, `env`, `apiKeyHelper` and a project skill's hooks are used, and `.mcp.json` servers connect.
   - How: `--setting-sources user` or `--bare`, plus `disableAllHooks` via `--settings` (in user settings alone it loses to project settings); watch stderr for "this workspace has not been trusted". In Codex, do not trust the project and do not pass `--dangerously-bypass-hook-trust`.
   - Evidence: [Vendor] [CC permissions](https://code.claude.com/docs/en/permissions), [Codex hooks](https://learn.chatgpt.com/docs/hooks).

8. **Keep personal overrides out of git.**
   - Why: Claude Code adds `settings.local.json` to global git excludes only when it writes the file itself. A tracked local file, or one under a symlinked `.claude`, counts as repository-supplied and its allow rules wait for trust.
   - How: Git-ignore a hand-created local file; use it, not user settings, to override a project scalar.
   - Evidence: [Vendor] [CC settings](https://code.claude.com/docs/en/settings).

9. **Pin the telemetry destination in policy and keep content logging off.**
   - Why: Tool-decision events are the audit trail in both leads; content logging is a privacy decision.
   - How: Claude Code endpoint and headers in managed settings (this removes conflicting developer variables); `OTEL_LOG_USER_PROMPTS` and `OTEL_LOG_TOOL_CONTENT` stay off by default. Codex `[otel]` pinned in managed config, `log_user_prompt = false`; a project cannot set `otel`.
   - Evidence: [Vendor] [CC monitoring](https://code.claude.com/docs/en/monitoring-usage), [Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration).

10. **Verify the resolved config after every change and upgrade.**
    - Why: Merges are vendor-specific, `-p` skips bad entries silently, and precedence changed between versions (Claude Code v2.1.207 local-file trust, v2.1.285 strict-sandbox precedence; Codex 0.134 profiles).
    - How: See [Verification and checklist](#verification-and-checklist).
    - Evidence: [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing), [Codex rules](https://learn.chatgpt.com/codex/rules).

## Security

Every advisory below exploited configuration that ran before or outside the permission system. Verification should therefore focus on pre-trust paths, not only on rule lists (inference).

| Threat | Advisory | Mitigation |
| --- | --- | --- |
| Repository hooks run at session start | GHSA-ph6w-f82w-28w6 (Claude Code, CVSS 8.7): hooks in `.claude/settings.json` ran without confirmation. Reported 2025-07-21, fixed 2025-08-26 in 1.0.87 ([Check Point](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)) | Workspace trust; [practice 7](#practices) for `-p` |
| Repository MCP config starts servers before trust | CVE-2025-59536 (Claude Code, CVSS 8.7): `enableAllProjectMcpServers` started servers before the dialog. Fixed 2025-09-22 in 1.0.111 ([GitLab](https://advisories.gitlab.com/npm/@anthropic-ai/claude-code/CVE-2025-59536/)) | `enableAllProjectMcpServers: false`; MCP allowlist in policy |
| Repository redirects the API endpoint | CVE-2026-21852 (Claude Code): project `ANTHROPIC_BASE_URL` leaked the API key before trust. Reported 2025-10-28, fixed 2025-12-28, published 2026-01-21 | No endpoints in committed config |
| Repository redirects the harness home | CVE-2025-61260 (Codex): `.env` with `CODEX_HOME=./.codex` plus `mcp_servers` ran commands at startup ([Check Point](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/), [NVD](https://nvd.nist.gov/vuln/detail/cve-2025-61260)) | Keep Codex updated; do not trust unknown projects |
| Agent edits its own config | CVE-2025-53773 (Copilot / VS Code, CVSS 7.8, Aug 2025): injection wrote `"chat.tools.autoApprove": true` ([Wiz](https://www.wiz.io/vulnerability-database/cve/cve-2025-53773)) | Protected paths in both leads; keep Claude Code sandbox filesystem isolation on, or a sandboxed command can write `~/.claude/settings.json` |
| Malware launches the CLI with bypass flags | s1ngularity / Nx npm compromise, 2025-08-26 ([Wiz](https://wiz.io/blog/s1ngularity-supply-chain-attack)) | Lock bypass in policy or user settings |
| Telemetry redirected | — | Pin endpoint in managed settings |

Several fixes were delivered by forced updates (Claude Code deprecated versions before 1.0.24, per the [CVE-2025-55284 advisory](https://advisories.gitlab.com/pkg/npm/@anthropic-ai/claude-code/CVE-2025-55284/)). Keep harnesses current unless a container pins a version on purpose (inference).

## Verification and checklist

1. **Layers loaded.** Claude Code `/status` (setting sources); Codex `/debug-config` and `/status`; OpenCode `opencode debug config`. The policy layer appears where expected.
2. **Rules by source.** Claude Code `/permissions` lists rules per file and has a "Recently denied" tab.
3. **Config health.** `claude doctor`, `codex doctor`; Codex `--strict-config` errors on unknown fields such as leftover `[profiles.*]` tables.
4. **Trust gate.** Clone a test repository with hooks, `.mcp.json`, `env.ANTHROPIC_BASE_URL` and a `.env` setting `CODEX_HOME`. Nothing may run before trust, also in `-p` and `codex exec` (inference).
5. **Policy holds.** Start with `--dangerously-skip-permissions` or `--yolo`; policy must refuse it. Set a managed-only key from a project file; it must have no effect.
6. **Telemetry.** `tool_decision` deny events reach the collector.
7. **After upgrades.** Repeat steps 1 to 6.

- [ ] User layer holds secret-path denies, personal MCP servers and preferences only.
- [ ] Committed config has no secrets, base URLs, provider settings or credential helpers.
- [ ] `settings.local.json` is git-ignored and untracked.
- [ ] Harness config paths, `AGENTS.md`, `.devcontainer/` and CI workflows need owner review.
- [ ] Bypass mode is disabled in policy (or user settings, for individuals).
- [ ] Policy is delivered by MDM, server or system file, not a repository file.
- [ ] Subprocess secret filtering is set explicitly in both leads.
- [ ] Headless runs over third-party repositories skip project config and hooks.
- [ ] Codex config has no `[profiles.*]` tables and passes `--strict-config`.
- [ ] Telemetry endpoint is pinned; prompt logging is off unless policy allows it.

## Portability

No harness reads another harness's settings file. Each project needs one file per harness. Keep shared guidance in [instructions.md](instructions.md) and [skills.md](skills.md), which have shared file names, and keep settings files minimal.

| Intent | Claude Code | Codex |
| --- | --- | --- |
| Pick a model | `"model": "<alias or ID>"` | `model = "<ID>"` |
| Set effort | `"effortLevel": "high"` | `model_reasoning_effort = "high"` |
| Personal project override | `.claude/settings.local.json` | User config or `--profile` file |
| One-run override | `--settings '{"...": ...}'` | `-c key=value` |
| Enforce for an organization | Managed settings | `requirements.toml` |

Model IDs are not portable. The effort names `low`, `medium`, `high`, `xhigh` and `max` appear in both leads; Codex accepts only the levels the selected model advertises.

Traps:

- **Trust scope differs.** Untrusted Codex projects ignore the whole `.codex/` folder, including hooks and rules. Untrusted Claude Code projects still apply their `deny` and `ask` rules ([Codex](../vendors/codex/configuration.md#project-trust), [CC](../vendors/claude-code/configuration.md#workspace-trust)).
- **Claude Code headless runs never show the trust dialog.** Project allow rules are skipped, but project hooks and `env` are used.
- **A trusted Codex project beats `--profile`** for every key it may set ([Codex](../vendors/codex/configuration.md#profiles-file-based-since-01340)).
- **A Claude Code project scalar beats a user scalar.** A user `false` cannot override a project `true` ([CC](../vendors/claude-code/configuration.md#limits-and-gotchas)).
- **Array merging differs:** Claude Code merges, OpenCode replaces (except `instructions`, `plugin`), Codex does not document it.
- **Hot reload exists only in Claude Code.** Codex and OpenCode need a new session.
- **Codex profiles changed in 0.134.0.** `[profiles.<name>]` and `profile =` no longer work.
- **Comments.** Claude Code settings are strict JSON; TOML and OpenCode's JSONC allow comments.

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| Personal project file `settings.local.json`; `attribution`, `includeGitInstructions`; `requiredMinimumVersion`/`requiredMaximumVersion` | Claude Code | No Codex counterpart |
| Output styles; command-driven status line | Claude Code | Codex `personality` is a fixed enum; Codex `tui.status_line` runs no script |
| Specific stricter-wins key list | Claude Code | Keys are vendor-specific; the principle stays in the model |
| Named profile files `--profile`; `[features]` flags; `[model_providers.<id>]`; `[otel]` table | Codex | No Claude Code counterpart as a settings mechanism (Claude Code uses `--settings`, environment variables) |
| Overridable admin defaults | Codex, OpenCode | Claude Code managed settings are always enforced |
| `{env:}`/`{file:}` substitution; separate `tui.json` | OpenCode | Neither lead has them |

## Open questions

- **Codex secret filtering default.** The docs summary and the vendor notes disagree; set it explicitly.
- **Codex array merging** across layers is undocumented.
- **CODEOWNERS for harness config** is inference from the CVE history; no vendor prescribes it.
- **CVE-2025-61260 fixed version.** One research note lists affected versions as "≤ 0.23.0", another "fixed in 0.23.0 (2025-08-20)". Check [NVD](https://nvd.nist.gov/vuln/detail/cve-2025-61260).
- **Adoption** of managed settings and requirements, and SIEM detection content for `tool_decision` events: no public data found.

## Sources

- Vendor pages: [Claude Code configuration](../vendors/claude-code/configuration.md), [Codex configuration](../vendors/codex/configuration.md), [OpenCode configuration](../vendors/opencode/configuration.md)
- Research note: [configuration, permissions and sandbox](../research-notes/agent-harness-best-practices/configuration-permissions-sandbox.md)
- Claude Code: [settings](https://code.claude.com/docs/en/settings), [permissions](https://code.claude.com/docs/en/permissions), [permission modes](https://code.claude.com/docs/en/permission-modes), [sandboxing](https://code.claude.com/docs/en/sandboxing), [devcontainer](https://code.claude.com/docs/en/devcontainer), [security](https://code.claude.com/docs/en/security), [monitoring](https://code.claude.com/docs/en/monitoring-usage), [examples/settings](https://github.com/anthropics/claude-code/tree/main/examples/settings)
- Codex: [advanced config](https://learn.chatgpt.com/codex/config-advanced), [managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration), [agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security), [rules](https://learn.chatgpt.com/codex/rules), [hooks](https://learn.chatgpt.com/docs/hooks)
- Practitioner: [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)
- Advisories: [Check Point on CVE-2025-59536 and CVE-2026-21852](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/), [GitLab CVE-2025-59536](https://advisories.gitlab.com/npm/@anthropic-ai/claude-code/CVE-2025-59536/), [GitLab CVE-2025-55284](https://advisories.gitlab.com/pkg/npm/@anthropic-ai/claude-code/CVE-2025-55284/), [Check Point on CVE-2025-61260](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/), [NVD CVE-2025-61260](https://nvd.nist.gov/vuln/detail/cve-2025-61260), [Wiz CVE-2025-53773](https://www.wiz.io/vulnerability-database/cve/cve-2025-53773), [Wiz s1ngularity](https://wiz.io/blog/s1ngularity-supply-chain-attack)
