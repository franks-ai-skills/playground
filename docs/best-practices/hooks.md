# Hooks: best practices

How to decide when a hook is the right tool, design its decisions, keep it fast, secure it, and test it in both leads. Claude Code (CC) and Codex are equal leads; OpenCode (OC) plugin hooks appear where the research covers them. Terms follow the generalized model in [Hooks](../concepts/hooks.md): registration `event → matcher group → handler`, the eleven shared events, the shared decision contract. Where hooks are registered and trusted is on [Configuration](configuration.md); how hooks relate to permission rules and the sandbox is on [Permissions and sandbox](permissions-and-sandbox.md).

Research date: 2026-10-04. Items marked "(2025)" are older. Evidence labels: **[Vendor]** vendor documentation or vendor-published guidance, **[Empirical]** measured data, **[Advisory]** CVE, GHSA or security research disclosure, **[Practitioner]** practitioner opinion or issue report. "Inference" marks a conclusion the research draws without a direct source.

## Summary

1. [Use a hook only for rules that must hold every time](#1-use-a-hook-only-for-rules-that-must-hold-every-time); judgement goes to instructions, hard limits to rules, sandbox and CI.
2. [Block with exit 2 or a deny decision, never with exit 1 or ask](#2-block-with-exit-2-or-a-deny-decision-never-with-exit-1-or-ask); Codex fails open on `ask`.
3. [Write every block reason as an instruction the model can act on](#4-write-every-block-reason-as-an-instruction-the-model-can-act-on).
4. [Guard every Stop gate against loops](#5-guard-every-stop-gate-against-loops) with `stop_hook_active`; Codex documents no cap.
5. [Keep synchronous hooks fast with explicit timeouts and narrow matchers](#6-keep-synchronous-hooks-fast-with-explicit-timeouts-and-narrow-matchers); a timed-out hook is not a gate.
6. [Treat repository hooks as code execution](#9-treat-repository-hooks-as-code-execution); CC `-p` runs them in untrusted folders.
7. [Harden hook scripts against hostile input](#10-harden-hook-scripts-against-hostile-input) and fail closed inside the script.
8. [Test hooks in isolation and prove each gate live](#15-test-hooks-in-isolation-and-prove-each-gate-live); a mistyped path silently disables a gate.

## When to use it

Related best-practice pages: [configuration](configuration.md), [permissions and sandbox](permissions-and-sandbox.md), [instructions](instructions.md), [skills](skills.md), [subagents](subagents.md), [MCP](mcp.md), [plugins](plugins.md), [automation](automation.md).

A hook runs deterministically at a lifecycle point, with the user's full privileges, outside the sandbox. Both vendors and Trail of Bits call hooks guardrails, not a security boundary.

| Need | Right tool | Source |
| --- | --- | --- |
| An action that must happen every time, checkable by a script, tied to a lifecycle point (format after edit, block a known-bad command, tests before "done") | Hook | "Use hooks for actions that must happen every time with zero exceptions" ([CC best practices](https://code.claude.com/docs/en/best-practices)) |
| Guidance that needs judgement | [Instructions](../concepts/instructions.md) or [skills](../concepts/skills.md); a `prompt` hook in CC only | [CC hooks guide](https://code.claude.com/docs/en/hooks-guide) |
| An instruction the model already follows without being told | Delete it, or convert it to a hook | "If Claude already does something correctly without the instruction, delete it or convert it to a hook" ([CC best practices](https://code.claude.com/docs/en/best-practices)) |
| A hard limit on what the agent can read, write or reach | Deny rule and sandbox, see [Permissions and sandbox](permissions-and-sandbox.md) | Hooks are bypassable by tool switching, specialized tool paths, hosted tools and prompt injection |
| Prompt the human before an action | Ask rule in the harness, not a hook | A Codex `PreToolUse` `ask` fails open ([Codex hooks](https://learn.chatgpt.com/docs/hooks)) |
| Inspect arguments, repository state or time of day before a call | Synchronous `PreToolUse` hook | Rules cannot express it (inference) |
| Merge gate independent of agent config | CI, see [Automation](../concepts/automation.md) | "For hard enforcement, pair the plugin with a hook that blocks the edit or a CI check" ([CC security-guidance](https://code.claude.com/docs/en/security-guidance)) |

Layering suggested by the research (inference from the cited sources): (1) sandbox or dev container for limits that hold whatever the model does; (2) permission deny and ask rules; (3) synchronous `PreToolUse` hooks for context-aware vetoes, treated as steering; (4) `PostToolUse` and `Stop` hooks for fast feedback loops; (5) Git hooks or pre-commit as a harness-independent local gate; (6) CI as the authoritative merge gate.

Trail of Bits' placement rule: "anything that must hold unconditionally belongs in CLAUDE.md, and anything that must hold regardless of what Claude decides belongs in a hook" ([trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)).

## Approaches

All portable approaches use the shared events and the `command` handler. Register the same `{"hooks": {...}}` object in `.claude/settings.json` (CC) and `.codex/hooks.json` or `[hooks]` in `.codex/config.toml` (Codex); see [practice 14](#14-write-one-script-and-register-it-in-both-leads).

### Gate before a tool call

**What it is.** `PreToolUse` on a tool matcher that denies a call.

**When it fits.** Dangerous commands (`Bash`), protected files (`Edit|Write`), patterns rules cannot express.

**How.** Exit 2 with the reason on stderr, or exit 0 with `hookSpecificOutput.permissionDecision: "deny"` and `permissionDecisionReason`. Both leads honor both forms. CC also supports `allow`, `ask` and `defer`, with precedence `deny > defer > ask > allow` across hooks; `defer` is honored only with `-p`. Codex supports `deny`, the legacy `{"decision":"block","reason"}`, exit 2, `additionalContext`, and `allow` with `updatedInput` (rewrite only); plain stdout is ignored ([CC hooks reference](https://code.claude.com/docs/en/hooks), [Codex hooks](https://learn.chatgpt.com/docs/hooks)). CC example: a script that blocks edits to `.env`, `package-lock.json` and `.git/` with exit 2 ([CC hooks guide](https://code.claude.com/docs/en/hooks-guide)). Reference implementation: [bash_command_validator_example.py](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py). Trail of Bits recommends only two default hooks: `PreToolUse` on `Bash` blocking `rm -rf` (suggesting `trash`) and blocking a direct push to main or master ([trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)).

**Trade-offs.** A CC `PreToolUse` deny holds even in `bypassPermissions` mode; hooks cannot loosen deny or ask rules ([CC permissions](https://code.claude.com/docs/en/permissions#extend-permissions-with-hooks)). A gate keyed on one tool does not stop the same capability through another tool ([practice 11](#11-match-the-capability-not-a-single-tool)). CC documents a combined pattern: allow `"Bash"` and register a `PreToolUse` hook that rejects specific commands ([CC permissions](https://code.claude.com/docs/en/permissions#extend-permissions-with-hooks)); this trades prompts for a bypassable blocklist.

### Feedback after a tool call

**What it is.** `PostToolUse` that formats, lints or checks what a tool just did and feeds problems back.

**When it fits.** Formatting and linting after edits; commit or push checks after `Bash`.

**How.** Matcher `Edit|Write`; run the formatter on the edited file only. To surface a warning to the model, exit 2 or return `decision: "block"` with a reason; stderr from an exit-0 hook "Claude never sees". CC only: an `if` filter such as `Bash(git *)` matches subcommands (`npm test && git push`) and commands inside `$()` and backticks, and a `FileChanged` hook catches files rewritten by `Bash` ([CC hooks reference](https://code.claude.com/docs/en/hooks), [CC hooks guide](https://code.claude.com/docs/en/hooks-guide)). Portable commit checks filter inside the script, because `if` is CC only.

**Trade-offs.** `PostToolUse` cannot undo side effects in either lead. CC shows the reason to the model alongside the result; Codex "replaces the tool result with that feedback" ([Codex hooks](https://learn.chatgpt.com/docs/hooks)).

### Completion gate

**What it is.** A `Stop` hook that runs a check and forces the agent to continue until it passes.

**When it fits.** Making "done" mean "checks passed", especially in unattended runs. CC: "The /goal and Stop hook versions are what let an unattended run finish correctly without you" ([CC best practices](https://code.claude.com/docs/en/best-practices)). This is the use case with the strongest agreement across the vendor, Trail of Bits and Anthropic's own plugin (inference).

**How.** Return `{"decision": "block", "reason": "..."}` on exit 0. In Codex the block "tells Codex to continue and automatically creates a new continuation prompt", using the reason as prompt text; `Stop` requires JSON ("Plain text output is invalid for this event"); `continue: false` from any matching `Stop` hook wins over continuation. Guard with `stop_hook_active` ([practice 5](#5-guard-every-stop-gate-against-loops)). CC `Stop` hooks fire whenever Claude finishes responding, not only at task completion, and not on user interrupts ([CC hooks guide](https://code.claude.com/docs/en/hooks-guide), [Codex hooks](https://learn.chatgpt.com/docs/hooks)).

**Trade-offs.** A slow gate delays every turn end. Run a fast subset; full suites belong in CI (inference).

### Context injection

**What it is.** Adding text to the model's context at a lifecycle point.

**When it fits.** Re-injecting context after compaction, per-directory prompting, session bootstrap.

**How.** `SessionStart` (matcher `startup|resume|clear|compact`) or `UserPromptSubmit` with plain stdout, which becomes context in both leads; or `additionalContext` in JSON. CC example: `SessionStart` with matcher `compact` to re-inject context after compaction ([CC hooks guide](https://code.claude.com/docs/en/hooks-guide)). Codex use cases include "Customize prompting when in a certain directory" and "Summarize chats to create persistent memories automatically" ([Codex hooks](https://learn.chatgpt.com/docs/hooks)).

**Trade-offs.** Context costs model performance ([practice 8](#8-keep-hook-context-short-and-free-of-secrets)).

### Permission answering

**What it is.** A `PermissionRequest` hook that answers an approval prompt on the user's behalf.

**When it fits.** Auto-approving one specific, low-risk prompt (the CC guide's example is `ExitPlanMode`).

**How.** Return `{"decision": {"behavior": "allow" | "deny", "message": "..."}}`. Codex: "any `deny` wins. Otherwise, an `allow` lets the request proceed without surfacing the approval prompt"; `updatedInput`, `updatedPermissions` and `interrupt` "fail closed today" ([Codex hooks](https://learn.chatgpt.com/docs/hooks)).

**Trade-offs.** "Matching on `.*` or leaving the matcher empty would auto-approve every tool permission prompt, including file writes and shell commands" ([CC hooks guide](https://code.claude.com/docs/en/hooks-guide)).

### Judgement hooks (Claude Code only)

**What it is.** `type: "prompt"` (a single-turn model returns `{"ok": bool, "reason"}`) or `type: "agent"` (multi-turn with tools; "experimental and may change").

**When it fits.** Checks that need judgement rather than a script, for example Trail of Bits' anti-rationalization `Stop` hook, which rejects final answers that call issues "pre-existing" or "out of scope", defer to unrequested follow-ups, or skip test or lint failures ([trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)). The CC docs' example is an agent `Stop` hook that verifies unit tests pass ([CC hooks guide](https://code.claude.com/docs/en/hooks-guide)).

**How.** Force the prompt hook's output to raw JSON: "Without this, Haiku wraps the JSON in markdown code fences or adds explanatory text, which fails JSON parsing and silently breaks the hook" ([trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)). A prompt hook on `Stop` can return `"impossible": true` so a condition that can never be met does not loop.

**Trade-offs.** Not portable: Codex parses `prompt` and `agent` handlers but skips them ([Hooks concept](../concepts/hooks.md)).

### Observation and audit

**What it is.** Hooks that log, notify or run slow reviews without blocking.

**When it fits.** Audit logs, telemetry, notifications, background reviews. Codex lists "Send the chat to a custom logging/analytics engine" and "Scan your team's prompts to block accidentally pasting API keys" ([Codex hooks](https://learn.chatgpt.com/docs/hooks)).

**How.** `PostToolUse` with `async: true`, and `SessionEnd`. Notifications on turn end: `Stop` in both leads (`Notification` is CC only). CC only: `ConfigChange` to audit or block in-session settings changes ([CC security](https://code.claude.com/docs/en/security)). Anthropic's `security-guidance` plugin keeps only its per-edit pattern match synchronous and runs the `Stop` diff review and the commit/push review in the background ([CC security-guidance](https://code.claude.com/docs/en/security-guidance)).

**Trade-offs.** Async hooks cannot block in either lead ([practice 7](#7-use-async-hooks-for-observation-only)).

### Packaging in a plugin

**What it is.** Shipping hooks in a plugin's `hooks/hooks.json`, the one hook path both leads share.

**How.** Codex sets `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` for plugin hooks in addition to `PLUGIN_ROOT` and `PLUGIN_DATA`, so one plugin can serve both leads ([Codex hooks](https://learn.chatgpt.com/docs/hooks)). Anthropic's `security-guidance` plugin is a production reference built only on hooks: `SessionStart` bootstraps a Python environment, `UserPromptSubmit` captures a working-tree baseline, `PostToolUse` on `Edit`/`Write`/`NotebookEdit` pattern-matches each edit, `Stop` reviews the diff in the background, and `PostToolUse` on `Bash` filtered to `git commit`/`git push` reviews in the background ([CC security-guidance](https://code.claude.com/docs/en/security-guidance)). The hookify plugin generates hooks from plain English, for example `/hookify Warn me when I use rm -rf commands` ([hookify](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/hookify)). See [Plugins](../concepts/plugins.md).

**Trade-offs.** Codex does not auto-trust plugin-bundled hooks ([Codex hooks](https://learn.chatgpt.com/docs/hooks)). Plugin `${user_config.*}` values are substituted only in CC exec form.

### OpenCode plugin hooks

OpenCode has no shell-command hooks. A plugin function throws in `tool.execute.before` to block. Its documented `.env` example blocks only `input.tool === "read"` where `filePath.includes(".env")`, so shell reads are not covered; another example escapes the bash command with `shescape` ([OpenCode plugins](https://opencode.ai/docs/plugins/)). Reusing a shared script needs an adapter plugin that builds the JSON input, calls the script through the `$` helper and maps exit 2 to a thrown error (inference, [Hooks concept](../concepts/hooks.md)).

## Practices

### 1. Use a hook only for rules that must hold every time

- **Why:** "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." Trail of Bits: "An instruction in your CLAUDE.md saying 'never use rm -rf' can be forgotten or overridden by context pressure. A PreToolUse hook that blocks rm -rf fires every single time." Trail of Bits treats everything beyond its two default hooks ("Audit logging", "Bash command log", "Enforce package manager", "Anti-rationalization gate") as "patterns to adapt, not drop-in configs".
- **How:** Hook if the rule must hold deterministically, can be checked by a script and is tied to a lifecycle point. Otherwise use instructions or skills. For hard security limits use deny rules, the sandbox or CI. Portable use cases on shared events: format or lint (`PostToolUse` + `Edit|Write`); dangerous commands (`PreToolUse` + `Bash`, exit 2); protected files (`PreToolUse` + `Edit|Write`, exit 2); context (`SessionStart` or `UserPromptSubmit`); quality gate (`Stop` with a `stop_hook_active` guard); notifications (`Stop`); audit (`PostToolUse` async, `SessionEnd`).
- **Evidence:** [Vendor] [CC best practices](https://code.claude.com/docs/en/best-practices); [Vendor] [CC hooks guide](https://code.claude.com/docs/en/hooks-guide); [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks); [Practitioner] [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config); [Empirical] a study of 2,926 GitHub repositories found hooks are "usually defined in Settings files" and correlate with them (ρ=0.52), with advanced mechanisms adopted only shallowly, but gives no hook counts or purposes ([Galster et al., arXiv:2602.14690, Feb 2026](https://arxiv.org/abs/2602.14690)).

### 2. Block with exit 2 or a deny decision, never with exit 1 or ask

- **Why:** CC: "Without valid JSON on stdout, Claude Code treats exit code 1 as a non-blocking error and proceeds with the action... If your hook is meant to enforce a policy, use `exit 2`." Codex behavior for other exit codes is not documented. In Codex, `PreToolUse` `permissionDecision: "ask"`, legacy `decision: "approve"`, `continue: false`, `stopReason` and `suppressOutput` "are parsed but not supported yet. Codex marks the hook run as failed, reports the error, and continues the tool call."
- **How:** Use exit 2 with a stderr reason, or `permissionDecision: "deny"` with `permissionDecisionReason`. To get a human decision, let the harness's own ask rules prompt, or deny with a reason telling the model to ask the user. Return `allow` only to rewrite input (`updatedInput`), not to approve: in Codex `allow` is documented only for rewriting.
- **Evidence:** [Vendor] [CC hooks reference](https://code.claude.com/docs/en/hooks#exit-code-output); [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks).

### 3. Pick one signalling style per hook and keep stdout clean

- **Why:** "Choose one approach per hook: either use exit codes alone for signaling, or exit 0 and print JSON for structured control." When stdout parses as a valid object, CC "ignores the exit code and the JSON alone decides the outcome"; exit 2 with schema-invalid JSON still blocks (since v2.1.214). Extra stdout before the JSON (for example an unconditional `echo` in a shell profile sourced through `BASH_ENV` or Git Bash) means stdout "no longer starts with `{`" and is treated as plain text. A field at the wrong level, such as `permissionDecision` outside `hookSpecificOutput`, is silently ignored.
- **How:** Simple gate: exit codes only. Structured control: exit 0 plus JSON. Write diagnostics to stderr, which "keeps stdout clean for JSON output and sends the message to the debug log". Guard profile output with `if [[ $- == *i* ]]; then echo ...; fi`. Check the CC debug log for "Hook JSON output had unrecognized keys".
- **Evidence:** [Vendor] [CC hooks reference](https://code.claude.com/docs/en/hooks); [Vendor] [CC hooks guide](https://code.claude.com/docs/en/hooks-guide).

### 4. Write every block reason as an instruction the model can act on

- **Why:** Both leads feed the reason back as the next model input. In CC's protected-files example, "Claude receives feedback explaining why the edit was blocked, so it can adjust its approach". The CC `permissionDecisionReason` for `deny` goes to Claude, for `ask` to the user, and for `allow`/`defer` only to the debug log.
- **How:** State the rule, the violated value and the allowed alternative in one or two sentences, for example: "Blocked: `.env` is protected. Read `.env.example` instead or ask the user to set the value." (inference). The CC docs use "Use rg instead of grep for better performance"; Trail of Bits suggests `trash` instead of `rm -rf` and feature branches instead of pushing to main.
- **Evidence:** [Vendor] [CC hooks guide](https://code.claude.com/docs/en/hooks-guide); [Vendor] [CC hooks reference](https://code.claude.com/docs/en/hooks); [Practitioner] [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config). No empirical comparison of reason phrasings was found.

### 5. Guard every Stop gate against loops

- **Why:** CC "overrides a Stop hook after it blocks eight times in a row without progress" (raise with `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`) and tells authors to check `stop_hook_active`. Codex documents no cap and passes `stop_hook_active` ("Whether this turn was already continued by `Stop`").
- **How:** (1) Exit 0 at once when `stop_hook_active` is true, or allow at most N continuations by counting in a state file keyed by `session_id` and `turn_id`. (2) Make the gate cheap and idempotent: a fast test subset, cached by tree hash. (3) Give the model an exit, for example a reason that says "if tests cannot pass because of X, say so explicitly"; this is the command-hook analogue of CC's prompt-hook `"impossible": true` (inference). (4) Always print JSON on exit 0 for `Stop`, even `{}`, because Codex rejects plain text. The guard is mandatory in Codex.
- **Evidence:** [Vendor] [CC hooks guide](https://code.claude.com/docs/en/hooks-guide); [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks).

### 6. Keep synchronous hooks fast with explicit timeouts and narrow matchers

- **Why:** Synchronous hooks sit on the critical path. Defaults are long: CC 600 s for `command`, `http` and `mcp_tool` (30 s on `UserPromptSubmit`; `prompt` 30 s; `agent` 60 s; `SessionEnd` hooks share 1.5 s, raisable to 60 s); Codex 600 s (`SessionEnd`/`Interrupt` 1 s, max 3 s). "A timed-out `command`, `http`, or `mcp_tool` hook doesn't block the tool call", so a hang degrades to fail-open. Codex MCP hook "Errors, missing servers, and unavailable tools don't block the operation." (A CC Agent SDK callback hook on `PreToolUse` that times out does block.) "Without a matcher, a hook fires on every occurrence of its event."
- **How:** Set `timeout` explicitly and keep it short for `PreToolUse` and `PermissionRequest` gates, with gate logic that does not depend on slow network calls (inference). Filter in the matcher, not inside the script, so the hook process is not spawned for calls it ignores (inference). CC: use the `if` field, which filters "by tool name and arguments together, so the hook process only spawns when the tool call matches". Portable: narrow matcher plus early `exit 0`. Formatters touch only the edited file. All matching handlers run concurrently in both leads; "one hook can't prevent another matching hook from starting" (Codex).
- **Evidence:** [Vendor] [CC hooks guide](https://code.claude.com/docs/en/hooks-guide); [Vendor] [CC hooks reference](https://code.claude.com/docs/en/hooks); [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks). No published latency measurements exist for either lead.

### 7. Use async hooks for observation only

- **Why:** CC async hooks "can't block or control Claude's behavior"; Codex background hooks "can't block, approve, rewrite, or otherwise control the operation... Use synchronous hooks for tool policies, permission decisions, prompt rejection, or turn continuation."
- **How:** Mark audit, telemetry and slow reviews `async: true`. Expect: CC delivers async output on the next turn, does not enforce `timeout` once running (it does for `asyncRewake`), kills running async hooks at `-p` teardown ("start a fully detached process" if the work must outlive it), and does not deduplicate repeated firings; `asyncRewake: true` wakes Claude on exit 2 even when idle. Codex runs at most eight background hooks per session ("Additional hooks wait"), may finish them out of order, cancels unfinished ones at session end, and always runs `SessionEnd` synchronously.
- **Evidence:** [Vendor] [CC hooks reference](https://code.claude.com/docs/en/hooks#run-hooks-in-the-background); [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks).

### 8. Keep hook context short and free of secrets

- **Why:** Codex: "Context from multiple hooks and plugins adds up and can degrade model performance." Its default is about 2,500 tokens per message before spilling to disk; it warns against `additionalContextLimit: 0` unless the hook caps its own output. CC caps `additionalContext` at 10,000 characters per string and saves the overflow to a file. Codex: "Because oversized output can be written to disk, avoid returning secrets or other sensitive data in hook output"; spill files go to `<temp_dir>/hook_outputs/<session_id>/<uuid>.txt`.
- **How:** Emit only what the model needs. Never echo secrets to stdout, stderr or `additionalContext`; they reach the model, logs and Codex spill files.
- **Evidence:** [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks); [Vendor] [CC hooks reference](https://code.claude.com/docs/en/hooks).

### 9. Treat repository hooks as code execution

- **Why:** "Command hooks execute shell commands with your full user permissions." Anyone with commit or PR access can ship a hook. In interactive CC sessions, hooks from every settings file wait for workspace trust, but in `-p` or SDK sessions "Claude Code never shows the dialog and treats the folder as trusted, so hooks committed in a repository's `.claude/settings.json` run in a folder you've never trusted". Hooks also run when only a parent folder was trusted. Codex requires trust of "the exact hook definition" by hash; new or changed hooks are skipped until reviewed, also in `codex exec`, and plugin hooks are not auto-trusted. `--dangerously-bypass-hook-trust` is meant "For one-off automation that already vets hook sources outside Codex".
- **How:**
  - For CC headless runs over repositories you did not write: review `.claude/` settings, start with `--bare`, or pass `--settings '{"disableAllHooks": true}'`.
  - Review `.claude/`, `.codex/`, `.opencode/` and `hooks/hooks.json` diffs in code review, with owner review on these paths (inference).
  - In Codex, do not use `--dangerously-bypass-hook-trust` on untrusted input; re-trust shared hooks after each edit via `/hooks`.
  - A tracked `.claude/settings.local.json` or a symlinked `.claude` counts as repository-supplied in CC.
- **Evidence:** [Vendor] [CC hooks reference, workspace trust](https://code.claude.com/docs/en/hooks#workspace-trust); [Vendor] [CC permissions, "What runs before you trust a folder"](https://code.claude.com/docs/en/permissions#what-runs-before-you-trust-a-folder); [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks); [Advisory] (2025) GHSA-ph6w-f82w-28w6 via [Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/).

### 10. Harden hook scripts against hostile input

- **Why:** Tool input comes from the model, which can be steered by injected content. CC lists: "Validate and sanitize inputs"; "Always quote shell variables"; "Block path traversal: check for `..` in file paths"; "Use absolute paths"; "Skip sensitive files: avoid `.env`, `.git/`, keys, etc." The harness fails open on crashes (exit 1, or 127 for a missing script).
- **How:**
  - Parse stdin with `jq`, Python or Node, never with `grep` on raw JSON.
  - Quote every variable. Never `eval` or interpolate `tool_input` into a shell string. `jq -r ... | xargs cmd` breaks on paths with spaces or newlines; use `jq --raw-output0` or a script (inference).
  - Normalize paths with `realpath` and check them against the project root, not only for `..` (inference).
  - Use absolute interpreter paths, as the Codex examples do (`/usr/bin/python3`), so a repository cannot shadow `python3` on `PATH`.
  - CC: prefer exec form (`args` present), which spawns the executable with no shell; "Special characters such as apostrophes, `$`, and backticks pass through verbatim". "Prefer exec form for any hook that references a path placeholder." Plugin `${user_config.*}` values are substituted only in exec form (since v2.1.207).
  - In gate hooks, catch parse errors and exit 2 (fail closed inside the script) (inference).
- **Evidence:** [Vendor] [CC hooks reference, security considerations](https://code.claude.com/docs/en/hooks#security-considerations); [Vendor] [CC hooks reference, exec form](https://code.claude.com/docs/en/hooks#exec-form-and-shell-form); [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks).

### 11. Match the capability, not a single tool

- **Why:** In anthropics/claude-code#29709 (2026-03-01, closed as not planned), after a `PreToolUse:Edit` hook blocked edits three times, the agent wrote the file with Python through `Bash`: "Any PreToolUse:Edit|Write hook can be trivially bypassed this way." Codex: "Some specialized tool paths can opt out of the default hook path", and hosted tools such as `WebSearch` are never hooked.
- **How:** For anything that matters for security, enforce at the capability level with a deny rule or the sandbox. If a hook is used, match every tool that grants the capability (`Edit|Write|Bash|mcp__.*`) and accept that Bash parsing is best-effort; CC's `if` filter is best-effort too. Use command-string blocklists for steering against mistakes only; aliases, `python -c`, base64 and written-then-run scripts get around them (inference).
- **Evidence:** [Practitioner] [anthropics/claude-code#29709](https://github.com/anthropics/claude-code/issues/29709); [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks); [Practitioner] "Guardrails, not walls" ([trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)).

### 12. Put non-negotiable hooks in managed settings

- **Why:** Managed hooks cannot be disabled by users in either lead. In CC, an installed mod handling `tool.check` "can approve a call that your PreToolUse hook blocked, unless the hook is in managed settings". Without managed-only enforcement, a project `disableAllHooks` setting can change the outcome (inference).
- **How:** Deliver the hook through managed settings (CC) or `requirements.toml` `[hooks]` (Codex). Set `allowManagedHooksOnly` (CC) or `allow_managed_hooks_only` (Codex) where only managed hooks should run. Codex admins can also force hooks off with `[features].hooks = false`. For Codex managed MCP hooks: "Before relying on these hooks, test callback connectivity, required events, and failure behavior"; a `PreToolUse` callback error, timeout or malformed response "can fail the hook without blocking the tool".
- **Evidence:** [Vendor] [CC hooks guide](https://code.claude.com/docs/en/hooks-guide); [Vendor] [CC permissions](https://code.claude.com/docs/en/permissions#extend-permissions-with-hooks); [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks); [Vendor] [Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration).

### 13. Keep auto-approving hooks narrow and input rewrites single

- **Why:** An empty or `.*` matcher on a `PermissionRequest` hook auto-approves every prompt. When several CC `PreToolUse` hooks return `updatedInput`, "the last one to finish takes effect. Since hooks run in parallel, the order is non-deterministic." `updatedInput` "Replaces the entire input object".
- **How:** Match one tool name in auto-approving hooks. Let at most one hook rewrite a given tool's input, and include unchanged fields. In Codex, `updatedInput` for Bash and `apply_patch` needs a string `command`.
- **Evidence:** [Vendor] [CC hooks guide](https://code.claude.com/docs/en/hooks-guide); [Vendor] [CC hooks reference](https://code.claude.com/docs/en/hooks); [Vendor] via the [Hooks concept](../concepts/hooks.md).

### 14. Write one script and register it in both leads

- **Why:** Both leads share the `hooks` JSON shape and eleven event names, but differ in tool input and paths. Codex `apply_patch` puts the patch in `tool_input.command`, so a hook keyed on `tool_input.file_path` sees nothing in Codex. CC `${CLAUDE_PROJECT_DIR}` stays at the session's start root after entering a worktree, while `cwd` follows Claude.
- **How:** Keep the script in the repository and register it in `.claude/settings.json` and `.codex/hooks.json`. Resolve its path from the git root, as Codex recommends: `/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py"`. Matchers: `Bash`, `Edit|Write`, `mcp__<server>__.*`; Codex maps `apply_patch` to `Edit`/`Write` and unified exec to `Bash`. Portable script skeleton (inference from both contracts):
  1. `input=$(cat)`; read `hook_event_name` and `tool_name`.
  2. Target file: `jq -r '.tool_input.file_path // .tool_input.path // empty'`; if empty and `tool_name == "apply_patch"`, the target paths are inside the patch text in `.tool_input.command`, whose format the hooks page does not specify.
  3. Bash: `.tool_input.command` (same field in both leads).
  4. Decide; exit 0 silently, or print the reason to stderr and exit 2.
  5. On `Stop`, always print JSON on exit 0.
  6. Resolve repository paths from the input `cwd` or `git rev-parse --show-toplevel`, not `${CLAUDE_PROJECT_DIR}`.

  Do not register hooks in both `.codex/hooks.json` and `[hooks]` in one layer; Codex merges them with a warning. Do not depend on Codex `transcript_path`, which "isn't a stable interface".
- **Evidence:** [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks); [Vendor] [CC hooks reference](https://code.claude.com/docs/en/hooks#reference-scripts-by-path); [Vendor] via the [Hooks concept](../concepts/hooks.md#portability).

### 15. Test hooks in isolation and prove each gate live

- **Why:** On success "you see nothing". "When the script path doesn't exist or isn't executable, the shell exits with a code like 127... For most hook events, the action proceeds... a mistyped path in `settings.json` leaves the gate silently disabled." In Codex an untrusted or changed hook is skipped, not errored.
- **How:** See [Verification](#verification). Pipe recorded JSON into the script, assert on exit code and output, then confirm in the harness with `/hooks`, and trigger each gate once on purpose after deploying it.
- **Evidence:** [Vendor] [CC hooks guide](https://code.claude.com/docs/en/hooks-guide); [Vendor] [CC hooks reference](https://code.claude.com/docs/en/hooks#exit-code-output); [Vendor] [Codex hooks](https://learn.chatgpt.com/docs/hooks). No dedicated hook test framework from a credible maintainer was found.

## Anti-patterns

| Avoid | Do instead |
| --- | --- |
| `exit 1` to block | `exit 2`, or `permissionDecision: "deny"` |
| `permissionDecision: "ask"` in a portable `PreToolUse` hook | An ask rule in the harness; or deny with "ask the user" in the reason |
| A hook as the only control for a security limit | Deny rule and sandbox; the hook is steering |
| A `PreToolUse` gate on `Edit` and `Write` only | Also cover `Bash` and MCP tools, or enforce with the sandbox |
| Unguarded `Stop` gate | `stop_hook_active` check or a continuation counter |
| Plain text on `Stop` | JSON, even `{}`, on exit 0 |
| Default 600 s timeout on a gate | Explicit short `timeout`; no slow network calls in gate logic |
| Async hook used for enforcement | Synchronous hook |
| Empty or `.*` matcher on an auto-approving `PermissionRequest` hook | One exact tool name |
| Several hooks rewriting the same tool's input | One rewriting hook |
| Relative script paths such as `.codex/hooks/...` | Path from `git rev-parse --show-toplevel`, absolute interpreter |
| `grep` on raw JSON, unquoted variables, `eval`, `xargs` on paths | JSON parser, quoting, exec form, NUL-separated output |
| Unconditional `echo` in shell profiles sourced by hooks | Guard with `if [[ $- == *i* ]]` |
| Reading only `tool_input.file_path` in a shared hook | Also handle Codex `apply_patch` in `tool_input.command` |
| Prompt hook output without forcing raw JSON | Instruct raw JSON only (CC prompt hooks) |
| `claude -p` over cloned repositories with project hooks enabled | `--bare` or `--settings '{"disableAllHooks": true}'` |
| `--dangerously-bypass-hook-trust` on unvetted repositories | Review and trust hooks via `/hooks` |
| Secrets in hook stdout, stderr or `additionalContext` | Log decisions without secret values |

## Security

| Threat | Advisory or source | Mitigation |
| --- | --- | --- |
| Repository hooks run on every collaborator's machine at startup | (2025) CC GHSA-ph6w-f82w-28w6, CVSS 8.7: hooks in a repository's `.claude/settings.json` executed at startup without confirmation; "any contributor with commit access can define hooks that will execute shell commands on every collaborator's machine". Reported 2025-07-21, fixed 2025-08-26 (1.0.87); Anthropic added an enhanced warning dialog for untrusted project configurations ([Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)) | Workspace trust; review config in code review; [practice 9](#9-treat-repository-hooks-as-code-execution) |
| Same class through MCP config and endpoints | (2025) CVE-2025-59536 (MCP servers started before trust) and CVE-2026-21852 (API key exfiltration via project config, published 2026-01-21), same research ([Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)); (2025) Codex CVE-2025-61260: repository `.env` `CODEX_HOME=./.codex` plus `.codex/config.toml` MCP entries made Codex "invoke the declared command/args immediately at startup" ([Check Point Research](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/)) | See [Configuration security](configuration.md#security) |
| Harness-driven Git operations run repository Git hooks | CVE-2026-19590 (published 2026-09-01): Codex Desktop "could execute attacker-controlled Git hooks because automated Git operations trusted the repository's local core.hooksPath setting... The hook executes outside Codex's command sandbox, without user approval" ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-19590)). These are Git hooks, not agent hooks, but an agent or hook that runs `git commit` triggers them | Keep Codex updated; treat Git hooks in untrusted repositories as untrusted code (inference) |
| Headless runs execute repository hooks | Documented CC behavior for `-p` and SDK ([CC hooks reference](https://code.claude.com/docs/en/hooks#workspace-trust)) | `--bare`, `disableAllHooks` via `--settings`; Codex per-hash trust without the bypass flag |
| Hook bypass by switching tools | [anthropics/claude-code#29709](https://github.com/anthropics/claude-code/issues/29709) | [Practice 11](#11-match-the-capability-not-a-single-tool) |
| Unhooked tool paths | Codex hosted tools such as `WebSearch` and some specialized tool paths ([Codex hooks](https://learn.chatgpt.com/docs/hooks)) | Network and sandbox limits; Codex web search `cached` mode |
| A mod or project setting overrides a hook | CC mods handling `tool.check`; project `disableAllHooks` ([CC hooks guide](https://code.claude.com/docs/en/hooks-guide)) | Managed hooks plus `allowManagedHooksOnly` |
| Prompt injection works around hooks | "Hooks are not a security boundary -- a prompt injection can work around them. They are structured prompt injection at opportune times" ([trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)) | Sandbox and deny rules for hard limits |
| Shell injection through tool input | [CC hooks reference, security considerations](https://code.claude.com/docs/en/hooks#security-considerations) | [Practice 10](#10-harden-hook-scripts-against-hostile-input) |
| Secrets leaked through hook output | Codex spill files ([Codex hooks](https://learn.chatgpt.com/docs/hooks)) | [Practice 8](#8-keep-hook-context-short-and-free-of-secrets) |
| Silent fail-open | Timeouts, crashes (exit 1, 127), Codex unsupported outputs, untrusted Codex hooks skipped | Exit 2 on internal errors; canary test after deploy |

No advisory specific to the Codex hooks system (as distinct from its MCP config or Git hooks) was found as of 2026-10-04.

## Verification

1. **Unit tests.** Pipe sample JSON: `echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh; echo $?`. Build payloads with `jq`, not string concatenation, and `chmod +x` the script ([CC hooks guide](https://code.claude.com/docs/en/hooks-guide)). Keep a fixtures directory of recorded stdin payloads per event and per lead; capture real ones by temporarily registering `cat > /tmp/hook-$EVENT.json`. Assert exit code, stdout JSON validity (`jq -e .`) and stderr. Include paths with spaces, quotes, `$()`, `..`, unicode, and missing fields (inference).
2. **Registration.** CC: `/hooks` shows the hook under the right event with its source label; "Matchers are case-sensitive"; restart if `/hooks` does not show an edit. Codex: `/hooks` lets you "inspect hook sources, review new or changed hooks, trust hooks, or disable individual non-managed hooks"; Codex prints a startup warning when hooks need review.
3. **Execution logs.** CC: `claude --debug-file /tmp/claude.log` and `tail -f`, or `/debug` mid-session; `Ctrl+O` opens the transcript. Codex documents no comparable hook execution log beyond `/hooks` and hook-failure reports.
4. **Integration.** Start each harness in a scratch repository, check `/hooks` and the Codex trust review, trigger the event with a scripted prompt (`claude -p`, `codex exec`) and assert on side effects or the debug log (inference).
5. **Canary.** After deploying a gate, trigger a block once on purpose. This catches a mistyped path (exit 127) and Codex's skipped-until-trusted state.
6. **Decision log.** Have each gate append timestamp, `session_id`, event, tool, decision and reason to a file outside the repository, independent of either harness's logging (inference).
7. **Bypass checks.** Try the blocked action through another tool (for example a `Bash` write after an `Edit` block) to confirm that the sandbox or a deny rule, not the hook alone, stops it.

## Checklist

- [ ] Each hook enforces a rule that must hold every time; judgement-based rules live in instructions.
- [ ] Every gate blocks with exit 2 or `permissionDecision: "deny"`; none rely on exit 1 or `ask`.
- [ ] Block reasons name the rule and the allowed alternative.
- [ ] Every `Stop` and `SubagentStop` gate checks `stop_hook_active` and prints JSON.
- [ ] Every synchronous hook has an explicit short `timeout` and a narrow matcher.
- [ ] Async hooks only observe.
- [ ] Scripts parse JSON with a parser, quote variables, use absolute paths and exit 2 on internal errors.
- [ ] Shared hooks handle both `tool_input.file_path` and Codex `apply_patch`.
- [ ] Security-relevant limits are also enforced by deny rules or the sandbox.
- [ ] Hook config changes need owner review; headless runs over third-party repositories disable project hooks.
- [ ] Non-negotiable hooks are managed, with managed-only hooks enabled where required.
- [ ] Each gate was triggered once after deployment and showed up in `/hooks` (and was trusted in Codex).

## Open questions

- **Codex exit codes** other than 0 and 2 on blocking events are undocumented; treat them as fail-open until verified.
- **Codex `Stop` continuation cap:** none documented, unlike CC's 8.
- **Codex `apply_patch` payload grammar** inside `tool_input.command` is not specified on the hooks page.
- **Codex matcher anchoring:** whether `Edit|Write` is anchored is not recorded.
- **Codex async timeout:** whether `timeout` is enforced on a running background hook is not stated.
- **Codex hook decisions vs approval policy and sandbox mode:** interaction is not documented beyond `permission_mode` being passed in the input.
- **Codex debug log:** no hook execution log comparable to CC's.
- **CC per-hook trust:** none documented; trust is per workspace only.
- **Evidence gaps:** no data on which hook use cases are most common or how much they help, no latency measurements, no comparison of bypass rates between hooks and rule or sandbox controls, and no Codex-published hooks best-practices page.

## Sources

- [Hooks concept](../concepts/hooks.md)
- [CC best practices](https://code.claude.com/docs/en/best-practices)
- [CC hooks guide](https://code.claude.com/docs/en/hooks-guide)
- [CC hooks reference](https://code.claude.com/docs/en/hooks)
- [CC permissions](https://code.claude.com/docs/en/permissions)
- [CC security](https://code.claude.com/docs/en/security)
- [CC security-guidance plugin](https://code.claude.com/docs/en/security-guidance)
- [anthropics/claude-code bash_command_validator_example.py](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)
- [hookify plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/hookify)
- [Codex hooks](https://learn.chatgpt.com/docs/hooks)
- [Codex managed configuration](https://learn.chatgpt.com/codex/enterprise/managed-configuration)
- [OpenCode plugins](https://opencode.ai/docs/plugins/)
- [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)
- [anthropics/claude-code#29709](https://github.com/anthropics/claude-code/issues/29709)
- [Galster et al., "Configuring Agentic AI Coding Tools: An Exploratory Study", arXiv:2602.14690](https://arxiv.org/abs/2602.14690)
- [Check Point Research: CC project files, GHSA-ph6w-f82w-28w6, CVE-2025-59536, CVE-2026-21852](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)
- [Check Point Research: Codex CLI CVE-2025-61260](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/)
- [NVD CVE-2026-19590](https://nvd.nist.gov/vuln/detail/CVE-2026-19590)
