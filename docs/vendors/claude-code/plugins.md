# Plugins

A plugin is a directory that packages Claude Code extensions for distribution: skills, legacy commands, subagents, hooks, MCP servers, LSP servers, output styles, workflows, themes, monitors, `bin/` executables, and default settings. Its components are namespaced as `plugin:component`, so they do not collide with each other or with local configuration. Plugins are distributed through marketplaces (a `marketplace.json` catalog) and installed at user, project, or local scope ([plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference); [marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference); [plugin install](https://code.claude.com/docs/en/plugins/install)). The plugin system was released in v2.0.12 ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).

## Locations and scopes

### Install scopes

| Scope | Writes `enabledPlugins` to | Effect |
| :- | :- | :- |
| User (CLI default) | `~/.claude/settings.json` | You, all projects |
| Project | `.claude/settings.json` | Enables the plugin for collaborators, but each still has to install it |
| Local | `.claude/settings.local.json` | You, this project |

Source: [plugin install](https://code.claude.com/docs/en/plugins/install)

- Precedence is local > project > user. A managed `enabledPlugins: false` blocks installation at every scope ([plugin install](https://code.claude.com/docs/en/plugins/install); [settings reference](https://code.claude.com/docs/en/settings-reference)).
- `--add-dir` directories also load the `enabledPlugins`/`extraKnownMarketplaces` keys ([permissions](https://code.claude.com/docs/en/permissions)).

### On disk

- Plugin root: `~/.claude/plugins` (override with `CLAUDE_CODE_PLUGIN_CACHE_DIR`). It contains `cache/<mkt>/<plugin>/<version>/`, `data/<id>/`, `marketplaces/<name>/`, `synced/`, `installed_plugins.json`, and `known_marketplaces.json` ([plugin loading](https://code.claude.com/docs/en/plugins/loading)).
- Session-only loading: `--plugin-dir <dir|zip>` (repeatable), `--plugin-url <zip-url>`, and `CLAUDE_CODE_PLUGIN_DIRS`. These appear as `<name>@inline` and shadow installed plugins of the same name. The managed `disableSideloadFlags` setting blocks them ([plugin CLI](https://code.claude.com/docs/en/plugins/cli-reference); [plugin loading](https://code.claude.com/docs/en/plugins/loading)).
- Skill folders as plugins: adding `.claude-plugin/plugin.json` to a skill folder turns it into a plugin named `<name>@skills-dir`. `claude plugin init <name>` scaffolds at `~/.claude/skills/<name>/`, which auto-loads as `<name>@skills-dir` ([skills](https://code.claude.com/docs/en/skills); [marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference); local CLI help).
- Special marketplace names: `inline`, `builtin`, `skills-dir`, `synced` ([marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference)).

### Name-conflict order

managed-locked > `--plugin-dir`/`--plugin-url` > installed marketplace > skills-dir (`~/.claude/skills/` beats project `.claude/skills/`) > synced from claude.ai ([plugin loading](https://code.claude.com/docs/en/plugins/loading)).

### Governance settings

From the [settings reference](https://code.claude.com/docs/en/settings-reference):

| Key | Scope | Effect |
| :- | :- | :- |
| `enabledPlugins` | Any | `{"name@marketplace": bool}` |
| `extraKnownMarketplaces` | Any; needs workspace trust | Register marketplaces for a repo or org |
| `strictKnownMarketplaces` | Managed | Marketplace allowlist |
| `blockedMarketplaces` | Managed | Marketplace denylist |
| `strictPluginOnlyCustomization` | Managed | Named in the reference; effect not recorded |
| `pluginTrustMessage` | Managed | Named in the reference; effect not recorded |
| `disableCommandPluginSources` | Managed | Named in the reference; effect not recorded |
| `disableSideloadFlags` | Managed | Blocks `--plugin-dir`, `--plugin-url`, `CLAUDE_CODE_PLUGIN_DIRS` |
| `syncClaudeAiPlugins` | Any; `false` from a lower scope beats managed | claude.ai plugin sync ([settings](https://code.claude.com/docs/en/settings)) |

## Format

### Standard layout

```
my-plugin/
├── .claude-plugin/plugin.json   # manifest (optional; only file in .claude-plugin/)
├── skills/<name>/SKILL.md
├── commands/                    # legacy; prefer skills
├── agents/
├── hooks/hooks.json
├── .mcp.json
├── .lsp.json
├── output-styles/
├── workflows/
├── themes/
├── monitors/monitors.json
├── bin/                         # added to the Bash PATH
└── settings.json                # default settings
```

Source: [plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference)

- A CLAUDE.md at the plugin root is not loaded; put instructions in a skill ([plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference)).
- Plugin components link to their own pages: [skills.md](skills.md), [commands.md](commands.md), [subagents.md](subagents.md), [hooks.md](hooks.md), [mcp.md](mcp.md), [configuration.md](configuration.md#output-styles) (output styles), [automation.md](automation.md#dynamic-workflows) (workflows).
- Channels (research preview) are MCP servers that push events into a running session ([channels](https://code.claude.com/docs/en/channels)).

### plugin.json fields

From the [plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference):

| Field | Meaning | Default |
| :- | :- | :- |
| `name` | Required; kebab-case. Reserved prefixes such as `claude-` and `anthropic-` are rejected by validate | — |
| `displayName` | Display name | — |
| `version` | Version string; pins users until changed | Source-derived |
| `description` | Description | — |
| `author` | `{name, email, url}` | — |
| `homepage`, `repository`, `license`, `keywords`, `metadata` | Metadata | — |
| `icon`, `documentationUrl`, `supportUrl`, `privacyPolicyUrl`, `termsOfServiceUrl` | Directory listing fields; Claude Code ignores them | — |
| `defaultEnabled` | Enabled after install | `true` |
| `dependencies` | `"name"`, `"name@mkt"`, or `{name, marketplace, version}` | — |
| `settings` | Default settings; only `agent` and `subagentStatusLine` take effect | — |
| `userConfig` | Options of type `string`, `number`, `boolean`, `directory`, `file`; option fields `title`, `description`, `required`, `default`, `options`, `multiple`, `sensitive`, `min`/`max` | — |
| `channels`, `types` | Channel and type declarations | — |
| `skills` | Path(s); adds to the default `skills/` | `skills/` |
| `commands` | Path(s) or inline map; replaces the default directory | `commands/` |
| `agents` | Path(s); replaces the default directory | `agents/` |
| `outputStyles` | Path(s); replaces the default directory | `output-styles/` |
| `workflows` | Path(s); replaces the default directory | `workflows/` |
| `hooks` | Path or inline; merges with `hooks/hooks.json` | `hooks/hooks.json` |
| `mcpServers` | Path, `.mcpb`/`.dxt` bundle, or inline; merges with `.mcp.json` | `.mcp.json` |
| `lspServers` | Merges with `.lsp.json` | `.lsp.json` |
| `experimental.themes`, `experimental.monitors`, `experimental.evals` | Experimental components | — |

- `userConfig` values are stored under `pluginConfigs` in settings (confirmed only from the settings index) and passed to hooks as `CLAUDE_PLUGIN_OPTION_<KEY>` ([plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference); [settings reference](https://code.claude.com/docs/en/settings-reference)).
- Inline command form: `"commands": {"about": {"content": "...", "description": "..."}}` ([plugin components](https://code.claude.com/docs/en/plugins/components)).

### Path variables

| Variable | Resolves to |
| :- | :- |
| `${CLAUDE_PLUGIN_ROOT}` | The installed version directory (`~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`); changes on every update, so do not write state there |
| `${CLAUDE_PLUGIN_DATA}` | `~/.claude/plugins/data/<id>/`; persists across updates; deleted on last uninstall unless `--keep-data` |
| `${CLAUDE_PROJECT_DIR}` | The project root |

Source: [plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference)

- The variables resolve inline in hook `command`/`args`, MCP `command`/`args`/`env`/`url`/`headers`, LSP fields, and skill, agent, and command Markdown bodies. They are not present in Bash tool commands ([plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference)).

### marketplace.json

Location: `<root>/.claude-plugin/marketplace.json`. Relative plugin sources resolve from the marketplace root ([marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference)).

Top-level fields:

| Field | Meaning |
| :- | :- |
| `name` | Required. Many official names are reserved, and `claudeai-*` is reserved |
| `owner` | Required; `{name, email?, url?}` |
| `plugins` | Required; list of plugin entries |
| `description`, `version` | Metadata |
| `metadata.pluginRoot` | Base directory for plugin sources (v2.1.239+) |
| `forceRemoveDeletedPlugins` | Remove plugins deleted from the catalog |
| `allowCrossMarketplaceDependenciesOn` | Allow dependencies on other marketplaces |
| `renames` | Plugin renames |

Plugin entry fields:

| Field | Meaning | Default |
| :- | :- | :- |
| `name` | Required | — |
| `source` | Required; see source types | — |
| `description` | Description | — |
| `version` | `plugin.json` wins if both are set | — |
| `category`, `tags`, `relevance` | Discovery metadata | — |
| `strict` | `true`: `plugin.json` is authoritative and the entry's components are appended. `false` with component fields in both places is a "conflicting manifests" error. Without `plugin.json`, the entry is the manifest | `true` |
| `dependencies`, `defaultEnabled`, `displayName`, `metadata` | As in `plugin.json` | — |
| `headers`, `headersHelper` | Request headers for fetching | — |
| Any `plugin.json` field | An entry can carry any manifest field | — |

Source: [marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference)

Plugin source types:

| Type | Fields |
| :- | :- |
| Relative path | `"./..."` |
| `github` | `repo`, `ref`, `sha` |
| `url` (git) | `url`, `ref`, `sha` |
| `git-subdir` | `url`, `path`, `ref`, `sha` |
| `npm` | `package`, `version`, `registry` |
| `archive` (v2.1.224+) | `url`, `sha256` |
| `command` (v2.1.229+) | `command`, `timeout`, `mode` |

Source: [marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference)

Marketplace source types (in `extraKnownMarketplaces` and the policy lists): `github{repo,ref,path,sparsePaths}`, `git{url,...}`, `url` (a direct `marketplace.json` link, with `headers`), `file`, `directory`, and `settings` (an inline catalog). `hostPattern` and `pathPattern` are valid only in `strictKnownMarketplaces`/`blockedMarketplaces` ([marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference)).

### Versioning

- Resolution order: manifest `version` > marketplace entry `version` > source-derived (12-character commit SHA, sha256, or `unknown`) ([plugin loading](https://code.claude.com/docs/en/plugins/loading)).
- Pinning `version` freezes users until it changes ([plugin loading](https://code.claude.com/docs/en/plugins/loading)). Inference (from the research notes): omitting `version` lets users track commits; setting it makes updates explicit.
- Auto-update is on by default only for official marketplaces and claude.ai-added ones; everything else is off. Toggle per marketplace in the `/plugin` Marketplaces tab. `FORCE_AUTOUPDATE_PLUGINS=1` forces updates even with `DISABLE_AUTOUPDATER` ([plugin install](https://code.claude.com/docs/en/plugins/install); [env vars](https://code.claude.com/docs/en/env-vars)).

### Mods

- v2.1.287 added "Claude Mods": plugins with JavaScript function hooks that can draw UI and answer `tool.check` ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md); [hooks reference](https://code.claude.com/docs/en/hooks)).
- Mods answering `tool.check` can override ask rules and non-managed hook blocks ([permissions](https://code.claude.com/docs/en/permissions)).
- `claude plugin test` tests mods (local CLI help; [plugin CLI](https://code.claude.com/docs/en/plugins/cli-reference)).

## Loading and invocation

### Commands

Shell (local CLI help; [plugin CLI](https://code.claude.com/docs/en/plugins/cli-reference)):

| Command | Purpose |
| :- | :- |
| `claude plugin install\|i <plugin[@mkt]> [-s user\|project\|local] [--config k=v] [-y] [--json]` | Install |
| `uninstall [--keep-data]` | Uninstall |
| `enable`, `disable` | Toggle |
| `update` | Update; restart or `/reload-plugins` to apply |
| `list [--json]` | List |
| `details` | Component inventory and projected token cost |
| `configure` | Set `userConfig` options |
| `prune`, `tag` | Maintenance |
| `validate [--strict]` | Authoritative check; since v2.1.281 also checks MCP entries |
| `init\|new` | Scaffold |
| `eval` | Plugin eval suites |
| `test` | Mods |
| `claude plugin marketplace add <source> [--scope] [--sparse] [--claudeai]` | Add a marketplace |
| `claude plugin marketplace list`, `remove\|rm`, `update [name]` | Manage marketplaces |

In session: `/plugin` (Discover, Installed, Marketplaces, and Errors tabs, plus subcommands), `/plugin marketplace add owner/repo[#ref]`, `/plugin install name --marketplace <source>` (v2.1.275+), and `/reload-plugins [--force]` ([plugin CLI](https://code.claude.com/docs/en/plugins/cli-reference); [plugin install](https://code.claude.com/docs/en/plugins/install)).

### Context cost

- Plugin components load like their local counterparts: skill listings and agent descriptions at startup, skill bodies on invocation, MCP tools through tool search. See [skills.md](skills.md#discovery-and-context-cost), [subagents.md](subagents.md#context-cost), [mcp.md](mcp.md#loading-and-invocation).
- `claude plugin details` shows a plugin's projected token cost ([plugin CLI](https://code.claude.com/docs/en/plugins/cli-reference)).

### Naming inside a session

- Skills: `/plugin-name:skill-name`; commands: `/<plugin>:<file>` ([skills](https://code.claude.com/docs/en/skills); [plugin components](https://code.claude.com/docs/en/plugins/components)).
- Agents: `@agent-<plugin>:<name>`; subfolders become part of the ID, e.g. `my-plugin:review:security` ([subagents](https://code.claude.com/docs/en/sub-agents)).
- MCP tools: `mcp__plugin_<plugin>_<server>__<tool>`; server registered as `plugin:<plugin>:<server>` ([MCP](https://code.claude.com/docs/en/mcp)).

### Recommending plugins to a team

Inference (from the research notes): a project-scope `enabledPlugins` entry plus `extraKnownMarketplaces` in a committed `.claude/settings.json` is the documented way to recommend plugins to a team. Each member still has to trust the folder and install the plugin.

## Example

Minimal plugin ([plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference)):

```
my-plugin/.claude-plugin/plugin.json   -> {"name":"my-plugin","version":"0.1.0","description":"..."}
my-plugin/skills/hello/SKILL.md
```

Minimal marketplace, `.claude-plugin/marketplace.json` (shape from the [marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference)):

```json
{"name":"team-tools","owner":{"name":"Team"},"plugins":[{"name":"my-plugin","source":"./plugins/my-plugin"}]}
```

Add it with `claude plugin marketplace add ./path` or `owner/repo`, then run `claude plugin install my-plugin@team-tools --scope project`.

## Limits and gotchas

- Validation: unknown top-level keys in `plugin.json` are stripped with a warning. Unknown keys inside `userConfig`, `channels`, `lspServers`, or `monitors` are errors that stop the plugin loading ([plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference)).
- Plugin agents ignore `hooks`, `mcpServers`, `permissionMode`, and `initialPrompt` for security ([subagents](https://code.claude.com/docs/en/sub-agents); [plugin components](https://code.claude.com/docs/en/plugins/components)).
- `skillOverrides` does not apply to plugin skills ([skills](https://code.claude.com/docs/en/skills)).
- `settings.json` in a plugin: only `agent` and `subagentStatusLine` take effect ([plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference)).
- `${CLAUDE_PLUGIN_ROOT}` changes on every update; write state to `${CLAUDE_PLUGIN_DATA}` ([plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference)).
- Project-scope install enables but does not install the plugin for collaborators ([plugin install](https://code.claude.com/docs/en/plugins/install)).
- `managed-mcp.json` blocks plugin MCP servers ([managed MCP](https://code.claude.com/docs/en/managed-mcp)).
- `allowManagedHooksOnly` blocks plugin hooks ([hooks reference](https://code.claude.com/docs/en/hooks)).
- `force-for-plugin` in a plugin output style overrides the user's `outputStyle` ([output styles](https://code.claude.com/docs/en/output-styles)).
- Recent changes: `claude plugin configure` and `install --config` arrived around v2.1.281–2.1.282; mods arrived in v2.1.287 ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- Doc URL change: the old URLs `/docs/en/plugins`, `/plugins-reference`, `/plugin-marketplaces`, and `/discover-plugins` now serve the new `/docs/en/plugins/*` pages (observed on 2026-10-04) ([plugins overview](https://code.claude.com/docs/en/plugins/overview)).
- Gap (research notes): the plugin `components` page, the dependencies page, the mods reference, and the org-management page were not read in detail. The `userConfig` storage location (`pluginConfigs`) was confirmed only from the settings index.
- Gap (research notes): the effects of `strictPluginOnlyCustomization`, `pluginTrustMessage`, and `disableCommandPluginSources` are not described in the notes beyond their names.

## Sources

- https://code.claude.com/docs/en/plugins/manifest-reference
- https://code.claude.com/docs/en/plugins/marketplace-reference
- https://code.claude.com/docs/en/plugins/install
- https://code.claude.com/docs/en/plugins/cli-reference
- https://code.claude.com/docs/en/plugins/loading
- https://code.claude.com/docs/en/plugins/overview
- https://code.claude.com/docs/en/plugins/components
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/settings-reference
- https://code.claude.com/docs/en/permissions
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/managed-mcp
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/output-styles
- https://code.claude.com/docs/en/env-vars
- https://code.claude.com/docs/en/channels
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- Local CLI help: `claude plugin --help`, `claude plugin install --help`, `claude plugin marketplace add --help` (v2.1.289)
