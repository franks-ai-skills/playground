# Automation

Automation covers how agent-driven development runs end to end: the interactive explore, plan, implement and verify loop, and every way a run starts and finishes without a person typing into a session. That includes headless command-line runs, SDKs, CI integrations, vendor-hosted runs, schedules and isolated worktrees for parallel work. These surfaces turn the agent into a step in a script, pipeline or timer, reusing the same instructions, skills, hooks and permissions as the interactive session with different defaults for trust, permissions and output.

All surfaces share one model: a *run* with a prompt, a configuration set, a permission envelope, an output contract and a session handle. Delegation inside a run is covered in [subagents](subagents.md).

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Headless CLI | `claude -p` ([CC](../vendors/claude-code/automation.md#headless-flags)) | `codex exec` ([Codex](../vendors/codex/automation.md#codex-exec)) | `opencode run` ([OC](../vendors/opencode/automation.md#opencode-run)) |
| Output formats | `--output-format text\|json\|stream-json`; `json` has `result`, `session_id`, `total_cost_usd` | Final message on stdout; `--json` JSONL events; `-o` writes the final message to a file | `--format default\|json` |
| Schema-validated output | `--json-schema` (inline) → `structured_output` | `--output-schema <file>` | SDK `format: { type: "json_schema" }` |
| Resume and fork | `--continue`, `--resume <id>`; SDK fork, `/fork` | `codex exec resume --last\|<id>`; `codex exec fork` | `--continue`, `--session`, `--fork` |
| Default permissions headless | Mode `default` or `auto` depending on feature flags; project allow rules not used | Sandbox `read-only` | Normal config; `--auto` approves every `ask` |
| Widen permissions | `--allowedTools`, `--permission-mode`, `--permission-prompts none` | `--sandbox workspace-write\|danger-full-access` | `--auto` |
| Config isolation | `--bare` skips hooks, skills, agents, plugins, MCP, memory, `CLAUDE.md` | `--ignore-user-config`, `--ignore-rules`, `--ephemeral` | Not recorded |
| Repository hooks headless | Run without a trust prompt ([CC hooks](../vendors/claude-code/hooks.md)) | Skipped until trusted by hash ([Codex hooks](../vendors/codex/hooks.md)) | Not recorded |
| API-key auth | `ANTHROPIC_API_KEY` or `apiKeyHelper` | `CODEX_API_KEY` | Not recorded |
| SDK | Agent SDK (Python, TypeScript); loads filesystem config unless `settingSources: []` ([CC](../vendors/claude-code/automation.md#agent-sdk)) | `@openai/codex-sdk`, `openai-codex`; threads ([Codex](../vendors/codex/automation.md#sdks)) | `@opencode-ai/sdk` wraps `opencode serve` ([OC](../vendors/opencode/automation.md#sdk)) |
| GitHub Action | `anthropics/claude-code-action@v1`; `@claude` mentions ([CC](../vendors/claude-code/automation.md#github-actions)) | `openai/codex-action@v1`; `@codex review` served by Codex Cloud | `anomalyco/opencode/github`; `/opencode`, `/oc` ([OC](../vendors/opencode/automation.md#github-action)) |
| Hosted runs | Routines, cloud sessions; repo and account skills only | Codex Cloud tasks, `codex cloud exec --env` ([Codex](../vendors/codex/automation.md#codex-cloud)) | None recorded |
| Schedules | Desktop tasks (min 1 min), routines (min 1 h), `/loop` in an open session; 5-field cron ([CC](../vendors/claude-code/automation.md#scheduling)) | Desktop-app and web scheduled tasks; RRULE; no CLI scheduling | GitHub Action `schedule` event |
| Event triggers outside CI | Routines: HTTP API, GitHub events | Gmail, Slack, GitHub on ChatGPT web only | None recorded |
| Skills in scheduled prompts | Only model-invocable skills run | `$skill-name` in the prompt | n/a |
| Goal-driven continuation | `/goal` | `/goal`, `goals` feature | Not recorded |
| Session worktree | `--worktree <name>` → `.claude/worktrees/<name>/`; `.worktreeinclude` ([CC](../vendors/claude-code/automation.md#worktrees)) | CLI `--worktree`; desktop Worktree mode (detached HEAD); setup scripts ([Codex](../vendors/codex/automation.md#worktrees)) | None recorded |

Cells without a link come from the vendor automation pages: [Claude Code](../vendors/claude-code/automation.md), [Codex](../vendors/codex/automation.md), [OpenCode](../vendors/opencode/automation.md).

## Generalized model

**Run.** One agent session started without an interactive user.

| Part | Meaning |
| --- | --- |
| Prompt | Text from an argument, a file or stdin |
| Configuration set | Which config layers, instructions, skills, subagents, hooks, plugins and MCP servers load. Default: the same discovery as an interactive session. Isolated: user or all discovered config skipped |
| Permission envelope | What the run may do without asking. No one answers prompts, so it is set before the run starts |
| Trust | Whether project-level hooks and config run without a person confirming them |
| Output contract | Final text, an event stream (JSON lines), or a final object validated against a JSON Schema |
| Session handle | An ID to resume or fork the run |
| Working copy | The checkout in place, or an isolated worktree |
| Credentials | An API key from the environment |

**Programmatic session (SDK).** A library that exposes the same agent loop as the CLI: create a session or thread, run a turn, continue or resume by ID. It loads the same filesystem configuration as the CLI unless told otherwise.

**CI integration.** An action installs the CLI and runs one headless run per workflow event, either with a fixed prompt or triggered by a mention in a comment. Who may trigger, privilege dropping and separate write jobs are part of the action configuration.

**Hosted run.** A run in the vendor's cloud against a cloned repository. It uses committed configuration plus account settings, not the user's home directory, and keeps running when the local machine is off.

**Schedule.** A stored prompt plus a cadence, an execution site (local or hosted), a context policy (new session per run or appended), an unattended permission policy and a working copy. The prompt may name a skill: the skill defines the method, the schedule the timing.

**Goal-driven continuation.** A session-level goal that keeps the agent working across turns until a condition holds. Both leads expose it as `/goal`.

**Worktree isolation.** A run starts in a new git worktree so parallel runs do not touch the main checkout. Untracked files the work needs (such as `.env`) come from a setup step.

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Headless run | `claude -p` | `codex exec` | `opencode run` |
| Event stream output | `--output-format stream-json` | `--json` | `--format json` |
| Schema-validated output | `--json-schema` | `--output-schema` | SDK `format.json_schema` |
| Resume | `--resume <id>`, `--continue` | `codex exec resume <id>`, `--last` | `--session`, `--continue` |
| Isolated configuration set | `--bare`, SDK `settingSources: []` | `--ignore-user-config`, `--ignore-rules` | — |
| Permission envelope | `--allowedTools`, `--permission-mode` | `--sandbox` | `--auto`, `permission` config |
| CI action | `claude-code-action` | `codex-action` | `opencode/github` |
| Hosted run | Routine, cloud session | Cloud task | — |
| Local / hosted schedule | Desktop task / routine | Desktop-app task / web task | — / GitHub `schedule` |
| Goal-driven continuation | `/goal` | `/goal` | — |
| Session worktree, setup | `--worktree <name>`, `.worktreeinclude` | `--worktree`, setup script | — |

## When to use it and when not

Use it when:

| Situation | Use |
| --- | --- |
| Exploratory, ambiguous or design-heavy work | Interactive session with plan mode ([Explore, plan, implement, verify](#approaches)) |
| A feature where agreeing on scope is the hard part | Spec-driven: interview, spec, fresh session |
| Work bigger than one prompt with a verifiable end state | `/goal` |
| A script, batch migration or pipeline step | Headless CLI |
| PR review, issue-to-PR, autofix on repository events | CI action |
| Several independent tasks that are cheap to review | Worktree-isolated sessions, cloud tasks, best-of-N |
| Repeatable unattended work with a clear outcome (triage, docs drift, dependency bumps) | Schedule or event-triggered hosted run |
| The agent inside your application, with programmatic approvals, sessions or per-tenant cost | SDK |

Do not use it when:

| Situation | Use instead | Cost or risk |
| --- | --- | --- |
| The diff fits in one sentence | A direct prompt, no plan or spec | Planning "adds overhead"; a full spec workflow for a small bug is "using a sledgehammer to crack a nut" ([Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)). |
| A rule must hold on every tool call or turn end | A [hook](hooks.md) or [permission rule](permissions-and-sandbox.md) | A prompt or goal is advisory; a hook is deterministic. |
| Delegation of a bounded subtask inside one run | A [subagent](subagents.md) | Script-driven orchestration of several runs does not generalize across the leads (see [Dropped](#dropped-from-the-generalization)). |
| The method must be reused across runs | A [skill](skills.md) named in the run or schedule prompt | "The skill defines the method, the schedule defines the timing"; a schedule prompt alone carries no reusable method. |
| Untrusted issue or PR text would reach a job with write tokens or secrets | A read-only agent job plus a separate write job (practice 11) | Prompt injection has exfiltrated keys from agent GitHub Actions (see [Security](#security)). |
| Significant changes in parallel | Serial work | "I can only focus on reviewing and landing one significant change at a time" ([Willison](https://simonwillison.net/2025/Oct/5/parallel-coding-agents/)). |
| Batch work that a shell loop over `-p`/`exec` can do | The headless CLI, not an SDK | Each layer up adds code to maintain. |

## Approaches

**Explore, plan, implement, verify.** Separate read-only exploration and planning from implementation, then verify and commit. Fits an uncertain approach, a multi-file change or unfamiliar code. Claude Code: Explore (plan mode), Plan (`Ctrl+G` edits the plan), Implement, Commit ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)). Codex: each prompt carries Goal, Context, Constraints and "Done when"; plan with `/plan`; review with `/review` ([Codex best practices](https://learn.chatgpt.com/guides/best-practices)). Trade-off: overhead on clear tasks.

**Spec-driven work.** A written spec fixes scope first. Böckeler distinguishes spec-first, spec-anchored and spec-as-source; Kiro and spec-kit are effectively spec-first ([Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html), Oct 2025). Claude Code's interview pattern: the agent interviews you with `AskUserQuestion`, writes `SPEC.md`, and a fresh session executes it. The pattern uses no vendor-only feature, so it also works in Codex with Plan mode. Trade-off: Markdown artifacts are "very verbose and tedious to review", and agents still ignore spec instructions.

**Test-driven work.** Write a failing test, confirm it fails, make it pass. Fits behaviour a test can express and bug fixes. Prompt "Use red/green TDD" ([Willison](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/)) or split Writer and Tester across sessions. Trade-off: agents modify or game tests ([ImpossibleBench](https://arxiv.org/abs/2510.20270)), so add a guard (practice 3).

**Goals and long-running work.** Fits a task "bigger than one prompt but smaller than an open-ended backlog" ([Codex: follow goals](https://learn.chatgpt.com/use-cases/follow-goals)). Claude Code `/goal`: after each turn a small model judges the condition from the transcript only; it works in `-p` (add `--output-format stream-json --verbose`) and does not change the permission mode ([Claude Code /goal](https://code.claude.com/docs/en/goal)). Codex: `/goal Complete [objective] without stopping until [verifiable end state].` with `pause|resume|clear`. For multi-session work Anthropic uses an initializer session that writes `init.sh`, a progress log and a feature list with every feature failing; later sessions do one feature each ([Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), Nov 2025). Trade-off: on one brief a solo agent took 20 min / $9 and a full planner-generator-evaluator harness 6 h / $200 ([Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps), Mar 2026, older models).

**Headless runs and fan-out.** One non-interactive run per invocation. Generalized: isolated configuration, explicit envelope, schema-validated output to a file, caps, API-key credentials. Claude Code: `--bare` "is the recommended mode for scripted and SDK calls" and loads context only through flags; `--permission-mode` explicit; stdin capped at 10 MB ([Claude Code headless](https://code.claude.com/docs/en/headless)). Codex: read-only by default, `--sandbox workspace-write` for edits, `--full-auto` deprecated ([Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)). Trade-off: `--bare` also drops project skills.

```bash
# Claude Code fan-out (vendor recipe): refine on 2-3 files, then run on all
for file in $(cat files.txt); do
  claude -p "Migrate $file to the new API. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)" --permission-mode dontAsk
done

# Codex pipeline step
CODEX_API_KEY="$KEY" codex exec --ephemeral --ignore-user-config \
  --sandbox read-only --json --output-schema schema.json -o result.json \
  "Summarize the risk of the changes on this branch."
```

**CI integration.** A vendor action runs one headless run per event. `claude-code-action` has an interactive mode (responds to `@claude`) and an automation mode (`prompt` set); plain-text prompts get no shell or GitHub API access until tools are granted; commits pushed with the default `GITHUB_TOKEN` do not trigger CI ([Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)). `codex-action` runs `codex exec` behind a Responses API proxy with `safety-strategy` (`drop-sudo` default); one job writes the final message and a second posts comments ([Codex GitHub Action](https://learn.chatgpt.com/docs/github-action)). Trade-off: CI is where untrusted text meets secrets.

**Parallel sessions and best-of-N.** Several sessions, each in its own working copy, or N attempts at one task. Fits research, proofs of concept, "system understanding" questions and small maintenance ([Willison](https://simonwillison.net/2025/Oct/5/parallel-coding-agents/), Oct 2025). Claude Code: `--worktree`, `.worktreeinclude`, `worktree.baseRef`; `/batch` splits work across 5–30 worktree subagents ([Claude Code worktrees](https://code.claude.com/docs/en/worktrees)). Codex: parallel cloud tasks that keep working while your computer sleeps ([Codex cloud](https://learn.chatgpt.com/docs/cloud)); `codex cloud exec --attempts` 2–4 ([Vaughan](https://codex.danielvaughan.com/2026/04/01/codex-cloud-exec-best-of-n-attempts/), [Practitioner]). Trade-off: review is the bottleneck; neither lead handles port conflicts or per-worktree installs.

**Scheduled and event-triggered runs.** Claude Code routines (research preview) save a prompt, repositories and connectors, trigger on schedule, API or GitHub events, run without approval, and push to `claude/`-prefixed branches ([Claude Code routines](https://code.claude.com/docs/en/routines)). Codex schedules "stable workflows as background tasks through the Scheduled page" and turns repeatable workflows into skills "scoped to one job" ([Codex best practices](https://learn.chatgpt.com/guides/best-practices)). Trade-off: "A green status … does not mean the task in your prompt succeeded."

**SDKs and custom platforms.** Use the lowest layer that fits: CLI or action for scripts and CI, SDK when the agent lives in your application, an own platform only when deep internal integration justifies it. The Claude Agent SDK loads `.claude/` like the CLI and powers the GitHub Action; third-party products must use API keys, not claude.ai login, without approval ([Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)). The Codex SDK offers threads and sandbox presets; the app-server serves custom clients ([Codex SDK](https://learn.chatgpt.com/docs/codex-sdk)). Ramp's own platform runs in sandboxed VMs with access to tests, Sentry, Datadog and databases, and produced ~30% of merged PRs ([InfoQ](https://www.infoq.com/news/2026/01/ramp-coding-agent-platform/), Jan 2026, [Practitioner]). Trade-off: each step up adds code to maintain; SDKs load filesystem config by default, so isolate and inject it for reproducible service use.

## Practices

1. **Plan non-trivial work and state "done when".**
   - Why: planning catches wrong approaches before code exists; the agent cannot verify or stop correctly without an end state.
   - How: plan mode for uncertain, multi-file or unfamiliar work; skip it when the diff fits in one sentence. Name goal, relevant files, constraints and what "fixed" looks like; put durable rules in [instructions](instructions.md).
   - Evidence: [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices); [Codex best practices](https://learn.chatgpt.com/guides/best-practices), which lists skipping planning on complex tasks as an anti-pattern).
2. **Size specs to the task and execute them in a fresh session.**
   - Why: "Time spent making the spec precise pays off more than time spent watching the implementation."
   - How: interview → `SPEC.md` naming files, interfaces, out-of-scope items and an end-to-end check → new session. No spec for small bugs.
   - Evidence: [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)); [Practitioner] Böckeler: "I'd rather review code than all these markdown files" ([Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)). Both agree on sizing; no controlled study compares spec-driven and ad-hoc prompting.
3. **Use red/green TDD and guard the tests.**
   - Why: tests that already pass validate nothing, and frontier agents exploit tests "from simple test modification to complex operator overloading".
   - How: "Use red/green TDD", or a Writer/Tester split. Guards (inference; neither vendor documents one): "no test file is modified" in the goal condition, a [hook](hooks.md) blocking test writes in the green phase, or a reviewer that diffs tests separately.
   - Evidence: [Practitioner] ([Willison](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/)); [Empirical] ([ImpossibleBench](https://arxiv.org/abs/2510.20270), ICLR 2026).
4. **Give the agent a check it can run and ask for evidence, not claims.**
   - Why: "It's the difference between a session you watch and one you walk away from." Without a check, "you become the verification loop".
   - How: tests, build, lint or screenshot comparison, escalating from the prompt to `/goal`, a Stop hook that blocks the turn until it passes, or a verification subagent. For UI work require browser automation "as a human user would".
   - Evidence: [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices); [Codex best practices](https://learn.chatgpt.com/guides/best-practices); [Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).
5. **Let something other than the implementer grade the work.**
   - Why: self-grading agents "tend to respond by confidently praising the work—even when … the quality is obviously mediocre"; separating generator and evaluator was "a strong lever".
   - How: a fresh-context reviewer [subagent](subagents.md) with the diff and plan and "Report gaps, not style preferences"; Codex `/review`; CI. A reviewer prompted to find gaps "will usually report some, even when the work is sound", so act only on correctness and requirement gaps.
   - Evidence: [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices); [Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps), older models).
6. **Keep sessions short, hand off in writing, and roll back with git.**
   - Why: "A clean session with a better prompt almost always outperforms a long session with accumulated corrections." Claude Code checkpoints miss Bash side effects: "This isn't a replacement for git."
   - How: one session per problem; after more than two corrections, clear and restart; steer `/compact`; commit per step. For multi-hour work Anthropic found context resets with a structured handoff better than compaction.
   - Evidence: [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices); [Codex best practices](https://learn.chatgpt.com/guides/best-practices); [Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps)).
7. **Write goal conditions the transcript can prove, and test each harness component.**
   - Why: the Claude Code evaluator reads only the transcript, so "code is clean" is judged on the agent's own claims. "Every component in a harness encodes an assumption about what the model can't do on its own."
   - How: `/goal npm test exits 0; no other test file is modified; or stop after 20 turns`; pair with an explicit permission mode. For multi-session work keep a progress file and a pass/fail feature list; remove parts the current model no longer needs.
   - Evidence: [Vendor] ([Claude Code /goal](https://code.claude.com/docs/en/goal); [Codex: follow goals](https://learn.chatgpt.com/use-cases/follow-goals); [Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps)).
8. **Isolate the configuration of headless runs.**
   - Why: without `--bare`, `claude -p` "runs the hooks in a project's `.claude/settings.json` and connects the servers in its `.mcp.json`, even in a folder you've never trusted". Codex skips untrusted project config in `codex exec`.
   - How: Claude Code `--bare` plus explicit `--settings`, `--mcp-config`, `--agents`, `--plugin-dir`; SDK `settingSources: []`. Codex `--ignore-user-config`, `--ignore-rules`, `--ephemeral`. `claude-code-action` restores `.claude/`, `.mcp.json` and `CLAUDE.md` from the PR base branch.
   - Evidence: [Vendor] ([Claude Code headless](https://code.claude.com/docs/en/headless); [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md); [claude-code-action security](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md)).
9. **Pass the permission envelope explicitly on every headless run.**
   - Why: nobody answers prompts, and the defaults differ: Codex read-only, Claude Code possibly `auto`, OpenCode `--auto` approves everything.
   - How: Claude Code `--permission-mode dontAsk` with `--allowedTools` prefix rules for locked-down CI, `--permission-prompts none` for scheduled runs, auto mode when a classifier should block scope escalation; check `permission_denials`. Codex `--sandbox read-only` or `workspace-write`; `danger-full-access` only in controlled environments.
   - Evidence: [Vendor] ([Claude Code headless](https://code.claude.com/docs/en/headless); [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)). Codex also lists "withholding execution permissions prematurely" as an anti-pattern, so grant what the task needs rather than too little.
10. **Return schema-validated output, gate on load errors, and cap every run.**
    - Why: a deterministic consumer can act on data; unattended loops do not stop on their own.
    - How: keep the schema in a file (Claude Code takes it inline: `--json-schema "$(cat schema.json)"`; Codex `--output-schema`). Fail CI on `plugin_errors` or `mcp_server_errors` in `system/init`. Set `--max-turns`, `--max-budget-usd` (Claude Code only), workflow timeouts and GitHub `concurrency`; track `total_cost_usd`.
    - Evidence: [Vendor] ([Claude Code headless](https://code.claude.com/docs/en/headless); [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)); [Practitioner] ([Vaughan, pipelines](https://codex.danielvaughan.com/2026/05/03/codex-cli-non-interactive-pipelines-exec-resume-structured-output/)).
11. **Split the agent job from the write job.**
    - Why: if injected text takes over the agent, it holds no write token and no secrets beyond the model key.
    - How: agent job with `contents: read` and the key only in the agent step, output as a patch artifact; a separate job without the key applies it. "Do not set `OPENAI_API_KEY` or `CODEX_API_KEY` as a job-level environment variable." Prefer OIDC (`id-token: write`) over long-lived secrets. The pattern uses no Codex-only feature and applies to `claude-code-action`.
    - Evidence: [Vendor] ([Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md); [Codex GitHub Action](https://learn.chatgpt.com/docs/github-action); [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)).
12. **Restrict triggers and treat repository text as hostile.**
    - Why: injection through issue and PR content was exploited against agent GitHub Actions in 2026.
    - How: keep the default of write-access users; do not set `allowed_non_write_users` or wildcard bots. Treat PR titles and bodies, commit messages, `AGENTS.md` and screenshots as attacker-controlled. Do not check out fork code under `pull_request_target`; pass untrusted values via `env:`; pin actions to SHAs; Codex `safety-strategy: drop-sudo` or `unprivileged-user`, run the action as the last step.
    - Evidence: [Vendor] ([claude-code-action security](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md); [codex-action security](https://github.com/openai/codex-action/blob/main/docs/security.md)); [Advisory] ([CSA](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-github-actions-security-20260503-csa-st/)).
13. **Parallelize only what is cheap to review, each session in its own worktree.**
    - Why: human review is the bottleneck, and sessions in one checkout overwrite each other.
    - How: worktree or container per session with a setup step; remove `-p` worktrees with `git worktree unlock` then `remove`. Pilot a batch prompt on 2–3 items first. Use best-of-N only when tests and a grader pick the winner.
    - Evidence: [Practitioner] ([Willison](https://simonwillison.net/2025/Oct/5/parallel-coding-agents/)); [Vendor] ([Claude Code worktrees](https://code.claude.com/docs/en/worktrees); [Claude Code best practices](https://code.claude.com/docs/en/best-practices)). No vendor gives a maximum number of sessions per reviewer.
14. **Make scheduled prompts self-contained, scope their reach, and monitor outcomes.**
    - Why: routines run without approval, and "Claude can use every tool from an included connector, including writes, without asking." A green run status is not success.
    - How: name a skill, success criteria and output location; write to a protected branch prefix; give triage runs no write tools beyond labels and comments and no secrets; act on `<routine-fire-payload>` only by opt-in. Check that the PR or artifact exists and passes; read transcripts.
    - Evidence: [Vendor] ([Claude Code routines](https://code.claude.com/docs/en/routines)). Codex scheduled-task guardrails are not documented.

## Security

Prompt injection through issue, PR and comment text is the main automation threat, and it is highest where automation is most attractive: issue-to-PR on public repositories. The safe default is that the agent reads untrusted text only in a job that holds no write token and no secret beyond the model key, and that its output is data (patch, JSON) consumed by a deterministic step.

| Date | Incident [Advisory] |
| --- | --- |
| Reported Jan 2026, fixed in v1.0.94, published 2026-06-04 | `claude-code-action` permission flaw, CVSS 7.8: the check waved through any actor whose name ended in `[bot]`, and an example workflow shipped `allowed_non_write_users: '*'`. One injected issue could steal OIDC tokens and obtain write-capable App tokens ([The Hacker News](https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html)) |
| April 2026 | "Comment and Control": one malicious PR comment or issue made Claude Code Security Review Action, Gemini CLI Action and GitHub Copilot Agent exfiltrate API keys and `GITHUB_TOKEN` ([CSA](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-github-actions-security-20260503-csa-st/)) |
| 2026-02-17 | "Clinejection": a malicious issue title led to a supply-chain compromise of the Cline npm package for about 8 hours; not independently verified ([CSA](https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-code-github-action-prompt-injection/)) |
| 2025 | Repository config ran code before consent: Claude Code CVE-2025-59536 and Codex CLI CVE-2025-61260; relevant to headless runs in untrusted checkouts. Details in [MCP](mcp.md) |

| Threat | Mitigation |
| --- | --- |
| Injected instructions in PR text, hidden HTML comments, commit messages, `AGENTS.md`, screenshots | Trusted-actor triggers; read-only agent job; output as data. Sanitization helps "but new bypass techniques may emerge" |
| Secret exfiltration from the runner | Key only in the agent step; `drop-sudo`/`unprivileged-user`; OIDC |
| Repository config executes in headless runs | `--bare`; config restored from base; Codex trust gating |
| Bot loops | Bots rejected unless in `allowed_bots` |
| Public logs leak data | `show_full_output` off on public repositories |
| Scheduled runs act on untrusted payloads | Payload opt-in; no write tools for triage; branch protection |

Gaps: no vendor statement on comparable injection CVEs for `codex-action`; no security guidance for the OpenCode action.

## Verification and checklist

**Run-level checks.** Claude Code: exit code, `permission_denials`, `total_cost_usd` (a client-side estimate), `plugin_errors`/`mcp_server_errors` in `system/init`. Codex: the `--json` stream, the `-o` file and the schema-validated output. Scheduled and CI runs: read the transcript and check the output exists and passes its checks.

**Evals.** "20-50 simple tasks drawn from real failures is a great start"; grade "what the agent produced, not the path it took"; combine code-based graders, model-based graders and human review. Use pass@k for best-of-N and pass^k (all k runs succeed) for scheduled and CI runs, which must work every time. "An eval at 100% tracks regressions but provides no signal for improvement" ([Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), [Vendor], Jan 2026).

**Outcome metrics.** Merge rate alone overstates value: rejected agent PRs often get no feedback, agent PRs are structurally simpler, and perceived and measured speed diverge. Track merge rate by task type, share merged without modification, review time per agent PR, revert rate, change-failure rate and cost per merged PR. Baselines [Empirical]:

| Study | Finding |
| --- | --- |
| Watanabe et al. (Sep 2025) | 567 Claude Code PRs in 157 projects: 83.8% merged, 54.9% of those without modification ([arXiv 2509.14745](https://arxiv.org/abs/2509.14745)) |
| AIDev (Jul 2025) | 456k+ agent PRs: agents are faster but "their PRs are accepted less frequently" ([arXiv 2507.15003](https://arxiv.org/abs/2507.15003)) |
| Pinna et al. (Feb 2026) | Docs 82.1% vs new features 66.1% acceptance; "no single agent performs best across all task types" ([arXiv 2602.08915](https://arxiv.org/abs/2602.08915)) |
| Nakashima et al. (Feb 2026) | 654 rejected agent PRs; 67.9% had no explicit reviewer feedback ([arXiv 2602.04226](https://arxiv.org/abs/2602.04226)) |
| METR RCT (Jul 2025, early-2025 tools) | Tasks took 19% longer with AI while developers believed they were ~20% faster; the Feb 2026 update shows speedups that METR calls unreliable ([METR 2025](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/); [METR 2026](https://metr.org/blog/2026-02-24-uplift-update/)) |
| DORA 2025 | ~90% use AI, 33% trust its output; adoption correlates with higher throughput and higher instability ([InfoQ](https://www.infoq.com/news/2025/09/dora-state-of-ai-in-dev-2025)) |

Checklist:

- [ ] Non-trivial tasks start with a plan or spec that states "done when" and a verification step.
- [ ] The agent has a check it can run; results appear as evidence in the transcript.
- [ ] Something other than the implementer grades the work; test-first work has a guard against test edits.
- [ ] `/goal` conditions name a check, constraints and a bound.
- [ ] Headless runs: isolated configuration, explicit permission mode or sandbox, schema-validated output to a file, turn, time and budget caps.
- [ ] CI: actions pinned to SHAs; triggers limited to write-access users; no fork checkout under `pull_request_target`; untrusted values via `env:`.
- [ ] CI: model key only in the agent step; writes in a separate job; minimal `permissions:`; Codex action uses `drop-sudo` or `unprivileged-user`.
- [ ] Parallel sessions use worktrees with a setup step; headless worktrees are removed.
- [ ] Schedules name a skill, success criteria and output location; writes go to a protected branch prefix.
- [ ] Monitoring reads outcomes and transcripts; an eval set from real failures exists; unattended workflows are judged by pass^k.

## Portability

- **Flags differ in name;** map them through the term table. There is no shared flag set.
- **Defaults point in opposite directions.** `codex exec` is read-only; `claude -p` runs in `default` or `auto` mode. Set the envelope in every script.
- **Trust differs.** Claude Code `-p` and SDK runs load repository hooks and MCP servers without a prompt; Codex skips untrusted project config and hooks. A hook that gates a CI run in Claude Code may silently not run in Codex until trusted.
- **Config isolation is not symmetric.** `--bare` skips all discovered config, including skills and instruction files; Codex's flags skip only user config and rules. A run that depends on project skills must not use `--bare`.
- **Structured output:** keep the schema in a file; pass its contents to Claude Code and the path to Codex.
- **`codex exec` requires a git repository** unless `--skip-git-repo-check` is set.
- **CI:** both actions pass through CLI arguments (`claude_args`, `codex-args`). Comment-driven review is not symmetric: `@codex review` runs in Codex Cloud with rules in a `## Code Review Rules` section of `AGENTS.md`.
- **Scheduling:** neither lead schedules from a plain CLI on a headless machine; system cron plus the headless CLI is the fallback, not an official feature. Store the cadence's intent, not the cron or RRULE expression.
- **Skills in schedules:** Claude Code runs only model-invocable skills from scheduled fires, so a skill with `disable-model-invocation: true` does not run there (see [skills](skills.md)).
- **Hosted runs use what the repository carries.** Claude Code routines ignore `~/.claude/skills`; the Codex pages do not say cloud tasks read local `config.toml`. Commit every skill, instruction file and hook a hosted run needs.
- **Worktrees:** both leads take `--worktree`; untracked files need `.worktreeinclude` (Claude Code) or a setup script (Codex). Scheduled runs in worktrees accumulate them; archive old runs.

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| Dynamic workflows, agent teams, `/batch`, background sessions (`claude --bg`) | Claude Code | No Codex counterpart. |
| `/loop`, cron tools, routine API trigger, channels | Claude Code | Session-bound or tool-level scheduling and push events with no Codex CLI counterpart. |
| Checkpoints and `/rewind`; hook `defer` in `-p`; `--max-budget-usd` | Claude Code | No Codex counterpart recorded. |
| Plan mode | Both | Codex semantics not recorded; belongs to permission modes. |
| `codex review`, `@codex review` and `## Code Review Rules` | Codex | Hosted or built-in review with no recorded Claude Code counterpart. |
| App-server protocol, cloud best-of-N, `codex cloud apply`/`diff`, `safety-strategy`, `codex queue`, `exec-server` | Codex | Single-vendor or experimental. |
| Gmail and Slack triggers | Codex (ChatGPT web) | No Claude Code counterpart. |
| `opencode serve`, `--attach`, ACP, session sharing | OpenCode | No lead counterpart. |

## Open questions

- No controlled study compares spec-driven and ad-hoc prompting, or TDD and no TDD, for agents. ImpossibleBench per-model cheating rates were not extracted.
- Codex documentation on compaction, handoff and long-running harnesses is thin.
- No public data on per-run cost of CI review or autofix workflows, or on scheduled-job success rates.
- No data on merge conflicts across many parallel agent branches; `codex cloud exec --attempts` semantics come from a third-party blog.
- No comparison of SDK-built and CLI-scripted automation.
- No study measures review time per agent PR or separates CI-originated from interactive PRs.
- Ramp's ~75% PR share by May 2026 and the "Clinejection" details are unverified secondary claims.
- Codex scheduled-task guardrails and `@codex review` configuration are not documented in the fetched pages.

## Sources

Vendor pages: [Claude Code: automation](../vendors/claude-code/automation.md), [Codex: automation](../vendors/codex/automation.md), [OpenCode: automation](../vendors/opencode/automation.md), [Claude Code: hooks](../vendors/claude-code/hooks.md), [Codex: hooks](../vendors/codex/hooks.md), [Codex: subagents](../vendors/codex/subagents.md). Research notes: [automation workflows](../research-notes/agent-harness-best-practices/automation-workflows.md).

- Claude Code: [best practices](https://code.claude.com/docs/en/best-practices), [/goal](https://code.claude.com/docs/en/goal), [headless](https://code.claude.com/docs/en/headless), [GitHub Actions](https://code.claude.com/docs/en/github-actions), [worktrees](https://code.claude.com/docs/en/worktrees), [routines](https://code.claude.com/docs/en/routines), [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview), [claude-code-action security](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md)
- Anthropic engineering: [Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [Harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps), [Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- Codex: [best practices](https://learn.chatgpt.com/guides/best-practices), [follow goals](https://learn.chatgpt.com/use-cases/follow-goals), [non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md), [GitHub Action](https://learn.chatgpt.com/docs/github-action), [codex-action security](https://github.com/openai/codex-action/blob/main/docs/security.md), [cloud](https://learn.chatgpt.com/docs/cloud), [SDK](https://learn.chatgpt.com/docs/codex-sdk)
- Empirical: [ImpossibleBench](https://arxiv.org/abs/2510.20270), [Watanabe](https://arxiv.org/abs/2509.14745), [AIDev](https://arxiv.org/abs/2507.15003), [Pinna](https://arxiv.org/abs/2602.08915), [Nakashima](https://arxiv.org/abs/2602.04226), [METR 2025](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/), [METR 2026](https://metr.org/blog/2026-02-24-uplift-update/), [DORA 2025](https://www.infoq.com/news/2025/09/dora-state-of-ai-in-dev-2025)
- Advisory: [The Hacker News, claude-code-action](https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html), [CSA, AI GitHub Actions](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-github-actions-security-20260503-csa-st/), [CSA, prompt injection](https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-code-github-action-prompt-injection/)
- Practitioner: [Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html), [Willison, TDD](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/), [Willison, parallel agents](https://simonwillison.net/2025/Oct/5/parallel-coding-agents/), [Vaughan, pipelines](https://codex.danielvaughan.com/2026/05/03/codex-cli-non-interactive-pipelines-exec-resume-structured-output/), [Vaughan, best-of-N](https://codex.danielvaughan.com/2026/04/01/codex-cloud-exec-best-of-n-attempts/), [InfoQ on Ramp](https://www.infoq.com/news/2026/01/ramp-coding-agent-platform/)
