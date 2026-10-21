---
slug: bug-report-lifecycle
search_mode: live
briefs:
- pass: survey
  part_id: null
  digest: 326dc4b1c9715a4fcebedd9f50df6c6893a30ff64d45360350bb580dfb5c017c
- pass: deep
  part_id: B
  digest: cdb45811bd72c0a095d56fdeede664f36e6c7e32cddb1c20b86137892fadefe6
- pass: deep
  part_id: C
  digest: 2a501c063c1db1e9bc7281f8af04aa13d4827f96df6086de6e2e59e6d208c15b
- pass: deep
  part_id: A1
  digest: e4e2c279c5d7191c4fa4f224f9c1dfcf276ded5710169bc400fc2d1811f706e9
- pass: deep
  part_id: D
  digest: 7f86a7fc18365a9da5e125430e880a868da2d9605693809da1a423f1d6e02b51
findings:
- id: F1
  part_id: null
  claim: GitHub issue forms support input types, validations, default assignees, and default labels.
  source: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
  fetched: '2026-10-18'
  quote: You can define different input types, validations, default assignees, and default labels for
    your issue forms.
  context: You can define different input types, validations, default assignees, and default labels for
    your issue forms.
  brief_digest: 326dc4b1c9715a4fcebedd9f50df6c6893a30ff64d45360350bb580dfb5c017c
  source_role: primary
  pass: survey
- id: F3
  part_id: null
  claim: GitHub automatically closes a linked issue when its pull request merges into the repository's
    default branch.
  source: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  fetched: '2026-10-18'
  quote: When you merge a linked pull request into the default branch of a repository, its linked issue
    is automatically closed.
  context: When you merge a linked pull request into the default branch of a repository, its linked issue
    is automatically closed.
  brief_digest: 326dc4b1c9715a4fcebedd9f50df6c6893a30ff64d45360350bb580dfb5c017c
  source_role: primary
  pass: survey
- id: F4
  part_id: null
  claim: Mozilla's bug reporting guidance calls for precise actual and expected results and separating
    observations from speculation.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: Clearly separate facts (observations) from speculations.
  context: After your steps, precisely describe the observed (actual) result and the expected result.
    Clearly separate facts (observations) from speculations.
  brief_digest: 326dc4b1c9715a4fcebedd9f50df6c6893a30ff64d45360350bb580dfb5c017c
  source_role: primary
  pass: survey
- id: F5
  part_id: null
  claim: AutoTriage can apply labels, request missing details, retitle reports, and handle stale items.
  source: https://raw.githubusercontent.com/danielchalmers/AutoTriage/main/README.md
  fetched: '2026-10-18'
  quote: It can apply labels, ask for missing details, retitle unclear reports and handle stale items.
  context: It can apply labels, ask for missing details, retitle unclear reports and handle stale items.
  brief_digest: 326dc4b1c9715a4fcebedd9f50df6c6893a30ff64d45360350bb580dfb5c017c
  source_role: primary
  pass: survey
- id: F6
  part_id: null
  claim: AutoTriage's license permits use, modification, distribution, sublicensing, and sale, provided
    its copyright and permission notices accompany substantial copies.
  source: https://raw.githubusercontent.com/danielchalmers/AutoTriage/main/LICENSE
  fetched: '2026-10-18'
  quote: 'The above copyright notice and this permission notice shall be included in all

    copies or substantial portions of the Software.'
  context: 'Permission is hereby granted, free of charge, to any person obtaining a copy

    of this software and associated documentation files (the "Software"), to deal

    in the Software without restriction, including without limitation the rights

    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell

    copies of the Software, and to permit persons to whom the Software is

    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all

    copies or substantial portions of the Software.'
  brief_digest: 326dc4b1c9715a4fcebedd9f50df6c6893a30ff64d45360350bb580dfb5c017c
  source_role: primary
  pass: survey
