# Configuration

Claude Code reads its configuration from JSON settings files at four scopes (managed, user, shared project, local project) plus command-line overrides. The settings control permissions, hooks, models, plugins, MCP approvals, memory, the status line, output styles, and environment variables for the session. This page also covers workspace trust, model aliases and effort, output styles, the status line, and configuration-related environment variables. About 240 keys are documented in the settings reference, many of them scope-restricted ([settings](https://code.claude.com/docs/en/settings); [settings reference](https://code.claude.com/docs/en/settings-reference)).

## Locations and scopes

### Settings files

| Scope | File | Who it affects |
| :- | :- | :- |
| User | `~/.claude/settings.json` | You, in all projects |
| Shared project | `.claude/settings.json` | Committed; affects the whole team |
| Project local | `.claude/settings.local.json` | You, in this project |
| Managed | `managed-settings.json`, MDM, or server-managed | Your organization |

Source: [settings](https://code.claude.com/docs/en/settings)

- `~/.claude.json` is a separate file that Claude Code writes itself. It holds auth, MCP server configs (local and user scope), per-project state such as trust decisions, and the "Global config" keys ([settings](https://code.claude.com/docs/en/settings)).
- `CLAUDE_CONFIG_DIR` relocates `~/.claude` ([settings](https://code.claude.com/docs/en/settings); [env vars](https://code.claude.com/docs/en/env-vars)).
- Since v2.1.211, `.claude/settings.local.json` is read and written at the git repo root, or the main checkout root for a worktree. It is auto-added to global git excludes as `**/.claude/settings.local.json` the first time Claude Code writes it ([settings](https://code.claude.com/docs/en/settings)).
- The shared `.claude/settings.json` is read from the session's primary working directory, with no parent fallback. `/cd` re-reads project settings from the new directory (v2.1.246+) ([settings](https://code.claude.com/docs/en/settings); [permissions](https://code.claude.com/docs/en/permissions)).

### Managed delivery

All from [managed settings](https://code.claude.com/docs/en/managed-settings):

- File-based: `managed-settings.json`, plus an optional `managed-settings.d/*.json` merged alphabetically, in `/Library/Application Support/ClaudeCode/` (macOS), `/etc/claude-code/` (Linux/WSL), or `C:\Program Files\ClaudeCode\` (Windows). The legacy `C:\ProgramData` path is not read.
- MDM: the macOS domain `com.anthropic.claudecode`, or the Windows `HKLM\SOFTWARE\Policies\ClaudeCode\Settings` value (a JSON string). HKCU is the lowest source and is not an admin source.
- Server-managed: from the claude.ai admin console or a Claude apps gateway. Fetched at startup and polled hourly.
- `managedSourcesBehavior`: default `"first-wins"` uses only the highest-ranked source that delivers policy. `"merge"` (v2.1.242+) composes all sources.

### Precedence

Highest first ([settings](https://code.claude.com/docs/en/settings)):

1. Managed (server, MDM, or file)
2. Command line: `--settings <file-or-json>` (merges by the same rules) and flags
3. `.claude/settings.local.json`
4. `.claude/settings.json`
5. `~/.claude/settings.json`

Merge rules ([settings](https://code.claude.com/docs/en/settings)):

- Scalar keys override. List keys, such as `permissions.allow`, merge across files.
- List exceptions: `fallbackModel` — the highest file wins whole; `modelPicker` — the highest of managed, `--settings`, or user wins whole, and it is ignored in project and local files; `availableModels` — a managed list is applied as-is; `modelSettings` — resolved per model.
- Exceptions to managed precedence, where the stricter value from a lower scope wins: `disableClaudeAiConnectors: true`, `enableArtifact: false`, `isolatePeerMachines: true`, `remoteControlAtStartup: false` (project or local), `crossSessionInbound` when stricter, `useAutoModeDuringPlan: false`, `syncClaudeAiSkills: false`, `syncClaudeAiPlugins: false`, and `maxEffortLevel` (the lowest cap wins).
- Environment variables are not a level in this stack. Precedence between a variable and its paired key is decided per pair. For example, `ANTHROPIC_MODEL` beats the `model` key, while `ANTHROPIC_DEFAULT_MODEL` applies only when no file sets `model`.

### Keys a repository cannot set

- Keys whose scope is "User, local, or managed", "User or managed", "Managed", or "Global config" never take effect from the shared project file ([settings](https://code.claude.com/docs/en/settings)).
- `permissions.defaultMode` values `auto` and `bypassPermissions` do not take effect from project or local files. Before v2.1.257, `bypassPermissions` took effect from any file ([settings](https://code.claude.com/docs/en/settings)).

### Workspace trust

- These wait for workspace trust: `permissions.allow`, `permissions.additionalDirectories`, `extraKnownMarketplaces`, and most `env` values. `deny` and `ask` rules apply immediately ([settings](https://code.claude.com/docs/en/settings)).
- Trust also gates `.mcp.json` servers ([permissions](https://code.claude.com/docs/en/permissions)) and settings-file hooks in interactive sessions ([hooks](https://code.claude.com/docs/en/hooks)).
- `-p` and SDK runs never show the trust dialog. Project allow rules are then not used, but hooks and `env` are ([permissions](https://code.claude.com/docs/en/permissions)).
- Trust is stored in `~/.claude.json` as `projects["<path>"].hasTrustDialogAccepted` ([permissions](https://code.claude.com/docs/en/permissions)).
- The allow rules in `.claude/settings.local.json` skip workspace trust while the file is untracked ([settings](https://code.claude.com/docs/en/settings)).

### Output style locations

- `~/.claude/output-styles`; every `.claude/output-styles` between the cwd and the repo root (closest wins); `.claude/output-styles` in the managed settings directory; a plugin's `output-styles/` ([output styles](https://code.claude.com/docs/en/output-styles)).

## Format

- Strict JSON: no comments, no trailing commas. Add `"$schema": "https://json.schemastore.org/claude-code-settings.json"` for editor validation; the schema can lag the CLI ([settings](https://code.claude.com/docs/en/settings)).

### Important keys

From the [settings reference](https://code.claude.com/docs/en/settings-reference):

| Key | Notes |
| :- | :- |
| `permissions` | `allow`, `ask`, `deny`, `additionalDirectories`, `blockReadsOutsideWorkingDirectories`, `defaultMode`, `disableBypassPermissionsMode`, `disableAutoMode`. See [permissions-and-sandbox.md](permissions-and-sandbox.md) |
| `env` | Env vars for the session and its subprocesses; values override inherited shell values. Project and local files cannot set some vars, e.g. `CLAUDE_CONFIG_DIR` and the OTel exporters |
| `hooks` | Event → `[{matcher, hooks:[{type: command\|prompt\|agent\|http\|mcp_tool}]}]`; merges across files; managed hooks cannot be removed. See [hooks.md](hooks.md) |
| `model`, `availableModels`, `fallbackModel`, `effortLevel`, `modelSettings`, `maxEffortLevel` | Model selection, allowlist, fallback chain, effort |
| `outputStyle` | Active output style |
| `statusLine` | `{type:"command", command, padding?, refreshInterval?, hideVimModeIndicator?}` |
| `attribution` | `{commit, pr, sessionUrl}`, or `false` (v2.1.281+) to hide all attribution. Replaces deprecated `includeCoAuthoredBy` (since v2.0.62) |
| `includeGitInstructions` | Drop the built-in commit/PR instructions |
| `enabledPlugins` | `{"name@marketplace": bool}`. See [plugins.md](plugins.md) |
| `extraKnownMarketplaces` | Register marketplaces for a repo or org |
| `sandbox.*` | See [permissions-and-sandbox.md](permissions-and-sandbox.md) |
| `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers`, `allowedMcpServers`, `deniedMcpServers` | MCP approvals and filters. See [mcp.md](mcp.md) |
| `autoMemoryEnabled`, `autoMemoryDirectory`, `claudeMdExcludes` | Memory. See [instructions.md](instructions.md) |
| `skillOverrides`, `disableBundledSkills`, `skillListingBudgetFraction` | Skills. See [skills.md](skills.md) |
| `cleanupPeriodDays` | Transcript retention |
| `language` | Response language |
| `autoUpdatesChannel` | Release channel |
| `disableAllHooks` | Turn off all hooks |
| `worktree.*` | Worktree behavior |
| `agent` | Run the main session as a named subagent ([subagents](https://code.claude.com/docs/en/sub-agents)) |

### Managed-only keys

Scope "Managed" in the [settings reference](https://code.claude.com/docs/en/settings-reference):

- `allowManagedPermissionRulesOnly`, `allowManagedHooksOnly`, `allowManagedMcpServersOnly`
- `strictKnownMarketplaces`, `blockedMarketplaces`, `strictPluginOnlyCustomization`
- `managedMcpServers`, `deniedModels`, `availableModelsMatch`
- `requiredMinimumVersion`, `requiredMaximumVersion`
- `forceRemoteSettingsRefresh`, `policyHelper`, `managedSourcesBehavior`, `disableSideloadFlags`, `allowedProviders`, `claudeMd`

### Models and aliases

All from [model config](https://code.claude.com/docs/en/model-config):

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
- Model precedence: `/model` (saves to user settings `model`; press `s` for session-only) > `--model` > `ANTHROPIC_MODEL` > `model` key > `ANTHROPIC_DEFAULT_MODEL` (v2.1.236+). A project or managed `model` reapplies at each launch.
- Pinning variables: `ANTHROPIC_DEFAULT_{FABLE,OPUS,SONNET,HAIKU}_MODEL` and `CLAUDE_CODE_SUBAGENT_MODEL`. `ANTHROPIC_SMALL_FAST_MODEL` is deprecated in favor of `ANTHROPIC_DEFAULT_HAIKU_MODEL`.
- Organization controls: `availableModels`, `deniedModels`, `enforceAvailableModels`, `modelOverrides`, `modelPicker`.
- Fallback: `fallbackModel` (array, max 3) or `--fallback-model a,b`; applies per turn.

### Effort

From [model config](https://code.claude.com/docs/en/model-config):

- Levels: `low`, `medium`, `high`, `xhigh`, `max`. Opus 5.5 and Sonnet 5.5 default to `medium`; other models default to `high`.
- Precedence: `CLAUDE_CODE_EFFORT_LEVEL` > `--effort` or `/effort` > `modelSettings`/`effortLevel` > model default. `maxEffortLevel` caps it (the lowest cap from any scope wins).
- `ultracode` is a separate toggle, not an effort level (see [automation.md](automation.md#dynamic-workflows)). `ultrathink` in a prompt requests deeper reasoning for one turn.

### Output styles

From [output styles](https://code.claude.com/docs/en/output-styles):

| Built-in style | What it does |
| :- | :- |
| Default | No style instructions |
| Proactive | Starts work without asking routine questions; does not change the permission mode |
| Concise | Shorter responses; v2.1.237+ |
| Explanatory | Adds `★ Insight` blocks |
| Learning | Insight blocks plus `TODO(human)` handoffs |

Custom style file: Markdown with frontmatter.

| Field | Meaning | Default |
| :- | :- | :- |
| `name` | Style name | — |
| `description` | Description | — |
| `keep-coding-instructions` | Keep the built-in software-engineering instructions | `false` (they are dropped) |
| `force-for-plugin` | Plugin-only; overrides the user's `outputStyle` | — |

### Status line

From [status line](https://code.claude.com/docs/en/statusline):

- Settings shape: `"statusLine": {"type":"command","command":"~/.claude/statusline.sh","padding":2,"refreshInterval":5,"hideVimModeIndicator":true}`.
- The script receives JSON on stdin and prints lines to stdout. ANSI colors and OSC 8 links are supported.
- JSON fields include: `model.{id,display_name}`, `workspace.{current_dir,project_dir,added_dirs,git_worktree,repo.*}`, `session_id`, `session_name`, `transcript_path`, `version`; `cost.{total_cost_usd,total_duration_ms,total_lines_added,...}`; `context_window.{used_percentage,context_window_size,...}`, `effort.level`, `thinking.enabled`, `fast_mode`; `rate_limits.{five_hour,seven_day,spend_limit}.*`, `prompt_cache`; `output_style.name`, `vim.mode`, `agent.name`, `pr.*`, `worktree.*`.

### Environment variables

From [env vars](https://code.claude.com/docs/en/env-vars) unless noted:

| Variable | Effect |
| :- | :- |
| `CLAUDE_CONFIG_DIR` | Relocate `~/.claude`; cannot be set from project or local `env` |
| `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_MODEL` | Model selection |
| `CLAUDE_CODE_EFFORT_LEVEL` | Effort; beats `--effort` and `/effort` |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY`, `CLAUDE_CODE_DISABLE_CLAUDE_MDS`, `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`, `CLAUDE_CODE_NEW_INIT` | Memory and instructions ([instructions.md](instructions.md)) |
| `MAX_MCP_OUTPUT_TOKENS`, `MCP_TIMEOUT`, `MCP_TOOL_TIMEOUT`, `ENABLE_TOOL_SEARCH`, `CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH`, `ENABLE_CLAUDEAI_MCP_SERVERS`, `MCP_DISCOVERY_CACHE` | MCP ([mcp.md](mcp.md)) |
| `CLAUDE_CODE_PLUGIN_CACHE_DIR`, `CLAUDE_CODE_PLUGIN_DIRS`, `FORCE_AUTOUPDATE_PLUGINS` | Plugins ([plugins.md](plugins.md)) |
| `CLAUDE_CODE_SIMPLE` (`--bare`), `CLAUDE_CODE_SAFE_MODE` (`--safe-mode`) | Minimal or troubleshooting modes |
| `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` | Strip credentials from subprocesses |
| `BASH_MAX_OUTPUT_LENGTH` | Default 30000 chars; superseded by the `bashOutputMaxChars` setting |
| `DISABLE_AUTOUPDATER`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | Updates and network traffic |

- An `env` block value in settings replaces the inherited shell value in most sessions. A settings file cannot unset a variable, but can set it to `""` ([env vars](https://code.claude.com/docs/en/env-vars)).
- `--model` and `/model` beat `ANTHROPIC_MODEL`, while `CLAUDE_CODE_EFFORT_LEVEL` beats `--effort` and `/effort` ([env vars](https://code.claude.com/docs/en/env-vars)).

## Loading and invocation

- Settings files are watched and hot-reloaded, including `permissions`, `hooks`, and `apiKeyHelper`. A `ConfigChange` hook fires on each change ([settings](https://code.claude.com/docs/en/settings)).
- Startup-only keys include `model`, `effortLevel`, and `modelSettings`. Use `/model` and `/effort` mid-session instead ([settings](https://code.claude.com/docs/en/settings)).
- Broken files: invalid JSON or a schema-rejected value causes a "Settings Error" dialog; bad individual entries cause a "Settings Warning" and are skipped. With `-p`, broken files or entries are silently skipped; `claude doctor` lists rejected entries ([settings](https://code.claude.com/docs/en/settings); local CLI help).
- `/status` shows a "Setting sources" line listing which files loaded. `/config` edits a subset of keys and accepts `/config key=value` ([settings](https://code.claude.com/docs/en/settings)).
- Output styles: selected with `/output-style <name>` (v2.1.269+; with no argument it lists styles), `/config` → Output style (saves to `.claude/settings.local.json`), or `"outputStyle": "Explanatory"` in any settings file. Since v2.1.251, a switch applies from the next message. Style files are read at startup, so restart after editing. Style instructions are sent with every request, prompt-cached. Styles apply to the main thread and forks, not to other subagents ([output styles](https://code.claude.com/docs/en/output-styles)).
- Status line: `/statusline <description>` generates a script and the settings entry. The command runs on new assistant messages, `/compact`, mode changes, and similar events, debounced at 300 ms. It uses no API tokens and runs outside the sandbox ([status line](https://code.claude.com/docs/en/statusline)).

## Example

Minimal `.claude/settings.json` ([settings](https://code.claude.com/docs/en/settings)):

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": ["Bash(npm run lint)", "Bash(npm run test *)"],
    "deny": ["Read(./.env)", "Read(./.env.*)"]
  }
}
```

Minimal output style `~/.claude/output-styles/diagrams.md` ([output styles](https://code.claude.com/docs/en/output-styles)):

```markdown
---
keep-coding-instructions: true
---
When explaining code, start with a Mermaid diagram...
```

## Limits and gotchas

- Precedence differs by key kind. Inference (from the research notes): for scalar keys, project settings beat user settings, so a user `false` cannot override a project `true` for a key like `enabledPlugins` (use `settings.local.json` instead). For permission rules, deny beats allow regardless of which scope each came from.
- Inference (from the research notes): because many keys are restricted to user or managed scope, a team cannot fully enforce behavior from a committed `.claude/settings.json`. Enforcement needs managed settings.
- `outputStyle` is case-sensitive; a mismatch falls back to Default ([output styles](https://code.claude.com/docs/en/output-styles)).
- An output style drops the built-in coding instructions unless `keep-coding-instructions: true` is set ([output styles](https://code.claude.com/docs/en/output-styles)).
- Model aliases differ by provider: on Bedrock and Vertex, `sonnet` is Sonnet 4.5; on Foundry the account default is Sonnet 4.5 ([model config](https://code.claude.com/docs/en/model-config)). Inference (from the research notes): configs written for the Anthropic API may select older models on third-party providers unless `ANTHROPIC_DEFAULT_*_MODEL` pins them.
- `disableAllHooks` and `allowManagedHooksOnly` also suppress non-managed status lines ([settings reference](https://code.claude.com/docs/en/settings-reference)).
- Deprecated or removed keys ([settings reference](https://code.claude.com/docs/en/settings-reference)): `includeCoAuthoredBy` (deprecated; use `attribution`), `disableArtifact` (deprecated; use `enableArtifact`), `keybindingFlavor` (deprecated; no effect), `permissionExplainerEnabled` (removed in v2.1.257), `taskOutputMaxChars` (removed in v2.1.277), `teammateDefaultModel` (removed in v2.1.234).
- Gap (research notes): the full per-key text of the ~240-entry settings reference was not enumerated, and the full list of `env` variables ignored in project and local files was not extracted.
- Gap (research notes): server-managed settings platform eligibility was not read in full.
- Gap (research notes): the full ~390-row environment variable table, and the "first session after an install or upgrade" and feature-flag-fetching behaviors, were not extracted.
- Gap (research notes): `keybindings.json`, `theme`, and terminal configuration were not covered.

## Sources

- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/settings-reference
- https://code.claude.com/docs/en/managed-settings
- https://code.claude.com/docs/en/permissions
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/output-styles
- https://code.claude.com/docs/en/model-config
- https://code.claude.com/docs/en/statusline
- https://code.claude.com/docs/en/env-vars
- Local CLI help: `claude --help` (v2.1.289)
