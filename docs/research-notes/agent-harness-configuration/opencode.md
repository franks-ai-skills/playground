# OpenCode agent harness: configuration and extension mechanisms (state as of 2026-10-04, release v1.18.34)

Method note: OpenCode was not installed locally. Findings come from the official docs (opencode.ai/docs, whose source lives in the repo at `packages/web/src/content/docs/*.mdx`), the source of a shallow clone of the repo at commit `907b3bc` (2026-10-02, `packages/opencode/package.json` version `1.18.34`), and GitHub release notes. Source links point to the `dev` branch, the branch the docs link to. Source-derived claims describe the behavior at that commit.

Abbreviations for the URLs used below:
- DOCS = https://opencode.ai/docs/
- SRC = https://github.com/anomalyco/opencode/blob/dev/
- REL = https://github.com/anomalyco/opencode/releases/tag/

## Project identity, location, and current release

### Takeaway
The project lives at github.com/anomalyco/opencode; the old `sst/opencode` URL still resolves there. The latest release is v1.18.34 (2026-09-30), with releases every few days. Global config lives in `~/.config/opencode/` and per-project config in `opencode.json[c]` and `.opencode/`.

### Cited Findings
- The README and docs link to `github.com/anomalyco/opencode`. The GitHub Action is published as `anomalyco/opencode/github@latest`. — [GitHub docs](https://opencode.ai/docs/github/); [README](https://github.com/anomalyco/opencode/blob/dev/README.md)
- Latest release is v1.18.34, published 2026-09-30. v1.18.0 shipped 2026-07-14 and v1.17.0 on 2026-06-10. — [Releases](https://github.com/anomalyco/opencode/releases)
- `@opencode-ai/plugin` has the same version (1.18.34) and exports `.`, `./tool`, `./tui`, `./v2/effect`, `./v2/promise`. — [SRC packages/plugin/package.json](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/package.json)

### Inferences
- With releases this frequent, any detail below can change within weeks. Pin a version when you depend on specific behavior.

### Gaps
- I did not check whether any successor org or fork beyond anomalyco exists. GitHub redirects `sst/opencode` to the same repo.

---

## Config: opencode.json / opencode.jsonc schema, locations, merge order, variables, providers/models, themes, keybinds, server

### Takeaway
There are two config files: `opencode.json[c]` for the server/runtime (schema `https://opencode.ai/config.json`) and `tui.json[c]` for the TUI (schema `https://opencode.ai/tui.json`). Config comes from 8 layers that are deep-merged, not replaced; later layers win on conflicting keys. `instructions` arrays are concatenated and plugin lists are deduped. Variables are `{env:VAR}` and `{file:path}`. Theme and keybinds moved from `opencode.json` to `tui.json`; the legacy keys are deprecated and auto-migrated.

### Cited Findings

**Format and schema**
- JSON and JSONC (JSON with comments) are both supported. Server/runtime schema is `https://opencode.ai/config.json`; TUI schema is `https://opencode.ai/tui.json`. — [Config](https://opencode.ai/docs/config/)

**Precedence order (later sources override earlier ones)**
1. Remote config from `.well-known/opencode`, fetched when you authenticate with a provider that supports it. These are organizational defaults.
2. Global config, `~/.config/opencode/opencode.json`.
3. Custom config file from the `OPENCODE_CONFIG` env var.
4. Project `opencode.json`.
5. `.opencode` directories (agents, commands, plugins).
6. Inline config from the `OPENCODE_CONFIG_CONTENT` env var.
7. Managed config files: `/Library/Application Support/opencode/` (macOS), `/etc/opencode/` (Linux), `%ProgramData%\opencode` (Windows).
8. macOS managed preferences: a `.mobileconfig` via MDM, preference domain `ai.opencode.managed`. Highest priority; users cannot override it.

Source: [Config – Precedence](https://opencode.ai/docs/config/)

**What the source adds to that order**
- The global layer reads `config.json`, then `opencode.json`, then `opencode.jsonc` from the global config dir. A legacy TOML `config` file is migrated. — [SRC packages/opencode/src/config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts)
- Project files are found by walking up from the cwd to the git worktree root, looking for `opencode.jsonc` and `opencode.json`. They are merged from the outermost to the innermost, so the closest file wins. — [SRC config/paths.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/paths.ts); [Config](https://opencode.ai/docs/config/)
- Config directories are scanned in this order:
  1. `~/.config/opencode`
  2. every `.opencode` dir from the cwd up to the worktree
  3. `~/.opencode`
  4. `OPENCODE_CONFIG_DIR`

  A `.opencode/opencode.json[c]` in any of these is also merged, then that directory's `commands/`, `agents/`, `modes/`, and `plugins/` are loaded. — [SRC config/paths.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/paths.ts), [SRC config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts)
- Setting `OPENCODE_DISABLE_PROJECT_CONFIG` skips project `opencode.json`, project `.opencode` dirs, and project AGENTS.md lookup. — [SRC config/paths.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/paths.ts), [SRC session/instruction.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts)
- If you are logged into an OpenCode Console account with an active org, the org config from `<console-url>/api/config` is merged after `OPENCODE_CONFIG_CONTENT`. — [SRC config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts)
- A `.well-known/opencode` response has the shape `{ config?, remote_config? }`. — [SRC packages/core/src/v1/config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)
- Directory names: subdirectory names are plural (`agents/`, `commands/`, `modes/`, `plugins/`, `skills/`, `tools/`, `themes/`). Singular names still work for backwards compatibility. — [Config](https://opencode.ai/docs/config/)
- `OPENCODE_CONFIG_DIR` is searched like `.opencode` and loaded after global config and `.opencode` dirs, so it can override them. — [Config](https://opencode.ai/docs/config/)

**Merge semantics**
- Configs use remeda `mergeDeep`, so objects merge deeply and later sources win per key. — [SRC config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts)
- `instructions` arrays are concatenated across sources and deduplicated. — same source
- `plugin` entries are deduped by plugin identity, and their origin (global or local) is tracked. Path-like plugin specs are resolved relative to the config file that declared them. — same source

**Managed settings**
- A file-based `opencode.json[c]` in the system dir requires admin rights to write.
- MDM plist keys map 1:1 to `opencode.json` fields; `Payload*` metadata keys are stripped.
- Run `opencode debug config` to see the resolved config.

Source: [Config – Managed settings](https://opencode.ai/docs/config/)

**Top-level `opencode.json` keys (from the schema source)**

| Key | Meaning |
| --- | --- |
| `$schema` | JSON schema reference for validation. |
| `shell` | Default shell for the terminal and the bash tool. |
| `logLevel` | `DEBUG`, `INFO`, `WARN`, or `ERROR`. |
| `server` | Settings for `opencode serve` / `opencode web`: `port`, `hostname`, `mdns`, `mdnsDomain`, `cors`. |
| `command` | Custom commands. |
| `skills` | `{ paths?: string[], urls?: string[] }`: extra skill folders and skill URLs. |
| `references` | Named git or local directory references (see below). |
| `reference` | Deprecated; use `references`. |
| `watcher.ignore` | Glob patterns the file watcher ignores. |
| `snapshot` | Boolean, default `true`. Internal-git snapshots that make undo/revert possible. |
| `plugin` | Array of `string` or `[string, options]`. |
| `share` | `manual`, `auto`, or `disabled`. |
| `autoshare` | Deprecated; use `share`. |
| `autoupdate` | `true`, `false`, or `"notify"`. |
| `disabled_providers` / `enabled_providers` | Provider deny list and allow list. When both name a provider, `disabled_providers` wins. |
| `model` / `small_model` | Format `provider/model`. |
| `default_agent` | Must be a primary agent; otherwise falls back to `build` with a warning. |
| `subagent_depth` | Non-negative integer, default `1`. |
| `username` | Name shown in conversations instead of the system username. |
| `mode` | Deprecated; use `agent`. |
| `agent` | Agent definitions, including the built-in keys `plan`, `build`, `general`, `explore`, `title`, `summary`, `compaction`. |
| `provider` | Custom provider configs and model overrides. |
| `mcp` | MCP server definitions. |
| `formatter` / `lsp` | Omit or `false` disables; `true` enables the built-ins; an object enables the built-ins with overrides. |
| `instructions` | Extra instruction files, globs, or URLs. |
| `layout` | Deprecated; the stretch layout is always used. |
| `permission` | Permission rules. |
| `tools` | Deprecated boolean map; use `permission`. |
| `attachment.image` | `auto_resize`, `max_width`, `max_height`, `max_base64_bytes`. |
| `enterprise.url` | Enterprise URL. |
| `tool_output` | `max_lines` (default 2000) and `max_bytes` (default 51200). Larger output is truncated and saved to disk. |
| `compaction` | `auto` (default `true`), `prune` (default `false`), `tail_turns`, `preserve_recent_tokens`, `reserved`. |
| `experimental` | `disable_paste_summary`, `batch_tool`, `openTelemetry`, `primary_tools`, `continue_loop_on_deny`, `mcp_timeout`, `policies`. |

Sources: [SRC core/src/v1/config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts); [Config](https://opencode.ai/docs/config/)

**Variable substitution**
- `{env:VAR}` substitutes an environment variable. An unset variable becomes an empty string.
- `{file:path}` substitutes a file's contents. The path is relative to the config file's directory, or absolute when it starts with `/` or `~`.
- Typical uses: API keys, prompt files (for example `"prompt": "{file:./prompts/build.txt}"`), and shared snippets.

Source: [Config – Variables](https://opencode.ai/docs/config/)

**Providers and models**
- Model IDs use the `provider/model-id` format. `small_model` runs light tasks such as title generation; by default OpenCode tries a cheaper model from the same provider. — [Config – Models](https://opencode.ai/docs/config/)
- Provider `options`:
  - `timeout`: default 300000 ms; `false` disables it.
  - `headerTimeout`: default 300000 ms.
  - `chunkTimeout`: default 300000 ms; `false` disables it.
  - `setCacheKey`
  - `apiKey`, `baseURL`
  - Bedrock-specific: `region`, `profile`, `endpoint`.

  Source: [Config](https://opencode.ai/docs/config/)
- Header and chunk timeouts were raised to a 5-minute default in v1.18.27. — [REL v1.18.27](https://github.com/anomalyco/opencode/releases/tag/v1.18.27)
- `opencode auth login` stores credentials in `~/.local/share/opencode/auth.json`. Providers come from Models.dev; env vars and a project `.env` are also read. `opencode models [provider] [--refresh] [--verbose]` lists models. — [CLI](https://opencode.ai/docs/cli/)
- `experimental.policies` takes entries like `{effect:"deny", action:"provider.use", resource:"openai"}`. — [Config – Policies](https://opencode.ai/docs/config/)

**TUI config, themes, and keybinds**
- `tui.json[c]` keys:
  - `theme`
  - `keybinds`: merged with the built-in defaults; `leader` defaults to `ctrl+x`; `"none"` unbinds a key.
  - `leader_timeout`: default 2000.
  - `scroll_speed`, `scroll_acceleration.enabled`
  - `diff_style`: `auto` or `stacked`.
  - `cursor.style` / `cursor.blinking`
  - `mouse`
  - `attention`: `enabled` (default `false`), `notifications`, `sound`, `volume`, `sound_pack`, `sounds`.
  - `plugin`: TUI plugins; the source handles plugin specs in tui config.

  The global file is `~/.config/opencode/tui.json` and the project file sits next to `opencode.json`. `OPENCODE_TUI_CONFIG` sets a custom path. — [TUI](https://opencode.ai/docs/tui/); [Config](https://opencode.ai/docs/config/); [Keybinds](https://opencode.ai/docs/keybinds/); [SRC config/tui.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/tui.ts)
- The legacy `theme`, `keybinds`, and `tui` keys in `opencode.json` are deprecated and migrated automatically when possible. — [Config](https://opencode.ai/docs/config/)
- Custom themes are JSON files. They are loaded in this order: built-in themes, then `~/.config/opencode/themes/*.json`, then `<project-root>/.opencode/themes/*.json`, then `./.opencode/themes/*.json`. Colors can be hex, ANSI 0–255, references to `defs`, `{dark, light}` variants, or `"none"` for the terminal default. — [Themes](https://opencode.ai/docs/themes/)

**Server config**
- `server.port`, `hostname`, `mdns`, `mdnsDomain` (default `opencode.local`), `cors` (full origins). — [Config – Server](https://opencode.ai/docs/config/)

**References (newer feature)**
- Configure `references: { alias: "../path" | "owner/repo" | { path | repository, branch?, description?, hidden? } }`.
- Git repos are cloned into a cache and refreshed asynchronously.
- References show up in `@` autocomplete as `@alias` or `@alias/file`.
- References that have a `description` are injected into agent system context.
- Reference dirs are automatically allowed through the `external_directory` permission. Normal tool permissions still apply.

Source: [References](https://opencode.ai/docs/references/)
- Release history: v1.17.1 added `description` and `hidden` and deprecated `reference` in favor of `references`; v1.17.12 added reference autocomplete. — [REL v1.17.1](https://github.com/anomalyco/opencode/releases/tag/v1.17.1), [REL v1.17.12](https://github.com/anomalyco/opencode/releases/tag/v1.17.12)

**Environment variables (selection)**
- Config: `OPENCODE_CONFIG`, `OPENCODE_TUI_CONFIG`, `OPENCODE_CONFIG_DIR`, `OPENCODE_CONFIG_CONTENT`, `OPENCODE_PERMISSION` (inline JSON permissions).
- Behavior toggles: `OPENCODE_DISABLE_AUTOUPDATE`, `OPENCODE_DISABLE_AUTOCOMPACT`, `OPENCODE_DISABLE_DEFAULT_PLUGINS`, `OPENCODE_DISABLE_LSP_DOWNLOAD`.
- Claude Code compatibility: `OPENCODE_DISABLE_CLAUDE_CODE`, `..._CLAUDE_CODE_PROMPT`, `..._CLAUDE_CODE_SKILLS`.
- Web search: `OPENCODE_ENABLE_EXA`, `OPENCODE_ENABLE_PARALLEL`.
- Server auth: `OPENCODE_SERVER_PASSWORD`, `OPENCODE_SERVER_USERNAME`.
- Experimental flags, for example `OPENCODE_EXPERIMENTAL_LSP_TOOL`, `_SCOUT`, `_BACKGROUND_SUBAGENTS`, `_WORKSPACES`, `_PLAN_MODE`.

Source: [CLI – Environment variables](https://opencode.ai/docs/cli/)

**Minimal example**
```jsonc
// opencode.jsonc (project root)
{ "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "instructions": ["CONTRIBUTING.md"],
  "permission": { "bash": "ask" },
  "provider": { "anthropic": { "options": { "apiKey": "{env:ANTHROPIC_API_KEY}" } } } }
```

### Inferences
- The docs list `.opencode` directories (5) before `OPENCODE_CONFIG_CONTENT` (6). In the source, the `OPENCODE_CONFIG_DIR` dir and `~/.opencode` are also scanned at step 5. The docs do not mention `~/.opencode`, so treat it as an implementation detail.

### Gaps
- Only `instructions` (concatenated and deduplicated) and `plugin` (deduplicated by plugin identity) have documented array merge behavior. How other arrays, such as `watcher.ignore` or `disabled_providers`, merge across layers is not documented.
- I did not fetch the generated `https://opencode.ai/config.json` itself; the key list comes from the Effect schema source.
- The full built-in keybind list (about 100 entries in keybinds.mdx) is not reproduced here.
- I could not find the release where LSP and formatters became opt-in (disabled unless configured). The current docs and schema both say "Omit or set to false to disable", but no release note in the v1.0–v1.18 notes I searched matched.

---

## Instructions/rules: AGENTS.md, CLAUDE.md compatibility, `instructions` (globs/URLs), /init

### Takeaway
AGENTS.md files are loaded in two scopes, project and global. In each scope the first matching filename wins: `AGENTS.md` beats `CLAUDE.md`, which beats the deprecated `CONTEXT.md`. Every ancestor copy of the winning project filename up to the worktree root is included. Nested AGENTS.md files below the cwd are attached lazily when the read tool opens a file in that subtree. The `instructions` config adds files, globs, `~/` paths, and http(s) URLs (5 s timeout). `/init` creates or improves AGENTS.md.

### Cited Findings
- Project scope: `AGENTS.md` in the project root applies to that directory and its subdirectories. Global scope: `~/.config/opencode/AGENTS.md` applies to all sessions. — [Rules](https://opencode.ai/docs/rules/)
- Claude Code fallbacks:
  - Project `CLAUDE.md` is used only if no `AGENTS.md` exists.
  - `~/.claude/CLAUDE.md` is used only if no `~/.config/opencode/AGENTS.md` exists.
  - `~/.claude/skills/` is also read.
  - Opt out with `OPENCODE_DISABLE_CLAUDE_CODE=1` (all `.claude` support), `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT=1`, or `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1`.

  Source: [Rules](https://opencode.ai/docs/rules/)
- Precedence: local files found by walking up from the cwd (`AGENTS.md`, `CLAUDE.md`), then the global file, then `~/.claude/CLAUDE.md`. The first match wins in each category. — [Rules](https://opencode.ai/docs/rules/)
- Source detail on precedence:
  - Project filenames are tried in the order `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md` (the last is marked deprecated).
  - For the first filename that matches, all matches found walking up from the cwd to the worktree are added.
  - Each file is injected into the system prompt as `Instructions from: <path>\n<content>`.

  Source: [SRC session/instruction.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts)
- Lazy nested instructions: when the read tool reads a file, OpenCode walks upward from that file toward the project root and attaches any `AGENTS.md`/`CLAUDE.md`/`CONTEXT.md` it finds that is not already in the system prompt. Each file is attached once per message. — [SRC session/instruction.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts), [SRC tool/read.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/tool/read.ts)
- The `instructions` array accepts:
  - paths and glob patterns, e.g. `"CONTRIBUTING.md"`, `".cursor/rules/*.md"`, `"packages/*/AGENTS.md"`
  - remote URLs, fetched with a 5 s timeout

  All of these are combined with the AGENTS.md files. — [Rules](https://opencode.ai/docs/rules/)
- How the source resolves `instructions` entries: relative entries are glob-searched upward from the cwd to the worktree; `~/` and absolute paths are globbed directly; URLs are fetched on every system-prompt build. — [SRC session/instruction.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts)
- OpenCode does not parse `@file` references inside AGENTS.md automatically. You can either use `instructions`, or write AGENTS.md text that tells the model to read referenced files lazily. — [Rules](https://opencode.ai/docs/rules/)
- `/init` scans the repo and may ask targeted questions. It writes or improves AGENTS.md in place with build/lint/test commands, architecture, conventions, gotchas, and pointers to existing Cursor/Copilot rules. — [Rules](https://opencode.ai/docs/rules/)
- In source, `/init` is a built-in command described as "guided AGENTS.md setup". — [SRC command/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/command/index.ts)
- MCP server `instructions` are appended to session context since v1.17.10. — [REL v1.17.10](https://github.com/anomalyco/opencode/releases/tag/v1.17.10)

Minimal example:
```json
{ "$schema": "https://opencode.ai/config.json",
  "instructions": ["docs/guidelines.md", "packages/*/AGENTS.md", "https://raw.githubusercontent.com/my-org/rules/main/style.md"] }
```

### Inferences
- Because every ancestor copy of the winning filename is loaded, a monorepo with AGENTS.md at the root and in a package gets both when you start in the package. AGENTS.md and CLAUDE.md are never mixed within one scope.

### Gaps
- None of the sources state a size limit for instruction files.

---

## Permissions

### Takeaway
`permission` maps permission keys (tool names, wildcards, MCP tool names) to `allow`, `ask`, or `deny`, or to an object of pattern → action. In an object, the last matching rule wins. Defaults are permissive. Agent-level `permission` merges over the global rules. The boolean `tools` map is deprecated since v1.1.1. `--auto` auto-approves anything not explicitly denied.

### Cited Findings
- Actions are `allow`, `ask`, and `deny`. A single string sets everything at once, e.g. `"permission": "allow"`. — [Permissions](https://opencode.ai/docs/permissions/)
- Keys and what they match:

  | Key | Matches |
  | --- | --- |
  | `read` | file path |
  | `edit` | covers `edit`, `write`, `apply_patch` |
  | `glob` | the glob pattern |
  | `grep` | the regex |
  | `list` | — |
  | `bash` | parsed command, e.g. `git status --porcelain` |
  | `task` | subagent type |
  | `skill` | skill name |
  | `lsp` | currently non-granular |
  | `question` | — |
  | `webfetch` | the URL |
  | `websearch` | the query |
  | `todowrite` | — |
  | `external_directory` | — |
  | `doom_loop` | the same call repeated 3 times with identical input |

  Source: [Permissions](https://opencode.ai/docs/permissions/); [Agents](https://opencode.ai/docs/agents/)
- In the schema, `todowrite`, `question`, `webfetch`, `websearch`, and `doom_loop` accept only an action. The other keys accept an action or a pattern object. Unknown keys (custom or MCP tools) are allowed. — [SRC core/src/v1/config/permission.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/permission.ts)
- Pattern syntax:
  - `*` matches any sequence and `?` matches one character.
  - `~` or `$HOME` expands to the home directory.
  - Last matching rule wins, so put `"*"` first.
  - User key order is preserved at parse time to keep precedence correct.

  Source: [Permissions](https://opencode.ai/docs/permissions/); [SRC permission.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/permission.ts)
- `"grep *"` allows `grep pattern file`, but `"grep"` alone does not match commands with arguments. — [Permissions](https://opencode.ai/docs/permissions/)
- Defaults: most keys are `allow`; `doom_loop` and `external_directory` are `ask`; `read` allows `*` but denies `*.env` and `*.env.*`, while allowing `*.env.example`. — [Permissions](https://opencode.ai/docs/permissions/)
- An "ask" prompt offers three answers:
  - `once`
  - `always`: approves the tool-suggested patterns (e.g. `git status*`) for the rest of the session
  - `reject`

  Source: [Permissions](https://opencode.ai/docs/permissions/)
- `external_directory` gates any path outside the working directory, e.g. `{"~/projects/personal/**": "allow"}`. Allowed directories inherit the workspace defaults. — [Permissions](https://opencode.ai/docs/permissions/)
- Per-agent `permission` is merged with the global config, and agent rules take precedence. It can be set in JSON or in agent markdown frontmatter. — [Permissions](https://opencode.ai/docs/permissions/)
- MCP or custom tools can be gated by name, e.g. `"mymcp_*": "deny"`. — [Agents](https://opencode.ai/docs/agents/); [Tools](https://opencode.ai/docs/tools/)
- Auto mode: `opencode --auto` or `opencode run --auto` approves requests that would otherwise ask; explicit `deny` still applies. The TUI palette has "Enable/Disable auto-approve permissions" toggles. — [Permissions](https://opencode.ai/docs/permissions/)
- Auto mode release history: introduced as "yolo mode" in v1.17.12; auto-accept state is kept per server since v1.18.0. — [REL v1.17.12](https://github.com/anomalyco/opencode/releases/tag/v1.17.12), [REL v1.18.0](https://github.com/anomalyco/opencode/releases/tag/v1.18.0)
- Deprecation: as of v1.1.1 the legacy `tools` booleans are merged into `permission` and still supported. `true` becomes `allow` and `false` becomes `deny`. `write`, `edit`, and `patch` map to `edit`. — [Permissions](https://opencode.ai/docs/permissions/); [REL v1.1.1](https://github.com/anomalyco/opencode/releases/tag/v1.1.1); [SRC core/src/v1/config/agent.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/agent.ts)
- The `OPENCODE_PERMISSION` env var supplies inline JSON permissions. — [CLI](https://opencode.ai/docs/cli/)
- Plugins can override decisions through the `permission.ask` hook (`output.status` = `ask`, `deny`, or `allow`). — [SRC packages/plugin/src/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts)
- `experimental.continue_loop_on_deny` keeps the agent loop running after a denied tool call. — [SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)

Minimal example:
```json
{ "permission": { "*": "ask", "read": "allow",
  "bash": { "*": "ask", "git status *": "allow", "rm *": "deny" },
  "edit": { "*": "deny", "src/**": "allow" } } }
```

### Gaps
- None of the sources describe the exact algorithm that merges agent and global rules: whether objects are concatenated or replaced key by key. The docs only say agent rules take precedence.

---

## Agents: primary vs subagents, markdown and JSON config, all options, @mentions, task tool, switching

### Takeaway
There are two kinds of agents:
- Primary agents (built-in `build` and `plan`) are cycled with Tab.
- Subagents (built-in `general`, `explore`, and an experimental `scout`) are invoked by the model through the `task` tool or by the user with `@name`.

Hidden system agents `compaction`, `title`, and `summary` also exist. You define agents in JSON under `agent` or as markdown files in `agents/`, where the file path gives the name. Options are `description`, `mode`, `model`, `variant`, `prompt`, `temperature`, `top_p`, `steps`, `disable`, `hidden`, `color`, `permission`, `options`, and passthrough keys. `tools` and `maxSteps` are deprecated.

### Cited Findings
- Built-in agents:

  | Agent | Mode | Behavior |
  | --- | --- | --- |
  | Build | primary | Default; all tools. |
  | Plan | primary | Restricted: file edits and bash are `ask`. |
  | General | subagent | Full tools except todo; can run work in parallel. |
  | Explore | subagent | Fast, read-only codebase search. |
  | Scout | subagent | Read-only research on external docs and dependencies; clones repos into a managed cache. |
  | compaction, title, summary | primary | Hidden, run automatically. |

  Source: [Agents](https://opencode.ai/docs/agents/)
- Scout is gated behind the `OPENCODE_EXPERIMENTAL_SCOUT` flag. — [CLI – Experimental](https://opencode.ai/docs/cli/)
- Switching and navigation:
  - Tab or the `switch_agent` keybind cycles primary agents.
  - `@general …` invokes a subagent manually.
  - Child sessions: `session_child_first` (Leader+Down) enters the first one, `session_child_cycle` (Right) and `session_child_cycle_reverse` (Left) move between them, `session_parent` (Up) returns.

  Source: [Agents – Usage](https://opencode.ai/docs/agents/)
- Markdown agents live in `~/.config/opencode/agents/` or `.opencode/agents/`. YAML frontmatter holds the options and the body is the prompt. The filename gives the name, e.g. `review.md` → `review`. — [Agents](https://opencode.ai/docs/agents/)
- In source, the scan glob is `{agent,agents}/**/*.md`. Nested directories are allowed and the name is the relative path without extension, e.g. `agents/team/review.md` → `team/review`. Markdown agents merge over JSON-defined agents from earlier layers. — [SRC config/agent.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/agent.ts), [SRC config/entry-name.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/entry-name.ts)
- Legacy modes: files in `{mode,modes}/*.md` are loaded as agents with `mode: primary`. The top-level `mode` config key is deprecated in favor of `agent`. — [SRC config/agent.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/agent.ts); [SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)
- Options:
  - `description`: documented as **required**; used for automatic selection.
  - `temperature`: model default, typically 0 for most models.
  - `top_p`
  - `steps`: maximum agentic iterations, after which the agent is forced to give a text summary. `maxSteps` is deprecated.
  - `disable`
  - `prompt`: often `{file:...}`, resolved relative to the config file.
  - `model`: when omitted, primary agents use the global model and subagents inherit the invoking agent's model.
  - `tools`: deprecated.
  - `permission`
  - `mode`: `primary`, `subagent`, or `all` (default `all`).
  - `hidden`: hides a subagent from `@` autocomplete; the Task tool can still invoke it.
  - `color`: hex or a theme color.
  - Any other key is passed to the provider, e.g. `reasoningEffort` or `textVerbosity`.

  Source: [Agents – Options](https://opencode.ai/docs/agents/)
- The schema also has `variant` (default model variant, applied only when the agent uses its own configured model) and `options`. Unknown keys are folded into `options`. — [SRC core/src/v1/config/agent.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/agent.ts)
- `permission.task` controls which subagents an agent may call, using globs where the last match wins. A denied subagent is removed from the Task tool description entirely. Users can still `@`-invoke any subagent. — [Agents – Task permissions](https://opencode.ai/docs/agents/)
- Task tool parameters:
  - `description`: 3–5 words.
  - `prompt`
  - `subagent_type`
  - `task_id`: optional; resumes a prior subagent session.
  - `command`: optional; the command that triggered the task.

  The permission check matches `subagent_type`. — [SRC tool/task.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/tool/task.ts)
- Nesting: `subagent_depth` defaults to 1, so subagents cannot spawn subagents. `2` allows one more level and `0` disables subagents. Changed in v1.18.2. — [Config](https://opencode.ai/docs/config/); [REL v1.18.2](https://github.com/anomalyco/opencode/releases/tag/v1.18.2)
- `default_agent` picks the default primary agent across TUI, `opencode run`, desktop, and the GitHub Action. — [Config](https://opencode.ai/docs/config/)
- `opencode agent create` creates an agent interactively. It runs non-interactively when given `--path`, `--description`, `--mode`, and `--permissions` (plus optional `-m`). Anything not allowed is written as denied. `opencode agent list` lists agents. — [CLI](https://opencode.ai/docs/cli/); [Agents](https://opencode.ai/docs/agents/)
- `todowrite` is disabled for subagents by default. — [Tools](https://opencode.ai/docs/tools/)
- `experimental.primary_tools` lists tools available only to primary agents. — [SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)
- Background subagents are behind `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS`. — [CLI](https://opencode.ai/docs/cli/)

Minimal example:
```markdown
<!-- .opencode/agents/review.md -->
---
description: Reviews code for quality; use after edits
mode: subagent
model: anthropic/claude-sonnet-4-5
temperature: 0.1
permission: { edit: deny, bash: { "*": ask, "git diff*": allow } }
---
You are a code reviewer. Report issues; do not edit files.
```

### Inferences
- `description` is "required" in the docs but optional in the schema.

### Gaps
- None of the sources document Scout's default model, permission set, or cache location beyond "managed cache".

---

## Commands: custom slash commands, templates, arguments, shell injection, file references

### Takeaway
Commands are markdown files in `commands/`, where the path gives the name and the body is the template, or entries in the `command` JSON key. Templates support `$ARGUMENTS`, `$1..$n`, `` !`cmd` `` shell output, and `@file` inclusion. Options are `template` (required), `description`, `agent`, `model`, `variant`, and `subtask`. Custom commands override built-ins. MCP prompts and skills also show up as slash commands.

### Cited Findings
- Locations are `~/.config/opencode/commands/` and `.opencode/commands/`, plus the JSON `command` key. Invoke with `/name args`. — [Commands](https://opencode.ai/docs/commands/)
- In source, the scan glob is `{command,commands}/**/*.md`. Nested paths become names such as `git/commit`. Invalid frontmatter raises an `InvalidError`. — [SRC config/command.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/command.ts)
- Template syntax:
  - `$ARGUMENTS` is the whole argument string.
  - `$1`, `$2`, … are positional arguments; quoted strings are kept together.
  - `` !`command` `` runs in the project root and its output is injected.
  - `@path/to/file` includes the file's content.

  Source: [Commands](https://opencode.ai/docs/commands/)
- Options:
  - `template`: required.
  - `description`: shown in the TUI.
  - `agent`: defaults to the current agent. If it names a subagent, the command runs as a subagent invocation by default; `subtask: false` disables that.
  - `subtask: true`: forces a subagent run, keeping the primary context clean.
  - `model`

  Source: [Commands – Options](https://opencode.ai/docs/commands/)
- The schema adds `variant`. — [SRC core/src/v1/config/command.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/command.ts)
- Built-in commands include `/init`, `/undo`, `/redo`, `/share`, `/help`, and others: `/connect`, `/compact`, `/details`, `/editor`, `/exit`, `/export`, `/models`, `/new`, `/sessions`, `/themes`, `/thinking`, `/unshare`. A custom command with the same name overrides the built-in. — [Commands](https://opencode.ai/docs/commands/); [TUI](https://opencode.ai/docs/tui/)
- The command registry in source:
  - Built-in `init` ("guided AGENTS.md setup") and `review` ("review changes [commit|branch|pr], defaults to uncommitted", `subtask: true`).
  - Config commands are added next.
  - MCP server prompts are registered as commands (`source: "mcp"`), with their arguments mapped to `$1..$n`.
  - Every skill is registered as a command (`source: "skill"`) unless a command already has that name. The template is the skill body plus "Base directory for this skill: <dir>".

  Source: [SRC command/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/command/index.ts)
- Plugins can rewrite command parts through the `command.execute.before` hook. — [SRC plugin/src/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts)
- `opencode run --command <name> [args]` runs a command non-interactively. — [CLI](https://opencode.ai/docs/cli/)

Minimal example:
```markdown
<!-- .opencode/commands/review-changes.md -->
---
description: Review recent changes
agent: plan
subtask: true
---
Recent commits:
!`git log --oneline -10`
Review these, focusing on $ARGUMENTS.
```

### Gaps
- None of the sources say whether `` !`cmd` `` respects bash permissions. The docs only say the command runs in the project root.

---

## Skills: SKILL.md / Agent Skills support

### Takeaway
OpenCode supports Agent Skills (`SKILL.md` with YAML frontmatter). Skills are discovered from `.opencode/skills`, `~/.config/opencode/skills`, `.claude/skills`, `~/.claude/skills`, `.agents/skills`, and `~/.agents/skills`, plus `skills.paths` and `skills.urls` in config. The model loads them on demand through the native `skill` tool, which is gated by `permission.skill`. Skills are also exposed as slash commands, and a built-in `customize-opencode` skill ships with OpenCode.

### Cited Findings
- Locations (one folder per skill, containing `SKILL.md`):
  - `.opencode/skills/<name>/`
  - `~/.config/opencode/skills/<name>/`
  - `.claude/skills/<name>/`
  - `~/.claude/skills/<name>/`
  - `.agents/skills/<name>/`
  - `~/.agents/skills/<name>/`

  For project paths, OpenCode walks up from the cwd to the git worktree. — [Skills](https://opencode.ai/docs/skills/)
- In source:
  - Pattern `skills/**/SKILL.md` for `.claude` and `.agents` dirs.
  - Pattern `{skill,skills}/**/SKILL.md` in every OpenCode config dir.
  - `**/SKILL.md` under each `skills.paths` entry (relative to cwd, `~/`, or absolute).
  - `skills.urls`: OpenCode fetches `<url>/index.json` (e.g. `https://example.com/.well-known/skills/`) and pulls the listed skills.
  - `OPENCODE_DISABLE_EXTERNAL_SKILLS` turns off `.claude` and `.agents` discovery.

  Source: [SRC skill/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/skill/index.ts), [SRC skill/discovery.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/skill/discovery.ts), [SRC core skills.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/skills.ts)
- Frontmatter:
  - Recognized fields: `name` (required), `description` (required), `license`, `compatibility`, `metadata` (string → string map). Unknown fields are ignored.
  - `name`: 1–64 characters, `^[a-z0-9]+(-[a-z0-9]+)*$`, and it must match the directory name.
  - `description`: 1–1024 characters.

  Source: [Skills](https://opencode.ai/docs/skills/)
- Discovery and invocation: the `skill` tool's description lists the available skills as `<available_skills><skill><name/><description/></skill>…`. The agent calls `skill({ name: "git-release" })` to load the full content. — [Skills](https://opencode.ai/docs/skills/)
- Permissions:
  - `permission.skill` takes patterns. `allow` loads immediately, `deny` hides the skill and rejects access, `ask` prompts first.
  - Overrides work per agent.
  - `tools: { skill: false }` removes `<available_skills>` entirely.

  Source: [Skills](https://opencode.ai/docs/skills/)
- Troubleshooting: the filename must be `SKILL.md` in all caps, `name` and `description` must be present, names must be unique across all locations, and denied skills are hidden. — [Skills](https://opencode.ai/docs/skills/)
- Skills appear as slash commands with the base-directory note appended. Since v1.17.10 that note is a filesystem path, not a `file://` URL. — [SRC command/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/command/index.ts); [REL v1.17.10](https://github.com/anomalyco/opencode/releases/tag/v1.17.10)
- Built-in skill `customize-opencode`: "Use ONLY when the user is editing or creating opencode's own configuration… agents, subagents, skills, plugins, MCP servers, or permission rules". — [SRC skill/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/skill/index.ts)
- Release history: v1.16.0 added skill discovery and file-based agent loading; v1.17.12 added refresh of cached remote skills and preservation of skill resource paths. — [REL v1.16.0](https://github.com/anomalyco/opencode/releases/tag/v1.16.0); [REL v1.17.12](https://github.com/anomalyco/opencode/releases/tag/v1.17.12)

### Inferences
- OpenCode reads Claude Code-format skills (`.claude/skills`) directly. Fields that only Claude Code understands, such as `allowed-tools`, are ignored ("Unknown frontmatter fields are ignored").

### Gaps
- None of the sources specify the format of the remote `index.json` for `skills.urls`, and `skills.paths`/`skills.urls` do not appear in the user docs page.

---

## Tools and custom tools; MCP servers (local/remote, OAuth); LSP and formatters

### Takeaway
- **Built-in tools:** bash, edit, write, read, grep, glob, list, apply_patch, skill, todowrite, webfetch, websearch, question, task, plus an experimental lsp tool.
- **Custom tools:** TS/JS files in `tools/` that use `tool()` from `@opencode-ai/plugin`, or tools returned by plugins.
- **MCP:** servers go under `mcp` as `local` (stdio command) or `remote` (URL), with automatic OAuth that uses dynamic client registration.
- **LSP and formatters:** both are now opt-in; omit the key and they stay disabled.

### Cited Findings

**Built-in tools**
- All tools are enabled and need no permission by default. — [Tools](https://opencode.ai/docs/tools/)
- Behavior notes:
  - `websearch` (Exa or Parallel) is available only with the OpenCode or OpenCode Go provider, or with `OPENCODE_ENABLE_EXA` or `OPENCODE_ENABLE_PARALLEL` set.
  - `lsp` requires `OPENCODE_EXPERIMENTAL_LSP_TOOL` or `OPENCODE_EXPERIMENTAL`.
  - In plugin hooks, `apply_patch` appears as `input.tool === "apply_patch"` and carries `args.patchText`.
  - grep and glob use ripgrep and respect `.gitignore`; a `.ignore` file with `!path` re-includes paths.

  Source: [Tools](https://opencode.ai/docs/tools/)
- `experimental.batch_tool` enables a batch tool. — [SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)

**Custom tools**
- Location: `.opencode/tools/` or `~/.config/opencode/tools/`.
- Naming: the filename is the tool name for a default export. Named exports become `<filename>_<export>`.
- Arguments are defined with `tool.schema` (Zod) or plain Zod.
- `execute(args, context)` receives `agent`, `sessionID`, `messageID`, `directory`, `worktree`, `abort`, `metadata()`, `ask()`.
- A custom tool with the same name as a built-in overrides it.
- Tools can shell out to any language, e.g. with `Bun.$`.

Source: [Custom tools](https://opencode.ai/docs/custom-tools/); [SRC plugin/src/tool.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/tool.ts)
- A tool may return a string or `{ title?, output, metadata?, attachments?: [{type:"file", mime, url, filename?}] }`. — [SRC plugin/src/tool.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/tool.ts)
- Tool output beyond 2000 lines or 51200 bytes (configurable in `tool_output`) is truncated and saved to disk. — [SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)

**MCP servers**
- Local server fields:
  - `type: "local"`
  - `command`: string array
  - `cwd`
  - `environment`
  - `enabled`
  - `timeout`: tool-fetch timeout, default 5000 ms

  Source: [MCP servers](https://opencode.ai/docs/mcp-servers/)
- Remote server fields:
  - `type: "remote"`
  - `url`
  - `enabled`
  - `headers`
  - `oauth`: an object or `false`
  - `timeout`

  Source: [MCP servers](https://opencode.ai/docs/mcp-servers/)
- OAuth:
  - Triggered automatically on a 401 response.
  - Uses Dynamic Client Registration (RFC 7591) when the server supports it.
  - Pre-registered clients use `oauth.clientId`, `clientSecret`, and `scope`.
  - Tokens are stored in `~/.local/share/opencode/mcp-auth.json`.
  - CLI: `opencode mcp add | list | auth [name] | auth list | logout [name] | debug <name>`.

  Source: [MCP servers](https://opencode.ai/docs/mcp-servers/); [CLI](https://opencode.ai/docs/cli/)
- MCP tools are prefixed with the server name (`<server>_<tool>`) and can be gated with `permission` or the legacy `tools` globs, globally or per agent. An org `.well-known/opencode` can ship servers disabled and let users enable them locally. — [MCP servers](https://opencode.ai/docs/mcp-servers/)
- `experimental.mcp_timeout` sets the MCP request timeout. — [SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)
- The docs warn that MCP tools consume context; the GitHub MCP server is called out as token-heavy. — [MCP servers](https://opencode.ai/docs/mcp-servers/)

**LSP**
- Disabled by default. `"lsp": true` enables the built-ins, an object enables them with overrides, and `false` disables all.
- Per-server keys: `disabled`, `command`, `extensions`, `env`, `initialization`.
- About 35 built-in servers (typescript, pyright, gopls, rust-analyzer, eslint, oxlint, clangd, jdtls, …), many installed automatically. `OPENCODE_DISABLE_LSP_DOWNLOAD` stops the downloads.
- Diagnostics are fed back to the agent.
- The docs caution that running lint/typecheck CLIs directly is often better.

Source: [LSP](https://opencode.ai/docs/lsp/)

**Formatters**
- Disabled by default. `"formatter": true` enables the built-ins; per-formatter keys are `disabled`, `command` (with a `$FILE` placeholder), `environment`, and `extensions`.
- Built-ins include prettier, biome, ruff, gofmt, rustfmt, shfmt, and others.
- Formatters run after each write or edit.

Source: [Formatters](https://opencode.ai/docs/formatters/)

Minimal examples:
```ts
// .opencode/tools/database.ts
import { tool } from "@opencode-ai/plugin"
export default tool({ description: "Query the project database",
  args: { query: tool.schema.string().describe("SQL") },
  async execute(args, ctx) { return `ran ${args.query} in ${ctx.worktree}` } })
```
```json
{ "mcp": { "everything": { "type": "local", "command": ["npx","-y","@modelcontextprotocol/server-everything"] },
           "remote-api": { "type": "remote", "url": "https://mcp.example.com/mcp", "oauth": false,
                           "headers": { "Authorization": "Bearer {env:MY_API_KEY}" } } },
  "lsp": true, "formatter": { "prettier": { "disabled": true } } }
```

### Gaps
- The docs give no hard limit on the number of MCP tools. Context cost is the only stated constraint.
- None of the sources document the `list` tool in tools.mdx, although the `list` permission key exists.

---

## Plugins: JS/TS plugin API, hooks and events, locations, npm plugins

### Takeaway
A plugin is a JS/TS module that exports async functions. Each function receives `{ project, client, $, directory, worktree, serverUrl, experimental_workspace }` and returns a hooks object. Plugins load from `plugins/` dirs and from npm via the `plugin` config key; an entry can be `[name, options]`. Hooks cover `event` (bus events), `tool`, `auth`, `provider`, `chat.*`, `permission.ask`, `command.execute.before`, `tool.execute.before/after`, `shell.env`, `tool.definition`, `dispose`, and several `experimental.*` hooks. v1.17.10 added a V2 plugin API (Promise and Effect) with namespaced transform hooks. TUI plugins also exist.

### Cited Findings

**Loading**
- Local plugins: `.opencode/plugins/` and `~/.config/opencode/plugins/`, loaded automatically at startup. — [Plugins](https://opencode.ai/docs/plugins/)
- npm plugins: `"plugin": ["opencode-wakatime", "@my-org/x"]`. They are installed with Bun at startup and cached in `~/.cache/opencode/node_modules/`. — [Plugins](https://opencode.ai/docs/plugins/)
- `opencode plugin <module> [-g] [-f]` (alias `plug`) installs a plugin and updates the config. — [CLI](https://opencode.ai/docs/cli/)
- Load order: global config `plugin`, then project config `plugin`, then the global plugin dir, then the project plugin dir. All hooks run in sequence. The same npm package at the same version loads once. — [Plugins](https://opencode.ai/docs/plugins/)
- Dependencies: a `package.json` in the config dir (e.g. `.opencode/package.json`) is installed with `bun install` at startup. OpenCode also auto-adds `@opencode-ai/plugin` to each config dir. — [Plugins](https://opencode.ai/docs/plugins/); [SRC config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts)
- Plugin options: config entries can be tuples `[spec, {…options}]`. The `Plugin` type is `(input: PluginInput, options?: PluginOptions) => Promise<Hooks>`. A `PluginModule` may also be `{ id?, server: Plugin }`. — [SRC plugin/src/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts); [SRC core plugin.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/plugin.ts)
- `--pure` runs without external plugins and `OPENCODE_DISABLE_DEFAULT_PLUGINS` disables the default plugins. — [CLI](https://opencode.ai/docs/cli/)
- Since v1.15.6, a plugin file that fails to load no longer breaks the remaining plugins. — [REL v1.15.6](https://github.com/anomalyco/opencode/releases/tag/v1.15.6)

**Hooks interface (current source)**

| Hook | Purpose |
| --- | --- |
| `dispose` | Cleanup; added in v1.15.11. |
| `event({event})` | Receives bus events. |
| `config(cfg)` | Receives the config. |
| `tool: {name: ToolDefinition}` | Adds tools. |
| `auth: AuthHook` | Provider auth with OAuth or API methods and a loader. |
| `provider: ProviderHook` | `{id, models()}`. |
| `chat.message` | `(input {sessionID, agent, model, messageID, variant}, output {message, parts})`. |
| `chat.params` | Modify `temperature`, `topP`, `topK`, `maxOutputTokens`, `options`. |
| `chat.headers` | Modify request headers. |
| `permission.ask` | `output.status` = `ask`, `deny`, or `allow`. |
| `command.execute.before` | `input {command, sessionID, arguments}`, `output {parts}`. |
| `tool.execute.before` | `input {tool, sessionID, callID}`, `output {args}`; throwing blocks the call. |
| `tool.execute.after` | `input {…, args}`, `output {title, output, metadata}`. |
| `shell.env` | `input {cwd, sessionID?, callID?}`, `output {env}`. |
| `tool.definition` | Rewrite a tool's description and parameters. |
| `experimental.chat.messages.transform` | Transform the message list. |
| `experimental.chat.system.transform` | `output.system: string[]`. |
| `experimental.provider.small_model` | Choose the small model. |
| `experimental.session.compacting` | `output.context[]` or `output.prompt`, which replaces the default prompt. |
| `experimental.compaction.autocontinue` | `output.enabled`. |
| `experimental.text.complete` | Post-process completed text. |

Source: [SRC packages/plugin/src/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts); [REL v1.15.11](https://github.com/anomalyco/opencode/releases/tag/v1.15.11)

**Bus events for the `event` hook**

| Group | Events |
| --- | --- |
| command | `command.executed` |
| file | `file.edited`, `file.watcher.updated` |
| installation | `installation.updated` |
| LSP | `lsp.client.diagnostics`, `lsp.updated` |
| message | `message.part.removed`, `message.part.updated`, `message.removed`, `message.updated` |
| permission | `permission.asked`, `permission.replied` |
| server | `server.connected` |
| session | `session.created`, `session.compacted`, `session.deleted`, `session.diff`, `session.error`, `session.idle`, `session.status`, `session.updated` |
| todo | `todo.updated` |
| shell | `shell.env` |
| tool | `tool.execute.before`, `tool.execute.after` |
| TUI | `tui.prompt.append`, `tui.command.execute`, `tui.toast.show` |

Source: [Plugins – Events](https://opencode.ai/docs/plugins/)

**Other plugin notes**
- Use `client.app.log({ body: {service, level, message, extra} })` for structured logs. A plugin tool with the same name as a built-in wins. — [Plugins](https://opencode.ai/docs/plugins/)
- V2 plugin API, added in v1.17.10:
  - Import `define({ id, setup: async (ctx) => {…} })` from `@opencode-ai/plugin/v2/promise`, or the Effect variant from `/v2/effect`.
  - `setup` registers hooks imperatively and does not return a hook object.
  - Options are available as `ctx.options`.
  - Transform hooks: `ctx.agent|catalog|command|integration|reference|skill.transform`.
  - Runtime hooks include `ctx.aisdk.sdk`.
  - Registrations can be removed with `dispose()`.

  Source: [SRC packages/plugin/src/v2/promise/README.md](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/v2/promise/README.md); [REL v1.17.10](https://github.com/anomalyco/opencode/releases/tag/v1.17.10)
- TUI plugins: `@opencode-ai/plugin/tui` exports types built on OpenTUI (Solid renderables, keymaps, slots), and `tui.json` accepts plugin specs. — [SRC packages/plugin/src/tui.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/tui.ts); [SRC config/tui.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/tui.ts)
- Since v1.17.7, environment variables from `shell.env` also apply to PTY sessions. — [REL v1.17.7](https://github.com/anomalyco/opencode/releases/tag/v1.17.7)

Minimal example:
```ts
// .opencode/plugins/guard.ts
import type { Plugin } from "@opencode-ai/plugin"
export const Guard: Plugin = async ({ $ }) => ({
  "tool.execute.before": async (input, output) => {
    if (input.tool === "read" && output.args.filePath.includes(".env")) throw new Error("no .env")
  },
  event: async ({ event }) => { if (event.type === "session.idle") await $`say done` },
})
```

### Inferences
- The docs page covers only the V1 hooks-object API. The V2 API (`define` with transforms) is documented only in the package README, so it should be treated as newer and less stable.

### Gaps
- The user docs do not cover the TUI plugin API. Only the type exports were confirmed.
- The `auth` and `provider` hook shapes were not explored in depth.

---

## Workflows/automation: `opencode run`, server/SDK, GitHub agent, sharing

### Takeaway
- **Scripting:** `opencode run` is the non-interactive entry point. It takes flags for agent, model, command, files, JSON output, `--auto`, and attaching to a running server.
- **Server and SDK:** `opencode serve` exposes an OpenAPI 3.1 HTTP server (the TUI is itself a client of this server), and `@opencode-ai/sdk` wraps it.
- **CI:** the GitHub Action `anomalyco/opencode/github@latest` responds to `/opencode` or `/oc` comments and other events.
- **Sharing:** set with `share` (`manual`, `auto`, `disabled`).

### Cited Findings

**`opencode run`**
- Flags:
  - Session: `--continue/-c`, `--session/-s`, `--fork`
  - Prompt: `--command`, `--file/-f`, `--title`
  - Model and agent: `--model/-m`, `--agent`, `--variant`, `--thinking`
  - Output: `--format default|json` (json gives raw events), `--share`
  - Server: `--attach <url>`, `--password/-p`, `--username/-u`, `--dir`, `--port`
  - Permissions: `--auto`
- `--attach` reuses a warm `opencode serve` instance and avoids MCP cold starts.

Source: [CLI – run](https://opencode.ai/docs/cli/)
- Since v1.18.20, `opencode run` answers permission requests raised by subagents. — [REL v1.18.20](https://github.com/anomalyco/opencode/releases/tag/v1.18.20)
- Other CLI commands: `tui` (default), `attach`, `auth`, `agent`, `github install|run`, `mcp`, `models`, `serve`, `web`, `acp` (Agent Client Protocol over stdio nd-JSON), `session list|delete`, `stats`, `export [--sanitize]`, `import <file|share-url>`, `plugin`, `pr <number>`, `db`, `debug`, `upgrade`, `uninstall`. Global flags: `--print-logs`, `--log-level`, `--pure`. — [CLI](https://opencode.ai/docs/cli/)

**Server**
- `opencode serve` flags:

  | Flag | Default |
  | --- | --- |
  | `--port` | 4096 |
  | `--hostname` | 127.0.0.1 |
  | `--mdns` | — |
  | `--mdns-domain` | — |
  | `--cors` | repeatable |

- HTTP basic auth is enabled by `OPENCODE_SERVER_PASSWORD`; the username defaults to `opencode`.
- The OpenAPI 3.1 spec is served at `/doc`.
- Endpoint groups: `/global/health`, `/global/event` (SSE), `/project`, `/config` (GET and PATCH), `/provider`, `/session` (CRUD, children, todo, prompt, …), and `/tui` for driving the TUI (used by IDE plugins).

Source: [Server](https://opencode.ai/docs/server/)

**SDK**
- Install with `npm install @opencode-ai/sdk`.
- `createOpencode({hostname, port, signal, timeout, config})` starts a server and a client. Inline `config` overrides `opencode.json`.
- `createOpencodeClient({baseUrl, fetch, parseAs, responseStyle, throwOnError})` connects to an existing server.
- Types are generated from OpenAPI.
- Structured output: `session.prompt({ body: { parts, format: { type: "json_schema", schema, retryCount? } } })`. The result is in `info.structured_output`; failure produces a `StructuredOutputError`.

Source: [SDK](https://opencode.ai/docs/sdk/)

**GitHub integration**
- `opencode github install` sets up the GitHub app, the workflow, and secrets. — [GitHub](https://opencode.ai/docs/github/)
- Manual setup: install github.com/apps/opencode-agent, add `.github/workflows/opencode.yml` using `anomalyco/opencode/github@latest`, and grant `id-token: write`. — [GitHub](https://opencode.ai/docs/github/)
- Action inputs:
  - `model`: required.
  - `agent`: must be a primary agent; falls back to `default_agent` or `build`.
  - `share`: defaults to true for public repos.
  - `prompt`
  - `mentions`: default `/opencode,/oc`.
  - `variant`
  - `oidc_base_url`
  - `use_github_token`: uses the caller's `GITHUB_TOKEN` and skips both the OIDC exchange and the app.

  Source: [GitHub](https://opencode.ai/docs/github/)
- Supported events: `issue_comment`, `pull_request_review_comment`, `issues`, `pull_request`, `schedule`, `workflow_dispatch`. `issues`, `schedule`, and `workflow_dispatch` require `prompt`. — [GitHub](https://opencode.ai/docs/github/)
- A GitLab integration also exists (gitlab.mdx in the docs). — [GitLab](https://opencode.ai/docs/gitlab/)

**Sharing**
- `share`: `manual` (default; use `/share`), `auto`, or `disabled`.
- Links have the form `opncd.ai/s/<id>` and are public to anyone with the link. `/unshare` removes the link.
- `OPENCODE_AUTO_SHARE` is the env equivalent of `auto`.
- The `autoshare` boolean is deprecated in favor of `share`.

Source: [Share](https://opencode.ai/docs/share/); [CLI](https://opencode.ai/docs/cli/); [SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)

Minimal example:
```bash
opencode run --agent plan --format json --auto "Summarize open TODOs"
opencode serve --port 4096 &  opencode run --attach http://localhost:4096 --command review
```

### Gaps
- The full HTTP route list in server.mdx (message, file, find, event, and tui routes) was only partly read here.
- SDK v2 (`@opencode-ai/sdk/v2`, used by the plugin types) is not covered in the user docs page.
