# Execution isolation and policy-as-code as gates outside a coding agent's harness

State as of 2026-10-07. All sources below were fetched on 2026-10-07 and the quoted text was checked against the fetched page. Date-sensitive items are marked (date-sensitive). Product names are examples only.

Working classification used throughout these notes ([Inference]; it follows from the cited behaviour of each control):
- **Containment** (isolation layers): limits what any action can reach. It does not decide whether an action is allowed.
- **Gate** (policy-as-code, admission, cloud org policy, budget actions, rulesets, push protection): evaluates a proposed change or API call and allows or denies it, outside the agent's process.
- **Limit** (quotas, rate/spend limits, timeouts): caps how much is consumed, regardless of intent.
- **Recovery** (backups, point-in-time recovery, immutable vaults): does not prevent anything; restores state afterwards.
- **Detection/classification** (DLP inspection, audit): finds sensitive data or violations; it is a gate only where it is wired in-line to block.

## 1. Isolation layers outside the harness: strength, what they contain, what they don't

### Takeaway
The isolation ladder runs from per-command OS sandbox → whole-process sandbox → container (shared host kernel) → user-space kernel (gVisor) → VM / microVM (own kernel, hypervisor boundary) → hosted cloud sandbox / separate machine. Every layer contains filesystem, process and (if configured) network reach; none of them stops misuse of data the agent can legitimately read or actions through APIs and credentials it is allowed to use, and egress-capable setups can still leak readable data.

### Cited Findings

