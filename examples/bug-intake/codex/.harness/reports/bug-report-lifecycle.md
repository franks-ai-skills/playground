# Verification report

- Run: `bug-report-lifecycle-2026-10-18-closing-extensive`
- Harness KB version: 0.1.0
- Contract digest: 3d0c06e3297c5cdd7176f5928f674b31a5cbad4a093e61c7df70d78134648640
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

- research worker: codex codex-cli 0.162.1, model account default, launcher independent-process, configuration d28f2bef0b1a2d477e3a44729b3bbe7971f0df2924cf44e48fc1fa9f21618a1b, controls: command: ["codex", "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--ephemeral", "--json", "--color", "never", "--strict-config", "-C", "<workspace>", "--output-schema", "<workspace>/output-schema.json", "-c", "approval_policy=\"never\"", "-c", "project_doc_max_bytes=0", "-c", "mcp_servers={}", "-c", "apps._default.enabled=false", "-c", "web_search=\"live\"", "-c", "default_permissions=\"forge-worker\"", "-c", "permissions.forge-worker.filesystem={\":root\"=\"deny\", \":minimal\"=\"read\", \"<workspace>\"=\"read\"}", "-c", "permissions.forge-worker.network.enabled=false", "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "features.hooks=false", "-c", "features.multi_agent=false", "-c", "features.browser_use=false", "-c", "features.browser_use_external=false", "-c", "features.computer_use=false", "-c", "features.image_generation=false", "-c", "features.remote_plugin=false", "-c", "features.tool_suggest=false", "-c", "features.view_image=false", "-c", "features.shell_tool=false", "-c", "features.unified_exec=false", "-"]; environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (ChatGPT), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- source-support worker: codex codex-cli 0.162.1, model account default, launcher independent-process, configuration faf9aa6201600adb491f3d870fcedefb9b6cf86d13bde50a61d7e3e8b755540f, controls: command: ["codex", "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--ephemeral", "--json", "--color", "never", "--strict-config", "-C", "<workspace>", "--output-schema", "<workspace>/output-schema.json", "-c", "approval_policy=\"never\"", "-c", "project_doc_max_bytes=0", "-c", "mcp_servers={}", "-c", "apps._default.enabled=false", "-c", "web_search=\"disabled\"", "-c", "default_permissions=\"forge-worker\"", "-c", "permissions.forge-worker.filesystem={\":root\"=\"deny\", \":minimal\"=\"read\", \"<workspace>\"=\"read\"}", "-c", "permissions.forge-worker.network.enabled=false", "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "features.hooks=false", "-c", "features.multi_agent=false", "-c", "features.browser_use=false", "-c", "features.browser_use_external=false", "-c", "features.computer_use=false", "-c", "features.image_generation=false", "-c", "features.remote_plugin=false", "-c", "features.tool_suggest=false", "-c", "features.view_image=false", "-c", "features.shell_tool=false", "-c", "features.unified_exec=false", "-"]; environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (ChatGPT), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- review worker: codex codex-cli 0.162.1, model account default, launcher independent-process, configuration 0952a1dca9b7ff5765fac8f2121e99b97aa2bce930524db4b061e9ca569f2876, controls: command: ["codex", "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--ephemeral", "--json", "--color", "never", "--strict-config", "-C", "<workspace>", "--output-schema", "<workspace>/output-schema.json", "-c", "approval_policy=\"never\"", "-c", "project_doc_max_bytes=0", "-c", "mcp_servers={}", "-c", "apps._default.enabled=false", "-c", "web_search=\"disabled\"", "-c", "default_permissions=\"forge-worker\"", "-c", "permissions.forge-worker.filesystem={\":root\"=\"deny\", \":minimal\"=\"read\", \"<workspace>\"=\"read\"}", "-c", "permissions.forge-worker.network.enabled=false", "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "features.hooks=false", "-c", "features.multi_agent=false", "-c", "features.browser_use=false", "-c", "features.browser_use_external=false", "-c", "features.computer_use=false", "-c", "features.image_generation=false", "-c", "features.remote_plugin=false", "-c", "features.tool_suggest=false", "-c", "features.view_image=false", "-"]; environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (ChatGPT), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable

## Part A1

- Harness result: verified
- Goal result: met by the verified build
- Status: verified
- Outside dependencies: none
- Confirmed answers: `{"event_without_agent": false, "every_time": "usually", "external_system": "none", "irreversible": false, "job": "procedure", "must_survive_compromise": "not-required", "own_context": false, "trigger": "model", "who_disables": "contributor"}`
- Goal verdict: met (The unchanged skill rewrites reports under all five required headings; the documented handoff leaves GitHub updates to the developer.)

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `outside.ci.required-on-ref` | warning | judged | fail | Does not specify required passing CI checks on protected refs. | README.md:36-40 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | Does not require pinning all sources executed by gate checks. | README.md:37 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | Protects gate definitions and CODEOWNERS itself. | README.md:37-38 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | Lists configuration for both harnesses and requires code-owner review. | README.md:38 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | fail | Does not address broader reachable credentials or channels. | README.md:36-40 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Requires periodic verification and explains silent drift. | README.md:40 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | fail | Availability is asserted, but plan-specific enforcement is neither required nor established. | README.md:3,36-40 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Targets actual protected refs and resources. | README.md:39 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | fail | The A1 recommendation does not exclude agent identities from bypass lists. | README.md:36-40 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | fail | Does not require independent approval or reset approvals after pushes. | README.md:36-40 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | not-applicable | The confirmed workflow does not have the agent open PRs. | request.json: inputs.context.facts.opens_prs | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 1 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `security.approval.claims-are-data` | warning | judged | pass | Contains no procedure accepting content claims as authorization. | .agents/skills/bug-report-format/SKILL.md:7 | docs/guide/security.md#context-and-persistent-state |
| `security.helpers.confined` | warning | judged | not-applicable | Runs no helpers. | .agents/skills/bug-report-format/SKILL.md:7 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#executables-approvals-and-isolation |
| `security.outbound.minimal-data` | warning | judged | not-applicable | Makes no outbound calls. | README.md:9 | docs/guide/security.md#data-access-and-outbound-channels, https://developers.openai.com/api/docs/guides/deep-research#prompt-injection-and-exfiltration |
| `security.secrets.none-in-files` | error | judged | pass | The complete package contains no secret values. | .agents/skills/bug-report-format/SKILL.md:1-7 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#context-and-persistent-state |
| `security.untrusted-input.as-data` | warning | judged | fail | Does not distinguish report content from instructions. | .agents/skills/bug-report-format/SKILL.md:7 | docs/guide/security.md#context-and-persistent-state |
| `skills.body.gotchas-first` | warning | judged | pass | The sole template requirement is immediately visible. | .agents/skills/bug-report-format/SKILL.md:7 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://agentskills.io/skill-creation/best-practices.md |
| `skills.body.no-time-bound-statements` | warning | judged | pass | Contains no dated or expiring instructions. | .agents/skills/bug-report-format/SKILL.md:1-7 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.only-what-model-lacks` | warning | judged | pass | Supplies only the team's required headings. | .agents/skills/bug-report-format/SKILL.md:7 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.reasons-before-hard-rules` | warning | judged | pass | The team-template purpose explains the heading instruction; no emphatic prohibitions appear. | .agents/skills/bug-report-format/SKILL.md:3-7 | docs/best-practices/skills.md#7-explain-the-why-before-adding-hard-rules |
| `skills.body.size` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, docs/concepts/skills.md#body, https://code.claude.com/docs/en/skills, https://agentskills.io/specification |
| `skills.body.strictness-matches-fragility` | warning | judged | pass | Prescribes the required template while leaving rewriting flexible. | .agents/skills/bug-report-format/SKILL.md:7 | docs/best-practices/skills.md#5-match-strictness-to-fragility, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.description.boundary` | warning | judged | pass | Excludes triage. | .agents/skills/bug-report-format/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.description.concise` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, docs/research-notes/agent-harness-best-practices/skills.md |
| `skills.description.length` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/opencode/skills.md#format, https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs, https://opencode.ai/docs/skills/ |
| `skills.description.no-workflow-steps` | warning | judged | pass | Describes scope without enumerating a workflow. | .agents/skills/bug-report-format/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md |
| `skills.description.voice` | warning | judged | pass | Uses third-person description. | .agents/skills/bug-report-format/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition |
| `skills.description.what-and-when` | warning | judged | pass | Names formatting, the template and the incoming-report trigger. | .agents/skills/bug-report-format/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://learn.chatgpt.com/docs/build-skills, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.frontmatter.valid` | error | script | pass | 1 skill(s) checked | - | docs/vendors/opencode/skills.md#format, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/claude-code/skills.md#format, docs/concepts/skills.md#frontmatter, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.goal.no-must-hold-rule-in-skill` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#13-move-rules-that-must-hold-every-time-into-hooks, https://code.claude.com/docs/en/skills |
| `skills.inputs.from-message` | warning | judged | fail | Does not direct the agent to obtain the report from the message or ask when missing. | .agents/skills/bug-report-format/SKILL.md:7 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, docs/concepts/skills.md#body |
| `skills.invocation.both-flags` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#invocation-policy-in-both-leads, docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.invocation.side-effects-user-invoked` | error | judged | not-applicable | Formatting returns text; the developer updates GitHub. | README.md:9 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.name.format` | error | script | pass | 1 skill(s) checked | - | docs/guide/skills.md#portability, docs/concepts/skills.md#frontmatter, docs/vendors/opencode/skills.md#format, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.package.no-auxiliary-docs` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#anti-patterns, https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md |
| `skills.portable.frontmatter` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/best-practices/skills.md#12-keep-one-canonical-copy-with-portable-frontmatter, https://code.claude.com/docs/en/skills |
| `skills.portable.layout` | error | script | pass | 1 skill(s) linked | - | docs/concepts/skills.md#directory-layout, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.portable.no-claude-placeholders` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#body, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills |
| `skills.portable.plugin-layout` | error | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#directory-layout, docs/vendors/claude-code/plugins.md#standard-layout, docs/vendors/codex/plugins.md#plugin-layout, https://code.claude.com/docs/en/plugins/manifest-reference, https://developers.openai.com/codex/plugins/build |
| `skills.references.load-conditions` | warning | judged | not-applicable | The reused package has no reference files. | README.md:16 | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/best-practices.md |
| `skills.references.one-level` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/specification |
| `skills.references.resolve` | error | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.reuse.reviewed-and-pinned` | error | judged | pass | Records full local-package review and immutable commit and hash pins. | README.md:16 | docs/best-practices/skills.md#security, https://owasp.github.io/www-project-agentic-skills-top-10/ast01 |
| `skills.scope.committed-for-automation` | warning | judged | not-applicable | No CI or cloud invocation is required. | request.json: inputs.context.parts, A1 answers | docs/concepts/skills.md#directory-layout, https://code.claude.com/docs/en/skills |
| `skills.scripts.agent-caller` | warning | judged | not-applicable | No scripts are bundled. | README.md:16 | docs/best-practices/skills.md#6-put-deterministic-logic-in-tested-scripts, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/using-scripts.md |
| `skills.security.allowed-tools-least-privilege` | warning | judged | not-applicable | No allowed-tools grant is declared. | .agents/skills/bug-report-format/SKILL.md:1-4 | docs/best-practices/skills.md#security, docs/vendors/claude-code/skills.md#limits-and-gotchas, https://code.claude.com/docs/en/skills |
| `skills.security.no-surprising-content` | error | judged | pass | Only the advertised formatting instruction is present. | .agents/skills/bug-report-format/SKILL.md:1-7 | docs/best-practices/skills.md#security, https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md |

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
| `outside.ci.required-on-ref` | warning | judged | fail | Required passing CI on protected refs is unspecified. | README.md:41-45 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | Pinning all check sources is not required. | README.md:42 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | Protects gate definitions and CODEOWNERS itself. | README.md:42-43 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | Covers both harnesses and requires code-owner review. | README.md:43 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | fail | Broader credentials and channels are not addressed. | README.md:41-45 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Requires periodic checks because configuration drifts. | README.md:45 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | fail | Does not require or establish enforcement for the stated plan and visibility. | README.md:3,41-45 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Targets actual refs and resources. | README.md:44 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | fail | No identity-bypass restriction is specified. | README.md:41-45 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | fail | Independent approval and approval reset are absent. | README.md:41-45 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | not-applicable | No agent-opened PRs are recommended. | request.json: inputs.context.facts.opens_prs | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 1 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |

## Part B

- Harness result: not verified
- Goal result: not met
- Status: built
- Outside dependencies: none
- Confirmed answers: `{"event_without_agent": false, "every_time": "usually", "external_system": "cli", "irreversible": false, "job": "procedure", "must_survive_compromise": "not-required", "own_context": false, "trigger": "user", "who_disables": "contributor"}`
- Goal verdict: met (Both harnesses require explicit invocation, and the procedure prepares and posts approved-issue checklists with precise results, separated speculation and redacted evidence.)

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `idea.bug-report-lifecycle.b.redaction` | error | judged | pass | Requires redaction in logs and supporting evidence before output or posting. | .agents/skills/reproduction-checklist/SKILL.md:19 | https://github.com/UsefulSoftwareCo/executor/issues/1225 |
| `idea.bug-report-lifecycle.b.results` | error | judged | pass | Requires precise observed and expected results after steps, with speculation separated. | .agents/skills/reproduction-checklist/SKILL.md:18 | https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html |
| `outside.ci.required-on-ref` | warning | judged | fail | Does not require passing CI checks on protected refs. | README.md:46-50 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | Does not require pinning all sources run by checks. | README.md:47 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | Protects gate definitions and CODEOWNERS itself. | README.md:47-48 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | Covers both harnesses with required code-owner review. | README.md:48 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | fail | Does not address broader reachable credentials or channels. | README.md:46-50 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Requires periodic drift checks. | README.md:50 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | fail | Does not require or establish enforcement on the stated hosting plan. | README.md:3,46-50 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Targets actual protected refs and resources. | README.md:49 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | fail | The B control does not exclude agent identities from bypass lists. | README.md:46-50 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | fail | Independent approval and reset after pushes are unspecified. | README.md:46-50 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | not-applicable | No agent-opened PRs are recommended. | request.json: inputs.context.facts.opens_prs | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 1 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `runtime.explicit-activation` | error | script | fail | the live build needs an observed explicit activation, and none passed | - | - |
| `security.approval.claims-are-data` | warning | judged | fail | Allows approval to be established from issue content without distinguishing an untrusted approval claim from authorization. | .agents/skills/reproduction-checklist/SKILL.md:15 | docs/guide/security.md#context-and-persistent-state |
| `security.helpers.confined` | warning | judged | pass | Uses reviewable standard CLI operations under interactive tool permissions, with no bypass. | README.md:3; .agents/skills/reproduction-checklist/SKILL.md:20 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#executables-approvals-and-isolation |
| `security.outbound.minimal-data` | warning | judged | fail | Resolves the posting issue and redacts evidence but does not prevent untrusted content from adding destinations, fields or actions. | .agents/skills/reproduction-checklist/SKILL.md:15-20 | docs/guide/security.md#data-access-and-outbound-channels, https://developers.openai.com/api/docs/guides/deep-research#prompt-injection-and-exfiltration |
| `security.secrets.none-in-files` | error | judged | pass | Contains redaction instructions and public source references, with no secret values. | .agents/skills/reproduction-checklist/SKILL.md:19; references/requirements.md:8-9 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#context-and-persistent-state |
| `security.untrusted-input.as-data` | warning | judged | fail | Reads issue content without directing the agent to treat embedded instructions as data. | .agents/skills/reproduction-checklist/SKILL.md:15-16 | docs/guide/security.md#context-and-persistent-state |
| `skills.body.gotchas-first` | warning | judged | pass | Results and redaction requirements appear before the procedure. | .agents/skills/reproduction-checklist/SKILL.md:8-11 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://agentskills.io/skill-creation/best-practices.md |
| `skills.body.no-time-bound-statements` | warning | judged | pass | Contains no dated operational claims. | .agents/skills/reproduction-checklist/SKILL.md:1-24; references/requirements.md:3-9 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.only-what-model-lacks` | warning | judged | pass | Provides task-specific evidence, approval, redaction and posting constraints. | .agents/skills/reproduction-checklist/SKILL.md:15-21 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.reasons-before-hard-rules` | warning | judged | pass | Constraints explain avoiding guessed observations, secret exposure and shell interpolation. | .agents/skills/reproduction-checklist/SKILL.md:16-20 | docs/best-practices/skills.md#7-explain-the-why-before-adding-hard-rules |
| `skills.body.size` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, docs/concepts/skills.md#body, https://code.claude.com/docs/en/skills, https://agentskills.io/specification |
| `skills.body.strictness-matches-fragility` | warning | judged | pass | Constrains sensitive evidence and shell handling, with draft-only and unavailable-posting escapes. | .agents/skills/reproduction-checklist/SKILL.md:19-20 | docs/best-practices/skills.md#5-match-strictness-to-fragility, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.description.boundary` | warning | judged | pass | Excludes neighboring report, fix, PR and closure tasks. | .agents/skills/reproduction-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.description.concise` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, docs/research-notes/agent-harness-best-practices/skills.md |
| `skills.description.length` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/opencode/skills.md#format, https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs, https://opencode.ai/docs/skills/ |
| `skills.description.no-workflow-steps` | warning | judged | pass | Names the capability without listing procedure steps. | .agents/skills/reproduction-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md |
| `skills.description.voice` | warning | judged | pass | Uses an impersonal capability description without I or you. | .agents/skills/reproduction-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition |
| `skills.description.what-and-when` | warning | judged | pass | Names checklist creation and posting, with an explicit approved-issue trigger. | .agents/skills/reproduction-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://learn.chatgpt.com/docs/build-skills, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.frontmatter.valid` | error | script | pass | 1 skill(s) checked | - | docs/vendors/opencode/skills.md#format, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/claude-code/skills.md#format, docs/concepts/skills.md#frontmatter, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.goal.no-must-hold-rule-in-skill` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#13-move-rules-that-must-hold-every-time-into-hooks, https://code.claude.com/docs/en/skills |
| `skills.inputs.from-message` | warning | judged | pass | Resolves the issue from the request and asks for missing issue or approval information. | .agents/skills/reproduction-checklist/SKILL.md:15 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, docs/concepts/skills.md#body |
| `skills.invocation.both-flags` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#invocation-policy-in-both-leads, docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.invocation.side-effects-user-invoked` | error | judged | pass | Disables model invocation in Claude Code and implicit invocation in Codex. | .agents/skills/reproduction-checklist/SKILL.md:4; .agents/skills/reproduction-checklist/agents/openai.yaml:1-2 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.name.format` | error | script | pass | 1 skill(s) checked | - | docs/guide/skills.md#portability, docs/concepts/skills.md#frontmatter, docs/vendors/opencode/skills.md#format, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.package.no-auxiliary-docs` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#anti-patterns, https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md |
| `skills.portable.frontmatter` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/best-practices/skills.md#12-keep-one-canonical-copy-with-portable-frontmatter, https://code.claude.com/docs/en/skills |
| `skills.portable.layout` | error | script | pass | 1 skill(s) linked | - | docs/concepts/skills.md#directory-layout, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.portable.no-claude-placeholders` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#body, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills |
| `skills.portable.plugin-layout` | error | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#directory-layout, docs/vendors/claude-code/plugins.md#standard-layout, docs/vendors/codex/plugins.md#plugin-layout, https://code.claude.com/docs/en/plugins/manifest-reference, https://developers.openai.com/codex/plugins/build |
| `skills.references.load-conditions` | warning | judged | pass | Names the reference and loads it only for requirement IDs or sources; metadata is separate from instructions. | .agents/skills/reproduction-checklist/SKILL.md:23-24; references/requirements.md:8-9 | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/best-practices.md |
| `skills.references.one-level` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/specification |
| `skills.references.resolve` | error | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.reuse.reviewed-and-pinned` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#security, https://owasp.github.io/www-project-agentic-skills-top-10/ast01 |
| `skills.scope.committed-for-automation` | warning | judged | not-applicable | This is an explicitly invoked interactive workflow, not a required CI/cloud skill. | README.md:3,30 | docs/concepts/skills.md#directory-layout, https://code.claude.com/docs/en/skills |
| `skills.scripts.agent-caller` | warning | judged | not-applicable | No executable scripts are bundled. | request.json: inputs.files, reproduction-checklist entries | docs/best-practices/skills.md#6-put-deterministic-logic-in-tested-scripts, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/using-scripts.md |
| `skills.security.allowed-tools-least-privilege` | warning | judged | not-applicable | No allowed-tools grant is present. | .agents/skills/reproduction-checklist/SKILL.md:1-5 | docs/best-practices/skills.md#security, docs/vendors/claude-code/skills.md#limits-and-gotchas, https://code.claude.com/docs/en/skills |
| `skills.security.no-surprising-content` | error | judged | pass | Instructions stay within the advertised checklist preparation and posting scope. | .agents/skills/reproduction-checklist/SKILL.md:15-24 | docs/best-practices/skills.md#security, https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md |

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
- Confirmed answers: `{"event_without_agent": false, "every_time": "usually", "external_system": "cli", "irreversible": false, "job": "procedure", "must_survive_compromise": "required", "own_context": false, "trigger": "user"}`
- Goal verdict: not-met (The skill satisfies both accepted procedural requirements, but the required outside merge gate is only recommended and explicitly unverified. The staged build does not establish the no-merge guarantee.)

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `idea.bug-report-lifecycle.c.latest-commit` | error | judged | pass | Requires evidence for the latest SHA and rechecks it after collecting evidence. | .agents/skills/check-fix-checklist/SKILL.md:16-18 | https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks |
| `idea.bug-report-lifecycle.c.required-merge-gate` | error | judged | pass | Explicitly requires a protected outside required-status-check gate and calls session verdicts advisory. | .agents/skills/check-fix-checklist/SKILL.md:11,19 | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches |
| `links.parts` | error | script | pass | every linked part exists under its recorded name | - | - |
| `outside.ci.required-on-ref` | warning | judged | pass | Requires an outside required-status-check gate on actual target branches. | README.md:20; .agents/skills/check-fix-checklist/SKILL.md:19-20 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | Offers protected local definitions as an alternative to pinned external definitions and does not require pinning all executed sources. | .agents/skills/check-fix-checklist/SKILL.md:20; README.md:57 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | Requires protected gate definitions and self-owned CODEOWNERS. | README.md:52-53,57 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | Covers both harnesses with mandatory code-owner review. | README.md:53 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | pass | Explicitly excludes broader credentials and channels from bypass. | README.md:58 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Requires periodic checks because gate configuration drifts. | README.md:59 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | pass | Requires enforcement on the hosting plan and reports missing evidence. | .agents/skills/check-fix-checklist/SKILL.md:20; README.md:60 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Requires the gate on actual merge targets and protected resources. | README.md:20,61 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | pass | Excludes bot, app, token and underlying human identities from bypass. | README.md:62 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | fail | No requirement excludes author, last pusher and launching user from approval or resets approval after pushes. | README.md:51-62; .agents/skills/check-fix-checklist/SKILL.md:20 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | not-applicable | The agent does not open PRs in the confirmed workflow. | request.json: inputs.context.facts.opens_prs | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 2 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `runtime.explicit-activation` | error | script | fail | the live build needs an observed explicit activation, and none passed | - | - |
| `security.approval.claims-are-data` | warning | judged | pass | Requires trusted gate provenance and rejects PR-provided enforcement claims. | .agents/skills/check-fix-checklist/SKILL.md:19-20 | docs/guide/security.md#context-and-persistent-state |
| `security.helpers.confined` | warning | judged | pass | Execution is limited to the authorized environment under interactive harness permissions. | README.md:3; .agents/skills/check-fix-checklist/SKILL.md:17 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#executables-approvals-and-isolation |
| `security.outbound.minimal-data` | warning | judged | fail | Does not constrain tool-call destinations and fields against additions from checklist or PR content. | .agents/skills/check-fix-checklist/SKILL.md:15-17 | docs/guide/security.md#data-access-and-outbound-channels, https://developers.openai.com/api/docs/guides/deep-research#prompt-injection-and-exfiltration |
| `security.secrets.none-in-files` | error | judged | pass | Contains no credential values or other secrets. | .agents/skills/check-fix-checklist/SKILL.md:1-24; references/requirements.md:8-9 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#context-and-persistent-state |
| `security.untrusted-input.as-data` | warning | judged | fail | Rejects PR success claims as enforcement evidence but does not generally treat checklist and PR instructions as untrusted data. | .agents/skills/check-fix-checklist/SKILL.md:15,17,19 | docs/guide/security.md#context-and-persistent-state |
| `skills.body.gotchas-first` | warning | judged | pass | Latest-SHA and outside-gate requirements lead the body. | .agents/skills/check-fix-checklist/SKILL.md:8-11 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://agentskills.io/skill-creation/best-practices.md |
| `skills.body.no-time-bound-statements` | warning | judged | pass | Contains no dated or expiring instructions. | .agents/skills/check-fix-checklist/SKILL.md:1-24; references/requirements.md:3-9 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.only-what-model-lacks` | warning | judged | pass | Specifies evidence freshness, inconclusive outcomes and the boundary between advice and enforcement. | .agents/skills/check-fix-checklist/SKILL.md:15-21 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.reasons-before-hard-rules` | warning | judged | pass | Explains why stale evidence and session verdicts cannot establish merge safety. | .agents/skills/check-fix-checklist/SKILL.md:16-20 | docs/best-practices/skills.md#7-explain-the-why-before-adding-hard-rules |
| `skills.body.size` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, docs/concepts/skills.md#body, https://code.claude.com/docs/en/skills, https://agentskills.io/specification |
| `skills.body.strictness-matches-fragility` | warning | judged | pass | Strictness focuses on stale evidence and gate integrity, with blocked or inconclusive outcomes when evidence is unavailable. | .agents/skills/check-fix-checklist/SKILL.md:16-20 | docs/best-practices/skills.md#5-match-strictness-to-fragility, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.description.boundary` | warning | judged | pass | Excludes checklist creation, implementation, CI repair, merging and closure. | .agents/skills/check-fix-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.description.concise` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, docs/research-notes/agent-harness-best-practices/skills.md |
| `skills.description.length` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/opencode/skills.md#format, https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs, https://opencode.ai/docs/skills/ |
| `skills.description.no-workflow-steps` | warning | judged | pass | Describes capability without listing workflow steps. | .agents/skills/check-fix-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md |
| `skills.description.voice` | warning | judged | pass | Uses an impersonal capability description. | .agents/skills/check-fix-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition |
| `skills.description.what-and-when` | warning | judged | pass | Names PR checklist verification and the explicit pre-merge trigger. | .agents/skills/check-fix-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://learn.chatgpt.com/docs/build-skills, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.frontmatter.valid` | error | script | pass | 1 skill(s) checked | - | docs/vendors/opencode/skills.md#format, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/claude-code/skills.md#format, docs/concepts/skills.md#frontmatter, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.goal.no-must-hold-rule-in-skill` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#13-move-rules-that-must-hold-every-time-into-hooks, https://code.claude.com/docs/en/skills |
| `skills.inputs.from-message` | warning | judged | pass | Uses the developer's request and asks for missing or ambiguous checklist association. | .agents/skills/check-fix-checklist/SKILL.md:15 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, docs/concepts/skills.md#body |
| `skills.invocation.both-flags` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#invocation-policy-in-both-leads, docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.invocation.side-effects-user-invoked` | error | judged | pass | Explicit invocation is configured in both target harnesses. | .agents/skills/check-fix-checklist/SKILL.md:4; .agents/skills/check-fix-checklist/agents/openai.yaml:1-2 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.name.format` | error | script | pass | 1 skill(s) checked | - | docs/guide/skills.md#portability, docs/concepts/skills.md#frontmatter, docs/vendors/opencode/skills.md#format, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.package.no-auxiliary-docs` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#anti-patterns, https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md |
| `skills.portable.frontmatter` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/best-practices/skills.md#12-keep-one-canonical-copy-with-portable-frontmatter, https://code.claude.com/docs/en/skills |
| `skills.portable.layout` | error | script | pass | 1 skill(s) linked | - | docs/concepts/skills.md#directory-layout, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.portable.no-claude-placeholders` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#body, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills |
| `skills.portable.plugin-layout` | error | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#directory-layout, docs/vendors/claude-code/plugins.md#standard-layout, docs/vendors/codex/plugins.md#plugin-layout, https://code.claude.com/docs/en/plugins/manifest-reference, https://developers.openai.com/codex/plugins/build |
| `skills.references.load-conditions` | warning | judged | pass | Provides a conditional reference link for IDs and sources without duplicating requirement prose. | .agents/skills/check-fix-checklist/SKILL.md:23-24; references/requirements.md:8-9 | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/best-practices.md |
| `skills.references.one-level` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/specification |
| `skills.references.resolve` | error | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.reuse.reviewed-and-pinned` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#security, https://owasp.github.io/www-project-agentic-skills-top-10/ast01 |
| `skills.scope.committed-for-automation` | warning | judged | not-applicable | The session skill is interactive; enforcement is assigned to a separate outside gate. | README.md:12,30 | docs/concepts/skills.md#directory-layout, https://code.claude.com/docs/en/skills |
| `skills.scripts.agent-caller` | warning | judged | not-applicable | No executable scripts are bundled. | request.json: inputs.files, check-fix-checklist entries | docs/best-practices/skills.md#6-put-deterministic-logic-in-tested-scripts, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/using-scripts.md |
| `skills.security.allowed-tools-least-privilege` | warning | judged | not-applicable | No allowed-tools grant is declared. | .agents/skills/check-fix-checklist/SKILL.md:1-5 | docs/best-practices/skills.md#security, docs/vendors/claude-code/skills.md#limits-and-gotchas, https://code.claude.com/docs/en/skills |
| `skills.security.no-surprising-content` | error | judged | pass | Stays within checklist verification and explicitly forbids manufacturing statuses or reconfiguring gates. | .agents/skills/check-fix-checklist/SKILL.md:15-21 | docs/best-practices/skills.md#security, https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md |

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
- Goal verdict: met (The read-only procedure explicitly targets the intended PR, diagnoses latest-SHA failures, distinguishes stale evidence and returns a proposed fix for the developer to apply and push.)

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `idea.bug-report-lifecycle.d.current-commit` | error | judged | pass | Matches runs to SHAs, distinguishes stale results and rechecks after gathering evidence. | .agents/skills/diagnose-ci/SKILL.md:16 | https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks |
| `idea.bug-report-lifecycle.d.explicit-pr` | error | judged | pass | Resolves the intended PR and explicitly selects it for gh pr checks. | .agents/skills/diagnose-ci/SKILL.md:14 | https://cli.github.com/manual/gh_pr_checks |
| `outside.ci.required-on-ref` | warning | judged | fail | Does not require passing CI checks on protected refs. | README.md:63-67 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | Does not require pinning all check sources. | README.md:64 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | Protects gate definitions and CODEOWNERS itself. | README.md:64-65 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | Covers both harnesses and requires code-owner review. | README.md:65 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | fail | Does not address broader reachable credentials or channels. | README.md:63-67 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Requires periodic drift verification. | README.md:67 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | fail | Does not require or establish plan-specific enforcement. | README.md:3,63-67 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Targets actual refs and resources. | README.md:66 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | fail | The D control does not exclude agent identities from bypass lists. | README.md:63-67 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | fail | Independent approval and reset after pushes are unspecified. | README.md:63-67 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | not-applicable | No agent-opened PRs are recommended. | request.json: inputs.context.facts.opens_prs | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 1 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `security.approval.claims-are-data` | warning | judged | pass | No content claim authorizes changes; the skill expressly remains read-only. | .agents/skills/diagnose-ci/SKILL.md:20 | docs/guide/security.md#context-and-persistent-state |
| `security.helpers.confined` | warning | judged | pass | Uses read-only CLI operations and authorized tools under harness permissions. | README.md:3; .agents/skills/diagnose-ci/SKILL.md:15,17 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#executables-approvals-and-isolation |
| `security.outbound.minimal-data` | warning | judged | fail | Keeps an explicit PR target but does not prohibit untrusted evidence from expanding outbound destinations or fields. | .agents/skills/diagnose-ci/SKILL.md:15-17 | docs/guide/security.md#data-access-and-outbound-channels, https://developers.openai.com/api/docs/guides/deep-research#prompt-injection-and-exfiltration |
| `security.secrets.none-in-files` | error | judged | pass | Contains no secret values. | .agents/skills/diagnose-ci/SKILL.md:1-23; references/requirements.md:8-9 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#context-and-persistent-state |
| `security.untrusted-input.as-data` | warning | judged | fail | Reads PR evidence and logs without instructing the agent to treat embedded instructions as data. | .agents/skills/diagnose-ci/SKILL.md:15-17 | docs/guide/security.md#context-and-persistent-state |
| `skills.body.gotchas-first` | warning | judged | pass | Latest-commit and explicit-PR requirements appear first. | .agents/skills/diagnose-ci/SKILL.md:7-10 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://agentskills.io/skill-creation/best-practices.md |
| `skills.body.no-time-bound-statements` | warning | judged | pass | Contains no dated or expiring operational statements. | .agents/skills/diagnose-ci/SKILL.md:1-23; references/requirements.md:3-9 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.only-what-model-lacks` | warning | judged | pass | Supplies specific PR-targeting, SHA freshness and developer-handoff constraints. | .agents/skills/diagnose-ci/SKILL.md:14-20 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.reasons-before-hard-rules` | warning | judged | pass | Explains current-branch ambiguity, stale evidence and the developer's responsibility for changes. | .agents/skills/diagnose-ci/SKILL.md:14,16,20 | docs/best-practices/skills.md#7-explain-the-why-before-adding-hard-rules |
| `skills.body.size` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, docs/concepts/skills.md#body, https://code.claude.com/docs/en/skills, https://agentskills.io/specification |
| `skills.body.strictness-matches-fragility` | warning | judged | pass | Strict constraints protect PR selection, freshness and read-only scope; unavailable evidence is reported. | .agents/skills/diagnose-ci/SKILL.md:14-20 | docs/best-practices/skills.md#5-match-strictness-to-fragility, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.description.boundary` | warning | judged | pass | Explicitly excludes editing, reruns, posting, credential changes and repository mutations. | .agents/skills/diagnose-ci/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.description.concise` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, docs/research-notes/agent-harness-best-practices/skills.md |
| `skills.description.length` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/opencode/skills.md#format, https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs, https://opencode.ai/docs/skills/ |
| `skills.description.no-workflow-steps` | warning | judged | pass | Describes scope rather than enumerating procedure steps. | .agents/skills/diagnose-ci/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md |
| `skills.description.voice` | warning | judged | pass | Uses an impersonal capability description. | .agents/skills/diagnose-ci/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition |
| `skills.description.what-and-when` | warning | judged | pass | Names CI diagnosis and proposed fixes, with recognizable failing-check triggers. | .agents/skills/diagnose-ci/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://learn.chatgpt.com/docs/build-skills, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.frontmatter.valid` | error | script | pass | 1 skill(s) checked | - | docs/vendors/opencode/skills.md#format, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/claude-code/skills.md#format, docs/concepts/skills.md#frontmatter, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.goal.no-must-hold-rule-in-skill` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#13-move-rules-that-must-hold-every-time-into-hooks, https://code.claude.com/docs/en/skills |
| `skills.inputs.from-message` | warning | judged | pass | Uses the developer's message and session context and asks when ambiguous. | .agents/skills/diagnose-ci/SKILL.md:14 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, docs/concepts/skills.md#body |
| `skills.invocation.both-flags` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#invocation-policy-in-both-leads, docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.invocation.side-effects-user-invoked` | error | judged | not-applicable | Diagnosis is read-only and leaves applying and pushing changes to the developer. | .agents/skills/diagnose-ci/SKILL.md:20 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.name.format` | error | script | pass | 1 skill(s) checked | - | docs/guide/skills.md#portability, docs/concepts/skills.md#frontmatter, docs/vendors/opencode/skills.md#format, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.package.no-auxiliary-docs` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#anti-patterns, https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md |
| `skills.portable.frontmatter` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/best-practices/skills.md#12-keep-one-canonical-copy-with-portable-frontmatter, https://code.claude.com/docs/en/skills |
| `skills.portable.layout` | error | script | pass | 1 skill(s) linked | - | docs/concepts/skills.md#directory-layout, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.portable.no-claude-placeholders` | warning | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#body, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills |
| `skills.portable.plugin-layout` | error | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#directory-layout, docs/vendors/claude-code/plugins.md#standard-layout, docs/vendors/codex/plugins.md#plugin-layout, https://code.claude.com/docs/en/plugins/manifest-reference, https://developers.openai.com/codex/plugins/build |
| `skills.references.load-conditions` | warning | judged | pass | Names the reference with a condition for loading IDs and sources. | .agents/skills/diagnose-ci/SKILL.md:22-23; references/requirements.md:8-9 | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/best-practices.md |
| `skills.references.one-level` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/specification |
| `skills.references.resolve` | error | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.reuse.reviewed-and-pinned` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#security, https://owasp.github.io/www-project-agentic-skills-top-10/ast01 |
| `skills.scope.committed-for-automation` | warning | judged | not-applicable | No CI or cloud execution of this skill is required. | README.md:3,32 | docs/concepts/skills.md#directory-layout, https://code.claude.com/docs/en/skills |
| `skills.scripts.agent-caller` | warning | judged | not-applicable | No executable scripts are bundled. | request.json: inputs.files, diagnose-ci entries | docs/best-practices/skills.md#6-put-deterministic-logic-in-tested-scripts, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/using-scripts.md |
| `skills.security.allowed-tools-least-privilege` | warning | judged | not-applicable | No allowed-tools grant is declared. | .agents/skills/diagnose-ci/SKILL.md:1-4 | docs/best-practices/skills.md#security, docs/vendors/claude-code/skills.md#limits-and-gotchas, https://code.claude.com/docs/en/skills |
| `skills.security.no-surprising-content` | error | judged | pass | All instructions support read-only diagnosis and a developer-applied proposal. | .agents/skills/diagnose-ci/SKILL.md:14-23 | docs/best-practices/skills.md#security, https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md |

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
| `outside.ci.required-on-ref` | warning | judged | fail | Does not specify required passing CI checks on protected refs. | README.md:68-79 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | Does not require pinning all sources executed by gate checks. | README.md:69,74 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | pass | Requires protected gate definitions and self-owned CODEOWNERS. | README.md:69-70,74 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | pass | Covers both harnesses with mandatory code-owner review. | README.md:70 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | pass | Explicitly prohibits broader credentials and channels from bypassing the control. | README.md:75 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | pass | Requires periodic checks because configuration drifts silently. | README.md:76 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | pass | Makes plan and visibility enforcement an explicit prerequisite. | README.md:77 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | pass | Names actual issue/customer-status resources and real protected targets. | README.md:22,78 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | pass | Explicitly excludes agent and underlying human identities from bypass. | README.md:79 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | fail | No independent approver or approval-reset requirement is given. | README.md:68-79 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | not-applicable | No agent-opened PRs are recommended. | request.json: inputs.context.facts.opens_prs | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 2 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |

## Runtime tests

| Part | Case | Harness | Result | Observed | Reason |
| --- | --- | --- | --- | --- | --- |
| A1 | format-explicit | codex codex-cli 0.162.1 | pass | read .agents/skills/bug-report-format/SKILL.md | read .agents/skills/bug-report-format/SKILL.md |
| A1 | format-implicit | codex codex-cli 0.162.1 | not-run | - | Codex showed no observable activation signal |
| A1 | format-negative | codex codex-cli 0.162.1 | not-run | - | Codex has no observable signal that proves non-activation |
| B | checklist-explicit | codex codex-cli 0.162.1 | not-run | - | Codex showed no observable activation signal |
| B | checklist-negative | codex codex-cli 0.162.1 | not-run | - | Codex has no observable signal that proves non-activation |
| C | check-fix-explicit | codex codex-cli 0.162.1 | not-run | - | Codex showed no observable activation signal |
| C | check-fix-negative | codex codex-cli 0.162.1 | not-run | - | Codex has no observable signal that proves non-activation |
| D | diagnose-ci-explicit | codex codex-cli 0.162.1 | pass | read .agents/skills/diagnose-ci/SKILL.md | read .agents/skills/diagnose-ci/SKILL.md |
| D | diagnose-ci-implicit | codex codex-cli 0.162.1 | pass | read .agents/skills/diagnose-ci/SKILL.md | read .agents/skills/diagnose-ci/SKILL.md |
| D | diagnose-ci-negative | codex codex-cli 0.162.1 | not-run | - | Codex has no observable signal that proves non-activation |

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
    "worker": "d7b55955550d1e0ae7442dd636cfb0c68cd5c02b7c932f908d2a8ab0a0b53f92"
  },
  "confirmed_parts": [
    "A1",
    "A2",
    "B",
    "C",
    "D",
    "E"
  ],
  "contract_digest": "3d0c06e3297c5cdd7176f5928f674b31a5cbad4a093e61c7df70d78134648640",
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
        "reason": "The unchanged skill rewrites reports under all five required headings; the documented handoff leaves GitHub updates to the developer.",
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
          "reason": "Describes scope without enumerating a workflow.",
          "result": "pass",
          "rule_id": "skills.description.no-workflow-steps"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:3",
          "reason": "Excludes triage.",
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
          "reason": "Supplies only the team's required headings.",
          "result": "pass",
          "rule_id": "skills.body.only-what-model-lacks"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:7",
          "reason": "The sole template requirement is immediately visible.",
          "result": "pass",
          "rule_id": "skills.body.gotchas-first"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:1-7",
          "reason": "Contains no dated or expiring instructions.",
          "result": "pass",
          "rule_id": "skills.body.no-time-bound-statements"
        },
        {
          "check": "judged",
          "citation": "README.md:16",
          "reason": "The reused package has no reference files.",
          "result": "not-applicable",
          "rule_id": "skills.references.load-conditions"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:7",
          "reason": "Prescribes the required template while leaving rewriting flexible.",
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
          "reason": "The team-template purpose explains the heading instruction; no emphatic prohibitions appear.",
          "result": "pass",
          "rule_id": "skills.body.reasons-before-hard-rules"
        },
        {
          "check": "judged",
          "citation": "README.md:9",
          "reason": "Formatting returns text; the developer updates GitHub.",
          "result": "not-applicable",
          "rule_id": "skills.invocation.side-effects-user-invoked"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:7",
          "reason": "Does not direct the agent to obtain the report from the message or ask when missing.",
          "result": "fail",
          "rule_id": "skills.inputs.from-message"
        },
        {
          "check": "judged",
          "citation": "request.json: inputs.context.parts, A1 answers",
          "reason": "No CI or cloud invocation is required.",
          "result": "not-applicable",
          "rule_id": "skills.scope.committed-for-automation"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:1-7",
          "reason": "Only the advertised formatting instruction is present.",
          "result": "pass",
          "rule_id": "skills.security.no-surprising-content"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:1-4",
          "reason": "No allowed-tools grant is declared.",
          "result": "not-applicable",
          "rule_id": "skills.security.allowed-tools-least-privilege"
        },
        {
          "check": "judged",
          "citation": "README.md:16",
          "reason": "Records full local-package review and immutable commit and hash pins.",
          "result": "pass",
          "rule_id": "skills.reuse.reviewed-and-pinned"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:1-7",
          "reason": "The complete package contains no secret values.",
          "result": "pass",
          "rule_id": "security.secrets.none-in-files"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:7",
          "reason": "Does not distinguish report content from instructions.",
          "result": "fail",
          "rule_id": "security.untrusted-input.as-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:7",
          "reason": "Contains no procedure accepting content claims as authorization.",
          "result": "pass",
          "rule_id": "security.approval.claims-are-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-report-format/SKILL.md:7",
          "reason": "Runs no helpers.",
          "result": "not-applicable",
          "rule_id": "security.helpers.confined"
        },
        {
          "check": "judged",
          "citation": "README.md:9",
          "reason": "Makes no outbound calls.",
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
          "reason": "Targets actual protected refs and resources.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:36-40",
          "reason": "The A1 recommendation does not exclude agent identities from bypass lists.",
          "result": "fail",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:36-40",
          "reason": "Does not require independent approval or reset approvals after pushes.",
          "result": "fail",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:36-40",
          "reason": "Does not specify required passing CI checks on protected refs.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:37",
          "reason": "Does not require pinning all sources executed by gate checks.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:37-38",
          "reason": "Protects gate definitions and CODEOWNERS itself.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:36-40",
          "reason": "Does not address broader reachable credentials or channels.",
          "result": "fail",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:3,36-40",
          "reason": "Availability is asserted, but plan-specific enforcement is neither required nor established.",
          "result": "fail",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:40",
          "reason": "Requires periodic verification and explains silent drift.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:38",
          "reason": "Lists configuration for both harnesses and requires code-owner review.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "request.json: inputs.context.facts.opens_prs",
          "reason": "The confirmed workflow does not have the agent open PRs.",
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
          "reason": "Targets actual refs and resources.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:41-45",
          "reason": "No identity-bypass restriction is specified.",
          "result": "fail",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:41-45",
          "reason": "Independent approval and approval reset are absent.",
          "result": "fail",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:41-45",
          "reason": "Required passing CI on protected refs is unspecified.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:42",
          "reason": "Pinning all check sources is not required.",
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
          "reason": "Broader credentials and channels are not addressed.",
          "result": "fail",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:3,41-45",
          "reason": "Does not require or establish enforcement for the stated plan and visibility.",
          "result": "fail",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:45",
          "reason": "Requires periodic checks because configuration drifts.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:43",
          "reason": "Covers both harnesses and requires code-owner review.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "request.json: inputs.context.facts.opens_prs",
          "reason": "No agent-opened PRs are recommended.",
          "result": "not-applicable",
          "rule_id": "outside.merge.rule-for-agent-prs"
        }
      ],
      "status": "decided"
    },
    {
      "goal_result": "not met",
      "goal_verdict": {
        "reason": "Both harnesses require explicit invocation, and the procedure prepares and posts approved-issue checklists with precise results, separated speculation and redacted evidence.",
        "verdict": "met"
      },
      "harness_result": "not verified",
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
          "reason": "Names checklist creation and posting, with an explicit approved-issue trigger.",
          "result": "pass",
          "rule_id": "skills.description.what-and-when"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:3",
          "reason": "Names the capability without listing procedure steps.",
          "result": "pass",
          "rule_id": "skills.description.no-workflow-steps"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:3",
          "reason": "Excludes neighboring report, fix, PR and closure tasks.",
          "result": "pass",
          "rule_id": "skills.description.boundary"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:3",
          "reason": "Uses an impersonal capability description without I or you.",
          "result": "pass",
          "rule_id": "skills.description.voice"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:15-21",
          "reason": "Provides task-specific evidence, approval, redaction and posting constraints.",
          "result": "pass",
          "rule_id": "skills.body.only-what-model-lacks"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:8-11",
          "reason": "Results and redaction requirements appear before the procedure.",
          "result": "pass",
          "rule_id": "skills.body.gotchas-first"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:1-24; references/requirements.md:3-9",
          "reason": "Contains no dated operational claims.",
          "result": "pass",
          "rule_id": "skills.body.no-time-bound-statements"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:23-24; references/requirements.md:8-9",
          "reason": "Names the reference and loads it only for requirement IDs or sources; metadata is separate from instructions.",
          "result": "pass",
          "rule_id": "skills.references.load-conditions"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:19-20",
          "reason": "Constrains sensitive evidence and shell handling, with draft-only and unavailable-posting escapes.",
          "result": "pass",
          "rule_id": "skills.body.strictness-matches-fragility"
        },
        {
          "check": "judged",
          "citation": "request.json: inputs.files, reproduction-checklist entries",
          "reason": "No executable scripts are bundled.",
          "result": "not-applicable",
          "rule_id": "skills.scripts.agent-caller"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:16-20",
          "reason": "Constraints explain avoiding guessed observations, secret exposure and shell interpolation.",
          "result": "pass",
          "rule_id": "skills.body.reasons-before-hard-rules"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:4; .agents/skills/reproduction-checklist/agents/openai.yaml:1-2",
          "reason": "Disables model invocation in Claude Code and implicit invocation in Codex.",
          "result": "pass",
          "rule_id": "skills.invocation.side-effects-user-invoked"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:15",
          "reason": "Resolves the issue from the request and asks for missing issue or approval information.",
          "result": "pass",
          "rule_id": "skills.inputs.from-message"
        },
        {
          "check": "judged",
          "citation": "README.md:3,30",
          "reason": "This is an explicitly invoked interactive workflow, not a required CI/cloud skill.",
          "result": "not-applicable",
          "rule_id": "skills.scope.committed-for-automation"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:15-24",
          "reason": "Instructions stay within the advertised checklist preparation and posting scope.",
          "result": "pass",
          "rule_id": "skills.security.no-surprising-content"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:1-5",
          "reason": "No allowed-tools grant is present.",
          "result": "not-applicable",
          "rule_id": "skills.security.allowed-tools-least-privilege"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:19; references/requirements.md:8-9",
          "reason": "Contains redaction instructions and public source references, with no secret values.",
          "result": "pass",
          "rule_id": "security.secrets.none-in-files"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:15-16",
          "reason": "Reads issue content without directing the agent to treat embedded instructions as data.",
          "result": "fail",
          "rule_id": "security.untrusted-input.as-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:15",
          "reason": "Allows approval to be established from issue content without distinguishing an untrusted approval claim from authorization.",
          "result": "fail",
          "rule_id": "security.approval.claims-are-data"
        },
        {
          "check": "judged",
          "citation": "README.md:3; .agents/skills/reproduction-checklist/SKILL.md:20",
          "reason": "Uses reviewable standard CLI operations under interactive tool permissions, with no bypass.",
          "result": "pass",
          "rule_id": "security.helpers.confined"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:15-20",
          "reason": "Resolves the posting issue and redacts evidence but does not prevent untrusted content from adding destinations, fields or actions.",
          "result": "fail",
          "rule_id": "security.outbound.minimal-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:18",
          "reason": "Requires precise observed and expected results after steps, with speculation separated.",
          "result": "pass",
          "rule_id": "idea.bug-report-lifecycle.b.results"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/reproduction-checklist/SKILL.md:19",
          "reason": "Requires redaction in logs and supporting evidence before output or posting.",
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
          "reason": "The B control does not exclude agent identities from bypass lists.",
          "result": "fail",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:46-50",
          "reason": "Independent approval and reset after pushes are unspecified.",
          "result": "fail",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:46-50",
          "reason": "Does not require passing CI checks on protected refs.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:47",
          "reason": "Does not require pinning all sources run by checks.",
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
          "reason": "Does not address broader reachable credentials or channels.",
          "result": "fail",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:3,46-50",
          "reason": "Does not require or establish enforcement on the stated hosting plan.",
          "result": "fail",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:50",
          "reason": "Requires periodic drift checks.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:48",
          "reason": "Covers both harnesses with required code-owner review.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "request.json: inputs.context.facts.opens_prs",
          "reason": "No agent-opened PRs are recommended.",
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
      "goal_result": "not met",
      "goal_verdict": {
        "reason": "The skill satisfies both accepted procedural requirements, but the required outside merge gate is only recommended and explicitly unverified. The staged build does not establish the no-merge guarantee.",
        "verdict": "not-met"
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
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:3",
          "reason": "Names PR checklist verification and the explicit pre-merge trigger.",
          "result": "pass",
          "rule_id": "skills.description.what-and-when"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:3",
          "reason": "Describes capability without listing workflow steps.",
          "result": "pass",
          "rule_id": "skills.description.no-workflow-steps"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:3",
          "reason": "Excludes checklist creation, implementation, CI repair, merging and closure.",
          "result": "pass",
          "rule_id": "skills.description.boundary"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:3",
          "reason": "Uses an impersonal capability description.",
          "result": "pass",
          "rule_id": "skills.description.voice"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:15-21",
          "reason": "Specifies evidence freshness, inconclusive outcomes and the boundary between advice and enforcement.",
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
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:1-24; references/requirements.md:3-9",
          "reason": "Contains no dated or expiring instructions.",
          "result": "pass",
          "rule_id": "skills.body.no-time-bound-statements"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:23-24; references/requirements.md:8-9",
          "reason": "Provides a conditional reference link for IDs and sources without duplicating requirement prose.",
          "result": "pass",
          "rule_id": "skills.references.load-conditions"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:16-20",
          "reason": "Strictness focuses on stale evidence and gate integrity, with blocked or inconclusive outcomes when evidence is unavailable.",
          "result": "pass",
          "rule_id": "skills.body.strictness-matches-fragility"
        },
        {
          "check": "judged",
          "citation": "request.json: inputs.files, check-fix-checklist entries",
          "reason": "No executable scripts are bundled.",
          "result": "not-applicable",
          "rule_id": "skills.scripts.agent-caller"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:16-20",
          "reason": "Explains why stale evidence and session verdicts cannot establish merge safety.",
          "result": "pass",
          "rule_id": "skills.body.reasons-before-hard-rules"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:4; .agents/skills/check-fix-checklist/agents/openai.yaml:1-2",
          "reason": "Explicit invocation is configured in both target harnesses.",
          "result": "pass",
          "rule_id": "skills.invocation.side-effects-user-invoked"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:15",
          "reason": "Uses the developer's request and asks for missing or ambiguous checklist association.",
          "result": "pass",
          "rule_id": "skills.inputs.from-message"
        },
        {
          "check": "judged",
          "citation": "README.md:12,30",
          "reason": "The session skill is interactive; enforcement is assigned to a separate outside gate.",
          "result": "not-applicable",
          "rule_id": "skills.scope.committed-for-automation"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:15-21",
          "reason": "Stays within checklist verification and explicitly forbids manufacturing statuses or reconfiguring gates.",
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
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:1-24; references/requirements.md:8-9",
          "reason": "Contains no credential values or other secrets.",
          "result": "pass",
          "rule_id": "security.secrets.none-in-files"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:15,17,19",
          "reason": "Rejects PR success claims as enforcement evidence but does not generally treat checklist and PR instructions as untrusted data.",
          "result": "fail",
          "rule_id": "security.untrusted-input.as-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:19-20",
          "reason": "Requires trusted gate provenance and rejects PR-provided enforcement claims.",
          "result": "pass",
          "rule_id": "security.approval.claims-are-data"
        },
        {
          "check": "judged",
          "citation": "README.md:3; .agents/skills/check-fix-checklist/SKILL.md:17",
          "reason": "Execution is limited to the authorized environment under interactive harness permissions.",
          "result": "pass",
          "rule_id": "security.helpers.confined"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:15-17",
          "reason": "Does not constrain tool-call destinations and fields against additions from checklist or PR content.",
          "result": "fail",
          "rule_id": "security.outbound.minimal-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:16-18",
          "reason": "Requires evidence for the latest SHA and rechecks it after collecting evidence.",
          "result": "pass",
          "rule_id": "idea.bug-report-lifecycle.c.latest-commit"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:11,19",
          "reason": "Explicitly requires a protected outside required-status-check gate and calls session verdicts advisory.",
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
          "citation": "README.md:20,61",
          "reason": "Requires the gate on actual merge targets and protected resources.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:62",
          "reason": "Excludes bot, app, token and underlying human identities from bypass.",
          "result": "pass",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:51-62; .agents/skills/check-fix-checklist/SKILL.md:20",
          "reason": "No requirement excludes author, last pusher and launching user from approval or resets approval after pushes.",
          "result": "fail",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:20; .agents/skills/check-fix-checklist/SKILL.md:19-20",
          "reason": "Requires an outside required-status-check gate on actual target branches.",
          "result": "pass",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:20; README.md:57",
          "reason": "Offers protected local definitions as an alternative to pinned external definitions and does not require pinning all executed sources.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:52-53,57",
          "reason": "Requires protected gate definitions and self-owned CODEOWNERS.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:58",
          "reason": "Explicitly excludes broader credentials and channels from bypass.",
          "result": "pass",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/check-fix-checklist/SKILL.md:20; README.md:60",
          "reason": "Requires enforcement on the hosting plan and reports missing evidence.",
          "result": "pass",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:59",
          "reason": "Requires periodic checks because gate configuration drifts.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:53",
          "reason": "Covers both harnesses with mandatory code-owner review.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "request.json: inputs.context.facts.opens_prs",
          "reason": "The agent does not open PRs in the confirmed workflow.",
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
      "goal_result": "met by the verified build",
      "goal_verdict": {
        "reason": "The read-only procedure explicitly targets the intended PR, diagnoses latest-SHA failures, distinguishes stale evidence and returns a proposed fix for the developer to apply and push.",
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
          "reason": "Names CI diagnosis and proposed fixes, with recognizable failing-check triggers.",
          "result": "pass",
          "rule_id": "skills.description.what-and-when"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:3",
          "reason": "Describes scope rather than enumerating procedure steps.",
          "result": "pass",
          "rule_id": "skills.description.no-workflow-steps"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:3",
          "reason": "Explicitly excludes editing, reruns, posting, credential changes and repository mutations.",
          "result": "pass",
          "rule_id": "skills.description.boundary"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:3",
          "reason": "Uses an impersonal capability description.",
          "result": "pass",
          "rule_id": "skills.description.voice"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:14-20",
          "reason": "Supplies specific PR-targeting, SHA freshness and developer-handoff constraints.",
          "result": "pass",
          "rule_id": "skills.body.only-what-model-lacks"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:7-10",
          "reason": "Latest-commit and explicit-PR requirements appear first.",
          "result": "pass",
          "rule_id": "skills.body.gotchas-first"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:1-23; references/requirements.md:3-9",
          "reason": "Contains no dated or expiring operational statements.",
          "result": "pass",
          "rule_id": "skills.body.no-time-bound-statements"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:22-23; references/requirements.md:8-9",
          "reason": "Names the reference with a condition for loading IDs and sources.",
          "result": "pass",
          "rule_id": "skills.references.load-conditions"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:14-20",
          "reason": "Strict constraints protect PR selection, freshness and read-only scope; unavailable evidence is reported.",
          "result": "pass",
          "rule_id": "skills.body.strictness-matches-fragility"
        },
        {
          "check": "judged",
          "citation": "request.json: inputs.files, diagnose-ci entries",
          "reason": "No executable scripts are bundled.",
          "result": "not-applicable",
          "rule_id": "skills.scripts.agent-caller"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:14,16,20",
          "reason": "Explains current-branch ambiguity, stale evidence and the developer's responsibility for changes.",
          "result": "pass",
          "rule_id": "skills.body.reasons-before-hard-rules"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:20",
          "reason": "Diagnosis is read-only and leaves applying and pushing changes to the developer.",
          "result": "not-applicable",
          "rule_id": "skills.invocation.side-effects-user-invoked"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:14",
          "reason": "Uses the developer's message and session context and asks when ambiguous.",
          "result": "pass",
          "rule_id": "skills.inputs.from-message"
        },
        {
          "check": "judged",
          "citation": "README.md:3,32",
          "reason": "No CI or cloud execution of this skill is required.",
          "result": "not-applicable",
          "rule_id": "skills.scope.committed-for-automation"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:14-23",
          "reason": "All instructions support read-only diagnosis and a developer-applied proposal.",
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
          "citation": ".agents/skills/diagnose-ci/SKILL.md:1-23; references/requirements.md:8-9",
          "reason": "Contains no secret values.",
          "result": "pass",
          "rule_id": "security.secrets.none-in-files"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:15-17",
          "reason": "Reads PR evidence and logs without instructing the agent to treat embedded instructions as data.",
          "result": "fail",
          "rule_id": "security.untrusted-input.as-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:20",
          "reason": "No content claim authorizes changes; the skill expressly remains read-only.",
          "result": "pass",
          "rule_id": "security.approval.claims-are-data"
        },
        {
          "check": "judged",
          "citation": "README.md:3; .agents/skills/diagnose-ci/SKILL.md:15,17",
          "reason": "Uses read-only CLI operations and authorized tools under harness permissions.",
          "result": "pass",
          "rule_id": "security.helpers.confined"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:15-17",
          "reason": "Keeps an explicit PR target but does not prohibit untrusted evidence from expanding outbound destinations or fields.",
          "result": "fail",
          "rule_id": "security.outbound.minimal-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:16",
          "reason": "Matches runs to SHAs, distinguishes stale results and rechecks after gathering evidence.",
          "result": "pass",
          "rule_id": "idea.bug-report-lifecycle.d.current-commit"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/diagnose-ci/SKILL.md:14",
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
          "reason": "Targets actual refs and resources.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:63-67",
          "reason": "The D control does not exclude agent identities from bypass lists.",
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
          "reason": "Does not require passing CI checks on protected refs.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:64",
          "reason": "Does not require pinning all check sources.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:64-65",
          "reason": "Protects gate definitions and CODEOWNERS itself.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:63-67",
          "reason": "Does not address broader reachable credentials or channels.",
          "result": "fail",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:3,63-67",
          "reason": "Does not require or establish plan-specific enforcement.",
          "result": "fail",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:67",
          "reason": "Requires periodic drift verification.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:65",
          "reason": "Covers both harnesses and requires code-owner review.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "request.json: inputs.context.facts.opens_prs",
          "reason": "No agent-opened PRs are recommended.",
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
          "citation": "README.md:22,78",
          "reason": "Names actual issue/customer-status resources and real protected targets.",
          "result": "pass",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:79",
          "reason": "Explicitly excludes agent and underlying human identities from bypass.",
          "result": "pass",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:68-79",
          "reason": "No independent approver or approval-reset requirement is given.",
          "result": "fail",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:68-79",
          "reason": "Does not specify required passing CI checks on protected refs.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:69,74",
          "reason": "Does not require pinning all sources executed by gate checks.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:69-70,74",
          "reason": "Requires protected gate definitions and self-owned CODEOWNERS.",
          "result": "pass",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:75",
          "reason": "Explicitly prohibits broader credentials and channels from bypassing the control.",
          "result": "pass",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:77",
          "reason": "Makes plan and visibility enforcement an explicit prerequisite.",
          "result": "pass",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:76",
          "reason": "Requires periodic checks because configuration drifts silently.",
          "result": "pass",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:70",
          "reason": "Covers both harnesses with mandatory code-owner review.",
          "result": "pass",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": "request.json: inputs.context.facts.opens_prs",
          "reason": "No agent-opened PRs are recommended.",
          "result": "not-applicable",
          "rule_id": "outside.merge.rule-for-agent-prs"
        }
      ],
      "status": "decided"
    }
  ],
  "revision_digest": "03caeb0fd62b468d5be723224f6a732f33ca3d8dc78f77fb6a3453bf87dfce4e",
  "rules_digest": "93fec41536adbe0420026720fecbe03465b27f5f457695dc9d5704d422d7488a",
  "run_id": "bug-report-lifecycle-2026-10-18-closing-extensive",
  "runtime_results": [
    {
      "case_id": "format-explicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: command_execution; network: none requested; bug-report.md sha256 cd9952ee3fcedcd372267c91861f67ba42c0763fa2c404206107552c1feb4739",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/bug-report-format/SKILL.md": "7d42ea98e84f3148e438267365a036dfa62353a463cd48ddd0f2dd1957ce31cd"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.162.1",
      "inventory": "not observable",
      "observed_activation": "read .agents/skills/bug-report-format/SKILL.md",
      "part_id": "A1",
      "prompt": "Use the bug-report-format skill to format the report in bug-report.md. Return the formatted text only; do not contact GitHub.",
      "reason": "read .agents/skills/bug-report-format/SKILL.md",
      "result": "pass",
      "run_id": "bug-report-lifecycle-2026-10-18-closing-extensive"
    },
    {
      "case_id": "format-implicit",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: command_execution; network: none requested; bug-report.md sha256 cd9952ee3fcedcd372267c91861f67ba42c0763fa2c404206107552c1feb4739",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/bug-report-format/SKILL.md": "7d42ea98e84f3148e438267365a036dfa62353a463cd48ddd0f2dd1957ce31cd"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.162.1",
      "inventory": "not observable",
      "observed_activation": null,
      "part_id": "A1",
      "prompt": "Format this new bug report with our team's template. The report is in bug-report.md. Return the text for me to apply to the issue.",
      "reason": "Codex showed no observable activation signal",
      "result": "not-run",
      "run_id": "bug-report-lifecycle-2026-10-18-closing-extensive"
    },
    {
      "case_id": "format-negative",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: command_execution; network: none requested",
      "expected": "does-not-activate",
      "file_hashes": {
        ".agents/skills/bug-report-format/SKILL.md": "7d42ea98e84f3148e438267365a036dfa62353a463cd48ddd0f2dd1957ce31cd"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.162.1",
      "inventory": "not observable",
      "observed_activation": null,
      "part_id": "A1",
      "prompt": "Explain why separating expected behavior from observed behavior helps developers understand bug reports. There is no report to format.",
      "reason": "Codex has no observable signal that proves non-activation",
      "result": "not-run",
      "run_id": "bug-report-lifecycle-2026-10-18-closing-extensive"
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
      "harness_version": "codex-cli 0.162.1",
      "inventory": "not observable",
      "observed_activation": null,
      "part_id": "B",
      "prompt": "Use the reproduction-checklist skill to prepare a reproduction checklist for the approved issue in bug-report.md. This is an offline draft-only exercise; do not post to GitHub.",
      "reason": "Codex showed no observable activation signal",
      "result": "not-run",
      "run_id": "bug-report-lifecycle-2026-10-18-closing-extensive"
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
      "harness_version": "codex-cli 0.162.1",
      "inventory": "not observable",
      "observed_activation": null,
      "part_id": "B",
      "prompt": "Explain what an approved bug report means in a development workflow. I am not requesting a reproduction checklist or any GitHub action.",
      "reason": "Codex has no observable signal that proves non-activation",
      "result": "not-run",
      "run_id": "bug-report-lifecycle-2026-10-18-closing-extensive"
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
      "harness_version": "codex-cli 0.162.1",
      "inventory": "not observable",
      "observed_activation": null,
      "part_id": "C",
      "prompt": "Check the fix against checklist.md using the snapshot in pr-evidence.md. This is an offline evidence review: do not run the application or contact GitHub. Report any limits on a current-commit or merge-enforcement verdict.",
      "reason": "Codex showed no observable activation signal",
      "result": "not-run",
      "run_id": "bug-report-lifecycle-2026-10-18-closing-extensive"
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
      "harness_version": "codex-cli 0.162.1",
      "inventory": "not observable",
      "observed_activation": null,
      "part_id": "C",
      "prompt": "Explain the difference between a GitHub issue and a pull request. Do not inspect a fix, run a checklist, or change anything on GitHub.",
      "reason": "Codex has no observable signal that proves non-activation",
      "result": "not-run",
      "run_id": "bug-report-lifecycle-2026-10-18-closing-extensive"
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
      "harness_version": "codex-cli 0.162.1",
      "inventory": "not observable",
      "observed_activation": "read .agents/skills/diagnose-ci/SKILL.md",
      "part_id": "D",
      "prompt": "Use the diagnose-ci skill to diagnose the failing checks on PR #45 using ci-evidence.md and propose a fix for the developer to apply. This is an offline snapshot review; do not contact GitHub or modify any files.",
      "reason": "read .agents/skills/diagnose-ci/SKILL.md",
      "result": "pass",
      "run_id": "bug-report-lifecycle-2026-10-18-closing-extensive"
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
      "harness_version": "codex-cli 0.162.1",
      "inventory": "not observable",
      "observed_activation": "read .agents/skills/diagnose-ci/SKILL.md",
      "part_id": "D",
      "prompt": "The CI checks on our fix pull request #45 failed. Investigate the evidence in ci-evidence.md and tell me the cause and proposed fix. I will apply and push changes myself. Work offline without modifying files.",
      "reason": "read .agents/skills/diagnose-ci/SKILL.md",
      "result": "pass",
      "run_id": "bug-report-lifecycle-2026-10-18-closing-extensive"
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
      "harness_version": "codex-cli 0.162.1",
      "inventory": "not observable",
      "observed_activation": null,
      "part_id": "D",
      "prompt": "Explain in two sentences what continuous integration means. There is no failing check or pull request to investigate, and no diagnosis is requested.",
      "reason": "Codex has no observable signal that proves non-activation",
      "result": "not-run",
      "run_id": "bug-report-lifecycle-2026-10-18-closing-extensive"
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
      "harness_version": "codex-cli 0.162.1",
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
      "harness_version": "codex-cli 0.162.1",
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
      "harness_version": "codex-cli 0.162.1",
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
