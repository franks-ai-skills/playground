# Plugins

A plugin is a versioned bundle of harness extensions (skills, hooks, MCP server definitions, plus vendor-specific components) that is listed in a marketplace catalog, installed into a local cache, and enabled by ID in configuration. It solves distribution: one install and update path delivers the same set of extensions to many users and repositories.

Claude Code and Codex use "plugin" for this bundle-and-marketplace concept. OpenCode uses the word for a JavaScript or TypeScript module that registers hooks, custom tools, auth methods and providers, with no marketplace and no bundled skills ([OC](../vendors/opencode/plugins.md)). This page follows the lead definition and lists OpenCode only where a counterpart exists.

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Manifest | `.claude-plugin/plugin.json`, optional; only `name` required; prefixes `claude-`, `anthropic-` reserved ([CC](../vendors/claude-code/plugins.md#pluginjson-fields)) | Root `plugin.json` in the cross-vendor Agent Plugins schema; `.codex-plugin/plugin.json` as fallback ([Codex](../vendors/codex/plugins.md#pluginjson)) | None; config entry is a spec string ([OC](../vendors/opencode/plugins.md#v1-plugin-api-hooks-object)) |
| Shared components | `skills/`, `hooks/hooks.json`, `.mcp.json` ([CC](../vendors/claude-code/plugins.md#standard-layout)) | `skills/`, `hooks/hooks.json`, `mcp.json` ([Codex](../vendors/codex/plugins.md#plugin-layout)) | Hooks and tools in code ([OC](../vendors/opencode/plugins.md#format)) |
| Other components | `commands/`, `agents/`, LSP, output styles, `bin/`, monitors, themes, and more ([CC](../vendors/claude-code/plugins.md#standard-layout)) | `assets/`, apps (connectors), browser extensions ([Codex](../vendors/codex/plugins.md#plugin-layout)) | Custom tools, auth, providers ([OC](../vendors/opencode/plugins.md#format)) |
| Path variables | `${CLAUDE_PLUGIN_ROOT}` (versioned), `${CLAUDE_PLUGIN_DATA}` (persists) ([CC](../vendors/claude-code/plugins.md#path-variables)) | `PLUGIN_ROOT`, `PLUGIN_DATA`, plus `CLAUDE_PLUGIN_*` for compatibility ([Codex](../vendors/codex/plugins.md#what-happens-on-install-and-load)) | `directory`, `worktree` inputs ([OC](../vendors/opencode/plugins.md#v1-plugin-api-hooks-object)) |
| Marketplace file | `.claude-plugin/marketplace.json` ([CC](../vendors/claude-code/plugins.md#marketplacejson)) | `.agents/plugins/marketplace.json`; reads `.claude-plugin/marketplace.json` as legacy-compatible ([Codex](../vendors/codex/plugins.md#marketplace-sources)) | None; npm specs in config ([OC](../vendors/opencode/plugins.md#locations-and-scopes)) |
| Marketplace required fields | Top: `name`, `owner`, `plugins`; entry: `name`, `source` ([CC](../vendors/claude-code/plugins.md#marketplacejson)) | Entry: `name`, `source`, `policy.installation`, `policy.authentication`, `category` ([Codex](../vendors/codex/plugins.md#marketplace-file-marketplacejson)) | — |
| Install | `claude plugin install <plugin@mkt> -s user\|project\|local`; `/plugin` ([CC](../vendors/claude-code/plugins.md#commands)) | `codex plugin add <plugin@mkt>`; `/plugins` ([Codex](../vendors/codex/plugins.md#cli-commands)) | `plugin` key, installed with Bun at startup ([OC](../vendors/opencode/plugins.md#cli-and-switches)) |
| Cache | `~/.claude/plugins/cache/<mkt>/<plugin>/<version>/` ([CC](../vendors/claude-code/plugins.md#on-disk)) | `~/.codex/plugins/cache/<mkt>/<plugin>/<version>/` ([Codex](../vendors/codex/plugins.md#cache-and-config)) | `~/.cache/opencode/node_modules/` ([OC](../vendors/opencode/plugins.md#locations-and-scopes)) |
| Enablement | `enabledPlugins: {"name@mkt": bool}` ([CC](../vendors/claude-code/plugins.md#governance-settings)) | `[plugins."name@mkt"] enabled` ([Codex](../vendors/codex/plugins.md#configtoml-keys)) | Presence in `plugin` key or `plugins/` dir ([OC](../vendors/opencode/plugins.md#locations-and-scopes)) |
| Scope precedence | local > project > user; managed `false` blocks everywhere ([CC](../vendors/claude-code/plugins.md#install-scopes)) | Trusted project > user > cloud > system ([Codex](../vendors/codex/plugins.md#cache-and-config)) | Global and project config and dirs ([OC](../vendors/opencode/plugins.md#load-order)) |
| Versioning | Manifest `version` > marketplace entry `version` > source-derived SHA ([CC](../vendors/claude-code/plugins.md#versioning)) | `version` field keys the cache path ([Codex](../vendors/codex/plugins.md#cache-and-config)) | npm version ([OC](../vendors/opencode/plugins.md#load-order)) |
| Dependencies | `dependencies` with semver ranges; installed automatically ([CC](../vendors/claude-code/plugins.md#dependencies)) | None recorded | Not recorded |
| Updates | `claude plugin update`; auto-update on by default only for official marketplaces ([CC](../vendors/claude-code/plugins.md#versioning)) | `codex plugin marketplace upgrade` ([Codex](../vendors/codex/plugins.md#cli-commands)) | Not recorded |
| Plugin hook trust | No separate gate recorded | Not trusted on install; review with `/hooks` ([Codex](../vendors/codex/plugins.md#what-happens-on-install-and-load)) | Code runs at startup |
| Admin marketplace control | `strictKnownMarketplaces`, `blockedMarketplaces` ([CC](../vendors/claude-code/plugins.md#governance-settings)) | `restrict_to_allowed_sources`, `allowed_sources`; the OpenAI catalog must be listed ([Codex](../vendors/codex/plugins.md#admin-controls-requirementstoml)) | — |
| Admin component control | `managed-mcp.json` blocks plugin MCP; `allowManagedHooksOnly` blocks plugin hooks ([CC](../vendors/claude-code/plugins.md#limits-and-gotchas)) | Plugin MCP identity allowlist; `allow_managed_hooks_only` ([Codex](../vendors/codex/plugins.md#admin-controls-requirementstoml)) | — |
| Turn plugins off | `--safe-mode` ([CC](../vendors/claude-code/instructions.md#related-settings-and-environment-variables)) | `features.plugins = false` ([Codex](../vendors/codex/plugins.md#configtoml-keys)) | `--pure` ([OC](../vendors/opencode/plugins.md#cli-and-switches)) |
| Surfaces without plugins | None recorded | IDE extension ([Codex](../vendors/codex/plugins.md#surfaces)) | — |

## Generalized model

**Plugin.** A directory with a **manifest** (`name` in kebab-case and unique within a marketplace, `version`, `description`, author, a vendor extension block) and **components** in conventional subdirectories: skills (`skills/<name>/SKILL.md`), hooks (`hooks/hooks.json`), and MCP server definitions (a JSON file at the plugin root).

**Marketplace.** A catalog file in a git repository or local directory: a name and a list of entries, each with a plugin name, a source (relative path, git subdirectory, npm package) and metadata.

**Plugin ID.** `<plugin>@<marketplace>`. Configuration refers to plugins only by this ID.

**Lifecycle.**

1. **Register** the marketplace, per user or in project config.
2. **Install:** the harness copies the plugin into `<cache>/<marketplace>/<plugin>/<version>/` and loads it from there, not from the source.
3. **Enable:** an `enabled` flag keyed by plugin ID in a config scope; project beats user.
4. **Load:** at session start, components join their local counterparts (skill catalog, hook table, MCP list). Changes need a new session or a reload command.
5. **Update:** refresh the marketplace; a new `version` gives a new cache directory.
6. **Uninstall.**

**Runtime paths.** A root path (the versioned cache directory, replaced on update) and a data path (persists across updates). Hook commands receive both.

**Governance.** Administrators allowlist marketplace sources. The MCP allowlist and the "managed hooks only" switch apply to plugin components as they do to local ones.

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

## When to use it and when not

A plugin adds a manifest, a marketplace entry and a release process. That cost pays off only with reuse.

Use it when:

| Situation | Notes |
| --- | --- |
| A second repository or team needs the same setup | Claude Code's stated trigger ([Extend Claude Code](https://code.claude.com/docs/en/features-overview)). |
| The setup goes to others through a marketplace | One install and update path, versioned. |
| A role needs a curated set ("backend standard") | A bundle plugin that only declares dependencies (Claude Code); several entries or `INSTALLED_BY_DEFAULT` (Codex). |
| An organization must control what runs on developer machines | Private marketplace plus admin source allowlist. |

Do not use it when:

| Situation | Use instead | Cost or risk of a plugin here |
| --- | --- | --- |
| Only one repository needs the skills, hooks or MCP servers | Repo-local [skills](skills.md), [hooks](hooks.md), [MCP](mcp.md) config | Packaging overhead; the setup no longer changes together with the code. |
| Project instructions must travel | A skill inside the plugin, or [instructions](instructions.md) in the repository | A `CLAUDE.md` at the plugin root is not loaded; Codex lists no instruction component. |
| OpenCode must receive the same skills | OpenCode's skill discovery paths (`.claude/skills`, `.agents/skills`; see [skills](skills.md)) | OpenCode has no marketplace or bundle. |
| You need a setting to apply to every user | Managed [configuration](configuration.md) | A plugin's `settings.json` in Claude Code applies only `agent` and `subagentStatusLine`. |

## Approaches

**Single-purpose plugin in a marketplace.** One plugin per capability or integration. Fits a capability reused across repositories. Claude Code: `.claude-plugin/plugin.json`, `.mcp.json`, executables in `scripts/` referenced as `${CLAUDE_PLUGIN_ROOT}/scripts/<name>`; org sync rejects a top-level `bin/` ([Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace)). Codex: root `plugin.json` in the Agent Plugins schema with OpenAI settings under `extensions.com.openai`; new packages should use this portable format rather than `.codex-plugin/`; hook paths start with `./` and stay inside the plugin root ([Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)). Trade-off: independent versioning, review and admin control per plugin, but more entries to maintain.

**Suite through a bundle plugin (Claude Code).** A plugin with only `name` and `dependencies`; installing it installs the whole set. Dependencies are declared in `plugin.json` or the marketplace entry as a name, `name@marketplace`, or `{name, version, marketplace}` with a semver range. `claude plugin install`, `/reload-plugins`, marketplace auto-update and `claude plugin marketplace add` install missing dependencies. Ranges resolve against git tags `<plugin>--v<version>` created by `claude plugin tag`; for `npm`, `archive` and `command` sources the range is only checked at load time. Dependencies come from the same marketplace unless the root marketplace lists another in `allowCrossMarketplaceDependenciesOn` or the user already has the dependency enabled at the same scope. Otherwise the install is refused (dependency declared in the marketplace entry) or completes and the plugin fails to load (dependency declared in `plugin.json`). Overlapping ranges resolve to the highest version that satisfies all; non-overlapping ranges make the second install fail. `claude plugin prune` removes unneeded auto-installed dependencies ([Claude Code: dependencies](../vendors/claude-code/plugins.md#dependencies); [plugin dependencies](https://code.claude.com/docs/en/plugin-dependencies)). Codex has no dependency mechanism; list several entries or use `policy.installation: INSTALLED_BY_DEFAULT`. Trade-off: not portable to Codex.

**Dual-harness marketplace repository.** One repository that both leads read. Fits teams that use both leads. See [Portability](#portability). Trade-off: the combined layout is documented, not tested in the sources; only skills, hooks and MCP servers work in both.

**Internal marketplace with admin governance.** A private catalog plus managed policy that restricts sources and force-enables approved plugins. Claude Code hosts it on GitHub, another git host, a `marketplace.json` URL or a shared directory; private repositories use the user's git credentials (`gh auth setup-git`), since `marketplace.json` has no token field ([Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace)). Codex enables plugins in the repository's `.codex/config.toml`; `features.plugin_sharing = false` turns sharing off. Trade-off: release channels need two marketplaces, because Claude Code has no release-channel concept.

**Seeded plugins for containers and CI.** Claude Code reads a pre-populated, read-only `CLAUDE_CODE_PLUGIN_SEED_DIR` (auto-update forced off); `CLAUDE_CODE_SYNC_PLUGIN_INSTALL=1` makes a `-p` run wait for installs ([Plugins for orgs](https://code.claude.com/docs/en/plugins/org)). No Codex counterpart is recorded.

## Practices

1. **Package only when a second repository needs the setup.**
   - Why: a plugin's manifest, entry and release process cost more than repo-local config until there is reuse.
   - How: move skills, hooks and MCP definitions into a plugin directory; replace project-relative paths with `${CLAUDE_PLUGIN_ROOT}`.
   - Evidence: [Vendor] ([Extend Claude Code](https://code.claude.com/docs/en/features-overview)).
2. **Keep plugins single-purpose and compose suites.**
   - Why: admin force-enable and block work per plugin, not per skill; small plugins are easier to review and version.
   - How: Claude Code bundle plugins with `dependencies`; Codex multiple entries.
   - Evidence: [Vendor] ([plugin dependencies](https://code.claude.com/docs/en/plugin-dependencies)); the granularity rule is an inference in the [research notes](../research-notes/agent-harness-best-practices/mcp-plugins.md).
3. **Set `version` explicitly, in one place, and bump it on every release.**
   - Why: Claude Code users stay on their cached copy until the string changes; Codex keys its cache by version. If `version` is set in both `plugin.json` and the marketplace entry, `plugin.json` silently wins.
   - How: bump in the manifest; tag releases `<plugin>--v<version>`. Alternative in Claude Code: omit `version` everywhere to track commits.
   - Evidence: [Vendor] ([Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace); [Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)).
4. **Pin dependency ranges and third-party sources; keep auto-update off for marketplaces you do not control.**
   - Why: "If that release renames an MCP tool your plugin calls, your plugin breaks." Auto-update can replace files you reviewed, and background updates use stored git credentials without prompting.
   - How: `~2.1.0` ranges for patches only; `ref`/`sha` on entries, `sha256` on archive sources; Codex `codex plugin marketplace add owner/repo --ref <ref>`; pin MCP packages inside the plugin (see [MCP](mcp.md)).
   - Evidence: [Vendor] ([plugin dependencies](https://code.claude.com/docs/en/plugin-dependencies); [Plugins for orgs](https://code.claude.com/docs/en/plugins/org); [Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)).
5. **Put guidance in skills, executables in `scripts/`, state in the data path.**
   - Why: a `CLAUDE.md` at the plugin root is not loaded; org sync rejects a top-level `bin/`; the root path changes on every update.
   - How: `skills/<name>/SKILL.md`; `${CLAUDE_PLUGIN_ROOT}/scripts/<name>` in hooks and MCP commands; state under `${CLAUDE_PLUGIN_DATA}`.
   - Evidence: [Vendor] ([Claude Code: plugins](../vendors/claude-code/plugins.md#limits-and-gotchas); [Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace)).
6. **Never change a published plugin's `name`.**
   - Why: configuration and installs refer to `<plugin>@<marketplace>`.
   - How: change `displayName`; for a real rename use the append-only `renames` map. Keep the entry name equal to the manifest name.
   - Evidence: [Vendor] ([Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace)).
7. **Validate in CI.**
   - Why: a push without a version bump never reaches Claude Code users, and diverging manifests break one harness silently.
   - How: run `claude plugin validate .` and fail when the two manifests' versions differ. Codex has no `validate` command in the sources.
   - Evidence: [Vendor] `claude plugin validate` ([Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces)); the CI job is an inference.
8. **As an admin, allowlist marketplace sources and pair the allowlist with MCP and hook controls.**
   - Why: sideloaded MCP servers and hooks bypass a marketplace allowlist unless restricted separately.
   - How: Claude Code `strictKnownMarketplaces` (`[]` blocks all, including the official one), `blockedMarketplaces`, `enabledPlugins` (`true` force-enables, `false` blocks), `disableSideloadFlags` paired with `allowedMcpServers`, `allowManagedHooksOnly`. Codex `requirements.toml` `restrict_to_allowed_sources` with `allowed_sources`, plugin MCP identity under `plugins.<p>.mcp_servers.<s>.identity`, `allow_managed_hooks_only`.
   - Evidence: [Vendor] ([Plugins for orgs](https://code.claude.com/docs/en/plugins/org); [Codex managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration)).
9. **Review a third-party plugin's executable parts before install and after every update.**
   - Why: "A Claude Code plugin you install can execute arbitrary code on your machine with your user privileges." A marketplace name signals who publishes the catalog, not what the plugins do.
   - How: Claude Code: check the source with `claude plugin marketplace list`, read the `/plugin` "Will install" pane, `hooks/hooks.json`, `.mcp.json` and every file in `bin/`; `claude plugin details` lists components. Codex: review bundled hooks with `/hooks`. Apply the MCP server review from [MCP](mcp.md).
   - Evidence: [Vendor] ([Plugin security and trust](https://code.claude.com/docs/en/plugins/security); [Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)). OpenAI publishes no checklist beyond hook trust review.
10. **Review plugin-enabling config like code.**
    - Why: project-level config ran code before consent in older versions of both leads (see [Security](#security)).
    - How: review changes to `.claude/settings.json` (`extraKnownMarketplaces`, `enabledPlugins`) and `.codex/config.toml` (`[plugins.*]`, `[marketplaces.*]`) in code review.
    - Evidence: [Advisory] ([Check Point, Claude Code](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/); [Check Point, Codex](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/)).

## Security

A plugin is code and instructions that run with your user privileges. Hooks, MCP servers and mod processes run outside the sandbox, `bin/` joins the Bash PATH, and auto-update can replace files you reviewed ([Plugin security and trust](https://code.claude.com/docs/en/plugins/security)). Codex does not trust plugin hooks on install; no separate gate for Claude Code plugin hooks is recorded.

| Threat | Mitigation |
| --- | --- |
| Malicious or compromised plugin | Source allowlist in both leads; review before install |
| Update changes reviewed code | Pin `ref`/`sha`/`sha256`; auto-update only for internal marketplaces |
| Lookalike marketplace name | Check the source; Claude Code accepts official marketplace names only from `github.com/anthropics/` |
| Bundled MCP server pulls an unpinned package | Pin versions; MCP identity allowlists apply to plugin servers in both leads |
| Bundled hooks run unreviewed | Codex `/hooks` trust review; managed-hooks-only switches |
| Repository config enables plugins or MCP before consent | Keep harnesses updated; review config in code review; trust only known repositories |

Advisories that apply to plugin-enabling configuration [Advisory]:

- Claude Code (fixes 2025-08-26, 2025-09-22, 2025-12-28): CVE-2025-59536, RCE through hooks in repository `.claude/settings.json`; an MCP consent bypass via `enableAllProjectMcpServers` in project settings; API key exfiltration via a project-set `ANTHROPIC_BASE_URL`. Sources disagree on which issue CVE-2026-21852 names ([Check Point](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/); [vpncentral](https://vpncentral.com/critical-claude-code-vulnerabilities-enable-remote-code-execution/)).
- Codex CLI CVE-2025-61260 (fixed 2025-08-20, v0.23.0, CVSS 9.8): a repository `.env` set `CODEX_HOME=./.codex`, and project `mcp_servers` commands ran at startup without a prompt ([NVD](https://nvd.nist.gov/vuln/detail/cve-2025-61260)).
- `postmark-mcp` (2025-09-17) shows the update risk for packages a plugin references; see [MCP](mcp.md).

No plugin supply-chain incident, as opposed to MCP package incidents, was found as of October 2026.

## Verification and checklist

- **Claude Code:** `claude plugin validate`, `claude plugin list`, `claude plugin details`. In `claude -p --output-format stream-json --verbose` the `init` event lists loaded plugins; CI can fail on `plugin_errors` in `system/init` ([Claude Code headless](https://code.claude.com/docs/en/headless)).
- **Admin policy:** `/status` shows "Enterprise managed settings"; add a blocked marketplace and confirm it is refused.
- **Codex:** `codex plugin marketplace list`, `/plugins`, `/hooks`; start a new session and confirm skills and tools load.
- **Dual-harness repository:** `claude plugin validate` plus a real `codex plugin marketplace add` against the same repository.
- **Release:** the version changed in both manifests and a `<plugin>--v<version>` tag exists.
- **Audit:** Claude Code emits OTel events `claude_code.plugin_installed` and `plugin_loaded`.

Checklist:

- [ ] A second repository or team uses this setup; otherwise it stays repo-local.
- [ ] Each plugin covers one capability; suites are bundle plugins or multiple entries.
- [ ] `version` is set in one place per manifest and bumped per release; both manifests match.
- [ ] Dependency ranges are constrained; third-party sources are pinned; auto-update is off for them.
- [ ] No secrets or tokens in `marketplace.json` or manifests.
- [ ] Instructions are in skills, executables in `scripts/`, state in the data path.
- [ ] Marketplace entries carry `owner` plus Codex `policy.*` and `category`; both `.mcp.json` and `mcp.json` exist for dual-harness use.
- [ ] Admin: source allowlist in both leads; `disableSideloadFlags` paired with `allowedMcpServers`.
- [ ] Third-party plugins were reviewed and are re-reviewed on update.
- [ ] Changes to plugin-enabling config go through code review.

## Portability

One repository can serve as a marketplace for both leads. Codex reads `.claude-plugin/marketplace.json` as legacy-compatible and sets `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` for plugin hooks ([Codex](../vendors/codex/plugins.md#marketplace-sources)). The combined layout has not been tested in the sources; verify it in both harnesses.

```text
<repo>/
├── .claude-plugin/marketplace.json   # read by Claude Code; read by Codex as legacy-compatible
└── plugins/my-plugin/
    ├── .claude-plugin/plugin.json    # Claude Code manifest
    ├── plugin.json                   # Codex manifest (Agent Plugins schema)
    ├── .mcp.json                     # Claude Code MCP servers
    ├── mcp.json                      # Codex MCP servers (same content, with `type`)
    ├── skills/<name>/SKILL.md        # same path in both
    └── hooks/hooks.json              # same path in both
```

Rules:

- **Marketplace entries carry the union of required fields:** top-level `owner` for Claude Code; `policy.installation`, `policy.authentication` and `category` per entry for Codex, which skips entries without them. Use a relative `source` starting with `./`, without `..`. `claude plugin validate` warns on `policy` but does not fail.
- **Two manifests with the same `name`, `version` and `description`.** Names are kebab-case, without the `claude-` or `anthropic-` prefix.
- **Hook commands use `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_PLUGIN_DATA}`;** both leads provide them. Hook event compatibility is covered in [hooks](hooks.md).
- **Ship both MCP file names with the same content.** Claude Code reads `.mcp.json`; the Codex plugin layout lists `mcp.json`, while the Codex MCP page refers to `.mcp.json` ([Codex](../vendors/codex/mcp.md#plugin-bundled-servers)).
- **Enablement is per harness:** the same ID goes into `enabledPlugins` in `.claude/settings.json` and into `[plugins."<id>"] enabled = true` in `.codex/config.toml`.

Traps:

- **A Claude Code project-scope install does not install.** It records the plugin as enabled; each collaborator still installs it.
- **Both leads gate repository-supplied marketplaces on trust:** `extraKnownMarketplaces` needs workspace trust; Codex reads project config only in trusted projects.
- **Claude Code agents, commands and output styles do nothing in Codex,** which documents no such components.
- **Dependencies do not port.** A Claude Code bundle plugin installs nothing extra in Codex.
- **The Codex IDE extension has no plugins.**
- **Admin allowlists must name each marketplace;** Codex does not implicitly allow even the OpenAI catalog.

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| Agents, commands, LSP servers, output styles, workflows, themes, monitors, `bin/`, plugin `settings.json`, channels | Claude Code | No Codex plugin component. |
| `dependencies`, `strict` manifest merge, `userConfig` and `claude plugin configure`, `renames` | Claude Code | No Codex counterpart. |
| Session-only loading (`--plugin-dir`, `--plugin-url`, `CLAUDE_CODE_PLUGIN_DIRS`), skill folders as plugins | Claude Code | Codex loads only installed, cached plugins. |
| Mods (JavaScript function hooks that draw UI) | Claude Code | No Codex counterpart. |
| Automatic updates per marketplace; `claude plugin validate`, `details`, `eval`, `test` | Claude Code | Codex documents only manual `marketplace upgrade` and no tooling counterpart. |
| Apps (connectors), assets, browser extensions; ChatGPT-shared plugin directory | Codex | No Claude Code counterpart; vendor platform features. |
| `policy.installation` values and `policy.authentication`; admin-set default enable state | Codex | Claude Code `defaultEnabled` sets state after install, and managed settings enforce rather than default. |
| Code plugins: custom tools, V2 API, TUI plugins, auth and provider hooks | OpenCode | A different concept; neither lead lets a plugin register tools in code. |

## Open questions

- Codex docs do not say whether Codex reads `.claude-plugin/plugin.json` manifests.
- The Codex MCP page and the Codex plugin layout disagree on `.mcp.json` versus `mcp.json`; untested.
- Whether Codex skips legacy-file entries that lack `policy` is untested.
- No Codex equivalent of `dependencies`, `renames`, release channels or a `validate` command was found.
- OpenAI publishes no review checklist for third-party plugins beyond hook trust review.
- The effects of `strictPluginOnlyCustomization`, `pluginTrustMessage` and `disableCommandPluginSources` are not described beyond their names ([Claude Code: plugins](../vendors/claude-code/plugins.md#limits-and-gotchas)).
- No empirical data on plugin supply-chain incidents.

## Sources

Vendor pages: [Claude Code: plugins](../vendors/claude-code/plugins.md), [Codex: plugins](../vendors/codex/plugins.md), [OpenCode: plugins](../vendors/opencode/plugins.md), [Codex: MCP](../vendors/codex/mcp.md), [Claude Code: instructions](../vendors/claude-code/instructions.md). Research notes: [MCP and plugins](../research-notes/agent-harness-best-practices/mcp-plugins.md), [Claude Code extensions](../research-notes/agent-harness-configuration/claude-code-extensions.md), [Codex extensions](../research-notes/agent-harness-configuration/codex-extensions.md).

- Claude Code: [Extend Claude Code](https://code.claude.com/docs/en/features-overview), [plugins overview](https://code.claude.com/docs/en/plugins/overview), [plugin dependencies](https://code.claude.com/docs/en/plugin-dependencies), [host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace), [create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces), [plugins for orgs](https://code.claude.com/docs/en/plugins/org), [plugin security](https://code.claude.com/docs/en/plugins/security), [headless](https://code.claude.com/docs/en/headless)
- Codex: [Build plugins](https://developers.openai.com/codex/plugins/build.md), [managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration)
- Advisories: [Check Point, Claude Code](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/), [vpncentral](https://vpncentral.com/critical-claude-code-vulnerabilities-enable-remote-code-execution/), [Check Point, Codex CLI](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/), [NVD CVE-2025-61260](https://nvd.nist.gov/vuln/detail/cve-2025-61260), [The Hacker News, postmark-mcp](https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html)
