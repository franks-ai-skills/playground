# Agent harness overview

The generalized agent-harness concepts on one page: what each one is
used for, how and when it is used, and when it should not be used. It
applies to Claude Code and Codex as equal leads, with OpenCode where it
matches. Each section links to the full [guide](guide/) page, which has
the comparison, practices with sources, security, a checklist and the
portability traps.

## At a glance

| Concept | Used for | Use it when | Do not use it when → use instead |
| --- | --- | --- | --- |
| [Instructions](#instructions) | Standing guidance loaded into every session | Short, stable facts every session needs and the agent cannot derive: commands, non-default conventions, gotchas, "done" | A procedure needed only sometimes → skill. A rule that must always hold → hook or permission rule. Long reference → `docs/` with a pointer |
| [Configuration](#configuration) | Layered settings that control the harness | Deciding which layer (policy, user, project, run) owns a setting | Conventions and workflow → instructions or skills. Secrets → secret manager. Merge gate → CI |
| [Permissions and sandbox](#permissions-and-sandbox) | Allowing, asking or refusing each action; OS limits on commands | A capability must never be used, a human must approve first, or routine commands should run without prompts | Context-dependent checks → hook. Containing MCP servers or hooks → outer isolation (container, VM). Merge gate → CI |
| [MCP](#mcp) | Giving the agent tools for external systems | SaaS with per-user OAuth, stateful integrations, systems without a CLI | The model knows a CLI and a sandboxed shell exists → CLI plus skill. Teaching a workflow → skill. Event-driven step → hook |
| [Skills](#skills) | Procedures and knowledge loaded on demand | Recurring procedures, team know-how, deterministic scripts; an occasional missed activation is acceptable | Needed every session, or omission silently breaks output → instructions. Must hold every time → hook. Needs isolation → subagent |
| [Commands](#commands) | User-triggered procedures (now user-invoked skills) | Side effects or timing the model must not decide (deploy, commit, send) | The agent should apply it on its own → model-invoked skill. Must hold every time → hook |
| [Subagents](#subagents) | Delegating a task to an agent with its own context | Verbose output needed only as a summary, parallel read-only work, fresh-context review, different tools or model | Phases share a lot of context, several agents would edit the same files, or a check must always run → main session, worktrees, hook |
| [Hooks](#hooks) | Deterministic handlers at lifecycle events | A rule that must hold every time and can be checked by a script: format after edit, block a command, "done" means tests pass | A hard security limit → permissions and sandbox. Judgement → instructions or skills. Merge gate → CI |
| [Plugins](#plugins) | Distributing a versioned bundle of skills, hooks and MCP servers | A second repository or team needs the same setup, or an organization controls what runs | Only one repository needs it → repo-local files. Instructions must travel → skill or repository instructions. Settings for every user → managed configuration |
| [Automation](#automation) | Running the agent outside an interactive session, and the overall workflow | Scripts, CI events, schedules, parallel isolated tasks, embedding in an application | The diff fits in one sentence → direct prompt. A rule must hold → hook. Untrusted issue text reaching write tokens → separate read-only and write jobs |

## How the concepts fit together

- **Guidance is advisory, enforcement is mechanical.** Instructions,
  skills and subagent definitions shape what the model chooses to do,
  and the model can skip them. Permissions, the sandbox and hooks run
  whatever the model decides. CI is the last gate and depends on no
  agent setting.
- **Always loaded versus on demand.** Configuration, instructions, the
  skill catalog and MCP tool names load when a session starts. Skill
  bodies, subagents and deferred MCP tool definitions load only when
  used. Hooks run on events. Automation starts sessions from outside.
- **Plugins carry the rest.** A plugin bundles skills, hooks and MCP
  server definitions so they can be installed in many places; it adds
  no capability of its own.

## Security across the concepts

Security guidance was already researched per mechanism. The
[2026-10-05 audit and deeper research](research-notes/agent-harness-security.md)
connects those findings into a shared threat model. The practical
[security guide](guide/security.md) covers controls, sixteen proposed
benign canary checks, detection and recovery. Security applies across
the ten concepts; it is not another extension mechanism.

| Boundary | Attack to consider | What to verify |
| --- | --- | --- |
| External content → context | Prompt injection, false approval claims, poisoned memory | Preserve provenance; inspect persistent writes; a fresh session does not clear stored poison ([research](research-notes/agent-harness-security.md#5-memory-poisoning-survives-the-conversation)) |
| Repository/extension → execution | Startup commands, hidden helpers, changed packages or metadata | Review before launch and after updates; isolate every executor, including hooks and servers ([research](research-notes/agent-harness-security.md#13-startup-and-execution-controls-have-different-scope)) |
| Private data → external service | Query arguments, tool calls, URLs and publication leak data | Enforce data access, call arguments and destinations; read-only tools still send data ([OpenAI](https://developers.openai.com/api/docs/guides/deep-research)) |
| Tool request → authority | OAuth confusion, cross-client state, event-specific hook failure | Check caller/resource binding, client isolation and live failure semantics ([research](research-notes/agent-harness-security.md#10-oauth-authorizes-the-wrong-client-or-resource)) |
| Untrusted work → privileged consumer | CI artifacts/caches, generated code, logs and resource exhaustion | Validate provenance and approved SHA; consume output as untrusted data; enforce external limits ([research](research-notes/agent-harness-security.md#15-privileged-ci-consumes-hostile-code-and-artifacts)) |

The verification recommendations are **[Inference]** from the cited
evidence. Prompt reminders and schema validation support security;
authorization and isolation must enforce the actual boundary. Proposed
canaries have not yet been executed against our deployments.

## Outside gates

Every harness control above is configuration the agent's own process
enforces, and a pull request can change it. A rule that must hold when
the agent errs, is prompt-injected or has its configuration changed
belongs in a control the agent's identity cannot reach. The
[outside-gates guide](guide/outside-gates.md), researched on
2026-10-07, covers ten families and when each fits:

| Family | Real gate only if |
| --- | --- |
| Merge rules (protected branches, rulesets, code owners) | The agent is on no bypass list; the requester and last pusher cannot approve; approvals reset on new pushes |
| Required CI checks | Required on the ref, pinned to a source, workflow definition protected, no privileged trigger on agent code |
| Scanners (SAST, SCA, secrets, IaC) | Ignore files, baselines and workflows are under code owners or org configuration |
| Identity and credentials | No broader credential is reachable; the ceiling sits outside the agent's admin rights |
| Network egress and DNS | Enforced outside the agent's environment, with the resolver controlled; DNS filtering alone is not a boundary |
| Domain and DNS records | Separate accounts, registry lock, approval-gated apply |
| Isolation | No host secrets inside; the boundary is not editable from the repository |
| Policy engines | The agent cannot override the policy |
| Limits (spend, rate, time) | Hard caps, not alerts |
| Recovery and DLP | Immutable backups; DLP in-line on the channel |

All rows are **[Inference]** from the cited research. The guide also
gives intake questions that place each part of an idea in one of four
outcomes: harness mechanism only, outside gate alongside it, outside
gate instead of any harness build, or nothing.

## Instructions

**Used for:** standing guidance that every session starts with: build
and test commands, conventions that differ from defaults, gotchas,
boundaries, and how to check that work is done.

**How:** Markdown files at user, project and subdirectory scope, loaded
when the session starts and joined from the broadest scope to the most
specific. `AGENTS.md` is the file both leads read; Claude Code reads it
only while no `CLAUDE.md` exists. Keep the files short: Claude Code
advises under 200 lines per file, Codex caps the chain at 32 KiB by
default.

**When:** short, stable facts the agent cannot derive from the code and
needs in every session; a trigger for another mechanism ("use the
reviewer agent after edits"); knowledge that must always apply, such as
APIs released after the model's training.

**When not:**
- A multi-step procedure or task-specific knowledge → [skills](#skills). It costs context in every session.
- A rule that must hold every time → [hooks](#hooks) or [permissions](#permissions-and-sandbox). Instruction files are context, not enforcement.
- Something a linter or formatter can check → the tool, run by a hook or CI.
- Long reference material or architecture → files under `docs/` with a one-line pointer. Length lowers adherence to the rules that matter.
- Personal preferences → user-scope file. Notes the agent learned → memory, as recall only.

Full page: [guide/instructions.md](guide/instructions.md)

## Configuration

**Used for:** the settings that control the harness: model and effort,
permissions, MCP servers, plugins, environment and UI.

**How:** layered settings files (Claude Code `settings.json`, Codex
`config.toml`) at policy, user, project and invocation scope. A fixed
precedence resolves conflicts, a stricter safety value wins from any
layer, and project files apply only after the user trusts the folder.

**When:** the real decision is which layer owns a setting. Shared
project behavior goes in the project layer, personal defaults in the
user layer, protections that must not be weakened in the policy layer,
and one-off presets (review, CI) on the command line or in a profile.

**When not:**
- Conventions, style and workflow → [instructions](#instructions) or [skills](#skills). Settings files are not shared between harnesses.
- Secrets and API keys → a secret manager or short-lived tokens. Repository-set endpoints have leaked keys (CVE-2026-21852).
- The authoritative merge gate → CI ([automation](#automation)). Any committed agent config can be changed by a pull request.

Full page: [guide/configuration.md](guide/configuration.md)

## Permissions and sandbox

**Used for:** deciding for each tool call whether it runs, asks first or
is refused, and limiting what executed commands can read, write and
reach on the network.

**How:** allow, ask and deny rules per tool, where a deny in any scope
wins in both leads, plus an OS-level sandbox for shell commands. An
automated reviewer can reduce prompts on top of the sandbox. Bypass
modes belong only inside outer isolation such as a container or VM.

**When:** a capability must never be used (secret paths, unknown hosts);
a human must see an action first (`git push`, deploy); routine project
commands should run without prompts; an unattended run must be
contained.

**When not:**
- Checks that depend on arguments, repository state or time → a `PreToolUse` [hook](#hooks).
- Containing MCP servers, hooks or file tools → outer isolation. The per-command sandbox confines shell commands only.
- Stopping exfiltration with command patterns alone → sandbox network isolation. Alternative spellings bypass command rules in both leads.
- The merge gate → CI.

Full page: [guide/permissions-and-sandbox.md](guide/permissions-and-sandbox.md)

## MCP

**Used for:** giving the agent tools for external systems through MCP
servers, local processes or remote endpoints.

**How:** server definitions (stdio or streamable HTTP) in configuration;
tools appear as `mcp__<server>__<tool>` and go through the permission
system. Both leads defer tool definitions until needed, so context cost
rarely decides between MCP and a CLI anymore. MCP servers run outside
the command sandbox.

**When:** SaaS with per-user OAuth (issue tracker, design tool,
observability), stateful integrations such as browser automation, and
systems without a usable CLI.

**When not:**
- The model knows a CLI (`gh`, `aws`, `kubectl`) and a sandboxed shell exists → the CLI plus a [skill](#skills). The CLI stays inside the sandbox and its output can be filtered.
- A workflow chains many calls over large data → code execution against an API or SDK. Every MCP result passes through the context.
- Teaching how to use a tool → a [skill](#skills). A server provides the connection, not the workflow.
- A step that must run on an event → a [hook](#hooks). The model may not call an MCP tool.

Full page: [guide/mcp.md](guide/mcp.md)

## Skills

**Used for:** procedures and specialized knowledge the agent loads only
when needed.

**How:** a folder with `SKILL.md` (`name`, `description`) plus optional
scripts and reference files. Only the name and description stay in
context; the body loads when the user invokes the skill (`/name` in
Claude Code, `$name` in Codex) or the model matches the description.
For both leads, keep the skill in `.agents/skills/` and symlink it from
`.claude/skills/`.

**When:** a procedure or checklist you keep repeating, a section of the
instruction file that has grown into a procedure, a deterministic step
that belongs in a tested script, recurring team work such as reviews,
runbooks or scaffolding.

**When not:**
- Needed in every session, or omission silently produces wrong output → [instructions](#instructions). In Vercel's eval the skill was not invoked in 56% of cases.
- A rule that must hold every time → [hooks](#hooks).
- Work that should run isolated or in the background → [subagents](#subagents), which can use skills.
- Access to an external system → [MCP](#mcp); the skill teaches what to do with it.
- A one-step task the model handles alone → nothing.

Full page: [guide/skills.md](guide/skills.md)

## Commands

**Used for:** procedures that only the user triggers. Both leads retired
custom commands in favor of skills, so a command is now a user-invoked
skill.

**How:** a skill with model invocation turned off:
`disable-model-invocation: true` in Claude Code,
`policy.allow_implicit_invocation: false` in Codex's
`agents/openai.yaml`.

**When:** the procedure has side effects or timing the model should not
decide (deploy, commit, send a message), or a rarely used skill should
not take catalog space.

**When not:**
- The agent should apply the knowledge on its own → a model-invoked [skill](#skills).
- A rule that must hold every time → [hooks](#hooks).
- A Claude Code schedule must run it → a model-invocable skill. The flag also blocks scheduled tasks.

Full page: [guide/commands.md](guide/commands.md)

## Subagents

**Used for:** delegating a task to a separate agent instance with its
own context window, which returns one result.

**How:** a named definition (instructions, model, tool scope) that a
spawn tool runs. The subagent does not see the conversation, so the
delegation message must carry the goal, facts, scope and return format.
Codex spawns only when the user, an instruction file or a skill asks for
it; Claude Code also delegates on the definition's description.

**When:** verbose work needed only as a summary (exploration, test runs,
log triage); independent read-only questions in parallel; a review with
a fresh context; a task that needs other tools, a narrower scope or
another model.

**When not:**
- Phases share a lot of context, or need back-and-forth or low latency → the main session. Each hand-off loses detail, and one study measured 39–70% losses on sequential tasks.
- Several agents would edit the same files → one writer, or worktrees with disjoint files.
- A check that must always run → [hooks](#hooks). Delegation is a model decision.
- Subagents always cost more tokens. Anthropic measured about 15 times the tokens of a chat for its multi-agent research system.

Full page: [guide/subagents.md](guide/subagents.md)

## Hooks

**Used for:** running a handler at a fixed lifecycle point, such as
before a tool call or at the end of a turn, every time, whatever the
model decides.

**How:** event → matcher → handler. The handler (a command or an MCP
tool call) receives the event as JSON and can allow, block, rewrite the
input or add context. Denial depends on the event: `PreToolUse` accepts
exit 2; `PermissionRequest` uses nested JSON, and Claude Code ignores
exit 2 there ([hooks reference](https://code.claude.com/docs/en/hooks),
[Codex hooks](https://learn.chatgpt.com/docs/hooks)). Eleven events share their names
in both leads. Codex treats some decisions differently: a `PreToolUse`
answer of `ask` fails open.

**When:** format or lint every edit; block a known-bad command or a
protected file; make "done" mean "checks passed" with a `Stop` hook;
re-inject context at session start or after compaction; audit and
notifications.

**When not:**
- A hard limit on reading, writing or network access → [permissions and sandbox](#permissions-and-sandbox). Tool switching and unhooked paths bypass hooks.
- Asking the human before an action → an ask rule.
- Guidance that needs judgement → [instructions](#instructions) or [skills](#skills).
- The merge gate, or slow full test suites → CI. A slow `Stop` hook delays every turn.

Full page: [guide/hooks.md](guide/hooks.md)

## Plugins

**Used for:** distributing a versioned bundle of skills, hooks and MCP
server definitions to many users and repositories.

**How:** a manifest plus the components, listed in a marketplace,
installed into a versioned cache and enabled by ID. One repository can
serve both leads, because Codex also reads `.claude-plugin/marketplace.json`.
Claude Code plugins can declare dependencies on other plugins; Codex has
no counterpart.

**When:** a second repository or team needs the same setup; a role needs
a curated set; an organization must control what runs on developer
machines through a private marketplace and an allowlist.

**When not:**
- Only one repository needs it → repo-local skills, hooks and MCP config. Packaging adds release overhead and decouples the setup from the code.
- Project instructions must travel → a skill in the plugin, or instructions in the repository. Claude Code does not load a `CLAUDE.md` at the plugin root, and Codex documents no instruction component.
- A setting must apply to every user → managed [configuration](#configuration).
- OpenCode must receive the skills → its skill directories. OpenCode has no marketplace.

Full page: [guide/plugins.md](guide/plugins.md)

## Automation

**Used for:** the overall development loop with an agent, and running
the agent without a person in the session: headless runs, SDKs, CI
actions, hosted runs, schedules and parallel worktrees.

**How:** the same instructions, skills, hooks and permissions as an
interactive session, with different defaults. `codex exec` is read-only
by default; `claude -p` treats the folder as trusted and runs its hooks
unless started with `--bare`. Set every unattended run's permissions,
output format, turn and budget limits explicitly. Interactive work
follows explore, plan, implement, verify, with a check the agent can
run and a grader other than the implementer.

**When:** exploratory or design-heavy work in an interactive session
with planning; scripts and batch migrations headless; PR review and
issue-to-PR in CI; independent, cheap-to-review tasks in parallel
worktrees; repeatable unattended work on a schedule; the agent inside
your own application through an SDK.

**When not:**
- The diff fits in one sentence → a direct prompt, no plan or spec.
- A rule that must hold on every tool call → a [hook](#hooks) or [permission rule](#permissions-and-sandbox).
- Untrusted issue or PR text would reach a job with write tokens → a read-only agent job plus a separate write job. Researchers showed that text in a PR title or issue comment can make agents in GitHub Actions extract credentials.
- Significant changes in parallel → serial work. Review capacity is the limit.
- Batch work a shell loop over `-p` or `exec` can do → the CLI, not an SDK.

Full page: [guide/automation.md](guide/automation.md)

## Where to go next

- [`guide/`](guide/): one page per concept, combining the generalized
  model and the best practices in condensed form.
- [`concepts/`](concepts/) and [`best-practices/`](best-practices/):
  the full, uncondensed versions.
- [`vendors/`](vendors/): exact file names, fields and flags per harness.