**Shared kernel vs hypervisor**
- NIST: containers "do not offer as clear and concrete of a security boundary as a VM. Because containers share the same kernel and can be run with varying capabilities and privileges on a host, the degree of segmentation between them is far less than that provided to VMs by a hypervisor." — [NIST SP 800-190](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf)
- NIST §3.5.2 "Shared kernel": "the use of a shared kernel invariably results in a larger inter-object attack surface than seen with hypervisors, even for container-specific OSs. In other words, the level of isolation provided by container runtimes is not as high as that provided by hypervisors." — [NIST SP 800-190](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf)
- NIST recommendation: "Only group containers with the same purpose, sensitivity, and threat posture on a single host OS kernel to allow for additional defense in depth." and "a best practice is to group containers together by relative sensitivity and to ensure that a given host kernel only runs containers of a single sensitivity level." — [NIST SP 800-190](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf)
- Anthropic: "Containers provide isolation through Linux namespaces. Each container has its own view of the filesystem, process tree, and network stack, while sharing the host kernel." — [Claude Code: Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
- Anthropic (sandbox runtime): "Unlike VMs, sandboxed processes share the host kernel. A kernel vulnerability could theoretically enable escape. … if you need kernel-level isolation, use gVisor or a separate VM." — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
- Anthropic's comparison table: Sandbox runtime "Good (secure defaults)"; Containers (Docker) "Setup dependent"; gVisor "Excellent (with correct setup)", overhead "Medium/High"; VMs (Firecracker, QEMU) "Excellent (with correct setup)", overhead "High". — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
- Anthropic: "VMs provide hardware-level isolation through CPU virtualization extensions. Each VM runs its own kernel … However, VMs aren't automatically 'more secure' than alternatives like gVisor. VM security depends heavily on the hypervisor and device emulation code." — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
- Anthropic: "A dedicated virtual machine provides the strongest separation, with its own kernel and, in cloud or microVM deployments, its own virtualized hardware." Use it "when you are evaluating untrusted code, when your security policy requires kernel-level separation". For "Work on an untrusted repository": "A dedicated virtual machine, or a cloud session". — [Claude Code: Sandbox environments](https://code.claude.com/docs/en/sandbox-environments)

**gVisor (user-space application kernel)**
- "gVisor provides a strong layer of isolation between running applications and the host operating system. It is an application kernel that implements a Linux-like interface." It is "not a syscall filter (e.g. seccomp-bpf), nor a wrapper over Linux isolation primitives"; tradeoff: "reduced application compatibility and higher per-system call overhead." — [gVisor docs](https://gvisor.dev/docs/)
- Anthropic: "If an agent runs malicious code (perhaps due to prompt injection), that code runs in the container and could attempt kernel exploits. With gVisor, the attack surface is much smaller". Overhead table: CPU-bound "~0%", simple syscalls "~2× slower", file-I/O intensive "Up to 10-200× slower for heavy open/close patterns". — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)

**MicroVMs (Firecracker, Kata)**
- Firecracker "runs in user space and uses the Linux Kernel-based Virtual Machine (KVM) to create microVMs"; "Boot in <125ms. Create up to 150 microVMs per second per host."; "only 5 emulated devices are available"; the jailer "provides a second line of defense in case the virtualization barrier is ever compromised." — [firecracker-microvm.github.io](https://firecracker-microvm.github.io/)
- Anthropic: with Firecracker "the agent VM has no external network interface. Instead, it communicates through `vsock` … All traffic routes through vsock to a proxy on the host, which enforces allowlists and injects credentials before forwarding requests." — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
- Kata Containers: "building lightweight virtual machines that seamlessly plug into the containers ecosystem"; "Runs in a dedicated kernel, providing isolation of network, I/O and memory"; "stronger workload isolation using hardware virtualization technology as a second layer of defense". — [katacontainers.io](https://katacontainers.io/)

**Dev containers**
- The Dev Container spec "allows you to use a container as a full-featured development environment" — the spec page does not present it as a security boundary. — [containers.dev](https://containers.dev/)
- Anthropic: committing a dev container "is a convention rather than an enforcement boundary, because Claude Code does not require a container. If developers should not be able to run Claude Code outside it, enforce that with your organization's device management or software allowlisting tools." — [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments)
- Anthropic: "When executed with `--dangerously-skip-permissions`, dev containers do not prevent a malicious project from exfiltrating anything accessible inside the container, including the Claude Code credentials stored in `~/.claude`. Only use dev containers when developing with trusted repositories". Also: "Claude can still modify any file in the bind-mounted workspace, which appears directly on your host". — [Claude Code: Dev containers](https://code.claude.com/docs/en/devcontainer)
- Anthropic: a managed-settings file copied by the Dockerfile can be removed by "anyone with write access"; "For policy that engineers cannot bypass by editing repository files, deliver managed settings through server-managed settings or your MDM instead." — [Dev containers](https://code.claude.com/docs/en/devcontainer)

**Hosted cloud sandboxes**
- Anthropic cloud sessions: "runs in an isolated, Anthropic-managed virtual machine. A network proxy enforces a default allowlist, and a separate proxy holds your GitHub token outside the sandbox while issuing scoped credentials for repository access inside it." Self-hosted environments: "isolation, egress control, and git credentials are your deployment's responsibility." (date-sensitive) — [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments)
- OpenAI Codex cloud: "Runs in isolated OpenAI-managed containers, preventing access to your host system or unrelated data."; "Secrets configured for cloud environments are available only during setup and are removed before the agent phase starts." (date-sensitive) — [Codex: Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)
- GitHub Copilot cloud agent: "Copilot can edit files and run tests and linters in an ephemeral cloud development environment" — [About Copilot coding agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent); "GitHub restricts Copilot cloud agent's access to the internet." — [Risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations)

**What isolation does not contain**
- "Any approach that allows network egress can still leak data the agent can read, and any approach that mounts your project directory writable can still modify that code." and "Isolation also does not change what is sent to the model." — [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments)
- Domain allowlists are hostname-based: the proxy "does not terminate or inspect encrypted traffic. Code running inside the sandbox can potentially use domain fronting … if the agent has permissive credentials for an allowed domain, ensure it cannot use that domain to trigger other network requests or to exfiltrate data." — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
- "Allowing broad domains such as `github.com` can create paths for data exfiltration." — [Claude Code: Sandboxing](https://code.claude.com/docs/en/sandboxing)
- "Effective sandboxing requires both filesystem and network isolation. Without network isolation, a compromised agent could exfiltrate sensitive files like SSH keys. Without filesystem isolation … a compromised agent could backdoor system resources to gain network access." — [Sandboxing](https://code.claude.com/docs/en/sandboxing)
- Read-only mounts still expose secrets: "Even read-only access to a code directory can expose credentials" (`.env`, `~/.aws/credentials`, `~/.kube/config`, `.npmrc`, `*.pem` …). — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)

**Credentials outside the boundary (the key outer pattern)**
- "you can place sensitive resources (like credentials) outside the boundary containing the agent. If something goes wrong in the agent's environment, resources outside that boundary remain protected." Proxy pattern benefits: "The agent never sees the actual credentials"; "The proxy can enforce an allowlist of permitted endpoints"; "The proxy can log all requests for auditing". — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
- With `--network none` plus a mounted proxy socket: "Even if the agent is compromised via prompt injection, it cannot exfiltrate data to arbitrary servers. It can only communicate through the proxy, which controls what domains are reachable." — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
- Cloud pattern: private subnet "with no internet gateway", firewall rules "to block all egress except to your proxy", "minimal IAM permissions to the agent's service account", "Log all traffic at the proxy for audit purposes". — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
- Ephemeral writable state: `tmpfs` mounts "are cleared when the container stops"; an overlay filesystem lets you "inspect, apply, or discard" the agent's changes. — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)

### Inferences
- [Inference] For harness-forge, "isolation layer" answers *where* the agent runs and *what it can reach*; it never encodes a business rule ("never touch prod table X"). A rule that names a specific resource or change needs a gate (section 2) or credential scoping, not a stronger sandbox.
- [Inference] Isolation strength matters mainly against a compromised agent running hostile code (kernel exploit, escape). Against honest mistakes, a container with no host secrets, a disposable workspace and no writable host mount already removes most blast radius; VM/microVM strength adds little there.
- [Inference] A "separate machine/account for agent work" is the same principle as credentials-outside-the-boundary applied at the identity level: the agent's account simply lacks the permissions. Its effect is only as good as the scoping of that account's tokens.

### Gaps
- No primary source found quantifying container-escape rates or comparing gVisor vs Firecracker escape history; strength claims above are qualitative.
- Docker Sandboxes (named by Anthropic as a microVM option) was not fetched from docs.docker.com in this pass; only Anthropic's description is cited.
- Separate OS user accounts / separate physical machines for agent work: no vendor primary doc found that addresses them specifically beyond Anthropic's VM/cloud-session guidance.

## 2. Policy-as-code engines as gates: where they intercept and what they can enforce on agent-produced changes

### Takeaway
Policy engines intercept at four points: CI (Conftest/OPA, Kyverno CLI on files and plans), IaC run (HCP Terraform Sentinel/OPA after plan, before apply), cluster admission (Gatekeeper, Kyverno on every create/update/delete), and the cloud control plane (AWS SCPs, GCP Organization Policy on every API call). They evaluate the *artifact or API request*, not the agent, so they hold whether the change came from an agent, a human, or a hijacked agent — provided the agent's identity cannot edit or bypass the policy.

### Cited Findings
- Conftest: "Conftest is a utility to help you write tests against structured configuration data." It covers Kubernetes, Terraform, Dockerfiles, JSON, YAML and more, with policies written in Rego from OPA. — [conftest.dev](https://www.conftest.dev/)
- OPA on Terraform: "OPA makes it possible to write policies that check the changes Terraform is about to make before it makes them." Workflow: `terraform plan --out tfplan.binary`, `terraform show -json tfplan.binary > tfplan.json`, evaluate against the JSON. Examples include restricting changes to IAM resources and a blast-radius score (e.g. weights `"aws_autoscaling_group": {"delete": 100, "create": 10}` against `blast_radius := 30`). — [OPA: Terraform](https://www.openpolicyagent.org/docs/terraform)
- HCP Terraform: "Policies are rules that let you validate that Terraform plans comply with security rules and best practices." "HCP Terraform checks the Terraform plan against the policy set during each run" and "Depending on their enforcement level, failed policies can stop the run." — [HCP Terraform policy enforcement](https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement)
- Enforcement levels (Sentinel): Advisory — "Failed policies never interrupt the run"; Soft mandatory — "Failed policies stop the run, but organization admins can configure the platform to allow team members to override failures"; Hard mandatory — "Failed policies stop the run. Unless the set containing the policy is configured to allow overrides, Terraform does not apply runs until a user fixes the issue". OPA: Mandatory — "any user with Manage Policy Overrides permission can override these failures". — [Manage policy sets](https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement/manage-policy-sets)
- Gatekeeper: "a validating and mutating webhook that enforces CRD-based policies executed by Open Policy Agent"; admission webhooks "are executed whenever a resource is created, updated or deleted"; "Gatekeeper's audit functionality allows administrators to see what resources are currently violating any given policy." — [Gatekeeper docs](https://open-policy-agent.github.io/gatekeeper/website/docs/)
- Kyverno: "a cloud native policy engine. It was originally built for Kubernetes and now can also be used outside of Kubernetes clusters as a unified policy language"; it can "validate, mutate, generate, or cleanup (remove) any Kubernetes resource" and handle "any JSON payload including Terraform resources, cloud resources, and service authorization." — [Kyverno introduction](https://kyverno.io/docs/introduction/)
- AWS SCPs: "SCPs offer central control over the maximum available permissions for the IAM users and IAM roles in your organization." "No permissions are granted by an SCP." A blocked permission cannot be used "even if the account administrator attaches the `AdministratorAccess` IAM policy". "SCPs affect all users and roles in attached accounts, including the root user." Limits: "SCPs don't affect users or roles in the management account" and "do not affect any service-linked role." — [AWS Organizations: SCPs](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)
- GCP Organization Policy: "gives you centralized and programmatic control over your organization's Google Cloud resources"; "all descendants of that resource inherit the organization policy by default"; "Identity and Access Management focuses on who … Organization Policy focuses on what, and lets the administrator set restrictions on specific resources to determine how they can be configured." — [GCP Organization Policy overview](https://docs.cloud.google.com/resource-manager/docs/organization-policy/overview)
- Repository-side gates (GitHub): rulesets control "who can push commits to a certain branch" and can require signed commits and block force pushes; push rulesets "block pushes to a private or internal repository and that repository's entire fork network based on file extensions, file path lengths, file and folder paths, and file sizes." Bypass can be granted to roles, teams or GitHub Apps. — [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- Push protection "blocks pushes that contain secrets before they reach your repository", covering command-line pushes, UI commits, uploads, REST API requests and GitHub MCP server interactions (public repositories only). — [About push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)
- Dependency review action "can also add enforcement mechanisms to the GitHub Actions workflow" to catch vulnerable dependencies in a PR. — [Configuring the dependency review action](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configuring-the-dependency-review-action)
- Vendor-built outside gates on an agent: Copilot cloud agent "can only push to that branch" (`copilot/`); "Draft pull requests created by Copilot cloud agent must be reviewed and merged by a human"; "workflows are not triggered until Copilot cloud agent's code is reviewed and a user with write access … clicks the Approve and run workflows button." — [Copilot risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations)

### Inferences
- [Inference] Interception points differ in what they can see: CI/Conftest sees files in the PR (and can be skipped if the agent can edit the workflow or the policy file in the same PR); plan-time policy sees the computed infrastructure diff; admission and cloud org policy see the live API call and hold even for changes that never went through a PR. For "must hold even if the agent is compromised", prefer admission/cloud-API gates or CI gates whose policy lives outside the repository the agent can write (required workflows, org rulesets).
- [Inference] Override paths (soft-mandatory, OPA "Mandatory" overrides, ruleset bypass lists, SCP management account) are the weak point: the agent's identity must not hold override/bypass permission.
- [Inference] Policy engines check structure, not intent: they catch "public bucket", "IAM change", "delete > N resources", "secret in diff", but not a logically wrong yet policy-compliant change; review and tests remain necessary.

### Gaps
- Did not fetch GitHub "required workflows"/org-level ruleset workflow enforcement docs to confirm policy-outside-repo mechanics; the inference about keeping CI policy outside the writable repository is not sourced here.
- AWS Resource Control Policies (RCPs) are mentioned by the SCP page but were not researched.

## 3. Resource and cost limits as gates against runaway agents

### Takeaway
Limits split into hard caps enforced by the provider (API spend/rate limits, job timeouts, container cgroup limits, budget actions that apply deny policies) and alerts that do not stop anything (alerts-only cloud budgets). Only the former are gates.

### Cited Findings
- Model API (Anthropic, date-sensitive): workspace "Spend limits: Cap monthly spending for a workspace"; "Rate limits: Limit requests per minute, input tokens per minute, or output tokens per minute"; workspace limits can be set "lower than (but not higher than) your organization's limits"; "Organization-wide limits always apply". The Claude Code workspace "is the only workspace that supports per-user monthly spend limits" and "admins can cap its share of the organization's limits". — [Claude Platform: Workspaces](https://platform.claude.com/docs/en/manage-claude/workspaces)
- CI timeouts (GitHub Actions): `jobs.<job_id>.timeout-minutes` — "The maximum number of minutes to let a job run before GitHub automatically cancels it. Default: 360"; step `timeout-minutes` — "The maximum number of minutes to run the step before killing the process. Maximum: 360 for both GitHub-hosted and self-hosted runners." — [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- Container resource limits: `--memory 2g` "Limits memory usage to prevent resource exhaustion"; `--pids-limit 100` "Limits process count to prevent fork bombs"; plus `--cpus 2`. — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
- AWS Budgets actions: "You can use AWS Budgets to run an action on your behalf when a budget exceeds a certain cost or usage threshold … configure a budget action to run either automatically or after your manual approval." Actions include "applying an IAM policy or a service control policy (SCP)" and "targeting specific Amazon EC2 or Amazon RDS instances". — [AWS Budgets: budget actions](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-controls.html)
- GCP budgets: "Setting an alerts-only budget doesn't automatically cap Google Cloud or Google Maps Platform usage or spending." Pub/Sub notifications can "automate cost management tasks, such as programmatically disabling Cloud Billing on a project". — [GCP: Create budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets)
- LLM gateways such as LiteLLM are listed by Anthropic as proxies "with credential injection and rate limiting". — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)

### Inferences
- [Inference] Limits work the same against honest loops and compromised agents because they ignore intent; they bound damage (spend, runtime, compute) but do not prevent a single harmful action that fits inside the limit.
- [Inference] Budget-triggered actions are reactive and depend on billing data arriving; treat them as a backstop, with hard per-key/per-workspace API caps and job timeouts as the primary runaway gates.

### Gaps
- AWS billing-data latency for budget actions was not stated on the fetched page; not cited.
- OpenAI project budget/limit docs were not fetched in this pass.

## 4. DLP and backups/point-in-time recovery: recovery and detection controls, not gates

### Takeaway
Backups and PITR are recovery controls: they prevent nothing but bound the cost of a destructive mistake. They only survive a compromised agent if the agent's identity cannot delete them (immutable/WORM vaults). DLP is mostly detection/classification; it acts as a gate only where deployed in-line (e.g. secret push protection, redaction of payloads before storage).

### Cited Findings
- PITR: "You can restore a DB instance to a specific point in time, creating a new DB instance without modifying the source DB instance." "RDS uploads transaction logs for DB instances to Amazon S3 every five minutes." "You can restore to any point in time within your backup retention period." — [Amazon RDS: point-in-time restore](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html)
- Immutable backups: Vault Lock provides "WORM (write-once, read-many) configuration" and "An additional layer of defense that protects backups … from inadvertent or malicious deletions." "If any user (including the root user) attempts to delete a backup or change the lifecycle properties in a locked vault, AWS Backup will deny the operation." Governance mode locks "can have the lock removed by users with sufficient IAM permissions"; compliance mode becomes immutable after a grace time of "at least 3 days (72 hours)". — [AWS Backup Vault Lock](https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html)
- DLP (Google Sensitive Data Protection): discovery profiles data; inspection performs "a deep scan of an individual resource to find instances of sensitive data"; de-identification uses "masking, redaction, bucketing, date shifting, and tokenization"; it can "Inspect and redact sensitive tokens … from streaming API payloads, user forms, and LLM prompt inputs before storing the data". — [Sensitive Data Protection overview](https://docs.cloud.google.com/sensitive-data-protection/docs/sensitive-data-protection-overview)
- In-line secret DLP as a gate: push protection blocks secret-bearing pushes "Rather than alerting you to credential leaks after the fact". — [About push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)
- Ephemeral/overlay workspaces as local recovery: tmpfs "cleared when the container stops"; overlay changes can be "inspect[ed], appl[ied], or discard[ed]". — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)

### Inferences
- [Inference] Classification for harness-forge: backups/PITR/version history = recovery; Vault-Lock-style immutability = a gate protecting the recovery path; DLP scanning = detection unless wired in-line (push protection, egress proxy redaction), which makes it a gate on that one channel only.
- [Inference] Recovery cannot undo exfiltration or external side effects (sent messages, published packages); for those, only gates and containment help.

### Gaps
- No primary source found on DLP effectiveness against deliberately obfuscated exfiltration by an LLM agent.

## 5. Honest mistakes vs compromised/prompt-injected agent: what each control accomplishes, and limits

### Takeaway
Vendors model both threats together ("prompt injection … or model error"). Controls outside the agent's process and identity (VM/container without secrets, credential-injecting proxy, admission/cloud org policy, budgets, immutable backups) hold against both. Controls the agent can edit or that rely on the agent's cooperation (repo-committed dev container config, in-repo CI policy, advisory policies) only help against honest mistakes.

### Cited Findings
- Threat model: "Agents can take unintended actions due to prompt injection (instructions embedded in content they process) or model error." "if an agent processes a malicious file that instructs it to send customer data to an external server, network controls can block that request entirely." — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
- "Sandbox isolation reduces the impact of a breach, but it does not eliminate risk." — [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments)
- Codex: "Prompt injection can cause the agent to fetch and follow untrusted instructions" when network/web search is enabled; "By default, the agent runs with network access turned off." (date-sensitive) — [Codex: Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)
- GitHub: "Only users with write access to the repository can trigger Copilot cloud agent to work"; "GitHub filters hidden characters before passing user input to Copilot cloud agent". — [Copilot risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations)
- [Practitioner] Simon Willison's "lethal trifecta": "Access to your private data", "Exposure to untrusted content", "The ability to externally communicate"; on filtering: "we still don't know how to 100% reliably prevent this". — [simonwillison.net](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
- Classifier/permission layers are not isolation: auto mode's classifier "is a per-action control, not an isolation boundary". — [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments)

### Inferences
- [Inference] Matrix for harness-forge:
  - Container/VM without host secrets: honest mistakes — contains damage to the workspace; compromised — contains host damage, but leaks whatever is readable over allowed egress.
  - Credential proxy / scoped identity: both — the agent cannot use what it never holds; allowed APIs remain usable for harm.
  - Admission / cloud org policy / SCP: both — holds even under compromise if the agent's identity cannot change policy or use a bypass role.
  - CI policy in the agent-writable repo: honest mistakes only.
  - Limits/timeouts: both, bounds magnitude only.
  - Backups/PITR: both for recovery of state; compromised agent may delete backups unless immutable.
  - DLP detection: honest leaks mostly; a compromised agent can encode or route around pattern detection (no source quantifies this — see gap in §4).
- [Inference] The common limit across all outer layers: actions through legitimately granted channels (an allowed domain, a writable repo, a permitted API) are not blocked by isolation; only a gate that understands that channel's semantics (branch ruleset, plan policy, SCP) can block them.

### Gaps
- No vendor document gives empirical rates for prompt-injection success under each isolation tier.

## 6. When outer controls complement a harness sandbox/hook vs replace building anything in the harness

### Takeaway
Vendor guidance layers them: the harness sandbox/permissions decide per-action, the outer boundary limits what any allowed action can reach. Outer controls replace harness configuration when the rule is about an external system that already has its own enforcement point (cloud API, cluster, branch, budget), when the harness runs without prompts, or when the rule must survive edits to agent-side config.

### Cited Findings
- "Permission modes decide whether a tool call runs and whether you are prompted first. Isolation restricts what a command can access once it runs. The two work together". — [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments)
- Harness Bash sandbox scope: "Built-in file tools, MCP servers, and hooks still run directly on your host. Every other approach in the table puts the whole Claude Code process inside the isolation boundary". The Bash sandbox alone "is not sufficient for fully unattended runs". Layering: "running the sandboxed Bash tool inside a container or VM gives you OS-level command restrictions on top of the outer environment boundary." — [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments)
- "Always run `--dangerously-skip-permissions` sessions inside a container, a VM, or the sandbox runtime". — [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments)
- Enforcement ownership: the built-in Bash sandbox is "the only approach Claude Code enforces itself"; for containers and VMs "use your organization's device management or software allowlisting tools to prevent installation outside it." — [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments)
- Codex CLI source: `--dangerously-bypass-approvals-and-sandbox` (alias `yolo`) is "EXTREMELY DANGEROUS. Intended solely for running in environments that are externally sandboxed." — [openai/codex shared_options.rs](https://github.com/openai/codex/blob/main/codex-rs/utils/cli/src/shared_options.rs)

### Inferences
- [Inference] Decision rule for harness-forge:
  - **Outer only (nothing in harness)**: rule targets a system with its own policy point and the agent reaches it only via credentials — e.g. "no public buckets" → org policy/SCP; "no direct pushes to main" → ruleset; "max spend" → workspace spend limit; "job ends after N minutes" → CI timeout. Duplicating it in a harness hook adds early feedback, not security.
  - **Both**: rule must hold under compromise *and* benefits from fast in-loop feedback — e.g. a harness hook running Conftest locally for quick correction plus the same policy enforced in CI/admission.
  - **Harness only**: rule is about agent behaviour within its own workspace with no external enforcement point (formatting, test-before-done) and violation is low-impact.
  - **Outer isolation required**: any bypass/no-prompt mode, untrusted repositories, or untrusted input combined with secrets and egress.

### Gaps
- No vendor guidance found that explicitly says "do not build X in the harness, rely on the external control"; the decision rule above is inference.

## 7. Coding-agent vendor guidance on containers/VMs (primary docs only)

### Takeaway
Anthropic gives the most detailed guidance (isolation ladder, hardened `docker run`, gVisor, Firecracker, credential proxy, cloud egress pattern). OpenAI documents an OS sandbox locally, isolated managed containers for cloud with secrets removed before the agent phase, and states in source that full bypass is for externally sandboxed environments. GitHub's cloud agent is itself an outer-gated design: ephemeral environment, restricted internet, single-branch push, human merge, workflow approval.

### Cited Findings
- Anthropic: hardened container flags `--cap-drop ALL`, `--security-opt no-new-privileges`, custom seccomp ("Docker's default blocks ~44"), `--read-only`, `--network none`, `--user 1000:1000`, read-only code mount; "Avoid mounting sensitive host directories like `~/.ssh`, `~/.aws`, or `~/.config`". — [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
- Anthropic: "On Linux and macOS, Claude Code refuses to start with this flag when running as root, so run the container, VM, or sandbox runtime as a non-root user." — [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments)
- Anthropic: the reference dev container firewall "blocks unapproved egress", so it "supports running Claude Code with `--dangerously-skip-permissions` for unattended work." — [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments)
- Anthropic custom containers checklist: "review what is mounted writable, what credentials and tokens are reachable inside it, and what the network egress policy allows." — [Sandbox environments](https://code.claude.com/docs/en/sandbox-environments)
- OpenAI: "Locally, Codex uses an OS-enforced sandbox that limits what it can touch."; in Docker "the sandbox may not work if the host or container configuration blocks the namespace, setuid `bwrap`, or `seccomp` operations." — [Codex: Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)
- OpenAI: bypass flag "Intended solely for running in environments that are externally sandboxed." — [openai/codex source](https://github.com/openai/codex/blob/main/codex-rs/utils/cli/src/shared_options.rs)
- GitHub: see §2 and §5 (branch restriction, human merge, workflow approval, write-access trigger, restricted internet). — [Copilot risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations)

### Inferences
- [Inference] All three vendors converge on: no prompts only inside an external boundary; credentials kept outside or removed before the agent runs; egress restricted by default; human review as the merge gate.

### Gaps
- OpenAI's public docs (learn.chatgpt.com sandboxing page, fetched 2026-10-07) did not contain an explicit recommendation to run `danger-full-access` in Docker/VMs; only the CLI source string above was verified. The repository's existing claim "Codex names Docker as acceptable isolation for `--yolo`" (docs/guide/permissions-and-sandbox.md) could not be re-verified from the pages fetched here.
- GitHub docs on self-hosted/larger runners for Copilot agent and its firewall allowlist configuration were not fetched.
- New domains cited that are not yet in docs/sources.md trusted tables (all primary per rule "Assessing a new domain" step 1): `nvlpubs.nist.gov`, `gvisor.dev`, `firecracker-microvm.github.io`, `katacontainers.io`, `containers.dev`, `www.conftest.dev`, `www.openpolicyagent.org`, `open-policy-agent.github.io`, `kyverno.io`, `developer.hashicorp.com`, `docs.aws.amazon.com`, `docs.cloud.google.com`.
