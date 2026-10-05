# Plugins and marketplaces

A plugin bundles skills, MCP servers, hooks, browser extensions, assets and optionally apps (connectors) into one installable unit. Plugins are distributed through marketplaces: the universal plugin directory that ChatGPT and Codex share, plus Git or local marketplaces that users or repositories add ([Plugins](https://developers.openai.com/codex/plugins); [Build plugins](https://developers.openai.com/codex/plugins/build)). Skills are the authoring format and plugins are how you distribute them beyond one repository ([Build skills](https://learn.chatgpt.com/docs/build-skills.md)).

## Locations and scopes

### Surfaces

Plugins work in the CLI (plugin browser) and in Codex in the desktop app. The IDE extension does not support plugins ([Plugins](https://developers.openai.com/codex/plugins); [Skill controls](https://learn.chatgpt.com/docs/enterprise/skills.md)). Skills bundled in plugins also work in ChatGPT Chat and Work on web, desktop and mobile ([Build skills](https://learn.chatgpt.com/docs/build-skills.md)).

### Marketplace sources

| Source | Location |
|---|---|
| Universal directory | Shared by ChatGPT and Codex ([Plugins](https://developers.openai.com/codex/plugins)) |
| OpenAI-curated catalog | `https://github.com/openai/plugins.git` ([Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)) |
| Repository marketplace | `$REPO_ROOT/.agents/plugins/marketplace.json` |
| Repository marketplace (legacy-compatible) | `$REPO_ROOT/.claude-plugin/marketplace.json` |
| Personal marketplace | `~/.agents/plugins/marketplace.json` |
| Added marketplaces | `codex plugin marketplace add <SOURCE>`; stored as `[marketplaces.<name>]` in `config.toml` |

Source: [Build plugins](https://developers.openai.com/codex/plugins/build) unless noted.

### Cache and config

- Installs go to `~/.codex/plugins/cache/$MARKETPLACE/$PLUGIN/$VERSION/` (`local` as the version for local plugins). Codex loads plugins from the cache ([Build plugins](https://developers.openai.com/codex/plugins/build)).
- Marketplaces can be defined in system, cloud-managed, user or trusted-project config. `[plugins."plugin@marketplace"] enabled` is read from the merged config, and trusted-project settings override user, cloud and system settings ([Config reference](https://developers.openai.com/codex/config-reference); [Build plugins](https://developers.openai.com/codex/plugins/build)).
- Cloud-managed and system config can set plugin default-enabled state; these are defaults, not enforced policy ([Config basics](https://developers.openai.com/codex/config-basic)).
- A local `~/.codex/config.toml` contains `[marketplaces.<name>] source_type/source` and `[plugins."frank@franks-ai-skills"] enabled` (local CLI, redacted inspection).

## Format

### Plugin layout

```text
my-plugin/
  plugin.json            # portable manifest
  skills/<name>/SKILL.md
  mcp.json
  hooks/                 # hooks/hooks.json
  assets/
  .codex-plugin/plugin.json   # older location; supported compatibility fallback
```

Source: [Build plugins](https://developers.openai.com/codex/plugins/build); [Package your plugin](https://developers.openai.com/plugins/build/plugins.md).

### `plugin.json`

| Field | Meaning |
|---|---|
| Schema | The manifest follows `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` (the cross-vendor "Agent Plugins" schema) |
| `name` | Kebab-case plugin name |
| `version` | Version |
| `description` | Description |
| author and similar metadata | Author information |
| `hooks` | Manifest hook entry; paths must start with `./` and stay inside the plugin root ([Hooks](https://learn.chatgpt.com/docs/hooks.md)) |
| `extensions.com.openai` | OpenAI-specific settings |

Source: [Build plugins](https://developers.openai.com/codex/plugins/build). The full field list of the schema is not recorded in the notes.

### Marketplace file (`marketplace.json`)

| Field | Meaning |
|---|---|
| `name` | Marketplace name |
| `interface.displayName` | Display name |
| `plugins[]` | Plugin entries |
| `plugins[].name` | Plugin name |
| `plugins[].source` | `{source: "local", path: "./..."}` or a string path; `{source: "url" \| "git-subdir", url, path, ref \| sha}`; `{source: "npm", package, version, registry}` |
| `plugins[].policy.installation` | Required. `AVAILABLE`, `INSTALLED_BY_DEFAULT` or `NOT_AVAILABLE` |
| `plugins[].policy.authentication` | Required. For example `ON_INSTALL` |
| `plugins[].category` | Required. Category |

Entries that cannot be resolved are skipped ([Build plugins](https://developers.openai.com/codex/plugins/build)).

### `config.toml` keys

| Key | Meaning |
|---|---|
| `[marketplaces.<name>] source_type` | `git` or `local` |
| `[marketplaces.<name>] source` | Path or Git URL |
| `[marketplaces.<name>] ref` | Git ref |
| `[marketplaces.<name>] sparse_paths` | Sparse checkout paths |
| `[plugins."<plugin>@<marketplace>"] enabled` | Enable or disable an installed plugin |
| `plugins."<p>@<m>".mcp_servers.<server>.enabled`, `enabled_tools`, `disabled_tools`, `default_tools_approval_mode`, `tools.<t>.approval_mode` | Control a plugin's MCP servers. The transport cannot be changed ([MCP](https://developers.openai.com/codex/mcp)) |
| `features.plugins` | `false` disables plugins, also for API-key sign-in ([Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)) |

Source: [Config reference](https://developers.openai.com/codex/config-reference) unless noted. Plugin `.mcp.json` OAuth settings use camelCase `clientId`, `callbackUrl`, `callbackPort` ([MCP](https://developers.openai.com/codex/mcp)).

### Admin controls (`requirements.toml`)

- `[marketplaces] restrict_to_allowed_sources = true` with `allowed_sources.<rule>`. A rule is `source = git` plus `url`/`ref`, a `host_pattern`, or `local` plus an absolute `path`. The OpenAI-curated catalog `https://github.com/openai/plugins.git` must be allowlisted explicitly ([Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)).
- `[plugins.<p>.mcp_servers.<s>.identity]` allowlists plugin MCP servers ([Config reference](https://developers.openai.com/codex/config-reference)); see [mcp.md](mcp.md).
- `allow_managed_hooks_only = true` skips plugin hooks ([Hooks](https://learn.chatgpt.com/docs/hooks.md)).

### Apps (connectors)

`features.apps` (stable, on) enables app (connector) integrations. App traffic is not governed by the command network proxy ([Config reference](https://developers.openai.com/codex/config-reference)).

| Key (`[apps._default]` or `[apps.<id>]`) | Meaning |
|---|---|
| `enabled` | Enable the app |
| `destructive_enabled` | Allow destructive tools |
| `open_world_enabled` | Allow open-world tools |
| `default_tools_enabled` | Default tool enablement |
| `default_tools_approval_mode` | `auto`, `prompt`, `writes` or `approve` |
| `approvals_reviewer` | Reviewer for this app's approvals |
| `tools.<tool>.enabled` | Per-tool enablement |
| `tools.<tool>.approval_mode` | Per-tool approval mode |

`requirements.toml` `apps.<id>.enabled = false` and per-tool `approval_mode` constrain these. `tool_suggest.discoverables` and `tool_suggest.disabled_tools` (entries with `type = "connector" | "plugin"` and `id`) control tool suggestions ([Config reference](https://developers.openai.com/codex/config-reference)). `/apps` inserts `$app-slug` into the prompt ([Slash commands](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)).

## Loading and invocation

### CLI commands

| Command | Purpose |
|---|---|
| `codex plugin add <PLUGIN[@MARKETPLACE]> [-m MARKETPLACE] [--json]` | Install a plugin |
| `codex plugin list [-m] [--json] [--available]` | List plugins |
| `codex plugin remove <PLUGIN[@MARKETPLACE]>` | Remove a plugin |
| `codex plugin marketplace add <SOURCE> [--ref REF] [--sparse PATH]... [--json]` | Add a marketplace. SOURCE is a local path, `owner/repo[@ref]`, an HTTPS Git URL or an SSH Git URL |
| `codex plugin marketplace list` | List marketplaces |
| `codex plugin marketplace upgrade [name]` | Upgrade marketplaces |
| `codex plugin marketplace remove <name>` | Remove a marketplace |
| `/plugins` (TUI) | Plugin browser, grouped by marketplace. Space toggles an installed plugin |

Sources: local CLI (`codex plugin ... --help`, 0.159.2); [Plugins](https://developers.openai.com/codex/plugins).

### What happens on install and load

- Start a new session after installing to use the bundled skills and tools ([Plugins](https://developers.openai.com/codex/plugins)).
- Codex loads plugins from the cache, not from the marketplace source ([Build plugins](https://developers.openai.com/codex/plugins/build)).
- Bundled skills are discovered with the other skills ([skills.md](skills.md)). Bundled MCP servers are controlled through the `plugins."<p>@<m>".mcp_servers.*` keys above ([mcp.md](mcp.md)).
- Bundled hooks are not trusted automatically on install; review them with `/hooks`. Plugin hooks receive `PLUGIN_ROOT` and `PLUGIN_DATA`, and Codex also sets `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` for compatibility ([Hooks](https://learn.chatgpt.com/docs/hooks.md)); see [hooks.md](hooks.md).

### Feature flags (local 0.159.2)

`plugins`, `remote_plugin` and `plugin_sharing` are stable and on. `recommended_plugins` is stable and off. `plugin_hooks` is removed.

## Example

```toml
# ~/.codex/config.toml
[plugins."my-plugin@local-repo"]
enabled = true
```

```sh
codex plugin marketplace add owner/repo --ref main && codex plugin add my-plugin@owner-marketplace
```

Sources: [Build plugins](https://developers.openai.com/codex/plugins/build); local CLI.

## Limits and gotchas

- **No plugins in the IDE extension** ([Plugins](https://developers.openai.com/codex/plugins)).
- **New session required** after install before bundled skills and tools are available.
- **Plugin hooks need trust** after install.
- **The OpenAI-curated catalog is not allowlisted implicitly** when an admin restricts marketplace sources.
- **Project trust gates plugins.** Inference: project `.codex/config.toml` can enable plugins and define marketplaces, so plugin activation from a repository depends on project trust.
- **Cross-vendor marketplaces.** Inference: Codex reads `.claude-plugin/marketplace.json` as a legacy-compatible source, and plugin manifests follow the cross-vendor "Agent Plugins" schema. One repository marketplace can potentially serve both Claude Code and Codex.
- **Compatibility fallback.** The older `.codex-plugin/plugin.json` remains supported as a fallback ([Build plugins](https://developers.openai.com/codex/plugins/build)) and is described as a compatibility overlay ([Package your plugin](https://developers.openai.com/plugins/build/plugins.md)).
- **Gap:** `policy.authentication` values beyond `ON_INSTALL` were not captured; the docs mention "on install or first use".
- **Gap:** no documented hard limits (plugin count, plugin size, number of MCP servers).
- **Gap:** `[apps]` IDs and how to discover them are not covered in the pages read.

## Sources

- https://developers.openai.com/codex/plugins
- https://developers.openai.com/codex/plugins/build
- https://developers.openai.com/plugins/build/plugins.md
- https://developers.openai.com/codex/config-reference
- https://developers.openai.com/codex/config-basic
- https://developers.openai.com/codex/enterprise/managed-configuration
- https://developers.openai.com/codex/mcp
- https://learn.chatgpt.com/docs/build-skills.md
- https://learn.chatgpt.com/docs/enterprise/skills.md
- https://learn.chatgpt.com/docs/hooks.md
- https://learn.chatgpt.com/docs/developer-commands.md?surface=cli
