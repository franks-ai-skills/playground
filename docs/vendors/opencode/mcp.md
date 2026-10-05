# MCP

OpenCode connects to Model Context Protocol (MCP) servers and exposes their tools to the model next to the built-in tools. Servers are configured under the `mcp` config key as `local` (a command started over stdio) or `remote` (a URL). Remote servers get OAuth automatically, including dynamic client registration.

## Locations and scopes

| Scope | Where |
| --- | --- |
| Any config layer | `mcp` key in `opencode.json[c]` (global, project, managed, and so on; see [configuration.md](configuration.md)). |
| Organization | An org `.well-known/opencode` config can ship servers disabled and let users enable them locally ([MCP servers](https://opencode.ai/docs/mcp-servers/)). |
| OAuth tokens | `~/.local/share/opencode/mcp-auth.json` ([MCP servers](https://opencode.ai/docs/mcp-servers/)). |

Server entries merge across layers like other config objects (deep merge, later layer wins per key).

## Format

`mcp` is an object keyed by server name.

### Local server

| Field | Meaning | Default |
| --- | --- | --- |
| `type` | `"local"` | |
| `command` | Command and arguments as a string array. | |
| `cwd` | Working directory. | |
| `environment` | Environment variables. | |
| `enabled` | Enables or disables the server. | |
| `timeout` | Tool-fetch timeout in ms. | 5000 |

### Remote server

| Field | Meaning | Default |
| --- | --- | --- |
| `type` | `"remote"` | |
| `url` | Server URL. | |
| `enabled` | Enables or disables the server. | |
| `headers` | Request headers, e.g. `"Authorization": "Bearer {env:MY_API_KEY}"`. | |
| `oauth` | OAuth settings object, or `false` to disable OAuth. | automatic OAuth |
| `timeout` | Timeout. | not stated in the notes |

### `oauth` object

| Field | Meaning |
| --- | --- |
| `clientId` | Pre-registered client ID. |
| `clientSecret` | Pre-registered client secret. |
| `scope` | Requested scope. |

Sources for the three tables: [MCP servers](https://opencode.ai/docs/mcp-servers/).

### Related config

| Key | Effect |
| --- | --- |
| `experimental.mcp_timeout` | MCP request timeout ([SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)). |
| `permission` / legacy `tools` | Gate MCP tools by name or glob, globally or per agent, e.g. `"mymcp_*": "deny"` ([MCP servers](https://opencode.ai/docs/mcp-servers/); [Agents](https://opencode.ai/docs/agents/)). See [permissions-and-sandbox.md](permissions-and-sandbox.md). |

## Loading and invocation

- **Tool naming:** MCP tools are prefixed with the server name: `<server>_<tool>` ([MCP servers](https://opencode.ai/docs/mcp-servers/)).
- **OAuth:** triggered automatically when the server responds with 401. OpenCode uses Dynamic Client Registration (RFC 7591) when the server supports it; pre-registered clients use `oauth.clientId`, `clientSecret`, and `scope` ([MCP servers](https://opencode.ai/docs/mcp-servers/)).
- **Prompts:** MCP server prompts are registered as slash commands (`source: "mcp"`), with their arguments mapped to `$1..$n` ([SRC command/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/command/index.ts)). See [commands.md](commands.md).
- **Server instructions:** appended to session context since v1.17.10 ([REL v1.17.10](https://github.com/anomalyco/opencode/releases/tag/v1.17.10)). See [instructions.md](instructions.md).
- **Context cost:** MCP tools consume context. The docs call out the GitHub MCP server as token-heavy ([MCP servers](https://opencode.ai/docs/mcp-servers/)).
- **Cold starts:** `opencode run --attach <url>` reuses a warm `opencode serve` instance and avoids MCP cold starts ([CLI – run](https://opencode.ai/docs/cli/)). See [automation.md](automation.md).

### CLI

| Command | Purpose |
| --- | --- |
| `opencode mcp add` | Add a server. |
| `opencode mcp list` | List servers. |
| `opencode mcp auth [name]` | Authenticate a server. |
| `opencode mcp auth list` | List auth state. |
| `opencode mcp logout [name]` | Remove stored credentials. |
| `opencode mcp debug <name>` | Debug a server. |

Sources: [MCP servers](https://opencode.ai/docs/mcp-servers/); [CLI](https://opencode.ai/docs/cli/).

## Example

```json
{ "mcp": { "everything": { "type": "local", "command": ["npx","-y","@modelcontextprotocol/server-everything"] },
           "remote-api": { "type": "remote", "url": "https://mcp.example.com/mcp", "oauth": false,
                           "headers": { "Authorization": "Bearer {env:MY_API_KEY}" } } } }
```

## Limits and gotchas

- **Context cost is the only stated constraint.** The docs give no hard limit on the number of MCP tools (gap).
- **Per-tool gating uses the prefixed name** (`<server>_<tool>`), so a glob like `"mymcp_*"` covers a whole server.
- **Remote `timeout` default is not stated** in the notes (gap). The local default is 5000 ms.
- **MCP server instructions** enter session context since v1.17.10.

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

- https://opencode.ai/docs/mcp-servers/
- https://opencode.ai/docs/agents/
- https://opencode.ai/docs/cli/
- https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/command/index.ts
- https://github.com/anomalyco/opencode/releases/tag/v1.17.10
