---
idea: Handle incoming bug reports from intake to closing.
picture: a bug report arrives as a GitHub issue. Every incoming report gets formatted with our team's
  template and labeled. For an approved report, the agent writes a reproduction checklist. A developer
  fixes the bug in a pull request; before the fix merges, it is checked against its reproduction checklist.
  If CI checks fail on the fix's pull request, the agent fixes them. Once the fix ships, the tracker issue
  is closed.
goals:
- Every incoming report is formatted and labeled.
- Every approved report has a reproduction checklist.
- No fix merges without passing its checklist check.
- The issue is closed after the fix ships.
targets:
- claude-code
- codex
reach: repository
hosting:
  platform: GitHub
  plan: Team
  visibility: private
kb_version: 0.1.0
facts:
  target_set: both
  reach: repository
  plan_controls: available
  opens_prs: false
  bypass_mode: false
  untrusted_repo: false
  lethal_trifecta: false
parts:
- id: A1
  slug: bug-report-format
  goal: Format an incoming bug report's text with the team's template (Title, Environment, Steps, Expected,
    Observed). A developer applies the formatted text to the GitHub issue; the skill itself does not change
    the issue.
  goal_history:
  - goal: Format an incoming bug report with the team's template.
    replaced: '2026-10-18'
    reason: The user wants to reuse the team's existing bug-report-format skill; formatting the text is
      what they need from it, and a developer applies the result to the issue.
  status: decided
  answers:
    job: procedure
    event_without_agent: false
    must_survive_compromise: not-required
    who_disables: contributor
    every_time: usually
    irreversible: false
    trigger: model
    own_context: false
  outcome: reuse
  recommended: skills
  chosen: skills
  override_reason: null
  reuse:
    name: bug-report-format
    source: https://github.com/example-team/bug-intake/tree/e2c098280917e7f92972649e86fc8e0200934677/.agents/skills/bug-report-format
    license: proprietary (owned by the team)
    maintenance: maintained
    path: .agents/skills/bug-report-format
    skill_home: repository
  alternatives:
  - concept: instructions
    pros:
    - Always in context; cannot be missed
    cons:
    - Costs context in every session
    rules:
    - selection.mechanism.procedure-as-instructions
    why_not_chosen: the outcome reuse builds no harness mechanism
  connects_to: []
  outside_controls:
  - control: codeowners-agent-config
    prerequisites:
    - outside.ci.workflow-protected
    - outside.codeowners.agent-config
    availability: available
    required_for_goal: false
- id: A2
  slug: label-bug-report
  goal: Label every incoming bug report.
  status: decided
  answers:
    job: procedure
    event_without_agent: false
    must_survive_compromise: not-required
    who_disables: contributor
    every_time: always
    irreversible: false
    own_context: false
    script_checkable: false
  outcome: nothing-fits
  recommended: null
  chosen: null
  override_reason: null
  alternatives: []
  connects_to: []
  outside_controls:
  - control: codeowners-agent-config
    prerequisites:
    - outside.ci.workflow-protected
    - outside.codeowners.agent-config
    availability: available
    required_for_goal: false
- id: B
  slug: repro-checklist
  goal: For an approved report, write a reproduction checklist.
  status: built
  answers:
    job: procedure
    event_without_agent: false
    must_survive_compromise: not-required
    who_disables: contributor
    every_time: usually
    irreversible: false
    trigger: user
    own_context: false
  outcome: harness-only
  recommended: commands
  chosen: commands
  override_reason: null
  alternatives:
  - concept: instructions
    pros:
    - Always in context; cannot be missed
    cons:
    - Costs context in every session
    rules:
    - selection.mechanism.procedure-as-instructions
    why_not_chosen: selection.mechanism.user-procedure comes before selection.mechanism.procedure-as-instructions
      in Forge's preference order (policy/selection.md)
  - concept: skills
    pros:
    - Loaded only when needed
    - Can bundle tested scripts
    cons:
    - Occasional missed activation
    - Advisory, not enforcement
    rules:
    - selection.mechanism.procedure
    why_not_chosen: selection.mechanism.user-procedure comes before selection.mechanism.procedure in Forge's
      preference order (policy/selection.md)
  connects_to: []
  outside_controls:
  - control: codeowners-agent-config
    prerequisites:
    - outside.ci.workflow-protected
    - outside.codeowners.agent-config
    availability: available
    required_for_goal: false
- id: C
  slug: check-fix-against-checklist
  goal: Before the fix merges, check the fix pull request against its reproduction checklist and report
    the result.
  status: built
  answers:
    job: procedure
    event_without_agent: false
    must_survive_compromise: required
    every_time: usually
    irreversible: false
    trigger: user
    own_context: false
  outcome: outside-alongside
  recommended: commands
  chosen: commands
  override_reason: null
  alternatives:
  - concept: instructions
    pros:
    - Always in context; cannot be missed
    cons:
    - Costs context in every session
    rules:
    - selection.mechanism.procedure-as-instructions
    why_not_chosen: selection.mechanism.user-procedure comes before selection.mechanism.procedure-as-instructions
      in Forge's preference order (policy/selection.md)
  - concept: skills
    pros:
    - Loaded only when needed
    - Can bundle tested scripts
    cons:
    - Occasional missed activation
    - Advisory, not enforcement
    rules:
    - selection.mechanism.procedure
    why_not_chosen: selection.mechanism.user-procedure comes before selection.mechanism.procedure in Forge's
      preference order (policy/selection.md)
  connects_to:
  - to: B
    how: uses
  outside_controls:
  - control: codeowners-agent-config
    prerequisites:
    - outside.ci.workflow-protected
    - outside.codeowners.agent-config
    availability: available
    required_for_goal: false
  - control: compromise-resistant-gate
    prerequisites:
    - outside.ci.workflow-protected
    - outside.gate.no-broader-bypass
    - outside.gate.periodic-verification
    - outside.gate.plan-enforced
    - outside.gate.real-refs
    - outside.merge.no-agent-bypass
    availability: available
    required_for_goal: true
