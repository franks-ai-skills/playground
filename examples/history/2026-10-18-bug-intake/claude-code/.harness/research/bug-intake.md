---
slug: bug-intake
search_mode: live
briefs:
- pass: survey
  part_id: null
  digest: c3693a9d7a8d954f8a997232ceccc3ebf88cb3951c08237716c6cf12ac8602ef
- pass: deep
  part_id: B
  digest: 7cfcb2e232d2ee9bfad04a01fa4ac168783446588af6b7be28abd1826c7ea555
- pass: deep
  part_id: C
  digest: 4d510095e2fc1707b4b1b9d3e46bf1c905b06649478cefca566feabedfdf3617
- pass: deep
  part_id: F
  digest: f79df32d27a379acf9e4b6893f84220433c56d96c205493c04b23f3bb6969306
findings:
- id: F1
  part_id: null
  claim: On GitHub, merging a linked pull request into the repository's default branch closes its linked
    issue automatically, so the 'close once merged' step can be done by linking the PR to the issue.
  source: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  fetched: '2026-10-18'
  quote: When you merge a linked pull request into the default branch of a repository, its linked issue
    is automatically closed.
  context: When you merge a linked pull request into the default branch of a repository, its linked issue
    is automatically closed.
  brief_digest: c3693a9d7a8d954f8a997232ceccc3ebf88cb3951c08237716c6cf12ac8602ef
  source_role: primary
  pass: survey
- id: F3
  part_id: null
  claim: GitHub issue forms let a team template define input types, validations, default assignees and
    default labels, which could enforce the team template the brief asks for.
  source: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
  fetched: '2026-10-18'
  quote: You can define different input types, validations, default assignees, and default labels for
    your issue forms.
  context: You can define different input types, validations, default assignees, and default labels for
    your issue forms.
  brief_digest: c3693a9d7a8d954f8a997232ceccc3ebf88cb3951c08237716c6cf12ac8602ef
  source_role: primary
  pass: survey
- id: F4
  part_id: null
  claim: A label that does not already exist in the repository is not added to issues by an issue form,
    so a skill that sets severity labels has to make sure those labels exist first.
  source: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
  fetched: '2026-10-18'
  quote: If a label does not already exist in the repository, it will not be automatically added to the
    issue.
  context: If a label does not already exist in the repository, it will not be automatically added to
    the issue.
  brief_digest: c3693a9d7a8d954f8a997232ceccc3ebf88cb3951c08237716c6cf12ac8602ef
  source_role: primary
  pass: survey
- id: F10
  part_id: null
  claim: Bug report content from external contributors can carry hidden instructions (prompt injection),
    and Anthropic recommends reviewing the raw content of external input before Claude processes it. This
    matters because the brief accepts reports from Discord, email and public issues.
  source: https://github.com/anthropics/claude-code-action/blob/main/docs/security.md
  fetched: '2026-10-18'
  quote: We recommend reviewing the raw content of all input coming from external contributors before
    allowing Claude to process it.
  context: External contributors may include hidden instructions through HTML comments, invisible characters,
    hidden attributes, or other techniques. The action sanitizes content by stripping HTML comments, invisible
    characters, markdown image alt text, hidden HTML attributes, and HTML entities, but new bypass techniques
    may emerge. We recommend reviewing the raw content of all input coming from external contributors
    before allowing Claude to process it.
  brief_digest: c3693a9d7a8d954f8a997232ceccc3ebf88cb3951c08237716c6cf12ac8602ef
  source_role: primary
  pass: survey
- id: F11
  part_id: null
  claim: Anthropic's claude-code-action security guidance says secret scrubbing and isolation reduce prompt
    injection risk but do not remove it, and advises keeping workflow permissions minimal and validating
    all outputs.
  source: https://github.com/anthropics/claude-code-action/blob/main/docs/security.md
  fetched: '2026-10-18'
  quote: This reduces but does not eliminate prompt injection risk — keep workflow permissions minimal
    and validate all outputs.
  context: When set, Claude does a best-effort scrub of Anthropic, cloud, and GitHub Actions secrets from
    subprocess environments. On Linux runners with bubblewrap available, subprocesses additionally run
    with PID-namespace isolation. This reduces but does not eliminate prompt injection risk — keep workflow
    permissions minimal and validate all outputs.
  brief_digest: c3693a9d7a8d954f8a997232ceccc3ebf88cb3951c08237716c6cf12ac8602ef
  source_role: primary
  pass: survey
