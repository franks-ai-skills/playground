---
slug: bug-report-lifecycle
search_mode: live
briefs:
- pass: survey
  part_id: null
  digest: 81924d40a56cbc5cb0674af2017d989254a7082d1f0ab59738ddce3d2bb6e8e2
- pass: deep
  part_id: B
  digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
- pass: deep
  part_id: C
  digest: 7f1845957c229db0e03091f921ab58468647b13d2ba03fb6cd8307fac7baae72
- pass: deep
  part_id: A1
  digest: aec9328f478fcb98521a3f311d8ad2c65634eab88951557db0318f37d239009c
- pass: deep
  part_id: A2
  digest: 730b10c85b085249207a7a989281617ee443ed57ac4557e305174369b190af14
- pass: deep
  part_id: E
  digest: d24d970bd6fdacdf40fd055860e1919fd2d9b9a83305e5c4281b7f9b487b7ef5
- pass: deep
  part_id: D
  digest: c3f2209a4e540d33c5d35cd910f5b82b155325f6c290ffe3962649bd019f07b4
findings:
- id: F2
  part_id: null
  claim: An issue form does not add a label that doesn't already exist in the repository. The team's labels
    therefore have to be created before the template can apply them.
  source: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
  fetched: '2026-10-18'
  quote: If a label does not already exist in the repository, it will not be automatically added to the
    issue.
  context: Labels that will automatically be added to issues created with this template. If a label does
    not already exist in the repository, it will not be automatically added to the issue.
  brief_digest: 81924d40a56cbc5cb0674af2017d989254a7082d1f0ab59738ddce3d2bb6e8e2
  source_role: primary
  pass: survey
- id: F4
  part_id: null
  claim: GitHub closes a linked issue automatically when the linked pull request is merged into the repository's
    default branch. This happens on merge, which may come before the fix 'ships'.
  source: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  fetched: '2026-10-18'
  quote: When you merge a linked pull request into the default branch of a repository, its linked issue
    is automatically closed.
  context: When you merge a linked pull request into the default branch of a repository, its linked issue
    is automatically closed.
  brief_digest: 81924d40a56cbc5cb0674af2017d989254a7082d1f0ab59738ddce3d2bb6e8e2
  source_role: primary
  pass: survey
- id: F5
  part_id: null
  claim: Closing keywords in a pull request description work only when the pull request targets the repository's
    default branch.
  source: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  fetched: '2026-10-18'
  quote: The special keywords in a pull request description are interpreted only when the pull request
    targets the repository's default branch.
  context: The special keywords in a pull request description are interpreted only when the pull request
    targets the repository's default branch. If the pull request targets any other branch, then these
    keywords are ignored, no links are created, and merging the PR has no effect on the issues.
  brief_digest: 81924d40a56cbc5cb0674af2017d989254a7082d1f0ab59738ddce3d2bb6e8e2
  source_role: primary
  pass: survey
- id: F6
  part_id: null
  claim: If a pull request targets any branch other than the default (for example a release branch), its
    closing keywords are ignored and merging it has no effect on the issues.
  source: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  fetched: '2026-10-18'
  quote: If the pull request targets any other branch, then these keywords are ignored, no links are created,
    and merging the PR has no effect on the issues.
  context: The special keywords in a pull request description are interpreted only when the pull request
    targets the repository's default branch. If the pull request targets any other branch, then these
    keywords are ignored, no links are created, and merging the PR has no effect on the issues.
  brief_digest: 81924d40a56cbc5cb0674af2017d989254a7082d1f0ab59738ddce3d2bb6e8e2
  source_role: primary
  pass: survey
- id: F7
  part_id: null
  claim: Closing keywords can also be used in commit messages, not only in pull request descriptions.
  source: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  fetched: '2026-10-18'
  quote: You can also use closing keywords in a commit message.
  context: You can also use closing keywords in a commit message.
  brief_digest: 81924d40a56cbc5cb0674af2017d989254a7082d1f0ab59738ddce3d2bb6e8e2
  source_role: primary
  pass: survey
- id: F10
  part_id: null
  claim: Required status checks can be set to 'loose' or 'strict'.
  source: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
  fetched: '2026-10-18'
  quote: You can set up required status checks to either be "loose" or "strict."
  context: You can set up required status checks to either be "loose" or "strict."
  brief_digest: 81924d40a56cbc5cb0674af2017d989254a7082d1f0ab59738ddce3d2bb6e8e2
  source_role: primary
  pass: survey
- id: F23
  part_id: B
  claim: Mozilla's bug-writing guidelines call steps to reproduce the most important part of any bug report.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: Steps to reproduce are the most important part of any bug report.
  context: Steps to reproduce are the most important part of any bug report. If a developer is able to
    reproduce the bug, the bug is very likely to be fixed. If the steps are unclear, it might not even
    be possible to know whether the bug has been fixed.
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: primary
  pass: deep
- id: F24
  part_id: B
  claim: Mozilla's guidelines say that if the steps to reproduce are unclear, it may not be possible to
    tell whether the bug has been fixed.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: If the steps are unclear, it might not even be possible to know whether the bug has been fixed.
  context: Steps to reproduce are the most important part of any bug report. If a developer is able to
    reproduce the bug, the bug is very likely to be fixed. If the steps are unclear, it might not even
    be possible to know whether the bug has been fixed.
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: primary
  pass: deep
