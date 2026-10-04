# Automation

Automation covers every way an agent run starts and finishes without a person typing into an interactive session: headless command-line runs, SDKs that drive the agent from code, CI integrations, runs hosted by the vendor, scheduled runs, and isolated working copies (git worktrees) for parallel work. These surfaces turn the agent into a step in a script, pipeline or timer. They all reuse the same configuration (instructions, skills, hooks, permissions) as the interactive session, with different defaults for trust, permissions and output.

This page keeps the surfaces on one page because they share one model: a *run* with a prompt, a configuration set, a permission envelope, an output contract and a session handle. Multi-agent orchestration inside a run is covered in [subagents.md](subagents.md); script-driven orchestration does not generalize (see Dropped).

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Headless CLI | `claude -p` ([automation][cc-auto]) | `codex exec` ([automation][cx-auto]) | `opencode run` ([automation][oc-auto]) |
| Prompt from stdin | `--input-format` exists; details not recorded ([automation][cc-auto]) | No prompt or `-` reads stdin; with both, stdin is appended as a `<stdin>` block ([automation][cx-auto]) | `--file/-f` flag exists; stdin not recorded ([automation][oc-auto]) |
| Output formats | `--output-format text\|json\|stream-json`; `json` has `result`, `session_id`, `total_cost_usd` ([automation][cc-auto]) | Final message on stdout, progress on stderr; `--json` gives JSONL events; `-o` writes the final message to a file ([automation][cx-auto]) | `--format default\|json` (raw events) ([automation][oc-auto]) |
| Schema-validated output | `--json-schema` → `structured_output` ([automation][cc-auto]) | `--output-schema <file>` ([automation][cx-auto]) | SDK `format: { type: "json_schema" }` → `structured_output` ([automation][oc-auto]) |
| Continue a session | `--continue`, `--resume <id>` ([automation][cc-auto]) | `codex exec resume --last` (cwd-scoped) or `resume <id\|name>` ([automation][cx-auto]) | `--continue`, `--session` ([automation][oc-auto]) |
| Fork a session | SDK sessions support fork; `/fork` copies a session into a background session ([automation][cc-auto], [subagents][cc-sub]) | `codex exec fork`, `codex fork` ([automation][cx-auto]) | `--fork` ([automation][oc-auto]) |
| Default permissions headless | Permission mode `default` or `auto` depending on feature flags (v2.1.285+); project allow rules not used ([automation][cc-auto]) | Sandbox `read-only` ([automation][cx-auto]); in non-interactive flows, a subagent action that needs new approval fails ([subagents][cx-sub]) | Normal config; `--auto` approves every `ask` ([automation][oc-auto]) |
| Widen permissions | `--allowedTools`, `--permission-mode`, `--permission-prompts none` ([automation][cc-auto]) | `--sandbox workspace-write\|danger-full-access` ([automation][cx-auto]) | `--auto` ([automation][oc-auto]) |
| Config isolation | `--bare` skips hooks, skills, agents, plugins, MCP, memory, CLAUDE.md; needs an API key ([automation][cc-auto]) | `--ignore-user-config`, `--ignore-rules`, `--ephemeral` ([automation][cx-auto]) | Not recorded ([automation][oc-auto]) |
| Repo hooks headless | Run without a trust prompt ([hooks][cc-hooks]) | Skipped until trusted by hash, unless `--dangerously-bypass-hook-trust` ([automation][cx-auto]) | Not recorded ([automation][oc-auto]) |
| API-key auth | `ANTHROPIC_API_KEY` or `apiKeyHelper` (required with `--bare`) ([automation][cc-auto]) | `CODEX_API_KEY` ([automation][cx-auto]) | Not recorded ([automation][oc-auto]) |
| SDK | Agent SDK, Python and TypeScript, `query()`; loads filesystem config unless `settingSources: []` ([automation][cc-auto]) | `@openai/codex-sdk` (TS), `openai-codex` (Python); thread objects; drive the local app-server ([automation][cx-auto]) | `@opencode-ai/sdk`; wraps `opencode serve` ([automation][oc-auto]) |
| Long-running server protocol | Not recorded ([automation][cc-auto]) | `codex app-server` (JSON-RPC, experimental) ([automation][cx-auto]) | `opencode serve` (HTTP, OpenAPI) ([automation][oc-auto]) |
| GitHub Action | `anthropics/claude-code-action@v1` ([automation][cc-auto]) | `openai/codex-action@v1` ([automation][cx-auto]) | `anomalyco/opencode/github@latest` ([automation][oc-auto]) |
| Action inputs | `prompt`, `claude_args`, API key or OAuth token, `github_token`, `settings`, `plugins`, `trigger_phrase` ([automation][cc-auto]) | `prompt`/`prompt-file`, `codex-args`, `model`, `effort`, `sandbox`, `openai-api-key`, `safety-strategy`, `allow-users` ([automation][cx-auto]) | `model` (required), `agent`, `prompt`, `mentions`, `share` ([automation][oc-auto]) |
| Comment-mention trigger | `@claude` in comments (interactive mode of the action) ([automation][cc-auto]) | `@codex review` on a PR, served by Codex Cloud, not the action ([automation][cx-auto]) | `/opencode`, `/oc` ([automation][oc-auto]) |
| Hosted (vendor cloud) runs | Routines and cloud sessions; use repo-committed and account skills, not `~/.claude/skills` ([automation][cc-auto]) | Codex Cloud tasks, `codex cloud exec --env`; environments carry repos, tools, network, secrets ([automation][cx-auto]) | None recorded ([automation][oc-auto]) |
| Local scheduled runs | Desktop scheduled tasks (min 1 min; machine on); `/loop` in an open session ([automation][cc-auto]) | Desktop-app scheduled tasks (app running, machine on) ([automation][cx-auto]) | None recorded ([automation][oc-auto]) |
| Hosted scheduled runs | Routines (min 1 h; cron via `/schedule`) ([automation][cc-auto]) | Web Scheduled page ([automation][cx-auto]) | GitHub Action `schedule` event on a GitHub runner ([automation][oc-auto]) |
| Schedule syntax | 5-field cron ([automation][cc-auto]) | RFC 5545 RRULE ([automation][cx-auto]) | GitHub Actions cron ([automation][oc-auto]) |
| Context per scheduled run | `/loop`: runs inside the open session; routines and desktop tasks run without an open session ([automation][cc-auto]) | Standalone task: new chat per run; in-chat task: keeps context ([automation][cx-auto]) | New run ([automation][oc-auto]) |
| Event triggers outside CI | Routines: HTTP API with bearer token, GitHub events ([automation][cc-auto]) | Gmail, Slack, GitHub PR triggers on ChatGPT web and mobile only ([automation][cx-auto]) | None recorded ([automation][oc-auto]) |
| Scheduling from the CLI | `/loop`, `/schedule` ([automation][cc-auto]) | Not available ([automation][cx-auto]) | n/a |
| Skills in scheduled prompts | Only model-invocable skills run ([automation][cc-auto]) | `$skill-name` in the task prompt ([automation][cx-auto]) | n/a |
| Goal-driven continuation | `/goal` ([automation][cc-auto]) | `/goal`, `goals` feature ([automation][cx-auto]) | Not recorded ([automation][oc-auto]) |
| Session worktree | `--worktree <name>` → `.claude/worktrees/<name>/`, branch `worktree-<name>` ([automation][cc-auto]) | CLI `--worktree`; desktop Worktree mode, detached HEAD, Handoff ([automation][cx-auto]) | None recorded ([automation][oc-auto]) |
| Worktree setup | `.worktreeinclude` copies gitignored files ([automation][cc-auto]) | Local environment setup scripts ([automation][cx-auto]) | n/a |