- id: F7
  part_id: null
  claim: Oz Agent Action documents a failing-checks workflow that analyzes failure logs and attempts a
    fix.
  source: https://raw.githubusercontent.com/warpdotdev/oz-agent-action/main/README.md
  fetched: '2026-10-18'
  quote: '**Description:** Analyzes failure logs from the failed workflow to determine the cause and attempts

    a fix.'
  context: '**Description:** Analyzes failure logs from the failed workflow to determine the cause and
    attempts

    a fix.'
  brief_digest: 326dc4b1c9715a4fcebedd9f50df6c6893a30ff64d45360350bb580dfb5c017c
  source_role: primary
  pass: survey
- id: F8
  part_id: null
  claim: The SWE-agent project recommends using mini-SWE-agent instead of SWE-agent going forward.
  source: https://raw.githubusercontent.com/SWE-agent/SWE-agent/main/README.md
  fetched: '2026-10-18'
  quote: '> Our general recommendation is to use mini-SWE-agent instead of SWE-agent going forward.'
  context: '> Our general recommendation is to use mini-SWE-agent instead of SWE-agent going forward.'
  brief_digest: 326dc4b1c9715a4fcebedd9f50df6c6893a30ff64d45360350bb580dfb5c017c
  source_role: primary
  pass: survey
- id: F9
  part_id: null
  claim: GitHub documents an AI triage tool that evaluates whether new issues are actionable or require
    more information.
  source: https://docs.github.com/en/issues/tracking-your-work-with-issues/administering-issues/triaging-an-issue-with-ai
  fetched: '2026-10-18'
  quote: Use AI to triage new issues and determine whether the issue is actionable or needs more information.
  context: Use AI to triage new issues and determine whether the issue is actionable or needs more information.
  brief_digest: 326dc4b1c9715a4fcebedd9f50df6c6893a30ff64d45360350bb580dfb5c017c
  source_role: primary
  pass: survey
- id: F10
  part_id: B
  claim: 'Proposed rule idea.bug-report-lifecycle.B.results (check: judged): After the reproduction steps,
    describe the actual and expected results precisely and distinguish observations from speculation.'
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: After your steps, precisely describe the observed (actual) result and the expected result.
  context: After your steps, precisely describe the observed (actual) result and the expected result.
    Clearly separate facts (observations) from speculations.
  brief_digest: cdb45811bd72c0a095d56fdeede664f36e6c7e32cddb1c20b86137892fadefe6
  source_role: primary
  pass: deep
- id: F11
  part_id: B
  claim: 'Proposed rule idea.bug-report-lifecycle.B.redaction (check: judged): Redact sensitive information
    from logs included in the checklist or its supporting evidence.'
  source: https://github.com/UsefulSoftwareCo/executor/issues/1225
  fetched: '2026-10-18'
  quote: Redact anything sensitive.
  context: Redact anything sensitive. **Don't attach files from `~/.executor` — that's where your data
    and secrets live.**
  brief_digest: cdb45811bd72c0a095d56fdeede664f36e6c7e32cddb1c20b86137892fadefe6
  source_role: primary
  pass: deep
- id: F12
  part_id: C
  claim: 'Proposed rule idea.bug-report-lifecycle.C.latest-commit (check: judged): Require the checklist
    check to pass on the latest commit SHA.'
  source: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks
  fetched: '2026-10-18'
  quote: Required checks must pass on the latest commit SHA.
  context: Required checks must pass on the latest commit SHA. Checks from earlier commits don't satisfy
    the requirement.
  brief_digest: 2a501c063c1db1e9bc7281f8af04aa13d4827f96df6086de6e2e59e6d208c15b
  source_role: primary
  pass: deep
- id: F13
  part_id: C
  claim: 'Proposed rule idea.bug-report-lifecycle.C.required-merge-gate (check: judged): Enable required
    status checks so all required checks must pass before merging.'
  source: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
  fetched: '2026-10-18'
  quote: After enabling required status checks, all required status checks must pass before collaborators
    can merge changes into the protected branch.
  context: After enabling required status checks, all required status checks must pass before collaborators
    can merge changes into the protected branch.
  brief_digest: 2a501c063c1db1e9bc7281f8af04aa13d4827f96df6086de6e2e59e6d208c15b
  source_role: primary
  pass: deep
