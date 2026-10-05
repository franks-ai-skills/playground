# Subagents, specialized agents and multi-agent orchestration: best practices

Scope: when and how to use subagents (generalized model in `docs/concepts/subagents.md`: subagent definition, built-in types, subagent instance, result, spawn tool, resume), how to design subagent definitions, which orchestration patterns work, how to delegate and merge, which specialist agents are worth having, and how to observe and evaluate multi-agent runs. Claude Code and Codex are equal leads; OpenCode is noted where useful. Researched 2026-10-04.

Evidence labels used on every finding:
- **[Vendor]** vendor documentation or vendor engineering blog
- **[Empirical]** study or measured data (paper, benchmark, vendor-published measurement)
- **[Practitioner]** opinion or experience report without controlled data

Dating: sources from 2024 to mid-2025 are marked **(older, 2024)** or **(older, 2025)**. They predate the current subagent features in both harnesses (named definitions, background subagents, agent teams, Codex multi-agent on by default) and should be read as principles, not as product guidance.

## 1. When do subagents help and when do they hurt?

### Takeaway
Subagents help when the work is read-heavy, parallelizable or produces verbose output that only needs a summary (exploration, research, test runs, log triage, independent review). They hurt on sequential, tightly coupled work and on parallel writes, where split context produces conflicting implicit decisions. Every source agrees they cost substantially more tokens (Anthropic measured roughly 15x a chat for its multi-agent research system), so they pay off only when the task is valuable and decomposable.

### Cited Findings

