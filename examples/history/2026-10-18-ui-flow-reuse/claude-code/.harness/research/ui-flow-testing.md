---
slug: ui-flow-testing
search_mode: live
briefs:
- pass: survey
  part_id: null
  digest: b829a7c4174077cfd0fefd67514d84b7c7b4d0d64a47711b2b7256762d431495
- pass: deep
  part_id: A
  digest: d52dec931ad6e5683c7b272d6c151896bf5293b1b0d228a833cd11d5ece90edc
findings:
- id: F2
  part_id: null
  claim: Playwright MCP works from accessibility snapshots, not pixel-based input.
  source: https://github.com/microsoft/playwright-mcp
  fetched: '2026-10-18'
  quote: Uses Playwright's accessibility tree, not pixel-based input.
  context: Uses Playwright's accessibility tree, not pixel-based input.
  brief_digest: b829a7c4174077cfd0fefd67514d84b7c7b4d0d64a47711b2b7256762d431495
  source_role: primary
  pass: survey
- id: F4
  part_id: null
  claim: 'In Playwright MCP, screenshots are evidence only: actions have to use the accessibility snapshot,
    not the screenshot.'
  source: https://github.com/microsoft/playwright-mcp
  fetched: '2026-10-18'
  quote: You can't perform actions based on the screenshot, use browser_snapshot for actions.
  context: You can't perform actions based on the screenshot, use browser_snapshot for actions.
  brief_digest: b829a7c4174077cfd0fefd67514d84b7c7b4d0d64a47711b2b7256762d431495
  source_role: primary
  pass: survey
- id: F10
  part_id: null
  claim: The webapp-testing skill has the agent write native Python Playwright scripts.
  source: https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md
  fetched: '2026-10-18'
  quote: To test local web applications, write native Python Playwright scripts.
  context: To test local web applications, write native Python Playwright scripts.
  brief_digest: b829a7c4174077cfd0fefd67514d84b7c7b4d0d64a47711b2b7256762d431495
  source_role: primary
  pass: survey
- id: F13
  part_id: null
  claim: Playwright's planner agent explores an app and writes a test plan for user flows.
  source: https://playwright.dev/docs/test-agents
  fetched: '2026-10-18'
  quote: Planner agent explores your app and produces a test plan for one or many scenarios and user flows.
  context: Planner agent explores your app and produces a test plan for one or many scenarios and user
    flows.
  brief_digest: b829a7c4174077cfd0fefd67514d84b7c7b4d0d64a47711b2b7256762d431495
  source_role: primary
  pass: survey
- id: F14
  part_id: null
  claim: Playwright's generator agent turns the Markdown plan into executable Playwright tests.
  source: https://playwright.dev/docs/test-agents
  fetched: '2026-10-18'
  quote: Generator agent uses the Markdown plan to produce executable Playwright Tests.
  context: Generator agent uses the Markdown plan to produce executable Playwright Tests.
  brief_digest: b829a7c4174077cfd0fefd67514d84b7c7b4d0d64a47711b2b7256762d431495
  source_role: primary
  pass: survey
- id: F15
  part_id: A
  claim: Anthropic's webapp-testing skill tells the agent not to inspect the DOM of a dynamic app before
    waiting for networkidle.
  source: https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md
  fetched: '2026-10-18'
  quote: ❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
  context: '❌ **Don''t** inspect the DOM before waiting for `networkidle` on dynamic apps

    ✅ **Do** wait for `page.wait_for_load_state(''networkidle'')` before inspection'
  brief_digest: d52dec931ad6e5683c7b272d6c151896bf5293b1b0d228a833cd11d5ece90edc
  source_role: primary
  pass: deep
- id: F17
  part_id: A
  claim: Anthropic's webapp-testing skill tells the agent to always close the browser when it is done.
  source: https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md
  fetched: '2026-10-18'
  quote: '- Always close the browser when done'
  context: '- Always close the browser when done'
  brief_digest: d52dec931ad6e5683c7b272d6c151896bf5293b1b0d228a833cd11d5ece90edc
  source_role: primary
  pass: deep
- id: F18
  part_id: A
  claim: Anthropic's webapp-testing skill does not give a standard open-source license in its frontmatter;
    it points to LICENSE.txt for the complete terms.
  source: https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md
  fetched: '2026-10-18'
  quote: 'license: Complete terms in LICENSE.txt'
  context: 'license: Complete terms in LICENSE.txt'
  brief_digest: d52dec931ad6e5683c7b272d6c151896bf5293b1b0d228a833cd11d5ece90edc
  source_role: primary
  pass: deep
