---
idea: Handle incoming bug reports from intake to closing
picture: 'For our team working on GitHub with Claude Code and Codex. In my words: a bug report arrives
  as a GitHub issue. Every incoming report gets formatted with our team''s template and labeled. For an
  approved report, the agent writes a reproduction checklist. A developer fixes the bug in a pull request;
  before the fix merges, it is checked against its reproduction checklist. If CI checks fail on the fix''s
  pull request, the agent fixes them. Once the fix ships, the tracker issue is closed.


  Updated D goal: Diagnose failing CI checks on the fix''s pull request and propose a fix; a developer
  applies and pushes it.

  Updated E goal and fallback: Close shipped tracker issues on its own once the agent sees a release;
  closing syncs to the customer status page and notifies reporting customers. If the harness cannot do
  that safely, leave closing entirely to something outside the agent.'
goals:
- It's working when every incoming report is formatted and labeled, every approved report has a reproduction
  checklist, no fix merges without passing its checklist check, and the issue is closed after the fix
  ships.
- Diagnose failing CI checks on the fix's pull request and propose a fix; a developer applies and pushes
  it.
targets:
- claude-code
- codex
reach: repository
hosting:
  platform: github
  plan: team
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
  goal: Format the report's text with the team's template (Title, Environment, Steps, Expected, Observed);
    a developer applies the formatted text to the issue, so the skill changes nothing on GitHub.
  status: decided
  answers:
    job: procedure
    event_without_agent: false
    must_survive_compromise: not-required
    who_disables: contributor
    every_time: usually
    irreversible: false
    own_context: false
    trigger: model
    external_system: none
  outcome: reuse
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
    why_not_chosen: the outcome reuse builds no harness mechanism
  connects_to: []
  outside_controls:
  - control: codeowners-agent-config
    prerequisites:
    - outside.ci.workflow-protected
    - outside.codeowners.agent-config
    availability: available
    required_for_goal: false
  goal_history:
  - goal: Format an incoming bug report with the team's template.
    replaced: '2026-10-18'
    reason: User supplied revised part goal in batched answers.
  reuse:
    name: bug-report-format
    source: https://github.com/example-team/bug-intake/tree/62eb5241487ef5d7fdb9efb8eb1d93b559a04437/.agents/skills/bug-report-format
    license: proprietary, owned by our team
    maintenance: maintained
    path: .agents/skills/bug-report-format
    skill_home: repository
  assessment:
  - concept: instructions
    rules:
    - selection.mechanism.procedure-as-instructions
    reasons:
    - A procedure can also live in the instruction file, as a pointer or a compressed index, when its
      omission would silently break output
    missing_facts: []
    state: viable alternative
  - concept: configuration
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: permissions-and-sandbox
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: mcp
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: skills
    rules: []
    reasons: []
    missing_facts: []
    state: recommended
  - concept: commands
    rules:
    - selection.eligibility.model-started-commands
    reasons:
    - A procedure the model should start on its own cannot be a user-invoked skill
    missing_facts: []
    state: ruled out
  - concept: subagents
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: hooks
    rules:
    - selection.eligibility.judgment-hooks
    - selection.eligibility.model-handler-event-hooks
    - selection.eligibility.claude-code-event-hooks
    - selection.eligibility.codex-event-hooks
    - selection.eligibility.claude-code-prevent-hooks
    - selection.eligibility.claude-code-stop-hooks
    - selection.eligibility.claude-code-feedback-hooks
    - selection.eligibility.codex-prevent-hooks
    - selection.eligibility.codex-stop-hooks
    - selection.eligibility.codex-feedback-hooks
    - selection.eligibility.model-handler-prevent-hooks
    - selection.eligibility.model-handler-stop-hooks
    - selection.eligibility.model-handler-feedback-hooks
    reasons: []
    missing_facts:
    - config_change_source
    - directory_added_source
    - hook_effect
    - hook_event
    - own_model
    - script_checkable
    - session_start_source
    - task_completed_trigger
    state: unresolved
  - concept: plugins
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: automation
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
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
    external_system: cli
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
  assessment:
  - concept: instructions
    rules:
    - selection.eligibility.must-hold-instructions
    reasons:
    - Instructions cannot guarantee a rule that must hold every time; they are context, not enforcement
    missing_facts: []
    state: ruled out
  - concept: configuration
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: permissions-and-sandbox
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: mcp
    rules:
    - selection.eligibility.must-hold-mcp
    reasons:
    - The model may not call an MCP tool, so an MCP server cannot make a step hold every time
    missing_facts: []
    state: ruled out
  - concept: skills
    rules:
    - selection.eligibility.must-hold-skills
    reasons:
    - A skill cannot guarantee a rule that must hold every time
    missing_facts: []
    state: ruled out
  - concept: commands
    rules:
    - selection.eligibility.must-hold-commands
    reasons:
    - A user-invoked skill cannot guarantee a rule that must hold every time
    missing_facts: []
    state: ruled out
  - concept: subagents
    rules:
    - selection.eligibility.must-hold-subagents
    reasons:
    - Delegation is a model decision, so a subagent cannot guarantee a check that must always run
    missing_facts: []
    state: ruled out
  - concept: hooks
    rules:
    - selection.eligibility.judgment-hooks
    reasons:
    - Portable hook handlers are commands and MCP tool calls, which cannot judge; judgment hooks (prompt,
      agent) are Claude Code only
    missing_facts: []
    state: ruled out
  - concept: plugins
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: automation
    rules:
    - selection.eligibility.must-hold-automation
    reasons:
    - Running the agent unattended does not make a rule hold on every tool call
    missing_facts: []
    state: ruled out
