# Automation

Claude Code can run without an interactive user and can orchestrate work beyond a single conversation. The surfaces are headless runs (`claude -p`), the Agent SDK (Python and TypeScript), GitHub Actions, schedulers (`/loop`, desktop scheduled tasks, cloud routines), and dynamic workflows (JavaScript scripts that fan out many subagents). Worktrees, plan mode, and checkpoints are the in-session safety and parallelism tools that these surfaces build on ([headless](https://code.claude.com/docs/en/headless); [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview); [workflows](https://code.claude.com/docs/en/workflows)).

## Locations and scopes

| Surface | Where it runs | Where it is configured |
| :- | :- | :- |
| Headless `claude -p` | Local machine or CI | CLI flags; auto-discovers hooks, skills, commands, agents, plugins, MCP, auto memory, and CLAUDE.md unless `--bare` |
| Agent SDK | Your process | `options` in code; `settingSources` controls which settings files load |
| GitHub Actions | GitHub runner | Workflow YAML using `anthropics/claude-code-action@v1` |
| `/loop` and cron tools | Open session | In-session; `.claude/loop.md` or `~/.claude/loop.md` for the default prompt |
| Desktop scheduled tasks | Local machine | Desktop app |
| Routines | Anthropic cloud (or a self-hosted environment) | claude.ai/code/routines or `/schedule` |
| Dynamic workflows | Background runtime in the session | `.claude/workflows/`, `~/.claude/workflows/`, plugin `workflows/` |
| Worktrees | `.claude/worktrees/<name>/` | `--worktree`, `worktree.*` settings, `.worktreeinclude` |

Sources: [headless](https://code.claude.com/docs/en/headless); [SDK features](https://code.claude.com/docs/en/agent-sdk/claude-code-features); [GitHub Actions](https://code.claude.com/docs/en/github-actions); [scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks); [routines](https://code.claude.com/docs/en/routines); [workflows](https://code.claude.com/docs/en/workflows); [worktrees](https://code.claude.com/docs/en/worktrees); [settings reference](https://code.claude.com/docs/en/settings-reference)

- SDK `settingSources` / `setting_sources`: omitting it equals `["user","project","local"]`, so the SDK loads filesystem configuration like the CLI. Pass `[]` to isolate ([SDK features](https://code.claude.com/docs/en/agent-sdk/claude-code-features)).
- Routines and cloud sessions use skills committed to the repo plus claude.ai-enabled skills, not `~/.claude/skills` ([routines](https://code.claude.com/docs/en/routines); [skills](https://code.claude.com/docs/en/skills)).

## Format

### Headless flags

From [headless](https://code.claude.com/docs/en/headless) unless noted:

| Flag | Meaning |
| :- | :- |
| `-p` / `--print` | Non-interactive run; exit code 0 means success |
| `--output-format text\|json\|stream-json` | `text` (default); `json` with `result`, `session_id`, `total_cost_usd`; `stream-json` (NDJSON; add `--verbose --include-partial-messages` for token streaming) |
| `--json-schema` | Schema-validated output in `structured_output`. Since v2.1.205 an invalid schema is an error |
| `--allowedTools` | Permission-rule syntax, e.g. `Bash(git diff *)`; the space before `*` matters |
| `--permission-mode` | `auto`, `dontAsk`, `acceptEdits`, or `plan` |
| `--permission-prompts none` | Unattended runs (v2.1.259+) |
| `--append-system-prompt`, `--system-prompt` | System prompt control |
| `--continue`, `--resume <id>` | Continue a session |
| `--bare` | Skips auto-discovery of hooks, skills, commands, agents, plugins, MCP, auto memory, and CLAUDE.md. Requires `ANTHROPIC_API_KEY` or an `apiKeyHelper`; no OAuth |
| `--max-budget-usd` | With `--print` (local CLI help) |
| `--input-format`, `--agents <json-or-file>`, `--plugin-dir`, `--setting-sources`, `--safe-mode`, `--bg`/`--background`, `-w`/`--worktree` | Further flags (local CLI help) |

### Agent SDK

From the [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) and [SDK features](https://code.claude.com/docs/en/agent-sdk/claude-code-features):

- It "gives you the same tools, agent loop, and context management that power Claude Code" in Python and TypeScript.
- Imports: TypeScript `import { query } from "@anthropic-ai/claude-agent-sdk"`; Python `from claude_agent_sdk import query, ClaudeAgentOptions`.
- Capabilities: built-in tools, hooks (callbacks; see [hooks.md](hooks.md)), subagents (`agents`; see [subagents.md](subagents.md)), MCP, permissions, sessions (resume and fork), skills, commands and memory from `.claude/`, and plugins by local path.

### GitHub Actions

From [GitHub Actions](https://code.claude.com/docs/en/github-actions):

- Action: `anthropics/claude-code-action@v1`.
- Setup: `/install-github-app` (github.com only), or manually install the app, add a secret, and copy `examples/claude.yml`.
- Modes, detected automatically: interactive (responds to `@claude` in comments); automation (when a `prompt` input is given, on any event including cron).

| Input | Purpose |
| :- | :- |
| `prompt` | Automation prompt |
| `claude_args` | CLI arguments (e.g. model, max turns, system prompt) |
| `anthropic_api_key`, `claude_code_oauth_token` | Auth |
| `github_token` | GitHub auth |
| `plugin_marketplaces`, `plugins` | Plugins |
| `settings` | Settings |
| `trigger_phrase` | Interactive trigger |
| `use_bedrock`, `use_vertex`, `use_foundry` | Provider |

### Scheduling

`/loop [interval] [prompt]` is a bundled skill ([scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks)):

- A fixed interval (s/m/h/d) is converted to cron.
- With no interval, Claude self-paces between 1 minute and 1 hour.
- With no prompt, a built-in maintenance prompt runs, or `.claude/loop.md` / `~/.claude/loop.md` if present.
- Tools: `CronCreate` (5-field cron), `CronList`, `CronDelete`.

Comparison ([scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks)):

| | Cloud routines | Desktop tasks | `/loop` |
| :- | :- | :- | :- |
| Minimum interval | 1 hour | 1 minute | 1 minute |
| Needs machine on | No | Yes | Yes |
| Needs open session | No | No | Yes |

Routines ([routines](https://code.claude.com/docs/en/routines)):

- Research preview. A saved prompt + repos + connectors, run on Anthropic cloud (or a self-hosted environment).
- Triggers: schedule (hourly / daily / weekdays / weekly, custom cron via `/schedule update` with a 1-hour minimum, or a one-off run); API (HTTP POST with a per-routine bearer token); GitHub (e.g. `pull_request.opened`; requires the Claude GitHub App).
- Create and manage at claude.ai/code/routines or via `/schedule` (alias `/routines`).
- Plans: Pro, Max, Team, Enterprise.

### Dynamic workflows

From [workflows](https://code.claude.com/docs/en/workflows):

- "A dynamic workflow is a JavaScript script that orchestrates many subagents at once. Claude writes the script… a runtime executes it in the background."
- Script API: `export const meta = {name, description}` must be the first statement. Functions: `agent(prompt, {schema, label})`, `pipeline(items, fn)`, `parallel()`, `phase()`, `log()`, and an `args` global.
- Restrictions: no `import()`, no direct filesystem or shell access. `Date.now()` and `Math.random()` throw, for deterministic resume.
- Saving: `/workflows` → `s` saves to `.claude/workflows/` or `~/.claude/workflows/`, runnable as `/<name>`. Plugins ship workflows in `workflows/`.
- Bundled workflow: `/deep-research`.

### Worktrees

From [worktrees](https://code.claude.com/docs/en/worktrees):

- `claude --worktree <name>` (`-w`) creates `.claude/worktrees/<name>/` on branch `worktree-<name>`.
- `.worktreeinclude` copies gitignored files such as `.env` into the worktree.
- `EnterWorktree` / `ExitWorktree` tools let Claude switch worktrees in-session.
- Subagents can use `isolation: worktree` ([subagents.md](subagents.md#worktree-isolation)).
- `WorktreeCreate` / `WorktreeRemove` hooks support non-git version control ([hooks.md](hooks.md)).

## Loading and invocation

### Headless

- Default `-p` loads repo hooks and MCP servers without trust prompts; project allow rules are not used ([permissions](https://code.claude.com/docs/en/permissions); [hooks reference](https://code.claude.com/docs/en/hooks); [MCP](https://code.claude.com/docs/en/mcp)).
- Built-in default permission mode in `-p` and the SDK: `default` in sessions that fetch feature flags, otherwise `auto` (v2.1.285+) ([permission modes](https://code.claude.com/docs/en/permission-modes)).
- Subagents in `-p`/SDK: fork mode is off; Claude chooses foreground or background, default background. `context: fork` skills run in the foreground. No agent-team teammates are spawned ([subagents](https://code.claude.com/docs/en/sub-agents); [skills](https://code.claude.com/docs/en/skills); [agent teams](https://code.claude.com/docs/en/agent-teams)).
- Inference (from the research notes): the safest CI baseline is `--bare` plus explicit `--allowedTools` / `--settings`.

### Scheduling behavior

- `/loop` tasks are session-scoped and restored on `--resume`. Recurring tasks expire after 7 days, and a jitter applies ([scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks)).
- Scheduled fires only run model-invocable skills; `disable-model-invocation` blocks a skill from running from a scheduled task since v2.1.196 ([scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks); [skills](https://code.claude.com/docs/en/skills)).
- Routine runs are autonomous, with no permission picker ([routines](https://code.claude.com/docs/en/routines)).

### Dynamic workflows

- Triggers: the `ultracode` keyword in a typed prompt (renamed from `workflow` in v2.1.160); a direct request in your own words; `/effort ultracode` for a whole session ([workflows](https://code.claude.com/docs/en/workflows); [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- Limits: 16 concurrent agents by default (configurable 1–256), 4,096 items per `parallel`/`pipeline`, 1,000 agents per run. Runs are resumable within the session ([workflows](https://code.claude.com/docs/en/workflows)).
- The concurrent-subagent limit of 20 is not enforced when ultracode is on ([subagents](https://code.claude.com/docs/en/sub-agents)).
- `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` also applies to workflow agents ([subagents](https://code.claude.com/docs/en/sub-agents)).
- Disable with `disableWorkflows` or `CLAUDE_CODE_DISABLE_WORKFLOWS=1` ([workflows](https://code.claude.com/docs/en/workflows)).

### Plan mode

From [permission modes](https://code.claude.com/docs/en/permission-modes):

- Claude "reads files, runs shell commands to explore, and writes a plan, but does not edit your source". Edits stay blocked until the plan is approved.
- Enter with Shift+Tab, `/plan [task]`, or `--permission-mode plan`.
- Shell commands during planning are reviewed by the auto-mode classifier when `useAutoModeDuringPlan` is on (the default).
- The built-in Plan subagent does the research.
- `opusplan` model alias: Opus in plan mode, Sonnet for execution ([model config](https://code.claude.com/docs/en/model-config)).

### Checkpoints

From [checkpointing](https://code.claude.com/docs/en/checkpointing):

- A checkpoint is taken before each user prompt that starts a turn. The last 100 checkpoints are kept, and they persist across resume.
- `/rewind` (or Esc twice; aliases `/checkpoint`, `/undo`) offers: restore code and conversation, restore conversation only, restore code only, summarize from here, or summarize up to here.

### Other automation-adjacent features

- `/goal`: keeps Claude working across turns until a condition is met ([commands](https://code.claude.com/docs/en/commands)).
- `/batch`: 5–30 worktree-isolated background subagents ([commands](https://code.claude.com/docs/en/commands)).
- Channels (research preview): MCP servers that push events into a running session ([channels](https://code.claude.com/docs/en/channels)).
- Background sessions: `claude --bg`, `/background`, managed in agent view (`claude agents`) ([agent view](https://code.claude.com/docs/en/agent-view)). See [subagents.md](subagents.md#other-parallel-features).
- Inference (from the research notes): the orchestration options differ by who holds the plan: Claude turn by turn (skills, subagents), a lead agent (agent teams), a script (workflows), or a scheduler (routines, loops). The workflows page's comparison table is the best single source for this framing.

## Example

Headless with structured output ([headless](https://code.claude.com/docs/en/headless)):

```bash
claude --bare -p "List exported functions in src/" --allowedTools "Read,Grep" \
  --output-format json --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

Dynamic workflow `.claude/workflows/audit-routes.js` ([workflows](https://code.claude.com/docs/en/workflows)):

```javascript
export const meta = { name: 'audit-routes', description: 'Audit every route handler for missing auth checks' }
const found = await agent('List every .ts file under src/routes/.', { schema: { type: 'object', required: ['files'], properties: { files: { type: 'array', items: { type: 'string' } } } } })
const audits = await pipeline(found.files, file => agent(`Audit ${file} for missing authentication checks.`, { label: file }))
return audits.filter(Boolean)
```

## Limits and gotchas

- `--bare` "is the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release" ([headless](https://code.claude.com/docs/en/headless)).
- With `-p`, broken settings files or entries are silently skipped; `claude doctor` lists rejected entries ([settings](https://code.claude.com/docs/en/settings)).
- Hook `defer` decisions work only in `-p`; the run exits with `stop_reason: "tool_deferred"`. Async hooks are killed at teardown in `-p` ([hooks reference](https://code.claude.com/docs/en/hooks)).
- Agent SDK rename: "The Claude Code SDK is now the Claude Agent SDK" (2.0.0) ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)). Third-party products may not offer claude.ai login ([Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)).
- GitHub Actions upgrade from `@beta`: drop `mode`, rename `direct_prompt` to `prompt`, move `max_turns` and `model` into `claude_args`, and turn `custom_instructions` into `--append-system-prompt` ([GitHub Actions](https://code.claude.com/docs/en/github-actions)).
- Routine limits: 100 scheduled runs per hour per account; 30 per hour per routine for Run now / API ([routines](https://code.claude.com/docs/en/routines)).
- `/loop` was added in v2.1.71; dynamic workflows in v2.1.154 ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- Checkpoints do not track Bash-made changes, background subagent edits, external edits, symlinked or hard-linked files, or mid-turn messages. "Not a replacement for version control" ([checkpointing](https://code.claude.com/docs/en/checkpointing)).
- Background `context: fork` skill edits bypass checkpoints ([skills](https://code.claude.com/docs/en/skills)).
- Worktrees: on exit, Claude checks for unsaved work before removing the worktree ([worktrees](https://code.claude.com/docs/en/worktrees)). Auto memory is shared across worktrees of one repo ([memory](https://code.claude.com/docs/en/memory)).
- Gap (research notes): not read in detail — desktop scheduled tasks, the GitLab CI/CD page, Code Review (managed PR review), ultrareview, the Agent SDK sessions and permissions pages, and the mods pages.
- Gap (research notes): the exact PyPI and npm install commands for the Agent SDK were not captured, only the import names.
- Gap (research notes): projects (claude.ai/code threads) and cross-session messaging were seen only in the overview table.

## Sources

- https://code.claude.com/docs/en/headless
- https://code.claude.com/docs/en/agent-sdk/overview
- https://code.claude.com/docs/en/agent-sdk/claude-code-features
- https://code.claude.com/docs/en/github-actions
- https://code.claude.com/docs/en/scheduled-tasks
- https://code.claude.com/docs/en/routines
- https://code.claude.com/docs/en/workflows
- https://code.claude.com/docs/en/worktrees
- https://code.claude.com/docs/en/permission-modes
- https://code.claude.com/docs/en/checkpointing
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/channels
- https://code.claude.com/docs/en/agent-view
- https://code.claude.com/docs/en/agent-teams
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/permissions
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/settings-reference
- https://code.claude.com/docs/en/model-config
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- Local CLI help: `claude --help` (v2.1.289)
