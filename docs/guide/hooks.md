# Hooks

A hook is a handler that the harness itself runs at a fixed point in the agent lifecycle, such as before a tool call or when a turn ends. Hooks enforce rules, add context and trigger side effects every time, which instructions to the model cannot guarantee. A hook receives a description of the event and can let the action proceed, block it, rewrite its input, or add context for the model.

Hooks run with the user's full permissions, outside the sandbox. Both vendors call them a guardrail, not a security boundary. Where hooks are registered and trusted is on [configuration](configuration.md); hard limits belong in [permissions-and-sandbox](permissions-and-sandbox.md).

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Mechanism | Declarative: event → matcher group → handlers ([CC][cc-hooks]) | Declarative, same three levels ([Codex][cx-hooks]) | JS/TS plugin functions ([OC][oc-hooks]) |
| User config | `~/.claude/settings.json` → `hooks` | `~/.codex/hooks.json` or `[hooks]` in `config.toml` | `~/.config/opencode/plugins/` |
| Project config | `.claude/settings.json`, `.claude/settings.local.json` | `.codex/hooks.json` or `[hooks]`; trusted projects only | `.opencode/plugins/` |
| Managed | Managed settings; cannot be removed | System, MDM, cloud, `requirements.toml`; users cannot disable | Not recorded |
| Plugin | `hooks/hooks.json` or `plugin.json` `hooks` | `hooks/hooks.json` or manifest `hooks` | The plugin is the hook |
| Events | About 30 | 12 | Hook keys plus bus events |
| Handler types | `command`, `http`, `mcp_tool`, `prompt`, `agent` | `command`, `mcp_tool`; `prompt`, `agent` parsed but skipped | JS function |
| Matcher | Exact name or `\|` list; otherwise unanchored JS regex | Regex; `*`, `""` or omitted match all | Code inspects `input.tool` |
| Block | Exit 2 (stderr is the reason) or JSON decision | Exit 2 or JSON decision | Throw in `tool.execute.before` |
| Other exit codes | Non-blocking error, including 1; missing script (127) disables the gate | Not recorded | n/a |
| Default timeout | 600 s | 600 s; `SessionEnd`/`Interrupt` 1 s, max 3 | Not recorded |
| Execution | All matching handlers in parallel | Matching command hooks concurrently | Sequential, plugin load order |
| Async | `async: true`; cannot block; killed at `-p` teardown | `async: true`; cannot block; max 8 per session | n/a |
| Trust | Waits for workspace trust interactively; `-p` and SDK treat the folder as trusted | Each non-managed hook trusted by hash via `/hooks`; changed hooks skipped until re-trusted | Not recorded |
| Off switches | `disableAllHooks`, `allowManagedHooksOnly` | `[features] hooks = false`, `allow_managed_hooks_only` | Not recorded |
| Context cap | `additionalContext` 10,000 chars per string; overflow to a file | About 2,500 tokens by default; overflow to a file | Nothing by default |

Details per cell: [Claude Code hooks][cc-hooks], [Codex hooks][cx-hooks], [OpenCode hooks][oc-hooks].

## Generalized model

**Registration.** `event → [matcher group] → [handler]`. Both leads use the same JSON shape: `{"hooks": {"<Event>": [{"matcher": "...", "hooks": [{"type": "...", ...}]}]}}`.

- **Event.** A lifecycle point with its own matcher target, input fields and accepted decisions.
- **Matcher.** A pattern over the event's target (tool name, session source, compaction trigger). Empty, `*` or omitted matches everything.
- **Handler.** Two portable types: `command` (`command`, `timeout`, `statusMessage`, `async`) and `mcp_tool` (`server`, `tool`, `input` with `${tool_input.<field>}` placeholders, `timeout`, `statusMessage`).
- **Input.** A JSON object on stdin. All events carry `session_id`, `transcript_path`, `cwd`, `hook_event_name`; tool events add `tool_name`, `tool_input`, `tool_use_id`; `Stop` adds `stop_hook_active` and `last_assistant_message`.
- **Output.** An exit code, optional plain text or JSON on stdout, and stderr.