- id: F15
  part_id: A1
  claim: 'Proposed rule idea.bug-report-lifecycle.A1.distinguish-observations (check: judged): Clearly
    separate observed facts from speculation when formatting Expected and Observed results.'
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: Clearly separate facts (observations) from speculations.
  context: After your steps, precisely describe the observed (actual) result and the expected result.
    Clearly separate facts (observations) from speculations.
  brief_digest: e4e2c279c5d7191c4fa4f224f9c1dfcf276ded5710169bc400fc2d1811f706e9
  source_role: primary
  pass: deep
- id: F16
  part_id: A1
  claim: 'Proposed rule idea.bug-report-lifecycle.A1.detailed-steps (check: judged): Include detailed
    reproduction steps and expected behavior.'
  source: https://www.chromium.org/for-testers/bug-reporting-guidelines/
  fetched: '2026-10-18'
  quote: Mention detailed steps to replicate the issue.
  context: 'Provide a high-level problem description.

    Mention detailed steps to replicate the issue.

    Include the expected behavior.'
  brief_digest: e4e2c279c5d7191c4fa4f224f9c1dfcf276ded5710169bc400fc2d1811f706e9
  source_role: primary
  pass: deep
- id: F17
  part_id: A1
  claim: 'Proposed rule idea.bug-report-lifecycle.A1.concise-title (check: judged): Give the report a
    very short title describing the problem.'
  source: https://docs.python.org/3/bugs.html
  fetched: '2026-10-18'
  quote: For the “Title” field, enter a very short description of the problem; fewer than ten words is
    good.
  context: 'The submission form has two fields, “Title” and “Comment”.


    For the “Title” field, enter a very short description of the problem; fewer than ten words is good.'
  brief_digest: e4e2c279c5d7191c4fa4f224f9c1dfcf276ded5710169bc400fc2d1811f706e9
  source_role: primary
  pass: deep
- id: F22
  part_id: D
  claim: 'idea.bug-report-lifecycle.D.current-commit — check: judged. Require checks to pass on the latest
    commit SHA; earlier commits'' checks do not satisfy the requirement.'
  source: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks
  fetched: '2026-10-18'
  quote: Checks from earlier commits don't satisfy the requirement.
  context: Required checks must pass on the latest commit SHA. Checks from earlier commits don't satisfy
    the requirement.
  brief_digest: 7f86a7fc18365a9da5e125430e880a868da2d9605693809da1a423f1d6e02b51
  source_role: primary
  pass: deep
- id: F23
  part_id: D
  claim: 'idea.bug-report-lifecycle.D.explicit-pr — check: judged. Select the intended pull request explicitly
    when using gh pr checks; omitting its argument selects the current branch''s pull request.'
  source: https://cli.github.com/manual/gh_pr_checks
  fetched: '2026-10-18'
  quote: Without an argument, the pull request that belongs to the current branch is selected.
  context: 'Show CI status for a single pull request.


    Without an argument, the pull request that belongs to the current branch is selected.'
  brief_digest: 7f86a7fc18365a9da5e125430e880a868da2d9605693809da1a423f1d6e02b51
  source_role: primary
  pass: deep
- id: F26
  part_id: D
  claim: 'idea.bug-report-lifecycle.D.secret-lifecycle — check: judged. Proposed workflow credential maintenance
    should review whether registered secrets remain necessary and remove unnecessary ones.'
  source: https://docs.github.com/en/actions/reference/security/secure-use
  fetched: '2026-10-18'
  quote: Remove those that are no longer needed.
  context: Periodically review the registered secrets to confirm they are still required. Remove those
    that are no longer needed.
  brief_digest: 7f86a7fc18365a9da5e125430e880a868da2d9605693809da1a423f1d6e02b51
  source_role: primary
  pass: deep
support:
- finding_id: F1
  quote_check: pass
  verdict: supported
  worker_ref: support-f1
  finding_digest: 619392f1727b4e5a782156210bbca7758ed7fb4e633c1f44e7b7db2a1f1fa8b7
- finding_id: F2
  quote_check: fail
  verdict: missing
  worker_ref: support-f2
- finding_id: F3
  quote_check: pass
  verdict: supported
  worker_ref: support-f3
  finding_digest: fb9b8f7fcf4c702d4cc39783c3ee2e552fec740452548845366f99c325478549