- id: B
  slug: reproduction-checklist
  goal: For an approved report, write a reproduction checklist and post it on the issue, started by the
    user.
  status: built
  answers:
    job: procedure
    event_without_agent: false
    must_survive_compromise: not-required
    who_disables: contributor
    every_time: usually
    irreversible: false
    own_context: false
    trigger: user
    external_system: cli
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
  goal_history:
  - goal: For an approved report, write a reproduction checklist.
    replaced: '2026-10-18'
    reason: User supplied revised part goal in batched answers.
  assessment:
  - concept: instructions
    rules:
    - selection.mechanism.procedure-as-instructions
    reasons:
    - A procedure can also live in the instruction file, as a pointer or a compressed index, when its
      omission would silently break output
    missing_facts: []
    state: viable alternative
  - concept: configuration
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: permissions-and-sandbox
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: mcp
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: skills
    rules:
    - selection.mechanism.procedure
    reasons:
    - A recurring procedure or knowledge needed only sometimes is a skill
    missing_facts: []
    state: viable alternative
  - concept: commands
    rules:
    - selection.mechanism.user-procedure
    reasons:
    - A procedure with side effects or timing the model must not decide is a user-invoked skill
    missing_facts: []
    state: recommended
  - concept: subagents
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: hooks
    rules:
    - selection.eligibility.judgment-hooks
    - selection.eligibility.model-handler-event-hooks
    - selection.eligibility.claude-code-event-hooks
    - selection.eligibility.codex-event-hooks
    - selection.eligibility.claude-code-prevent-hooks
    - selection.eligibility.claude-code-stop-hooks
    - selection.eligibility.claude-code-feedback-hooks
    - selection.eligibility.codex-prevent-hooks
    - selection.eligibility.codex-stop-hooks
    - selection.eligibility.codex-feedback-hooks
    - selection.eligibility.model-handler-prevent-hooks
    - selection.eligibility.model-handler-stop-hooks
    - selection.eligibility.model-handler-feedback-hooks
    reasons: []
    missing_facts:
    - config_change_source
    - directory_added_source
    - hook_effect
    - hook_event
    - own_model
    - script_checkable
    - session_start_source
    - task_completed_trigger
    state: unresolved
  - concept: plugins
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: automation
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
- id: C
  slug: check-fix-checklist
  goal: Before the fix merges, check the fix pull request against its reproduction checklist; no fix merges
    without passing its checklist check.
  status: built
  answers:
    job: procedure
    event_without_agent: false
    must_survive_compromise: required
    every_time: usually
    irreversible: false
    own_context: false
    trigger: user
    external_system: cli
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
  assessment:
  - concept: instructions
    rules:
    - selection.mechanism.procedure-as-instructions
    reasons:
    - A procedure can also live in the instruction file, as a pointer or a compressed index, when its
      omission would silently break output
    missing_facts: []
    state: viable alternative
  - concept: configuration
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: permissions-and-sandbox
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: mcp
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: skills
    rules:
    - selection.mechanism.procedure
    reasons:
    - A recurring procedure or knowledge needed only sometimes is a skill
    missing_facts: []
    state: viable alternative
  - concept: commands
    rules:
    - selection.mechanism.user-procedure
    reasons:
    - A procedure with side effects or timing the model must not decide is a user-invoked skill
    missing_facts: []
    state: recommended
  - concept: subagents
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: hooks
    rules:
    - selection.eligibility.judgment-hooks
    - selection.eligibility.model-handler-event-hooks
    - selection.eligibility.claude-code-event-hooks
    - selection.eligibility.codex-event-hooks
    - selection.eligibility.claude-code-prevent-hooks
    - selection.eligibility.claude-code-stop-hooks
    - selection.eligibility.claude-code-feedback-hooks
    - selection.eligibility.codex-prevent-hooks
    - selection.eligibility.codex-stop-hooks
    - selection.eligibility.codex-feedback-hooks
    - selection.eligibility.model-handler-prevent-hooks
    - selection.eligibility.model-handler-stop-hooks
    - selection.eligibility.model-handler-feedback-hooks
    reasons: []
    missing_facts:
    - config_change_source
    - directory_added_source
    - hook_effect
    - hook_event
    - own_model
    - script_checkable
    - session_start_source
    - task_completed_trigger
    state: unresolved
  - concept: plugins
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: automation
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
- id: D
  slug: diagnose-ci
  goal: Diagnose failing CI checks on the fix's pull request and propose a fix; a developer applies and
    pushes it.
  status: built
  answers:
    job: procedure
    event_without_agent: false
    must_survive_compromise: not-required
    who_disables: contributor
    every_time: usually
    irreversible: false
    own_context: false
    trigger: model
    external_system: cli
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
  goal_history:
  - goal: Fix the failing CI checks on the fix's pull request.
    replaced: '2026-10-18'
    reason: User supplied revised part goal in batched answers.
  assessment:
  - concept: instructions
    rules:
    - selection.mechanism.procedure-as-instructions
    reasons:
    - A procedure can also live in the instruction file, as a pointer or a compressed index, when its
      omission would silently break output
    missing_facts: []
    state: viable alternative
  - concept: configuration
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: permissions-and-sandbox
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: mcp
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: skills
    rules:
    - selection.mechanism.procedure
    reasons:
    - A recurring procedure or knowledge needed only sometimes is a skill
    missing_facts: []
    state: recommended
  - concept: commands
    rules:
    - selection.eligibility.model-started-commands
    reasons:
    - A procedure the model should start on its own cannot be a user-invoked skill
    missing_facts: []
    state: ruled out
  - concept: subagents
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: hooks
    rules:
    - selection.eligibility.judgment-hooks
    - selection.eligibility.model-handler-event-hooks
    - selection.eligibility.claude-code-event-hooks
    - selection.eligibility.codex-event-hooks
    - selection.eligibility.claude-code-prevent-hooks
    - selection.eligibility.claude-code-stop-hooks
    - selection.eligibility.claude-code-feedback-hooks
    - selection.eligibility.codex-prevent-hooks
    - selection.eligibility.codex-stop-hooks
    - selection.eligibility.codex-feedback-hooks
    - selection.eligibility.model-handler-prevent-hooks
    - selection.eligibility.model-handler-stop-hooks
    - selection.eligibility.model-handler-feedback-hooks
    reasons: []
    missing_facts:
    - config_change_source
    - directory_added_source
    - hook_effect
    - hook_event
    - own_model
    - script_checkable
    - session_start_source
    - task_completed_trigger
    state: unresolved
  - concept: plugins
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: automation
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
- id: E
  slug: close-shipped-issue
  goal: Close shipped tracker issues on its own once the agent sees a release; closing syncs to the customer
    status page and notifies reporting customers. If the harness cannot do that safely, leave closing
    entirely to something outside the agent.
  status: decided
  answers:
    job: procedure
    must_survive_compromise: not-required
    who_disables: contributor
    every_time: usually
    irreversible: true
    own_context: false
    trigger: model
    external_system: cli
    event_without_agent: false
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
  goal_history:
  - goal: Close the tracker issue once the fix ships.
    replaced: '2026-10-18'
    reason: User supplied revised part goal in batched answers.
  assessment:
  - concept: instructions
    rules:
    - selection.eligibility.side-effects-instructions
    reasons:
    - Instructions are context the model acts on by its own decision, so they cannot keep it from starting
      an irreversible or publishing procedure on its own
    missing_facts: []
    state: ruled out
  - concept: configuration
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: permissions-and-sandbox
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: mcp
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: skills
    rules:
    - selection.eligibility.side-effects-skills
    reasons:
    - The model must not decide on its own to run an irreversible or publishing procedure, so a model-invoked
      skill does not fit
    missing_facts: []
    state: ruled out
  - concept: commands
    rules:
    - selection.eligibility.model-started-commands
    reasons:
    - A procedure the model should start on its own cannot be a user-invoked skill
    missing_facts: []
    state: ruled out
  - concept: subagents
    rules:
    - selection.eligibility.side-effects-subagents
    reasons:
    - Delegation starts on the model's decision, or on instructions or a skill it follows, so a subagent
      cannot keep an irreversible or publishing procedure from starting without the user
    missing_facts: []
    state: ruled out
  - concept: hooks
    rules:
    - selection.eligibility.judgment-hooks
    - selection.eligibility.model-handler-event-hooks
    - selection.eligibility.claude-code-event-hooks
    - selection.eligibility.codex-event-hooks
    - selection.eligibility.claude-code-prevent-hooks
    - selection.eligibility.claude-code-stop-hooks
    - selection.eligibility.claude-code-feedback-hooks
    - selection.eligibility.codex-prevent-hooks
    - selection.eligibility.codex-stop-hooks
    - selection.eligibility.codex-feedback-hooks
    - selection.eligibility.model-handler-prevent-hooks
    - selection.eligibility.model-handler-stop-hooks
    - selection.eligibility.model-handler-feedback-hooks
    reasons: []
    missing_facts:
    - config_change_source
    - directory_added_source
    - hook_effect
    - hook_event
    - own_model
    - script_checkable
    - session_start_source
    - task_completed_trigger
    state: unresolved
  - concept: plugins
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
  - concept: automation
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
    state: not preferred
