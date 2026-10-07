# Code-analysis gates outside the agent harness

State as of 2026-10-07. Every source below was fetched during this
research; quotes are as returned by the fetch. Tools are examples of a
concept, not recommendations. Date-sensitive items are marked (dated).

Domains cited and their status against `docs/sources.md`:
already trusted: `arxiv.org`, `docs.github.com`, `github.blog`,
New, primary (owner of product/standard):
`slsa.dev`, `csrc.nist.gov`, `git-scm.com`, `github.com/gitleaks`,
`github.com/actions`, `docs.semgrep.dev`, `docs.sigstore.dev`,
`www.checkov.io`, `google.github.io/osv-scanner`, `trivy.dev`,
`docs.codecov.com`. New, first-hand security research:
`www.lasso.security` (the researcher's own experiment). Dropped:
`socket.dev` (vendor summary of third-party research; the figures were
re-sourced to the paper), `blog.gitguardian.com` Copilot figure (the
fetched text did not contain the number).

## 1. What each concept detects and where it can run (real gate vs advisory)

### Takeaway
Each analysis concept (SAST, SCA, secret scanning, IaC scanning,
license checks, provenance, coverage) can run at several placements;
only placements the agent cannot skip or edit are real gates: a
server-side push rejection, a required status check enforced by a
branch ruleset (ideally from a pinned source app), or an admission
controller at deploy time. Pre-commit hooks and agent-side hooks are
fast feedback, not gates.

### Cited Findings

Placements and their enforcement strength
- Client-side pre-commit hooks are bypassable by design: the pre-commit hook "can be bypassed with the `--no-verify` option" — [git githooks](https://git-scm.com/docs/githooks)
- Hooks are local, not shipped with the repository: "`git init` may copy hooks to the new repository, depending on its configuration" (hooks come from the local template, not the clone) — [git githooks](https://git-scm.com/docs/githooks)
- Server-side pre-receive is a real gate: invoked "when it reacts to `git push`"; "If it exits with non-zero status, none of the refs will be updated" — [git githooks](https://git-scm.com/docs/githooks)
- The pre-commit framework lets a committer skip a single hook: "SKIP=gitleaks git commit -m 'message'" — [gitleaks README](https://github.com/gitleaks/gitleaks)
- GitHub push protection blocks secrets "before they reach your repository", covering "Pushes from the command line", "Commits made in the GitHub UI", "File uploads", "Requests to the REST API" and "Interactions with the GitHub MCP server (public repositories only)" — [GitHub: About push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)
- Push protection is bypassable by any writer with a reason: users with write access can choose "It's used in tests", "It's a false positive" (both create a closed alert) or "I'll fix it later" (open alert); organizations can configure "delegated bypass" — [GitHub: About push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)
- (dated) Push protection at repository level "Requires GitHub Secret Protection" and is disabled by default; at user level it is "Enabled by default on GitHub.com" for pushes to public repositories — [GitHub: About push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)
- Push rulesets can block whole paths server-side: "Prevent commits that include changes in specified file paths from being pushed to the repository"; push-ruleset bypass applies to "the repository's entire fork network" — [GitHub: Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- Required status checks can be spoofed unless their source is pinned: "Any person or integration with write permissions to a repository can set the state of any status check", so "you may only want to accept a status check from a specific GitHub App" — [GitHub: Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- "Require code scanning results" blocks merge when "a required tool finds a code scanning alert of a severity that is defined in the ruleset", when analysis is ongoing, or when the tool is not configured — [GitHub: Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- Thresholds for code-scanning merge protection: alerts "None, Errors, Errors and Warnings, or All"; security alerts "None, Critical, High or higher, Medium or higher, or All" — [GitHub: Set code scanning merge protection](https://docs.github.com/en/code-security/code-scanning/managing-your-code-scanning-configuration/set-code-scanning-merge-protection)
- "Require review from Code Owners": "Any pull request that modifies content with a code owner must be approved by that code owner"; "Require approval of the most recent reviewable push" needs "an approval from someone other than the last person to push" — [GitHub: Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)

SAST (static analysis of first-party code)
- Example: CodeQL results feed code-scanning merge protection above; Semgrep findings can be suppressed inline (see question 3) — sources as cited there.

SCA / dependency review
- The dependency review action "scans your pull requests for dependency changes, and will raise an error if any vulnerabilities or invalid licenses are being introduced"; `fail-on-severity` takes `low`, `moderate`, `high`, `critical` (default `low`); `allow-ghsas` skips listed advisories; `show-openssf-scorecard` defaults to true; it becomes a gate only via branch protection requiring the check — [actions/dependency-review-action](https://github.com/actions/dependency-review-action)
- OSV-Scanner: "find existing vulnerabilities affecting your project's dependencies", "an officially supported frontend to the OSV database" — [OSV-Scanner](https://google.github.io/osv-scanner/)
- Trivy scans targets including "Container Image", "Filesystem", "Code Repository", "Kubernetes", "SBOM" with scanners "Vulnerability (Software Composition Analysis)", "Misconfiguration (Infrastructure as Code)", "Secret", "License" — [Trivy docs](https://trivy.dev/latest/docs/)

License checks
- Dependency review supports `allow-licenses` (SPDX identifiers); `deny-licenses` is deprecated; limitation: "If we can't detect the license for a dependency we will inform you, but the action won't fail" — [actions/dependency-review-action](https://github.com/actions/dependency-review-action)

IaC scanning
- Checkov and Trivy misconfiguration scanning, see suppression mechanisms under question 3 — [Checkov suppressions](https://www.checkov.io/2.Basics/Suppressing%20and%20Skipping%20Policies.html); [Trivy docs](https://trivy.dev/latest/docs/)

SBOM, provenance and deploy-time admission
- SLSA Build L1: "Automatically generate provenance describing how the artifact was built"; "Provenance may be incomplete and/or unsigned at L1". L2: "Run builds on a hosted build platform" and "Generate and sign the provenance itself"; "Prevents tampering after the build through digital signatures". L3: "prevent runs from influencing one another" and "prevent secret material used to sign the provenance from being accessible to the user-defined build steps"; "Prevents tampering during the build—by insider threats, compromised credentials, or other tenants" — [SLSA v1.1 levels](https://slsa.dev/spec/v1.1/levels)
- Sigstore policy-controller is "an admission controller that can be used to enforce policy on a Kubernetes cluster based on verifiable supply-chain metadata from cosign"; by default it only validates namespaces labelled `policy.sigstore.dev/include: "true"`; failing images are rejected by default but policies support a `warn` mode; `no-match-policy` can be `warn`, `allow` or `deny` (default) — [Sigstore policy-controller](https://docs.sigstore.dev/policy-controller/overview/)
- NIST SSDF (SP 800-218 v1.1, February 2022) is the framework-level reference: "secure software development practices usually need to be added to each SDLC model"; SP 800-218A is listed as a related part — [NIST SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final)

Test/coverage gates
- Codecov "project" status compares overall coverage to base; "patch" status measures only lines changed, i.e. "how well the pull request is tested"; `target` and `threshold` define pass; `informational: true` makes the status "pass no matter what the coverage is"; configuration lives in `codecov.yml` in the repository — [Codecov commit status](https://docs.codecov.com/docs/commit-status)

### Inferences
- [Inference] Placement ladder from advisory to enforcing: agent-side hook or IDE lint (agent-controlled) < local pre-commit (skippable via `--no-verify`/`SKIP`) < CI check that is not required < required check from a pinned source app on a protected branch < server-side push rejection / admission controller. Only the last two tiers hold if the agent is compromised, provided the agent's identity is not on the bypass list.
- [Inference] Push protection on GitHub is a gate against accidental leaks but not against an agent holding write credentials, because bypass with a reason is available to writers unless delegated bypass is configured.
- [Inference] A coverage gate configured in a repo-tracked `codecov.yml` can be weakened in the same PR (e.g. `informational: true`), so it is only a gate if that file is protected by code owners or a path restriction.

### Gaps
- Not verified here: GitLab's push rules/secret push protection and Dependabot/Renovate docs (not fetched in this pass).
- No fetched source gave CodeQL or Semgrep false-positive/false-negative rates.
- Whether code-scanning merge protection treats a missing analysis as failing was stated only in the rulesets page ("the tool isn't configured"); behaviour for a skipped/cancelled workflow run was not documented in the fetched text.

## 2. Relevance to AI-generated code

### Takeaway
There is peer-reviewed evidence that LLMs hallucinate package names
often and repeatably, and a first-hand experiment showing a
hallucinated name being installed in the wild; older peer-reviewed work
found roughly 40% of Copilot completions in security-relevant scenarios
vulnerable. GitHub now runs CodeQL, advisory-database and secret
scanning on code from its own and third-party coding agents by default
(dated: 2025-10-28 and 2026-06-09).

### Cited Findings

Package hallucination / slopsquatting
- Spracklen et al., USENIX Security 2025: "we generate 576,000 code samples in two programming languages"; hallucination rate "at least 5.2% for commercial models" and "21.7% for open-source models"; "205,474 unique examples of hallucinated package names"; 16 LLMs tested — [arXiv 2406.10279](https://arxiv.org/abs/2406.10279)
- Repeatability: "43% of hallucinated packages were repeated in all 10 queries, while 39% did not repeat at all"; "58% of the time, a hallucinated package is repeated more than once in 10 iterations" — [arXiv 2406.10279 (HTML v3)](https://arxiv.org/html/2406.10279v3)
- Models can flag their own hallucinations: "3 of the 4 models (GPT 4 Turbo, GPT 3.5, and DeepSeek) proved to be highly adept in detecting their own hallucinations with detection accuracy above 75%" — [arXiv 2406.10279 (HTML v3)](https://arxiv.org/html/2406.10279v3)
- Mitigations tested: RAG reduced hallucinations 24% (DeepSeek) / 49% (CodeLlama); self-refinement 19% / 3%; fine-tuning 83% / 61% but lowered code quality 26% / 3%; hallucination rate rises with temperature — [arXiv 2406.10279 (HTML v3)](https://arxiv.org/html/2406.10279v3)
- [Practitioner/first-hand research] Bar Lanyado (Lasso Security, 2024-03-28) uploaded an empty package named after a hallucinated name, "huggingface-cli", which received "more than 30k authentic downloads" in three months, and found that "several large companies either use or recommend this package in their repositories" (Alibaba named); measured hallucination rates included GPT-4 24.2%, GPT-3.5 22.2%, Gemini 64.5%, Cohere 29.1% over 47,803 "how to" questions — [Lasso Security](https://www.lasso.security/blog/ai-package-hallucinations)
- SLSA explicitly does not address name confusion: it "does not directly address" malicious source code, and does not address "package name confusion attacks" — [SLSA threats overview](https://slsa.dev/spec/v1.1/threats-overview)

Insecure patterns
- Pearce et al., "Asleep at the Keyboard?": "89 different scenarios", "1,689 programs", "approximately 40% to be vulnerable", using "high-risk CWEs (e.g. those from MITRE's 'Top 25' list)" — [arXiv 2108.09293](https://arxiv.org/abs/2108.09293) (dated: Copilot of 2021; not a measurement of current models)
- GitHub itself warns that agent output "can produce incorrect or suboptimal code, including code that contains security vulnerabilities. Review and test the output before using it in production." — [GitHub: About Copilot coding agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)

Vendor validation of agent-written code (dated)
- 2025-10-28: Copilot coding agent "analyzes it for potential security vulnerabilities using CodeQL", "checks any newly-introduced dependencies against the GitHub Advisory Database", "uses secret scanning", and "If the security validation or code review tools find any problems, Copilot attempts to resolve them before finishing the pull request" — [GitHub changelog 2025-10-28](https://github.blog/changelog/2025-10-28-copilot-coding-agent-now-automatically-validates-code-security-and-quality/)
- 2026-06-09: the same analysis runs for third-party coding agents "(including Claude and OpenAI Codex)"; "Security validation doesn't require a GitHub Advanced Security license"; validations "are on by default and follow your repository's Copilot settings for which validation tools to use"; "now generally available" — [GitHub changelog 2026-06-09](https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/)
- Copilot cloud agent mitigations: "only has the ability to push to a single branch", remains "subject to any branch protections and required checks"; "Draft pull requests created by Copilot cloud agent must be reviewed and merged by a human"; it "Prevents the user who asked Copilot cloud agent to create a pull request from approving it"; "Workflows are not triggered until Copilot cloud agent's code is reviewed" — [GitHub: Risks and mitigations for Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations)

Leaked secrets
- GitGuardian (vendor, own data, 2025-03-11): "23.8 million secrets leaked on public GitHub repositories in 2024, marking a 25% year-over-year increase"; "70% of secrets leaked in 2022 remain active today" — [GitGuardian State of Secrets Sprawl 2025](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2025/) (general, not agent-specific)

### Inferences
- [Inference] Because over half of hallucinated names recur, an attacker can predict and pre-register them; a gate that rejects dependencies that are new to the repo, very new on the registry, or absent from an allowlist targets this risk directly, while vulnerability-database SCA does not (a freshly registered malicious package has no CVE until reported).
- [Inference] GitHub's in-loop validation runs inside the agent's own workflow and the agent "attempts to resolve" findings; it improves honest output but is not by itself a merge gate. The merge gate is still the ruleset (required checks, code scanning results, human review).

### Gaps
- No primary study found that measures secret leakage rates specifically in agent-authored commits (the GitGuardian Copilot figure could not be verified in the fetched text and was dropped).
- No first-hand report found of a slopsquatted package exploited maliciously (as opposed to Lasso's benign experiment).
- No fetched study measures how often current (2026) coding agents add new dependencies or how often they introduce CWE-class bugs.

## 3. Honest mistakes vs compromised agent; known limits

### Takeaway
Against honest mistakes, scanners at any placement help. Against a
compromised or prompt-injected agent, every scanner whose configuration,
ignore list, baseline or inline suppression lives in the repository can
be disabled in the same change, so the gate only holds when those files
are protected (code owners, path-restricted pushes, org-level config)
and when the check's result source is pinned.

### Cited Findings
- Inline suppressions in the scanned code: gitleaks `#gitleaks:allow`; `.gitleaksignore` suppresses findings by fingerprint; `--baseline-path` reports only new findings; TOML config supports allowlists — [gitleaks README](https://github.com/gitleaks/gitleaks)
- Semgrep `nosemgrep` / `nosemgrep: RULE_ID` comments; they only work when the org setting "Allow inline comments to disable Semgrep" is on; "Ignoring code through this method still generates a finding. The finding is automatically set to the Ignored triage state."; `.semgrepignore` excludes paths — [Semgrep: Ignore files, folders and code](https://docs.semgrep.dev/ignoring-files-folders-code)
- Checkov inline skip "checkov:skip=<check_id>:<suppression_comment>" (Kubernetes annotation `checkov.io/skip#`), and CLI `--skip-check` with wildcards (e.g. `CKV_AWS*`) — [Checkov suppressions](https://www.checkov.io/2.Basics/Suppressing%20and%20Skipping%20Policies.html)
- OSV-Scanner ignores via `[[IgnoredVulns]]` with `id`, optional `ignoreUntil` ("Optional exception expiry date") and `reason`; PackageOverrides can `ignore = true` a whole package or override its license; "place an osv-scanner.toml file in the scanned file's directory" — [OSV-Scanner configuration](https://google.github.io/osv-scanner/configuration/)
- Dependency review: `allow-ghsas` skips advisories; config may live in `./.github/dependency-review-config.yml` or a remote repository — [actions/dependency-review-action](https://github.com/actions/dependency-review-action)
- Codecov `informational: true` makes the status always pass; config in `codecov.yml` — [Codecov commit status](https://docs.codecov.com/docs/commit-status)
- Status-check spoofing by any writer unless the expected source app is set — [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- Push-protection bypass reasons available to writers — [GitHub push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)
- License detection gaps do not fail the action — [actions/dependency-review-action](https://github.com/actions/dependency-review-action)
- Admission control can be weakened by namespace opt-in labels or `warn` mode — [Sigstore policy-controller](https://docs.sigstore.dev/policy-controller/overview/)
- SLSA scope: "SLSA does not directly address this threat [malicious source code]"; "For closed source software SLSA does not provide any solutions for malicious producers" — [SLSA threats overview](https://slsa.dev/spec/v1.1/threats-overview)
- SLSA notes that for the authoring stage "Two-person review could have caught the unauthorized change" — [SLSA threats overview](https://slsa.dev/spec/v1.1/threats-overview)

### Inferences
- [Inference] Suppression channels per tool: inline comment, repo ignore file, baseline file, config file, workflow file, CLI flag in CI. A harness-forge recommendation for an outside gate should list which of these exist for the chosen tool and require each to be either org-managed or covered by CODEOWNERS / a push-ruleset path restriction (e.g. `.github/workflows/**`, `.gitleaks*`, `.semgrepignore`, `osv-scanner.toml`, `codecov.yml`).
- [Inference] Semgrep's "Ignored" triage state and OSV's `reason`/`ignoreUntil` make suppressions auditable after the fact; they are detection, not prevention.
- [Inference] Provenance (SLSA/in-toto/cosign) proves where and how an artifact was built, not that its code is safe; it protects against a compromised agent tampering with artifacts after review, not against a reviewed-but-malicious change.
- [Inference] False positives push agents (and humans) to add suppressions; a gate that allows in-repo suppressions without review converts noise into a silent bypass path.

### Gaps
- No fetched source quantified suppression abuse by agents or humans.
- CodeQL's own suppression mechanisms (alert dismissal permissions) were not fetched in this pass.

## 4. Complement vs replace a harness mechanism; cost and friction

### Takeaway
The same scanner usually belongs in both places: as a harness hook or
instruction for fast, cheap feedback the agent can act on, and as an
outside required check for enforcement. The outside gate replaces
nothing in the harness for feedback speed, and the harness hook replaces
nothing outside for assurance. Main costs are licensing for some hosted
features, CI time, and false-positive triage.

### Cited Findings
- GitHub's own agent pattern pairs both: in-loop validation where the agent "attempts to resolve" findings, plus the agent remaining "subject to any branch protections and required checks" and human merge — [GitHub changelog 2025-10-28](https://github.blog/changelog/2025-10-28-copilot-coding-agent-now-automatically-validates-code-security-and-quality/); [GitHub: Risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations)
- Paper's mitigations for hallucination are model-side (RAG, self-refinement, fine-tuning) with partial reductions (e.g. self-refinement 3% for CodeLlama) — [arXiv 2406.10279 (HTML v3)](https://arxiv.org/html/2406.10279v3)
- Cost/licensing (dated): repository-level push protection "Requires GitHub Secret Protection"; agent security validation "doesn't require a GitHub Advanced Security license" — [GitHub push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection); [GitHub changelog 2026-06-09](https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/)
- Friction-reducing options exist: baselines (gitleaks `--baseline-path`), expiring exceptions (OSV `ignoreUntil`), patch-only coverage (Codecov patch status), severity thresholds (dependency review `fail-on-severity`, code-scanning thresholds) — sources as cited above.

### Inferences
- [Inference] Decision rule for harness-forge: rule must hold even if the agent is compromised → outside gate (required check with pinned source, push protection/pre-receive, admission control), with its config files protected; rule is about quality/speed of honest work → harness hook or instruction running the same tool; high-impact rules → both.
- [Inference] Model-side mitigations (prompting, RAG, self-check) only lower rates; slopsquatting needs a registry-side or CI-side dependency gate (allowlist, new-dependency review, age/reputation check such as OpenSSF Scorecard in dependency review).
- [Inference] Baselines and patch-only thresholds let teams adopt gates on legacy repos without blocking every PR, at the cost of ignoring pre-existing issues.

### Gaps
- No fetched source gives CI time or cost figures for CodeQL/Semgrep/Trivy runs.