- id: F20
  part_id: A
  claim: Playwright's best practices say web-first assertions make Playwright wait until the expected
    condition is met.
  source: https://playwright.dev/docs/best-practices
  fetched: '2026-10-18'
  quote: By using web first assertions Playwright will wait until the expected condition is met.
  context: Assertions are a way to verify that the expected result and the actual result matched or not.
    By using web first assertions Playwright will wait until the expected condition is met.
  brief_digest: d52dec931ad6e5683c7b272d6c151896bf5293b1b0d228a833cd11d5ece90edc
  source_role: primary
  pass: deep
- id: F22
  part_id: A
  claim: Playwright's best practices advise against testing links to external sites or third-party servers
    you do not control.
  source: https://playwright.dev/docs/best-practices
  fetched: '2026-10-18'
  quote: Don't try to test links to external sites or third party servers that you do not control.
  context: Only test what you control. Don't try to test links to external sites or third party servers
    that you do not control.
  brief_digest: d52dec931ad6e5683c7b272d6c151896bf5293b1b0d228a833cd11d5ece90edc
  source_role: primary
  pass: deep
- id: F23
  part_id: A
  claim: Playwright MCP's README says the agent cannot act on a screenshot and should use browser_snapshot
    for actions.
  source: https://raw.githubusercontent.com/microsoft/playwright-mcp/main/README.md
  fetched: '2026-10-18'
  quote: Take a screenshot of the current page. You can't perform actions based on the screenshot, use
    browser_snapshot for actions.
  context: Take a screenshot of the current page. You can't perform actions based on the screenshot, use
    browser_snapshot for actions.
  brief_digest: d52dec931ad6e5683c7b272d6c151896bf5293b1b0d228a833cd11d5ece90edc
  source_role: primary
  pass: deep
- id: F25
  part_id: A
  claim: Playwright MCP's README states that it is not a security boundary.
  source: https://raw.githubusercontent.com/microsoft/playwright-mcp/main/README.md
  fetched: '2026-10-18'
  quote: Playwright MCP is **not** a security boundary.
  context: Playwright MCP is **not** a security boundary.
  brief_digest: d52dec931ad6e5683c7b272d6c151896bf5293b1b0d228a833cd11d5ece90edc
  source_role: primary
  pass: deep
- id: F26
  part_id: A
  claim: In Playwright MCP's isolated mode, each session starts in an isolated profile.
  source: https://raw.githubusercontent.com/microsoft/playwright-mcp/main/README.md
  fetched: '2026-10-18'
  quote: In the isolated mode, each session is started in the isolated profile.
  context: In the isolated mode, each session is started in the isolated profile.
  brief_digest: d52dec931ad6e5683c7b272d6c151896bf5293b1b0d228a833cd11d5ece90edc
  source_role: primary
  pass: deep
- id: F27
  part_id: A
  claim: Playwright MCP's --allowed-origins option takes a semicolon-separated list of trusted origins
    the browser may request.
  source: https://raw.githubusercontent.com/microsoft/playwright-mcp/main/README.md
  fetched: '2026-10-18'
  quote: semicolon-separated list of TRUSTED origins to allow the browser to request.
  context: --allowed-origins <origins> | semicolon-separated list of TRUSTED origins to allow the browser
    to request.
  brief_digest: d52dec931ad6e5683c7b272d6c151896bf5293b1b0d228a833cd11d5ece90edc
  source_role: primary
  pass: deep
- id: F29
  part_id: A
  claim: Chrome DevTools MCP advises users not to share sensitive or personal information they do not
    want exposed to MCP clients.
  source: https://raw.githubusercontent.com/ChromeDevTools/chrome-devtools-mcp/main/README.md
  fetched: '2026-10-18'
  quote: Avoid sharing sensitive or personal information that you don't want to share with MCP clients.
  context: Avoid sharing sensitive or personal information that you don't want to share with MCP clients.
  brief_digest: d52dec931ad6e5683c7b272d6c151896bf5293b1b0d228a833cd11d5ece90edc
  source_role: primary
  pass: deep
