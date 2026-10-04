# Permissions and sandbox

Codex limits what the agent can do with three mechanisms: an approval policy (when Codex asks the user before acting), a sandbox (what commands can read, write and reach over the network), and Starlark rules (which commands may run outside the sandbox). The sandbox is configured either with the legacy `sandbox_mode` or with the newer named permission profiles (beta); the two cannot be combined ([Config reference](https://developers.openai.com/codex/config-reference); [Permissions](https://developers.openai.com/codex/permissions)).

## Locations and scopes

| Setting | Where it lives |
|---|---|
| `approval_policy`, `approvals_reviewer`, `sandbox_mode`, `[sandbox_workspace_write]`, `default_permissions`, `[permissions.<name>]`, `[windows]`, `[auto_review]` | Any `config.toml` layer, see [configuration.md](configuration.md) |
| Project trust (`[projects."<path>"] trust_level`) | User `~/.codex/config.toml` ([Config reference](https://developers.openai.com/codex/config-reference)) |
| Rules (`*.rules`) | `rules/` next to each active config layer, for example `~/.codex/rules/default.rules`. Project `<repo>/.codex/rules/` loads only if the project is trusted ([Rules](https://developers.openai.com/codex/rules)) |
| Admin constraints | `requirements.toml`: `allowed_approval_policies`, `allowed_approvals_reviewers`, `allowed_sandbox_modes`, `allowed_permission_profiles`, `default_permissions`, `[rules] prefix_rules`, `[experimental_network]`, `permissions.filesystem.deny_read`, `guardian_policy_config`, `windows.allowed_sandbox_implementations` ([Config reference](https://developers.openai.com/codex/config-reference); [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)) |
| CLI | `-a/--ask-for-approval`, `-s/--sandbox`, `--add-dir <DIR>` (adds writable directories), `--approve-for-me`, `--dangerously-bypass-approvals-and-sandbox` (alias `--yolo`) (local CLI, `codex --help`) |

### Launch defaults

- Codex detects version control. Version-controlled folders get `Auto` (workspace-write plus on-request); other folders get `read-only`. Codex may start in read-only until the directory is trusted. The workspace includes the cwd and temporary directories such as `/tmp` ([Security](https://developers.openai.com/codex/agent-approvals-security)).
- The sample config comments `sandbox_mode` as "read-only (default)" ([Sample config](https://developers.openai.com/codex/config-sample)). See Limits and gotchas for the difference.
- `codex exec` defaults to a read-only sandbox ([Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)).

### Protected paths

Inside writable roots these paths stay read-only, recursively ([Security](https://developers.openai.com/codex/agent-approvals-security)):

- `<root>/.git` (directory or file, plus the resolved gitdir for pointer files)
- `<root>/.agents` (if it is a directory)
- `<root>/.codex` (if it is a directory)
- `.aws` directories under writable roots, since 0.159.0 (PR #48176) ([Changelog](https://developers.openai.com/codex/changelog))

Inference: this protection explains why `git commit` and edits to `.codex/` often trigger approval even in workspace-write.

## Format

### `approval_policy`

| Value | Status | Meaning |
|---|---|---|
| `on-request` | Current, default | The model decides when to ask ([Sample config](https://developers.openai.com/codex/config-sample)). Use for interactive runs |
| `never` | Current | Never ask. Use for non-interactive runs |
| `{ granular = { ... } }` | Current | Per-category control, see below |
| `untrusted` | Retired | "Codex and ChatGPT Work no longer support `approval_policy = "untrusted"`. The retired setting can prevent either client from starting." ([Security](https://developers.openai.com/codex/agent-approvals-security)) |
| `on-failure` | Deprecated | Use `on-request` or `never` ([Config reference](https://developers.openai.com/codex/config-reference)) |

The CLI help lists only `on-request` and `never` for `-a/--ask-for-approval` (local CLI).

**Replacing `untrusted`.** Remove it from user and project config, profile files, startup scripts and managed defaults. To keep stricter approvals, omit `approval_policy` and set `[projects."/path"] trust_level = "untrusted"` in the user config. Commands then need approval unless a rule allows them, and project-local config is disabled. An explicit `on-request` overrides this, and managed `allowed_approval_policies` must include `untrusted` to permit it ([Security](https://developers.openai.com/codex/agent-approvals-security); [Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)).

**Granular sub-keys.** Each key set to `true` lets the prompt appear; `false` rejects automatically ([Config reference](https://developers.openai.com/codex/config-reference)):

| Key | Prompt category |
|---|---|
| `sandbox_approval` | Sandbox escalation |
| `rules` | Execpolicy `prompt` rules |
| `mcp_elicitations` | MCP elicitations |
| `request_permissions` | The `request_permissions` tool |
| `skill_approval` | Skill scripts |

### `approvals_reviewer` (auto-review)

| Key | Meaning | Default |
|---|---|---|
| `approvals_reviewer` | `user` or `auto_review`. Auto-review sends eligible approval requests to a reviewer subagent; it does not change the sandbox boundary | `user` |
| `[auto_review] policy`, `extra_policy` | Local policy text for the reviewer | |
| `guardian_policy_config`, `guardian_extra_policy` (managed) | Take precedence over the local policy | |

Admins restrict the reviewer with `allowed_approvals_reviewers`. Reviewer failures fail closed ([Security](https://developers.openai.com/codex/agent-approvals-security); [Config reference](https://developers.openai.com/codex/config-reference)). `--approve-for-me` routes approval requests through automatic review using the workspace-write sandbox (local CLI).

### `sandbox_mode` (legacy, still primary in the docs)

| Value | Notes |
|---|---|
| `read-only` | Default per the sample config; default for `codex exec` |
| `workspace-write` | Writes allowed in the workspace (cwd, `writable_roots`, temp directories such as `/tmp`), except protected paths; network off by default |
| `danger-full-access` | Suggested inside Docker containers that block bwrap/seccomp ([Security](https://developers.openai.com/codex/agent-approvals-security)) |

`[sandbox_workspace_write]` keys ([Config reference](https://developers.openai.com/codex/config-reference); [Advanced config](https://developers.openai.com/codex/config-advanced)):

| Key | Meaning | Default |
|---|---|---|
| `writable_roots` | Array of extra writable directories | |
| `network_access` | Allow network access | `false` |
| `exclude_tmpdir_env_var` | Exclude `$TMPDIR` from writable roots | |
| `exclude_slash_tmp` | Exclude `/tmp` from writable roots | |

`--dangerously-bypass-approvals-and-sandbox` (alias `--yolo`) removes both sandbox and approvals. It is intended only for externally sandboxed environments ([Security](https://developers.openai.com/codex/agent-approvals-security)).

### Permission profiles (beta)

Built-in profiles: `:read-only`, `:workspace` (writes in workspace roots and system temp directories) and `:danger-full-access`. Custom profiles are `[permissions.<name>]` tables, selected with `default_permissions = "<name>"` ([Permissions](https://developers.openai.com/codex/permissions)).

| Key | Meaning | Default |
|---|---|---|
| `description` | Profile description | |
| `extends` | `:read-only`, `:workspace` or another named profile. `:danger-full-access` and cycles are not allowed | |
| `workspace_roots."<path>" = true` | Adds a workspace root | |
| `filesystem."<path-or-glob-or-token>"` | `read`, `write` or `deny`. Tokens include `:minimal`, `:root`, `:workspace_roots` (with nested subpaths) | |
| `filesystem.glob_scan_max_depth` | Glob scan depth | |
| `network.enabled` | Enable network | |
| `network.domains` | Domain rules (`allow`/`deny`) | |
| `network.unix_sockets` | Unix socket access | |
| `network.mode` | `limited` or `full` | |
| `network.proxy_url` | HTTP proxy URL | `http://127.0.0.1:3128` |
| `network.socks_url` | SOCKS URL | `http://127.0.0.1:8081` |
| `enable_socks5`, `enable_socks5_udp` | SOCKS5 support | `true` |
| `allow_local_binding` | Allow local and private destinations | |
| `allow_upstream_proxy` | Allow an upstream proxy | |
| `dangerously_allow_*` | Dangerous overrides | |

Sources: [Permissions](https://developers.openai.com/codex/permissions); [Config reference](https://developers.openai.com/codex/config-reference).

Filesystem precedence: more specific paths override broader ones. For the same path, `deny` > `write` > `read`. Profiles merge across config layers by name; for example `/etc/codex/config.toml` and `~/.codex/config.toml` can each add `workspace_roots` to the same profile ([Permissions](https://developers.openai.com/codex/permissions)).

### Network domain rules

Domain rules are allowlist-first ([Security](https://developers.openai.com/codex/agent-approvals-security)):

| Pattern | Matches |
|---|---|
| `example.com` | That exact host |
| `*.example.com` | Subdomains only |
| `**.example.com` | Apex plus subdomains |
| `*` | Everything; allowed in allow rules only |

Deny always wins. Local and private destinations are blocked unless `allow_local_binding = true` or an exact `localhost`/IP rule exists. Best-effort DNS-rebinding checks apply.

### Windows

`[windows] sandbox = "elevated"` (recommended), `"unelevated"` (fallback without admin rights) or `"mxc"`, plus `sandbox_private_desktop` (default `true`). Admins can constrain this with `windows.allowed_sandbox_implementations` ([Config basics](https://developers.openai.com/codex/config-basic); [Security](https://developers.openai.com/codex/agent-approvals-security); [Config reference](https://developers.openai.com/codex/config-reference)). The slash commands `/setup-default-sandbox` and `/sandbox-add-read-dir` exist on Windows only ([Slash commands](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)).

### Rules (execpolicy, experimental)

Rules control which commands Codex can run outside the sandbox. They are Starlark files ([Rules](https://developers.openai.com/codex/rules)).

`prefix_rule(...)` arguments:

| Argument | Meaning | Default |
|---|---|---|
| `pattern` | List of command tokens. Each element is a literal or a union such as `["view","list"]` | required |
| `decision` | `allow`, `prompt` or `forbidden` | `allow` |
| `justification` | Reason shown to the user | |
| `match` | Inline test commands that must match; checked at load | |
| `not_match` | Inline test commands that must not match; checked at load | |

Admin rules in `requirements.toml`: `[rules] prefix_rules = [{ pattern = [{ token = "rm" }], decision = "forbidden", justification = "..." }]`. Pattern elements use `token` or `any_of`. Only `prompt` and `forbidden` are allowed. Admin rules merge with `.rules` files, and the most restrictive decision wins ([Managed config](https://developers.openai.com/codex/enterprise/managed-configuration); [Config reference](https://developers.openai.com/codex/config-reference)).

## Loading and invocation

### Approvals and rules

- When several rules match, the most restrictive decision wins: `forbidden` > `prompt` > `allow` ([Rules](https://developers.openai.com/codex/rules)).
- Shell wrappers: a `bash|zsh|sh -c/-lc` script made only of plain words joined by `&&`, `||`, `;` or `|` is split with tree-sitter, and each command is evaluated on its own. Scripts with redirection, substitution, variables, globs or control flow are evaluated as one invocation ([Rules](https://developers.openai.com/codex/rules)).
- Choosing "allow" in the TUI writes a rule to `~/.codex/rules/default.rules`. Smart approvals (default) may propose a `prefix_rule` during escalation ([Rules](https://developers.openai.com/codex/rules)).
- Destructive app and MCP tool calls always require approval when the tool advertises a destructive annotation, unless it advertises a read annotation ([Security](https://developers.openai.com/codex/agent-approvals-security)).
- Subagents inherit the parent sandbox policy and live runtime overrides; see [subagents.md](subagents.md). Hooks can decide approvals through the `PermissionRequest` event; see [hooks.md](hooks.md).
- `/permissions` (TUI) and `--yolo` are live runtime overrides; subagents inherit them ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md); [Slash commands](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)).

### Legacy vs profiles

"Configure either `default_permissions` and `[permissions]`, or `sandbox_mode` / `sandbox_workspace_write`, but not both." If `sandbox_mode` appears in any loaded config, or `--sandbox` is passed, the legacy settings win. The exception is managed `allowed_permission_profiles`, which forces profiles ([Permissions](https://developers.openai.com/codex/permissions)).

### Network

- Network is off by default in `workspace-write`. Turn it on with `[sandbox_workspace_write] network_access = true` ([Security](https://developers.openai.com/codex/agent-approvals-security)).
- `features.network_proxy` (experimental, off by default) enforces domain rules but does not grant network access ([Security](https://developers.openai.com/codex/agent-approvals-security)):

| Network access | Proxy | Result |
|---|---|---|
| off | on | Still off |
| on | off | Unrestricted direct access |
| on | on | Filtered by policy |

- The proxy does not filter web search, apps/connectors, MCP server connections, browser or Computer Use, cloud tasks, or the client's own model and auth requests ([Security](https://developers.openai.com/codex/agent-approvals-security)). Use the `mcp_servers` allowlist for MCP ([mcp.md](mcp.md)).
- Admin `[experimental_network]` in `requirements.toml` can start the proxy without the user feature flag, but cannot turn on network when the sandbox keeps it off ([Security](https://developers.openai.com/codex/agent-approvals-security)).

### Platform implementations

| Platform | Implementation | Notes |
|---|---|---|
| macOS | Seatbelt via `sandbox-exec` with a profile matching the mode | A curated macOS platform policy is appended for restricted reads ([Security](https://developers.openai.com/codex/agent-approvals-security)) |
| Linux | `bwrap` plus `seccomp` | Install `bubblewrap`. Codex uses the first `bwrap` on `PATH` and warns at startup if it is missing. Ubuntu 25.04+ needs the `bwrap-userns-restrict` AppArmor profile ([Sandboxing](https://developers.openai.com/codex/concepts/sandboxing)). Docker containers may block bwrap/seccomp; then use `danger-full-access` inside the container ([Security](https://developers.openai.com/codex/agent-approvals-security)) |
| WSL2 | Linux sandbox | |
| WSL1 | Unsupported from 0.115 | Supported through 0.114; dropped with the move to bwrap ([Security](https://developers.openai.com/codex/agent-approvals-security)) |
| Windows | Native sandbox: `elevated`, `unelevated` or `mxc` | See Windows above |

Feature flags (local `codex features list`): `use_legacy_landlock` is deprecated; `use_linux_sandbox_bwrap` is removed because bwrap is now the only path.

### Testing

- Sandbox: `codex sandbox macos|linux|windows [--permissions-profile <name>] [--log-denials] [COMMAND]...` (aliases `seatbelt`, `landlock`; also reachable as `codex debug`) ([Security](https://developers.openai.com/codex/agent-approvals-security)). See Limits and gotchas for the local CLI discrepancy.
- Rules: `codex execpolicy check --pretty --rules <file> -- <cmd...>` prints JSON ([Rules](https://developers.openai.com/codex/rules)); the command exists in local 0.159.2.

## Example

```toml
# Legacy sandbox mode
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true
```

```toml
# Permission profile (beta); do not combine with sandbox_mode
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

Sources: [Advanced config](https://developers.openai.com/codex/config-advanced); [Permissions](https://developers.openai.com/codex/permissions); [Rules](https://developers.openai.com/codex/rules).

## Limits and gotchas

- **Retired and deprecated approval values.** A list of `untrusted`, `on-request`, `on-failure` and `never` is outdated. Current Codex accepts only `on-request`, `never` and `granular`. `untrusted` survives only as a project trust level, and leaving `approval_policy = "untrusted"` in a config can stop the client from starting ([Config reference](https://developers.openai.com/codex/config-reference); [Security](https://developers.openai.com/codex/agent-approvals-security)). **Gap:** no release date was found for the retirement of `untrusted` or the deprecation of `on-failure`.
- **`codex exec --full-auto`** is a deprecated compatibility flag that prints a warning. Use `--sandbox workspace-write` ([CLI reference](https://developers.openai.com/codex/cli/reference); [Security](https://developers.openai.com/codex/agent-approvals-security)).
- **Contradiction: default sandbox.** The sample config says "read-only (default)"; the security page describes VCS-detected `Auto` (workspace-write plus on-request). These likely refer to the config default versus the onboarding/trust-flow recommendation; this is not confirmed.
- **Contradiction: `codex sandbox` subcommands.** On local 0.159.2, `codex sandbox --help` shows no platform subcommands, and `codex sandbox macos --help` tried to run `macos` under `sandbox-exec`. `codex debug` lists only `models`, `app-server` and `prompt-input`. The docs describe `codex sandbox macos|linux|windows`. Unresolved.
- **Legacy wins over profiles.** One `sandbox_mode` in any loaded layer, or `--sandbox` on the command line, disables permission profiles unless an admin sets `allowed_permission_profiles` ([Permissions](https://developers.openai.com/codex/permissions)).
- **Inference: profiles are the successor.** Enterprise docs say to "use permission profiles ... instead of building new deployments around legacy sandbox-mode restrictions" ([Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)), but user-facing docs still teach `sandbox_mode` first.
- **`allowed_permission_profiles`** requires Codex 0.138.0 or later. Once present, profiles not listed are denied ([Config reference](https://developers.openai.com/codex/config-reference)).
- **The proxy is not a full egress boundary.** It does not cover web search, connectors, MCP, browser or Computer Use, or cloud tasks ([Security](https://developers.openai.com/codex/agent-approvals-security)).
- **Rules are experimental** ([Rules](https://developers.openai.com/codex/rules)).

## Sources

- https://developers.openai.com/codex/config-reference
- https://developers.openai.com/codex/config-sample
- https://developers.openai.com/codex/config-basic
- https://developers.openai.com/codex/config-advanced
- https://developers.openai.com/codex/agent-approvals-security
- https://developers.openai.com/codex/concepts/sandboxing
- https://developers.openai.com/codex/permissions
- https://developers.openai.com/codex/rules
- https://developers.openai.com/codex/enterprise/managed-configuration
- https://developers.openai.com/codex/cli/reference
- https://developers.openai.com/codex/changelog
- https://learn.chatgpt.com/docs/non-interactive-mode.md
- https://learn.chatgpt.com/docs/developer-commands.md?surface=cli
- https://learn.chatgpt.com/docs/agent-configuration/subagents.md