- id: F25
  part_id: B
  claim: Mozilla's guidelines tell reporters to keep facts (observations) clearly separate from speculation.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: Clearly separate facts (observations) from speculations.
  context: Clearly separate facts (observations) from speculations.
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: primary
  pass: deep
- id: F26
  part_id: B
  claim: Mozilla's outline defines Actual Results as what the application did after the steps were performed.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: 'Actual Results: What the application did after performing the above steps.'
  context: 'Actual Results: What the application did after performing the above steps.'
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: primary
  pass: deep
- id: F27
  part_id: B
  claim: Mozilla's outline defines Expected Results as what the application should have done if the bug
    were not present.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: 'Expected Results: What the application should have done, were the bug not present.'
  context: 'Expected Results: What the application should have done, were the bug not present.'
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: primary
  pass: deep
- id: F28
  part_id: B
  claim: Mozilla's guidelines ask reporters to say whether the bug reproduces at will, occasionally, or
    not at all.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: Indicate whether you can reproduce the bug at will, occasionally, or not at all.
  context: Indicate whether you can reproduce the bug at will, occasionally, or not at all.
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: primary
  pass: deep
- id: F29
  part_id: B
  claim: Simon Tatham's essay says the reporter should tell the programmer exactly what they did, including
    which buttons were pressed and in what order.
  source: https://www.chiark.greenend.org.uk/~sgtatham/bugs.html
  fetched: '2026-10-18'
  quote: So tell them exactly what you did.
  context: So tell them exactly what you did. If it's a graphical program, tell them which buttons you
    pressed and what order you pressed them in. If it's a program you run by typing a command, show them
    precisely what command you typed.
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: practitioner
  pass: deep
- id: F30
  part_id: B
  claim: For a command-line program, Tatham's essay says to show the exact command that was typed.
  source: https://www.chiark.greenend.org.uk/~sgtatham/bugs.html
  fetched: '2026-10-18'
  quote: If it's a program you run by typing a command, show them precisely what command you typed.
  context: So tell them exactly what you did. If it's a graphical program, tell them which buttons you
    pressed and what order you pressed them in. If it's a program you run by typing a command, show them
    precisely what command you typed.
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: practitioner
  pass: deep
- id: F32
  part_id: B
  claim: Tatham's essay says a bug report may leave out speculation but must not leave out facts.
  source: https://www.chiark.greenend.org.uk/~sgtatham/bugs.html
  fetched: '2026-10-18'
  quote: Leave out speculations if you want to, but don't leave out facts.
  context: Leave out speculations if you want to, but don't leave out facts.
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: practitioner
  pass: deep
- id: F33
  part_id: B
  claim: In Django's triage process, a bug ticket marked accepted means at least one triager has verified
    it as a legitimate bug.
  source: https://docs.djangoproject.com/en/dev/internals/contributing/triaging-tickets/
  fetched: '2026-10-18'
  quote: A ticket for a bug that has been accepted means that the issue has been verified by at least
    one triager as a legitimate bug - and should probably be fixed if possible.
  context: Often this means you could safely start writing a fix for it. This is generally more true for
    the case of accepted bugs than accepted features. A ticket for a bug that has been accepted means
    that the issue has been verified by at least one triager as a legitimate bug - and should probably
    be fixed if possible.
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: primary
  pass: deep
- id: F34
  part_id: B
  claim: Django's guidelines say a reporter should not promote their own ticket to Accepted; another community
    member sets that stage after reproducing and confirming the issue.
  source: https://docs.djangoproject.com/en/dev/internals/contributing/triaging-tickets/
  fetched: '2026-10-18'
  quote: Another community member should review the report and set this stage after reproducing and confirming
    the issue.
  context: Please don’t promote your own tickets to “Accepted”. Another community member should review
    the report and set this stage after reproducing and confirming the issue.
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: primary
  pass: deep
- id: F35
  part_id: B
  claim: Django's patch review process says a bug fix should come with a regression test, and the reviewer
    should confirm the test fails when the change is reverted.
  source: https://docs.djangoproject.com/en/dev/internals/contributing/triaging-tickets/
  fetched: '2026-10-18'
  quote: Confirm that the test fails if the change is reverted.
  context: If the ticket is for a bug, there should be a regression test. Confirm that the test fails
    if the change is reverted.
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: primary
  pass: deep
- id: F36
  part_id: B
  claim: Django's docs say that once a regression test is attached to the ticket, whoever writes the fix
    already has the test as a starting point.
  source: https://docs.djangoproject.com/en/dev/internals/contributing/triaging-tickets/
  fetched: '2026-10-18'
  quote: When someone writes a fix for the bug, they’ll already have your test as a starting point.
  context: Now, report your results on the Trac ticket, and please include the regression test as an attachment.
    When someone writes a fix for the bug, they’ll already have your test as a starting point.
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: primary
  pass: deep
- id: F37
  part_id: B
  claim: OWASP defines indirect prompt injection as an LLM taking in input from external sources such
    as websites or files.
  source: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  fetched: '2026-10-18'
  quote: Indirect prompt injections occur when an LLM accepts input from external sources, such as websites
    or files.
  context: Indirect prompt injections occur when an LLM accepts input from external sources, such as websites
    or files.
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: primary
  pass: deep
- id: F38
  part_id: B
  claim: OWASP recommends separating untrusted content and labeling it clearly to limit its influence
    on prompts.
  source: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  fetched: '2026-10-18'
  quote: Separate and clearly denote untrusted content to limit its influence on user prompts.
  context: Separate and clearly denote untrusted content to limit its influence on user prompts.
  brief_digest: d44d75ba4fb6bd73cb883953d7b70f4c7280ceb5822d59ad5486456ff6b37c02
  source_role: primary
  pass: deep
