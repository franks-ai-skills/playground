---
slug: local-ui-testing
search_mode: live
briefs:
- pass: survey
  part_id: null
  digest: 1420be8e65da7160060ffa1f048e2292d0158d681859ee33aca743ee8667fb58
- pass: deep
  part_id: A
  digest: b9bdda02a6c8f46abc583053f4a94ab8f15b8b575fc7ca1b8a90ed85e020470d
findings:
- id: F1
  part_id: null
  claim: Anthropic's webapp-testing skill uses native Python Playwright scripts to test local web applications.
  source: https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md
  fetched: '2026-10-18'
  quote: To test local web applications, write native Python Playwright scripts.
  context: '# Web Application Testing


    To test local web applications, write native Python Playwright scripts.


    **Helper Scripts Available**:'
  brief_digest: 1420be8e65da7160060ffa1f048e2292d0158d681859ee33aca743ee8667fb58
  source_role: primary
  pass: survey
- id: F2
  part_id: null
  claim: The webapp-testing license identifies Apache License, Version 2.0 as its license.
  source: https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/LICENSE.txt
  fetched: '2026-10-18'
  quote: "Licensed under the Apache License, Version 2.0 (the \"License\");\n   you may not use this file\
    \ except in compliance with the License."
  context: "Copyright 2026 Anthropic, PBC.\n\n   Licensed under the Apache License, Version 2.0 (the \"\
    License\");\n   you may not use this file except in compliance with the License."
  brief_digest: 1420be8e65da7160060ffa1f048e2292d0158d681859ee33aca743ee8667fb58
  source_role: primary
  pass: survey
- id: F3
  part_id: null
  claim: Anthropic describes its example skills as being provided for demonstration and educational purposes
    only.
  source: https://github.com/anthropics/skills
  fetched: '2026-10-18'
  quote: These skills are provided for demonstration and educational purposes only.
  context: 'Disclaimer


    These skills are provided for demonstration and educational purposes only.'
  brief_digest: 1420be8e65da7160060ffa1f048e2292d0158d681859ee33aca743ee8667fb58
  source_role: primary
  pass: survey
- id: F4
  part_id: null
  claim: Microsoft's Playwright CLI can record and generate Playwright code, inspect selectors, and take
    screenshots.
  source: https://github.com/microsoft/playwright-cli
  fetched: '2026-10-18'
  quote: Record and generate Playwright code, inspect selectors and take screenshots.
  context: CLI for common Playwright actions. Record and generate Playwright code, inspect selectors and
    take screenshots.
  brief_digest: 1420be8e65da7160060ffa1f048e2292d0158d681859ee33aca743ee8667fb58
  source_role: primary
  pass: survey
- id: F6
  part_id: null
  claim: Playwright supports soft assertions that mark a test as failed while allowing execution to continue.
  source: https://playwright.dev/docs/test-assertions
  fetched: '2026-10-18'
  quote: 'Playwright also supports soft assertions: failed soft assertions do not terminate test execution,
    but mark the test as failed.'
  context: 'By default, failed assertion will terminate test execution. Playwright also supports soft
    assertions: failed soft assertions do not terminate test execution, but mark the test as failed.'
  brief_digest: 1420be8e65da7160060ffa1f048e2292d0158d681859ee33aca743ee8667fb58
  source_role: primary
  pass: survey
- id: F8
  part_id: null
  claim: Playwright Trace Viewer loads traces in the browser without transmitting data externally.
  source: https://playwright.dev/docs/trace-viewer
  fetched: '2026-10-18'
  quote: Trace Viewer loads the trace entirely in your browser and does not transmit any data externally.
  context: Trace Viewer loads the trace entirely in your browser and does not transmit any data externally.
  brief_digest: 1420be8e65da7160060ffa1f048e2292d0158d681859ee33aca743ee8667fb58
  source_role: primary
  pass: survey
- id: F9
  part_id: null
  claim: Playwright warns that browser state files may contain cookies and headers capable of impersonating
    the user or test account.
  source: https://playwright.dev/docs/auth
  fetched: '2026-10-18'
  quote: The browser state file may contain sensitive cookies and headers that could be used to impersonate
    you or your test account.
  context: The browser state file may contain sensitive cookies and headers that could be used to impersonate
    you or your test account.
  brief_digest: 1420be8e65da7160060ffa1f048e2292d0158d681859ee33aca743ee8667fb58
  source_role: primary
  pass: survey
- id: F10
  part_id: A
  claim: 'Proposed rule idea.local-ui-testing.A.python-playwright (check: judged): Use native Python Playwright
    scripts to test the local web application.'
  source: https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md
  fetched: '2026-10-18'
  quote: To test local web applications, write native Python Playwright scripts.
  context: '# Web Application Testing


    To test local web applications, write native Python Playwright scripts.


    **Helper Scripts Available**:'
  brief_digest: b9bdda02a6c8f46abc583053f4a94ab8f15b8b575fc7ca1b8a90ed85e020470d
  source_role: primary
  pass: deep
