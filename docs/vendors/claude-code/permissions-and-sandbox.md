# Permissions and sandbox

Permissions decide which tool calls Claude Code runs without asking, which it asks about, and which it refuses. They combine permission rules (`permissions.allow`, `ask`, `deny`), a permission mode (`default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`), managed policy, and hooks. The sandbox is a separate, OS-level layer that confines Bash, PowerShell, and Monitor commands and their children in filesystem and network access ([permissions](https://code.claude.com/docs/en/permissions); [permission modes](https://code.claude.com/docs/en/permission-modes); [sandboxing](https://code.claude.com/docs/en/sandboxing)).

## Locations and scopes

- Rules live in the `permissions` key of any settings file (user, shared project, local project, managed, `--settings`); see [configuration.md](configuration.md) for file locations and precedence. Rule lists merge across scopes ([settings](https://code.claude.com/docs/en/settings)).
- Deny in any scope beats allow in any scope ([permissions](https://code.claude.com/docs/en/permissions)).
- Project `permissions.allow` and `permissions.additionalDirectories` wait for workspace trust; `deny` and `ask` apply immediately ([settings](https://code.claude.com/docs/en/settings)).
- Managed policy: no other level can override a managed rule. `allowManagedPermissionRulesOnly` makes managed the only rule source. `disableBypassPermissionsMode: "disable"` works from any scope ([permissions](https://code.claude.com/docs/en/permissions)).
- `autoMode` (classifier customization: `environment`, `allow`, `soft_deny`, `hard_deny`) is honored in user or managed scope only ([permission modes](https://code.claude.com/docs/en/permission-modes); [settings reference](https://code.claude.com/docs/en/settings-reference)).
- `/sandbox` saves to `.claude/settings.local.json` ([sandboxing](https://code.claude.com/docs/en/sandboxing)).
- Sandbox arrays (`filesystem.*`) merge across scopes ([sandboxing](https://code.claude.com/docs/en/sandboxing); [settings reference](https://code.claude.com/docs/en/settings-reference)).

### Working directories

- Extend access with `--add-dir`, `/add-dir`, `permissions.additionalDirectories`, or move with `/cd` ([permissions](https://code.claude.com/docs/en/permissions)).
- `permissions.additionalDirectories` grants file access only. `--add-dir` and `/add-dir` directories also load skills, commands, agents, and the `enabledPlugins`/`extraKnownMarketplaces` keys, plus CLAUDE.md only with `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` ([permissions](https://code.claude.com/docs/en/permissions)).

## Format

### Rule syntax

Rules are `Tool` or `Tool(specifier)` strings in `permissions.allow`, `permissions.ask`, and `permissions.deny` ([permissions](https://code.claude.com/docs/en/permissions)).

- A bare tool name in deny (e.g. `Bash`) removes the tool from Claude's context; a scoped deny blocks matching calls. Exception: `EndConversation` cannot be removed.
- Deny and ask rules can match one top-level scalar input parameter as `Tool(param:value)`, with `*` wildcards. Examples: `Agent(model:opus)`, `Bash(run_in_background:true)`, `Bash(dangerouslyDisableSandbox:true)`. Primary content fields such as `command`, `file_path`, and `url` are not matchable this way.
- Tool-name globs: `"*"` and `"mcp__*"` are accepted in deny and ask. Allow rules accept globs only after a literal `mcp__<server>__` prefix.
- Settings files skip any `mcp__` rule that has parentheses; use `--disallowedTools` for MCP parameter rules.
- Rules must use canonical tool names (see the tools reference), not UI labels.

Source: [permissions](https://code.claude.com/docs/en/permissions)

#### Bash (and PowerShell)

- `*` matches any text including spaces. A trailing ` *` also matches the bare command. `:*` is a legacy-equivalent trailing wildcard. Put the `*` after the subcommand (`Bash(git log *)`), not before it.
- Compound commands are split on `&&`, `||`, `;`, `|`, `|&`, `&`, and newlines; each subcommand must match an allow rule. Deny and ask rules match nested commands, including subshells and `$(...)`.
- These wrappers are stripped before matching: `timeout`, `time`, `nice`, `nohup`, `stdbuf`, `command`, `builtin`, `noglob`, and flagless `xargs`. Known-safe env assignments are also stripped.
- A built-in, non-configurable read-only command set (`ls`, `cat`, `grep`, `find`, `git` read forms, …) runs without a prompt in every mode. Redirect targets (`>`, `<`, `tee`) are checked against Edit and Read rules.
- "Yes, and don't ask again" for a compound command saves up to 5 per-subcommand rules.
- PowerShell rules mirror Bash, with alias canonicalization.

Source: [permissions](https://code.claude.com/docs/en/permissions)

#### Read and Edit (gitignore syntax)

| Pattern | Meaning |
| :- | :- |
| `//abs/path` | Absolute filesystem path |
| `~/path` | Home-relative |
| `/path` | Relative to the settings source: the project root for project and local files, `~/.claude/` for the user file, the file's own directory for `--settings` |
| `path` or `./path` | Relative to the cwd |

Source: [permissions](https://code.claude.com/docs/en/permissions)

- Write, NotebookEdit, Glob, and MultiEdit path rules are never consulted (a startup warning appears). Use `Edit(...)` and `Read(...)`.
- A `Read` deny also blocks Edit and Write on that path.
- A `!` negation carves out exceptions within the same source.
- Symlinks: an allow must match both the requested path and its target; a deny matches either.

Source: [permissions](https://code.claude.com/docs/en/permissions)

#### Other tools

| Rule | Meaning |
| :- | :- |
| `WebFetch(domain:example.com)` | Domain rule; `*.example.com` and `*` accepted. A bare `WebFetch` allow skips prompts but does not widen the sandbox; `WebFetch(domain:*)` also feeds the sandbox allowlist |
| `mcp__server`, `mcp__server__*`, `mcp__server__tool` | MCP tools; see [mcp.md](mcp.md) |
| `Agent(Name)` | Subagent types; see [subagents.md](subagents.md) |
| `Skill`, `Skill(name)`, `Skill(name *)` | Skill invocation by Claude ([skills](https://code.claude.com/docs/en/skills)); see [skills.md](skills.md) |
| `Cd(path)` | `/cd` targets |

Source: [permissions](https://code.claude.com/docs/en/permissions) unless noted

### Permission keys

| Key | Meaning |
| :- | :- |
| `permissions.allow` / `ask` / `deny` | Rule lists |
| `permissions.additionalDirectories` | Extra directories with file access |
| `permissions.blockReadsOutsideWorkingDirectories` | Reads outside working dirs are never auto-approved while on |
| `permissions.defaultMode` | Starting mode; `auto` and `bypassPermissions` do not take effect from project or local files |
| `permissions.disableBypassPermissionsMode` | `"disable"` blocks bypass mode; works from any scope |
| `permissions.disableAutoMode` | `"disable"` forces `default` as starting mode |
| `autoMode` | Classifier rules: `environment`, `allow`, `soft_deny`, `hard_deny` (user or managed only) |
| `allowManagedPermissionRulesOnly` | Managed-only; managed is the only rule source |
| `skipDangerousModePermissionPrompt` | Set by the first-use bypass dialog |
| `useAutoModeDuringPlan` | Classifier reviews shell commands in plan mode (default on) |

Sources: [settings reference](https://code.claude.com/docs/en/settings-reference); [permissions](https://code.claude.com/docs/en/permissions); [permission modes](https://code.claude.com/docs/en/permission-modes)

### Permission modes

| Mode | What runs without asking |
| :- | :- |
| `default` ("Manual"; `manual` alias in v2.1.200+) | Reads only |
| `acceptEdits` | Also file edits and `mkdir`/`touch`/`rm`/`rmdir`/`mv`/`cp`/`sed` inside working dirs |
| `plan` | Read-only exploration, plus classifier-approved commands when auto is available |
| `auto` | Classifier reviews actions |
| `dontAsk` | Anything that would prompt is denied; for CI |
| `bypassPermissions` | Everything except the never-auto-approved set |

Source: [permission modes](https://code.claude.com/docs/en/permission-modes)

### Sandbox keys

All under `sandbox` ([sandboxing](https://code.claude.com/docs/en/sandboxing); [settings reference](https://code.claude.com/docs/en/settings-reference)):

| Key | Meaning |
| :- | :- |
| `enabled` | Turn the sandbox on (off by default) |
| `failIfUnavailable` | `true`: fail instead of running unsandboxed when the sandbox cannot start |
| `autoAllowBashIfSandboxed` | Default `true` ("auto-allow mode"): sandboxed commands run without prompts. `false`: regular-permissions mode |
| `allowUnsandboxedCommands` | `false` ("strict sandbox mode") disables the `dangerouslyDisableSandbox` retry |
| `excludedCommands` | Commands run outside the sandbox; Bash-rule syntax; every subcommand must match |
| `filesystem.allowWrite` | Extra writable paths |
| `filesystem.denyWrite` | Paths not writable |
| `filesystem.denyRead` | Paths not readable |
| `filesystem.allowRead` | Re-opens a path inside a `denyRead` region; the narrower path wins |
| `filesystem.disabled` | Filesystem isolation off, network isolation kept |
| `network.allowedDomains` | Proxy allowlist (initially empty) |
| `network.deniedDomains` | Proxy denylist |
| `network.allowUnixSockets`, `network.allowAllUnixSockets` | Unix socket access |
| `network.allowLocalBinding` | Allow binding local ports |
| `network.allowMachLookup` | macOS Mach lookups |
| `network.strictAllowlist` | User or managed: deny instead of prompting |
| `network.allowManagedDomainsOnly` | Managed: only managed domains |
| `network.httpProxyPort`, `network.socksProxyPort` | Custom proxy |
| `network.tlsTerminate` | Experimental |
| `credentials.{envVars,files,awsPairs,sigv4,allowPlaintextInject}` | Mask or hide secrets |
| `enableWeakerNestedSandbox`, `enableWeakerNetworkIsolation` | Weaker isolation options |
| `ignoreViolations`, `allowAppleEvents`, `bwrapPath`, `socatPath`, `ripgrep` | Other options |

Sandbox paths use normal conventions (`/abs`, `~/`, relative to the settings file location). Permission rules use `//` and `/` instead ([sandboxing](https://code.claude.com/docs/en/sandboxing)).

## Loading and invocation

### Rule evaluation

- Order: deny, then ask, then allow. The first match decides; specificity is irrelevant. A broad deny such as `Bash(aws *)` cannot be carved out by a narrower allow ([permissions](https://code.claude.com/docs/en/permissions)).
- `PreToolUse` hooks run before the prompt. They can deny, force ask, or allow, but never override deny or ask rules. Exit code 2 blocks the call even when an allow rule matches ([permissions](https://code.claude.com/docs/en/permissions)). See [hooks.md](hooks.md).
- Mods (v2.1.287+) answering `tool.check` can override ask rules and non-managed hook blocks ([permissions](https://code.claude.com/docs/en/permissions); [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)). See [plugins.md](plugins.md#mods).

### Starting mode and switching

- Starting mode order: `--permission-mode` flag, then `permissions.defaultMode`, then the built-in default ([permission modes](https://code.claude.com/docs/en/permission-modes)).
- Built-in default as of v2.1.283: `auto` for terminal and VS Code. For `-p` and the SDK: `default` in sessions that fetch feature flags, otherwise `auto` (v2.1.285+). `disableAutoMode: "disable"` forces `default` ([permission modes](https://code.claude.com/docs/en/permission-modes); [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- Shift+Tab cycles `default` → `acceptEdits` → `plan`, then optional modes: `bypassPermissions` only if enabled at launch, then `auto`. `dontAsk` is never in the cycle ([permission modes](https://code.claude.com/docs/en/permission-modes)).
- Auto mode availability: all plans, and on Team/Enterprise unless an admin disables it. Supported models on the Anthropic API: Opus 4.6+, Sonnet 4.6+, Fable. On Bedrock, Vertex, and Foundry: Sonnet 5+, Opus 4.7+, Fable ([permission modes](https://code.claude.com/docs/en/permission-modes)).

### Never auto-approved, in any mode

- Explicit ask rules
- Org-"ask" connector tools
- `AskUserQuestion`, and MCP tools with `_meta["anthropic/requiresUserInteraction"]`
- `rm`/`rmdir` on critical paths
- Cross-session messaging safeguards
- Reads outside working dirs while `blockReadsOutsideWorkingDirectories` is on

Source: [permission modes](https://code.claude.com/docs/en/permission-modes)

### Protected paths

Writes are never auto-approved except in bypass mode, and allow rules do not pre-approve them ([permission modes](https://code.claude.com/docs/en/permission-modes)):

- Directories: `.git`, `.config/git`, `.vscode`, `.idea`, `.husky`, `.cargo`, `.devcontainer`, `.yarn`, `.mvn`, and `.claude` (except `.claude/worktrees` and the auto memory markdown).
- Files: shell rc files, `.gitconfig`, `.npmrc`, `.mcp.json`, `.claude.json`.

### Sandbox coverage

- Built on `@anthropic-ai/sandbox-runtime`. macOS: Seatbelt. Linux and WSL2: bubblewrap + socat. Native Windows: unsandboxed ([sandboxing](https://code.claude.com/docs/en/sandboxing)).
- Applies to Bash, PowerShell, and Monitor commands and their children. Runs outside the sandbox: built-in file and web tools, hooks, local MCP servers, plugin monitors, LSP servers, the status line, `apiKeyHelper`, `!` shell-mode commands (in most sessions), `excludedCommands`, and approved unsandboxed retries ([sandboxing](https://code.claude.com/docs/en/sandboxing)).
- Off by default. Enable with `/sandbox` or `sandbox.enabled`. `/sandbox` opens a panel with Mode, Overrides, and Config tabs, plus a Dependencies tab on Linux ([sandboxing](https://code.claude.com/docs/en/sandboxing)).

Defaults ([sandboxing](https://code.claude.com/docs/en/sandboxing)):

| Access | Default |
| :- | :- |
| Writes | cwd, a per-user temp dir (`$TMPDIR` is set to it), `--add-dir`/`additionalDirectories` |
| Reads | Whole machine, including `~/.ssh` (use `denyRead` or `credentials`) |
| Network | No direct route; an HTTP/SOCKS proxy checks hostnames against allowed domains (initially empty) |
| Env | Inherited |

- Auto-allow mode (`autoAllowBashIfSandboxed: true`): sandboxed commands run without prompts. Deny rules, content-scoped ask rules such as `Bash(git push *)`, and critical-path `rm` still apply; a bare `Bash` ask rule is skipped, except in plan mode ([sandboxing](https://code.claude.com/docs/en/sandboxing)).
- Unsandboxed retry: Claude can retry with `dangerouslyDisableSandbox`; who approves depends on the mode. `allowUnsandboxedCommands: false` disables the retry. A `false` from user, `--settings`, or managed settings beats a project `true` (v2.1.285+) ([sandboxing](https://code.claude.com/docs/en/sandboxing)).
- When managed settings or `--settings` disable the retry, the sandbox becomes "admin-required", and repo settings that loosen it are ignored. Since v2.1.281, project settings cannot widen an admin-required sandbox ([sandboxing](https://code.claude.com/docs/en/sandboxing); [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- Network: `WebFetch(domain:...)` allow and deny rules merge into the allowlist. Non-HTTP tools (ssh, DB drivers) and UDP/QUIC/ICMP cannot reach the network. Hostnames resolving only to loopback or link-local addresses are refused. In auto mode, commands carry per-command allowed hosts for the classifier to review ([sandboxing](https://code.claude.com/docs/en/sandboxing)).

### CLI and slash commands

- `/permissions`: dialog showing rules by source file ([permissions](https://code.claude.com/docs/en/permissions)).
- Flags: `--allowedTools`, `--disallowedTools`, `--permission-mode`, `--dangerously-skip-permissions`, `--allow-dangerously-skip-permissions`, `--permission-prompts host|none` ([permissions](https://code.claude.com/docs/en/permissions); local CLI help).
- `--restricted` (v2.1.248+) removes code-running tools, ignores user, project, and local settings, and refuses bypass (local CLI help; [permission modes](https://code.claude.com/docs/en/permission-modes)).
- Plan mode: see [automation.md](automation.md#plan-mode).

## Example

Permission rules ([settings](https://code.claude.com/docs/en/settings)):

```json
{
  "permissions": {
    "allow": ["Bash(npm run lint)", "Bash(npm run test *)"],
    "deny": ["Read(./.env)", "Read(./.env.*)"]
  }
}
```

Sandbox ([sandboxing](https://code.claude.com/docs/en/sandboxing)):

```json
{
  "sandbox": {
    "enabled": true,
    "filesystem": { "allowWrite": ["~/.kube", "/tmp/build"] },
    "excludedCommands": ["docker compose *"]
  }
}
```

For one session only: `claude --settings '{"sandbox":{"enabled":true,"allowUnsandboxedCommands":false}}'` ([sandboxing](https://code.claude.com/docs/en/sandboxing)).

## Limits and gotchas

- A Bash rule is not a security boundary: `Bash(curl *)` does not stop `/usr/bin/curl` or `sh -c 'curl ...'` ([permissions](https://code.claude.com/docs/en/permissions)). Inference (from the research notes): treat Bash rules as UX controls; the docs point to the sandbox or hooks for enforcement.
- `.claudeignore` has no effect; use Read deny rules ([permissions](https://code.claude.com/docs/en/permissions)).
- Write, NotebookEdit, Glob, and MultiEdit path rules are silently not consulted apart from a startup warning ([permissions](https://code.claude.com/docs/en/permissions)).
- Default mode change: as of v2.1.283, `auto` is the built-in starting mode for interactive terminal and VS Code sessions. Inference (from the research notes): guidance that assumes "default prompts for everything" is out of date.
- `bypassPermissions` is refused as root or under sudo on Linux and macOS, and refused under `--restricted`. First use shows a dialog that sets `skipDangerousModePermissionPrompt`. Cloud sessions ignore `bypassPermissions` and `dontAsk` from settings files ([permission modes](https://code.claude.com/docs/en/permission-modes)).
- Before v2.1.257, `permissions.defaultMode: bypassPermissions` took effect from any settings file ([settings](https://code.claude.com/docs/en/settings)).
- `CLAUDE_CODE_ENABLE_AUTO_MODE` has had no effect since v2.1.207 ([permission modes](https://code.claude.com/docs/en/permission-modes)).
- `-p` and SDK runs never show the trust dialog. Project allow rules are not used, but hooks and `env` are ([permissions](https://code.claude.com/docs/en/permissions)).
- Sandbox defaults allow reads everywhere, including `~/.ssh`. If the sandbox cannot start, commands run unsandboxed unless `failIfUnavailable: true` ([sandboxing](https://code.claude.com/docs/en/sandboxing)). Inference (from the research notes): with default settings the sandbox mainly reduces prompts and limits writes and network; protecting secrets needs `denyRead`, `credentials`, or `blockReadsOutsideWorkingDirectories`.
- Sandbox-protected paths cannot be exempted by `allowWrite`: `.claude` settings, skills, agents, commands, hooks, `.mcp.json`, shell rc files, `.git/hooks` and `.git/config`, and most of `~/.claude` ([sandboxing](https://code.claude.com/docs/en/sandboxing)).
- Gap (research notes): the full list of what the auto-mode classifier blocks by default, and the critical-path list in detail, were not extracted.
- Gap (research notes): the "Protect credentials / Mask credentials" sections and managed-sandbox lock details were not read in full.

## Sources

- https://code.claude.com/docs/en/permissions
- https://code.claude.com/docs/en/permission-modes
- https://code.claude.com/docs/en/sandboxing
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/settings-reference
- https://code.claude.com/docs/en/skills
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- Local CLI help: `claude --help` (v2.1.289)
