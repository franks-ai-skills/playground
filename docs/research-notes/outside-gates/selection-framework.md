# Outside gates for coding agents: when to recommend a control outside the harness

Scope: decision criteria for harness-forge's intake (step 7, "Recommendation") on when a part
should get an outside gate (CI, merge rules, scanners, IAM, egress, isolation, policy engines,
deployment approvals) instead of, or alongside, a harness mechanism. All sources fetched
2026-10-07. Quotes are verbatim from the fetched page. Repo context read first:
`docs/overview.md` ("Guidance is advisory, enforcement is mechanical ... CI is the last gate and
depends on no agent setting"), `docs/guide/security.md` ("Place enforced policy outside
agent-writable state"; "Prompts and 'no write tools' are supporting controls, not sufficient
confidentiality boundaries"), and the spec's harness-intake / Decisions sections (outcome
"a control outside the harness"; CI is a gate only once branch protection requires it).

## 1. What authoritative guidance says about where agent controls must live

### Takeaway
Every authoritative source fetched says the same thing in different words: the decision whether
an agent action is allowed must be enforced by a deterministic mechanism outside the model's
reasoning (downstream authorization, policy engines, OS sandbox, repository rules), with least
privilege and human approval for high-impact or irreversible actions; model judgment and prompt
instructions are a supporting layer only. Coding-agent vendors themselves rely on outside
controls (branch protection, required checks, VM isolation, egress limits) for their own
products' safety guarantees.

### Cited Findings

**OWASP Top 10 for LLM Applications 2025, LLM06 Excessive Agency** ([genai.owasp.org](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/))
- Complete mediation, verbatim: "Implement authorization in downstream systems rather than relying on an LLM to decide if an action is allowed or not. Enforce the complete mediation principle so that all requests made to downstream systems via extensions are validated against security policies."
- Least privilege: "Limit the permissions that LLM extensions are granted to other systems to the minimum necessary in order to limit the scope of undesirable actions."
- Minimize extensions: "Limit the extensions that LLM agents are allowed to call to only the minimum necessary."
- User context: "Track user authorization and security scope to ensure actions taken on behalf of a user are executed on downstream systems in the context of that specific user, and with the minimum privileges necessary."
- Human approval, and where it can live: "Utilise human-in-the-loop control to require a human to approve high-impact actions before they are taken. This may be implemented in a downstream system (outside the scope of the LLM application) or within the LLM extension itself."