**Scopes.** User (always loaded), project (only after trust), managed (cannot be disabled; a switch can restrict hooks to managed ones), plugin (while enabled). Hooks from all scopes add up, and all matching handlers run concurrently.

**Shared events.** Both leads use identical names.

| Event | When | Matcher target | Can block or steer |
| --- | --- | --- | --- |
| `SessionStart` | Start, resume, clear, after compaction | `startup`, `resume`, `clear`, `compact` | Plain stdout becomes context |
| `UserPromptSubmit` | Prompt submitted | None | Reject the prompt; add context |
| `PreToolUse` | Before a tool call | Tool name | Deny; rewrite input; add context |
| `PermissionRequest` | Approval prompt about to appear | Tool name | Allow or deny for the user |
| `PostToolUse` | After a tool call | Tool name | Feed back a reason; add context |
| `PreCompact` / `PostCompact` | Around compaction | `manual`, `auto` | Cancel compaction (output differs) |
| `SubagentStart` / `SubagentStop` | Subagent starts / finishes | Agent type (Codex) | `SubagentStop`: force it to continue |
| `Stop` | Main agent's turn ends | None | Force the agent to continue |
| `SessionEnd` | Session ends | Reason | — |

**Decision contract (shared subset).**

| Output | Meaning |
| --- | --- |
| Exit 0, no output | Proceed |
| Exit 0, plain stdout | Context on `SessionStart` and `UserPromptSubmit` |
| Exit 2, reason on stderr | Block: deny the call, reject the prompt, feed back the reason, or continue the agent |
| `hookSpecificOutput.permissionDecision: "deny"` + `permissionDecisionReason` | Deny a tool call (`PreToolUse`) |
| `permissionDecision: "allow"` + `updatedInput` | Rewrite the tool input |
| `{"decision": "block", "reason": "..."}` | Block on `UserPromptSubmit`, `PostToolUse`, `Stop`, `SubagentStop` |
| `{"decision": {"behavior": "allow" \| "deny"}}` | Answer a `PermissionRequest` |
| `additionalContext` | Extra context on `PreToolUse` in both leads |

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Hook config file | `settings.json` → `hooks` | `hooks.json` or `[hooks]` | Plugin module |
| `PreToolUse` | `PreToolUse` | `PreToolUse` | `tool.execute.before` |
| `PermissionRequest` | `PermissionRequest` | `PermissionRequest` | `permission.ask` |
| `PostToolUse` | `PostToolUse` | `PostToolUse` | `tool.execute.after` |
| `Stop` | `Stop` | `Stop` | `session.idle` event (approximate, observe only) |
| Block | Exit 2 / JSON | Exit 2 / JSON | Throw |
| Project trust | Workspace trust | Project trust plus per-hook hash | — |
| Managed only | `allowManagedHooksOnly` | `allow_managed_hooks_only` | — |

The full event mapping, including OpenCode approximations, is on the [vendor pages][oc-hooks].

## When to use it and when not

