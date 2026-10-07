# harness-forge skills thin slice

Status: implementation scope derived on 2026-10-07 from the
[harness-forge design](2026-10-06-harness-forge-design.md). The parent
design governs conflicts; revised after review on 2026-10-07. The design,
this scope and the [implementation plan](../plans/2026-10-07-harness-forge-thin-slice.md)
await execution review together; this document does not approve changes
to the parent design.

## Deliverable

An installable plugin takes an idea through intake, survey research,
deterministic selection, deep research, requirement acceptance, a
portable skill build and verification in both Claude Code and Codex.
The same confirmed inputs, pinned Harness KB and confirmed overrides
produce the same recommendation. A clean installation needs none of
the author's personal plugins.

This is sub-project 1 of the parent design. Implement its contracts
before extracting detailed rules or building the other mechanisms.

## Proposed decisions beyond the parent design

These choices make the implementation concrete; they are not previously
approved requirements. Review them with the plan before execution.

- Use Python 3.11+ and JSON Schema Draft 2020-12 for the shared core.
  YAML record formats stay as designed. PyYAML/jsonschema and their
  distribution remain provisional until a bounded assessment compares
  platform bundles, a maintained pure-Python validator and one-time setup.
- Use the reproduction-checklist idea below as the first reference case.
- Give selection a closed predicate grammar and canonical JSON hashes.
  Initial parser/checker limits are 1 MiB per document, nesting depth 32,
  five seconds per checker and 64 KiB of checker output; these are
  implementation defaults, not values prescribed by the parent.
- Try native workers and independent harness processes. The latter is
  an implementation alternative to native delegation, requiring the same
  fresh-context and access guarantees. An empty directory is not proof
  of isolation. Test discovery, inherited context/environment and tools,
  then document supported environments and actual launcher choices.
- Define explicit contract confirmation: selected Confirm or unambiguous
  current-session text, relayed with the displayed digest, run and part
  ids. Scripts check consistency but cannot authenticate the human
  origin. Silence, ambiguous text and prior records leave it pending.
- Record `required_for_goal` for outside controls in the confirmed
  contract. Configuration-protection precautions remain listed without
  silently becoming dependencies of an otherwise advisory task's goal.
- Store the plan in root `plans/` and use sibling repository checkouts.
- Make the destination KB authoritative after copying; freeze the retained
  playground research and redirect corrections to KB. Compare the retained
  copy with its recorded migration inventory before deletion. Snapshot
  updates remain explicit and invalidate affected verification evidence.
- Deliver in milestones: minimal bootstrap and worker feasibility,
  offline primary workflow, live primary workflow, remaining flows,
  then distribution. Publish reviewable evidence at each milestone;
  automatic human approval stops are an execution preference, not a
  default. Intermediate milestones do not complete the slice.
- Run a 24-case routing smoke suite at the first live milestone and the
  roughly 480-run routing evaluation at distribution, before baselines.
- Test each live generated reference skill with small activation cases
  in disposable harness profiles, separately from the forge's own routing
  suite. Offline reports say `none run`; unsupported modes carry reasons,
  and the live build requires observed explicit activation in both harnesses.
- Draft the exact generated-output permission and obtain approval of
  its wording before repository/plugin publication. The parent settled
  the license choice; it did not supply that wording.

If a feasibility or distribution choice requires changing the parent's
guarantees, formats or platform commitments, present that concrete change
for a decision before continuing dependent work. Failure of two tested
launch methods does not establish that every possible approach fails.

## Scope

- Establish public `agent-harness-kb` and `harness-forge` repositories.
  Bootstrap locally, prove worker feasibility, then copy the knowledge
  base for rule extraction. Publish and remove the playground copy only
  at distribution, updating documentation pointers and checking the frozen
  source inventory for untransferred edits. Retain this spec and
  its plan in playground.
- Define rule, catalog, selection, decision, research, override and
  report formats. Extract detailed skills rules and the cross-concept
  security rules that apply to this slice. Extract overview-level
  selection rules for every concept and prerequisite rules for outside
  recommendations. Every extracted claim follows `docs/sources.md`.
- Ship `harness-intake`, `harness-research`, `build-skill` and
  `harness-verify`, fresh research and review workers, deterministic
  checkers, fixtures and a pinned KB snapshot.
- Support all five outcomes: `harness-only`, `outside-alongside`,
  `outside-instead`, `reuse` and `nothing-fits`. A non-skill selection
  remains the recommendation and records that its builder is outside
  this slice; it is never silently converted into a skill.
- Research runs both passes, validates quotes and claim support,
  presents requirements for acceptance and handles drift. An existing
  research artifact is reused only when its brief still matches.
- Preserve part identifiers, split/merge history, connections, choice
  overrides, goal conflicts and per-repository rule overrides.
- Intake updates the result README's `Outside controls` section,
  including outcomes that produce no files. Outside controls are
  always `recommended, not verified`; the forge never inspects or
  configures their platform settings.
- Intake and verification each confirm the current full contract in
  the current session. Historical approvals are explanatory data.
  Missing confirmation blocks the part and leaves its goal unassessed.
  The active agent displays and relays the confirmation; there is no
  Python API that reads or authenticates the user's conversation turns.
- Verify applicable script and judged rules, goal fit and links. Bind
  results to file hashes, KB content, overrides, accepted Idea KB,
  answers and checker versions. Preserve the parent design's exact
  harness-result and goal-result precedence.
- Run cheap sample-prompt tests of generated skills in disposable
  environments and report their outcomes separately from rule checks.
- Support `Review` and `Extensive review`, with their part sets and
  judged-rule counts shown before the user chooses.
- Run the reference idea and restriction canaries in both harnesses
  from clean installations. Run the plugin's own skills through its
  verifier.

## Reference idea

"Create a repository skill that turns an approved bug report into a
reproduction checklist. It should identify the environment, numbered
reproduction steps, expected behavior and observed behavior. Invoke it
when asked; it must not run the reproducer or contact external systems."

The reference's confirmed answers make occasional missed activation
acceptable, require no separate context and request no enforcement
guarantee. Research may recommend an existing solution; a recorded
fixture with no compatible reuse candidate exercises the build path.
Do not suppress a real reuse finding to force a live build.

The built skill needs configuration-protection recommendations, as the
parent design requires for every build. Assess dependency on outside
controls against the accepted goal; listing a precaution does not
silently add it to that goal. If the confirmed goal depends on any
outside control, its result stays `depends on outside controls`.

## Exclusions

No other builders, OpenCode builders, platform administration or
platform verification. No automatic snapshot synchronization or release
CI; an initial reproducible snapshot and manual version pin are needed
for this slice. The later code-review reference waits for the hook,
subagent and automation builders.

## Acceptance

The implementation plan maps these requirements to named tests and
live evidence. Stubbed research and reviewer responses prove contracts,
not harness parity. Both real harness runs and their current-session
human confirmations are required before claiming the slice is complete.
All five outcomes and the complete override/drift/conflict/review flows
remain final acceptance requirements even though the first vertical
workflow excludes those conversations. Until implemented, unsupported
inputs block rather than silently bypassing their contracts.

If either harness cannot enforce the research or reviewer restrictions,
that path reports unavailable and blocks the affected stage. A prompt,
working-directory change or agent file does not substitute for a tested
restriction.