## Generalized model

### Run

A run is one agent session started without an interactive user.

| Part | Meaning |
| --- | --- |
| Prompt | Text from an argument, a file or stdin |
| Configuration set | Which config layers, instruction files, skills, subagents, hooks, plugins and MCP servers load. Default: the same discovery as an interactive session. Isolated: user or all discovered config skipped |
| Permission envelope | What the run may do without asking. No one is present to answer prompts, so the envelope must be set before the run starts |
| Trust | Whether project-level hooks and config run without a person confirming them |
| Output contract | Final text; an event stream (JSON lines); or a final object validated against a JSON Schema |
| Session handle | An ID to continue (resume) or branch (fork) the run later |
| Working copy | The checkout in place, or an isolated worktree |
| Credentials | An API key from the environment |

### Programmatic session (SDK)

A library that exposes the same agent loop as the CLI. It creates a session or thread, runs a turn with a prompt, returns the final response, and continues or resumes by ID. The SDK loads the same filesystem configuration as the CLI unless told otherwise.

### CI integration

A CI action installs the CLI, runs one headless run per workflow event, and passes through prompt, CLI arguments, model and credentials. Two trigger modes exist: event-driven with a fixed prompt, and comment-driven, where a mention in an issue or PR comment starts a run. CI-specific safety (who may trigger, privilege dropping, separate jobs for writing) is part of the action configuration.

### Hosted run

A run in the vendor's cloud environment against a cloned repository. It uses configuration committed to the repository plus account-level settings. It does not see the user's home-directory configuration. It keeps running when the local machine is off.

### Schedule

A schedule is a stored prompt plus a cadence that starts runs.

