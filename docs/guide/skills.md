# Skills

A skill is a named package of instructions, a directory with a `SKILL.md` file and optional scripts and reference files, that the agent loads only when it is needed. Until then only the skill's name and a short description sit in context, so a harness can offer many procedures at a small, fixed context cost and keep procedures out of always-loaded [instructions](instructions.md). All three harnesses follow the Agent Skills open standard (agentskills.io) at the core and add their own extensions; a skill that only the user can invoke replaces custom [commands](commands.md).

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Unit | Directory with `SKILL.md` plus supporting files ([CC][cc-skills]) | Directory with `SKILL.md`, optional `agents/openai.yaml`, `scripts/`, `references/`, `assets/` ([Codex][cx-skills]) | Directory with `SKILL.md` ([OC][oc-skills]) |
| Project scope | `.claude/skills/<name>/` from the start directory up to the repo root; nested `<subdir>/.claude/skills/` loads once Claude reads a file there ([CC][cc-skills]) | `.agents/skills/` from the cwd up to the repo root ([Codex][cx-skills]) | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/`, up to the git worktree ([OC][oc-skills]) |
| User scope | `~/.claude/skills/` ([CC][cc-skills]) | `~/.agents/skills`; deprecated `$CODEX_HOME/skills` still read ([Codex][cx-skills]) | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` ([OC][oc-skills]) |
| Admin scope | `.claude/skills/` in the managed settings directory ([CC][cc-skills]) | `/etc/codex/skills` ([Codex][cx-skills]) | Not recorded |
| Plugin-provided | `<plugin>/skills/<name>/SKILL.md`, namespaced `/plugin:name` ([CC][cc-skills]) | `skills/<name>/SKILL.md` in a plugin ([Codex][cx-skills]) | Not recorded |
| Required fields | None; `name` defaults to the directory name ([CC][cc-skills]) | `description` (empty is an error); `name` falls back to the directory name ([Codex][cx-skills]) | `name` (spec regex, equal to the directory) and `description` ([OC][oc-skills]) |
| Fields acted on | Spec fields plus Claude-only keys (`disable-model-invocation`, `allowed-tools`, `context`, `hooks`, `paths`, …) ([CC][cc-skills]) | `name`, `description`, `metadata.short-description`; policy, UI and dependencies live in `agents/openai.yaml` ([Codex][cx-skills]) | `name`, `description`, `license`, `compatibility`, `metadata` ([OC][oc-skills]) |
| Description limit | `description` + `when_to_use` truncated together at 1,536 chars ([CC][cc-skills]) | 1,024 chars ([Codex][cx-skills]) | 1–1,024 chars ([OC][oc-skills]) |
| Catalog in context | Name and description; 1% of the context window; on overflow, least-invoked descriptions drop first ([CC][cc-skills]) | Name, description and file path; 2% of the context window or 8,000 chars; descriptions shortened, then skills omitted with a warning ([Codex][cx-skills]) | Name and description in the `skill` tool description ([OC][oc-skills]) |
| Body loading | On invocation; stays in context; re-attached after compaction (5,000 tokens each, 25,000 combined) ([CC][cc-skills]) | Full `SKILL.md` read when selected ([Codex][cx-skills]) | Model calls `skill({ name })` ([OC][oc-skills]) |
| Explicit invocation | `/name` ([CC][cc-skills]) | `$name` or the `/skills` picker ([Codex][cx-skills]) | `/name` ([OC][oc-skills]) |
| Implicit invocation | Skill tool, matched on the description ([CC][cc-skills]) | Description match ([Codex][cx-skills]) | `skill` tool ([OC][oc-skills]) |
| Turn off model invocation | `disable-model-invocation: true` ([CC][cc-skills]) | `policy.allow_implicit_invocation: false` in `agents/openai.yaml` ([Codex][cx-skills]) | No model-only switch; `permission.skill: deny` hides the skill ([OC][oc-skills]) |
| Disable without deleting | `skillOverrides`: `on` / `name-only` / `user-invocable-only` / `off` ([CC][cc-skills]) | `[[skills.config]]` with `enabled = false`; restart required ([Codex][cx-skills]) | `permission.skill`: `allow` / `ask` / `deny` ([OC][oc-skills]) |
| Arguments | `$ARGUMENTS`, `$N`, named ([CC][cc-skills]) | None; text after `$name` is part of the message ([Codex][cx-skills]) | Not recorded for skills ([OC][oc-skills]) |
| Symlinked skill folders | Allowed ([CC][cc-skills]) | Followed for user, repo and admin scopes ([Codex][cx-skills]) | Not recorded |

