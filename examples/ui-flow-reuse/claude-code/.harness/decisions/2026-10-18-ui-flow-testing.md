---
idea: Test our web app's UI flows locally in a browser.
picture: a developer changes the frontend, runs the app locally, and asks the agent to test the affected
  UI flows in a real browser (click through, check what renders, look at console errors, take screenshots)
  before opening a pull request. It's working when a developer gets a clear pass or fail per flow, with
  screenshots and console logs, before the PR.
goals:
- A developer gets a clear pass or fail per affected UI flow, with screenshots and console logs, from
  a real local browser before opening a pull request.
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
- id: A
  slug: test-ui-flows-locally
  goal: The agent drives the locally running app in a real browser and captures screenshots and console
    logs for the flows the developer names; the developer judges pass or fail from that evidence.
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
  alternatives:
  - concept: instructions
    pros:
    - Always in context; cannot be missed
    cons:
    - Costs context in every session
    rules:
    - selection.mechanism.procedure-as-instructions
    why_not_chosen: the outcome reuse builds no harness mechanism
  assessment:
  - concept: instructions
    state: viable alternative
    rules:
    - selection.mechanism.procedure-as-instructions
    reasons:
    - A procedure can also live in the instruction file, as a pointer or a compressed index, when its
      omission would silently break output
    missing_facts: []
  - concept: configuration
    state: not preferred
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
  - concept: permissions-and-sandbox
    state: not preferred
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
  - concept: mcp
    state: not preferred
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
  - concept: skills
    state: recommended
    rules: []
    reasons: []
    missing_facts: []
  - concept: commands
    state: ruled out
    rules:
    - selection.eligibility.model-started-commands
    reasons:
    - A procedure the model should start on its own cannot be a user-invoked skill
    missing_facts: []
  - concept: subagents
    state: not preferred
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
  - concept: hooks
    state: unresolved
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
  - concept: plugins
    state: not preferred
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
  - concept: automation
    state: not preferred
    rules: []
    reasons:
    - no preference rule shows an advantage for this goal
    missing_facts: []
  connects_to: []
  outside_controls:
  - control: codeowners-agent-config
    prerequisites:
    - outside.ci.workflow-protected
    - outside.codeowners.agent-config
    availability: available
    required_for_goal: false
  reuse:
    name: webapp-testing
    source: https://github.com/anthropics/skills/tree/main/skills/webapp-testing
    license: Apache-2.0
    maintenance: maintained
retired_ids: []
research:
  survey_digest: null
  deep_digests: {}
accepted_revision:
  digest: c724ac91b59e022d5ed2ecffaeedbab8332d05b79462704ef64206d1b4d21f2d
  rule_ids:
  - idea.ui-flow-testing.a.wait-before-inspect
  - idea.ui-flow-testing.a.close-browser
  - idea.ui-flow-testing.a.license-file
  - idea.ui-flow-testing.a.only-controlled-origins
survey_findings_used:
- F10
split_confirmed: true
---
# UI flow testing

Developers test the UI flows a frontend change affects in a real local
browser before opening a pull request. The agent never opens pull
requests or pushes; a developer starts each step interactively.

Part A reuses webapp-testing from anthropics/skills unchanged. The
developer confirmed its fit for the adjusted part goal (the developer
judges pass or fail from the captured evidence) on 2026-10-18. It is
not installed yet, so its skill home is left open.