| Part | Meaning |
| --- | --- |
| Prompt | The task; may name a skill ("the skill defines the method, the schedule defines the timing") |
| Cadence | Recurrence rule; the syntax is vendor-specific |
| Execution site | Local machine (requires the app or session to be running) or hosted |
| Context | New session per run, or appended to an existing session |
| Permission policy | Unattended approval policy for the run |
| Working copy | Checkout in place or a dedicated worktree |

### Goal-driven continuation

A session-level goal that keeps the agent working across turns until a condition is met. Both leads expose it as `/goal`; the pages record no configuration beyond the command and the Codex feature flag.

### Worktree isolation

A run or session can start in a new git worktree, so parallel runs do not touch the main checkout. Untracked files the work needs (such as `.env`) must be copied or created by a setup step.

### Mapping

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Headless run | `claude -p` | `codex exec` | `opencode run` |
| Event stream output | `--output-format stream-json` | `--json` | `--format json` |
| Schema-validated output | `--json-schema` | `--output-schema` | SDK `format.json_schema` |
| Resume | `--resume <id>`, `--continue` | `codex exec resume <id>`, `--last` | `--session`, `--continue` |
| Fork | SDK session fork, `/fork` | `codex exec fork` | `--fork` |
| Isolated configuration set | `--bare`, SDK `settingSources: []` | `--ignore-user-config`, `--ignore-rules` | — |
| Permission envelope | `--allowedTools`, `--permission-mode` | `--sandbox` | `--auto`, `permission` config |
| SDK | Claude Agent SDK | Codex SDK | `@opencode-ai/sdk` |
| CI action | `claude-code-action` | `codex-action` | `opencode/github` |
| Comment-mention trigger | `@claude` | `@codex review` (cloud) | `/opencode`, `/oc` |
| Hosted run | Routine, cloud session | Cloud task | — |
| Local schedule | Desktop scheduled task | Desktop-app scheduled task | — |
| Hosted schedule | Routine | Web scheduled task | GitHub Action `schedule` event |
| Goal-driven continuation | `/goal` | `/goal` | — |
| Session worktree | `--worktree <name>` | `--worktree` | — |
| Worktree setup step | `.worktreeinclude` | Local environment setup script | — |

## Portability

### Headless runs

- **Equivalent flags differ in name.** Map them through the table above. There is no shared flag set.
- **Defaults point in opposite directions.** `codex exec` is read-only unless `--sandbox workspace-write` is given ([automation][cx-auto]). Claude Code `-p` runs in `default` or `auto` permission mode ([automation][cc-auto]). Set the envelope explicitly in every script.
- **Trust differs.** Claude Code `-p` and SDK runs load a repository's hooks and MCP servers without a trust prompt; the docs recommend `--bare` for scripted runs ([automation][cc-auto]). Codex skips untrusted project config and untrusted hooks in `codex exec` ([automation][cx-auto], [hooks][cx-hooks]). A hook that gates a CI run in Claude Code may silently not run in Codex until trusted.
- **Config isolation is not symmetric.** `--bare` skips all discovered configuration, including skills and instruction files. Codex's flags skip only user config and rules files ([automation][cc-auto], [automation][cx-auto]). A run that depends on project skills must not use `--bare`.
- **Structured output.** Both leads accept a JSON Schema; Claude Code takes it inline, Codex from a file ([automation][cc-auto], [automation][cx-auto]). Keep the schema in a file and pass its contents to Claude Code.
- **Git.** `codex exec` requires a git repository unless `--skip-git-repo-check` is set ([automation][cx-auto]).

### CI

- Both actions take a prompt and a pass-through for CLI arguments (`claude_args`, `codex-args`), so the headless mapping applies inside the action ([automation][cc-auto], [automation][cx-auto]).
- Comment-driven review is not symmetric: Claude Code handles `@claude` through the action; Codex handles `@codex review` through Codex Cloud, with review rules in a `## Code Review Rules` section of `AGENTS.md` ([automation][cx-auto]).
- Codex documents an autofix pattern: the agent job runs with `contents: read` and produces a patch artifact; a separate job without the API key opens the PR ([automation][cx-auto]). It does not depend on Codex features and applies to both.
- Do not expose the API key at job level in workflows that run repository code ([automation][cx-auto]).

### Scheduling

