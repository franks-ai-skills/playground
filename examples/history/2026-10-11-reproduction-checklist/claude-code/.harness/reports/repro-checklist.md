# Verification report

- Run: `713d699f-verify-a-4`
- Harness KB version: 0.1.0
- Contract digest: b5aa8b27b98a59d8495390268762147f69731a9b8b43034f378c2443cee6c771
- Confirmed parts: A
- Decision record digest: b5863aaffa9e6e8fdee18c2db14d5823007eb1661fdf47fd31e8d36214afb9a2
- Whole-idea answers and targets: `{"facts": {"bypass_mode": true, "lethal_trifecta": true, "opens_prs": true, "plan_controls": "unknown", "reach": "public", "target_set": "both", "untrusted_repo": true}, "hosting": {"plan": "any", "platform": "any (platform-agnostic)", "visibility": "unknown"}, "reach": "public", "targets": ["claude-code", "codex"]}` (digest 32800bac475d0067eb27ae63089e714e68d10acea3cf9118c90ef56c8e990214)
- Rule content digest: d57f742e2e061ef35e3497be96cb6e20e1782272b44da47b59abacba8d164e54
- Accepted Idea KB revision: fb67de3f6a2a7c750204d87f62f3c26fcf0646f53562bb594396b495eea19e25
- Review scope: Extensive review (rarely needed)
- Rule overrides: none
- Checker versions digest: 49d1dc3feb234903cb74e7ea22c79bd3e66bea53f90e2c85a2ba30f091cdcd1c

## Worker isolation

Workers ran under `best-effort-v1` with isolation status `not-certified`. Research, source-support and review workers run as independent CLI processes with explicit role inputs and the available restrictions. Complete tool absence and context, file and network isolation are not guaranteed; use trusted projects and operator-approved inputs.

- research worker: claude-code 2.1.296 (Claude Code), model account default, launcher independent-process, configuration 8f829a4997165574f012341c9cfd6babd3d9105bc9c559508d67a78b3ae277ea, controls: command: ["claude", "--print", "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--safe-mode", "--restricted", "--setting-sources", "", "--strict-mcp-config", "--mcp-config", "{\"mcpServers\":{}}", "--disable-slash-commands", "--permission-mode", "dontAsk", "--permission-prompts", "none", "--settings", "{\"disableAllHooks\":true,\"autoMemoryEnabled\":false}", "--tools", "WebFetch,WebSearch", "--allowedTools", "WebFetch,WebSearch", "--json-schema", "{\"type\":\"object\",\"properties\":{\"findings\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"claim\":{\"type\":\"string\"},\"source\":{\"type\":\"string\"},\"fetched\":{\"type\":\"string\"},\"quote\":{\"type\":\"string\"},\"context\":{\"type\":\"string\"},\"source_role\":{\"enum\":[\"primary\",\"practitioner\",\"trade-press\"]}},\"required\":[\"claim\",\"source\",\"fetched\",\"quote\",\"context\",\"source_role\"],\"additionalProperties\":false}}},\"required\":[\"findings\"],\"additionalProperties\":false}"]; environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (claude.ai), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- source-support worker: claude-code 2.1.296 (Claude Code), model account default, launcher independent-process, configuration f79908e2f8761717b26bb5d87aed5c56e135ba70a0edb97e404129d59e06e708, controls: command: ["claude", "--print", "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--safe-mode", "--restricted", "--setting-sources", "", "--strict-mcp-config", "--mcp-config", "{\"mcpServers\":{}}", "--disable-slash-commands", "--permission-mode", "dontAsk", "--permission-prompts", "none", "--settings", "{\"disableAllHooks\":true,\"autoMemoryEnabled\":false}", "--tools", "", "--allowedTools", "", "--json-schema", "{\"type\":\"object\",\"properties\":{\"verdicts\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"finding_id\":{\"type\":\"string\"},\"verdict\":{\"enum\":[\"supported\",\"unsupported\"]},\"reasoning\":{\"type\":\"string\"}},\"required\":[\"finding_id\",\"verdict\",\"reasoning\"],\"additionalProperties\":false}}},\"required\":[\"verdicts\"],\"additionalProperties\":false}"]; environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (claude.ai), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- review worker: claude-code 2.1.296 (Claude Code), model account default, launcher independent-process, configuration bd41806234b54333f0b42bf98e08945ea9756a175b212e92e0435a771b2beb3f, controls: command: ["claude", "--print", "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--safe-mode", "--restricted", "--setting-sources", "", "--strict-mcp-config", "--mcp-config", "{\"mcpServers\":{}}", "--disable-slash-commands", "--permission-mode", "dontAsk", "--permission-prompts", "none", "--settings", "{\"disableAllHooks\":true,\"autoMemoryEnabled\":false}", "--tools", "Read,Grep,Glob", "--allowedTools", "Read,Grep,Glob", "--json-schema", "{\"type\":\"object\",\"properties\":{\"run_id\":{\"type\":\"string\"},\"verdicts\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"part_id\":{\"type\":\"string\"},\"rule_id\":{\"type\":\"string\"},\"verdict\":{\"enum\":[\"pass\",\"fail\",\"not-applicable\"]},\"reason\":{\"type\":\"string\"},\"citation\":{\"type\":\"string\"}},\"required\":[\"part_id\",\"rule_id\",\"verdict\",\"reason\",\"citation\"],\"additionalProperties\":false}},\"goal_verdicts\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"part_id\":{\"type\":\"string\"},\"verdict\":{\"enum\":[\"met\",\"not-met\"]},\"reason\":{\"type\":\"string\"}},\"required\":[\"part_id\",\"verdict\",\"reason\"],\"additionalProperties\":false}}},\"required\":[\"run_id\",\"verdicts\",\"goal_verdicts\"],\"additionalProperties\":false}"]; environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (claude.ai), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- review worker: claude-code 2.1.296 (Claude Code), model account default, launcher independent-process, configuration bd41806234b54333f0b42bf98e08945ea9756a175b212e92e0435a771b2beb3f, controls: command: ["claude", "--print", "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--safe-mode", "--restricted", "--setting-sources", "", "--strict-mcp-config", "--mcp-config", "{\"mcpServers\":{}}", "--disable-slash-commands", "--permission-mode", "dontAsk", "--permission-prompts", "none", "--settings", "{\"disableAllHooks\":true,\"autoMemoryEnabled\":false}", "--tools", "Read,Grep,Glob", "--allowedTools", "Read,Grep,Glob", "--json-schema", "{\"type\":\"object\",\"properties\":{\"run_id\":{\"type\":\"string\"},\"verdicts\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"part_id\":{\"type\":\"string\"},\"rule_id\":{\"type\":\"string\"},\"verdict\":{\"enum\":[\"pass\",\"fail\",\"not-applicable\"]},\"reason\":{\"type\":\"string\"},\"citation\":{\"type\":\"string\"}},\"required\":[\"part_id\",\"rule_id\",\"verdict\",\"reason\",\"citation\"],\"additionalProperties\":false}},\"goal_verdicts\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"part_id\":{\"type\":\"string\"},\"verdict\":{\"enum\":[\"met\",\"not-met\"]},\"reason\":{\"type\":\"string\"}},\"required\":[\"part_id\",\"verdict\",\"reason\"],\"additionalProperties\":false}}},\"required\":[\"run_id\",\"verdicts\",\"goal_verdicts\"],\"additionalProperties\":false}"]; environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (claude.ai), observed tools: Glob, Grep, Read, StructuredOutput, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable

