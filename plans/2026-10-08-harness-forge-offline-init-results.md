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
configuration was added or changed. `claude-frank` remains the owner's
temporary local-development selection after this diagnostic-only exception.
These names are not public product defaults; the
[development boundary](harness-forge-local-development.md) governs later runs.
The observation applies only to the tested `claude-tp` Team profile,
binary, model and flags. It does not carry over to `claude-frank` or
another account: account/managed-policy equivalence was not tested.

Before sending a prompt, deterministic controls verified the OS profile
`(version 1)(allow default)(deny network*)`:

- Four positive local controls connected outside the restriction:
  IPv4, IPv6, Unix sockets and the hostname `localhost`.
- All seven corresponding/direct network attempts inside the restriction
  returned `EPERM`: those four cases, external IPv4 and IPv6 TCP, and
  external UDP. This was policy-denial evidence, not only a DNS error.
- The same seven attempts in a child process also returned `EPERM`,
  under the same effective user identity.

The name-based case was only `localhost`. An external hostname lookup
through the system resolver was not tested, and no machine-wide DNS or
packet capture was collected. Direct UDP denial does not establish that
OS-service-mediated resolution cannot emit traffic. The review's proposed
DNS escape is therefore an untested hypothesis, not an observed leak or
a proven block. “Network-blocked” here means the measured socket
operations were denied; it is not proof of zero outbound machine traffic.

Each CLI launch used that OS profile and closed inherited extra file
descriptors. The network block remained in place throughout. Neither
stream contained an assistant/model response or a terminal usage/cost
event. The no-extra-cost basis is externally blocked provider access;
this was not a provider billing query, and missing cost fields are not
being represented as a CLI-reported zero-dollar bill. Retry events alone
would not prove non-delivery or non-billing; the cost argument rests on
the socket-denial controls together with subscription authentication and
the absence of an API-key source, with the resolver limit stated above.

## Observations

Claude Code 2.1.292, Darwin arm64, retained its recorded binary SHA-256:
`97a01e5bc74a199e67189435d0331ea3a24eac2e07db4b76d9148c5b0386138f`.
Both launches used an empty temporary working directory, the guarded
wrapper, pinned model, safe/restricted flags, empty MCP configuration,
settings/hook-discovery controls and the same harmless synthetic prompt.
The control selected `Read`; the candidate selected no tools.

Both init events also advertised the following metadata despite the
restricted tool selections:

- **19 skills:** `deep-research`, `design`, `design-sync`, `dataviz`,
  `update-config`, `verify`, `debug`, `code-review`, `simplify`, `batch`,
  `fewer-permission-prompts`, `doctor`, `loop`, `schedule`, `claude-api`,
  `workflow-authoring`, `run`, `run-skill-generator`, `plugin-authoring`.
- **4 agents:** `claude`, `Explore`, `general-purpose`, `Plan`.
- **4 plugins marked `builtin`:** `cc-plugin-sec-default`,
  `cc-plugin-agents-md`, `cc-plugin-telemetry`, `cc-plugin-plugin-authoring`.

This is observed startup metadata, not a captured model prompt. The init
event does not establish which skill/agent bodies, plugin instructions
or discovered files would enter model context. It does not label the
origin of every skill or agent. In particular, a plugin named
`cc-plugin-agents-md` is not proof that an instruction file was read.
The empty tools array still establishes the narrow advertised-tool
observation: neither Skill nor Agent is advertised as a callable tool.
It does not establish absence of automatic harness discovery or all
file access by the harness itself. The context/discovery acceptance row
remains open and must account for these advertised components.

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
establishes that init can be observed under the tested socket-denial
profile. It does not establish absence of all outbound DNS traffic.

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
The twenty-eight unused slots are not permission to revise the current
candidate again. A new Codex configuration/probe experiment, including
an offline one, requires its own bounded execution handoff. Reviewing
existing evidence and correcting these reports does not consume a new
experimental handoff.

Claude's host startup-inventory gap is resolved. The remaining work is
proof of Codex's complete tool-removal configuration and the guest,
authentication and role boundaries in both harnesses. Further diagnostic
work needs a concrete bounded handoff within the subscription-only
constraint; API access or API credits are not fallback options. T3
remains stopped until those feasibility decisions are settled.

The [current decision brief](2026-10-09-harness-forge-decisions.md)
separates the parity choice from the remaining qualification work.

Subsequent work: the user approved one final [Codex catalog spike](2026-10-09-harness-forge-catalog-spike-results.md).
It accepted the configuration but did not close parity. The decision brief
records the user's subsequent choice of option 3: automated workers with
weaker isolation and README disclosure. The Claude observations and
accounting in this report are unchanged.
