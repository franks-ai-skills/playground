# Plugins: best practices

How to package, version, distribute, govern and review plugins for Claude Code and Codex. A plugin here is the bundle-and-marketplace unit both leads share: a versioned directory of skills, hooks and MCP server definitions, listed in a marketplace, installed into a versioned cache and enabled by plugin ID (`<plugin>@<marketplace>`). OpenCode uses "plugin" for a JavaScript/TypeScript code module with no marketplace, so it appears only where noted. Terms follow the [plugins concept page](../concepts/plugins.md). Research date: 2026-10-04.

Evidence labels: **[Vendor]** vendor guidance. **[Empirical]** a study or measured data. **[Advisory]** a security advisory, CVE or coordinated disclosure. **[Practitioner]** practitioner opinion or an informal experiment.

## Summary

1. [Package a setup as a plugin when a second repository or team needs it](#1-package-when-a-second-repository-needs-the-setup); until then keep it repo-local.
2. [Keep plugins single-purpose and compose suites from them](#2-keep-plugins-single-purpose-and-compose-suites).
3. [Set `version` explicitly, in one place, and bump it on every release](#3-set-version-explicitly-and-bump-it-on-every-release).
4. [Pin dependency ranges and third-party sources](#4-pin-dependencies-and-third-party-sources); leave auto-update off for marketplaces you do not control.
5. [Serve both leads from one repository with the union of required fields](#7-serve-both-leads-from-one-repository), and validate in both.
6. [Allowlist marketplace sources and pair them with MCP and hook controls](#9-allowlist-marketplace-sources-as-an-admin).
7. [Review a third-party plugin's hooks, MCP commands and executables before installing](#10-review-third-party-plugins-before-installing); a plugin runs code with your privileges outside the sandbox.
8. [Treat committed config that enables plugins or marketplaces as executable code](#11-review-plugin-enabling-config-like-code).

## When to use it

| Situation | Use | Notes |
| --- | --- | --- |
| One repository needs skills, hooks or MCP servers | Repo-local config: [skills](../concepts/skills.md), [hooks](../concepts/hooks.md), [MCP](./mcp.md), [instructions](../concepts/instructions.md) | No packaging overhead. |
| "A second repository needs the same setup", or the setup goes to others via a marketplace | Plugin | Claude Code's stated trigger ([Extend Claude Code](https://code.claude.com/docs/en/features-overview)). |
| A role needs a curated set (for example "backend standard") | A bundle plugin that only declares dependencies (Claude Code); several entries or `INSTALLED_BY_DEFAULT` (Codex) | Codex has no dependency mechanism. |
| Project instructions must travel | A skill inside the plugin | Instructions do not travel in a plugin: a `CLAUDE.md` at the plugin root is not loaded ([plugins concept page](../concepts/plugins.md)). |
| OpenCode must receive the same skills | OpenCode's skill discovery paths (`.claude/skills`, `.agents/skills`) | OpenCode has no marketplace or bundle (inference on the [plugins concept page](../concepts/plugins.md)). |
| Containers and CI need plugins without interactive installs | A seed directory (`CLAUDE_CODE_PLUGIN_SEED_DIR`) | See [automation](./automation.md). |

## Approaches

### Repo-local configuration, no plugin

- **What:** skills, hooks and MCP definitions committed in the repository (`.claude/`, `.agents/skills/`, `.mcp.json`, `.codex/config.toml`).
- **When it fits:** one repository; the setup changes with the code.
- **Trade-offs:** no versioning or update path across repositories; copies drift once a second repository needs them.

### Single-purpose plugin in a marketplace

- **What:** one plugin per capability or integration, listed in a marketplace.
- **When it fits:** a capability reused across repositories or shared outside the team.
- **How (generalized):** manifest (`name` in kebab-case, `version`, `description`, author), `skills/<name>/SKILL.md`, `hooks/hooks.json`, an MCP JSON file at the plugin root.
  - Claude Code: `.claude-plugin/plugin.json` (optional; only `name` required; `claude-` and `anthropic-` prefixes are rejected), `.mcp.json`, `${CLAUDE_PLUGIN_ROOT}` (versioned, replaced on update) and `${CLAUDE_PLUGIN_DATA}` (persists across updates). Executables go in `scripts/`, referenced as `${CLAUDE_PLUGIN_ROOT}/scripts/<name>`; org sync rejects a top-level `bin/` ([Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace)).
  - Codex: root `plugin.json` in the cross-vendor Agent Plugins schema, `skills/`, `mcp.json` with a transport `type` per server, `hooks/hooks.json`, `assets/`; OpenAI-specific settings under `extensions.com.openai`. The legacy `.codex-plugin/plugin.json` still works, but "new packages should use portable format". Hook paths start with `./` and stay inside the plugin root ([Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)).
- **Trade-offs:** independent versioning, review and admin control per plugin. More entries to maintain.

### Suite through a bundle plugin

- **What:** a Claude Code plugin made only of a name and `dependencies`, such as `backend-standard`, which installs a curated set with one command ([Plugin dependencies](https://code.claude.com/docs/en/plugins/dependencies)). A meta-plugin can also symlink skills from sibling plugins in the same marketplace; they are dereferenced into the cache, and symlinks that leave the marketplace are skipped ([Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace)).
- **When it fits:** role-based setups built from single-purpose plugins.
- **How:** semver ranges in `dependencies`; ranges resolve against `<plugin>--v<version>` git tags created by `claude plugin tag --push`; cross-marketplace dependencies need `allowCrossMarketplaceDependenciesOn`. In Codex, list several entries or use `policy.installation: INSTALLED_BY_DEFAULT`.
- **Trade-offs:** dependency ranges must be pinned or a dependency's MCP rename breaks the bundle. Not portable to Codex.

### Dual-harness marketplace repository

- **What:** one repository that both leads read as a marketplace. Codex reads `.claude-plugin/marketplace.json` as "Legacy-compatible" and sets `CLAUDE_PLUGIN_ROOT` / `CLAUDE_PLUGIN_DATA` for plugin hooks ([Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)).
- **When it fits:** a team uses both leads.
- **How:** see [practice 7](#7-serve-both-leads-from-one-repository). Layout from the [plugins concept page](../concepts/plugins.md):

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

- **Trade-offs:** the combined layout is documented but not tested in the sources. Only shared components (skills, hooks, MCP) work in both; Claude Code agents, commands and output styles do nothing in Codex.

### Internal or org marketplace with admin governance

- **What:** a private catalog plus managed policy that restricts sources and force-enables approved plugins.
- **When it fits:** organizations that need control over what runs on developer machines.
- **How:**
  - Claude Code hosting: GitHub, another git host, a hosted `marketplace.json` URL, or a shared directory. Private repositories use the user's non-interactive git credentials (`gh auth setup-git`); `marketplace.json` has no token field. For a repository-scoped team, `claude plugin marketplace add ... --scope project` and commit `.claude/settings.json`; it applies only after folder trust ([Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace); [Plugins for orgs](https://code.claude.com/docs/en/plugins/org)).
  - Codex: `[plugins."my-plugin@local-repo"] enabled = true` in the repository's `.codex/config.toml`; admin workspace publishing keeps plugins inside the org; `features.plugin_sharing = false` turns sharing off ([Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)).
  - Governance: [practice 9](#9-allowlist-marketplace-sources-as-an-admin).
- **Trade-offs:** release channels need two marketplaces, because "Claude Code has no release-channel concept" ([Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace)).

### Seeded plugins for containers and CI

- **What:** pre-populated plugin directory for non-interactive environments.
- **How:** Claude Code reads `CLAUDE_CODE_PLUGIN_SEED_DIR` (read-only; auto-update forced off). `CLAUDE_CODE_SYNC_PLUGIN_INSTALL=1` makes a `-p` run wait for plugin installs ([Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace); [Plugins for orgs](https://code.claude.com/docs/en/plugins/org)). No Codex counterpart is recorded in the notes.

## Practices

### 1. Package when a second repository needs the setup

- **Practice:** keep extensions repo-local until a second repository or team needs them; then move them into a plugin.
- **Why:** a plugin adds a manifest, a marketplace entry and a release process; that cost pays off only with reuse.
- **How:** move skills, hooks and MCP definitions into a plugin directory; replace project-relative paths with `${CLAUDE_PLUGIN_ROOT}`.
- **Evidence:** [Vendor] "Use plugins when you want to reuse the same setup across multiple repositories or distribute to others via a marketplace"; trigger: "A second repository needs the same setup" ([Extend Claude Code](https://code.claude.com/docs/en/features-overview)).

### 2. Keep plugins single-purpose and compose suites

- **Practice:** one plugin per capability or integration; build role suites as bundle plugins.
- **Why:** admin force-enable and block work per plugin, not per skill. Small plugins are easier to review and version.
- **How:** Claude Code bundle plugins with `dependencies`; Codex multiple entries or `INSTALLED_BY_DEFAULT`.
- **Evidence:** [Vendor] ([Plugin dependencies](https://code.claude.com/docs/en/plugins/dependencies)). Granularity rule is an inference in the notes.

### 3. Set version explicitly and bump it on every release

- **Practice:** set a semver `version` and bump it with every release; set it in one place.
- **Why:** "users stay on their cached copy until the string changes". Codex keys its cache directory by version, and a semver `version` "enables marketplace updates". If `version` is set in both `plugin.json` and the marketplace entry, `plugin.json` silently wins.
- **How:** bump in the manifest; for dual-harness plugins keep `name`, `version` and `description` identical in `.claude-plugin/plugin.json` and root `plugin.json`. Tag releases `<plugin>--v<version>`. Alternative in Claude Code: omit `version` everywhere to track commits.
- **Evidence:** [Vendor] ([Host and maintain a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace); [Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)).

### 4. Pin dependencies and third-party sources

- **Practice:** constrain dependency ranges, pin third-party marketplace sources, and keep auto-update off for marketplaces you do not control.
- **Why:** "If that release renames an MCP tool your plugin calls, your plugin breaks." Auto-update can change files you already reviewed, and background updates use stored git credentials without prompting.
- **How:**
  - Dependencies: `~2.1.0` to receive patches only ([Plugin dependencies](https://code.claude.com/docs/en/plugins/dependencies)).
  - Sources: `ref` / `sha` on entries or `#<ref>` on the add command; `sha256` on archive sources (Claude Code refuses a download whose digest differs). The community catalog pins plugins to commit SHAs ([Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace); [Plugin security](https://code.claude.com/docs/en/plugins/security)).
  - Codex: `codex plugin marketplace add owner/repo --ref main` pins a ref; updates come through `codex plugin marketplace upgrade` ([Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)).
  - Auto-update: off by default for third-party marketplaces in Claude Code; turn it on (`autoUpdate` in managed `extraKnownMarketplaces`) only for internal marketplaces you control. Re-review before updating third-party plugins.
  - MCP servers inside a plugin: pin package versions (see [MCP practice 12](./mcp.md#12-allowlist-servers-by-identity-and-pin-versions)).
- **Evidence:** [Vendor] as cited ([Plugins for orgs](https://code.claude.com/docs/en/plugins/org)).

### 5. Put instructions in skills and executables in scripts

- **Practice:** ship guidance as skills and executables under `scripts/`; write persistent state to the data path.
- **Why:** a `CLAUDE.md` at the plugin root is not loaded, and the Codex plugin format lists no instruction-file component. Org sync rejects a top-level `bin/`. The root path changes on every update.
- **How:** `skills/<name>/SKILL.md`; `${CLAUDE_PLUGIN_ROOT}/scripts/<name>` in hooks and MCP commands; state under `${CLAUDE_PLUGIN_DATA}`.
- **Evidence:** [Vendor] ([plugins concept page](../concepts/plugins.md), from [Claude Code plugins docs](https://code.claude.com/docs/en/plugins/overview); [Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace)).

### 6. Never change a published plugin's name

- **Practice:** keep `name` stable; change the display name instead.
- **Why:** the plugin ID `<plugin>@<marketplace>` is what configuration and installs refer to; changing `name` breaks installs.
- **How:** use `displayName`; for a real rename, use the `renames` map and treat it as append-only. Keep the marketplace entry name equal to the manifest name. `forceRemoveDeletedPlugins` uninstalls removed entries.
- **Evidence:** [Vendor] ([Host and maintain a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace); [Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces)).

### 7. Serve both leads from one repository

- **Practice:** one `.claude-plugin/marketplace.json` with the union of both leads' required fields, two manifests per plugin, and shared component paths.
- **Why:** Codex reads the Claude Code marketplace file as legacy-compatible and provides the `CLAUDE_PLUGIN_*` variables to hooks.
- **How:**
  - Marketplace: Claude Code requires top-level `name`, `owner`, `plugins` and per entry `name`, `source`. Codex requires per entry `name`, `source`, `policy.installation` (`AVAILABLE` / `INSTALLED_BY_DEFAULT` / `NOT_AVAILABLE`), `policy.authentication`, `category`, and skips entries missing them. Use a relative `source` starting with `./`, inside the marketplace root, without `..` ([Codex Build plugins](https://developers.openai.com/codex/plugins/build.md); [Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces)).
  - `claude plugin validate` warns on unknown fields such as `policy` but does not fail.
  - Manifests: `.claude-plugin/plugin.json` and root `plugin.json` with identical `name`, `version`, `description`.
  - Hooks: `hooks/hooks.json` with `${CLAUDE_PLUGIN_ROOT}` paths.
  - MCP: ship `.mcp.json` and `mcp.json` (with `type` per server) with the same content; the Codex docs contradict each other on the file name ([plugins concept page](../concepts/plugins.md)).
  - Enablement stays per harness: `enabledPlugins` in `.claude/settings.json`, `[plugins."<id>"] enabled = true` in `.codex/config.toml`.
- **Evidence:** [Vendor] as cited; layout is an inference in the notes and the concept page, not a tested setup. Verify with `claude plugin validate` and a real `codex plugin marketplace add`.

### 8. Validate in CI

- **Practice:** run validation on every change to a plugin repository.
- **Why:** pushes without a version bump never reach Claude Code users, and diverging manifests break one harness silently.
- **How:** a CI job that runs `claude plugin validate .` and fails when the two manifests' versions differ (inference in the notes). Codex has no `validate` command in the sources.
- **Evidence:** [Vendor] `claude plugin validate` ([Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces)); the CI job is an inference.

### 9. Allowlist marketplace sources as an admin

- **Practice:** restrict marketplace sources in managed policy, register approved marketplaces explicitly, and pair the source allowlist with MCP and hook controls.
- **Why:** sideloaded MCP servers and hooks bypass a marketplace allowlist unless restricted separately.
- **How:**
  - Claude Code managed settings: `strictKnownMarketplaces` (`[]` blocks all, including the official marketplace; owner wildcard `your-org/*` and `hostPattern` supported; `ref` / `path` must match exactly); `blockedMarketplaces` (checked first, URLs canonicalized); `enabledPlugins` (`true` force-enables, `false` blocks and hides). Further switches: `disableSideloadFlags`, `allowManagedHooksOnly`, `disableCommandPluginSources`, `strictPluginOnlyCustomization`. Lists apply before download and again at session start. Recommended policy: allow the official marketplace plus your own, register both in `extraKnownMarketplaces`, set `disableSideloadFlags`, and pair it with `allowedMcpServers` because `disableSideloadFlags` does not restrict `.mcp.json`, `claude mcp add` or SDK servers ([Plugins for orgs](https://code.claude.com/docs/en/plugins/org)).
  - Codex `requirements.toml`: `[marketplaces] restrict_to_allowed_sources = true` with `allowed_sources` rules (git URL plus ref, `host_pattern`, or local path); the OpenAI catalog must be listed explicitly; plugin MCP identity allowlist under `plugins.<p>.mcp_servers.<s>.identity`; `allow_managed_hooks_only` skips plugin hooks ([Codex managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration)).
  - Audit: Claude Code emits OTel events `claude_code.plugin_installed` / `plugin_loaded`; third-party names are redacted unless `OTEL_LOG_TOOL_DETAILS=1`. Enterprise customers have a plugins Analytics API ([Plugins for orgs](https://code.claude.com/docs/en/plugins/org)).
- **Evidence:** [Vendor] as cited.

### 10. Review third-party plugins before installing

- **Practice:** inspect every executable component before install and after every update.
- **Why:** "A Claude Code plugin you install can execute arbitrary code on your machine with your user privileges." Hooks, MCP servers and mod processes run outside the sandbox; `bin/` goes on the Bash tool's PATH. A marketplace name signals who publishes the catalog, not what the plugins do.
- **How:**
  - Claude Code: `claude plugin marketplace list` to check the source; read the `/plugin` "Will install" pane; read `hooks/hooks.json`, `.mcp.json` and every file in `bin/`; `claude --plugin-dir <dir> plugin details <name>` for the component inventory. Official and community marketplace names are accepted only from `github.com/anthropics/` ([Plugin security and trust](https://code.claude.com/docs/en/plugins/security)).
  - Codex: bundled hooks "are non-managed and require user trust review before execution"; review them with `/hooks` ([Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)).
  - For bundled MCP servers, apply the [MCP server review](./mcp.md#14-review-a-third-party-server-before-connecting-it).
- **Evidence:** [Vendor] as cited. OpenAI publishes no review checklist beyond hook trust review.

### 11. Review plugin-enabling config like code

- **Practice:** treat committed settings that register marketplaces or enable plugins as executable configuration, and review it in code review.
- **Why:** project-level config ran code before consent in older versions of both leads (see [Security](#security)).
- **How:** review changes to `.claude/settings.json` (`extraKnownMarketplaces`, `enabledPlugins`) and `.codex/config.toml` (`[plugins.*]`, `[marketplaces.*]`). Both leads gate repository-supplied marketplaces on trust: Claude Code `extraKnownMarketplaces` needs workspace trust; Codex reads project config only in trusted projects ([plugins concept page](../concepts/plugins.md)). A Claude Code project-scope install records the plugin as enabled for collaborators; each must still install it.
- **Evidence:** [Advisory] ([Check Point, Claude Code](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/); [Check Point, Codex](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/)).

## Anti-patterns

| Avoid | Do instead |
| --- | --- |
| Pushing commits without a version bump | Bump `version` per release; Claude Code users otherwise never receive them ([3](#3-set-version-explicitly-and-bump-it-on-every-release)) |
| `version` in both `plugin.json` and the marketplace entry | One place; `plugin.json` silently wins |
| Changing `name` | `displayName` or the `renames` map ([6](#6-never-change-a-published-plugins-name)) |
| Unconstrained dependency ranges | `~x.y.z` patch ranges |
| Secrets or git tokens in `marketplace.json` | Users' git credentials (`gh auth setup-git`) |
| Relative-path entries in a URL-hosted catalog | Git or archive sources |
| Plugin files in Git LFS | Regular git files |
| A top-level `bin/` for org sync | `scripts/` plus `${CLAUDE_PLUGIN_ROOT}/scripts/<name>` |
| `CLAUDE.md` at the plugin root | A skill |
| Unpinned `npx` MCP servers inside a plugin | Pinned versions ([MCP 12](./mcp.md#12-allowlist-servers-by-identity-and-pin-versions)) |
| Auto-update on for third-party marketplaces | Pin `ref` / `sha`; re-review before updating |
| `disableSideloadFlags` alone | Pair with `allowedMcpServers` |
| A suite plugin that duplicates other plugins' files | Bundle plugin with `dependencies`, or symlinks inside the marketplace |

## Security

A plugin is code and instructions with your user privileges. Hooks, MCP servers and mod processes run outside the sandbox, `bin/` joins the Bash PATH, and auto-update can replace files you reviewed ([Plugin security and trust](https://code.claude.com/docs/en/plugins/security)). Codex does not trust plugin hooks on install ([Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)); the notes record no separate gate for Claude Code plugin hooks ([plugins concept page](../concepts/plugins.md)).

| Threat | Mitigation |
| --- | --- |
| Malicious or compromised plugin | Source allowlist (`strictKnownMarketplaces`, `restrict_to_allowed_sources`); review before install ([10](#10-review-third-party-plugins-before-installing)) |
| Update changes reviewed code | Pin `ref` / `sha` / `sha256`; auto-update only for internal marketplaces |
| Lookalike marketplace name | Check the source with `claude plugin marketplace list`; official names are accepted only from `github.com/anthropics/` |
| Bundled MCP server pulls an unpinned package | Pin versions; MCP identity allowlists apply to plugin servers in both leads |
| Bundled hooks run unreviewed | Codex `/hooks` trust review; `allowManagedHooksOnly` / `allow_managed_hooks_only` |
| Repository config enables plugins or MCP before consent | Keep both harnesses updated; review config in code review; trust only known repositories |

Advisories that apply to plugin-enabling configuration:

- [Advisory] Claude Code, Check Point: CVE-2025-59536 (RCE through hooks in repository `.claude/settings.json`), an MCP consent bypass via `enableAllProjectMcpServers` / `enabledMcpjsonServers` in project settings, and API key exfiltration via a project-set `ANTHROPIC_BASE_URL` before the trust dialog. Fixes shipped 2025-08-26, 2025-09-22 and 2025-12-28 ([Check Point](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)).
- [Advisory] Codex CLI CVE-2025-61260 (CVSS 9.8): a repository `.env` set `CODEX_HOME=./.codex`, and project `mcp_servers` commands ran at startup without a prompt. Fixed in v0.23.0 (2025-08-20) ([Check Point](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/); [NVD](https://nvd.nist.gov/vuln/detail/cve-2025-61260)).
- [Advisory] `postmark-mcp` on npm shows the update path risk for packages a plugin might reference: since version 1.0.16 it BCC'd every email to the attacker ([CSO Online](https://www.csoonline.com/article/4064009/trust-in-mcp-takes-first-in-the-wild-hit-via-squatted-postmark-connector.html)). See [MCP security](./mcp.md#security).

No plugin supply-chain incident (as opposed to MCP package incidents) was found as of October 2026.

## Verification

- **Claude Code:** `claude plugin validate`, `claude plugin list`, `claude plugin details`; `claude -p --output-format stream-json --verbose` (the `init` event lists the loaded plugins); CI gates can fail on `plugin_errors` in the `system/init` event ([Claude Code headless](https://code.claude.com/docs/en/headless)).
- **Admin policy (Claude Code):** `/status` shows "Enterprise managed settings"; try adding a blocked marketplace and confirm it is refused.
- **Codex:** `codex plugin marketplace list`, `/plugins`, `/hooks` for trust; start a new session and confirm skills and tools load.
- **Dual-harness repository:** `claude plugin validate` plus a real `codex plugin marketplace add` against the same repository.
- **Release:** confirm the version changed in both manifests and a `<plugin>--v<version>` tag exists.

## Checklist

- [ ] A second repository or team uses this setup; otherwise it stays repo-local.
- [ ] Each plugin covers one capability; suites are bundle plugins or multiple entries.
- [ ] `version` is set in exactly one place per manifest and bumped per release; both manifests match.
- [ ] Dependency ranges are constrained (`~x.y.z`).
- [ ] Third-party sources are pinned (`ref` / `sha` / `sha256`); auto-update is off for them.
- [ ] No secrets or tokens in `marketplace.json` or manifests.
- [ ] Instructions are in skills; executables in `scripts/`; state in the data path.
- [ ] MCP servers in the plugin pin versions; both `.mcp.json` and `mcp.json` exist for dual-harness use.
- [ ] Marketplace entries carry `owner` plus Codex `policy.*` and `category`.
- [ ] Admin: source allowlist set in both leads (OpenAI catalog listed explicitly if wanted); `disableSideloadFlags` paired with `allowedMcpServers`; managed-hooks-only considered.
- [ ] Third-party plugins were reviewed (hooks, MCP commands, `bin/`, component inventory) and are re-reviewed on update.
- [ ] Changes to plugin-enabling config go through code review.

## Open questions

- Codex docs do not say whether Codex reads `.claude-plugin/plugin.json` manifests.
- The Codex MCP page and the Codex plugin layout disagree on `.mcp.json` versus `mcp.json`. Untested.
- No Codex equivalent of plugin `dependencies`, `renames`, release-channel guidance or a `validate` command was found.
- Whether Claude Code accepts Codex `policy` fields without error beyond a warning, and whether Codex skips legacy-file entries that lack `policy`, is not tested ([plugins concept page](../concepts/plugins.md)).
- OpenAI publishes no review checklist for third-party Codex plugins beyond hook trust review.
- No empirical data on plugin supply-chain incidents as of October 2026.

## Sources

- [Extend Claude Code](https://code.claude.com/docs/en/features-overview)
- [Claude Code plugins overview](https://code.claude.com/docs/en/plugins/overview)
- [Claude Code plugin dependencies](https://code.claude.com/docs/en/plugins/dependencies)
- [Claude Code: host and maintain a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace)
- [Claude Code: create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude Code plugins for orgs](https://code.claude.com/docs/en/plugins/org)
- [Claude Code plugin security and trust](https://code.claude.com/docs/en/plugins/security)
- [Claude Code headless](https://code.claude.com/docs/en/headless)
- [Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)
- [Codex managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration)
- [Check Point Research, Claude Code project files](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)
- [Check Point Research, Codex CLI](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/)
- [NVD CVE-2025-61260](https://nvd.nist.gov/vuln/detail/cve-2025-61260)
- [CSO Online, squatted Postmark connector](https://www.csoonline.com/article/4064009/trust-in-mcp-takes-first-in-the-wild-hit-via-squatted-postmark-connector.html)
- Repo: [plugins concept page](../concepts/plugins.md), [concept index](../concepts/README.md)
