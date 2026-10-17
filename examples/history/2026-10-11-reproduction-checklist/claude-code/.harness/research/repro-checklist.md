---
slug: repro-checklist
search_mode: live
briefs:
- pass: survey
  part_id: null
  digest: f7b439628cf9cfd9cebf2b9ee2469308baffa124b4dfd2491851da1a245afbb4
- pass: deep
  part_id: A
  digest: 2fc89daff3ceadd6899aaa217b939eb5d0fac3c2256814e52a88c6ccdab10bb9
findings:
- id: F2
  part_id: null
  claim: 'The awesome-copilot bug-reproduction-brief skill tells the agent to record only environment
    facts it can inspect: repository and commit, runtime and package-manager versions, OS or container,
    lockfile, feature flags, and the target environment.'
  source: https://raw.githubusercontent.com/github/awesome-copilot/main/skills/bug-reproduction-brief/SKILL.md
  fetched: '2026-10-11'
  quote: 'Record only facts you can inspect:'
  context: '## 2. Identify the environment


    Record only facts you can inspect:


    - repository and commit;

    - runtime and package-manager versions;

    - operating system or container;

    - dependency lockfile;

    - relevant feature flags;

    - whether the target is local, test, staging, or production.


    Never guess credentials or production configuration.'
  brief_digest: f7b439628cf9cfd9cebf2b9ee2469308baffa124b4dfd2491851da1a245afbb4
  source_role: primary
  pass: survey
