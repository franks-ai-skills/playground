# MCP servers

Claude Code connects to Model Context Protocol (MCP) servers to add external tools, resources, and prompts to a session. Servers are configured at local, project, or user scope, and can also come from plugins, claude.ai connectors, or managed configuration. Tool search is on by default, so only tool names and server instructions load upfront and full tool definitions are fetched on demand ([MCP](https://code.claude.com/docs/en/mcp)).

## Locations and scopes

| Scope | Loads in | Shared | Stored in |
| :- | :- | :- | :- |
| Local (default) | Current project | No | `~/.claude.json` under `projects["<path>"].mcpServers` |
| Project | Current project | Yes, via VCS | `.mcp.json` in the project root |
| User | All projects | No | `~/.claude.json` |

Source: [MCP](https://code.claude.com/docs/en/mcp)

Further sources:

- Plugin servers: a plugin's `.mcp.json` or `mcpServers` in `plugin.json` ([plugin manifest](https://code.claude.com/docs/en/plugins/manifest-reference)); see [plugins.md](plugins.md).
- claude.ai connectors: load only with claude.ai subscription auth ([MCP](https://code.claude.com/docs/en/mcp)).
- `managedMcpServers` (managed settings, v2.1.259+): servers provided alongside the user's own ([MCP](https://code.claude.com/docs/en/mcp); [managed MCP](https://code.claude.com/docs/en/managed-mcp)).
- `managed-mcp.json` in the managed settings system directories: exclusive control. Users cannot add servers, and plugin and `--mcp-config` servers are blocked. An empty map disables MCP ([managed MCP](https://code.claude.com/docs/en/managed-mcp)).
- Subagent frontmatter `mcpServers` (name reference or inline definition); see [subagents.md](subagents.md).
- CLI: `--mcp-config <files|json>` and `--strict-mcp-config` (use only `--mcp-config` servers) (local CLI help).

Precedence when the same server is defined in several places: `managedMcpServers` > local > project > user > plugin > claude.ai connectors. The whole entry from the winning source is used, with no field merge. Plugins and connectors are deduplicated by endpoint ([MCP](https://code.claude.com/docs/en/mcp)).

### Approval and filtering

- Project `.mcp.json` servers need interactive approval. Reset choices with `claude mcp reset-project-choices`. In `-p`, SDK, and cloud sessions they load without asking ([MCP](https://code.claude.com/docs/en/mcp)).
- Settings keys `enableAllProjectMcpServers`, `enabledMcpjsonServers`, and `disabledMcpjsonServers` control approval. A cloned repo cannot approve its own servers before trust (v2.1.196+) ([MCP](https://code.claude.com/docs/en/mcp)).
- Toggling a server in `/mcp` writes `disabledMcpServers`/`enabledMcpServers` per project in `~/.claude.json` ([MCP](https://code.claude.com/docs/en/mcp)).
- `allowedMcpServers`/`deniedMcpServers`: entries by `serverUrl` (wildcards), `serverCommand`, or `serverName`. Names are not a security control ([managed MCP](https://code.claude.com/docs/en/managed-mcp)).
- `allowManagedMcpServersOnly` (managed) ([managed MCP](https://code.claude.com/docs/en/managed-mcp)).
- claude.ai connectors: disable with `disableClaudeAiConnectors: true` (`true` from any scope wins) or `ENABLE_CLAUDEAI_MCP_SERVERS=false` ([MCP](https://code.claude.com/docs/en/mcp)).

## Format

`.mcp.json` and `~/.claude.json` hold an `mcpServers` map from server name to entry.

### Transports

| `type` | Notes |
| :- | :- |
| `stdio` (default) | `command`, `args`, `env` |
| `http` | Recommended. `streamable-http` is an alias |
| `sse` | Deprecated. Since v2.1.265, `--transport http` auto-falls back to SSE |
| `ws` | WebSocket; only via JSON (`add-json` or `.mcp.json`); header auth only, no OAuth |
| `sdk` | SDK-host-only |

Source: [MCP](https://code.claude.com/docs/en/mcp)

### Server entry fields

| Field | Meaning |
| :- | :- |
| `type` | Transport (see above) |
| `command`, `args`, `env` | stdio server process |
| `url` | Remote server URL |
| `headers` | Static HTTP headers |
| `headersHelper` | Dynamic auth headers; needs workspace trust for `.mcp.json` |
| `oauth` | `clientId`, `callbackPort` |
| `timeout` | Per-server timeout |
| `alwaysLoad` | `true` exempts the server's tools from tool-search deferral; since v2.1.281 `false` defers all of the server's tools |

Source: [MCP](https://code.claude.com/docs/en/mcp); [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

- Variable expansion: `${VAR}` and `${VAR:-default}` work in `command`, `args`, `env`, `url`, and `headers`. Credential variables such as `ANTHROPIC_API_KEY` are deliberately expanded as empty in a remote `url` or `headers`. `CLAUDE_PROJECT_DIR` is set in the stdio server's environment ([MCP](https://code.claude.com/docs/en/mcp)).
- Reserved server names: `workspace`, `claude-in-chrome`, `computer-use`, `Claude Preview`, `Claude Browser`. `widgets` is reserved in cloud and self-hosted sessions as of v2.1.281 ([MCP](https://code.claude.com/docs/en/mcp); [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).

### Server-side metadata recognized by Claude Code

| `_meta` key | Effect |
| :- | :- |
| `anthropic/alwaysLoad` | Per-tool exemption from deferral |
| `anthropic/maxResultSizeChars` | Raises the output threshold per tool, up to 500,000 characters |
| `anthropic/requiresUserInteraction` | `true` forces a prompt on every call, in every mode |

Source: [MCP](https://code.claude.com/docs/en/mcp)

### Tool naming

| Source | Tool name |
| :- | :- |
| Configured server | `mcp__<server>__<tool>` |
| Plugin server | `mcp__plugin_<plugin>_<server>__<tool>`; the server is registered as `plugin:<plugin>:<server>` |
| claude.ai connector | `mcp__claude_ai_<server>__<tool>` |

Sources: [MCP](https://code.claude.com/docs/en/mcp); [permissions](https://code.claude.com/docs/en/permissions)

Permission rules: `mcp__server`, `mcp__server__*`, `mcp__server__tool` ([permissions](https://code.claude.com/docs/en/permissions)); see [permissions-and-sandbox.md](permissions-and-sandbox.md).

### Resources and prompts

- Resources: referenced as `@server:protocol://path` in prompts and fetched as attachments. List and read tools are auto-provided ([MCP](https://code.claude.com/docs/en/mcp)).
- Prompts: appear as `/servername:promptname (MCP)` or `/mcp__server__prompt arg1 arg2` (whitespace-split arguments) ([MCP](https://code.claude.com/docs/en/mcp)). See [commands.md](commands.md).
- Elicitation (form and URL modes) is supported and can be auto-answered with the `Elicitation` hook ([MCP](https://code.claude.com/docs/en/mcp)); see [hooks.md](hooks.md).

### `claude mcp` commands

- `claude mcp add [--transport http|sse|stdio] [-s local|user|project] [-e KEY=val] [-H "Header: v"] [--client-id] [--client-secret] [--callback-port] <name> <url | -- command args>`. Default transport is stdio; default scope is local. Everything after `--` is passed to a stdio server (local CLI help; [MCP](https://code.claude.com/docs/en/mcp)).
- `add-json <name> '<json>'`, `add-from-claude-desktop`, `list`, `get <name>`, `remove`, `login`/`logout` (OAuth), `reset-project-choices`, `serve` (Claude Code as a stdio MCP server) (local CLI help).
- In a session: `/mcp`, plus `/mcp reconnect|enable|disable <server|all>` ([commands](https://code.claude.com/docs/en/commands)).

### Environment variables

| Variable | Effect | Default |
| :- | :- | :- |
| `ENABLE_TOOL_SEARCH` | Tool search behavior (see below) | unset = defer all |
| `MAX_MCP_OUTPUT_TOKENS` | Max tool output | 25,000 tokens |
| `MCP_TIMEOUT` | Server startup timeout | 30000 ms |
| `MCP_TOOL_TIMEOUT` | Tool execution time | about 28 h; HTTP requests time out per request at 60 s unless raised |
| `CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH` | Truncation of tool descriptions and server instructions (v2.1.280+) | 2,048 chars |
| `ENABLE_CLAUDEAI_MCP_SERVERS` | `false` disables claude.ai connectors | — |
| `MCP_DISCOVERY_CACHE` | MCP-related (listed without detail in the notes) | — |

Sources: [MCP](https://code.claude.com/docs/en/mcp); [env vars](https://code.claude.com/docs/en/env-vars)

## Loading and invocation

- Tool search is on by default. Only tool names and server instructions load at startup; definitions are fetched through the `ToolSearch` tool ([MCP](https://code.claude.com/docs/en/mcp)).

| `ENABLE_TOOL_SEARCH` | Behavior |
| :- | :- |
| unset | Defer all MCP tools (with platform fallbacks) |
| `true` | Always defer |
| `auto` | Load upfront below 10% of context, defer above |
| `auto:N` | Same, with an N% threshold |
| `false` | Load all upfront |

Source: [MCP](https://code.claude.com/docs/en/mcp)

- Tool search is disabled automatically when `ANTHROPIC_BASE_URL` points to a non-first-party host, and kept off by `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`. It requires Sonnet/Haiku/Opus 4.5 or later ([MCP](https://code.claude.com/docs/en/mcp)).
- Output: a warning appears above 10,000 tokens. The default maximum is 25,000 tokens. Larger results are saved to a file under the session's `tool-results` directory and replaced by a reference ([MCP](https://code.claude.com/docs/en/mcp)).
- Inference (from the research notes): with tool search on, the per-server context cost is mostly server instructions and tool names. Reserve `alwaysLoad` for a few frequently used tools.

## Example

Minimal `.mcp.json` ([MCP](https://code.claude.com/docs/en/mcp)):

```json
{ "mcpServers": {
    "api-server": { "type": "http", "url": "${API_BASE_URL:-https://api.example.com}/mcp",
                    "headers": { "Authorization": "Bearer ${API_KEY}" } },
    "airtable": { "command": "npx", "args": ["-y", "airtable-mcp-server"], "env": { "AIRTABLE_API_KEY": "${AIRTABLE_API_KEY}" } } } }
```

## Limits and gotchas

- An entry with a `url` but no `type` is an error; it is read as stdio ([MCP](https://code.claude.com/docs/en/mcp)).
- MCP "local scope" (`~/.claude.json`) is not the same as local settings (`.claude/settings.local.json`); the docs flag this explicitly ([MCP](https://code.claude.com/docs/en/mcp)).
- Settings files skip any `mcp__` permission rule that has parentheses; use `--disallowedTools` for MCP parameter rules ([permissions](https://code.claude.com/docs/en/permissions)).
- A hook matcher `mcp__memory` alone matches nothing; use `mcp__memory__.*` ([hooks](https://code.claude.com/docs/en/hooks)).
- Local MCP servers run outside the sandbox ([sandboxing](https://code.claude.com/docs/en/sandboxing)).
- Tool descriptions and server instructions are truncated at 2,048 characters by default ([MCP](https://code.claude.com/docs/en/mcp)).
- SSE is deprecated ([MCP](https://code.claude.com/docs/en/mcp)).
- Gap (research notes): the OAuth configuration subsections (pre-configured credentials, scope restriction, metadata override) and the v2 runtime notification specifics were not read in detail.
- Gap (research notes): `MCP_DISCOVERY_CACHE` appears in the env var list without a described effect.

## Protocol security baseline

Security supplement checked 2026-10-05. These are MCP specification
requirements, not evidence that this harness implements every revision.
The [current revision is 2026-07-28](https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning);
record the deployment's negotiated revision before applying its rules.

- **Authorization:** validate token audience and resource binding; use
  PKCE; check a returned authorization-response issuer before code
  exchange. Reject missing `iss` when issuer support was advertised;
  compare any returned `iss` even when it was not advertised. Keep
  upstream tokens separate from MCP tokens; no token passthrough
  ([authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization),
  [security considerations](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations)).
- **HTTP:** validate present `Origin`, returning 403 for an invalid
  value. Local-only binding and authentication are additional
  recommendations, not substitutes for Origin validation
  ([transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)).
- **Server and client duties:** servers validate inputs, enforce access
  control and rate limits, and sanitize outputs. Clients should confirm
  sensitive operations, validate results, apply timeouts and log calls;
  annotations from untrusted servers are untrusted
  ([tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)).
- **Discovery and isolation:** check redirects and resolved addresses
  against SSRF, bind proxy consent to each client, and reauthorize
  application state handles. The current revision has no protocol
  session; do not copy legacy session recipes into it
  ([security guidance](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices),
  [tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)).

See the [cross-concept security guide](../../guide/security.md) for
attack evidence and proposed verification with synthetic fixtures.

## Sources

- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/managed-mcp
- https://code.claude.com/docs/en/permissions
- https://code.claude.com/docs/en/env-vars
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/sandboxing
- https://code.claude.com/docs/en/plugins/manifest-reference
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- Local CLI help: `claude mcp --help`, `claude mcp add --help` (v2.1.289)
