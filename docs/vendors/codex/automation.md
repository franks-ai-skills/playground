# Automation

Codex can run without an interactive session through several surfaces: the headless CLI (`codex exec`, `codex review`), SDKs for TypeScript and Python, the app-server JSON-RPC protocol, a GitHub Action, cloud tasks and GitHub code review, and scheduled tasks in the desktop app. These surfaces cover CI jobs, structured-output pipelines, custom clients and recurring work ([Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md); [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk.md); [Scheduled tasks](https://learn.chatgpt.com/docs/automations.md)).

## Locations and scopes

| Surface | Runs where | Configured by |
|---|---|---|
| `codex exec` | Local machine or CI runner | CLI flags plus the normal `config.toml` layers ([configuration.md](configuration.md)) |
| `codex review` | Local machine or CI runner | CLI flags |
| `/review` | CLI, IDE extension, desktop app | `review_model` |
| TypeScript SDK `@openai/codex-sdk` | Drives the local app-server | Code |
| Python SDK `openai-codex` | Drives the local app-server over JSON-RPC; pins a Codex CLI runtime | Code |
| App-server (`codex app-server`) | Local; custom clients | JSON-RPC protocol |
| GitHub Action `openai/codex-action@v1` | GitHub Actions runner | Action inputs |
| GitHub cloud review (`@codex review`, automatic review) | Codex Cloud | Codex settings, `## Code Review Rules` in `AGENTS.md` |
| Codex Cloud tasks, `codex cloud` | Cloud environments | Cloud environment (repos, tools, network, secrets) |
| Scheduled tasks | Desktop app (local checkout or worktree) or web | Desktop app or web **Scheduled** page |

## Format

### `codex exec`

| Flag / input | Effect |
|---|---|
| `PROMPT` | Prompt text. Without a prompt, or with `-`, the prompt is read from stdin. When both are given, stdin is appended as a `<stdin>` block |
| `--sandbox read-only\|workspace-write\|danger-full-access` | Sandbox; default is read-only |
| `--full-auto` | "Deprecated compatibility flag"; use `--sandbox workspace-write` |
| `--json` (alias `--experimental-json`) | Stdout becomes JSONL events |
| `-o/--output-last-message <file>` | Writes the final message to a file |
| `--output-schema <file>` | JSON Schema for the final response |
| `--ephemeral` | Does not write rollout files |
| `--skip-git-repo-check` | Allows running outside a Git repository |
| `--ignore-user-config` | Does not load `$CODEX_HOME/config.toml`; auth still uses `CODEX_HOME` |
| `--ignore-rules` | Skips user and project `.rules` files |
| `--dangerously-bypass-hook-trust` | Skips hook trust for this invocation |
| `--thread-source`, `--worktree` | Present in 0.159.2 |
| `codex exec resume --last "follow-up"` | Resume the last session in the cwd; `--all` searches all directories |
| `codex exec resume <SESSION_ID\|name>` | Resume a specific session |
| `codex exec fork`, `codex exec review` | Present in 0.159.2 |

Sources: [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md); [CLI command reference](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli); local `codex exec --help`.

**JSONL event types** (`--json`): `thread.started`, `turn.started`, `turn.completed` (with `usage`), `turn.failed`, `item.*`, `error`. Item types: agent messages, reasoning, command executions, file changes, MCP tool calls, web searches, plan updates ([Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)).

### `codex review`

`codex review [--uncommitted | --base BRANCH | --commit SHA [--title T] | PROMPT|-]`. The targets are mutually exclusive ([CLI command reference](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli); local `codex review --help`).

### SDKs

| SDK | Install | Usage |
|---|---|---|
| TypeScript | `npm install @openai/codex-sdk` (Node 18+) | `new Codex().startThread().run(prompt)` returns `result.finalResponse`. Calling `run()` again continues the thread; `resumeThread(id)` resumes one |
| Python (stable) | `pip install openai-codex` (Python 3.10+) | `Codex()` / `AsyncCodex()`, `thread_start(model=..., sandbox=Sandbox.workspace_write)`, `thread.run(...)` returns `.final_response`. Sandbox presets: `read_only`, `workspace_write`, `full_access`. A per-turn sandbox persists to later turns |

Source: [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk.md).

### App-server

`codex app-server` (marked experimental in the CLI table) is the protocol for custom clients: threads, turns, `turn/steer`, `turn/interrupt`, `skills/list`, `skills/config/write` and more ([Codex App Server](https://learn.chatgpt.com/docs/app-server.md); [CLI command reference](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)). Local 0.159.2 subcommands: `daemon`, `proxy`, `generate-ts`, `generate-json-schema`. It replaces the removed `codex mcp-server` ([mcp.md](mcp.md)).

### GitHub Action (`openai/codex-action@v1`)

The action installs the CLI, starts a Responses API proxy when `openai-api-key` is given, and runs `codex exec` ([Codex GitHub Action](https://learn.chatgpt.com/docs/github-action.md)).

| Input | Meaning | Default |
|---|---|---|
| `prompt` / `prompt-file` | Prompt; exactly one is required | |
| `openai-api-key` | Starts the Responses API proxy | |
| `codex-args` | Extra CLI arguments; JSON array or shell string | |
| `model` | Model | |
| `effort` | Reasoning effort | |
| `sandbox` | Sandbox mode | |
| `output-file` | File for the final message | |
| `codex-version` | CLI version | |
| `codex-home` | `CODEX_HOME` | |
| `safety-strategy` | `drop-sudo`, `unprivileged-user` (with `codex-user`), `read-only` or `unsafe` (required on Windows) | `drop-sudo` |
| `allow-users`, `allow-bots` | Who may trigger the action | |

Output: `final-message`.

### Codex Cloud

- Cloud tasks run in published cloud environments (repos, tools, network and secrets). "Each task has its own workspace and can keep working while your computer is asleep." Codex Cloud (Legacy) environments still back Code Review and the Linear and GitHub integrations; they use the `universal` image, setup and maintenance scripts, and agent internet access off by default ([Codex Cloud](https://learn.chatgpt.com/docs/cloud.md); [Codex Cloud (Legacy)](https://learn.chatgpt.com/docs/environments/cloud-environment.md)).
- `codex cloud` (experimental; alias `codex cloud-tasks`): an interactive picker plus these subcommands ([CLI command reference](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli); local `codex cloud --help`):

| Subcommand | Flags |
|---|---|
| `exec` | `--env ENV_ID` (required), `--attempts 1-4` (best-of-N, default 1) |
| `list` | `--json` (includes `attempt_total`), `--limit 1-20`, `--cursor`, `--env` |
| `status` | |
| `diff` | |
| `apply` | |

`codex apply` applies the latest cloud diff locally.

### Scheduled tasks (formerly "Automations")

| Element | Value |
|---|---|
| Where managed | ChatGPT desktop app or the web **Scheduled** page. Not the CLI and not the IDE extension |
| Task kinds (desktop) | Standalone task (new chat per run; can span several projects) or a task inside an existing chat (keeps context; minute-based intervals allowed) |
| Schedule | A custom cadence uses an RFC 5545 RRULE, for example `RRULE:FREQ=MONTHLY;BYMONTHDAY=1;BYHOUR=9;BYMINUTE=0` |
| Execution (Git projects) | In the local checkout or in a dedicated background worktree |
| Approvals | `approval_policy = "never"` when policy allows it; otherwise the selected permission mode |
| Skills | Prompts can use `$skill-name`; skills can create or update scheduled tasks |
| Event triggers | Gmail, Slack and GitHub PR activity triggers exist only on ChatGPT web and mobile, and cannot be combined with a time schedule |

Source: [Scheduled tasks](https://learn.chatgpt.com/docs/automations.md). Guidance: "skills define the method and scheduled tasks define the schedule" ([Best practices](https://learn.chatgpt.com/docs/codex-manual.md)).

### Worktrees

- Desktop app: Worktree mode runs chats in Git worktrees (detached HEAD by default). "Handoff" moves a chat between Local and Worktree. Local environments supply setup scripts for worktrees ([Worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees.md); [Local environments](https://learn.chatgpt.com/docs/environments/local-environment.md)).
- CLI: `--worktree` ("Run the session in a new managed Git worktree"); the `worktrees` feature is stable and on (local `codex --help`, `codex features list`).

### Other CLI commands (local 0.159.2)

`codex queue` ("Queue a message for an existing session"), `codex fork`, `codex resume`, `codex remote-control` (experimental), `codex exec-server` (experimental), `codex agents` (agent command center, see [subagents.md](subagents.md)). The `goals` feature (persisted goals and automatic continuation, `/goal`) is stable and on ([Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference.md)).

## Loading and invocation

- **Output.** `codex exec` streams progress to stderr and prints only the final message to stdout ([Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)).
- **Git requirement.** A Git repository is required unless `--skip-git-repo-check` is set.
- **Required MCP servers.** An MCP server with `required = true` that fails to start makes `codex exec` exit with an error ([mcp.md](mcp.md)).
- **Auth.** `CODEX_API_KEY=<key> codex exec ...` works for `codex exec`, `codex review`, the TypeScript SDK and `codex exec-server --remote`. Do not set the key at job level in workflows that run repository code. ChatGPT-managed `auth.json` in CI is "advanced" and not for public repositories ([Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)).
- **`/review`** "starts a dedicated reviewer that reads the selected diff and reports prioritized, actionable findings without changing your working tree". Presets: base branch and uncommitted changes. It uses the session model unless `review_model` is set ([Code review](https://learn.chatgpt.com/docs/code-review.md)).
- **GitHub cloud review.** Comment `@codex review` on a PR, or turn on Automatic review in Codex settings. On GitHub, Codex flags only P0/P1 issues. Review rules come from a `## Code Review Rules` section in the nearest `AGENTS.md` ([instructions.md](instructions.md)). GitLab merge-request review is in preview ([Review GitHub pull requests with Codex](https://learn.chatgpt.com/docs/third-party/github.md); [Code review](https://learn.chatgpt.com/docs/code-review.md)).
- **Scheduled tasks** run only while the desktop app is running and the machine is on ([Scheduled tasks](https://learn.chatgpt.com/docs/automations.md)).
- **CI autofix pattern.** The Codex job runs with `contents: read` and produces a patch artifact; a separate job with write permissions and no API key opens the PR ([Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)).

## Example

Structured output from `codex exec`:

```sh
codex exec "Extract project metadata" --output-schema ./schema.json -o ./project-metadata.json
```

Source: [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md).

Follow-up in the same session:

```sh
codex exec resume --last "follow-up"
```

## Limits and gotchas

- **`--full-auto` is deprecated** and prints a warning; use `--sandbox workspace-write` ([Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)).
- **`codex exec` is read-only by default.** Pass `--sandbox workspace-write` to let it edit files.
- **No scheduling from the CLI.** "Codex CLI doesn't provide the Scheduled management interface", and neither does the IDE extension ([Scheduled tasks](https://learn.chatgpt.com/docs/automations.md)). Inference: on a headless machine, plain cron plus `codex exec` is the fallback; this is not an official feature.
- **Worktree buildup.** Frequent scheduled tasks can pile up worktrees; archive old runs ([Scheduled tasks](https://learn.chatgpt.com/docs/automations.md)).
- **Experimental surfaces.** `codex cloud`, `codex app-server`, `codex remote-control` and `codex exec-server` are marked experimental. The app-server is not supported for production ([Agents SDK guide](https://developers.openai.com/codex/guides/agents-sdk)).
- **`codex mcp-server` removed** on 2026-09-05; use the SDKs or app-server ([mcp.md](mcp.md)).
- **Inference: choosing a surface.** For CI, use `openai/codex-action` with `--output-schema` passed through `codex-args`. For long-running or multi-turn pipelines, use the SDKs, or `codex exec` plus `exec resume`. Recurring local jobs need the desktop app.
- **Gap:** the detailed Cloud environments page (setup scripts, secrets, saved state) and the GitHub, Linear and Slack integration triggers beyond `@codex review` were not read.
- **Gap:** no documented way to start scheduled tasks or event triggers from the CLI or an API. Team Tasks run through service accounts and are an admin feature not explored.

## Sources

- https://learn.chatgpt.com/docs/non-interactive-mode.md
- https://learn.chatgpt.com/docs/developer-commands.md?surface=cli
- https://learn.chatgpt.com/docs/code-review.md
- https://learn.chatgpt.com/docs/third-party/github.md
- https://learn.chatgpt.com/docs/codex-sdk.md
- https://learn.chatgpt.com/docs/app-server.md
- https://learn.chatgpt.com/docs/github-action.md
- https://learn.chatgpt.com/docs/cloud.md
- https://learn.chatgpt.com/docs/environments/cloud-environment.md
- https://learn.chatgpt.com/docs/automations.md
- https://learn.chatgpt.com/docs/codex-manual.md
- https://learn.chatgpt.com/docs/environments/git-worktrees.md
- https://learn.chatgpt.com/docs/environments/local-environment.md
- https://learn.chatgpt.com/docs/config-file/config-reference.md
- https://developers.openai.com/codex/guides/agents-sdk