- finding_id: F4
  quote_check: pass
  verdict: supported
  worker_ref: support-f4
  finding_digest: bbc42db90428cc2d0a3d195cd6199e0bec956923d0d6215cccfcfe086c40f9c2
- finding_id: F5
  quote_check: pass
  verdict: supported
  worker_ref: support-f5
  finding_digest: 49a234bf628e223ec205a3ce7fce3634a53861e99690e89ed9dc7941e2b38ec8
- finding_id: F6
  quote_check: pass
  verdict: supported
  worker_ref: support-f6
  finding_digest: 3a556d58986ae18fec77935b9f58a605c4296e4432b8ebe0cbd09f970c1067d6
- finding_id: F7
  quote_check: pass
  verdict: supported
  worker_ref: support-f7
  finding_digest: 76366ccf964184f90431bf26fa6a06ce33328708b2a8e9cd22481e36188f777e
- finding_id: F8
  quote_check: pass
  verdict: supported
  worker_ref: support-f8
  finding_digest: c18a8fd6bb570af40558910c88d5478a5c57fbcd472be3621a6ddb7a94ce0eb9
- finding_id: F9
  quote_check: pass
  verdict: supported
  worker_ref: support-f9
  finding_digest: 580cb610d2a2ba7b3b95c2f8d9561e85a64f80c5d7a6bfaffcd749eac783a9c7
- finding_id: F10
  quote_check: pass
  verdict: supported
  worker_ref: support-f10
  finding_digest: 78329f99d698c16e86b35c178a9ee5ca5c7d76cb6371e7f997217c52ef15f62f
- finding_id: F11
  quote_check: pass
  verdict: supported
  worker_ref: support-f11
  finding_digest: 1441816fcf359befbfca3ff59095e859d18b95897686027cfd752fd52c2918c7
- finding_id: F12
  quote_check: pass
  verdict: supported
  worker_ref: support-f12
  finding_digest: cb0d6cfebda3ae4df9137df108b24ddb516f130b48853f561bd96dfc9d490b9e
- finding_id: F13
  quote_check: pass
  verdict: supported
  worker_ref: support-f13
  finding_digest: edc739e7b743052189a003beef19527183fec0dfe4254c34a4ac966f0cb9e5a3
- finding_id: F14
  quote_check: fail
  verdict: missing
  worker_ref: support-f14
- finding_id: F15
  quote_check: pass
  verdict: supported
  worker_ref: support-f15
  finding_digest: 58d88c86970eca9424b8b7efedb110f3df0ebc9891b1509e3084447432513819
- finding_id: F16
  quote_check: pass
  verdict: supported
  worker_ref: support-f16
  finding_digest: 370f1d41e69172b3b074d399490aa0b9cc368ce0a8f23e76d08abc6dd1d90b65
- finding_id: F17
  quote_check: pass
  verdict: supported
  worker_ref: support-f17
  finding_digest: e7cc7dce66f179b4dca79ffb407a323befad8fe8dd8703f5fff4f5395da08854
- finding_id: F21
  quote_check: fail
  verdict: missing
  worker_ref: support-f21
- finding_id: F22
  quote_check: pass
  verdict: supported
  worker_ref: support-f22
  finding_digest: 95082c06dbd5bded2003ea84bab557185ed07408ec7fba0f593daa7598aef171
- finding_id: F23
  quote_check: pass
  verdict: supported
  worker_ref: support-f23
  finding_digest: 0d1707dfe0f9090ce342aa145de81a1cbd08f1e53daad6b6eee462901b667f65
- finding_id: F24
  quote_check: fail
  verdict: missing
  worker_ref: support-f24
- finding_id: F25
  quote_check: fail
  verdict: missing
  worker_ref: support-f25
- finding_id: F26
  quote_check: pass
  verdict: supported
  worker_ref: support-f26
  finding_digest: 52cb9d9d9d2343fb60bd3476d4e8ca50d846bfeca825ed14911633ce46138dee
drift: []
---
Findings grouped by pass and part are in the frontmatter; dropped findings are not kept.
