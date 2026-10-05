# Security across the agent-harness concepts

Researched and sources fetched on 2026-10-05. This pass covers attacks
against coding-agent deployments, their trust boundaries, defenses and
defensive verification. It supplements the earlier concept-specific
research; it does not establish that a particular deployment is secure.

## Audit before the new research

Security was already researched. The existing
[best-practice notes](agent-harness-best-practices/) contain security
findings, and the [guide](../guide/README.md) carries them into most
concept pages:

| Existing coverage | Where | Gap motivating this pass |
| --- | --- | --- |
| Instruction-file injection; memory persistence risk | [Instructions](../guide/instructions.md#security) | Cross-session evidence and memory recovery |
| Malicious skill prose, scripts and marketplaces | [Skills](../guide/skills.md#security) | Plausible prerequisites, remembered approvals and runtime tests |
| Pre-consent startup execution and endpoint redirection | [Configuration](../guide/configuration.md#security) | Separation of historical defects from current trust behavior |
| Command-pattern bypass, DNS disclosure, sandbox exclusions | [Permissions](../guide/permissions-and-sandbox.md#security) | Coverage of every process/tool and allowed outbound channels |
| Poisoning, shadowing, rug pulls and OAuth | [MCP](../guide/mcp.md#security) | Current revision, discovery SSRF and cross-client isolation |
| Privileged extensions and update risk | [Plugins](../guide/plugins.md#security) | Separate package integrity from remote metadata integrity |
| Untrusted delegated output | [Subagents](../guide/subagents.md#security) | Provenance of approval claims and constrained handoffs |
| Privileged handlers; bypass and fail-open behavior | [Hooks](../guide/hooks.md#security) | Event-specific failures and fault-injection checks |
| Issue/PR injection and runner secrets | [Automation](../guide/automation.md#security) | Artifact/cache poisoning, approval races, recovery and budgets |

**Assessment:** a deeper pass is warranted. The earlier material is
organized by mechanism; an attack can cross several mechanisms. The
missing deliverable is a shared threat model with observable negative
tests, not another unsorted CVE list. This is an editorial assessment of
the linked repository content.

## Method and evidence boundaries

The [source policy](../sources.md) applies. Findings below use fetched
primary documentation, specifications, maintainer advisories, original
security research and research papers. Search snippets and unfetchable
pages are not evidence. No X posts or mirrors were used.

Labels: **[Vendor]** documented behavior or vendor guidance;
**[Specification]** protocol requirements; **[Advisory]** a disclosure
or first-party incident notice; **[Empirical]** a controlled experiment,
including preprints; **[Inference]** a proposed engineering control or
test derived from the cited evidence. A demonstrated attack is not an
in-the-wild incident. A historical patched defect is not a claim that
current releases remain vulnerable.

Local version checks returned Claude Code 2.1.289 and codex-cli 0.160.0.
The existing vendor baseline remains 2026-10-04; this security pass has
its own date. Documentation requirements do not establish that those
installed binaries implement every control. No exploit, malicious
package, live credential-disclosure test or harness red-team suite was
executed. Verification cases below are proposed benign checks.

## 1. External data becomes instructions

**[Vendor]** OpenAI describes injections that redirect tool use and
leak private data. It recommends keeping untrusted variables out of
developer messages and restricting handoffs to structured fields
([agent workflow safety][workflow-safety]). **[Specification/guidance]**
OWASP documents indirect, multimodal, split and encoded payloads; it
does not claim a foolproof prevention method ([LLM01][llm01]).

**Attack:** an attacker controls issue text, a fetched document, image,
dependency README or tool result. The agent interprets that content as
an instruction to change the task, disclose data or disable a control.

**[Inference] Defense/check:** retain source provenance and low-trust
labels through extraction and delegation. Test a plain-text fixture,
an image and a split/encoded fixture asking for an unrelated harmless
marker change. Grade the action trace and diff, not just the final
refusal. Filtering and better prompts supplement capability limits.

## 2. Dependency execution poisons project guidance and review

**[Empirical; older experiment]** NVIDIA demonstrated a malicious Go
dependency writing an untracked `AGENTS.md`, causing Codex to insert a
delay, and using code comments to influence the summary. The article
was published 2026-04-20; disclosure began 2025-07-01. No tested harness
version is specified. Existing dependency code execution is an attack
prerequisite; OpenAI judged the incremental risk comparable to
dependency compromise ([NVIDIA original][nvidia]).

**[Inference] Defense/check:** review build/install scripts and protect
instruction-file changes. In a disposable checkout, manually introduce
an inert unexpected instruction file and misleading diff comment.
Require the reviewer to report both the unexpected file and the actual
change. A tracked-files-only check misses untracked instructions.

## 3. Skills turn plausible preparation into execution

**[Empirical; preprint]** SkillJect v3, revised 2026-06-16, tests poisoned
skills that direct agents to helper scripts as required preparation.
Its success metric records helper execution; subsequent harm depends
on permissions and isolation. Claude Code and OpenClaw are evaluated
with several backends; this is not a current-version malware incidence
estimate ([SkillJect][skillject]).

**[Vendor]** Claude Code checks dynamic skill commands against
permissions, but workspace trust does not gate a skill's `allowed-tools`.
Managed permission rules can ignore these grants, and
`disableSkillShellExecution` disables injected commands from the
documented non-managed sources; it is not a universal script-execution
ban ([skills reference][cc-skills]).

**[Inference] Defense/check:** inspect helpers, dependencies and fetched
artifacts as well as prose. A fixture skill's mandatory setup helper
should only print a canary; confirm it cannot run under a deny rule.
Repeat with shell preprocessing disabled. Catalog metadata and a static
scan do not establish the safety of referenced code.

## 4. Remembered approvals and output links broaden disclosure

**[Empirical; historical demonstration, 2025-10-30]** Schmotz et al.
showed approval for presentation-editing Python carrying over to a
different helper that uploaded a file. In their Claude web experiment,
network restrictions stopped a direct upload; a generated link instead
embedded a password and disclosed it if opened. This is not a measured
regression in today's harnesses ([Agent Skills injection][skill-approval]).

**[Inference] Defense/check:** approve the actual executable, script
contents, data and destination. With synthetic data, test a second
helper after a narrowly approved first helper; inspect output links
without visiting them. A restriction on shell HTTP does not cover a
user-mediated link or browser-rendered output.

## 5. Memory poisoning survives the conversation

**[Empirical; preprint, 2026-09-12]** PMPA studies external text, images
and PDFs causing memory writes, then disclosure in another session.
The experiments use Claude Code/OpenClaw with DeepSeek-V4-Flash,
DeepSeek-V4-Pro and Qwen3-Max, plus local JSON workspace simulations
and scenario skills. Harness versions are not stated. Prompt reminders
reduce insertion but provide limited protection after poisoning;
headline rates must not be generalized to default Claude deployments
([PMPA, setup and defense sections][pmpa]).

**[Inference] Defense/check:** review persistent writes and retain their
origin. Summarize a synthetic document requesting a future response
marker; inspect memory, then start a fresh session and exercise its
trigger. Restore contaminated memory from reviewed state as part of
recovery. A fresh conversation alone does not remove persistent state.

## 6. Delegation launders apparent authority

**[Vendor]** Claude Code labels team messages as agent-originated;
teammates cannot provide human consent. Auto mode treats relayed
approval claims as untrusted and reviews messages before delivery.
These are Claude-specific documented controls, not a portable guarantee
([agent teams, messages between agents][cc-teams]).

**[Inference] Defense/check:** a worker's report must not widen the
parent's authorized scope. Return a synthetic claim that the user
approved an unrelated canary write and confirm that it grants no
permission. Preserve source identity in handoffs. Schema validation
reduces unconstrained text but does not validate the meaning or
authorization of every field: structured outputs can contain mistakes
([OpenAI Structured Outputs][structured]).

## 7. Read-only tools can be outbound channels

**[Vendor]** OpenAI documents an MCP search result asking the agent to
put private data in its next search query. A read-only API still sends
arguments to its operator ([deep research security][deep-research]).
**[Empirical]** Invariant's 2025-05-26 demonstration used clean GitHub
MCP tools, a public issue, private repositories and a public PR; it was
a Claude Desktop/Claude 4 Opus experiment, not a GitHub breach
([GitHub MCP experiment][github-mcp]).

**[Inference] Defense/check:** separate hostile-content readers from
private-data readers and constrain outbound arguments and publication
destinations. A public fixture issue must not cause a private synthetic
marker to appear in search arguments, a PR, URL or log. Test allowed
destinations as well as blocked domains. “No write tools” alone is not
an exfiltration defense.

## 8. Metadata poisoning differs from package poisoning

**[Empirical, 2025-04-01]** Invariant demonstrates poisoned descriptions,
metadata changing after approval, and one server influencing another
server's calls without invoking its own tool ([tool poisoning][poisoning]).
**[Specification]** Tool annotations are untrusted unless supplied by a
trusted server ([MCP Tools, 2026-07-28][mcp-tools]).

**[Inference] Defense/check:** review and snapshot complete definitions
and server instructions; detect changes before exposing them to the
model. Package pins do not freeze remote descriptions or results.
Modify a harmless server's metadata and require re-review. Checksums
detect change, not malicious intent in the original artifact.

## 9. Connector updates can carry real backdoors

**[Advisory; first-party notice, 2025-09-25]** Postmark confirms a fake
`postmark-mcp` package built trust over 15 versions, then added an
external BCC in 1.0.16. It was not an official connector; Postmark's
legitimate API was unaffected. Its response advice is removal, email-log
inspection and consideration of rotating credentials sent in email
([Postmark incident notice][postmark]). This primary source replaces
the earlier trade-press citation; it does not support “first-ever”.

**[Vendor]** Claude plugin permissions govern the agent's tool calls,
not independently running plugin code; hooks, servers and mod processes
need their own confinement ([plugin security][cc-plugin-security]).

**[Inference] Defense/check:** verify publisher identity through vendor
documentation; pin reviewed packages and review updates. Use fictional
messages to inspect all recipients and actual process network access.
An approved name or unchanged description cannot detect every code
backdoor. A worktree separates edits, not process privileges.

## 10. OAuth authorizes the wrong client or resource

**[Specification, 2026-07-28]** MCP requires resource indicators,
intended-audience validation, and validation of the authorization
response issuer before exchanging its code. A returned `iss` must
match even if support was not advertised; missing `iss` must be rejected
when advertised ([authorization][mcp-auth]). PKCE is required and
metadata lacking support must cause refusal. Tokens for upstream APIs
are separate from incoming MCP tokens; passthrough is forbidden.
Static-client-ID proxies require consent for each dynamically registered
client ([authorization security][mcp-auth-security]).

**[Inference] Defense/check:** use dummy issuers, clients and tokens.
Wrong issuer must cause no code exchange; wrong audience must be
rejected; client B must not inherit client A's consent. Validate PKCE,
redirect binding and requested scope separately. PKCE does not prove
which process owns a localhost callback. A missing issuer can still be
accepted when issuer support was not advertised; do not overstate the
requirement.

## 11. Discovery and local HTTP cross network boundaries

**[Specification, 2026-07-28]** Streamable HTTP requires validation of
present `Origin`; an invalid one receives 403. Local-only binding and
authentication are additional recommendations ([transport][mcp-http]).
**[Vendor/specification guidance]** MCP security guidance covers SSRF
through discovery and CIMD URLs, redirects, DNS changes between check
and use, unsafe authorization URL schemes, and web-accessible stdio
proxies ([security tutorial][mcp-security]).

**[Inference] Defense/check:** exercise a disposable server with invalid
Origin and Host, and a discovery fixture redirecting to a harmless
private canary endpoint. Validate each redirect and resolved address at
the actual request boundary. A localhost bind alone is insufficient;
direct stdio and a network-exposed process-spawning proxy differ.

## 12. Correct credentials do not ensure client isolation

**[Advisory]** GHSA-w48q-cv73-mx4w, published 2025-12-02, affects
TypeScript SDK <1.24.0: unauthenticated localhost HTTP servers lacked
default rebinding protection. The fix helps `createMcpExpressApp()`;
custom Express apps need appropriate middleware. Direct stdio is
unaffected ([maintainer advisory][sdk-rebinding]).

**[Advisory]** GHSA-345p-7cg4-v4c7, published 2026-02-04, affects
SDK >=1.10.0 through 1.25.3, patched in 1.26.0. Reused server/transport
instances can route responses or intermediate messages to another
client. Patched guards surface misuse as errors; applications may need
changes ([maintainer advisory][sdk-isolation]).

**[Inference] Defense/check:** test the actual application, not only an
SDK example. Two dummy users send overlapping concurrent requests with
equal JSON-RPC IDs and distinct canaries; neither may receive the other's
responses or notifications.
These historical SDK advisories do not establish a current deployment's
protocol revision or vulnerability status.

## 13. Startup and execution controls have different scope

**[Advisory]** `claude-code-action` GHSA-8q5r-mmjf-575q, published
2026-05-20, affected versions <1.0.74; fixed in 1.0.74. Attacker PR
MCP configuration could execute commands on a privileged runner
([maintainer advisory][action-advisory]). **[Vendor]** Current Claude
headless documentation says `-p` skips workspace/server prompts; bare
mode omits automatic discovery but explicitly supplied components
still need review ([headless][cc-headless]).

**[Vendor]** Claude's Bash sandbox does not cover every file/web tool,
hook or MCP process ([sandbox scope][cc-sandbox]). OpenAI separately
recommends isolating whole workloads and keeping third-party credentials
outside executable environments; injecting a secret into an environment
still exposes it to generated code ([environment security][env-security]).

**[Inference] Defense/check:** inventory every executor, startup source,
network path and credential. With dummy files, compare shell, file tools
and external processes. Review startup configuration before launching
an unknown checkout. Scope credentials at the downstream service.

## 14. Hooks can fail to decide, or interpret input as code

**[Vendor]** Claude `PreToolUse` command/HTTP/MCP timeouts continue normal
permission flow; SDK callback timeouts block. `PermissionRequest`
ignores exit 2 and requires its structured decision. These rules must
not be collapsed into “exit 2 makes every hook fail closed”
([hooks, timeouts and decision control][cc-hooks]).

**[Vendor; review correction]** On events where exit 2 blocks, valid JSON
cannot override the block. For other exit codes in the standard decision
model, valid JSON determines the outcome; malformed output normally
produces a non-blocking error. `PermissionRequest` has its separate
decision contract ([hooks output precedence][cc-hooks]).

**[Inference] Defense/check:** parse JSON, pass arguments without `eval`,
resolve paths and reject escape outside an allowed root. Test malformed
input/output, missing handlers, timeout, alternate tools and an inert
symlink escape. Use event-specific denial and retain independent
permissions/isolation if the hook never runs. `PostToolUse` cannot undo
an already completed disclosure.

## 15. Privileged CI consumes hostile code and artifacts

**[Vendor]** GitHub documents shell injection through context values,
privileged `pull_request_target`/`workflow_run` checkout risk, and
cross-job compromise through shared resources ([secure use][gh-secure]).
`workflow_run` may hold secrets/write tokens absent from the earlier
workflow ([events][gh-events]). **[Vendor; first-hand research]** GitHub
Security Lab documents untrusted artifacts and the race between label
approval and a later PR update ([pwn requests][pwn-requests]).

**[Inference] Defense/check:** an unprivileged producer emits data to a
fresh privileged consumer that validates provenance, run ID, approved
SHA, schema and destination. Do not execute supplied artifacts, restore
hostile executable caches or check out untrusted heads there. Test a
noninteger artifact field and a changed SHA with dummy fixtures. Passing
a schema or an earlier workflow does not confer publication authority.

**[Vendor]** `codex-action` recommends being last in its job because the
agent may leave processes or modify files used by later privileged
steps ([action security][codex-action]). A separate job must also avoid
shared hostile executable state; merely naming two jobs is insufficient.

## 16. Output handling, exhaustion, detection and recovery

**[Specification/guidance]** OWASP LLM05 treats generated shell, SQL,
HTML and paths as untrusted input to their respective consumers
([improper output handling][llm05]). LLM07 requires authorization outside
the prompt and excludes secrets from prompts ([prompt leakage][llm07]).
LLM10 recommends limits, timeouts and monitoring against resource and
cost exhaustion ([unbounded consumption][llm10]).

**[Inference] Defense/check:** validate action semantics and authorization
in addition to JSON shape; use argument APIs and parameterized queries.
Set external wall-time, process, disk, retry, concurrency and spend
limits. Test an oversized harmless response or repeated dummy request
and require bounded failure, not a success report.

**[Vendor]** GitHub warns masking is not guaranteed and recommends
deleting exposed logs and rotating secrets ([secure use][gh-secure]).
**[Inference] Recovery:** stop affected work, isolate the runner, retain
access-controlled evidence, revoke credentials, and review modified
instructions, memory, settings, hooks and artifacts before rebuilding
from reviewed state. Record denied and completed actions without raw
secrets. This procedure combines the cited persistence, privileged
execution and incident evidence; it is not a vendor-provided playbook.

## What remains unestablished

- No source here certifies resistance for our installed harness/model/
  configuration combination. Mechanism evidence is not a universal
  attack-success rate.
- MCP 2026-07-28 is the current specification, per
  [versioning][mcp-versioning]; older implementations may negotiate
  legacy revisions. Current application state handles and legacy
  protocol sessions must not be conflated.
- A source or package allowlist establishes an identity boundary; it
  does not make every result, dependency, update or user-generated issue
  safe. Independent checks are still required at each consumer.
- The proposed canary suite needs execution in an isolated deployment
  with synthetic credentials. Documentation review alone cannot verify
  enforcement.

## Source locations

All referenced pages were fetched on 2026-10-05. Versioned paper URLs
and specification revisions preserve the evidence used; live vendor
pages can change. Claims above name their scope and source beside them.

[workflow-safety]: https://developers.openai.com/api/docs/guides/agent-builder-safety
[structured]: https://developers.openai.com/api/docs/guides/structured-outputs
[deep-research]: https://developers.openai.com/api/docs/guides/deep-research
[env-security]: https://developers.openai.com/api/docs/guides/agents-api/environments/security
[llm01]: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
[llm05]: https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/
[llm07]: https://genai.owasp.org/llmrisk/llm072025-system-prompt-leakage/
[llm10]: https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/
[nvidia]: https://developer.nvidia.com/blog/mitigating-indirect-agents-md-injection-attacks-in-agentic-environments/
[skillject]: https://arxiv.org/html/2602.14211v3
[skill-approval]: https://arxiv.org/html/2510.26328v1
[pmpa]: https://arxiv.org/html/2609.13889v1
[cc-skills]: https://code.claude.com/docs/en/skills
[cc-teams]: https://code.claude.com/docs/en/agent-teams
[cc-plugin-security]: https://code.claude.com/docs/en/plugins/security
[cc-headless]: https://code.claude.com/docs/en/headless
[cc-sandbox]: https://code.claude.com/docs/en/sandboxing
[cc-hooks]: https://code.claude.com/docs/en/hooks
[poisoning]: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
[github-mcp]: https://invariantlabs.ai/blog/mcp-github-vulnerability
[postmark]: https://postmarkapp.com/blog/information-regarding-malicious-postmark-mcp-package
[mcp-versioning]: https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning
[mcp-tools]: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
[mcp-auth]: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
[mcp-auth-security]: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations
[mcp-http]: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http
[mcp-security]: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices
[sdk-rebinding]: https://github.com/modelcontextprotocol/typescript-sdk/security/advisories/GHSA-w48q-cv73-mx4w
[sdk-isolation]: https://github.com/modelcontextprotocol/typescript-sdk/security/advisories/GHSA-345p-7cg4-v4c7
[action-advisory]: https://github.com/anthropics/claude-code-action/security/advisories/GHSA-8q5r-mmjf-575q
[gh-secure]: https://docs.github.com/en/actions/reference/security/secure-use
[gh-events]: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
[pwn-requests]: https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/
[codex-action]: https://github.com/openai/codex-action/blob/main/docs/security.md
