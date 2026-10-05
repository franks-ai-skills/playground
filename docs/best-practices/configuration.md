# Configuration: best practices

How to split harness settings across scopes, keep secrets out of them, and make protections stick. Claude Code (CC) and Codex are equal leads; OpenCode (OC) appears where the research covers it. Terms follow the generalized model in [Configuration](../concepts/configuration.md): layer, scope, trust gate, policy layer, invocation layer. Rule and sandbox design is on [Permissions and sandbox](permissions-and-sandbox.md); hook design is on [Hooks](hooks.md).

Research date: 2026-10-04 (CC around v2.1.28x, Codex after the 0.134 profile change). Items marked "(2025)" are older. Evidence labels: **[Vendor]** vendor documentation, **[Empirical]** measured data, **[Advisory]** CVE, security advisory or incident report, **[Practitioner]** practitioner or researcher opinion. "Inference" marks a conclusion the research draws without a direct source.

## Summary

1. [Assign each setting to the scope that owns it](#1-assign-each-setting-to-the-scope-that-owns-it): personal in user, team in project, experiments in CC local, non-negotiable in policy.
2. [Keep secrets, endpoints and credential helpers out of committed config](#2-keep-secrets-endpoints-and-credential-helpers-out-of-committed-config); repository-set base URLs have leaked API keys.
3. [Review harness config as executable code](#3-review-harness-config-as-executable-code); it caused CVEs in both leads.
4. [Put protections that must not be weakened in the policy layer](#4-put-protections-that-must-not-be-weakened-in-the-policy-layer), delivered by a channel that repository files cannot change.
5. [Filter secrets from subprocess environments explicitly](#5-filter-secrets-from-subprocess-environments-explicitly); do not rely on defaults.
6. [Use task profiles instead of editing the base config](#6-use-task-profiles-instead-of-editing-the-base-config), with a minimal CI profile.
7. [Turn off repository config for headless runs over untrusted repositories](#7-turn-off-repository-config-for-headless-runs-over-untrusted-repositories); CC `-p` treats every folder as trusted.
8. [Verify the resolved config after every change and upgrade](#10-verify-the-resolved-config-after-every-change-and-upgrade).

## When to use it

Related best-practice pages: [permissions and sandbox](permissions-and-sandbox.md), [hooks](hooks.md), [instructions](instructions.md), [skills](skills.md), [subagents](subagents.md), [MCP](mcp.md), [plugins](plugins.md), [automation](automation.md).

Configuration stores every other control: permission rules, sandbox policy, hooks, MCP servers, plugins, environment, model. The decision on this page is mostly *which layer* holds a setting. What the setting should be is decided on the concept's own page.

| Goal | Right tool |
| --- | --- |
| Model, effort, environment or UI for everyone on a repository | Project layer (this page) |
| Personal defaults for every project | User layer (this page) |
| A protection that users and repositories must not weaken | Policy layer (this page) |
| Tell the model how to work: conventions, style, workflow | [Instructions](../concepts/instructions.md) and [skills](../concepts/skills.md). The concept page recommends keeping shared guidance there and keeping settings files minimal, because instructions and skills have shared file names and settings files do not ([Configuration concept](../concepts/configuration.md#portability)). |
| Allow, ask or deny a specific action | Permission rules, stored in config but designed per [Permissions and sandbox](permissions-and-sandbox.md) |
| Limit what an executed command can read, write or reach | Sandbox policy, see [Permissions and sandbox](permissions-and-sandbox.md) |
| An action that must run at a lifecycle point every time | [Hooks](hooks.md) |
| Which MCP servers or plugins may load | [MCP](../concepts/mcp.md), [Plugins](../concepts/plugins.md), with allowlists in the policy layer |
| A merge gate that does not depend on any agent config in the repository | CI, see [Automation](../concepts/automation.md) |

## Approaches

### Scope split

**What it is.** Each setting goes into the layer whose owner should control it: user, project (committed, active only after trust), project-local (CC only, uncommitted), invocation, policy.

**When it fits.** Every setup. The other approaches build on it.

**How, generalized.** The research proposes this split for both leads (inference from the vendor scope tables and the CVE history):

| Layer | Put here | Keep out |
| --- | --- | --- |
| User | Secret-path read denials, destructive-command denies or asks, personal MCP servers, telemetry opt-outs, a bypass-mode lock if you want one | Team-specific rules other people need |
| Project (committed) | Narrow allow rules for the project's own build and test commands, ask rules for `git push` and deploys, project hooks, the sandbox write paths and domains the build needs | Secrets, provider endpoints, credential helpers, broad allow rules |
| Project-local (CC only) | Experiments before promoting them to project; personal per-project overrides | Anything the team needs |
| Policy | Sandbox required, bypass disabled, MCP allowlist, telemetry destination, secret-path denies | Preferences users should be able to change |

**Claude Code.**

- Files: user `~/.claude/settings.json`, shared project `.claude/settings.json`, project-local `.claude/settings.local.json`, managed settings. CC's own scope table says the same: user for "Personal preferences: theme, editor mode, default model, your own permission rules", shared project for "Team permissions, hooks, plugins, and the environment variables the project needs", local for "Personal overrides for one project, and testing before you share", managed for "Security policy and compliance requirements" ([CC settings](https://code.claude.com/docs/en/settings)).
- Precedence, highest first: managed > `--settings`/CLI > project local > shared project > user. A project scalar beats a user scalar. List keys such as `permissions.allow` merge across files. A deny at any level blocks an allow at any other level ([CC settings](https://code.claude.com/docs/en/settings), [CC permissions](https://code.claude.com/docs/en/permissions)).
- Some restrictive keys win from lower scopes even over managed, for example `disableClaudeAiConnectors: true` and the lowest `maxEffortLevel` ([CC settings](https://code.claude.com/docs/en/settings)).
- A repository cannot start CC in `auto` or `bypassPermissions`; those `defaultMode` values in project files are ignored ([CC permission modes](https://code.claude.com/docs/en/permission-modes)).

**Codex.**

- Files: user `~/.codex/config.toml`, project `.codex/config.toml` in every directory from the project root to the cwd (closest wins), `--profile` overlay files, `requirements.toml` for policy ([Configuration concept](../concepts/configuration.md)).
- Project config loads only for trusted projects. An untrusted project's whole `.codex/` layer is ignored, including hooks and rules. Project config cannot set `openai_base_url`, `chatgpt_base_url`, `model_provider(s)`, `notify`, `profile` and others; it cannot "redirect credentials, alter host-owned app request metadata, change provider auth, select config profiles, or run machine-local notification/telemetry commands" ([Codex advanced config](https://learn.chatgpt.com/codex/config-advanced)).
- There is no project-local layer. Use user config or a `--profile` overlay for personal overrides.

**OpenCode.** Config layers from remote org defaults up to MDM; no trust gate is recorded; `OPENCODE_DISABLE_PROJECT_CONFIG` skips project config ([Configuration concept](../concepts/configuration.md)).

**Trade-offs.** CC merges list keys, so a trusted project file can *add* allow rules and sandbox `allowWrite` and `allowedDomains` entries (inference). Codex does not document array merging in general. OpenCode replaces arrays except `instructions` and `plugin`. In CC a user `false` cannot override a project `true`; only the local file can.

### Task profiles

**What it is.** An overlay selected per run, so read-only review, normal work and CI use different presets without editing the base config.

**When it fits.** Recurring tasks with different risk: exploration, editing, CI, review.

**How.**

- Codex: `--profile <name>` loads `~/.codex/<name>.config.toml` as an overlay above the base user config. `[profiles.<name>]` tables no longer work since 0.134.0 ([Codex advanced config](https://learn.chatgpt.com/codex/config-advanced)). Vendor preset combinations: standard `--sandbox workspace-write --ask-for-approval on-request`; read-only `--sandbox read-only --ask-for-approval on-request`; CI `--sandbox read-only --ask-for-approval never`; auto-review `on-request` plus `approvals_reviewer = "auto_review"` ([Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security)).
- CC: `--settings <file-or-json>` is the closest equivalent. The "Common setups" table lists Manual (`default`) for sensitive work, Manual plus Bash sandbox auto-allow for local iteration, `plan` to explore, `auto` for hands-off work, CI with `-p --permission-mode dontAsk --allowedTools "Bash(npm test)" "Read"`, and `--dangerously-skip-permissions` only with a container, VM or sandbox runtime as a non-root user ([CC permission modes](https://code.claude.com/docs/en/permission-modes)). Starter settings files are in [anthropics/claude-code examples/settings](https://github.com/anthropics/claude-code/tree/main/examples/settings).

**Trade-offs.** A trusted Codex project beats `--profile` for every key it sets, except keys a project cannot set ([Configuration concept](../concepts/configuration.md#portability)). CC has no named profiles.

### Policy layer

**What it is.** An administrator layer that forces values or restricts allowed values, and can restrict which sources other settings come from.

**When it fits.** Teams and fleets. Individuals can use parts of it (see [practice 4](#4-put-protections-that-must-not-be-weakened-in-the-policy-layer)).

**How.**

- CC: managed settings via `managed-settings.json` (plus `managed-settings.d/`), MDM, or server-managed settings ([Configuration concept](../concepts/configuration.md)). Source restrictions: `allowManagedPermissionRulesOnly`, `allowManagedHooksOnly`, `allowManagedReadPathsOnly`, `allowManagedDomainsOnly` ([CC permissions](https://code.claude.com/docs/en/permissions), [CC sandboxing](https://code.claude.com/docs/en/sandboxing)).
- Codex: two stacks. `requirements.toml` "enforces admin-controlled constraints users cannot override"; `managed_config.toml` "sets startup defaults users can modify". Requirements cover approval policy, approvals reviewer, automatic review policy, sandbox mode, permission profiles, web search mode, managed hooks, allowed MCP servers and plugin marketplace sources. Delivery: Agent Security cloud console (signed bundles), macOS MDM `com.openai.codex:requirements_toml_base64`, `/etc/codex/requirements.toml` ([Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration)).
- OpenCode: managed files in a system directory and macOS MDM domain `ai.opencode.managed` ([Configuration concept](../concepts/configuration.md)).

**Trade-offs.** A managed-settings file copied in by a repository Dockerfile can be changed by anyone with write access ([CC devcontainer](https://code.claude.com/docs/en/devcontainer)). Dev containers are "a convention rather than an enforcement boundary" ([CC sandbox environments](https://code.claude.com/docs/en/sandbox-environments)). CC Windows hosts exit under `failIfUnavailable`, so sandbox policy has to be delivered per OS ([CC sandboxing](https://code.claude.com/docs/en/sandboxing)).

### Restricted loading for untrusted repositories

**What it is.** Starting the harness with the project layer skipped, for repositories you did not write.

**When it fits.** Batch or CI runs over cloned or forked repositories, evaluating third-party code.

**How.**

- CC: `--setting-sources user`, `--bare`, `--settings '{"disableAllHooks": true}'`, and `disabledMcpjsonServers` ([CC permissions](https://code.claude.com/docs/en/permissions)). Directories added via `permissions.additionalDirectories` grant file access only and do not load that directory's configuration; `--add-dir` and `/add-dir` have listed exceptions ([CC permissions](https://code.claude.com/docs/en/permissions)).
- Codex: do not trust the project; untrusted projects skip all `.codex/` layers ([Codex advanced config](https://learn.chatgpt.com/codex/config-advanced)).
- OpenCode: `OPENCODE_DISABLE_PROJECT_CONFIG` ([Configuration concept](../concepts/configuration.md)).

**Trade-offs.** The run loses the team's project settings, including its deny and ask rules.

## Practices

### 1. Assign each setting to the scope that owns it

- **Why:** Layers differ in reach and trust. User settings apply to every project; project settings apply to everyone who clones the repository and only after trust; policy settings cannot be overridden.
- **How:** Follow the [scope split](#scope-split) table. Trail of Bits keeps secret-path denies and global MCP servers in the user layer, and only project-specific MCP servers in `.mcp.json` with `enableAllProjectMcpServers: false`, because "Project `.mcp.json` files live in git, so a compromised repo could ship malicious MCP servers".
- **Evidence:** [Vendor] [CC settings](https://code.claude.com/docs/en/settings); [Vendor] [Codex advanced config](https://learn.chatgpt.com/codex/config-advanced); [Practitioner] [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config).

### 2. Keep secrets, endpoints and credential helpers out of committed config

- **Why:** CVE-2026-21852 let a project-set `ANTHROPIC_BASE_URL` send the API key in plaintext headers to an attacker before trust confirmation. Codex blocks the same class by refusing provider and base-URL keys in project config. CC honors credential masking (`sandbox.credentials` `mask`, `network.tlsTerminate`, `allowPlaintextInject`) only from user settings, managed settings and `--settings`; since v2.1.246 project and local `credentials` entries are ignored entirely.
- **How:** Load API keys from a secret manager (Trail of Bits uses 1Password), not from config files. In dev containers, do not mount host secrets such as `~/.ssh` or cloud credential files; prefer repository-scoped or short-lived tokens passed through `containerEnv`, Codespaces secrets or workload identity.
- **Evidence:** [Advisory] [Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/); [Vendor] [Codex advanced config](https://learn.chatgpt.com/codex/config-advanced); [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing); [Vendor] [CC devcontainer](https://code.claude.com/docs/en/devcontainer); [Practitioner] [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config).

### 3. Review harness config as executable code

- **Why:** Hooks, MCP server definitions, environment variables and config redirects in repository files have executed code or leaked credentials in both leads (see [Security](#security)). Check Point: "The line between configuration and execution continues to blur, requiring us to treat project setup files with the same careful attention we apply to executable code".
- **How:**
  - Inspect `.claude/`, `.codex/`, `.mcp.json` and similar directories before opening a project, and review config changes in code review.
  - Require owner review (for example CODEOWNERS) on `.claude/`, `.codex/`, `.agents/`, `.mcp.json`, `AGENTS.md`/`CLAUDE.md`, `.devcontainer/` and CI workflow files. This is inference from the CVE history; no vendor doc names CODEOWNERS.
  - Read the trust dialog, which lists the rules being granted, instead of clicking through it (inference).
  - Do not treat `.mcp.json` as the full list of servers: servers at other scopes, claude.ai connectors and plugins add more.
  - In CC, audit or block in-session settings changes with `ConfigChange` hooks, and share approved permission configurations through version control.
  - Keep the harness updated.
- **Evidence:** [Advisory] [Check Point Research (Feb 2026)](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/); [Vendor] [CC security](https://code.claude.com/docs/en/security).

### 4. Put protections that must not be weakened in the policy layer

- **Why:** Anything in user or project files can be edited by whoever controls them. The s1ngularity malware (Aug 26, 2025) launched installed agent CLIs with bypass flags; the research infers that a policy setting is the only place that stops a local process from doing this.
- **How:**
  - CC managed settings: `{"sandbox": {"enabled": true, "failIfUnavailable": true, "allowUnsandboxedCommands": false}}`, `permissions.disableBypassPermissionsMode: "disable"`, `allowManagedPermissionRulesOnly`, `allowManagedHooksOnly`, `allowManagedDomainsOnly`, managed MCP configuration, and `sandbox.credentials` entries for `~/.aws`, `~/.ssh` and secret environment variables. Auto mode can be turned off by the organization.
  - Codex `requirements.toml`: `allowed_approval_policies = ["on-request"]`, `allowed_sandbox_modes = ["read-only","workspace-write"]`, `[rules] prefix_rules` with `decision = "prompt"` (admin rules can only be `prompt` or `forbidden`), `[mcp_servers.<id>] identity = { command = "..." }`, `[experimental_network] managed_allowed_domains_only = true`, `[permissions.filesystem]` deny-read globs, `[hooks]`, `[features]` pins.
  - Codex admin guidance: give every policy an owner and a business justification, test allowed and blocked workflows before rollout, keep `network_access = false` in managed defaults unless security review permits otherwise, validate `[[remote_sandbox_config]]` host overrides on deployed client versions.
  - Individuals: CC `disableBypassPermissionsMode` "works from any scope. A user can set it in their own settings to lock themselves out of bypass mode".
  - Deliver through MDM or server-managed settings, not a file a repository Dockerfile copies in.
- **Evidence:** [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing); [Vendor] [CC permissions](https://code.claude.com/docs/en/permissions); [Vendor] [CC security](https://code.claude.com/docs/en/security); [Vendor] [CC devcontainer](https://code.claude.com/docs/en/devcontainer); [Vendor] [Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration); [Advisory] (2025) [Wiz on s1ngularity](https://wiz.io/blog/s1ngularity-supply-chain-attack).

### 5. Filter secrets from subprocess environments explicitly

- **Why:** CC sandboxed commands inherit environment variables "including any secrets". For Codex, this repository's vendor notes record `ignore_default_excludes` defaulting to `true`, so names containing KEY, SECRET or TOKEN pass through ([Codex configuration](../vendors/codex/configuration.md)).
- **How:**
  - CC: set `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` to strip credentials from all subprocesses. Inside the sandbox, `sandbox.credentials.envVars` with `deny` unsets a variable before each sandboxed command, and `mask` replaces it with a per-session sentinel that the proxy swaps back only on requests to allowed hosts.
  - Codex: set `ignore_default_excludes = false` explicitly under `[shell_environment_policy]`, and use `exclude`/`filters` or `include_only`. "Includes don't restore variables that were already excluded."
  - Do not put secrets in the CC `env` block; it passes them to the session and every subprocess.
- **Evidence:** [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing); [Vendor] [Codex advanced config](https://learn.chatgpt.com/codex/config-advanced); [Vendor] via the [Codex vendor notes](../vendors/codex/configuration.md).

### 6. Use task profiles instead of editing the base config

- **Why:** Different tasks need different presets. A CI run needs no prompts and no network; a review needs no writes.
- **How:** See [task profiles](#task-profiles). Keep the CI profile minimal: read-only or an exact allowlist, no network (inference). Codex CI: `--sandbox read-only --ask-for-approval never`. CC CI: `-p --permission-mode dontAsk --allowedTools "Bash(npm test)" "Read"`. In Codex, move old `[profiles.<name>]` tables to `~/.codex/<name>.config.toml`.
- **Evidence:** [Vendor] [Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security); [Vendor] [CC permission modes](https://code.claude.com/docs/en/permission-modes); [Vendor] [Codex advanced config](https://learn.chatgpt.com/codex/config-advanced).

### 7. Turn off repository config for headless runs over untrusted repositories

- **Why:** CC `-p` and SDK runs never show the trust dialog. In a never-trusted folder, hooks, the `env` block, `apiKeyHelper`, and a project skill's hooks and `allowed-tools` are used, and `.mcp.json` servers connect without asking. Codex is stricter: untrusted projects skip the whole `.codex/` layer, and new or changed hooks are skipped until trusted by hash.
- **How:** For CC, start with `--setting-sources user` or `--bare`, add `--settings '{"disableAllHooks": true}'`, and set `disabledMcpjsonServers`. Setting `disableAllHooks` only in user settings is not enough, because project settings take precedence over user settings. Watch stderr for the "this workspace has not been trusted" warning, which lists skipped allow rules. For Codex, do not trust the project and do not pass `--dangerously-bypass-hook-trust`.
- **Evidence:** [Vendor] [CC permissions, "What runs before you trust a folder"](https://code.claude.com/docs/en/permissions); [Vendor] [Codex advanced config](https://learn.chatgpt.com/codex/config-advanced); [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks).

### 8. Keep personal overrides out of git

- **Why:** CC adds `**/.claude/settings.local.json` to the global git excludes file only the first time CC itself writes the file. A local file that is tracked in git, or whose `.claude` directory is a symlink, is treated as repository-supplied, and its allow rules wait for trust.
- **How:** Add a hand-created `settings.local.json` to `.gitignore`. Use the local file, not user settings, to override a project scalar in CC, because a project scalar beats a user scalar. In Codex, use user config or a `--profile` file.
- **Evidence:** [Vendor] [CC settings](https://code.claude.com/docs/en/settings); [Vendor] [CC permissions](https://code.claude.com/docs/en/permissions).

### 9. Pin the telemetry destination in policy and keep content logging off by default

- **Why:** Tool-decision events are the audit trail in both leads. Content logging is a privacy decision.
- **How:**
  - CC: enable with `CLAUDE_CODE_ENABLE_TELEMETRY=1` and OTLP exporters. Setting endpoint and headers in managed settings removes conflicting developer-set variables, so telemetry cannot be redirected. `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_DETAILS` and `OTEL_LOG_TOOL_CONTENT` are off by default.
  - Codex: `[otel]` is opt-in (`otlp-http`, `otlp-grpc`, `none`); a project cannot set it. Pin the exporter in managed config and keep `log_user_prompt = false` unless policy allows. Local history is in `~/.codex/history.jsonl`; `[history] persistence = "none"` disables it. Route telemetry to controlled collectors only and apply retention limits.
  - Inference: `OTEL_LOG_TOOL_DETAILS` (commands, paths) is the minimum useful for security review; logging full prompts needs a policy decision.
- **Evidence:** [Vendor] [CC monitoring](https://code.claude.com/docs/en/monitoring-usage); [Vendor] [Codex advanced config](https://learn.chatgpt.com/codex/config-advanced); [Vendor] [Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration); [Vendor] [Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security).

### 10. Verify the resolved config after every change and upgrade

- **Why:** Layers merge in vendor-specific ways, invalid entries can be skipped silently (CC `-p` skips bad entries), and precedence details change between versions: CC v2.1.207 changed local-file trust, v2.1.285 changed strict-sandbox precedence, Codex 0.134 changed profiles.
- **How:** CC: `/status` (setting sources), `/permissions` (rules by source file), `claude doctor`. Codex: `/debug-config`, `/status`, `codex doctor`, and `--strict-config` to error on unknown fields. OpenCode: `opencode debug config`. CC hot-reloads most settings; Codex and OpenCode need a new session. Run the [Verification](#verification) steps again after each harness upgrade.
- **Evidence:** [Vendor] via the [Configuration concept](../concepts/configuration.md); [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing); [Vendor] [Codex rules](https://learn.chatgpt.com/codex/rules).

## Anti-patterns

| Avoid | Do instead |
| --- | --- |
| API keys, `ANTHROPIC_BASE_URL`, provider endpoints or `apiKeyHelper` in committed files | User layer, secret manager, short-lived tokens ([practice 2](#2-keep-secrets-endpoints-and-credential-helpers-out-of-committed-config)) |
| Relying on Codex's default environment filtering | Set `ignore_default_excludes = false` and explicit filters ([practice 5](#5-filter-secrets-from-subprocess-environments-explicitly)) |
| Overriding a CC project `true` with a user `false` | Use `.claude/settings.local.json` |
| `[profiles.<name>]` tables or `profile =` in Codex config | `~/.codex/<name>.config.toml` with `--profile <name>` |
| `defaultMode: "bypassPermissions"` or `"auto"` in a project file | Ignored by CC; set modes per user or per run, and lock bypass in policy |
| Enforcing policy with a managed-settings file that a repository Dockerfile copies in | MDM or server-managed delivery |
| Reviewing only `.mcp.json` to know which MCP servers load | Check all scopes, connectors and plugins ([MCP concept](../concepts/mcp.md)) |
| Clicking through the trust dialog | Read the rules it lists before accepting |
| Scripting `claude -p` over cloned repositories with default settings | `--setting-sources user` or `--bare`, plus `disableAllHooks` via `--settings` |
| A hand-created `settings.local.json` that is not ignored by git | Add it to `.gitignore`; a tracked local file is treated as repository-supplied |

## Security

Every advisory below exploited configuration that ran *before or outside* the permission system. The research infers that verification should therefore focus on pre-trust and out-of-sandbox paths, not only on rule lists.

| Threat | Advisory | Mitigation |
| --- | --- | --- |
| Repository hooks run at session start without consent | (2025) CC GHSA-ph6w-f82w-28w6, CVSS 8.7: hooks in `.claude/settings.json` ran without confirmation. Reported 2025-07-21, fixed 2025-08-26 in 1.0.87 ([Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)) | Hooks now wait for workspace trust in interactive sessions; for `-p`, see [practice 7](#7-turn-off-repository-config-for-headless-runs-over-untrusted-repositories) |
| Repository MCP config starts servers before trust | (2025) CVE-2025-59536, CVSS 8.7: repository-controlled `enableAllProjectMcpServers`/`enabledMcpjsonServers` started MCP servers before the trust dialog. Fixed 2025-09-22 in 1.0.111 ([Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/), [GitLab advisory](https://advisories.gitlab.com/npm/@anthropic-ai/claude-code/CVE-2025-59536/)) | Keep `enableAllProjectMcpServers: false`; MCP allowlist in policy |
| Repository redirects the API endpoint and leaks the key | CVE-2026-21852: project-set `ANTHROPIC_BASE_URL` sent the API key in plaintext headers before trust. Reported 2025-10-28, fixed 2025-12-28, published 2026-01-21; fix defers network operations until consent ([Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)) | No endpoints in committed config; Codex refuses these keys from project config |
| Repository redirects the harness home | (2025) Codex CVE-2025-61260: a repository `.env` setting `CODEX_HOME=./.codex` plus `./.codex/config.toml` `mcp_servers` ran attacker commands at startup with no approval. Fixed by blocking project-level config redirects ([Check Point Research](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/), [NVD](https://nvd.nist.gov/vuln/detail/cve-2025-61260)) | Keep Codex updated; do not trust unknown projects |
| Agent edits its own config to grant itself more | (2025) CVE-2025-53773 (GitHub Copilot / VS Code, CVSS 7.8, Aug 2025): a prompt injection made the agent write `"chat.tools.autoApprove": true` into `.vscode/settings.json` ([Wiz](https://www.wiz.io/vulnerability-database/cve/cve-2025-53773)) | Keep protected paths protected: CC never auto-approves writes to `.claude`, `.vscode`, `.mcp.json` and shell rc files outside bypass; Codex keeps `.codex/`, `.agents/` and `.git` read-only inside writable roots. With CC filesystem isolation off and auto-allow on, a sandboxed command can write `~/.claude/settings.json`; keep filesystem isolation on. The CC sandbox runtime builds its Linux protected-path list once at launch; add `denyWrite` for other config paths ([CC sandboxing](https://code.claude.com/docs/en/sandboxing), [CC sandbox environments](https://code.claude.com/docs/en/sandbox-environments)) |
| Malware launches the CLI with bypass flags | (2025) s1ngularity/Nx npm compromise, Aug 26, 2025 ([Wiz](https://wiz.io/blog/s1ngularity-supply-chain-attack)) | Lock bypass in policy or user settings ([practice 4](#4-put-protections-that-must-not-be-weakened-in-the-policy-layer)); details on [Permissions and sandbox](permissions-and-sandbox.md#security) |
| Telemetry redirected by a developer or repository | — | Pin endpoint and headers in managed settings; Codex project config cannot set `otel` |
| Headless CC run uses repository hooks, `env`, `apiKeyHelper` and `.mcp.json` | Documented current behavior ([CC permissions](https://code.claude.com/docs/en/permissions)) | [Practice 7](#7-turn-off-repository-config-for-headless-runs-over-untrusted-repositories) |

Several fixes were delivered by forced updates (CC deprecated versions before 1.0.24 per the CVE-2025-55284 advisory text, [GitLab advisory](https://advisories.gitlab.com/pkg/npm/@anthropic-ai/claude-code/CVE-2025-55284/)). Keep harnesses current and auto-updating, except where a container pins a version on purpose (inference).

## Verification

1. **Layers loaded.** CC `/status` shows setting sources; Codex `/debug-config` and `/status`; OpenCode `opencode debug config`. Confirm the policy layer appears where expected.
2. **Rules by source.** CC `/permissions` lists rules by source file and has a "Recently denied" tab.
3. **Config health.** `claude doctor` and `codex doctor`. Run Codex with `--strict-config` to surface unknown fields, for example leftover `[profiles.*]` tables.
4. **Trust gate.** Clone a test repository containing hooks, a `.mcp.json`, `env.ANTHROPIC_BASE_URL` and a `.env` with `CODEX_HOME`. Confirm nothing runs before trust, also in `-p` and `codex exec` mode (inference from the CVE list). In CC `-p`, check stderr for "this workspace has not been trusted".
5. **Policy holds.** Start with `--dangerously-skip-permissions` or `--yolo` and confirm policy refuses it. Try to widen a managed-only key from a project file and confirm it has no effect.
6. **Telemetry.** CC: look for `claude_code.session.count` or a `user_prompt` event; run `claude --debug-file <path>` and check for `[3P telemetry]` errors. Confirm `tool_decision` deny events reach the collector.
7. **After upgrades.** Repeat steps 1 to 6; version-gated behavior changes often.

## Checklist

- [ ] User layer holds secret-path denies, personal MCP servers and personal preferences only.
- [ ] Committed project config contains no secrets, base URLs, provider settings or credential helpers.
- [ ] `settings.local.json` is git-ignored and not tracked.
- [ ] Changes to `.claude/`, `.codex/`, `.agents/`, `.mcp.json`, `AGENTS.md`, `.devcontainer/` and CI workflows need owner review.
- [ ] Policy layer (or user settings, for individuals) disables bypass mode.
- [ ] Policy is delivered via MDM, server-managed settings or a system file, not a repository file.
- [ ] Subprocess secret filtering is set explicitly: `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`, Codex `ignore_default_excludes = false`.
- [ ] Headless runs over third-party repositories use `--setting-sources user` or `--bare` with hooks disabled; Codex hook trust is not bypassed.
- [ ] Codex config has no `[profiles.*]` tables and passes `--strict-config`.
- [ ] Telemetry endpoint is pinned in policy; prompt logging is off unless a policy allows it.
- [ ] Diagnostics were run after the last harness upgrade.

## Open questions

- **Codex array merging** across layers is not documented.
- **CODEOWNERS or branch protection** for harness config is inference from the CVE history; no vendor document prescribes it.
- **CVE-2025-61260 fixed version.** The configuration research lists affected versions as "≤ 0.23.0"; the hooks research records "Fixed in 0.23.0 (2025-08-20)". Check [NVD](https://nvd.nist.gov/vuln/detail/cve-2025-61260) before relying on a version boundary.
- **Adoption and outcomes** of managed settings and requirements: no public data found.
- **SIEM detection content** over `tool_decision` events: none found from vendors.

## Sources

- [Configuration concept](../concepts/configuration.md)
- [Codex configuration (vendor notes)](../vendors/codex/configuration.md)
- [CC settings](https://code.claude.com/docs/en/settings)
- [CC permissions](https://code.claude.com/docs/en/permissions)
- [CC permission modes](https://code.claude.com/docs/en/permission-modes)
- [CC sandboxing](https://code.claude.com/docs/en/sandboxing)
- [CC sandbox environments](https://code.claude.com/docs/en/sandbox-environments)
- [CC devcontainer](https://code.claude.com/docs/en/devcontainer)
- [CC security](https://code.claude.com/docs/en/security)
- [CC monitoring](https://code.claude.com/docs/en/monitoring-usage)
- [anthropics/claude-code examples/settings](https://github.com/anthropics/claude-code/tree/main/examples/settings)
- [Codex advanced config](https://learn.chatgpt.com/codex/config-advanced)
- [Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration)
- [Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security)
- [Codex rules](https://learn.chatgpt.com/codex/rules)
- [Codex hooks](https://learn.chatgpt.com/docs/hooks)
- [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)
- [Check Point Research: CC project files, CVE-2025-59536 and CVE-2026-21852](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)
- [GitLab advisory CVE-2025-59536](https://advisories.gitlab.com/npm/@anthropic-ai/claude-code/CVE-2025-59536/)
- [GitLab advisory CVE-2025-55284](https://advisories.gitlab.com/pkg/npm/@anthropic-ai/claude-code/CVE-2025-55284/)
- [Check Point Research: Codex CLI CVE-2025-61260](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/)
- [NVD CVE-2025-61260](https://nvd.nist.gov/vuln/detail/cve-2025-61260)
- [Wiz: CVE-2025-53773](https://www.wiz.io/vulnerability-database/cve/cve-2025-53773)
- [Wiz: s1ngularity supply-chain attack](https://wiz.io/blog/s1ngularity-supply-chain-attack)
