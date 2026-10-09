# Decisions after the offline-init review

Status: **options for the user; none selected**. This brief does not
amend the approved design or authorize another experiment. It accompanies
the [corrected result](2026-10-08-harness-forge-offline-init-results.md).

## What is settled

The intended outcome remains a skill pipeline with evidence-backed worker
restrictions and equal Claude Code/Codex support. The user approved the
design, scope and plan, selected native execution and a stop after M1,
and requires subscription-only use. Direct model APIs, extra API keys or
credits, and paid fallbacks are excluded.

Claude's tested `claude-tp` profile advertised an empty tool list. That
is a host startup observation, not a completed tool-free worker: context,
automatic discovery, external DNS, authentication isolation and the guest
environment remain unqualified. It does not transfer to the default
`claude-frank` profile. The temporary Team-account exception is spent.
Codex has no established configuration meeting the full tool-free rule;
the evidence does not prove that every possible configuration fails.

Both configuration corrections are spent. Two prompt-bearing launches
were charged, leaving 28 of 30 invocation slots. Those slots do not
authorize a new candidate revision. T3 remains stopped.

## Decide now: the next direction

The policy choice is whether to keep parity. The execution choice is
whether to spend any more effort investigating it. These are distinct:

| Option | What it preserves or changes | Consequence |
| --- | --- | --- |
| **A. Keep parity; approve one targeted Codex spike (recommended)** | Preserves the design and subscription-only constraint. | At most 20 active minutes, zero model calls, for the specific lead below. No promise of a working launcher. |
| **B. Keep parity; park the current launcher** | Preserves all requirements; marks the launcher unavailable. | No further diagnostic work now. T3 stays stopped until a concrete new lead and handoff. |
| **C. Accept a Codex parity gap** | Requires a design/scope/plan amendment defining the unsupported workflow. | Codex research findings without independent source support cannot proceed to acceptance or builds. Claude still needs qualification; this choice does not certify it or automatically release T3. |

I recommend A because the gap would disable a central workflow, while
there is a specific configuration lead that has not been qualified.
If avoiding further investigation matters more, B preserves the agreed
product requirements without spending more diagnostic effort.

### Proposed spike for option A

Question: can the public `model_catalog_json` configuration, combined
with feature controls, remove the model-driven tools that remain in the
pinned Codex build? Inspect the existing matching source/schema and test
strict configuration acceptance offline, capped at 20 active minutes and
zero model calls; no custom binary, container, account changes or API
access. Report which registration paths are eliminated or still
unproven, then stop; parser acceptance alone is not tool-absence proof,
and no live qualification is included or automatically authorized.

The concrete lead is the pinned source at commit
`d27764b82f7118f674371e6d6e76271d9d606edb`:
`codex-rs/core/src/config/mod.rs` loads `model_catalog_json`, while
`codex-rs/core/src/tools/spec_plan.rs` registers tools from
`apply_patch_tool_type` and `experimental_supported_tools`. The earlier
[diagnostic](2026-10-08-harness-forge-worker-diagnostic-results.md)
records this source's build correspondence. This is a hypothesis about
configuration, not an established public tool allowlist or a support
declaration. No new configuration trial was run during this review.

## Decisions that come later

- **Claude qualification scope and account:** a bounded proposal must
  cover the default `claude-frank` profile, advertised skills/plugins and
  automatic discovery, resolver/egress limits, guest and authentication
  isolation, and all three worker roles. Live work must use subscriptions
  and an explicit budget. The old `claude-tp` observation is not enough.
- **External runtime ownership:** if isolation needs a container or VM,
  decide whether users provide it or Forge provisions it before making
  it a public requirement. That result informs T3's packaging choice.
- **Distribution and publication:** select packaging after feasibility
  is settled, and approve the exact generated-output license exception
  when its wording is available, before publication.

These later decisions need concrete proposals and evidence. They do not
need to be answered together with the next-direction choice, and the
already approved design/execution decisions need no blanket reapproval.
