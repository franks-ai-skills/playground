# Reproduction checklists

Throwaway repository for a hands-on Harness Forge trial.

The repository-local Codex skill lives at
[bug-reproduction-checklist](.agents/skills/bug-reproduction-checklist/SKILL.md).
An invoking agent supplies an approved bug report and local repository context.
The skill inspects code and runs existing local apps or tests, then returns a
validated Markdown checklist, an error, or a blocker. It does not install tools,
change code, fix bugs, post comments, or ask the user questions.

Internal privacy and data-risk precautions are best effort. Every returned
result must be checked for personal information and cleaned.

Build and verification evidence is recorded under `.harness/`; the verification
report is written to `.harness/reports/bug-reproduction-checklist.md`.

## Outside controls

- `codeowners-agent-config` (part A): recommended, not verified. Precaution; availability unavailable. Prerequisites: outside.ci.workflow-protected, outside.codeowners.agent-config.
- `outer-isolation` (part A): recommended, not verified. Precaution; availability unavailable. Prerequisites: outside.gate.no-broader-bypass.
