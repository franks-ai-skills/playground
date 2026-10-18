---
idea: Handle incoming bug reports from intake to closing.
picture: Bug reports can come from different sources (like discord, gh issues, emails etc.), a github
  issue must be created for the bug report, the issue must reference the bugs origin (a link to the source,
  a copy of a conversation, the email), the issue should use a team-template on how to format it, after
  the issue is created and well formed, the first thing is to reproduce the bug and add the exact steps
  to reproduce the bug (the steps must hold, check in multiple runs) also it must state if the bug is
  consistent or only triggered sometimes, than a branch for the fix should be created, fix the issue,
  create a pr, fix ci errors (don't work around the ci), once everything is green and the fix is merged,
  close the issue and label the bug report
goals:
- 'Full lifecycle: a new bug report is formatted, triaged (severity, duplicate check, owner), tracked
  while it is fixed, and closed with a note once the fix is confirmed. For anyone who wants to use it
  (published as a public skill).'
- 'It works when every report ends up in a consistent state: formatted with the template, severity and
  owner set, duplicates linked, and closed only with a closing note that names the fix.'
targets:
- claude-code
- codex
reach: public
hosting:
  platform: github
  plan: free (assumed; the repositories it runs in vary)
  visibility: public
kb_version: 0.1.0
facts:
  target_set: both
  reach: public
  plan_controls: available
  opens_prs: true
  untrusted_repo: true
  lethal_trifecta: true
parts:
- id: A
  slug: intake
  goal: 'Take a bug report from any source (Discord, GitHub issue, email, ...), check whether an issue
    for the same bug already exists (duplicate check, as its own named step), and create a GitHub issue
    in the team template that references the report''s origin (a link, a copy of the conversation, or
    the email), with severity and owner set and labels that exist in the repository. The issue is checked
    mechanically before it is created: template headings, origin reference and labels.'
  status: decided
  answers:
    job: procedure
    event_without_agent: false
    must_survive_compromise: not-required
    who_disables: contributor
    every_time: always
    irreversible: true
    own_context: false
    script_checkable: true
    hook_event: PreToolUse
    hook_effect: prevent
  outcome: outside-alongside
  recommended: hooks
  chosen: hooks
  override_reason: null
  alternatives: []
  assessment:
  - concept: instructions
    rules:
    - selection.eligibility.must-hold-instructions
    - selection.eligibility.side-effects-instructions
    reasons:
    - Instructions cannot guarantee a rule that must hold every time; they are context, not enforcement
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
    rules:
    - selection.eligibility.must-hold-mcp
    reasons:
    - The model may not call an MCP tool, so an MCP server cannot make a step hold every time
    missing_facts: []
    state: ruled out
  - concept: skills
    rules:
    - selection.eligibility.must-hold-skills
    - selection.eligibility.side-effects-skills
    reasons:
    - A skill cannot guarantee a rule that must hold every time
    - The model must not decide on its own to run an irreversible or publishing procedure, so a model-invoked
      skill does not fit
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
    - selection.eligibility.side-effects-subagents
    reasons:
    - Delegation is a model decision, so a subagent cannot guarantee a check that must always run
    - Delegation starts on the model's decision, or on instructions or a skill it follows, so a subagent
      cannot keep an irreversible or publishing procedure from starting without the user
    missing_facts: []
    state: ruled out
  - concept: hooks
    rules:
    - selection.mechanism.must-hold-check
    reasons:
    - A rule that must hold every time and that a script can check is a hook
    missing_facts: []
    state: recommended
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
  - control: merge-rules
    prerequisites:
    - outside.gate.periodic-verification
    - outside.gate.plan-enforced
    - outside.gate.real-refs
    - outside.merge.no-agent-bypass
    - outside.merge.requester-cannot-approve
    availability: available
    required_for_goal: false
  - control: outer-isolation
    prerequisites:
    - outside.gate.no-broader-bypass
    availability: available
    required_for_goal: false
- id: B
  slug: reproduce
  goal: Reproduce the bug in several runs, add the exact steps that held to the issue, and state whether
    the bug is consistent or only triggered sometimes.
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
  connects_to:
  - to: A
    how: uses
  outside_controls:
  - control: codeowners-agent-config
    prerequisites:
    - outside.ci.workflow-protected
    - outside.codeowners.agent-config
    availability: available
    required_for_goal: false
  - control: merge-rules
    prerequisites:
    - outside.gate.periodic-verification
    - outside.gate.plan-enforced
    - outside.gate.real-refs
    - outside.merge.no-agent-bypass
    - outside.merge.requester-cannot-approve
    availability: available
    required_for_goal: false
  - control: outer-isolation
    prerequisites:
    - outside.gate.no-broader-bypass
    availability: available
    required_for_goal: false
- id: C
  slug: fix-and-pr
  goal: On the user's request, create a fix branch, fix the bug, open a pull request linked to the issue,
    and fix CI errors until every check is green.
  status: built
  answers:
    job: procedure
    event_without_agent: false
    must_survive_compromise: not-required
    who_disables: contributor
    every_time: usually
    irreversible: true
    trigger: user
    own_context: false
  outcome: outside-alongside
  recommended: commands
  chosen: commands
  override_reason: null
  alternatives: []
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
    - selection.mechanism.user-procedure
    reasons:
    - A procedure with side effects or timing the model must not decide is a user-invoked skill
    missing_facts: []
    state: recommended
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
  - control: merge-rules
    prerequisites:
    - outside.gate.periodic-verification
    - outside.gate.plan-enforced
    - outside.gate.real-refs
    - outside.merge.no-agent-bypass
    - outside.merge.requester-cannot-approve
    availability: available
    required_for_goal: false
  - control: outer-isolation
    prerequisites:
    - outside.gate.no-broader-bypass
    availability: available
    required_for_goal: false
- id: D
  slug: no-ci-workarounds
  goal: 'CI failures are fixed, never worked around: no skipped or deleted tests, no weakened CI configuration,
    no bypassed checks; checked mechanically before the agent commits or pushes and enforced on GitHub.'
  status: decided
  answers:
    job: check
    event_without_agent: true
    must_survive_compromise: required
    every_time: always
    early_feedback: true
    own_context: false
    script_checkable: true
    hook_event: PreToolUse
    hook_effect: prevent
  outcome: outside-alongside
  recommended: hooks
  chosen: hooks
  override_reason: null
  alternatives: []
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
    - selection.mechanism.early-feedback-mirror
    reasons:
    - An advisory hook mirrors the outside gate's check for earlier feedback
    missing_facts: []
    state: recommended
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
  connects_to:
  - to: C
    how: enforces
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
  - control: event-gate
    prerequisites:
    - outside.ci.required-on-ref
    - outside.gate.periodic-verification
    - outside.gate.plan-enforced
    - outside.gate.real-refs
    - outside.merge.no-agent-bypass
    - outside.merge.requester-cannot-approve
    availability: available
    required_for_goal: true
  - control: merge-rules
    prerequisites:
    - outside.gate.periodic-verification
    - outside.gate.plan-enforced
    - outside.gate.real-refs
    - outside.merge.no-agent-bypass
    - outside.merge.requester-cannot-approve
    availability: available
    required_for_goal: false
  - control: outer-isolation
    prerequisites:
    - outside.gate.no-broader-bypass
    availability: available
    required_for_goal: false
- id: E
  slug: merge-when-green
  goal: The fix is merged only after every required check passes.
  status: decided
  answers:
    job: check
    event_without_agent: true
    must_survive_compromise: required
    every_time: always
    early_feedback: false
  outcome: outside-instead
  recommended: null
  chosen: null
  override_reason: null
  alternatives: []
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
    - selection.eligibility.own-model-hooks
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
    - selection.mechanism.must-hold-check
    reasons: []
    missing_facts:
    - config_change_source
    - directory_added_source
    - hook_effect
    - hook_event
    - own_context
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
    rules:
    - selection.eligibility.must-hold-automation
    reasons:
    - Running the agent unattended does not make a rule hold on every tool call
    missing_facts: []
    state: ruled out
  connects_to:
  - to: C
    how: enforces
  outside_controls:
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
  - control: event-gate
    prerequisites:
    - outside.ci.required-on-ref
    - outside.gate.periodic-verification
    - outside.gate.plan-enforced
    - outside.gate.real-refs
    - outside.merge.no-agent-bypass
    - outside.merge.requester-cannot-approve
    availability: available
    required_for_goal: true
  - control: merge-rules
    prerequisites:
    - outside.gate.periodic-verification
    - outside.gate.plan-enforced
    - outside.gate.real-refs
    - outside.merge.no-agent-bypass
    - outside.merge.requester-cannot-approve
    availability: available
    required_for_goal: false
  - control: outer-isolation
    prerequisites:
    - outside.gate.no-broader-bypass
    availability: available
    required_for_goal: false
- id: F
  slug: close-and-label
  goal: Once the fix is merged, the issue is closed with a closing note that names the fix, and the bug
    report gets its final label.
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
  connects_to:
  - to: C
    how: uses
  outside_controls:
  - control: codeowners-agent-config
    prerequisites:
    - outside.ci.workflow-protected
    - outside.codeowners.agent-config
    availability: available
    required_for_goal: false
  - control: merge-rules
    prerequisites:
    - outside.gate.periodic-verification
    - outside.gate.plan-enforced
    - outside.gate.real-refs
    - outside.merge.no-agent-bypass
    - outside.merge.requester-cannot-approve
    availability: available
    required_for_goal: false
  - control: outer-isolation
    prerequisites:
    - outside.gate.no-broader-bypass
    availability: available
    required_for_goal: false
- id: G
  slug: untrusted-reports
  goal: 'Report content from outsiders is treated as data, never as instructions: it cannot make the agent
    leak the GitHub token or act outside the workflow.'
  status: decided
  answers:
    job: access-control
    event_without_agent: false
    must_survive_compromise: required
    every_time: always
  outcome: outside-alongside
  recommended: permissions-and-sandbox
  chosen: permissions-and-sandbox
  override_reason: null
  alternatives: []
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
    rules:
    - selection.mechanism.must-hold-access
    reasons:
    - A capability that must never be used, or must be approved first, is a permission rule
    missing_facts: []
    state: recommended
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
    - selection.eligibility.hard-limit-hooks
    reasons:
    - A hard limit on reading, writing or network access needs permissions and the sandbox; tool switching
      and unhooked paths bypass hooks
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
  connects_to:
  - to: A
    how: enforces
  - to: B
    how: enforces
  - to: C
    how: enforces
  - to: F
    how: enforces
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
  - control: merge-rules
    prerequisites:
    - outside.gate.periodic-verification
    - outside.gate.plan-enforced
    - outside.gate.real-refs
    - outside.merge.no-agent-bypass
    - outside.merge.requester-cannot-approve
    availability: available
    required_for_goal: false
  - control: outer-isolation
    prerequisites:
    - outside.gate.no-broader-bypass
    availability: available
    required_for_goal: false
retired_ids: []
research:
  survey_digest: null
  deep_digests: {}
accepted_revision:
  digest: e1805692c07794fb076d85404a8ce1d99581b7ad56af5cabea3935af53c2acde
  rule_ids:
  - idea.bug-intake.b.exact-steps
  - idea.bug-intake.b.repeated-runs
  - idea.bug-intake.b.consistency-statement
  - idea.bug-intake.b.observed-expected
  - idea.bug-intake.b.facts-vs-speculation
  - idea.bug-intake.b.order-dependency
  - idea.bug-intake.c.closing-keyword
  - idea.bug-intake.c.regression-test
  - idea.bug-intake.c.ci-workaround
  - idea.bug-intake.c.pwn-request
  - idea.bug-intake.c.self-merge
  - idea.bug-intake.c.green-before-done
  - idea.bug-intake.f.closing-note
  - idea.bug-intake.f.merged-first
  - idea.bug-intake.f.auto-closed
survey_findings_used:
- F1
- F3
- F4
- F10
- F11
- F12
- F13
- F14
split_confirmed: true
confirmations_history:
- run_id: 78cd85df-fce7-4e2d-a70a-185a616379f0
  contract_digest: 65fdcd9ca0df8bf6765b350e49d245a87bb8c3778e823631ee9982c5a52f3cec
  part_ids:
  - A
  - B
  - C
  - D
  - E
  - F
  - G
  date: '2026-10-18'
- run_id: 78cd85df-fce7-4e2d-a70a-185a616379f0
  contract_digest: fc70159e7f5c6dc73841840dbc3b1da4fccb82fa3da3b4be6a5ccc25961e6178
  part_ids:
  - A
  - B
  - C
  - D
  - E
  - F
  - G
  date: '2026-10-18'
- run_id: 78cd85df-fce7-4e2d-a70a-185a616379f0
  contract_digest: 1aca09f6e1858d262e090a9202425c1d4e84904834b83c048aee345e274784ae
  part_ids:
  - A
  - B
  - C
  - D
  - E
  - F
  - G
  date: '2026-10-18'
---

# Bug intake

Whole-idea answers confirmed by the user on 2026-10-18. Permission prompts
(bypass_mode): unknown, users of the public skill decide; left unset.
Hosting: plan and visibility vary; the user asked to assume the
capabilities of a public repository on GitHub Free.