- id: F12
  part_id: null
  claim: Mozilla's bug-writing guidelines call steps to reproduce the most important part of a bug report
    and tie a developer's ability to reproduce a bug to the bug being fixed.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: Steps to reproduce are the most important part of any bug report.
  context: How can a developer reproduce the bug on his or her own computer? Steps to reproduce are the
    most important part of any bug report. If a developer is able to reproduce the bug, the bug is very
    likely to be fixed.
  brief_digest: c3693a9d7a8d954f8a997232ceccc3ebf88cb3951c08237716c6cf12ac8602ef
  source_role: primary
  pass: survey
- id: F13
  part_id: null
  claim: Mozilla's guidelines ask reporters to say whether a bug reproduces at will, occasionally or not
    at all, which matches the brief's 'consistent or only sometimes' requirement.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: Indicate whether you can reproduce the bug at will, occasionally, or not at all.
  context: Indicate whether you can reproduce the bug at will, occasionally, or not at all.
  brief_digest: c3693a9d7a8d954f8a997232ceccc3ebf88cb3951c08237716c6cf12ac8602ef
  source_role: primary
  pass: survey
- id: F14
  part_id: null
  claim: Mozilla's guidelines tell reporters to check whether a bug has already been reported when filing
    it, which puts the duplicate check at intake.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: Enter a clear unique summary as described below; check if the bug has already been reported.
  context: Create a Bugzilla account if you don't have one already, select the product having the bug.
    Enter a clear unique summary as described below; check if the bug has already been reported. Provide
    precise steps to reproduce, expected results and actual results as described in the following section.
  brief_digest: c3693a9d7a8d954f8a997232ceccc3ebf88cb3951c08237716c6cf12ac8602ef
  source_role: primary
  pass: survey
- id: F16
  part_id: B
  claim: Mozilla's bug-writing guidelines call steps to reproduce the most important part of a bug report.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: Steps to reproduce are the most important part of any bug report.
  context: Steps to reproduce are the most important part of any bug report. If a developer is able to
    reproduce the bug, the bug is very likely to be fixed. If the steps are unclear, it might not even
    be possible to know whether the bug has been fixed.
  brief_digest: 7cfcb2e232d2ee9bfad04a01fa4ac168783446588af6b7be28abd1826c7ea555
  source_role: primary
  pass: deep
- id: F17
  part_id: B
  claim: Mozilla's guidelines say that if the steps are unclear, it may not even be possible to know whether
    the bug has been fixed.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: If the steps are unclear, it might not even be possible to know whether the bug has been fixed.
  context: Steps to reproduce are the most important part of any bug report. If a developer is able to
    reproduce the bug, the bug is very likely to be fixed. If the steps are unclear, it might not even
    be possible to know whether the bug has been fixed.
  brief_digest: 7cfcb2e232d2ee9bfad04a01fa4ac168783446588af6b7be28abd1826c7ea555
  source_role: primary
  pass: deep
- id: F19
  part_id: B
  claim: Mozilla's guidelines ask that, after the steps, the report precisely describes the observed (actual)
    result and the expected result.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: After your steps, precisely describe the observed (actual) result and the expected result.
  context: After your steps, precisely describe the observed (actual) result and the expected result.
    Clearly separate facts (observations) from speculations.
  brief_digest: 7cfcb2e232d2ee9bfad04a01fa4ac168783446588af6b7be28abd1826c7ea555
  source_role: primary
  pass: deep
- id: F20
  part_id: B
  claim: Mozilla's guidelines ask reporters to keep facts (observations) clearly separate from speculation.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-18'
  quote: Clearly separate facts (observations) from speculations.
  context: After your steps, precisely describe the observed (actual) result and the expected result.
    Clearly separate facts (observations) from speculations.
  brief_digest: 7cfcb2e232d2ee9bfad04a01fa4ac168783446588af6b7be28abd1826c7ea555
  source_role: primary
  pass: deep
