# Codex model-catalog spike

Status: **configuration accepted; complete tool absence unproven**.
Parity is not closed. The user authorized one more round of option A,
then requested choices for proceeding with both harnesses if it failed
to close the gap. That round is finished; no further isolation experiment
is proposed as the default next step.

## Scope and accounting

The approved limit was 20 active minutes, offline source/schema and
strict configuration checks, zero model calls. Investigation ran from
04:10:32 to 04:16:19 UTC on 2026-10-09: 5 minutes 47 seconds, without an
interruption. Evidence packaging and this report followed that stop.

Nine offline CLI processes were launched across three recorded sets.
Their only protocol request was `initialize`; none submitted a thread,
prompt or model turn. No Claude launcher, custom binary, container,
model API, API key or account change was used. The previous diagnostic
remains at two charged prompt-bearing invocations and 28 unused slots;
this separately authorized round does not replenish its exhausted
correction allowance.

Each process used the existing OS socket-denial profile, an empty
temporary working directory, closed inherited file descriptors and a
small environment allowlist. HOME retained its real value; this was not
an isolated login or configuration profile. No claim of system-resolver
DNS containment follows from the socket profile.

## What was tested

The installed Darwin arm64 Codex 0.160.1 binary still has SHA-256
`09fa44fdc37a5fc70dc1ace31235f90468a2e193d0e85f7552eab068ea2582be`,
matching the earlier release check. The source remains commit
`d27764b82f7118f674371e6d6e76271d9d606edb`.

The candidate retained the `gpt-6-sol` model identifier and changed its
local catalog metadata: disabled shell, null patch-tool type, empty
experimental-tool list, no search-tool support, direct tool mode and no
model-selected multi-agent version. It combined this with recognized
feature controls, disabled web search, agents, plan and user-input tools,
and enabled skipping host skill discovery. This changes local metadata;
it does not establish provider compatibility or a usable model response.

| Final check | Observation |
| --- | --- |
| Original model catalog with the same configuration overrides | Initialization response, exit 0 |
| Modified model catalog with those overrides | Initialization response, exit 0 |
| Invalid empty catalog with those overrides | Rejected as requiring at least one model, exit 1 |

These controls establish that the installed parser loads the catalog and
accepts the candidate. The original-catalog control is not a permissive
runtime tool test. Initialization still exposes no effective tool list.

Two runner corrections are preserved rather than discarded. The first
set incorrectly assigned a boolean to `features.tool_registry`, which
is a configuration table; all three invocations were rejected. The second
set closed stdin immediately and the candidate exited without an init
event. The final set kept stdin open until response/error/EOF, then closed
it. All nine command lines, streams, results and launcher versions remain
in the new evidence set. These are corrections within this new handoff,
not retroactive use of the old diagnostic's correction allowance.

## Why this does not close parity

The matching source supports a narrower, useful inference: the modified
fields remove the registration conditions for patch, model-advertised
async input, clock and model-selected code mode. See the pinned
[`spec_plan.rs`](https://github.com/openai/codex/blob/d27764b82f7118f674371e6d6e76271d9d606edb/codex-rs/core/src/tools/spec_plan.rs)
and [`tools/mod.rs`](https://github.com/openai/codex/blob/d27764b82f7118f674371e6d6e76271d9d606edb/codex-rs/core/src/tools/mod.rs).
This is conditional source reasoning, not a measured empty runtime registry.

The router also adds MCP, dynamic and extension tools. The app server
installs multiple extensions, including skills. In the inspected skills
path, a selected executor root can produce `skills.list` and `skills.read`
without testing the model's experimental-tool list. Disabling host skill
discovery does not by itself prove those roots or tools absent. See
[`app-server/src/extensions.rs`](https://github.com/openai/codex/blob/d27764b82f7118f674371e6d6e76271d9d606edb/codex-rs/app-server/src/extensions.rs)
and [`ext/skills/src/tools/mod.rs`](https://github.com/openai/codex/blob/d27764b82f7118f674371e6d6e76271d9d606edb/codex-rs/ext/skills/src/tools/mod.rs).
No claim is made that these tools were observed in the candidate.

The local source checkout is partial. An attempted read of the
model-provider source with Git lazy fetching disabled found the blob
unavailable; it was not fetched during this offline round. Initialization
also does not exercise the actual `codex exec` turn, extension state,
managed policy, authentication boundary or role inputs. Consequently the
complete no-tool guarantee remains unproven; this is not proof that it
cannot be achieved.

## Evidence and next action

The local Forge index
`evals/canaries/results/catalog-spike-2026-10-09-index.json` records 76
hashed artifacts, including all attempts, catalogs, runner versions and
numbered source excerpts. All 76 hashes and the 19 prior offline-init
hashes were checked. Earlier evidence and the M1 grader are unchanged.

The [decision brief](2026-10-09-harness-forge-decisions.md) now presents
ways to move forward with both harnesses. At this experiment's stop,
no relaxation had been selected and T3 awaited a policy decision.

**Subsequent decision, 2026-10-09:** the user selected option 3, automated
workers with weaker isolation, and required README disclosure. The amended
design adopts `best-effort-v1` and releases the isolation gate before T3.
This changes acceptance policy, not the experiment's unproven result or
any recorded evidence. Functional worker support still needs live checks.