- id: F39
  part_id: C
  claim: 'Qt asks that every bug fix come with a regression test, ideally automated, that fails before
    the fix by exhibiting the bug and passes after the fix. This supports a judged rule for part C: the
    result must show the checklist failing on the unfixed code and passing on the fix.'
  source: https://wiki.qt.io/Writing_Unit_Tests
  fetched: '2026-10-18'
  quote: 'Whenever you fix a bug, please add a regression test for it: this is a test (ideally automatic)
    that fails before the fix, exhibiting the bug, and passes after the fix.'
  context: 'Whenever you fix a bug, please add a regression test for it: this is a test (ideally automatic)
    that fails before the fix, exhibiting the bug, and passes after the fix. Whenever you implement a
    new feature, please add tests that verify that the new feature works as intended.'
  brief_digest: 7f1845957c229db0e03091f921ab58468647b13d2ba03fb6cd8307fac7baae72
  source_role: primary
  pass: deep
- id: F40
  part_id: C
  claim: Mozilla's bug-writing guidelines say steps to reproduce are the most important part of a bug
    report.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: Steps to reproduce are the most important part of any bug report.
  context: How can a developer reproduce the bug on his or her own computer? Steps to reproduce are the
    most important part of any bug report. If a developer is able to reproduce the bug, the bug is very
    likely to be fixed.
  brief_digest: 7f1845957c229db0e03091f921ab58468647b13d2ba03fb6cd8307fac7baae72
  source_role: primary
  pass: deep
- id: F41
  part_id: C
  claim: 'Mozilla''s guidelines warn that when reproduction steps are unclear, it may be impossible to
    tell whether the bug has been fixed. This is a pitfall for part C: a vague checklist cannot verify
    a fix.'
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: If the steps are unclear, it might not even be possible to know whether the bug has been fixed.
  context: If a developer is able to reproduce the bug, the bug is very likely to be fixed. If the steps
    are unclear, it might not even be possible to know whether the bug has been fixed.
  brief_digest: 7f1845957c229db0e03091f921ab58468647b13d2ba03fb6cd8307fac7baae72
  source_role: primary
  pass: deep
- id: F43
  part_id: C
  claim: GitHub branch protection can require that all required status checks pass before changes merge
    into a protected branch. This is a way to make part C's check result block a merge.
  source: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
  fetched: '2026-10-18'
  quote: After enabling required status checks, all required status checks must pass before collaborators
    can merge changes into the protected branch.
  context: After enabling required status checks, all required status checks must pass before collaborators
    can merge changes into the protected branch.
  brief_digest: 7f1845957c229db0e03091f921ab58468647b13d2ba03fb6cd8307fac7baae72
  source_role: primary
  pass: deep
- id: F44
  part_id: C
  claim: On GitHub, any person or integration with write permission to a repository can set the state
    of any status check. A reported checklist result can therefore be forged unless its source is restricted,
    which matters because part C must survive compromise.
  source: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
  fetched: '2026-10-18'
  quote: Any person or integration with write permissions to a repository can set the state of any status
    check in the repository, but in some cases you may only want to accept a status check from a specific
    GitHub App.
  context: Any person or integration with write permissions to a repository can set the state of any status
    check in the repository, but in some cases you may only want to accept a status check from a specific
    GitHub App.
  brief_digest: 7f1845957c229db0e03091f921ab58468647b13d2ba03fb6cd8307fac7baae72
  source_role: primary
  pass: deep
- id: F49
  part_id: C
  claim: OWASP describes indirect prompt injection as an LLM accepting input from external sources such
    as websites or files. For part C, the PR diff, issue text and checklist are external content an injection
    could arrive through.
  source: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  fetched: '2026-10-18'
  quote: Indirect prompt injections occur when an LLM accepts input from external sources, such as websites
    or files.
  context: Indirect prompt injections occur when an LLM accepts input from external sources, such as websites
    or files.
  brief_digest: 7f1845957c229db0e03091f921ab58468647b13d2ba03fb6cd8307fac7baae72
  source_role: primary
  pass: deep
- id: F52
  part_id: A1
  claim: Mozilla's bug-writing guidelines say steps to reproduce are the most important part of a bug
    report, and that unclear steps can make it impossible to tell whether the bug was fixed. A formatted
    report therefore needs concrete, ordered Steps.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: Steps to reproduce are the most important part of any bug report.
  context: Steps to reproduce are the most important part of any bug report. If a developer is able to
    reproduce the bug, the bug is very likely to be fixed. If the steps are unclear, it might not even
    be possible to know whether the bug has been fixed.
  brief_digest: aec9328f478fcb98521a3f311d8ad2c65634eab88951557db0318f37d239009c
  source_role: primary
  pass: deep
- id: F53
  part_id: A1
  claim: 'Mozilla''s guidelines ask reporters to state how reproducible the bug is: at will, occasionally,
    or not at all.'
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: Indicate whether you can reproduce the bug at will, occasionally, or not at all.
  context: Indicate whether you can reproduce the bug at will, occasionally, or not at all.
  brief_digest: aec9328f478fcb98521a3f311d8ad2c65634eab88951557db0318f37d239009c
  source_role: primary
  pass: deep
