# Subagents

A subagent is a separate agent instance that the main agent starts for a delegated task. It runs in its own context window and returns one result to its caller, which keeps noisy intermediate output such as search results, logs and test runs out of the main context and lets independent tasks run in parallel. A subagent definition is a named, reusable configuration (instructions, model and capability scope) that the harness applies when it spawns that kind of subagent.

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Definition format | Markdown with YAML frontmatter; body is the system prompt ([CC][cc-sub]) | TOML; `developer_instructions` holds the prompt; applied as a config layer ([Codex][cx-sub]) | Markdown with frontmatter, or JSON under `agent` ([OC][oc-sub]) |
| Project location | `.claude/agents/`, walking up to the repo root ([CC][cc-sub]) | `.codex/agents/*.toml` ([Codex][cx-sub]) | `.opencode/agents/` ([OC][oc-sub]) |
| User location | `~/.claude/agents/` ([CC][cc-sub]) | `~/.codex/agents/*.toml` ([Codex][cx-sub]) | `~/.config/opencode/agents/` ([OC][oc-sub]) |
| Required fields | `name`, `description`; invalid files skipped silently ([CC][cc-sub]) | `name`, `description`, `developer_instructions` ([Codex][cx-sub]) | `description`; name from the file path ([OC][oc-sub]) |
| Model / effort | `model` (alias, ID or `inherit`), `effort` ([CC][cc-sub]) | `model`, `model_reasoning_effort` ([Codex][cx-sub]) | `model`, `variant` ([OC][oc-sub]) |
| Capability scope | `tools` allowlist, `disallowedTools`, `permissionMode` ([CC][cc-sub]) | No tool allowlist; `sandbox_mode`, `mcp_servers`, `skills.config`; parent sandbox and runtime overrides win ([Codex][cx-sub]) | `permission` rules merged over global rules ([OC][oc-sub]) |
| Built-in types | Explore, Plan (both read-only), general-purpose and others ([CC][cc-sub]) | `default`, `worker`, `explorer` ([Codex][cx-sub]) | General, Explore (read-only), Scout (experimental) ([OC][oc-sub]) |
| Spawn mechanism | Agent tool ([CC][cc-sub]) | `spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, `close_agent` ([Codex][cx-sub]) | `task` tool ([OC][oc-sub]) |
| When the model delegates | Automatically by description, or on request ([CC][cc-sub]) | Only on a direct request or an `AGENTS.md`/skill instruction ([Codex][cx-sub]) | By description ([OC][oc-sub]) |
| What the subagent receives | Own prompt, delegation message, `CLAUDE.md` (except Explore/Plan), git status, preloaded skills; no conversation history ([CC][cc-sub]) | Not recorded beyond inherited settings ([Codex][cx-sub]) | Not recorded |
| Result | Final report, marked as having no user authority ([CC][cc-sub]) | Summary; Codex waits for all results and returns one consolidated response ([Codex][cx-sub]) | Child session ([OC][oc-sub]) |
| Model resolution | Spawn parameter > definition > `CLAUDE_CODE_SUBAGENT_MODEL` > main model ([CC][cc-sub]) | Agent file > spawn value > `[agents]` default > parent ([Codex][cx-sub]) | Own `model`, else the invoking agent's ([OC][oc-sub]) |
| Resume | `SendMessage` with ID or name ([CC][cc-sub]) | `resume_agent`, `send_input` ([Codex][cx-sub]) | `task_id` ([OC][oc-sub]) |
| Nesting / concurrency | Depth 3 by default; 20 concurrent by default ([CC][cc-sub]) | Nesting not documented; `agents.max_concurrent_threads_per_session`, default not documented ([Codex][cx-sub]) | `subagent_depth` default `1` ([OC][oc-sub]) |
| Approvals inside subagents | Background prompts surface in the main session ([CC][cc-sub]) | In non-interactive runs the action fails and the error returns to the parent ([Codex][cx-sub]) | `opencode run` answers them ([OC][oc-sub]) |
| Hook events | `SubagentStart`, `SubagentStop` ([CC hooks][cc-hooks]) | `SubagentStart`, `SubagentStop` ([Codex][cx-sub]) | None recorded |

## Generalized model

- **Subagent definition.** One file per definition with `name` and `description` (required), instructions (required), and optional model, reasoning effort, capability scope and MCP servers. The main agent reads the description to choose a type.
- **Built-in types.** Each harness ships at least a general-purpose type and a read-only exploration type.
- **Instance.** A running agent created from a definition plus a delegation message, with its own context window and an ID. It does not see the caller's conversation history.
- **Result.** The single message the instance returns. The caller sees the result, not the intermediate output.
- **Scopes.** Project and user in both leads.
- **Lifecycle.** Load definitions at session start; spawn with a type and a delegation message; run in its own context (approval requests surface through the main session or fail back to the parent in non-interactive runs); return one result; optionally resume by ID with history retained; close.
- **Invocation.** Model-initiated (trigger policy differs: Claude Code delegates on descriptions, Codex only when asked) or user-initiated. Several instances can run in parallel up to a concurrency limit.
- **Inheritance.** Unspecified settings come from the parent. In Claude Code the definition's `tools` and `permissionMode` apply; in Codex the parent's sandbox and live overrides win over the definition.

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Subagent definition | `.claude/agents/*.md` | `.codex/agents/*.toml` | `.opencode/agents/*.md` with `mode: subagent` |
| Instructions | Markdown body | `developer_instructions` | Markdown body / `prompt` |
| Reasoning effort | `effort` | `model_reasoning_effort` | `variant` |
| Capability scope | `tools`, `disallowedTools`, `permissionMode` | `sandbox_mode` (parent wins) | `permission` |
| MCP servers | `mcpServers` | `mcp_servers` | — |
| Spawn tool | Agent tool | `spawn_agent` | `task` |
| Resume | `SendMessage` | `resume_agent` / `send_input` | `task_id` |
| General-purpose / read-only built-in | general-purpose / Explore | `default` (also `worker`) / `explorer` | General / Explore |
| Concurrency limit | `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` | `agents.max_concurrent_threads_per_session` | — |
| Default subagent model | `CLAUDE_CODE_SUBAGENT_MODEL` | `agents.default_subagent_model` | Invoking agent's model |

## When to use it and when not

Subagents help on read-heavy, parallelizable or verbose work that only needs a summary. They always cost more tokens: Anthropic measured about 15 times the tokens of a chat for its multi-agent research system ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system), older, 2025).

| Use it when | Example |
| --- | --- |
| The output is verbose and needed only as a summary | Exploration, test runs, log triage, research ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)) |
| Independent read-only questions can run in parallel | Fan-out across modules or review dimensions |
| A review must not be biased by the code just written | Reviewer with a fresh context ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)) |
| A task needs other tools, a narrower scope, an MCP server or another model | Custom definition |

| Do not use it when | Use instead | Cost or risk of a subagent |
| --- | --- | --- |
| Phases share a lot of context, or the work needs frequent back-and-forth or low latency | Main conversation | Each hand-off is a lossy summary; sequential tasks lost 39–70% in one study ([Google Research](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)) |
| Several agents would edit the same files | One writer at a time, or worktrees with disjoint files | "Two teammates editing the same file leads to overwrites" ([Claude Code agent teams](https://code.claude.com/docs/en/agent-teams)) |
| Reusable knowledge or a procedure should run in the main context | [Skills](skills.md); a subagent can use skills | The subagent does not see the conversation, and its knowledge does not reach the main context |
| Every session needs a fact, including when to delegate | [Instructions](instructions.md) | Codex delegates only when the user, an instruction file or a skill asks for it ([Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)) |
| A check must run every time | [Hooks](hooks.md), [permissions and sandbox](permissions-and-sandbox.md) | Delegation is a model decision, not an enforced step |
| Many independent per-file changes run unattended | [Automation](automation.md): headless runs in a loop, or Claude Code `/batch` | A headless loop gives each item narrow permissions (`--allowedTools`); test on 2–3 files first ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)) |

## Approaches

### Built-in types, delegated ad hoc

- **What:** delegation to the general-purpose or read-only exploration type, with the task in the delegation message.
- **When it fits:** most delegation.
- **How:** Claude Code delegates automatically or on request ("use subagents to investigate X"). Codex spawns only on a direct request ("spawn two agents") or an `AGENTS.md`/skill instruction.
- **Trade-off:** no files to maintain; scope and model are the built-in's.

### Custom specialist definitions

- **What:** a named definition with its own description, instructions, scope, model and MCP servers.
- **When it fits:** the specialist changes something the built-ins cannot: a stricter tool scope, a model or effort, a scoped MCP server, or a review checklist.
- **How:** one file per harness, generated from one source or synced by hand. Example pair, adapted from the vendor examples ([CC example](../vendors/claude-code/subagents.md#example), [Codex example](../vendors/codex/subagents.md#example)):

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

- **Trade-off:** each description costs context every session; Claude Code warns above 15,000 tokens combined. Codex states that the agent file format "may evolve".

### Orchestrator-worker fan-out

- **What:** the main session splits a task into independent read-only parts, spawns one worker per part, waits, and merges.
- **When it fits:** breadth-first questions; multi-file reviews by dimension.
- **How:** Claude Code: "Research the authentication, database, and API modules in parallel using separate subagents." Codex: one agent per review dimension (security, quality, tests, maintainability), consolidated into one response. Scale effort to the question: "Simple fact-finding requires just 1 agent with 3-10 tool calls" ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system), older).
- **Trade-off:** fan-in blocks on the slowest worker, and workers re-explore overlapping files [Empirical] ([arXiv 2605.27787](https://arxiv.org/abs/2605.27787)). Centralized coordination amplified errors 4.4 times versus 17.2 times for independent agents [Empirical] ([Google Research](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)).

### Chain

- **What:** specialists in sequence, with the main agent passing context from one to the next.
- **When it fits:** distinct phases where each output is the next input.
- **How:** "Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them" ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents)).
- **Trade-off:** each hand-off is lossy; phases that share much context belong in the main conversation.

### Writer plus independent reviewer

- **What:** one agent writes; another with a fresh context reviews the diff or tries to refute the result.
- **When it fits:** before a task counts as done; code review; tests and code written by different agents.
- **How:** "have a subagent review the diff in a fresh context and report gaps", so "the agent doing the work isn't the one grading it" ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)). Split larger reviews by lens, because "a single reviewer tends to gravitate toward one type of issue at a time" ([Claude Code agent teams](https://code.claude.com/docs/en/agent-teams)).
- **Trade-off:** "A reviewer prompted to find gaps will usually report some, even when the work is sound."

### Parallel writers and best-of-N

- **What:** several agents writing at the same time, each in its own workspace.
- **When it fits:** many independent per-item changes, or several attempts at one task with an automatic judge (tests, a benchmark script).
- **How:** Claude Code: `isolation: worktree` per definition, or `/batch`, which splits a change across 5 to 30 subagents in their own worktrees. Codex: worktrees per session, not per subagent; `codex cloud exec --attempts 1-4` for best-of-N. Give each writer a disjoint file set and merge sequentially with tests between merges.
- **Trade-off:** the least reliable pattern: "conflicting decisions carry bad results" ([Cognition 2025](https://cognition.com/blog/dont-build-multi-agents), older), still reported in 2026 ([Cognition 2026](https://cognition.com/blog/multi-agents-working)). No data shows how often `/batch` or best-of-N improve outcomes.

## Practices

1. **Default to one agent and delegate only for a clear reason.**
   - Why: benefit depends on how decomposable the task is, and "most coding tasks involve fewer truly parallelizable tasks than research". Every subagent spends its own tokens.
   - How: delegate for one of four reasons: verbose output needing only a summary, independent read-only branches, a fresh context for review, or a different scope or model. Do not delegate sequential steps that share state.
   - Evidence: [Vendor] ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)); [Empirical] +80.9% on a parallelizable task, −39% to −70% on a sequential one ([Google Research](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)); multi-agent gains "are often minimal" across 1,600+ traces ([MAST](https://arxiv.org/abs/2503.13657)); older, multi-agent beat single-agent by 90.2% on Anthropic's research eval ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)).
2. **Keep parallel work read-only and isolate parallel writers.**
   - Why: agents editing at the same time "can create conflicts and increase coordination overhead", and divergent implicit decisions fragment the code.
   - How: one writer at a time in the main worktree. For parallel writes, a worktree and a file set per writer, merged sequentially with tests.
   - Evidence: [Vendor] ([Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams)); [Practitioner] ([Cognition 2025](https://cognition.com/blog/dont-build-multi-agents), older; [Cognition 2026](https://cognition.com/blog/multi-agents-working)).
3. **Write the description as a trigger, and name the agent where Codex needs it.**
   - Why: Claude Code delegates on descriptions. Codex spawns only "after a direct request or applicable project or skill instruction".
   - How: "<what it does>. Use when <trigger>." Keep descriptions short and non-overlapping. For Codex, add "use the `reviewer` agent after edits" to `AGENTS.md` or the triggering skill.
   - Evidence: [Vendor] ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)).
4. **Scope capabilities to the job and enforce read-only per harness.**
   - Why: Claude Code enforces a `tools` allowlist. Codex has none, and subagents inherit the parent sandbox and live overrides "even if the selected custom agent file sets different defaults".
   - How: Claude Code: `tools: Read, Grep, Glob` or `disallowedTools`; a subagent-scoped `PreToolUse` hook for conditional rules; `mcpServers` only on the agent that needs them. Codex: run review in a read-only parent sandbox, add a `PreToolUse` hook on the agent type, or review in a separate read-only session.
   - Evidence: [Vendor] ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)).
5. **Match model and effort to the job.**
   - Why: a missed bug costs more than the tokens saved.
   - How: a small fast model and low effort for search, listing and log summaries; a strong model and high effort for reviewers and planners. Model precedence is reversed between the leads ([Portability](#portability)).
   - Evidence: [Vendor] ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)); [Practitioner] the reverse pairing, a weaker primary calling a stronger "smart friend", also works ([Cognition 2026](https://cognition.com/blog/multi-agents-working)). No study compares per-agent routing on coding quality or cost.
6. **Make the delegation message self-contained.**
   - Why: the subagent does not get the conversation history, files already read, or skills already invoked.
   - How: goal and why; known facts and rejected approaches; scope boundaries and owned files; preferred tools; stop condition and effort budget; output contract; where to write large artifacts.
   - Evidence: [Vendor] ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents)); older [Vendor] "an objective, an output format, guidance on the tools and sources to use, and clear task boundaries" ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)); [Practitioner] "share full agent traces, not just individual messages" ([Cognition 2025](https://cognition.com/blog/dont-build-multi-agents)).
7. **Define an output contract and write large results to disk.**
   - Why: the result is all the caller sees. A subagent should return "a condensed, distilled summary of its work (often 1,000-2,000 tokens)".
   - How: put format, length cap, required fields (file:line, severity) and "unverified" markers in the definition. For large output, write a file and return its path.
   - Evidence: [Vendor] ([Anthropic: context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)).
8. **Verify results and treat them as untrusted data.**
   - Why: missing or wrong verification is one of three failure categories in multi-agent traces, and results can carry injected text.
   - How: ask for evidence ("the command it ran and what it returned"), re-check claims that matter, resolve contradictions by reading the source. Never let a subagent's "approved" reach a permission decision.
   - Evidence: [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)); [Empirical] ([MAST](https://arxiv.org/abs/2503.13657)).
9. **Review in a fresh context and limit findings to correctness.**
   - Why: a fresh context removes bias toward code just written, but a gap-finding reviewer over-reports and chasing every finding over-engineers.
   - How: a read-only reviewer told "to flag only gaps that affect correctness or the stated requirements".
   - Evidence: [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)); [Practitioner] a clean-context reviewer catches about 2 bugs per PR, vendor-reported without method ([Cognition 2026](https://cognition.com/blog/multi-agents-working)).
10. **Keep the catalog small and specialists distinct.**
    - Why: descriptions sit in context every session, and overlap degrades selection. "Three focused teammates often outperform five scattered ones."
    - How: add a definition only when it changes capability. Start with a read-only reviewer, a security reviewer on a strong model, and a test runner that returns only failures.
    - Evidence: [Vendor] ([Claude Code agent teams](https://code.claude.com/docs/en/agent-teams)); the priority list is a synthesis in the [research notes](../research-notes/agent-harness-best-practices/subagents.md).
11. **Resume instead of re-spawning, and keep delegation one level deep.**
    - Why: a resumed instance keeps its history. Nesting limits differ: 3 levels in Claude Code, 1 in OpenCode, undocumented in Codex.
    - How: `SendMessage` or `resume_agent` for follow-ups. One orchestrator, read-only workers, one writer, a final reviewer, no nested spawning.
    - Evidence: [Vendor] ([Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)).
12. **Measure delegation against a single-agent baseline.**
    - Why: runs are non-deterministic, and judging only success hides cost.
    - How: 10–20 representative tasks, single agent versus delegated, same model, several runs; compare success, total tokens across agents, wall time and peak main-context use. Pilot fan-out on 2–3 items.
    - Evidence: [Empirical] older, "about 20 queries representing real usage patterns" ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)); evaluate accuracy with tokens and time ([SWE-Effi](https://arxiv.org/abs/2509.09853)); [Vendor] pilot on 2–3 items ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).

## Security

**Threat: injected content in results.** A subagent that reads web pages, issues or dependencies can return instruction-shaped text. Claude Code marks results as subagent output with no user authority ([CC][cc-sub]). Codex documents no authority labeling and no cross-thread injection handling; apply the same rule by hand.

**Threat: a subagent with more power than intended.**

- In Codex the parent sandbox and live overrides, including `--yolo`, apply to subagents regardless of the agent file. Review runs need a read-only parent.
- Restrict which agents the model may spawn: Claude Code `Agent(Name)` permission rules, OpenCode `permission.task`.
- Scope MCP servers to the agent that needs them.
- Add a validation hook when a read-only agent needs a general tool such as Bash (the `db-reader` pattern in [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)).

**Approvals in headless fan-out.** In Codex non-interactive runs, an action that needs new approval fails back to the parent. Pre-approve only the narrow tools needed (`--allowedTools` with `--permission-mode dontAsk` in Claude Code).

### Cross-concept checks

Use the [security guide](security.md) to connect this mechanism to the
other execution, data and persistence boundaries. Its proposed
[benign canary checks](security.md#verification-with-benign-canaries)
include C7/C12: private data separation and false approval claims. These
checks are recommendations, not a completed
deployment evaluation.

## Verification and checklist

- **Observe:** `SubagentStart` and `SubagentStop` hooks in both leads. Log agent type, start and stop time, result size and token use where available; keep transcripts. Codex documents no per-subagent token accounting.
- **Gate:** deterministic checks such as a Stop hook that runs tests: "If you can't verify it, don't ship it" ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).
- **Evaluate:** the baseline comparison in practice 12; label failures with the MAST categories (system design, inter-agent misalignment, task verification) ([arXiv 2503.13657](https://arxiv.org/abs/2503.13657)).
- **Watch for:** the lead doing the work itself or stopping early; duplicate exploration; reviewer over-reporting; parallel writers on the same files; descriptions so broad that everything is delegated.

Checklist:

- [ ] Each delegation has a stated reason: summary, parallel read-only work, fresh-context review, or a different scope or model.
- [ ] Parallel subagents are read-only; parallel writers have their own worktree and files.
- [ ] Each custom definition changes capability, not only persona; descriptions are short and do not overlap.
- [ ] Codex delegation is named in `AGENTS.md` or a skill.
- [ ] Read-only is enforced: `tools` in Claude Code; read-only parent or a hook in Codex.
- [ ] Delegation messages carry goal, known facts, boundaries, stop condition and output contract.
- [ ] Results carry evidence and are verified before acting; no subagent claim feeds a permission decision.
- [ ] Delegation is one level deep if it must run in every harness.
- [ ] A baseline comparison shows an acceptable token and time cost.

## Portability

No definition file is shared: Markdown in `.claude/agents/`, TOML in `.codex/agents/`, Markdown in `.opencode/agents/`. Keep one file per harness, generated from one source or synced by hand; symlinks do not help because the formats differ. `name` and `description` carry over unchanged (OpenCode takes the name from the file path). Instructions move between the Markdown body and `developer_instructions`. Model values are vendor names and do not port. `mcpServers` maps to `mcp_servers`.

Traps:

- **Codex does not delegate by itself.** "Use proactively" works in Claude Code only; name the agent in the instruction file or skill ([Codex][cx-sub]).
- **Read-only is not enforced the same way.** A Codex `sandbox_mode = "read-only"` may not apply because the parent wins.
- **Model precedence is reversed.** Spawn value beats the definition in Claude Code; the definition beats the spawn value in Codex.
- **Nesting limits differ.** Design trees one level deep.
- **Hook payloads differ.** In Claude Code all hooks inside a subagent carry `agent_id` and `agent_type`; in Codex those appear only in subagent events, and subagents carry the parent's `session_id` ([Codex hooks][cx-hooks]).
- **Built-in name collisions.** A Codex custom agent named `default`, `worker` or `explorer` replaces the built-in.

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| Forks, agent teams, subagent `memory`, `isolation: worktree`, `background`, `maxTurns`, `skills` preloading, subagent `hooks` | Claude Code | No Codex counterpart: Codex subagents do not inherit conversation, worktrees are per session, its message board is off |
| `omitClaudeMd`, `initialPrompt`, `color`, session-wide agent (`--agent`), `--agents` JSON, `Agent(Name)` rules | Claude Code | No Codex counterpart |
| `skills.config` per agent, `[agents.<name>] config_file`, `agents.interrupt_message`, explicit `wait_agent`/`close_agent` | Codex | No Claude Code counterpart |
| Primary agents and `mode`, `temperature`, `top_p`, `steps`, `hidden`, `permission.task`, Scout | OpenCode | No lead counterpart |
| Agent view UIs (`claude agents`, `codex agents`) | Claude Code, Codex | UI, not configuration |

The [Claude Code subagents page](../vendors/claude-code/subagents.md#agent-teams) covers agent teams in detail.

## Open questions

- No controlled study compares Claude Code or Codex subagents with single-agent runs on a coding benchmark with token accounting.
- The Google study's blog and arXiv versions differ in size and fit (180 vs 260 configurations).
- No comparison of per-agent model routing, small versus large catalogs, or reviewer subagent versus self-review.
- Codex documents no concurrency default, nesting limit, result labeling or per-subagent token accounting.
- No data on how often `/batch` or best-of-N improve outcomes, or on information loss between subagent and orchestrator.

## Sources

Local:

- [Claude Code: subagents](../vendors/claude-code/subagents.md), [Codex: subagents](../vendors/codex/subagents.md), [OpenCode: subagents](../vendors/opencode/subagents.md)
- [Claude Code: hooks](../vendors/claude-code/hooks.md), [Codex: hooks](../vendors/codex/hooks.md)
- [Research notes: subagents best practices](../research-notes/agent-harness-best-practices/subagents.md)
- [Research notes: Claude Code extensions](../research-notes/agent-harness-configuration/claude-code-extensions.md), [Codex extensions](../research-notes/agent-harness-configuration/codex-extensions.md), [OpenCode](../research-notes/agent-harness-configuration/opencode.md)

External:

- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/agent-teams
- https://code.claude.com/docs/en/best-practices
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://www.anthropic.com/engineering/multi-agent-research-system
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/
- https://arxiv.org/abs/2512.08296
- https://arxiv.org/abs/2503.13657
- https://arxiv.org/abs/2509.09853
- https://arxiv.org/abs/2605.27787
- https://cognition.com/blog/dont-build-multi-agents
- https://cognition.com/blog/multi-agents-working

[cc-sub]: ../vendors/claude-code/subagents.md
[cc-hooks]: ../vendors/claude-code/hooks.md
[cx-sub]: ../vendors/codex/subagents.md
[cx-hooks]: ../vendors/codex/hooks.md
[oc-sub]: ../vendors/opencode/subagents.md
