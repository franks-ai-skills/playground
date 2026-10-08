# Worker diagnostic: no-model gate result

Status: **stopped, unproven** on 2026-10-08. No launcher is certified.
The user approved the [bounded diagnostic](2026-10-08-harness-forge-worker-diagnostic.md),
and its no-model gate ran. Zero live harness/model invocations were
made; container setup, controls, qualification and T3 did not start.
The M1 code, grader and evidence index remain unchanged.

## Budget and stopping point

The gate started at 10:36:04 UTC with a deadline of 11:06:04 UTC.
After the conversation interruption/resumption, the clock read
12:58:28 UTC. The deadline had elapsed with incomplete evidence; the
diagnostic was closed rather than resetting its budget. This does not
mean that 142 minutes of active gate investigation were performed.
Subsequent work records and reviews the result, rather than running
new capability probes. There were zero configuration corrections and
zero live calls. The approved four-hour ceiling was not used to extend
the shorter gate.

## Codex findings

The installed Darwin arm64 binary is codex-cli 0.160.1. Its SHA-256
matches the executable inside the vendor's release archive, whose
SHA-256 matches the published release digest. The release tag resolves
to source commit `d27764b82f7118f674371e6d6e76271d9d606edb`.
This establishes release-asset identity, not a reproducible-build
attestation. The Linux guest candidate was identified in the release
metadata but was neither downloaded nor executed.
Source: [vendor release](https://github.com/openai/codex/releases/tag/rust-v0.160.1).

The vendor-source suggestion was useful, with these qualifications:

- **The image setting has a version-specific answer.** The release
  schema defines `features.view_image`, whereas `ToolsToml` has no
  `view_image` field. The source registers the image handler only when
  an environment exists and that feature is enabled. M1's rejected
  `tools.view_image` override therefore did not establish that image
  access is unavoidable.
  Sources: [release schema](https://github.com/openai/codex/releases/download/rust-v0.160.1/config-schema.json),
  [registration](https://github.com/openai/codex/blob/d27764b82f7118f674371e6d6e76271d9d606edb/codex-rs/core/src/tools/spec_plan.rs#L1283-L1298).
- **Shell/image toggles do not remove every tool.** `apply_patch`
  registration depends on the environment and model metadata. Other
  utility tools can also depend on model metadata. No selected-model,
  strict-valid complete configuration was established during the gate.
  Source: [utility registration](https://github.com/openai/codex/blob/d27764b82f7118f674371e6d6e76271d9d606edb/codex-rs/core/src/tools/spec_plan.rs#L1151-L1300).
- **An internal empty allowlist exists.** `ToolPolicy.allowed_tools`
  supports an empty list, and the vendor's test exercises filtering
  across core, hosted, extension, dynamic and MCP tool sources. That
  test was inspected, not executed. The policy is supplied through a
  Rust startup attachment; this investigation did not establish a
  supported public `codex exec` control for it. The finding argues
  against a claim of general impossibility, but does not qualify the CLI.
  Sources: [policy](https://github.com/openai/codex/blob/d27764b82f7118f674371e6d6e76271d9d606edb/codex-rs/ext/extension-api/src/tool_policy.rs),
  [startup attachment](https://github.com/openai/codex/blob/d27764b82f7118f674371e6d6e76271d9d606edb/codex-rs/core/src/session/session.rs#L984-L995),
  [test](https://github.com/openai/codex/blob/d27764b82f7118f674371e6d6e76271d9d606edb/codex-rs/core/src/tools/spec_plan_tests.rs#L517-L604).

An attempted offline parser check used `codex --strict-config` with
the two feature overrides and `features list`. The CLI rejected the
command combination: `--strict-config` is not supported for
`codex features`. It never validated those overrides. This failed
check is preserved rather than represented as parser acceptance.
No Codex model was pinned and no guest capability set was established.

| Registration surface | Gate evidence and remaining gap |
| --- | --- |
| Shell and local images | Source controls identified; complete effective configuration not validated. |
| File editing and model-selected utilities | Registration conditions identified; no selected-model removal proof. |
| Web, apps, MCP, dynamic tools and extensions | Source includes filtering paths; no complete launcher/configuration proof. |
| Delegation and other generated/utility tools | Partial source inspection only; exhaustive effective inventory not established. |

Codex is **unproven**, not demonstrated incapable of tool-free operation.

## Claude findings and the requested launcher

The installed raw CLI is Claude Code 2.1.292, Darwin arm64. Before the
user specified `claude-frank`, one initialization-only process ran with
`--model claude-opus-5-5`, empty tools/MCP settings, safe/restricted
flags, a fresh `CLAUDE_CONFIG_DIR`, and an OS network-denial profile.
Only a streaming `initialize` control request was sent. No user prompt
or model request was sent. After 20 seconds the process was terminated;
its exit status was 143, not a successful completed model run.

The response reported commands, agents, model choices, session state
and UI capabilities. It did **not** include the effective tool inventory
needed by this gate. Available command/agent names do not themselves
prove that model-callable tools were exposed. The account response had
`tokenSource: none`; no credential values were supplied by the probe.
The original home path remained in the process environment, so this
was not evidence of login or filesystem isolation. The accompanying
network negative returned a DNS-resolution error; it was not a complete
egress-control qualification.

The user's subsequent instruction selects `claude-frank` for future
Claude runs. Inspection of `.zshrc` showed that it is a function using
`_claude_as`: it selects the personal `~/.claude-frank` configuration,
checks the expected account, and may log out or start interactive login
when the account differs. It was not executed after the gate expired.
The raw-CLI observation does not qualify this wrapper. Future authorized
live work must use the selected account while separately proving the
worker's authentication boundary; copying the personal profile into a
worker would not establish isolation.

Claude is also **unproven**. M1's historical empty startup list cannot
substitute for the required offline evidence on the chosen launcher.

## Evidence and preserved state

The local forge checkout contains a separate portable index at
`evals/canaries/results/diagnostic-2026-10-08-index.json`: twenty hashed
artifacts covering vendor metadata/source, release/schema digests,
parser output, and the Claude command/request/event stream. Raw files
remain ignored under `evals/canaries/results/private/diagnostic-2026-10-08/`.
The exploratory SDK source snapshot was fetched from a moving branch;
it is retained as a hashed artifact, not used as version-matched proof
of the Claude CLI's behavior.

No new grader was run: the diagnostic stopped before the live grading
phase. Its index records this explicitly with a null grader hash.
The original M1 evidence is separate. These records support the narrow
observations above, not production support or a completed isolation test.

The Codex knowledge-base pages now cite the published configuration
schema and the version-specific local-image registration control.
No knowledge-base migration or sibling-repository publication occurred.

## Decision required before more implementation

The blocker is missing proof of a complete tool-free source-support
launcher in both harnesses. A container cannot resolve this capability
requirement by itself. The approved diagnostic provides these choices:

1. **Keep the CLI/tool-free contracts and mark these candidates
   unavailable.** A new investigation needs a specific new lead and a
   new bounded handoff. Codex's internal allowlist is a concrete lead,
   but exposing it may require a custom host/build; that has not been
   assessed or approved as distribution work. Claude still needs a
   qualifying observation path for the selected launcher.
2. **Amend the design to investigate a dedicated tool-free API adapter
   for source support.** This could avoid the CLI's tool-registration
   surface, but adds authentication, billing and distribution decisions
   and still needs verification. It would not solve the untested
   research/reviewer boundaries automatically.
3. **Accept a Codex parity gap.** Without an approved independent support
   checker, Codex research findings cannot advance into acceptance or
   builds. This option also leaves Claude's current gate unproven; it
   does not produce one certified end-to-end launcher.

None has been selected. T3 remains stopped under the approved diagnostic's
decision gate, not because reviewer agreement requires another approval.
