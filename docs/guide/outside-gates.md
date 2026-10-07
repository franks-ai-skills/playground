# Outside gates

Controls outside the agent harness that hold when the agent errs, is
prompt-injected, or has its configuration changed by a pull request:
merge rules, CI checks, scanners, identity and credentials, network and
DNS boundaries, isolation, policy engines and limits. Like
[security](security.md), this is a concern across the ten concepts, not
an eleventh extension mechanism. It gives harness-forge the knowledge
to recommend an outside gate alongside a harness mechanism, instead of
any harness build, or not at all
([design](../../specs/2026-10-06-harness-forge-design.md)).

The [research notes](../research-notes/outside-gates/README.md) were
fetched on 2026-10-07. Plan-tier availability and vendor defaults
change often; re-check them against the cited page before relying on
them.

**Evidence labels:** **[Practitioner]** marks a first-hand report by
an identifiable author; **[Inference]** marks our conclusions from the
cited evidence. Unlabelled statements quote or paraphrase the linked
primary source.

## Summary

A rule that must still hold when a coding agent has been
prompt-injected, or its configuration changed by a pull request, belongs
in a control the agent's process and identity cannot reach. That means a
forge ruleset that requires an independent approver, a required check
from a pinned source whose definition the change cannot edit, a
credential the agent never holds, a default-deny egress boundary with
resolver control, a VM or container without host secrets, or a policy
engine at plan, admission or cloud-API time. Every authoritative source
in the notes says this in its own words: OWASP tells builders to
"implement authorization in downstream systems rather than relying on an
LLM to decide if an action is allowed" ([OWASP
LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)).
Google calls reasoning-based defenses "inadequate, on their own" for
irreversible actions
([Google](https://storage.googleapis.com/gweb-research2023-media/pubtools/1018686.pdf)).
GitHub's and Anthropic's own cloud agents rely on branch protection and
rulesets for their safety guarantees
([GitHub](https://docs.github.com/en/copilot/concepts/agents/coding-agent/risks-and-mitigations),
[Anthropic](https://code.claude.com/docs/en/security)). Against honest
mistakes, nearly any layer helps, including advisory ones. Against a
compromised agent, only controls that sit outside agent-writable state,
have no bypass for the agent's identity, and are enforced on the user's
plan tier work as gates. Even those cannot stop misuse of authority the
agent legitimately holds, or exfiltration through a channel that is
allowed. For harness-forge, the practical result is a short set of
intake questions: must it survive compromise, who may turn it off, does
the event happen without an agent, is it irreversible, is the gate
available, and is earlier feedback wanted? Their answers place each part
of a user's idea in one of four outcomes: harness mechanism, outside
gate alongside it, outside gate instead of any harness build, or
nothing. A "build it anyway" override keeps the harness piece but labels
it as not a guarantee.

## Harness controls keep failing, so guarantees live elsewhere

The sources agree on where a guarantee can come from. OWASP's Excessive
Agency entry asks for "complete mediation" so that "all requests made to
downstream systems via extensions are validated against security
policies", and allows human approval either "in a downstream system
(outside the scope of the LLM application) or within the LLM extension
itself" ([OWASP
LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)).
The Agentic Top 10 for 2026 adds **"Least-Agency"**: "deploying agentic
behavior where it is not needed expands the attack surface without
adding value". It also recommends a "pre-execution Policy Enforcement
Point (PEP/PDP)" that treats "LLM or planner outputs as untrusted"
([OWASP Agentic Top
10](https://genai.owasp.org/download/52117/?tmstv=1765059207)). Google
describes policy engines "that operate outside the AI model's reasoning
process" as "security chokepoints", and states that "neither approach is
sufficient in isolation"
([Google](https://storage.googleapis.com/gweb-research2023-media/pubtools/1018686.pdf)).
The NCSC asks for "external AI and non-AI fail-safes if necessary" when
AI components amend files or send output to external systems
([NCSC](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development/guidelines/secure-design)).

A classic test separates a real gate from a convenience. NIST defines a
reference monitor as **"always invoked (i.e., complete mediation),
tamperproof, and small enough to be subject to analysis and tests"**
([NIST CSRC](https://csrc.nist.gov/glossary/term/reference_monitor)).
Saltzer and Schroeder add separation of privilege (two keys beat one),
fail-safe defaults, and "compromise recording". Compromise recording is
acceptable in place of prevention only where loss is recoverable
([Saltzer and
Schroeder](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html)).
[Inference] A harness permission rule fails the "tamperproof" test
against the agent it governs, because the agent's process enforces it
and a committed config file can change it. Claude Code's deny rule
"matches the command as written" ([Claude Code
security](https://code.claude.com/docs/en/security)), so it also fails
"always invoked" for paths it does not see.

The advisory record bears this out. Within one product's list, **a
committed `.claude/settings.json` could set `bypassPermissions` and
silently skip the trust dialog**
([GHSA-mmgp-wc2j-qcv7](https://github.com/anthropics/claude-code/security/advisories/GHSA-mmgp-wc2j-qcv7)).
Sandboxed code could create that file and inject hooks "that would
execute with host privileges"
([GHSA-ff64-7w26-62rf](https://github.com/anthropics/claude-code/security/advisories/GHSA-ff64-7w26-62rf)).
A worktree bug allowed "code execution outside of seatbelt sandbox
restrictions"
([GHSA-7835-87q9-rgvv](https://github.com/anthropics/claude-code/security/advisories/GHSA-7835-87q9-rgvv)).
With a stored API key, sessions started "without the organization's
server-managed policy", while MDM or file-based managed settings were
unaffected
([GHSA-gfvf-j8jh-jxxw](https://github.com/anthropics/claude-code/security/advisories/GHSA-gfvf-j8jh-jxxw)).
An overly broad allowlist let auto-approved `ping`/`dig`/`nslookup`
exfiltrate file contents via DNS (CVE-2025-55284, CVSS 7.1)
([GHSA-x5gv-jw7f-j6xj](https://github.com/anthropics/claude-code/security/advisories/GHSA-x5gv-jw7f-j6xj),
[Embrace The
Red](https://embracethered.com/blog/posts/2025/claude-code-exfiltration-via-dns-requests/)).

Outside gates are not automatically safe either. Two supply-chain
incidents involving agent tooling came from failures of the outside
layer itself. In the first, an "inappropriately scoped GitHub token in
their CodeBuild configuration" let an attacker commit code that shipped
in Amazon Q Developer for VS Code 1.84.0
([AWS-2025-015](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/)).
In the second, a bash injection in an Nx `pull_request_target` workflow
with a read/write `GITHUB_TOKEN` led to an npm token being sent to a
webhook. Nx's fix moved publishing to 2FA and trusted publishing
([GHSA-cxm3-wv7p-598c](https://github.com/nrwl/nx/security/advisories/GHSA-cxm3-wv7p-598c)).
[Inference] Recommending "a CI job" is therefore incomplete unless it
comes with least-privilege tokens and protected workflow definitions.

There are gaps in the evidence. The notes found no fetchable primary
postmortem in which an outside gate demonstrably stopped a coding
agent's harmful action. The widely discussed
agent-deletes-production-database cases rest on posts the source policy
excludes. CISA's joint AI deployment guidance could not be fetched, and
NIST's agent-identity work is still a concept paper that poses questions
([NCCoE](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf)).

## Ten families of outside gates, and what each stops

The notes support a working taxonomy [Inference]. Each control is
classified as *containment* (limits reach), *gate* (allows or denies a
proposed change or call), *limit* (caps quantity), *recovery* (restores
afterwards) or *detection* (finds violations; it is a gate only when
wired in-line). The sections below go family by family. Each covers what
the family achieves against an honest mistake and against a compromised
or prompt-injected agent, what it cannot do, and what makes it real.

### Branch protection and merge rules: the gate is separation of identities

Every major forge implements the same core under different names.
Changes reach the target ref only through a change request, with N
approvals, path-owner approval, re-approval on new pushes, exclusion of
author or last pusher, required checks, a merge queue, ref integrity
rules, pre-receive content rules, and gated deployment environments.
GitHub
([rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)),
GitLab ([protected
branches](https://docs.gitlab.com/user/project/repository/branches/protected/)),
Azure DevOps ([branch
policies](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies)),
Bitbucket ([merge
checks](https://support.atlassian.com/bitbucket-cloud/docs/suggest-or-require-checks-before-a-merge/))
and Gerrit ([submit
requirements](https://gerrit-review.googlesource.com/Documentation/config-submit-requirements.html))
all provide most of these. SLSA Source L4 states the target directly:
changes in protected branches "MUST be agreed to by two or more trusted
persons prior to submission" ([SLSA
v1.2](https://slsa.dev/spec/v1.2/source-requirements)).

Against honest mistakes, review catches what a reviewer notices, and a
merge queue keeps "the branch never broken by incompatible changes"
([GitHub merge
queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)).
Against a compromised agent, the decisive properties are identity
separation and stale-approval reset. GitHub can require "an approval
from someone other than the last person to push" ([GitHub
rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)).
Copilot's cloud agent shows the agent-specific form: it "Prevents the
user who asked Copilot cloud agent to create a pull request from
approving it" and "cannot approve or merge a pull request". When it
opens a PR under its own app identity, "one more approval is required"
([GitHub](https://docs.github.com/en/copilot/concepts/agents/coding-agent/risks-and-mitigations)).
[Inference] Without re-approval on push, an approval of a benign diff
carries over to a later malicious commit. Code owners on agent-config
paths (`AGENTS.md`, `.claude/`, `.codex/`, `.agents/skills/`, hooks, MCP
config, workflow files, and CODEOWNERS itself) stop an agent from
quietly loosening its own harness through a PR. Because CODEOWNERS "must
be on the base branch", a PR cannot exempt itself ([GitHub code
owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)).

The limits are concrete and mostly silent:

- Admins bypass classic branch protection "by default" ([GitHub
  protected
  branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)).
- GitLab committers "can still approve" by default, and rules can be
  overridden per merge request by default ([GitLab approval
  settings](https://docs.gitlab.com/user/project/merge_requests/approvals/settings/)).
- Users allowed to push "can skip merge request approval rules, Code
  Owners included"
  ([GitLab](https://docs.gitlab.com/user/project/repository/branches/protected/)).
- An invalid CODEOWNERS line "will be skipped"
  ([GitHub](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)).
- Bitbucket Cloud merge checks only warn unless the plan is Premium
  ([Bitbucket](https://support.atlassian.com/bitbucket-cloud/docs/suggest-or-require-checks-before-a-merge/)).
- Signing proves which key signed, not that the content is good
  [Inference].
- Anthropic's cloud sessions state: "A rule that access can bypass
  doesn't block a session's push" ([Claude Code
  security](https://code.claude.com/docs/en/security)).

[Inference] A single-maintainer repository cannot satisfy "someone other
than the last pusher". For it, required checks, protected workflow
definitions and environment approvals are the realistic outside gates,
and the residual risk should be stated.

### CI pipelines: a check is a gate only if the change cannot rewrite it

A CI job becomes a gate only when the target ref requires it, its result
source is pinned, nobody relevant can bypass, and its definition is
outside the change's control. GitHub warns that "Any person or
integration with write permissions to a repository can set the state of
any status check", so the ruleset should accept a check only "from a
specific GitHub App" ([GitHub
rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)).
For `pull_request` triggers, the workflow runs from the PR's merge
commit ([GitHub
events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)).
[Inference] For a same-repository agent PR, the check is therefore
author-controlled. Org-level required workflows pinned to "a specific
SHA" ([GitHub
blog](https://github.blog/2023-10-11-enforcing-code-reliability-by-requiring-workflows-with-github-repository-rules)),
plus code-owner review on workflow files, close that gap.

The opposite failure is a privileged trigger running untrusted code.
`pull_request_target` workflows "have write permission to the target
repository" and "access to target repository secrets", and combining
them with a checkout of the PR "may lead to repository compromise"
([GitHub Security
Lab](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/)).
That is exactly the Nx path
([GHSA-cxm3-wv7p-598c](https://github.com/nrwl/nx/security/advisories/GHSA-cxm3-wv7p-598c)).
Self-hosted runners execute "potentially malicious user-controlled
workflow code" automatically if approval can be bypassed ([GitHub
Actions
settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)).
On the defensive side, Copilot's agent does not trigger workflows until
a human with write access clicks "Approve and run workflows"
([GitHub](https://docs.github.com/en/copilot/concepts/agents/coding-agent/risks-and-mitigations)).
By default, workflows in a new personal repository "are not allowed to
create or approve pull requests" ([GitHub Actions
settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)).

Deployment environments are the strongest CI-side gate for production:
"a job cannot access environment secrets until one of the required
reviewers approves it", and "Prevent self-review" stops the initiator
from approving ([GitHub
environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)).
GitLab blocks the pipeline triggerer from approving by default, on
Premium and Ultimate
([GitLab](https://docs.gitlab.com/ci/environments/deployment_approvals/)).
Admins can still "bypass the protection rules and force deployments" by
default ([GitHub
environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)).
Client-side git hooks are never policy: they "are not copied when you
clone a repository" ([Pro
Git](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)), and
pre-commit "can be bypassed with the `--no-verify` option" ([git
docs](https://git-scm.com/docs/githooks)). Server-side pre-receive
rejects the whole push on non-zero exit ([git
docs](https://git-scm.com/docs/githooks)).

### Static analysis and scanners: every in-repo suppression is a bypass

SAST, SCA, secret scanning, IaC scanning, license checks and coverage
gates can run at any placement. [Inference] The placements form a ladder
from advisory to enforcing: agent-side hook < local pre-commit
(skippable via `--no-verify`, or `SKIP=gitleaks` per
[gitleaks](https://github.com/gitleaks/gitleaks)) < non-required CI
check < required check from a pinned app < server-side push rejection or
admission control. Only the last two hold against a compromised agent.
GitHub can block merges on code-scanning alerts above a chosen severity,
or when "the tool isn't configured" ([GitHub
rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets),
[merge
protection](https://docs.github.com/en/code-security/code-scanning/managing-your-code-scanning-configuration/set-code-scanning-merge-protection)).
Push protection blocks secrets "before they reach your repository"
across CLI pushes, UI, uploads and the REST API ([GitHub push
protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)).

The case for scanners on agent-written code is well documented. A USENIX
Security 2025 study of 576,000 samples found package hallucination rates
of **at least 5.2% for commercial and 21.7% for open-source models**
([arXiv 2406.10279](https://arxiv.org/abs/2406.10279)). **43% of
hallucinated names recurred in all 10 repeat queries** ([arXiv
HTML](https://arxiv.org/html/2406.10279v3)). [Practitioner] Lasso
Security's empty package registered under a hallucinated name,
"huggingface-cli", drew "more than 30k authentic downloads" in three
months ([Lasso
Security](https://www.lasso.security/blog/ai-package-hallucinations)).
An older study found roughly 40% of 1,689 Copilot programs vulnerable in
high-risk-CWE scenarios (2021 model) ([arXiv
2108.09293](https://arxiv.org/abs/2108.09293)). GitHub now runs CodeQL,
advisory-database and secret scanning on third-party agents' code too,
"including Claude and OpenAI Codex", on by default ([GitHub changelog
2026-06-09](https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/)).
[Inference] That validation runs inside the agent's loop, where the
agent "attempts to resolve" findings. It improves honest output but is
not a merge gate. [Inference] Vulnerability-database SCA misses
slopsquatting, because a fresh malicious package has no advisory yet.
The gate that targets it is a new-dependency allowlist, review, or
age/reputation check, consistent with SLSA's statement that it does not
address "package name confusion attacks" ([SLSA
threats](https://slsa.dev/spec/v1.1/threats-overview)).

Against a compromised agent, the weak point is suppression. Each tool
has in-repo channels:

- gitleaks: `#gitleaks:allow` and `.gitleaksignore`
  ([gitleaks](https://github.com/gitleaks/gitleaks)).
- Semgrep: `nosemgrep` and `.semgrepignore`
  ([Semgrep](https://docs.semgrep.dev/ignoring-files-folders-code)).
- Checkov: `checkov:skip=`
  ([Checkov](https://www.checkov.io/2.Basics/Suppressing%20and%20Skipping%20Policies.html)).
- OSV-Scanner: `osv-scanner.toml` ignores
  ([OSV-Scanner](https://google.github.io/osv-scanner/configuration/)).
- Dependency review: `allow-ghsas`
  ([dependency-review-action](https://github.com/actions/dependency-review-action)).
- Codecov: `informational: true`, which makes the status "pass no matter
  what" ([Codecov](https://docs.codecov.com/docs/commit-status)).

Writers can also bypass push protection by picking a reason such as
"It's a false positive", unless delegated bypass is configured ([GitHub
push
protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)).
[Inference] A scanner is a real gate only when its config, ignore files,
baselines and workflow are org-managed or covered by CODEOWNERS or a
push-ruleset path restriction. Semgrep's "Ignored" triage state and
OSV's `reason`/`ignoreUntil` make suppressions auditable, which counts
as detection, not prevention. Provenance (SLSA L2/L3 signed, isolated
builds; [SLSA levels](https://slsa.dev/spec/v1.1/levels)) and admission
control such as Sigstore policy-controller
([Sigstore](https://docs.sigstore.dev/policy-controller/overview/))
prove where an artifact was built. They do not prove the code is safe,
and SLSA "does not directly address" malicious source ([SLSA
threats](https://slsa.dev/spec/v1.1/threats-overview)).
Policy-controller only checks namespaces labelled for inclusion, and
policies can run in `warn` mode
([Sigstore](https://docs.sigstore.dev/policy-controller/overview/)).

### Identity, IAM and credentials: the agent cannot misuse what it never holds

[Inference] An identity control is enforced by the system that holds the
resource, so it holds even if the agent is hijacked. OWASP ASI03 says
that without "a distinct, governed identity of its own, an agent
operates in an attribution gap that makes enforcing true least privilege
impossible". It calls for "short-lived, narrowly scoped tokens per task"
capped by permission boundaries ([OWASP Agentic Top
10](https://genai.owasp.org/download/52117/?tmstv=1765059207)). Concrete
forms in the notes include:

- GitHub App installation tokens that "expire after 1 hour" and can be
  narrowed per request to specific repositories and permissions
  ([GitHub](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)).
- OIDC federation, where the cloud token "is only valid for a single
  job" ([GitHub
  OIDC](https://docs.github.com/en/actions/concepts/security/openid-connect)).
- Vault dynamic secrets with unique per-service credentials
  ([Vault](https://developer.hashicorp.com/vault/docs/secrets/databases)).
- Entra PIM's time-bound, approval-gated elevation ([Microsoft
  Learn](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-configure)).
- MCP's progressive scopes with step-up challenges ([MCP
  security](https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices)).

Ceilings that the agent's own admin rights cannot lift are the strongest
form. An SCP blocks a permission "even if the account administrator
attaches the `AdministratorAccess` IAM policy" ([AWS
SCPs](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)).
GCP Organization Policy inherits down the hierarchy
([GCP](https://docs.cloud.google.com/resource-manager/docs/organization-policy/overview)).

These controls cap blast radius equally for mistakes and attacks. They
do not stop misuse of authority the agent legitimately holds, which
OWASP files separately as ASI02 ([OWASP Agentic Top
10](https://genai.owasp.org/download/52117/?tmstv=1765059207)).
[Inference] A hijacked agent inherits whatever the token can do for its
lifetime, and a short TTL bounds a session-length attack but does not
prevent it. The guardrails also have documented holes. SCPs "don't
affect users or roles in the management account" or service-linked
roles, and permissions boundaries "do not limit resource-based policies"
([AWS
SCPs](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html),
[AWS
boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html)).
Token passthrough lets "an attacker compromising one service ... access
other connected services", so MCP servers "MUST NOT accept any tokens
that were not explicitly issued for the MCP server" ([MCP
security](https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices)).
Stdio MCP servers simply "retrieve credentials from the environment"
([MCP
authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)).
[Inference] An identity gate is therefore only real if no broader
credential is reachable in the agent's environment: no developer token,
no cached SSO, no `~/.aws` profile, and no metadata endpoint at
`169.254.169.254` ([MCP
security](https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices)).
Break-glass credentials must stay out of reach entirely, since AWS calls
them potentially "a backdoor" and wants their use alerted ([AWS
SEC03-BP03](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_permissions_emergency_process.html)).
Audit logs in the resource owner's system survive agent compromise.
[Inference] They are still detective: they never satisfy a "must hold"
rule unless paired with automated revocation.

### Network egress and DNS: filtering is not a boundary

Protective DNS "prevents malicious or suspicious communication streams
from starting". NIST also warns that resolvers with internet access let
attackers use authoritative servers "for command and control (C2) and
data exfiltration" ([NIST SP
800-81r3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-81r3.pdf)).
Real agent incidents used exactly this channel. The Claude Code advisory
above did. [Practitioner] Zenity Labs found that in Claude's
code-execution sandbox "DNS resolution happens before those filters can
intervene" despite HTTP egress blocking, and built a bidirectional DNS
shell ([Zenity
Labs](https://labs.zenity.io/post/it-s-always-dns-in-claude-s-sandbox-from-data-exfiltration-to-a-bidirectional-dns-shell)).
An enforced egress boundary needs three things:

- default-deny at the IP and port layer, outside the agent's
  environment;
- only an approved resolver allowed out, with outbound 53, DoT and DoQ
  on 853, and known DoH endpoints blocked ([NIST SP 800-81r3
  §4.2.2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-81r3.pdf));
- either no general DNS for the sandbox, or resolver logging with
  tunneling detection based on volume and QNAME entropy ([NIST
  §4.2.4](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-81r3.pdf))
  [Inference].

Against honest mistakes, an allowlist is very effective. Against prompt
injection, it only shrinks the set of channels [Inference]. A hostname
allowlist "does not terminate or inspect encrypted traffic", domain
fronting is possible, and "allowing broad domains such as `github.com`
can create paths for data exfiltration" ([Secure
deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment),
[Sandboxing](https://code.claude.com/docs/en/sandboxing)). Default
"Trusted" lists include user-content hosts such as `gist.github.com` and
`raw.githubusercontent.com` ([Claude Code cloud
environments](https://code.claude.com/docs/en/cloud-environments)).
Codex's GET-only option narrows the channels, but [Inference] data can
still ride in GET paths and query strings ([Codex
cloud](https://learn.chatgpt.com/docs/cloud/internet-access)).

Vendors document their own carve-outs:

- Claude Code cloud sessions always reach GitHub through a separate
  proxy, enabled MCP connectors, and "The Anthropic API ... even at
  None" ([cloud
  environments](https://code.claude.com/docs/en/cloud-environments)).
- Copilot's firewall "only applies to processes started by the agent via
  its Bash tool", not to MCP servers or setup steps, and "should not be
  considered a comprehensive security solution"
  ([GitHub](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/customize-the-agent-firewall)).
- Codex setup scripts "still run with internet access" ([Codex
  cloud](https://learn.chatgpt.com/docs/cloud/internet-access)).

For CI, harden-runner offers audit-then-block domain allowlists. It is
"a no-op on self-hosted runners" without an Enterprise subscription, and
audit-only on hosted Windows and macOS runners
([harden-runner](https://github.com/step-security/harden-runner)).
[Inference] A firewall started by a repo-controlled script, such as a
dev container `postStartCommand` or a workflow step, contains the
agent's runtime actions but not a PR that edits it. It becomes a real
gate only when host firewall, VPC rules, runner groups or a managed
proxy enforce it. Anthropic says the same: "Because the Dockerfile lives
in the repository, anyone with write access can change or remove this
step" ([dev containers](https://code.claude.com/docs/en/devcontainer)).

### Protecting domains and DNS records from an agent with infra access

This is a different problem: keeping the organization's own zone safe
from an agent that can touch infrastructure. CISA's DNS-tampering
directive identifies the attack path as compromised credentials for "an
account that can make changes to DNS records", which also lets the
attacker "obtain valid encryption certificates". It requires MFA on such
accounts, audits of public records, and CT-log monitoring ([CISA ED
19-01](https://www.cisa.gov/news-events/directives/ed-19-01-mitigate-dns-infrastructure-tampering)).
The notes classify the controls as follows:

| Control | Class | What it does and does not do |
|---|---|---|
| Registry lock (`server*Prohibited` EPP statuses) | Gate | Set by the registry; "some Registry Operators offer a Registry Lock Service" against unauthorized updates ([ICANN](https://www.icann.org/resources/pages/epp-status-codes-2014-06-16-en)) |
| Registrar lock (`client*Prohibited`) | Weak gate | Set by the registrar ([ICANN](https://www.icann.org/resources/pages/epp-status-codes-2014-06-16-en)). [Inference] Anyone holding the registrar account, including an agent whose credential reaches the registrar API, can remove it |
| Separate DNS/registrar accounts with MFA | Gate | Agent credentials exclude them ([CISA ED 19-01](https://www.cisa.gov/news-events/directives/ed-19-01-mitigate-dns-infrastructure-tampering)) |
| IaC apply behind a protected environment, self-review prevented | Gate | Secrets are released only after approval ([GitHub environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)) |
| CAA | Third-party constraint | Binds only compliant CAs; "Suppression of a CAA record or insertion of a bogus CAA record" enables misissuance ([RFC 8659](https://www.rfc-editor.org/rfc/rfc8659)) |
| DNSSEC | Third-party constraint | Origin authentication and integrity, but no "access control lists" or DoS protection; misconfiguration can make zones "effectively unreachable" ([RFC 4033](https://www.rfc-editor.org/rfc/rfc4033)) |
| CT monitoring, record audits, DMARC/`iodef` reports, dangling-CNAME checks | Detection | ([CISA](https://www.cisa.gov/news-events/directives/ed-19-01-mitigate-dns-infrastructure-tampering), [RFC 7489](https://www.rfc-editor.org/rfc/rfc7489), [NIST SP 800-81r3 §3.6](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-81r3.pdf)) |

[Inference] Routine infra work by an agent can break several kinds of
record:

- NS/DS records, causing an outage or a validation failure.
- MX/SPF/DKIM/DMARC records. A `ruf=` edit redirects failure reports,
  which RFC 7489 says may contain "actual email content" ([RFC
  7489](https://www.rfc-editor.org/rfc/rfc7489)).
- CAA records.
- CNAMEs left dangling after a cloud resource is deleted. NIST describes
  these as a takeover risk and says they "should be deleted" ([NIST SP
  800-81r3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-81r3.pdf)).

[Inference] The strongest pattern has the agent propose DNS changes as
IaC in a PR. Plan runs with read-only credentials, and apply runs with a
credential held only by a protected environment whose approval the
agent's identity cannot give. NS, DS and transfer changes stay out of
IaC entirely, behind registry lock and a separate human account.
Comment-triggered IaC is a bypass: Anthropic advises disabling auto-fix
"for repositories where a PR comment can deploy infrastructure" ([Claude
Code on the
web](https://code.claude.com/docs/en/claude-code-on-the-web)). The notes
found no source that addresses agent-specific DNS or registrar access
directly, so this mapping is inference from general DNS guidance.

### Isolation: containment of reach, never a business rule

The isolation ladder runs from OS sandbox to container to gVisor to VM
or microVM to hosted sandbox. NIST says containers "do not offer as
clear and concrete of a security boundary as a VM" because of the shared
kernel ([NIST SP
800-190](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf)).
gVisor shrinks the attack surface at a cost of up to "10-200× slower"
heavy file I/O. Firecracker boots in "<125ms" with "only 5 emulated
devices" ([Secure
deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment),
[Firecracker](https://firecracker-microvm.github.io/)). Anthropic
recommends "a dedicated virtual machine, or a cloud session" for
untrusted repositories ([Sandbox
environments](https://code.claude.com/docs/en/sandbox-environments)).
The most useful outer pattern puts credentials outside the boundary.
With `--network none` plus a proxy socket, "even if the agent is
compromised via prompt injection, it cannot exfiltrate data to arbitrary
servers" ([Secure
deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)).

What isolation cannot do is equally explicit: "Any approach that allows
network egress can still leak data the agent can read, and any approach
that mounts your project directory writable can still modify that code".
In addition, "Isolation also does not change what is sent to the model"
([Sandbox
environments](https://code.claude.com/docs/en/sandbox-environments)).
Read-only mounts still expose `.env`, `~/.aws/credentials` and `.npmrc`
([Secure
deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)).
A committed dev container "is a convention rather than an enforcement
boundary". It becomes enforced only through device management or
software allowlisting ([Sandbox
environments](https://code.claude.com/docs/en/sandbox-environments)).
[Inference] Isolation answers *where* the agent runs and *what it can
reach*. It never encodes "don't touch prod table X", and against honest
mistakes a container with no host secrets and a disposable workspace
already removes most blast radius. All three vendors restrict bypass
modes to external boundaries. Codex's bypass flag is "intended solely
for running in environments that are externally sandboxed"
([openai/codex](https://github.com/openai/codex/blob/main/codex-rs/utils/cli/src/shared_options.rs)).
Anthropic: "Always run `--dangerously-skip-permissions` sessions inside
a container, a VM, or the sandbox runtime" ([Sandbox
environments](https://code.claude.com/docs/en/sandbox-environments)).

### Policy engines, limits, recovery and DLP

Policy engines intercept at four points:

- CI: Conftest/OPA on files and plans
  ([Conftest](https://www.conftest.dev/), [OPA
  Terraform](https://www.openpolicyagent.org/docs/terraform)).
- IaC run: HCP Terraform Sentinel/OPA between plan and apply ([HCP
  Terraform](https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement)).
- Cluster admission: Gatekeeper and Kyverno on every create, update and
  delete
  ([Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/),
  [Kyverno](https://kyverno.io/docs/introduction/)).
- Cloud control plane: SCPs and GCP Organization Policy.

They evaluate the artifact or API call, not the agent, so they apply
equally to a human, an agent and a hijacked agent. OPA's Terraform
examples include restricting IAM changes and a "blast radius" score
([OPA](https://www.openpolicyagent.org/docs/terraform)). Their weak
points are override paths. "Advisory" failures "never interrupt the
run", soft-mandatory can be overridden by configured team members, and
OPA "Mandatory" can be overridden by anyone with "Manage Policy
Overrides" ([HCP policy
sets](https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement/manage-policy-sets)).
[Inference] In-repo CI policy helps only against honest mistakes.
Admission and cloud-API policy hold even for changes that never went
through a PR. All of these check structure, not intent, so a logically
wrong but compliant change passes. Google concurs that policies "often
lack deep contextual understanding"
([Google](https://storage.googleapis.com/gweb-research2023-media/pubtools/1018686.pdf)).

Limits ignore intent and bound magnitude only. Real caps include:

- Anthropic workspace spend and rate limits, which can be set "lower
  than (but not higher than)" organization limits, plus per-user spend
  limits in the Claude Code workspace ([Claude
  Platform](https://platform.claude.com/docs/en/manage-claude/workspaces)).
- CI `timeout-minutes`, which defaults to 360 ([GitHub workflow
  syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)).
- Container `--memory`, `--pids-limit` and `--cpus` ([Secure
  deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)).
- AWS budget actions that apply an IAM policy or SCP ([AWS
  Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-controls.html)).

An alerts-only GCP budget "doesn't automatically cap" spending
([GCP](https://docs.cloud.google.com/billing/docs/how-to/budgets)).

Backups and point-in-time recovery prevent nothing ([RDS
PITR](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html)).
They survive a compromised agent only in a locked vault, where even root
deletes are denied. Governance-mode locks can be removed with IAM
permissions; compliance mode becomes immutable after "at least 3 days
(72 hours)" ([AWS Backup Vault
Lock](https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html)).
[Inference] Recovery cannot undo exfiltration, sent messages or
published packages. DLP is detection unless it is wired in-line, as push
protection is
([GitHub](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection))
or redaction before storage is ([Google
SDP](https://docs.cloud.google.com/sensitive-data-protection/docs/sensitive-data-protection-overview)).
In-line DLP is a gate on that one channel only.

### Summary matrix

| Family | Honest mistakes | Compromised / injected agent | Cannot do | Real only if |
|---|---|---|---|---|
| Merge rules | Catches what reviewers see | Requires a second identity | Stop rubber-stamping; bind admins or bypass actors | Agent is not on a bypass list; requester and last pusher excluded; stale approvals reset |
| Required CI checks | Deterministic catch | Holds if definition and source are pinned | Judge intent | Required on the ref; pinned app; workflow protected; no privileged trigger on agent code |
| Scanners | Catch known patterns | Only with protected config | Catch new malicious packages (SCA) or novel logic | Ignore files, baselines and workflows under code owners or org config |
| Identity / IAM | Caps blast radius | Caps blast radius | Stop misuse of granted rights | No broader credential reachable; ceiling outside the agent's admin |
| Egress / DNS | Very effective | Shrinks channels | Inspect payloads; close allowed write hosts | Enforced outside the environment; resolver controlled |
| DNS record protection | Prevents breaking records | Prevents hijack | Stop authorized-but-wrong changes (DNSSEC) | Separate accounts, registry lock, approval-gated apply |
| Isolation | Contains damage | Contains host damage | Stop leaks of readable data over egress | No host secrets; boundary not repo-editable |
| Policy engines | Block bad structure | Hold at admission or API | Judge logic | Agent lacks override permission |
| Limits | Stop loops | Bound magnitude | Stop one harmful action under the cap | Hard caps, not alerts |
| Recovery / DLP | Restore; detect | Only if immutable or in-line | Undo disclosure | Vault lock; in-line placement |

All rows are [Inference] syntheses of the sourced findings above.

## Seven conditions turn a control into a gate

Most failures across the families come from the same short list of
prerequisites. [Inference] Before calling something an outside gate,
harness-forge should verify each of the following:

1. **It targets the real refs and resources.** The rule covers default
   and release branches and tags, or the actual production accounts and
   zones.
2. **The agent's identity is excluded from every bypass and override
   path.** This covers the bot, the app, the token, and the human whose
   token the agent uses. It includes ruleset bypass lists, admin rights,
   "Bypass policies when pushing" ([Azure
   Repos](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies)),
   Sentinel/OPA overrides, the SCP management account, and
   governance-mode vault locks.
3. **Approval comes from an identity other than the author, the last
   pusher and the launching user, and resets on new pushes.**
4. **The gate's definition sits outside the change's reach.** Check
   sources are pinned, and workflow, scanner and policy files sit under
   code owners or come from outside the repository at a pinned ref.
   CODEOWNERS owns itself.
5. **No broader credential or channel bypasses the gate.** No personal
   token, metadata endpoint or unrestricted resolver is reachable, and
   allowlisted hosts are not writable with the agent's credentials.
6. **The feature is enforced on the user's plan and repository
   visibility.** For example, rulesets cover private repositories only
   on Pro, Team and Enterprise Cloud ([GitHub
   rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)).
   GitLab approval settings, push rules and deployment approvals require
   Premium or Ultimate
   ([GitLab](https://docs.gitlab.com/user/project/repository/push_rules/)).
   Bitbucket Cloud checks only warn below Premium.
7. **It is verified periodically.** Gate configuration drifts silently.
   OpenSSF Scorecard checks branch protection but needs an admin token
   to see `DismissStaleReviews`, `EnforceAdmins` and
   `RequireLastPushApproval` ([OpenSSF
   Scorecard](https://github.com/ossf/scorecard/blob/main/docs/checks.md)).

[Inference] Review is also where agent volume creates pressure. Required
human approval scales with PR count, which tempts teams to add the
agent's bot to bypass lists or enable "Actions can approve PRs". Either
change removes the gate against a compromised agent, and the forge
should flag both as gate-defeating.

## Four outcomes from six intake questions

The forge's job per part of an idea is to answer two different
questions. "May the agent skip it?" decides between guidance
(instructions, skills) and harness enforcement (hooks, permissions).
"Must it hold if the agent or its config is hostile?" decides whether
enforcement moves outside the harness ([Inference], from [OWASP
LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) and
[Google](https://storage.googleapis.com/gweb-research2023-media/pubtools/1018686.pdf)).
The notes propose six intake questions, all [Inference] grounded in the
cited criteria:

| # | Intake question | Implied outcome |
|---|---|---|
| 1 | Must this hold even if the agent is manipulated by prompt injection, or its config is changed by a PR? | Yes: an outside gate is required, and a harness piece is optional. No: a harness mechanism may suffice. |
| 2 | Who should be able to turn this off? | The agent or any contributor: harness or committed config is fine. Only an admin: outside gate (rulesets, managed settings / `requirements.toml`, IAM). Managed settings are admin-owned but still harness-side, and GHSA-gfvf showed server-managed policy being skipped ([advisory](https://github.com/anthropics/claude-code/security/advisories/GHSA-gfvf-j8jh-jxxw)). |
| 3 | Does the event happen without an agent (merge, deploy, publish, credential scope, egress)? | Yes: outside gate alone. A harness build adds no enforcement. |
| 4 | Is the action irreversible, money-related, or does it publish or disclose data? | Yes: human approval or a block in an outside gate, with a harness ask-prompt as a convenience ([OWASP Agentic Top 10](https://genai.owasp.org/download/52117/?tmstv=1765059207), [Google](https://storage.googleapis.com/gweb-research2023-media/pubtools/1018686.pdf)). |
| 5 | Is the outside control available on the user's plan for this repository's visibility? | No: say so, offer the harness piece with a "not a guarantee" warning, or report that nothing fits if the goal demands a guarantee. |
| 6 | Does the user want earlier feedback than the gate gives? | Yes: add a harness mirror (hook or skill) of the same check, flagged as advisory. |

The answers map to the four outcomes. Every row below is [Inference]
from the notes' decision rules.

| Outcome | When | Examples from the notes |
|---|---|---|
| **Outside gate instead of any harness build** | Rule constrains an event the agent cannot perform without passing the gate, and no earlier feedback is wanted | "Never merge without review" (required approvals, requester cannot approve); "no prod deploy without sign-off" (environment approval); "agent token may only push branches"; "no public buckets" (org policy/SCP); "max spend" (workspace spend limit); "DNS/registrar changes need a human" (separate credentials, registry lock) |
| **Outside gate alongside a harness mechanism** | Rule must survive compromise, and in-loop feedback saves iterations; or the rule protects agent config itself | "Tests pass before merge" (required check plus a Stop/PostToolUse hook); "no secrets in commits" (push protection plus a pre-commit or edit hook); a Conftest hook mirroring CI/admission policy; deny-edit on `.claude/` plus code owners; "only migrate the dev DB" when one credential reaches both; local CLI using a personal cloud profile |
| **Harness mechanism (or OS isolation) only** | Local actions no forge or cloud gate sees, or low-impact workspace conventions | "Don't read `~/.ssh`", "no `rm -rf` outside the repo", "don't exfiltrate local env vars": sandbox, container or VM, which the intake should still class as outside the model ([Claude Code security](https://code.claude.com/docs/en/security)); formatting and test-before-done conventions |
| **Nothing** | No enforcement point and no feedback value; or read-only public data where the agent identity already lacks write rights | OWASP's least agency: do not add agentic behavior "where it is not needed" ([OWASP Agentic Top 10](https://genai.owasp.org/download/52117/?tmstv=1765059207)); domain hygiene such as DNSSEC, CAA, DMARC and CT monitoring needs nothing in the harness beyond "the agent's credentials must not edit these records" |

Some patterns force isolation regardless of the questions above.
[Inference] Any bypass or no-prompt mode, any untrusted repository, and
any combination of untrusted input with secrets and egress require an
outer boundary. That combination is Simon Willison's "lethal trifecta"
of private data, untrusted content and external communication.
[Practitioner] He writes that "we still don't know how to 100% reliably
prevent this"
([simonwillison.net](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)).
In addition, any recommendation of "agent may open PRs" must come with a
merge rule. [Inference] Without one, the outer control that GitHub's and
Anthropic's agents assume is missing.

The "build it anyway" override fits the same structure. When the user
insists on a harness mechanism where the forge recommended an outside
gate, or where the gate is unavailable on their plan, the forge builds
it. It labels the result advisory: it gives earlier feedback, but the
agent or a PR can edit it, and it has a bypass history ([Claude Code
advisories](https://github.com/anthropics/claude-code/security/advisories)).
The [harness-forge
design](../../specs/2026-10-06-harness-forge-design.md) adds one firm
limit: a chosen mechanism that cannot meet a *stated* goal, such as
"must hold under prompt injection", stays an error rather than a silent
downgrade. [Inference] The override therefore changes what gets built,
never what the forge claims the build guarantees. Economy of mechanism
is the forge's argument against building a duplicate when the user does
not override: keep the design "as simple and small as possible"
([Saltzer and
Schroeder](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html)).

## Conclusion

The useful shift is from asking "which tool?" to asking "who enforces
it, and can the agent's identity reach that enforcer?" Across forges,
clouds, networks and registries, the gates that matter share one
property: a principal other than the agent decides, and nothing the
agent can write or hold changes that decision. Most real failures in the
notes are failures of that property, not of the tools. Examples are an
over-scoped CI token, a privileged workflow on untrusted input, an admin
bypass, an in-repo ignore file, a repo-shipped firewall script, and a
DNS channel left open under an HTTP block. Harness-forge should
therefore recommend an outside gate together with its prerequisites, and
treat a missing prerequisite as the most likely way the recommendation
fails silently.

Two limits stay open and should be stated rather than hidden. No outside
gate stops misuse of authority the agent legitimately holds, or leakage
through a channel the work requires (GitHub, a package registry, the
model API). The only answers there are narrower credentials and
separating untrusted-content readers from secret holders. The evidence
base is also thin in places. No primary postmortem in the notes shows an
outside gate stopping a coding agent mid-harm, NIST agent-identity
guidance is still a set of questions, and plan-tier availability changes
over time. The forge should date-stamp tier claims and re-verify them
before relying on them.