- id: D
  slug: fix-ci
  goal: Diagnose failing CI checks on the fix's pull request and propose a fix; a developer applies and
    pushes it.
  goal_history:
  - goal: If CI checks fail on the fix's pull request, fix them by pushing commits to the developer's
      existing pull request branch.
    replaced: '2026-10-18'
    reason: The user chose to reuse gh-fix-ci from openai/skills as it is; it diagnoses and proposes a
      fix but does not push, so a developer applies and pushes the fix.
  status: built
  answers:
    job: procedure
    event_without_agent: false
    must_survive_compromise: not-required
    who_disables: contributor
    every_time: usually
    irreversible: false
    trigger: model
    own_context: false
  outcome: harness-only
  recommended: skills
  chosen: skills
  override_reason: null
  alternatives:
  - concept: instructions
    pros:
    - Always in context; cannot be missed
    cons:
    - Costs context in every session
    rules:
    - selection.mechanism.procedure-as-instructions
    why_not_chosen: selection.mechanism.procedure comes before selection.mechanism.procedure-as-instructions
      in Forge's preference order (policy/selection.md)
  connects_to: []
  outside_controls:
  - control: codeowners-agent-config
    prerequisites:
    - outside.ci.workflow-protected
    - outside.codeowners.agent-config
    availability: available
    required_for_goal: false
- id: E
  slug: close-shipped-issues
  goal: Close the tracker issue once the fix ships.
  status: decided
  answers:
    job: procedure
    event_without_agent: false
    must_survive_compromise: not-required
    who_disables: contributor
    every_time: usually
    irreversible: true
    trigger: model
    own_context: false
  outcome: outside-instead
  recommended: null
  chosen: null
  override_reason: null
  alternatives: []
  connects_to: []
  outside_controls:
  - control: codeowners-agent-config
    prerequisites:
    - outside.ci.workflow-protected
    - outside.codeowners.agent-config
    availability: available
    required_for_goal: false
  - control: compromise-resistant-gate
    prerequisites:
    - outside.ci.workflow-protected
    - outside.gate.no-broader-bypass
    - outside.gate.periodic-verification
    - outside.gate.plan-enforced
    - outside.gate.real-refs
    - outside.merge.no-agent-bypass
    availability: available
    required_for_goal: true
retired_ids:
- A
split_confirmed: true
research:
  survey_digest: null
  deep_digests: {}
accepted_revision:
  digest: 58d06ee37346a063060acbac891c898a1183b960dca472376329769d4aec6a91
  rule_ids:
  - idea.bug-report-lifecycle.b.exact-steps
  - idea.bug-report-lifecycle.b.expected-actual
  - idea.bug-report-lifecycle.b.reproducibility
  - idea.bug-report-lifecycle.b.facts-vs-speculation
  - idea.bug-report-lifecycle.b.fix-verification
  - idea.bug-report-lifecycle.b.only-approved
  - idea.bug-report-lifecycle.b.issue-text-as-data
  - idea.bug-report-lifecycle.c.per-item-verdict
  - idea.bug-report-lifecycle.c.fail-before-pass-after
  - idea.bug-report-lifecycle.c.overall-verdict
  - idea.bug-report-lifecycle.c.vague-item-passes
  - idea.bug-report-lifecycle.c.checklist-from-pr
  - idea.bug-report-lifecycle.c.content-as-data
  - idea.bug-report-lifecycle.a1.template-headings
  - idea.bug-report-lifecycle.d.real-or-flaky
  - idea.bug-report-lifecycle.d.flaky-source
  - idea.bug-report-lifecycle.d.rerun-as-proof
  - idea.bug-report-lifecycle.d.secret-quoting
  - idea.bug-report-lifecycle.d.content-as-data
  - idea.bug-report-lifecycle.d.no-push
survey_findings_used:
- F2
- F4
- F5
- F6
- F7
- F10
---

# Bug report lifecycle

Team bug reports on GitHub, from intake to closing, in Claude Code and Codex.

Whole-idea answers confirmed by the user on 2026-10-18:

- Reach: this one repository.
- Hosting: private repository on GitHub Team.
- The agent pushes commits to the developer's existing PR branch only; it never opens pull requests of its own.
- Nothing runs unattended: a developer starts each step in an interactive session.
- The agent works only in the team's own private repository.
- Only team members write issues.

Split confirmed on 2026-10-18: A was split into A1 (format) and A2 (label); A is retired. C uses B.

Part notes:

- A1 reuses the team's own `bug-report-format` skill; the user confirmed fit, license, maintenance and the repository home.
- A2 stays `nothing-fits` by the user's choice: labels must be applied every time, but choosing them needs judgment.
- C: the compromise-resistant gate is required because the verdict must hold even if the PR tampers with the check.
- D: first recorded as a reuse of `gh-fix-ci` from https://github.com/openai/skills (skills/.curated/gh-fix-ci), with D's goal narrowed to diagnose and propose. D's later deep pass kept finding F76: the openai/skills repository is deprecated. On 2026-10-18 the user marked `gh-fix-ci` not maintained (they found no successor in the OpenAI Plugins repository), so it is no longer a reuse candidate. The user kept the narrowed goal; D is now a model-started skill that Forge builds.
- E: closing publishes to the customer-facing status page and notifies reporters, so it is irreversible; the user wants the agent to close on its own, which no harness mechanism can do safely, so closing is left to an outside control.
