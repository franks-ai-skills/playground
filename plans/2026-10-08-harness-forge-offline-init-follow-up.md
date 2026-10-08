# Offline startup-inventory follow-up

Status: **authorized on 2026-10-08, subject to no extra cost**. The user
requires subscription usage only: no API keys/tokens, API credits or paid
fallback. This authorizes the two network-blocked startup probes below
only after the external network-denial controls pass. It adopts the
useful leads from Claude Opus 5.5's review of the
[resumed diagnostic](2026-10-08-harness-forge-worker-diagnostic-results.md).
The existing result remains unproven; T3 remains stopped.

Execution result: the positive control exposed `Read`, and the restricted
candidate exposed `tools: []` in `system/init` under externally verified
network denial. See [the result](2026-10-08-harness-forge-offline-init-results.md).
This resolves the host startup-inventory gap only. Two prompt-bearing
launches are charged; no provider response was obtained. The CLI emitted
internal retry events in both processes, which the result records
separately from process launches.

## Review disposition

- **Agree: inspect Claude's `system/init` event.** M1's grader reads its
  `tools` array. The streaming `initialize` control response inspected
  in the later gate is a different event. Whether an ordinary prompt
  produces `system/init` before network failure is a testable lead.
- **Qualify: blocking a request is not preventing its construction.**
  An M1-style prompt may make the CLI attempt a model request even when
  the OS denies its connection. This changes the approved gate's literal
  “no model request and no outbound traffic” condition to “no provider
  traffic or serviced model request.” It needs a specific execution
  handoff, not retrospective relabeling of attempted calls.
- **Qualify: an empty host inventory does not pass the whole gate.** It
  would resolve the missing startup-inventory observation for that host
  build/model/configuration. Intended guest identity, effective overrides
  and later role/isolation checks still need evidence. An absent or
  malformed `tools` field is not an empty inventory.
- **Correct: scripts can invoke zsh functions.** The prior probe copied
  the actual `_claude_as` and `claude-tp` definitions into a zsh script,
  adding guards against login/logout and network access. Directly setting
  `CLAUDE_CONFIG_DIR` would bypass that wrapper's account check; it is
  unnecessary. Keep `claude-tp` only for this diagnostic's temporary
  exception, with `claude-frank` the later default.
- **Correct: the time figure is an estimate.** The previous charge was
  twenty estimated minutes plus 317 measured resumed seconds. It is not
  a measurement of 25 minutes of uninterrupted investigation.
- **Correct: Codex impossibility is unproved.** An internal empty
  allowlist exists; the investigation has not established a supported
  public `codex exec` control. “Can't be reached” is stronger than the
  evidence permits.

## Codex schema lead: checked during this review

The installed 0.160.1 binary generated its app-server protocol schemas
under OS network denial with:

```sh
codex app-server generate-json-schema --experimental --out <scratch-dir>
```