- id: F21
  part_id: B
  claim: In Mozilla's test verification, a modified mochitest is run 10 times, then another 5 times, each
    time in a new browser instance.
  source: https://firefox-source-docs.mozilla.org/testing/test-verification/index.html
  fetched: '2026-10-18'
  quote: That test will be run 10 times, then the same test will be run another 5 times, each time in
    a new browser instance.
  context: For instance, when a mochitest is modified, TV runs the mochitest harness in a verify mode
    on the modified mochitest. That test will be run 10 times, then the same test will be run another
    5 times, each time in a new browser instance. Once this is done, the whole sequence will be repeated
    in the test chaos mode (setting MOZ_CHAOSMODE).
  brief_digest: 7cfcb2e232d2ee9bfad04a01fa4ac168783446588af6b7be28abd1826c7ea555
  source_role: primary
  pass: deep
- id: F22
  part_id: B
  claim: Mozilla's test verification then repeats the whole run sequence in chaos mode (MOZ_CHAOSMODE).
  source: https://firefox-source-docs.mozilla.org/testing/test-verification/index.html
  fetched: '2026-10-18'
  quote: Once this is done, the whole sequence will be repeated in the test chaos mode (setting MOZ_CHAOSMODE).
  context: That test will be run 10 times, then the same test will be run another 5 times, each time in
    a new browser instance. Once this is done, the whole sequence will be repeated in the test chaos mode
    (setting MOZ_CHAOSMODE). If any test run fails then the failure is reported normally, testing ends,
    and the test suite reports the failure.
  brief_digest: 7cfcb2e232d2ee9bfad04a01fa4ac168783446588af6b7be28abd1826c7ea555
  source_role: primary
  pass: deep
- id: F23
  part_id: B
  claim: In Mozilla's test verification, a failure in any single run is reported and ends testing.
  source: https://firefox-source-docs.mozilla.org/testing/test-verification/index.html
  fetched: '2026-10-18'
  quote: If any test run fails then the failure is reported normally, testing ends, and the test suite
    reports the failure.
  context: Once this is done, the whole sequence will be repeated in the test chaos mode (setting MOZ_CHAOSMODE).
    If any test run fails then the failure is reported normally, testing ends, and the test suite reports
    the failure.
  brief_digest: 7cfcb2e232d2ee9bfad04a01fa4ac168783446588af6b7be28abd1826c7ea555
  source_role: primary
  pass: deep
- id: F24
  part_id: B
  claim: Mozilla's guide to debugging intermittents says the first step to fixing an intermittent failure
    is to reproduce it.
  source: https://firefox-source-docs.mozilla.org/testing/debugging-intermittents/index.html
  fetched: '2026-10-18'
  quote: The first step to fix an intermittent is to reproduce it.
  context: The first step to fix an intermittent is to reproduce it.
  brief_digest: 7cfcb2e232d2ee9bfad04a01fa4ac168783446588af6b7be28abd1826c7ea555
  source_role: primary
  pass: deep
- id: F25
  part_id: B
  claim: Mozilla notes that some tests fail only when run together with one or more other tests.
  source: https://firefox-source-docs.mozilla.org/testing/debugging-intermittents/index.html
  fetched: '2026-10-18'
  quote: Sometimes, though, a test will only fail if it is run in conjunction with one or more other tests.
  context: Sometimes, though, a test will only fail if it is run in conjunction with one or more other
    tests.
  brief_digest: 7cfcb2e232d2ee9bfad04a01fa4ac168783446588af6b7be28abd1826c7ea555
  source_role: primary
  pass: deep
- id: F27
  part_id: B
  claim: Mozilla says the number of times to retrigger a job when checking an intermittent depends on
    how often the failure occurs.
  source: https://firefox-source-docs.mozilla.org/testing/debugging-intermittents/index.html
  fetched: '2026-10-18'
  quote: Exactly how many times you should retrigger depends on the frequency of the failure.
  context: Exactly how many times you should retrigger depends on the frequency of the failure.
  brief_digest: 7cfcb2e232d2ee9bfad04a01fa4ac168783446588af6b7be28abd1826c7ea555
  source_role: primary
  pass: deep