- id: F54
  part_id: A1
  claim: Mozilla's guidelines say to describe the observed (actual) result and the expected result precisely,
    and to keep facts (observations) clearly separate from speculation. This maps to the Expected and
    Observed sections.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: Clearly separate facts (observations) from speculations.
  context: After your steps, precisely describe the observed (actual) result and the expected result.
    Clearly separate facts (observations) from speculations.
  brief_digest: aec9328f478fcb98521a3f311d8ad2c65634eab88951557db0318f37d239009c
  source_role: primary
  pass: deep
- id: F55
  part_id: A1
  claim: Mozilla's guidelines say a good summary (title) should quickly and uniquely identify the bug
    and describe the problem, not a suggested solution.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: A good summary should quickly and uniquely identify a bug report.
  context: A good summary should quickly and uniquely identify a bug report. It should explain the problem,
    not your suggested solution.
  brief_digest: aec9328f478fcb98521a3f311d8ad2c65634eab88951557db0318f37d239009c
  source_role: primary
  pass: deep
- id: F57
  part_id: A1
  claim: Simon Tatham states that the aim of a bug report is to let the programmer see the program fail
    in front of them.
  source: https://www.chiark.greenend.org.uk/~sgtatham/bugs.html
  fetched: '2026-10-18'
  quote: In a nutshell, the aim of a bug report is to enable the programmer to see the program failing
    in front of them.
  context: In a nutshell, the aim of a bug report is to enable the programmer to see the program failing
    in front of them.
  brief_digest: aec9328f478fcb98521a3f311d8ad2c65634eab88951557db0318f37d239009c
  source_role: practitioner
  pass: deep
- id: F59
  part_id: A1
  claim: OWASP defines indirect prompt injection as an LLM accepting input from external sources whose
    content changes the model's behavior in unintended ways. Issue text from outside reporters is this
    kind of external input to a formatting skill.
  source: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  fetched: '2026-10-18'
  quote: Indirect prompt injections occur when an LLM accepts input from external sources, such as websites
    or files.
  context: Indirect prompt injections occur when an LLM accepts input from external sources, such as websites
    or files. The content may have in the external content data that when interpreted by the model, alters
    the behavior of the model in unintended or unexpected ways. Like direct injections, indirect injections
    can be either intentional or unintentional.
  brief_digest: aec9328f478fcb98521a3f311d8ad2c65634eab88951557db0318f37d239009c
  source_role: primary
  pass: deep
- id: F60
  part_id: A1
  claim: As a mitigation, OWASP recommends separating and clearly marking untrusted content to limit its
    influence.
  source: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  fetched: '2026-10-18'
  quote: Separate and clearly denote untrusted content to limit its influence on user prompts.
  context: Separate and clearly denote untrusted content to limit its influence on user prompts.
  brief_digest: aec9328f478fcb98521a3f311d8ad2c65634eab88951557db0318f37d239009c
  source_role: primary
  pass: deep
