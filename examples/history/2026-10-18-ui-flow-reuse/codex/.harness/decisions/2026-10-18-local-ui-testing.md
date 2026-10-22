---
idea: Test our web app's UI flows locally in a browser.
picture: the agent drives the locally running app in a real browser and captures screenshots and console
  logs for the flows the developer names; the developer judges pass or fail from that evidence.
goals:
- the agent drives the locally running app in a real browser and captures screenshots and console logs
  for the flows the developer names; the developer judges pass or fail from that evidence.
- Reuse webapp-testing unchanged from https://github.com/anthropics/skills/tree/main/skills/webapp-testing
  under Apache-2.0.
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
  opens_prs: false
  untrusted_repo: false
  bypass_mode: false
  lethal_trifecta: false
parts:
- id: A
  slug: webapp-testing
  goal: the agent drives the locally running app in a real browser and captures screenshots and console
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
  connects_to: []
  outside_controls:
  - control: codeowners-agent-config
    prerequisites:
    - outside.ci.workflow-protected
    - outside.codeowners.agent-config
    availability: unknown
    required_for_goal: false
  reuse:
    name: webapp-testing
    source: https://github.com/anthropics/skills/tree/main/skills/webapp-testing
    license: Apache-2.0
    maintenance: maintained
  goal_history:
  - goal: Test affected local UI flows in a real browser and give developers a clear pass or fail per
      flow, with screenshots and console logs, before a pull request.
    replaced: '2026-10-18'
    reason: 'User revised the goal: the agent captures browser evidence and the developer judges pass
      or fail.'
retired_ids: []
research:
  survey_digest: 1420be8e65da7160060ffa1f048e2292d0158d681859ee33aca743ee8667fb58
  deep_digests: {}
accepted_revision:
  digest: f6f1a9b7ba48dbbc780350f1f90a7ed03344e159728568be5fd596e38a9912d2
  rule_ids:
  - idea.local-ui-testing.a.python-playwright
  - idea.local-ui-testing.a.console-events
  - idea.local-ui-testing.a.screenshot-file
survey_findings_used:
- F1
- F2
- F3
split_confirmed: true
---
# Local UI testing

Reuse selected from the user’s confirmed inputs. No artifact is installed or built.

## Supplied constraints

- opens_prs: False
- pushes: False
- unattended: False
- interaction: A developer starts each step interactively.
- untrusted_repo: False
- tracker_writers: Only team members write issues and PRs.
- requested_part: One part only: test the UI flows locally. It's a procedure; it runs when a developer asks (no event without an agent); must survive compromise: not required; any contributor may change it; usually is fine; not irreversible (it only drives a local browser and writes local screenshots); the model may start it; no separate context.
- approved_read_only_fetches: https://api.github.com/repos/anthropics/skills/ and https://raw.githubusercontent.com/anthropics/skills/
- working_files: ../reuse-codex-scratch/; repository .harness/ holds only decisions, research, reports and cases.

- permission_prompts: Keep normal prompts (user confirmed A).

- input_trust: Tests use trusted local content and fixtures; no combination of untrusted content, secrets and outbound network access (user confirmed A).

## Revised goal and reuse decision

Original picture (verbatim): a developer changes the frontend, runs the app locally, and asks the agent to test the affected UI flows in a real browser (click through, check what renders, look at console errors, take screenshots) before opening a pull request. It's working when a developer gets a clear pass or fail per flow, with screenshots and console logs, before the PR.

Current picture and part goal (verbatim): the agent drives the locally running app in a real browser and captures screenshots and console logs for the flows the developer names; the developer judges pass or fail from that evidence.

The user confirmed unchanged reuse, fit for the revised goal, Apache-2.0 and maintenance: the anthropics/skills repository is actively maintained (commits this month), and its example status is accepted. Maintenance is user-confirmed, not an independently established survey finding.

The skill is not installed. Both reuse.path and reuse.skill_home are intentionally omitted at the user’s request. A staged download in sibling scratch is inspection material, not an installation. No new wrapper, skill build or modification to upstream is authorized by this reuse decision.

F1–F3 were selected from the initial survey. That survey used the earlier goal and remains historical; the requested deep pass must use the revised goal and its new brief. No earlier requirements are accepted or carried over.

Configuration protection remains a recommended precaution, not required for the goal; any contributor may change this procedure and compromise resistance is not required.

The user requests the deep-pass proposed requirements together in one list.