Bundled skills, extra roots, name-collision rules and change detection are in the vendor pages.

## Generalized model

- **Skill package.** A directory named after the skill. It holds `SKILL.md` (YAML frontmatter and a Markdown body) and optionally `scripts/` (executed, not loaded), `references/` (read on demand) and `assets/` (templates).
- **Frontmatter.** `name` and `description` carry the model. `license`, `compatibility` and `metadata` (string-to-string map) are optional and informational.
- **Harness extension metadata.** Each lead keeps extra settings in its own place: Claude Code as extra frontmatter keys, Codex in a sidecar file. Both ignore what they do not understand.
- **Skill root and scope.** A directory scanned for `<name>/SKILL.md`. Scopes are project (committed, scanned from the cwd up to the repo root), user, admin, bundled and plugin. Precedence on a name collision is not portable.
- **Catalog.** The per-session list of skills the model sees, rendered under a budget proportional to the context window.
- **Lifecycle.** Discover roots at session start; list the catalog (on overflow shorten descriptions first, then drop entries); activate on explicit user request or on a description match; load the body; load resources only when the body says so.
- **Invocation policy.** Two flags per skill: model-invocable (off removes the description from the catalog; explicit invocation still works) and enabled (off hides and blocks the skill). A user-invocable flag exists in Claude Code only.

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Project root | `.claude/skills/` | `.agents/skills/` | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` |
| User root | `~/.claude/skills/` | `~/.agents/skills/` | `~/.config/opencode/skills/` and the two above |
| Harness extension metadata | Extra frontmatter keys | `agents/openai.yaml` | — |
| Catalog budget | 1% (`skillListingBudgetFraction`) | 2% (`skills.max_context_tokens`) | — |
| Explicit invocation | `/name` | `$name`, `/skills` | `/name` |
| Model-invocable = off | `disable-model-invocation: true` | `policy.allow_implicit_invocation: false` | — |
| Enabled = off | `skillOverrides: off` | `[[skills.config]] enabled = false` | `permission.skill: deny` |

## When to use it and when not

A skill fits a recurring procedure or specialized knowledge that the model lacks, that is needed only sometimes, and where an occasional missed activation is acceptable.

| Use it when | Notes |
| --- | --- |
| You keep pasting the same procedure or checklist into chat | The catalog entry is cheap; "long reference material costs almost nothing until you need it" ([Claude Code skills](https://code.claude.com/docs/en/skills)) |
| An instruction-file section "has grown into a procedure rather than a fact" | Moves recurring cost out of every session ([Claude Code skills](https://code.claude.com/docs/en/skills)) |
| A procedure has side effects or timing (deploy, commit, send a message) | Make it user-invoked ([Approaches](#approaches)) |
| An operation must be deterministic and is reinvented each run | Bundle a script in `scripts/` |

| Do not use it when | Use instead | Cost or risk of a skill |
| --- | --- | --- |
| A fact or convention is needed in every session | [Instructions](instructions.md) | The skill may never load |
| Knowledge must always be applied and its omission silently produces wrong output | A compressed index or a trigger pointer in [instructions](instructions.md) | Skill not invoked in 56% of cases in Vercel's eval ([Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)) |
| A rule must hold every time an event occurs | [Hooks](hooks.md) | Skills are context; after compaction older skills "may drop entirely" |
| The work should run isolated from the conversation or in the background | [Subagents](subagents.md); a subagent can use skills | The body and its output fill the main context |
| The agent needs access to an external system or data | [MCP](mcp.md); a skill teaches what to do with it | "MCP connects to data; Skills teach Claude what to do with that data" ([Anthropic blog](https://claude.com/blog/skills-explained)) |
| Several skills, or skills plus a connector, are shared across repositories | [Plugins](plugins.md) | A plugin adds versioned releases and namespacing ([Codex build skills](https://learn.chatgpt.com/docs/build-skills)) |
| The task is one step the model handles alone | Nothing | Agents "only consult skills for tasks that require knowledge or capabilities beyond what they can handle alone" ([agentskills.io](https://agentskills.io/skill-creation/optimizing-descriptions.md)) |

## Approaches

### Model-invoked skill

- **What:** the default. Name and description sit in the catalog; the model activates the skill when a task matches.
- **When it fits:** knowledge or a procedure the agent should apply without being asked.
- **How:** activation depends entirely on the description. Claude Code activates through the Skill tool; Codex chooses on a description match.
- **Trade-off:** each catalog entry costs "a few dozen extra tokens" [Practitioner] ([Simon Willison](https://simonwillison.net/2025/Oct/16/claude-skills/), older). Implicit activation is unreliable: a practitioner measured 50–55% activation without help ([Scott Spence](https://scottspence.com/posts/measuring-claude-code-skill-activation-with-sandboxed-evals)), and SkillsBench saw Codex CLI agents "acknowledge Skills content but often implement solutions independently", with Claude Code showing the highest skill use ([SkillsBench](https://arxiv.org/html/2602.12670v1)).

### User-invoked skill

- **What:** a skill with model invocation off. Only the user starts it. Both leads replaced custom commands with this ([commands](commands.md)).
- **When it fits:** side effects or timing: "You don't want Claude deciding to deploy because your code looks ready" ([Claude Code skills](https://code.claude.com/docs/en/skills)).
- **How:** `disable-model-invocation: true` (Claude Code, invoke with `/name`) and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` (Codex, invoke with `$name`), both in the same folder.
- **Trade-off:** no catalog cost. In Claude Code the flag also blocks scheduled tasks and subagent preloading; in Codex a scheduled prompt naming `$name` still runs it.

