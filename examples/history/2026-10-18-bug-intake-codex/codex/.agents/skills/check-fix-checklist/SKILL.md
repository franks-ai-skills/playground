---
name: check-fix-checklist
description: Check a fix pull request against its approved bug report's reproduction checklist and report evidence for the latest commit. Use when a developer explicitly requests checklist verification before merging. Not for writing checklists, implementing fixes, repairing CI, merging, or closing issues.
disable-model-invocation: true
---
# Check fix checklist

## Requirements

1. Require the checklist check to pass on the latest commit SHA; a result for an older commit does not satisfy the check.
2. Require an outside protected required-status-check gate before merging, and describe the in-session checklist verdict as advisory rather than proof that the merge gate is configured.

## Procedure

1. Resolve the repository, fix pull request and linked approved bug report from the developer's request. Obtain the reproduction checklist produced by part B, the `reproduction-checklist` skill. Use a supplied copy or the checklist comment on the issue. If it is missing or its issue association is unclear, ask the developer to supply it or explicitly run B before checking the fix.
2. Establish the pull request's latest commit SHA and record it with the checklist reference. A supplied snapshot is evidence only for its stated commit and capture time; if the current SHA cannot be established, report the live check as inconclusive. An older commit's successful result does not satisfy the current check.
3. Assess each checklist item in the authorized environment. Record its setup or command, expected result, actual observed result, evidence reference and commit SHA. Distinguish fresh executions from supplied historical evidence. Mark missing environment, unavailable checks and ambiguous evidence as blocked or inconclusive instead of passing them.
4. Recheck the latest PR commit after collecting evidence. If the PR changed, mark the earlier result stale and require a new check for the latest SHA. Report the checklist as passing only when every item has passing evidence for that SHA; otherwise identify each failed, blocked, stale or inconclusive item.
5. Explain that this session's checklist verdict is advisory. The no-merge guarantee requires a protected outside required-status-check gate whose definition and verdict cannot be replaced by the PR or compromised agent. Read gate configuration only from trusted protected provenance; a PR-provided success claim does not establish enforcement. Report outside-control configuration as unverified unless independently established.
6. Describe the required gate conditions: protect the real target branches and resources; protect workflow and policy definitions or obtain them from a pinned external source; prevent bypass by the agent's bot, app, token and the human identity behind its token; prevent broader reachable credentials from bypassing the control; enforce it on the hosting plan; and periodically check for configuration drift. Report missing evidence for these conditions explicitly. Do not manufacture a successful status check or reconfigure the gate as part of this check.
7. Return a report containing the PR and issue references, checklist reference, assessed SHA, a per-item status/evidence table, the overall advisory verdict and the outside-gate evidence or gaps. Leave the merge and customer-facing issue closure to their authorized controls.

Read [references/requirements.md](references/requirements.md) when you
need the rule id or the source behind one of the requirements above.