Vendor guidance, current (both leads agree):
- [Vendor] Claude Code: use subagents when "the task produces verbose output you don't need in your main context", when you want to enforce tool restrictions, when "the work is self-contained and can return a summary", or to keep exploration and implementation out of the main conversation — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Vendor] Claude Code: stay in the main conversation when the task needs frequent back-and-forth, when "multiple phases share significant context (planning, implementation, testing)", for quick targeted changes, and when latency matters, because non-fork subagents "start fresh" and must gather context again — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Vendor] Codex: subagents work best for "read-heavy tasks such as exploration, tests, triage, and summarization"; they keep intermediate output off the main thread to avoid "context pollution" and "context rot" — [Codex: subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Vendor] Codex: "Be more careful with parallel write-heavy workflows, because agents editing code at once can create conflicts and increase coordination overhead." — [Codex: subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Vendor] Codex: "Because each subagent does its own model and tool work, subagent workflows consume more tokens than comparable single-agent runs." — [Codex: subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Vendor] Claude Code: "Running many subagents that each return detailed results can consume significant context, and each subagent spends tokens of its own while it runs." — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Vendor] Claude Code best practices name context as the main constraint ("performance degrades as it fills") and recommend "use subagents to investigate X" so exploration happens in a separate context; the "infinite exploration" anti-pattern (unscoped investigation reading hundreds of files) is fixed by scoping narrowly or delegating to subagents — [Claude Code: best practices](https://code.claude.com/docs/en/best-practices)
- [Vendor] Claude Code agent teams: "For sequential tasks, same-file edits, or work with many dependencies, a single session or subagents are more effective"; teams "use significantly more tokens than a single session" and are worthwhile for "research, review, and new feature work", while "for routine tasks, a single session is more cost-effective" — [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)
- [Vendor] OpenAI (older, 2025): "maximize a single agent's capabilities first. More agents can provide intuitive separation of concepts, but can introduce additional complexity and overhead, so often a single agent with tools is sufficient." Split only on "complex logic" (many if-then-else branches) or "tool overload", noting the issue is tool similarity/overlap, not count: some setups manage "more than 15 well-defined, distinct tools while others struggle with fewer than 10 overlapping tools" — [OpenAI: A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- [Vendor] Anthropic (older, 2024): "find the simplest solution possible, and only increasing complexity when needed"; agentic systems "often trade latency and cost for better task performance" — [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

Empirical data:
- [Empirical] Anthropic (older, 2025): a multi-agent system (Claude Opus 4 lead, Claude Sonnet 4 subagents) "outperformed single-agent Claude Opus 4 by 90.2%" on Anthropic's internal research eval; it is strongest for "breadth-first queries that involve pursuing multiple independent directions simultaneously" — [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Empirical] Same source: agents use "about 4× more tokens than chat interactions", multi-agent systems "about 15× more tokens than chats"; on BrowseComp, token usage alone explained 80% of performance variance, and token usage, number of tool calls and model choice together explained 95% — [Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Empirical/Vendor] Same source names the bad fits: domains "that require all agents to share the same context or involve many dependencies between agents", and "most coding tasks involve fewer truly parallelizable tasks than research" — [Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Empirical] Google Research (blog Jan 28, 2026; paper arXiv 2512.08296): multi-agent coordination gave +80.9% on the parallelizable Finance-Agent task but −39% to −70% on the sequential PlanCraft task "across all multi-agent variants"; independent (uncoordinated) multi-agent systems amplified errors 17.2x vs 4.4x for centralized (orchestrated) ones; "more agents" is not universally optimal, architecture must match task structure — [Google Research blog](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/); [arXiv 2512.08296](https://arxiv.org/abs/2512.08296)
- [Empirical] Version conflict in the Google study: the blog reports 180 configurations, 4 benchmarks, predictive model R² = 0.513, 87% correct architecture choice on unseen configurations — [Google Research blog](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/); the arXiv listing (later version) reports 260 configurations, 6 benchmarks, cross-validated R² = 0.373, 87% on unseen tasks, and notes that systems improving monotonically with team size on static benchmarks behave differently on tasks with "sustained environmental interaction, where coordination overhead and error propagation dynamics dominate" — [arXiv 2512.08296](https://arxiv.org/abs/2512.08296)
- [Empirical] MAST, "Why Do Multi-Agent LLM Systems Fail?" (Cemri et al., UC Berkeley; v1 March 2025, v3 Oct 26, 2025): 1,600+ annotated traces from 7 multi-agent frameworks, 14 failure modes in 3 categories (system design issues, inter-agent misalignment, task verification), inter-annotator κ = 0.88; "performance gains on popular benchmarks are often minimal" relative to single-agent baselines — [arXiv 2503.13657](https://arxiv.org/abs/2503.13657)
- [Empirical] Yin et al. (Nov 2025), 7 agent frameworks on software development, vulnerability detection and program repair: the multi-agent AgentOrchestra had "the longest trajectories and the most correction attempts due to coordination overhead"; overall performance "moderate" — [arXiv 2511.00872](https://arxiv.org/abs/2511.00872)
- [Empirical] "Long Live the Librarian!" (Cho et al., arXiv 2605.27787, submitted May 27, 2026): in multi-agent SWE systems, agents "repeatedly re-explore overlapping repository regions", inflating output tokens, which cost "30 to 1,000 times more energy than an input or cached token"; a persistent search sub-agent cut per-episode GPU energy by 11–30% while preserving task performance — [arXiv 2605.27787](https://arxiv.org/abs/2605.27787)

Practitioner opinion:
- [Practitioner] Cognition (older, June 12, 2025), "Don't build multi-agents": two principles, "Share context, and share full agent traces, not just individual messages" and "Actions carry implicit decisions, and conflicting decisions carry bad results"; the Flappy Bird example (one subagent built a Super Mario style background, another a mismatched bird); recommends a "single-threaded linear agent" plus a history-compression model for long tasks; notes Claude Code then used subagents only to answer questions, not to write code in parallel — [Cognition: Don't build multi-agents](https://cognition.com/blog/dont-build-multi-agents)
- [Practitioner/Empirical] Cognition update (April 22, 2026), "Multi-Agents: What's Actually Working": now uses several multi-agent flows in Devin (reviewer loop, "smart friend" escalation, read-only subagents, manager/child Devins) but still reports that parallel writing agents fail because divergent implicit decisions fragment the code — [Cognition: Multi-Agents: What's Actually Working](https://cognition.com/blog/multi-agents-working)

### Inferences
- Default to a single agent; add a subagent when one of four conditions holds: (1) verbose output that needs only a summary, (2) independent read-only branches that can run in parallel, (3) a need for a fresh, unbiased context (review, verification), (4) a need for a different capability scope or model. Do not delegate sequential implementation steps that share state.
- The 90.2% research gain and the −39% to −70% sequential-task loss are compatible: both say the benefit depends on decomposability. Coding is usually less decomposable than research, so coding gains come mostly from isolation (exploration, review) rather than from parallel writing.
- Token cost is the first-order trade-off. Because both harnesses bill each subagent's own context, a fan-out of N read-heavy subagents costs roughly N full explorations plus the merged summaries; this is acceptable only when the task is valuable or the main context would otherwise overflow.

### Gaps
- No controlled study found that compares Claude Code or Codex subagent use against single-agent runs on a coding benchmark (SWE-bench or similar) with token accounting.
- MAST category percentages (share of failures per category) were not visible in the abstract fetched; not reported here.

## 2. Designing subagent definitions

### Takeaway
A good definition has a short, trigger-oriented description (what and when), focused instructions for one job, the narrowest capability scope that works (read-only for explorers and reviewers), a model and effort matched to the job (cheap/fast for search, strong for review and planning), and an explicit output contract. Capability scoping is enforced differently: Claude Code enforces a `tools` allowlist per definition; Codex has no tool allowlist and the parent sandbox wins over the definition's `sandbox_mode`.

### Cited Findings

Description (delegation trigger):
- [Vendor] Claude Code: "Claude uses each subagent's description to decide when to delegate tasks"; descriptions occupy context, so keep them short; a startup warning appears when custom descriptions combined exceed 15,000 tokens; phrases like "use proactively" encourage automatic delegation — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Vendor] Claude Code example description pattern: what it does plus when to use it, e.g. "Scans files and suggests improvements for readability, performance, and best practices. Use after writing or modifying code." — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Vendor] Codex: `description` tells "when Codex should use this agent", but current local releases "spawn agents after a direct request or applicable project or skill instruction" (e.g. "spawn two agents", "use one agent per point"), so the description alone does not trigger delegation — [Codex: subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) (as recorded in the repo's [Codex vendor reference](../../vendors/codex/subagents.md))
- [Vendor] OpenCode: only subagents allowed by `permission.task` appear in the Task tool description, so denied subagents cost no context — [OpenCode: agents](https://opencode.ai/docs/agents/)

Instructions and focus:
- [Vendor] Claude Code best practices example `security-reviewer`: role ("You are a senior security engineer"), a checklist of what to look for, and an output requirement ("Provide specific line references and suggested fixes") — [Claude Code: best practices](https://code.claude.com/docs/en/best-practices)
- [Vendor] Claude Code: `skills` field preloads skill content into a subagent ("gives the subagent domain knowledge without needing to discover skills during execution"); `memory` gives a subagent a persistent directory (user/project/local) for learned patterns — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents). Neither has a Codex counterpart (dropped in `docs/concepts/subagents.md`).
- [Vendor] Codex: required fields `name`, `description`, `developer_instructions`; optional `model`, `model_reasoning_effort`, `sandbox_mode`, plus other config keys such as `mcp_servers` and `skills.config` — [Codex: subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

Capability scope (least privilege):
- [Vendor] Claude Code: restrict with a `tools` allowlist (e.g. `Read, Grep, Glob` for a reviewer) or a `disallowedTools` denylist (e.g. `Write, Edit`); add conditional rules with a subagent-scoped `PreToolUse` hook (example: a `db-reader` agent whose Bash calls are validated by `validate-readonly-query.sh`; exit code 2 blocks) — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Vendor] Claude Code: scope MCP servers to one subagent with `mcpServers` (example: Playwright only for a `browser-tester`), keeping those tool descriptions out of the main context — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Vendor] Codex: subagents inherit the parent sandbox policy and live runtime overrides (`/permissions`, `--yolo`) "even if the selected custom agent file sets different defaults"; in non-interactive runs an action needing new approval fails and the error returns to the parent — [Codex: subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Vendor] Claude Code agent teams: teammates start with the lead's permission mode; per-teammate modes cannot be set at spawn time; `tools` from a referenced subagent definition does apply to the teammate — [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)
- [Vendor] OpenAI (older, 2025): split agents when tools overlap and better tool names/descriptions do not fix selection errors — [OpenAI: practical guide (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- [Vendor] Anthropic (older, 2024): design tools "poka-yoke" so mistakes are hard (SWE-bench agent: switching to absolute file paths removed a class of errors); the team "spent more time optimizing our tools than the overall prompt" — [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

Model and effort per agent:
- [Vendor] Claude Code: Haiku for "exploration and research" and to "control costs by routing tasks to faster, cheaper models"; Sonnet for balance; Opus for complex analysis; `inherit` to match the main model. Resolution order: spawn parameter > definition `model` > `CLAUDE_CODE_SUBAGENT_MODEL` > main model — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Vendor] Codex: a large model for "demanding, ambiguous work requiring planning and validation", a small fast model for "fast, narrowly scoped tasks with clear, repeatable work"; reasoning effort `high` for tracing logic and edge cases, `low` for straightforward work. As of Oct 2026 the page names "GPT-6.1 Sol" and "GPT-6 Luna" for these roles (model names change; treat as examples) — [Codex: subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Empirical] Anthropic (older, 2025) used a strong lead (Opus 4) with cheaper workers (Sonnet 4); model choice was one of three factors explaining 95% of BrowseComp variance — [Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Practitioner] Cognition (2026): the reverse pairing also works — a weaker primary calls a stronger "smart friend" model for hard sub-problems, including across vendors; the open problem is getting the weaker model to recognize when to escalate — [Cognition: Multi-Agents: What's Actually Working](https://cognition.com/blog/multi-agents-working)

Output contract:
- [Vendor] Anthropic (older, 2025): each delegation needs "an objective, an output format, guidance on the tools and sources to use, and clear task boundaries" — [Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Vendor] Anthropic (Sept 29, 2025): subagents may use "tens of thousands of tokens or more" but return "a condensed, distilled summary of its work (often 1,000-2,000 tokens)" — [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Vendor] Claude Code example prompts state the return shape: "run the test suite and report only the failing tests with their error messages"; teammate prompts ask to "Report any issues with severity ratings" — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents); [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)
- [Vendor] Claude Code fan-out scripts use a minimal machine-checkable contract: "Return OK or FAIL." — [Claude Code: best practices](https://code.claude.com/docs/en/best-practices)

### Inferences
- Write the description as "<what it does>. Use when <trigger>." For Codex, additionally name the agent in `AGENTS.md` or the triggering skill ("use the `reviewer` agent after edits"), because Codex does not delegate on descriptions alone.
- Put the output contract in the definition's instructions (format, length cap, required fields such as file:line, severity, confidence, "unverified" markers), and repeat task-specific parts in the delegation message.
- Do not rely on a Codex agent file to make a reviewer read-only. Enforce read-only by running the parent in a read-only sandbox for review runs, by a `PreToolUse` hook on the subagent's agent type, or by reviewing in a separate read-only session. In Claude Code the `tools` allowlist is sufficient.
- Pin a cheap model only on agents whose failure is cheap to detect (search, listing, summarizing logs); keep reviewers and planners on the strong model, since a missed bug costs more than the tokens.

### Gaps
- No empirical comparison found of per-agent model routing (e.g. Haiku explorer vs inherited model) on coding quality or total cost in Claude Code or Codex.
- Codex documents no default for `agents.max_concurrent_threads_per_session` and no nesting limit (repo's [Codex vendor reference](../../vendors/codex/subagents.md)).

## 3. Orchestration patterns

### Takeaway
The patterns that work in coding harnesses are centralized: orchestrator-worker with read-only fan-out/fan-in, explore-then-plan-then-implement, writer plus independent reviewer or verifier, chains of specialists, and best-of-N or per-item fan-out with each writer in its own worktree. Peer-to-peer and parallel-writer setups are the least reliable; centralized orchestration amplified errors about 4x less than independent agents in Google's study.

### Cited Findings

Pattern catalog (definitions):
- [Vendor] Anthropic (older, 2024) defines the workflow patterns: prompt chaining (fixed sequential subtasks), routing (classify then dispatch to specialists), parallelization as *sectioning* (independent subtasks) or *voting* (same task several times), orchestrator-workers ("complex tasks where you can't predict the subtasks needed", e.g. "coding products that make complex changes to multiple files"), evaluator-optimizer (generator plus critic loop, "when we have clear evaluation criteria, and when iterative refinement provides measurable value") — [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Vendor] OpenAI (older, 2025): *manager* pattern ("agents as tools"; one agent keeps control and user access) vs *decentralized* handoffs (one-way transfer of execution and conversation state between peers); "starting with a single agent and evolving to multi-agent systems only when needed" — [OpenAI: practical guide (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

Orchestrator-worker / fan-out, fan-in:
- [Vendor] Claude Code: "Research the authentication, database, and API modules in parallel using separate subagents"; default cap of 20 concurrent subagents (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`) — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Vendor] Codex: spawn one agent per review dimension (security, code quality, tests, maintainability) and consolidate by category; Codex "waits until all requested results are available" and returns one consolidated response — [Codex: subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Empirical] Anthropic (older, 2025): the lead "spins up 3-5 subagents in parallel" and each subagent uses 3+ tools in parallel, cutting research time "up to 90% for complex queries"; effort-scaling rules embedded in the lead prompt: "Simple fact-finding requires just 1 agent with 3-10 tool calls, direct comparisons might need 2-4 subagents with 10-15 calls each" — [Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Empirical] Same source: synchronous fan-in is a bottleneck: "Subagents can't coordinate, and the entire system can be blocked while waiting for a single subagent to finish" — [Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Empirical] Google (2026): centralized coordination amplified errors 4.4x vs 17.2x for independent agents; "orchestrators function as validation checkpoints" — [Google Research blog](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)
- [Practitioner] Cognition (2026): a manager Devin splits a task, spawns child Devins and coordinates them in a map-reduce style — [Cognition: Multi-Agents: What's Actually Working](https://cognition.com/blog/multi-agents-working)

Pipeline / chain and plan-then-execute:
- [Vendor] Claude Code: chain subagents ("Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them"); the main agent passes relevant context from one to the next — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Vendor] Claude Code: explore, plan, implement, commit; skip planning "if you could describe the diff in one sentence"; for larger features, interview the user, write `SPEC.md`, then implement in a fresh session — [Claude Code: best practices](https://code.claude.com/docs/en/best-practices)
- [Vendor] Claude Code agent teams: teammates spawned while the lead is in plan mode stay read-only until their plan is approved (note: the lead approves automatically, without the user) — [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)

Reviewer / critic, writer plus verifier:
- [Vendor] Claude Code: "A fresh context improves code review since Claude won't be biased toward code it just wrote" (Writer/Reviewer sessions; also one agent writes tests, another writes code to pass them) — [Claude Code: best practices](https://code.claude.com/docs/en/best-practices)
- [Vendor] Claude Code: "Before treating a task as done, have a subagent review the diff in a fresh context and report gaps"; a verification subagent has "a fresh model try to refute the result, so the agent doing the work isn't the one grading it" — [Claude Code: best practices](https://code.claude.com/docs/en/best-practices)
- [Vendor] Claude Code warning: "A reviewer prompted to find gaps will usually report some, even when the work is sound"; chasing every finding causes over-engineering; tell the reviewer "to flag only gaps that affect correctness or the stated requirements" — [Claude Code: best practices](https://code.claude.com/docs/en/best-practices)
- [Empirical/Practitioner] Cognition (2026): a review agent with clean context catches on average 2 bugs per PR, "roughly 58%" severe (logic errors, missing edge cases, security) — vendor-reported, no method published — [Cognition: Multi-Agents: What's Actually Working](https://cognition.com/blog/multi-agents-working)
- [Vendor] Claude Code agent teams: split review by lens (security, performance, test coverage) because "a single reviewer tends to gravitate toward one type of issue at a time"; for debugging, run competing hypotheses with teammates that try to disprove each other, because sequential investigation "suffers from anchoring" — [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)

Best-of-N and per-item fan-out with writes:
- [Vendor] Codex cloud: `codex cloud exec --attempts 1-4` (default 1) runs best-of-N attempts — [Codex CLI reference](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli) (recorded in the repo's [Codex vendor reference](../../vendors/codex/subagents.md))
- [Vendor] Claude Code: `/batch <instruction>` splits a change across 5 to 30 subagents, each in its own worktree; for scripted fan-out loop `claude -p` per file with `--allowedTools` and `--permission-mode dontAsk`, test on 2-3 files first, then run on all — [Claude Code: best practices](https://code.claude.com/docs/en/best-practices)

Parallel writes and isolation:
- [Vendor] Claude Code: `isolation: worktree` on a definition runs the subagent in its own git worktree, auto-cleaned if unchanged — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Vendor] Codex: worktrees are per session (desktop app parallel chats in worktrees; CLI `--worktree`), not per subagent — [Codex: worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees.md)
- [Vendor] Claude Code agent teams: "Two teammates editing the same file leads to overwrites. Break the work so each teammate owns a different set of files." — [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)
- [Practitioner] Cognition (2025 and 2026): parallel writers remain the failing pattern — [Cognition: Don't build multi-agents](https://cognition.com/blog/dont-build-multi-agents); [Cognition: Multi-Agents: What's Actually Working](https://cognition.com/blog/multi-agents-working)

Nesting:
- [Vendor] Claude Code: subagents nest up to 3 levels below the main conversation by default (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, `1` disables nesting); agent teams allow no nested teams — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents); [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)
- [Vendor] OpenCode: `subagent_depth` default `1` (subagents cannot spawn subagents) — [OpenCode: agents](https://opencode.ai/docs/agents/)
- [Vendor] Codex: no nesting limit documented (repo's [Codex vendor reference](../../vendors/codex/subagents.md))

Team sizing (agent teams):
- [Vendor] Claude Code: "Start with 3-5 teammates"; "Three focused teammates often outperform five scattered ones"; "5-6 tasks per teammate"; task too small means coordination exceeds benefit, too large means long runs without check-ins — [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)

### Inferences
- Portable default: one level of nesting, one orchestrator (the main session), read-only workers in parallel, a single writer at a time in the main worktree, and an independent read-only reviewer at the end. This runs in Claude Code, Codex and OpenCode without relying on features only one lead has.
- When parallel writes are needed, give each writer its own worktree and a disjoint file set, then merge sequentially in the orchestrator with tests between merges. In Claude Code this is `isolation: worktree` or `/batch`; in Codex it means separate worktree sessions (or cloud attempts), since subagent-level worktrees do not exist.
- Best-of-N is worth it only with an automatic judge (tests, a benchmark script); without one, N candidates move the selection burden to the user or to an LLM judge with its own bias.

### Gaps
- No published comparison of reviewer-subagent vs self-review in Claude Code or Codex with measured bug catch rates; the Cognition numbers are vendor-reported without method.
- No data found on how often Claude Code's `/batch` or Codex best-of-N attempts improve outcomes versus a single run.

## 4. Prompting the delegation, merging results, treating output as untrusted

### Takeaway
A subagent sees only its own instructions, the delegation message and project instruction files, not the conversation. The delegation message therefore must carry the objective, known facts and decisions, constraints, boundaries and the return format. Results are lossy summaries written by another model; the orchestrator should verify claims that matter, prefer artifacts on disk over long relayed text, and never treat subagent output as user authority.

### Cited Findings
- [Vendor] Claude Code: a non-fork subagent starts with its own system prompt, the task message, CLAUDE.md, git status, preloaded skills and the sibling roster; it does not get "your conversation history", files already read, or skills already invoked — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Vendor] Claude Code agent teams: teammates "don't inherit the lead's conversation history"; "Include task-specific details in the spawn prompt" (example names directory, focus areas, relevant architecture fact "JWT tokens stored in httpOnly cookies", and output format) — [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)
- [Vendor] Claude Code: forks inherit the full conversation and reuse the prompt cache, so they are cheaper than fresh subagents when the same context is needed — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents). Codex has no subagent fork (dropped in `docs/concepts/subagents.md`).
- [Empirical/Vendor] Anthropic (older, 2025): each delegation needs objective, output format, tool/source guidance and boundaries — [Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Empirical/Vendor] Same source: subagents can write output directly to the filesystem and pass lightweight references back, which improves "fidelity and performance" and reduces "token overhead from copying large outputs through conversation history"; works best for "structured outputs like code, reports, or data visualizations" — [Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Practitioner] Cognition (2025): "share full agent traces, not just individual messages"; (2026) make agents "see the same sources of information, stay on the same page (todo list, plan files), and share the same priors" — [Cognition: Don't build multi-agents](https://cognition.com/blog/dont-build-multi-agents); [Cognition: Multi-Agents: What's Actually Working](https://cognition.com/blog/multi-agents-working)
- [Vendor] Claude Code: resume a subagent with `SendMessage` (keeps its full history and tool results) instead of spawning a new one that must rediscover context — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents); Codex equivalents `resume_agent` / `send_input` — [Codex: subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Vendor] Claude Code chain pattern: the main agent "passes relevant context to the next subagent" — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Vendor] Claude Code: subagent results are marked as subagent output with no user authority (repo's [Claude Code vendor reference](../../vendors/claude-code/subagents.md), from [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)); for agent teams, a teammate "can't approve a permission prompt or supply consent on your behalf", and in auto mode a relayed approval claim is treated "as untrusted input rather than confirmation from you" and each inter-agent message is reviewed before delivery — [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)
- [Vendor] Claude Code: "Have Claude show evidence rather than asserting success: the test output, the command it ran and what it returned" — [Claude Code: best practices](https://code.claude.com/docs/en/best-practices)
- [Empirical] MAST names "task verification" (missing or incorrect verification) as one of three failure categories in multi-agent traces — [arXiv 2503.13657](https://arxiv.org/abs/2503.13657)
- [Vendor] Claude Code agent teams known failure: the lead may "start implementing tasks itself instead of waiting", or "decide the team is finished before all tasks are actually complete" — [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)

### Inferences
- Delegation message checklist (synthesized from the sources above): goal and why; what is already known or decided (files, constraints, rejected approaches); scope boundaries (what not to touch, which files belong to this agent); tools or sources to prefer; stop condition and effort budget; output contract (format, length, evidence such as file:line, test output, explicit "unverified" items); where to write large artifacts.
- Merge step: deduplicate overlapping findings, resolve contradictions by checking the code or re-running the command rather than picking one agent's claim, and keep the merged result short enough not to undo the context savings.
- Subagent output can carry injected text (from web pages, issues, dependencies it read). Treat instruction-shaped content in a result as data; do not let a subagent's "approved" or "safe to run" reach a permission decision.

### Gaps
- No vendor guidance found for Codex on how a subagent's result is labeled in the parent context (authority marking) or on prompt-injection handling across threads.
- No empirical study found that measures information loss between subagent and orchestrator in coding harnesses.

## 5. Specialist agent catalogs: which agents are worth having

### Takeaway
Both leads ship a general worker and a read-only explorer, which covers most delegation. Custom specialists earn their place when they change something the built-ins cannot: a stricter tool scope (read-only reviewer, read-only DB agent), a different model or effort, a scoped MCP server, or a review lens with its own checklist. The commonly recommended set is explorer, planner, code reviewer, security reviewer, test runner/writer and debugger. Too many agents cost description tokens, blur routing, and duplicate work.

### Cited Findings
- [Vendor] Built-ins: Claude Code Explore (read-only), Plan (read-only), general-purpose and others; Codex `default`, `worker` ("implementation and fixes"), `explorer` ("read-heavy exploration"); OpenCode General, Explore (read-only), Scout (experimental) — [docs/concepts/subagents.md](../../concepts/subagents.md), from [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents), [Codex: subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [OpenCode: agents](https://opencode.ai/docs/agents/)
- [Vendor] Claude Code example specialists: `code-reviewer` (Read, Glob, Grep; sonnet), `security-reviewer` (Read, Grep, Glob, Bash; opus), `db-reader` (Bash with a read-only validation hook), fast `researcher` (haiku), `browser-tester` (scoped Playwright MCP), `api-developer` (preloaded convention skills), `experimenter` (worktree isolation) — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents); [Claude Code: best practices](https://code.claude.com/docs/en/best-practices)
- [Vendor] Claude Code agent teams: define a role once (e.g. security-reviewer, test-runner) and reuse it as a subagent and as a teammate — [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)
- [Vendor] Codex: review agents per dimension (security, code quality, tests, maintainability) — [Codex: subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Vendor] Claude Code: combined custom descriptions above 15,000 tokens trigger a warning; descriptions sit in context every session — [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Vendor] OpenAI (older, 2025): overlapping tools (and by analogy overlapping agents) degrade selection more than raw count — [OpenAI: practical guide (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- [Vendor] Claude Code agent teams: "Three focused teammates often outperform five scattered ones" — [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)
- [Empirical] Redundant re-exploration of overlapping repo regions is a measured cost driver in multi-agent SWE systems; a persistent search sub-agent reduced it — [arXiv 2605.27787](https://arxiv.org/abs/2605.27787)
- [Practitioner] Cognition (2026): code search and web search work as "readonly subagents" that "mostly resemble tool calls rather than true multi-agent collaboration" — [Cognition: Multi-Agents: What's Actually Working](https://cognition.com/blog/multi-agents-working)

### Inferences
- Worth having (in rough priority): (1) a read-only reviewer with a correctness-only reporting rule; (2) a security reviewer with a checklist and strong model; (3) a test runner that returns only failures; (4) a cheap explorer only if the built-in one does not fit (e.g. different model); (5) a planner if plan mode is not used. Debugger, docs researcher and DB reader are situational.
- A specialist that differs from a built-in only in persona ("You are an expert X developer") adds routing ambiguity and description tokens without changing capability. Prefer a skill for reusable knowledge that should run in the main context.
- Keep descriptions non-overlapping; if two agents could plausibly handle the same request, merge them or make the trigger conditions disjoint.

### Gaps
- No empirical comparison found between a small and a large custom-agent catalog in either harness (routing accuracy or cost).
- No vendor-published Codex custom-agent example catalog was retrievable in this session beyond the review-dimension example (a `learn.chatgpt.com/docs/concepts/subagents` URL returned 404).

## 6. Observability and evaluation of multi-agent runs

### Takeaway
Multi-agent runs are non-deterministic and fail in compounding ways, so they need traces of agent decisions, hooks at subagent start and stop, and outcome-based evaluation on a small, realistic task set before scaling. Both leads expose `SubagentStart` and `SubagentStop` hooks. Verify that subagents help by comparing the same tasks with and without delegation on success rate, total tokens and wall time.

### Cited Findings
- [Empirical/Vendor] Anthropic (older, 2025): agents are "non-deterministic between runs, even with identical prompts"; full production tracing was needed to diagnose failures; they monitored "agent decision patterns and interaction structures" without reading conversation contents — [Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Empirical/Vendor] Same source: start evaluating with "about 20 queries representing real usage patterns", since early changes have large effect sizes; an LLM judge with a rubric (factual accuracy, citation accuracy, completeness, source quality, tool efficiency) in a single call with 0.0-1.0 scores and pass/fail "was the most consistent"; human testing caught hallucinations, system failures and "subtle source selection biases" — [Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Empirical/Vendor] Same source: "Minor system failures can be catastrophic for agents"; resume from checkpoints rather than restart; use "rainbow deployments" when changing a running agent system; a tool-testing agent that rewrote tool descriptions cut task completion time by 40% — [Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Empirical] MAST provides a failure taxonomy (14 modes) and an LLM-as-a-judge annotation pipeline aligned with human annotation, usable to label failures in one's own traces — [arXiv 2503.13657](https://arxiv.org/abs/2503.13657)
- [Empirical] Google (2026): measured task properties (tool count, decomposability) predict the better architecture for 87% of unseen configurations — [Google Research blog](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)
- [Vendor] Hooks: Claude Code `SubagentStart`/`SubagentStop`, with `agent_id`/`agent_type` on all hooks inside a subagent; Codex `SubagentStart`/`SubagentStop` with agent type as matcher, `spawn_agent` also matched as `Agent` in tool hooks, subagents carry the parent's `session_id` — [docs/concepts/subagents.md](../../concepts/subagents.md), from [Claude Code: hooks](https://code.claude.com/docs/en/hooks) and [Codex: hooks](https://learn.chatgpt.com/docs/hooks.md)
- [Vendor] Claude Code agent teams quality gates: `TeammateIdle`, `TaskCreated`, `TaskCompleted` hooks; exit code 2 sends feedback and blocks — [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)
- [Vendor] Claude Code: deterministic gates (Stop hook running tests, `/goal` condition) let unattended runs finish correctly; "If you can't verify it, don't ship it" — [Claude Code: best practices](https://code.claude.com/docs/en/best-practices)
- [Vendor] Claude Code agent teams: "Monitor and steer"; letting a team run unattended too long "increases the risk of wasted effort"; known limitations include lagging task status and leads stopping early — [Claude Code: agent teams](https://code.claude.com/docs/en/agent-teams)
- [Vendor] Claude Code fan-out: pilot on 2-3 items, refine the prompt, then run on all — [Claude Code: best practices](https://code.claude.com/docs/en/best-practices)
- [Empirical] SWE-Effi (Fan et al.): leaderboards "focus solely on solution accuracy"; it defines effectiveness as the balance of accuracy and resources (tokens, time), so evaluate accuracy together with tokens and time — [arXiv 2509.09853](https://arxiv.org/abs/2509.09853)

### Inferences
- Minimum observability for both leads: a `SubagentStart`/`SubagentStop` hook that logs agent type, start/stop time, and (where available) token use and result size; keep transcripts of subagent runs; record which delegation message produced which result.
- Verification protocol to show a subagent setup helps: pick 10-20 representative tasks; run baseline (single agent) and delegated variant with the same model, several times each because runs are non-deterministic; compare task success (tests or rubric), total tokens across all agents, wall time and main-context peak; inspect failures with the MAST categories (specification, inter-agent misalignment, verification).
- Watch for the documented anti-patterns: lead does the work itself or stops early; duplicate exploration across workers; reviewer over-reporting; parallel writers editing the same files; descriptions so broad that every task gets delegated.

### Gaps
- No vendor documentation found on per-subagent token accounting in Codex; Claude Code's per-subagent cost reporting was not checked in this session.
- No independent study found that validates Anthropic's ~20-task eval-set heuristic for coding agents specifically.
