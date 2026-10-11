---
idea: I want a skill that turns approved bug reports into reproduction checklists.
picture: When a collaborator asks an ai-agent to fix the bug (pointing to an issue) the first step should
  be to check if there is a list to reproduce the bug and if non is present, the issue report should be
  ammended (e.g. a comment on that issue) with that checklist.
goals:
- It's mostly for myself but I want to make it publicly available so anyone can use it on their own choosing.
  Any collaborator should be enabled to reproduce the bug on their own, without asking anyone and also
  ai-agents should understand the checklist so collaborators can ask their ai-agents to fix the bug.
- 'Both: a collaborator who has never seen the bug follows the checklist and reproduces it on the first
  try, without contacting anyone; and an AI agent given only the checklist reproduces the bug and proposes
  a fix.'
targets:
- claude-code
- codex
reach: public
hosting:
  platform: any (platform-agnostic)
  plan: any
  visibility: unknown
kb_version: 0.1.0
facts:
  target_set: both
  reach: public
  plan_controls: unknown
  opens_prs: true
  bypass_mode: true
  untrusted_repo: true
  lethal_trifecta: true
parts:
- id: A
  slug: repro-checklist
  goal: Given a bug report the agent was pointed to, first check whether it has all tools needed to reproduce
    the bug and verify the checklist, and inform the user about any missing tools; then reproduce the
    bug (only inspectable environment facts; separate, observable Expected and Actual without the suspected
    cause; run the minimal reproduction at least twice where safe and report the frequency of intermittent
    failures; no implementation edits while building it) and return a reproduction checklist that a human
    collaborator and an AI agent can both follow. The calling agent decides where the checklist goes.
  status: built
  answers:
    job: procedure
    event_without_agent: false
    must_survive_compromise: not-required
    who_disables: contributor
    every_time: usually
    irreversible: false
    trigger: model
    own_context: true
  outcome: harness-only
  recommended: subagents
  chosen: skills
  override_reason: I want something this Forge release can build now.
  alternatives: []
  connects_to: []
  outside_controls:
  - control: codeowners-agent-config
    prerequisites:
    - outside.ci.workflow-protected
    - outside.codeowners.agent-config
    availability: unknown
    required_for_goal: false
  - control: merge-rules
    prerequisites:
    - outside.gate.periodic-verification
    - outside.gate.plan-enforced
    - outside.gate.real-refs
    - outside.merge.no-agent-bypass
    - outside.merge.requester-cannot-approve
    availability: unknown
    required_for_goal: false
  - control: outer-isolation
    prerequisites:
    - outside.gate.no-broader-bypass
    availability: unknown
    required_for_goal: false
  assessment:
  - concept: instructions
    state: ruled out
    rules:
    - selection.eligibility.own-context-instructions
    reasons:
    - Instructions load into the session's own context, so they cannot give work a context, tools or model
      of its own
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
    state: ruled out
    rules:
    - selection.eligibility.own-context-skills
    reasons:
    - A skill runs in the session's context; work that needs its own context belongs in a subagent, which
      can use skills
    missing_facts: []
  - concept: commands
    state: ruled out
    rules:
    - selection.eligibility.model-started-commands
    - selection.eligibility.own-context-commands
    reasons:
    - A procedure the model should start on its own cannot be a user-invoked skill
    - A command is a user-invoked skill and runs in the session's context; work that needs its own context
      belongs in a subagent
    missing_facts: []
  - concept: subagents
    state: recommended
    rules:
    - selection.mechanism.fresh-context
    reasons:
    - Work that needs its own context, other tools or another model, such as a fresh-context review, is
      a subagent
    missing_facts: []
  - concept: hooks
    state: unresolved
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
retired_ids: []
research:
  survey_digest: null
  deep_digests: {}
accepted_revision:
  digest: fb67de3f6a2a7c750204d87f62f3c26fcf0646f53562bb594396b495eea19e25
  rule_ids:
  - idea.repro-checklist.a.tool-preflight
  - idea.repro-checklist.a.no-interaction
  - idea.repro-checklist.a.numbered-steps
  - idea.repro-checklist.a.inspectable-environment
  - idea.repro-checklist.a.expected-actual
  - idea.repro-checklist.a.repeat-and-frequency
  - idea.repro-checklist.a.no-implementation-edits
  - idea.repro-checklist.a.report-is-data
  - idea.repro-checklist.a.returns-only
survey_findings_used:
- F2
- F3
- F4
- F5
- F9
split_confirmed: true
---
# Reproduction checklists from approved bug reports

## The user's own words

Idea: "I want a skill that turns approved bug reports into reproduction checklists."

Goal: "It's mostly for myself but I want to make it publicly available so anyone can use it on their own choosing. Any collaborator should be enabled to reproduce the bug on their own, without asking anyone and also ai-agents should understand the checklist so collaborators can ask their ai-agents to fix the bug."

How they will know it works: C, both of: "A collaborator who has never seen the bug follows the checklist and reproduces it on the first try, without contacting anyone." and "An AI agent given only the checklist reproduces the bug and proposes a fix."

How it should work: "When a collaborator asks an ai-agent to fix the bug (pointing to an issue) the first step should be to check if there is a list to reproduce the bug and if non is present, the issue report should be ammended (e.g. a comment on that issue) with that checklist."

Scope: "the skill should only create the checklist, the ai-agent using the skill should handle where to put it (e.g. comment on the issue, in a pr, in jira)"

Hosting: "D. make it agnostic"

Survey use: "F2; F3; F4; F5; F9; (drop F17 and F19 those are relevant for forge, but not for the result)"

Scope update: "yes the skill should reproduce the bug to compose the checklist"

Approval: "A" (the skill does not check approval; asking the agent to fix the bug implies the report is approved).

Split adjustment: "one adjustment, drop the check if a checklist is already available, but ensure: the skill must also check if it has all tools to reproduce the bug and inform the user if it is missing tools to reproduce the bug or verify the checklist"

Part A job: "not sure: when part A is invoked (directly by the user, or a workflow where an ai-agent invokes the skill) it should handle everything by its own without human interaction (so missing tools might lead to an error as a result)", then "A" (procedure).

Part A mechanism: Forge recommended subagents; the user chose "Override: skill" because "I want something this Forge release can build now."

Outside controls: outer-isolation, merge-rules and codeowners-agent-config are precautions, not required for the goal.

## Open points

- None.
