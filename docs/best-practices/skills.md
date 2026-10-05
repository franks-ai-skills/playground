# Skills: best practices

How to decide on, write, test, distribute and secure skills (`SKILL.md` packages under the Agent Skills standard) for Claude Code and Codex, with OpenCode where the sources cover it. This page also covers user-invoked skills, which replace custom slash commands in both leads. Terms follow [Skills](../concepts/skills.md) and [Commands](../concepts/commands.md): skill package, catalog, skill root, scope, explicit and implicit invocation, model-invocable flag, user-invoked skill, harness extension metadata. Research date: 2026-10-04.

Evidence labels: **[Vendor]** vendor documentation, vendor engineering post or vendor-maintained tool (Anthropic, OpenAI). **[Empirical]** study or measured data. **[Advisory]** standards body or open specification (agentskills.io, OWASP). **[Practitioner]** named engineer or company experience, including small self-run measurements. "Older" marks sources from 2025 or early 2026 where the harness or model generation has since moved on.

## Summary

- [Use a skill only where it adds what the model lacks](#1-use-a-skill-only-where-it-adds-what-the-model-lacks), and compare against a no-skill baseline before adopting it.
- [Write the description as the trigger condition](#2-write-the-description-as-the-trigger-condition): what it does, "Use when …" with user phrasing, a boundary; key words first; no workflow summary.
- [Keep `SKILL.md` lean and put gotchas first](#3-keep-skillmd-lean-and-put-gotchas-first): under 500 lines and ~5,000 tokens, only what the model would otherwise get wrong.
- [Disclose detail progressively with explicit triggers](#4-disclose-detail-progressively-with-explicit-triggers): one level of `references/`, each with "read X when Y".
- [Put deterministic logic in tested scripts](#6-put-deterministic-logic-in-tested-scripts) with non-interactive, structured, bounded output.
- [Make side-effecting skills user-invoked in both leads](#8-make-side-effecting-skills-user-invoked-in-both-leads), and read arguments from the message.
- [Write evals first and test triggering and behavior separately](#9-write-evals-first-and-test-triggering-and-behavior-separately), with a baseline arm, a pinned model and at least 3 runs.
- [Treat third-party skills as unreviewed dependencies](#security): read every file, pin, and run in isolation first.

## When to use it

A skill fits a recurring procedure or specialized knowledge that the model lacks, that is needed only sometimes, and where an occasional missed activation is acceptable ([research notes](../research-notes/agent-harness-best-practices/skills.md)).

| Need | Use | Source |
| --- | --- | --- |
| A fact or convention needed in every session | [Instruction file](./instructions.md) ([concept](../concepts/instructions.md)) | [Claude Code skills](https://code.claude.com/docs/en/skills) |
| A procedure or checklist you keep pasting into chat; an instruction-file section that "has grown into a procedure rather than a fact" | Skill | [Claude Code skills](https://code.claude.com/docs/en/skills) |
| A procedure with side effects or timing (deploy, commit, send a message) | User-invoked skill | [Claude Code skills](https://code.claude.com/docs/en/skills) |
| Knowledge the model lacks that it must always use (for example new framework APIs) | A compressed index or at least a one-line pointer in the instruction file; a skill alone is often not activated | [Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals) |
| A rule that must hold every time an event occurs | [Hook](../concepts/hooks.md) | [Claude Code skills](https://code.claude.com/docs/en/skills) |
| Work isolated from the conversation or running in the background | [Subagent](./subagents.md) ([concept](../concepts/subagents.md)); a subagent can use skills | [Claude Code skills](https://code.claude.com/docs/en/skills), [Anthropic blog](https://claude.com/blog/skills-explained) |
| Access to an external system or data | [MCP server](../concepts/mcp.md); a skill teaches what to do with it. "MCP connects to data; Skills teach Claude what to do with that data" | [Anthropic blog](https://claude.com/blog/skills-explained) |
| Deterministic, repeatable transformation | A script, usually bundled in the skill's `scripts/` | [Codex build skills](https://learn.chatgpt.com/docs/build-skills) |
| Two or more skills, or a skill plus a connector, shared across repos | [Plugin](../concepts/plugins.md) | [Codex build skills](https://learn.chatgpt.com/docs/build-skills) |
| A one-step request the model handles alone | Nothing; agents "typically only consult skills for tasks that require knowledge or capabilities beyond what they can handle alone" | [agentskills.io](https://agentskills.io/skill-creation/optimizing-descriptions.md) |

## Approaches

### Model-invoked skill

**What.** A skill with model invocation on (the default). Its name and description sit in the catalog; the model activates it when a task matches.

**When it fits.** Knowledge or a procedure the agent should apply without being asked.

**How.**
- Generalized: `SKILL.md` with `name` and `description`; activation depends entirely on the description ([concept: lifecycle](../concepts/skills.md#lifecycle)).
- Claude Code: activated through the Skill tool; catalog budget 1% of the context window; on overflow, descriptions of the least-invoked skills drop first ([concept](../concepts/skills.md#comparison)).
- Codex: chooses a skill when the task matches the description; catalog limited to 2% of the context window or 8,000 characters, descriptions shortened first, then skills omitted with a warning ([Codex build skills](https://learn.chatgpt.com/docs/build-skills), [concept](../concepts/skills.md#comparison)).
- OpenCode: the model calls the `skill` tool.

**Trade-offs.** The catalog entry is cheap: "long reference material costs almost nothing until you need it" ([Claude Code skills](https://code.claude.com/docs/en/skills)); each skill takes "a few dozen extra tokens", versus "tens of thousands of tokens" for GitHub's MCP server [Practitioner] (Simon Willison, older, 2025-10-16, [blog](https://simonwillison.net/2025/Oct/16/claude-skills/)). Implicit activation is unreliable. In Vercel's eval the skill was not invoked in 56% of cases ([Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)); a practitioner measured 50–55% activation without help ([Scott Spence](https://scottspence.com/posts/measuring-claude-code-skill-activation-with-sandboxed-evals)). SkillsBench observed Codex CLI agents "acknowledge Skills content but often implement solutions independently", while Claude Code showed the highest skill use ([SkillsBench](https://arxiv.org/html/2602.12670v1)).

### User-invoked skill (replaces custom commands)

**What.** A skill with model invocation off. Only the user starts it. Both leads replaced custom commands with this ([concept: commands](../concepts/commands.md)).

**When it fits.** Side effects or timing control: "You don't want Claude deciding to deploy because your code looks ready" ([Claude Code skills](https://code.claude.com/docs/en/skills)). Vercel recommends skills for "vertical, action-specific workflows that users explicitly trigger" ([Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)).

**How.**
- Generalized: set the model-invocable flag off in both leads in the same folder ([concept: invocation policy in both leads](../concepts/skills.md#invocation-policy-in-both-leads)).
- Claude Code: `disable-model-invocation: true` in frontmatter; invoke with `/name`. Migrate `.claude/commands/<name>.md` to `<name>/SKILL.md`.
- Codex: `agents/openai.yaml` with `policy.allow_implicit_invocation: false`; invoke with `$name` or `/skills`. Custom prompts in `~/.codex/prompts/` are deprecated ("Use skills for reusable instructions") ([concept: commands](../concepts/commands.md#portability)).
- OpenCode: a command file in `.opencode/commands/`; a same-named command wins the slash name over a skill.

**Trade-offs.** No catalog cost. In Claude Code the flag also blocks the skill from scheduled tasks and subagent preloading; in Codex a scheduled prompt naming `$name` still runs it. A skill meant to run from a Claude Code schedule must stay model-invocable ([concept](../concepts/skills.md#invocation-policy-in-both-leads)).

### Pointer in the instruction file plus skill

**What.** A one-line pointer in `AGENTS.md` tells the agent when to load a skill; or the knowledge goes into the instruction file as a compressed index instead of a skill.

**When it fits.** Knowledge whose omission causes silently wrong output.

**How.** Vercel's 8 KB pipe-delimited docs index in `AGENTS.md` scored 100%; skills reached at most 79% even with explicit instructions, against a 53% baseline without docs. Wording mattered: "You MUST invoke the skill" anchored the agent on the docs and missed project context; "Explore project first, then invoke skill" scored better ([Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)). See [Instructions: practice 4](./instructions.md#4-move-situational-guidance-out-of-the-always-loaded-file).

**Trade-offs.** The pointer or index costs instruction budget every session. Evidence is one framework, January 2026, models not published.

### Script-backed skill

**What.** A skill whose core is one or more scripts in `scripts/`, with the body explaining when and how to run them.

**When it fits.** Fragile, deterministic or repeatedly reinvented operations; when traces show the agent rewriting the same helper each run ([agentskills.io](https://agentskills.io/skill-creation/best-practices.md)).

**How.** See [practice 6](#6-put-deterministic-logic-in-tested-scripts). State whether to execute or read each script. Skills depend on filesystem access and command execution ([Simon Willison](https://simonwillison.net/2025/Oct/16/claude-skills/)). Pre-approval differs: Claude Code can pre-approve scripts through `allowed-tools`; Codex gates skill scripts through `approval_policy.granular.skill_approval`; there is no shared mechanism ([concept: body](../concepts/skills.md#body)).

**Trade-offs.** "Prefer instructions over scripts unless you need deterministic behavior or external tooling" ([Codex build skills](https://learn.chatgpt.com/docs/build-skills)). Scripts are code that must be maintained and reviewed. Only their output consumes context ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)).

### Skill that runs in its own context

**What.** A skill whose work happens in a subagent instead of the main conversation.

**When it fits.** Skills "with explicit instructions and concrete tasks, not guidelines" ([Claude Code skills](https://code.claude.com/docs/en/skills)).

**How.** Claude Code: `context: fork` runs the skill in a subagent that "doesn't see your conversation history — skill instructions must stand alone". Codex skills cannot run themselves in a subagent; portable skills instruct delegation in the body instead ([concept: dropped](../concepts/skills.md#dropped-from-the-generalization)). Naming the subagent in the skill is also how Codex gets delegation at all ([Subagents: practice 3](./subagents.md#3-write-the-description-as-a-trigger-and-name-the-agent-where-codex-needs-it)).

**Trade-offs.** `context: fork` is Claude-only.

### Distribution and scope

**What.** Where a skill lives: project (committed), user (personal), plugin (shared across repos), managed/admin (organization).

**When it fits.**
- Project scope for anything tied to a repo or needed by CI and cloud runs. Claude Code cloud sessions ignore `~/.claude/skills/` ([concept](../concepts/skills.md#directory-layout)).
- User scope for personal workflow.
- Plugin for skills shared across repos or teams, with versioned releases and namespacing ([Codex build skills](https://learn.chatgpt.com/docs/build-skills), [Claude Code skills](https://code.claude.com/docs/en/skills)).
- Managed for policy-like skills.

**How.** For Claude Code plus Codex, keep one canonical copy in `.agents/skills/<name>/` and symlink `.claude/skills/<name>` to it; both leads follow symlinked skill folders. Repeat at user scope with `~/.agents/skills/` and `~/.claude/skills/` ([concept: directory layout](../concepts/skills.md#directory-layout)). Codex needs a restart after installing ([openai/skills](https://github.com/openai/skills)).

**Trade-offs.** OpenCode reads both directories and may see the skill twice; `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1` stops it reading Claude Code skills. Codex's `$skill-installer` writes to the deprecated `$CODEX_HOME/skills`, invisible to Claude Code. The `openai/skills` repository is marked deprecated in favor of OpenAI's plugins repository ([openai/skills](https://github.com/openai/skills)).

## Practices

### 1. Use a skill only where it adds what the model lacks

**Practice.** Before writing a skill, run the task without it. Write the skill only for what the agent gets wrong or does not know, and keep it only if it beats the baseline.

**Why.** Skills help most where pretraining coverage is weak and least on tasks the model already does well; some hurt. "If the agent already handles the entire task well without the skill, the skill may not be adding value."

**How.** Run representative tasks without a skill, record failures, build three scenarios, measure the baseline, then write minimal instructions that close the gap ("evaluation-driven development").

**Evidence.**
- [Empirical] SkillsBench (Li et al., 2026-02-13; 86 tasks, Claude Code, Codex CLI, Gemini CLI, 7,308 trajectories): curated skills +16.2 pp on average, but +4.5 pp for software engineering vs +51.9 pp for healthcare; 16 of 84 tasks had negative deltas (one −39.3 pp). Claude Haiku 4.5 with skills (27.7%) matched Opus 4.5 without (22.0%) ([SkillsBench](https://arxiv.org/html/2602.12670v1)).
- [Advisory] "Would the agent get this wrong without this instruction? If the answer is no, cut it" ([agentskills.io best practices](https://agentskills.io/skill-creation/best-practices.md)).
- [Vendor] Evaluation-driven development ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)); "Start with evaluation" (older, 2025-10) ([Anthropic engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)).

### 2. Write the description as the trigger condition

**Practice.** The description is the only thing in the catalog. Write one sentence of *what* (concrete verbs and object types), then "Use when …" with phrases a user would say (including phrasings that do not name the domain), then one boundary clause ("Not for … — use X instead"). Put the key use case and trigger words first. Keep it to roughly 500 characters. Do not summarize the workflow. Use a spec-valid name equal to the directory name.

**Why.** "The body loads only after triggering", so usage guidance in the body does not affect the decision. Both leads truncate descriptions. Under-triggering is the documented default failure. When a description summarizes the workflow, agents may follow the description instead of the body: a description mentioning "code review between tasks" led agents to do one review where the body specified two.

**How.**
- Spec: `name` 1–64 characters, lowercase `a-z0-9` and single hyphens, equal to the directory name; `description` 1–1,024 characters. Good: "Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction." Poor: "Helps with PDFs."
- Claude Code example: "Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff." `description` plus `when_to_use` are truncated together at 1,536 characters; Codex reads only `description`, so put trigger phrases there.
- Anthropic forbids "anthropic" and "claude" in names and XML tags; prefers gerund names (`processing-pdfs`); avoid `helper`, `utils`, `tools`, `documents`, `data`.
- Fix false triggers by stating what the skill does not do, not by adding keywords from failed queries ("that's overfitting").
- For over-triggering in Claude Code: narrow the description, set `disable-model-invocation: true`, or set `skillOverrides` to `"name-only"`.

**Evidence.** Sources disagree on voice. Anthropic: "Always write in third person … inconsistent point-of-view can cause discovery problems." agentskills.io and superpowers: imperative "Use this skill when …" / "Use when …". Anthropic's own examples combine a third-person *what* with a "Use when …" *when*; all sources reject "I can …" and "You can …". Sources also differ on how "pushy" to be; that trade-off has to be measured with near-miss negatives ([practice 9](#9-write-evals-first-and-test-triggering-and-behavior-separately)).
- [Advisory] Spec and examples ([specification](https://agentskills.io/specification)); imperative phrasing, user intent, "Err on the side of being pushy", boundaries, overfitting ([optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions.md)).
- [Vendor] Third person, naming rules ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)); Claude "undertriggers", be "a little bit pushy" ([Anthropic skill-creator](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md)).
- [Vendor] "front-load the key use case and trigger words"; descriptions "may be shortened when many skills exist" ([Codex build skills](https://learn.chatgpt.com/docs/build-skills)); name and description "are the primary signals Codex uses" ([OpenAI eval blog](https://developers.openai.com/blog/eval-skills)); all "when to use" information belongs in the description ([OpenAI skill-creator](https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md)).
- [Vendor] Example, truncation, troubleshooting ([Claude Code skills](https://code.claude.com/docs/en/skills)).
- [Practitioner] "Description = When to Use, NOT What the Skill Does" and the two-reviews failure ([superpowers writing-skills](https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)).
- [Practitioner] Scott Spence (2026-02-08; ~250 sandboxed runs, Sonnet 4.5): when Claude activates a skill "it always picks correctly", so the problem is activation frequency; explicit keywords gave ~100% activation, conceptual phrasings ~0% ([Scott Spence](https://scottspence.com/posts/measuring-claude-code-skill-activation-with-sandboxed-evals)). Small sample, one author.

### 3. Keep `SKILL.md` lean and put gotchas first

**Practice.** Keep the body under 500 lines and about 5,000 tokens, much less for frequently loaded skills. Write only what the model would otherwise get wrong. Put the gotchas section and non-negotiable rules near the top. Write standing instructions, not one-time steps.

**Why.** "The context window is a public good." "Every line is a recurring token cost once the skill loads." In Claude Code only the first 5,000 tokens per skill (25,000 combined) are re-attached after compaction, and older skills may drop entirely. Measured data favors focused skills over comprehensive ones.

**How.** Ask of each paragraph: "Does this paragraph justify its token cost?" Do not explain what the model knows. Keep the gotchas in `SKILL.md`, not in a reference, because the agent "may not recognize the trigger" to open it. Do not add README.md or CHANGELOG.md to the skill. Avoid time-sensitive statements; put old patterns in a collapsed "Old patterns" section. Use consistent terminology.

**Evidence.**
- [Advisory] Under 500 lines, < 5,000 tokens; gotchas are "the highest-value content in many skills"; "Concise, stepwise guidance with a working example tends to outperform exhaustive documentation" ([specification](https://agentskills.io/specification), [best practices](https://agentskills.io/skill-creation/best-practices.md)).
- [Vendor] Public good, token-cost question, "Default assumption: Claude is already very smart" ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)); recurring cost, standing instructions, compaction limits ([Claude Code skills](https://code.claude.com/docs/en/skills)); no README/CHANGELOG, imperative form ([OpenAI skill-creator](https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md)).
- [Empirical] "Moderate-length Skills outperform comprehensive ones": detailed +18.8 pp vs comprehensive −2.9 pp ([SkillsBench](https://arxiv.org/html/2602.12670v1)).
- [Practitioner] superpowers: frequently loaded skills "<200 words total" ([superpowers](https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)).

### 4. Disclose detail progressively with explicit triggers

**Practice.** Move detail into `references/` files one level deep from `SKILL.md`. For each, say when to read it. Keep each fact in one place.

**Why.** Nested references cause partial reads ("Claude might use commands like `head -100`"). A generic "see references/" pointer gives the agent no reason to open the file.

**How.** "Read `references/api-errors.md` if the API returns a non-200 status code." Patterns: a high-level guide linking `FORMS.md`, `REFERENCE.md`, `EXAMPLES.md`; domain-split files (`reference/finance.md`) with a grep hint; conditional details ("For tracked changes: see REDLINING.md"). Add a table of contents to reference files over 100 lines. Name files descriptively; use forward slashes. Information "should live in either SKILL.md or references files, not both". Reference other skills by name, not by `@path`, which force-loads them. Use `assets/` for templates and data.

**Evidence.**
- [Vendor] One level deep, TOC over 100 lines, patterns, naming ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)); no duplication ([OpenAI skill-creator](https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md)).
- [Advisory] Explicit load conditions ([agentskills.io best practices](https://agentskills.io/skill-creation/best-practices.md)); directory roles ([specification](https://agentskills.io/specification)).
- [Practitioner] Cross-reference skills by name; `@path` links "force-load and burn context" ([superpowers](https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)).
- No controlled study of reference layout exists; Anthropic's observation is qualitative.

### 5. Match strictness to fragility

**Practice.** Per section, choose high freedom (heuristics) where many approaches work, medium (pseudocode or a parameterized script) where a preferred pattern exists, and low ("Run exactly this script … Do not modify the command") where an operation is fragile. Give one default with an escape hatch, not a menu.

**Why.** "Narrow bridge with cliffs" vs "open field": prescriptive steps where they are not needed railroad the agent; freedom where it is not safe breaks things.

**How.** Use a copyable progress checklist for multi-step workflows; validate → fix → repeat loops; for batch, destructive or high-stakes operations, plan → validate → execute with an intermediate file (for example `changes.json`) checked by a script. Use templates (strict or flexible default) and input/output example pairs. "Favor procedures over declarations."

**Evidence.**
- [Vendor] Degrees of freedom, checklist, feedback loops, plan-validate-execute, templates, defaults with escape hatch ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)); same model in [OpenAI skill-creator](https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md).
- [Advisory] "Provide defaults, not menus"; "Favor procedures over declarations" ([agentskills.io best practices](https://agentskills.io/skill-creation/best-practices.md)).

### 6. Put deterministic logic in tested scripts

**Practice.** Bundle code that the agent would otherwise rewrite each run, or that must behave the same every time, as scripts in `scripts/`. Design them for an agent caller.

**Why.** Pre-made scripts are "more reliable than generated code", save tokens and keep results consistent; only their output enters context.

**How.**
- No interactive prompts ("a hard requirement"). `--help` as the interface documentation.
- Structured output (JSON, CSV) on stdout, diagnostics on stderr, distinct exit codes.
- Errors that say what was expected: "Field 'signature_date' not found. Available fields: …". "Solve, don't defer": handle errors in the script. No unexplained constants.
- Idempotent; `--dry-run`; safe defaults such as `--confirm` for destructive actions.
- Predictable output size; harnesses truncate around 10–30K characters.
- Self-contained dependencies (PEP 723 with `uv run`, Deno `npm:` imports, Bun, `bundler/inline`); pin versions in one-off commands (`npx eslint@9.0.0`); list required packages.
- Paths relative to the skill root. Refer to MCP tools by fully qualified name.
- In the body, reference `--help` instead of documenting flags.

**Evidence.** [Vendor] Scripts guidance ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)); scripts when code is "repeatedly rewritten or deterministic reliability is needed" ([OpenAI skill-creator](https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md)). [Advisory] Interface rules ([agentskills.io using scripts](https://agentskills.io/skill-creation/using-scripts.md)). [Practitioner] Reference `--help` ([superpowers](https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)).

### 7. Explain the why before adding hard rules

**Practice.** By default, give the reason behind a rule. Add explicit prohibitions only where baseline runs show the agent rationalizing past the rule.

**Why.** Reasoned instructions generalize; shouted rules over-apply. But discipline skills that agents skip "under pressure" may need firm wording.

**How.** Write the rule with its reason. If evals still show violations, add a direct prohibition, and for discipline skills a list of the rationalizations observed. Test with every model you plan to use; what works for Opus "might need more detail for Haiku".

**Evidence.** Sources conflict:
- [Vendor] "If you find yourself writing ALWAYS or NEVER in all caps … that's a yellow flag" ([Anthropic skill-creator](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md)). [Advisory] "Reasoning-based instructions … work better than rigid directives" ([agentskills.io evaluating](https://agentskills.io/skill-creation/evaluating-skills.md)).
- [Vendor] Anthropic's own iteration example strengthens wording to "MUST filter"; test across models ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)).
- [Practitioner] superpowers prescribes prohibition, a rationalization table and a red-flags list, with "No nuance clauses" ([superpowers](https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)).
- [Empirical] "You MUST invoke the skill" backfired in Vercel's eval ([Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)).

### 8. Make side-effecting skills user-invoked in both leads

**Practice.** Turn off model invocation for skills that change external state or where timing matters, in both leads in the same folder. Keep knowledge skills model-invocable. Write the body to take inputs from the user's message.

**Why.** The model should not decide to deploy or commit. A user-invoked skill also leaves the catalog, freeing budget for model-invocable skills. Codex skills have no argument substitution.

**How.**
- Set `disable-model-invocation: true` (Claude Code) and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` (Codex) ([concept](../concepts/skills.md#invocation-policy-in-both-leads)).
- Write "The user names the issue number in their message; if missing, ask." Treat `$ARGUMENTS`, `$0`/`$1` and named arguments as Claude Code-only. Claude Code numbers arguments from `$0`, Codex prompts and OpenCode from `$1` ([concept: commands](../concepts/commands.md#portability)).
- Still write a good description: it appears in menus and in the Codex `/skills` list.
- Keep a skill model-invocable if a Claude Code schedule must run it.
- Claude Code-only: `user-invocable: false` hides background knowledge from the menu; it does not generalize.
- Before evaluating a new skill, invoke it explicitly once to surface hidden assumptions about naming, environment and execution order.

**Evidence.** [Vendor] `/deploy`, `/commit`, `/send-slack-message` examples; "Description not in context"; `allowed-tools` grants only for the invoking turn and "Doesn't restrict tools" ([Claude Code skills](https://code.claude.com/docs/en/skills)); `policy.allow_implicit_invocation` ([Codex build skills](https://learn.chatgpt.com/docs/build-skills)); explicit activation first ([OpenAI eval blog](https://developers.openai.com/blog/eval-skills)). [Empirical] User-triggered vertical workflows suit skills ([Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)). No data on whether user-invoked skills are followed more faithfully.

### 9. Write evals first and test triggering and behavior separately

**Practice.** Keep two test sets per skill and run both on every skill change and every model upgrade, with a pinned model and a baseline arm.

**Why.** A skill can fail by not triggering or by triggering and doing the wrong thing. Runs are noisy: a baseline varied 5 points between identical runs. "The most common first finding is a `Δ` near zero with the case's `tool_used: Skill` grader failing", meaning the description does not trigger on natural phrasing.

**How.**
- **Trigger set.** About 20 realistic prompts: 8–10 should trigger (including ones where "the connection isn't obvious"), 8–10 near-miss should-not-trigger cases that share keywords. Vary phrasing; include file paths, typos and personal context. Run each at least 3 times; pass if the trigger rate is above 0.5 (should) or below 0.5 (should not). Split ~60% train / ~40% validation, keep it fixed, pick the best iteration by validation score; "Five iterations is usually enough"; confirm with 5–10 fresh queries.
- **Behavior set.** Start with 2–3 cases (prompt, expected output, files, later assertions), grow to 10–20. Run each with and without the skill (or against the previous version) in fresh contexts. Grade with deterministic checks first, a model-graded rubric second, and human review of outputs and traces. Require concrete evidence for a PASS. Record tokens and duration; drop assertions that pass in both arms; high variance points to ambiguous instructions.
- **Codex.** Define success in four categories (outcome, process, style, efficiency); keep 10–20 prompts in a CSV covering explicit (`$skill`), implicit, contextual and at least one `should_trigger=false` case; capture traces with `codex exec --json --full-auto "<prompt>"` and check commands and files deterministically; add a rubric via a second `codex exec` with `--output-schema`; grow the CSV from real misses.
- **Claude Code.** `claude plugin eval` or the skill-creator plugin (see [Verification](#verification)). The two tools use different case formats; neither reads the other's files.
- Use a fresh session for each run: "a fresh session is crucial to avoid authoring-context bias". Use one instance to write the skill and a fresh one to use it, and watch for unexpected exploration paths, missed connections, overreliance on sections, and ignored files.

**Evidence.**
- [Advisory] Trigger and behavior eval method ([optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions.md), [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills.md)).
- [Vendor] Baseline in fresh sessions with `skillOverrides: "off"` ([Claude Code skills](https://code.claude.com/docs/en/skills)); `claude plugin eval` ([Claude Code plugin evals](https://code.claude.com/docs/en/plugin-evals)); with-skill and baseline subagents "in the same turn", 20-query description optimization ([Anthropic skill-creator](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md)); Claude A / Claude B and "At least three evaluations created", "Tested with Haiku, Sonnet, and Opus" ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)). That page still says there is no built-in way to run evaluations, which is outdated given `claude plugin eval`.
- [Vendor] Codex method; "start small, then layer in deeper checks only where they add real confidence" ([OpenAI eval blog](https://developers.openai.com/blog/eval-skills)).
- [Practitioner] RED-GREEN-REFACTOR: "NO SKILL WITHOUT A FAILING TEST FIRST" ([superpowers](https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md)); run-to-run variance ([Scott Spence](https://scottspence.com/posts/measuring-claude-code-skill-activation-with-sandboxed-evals)).

### 10. Ground skills in human domain knowledge

**Practice.** Source the content from real tasks and project artifacts: runbooks, review comments, incident reports, fix history. Use the model for structure and iteration, not as the knowledge source.

**Why.** Self-generated skills averaged −1.3 pp versus no skill: "models cannot reliably author the procedural knowledge they benefit from consuming". LLM-generated skills without domain context produce "vague, generic procedures".

**How.** Do the task by hand with the agent once, then extract what had to be corrected. Read execution traces, not just final outputs. When giving failures to an LLM to propose changes, tell it to "Generalize from feedback" and "Keep the skill lean".

**Evidence.** [Empirical] ([SkillsBench](https://arxiv.org/html/2602.12670v1)). [Advisory] ([agentskills.io best practices](https://agentskills.io/skill-creation/best-practices.md), [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills.md)).

### 11. Keep the library small and curated

**Practice.** Install only skills that earn their place. Design each as one coherent job. Prune never-invoked skills and turn rarely needed ones into user-invoked skills.

**Why.** Both catalogs are 1–2% of context and truncate silently. With Codex's 8,000-character floor, about 16 skills at 500 characters fill it (inference). Too narrow skills load together with conflicting instructions; too broad ones are "hard to activate precisely". Two to three skills per task helped far more than four or more.

**How.** Count catalog characters per harness. Use `/skill-doctor` (Claude Code) for context cost and never-invoked skills; `skillOverrides` (`off`, `name-only`) or Codex `[[skills.config]] enabled = false` to disable without deleting. Test triggering per harness, because budgets differ.

**Evidence.**
- [Vendor] Budgets and overflow ([Codex build skills](https://learn.chatgpt.com/docs/build-skills), [concept](../concepts/skills.md#comparison)); `/skill-doctor`, `skillOverrides` ([Claude Code skills](https://code.claude.com/docs/en/skills)); "Keep each skill focused on one job" ([Codex build skills](https://learn.chatgpt.com/docs/build-skills)).
- [Empirical] 2–3 skills per task +18.6 pp vs 4+ skills +5.9 pp ([SkillsBench](https://arxiv.org/html/2602.12670v1)). This measures skills per task, not catalog size.
- [Advisory] "Coherent units" ([agentskills.io best practices](https://agentskills.io/skill-creation/best-practices.md)).

### 12. Keep one canonical copy with portable frontmatter

**Practice.** Store each skill once and symlink it into the other harness's root. Use only portable frontmatter in shared skills, and keep harness-specific features in harness extension metadata.

**Why.** The leads share no skill directory. Claude-only frontmatter keys are ignored by Codex and OpenCode and cause hard errors on upload to claude.ai, the Skills API or `package_skill.py`.

**How.**
- Portable fields: `name`, `description` (non-empty, at most 1,024 characters, one line), `license`, `compatibility` (only with real environment requirements, ≤ 500 characters), `metadata` (string-to-string map).
- Codex-only settings go in `agents/openai.yaml`. Claude-only keys (`allowed-tools`, `context`, `hooks`, `paths`, `model`, …) stay out of skills meant to be portable.
- No `$ARGUMENTS`, `${CLAUDE_SKILL_DIR}` or `` !`cmd` `` in portable bodies.
- Commit skills that CI and cloud runs need; Claude Code cloud sessions do not read user scope.
- Versioning: no vendor defines skill versions. Use git tags or plugin versions, `metadata.version` as information only, and hash pinning for third-party skills.

**Evidence.** [Vendor] Concept page facts ([concept: portability](../concepts/skills.md#portability)); claude.ai-synced skills restricted to spec fields ([Claude Code skills](https://code.claude.com/docs/en/skills)). [Advisory] `metadata` and `compatibility` rules ([specification](https://agentskills.io/specification)). OpenAI's skill-creator says not to put a CHANGELOG in a skill ([OpenAI skill-creator](https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md)).

### 13. Move rules that must hold every time into hooks

**Practice.** If a skill contains a rule that must never be skipped, enforce it with a hook. In Claude Code a skill can carry hooks that apply only while it is active.

**Why.** Skills are context. After compaction only the most recent invocation of each skill is re-attached, and older skills "may drop entirely".

**How.** Claude Code: "move rules into hooks if they must hold every time"; skill-scoped `hooks` frontmatter. Codex has no skill-scoped hooks; use a regular hook ([concept: hooks](../concepts/hooks.md)).

**Evidence.** [Vendor] ([Claude Code skills](https://code.claude.com/docs/en/skills)).

## Anti-patterns

| Avoid | Do instead |
| --- | --- |
| "Helps with documents"; "I can help you …" | Third-person what, "Use when …" with user phrases, a boundary |
| Workflow steps in the description | Trigger conditions only; steps go in the body |
| "When to use" guidance only in the body | Put it in `description` |
| Adding keywords from each failed query to the description | Clarify the boundary; validate on a held-out set |
| Explaining what the model already knows; "comprehensive" documentation dumps | Gotchas and non-obvious steps only |
| Menus of equal options | One default with an escape hatch |
| Nested reference chains; "see references/" without a condition | One level deep, "read X when Y" |
| The same content in `SKILL.md` and a reference | One place |
| README.md or CHANGELOG.md inside the skill | Nothing; the skill folder holds only what the agent uses |
| Time-bound statements ("as of this year …") | An "Old patterns" section |
| Backslash paths; `@path` links to other skills | Forward slashes; reference skills by name |
| Scripts that prompt, dump huge output, or fail without guidance | Non-interactive, bounded, structured, descriptive errors |
| `$ARGUMENTS`, `${CLAUDE_SKILL_DIR}`, `` !`cmd` `` in a skill meant for both leads | Read inputs from the message; let the harness supply the path |
| A model-invocable `/deploy` or `/commit` skill | User-invoked in both leads |
| Many ALL-CAPS MUST/NEVER rules | Reasons first; prohibitions only where evals show rationalization |
| Skills generated by the model with no domain input | Content from real tasks and artifacts |
| Large, uncurated libraries | Small set; prune never-invoked skills |
| Judging triggering by eye or from one run | Labeled trigger set, 3+ runs, near-miss negatives |
| Installing third-party skills after reading only `SKILL.md` | Read every file; see [Security](#security) |
| Rules that must always hold, stated only in a skill | Hook |

## Security

**Threat: third-party skills are code and prompt injection with your privileges.** The natural-language body is a prompt-injection surface and `scripts/` is code. Measured prevalence varies widely by method:
- [Empirical] "Agent Skills in the Wild" (2026-01-15): 31,132 skills; 26.1% had at least one vulnerability (data exfiltration 13.3%, privilege escalation 11.8%); 5.2% showed high-severity patterns suggesting malicious intent ([arXiv 2601.10338](https://arxiv.org/abs/2601.10338)).
- [Empirical] Liu et al., "Do Not Mention This to the User" (rev. 2026-06-10): 98,380 skills; 157 confirmed malicious with 632 vulnerabilities; dominant patterns are credential theft via code execution and covert instructions in documentation files; all 157 removed after reporting ([arXiv 2602.06547](https://arxiv.org/abs/2602.06547)).
- [Empirical] Snyk ToxicSkills (2026-02-05): 3,984 skills from ClawHub and skills.sh; 13.4% with a critical issue; 2.9% of ClawHub skills fetch and execute remote content at runtime (`curl … | source`); attacks hidden mid-`SKILL.md` and base64 payloads piped to bash ([Snyk](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub)).
- [Empirical] Conflicting estimate, Holzbauer et al. (rev. 2026-06-01; 238,180 skills): scanners flagged up to 46.8%, but with repository context only 0.52% stayed suspicious; "isolated scanning significantly overestimates risk". Documents hijacking of skills hosted in abandoned GitHub repositories ([arXiv 2603.16572](https://arxiv.org/abs/2603.16572)).
- Summary: confirmed malicious skills are a small fraction of large registries; vulnerable or low-quality skills are common; open marketplaces carry more risk than curated ones.

**Threat: repository skills grant tools without trust.** In Claude Code "Workspace trust doesn't gate `allowed-tools` — a project skill applies even in `-p` runs in untrusted folders" ([Claude Code skills](https://code.claude.com/docs/en/skills)).

**Mitigations.**
- Install only from trusted sources; audit bundled code, dependencies and network connections ([Anthropic engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), older). "A skill's contents should not surprise the user in their intent if described" ([Anthropic skill-creator](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md)).
- Review checklist for a third-party skill:
  - Read every file, not just `SKILL.md`; the harness lists only name and description.
  - Search prose for hidden directives ("do not mention", "ignore previous"), instructions to fetch or run remote content, base64.
  - Inspect `scripts/` for network calls, credential or file access, `curl | sh`, package installs.
  - Check Claude Code `allowed-tools`, `hooks` and `` !`cmd` ``; check Codex `agents/openai.yaml` `dependencies.tools` (MCP).
  - Check that the source repository is maintained.
  - Pin by commit or hash; re-review on every update.
- [Advisory] OWASP Agentic Skills Top 10 (incubator, v0.0.0, March 2026), AST01 Malicious Skills (Critical; cites the "ClawHavoc campaign (Jan 2026): 1,184 malicious skills across 12 publisher accounts"): "Display skill publisher trust level, install count, and scan status"; "Never auto-execute 'Prerequisites' sections"; "Hash-pin installed skills" and alert on modifications ([OWASP AST01](https://owasp.github.io/www-project-agentic-skills-top-10/ast01)).
- Claude Code controls: review `allowed-tools` in unfamiliar repositories; `allowManagedPermissionRulesOnly` makes the harness ignore skill `allowed-tools`; `disableSkillShellExecution` turns off `` !`cmd` ``; claude.ai-synced skills never run injected commands (v2.1.228+) ([Claude Code skills](https://code.claude.com/docs/en/skills)).
- Codex control: `approval_policy.granular.skill_approval` gates skill scripts ([concept](../concepts/skills.md#body)).
- Evaluate untrusted skills in isolation. Running `claude plugin eval` on a plugin "is the same trust decision as `claude --plugin-dir`"; with hooks or MCP servers you did not write, "treat its scores as advisory unless you ran it in an isolated environment such as a container or CI runner" ([Claude Code plugin evals](https://code.claude.com/docs/en/plugin-evals)).
- For your own skills: least privilege in `allowed-tools`; `--dry-run` and explicit `--confirm` in destructive scripts; user-invoked only for side-effecting skills.
- [Practitioner] "We really need to figure out how best to sandbox these environments such that attacks such as prompt injections are limited to an acceptable amount of damage" (Simon Willison, older, 2025-10-16, [blog](https://simonwillison.net/2025/Oct/16/claude-skills/)). Run untrusted skills in a sandbox or container first.
- No vendor signing or provenance mechanism for skills was found in Claude Code or Codex docs.

## Verification

**Structure.**
- Claude Code: `claude plugin validate .claude/skills` (v2.1.233+) ([Claude Code skills](https://code.claude.com/docs/en/skills)).
- Spec: `skills-ref validate ./my-skill` ([specification](https://agentskills.io/specification)).
- Codex skill-creator: `scripts/quick_validate.py` ([OpenAI skill-creator](https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md)).

**Discovery and triggering.**
- Ask "What skills are available?" to confirm the skill is listed; invoke it with `/skill-name` (Claude Code) or `$name` (Codex) to separate content problems from trigger problems ([Claude Code skills](https://code.claude.com/docs/en/skills)).
- Headless trigger check: `claude -p "$query" --output-format json` piped to `jq` to find a `Skill` tool use ([agentskills.io](https://agentskills.io/skill-creation/optimizing-descriptions.md)); `codex exec --json` traces for Codex ([OpenAI eval blog](https://developers.openai.com/blog/eval-skills)). Which Codex JSONL event marks an implicit skill load is not documented.
- `claude plugin eval` (v2.1.269+, plugins and skills-directory plugins): one case directory per prompt with `prompt.md` and `graders/*.md`; graders `regex`, `tool_used`, `tool_order`, `file_exists`, `llm` (PASS in ≥ 2 of 3), `baseline`. Trigger check: `tool_used` with `tool: Skill` and `input_match` on the skill name. Must-not-trigger: `min: 0`, `max: 0`, `arm: both`. Three runs per arm by default; reports `Δ` between with-plugin and no-plugin arms; `--threshold` (default 1.0) exits 1 below it for CI; pin `--model`; runs use a temporary home with no personal `CLAUDE.md`, skills or MCP ([Claude Code plugin evals](https://code.claude.com/docs/en/plugin-evals)).
- Anthropic skill-creator plugin: cases in `evals/evals.json`, isolated subagents, assertion grading, with/without comparison, blind A/B between versions, HTML report ([Claude Code skills](https://code.claude.com/docs/en/skills)).

**In real use.**
- `/skill-doctor` (v2.1.252+): per-skill context cost, invocation frequency, never-invoked skills ([Claude Code skills](https://code.claude.com/docs/en/skills)).
- [Practitioner] A `UserPromptSubmit` "forced-eval" hook that makes the model state YES/NO per skill reached 100% activation on standard prompts and 75% accuracy with 100% true negatives on hard prompts, at 10.7 s average latency vs 8.7 s without a hook (Run 1); an LLM pre-classifier hook had 80% false positives ([Scott Spence](https://scottspence.com/posts/measuring-claude-code-skill-activation-with-sandboxed-evals)). One author, small sample.
- Ask the team whether the skill activates when expected ([Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)).

**Minimal portable test kit per skill** (synthesis in the [research notes](../research-notes/agent-harness-best-practices/skills.md)): `evals/trigger_queries.json` (20 labeled prompts with near-misses), `evals/evals.json` (behavior cases with assertions), a runner per harness, at least 3 runs each, a pinned model, and a baseline arm. Re-run on every skill change and model upgrade.

## Checklist

- [ ] A no-skill baseline showed the skill is needed; the eval set exists.
- [ ] `name` is spec-valid and equals the directory name.
- [ ] `description` states what, "Use when …" with user phrasing, and a boundary; key words first; ~500 characters or less; no workflow steps.
- [ ] `SKILL.md` is under 500 lines; gotchas are near the top; nothing the model already knows.
- [ ] References are one level deep, each with a load condition; no duplicated content.
- [ ] Scripts are non-interactive, have `--help`, structured output, bounded size, clear errors, `--dry-run` for destructive actions.
- [ ] Side-effecting skills have `disable-model-invocation: true` and `policy.allow_implicit_invocation: false`.
- [ ] Shared skills use only portable frontmatter and no argument placeholders; one canonical copy is symlinked into the other root.
- [ ] Skills needed by CI or cloud runs are committed, not in user scope.
- [ ] Trigger evals (with near-misses) and behavior evals pass with a pinned model across 3+ runs, in each harness.
- [ ] Catalog size fits both budgets; never-invoked skills are pruned.
- [ ] Every third-party skill was read in full, is pinned, and `allowed-tools` was reviewed.
- [ ] Rules that must always hold are hooks, not skill text.

## Open questions

- No cross-harness data compares "pointer in `AGENTS.md` plus skill", "skill alone" and "content in `AGENTS.md`"; Vercel's study is one framework with unnamed models.
- No Codex guidance on skills versus `AGENTS.md` versus hooks; Codex docs cover skills versus plugins only.
- Description voice: Anthropic requires third person, agentskills.io and superpowers recommend "Use when …"; no trigger-rate data per style exists. No data on `metadata.short-description` (Codex) or `when_to_use` (Claude Code), or on gerund versus noun names.
- Emphatic rules: Anthropic's skill-creator and agentskills.io advise against them; Anthropic's best-practices example and superpowers use them; Vercel saw "You MUST" backfire.
- No controlled study of reference layout; no data on how Codex reads long reference files.
- No vendor guidance on argument conventions for Codex skills beyond "text after `$name` is part of the message"; no data on whether user-invoked skills are followed more faithfully.
- How to detect implicit skill loads in Codex traces is undocumented. No guidance on sample sizes beyond "3 runs" and the 0.5 threshold.
- No data on how catalog size affects trigger accuracy in either lead; no vendor guidance on skill versioning or deprecation.
- Whether OpenCode deduplicates symlinked duplicate skills is unrecorded.
- Prevalence of malicious skills ranges from 0.52% to 46.8% flagged depending on method; numbers are not comparable. No vendor signing or provenance mechanism exists.
- Not read in the research: AEVAL (arXiv 2607.16345), Phil Schmid's skill-testing guide, OWASP AST02–AST10.

## Sources

Local:
- [Skills concept](../concepts/skills.md), [Commands concept](../concepts/commands.md), [Concepts overview](../concepts/README.md)
- [Research notes: skills](../research-notes/agent-harness-best-practices/skills.md)

External:
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/plugin-evals
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- https://claude.com/blog/skills-explained
- https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md
- https://learn.chatgpt.com/docs/build-skills
- https://developers.openai.com/blog/eval-skills
- https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md
- https://github.com/openai/skills
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
