---
slug: bug-reproduction-checklist
search_mode: live
briefs:
- pass: survey
  part_id: null
  digest: 031c336224aeb220ab7e8b5c68fa15b513e5cab05c214fce71835e4756216830
- pass: deep
  part_id: A
  digest: 30df48750d09c11eca55bf76716ef3cd41424897f4cabdd8bc14b289150f254d
findings:
- id: F2
  part_id: null
  claim: Mozilla's bug-writing guidance calls for describing actual and expected results after reproduction
    steps and separating observations from speculation.
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-11'
  quote: After your steps, precisely describe the observed (actual) result and the expected result.
  context: After your steps, precisely describe the observed (actual) result and the expected result.
    Clearly separate facts (observations) from speculations.
  brief_digest: 031c336224aeb220ab7e8b5c68fa15b513e5cab05c214fce71835e4756216830
  source_role: primary
  pass: survey
- id: F3
  part_id: null
  claim: Playwright Trace Viewer loads traces within the browser without transmitting their data externally.
  source: https://playwright.dev/docs/trace-viewer
  fetched: '2026-10-11'
  quote: Trace Viewer loads the trace entirely in your browser and does not transmit any data externally.
  context: Trace Viewer loads the trace entirely in your browser and does not transmit any data externally.
  brief_digest: 031c336224aeb220ab7e8b5c68fa15b513e5cab05c214fce71835e4756216830
  source_role: primary
  pass: survey
- id: F4
  part_id: null
  claim: MDN recommends first creating a minimal test case that reproduces the bug when identifying the
    problem's source.
  source: https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Web_mechanics/File_browser_bugs
  fetched: '2026-10-11'
  quote: The first step in identifying the source of the problem is to create a minimal test case that
    reproduces the bug.
  context: The first step in identifying the source of the problem is to create a minimal test case that
    reproduces the bug.
  brief_digest: 031c336224aeb220ab7e8b5c68fa15b513e5cab05c214fce71835e4756216830
  source_role: primary
  pass: survey
- id: F5
  part_id: A
  claim: 'Proposed rule idea.bug-reproduction-checklist.A.results (check: judged): After the reproduction
    steps, precisely describe the observed and expected results and separate observations from speculation.'
  source: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  fetched: '2026-10-11'
  quote: After your steps, precisely describe the observed (actual) result and the expected result.
  context: After your steps, precisely describe the observed (actual) result and the expected result.
    Clearly separate facts (observations) from speculations.
  brief_digest: 30df48750d09c11eca55bf76716ef3cd41424897f4cabdd8bc14b289150f254d
  source_role: primary
  pass: deep
- id: F6
  part_id: A
  claim: The networking bug guidance warns that logs may contain personal information, including cookies,
    and suggests capturing logs with a fresh Firefox profile.
  source: https://firefox-source-docs.mozilla.org/networking/submitting_networking_bugs.html
  fetched: '2026-10-11'
  quote: Logs may include personal information such as cookies.
  context: Logs may include personal information such as cookies. Try using a fresh Firefox profile to
    capture the logs.
  brief_digest: 30df48750d09c11eca55bf76716ef3cd41424897f4cabdd8bc14b289150f254d
  source_role: primary
  pass: deep
- id: F7
  part_id: A
  claim: A process can overwrite an SQLite database file, and the SQLite library cannot defend against
    that overwrite.
  source: https://www.sqlite.org/howtocorrupt.html
  fetched: '2026-10-11'
  quote: That means that any process can open the file and overwrite it with garbage.
  context: SQLite database files are ordinary disk files. That means that any process can open the file
    and overwrite it with garbage. There is nothing that the SQLite library can do to defend against this.
  brief_digest: 30df48750d09c11eca55bf76716ef3cd41424897f4cabdd8bc14b289150f254d
  source_role: primary
  pass: deep
support:
- finding_id: F1
  quote_check: pass
  verdict: supported
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
  verdict: supported
  worker_ref: support-f6
- finding_id: F7
  quote_check: pass
  verdict: supported
  worker_ref: support-f7
drift: []
---
Findings grouped by pass and part are in the frontmatter; dropped findings are not kept.