- id: F29
  part_id: B
  claim: In Gruber et al.'s Python dataset, order dependency caused 59% of the 7571 flaky tests.
  source: https://arxiv.org/abs/2101.09077
  fetched: '2026-10-18'
  quote: Order dependency is a much more dominant problem in Python, causing 59% of the 7571 flaky tests
    in our dataset.
  context: Order dependency is a much more dominant problem in Python, causing 59% of the 7571 flaky tests
    in our dataset.
  brief_digest: 7cfcb2e232d2ee9bfad04a01fa4ac168783446588af6b7be28abd1826c7ea555
  source_role: primary
  pass: deep
- id: F30
  part_id: C
  claim: GitHub only reads closing keywords in a pull request description when the pull request targets
    the repository's default branch. On any other target branch the keywords are ignored, no link is created,
    and merging has no effect on the issue.
  source: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  fetched: '2026-10-18'
  quote: If the pull request targets any other branch, then these keywords are ignored, no links are created,
    and merging the PR has no effect on the issues.
  context: The special keywords in a pull request description are interpreted only when the pull request
    targets the repository's default branch. If the pull request targets any other branch, then these
    keywords are ignored, no links are created, and merging the PR has no effect on the issues.
  brief_digest: 4d510095e2fc1707b4b1b9d3e46bf1c905b06649478cefca566feabedfdf3617
  source_role: primary
  pass: deep
- id: F31
  part_id: C
  claim: When a linked pull request is merged into the default branch, GitHub closes the linked issue
    automatically.
  source: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  fetched: '2026-10-18'
  quote: When you merge a linked pull request into the default branch of a repository, its linked issue
    is automatically closed.
  context: When you merge a linked pull request into the default branch of a repository, its linked issue
    is automatically closed. For more information about the default branch, see Changing the default branch.
  brief_digest: 4d510095e2fc1707b4b1b9d3e46bf1c905b06649478cefca566feabedfdf3617
  source_role: primary
  pass: deep
- id: F33
  part_id: C
  claim: Once required status checks are enabled on a protected branch, every required check must pass
    before collaborators can merge changes into it.
  source: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
  fetched: '2026-10-18'
  quote: After enabling required status checks, all required status checks must pass before collaborators
    can merge changes into the protected branch.
  context: After enabling required status checks, all required status checks must pass before collaborators
    can merge changes into the protected branch. After all required status checks pass, any commits must
    either be pushed to another branch and then merged or pushed directly to the protected branch.
  brief_digest: 4d510095e2fc1707b4b1b9d3e46bf1c905b06649478cefca566feabedfdf3617
  source_role: primary
  pass: deep
- id: F35
  part_id: C
  claim: Google's code review guidance says a change that adds or changes logic should come with new or
    updated tests for the new behavior. For a bug fix, that means adding a test that covers the fixed
    behavior.
  source: https://google.github.io/eng-practices/review/developer/small-cls.html
  fetched: '2026-10-18'
  quote: A CL that adds or changes logic should be accompanied by new or updated tests for the new behavior.
  context: Tests are expected for all Google changes. A CL that adds or changes logic should be accompanied
    by new or updated tests for the new behavior.
  brief_digest: 4d510095e2fc1707b4b1b9d3e46bf1c905b06649478cefca566feabedfdf3617
  source_role: primary
  pass: deep
- id: F37
  part_id: C
  claim: GitHub Security Lab warns that combining the pull_request_target trigger with an explicit checkout
    of an untrusted PR is dangerous and may lead to repository compromise. This matters when the agent
    edits CI workflows to fix failing checks.
  source: https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/
  fetched: '2026-10-18'
  quote: Combining pull_request_target workflow trigger with an explicit checkout of an untrusted PR is
    a dangerous practice that may lead to repository compromise.
  context: Combining pull_request_target workflow trigger with an explicit checkout of an untrusted PR
    is a dangerous practice that may lead to repository compromise.
  brief_digest: 4d510095e2fc1707b4b1b9d3e46bf1c905b06649478cefca566feabedfdf3617
  source_role: primary
  pass: deep
- id: F38
  part_id: C
  claim: GitHub Security Lab advises treating PRs from external forks as untrusted input in any automated
    processing.
  source: https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/
  fetched: '2026-10-18'
  quote: Any automated processing of PRs from an external fork is potentially dangerous and such PRs should
    be treated like untrusted input.
  context: Any automated processing of PRs from an external fork is potentially dangerous and such PRs
    should be treated like untrusted input.
  brief_digest: 4d510095e2fc1707b4b1b9d3e46bf1c905b06649478cefca566feabedfdf3617
  source_role: primary
  pass: deep
