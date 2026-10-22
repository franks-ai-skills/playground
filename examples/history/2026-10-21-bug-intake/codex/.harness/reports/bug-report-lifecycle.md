# Verification report

- Run: `5d46ccd1-765d-41da-aed2-8a01d4eca896`
- Harness KB version: 0.1.0
- Contract digest: a95d731abff44dd7836ab770e9851fec878c314bdfcbf6b43bc51dc8c90a822c
- Confirmed parts: A1, A2, B, C, D, E
- Decision record digest: 6cd2d382a3614bd90329cfae4dd44f22ccb01057ac4bae9a409cb981c2113fb8
- Whole-idea answers and targets: `{"facts": {"bypass_mode": false, "lethal_trifecta": false, "opens_prs": false, "plan_controls": "available", "reach": "repository", "target_set": "both", "untrusted_repo": false}, "hosting": {"plan": "team", "platform": "github", "visibility": "private"}, "reach": "repository", "targets": ["claude-code", "codex"]}` (digest 8ecdc9123c6bac1eb00b4cbbb201f39377d341996027945dfd0db534bf363dd5)
- Rule content digest: 93fec41536adbe0420026720fecbe03465b27f5f457695dc9d5704d422d7488a
- Accepted Idea KB revision: 03caeb0fd62b468d5be723224f6a732f33ca3d8dc78f77fb6a3453bf87dfce4e
- Review scope: Extensive review (rarely needed): judged A1, A2, B, C, D, E
- Rule overrides: none
- Checker versions digest: 7beeb29d229339f59695dccf5877b0efc53a7e117ff8fb0b7773c93c0d92e0df

## Worker isolation

Workers ran under `best-effort-v1` with isolation status `not-certified`. Research, source-support and review workers run as independent CLI processes with explicit role inputs and the available restrictions. Complete tool absence and context, file and network isolation are not guaranteed; use trusted projects and operator-approved inputs.