**OWASP Top 10 for Agentic Applications 2026** (published 9 December 2025; [resource page](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), [PDF](https://genai.owasp.org/download/52117/?tmstv=1765059207))
- Risk list: ASI01 Agent Goal Hijack, ASI02 Tool Misuse & Exploitation, ASI03 Identity & Privilege Abuse, ASI04 Agentic Supply Chain Vulnerabilities, ASI05 Unexpected Code Execution (RCE), ASI06 Memory & Context Poisoning, ASI07 Insecure Inter-Agent Communication, ASI08 Cascading Failures, ASI09 Human-Agent Trust Exploitation, ASI10 Rogue Agents.
- Least agency: "We expand on the concepts of Least-Privilege and Excessive Agency by citing Least-Agency. This captures our advice to organizations to avoid unnecessary autonomy; deploying agentic behavior where it is not needed expands the attack surface without adding value."
- ASI02 mitigation, outside enforcement: "Define per-tool least-privilege profiles (scopes, maximum rate, and egress allowlists) ... Where possible, express these profiles as IAM or authorization policy stanzas attached to each t[ool]" (text cut at extraction boundary).
- ASI02 mitigation: "Policy Enforcement Middleware ('Intent Gate'). Treat LLM or planner outputs as untrusted. A pre- execution Policy Enforcement Point (PEP/PDP) validates intent and arguments, enforces schemas and rate limits, issues short-lived credentials, and revokes or audits on drift."
- ASI08 mitigation: "Independent policy enforcement: Separate planning and execution via an external policy engine to prevent corrupt planning from triggering harmful actions." and "Output validation and human gates: Checkpoints, governance agents, or human review for high risk before agent outputs are propagated downstream."
- ASI05 mitigation (code execution, most relevant to coding agents): "Access control and approvals: Require human approval for elevated runs; keep an allowlist for auto-execution under version control; enforce role and action-based controls." and "Code analysis and monitoring: Do static scans before execution; enable runtime monitoring".

**Google, "An Introduction to Google's Approach for Secure AI Agents"** (Díaz and Olive, 2025; [research.google](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/), [PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/1018686.pdf))
- Neither layer alone: "purely reason- ing-based security (relying solely on the AI model's judgment) is insuffi cient because current LLMs remain susceptible to manipulations like prompt injection and cannot yet off er suffi ciently robust guarantees. Neither approach is suffi cient in isolation".
- Layer 1 lives outside the model: "deterministic security mechanisms, which Google calls policy engines, that operate outside the AI model's reasoning process. These engines monitor and control the agent's actions before they are executed, acting as security chokepoints."
- Policy engine outcomes: "it can allow the action, block it if it violates a critical policy, or require user confirmation. This deterministic enforcement provides reliable and predictable hard limits, is testable and auditable, and effectively limits the worst-case impact of agent mal- function".
- Limits of policy engines: "Defining comprehensive policies for vast action eco- systems is complex and difficult to scale. Furthermore, policies often lack deep contextual understanding".
- Reasoning defenses are inadequate for irreversible actions: "these strategies are non-deterministic and cannot provide absolute guarantees ... This makes them inadequate, on their own, for scenarios demanding absolute safety guarantees, especially involving critical or irreversible actions. They must work in concert with deterministic controls."
- Principles: "agents must operate under well-defined human control, their powers must be carefully limited accord- ing to risk and purpose, and their actions and planning must be observable".

**Google SAIF, agent controls** ([saif.google/focus-on-agents](https://saif.google/focus-on-agents))
- Agent User Control: "Ensure user approval for any actions performed by agents/plugins that alter user data or act on the user's behalf."
- Agent Permissions: "Use least-privilege principle as the upper bound on agentic system permissions to minimize the number of tools that an agent is permitted to interact with and the actions it is allowed to take."
- Agent Observability: "Ensure an agent's actions, tool use, and reasoning are transparent and auditable through logging".
- Rogue Actions: "Mitigating Rogue Actions requires a multi-layered defense ... Within orchestration, govern the agent's capabilities with observability, policy engines, and credentialed tool access".

**NCSC (UK) Guidelines for secure AI system development** (published and reviewed 27 November 2023, version 1.0; [collection](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development))
- Secure design ([page](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development/guidelines/secure-design)): "if AI components need to trigger actions, for example amending files or directing output to external systems, you apply appropriate restrictions to the possible actions (this includes external AI and non-AI fail-safes if necessary)"; "you apply least privilege principles to limit access to a system's functionality"; "you explain riskier capabilities to users and require users to opt in to use them".
- Secure deployment ([page](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development/guidelines/secure-deployment)): "This includes appropriate segregation of environments holding sensitive code or data."; "When configuration is necessary, the default option should be broadly secure against common threats (that is, secure by default)."; "The inevitability of security incidents affecting your AI systems is reflected in your incident response, escalation and remediation plans."
- The collection page describes alignment with "'secure by design principles' published by CISA, the NCSC and international cyber agencies".

**NIST**
- NIST AI 600-1 (Generative AI Profile, July 2024; [PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)): "Organizations' use of GAI systems may also warrant additional human review, tracking and documentation, and greater management oversight." (The profile contains no occurrence of "least privilege" or "permissions"; see Gaps.)
- NIST SP 800-218A (July 2024; [CSRC](https://csrc.nist.gov/pubs/sp/800/218/a/final)) is the SSDF community profile for "Generative AI and Dual-Use Foundation Models"; it targets AI model and system producers' development practices, not runtime control of a coding agent (see Gaps).

**Anthropic, Claude Code security** ([code.claude.com/docs/en/security](https://code.claude.com/docs/en/security))
- "You're responsible for reviewing proposed code and commands for safety before approval."
- "The boundary is a permission prompt, so a Bash command you approve can still write anywhere your user account can" (working-directory boundary), and "To restrict Bash commands at the operating system level, turn on sandboxing".
- "A deny rule matches the command as written; for network enforcement that doesn't depend on the command text, see sandbox network isolation".
- "Use virtual machines (VMs) to run scripts and make tool calls, especially when interacting with external web services"; "For additional isolation, run the whole Claude Code (local mode) process inside the sandbox runtime or a dev container".
- "While these protections significantly reduce risk, no system is completely immune to all attacks."
- Team: "Use managed settings to enforce organizational standards"; "Audit or block settings changes during sessions with ConfigChange hooks".
- Cloud sessions defer to repository rules: "GitHub decides which branches a session can update by applying your repository's branch protection rules and rulesets to the GitHub access you connected. A rule that access can bypass doesn't block a session's push". Self-hosted: "isolation, network egress, and git credentials are your deployment's responsibility".

**OpenAI Codex** ([agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security); developers.openai.com/codex/security now 308-redirects there)
- "By default, the agent runs with network access turned off. Locally, Codex uses an OS-enforced sandbox that limits what it can touch (typically to the current workspace), plus an approval policy that controls when it must stop and ask you before acting."
- Protected paths: "<writable_root>/.git is protected as read-only whether it appears as a directory or file."
- "Use caution when enabling network access or web search in Codex. Prompt injection can cause the agent to fetch and follow untrusted instructions."
- Admin layer: the page points to "Managed configuration for the administrator-side requirements.toml shape".
- Cloud internet access ([page](https://learn.chatgpt.com/docs/cloud/internet-access), titled "Codex Cloud (Legacy)", date-sensitive): "By default, Codex blocks internet access during the agent phase. Setup scripts still run with internet access"; risks listed: "Prompt injection from untrusted web content Code or secret exfiltration Downloading malware or vulnerable dependencies"; "To reduce risk, allow only the domains and HTTP methods you need, and review the agent output and work log."; "Point Codex only to trusted resources and keep internet access as limited as possible."

**GitHub Copilot cloud agent** ([risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/coding-agent/risks-and-mitigations); GitHub now calls it "cloud agent")
- "Only users with write access to the repository can trigger Copilot cloud agent to work. Comments from users without write access are never presented to the agent."
- "a new copilot/ branch is created for Copilot, and the agent can only push to that branch. The agent is also subject to any branch protections and required checks for the working repository."
- "Copilot cloud agent can only perform simple push operations. It cannot directly run git push or other Git commands."
- "Draft pull requests created by Copilot cloud agent must be reviewed and merged by a human. Copilot cloud agent cannot mark its pull requests as 'Ready for review' and cannot approve or merge a pull request."
- "By default, workflows are not triggered until Copilot cloud agent's code is reviewed and a user with write access to the repository clicks the Approve and run workflows button. Optionally, you can configure Copilot to allow workflows to run automatically."
- "Prevents the user who asked Copilot cloud agent to create a pull request from approving it. This maintains the expected controls in the 'Required approvals' rule and branch protection."
- "When Copilot cloud agent opens a pull request under its own app identity, one more approval is required before it can be merged, as long as the repository already requires at least one approval. This is enabled by default in rulesets, where administrators can turn it off".
- "To mitigate this risk, GitHub restricts Copilot cloud agent's access to the internet."

### Inferences
- [Inference] The sources converge on a split the intake can encode: "may the agent skip it?" is answered by the harness question (instructions/skills vs hooks/permissions), but "must it hold even if the agent or its config is hostile?" moves the control out of the harness to a downstream PEP (OWASP LLM06 complete mediation; Google Layer 1; OWASP ASI02 "Intent Gate").
- [Inference] OWASP LLM06 explicitly allows human approval "within the LLM extension itself", so a harness approval prompt is legitimate for high-impact actions, but only an outside approval (required review, deployment approval) survives a compromised or reconfigured agent.
- [Inference] GitHub's own safety story for its agent relies on branch protection and required approvals being configured; Anthropic's cloud sessions likewise defer push authorization to "your repository's branch protection rules and rulesets". A forge recommending "agent may open PRs" without a merge rule leaves the vendor's assumed outer control missing.

### Gaps
- CISA's joint guidance "Deploying AI Systems Securely" (April 2024) could not be fetched: the cisa.gov resource URL returned 404 and the media.defense.gov PDF download failed. No CISA-specific quote is included.
- NIST AI 600-1 and SP 800-218A contain no runtime-control guidance for tool-using agents that I could find (no "least privilege" or "permissions" in AI 600-1's text). No NIST agent-specific profile was located in this pass.
- Google SAIF's agent page did not contain explicit text weighing model-config vs external enforcement beyond the control list; the Google paper is the source for that argument.

## 2. Control taxonomy for classifying gates

### Takeaway
Saltzer and Schroeder's principles (complete mediation, least privilege, separation of privilege,
fail-safe defaults, compromise recording) and NIST's reference-monitor definition (always invoked,
tamperproof, verifiable) give the forge a test for whether a control is a real gate: it must
mediate every path, be outside the subject's control, and be small enough to verify. Agent
harness controls are partially mediating and partly agent-writable; outside gates usually meet
the tamperproof condition only if the agent's identity cannot change them.

### Cited Findings
- Saltzer and Schroeder, "The Protection of Information in Computer Systems" ([Basic principles](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html)):
  - Complete mediation: "Every access to every object must be checked for authority."
  - Least privilege: "Every program and every user of the system should operate using the least set of privileges necessary to complete the job."
  - Fail-safe defaults: "Base access decisions on permission rather than exclusion."
  - Separation of privilege: a mechanism requiring two keys is "more robust and flexible than one that allows access to the presenter of only a single key."
  - Economy of mechanism: "Keep the design as simple and small as possible."
  - Psychological acceptability: "It is essential that the human interface be designed for ease of use, so that users routinely and automatically apply the protection mechanisms correctly."
  - Work factor: "Compare the cost of circumventing the mechanism with the resources of a potential attacker."
  - Compromise recording: mechanisms that "reliably record that a compromise of information has occurred can be used in place of more elaborate mechanisms that completely prevent loss."
- NIST reference monitor ([CSRC glossary](https://csrc.nist.gov/glossary/term/reference_monitor), from SP 800-53 Rev. 5): "A reference validation mechanism is always invoked (i.e., complete mediation), tamperproof, and small enough to be subject to analysis and tests, the completeness of which can be assured (i.e., verifiable)."
- Reference validation mechanism ([CSRC glossary](https://csrc.nist.gov/glossary/term/reference_validation_mechanism), SP 800-160v1r1): "An implementation of the reference monitor concept that validates each access to resources against a list of authorized accesses allowed."
- Defense in depth ([CSRC glossary](https://csrc.nist.gov/glossary/term/defense_in_depth), SP 800-53 Rev. 5): "An information security strategy that integrates people, technology, and operations capabilities to establish variable barriers across multiple layers and missions of the organization."
- Compensating controls ([CSRC glossary](https://csrc.nist.gov/glossary/term/compensating_controls), SP 800-37 Rev. 2): "The security and privacy controls implemented in lieu of the controls in the baselines ... that provide equivalent or comparable protection".
- Google's paper names a policy engine a "security chokepoint" that intercepts requests "before they are executed" ([PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/1018686.pdf)); OWASP ASI02 names a "pre- execution Policy Enforcement Point (PEP/PDP)" ([PDF](https://genai.owasp.org/download/52117/?tmstv=1765059207)).

### Inferences
- [Inference] Classification the intake can apply per proposed control:
  - Preventive, inside harness: permission deny rules, sandbox, PreToolUse hooks. Mediates only the paths the harness sees (Claude docs: deny rules match "the command as written"; sandbox does not confine hooks/MCP per `docs/guide/security.md`).
  - Preventive, outside harness: branch protection/rulesets, required checks, IAM scopes, egress firewall, VM/container isolation, deployment approvals. Mediates every path into the protected object regardless of which tool the agent used.
  - Detective: CI scanners, audit logs, OpenTelemetry (Claude docs "Monitor Claude Code usage through OpenTelemetry metrics"), SAIF "Agent Observability". Saltzer's "compromise recording" justifies a detective control in place of a preventive one only when loss is recoverable.
  - Corrective: credential revocation, rollback, rebuild (the AWS and Nx postmortems in section 5 are corrective actions).
- [Inference] Tamperproof test for coding agents: a control the agent's own process or identity can edit (committed `.claude/settings.json`, hooks, CI workflow files on a branch the agent can push) is not tamperproof against that agent. Separation of privilege maps onto "the agent cannot approve its own PR" (Copilot) and "the requester cannot approve" (GitHub required approvals).
- [Inference] Economy of mechanism argues against building a harness control that duplicates an existing outside gate with no added benefit.

### Gaps
- I found no fetchable NIST glossary definitions for "preventive control", "detective control" or "corrective control" (CSRC glossary returned no definition pages for those terms). The preventive/detective/corrective split above is labelled inference, not a cited NIST definition.

## 3. Decision criteria for the intake

### Takeaway
Five criteria, each grounded in the sources, decide placement: (a) must the rule hold if the agent
or its configuration is compromised; (b) who can change the control; (c) does the rule need an
agent at all; (d) is the action irreversible or high-impact; (e) is the outside control available
on the user's platform tier. Feedback speed and friction decide whether to add a harness mirror,
not where enforcement lives.

### Cited Findings
- (a) Compromise: Google: reasoning-based defenses are "inadequate, on their own, for scenarios demanding absolute safety guarantees, especially involving critical or irreversible actions" ([PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/1018686.pdf)). OWASP: "rather than relying on an LLM to decide if an action is allowed" ([LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)). Harness controls themselves have had bypasses (section 5: sandbox escapes, approval-prompt bypasses, repo-controlled settings skipping the trust dialog) ([Claude Code advisories](https://github.com/anthropics/claude-code/security/advisories)).
- (b) Who can change it: GitHub rulesets: "People with admin access to a repository, or a custom role with the 'edit repository rules' permission, can create, edit, and delete rulesets for a repository." and "you can allow certain users to bypass the rules in the ruleset. This can be users with a certain role, such as repository administrator, or it can be specific teams or GitHub Apps." ([about rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)). Claude cloud sessions: "A rule that access can bypass doesn't block a session's push" ([Claude security](https://code.claude.com/docs/en/security)). Codex enterprise layer: administrator-side `requirements.toml` ([Codex](https://learn.chatgpt.com/docs/agent-approvals-security)). Copilot: required extra approval for agent PRs "is enabled by default in rulesets, where administrators can turn it off" ([GitHub](https://docs.github.com/en/copilot/concepts/agents/coding-agent/risks-and-mitigations)).
- Layering: "Rulesets and branch protection rules can both protect branches in a repository. They work alongside each other, and all applicable rules are enforced." and "the most restrictive version of the rule applies" ([about rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)).
- (d) Impact: OWASP "require a human to approve high-impact actions"; ASI05 "Require human approval for elevated runs" ([PDF](https://genai.owasp.org/download/52117/?tmstv=1765059207)); Google's example policy evaluates "Is it irreversible? Does it involve money?" ([PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/1018686.pdf)); NCSC "require users to opt in" for riskier capabilities ([NCSC](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development/guidelines/secure-design)).
- (e) Platform availability (date-sensitive, as of 2026-10-07): "Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations. Protected branches are also available in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server." ([about protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)). "Rulesets are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, and GitHub Enterprise Cloud." ([about rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)).
- Least agency as a criterion against building anything: "deploying agentic behavior where it is not needed expands the attack surface without adding value" ([OWASP Agentic Top 10](https://genai.owasp.org/download/52117/?tmstv=1765059207)).
- Friction: Saltzer's psychological acceptability ("users routinely and automatically apply the protection mechanisms correctly") ([Saltzer](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html)); Google notes policy engines "can overly restrict utility" and are "difficult to scale" ([PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/1018686.pdf)).

### Inferences
- [Inference] Proposed intake questions (to add to `rules/selection.yaml`), each with the implied outcome:
  1. "Must this hold even if the agent is manipulated by prompt injection or its config is changed by a PR?" Yes → outside gate required (harness piece optional). No → harness mechanism may suffice.
  2. "Who should be able to turn this off?" Agent or any contributor → harness or committed config is acceptable. Only an admin → outside gate (rulesets, managed settings / `requirements.toml`, IAM). Note: managed settings are harness-side but admin-owned; they are tamperproof against the repo, not against the local machine owner (see GHSA-gfvf in section 5).
  3. "Does the rule concern something that happens without an agent (merge, deploy, publish, credential scope, network egress)?" Yes → outside gate alone; a harness build adds nothing to enforcement. Example from the spec: "never merge without review".
  4. "Is the action irreversible, money-related, or does it publish/disclose data?" Yes → human approval or block in an outside gate; harness ask-prompt as convenience layer.
  5. "Is the outside control available on the user's plan for this repository's visibility?" No (e.g. private repo on GitHub Free) → say the gate is unavailable, recommend the harness piece with an explicit "not a guarantee" warning, or "nothing fits" if the goal demands a guarantee. This matches the spec's Override rule: a chosen mechanism that cannot meet a stated goal stays an error.
  6. "Does the user want earlier feedback than the gate gives?" Yes → add a harness mirror (hook/skill) of the same check, flagged as advisory.
- [Inference] A CI job is not tamperproof when the workflow file is editable on the PR branch and runs with privileges (Nx incident, section 5). The intake should list both "require the check" and "protect the workflow" (e.g. privileged triggers, token scopes) as prerequisites, consistent with the spec's existing branch-protection prerequisite.

### Gaps
- No authoritative source quantifies feedback speed or CI cost trade-offs for agent-run checks; criteria 6 is inference only.
- Plan availability for GitHub Enterprise Server rulesets and for GitLab/Bitbucket equivalents was not researched.

## 4. When an outside gate alone suffices, and when the harness piece is still worth it

### Takeaway
An outside gate alone suffices when the rule constrains an event the agent cannot perform without
passing the gate (merge, deploy, publish, network egress, cloud IAM) and the user does not need
earlier feedback. A harness piece is still worth adding when it shortens the feedback loop, avoids
wasted CI runs or reviewer time, or covers a local action that no outside gate sees (local file
writes, local command execution, local secrets).

### Cited Findings
- Vendors already put the merge decision outside the agent: Copilot "cannot approve or merge a pull request" and is "subject to any branch protections and required checks" ([GitHub](https://docs.github.com/en/copilot/concepts/agents/coding-agent/risks-and-mitigations)); Claude cloud sessions' pushes are decided by "your repository's branch protection rules and rulesets" ([Claude security](https://code.claude.com/docs/en/security)).
- Local actions need harness or OS isolation, since no repository gate sees them: Claude "a Bash command you approve can still write anywhere your user account can"; recommends VMs, sandbox runtime or dev container ([Claude security](https://code.claude.com/docs/en/security)). Codex: "OS-enforced sandbox that limits what it can touch" ([Codex](https://learn.chatgpt.com/docs/agent-approvals-security)).
- Egress is enforced at network level, not by command text: Claude "for network enforcement that doesn't depend on the command text, see sandbox network isolation" ([Claude security](https://code.claude.com/docs/en/security)); Codex cloud "allow only the domains and HTTP methods you need" ([Codex cloud](https://learn.chatgpt.com/docs/cloud/internet-access)); OWASP ASI02 "egress allowlists" expressed "as IAM or authorization policy stanzas" ([PDF](https://genai.owasp.org/download/52117/?tmstv=1765059207)).
- Google: the two layers have complementary weaknesses (policy engines lack context; reasoning defenses lack guarantees), so both are recommended together ([PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/1018686.pdf)).
- Claude Code ships in-session checks that mirror a later gate: "Security guidance plugin: have Claude review and fix vulnerabilities in its own code changes during the session" and "/security-review: run an on-demand security pass over the changes on your current branch" ([Claude security](https://code.claude.com/docs/en/security)).

### Inferences
- [Inference] Outside gate alone (recommend no harness build): "never merge without review" (required approvals + agent cannot self-approve); "no deploy to prod without sign-off" (deployment approval); "agent must not reach host X" in cloud runs (egress allowlist); "agent token may only push branches" (token scope / ruleset). The harness has no event to hook for these that the gate does not already mediate.
- [Inference] Both (gate enforces, harness mirrors): "tests must pass before merge" (required check enforces; a Stop/PostToolUse hook gives the agent the failure in-loop and avoids pushing red commits); "no secrets in commits" (push protection / CI scanner enforces; pre-commit hook or hook on edit catches earlier); "lint/format" (CI enforces; PostToolUse formatter prevents churn).
- [Inference] Harness or OS isolation only (no outside gate can see it): "don't read ~/.ssh", "don't run rm -rf outside the repo", "don't exfiltrate local env vars" on a developer laptop. Here the "outside" control is OS-level isolation (sandbox, container, VM), which the intake should classify as an outside-the-model control even though harnesses expose it as a setting.
- [Inference] Nothing: a rule with no enforcement point and no feedback value (least agency: don't add agentic behavior "where it is not needed").

### Gaps
- No primary source measured how many CI runs or review cycles an in-loop harness check saves; the "fewer wasted CI runs" benefit is inference.

## 5. Incidents where an outside control contained, or would have contained, damage

### Takeaway
Primary advisories show (1) harness-level controls in coding agents have repeatedly been bypassed,
so outside layers carry the guarantee; (2) supply-chain incidents around agent tooling were caused
by over-scoped CI tokens and privileged CI workflows, i.e. failures of outside gates themselves,
and were fixed with outside controls (token scoping, trusted publishing, 2FA). I found no
primary-source postmortem in this pass of a coding agent destroying data where an outside gate
contained it.

### Cited Findings
- **Amazon Q Developer for VS Code 1.84.0, CVE-2025-8217** ([AWS-2025-015](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/)): "Amazon Q Developer for VS Code Extension had an inappropriately scoped GitHub token in their CodeBuild configuration. With that access token, the threat actor was able to commit malicious code into the extension's open-source repository that was automatically included in a release." The malicious code "was distributed with the extension but was unsuccessful in executing due to a syntax error." Response: "we immediately revoked and replaced the credentials, removed the malicious code from the code base, and subsequently released ... version 1.85.0."
- **Nx malicious npm releases, 26 August 2025** ([GHSA-cxm3-wv7p-598c](https://github.com/nrwl/nx/security/advisories/GHSA-cxm3-wv7p-598c)): a PR-title bash injection in a `pull_request_target` workflow, which "runs workflows with elevated permissions including a `GITHUB_TOKEN` which has read/write repository permission", let an attacker run a malicious commit that "altered the behavior of the `publish.yml` pipeline to send the npm token to a webhook". Remediations included: "All NPM packages under Nx have been set to require 2FA and cannot be published with access tokens" and moving to "Trusted Providers methodology of publishing". The advisory also notes packages can be installed by "AI agents". (The advisory text fetched via the GitHub API does not describe the malware's use of AI CLIs; that claim is not included.)
- **Claude Code harness-control bypasses** (all fixed; [advisory list](https://github.com/anthropics/claude-code/security/advisories)):
  - [GHSA-mmgp-wc2j-qcv7](https://github.com/anthropics/claude-code/security/advisories/GHSA-mmgp-wc2j-qcv7) (2026-03-18): "A malicious repository could set `permissions.defaultMode` to `bypassPermissions` in its committed `.claude/settings.json`, causing the trust dialog to be silently skipped on first open."
  - [GHSA-ff64-7w26-62rf](https://github.com/anthropics/claude-code/security/advisories/GHSA-ff64-7w26-62rf) (2026-02-06): sandbox "failed to properly protect the .claude/settings.json configuration file when it did not exist at startup ... This allowed malicious code running inside the sandbox to create this file and inject persistent hooks (such as SessionStart commands) that would execute with host privileges when Claude Code was restarted."
  - [GHSA-7835-87q9-rgvv](https://github.com/anthropics/claude-code/security/advisories/GHSA-7835-87q9-rgvv) (2026-06-25): worktree handling enabled overwriting files such as `.zshenv`, "leading to code execution outside of seatbelt sandbox restrictions. Reliably exploiting this required the user to clone a malicious repository containing prompt injection content and run Claude Code against it."
  - [GHSA-gfvf-j8jh-jxxw](https://github.com/anthropics/claude-code/security/advisories/GHSA-gfvf-j8jh-jxxw) (2026-09-29): with a stored API key, "the session started without the organization's server-managed policy (such as permission deny rules, model restrictions and managed-only locks)"; "Endpoint-managed (MDM or file-based) settings were not affected." Fixed in 2.1.260.
  - Advisory titles on the same list include "Command Injection in find Command Bypasses User Approval Prompt" (GHSA-qgqw-h4xq-7w8w), "Permission Deny Bypass Through Symbolic Links" (GHSA-4q92-rfm6-2cqx) and "Permissive Default Allowlist Enables Unauthorized File Read and Network Exfiltration in Claude Code" (GHSA-x5gv-jw7f-j6xj).

### Inferences
- [Inference] Harness controls (approval prompts, deny rules, sandbox, managed settings) are patched software with a track record of bypasses, so a rule that must hold under compromise needs a second, independent layer outside the agent process (repository rules, IAM, egress, VM). This supports the spec's choice to put the authoritative merge gate in CI plus branch protection.
- [Inference] GHSA-mmgp and GHSA-ff64 show committed or agent-writable configuration acting as an attack vector, which directly supports intake criterion (b) "who can change the control".
- [Inference] AWS and Nx show the outside gate itself must be scoped: an over-privileged CI token or a privileged workflow on untrusted input turns the gate into the attack path. Recommending "a CI job" therefore needs least-privilege tokens and protected workflows as prerequisites, not just "required to pass".
- [Inference] In both supply-chain incidents, an outside control that would have contained the release (required human review before release, publish only via trusted publishing with 2FA) was the remediation chosen by the vendor.

### Gaps
- Widely discussed incidents of a coding agent deleting a production database (e.g. the July 2025 Replit case) rest on first-hand posts on X, which the source policy excludes; no fetchable primary postmortem was found in this pass, so no such incident is included.
- No vendor postmortem was found in which an outside gate demonstrably stopped a coding agent's harmful action (as opposed to remediation after the fact).
