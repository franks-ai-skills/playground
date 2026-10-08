# Claude offline startup-inventory result

Status: **host startup inventory observed** on 2026-10-08. The control
reported `tools: ["Read"]`; the source-support candidate reported
`tools: []`. Both came from actual `system/init` events with
`model: "claude-opus-5-5"` and `apiKeySource: "none"`.

This resolves the missing Claude host-inventory observation identified
by Opus's review. It does not certify an isolated worker, qualify a
guest build, establish Codex support or authorize T3.

## Authorization and cost boundary

The user authorized the [follow-up](2026-10-08-harness-forge-offline-init-follow-up.md)
only if it incurred no extra cost, with subscription usage only and no
additional API tokens/keys or API credits. This restriction is now
recorded in the parent design, scope and implementation plan. A direct
model API adapter is excluded under that constraint.

The probe used the requested `claude-tp` zsh definitions with guards
against login/logout changes and non-subscription authentication.
Local status reported `authMethod: "claude.ai"`, subscription type
`team`, and no API-key source. The subprocess environment contained
only HOME, PATH, USER, LOGNAME, LANG and TMPDIR; inherited API/provider
variables were not passed. No API credential, credit, billing or account
configuration was added or changed. `claude-frank` remains the default
after this diagnostic-only exception.

Before sending a prompt, deterministic controls verified the OS profile
`(version 1)(allow default)(deny network*)`:

- Four positive local controls connected outside the restriction:
  IPv4, IPv6, Unix sockets and the hostname `localhost`.
- All seven corresponding/direct network attempts inside the restriction
  returned `EPERM`: those four cases, external IPv4 and IPv6 TCP, and
  external UDP. This was policy-denial evidence, not only a DNS error.
- The same seven attempts in a child process also returned `EPERM`,
  under the same effective user identity.

Each CLI launch used that OS profile and closed inherited extra file
descriptors. The network block remained in place throughout. Neither
stream contained an assistant/model response or a terminal usage/cost
event. The no-extra-cost basis is externally blocked provider access;
this was not a provider billing query, and missing cost fields are not
being represented as a CLI-reported zero-dollar bill.

## Observations

Claude Code 2.1.292, Darwin arm64, retained its recorded binary SHA-256:
`97a01e5bc74a199e67189435d0331ea3a24eac2e07db4b76d9148c5b0386138f`.
Both launches used an empty temporary working directory, the guarded
wrapper, pinned model, safe/restricted flags, empty MCP configuration,
disabled settings/hook discovery and the same harmless synthetic prompt.
The control selected `Read`; the candidate selected no tools.

| Check | Control | Restricted candidate |
| --- | --- | --- |
| First captured event | `system/init` | `system/init` |
| Explicit tools array | `["Read"]` | `[]` |
| Requested and reported model | `claude-opus-5-5` | `claude-opus-5-5` |
| API-key source | `none` | `none` |
| Assistant or terminal result events | None | None |
| Internal `api_retry` events | 6 | 6 |
| Captured stdout/stderr | 3,619 bytes | 3,616 bytes |
| Termination | SIGTERM at 30-second cap | SIGTERM at 30-second cap |

The startup event appeared before the captured retry events. The trace
does not locate the first attempted network call relative to init; it
establishes that init can be observed while outbound access is denied.

There were no process relaunches, account switches or model fallbacks.
The CLI did perform internal retry handling: six `api_retry` events per
process, all under the same network prohibition. The plan's no-retry
limit was enforced at process-launch level; it was not a disabled SDK
retry policy. These events are preserved, not counted as successful
model calls or hidden by a claim that no request was attempted.

Both processes timed out and were terminated. That is acceptable for
this narrow startup observation; neither is a successful completed
source-support worker run. The M1 full-run grader was not used. The
selected account profile remained available to these host processes,
so authentication isolation remains unqualified.

## Evidence, budget and next boundary

The experiment started at 18:14:01 UTC; both probes were complete by
18:20:06 UTC, within the additional 30-minute active-work allowance.
No interruption was counted as active work in this follow-up.

The local forge index
`evals/canaries/results/offline-init-2026-10-08-index.json` records nineteen
hashed artifacts: deterministic controls, launcher/auth preflight,
runner source, exact commands/prompts, raw streams and assessments.
Raw files remain ignored under `evals/canaries/results/private/offline-init-2026-10-08/`.
Prior M1 and diagnostic indexes and streams remain unchanged.

Two prompt-bearing invocations are charged against the original thirty,
leaving twenty-eight. Both permitted configuration corrections are now
charged. There have been no live qualification runs, model responses,
container setups or production support declarations.

Claude's host startup-inventory gap is resolved. The remaining work is
proof of Codex's complete tool-removal configuration and the guest,
authentication and role boundaries in both harnesses. Further diagnostic
work needs a concrete bounded handoff within the subscription-only
constraint; API access or API credits are not fallback options. T3
remains stopped until those feasibility decisions are settled.
