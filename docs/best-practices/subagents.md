# Subagents: best practices

When to delegate to subagents, how to design subagent definitions, which orchestration patterns work, how to write delegation messages and merge results, and how to observe and evaluate multi-agent runs. Claude Code and Codex are equal leads; OpenCode is noted where the sources cover it. Terms follow [Subagents](../concepts/subagents.md): subagent definition, built-in types, subagent instance, result, spawn tool, resume. Research date: 2026-10-04.

Evidence labels: **[Vendor]** vendor documentation or vendor engineering post. **[Empirical]** study or measured data, including vendor-published measurements. **[Advisory]** standards body or industry advisory (none of the subagent sources fall in this class). **[Practitioner]** experience report without controlled data. "Older" marks sources from 2024 to mid-2025. They predate named definitions, background subagents, agent teams and Codex multi-agent on by default, so read them as principles, not product guidance.

## Summary

- [Default to one agent and delegate only for a clear reason](#1-default-to-one-agent-and-delegate-only-for-a-clear-reason): verbose output that needs only a summary, independent read-only branches, a fresh context for review, or a different capability scope or model.
- [Keep parallel work read-only and isolate parallel writers](#2-keep-parallel-work-read-only-and-isolate-parallel-writers) in their own worktrees with disjoint file sets.
- [Write the description as a trigger, and name the agent where Codex needs it](#3-write-the-description-as-a-trigger-and-name-the-agent-where-codex-needs-it): Codex does not delegate on descriptions alone.
- [Scope capabilities to the job and enforce read-only per harness](#4-scope-capabilities-to-the-job-and-enforce-read-only-per-harness): a Claude Code `tools` allowlist works; a Codex agent file's `sandbox_mode` can be overridden by the parent.
- [Make the delegation message self-contained](#6-make-the-delegation-message-self-contained) and [define an output contract](#7-define-an-output-contract-and-write-large-results-to-disk): the subagent does not see the conversation.
- [Verify results and treat them as untrusted data](#8-verify-results-and-treat-them-as-untrusted-data); have a fresh-context reviewer [report only correctness gaps](#9-review-in-a-fresh-context-and-limit-findings-to-correctness).
- [Measure delegation against a single-agent baseline](#13-measure-delegation-against-a-single-agent-baseline) on success, total tokens and wall time.

## When to use it

Subagents help on read-heavy, parallelizable or verbose work that only needs a summary. They hurt on sequential, tightly coupled work and on parallel writes. They always cost more tokens: Anthropic measured about 15 times the tokens of a chat for its multi-agent research system ([Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), older, 2025).

| Situation | Use | Source |
| --- | --- | --- |
| Exploration, test runs, log triage or research whose output is verbose and needed only as a summary | Subagent | [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) |
| Independent read-only questions that can run in parallel | Several subagents, fan-out/fan-in | Same |
| Review or verification that must not be biased by the code just written | Subagent with a fresh context | [Claude Code best practices](https://code.claude.com/docs/en/best-practices) |
| A task that needs other tools, a narrower scope, an MCP server or another model | Custom subagent definition | [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) |
| Frequent back-and-forth, phases that share a lot of context (plan, implement, test), quick targeted changes, latency-sensitive work | Main conversation | [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) |
| Sequential tasks, same-file edits, many dependencies | Single session | [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams) |
| Reusable knowledge or a procedure that should run in the main context | [Skill](./skills.md) ([concept](../concepts/skills.md)); a subagent can preload or use skills | [Anthropic blog](https://claude.com/blog/skills-explained) |
| Facts every session needs, including when to delegate | [Instruction file](./instructions.md) ([concept](../concepts/instructions.md)) | [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) |
| A check that must run every time (tests before stop, blocking writes) | [Hook](../concepts/hooks.md) or [permission rule](../concepts/permissions-and-sandbox.md) | [Claude Code best practices](https://code.claude.com/docs/en/best-practices) |
| Many independent per-file changes, unattended | [Automation](../concepts/automation.md): headless runs in a loop, or Claude Code `/batch` | [Claude Code best practices](https://code.claude.com/docs/en/best-practices) |

## Approaches

### Built-in types, delegated ad hoc

**What.** Delegation to the harness's built-in general-purpose or read-only exploration type, with the task described in the delegation message.

**When it fits.** Most delegation. Both leads ship a general worker and a read-only explorer.

**How.**
- Claude Code: Explore (read-only), Plan (read-only), general-purpose and others; Claude delegates automatically by description or on request ("use subagents to investigate X") ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Claude Code best practices](https://code.claude.com/docs/en/best-practices)).
- Codex: `default`, `worker` ("implementation and fixes"), `explorer` ("read-heavy exploration"); spawned only on a direct request ("spawn two agents") or an `AGENTS.md`/skill instruction ([Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)).
- OpenCode: General, Explore (read-only), Scout (experimental) ([OpenCode agents](https://opencode.ai/docs/agents/)).

**Trade-offs.** No files to maintain. Scope and model are whatever the built-in uses.

### Custom specialist definitions

**What.** A named definition with its own description, instructions, capability scope, model and MCP servers ([concept: entities](../concepts/subagents.md#entities)).

**When it fits.** When the specialist changes something the built-ins cannot: a stricter tool scope, a different model or effort, a scoped MCP server, or a review lens with its own checklist.

**How.** No definition file is shared between harnesses; keep one file per harness, generated from one source or synced by hand ([concept: portability](../concepts/subagents.md#portability)). `name` and `description` carry over unchanged; the instructions move between the Markdown body and `developer_instructions`. Example pair, adapted from the vendor examples ([Claude Code reference](../vendors/claude-code/subagents.md#example), [Codex reference](../vendors/codex/subagents.md#example)):

```markdown
---
# .claude/agents/reviewer.md
name: reviewer
description: Reviews a diff for correctness, security and missing tests. Use after code changes, before a task is reported done.
tools: Read, Glob, Grep
model: inherit
---
Review the diff named in the task. Report only gaps that affect correctness or the stated requirements.
Return a list of findings, each with file:line, severity and a suggested fix. Mark anything you did not verify as "unverified".
```

```toml
# .codex/agents/reviewer.toml
name = "reviewer"
description = "Reviews a diff for correctness, security and missing tests. Use after code changes, before a task is reported done."
model_reasoning_effort = "high"
sandbox_mode = "read-only"   # may not apply: the parent sandbox wins
developer_instructions = """
Review the diff named in the task. Report only gaps that affect correctness or the stated requirements.
Return a list of findings, each with file:line, severity and a suggested fix. Mark anything you did not verify as "unverified".
"""
```

OpenCode takes the name from the file path, so name the file after the agent.

**Trade-offs.** Each definition's description costs context every session; Claude Code warns above 15,000 tokens combined. A specialist that differs from a built-in only in persona adds routing ambiguity without changing capability ([practice 10](#10-keep-the-catalog-small-and-specialists-distinct)). Codex states that the agent file format "may evolve".

### Orchestrator-worker: fan-out, fan-in

**What.** The main session splits a task into independent read-only parts, spawns one worker per part in parallel, waits, and merges the results.

**When it fits.** Breadth-first questions that pursue several independent directions. Multi-file reviews by dimension.

**How.**
- Claude Code: "Research the authentication, database, and API modules in parallel using separate subagents"; up to 20 concurrent subagents by default (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`) ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents)).
- Codex: one agent per review dimension (security, code quality, tests, maintainability), consolidated by category; Codex "waits until all requested results are available" and returns one consolidated response ([Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)).
- Scale effort to the question. Anthropic's lead prompt: "Simple fact-finding requires just 1 agent with 3-10 tool calls, direct comparisons might need 2-4 subagents with 10-15 calls each"; the lead "spins up 3-5 subagents in parallel" ([Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), older, 2025).

**Trade-offs.** [Empirical] Centralized coordination amplified errors 4.4 times versus 17.2 times for independent agents; "orchestrators function as validation checkpoints" ([Google Research](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)). Synchronous fan-in blocks on the slowest worker ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)). Workers re-explore overlapping parts of the repository; a persistent search sub-agent cut per-episode GPU energy by 11–30% while preserving task performance ([arXiv 2605.27787](https://arxiv.org/abs/2605.27787)).

### Chain and explore-plan-implement

**What.** Specialists in sequence, with the main agent passing relevant context from one to the next.

**When it fits.** Work with distinct phases where each phase's output is the next phase's input.

**How.** "Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them" ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents)). Explore, plan, implement, commit; skip planning "if you could describe the diff in one sentence"; for larger features, interview the user, write `SPEC.md`, then implement in a fresh session ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).

**Trade-offs.** Each hand-off is a lossy summary. Phases that share a lot of context are better kept in the main conversation.

### Writer plus independent reviewer or verifier

**What.** One agent writes; a separate agent with a fresh context reviews the diff or tries to refute the result.

**When it fits.** Before treating a task as done; for code review; for tests written by one agent and code by another.

**How.** "Before treating a task as done, have a subagent review the diff in a fresh context and report gaps"; a verification subagent has "a fresh model try to refute the result, so the agent doing the work isn't the one grading it" ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)). Split review by lens (security, performance, test coverage), because "a single reviewer tends to gravitate toward one type of issue at a time". For debugging, run competing hypotheses that try to disprove each other, because sequential investigation "suffers from anchoring" ([Claude Code agent teams](https://code.claude.com/docs/en/agent-teams)).

**Trade-offs.** "A reviewer prompted to find gaps will usually report some, even when the work is sound"; chasing every finding leads to over-engineering ([practice 9](#9-review-in-a-fresh-context-and-limit-findings-to-correctness)).

### Parallel writers, per-item fan-out and best-of-N

**What.** Several agents that write code at the same time, each in its own workspace.

**When it fits.** Many independent per-item changes, or several attempts at one task when an automatic judge (tests, a benchmark script) picks the winner.

**How.**
- Claude Code: `isolation: worktree` on a definition runs the subagent in its own git worktree, auto-cleaned if unchanged; `/batch <instruction>` splits a change across 5 to 30 subagents, each in its own worktree; for scripted fan-out, loop `claude -p` per file with `--allowedTools` and `--permission-mode dontAsk`, test on 2–3 files first, then run on all ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Claude Code best practices](https://code.claude.com/docs/en/best-practices)).
- Codex: worktrees are per session, not per subagent (desktop parallel chats in worktrees; CLI `--worktree`) ([Codex worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees.md)); `codex cloud exec --attempts 1-4` runs best-of-N ([Codex CLI reference](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)).
- Generalized: give each writer a disjoint file set, then merge sequentially in the orchestrator with tests between merges.

**Trade-offs.** Parallel writers are the least reliable pattern: "Actions carry implicit decisions, and conflicting decisions carry bad results" ([Cognition 2025](https://cognition.com/blog/dont-build-multi-agents), older), and Cognition still reported in 2026 that parallel writers fragment the code ([Cognition 2026](https://cognition.com/blog/multi-agents-working)). "Two teammates editing the same file leads to overwrites" ([Claude Code agent teams](https://code.claude.com/docs/en/agent-teams)). Best-of-N without an automatic judge moves the selection burden to the user or to an LLM judge with its own bias. No data shows how often `/batch` or best-of-N improve outcomes.

### Agent teams (Claude Code only)

**What.** An experimental Claude Code feature: a lead, teammates, a shared task list and a mailbox. Dropped from the generalization because Codex's message board is under development and off ([concept: dropped](../concepts/subagents.md#dropped-from-the-generalization)).

**When it fits.** "Research, review, and new feature work"; "for routine tasks, a single session is more cost-effective" ([Claude Code agent teams](https://code.claude.com/docs/en/agent-teams)).

**How.** "Start with 3-5 teammates"; "Three focused teammates often outperform five scattered ones"; "5-6 tasks per teammate". Teammates do not inherit the lead's history, so put task details in the spawn prompt. Define a role once (for example security-reviewer) and reuse it as a subagent and as a teammate; `tools` from the definition applies. Teammates start with the lead's permission mode. Teammates spawned in plan mode stay read-only until their plan is approved, but the lead approves automatically, without the user.

**Trade-offs.** "Significantly more tokens than a single session". Known failures: the lead implements tasks itself instead of waiting, or decides the team is finished early; task status lags. No nested teams.

## Practices

### 1. Default to one agent and delegate only for a clear reason

**Practice.** Start with a single agent. Add a subagent when one of four conditions holds: (1) verbose output that needs only a summary, (2) independent read-only branches that can run in parallel, (3) a need for a fresh, unbiased context, (4) a need for a different capability scope or model. Do not delegate sequential implementation steps that share state.

**Why.** Benefit depends on how decomposable the task is, and coding is usually less decomposable than research. Every subagent spends its own tokens.

**How.** Scope investigations narrowly or delegate them, to avoid the "infinite exploration" anti-pattern (an unscoped investigation reading hundreds of files). Estimate cost as roughly N full explorations plus the merged summaries for a fan-out of N.

**Evidence.**
- [Vendor] Use and avoid lists ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents)); "read-heavy tasks such as exploration, tests, triage, and summarization"; subagent workflows "consume more tokens than comparable single-agent runs" ([Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)); context is the main constraint ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).
- [Vendor] Older: "maximize a single agent's capabilities first"; split on complex logic or overlapping tools, not tool count ([OpenAI practical guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf), 2025); "find the simplest solution possible" ([Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), 2024).
- [Empirical] Older: multi-agent (Opus 4 lead, Sonnet 4 workers) beat single-agent Opus 4 by 90.2% on Anthropic's internal research eval; ~4× tokens for agents and ~15× for multi-agent versus chat; token usage alone explained 80% of BrowseComp variance; "most coding tasks involve fewer truly parallelizable tasks than research" ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system), 2025).
- [Empirical] Google Research (2026-01-28; arXiv 2512.08296): +80.9% on parallelizable Finance-Agent, −39% to −70% on sequential PlanCraft across all multi-agent variants ([blog](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/), [arXiv](https://arxiv.org/abs/2512.08296)). The blog and the later arXiv version report different study sizes and fit (180 vs 260 configurations; R² 0.513 vs cross-validated 0.373); both report 87% correct architecture choice on unseen cases.
- [Empirical] MAST (UC Berkeley, v3 2025-10-26): 1,600+ traces from 7 frameworks; gains over single-agent baselines "are often minimal" ([arXiv 2503.13657](https://arxiv.org/abs/2503.13657)). Yin et al. (Nov 2025): the multi-agent framework had the longest trajectories and most corrections due to coordination overhead ([arXiv 2511.00872](https://arxiv.org/abs/2511.00872)).
- [Practitioner] Cognition: older (2025-06-12) "Don't build multi-agents"; 2026 update uses reviewer loops, "smart friend" escalation, read-only subagents and manager/child agents, but not parallel writers ([2025](https://cognition.com/blog/dont-build-multi-agents), [2026](https://cognition.com/blog/multi-agents-working)).
- No controlled study compares Claude Code or Codex subagent use with single-agent runs on a coding benchmark with token accounting.

### 2. Keep parallel work read-only and isolate parallel writers

**Practice.** Run parallel subagents read-only. Keep one writer at a time in the main worktree. When parallel writes are needed, give each writer its own worktree and its own files, and merge sequentially with tests between merges.

**Why.** Agents editing at the same time "can create conflicts and increase coordination overhead". Divergent implicit decisions fragment the code.

**How.** Claude Code: `isolation: worktree` or `/batch`. Codex: separate worktree sessions or cloud attempts, since subagent-level worktrees do not exist. Agent teams: "each teammate owns a different set of files".

**Evidence.** [Vendor] ([Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Codex worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees.md), [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams)). [Practitioner] Flappy Bird example: one subagent built a Super Mario style background, another a mismatched bird ([Cognition 2025](https://cognition.com/blog/dont-build-multi-agents), older); parallel writers still fail ([Cognition 2026](https://cognition.com/blog/multi-agents-working)).

### 3. Write the description as a trigger, and name the agent where Codex needs it

**Practice.** Write "<what it does>. Use when <trigger>." Keep it short. For Codex, also name the agent in `AGENTS.md` or in the skill that should trigger it ("use the `reviewer` agent after edits").

**Why.** Claude Code uses the description to decide when to delegate, and descriptions occupy context. Codex "spawn[s] agents after a direct request or applicable project or skill instruction", so the description alone does not trigger delegation.

**How.** Claude Code example: "Scans files and suggests improvements for readability, performance, and best practices. Use after writing or modifying code." "Use proactively" encourages automatic delegation in Claude Code but not in Codex. Keep descriptions non-overlapping ([practice 10](#10-keep-the-catalog-small-and-specialists-distinct)).

**Evidence.** [Vendor] ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Codex reference](../vendors/codex/subagents.md#when-codex-spawns)). OpenCode lists only subagents allowed by `permission.task` in the Task tool description, so denied ones cost no context ([OpenCode agents](https://opencode.ai/docs/agents/)).

### 4. Scope capabilities to the job and enforce read-only per harness

**Practice.** Give each definition the narrowest capability scope that works: read-only for explorers and reviewers, MCP servers only on the agent that needs them. Enforce read-only with a mechanism that the harness actually honors.

**Why.** Claude Code enforces a `tools` allowlist per definition. Codex has no tool allowlist, and subagents inherit the parent sandbox policy and live overrides (`/permissions`, `--yolo`) "even if the selected custom agent file sets different defaults".

**How.**
- Claude Code: `tools` allowlist (for example `Read, Grep, Glob`) or `disallowedTools` (for example `Write, Edit`); a subagent-scoped `PreToolUse` hook for conditional rules (example: a `db-reader` agent whose Bash calls go through `validate-readonly-query.sh`, exit code 2 blocks); `mcpServers` on one agent (example: Playwright only for a `browser-tester`) keeps those tool descriptions out of the main context.
- Codex: do not rely on the agent file's `sandbox_mode`. Run the parent in a read-only sandbox for review runs, add a `PreToolUse` hook on the subagent's agent type, or review in a separate read-only session. Scope MCP with `mcp_servers` and skills with `skills.config`.
- Agent teams: per-teammate permission modes cannot be set at spawn time; the definition's `tools` does apply.
- Older: split agents when tools overlap and better names do not fix selection; "poka-yoke" tools (absolute paths removed a class of errors).

**Evidence.** [Vendor] ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams), [concept: portability](../concepts/subagents.md#portability)). Older [Vendor] ([OpenAI practical guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf), 2025; [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), 2024).

### 5. Match model and effort to the job

**Practice.** Use a cheap, fast model and low effort for narrow, repeatable work whose failure is easy to detect (search, listing, summarizing logs). Keep reviewers and planners on a strong model and high effort.

**Why.** A missed bug costs more than the tokens saved. Model choice was one of three factors explaining 95% of BrowseComp variance in Anthropic's research system.

**How.**
- Claude Code: Haiku for exploration and to "control costs"; Sonnet for balance; Opus for complex analysis; `inherit` to match the main model. Resolution: spawn parameter > definition `model` > `CLAUDE_CODE_SUBAGENT_MODEL` > main model.
- Codex: a large model for "demanding, ambiguous work requiring planning and validation", a small fast model for "fast, narrowly scoped tasks with clear, repeatable work"; `model_reasoning_effort` `high` for tracing logic and edge cases, `low` for straightforward work. The page names current models (as of Oct 2026 "GPT-6.1 Sol" and "GPT-6 Luna"); names change.
- Precedence is reversed between leads: in Codex the definition beats the spawn value ([concept: portability](../concepts/subagents.md#portability)). Default subagent model: `CLAUDE_CODE_SUBAGENT_MODEL` / `agents.default_subagent_model`.

**Evidence.** [Vendor] ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)). [Empirical] Older: strong lead with cheaper workers ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system), 2025). [Practitioner] The reverse pairing also works: a weaker primary calls a stronger "smart friend" model for hard sub-problems; the open problem is getting the weaker model to recognize when to escalate ([Cognition 2026](https://cognition.com/blog/multi-agents-working)). No study compares per-agent model routing on coding quality or total cost.

### 6. Make the delegation message self-contained

**Practice.** Write each delegation message so a newcomer could do the task: goal and why; what is already known or decided (files, constraints, rejected approaches); scope boundaries (what not to touch, which files belong to this agent); tools or sources to prefer; stop condition and effort budget; output contract; where to write large artifacts.

**Why.** A non-fork Claude Code subagent gets its own system prompt, the delegation message, `CLAUDE.md` (not for Explore and Plan), git status, preloaded skills and the sibling roster. It does not get the conversation history, files already read, or skills already invoked. Agent-team teammates also do not inherit the lead's history.

**How.** Example from the agent-teams docs: name the directory, the focus areas, a relevant architecture fact ("JWT tokens stored in httpOnly cookies") and the output format. In chains, pass the relevant context from one subagent to the next. Keep agents on the same page with shared plan or todo files.

**Evidence.** [Vendor] ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams)). [Vendor] Older: each delegation needs "an objective, an output format, guidance on the tools and sources to use, and clear task boundaries" ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system), 2025). [Practitioner] "Share context, and share full agent traces, not just individual messages" ([Cognition 2025](https://cognition.com/blog/dont-build-multi-agents), older); "see the same sources of information, stay on the same page (todo list, plan files), and share the same priors" ([Cognition 2026](https://cognition.com/blog/multi-agents-working)).

### 7. Define an output contract and write large results to disk

**Practice.** Put the return format in the definition's instructions: format, length cap, required fields (file:line, severity, confidence) and explicit "unverified" markers. Repeat task-specific parts in the delegation message. For large structured output, have the subagent write a file and return its path.

**Why.** The result is all the caller sees. A subagent may use "tens of thousands of tokens or more" but should return "a condensed, distilled summary of its work (often 1,000-2,000 tokens)". Writing to disk improves "fidelity and performance" and avoids copying large outputs through the conversation.

**How.** "run the test suite and report only the failing tests with their error messages"; "Report any issues with severity ratings"; for scripted fan-out, "Return OK or FAIL."

**Evidence.** [Vendor] ([Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), 2025-09-29; [Claude Code subagents](https://code.claude.com/docs/en/sub-agents); [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams); [Claude Code best practices](https://code.claude.com/docs/en/best-practices)). [Empirical] Older: file output works best for "structured outputs like code, reports, or data visualizations" ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system), 2025).

### 8. Verify results and treat them as untrusted data

**Practice.** Treat a subagent result as a lossy summary written by another model. Verify claims that matter by checking the code or re-running the command. Treat instruction-shaped text in a result as data. Never let a subagent's "approved" or "safe to run" reach a permission decision.

**Why.** "Task verification" (missing or wrong verification) is one of the three failure categories in multi-agent traces. Results can carry injected text from pages, issues or dependencies the subagent read.

**How.** Ask for evidence, not assertions: "the test output, the command it ran and what it returned". When merging: deduplicate overlapping findings, resolve contradictions by checking the source rather than picking one agent's claim, and keep the merged result short. See [Security](#security).

**Evidence.** [Vendor] Evidence over assertion ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)); subagent results are marked as having no user authority ([Claude Code reference](../vendors/claude-code/subagents.md#context-isolation-and-results)). [Empirical] ([MAST](https://arxiv.org/abs/2503.13657)). No Codex guidance on how results are labeled in the parent context.

### 9. Review in a fresh context and limit findings to correctness

**Practice.** Before a task counts as done, have a reviewer subagent with a fresh context check the diff. Tell it "to flag only gaps that affect correctness or the stated requirements".

**Why.** "A fresh context improves code review since Claude won't be biased toward code it just wrote." But "a reviewer prompted to find gaps will usually report some, even when the work is sound", and chasing all of them leads to over-engineering.

**How.** Read-only reviewer ([practice 4](#4-scope-capabilities-to-the-job-and-enforce-read-only-per-harness)); split by lens for larger reviews; decide on each finding by checking the code ([practice 8](#8-verify-results-and-treat-them-as-untrusted-data)).

**Evidence.** [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices), [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams)). [Practitioner] Cognition reports a clean-context review agent catches on average 2 bugs per PR, "roughly 58%" severe; vendor-reported, no method published ([Cognition 2026](https://cognition.com/blog/multi-agents-working)). No published comparison of reviewer subagent versus self-review exists.

### 10. Keep the catalog small and specialists distinct

**Practice.** Add a custom definition only when it changes capability (scope, model, MCP, checklist). Keep descriptions non-overlapping; merge agents that could plausibly handle the same request.

**Why.** Descriptions sit in context every session. Overlap degrades selection more than count. "Three focused teammates often outperform five scattered ones."

**How.** In rough priority: (1) a read-only reviewer with a correctness-only rule; (2) a security reviewer with a checklist and a strong model; (3) a test runner that returns only failures; (4) a cheap explorer only if the built-in does not fit; (5) a planner if plan mode is not used. Debugger, docs researcher and database reader are situational. Prefer a skill for reusable knowledge that should run in the main context. Claude Code examples: `code-reviewer` (Read, Glob, Grep; sonnet), `security-reviewer` (Read, Grep, Glob, Bash; opus), `db-reader`, `researcher` (haiku), `browser-tester`, `api-developer` (preloaded skills), `experimenter` (worktree). Codex example: one review agent per dimension.

**Evidence.** [Vendor] ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Claude Code best practices](https://code.claude.com/docs/en/best-practices), [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)). Older [Vendor] overlapping tools ([OpenAI practical guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf), 2025). [Practitioner] Code and web search work as read-only subagents that "mostly resemble tool calls rather than true multi-agent collaboration" ([Cognition 2026](https://cognition.com/blog/multi-agents-working)). The priority list is a synthesis in the [research notes](../research-notes/agent-harness-best-practices/subagents.md); no study compares small and large catalogs.

### 11. Resume or fork instead of re-spawning

**Practice.** For a follow-up on finished work, resume the same subagent instead of spawning a new one that must rediscover the context.

**Why.** A resumed instance keeps its full history and tool results.

**How.** Claude Code: `SendMessage` with the agent ID or name. Codex: `resume_agent` / `send_input`. OpenCode: `task_id`. Claude Code forks inherit the full conversation and reuse the prompt cache, so they are cheaper than fresh subagents when the same context is needed; Codex has no subagent fork.

**Evidence.** [Vendor] ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [concept: mapping](../concepts/subagents.md#mapping)).

### 12. Design delegation one level deep for portability

**Practice.** One orchestrator (the main session), read-only workers in parallel, one writer at a time, an independent read-only reviewer at the end, and no nested spawning.

**Why.** Nesting limits differ: Claude Code allows 3 levels below the main conversation by default (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, `1` disables nesting); OpenCode's `subagent_depth` defaults to `1`; Codex documents no limit and no concurrency default.

**How.** Keep the plan in the main session; let workers report back rather than spawn further.

**Evidence.** [Vendor] ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [OpenCode agents](https://opencode.ai/docs/agents/), [Codex reference](../vendors/codex/subagents.md#limits-and-gotchas)). The pattern is a synthesis in the [research notes](../research-notes/agent-harness-best-practices/subagents.md).

### 13. Measure delegation against a single-agent baseline

**Practice.** Before adopting a delegation setup, run the same 10–20 representative tasks with a single agent and with delegation, several times each, with the same model. Compare task success, total tokens across all agents, wall time and peak main-context use.

**Why.** Runs are "non-deterministic between runs, even with identical prompts". Evaluating only success hides cost.

**How.** See [Verification](#verification). Pilot on 2–3 items before a large fan-out.

**Evidence.** [Empirical] Older: start with "about 20 queries representing real usage patterns" ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system), 2025); evaluate accuracy together with tokens and time, since leaderboards "focus solely on solution accuracy" ([SWE-Effi](https://arxiv.org/abs/2509.09853)). [Vendor] Pilot on 2–3 items ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)). No study validates the ~20-task heuristic for coding agents.

## Anti-patterns

| Avoid | Do instead |
| --- | --- |
| Delegating sequential implementation steps that share state | Keep them in the main conversation |
| Several subagents editing the same files | Read-only parallel work; one writer; or worktrees with disjoint file sets |
| "Use proactively" as the only trigger in a setup shared with Codex | Name the agent in `AGENTS.md` or the triggering skill |
| A Codex reviewer made "read-only" only by `sandbox_mode` in its file | Read-only parent sandbox, a `PreToolUse` hook, or a separate read-only session |
| A one-line delegation message that assumes the subagent saw the conversation | Goal, known facts, boundaries, stop condition, output contract |
| Relaying long subagent output through the conversation | A short summary plus a file path |
| Accepting a subagent's claim of success | Evidence: command, output, file:line; re-check what matters |
| A reviewer that reports every possible gap | Correctness and stated requirements only |
| Persona-only specialists ("You are an expert X developer") | The built-in type, or a skill |
| Many agents with overlapping descriptions | Few agents with disjoint triggers |
| Unscoped "investigate the codebase" | A narrow question per subagent |
| Spawning a new subagent to follow up on finished work | Resume it (`SendMessage`, `resume_agent`) |
| Deep delegation trees | One level |
| A cheap model on reviewers and planners | Cheap models only where failure is cheap to detect |
| Agent teams left unattended for long | "Monitor and steer"; quality-gate hooks |
| Best-of-N with no automatic judge | Tests or a benchmark script to pick the winner |

## Security

**Threat: injected content in results.** A subagent that reads web pages, issues or dependencies can return instruction-shaped text. Treat it as data ([practice 8](#8-verify-results-and-treat-them-as-untrusted-data)).
- Claude Code marks subagent results as subagent output with no user authority ([Claude Code reference](../vendors/claude-code/subagents.md#context-isolation-and-results)). In agent teams, a teammate "can't approve a permission prompt or supply consent on your behalf", and in auto mode a relayed approval claim is treated "as untrusted input rather than confirmation from you"; each inter-agent message is reviewed before delivery ([Claude Code agent teams](https://code.claude.com/docs/en/agent-teams)).
- Codex documents no authority labeling of results and no cross-thread injection handling. Apply the same rule by hand.

**Threat: a subagent with more power than intended.**
- Codex: the parent sandbox and live overrides (including `--yolo`) apply to subagents regardless of the agent file. Review runs need a read-only parent ([practice 4](#4-scope-capabilities-to-the-job-and-enforce-read-only-per-harness)).
- Restrict which agents the model may spawn: Claude Code `Agent(Name)` permission rules; OpenCode `permission.task` globs ([concept: comparison](../concepts/subagents.md#comparison)).
- Scope MCP servers to the agent that needs them (`mcpServers`, `mcp_servers`) instead of the main session.
- Add a validation hook when an agent needs a general tool such as Bash for read-only work (the `db-reader` pattern).

**Approvals.** Background subagent prompts surface in the main Claude Code session. In Codex non-interactive runs, an action that needs new approval fails and the error returns to the parent ([concept: comparison](../concepts/subagents.md#comparison)). Plan for that in headless fan-out by pre-approving only the narrow tools needed (`--allowedTools` with `--permission-mode dontAsk` in Claude Code).

**Context hygiene.** Claude Code auto memory is not loaded into subagents, except forks ([Claude Code memory docs](https://code.claude.com/docs/en/memory)).

## Verification

**Observe.**
- Hooks: `SubagentStart` and `SubagentStop` in both leads. In Claude Code all hooks inside a subagent carry `agent_id` and `agent_type`. In Codex the matcher is the agent type, `spawn_agent` is also matched as `Agent` in tool hooks, and subagents carry the parent's `session_id` ([concept: portability](../concepts/subagents.md#portability), [Claude Code hooks](https://code.claude.com/docs/en/hooks), [Codex hooks](https://learn.chatgpt.com/docs/hooks.md)).
- Minimum log: agent type, start and stop time, result size and, where available, token use; keep subagent transcripts; record which delegation message produced which result. No Codex documentation for per-subagent token accounting was found.
- Agent teams: `TeammateIdle`, `TaskCreated` and `TaskCompleted` hooks; exit code 2 sends feedback and blocks ([Claude Code agent teams](https://code.claude.com/docs/en/agent-teams)).

**Gate.** Deterministic gates such as a Stop hook that runs tests, or a `/goal` condition, let unattended runs finish correctly: "If you can't verify it, don't ship it" ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).

**Evaluate (baseline comparison).**
1. Pick 10–20 representative tasks.
2. Run a single-agent baseline and the delegated variant with the same model, several times each.
3. Compare success (tests or a rubric), total tokens across all agents, wall time and peak main-context use.
4. Label failures with the MAST categories (system design, inter-agent misalignment, task verification); MAST's LLM-as-judge pipeline aligns with human annotation, κ = 0.88 ([arXiv 2503.13657](https://arxiv.org/abs/2503.13657)).

[Empirical] Older: Anthropic found a single LLM-judge call with a rubric (factual accuracy, citation accuracy, completeness, source quality, tool efficiency), 0.0–1.0 scores and pass/fail "the most consistent"; human testing still caught hallucinations, system failures and source-selection bias. They resumed from checkpoints instead of restarting, used "rainbow deployments" when changing a running system, and a tool-testing agent that rewrote tool descriptions cut task completion time by 40% ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system), 2025).

**Watch for** the documented failures: the lead doing the work itself or stopping early; duplicate exploration across workers; reviewer over-reporting; parallel writers on the same files; descriptions so broad that every task gets delegated.

## Checklist

- [ ] Each delegation has a stated reason: summary of verbose output, parallel read-only work, fresh-context review, or a different scope or model.
- [ ] Parallel subagents are read-only; any parallel writer has its own worktree and file set.
- [ ] Each custom definition changes capability (tools, model, MCP, checklist), not only persona.
- [ ] Descriptions read "<what>. Use when <trigger>.", are short and do not overlap.
- [ ] Codex delegation is named in `AGENTS.md` or a skill.
- [ ] Read-only agents are enforced: `tools` allowlist in Claude Code; read-only parent or a hook in Codex.
- [ ] Models: cheap only for search and summarizing; strong for review and planning.
- [ ] Delegation messages carry goal, known facts, boundaries, stop condition and output contract.
- [ ] Output contracts require evidence (file:line, command output) and mark unverified items.
- [ ] Results are verified before acting; no subagent claim feeds a permission decision.
- [ ] Delegation trees are one level deep if they must run in every harness.
- [ ] `SubagentStart`/`SubagentStop` hooks log agent activity.
- [ ] A baseline comparison shows the setup improves success at an acceptable token and time cost.

## Open questions

- No controlled study compares Claude Code or Codex subagent use with single-agent runs on a coding benchmark with token accounting.
- The Google study's blog and arXiv versions differ in size and fit (180 vs 260 configurations; R² 0.513 vs 0.373). MAST per-category failure shares were not visible.
- No comparison of per-agent model routing on quality or cost; no comparison of small versus large custom-agent catalogs.
- Codex documents no default for `agents.max_concurrent_threads_per_session`, no nesting limit, no authority labeling of results, no cross-thread injection handling and no per-subagent token accounting. No Codex custom-agent example catalog was retrievable beyond the review-dimension example.
- No published comparison of a reviewer subagent with self-review; Cognition's bug-catch figures have no published method.
- No data on how often `/batch` or Codex best-of-N attempts improve outcomes.
- No study measures information loss between a subagent and its orchestrator in coding harnesses.
- No independent validation of the ~20-task eval-set heuristic for coding agents.

## Sources

Local:
- [Subagents concept](../concepts/subagents.md), [Concepts overview](../concepts/README.md)
- [Claude Code reference: subagents](../vendors/claude-code/subagents.md), [Codex reference: subagents](../vendors/codex/subagents.md)
- [Research notes: subagents](../research-notes/agent-harness-best-practices/subagents.md)

External:
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/agent-teams
- https://code.claude.com/docs/en/best-practices
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/memory
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/environments/git-worktrees.md
- https://learn.chatgpt.com/docs/developer-commands.md?surface=cli
- https://learn.chatgpt.com/docs/hooks.md
- https://opencode.ai/docs/agents/
- https://claude.com/blog/skills-explained
- https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- https://www.anthropic.com/engineering/building-effective-agents
- https://www.anthropic.com/engineering/multi-agent-research-system
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/
- https://arxiv.org/abs/2512.08296
- https://arxiv.org/abs/2503.13657
- https://arxiv.org/abs/2511.00872
- https://arxiv.org/abs/2605.27787
- https://arxiv.org/abs/2509.09853
- https://cognition.com/blog/dont-build-multi-agents
- https://cognition.com/blog/multi-agents-working
