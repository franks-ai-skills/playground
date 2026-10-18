# Verification report

- Run: `78cd85df-fce7-4e2d-a70a-185a616379f0`
- Harness KB version: 0.1.0
- Contract digest: 1aca09f6e1858d262e090a9202425c1d4e84904834b83c048aee345e274784ae
- Confirmed parts: A, B, C, D, E, F, G
- Decision record digest: a8fd69b94b43a23ee3aaf81944c247decb355763b04306d9453decb00c104e61
- Whole-idea answers and targets: `{"facts": {"lethal_trifecta": true, "opens_prs": true, "plan_controls": "available", "reach": "public", "target_set": "both", "untrusted_repo": true}, "hosting": {"plan": "free (assumed; the repositories it runs in vary)", "platform": "github", "visibility": "public"}, "reach": "public", "targets": ["claude-code", "codex"]}` (digest 39333c05d327aa7d3a809a95990b6c92a08e3b6ea12bb192c3d34a902598aed7)
- Rule content digest: 93fec41536adbe0420026720fecbe03465b27f5f457695dc9d5704d422d7488a
- Accepted Idea KB revision: e1805692c07794fb076d85404a8ce1d99581b7ad56af5cabea3935af53c2acde
- Review scope: First run: judged A, B, C, D, E, F, G
- Rule overrides: none
- Checker versions digest: 7beeb29d229339f59695dccf5877b0efc53a7e117ff8fb0b7773c93c0d92e0df

## Worker isolation

Workers ran under `best-effort-v1` with isolation status `not-certified`. Research, source-support and review workers run as independent CLI processes with explicit role inputs and the available restrictions. Complete tool absence and context, file and network isolation are not guaranteed; use trusted projects and operator-approved inputs.

- research worker: claude-code 2.1.302 (Claude Code), model account default, launcher independent-process, configuration 8f829a4997165574f012341c9cfd6babd3d9105bc9c559508d67a78b3ae277ea, controls: command: ["claude", "--print", "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--safe-mode", "--restricted", "--setting-sources", "", "--strict-mcp-config", "--mcp-config", "{\"mcpServers\":{}}", "--disable-slash-commands", "--permission-mode", "dontAsk", "--permission-prompts", "none", "--settings", "{\"disableAllHooks\":true,\"autoMemoryEnabled\":false}", "--tools", "WebFetch,WebSearch", "--allowedTools", "WebFetch,WebSearch", "--json-schema", "{\"type\":\"object\",\"properties\":{\"findings\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"claim\":{\"type\":\"string\"},\"source\":{\"type\":\"string\"},\"fetched\":{\"type\":\"string\"},\"quote\":{\"type\":\"string\"},\"context\":{\"type\":\"string\"},\"source_role\":{\"enum\":[\"primary\",\"practitioner\",\"trade-press\"]}},\"required\":[\"claim\",\"source\",\"fetched\",\"quote\",\"context\",\"source_role\"],\"additionalProperties\":false}}},\"required\":[\"findings\"],\"additionalProperties\":false}"]; environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (claude.ai), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- source-support worker: claude-code 2.1.302 (Claude Code), model account default, launcher independent-process, configuration f79908e2f8761717b26bb5d87aed5c56e135ba70a0edb97e404129d59e06e708, controls: command: ["claude", "--print", "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--safe-mode", "--restricted", "--setting-sources", "", "--strict-mcp-config", "--mcp-config", "{\"mcpServers\":{}}", "--disable-slash-commands", "--permission-mode", "dontAsk", "--permission-prompts", "none", "--settings", "{\"disableAllHooks\":true,\"autoMemoryEnabled\":false}", "--tools", "", "--allowedTools", "", "--json-schema", "{\"type\":\"object\",\"properties\":{\"verdicts\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"finding_id\":{\"type\":\"string\"},\"verdict\":{\"enum\":[\"supported\",\"unsupported\"]},\"reasoning\":{\"type\":\"string\"}},\"required\":[\"finding_id\",\"verdict\",\"reasoning\"],\"additionalProperties\":false}}},\"required\":[\"verdicts\"],\"additionalProperties\":false}"]; environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (claude.ai), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- review worker: claude-code 2.1.302 (Claude Code), model account default, launcher independent-process, configuration bd41806234b54333f0b42bf98e08945ea9756a175b212e92e0435a771b2beb3f, controls: command: ["claude", "--print", "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--safe-mode", "--restricted", "--setting-sources", "", "--strict-mcp-config", "--mcp-config", "{\"mcpServers\":{}}", "--disable-slash-commands", "--permission-mode", "dontAsk", "--permission-prompts", "none", "--settings", "{\"disableAllHooks\":true,\"autoMemoryEnabled\":false}", "--tools", "Read,Grep,Glob", "--allowedTools", "Read,Grep,Glob", "--json-schema", "{\"type\":\"object\",\"properties\":{\"run_id\":{\"type\":\"string\"},\"verdicts\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"part_id\":{\"type\":\"string\"},\"rule_id\":{\"type\":\"string\"},\"verdict\":{\"enum\":[\"pass\",\"fail\",\"not-applicable\"]},\"reason\":{\"type\":\"string\"},\"citation\":{\"type\":\"string\"}},\"required\":[\"part_id\",\"rule_id\",\"verdict\",\"reason\",\"citation\"],\"additionalProperties\":false}},\"goal_verdicts\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"part_id\":{\"type\":\"string\"},\"verdict\":{\"enum\":[\"met\",\"not-met\"]},\"reason\":{\"type\":\"string\"}},\"required\":[\"part_id\",\"verdict\",\"reason\"],\"additionalProperties\":false}}},\"required\":[\"run_id\",\"verdicts\",\"goal_verdicts\"],\"additionalProperties\":false}"]; environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (claude.ai), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- review worker: claude-code 2.1.302 (Claude Code), model account default, launcher independent-process, configuration bd41806234b54333f0b42bf98e08945ea9756a175b212e92e0435a771b2beb3f, controls: command: ["claude", "--print", "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--safe-mode", "--restricted", "--setting-sources", "", "--strict-mcp-config", "--mcp-config", "{\"mcpServers\":{}}", "--disable-slash-commands", "--permission-mode", "dontAsk", "--permission-prompts", "none", "--settings", "{\"disableAllHooks\":true,\"autoMemoryEnabled\":false}", "--tools", "Read,Grep,Glob", "--allowedTools", "Read,Grep,Glob", "--json-schema", "{\"type\":\"object\",\"properties\":{\"run_id\":{\"type\":\"string\"},\"verdicts\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"part_id\":{\"type\":\"string\"},\"rule_id\":{\"type\":\"string\"},\"verdict\":{\"enum\":[\"pass\",\"fail\",\"not-applicable\"]},\"reason\":{\"type\":\"string\"},\"citation\":{\"type\":\"string\"}},\"required\":[\"part_id\",\"rule_id\",\"verdict\",\"reason\",\"citation\"],\"additionalProperties\":false}},\"goal_verdicts\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"part_id\":{\"type\":\"string\"},\"verdict\":{\"enum\":[\"met\",\"not-met\"]},\"reason\":{\"type\":\"string\"}},\"required\":[\"part_id\",\"verdict\",\"reason\"],\"additionalProperties\":false}}},\"required\":[\"run_id\",\"verdicts\",\"goal_verdicts\"],\"additionalProperties\":false}"]; environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (claude.ai), observed tools: Glob, Grep, Read, StructuredOutput, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable

## Part A

- Harness result: not applicable
- Goal result: not assessed
- Status: blocked
- Outside dependencies: compromise-resistant-gate
- Confirmed answers: `{"event_without_agent": false, "every_time": "always", "hook_effect": "prevent", "hook_event": "PreToolUse", "irreversible": true, "job": "procedure", "must_survive_compromise": "not-required", "own_context": false, "script_checkable": true, "who_disables": "contributor"}`

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `outside.ci.required-on-ref` | warning | judged | fail | Part A's gates depend on workflow-defined checks (see the workflow-protected condition), but no part A recommendation says a CI check counts as a gate only when it is required on the protected ref. | README.md:5-26 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | No part A recommendation requires pinning the sources the gate's checks run, such as actions or scanners. Only workflow files from outside the repository are mentioned as pinned. | README.md:5-26 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | codeowners-agent-config and compromise-resistant-gate both include the workflow-protected condition, including that CODEOWNERS owns itself. | README.md:6,11 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | A CODEOWNERS entry is recommended for .agents/, .claude/, .codex/, AGENTS.md, the workflows and CODEOWNERS itself, together with required code-owner review. | README.md:7 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | pass | compromise-resistant-gate and outer-isolation both carry the no-broader-bypass condition. | README.md:12,24 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Every control for part A says to check its configuration periodically. | README.md:9,13,18,26 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | pass | The plan-enforced condition is stated, and availability is given as available. | README.md:14,19 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Every control recommended for part A carries the real-refs condition. | README.md:8,15,20,25 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | pass | compromise-resistant-gate and merge-rules both require that the agent's identity is on no bypass list. | README.md:16,21 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | pass | merge-rules for part A requires approval from a different identity that resets on new pushes. | README.md:22 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | pass | merge-rules is recommended for part A. | README.md:17-22 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 4 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |

## Part B