- Neither lead schedules from a plain CLI on a headless machine: Claude Code's `/loop` needs an open session, and Codex's CLI has no scheduling interface ([automation][cc-auto], [automation][cx-auto]). Inference from the Codex page: system cron plus the headless CLI is the fallback; it is not an official feature of either vendor.
- Cadence syntax differs (cron vs RRULE). Store the intent, not the expression.
- Put the method in a skill and name it in the schedule prompt. Trap: Claude Code runs only model-invocable skills from scheduled fires, so a skill marked `disable-model-invocation: true` does not run there ([automation][cc-auto]). See [skills.md](skills.md#invocation-policy-in-both-leads).
- Scheduled runs in worktrees accumulate worktrees; Codex advises archiving old runs ([automation][cx-auto]).

### Hosted runs

Hosted runs in both leads use what the repository carries. Claude Code routines and cloud sessions ignore `~/.claude/skills` ([automation][cc-auto]). The Codex pages do not say that cloud tasks read local `config.toml` ([README][cx-readme]). Commit every skill, instruction file and hook a hosted run needs.

### Worktrees

Both leads start a session in a new worktree with `--worktree`. Claude Code takes a name and creates `.claude/worktrees/<name>/` on branch `worktree-<name>` ([automation][cc-auto]); the Codex CLI flag's location and branch naming are not recorded, and the desktop app uses a detached HEAD ([automation][cx-auto]). Untracked files need a setup step in each lead: `.worktreeinclude` in Claude Code, a local environment setup script in Codex.

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| Dynamic workflows (JavaScript orchestration scripts, `ultracode`) | Claude Code | No Codex counterpart. |
| Agent teams | Claude Code | No Codex counterpart; see [subagents.md](subagents.md). |
| `/batch` (5–30 worktree-isolated subagents) | Claude Code | Bundled skill with no Codex counterpart. |
| `/loop` as a CLI-session scheduler with self-pacing and `loop.md` | Claude Code | Codex in-chat scheduled tasks exist only in the desktop app; the session-bound loop has no CLI counterpart. |
| Cron tools (`CronCreate`, `CronList`, `CronDelete`) | Claude Code | Claude-only tool interface. Codex states that skills can create or update scheduled tasks but records no mechanism. |
| Routine API trigger (HTTP POST with bearer token) | Claude Code | No documented API trigger for Codex scheduled tasks. |
| Checkpoints and `/rewind` | Claude Code | No Codex counterpart recorded. |
| Plan mode | Claude Code, Codex | Both have `/plan`, but the Codex pages record no semantics; belongs to permission modes, not automation. |
| Channels (MCP servers pushing events into a session) | Claude Code | No Codex counterpart. |
| Background sessions (`claude --bg`, agent view) | Claude Code | No Codex counterpart recorded; `codex agents` is a session browser. |
| Hook `defer` decision in `-p` | Claude Code | Codex does not support it. |
| `--max-budget-usd` | Claude Code | No Codex counterpart. |
| `codex review` headless subcommand and `/review` | Codex | Claude Code has review skills but no headless review subcommand; built-in features, not configuration. |
| `@codex review` automatic review and `## Code Review Rules` | Codex | Hosted review service with no Claude Code counterpart recorded (Claude Code's managed review was not researched). |
| App-server JSON-RPC protocol | Codex | No Claude Code counterpart recorded; OpenCode's server does not decide. |
| Cloud best-of-N (`--attempts 1-4`) | Codex | No Claude Code counterpart. |
| `codex cloud apply`/`diff`, `codex apply` | Codex | No Claude Code counterpart recorded. |
| `safety-strategy` action input | Codex | No Claude Code counterpart. |
| `codex queue`, `remote-control`, `exec-server` | Codex | Experimental or single-vendor. |
| Event triggers on Gmail, Slack | Codex (ChatGPT web) | No Claude Code counterpart. |
| `opencode serve`, `--attach`, ACP | OpenCode | No Claude Code counterpart. |
| Session sharing (`/share`, `opncd.ai` links) | OpenCode | No lead counterpart. |

## Sources

- [Claude Code: automation](../vendors/claude-code/automation.md)
- [Claude Code: hooks](../vendors/claude-code/hooks.md)
- [Claude Code: subagents](../vendors/claude-code/subagents.md)
- [Codex: automation](../vendors/codex/automation.md)
- [Codex: hooks](../vendors/codex/hooks.md)
- [Codex: subagents](../vendors/codex/subagents.md)
- [Codex: README](../vendors/codex/README.md)
- [OpenCode: automation](../vendors/opencode/automation.md)
- [Research notes](../research-notes/agent-harness-configuration/)

[cc-auto]: ../vendors/claude-code/automation.md
[cc-hooks]: ../vendors/claude-code/hooks.md
[cc-sub]: ../vendors/claude-code/subagents.md
[cx-auto]: ../vendors/codex/automation.md
[cx-hooks]: ../vendors/codex/hooks.md
[cx-sub]: ../vendors/codex/subagents.md
[cx-readme]: ../vendors/codex/README.md
[oc-auto]: ../vendors/opencode/automation.md
