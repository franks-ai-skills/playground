# Bug intake

The recorded workflow targets this repository on GitHub Team (private), using Claude Code and Codex. Developers start interactive sessions and answer tool-permission prompts. B, C and D have been built from the confirmed requirements. Verification results and their limits are recorded in `.harness/reports/bug-report-lifecycle.md`.

## Workflow decisions

| Part | Result | Responsibility |
| --- | --- | --- |
| A1 | Reuse `bug-report-format` unchanged | Format text under Title, Environment, Steps, Expected, Observed. A developer applies the text to GitHub. The confirmed home is `.agents/skills/bug-report-format`. |
| A2 | `nothing-fits`; goal unmet | Always-required labeling needs judgment across both harnesses. No supported standalone mechanism meets all confirmed requirements; combinations were not assessed. No labeling mechanism is being built. |
| B | User-invoked `reproduction-checklist` skill | Prepare and post a checklist for an approved issue, with precise actual/expected results and redacted sensitive evidence. |
| C | User-invoked `check-fix-checklist` skill with required outside gate | Use B's checklist to assess the latest PR commit. The session report is advisory. A protected outside required check enforces the no-merge guarantee and must survive PR tampering. |
| D | New local `diagnose-ci` skill built | Diagnose failing CI checks for the intended PR's latest commit and propose a fix. A developer applies and pushes it. The previous `gh-fix-ci` candidate is unmaintained: its upstream repository declares itself deprecated. It is no longer selected for reuse or installation. |
| E | `outside-instead` | An active session may notice a release, but closing shipped issues is left entirely to an outside process. Closing syncs to the customer status page and notifies reporting customers. No agent-closing mechanism is being built. |

