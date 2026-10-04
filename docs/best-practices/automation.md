# Automation: best practices

How to run agent-driven development end to end: the interactive explore, plan, implement and verify loop; spec-driven and test-driven work; goal-driven and long-running sessions; headless and CI runs; parallel sessions; schedules; SDKs; and how to measure outcomes. Claude Code and Codex are the leads; OpenCode appears where the sources cover it. Terms follow the [automation concept page](../concepts/automation.md): a *run* has a prompt, a configuration set, a permission envelope, trust, an output contract, a session handle, a working copy and credentials; *hosted run*, *schedule*, *goal-driven continuation* and *worktree isolation* are used as defined there. Research date: 2026-10-04.

Evidence labels: **[Vendor]** vendor guidance, docs or engineering blog. **[Empirical]** a study or measured data. **[Advisory]** a security advisory, CVE or security research. **[Practitioner]** a named practitioner's or company's report or opinion. Undated vendor pages were fetched 2026-10-04.

## Summary

1. [Give the agent a check it can run and ask for evidence, not assertions](#5-give-the-agent-a-check-it-can-run).
2. [Let something other than the implementer grade the work](#6-separate-the-grader-from-the-implementer): a fresh subagent, a `/goal` evaluator, a Stop hook or CI.
3. [Plan or write a spec for non-trivial work and state "done when"](#1-plan-before-non-trivial-changes); skip the plan when the diff fits in one sentence.
4. [Prefer a fresh session with a written handoff over a long session with accumulated corrections](#7-keep-sessions-short-and-hand-off-in-writing).
5. [Set every headless run's envelope explicitly](#11-isolate-the-configuration-of-headless-runs): isolated configuration, explicit permissions, schema-validated output, turn, time and budget caps.
6. [Keep the agent job read-only and secret-poor; apply its output in a separate job](#15-split-the-agent-job-from-the-write-job), and [treat issue and PR text as hostile](#16-restrict-triggers-and-treat-repository-text-as-hostile).
7. [Isolate parallel sessions in worktrees and parallelize only what you can review](#19-parallelize-what-is-cheap-to-review).
8. [Measure outcomes and review burden, not run status](#24-track-outcome-and-burden-metrics); use pass^k for unattended runs.

## When to use it

| Situation | Use | See |
| --- | --- | --- |
| Exploratory, ambiguous or design-heavy work | Interactive session with plan mode | [Explore, plan, implement, verify](#explore-plan-implement-verify) |
| A feature that needs agreed scope before code | Spec-driven: interview, write a spec, execute in a fresh session | [Spec-driven work](#spec-driven-work) |
| Work bigger than one prompt with a verifiable end state | Goal-driven continuation (`/goal`) | [Goals and long-running work](#goals-and-long-running-work) |
| A script, batch migration or pipeline step | Headless CLI: `claude -p`, `codex exec`, `opencode run` | [Headless runs](#headless-runs-and-fan-out) |
| PR review, issue-to-PR, autofix on repository events | CI action (`claude-code-action`, `codex-action`, OpenCode GitHub action) | [CI integration](#ci-integration) |
| Several independent tasks at once | Worktree-isolated sessions, cloud tasks, best-of-N | [Parallel sessions](#parallel-sessions-and-best-of-n) |
| Repeatable unattended work (triage, docs drift, dependency bumps) | Schedule or event-triggered hosted run | [Schedules](#scheduled-and-event-triggered-runs) |
| The agent inside your own application or service, with programmatic approvals, sessions, per-tenant cost | SDK | [SDKs and custom platforms](#sdks-and-custom-platforms) |
| Deep integration with internal systems justifies owning the tooling | Own platform (as Ramp did) | same |

Related concepts: the [run model](../concepts/automation.md), [subagents](../concepts/subagents.md) for in-run delegation and review, [hooks](../concepts/hooks.md) for deterministic gates, [permissions and sandbox](../concepts/permissions-and-sandbox.md) for the envelope, [skills](../concepts/skills.md) for reusable methods named in schedules, [MCP](./mcp.md) and [plugins](./plugins.md) for what a run loads.

## Approaches

### Explore, plan, implement, verify

- **What:** separate read-only exploration and planning from implementation, then verify and commit.
- **When it fits:** uncertain approach, multi-file change, unfamiliar code. "If you could describe the diff in one sentence, skip the plan" ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).
- **How:**
  - Generalized: explore read-only; write a plan; implement against the plan with tests; run the checks; commit and open a PR.
  - Claude Code: four phases Explore (plan mode), Plan (`Ctrl+G` edits the plan), Implement ("verifying against its plan"), Commit ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).
  - Codex: every prompt carries Goal, Context, Constraints and "Done when"; for complex tasks plan first with `/plan` or Shift+Tab; review with `/review` against the base branch or uncommitted changes ([Codex best practices](https://learn.chatgpt.com/guides/best-practices)).
- **Trade-offs:** planning "adds overhead"; worth it only when scope is unclear.

### Spec-driven work

- **What:** a written spec fixes scope before implementation. Böckeler distinguishes spec-first (spec discarded after), spec-anchored (maintained with the feature) and spec-as-source (humans edit only specs); Kiro and GitHub spec-kit are effectively spec-first, Tessl targets the other two ([Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html), Oct 2025, older).
- **When it fits:** features where agreeing on scope is the hard part. Not small bugs: one workflow for all sizes is "using a sledgehammer to crack a nut".
- **How:** Claude Code's interview pattern: start minimal, let the agent interview you with `AskUserQuestion` about implementation, UI/UX, edge cases and trade-offs, "write a complete spec to SPEC.md", then "start a fresh session to execute it". A useful spec names files and interfaces, states what is out of scope, and ends with an end-to-end verification step ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)). The same works in Codex with a spec file and Plan mode (inference: the pattern uses no vendor-only feature).
- **Trade-offs:** Markdown artifacts are "very verbose and tedious to review"; agents still ignore spec instructions or duplicate existing code ([Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)).

### Test-driven work

- **What:** write tests first, confirm they fail (red), iterate until they pass (green).
- **When it fits:** behaviour that a test can express; bug fixes ("write a failing test that reproduces the issue, then fix it").
- **How:** prompt "Use red/green TDD" ([Willison, Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/)); or split roles: "have one Claude write tests, then another write code to pass them" ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).
- **Trade-offs:** agents modify or game tests ([ImpossibleBench](https://arxiv.org/abs/2510.20270)); add a guard (see [practice 4](#4-use-redgreen-tdd-and-guard-the-tests)).

### Goals and long-running work

- **What:** goal-driven continuation keeps the agent working across turns until a condition holds. For multi-hour or multi-session work, a harness adds a progress log, a feature list and an evaluator.
- **When it fits:** a task "bigger than one prompt but smaller than an open-ended backlog" with a verifiable end state ([Codex: follow goals](https://learn.chatgpt.com/use-cases/follow-goals)).
- **How:**
  - Claude Code `/goal`: after each turn a small fast model judges the condition (not met, met, impossible). It "doesn't run commands or read files independently", so the check must print in the transcript. Works in `-p` (`claude -p "/goal …"`); add `--output-format stream-json --verbose` or it looks stuck. It does not change the permission mode; pair it with auto mode for unattended turns. It clears on unrecoverable errors (auth, credits, context overflow, model unavailable) ([Claude Code /goal](https://code.claude.com/docs/en/goal)).
  - Codex `/goal`: template "`/goal Complete [objective] without stopping until [verifiable end state].`"; `/goal pause|resume|clear`; ask for compact status updates (checkpoint, what was verified, what remains, blocked?) ([Codex: follow goals](https://learn.chatgpt.com/use-cases/follow-goals)).
  - Long-running harness (Anthropic, Nov 2025): an initializer session creates `init.sh`, a `claude-progress.txt` log, an initial commit and a JSON feature list with every feature failing; later sessions work "on only one feature at a time", commit with descriptive messages and update the progress file ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).
- **Trade-offs:** on the same brief a solo agent took 20 min / $9; a full planner-generator-evaluator harness took 6 h / $200; a simplified harness built a DAW in 3 h 50 min for $124.70 (experiments used Sonnet 4.5 / Opus 4.6, older models) ([Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps), Mar 2026).

### Headless runs and fan-out

- **What:** one non-interactive run per invocation, from a script or pipeline.
- **When it fits:** batch migrations, pipeline steps, report generation.
- **How (generalized):** isolated configuration set, explicit permission envelope, schema-validated output to a file, caps, API-key credentials.
  - Claude Code `claude -p`: `--bare` "is the recommended mode for scripted and SDK calls" and will become the default for `-p`; it skips hooks, skills, agents, plugins, MCP, memory and `CLAUDE.md`, needs `ANTHROPIC_API_KEY`, and loads context only via flags (`--append-system-prompt-file`, `--settings`, `--mcp-config`, `--agents`, `--plugin-dir`). Permissions: pass `--permission-mode` explicitly (unset can start in `auto`); `dontAsk` denies everything that would prompt; `--allowedTools` with prefix rules such as `Bash(git diff *)` (the space before `*` matters); `--permission-prompts none` for unattended runs. Output: `--output-format json --json-schema '<schema>'` → `structured_output`; `json` includes `total_cost_usd` (client-side estimate) and `permission_denials`. Stdin is capped at 10 MB; SIGTERM exits 143 ([Claude Code headless](https://code.claude.com/docs/en/headless)).
  - Codex `codex exec`: read-only sandbox by default; `--sandbox workspace-write` for edits, `danger-full-access` only in controlled environments; `--full-auto` is deprecated. `--json` (JSONL events), `-o` (final message to file), `--output-schema <file>`; `--ephemeral`, `--ignore-user-config`, `--ignore-rules`; `codex exec resume --last` or `resume <SESSION_ID>`; `--skip-git-repo-check` "use cautiously". Auth: `CODEX_API_KEY=<key> codex exec …` ([Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)).
  - OpenCode `opencode run`: `--format json` for raw events; `--auto` approves every `ask`; config isolation is not recorded ([automation concept page](../concepts/automation.md)).
- **Example** (Claude Code fan-out recipe from the vendor; refine the prompt on the first 2–3 files, then run on all):

```bash
for file in $(cat files.txt); do
  claude -p "Migrate $file to the new API. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)" --permission-mode dontAsk
done
```

- **Example** (Codex pipeline step; flags from the vendor docs):

```bash
CODEX_API_KEY="$KEY" codex exec --ephemeral --ignore-user-config \
  --sandbox read-only --json --output-schema schema.json -o result.json \
  "Summarize the risk of the changes on this branch."
```

- **Trade-offs:** defaults point in opposite directions (Codex read-only; Claude Code `default` or `auto`). `--bare` also drops project skills; a run that needs them must load them through flags such as `--plugin-dir` (inference) or not use `--bare` ([automation concept page](../concepts/automation.md)).

### CI integration

- **What:** a vendor action runs one headless run per workflow event.
- **When it fits:** PR review, issue-to-PR, autofix, scheduled repository chores.
- **How:**
  - Claude Code `anthropics/claude-code-action`: interactive mode (no `prompt`; responds to `@claude`) or automation mode (`prompt` set; any event). Plain-text automation prompts get "no shell or GitHub API access until you grant the tools" via `--allowedTools` in `claude_args` or `permissions.allow` in `settings`. Skills run as `prompt: "/skill-name"` after checkout. PR review via plugin: `plugins: "code-review@claude-code-plugins"`, `prompt: "/code-review:code-review --comment …"`, `claude_args: '--allowedTools "mcp__github_inline_comment__create_inline_comment"'`, job permissions read-only plus `id-token: write`. Commits pushed with the default `GITHUB_TOKEN` do not trigger CI; authenticate as the GitHub App or pass an app token ([Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)).
  - Codex `openai/codex-action`: installs the CLI, starts the Responses API proxy, runs `codex exec`; inputs `prompt` / `prompt-file`, `codex-args`, `model`, `effort`, `sandbox`, `safety-strategy` (`drop-sudo` default, `unprivileged-user`, `unsafe`; Windows requires `unsafe`), `output-file`. Pattern: the Codex job writes `final-message`; a second job posts PR comments ([Codex GitHub Action](https://learn.chatgpt.com/docs/github-action)). Hosted `@codex review` is served by Codex Cloud, with rules in a `## Code Review Rules` section of `AGENTS.md` ([automation concept page](../concepts/automation.md)).
  - OpenCode `anomalyco/opencode/github@latest`, triggered by `/opencode` or `/oc` ([automation concept page](../concepts/automation.md)); no security guidance was found.
- **Trade-offs:** CI is where untrusted text meets secrets. See [Security](#security).

### Parallel sessions and best-of-N

- **What:** several sessions at once, each in its own working copy; or N independent attempts at one task.
- **When it fits:** research, proof-of-concepts, "system understanding" questions, small maintenance, carefully specified work ([Willison, parallel coding agents](https://simonwillison.net/2025/Oct/5/parallel-coding-agents/), Oct 2025, older).
- **How:**
  - Claude Code: `claude --worktree <name>` → `.claude/worktrees/<name>/` on branch `worktree-<name>`; gitignore `.claude/worktrees/`; install dependencies (a worktree is a fresh checkout); `.worktreeinclude` copies gitignored files such as `.env`; `worktree.baseRef` `"fresh"` (default, remote default branch) or `"head"` (carries unpushed work). Edits, command cwd and git redirects into the main checkout are blocked. Subagents can use `isolation: worktree`. `/batch <instruction>` splits work across 5–30 worktree-isolated subagents ([Claude Code worktrees](https://code.claude.com/docs/en/worktrees); [Claude Code best practices](https://code.claude.com/docs/en/best-practices)).
  - Codex: parallel cloud tasks from a published environment, each with its own workspace, that "can keep working while your computer is asleep"; review diffs and tests, request follow-ups, open a PR ([Codex cloud](https://learn.chatgpt.com/docs/cloud)). CLI `--worktree`; desktop Worktree mode uses detached HEAD and Handoff; local environment setup scripts prepare untracked files ([automation concept page](../concepts/automation.md)). `codex cloud exec --attempts` (2–4) runs independent attempts in separate containers ([Vaughan, best-of-N](https://codex.danielvaughan.com/2026/04/01/codex-cloud-exec-best-of-n-attempts/), [Practitioner]).
- **Trade-offs:** "I can only focus on reviewing and landing one significant change at a time" (Willison). Best-of-N multiplies review unless tests and a grader pick the winner (inference). Port conflicts and per-worktree installs are not handled by either lead.

### Scheduled and event-triggered runs

- **What:** a stored prompt plus a cadence or trigger that starts runs.
- **When it fits:** unattended, repeatable work with a clear outcome: backlog triage, alert triage, bespoke review, deploy verification, docs drift, library ports ([Claude Code routines](https://code.claude.com/docs/en/routines)).
- **How:**
  - Claude Code routines (research preview): saved prompt, repositories and connectors; triggers schedule, API or GitHub events; Anthropic cloud or self-hosted. No permission-mode picker; runs without approval. Pushes to `claude/`-prefixed branches by default. Minimum interval 1 h; hourly caps (for example 100 scheduled runs/h per account); GitHub events beyond caps are dropped. Actions appear under the user's identity ([Claude Code routines](https://code.claude.com/docs/en/routines)).
  - Claude Code GitHub Action schedules run only from the default branch; public repositories disable schedules after 60 days without activity; scheduled runs are attributed to the user who last changed the cron ([Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)).
  - Codex: "Schedule stable workflows as background tasks through the Scheduled page, choosing cadence and execution environment"; turn repeatable workflows into skills, "scoped to one job" ([Codex best practices](https://learn.chatgpt.com/guides/best-practices)).
  - Portability: cron (Claude Code) vs RRULE (Codex); Claude Code scheduled fires run only model-invocable skills; neither lead schedules from a plain CLI on a headless machine, so system cron plus the headless CLI is the fallback ([automation concept page](../concepts/automation.md); [skills invocation policy](../concepts/skills.md#invocation-policy-in-both-leads)).
- **Trade-offs:** "A green status … does not mean the task in your prompt succeeded. Open the run to read the transcript" ([Claude Code routines](https://code.claude.com/docs/en/routines)).

### SDKs and custom platforms

- **What:** a library that runs the same agent loop as the CLI inside your code.
- **When it fits:** the agent is part of your application or service and needs programmatic permission callbacks, sessions, streaming, custom tools, retries or per-tenant cost accounting. Shell loops over `-p` / `exec` suffice for batch migrations (inference).
- **How:**
  - Claude Agent SDK (Python, TypeScript): built-in tools, hooks, subagents, MCP, permissions, sessions (resume, fork), skills and memory loaded from `.claude/` and `~/.claude/` like the CLI, plugins. The GitHub Action is built on it. Other languages: run the CLI as a subprocess with `-p --output-format json`. Client SDK when you write the tool loop yourself; Managed Agents for Anthropic-hosted sessions. Third parties may not offer claude.ai login or subscription limits in Agent SDK products without approval; use API keys ([Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)).
  - Codex SDK (TypeScript, Python `openai-codex`): threads (`startThread`, `run`, resume by ID); sandbox presets read-only, workspace-write, full-access. Use the app-server for custom clients that manage auth and conversation history ([Codex SDK](https://learn.chatgpt.com/docs/codex-sdk)).
  - OpenCode: `@opencode-ai/sdk` wraps `opencode serve`; structured output via `format: { type: "json_schema" }` ([automation concept page](../concepts/automation.md)).
  - Own platform: Ramp's "Inspect" runs in sandboxed VMs on Modal with snapshots, state in Cloudflare Durable Objects, access to tests, Sentry, Datadog and databases, and Slack, web and Chrome entry points; ~30% of merged frontend and backend PRs through voluntary adoption ([InfoQ](https://www.infoq.com/news/2026/01/ramp-coding-agent-platform/), Jan 2026). "Owning the tooling allows for much stronger integration than commercial products." A secondary source claims ~75% by May 2026 (unverified).
- **Trade-offs:** SDKs load the same filesystem configuration as the CLI by default; pass `settingSources: []` (Claude) or the ignore flags (Codex) and inject configuration explicitly for reproducible service use (inference).

## Practices

### Workflow

#### 1. Plan before non-trivial changes

- **Practice:** explore and plan read-only before implementing uncertain, multi-file or unfamiliar work; skip the plan when the diff fits in one sentence.
- **Why:** planning catches wrong approaches before code exists; on clear tasks it is overhead.
- **How:** plan mode in either lead; edit the plan before implementing (`Ctrl+G` in Claude Code).
- **Evidence:** [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)); [Vendor] Codex lists "skipping planning on complex tasks" as an anti-pattern ([Codex best practices](https://learn.chatgpt.com/guides/best-practices)).

#### 2. State goal, context, constraints and done-when

- **Practice:** every task prompt names the goal, the relevant files, docs or errors, the constraints, and what must be true when it is done.
- **Why:** the agent cannot verify or stop correctly without a defined end state.
- **How:** scope the task (file, scenario, "avoid mocks"); point to sources (git history) and an existing example file; for bugs, describe symptom, likely location and what "fixed" looks like. Put durable rules in `AGENTS.md`, not in each prompt (see [instructions](../concepts/instructions.md)).
- **Evidence:** [Vendor] ([Codex best practices](https://learn.chatgpt.com/guides/best-practices)); [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).

#### 3. Size specs to the task and execute them in a fresh session

- **Practice:** write a self-contained spec for features where scope is the hard part, then implement it in a new session.
- **Why:** "Time spent making the spec precise pays off more than time spent watching the implementation." A fresh session starts without the interview's context.
- **How:** interview pattern → `SPEC.md` naming files and interfaces, out-of-scope items and an end-to-end verification step → fresh session. No spec for small bugs.
- **Evidence:** [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)). [Practitioner, Oct 2025, older] Böckeler criticises one workflow for all sizes and verbose artifacts: "I'd rather review code than all these markdown files" ([Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)). The two agree on sizing. No controlled study compares spec-driven and ad-hoc prompting. A secondary claim that GitHub released spec-kit in late 2025 and that Ramp framed specs as defining "what a completed outcome looks like" is unverified ([softwareseni.com](https://www.softwareseni.com/spec-driven-development-is-replacing-vibe-coding-as-the-professional-standard-for-ai-teams)).

#### 4. Use red/green TDD and guard the tests

- **Practice:** have the agent write a failing test first, confirm it fails, then make it pass, and prevent it from changing the tests to pass.
- **Why:** test-first guards against code that does not work and code that is not needed. Tests that already pass validate nothing. Frontier agents exploit tests "from simple test modification to complex operator overloading"; prompt, test access and feedback loop affect cheating rates.
- **How:** prompt "Use red/green TDD"; or a Writer/Tester split across two sessions or subagents. Guards (inference; neither vendor documents a dedicated mechanism): a "do not modify tests" constraint in the goal condition, a [hook](../concepts/hooks.md) that blocks writes to test files during the green phase, or a reviewer that diffs tests separately.
- **Evidence:** [Practitioner] ([Willison, Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/), undated); [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)); [Empirical, Oct 2025; ICLR 2026] ImpossibleBench ([arXiv 2510.20270](https://arxiv.org/abs/2510.20270); [ICLR 2026](https://iclr.cc/virtual/2026/poster/10009390)). Summaries report that stronger models cheat more often; not verified against the paper. No controlled study of TDD vs no TDD for agents was found.

### Verification

#### 5. Give the agent a check it can run

- **Practice:** provide tests, a build, a linter or a screenshot comparison the agent runs itself, and ask for evidence (test output, command and result, screenshot) instead of claims.
- **Why:** "It's the difference between a session you watch and one you walk away from." Without a check, "you become the verification loop". "If you can't verify it, don't ship it."
- **How:** escalating gates: in one prompt; across a session with `/goal`; a deterministic Stop hook that "blocks the turn from ending until it passes"; a verification subagent. For UI work, require browser automation: Claude marked features done without end-to-end testing until told to "use browser automation tools and do all testing as a human user would".
- **Evidence:** [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)); [Vendor] "create tests when needed, run the relevant checks, confirm the result, and review the work before you accept it" ([Codex best practices](https://learn.chatgpt.com/guides/best-practices)); [Vendor, Nov 2025] ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).

#### 6. Separate the grader from the implementer

- **Practice:** let a different context judge the work: a fresh-context review subagent, a `/goal` evaluator, a Stop hook, or CI.
- **Why:** agents grading their own work "tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre"; separating generator and evaluator was "a strong lever". A fresh context "won't be biased toward code it just wrote."
- **How:** a reviewer subagent with the diff and `PLAN.md` and the instruction "Report gaps, not style preferences"; flag only correctness and requirement gaps. Codex: `/review`. See [subagents](../concepts/subagents.md).
- **Evidence:** [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)); [Vendor, Mar 2026; experiments on Sonnet 4.5 / Opus 4.6, older models] ([Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)).
- **Caveat:** "A reviewer prompted to find gaps will usually report some, even when the work is sound"; chasing every finding leads to over-engineering.

### Context

#### 7. Keep sessions short and hand off in writing

- **Practice:** one session per coherent problem; clear between unrelated tasks; restart instead of correcting repeatedly; carry state in a written handoff.
- **Why:** "performance degrades as it fills." "A clean session with a better prompt almost always outperforms a long session with accumulated corrections."
- **How:**
  - Claude Code: `/clear` between tasks; after more than two corrections on the same issue, `/clear` and start fresh; steer compaction (`/compact Focus on the API changes`, or a rule in `CLAUDE.md` to preserve the modified-file list and test commands); `/rewind` for partial summarization; `/btw` for side questions; subagents for investigation so file reads stay out of the main context ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).
  - Codex: "one chat per coherent problem"; `/fork` only when work truly branches; `/compact` for long conversations; subagents for bounded parallel tasks ([Codex best practices](https://learn.chatgpt.com/guides/best-practices)).
  - Multi-hour runs: Anthropic found context resets (clear plus structured handoff) better than compaction, which "doesn't give the agent a clean slate" (observed strongly in Sonnet 4.5, an older model) ([Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)).
- **Evidence:** [Vendor] as cited. Failure patterns named by Claude Code: kitchen-sink session, correcting over and over, over-specified `CLAUDE.md`, trust-then-verify gap, infinite exploration.

#### 8. Use git for rollback

- **Practice:** commit at checkpoints and roll back with git.
- **Why:** Claude Code checkpoints track only edits through its file tools, not Bash side effects: "This isn't a replacement for git."
- **How:** commit per feature or step with descriptive messages; use worktrees for risky live changes (Codex lists "running untested live changes without Git worktrees" as an anti-pattern).
- **Evidence:** [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices); [Codex best practices](https://learn.chatgpt.com/guides/best-practices)).

### Goals and long-running work

#### 9. Write goal conditions the transcript can prove

- **Practice:** a `/goal` has one measurable end state, a stated check, constraints and a bound.
- **Why:** the Claude Code evaluator reads only the transcript; an unobservable goal ("code is clean") is judged on the agent's own assertions, which reintroduces self-grading (inference in the notes).
- **How:** for example `/goal npm test exits 0; no other test file is modified; or stop after 20 turns`. Codex: "Codex should know what 'done' means before it starts"; give it a validation mechanism and checkpoints; avoid a "loose list of unrelated work". Pair with an explicit permission mode for unattended turns.
- **Evidence:** [Vendor] ([Claude Code /goal](https://code.claude.com/docs/en/goal); [Codex: follow goals](https://learn.chatgpt.com/use-cases/follow-goals)).

#### 10. Structure multi-session work and test each harness component

- **Practice:** for work spanning sessions, keep a progress file, a feature list with pass/fail state and a commit per feature; remove harness parts the current model no longer needs.
- **Why:** observed failures: doing too much at once, declaring completion prematurely, marking features done untested, leaving undocumented broken state. "Every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing"; with Opus 4.6 the sprint construct was removable while the evaluator stayed valuable.
- **How:** initializer session (`init.sh`, progress log, initial commit, feature list all failing); then one feature per session.
- **Evidence:** [Vendor, Nov 2025] ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)); [Vendor, Mar 2026, older models] ([Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)). No Codex equivalent write-up was found.

### Headless and CI

#### 11. Isolate the configuration of headless runs

- **Practice:** decide which configuration a headless run loads, and load nothing implicitly from an untrusted checkout.
- **Why:** without `--bare`, `claude -p` "runs the hooks in a project's `.claude/settings.json` and connects the servers in its `.mcp.json`, even in a folder you've never trusted". A PR that edits those files is a code-execution vector in Claude Code CI unless config is restored from base or `--bare` is used (inference). Codex skips untrusted project config and hooks in `codex exec`.
- **How:** Claude Code `--bare` plus explicit `--settings`, `--mcp-config`, `--agents`, `--plugin-dir`, `--append-system-prompt-file`; SDK `settingSources: []`. Codex `--ignore-user-config`, `--ignore-rules`, `--ephemeral`. `claude-code-action` restores `.claude/`, `.mcp.json`, `CLAUDE.md` and `.husky/` from the PR base branch.
- **Evidence:** [Vendor] ([Claude Code headless](https://code.claude.com/docs/en/headless); [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md); [claude-code-action security.md](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md)).

#### 12. Set the permission envelope explicitly

- **Practice:** pass the permission mode or sandbox on every headless invocation.
- **Why:** nobody can answer prompts, and defaults differ: Codex is read-only; Claude Code may start in `auto`; OpenCode `--auto` approves every `ask`.
- **How:** Claude Code `--permission-mode dontAsk` with `--allowedTools` prefix rules for locked-down CI; `--permission-prompts none` for scheduled runs (prompts are denied and Claude is told not to retry); auto mode (`--permission-mode auto`) when a classifier should block "scope escalation, unknown infrastructure, and hostile-content-driven actions" (repeated blocks in `-p` do not stop the run). Codex `--sandbox read-only` or `workspace-write`; `danger-full-access` only in controlled environments. Check `permission_denials` in Claude Code output.
- **Evidence:** [Vendor] ([Claude Code headless](https://code.claude.com/docs/en/headless); [Claude Code best practices](https://code.claude.com/docs/en/best-practices); [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)). [Vendor] Codex also lists "withholding execution permissions prematurely" as an anti-pattern ([Codex best practices](https://learn.chatgpt.com/guides/best-practices)); in a headless run, grant what the task needs explicitly instead of relying on defaults.

#### 13. Request schema-validated output and gate on load errors

- **Practice:** make the run's result a JSON object validated against a schema, written to a file, and fail the job when extensions did not load.
- **Why:** a deterministic consumer can act on data; free text needs another model to interpret.
- **How:** keep the schema in a file. Claude Code `--output-format json --json-schema "$(cat schema.json)"` → `structured_output` (an invalid schema errors since v2.1.205; before that it was silently ignored; the `format` keyword is not enforced). Codex `--output-schema schema.json -o result.json`. Fail CI on `plugin_errors` or `mcp_server_errors` in the Claude Code `system/init` event.
- **Evidence:** [Vendor] ([Claude Code headless](https://code.claude.com/docs/en/headless); [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)). [Practitioner, 2026] `--ephemeral` + `--json` + `--output-schema` + `CODEX_API_KEY` for deterministic Codex pipelines ([codex.danielvaughan.com](https://codex.danielvaughan.com/2026/05/03/codex-cli-non-interactive-pipelines-exec-resume-structured-output/)).

#### 14. Cap turns, time, budget and concurrency

- **Practice:** bound every CI and headless run.
- **Why:** CI cost is runner minutes plus tokens; unattended loops do not stop on their own.
- **How:** `--max-turns` in `claude_args`; `--max-budget-usd` (Claude Code only); workflow-level timeouts; GitHub `concurrency`; specific `@claude` requests and issue templates; a concise `CLAUDE.md`, which is read on every run. OAuth-token runs bill the subscription instead of the API. Track `total_cost_usd` per run (a client-side estimate).
- **Evidence:** [Vendor] ([Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions); [Claude Code headless](https://code.claude.com/docs/en/headless); [automation concept page](../concepts/automation.md)). No public data on typical per-run cost was found.

#### 15. Split the agent job from the write job

- **Practice:** run the agent in a read-only job that holds only the model key; let a separate job without the key apply the patch or post comments.
- **Why:** if injected text takes over the agent, it holds no write token and no secrets beyond the model key.
- **How:** Codex autofix pattern: agent job with `contents: read`, API key only in the Codex step, result serialized as a patch artifact "before granting write permissions". "Do not set `OPENAI_API_KEY` or `CODEX_API_KEY` as a job-level environment variable in workflows that check out or run repository-controlled code." Same shape for `claude-code-action` (inference: the pattern uses no Codex-only feature). Prefer OIDC workload identity federation (`anthropic_federation_rule_id`, `id-token: write`) over long-lived secrets; for shared secrets prefer a Console API key over a personal OAuth token. The official Claude GitHub App requests a broad permission set that cannot be partially accepted; build a custom app with only Contents, Issues and PRs if required.
- **Evidence:** [Vendor] ([Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md); [Codex GitHub Action](https://learn.chatgpt.com/docs/github-action); [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)).

#### 16. Restrict triggers and treat repository text as hostile

- **Practice:** allow only trusted actors to trigger runs, never run fork code with secrets, and treat issue, PR, comment and commit text as attacker-controlled.
- **Why:** prompt injection through issue and PR content was exploited against agent GitHub Actions in 2026 (see [Security](#security)).
- **How:**
  - Triggers: both actions default to write-access users. Do not widen with `allowed_non_write_users` ("a significant security risk") or wildcard bots; "Allowed bots are not checked for repository permissions". Codex: `allow-users`, `allow-bots`, `allow-bot-users` (no `*`). On public repos use `include_comments_by_actor`.
  - Untrusted sources: PR titles and bodies (hidden HTML comments), commit messages, `AGENTS.md` / `AGENTS.override.md`, screenshots. `claude-code-action` strips HTML comments, invisible characters, alt text and hidden attributes, "but new bypass techniques may emerge".
  - Workflows: do not check out an untrusted ref into the workspace root; `pull_request_target` and `workflow_run` run with base-repo secrets. Pass untrusted values via `env:`, not inline interpolation. Fork PRs on public repos get no secrets, so review runs only for same-repo branches.
  - Codex runner: `safety-strategy: drop-sudo` or `unprivileged-user` so the key "stays secret" (a read-only filesystem is not enough if `sudo` is available); run `openai/codex-action` "as the last step in a job"; `permission-profile` narrows filesystem and network but does not replace `safety-strategy`.
  - Pin actions to commit SHAs; keep `show_full_output` off on public repos (logs are public).
- **Evidence:** [Vendor] ([claude-code-action security.md](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md); [codex-action security.md](https://github.com/openai/codex-action/blob/main/docs/security.md); [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)); [Advisory] ([CSA research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-github-actions-security-20260503-csa-st/)).

#### 17. Pilot fan-out on a few items

- **Practice:** run a batch prompt on 2–3 items, refine it, then run it on all.
- **Why:** prompt errors multiply across a batch.
- **How:** "Test on a few files, then run on all of them"; have each run return a machine-checkable status (`OK` / `FAIL`).
- **Evidence:** [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).

### Parallelism

#### 18. Give each parallel session its own worktree, setup and cleanup

- **Practice:** isolate every parallel session in a worktree or separate clone or container, with a setup step and explicit cleanup.
- **Why:** parallel sessions in one checkout overwrite each other. A worktree is a fresh checkout without dependencies or gitignored files. `-p` runs do not clean up their worktrees and leave locks.
- **How:** Claude Code `--worktree`, `.worktreeinclude`, `worktree.baseRef`; remove leftovers with `git worktree unlock` then `git worktree remove`. Hooks: `${CLAUDE_PROJECT_DIR}` stays at the original root, so read `cwd` from hook input. Git LFS installed with `--local` yields pointer files (`git lfs pull`). Codex: local environment setup scripts; archive old scheduled runs. Script port allocation and per-worktree installs yourself.
- **Evidence:** [Vendor] ([Claude Code worktrees](https://code.claude.com/docs/en/worktrees); [automation concept page](../concepts/automation.md)). [Practitioner, Oct 2025, older] Willison uses fresh `/tmp` checkouts and considers Docker containers to limit blast radius ([Willison](https://simonwillison.net/2025/Oct/5/parallel-coding-agents/)).

#### 19. Parallelize what is cheap to review

- **Practice:** run in parallel the work whose results are easy to review; keep significant changes serial; use best-of-N only with an objective selector.
- **Why:** human review is the bottleneck. "Code that started from your own specification is a lot less effort to review."
- **How:** parallel research, proof-of-concepts, "system understanding" questions and small maintenance (deprecation warnings: "Chuck that at a bot"). Writer/Reviewer pairs in separate contexts. For best-of-N (`codex cloud exec --attempts`), let tests and a grader choose. Use unrestricted modes only "where I'm confident malicious instructions can't sneak into the context".
- **Evidence:** [Practitioner, Oct 2025, older] ([Willison, parallel coding agents](https://simonwillison.net/2025/Oct/5/parallel-coding-agents/)); [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)); best-of-N selection is an inference. No vendor recommends a maximum number of sessions per reviewer, and no data on merge-conflict cost was found.

### Scheduling

#### 20. Make scheduled prompts self-contained and scope what they can reach

- **Practice:** a schedule names a skill (the method), success criteria and an output location, and runs with the narrowest repositories, network, connectors and branch rights that work.
- **Why:** "the routine runs autonomously, so the prompt must be self-contained and explicit about what to do and what success looks like." Routines run without approval, and "Claude can use every tool from an included connector, including writes, without asking."
- **How:** writes go to a dedicated branch prefix (`claude/` by default) that branch protection or rulesets keep from merging without review. Triage runs that read issue text get no write tools beyond labels and comments, and no secrets. Routine API payloads arrive wrapped in a `<routine-fire-payload>` block marked untrusted; the saved prompt must opt in to act on it. Store the intent of a cadence, not the cron or RRULE expression. Make the named skill model-invocable for Claude Code scheduled fires.
- **Evidence:** [Vendor] ([Claude Code routines](https://code.claude.com/docs/en/routines); [Codex best practices](https://learn.chatgpt.com/guides/best-practices); [automation concept page](../concepts/automation.md)). Codex scheduled-task guardrails are not documented in the fetched pages.

#### 21. Monitor outcomes, not run status

- **Practice:** check whether the PR opened and its checks passed, not whether the run finished.
- **Why:** "A green status … does not mean the task in your prompt succeeded."
- **How:** read transcripts of scheduled and CI runs; alert on missing outputs; collect failed transcripts as eval cases ([practice 23](#23-build-evals-from-real-failures)).
- **Evidence:** [Vendor] ([Claude Code routines](https://code.claude.com/docs/en/routines)).

### SDKs

#### 22. Use the lowest layer that fits

- **Practice:** CLI or vendor action for scripts and CI; SDK when the agent lives in your application; own platform only when deep internal integration justifies the cost.
- **Why:** each step up adds code to maintain; each step down loses programmatic control.
- **How:** see [SDKs and custom platforms](#sdks-and-custom-platforms). In SDK services, isolate filesystem configuration and inject it explicitly; use API keys.
- **Evidence:** [Vendor] ([Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview); [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk)); [Practitioner] ([InfoQ on Ramp](https://www.infoq.com/news/2026/01/ramp-coding-agent-platform/)). No comparison of SDK-built and CLI-scripted reliability or cost was found.

### Measuring outcomes

#### 23. Build evals from real failures

- **Practice:** maintain a task-specific eval set drawn from real failed runs, graded on outcomes.
- **Why:** "An eval at 100% tracks regressions but provides no signal for improvement."
- **How:** "20-50 simple tasks drawn from real failures is a great start"; grade "what the agent produced, not the path it took"; combine code-based graders (fast, objective, brittle), model-based graders (flexible, need calibration) and human review (gold standard, slow). Use pass@k for best-of-N and pass^k (all k runs succeed) for scheduled and CI runs, which must work every time (inference in the notes).
- **Evidence:** [Vendor, Jan 2026] ([Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)).

#### 24. Track outcome and burden metrics

- **Practice:** measure merge rate by task type together with review burden and stability; distrust self-reported speedups.
- **Why:** merge rate alone overstates value: rejected agent PRs often get no feedback, and agent PRs are structurally simpler. Perceived and measured speed diverge.
- **How:** merge rate by task type; share merged without modification; review comments and time per agent PR; rework and revert rate; change-failure rate; cost per merged PR (inference in the notes). Ramp measures PR-authorship share, session count and integration cost or count ([port.io, secondary](https://software-factories.port.io/ramp)).
- **Evidence:** see [Verification](#verification) for the studies.

## Anti-patterns

| Avoid | Do instead |
| --- | --- |
| Kitchen-sink session; correcting the same issue more than twice | `/clear` and a better prompt; one session per problem ([7](#7-keep-sessions-short-and-hand-off-in-writing)) |
| Trust-then-verify gap: accepting plausible code without edge cases | A check the agent runs, evidence in the transcript ([5](#5-give-the-agent-a-check-it-can-run)) |
| The implementer grading itself | Fresh-context reviewer, evaluator or CI ([6](#6-separate-the-grader-from-the-implementer)) |
| Chasing every reviewer finding | Flag only correctness and requirement gaps |
| A full spec workflow for a one-line bug | Skip the plan when the diff fits in one sentence |
| Durable rules crammed into one prompt | `AGENTS.md` / instructions |
| Infinite exploration | Scope the investigation; use a subagent |
| Goals phrased as unobservable properties ("code is clean") | One measurable end state, a check, constraints, a bound ([9](#9-write-goal-conditions-the-transcript-can-prove)) |
| Checkpoints as the only rollback | Git commits ([8](#8-use-git-for-rollback)) |
| `claude -p` in an untrusted checkout without `--bare` | `--bare` plus explicit flags; config restored from base ([11](#11-isolate-the-configuration-of-headless-runs)) |
| Relying on headless permission defaults | Explicit mode or sandbox ([12](#12-set-the-permission-envelope-explicitly)) |
| Model API key as a job-level env var in workflows running repo code | Key only in the agent step; separate write job ([15](#15-split-the-agent-job-from-the-write-job)) |
| `allowed_non_write_users: '*'`, wildcard bots, `pull_request_target` checking out fork code | Write-access trigger only; no fork code with secrets ([16](#16-restrict-triggers-and-treat-repository-text-as-hostile)) |
| Inline interpolation of untrusted values in workflow steps | Pass via `env:` |
| Pushing agent commits with the default `GITHUB_TOKEN` and expecting CI | GitHub App or app token |
| Untested live changes without worktrees | Worktree per session ([18](#18-give-each-parallel-session-its-own-worktree-setup-and-cleanup)) |
| Best-of-N without an automated selector | Tests plus a grader pick the winner |
| Treating a green scheduled run as success | Read transcripts; check outputs ([21](#21-monitor-outcomes-not-run-status)) |
| Constant supervision of the agent (Codex anti-pattern) | Give it permissions and checks inside a safe envelope |

## Security

Prompt injection through issue, PR and comment text is the main automation threat. It is highest where automation is most attractive: issue-to-PR on public repositories. The safe default (inference in the notes) is that the agent reads untrusted text only in a job that holds no write token and no secrets beyond the model key, and that its output is data (patch, JSON) consumed by a deterministic step.

Incidents and research:

| Date | Item | Detail |
| --- | --- | --- |
| Reported Jan 2026; fixed in v1.0.94 within four days; published 2026-06-04 | `claude-code-action` permission flaw, CVSS 7.8 (GMO Flatt Security, RyotaK) [Advisory] | The check "waved through any actor whose name ended in [bot]", and an example workflow shipped `allowed_non_write_users: '*'`. One public issue with an injected payload could make Claude read env credentials, steal OIDC tokens, exchange them for App installation tokens with write access, and potentially poison the action repository. Mitigations: update; audit workflows that admit non-write users or bots; expose only the API key and `GITHUB_TOKEN`; remove tools and permissions usable for exfiltration ([The Hacker News](https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html)) |
| April 2026 | "Comment and Control" [Advisory] | A single malicious PR comment or issue could make Claude Code Security Review Action, Gemini CLI Action and GitHub Copilot Agent exfiltrate `ANTHROPIC_API_KEY`, `GITHUB_TOKEN`, `GEMINI_API_KEY` with "zero interaction from a repository maintainer beyond the automated workflow trigger". CSA mitigations: pin actions to SHAs, remove `pull_request_target` workflows that check out fork code, OIDC ephemeral credentials, minimum `permissions:`, runner monitoring (for example Harden-Runner), delimit untrusted input ([CSA research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-github-actions-security-20260503-csa-st/)) |
| 2026-02-17 | "Clinejection" [Advisory] | A malicious GitHub issue title chained four vulnerabilities into a supply-chain compromise of the Cline npm package for about 8 hours. From a CSA search snippet; details not independently verified ([CSA research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-code-github-action-prompt-injection/)) |
| Fixes 2025-08-26 to 2025-12-28; fixed 2025-08-20 | Repository config RCE in Claude Code (CVE-2025-59536) and Codex CLI (CVE-2025-61260) [Advisory] | Project hooks, MCP servers or `CODEX_HOME` redirection ran code before consent in older versions; relevant to headless runs over untrusted checkouts. Details in [MCP security](./mcp.md#security) |

Threats and mitigations:

| Threat | Mitigation |
| --- | --- |
| Injected instructions in PR titles and bodies (hidden HTML comments), commit messages, `AGENTS.md`, screenshots | Trusted-actor triggers; read-only agent job; output as data; sanitization is not sufficient on its own ([16](#16-restrict-triggers-and-treat-repository-text-as-hostile)) |
| Secret exfiltration from the runner | Key only in the agent step; `drop-sudo` / `unprivileged-user`; OIDC; codex-action as the last step |
| Repository config executes in headless runs | `--bare`; config restored from base branch; Codex trust gating ([11](#11-isolate-the-configuration-of-headless-runs)) |
| Bot loops | Bots rejected unless in `allowed_bots`, which "keeps bots from triggering Claude in a loop" |
| Public logs leak data | `show_full_output` off on public repos |
| Scheduled runs act on untrusted payloads | `<routine-fire-payload>` opt-in; no write tools for triage; branch protection |
| Unsigned agent commits | `use_commit_signing` (no rebase or cherry-pick) or an SSH key |

Gaps: no vendor statement on comparable injection CVEs for `codex-action`; no OpenCode GitHub action security guidance.

## Verification

Run-level checks:

- Claude Code: exit code; `permission_denials`; `total_cost_usd`; fail on `plugin_errors` / `mcp_server_errors` in `system/init`; `--output-format stream-json --verbose` to watch `/goal` and plugin loading ([Claude Code headless](https://code.claude.com/docs/en/headless)).
- Codex: `--json` event stream; `-o` final message; schema-validated output file ([Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)).
- Scheduled and CI runs: read the transcript; check the output (PR, comment, artifact) exists and its checks pass.
- Usage: Claude Code GitHub Action analytics dashboard and monitoring ([Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)).

Evals ([practice 23](#23-build-evals-from-real-failures)): 20–50 tasks from real failures; outcome grading; pass@k for best-of-N, pass^k for unattended runs; add new failures as cases.

Outcome baselines from studies, for comparison with your own metrics:

| Study | Finding |
| --- | --- |
| Watanabe et al. (Sep 2025, v3 Feb 2026) [Empirical] | 567 Claude Code PRs in 157 OSS projects, mostly refactoring, docs, tests; 83.8% merged; 54.9% of merged PRs without modification; the rest needed changes, especially bug fixes, docs and project standards ([arXiv 2509.14745](https://arxiv.org/abs/2509.14745)) |
| AIDev, Li, Zhang, Hassan (Jul 2025) [Empirical] | 456k+ agent PRs (Codex, Devin, Copilot, Cursor, Claude Code) in 61k repos; agents are faster but "their PRs are accepted less frequently"; agent PRs are structurally simpler ([arXiv 2507.15003](https://arxiv.org/abs/2507.15003)) |
| Pinna et al. (Feb 2026, rev. May 2026) [Empirical] | 7,156 AIDev PRs; docs 82.1% vs new features 66.1% acceptance; Codex 59.6–88.6% across nine categories; Claude Code 92.3% (docs), 72.6% (features); "no single agent performs best across all task types"; task type matters more than agent ([arXiv 2602.08915](https://arxiv.org/abs/2602.08915)) |
| Nakashima et al. (Feb 2026) [Empirical] | 654 rejected agent PRs; seven agent-specific rejection modes including distrust of AI code; 67.9% had no explicit reviewer feedback ([arXiv 2602.04226](https://arxiv.org/abs/2602.04226)) |
| Mazloomzadeh, Morovati, Khomh (Jul 2026) [Empirical] | Longitudinal agent vs human merge-rate gaps; abstract gives no numbers ([arXiv 2607.21832](https://arxiv.org/abs/2607.21832)) |
| METR RCT (Jul 2025, early-2025 tools, older) [Empirical] | 16 experienced OSS developers, 246 tasks: AI use made tasks take 19% longer (CI +2% to +39%) while developers believed they were ~20% faster. Feb 2026 update: −18% (CI −38% to +9%) for returning and −4% (CI −15% to +9%) for new developers (negative = speedup); METR calls the data unreliable due to selection effects ([METR 2025](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/); [METR Feb 2026](https://metr.org/blog/2026-02-24-uplift-update/)) |
| DORA 2025 (Sep 29 2025) [Empirical] | ~90% use AI; 33% trust its output (3% high trust), 46% distrust accuracy; adoption correlates with higher throughput and higher instability; AI is "an amplifier"; capabilities include clear AI policies, quality internal platforms, version control practices, small batches ([InfoQ on DORA 2025](https://www.infoq.com/news/2025/09/dora-state-of-ai-in-dev-2025)) |

Aggregator summaries of AIDev give contradictory per-agent merge figures (for example "Claude 84.3%, Codex 73.5%" vs "Codex dominates at 0.83"); they could not be traced to a primary table and are not used ([emergentmind](https://www.emergentmind.com/topics/aidev.md)).

## Checklist

- [ ] Non-trivial tasks start with a plan or spec that states "done when" and a verification step.
- [ ] The agent has a check it can run (tests, build, lint, screenshot); results appear as evidence in the transcript.
- [ ] Something other than the implementer grades the work (reviewer subagent, evaluator, Stop hook, CI).
- [ ] Test-first work has a guard against test edits.
- [ ] `/goal` conditions name a check, constraints and a bound.
- [ ] Headless runs: configuration isolated (`--bare` / `settingSources: []` / `--ignore-user-config`); permission mode or sandbox passed explicitly; schema-validated output to a file; turn, time and budget caps.
- [ ] CI: actions pinned to SHAs; triggers limited to write-access users; no `allowed_non_write_users`, no wildcard bots; no `pull_request_target` with fork checkout; untrusted values via `env:`.
- [ ] CI: model key only in the agent step; writes happen in a separate job; job `permissions:` minimal; OIDC where available.
- [ ] Codex action uses `drop-sudo` or `unprivileged-user` and runs as the last step.
- [ ] Parallel sessions use worktrees with a setup step; headless worktrees are removed.
- [ ] Schedules name a skill, success criteria and output location; writes go to a protected branch prefix; triage runs have no write tools or secrets.
- [ ] Monitoring reads outcomes and transcripts, not run status.
- [ ] An eval set from real failures exists; unattended workflows are judged by pass^k.
- [ ] Team metrics include merge rate by task type, unmodified-merge share, review time, revert rate, change-failure rate and cost per merged PR.

## Open questions

- No controlled study compares spec-driven and ad-hoc prompting, or TDD and no TDD, for agent outcomes.
- ImpossibleBench per-model cheating rates were not extracted; "stronger models cheat more" is unverified.
- Codex documentation on compaction and handoff patterns is thin; no Codex counterpart to Anthropic's long-running-harness write-ups.
- OpenCode: no workflow-level best-practice guidance, no GitHub action security guidance, no SDK best practices beyond the vendor reference.
- No public data on per-run cost or tokens for CI review or autofix workflows.
- Codex hosted `@codex review` configuration (severity levels, `AGENTS.md` rules) could not be retrieved from current docs.
- No vendor statement on whether `codex-action` has had injection CVEs comparable to those reported for Claude, Gemini and Copilot.
- No data on merge-conflict rates when merging many parallel agent branches; no vendor guidance on concurrent sessions per reviewer.
- `codex cloud exec --attempts` semantics and winner selection come from a third-party blog only.
- No numbers on scheduled agent jobs (for example dependency-update success vs Renovate or Dependabot); Codex scheduled-task guardrails are undocumented in the fetched pages.
- No comparison of SDK-built and CLI-scripted automation reliability or cost.
- No study measures human review time per agent PR directly; no study separates headless/CI-originated PRs from interactive ones; PR-acceptance studies conflate tool, model version and usage.
- Ramp's ~75% PR share by May 2026 and the "Clinejection" details are unverified secondary claims.

## Sources

Vendor:

- [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- [Claude Code /goal](https://code.claude.com/docs/en/goal)
- [Claude Code headless](https://code.claude.com/docs/en/headless)
- [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)
- [Claude Code worktrees](https://code.claude.com/docs/en/worktrees)
- [Claude Code routines](https://code.claude.com/docs/en/routines)
- [Claude Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [claude-code-action security.md](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md)
- [Anthropic, Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Anthropic, Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Anthropic, Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Codex best practices](https://learn.chatgpt.com/guides/best-practices)
- [Codex: follow goals](https://learn.chatgpt.com/use-cases/follow-goals)
- [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)
- [Codex GitHub Action](https://learn.chatgpt.com/docs/github-action)
- [codex-action security.md](https://github.com/openai/codex-action/blob/main/docs/security.md)
- [Codex cloud](https://learn.chatgpt.com/docs/cloud)
- [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk)

Empirical:

- [ImpossibleBench, arXiv 2510.20270](https://arxiv.org/abs/2510.20270); [ICLR 2026 poster](https://iclr.cc/virtual/2026/poster/10009390)
- [Watanabe et al., arXiv 2509.14745](https://arxiv.org/abs/2509.14745)
- [AIDev, arXiv 2507.15003](https://arxiv.org/abs/2507.15003)
- [Pinna et al., arXiv 2602.08915](https://arxiv.org/abs/2602.08915)
- [Nakashima et al., arXiv 2602.04226](https://arxiv.org/abs/2602.04226)
- [Mazloomzadeh et al., arXiv 2607.21832](https://arxiv.org/abs/2607.21832)
- [METR 2025](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/); [METR Feb 2026 update](https://metr.org/blog/2026-02-24-uplift-update/)
- [InfoQ on DORA 2025](https://www.infoq.com/news/2025/09/dora-state-of-ai-in-dev-2025)
- [emergentmind AIDev summary (aggregator, not used for figures)](https://www.emergentmind.com/topics/aidev.md)

Advisory:

- [The Hacker News, claude-code-action flaw](https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html)
- [CSA research note, AI GitHub Actions security](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-github-actions-security-20260503-csa-st/)
- [CSA research note, Claude Code GitHub Action prompt injection](https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-code-github-action-prompt-injection/)

Practitioner:

- [Böckeler, Understanding SDD tools](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [softwareseni.com, spec-driven development (secondary)](https://www.softwareseni.com/spec-driven-development-is-replacing-vibe-coding-as-the-professional-standard-for-ai-teams)
- [Willison, Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/)
- [Willison, parallel coding agents](https://simonwillison.net/2025/Oct/5/parallel-coding-agents/)
- [Vaughan, Codex non-interactive pipelines](https://codex.danielvaughan.com/2026/05/03/codex-cli-non-interactive-pipelines-exec-resume-structured-output/)
- [Vaughan, Codex best-of-N](https://codex.danielvaughan.com/2026/04/01/codex-cloud-exec-best-of-n-attempts/)
- [InfoQ on Ramp's coding agent platform](https://www.infoq.com/news/2026/01/ramp-coding-agent-platform/)
- [port.io on Ramp (secondary)](https://software-factories.port.io/ramp)

Repo: [automation concept page](../concepts/automation.md), [concept index](../concepts/README.md)
