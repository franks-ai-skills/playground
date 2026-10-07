# Merge and CI gates outside the agent harness

Researched 2026-10-07. All quotes were fetched from the cited page on that
date. Platform features are examples of general concepts; tiers and defaults
are date-sensitive. Labels: [Vendor] platform documentation, [Spec] standard,
[Advisory/Research] first-hand security research, [Inference] my reasoning
from the cited facts. Domains not yet in `docs/sources.md` and needing
assessment: `docs.gitlab.com`, `learn.microsoft.com`,
`support.atlassian.com`, `gerrit-review.googlesource.com`, `slsa.dev`,
`git-scm.com`, GitHub `ossf/scorecard` (all are primary sources for their own
product, standard or tool).

## 1. Which gate concepts exist (platform-neutral, with examples)

### Takeaway
Every major forge offers the same core set: a protected target ref that only
accepts changes through a reviewed change request; required approvals (often
from path owners); author/pusher-cannot-approve rules; required checks that
must report success (optionally from a named source); serialized merging
against the latest base; ref-level push rules (force-push, deletion, signing,
linear history, file paths); server-side pre-receive hooks; and deployment
environments with approvals and timers. Names differ; the concepts map
almost one-to-one.

### Cited Findings

**Protected branch / ruleset (change only through a reviewed request)**
- [Vendor] GitHub rulesets: "You can require that all changes to the target branch be associated with a pull request." — [GitHub: available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Vendor] GitHub branch restriction: "When you enable branch restrictions, only users, teams, or apps that have been given permission can push to the protected branch." — [GitHub: about protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Vendor] GitHub lock branch: "Locking a branch will make the branch read-only and ensures that no commits can be made to the branch." — [GitHub: about protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Vendor] GitLab: "**Allowed to push and merge** grants both push and merge capabilities. Users with this permission can merge through merge requests even without **Allowed to merge** permission." — [GitLab: protected branches](https://docs.gitlab.com/user/project/repository/branches/protected/)
- [Spec] SLSA Source L3: "The SCS is configured to enforce the Organization's technical controls for specific Named References within the Source Repository." — [SLSA v1.2 source requirements](https://slsa.dev/spec/v1.2/source-requirements) (page status: "Approved")

**Required reviews, stale-approval dismissal, code owners**
- [Vendor] GitHub: "You can choose to dismiss stale pull request approvals when commits are pushed that affect the diff." — [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Vendor] GitHub: "any pull request that modifies content with a code owner must be approved by that code owner." — [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Vendor] GitLab protected branch with code owner approval: "When enabled, all merge requests for these branches require approval by a Code Owner per matched rule before they can be merged." — [GitLab: protected branches](https://docs.gitlab.com/user/project/repository/branches/protected/)
- [Vendor] GitLab: "By default, an approval on a merge request is removed when you add more changes after the approval." — [GitLab: MR approval settings](https://docs.gitlab.com/user/project/merge_requests/approvals/settings/)
- [Vendor] Bitbucket Cloud: "Reset approvals when the source branch is modified - If there are any changes to the source branch of the pull request, the pull request updates with no approvals, and the reviewers have to review and approve the pull request again." — [Bitbucket: merge checks](https://support.atlassian.com/bitbucket-cloud/docs/suggest-or-require-checks-before-a-merge/)
- [Vendor] Azure DevOps: "Select **Reset all approval votes (does not reset votes to reject or wait)** to remove all approval votes, but keep votes to reject or wait, whenever the source branch changes." Path-scoped "Automatically included reviewers": "Specify the files and folders that require the automatically included reviewers." — [Azure Repos: branch policies](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies) (page dated 2026-07-15)
- [Vendor] Gerrit expresses all of this as submit requirements: "Submit requirements are rules that define when a change can be submitted"; typical approval expression "label:Code-Review=MAX AND -label:Code-Review=MIN". — [Gerrit: submit requirements](https://gerrit-review.googlesource.com/Documentation/config-submit-requirements.html)

**Separation of author/pusher and approver**
- [Vendor] GitHub: "You can require an approval from someone other than the last person to push to a branch before a pull request can be merged." — [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Vendor] GitLab: "By default, the creator of a merge request (author) cannot approve it." but "By default, users who commit to a merge request (the committers) can still approve it." (separate setting to prevent committer approval; Premium/Ultimate). — [GitLab: MR approval settings](https://docs.gitlab.com/user/project/merge_requests/approvals/settings/)
- [Vendor] Azure DevOps: if "Allow requestors to approve their own changes" is off, "the creator can still vote **Approve** on the PR, but their vote doesn't count toward the minimum number of reviewers." And "Prohibit the most recent pusher from approving their own changes" exists "to enforce segregation of duties. By default, anyone with push permission on the source branch can both add commits and vote on PR approval." — [Azure Repos: branch policies](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies)
- [Vendor] Gerrit: "label:Code-Review=MAX,user=non_uploader"; "user=non_contributor" means "a user that's not the uploader, author or committer of the latest patchset". — [Gerrit: submit requirements](https://gerrit-review.googlesource.com/Documentation/config-submit-requirements.html)
- [Spec] SLSA Source L4: "Changes in protected branches MUST be agreed to by two or more trusted persons prior to submission." Acceptable: "Uploader and reviewer are two different trusted persons" or "Two different reviewers are trusted persons." — [SLSA v1.2 source requirements](https://slsa.dev/spec/v1.2/source-requirements)

**Required status checks bound to a source**
- [Vendor] GitHub: "When you add a required status check rule, you can select an app as the expected source of status updates." — [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Vendor] Azure DevOps status-check policy: "Optionally configure **Authorized identity**, **Reset conditions**, **Policy applicability**, and **Path filter**." Build validation: "the policy evaluates the build results to determine whether the PR can be completed." — [Azure Repos: branch policies](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies)
- [Vendor] Bitbucket: "Minimum number of successful builds for the last commit with no failed builds and no in progress builds". — [Bitbucket: merge checks](https://support.atlassian.com/bitbucket-cloud/docs/suggest-or-require-checks-before-a-merge/)
- [Vendor] Gerrit: "label:Verified=MAX AND -label:Verified=MIN". — [Gerrit: submit requirements](https://gerrit-review.googlesource.com/Documentation/config-submit-requirements.html)
- [Vendor] GitHub can also require code-scanning results and successful deployments: "You can require that changes are successfully deployed to specific environments before a branch can be merged." — [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Vendor] GitHub org-level required workflows (ruleset rule, GA 2023-10-11): an admin can "choose a workflow by specific branch, tag, current commit or specific SHA". — [GitHub blog, Tony Camp, 2023-10-11](https://github.blog/2023-10-11-enforcing-code-reliability-by-requiring-workflows-with-github-repository-rules)

**Merge queue**
- [Vendor] GitHub: "the changes in the pull request are grouped into a `merge_group` with the latest version of the `base_branch`"; it ensures "the branch is never broken by incompatible changes." — [GitHub: managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)

**Ref integrity: signing, linear history, force-push, deletion, tags**
- [Vendor] GitHub: "contributors and bots can only push commits that have been signed and verified." "Enforcing a linear commit history prevents collaborators from pushing merge commits to the targeted branches." "You can prevent users from force pushing to the targeted branches or tags." "Only users with bypass permissions can delete branches or tags whose name matches the pattern you specify." — [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Spec] SLSA Source L2: "Branch history is continuous, immutable, and retained". — [SLSA v1.2](https://slsa.dev/spec/v1.2/source-requirements)

**Server-side push rules (pre-receive)**
- [Vendor] Git: pre-receive "takes a list of references that are being pushed from stdin; if it exits non-zero, none of them are accepted." — [Pro Git: Git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [Vendor] GitLab: "Push rules are `pre-receive` Git hooks you can enable in a user-friendly interface"; examples "Reject unsigned commits", "Prohibited filenames", "Prevent pushing secret files"; "For custom push rules use server hooks" (self-managed). Tier: Premium, Ultimate. — [GitLab: push rules](https://docs.gitlab.com/user/project/repository/push_rules/)
- [Vendor] GitHub push rulesets: "Prevent commits that include changes in specified file paths from being pushed to the repository." "For push rulesets, bypass permissions apply to a repository and the repository's entire fork network." — [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)

**Deployment environments: approvals, self-review, timers, secrets**
- [Vendor] GitHub: "You can list up to six users or teams as reviewers." "Prevent self-review": "users who initiate a deployment cannot approve the deployment job, even if they are a required reviewer." Wait timer: "an integer between 1 and 43,200 (30 days)." "If the environment requires approval, a job cannot access environment secrets until one of the required reviewers approves it." Branch/tag limits and "custom protection rules to gate deployments with third-party services." — [GitHub: deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
- [Vendor] GitLab: "By default, the user who triggers a deployment pipeline can't also approve the deployment job" (opt-out "Allow pipeline triggerer to approve deployment"); "All jobs deploying to the environment are blocked and wait for approvals before running." Tier: Premium, Ultimate. — [GitLab: deployment approvals](https://docs.gitlab.com/ci/environments/deployment_approvals/)

### Inferences
- [Inference] A tool can model these as one platform-neutral list: (1) change-only-via-request, (2) N independent approvals, (3) path-owner approval, (4) author/last-pusher exclusion, (5) re-approval on new push, (6) required checks with pinned source, (7) serialized merge against latest base, (8) ref integrity (signing, linear, no force/delete, tag protection), (9) pre-receive content rules, (10) gated deployment environments. Each forge cited above implements most of them under different names.

### Gaps
- Bitbucket Data Center, GitHub Enterprise Server and Gerrit plugin-specific variants were not fetched; feature parity per tier/version is not verified beyond what is quoted.

## 2. What each gate stops: honest mistakes vs. compromised/prompt-injected agent, and what it does not stop

### Takeaway
Against honest mistakes, required checks and review catch broken or unreviewed code and the merge queue catches semantic conflicts. Against a compromised agent, the decisive properties are identity separation (the agent's identity, and the human who launched it, cannot satisfy approval) and that gate configuration and check definitions lie outside what the agent's identity can change. Gates fail through bypass lists and admins, self-approval defaults, approvals that survive later pushes, checks whose definition the PR itself edits, and privileged CI triggers that run untrusted code.

### Cited Findings
- [Vendor] Agent-specific example (GitHub Copilot cloud agent): it "Prevents the user who asked Copilot cloud agent to create a pull request from approving it"; "the agent can only push to that branch" (a new `copilot/` branch); "The agent is also subject to any branch protections and required checks for the working repository"; "By default, workflows are not triggered until Copilot cloud agent's code is reviewed and a user with write access to the repository clicks the **Approve and run workflows** button." — [GitHub: Copilot cloud agent risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/coding-agent/risks-and-mitigations)
- [Vendor] Workflow-token approval default: "By default, when you create a new repository in your personal account, workflows are not allowed to create or approve pull requests." — [GitHub: Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
- [Vendor] Admin bypass by default (classic branch protection): "By default, the restrictions of a branch protection rule do not apply to people with admin permissions to the repository or custom roles with the 'bypass branch protections' permission." — [GitHub: about protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Vendor] Bypass lists: "When you create a ruleset, you can allow certain users to bypass the rules in the ruleset." — [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Vendor] Environment admin bypass: "By default, administrators can bypass the protection rules and force deployments to specific environments." — [GitHub: deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
- [Vendor] Azure DevOps bypass permissions: "Bypass policies when completing pull requests" ("can complete pull requests even if the pull requests don't satisfy policies") and "Bypass policies when pushing" ("can push changes directly to protected branches without meeting policy requirements"); "Use caution when granting the ability to bypass policies". — [Azure Repos: branch policies](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies)
- [Vendor] GitLab push-access bypass: "Users and groups who are allowed to push to protected branches do not need a merge request to merge their feature branches. Thus, they can skip merge request approval rules, Code Owners included." — [GitLab: protected branches](https://docs.gitlab.com/user/project/repository/branches/protected/)
- [Vendor] GitLab per-MR override default: "By default, users can override the approval rules you create for a project on a per-merge-request basis." — [GitLab: MR approval settings](https://docs.gitlab.com/user/project/merge_requests/approvals/settings/)
- [Vendor] Gerrit override: when overrideIf matches, "the submit requirement state becomes `OVERRIDDEN` and the submit requirement is no longer blocking the change submission." — [Gerrit: submit requirements](https://gerrit-review.googlesource.com/Documentation/config-submit-requirements.html)
- [Vendor] Workflow definition comes from the PR for `pull_request`: GITHUB_SHA is the "Last merge commit on the `GITHUB_REF` branch"; for `pull_request_target` it is the "Last commit on default branch", and it "runs in the context of the default branch of the base repository". Warning: "Running untrusted code on the `pull_request_target` trigger may lead to security vulnerabilities. These vulnerabilities include cache poisoning and granting unintended access to write privileges or secrets." Forks: "secrets are not passed to the runner when a workflow is triggered from a forked repository. The `GITHUB_TOKEN` has read-only permissions in pull requests from forked repositories." — [GitHub: events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- [Advisory/Research] GitHub Security Lab (Jaroslav Lobačevski, 2021-08-03): "Combining `pull_request_target` workflow trigger with an explicit checkout of an untrusted PR is a dangerous practice that may lead to repository compromise." "Workflows triggered via `pull_request_target` have write permission to the target repository. They also have access to target repository secrets." — [Preventing pwn requests](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/)
- [Vendor] Self-hosted runners: "potentially malicious user-controlled workflow code will execute automatically if the user is allowed to bypass approval in the set approval policy." — [GitHub: Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
- [Vendor] CODEOWNERS is read from the base branch: "the CODEOWNERS file must be on the base branch of the pull request." Recommended: define it in `.github` "and define the repository owner as the owner of either the CODEOWNERS file". "If any line in your CODEOWNERS file contains invalid syntax, that line will be skipped." — [GitHub: about code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Vendor] OpenSSF Scorecard rates branch protection risk "High (vulnerable to intentional malicious code injection)", its top tier needs "Dismiss stale reviews and approvals when new commits are pushed" and "Include administrator for review"; Dangerous-Workflow risk is "Critical (vulnerable to repository compromise)". — [OpenSSF Scorecard checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md)

### Inferences
- [Inference] Per gate, against (a) honest mistakes / (b) compromised agent:
  - Required PR + review: (a) catches errors a reviewer notices; (b) blocks direct pushes and requires a second identity. Does not stop: a rubber-stamp reviewer, the launching human approving when the agent acts under that human's identity (unless the platform excludes the requester, as Copilot does), admins/bypass actors, agent tokens holding bypass or admin rights.
  - Re-approval on new push / last-pusher exclusion: (b) prevents "get approved, then push a malicious commit". Without it, approval of a benign diff carries over.
  - Code owners on agent config (`AGENTS.md`, `CLAUDE.md`, `.claude/`, `.codex/`, `.opencode/`, `.agents/skills/`, hooks, MCP config, CI workflow files, and the CODEOWNERS file itself): (b) stops an agent from silently loosening its own harness or CI via PR. Because CODEOWNERS is read from the base branch, a PR cannot exempt itself, but a bad CODEOWNERS line is skipped silently.
  - Required checks: (a) deterministic catch of failing tests/lint; (b) only meaningful if the agent cannot (i) edit the check's definition in the same PR and have it run from the PR head, (ii) post a fake success status (mitigated by pinning the expected source app/identity), or (iii) obtain bypass. A `pull_request`-triggered workflow runs the PR's version of the workflow file, so for a same-repo agent PR the check is author-controlled; org-level required workflows pinned to a SHA in another repository, plus code owner review on workflow files, close this.
  - Merge queue: (a) catches semantic merge conflicts; (b) little security value on its own.
  - Signed commits / linear history / no force-push / tag protection: (b) preserve attributable, immutable history and stop rewriting releases; signing proves which key signed, not that the content is good. An agent holding a signing key signs whatever it writes.
  - Push rules / pre-receive (path, extension, secret, size): (a) and (b) for content rules that must hold on every push regardless of the PR flow, including direct pushes to agent branches.
  - Environment approvals + self-review prevention + secrets withheld until approval: (b) keeps deployment credentials away from agent-triggered runs until a different human approves.
  - `pull_request_target`/privileged triggers that check out agent-written code turn a gate into an attack path, as do self-hosted runners with auto-run.

### Gaps
- No first-hand published incident was verified in this pass in which a coding agent itself bypassed or abused a merge gate; the risks above are inferred from platform semantics and the Security Lab write-up.
- Not verified whether GitHub's "Prevent self-review" or GitLab's author-approval rule treats a bot/app identity acting on behalf of a user as that user, other than the Copilot statement quoted.

## 3. Prerequisites for a gate to be real

### Takeaway
A CI job is only a gate if the target ref requires it, its source is pinned, nobody relevant can bypass, and its definition is outside the change's control. Several features are paid-tier or off by default.

### Cited Findings
- [Vendor] Checks must be required and source-bound: "you can select an app as the expected source of status updates." — [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Vendor] Azure DevOps prerequisite: "Before you configure **Build validation**, have a build pipeline ready. Before you configure **Status checks**, make sure the external service or built-in integration can already post pull request status." — [Azure Repos: branch policies](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies)
- [Vendor] Merge queue requires CI changes: "You must update your CI configuration to trigger and report on merge group events when requiring a merge queue." — [GitHub: managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
- [Vendor] Code owners need write access and branch-protection enforcement: "The people you choose as code owners must have write permissions for the repository." "Repository owners can update branch protection rules to ensure that changed code is reviewed by the owners of the changed files." — [GitHub: about code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Vendor] Bitbucket Cloud merge checks only warn on the free/standard plan: "To prevent users from merging, upgrade to Premium and select **Prevent a merge with unresolved merge checks**." — [Bitbucket: merge checks](https://support.atlassian.com/bitbucket-cloud/docs/suggest-or-require-checks-before-a-merge/)
- [Vendor] GitLab approval settings, push rules and deployment approvals are listed as "Tier: Premium, Ultimate". — [GitLab MR approval settings](https://docs.gitlab.com/user/project/merge_requests/approvals/settings/); [GitLab push rules](https://docs.gitlab.com/user/project/repository/push_rules/); [GitLab deployment approvals](https://docs.gitlab.com/ci/environments/deployment_approvals/)
- [Vendor] Client-side hooks are not policy: "client-side hooks are **not** copied when you clone a repository. If your intent with these scripts is to enforce a policy, you'll probably want to do that on the server side". — [Pro Git: Git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [Vendor] Auditing gates needs privilege: Scorecard notes "The following settings require an admin token: `DismissStaleReviews`, `EnforceAdmins`, `RequireLastPushApproval`, `RequiresStatusChecks` and `UpToDateBeforeMerge`." — [OpenSSF Scorecard checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md)
- [Vendor] An incompatible ruleset can block an agent entirely: "If a ruleset or branch protection rule is incompatible with Copilot cloud agent, access to the agent is blocked." — [GitHub: about Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)

### Inferences
- [Inference] Prerequisite checklist for harness-forge to verify before calling something an "outside gate": (1) rule targets the actual default/release refs and tags; (2) the agent's identity (bot, app, token, or the human whose token it uses) is not on any bypass list and is not admin; (3) approval must come from an identity other than the author, last pusher and launching user; (4) approvals reset on new pushes; (5) required checks are pinned to a source and their definitions are protected by code owners or supplied from outside the repo at a pinned ref; (6) the feature is enforced on the user's plan/tier (not just advisory); (7) agent config and workflow files have code owners, and CODEOWNERS owns itself.

### Gaps
- Exact plan/tier availability of GitHub rulesets features for private repositories on each GitHub plan was not fetched.

## 4. Complement vs. replace harness mechanisms

### Takeaway
Harness mechanisms (hooks, permissions) give fast, in-session feedback and block actions before they happen; outside gates enforce at the shared boundary independently of the agent's configuration. For rules about what reaches a protected branch or deployment, the outside gate is the enforcement and a harness hook is an optional speed-up; for rules about actions during a session (local commands, file reads, network egress), an outside gate cannot help.

### Cited Findings
- [Vendor] Policy belongs server-side, not in client hooks ("client-side hooks are not copied when you clone a repository"). — [Pro Git](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [Vendor] Agent platforms layer both: Copilot cloud agent is limited to a `copilot/` branch and "is also subject to any branch protections and required checks for the working repository." — [GitHub: Copilot risks and mitigations](https://docs.github.com/en/copilot/concepts/agents/coding-agent/risks-and-mitigations)
- Repository knowledge base already routes merge gates to CI: overview table says "Merge gate → CI" for configuration, permissions and hooks (`docs/overview.md`, "At a glance"), and the security guide says to "Place enforced policy outside agent-writable state" (`docs/guide/security.md`).

### Inferences
- [Inference] Recommend "outside gate only" when the rule concerns the state of a shared ref or a deployment (e.g., "tests pass before merge", "two reviewers", "no secrets in main", "only signed releases"). Building a harness hook for it is optional duplication.
- [Inference] Recommend "both" when early feedback saves agent iterations (hook runs tests/lint on stop or before commit; CI enforces the same check at merge), or when the rule protects agent config itself (permission deny on editing `.claude/` etc. plus code owners on those paths).
- [Inference] Recommend "harness only" for in-session actions with no artifact reaching the forge: reading secrets, network egress, destructive local commands. A merge gate sees only the pushed result, not exfiltration during the session.
- [Inference] Recommend "deployment environment gate" for anything that touches production credentials, because it withholds secrets until a different human approves, independent of what the agent did in CI.

### Gaps
- No vendor or practitioner source was found that explicitly prescribes the hook-plus-CI split for coding agents; the split is inferred.

## 5. Cost, friction and failure modes

### Takeaway
Costs are human review latency, CI time, plan tier, and setup complexity; the main failure modes are silent: bypass actors, defaults that allow self- or committer-approval, approvals that persist after new pushes, skipped CODEOWNERS lines, checks that never report (merge queue misconfigured), and checks the PR can rewrite.

### Cited Findings
- [Vendor] Wait timer up to "43,200 (30 days)"; up to "six users or teams as reviewers". — [GitHub: deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
- [Vendor] Silent CODEOWNERS failure: invalid line "will be skipped". — [GitHub: about code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Vendor] Permissive defaults: GitLab committers "can still approve" by default and approval rules can be overridden per MR by default. — [GitLab: MR approval settings](https://docs.gitlab.com/user/project/merge_requests/approvals/settings/)
- [Vendor] Azure DevOps Build validation "Set a build expiration to make sure updates to your protected branch don't break changes for open PRs." — [Azure Repos: branch policies](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies)
- [Vendor] Merge queue needs `merge_group` CI triggers (otherwise required checks are missing). — [GitHub: managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
- [Vendor] Gerrit overrideIf and GitHub/Azure bypass lists provide emergency paths that are also the main bypass surface. — [Gerrit](https://gerrit-review.googlesource.com/Documentation/config-submit-requirements.html); [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets); [Azure Repos](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies)
- [Spec] SLSA asks for a two-person rule even for history rewriting: SCSs "SHOULD have technical mechanisms in place which require an Administrator plus at least one additional 'trusted person' to trigger any expunging." — [SLSA v1.2](https://slsa.dev/spec/v1.2/source-requirements)

### Inferences
- [Inference] Review becomes the bottleneck when agents open many PRs; required human approval scales with PR volume, so teams may be tempted to add the agent's bot to bypass lists or enable "Actions can approve PRs", which removes the gate against a compromised agent.
- [Inference] Single-maintainer repositories cannot satisfy "someone other than the last pusher" without a second human; for them, required checks plus protected workflow definitions plus environment approvals are the realistic outside gates, and the residual risk should be stated.
- [Inference] Gate configuration drifts silently; harness-forge should recommend periodic verification (e.g., OpenSSF Scorecard Branch-Protection, run with an admin-scoped token, since several settings are invisible without one).

### Gaps
- No measured data (latency, cost) on review/CI friction for agent-generated PRs was found from a primary or first-hand source in this pass.
