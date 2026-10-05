# Claude Code configuration: the foundation layer (instructions and memory, settings, permissions, sandboxing, MCP, plugins and marketplaces, output styles, models)

Research date: 2026-10-04. Installed version checked: Claude Code 2.1.289 (`claude --version`). Primary sources: the official docs at code.claude.com/docs (I fetched the raw `.md` pages on 2026-10-04), the anthropics/claude-code CHANGELOG.md, and local read-only `--help` output. Doc URLs are given without the `.md` suffix. "Local CLI help" means output of `claude --help`, `claude mcp --help`, `claude mcp add --help`, `claude plugin --help`, `claude plugin install --help`, and `claude plugin marketplace add --help` on v2.1.289.

Source key (used in citations below):
- MEM = https://code.claude.com/docs/en/memory
- SET = https://code.claude.com/docs/en/settings
- SREF = https://code.claude.com/docs/en/settings-reference
- MSET = https://code.claude.com/docs/en/managed-settings
- PERM = https://code.claude.com/docs/en/permissions
- PMODE = https://code.claude.com/docs/en/permission-modes
- SBX = https://code.claude.com/docs/en/sandboxing
- MCP = https://code.claude.com/docs/en/mcp
- MMCP = https://code.claude.com/docs/en/managed-mcp
- PMAN = https://code.claude.com/docs/en/plugins/manifest-reference
- PMKT = https://code.claude.com/docs/en/plugins/marketplace-reference
- PINST = https://code.claude.com/docs/en/plugins/install
- PCLI = https://code.claude.com/docs/en/plugins/cli-reference
- PLOAD = https://code.claude.com/docs/en/plugins/loading
- POV = https://code.claude.com/docs/en/plugins/overview
- OST = https://code.claude.com/docs/en/output-styles
- MODEL = https://code.claude.com/docs/en/model-config
- SL = https://code.claude.com/docs/en/statusline
- ENV = https://code.claude.com/docs/en/env-vars
- CMD = https://code.claude.com/docs/en/commands
- CL = https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md

## Memory and instructions: the CLAUDE.md hierarchy, imports, CLAUDE.local.md, .claude/rules, auto memory, /memory, /init, and AGENTS.md

### Takeaway
Claude Code has two memory systems, and both load at session start. CLAUDE.md files are written by you; they are concatenated, never overridden, from managed scope through user and project to local, plus subdirectory files that load on demand. Auto memory is written by Claude to `~/.claude/projects/<project>/memory/`, and only the first 200 lines or 25KB of its MEMORY.md index load at startup. Since v2.1.277, Claude Code reads AGENTS.md natively, by default only when no CLAUDE.md or CLAUDE.local.md exists on the path. This is controlled by the "Project instructions" setting of the built-in `agents-md` plugin. `.claude/rules/*.md` files with optional `paths:` frontmatter give path-scoped, lazily loaded instructions.