- id: F30
  part_id: A
  claim: Playwright MCP Server versions before 0.0.40 did not validate the Origin header on incoming connections
    (GHSA-6fg3-hvw7-2fwq).
  source: https://github.com/advisories/GHSA-6fg3-hvw7-2fwq
  fetched: '2026-10-18'
  quote: Microsoft Playwright MCP Server versions prior to 0.0.40 fails to validate the Origin header
    on incoming connections.
  context: Microsoft Playwright MCP Server versions prior to 0.0.40 fails to validate the Origin header
    on incoming connections.
  brief_digest: d52dec931ad6e5683c7b272d6c151896bf5293b1b0d228a833cd11d5ece90edc
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
  finding_digest: c69d2187b3ee4793e84c56e501155cca5e0864c1665125ab352e1d948ba971f4
- finding_id: F3
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f3
- finding_id: F4
  quote_check: pass
  verdict: supported
  worker_ref: support-f4
  finding_digest: dd0c5af0613bf70833c87aeedd7b666738f32104f4e8c6b1aabf8d99acd0dd7c
- finding_id: F5
  quote_check: fail
  verdict: missing
  worker_ref: support-f5
- finding_id: F6
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f6
- finding_id: F7
  quote_check: fail
  verdict: missing
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
  finding_digest: 3c4466bccbceba2a03efaeb178c56097308a4992ffd0e76dc0fbd3ac231a36c1
- finding_id: F11
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f11
- finding_id: F12
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f12
- finding_id: F13
  quote_check: pass
  verdict: supported
  worker_ref: support-f13
  finding_digest: 2cf8c7a51c6607084f9aa837911028b7581af24ca1acb73bf352e8134624ab54
- finding_id: F14
  quote_check: pass
  verdict: supported
  worker_ref: support-f14
  finding_digest: d5674d76f819110d4099c51aaaf3b68be05311b0c1569db1b4ceafa2716aa538
- finding_id: F15
  quote_check: pass
  verdict: supported
  worker_ref: support-f15
  finding_digest: acb59bfc0af1c57935ab776be93ee7fe7247353af2b9c84ba6fba181ba298cd5
- finding_id: F16
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f16
- finding_id: F17
  quote_check: pass
  verdict: supported
  worker_ref: support-f17
  finding_digest: 45d06692728f8b40e9277b4e2db30ba9a90687a988b4e727ba598b5a065f9455
- finding_id: F18
  quote_check: pass
  verdict: supported
  worker_ref: support-f18
  finding_digest: 96e674b5aad7a4fc74cb00ec765ba2027c21fa46a877db58024996b2e7364d2d
- finding_id: F19
  quote_check: pass
  verdict: supported
  worker_ref: support-f19
- finding_id: F20
  quote_check: pass
  verdict: supported
  worker_ref: support-f20
  finding_digest: dd971a877f2092732b4319f61a43552eaa42d5883a759dd6e21e91eaac196db7
- finding_id: F21
  quote_check: pass
  verdict: supported
  worker_ref: support-f21
- finding_id: F22
  quote_check: pass
  verdict: supported
  worker_ref: support-f22
  finding_digest: 64c2ca4fb9ffaa0b53de13a591fc15db9676e525ed52dece21885b3b8ee67659
- finding_id: F23
  quote_check: pass
  verdict: supported
  worker_ref: support-f23
  finding_digest: cc95e4ddde95faa3dae196d8f04a8ef047934ce56853797c7c90dd2abb0c2add
- finding_id: F24
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f24
- finding_id: F25
  quote_check: pass
  verdict: supported
  worker_ref: support-f25
  finding_digest: e2ba5837389711d8778953f7844aa83bb447a093274cf9fdba7902841d05cc6c
- finding_id: F26
  quote_check: pass
  verdict: supported
  worker_ref: support-f26
  finding_digest: 6eb595012bf58f88d60781ca3e9e405c4fefb066276a872ee64583b24b692d6f
- finding_id: F27
  quote_check: pass
  verdict: supported
  worker_ref: support-f27
  finding_digest: eee923e08f1ae6ec5a0d5e5ac37a5c5a740ce4b92656c212583ded5a3e4dec56
- finding_id: F28
  quote_check: pass
  verdict: unsupported
  worker_ref: support-f28
- finding_id: F29
  quote_check: pass
  verdict: supported
  worker_ref: support-f29
  finding_digest: 6a213f19aeaef2d230684022dba2acceae322c2d975c78746346beaff13b4446
- finding_id: F30
  quote_check: pass
  verdict: supported
  worker_ref: support-f30
  finding_digest: 266fa2a162a3837d2ef1b03059258b7ebdb1655824537129ce3e6434f9477cfd
drift: []
---
Findings grouped by pass and part are in the frontmatter; dropped findings are not kept.