This is schema generation, not thread creation or a model turn. Including
experimental fields produced 440 JSON files. Inspection of the generated
method declarations and the matching source found no declared method
that returns a thread's complete effective tool inventory.
`mcpServerStatus/list` exposes MCP tools, `app/list` concerns apps,
`model/list` describes models, and `thread/read` returns thread state and
history. None is a demonstrated replacement for the combined registry.
Sources: [method declarations](https://github.com/openai/codex/blob/d27764b82f7118f674371e6d6e76271d9d606edb/codex-rs/app-server-protocol/src/protocol/common.rs),
[MCP response](https://github.com/openai/codex/blob/d27764b82f7118f674371e6d6e76271d9d606edb/codex-rs/app-server-protocol/src/protocol/v2/mcp.rs#L76-L96).

This closes the suggested schema-discovery lead for the checked build,
not all possible implementation or future-version routes. The schema
snapshot and command are retained in a separate local evidence index,
`harness-forge/evals/canaries/results/diagnostic-2026-10-08-review-index.json`.
There is no reason to spend the proposed follow-up repeating this search
or issuing speculative protocol requests.

## Concrete Claude-only experiment

Authorize at most **30 additional active minutes** for this specific lead,
within the original four-hour active-work ceiling. External rate-limit
or user waits are recorded separately. The experiment stops after at
most two prompt-bearing process launches, with no retries or account/model
fallback. The intended number of requests reaching a provider is zero.

1. Recheck the exact binary hash and pin `claude-opus-5-5`. Invoke the
   guarded `claude-tp` zsh wrapper; do not source unrelated shell startup
   commands or alter login state. Authentication failure stops the check.
2. Before a prompt, run deterministic connection-denial controls under
   the same OS profile and identity. Check direct IPv4/IPv6 connections
   as well as name-based access; require policy-denial evidence rather
   than relying on a DNS failure. Keep the deny-all network boundary
   active for each CLI process and its descendants. If this cannot be
   demonstrated, do not launch a prompt.
3. In an empty temporary working directory, launch a positive inventory
   control with only `Read` selected, then a source-support candidate
   with `--tools ""`. Keep the existing restricted/safe flags, empty
   MCP configuration and disabled settings/hook discovery. Both use
   `-p --output-format stream-json --verbose` and a harmless synthetic
   prompt through stdin. No real repository content or secrets belong
   in the prompt. Account/profile access remains a host-side trust
   assumption, not a certified worker boundary.
4. Cap each launch at 30 seconds and 2 MiB captured stdout/stderr. Capture
   the whole event stream and termination status. The control must expose
   `Read` in a valid `system/init.tools` list; the restricted candidate
   must expose an explicitly empty list. Missing init, invalid control,
   contradictory later tool events, or any evidence of successful model
   service leaves the experiment unproven/failed as appropriate.
5. Record prompt-bearing attempts, blocked connections and any model
   usage fields separately. Do not claim “no request attempted” because
   the CLI failed, or claim startup ordering beyond the recorded events.
   A network error is expected here and is not a successful completed
   worker run. Do not reuse M1's full-run success grader as an init-only
   acceptance rule.

Conservatively charge these two launches against the original
thirty-invocation ceiling even though no model request may reach a
provider. If both run, at most 28 subsequent launches remain: six live
controls, up to four live diagnostic attempts, and eighteen qualifying
runs. This is an explicit proposed exception to the earlier phase order;
neither offline startup can count as a live control or qualifying run.
Conservatively charge the candidate's change to prompt-bearing startup
as the second and final allowed pre-live configuration correction.
The permissive inventory control is a test fixture, not another candidate
revision. Any later necessary candidate correction requires a new handoff;
the earlier allowance is not reset.

If the candidate shows `tools: []`, record **host startup inventory
observed**, not full gate eligibility or production support. Codex's
complete tool-removal proof and intended-guest checks remain open.
If no valid inventory appears, stop this lead without extending it into
an API adapter, custom CLI build or container setup. Preserve the old
indexes and append a new evidence index and result.

## API option and billing

User decision on 2026-10-08: **subscription-only**. Direct API usage,
API tokens/keys and API credits are excluded, even if credits could
cover the cost. The historical option below is not an approved path.
No account linking, credit claiming or billing changes are authorized.

A tool-free source-support API adapter was discussed before the user's
subscription-only decision and is now excluded. Its role takes
claim/quote/context data and does not inherently need local harness
tools. It would still introduce API authentication and distribution
requirements and would not resolve the research/reviewer boundaries.

OpenAI documents API billing separately from ChatGPT subscriptions
([billing guidance](https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform)).
Claude also distinguishes API usage from the plan's Claude Code usage
limits. However, its current documentation offers separately claimed
monthly API credits to eligible Max and Team plans; those credits can
cover API usage without drawing on Claude Code's plan limits
([API-credit guidance](https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-and-team-plans)).
Account eligibility, claimed credits and remaining balances were not
checked. Do not promise either additional out-of-pocket cost or free API
usage for these accounts. A CLI/subscription-only requirement still
requires an explicit design decision before adding a direct API adapter.

Execute only the authorized, network-blocked Claude startup experiment.
The Codex schema lead has already been checked. No core design option
is selected by this document, and the API alternative is excluded by
the user's subscription-only constraint.
