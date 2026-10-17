---
idea: Approved bug reports to reproduction checklists
picture: no, it should read a bug report and investigate how to reproduce the bug and then create a checklist
  on how to reproduce (e.g. so i can create a comment on the corresponding issue)
goals:
- Read an approved bug report, inspect code and run local reproduction attempts without changing code
  or fixing the bug, then return valid reproduction steps as a checklist for the invoking AI agent to
  use in an issue comment, or report an error or blocker without interacting with the user.
targets:
- codex
reach: repository
hosting:
  platform: local only
  plan: not applicable
  visibility: unknown
kb_version: 0.1.0
facts:
  target_set: codex
  reach: repository
  plan_controls: unavailable
  opens_prs: false
  bypass_mode: true
  environment_trust: unknown
  no_prompt_scope: Skill runtime; full-access sandbox bypass has not been requested.
  no_code_changes: true
  no_fixes: true
  no_tool_installation: true
  local_tools_and_test_services_only: true
  missing_tools_result: Return an error to the calling agent.
  credentials_external_services_broader_permissions_result: Return a blocker to the calling agent.
  permanent_data_loss_payments_publishing_external_disclosure_result: Return a blocker to the calling
    agent.
  caller: AI agent invoking this procedure in its own workflow, context, tools, and model.
parts:
- id: A
  slug: bug-reproduction-checklist
  goal: Read an approved bug report, inspect code and run local reproduction attempts without changing
    code or fixing the bug, then return valid reproduction steps as a checklist for the invoking AI agent
    to use in an issue comment, or report an error or blocker without interacting with the user.
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
    external_system: none
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
    - selection.eligibility.codex-event-hooks
    - selection.eligibility.codex-prevent-hooks
    - selection.eligibility.codex-stop-hooks
    - selection.eligibility.codex-feedback-hooks
    - selection.eligibility.model-handler-prevent-hooks
    - selection.eligibility.model-handler-stop-hooks
    - selection.eligibility.model-handler-feedback-hooks
    reasons: []
    missing_facts:
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
  - prerequisites:
    - outside.ci.workflow-protected
    - outside.codeowners.agent-config
    required_for_goal: false
    availability: unavailable
    control: codeowners-agent-config
  - prerequisites:
    - outside.gate.no-broader-bypass
    required_for_goal: false
    availability: unavailable
    control: outer-isolation
retired_ids: []
research:
  survey_digest: 031c336224aeb220ab7e8b5c68fa15b513e5cab05c214fce71835e4756216830
  deep_digests:
    A: 30df48750d09c11eca55bf76716ef3cd41424897f4cabdd8bc14b289150f254d
accepted_revision:
  digest: 70dbad821d81ee1443861f063f3cd3c983c5538b201fc5117a7e4f8e71caaebe
  rule_ids:
  - idea.bug-reproduction-checklist.a.results
  - idea.bug-reproduction-checklist.a.data-risk-check
split_confirmed: true
survey_findings_used:
- F2
- F4
confirmations_history:
- run_id: bug-reproduction-checklist-research-20261011-01
  contract_digest: ff0c651b6c29b9e1f4e2b719543f38d3d76d08f676d64c88507ff3bbdd813969
  part_ids:
  - A
  date: '2026-10-11'
- run_id: bug-reproduction-checklist-deep-20261011-01
  contract_digest: 74f0488b1d01ea85c25a2a3c7c43083a867fba20cee527b7a4efa8eaba39e268
  part_ids:
  - A
  date: '2026-10-11'
---
The user confirmed one part, A, as an agent-invoked Codex skill. Selection recommends skills, and skills is chosen. Survey research is complete with F2 and F4 selected. Deep research is complete. The user accepted the separate results requirement and edited the combined F6+F7 requirement to best-effort internal checks with mandatory reported-result cleanup. The user confirmed the build and verification contract for the accepted revision in this session. The skill is built. The user confirmed both outside controls are precautions, not required for the goal. They are recommended, not verified.

Original user idea (verbatim): I want a skill that turns approved bug reports into reproduction checklists.

The confirmed answers and verbatim runtime constraints are also preserved in .harness/intake/bug-reproduction-checklist.md.

The user confirmed configuration protection is a precaution, not required for the goal.

The user confirmed outer isolation is a precaution, not required for the goal.

The user confirmed the initial research contract in this session (run bug-reproduction-checklist-research-20261011-01). The survey completed and retained F2, F3, F4; F1 was dropped because the context did not contain the quote or did not appear in fetched text. Finding use remains pending.

The user selected survey findings F2 and F4 for use. F3 was not selected. The provisional one-part split remains unconfirmed.

The user answered "agree" to confirming Part A as one skill. Recorded split_confirmed: true, chosen: skills, status: decided.

The user confirmed the deep-research contract in this session. Deep research for A completed, retaining F5, F6, F7, with no findings dropped. Requirement acceptance is pending.

The user edited F6+F7: internal checks and precautions are best effort; every reported result must be checked for personal information and cleaned. That edited rule was accepted through Forge. Draft description, procedure, and runtime activation cases are prepared in .harness/intake/.

The user answered "confirm" to the full build and verification contract with digest ab47344787da0ec7db34297a9c9b3b2506cca6f21ec49a777c14f1bec9c7c522. The relay records run bug-reproduction-checklist-build-20261011-01, Part A. Forge built the skill from the confirmed description and procedure. Verification will include the approved-report activation case and the missing-tool activation case; runtime activation results do not independently certify the returned checklist or cleanup.