- research worker: codex codex-cli 0.163.0, model account default, launcher independent-process, configuration d28f2bef0b1a2d477e3a44729b3bbe7971f0df2924cf44e48fc1fa9f21618a1b, controls: command: ["codex", "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--ephemeral", "--json", "--color", "never", "--strict-config", "-C", "<workspace>", "--output-schema", "<workspace>/output-schema.json", "-c", "approval_policy=\"never\"", "-c", "project_doc_max_bytes=0", "-c", "mcp_servers={}", "-c", "apps._default.enabled=false", "-c", "web_search=\"live\"", "-c", "default_permissions=\"forge-worker\"", "-c", "permissions.forge-worker.filesystem={\":root\"=\"deny\", \":minimal\"=\"read\", \"<workspace>\"=\"read\"}", "-c", "permissions.forge-worker.network.enabled=false", "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "features.hooks=false", "-c", "features.multi_agent=false", "-c", "features.browser_use=false", "-c", "features.browser_use_external=false", "-c", "features.computer_use=false", "-c", "features.image_generation=false", "-c", "features.remote_plugin=false", "-c", "features.tool_suggest=false", "-c", "features.view_image=false", "-c", "features.shell_tool=false", "-c", "features.unified_exec=false", "-"]; environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (ChatGPT), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- source-support worker: codex codex-cli 0.163.0, model account default, launcher independent-process, configuration faf9aa6201600adb491f3d870fcedefb9b6cf86d13bde50a61d7e3e8b755540f, controls: command: ["codex", "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--ephemeral", "--json", "--color", "never", "--strict-config", "-C", "<workspace>", "--output-schema", "<workspace>/output-schema.json", "-c", "approval_policy=\"never\"", "-c", "project_doc_max_bytes=0", "-c", "mcp_servers={}", "-c", "apps._default.enabled=false", "-c", "web_search=\"disabled\"", "-c", "default_permissions=\"forge-worker\"", "-c", "permissions.forge-worker.filesystem={\":root\"=\"deny\", \":minimal\"=\"read\", \"<workspace>\"=\"read\"}", "-c", "permissions.forge-worker.network.enabled=false", "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "features.hooks=false", "-c", "features.multi_agent=false", "-c", "features.browser_use=false", "-c", "features.browser_use_external=false", "-c", "features.computer_use=false", "-c", "features.image_generation=false", "-c", "features.remote_plugin=false", "-c", "features.tool_suggest=false", "-c", "features.view_image=false", "-c", "features.shell_tool=false", "-c", "features.unified_exec=false", "-"]; environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (ChatGPT), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- review worker: codex codex-cli 0.163.0, model account default, launcher independent-process, configuration 0952a1dca9b7ff5765fac8f2121e99b97aa2bce930524db4b061e9ca569f2876, controls: command: ["codex", "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--ephemeral", "--json", "--color", "never", "--strict-config", "-C", "<workspace>", "--output-schema", "<workspace>/output-schema.json", "-c", "approval_policy=\"never\"", "-c", "project_doc_max_bytes=0", "-c", "mcp_servers={}", "-c", "apps._default.enabled=false", "-c", "web_search=\"disabled\"", "-c", "default_permissions=\"forge-worker\"", "-c", "permissions.forge-worker.filesystem={\":root\"=\"deny\", \":minimal\"=\"read\", \"<workspace>\"=\"read\"}", "-c", "permissions.forge-worker.network.enabled=false", "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "features.hooks=false", "-c", "features.multi_agent=false", "-c", "features.browser_use=false", "-c", "features.browser_use_external=false", "-c", "features.computer_use=false", "-c", "features.image_generation=false", "-c", "features.remote_plugin=false", "-c", "features.tool_suggest=false", "-c", "features.view_image=false", "-"]; environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (ChatGPT), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable

## Part A1

- Harness result: verified
- Goal result: met by the verified build
- Status: verified
- Outside dependencies: none
- Confirmed answers: `{"event_without_agent": false, "every_time": "usually", "external_system": "none", "irreversible": false, "job": "procedure", "must_survive_compromise": "not-required", "own_context": false, "trigger": "model", "who_disables": "contributor"}`
- Goal verdict: met (The unchanged skill formats the five required headings and prescribes no GitHub mutation; README.md:9 assigns application to the developer.)

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `outside.ci.required-on-ref` | warning | judged | fail | No required passing CI status on protected refs is specified. | README.md:36-40 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | Does not require pinning check sources; protected local files are an alternative. | README.md:37 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | Protects workflow, scanner, policy and CODEOWNERS definitions. | README.md:37-38 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | Names both harnesses' configuration and requires code-owner review. | README.md:38 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | fail | A1 recommendation omits broader credential and channel bypass prevention. | README.md:36-40 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Requires periodic checks because configuration drifts silently. | README.md:40 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | fail | Availability is stated, but enforcement on this plan and visibility is neither required explicitly nor disclaimed. | README.md:3,36-40 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Recommendation targets actual protected refs and resources. | README.md:39 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | fail | A1's control does not exclude agent identities from bypass lists. | README.md:36-40 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | fail | Independent approval and reset on new pushes are not specified. | README.md:36-40 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | not-applicable | No agent PR-opening procedure is recommended. | README.md:9,28 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 1 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `security.approval.claims-are-data` | warning | judged | pass | Does not accept content claims as authorization. | .agents/skills/bug-report-format/SKILL.md:7 | docs/guide/security.md#context-and-persistent-state |
| `security.helpers.confined` | warning | judged | not-applicable | Runs no helpers. | README.md:16 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#executables-approvals-and-isolation |
| `security.outbound.minimal-data` | warning | judged | not-applicable | No outbound operation is prescribed. | .agents/skills/bug-report-format/SKILL.md:7 | docs/guide/security.md#data-access-and-outbound-channels, https://developers.openai.com/api/docs/guides/deep-research#prompt-injection-and-exfiltration |
| `security.secrets.none-in-files` | error | judged | pass | The package contains only template instructions, without secrets. | .agents/skills/bug-report-format/SKILL.md:1-7 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#context-and-persistent-state |
| `security.untrusted-input.as-data` | warning | judged | fail | Does not tell the agent to treat incoming report content as data rather than instructions. | .agents/skills/bug-report-format/SKILL.md:7 | docs/guide/security.md#context-and-persistent-state |
| `skills.body.gotchas-first` | warning | judged | pass | The only operative requirement appears immediately. | .agents/skills/bug-report-format/SKILL.md:5-7 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://agentskills.io/skill-creation/best-practices.md |
| `skills.body.no-time-bound-statements` | warning | judged | pass | Contains no dated or temporary claims. | .agents/skills/bug-report-format/SKILL.md:1-7 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.only-what-model-lacks` | warning | judged | pass | Supplies only the team-specific heading contract. | .agents/skills/bug-report-format/SKILL.md:7 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.reasons-before-hard-rules` | warning | judged | pass | The template purpose explains the single formatting instruction; no emphatic wording appears. | .agents/skills/bug-report-format/SKILL.md:3-7 | docs/best-practices/skills.md#7-explain-the-why-before-adding-hard-rules |
| `skills.body.size` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, docs/concepts/skills.md#body, https://code.claude.com/docs/en/skills, https://agentskills.io/specification |
| `skills.body.strictness-matches-fragility` | warning | judged | pass | Prescribes only the required template. | .agents/skills/bug-report-format/SKILL.md:7 | docs/best-practices/skills.md#5-match-strictness-to-fragility, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.description.boundary` | warning | judged | pass | Explicitly excludes triage. | .agents/skills/bug-report-format/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.description.concise` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, docs/research-notes/agent-harness-best-practices/skills.md |
| `skills.description.length` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/opencode/skills.md#format, https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs, https://opencode.ai/docs/skills/ |
| `skills.description.no-workflow-steps` | warning | judged | pass | Describes the output rather than workflow steps. | .agents/skills/bug-report-format/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md |
| `skills.description.voice` | warning | judged | pass | Uses third-person description. | .agents/skills/bug-report-format/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition |
| `skills.description.what-and-when` | warning | judged | pass | Names formatting, the template and the incoming-report trigger. | .agents/skills/bug-report-format/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://learn.chatgpt.com/docs/build-skills, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.frontmatter.valid` | error | script | pass | 1 skill(s) checked | - | docs/vendors/opencode/skills.md#format, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/claude-code/skills.md#format, docs/concepts/skills.md#frontmatter, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.goal.no-must-hold-rule-in-skill` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#13-move-rules-that-must-hold-every-time-into-hooks, https://code.claude.com/docs/en/skills |
| `skills.inputs.from-message` | warning | judged | fail | Does not say to obtain the report from the user's message or ask when it is missing. | .agents/skills/bug-report-format/SKILL.md:7 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, docs/concepts/skills.md#body |
| `skills.invocation.both-flags` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#invocation-policy-in-both-leads, docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.invocation.side-effects-user-invoked` | error | judged | not-applicable | Only formats text; the developer applies it. | README.md:9 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.name.format` | error | script | pass | 1 skill(s) checked | - | docs/guide/skills.md#portability, docs/concepts/skills.md#frontmatter, docs/vendors/opencode/skills.md#format, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.package.no-auxiliary-docs` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#anti-patterns, https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md |
| `skills.portable.frontmatter` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/best-practices/skills.md#12-keep-one-canonical-copy-with-portable-frontmatter, https://code.claude.com/docs/en/skills |
| `skills.portable.layout` | error | script | pass | 1 skill(s) linked | - | docs/concepts/skills.md#directory-layout, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.portable.no-claude-placeholders` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#body, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills |
| `skills.portable.plugin-layout` | error | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#directory-layout, docs/vendors/claude-code/plugins.md#standard-layout, docs/vendors/codex/plugins.md#plugin-layout, https://code.claude.com/docs/en/plugins/manifest-reference, https://developers.openai.com/codex/plugins/build |
| `skills.references.load-conditions` | warning | judged | not-applicable | The package has no reference files. | README.md:16 | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/best-practices.md |
| `skills.references.one-level` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/specification |
| `skills.references.resolve` | error | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.reuse.reviewed-and-pinned` | error | judged | pass | Records full package review, an immutable upstream commit and local hash. | README.md:16 | docs/best-practices/skills.md#security, https://owasp.github.io/www-project-agentic-skills-top-10/ast01 |
| `skills.scope.committed-for-automation` | warning | judged | not-applicable | No CI or cloud execution of this formatter is required. | README.md:9 | docs/concepts/skills.md#directory-layout, https://code.claude.com/docs/en/skills |
| `skills.scripts.agent-caller` | warning | judged | not-applicable | No scripts are bundled. | README.md:16 | docs/best-practices/skills.md#6-put-deterministic-logic-in-tested-scripts, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/using-scripts.md |
| `skills.security.allowed-tools-least-privilege` | warning | judged | not-applicable | No allowed-tools grant is present. | .agents/skills/bug-report-format/SKILL.md:1-4 | docs/best-practices/skills.md#security, docs/vendors/claude-code/skills.md#limits-and-gotchas, https://code.claude.com/docs/en/skills |
| `skills.security.no-surprising-content` | error | judged | pass | Only the advertised formatting instruction appears. | .agents/skills/bug-report-format/SKILL.md:1-7 | docs/best-practices/skills.md#security, https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md |

Contested `skills.body.reasons-before-hard-rules`:
- All-caps ALWAYS or NEVER is a yellow flag; explain the reasoning instead (https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md, https://agentskills.io/skill-creation/evaluating-skills.md)
- Discipline skills need firm prohibitions and rationalization tables (https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

Contested `skills.description.voice`:
- Always write in the third person; an inconsistent point of view can cause discovery problems (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Use imperative "Use this skill when" phrasing for the trigger (https://agentskills.io/skill-creation/optimizing-descriptions.md, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)

## Part A2

- Harness result: not applicable
- Goal result: not met
- Status: decided
- Outside dependencies: none
- Confirmed answers: `{"event_without_agent": false, "every_time": "always", "external_system": "cli", "irreversible": false, "job": "procedure", "must_survive_compromise": "not-required", "own_context": false, "script_checkable": false, "who_disables": "contributor"}`

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `outside.ci.required-on-ref` | warning | judged | fail | Does not require passing CI on protected refs. | README.md:41-45 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | Does not require all check sources to be pinned. | README.md:42 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | Protects gate definitions and CODEOWNERS itself. | README.md:42-43 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | Covers both harnesses' agent configuration and requires code-owner review. | README.md:43 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | fail | Omits broader credential and channel bypass prevention. | README.md:41-45 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Requires periodic configuration verification. | README.md:45 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | fail | Availability does not establish or explicitly require enforcement for the stated plan and visibility. | README.md:3,41-45 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Targets actual protected refs and resources. | README.md:44 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | fail | A2 recommendation omits exclusions from bypass lists. | README.md:41-45 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | fail | Does not require independent approval or reset after pushes. | README.md:41-45 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | not-applicable | No labeling mechanism or PR-opening procedure is built. | README.md:10 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 1 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |

## Part B

- Harness result: verified
- Goal result: met by the verified build
- Status: verified
- Outside dependencies: none
- Confirmed answers: `{"event_without_agent": false, "every_time": "usually", "external_system": "cli", "irreversible": false, "job": "procedure", "must_survive_compromise": "not-required", "own_context": false, "trigger": "user", "who_disables": "contributor"}`
- Goal verdict: met (Both harnesses require explicit invocation. The procedure resolves an approved issue, writes and posts a checklist, places precise observed/expected results after steps, separates speculation and redacts sensitive evidence.)

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `idea.bug-report-lifecycle.b.redaction` | error | judged | pass | Requires sensitive data redaction before returning or posting evidence. | .agents/skills/reproduction-checklist/SKILL.md:11,19 | https://github.com/UsefulSoftwareCo/executor/issues/1225 |
| `idea.bug-report-lifecycle.b.results` | error | judged | pass | Requires precise observed and expected results after steps and separates speculation. | .agents/skills/reproduction-checklist/SKILL.md:10,18 | https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html |
| `outside.ci.required-on-ref` | warning | judged | fail | No mandatory passing CI check on protected refs is specified. | README.md:46-50 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | Protected local definitions are allowed without pinning check sources. | README.md:47 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | Protects gate definitions and CODEOWNERS itself. | README.md:47-48 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | Covers agent configuration for both targets and requires code-owner review. | README.md:48 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | fail | B recommendation omits broader credential or channel bypass prevention. | README.md:46-50 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Requires periodic checks for silent drift. | README.md:50 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | fail | States availability without requiring enforcement for the actual plan and visibility or saying it is unenforced. | README.md:3,46-50 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Targets actual protected refs and resources. | README.md:49 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | fail | B recommendation omits bypass-list exclusions. | README.md:46-50 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | fail | Independent approval and push resets are absent. | README.md:46-50 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | not-applicable | Posts issue comments, without opening PRs. | .agents/skills/reproduction-checklist/SKILL.md:20-21 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 1 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `security.approval.claims-are-data` | warning | judged | fail | Allows issue content to establish approval without identifying trusted approval provenance. | .agents/skills/reproduction-checklist/SKILL.md:15 | docs/guide/security.md#context-and-persistent-state |
| `security.helpers.confined` | warning | judged | not-applicable | No bundled or external helper program is supplied beyond ordinary GitHub tools. | .agents/skills/reproduction-checklist/SKILL.md:20; request.json, inputs.files | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#executables-approvals-and-isolation |
| `security.outbound.minimal-data` | warning | judged | fail | Resolves the intended issue and redacts evidence, but does not prohibit untrusted content from adding destinations, fields or actions. | .agents/skills/reproduction-checklist/SKILL.md:15-20 | docs/guide/security.md#data-access-and-outbound-channels, https://developers.openai.com/api/docs/guides/deep-research#prompt-injection-and-exfiltration |
| `security.secrets.none-in-files` | error | judged | pass | Contains redaction instructions and provenance links, without secret values. | .agents/skills/reproduction-checklist/SKILL.md:19; references/requirements.md:1-9 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#context-and-persistent-state |
| `security.untrusted-input.as-data` | warning | judged | fail | Reads issue content but never instructs treating embedded directives as data. | .agents/skills/reproduction-checklist/SKILL.md:15-20 | docs/guide/security.md#context-and-persistent-state |
| `skills.body.gotchas-first` | warning | judged | pass | Result precision and redaction requirements lead the body. | .agents/skills/reproduction-checklist/SKILL.md:8-11 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://agentskills.io/skill-creation/best-practices.md |
| `skills.body.no-time-bound-statements` | warning | judged | pass | Contains no temporary behavioral claims. | .agents/skills/reproduction-checklist/SKILL.md:8-24 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.only-what-model-lacks` | warning | judged | pass | Provides workflow-specific evidence, approval, redaction and posting constraints. | .agents/skills/reproduction-checklist/SKILL.md:15-21 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.reasons-before-hard-rules` | warning | judged | pass | Instructions connect precision to later checking and safe CLI handling to avoiding interpolation. | .agents/skills/reproduction-checklist/SKILL.md:17-20 | docs/best-practices/skills.md#7-explain-the-why-before-adding-hard-rules |
| `skills.body.size` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, docs/concepts/skills.md#body, https://code.claude.com/docs/en/skills, https://agentskills.io/specification |
| `skills.body.strictness-matches-fragility` | warning | judged | pass | Prescribes evidence and safe posting, with explicit draft and unavailable-posting fallbacks. | .agents/skills/reproduction-checklist/SKILL.md:15-21 | docs/best-practices/skills.md#5-match-strictness-to-fragility, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.description.boundary` | warning | judged | pass | Excludes adjacent formatting, labeling, fixing, checking and closing tasks. | .agents/skills/reproduction-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.description.concise` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, docs/research-notes/agent-harness-best-practices/skills.md |
| `skills.description.length` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/opencode/skills.md#format, https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs, https://opencode.ai/docs/skills/ |
| `skills.description.no-workflow-steps` | warning | judged | pass | Describes the task and trigger without procedural steps. | .agents/skills/reproduction-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md |
| `skills.description.voice` | warning | judged | pass | Uses impersonal task language without I or you. | .agents/skills/reproduction-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition |
| `skills.description.what-and-when` | warning | judged | pass | Names checklist writing and posting and an explicit approved-issue request. | .agents/skills/reproduction-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://learn.chatgpt.com/docs/build-skills, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.frontmatter.valid` | error | script | pass | 1 skill(s) checked | - | docs/vendors/opencode/skills.md#format, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/claude-code/skills.md#format, docs/concepts/skills.md#frontmatter, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.goal.no-must-hold-rule-in-skill` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#13-move-rules-that-must-hold-every-time-into-hooks, https://code.claude.com/docs/en/skills |
| `skills.inputs.from-message` | warning | judged | pass | Resolves inputs from the request and asks for missing issue or approval information. | .agents/skills/reproduction-checklist/SKILL.md:15 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, docs/concepts/skills.md#body |
| `skills.invocation.both-flags` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#invocation-policy-in-both-leads, docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.invocation.side-effects-user-invoked` | error | judged | pass | Both harnesses disable implicit invocation. | .agents/skills/reproduction-checklist/SKILL.md:4; .agents/skills/reproduction-checklist/agents/openai.yaml:1-2 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.name.format` | error | script | pass | 1 skill(s) checked | - | docs/guide/skills.md#portability, docs/concepts/skills.md#frontmatter, docs/vendors/opencode/skills.md#format, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.package.no-auxiliary-docs` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#anti-patterns, https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md |
| `skills.portable.frontmatter` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/best-practices/skills.md#12-keep-one-canonical-copy-with-portable-frontmatter, https://code.claude.com/docs/en/skills |
| `skills.portable.layout` | error | script | pass | 1 skill(s) linked | - | docs/concepts/skills.md#directory-layout, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.portable.no-claude-placeholders` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#body, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills |
| `skills.portable.plugin-layout` | error | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#directory-layout, docs/vendors/claude-code/plugins.md#standard-layout, docs/vendors/codex/plugins.md#plugin-layout, https://code.claude.com/docs/en/plugins/manifest-reference, https://developers.openai.com/codex/plugins/build |
| `skills.references.load-conditions` | warning | judged | pass | Names the reference and its provenance lookup condition; substantive requirements stay in SKILL.md. | .agents/skills/reproduction-checklist/SKILL.md:23-24; references/requirements.md:3-9 | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/best-practices.md |
| `skills.references.one-level` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/specification |
| `skills.references.resolve` | error | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.reuse.reviewed-and-pinned` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#security, https://owasp.github.io/www-project-agentic-skills-top-10/ast01 |
| `skills.scope.committed-for-automation` | warning | judged | not-applicable | This is an interactive posting procedure, not a CI or cloud dependency. | README.md:3,30 | docs/concepts/skills.md#directory-layout, https://code.claude.com/docs/en/skills |
| `skills.scripts.agent-caller` | warning | judged | not-applicable | No bundled scripts are present. | request.json, inputs.files | docs/best-practices/skills.md#6-put-deterministic-logic-in-tested-scripts, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/using-scripts.md |
| `skills.security.allowed-tools-least-privilege` | warning | judged | not-applicable | No allowed-tools grant is declared. | .agents/skills/reproduction-checklist/SKILL.md:1-5 | docs/best-practices/skills.md#security, docs/vendors/claude-code/skills.md#limits-and-gotchas, https://code.claude.com/docs/en/skills |
| `skills.security.no-surprising-content` | error | judged | pass | Operations match the advertised checklist posting task. | .agents/skills/reproduction-checklist/SKILL.md:15-21 | docs/best-practices/skills.md#security, https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md |

Contested `skills.body.reasons-before-hard-rules`:
- All-caps ALWAYS or NEVER is a yellow flag; explain the reasoning instead (https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md, https://agentskills.io/skill-creation/evaluating-skills.md)
- Discipline skills need firm prohibitions and rationalization tables (https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

Contested `skills.description.voice`:
- Always write in the third person; an inconsistent point of view can cause discovery problems (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Use imperative "Use this skill when" phrasing for the trigger (https://agentskills.io/skill-creation/optimizing-descriptions.md, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)

## Part C

- Harness result: verified
- Goal result: depends on outside controls
- Status: verified
- Outside dependencies: compromise-resistant-gate
- Confirmed answers: `{"event_without_agent": false, "every_time": "usually", "external_system": "cli", "irreversible": false, "job": "procedure", "must_survive_compromise": "required", "own_context": false, "trigger": "user"}`
- Goal verdict: met (The files do their share: assess every item for the latest SHA, reject stale evidence, recheck for pushes and require an outside protected required-status gate. The session verdict remains advisory; merge enforcement depends on the recommended, unverified outside control.)

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `idea.bug-report-lifecycle.c.latest-commit` | error | judged | pass | Requires all items to pass for the latest SHA and rechecks for pushes. | .agents/skills/check-fix-checklist/SKILL.md:10,16-18 | https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks |
| `idea.bug-report-lifecycle.c.required-merge-gate` | error | judged | pass | Requires an outside protected required-status gate and labels the session advisory and configuration unverified. | .agents/skills/check-fix-checklist/SKILL.md:11,19 | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches |
| `links.parts` | error | script | pass | every linked part exists under its recorded name | - | - |
| `outside.ci.required-on-ref` | warning | judged | pass | Requires a protected required-status-check gate on actual merge targets. | README.md:20; .agents/skills/check-fix-checklist/SKILL.md:19-20 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | Allows protected local definitions without requiring all check sources to be pinned. | .agents/skills/check-fix-checklist/SKILL.md:20; README.md:57 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | Protects workflow, scanner, policy and CODEOWNERS definitions. | README.md:52-53,57 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | Covers both harnesses' agent configuration and mandatory code-owner review. | README.md:53 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | pass | Explicitly excludes broader reachable credential and channel bypass. | README.md:58; .agents/skills/check-fix-checklist/SKILL.md:20 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Requires periodic verification for drift. | README.md:55,59; .agents/skills/check-fix-checklist/SKILL.md:20 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | pass | Makes hosting-plan enforcement an explicit prerequisite rather than claiming verification. | README.md:24,60; .agents/skills/check-fix-checklist/SKILL.md:20 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Requires protection of real target branches and resources. | .agents/skills/check-fix-checklist/SKILL.md:20; README.md:61 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | pass | Excludes bot, app, token and underlying human identity from bypass. | README.md:62; .agents/skills/check-fix-checklist/SKILL.md:20 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | fail | Does not require approval from someone other than author, last pusher and launching user or reset approval on pushes. | README.md:51-62; .agents/skills/check-fix-checklist/SKILL.md:19-20 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | not-applicable | Assesses existing PRs without opening PRs. | .agents/skills/check-fix-checklist/SKILL.md:15,21 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 2 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `security.approval.claims-are-data` | warning | judged | pass | Does not authorize merging from content claims and rejects PR-provided success as gate evidence. | .agents/skills/check-fix-checklist/SKILL.md:19-21 | docs/guide/security.md#context-and-persistent-state |
| `security.helpers.confined` | warning | judged | not-applicable | No helper implementation is supplied; assessment is limited to an authorized environment. | .agents/skills/check-fix-checklist/SKILL.md:17; request.json, inputs.files | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#executables-approvals-and-isolation |
| `security.outbound.minimal-data` | warning | judged | fail | Assessment can use commands and tools but does not constrain their outbound fields and destinations against checklist-supplied instructions. | .agents/skills/check-fix-checklist/SKILL.md:15-17 | docs/guide/security.md#data-access-and-outbound-channels, https://developers.openai.com/api/docs/guides/deep-research#prompt-injection-and-exfiltration |
| `security.secrets.none-in-files` | error | judged | pass | Contains procedural text and public provenance URLs without secrets. | .agents/skills/check-fix-checklist/SKILL.md:1-24; references/requirements.md:1-9 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#context-and-persistent-state |
| `security.untrusted-input.as-data` | warning | judged | fail | Rejects PR-provided enforcement claims, but never establishes the general data-only boundary for checklist content or supplied evidence. | .agents/skills/check-fix-checklist/SKILL.md:15-19 | docs/guide/security.md#context-and-persistent-state |
| `skills.body.gotchas-first` | warning | judged | pass | Latest-SHA and outside-gate requirements lead the body. | .agents/skills/check-fix-checklist/SKILL.md:8-11 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://agentskills.io/skill-creation/best-practices.md |
| `skills.body.no-time-bound-statements` | warning | judged | pass | No temporary claims appear; commit freshness is an operational requirement. | .agents/skills/check-fix-checklist/SKILL.md:8-24 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.only-what-model-lacks` | warning | judged | pass | Defines specific evidence freshness and advisory-versus-gate behavior. | .agents/skills/check-fix-checklist/SKILL.md:15-21 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.reasons-before-hard-rules` | warning | judged | pass | Explains stale evidence and why an advisory session cannot enforce the merge guarantee. | .agents/skills/check-fix-checklist/SKILL.md:16-20 | docs/best-practices/skills.md#7-explain-the-why-before-adding-hard-rules |
| `skills.body.size` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, docs/concepts/skills.md#body, https://code.claude.com/docs/en/skills, https://agentskills.io/specification |
| `skills.body.strictness-matches-fragility` | warning | judged | pass | Strict evidence and gate constraints address false passing; missing evidence has explicit fallbacks. | .agents/skills/check-fix-checklist/SKILL.md:16-20 | docs/best-practices/skills.md#5-match-strictness-to-fragility, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.description.boundary` | warning | judged | pass | Excludes checklist creation, implementation, CI repair, merging and closing. | .agents/skills/check-fix-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.description.concise` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, docs/research-notes/agent-harness-best-practices/skills.md |
| `skills.description.length` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/opencode/skills.md#format, https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs, https://opencode.ai/docs/skills/ |
| `skills.description.no-workflow-steps` | warning | judged | pass | States the task and output rather than enumerating procedure. | .agents/skills/check-fix-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md |
| `skills.description.voice` | warning | judged | pass | Uses impersonal task phrasing. | .agents/skills/check-fix-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition |
| `skills.description.what-and-when` | warning | judged | pass | Names checklist verification, latest-commit evidence and the pre-merge request trigger. | .agents/skills/check-fix-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://learn.chatgpt.com/docs/build-skills, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.frontmatter.valid` | error | script | pass | 1 skill(s) checked | - | docs/vendors/opencode/skills.md#format, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/claude-code/skills.md#format, docs/concepts/skills.md#frontmatter, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.goal.no-must-hold-rule-in-skill` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#13-move-rules-that-must-hold-every-time-into-hooks, https://code.claude.com/docs/en/skills |
| `skills.inputs.from-message` | warning | judged | pass | Resolves inputs from the request and asks for missing checklist association. | .agents/skills/check-fix-checklist/SKILL.md:15 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, docs/concepts/skills.md#body |
| `skills.invocation.both-flags` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#invocation-policy-in-both-leads, docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.invocation.side-effects-user-invoked` | error | judged | pass | Both harnesses prevent implicit invocation. | .agents/skills/check-fix-checklist/SKILL.md:4; .agents/skills/check-fix-checklist/agents/openai.yaml:1-2 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.name.format` | error | script | pass | 1 skill(s) checked | - | docs/guide/skills.md#portability, docs/concepts/skills.md#frontmatter, docs/vendors/opencode/skills.md#format, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.package.no-auxiliary-docs` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#anti-patterns, https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md |
| `skills.portable.frontmatter` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/best-practices/skills.md#12-keep-one-canonical-copy-with-portable-frontmatter, https://code.claude.com/docs/en/skills |
| `skills.portable.layout` | error | script | pass | 1 skill(s) linked | - | docs/concepts/skills.md#directory-layout, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.portable.no-claude-placeholders` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#body, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills |
| `skills.portable.plugin-layout` | error | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#directory-layout, docs/vendors/claude-code/plugins.md#standard-layout, docs/vendors/codex/plugins.md#plugin-layout, https://code.claude.com/docs/en/plugins/manifest-reference, https://developers.openai.com/codex/plugins/build |
| `skills.references.load-conditions` | warning | judged | pass | Names provenance reference with a lookup condition and keeps requirement text in the body. | .agents/skills/check-fix-checklist/SKILL.md:23-24; references/requirements.md:3-9 | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/best-practices.md |
| `skills.references.one-level` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/specification |
| `skills.references.resolve` | error | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.reuse.reviewed-and-pinned` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#security, https://owasp.github.io/www-project-agentic-skills-top-10/ast01 |
| `skills.scope.committed-for-automation` | warning | judged | pass | The checklist procedure is project-scoped and available to both harnesses. | README.md:28; request.json, inputs.links | docs/concepts/skills.md#directory-layout, https://code.claude.com/docs/en/skills |
| `skills.scripts.agent-caller` | warning | judged | not-applicable | No bundled scripts are present. | request.json, inputs.files | docs/best-practices/skills.md#6-put-deterministic-logic-in-tested-scripts, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/using-scripts.md |
| `skills.security.allowed-tools-least-privilege` | warning | judged | not-applicable | No allowed-tools grant is declared. | .agents/skills/check-fix-checklist/SKILL.md:1-5 | docs/best-practices/skills.md#security, docs/vendors/claude-code/skills.md#limits-and-gotchas, https://code.claude.com/docs/en/skills |
| `skills.security.no-surprising-content` | error | judged | pass | Instructions match checklist assessment and explicitly leave gate configuration and merging outside the procedure. | .agents/skills/check-fix-checklist/SKILL.md:15-21 | docs/best-practices/skills.md#security, https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md |

Contested `skills.body.reasons-before-hard-rules`:
- All-caps ALWAYS or NEVER is a yellow flag; explain the reasoning instead (https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md, https://agentskills.io/skill-creation/evaluating-skills.md)
- Discipline skills need firm prohibitions and rationalization tables (https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

Contested `skills.description.voice`:
- Always write in the third person; an inconsistent point of view can cause discovery problems (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Use imperative "Use this skill when" phrasing for the trigger (https://agentskills.io/skill-creation/optimizing-descriptions.md, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)

## Part D

- Harness result: verified
- Goal result: met by the verified build
- Status: verified
- Outside dependencies: none
- Confirmed answers: `{"event_without_agent": false, "every_time": "usually", "external_system": "cli", "irreversible": false, "job": "procedure", "must_survive_compromise": "not-required", "own_context": false, "trigger": "model", "who_disables": "contributor"}`
- Goal verdict: met (The procedure explicitly selects the intended PR, diagnoses current-SHA checks while distinguishing stale results, and returns a proposed fix for a developer to apply and push.)

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `idea.bug-report-lifecycle.d.current-commit` | error | judged | pass | Matches checks to the latest SHA, labels older results stale and rechecks for pushes. | .agents/skills/diagnose-ci/SKILL.md:9,15-16 | https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks |
| `idea.bug-report-lifecycle.d.explicit-pr` | error | judged | pass | Resolves the intended PR and explicitly selects it for gh pr checks. | .agents/skills/diagnose-ci/SKILL.md:10,14 | https://cli.github.com/manual/gh_pr_checks |
| `outside.ci.required-on-ref` | warning | judged | fail | Does not require passing CI on protected refs. | README.md:63-67 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | Allows protected local gate definitions without pinning check sources. | README.md:64 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | Protects workflow, scanner, policy and CODEOWNERS definitions. | README.md:64-65 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | Names both harnesses' configuration and requires code-owner review. | README.md:65 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | fail | D recommendation omits broader credential and channel bypass prevention. | README.md:63-67 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Requires periodic configuration checks for silent drift. | README.md:67 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | fail | Availability is stated without an explicit plan-and-visibility enforcement prerequisite or disclaimer of non-enforcement. | README.md:3,63-67 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Targets actual protected refs and resources. | README.md:66 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | fail | D recommendation omits bypass-list exclusions. | README.md:63-67 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | fail | Independent approval and reset after pushes are unspecified. | README.md:63-67 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | not-applicable | Explicitly forbids opening PRs. | .agents/skills/diagnose-ci/SKILL.md:20 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 1 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `security.approval.claims-are-data` | warning | judged | pass | No content claim grants authorization; modification remains forbidden. | .agents/skills/diagnose-ci/SKILL.md:15,20 | docs/guide/security.md#context-and-persistent-state |
| `security.helpers.confined` | warning | judged | not-applicable | No helper implementation is supplied or required beyond ordinary read tools. | .agents/skills/diagnose-ci/SKILL.md:15-17; request.json, inputs.files | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#executables-approvals-and-isolation |
| `security.outbound.minimal-data` | warning | judged | fail | Fixes repository and PR targeting but does not explicitly limit outbound fields or prevent fetched content from adding destinations and actions. | .agents/skills/diagnose-ci/SKILL.md:15-17 | docs/guide/security.md#data-access-and-outbound-channels, https://developers.openai.com/api/docs/guides/deep-research#prompt-injection-and-exfiltration |
| `security.secrets.none-in-files` | error | judged | pass | Contains procedure and public provenance links without secret values. | .agents/skills/diagnose-ci/SKILL.md:1-23; references/requirements.md:1-9 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#context-and-persistent-state |
| `security.untrusted-input.as-data` | warning | judged | fail | Reads logs and tool output without saying embedded instructions are untrusted data. | .agents/skills/diagnose-ci/SKILL.md:15-17 | docs/guide/security.md#context-and-persistent-state |
| `skills.body.gotchas-first` | warning | judged | pass | Latest-SHA and explicit-PR requirements appear first; read-only scope is in the description. | .agents/skills/diagnose-ci/SKILL.md:3,7-10 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://agentskills.io/skill-creation/best-practices.md |
| `skills.body.no-time-bound-statements` | warning | judged | pass | Contains no temporary claims. | .agents/skills/diagnose-ci/SKILL.md:7-23 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.only-what-model-lacks` | warning | judged | pass | Defines intended-PR selection, evidence freshness and read-only handoff constraints. | .agents/skills/diagnose-ci/SKILL.md:14-20 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.reasons-before-hard-rules` | warning | judged | pass | Explains why historical success is insufficient and assigns application and pushing to the developer. | .agents/skills/diagnose-ci/SKILL.md:16,20 | docs/best-practices/skills.md#7-explain-the-why-before-adding-hard-rules |
| `skills.body.size` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, docs/concepts/skills.md#body, https://code.claude.com/docs/en/skills, https://agentskills.io/specification |
| `skills.body.strictness-matches-fragility` | warning | judged | pass | Strict PR targeting and read-only constraints address wrong-target and mutation risks; missing access and evidence have fallbacks. | .agents/skills/diagnose-ci/SKILL.md:14-20 | docs/best-practices/skills.md#5-match-strictness-to-fragility, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.description.boundary` | warning | judged | pass | Explicitly excludes modifications, reruns, posting and merging. | .agents/skills/diagnose-ci/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.description.concise` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, docs/research-notes/agent-harness-best-practices/skills.md |
| `skills.description.length` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/opencode/skills.md#format, https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs, https://opencode.ai/docs/skills/ |
| `skills.description.no-workflow-steps` | warning | judged | pass | Describes scope and outcome without listing workflow steps. | .agents/skills/diagnose-ci/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md |
| `skills.description.voice` | warning | judged | pass | Uses impersonal task phrasing. | .agents/skills/diagnose-ci/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition |
| `skills.description.what-and-when` | warning | judged | pass | Names failing-CI diagnosis, developer-applied proposals and common failure triggers. | .agents/skills/diagnose-ci/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://learn.chatgpt.com/docs/build-skills, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.frontmatter.valid` | error | script | pass | 1 skill(s) checked | - | docs/vendors/opencode/skills.md#format, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/claude-code/skills.md#format, docs/concepts/skills.md#frontmatter, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.goal.no-must-hold-rule-in-skill` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#13-move-rules-that-must-hold-every-time-into-hooks, https://code.claude.com/docs/en/skills |
| `skills.inputs.from-message` | warning | judged | pass | Uses the developer message and session context and asks on ambiguity. | .agents/skills/diagnose-ci/SKILL.md:14 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, docs/concepts/skills.md#body |
| `skills.invocation.both-flags` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#invocation-policy-in-both-leads, docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.invocation.side-effects-user-invoked` | error | judged | not-applicable | Diagnosis is read-only and explicitly forbids external mutations. | .agents/skills/diagnose-ci/SKILL.md:20 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.name.format` | error | script | pass | 1 skill(s) checked | - | docs/guide/skills.md#portability, docs/concepts/skills.md#frontmatter, docs/vendors/opencode/skills.md#format, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.package.no-auxiliary-docs` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#anti-patterns, https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md |
| `skills.portable.frontmatter` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/best-practices/skills.md#12-keep-one-canonical-copy-with-portable-frontmatter, https://code.claude.com/docs/en/skills |
| `skills.portable.layout` | error | script | pass | 1 skill(s) linked | - | docs/concepts/skills.md#directory-layout, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.portable.no-claude-placeholders` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#body, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills |
| `skills.portable.plugin-layout` | error | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#directory-layout, docs/vendors/claude-code/plugins.md#standard-layout, docs/vendors/codex/plugins.md#plugin-layout, https://code.claude.com/docs/en/plugins/manifest-reference, https://developers.openai.com/codex/plugins/build |
| `skills.references.load-conditions` | warning | judged | pass | Names the provenance reference and when to read it. | .agents/skills/diagnose-ci/SKILL.md:22-23; references/requirements.md:3-9 | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/best-practices.md |
| `skills.references.one-level` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/specification |
| `skills.references.resolve` | error | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.reuse.reviewed-and-pinned` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#security, https://owasp.github.io/www-project-agentic-skills-top-10/ast01 |
| `skills.scope.committed-for-automation` | warning | judged | not-applicable | CI checks are inspected; CI does not need to run this interactive diagnosis skill. | README.md:3,32; .agents/skills/diagnose-ci/SKILL.md:15 | docs/concepts/skills.md#directory-layout, https://code.claude.com/docs/en/skills |
| `skills.scripts.agent-caller` | warning | judged | not-applicable | No bundled scripts are present. | request.json, inputs.files | docs/best-practices/skills.md#6-put-deterministic-logic-in-tested-scripts, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/using-scripts.md |
| `skills.security.allowed-tools-least-privilege` | warning | judged | not-applicable | No allowed-tools grant is declared. | .agents/skills/diagnose-ci/SKILL.md:1-4 | docs/best-practices/skills.md#security, docs/vendors/claude-code/skills.md#limits-and-gotchas, https://code.claude.com/docs/en/skills |
| `skills.security.no-surprising-content` | error | judged | pass | Only diagnosis and a developer-applied proposal are prescribed. | .agents/skills/diagnose-ci/SKILL.md:14-20 | docs/best-practices/skills.md#security, https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md |

Contested `skills.body.reasons-before-hard-rules`:
- All-caps ALWAYS or NEVER is a yellow flag; explain the reasoning instead (https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md, https://agentskills.io/skill-creation/evaluating-skills.md)
- Discipline skills need firm prohibitions and rationalization tables (https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

Contested `skills.description.voice`:
- Always write in the third person; an inconsistent point of view can cause discovery problems (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Use imperative "Use this skill when" phrasing for the trigger (https://agentskills.io/skill-creation/optimizing-descriptions.md, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)

## Part E

- Harness result: not applicable
- Goal result: depends on outside controls
- Status: decided
- Outside dependencies: compromise-resistant-gate
- Confirmed answers: `{"event_without_agent": false, "every_time": "usually", "external_system": "cli", "irreversible": true, "job": "procedure", "must_survive_compromise": "not-required", "own_context": false, "trigger": "model", "who_disables": "contributor"}`

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `outside.ci.required-on-ref` | warning | judged | fail | Does not specify a required passing CI gate on protected refs. | README.md:68-79 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | Protected local definitions are allowed without requiring pinned check sources. | README.md:69,74 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | Protects gate definitions and CODEOWNERS itself. | README.md:69-70,74 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | Covers agent configuration in both harnesses and requires code-owner review. | README.md:70 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | pass | Explicitly excludes broader credential or channel bypass. | README.md:75 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Requires periodic verification because configuration drifts silently. | README.md:72,76 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | pass | Explicitly makes plan and visibility enforcement a prerequisite. | README.md:73,77 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Targets real issue/customer resources and protected refs/resources. | README.md:22,71,78 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | pass | Excludes all agent identities, including the human behind its token. | README.md:79 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | fail | Does not specify independent approval or reset on pushes. | README.md:68-79 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | not-applicable | No agent PR-opening or closing mechanism is built. | README.md:14,22 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 2 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |

## Runtime tests

| Part | Case | Harness | Result | Observed | Reason |
| --- | --- | --- | --- | --- | --- |
| A1 | format-explicit | codex codex-cli 0.163.0 | not-run | - | Codex showed no observable activation signal |
| A1 | format-implicit | codex codex-cli 0.163.0 | not-run | - | Codex showed no observable activation signal |
| A1 | format-negative | codex codex-cli 0.163.0 | not-run | - | Codex has no observable signal that proves non-activation |
| B | checklist-explicit | codex codex-cli 0.163.0 | pass | instructions injected for .agents/skills/reproduction-checklist/SKILL.md (session rollout) | instructions injected for .agents/skills/reproduction-checklist/SKILL.md (session rollout) |
| B | checklist-negative | codex codex-cli 0.163.0 | not-run | - | Codex has no observable signal that proves non-activation |
| C | check-fix-explicit | codex codex-cli 0.163.0 | pass | read .agents/skills/check-fix-checklist/SKILL.md | read .agents/skills/check-fix-checklist/SKILL.md |
| C | check-fix-negative | codex codex-cli 0.163.0 | not-run | - | Codex has no observable signal that proves non-activation |
| D | diagnose-ci-explicit | codex codex-cli 0.163.0 | pass | read .agents/skills/diagnose-ci/SKILL.md | read .agents/skills/diagnose-ci/SKILL.md |
| D | diagnose-ci-implicit | codex codex-cli 0.163.0 | pass | read .agents/skills/diagnose-ci/SKILL.md | read .agents/skills/diagnose-ci/SKILL.md |
| D | diagnose-ci-negative | codex codex-cli 0.163.0 | not-run | - | Codex has no observable signal that proves non-activation |

Inventory gap: codex does not report the skills, plugins and MCP servers it loaded, so a user-level one that stayed loaded cannot be ruled out; its results are best-effort.

## Checked files

```
7d42ea98e84f3148e438267365a036dfa62353a463cd48ddd0f2dd1957ce31cd  .agents/skills/bug-report-format/SKILL.md
68e5c204a8671168e766391224467749b5eba53d8f2d70f4675d9ad575f4fcff  .agents/skills/check-fix-checklist/SKILL.md
a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94  .agents/skills/check-fix-checklist/agents/openai.yaml
0c92710d6b79f400ec5007a167318eb3e06a224f0c48dc13954bbb73b77c2098  .agents/skills/check-fix-checklist/references/requirements.md
cadfa2b00ff1f84a70668f5f1d64678a64f9adcad2fff1979a5131efd2d06f5d  .agents/skills/diagnose-ci/SKILL.md
0b35f83e9a82fe74728b9b86f6dd90e25cd4fa546065f3afdcfc3a4e45b7ee6e  .agents/skills/diagnose-ci/references/requirements.md
710ff3f495bb2847ba4c5ef601516f158eb7df7995c880f10032ed4bba8e9e3b  .agents/skills/reproduction-checklist/SKILL.md
a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94  .agents/skills/reproduction-checklist/agents/openai.yaml
6a89803edb0a5bce8995a56b34fb830512d93ea0646f17a791238b286a056328  .agents/skills/reproduction-checklist/references/requirements.md
87f570fe88b4587fa570b09b3df030986632909a8244e359b08b549d333dcbf8  README.md
link  .claude/skills/bug-report-format -> ../../.agents/skills/bug-report-format
link  .claude/skills/check-fix-checklist -> ../../.agents/skills/check-fix-checklist
link  .claude/skills/diagnose-ci -> ../../.agents/skills/diagnose-ci
link  .claude/skills/reproduction-checklist -> ../../.agents/skills/reproduction-checklist
```

## Report data

```json
{
  "answers": {
    "A1": {
      "event_without_agent": false,
      "every_time": "usually",
      "external_system": "none",
      "irreversible": false,
      "job": "procedure",
      "must_survive_compromise": "not-required",
      "own_context": false,
      "trigger": "model",
      "who_disables": "contributor"
    },
    "A2": {
      "event_without_agent": false,
      "every_time": "always",
      "external_system": "cli",
      "irreversible": false,
      "job": "procedure",
      "must_survive_compromise": "not-required",
      "own_context": false,
      "script_checkable": false,
      "who_disables": "contributor"
    },
    "B": {
      "event_without_agent": false,
      "every_time": "usually",
      "external_system": "cli",
      "irreversible": false,
      "job": "procedure",
      "must_survive_compromise": "not-required",
      "own_context": false,
      "trigger": "user",
      "who_disables": "contributor"
    },
    "C": {
      "event_without_agent": false,
      "every_time": "usually",
      "external_system": "cli",
      "irreversible": false,
      "job": "procedure",
      "must_survive_compromise": "required",
      "own_context": false,
      "trigger": "user"
    },
    "D": {
      "event_without_agent": false,
      "every_time": "usually",
      "external_system": "cli",
      "irreversible": false,
      "job": "procedure",
      "must_survive_compromise": "not-required",
      "own_context": false,
      "trigger": "model",
      "who_disables": "contributor"
    },
    "E": {
      "event_without_agent": false,
      "every_time": "usually",
      "external_system": "cli",
      "irreversible": true,
      "job": "procedure",
      "must_survive_compromise": "not-required",
      "own_context": false,
      "trigger": "model",
      "who_disables": "contributor"
    }
  },
  "bound_inputs": {
    "cases": {
      "A1": "e53b76f2c25db2f6320cc486120762f55ef387bdba4f36db8f4e522cd003beec",
      "A2": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
      "B": "e15fff006e4c24d6829d48bbeb7d11c05135851437fad216225691556cadc6fa",
      "C": "5f7d22f5677c9df8141c941cd87ed63a1fa4991e6c330056e9adb721e43cbc0c",
      "D": "c683ddde812f566756acbfc75aa47bb835f01c7e801ded581d45862486eb4c45",
      "E": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
    },
    "checkers": "7beeb29d229339f59695dccf5877b0efc53a7e117ff8fb0b7773c93c0d92e0df",
    "files": {
      ".agents/skills/bug-report-format/SKILL.md": "7d42ea98e84f3148e438267365a036dfa62353a463cd48ddd0f2dd1957ce31cd",
      ".agents/skills/check-fix-checklist/SKILL.md": "68e5c204a8671168e766391224467749b5eba53d8f2d70f4675d9ad575f4fcff",
      ".agents/skills/check-fix-checklist/agents/openai.yaml": "a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94",
      ".agents/skills/check-fix-checklist/references/requirements.md": "0c92710d6b79f400ec5007a167318eb3e06a224f0c48dc13954bbb73b77c2098",
      ".agents/skills/diagnose-ci/SKILL.md": "cadfa2b00ff1f84a70668f5f1d64678a64f9adcad2fff1979a5131efd2d06f5d",
      ".agents/skills/diagnose-ci/references/requirements.md": "0b35f83e9a82fe74728b9b86f6dd90e25cd4fa546065f3afdcfc3a4e45b7ee6e",
      ".agents/skills/reproduction-checklist/SKILL.md": "710ff3f495bb2847ba4c5ef601516f158eb7df7995c880f10032ed4bba8e9e3b",
      ".agents/skills/reproduction-checklist/agents/openai.yaml": "a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94",
      ".agents/skills/reproduction-checklist/references/requirements.md": "6a89803edb0a5bce8995a56b34fb830512d93ea0646f17a791238b286a056328",
      "README.md": "87f570fe88b4587fa570b09b3df030986632909a8244e359b08b549d333dcbf8"
    },
    "idea": "8ecdc9123c6bac1eb00b4cbbb201f39377d341996027945dfd0db534bf363dd5",
    "kb_version": "0.1.0",
    "overrides": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "parts": {
      "A1": "dd90006f32386e36fa7b0bce8926330b11355dafe668823be5dc4fbbe854a478",
      "A2": "037463ea27cceb919890720bfea045dc061c9080db5ef275d8aec4457a4a76cc",
      "B": "133f40a9e736ee0ada1dafaf4f7bcac79d9e7c2697c09ea5927fd6453bfc7dbb",
      "C": "7dbe37a05a039a47aec2a6125f1210551debc1e1e016aad2be738bc886c8f954",
      "D": "c79cbfd86ed878acd2818d6cdf55cdc3ac3eb4b2a4337abce35edf02bffc9674",
      "E": "83fd29a49a3603bdb772fd9fafdb27d50d97cdf56988ea1471ae217f87bd0407"
    },
    "revision": "03caeb0fd62b468d5be723224f6a732f33ca3d8dc78f77fb6a3453bf87dfce4e",
    "rules": "93fec41536adbe0420026720fecbe03465b27f5f457695dc9d5704d422d7488a",
    "symlinks": {
      ".claude/skills/bug-report-format": "../../.agents/skills/bug-report-format",
      ".claude/skills/check-fix-checklist": "../../.agents/skills/check-fix-checklist",
      ".claude/skills/diagnose-ci": "../../.agents/skills/diagnose-ci",
      ".claude/skills/reproduction-checklist": "../../.agents/skills/reproduction-checklist"
    },
    "worker": "93fb12f1c9e298ba69bb8cf058e31660c4b51f99a5e0236503cbcc69a56cb54a"
  },
  "confirmed_parts": [
    "A1",
    "A2",
    "B",
    "C",
    "D",
    "E"
  ],
  "contract_digest": "a95d731abff44dd7836ab770e9851fec878c314bdfcbf6b43bc51dc8c90a822c",
  "decision_digest": "6cd2d382a3614bd90329cfae4dd44f22ccb01057ac4bae9a409cb981c2113fb8",
  "file_hashes": {
    ".agents/skills/bug-report-format/SKILL.md": "7d42ea98e84f3148e438267365a036dfa62353a463cd48ddd0f2dd1957ce31cd",
    ".agents/skills/check-fix-checklist/SKILL.md": "68e5c204a8671168e766391224467749b5eba53d8f2d70f4675d9ad575f4fcff",
    ".agents/skills/check-fix-checklist/agents/openai.yaml": "a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94",
    ".agents/skills/check-fix-checklist/references/requirements.md": "0c92710d6b79f400ec5007a167318eb3e06a224f0c48dc13954bbb73b77c2098",
    ".agents/skills/diagnose-ci/SKILL.md": "cadfa2b00ff1f84a70668f5f1d64678a64f9adcad2fff1979a5131efd2d06f5d",
    ".agents/skills/diagnose-ci/references/requirements.md": "0b35f83e9a82fe74728b9b86f6dd90e25cd4fa546065f3afdcfc3a4e45b7ee6e",
    ".agents/skills/reproduction-checklist/SKILL.md": "710ff3f495bb2847ba4c5ef601516f158eb7df7995c880f10032ed4bba8e9e3b",
    ".agents/skills/reproduction-checklist/agents/openai.yaml": "a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94",
    ".agents/skills/reproduction-checklist/references/requirements.md": "6a89803edb0a5bce8995a56b34fb830512d93ea0646f17a791238b286a056328",
    "README.md": "87f570fe88b4587fa570b09b3df030986632909a8244e359b08b549d333dcbf8"
  },
  "idea_digest": "8ecdc9123c6bac1eb00b4cbbb201f39377d341996027945dfd0db534bf363dd5",
  "kb_version": "0.1.0",
  "overrides": [],
  "part_map": {
    "dirs": {
      "A1": ".agents/skills/bug-report-format",
      "B": ".agents/skills/reproduction-checklist",
      "C": ".agents/skills/check-fix-checklist",
      "D": ".agents/skills/diagnose-ci"
    },
    "files": {
      "A1": [
        ".agents/skills/bug-report-format/SKILL.md",
        "README.md"
      ],
      "A2": [
        "README.md"
      ],
      "B": [
        ".agents/skills/reproduction-checklist/SKILL.md",
        ".agents/skills/reproduction-checklist/agents/openai.yaml",
        ".agents/skills/reproduction-checklist/references/requirements.md",
        "README.md"
      ],
      "C": [
        ".agents/skills/check-fix-checklist/SKILL.md",
        ".agents/skills/check-fix-checklist/agents/openai.yaml",
        ".agents/skills/check-fix-checklist/references/requirements.md",
        "README.md"
      ],
      "D": [
        ".agents/skills/diagnose-ci/SKILL.md",
        ".agents/skills/diagnose-ci/references/requirements.md",
        "README.md"
      ],
      "E": [
        "README.md"
      ]
    },
    "links": {
      "A1": [
        ".claude/skills/bug-report-format"
      ],
      "B": [
        ".claude/skills/reproduction-checklist"
      ],
      "C": [
        ".claude/skills/check-fix-checklist"
      ],
      "D": [
        ".claude/skills/diagnose-ci"
      ]
    },
    "requirement_parts": [
      "B",
      "C",
      "D"
    ]
  },
  "parts": [
    {
      "goal_result": "met by the verified build",
      "goal_verdict": {
        "reason": "The unchanged skill formats the five required headings and prescribes no GitHub mutation; README.md:9 assigns application to the developer.",
        "verdict": "met"
      },
      "harness_result": "verified",
      "outside_dependencies": [],
      "part_id": "A1",
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
          "citation": ".agents/skills/bug-report-format/SKILL.md:3",
          "reason": "Names formatting, the template and the incoming-report trigger.",
          "result": "pass",
          "rule_id": "skills.description.what-and-when"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:3",
          "reason": "Describes the output rather than workflow steps.",
          "result": "pass",
          "rule_id": "skills.description.no-workflow-steps"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:3",
          "reason": "Explicitly excludes triage.",
          "result": "pass",
          "rule_id": "skills.description.boundary"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:3",
          "reason": "Uses third-person description.",
          "result": "pass",
          "rule_id": "skills.description.voice"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:7",
          "reason": "Supplies only the team-specific heading contract.",
          "result": "pass",
          "rule_id": "skills.body.only-what-model-lacks"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:5-7",
          "reason": "The only operative requirement appears immediately.",
          "result": "pass",
          "rule_id": "skills.body.gotchas-first"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:1-7",
          "reason": "Contains no dated or temporary claims.",
          "result": "pass",
          "rule_id": "skills.body.no-time-bound-statements"
        },
        {
          "check": "judged",
          "citation": "README.md:16",
          "reason": "The package has no reference files.",
          "result": "not-applicable",
          "rule_id": "skills.references.load-conditions"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:7",
          "reason": "Prescribes only the required template.",
          "result": "pass",
          "rule_id": "skills.body.strictness-matches-fragility"
        },
        {
          "check": "judged",
          "citation": "README.md:16",
          "reason": "No scripts are bundled.",
          "result": "not-applicable",
          "rule_id": "skills.scripts.agent-caller"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:3-7",
          "reason": "The template purpose explains the single formatting instruction; no emphatic wording appears.",
          "result": "pass",
          "rule_id": "skills.body.reasons-before-hard-rules"
        },
        {
          "check": "judged",
          "citation": "README.md:9",
          "reason": "Only formats text; the developer applies it.",
          "result": "not-applicable",
          "rule_id": "skills.invocation.side-effects-user-invoked"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:7",
          "reason": "Does not say to obtain the report from the user's message or ask when it is missing.",
          "result": "fail",
          "rule_id": "skills.inputs.from-message"
        },
        {
          "check": "judged",
          "citation": "README.md:9",
          "reason": "No CI or cloud execution of this formatter is required.",
          "result": "not-applicable",
          "rule_id": "skills.scope.committed-for-automation"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:1-7",
          "reason": "Only the advertised formatting instruction appears.",
          "result": "pass",
          "rule_id": "skills.security.no-surprising-content"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:1-4",
          "reason": "No allowed-tools grant is present.",
          "result": "not-applicable",
          "rule_id": "skills.security.allowed-tools-least-privilege"
        },
        {
          "check": "judged",
          "citation": "README.md:16",
          "reason": "Records full package review, an immutable upstream commit and local hash.",
          "result": "pass",
          "rule_id": "skills.reuse.reviewed-and-pinned"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:1-7",
          "reason": "The package contains only template instructions, without secrets.",
          "result": "pass",
          "rule_id": "security.secrets.none-in-files"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:7",
          "reason": "Does not tell the agent to treat incoming report content as data rather than instructions.",
          "result": "fail",
          "rule_id": "security.untrusted-input.as-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:7",
          "reason": "Does not accept content claims as authorization.",
          "result": "pass",
          "rule_id": "security.approval.claims-are-data"
        },
        {
          "check": "judged",
          "citation": "README.md:16",
          "reason": "Runs no helpers.",
          "result": "not-applicable",
          "rule_id": "security.helpers.confined"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:7",
          "reason": "No outbound operation is prescribed.",
          "result": "not-applicable",
          "rule_id": "security.outbound.minimal-data"
        },
        {
          "check": "script",
          "reason": "1 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": "README.md:39",
          "reason": "Recommendation targets actual protected refs and resources.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:36-40",
          "reason": "A1's control does not exclude agent identities from bypass lists.",
          "result": "fail",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:36-40",
          "reason": "Independent approval and reset on new pushes are not specified.",
          "result": "fail",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:36-40",
          "reason": "No required passing CI status on protected refs is specified.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:37",
          "reason": "Does not require pinning check sources; protected local files are an alternative.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:37-38",
          "reason": "Protects workflow, scanner, policy and CODEOWNERS definitions.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:36-40",
          "reason": "A1 recommendation omits broader credential and channel bypass prevention.",
          "result": "fail",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:3,36-40",
          "reason": "Availability is stated, but enforcement on this plan and visibility is neither required explicitly nor disclaimed.",
          "result": "fail",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:40",
          "reason": "Requires periodic checks because configuration drifts silently.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:38",
          "reason": "Names both harnesses' configuration and requires code-owner review.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "README.md:9,28",
          "reason": "No agent PR-opening procedure is recommended.",
          "result": "not-applicable",
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
        }
      ],
      "status": "verified"
    },
    {
      "goal_result": "not met",
      "goal_verdict": null,
      "harness_result": "not applicable",
      "outside_dependencies": [],
      "part_id": "A2",
      "rule_results": [
        {
          "check": "script",
          "reason": "1 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": "README.md:44",
          "reason": "Targets actual protected refs and resources.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:41-45",
          "reason": "A2 recommendation omits exclusions from bypass lists.",
          "result": "fail",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:41-45",
          "reason": "Does not require independent approval or reset after pushes.",
          "result": "fail",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:41-45",
          "reason": "Does not require passing CI on protected refs.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:42",
          "reason": "Does not require all check sources to be pinned.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:42-43",
          "reason": "Protects gate definitions and CODEOWNERS itself.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:41-45",
          "reason": "Omits broader credential and channel bypass prevention.",
          "result": "fail",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:3,41-45",
          "reason": "Availability does not establish or explicitly require enforcement for the stated plan and visibility.",
          "result": "fail",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:45",
          "reason": "Requires periodic configuration verification.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:43",
          "reason": "Covers both harnesses' agent configuration and requires code-owner review.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "README.md:10",
          "reason": "No labeling mechanism or PR-opening procedure is built.",
          "result": "not-applicable",
          "rule_id": "outside.merge.rule-for-agent-prs"
        }
      ],
      "status": "decided"
    },
    {
      "goal_result": "met by the verified build",
      "goal_verdict": {
        "reason": "Both harnesses require explicit invocation. The procedure resolves an approved issue, writes and posts a checklist, places precise observed/expected results after steps, separates speculation and redacts sensitive evidence.",
        "verdict": "met"
      },
      "harness_result": "verified",
      "outside_dependencies": [],
      "part_id": "B",
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
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:3",
          "reason": "Names checklist writing and posting and an explicit approved-issue request.",
          "result": "pass",
          "rule_id": "skills.description.what-and-when"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:3",
          "reason": "Describes the task and trigger without procedural steps.",
          "result": "pass",
          "rule_id": "skills.description.no-workflow-steps"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:3",
          "reason": "Excludes adjacent formatting, labeling, fixing, checking and closing tasks.",
          "result": "pass",
          "rule_id": "skills.description.boundary"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:3",
          "reason": "Uses impersonal task language without I or you.",
          "result": "pass",
          "rule_id": "skills.description.voice"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:15-21",
          "reason": "Provides workflow-specific evidence, approval, redaction and posting constraints.",
          "result": "pass",
          "rule_id": "skills.body.only-what-model-lacks"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:8-11",
          "reason": "Result precision and redaction requirements lead the body.",
          "result": "pass",
          "rule_id": "skills.body.gotchas-first"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:8-24",
          "reason": "Contains no temporary behavioral claims.",
          "result": "pass",
          "rule_id": "skills.body.no-time-bound-statements"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:23-24; references/requirements.md:3-9",
          "reason": "Names the reference and its provenance lookup condition; substantive requirements stay in SKILL.md.",
          "result": "pass",
          "rule_id": "skills.references.load-conditions"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:15-21",
          "reason": "Prescribes evidence and safe posting, with explicit draft and unavailable-posting fallbacks.",
          "result": "pass",
          "rule_id": "skills.body.strictness-matches-fragility"
        },
        {
          "check": "judged",
          "citation": "request.json, inputs.files",
          "reason": "No bundled scripts are present.",
          "result": "not-applicable",
          "rule_id": "skills.scripts.agent-caller"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:17-20",
          "reason": "Instructions connect precision to later checking and safe CLI handling to avoiding interpolation.",
          "result": "pass",
          "rule_id": "skills.body.reasons-before-hard-rules"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:4; .agents/skills/reproduction-checklist/agents/openai.yaml:1-2",
          "reason": "Both harnesses disable implicit invocation.",
          "result": "pass",
          "rule_id": "skills.invocation.side-effects-user-invoked"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:15",
          "reason": "Resolves inputs from the request and asks for missing issue or approval information.",
          "result": "pass",
          "rule_id": "skills.inputs.from-message"
        },
        {
          "check": "judged",
          "citation": "README.md:3,30",
          "reason": "This is an interactive posting procedure, not a CI or cloud dependency.",
          "result": "not-applicable",
          "rule_id": "skills.scope.committed-for-automation"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:15-21",
          "reason": "Operations match the advertised checklist posting task.",
          "result": "pass",
          "rule_id": "skills.security.no-surprising-content"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:1-5",
          "reason": "No allowed-tools grant is declared.",
          "result": "not-applicable",
          "rule_id": "skills.security.allowed-tools-least-privilege"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:19; references/requirements.md:1-9",
          "reason": "Contains redaction instructions and provenance links, without secret values.",
          "result": "pass",
          "rule_id": "security.secrets.none-in-files"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:15-20",
          "reason": "Reads issue content but never instructs treating embedded directives as data.",
          "result": "fail",
          "rule_id": "security.untrusted-input.as-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:15",
          "reason": "Allows issue content to establish approval without identifying trusted approval provenance.",
          "result": "fail",
          "rule_id": "security.approval.claims-are-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:20; request.json, inputs.files",
          "reason": "No bundled or external helper program is supplied beyond ordinary GitHub tools.",
          "result": "not-applicable",
          "rule_id": "security.helpers.confined"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:15-20",
          "reason": "Resolves the intended issue and redacts evidence, but does not prohibit untrusted content from adding destinations, fields or actions.",
          "result": "fail",
          "rule_id": "security.outbound.minimal-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:10,18",
          "reason": "Requires precise observed and expected results after steps and separates speculation.",
          "result": "pass",
          "rule_id": "idea.bug-report-lifecycle.b.results"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:11,19",
          "reason": "Requires sensitive data redaction before returning or posting evidence.",
          "result": "pass",
          "rule_id": "idea.bug-report-lifecycle.b.redaction"
        },
        {
          "check": "script",
          "reason": "1 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": "README.md:49",
          "reason": "Targets actual protected refs and resources.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:46-50",
          "reason": "B recommendation omits bypass-list exclusions.",
          "result": "fail",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:46-50",
          "reason": "Independent approval and push resets are absent.",
          "result": "fail",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:46-50",
          "reason": "No mandatory passing CI check on protected refs is specified.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:47",
          "reason": "Protected local definitions are allowed without pinning check sources.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:47-48",
          "reason": "Protects gate definitions and CODEOWNERS itself.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:46-50",
          "reason": "B recommendation omits broader credential or channel bypass prevention.",
          "result": "fail",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:3,46-50",
          "reason": "States availability without requiring enforcement for the actual plan and visibility or saying it is unenforced.",
          "result": "fail",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:50",
          "reason": "Requires periodic checks for silent drift.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:48",
          "reason": "Covers agent configuration for both targets and requires code-owner review.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:20-21",
          "reason": "Posts issue comments, without opening PRs.",
          "result": "not-applicable",
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
      "status": "verified"
    },
    {
      "goal_result": "depends on outside controls",
      "goal_verdict": {
        "reason": "The files do their share: assess every item for the latest SHA, reject stale evidence, recheck for pushes and require an outside protected required-status gate. The session verdict remains advisory; merge enforcement depends on the recommended, unverified outside control.",
        "verdict": "met"
      },
      "harness_result": "verified",
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
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:3",
          "reason": "Names checklist verification, latest-commit evidence and the pre-merge request trigger.",
          "result": "pass",
          "rule_id": "skills.description.what-and-when"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:3",
          "reason": "States the task and output rather than enumerating procedure.",
          "result": "pass",
          "rule_id": "skills.description.no-workflow-steps"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:3",
          "reason": "Excludes checklist creation, implementation, CI repair, merging and closing.",
          "result": "pass",
          "rule_id": "skills.description.boundary"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:3",
          "reason": "Uses impersonal task phrasing.",
          "result": "pass",
          "rule_id": "skills.description.voice"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:15-21",
          "reason": "Defines specific evidence freshness and advisory-versus-gate behavior.",
          "result": "pass",
          "rule_id": "skills.body.only-what-model-lacks"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:8-11",
          "reason": "Latest-SHA and outside-gate requirements lead the body.",
          "result": "pass",
          "rule_id": "skills.body.gotchas-first"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:8-24",
          "reason": "No temporary claims appear; commit freshness is an operational requirement.",
          "result": "pass",
          "rule_id": "skills.body.no-time-bound-statements"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:23-24; references/requirements.md:3-9",
          "reason": "Names provenance reference with a lookup condition and keeps requirement text in the body.",
          "result": "pass",
          "rule_id": "skills.references.load-conditions"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:16-20",
          "reason": "Strict evidence and gate constraints address false passing; missing evidence has explicit fallbacks.",
          "result": "pass",
          "rule_id": "skills.body.strictness-matches-fragility"
        },
        {
          "check": "judged",
          "citation": "request.json, inputs.files",
          "reason": "No bundled scripts are present.",
          "result": "not-applicable",
          "rule_id": "skills.scripts.agent-caller"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:16-20",
          "reason": "Explains stale evidence and why an advisory session cannot enforce the merge guarantee.",
          "result": "pass",
          "rule_id": "skills.body.reasons-before-hard-rules"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:4; .agents/skills/check-fix-checklist/agents/openai.yaml:1-2",
          "reason": "Both harnesses prevent implicit invocation.",
          "result": "pass",
          "rule_id": "skills.invocation.side-effects-user-invoked"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:15",
          "reason": "Resolves inputs from the request and asks for missing checklist association.",
          "result": "pass",
          "rule_id": "skills.inputs.from-message"
        },
        {
          "check": "judged",
          "citation": "README.md:28; request.json, inputs.links",
          "reason": "The checklist procedure is project-scoped and available to both harnesses.",
          "result": "pass",
          "rule_id": "skills.scope.committed-for-automation"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:15-21",
          "reason": "Instructions match checklist assessment and explicitly leave gate configuration and merging outside the procedure.",
          "result": "pass",
          "rule_id": "skills.security.no-surprising-content"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:1-5",
          "reason": "No allowed-tools grant is declared.",
          "result": "not-applicable",
          "rule_id": "skills.security.allowed-tools-least-privilege"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:1-24; references/requirements.md:1-9",
          "reason": "Contains procedural text and public provenance URLs without secrets.",
          "result": "pass",
          "rule_id": "security.secrets.none-in-files"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:15-19",
          "reason": "Rejects PR-provided enforcement claims, but never establishes the general data-only boundary for checklist content or supplied evidence.",
          "result": "fail",
          "rule_id": "security.untrusted-input.as-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:19-21",
          "reason": "Does not authorize merging from content claims and rejects PR-provided success as gate evidence.",
          "result": "pass",
          "rule_id": "security.approval.claims-are-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:17; request.json, inputs.files",
          "reason": "No helper implementation is supplied; assessment is limited to an authorized environment.",
          "result": "not-applicable",
          "rule_id": "security.helpers.confined"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:15-17",
          "reason": "Assessment can use commands and tools but does not constrain their outbound fields and destinations against checklist-supplied instructions.",
          "result": "fail",
          "rule_id": "security.outbound.minimal-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:10,16-18",
          "reason": "Requires all items to pass for the latest SHA and rechecks for pushes.",
          "result": "pass",
          "rule_id": "idea.bug-report-lifecycle.c.latest-commit"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:11,19",
          "reason": "Requires an outside protected required-status gate and labels the session advisory and configuration unverified.",
          "result": "pass",
          "rule_id": "idea.bug-report-lifecycle.c.required-merge-gate"
        },
        {
          "check": "script",
          "reason": "2 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:20; README.md:61",
          "reason": "Requires protection of real target branches and resources.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:62; .agents/skills/check-fix-checklist/SKILL.md:20",
          "reason": "Excludes bot, app, token and underlying human identity from bypass.",
          "result": "pass",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:51-62; .agents/skills/check-fix-checklist/SKILL.md:19-20",
          "reason": "Does not require approval from someone other than author, last pusher and launching user or reset approval on pushes.",
          "result": "fail",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:20; .agents/skills/check-fix-checklist/SKILL.md:19-20",
          "reason": "Requires a protected required-status-check gate on actual merge targets.",
          "result": "pass",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:20; README.md:57",
          "reason": "Allows protected local definitions without requiring all check sources to be pinned.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:52-53,57",
          "reason": "Protects workflow, scanner, policy and CODEOWNERS definitions.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:58; .agents/skills/check-fix-checklist/SKILL.md:20",
          "reason": "Explicitly excludes broader reachable credential and channel bypass.",
          "result": "pass",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:24,60; .agents/skills/check-fix-checklist/SKILL.md:20",
          "reason": "Makes hosting-plan enforcement an explicit prerequisite rather than claiming verification.",
          "result": "pass",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:55,59; .agents/skills/check-fix-checklist/SKILL.md:20",
          "reason": "Requires periodic verification for drift.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:53",
          "reason": "Covers both harnesses' agent configuration and mandatory code-owner review.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:15,21",
          "reason": "Assesses existing PRs without opening PRs.",
          "result": "not-applicable",
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
      "status": "verified"
    },
    {
      "goal_result": "met by the verified build",
      "goal_verdict": {
        "reason": "The procedure explicitly selects the intended PR, diagnoses current-SHA checks while distinguishing stale results, and returns a proposed fix for a developer to apply and push.",
        "verdict": "met"
      },
      "harness_result": "verified",
      "outside_dependencies": [],
      "part_id": "D",
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
          "citation": ".agents/skills/diagnose-ci/SKILL.md:3",
          "reason": "Names failing-CI diagnosis, developer-applied proposals and common failure triggers.",
          "result": "pass",
          "rule_id": "skills.description.what-and-when"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:3",
          "reason": "Describes scope and outcome without listing workflow steps.",
          "result": "pass",
          "rule_id": "skills.description.no-workflow-steps"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:3",
          "reason": "Explicitly excludes modifications, reruns, posting and merging.",
          "result": "pass",
          "rule_id": "skills.description.boundary"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:3",
          "reason": "Uses impersonal task phrasing.",
          "result": "pass",
          "rule_id": "skills.description.voice"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:14-20",
          "reason": "Defines intended-PR selection, evidence freshness and read-only handoff constraints.",
          "result": "pass",
          "rule_id": "skills.body.only-what-model-lacks"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:3,7-10",
          "reason": "Latest-SHA and explicit-PR requirements appear first; read-only scope is in the description.",
          "result": "pass",
          "rule_id": "skills.body.gotchas-first"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:7-23",
          "reason": "Contains no temporary claims.",
          "result": "pass",
          "rule_id": "skills.body.no-time-bound-statements"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:22-23; references/requirements.md:3-9",
          "reason": "Names the provenance reference and when to read it.",
          "result": "pass",
          "rule_id": "skills.references.load-conditions"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:14-20",
          "reason": "Strict PR targeting and read-only constraints address wrong-target and mutation risks; missing access and evidence have fallbacks.",
          "result": "pass",
          "rule_id": "skills.body.strictness-matches-fragility"
        },
        {
          "check": "judged",
          "citation": "request.json, inputs.files",
          "reason": "No bundled scripts are present.",
          "result": "not-applicable",
          "rule_id": "skills.scripts.agent-caller"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:16,20",
          "reason": "Explains why historical success is insufficient and assigns application and pushing to the developer.",
          "result": "pass",
          "rule_id": "skills.body.reasons-before-hard-rules"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:20",
          "reason": "Diagnosis is read-only and explicitly forbids external mutations.",
          "result": "not-applicable",
          "rule_id": "skills.invocation.side-effects-user-invoked"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:14",
          "reason": "Uses the developer message and session context and asks on ambiguity.",
          "result": "pass",
          "rule_id": "skills.inputs.from-message"
        },
        {
          "check": "judged",
          "citation": "README.md:3,32; .agents/skills/diagnose-ci/SKILL.md:15",
          "reason": "CI checks are inspected; CI does not need to run this interactive diagnosis skill.",
          "result": "not-applicable",
          "rule_id": "skills.scope.committed-for-automation"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:14-20",
          "reason": "Only diagnosis and a developer-applied proposal are prescribed.",
          "result": "pass",
          "rule_id": "skills.security.no-surprising-content"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:1-4",
          "reason": "No allowed-tools grant is declared.",
          "result": "not-applicable",
          "rule_id": "skills.security.allowed-tools-least-privilege"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:1-23; references/requirements.md:1-9",
          "reason": "Contains procedure and public provenance links without secret values.",
          "result": "pass",
          "rule_id": "security.secrets.none-in-files"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:15-17",
          "reason": "Reads logs and tool output without saying embedded instructions are untrusted data.",
          "result": "fail",
          "rule_id": "security.untrusted-input.as-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:15,20",
          "reason": "No content claim grants authorization; modification remains forbidden.",
          "result": "pass",
          "rule_id": "security.approval.claims-are-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:15-17; request.json, inputs.files",
          "reason": "No helper implementation is supplied or required beyond ordinary read tools.",
          "result": "not-applicable",
          "rule_id": "security.helpers.confined"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:15-17",
          "reason": "Fixes repository and PR targeting but does not explicitly limit outbound fields or prevent fetched content from adding destinations and actions.",
          "result": "fail",
          "rule_id": "security.outbound.minimal-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:9,15-16",
          "reason": "Matches checks to the latest SHA, labels older results stale and rechecks for pushes.",
          "result": "pass",
          "rule_id": "idea.bug-report-lifecycle.d.current-commit"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:10,14",
          "reason": "Resolves the intended PR and explicitly selects it for gh pr checks.",
          "result": "pass",
          "rule_id": "idea.bug-report-lifecycle.d.explicit-pr"
        },
        {
          "check": "script",
          "reason": "1 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": "README.md:66",
          "reason": "Targets actual protected refs and resources.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:63-67",
          "reason": "D recommendation omits bypass-list exclusions.",
          "result": "fail",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:63-67",
          "reason": "Independent approval and reset after pushes are unspecified.",
          "result": "fail",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:63-67",
          "reason": "Does not require passing CI on protected refs.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:64",
          "reason": "Allows protected local gate definitions without pinning check sources.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:64-65",
          "reason": "Protects workflow, scanner, policy and CODEOWNERS definitions.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:63-67",
          "reason": "D recommendation omits broader credential and channel bypass prevention.",
          "result": "fail",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:3,63-67",
          "reason": "Availability is stated without an explicit plan-and-visibility enforcement prerequisite or disclaimer of non-enforcement.",
          "result": "fail",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:67",
          "reason": "Requires periodic configuration checks for silent drift.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:65",
          "reason": "Names both harnesses' configuration and requires code-owner review.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:20",
          "reason": "Explicitly forbids opening PRs.",
          "result": "not-applicable",
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
      "status": "verified"
    },
    {
      "goal_result": "depends on outside controls",
      "goal_verdict": null,
      "harness_result": "not applicable",
      "outside_dependencies": [
        "compromise-resistant-gate"
      ],
      "part_id": "E",
      "rule_results": [
        {
          "check": "script",
          "reason": "2 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": "README.md:22,71,78",
          "reason": "Targets real issue/customer resources and protected refs/resources.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:79",
          "reason": "Excludes all agent identities, including the human behind its token.",
          "result": "pass",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:68-79",
          "reason": "Does not specify independent approval or reset on pushes.",
          "result": "fail",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:68-79",
          "reason": "Does not specify a required passing CI gate on protected refs.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:69,74",
          "reason": "Protected local definitions are allowed without requiring pinned check sources.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:69-70,74",
          "reason": "Protects gate definitions and CODEOWNERS itself.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:75",
          "reason": "Explicitly excludes broader credential or channel bypass.",
          "result": "pass",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:73,77",
          "reason": "Explicitly makes plan and visibility enforcement a prerequisite.",
          "result": "pass",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:72,76",
          "reason": "Requires periodic verification because configuration drifts silently.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:70",
          "reason": "Covers agent configuration in both harnesses and requires code-owner review.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "README.md:14,22",
          "reason": "No agent PR-opening or closing mechanism is built.",
          "result": "not-applicable",
          "rule_id": "outside.merge.rule-for-agent-prs"
        }
      ],
      "status": "decided"
    }
  ],
  "revision_digest": "03caeb0fd62b468d5be723224f6a732f33ca3d8dc78f77fb6a3453bf87dfce4e",
  "rules_digest": "93fec41536adbe0420026720fecbe03465b27f5f457695dc9d5704d422d7488a",
  "run_id": "5d46ccd1-765d-41da-aed2-8a01d4eca896",
  "runtime_results": [
    {
      "case_id": "format-explicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: command_execution; network: none requested; bug-report.md sha256 cd9952ee3fcedcd372267c91861f67ba42c0763fa2c404206107552c1feb4739",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/bug-report-format/SKILL.md": "7d42ea98e84f3148e438267365a036dfa62353a463cd48ddd0f2dd1957ce31cd"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.163.0",
      "inventory": "not observable",
      "observed_activation": null,
      "part_id": "A1",
      "prompt": "Use the bug-report-format skill to format the report in bug-report.md. Return the formatted text only; do not contact GitHub.",
      "reason": "Codex showed no observable activation signal",
      "result": "not-run",
      "run_id": "5d46ccd1-765d-41da-aed2-8a01d4eca896"
    },
    {
      "case_id": "format-implicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: command_execution; network: none requested; bug-report.md sha256 cd9952ee3fcedcd372267c91861f67ba42c0763fa2c404206107552c1feb4739",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/bug-report-format/SKILL.md": "7d42ea98e84f3148e438267365a036dfa62353a463cd48ddd0f2dd1957ce31cd"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.163.0",
      "inventory": "not observable",
      "observed_activation": null,
      "part_id": "A1",
      "prompt": "Format this new bug report with our team's template. The report is in bug-report.md. Return the text for me to apply to the issue.",
      "reason": "Codex showed no observable activation signal",
      "result": "not-run",
      "run_id": "5d46ccd1-765d-41da-aed2-8a01d4eca896"
    },
    {
      "case_id": "format-negative",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: command_execution; network: none requested",
      "expected": "does-not-activate",
      "file_hashes": {
        ".agents/skills/bug-report-format/SKILL.md": "7d42ea98e84f3148e438267365a036dfa62353a463cd48ddd0f2dd1957ce31cd"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.163.0",
      "inventory": "not observable",
      "observed_activation": null,
      "part_id": "A1",
      "prompt": "Explain why separating expected behavior from observed behavior helps developers understand bug reports. There is no report to format.",
      "reason": "Codex has no observable signal that proves non-activation",
      "result": "not-run",
      "run_id": "5d46ccd1-765d-41da-aed2-8a01d4eca896"
    },
    {
      "case_id": "checklist-explicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; invoked as $reproduction-checklist; tools: command_execution; network: none requested; bug-report.md sha256 cbdb4c341e3d2928cd9968cbc5909debc4d2b737c636c5861ac2989205e9885f",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/reproduction-checklist/SKILL.md": "710ff3f495bb2847ba4c5ef601516f158eb7df7995c880f10032ed4bba8e9e3b",
        ".agents/skills/reproduction-checklist/agents/openai.yaml": "a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94",
        ".agents/skills/reproduction-checklist/references/requirements.md": "6a89803edb0a5bce8995a56b34fb830512d93ea0646f17a791238b286a056328"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.163.0",
      "inventory": "not observable",
      "observed_activation": "instructions injected for .agents/skills/reproduction-checklist/SKILL.md (session rollout)",
      "part_id": "B",
      "prompt": "Use the reproduction-checklist skill to prepare a reproduction checklist for the approved issue in bug-report.md. This is an offline draft-only exercise; do not post to GitHub.",
      "reason": "instructions injected for .agents/skills/reproduction-checklist/SKILL.md (session rollout)",
      "result": "pass",
      "run_id": "5d46ccd1-765d-41da-aed2-8a01d4eca896"
    },
    {
      "case_id": "checklist-negative",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: command_execution; network: none requested",
      "expected": "does-not-activate",
      "file_hashes": {
        ".agents/skills/reproduction-checklist/SKILL.md": "710ff3f495bb2847ba4c5ef601516f158eb7df7995c880f10032ed4bba8e9e3b",
        ".agents/skills/reproduction-checklist/agents/openai.yaml": "a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94",
        ".agents/skills/reproduction-checklist/references/requirements.md": "6a89803edb0a5bce8995a56b34fb830512d93ea0646f17a791238b286a056328"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.163.0",
      "inventory": "not observable",
      "observed_activation": null,
      "part_id": "B",
      "prompt": "Explain what an approved bug report means in a development workflow. I am not requesting a reproduction checklist or any GitHub action.",
      "reason": "Codex has no observable signal that proves non-activation",
      "result": "not-run",
      "run_id": "5d46ccd1-765d-41da-aed2-8a01d4eca896"
    },
    {
      "case_id": "check-fix-explicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; invoked as $check-fix-checklist; tools: command_execution; network: none requested; checklist.md sha256 6d1c3bb7df3588e8784f80b9ec8cce5460b4168abc118502b85cb1e13b8d5969; pr-evidence.md sha256 98edae18925f61ca609551964a60d99fa5649596ed50683677ad5473bf86ae1e",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/check-fix-checklist/SKILL.md": "68e5c204a8671168e766391224467749b5eba53d8f2d70f4675d9ad575f4fcff",
        ".agents/skills/check-fix-checklist/agents/openai.yaml": "a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94",
        ".agents/skills/check-fix-checklist/references/requirements.md": "0c92710d6b79f400ec5007a167318eb3e06a224f0c48dc13954bbb73b77c2098"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.163.0",
      "inventory": "not observable",
      "observed_activation": "read .agents/skills/check-fix-checklist/SKILL.md",
      "part_id": "C",
      "prompt": "Check the fix against checklist.md using the snapshot in pr-evidence.md. This is an offline evidence review: do not run the application or contact GitHub. Report any limits on a current-commit or merge-enforcement verdict.",
      "reason": "read .agents/skills/check-fix-checklist/SKILL.md",
      "result": "pass",
      "run_id": "5d46ccd1-765d-41da-aed2-8a01d4eca896"
    },
    {
      "case_id": "check-fix-negative",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: command_execution; network: none requested",
      "expected": "does-not-activate",
      "file_hashes": {
        ".agents/skills/check-fix-checklist/SKILL.md": "68e5c204a8671168e766391224467749b5eba53d8f2d70f4675d9ad575f4fcff",
        ".agents/skills/check-fix-checklist/agents/openai.yaml": "a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94",
        ".agents/skills/check-fix-checklist/references/requirements.md": "0c92710d6b79f400ec5007a167318eb3e06a224f0c48dc13954bbb73b77c2098"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.163.0",
      "inventory": "not observable",
      "observed_activation": null,
      "part_id": "C",
      "prompt": "Explain the difference between a GitHub issue and a pull request. Do not inspect a fix, run a checklist, or change anything on GitHub.",
      "reason": "Codex has no observable signal that proves non-activation",
      "result": "not-run",
      "run_id": "5d46ccd1-765d-41da-aed2-8a01d4eca896"
    },
    {
      "case_id": "diagnose-ci-explicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: command_execution; network: none requested; ci-evidence.md sha256 fc83f5f831f24ad5087c67e21344a4a84b29f34af692b53237aad61baa4cb0da",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/diagnose-ci/SKILL.md": "cadfa2b00ff1f84a70668f5f1d64678a64f9adcad2fff1979a5131efd2d06f5d",
        ".agents/skills/diagnose-ci/references/requirements.md": "0b35f83e9a82fe74728b9b86f6dd90e25cd4fa546065f3afdcfc3a4e45b7ee6e"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.163.0",
      "inventory": "not observable",
      "observed_activation": "read .agents/skills/diagnose-ci/SKILL.md",
      "part_id": "D",
      "prompt": "Use the diagnose-ci skill to diagnose the failing checks on PR #45 using ci-evidence.md and propose a fix for the developer to apply. This is an offline snapshot review; do not contact GitHub or modify any files.",
      "reason": "read .agents/skills/diagnose-ci/SKILL.md",
      "result": "pass",
      "run_id": "5d46ccd1-765d-41da-aed2-8a01d4eca896"
    },
    {
      "case_id": "diagnose-ci-implicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: command_execution; network: none requested; ci-evidence.md sha256 fc83f5f831f24ad5087c67e21344a4a84b29f34af692b53237aad61baa4cb0da",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/diagnose-ci/SKILL.md": "cadfa2b00ff1f84a70668f5f1d64678a64f9adcad2fff1979a5131efd2d06f5d",
        ".agents/skills/diagnose-ci/references/requirements.md": "0b35f83e9a82fe74728b9b86f6dd90e25cd4fa546065f3afdcfc3a4e45b7ee6e"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.163.0",
      "inventory": "not observable",
      "observed_activation": "read .agents/skills/diagnose-ci/SKILL.md",
      "part_id": "D",
      "prompt": "The CI checks on our fix pull request #45 failed. Investigate the evidence in ci-evidence.md and tell me the cause and proposed fix. I will apply and push changes myself. Work offline without modifying files.",
      "reason": "read .agents/skills/diagnose-ci/SKILL.md",
      "result": "pass",
      "run_id": "5d46ccd1-765d-41da-aed2-8a01d4eca896"
    },
    {
      "case_id": "diagnose-ci-negative",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: command_execution; network: none requested",
      "expected": "does-not-activate",
      "file_hashes": {
        ".agents/skills/diagnose-ci/SKILL.md": "cadfa2b00ff1f84a70668f5f1d64678a64f9adcad2fff1979a5131efd2d06f5d",
        ".agents/skills/diagnose-ci/references/requirements.md": "0b35f83e9a82fe74728b9b86f6dd90e25cd4fa546065f3afdcfc3a4e45b7ee6e"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.163.0",
      "inventory": "not observable",
      "observed_activation": null,
      "part_id": "D",
      "prompt": "Explain in two sentences what continuous integration means. There is no failing check or pull request to investigate, and no diagnosis is requested.",
      "reason": "Codex has no observable signal that proves non-activation",
      "result": "not-run",
      "run_id": "5d46ccd1-765d-41da-aed2-8a01d4eca896"
    }
  ],
  "scope": "Extensive review (rarely needed): judged A1, A2, B, C, D, E",
  "scope_parts": null,
  "symlinks": {
    ".claude/skills/bug-report-format": "../../.agents/skills/bug-report-format",
    ".claude/skills/check-fix-checklist": "../../.agents/skills/check-fix-checklist",
    ".claude/skills/diagnose-ci": "../../.agents/skills/diagnose-ci",
    ".claude/skills/reproduction-checklist": "../../.agents/skills/reproduction-checklist"
  },
  "tool_versions": {
    "harness-forge-checkers": "7beeb29d229339f59695dccf5877b0efc53a7e117ff8fb0b7773c93c0d92e0df"
  },
  "whole_idea": {
    "facts": {
      "bypass_mode": false,
      "lethal_trifecta": false,
      "opens_prs": false,
      "plan_controls": "available",
      "reach": "repository",
      "target_set": "both",
      "untrusted_repo": false
    },
    "hosting": {
      "plan": "team",
      "platform": "github",
      "visibility": "private"
    },
    "reach": "repository",
    "targets": [
      "claude-code",
      "codex"
    ]
  },
  "worker_evidence": [
    {
      "configuration_digest": "d28f2bef0b1a2d477e3a44729b3bbe7971f0df2924cf44e48fc1fa9f21618a1b",
      "configured_controls": [
        "command: [\"codex\", \"--no-daemon\", \"exec\", \"--ignore-user-config\", \"--ignore-rules\", \"--skip-git-repo-check\", \"--ephemeral\", \"--json\", \"--color\", \"never\", \"--strict-config\", \"-C\", \"<workspace>\", \"--output-schema\", \"<workspace>/output-schema.json\", \"-c\", \"approval_policy=\\\"never\\\"\", \"-c\", \"project_doc_max_bytes=0\", \"-c\", \"mcp_servers={}\", \"-c\", \"apps._default.enabled=false\", \"-c\", \"web_search=\\\"live\\\"\", \"-c\", \"default_permissions=\\\"forge-worker\\\"\", \"-c\", \"permissions.forge-worker.filesystem={\\\":root\\\"=\\\"deny\\\", \\\":minimal\\\"=\\\"read\\\", \\\"<workspace>\\\"=\\\"read\\\"}\", \"-c\", \"permissions.forge-worker.network.enabled=false\", \"-c\", \"features.apps=false\", \"-c\", \"features.plugins=false\", \"-c\", \"features.hooks=false\", \"-c\", \"features.multi_agent=false\", \"-c\", \"features.browser_use=false\", \"-c\", \"features.browser_use_external=false\", \"-c\", \"features.computer_use=false\", \"-c\", \"features.image_generation=false\", \"-c\", \"features.remote_plugin=false\", \"-c\", \"features.tool_suggest=false\", \"-c\", \"features.view_image=false\", \"-c\", \"features.shell_tool=false\", \"-c\", \"features.unified_exec=false\", \"-\"]",
        "environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER",
        "login: subscription (ChatGPT)"
      ],
      "evidence_refs": [],
      "harness": "codex",
      "harness_version": "codex-cli 0.163.0",
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
      "configuration_digest": "faf9aa6201600adb491f3d870fcedefb9b6cf86d13bde50a61d7e3e8b755540f",
      "configured_controls": [
        "command: [\"codex\", \"--no-daemon\", \"exec\", \"--ignore-user-config\", \"--ignore-rules\", \"--skip-git-repo-check\", \"--ephemeral\", \"--json\", \"--color\", \"never\", \"--strict-config\", \"-C\", \"<workspace>\", \"--output-schema\", \"<workspace>/output-schema.json\", \"-c\", \"approval_policy=\\\"never\\\"\", \"-c\", \"project_doc_max_bytes=0\", \"-c\", \"mcp_servers={}\", \"-c\", \"apps._default.enabled=false\", \"-c\", \"web_search=\\\"disabled\\\"\", \"-c\", \"default_permissions=\\\"forge-worker\\\"\", \"-c\", \"permissions.forge-worker.filesystem={\\\":root\\\"=\\\"deny\\\", \\\":minimal\\\"=\\\"read\\\", \\\"<workspace>\\\"=\\\"read\\\"}\", \"-c\", \"permissions.forge-worker.network.enabled=false\", \"-c\", \"features.apps=false\", \"-c\", \"features.plugins=false\", \"-c\", \"features.hooks=false\", \"-c\", \"features.multi_agent=false\", \"-c\", \"features.browser_use=false\", \"-c\", \"features.browser_use_external=false\", \"-c\", \"features.computer_use=false\", \"-c\", \"features.image_generation=false\", \"-c\", \"features.remote_plugin=false\", \"-c\", \"features.tool_suggest=false\", \"-c\", \"features.view_image=false\", \"-c\", \"features.shell_tool=false\", \"-c\", \"features.unified_exec=false\", \"-\"]",
        "environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER",
        "login: subscription (ChatGPT)"
      ],
      "evidence_refs": [],
      "harness": "codex",
      "harness_version": "codex-cli 0.163.0",
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
      "configuration_digest": "0952a1dca9b7ff5765fac8f2121e99b97aa2bce930524db4b061e9ca569f2876",
      "configured_controls": [
        "command: [\"codex\", \"--no-daemon\", \"exec\", \"--ignore-user-config\", \"--ignore-rules\", \"--skip-git-repo-check\", \"--ephemeral\", \"--json\", \"--color\", \"never\", \"--strict-config\", \"-C\", \"<workspace>\", \"--output-schema\", \"<workspace>/output-schema.json\", \"-c\", \"approval_policy=\\\"never\\\"\", \"-c\", \"project_doc_max_bytes=0\", \"-c\", \"mcp_servers={}\", \"-c\", \"apps._default.enabled=false\", \"-c\", \"web_search=\\\"disabled\\\"\", \"-c\", \"default_permissions=\\\"forge-worker\\\"\", \"-c\", \"permissions.forge-worker.filesystem={\\\":root\\\"=\\\"deny\\\", \\\":minimal\\\"=\\\"read\\\", \\\"<workspace>\\\"=\\\"read\\\"}\", \"-c\", \"permissions.forge-worker.network.enabled=false\", \"-c\", \"features.apps=false\", \"-c\", \"features.plugins=false\", \"-c\", \"features.hooks=false\", \"-c\", \"features.multi_agent=false\", \"-c\", \"features.browser_use=false\", \"-c\", \"features.browser_use_external=false\", \"-c\", \"features.computer_use=false\", \"-c\", \"features.image_generation=false\", \"-c\", \"features.remote_plugin=false\", \"-c\", \"features.tool_suggest=false\", \"-c\", \"features.view_image=false\", \"-\"]",
        "environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER",
        "login: subscription (ChatGPT)"
      ],
      "evidence_refs": [],
      "harness": "codex",
      "harness_version": "codex-cli 0.163.0",
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
    }
  ],
  "worker_violations": []
}
```