- id: F11
  part_id: A
  claim: 'Proposed rule idea.local-ui-testing.A.console-events (check: judged): Capture browser console
    messages through page console events.'
  source: https://playwright.dev/docs/api/class-consolemessage
  fetched: '2026-10-18'
  quote: For each console message logged in the page there will be corresponding event in the Playwright
    context.
  context: ConsoleMessage objects are dispatched by page via the page.on('console') event. For each console
    message logged in the page there will be corresponding event in the Playwright context.
  brief_digest: b9bdda02a6c8f46abc583053f4a94ab8f15b8b575fc7ca1b8a90ed85e020470d
  source_role: primary
  pass: deep
- id: F12
  part_id: A
  claim: 'Proposed rule idea.local-ui-testing.A.console-buffer-limit (check: judged): Account for the
    console_messages API returning only up to the last 200 messages.'
  source: https://playwright.dev/python/docs/api/class-page
  fetched: '2026-10-18'
  quote: Returns up to (currently) 200 last console messages from this page.
  context: Returns up to (currently) 200 last console messages from this page. See page.on("console")
    for more details.
  brief_digest: b9bdda02a6c8f46abc583053f4a94ab8f15b8b575fc7ca1b8a90ed85e020470d
  source_role: primary
  pass: deep
- id: F13
  part_id: A
  claim: 'Proposed rule idea.local-ui-testing.A.screenshot-file (check: judged): Use the screenshot API
    with a file path to save screenshot evidence.'
  source: https://playwright.dev/docs/screenshots
  fetched: '2026-10-18'
  quote: 'Here is a quick way to capture a screenshot and save it into a file:'
  context: 'Here is a quick way to capture a screenshot and save it into a file:


    await page.screenshot({ path: ''screenshot.png'' });'
  brief_digest: b9bdda02a6c8f46abc583053f4a94ab8f15b8b575fc7ca1b8a90ed85e020470d
  source_role: primary
  pass: deep
support:
- finding_id: F1
  quote_check: pass
  verdict: supported
  worker_ref: support-f1
  finding_digest: bef9a93387b99b0bf34ecf9a5f9745ec486539712cbed0444d00bc970a710a55
- finding_id: F2
  quote_check: pass
  verdict: supported
  worker_ref: support-f2
  finding_digest: 98de76aa1d4b4b8f35c81e552b3b8bf9f35f59ec54972067ce92e02e88769b73
- finding_id: F3
  quote_check: pass
  verdict: supported
  worker_ref: support-f3
  finding_digest: 4f81b866a32d06d8a1f0fc82b6a56858b75a4dfa45a833c5875db1e86e1f9e04
- finding_id: F4
  quote_check: pass
  verdict: supported
  worker_ref: support-f4
  finding_digest: a8c296a6f3caf5bf9b75a8d85dd8f4611846939e83a55e45ed393dabd7727901
- finding_id: F5
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f5
- finding_id: F6
  quote_check: pass
  verdict: supported
  worker_ref: support-f6
  finding_digest: 0c95ac9956825387ae2bdb6e03078432b2bdcbfe53316d31c45629b98e8e7a50
- finding_id: F7
  quote_check: pass
  verdict: supported
  worker_ref: support-f7
- finding_id: F8
  quote_check: pass
  verdict: supported
  worker_ref: support-f8
  finding_digest: 539345cbc7ce681375ccc9f77501e3dc07e2a79479d24580fc0b14bc569bc80e
- finding_id: F9
  quote_check: pass
  verdict: supported
  worker_ref: support-f9
  finding_digest: 139735e161aec87e012b722c5716d76a5bc3521140b5f2a099cb834846c35e24
- finding_id: F10
  quote_check: pass
  verdict: supported
  worker_ref: support-f10
  finding_digest: 4e2b77a95a396abad772065ad984425f031a969ca04c2f6784062d2ed563a6cf
- finding_id: F11
  quote_check: pass
  verdict: supported
  worker_ref: support-f11
  finding_digest: 69db68db094d2cb0a8ad34e94b3390fd75bd2eed1cd6750a2cf8bb2bfa21a28c
- finding_id: F12
  quote_check: pass
  verdict: supported
  worker_ref: support-f12
  finding_digest: a98031e46873ed56bc0dd98616665fac8b87c3bf23ccad559ce7005f492583be
- finding_id: F13
  quote_check: pass
  verdict: supported
  worker_ref: support-f13
  finding_digest: 2a558c0d0059ec35e2a198840484e6b5fb17758fbb2cf467ecbf80ba1a3e1606
drift: []
---
Findings grouped by pass and part are in the frontmatter; dropped findings are not kept.
