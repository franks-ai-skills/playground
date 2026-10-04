# Automation

OpenCode runs without the TUI through four entry points: `opencode run` for one-shot scripted prompts, `opencode serve` for a long-running HTTP server, the `@opencode-ai/sdk` JavaScript client that wraps that server, and a GitHub Action that responds to issue and PR events. Session sharing publishes a conversation as a public link. These let scripts, CI jobs, and IDE integrations drive the same agent, config, and permissions as the TUI.

## Locations and scopes

| Entry point | Where it runs | Config it uses |
| --- | --- | --- |
| `opencode run` | Local shell, CI | Normal config layers ([configuration.md](configuration.md)); flags override agent, model, and permissions. |
| `opencode serve` / `opencode web` | Local HTTP server | Normal config layers plus the `server` key; `/config` supports GET and PATCH. |
| SDK `createOpencode` | Starts a server from Node | Inline `config` overrides `opencode.json`. |
| GitHub Action | GitHub Actions runner, `.github/workflows/opencode.yml` | Repo config plus Action inputs. |
| GitLab | GitLab (gitlab.mdx in the docs) | Not covered in the notes beyond its existence ([GitLab](https://opencode.ai/docs/gitlab/)). |

`default_agent` picks the default primary agent across TUI, `opencode run`, desktop, and the GitHub Action ([Config](https://opencode.ai/docs/config/)).

## Format

### `opencode run`

([CLI – run](https://opencode.ai/docs/cli/))

| Group | Flags |
| --- | --- |
| Session | `--continue/-c`, `--session/-s`, `--fork` |
| Prompt | `--command`, `--file/-f`, `--title` |
| Model and agent | `--model/-m`, `--agent`, `--variant`, `--thinking` |
| Output | `--format default\|json` (`json` emits raw events), `--share` |
| Server | `--attach <url>`, `--password/-p`, `--username/-u`, `--dir`, `--port` |
| Permissions | `--auto` (approves anything not explicitly denied; see [permissions-and-sandbox.md](permissions-and-sandbox.md)) |

`--attach` reuses a warm `opencode serve` instance and avoids MCP cold starts. `--command <name> [args]` runs a custom command ([commands.md](commands.md)).

### Other CLI commands

`tui` (default), `attach`, `auth`, `agent`, `github install|run`, `mcp`, `models`, `serve`, `web`, `acp` (Agent Client Protocol over stdio nd-JSON), `session list|delete`, `stats`, `export [--sanitize]`, `import <file|share-url>`, `plugin`, `pr <number>`, `db`, `debug`, `upgrade`, `uninstall`. Global flags: `--print-logs`, `--log-level`, `--pure` ([CLI](https://opencode.ai/docs/cli/)).

### Server

`opencode serve` flags ([Server](https://opencode.ai/docs/server/)):

| Flag | Default |
| --- | --- |
| `--port` | 4096 |
| `--hostname` | 127.0.0.1 |
| `--mdns` | — |
| `--mdns-domain` | — (config `server.mdnsDomain` defaults to `opencode.local`) |
| `--cors` | repeatable |

Config equivalents: `server.port`, `server.hostname`, `server.mdns`, `server.mdnsDomain`, `server.cors` ([Config – Server](https://opencode.ai/docs/config/)).

- Auth: HTTP basic auth is enabled by `OPENCODE_SERVER_PASSWORD`; the username defaults to `opencode` (`OPENCODE_SERVER_USERNAME` sets it).
- Spec: OpenAPI 3.1 at `/doc`.
- Endpoint groups: `/global/health`, `/global/event` (SSE), `/project`, `/config` (GET and PATCH), `/provider`, `/session` (CRUD, children, todo, prompt, …), and `/tui` for driving the TUI (used by IDE plugins).
- The TUI is itself a client of this server.

Source: [Server](https://opencode.ai/docs/server/); env vars from [CLI](https://opencode.ai/docs/cli/).

### SDK

([SDK](https://opencode.ai/docs/sdk/))

| Call | Purpose |
| --- | --- |
| `npm install @opencode-ai/sdk` | Install. |
| `createOpencode({hostname, port, signal, timeout, config})` | Starts a server and a client. Inline `config` overrides `opencode.json`. |
| `createOpencodeClient({baseUrl, fetch, parseAs, responseStyle, throwOnError})` | Connects to an existing server. |
| `session.prompt({ body: { parts, format: { type: "json_schema", schema, retryCount? } } })` | Structured output. The result is in `info.structured_output`; failure produces a `StructuredOutputError`. |

Types are generated from the OpenAPI spec.

### GitHub Action

Setup: `opencode github install` sets up the GitHub app, the workflow, and secrets. Manual setup: install github.com/apps/opencode-agent, add `.github/workflows/opencode.yml` using `anomalyco/opencode/github@latest`, and grant `id-token: write` ([GitHub](https://opencode.ai/docs/github/)).

| Input | Meaning | Default |
| --- | --- | --- |
| `model` | Model. Required. | |
| `agent` | Must be a primary agent. | `default_agent`, then `build` |
| `share` | Share the session. | `true` for public repos |
| `prompt` | Prompt. Required for `issues`, `schedule`, and `workflow_dispatch` events. | |
| `mentions` | Trigger phrases in comments. | `/opencode,/oc` |
| `variant` | Model variant. | |
| `oidc_base_url` | OIDC base URL. | |
| `use_github_token` | Uses the caller's `GITHUB_TOKEN` and skips both the OIDC exchange and the app. | |

Supported events: `issue_comment`, `pull_request_review_comment`, `issues`, `pull_request`, `schedule`, `workflow_dispatch` ([GitHub](https://opencode.ai/docs/github/)).

### Sharing

| Setting | Effect |
| --- | --- |
| `share: "manual"` | Default. Share with `/share`. |
| `share: "auto"` | Shares automatically. `OPENCODE_AUTO_SHARE` is the env equivalent. |
| `share: "disabled"` | Sharing off. |
| `autoshare` | Deprecated boolean; use `share`. |

Links have the form `opncd.ai/s/<id>` and are public to anyone with the link. `/unshare` removes the link. `opencode run --share` shares a scripted run; `opencode import <share-url>` imports a shared session ([Share](https://opencode.ai/docs/share/); [CLI](https://opencode.ai/docs/cli/); [SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)).

## Loading and invocation

- `opencode run` is the non-interactive entry point: it runs one prompt or command with the normal config. With `--attach`, it reuses a warm `opencode serve` instance and avoids MCP cold starts ([CLI – run](https://opencode.ai/docs/cli/)).
- Since v1.18.20, `opencode run` answers permission requests raised by subagents ([REL v1.18.20](https://github.com/anomalyco/opencode/releases/tag/v1.18.20)).
- Since v1.18.0, the auto-accept state is kept per server ([REL v1.18.0](https://github.com/anomalyco/opencode/releases/tag/v1.18.0)).
- The GitHub Action triggers on the configured events; comment events need one of the `mentions` phrases.
- `--format json` emits raw events instead of the default output.

## Example

```bash
opencode run --agent plan --format json --auto "Summarize open TODOs"
opencode serve --port 4096 &  opencode run --attach http://localhost:4096 --command review
```

## Limits and gotchas

- **Share links are public** to anyone with the link. The GitHub Action shares by default on public repos.
- **`--auto` in scripts** approves every `ask`; explicit `deny` rules still apply.
- **The Action's `agent` must be primary**; otherwise it falls back to `default_agent` or `build`.
- **`issues`, `schedule`, and `workflow_dispatch` events require `prompt`.**
- **`autoshare` is deprecated** in favor of `share`.
- **Gap:** the full HTTP route list in server.mdx (message, file, find, event, and tui routes) was only partly read.
- **Gap:** SDK v2 (`@opencode-ai/sdk/v2`, used by the plugin types) is not covered on the user docs page.
- **Gap:** the GitLab integration exists in the docs but was not researched.

## Sources

- https://opencode.ai/docs/cli/
- https://opencode.ai/docs/server/
- https://opencode.ai/docs/sdk/
- https://opencode.ai/docs/github/
- https://opencode.ai/docs/gitlab/
- https://opencode.ai/docs/share/
- https://opencode.ai/docs/config/
- https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts
- https://github.com/anomalyco/opencode/releases/tag/v1.18.0
- https://github.com/anomalyco/opencode/releases/tag/v1.18.20