retired_ids: []
research:
  survey_digest: null
  deep_digests: {}
accepted_revision:
  digest: 03caeb0fd62b468d5be723224f6a732f33ca3d8dc78f77fb6a3453bf87dfce4e
  rule_ids:
  - idea.bug-report-lifecycle.b.results
  - idea.bug-report-lifecycle.b.redaction
  - idea.bug-report-lifecycle.c.latest-commit
  - idea.bug-report-lifecycle.c.required-merge-gate
  - idea.bug-report-lifecycle.d.current-commit
  - idea.bug-report-lifecycle.d.explicit-pr
survey_findings_used:
- F1
- F3
- F4
split_confirmed: true
---

For our team working on GitHub with Claude Code and Codex. In my words: a bug report arrives as a GitHub issue. Every incoming report gets formatted with our team's template and labeled. For an approved report, the agent writes a reproduction checklist. A developer fixes the bug in a pull request; before the fix merges, it is checked against its reproduction checklist. If CI checks fail on the fix's pull request, the agent fixes them. Once the fix ships, the tracker issue is closed.

It's working when every incoming report is formatted and labeled, every approved report has a reproduction checklist, no fix merges without passing its checklist check, and the issue is closed after the fix ships.

Additional confirmed context:
- A developer always starts each step in an interactive session and answers the prompts; nothing runs unattended.
- The agent only updates developer-opened pull requests to fix CI failures; it does not open pull requests.
- Only the team's own trusted repository is in scope.
- Only team members write issues and PRs in this private repository; the user considers that text trusted and requested recording untrusted input combined with secrets and network access as no.