- id: F39
  part_id: F
  claim: GitHub automatically closes an issue when a pull request linked to it is merged into the repository's
    default branch.
  source: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  fetched: '2026-10-18'
  quote: When you merge a linked pull request into the default branch of a repository, its linked issue
    is automatically closed.
  context: When you merge a linked pull request into the default branch of a repository, its linked issue
    is automatically closed. For more information about the default branch, see Changing the default branch.
  brief_digest: f79df32d27a379acf9e4b6893f84220433c56d96c205493c04b23f3bb6969306
  source_role: primary
  pass: deep
- id: F42
  part_id: F
  claim: A keyword-created link between a PR and an issue can only be removed by editing the PR description
    to remove the keyword.
  source: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
  fetched: '2026-10-18'
  quote: To unlink an issue that you linked using a keyword, you must edit the pull request description
    to remove the keyword.
  context: To unlink an issue that you linked using a keyword, you must edit the pull request description
    to remove the keyword.
  brief_digest: f79df32d27a379acf9e4b6893f84220433c56d96c205493c04b23f3bb6969306
  source_role: primary
  pass: deep
support:
- finding_id: F1
  quote_check: pass
  verdict: supported
  worker_ref: support-f1
  finding_digest: 5b981af9113518032bebc0e907a1fc2bea9f282fe34d10df93471dd5f830afca
- finding_id: F2
  quote_check: fail
  verdict: missing
  worker_ref: support-f2
- finding_id: F3
  quote_check: pass
  verdict: supported
  worker_ref: support-f3
  finding_digest: 074309979ae52b4cd158bf964aee9bdf0b48f32010fbd312c71a84633df764f5
- finding_id: F4
  quote_check: pass
  verdict: supported
  worker_ref: support-f4
  finding_digest: eb4a8527c4093a3cae99a7704299403acd4310ba7acacafe7106f5d832ef15aa
- finding_id: F5
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f5
- finding_id: F6
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f6
- finding_id: F7
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f7
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
  finding_digest: dc5f80dee8763b66654513947e46bcbc4e9171baa60bd2b2924e57da1f9fb9d7
- finding_id: F11
  quote_check: pass
  verdict: supported
  worker_ref: support-f11
  finding_digest: d42804f8c2c3db1b987b6ac3f0cacdb17ba2cc71472cbbfe1047dfaac0188ab4
- finding_id: F12
  quote_check: pass
  verdict: supported
  worker_ref: support-f12
  finding_digest: 7a8bcaa9b9200909b6b9dff0c5051df07933e330544cd6b052c3df353fc18960
- finding_id: F13
  quote_check: pass
  verdict: supported
  worker_ref: support-f13
  finding_digest: 9c091eefa8d4db903139ee7c8f06b8cc46e66a7ceadda1d43a1cd63678f8825a
- finding_id: F14
  quote_check: pass
  verdict: supported
  worker_ref: support-f14
  finding_digest: c23a9ce9dd28b04d1c256f2204bcd6c50ded8d5e9be47269d41dfb3f210edd5b
- finding_id: F15
  quote_check: fail
  verdict: missing
  worker_ref: support-f15
- finding_id: F16
  quote_check: pass
  verdict: supported
  worker_ref: support-f16
  finding_digest: 17f49e06edcedf8f0e661a684144c9b9e4cb49fe2e700df7f25ce79c01c0892f
- finding_id: F17
  quote_check: pass
  verdict: supported
  worker_ref: support-f17
  finding_digest: 175ead8028ef068b1db824441a334f391d2426bbd9037b69327687d90a188d56
- finding_id: F18
  quote_check: pass
  verdict: supported
  worker_ref: support-f18
- finding_id: F19
  quote_check: pass
  verdict: supported
  worker_ref: support-f19
  finding_digest: d803fe0dab6891986799831a06f9d69273fa63a75cb3800864a2507340d7fcf6
- finding_id: F20
  quote_check: pass
  verdict: supported
  worker_ref: support-f20
  finding_digest: 79e31f83ced3566caf59ecd6edf182a80d74ca644b7ba0b05b6d5511370e21b3
