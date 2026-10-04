# Plugins

A plugin is a versioned bundle of harness extensions (skills, hooks, MCP server definitions, plus vendor-specific components) that is listed in a marketplace catalog, installed into a local cache, and enabled by ID in configuration. It solves distribution: one install and update path delivers the same set of extensions to many users and repositories.

**Scope of this page.** Claude Code and Codex use "plugin" for this bundle-and-marketplace concept. OpenCode uses the word for something else: a JavaScript or TypeScript module that registers hooks, custom tools, auth methods, and providers, loaded from a directory or from npm, with no marketplace and no bundled skills ([OC](../vendors/opencode/plugins.md)). That is closer to hooks and custom tools than to a distribution bundle. This page follows the lead definition and lists OpenCode in the comparison only where a counterpart exists.

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Unit | Directory with optional manifest ([CC](../vendors/claude-code/plugins.md#standard-layout)) | Directory with manifest ([Codex](../vendors/codex/plugins.md#plugin-layout)) | JS/TS module or npm package ([OC](../vendors/opencode/plugins.md#v1-plugin-api-hooks-object)) |
| Manifest location | `.claude-plugin/plugin.json`; optional ([CC](../vendors/claude-code/plugins.md#standard-layout)) | Root `plugin.json`; `.codex-plugin/plugin.json` as compatibility fallback ([Codex](../vendors/codex/plugins.md#plugin-layout)) | None; config entry is a spec string or `[spec, options]` ([OC](../vendors/opencode/plugins.md#v1-plugin-api-hooks-object)) |
| Manifest schema | Vendor schema; only `name` required (kebab-case); reserved prefixes `claude-`, `anthropic-` ([CC](../vendors/claude-code/plugins.md#pluginjson-fields)) | Cross-vendor "Agent Plugins" schema `agent-plugins.org/schemas/1.0.0`; `name` (kebab-case), `version`, `description`, author; vendor block `extensions.com.openai` ([Codex](../vendors/codex/plugins.md#pluginjson)) | — |
| Shared components | `skills/`, `hooks/hooks.json`, `.mcp.json` ([CC](../vendors/claude-code/plugins.md#standard-layout)) | `skills/`, `hooks/` (`hooks/hooks.json`), `mcp.json` ([Codex](../vendors/codex/plugins.md#plugin-layout)) | Hooks and tools in code ([OC](../vendors/opencode/plugins.md#format)) |
| Other components | `commands/`, `agents/`, `.lsp.json`, `output-styles/`, `workflows/`, `themes/`, `monitors/`, `bin/`, `settings.json`, channels ([CC](../vendors/claude-code/plugins.md#standard-layout)) | `assets/`, apps (connectors), browser extensions ([Codex](../vendors/codex/plugins.md#plugin-layout)) | Custom tools, auth, providers, TUI plugins ([OC](../vendors/opencode/plugins.md#format)) |
| Plugin path variables | `${CLAUDE_PLUGIN_ROOT}` (versioned dir), `${CLAUDE_PLUGIN_DATA}` (persists across updates); resolved in hooks, MCP fields, LSP, skill/agent/command bodies ([CC](../vendors/claude-code/plugins.md#path-variables)) | Hooks get `PLUGIN_ROOT`, `PLUGIN_DATA`, and also `CLAUDE_PLUGIN_ROOT`, `CLAUDE_PLUGIN_DATA` for compatibility ([Codex](../vendors/codex/plugins.md#what-happens-on-install-and-load)) | `PluginInput` fields `directory`, `worktree` ([OC](../vendors/opencode/plugins.md#v1-plugin-api-hooks-object)) |
| Marketplace file | `<root>/.claude-plugin/marketplace.json` ([CC](../vendors/claude-code/plugins.md#marketplacejson)) | `.agents/plugins/marketplace.json` (repo), `~/.agents/plugins/marketplace.json` (personal); `.claude-plugin/marketplace.json` read as legacy-compatible ([Codex](../vendors/codex/plugins.md#marketplace-sources)) | None; npm specs in the `plugin` config key ([OC](../vendors/opencode/plugins.md#locations-and-scopes)) |
| Marketplace required fields | Top: `name`, `owner`, `plugins`; entry: `name`, `source` ([CC](../vendors/claude-code/plugins.md#marketplacejson)) | Top: `name`; entry: `name`, `source`, `policy.installation`, `policy.authentication`, `category` ([Codex](../vendors/codex/plugins.md#marketplace-file-marketplacejson)) | — |
| Plugin source types | Relative path string, `github`, `url`, `git-subdir`, `npm`, `archive`, `command` ([CC](../vendors/claude-code/plugins.md#marketplacejson)) | String path or `{source: "local", path}`, `url`, `git-subdir`, `npm` ([Codex](../vendors/codex/plugins.md#marketplace-file-marketplacejson)) | npm package or local path ([OC](../vendors/opencode/plugins.md#locations-and-scopes)) |
| Register a marketplace | `claude plugin marketplace add <source>`; `extraKnownMarketplaces` in settings (needs workspace trust) ([CC](../vendors/claude-code/plugins.md#commands)) | `codex plugin marketplace add <source>`; `[marketplaces.<name>]` in config ([Codex](../vendors/codex/plugins.md#cli-commands)) | — |
| Install | `claude plugin install <plugin@mkt> -s user\|project\|local`; `/plugin` ([CC](../vendors/claude-code/plugins.md#commands)) | `codex plugin add <plugin@mkt>`; `/plugins` ([Codex](../vendors/codex/plugins.md#cli-commands)) | `opencode plugin <module>`; or list in `plugin` key, installed with Bun at startup ([OC](../vendors/opencode/plugins.md#cli-and-switches)) |
| Cache | `~/.claude/plugins/cache/<mkt>/<plugin>/<version>/` ([CC](../vendors/claude-code/plugins.md#on-disk)) | `~/.codex/plugins/cache/<mkt>/<plugin>/<version>/` ([Codex](../vendors/codex/plugins.md#cache-and-config)) | `~/.cache/opencode/node_modules/` ([OC](../vendors/opencode/plugins.md#locations-and-scopes)) |
| Enablement | `enabledPlugins: {"name@mkt": bool}` in settings ([CC](../vendors/claude-code/plugins.md#governance-settings)) | `[plugins."name@mkt"] enabled` in config ([Codex](../vendors/codex/plugins.md#configtoml-keys)) | Presence in `plugin` key or `plugins/` dir ([OC](../vendors/opencode/plugins.md#locations-and-scopes)) |
| Scope precedence | local > project > user; managed `false` blocks everywhere ([CC](../vendors/claude-code/plugins.md#install-scopes)) | Trusted project > user > cloud > system ([Codex](../vendors/codex/plugins.md#cache-and-config)) | Global config, project config, global dir, project dir; same npm package/version loads once ([OC](../vendors/opencode/plugins.md#load-order)) |
| Project-scope effect | Enables for collaborators; each must still install ([CC](../vendors/claude-code/plugins.md#install-scopes)) | Trusted project config can define marketplaces and enable plugins ([Codex](../vendors/codex/plugins.md#limits-and-gotchas)) | Project `plugin` key installs at startup ([OC](../vendors/opencode/plugins.md#loading-and-invocation)) |
| Apply changes | `/reload-plugins` or restart ([CC](../vendors/claude-code/plugins.md#commands)) | New session ([Codex](../vendors/codex/plugins.md#what-happens-on-install-and-load)) | Startup ([OC](../vendors/opencode/plugins.md#loading-and-invocation)) |
| Plugin hook trust | Not recorded as separately gated | Not trusted on install; review with `/hooks` ([Codex](../vendors/codex/plugins.md#what-happens-on-install-and-load)) | Code runs at startup |
| Versioning | Manifest `version` > marketplace entry `version` > source-derived SHA; a set version pins users until it changes ([CC](../vendors/claude-code/plugins.md#versioning)) | `version` field; cache path is keyed by version ([Codex](../vendors/codex/plugins.md#cache-and-config)) | npm version ([OC](../vendors/opencode/plugins.md#load-order)) |
| Updates | `claude plugin update`; auto-update on by default only for official marketplaces ([CC](../vendors/claude-code/plugins.md#versioning)) | `codex plugin marketplace upgrade` ([Codex](../vendors/codex/plugins.md#cli-commands)) | Not recorded |
| Admin marketplace control | `strictKnownMarketplaces` (allowlist), `blockedMarketplaces` ([CC](../vendors/claude-code/plugins.md#governance-settings)) | `[marketplaces] restrict_to_allowed_sources`, `allowed_sources`; the OpenAI catalog must be listed explicitly ([Codex](../vendors/codex/plugins.md#admin-controls-requirementstoml)) | — |
| Admin component control | `managed-mcp.json` blocks plugin MCP; `allowManagedHooksOnly` blocks plugin hooks ([CC](../vendors/claude-code/plugins.md#limits-and-gotchas)) | Plugin MCP identity allowlist; `allow_managed_hooks_only` skips plugin hooks ([Codex](../vendors/codex/plugins.md#admin-controls-requirementstoml)) | — |
| Turn plugins off | `--safe-mode` ([CC instructions](../vendors/claude-code/instructions.md#related-settings-and-environment-variables)) | `features.plugins = false` ([Codex](../vendors/codex/plugins.md#configtoml-keys)) | `--pure` ([OC](../vendors/opencode/plugins.md#cli-and-switches)) |
| Namespacing | Skills `/plugin:skill`; agents `plugin:name`; MCP `mcp__plugin_<plugin>_<server>__<tool>` ([CC](../vendors/claude-code/plugins.md#naming-inside-a-session)) | Not recorded | Custom tools named after the file ([OC](../vendors/opencode/plugins.md#custom-tools)) |
| Surfaces without plugins | None recorded | IDE extension ([Codex](../vendors/codex/plugins.md#surfaces)) | — |

## Generalized model

**Plugin.** A directory with:

- A **manifest**: `name` (kebab-case, unique within a marketplace), `version`, `description`, author, and a vendor-specific extension block.
- **Components** in conventional subdirectories: skills (`skills/<name>/SKILL.md`), hooks (`hooks/hooks.json`), MCP server definitions (a JSON file at the plugin root). A harness may support more component types.

**Marketplace.** A catalog file in a git repository or local directory. It has a name and a list of entries; each entry has a plugin name, a source (relative path, git subdirectory, npm package, ...), and metadata.

**Plugin ID.** `<plugin>@<marketplace>`. Configuration refers to plugins only by this ID.

**Lifecycle.**

1. **Register** the marketplace, per user or in project config.
2. **Install**: the harness copies the plugin into a versioned cache, `<cache>/<marketplace>/<plugin>/<version>/`, and loads it from there, not from the source.
3. **Enable**: an `enabled` flag keyed by plugin ID in a config scope. Enable state follows configuration precedence; project beats user.
4. **Load**: at session start, components join their local counterparts (skills in the skill catalog, hooks in the hook table, servers in the MCP list). Changes need a new session or a reload command.
5. **Update**: refresh the marketplace; a new `version` gives a new cache directory.
6. **Uninstall.**

**Runtime paths.** Each plugin gets a root path (the versioned cache directory, replaced on update) and a data path (persists across updates). Hook commands receive both.

**Governance.** Administrators allowlist marketplace sources, and the MCP allowlist and "managed hooks only" switch apply to plugin components as they do to local ones.

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Plugin manifest | `.claude-plugin/plugin.json` | `plugin.json` | — |
| Skills component | `skills/` | `skills/` | — |
| Hooks component | `hooks/hooks.json` | `hooks/hooks.json` | Hooks object returned by the module |
| MCP component | `.mcp.json` or `mcpServers` | `mcp.json` | — |
| Marketplace file | `.claude-plugin/marketplace.json` | `.agents/plugins/marketplace.json` | — |
| Plugin ID | `name@marketplace` | `name@marketplace` | npm spec or file |
| Enable flag | `enabledPlugins` | `[plugins."<id>"] enabled` | `plugin` list |
| Plugin root path | `CLAUDE_PLUGIN_ROOT` | `PLUGIN_ROOT` (and `CLAUDE_PLUGIN_ROOT`) | — |
| Plugin data path | `CLAUDE_PLUGIN_DATA` | `PLUGIN_DATA` (and `CLAUDE_PLUGIN_DATA`) | — |
| Marketplace allowlist | `strictKnownMarketplaces` | `restrict_to_allowed_sources` + `allowed_sources` | — |

## Portability

One repository can serve as a marketplace for both leads, and one plugin directory can be loaded by both. Codex reads `.claude-plugin/marketplace.json` as a legacy-compatible source ([Codex](../vendors/codex/plugins.md#marketplace-sources)), and Codex sets the `CLAUDE_PLUGIN_*` variables for plugin hooks ([Codex](../vendors/codex/plugins.md#what-happens-on-install-and-load)). The pages do not record a test of the combined layout; treat the items below as the documented basis and verify in both harnesses.

Layout for a dual-harness plugin repository:

```text
<repo>/
├── .claude-plugin/marketplace.json   # read by Claude Code; read by Codex as legacy-compatible
└── plugins/my-plugin/
    ├── .claude-plugin/plugin.json    # Claude Code manifest
    ├── plugin.json                   # Codex manifest (Agent Plugins schema)
    ├── skills/<name>/SKILL.md        # same path in both
    └── hooks/hooks.json              # same path in both
```

Rules:

- **Marketplace entries: write the union of required fields.** Claude Code requires top-level `owner`; Codex requires `policy.installation`, `policy.authentication`, and `category` per entry. Use a relative string `source` such as `"./plugins/my-plugin"`, which both accept. Gap: the pages do not say whether Claude Code accepts unknown entry fields such as `policy`, or whether Codex skips entries from the legacy file that lack `policy`. Codex skips entries it cannot resolve ([Codex](../vendors/codex/plugins.md#marketplace-file-marketplacejson)).
- **Manifests: keep two files with the same `name`, `version`, `description`, and author.** Claude Code reads `.claude-plugin/plugin.json`; Codex reads root `plugin.json` or `.codex-plugin/plugin.json`. Gap: the pages do not say whether either harness reads the other's manifest location. The Claude Code manifest is optional and only `name` is required, so Claude Code can also load the default directories without it ([CC](../vendors/claude-code/plugins.md#pluginjson-fields)).
- **Names:** kebab-case, without the `claude-` or `anthropic-` prefix that Claude Code rejects.
- **Set `version` explicitly.** Claude Code pins users to it until it changes; Codex keys the cache directory by it.
- **Hook commands: use `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_PLUGIN_DATA}`.** Both leads provide them to plugin hooks. Codex requires manifest hook paths to start with `./` and stay inside the plugin root ([Codex](../vendors/codex/plugins.md#pluginjson)). Write persistent state to the data path; the root path changes on every update ([CC](../vendors/claude-code/plugins.md#path-variables)). Hook event compatibility is covered in [hooks](hooks.md).
- **MCP servers: the file name is unresolved.** Claude Code reads `.mcp.json` at the plugin root. The Codex plugin layout lists `mcp.json`, while the Codex MCP page refers to a plugin `.mcp.json` with camelCase OAuth keys `clientId`, `callbackUrl`, `callbackPort` ([Codex](../vendors/codex/mcp.md#plugin-bundled-servers)). This is a contradiction in the Codex docs. Inference: shipping both files with the same content covers both readings.
- **Enablement is per harness.** The ID `my-plugin@my-marketplace` is the same, but it goes into `enabledPlugins` in `.claude/settings.json` and into `[plugins."my-plugin@my-marketplace"] enabled = true` in `.codex/config.toml`.
- **OpenCode:** no marketplace or bundle. Inference: distribute the skills to OpenCode through its skill discovery paths instead (it reads `.claude/skills` and `.agents/skills`; see [skills](skills.md)).

Traps:

- **Claude Code project-scope install does not install.** It records the plugin as enabled for collaborators; each still runs the install ([CC](../vendors/claude-code/plugins.md#limits-and-gotchas)).
- **Both leads gate repository-supplied marketplaces on trust.** Claude Code `extraKnownMarketplaces` needs workspace trust; Codex reads project config only in trusted projects ([CC](../vendors/claude-code/plugins.md#governance-settings), [Codex](../vendors/codex/plugins.md#limits-and-gotchas)).
- **Codex plugin hooks are not trusted on install.** The user reviews them with `/hooks` ([Codex](../vendors/codex/plugins.md#limits-and-gotchas)).
- **Instructions do not travel in a plugin.** A `CLAUDE.md` at the plugin root is not loaded; put instructions in a skill ([CC](../vendors/claude-code/plugins.md#standard-layout)). The Codex pages list no instruction-file component either.
- **Components outside the shared set are ignored by the other harness.** Inference: Codex documents no `agents/`, `commands/`, or output-style components, so a Claude Code plugin's agents and commands do nothing in Codex. Codex plugin "commands" are mentioned only in a bundled reference and are unverified ([Codex](../vendors/codex/plugins.md#limits-and-gotchas)).
- **No plugins in the Codex IDE extension** ([Codex](../vendors/codex/plugins.md#limits-and-gotchas)).
- **Admin allowlists must name each marketplace.** Codex does not implicitly allow even the OpenAI-curated catalog ([Codex](../vendors/codex/plugins.md#admin-controls-requirementstoml)).

## Dropped from the generalization

- **Agents, commands, LSP servers, output styles, workflows, themes, monitors, `bin/`, plugin `settings.json`, channels** (Claude Code): the Codex plugin format has no such components.
- **Apps (connectors), assets, browser extensions** (Codex): the Claude Code plugin format has no such components.
- **`userConfig` options and `claude plugin configure`** (Claude Code): Codex plugins have no documented user options.
- **Plugin `dependencies`** (Claude Code): no Codex counterpart.
- **`strict` merge between manifest and marketplace entry** (Claude Code): no Codex counterpart.
- **Session-only loading, `--plugin-dir`, `--plugin-url`, `CLAUDE_CODE_PLUGIN_DIRS`** (Claude Code): Codex loads only installed, cached plugins.
- **Skill folders as plugins, `@skills-dir`** (Claude Code): no Codex counterpart.
- **Mods, JavaScript function hooks that draw UI** (Claude Code): no Codex counterpart. The OpenCode code-module plugin is the nearest analogue, which is not a lead.
- **Installation policy `AVAILABLE` / `INSTALLED_BY_DEFAULT` / `NOT_AVAILABLE` and `policy.authentication`** (Codex): Claude Code has `defaultEnabled`, which sets the state after install, not whether install happens. Different semantics.
- **Universal plugin directory shared with ChatGPT** (Codex): vendor platform feature.
- **Automatic updates per marketplace** (Claude Code): Codex documents only a manual `marketplace upgrade`.
- **`claude plugin validate`, `details` (token cost), `eval`, `test`** (Claude Code): no Codex tooling counterpart recorded.
- **Admin-set default enable state** (Codex system and cloud config): Claude Code managed settings enforce rather than default.
- **OpenCode code plugins: custom tools via `tool()`, V2 API, TUI plugins, auth and provider hooks** (OpenCode): a different concept; neither lead lets a plugin register tools in code.

## Sources

- [Claude Code: plugins](../vendors/claude-code/plugins.md)
- [Codex: plugins](../vendors/codex/plugins.md)
- [OpenCode: plugins](../vendors/opencode/plugins.md)
- [Codex: MCP](../vendors/codex/mcp.md)
- [Claude Code: instructions](../vendors/claude-code/instructions.md)
- [Claude Code README](../vendors/claude-code/README.md), [Codex README](../vendors/codex/README.md), [OpenCode README](../vendors/opencode/README.md)