- id: F62
  part_id: A2
  claim: The Kubernetes triage guide says the reporter usually applies the `kind` label.
  source: https://raw.githubusercontent.com/kubernetes/community/master/contributors/guide/issue-triage.md
  fetched: '2026-10-18'
  quote: Usually the `kind` label is applied by the person submitting the issue.
  context: Usually the `kind` label is applied by the person submitting the issue. Issues that feature
    the wrong `kind` (for example, support requests labelled as bugs) can be corrected by someone triaging;
    double-checking is a good approach. Our [issue templates](https://github.com/kubernetes/kubernetes/issues/new/choose)
    aim to steer people to the right kind.
  brief_digest: 730b10c85b085249207a7a989281617ee443ed57ac4557e305174369b190af14
  source_role: primary
  pass: deep
- id: F63
  part_id: A2
  claim: The Kubernetes triage guide says a triager can correct an issue that has the wrong `kind`, such
    as a support request labelled as a bug, and recommends double-checking.
  source: https://raw.githubusercontent.com/kubernetes/community/master/contributors/guide/issue-triage.md
  fetched: '2026-10-18'
  quote: Issues that feature the wrong `kind` (for example, support requests labelled as bugs) can be
    corrected by someone triaging; double-checking is a good approach.
  context: Usually the `kind` label is applied by the person submitting the issue. Issues that feature
    the wrong `kind` (for example, support requests labelled as bugs) can be corrected by someone triaging;
    double-checking is a good approach. Our [issue templates](https://github.com/kubernetes/kubernetes/issues/new/choose)
    aim to steer people to the right kind.
  brief_digest: 730b10c85b085249207a7a989281617ee443ed57ac4557e305174369b190af14
  source_role: primary
  pass: deep
- id: F87
  part_id: E
  claim: GitHub closes a linked issue automatically when the linked pull request is merged into the repository's
    default branch.
  source: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  fetched: '2026-10-18'
  quote: When you merge a linked pull request into the default branch of a repository, its linked issue
    is automatically closed.
  context: When you link a pull request to the issue the pull request addresses, collaborators can see
    that someone is working on the issue. When you merge a linked pull request into the default branch
    of a repository, its linked issue is automatically closed.
  brief_digest: d24d970bd6fdacdf40fd055860e1919fd2d9b9a83305e5c4281b7f9b487b7ef5
  source_role: primary
  pass: deep
- id: F88
  part_id: E
  claim: Closing keywords in a pull request description are honored only when the pull request targets
    the default branch; for any other target branch they are ignored, no links are created, and merging
    has no effect on the issues.
  source: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  fetched: '2026-10-18'
  quote: If the pull request targets any other branch, then these keywords are ignored, no links are created,
    and merging the PR has no effect on the issues.
  context: The special keywords in a pull request description are interpreted only when the pull request
    targets the repository's default branch. If the pull request targets any other branch, then these
    keywords are ignored, no links are created, and merging the PR has no effect on the issues.
  brief_digest: d24d970bd6fdacdf40fd055860e1919fd2d9b9a83305e5c4281b7f9b487b7ef5
  source_role: primary
  pass: deep
- id: F89
  part_id: E
  claim: 'Closing keywords also work in commit messages: the issue closes when the commit is merged into
    the default branch, but the containing pull request is not listed as a linked pull request.'
  source: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  fetched: '2026-10-18'
  quote: The issue will be closed when you merge the commit into the default branch, but the pull request
    that contains the commit will not be listed as a linked pull request.
  context: You can also use closing keywords in a commit message. The issue will be closed when you merge
    the commit into the default branch, but the pull request that contains the commit will not be listed
    as a linked pull request.
  brief_digest: d24d970bd6fdacdf40fd055860e1919fd2d9b9a83305e5c4281b7f9b487b7ef5
  source_role: primary
  pass: deep
- id: F99
  part_id: D
  claim: GitHub's CI marked a test as flaky when it passed on a rerun, but this approach could not catch
    some kinds of flaky tests, such as time-based ones.
  source: https://github.blog/2020-12-16-reducing-flaky-builds-by-18x
  fetched: '2026-10-18'
  quote: However, certain types of flaky tests couldn’t be detected with this approach, such as a time-based
    flaky test.
  context: If the test passed when rerun, it was marked as flaky. However, certain types of flaky tests
    couldn’t be detected with this approach, such as a time-based flaky test. (If your test failed because
    it was a leap year, rerunning it two minutes later won’t help.)
  brief_digest: c3f2209a4e540d33c5d35cd910f5b82b155325f6c290ffe3962649bd019f07b4
  source_role: primary
  pass: deep
- id: F100
  part_id: D
  claim: Martin Fowler recommends moving non-deterministic tests into a quarantined area and fixing them
    quickly.
  source: https://martinfowler.com/articles/nonDeterminism.html
  fetched: '2026-10-18'
  quote: Place any non-deterministic test in a quarantined area.
  context: Place any non-deterministic test in a quarantined area. (But fix quarantined tests quickly.)
  brief_digest: c3f2209a4e540d33c5d35cd910f5b82b155325f6c290ffe3962649bd019f07b4
  source_role: practitioner
  pass: deep
- id: F102
  part_id: D
  claim: Martin Fowler names lack of isolation between tests as a common cause of non-deterministic test
    failures.
  source: https://martinfowler.com/articles/nonDeterminism.html
  fetched: '2026-10-18'
  quote: When you are tracking down a non-determinism, lack of isolation is a common and frustrating cause.
  context: As you get to the larger operational scope of functional tests, it gets progressively harder
    to keep tests isolated. When you are tracking down a non-determinism, lack of isolation is a common
    and frustrating cause. Keep your tests isolated from each other, so that execution of one test will
    not affect any others.
  brief_digest: c3f2209a4e540d33c5d35cd910f5b82b155325f6c290ffe3962649bd019f07b4
  source_role: practitioner
  pass: deep
- id: F103
  part_id: D
  claim: Martin Fowler names calls to the system clock as a source of non-deterministic tests.
  source: https://martinfowler.com/articles/nonDeterminism.html
  fetched: '2026-10-18'
  quote: Few things are more non-deterministic than a call to the system clock.
  context: Few things are more non-deterministic than a call to the system clock. Each time you call it,
    you get a new result, and any tests that depend on it can thus change.
  brief_digest: c3f2209a4e540d33c5d35cd910f5b82b155325f6c290ffe3962649bd019f07b4
  source_role: practitioner
  pass: deep
- id: F104
  part_id: D
  claim: Martin Fowler names tests that call live remote systems as a source of non-determinism.
  source: https://martinfowler.com/articles/nonDeterminism.html
  fetched: '2026-10-18'
  quote: Often remote systems don't have test system we can call, which means hitting a live system.
  context: Testing with such remote systems brings a number of problems, and non-determinism is high on
    the list. Often remote systems don't have test system we can call, which means hitting a live system.
    If there is a test system, it may not be stable enough to provide deterministic responses.
  brief_digest: c3f2209a4e540d33c5d35cd910f5b82b155325f6c290ffe3962649bd019f07b4
  source_role: practitioner
  pass: deep
- id: F106
  part_id: D
  claim: GitHub Actions automatically redacts the contents of GitHub secrets that are printed to workflow
    logs.
  source: https://docs.github.com/en/actions/concepts/security/secrets
  fetched: '2026-10-18'
  quote: GitHub Actions automatically redacts the contents of all GitHub secrets that are printed to workflow
    logs.
  context: GitHub Actions automatically redacts the contents of all GitHub secrets that are printed to
    workflow logs. GitHub Actions also redacts information that is recognized as sensitive, but is not
    stored as a secret.
  brief_digest: c3f2209a4e540d33c5d35cd910f5b82b155325f6c290ffe3962649bd019f07b4
  source_role: primary
  pass: deep
- id: F107
  part_id: D
  claim: GitHub does not guarantee secret redaction in logs, and the runner can redact only secrets used
    within the current job. Logs an agent reads may therefore still contain sensitive values.
  source: https://docs.github.com/en/actions/concepts/security/secrets
  fetched: '2026-10-18'
  quote: Because there are multiple ways a secret value can be transformed, this redaction is not guaranteed.
  context: Because there are multiple ways a secret value can be transformed, this redaction is not guaranteed.
    Additionally, the runner can only redact secrets used within the current job.
  brief_digest: c3f2209a4e540d33c5d35cd910f5b82b155325f6c290ffe3962649bd019f07b4
  source_role: primary
  pass: deep
- id: F108
  part_id: D
  claim: Any GitHub event that runs with secrets can introduce a pwn request if it checks out or downloads
    untrusted code and executes it.
  source: https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target
  fetched: '2026-10-18'
  quote: Any event that runs with secrets can introduce a pwn request if it checks out or downloads and
    executes untrusted code.
  context: Any event that runs with secrets can introduce a pwn request if it checks out or downloads
    and executes untrusted code.
  brief_digest: c3f2209a4e540d33c5d35cd910f5b82b155325f6c290ffe3962649bd019f07b4
  source_role: primary
  pass: deep
- id: F110
  part_id: D
  claim: OWASP recommends separating and clearly marking untrusted content to limit its influence as a
    prompt-injection mitigation.
  source: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  fetched: '2026-10-18'
  quote: Separate and clearly denote untrusted content to limit its influence on user prompts.
  context: Separate and clearly denote untrusted content to limit its influence on user prompts.
  brief_digest: c3f2209a4e540d33c5d35cd910f5b82b155325f6c290ffe3962649bd019f07b4
  source_role: primary
  pass: deep
- id: F111
  part_id: D
  claim: OWASP recommends human-in-the-loop controls for privileged operations, which supports the brief's
    design where a developer, not the agent, applies and pushes the fix.
  source: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  fetched: '2026-10-18'
  quote: Implement human-in-the-loop controls for privileged operations to prevent unauthorized actions.
  context: Implement human-in-the-loop controls for privileged operations to prevent unauthorized actions.
  brief_digest: c3f2209a4e540d33c5d35cd910f5b82b155325f6c290ffe3962649bd019f07b4
  source_role: primary
  pass: deep
support:
- finding_id: F1
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f1
- finding_id: F2
  quote_check: pass
  verdict: supported
  worker_ref: support-f2
  finding_digest: f4749379e68d5f4e83e2b1ffac17e460b3cce6e802a1bdc8e5c78e60382c80e7
- finding_id: F3
  quote_check: fail
  verdict: missing
  worker_ref: support-f3
- finding_id: F4
  quote_check: pass
  verdict: supported
  worker_ref: support-f4
  finding_digest: e2a989e367b10824aae1b260153bae2d8935a8169f53f1ec0877397b1f6e1605
- finding_id: F5
  quote_check: pass
  verdict: supported
  worker_ref: support-f5
  finding_digest: 27554469f513d6fbd619ebfebdcd93e4bc1a24c3958896d52cd74e689e3b8b97
- finding_id: F6
  quote_check: pass
  verdict: supported
  worker_ref: support-f6
  finding_digest: 5be25b93e7d734786c1f5f70874bef7a9e160be178d61ab040e107a8a45e6014
- finding_id: F7
  quote_check: pass
  verdict: supported
  worker_ref: support-f7
  finding_digest: 38fe1a593c62da630dba634d814ed56c0dacec1a37958bf7c5a2097e277d8862
- finding_id: F8
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f8
- finding_id: F9
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f9
- finding_id: F10
  quote_check: pass
  verdict: supported
  worker_ref: support-f10
  finding_digest: 93ce8e76987ec4eedf11b5afba591c8b37e3583dcd070c9c86457c02b0eace12
- finding_id: F11
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f11
- finding_id: F12
  quote_check: fail
  verdict: missing
  worker_ref: support-f12
- finding_id: F13
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f13
- finding_id: F14
  quote_check: fail
  verdict: missing
  worker_ref: support-f14
- finding_id: F21
  quote_check: pass
  verdict: supported
  worker_ref: support-f21
- finding_id: F22
  quote_check: pass
  verdict: supported
  worker_ref: support-f22
- finding_id: F23
  quote_check: pass
  verdict: supported
  worker_ref: support-f23
  finding_digest: fd6151e3a7e37309e926eb6871e2f088fb9e7b4e12c3a02738b8bb567827d02a
- finding_id: F24
  quote_check: pass
  verdict: supported
  worker_ref: support-f24
  finding_digest: 247db496ca78526fc725d999635cb23b6b621b129bae5f4b9953bbe4a7e05d07
- finding_id: F25
  quote_check: pass
  verdict: supported
  worker_ref: support-f25
  finding_digest: 64a2b46ba484b35914928fb2007c3de22f449daa2ba0a1f8b1e4654d2929ae6b
- finding_id: F26
  quote_check: pass
  verdict: supported
  worker_ref: support-f26
  finding_digest: 2dfb12ebbbdf1a45388dacdb168dea3b702a6e25d81760a51c60a2858a66f2ba
- finding_id: F27
  quote_check: pass
  verdict: supported
  worker_ref: support-f27
  finding_digest: 6e05d06d70bead8820e1aa24e3e6021d2a3be697d39146aa880fbf017997f71d
- finding_id: F28
  quote_check: pass
  verdict: supported
  worker_ref: support-f28
  finding_digest: f66348b7a0a6e70a7e89fbc6f58b9ad50bf4c723267a9b0968fa8df27de99527
- finding_id: F29
  quote_check: pass
  verdict: supported
  worker_ref: support-f29
  finding_digest: a16ca777fc0c2ea82ff65d504c76cbae4941c5bd87a3935f8d7aa3a59001e1b5
- finding_id: F30
  quote_check: pass
  verdict: supported
  worker_ref: support-f30
  finding_digest: 05846c819ddfeccb7085a9aa3aaf00ca5ec26e400b85fb204ef0ab3fd4177dbe
- finding_id: F31
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f31
- finding_id: F32
  quote_check: pass
  verdict: supported
  worker_ref: support-f32
  finding_digest: 3e2e336534d4cf10b09dd942f5ccf18dc96e3e03c6c3c3384eb93c81ef35abca
- finding_id: F33
  quote_check: pass
  verdict: supported
  worker_ref: support-f33
  finding_digest: e7aae31d2fe454cecfb5764d82a6b834ab382bdca2185b744685e27eaf436512
- finding_id: F34
  quote_check: pass
  verdict: supported
  worker_ref: support-f34
  finding_digest: d1b2179749bd54518db8355fdaf4979151130dd62ffa12d40bd6b9a066f0cd30
- finding_id: F35
  quote_check: pass
  verdict: supported
  worker_ref: support-f35
  finding_digest: 4ba90cdd1e87e00060b5a60e57dc3673bc1479fe7b72bb2deab27cea28f7acea
- finding_id: F36
  quote_check: pass
  verdict: supported
  worker_ref: support-f36
  finding_digest: 6d3163e77ba684e079b2c0598439ff7c9bb3e522af3fafd04c4ff2b16024579d
- finding_id: F37
  quote_check: pass
  verdict: supported
  worker_ref: support-f37
  finding_digest: ff883cdc61ab4628795dcb9085f99ddc2d8a6b52faaaa47815f6af5943cc80cb
- finding_id: F38
  quote_check: pass
  verdict: supported
  worker_ref: support-f38
  finding_digest: 707cf229389c7f5bcb6294ec955e38e9951493d9dd3a7a9096b69fe9765de4e1
- finding_id: F39
  quote_check: pass
  verdict: supported
  worker_ref: support-f39
  finding_digest: 7c358d8b958b716599270535bcea595bac4e2fa2922f20afe5ffd1934233c54d
- finding_id: F40
  quote_check: pass
  verdict: supported
  worker_ref: support-f40
  finding_digest: d3a206f7324251a8ef7b064ce8e4ec56599819d255b124ae4dacaf700f7a825e
- finding_id: F41
  quote_check: pass
  verdict: supported
  worker_ref: support-f41
  finding_digest: 8215d00672e88b589d2e67c77e26e684e163f94dca7359023637ec3e84c46b7d
- finding_id: F42
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f42
- finding_id: F43
  quote_check: pass
  verdict: supported
  worker_ref: support-f43
  finding_digest: 5318383c227e9c52b1d2f1d9f6e1c0497d0c84a71ae2d6a017625e67f1d4b748
- finding_id: F44
  quote_check: pass
  verdict: supported
  worker_ref: support-f44
  finding_digest: 1dfb9a6334d2324ca6e99f696172cdc71ec6f4d85a0da7a9ef844730cab27eff
- finding_id: F45
  quote_check: fail
  verdict: missing
  worker_ref: support-f45
- finding_id: F46
  quote_check: pass
  verdict: supported
  worker_ref: support-f46
- finding_id: F47
  quote_check: fail
  verdict: missing
  worker_ref: support-f47
- finding_id: F48
  quote_check: pass
  verdict: supported
  worker_ref: support-f48
- finding_id: F49
  quote_check: pass
  verdict: supported
  worker_ref: support-f49
  finding_digest: 02d7b3912e928d4be9ccdb981fd7d3f1fc895deb9d3bb9d866ca546667e76581
- finding_id: F50
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f50
- finding_id: F51
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f51
- finding_id: F52
  quote_check: pass
  verdict: supported
  worker_ref: support-f52
  finding_digest: cfcc2539f4050a6165ad15224452b40494d68a235c1c977007adfb692d2076a6
- finding_id: F53
  quote_check: pass
  verdict: supported
  worker_ref: support-f53
  finding_digest: 83f8133562256f375b5f4b6098a5b7c0c677fb9c53e49a494b45e71e347f4cf0
- finding_id: F54
  quote_check: pass
  verdict: supported
  worker_ref: support-f54
  finding_digest: 9c107e579cb24c554671c6754ef502c9aa95adc6a748041d144cdc6991b35a95
- finding_id: F55
  quote_check: pass
  verdict: supported
  worker_ref: support-f55
  finding_digest: 97b8ef55eae24ef9db9c041089461e6cf40fe45d3650ef91d66ba05496cde0c0
- finding_id: F56
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f56
- finding_id: F57
  quote_check: pass
  verdict: supported
  worker_ref: support-f57
  finding_digest: 71901436a8235ef9c39b2981252f76f558533eb90da8ca02fac8ff4e8bc5f501
- finding_id: F58
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f58
- finding_id: F59
  quote_check: pass
  verdict: supported
  worker_ref: support-f59
  finding_digest: 0523ee6fef0db5663806e0bdeddf8fcba47fe0d5abeb56f4aefdb4817273791d
- finding_id: F60
  quote_check: pass
  verdict: supported
  worker_ref: support-f60
  finding_digest: 3cf95bdaf7a55733fc45886f3afd140286ed9b55f80c5c6d18c4efa8a44f32bb
- finding_id: F61
  quote_check: pass
  verdict: supported
  worker_ref: support-f61
- finding_id: F62
  quote_check: pass
  verdict: supported
  worker_ref: support-f62
  finding_digest: d24a7c4e06ccfe6e2be56a078c8efc69f13d5f7845986e21f8254dbe9416e3d6
- finding_id: F63
  quote_check: pass
  verdict: supported
  worker_ref: support-f63
  finding_digest: 2fcee2cecc24c9110afa0c1d250496f102663b4d189b28cf551bf7b387b1859c
- finding_id: F64
  quote_check: pass
  verdict: missing
  worker_ref: support-f64
- finding_id: F65
  quote_check: pass
  verdict: missing
  worker_ref: support-f65
- finding_id: F66
  quote_check: pass
  verdict: missing
  worker_ref: support-f66
- finding_id: F67
  quote_check: pass
  verdict: missing
  worker_ref: support-f67
- finding_id: F68
  quote_check: pass
  verdict: missing
  worker_ref: support-f68
- finding_id: F69
  quote_check: pass
  verdict: missing
  worker_ref: support-f69
- finding_id: F70
  quote_check: fail
  verdict: missing
  worker_ref: support-f70
- finding_id: F71
  quote_check: pass
  verdict: missing
  worker_ref: support-f71
- finding_id: F72
  quote_check: pass
  verdict: missing
  worker_ref: support-f72
- finding_id: F73
  quote_check: pass
  verdict: missing
  worker_ref: support-f73
- finding_id: F75
  quote_check: pass
  verdict: supported
  worker_ref: support-f75
- finding_id: F77
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f77
- finding_id: F79
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f79
- finding_id: F82
  quote_check: fail
  verdict: missing
  worker_ref: support-f82
- finding_id: F83
  quote_check: fail
  verdict: missing
  worker_ref: support-f83
- finding_id: F85
  quote_check: fail
  verdict: missing
  worker_ref: support-f85
- finding_id: F86
  quote_check: fail
  verdict: missing
  worker_ref: support-f86
- finding_id: F87
  quote_check: pass
  verdict: supported
  worker_ref: support-f87
  finding_digest: e49749bb1ea0524404eac024d569438774bdb3d86191923e8625fcc5caf4198a
- finding_id: F88
  quote_check: pass
  verdict: supported
  worker_ref: support-f88
  finding_digest: 942fb137faf5145a4e9f48c0016a9fbbe29eae6dc79ddfdb14f116aad434c6fc
- finding_id: F89
  quote_check: pass
  verdict: supported
  worker_ref: support-f89
  finding_digest: 133c68ff3626f82622285b0682b35fdc2d3ca1133742e1c306a0cb58aa327287
- finding_id: F90
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f90
- finding_id: F91
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f91
- finding_id: F92
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f92
- finding_id: F93
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f93
- finding_id: F94
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f94
- finding_id: F95
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f95
- finding_id: F96
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f96
- finding_id: F97
  quote_check: fail
  verdict: missing
  worker_ref: support-f97
- finding_id: F98
  quote_check: fail
  verdict: missing
  worker_ref: support-f98
- finding_id: F99
  quote_check: pass
  verdict: supported
  worker_ref: support-f99
  finding_digest: 6c77c8d77e304fa2592cda64039239c537defd5ac0635f9b7970be04acd561a8
- finding_id: F100
  quote_check: pass
  verdict: supported
  worker_ref: support-f100
  finding_digest: 9d6954151a01b0b534c091ed2b8912eb6b95f4125fb3808a008b061e49ba61ee
- finding_id: F101
  quote_check: pass
  verdict: supported
  worker_ref: support-f101
- finding_id: F102
  quote_check: pass
  verdict: supported
  worker_ref: support-f102
  finding_digest: 3473e3689adcc05f0057ad9fc802e18c75508c1ec24f639794be6b2932c3df1a
- finding_id: F103
  quote_check: pass
  verdict: supported
  worker_ref: support-f103
  finding_digest: f35dba8044e4bdb65825015a5ef0699afbeef5fa825b4a3dff0c7adf12436532
- finding_id: F104
  quote_check: pass
  verdict: supported
  worker_ref: support-f104
  finding_digest: a5635238a8728b3d9edd3ee471e655016e3334a45f71c1510679997e94980806
- finding_id: F105
  quote_check: fail
  verdict: missing
  worker_ref: support-f105
- finding_id: F106
  quote_check: pass
  verdict: supported
  worker_ref: support-f106
  finding_digest: 7a5f6cfe25c3bbeb0bcacb633803744ddf8daf164c91f751e95b42a85cf1f224
- finding_id: F107
  quote_check: pass
  verdict: supported
  worker_ref: support-f107
  finding_digest: 665e28384f15b927e182433931733bebb97d421caa92bf6478abbe8238c881e1
- finding_id: F108
  quote_check: pass
  verdict: supported
  worker_ref: support-f108
  finding_digest: beddff49830263263297c0738df3df44647392973ec8dd7e5c552b422b69d5c1
- finding_id: F109
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f109
- finding_id: F110
  quote_check: pass
  verdict: supported
  worker_ref: support-f110
  finding_digest: 859d70ea15ec514dd1ab3c0338c196949ff35148921411bf7dc2380e7563084f
- finding_id: F111
  quote_check: pass
  verdict: supported
  worker_ref: support-f111
  finding_digest: 9893299f40868901038f7dd1123cd95a900c4ec908b3698c7f353351b27a2842
drift: []
---
Findings grouped by pass and part are in the frontmatter; dropped findings are not kept.
