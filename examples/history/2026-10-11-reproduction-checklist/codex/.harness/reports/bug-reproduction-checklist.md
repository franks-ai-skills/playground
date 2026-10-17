# Verification report

- Run: `bug-reproduction-checklist-build-20261011-01`
- Harness KB version: 0.1.0
- Contract digest: ab47344787da0ec7db34297a9c9b3b2506cca6f21ec49a777c14f1bec9c7c522
- Confirmed parts: A
- Decision record digest: ca534abca9d9b8448b9e3aa5e4ca2d926bf65d86e9bb4781750861808a58017a
- Whole-idea answers and targets: `{"facts": {"bypass_mode": true, "caller": "AI agent invoking this procedure in its own workflow, context, tools, and model.", "credentials_external_services_broader_permissions_result": "Return a blocker to the calling agent.", "environment_trust": "unknown", "local_tools_and_test_services_only": true, "missing_tools_result": "Return an error to the calling agent.", "no_code_changes": true, "no_fixes": true, "no_prompt_scope": "Skill runtime; full-access sandbox bypass has not been requested.", "no_tool_installation": true, "opens_prs": false, "permanent_data_loss_payments_publishing_external_disclosure_result": "Return a blocker to the calling agent.", "plan_controls": "unavailable", "reach": "repository", "target_set": "codex"}, "hosting": {"plan": "not applicable", "platform": "local only", "visibility": "unknown"}, "reach": "repository", "targets": ["codex"]}` (digest ec18f34625b7b6784a82d8382bdb7030abc2d375d5de4570ef2b1d9123435489)
- Rule content digest: d57f742e2e061ef35e3497be96cb6e20e1782272b44da47b59abacba8d164e54
- Accepted Idea KB revision: 70dbad821d81ee1443861f063f3cd3c983c5538b201fc5117a7e4f8e71caaebe
- Review scope: Extensive review (rarely needed)
- Rule overrides: none
- Checker versions digest: 49d1dc3feb234903cb74e7ea22c79bd3e66bea53f90e2c85a2ba30f091cdcd1c

## Worker isolation

Workers ran under `best-effort-v1` with isolation status `not-certified`. Research, source-support and review workers run as independent CLI processes with explicit role inputs and the available restrictions. Complete tool absence and context, file and network isolation are not guaranteed; use trusted projects and operator-approved inputs.

