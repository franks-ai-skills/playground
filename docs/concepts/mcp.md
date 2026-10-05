# MCP

MCP (Model Context Protocol) servers are external processes or remote endpoints that give the agent extra tools. The harness is the MCP client: it starts or connects to the configured servers, lists their tools to the model, and routes each tool call through its permission system. This adds capabilities, such as access to an issue tracker or a design tool, without changing the harness.

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Where servers are defined | `.mcp.json` (project), `~/.claude.json` (local and user scope) ([CC](../vendors/claude-code/mcp.md#locations-and-scopes)) | `[mcp_servers.<name>]` in `config.toml` (user, trusted project) ([Codex](../vendors/codex/mcp.md#locations-and-scopes)) | `mcp` key in any config layer ([OC](../vendors/opencode/mcp.md#locations-and-scopes)) |
| Scopes | Local (per project, private), project (committed), user; plus plugin, managed, subagent, `--mcp-config` ([CC](../vendors/claude-code/mcp.md#locations-and-scopes)) | User, project, custom agent file, plugin; admin allowlist ([Codex](../vendors/codex/mcp.md#locations-and-scopes)) | Any config layer; org config can ship servers disabled ([OC](../vendors/opencode/mcp.md#locations-and-scopes)) |
| Same name in several sources | Whole entry from the winning source, no field merge: managed > local > project > user > plugin > connectors ([CC](../vendors/claude-code/mcp.md#locations-and-scopes)) | Not documented ([Codex](../vendors/codex/mcp.md#limits-and-gotchas)) | Deep merge per key ([OC](../vendors/opencode/mcp.md#locations-and-scopes)) |
| Transports | `stdio` (default), `http` (`streamable-http`), `sse` (deprecated), `ws`, `sdk` ([CC](../vendors/claude-code/mcp.md#transports)) | stdio, streamable HTTP ([Codex](../vendors/codex/mcp.md#supported-features)) | `local` (stdio), `remote` ([OC](../vendors/opencode/mcp.md#format)) |
| Transport selection | `type` field; `url` without `type` is an error ([CC](../vendors/claude-code/mcp.md#limits-and-gotchas)) | Inferred: `command` for stdio, `url` for HTTP ([Codex](../vendors/codex/mcp.md#stdio-server-keys)) | `type` field ([OC](../vendors/opencode/mcp.md#local-server)) |
| stdio fields | `command`, `args`, `env` ([CC](../vendors/claude-code/mcp.md#server-entry-fields)) | `command`, `args`, `env`, `env_vars` (pass-through allowlist), `cwd` ([Codex](../vendors/codex/mcp.md#stdio-server-keys)) | `command` (array incl. args), `environment`, `cwd` ([OC](../vendors/opencode/mcp.md#local-server)) |
| HTTP fields | `url`, `headers` ([CC](../vendors/claude-code/mcp.md#server-entry-fields)) | `url`, `http_headers`, `env_http_headers`, `bearer_token_env_var` ([Codex](../vendors/codex/mcp.md#streamable-http-server-keys)) | `url`, `headers` ([OC](../vendors/opencode/mcp.md#remote-server)) |
| Secrets from environment | `${VAR}`, `${VAR:-default}` in `command`, `args`, `env`, `url`, `headers` ([CC](../vendors/claude-code/mcp.md#server-entry-fields)) | `env_vars`, `bearer_token_env_var`, `env_http_headers` ([Codex](../vendors/codex/mcp.md#format)) | `{env:VAR}` ([OC](../vendors/opencode/mcp.md#remote-server)) |
| Dynamic headers | `headersHelper`; needs workspace trust in `.mcp.json` ([CC](../vendors/claude-code/mcp.md#server-entry-fields)) | `http_headers_helper`: a command printing JSON headers; refreshed once on 401/403 ([Codex](../vendors/codex/mcp.md#streamable-http-server-keys)) | None recorded |
| OAuth | `oauth.clientId`, `callbackPort`; `claude mcp login` ([CC](../vendors/claude-code/mcp.md#server-entry-fields)) | Automatic CIMD or DCR; `[...oauth] client_id`, `callback_port`, `scopes`; `codex mcp login` ([Codex](../vendors/codex/mcp.md#oauth)) | Automatic on 401 with DCR; `oauth.clientId`, `clientSecret`, `scope` ([OC](../vendors/opencode/mcp.md#loading-and-invocation)) |
| Timeouts | Per-server `timeout`; `MCP_TIMEOUT` startup 30 s; `MCP_TOOL_TIMEOUT`; HTTP requests 60 s ([CC](../vendors/claude-code/mcp.md#environment-variables)) | `startup_timeout_sec` 10; `tool_timeout_sec` 60 ([Codex](../vendors/codex/mcp.md#keys-for-both-transports)) | `timeout` 5000 ms (local); `experimental.mcp_timeout` ([OC](../vendors/opencode/mcp.md#local-server)) |
| Enable / disable | `/mcp enable\|disable` writes per-project state in `~/.claude.json` ([CC](../vendors/claude-code/mcp.md#approval-and-filtering)) | `enabled` key; `-c mcp_servers.<id>.enabled=false` ([Codex](../vendors/codex/mcp.md#example)) | `enabled` key ([OC](../vendors/opencode/mcp.md#local-server)) |
| Tool filtering | Permission rules; a bare deny removes the tool from context ([CC](../vendors/claude-code/mcp.md#tool-naming), [rules](../vendors/claude-code/permissions-and-sandbox.md#rule-syntax)) | `enabled_tools`, `disabled_tools` ([Codex](../vendors/codex/mcp.md#keys-for-both-transports)) | `permission` patterns, e.g. `"mymcp_*": "deny"` ([OC](../vendors/opencode/mcp.md#related-config)) |
| Per-tool approval | `allow`/`ask`/`deny` rules on `mcp__server__tool` ([CC](../vendors/claude-code/mcp.md#tool-naming)) | `default_tools_approval_mode`, `tools.<tool>.approval_mode` ([Codex](../vendors/codex/mcp.md#keys-for-both-transports)) | `permission` per tool name ([OC](../vendors/opencode/mcp.md#related-config)) |
| Tool name | `mcp__<server>__<tool>` ([CC](../vendors/claude-code/mcp.md#tool-naming)) | `mcp__<server>__<tool>` as seen by hooks ([Codex](../vendors/codex/mcp.md#startup)) | `<server>_<tool>` ([OC](../vendors/opencode/mcp.md#loading-and-invocation)) |
| Server-forced approval | `_meta["anthropic/requiresUserInteraction"]` ([CC](../vendors/claude-code/mcp.md#server-side-metadata-recognized-by-claude-code)) | Destructive tool annotation, unless also a read annotation ([Codex](../vendors/codex/mcp.md#startup)) | None recorded |
| Server instructions | Loaded at startup; truncated at 2,048 chars ([CC](../vendors/claude-code/mcp.md#limits-and-gotchas)) | Read; keep the first 512 chars self-contained ([Codex](../vendors/codex/mcp.md#supported-features)) | Appended to context since v1.17.10 ([OC](../vendors/opencode/mcp.md#loading-and-invocation)) |
| Tool definitions in context | Deferred by default; fetched through `ToolSearch` ([CC](../vendors/claude-code/mcp.md#loading-and-invocation)) | Not documented | All loaded; costs context ([OC](../vendors/opencode/mcp.md#loading-and-invocation)) |
| Output limit | `MAX_MCP_OUTPUT_TOKENS` 25,000; larger results saved to a file ([CC](../vendors/claude-code/mcp.md#loading-and-invocation)) | `tools.<tool>.output_token_limit` ([Codex](../vendors/codex/mcp.md#keys-for-both-transports)) | `tool_output` 2000 lines / 51200 bytes, applies to all tools ([OC config](../vendors/opencode/configuration.md#top-level-opencodejson-keys)) |
| Repository-supplied servers | Each `.mcp.json` server needs interactive approval; loads without asking in `-p`, SDK, cloud ([CC](../vendors/claude-code/mcp.md#approval-and-filtering)) | Loaded only if the project is trusted ([Codex](../vendors/codex/mcp.md#locations-and-scopes)) | No gate recorded |
| Admin allowlist | `allowedMcpServers`/`deniedMcpServers` by `serverUrl`, `serverCommand`, or `serverName` ([CC](../vendors/claude-code/mcp.md#approval-and-filtering)) | `requirements.toml` `[mcp_servers.<id>] identity` by command or URL (exact, prefix, regex); name and identity must match ([Codex](../vendors/codex/mcp.md#admin-allowlist-requirementstoml)) | None recorded |
| Admin lockdown | `managed-mcp.json`: exclusive control; empty map disables MCP ([CC](../vendors/claude-code/mcp.md#locations-and-scopes)) | Empty `mcp_servers` table in requirements disables all servers ([Codex](../vendors/codex/mcp.md#admin-allowlist-requirementstoml)) | None recorded |
| Plugin-bundled servers | Plugin `.mcp.json` or `mcpServers`; tool names `mcp__plugin_<plugin>_<server>__<tool>` ([CC](../vendors/claude-code/mcp.md#tool-naming)) | Plugin manifest or `mcp.json`; users control enablement and tool settings, not transport ([Codex](../vendors/codex/mcp.md#plugin-bundled-servers)) | None |
| Elicitation | Supported (form and URL modes); the `Elicitation` hook can answer ([CC](../vendors/claude-code/mcp.md#resources-and-prompts)) | `approval_policy.granular.mcp_elicitations = false` auto-rejects ([Codex](../vendors/codex/mcp.md#startup)) | Not recorded |
| Sandbox | Local MCP servers run outside the sandbox ([CC](../vendors/claude-code/mcp.md#limits-and-gotchas)) | The network proxy does not filter MCP connections ([Codex](../vendors/codex/mcp.md#limits-and-gotchas)) | No sandbox |
| CLI | `claude mcp add\|add-json\|list\|get\|remove\|login\|logout`; `/mcp` ([CC](../vendors/claude-code/mcp.md#claude-mcp-commands)) | `codex mcp add\|list\|get\|remove\|login\|logout`; `/mcp` ([Codex](../vendors/codex/mcp.md#cli-and-ui)) | `opencode mcp add\|list\|auth\|logout\|debug` ([OC](../vendors/opencode/mcp.md#cli)) |

## Generalized model

**Server definition.** A named entry with:

- **Transport:** local process over stdio, or remote endpoint over streamable HTTP.
- **Local process fields:** command, arguments, environment, working directory.
- **Remote fields:** URL, static headers, headers built from environment variables, an optional header-helper command that prints headers, and OAuth settings (client ID, callback port, scopes).
- **Enabled flag.**
- **Timeouts:** startup and per tool call.
- **Tool filter:** allowlist and denylist of tool names. A filtered tool is not shown to the model.
- **Tool approval:** default decision for the server's tools and per-tool overrides. Expressed either inside the server entry (Codex) or as permission rules on the qualified tool name (Claude Code, OpenCode).
- **Output limit.**

**Qualified tool name.** `mcp__<server>__<tool>` in both leads. Permission rules and hook matchers address MCP tools by this name, so the server name is part of the public interface.

**Sources and scopes.** User, project (committed, trust-gated), plugin bundle, and subagent definition. Administrators do not define the user's servers; they restrict them.

**Governance.** An admin allowlist matches servers by identity (command or URL), not only by name, because a name is not a security control. An empty allowlist disables MCP.

**Lifecycle.**

1. At session start the harness starts local servers and connects to remote ones, bounded by the startup timeout.
2. Remote servers that answer 401 trigger OAuth. Tokens are stored per user.
3. The harness adds each server's instructions and its tool list to the context. Full tool schemas can be loaded eagerly or on demand.
4. Each tool call passes the permission pipeline. A server can mark a tool so that it always needs approval.
5. Results longer than the output limit are truncated or saved to a file.

**Trust boundary.** MCP server processes are not confined by the command sandbox. Tool-call approval does not constrain independently running server code ([Claude plugin security](https://code.claude.com/docs/en/plugins/security), [Codex limits](../vendors/codex/mcp.md#limits-and-gotchas)). Their actual access also depends on process identity, downstream authorization and outer isolation (inference). Read-only calls can disclose private data in arguments ([OpenAI deep research security](https://developers.openai.com/api/docs/guides/deep-research)).

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Server map | `mcpServers` | `[mcp_servers.<name>]` | `mcp` |
| Local process transport | `type: "stdio"` | `command` present | `type: "local"` |
| Remote transport | `type: "http"` | `url` present | `type: "remote"` |
| Environment for process | `env` | `env`, `env_vars` | `environment` |
| Header from secret | `headers` with `${VAR}` | `bearer_token_env_var`, `env_http_headers` | `headers` with `{env:VAR}` |
| Header helper | `headersHelper` | `http_headers_helper` | — |
| Startup timeout | `MCP_TIMEOUT` | `startup_timeout_sec` | `timeout` |
| Tool timeout | `timeout`, `MCP_TOOL_TIMEOUT` | `tool_timeout_sec` | `experimental.mcp_timeout` |
| Tool filter | Bare `deny` rule | `enabled_tools`, `disabled_tools` | `permission` deny |
| Tool approval | `allow`/`ask`/`deny` rules | `approval_mode` | `permission` |
| Qualified tool name | `mcp__s__t` | `mcp__s__t` | `s_t` |
| Admin allowlist | `allowedMcpServers` | `requirements.toml` `identity` | — |

## Portability

The leads share no MCP config file. Define each server once per harness: `.mcp.json` for Claude Code, `.codex/config.toml` for Codex, `opencode.json` for OpenCode.

The same stdio server in each format. Claude Code, `.mcp.json`:

```json
{ "mcpServers": { "context7": { "type": "stdio", "command": "npx", "args": ["-y", "@upstash/context7-mcp"] } } }
```

Codex, `.codex/config.toml`:

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

OpenCode, `opencode.json`:

```json
{ "mcp": { "context7": { "type": "local", "command": ["npx", "-y", "@upstash/context7-mcp"] } } }
```

Rules for a definition that behaves the same everywhere:

- **Use the same server name in every harness.** Claude Code and Codex then expose the same `mcp__<name>__<tool>` names, so permission rules and hook matchers can be written once per syntax with the same target. OpenCode names the tool `<name>_<tool>`.
- **Use stdio or streamable HTTP.** SSE, WebSocket, and SDK transports exist only in Claude Code, and SSE is deprecated ([CC](../vendors/claude-code/mcp.md#transports)).
- **Always set `type` in Claude Code.** An entry with `url` but no `type` is an error ([CC](../vendors/claude-code/mcp.md#limits-and-gotchas)). Codex has no `type` field.
- **Pass secrets through environment variables, in each harness's syntax.** Claude Code: `${VAR}` in `env` or `headers`; it expands credential variables such as `ANTHROPIC_API_KEY` to empty in a remote `url` or `headers` ([CC](../vendors/claude-code/mcp.md#server-entry-fields)). Codex: `env_vars` or `bearer_token_env_var`. OpenCode: `{env:VAR}`.
- **Write server instructions with the important part in the first 512 characters.** Codex asks for the first 512 characters to be self-contained; Claude Code truncates at 2,048 ([Codex](../vendors/codex/mcp.md#supported-features), [CC](../vendors/claude-code/mcp.md#limits-and-gotchas)).
- **Set timeouts explicitly** if startup is slow. Defaults differ: 30 s (Claude Code `MCP_TIMEOUT`), 10 s (Codex), 5 s (OpenCode local).
- **Emit both approval hints** if a server must force approval: `_meta["anthropic/requiresUserInteraction"]` for Claude Code and the destructive annotation for Codex.

Traps:

- **Repository servers load differently.** Claude Code asks once per `.mcp.json` server, but loads them without asking in `-p`, SDK, and cloud sessions. Codex loads project servers only after project trust, without a per-server prompt ([CC](../vendors/claude-code/mcp.md#approval-and-filtering), [Codex](../vendors/codex/mcp.md#limits-and-gotchas)).
- **"Local scope" in Claude Code is `~/.claude.json`**, not `.claude/settings.local.json` ([CC](../vendors/claude-code/mcp.md#limits-and-gotchas)).
- **MCP permission rules with parentheses are skipped in Claude Code settings files**; use `--disallowedTools` for parameter rules ([CC](../vendors/claude-code/mcp.md#limits-and-gotchas)).
- **A Claude Code hook matcher `mcp__memory` alone matches nothing**; use `mcp__memory__.*` ([CC](../vendors/claude-code/mcp.md#limits-and-gotchas)).
- **Context cost differs.** Claude Code defers tool definitions by default; OpenCode loads all of them; the Codex pages do not say. A server with many tools that is cheap in Claude Code can be expensive elsewhere.
- **Codex can no longer run as an MCP server.** `codex mcp-server` was removed in September 2026. Integrations that drove Codex through MCP need the app-server protocol ([Codex](../vendors/codex/mcp.md#limits-and-gotchas)).
- **Gap:** the Codex pages do not document whether a server defined in both user and project config is replaced as a whole or merged per key. Claude Code uses the whole entry from the winning source.

## Dropped from the generalization

- **Tool search and `alwaysLoad`** (Claude Code): deferred tool loading has no documented Codex counterpart.
- **MCP resources referenced as `@server:...`** (Claude Code): Codex pages record no resource support.
- **MCP prompts as slash commands** (Claude Code, OpenCode): not recorded for Codex.
- **`_meta` keys `anthropic/alwaysLoad` and `anthropic/maxResultSizeChars`** (Claude Code): vendor-specific server metadata.
- **`required` servers that fail startup** (Codex): Claude Code has no required-server flag.
- **Local scope stored per project in `~/.claude.json`** (Claude Code): Codex has no private per-project server store.
- **SSE, WebSocket, and SDK transports** (Claude Code): Codex supports only stdio and streamable HTTP.
- **The harness as an MCP server, `claude mcp serve`** (Claude Code): Codex removed `codex mcp-server`.
- **Vendor-account connectors** (Claude Code claude.ai connectors; Codex apps): each is tied to one vendor's account system.
- **`experimental_environment` and remote `env_vars` sources** (Codex): no Claude Code counterpart.
- **`mcp_optional_startup_grace_ms`** (Codex): no Claude Code counterpart.
- **Exact OAuth client registration details, CIMD** (Codex): the Claude Code OAuth subsections were not researched in detail, so no comparison is possible.
- **`--strict-mcp-config`** (Claude Code): Codex has no flag that limits a run to command-line servers.
- **`opencode mcp debug`** (OpenCode): no lead counterpart.

## Protocol revision and security checks

[Specification] These references use MCP 2026-07-28, the
[current revision](https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning).
They do not establish which revision a deployed harness negotiates.
For HTTP, validate present Origin (invalid values receive 403); local
binding and authentication add protection
([transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)).
Authorization also needs resource/audience binding, PKCE, response-issuer
checks and per-client consent; discovery needs SSRF defenses
([authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization),
[security considerations](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations),
[security guidance](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)).

The [security guide](../guide/security.md#mcp-authorization-and-transport)
connects those requirements to deployment checks and historical SDK
advisories. Do not conflate current application state handles with
legacy protocol sessions.

## Sources

- [Claude Code: MCP](../vendors/claude-code/mcp.md)
- [Codex: MCP](../vendors/codex/mcp.md)
- [OpenCode: MCP](../vendors/opencode/mcp.md)
- [Claude Code: permissions and sandbox](../vendors/claude-code/permissions-and-sandbox.md)
- [OpenCode: configuration](../vendors/opencode/configuration.md)
- [Claude Code README](../vendors/claude-code/README.md), [Codex README](../vendors/codex/README.md), [OpenCode README](../vendors/opencode/README.md)