### Pointer in the instruction file plus skill

- **What:** a one-line pointer in `AGENTS.md` that tells the agent when to load the skill, or a compressed index in the instruction file instead of a skill.
- **When it fits:** knowledge whose omission causes silently wrong output.
- **How:** Vercel's 8 KB docs index in `AGENTS.md` scored 100%; skills reached at most 79% even with explicit instructions, against a 53% baseline without docs. Wording mattered: "You MUST invoke the skill" anchored the agent on the docs; "Explore project first, then invoke skill" scored better ([Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)).
- **Trade-off:** costs instruction budget every session. Evidence is one framework with unnamed models.

### Script-backed skill

- **What:** a skill whose core is scripts in `scripts/`, with the body saying when and how to run them.
- **When it fits:** fragile or deterministic operations, or when traces show the agent rewriting the same helper each run.
- **How:** see [practice 6](#practices). Pre-approval differs: Claude Code can pre-approve scripts through `allowed-tools`; Codex gates them through `approval_policy.granular.skill_approval`.
- **Trade-off:** "Prefer instructions over scripts unless you need deterministic behavior or external tooling" ([Codex build skills](https://learn.chatgpt.com/docs/build-skills)). Scripts are code to maintain and review; only their output enters context.

### Skill that delegates to a subagent

- **What:** a skill whose work runs in a subagent.
- **When it fits:** skills "with explicit instructions and concrete tasks, not guidelines" ([Claude Code skills](https://code.claude.com/docs/en/skills)).
- **How:** Claude Code `context: fork` runs the skill in a subagent that does not see the conversation. Codex skills cannot run themselves in a subagent; a portable skill names the subagent in its body, which is also how Codex gets delegation at all ([subagents](subagents.md)).
- **Trade-off:** `context: fork` is Claude-only.

### Distribution and scope

- **What:** project (committed), user (personal), plugin (shared across repos, versioned, namespaced) or admin (organization).
- **When it fits:** project scope for anything tied to a repo or needed by CI and cloud runs, because Claude Code cloud sessions ignore `~/.claude/skills/`. User scope for personal workflow.
- **How:** one canonical copy, symlinked into the other lead's root ([Portability](#portability)).
- **Trade-off:** Codex's `$skill-installer` writes to the deprecated `$CODEX_HOME/skills`, invisible to Claude Code.

## Practices

1. **Write a skill only where it adds what the model lacks.**
   - Why: skills help most where pretraining coverage is weak. SkillsBench measured +16.2 pp on average, but +4.5 pp for software engineering, and 16 of 84 tasks got worse.
   - How: run representative tasks without a skill, record failures, then write minimal instructions that close the gap. Keep the skill only if it beats the baseline.
   - Evidence: [Empirical] ([SkillsBench](https://arxiv.org/html/2602.12670v1)); [Advisory] "Would the agent get this wrong without this instruction? If the answer is no, cut it" ([agentskills.io best practices](https://agentskills.io/skill-creation/best-practices.md)); [Vendor] evaluation-driven development ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)).
2. **Write the description as the trigger condition.**
   - Why: "The body loads only after triggering." Both leads truncate descriptions. Under-triggering is the default failure. A description that summarizes the workflow gets followed instead of the body: one mentioning "code review between tasks" led agents to do one review where the body said two.
   - How: one sentence of what (concrete verbs and objects), then "Use when …" with phrases a user would say, then a boundary ("Not for … — use X instead"). Key words first, about 500 characters, no workflow steps. Fix false triggers by stating what the skill does not do, not by adding keywords from failed queries.
   - Evidence: [Advisory] ([optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions.md)); [Vendor] "front-load the key use case and trigger words" ([Codex build skills](https://learn.chatgpt.com/docs/build-skills)), Claude "undertriggers" ([Anthropic skill-creator](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md)); [Practitioner] the two-reviews failure ([superpowers](https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)). Sources disagree on voice: Anthropic requires third person, agentskills.io and superpowers use "Use when …"; all reject "I can …" and "You can …".
3. **Keep `SKILL.md` lean and put gotchas first.**
   - Why: "Every line is a recurring token cost once the skill loads." Only the first 5,000 tokens per skill are re-attached after compaction in Claude Code. Focused skills scored +18.8 pp, comprehensive ones −2.9 pp.
   - How: under 500 lines and about 5,000 tokens. Write only what the model would otherwise get wrong. Keep gotchas in `SKILL.md`, not in a reference the agent may not open. No README or CHANGELOG inside the skill.
   - Evidence: [Advisory] ([specification](https://agentskills.io/specification)); [Vendor] ([Claude Code skills](https://code.claude.com/docs/en/skills), [Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)); [Empirical] ([SkillsBench](https://arxiv.org/html/2602.12670v1)).
4. **Disclose detail progressively with explicit triggers.**
   - Why: nested references cause partial reads, and a generic "see references/" gives the agent no reason to open a file.
   - How: `references/` one level deep, each with a load condition ("Read `references/api-errors.md` if the API returns a non-200 status code"). Each fact in one place. A table of contents in files over 100 lines. Reference other skills by name; `@path` force-loads them.
   - Evidence: [Vendor] ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)); [Advisory] ([agentskills.io best practices](https://agentskills.io/skill-creation/best-practices.md)). No controlled study of reference layout exists.
5. **Match strictness to fragility.**
   - Why: prescriptive steps where many approaches work railroad the agent; freedom where an operation is fragile breaks things.
   - How: heuristics where many approaches work; "Run exactly this script" where one wrong step fails. One default with an escape hatch, not a menu. For destructive or batch work: plan, validate with a script, then execute.
   - Evidence: [Vendor] ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [OpenAI skill-creator](https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md)); [Advisory] "Provide defaults, not menus" ([agentskills.io best practices](https://agentskills.io/skill-creation/best-practices.md)).
6. **Put deterministic logic in tested scripts built for an agent caller.**
   - Why: pre-made scripts are "more reliable than generated code", save tokens and keep results consistent.
   - How: no interactive prompts; `--help` as the interface; structured output on stdout and diagnostics on stderr; errors that say what was expected; `--dry-run` and safe defaults for destructive actions; bounded output (harnesses truncate around 10–30K characters); pinned, self-contained dependencies; paths relative to the skill root.
   - Evidence: [Vendor] ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)); [Advisory] ([agentskills.io using scripts](https://agentskills.io/skill-creation/using-scripts.md)).
7. **Explain the why before adding hard rules.**
   - Why: reasoned instructions generalize; shouted rules over-apply. Discipline skills that agents skip under pressure may still need firm wording.
   - How: write the rule with its reason. Add a direct prohibition only where evals show the agent rationalizing past it. Test with every model you plan to use.
   - Evidence: sources conflict. [Vendor] all-caps ALWAYS/NEVER is "a yellow flag" ([Anthropic skill-creator](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md)), yet Anthropic's own iteration example strengthens wording to "MUST filter" ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)); [Practitioner] superpowers prescribes prohibitions and rationalization tables ([superpowers](https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)); [Empirical] "You MUST invoke the skill" backfired ([Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)).
8. **Make side-effecting skills user-invoked in both leads, and read inputs from the message.**
   - Why: the model should not decide to deploy or commit. Codex skills have no argument substitution.
   - How: set both flags ([User-invoked skill](#user-invoked-skill)). Write "The user names the issue number in their message; if missing, ask." Keep a good description; it appears in menus. Keep the skill model-invocable if a Claude Code schedule must run it.
   - Evidence: [Vendor] ([Claude Code skills](https://code.claude.com/docs/en/skills), [Codex build skills](https://learn.chatgpt.com/docs/build-skills)).
9. **Write evals first and test triggering and behavior separately.**
   - Why: a skill fails either by not triggering or by doing the wrong thing. Runs are noisy; a baseline varied 5 points between identical runs.
   - How: a trigger set of about 20 prompts, half should-trigger and half near-miss should-not-trigger, each run 3+ times. A behavior set of 2–3 cases growing to 10–20, run with and without the skill in fresh sessions, graded deterministically first. Pin the model; re-run on skill changes and model upgrades.
   - Evidence: [Advisory] ([optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions.md), [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills.md)); [Vendor] ([Claude Code plugin evals](https://code.claude.com/docs/en/plugin-evals), [OpenAI eval blog](https://developers.openai.com/blog/eval-skills)); [Practitioner] run-to-run variance ([Scott Spence](https://scottspence.com/posts/measuring-claude-code-skill-activation-with-sandboxed-evals)).
10. **Ground skills in human domain knowledge.**
    - Why: self-generated skills averaged −1.3 pp versus no skill: "models cannot reliably author the procedural knowledge they benefit from consuming".
    - How: do the task with the agent once, then extract what had to be corrected. Source content from runbooks, review comments and incident reports.
    - Evidence: [Empirical] ([SkillsBench](https://arxiv.org/html/2602.12670v1)); [Advisory] ([agentskills.io best practices](https://agentskills.io/skill-creation/best-practices.md)).
11. **Keep the library small and curated.**
    - Why: both catalogs are 1–2% of context and truncate silently; with Codex's 8,000-character floor, about 16 skills at 500 characters fill it. Two to three skills per task gave +18.6 pp, four or more +5.9 pp.
    - How: one coherent job per skill. Prune never-invoked skills (`/skill-doctor` in Claude Code). Turn rarely needed ones into user-invoked skills.
    - Evidence: [Vendor] ([Codex build skills](https://learn.chatgpt.com/docs/build-skills), [Claude Code skills](https://code.claude.com/docs/en/skills)); [Empirical] skills per task, not catalog size ([SkillsBench](https://arxiv.org/html/2602.12670v1)).
12. **Move rules that must hold every time into hooks.**
    - Why: skills are context and can drop out after compaction.
    - How: a regular [hook](hooks.md) in both leads. Claude Code also supports hooks scoped to a skill while it is active.
    - Evidence: [Vendor] "move rules into hooks if they must hold every time" ([Claude Code skills](https://code.claude.com/docs/en/skills)).

## Security

**Threat: third-party skills are code and prompt injection with your privileges.** The body is an injection surface and `scripts/` is code. Measured prevalence depends on method:

- [Empirical] 26.1% of 31,132 skills had at least one vulnerability; 5.2% showed high-severity patterns suggesting malicious intent ([arXiv 2601.10338](https://arxiv.org/abs/2601.10338)).
- [Empirical] 157 confirmed malicious skills among 98,380; dominant patterns are credential theft through code execution and covert instructions in documentation files ([arXiv 2602.06547](https://arxiv.org/abs/2602.06547)).
- [Empirical] 13.4% of 3,984 marketplace skills had a critical issue; 2.9% fetch and execute remote content at runtime ([Snyk](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub)).
- [Empirical] Conflicting estimate: scanners flagged up to 46.8% of 238,180 skills, but only 0.52% stayed suspicious with repository context ([arXiv 2603.16572](https://arxiv.org/abs/2603.16572)).

**Threat: repository skills grant tools without trust.** In Claude Code, "Workspace trust doesn't gate `allowed-tools`"; a project skill applies even in `-p` runs in untrusted folders ([Claude Code skills](https://code.claude.com/docs/en/skills)).

**Mitigations.**

- Read every file of a third-party skill, not only `SKILL.md`. Search for hidden directives ("do not mention"), remote fetch-and-run, base64, network and credential access in scripts.
- Check Claude Code `allowed-tools`, `hooks` and `` !`cmd` ``; check Codex `agents/openai.yaml` `dependencies.tools`.
- Pin by commit or hash and re-review on every update. [Advisory] OWASP: "Hash-pin installed skills" and alert on modifications ([OWASP AST01](https://owasp.github.io/www-project-agentic-skills-top-10/ast01)).
- Claude Code: `allowManagedPermissionRulesOnly` ignores skill `allowed-tools`; `disableSkillShellExecution` turns off `` !`cmd` ``. Codex: `approval_policy.granular.skill_approval` gates skill scripts.
- Evaluate untrusted skills in a container or CI runner; running `claude plugin eval` "is the same trust decision as `claude --plugin-dir`" ([Claude Code plugin evals](https://code.claude.com/docs/en/plugin-evals)).
- No vendor signing or provenance mechanism for skills exists in either lead.

## Verification and checklist

- **Structure:** `claude plugin validate .claude/skills`; `skills-ref validate ./my-skill` for the spec; `scripts/quick_validate.py` from the Codex skill-creator.
- **Discovery:** ask "What skills are available?"; invoke explicitly with `/name` or `$name` to separate content problems from trigger problems.
- **Triggering, headless:** `claude -p "$query" --output-format json` and look for a `Skill` tool use; `codex exec --json` traces for Codex. Which Codex event marks an implicit skill load is undocumented.
- **Claude Code evals:** `claude plugin eval` runs case directories with `tool_used`, `regex`, `llm` and `baseline` graders, three runs per arm, and reports `Δ` against a no-plugin arm; `--threshold` fails CI below it ([Claude Code plugin evals](https://code.claude.com/docs/en/plugin-evals)).
- **Codex evals:** 10–20 prompts in a CSV covering explicit, implicit and should-not-trigger cases; traces from `codex exec --json`; a rubric via a second `codex exec --output-schema` ([OpenAI eval blog](https://developers.openai.com/blog/eval-skills)).
- **In real use:** `/skill-doctor` reports context cost and never-invoked skills.

Checklist:

- [ ] A no-skill baseline showed the skill is needed; trigger and behavior evals exist.
- [ ] `name` is spec-valid and equals the directory name.
- [ ] `description` states what, "Use when …" and a boundary; key words first; no workflow steps.
- [ ] `SKILL.md` is under 500 lines with gotchas near the top; references are one level deep with load conditions.
- [ ] Scripts are non-interactive, bounded, with `--help`, clear errors and `--dry-run` for destructive actions.
- [ ] Side-effecting skills set both lead flags for user-only invocation.
- [ ] Shared skills use only portable frontmatter; one canonical copy is symlinked into the other root.
- [ ] Skills needed by CI or cloud runs are committed.
- [ ] The catalog fits both budgets; never-invoked skills are pruned.
- [ ] Every third-party skill was read in full and pinned.

## Portability

**Directory layout.** The leads share no skill directory: Claude Code never reads `.agents/`, and Codex does not read `.claude/skills`. Keep one canonical copy in `.agents/skills/<name>/` and symlink `.claude/skills/<name>` to it; both leads follow symlinked skill folders. Repeat at user scope with `~/.agents/skills/` and `~/.claude/skills/`. The reverse direction works too.

**Frontmatter.**

| Field | Rule for portable skills |
| --- | --- |
| `name` | 1–64 chars, lowercase `a-z`, `0-9`, single hyphens, equal to the directory name; OpenCode enforces this |
| `description` | Non-empty, at most 1,024 chars, one line, trigger words first |
| `license`, `compatibility`, `metadata` | Safe and informational; `metadata` is a string-to-string map |
| Claude-only keys (`allowed-tools`, `context`, `hooks`, `paths`, `model`, …) | Ignored by Codex and OpenCode; hard error when uploaded to claude.ai, the Skills API or `package_skill.py` ([CC][cc-skills]) |
| `agents/openai.yaml` | Codex-only sidecar; leaves `SKILL.md` untouched |

Traps:

- **User-only invocation needs both flags.** `disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. In Claude Code the flag also blocks scheduled tasks ([CC automation](../vendors/claude-code/automation.md)); in Codex a scheduled `$name` prompt still runs ([Codex automation](../vendors/codex/automation.md)).
- **No placeholders or preprocessing.** `$ARGUMENTS`, `$N`, `${CLAUDE_SKILL_DIR}` and `` !`cmd` `` are Claude Code-only and stay literal elsewhere. Codex lists each skill's file path in the catalog.
- **OpenCode sees two copies** when both directories are populated, and requires unique names. `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1` stops it reading Claude Code skills ([OC][oc-skills]).
- **Cloud runs ignore user scope** in Claude Code. Commit skills that automation needs.
- **Script pre-approval** has no shared mechanism.
- **Versioning.** Neither lead defines skill versions. Use git tags or plugin versions; `metadata.version` is information only.

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| `user-invocable: false`, `when_to_use`, `skillOverrides` modes `name-only` and `user-invocable-only` | Claude Code | Codex has only enabled/disabled and reads only `description` |
| `argument-hint`, `arguments`, `$ARGUMENTS`/`$N`, `${CLAUDE_SKILL_DIR}` and other placeholders, `` !`cmd` ``, `@path`, `shell` | Claude Code | Codex does not preprocess the body |
| `allowed-tools`, `disallowed-tools`, `model`, `effort`, `hooks`, `paths` | Claude Code | No per-skill tool scope, model, hooks or glob activation in Codex |
| `context: fork`, `agent`, `background` | Claude Code | Codex skills cannot run themselves in a subagent |
| Nested `<subdir>/.claude/skills/`, auto-run of `verify`/`simplify`, `/skill-doctor`, `disableSkillShellExecution`, account-synced skills | Claude Code | Harness or account features with no Codex counterpart |
| `agents/openai.yaml` `interface.*` and `dependencies.tools`, `metadata.short-description` | Codex | UI metadata and MCP dependencies with no Claude Code counterpart |
| `$skill-installer`, `$skill-creator`, app-server skill APIs, `skill_approval` | Codex | Tooling, client protocol and an approval gate with no Claude Code counterpart |
| `skills.urls`, `skills.paths`, `permission.skill: ask` | OpenCode | No counterpart in either lead |

## Open questions

- No cross-harness data compares "pointer plus skill", "skill alone" and "content in `AGENTS.md`"; Vercel's study covers one framework with unnamed models.
- No Codex guidance on skills versus `AGENTS.md` versus hooks.
- Description voice (third person vs "Use when …") has no trigger-rate data per style.
- Emphatic rules: Anthropic's skill-creator and agentskills.io advise against them; Anthropic's own example and superpowers use them.
- No data on how catalog size affects trigger accuracy, or on whether user-invoked skills are followed more faithfully.
- How to detect implicit skill loads in Codex traces is undocumented; whether OpenCode deduplicates symlinked skills is unrecorded.
- Malicious-skill prevalence ranges from 0.52% to 46.8% flagged depending on method.

## Sources

Local:

- [Claude Code: skills](../vendors/claude-code/skills.md), [Codex: skills](../vendors/codex/skills.md), [OpenCode: skills](../vendors/opencode/skills.md)
- [Claude Code: automation](../vendors/claude-code/automation.md), [Codex: automation](../vendors/codex/automation.md), [OpenCode: commands](../vendors/opencode/commands.md)
- [Research notes: skills best practices](../research-notes/agent-harness-best-practices/skills.md)
- [Research notes: Claude Code extensions](../research-notes/agent-harness-configuration/claude-code-extensions.md), [Codex extensions](../research-notes/agent-harness-configuration/codex-extensions.md), [OpenCode](../research-notes/agent-harness-configuration/opencode.md)

External:

- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/plugin-evals
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md
- https://learn.chatgpt.com/docs/build-skills
- https://claude.com/blog/skills-explained
- https://developers.openai.com/blog/eval-skills
- https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md
- https://agentskills.io/specification
- https://agentskills.io/skill-creation/best-practices.md
- https://agentskills.io/skill-creation/optimizing-descriptions.md
- https://agentskills.io/skill-creation/evaluating-skills.md
- https://agentskills.io/skill-creation/using-scripts.md
- https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
- https://arxiv.org/html/2602.12670v1
- https://simonwillison.net/2025/Oct/16/claude-skills/
- https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md
- https://scottspence.com/posts/measuring-claude-code-skill-activation-with-sandboxed-evals
- https://arxiv.org/abs/2601.10338
- https://arxiv.org/abs/2602.06547
- https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub
- https://arxiv.org/abs/2603.16572
- https://owasp.github.io/www-project-agentic-skills-top-10/ast01

[cc-skills]: ../vendors/claude-code/skills.md
[cx-skills]: ../vendors/codex/skills.md
[oc-skills]: ../vendors/opencode/skills.md
