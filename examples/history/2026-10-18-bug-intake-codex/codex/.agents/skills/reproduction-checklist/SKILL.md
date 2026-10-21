---
name: reproduction-checklist
description: Write and post reproduction checklists for approved GitHub bug reports. Use when a developer explicitly requests a reproduction checklist for an approved issue. Not for formatting or labeling reports, implementing fixes, checking pull requests, or closing issues.
disable-model-invocation: true
---
# Reproduction checklist

## Requirements

1. After the reproduction steps, describe the observed and expected results precisely and distinguish observations from speculation.
2. Redact sensitive information from logs included in the checklist or its supporting evidence.

## Procedure

1. Resolve the repository and issue from the developer's request. Read the report and verify approval from the issue or the developer's explicit statement. If the issue or its approval cannot be established, ask for the missing information before posting.
2. Extract the reported environment, relevant setup, and reproduction facts. Preserve unknown details as questions or explicitly marked gaps; do not present guessed setup or an untested hypothesis as an observation.
3. Write a checklist identifying the issue, environment and prerequisites, followed by numbered, actionable reproduction steps with checkboxes. Keep each step specific enough for the developer who will later check the fix.
4. After the steps, state the observed result and expected result precisely. Attribute reported observations to the report when you have not reproduced them yourself. Put speculative explanations in a separate, clearly marked section if they are needed.
5. Redact credentials, tokens, personal information and other sensitive details from any included logs or supporting evidence before returning or posting the checklist. Preserve useful diagnostic context without copying secret values.
6. Post the completed checklist as a comment on the resolved issue using structured GitHub tool arguments or the GitHub CLI. For a multiline CLI comment, write the exact comment to a UTF-8 temporary file and use `gh issue comment` with `--body-file`; do not interpolate the report into shell command text. Honor an explicit draft-only request. If posting is unavailable, return the checklist and state that it has not been posted.
7. Return the posted comment's link when available, along with any remaining information needed to reproduce the bug. Leave approval decisions, fixes and closure to their respective workflow steps.

Read [references/requirements.md](references/requirements.md) when you
need the rule id or the source behind one of the requirements above.