- finding_id: F21
  quote_check: pass
  verdict: supported
  worker_ref: support-f21
  finding_digest: 0b139eb9a82132c32345d5cf0f5348a79fbe8757bba2a0986796715caf825592
- finding_id: F22
  quote_check: pass
  verdict: supported
  worker_ref: support-f22
  finding_digest: 115419c20da8de94b52290e9c503c7ebdcdedf433d7f887166e488e532c6170f
- finding_id: F23
  quote_check: pass
  verdict: supported
  worker_ref: support-f23
  finding_digest: 49bb34d06d470c036a0faf7ca6f60150b6cee671ab123c57834db7bd39b559cc
- finding_id: F24
  quote_check: pass
  verdict: supported
  worker_ref: support-f24
  finding_digest: 8f10a83c0a97e538fdf54daa494b59ae89475b970a1fbdb73b76a7280b0eb272
- finding_id: F25
  quote_check: pass
  verdict: supported
  worker_ref: support-f25
  finding_digest: 00eeb134c6776c88b014a61f61355092367ef707327b681436170d638a582a93
- finding_id: F26
  quote_check: fail
  verdict: missing
  worker_ref: support-f26
- finding_id: F27
  quote_check: pass
  verdict: supported
  worker_ref: support-f27
  finding_digest: 675f24c2cefd8199d31e8e8296198bc6c00ee8ddeb504994d50cd3ca03459b34
- finding_id: F28
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f28
- finding_id: F29
  quote_check: pass
  verdict: supported
  worker_ref: support-f29
  finding_digest: b5b9200549b4c92a8cc1ddc9e9298cbe59781fc5d88d3bb3997c18997e501f04
- finding_id: F30
  quote_check: pass
  verdict: supported
  worker_ref: support-f30
  finding_digest: 4f4a80ef0c0dd1ed0837a56a6905c5872ce22cd8adb00e90eeb3f9247fc8e918
- finding_id: F31
  quote_check: pass
  verdict: supported
  worker_ref: support-f31
  finding_digest: 9578e2cac41ebeb6f04c66071fea235e2bbb7a8b136dbbc5276fb22ad02306b1
- finding_id: F32
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f32
- finding_id: F33
  quote_check: pass
  verdict: supported
  worker_ref: support-f33
  finding_digest: 02c217244200d600f7e7a1c35bee16bd833f71614e455b0e5c867e77492e265c
- finding_id: F34
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f34
- finding_id: F35
  quote_check: pass
  verdict: supported
  worker_ref: support-f35
  finding_digest: 24dd99250f8a68fc8c0dc4eb1ccd27218fd4f29c57b0345fc13c8c0022211951
- finding_id: F36
  quote_check: fail
  verdict: missing
  worker_ref: support-f36
- finding_id: F37
  quote_check: pass
  verdict: supported
  worker_ref: support-f37
  finding_digest: 76f9b8104f0a7a54f20776fa3a7259248472b4623d4c111bdff062705f49cd66
- finding_id: F38
  quote_check: pass
  verdict: supported
  worker_ref: support-f38
  finding_digest: 61046c93bfdd2e0cce32d4e474ed4b0c7672e54246dbd71107de2db4dd0dae59
- finding_id: F39
  quote_check: pass
  verdict: supported
  worker_ref: support-f39
  finding_digest: a5f6bf4f6f3a2de496692db8fa2df76c64a1df1f518d0e31aee7c82dd6a86292
- finding_id: F40
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f40
- finding_id: F41
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f41
- finding_id: F42
  quote_check: pass
  verdict: supported
  worker_ref: support-f42
  finding_digest: 35c58ec70cb3b967955fab8ff02addb19de5134bd89c884c4fd77b05cdeefb82
- finding_id: F43
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f43
- finding_id: F44
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f44
- finding_id: F45
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f45
- finding_id: F46
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f46
- finding_id: F47
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f47
- finding_id: F48
  quote_check: fail
  verdict: missing
  worker_ref: support-f48
- finding_id: F49
  quote_check: fail
  verdict: missing
  worker_ref: support-f49
- finding_id: F50
  quote_check: fail
  verdict: missing
  worker_ref: support-f50
drift: []
---
Findings grouped by pass and part are in the frontmatter; dropped findings are not kept.
