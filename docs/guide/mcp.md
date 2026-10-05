# MCP

MCP (Model Context Protocol) servers are external processes or remote endpoints that give the agent extra tools. The harness is the MCP client: it starts or connects to the configured servers, lists their tools to the model, and routes each tool call through its permission system. MCP adds capabilities, such as access to an issue tracker or a design tool, without changing the harness.

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Where servers are defined | `.mcp.json` (project), `~/.claude.json` (local and user scope) ([CC](../vendors/claude-code/mcp.md#locations-and-scopes)) | `[mcp_servers.<name>]` in `config.toml` (user, trusted project) ([Codex](../vendors/codex/mcp.md#locations-and-scopes)) | `mcp` key in any config layer ([OC](../vendors/opencode/mcp.md#locations-and-scopes)) |
| Same name in several sources | Whole entry from the winning source: managed > local > project > user > plugin > connectors ([CC](../vendors/claude-code/mcp.md#locations-and-scopes)) | Not documented ([Codex](../vendors/codex/mcp.md#limits-and-gotchas)) | Deep merge per key ([OC](../vendors/opencode/mcp.md#locations-and-scopes)) |
| Transports | `stdio` (default), `http`, `sse` (deprecated), `ws`, `sdk`; `type` required ([CC](../vendors/claude-code/mcp.md#transports)) | stdio, streamable HTTP; inferred from `command` or `url` ([Codex](../vendors/codex/mcp.md#stdio-server-keys)) | `local` (stdio), `remote` ([OC](../vendors/opencode/mcp.md#format)) |
| Secrets from environment | `${VAR}`, `${VAR:-default}` in `command`, `args`, `env`, `url`, `headers` ([CC](../vendors/claude-code/mcp.md#server-entry-fields)) | `env_vars`, `bearer_token_env_var`, `env_http_headers` ([Codex](../vendors/codex/mcp.md#format)) | `{env:VAR}` ([OC](../vendors/opencode/mcp.md#remote-server)) |
| Dynamic headers | `headersHelper`; needs workspace trust in `.mcp.json` ([CC](../vendors/claude-code/mcp.md#server-entry-fields)) | `http_headers_helper`, refreshed once on 401/403 ([Codex](../vendors/codex/mcp.md#streamable-http-server-keys)) | None recorded |
| OAuth | `oauth.clientId`, `callbackPort`; `claude mcp login` ([CC](../vendors/claude-code/mcp.md#server-entry-fields)) | Automatic CIMD or DCR; `client_id`, `callback_port`, `scopes`; `codex mcp login` ([Codex](../vendors/codex/mcp.md#oauth)) | Automatic on 401 with DCR ([OC](../vendors/opencode/mcp.md#loading-and-invocation)) |
| Timeouts | `MCP_TIMEOUT` startup 30 s; per-server `timeout`, `MCP_TOOL_TIMEOUT` ([CC](../vendors/claude-code/mcp.md#environment-variables)) | `startup_timeout_sec` 10; `tool_timeout_sec` 60 ([Codex](../vendors/codex/mcp.md#keys-for-both-transports)) | `timeout` 5000 ms (local) ([OC](../vendors/opencode/mcp.md#local-server)) |
| Tool filtering | Permission rules; a bare deny removes the tool from context ([CC](../vendors/claude-code/mcp.md#tool-naming)) | `enabled_tools`, `disabled_tools` ([Codex](../vendors/codex/mcp.md#keys-for-both-transports)) | `permission` patterns ([OC](../vendors/opencode/mcp.md#related-config)) |
| Per-tool approval | `allow`/`ask`/`deny` on `mcp__server__tool` ([CC](../vendors/claude-code/mcp.md#tool-naming)) | `default_tools_approval_mode`, `tools.<tool>.approval_mode` ([Codex](../vendors/codex/mcp.md#keys-for-both-transports)) | `permission` per tool ([OC](../vendors/opencode/mcp.md#related-config)) |
| Tool name | `mcp__<server>__<tool>` ([CC](../vendors/claude-code/mcp.md#tool-naming)) | `mcp__<server>__<tool>` as seen by hooks ([Codex](../vendors/codex/mcp.md#startup)) | `<server>_<tool>` ([OC](../vendors/opencode/mcp.md#loading-and-invocation)) |
| Server-forced approval | `_meta["anthropic/requiresUserInteraction"]` ([CC](../vendors/claude-code/mcp.md#server-side-metadata-recognized-by-claude-code)) | Destructive annotation, unless also a read annotation ([Codex](../vendors/codex/mcp.md#startup)) | None recorded |
| Server instructions | Truncated at 2,048 chars ([CC](../vendors/claude-code/mcp.md#limits-and-gotchas)) | Keep the first 512 chars self-contained ([Codex](../vendors/codex/mcp.md#supported-features)) | Appended to context ([OC](../vendors/opencode/mcp.md#loading-and-invocation)) |
| Tool definitions in context | Deferred by default, fetched through tool search ([CC](../vendors/claude-code/mcp.md#loading-and-invocation)) | Deferred since PR #29486 (2026-06-22) on supported models; not in the user docs ([notes](../research-notes/agent-harness-best-practices/mcp-plugins.md#cited-findings)) | All loaded ([OC](../vendors/opencode/mcp.md#loading-and-invocation)) |
| Output limit | `MAX_MCP_OUTPUT_TOKENS` 25,000; larger results saved to a file ([CC](../vendors/claude-code/mcp.md#loading-and-invocation)) | `tools.<tool>.output_token_limit`; default not documented ([Codex](../vendors/codex/mcp.md#keys-for-both-transports)) | `tool_output` for all tools ([OC config](../vendors/opencode/configuration.md#top-level-opencodejson-keys)) |
| Repository-supplied servers | Interactive approval per `.mcp.json` server; loads without asking in `-p`, SDK, cloud ([CC](../vendors/claude-code/mcp.md#approval-and-filtering)) | Loaded only if the project is trusted ([Codex](../vendors/codex/mcp.md#locations-and-scopes)) | No gate recorded |
| Admin allowlist | `allowedMcpServers`/`deniedMcpServers` by URL, command or name; `managed-mcp.json` for exclusive control ([CC](../vendors/claude-code/mcp.md#approval-and-filtering)) | `requirements.toml` `identity` by command or URL; empty table disables MCP ([Codex](../vendors/codex/mcp.md#admin-allowlist-requirementstoml)) | None recorded |
| Plugin-bundled servers | Tool names `mcp__plugin_<plugin>_<server>__<tool>` ([CC](../vendors/claude-code/mcp.md#tool-naming)) | Users control enablement and tool settings, not transport ([Codex](../vendors/codex/mcp.md#plugin-bundled-servers)) | None |
| Sandbox | Local servers run outside the sandbox ([CC](../vendors/claude-code/mcp.md#limits-and-gotchas)) | Network proxy does not filter MCP connections ([Codex](../vendors/codex/mcp.md#limits-and-gotchas)) | No sandbox |
| CLI | `claude mcp add\|list\|get\|remove\|login`; `/mcp` ([CC](../vendors/claude-code/mcp.md#claude-mcp-commands)) | `codex mcp add\|list\|get\|remove\|login`; `/mcp` ([Codex](../vendors/codex/mcp.md#cli-and-ui)) | `opencode mcp add\|list\|auth\|debug` ([OC](../vendors/opencode/mcp.md#cli)) |

## Generalized model

**Server definition.** A named entry with:

- **Transport:** local process over stdio, or remote endpoint over streamable HTTP.
- **Local process fields:** command, arguments, environment, working directory.
- **Remote fields:** URL, static headers, headers built from environment variables, an optional header-helper command, and OAuth settings (client ID, callback port, scopes).
- **Enabled flag, startup and tool timeouts, output limit.**
- **Tool filter:** allowlist and denylist of tool names. A filtered tool is not shown to the model.
- **Tool approval:** a default decision for the server's tools and per-tool overrides, either inside the server entry (Codex) or as permission rules on the qualified tool name (Claude Code, OpenCode).

**Qualified tool name.** `mcp__<server>__<tool>` in both leads. Permission rules and hook matchers address MCP tools by this name, so the server name is part of the public interface.

**Sources and scopes.** User, project (committed, trust-gated), plugin bundle, and subagent definition. Administrators do not define the user's servers; they restrict them with an allowlist that matches by identity (command or URL), because a name is not a security control. An empty allowlist disables MCP.

**Lifecycle.**

1. At session start the harness starts local servers and connects to remote ones, bounded by the startup timeout.
2. A remote server that answers 401 triggers OAuth. Tokens are stored per user.
3. The harness adds each server's instructions and its tool list to the context. Full schemas load eagerly or on demand.
4. Each tool call passes the permission pipeline. A server can mark a tool so that it always needs approval.
5. Results longer than the output limit are truncated or saved to a file.

**Trust boundary.** MCP servers run outside the command sandbox. Their access is limited only by which servers are allowed and which tool calls are approved.

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

## When to use it and when not

MCP is one of several ways to reach an external system. Since mid-2026 both leads defer tool definitions, so context cost no longer decides between a CLI and MCP, except where deferral is off: Claude Code with a custom `ANTHROPIC_BASE_URL`, `ENABLE_TOOL_SEARCH=false` or a pre-4.5 model; Codex with an older model/provider combination; and OpenCode, which loads every definition.

Use it when:

| Situation | Why MCP fits |
| --- | --- |
| SaaS with per-user OAuth (issue tracker, design tool, observability) | The server handles connection and auth. |
| Stateful integration (browser automation, debugger session) | A long-lived process holds the state between calls. |
| No usable CLI exists, or the client has no shell | There is nothing else for the agent to call ([Zechner](https://mariozechner.at/posts/2025-08-15-mcp-vs-cli/), 2025). |
| The agent copies data from a browser tab it cannot see | Claude Code's stated trigger for adding MCP ([Extend Claude Code](https://code.claude.com/docs/en/features-overview)). |

Do not use it when:

| Situation | Use instead | Cost or risk of MCP here |
| --- | --- | --- |
| The model knows a CLI for the system (`gh`, `aws`, `kubectl`) and a sandboxed shell exists | The CLI plus a [skill](skills.md) with team conventions | MCP servers run outside the sandbox and the shell [permission rules](permissions-and-sandbox.md); CLI output can be piped through `jq` or `head`, MCP results cannot. |
| A workflow chains many calls over large data | Code execution against an API, SDK or MCP bindings in a sandbox (see [Approaches](#approaches)) | Every intermediate result passes through the context. |
| A deterministic step must run on an event | A [hook](hooks.md) | MCP tools are offered to the model, which may not call them. |
| You need to teach how to use a tool | A [skill](skills.md) | A server provides the connection, not the workflow. |
| The same servers must reach several repositories | Ship the definitions in a [plugin](plugins.md) | Copies drift across repositories. |

## Approaches

**CLI plus skill, no MCP.** The agent calls a known CLI through its shell; a skill documents commands and conventions. Fits when a known CLI and a sandboxed shell exist. Allow specific subcommands (Claude Code `Bash(gh pr view *)`) and keep the sandbox on. Trade-off: portable and sandboxed, but in Claude Code the command-safety check runs on every bash call; in Zechner's Aug 2025 benchmark that cost 1.3–2M Haiku tokens against 35k for MCP, at similar total cost ($19.95 vs $19.45).

**Local stdio server.** The harness starts a local process. Fits tools that need local state or a local runtime. Claude Code: `.mcp.json` or `~/.claude.json`, always with `"type": "stdio"`, filter with bare `deny` rules. Codex: `[mcp_servers.<name>]`, filter with `enabled_tools`/`disabled_tools`, approval with `default_tools_approval_mode`. Trade-off: the process runs with user privileges outside the sandbox, and an unpinned `npx -y` or `uvx` command runs whatever the latest release is.

**Remote streamable HTTP server.** The harness connects to an HTTPS endpoint with OAuth, a bearer token from the environment, or a header helper. Fits SaaS with per-user auth. Claude Code: `"type": "http"`, `claude mcp login`, `oauth.scopes`, `headersHelper` for Kerberos or internal SSO (must print JSON within 10 s; runs only after workspace trust). Codex: `url`, `bearer_token_env_var` or `http_headers_helper`, OAuth through CIMD or DCR ([Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)). Trade-off: no local process, but OAuth adds confused-deputy, SSRF and redirect risks (see [Security](#security)).

**Code execution against MCP or APIs.** The agent writes code against servers presented as files or bindings and runs it in a sandbox. Anthropic reported one example dropping from 150,000 to 2,000 tokens ([Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp), Nov 2025); Cloudflare's Code Mode runs TypeScript in V8 isolates with credentials kept outside the sandbox ([Cloudflare](https://blog.cloudflare.com/code-mode/)). Fits many chained calls over large data. Trade-off: needs a secure execution environment with resource limits and monitoring.

**Plugin-bundled server.** Server definitions shipped in a [plugin](plugins.md). Fits a server set used in several repositories. Trade-off: the plugin version, not the user, decides the server command. Admin allowlists still apply; Codex matches plugin servers under `plugins.<p>.mcp_servers.<s>.identity` ([Codex managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration)).

## Practices

1. **Prefer a known CLI plus a skill when a sandboxed shell exists.**
   - Why: the CLI runs inside the sandbox and permission rules, and its output can be filtered.
   - How: name the CLI in the task, allow its subcommands by prefix, put conventions in a skill.
   - Evidence: [Vendor] "CLI tools are the most context-efficient way to interact with external services" ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)). Sources disagree on context cost: 2025 measurements assumed eager loading ([Willison](https://simonwillison.net/2025/Oct/16/claude-skills/): GitHub's server "consumes tens of thousands of tokens"), while a Jul 2026 single-task test with deferred loading found 48–50k tokens for MCP against 45–48k for CLI plus skill ([Checkly](https://www.checklyhq.com/blog/mcp-vs-cli-token-efficiency/), [Empirical], small n). The remaining reasons for a CLI are sandboxing, output filtering and portability.
2. **Pair each server with a skill.**
   - Why: the server provides the connection, the skill the workflow.
   - How: a skill that names the qualified tools, the call order and conventions; ship both in a plugin when reused.
   - Evidence: [Vendor] ([Extend Claude Code](https://code.claude.com/docs/en/features-overview)).
3. **Enable only the tools the task needs.**
   - Why: each tool is attack surface and a choice the model must make; overlapping tools confuse it.
   - How: Codex `enabled_tools`/`disabled_tools`; Claude Code bare `deny` rules; OpenCode `permission` deny patterns.
   - Evidence: [Vendor] ([Anthropic, Writing effective tools](https://www.anthropic.com/engineering/writing-tools-for-agents)).
4. **Keep deferred tool loading on and know when it is off.**
   - Why: five servers with 58 tools cost about 55K tokens of definitions. Tool search cut about 77K to 8.7K tokens and raised MCP-eval accuracy from 49% to 74% (Opus 4).
   - How: check per-tool tokens with `/context all` in Claude Code; keep tool sets small in OpenCode and on older Codex model/provider combinations, which load all tools eagerly.
   - Evidence: [Vendor] ([Anthropic, Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use), Nov 2025; [openai/codex PR #29486](https://github.com/openai/codex/pull/29486)).
5. **Bound tool output.**
   - Why: deferral shrinks definitions, not results.
   - How: Claude Code warns above 10,000 tokens per output and saves results above `MAX_MCP_OUTPUT_TOKENS`; Codex `tools.<tool>.output_token_limit`; prefer servers that paginate.
   - Evidence: [Vendor] ([Claude Code MCP](https://code.claude.com/docs/en/mcp)).
6. **Commit shared servers without secrets; keep credential-bearing ones private.**
   - Why: project config is shared through version control.
   - How: Claude Code project `.mcp.json` for the team, local scope (`~/.claude.json`) for personal and credential-bearing servers; Codex user config versus trusted project config. Pass secrets as environment variables in each harness's syntax. Claude Code expands credential variables such as `ANTHROPIC_API_KEY` to empty for remote servers, so copy the value into your own variable name.
   - Evidence: [Vendor] ([Claude Code MCP](https://code.claude.com/docs/en/mcp)).
7. **When building a server, design few workflow-level tools.**
   - Why: consolidated tools need fewer calls and less context.
   - How: `schedule_event` instead of `list_users` + `list_events` + `create_event`; prefix tools per service; keep the server name stable because it is part of `mcp__<server>__<tool>`. No vendor gives a number beyond "few".
   - Evidence: [Vendor] ([Anthropic, Writing effective tools](https://www.anthropic.com/engineering/writing-tools-for-agents); [MCP spec, Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)).
8. **Write tool descriptions for a new team member and return concise, actionable results.**
   - Why: with deferred loading the description is also the search key; tool use examples raised accuracy on complex parameters from 72% to 90% ([Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)).
   - How: unambiguous parameter names, examples for nested parameters, a `concise` default response format, pagination with instructions for narrowing, and execution failures as `isError: true` results that name the fix.
   - Evidence: [Vendor] ([Anthropic, Writing effective tools](https://www.anthropic.com/engineering/writing-tools-for-agents); [MCP spec, Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)).
9. **Authenticate with minimal scopes and never pass tokens through.**
   - Why: a broad or forwarded token turns a confused server into access to everything the user can reach.
   - How: servers validate token audience; start with a minimal scope and step up; no static API keys in `.mcp.json` or `config.toml`.
   - Evidence: [Vendor] ([MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)).
10. **Allowlist servers by identity and pin versions.**
   - Why: a name is not a security control, and unpinned `npx -y` runs the latest release in every session. `postmark-mcp` added a backdoor in version 1.0.16; an unpinned installation can pick up such an update.
   - How: Claude Code `allowedMcpServers` by `serverUrl` or `serverCommand`, paired with `disableSideloadFlags` (which alone does not restrict `.mcp.json`, `claude mcp add` or SDK servers); Codex `requirements.toml` `identity`; pin `@x.y.z`.
   - Evidence: [Vendor] ([Claude Code plugins for orgs](https://code.claude.com/docs/en/plugins/org); [Codex managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration)); [Advisory] ([OWASP MCP04](https://owasp.org/www-project-mcp-top-10/2025/MCP04-2025%E2%80%93Software-Supply-Chain-Attacks%26Dependency-Tampering)).
11. **Never give one session private data, untrusted content and an exfiltration channel.**
   - Why: injection through tool results works even when the server is clean (GitHub MCP, May 2025, below).
   - How: read untrusted content (issues, web, email) in a [subagent](subagents.md) or session without write or outbound tools; require approval for any tool that sends data out. Read-only queries are outbound too: keep private data out of the reader and enforce allowed query arguments ([OpenAI deep research security](https://developers.openai.com/api/docs/guides/deep-research), [Vendor]; enforcement recommendation [Inference]).
   - Evidence: [Practitioner] ([Willison, lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)); [Advisory] ([Invariant Labs](https://invariantlabs.ai/blog/mcp-github-vulnerability)).
12. **Review a third-party server before connecting it, and again on every update.**
   - Why: descriptions can carry hidden instructions and can change after approval; neither lead documents detection of such changes.
   - How: read the source and `tools/list` output, check the publisher against typosquats, pin the version, check the OAuth scopes, diff `tools/list` on update.
   - Evidence: [Vendor] ([Claude Code MCP](https://code.claude.com/docs/en/mcp)); [Advisory] ([Invariant Labs](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)).

## Security

Threat model per server: is the code trustworthy (supply chain), are the descriptions trustworthy (poisoning, rug pull), are the results trustworthy (injection), are the credentials scoped. Allowlisting covers the first and part of the second. Least privilege, separated data access and enforced outbound argument/destination checks reduce injection impact (inference; [security guide](security.md#data-access-and-outbound-channels)). Read-only search still sends its arguments outside the session ([OpenAI deep research](https://developers.openai.com/api/docs/guides/deep-research)).

| Threat | Mitigation |
| --- | --- |
| Tool poisoning: hidden instructions in descriptions, visible to the model, not the UI (Invariant Labs, 2025-04-01) | Read full descriptions; pin by hash ([Invariant](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)) |
| Rug pull: descriptions change after approval | Pin versions; diff `tools/list` on update |
| Shadowing: one server's descriptions change how another server is used | Fewer servers per session |
| Injection through results: a clean server returns attacker content | Trifecta split; approval on outbound tools |
| OAuth confused deputy, SSRF via metadata URLs, `javascript:` authorization URLs | Per-client consent, exact `redirect_uri`, single-use `state`; block private ranges; validate URL schemes ([MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)) |
| Malicious startup command in a one-click install | Show the full command; explicit consent |
| Local HTTP server reached from a browser page (DNS rebinding) | Prefer stdio; for HTTP, validate present Origin and use authentication plus restricted binding or restricted IPC |

Measured susceptibility: MCPTox tested 45 live servers and 1,348 malicious cases; average attack success was 36.5%, and the highest refusal rate was under 3%. The models tested are from 2025; no 2026 data was found ([MCPTox](https://arxiv.org/html/2508.14925v1), [Empirical]).

| Date | Incident [Advisory] |
| --- | --- |
| Fixed 2025-06-17 | CVE-2025-6514, `mcp-remote` 0.0.5–0.1.15: OS command injection via a crafted `authorization_endpoint`; CVSS 9.6 ([GitLab](https://advisories.gitlab.com/npm/mcp-remote/CVE-2025-6514/)) |
| 2025 | CVE-2025-49596 (MCP Inspector < 0.14.1, RCE) and CVE-2025-58444 (Inspector, XSS to command execution, fixed 0.16.6) ([SentinelOne](https://www.sentinelone.com/vulnerability-database/cve-2025-49596/); [GitLab](https://advisories.gitlab.com/npm/@modelcontextprotocol/inspector/CVE-2025-58444/)) |
| Fixed 2025-08-20 | CVE-2025-61260, Codex CLI: a repository `.env` set `CODEX_HOME=./.codex`, and project `mcp_servers` commands ran at startup without a prompt; CVSS 9.8; fixed in v0.23.0 ([Check Point](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/)) |
| 2025 | Unofficial `postmark-mcp` on npm added an external BCC in 1.0.16 after building trust over 15 versions; Postmark's API was unaffected ([Postmark incident notice](https://postmarkapp.com/blog/information-regarding-malicious-postmark-mcp-package)) |
| Fixes 2025-08-26 to 2025-12-28 | Claude Code project files: CVE-2025-59536 (hooks RCE), MCP consent bypass via `enableAllProjectMcpServers` in project settings, API key exfiltration via `ANTHROPIC_BASE_URL` ([Check Point](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)) |

Plan around current behaviour: Claude Code loads `.mcp.json` servers without asking in `-p`, SDK and cloud runs; Codex `trust_level = "untrusted"` turns project-local config off ([Codex security](https://learn.chatgpt.com/docs/agent-approvals-security)). Do not commit `enableAllProjectMcpServers`. For headless runs in untrusted checkouts, see [automation](automation.md).

### Cross-concept checks

Use the [security guide](security.md) to connect this mechanism to the
other execution, data and persistence boundaries. Its proposed
[benign canary checks](security.md#verification-with-benign-canaries)
include C7–C11: outbound arguments, metadata changes, OAuth, transport and
client isolation. These checks are recommendations, not a completed
deployment evaluation.

## Verification and checklist

- **Status and context cost:** `/mcp` in both leads; `/context all` in Claude Code for tokens per tool.
- **CLI versus MCP:** run the same task with and without the server; compare tokens and success.
- **Server quality:** run a held-out set of realistic multi-step tasks in both leads; measure success, tool calls, tokens and errors ([Anthropic, Writing effective tools](https://www.anthropic.com/engineering/writing-tools-for-agents)). Confirm tool search finds each tool from a natural-language request.
- **Admin allowlist:** add an unlisted server with `claude mcp add` or `codex mcp add` and confirm it is refused.
- **Trust gate:** open the repository untrusted and confirm with `ps` that no MCP process starts.
- **Headless CI:** fail a run on `mcp_server_errors` in the Claude Code `system/init` event.

Checklist:

- [ ] Each server has a reason a CLI plus skill would not do (auth, state, no CLI, no shell).
- [ ] Each server has a companion skill.
- [ ] Only needed tools are enabled; output limits are set.
- [ ] Outbound and write tools need approval; no auto-approved writes on servers that read untrusted content.
- [ ] Commands pin versions.
- [ ] No secrets in `.mcp.json`, `config.toml` or `opencode.json`; credential-bearing servers are in local or user scope.
- [ ] The admin allowlist matches by command or URL.
- [ ] Third-party servers were reviewed and are re-reviewed on update.
- [ ] Own servers: workflow-level tools, examples in descriptions, `isError` messages, instructions within 512 characters, both approval hints.

## Portability

The leads share no MCP config file. Define each server once per harness. The same stdio server in Claude Code `.mcp.json`, Codex `.codex/config.toml` and OpenCode `opencode.json`:

```json
{ "mcpServers": { "context7": { "type": "stdio", "command": "npx", "args": ["-y", "@upstash/context7-mcp"] } } }
```

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

```json
{ "mcp": { "context7": { "type": "local", "command": ["npx", "-y", "@upstash/context7-mcp"] } } }
```

Rules:

- **Use the same server name everywhere,** so permission rules and hook matchers target the same `mcp__<name>__<tool>` in both leads.
- **Use stdio or streamable HTTP.** Other transports exist only in Claude Code.
- **Always set `type` in Claude Code.** An entry with `url` but no `type` is an error; Codex has no `type` field.
- **Put the important part of server instructions in the first 512 characters** (Codex); Claude Code truncates at 2,048.
- **Set timeouts explicitly** if startup is slow: the defaults are 30 s, 10 s and 5 s.
- **Emit both approval hints** on destructive tools: `_meta["anthropic/requiresUserInteraction"]` and the destructive annotation.

Traps:

- **Repository servers load differently.** Claude Code asks per server interactively but not in `-p`, SDK or cloud runs; Codex loads them after project trust, without a per-server prompt.
- **"Local scope" in Claude Code is `~/.claude.json`,** not `.claude/settings.local.json`.
- **Claude Code settings files skip MCP permission rules with parentheses;** use `--disallowedTools` for parameter rules.
- **A Claude Code hook matcher `mcp__memory` matches nothing;** use `mcp__memory__.*`.
- **Context cost differs:** a server with many tools that is cheap in Claude Code can be expensive in OpenCode.
- **Codex can no longer run as an MCP server.** `codex mcp-server` was removed in September 2026; use the app-server protocol.

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| SSE, WebSocket and SDK transports; `claude mcp serve`; `--strict-mcp-config`; local scope in `~/.claude.json` | Claude Code | No Codex counterpart. |
| `alwaysLoad`, MCP resources as `@server:...`, `_meta` keys `anthropic/alwaysLoad` and `anthropic/maxResultSizeChars` | Claude Code | No documented Codex counterpart. |
| MCP prompts as slash commands | Claude Code, OpenCode | Not recorded for Codex. |
| `required` servers, `mcp_optional_startup_grace_ms`, `experimental_environment`, remote `env_vars` sources | Codex | No Claude Code counterpart. |
| OAuth client registration details, CIMD | Codex | The Claude Code side was not researched in enough detail to compare. |
| Vendor-account connectors (claude.ai connectors, Codex apps) | Both | Tied to one vendor's account system. |
| `opencode mcp debug` | OpenCode | No lead counterpart. |

## Open questions

- The fetched Codex user docs do not describe tool search; only PR #29486 does.
- No controlled study after deferred loading compares MCP and CLI across many tasks; Checkly is one task.
- Codex's default `output_token_limit` is not documented, nor whether a server defined in user and project config is replaced or merged.
- No vendor quantifies the ideal number of tools per server.
- Not re-verified whether Claude Code reads `readOnlyHint`/`destructiveHint` annotations for approval.
- Neither lead documents rug-pull detection; treat it as absent.
- No MCPTox-style data for 2026 models.

## Sources

Vendor pages: [Claude Code: MCP](../vendors/claude-code/mcp.md), [Codex: MCP](../vendors/codex/mcp.md), [OpenCode: MCP](../vendors/opencode/mcp.md), [OpenCode: configuration](../vendors/opencode/configuration.md). Research notes: [MCP and plugins](../research-notes/agent-harness-best-practices/mcp-plugins.md).

- Claude Code: [best practices](https://code.claude.com/docs/en/best-practices), [Extend Claude Code](https://code.claude.com/docs/en/features-overview), [MCP](https://code.claude.com/docs/en/mcp), [plugins for orgs](https://code.claude.com/docs/en/plugins/org)
- Codex: [MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security), [managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration), [PR #29486](https://github.com/openai/codex/pull/29486)
- Anthropic: [Writing effective tools](https://www.anthropic.com/engineering/writing-tools-for-agents), [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use), [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp); [Cloudflare Code Mode](https://blog.cloudflare.com/code-mode/)
- MCP spec: [Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools), [Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
- Practitioner and empirical: [Zechner](https://mariozechner.at/posts/2025-08-15-mcp-vs-cli/), [Willison, skills](https://simonwillison.net/2025/Oct/16/claude-skills/), [Willison, lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/), [Checkly](https://www.checklyhq.com/blog/mcp-vs-cli-token-efficiency/), [MCPTox](https://arxiv.org/html/2508.14925v1)
- Advisories: [Invariant, tool poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks), [Invariant, GitHub MCP](https://invariantlabs.ai/blog/mcp-github-vulnerability), [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/), [CVE-2025-6514](https://advisories.gitlab.com/npm/mcp-remote/CVE-2025-6514/), [CVE-2025-49596](https://www.sentinelone.com/vulnerability-database/cve-2025-49596/), [CVE-2025-58444](https://advisories.gitlab.com/npm/@modelcontextprotocol/inspector/CVE-2025-58444/), [CVE-2025-61260 (NVD)](https://nvd.nist.gov/vuln/detail/cve-2025-61260), [Check Point, Codex CLI](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/), [Check Point, Claude Code](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/), [postmark-mcp (Postmark notice)](https://postmarkapp.com/blog/information-regarding-malicious-postmark-mcp-package)