A hook fits a rule that must hold every time, can be checked by a script, and is tied to a lifecycle point. "Use hooks for actions that must happen every time with zero exceptions" ([CC best practices](https://code.claude.com/docs/en/best-practices)).

| Use it when | Event and handler |
| --- | --- |
| Format or lint every edited file | `PostToolUse` on `Edit\|Write` |
| Block a known-bad command or a protected file | `PreToolUse` on `Bash` or `Edit\|Write`, exit 2 |
| A check needs arguments, repository state or time of day | Synchronous `PreToolUse` |
| "Done" must mean "checks passed" | `Stop` with a `stop_hook_active` guard |
| Context must be re-injected at start or after compaction | `SessionStart` (matcher `compact`) or `UserPromptSubmit` |
| Audit, telemetry, notifications | `PostToolUse` with `async: true`, `SessionEnd`, `Stop` |
| An instruction the model already follows | Delete it, or turn it into a hook |

| Do not use it for | Use instead | Cost or risk of a hook |
| --- | --- | --- |
| A hard limit on what the agent can read, write or reach | Deny rule and sandbox, see [permissions-and-sandbox.md](permissions-and-sandbox.md) | Tool switching, unhooked tool paths and prompt injection bypass hooks |
| Prompting the human before an action | Ask rule in the harness | A Codex `PreToolUse` `ask` fails open |
| Guidance that needs judgement | [instructions.md](instructions.md) or [skills.md](skills.md) | Scripts cannot judge; `prompt` hooks are Claude Code only |
| The authoritative merge gate | CI, see [automation.md](automation.md) | Repository hooks are agent config and can be disabled or changed |
| Slow full test suites at every turn end | A fast subset in the hook, full suite in CI | A slow `Stop` gate delays every turn |

Suggested layering (inference): sandbox for limits that hold whatever the model does; deny and ask rules; `PreToolUse` hooks for context-aware vetoes; `PostToolUse` and `Stop` hooks for feedback; Git pre-commit hooks; CI as the merge gate.

## Approaches

All portable approaches use the shared events and the `command` handler.

### Gate before a tool call

**What.** `PreToolUse` that denies a call. **When.** Dangerous commands, protected files, patterns rules cannot express. **How.** Exit 2 with a stderr reason, or `permissionDecision: "deny"`; both leads honor both. Claude Code also supports `ask` and `defer`; Codex supports `allow` only to rewrite input ([CC hooks reference](https://code.claude.com/docs/en/hooks), [Codex hooks](https://learn.chatgpt.com/docs/hooks)). Trail of Bits ships only two default hooks: block `rm -rf` (suggest `trash`) and block a direct push to main. **Trade-off.** A Claude Code deny holds even in `bypassPermissions`, but a gate on one tool does not stop the same capability through another.

### Feedback after a tool call

**What.** `PostToolUse` that formats, lints or checks and feeds problems back. **How.** Matcher `Edit|Write`; run on the edited file only; surface problems with exit 2 or `decision: "block"` (stderr on exit 0 "Claude never sees"). **Trade-off.** Cannot undo side effects. Claude Code shows the reason next to the result; Codex replaces the result with it.

### Completion gate

**What.** `Stop` hook that runs a check and makes the agent continue until it passes. **When.** Unattended runs; the use case with the strongest agreement across sources (inference). **How.** Return `{"decision": "block", "reason": "..."}` on exit 0; Codex turns the reason into a continuation prompt and rejects plain text on `Stop`. Guard with `stop_hook_active`. **Trade-off.** A slow gate delays every turn end.

### Context injection

**What.** Plain stdout or `additionalContext` on `SessionStart` or `UserPromptSubmit`. **When.** Re-injecting context after compaction, per-directory prompting. **Trade-off.** Context from many hooks adds up and can degrade the model.

### Permission answering

**What.** `PermissionRequest` hook that answers an approval prompt. **When.** One specific low-risk prompt (the Claude Code example is `ExitPlanMode`). **Trade-off.** "Matching on `.*` or leaving the matcher empty would auto-approve every tool permission prompt" ([CC hooks guide](https://code.claude.com/docs/en/hooks-guide)).

### Packaging in a plugin

**What.** Hooks in a plugin's `hooks/hooks.json`, the one hook path both leads share. **How.** Codex sets `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` for plugin hooks, so one plugin serves both. Anthropic's [security-guidance plugin](https://code.claude.com/docs/en/security-guidance) is a reference built only on hooks. See [plugins.md](plugins.md). **Trade-off.** Codex does not auto-trust plugin hooks.

Claude Code also has judgement hooks (`prompt`, `agent`), which Codex skips; OpenCode needs an adapter plugin. Both are listed under [Dropped](#dropped-from-the-generalization) and [Portability](#portability).

## Practices

1. **Block with exit 2 or a deny decision, never with exit 1 or ask.**
   - Why: Claude Code treats exit 1 as a non-blocking error and proceeds. Codex marks `permissionDecision: "ask"`, `decision: "approve"`, `continue: false` and `stopReason` on `PreToolUse` as failed "and continues the tool call".
   - How: Exit 2 with a stderr reason, or `permissionDecision: "deny"` with `permissionDecisionReason`. For a human decision, use the harness's ask rules. Return `allow` only to rewrite input.
   - Evidence: [Vendor] [CC hooks reference](https://code.claude.com/docs/en/hooks#exit-code-output), [Codex hooks](https://learn.chatgpt.com/docs/hooks).

2. **Pick one signalling style per hook and keep stdout clean.**
   - Why: When stdout parses as JSON, Claude Code "ignores the exit code and the JSON alone decides". Stray output (for example from a shell profile) means stdout "no longer starts with `{`". A field at the wrong level is silently ignored.
   - How: Exit codes alone, or exit 0 plus JSON. Diagnostics go to stderr. Guard profile output with `if [[ $- == *i* ]]`.
   - Evidence: [Vendor] [CC hooks reference](https://code.claude.com/docs/en/hooks), [CC hooks guide](https://code.claude.com/docs/en/hooks-guide).

3. **Write every block reason as an instruction the model can act on.**
   - Why: Both leads feed the reason back as the next model input.
   - How: Name the rule, the violated value and the allowed alternative, for example "Use rg instead of grep" or `trash` instead of `rm -rf`.
   - Evidence: [Vendor] [CC hooks guide](https://code.claude.com/docs/en/hooks-guide); [Practitioner] [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config). No empirical comparison of phrasings exists.

4. **Guard every Stop gate against loops.**
   - Why: Claude Code overrides a `Stop` hook after eight blocks in a row without progress (`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`). Codex documents no cap.
   - How: Exit 0 at once when `stop_hook_active` is true, or count continuations in a state file keyed by `session_id`. Keep the check fast and cached. Give the model an exit ("if tests cannot pass because of X, say so"). Always print JSON on `Stop`, even `{}`.
   - Evidence: [Vendor] [CC hooks guide](https://code.claude.com/docs/en/hooks-guide), [Codex hooks](https://learn.chatgpt.com/docs/hooks).

5. **Keep synchronous hooks fast with explicit timeouts and narrow matchers.**
   - Why: Defaults are 600 s, and "a timed-out `command`, `http`, or `mcp_tool` hook doesn't block the tool call", so a hang fails open. Without a matcher a hook fires on every occurrence.
   - How: Set `timeout` explicitly and keep it short on gates (inference); no slow network calls in gate logic; filter in the matcher, then exit 0 early. Claude Code's `if` field avoids spawning the process at all.
   - Evidence: [Vendor] [CC hooks reference](https://code.claude.com/docs/en/hooks), [Codex hooks](https://learn.chatgpt.com/docs/hooks). No latency measurements exist.

6. **Use async hooks for observation only.**
   - Why: Async hooks "can't block or control" the agent in either lead.
   - How: Mark audit, telemetry and slow reviews `async: true`. Claude Code kills them at `-p` teardown; Codex runs at most eight per session and cancels unfinished ones at session end.
   - Evidence: [Vendor] [CC hooks reference](https://code.claude.com/docs/en/hooks#run-hooks-in-the-background), [Codex hooks](https://learn.chatgpt.com/docs/hooks).

7. **Keep hook context short and free of secrets.**
   - Why: "Context from multiple hooks and plugins adds up and can degrade model performance." Oversized Codex output is written to `<temp_dir>/hook_outputs/`.
   - How: Emit only what the model needs; never echo secrets to stdout, stderr or `additionalContext`.
   - Evidence: [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks), [CC hooks reference](https://code.claude.com/docs/en/hooks).

8. **Treat repository hooks as code execution.**
   - Why: Anyone with commit access can ship a hook. Claude Code `-p` and SDK runs treat the folder as trusted, so repository hooks run in folders never trusted. Codex skips new or changed hooks until trusted by hash, also in `codex exec`.
   - How: For Claude Code headless runs over foreign repositories use `--bare` or `--settings '{"disableAllHooks": true}'`. Review hook config diffs with owner review (inference). Do not pass `--dangerously-bypass-hook-trust` on untrusted input; re-trust shared hooks after each edit.
   - Evidence: [Vendor] [CC hooks reference, workspace trust](https://code.claude.com/docs/en/hooks#workspace-trust), [Codex hooks](https://learn.chatgpt.com/docs/hooks); [Advisory] GHSA-ph6w-f82w-28w6 via [Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/).

9. **Harden hook scripts against hostile input and fail closed inside the script.**
   - Why: Tool input comes from the model, which injected content can steer. The harness fails open on crashes (exit 1, 127).
   - How: Parse stdin with `jq`, Python or Node; quote every variable; never `eval` tool input; normalize paths with `realpath` against the project root; use absolute interpreter paths (`/usr/bin/python3`); in Claude Code prefer exec form (`args`); catch parse errors and exit 2 (inference).
   - Evidence: [Vendor] [CC hooks reference, security considerations](https://code.claude.com/docs/en/hooks#security-considerations), [Codex hooks](https://learn.chatgpt.com/docs/hooks).

10. **Match the capability, not a single tool.**
    - Why: After a `PreToolUse:Edit` hook blocked three edits, the agent wrote the file with Python through `Bash` ([anthropics/claude-code#29709](https://github.com/anthropics/claude-code/issues/29709), closed as not planned). Codex hosted tools such as `WebSearch` are never hooked.
    - How: Enforce security limits with a deny rule or the sandbox. If a hook is used, match every tool that grants the capability (`Edit|Write|Bash|mcp__.*`) and treat command blocklists as steering.
    - Evidence: [Practitioner] issue #29709, "Guardrails, not walls" ([trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)); [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks).

11. **Put non-negotiable hooks in managed settings.**
    - Why: Managed hooks cannot be disabled by users. In Claude Code a mod handling `tool.check` can approve a call a hook blocked "unless the hook is in managed settings".
    - How: Managed settings (Claude Code) or `requirements.toml` `[hooks]` (Codex), plus `allowManagedHooksOnly` / `allow_managed_hooks_only`. Test Codex managed MCP hooks for failure behavior first.
    - Evidence: [Vendor] [CC hooks guide](https://code.claude.com/docs/en/hooks-guide), [Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration).

12. **Keep auto-approving hooks narrow and input rewrites single.**
    - Why: An empty matcher on `PermissionRequest` approves everything. With several `updatedInput` hooks, "the last one to finish takes effect", and `updatedInput` replaces the whole input.
    - How: Match one tool in approving hooks; let one hook rewrite a tool's input and include unchanged fields.
    - Evidence: [Vendor] [CC hooks guide](https://code.claude.com/docs/en/hooks-guide), [CC hooks reference](https://code.claude.com/docs/en/hooks).

## Security

| Threat | Advisory or source | Mitigation |
| --- | --- | --- |
| Repository hooks run on every collaborator's machine | GHSA-ph6w-f82w-28w6 (Claude Code, CVSS 8.7): hooks in `.claude/settings.json` ran at startup without confirmation. Reported 2025-07-21, fixed 2025-08-26 in 1.0.87 ([Check Point](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)) | Workspace trust; code review; [practice 8](#practices) |
| Same class via MCP config and endpoints | CVE-2025-59536, CVE-2026-21852 (Claude Code); CVE-2025-61260 (Codex) | See [configuration.md](configuration.md) |
| Harness Git operations run repository Git hooks | CVE-2026-19590 (Codex Desktop, published 2026-09-01): trusted the repository's `core.hooksPath`; ran outside the sandbox without approval ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-19590)) | Keep Codex updated; treat Git hooks in untrusted repositories as untrusted code (inference) |
| Headless runs execute repository hooks | Documented Claude Code `-p`/SDK behavior | `--bare` or `disableAllHooks` via `--settings` |
| Bypass by switching tools; unhooked tool paths | Issue #29709; Codex hosted tools | Sandbox and deny rules |
| A mod or project setting overrides a hook | Claude Code mods, project `disableAllHooks` | Managed hooks, managed-only switch |
| Prompt injection works around hooks | "Hooks are not a security boundary" ([Trail of Bits](https://github.com/trailofbits/claude-code-config)) | Sandbox and deny rules |
| Shell injection via tool input; secrets in output | [CC security considerations](https://code.claude.com/docs/en/hooks#security-considerations); Codex spill files | [Practices 7 and 9](#practices) |
| Silent fail-open | Timeouts, exit 1 or 127, Codex unsupported outputs, untrusted Codex hooks skipped | Exit 2 on internal errors; canary test |

No advisory specific to the Codex hooks system was found as of 2026-10-04.

## Verification and checklist

1. **Unit tests.** Pipe recorded JSON into the script: `echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh; echo $?`. Capture real payloads per event and lead by temporarily registering `cat > /tmp/hook-$EVENT.json`. Include paths with spaces, quotes, `$()`, `..` and missing fields (inference).
2. **Registration.** `/hooks` in both leads shows the hook and its source; in Codex it also reviews and trusts hooks. Claude Code matchers are case-sensitive.
3. **Execution logs.** Claude Code `claude --debug-file /tmp/claude.log` or `/debug`. Codex has no comparable hook log.
4. **Canary.** Trigger each gate once on purpose after deploying it. This catches a mistyped path (exit 127) and Codex's skipped-until-trusted state.
5. **Bypass check.** Try the blocked action through another tool and confirm that the sandbox or a deny rule stops it.

- [ ] Each hook enforces a rule that must hold every time.
- [ ] Every gate blocks with exit 2 or `deny`; none rely on exit 1 or `ask`.
- [ ] Block reasons name the rule and the alternative.
- [ ] Every `Stop` and `SubagentStop` gate checks `stop_hook_active` and prints JSON.
- [ ] Synchronous hooks have a short explicit `timeout` and a narrow matcher; async hooks only observe.
- [ ] Scripts use a JSON parser, quote variables, use absolute paths, exit 2 on internal errors.
- [ ] Shared hooks handle Codex `apply_patch` as well as `tool_input.file_path`.
- [ ] Security limits are also enforced by deny rules or the sandbox.
- [ ] Hook config changes need owner review; headless runs over foreign repositories disable project hooks.
- [ ] Each gate showed up in `/hooks` (trusted in Codex) and was triggered once.

## Portability

**One script, two registrations.** Keep the handler as one script in the repository and register the same `hooks` object in `.claude/settings.json` and `.codex/hooks.json` (or `[[hooks.<Event>]]` in `.codex/config.toml`, but not both in one layer). Plugins share `hooks/hooks.json`.

**Safe subset.** The eleven shared events; `command` and `mcp_tool` handlers; matchers `Bash`, `Edit|Write`, `Agent`, `mcp__<server>__.*` (Codex maps `apply_patch` to `Edit`/`Write`); the shared decisions above; explicit timeouts.

**Script skeleton** (inference from both contracts):

1. Read stdin; take `hook_event_name` and `tool_name`.
2. Target file: `.tool_input.file_path // .tool_input.path`; if empty and `tool_name == "apply_patch"`, the target paths are inside the patch text in `.tool_input.command`, whose format is not specified.
3. Bash command: `.tool_input.command` in both leads.
4. Exit 0 silently, or print the reason to stderr and exit 2. On `Stop`, print JSON.
5. Resolve paths with `$(git rev-parse --show-toplevel)` or the input `cwd`, not `${CLAUDE_PROJECT_DIR}`.

Traps:

- **Codex fails open on `ask`** and other unsupported `PreToolUse` output ([Codex][cx-hooks]).
- **Exit 1 is not a block** in Claude Code; Codex behavior is not recorded.
- **`allow` differs.** Claude Code `allow` can approve but never overrides deny or ask rules; Codex `allow` only rewrites input ([CC][cc-hooks]).
- **Rewrites need per-tool shapes.** Codex needs a string `command` in `updatedInput` for Bash and `apply_patch`.
- **Cancelling compaction differs:** exit 2 or `decision: "block"` in Claude Code, `continue: false` in Codex.
- **Trust differs in headless runs:** Claude Code runs repository hooks; Codex skips untrusted ones, and editing a shared hook requires re-trust.
- **Plain stdout** becomes context only on `SessionStart` and `UserPromptSubmit` in both leads.
- **Subagent fields.** Codex adds `agent_id`/`agent_type` only on subagent events; Claude Code adds them to every hook inside a subagent.
- **`${CLAUDE_PROJECT_DIR}`** is Claude Code only and stays at the start root after entering a worktree.
- **OpenCode** has no shell-command hooks. Reuse a script through an adapter plugin that calls it via the `$` helper and throws on exit 2 (inference, [OC][oc-hooks]).

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| Events `Setup`, `UserPromptExpansion`, `StopFailure`, `PermissionDenied`, `PostToolUseFailure`, `PostToolBatch`, `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `DirectoryAdded`, `FileChanged`, model-switch, worktree, elicitation, `Notification`, `MessageDisplay` | Claude Code | No Codex counterpart |
| Events `TaskCreated`, `TaskCompleted`, `TeammateIdle` | Claude Code | Tied to agent teams |
| Event `Interrupt`; fields `additionalContextLimit`, `commandWindows` | Codex | No Claude Code counterpart |
| Handlers `http`, `prompt`, `agent`; fields `if`, `once`, `args`, `shell`, `asyncRewake`, `continueOnBlock` | Claude Code | Codex lacks `http` and skips `prompt`/`agent` |
| `permissionDecision` `ask`/`defer`; `updatedPermissions`, `interrupt`; `updatedToolOutput`; SessionStart extras | Claude Code | Codex fails open, fails closed, or lacks them |
| Hooks in skill or subagent frontmatter; SDK callback hooks; mods | Claude Code | No Codex counterpart |
| Per-hook hash trust; `notify`; `tui.notifications` | Codex | Treated as a trap; overlaps `Stop`; UI setting |
| `chat.params`, `shell.env`, `tool.definition`, `experimental.*` transforms | OpenCode | No lead counterpart |

## Open questions

- **Codex exit codes** other than 0 and 2 are undocumented; treat them as fail-open.
- **Codex `Stop` cap:** none documented.
- **Codex `apply_patch` grammar** inside `tool_input.command` and **matcher anchoring** for `Edit|Write` are not specified.
- **Codex async timeouts** and the interaction of hook decisions with approval policy are not documented.
- **Claude Code per-hook trust:** none; trust is per workspace.
- **Evidence gaps:** no data on common hook use cases or their benefit, no latency measurements, no bypass-rate comparison with rules or sandbox. A study of 2,926 repositories found hooks mostly in settings files but gives no counts ([Galster et al., arXiv:2602.14690](https://arxiv.org/abs/2602.14690)).

## Sources

- Vendor pages: [Claude Code hooks][cc-hooks], [Codex hooks][cx-hooks], [OpenCode hooks][oc-hooks]
- Research notes: [hooks best practices](../research-notes/agent-harness-best-practices/hooks.md), [Claude Code extensions](../research-notes/agent-harness-configuration/claude-code-extensions.md), [Codex extensions](../research-notes/agent-harness-configuration/codex-extensions.md)
- Claude Code: [best practices](https://code.claude.com/docs/en/best-practices), [hooks guide](https://code.claude.com/docs/en/hooks-guide), [hooks reference](https://code.claude.com/docs/en/hooks), [permissions](https://code.claude.com/docs/en/permissions), [security-guidance plugin](https://code.claude.com/docs/en/security-guidance), [bash_command_validator_example.py](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)
- Codex: [hooks](https://learn.chatgpt.com/docs/hooks), [managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration)
- OpenCode: [plugins](https://opencode.ai/docs/plugins/)
- Practitioner: [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config), [anthropics/claude-code#29709](https://github.com/anthropics/claude-code/issues/29709)
- Advisories: [Check Point on Claude Code project files](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/), [Check Point on CVE-2025-61260](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/), [NVD CVE-2026-19590](https://nvd.nist.gov/vuln/detail/CVE-2026-19590)

[cc-hooks]: ../vendors/claude-code/hooks.md
[cx-hooks]: ../vendors/codex/hooks.md
[oc-hooks]: ../vendors/opencode/hooks.md