## Part A

- Harness result: not verified
- Goal result: not met
- Status: built
- Outside dependencies: none
- Confirmed answers: `{"event_without_agent": false, "every_time": "usually", "irreversible": false, "job": "procedure", "must_survive_compromise": "not-required", "own_context": true, "trigger": "model", "who_disables": "contributor"}`
- Goal verdict: met (SKILL.md runs a tool preflight that blocks with an error naming each missing tool, which tells the user what is missing without asking questions. It then records only inspected environment facts and keeps Expected and Actual separate and observable, with speculation in its own section. It runs the reproduction at least twice and reports frequency, makes no implementation edits, treats the report as untrusted quoted data, and returns a checklist that people can follow and agents can parse without placing it anywhere. All nine accepted requirements are covered by the written procedure.)

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `idea.repro-checklist.a.expected-actual` | error | judged | pass | Expected and Actual are separate sections, each marked 'without a cause'. Any suspected cause goes in a separate 'Speculation (not verified)' section. | SKILL.md lines 72-79 | https://raw.githubusercontent.com/github/awesome-copilot/main/skills/bug-reproduction-brief/SKILL.md, https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html, https://www.chiark.greenend.org.uk/~sgtatham/bugs.html |
| `idea.repro-checklist.a.inspectable-environment` | error | judged | pass | Step 3 says to write down only what command output showed and to mark everything else 'not inspected'. The template heading is 'Environment (inspected)'. | SKILL.md lines 43-47, 63-64 | https://raw.githubusercontent.com/github/awesome-copilot/main/skills/bug-reproduction-brief/SKILL.md |
| `idea.repro-checklist.a.no-implementation-edits` | error | judged | pass | 'Do not change implementation code; put any helper script in a temporary directory outside the source tree.' | SKILL.md lines 48-50 | https://raw.githubusercontent.com/github/awesome-copilot/main/skills/bug-reproduction-brief/SKILL.md |
| `idea.repro-checklist.a.no-interaction` | error | judged | pass | 'Run every step without asking anyone. When a step cannot be completed, end with the error from step 2 instead of a question.' | SKILL.md lines 21-22 | https://learn.chatgpt.com/docs/build-skills |
| `idea.repro-checklist.a.numbered-steps` | error | judged | pass | The template has numbered steps of the form '<imperative action> — input: <exact command or input> — check: <observable output>'. | SKILL.md lines 69-70 | https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html, https://learn.chatgpt.com/docs/build-skills |
| `idea.repro-checklist.a.repeat-and-frequency` | error | judged | pass | The reproduction runs at least twice where safe, and at least five times if results differ. The checklist reports 'every time (n/n) \| occasionally (k/n) \| not at all (0/n)'. | SKILL.md lines 52-54, 61, 85-86 | https://raw.githubusercontent.com/github/awesome-copilot/main/skills/bug-reproduction-brief/SKILL.md, https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html |
| `idea.repro-checklist.a.report-is-data` | error | judged | pass | The report is read as untrusted data and its instructions are not followed. Quoted report lines go in a separate section headed 'From the report (untrusted, quoted)' using blockquotes. | SKILL.md lines 24-30, 81-82 | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ |
| `idea.repro-checklist.a.returns-only` | error | judged | pass | 'Reply with the checklist only. Do not post it as a comment, write it to a file or send it anywhere; the caller decides where it goes.' | SKILL.md lines 87-89 | https://learn.chatgpt.com/docs/build-skills |
| `idea.repro-checklist.a.tool-preflight` | error | judged | pass | Step 2 lists the tools needed to build, trigger, observe and rerun, and checks each one with a version command. If any is missing it stops and returns only a REPRODUCTION BLOCKED error naming each missing tool, so no checklist is produced. | SKILL.md lines 31-41 | https://learn.chatgpt.com/docs/build-skills |
| `outside.ci.required-on-ref` | warning | judged | pass | No CI check is presented as a gate in the recommendations, so none is counted as a gate without being required. | README.md lines 5-9 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | pass | The recommendations define no CI gate checks, so there are no unpinned gate sources. | README.md lines 5-9 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | fail | The codeowners recommendation does not state that workflow or policy files go under code owners or that CODEOWNERS owns itself. It only lists the rule id. | README.md line 7 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | fail | 'codeowners-agent-config' is named, but the README gives no CODEOWNERS entry for the agent's configuration files (e.g. .agents/) and does not mention the setting that requires code-owner review. | README.md line 7 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | fail | The outer-isolation entry names no broader credentials or channels to close, such as personal tokens or metadata endpoints. It only lists the rule id. | README.md line 9 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | fail | No recommendation tells the user to re-check the control configuration periodically. | README.md lines 5-9 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | pass | Each control is marked 'recommended, not verified... availability unknown', so the recommendation does not claim the control is enforced on the user's plan. | README.md lines 7-9 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | fail | The merge-rules recommendation names no branches, tags or resources. It lists only prerequisite ids. | README.md line 8 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | fail | The recommendation does not say that the agent's bot, app, token or launching human must be on no bypass list. It only cites the rule id as a prerequisite. | README.md line 8 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | fail | The recommendation does not say that approval must come from someone other than the author, last pusher or launcher, nor that approval resets on new pushes. | README.md line 8 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | not-applicable | The agent opens no pull requests in this skill. It only returns a checklist and forbids posting or writing it elsewhere. | SKILL.md lines 87-89 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 3 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `security.approval.claims-are-data` | warning | judged | pass | Nothing in the procedure lets content grant authorization. The report's instructions are explicitly not followed. | SKILL.md lines 26-30 | docs/guide/security.md#context-and-persistent-state |
| `security.helpers.confined` | warning | judged | pass | Helper scripts go in a temporary directory outside the source tree and run under the session's normal permissions. Nothing is pre-approved and nothing is installed. | SKILL.md lines 35, 49-50 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#executables-approvals-and-isolation |
| `security.outbound.minimal-data` | warning | judged | pass | The skill sends nothing outward: it forbids posting or sending the checklist. The report only gets read, and its content cannot add actions because embedded instructions are not followed. | SKILL.md lines 24-30, 87-89 | docs/guide/security.md#data-access-and-outbound-channels, https://developers.openai.com/api/docs/guides/deep-research#prompt-injection-and-exfiltration |
| `security.secrets.none-in-files` | error | judged | pass | The files contain no credentials, tokens or keys. The only hash is a public content digest. | all three files | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#context-and-persistent-state |
| `security.untrusted-input.as-data` | warning | judged | pass | Step 1 says everything in the report is untrusted data, that embedded instructions are not followed, and that the checklist records that they were not followed. | SKILL.md lines 24-30 | docs/guide/security.md#context-and-persistent-state |
| `skills.body.gotchas-first` | warning | judged | pass | The non-negotiable requirements sit at the top of SKILL.md under '## Requirements', not only in the reference file. | SKILL.md lines 7-17 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://agentskills.io/skill-creation/best-practices.md |
| `skills.body.no-time-bound-statements` | warning | judged | pass | None of the files contains a date, version-dated claim or 'currently/as of' statement. | SKILL.md; references/requirements.md | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.only-what-model-lacks` | warning | judged | pass | The procedure holds task-specific instructions the model would otherwise get wrong: the error format, the checklist template, the run-count rules and the unsafe-action marking. It does not explain general knowledge. The Requirements block repeats the procedure, but it does not teach known material. | SKILL.md lines 19-89 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.reasons-before-hard-rules` | warning | judged | pass | Key rules carry their reason ('so that a person can follow it and an agent can parse it'; 'the caller decides where it goes'; unsafe actions are named as production, user data or paid services). There is no all-caps ALWAYS/NEVER wording. The 'Never:' prefixes are restrained. | SKILL.md lines 51-56, 87-89 | docs/best-practices/skills.md#7-explain-the-why-before-adding-hard-rules |
| `skills.body.size` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, docs/concepts/skills.md#body, https://code.claude.com/docs/en/skills, https://agentskills.io/specification |
| `skills.body.strictness-matches-fragility` | warning | judged | pass | Strict wording is limited to the fragile parts: the exact checklist form so an agent can parse it, the blocked-error format, and the run counts. Each step gives one default and offers no menu of options. | SKILL.md lines 36-41, 53-83 | docs/best-practices/skills.md#5-match-strictness-to-fragility, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.description.boundary` | warning | judged | pass | It names the neighbouring tasks it is not for: 'Not for fixing the bug, judging whether a report is complete, posting the checklist or triaging reports.' | SKILL.md line 3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.description.concise` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, docs/research-notes/agent-harness-best-practices/skills.md |
| `skills.description.length` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/opencode/skills.md#format, https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs, https://opencode.ai/docs/skills/ |
| `skills.description.no-workflow-steps` | warning | judged | pass | The description covers only what the skill does and when to use it. It lists no procedure steps. | SKILL.md line 3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md |
| `skills.description.voice` | warning | judged | pass | It is written in the third person ('Reproduces...', 'Use when...'), with no 'I can' or 'You can'. | SKILL.md line 3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition |
| `skills.description.what-and-when` | warning | judged | pass | The description opens with concrete verbs and objects ('Reproduces a reported bug and returns a numbered reproduction checklist'), then gives triggers a user would say ('reproduce a bug', 'write repro steps', 'make a reproduction checklist for issue #42'). | SKILL.md line 3, description | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://learn.chatgpt.com/docs/build-skills, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.frontmatter.valid` | error | script | pass | 1 skill(s) checked | - | docs/vendors/opencode/skills.md#format, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/claude-code/skills.md#format, docs/concepts/skills.md#frontmatter, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.goal.no-must-hold-rule-in-skill` | error | judged | fail | The goal requires 'no implementation edits while building it', a rule that must hold on every edit. Only skill text enforces it (Requirements line 15, Procedure step 4). There is no hook, permission deny or allowed-tools restriction, and the README lists no outside control for it. | SKILL.md lines 15, 48-50; README.md lines 5-9 | docs/best-practices/skills.md#13-move-rules-that-must-hold-every-time-into-hooks, https://code.claude.com/docs/en/skills |
| `skills.inputs.from-message` | warning | judged | pass | The bug report is taken from the user's message, with no argument substitution. When the report is missing or unreadable, the skill ends with an error instead of asking, which the no-interaction requirement demands. | SKILL.md lines 21-25, 35-36 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, docs/concepts/skills.md#body |
| `skills.invocation.both-flags` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#invocation-policy-in-both-leads, docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.invocation.side-effects-user-invoked` | error | judged | not-applicable | The skill does not deploy, commit, post or change external state. It forbids posting or writing the checklist and skips actions on production systems or paid services. | SKILL.md lines 50-52, 87-89 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.name.format` | error | script | pass | 1 skill(s) checked | - | docs/guide/skills.md#portability, docs/concepts/skills.md#frontmatter, docs/vendors/opencode/skills.md#format, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.package.no-auxiliary-docs` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#anti-patterns, https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md |
| `skills.portable.frontmatter` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/best-practices/skills.md#12-keep-one-canonical-copy-with-portable-frontmatter, https://code.claude.com/docs/en/skills |
| `skills.portable.layout` | error | script | pass | 1 skill(s) linked | - | docs/concepts/skills.md#directory-layout, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.portable.no-claude-placeholders` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#body, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills |
| `skills.references.load-conditions` | warning | judged | fail | The reference file is named with a load condition ('when you need the source behind one of the requirements'). But every requirement statement appears word for word in both SKILL.md and references/requirements.md, and again in substance in the Procedure. Those facts do not live in one place. | SKILL.md lines 9-17 and 91-92; references/requirements.md lines 6-14 | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/best-practices.md |
| `skills.references.one-level` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/specification |
| `skills.references.resolve` | error | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.reuse.reviewed-and-pinned` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#security, https://owasp.github.io/www-project-agentic-skills-top-10/ast01 |
| `skills.scope.committed-for-automation` | warning | judged | pass | The skill sits in the project-scoped .agents/skills/ directory of the repository, not only in user scope. | .agents/skills/repro-checklist/SKILL.md path | docs/concepts/skills.md#directory-layout, https://code.claude.com/docs/en/skills |
| `skills.scripts.agent-caller` | warning | judged | not-applicable | The skill bundles no scripts. Its only files are SKILL.md and a markdown reference. | .agents/skills/repro-checklist/ file list | docs/best-practices/skills.md#6-put-deterministic-logic-in-tested-scripts, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/using-scripts.md |
| `skills.security.allowed-tools-least-privilege` | warning | judged | not-applicable | The frontmatter declares no allowed-tools, so the skill grants no tools. | SKILL.md lines 1-4 | docs/best-practices/skills.md#security, docs/vendors/claude-code/skills.md#limits-and-gotchas, https://code.claude.com/docs/en/skills |
| `skills.security.no-surprising-content` | error | judged | pass | The files contain no hidden directives, remote fetch-and-run, encoded payloads or credential access. The source URLs in the reference file are citations only. | SKILL.md; references/requirements.md | docs/best-practices/skills.md#security, https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md |

Contested `skills.body.reasons-before-hard-rules`:
- All-caps ALWAYS or NEVER is a yellow flag; explain the reasoning instead (https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md, https://agentskills.io/skill-creation/evaluating-skills.md)
- Discipline skills need firm prohibitions and rationalization tables (https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

Contested `skills.description.voice`:
- Always write in the third person; an inconsistent point of view can cause discovery problems (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Use imperative "Use this skill when" phrasing for the trigger (https://agentskills.io/skill-creation/optimizing-descriptions.md, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)

## Runtime tests

| Part | Case | Harness | Result | Observed | Reason |
| --- | --- | --- | --- | --- | --- |
| A | repro-explicit | claude-code 2.1.296 (Claude Code) | pass | Skill tool called for repro-checklist | Skill tool called for repro-checklist |
| A | repro-implicit | claude-code 2.1.296 (Claude Code) | pass | Skill tool called for repro-checklist | Skill tool called for repro-checklist |
| A | repro-near-miss | claude-code 2.1.296 (Claude Code) | pass | - | no Skill tool call for the candidate |

## Checked files

```
0bb1a838d12c534099cf7d7927cce508ffb98b193287c4e7efc659c2f6bb31a8  .agents/skills/repro-checklist/SKILL.md
e18797951df45df71f8689db7f208c77c397781955b519a700438ad553bf1b5f  .agents/skills/repro-checklist/references/requirements.md
2962f60e38e29c7b8331f08654f8254f7fe2725f5ba79c2d53aa342dc1859fa4  README.md
link  .claude/skills/repro-checklist -> ../../.agents/skills/repro-checklist
```

## Report data

```json
{
  "answers": {
    "A": {
      "event_without_agent": false,
      "every_time": "usually",
      "irreversible": false,
      "job": "procedure",
      "must_survive_compromise": "not-required",
      "own_context": true,
      "trigger": "model",
      "who_disables": "contributor"
    }
  },
  "confirmed_parts": [
    "A"
  ],
  "contract_digest": "b5aa8b27b98a59d8495390268762147f69731a9b8b43034f378c2443cee6c771",
  "decision_digest": "b5863aaffa9e6e8fdee18c2db14d5823007eb1661fdf47fd31e8d36214afb9a2",
  "file_hashes": {
    ".agents/skills/repro-checklist/SKILL.md": "0bb1a838d12c534099cf7d7927cce508ffb98b193287c4e7efc659c2f6bb31a8",
    ".agents/skills/repro-checklist/references/requirements.md": "e18797951df45df71f8689db7f208c77c397781955b519a700438ad553bf1b5f",
    "README.md": "2962f60e38e29c7b8331f08654f8254f7fe2725f5ba79c2d53aa342dc1859fa4"
  },
  "idea_digest": "32800bac475d0067eb27ae63089e714e68d10acea3cf9118c90ef56c8e990214",
  "kb_version": "0.1.0",
  "overrides": [],
  "parts": [
    {
      "goal_result": "not met",
      "goal_verdict": {
        "reason": "SKILL.md runs a tool preflight that blocks with an error naming each missing tool, which tells the user what is missing without asking questions. It then records only inspected environment facts and keeps Expected and Actual separate and observable, with speculation in its own section. It runs the reproduction at least twice and reports frequency, makes no implementation edits, treats the report as untrusted quoted data, and returns a checklist that people can follow and agents can parse without placing it anywhere. All nine accepted requirements are covered by the written procedure.",
        "verdict": "met"
      },
      "harness_result": "not verified",
      "outside_dependencies": [],
      "part_id": "A",
      "rule_results": [
        {
          "check": "script",
          "reason": "1 skill(s) checked",
          "result": "pass",
          "rule_id": "skills.frontmatter.valid"
        },
        {
          "check": "script",
          "reason": "1 skill(s) checked",
          "result": "pass",
          "rule_id": "skills.name.format"
        },
        {
          "check": "script",
          "reason": "1 skill(s) checked",
          "result": "pass",
          "rule_id": "skills.description.length"
        },
        {
          "check": "script",
          "reason": "1 skill(s) checked",
          "result": "pass",
          "rule_id": "skills.description.concise"
        },
        {
          "check": "script",
          "reason": "1 skill(s) checked",
          "result": "pass",
          "rule_id": "skills.body.size"
        },
        {
          "check": "script",
          "reason": "1 skill(s) checked",
          "result": "pass",
          "rule_id": "skills.references.resolve"
        },
        {
          "check": "script",
          "reason": "1 skill(s) checked",
          "result": "pass",
          "rule_id": "skills.references.one-level"
        },
        {
          "check": "script",
          "reason": "1 skill(s) checked",
          "result": "pass",
          "rule_id": "skills.package.no-auxiliary-docs"
        },
        {
          "check": "script",
          "reason": "1 skill(s) linked",
          "result": "pass",
          "rule_id": "skills.portable.layout"
        },
        {
          "check": "script",
          "reason": "1 skill(s) checked",
          "result": "pass",
          "rule_id": "skills.portable.frontmatter"
        },
        {
          "check": "script",
          "reason": "1 skill(s) checked",
          "result": "pass",
          "rule_id": "skills.portable.no-claude-placeholders"
        },
        {
          "check": "script",
          "reason": "1 skill(s) checked",
          "result": "pass",
          "rule_id": "skills.invocation.both-flags"
        },
        {
          "check": "judged",
          "citation": "SKILL.md line 3, description",
          "reason": "The description opens with concrete verbs and objects ('Reproduces a reported bug and returns a numbered reproduction checklist'), then gives triggers a user would say ('reproduce a bug', 'write repro steps', 'make a reproduction checklist for issue #42').",
          "result": "pass",
          "rule_id": "skills.description.what-and-when"
        },
        {
          "check": "judged",
          "citation": "SKILL.md line 3",
          "reason": "The description covers only what the skill does and when to use it. It lists no procedure steps.",
          "result": "pass",
          "rule_id": "skills.description.no-workflow-steps"
        },
        {
          "check": "judged",
          "citation": "SKILL.md line 3",
          "reason": "It names the neighbouring tasks it is not for: 'Not for fixing the bug, judging whether a report is complete, posting the checklist or triaging reports.'",
          "result": "pass",
          "rule_id": "skills.description.boundary"
        },
        {
          "check": "judged",
          "citation": "SKILL.md line 3",
          "reason": "It is written in the third person ('Reproduces...', 'Use when...'), with no 'I can' or 'You can'.",
          "result": "pass",
          "rule_id": "skills.description.voice"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 19-89",
          "reason": "The procedure holds task-specific instructions the model would otherwise get wrong: the error format, the checklist template, the run-count rules and the unsafe-action marking. It does not explain general knowledge. The Requirements block repeats the procedure, but it does not teach known material.",
          "result": "pass",
          "rule_id": "skills.body.only-what-model-lacks"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 7-17",
          "reason": "The non-negotiable requirements sit at the top of SKILL.md under '## Requirements', not only in the reference file.",
          "result": "pass",
          "rule_id": "skills.body.gotchas-first"
        },
        {
          "check": "judged",
          "citation": "SKILL.md; references/requirements.md",
          "reason": "None of the files contains a date, version-dated claim or 'currently/as of' statement.",
          "result": "pass",
          "rule_id": "skills.body.no-time-bound-statements"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 9-17 and 91-92; references/requirements.md lines 6-14",
          "reason": "The reference file is named with a load condition ('when you need the source behind one of the requirements'). But every requirement statement appears word for word in both SKILL.md and references/requirements.md, and again in substance in the Procedure. Those facts do not live in one place.",
          "result": "fail",
          "rule_id": "skills.references.load-conditions"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 36-41, 53-83",
          "reason": "Strict wording is limited to the fragile parts: the exact checklist form so an agent can parse it, the blocked-error format, and the run counts. Each step gives one default and offers no menu of options.",
          "result": "pass",
          "rule_id": "skills.body.strictness-matches-fragility"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/repro-checklist/ file list",
          "reason": "The skill bundles no scripts. Its only files are SKILL.md and a markdown reference.",
          "result": "not-applicable",
          "rule_id": "skills.scripts.agent-caller"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 51-56, 87-89",
          "reason": "Key rules carry their reason ('so that a person can follow it and an agent can parse it'; 'the caller decides where it goes'; unsafe actions are named as production, user data or paid services). There is no all-caps ALWAYS/NEVER wording. The 'Never:' prefixes are restrained.",
          "result": "pass",
          "rule_id": "skills.body.reasons-before-hard-rules"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 50-52, 87-89",
          "reason": "The skill does not deploy, commit, post or change external state. It forbids posting or writing the checklist and skips actions on production systems or paid services.",
          "result": "not-applicable",
          "rule_id": "skills.invocation.side-effects-user-invoked"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 21-25, 35-36",
          "reason": "The bug report is taken from the user's message, with no argument substitution. When the report is missing or unreadable, the skill ends with an error instead of asking, which the no-interaction requirement demands.",
          "result": "pass",
          "rule_id": "skills.inputs.from-message"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 15, 48-50; README.md lines 5-9",
          "reason": "The goal requires 'no implementation edits while building it', a rule that must hold on every edit. Only skill text enforces it (Requirements line 15, Procedure step 4). There is no hook, permission deny or allowed-tools restriction, and the README lists no outside control for it.",
          "result": "fail",
          "rule_id": "skills.goal.no-must-hold-rule-in-skill"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/repro-checklist/SKILL.md path",
          "reason": "The skill sits in the project-scoped .agents/skills/ directory of the repository, not only in user scope.",
          "result": "pass",
          "rule_id": "skills.scope.committed-for-automation"
        },
        {
          "check": "judged",
          "citation": "SKILL.md; references/requirements.md",
          "reason": "The files contain no hidden directives, remote fetch-and-run, encoded payloads or credential access. The source URLs in the reference file are citations only.",
          "result": "pass",
          "rule_id": "skills.security.no-surprising-content"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 1-4",
          "reason": "The frontmatter declares no allowed-tools, so the skill grants no tools.",
          "result": "not-applicable",
          "rule_id": "skills.security.allowed-tools-least-privilege"
        },
        {
          "check": "judged",
          "citation": "all three files",
          "reason": "The files contain no credentials, tokens or keys. The only hash is a public content digest.",
          "result": "pass",
          "rule_id": "security.secrets.none-in-files"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 24-30",
          "reason": "Step 1 says everything in the report is untrusted data, that embedded instructions are not followed, and that the checklist records that they were not followed.",
          "result": "pass",
          "rule_id": "security.untrusted-input.as-data"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 26-30",
          "reason": "Nothing in the procedure lets content grant authorization. The report's instructions are explicitly not followed.",
          "result": "pass",
          "rule_id": "security.approval.claims-are-data"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 35, 49-50",
          "reason": "Helper scripts go in a temporary directory outside the source tree and run under the session's normal permissions. Nothing is pre-approved and nothing is installed.",
          "result": "pass",
          "rule_id": "security.helpers.confined"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 24-30, 87-89",
          "reason": "The skill sends nothing outward: it forbids posting or sending the checklist. The report only gets read, and its content cannot add actions because embedded instructions are not followed.",
          "result": "pass",
          "rule_id": "security.outbound.minimal-data"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 31-41",
          "reason": "Step 2 lists the tools needed to build, trigger, observe and rerun, and checks each one with a version command. If any is missing it stops and returns only a REPRODUCTION BLOCKED error naming each missing tool, so no checklist is produced.",
          "result": "pass",
          "rule_id": "idea.repro-checklist.a.tool-preflight"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 21-22",
          "reason": "'Run every step without asking anyone. When a step cannot be completed, end with the error from step 2 instead of a question.'",
          "result": "pass",
          "rule_id": "idea.repro-checklist.a.no-interaction"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 69-70",
          "reason": "The template has numbered steps of the form '<imperative action> \u2014 input: <exact command or input> \u2014 check: <observable output>'.",
          "result": "pass",
          "rule_id": "idea.repro-checklist.a.numbered-steps"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 43-47, 63-64",
          "reason": "Step 3 says to write down only what command output showed and to mark everything else 'not inspected'. The template heading is 'Environment (inspected)'.",
          "result": "pass",
          "rule_id": "idea.repro-checklist.a.inspectable-environment"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 72-79",
          "reason": "Expected and Actual are separate sections, each marked 'without a cause'. Any suspected cause goes in a separate 'Speculation (not verified)' section.",
          "result": "pass",
          "rule_id": "idea.repro-checklist.a.expected-actual"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 52-54, 61, 85-86",
          "reason": "The reproduction runs at least twice where safe, and at least five times if results differ. The checklist reports 'every time (n/n) | occasionally (k/n) | not at all (0/n)'.",
          "result": "pass",
          "rule_id": "idea.repro-checklist.a.repeat-and-frequency"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 48-50",
          "reason": "'Do not change implementation code; put any helper script in a temporary directory outside the source tree.'",
          "result": "pass",
          "rule_id": "idea.repro-checklist.a.no-implementation-edits"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 24-30, 81-82",
          "reason": "The report is read as untrusted data and its instructions are not followed. Quoted report lines go in a separate section headed 'From the report (untrusted, quoted)' using blockquotes.",
          "result": "pass",
          "rule_id": "idea.repro-checklist.a.report-is-data"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 87-89",
          "reason": "'Reply with the checklist only. Do not post it as a comment, write it to a file or send it anywhere; the caller decides where it goes.'",
          "result": "pass",
          "rule_id": "idea.repro-checklist.a.returns-only"
        },
        {
          "check": "script",
          "reason": "3 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": "README.md line 8",
          "reason": "The merge-rules recommendation names no branches, tags or resources. It lists only prerequisite ids.",
          "result": "fail",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md line 8",
          "reason": "The recommendation does not say that the agent's bot, app, token or launching human must be on no bypass list. It only cites the rule id as a prerequisite.",
          "result": "fail",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md line 8",
          "reason": "The recommendation does not say that approval must come from someone other than the author, last pusher or launcher, nor that approval resets on new pushes.",
          "result": "fail",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md lines 5-9",
          "reason": "No CI check is presented as a gate in the recommendations, so none is counted as a gate without being required.",
          "result": "pass",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md lines 5-9",
          "reason": "The recommendations define no CI gate checks, so there are no unpinned gate sources.",
          "result": "pass",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md line 7",
          "reason": "The codeowners recommendation does not state that workflow or policy files go under code owners or that CODEOWNERS owns itself. It only lists the rule id.",
          "result": "fail",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md line 9",
          "reason": "The outer-isolation entry names no broader credentials or channels to close, such as personal tokens or metadata endpoints. It only lists the rule id.",
          "result": "fail",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md lines 7-9",
          "reason": "Each control is marked 'recommended, not verified... availability unknown', so the recommendation does not claim the control is enforced on the user's plan.",
          "result": "pass",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md lines 5-9",
          "reason": "No recommendation tells the user to re-check the control configuration periodically.",
          "result": "fail",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md line 7",
          "reason": "'codeowners-agent-config' is named, but the README gives no CODEOWNERS entry for the agent's configuration files (e.g. .agents/) and does not mention the setting that requires code-owner review.",
          "result": "fail",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "SKILL.md lines 87-89",
          "reason": "The agent opens no pull requests in this skill. It only returns a checklist and forbids posting or writing it elsewhere.",
          "result": "not-applicable",
          "rule_id": "outside.merge.rule-for-agent-prs"
        },
        {
          "check": "judged",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.reuse.reviewed-and-pinned"
        }
      ],
      "status": "built"
    }
  ],
  "revision_digest": "fb67de3f6a2a7c750204d87f62f3c26fcf0646f53562bb594396b495eea19e25",
  "rules_digest": "d57f742e2e061ef35e3497be96cb6e20e1782272b44da47b59abacba8d164e54",
  "run_id": "713d699f-verify-a-4",
  "runtime_results": [
    {
      "case_id": "repro-explicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: Skill, Read, Bash, Glob, Grep; network: none requested; bug-report.md sha256 6a391585dd84ed8909d13c924dc19e4cc7444a92bbe7e06e773902e9bad442ac",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/repro-checklist/SKILL.md": "0bb1a838d12c534099cf7d7927cce508ffb98b193287c4e7efc659c2f6bb31a8",
        ".agents/skills/repro-checklist/references/requirements.md": "e18797951df45df71f8689db7f208c77c397781955b519a700438ad553bf1b5f"
      },
      "harness": "claude-code",
      "harness_version": "2.1.296 (Claude Code)",
      "observed_activation": "Skill tool called for repro-checklist",
      "part_id": "A",
      "prompt": "Use the repro-checklist skill on the bug report in bug-report.md and give me the checklist.",
      "reason": "Skill tool called for repro-checklist",
      "result": "pass",
      "run_id": "713d699f-verify-a-4"
    },
    {
      "case_id": "repro-implicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: Skill, Read, Bash, Glob, Grep; network: none requested; bug-report.md sha256 6a391585dd84ed8909d13c924dc19e4cc7444a92bbe7e06e773902e9bad442ac",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/repro-checklist/SKILL.md": "0bb1a838d12c534099cf7d7927cce508ffb98b193287c4e7efc659c2f6bb31a8",
        ".agents/skills/repro-checklist/references/requirements.md": "e18797951df45df71f8689db7f208c77c397781955b519a700438ad553bf1b5f"
      },
      "harness": "claude-code",
      "harness_version": "2.1.296 (Claude Code)",
      "observed_activation": "Skill tool called for repro-checklist",
      "part_id": "A",
      "prompt": "The bug report in bug-report.md has no reproduction steps yet. Work out exactly how someone can reproduce it.",
      "reason": "Skill tool called for repro-checklist",
      "result": "pass",
      "run_id": "713d699f-verify-a-4"
    },
    {
      "case_id": "repro-near-miss",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: Skill, Read, Bash, Glob, Grep; network: none requested; bug-report.md sha256 6a391585dd84ed8909d13c924dc19e4cc7444a92bbe7e06e773902e9bad442ac",
      "expected": "does-not-activate",
      "file_hashes": {
        ".agents/skills/repro-checklist/SKILL.md": "0bb1a838d12c534099cf7d7927cce508ffb98b193287c4e7efc659c2f6bb31a8",
        ".agents/skills/repro-checklist/references/requirements.md": "e18797951df45df71f8689db7f208c77c397781955b519a700438ad553bf1b5f"
      },
      "harness": "claude-code",
      "harness_version": "2.1.296 (Claude Code)",
      "observed_activation": null,
      "part_id": "A",
      "prompt": "Summarize in two sentences what the bug report in bug-report.md is about; I do not need reproduction steps.",
      "reason": "no Skill tool call for the candidate",
      "result": "pass",
      "run_id": "713d699f-verify-a-4"
    }
  ],
  "scope": "Extensive review (rarely needed)",
  "symlinks": {
    ".claude/skills/repro-checklist": "../../.agents/skills/repro-checklist"
  },
  "tool_versions": {
    "harness-forge-checkers": "49d1dc3feb234903cb74e7ea22c79bd3e66bea53f90e2c85a2ba30f091cdcd1c"
  },
  "whole_idea": {
    "facts": {
      "bypass_mode": true,
      "lethal_trifecta": true,
      "opens_prs": true,
      "plan_controls": "unknown",
      "reach": "public",
      "target_set": "both",
      "untrusted_repo": true
    },
    "hosting": {
      "plan": "any",
      "platform": "any (platform-agnostic)",
      "visibility": "unknown"
    },
    "reach": "public",
    "targets": [
      "claude-code",
      "codex"
    ]
  },
  "worker_evidence": [
    {
      "configuration_digest": "8f829a4997165574f012341c9cfd6babd3d9105bc9c559508d67a78b3ae277ea",
      "configured_controls": [
        "command: [\"claude\", \"--print\", \"--output-format\", \"stream-json\", \"--verbose\", \"--no-session-persistence\", \"--safe-mode\", \"--restricted\", \"--setting-sources\", \"\", \"--strict-mcp-config\", \"--mcp-config\", \"{\\\"mcpServers\\\":{}}\", \"--disable-slash-commands\", \"--permission-mode\", \"dontAsk\", \"--permission-prompts\", \"none\", \"--settings\", \"{\\\"disableAllHooks\\\":true,\\\"autoMemoryEnabled\\\":false}\", \"--tools\", \"WebFetch,WebSearch\", \"--allowedTools\", \"WebFetch,WebSearch\", \"--json-schema\", \"{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"findings\\\":{\\\"type\\\":\\\"array\\\",\\\"items\\\":{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"claim\\\":{\\\"type\\\":\\\"string\\\"},\\\"source\\\":{\\\"type\\\":\\\"string\\\"},\\\"fetched\\\":{\\\"type\\\":\\\"string\\\"},\\\"quote\\\":{\\\"type\\\":\\\"string\\\"},\\\"context\\\":{\\\"type\\\":\\\"string\\\"},\\\"source_role\\\":{\\\"enum\\\":[\\\"primary\\\",\\\"practitioner\\\",\\\"trade-press\\\"]}},\\\"required\\\":[\\\"claim\\\",\\\"source\\\",\\\"fetched\\\",\\\"quote\\\",\\\"context\\\",\\\"source_role\\\"],\\\"additionalProperties\\\":false}}},\\\"required\\\":[\\\"findings\\\"],\\\"additionalProperties\\\":false}\"]",
        "environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER",
        "login: subscription (claude.ai)"
      ],
      "evidence_refs": [],
      "harness": "claude-code",
      "harness_version": "2.1.296 (Claude Code)",
      "isolation_status": "not-certified",
      "launcher": "independent-process",
      "model": "account default",
      "observed_behavior": [],
      "observed_tools": {
        "status": "unknown"
      },
      "role": "research",
      "unknowns": [
        "context, file and network isolation are not certified",
        "not every tool-registration path is observable"
      ],
      "worker_policy": "best-effort-v1"
    },
    {
      "configuration_digest": "f79908e2f8761717b26bb5d87aed5c56e135ba70a0edb97e404129d59e06e708",
      "configured_controls": [
        "command: [\"claude\", \"--print\", \"--output-format\", \"stream-json\", \"--verbose\", \"--no-session-persistence\", \"--safe-mode\", \"--restricted\", \"--setting-sources\", \"\", \"--strict-mcp-config\", \"--mcp-config\", \"{\\\"mcpServers\\\":{}}\", \"--disable-slash-commands\", \"--permission-mode\", \"dontAsk\", \"--permission-prompts\", \"none\", \"--settings\", \"{\\\"disableAllHooks\\\":true,\\\"autoMemoryEnabled\\\":false}\", \"--tools\", \"\", \"--allowedTools\", \"\", \"--json-schema\", \"{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"verdicts\\\":{\\\"type\\\":\\\"array\\\",\\\"items\\\":{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"finding_id\\\":{\\\"type\\\":\\\"string\\\"},\\\"verdict\\\":{\\\"enum\\\":[\\\"supported\\\",\\\"unsupported\\\"]},\\\"reasoning\\\":{\\\"type\\\":\\\"string\\\"}},\\\"required\\\":[\\\"finding_id\\\",\\\"verdict\\\",\\\"reasoning\\\"],\\\"additionalProperties\\\":false}}},\\\"required\\\":[\\\"verdicts\\\"],\\\"additionalProperties\\\":false}\"]",
        "environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER",
        "login: subscription (claude.ai)"
      ],
      "evidence_refs": [],
      "harness": "claude-code",
      "harness_version": "2.1.296 (Claude Code)",
      "isolation_status": "not-certified",
      "launcher": "independent-process",
      "model": "account default",
      "observed_behavior": [],
      "observed_tools": {
        "status": "unknown"
      },
      "role": "source-support",
      "unknowns": [
        "context, file and network isolation are not certified",
        "not every tool-registration path is observable"
      ],
      "worker_policy": "best-effort-v1"
    },
    {
      "configuration_digest": "bd41806234b54333f0b42bf98e08945ea9756a175b212e92e0435a771b2beb3f",
      "configured_controls": [
        "command: [\"claude\", \"--print\", \"--output-format\", \"stream-json\", \"--verbose\", \"--no-session-persistence\", \"--safe-mode\", \"--restricted\", \"--setting-sources\", \"\", \"--strict-mcp-config\", \"--mcp-config\", \"{\\\"mcpServers\\\":{}}\", \"--disable-slash-commands\", \"--permission-mode\", \"dontAsk\", \"--permission-prompts\", \"none\", \"--settings\", \"{\\\"disableAllHooks\\\":true,\\\"autoMemoryEnabled\\\":false}\", \"--tools\", \"Read,Grep,Glob\", \"--allowedTools\", \"Read,Grep,Glob\", \"--json-schema\", \"{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"run_id\\\":{\\\"type\\\":\\\"string\\\"},\\\"verdicts\\\":{\\\"type\\\":\\\"array\\\",\\\"items\\\":{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"part_id\\\":{\\\"type\\\":\\\"string\\\"},\\\"rule_id\\\":{\\\"type\\\":\\\"string\\\"},\\\"verdict\\\":{\\\"enum\\\":[\\\"pass\\\",\\\"fail\\\",\\\"not-applicable\\\"]},\\\"reason\\\":{\\\"type\\\":\\\"string\\\"},\\\"citation\\\":{\\\"type\\\":\\\"string\\\"}},\\\"required\\\":[\\\"part_id\\\",\\\"rule_id\\\",\\\"verdict\\\",\\\"reason\\\",\\\"citation\\\"],\\\"additionalProperties\\\":false}},\\\"goal_verdicts\\\":{\\\"type\\\":\\\"array\\\",\\\"items\\\":{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"part_id\\\":{\\\"type\\\":\\\"string\\\"},\\\"verdict\\\":{\\\"enum\\\":[\\\"met\\\",\\\"not-met\\\"]},\\\"reason\\\":{\\\"type\\\":\\\"string\\\"}},\\\"required\\\":[\\\"part_id\\\",\\\"verdict\\\",\\\"reason\\\"],\\\"additionalProperties\\\":false}}},\\\"required\\\":[\\\"run_id\\\",\\\"verdicts\\\",\\\"goal_verdicts\\\"],\\\"additionalProperties\\\":false}\"]",
        "environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER",
        "login: subscription (claude.ai)"
      ],
      "evidence_refs": [],
      "harness": "claude-code",
      "harness_version": "2.1.296 (Claude Code)",
      "isolation_status": "not-certified",
      "launcher": "independent-process",
      "model": "account default",
      "observed_behavior": [],
      "observed_tools": {
        "status": "unknown"
      },
      "role": "review",
      "unknowns": [
        "context, file and network isolation are not certified",
        "not every tool-registration path is observable"
      ],
      "worker_policy": "best-effort-v1"
    },
    {
      "configuration_digest": "bd41806234b54333f0b42bf98e08945ea9756a175b212e92e0435a771b2beb3f",
      "configured_controls": [
        "command: [\"claude\", \"--print\", \"--output-format\", \"stream-json\", \"--verbose\", \"--no-session-persistence\", \"--safe-mode\", \"--restricted\", \"--setting-sources\", \"\", \"--strict-mcp-config\", \"--mcp-config\", \"{\\\"mcpServers\\\":{}}\", \"--disable-slash-commands\", \"--permission-mode\", \"dontAsk\", \"--permission-prompts\", \"none\", \"--settings\", \"{\\\"disableAllHooks\\\":true,\\\"autoMemoryEnabled\\\":false}\", \"--tools\", \"Read,Grep,Glob\", \"--allowedTools\", \"Read,Grep,Glob\", \"--json-schema\", \"{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"run_id\\\":{\\\"type\\\":\\\"string\\\"},\\\"verdicts\\\":{\\\"type\\\":\\\"array\\\",\\\"items\\\":{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"part_id\\\":{\\\"type\\\":\\\"string\\\"},\\\"rule_id\\\":{\\\"type\\\":\\\"string\\\"},\\\"verdict\\\":{\\\"enum\\\":[\\\"pass\\\",\\\"fail\\\",\\\"not-applicable\\\"]},\\\"reason\\\":{\\\"type\\\":\\\"string\\\"},\\\"citation\\\":{\\\"type\\\":\\\"string\\\"}},\\\"required\\\":[\\\"part_id\\\",\\\"rule_id\\\",\\\"verdict\\\",\\\"reason\\\",\\\"citation\\\"],\\\"additionalProperties\\\":false}},\\\"goal_verdicts\\\":{\\\"type\\\":\\\"array\\\",\\\"items\\\":{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"part_id\\\":{\\\"type\\\":\\\"string\\\"},\\\"verdict\\\":{\\\"enum\\\":[\\\"met\\\",\\\"not-met\\\"]},\\\"reason\\\":{\\\"type\\\":\\\"string\\\"}},\\\"required\\\":[\\\"part_id\\\",\\\"verdict\\\",\\\"reason\\\"],\\\"additionalProperties\\\":false}}},\\\"required\\\":[\\\"run_id\\\",\\\"verdicts\\\",\\\"goal_verdicts\\\"],\\\"additionalProperties\\\":false}\"]",
        "environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER",
        "login: subscription (claude.ai)"
      ],
      "evidence_refs": [],
      "harness": "claude-code",
      "harness_version": "2.1.296 (Claude Code)",
      "isolation_status": "not-certified",
      "launcher": "independent-process",
      "model": "account default",
      "observed_behavior": [
        "model reported: claude-opus-5-5",
        "apiKeySource: none",
        "skills listed: ",
        "plugins listed: cc-plugin-agents-md (builtin), cc-plugin-plugin-authoring (builtin), cc-plugin-telemetry (builtin)"
      ],
      "observed_tools": {
        "status": "observed",
        "tools": [
          "Glob",
          "Grep",
          "Read",
          "StructuredOutput"
        ]
      },
      "role": "review",
      "unknowns": [
        "context, file and network isolation are not certified",
        "not every tool-registration path is observable"
      ],
      "worker_policy": "best-effort-v1"
    }
  ],
  "worker_violations": []
}
```