- id: F3
  part_id: null
  claim: The bug-reproduction-brief skill requires separate, observable Expected and Actual statements,
    and neither statement may contain the suspected cause.
  source: https://raw.githubusercontent.com/github/awesome-copilot/main/skills/bug-reproduction-brief/SKILL.md
  fetched: '2026-10-11'
  quote: Do not put the suspected cause in either statement.
  context: 'Expected: [observable result]

    Actual:   [observable result, including status or error]

    ```


    Do not put the suspected cause in either statement.'
  brief_digest: f7b439628cf9cfd9cebf2b9ee2469308baffa124b4dfd2491851da1a245afbb4
  source_role: primary
  pass: survey
- id: F4
  part_id: null
  claim: The bug-reproduction-brief skill requires running the minimal reproduction at least twice where
    it is safe to do so. For an intermittent failure, it requires reporting the observed frequency rather
    than calling the failure deterministic.
  source: https://raw.githubusercontent.com/github/awesome-copilot/main/skills/bug-reproduction-brief/SKILL.md
  fetched: '2026-10-11'
  quote: Run the minimal reproduction at least twice where safe.
  context: '## 5. Prove repeatability


    Run the minimal reproduction at least twice where safe. Record commands and outputs. If the failure
    is intermittent, report the observed frequency and duration instead of calling it deterministic.'
  brief_digest: f7b439628cf9cfd9cebf2b9ee2469308baffa124b4dfd2491851da1a245afbb4
  source_role: primary
  pass: survey
- id: F5
  part_id: null
  claim: The bug-reproduction-brief skill makes the verified reproduction its deliverable and forbids
    editing implementation code while the brief is being built.
  source: https://raw.githubusercontent.com/github/awesome-copilot/main/skills/bug-reproduction-brief/SKILL.md
  fetched: '2026-10-11'
  quote: A verified reproduction is the deliverable.
  context: '## 6. Stop before repair


    A verified reproduction is the deliverable. Do not edit implementation code while building the brief
    because that can destroy the evidence or mix diagnosis with remediation.'
  brief_digest: f7b439628cf9cfd9cebf2b9ee2469308baffa124b4dfd2491851da1a245afbb4
  source_role: primary
  pass: survey
- id: F9
  part_id: null
  claim: The 'reproduce' skill in antoniowolkk/junior-agent holds that a defect that cannot be reproduced
    cannot be proven fixed.
  source: https://raw.githubusercontent.com/antoniowolkk/junior-agent/main/skills/reproduce/SKILL.md
  fetched: '2026-10-11'
  quote: A defect you cannot reproduce is a defect you cannot prove you fixed.
  context: A defect you cannot reproduce is a defect you cannot prove you fixed.
  brief_digest: f7b439628cf9cfd9cebf2b9ee2469308baffa124b4dfd2491851da1a245afbb4
  source_role: primary
  pass: survey
- id: F17
  part_id: null
  claim: 'In Claude Code, the location where a skill is saved determines its reach: the home directory
    for every project, a committed repository for everyone who works there, or a plugin to reach a whole
    team.'
  source: https://code.claude.com/docs/en/skills
  fetched: '2026-10-11'
  quote: Save it under your home directory to get it in every project, commit it to a repository to share
    it with everyone who works there, or distribute it through a plugin or managed settings to reach a
    whole team.
  context: Where you save a skill decides which sessions load it. Save it under your home directory to
    get it in every project, commit it to a repository to share it with everyone who works there, or distribute
    it through a plugin or managed settings to reach a whole team.
  brief_digest: f7b439628cf9cfd9cebf2b9ee2469308baffa124b4dfd2491851da1a245afbb4
  source_role: primary
  pass: survey
- id: F19
  part_id: null
  claim: The GitHub CLI command 'gh issue comment' adds a comment to an issue. It is one way an agent
    could add a reproduction checklist to an issue.
  source: https://cli.github.com/manual/gh_issue_comment
  fetched: '2026-10-11'
  quote: Add a comment to a GitHub issue.
  context: Add a comment to a GitHub issue.
  brief_digest: f7b439628cf9cfd9cebf2b9ee2469308baffa124b4dfd2491851da1a245afbb4
  source_role: primary
  pass: survey
- id: F20
  part_id: A
  claim: Mozilla's bug-writing guidelines treat steps to reproduce as the most important part of a bug
    report.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-11'
  quote: Steps to reproduce are the most important part of any bug report.
  context: Steps to reproduce are the most important part of any bug report. If a developer is able to
    reproduce the bug, the bug is very likely to be fixed.
  brief_digest: 2fc89daff3ceadd6899aaa217b939eb5d0fac3c2256814e52a88c6ccdab10bb9
  source_role: primary
  pass: deep
- id: F21
  part_id: A
  claim: Mozilla's guidelines ask the reporter to say whether the bug reproduces at will, occasionally,
    or not at all. This supports a rule that the checklist reports how often the bug reproduces.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-11'
  quote: Indicate whether you can reproduce the bug at will, occasionally, or not at all.
  context: Indicate whether you can reproduce the bug at will, occasionally, or not at all.
  brief_digest: 2fc89daff3ceadd6899aaa217b939eb5d0fac3c2256814e52a88c6ccdab10bb9
  source_role: primary
  pass: deep
- id: F22
  part_id: A
  claim: Mozilla's guidelines ask for the observed (actual) result and the expected result to be described
    precisely after the steps.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-11'
  quote: After your steps, precisely describe the observed (actual) result and the expected result.
  context: After your steps, precisely describe the observed (actual) result and the expected result.
    Clearly separate facts (observations) from speculations.
  brief_digest: 2fc89daff3ceadd6899aaa217b939eb5d0fac3c2256814e52a88c6ccdab10bb9
  source_role: primary
  pass: deep
- id: F23
  part_id: A
  claim: Mozilla's guidelines tell reporters to keep facts (observations) clearly separate from speculation.
    This supports keeping the suspected cause out of the Expected and Actual fields.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-11'
  quote: Clearly separate facts (observations) from speculations.
  context: After your steps, precisely describe the observed (actual) result and the expected result.
    Clearly separate facts (observations) from speculations.
  brief_digest: 2fc89daff3ceadd6899aaa217b939eb5d0fac3c2256814e52a88c6ccdab10bb9
  source_role: primary
  pass: deep
- id: F25
  part_id: A
  claim: Tatham writes that a reporter's own diagnosis is optional and does not replace stating the symptoms.
  source: https://www.chiark.greenend.org.uk/~sgtatham/bugs.html
  fetched: '2026-10-11'
  quote: The diagnosis is an optional extra, and not an alternative to giving the symptoms.
  context: Providing your own diagnosis might be helpful sometimes, but always state the symptoms. The
    diagnosis is an optional extra, and not an alternative to giving the symptoms.
  brief_digest: 2fc89daff3ceadd6899aaa217b939eb5d0fac3c2256814e52a88c6ccdab10bb9
  source_role: practitioner
  pass: deep
- id: F26
  part_id: A
  claim: Tatham advises stating exactly what you expected to see, not only what went wrong.
  source: https://www.chiark.greenend.org.uk/~sgtatham/bugs.html
  fetched: '2026-10-11'
  quote: Tell them why you think what you saw is wrong; better still, tell them exactly what you expected
    to see.
  context: Tell them why you think what you saw is wrong; better still, tell them exactly what you expected
    to see.
  brief_digest: 2fc89daff3ceadd6899aaa217b939eb5d0fac3c2256814e52a88c6ccdab10bb9
  source_role: practitioner
  pass: deep
- id: F33
  part_id: A
  claim: OpenAI's skill guidance recommends imperative steps with explicit inputs and outputs, and instructions
    over scripts unless deterministic behavior or external tooling is needed.
  source: https://learn.chatgpt.com/docs/build-skills
  fetched: '2026-10-11'
  quote: Write imperative steps with explicit inputs and outputs.
  context: Prefer instructions over scripts unless you need deterministic behavior or external tooling.
    Write imperative steps with explicit inputs and outputs.
  brief_digest: 2fc89daff3ceadd6899aaa217b939eb5d0fac3c2256814e52a88c6ccdab10bb9
  source_role: primary
  pass: deep
- id: F35
  part_id: A
  claim: OWASP recommends separating and clearly marking untrusted content to limit its influence. This
    supports treating the issue text as data, not instructions.
  source: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  fetched: '2026-10-11'
  quote: Separate and clearly denote untrusted content to limit its influence on user prompts.
  context: Separate and clearly denote untrusted content to limit its influence on user prompts.
  brief_digest: 2fc89daff3ceadd6899aaa217b939eb5d0fac3c2256814e52a88c6ccdab10bb9
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
- finding_id: F3
  quote_check: pass
  verdict: supported
  worker_ref: support-f3
- finding_id: F4
  quote_check: pass
  verdict: supported
  worker_ref: support-f4
- finding_id: F5
  quote_check: pass
  verdict: supported
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
  verdict: supported
  worker_ref: support-f9
- finding_id: F10
  quote_check: fail
  verdict: missing
  worker_ref: support-f10
- finding_id: F11
  quote_check: pass
  verdict: supported
  worker_ref: support-f11
- finding_id: F12
  quote_check: fail
  verdict: missing
  worker_ref: support-f12
- finding_id: F13
  quote_check: fail
  verdict: missing
  worker_ref: support-f13
- finding_id: F14
  quote_check: fail
  verdict: missing
  worker_ref: support-f14
- finding_id: F15
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f15
- finding_id: F16
  quote_check: fail
  verdict: missing
  worker_ref: support-f16
- finding_id: F17
  quote_check: pass
  verdict: supported
  worker_ref: support-f17
- finding_id: F18
  quote_check: fail
  verdict: missing
  worker_ref: support-f18
- finding_id: F19
  quote_check: pass
  verdict: supported
  worker_ref: support-f19
- finding_id: F20
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f20
- finding_id: F21
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f21
- finding_id: F22
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f22
- finding_id: F20
  quote_check: pass
  verdict: supported
  worker_ref: support-f20
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
- finding_id: F24
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f24
- finding_id: F25
  quote_check: pass
  verdict: supported
  worker_ref: support-f25
- finding_id: F26
  quote_check: pass
  verdict: supported
  worker_ref: support-f26
- finding_id: F27
  quote_check: fail
  verdict: missing
  worker_ref: support-f27
- finding_id: F28
  quote_check: fail
  verdict: missing
  worker_ref: support-f28
- finding_id: F29
  quote_check: fail
  verdict: missing
  worker_ref: support-f29
- finding_id: F30
  quote_check: fail
  verdict: missing
  worker_ref: support-f30
- finding_id: F31
  quote_check: fail
  verdict: missing
  worker_ref: support-f31
- finding_id: F32
  quote_check: fail
  verdict: missing
  worker_ref: support-f32
- finding_id: F33
  quote_check: pass
  verdict: supported
  worker_ref: support-f33
- finding_id: F34
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f34
- finding_id: F35
  quote_check: pass
  verdict: supported
  worker_ref: support-f35
- finding_id: F36
  quote_check: fail
  verdict: missing
  worker_ref: support-f36
- finding_id: F37
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f37
drift: []
---
Findings grouped by pass and part are in the frontmatter; dropped findings are not kept.
