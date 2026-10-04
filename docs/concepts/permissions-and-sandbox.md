# Permissions and sandbox

Permissions decide, for each tool call, whether the harness runs it, asks the user first, or refuses it. The sandbox is a separate, OS-level boundary that limits what executed commands can read, write, and reach on the network, whatever was approved. Together they let an agent work without a prompt for every step while limiting the damage of a wrong or injected action.

The two parts are kept on one page because both leads couple them: Codex picks its approval behavior together with a sandbox mode, and Claude Code's sandbox changes which commands need a prompt (auto-allow mode).

## Comparison

### Approvals and rules

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Decisions | `allow`, `ask`, `deny` ([CC](../vendors/claude-code/permissions-and-sandbox.md#rule-syntax)) | Rules: `allow`, `prompt`, `forbidden`; MCP tools: `auto`, `prompt`, `writes`, `approve` ([Codex](../vendors/codex/permissions-and-sandbox.md#rules-execpolicy-experimental), [MCP](../vendors/codex/mcp.md#keys-for-both-transports)) | `allow`, `ask`, `deny` ([OC](../vendors/opencode/permissions-and-sandbox.md#actions)) |
| Rule targets | Any tool: `Bash(...)`, `Read(...)`, `Edit(...)`, `WebFetch(domain:...)`, `mcp__...`, `Agent(...)`, `Skill(...)` ([CC](../vendors/claude-code/permissions-and-sandbox.md#rule-syntax)) | Shell commands (Starlark `prefix_rule`); MCP tools per tool; files and network through the sandbox profile ([Codex](../vendors/codex/permissions-and-sandbox.md#rules-execpolicy-experimental)) | One key per tool (`read`, `edit`, `bash`, `task`, `skill`, MCP names, ...) ([OC](../vendors/opencode/permissions-and-sandbox.md#keys)) |
| Command matching | Glob over the command string; compound commands split on `&&`, `\|\|`, `;`, `\|`, ...; wrappers like `timeout` stripped ([CC](../vendors/claude-code/permissions-and-sandbox.md#bash-and-powershell)) | Token-prefix `pattern`; simple `sh -c` scripts split with tree-sitter; complex scripts evaluated whole ([Codex](../vendors/codex/permissions-and-sandbox.md#approvals-and-rules)) | Glob over the parsed command; `"grep"` does not match `grep x` ([OC](../vendors/opencode/permissions-and-sandbox.md#pattern-syntax)) |
| Conflict resolution | deny, then ask, then allow; first match decides; specificity irrelevant; deny in any scope beats allow in any scope ([CC](../vendors/claude-code/permissions-and-sandbox.md#rule-evaluation)) | Most restrictive wins: `forbidden` > `prompt` > `allow`; admin rules merge with file rules ([Codex](../vendors/codex/permissions-and-sandbox.md#approvals-and-rules)) | Last matching rule wins; order matters ([OC](../vendors/opencode/permissions-and-sandbox.md#pattern-syntax)) |
| Rule location | `permissions` key in any settings file; lists merge ([CC](../vendors/claude-code/permissions-and-sandbox.md#locations-and-scopes)) | `rules/*.rules` next to each config layer; project rules only if trusted ([Codex](../vendors/codex/permissions-and-sandbox.md#locations-and-scopes)) | `permission` key in any config layer, per agent, or `OPENCODE_PERMISSION` ([OC](../vendors/opencode/permissions-and-sandbox.md#locations-and-scopes)) |
| Remembered approvals | "Don't ask again" saves rules (up to 5 per compound command) ([CC](../vendors/claude-code/permissions-and-sandbox.md#bash-and-powershell)) | TUI "allow" writes to `~/.codex/rules/default.rules`; smart approvals may propose a rule ([Codex](../vendors/codex/permissions-and-sandbox.md#approvals-and-rules)) | "always" approves suggested patterns for the session only ([OC](../vendors/opencode/permissions-and-sandbox.md#actions)) |
| Approval presets | Modes: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` ([CC](../vendors/claude-code/permissions-and-sandbox.md#permission-modes)) | `approval_policy` (`on-request`, `never`, `granular`) combined with `sandbox_mode` or a permission profile ([Codex](../vendors/codex/permissions-and-sandbox.md#approval_policy)) | Defaults per key; `--auto` approves anything that would ask ([OC](../vendors/opencode/permissions-and-sandbox.md#loading-and-invocation)) |
| Launch default | `auto` in terminal and VS Code since v2.1.283; `-p`/SDK: `default` or `auto` ([CC](../vendors/claude-code/permissions-and-sandbox.md#starting-mode-and-switching)) | Version-controlled folder: workspace-write + `on-request`; else read-only; `codex exec`: read-only. Sample config says read-only (contradiction) ([Codex](../vendors/codex/permissions-and-sandbox.md#launch-defaults)) | Most tools `allow`; `external_directory` and `doom_loop` `ask`; `.env` reads `deny` ([OC](../vendors/opencode/permissions-and-sandbox.md#keys)) |
| Automated reviewer | `auto` mode: a classifier reviews actions; `autoMode` rules (`environment`, `allow`, `soft_deny`, `hard_deny`), user or managed scope ([CC](../vendors/claude-code/permissions-and-sandbox.md#permission-keys)) | `approvals_reviewer = "auto_review"`: a reviewer subagent; `[auto_review] policy`; fails closed ([Codex](../vendors/codex/permissions-and-sandbox.md#approvals_reviewer-auto-review)) | None |
| Unattended runs | `dontAsk`: anything that would prompt is denied ([CC](../vendors/claude-code/permissions-and-sandbox.md#permission-modes)) | `never`: never ask ([Codex](../vendors/codex/permissions-and-sandbox.md#approval_policy)) | `opencode run --auto` ([OC](../vendors/opencode/permissions-and-sandbox.md#loading-and-invocation)) |
| Full bypass | `bypassPermissions`, `--dangerously-skip-permissions`; refused as root ([CC](../vendors/claude-code/permissions-and-sandbox.md#limits-and-gotchas)) | `--dangerously-bypass-approvals-and-sandbox` (`--yolo`) ([Codex](../vendors/codex/permissions-and-sandbox.md#sandbox_mode-legacy-still-primary-in-the-docs)) | `"permission": "allow"` ([OC](../vendors/opencode/permissions-and-sandbox.md#format)) |
| Never auto-approved | Explicit ask rules, `rm` on critical paths, `requiresUserInteraction` MCP tools, protected-path writes ([CC](../vendors/claude-code/permissions-and-sandbox.md#never-auto-approved-in-any-mode)) | Destructive-annotated app and MCP tools ([Codex](../vendors/codex/permissions-and-sandbox.md#approvals-and-rules)) | Explicit `deny` survives `--auto` ([OC](../vendors/opencode/permissions-and-sandbox.md#loading-and-invocation)) |
| Protected paths | Writes to `.git`, `.claude`, `.vscode`, `.idea`, `.husky`, ..., shell rc files, `.mcp.json` are never auto-approved ([CC](../vendors/claude-code/permissions-and-sandbox.md#protected-paths)) | `.git`, `.agents`, `.codex`, `.aws` stay read-only inside writable roots ([Codex](../vendors/codex/permissions-and-sandbox.md#protected-paths)) | Only the default `.env` read deny ([OC](../vendors/opencode/permissions-and-sandbox.md#keys)) |
| Extra directories | `--add-dir`, `/add-dir`, `permissions.additionalDirectories` ([CC](../vendors/claude-code/permissions-and-sandbox.md#working-directories)) | `--add-dir`, `writable_roots`, profile `workspace_roots` ([Codex](../vendors/codex/permissions-and-sandbox.md#locations-and-scopes)) | `external_directory` patterns ([OC](../vendors/opencode/permissions-and-sandbox.md#external_directory)) |
| Hook decision | `PreToolUse` can deny, ask, or allow, but never overrides deny or ask rules ([CC](../vendors/claude-code/permissions-and-sandbox.md#rule-evaluation)) | `PermissionRequest` hook ([Codex](../vendors/codex/permissions-and-sandbox.md#approvals-and-rules)) | `permission.ask` hook; throw in `tool.execute.before` ([OC](../vendors/opencode/permissions-and-sandbox.md#loading-and-invocation)) |
| Admin enforcement | Managed rules cannot be overridden; `allowManagedPermissionRulesOnly`; `disableBypassPermissionsMode`; `disableAutoMode` ([CC](../vendors/claude-code/permissions-and-sandbox.md#permission-keys)) | `allowed_approval_policies`, `allowed_sandbox_modes`, `allowed_permission_profiles`, admin `prefix_rules` (`prompt`/`forbidden` only), `deny_read` ([Codex](../vendors/codex/permissions-and-sandbox.md#locations-and-scopes)) | Managed config layers ([OC](../vendors/opencode/configuration.md#layers)) |
| Inspect | `/permissions` dialog by source file ([CC](../vendors/claude-code/permissions-and-sandbox.md#cli-and-slash-commands)) | `/permissions`; `codex execpolicy check` ([Codex](../vendors/codex/permissions-and-sandbox.md#testing)) | Not recorded |

### Sandbox

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Exists | Yes; off by default; `sandbox.enabled` or `/sandbox` ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-coverage)) | Yes; always selected through `sandbox_mode` or a permission profile ([Codex](../vendors/codex/permissions-and-sandbox.md#sandbox_mode-legacy-still-primary-in-the-docs)) | None recorded in the notes ([OC](../vendors/opencode/permissions-and-sandbox.md)) |
| Config shape | One `sandbox` object ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-keys)) | Legacy `sandbox_mode` + `[sandbox_workspace_write]`, or named `[permissions.<name>]` profiles (beta); not both ([Codex](../vendors/codex/permissions-and-sandbox.md#legacy-vs-profiles)) | — |
| What it confines | Bash, PowerShell, Monitor commands and children; not file tools, hooks, local MCP servers, status line ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-coverage)) | Commands Codex runs; rules decide what runs outside it ([Codex](../vendors/codex/permissions-and-sandbox.md#rules-execpolicy-experimental)) | — |
| macOS / Linux | Seatbelt / bubblewrap + socat ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-coverage)) | Seatbelt / bubblewrap + seccomp ([Codex](../vendors/codex/permissions-and-sandbox.md#platform-implementations)) | — |
| Windows | Native: unsandboxed; WSL2: Linux sandbox ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-coverage)) | Native sandbox (`elevated`, `unelevated`, `mxc`); WSL1 unsupported ([Codex](../vendors/codex/permissions-and-sandbox.md#platform-implementations)) | — |
| Default writes | cwd, per-user temp dir, added dirs ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-coverage)) | `read-only`: none; `workspace-write`: cwd, `writable_roots`, `/tmp`, `$TMPDIR` ([Codex](../vendors/codex/permissions-and-sandbox.md#sandbox_mode-legacy-still-primary-in-the-docs)) | — |
| Default reads | Whole machine, including `~/.ssh` ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-coverage)) | Not stated for legacy modes; profiles can set `read`/`deny` per path ([Codex](../vendors/codex/permissions-and-sandbox.md#permission-profiles-beta)) | — |
| Read denies | `filesystem.denyRead`, `allowRead` re-opens ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-keys)) | Profile `filesystem."<path>" = "deny"`; admin `permissions.filesystem.deny_read` ([Codex](../vendors/codex/permissions-and-sandbox.md#permission-profiles-beta)) | `read` permission patterns ([OC](../vendors/opencode/permissions-and-sandbox.md#keys)) |
| Path precedence | Narrower `allowRead` wins inside a `denyRead` region ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-keys)) | More specific path wins; same path: `deny` > `write` > `read` ([Codex](../vendors/codex/permissions-and-sandbox.md#permission-profiles-beta)) | — |
| Network default | No direct route; HTTP/SOCKS proxy with an empty domain allowlist ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-coverage)) | Off in `workspace-write`; `network_access = true` gives unrestricted access ([Codex](../vendors/codex/permissions-and-sandbox.md#network)) | — |
| Domain filtering | `network.allowedDomains`, `deniedDomains`; `WebFetch(domain:...)` rules merge in ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-keys)) | `features.network_proxy` (experimental) with `network.domains`; deny wins; `*.x` subdomains, `**.x` apex + subdomains ([Codex](../vendors/codex/permissions-and-sandbox.md#network-domain-rules)) | `webfetch` is action-only, no URL patterns ([OC](../vendors/opencode/permissions-and-sandbox.md#keys)) |
| Escape path | `dangerouslyDisableSandbox` retry; `excludedCommands`; `allowUnsandboxedCommands: false` disables the retry ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-keys)) | Sandbox escalation through approval (`sandbox_approval`); `allow` rules run commands outside the sandbox ([Codex](../vendors/codex/permissions-and-sandbox.md#approval_policy)) | — |
| Prompts inside the sandbox | Auto-allow mode (default): sandboxed commands run without prompts; deny and content-scoped ask rules still apply ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-coverage)) | `on-request`: the model decides when to ask ([Codex](../vendors/codex/permissions-and-sandbox.md#approval_policy)) | — |
| Sandbox unavailable | Runs unsandboxed unless `failIfUnavailable: true` ([CC](../vendors/claude-code/permissions-and-sandbox.md#limits-and-gotchas)) | Linux: startup warning if `bwrap` is missing; in Docker use `danger-full-access` ([Codex](../vendors/codex/permissions-and-sandbox.md#platform-implementations)) | — |

## Generalized model

**Action request.** A tool name plus its input (command line, file path, URL, MCP tool name, subagent name).

**Decision.** `allow` (run), `ask` (prompt the user or a reviewer), or `deny` (refuse and tell the model).

**Evaluation pipeline** for each request:

1. **Policy rules** from the administrator. Highest authority.
2. **Rules** from user and project configuration: patterns per tool or per command prefix, each with a decision. Across all sources, the most restrictive matching decision wins (deny over ask over allow).
3. **Hooks** may return a decision. In Claude Code they cannot weaken a deny or ask rule.
4. **Protected categories** are never auto-approved: writes to the harness's own config directories and to `.git`, destructive operations, and tools the server marks as requiring a user.
5. **Approval preset** decides requests no rule matched (see table below).
6. **Automated reviewer**, if enabled, answers the prompt instead of the user, using a policy text.
7. **User prompt.** The answer can be remembered as a new rule.

**Approval presets.** Named autonomy levels. The mapping is approximate because the leads split the axes differently: Claude Code uses one mode, Codex combines an approval policy with a sandbox mode.

| Preset | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Read-only, ask before changes | `default` (or `plan`) | `sandbox_mode = "read-only"` + `on-request` | `edit: ask`, `bash: ask` |
| Edit the workspace freely, ask for the rest | `acceptEdits` | `workspace-write` + `on-request` | default rules |
| Reviewer answers prompts | `auto` | `approvals_reviewer = "auto_review"` | — |
| Unattended, never prompt | `dontAsk` (denies what would prompt) | `never` (gap: the pages do not say what happens to a request that would need approval) | `--auto` (approves what would ask) |
| No limits | `bypassPermissions` | `--yolo` | `"permission": "allow"` |

**Sandbox policy.** Applied by the operating system to processes the agent starts.

- **Filesystem:** writable roots (working directory, temp, added directories), read denials, and protected paths that stay read-only even inside writable roots. The more specific path wins.
- **Network:** off, filtered by a local proxy with a domain allowlist (deny wins), or unrestricted.
- **Escalation:** a command that fails in the sandbox can be re-run outside it, but only through an approval or an explicit rule. An administrator can turn escalation off.
- **Coverage:** shell commands and their children. MCP servers and other harness-internal processes are outside it in both leads.

**Admin constraints.** Allowed preset values, forced rules, and a switch that removes the bypass preset.

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Rule | `permissions.allow/ask/deny` entry | `prefix_rule(...)` | `permission` entry |
| Decision `allow`/`ask`/`deny` | `allow`/`ask`/`deny` | `allow`/`prompt`/`forbidden` | `allow`/`ask`/`deny` |
| Rule file | Settings files | `rules/*.rules` | Config files |
| Approval preset | Permission mode | `approval_policy` + sandbox mode or profile | `--auto`, defaults |
| Automated reviewer | `auto` mode classifier, `autoMode` | `approvals_reviewer = "auto_review"`, `[auto_review]` | — |
| Hook decision point | `PreToolUse` | `PermissionRequest` | `permission.ask` |
| Sandbox policy | `sandbox` object | `sandbox_mode` / `[permissions.<name>]` | — |
| Writable root | `sandbox.filesystem.allowWrite`, `--add-dir` | `writable_roots`, `workspace_roots`, `--add-dir` | `external_directory` (permission only) |
| Read denial | `sandbox.filesystem.denyRead`, `Read(...)` deny | Profile `filesystem` `deny`, `deny_read` | `read` deny pattern |
| Network allowlist | `sandbox.network.allowedDomains` | `network.domains` (proxy) | — |
| Escalation | `dangerouslyDisableSandbox` retry | Sandbox approval, `allow` rule | — |
| Admin constraint | Managed `permissions`, `disableBypassPermissionsMode` | `allowed_approval_policies`, `allowed_sandbox_modes` | Managed config |

## Portability

There is no shared permissions file. Each rule has to be written once per harness. The same intent in each syntax:

| Intent | Claude Code (`.claude/settings.json`) | Codex | OpenCode (`opencode.json`) |
| --- | --- | --- | --- |
| Ask before `git push` | `"ask": ["Bash(git push *)"]` | `prefix_rule(pattern=["git","push"], decision="prompt")` in `.codex/rules/*.rules` | `"bash": {"git push *": "ask"}` |
| Block `rm -rf` | `"deny": ["Bash(rm -rf *)"]` | `prefix_rule(pattern=["rm","-rf"], decision="forbidden")` | `"bash": {"rm -rf *": "deny"}` |
| Hide `.env` | `"deny": ["Read(./.env)", "Read(./.env.*)"]` | Profile `filesystem` entry `"**/*.env" = "deny"` (beta, requires profiles instead of `sandbox_mode`) | Default |
| Allow network to a registry | `sandbox.network.allowedDomains` | `network_access = true`, or profile `network.domains` with `features.network_proxy` | No sandbox |

Traps:

- **Rule order means different things.** Claude Code and Codex: most restrictive wins, regardless of order or specificity, so a broad deny cannot be narrowed by an allow ([CC](../vendors/claude-code/permissions-and-sandbox.md#rule-evaluation), [Codex](../vendors/codex/permissions-and-sandbox.md#approvals-and-rules)). OpenCode: the last matching rule wins, so put `"*"` first ([OC](../vendors/opencode/permissions-and-sandbox.md#limits-and-gotchas)).
- **Command rules are not a security boundary.** In Claude Code, `Bash(curl *)` does not stop `/usr/bin/curl` or `sh -c 'curl ...'` ([CC](../vendors/claude-code/permissions-and-sandbox.md#limits-and-gotchas)). Codex evaluates `sh -c` scripts with redirection, substitution, or variables as one invocation ([Codex](../vendors/codex/permissions-and-sandbox.md#approvals-and-rules)). Enforcement belongs to the sandbox.
- **The sandbox default differs.** Claude Code runs commands unsandboxed unless the sandbox is enabled; Codex always applies a sandbox mode. The same task can need network or write approvals in Codex and none in Claude Code.
- **Network defaults differ.** Claude Code's sandbox proxies to an allowlist that starts empty; Codex `workspace-write` has no network until `network_access = true`, and the Codex proxy filters domains but does not grant access ([Codex](../vendors/codex/permissions-and-sandbox.md#network)).
- **MCP servers escape the command sandbox in both leads.** Claude Code runs local MCP servers outside the sandbox; the Codex proxy does not filter MCP connections ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-coverage), [Codex](../vendors/codex/permissions-and-sandbox.md#network)). Govern them with the MCP allowlists in [mcp](mcp.md).
- **Harness config directories are protected.** Edits to `.claude/` (Claude Code) and `.codex/` or `.agents/` (Codex) need approval even in permissive presets. Inference: an agent that edits shared config for both harnesses will hit prompts in both.
- **Repositories cannot loosen their own permissions before trust.** Claude Code holds project `allow` rules until workspace trust and ignores project `auto`/`bypassPermissions` defaults ([CC](../vendors/claude-code/permissions-and-sandbox.md#locations-and-scopes)). Codex loads project rules only for trusted projects.
- **Outdated preset names.** Codex `approval_policy = "untrusted"` is retired and can stop the client from starting; `on-failure` is deprecated ([Codex](../vendors/codex/permissions-and-sandbox.md#limits-and-gotchas)). Claude Code no longer starts in `default` mode in the terminal ([CC](../vendors/claude-code/permissions-and-sandbox.md#limits-and-gotchas)).
- **Secrets are readable by default.** The Claude Code sandbox allows reads of the whole machine, including `~/.ssh` ([CC](../vendors/claude-code/permissions-and-sandbox.md#limits-and-gotchas)). Add explicit read denials in each harness.

## Dropped from the generalization

- **Parameter-matching rules, `Tool(param:value)`** (Claude Code): Codex rules match only command tokens.
- **Rules for subagents, skills, web fetch, and `cd`, `Agent(...)`, `Skill(...)`, `WebFetch(...)`, `Cd(...)`** (Claude Code): Codex has no rule target for these tools.
- **`plan` as a permission mode** (Claude Code): Codex has `/plan`, but its permission behavior is not documented on the pages.
- **Granular approval policy, `approval_policy = { granular = ... }`** (Codex): Claude Code has no per-category prompt switch.
- **Named and inheritable permission profiles, `[permissions.<name>]` with `extends`** (Codex): Claude Code has one unnamed sandbox configuration.
- **Inline rule tests, `match` and `not_match`** (Codex): Claude Code rules have no self-test.
- **Native Windows sandbox** (Codex): Claude Code is unsandboxed on native Windows.
- **Sandbox credential masking, `sandbox.credentials`** (Claude Code): no Codex sandbox counterpart. Environment filtering is covered in [configuration](configuration.md).
- **`blockReadsOutsideWorkingDirectories`** (Claude Code): Codex expresses read limits only through profile paths.
- **`--restricted`** (Claude Code): no Codex counterpart.
- **Mods answering `tool.check`** (Claude Code): plugin code that overrides ask rules has no Codex counterpart.
- **`doom_loop` repeated-call check** (OpenCode): neither lead has it.
- **`continue_loop_on_deny` and `experimental.policies`** (OpenCode): no lead counterpart.

## Sources

- [Claude Code: permissions and sandbox](../vendors/claude-code/permissions-and-sandbox.md)
- [Codex: permissions and sandbox](../vendors/codex/permissions-and-sandbox.md)
- [OpenCode: permissions and sandbox](../vendors/opencode/permissions-and-sandbox.md)
- [Codex: MCP](../vendors/codex/mcp.md)
- [OpenCode: configuration](../vendors/opencode/configuration.md)
- [Claude Code README](../vendors/claude-code/README.md), [Codex README](../vendors/codex/README.md), [OpenCode README](../vendors/opencode/README.md)
