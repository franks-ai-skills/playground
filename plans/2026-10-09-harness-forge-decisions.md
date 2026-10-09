# Accepted worker policy for both harnesses

Status: **option 3 selected by the user on 2026-10-09**, with the gap
documented in the relevant READMEs. The [last catalog spike](2026-10-09-harness-forge-catalog-spike-results.md)
accepted a configuration but did not prove complete tool absence. The
user chose to proceed with automated workers under weaker isolation.
No additional isolation investigation is required before T3.

## Decision

Use `best-effort-v1`: Claude Code and Codex each run their own research,
source-support and review workers, using independent CLI processes,
explicit role inputs and available restrictions. Both retain the same
functional workflow. A shared Claude backend and replacing workers with
manual review were not selected.
Native subagents are excluded from this release's worker adapters because
the tested launch paths had actual canary leaks or writes. Process probes
are the better starting evidence, not proof of production containment.
Require the parent's baseline: initially empty temporary working directory,
staged role inputs, small environment allowlist, no resume/fork, closed
extra file descriptors, suppressed optional discovery, disabled apps and
no configured MCP servers. Known inability to apply a required control
blocks launch; unproved runtime isolation remains disclosed.

Research is instructed to use the web for the supplied brief; source
support to judge only the supplied claim/quote/context without tools;
review to use frozen supplied files read-only, without network access.
Configure these limits where supported and report residual capabilities.
Complete tool absence and context/file/network isolation are not
guaranteed. Use trusted projects and operator-approved inputs; this is
not a boundary for secrets or hostile workloads. Human acceptance does
not undo an earlier out-of-scope action.
Research still processes untrusted pages. Forge's README recommends an
operator-provided disposable environment without project secrets or
unrelated credentials and with restricted egress, labelled `recommended,
not verified`. The harness's subscription login remains necessary and
its isolation unproved; no credential-free guarantee is made.

## What remains mandatory

- Both research passes, exact-quote checks and a distinct source-support
  verdict, followed by explicit user acceptance before building.
- Fresh worker processes without intentionally inherited builder/researcher
  conversations; role-specific inputs, structured outputs and schema checks.
  Automatic context discovery remains a disclosed limitation.
- Deterministic checks, complete judged-rule coverage, hash-bound evidence,
  current-session contract confirmation and the existing result precedence.
- Functional live checks in both harnesses before claiming workflow support.
  Missing capabilities, malformed or missing verdicts, failed source checks
  and observed out-of-scope actions block affected work. Known unproven
  containment alone does not block this accepted mode.
- Recorded policy, controls, observations and unknowns in each run, with
  `isolation_status: not-certified`. An artifact may be `verified` only
  under its confirmed rules/goals; that never certifies worker containment.
  A goal requiring enforced isolation still needs the existing conflict or
  outside-control flow. No general security rule is silently downgraded.
- Subscription-only model access, with no direct model API, extra API keys,
  credits or paid fallback. The owner's Claude default is `claude-frank`;
  the completed `claude-tp` diagnostic exception is not renewed.

The exception covers Forge's three workers. It does not relax the
security of catalog checkers, candidate runtime-test environments or
outside-control boundaries. Do not silently widen permissions or switch
accounts when a worker fails.

## README ownership

Forge's local sibling README, `../harness-forge/README.md` relative to the
playground root, contains the policy and per-harness evidence. The
playground and KB READMEs disclose the gap and label local-only paths;
public cross-repository links follow publication. Per-run
`.harness/reports/<slug>.md` retains the disclosure alongside successful
artifact results. A generic `Worker isolation limitations` section is
not required in generated READMEs: it describes Forge's build process,
not the generated artifact's behavior. Artifact-specific limitations and
intake's existing `Outside controls` section remain required.

## Implementation consequence

The [parent design](../specs/2026-10-06-harness-forge-design.md),
[scope](../specs/2026-10-07-harness-forge-thin-slice.md) and
[plan](2026-10-07-harness-forge-thin-slice.md) now encode this choice.
The M1 isolation-policy stop is resolved. Continue with T3's packaging
assessment and then the planned core; T11 establishes functional worker
support under the revised policy. Earlier evidence and the M1 grader
remain unchanged, including their failed/unproven classifications.

Native execution remains selected. No mandatory container or VM is
introduced. Packaging and exact generated-output license wording remain
later decisions at their planned tasks; publication is not authorized by
this worker-policy decision.