### Cited Findings
**What CLAUDE.md is**
- CLAUDE.md and auto memory are both loaded at the start of every conversation. They act as context, not enforced configuration. To block an action regardless of what Claude decides, the docs point to PreToolUse hooks — [MEM](https://code.claude.com/docs/en/memory)
- CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt. For system-prompt-level instructions, use `--append-system-prompt` — [MEM](https://code.claude.com/docs/en/memory)

**Locations, in load order (broadest first)**

| Scope | Location |
| :- | :- |
| Managed policy | macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`; Linux/WSL `/etc/claude-code/CLAUDE.md`; Windows `C:\Program Files\ClaudeCode\CLAUDE.md` |
| User | `~/.claude/CLAUDE.md` |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` |
| Local | `./CLAUDE.local.md` (personal; add it to `.gitignore`) |

Source: [MEM](https://code.claude.com/docs/en/memory)

**How files load and merge**
- At launch, Claude Code loads CLAUDE.md and CLAUDE.local.md from the working directory and every ancestor directory. All files are concatenated, ordered from the filesystem root down to the cwd, so closer files are read last. Within one directory, CLAUDE.local.md is appended after CLAUDE.md. CLAUDE.md files in subdirectories load on demand, when Claude reads files there — [MEM](https://code.claude.com/docs/en/memory)
- Block-level HTML comments (`<!-- ... -->`) are stripped before injection, which saves tokens. Comments inside code blocks are kept — [MEM](https://code.claude.com/docs/en/memory)

**Size limits and context cost**
- The docs recommend under 200 lines per file. A CLAUDE.md up to 4 MiB loads in full; a larger file is skipped. A warning appears at startup and in `/status` when a file is over the recommended length, or when several files together pass a combined limit — [MEM](https://code.claude.com/docs/en/memory)
- `@path` imports do not reduce context cost, because imported files also load at launch — [MEM](https://code.claude.com/docs/en/memory)

**Imports (`@path`)**
- The `@path/to/file` syntax accepts relative paths (resolved against the importing file) and absolute paths, including `@~/...`. Imports can recurse up to 4 hops deep — [MEM](https://code.claude.com/docs/en/memory)
- Escape spaces with a backslash. A quoted path is never imported. Imports inside code spans and fences are ignored, so wrapping a path in backticks keeps it literal — [MEM](https://code.claude.com/docs/en/memory)
- An import in a project file that resolves outside the working directory is "external". The first time, Claude Code shows a one-time approval dialog; if you decline, the imports stay disabled. Imports from user-scope files load without the dialog, except in Cowork — [MEM](https://code.claude.com/docs/en/memory)

**Compaction and debugging**
- After `/compact`, the project-root CLAUDE.md is re-read from disk and re-injected. Nested CLAUDE.md files and path-scoped rules reload when matching files are read again — [MEM](https://code.claude.com/docs/en/memory)
- Debugging tools: `/context` lists "Memory files", `/memory` opens and creates files, `/doctor prompt-audit` (v2.1.283+) audits instruction files, and the `InstructionsLoaded` hook logs which files loaded and why — [MEM](https://code.claude.com/docs/en/memory)

**Additional directories**
- CLAUDE.md files in `--add-dir` directories are not loaded by default. Set `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` to load their CLAUDE.md, `.claude/CLAUDE.md`, `.claude/rules/*.md`, and CLAUDE.local.md — [MEM](https://code.claude.com/docs/en/memory)

**Exclusions and managed content**
- `claudeMdExcludes` takes glob patterns matched against absolute paths. It works from any settings layer, and arrays merge across layers. The managed CLAUDE.md cannot be excluded — [MEM](https://code.claude.com/docs/en/memory)
- The managed-only `claudeMd` key puts CLAUDE.md content directly inside managed settings. For example: `{"claudeMd": "Always run \`make lint\` before committing."}`. It is ignored in user, project, and local settings — [MEM](https://code.claude.com/docs/en/memory)
- Environment variables: `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` prevents loading any CLAUDE.md, including auto memory files. `--bare` (which sets `CLAUDE_CODE_SIMPLE=1`) skips CLAUDE.md auto-discovery and auto memory. `--safe-mode` disables CLAUDE.md, skills, plugins, hooks, MCP, and more for troubleshooting — [ENV](https://code.claude.com/docs/en/env-vars); local CLI help

**`.claude/rules/`**
- Every `.md` file in `.claude/rules/` is discovered recursively. A rule without `paths` loads at launch with the same priority as `.claude/CLAUDE.md` — [MEM](https://code.claude.com/docs/en/memory)
- With `paths:` frontmatter (a YAML list or a comma-separated string of globs, with brace expansion), a rule loads only when Claude uses Read, Write, or Edit on a matching file. Write and Edit triggering was fixed in v2.1.288 — [MEM](https://code.claude.com/docs/en/memory); [CL](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- `paths` is the only frontmatter field read; any other field is ignored. Brace expansion is capped at 1,000 expanded patterns or 4 MiB per rule — [MEM](https://code.claude.com/docs/en/memory)
- User-level rules in `~/.claude/rules/` load before project rules. Symlinks are supported, but a symlink target outside the project is treated like an external import. Project rules are skipped when `--setting-sources` excludes `project` — [MEM](https://code.claude.com/docs/en/memory)
- `.claude/rules/` was added in v2.0.64 — [CL](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- Minimal rule example: a file `.claude/rules/api.md` containing

  ```
  ---
  paths:
    - "src/api/**/*.ts"
  ---
  - All API endpoints must include input validation
  ```

  Source: [MEM](https://code.claude.com/docs/en/memory)

**AGENTS.md**
- Default behavior: Claude reads AGENTS.md (and `.claude/AGENTS.md`) from the cwd and its ancestors only if no CLAUDE.md, `.claude/CLAUDE.md`, or CLAUDE.local.md exists in the cwd or above it. `~/.claude/CLAUDE.md`, the managed CLAUDE.md, and `.claude/rules/` do not count for this check — [MEM](https://code.claude.com/docs/en/memory)
- A subdirectory's AGENTS.md loads when Claude reads a file there, if that subdirectory has no CLAUDE.md files of its own. These are never read: `AGENTS.local.md`, `AGENTS.override.md`, and anything under `.agents/` — [MEM](https://code.claude.com/docs/en/memory)
- The "Project instructions" setting (`/config`) takes one of four values:

  | Value | Effect |
  | :- | :- |
  | `claude-md-or-agents-md` (default) | CLAUDE.md files, or AGENTS.md when no CLAUDE.md exists |
  | `claude-md-and-agents-md` | Both; per directory, CLAUDE.md first, then AGENTS.md, deduplicated |
  | `claude-md` | CLAUDE.md only |
  | `managed-only` | Managed CLAUDE.md and auto memory only |

  Source: [MEM](https://code.claude.com/docs/en/memory)
- The setting is stored as `pluginConfigs["agents-md@builtin"].options.instructionFiles`. It is honored in user, `--settings`, and managed settings, and ignored in project and local settings — [MEM](https://code.claude.com/docs/en/memory)
- Version history: native AGENTS.md support arrived in v2.1.277. v2.1.281 extended it to Bedrock, Vertex, Foundry, gateways, and sessions with telemetry off. Disabling the built-in `agents-md` plugin turns it off. An AGENTS.md read through this setting does not fire `InstructionsLoaded` hooks — [MEM](https://code.claude.com/docs/en/memory); [CL](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- The older workaround, a CLAUDE.md containing `@AGENTS.md` or a symlink `ln -s AGENTS.md CLAUDE.md`, still works and never double-loads. A SessionStart hook that prints AGENTS.md should be removed, because it now adds a duplicate — [MEM](https://code.claude.com/docs/en/memory)

**Auto memory**
- Claude saves four types of notes, recorded as frontmatter `type`: `user`, `feedback`, `project`, and `reference`. Claude writes them itself and skips anything derivable from the code — [MEM](https://code.claude.com/docs/en/memory)
- Storage is `~/.claude/projects/<project>/memory/`, with a `MEMORY.md` index plus one topic file per memory. `<project>` is derived from the git repo, so worktrees share one directory. Memory is machine-local — [MEM](https://code.claude.com/docs/en/memory)
- Only the first 200 lines or 25KB of MEMORY.md load at session start. Topic files are read on demand. A write that pushes the index over the limit returns an error telling Claude to rewrite it — [MEM](https://code.claude.com/docs/en/memory)
- Auto memory is on by default in local sessions and off by default in self-hosted environments — [MEM](https://code.claude.com/docs/en/memory)
- Ways to toggle it: the `/memory` toggle writes `autoMemoryEnabled` to `~/.claude/settings.json`. `autoMemoryEnabled: false` in project settings turns it off per project. `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` turns it off; `=0` forces it on — [MEM](https://code.claude.com/docs/en/memory); [ENV](https://code.claude.com/docs/en/env-vars)
- `autoMemoryDirectory` relocates the store (an absolute path or `~/`). It is honored from any scope, subject to workspace trust in project files. `CLAUDE_CODE_PROJECT_DIR_NAME` (v2.1.234+) overrides the `<project>` name — [MEM](https://code.claude.com/docs/en/memory)
- Auto memory is not loaded into subagents, except forks. Subagents can have their own memory through the `memory` field. Since v2.1.214, a `modified` timestamp is added to the frontmatter of memory files that have frontmatter — [MEM](https://code.claude.com/docs/en/memory)

**`/memory` and `/init`**
- `/memory` lists the CLAUDE.md, CLAUDE.local.md, and memory locations at user and project scope, opens them in an editor (creating missing files), toggles auto memory, and opens the auto memory folder — [MEM](https://code.claude.com/docs/en/memory); [CMD](https://code.claude.com/docs/en/commands)
- `/init` generates a CLAUDE.md, or suggests improvements to an existing one. It incorporates `.cursor/rules`, `.cursorrules`, and `.github/copilot-instructions.md` — [MEM](https://code.claude.com/docs/en/memory)
- With `CLAUDE_CODE_NEW_INIT=1`, `/init` runs an interactive multi-phase flow that can create CLAUDE.md files, skills, and hooks. It also reads AGENTS.md, `.devin/rules/`, `.windsurf/rules/`, and `.clinerules`. `/import` (v2.1.213+) imports configuration from Codex, Gemini CLI, or Cursor — [MEM](https://code.claude.com/docs/en/memory); [CMD](https://code.claude.com/docs/en/commands)

### Inferences
- For context budgeting, everything at launch is an always-on cost: ancestor CLAUDE.md files, imports, unscoped rules, and up to 25KB of MEMORY.md. Path-scoped rules, nested CLAUDE.md files, and memory topic files cost context only when triggered. Skills are the on-demand alternative for procedures.
- A repo that targets several agents can keep a single AGENTS.md and no CLAUDE.md. Adding a personal CLAUDE.local.md silently disables AGENTS.md loading unless "Project instructions" is set to `claude-md-and-agents-md`.

### Gaps
- The docs do not publish the "combined limit" across instruction files that triggers the startup warning.
- I did not verify the exact on-disk name derivation for `<project>` (path sanitization) beyond "derived from the git repository".

## settings.json: scopes, precedence and merge rules, important keys

### Takeaway
There are four settings scopes plus CLI overrides. Precedence from highest to lowest:
1. Managed (server, MDM, or file)
2. Command line (`--settings` and flags)
3. `.claude/settings.local.json`
4. `.claude/settings.json`
5. `~/.claude/settings.json`

Scalar keys override; list keys such as `permissions.allow` merge across scopes. A handful of security keys honor the stricter value from any scope. Settings hot-reload, except a few startup-only keys such as `model`. About 240 keys are documented in the settings reference, many of them scope-restricted (user-or-managed only, or managed only).

### Cited Findings
**Files and scopes**

| Scope | File | Who it affects |
| :- | :- | :- |
| User | `~/.claude/settings.json` | You, in all projects |
| Shared project | `.claude/settings.json` | Committed; affects the whole team |
| Project local | `.claude/settings.local.json` | You, in this project |
| Managed | `managed-settings.json`, MDM, or server-managed | Your organization |

- `~/.claude.json` is a separate file that Claude Code writes itself. It holds auth, MCP server configs (local and user scope), per-project state such as trust decisions, and the "Global config" keys — [SET](https://code.claude.com/docs/en/settings)
- `CLAUDE_CONFIG_DIR` relocates `~/.claude` — [SET](https://code.claude.com/docs/en/settings); [ENV](https://code.claude.com/docs/en/env-vars)
- Since v2.1.211, `.claude/settings.local.json` is read and written at the git repo root, or the main checkout root for a worktree. It is auto-added to global git excludes as `**/.claude/settings.local.json` the first time Claude Code writes it. Its allow rules skip workspace trust while the file is untracked — [SET](https://code.claude.com/docs/en/settings)
- The shared `.claude/settings.json` is read from the session's primary working directory, with no parent fallback. `/cd` re-reads project settings from the new directory (v2.1.246+) — [SET](https://code.claude.com/docs/en/settings); [PERM](https://code.claude.com/docs/en/permissions)

**Precedence and merging**
- Precedence, highest first: (1) managed; (2) command line (`--settings <file-or-json>`, which merges by the same rules, plus flags); (3) project local; (4) shared project; (5) user — [SET](https://code.claude.com/docs/en/settings)
- Environment variables are not a level in this stack. Precedence between a variable and its paired key is decided per pair. For example, `ANTHROPIC_MODEL` beats the `model` key, while `ANTHROPIC_DEFAULT_MODEL` applies only when no file sets `model` — [SET](https://code.claude.com/docs/en/settings)
- Lists merge across files. Exceptions:
  - `fallbackModel`: the highest file wins whole.
  - `modelPicker`: the highest of managed, `--settings`, or user wins whole; it is ignored in project and local files.
  - `availableModels`: a managed list is applied as-is.
  - `modelSettings`: resolved per model.

  Source: [SET](https://code.claude.com/docs/en/settings)
- Exceptions to managed precedence, where the stricter value from a lower scope wins:
  - `disableClaudeAiConnectors: true`
  - `enableArtifact: false`
  - `isolatePeerMachines: true`
  - `remoteControlAtStartup: false` (project or local)
  - `crossSessionInbound`, when stricter
  - `useAutoModeDuringPlan: false`
  - `syncClaudeAiSkills: false` and `syncClaudeAiPlugins: false`
  - `maxEffortLevel`, where the lowest cap wins

  Source: [SET](https://code.claude.com/docs/en/settings)

**Format, validation, and reload**
- Files are strict JSON: no comments, no trailing commas. Add `"$schema": "https://json.schemastore.org/claude-code-settings.json"` for editor validation (the schema can lag the CLI) — [SET](https://code.claude.com/docs/en/settings)
- Broken files: invalid JSON or a schema-rejected value causes a "Settings Error" dialog; bad individual entries cause a "Settings Warning" and are skipped. With `-p`, broken files or entries are silently skipped; run `claude doctor` to list rejected entries — [SET](https://code.claude.com/docs/en/settings); local CLI help
- Files are watched and hot-reloaded, including `permissions`, `hooks`, and `apiKeyHelper`. A `ConfigChange` hook fires on each change. Startup-only keys include `model`, `effortLevel`, and `modelSettings` (use `/model` and `/effort` mid-session instead) — [SET](https://code.claude.com/docs/en/settings)
- `/status` shows a "Setting sources" line listing which files loaded. `/config` edits a subset of keys and also accepts `/config key=value` — [SET](https://code.claude.com/docs/en/settings)

**Keys a repository cannot set**
- Keys whose scope is "User, local, or managed", "User or managed", "Managed", or "Global config" never take effect from the shared project file — [SET](https://code.claude.com/docs/en/settings)
- `permissions.defaultMode` values `auto` and `bypassPermissions` do not take effect from project or local files. Before v2.1.257, `bypassPermissions` took effect from any file — [SET](https://code.claude.com/docs/en/settings)
- These wait for workspace trust: `permissions.allow`, `permissions.additionalDirectories`, `extraKnownMarketplaces`, and most `env` values. `deny` and `ask` rules apply immediately — [SET](https://code.claude.com/docs/en/settings)

**Important keys (all from [SREF](https://code.claude.com/docs/en/settings-reference))**

| Key | Notes |
| :- | :- |
| `permissions` | `allow`, `ask`, `deny`, `additionalDirectories`, `blockReadsOutsideWorkingDirectories`, `defaultMode`, `disableBypassPermissionsMode`, `disableAutoMode` |
| `env` | Env vars for the session and its subprocesses; values override inherited shell values. Project and local files cannot set some vars, e.g. `CLAUDE_CONFIG_DIR` and the OTel exporters |
| `hooks` | Event → `[{matcher, hooks:[{type: command\|prompt\|agent\|http\|mcp_tool}]}]`; merges across files; managed hooks cannot be removed |
| `model`, `availableModels`, `fallbackModel`, `effortLevel`, `modelSettings`, `maxEffortLevel` | Model selection, allowlist, fallback chain, effort |
| `outputStyle` | Active output style |
| `statusLine` | `{type:"command", command, padding?, refreshInterval?, hideVimModeIndicator?}` |
| `attribution` | `{commit, pr, sessionUrl}`, or `false` (v2.1.281+) to hide all attribution. Deprecated since v2.0.62: `includeCoAuthoredBy` |
| `includeGitInstructions` | Drop the built-in commit/PR instructions |
| `enabledPlugins` | `{"name@marketplace": bool}` |
| `extraKnownMarketplaces` | Register marketplaces for a repo or org |
| `sandbox.*` | See the sandboxing section |
| `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers`, `allowedMcpServers`, `deniedMcpServers` | MCP approvals and filters |
| `autoMemoryEnabled`, `autoMemoryDirectory`, `claudeMdExcludes` | Memory |
| `skillOverrides`, `disableBundledSkills`, `skillListingBudgetFraction` | Skills |
| `cleanupPeriodDays` | Transcript retention |
| `language` | Response language |
| `autoUpdatesChannel` | Release channel |
| `disableAllHooks` | Turn off all hooks |
| `worktree.*` | Worktree behavior |

**Managed-only keys (scope "Managed" in [SREF](https://code.claude.com/docs/en/settings-reference))**
- `allowManagedPermissionRulesOnly`, `allowManagedHooksOnly`, `allowManagedMcpServersOnly`
- `strictKnownMarketplaces`, `blockedMarketplaces`, `strictPluginOnlyCustomization`
- `managedMcpServers`, `deniedModels`, `availableModelsMatch`
- `requiredMinimumVersion` and `requiredMaximumVersion`
- `forceRemoteSettingsRefresh`, `policyHelper`, `managedSourcesBehavior`, `disableSideloadFlags`, `allowedProviders`, `claudeMd`

**Managed delivery** (all from [MSET](https://code.claude.com/docs/en/managed-settings))
- File-based: `managed-settings.json`, plus an optional `managed-settings.d/*.json` merged alphabetically, in `/Library/Application Support/ClaudeCode/` (macOS), `/etc/claude-code/` (Linux/WSL), or `C:\Program Files\ClaudeCode\` (Windows). The legacy `C:\ProgramData` path is not read.
- MDM: the macOS domain `com.anthropic.claudecode`, or the Windows `HKLM\SOFTWARE\Policies\ClaudeCode\Settings` value (JSON string). HKCU is the lowest source and is not an admin source.
- Server-managed settings come from the claude.ai admin console or a Claude apps gateway. They are fetched at startup and polled hourly.
- Default `managedSourcesBehavior: "first-wins"` uses only the highest-ranked source that delivers policy. `"merge"` (v2.1.242+) composes all sources.

**Minimal example** (from [SET](https://code.claude.com/docs/en/settings)):
```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": ["Bash(npm run lint)", "Bash(npm run test *)"],
    "deny": ["Read(./.env)", "Read(./.env.*)"]
  }
}
```

**Deprecated or removed keys**
- `includeCoAuthoredBy`: deprecated, replaced by `attribution`
- `disableArtifact`: deprecated, replaced by `enableArtifact`
- `keybindingFlavor`: deprecated, has no effect
- `permissionExplainerEnabled`: removed in v2.1.257
- `taskOutputMaxChars`: removed in v2.1.277
- `teammateDefaultModel`: removed in v2.1.234

Source: [SREF](https://code.claude.com/docs/en/settings-reference)

### Inferences
- Precedence differs between kinds of key. For scalar keys, project settings beat user settings, so a user `false` cannot override a project `true` for, say, `enabledPlugins` (use `settings.local.json` instead). For permission rules, deny beats allow regardless of which scope each came from.
- Because so many keys are restricted to user or managed scope, a team cannot fully enforce behavior from a committed `.claude/settings.json`. Real enforcement needs managed settings.

### Gaps
- I did not enumerate the full per-key text of the ~240-entry settings reference (418KB). Only the index and the key entries above were read. The full list of `env` variables ignored in project and local files was not extracted.
- Server-managed settings platform eligibility details were not read in full.

## Permissions: rule syntax per tool, permission modes, additionalDirectories, managed policy

### Takeaway
Rules are `Tool` or `Tool(specifier)` in `permissions.allow`, `ask`, and `deny`. They are evaluated deny → ask → allow, the first match wins, specificity is irrelevant, and deny in any scope beats allow in any scope. Six modes exist: `default` (labeled Manual), `acceptEdits`, `plan`, `auto`, `dontAsk`, and `bypassPermissions`. As of v2.1.283, `auto` (classifier-reviewed) is the built-in starting mode for interactive terminal and VS Code sessions. Deny rules hold in every mode, and a fixed set of protected paths and "critical paths" is never auto-approved.

### Cited Findings
**Rule evaluation**
- Order is deny, then ask, then allow; the first match decides. A broad deny such as `Bash(aws *)` cannot be carved out by a narrower allow — [PERM](https://code.claude.com/docs/en/permissions)
- A bare tool name in deny (e.g. `Bash`) removes the tool from Claude's context; a scoped deny blocks matching calls. Exception: `EndConversation` cannot be removed — [PERM](https://code.claude.com/docs/en/permissions)
- Deny and ask rules can match one top-level scalar input parameter as `Tool(param:value)`, with `*` wildcards. Examples: `Agent(model:opus)`, `Bash(run_in_background:true)`, `Bash(dangerouslyDisableSandbox:true)`. Primary content fields such as `command`, `file_path`, and `url` are not matchable this way — [PERM](https://code.claude.com/docs/en/permissions)
- Tool-name globs: `"*"` and `"mcp__*"` are accepted in deny and ask. Allow rules accept globs only after a literal `mcp__<server>__` prefix — [PERM](https://code.claude.com/docs/en/permissions)
- Settings files skip any `mcp__` rule that has parentheses; use `--disallowedTools` for MCP parameter rules. Rules must use canonical tool names (see the tools reference), not UI labels — [PERM](https://code.claude.com/docs/en/permissions)

**Bash rules**
- `*` matches any text including spaces. A trailing ` *` also matches the bare command. `:*` is a legacy-equivalent trailing wildcard. Put the `*` after the subcommand (`Bash(git log *)`), not before it — [PERM](https://code.claude.com/docs/en/permissions)
- Compound commands are split on `&&`, `||`, `;`, `|`, `|&`, `&`, and newlines, and each subcommand must match an allow rule. Deny and ask rules match nested commands, including subshells and `$(...)` — [PERM](https://code.claude.com/docs/en/permissions)
- Before matching, these wrappers are stripped: `timeout`, `time`, `nice`, `nohup`, `stdbuf`, `command`, `builtin`, `noglob`, and flagless `xargs`. Known-safe env assignments are also stripped — [PERM](https://code.claude.com/docs/en/permissions)
- A rule is not a security boundary: `Bash(curl *)` does not stop `/usr/bin/curl` or `sh -c 'curl ...'` — [PERM](https://code.claude.com/docs/en/permissions)
- A built-in, non-configurable read-only command set (`ls`, `cat`, `grep`, `find`, `git` read forms, …) runs without a prompt in every mode. Redirect targets (`>`, `<`, `tee`) are checked against Edit and Read rules — [PERM](https://code.claude.com/docs/en/permissions)
- "Yes, and don't ask again" for a compound command saves up to 5 per-subcommand rules — [PERM](https://code.claude.com/docs/en/permissions)

**Read and Edit rules (gitignore syntax)**

| Pattern | Meaning |
| :- | :- |
| `//abs/path` | Absolute filesystem path |
| `~/path` | Home-relative |
| `/path` | Relative to the settings source: the project root for project and local files, `~/.claude/` for the user file, the file's own directory for `--settings` |
| `path` or `./path` | Relative to the cwd |

Source: [PERM](https://code.claude.com/docs/en/permissions)
- Write, NotebookEdit, Glob, and MultiEdit path rules are never consulted (startup warning). Use `Edit(...)` and `Read(...)` instead — [PERM](https://code.claude.com/docs/en/permissions)
- A `Read` deny also blocks Edit and Write on that path. A `.claudeignore` file has no effect; use Read deny rules — [PERM](https://code.claude.com/docs/en/permissions)
- A `!` negation carves out exceptions within the same source. For symlinks, an allow must match both the requested path and its target, while a deny matches either — [PERM](https://code.claude.com/docs/en/permissions)

**Other tool rules**
- WebFetch: `WebFetch(domain:example.com)`, with `*.example.com` and `*`. A bare `WebFetch` allow skips prompts but does not widen the sandbox; `WebFetch(domain:*)` also feeds the sandbox allowlist — [PERM](https://code.claude.com/docs/en/permissions)
- MCP: `mcp__server`, `mcp__server__*`, `mcp__server__tool` — [PERM](https://code.claude.com/docs/en/permissions)
- Subagents: `Agent(Name)`. `/cd` targets: `Cd(path)`. PowerShell rules mirror Bash, with alias canonicalization — [PERM](https://code.claude.com/docs/en/permissions)

**Modes**

| Mode | What runs without asking |
| :- | :- |
| `default` ("Manual"; `manual` alias in v2.1.200+) | Reads only |
| `acceptEdits` | Also file edits and `mkdir`/`touch`/`rm`/`rmdir`/`mv`/`cp`/`sed` inside working dirs |
| `plan` | Read-only exploration, plus classifier-approved commands when auto is available |
| `auto` | Classifier reviews actions |
| `dontAsk` | Anything that would prompt is denied; for CI |
| `bypassPermissions` | Everything except the never-auto-approved set |

Source: [PMODE](https://code.claude.com/docs/en/permission-modes)

**Starting mode and switching**
- Starting mode order: the `--permission-mode` flag, then `permissions.defaultMode`, then the built-in default. As of v2.1.283, the built-in default is `auto` for terminal and VS Code. For `-p` and the SDK it is `default` in sessions that fetch feature flags, otherwise `auto` (v2.1.285+). `disableAutoMode: "disable"` forces `default` — [PMODE](https://code.claude.com/docs/en/permission-modes); [CL](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- Shift+Tab cycles `default` → `acceptEdits` → `plan`, then optional modes: `bypassPermissions` only if enabled at launch, then `auto`. `dontAsk` is never in the cycle — [PMODE](https://code.claude.com/docs/en/permission-modes)
- Auto mode availability: all plans, and on Team/Enterprise unless an admin disables it. Supported models on the Anthropic API are Opus 4.6+, Sonnet 4.6+, and Fable. On Bedrock, Vertex, and Foundry only Sonnet 5+, Opus 4.7+, and Fable are supported. Classifier rules are customized via `autoMode` (`environment`, `allow`, `soft_deny`, `hard_deny`; user or managed scope only) — [PMODE](https://code.claude.com/docs/en/permission-modes); [SREF](https://code.claude.com/docs/en/settings-reference)
- `CLAUDE_CODE_ENABLE_AUTO_MODE` has had no effect since v2.1.207 — [PMODE](https://code.claude.com/docs/en/permission-modes)
- `bypassPermissions` is refused as root or under sudo on Linux and macOS, and refused under `--restricted`. First use shows a dialog that sets `skipDangerousModePermissionPrompt`. Cloud sessions ignore `bypassPermissions` and `dontAsk` from settings files — [PMODE](https://code.claude.com/docs/en/permission-modes)

**Never auto-approved, in any mode**
- Explicit ask rules
- Org-"ask" connector tools
- `AskUserQuestion`, and MCP tools with `_meta["anthropic/requiresUserInteraction"]`
- `rm`/`rmdir` on critical paths
- The cross-session messaging safeguards
- Reads outside working dirs while `blockReadsOutsideWorkingDirectories` is on

Source: [PMODE](https://code.claude.com/docs/en/permission-modes)

**Protected paths** (writes never auto-approved except in bypass): `.git`, `.config/git`, `.vscode`, `.idea`, `.husky`, `.cargo`, `.devcontainer`, `.yarn`, `.mvn`, and `.claude` (except `.claude/worktrees` and the auto memory markdown). Protected files include shell rc files, `.gitconfig`, `.npmrc`, `.mcp.json`, and `.claude.json`. Allow rules do not pre-approve them — [PMODE](https://code.claude.com/docs/en/permission-modes)

**Working directories**
- Extend access with `--add-dir`, `/add-dir`, `permissions.additionalDirectories`, or `/cd` to move — [PERM](https://code.claude.com/docs/en/permissions)
- Directories in `permissions.additionalDirectories` grant file access only. `--add-dir` and `/add-dir` directories also load skills, commands, agents, and the `enabledPlugins`/`extraKnownMarketplaces` keys, plus CLAUDE.md only with the env var — [PERM](https://code.claude.com/docs/en/permissions)

**Hooks, managed policy, and trust**
- PreToolUse hooks run before the prompt. They can deny, force ask, or allow, but they never override deny or ask rules. Exit code 2 blocks the call even when an allow rule matches. Mods (v2.1.287+) answering `tool.check` can override ask rules and non-managed hook blocks — [PERM](https://code.claude.com/docs/en/permissions); [CL](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- Managed policy: no other level can override a managed rule. `allowManagedPermissionRulesOnly` makes managed the only rule source. `disableBypassPermissionsMode: "disable"` works from any scope — [PERM](https://code.claude.com/docs/en/permissions)
- Workspace trust gates project `permissions.allow`, `additionalDirectories`, `extraKnownMarketplaces`, and `.mcp.json` servers. `-p` and SDK runs never show the trust dialog: project allow rules are then not used, but hooks and `env` are. Trust is stored in `~/.claude.json` as `projects["<path>"].hasTrustDialogAccepted` — [PERM](https://code.claude.com/docs/en/permissions)

**CLI and slash commands**
- `/permissions` is the dialog showing rules by source file. Flags: `--allowedTools`, `--disallowedTools`, `--permission-mode`, `--dangerously-skip-permissions`, `--allow-dangerously-skip-permissions`, and `--permission-prompts host|none` — [PERM](https://code.claude.com/docs/en/permissions); local CLI help
- `--restricted` (v2.1.248+) removes code-running tools, ignores user, project, and local settings, and refuses bypass — local CLI help; [PMODE](https://code.claude.com/docs/en/permission-modes)

### Inferences
- Treat Bash allow, ask, and deny rules as UX controls rather than security boundaries. The docs repeatedly point to the sandbox or hooks for real enforcement.
- The v2.1.283 move to `auto` as the default starting mode is a major behavioral change. Older guidance that assumes "default prompts for everything" is out of date.

### Gaps
- I did not extract the full list of what the auto-mode classifier blocks by default, or the critical-path list in detail (the "What the classifier blocks by default" and "Critical paths" sections).

## Sandboxing: filesystem and network sandbox config

### Takeaway
The sandbox is OS-level: Seatbelt on macOS, bubblewrap plus socat on Linux and WSL2, and none on native Windows. It applies only to Bash, PowerShell, and Monitor commands and their children, not to the Read/Edit/WebFetch tools, MCP servers, hooks, or the status line. It is off by default; enable it with `/sandbox` or `sandbox.enabled`. Default writes go to the cwd, added dirs, and a per-user tmp. Default reads cover most of the machine. Network goes through a local proxy with an initially empty domain allowlist. In "auto-allow" mode (`autoAllowBashIfSandboxed: true`, the default), sandboxed commands run without prompts.

### Cited Findings
**Coverage and defaults**
- Built on `@anthropic-ai/sandbox-runtime`. Platforms: macOS (Seatbelt), Linux and WSL2 (bubblewrap + socat), native Windows unsandboxed — [SBX](https://code.claude.com/docs/en/sandboxing)
- Runs outside the sandbox: built-in file and web tools, hooks, local MCP servers, plugin monitors, LSP servers, the status line, `apiKeyHelper`, `!` shell-mode commands (in most sessions), `excludedCommands`, and approved unsandboxed retries — [SBX](https://code.claude.com/docs/en/sandboxing)
- Defaults:

  | Access | Default |
  | :- | :- |
  | Writes | cwd, a per-user temp dir (`$TMPDIR` is set to it), `--add-dir`/`additionalDirectories` |
  | Reads | Whole machine, including `~/.ssh` (use `denyRead` or `credentials`) |
  | Network | No direct route; HTTP/SOCKS proxy checks hostnames against allowed domains (initially empty) |
  | Env | Inherited |

  Source: [SBX](https://code.claude.com/docs/en/sandboxing)
- If the sandbox cannot start, commands run unsandboxed unless `sandbox.failIfUnavailable: true` — [SBX](https://code.claude.com/docs/en/sandboxing); [SREF](https://code.claude.com/docs/en/settings-reference)

**Modes and the retry escape hatch**
- Auto-allow mode (`autoAllowBashIfSandboxed`, default `true`) runs sandboxed commands without prompts. Deny rules, content-scoped ask rules such as `Bash(git push *)`, and critical-path `rm` still apply; a bare `Bash` ask rule is skipped, except in plan mode. Regular-permissions mode (`false`) prompts as usual — [SBX](https://code.claude.com/docs/en/sandboxing)
- Unsandboxed retry: Claude can retry with `dangerouslyDisableSandbox`, and who approves depends on the mode. `allowUnsandboxedCommands: false` ("strict sandbox mode") disables the retry. A `false` from user, `--settings`, or managed settings beats a project `true` (v2.1.285+) — [SBX](https://code.claude.com/docs/en/sandboxing)
- When managed settings or `--settings` disable the retry, the sandbox becomes "admin-required", and repo settings that loosen it are ignored. Since v2.1.281, project settings cannot widen an admin-required sandbox — [SBX](https://code.claude.com/docs/en/sandboxing); [CL](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

**Filesystem keys**
- `sandbox.filesystem.allowWrite`, `denyWrite`, `denyRead`, `allowRead` (re-opens inside a denyRead region; the narrower path wins), and `disabled` (filesystem isolation off, network kept). Arrays merge across scopes — [SBX](https://code.claude.com/docs/en/sandboxing); [SREF](https://code.claude.com/docs/en/settings-reference)
- Sandbox paths use normal conventions (`/abs`, `~/`, relative to the settings file location). Permission rules use `//` and `/` instead — [SBX](https://code.claude.com/docs/en/sandboxing)
- Sandbox-protected paths cannot be exempted by `allowWrite`: `.claude` settings, skills, agents, commands, hooks, `.mcp.json`, shell rc files, `.git/hooks` and `.git/config`, and most of `~/.claude` — [SBX](https://code.claude.com/docs/en/sandboxing)

**Network keys**
- `sandbox.network.allowedDomains`, `deniedDomains`, `allowUnixSockets`, `allowAllUnixSockets`, `allowLocalBinding`, and `allowMachLookup` — [SREF](https://code.claude.com/docs/en/settings-reference)
- `strictAllowlist` (user or managed): deny instead of prompting. `allowManagedDomainsOnly` (managed). `httpProxyPort` and `socksProxyPort` for a custom proxy. `tlsTerminate` is experimental — [SREF](https://code.claude.com/docs/en/settings-reference)
- `WebFetch(domain:...)` allow and deny rules merge into the allowlist. Non-HTTP tools (ssh, DB drivers) and UDP/QUIC/ICMP cannot reach the network. Hostnames resolving only to loopback or link-local addresses are refused — [SBX](https://code.claude.com/docs/en/sandboxing)
- In auto mode, commands carry per-command allowed hosts for the classifier to review — [SBX](https://code.claude.com/docs/en/sandboxing)

**Other keys**
- `excludedCommands` (Bash-rule syntax; every subcommand must match), `credentials.{envVars,files,awsPairs,sigv4,allowPlaintextInject}` (mask or hide secrets), `enableWeakerNestedSandbox`, `enableWeakerNetworkIsolation`, `ignoreViolations`, `allowAppleEvents`, `bwrapPath`, `socatPath`, and `ripgrep` — [SREF](https://code.claude.com/docs/en/settings-reference)
- `/sandbox` opens a panel with Mode, Overrides, and Config tabs, plus a Dependencies tab on Linux. It saves to `.claude/settings.local.json` — [SBX](https://code.claude.com/docs/en/sandboxing)

**Minimal example** (from [SBX](https://code.claude.com/docs/en/sandboxing)):
```json
{
  "sandbox": {
    "enabled": true,
    "filesystem": { "allowWrite": ["~/.kube", "/tmp/build"] },
    "excludedCommands": ["docker compose *"]
  }
}
```

For one session only: `claude --settings '{"sandbox":{"enabled":true,"allowUnsandboxedCommands":false}}'` — [SBX](https://code.claude.com/docs/en/sandboxing)

### Inferences
- With default settings (reads allowed everywhere, retry allowed, auto-allow on), the sandbox mainly reduces prompts and limits writes and network. Protecting secrets requires explicit `denyRead` or `credentials` entries, or `permissions.blockReadsOutsideWorkingDirectories`.

### Gaps
- I did not read the "Protect credentials / Mask credentials" sections or the managed-sandbox lock details in full.

## MCP: .mcp.json, scopes, transports, `claude mcp` commands, tool naming, resources and prompts, tool search, output limits

### Takeaway
There are three user-facing scopes: local (default; stored in `~/.claude.json` under the project), project (`.mcp.json` at the repo root, committed, approval-gated), and user (`~/.claude.json`, all projects). Plugin servers, claude.ai connectors, and managed configuration (`managed-mcp.json` or `managedMcpServers`) add more sources. Transports are stdio, http (`streamable-http`), sse (deprecated), and ws. Tools are named `mcp__<server>__<tool>`. Tool search is on by default, so only tool names and server instructions load upfront. MCP output is capped at 25k tokens by default, with a warning at 10k.

### Cited Findings
**Scopes and precedence**

| Scope | Loads in | Shared | Stored in |
| :- | :- | :- | :- |
| Local (default) | Current project | No | `~/.claude.json` under `projects["<path>"].mcpServers` |
| Project | Current project | Yes, via VCS | `.mcp.json` in project root |
| User | All projects | No | `~/.claude.json` |

Source: [MCP](https://code.claude.com/docs/en/mcp)

- When the same server is defined in several places, precedence is local > project > user > plugin > claude.ai connectors. The whole entry from the winning source is used, with no field merge. Plugins and connectors are deduplicated by endpoint. `managedMcpServers` (managed, v2.1.259+) ranks above all — [MCP](https://code.claude.com/docs/en/mcp)
- Project `.mcp.json` servers need interactive approval, which is reset with `claude mcp reset-project-choices`. In `-p`, SDK, and cloud sessions they load without asking. Settings keys `enableAllProjectMcpServers`, `enabledMcpjsonServers`, and `disabledMcpjsonServers` control approval, but a cloned repo cannot approve its own servers before trust (v2.1.196+) — [MCP](https://code.claude.com/docs/en/mcp)

**Transports and the add command**
- `claude mcp add [--transport http|sse|stdio] [-s local|user|project] [-e KEY=val] [-H "Header: v"] [--client-id] [--client-secret] [--callback-port] <name> <url | -- command args>`. The default transport is stdio and the default scope is local. Everything after `--` is passed to a stdio server — local CLI help; [MCP](https://code.claude.com/docs/en/mcp)
- HTTP is recommended. `type: "streamable-http"` is an alias for `http`. SSE is deprecated, and since v2.1.265 `--transport http` auto-falls back to SSE — [MCP](https://code.claude.com/docs/en/mcp)
- WebSocket (`"type":"ws"`) is available only via JSON (`add-json` or `.mcp.json`), with header auth only and no OAuth — [MCP](https://code.claude.com/docs/en/mcp)
- An entry with a `url` but no `type` is an error (it is read as stdio). `"type":"sdk"` is SDK-host-only — [MCP](https://code.claude.com/docs/en/mcp)

**Other `claude mcp` commands**
- `add-json <name> '<json>'`, `add-from-claude-desktop`, `list`, `get <name>`, `remove`, `login`/`logout` (OAuth), `reset-project-choices`, and `serve` (Claude Code as a stdio MCP server) — local CLI help (`claude mcp --help`)
- In a session: `/mcp`, plus `/mcp reconnect|enable|disable <server|all>` — [CMD](https://code.claude.com/docs/en/commands)

**Server entry fields**
- `command`, `args`, `env` (stdio); `url`, `headers`, `headersHelper` (dynamic auth headers; needs workspace trust for `.mcp.json`), `oauth` (`clientId`, `callbackPort`); `timeout`; `alwaysLoad` — [MCP](https://code.claude.com/docs/en/mcp)
- `${VAR}` and `${VAR:-default}` expansion works in `command`, `args`, `env`, `url`, and `headers`. Credential variables such as `ANTHROPIC_API_KEY` are deliberately expanded as empty in a remote `url` or `headers`. `CLAUDE_PROJECT_DIR` is set in the stdio server's environment — [MCP](https://code.claude.com/docs/en/mcp)
- Reserved server names: `workspace`, `claude-in-chrome`, `computer-use`, `Claude Preview`, `Claude Browser`. `widgets` is reserved in cloud and self-hosted sessions as of v2.1.281 — [MCP](https://code.claude.com/docs/en/mcp); [CL](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- Toggling a server in `/mcp` writes `disabledMcpServers`/`enabledMcpServers` per project in `~/.claude.json` — [MCP](https://code.claude.com/docs/en/mcp)

**Tool naming**
- `mcp__<server>__<tool>`. Plugin servers use `mcp__plugin_<plugin>_<server>__<tool>`, and the server is registered as `plugin:<plugin>:<server>`. claude.ai connectors appear as `mcp__claude_ai_<server>__<tool>` — [MCP](https://code.claude.com/docs/en/mcp); [PERM](https://code.claude.com/docs/en/permissions)

**Resources and prompts**
- Resources are referenced as `@server:protocol://path` in prompts and fetched as attachments. List and read tools are auto-provided — [MCP](https://code.claude.com/docs/en/mcp)
- Prompts appear as `/servername:promptname (MCP)` or `/mcp__server__prompt arg1 arg2` (whitespace-split arguments) — [MCP](https://code.claude.com/docs/en/mcp)

**Tool search and deferred tools**
- On by default. Only tool names and server instructions load at startup, and definitions are fetched through the `ToolSearch` tool — [MCP](https://code.claude.com/docs/en/mcp)
- `ENABLE_TOOL_SEARCH` values:

  | Value | Behavior |
  | :- | :- |
  | unset | Defer all MCP tools (with platform fallbacks) |
  | `true` | Always defer |
  | `auto` | Load upfront below 10% of context, defer above |
  | `auto:N` | Same, with an N% threshold |
  | `false` | Load all upfront |

  Source: [MCP](https://code.claude.com/docs/en/mcp)
- Tool search is disabled automatically when `ANTHROPIC_BASE_URL` points to a non-first-party host, and kept off by `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`. It requires Sonnet/Haiku/Opus 4.5 or later — [MCP](https://code.claude.com/docs/en/mcp)
- Per-server `alwaysLoad: true`, or per-tool `_meta["anthropic/alwaysLoad"]`, exempts tools from deferral. Since v2.1.281, `alwaysLoad: false` defers all of a server's tools — [MCP](https://code.claude.com/docs/en/mcp); [CL](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- Tool descriptions and server instructions are truncated at 2,048 characters (`CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH`, v2.1.280+) — [MCP](https://code.claude.com/docs/en/mcp)

**Output limits and timeouts**
- A warning appears when output exceeds 10,000 tokens. The default maximum is 25,000 tokens (`MAX_MCP_OUTPUT_TOKENS`). Larger results are saved to a file under the session's `tool-results` directory and replaced by a reference — [MCP](https://code.claude.com/docs/en/mcp)
- Servers can raise the threshold per tool with `_meta["anthropic/maxResultSizeChars"]`, up to 500,000 characters — [MCP](https://code.claude.com/docs/en/mcp)
- `MCP_TIMEOUT` sets the startup timeout (default 30000 ms). `MCP_TOOL_TIMEOUT` sets tool execution time (default about 28 h; HTTP requests time out per request at 60 s unless raised) — [ENV](https://code.claude.com/docs/en/env-vars)

**Approval-related server metadata**
- `_meta["anthropic/requiresUserInteraction"]: true` forces a prompt on every call, in every mode — [MCP](https://code.claude.com/docs/en/mcp)
- Elicitation (form and URL modes) is supported and can be auto-answered with the `Elicitation` hook — [MCP](https://code.claude.com/docs/en/mcp)

**Managed MCP**
- `managed-mcp.json` lives in the same system directories as managed settings. It gives exclusive control: users cannot add servers, and plugin and `--mcp-config` servers are blocked. An empty map disables MCP — [MMCP](https://code.claude.com/docs/en/managed-mcp)
- Alternatives: `managedMcpServers` (servers provided alongside the user's own), `allowedMcpServers`/`deniedMcpServers` (entries by `serverUrl` with wildcards, `serverCommand`, or `serverName` — names are not a security control), and `allowManagedMcpServersOnly` — [MMCP](https://code.claude.com/docs/en/managed-mcp)
- claude.ai connectors load only with claude.ai subscription auth. Disable them with `disableClaudeAiConnectors: true` (true from any scope wins) or `ENABLE_CLAUDEAI_MCP_SERVERS=false` — [MCP](https://code.claude.com/docs/en/mcp)

**CLI flags**
- `--mcp-config <files|json>` and `--strict-mcp-config` (use only `--mcp-config` servers) — local CLI help

**Minimal `.mcp.json`** (from [MCP](https://code.claude.com/docs/en/mcp)):
```json
{ "mcpServers": {
    "api-server": { "type": "http", "url": "${API_BASE_URL:-https://api.example.com}/mcp",
                    "headers": { "Authorization": "Bearer ${API_KEY}" } },
    "airtable": { "command": "npx", "args": ["-y", "airtable-mcp-server"], "env": { "AIRTABLE_API_KEY": "${AIRTABLE_API_KEY}" } } } }
```

### Inferences
- "Local scope" for MCP (`~/.claude.json`) is not the same as local settings (`.claude/settings.local.json`); the docs flag this explicitly.
- With tool search on by default, the per-server context cost is mostly the server instructions and tool names. `alwaysLoad` should be reserved for a few hot tools.

### Gaps
- I did not read the OAuth configuration subsections (pre-configured credentials, scope restriction, metadata override) or the v2 runtime notification specifics in detail.

## Plugins and marketplaces: plugin structure, plugin.json, marketplace.json, install and enable commands, scopes, ${CLAUDE_PLUGIN_ROOT}

### Takeaway
A plugin is a directory whose manifest, `.claude-plugin/plugin.json`, is optional; only `name` is required. It can bundle skills, commands, agents, hooks, MCP servers, LSP servers, output styles, workflows, themes, monitors, `bin/` executables, and default settings (`agent`/`subagentStatusLine` only). Components are namespaced `plugin:component`. A marketplace is `.claude-plugin/marketplace.json` (required: `name`, `owner`, `plugins`), and each entry has a `source` (relative path, github, url, git-subdir, npm, archive, or command). Install scope (user, project, local) decides which settings file's `enabledPlugins` records the plugin. Files are cached under `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`, which is what `${CLAUDE_PLUGIN_ROOT}` points to.

### Cited Findings
**plugin.json fields** — all from [PMAN](https://code.claude.com/docs/en/plugins/manifest-reference)
- Metadata:
  - `name` (required; kebab-case; reserved prefixes such as `claude-` and `anthropic-` are rejected by validate)
  - `displayName`, `version` (pins users until changed), `description`, `author{name,email,url}`, `homepage`, `repository`, `license`, `keywords`, `metadata`
  - Directory listing fields Claude Code ignores: `icon`, `documentationUrl`, `supportUrl`, `privacyPolicyUrl`, `termsOfServiceUrl`
  - `defaultEnabled` (default `true`)
- Behavior:
  - `dependencies`: `"name"`, `"name@mkt"`, or `{name, marketplace, version}`
  - `settings`: only `agent` and `subagentStatusLine` take effect
  - `userConfig`: options with type `string`, `number`, `boolean`, `directory`, or `file`; fields `title`, `description`, `required`, `default`, `options`, `multiple`, `sensitive`, `min`/`max`
  - `channels`, `types`
- Component paths:
  - `skills` adds to the default `skills/`
  - `commands`, `agents`, `outputStyles`, and `workflows` replace their default directories
  - `hooks` (path or inline) merges with `hooks/hooks.json`
  - `mcpServers` (path, `.mcpb`/`.dxt` bundle, or inline) merges with `.mcp.json`
  - `lspServers` merges with `.lsp.json`
  - `experimental.{themes,monitors,evals}`

**Standard layout** — from [PMAN](https://code.claude.com/docs/en/plugins/manifest-reference)
- `.claude-plugin/plugin.json`, `skills/<name>/SKILL.md`, `commands/` (legacy; prefer skills), `agents/`, `hooks/hooks.json`, `.mcp.json`, `.lsp.json`, `output-styles/`, `workflows/`, `themes/`, `monitors/monitors.json`, `bin/` (added to the Bash PATH), `settings.json`
- Only the manifest goes in `.claude-plugin/`. A CLAUDE.md at the plugin root is not loaded; put instructions in a skill.

**Validation**
- Unknown top-level keys are stripped with a warning. Unknown keys inside `userConfig`, `channels`, `lspServers`, or `monitors` are errors that stop the plugin loading — [PMAN](https://code.claude.com/docs/en/plugins/manifest-reference)
- `claude plugin validate [--strict]` is the authoritative check; since v2.1.281 it also checks MCP entries — [PMAN](https://code.claude.com/docs/en/plugins/manifest-reference)

**Path variables**

| Variable | Resolves to |
| :- | :- |
| `${CLAUDE_PLUGIN_ROOT}` | The installed version directory; changes on every update, so don't write state there |
| `${CLAUDE_PLUGIN_DATA}` | `~/.claude/plugins/data/<id>/`; persists across updates and is deleted on last uninstall unless `--keep-data` |
| `${CLAUDE_PROJECT_DIR}` | The project root |

Source: [PMAN](https://code.claude.com/docs/en/plugins/manifest-reference)
- The variables resolve inline in hook `command`/`args`, MCP `command`/`args`/`env`/`url`/`headers`, LSP fields, and skill, agent, and command Markdown bodies. They are not present in Bash tool commands. Hooks also get `CLAUDE_PLUGIN_OPTION_<KEY>` for `userConfig` values — [PMAN](https://code.claude.com/docs/en/plugins/manifest-reference)

**marketplace.json** — from [PMKT](https://code.claude.com/docs/en/plugins/marketplace-reference)
- Lives at `<root>/.claude-plugin/marketplace.json`; relative plugin sources resolve from the marketplace root.
- Top-level fields: `name` (required; many official names are reserved, and `claudeai-*` is reserved), `owner{name,email?,url?}` (required), `plugins` (required), `description`, `version`, `metadata.pluginRoot` (v2.1.239+), `forceRemoveDeletedPlugins`, `allowCrossMarketplaceDependenciesOn`, `renames`.
- Plugin entry fields: `name` and `source` (required), `description`, `version` (`plugin.json` wins), `category`, `tags`, `strict` (default `true`), `relevance`, `dependencies`, `defaultEnabled`, `displayName`, `metadata`, `headers`, `headersHelper`. An entry can also carry any `plugin.json` field.
- `strict` behavior: `true` (default) means `plugin.json` is authoritative and the entry's components are appended. `false` with component fields in both places is a "conflicting manifests" error. When there is no `plugin.json`, the entry is the manifest.

**Plugin source types** — from [PMKT](https://code.claude.com/docs/en/plugins/marketplace-reference)

| Type | Fields |
| :- | :- |
| Relative path | `"./..."` |
| `github` | `repo`, `ref`, `sha` |
| `url` (git) | `url`, `ref`, `sha` |
| `git-subdir` | `url`, `path`, `ref`, `sha` |
| `npm` | `package`, `version`, `registry` |
| `archive` (v2.1.224+) | `url`, `sha256` |
| `command` (v2.1.229+) | `command`, `timeout`, `mode` |

- Marketplace source types (in `extraKnownMarketplaces` and the policy lists): `github{repo,ref,path,sparsePaths}`, `git{url,...}`, `url` (a direct `marketplace.json` link, `headers`), `file`, `directory`, and `settings` (an inline catalog). `hostPattern` and `pathPattern` are valid only in `strictKnownMarketplaces`/`blockedMarketplaces` — [PMKT](https://code.claude.com/docs/en/plugins/marketplace-reference)

**Install scopes**
- User (default for the CLI) writes `enabledPlugins` in `~/.claude/settings.json`. Project writes `.claude/settings.json`, which enables the plugin for collaborators, but each still has to install it. Local writes `.claude/settings.local.json` — [PINST](https://code.claude.com/docs/en/plugins/install)
- Precedence is local > project > user. A managed `enabledPlugins: false` blocks installation at every scope — [PINST](https://code.claude.com/docs/en/plugins/install); [SREF](https://code.claude.com/docs/en/settings-reference)

**Commands**
- Shell — local CLI help; [PCLI](https://code.claude.com/docs/en/plugins/cli-reference):
  - `claude plugin install|i <plugin[@mkt]> [-s user|project|local] [--config k=v] [-y] [--json]`
  - `uninstall [--keep-data]`, `enable`, `disable`, `update` (restart or `/reload-plugins` to apply), `list [--json]`
  - `details` (component inventory and projected token cost), `configure`, `prune`, `validate`, `tag`, `init|new`
  - `eval` (plugin eval suites), `test` (mods)
  - `claude plugin marketplace add <source> [--scope] [--sparse] [--claudeai]`, plus `list`, `remove|rm`, `update [name]`
- In session: `/plugin` (Discover, Installed, Marketplaces, and Errors tabs, plus subcommands), `/plugin marketplace add owner/repo[#ref]`, `/plugin install name --marketplace <source>` (v2.1.275+), and `/reload-plugins [--force]` — [PCLI](https://code.claude.com/docs/en/plugins/cli-reference); [PINST](https://code.claude.com/docs/en/plugins/install)
- Session-only loading: `--plugin-dir <dir|zip>` (repeatable), `--plugin-url <zip-url>`, and `CLAUDE_CODE_PLUGIN_DIRS`. These appear as `<name>@inline` and shadow installed plugins of the same name. The managed `disableSideloadFlags` setting blocks them — [PCLI](https://code.claude.com/docs/en/plugins/cli-reference); [PLOAD](https://code.claude.com/docs/en/plugins/loading)

**On disk and naming**
- Plugin root: `~/.claude/plugins` (override with `CLAUDE_CODE_PLUGIN_CACHE_DIR`), containing `cache/<mkt>/<plugin>/<version>/`, `data/<id>/`, `marketplaces/<name>/`, `synced/`, `installed_plugins.json`, and `known_marketplaces.json` — [PLOAD](https://code.claude.com/docs/en/plugins/loading)
- Version resolution order: manifest `version` > entry `version` > source-derived (12-character commit SHA, sha256, or `unknown`). Pinning `version` freezes users until it changes — [PLOAD](https://code.claude.com/docs/en/plugins/loading)
- Name-conflict order: managed-locked > `--plugin-dir`/`--plugin-url` > installed marketplace > skills-dir (`~/.claude/skills/` beats project `.claude/skills/`) > synced from claude.ai — [PLOAD](https://code.claude.com/docs/en/plugins/loading)
- Special marketplace names: `inline`, `builtin`, `skills-dir`, `synced`. `claude plugin init <name>` scaffolds at `~/.claude/skills/<name>/`, which auto-loads as `<name>@skills-dir` — [PMKT](https://code.claude.com/docs/en/plugins/marketplace-reference); local CLI help

**Updates and governance**
- Auto-update is on by default only for official marketplaces and claude.ai-added ones; everything else is off. Toggle it per marketplace in the `/plugin` Marketplaces tab. `FORCE_AUTOUPDATE_PLUGINS=1` forces updates even with `DISABLE_AUTOUPDATER` — [PINST](https://code.claude.com/docs/en/plugins/install); [ENV](https://code.claude.com/docs/en/env-vars)
- Team and org settings: `extraKnownMarketplaces` (repo or org registration; needs trust), and the managed `strictKnownMarketplaces` (allowlist), `blockedMarketplaces`, `strictPluginOnlyCustomization`, `pluginTrustMessage`, and `disableCommandPluginSources` — [SREF](https://code.claude.com/docs/en/settings-reference)

**Recent changes**
- v2.1.287 added "Claude Mods": plugins with function hooks that can draw UI and answer `tool.check`; see the `plugins/mods/*` docs. `claude plugin configure` and `install --config` arrived around v2.1.281–2.1.282 — [CL](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md); [PERM](https://code.claude.com/docs/en/permissions)
- The old doc URLs `/docs/en/plugins`, `/plugins-reference`, `/plugin-marketplaces`, and `/discover-plugins` now serve the new `/docs/en/plugins/*` pages — observed by fetching both on 2026-10-04 ([POV](https://code.claude.com/docs/en/plugins/overview))

**Minimal plugin** (from [PMAN](https://code.claude.com/docs/en/plugins/manifest-reference)):
```
my-plugin/.claude-plugin/plugin.json   -> {"name":"my-plugin","version":"0.1.0","description":"..."}
my-plugin/skills/hello/SKILL.md
```

**Minimal marketplace** (shape from [PMKT](https://code.claude.com/docs/en/plugins/marketplace-reference)):
```json
{"name":"team-tools","owner":{"name":"Team"},"plugins":[{"name":"my-plugin","source":"./plugins/my-plugin"}]}
```
Add it with `claude plugin marketplace add ./path` or `owner/repo`, then run `claude plugin install my-plugin@team-tools --scope project`.

### Inferences
- Setting `version` in plugin.json makes updates explicit: users only update when the string changes. Omitting it lets users track commits. This matters for how a team marketplace should publish.
- A project-scope `enabledPlugins` entry plus `extraKnownMarketplaces` in a committed `.claude/settings.json` is the documented way to "recommend" plugins to a team. It still requires each member to trust the folder and install the plugin.

### Gaps
- I did not read the plugin `components` page, the dependencies page, the mods reference, or the org-management page in detail. The `userConfig` storage location (`pluginConfigs`) was confirmed only from the settings index.

## Output styles, model selection and aliases, status line, environment variables

### Takeaway
- **Output styles** are Markdown files with frontmatter (`name`, `description`, `keep-coding-instructions`, `force-for-plugin`) in `~/.claude/output-styles`, `.claude/output-styles`, managed dirs, or plugins. They are selected with `/output-style` or `outputStyle`. The built-ins are Default, Proactive, Concise, Explanatory, and Learning.
- **Models**: the aliases are `default`, `best`, `fable`, `opus`, `sonnet`, `haiku`, `sonnet[1m]`, `opus[1m]`, and `opusplan`. On the Anthropic API, `opus` resolves to Opus 5.5 and `sonnet` to Sonnet 5.5. The model is chosen by `/model` > `--model` > `ANTHROPIC_MODEL` > the `model` setting > `ANTHROPIC_DEFAULT_MODEL`.
- **Status line** is a `statusLine` command that receives session JSON on stdin.
- **Environment variables** mostly override per pair, and the settings `env` block sets them for sessions.

### Cited Findings
**Output styles** — all from [OST](https://code.claude.com/docs/en/output-styles)
- Built-ins:

  | Style | What it does |
  | :- | :- |
  | Default | No style instructions |
  | Proactive | Starts work without asking routine questions; does not change the permission mode |
  | Concise | Shorter responses; v2.1.237+ |
  | Explanatory | Adds `★ Insight` blocks |
  | Learning | Insight blocks plus `TODO(human)` handoffs |

- Selection: `/output-style <name>` (v2.1.269+; with no argument it lists styles), `/config` → Output style (saves to `.claude/settings.local.json`), or `"outputStyle": "Explanatory"` in any settings file. The value is case-sensitive; a mismatch falls back to Default. Since v2.1.251, a switch applies from the next message.
- Custom style locations: `~/.claude/output-styles`, every `.claude/output-styles` between the cwd and the repo root (closest wins), `.claude/output-styles` in the managed settings directory, and a plugin's `output-styles/`. Style files are read at startup, so restart after editing.
- Frontmatter: `name`, `description`, `keep-coding-instructions` (default `false`, which drops the built-in software-engineering instructions), and `force-for-plugin` (plugin-only; overrides the user's `outputStyle`).
- Cost and reach: style instructions are sent with every request, prompt-cached. Styles apply to the main thread and forks, not to other subagents.

**Models** — all from [MODEL](https://code.claude.com/docs/en/model-config)
- Aliases:

  | Alias | Behavior |
  | :- | :- |
  | `default` | Clears overrides → account default (Opus 5.5 on Pro/Max/Team/Enterprise/API/Bedrock/Vertex; Sonnet 4.5 on Foundry) |
  | `best` | `fable` if available, else `opus` |
  | `fable` | Fable 5.1 |
  | `opus` | Anthropic API: Opus 5.5 |
  | `sonnet` | Anthropic API: Sonnet 5.5; Bedrock/Vertex: Sonnet 4.5 |
  | `haiku` | Haiku |
  | `sonnet[1m]`, `opus[1m]` | 1M context window variants |
  | `opusplan` | Opus in plan mode, Sonnet for execution |

- Version requirements: Sonnet 5.5 needs v2.1.284+, Opus 5.5 needs v2.1.280+, Fable 5.1 needs v2.1.257+.
- Precedence: `/model` (saves to user settings `model`; press `s` for session-only) > `--model` > `ANTHROPIC_MODEL` > `model` key > `ANTHROPIC_DEFAULT_MODEL` (v2.1.236+). Project or managed `model` reapplies at each launch.
- Pinning variables: `ANTHROPIC_DEFAULT_{FABLE,OPUS,SONNET,HAIKU}_MODEL` and `CLAUDE_CODE_SUBAGENT_MODEL`. `ANTHROPIC_SMALL_FAST_MODEL` is deprecated in favor of `ANTHROPIC_DEFAULT_HAIKU_MODEL`.
- Organization controls: `availableModels`, `deniedModels`, `enforceAvailableModels`, `modelOverrides`, and `modelPicker`.
- Fallback: `fallbackModel` (array, max 3) or `--fallback-model a,b`; applies per turn.
- Effort levels are `low`, `medium`, `high`, `xhigh`, and `max`. Opus 5.5 and Sonnet 5.5 default to `medium`, other models to `high`.
  - Precedence: `CLAUDE_CODE_EFFORT_LEVEL` > `--effort` or `/effort` > `modelSettings`/`effortLevel` > model default. `maxEffortLevel` caps it.
  - `ultracode` is a separate toggle, not an effort level. `ultrathink` in a prompt requests deeper reasoning for one turn.

**Status line** — all from [SL](https://code.claude.com/docs/en/statusline)
- Settings shape: `"statusLine": {"type":"command","command":"~/.claude/statusline.sh","padding":2,"refreshInterval":5,"hideVimModeIndicator":true}`. `/statusline <description>` generates a script and the settings entry.
- The script receives JSON on stdin and prints lines to stdout (ANSI colors and OSC 8 links are supported). It runs on new assistant messages, `/compact`, mode changes, and so on, debounced at 300 ms. It uses no API tokens and runs outside the sandbox.
- JSON fields include:
  - `model.{id,display_name}`, `workspace.{current_dir,project_dir,added_dirs,git_worktree,repo.*}`, `session_id`, `session_name`, `transcript_path`, `version`
  - `cost.{total_cost_usd,total_duration_ms,total_lines_added,...}`
  - `context_window.{used_percentage,context_window_size,...}`, `effort.level`, `thinking.enabled`, `fast_mode`
  - `rate_limits.{five_hour,seven_day,spend_limit}.*`, `prompt_cache`
  - `output_style.name`, `vim.mode`, `agent.name`, `pr.*`, `worktree.*`
- `disableAllHooks` and `allowManagedHooksOnly` also suppress non-managed status lines — [SREF](https://code.claude.com/docs/en/settings-reference)

**Environment variables that matter for configuration** — all from [ENV](https://code.claude.com/docs/en/env-vars) unless noted

| Variable | Effect |
| :- | :- |
| `CLAUDE_CONFIG_DIR` | Relocate `~/.claude`; cannot be set from project or local `env` |
| `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_MODEL` | Model selection |
| `CLAUDE_CODE_EFFORT_LEVEL` | Effort; beats `--effort` |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY`, `CLAUDE_CODE_DISABLE_CLAUDE_MDS`, `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`, `CLAUDE_CODE_NEW_INIT` | Memory and instructions |
| `MAX_MCP_OUTPUT_TOKENS`, `MCP_TIMEOUT`, `MCP_TOOL_TIMEOUT`, `ENABLE_TOOL_SEARCH`, `CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH`, `ENABLE_CLAUDEAI_MCP_SERVERS`, `MCP_DISCOVERY_CACHE` | MCP |
| `CLAUDE_CODE_PLUGIN_CACHE_DIR`, `CLAUDE_CODE_PLUGIN_DIRS`, `FORCE_AUTOUPDATE_PLUGINS` | Plugins |
| `CLAUDE_CODE_SIMPLE` (`--bare`), `CLAUDE_CODE_SAFE_MODE` (`--safe-mode`) | Minimal or troubleshooting modes |
| `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` | Strip credentials from subprocesses |
| `BASH_MAX_OUTPUT_LENGTH` | Default 30000 chars; superseded by the `bashOutputMaxChars` setting |
| `DISABLE_AUTOUPDATER`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | Updates and network traffic |

- How `env` and shell values interact: an `env` block value in settings replaces the inherited shell value in most sessions. A settings file cannot unset a variable, but can set it to `""`. `--model` and `/model` beat `ANTHROPIC_MODEL`, while `CLAUDE_CODE_EFFORT_LEVEL` beats `--effort` and `/effort` — [ENV](https://code.claude.com/docs/en/env-vars)

**Minimal style file** (from [OST](https://code.claude.com/docs/en/output-styles)): `~/.claude/output-styles/diagrams.md` containing

```
---
keep-coding-instructions: true
---
When explaining code, start with a Mermaid diagram...
```

### Inferences
- Model aliases differ by provider (Bedrock and Vertex `sonnet` = Sonnet 4.5). Docs and configs written for the Anthropic API may silently select older models on third-party providers unless `ANTHROPIC_DEFAULT_*_MODEL` pins them.
- An output style replaces the coding instructions unless `keep-coding-instructions: true` is set. It is therefore a heavier lever than CLAUDE.md, suited to role changes rather than project conventions.

### Gaps
- I did not extract the full ~390-row environment variable table, nor the "first session after an install or upgrade" and feature-flag-fetching behaviors in detail.
- The `keybindings.json`, `theme`, and terminal-config mechanisms were not covered; they are arguably UI rather than foundation.