- research worker: codex codex-cli 0.162.1, model account default, launcher independent-process, configuration d28f2bef0b1a2d477e3a44729b3bbe7971f0df2924cf44e48fc1fa9f21618a1b, controls: command: ["codex", "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--ephemeral", "--json", "--color", "never", "--strict-config", "-C", "<workspace>", "--output-schema", "<workspace>/output-schema.json", "-c", "approval_policy=\"never\"", "-c", "project_doc_max_bytes=0", "-c", "mcp_servers={}", "-c", "apps._default.enabled=false", "-c", "web_search=\"live\"", "-c", "default_permissions=\"forge-worker\"", "-c", "permissions.forge-worker.filesystem={\":root\"=\"deny\", \":minimal\"=\"read\", \"<workspace>\"=\"read\"}", "-c", "permissions.forge-worker.network.enabled=false", "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "features.hooks=false", "-c", "features.multi_agent=false", "-c", "features.browser_use=false", "-c", "features.browser_use_external=false", "-c", "features.computer_use=false", "-c", "features.image_generation=false", "-c", "features.remote_plugin=false", "-c", "features.tool_suggest=false", "-c", "features.view_image=false", "-c", "features.shell_tool=false", "-c", "features.unified_exec=false", "-"]; environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (ChatGPT), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- source-support worker: codex codex-cli 0.162.1, model account default, launcher independent-process, configuration faf9aa6201600adb491f3d870fcedefb9b6cf86d13bde50a61d7e3e8b755540f, controls: command: ["codex", "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--ephemeral", "--json", "--color", "never", "--strict-config", "-C", "<workspace>", "--output-schema", "<workspace>/output-schema.json", "-c", "approval_policy=\"never\"", "-c", "project_doc_max_bytes=0", "-c", "mcp_servers={}", "-c", "apps._default.enabled=false", "-c", "web_search=\"disabled\"", "-c", "default_permissions=\"forge-worker\"", "-c", "permissions.forge-worker.filesystem={\":root\"=\"deny\", \":minimal\"=\"read\", \"<workspace>\"=\"read\"}", "-c", "permissions.forge-worker.network.enabled=false", "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "features.hooks=false", "-c", "features.multi_agent=false", "-c", "features.browser_use=false", "-c", "features.browser_use_external=false", "-c", "features.computer_use=false", "-c", "features.image_generation=false", "-c", "features.remote_plugin=false", "-c", "features.tool_suggest=false", "-c", "features.view_image=false", "-c", "features.shell_tool=false", "-c", "features.unified_exec=false", "-"]; environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (ChatGPT), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- review worker: codex codex-cli 0.162.1, model account default, launcher independent-process, configuration 0952a1dca9b7ff5765fac8f2121e99b97aa2bce930524db4b061e9ca569f2876, controls: command: ["codex", "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--ephemeral", "--json", "--color", "never", "--strict-config", "-C", "<workspace>", "--output-schema", "<workspace>/output-schema.json", "-c", "approval_policy=\"never\"", "-c", "project_doc_max_bytes=0", "-c", "mcp_servers={}", "-c", "apps._default.enabled=false", "-c", "web_search=\"disabled\"", "-c", "default_permissions=\"forge-worker\"", "-c", "permissions.forge-worker.filesystem={\":root\"=\"deny\", \":minimal\"=\"read\", \"<workspace>\"=\"read\"}", "-c", "permissions.forge-worker.network.enabled=false", "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "features.hooks=false", "-c", "features.multi_agent=false", "-c", "features.browser_use=false", "-c", "features.browser_use_external=false", "-c", "features.computer_use=false", "-c", "features.image_generation=false", "-c", "features.remote_plugin=false", "-c", "features.tool_suggest=false", "-c", "features.view_image=false", "-"]; environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (ChatGPT), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable

## Part A

- Harness result: verified
- Goal result: met by the verified build
- Status: verified
- Outside dependencies: none
- Confirmed answers: `{"event_without_agent": false, "every_time": "usually", "external_system": "none", "irreversible": false, "job": "procedure", "must_survive_compromise": "not-required", "own_context": false, "trigger": "model", "who_disables": "contributor"}`
- Goal verdict: met (The procedure consumes an approved report, inspects code, runs and validates bounded local reproduction without edits or fixes, and returns a checklist or cleaned error/blocker without user interaction. Both accepted requirements are explicitly implemented.)

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| `idea.bug-reproduction-checklist.a.data-risk-check` | error | judged | pass | Requires best-effort internal privacy and data-risk precautions plus mandatory inspection and redaction of every returned result. | .agents/skills/bug-reproduction-checklist/SKILL.md:20,30 | https://firefox-source-docs.mozilla.org/networking/submitting_networking_bugs.html, https://www.sqlite.org/howtocorrupt.html |
| `idea.bug-reproduction-checklist.a.results` | error | judged | pass | Requires validated local steps, precise expected and observed results, and separate labeling of hypotheses. | .agents/skills/bug-reproduction-checklist/SKILL.md:24-26 | https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html |
| `outside.ci.required-on-ref` | warning | judged | fail | No recommendation requires a CI check on a protected ref. | README.md:18-21 | docs/guide/outside-gates.md#ci-pipelines-a-check-is-a-gate-only-if-the-change-cannot-rewrite-it, docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.source-pinned` | warning | judged | fail | No pinned gate-check sources are specified. | README.md:18-21 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.ci.workflow-protected` | warning | judged | fail | Naming the prerequisite does not specify ownership of workflow, policy, scanner, and CODEOWNERS files or pinned external sources. | README.md:20 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.codeowners.agent-config` | warning | judged | fail | Names a control but supplies neither a concrete CODEOWNERS entry for agent configuration nor the setting requiring code-owner review. | README.md:20 | docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners |
| `outside.gate.no-broader-bypass` | warning | judged | fail | Outer isolation is merely named; no restriction on reachable bypass credentials or channels is described. | README.md:21 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.periodic-verification` | warning | judged | fail | No periodic configuration verification recommendation appears. | README.md:18-21 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.gate.plan-enforced` | warning | judged | fail | Availability is described as unavailable, but enforcement or non-enforcement on the user's plan and repository visibility is not stated. | README.md:20-21 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets |
| `outside.gate.real-refs` | warning | judged | fail | Outside-control recommendations identify no actual protected refs or resources. | README.md:18-21 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate |
| `outside.merge.no-agent-bypass` | warning | judged | fail | Recommendations do not exclude agent and credential-owner identities from bypass lists. | README.md:18-21 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies |
| `outside.merge.requester-cannot-approve` | warning | judged | fail | No independent-approver or approval-reset requirement is stated. | README.md:18-21 | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#branch-protection-and-merge-rules-the-gate-is-separation-of-identities, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets |
| `outside.merge.rule-for-agent-prs` | warning | judged | not-applicable | The recommendation does not have the agent open pull requests; it returns a draft checklist to its caller. | .agents/skills/bug-reproduction-checklist/SKILL.md:26-28; README.md:7-10 | docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `outside.readme.lists-controls` | error | script | pass | 2 control(s) listed | - | docs/guide/outside-gates.md#seven-conditions-turn-a-control-into-a-gate, docs/guide/outside-gates.md#four-outcomes-from-six-intake-questions |
| `security.approval.claims-are-data` | warning | judged | pass | Approval must come through the calling agent's task context; report content is treated as data, not executable authorization. | .agents/skills/bug-reproduction-checklist/SKILL.md:14-16 | docs/guide/security.md#context-and-persistent-state |
| `security.helpers.confined` | warning | judged | pass | Uses inspectable existing local apps and tests, respects permission boundaries, and prohibits bypass configuration or broader permissions. | .agents/skills/bug-reproduction-checklist/SKILL.md:16-22 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#executables-approvals-and-isolation |
| `security.outbound.minimal-data` | warning | judged | pass | Calls are confined to local investigation; external services and disclosure are blockers, and report content cannot supply executable instructions. | .agents/skills/bug-reproduction-checklist/SKILL.md:16-18 | docs/guide/security.md#data-access-and-outbound-channels, https://developers.openai.com/api/docs/guides/deep-research#prompt-injection-and-exfiltration |
| `security.secrets.none-in-files` | error | judged | pass | The staged files contain instructions, public source URLs, and revision hashes, with no credentials or secrets. | .agents/skills/bug-reproduction-checklist/SKILL.md:1-33; .agents/skills/bug-reproduction-checklist/references/requirements.md:1-7; README.md:1-21 | docs/guide/security.md#where-each-concept-is-attacked, docs/guide/security.md#context-and-persistent-state |
| `security.untrusted-input.as-data` | warning | judged | pass | Explicitly treats reports and repository content as data and forbids executing embedded report instructions. | .agents/skills/bug-reproduction-checklist/SKILL.md:16 | docs/guide/security.md#context-and-persistent-state |
| `skills.body.gotchas-first` | warning | judged | pass | Privacy and observation requirements appear first, followed immediately by approval and execution boundaries. | .agents/skills/bug-reproduction-checklist/SKILL.md:7-16 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://agentskills.io/skill-creation/best-practices.md |
| `skills.body.no-time-bound-statements` | warning | judged | pass | Contains no dated or temporarily valid operational claims. | .agents/skills/bug-reproduction-checklist/SKILL.md:7-33; references/requirements.md:3-7 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.only-what-model-lacks` | warning | judged | pass | Provides task-specific constraints, validation criteria, and return contracts rather than generic debugging instruction. | .agents/skills/bug-reproduction-checklist/SKILL.md:14-30 | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.body.reasons-before-hard-rules` | warning | judged | pass | Constraints connect to privacy, irreversible effects, preserving user changes, and avoiding unvalidated results; emphatic uppercase wording is absent. | .agents/skills/bug-reproduction-checklist/SKILL.md:20-30 | docs/best-practices/skills.md#7-explain-the-why-before-adding-hard-rules |
| `skills.body.size` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#3-keep-skillmd-lean-and-put-gotchas-first, docs/concepts/skills.md#body, https://code.claude.com/docs/en/skills, https://agentskills.io/specification |
| `skills.body.strictness-matches-fragility` | warning | judged | pass | Strict constraints protect authorization, files, and returned data; local reproduction methods remain flexible with error and blocker exits. | .agents/skills/bug-reproduction-checklist/SKILL.md:16-28 | docs/best-practices/skills.md#5-match-strictness-to-fragility, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.description.boundary` | warning | judged | pass | Explicitly excludes unapproved reports, fixing bugs, and posting comments. | .agents/skills/bug-reproduction-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.description.concise` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, docs/research-notes/agent-harness-best-practices/skills.md |
| `skills.description.length` | error | script | pass | 1 skill(s) checked | - | docs/concepts/skills.md#frontmatter, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/opencode/skills.md#format, https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/loader/mod.rs, https://opencode.ai/docs/skills/ |
| `skills.description.no-workflow-steps` | warning | judged | pass | Summarizes purpose and boundaries without listing procedural steps. | .agents/skills/bug-reproduction-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md |
| `skills.description.voice` | warning | judged | pass | Uses third-person descriptive verbs. | .agents/skills/bug-reproduction-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition |
| `skills.description.what-and-when` | warning | judged | pass | Names investigation and its outputs, then gives the reproduction-checklist use case. | .agents/skills/bug-reproduction-checklist/SKILL.md:3 | docs/best-practices/skills.md#2-write-the-description-as-the-trigger-condition, https://learn.chatgpt.com/docs/build-skills, https://agentskills.io/skill-creation/optimizing-descriptions.md |
| `skills.frontmatter.valid` | error | script | pass | 1 skill(s) checked | - | docs/vendors/opencode/skills.md#format, docs/vendors/codex/skills.md#skillmd-frontmatter-that-codex-reads, docs/vendors/claude-code/skills.md#format, docs/concepts/skills.md#frontmatter, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.goal.no-must-hold-rule-in-skill` | error | judged | pass | The confirmed goal defines an invoked investigation procedure, not a universal event-triggered enforcement control. | request.json: inputs.goals[0]; .agents/skills/bug-reproduction-checklist/SKILL.md:14-30 | docs/best-practices/skills.md#13-move-rules-that-must-hold-every-time-into-hooks, https://code.claude.com/docs/en/skills |
| `skills.inputs.from-message` | warning | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, docs/concepts/skills.md#body |
| `skills.invocation.both-flags` | error | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#invocation-policy-in-both-leads, docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.invocation.side-effects-user-invoked` | error | judged | not-applicable | The skill performs bounded local investigation and explicitly forbids publishing and external state-changing operations. | .agents/skills/bug-reproduction-checklist/SKILL.md:16,22,26 | docs/best-practices/skills.md#8-make-side-effecting-skills-user-invoked-in-both-leads, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.name.format` | error | script | pass | 1 skill(s) checked | - | docs/guide/skills.md#portability, docs/concepts/skills.md#frontmatter, docs/vendors/opencode/skills.md#format, https://opencode.ai/docs/skills/, https://agentskills.io/specification |
| `skills.package.no-auxiliary-docs` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#anti-patterns, https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md |
| `skills.portable.frontmatter` | warning | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#frontmatter, docs/best-practices/skills.md#12-keep-one-canonical-copy-with-portable-frontmatter, https://code.claude.com/docs/en/skills |
| `skills.portable.layout` | error | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#directory-layout, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills, https://learn.chatgpt.com/docs/build-skills |
| `skills.portable.no-claude-placeholders` | warning | script | not-applicable | a condition in applies_to.when does not hold | - | docs/concepts/skills.md#body, docs/guide/skills.md#portability, https://code.claude.com/docs/en/skills |
| `skills.references.load-conditions` | warning | judged | fail | The reference has a loading condition, but repeats both requirements verbatim from the skill body. | .agents/skills/bug-reproduction-checklist/SKILL.md:9-10,32-33; .agents/skills/bug-reproduction-checklist/references/requirements.md:6-7 | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/best-practices.md |
| `skills.references.one-level` | warning | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/specification |
| `skills.references.resolve` | error | script | pass | 1 skill(s) checked | - | docs/best-practices/skills.md#4-disclose-detail-progressively-with-explicit-triggers, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| `skills.reuse.reviewed-and-pinned` | error | judged | not-applicable | a condition in applies_to.when does not hold | - | docs/best-practices/skills.md#security, https://owasp.github.io/www-project-agentic-skills-top-10/ast01 |
| `skills.scope.committed-for-automation` | warning | judged | not-applicable | No CI or cloud execution requirement is specified. | request.json: inputs.goals[0]; README.md:5-10 | docs/concepts/skills.md#directory-layout, https://code.claude.com/docs/en/skills |
| `skills.scripts.agent-caller` | warning | judged | not-applicable | The staged package contains no bundled scripts. | request.json: inputs.files | docs/best-practices/skills.md#6-put-deterministic-logic-in-tested-scripts, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://agentskills.io/skill-creation/using-scripts.md |
| `skills.security.allowed-tools-least-privilege` | warning | judged | not-applicable | applies to claude-code, not the targets | - | docs/best-practices/skills.md#security, docs/vendors/claude-code/skills.md#limits-and-gotchas, https://code.claude.com/docs/en/skills |
| `skills.security.no-surprising-content` | error | judged | pass | Instructions remain within the described local reproduction and cleaned-report scope; no hidden execution or credential-access directives appear. | .agents/skills/bug-reproduction-checklist/SKILL.md:14-33; .agents/skills/bug-reproduction-checklist/references/requirements.md:1-7 | docs/best-practices/skills.md#security, https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md |

Contested `skills.body.reasons-before-hard-rules`:
- All-caps ALWAYS or NEVER is a yellow flag; explain the reasoning instead (https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md, https://agentskills.io/skill-creation/evaluating-skills.md)
- Discipline skills need firm prohibitions and rationalization tables (https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

Contested `skills.description.voice`:
- Always write in the third person; an inconsistent point of view can cause discovery problems (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Use imperative "Use this skill when" phrasing for the trigger (https://agentskills.io/skill-creation/optimizing-descriptions.md, https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)

## Runtime tests

| Part | Case | Harness | Result | Observed | Reason |
| --- | --- | --- | --- | --- | --- |
| A | caller-reproduction | codex codex-cli 0.162.1 | pass | read .agents/skills/bug-reproduction-checklist/SKILL.md | read .agents/skills/bug-reproduction-checklist/SKILL.md |
| A | caller-missing-tool | codex codex-cli 0.162.1 | pass | read .agents/skills/bug-reproduction-checklist/SKILL.md | read .agents/skills/bug-reproduction-checklist/SKILL.md |

## Checked files

```
af2bf17fe095dd59feafe52bee15bef5bd4db3bb00e876ebf496ffec16f8ab26  .agents/skills/bug-reproduction-checklist/SKILL.md
8d3cffd7945237a35c0bfa0816681ba0c0fbbf2fce2e1d84bb850d4f048665d9  .agents/skills/bug-reproduction-checklist/references/requirements.md
47e08a8c286f14650873f3b4be93d566998fbffbd6b580aec369cdf9e461cc2f  README.md
```

## Report data

```json
{
  "answers": {
    "A": {
      "event_without_agent": false,
      "every_time": "usually",
      "external_system": "none",
      "irreversible": false,
      "job": "procedure",
      "must_survive_compromise": "not-required",
      "own_context": false,
      "trigger": "model",
      "who_disables": "contributor"
    }
  },
  "confirmed_parts": [
    "A"
  ],
  "contract_digest": "ab47344787da0ec7db34297a9c9b3b2506cca6f21ec49a777c14f1bec9c7c522",
  "decision_digest": "ca534abca9d9b8448b9e3aa5e4ca2d926bf65d86e9bb4781750861808a58017a",
  "file_hashes": {
    ".agents/skills/bug-reproduction-checklist/SKILL.md": "af2bf17fe095dd59feafe52bee15bef5bd4db3bb00e876ebf496ffec16f8ab26",
    ".agents/skills/bug-reproduction-checklist/references/requirements.md": "8d3cffd7945237a35c0bfa0816681ba0c0fbbf2fce2e1d84bb850d4f048665d9",
    "README.md": "47e08a8c286f14650873f3b4be93d566998fbffbd6b580aec369cdf9e461cc2f"
  },
  "idea_digest": "ec18f34625b7b6784a82d8382bdb7030abc2d375d5de4570ef2b1d9123435489",
  "kb_version": "0.1.0",
  "overrides": [],
  "parts": [
    {
      "goal_result": "met by the verified build",
      "goal_verdict": {
        "reason": "The procedure consumes an approved report, inspects code, runs and validates bounded local reproduction without edits or fixes, and returns a checklist or cleaned error/blocker without user interaction. Both accepted requirements are explicitly implemented.",
        "verdict": "met"
      },
      "harness_result": "verified",
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
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:3",
          "reason": "Names investigation and its outputs, then gives the reproduction-checklist use case.",
          "result": "pass",
          "rule_id": "skills.description.what-and-when"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:3",
          "reason": "Summarizes purpose and boundaries without listing procedural steps.",
          "result": "pass",
          "rule_id": "skills.description.no-workflow-steps"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:3",
          "reason": "Explicitly excludes unapproved reports, fixing bugs, and posting comments.",
          "result": "pass",
          "rule_id": "skills.description.boundary"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:3",
          "reason": "Uses third-person descriptive verbs.",
          "result": "pass",
          "rule_id": "skills.description.voice"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:14-30",
          "reason": "Provides task-specific constraints, validation criteria, and return contracts rather than generic debugging instruction.",
          "result": "pass",
          "rule_id": "skills.body.only-what-model-lacks"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:7-16",
          "reason": "Privacy and observation requirements appear first, followed immediately by approval and execution boundaries.",
          "result": "pass",
          "rule_id": "skills.body.gotchas-first"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:7-33; references/requirements.md:3-7",
          "reason": "Contains no dated or temporarily valid operational claims.",
          "result": "pass",
          "rule_id": "skills.body.no-time-bound-statements"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:9-10,32-33; .agents/skills/bug-reproduction-checklist/references/requirements.md:6-7",
          "reason": "The reference has a loading condition, but repeats both requirements verbatim from the skill body.",
          "result": "fail",
          "rule_id": "skills.references.load-conditions"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:16-28",
          "reason": "Strict constraints protect authorization, files, and returned data; local reproduction methods remain flexible with error and blocker exits.",
          "result": "pass",
          "rule_id": "skills.body.strictness-matches-fragility"
        },
        {
          "check": "judged",
          "citation": "request.json: inputs.files",
          "reason": "The staged package contains no bundled scripts.",
          "result": "not-applicable",
          "rule_id": "skills.scripts.agent-caller"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:20-30",
          "reason": "Constraints connect to privacy, irreversible effects, preserving user changes, and avoiding unvalidated results; emphatic uppercase wording is absent.",
          "result": "pass",
          "rule_id": "skills.body.reasons-before-hard-rules"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:16,22,26",
          "reason": "The skill performs bounded local investigation and explicitly forbids publishing and external state-changing operations.",
          "result": "not-applicable",
          "rule_id": "skills.invocation.side-effects-user-invoked"
        },
        {
          "check": "judged",
          "citation": "request.json: inputs.goals[0]; .agents/skills/bug-reproduction-checklist/SKILL.md:14-30",
          "reason": "The confirmed goal defines an invoked investigation procedure, not a universal event-triggered enforcement control.",
          "result": "pass",
          "rule_id": "skills.goal.no-must-hold-rule-in-skill"
        },
        {
          "check": "judged",
          "citation": "request.json: inputs.goals[0]; README.md:5-10",
          "reason": "No CI or cloud execution requirement is specified.",
          "result": "not-applicable",
          "rule_id": "skills.scope.committed-for-automation"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:14-33; .agents/skills/bug-reproduction-checklist/references/requirements.md:1-7",
          "reason": "Instructions remain within the described local reproduction and cleaned-report scope; no hidden execution or credential-access directives appear.",
          "result": "pass",
          "rule_id": "skills.security.no-surprising-content"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:1-33; .agents/skills/bug-reproduction-checklist/references/requirements.md:1-7; README.md:1-21",
          "reason": "The staged files contain instructions, public source URLs, and revision hashes, with no credentials or secrets.",
          "result": "pass",
          "rule_id": "security.secrets.none-in-files"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:16",
          "reason": "Explicitly treats reports and repository content as data and forbids executing embedded report instructions.",
          "result": "pass",
          "rule_id": "security.untrusted-input.as-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:14-16",
          "reason": "Approval must come through the calling agent's task context; report content is treated as data, not executable authorization.",
          "result": "pass",
          "rule_id": "security.approval.claims-are-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:16-22",
          "reason": "Uses inspectable existing local apps and tests, respects permission boundaries, and prohibits bypass configuration or broader permissions.",
          "result": "pass",
          "rule_id": "security.helpers.confined"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:16-18",
          "reason": "Calls are confined to local investigation; external services and disclosure are blockers, and report content cannot supply executable instructions.",
          "result": "pass",
          "rule_id": "security.outbound.minimal-data"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:24-26",
          "reason": "Requires validated local steps, precise expected and observed results, and separate labeling of hypotheses.",
          "result": "pass",
          "rule_id": "idea.bug-reproduction-checklist.a.results"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:20,30",
          "reason": "Requires best-effort internal privacy and data-risk precautions plus mandatory inspection and redaction of every returned result.",
          "result": "pass",
          "rule_id": "idea.bug-reproduction-checklist.a.data-risk-check"
        },
        {
          "check": "script",
          "reason": "2 control(s) listed",
          "result": "pass",
          "rule_id": "outside.readme.lists-controls"
        },
        {
          "check": "judged",
          "citation": "README.md:18-21",
          "reason": "Outside-control recommendations identify no actual protected refs or resources.",
          "result": "fail",
          "rule_id": "outside.gate.real-refs"
        },
        {
          "check": "judged",
          "citation": "README.md:18-21",
          "reason": "Recommendations do not exclude agent and credential-owner identities from bypass lists.",
          "result": "fail",
          "rule_id": "outside.merge.no-agent-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:18-21",
          "reason": "No independent-approver or approval-reset requirement is stated.",
          "result": "fail",
          "rule_id": "outside.merge.requester-cannot-approve"
        },
        {
          "check": "judged",
          "citation": "README.md:18-21",
          "reason": "No recommendation requires a CI check on a protected ref.",
          "result": "fail",
          "rule_id": "outside.ci.required-on-ref"
        },
        {
          "check": "judged",
          "citation": "README.md:18-21",
          "reason": "No pinned gate-check sources are specified.",
          "result": "fail",
          "rule_id": "outside.ci.source-pinned"
        },
        {
          "check": "judged",
          "citation": "README.md:20",
          "reason": "Naming the prerequisite does not specify ownership of workflow, policy, scanner, and CODEOWNERS files or pinned external sources.",
          "result": "fail",
          "rule_id": "outside.ci.workflow-protected"
        },
        {
          "check": "judged",
          "citation": "README.md:21",
          "reason": "Outer isolation is merely named; no restriction on reachable bypass credentials or channels is described.",
          "result": "fail",
          "rule_id": "outside.gate.no-broader-bypass"
        },
        {
          "check": "judged",
          "citation": "README.md:20-21",
          "reason": "Availability is described as unavailable, but enforcement or non-enforcement on the user's plan and repository visibility is not stated.",
          "result": "fail",
          "rule_id": "outside.gate.plan-enforced"
        },
        {
          "check": "judged",
          "citation": "README.md:18-21",
          "reason": "No periodic configuration verification recommendation appears.",
          "result": "fail",
          "rule_id": "outside.gate.periodic-verification"
        },
        {
          "check": "judged",
          "citation": "README.md:20",
          "reason": "Names a control but supplies neither a concrete CODEOWNERS entry for agent configuration nor the setting requiring code-owner review.",
          "result": "fail",
          "rule_id": "outside.codeowners.agent-config"
        },
        {
          "check": "judged",
          "citation": ".agents/skills/bug-reproduction-checklist/SKILL.md:26-28; README.md:7-10",
          "reason": "The recommendation does not have the agent open pull requests; it returns a draft checklist to its caller.",
          "result": "not-applicable",
          "rule_id": "outside.merge.rule-for-agent-prs"
        },
        {
          "check": "judged",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.inputs.from-message"
        },
        {
          "check": "script",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.invocation.both-flags"
        },
        {
          "check": "script",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.portable.frontmatter"
        },
        {
          "check": "script",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.portable.layout"
        },
        {
          "check": "script",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.portable.no-claude-placeholders"
        },
        {
          "check": "judged",
          "reason": "a condition in applies_to.when does not hold",
          "result": "not-applicable",
          "rule_id": "skills.reuse.reviewed-and-pinned"
        },
        {
          "check": "judged",
          "reason": "applies to claude-code, not the targets",
          "result": "not-applicable",
          "rule_id": "skills.security.allowed-tools-least-privilege"
        }
      ],
      "status": "verified"
    }
  ],
  "revision_digest": "70dbad821d81ee1443861f063f3cd3c983c5538b201fc5117a7e4f8e71caaebe",
  "rules_digest": "d57f742e2e061ef35e3497be96cb6e20e1782272b44da47b59abacba8d164e54",
  "run_id": "bug-reproduction-checklist-build-20261011-01",
  "runtime_results": [
    {
      "case_id": "caller-reproduction",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: command_execution; network: none requested; app.sh sha256 91c470006f54fdb700bfa32be38d5d9de770eff71c9a42849553f38842697534; bug-report.md sha256 9691f3d0e17e13ef006dc126a8e8981ec0301e9574a94a77c0878f5555d15fc8; test-zero.sh sha256 3a73b1b1406c31fb0d96b129c53339dc77b525d899fe9d1438ae379d32a7f3e7",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/bug-reproduction-checklist/SKILL.md": "af2bf17fe095dd59feafe52bee15bef5bd4db3bb00e876ebf496ffec16f8ab26",
        ".agents/skills/bug-reproduction-checklist/references/requirements.md": "8d3cffd7945237a35c0bfa0816681ba0c0fbbf2fce2e1d84bb850d4f048665d9"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.162.1",
      "observed_activation": "read .agents/skills/bug-reproduction-checklist/SKILL.md",
      "part_id": "A",
      "prompt": "You are the calling AI agent's reproduction stage. Use the bug-reproduction-checklist skill on the approved report in bug-report.md. Inspect the existing local app and test, establish valid reproduction steps without changing any code, and return the checklist to this workflow without questions or installations.",
      "reason": "read .agents/skills/bug-reproduction-checklist/SKILL.md",
      "result": "pass",
      "run_id": "bug-reproduction-checklist-build-20261011-01"
    },
    {
      "case_id": "caller-missing-tool",
      "environment": "throwaway workspace with only the frozen skill and fixtures; tools: command_execution; network: none requested; README.md sha256 f9fb5566b7373301101c4be2b8c85a836ffa3f044fb0057b436d8de1c4595d8f; bug-report.md sha256 85ad1fbbcd81c44d3b6157fb319dbb834406efb641c8296709e5163ac256aee4",
      "expected": "activates",
      "file_hashes": {
        ".agents/skills/bug-reproduction-checklist/SKILL.md": "af2bf17fe095dd59feafe52bee15bef5bd4db3bb00e876ebf496ffec16f8ab26",
        ".agents/skills/bug-reproduction-checklist/references/requirements.md": "8d3cffd7945237a35c0bfa0816681ba0c0fbbf2fce2e1d84bb850d4f048665d9"
      },
      "harness": "codex",
      "harness_version": "codex-cli 0.162.1",
      "observed_activation": "read .agents/skills/bug-reproduction-checklist/SKILL.md",
      "part_id": "A",
      "prompt": "The agent workflow needs an issue-comment reproduction checklist for the approved bug report in bug-report.md. Investigate locally using the existing repository and tools. Return the result to the calling agent without user questions, installations, or code changes.",
      "reason": "read .agents/skills/bug-reproduction-checklist/SKILL.md",
      "result": "pass",
      "run_id": "bug-reproduction-checklist-build-20261011-01"
    }
  ],
  "scope": "Extensive review (rarely needed)",
  "symlinks": {},
  "tool_versions": {
    "harness-forge-checkers": "49d1dc3feb234903cb74e7ea22c79bd3e66bea53f90e2c85a2ba30f091cdcd1c"
  },
  "whole_idea": {
    "facts": {
      "bypass_mode": true,
      "caller": "AI agent invoking this procedure in its own workflow, context, tools, and model.",
      "credentials_external_services_broader_permissions_result": "Return a blocker to the calling agent.",
      "environment_trust": "unknown",
      "local_tools_and_test_services_only": true,
      "missing_tools_result": "Return an error to the calling agent.",
      "no_code_changes": true,
      "no_fixes": true,
      "no_prompt_scope": "Skill runtime; full-access sandbox bypass has not been requested.",
      "no_tool_installation": true,
      "opens_prs": false,
      "permanent_data_loss_payments_publishing_external_disclosure_result": "Return a blocker to the calling agent.",
      "plan_controls": "unavailable",
      "reach": "repository",
      "target_set": "codex"
    },
    "hosting": {
      "plan": "not applicable",
      "platform": "local only",
      "visibility": "unknown"
    },
    "reach": "repository",
    "targets": [
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