A1 reuse is pinned to commit `62eb5241487ef5d7fdb9efb8eb1d93b559a04437` at [the user-supplied source](https://github.com/example-team/bug-intake/tree/62eb5241487ef5d7fdb9efb8eb1d93b559a04437/.agents/skills/bug-report-format). The complete local package was reviewed; it contains only the unchanged seven-line SKILL.md and no scripts. Reviewed local SHA-256: `7d42ea98e84f3148e438267365a036dfa62353a463cd48ddd0f2dd1957ce31cd`. The review is recorded in `.harness/intake/a1-reuse-review.md`; the private upstream contents were not independently fetched.

## Outside handoff

C's outside gate must require successful checklist evidence for the current commit on the actual merge target. Its check and policy definitions must come from protected provenance that a pull request cannot replace. The agent's identity and every credential it can reach must be unable to bypass or rewrite the gate. Its enforcement and configuration require periodic verification by the platform owner.

E's outside closer must establish that the release contains the fix before it closes the issue and triggers customer-facing effects. An outside control must protect that decision and the real issue/customer-status resources from agent-side bypass, including any human token used by the agent. Release observation alone does not authorize this agent to perform closure.

The outside controls below are recommendations with prerequisites, not evidence of platform configuration. Broader code-owner protection of agent configuration is a precaution; required protection of the C/E gate definitions is recorded separately.

## Build and verification plan

B, C and D are built packages, with canonical files in `.agents/skills/` and relative symlinks in `.claude/skills/`. A1 is preserved unchanged. D was built locally after the upstream reuse candidate was confirmed unmaintained; it diagnoses and proposes without applying changes. Verification runs static checks, an independent review, and activation/near-miss cases in throwaway workspaces. Offline activation cases do not exercise live GitHub posting, application reproduction, merge blocking or customer notifications. Verification reports every unavailable artifact and outside dependency separately. The contract-bound report is written to `.harness/reports/bug-report-lifecycle.md`.

Invoke B explicitly with `$reproduction-checklist` in Codex or `/reproduction-checklist` in Claude Code, supplying the approved issue. Invoke C explicitly with `$check-fix-checklist` or `/check-fix-checklist`, supplying the fix pull request and B's checklist. These two skills are configured to prevent implicit model invocation.

D can activate for a failing-CI diagnosis request or be invoked explicitly with `$diagnose-ci` in Codex or `/diagnose-ci` in Claude Code. Supply the intended repository and PR, or enough session context to resolve them. The developer applies and pushes the proposed fix.

## Outside controls

- `codeowners-agent-config` (part A1): recommended, not verified. Precaution; availability available. It works as a gate only when:
  - Workflow, scanner and policy files that define a gate are under code owners or come from outside the repository at a pinned ref, and CODEOWNERS owns itself (`outside.ci.workflow-protected`)
  - A CODEOWNERS entry names an owner for every file that configures the agent, including `.agents/`, `.claude/`, `CLAUDE.md`, `.mcp.json`, `.codex/`, `AGENTS.md`, `AGENTS.override.md`, `.devcontainer/`, the CI workflow files and the CODEOWNERS file itself, and the branch rule requires code-owner review (`outside.codeowners.agent-config`)
  - It targets the real refs and resources it protects, such as the default and release branches and tags or the production accounts (`outside.gate.real-refs`)
  - Its configuration is checked periodically, because gate configuration drifts silently (`outside.gate.periodic-verification`)
- `codeowners-agent-config` (part A2): recommended, not verified. Precaution; availability available. It works as a gate only when:
  - Workflow, scanner and policy files that define a gate are under code owners or come from outside the repository at a pinned ref, and CODEOWNERS owns itself (`outside.ci.workflow-protected`)
  - A CODEOWNERS entry names an owner for every file that configures the agent, including `.agents/`, `.claude/`, `CLAUDE.md`, `.mcp.json`, `.codex/`, `AGENTS.md`, `AGENTS.override.md`, `.devcontainer/`, the CI workflow files and the CODEOWNERS file itself, and the branch rule requires code-owner review (`outside.codeowners.agent-config`)
  - It targets the real refs and resources it protects, such as the default and release branches and tags or the production accounts (`outside.gate.real-refs`)
  - Its configuration is checked periodically, because gate configuration drifts silently (`outside.gate.periodic-verification`)
- `codeowners-agent-config` (part B): recommended, not verified. Precaution; availability available. It works as a gate only when:
  - Workflow, scanner and policy files that define a gate are under code owners or come from outside the repository at a pinned ref, and CODEOWNERS owns itself (`outside.ci.workflow-protected`)
  - A CODEOWNERS entry names an owner for every file that configures the agent, including `.agents/`, `.claude/`, `CLAUDE.md`, `.mcp.json`, `.codex/`, `AGENTS.md`, `AGENTS.override.md`, `.devcontainer/`, the CI workflow files and the CODEOWNERS file itself, and the branch rule requires code-owner review (`outside.codeowners.agent-config`)
  - It targets the real refs and resources it protects, such as the default and release branches and tags or the production accounts (`outside.gate.real-refs`)
  - Its configuration is checked periodically, because gate configuration drifts silently (`outside.gate.periodic-verification`)
- `codeowners-agent-config` (part C): recommended, not verified. Precaution; availability available. It works as a gate only when:
  - Workflow, scanner and policy files that define a gate are under code owners or come from outside the repository at a pinned ref, and CODEOWNERS owns itself (`outside.ci.workflow-protected`)
  - A CODEOWNERS entry names an owner for every file that configures the agent, including `.agents/`, `.claude/`, `CLAUDE.md`, `.mcp.json`, `.codex/`, `AGENTS.md`, `AGENTS.override.md`, `.devcontainer/`, the CI workflow files and the CODEOWNERS file itself, and the branch rule requires code-owner review (`outside.codeowners.agent-config`)
  - It targets the real refs and resources it protects, such as the default and release branches and tags or the production accounts (`outside.gate.real-refs`)
  - Its configuration is checked periodically, because gate configuration drifts silently (`outside.gate.periodic-verification`)
- `compromise-resistant-gate` (part C): recommended, not verified. Required for the goal; availability available. It works as a gate only when:
  - Workflow, scanner and policy files that define a gate are under code owners or come from outside the repository at a pinned ref, and CODEOWNERS owns itself (`outside.ci.workflow-protected`)
  - No broader credential or channel the agent can reach, such as a personal token or a metadata endpoint, bypasses the control (`outside.gate.no-broader-bypass`)
  - Its configuration is checked periodically, because gate configuration drifts silently (`outside.gate.periodic-verification`)
  - The control is enforced on the user's plan and repository visibility, or the recommendation says it is not (`outside.gate.plan-enforced`)
  - It targets the real refs and resources it protects, such as the default and release branches and tags or the production accounts (`outside.gate.real-refs`)
  - The agent's identity, including the bot, app, token and the human whose token it uses, is on no bypass or override list of the control (`outside.merge.no-agent-bypass`)
- `codeowners-agent-config` (part D): recommended, not verified. Precaution; availability available. It works as a gate only when:
  - Workflow, scanner and policy files that define a gate are under code owners or come from outside the repository at a pinned ref, and CODEOWNERS owns itself (`outside.ci.workflow-protected`)
  - A CODEOWNERS entry names an owner for every file that configures the agent, including `.agents/`, `.claude/`, `CLAUDE.md`, `.mcp.json`, `.codex/`, `AGENTS.md`, `AGENTS.override.md`, `.devcontainer/`, the CI workflow files and the CODEOWNERS file itself, and the branch rule requires code-owner review (`outside.codeowners.agent-config`)
  - It targets the real refs and resources it protects, such as the default and release branches and tags or the production accounts (`outside.gate.real-refs`)
  - Its configuration is checked periodically, because gate configuration drifts silently (`outside.gate.periodic-verification`)
- `codeowners-agent-config` (part E): recommended, not verified. Precaution; availability available. It works as a gate only when:
  - Workflow, scanner and policy files that define a gate are under code owners or come from outside the repository at a pinned ref, and CODEOWNERS owns itself (`outside.ci.workflow-protected`)
  - A CODEOWNERS entry names an owner for every file that configures the agent, including `.agents/`, `.claude/`, `CLAUDE.md`, `.mcp.json`, `.codex/`, `AGENTS.md`, `AGENTS.override.md`, `.devcontainer/`, the CI workflow files and the CODEOWNERS file itself, and the branch rule requires code-owner review (`outside.codeowners.agent-config`)
  - It targets the real refs and resources it protects, such as the default and release branches and tags or the production accounts (`outside.gate.real-refs`)
  - Its configuration is checked periodically, because gate configuration drifts silently (`outside.gate.periodic-verification`)
- `compromise-resistant-gate` (part E): recommended, not verified. Required for the goal; availability available. It works as a gate only when:
  - Workflow, scanner and policy files that define a gate are under code owners or come from outside the repository at a pinned ref, and CODEOWNERS owns itself (`outside.ci.workflow-protected`)
  - No broader credential or channel the agent can reach, such as a personal token or a metadata endpoint, bypasses the control (`outside.gate.no-broader-bypass`)
  - Its configuration is checked periodically, because gate configuration drifts silently (`outside.gate.periodic-verification`)
  - The control is enforced on the user's plan and repository visibility, or the recommendation says it is not (`outside.gate.plan-enforced`)
  - It targets the real refs and resources it protects, such as the default and release branches and tags or the production accounts (`outside.gate.real-refs`)
  - The agent's identity, including the bot, app, token and the human whose token it uses, is on no bypass or override list of the control (`outside.merge.no-agent-bypass`)