Hosting capability source (availability, not configuration or verification): https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches

User-confirmed split (verbatim):
A1: format an incoming bug report with the team's template;
A2: label every incoming bug report;
B: for an approved report, write a reproduction checklist;
C: before the fix merges, check the fix pull request against its reproduction checklist (C uses B's checklist);
D: fix the failing CI checks on the fix's pull request;
E: close the tracker issue once the fix ships.

The user chose survey option A: use F1, F3, and F4; external tools remain references only.
Parts are provisional records awaiting selection; nothing-fits/null fields are placeholders, not assessed outcomes.

Latest user-confirmed changes:
- A1 reuses the existing repository skill unchanged; it formats text only, and a developer applies it to GitHub. The model may invoke A1.
- A2 must run always and needs judgment; record nothing-fits if no mechanism fits.
- B is user-started and posts its checklist on the issue.
- C must hold despite a compromised agent or a pull request tampering with the check.
- D reuses gh-fix-ci unchanged for diagnosis and a proposed fix; a developer applies and pushes the fix. Its skill home remains open, and it has not been installed.
- E is model-started and irreversible because closing syncs to a customer status page and notifies customers; the user explicitly accepts leaving closure entirely to an outside control if the harness cannot do it safely.
- A1 license and maintenance are team-owned proprietary and team-maintained; its source and repository home were confirmed by the user.
- D license, maintenance, fit and source were confirmed by the user.

Computed selections (not yet confirmed as a changed contract): A1 reuse skills; A2 nothing-fits with no standalone mechanism and combinations not assessed; B harness-only commands; C outside-alongside commands with a required compromise-resistant gate; D reuse skills with unresolved installation home. E awaits whether the release event occurs without an agent.

E timing clarification confirmed by the user: closure is needed only when an agent in an active session notices the release; no event without an agent.

E computed outcome: outside-instead, no standalone supported mechanism meets its confirmed requirements; combinations were not assessed. Use the user-authorized outside-only fallback and build no agent-closing mechanism. Required outside control is recommended, not verified.

Shared optional-control dependency confirmed by the user: code-owner protection of the broader agent configuration is a precaution, not required for the part goals. Required C/E outside-gate protection remains separately recorded.

User correction after the first verification:
- A1: user confirmed skills.invocation.side-effects-user-invoked does not apply because A1 returns formatted text and a developer applies it to GitHub.
- D: gh-fix-ci is not maintained. The upstream repository at https://github.com/openai/skills explicitly says "This repository is deprecated." and points to https://github.com/openai/plugins. The user reports that successor has no gh-fix-ci.
- D goal stays exactly: diagnose failing CI checks and propose a fix; a developer applies and pushes it.
- Reselection with maintenance unmaintained yields harness-only / skills. The old candidate no longer qualifies for reuse. Its historical provenance is preserved in .harness/intake/d-deprecated-reuse.json, and no deprecated skill is installed.
- Proposed new repository package name: diagnose-ci. All existing D answers, its goal and precautionary control dependency are preserved.
- The new D outcome changes its research brief; fresh deep research is needed before building D. Other parts and their accepted requirements are unchanged.

A1 reuse pin supplied by the user after D verification:
- Pinned source: https://github.com/example-team/bug-intake/tree/62eb5241487ef5d7fdb9efb8eb1d93b559a04437/.agents/skills/bug-report-format
- Commit: 62eb5241487ef5d7fdb9efb8eb1d93b559a04437
- Existing repository skill remains unchanged; full local-package review is recorded in .harness/intake/a1-reuse-review.md.
- User confirmed skills.invocation.side-effects-user-invoked does not apply to A1 or D.