- Harness result: not verified
- Goal result: not met
- Status: built
- Outside dependencies: none
- Confirmed answers: `{"event_without_agent": false, "every_time": "usually", "irreversible": false, "job": "procedure", "must_survive_compromise": "not-required", "own_context": false, "trigger": "model", "who_disables": "contributor"}`
- Goal verdict: met (The reproduce skill runs fresh repeated reproductions, posts exact numbered steps, observed and expected results, a run tally and a consistent, intermittent or not-reproduced verdict to the issue, and covers all six accepted requirements.)

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `idea.bug-intake.b.consistency-statement` | error | judged | pass | The verdict is consistent, intermittent with a count, or not reproduced, and it goes into the issue. | .agents/skills/reproduce/SKILL.md:25-28,33 | https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html, https://firefox-source-docs.mozilla.org/testing/test-verification/index.html |
| `idea.bug-intake.b.exact-steps` | error | judged | pass | The skill requires numbered, exact steps and puts them in the issue comment. | .agents/skills/reproduce/SKILL.md:22,31 | https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html |
| `idea.bug-intake.b.facts-vs-speculation` | warning | judged | pass | Observations are kept separate from a "Possible cause (unverified)" section. | .agents/skills/reproduce/SKILL.md:34 | https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html |
| `idea.bug-intake.b.observed-expected` | warning | judged | pass | Observed and Expected results, each precise, come after the steps. | .agents/skills/reproduce/SKILL.md:31-32 | https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html |
| `idea.bug-intake.b.order-dependency` | warning | judged | pass | When runs disagree, the skill runs the reproduction alone, together with related tests, and in a different order. | .agents/skills/reproduce/SKILL.md:24 | https://firefox-source-docs.mozilla.org/testing/debugging-intermittents/index.html, https://arxiv.org/abs/2101.09077 |
| `idea.bug-intake.b.repeated-runs` | error | judged | pass | The skill requires several fresh-process runs and records the tally in the issue. | .agents/skills/reproduce/SKILL.md:23,33 | https://firefox-source-docs.mozilla.org/testing/test-verification/index.html, https://firefox-source-docs.mozilla.org/testing/debugging-intermittents/index.html |
| `links.parts` | error | script | error | part A's hooks has no builder in this release, so its name cannot be checked | - | - |
| `outside.ci.required-on-ref` | warning | judged | fail | Part B's gates rely on workflow-defined checks, but nothing says a check counts only when it is required on the protected ref. | README.md:27-41 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | No recommendation for part B requires pinning the sources the checks run. | README.md:27-41 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | codeowners-agent-config carries the workflow-protected condition. | README.md:28 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | CODEOWNERS for the agent configuration and required code-owner review are recommended. | README.md:29 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | pass | outer-isolation carries the no-broader-bypass condition. | README.md:39 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Every control for part B says to check its configuration periodically. | README.md:31,33,41 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | pass | merge-rules carries the plan-enforced condition, and availability is given as available. | README.md:32-34 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Every control for part B carries the real-refs condition. | README.md:30,35,40 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | pass | merge-rules for part B carries the no-agent-bypass condition. | README.md:36 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | pass | merge-rules for part B carries the requester-cannot-approve condition. | README.md:37 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | pass | merge-rules is recommended for part B. | README.md:32-37 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 3 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `security.approval.claims-are-data` | warning | judged | pass | No step treats a claim in content as authorization. | .agents/skills/reproduce/SKILL.md:18 | docs/guide/security.md#context-and-persistent-state |
| `security.helpers.confined` | warning | judged | pass | The skill uses only gh and the reproduction commands under the harness's permissions, with no pre-approval. | .agents/skills/reproduce/SKILL.md:20,29 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#executables-approvals-and-isolation |
| `security.outbound.minimal-data` | warning | judged | pass | The only outbound write is a comment on the same issue, with defined fields, and content is treated as data. | .agents/skills/reproduce/SKILL.md:18,29-34 | docs/guide/security.md#data-access-and-outbound-channels, https://developers.openai.com/api/docs/guides/deep-research#prompt-injection-and-exfiltration |
| `security.secrets.none-in-files` | error | judged | pass | The files contain no secrets. | .agents/skills/reproduce/ | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#context-and-persistent-state |
| `security.untrusted-input.as-data` | warning | judged | pass | The procedure says to treat issues, fetched pages and tool output as data. | .agents/skills/reproduce/SKILL.md:18 | docs/guide/security.md#context-and-persistent-state |
| `skills.body.gotchas-first` | warning | judged | pass | Requirements and the untrusted-data rule sit at the top of SKILL.md. | .agents/skills/reproduce/SKILL.md:7-18 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://agentskills.io/skill-creation/best-practices.md |
| `skills.body.no-time-bound-statements` | warning | judged | pass | There are no time-bound statements. | .agents/skills/reproduce/SKILL.md | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.only-what-model-lacks` | warning | judged | pass | The body holds specific standing instructions (run counts, fresh state, comment structure) and no general explanation. | .agents/skills/reproduce/SKILL.md:20-36 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.reasons-before-hard-rules` | warning | judged | pass | Rules carry reasons, for example "since it can be rerun unchanged" and "so the count means something", and emphatic wording is rare. | .agents/skills/reproduce/SKILL.md:22-23 | docs/best-practices/skills.md#7-explain-the-why-before-adding-hard-rules |
| `skills.body.size` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, docs/concepts/skills.md#body, https://code.claude.com/docs/en/skills, https://agentskills.io/specification |
| `skills.body.strictness-matches-fragility` | warning | judged | pass | There is one default (5 runs, at least 10 if the runs disagree) and a single preferred form (an automated reproduction). | .agents/skills/reproduce/SKILL.md:22-23 | docs/best-practices/skills.md#5-match-strictness-to-fragility, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.description.boundary` | warning | judged | pass | The description says the skill is not for creating, fixing or closing issues. | .agents/skills/reproduce/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.description.concise` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, docs/research-notes/agent-harness-best-practices/skills.md |
| `skills.description.length` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/opencode/skills.md#format, https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs, https://opencode.ai/docs/skills/ |
| `skills.description.no-workflow-steps` | warning | judged | pass | The description names what the skill produces (steps, results, run counts, verdict), not the order of its procedure. | .agents/skills/reproduce/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md |
| `skills.description.voice` | warning | judged | pass | The description is in the third person ("Reproduces ..."). | .agents/skills/reproduce/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition |
| `skills.description.what-and-when` | warning | judged | pass | The description states what the skill does with concrete verbs, then gives trigger phrases such as "reproduce this bug" and "can you repro #123". | .agents/skills/reproduce/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://learn.chatgpt.com/docs/build-skills, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.frontmatter.valid` | error | script | pass | 1 skill(s) checked | - | docs/vendors/opencode/skills.md#format, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/claude-code/skills.md#format, docs/concepts/skills.md#frontmatter, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.goal.no-must-hold-rule-in-skill` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#13-move-rules-that-must-hold-every-time-into-hooks, https://code.claude.com/docs/en/skills |
| `skills.inputs.from-message` | warning | judged | fail | The skill reads the issue from the user's message but does not say to ask when the issue number or URL is missing. | .agents/skills/reproduce/SKILL.md:20 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, docs/concepts/skills.md#body |
| `skills.invocation.both-flags` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#invocation-policy-in-both-leads, docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.invocation.side-effects-user-invoked` | error | judged | fail | The skill posts a comment to a GitHub issue, which changes external state, yet it is model-invocable in both harnesses: there is no disable-model-invocation and no agents/openai.yaml. | .agents/skills/reproduce/SKILL.md:1-4,29 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.name.format` | error | script | pass | 1 skill(s) checked | - | docs/guide/skills.md#portability, docs/concepts/skills.md#frontmatter, docs/vendors/opencode/skills.md#format, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.package.no-auxiliary-docs` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#anti-patterns, https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md |
| `skills.portable.frontmatter` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/best-practices/skills.md#12-keep-one-canonical-copy-with-portable-frontmatter, https://code.claude.com/docs/en/skills |
| `skills.portable.layout` | error | script | pass | 1 skill(s) linked | - | docs/concepts/skills.md#directory-layout, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.portable.no-claude-placeholders` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#body, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills |
| `skills.portable.plugin-layout` | error | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#directory-layout, docs/vendors/claude-code/plugins.md#standard-layout, docs/vendors/codex/plugins.md#plugin-layout, https://code.claude.com/docs/en/plugins/manifest-reference, https://developers.openai.com/codex/plugins/build |
| `skills.references.load-conditions` | warning | judged | pass | The reference file is named with its load condition and holds only rule ids and sources. | .agents/skills/reproduce/SKILL.md:38-39 | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/best-practices.md |
| `skills.references.one-level` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/specification |
| `skills.references.resolve` | error | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.reuse.reviewed-and-pinned` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#security, https://owasp.github.io/www-project-agentic-skills-top-10/ast01 |
| `skills.scope.committed-for-automation` | warning | judged | pass | The skill is committed in project scope under .agents/skills, with a .claude/skills link. | links: .claude/skills/reproduce | docs/concepts/skills.md#directory-layout, https://code.claude.com/docs/en/skills |
| `skills.scripts.agent-caller` | warning | judged | not-applicable | The skill bundles no scripts. | .agents/skills/reproduce/ | docs/best-practices/skills.md#6-put-deterministic-logic-in-tested-scripts, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/using-scripts.md |
| `skills.security.allowed-tools-least-privilege` | warning | judged | not-applicable | The frontmatter declares no allowed-tools. | .agents/skills/reproduce/SKILL.md:1-4 | docs/best-practices/skills.md#security, docs/vendors/claude-code/skills.md#limits-and-gotchas, https://code.claude.com/docs/en/skills |
| `skills.security.no-surprising-content` | error | judged | pass | There is no hidden directive, remote fetch-and-run or credential access. | .agents/skills/reproduce/SKILL.md | docs/best-practices/skills.md#security, https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md |

Contested `skills.body.reasons-before-hard-rules`:
- All-caps ALWAYS or NEVER is a yellow flag; explain the reasoning instead (https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md, https://agentskills.io/skill-creation/evaluating-skills.md)
- Discipline skills need firm prohibitions and rationalization tables (https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

Contested `skills.description.voice`:
- Always write in the third person; an inconsistent point of view can cause discovery problems (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Use imperative "Use this skill when" phrasing for the trigger (https://agentskills.io/skill-creation/optimizing-descriptions.md, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)

## Part C

- Harness result: not verified
- Goal result: not met
- Status: built
- Outside dependencies: compromise-resistant-gate
- Confirmed answers: `{"event_without_agent": false, "every_time": "usually", "irreversible": true, "job": "procedure", "must_survive_compromise": "not-required", "own_context": false, "trigger": "user", "who_disables": "contributor"}`
- Goal verdict: met (fix-and-pr creates a fix branch from the default branch, adds a regression test, opens a PR with Fixes #N, fixes CI at the cause without workarounds or pwn-request changes, never merges, and reports ready only when all required checks are green.)

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `idea.bug-intake.c.ci-workaround` | error | judged | pass | Skipping, weakening or deleting tests and changing CI are explicitly forbidden. | .agents/skills/fix-and-pr/SKILL.md:26-31 | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches |
| `idea.bug-intake.c.closing-keyword` | error | judged | pass | The PR targets the default branch with "Fixes #<number>". For another branch it uses "Related to" and tells the user. | .agents/skills/fix-and-pr/SKILL.md:25 | https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue |
| `idea.bug-intake.c.green-before-done` | error | judged | pass | The PR is reported ready only when every required check has passed; otherwise the failing checks are listed. | .agents/skills/fix-and-pr/SKILL.md:32 | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches |
| `idea.bug-intake.c.pwn-request` | error | judged | pass | Combining pull_request_target with a checkout of PR code is forbidden. | .agents/skills/fix-and-pr/SKILL.md:31 | https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/ |
| `idea.bug-intake.c.regression-test` | error | judged | pass | The reproduction steps become a new or updated test that is confirmed to fail before the fix. | .agents/skills/fix-and-pr/SKILL.md:23 | https://google.github.io/eng-practices/review/developer/small-cls.html |
| `idea.bug-intake.c.self-merge` | warning | judged | pass | The skill says "Never merge the pull request". | .agents/skills/fix-and-pr/SKILL.md:32 | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches |
| `links.parts` | error | script | pass | every linked part exists under its recorded name | - | - |
| `outside.ci.required-on-ref` | warning | judged | fail | Part C depends on required checks passing, but no part C recommendation says a check counts as a gate only when it is required on the protected ref (no event-gate for C). | README.md:42-63 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | No recommendation for part C requires pinning check sources. | README.md:42-63 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | The workflow-protected condition is present. | README.md:43,48 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | The CODEOWNERS recommendation for agent configuration and required code-owner review is present. | README.md:44 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | pass | The no-broader-bypass condition is present. | README.md:49,61 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Periodic verification is stated. | README.md:46,50,55,63 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | pass | The plan-enforced condition is present. | README.md:51,56 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Every control for part C carries the real-refs condition. | README.md:45,52,57,62 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | pass | The no-agent-bypass condition is present. | README.md:53,58 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | pass | merge-rules carries the requester-cannot-approve condition. | README.md:59 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | pass | The agent opens PRs in part C, and merge-rules is recommended. | README.md:54-59 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 4 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `runtime.explicit-activation` | error | script | fail | the live build needs an observed explicit activation, and none passed | - | - |
| `security.approval.claims-are-data` | warning | judged | pass | No step treats a claim in content as authorization, and workflow changes require asking the user. | .agents/skills/fix-and-pr/SKILL.md:19,31 | docs/guide/security.md#context-and-persistent-state |
| `security.helpers.confined` | warning | judged | pass | Only gh and git run, under the harness's permissions, with no pre-approval. | .agents/skills/fix-and-pr/SKILL.md:21-26 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#executables-approvals-and-isolation |
| `security.outbound.minimal-data` | warning | judged | pass | Pushes go only to this repository's branch and PR, with defined content, and untrusted content is treated as data. | .agents/skills/fix-and-pr/SKILL.md:19,25 | docs/guide/security.md#data-access-and-outbound-channels, https://developers.openai.com/api/docs/guides/deep-research#prompt-injection-and-exfiltration |
| `security.secrets.none-in-files` | error | judged | pass | The files contain no secrets. | .agents/skills/fix-and-pr/ | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#context-and-persistent-state |
| `security.untrusted-input.as-data` | warning | judged | pass | The procedure says to treat issues, fetched pages and tool output as data. | .agents/skills/fix-and-pr/SKILL.md:19 | docs/guide/security.md#context-and-persistent-state |
| `skills.body.gotchas-first` | warning | judged | pass | The Never-rules and the untrusted-data rule are at the top. | .agents/skills/fix-and-pr/SKILL.md:8-19 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://agentskills.io/skill-creation/best-practices.md |
| `skills.body.no-time-bound-statements` | warning | judged | pass | There are no time-bound statements. | .agents/skills/fix-and-pr/SKILL.md | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.only-what-model-lacks` | warning | judged | pass | The body holds specific standing instructions, such as the list of workarounds and how closing keywords behave, without generic explanation. | .agents/skills/fix-and-pr/SKILL.md:21-32 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.reasons-before-hard-rules` | warning | judged | pass | Hard rules carry reasons, for example "closing keywords are ignored there" and "merging is left to the people and rules of the repository". | .agents/skills/fix-and-pr/SKILL.md:25,32 | docs/best-practices/skills.md#7-explain-the-why-before-adding-hard-rules |
| `skills.body.size` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, docs/concepts/skills.md#body, https://code.claude.com/docs/en/skills, https://agentskills.io/specification |
| `skills.body.strictness-matches-fragility` | warning | judged | pass | The skill is prescriptive about fragile CI and merge actions, gives one default branch naming, and has an escape hatch (ask the user). | .agents/skills/fix-and-pr/SKILL.md:22,26-31 | docs/best-practices/skills.md#5-match-strictness-to-fragility, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.description.boundary` | warning | judged | pass | The description says the skill is not for reproducing, merging or closing issues. | .agents/skills/fix-and-pr/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.description.concise` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, docs/research-notes/agent-harness-best-practices/skills.md |
| `skills.description.length` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/opencode/skills.md#format, https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs, https://opencode.ai/docs/skills/ |
| `skills.description.no-workflow-steps` | warning | judged | fail | The description lists the procedure in order: branch, regression test, root-cause fix, open PR, fix CI. This mirrors procedure steps 2-6. | .agents/skills/fix-and-pr/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md |
| `skills.description.voice` | warning | judged | pass | The description is in the third person ("Fixes ..."). | .agents/skills/fix-and-pr/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition |
| `skills.description.what-and-when` | warning | judged | pass | The description gives concrete actions and then trigger phrases such as "fix bug #123". | .agents/skills/fix-and-pr/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://learn.chatgpt.com/docs/build-skills, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.frontmatter.valid` | error | script | pass | 1 skill(s) checked | - | docs/vendors/opencode/skills.md#format, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/claude-code/skills.md#format, docs/concepts/skills.md#frontmatter, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.goal.no-must-hold-rule-in-skill` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#13-move-rules-that-must-hold-every-time-into-hooks, https://code.claude.com/docs/en/skills |
| `skills.inputs.from-message` | warning | judged | fail | The skill takes the issue from the user's message but does not say to ask when it is missing. | .agents/skills/fix-and-pr/SKILL.md:21 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, docs/concepts/skills.md#body |
| `skills.invocation.both-flags` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#invocation-policy-in-both-leads, docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.invocation.side-effects-user-invoked` | error | judged | pass | The skill is user-invoked in both harnesses: disable-model-invocation: true for Claude Code and allow_implicit_invocation: false for Codex. | .agents/skills/fix-and-pr/SKILL.md:4; agents/openai.yaml:2 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.name.format` | error | script | pass | 1 skill(s) checked | - | docs/guide/skills.md#portability, docs/concepts/skills.md#frontmatter, docs/vendors/opencode/skills.md#format, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.package.no-auxiliary-docs` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#anti-patterns, https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md |
| `skills.portable.frontmatter` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/best-practices/skills.md#12-keep-one-canonical-copy-with-portable-frontmatter, https://code.claude.com/docs/en/skills |
| `skills.portable.layout` | error | script | pass | 1 skill(s) linked | - | docs/concepts/skills.md#directory-layout, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.portable.no-claude-placeholders` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#body, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills |
| `skills.portable.plugin-layout` | error | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#directory-layout, docs/vendors/claude-code/plugins.md#standard-layout, docs/vendors/codex/plugins.md#plugin-layout, https://code.claude.com/docs/en/plugins/manifest-reference, https://developers.openai.com/codex/plugins/build |
| `skills.references.load-conditions` | warning | judged | pass | The reference file is named with its load condition and holds only rule ids and sources. | .agents/skills/fix-and-pr/SKILL.md:34-35 | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/best-practices.md |
| `skills.references.one-level` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/specification |
| `skills.references.resolve` | error | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.reuse.reviewed-and-pinned` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#security, https://owasp.github.io/www-project-agentic-skills-top-10/ast01 |
| `skills.scope.committed-for-automation` | warning | judged | pass | The skill is committed in project scope, with a .claude/skills link. | links: .claude/skills/fix-and-pr | docs/concepts/skills.md#directory-layout, https://code.claude.com/docs/en/skills |
| `skills.scripts.agent-caller` | warning | judged | not-applicable | The skill bundles no scripts. | .agents/skills/fix-and-pr/ | docs/best-practices/skills.md#6-put-deterministic-logic-in-tested-scripts, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/using-scripts.md |
| `skills.security.allowed-tools-least-privilege` | warning | judged | not-applicable | The frontmatter declares no allowed-tools. | .agents/skills/fix-and-pr/SKILL.md:1-5 | docs/best-practices/skills.md#security, docs/vendors/claude-code/skills.md#limits-and-gotchas, https://code.claude.com/docs/en/skills |
| `skills.security.no-surprising-content` | error | judged | pass | There is no surprising content. | .agents/skills/fix-and-pr/SKILL.md | docs/best-practices/skills.md#security, https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md |

Contested `skills.body.reasons-before-hard-rules`:
- All-caps ALWAYS or NEVER is a yellow flag; explain the reasoning instead (https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md, https://agentskills.io/skill-creation/evaluating-skills.md)
- Discipline skills need firm prohibitions and rationalization tables (https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

Contested `skills.description.voice`:
- Always write in the third person; an inconsistent point of view can cause discovery problems (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Use imperative "Use this skill when" phrasing for the trigger (https://agentskills.io/skill-creation/optimizing-descriptions.md, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)

## Part D

- Harness result: not applicable
- Goal result: not assessed
- Status: blocked
- Outside dependencies: compromise-resistant-gate, event-gate
- Confirmed answers: `{"early_feedback": true, "event_without_agent": true, "every_time": "always", "hook_effect": "prevent", "hook_event": "PreToolUse", "job": "check", "must_survive_compromise": "required", "own_context": false, "script_checkable": true}`

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `links.parts` | error | script | pass | every linked part exists under its recorded name | - | - |
| `outside.ci.required-on-ref` | warning | judged | pass | event-gate says a CI check counts only when it is required on the protected ref. | README.md:77 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | The CI event-gate is recommended without any requirement to pin the sources its checks run. | README.md:76-82 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | The workflow-protected condition is present. | README.md:65,70 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | The CODEOWNERS recommendation with required code-owner review is present. | README.md:66 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | pass | The no-broader-bypass condition is present. | README.md:71,90 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Periodic verification is stated. | README.md:68,72,78,84,92 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | pass | The plan-enforced condition is present. | README.md:73,79,85 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | The real-refs condition is on every control. | README.md:67,74,80,86,91 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | pass | The no-agent-bypass condition is present. | README.md:75,81,87 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | pass | The requester-cannot-approve condition is present. | README.md:82,88 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | pass | merge-rules is recommended for part D. | README.md:83-88 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 5 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |

## Part E

- Harness result: not applicable
- Goal result: depends on outside controls
- Status: decided
- Outside dependencies: compromise-resistant-gate, event-gate
- Confirmed answers: `{"early_feedback": false, "event_without_agent": true, "every_time": "always", "job": "check", "must_survive_compromise": "required"}`

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `links.parts` | error | script | pass | every linked part exists under its recorded name | - | - |
| `outside.ci.required-on-ref` | warning | judged | pass | event-gate carries the required-on-ref condition. | README.md:101 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | The CI event-gate is recommended without pinning its check sources. | README.md:100-106 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | compromise-resistant-gate carries the workflow-protected condition. | README.md:94 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | Part E builds no harness setup. The built setup's agent configuration is covered by the CODEOWNERS recommendations elsewhere in the README, which also require code-owner review. | README.md:7,44,119 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | pass | The no-broader-bypass condition is present. | README.md:95,114 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Periodic verification is stated. | README.md:96,102,108,116 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | pass | The plan-enforced condition is present. | README.md:97,103,109 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | The real-refs condition is present. | README.md:98,104,110,115 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | pass | The no-agent-bypass condition is present. | README.md:99,105,111 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | pass | The requester-cannot-approve condition is present. | README.md:106,112 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | pass | merge-rules is recommended for part E. | README.md:107-112 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 4 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |

## Part F

- Harness result: not verified
- Goal result: not met
- Status: built
- Outside dependencies: none
- Confirmed answers: `{"event_without_agent": false, "every_time": "usually", "irreversible": false, "job": "procedure", "must_survive_compromise": "not-required", "own_context": false, "trigger": "model", "who_disables": "contributor"}`
- Goal verdict: met (close-and-label verifies the merge first, posts a note with the PR URL and merge commit, applies the final label, and closes the issue only if GitHub did not, without reopening it.)

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `idea.bug-intake.f.auto-closed` | warning | judged | pass | The skill checks the issue state, does not reopen an already-closed issue, and closes it itself if it is still open. | .agents/skills/close-and-label/SKILL.md:19,22 | https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue |
| `idea.bug-intake.f.closing-note` | error | judged | pass | The closing note is "Fixed by <PR URL>, merged in <merge commit SHA>". | .agents/skills/close-and-label/SKILL.md:20 | https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue |
| `idea.bug-intake.f.merged-first` | error | judged | pass | If the PR is not merged, the skill stops and leaves the issue as it is. | .agents/skills/close-and-label/SKILL.md:18 | https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue |
| `links.parts` | error | script | pass | every linked part exists under its recorded name | - | - |
| `outside.ci.required-on-ref` | warning | judged | fail | Nothing for part F says a check counts only when it is required on the protected ref. | README.md:117-131 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | No recommendation for part F requires pinning check sources. | README.md:117-131 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | The workflow-protected condition is present. | README.md:118 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | The CODEOWNERS recommendation with required code-owner review is present. | README.md:119 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | pass | The no-broader-bypass condition is present. | README.md:129 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Periodic verification is stated. | README.md:121,123,131 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | pass | The plan-enforced condition is present. | README.md:124 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | The real-refs condition is present. | README.md:120,125,130 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | pass | The no-agent-bypass condition is present. | README.md:126 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | pass | The requester-cannot-approve condition is present. | README.md:127 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | pass | merge-rules is recommended. | README.md:122-127 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 3 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `security.approval.claims-are-data` | warning | judged | pass | The merge is verified through gh pr view state, not through claims in content. | .agents/skills/close-and-label/SKILL.md:18 | docs/guide/security.md#context-and-persistent-state |
| `security.helpers.confined` | warning | judged | pass | Only gh runs, under the harness's permissions. | .agents/skills/close-and-label/SKILL.md:17-22 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#executables-approvals-and-isolation |
| `security.outbound.minimal-data` | warning | judged | pass | Writes are limited to the named issue (a comment with a fixed format, the label, closing). | .agents/skills/close-and-label/SKILL.md:20-22 | docs/guide/security.md#data-access-and-outbound-channels, https://developers.openai.com/api/docs/guides/deep-research#prompt-injection-and-exfiltration |
| `security.secrets.none-in-files` | error | judged | pass | The files contain no secrets. | .agents/skills/close-and-label/ | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#context-and-persistent-state |
| `security.untrusted-input.as-data` | warning | judged | pass | The procedure says to treat issues and tool output as data. | .agents/skills/close-and-label/SKILL.md:15 | docs/guide/security.md#context-and-persistent-state |
| `skills.body.gotchas-first` | warning | judged | pass | Requirements, including the Never-rule, are at the top. | .agents/skills/close-and-label/SKILL.md:7-15 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://agentskills.io/skill-creation/best-practices.md |
| `skills.body.no-time-bound-statements` | warning | judged | pass | There are none. | .agents/skills/close-and-label/SKILL.md | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.only-what-model-lacks` | warning | judged | pass | The body holds specific gh fields and closing behaviour. | .agents/skills/close-and-label/SKILL.md:17-23 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.reasons-before-hard-rules` | warning | judged | pass | Rules carry reasons, for example "since GitHub does not add a missing label", and there is little emphatic wording. | .agents/skills/close-and-label/SKILL.md:21 | docs/best-practices/skills.md#7-explain-the-why-before-adding-hard-rules |
| `skills.body.size` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, docs/concepts/skills.md#body, https://code.claude.com/docs/en/skills, https://agentskills.io/specification |
| `skills.body.strictness-matches-fragility` | warning | judged | pass | There is one default label path (the existing fixed label) with an escape hatch (ask the user). | .agents/skills/close-and-label/SKILL.md:21 | docs/best-practices/skills.md#5-match-strictness-to-fragility, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.description.boundary` | warning | judged | pass | The description says the skill is not for unmerged PRs, reproducing or fixing. | .agents/skills/close-and-label/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.description.concise` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, docs/research-notes/agent-harness-best-practices/skills.md |
| `skills.description.length` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/opencode/skills.md#format, https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs, https://opencode.ai/docs/skills/ |
| `skills.description.no-workflow-steps` | warning | judged | fail | The description lists the procedure in order: confirm merge, post note, apply label, close the issue if needed. | .agents/skills/close-and-label/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md |
| `skills.description.voice` | warning | judged | pass | The description is in the third person. | .agents/skills/close-and-label/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition |
| `skills.description.what-and-when` | warning | judged | pass | The description gives concrete actions and then trigger phrases such as "the fix is merged" and "close out #123". | .agents/skills/close-and-label/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://learn.chatgpt.com/docs/build-skills, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.frontmatter.valid` | error | script | pass | 1 skill(s) checked | - | docs/vendors/opencode/skills.md#format, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/claude-code/skills.md#format, docs/concepts/skills.md#frontmatter, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.goal.no-must-hold-rule-in-skill` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#13-move-rules-that-must-hold-every-time-into-hooks, https://code.claude.com/docs/en/skills |
| `skills.inputs.from-message` | warning | judged | pass | The skill reads the issue or PR from the message and asks the user if it stays unclear. | .agents/skills/close-and-label/SKILL.md:17 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, docs/concepts/skills.md#body |
| `skills.invocation.both-flags` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#invocation-policy-in-both-leads, docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.invocation.side-effects-user-invoked` | error | judged | fail | The skill closes issues, creates labels and posts comments on GitHub, which changes external state, but it is model-invocable in both harnesses: there is no disable-model-invocation and no agents/openai.yaml. | .agents/skills/close-and-label/SKILL.md:1-4,20-22 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.name.format` | error | script | pass | 1 skill(s) checked | - | docs/guide/skills.md#portability, docs/concepts/skills.md#frontmatter, docs/vendors/opencode/skills.md#format, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.package.no-auxiliary-docs` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#anti-patterns, https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md |
| `skills.portable.frontmatter` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/best-practices/skills.md#12-keep-one-canonical-copy-with-portable-frontmatter, https://code.claude.com/docs/en/skills |
| `skills.portable.layout` | error | script | pass | 1 skill(s) linked | - | docs/concepts/skills.md#directory-layout, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.portable.no-claude-placeholders` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#body, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills |
| `skills.portable.plugin-layout` | error | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#directory-layout, docs/vendors/claude-code/plugins.md#standard-layout, docs/vendors/codex/plugins.md#plugin-layout, https://code.claude.com/docs/en/plugins/manifest-reference, https://developers.openai.com/codex/plugins/build |
| `skills.references.load-conditions` | warning | judged | pass | The reference file is named with its condition and holds only ids and sources. | .agents/skills/close-and-label/SKILL.md:25-26 | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/best-practices.md |
| `skills.references.one-level` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/specification |
| `skills.references.resolve` | error | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.reuse.reviewed-and-pinned` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#security, https://owasp.github.io/www-project-agentic-skills-top-10/ast01 |
| `skills.scope.committed-for-automation` | warning | judged | pass | The skill is committed in project scope, with a .claude/skills link. | links: .claude/skills/close-and-label | docs/concepts/skills.md#directory-layout, https://code.claude.com/docs/en/skills |
| `skills.scripts.agent-caller` | warning | judged | not-applicable | The skill bundles no scripts. | .agents/skills/close-and-label/ | docs/best-practices/skills.md#6-put-deterministic-logic-in-tested-scripts, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/using-scripts.md |
| `skills.security.allowed-tools-least-privilege` | warning | judged | not-applicable | The frontmatter declares no allowed-tools. | .agents/skills/close-and-label/SKILL.md:1-4 | docs/best-practices/skills.md#security, docs/vendors/claude-code/skills.md#limits-and-gotchas, https://code.claude.com/docs/en/skills |
| `skills.security.no-surprising-content` | error | judged | pass | There is no surprising content. | .agents/skills/close-and-label/SKILL.md | docs/best-practices/skills.md#security, https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md |

Contested `skills.body.reasons-before-hard-rules`:
- All-caps ALWAYS or NEVER is a yellow flag; explain the reasoning instead (https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md, https://agentskills.io/skill-creation/evaluating-skills.md)
- Discipline skills need firm prohibitions and rationalization tables (https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

Contested `skills.description.voice`:
- Always write in the third person; an inconsistent point of view can cause discovery problems (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Use imperative "Use this skill when" phrasing for the trigger (https://agentskills.io/skill-creation/optimizing-descriptions.md, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)

## Part G

- Harness result: not applicable
- Goal result: not assessed
- Status: blocked
- Outside dependencies: compromise-resistant-gate
- Confirmed answers: `{"event_without_agent": false, "every_time": "always", "job": "access-control", "must_survive_compromise": "required"}`

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `links.parts` | error | script | error | part A's hooks has no builder in this release, so its name cannot be checked | - | - |
| `outside.ci.required-on-ref` | warning | judged | fail | Part G's gates rely on workflow-defined checks, but nothing says a check counts only when it is required on the protected ref. | README.md:132-153 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | No recommendation for part G requires pinning check sources. | README.md:132-153 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | The workflow-protected condition is present. | README.md:133,138 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | The CODEOWNERS recommendation with required code-owner review is present. | README.md:134 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | pass | The no-broader-bypass condition is present. | README.md:139,151 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Periodic verification is stated. | README.md:136,140,145,153 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | pass | The plan-enforced condition is present. | README.md:141,146 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | The real-refs condition is present. | README.md:135,142,147,152 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | pass | The no-agent-bypass condition is present. | README.md:143,148 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | pass | The requester-cannot-approve condition is present. | README.md:149 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | pass | merge-rules is recommended. | README.md:144-149 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 4 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |

## Runtime tests

| Part | Case | Harness | Result | Observed | Reason |
| --- | --- | --- | --- | --- | --- |
| B | reproduce-explicit | claude-code 2.1.302 (Claude Code) | pass | Skill tool called for reproduce | Skill tool called for reproduce |
| B | reproduce-implicit | claude-code 2.1.302 (Claude Code) | pass | Skill tool called for reproduce | Skill tool called for reproduce |
| B | reproduce-near-miss | claude-code 2.1.302 (Claude Code) | pass | - | no Skill tool call for the candidate |
| C | fix-and-pr-explicit | claude-code 2.1.302 (Claude Code) | fail | - | the skill was not activated |
| C | fix-and-pr-near-miss | claude-code 2.1.302 (Claude Code) | pass | - | no Skill tool call for the candidate |
| F | close-and-label-explicit | claude-code 2.1.302 (Claude Code) | pass | Skill tool called for close-and-label | Skill tool called for close-and-label |
| F | close-and-label-implicit | claude-code 2.1.302 (Claude Code) | pass | Skill tool called for close-and-label | Skill tool called for close-and-label |
| F | close-and-label-near-miss | claude-code 2.1.302 (Claude Code) | pass | - | no Skill tool call for the candidate |

## Checked files

```
65989f132adcc3cbc403aaca9359719eba8496dcf21e54336f582c75d085f449  .agents/skills/close-and-label/SKILL.md
0de99399c492825eed679fba31bd12279fe15ad017644a3740646fb05a0aac69  .agents/skills/close-and-label/references/requirements.md
18a359c776eea82acdbe4d13a21ecc2ac9dfae881ab8e484bc44daef70cabd1e  .agents/skills/fix-and-pr/SKILL.md
a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94  .agents/skills/fix-and-pr/agents/openai.yaml
9e6ad0a1f3fff8f948bb0c972ff011fc4ecfb266e2914618de896bbc71dbd84f  .agents/skills/fix-and-pr/references/requirements.md
c657df4e103312fc3c875337b3015c5bdd6db10cc825a1e521ea067de2adb9a9  .agents/skills/reproduce/SKILL.md
efe1922fced886a763fb805b9f2123ed35027afe2b65fec8c2a8b17687d56c50  .agents/skills/reproduce/references/requirements.md
5dcbfbbf8694697fd4a9669a42878bdbc3ae31a5cf70d5b95737e419360a6bae  README.md
link  .claude/skills/close-and-label -> ../../.agents/skills/close-and-label
link  .claude/skills/fix-and-pr -> ../../.agents/skills/fix-and-pr
link  .claude/skills/reproduce -> ../../.agents/skills/reproduce
```

## Report data

```json
{
  "answers": {
    "A": {
      "event_without_agent": false,
      "every_time": "always",
      "hook_effect": "prevent",
      "hook_event": "PreToolUse",
      "irreversible": true,
      "job": "procedure",
      "must_survive_compromise": "not-required",
      "own_context": false,
      "script_checkable": true,
      "who_disables": "contributor"
    },
    "B": {
      "event_without_agent": false,
      "every_time": "usually",
      "irreversible": false,
      "job": "procedure",
      "must_survive_compromise": "not-required",
      "own_context": false,
      "trigger": "model",
      "who_disables": "contributor"
    },
    "C": {
      "event_without_agent": false,
      "every_time": "usually",
      "irreversible": true,
      "job": "procedure",
      "must_survive_compromise": "not-required",
      "own_context": false,
      "trigger": "user",
      "who_disables": "contributor"
    },
    "D": {
      "early_feedback": true,
      "event_without_agent": true,
      "every_time": "always",
      "hook_effect": "prevent",
      "hook_event": "PreToolUse",
      "job": "check",
      "must_survive_compromise": "required",
      "own_context": false,
      "script_checkable": true
    },
    "E": {
      "early_feedback": false,
      "event_without_agent": true,
      "every_time": "always",
      "job": "check",
      "must_survive_compromise": "required"
    },
    "F": {
      "event_without_agent": false,
      "every_time": "usually",
      "irreversible": false,
      "job": "procedure",
      "must_survive_compromise": "not-required",
      "own_context": false,
      "trigger": "model",
      "who_disables": "contributor"
    },
    "G": {
      "event_without_agent": false,
      "every_time": "always",
      "job": "access-control",
      "must_survive_compromise": "required"
    }
  },
  "bound_inputs": {
    "cases": {
      "A": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
      "B": "a862ada03450499f3982d15dc4b8da9912e1ca202eb068d01befb812c305ac14",
      "C": "13d0ecf6afdc073f4bc36222bb67c405be9855860782063a3099063c564e3e60",
      "D": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
      "E": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
      "F": "896a8b322393d7af09ccf544d84a0b574312247ea79716d7ceb91f5ed94354dc",
      "G": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
    },
    "checkers": "7beeb29d229339f59695dccf5877b0efc53a7e117ff8fb0b7773c93c0d92e0df",
    "files": {
      ".agents/skills/close-and-label/SKILL.md": "65989f132adcc3cbc403aaca9359719eba8496dcf21e54336f582c75d085f449",
      ".agents/skills/close-and-label/references/requirements.md": "0de99399c492825eed679fba31bd12279fe15ad017644a3740646fb05a0aac69",
      ".agents/skills/fix-and-pr/SKILL.md": "18a359c776eea82acdbe4d13a21ecc2ac9dfae881ab8e484bc44daef70cabd1e",
      ".agents/skills/fix-and-pr/agents/openai.yaml": "a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94",
      ".agents/skills/fix-and-pr/references/requirements.md": "9e6ad0a1f3fff8f948bb0c972ff011fc4ecfb266e2914618de896bbc71dbd84f",
      ".agents/skills/reproduce/SKILL.md": "c657df4e103312fc3c875337b3015c5bdd6db10cc825a1e521ea067de2adb9a9",
      ".agents/skills/reproduce/references/requirements.md": "efe1922fced886a763fb805b9f2123ed35027afe2b65fec8c2a8b17687d56c50",
      "README.md": "5dcbfbbf8694697fd4a9669a42878bdbc3ae31a5cf70d5b95737e419360a6bae"
    },
    "idea": "39333c05d327aa7d3a809a95990b6c92a08e3b6ea12bb192c3d34a902598aed7",
    "kb_version": "0.1.0",
    "overrides": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "parts": {
      "A": "41bfd04338241ee31fb708a216905849bba4f04fe73f1606a593fdbba0196984",
      "B": "41463a8c66317595ec03815642d28af40b6eea5c0a76b484726bdc731fb746b6",
      "C": "01634246be47decea0a7a80f05858340bf8e24c3f5ed61ef9e7f06e097182ad5",
      "D": "aed4918861ab181b0eae10e80ca427471c9b124955da5529bef445e54170eda4",
      "E": "78fe67e4c3318a32646b45b8a1280b4abc4046ba120ac1635114530f47f8d60e",
      "F": "16b73f1555ac062191bef023a93c546777f2448cbf0d75969f4391b016f0cba9",
      "G": "5885d7fbc3da3916e3348f95d35d32b6fa775b695a88ba8ebd28941c16f5349a"
    },
    "revision": "e1805692c07794fb076d85404a8ce1d99581b7ad56af5cabea3935af53c2acde",
    "rules": "93fec41536adbe0420026720fecbe03465b27f5f457695dc9d5704d422d7488a",
    "symlinks": {
      ".claude/skills/close-and-label": "../../.agents/skills/close-and-label",
      ".claude/skills/fix-and-pr": "../../.agents/skills/fix-and-pr",
      ".claude/skills/reproduce": "../../.agents/skills/reproduce"
    },
    "worker": "cb9988f2be30ff09747816ba5776418c93488ff83c58db1c3b94386ed7c3018d"
  },
  "confirmed_parts": [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G"
  ],
  "contract_digest": "1aca09f6e1858d262e090a9202425c1d4e84904834b83c048aee345e274784ae",
  "decision_digest": "a8fd69b94b43a23ee3aaf81944c247decb355763b04306d9453decb00c104e61",
  "file_hashes": {
    ".agents/skills/close-and-label/SKILL.md": "65989f132adcc3cbc403aaca9359719eba8496dcf21e54336f582c75d085f449",
    ".agents/skills/close-and-label/references/requirements.md": "0de99399c492825eed679fba31bd12279fe15ad017644a3740646fb05a0aac69",
    ".agents/skills/fix-and-pr/SKILL.md": "18a359c776eea82acdbe4d13a21ecc2ac9dfae881ab8e484bc44daef70cabd1e",
    ".agents/skills/fix-and-pr/agents/openai.yaml": "a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94",
    ".agents/skills/fix-and-pr/references/requirements.md": "9e6ad0a1f3fff8f948bb0c972ff011fc4ecfb266e2914618de896bbc71dbd84f",
    ".agents/skills/reproduce/SKILL.md": "c657df4e103312fc3c875337b3015c5bdd6db10cc825a1e521ea067de2adb9a9",
    ".agents/skills/reproduce/references/requirements.md": "efe1922fced886a763fb805b9f2123ed35027afe2b65fec8c2a8b17687d56c50",
    "README.md": "5dcbfbbf8694697fd4a9669a42878bdbc3ae31a5cf70d5b95737e419360a6bae"
  },
  "idea_digest": "39333c05d327aa7d3a809a95990b6c92a08e3b6ea12bb192c3d34a902598aed7",
  "kb_version": "0.1.0",
  "overrides": [],
  "part_map": {
    "dirs": {
      "B": ".agents/skills/reproduce",
      "C": ".agents/skills/fix-and-pr",
      "F": ".agents/skills/close-and-label"
    },
    "files": {
      "A": [
        "README.md"
      ],
      "B": [
        ".agents/skills/reproduce/SKILL.md",
        ".agents/skills/reproduce/references/requirements.md",
        "README.md"
      ],
      "C": [
        ".agents/skills/fix-and-pr/SKILL.md",
        ".agents/skills/fix-and-pr/agents/openai.yaml",
        ".agents/skills/fix-and-pr/references/requirements.md",
        "README.md"
      ],
      "D": [
        "README.md"
      ],
      "E": [
        "README.md"
      ],
      "F": [
        ".agents/skills/close-and-label/SKILL.md",
        ".agents/skills/close-and-label/references/requirements.md",
        "README.md"
      ],
      "G": [
        "README.md"
      ]
    },
    "links": {
      "B": [
        ".claude/skills/reproduce"
      ],
      "C": [
        ".claude/skills/fix-and-pr"
      ],
      "F": [
        ".claude/skills/close-and-label"
      ]
    },
    "requirement_parts": [
      "B",
      "C",
      "F"
    ]
  },
  "parts": [
    {
      "goal_result": "not assessed",
      "goal_verdict": null,
      "harness_result": "not applicable",
      "outside_dependencies": [
        "compromise-resistant-gate"
      ],
      "part_id": "A",
      "rule_results": [
        {
          "check": "script",
          "reason": "4 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": "README.md:8,15,20,25",
          "reason": "Every control recommended for part A carries the real-refs condition.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:16,21",
          "reason": "compromise-resistant-gate and merge-rules both require that the agent's identity is on no bypass list.",
          "result": "pass",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:22",
          "reason": "merge-rules for part A requires approval from a different identity that resets on new pushes.",
          "result": "pass",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:5-26",
          "reason": "Part A's gates depend on workflow-defined checks (see the workflow-protected condition), but no part A recommendation says a CI check counts as a gate only when it is required on the protected ref.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:5-26",
          "reason": "No part A recommendation requires pinning the sources the gate's checks run, such as actions or scanners. Only workflow files from outside the repository are mentioned as pinned.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:6,11",
          "reason": "codeowners-agent-config and compromise-resistant-gate both include the workflow-protected condition, including that CODEOWNERS owns itself.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:12,24",
          "reason": "compromise-resistant-gate and outer-isolation both carry the no-broader-bypass condition.",
          "result": "pass",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:14,19",
          "reason": "The plan-enforced condition is stated, and availability is given as available.",
          "result": "pass",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:9,13,18,26",
          "reason": "Every control for part A says to check its configuration periodically.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:7",
          "reason": "A CODEOWNERS entry is recommended for .agents/, .claude/, .codex/, AGENTS.md, the workflows and CODEOWNERS itself, together with required code-owner review.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "README.md:17-22",
          "reason": "merge-rules is recommended for part A.",
          "result": "pass",
          "rule_id": "outside.merge.rule-for-agent-prs"
        }
      ],
      "status": "blocked"
    },
    {
      "goal_result": "not met",
      "goal_verdict": {
        "reason": "The reproduce skill runs fresh repeated reproductions, posts exact numbered steps, observed and expected results, a run tally and a consistent, intermittent or not-reproduced verdict to the issue, and covers all six accepted requirements.",
        "verdict": "met"
      },
      "harness_result": "not verified",
      "outside_dependencies": [],
      "part_id": "B",
      "rule_results": [
        {
          "check": "script",
          "reason": "part A's hooks has no builder in this release, so its name cannot be checked",
          "result": "error",
          "rule_id": "links.parts"
        },
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
          "citation": ".agents/skills/reproduce/SKILL.md:3",
          "reason": "The description states what the skill does with concrete verbs, then gives trigger phrases such as \"reproduce this bug\" and \"can you repro #123\".",
          "result": "pass",
          "rule_id": "skills.description.what-and-when"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:3",
          "reason": "The description names what the skill produces (steps, results, run counts, verdict), not the order of its procedure.",
          "result": "pass",
          "rule_id": "skills.description.no-workflow-steps"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:3",
          "reason": "The description says the skill is not for creating, fixing or closing issues.",
          "result": "pass",
          "rule_id": "skills.description.boundary"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:3",
          "reason": "The description is in the third person (\"Reproduces ...\").",
          "result": "pass",
          "rule_id": "skills.description.voice"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:20-36",
          "reason": "The body holds specific standing instructions (run counts, fresh state, comment structure) and no general explanation.",
          "result": "pass",
          "rule_id": "skills.body.only-what-model-lacks"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:7-18",
          "reason": "Requirements and the untrusted-data rule sit at the top of SKILL.md.",
          "result": "pass",
          "rule_id": "skills.body.gotchas-first"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md",
          "reason": "There are no time-bound statements.",
          "result": "pass",
          "rule_id": "skills.body.no-time-bound-statements"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:38-39",
          "reason": "The reference file is named with its load condition and holds only rule ids and sources.",
          "result": "pass",
          "rule_id": "skills.references.load-conditions"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:22-23",
          "reason": "There is one default (5 runs, at least 10 if the runs disagree) and a single preferred form (an automated reproduction).",
          "result": "pass",
          "rule_id": "skills.body.strictness-matches-fragility"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/",
          "reason": "The skill bundles no scripts.",
          "result": "not-applicable",
          "rule_id": "skills.scripts.agent-caller"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:22-23",
          "reason": "Rules carry reasons, for example \"since it can be rerun unchanged\" and \"so the count means something\", and emphatic wording is rare.",
          "result": "pass",
          "rule_id": "skills.body.reasons-before-hard-rules"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:1-4,29",
          "reason": "The skill posts a comment to a GitHub issue, which changes external state, yet it is model-invocable in both harnesses: there is no disable-model-invocation and no agents/openai.yaml.",
          "result": "fail",
          "rule_id": "skills.invocation.side-effects-user-invoked"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:20",
          "reason": "The skill reads the issue from the user's message but does not say to ask when the issue number or URL is missing.",
          "result": "fail",
          "rule_id": "skills.inputs.from-message"
        },
        {
          "check": "judged",
          "citation": "links: .claude/skills/reproduce",
          "reason": "The skill is committed in project scope under .agents/skills, with a .claude/skills link.",
          "result": "pass",
          "rule_id": "skills.scope.committed-for-automation"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md",
          "reason": "There is no hidden directive, remote fetch-and-run or credential access.",
          "result": "pass",
          "rule_id": "skills.security.no-surprising-content"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:1-4",
          "reason": "The frontmatter declares no allowed-tools.",
          "result": "not-applicable",
          "rule_id": "skills.security.allowed-tools-least-privilege"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/",
          "reason": "The files contain no secrets.",
          "result": "pass",
          "rule_id": "security.secrets.none-in-files"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:18",
          "reason": "The procedure says to treat issues, fetched pages and tool output as data.",
          "result": "pass",
          "rule_id": "security.untrusted-input.as-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:18",
          "reason": "No step treats a claim in content as authorization.",
          "result": "pass",
          "rule_id": "security.approval.claims-are-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:20,29",
          "reason": "The skill uses only gh and the reproduction commands under the harness's permissions, with no pre-approval.",
          "result": "pass",
          "rule_id": "security.helpers.confined"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:18,29-34",
          "reason": "The only outbound write is a comment on the same issue, with defined fields, and content is treated as data.",
          "result": "pass",
          "rule_id": "security.outbound.minimal-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:22,31",
          "reason": "The skill requires numbered, exact steps and puts them in the issue comment.",
          "result": "pass",
          "rule_id": "idea.bug-intake.b.exact-steps"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:23,33",
          "reason": "The skill requires several fresh-process runs and records the tally in the issue.",
          "result": "pass",
          "rule_id": "idea.bug-intake.b.repeated-runs"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:25-28,33",
          "reason": "The verdict is consistent, intermittent with a count, or not reproduced, and it goes into the issue.",
          "result": "pass",
          "rule_id": "idea.bug-intake.b.consistency-statement"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:31-32",
          "reason": "Observed and Expected results, each precise, come after the steps.",
          "result": "pass",
          "rule_id": "idea.bug-intake.b.observed-expected"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:34",
          "reason": "Observations are kept separate from a \"Possible cause (unverified)\" section.",
          "result": "pass",
          "rule_id": "idea.bug-intake.b.facts-vs-speculation"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduce/SKILL.md:24",
          "reason": "When runs disagree, the skill runs the reproduction alone, together with related tests, and in a different order.",
          "result": "pass",
          "rule_id": "idea.bug-intake.b.order-dependency"
        },
        {
          "check": "script",
          "reason": "3 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": "README.md:30,35,40",
          "reason": "Every control for part B carries the real-refs condition.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:36",
          "reason": "merge-rules for part B carries the no-agent-bypass condition.",
          "result": "pass",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:37",
          "reason": "merge-rules for part B carries the requester-cannot-approve condition.",
          "result": "pass",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:27-41",
          "reason": "Part B's gates rely on workflow-defined checks, but nothing says a check counts only when it is required on the protected ref.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:27-41",
          "reason": "No recommendation for part B requires pinning the sources the checks run.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:28",
          "reason": "codeowners-agent-config carries the workflow-protected condition.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:39",
          "reason": "outer-isolation carries the no-broader-bypass condition.",
          "result": "pass",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:32-34",
          "reason": "merge-rules carries the plan-enforced condition, and availability is given as available.",
          "result": "pass",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:31,33,41",
          "reason": "Every control for part B says to check its configuration periodically.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:29",
          "reason": "CODEOWNERS for the agent configuration and required code-owner review are recommended.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "README.md:32-37",
          "reason": "merge-rules is recommended for part B.",
          "result": "pass",
          "rule_id": "outside.merge.rule-for-agent-prs"
        },
        {
          "check": "judged",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.goal.no-must-hold-rule-in-skill"
        },
        {
          "check": "script",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.portable.plugin-layout"
        },
        {
          "check": "judged",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.reuse.reviewed-and-pinned"
        }
      ],
      "status": "built"
    },
    {
      "goal_result": "not met",
      "goal_verdict": {
        "reason": "fix-and-pr creates a fix branch from the default branch, adds a regression test, opens a PR with Fixes #N, fixes CI at the cause without workarounds or pwn-request changes, never merges, and reports ready only when all required checks are green.",
        "verdict": "met"
      },
      "harness_result": "not verified",
      "outside_dependencies": [
        "compromise-resistant-gate"
      ],
      "part_id": "C",
      "rule_results": [
        {
          "check": "script",
          "reason": "every linked part exists under its recorded name",
          "result": "pass",
          "rule_id": "links.parts"
        },
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
          "citation": ".agents/skills/fix-and-pr/SKILL.md:3",
          "reason": "The description gives concrete actions and then trigger phrases such as \"fix bug #123\".",
          "result": "pass",
          "rule_id": "skills.description.what-and-when"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:3",
          "reason": "The description lists the procedure in order: branch, regression test, root-cause fix, open PR, fix CI. This mirrors procedure steps 2-6.",
          "result": "fail",
          "rule_id": "skills.description.no-workflow-steps"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:3",
          "reason": "The description says the skill is not for reproducing, merging or closing issues.",
          "result": "pass",
          "rule_id": "skills.description.boundary"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:3",
          "reason": "The description is in the third person (\"Fixes ...\").",
          "result": "pass",
          "rule_id": "skills.description.voice"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:21-32",
          "reason": "The body holds specific standing instructions, such as the list of workarounds and how closing keywords behave, without generic explanation.",
          "result": "pass",
          "rule_id": "skills.body.only-what-model-lacks"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:8-19",
          "reason": "The Never-rules and the untrusted-data rule are at the top.",
          "result": "pass",
          "rule_id": "skills.body.gotchas-first"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md",
          "reason": "There are no time-bound statements.",
          "result": "pass",
          "rule_id": "skills.body.no-time-bound-statements"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:34-35",
          "reason": "The reference file is named with its load condition and holds only rule ids and sources.",
          "result": "pass",
          "rule_id": "skills.references.load-conditions"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:22,26-31",
          "reason": "The skill is prescriptive about fragile CI and merge actions, gives one default branch naming, and has an escape hatch (ask the user).",
          "result": "pass",
          "rule_id": "skills.body.strictness-matches-fragility"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/",
          "reason": "The skill bundles no scripts.",
          "result": "not-applicable",
          "rule_id": "skills.scripts.agent-caller"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:25,32",
          "reason": "Hard rules carry reasons, for example \"closing keywords are ignored there\" and \"merging is left to the people and rules of the repository\".",
          "result": "pass",
          "rule_id": "skills.body.reasons-before-hard-rules"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:4; agents/openai.yaml:2",
          "reason": "The skill is user-invoked in both harnesses: disable-model-invocation: true for Claude Code and allow_implicit_invocation: false for Codex.",
          "result": "pass",
          "rule_id": "skills.invocation.side-effects-user-invoked"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:21",
          "reason": "The skill takes the issue from the user's message but does not say to ask when it is missing.",
          "result": "fail",
          "rule_id": "skills.inputs.from-message"
        },
        {
          "check": "judged",
          "citation": "links: .claude/skills/fix-and-pr",
          "reason": "The skill is committed in project scope, with a .claude/skills link.",
          "result": "pass",
          "rule_id": "skills.scope.committed-for-automation"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md",
          "reason": "There is no surprising content.",
          "result": "pass",
          "rule_id": "skills.security.no-surprising-content"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:1-5",
          "reason": "The frontmatter declares no allowed-tools.",
          "result": "not-applicable",
          "rule_id": "skills.security.allowed-tools-least-privilege"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/",
          "reason": "The files contain no secrets.",
          "result": "pass",
          "rule_id": "security.secrets.none-in-files"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:19",
          "reason": "The procedure says to treat issues, fetched pages and tool output as data.",
          "result": "pass",
          "rule_id": "security.untrusted-input.as-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:19,31",
          "reason": "No step treats a claim in content as authorization, and workflow changes require asking the user.",
          "result": "pass",
          "rule_id": "security.approval.claims-are-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:21-26",
          "reason": "Only gh and git run, under the harness's permissions, with no pre-approval.",
          "result": "pass",
          "rule_id": "security.helpers.confined"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:19,25",
          "reason": "Pushes go only to this repository's branch and PR, with defined content, and untrusted content is treated as data.",
          "result": "pass",
          "rule_id": "security.outbound.minimal-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:25",
          "reason": "The PR targets the default branch with \"Fixes #<number>\". For another branch it uses \"Related to\" and tells the user.",
          "result": "pass",
          "rule_id": "idea.bug-intake.c.closing-keyword"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:23",
          "reason": "The reproduction steps become a new or updated test that is confirmed to fail before the fix.",
          "result": "pass",
          "rule_id": "idea.bug-intake.c.regression-test"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:26-31",
          "reason": "Skipping, weakening or deleting tests and changing CI are explicitly forbidden.",
          "result": "pass",
          "rule_id": "idea.bug-intake.c.ci-workaround"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:31",
          "reason": "Combining pull_request_target with a checkout of PR code is forbidden.",
          "result": "pass",
          "rule_id": "idea.bug-intake.c.pwn-request"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:32",
          "reason": "The skill says \"Never merge the pull request\".",
          "result": "pass",
          "rule_id": "idea.bug-intake.c.self-merge"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/fix-and-pr/SKILL.md:32",
          "reason": "The PR is reported ready only when every required check has passed; otherwise the failing checks are listed.",
          "result": "pass",
          "rule_id": "idea.bug-intake.c.green-before-done"
        },
        {
          "check": "script",
          "reason": "4 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": "README.md:45,52,57,62",
          "reason": "Every control for part C carries the real-refs condition.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:53,58",
          "reason": "The no-agent-bypass condition is present.",
          "result": "pass",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:59",
          "reason": "merge-rules carries the requester-cannot-approve condition.",
          "result": "pass",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:42-63",
          "reason": "Part C depends on required checks passing, but no part C recommendation says a check counts as a gate only when it is required on the protected ref (no event-gate for C).",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:42-63",
          "reason": "No recommendation for part C requires pinning check sources.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:43,48",
          "reason": "The workflow-protected condition is present.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:49,61",
          "reason": "The no-broader-bypass condition is present.",
          "result": "pass",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:51,56",
          "reason": "The plan-enforced condition is present.",
          "result": "pass",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:46,50,55,63",
          "reason": "Periodic verification is stated.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:44",
          "reason": "The CODEOWNERS recommendation for agent configuration and required code-owner review is present.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "README.md:54-59",
          "reason": "The agent opens PRs in part C, and merge-rules is recommended.",
          "result": "pass",
          "rule_id": "outside.merge.rule-for-agent-prs"
        },
        {
          "check": "judged",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.goal.no-must-hold-rule-in-skill"
        },
        {
          "check": "script",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.portable.plugin-layout"
        },
        {
          "check": "judged",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.reuse.reviewed-and-pinned"
        },
        {
          "check": "script",
          "reason": "the live build needs an observed explicit activation, and none passed",
          "result": "fail",
          "rule_id": "runtime.explicit-activation"
        }
      ],
      "status": "built"
    },
    {
      "goal_result": "not assessed",
      "goal_verdict": null,
      "harness_result": "not applicable",
      "outside_dependencies": [
        "compromise-resistant-gate",
        "event-gate"
      ],
      "part_id": "D",
      "rule_results": [
        {
          "check": "script",
          "reason": "every linked part exists under its recorded name",
          "result": "pass",
          "rule_id": "links.parts"
        },
        {
          "check": "script",
          "reason": "5 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": "README.md:67,74,80,86,91",
          "reason": "The real-refs condition is on every control.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:75,81,87",
          "reason": "The no-agent-bypass condition is present.",
          "result": "pass",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:82,88",
          "reason": "The requester-cannot-approve condition is present.",
          "result": "pass",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:77",
          "reason": "event-gate says a CI check counts only when it is required on the protected ref.",
          "result": "pass",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:76-82",
          "reason": "The CI event-gate is recommended without any requirement to pin the sources its checks run.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:65,70",
          "reason": "The workflow-protected condition is present.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:71,90",
          "reason": "The no-broader-bypass condition is present.",
          "result": "pass",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:73,79,85",
          "reason": "The plan-enforced condition is present.",
          "result": "pass",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:68,72,78,84,92",
          "reason": "Periodic verification is stated.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:66",
          "reason": "The CODEOWNERS recommendation with required code-owner review is present.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "README.md:83-88",
          "reason": "merge-rules is recommended for part D.",
          "result": "pass",
          "rule_id": "outside.merge.rule-for-agent-prs"
        }
      ],
      "status": "blocked"
    },
    {
      "goal_result": "depends on outside controls",
      "goal_verdict": null,
      "harness_result": "not applicable",
      "outside_dependencies": [
        "compromise-resistant-gate",
        "event-gate"
      ],
      "part_id": "E",
      "rule_results": [
        {
          "check": "script",
          "reason": "every linked part exists under its recorded name",
          "result": "pass",
          "rule_id": "links.parts"
        },
        {
          "check": "script",
          "reason": "4 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": "README.md:98,104,110,115",
          "reason": "The real-refs condition is present.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:99,105,111",
          "reason": "The no-agent-bypass condition is present.",
          "result": "pass",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:106,112",
          "reason": "The requester-cannot-approve condition is present.",
          "result": "pass",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:101",
          "reason": "event-gate carries the required-on-ref condition.",
          "result": "pass",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:100-106",
          "reason": "The CI event-gate is recommended without pinning its check sources.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:94",
          "reason": "compromise-resistant-gate carries the workflow-protected condition.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:95,114",
          "reason": "The no-broader-bypass condition is present.",
          "result": "pass",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:97,103,109",
          "reason": "The plan-enforced condition is present.",
          "result": "pass",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:96,102,108,116",
          "reason": "Periodic verification is stated.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:7,44,119",
          "reason": "Part E builds no harness setup. The built setup's agent configuration is covered by the CODEOWNERS recommendations elsewhere in the README, which also require code-owner review.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "README.md:107-112",
          "reason": "merge-rules is recommended for part E.",
          "result": "pass",
          "rule_id": "outside.merge.rule-for-agent-prs"
        }
      ],
      "status": "decided"
    },
    {
      "goal_result": "not met",
      "goal_verdict": {
        "reason": "close-and-label verifies the merge first, posts a note with the PR URL and merge commit, applies the final label, and closes the issue only if GitHub did not, without reopening it.",
        "verdict": "met"
      },
      "harness_result": "not verified",
      "outside_dependencies": [],
      "part_id": "F",
      "rule_results": [
        {
          "check": "script",
          "reason": "every linked part exists under its recorded name",
          "result": "pass",
          "rule_id": "links.parts"
        },
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
          "citation": ".agents/skills/close-and-label/SKILL.md:3",
          "reason": "The description gives concrete actions and then trigger phrases such as \"the fix is merged\" and \"close out #123\".",
          "result": "pass",
          "rule_id": "skills.description.what-and-when"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:3",
          "reason": "The description lists the procedure in order: confirm merge, post note, apply label, close the issue if needed.",
          "result": "fail",
          "rule_id": "skills.description.no-workflow-steps"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:3",
          "reason": "The description says the skill is not for unmerged PRs, reproducing or fixing.",
          "result": "pass",
          "rule_id": "skills.description.boundary"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:3",
          "reason": "The description is in the third person.",
          "result": "pass",
          "rule_id": "skills.description.voice"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:17-23",
          "reason": "The body holds specific gh fields and closing behaviour.",
          "result": "pass",
          "rule_id": "skills.body.only-what-model-lacks"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:7-15",
          "reason": "Requirements, including the Never-rule, are at the top.",
          "result": "pass",
          "rule_id": "skills.body.gotchas-first"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md",
          "reason": "There are none.",
          "result": "pass",
          "rule_id": "skills.body.no-time-bound-statements"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:25-26",
          "reason": "The reference file is named with its condition and holds only ids and sources.",
          "result": "pass",
          "rule_id": "skills.references.load-conditions"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:21",
          "reason": "There is one default label path (the existing fixed label) with an escape hatch (ask the user).",
          "result": "pass",
          "rule_id": "skills.body.strictness-matches-fragility"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/",
          "reason": "The skill bundles no scripts.",
          "result": "not-applicable",
          "rule_id": "skills.scripts.agent-caller"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:21",
          "reason": "Rules carry reasons, for example \"since GitHub does not add a missing label\", and there is little emphatic wording.",
          "result": "pass",
          "rule_id": "skills.body.reasons-before-hard-rules"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:1-4,20-22",
          "reason": "The skill closes issues, creates labels and posts comments on GitHub, which changes external state, but it is model-invocable in both harnesses: there is no disable-model-invocation and no agents/openai.yaml.",
          "result": "fail",
          "rule_id": "skills.invocation.side-effects-user-invoked"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:17",
          "reason": "The skill reads the issue or PR from the message and asks the user if it stays unclear.",
          "result": "pass",
          "rule_id": "skills.inputs.from-message"
        },
        {
          "check": "judged",
          "citation": "links: .claude/skills/close-and-label",
          "reason": "The skill is committed in project scope, with a .claude/skills link.",
          "result": "pass",
          "rule_id": "skills.scope.committed-for-automation"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md",
          "reason": "There is no surprising content.",
          "result": "pass",
          "rule_id": "skills.security.no-surprising-content"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:1-4",
          "reason": "The frontmatter declares no allowed-tools.",
          "result": "not-applicable",
          "rule_id": "skills.security.allowed-tools-least-privilege"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/",
          "reason": "The files contain no secrets.",
          "result": "pass",
          "rule_id": "security.secrets.none-in-files"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:15",
          "reason": "The procedure says to treat issues and tool output as data.",
          "result": "pass",
          "rule_id": "security.untrusted-input.as-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:18",
          "reason": "The merge is verified through gh pr view state, not through claims in content.",
          "result": "pass",
          "rule_id": "security.approval.claims-are-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:17-22",
          "reason": "Only gh runs, under the harness's permissions.",
          "result": "pass",
          "rule_id": "security.helpers.confined"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:20-22",
          "reason": "Writes are limited to the named issue (a comment with a fixed format, the label, closing).",
          "result": "pass",
          "rule_id": "security.outbound.minimal-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:20",
          "reason": "The closing note is \"Fixed by <PR URL>, merged in <merge commit SHA>\".",
          "result": "pass",
          "rule_id": "idea.bug-intake.f.closing-note"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:18",
          "reason": "If the PR is not merged, the skill stops and leaves the issue as it is.",
          "result": "pass",
          "rule_id": "idea.bug-intake.f.merged-first"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/close-and-label/SKILL.md:19,22",
          "reason": "The skill checks the issue state, does not reopen an already-closed issue, and closes it itself if it is still open.",
          "result": "pass",
          "rule_id": "idea.bug-intake.f.auto-closed"
        },
        {
          "check": "script",
          "reason": "3 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": "README.md:120,125,130",
          "reason": "The real-refs condition is present.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:126",
          "reason": "The no-agent-bypass condition is present.",
          "result": "pass",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:127",
          "reason": "The requester-cannot-approve condition is present.",
          "result": "pass",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:117-131",
          "reason": "Nothing for part F says a check counts only when it is required on the protected ref.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:117-131",
          "reason": "No recommendation for part F requires pinning check sources.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:118",
          "reason": "The workflow-protected condition is present.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:129",
          "reason": "The no-broader-bypass condition is present.",
          "result": "pass",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:124",
          "reason": "The plan-enforced condition is present.",
          "result": "pass",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:121,123,131",
          "reason": "Periodic verification is stated.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:119",
          "reason": "The CODEOWNERS recommendation with required code-owner review is present.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "README.md:122-127",
          "reason": "merge-rules is recommended.",
          "result": "pass",
          "rule_id": "outside.merge.rule-for-agent-prs"
        },
        {
          "check": "judged",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.goal.no-must-hold-rule-in-skill"
        },
        {
          "check": "script",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.portable.plugin-layout"
        },
        {
          "check": "judged",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.reuse.reviewed-and-pinned"
        }
      ],
      "status": "built"
    },
    {
      "goal_result": "not assessed",
      "goal_verdict": null,
      "harness_result": "not applicable",
      "outside_dependencies": [
        "compromise-resistant-gate"
      ],
      "part_id": "G",
      "rule_results": [
        {
          "check": "script",
          "reason": "part A's hooks has no builder in this release, so its name cannot be checked",
          "result": "error",
          "rule_id": "links.parts"
        },
        {
          "check": "script",
          "reason": "4 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": "README.md:135,142,147,152",
          "reason": "The real-refs condition is present.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:143,148",
          "reason": "The no-agent-bypass condition is present.",
          "result": "pass",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:149",
          "reason": "The requester-cannot-approve condition is present.",
          "result": "pass",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:132-153",
          "reason": "Part G's gates rely on workflow-defined checks, but nothing says a check counts only when it is required on the protected ref.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:132-153",
          "reason": "No recommendation for part G requires pinning check sources.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:133,138",
          "reason": "The workflow-protected condition is present.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:139,151",
          "reason": "The no-broader-bypass condition is present.",
          "result": "pass",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:141,146",
          "reason": "The plan-enforced condition is present.",
          "result": "pass",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:136,140,145,153",
          "reason": "Periodic verification is stated.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:134",
          "reason": "The CODEOWNERS recommendation with required code-owner review is present.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "README.md:144-149",
          "reason": "merge-rules is recommended.",
          "result": "pass",
          "rule_id": "outside.merge.rule-for-agent-prs"
        }
      ],
      "status": "blocked"
    }
  ],
  "revision_digest": "e1805692c07794fb076d85404a8ce1d99581b7ad56af5cabea3935af53c2acde",
  "rules_digest": "93fec41536adbe0420026720fecbe03465b27f5f457695dc9d5704d422d7488a",
  "run_id": "78cd85df-fce7-4e2d-a70a-185a616379f0",
  "runtime_results": [
    {
      "case_id": "reproduce-explicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: Skill, Read; network: none requested; issue-42.md sha256 25860a9f5ed18ee7b25ffe65dc53952d65f41d572bffcd456661e7c3b159f6e8",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/reproduce/SKILL.md": "c657df4e103312fc3c875337b3015c5bdd6db10cc825a1e521ea067de2adb9a9",
        ".agents/skills/reproduce/references/requirements.md": "efe1922fced886a763fb805b9f2123ed35027afe2b65fec8c2a8b17687d56c50"
      },
      "harness": "claude-code",
      "harness_version": "2.1.302 (Claude Code)",
      "inventory": "observed",
      "observed_activation": "Skill tool called for reproduce",
      "part_id": "B",
      "prompt": "Use the reproduce skill on the bug in issue-42.md and tell me how you would reproduce it.",
      "reason": "Skill tool called for reproduce",
      "result": "pass",
      "run_id": "78cd85df-fce7-4e2d-a70a-185a616379f0"
    },
    {
      "case_id": "reproduce-implicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: Skill, Read; network: none requested; issue-42.md sha256 25860a9f5ed18ee7b25ffe65dc53952d65f41d572bffcd456661e7c3b159f6e8",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/reproduce/SKILL.md": "c657df4e103312fc3c875337b3015c5bdd6db10cc825a1e521ea067de2adb9a9",
        ".agents/skills/reproduce/references/requirements.md": "efe1922fced886a763fb805b9f2123ed35027afe2b65fec8c2a8b17687d56c50"
      },
      "harness": "claude-code",
      "harness_version": "2.1.302 (Claude Code)",
      "inventory": "observed",
      "observed_activation": "Skill tool called for reproduce",
      "part_id": "B",
      "prompt": "Can you repro the bug described in issue-42.md and check whether it is flaky?",
      "reason": "Skill tool called for reproduce",
      "result": "pass",
      "run_id": "78cd85df-fce7-4e2d-a70a-185a616379f0"
    },
    {
      "case_id": "reproduce-near-miss",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: Skill, Read; network: none requested; issue-42.md sha256 25860a9f5ed18ee7b25ffe65dc53952d65f41d572bffcd456661e7c3b159f6e8",
      "expected": "does-not-activate",
      "file_hashes": {
        ".agents/skills/reproduce/SKILL.md": "c657df4e103312fc3c875337b3015c5bdd6db10cc825a1e521ea067de2adb9a9",
        ".agents/skills/reproduce/references/requirements.md": "efe1922fced886a763fb805b9f2123ed35027afe2b65fec8c2a8b17687d56c50"
      },
      "harness": "claude-code",
      "harness_version": "2.1.302 (Claude Code)",
      "inventory": "observed",
      "observed_activation": null,
      "part_id": "B",
      "prompt": "Summarize in two sentences what issue-42.md is about; I do not need it reproduced.",
      "reason": "no Skill tool call for the candidate",
      "result": "pass",
      "run_id": "78cd85df-fce7-4e2d-a70a-185a616379f0"
    },
    {
      "case_id": "fix-and-pr-explicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: Skill, Read; network: none requested; issue-42.md sha256 25860a9f5ed18ee7b25ffe65dc53952d65f41d572bffcd456661e7c3b159f6e8",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/fix-and-pr/SKILL.md": "18a359c776eea82acdbe4d13a21ecc2ac9dfae881ab8e484bc44daef70cabd1e",
        ".agents/skills/fix-and-pr/agents/openai.yaml": "a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94",
        ".agents/skills/fix-and-pr/references/requirements.md": "9e6ad0a1f3fff8f948bb0c972ff011fc4ecfb266e2914618de896bbc71dbd84f"
      },
      "harness": "claude-code",
      "harness_version": "2.1.302 (Claude Code)",
      "inventory": "observed",
      "observed_activation": null,
      "part_id": "C",
      "prompt": "Use the fix-and-pr skill for the bug in issue-42.md and tell me the first steps you would take.",
      "reason": "the skill was not activated",
      "result": "fail",
      "run_id": "78cd85df-fce7-4e2d-a70a-185a616379f0"
    },
    {
      "case_id": "fix-and-pr-near-miss",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: Skill, Read; network: none requested; issue-42.md sha256 25860a9f5ed18ee7b25ffe65dc53952d65f41d572bffcd456661e7c3b159f6e8",
      "expected": "does-not-activate",
      "file_hashes": {
        ".agents/skills/fix-and-pr/SKILL.md": "18a359c776eea82acdbe4d13a21ecc2ac9dfae881ab8e484bc44daef70cabd1e",
        ".agents/skills/fix-and-pr/agents/openai.yaml": "a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94",
        ".agents/skills/fix-and-pr/references/requirements.md": "9e6ad0a1f3fff8f948bb0c972ff011fc4ecfb266e2914618de896bbc71dbd84f"
      },
      "harness": "claude-code",
      "harness_version": "2.1.302 (Claude Code)",
      "inventory": "observed",
      "observed_activation": null,
      "part_id": "C",
      "prompt": "What do you think causes the crash described in issue-42.md? Just give me your guess, no changes.",
      "reason": "no Skill tool call for the candidate",
      "result": "pass",
      "run_id": "78cd85df-fce7-4e2d-a70a-185a616379f0"
    },
    {
      "case_id": "close-and-label-explicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: Skill, Read; network: none requested; issue-42.md sha256 c17b6bc9f8f75e56f593c1cf4765e8f7e2fe5a4be4ccec915fc8437e6ef392b8",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/close-and-label/SKILL.md": "65989f132adcc3cbc403aaca9359719eba8496dcf21e54336f582c75d085f449",
        ".agents/skills/close-and-label/references/requirements.md": "0de99399c492825eed679fba31bd12279fe15ad017644a3740646fb05a0aac69"
      },
      "harness": "claude-code",
      "harness_version": "2.1.302 (Claude Code)",
      "inventory": "observed",
      "observed_activation": "Skill tool called for close-and-label",
      "part_id": "F",
      "prompt": "Use the close-and-label skill for the bug in issue-42.md and tell me what you would do.",
      "reason": "Skill tool called for close-and-label",
      "result": "pass",
      "run_id": "78cd85df-fce7-4e2d-a70a-185a616379f0"
    },
    {
      "case_id": "close-and-label-implicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: Skill, Read; network: none requested; issue-42.md sha256 c17b6bc9f8f75e56f593c1cf4765e8f7e2fe5a4be4ccec915fc8437e6ef392b8",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/close-and-label/SKILL.md": "65989f132adcc3cbc403aaca9359719eba8496dcf21e54336f582c75d085f449",
        ".agents/skills/close-and-label/references/requirements.md": "0de99399c492825eed679fba31bd12279fe15ad017644a3740646fb05a0aac69"
      },
      "harness": "claude-code",
      "harness_version": "2.1.302 (Claude Code)",
      "inventory": "observed",
      "observed_activation": "Skill tool called for close-and-label",
      "part_id": "F",
      "prompt": "The fix for the bug in issue-42.md is merged now. Close it out.",
      "reason": "Skill tool called for close-and-label",
      "result": "pass",
      "run_id": "78cd85df-fce7-4e2d-a70a-185a616379f0"
    },
    {
      "case_id": "close-and-label-near-miss",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: Skill, Read; network: none requested; issue-42.md sha256 c17b6bc9f8f75e56f593c1cf4765e8f7e2fe5a4be4ccec915fc8437e6ef392b8",
      "expected": "does-not-activate",
      "file_hashes": {
        ".agents/skills/close-and-label/SKILL.md": "65989f132adcc3cbc403aaca9359719eba8496dcf21e54336f582c75d085f449",
        ".agents/skills/close-and-label/references/requirements.md": "0de99399c492825eed679fba31bd12279fe15ad017644a3740646fb05a0aac69"
      },
      "harness": "claude-code",
      "harness_version": "2.1.302 (Claude Code)",
      "inventory": "observed",
      "observed_activation": null,
      "part_id": "F",
      "prompt": "List the dates mentioned in issue-42.md.",
      "reason": "no Skill tool call for the candidate",
      "result": "pass",
      "run_id": "78cd85df-fce7-4e2d-a70a-185a616379f0"
    }
  ],
  "scope": "First run: judged A, B, C, D, E, F, G",
  "scope_parts": null,
  "symlinks": {
    ".claude/skills/close-and-label": "../../.agents/skills/close-and-label",
    ".claude/skills/fix-and-pr": "../../.agents/skills/fix-and-pr",
    ".claude/skills/reproduce": "../../.agents/skills/reproduce"
  },
  "tool_versions": {
    "harness-forge-checkers": "7beeb29d229339f59695dccf5877b0efc53a7e117ff8fb0b7773c93c0d92e0df"
  },
  "whole_idea": {
    "facts": {
      "lethal_trifecta": true,
      "opens_prs": true,
      "plan_controls": "available",
      "reach": "public",
      "target_set": "both",
      "untrusted_repo": true
    },
    "hosting": {
      "plan": "free (assumed; the repositories it runs in vary)",
      "platform": "github",
      "visibility": "public"
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
      "harness_version": "2.1.302 (Claude Code)",
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
      "harness_version": "2.1.302 (Claude Code)",
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
      "harness_version": "2.1.302 (Claude Code)",
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
      "harness_version": "2.1.302 (Claude Code)",
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
