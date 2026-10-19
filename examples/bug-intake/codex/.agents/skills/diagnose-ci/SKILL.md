---
name: diagnose-ci
description: Diagnose failing CI checks on GitHub fix pull requests and propose a developer-applied fix. Use when investigating a failing PR check, CI failure, or failed workflow run. Not for editing code, rerunning workflows, posting comments, changing credentials, committing, pushing, opening pull requests, or merging.
---
# Diagnose ci

## Requirements

1. Diagnose checks for the latest commit SHA and distinguish stale check results from current-commit results.
2. Resolve the intended pull request from the developer context and select that pull request explicitly when using gh pr checks.

## Procedure

1. Resolve the repository and intended fix pull request from the developer's message and session context. When context identifies only a branch, resolve its pull request and verify that association. Ask when the target is ambiguous. Record the intended PR number or URL and select it explicitly when using `gh pr checks`; do not rely on that command's current-branch default.
2. Read the PR's latest commit SHA, check statuses and associated workflow runs using structured GitHub read tools or read-only GitHub CLI operations. Keep the explicit repository and PR target throughout the diagnosis. If authentication or access is unavailable, request the missing access or supplied logs without attempting to change authentication or permissions.
3. Match each relevant check and run to its commit SHA. Diagnose the latest commit's checks. Mark older results as historical or stale, and explain when no current-commit evidence is available. A prior green check does not establish the current commit's status. Recheck the current SHA after gathering evidence and identify any results made stale by a new push.
4. Read the failing job or step's available logs and identify the first actionable failure, separating it from downstream symptoms. For GitHub Actions, use the associated run and job logs. For an external provider, use evidence already supplied or available through authorized read tools; otherwise report its details URL and the missing log evidence. Separate observed failures from an unconfirmed explanation.
5. Summarize the failed check, current commit SHA, run or job reference, relevant log evidence and the supported cause or remaining uncertainty. Avoid presenting a successful historical run as a resolution of the current failure.
6. Propose a focused fix as an explanation or inline diff for the developer to apply. Include the files or configuration involved, why the proposal addresses the observed failure, and the checks the developer should run after applying it. Clearly identify any proposal that still needs more evidence.
7. Return the diagnosis and proposed validation steps to the developer. Keep this skill read-only: the developer applies and pushes the fix. Do not modify tracked files, commit, push, open or merge pull requests, post comments, rerun workflows, or change secrets or other external configuration.

Read [references/requirements.md](references/requirements.md) when you
need the rule id or the source behind one of the requirements above.
