# MCP

Codex is a Model Context Protocol (MCP) client: it connects to external MCP servers and exposes their tools to the model. Servers are defined in `[mcp_servers.<name>]` tables in `config.toml` and use either stdio or streamable HTTP ([MCP](https://developers.openai.com/codex/mcp)). Codex can no longer run as an MCP server itself; `codex mcp-server` was removed in September 2026 in favor of the app-server protocol.

## Locations and scopes

| Source | Path | Notes |
|---|---|---|
| User config | `~/.codex/config.toml` | |
| Project config | `.codex/config.toml` | Trusted projects only ([MCP](https://developers.openai.com/codex/mcp)) |
| Custom agent files | `~/.codex/agents/*.toml`, `.codex/agents/*.toml` | A custom agent can set its own `mcp_servers`; otherwise the subagent inherits the parent's, see [subagents.md](subagents.md) |
| Plugins | Plugin `mcp.json` / manifest | Users cannot change the transport, only enablement and tool settings, see below and [plugins.md](plugins.md) |
| Admin allowlist | `requirements.toml` `[mcp_servers.<id>]` | Identity matching, see below |

The desktop app, CLI and IDE extension share this configuration ([MCP](https://developers.openai.com/codex/mcp)).

## Format

### Supported features

Stdio servers, environment variables, streamable HTTP, bearer token auth, OAuth (including CIMD and DCR), ChatGPT session auth for trusted first-party servers, and server `instructions`. Codex reads the server `instructions`; keep the first 512 characters self-contained ([MCP](https://developers.openai.com/codex/mcp)).

### stdio server keys

| Key | Meaning |
|---|---|
| `command` | Command to start the server (required) |
| `args` | Arguments |
| `env` | Map of environment variables |
| `env_vars` | Allowlist of variables to pass through; strings or `{ name, source = "local" \| "remote" }` |
| `cwd` | Working directory |
| `experimental_environment` | `local` or `remote` |

Sources: [MCP](https://developers.openai.com/codex/mcp); [Config reference](https://developers.openai.com/codex/config-reference).

### Streamable HTTP server keys

| Key | Meaning | Default |
|---|---|---|
| `url` | Server URL (required) | |
| `auth` | `oauth` or `chatgpt` | `oauth` |
| `bearer_token_env_var` | Environment variable that holds a bearer token | |
| `http_headers` | Static headers | |
| `env_http_headers` | Headers read from environment variables | |
| `http_headers_helper` | Local command that prints JSON headers. Refreshed once on a 401/403. An explicit bearer token or OAuth wins over the helper's `Authorization` header | |
| `scopes` | OAuth scopes | |
| `oauth_resource` | RFC 8707 resource indicator | |
| `[mcp_servers.<id>.oauth] client_id`, `callback_url`, `callback_port` | OAuth client settings | |

With no credentials configured, Codex connects unauthenticated ([MCP](https://developers.openai.com/codex/mcp); [Config reference](https://developers.openai.com/codex/config-reference)).

### Keys for both transports

| Key | Meaning | Default |
|---|---|---|
| `startup_timeout_sec` | Startup timeout; alias `startup_timeout_ms` | `10` |
| `tool_timeout_sec` | Per-tool-call timeout | `60` |
| `enabled` | Enable or disable the server | |
| `required` | Fail startup or resume if the server cannot initialize | |
| `enabled_tools` | Tool allowlist | |
| `disabled_tools` | Tool denylist, applied after the allowlist | |
| `default_tools_approval_mode` | `auto`, `prompt`, `writes` or `approve`. `writes` prompts for tools not marked read-only | |
| `tools.<tool>.approval_mode` | Per-tool approval mode | |
| `tools.<tool>.output_token_limit` | Per-tool output limit | |

Sources: [MCP](https://developers.openai.com/codex/mcp); [Config reference](https://developers.openai.com/codex/config-reference).

### Global MCP keys

| Key | Meaning | Default |
|---|---|---|
| `mcp_optional_startup_grace_ms` | Grace period for optional servers at startup. `0` waits for each server's full startup timeout | `1000` |
| `mcp_oauth_callback_port` | OAuth callback port | |
| `mcp_oauth_callback_url` | OAuth callback URL | |
| `mcp_oauth_credentials_store` | `auto`, `file` or `keyring` | |

Sources: [MCP](https://developers.openai.com/codex/mcp); [Config reference](https://developers.openai.com/codex/config-reference).

### Plugin-bundled servers

Plugins ship servers in their manifest or `mcp.json`. Users cannot set the transport, but can control `plugins."<plugin>@<marketplace>".mcp_servers.<server>.enabled`, `enabled_tools`, `disabled_tools`, `default_tools_approval_mode` and `tools.<t>.approval_mode`. Plugin `.mcp.json` OAuth settings use camelCase: `clientId`, `callbackUrl`, `callbackPort` ([MCP](https://developers.openai.com/codex/mcp); [Config reference](https://developers.openai.com/codex/config-reference)).

### Admin allowlist (`requirements.toml`)

- `[mcp_servers.<id>] identity = { command = "..." }` or `{ url = "..." }`. Structured matchers are available: `executable` plus ordered `args` with `exact`, `prefix` or `regex`; URL with `exact`, `prefix` or `regex` ([Managed config](https://developers.openai.com/codex/enterprise/managed-configuration); [Config reference](https://developers.openai.com/codex/config-reference)).
- Both the name and the identity must match, or the server is disabled. An empty `mcp_servers` table disables all servers. The same shapes apply under `plugins.<p>.mcp_servers.<s>` ([Managed config](https://developers.openai.com/codex/enterprise/managed-configuration)).

## Loading and invocation

### Startup

- Codex starts configured servers at session start. `startup_timeout_sec` bounds each server's startup; `mcp_optional_startup_grace_ms` bounds how long Codex waits for optional servers. A server with `required = true` that cannot initialize fails startup or resume ([MCP](https://developers.openai.com/codex/mcp)), and makes `codex exec` exit with an error ([Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)).
- Tools from servers become available to the model. Tool names appear to hooks as `mcp__server__tool` ([Hooks](https://learn.chatgpt.com/docs/hooks.md)).
- Destructive tool calls always require approval when the tool advertises a destructive annotation, unless it advertises a read annotation ([Security](https://developers.openai.com/codex/agent-approvals-security)). MCP elicitations can be auto-rejected with `approval_policy.granular.mcp_elicitations = false`; see [permissions-and-sandbox.md](permissions-and-sandbox.md).
- Skills can declare MCP server dependencies in `agents/openai.yaml`; see [skills.md](skills.md). Hooks can call MCP tools through `mcp_tool` handlers on already-connected servers; see [hooks.md](hooks.md).

### OAuth

- Codex prefers CIMD (Client ID Metadata Document) when the authorization server advertises `client_id_metadata_document_supported` and supports `none` token auth; otherwise it uses DCR (Dynamic Client Registration). A configured client ID skips registration ([MCP](https://developers.openai.com/codex/mcp)).
- Codex uses ChatGPT-hosted CIMD documents (`https://chatgpt.com/oauth/codex/client.json` or a per-server variant), validates `iss`, and prefers the server-advertised `scopes_supported` over configured scopes. Loopback `http://127.0.0.1` callbacks get the active port inserted (RFC 8252) ([MCP](https://developers.openai.com/codex/mcp)).

### CLI and UI

| Command | Purpose |
|---|---|
| `codex mcp list [--json]` | List configured servers |
| `codex mcp get` | Exists per `codex mcp --help`; flags not captured |
| `codex mcp add <NAME> (--url <URL> \| -- <COMMAND>...)` | Add a server. Flags: `--env KEY=VALUE` (stdio only), `--bearer-token-env-var` (HTTP only), `--oauth-client-id`, `--oauth-client-secret`, `--oauth-client-registration auto\|cimd\|dcr`, `--oauth-resource` |
| `codex mcp remove` | Remove a server |
| `codex mcp login <NAME> [--scopes a,b] [--no-browser] [--oauth-client-registration ...]` | OAuth login. The registration choice applies only to that login and is not stored |
| `codex mcp logout` | Counterpart to `login`; flags not captured |
| `/mcp [verbose]` (TUI) | List active servers; `verbose` shows details |

Sources: local CLI (`codex mcp --help`, `codex mcp add --help`, 0.159.2); [MCP](https://developers.openai.com/codex/mcp); [CLI reference](https://developers.openai.com/codex/cli/reference). The IDE extension and desktop app have a Settings > MCP servers UI ([MCP](https://developers.openai.com/codex/mcp)).

## Example

```toml
# ~/.codex/config.toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
enabled_tools = ["get_file"]
tool_timeout_sec = 45
```

CLI equivalent for the first server: `codex mcp add context7 -- npx -y @upstash/context7-mcp`. Disable a server for one run: `codex -c mcp_servers.context7.enabled=false`. Sources: [MCP](https://developers.openai.com/codex/mcp); [Advanced config](https://developers.openai.com/codex/config-advanced).

## Limits and gotchas

- **`codex mcp-server` removed.** "The `codex mcp-server` command and the standalone `codex-mcp-server` binary have been removed." Use the Codex app server, a separate JSON-RPC protocol that is not MCP. The app-server is experimental and not supported for production ([Agents SDK guide](https://developers.openai.com/codex/guides/agents-sdk); [CLI reference](https://developers.openai.com/codex/cli/reference); [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk.md)). Deprecated 2026-08-24, removed 2026-09-05 ([Changelog](https://developers.openai.com/codex/changelog)). Local 0.159.2 has no `mcp-server` subcommand; `codex app-server` offers `daemon`, `proxy`, `generate-ts` and `generate-json-schema` (local CLI). See [automation.md](automation.md) for the SDKs and app-server.
- **Inference: older integrations break.** Integrations built before September 2026 on the Agents SDK `MCPServerStdio("codex mcp-server")` pattern do not work on current releases.
- **The network proxy does not filter MCP connections.** Use the `mcp_servers` allowlist in `requirements.toml` instead ([Security](https://developers.openai.com/codex/agent-approvals-security)).
- **Project trust gates repository servers.** Inference: a trusted repository can ship `.codex/config.toml` with `[mcp_servers]`, so trust is effectively the gate for repository-supplied MCP servers.
- **Gap: merge semantics.** Whether a `mcp_servers.<id>` defined in both user and project config is replaced as a whole table or merged per key is not documented.
- **Gap: CLI flags.** The exact flags of `codex mcp get` and `codex mcp logout` were not captured; the subcommands exist per `codex mcp --help`.

## Sources

- https://developers.openai.com/codex/mcp
- https://developers.openai.com/codex/config-reference
- https://developers.openai.com/codex/config-advanced
- https://developers.openai.com/codex/enterprise/managed-configuration
- https://developers.openai.com/codex/agent-approvals-security
- https://developers.openai.com/codex/cli/reference
- https://developers.openai.com/codex/guides/agents-sdk
- https://developers.openai.com/codex/changelog
- https://learn.chatgpt.com/docs/codex-sdk.md
- https://learn.chatgpt.com/docs/non-interactive-mode.md
- https://learn.chatgpt.com/docs/hooks.md
