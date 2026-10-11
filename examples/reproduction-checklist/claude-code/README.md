# Reproduction checklists

Throwaway repository for a hands-on Harness Forge trial.

## Outside controls

- `codeowners-agent-config` (part A): recommended, not verified. Precaution; availability unknown. Prerequisites: outside.ci.workflow-protected, outside.codeowners.agent-config.
- `merge-rules` (part A): recommended, not verified. Precaution; availability unknown. Prerequisites: outside.gate.periodic-verification, outside.gate.plan-enforced, outside.gate.real-refs, outside.merge.no-agent-bypass, outside.merge.requester-cannot-approve.
- `outer-isolation` (part A): recommended, not verified. Precaution; availability unknown. Prerequisites: outside.gate.no-broader-bypass.
