# Harness Forge M1 checkpoint

The user approved the design, scope and plan on 2026-10-07, chose native
execution and requested a stop after M1. The bootstrap exists and the
worker feasibility spike has reached that checkpoint. Do not begin T3.
The thin slice is unfinished; harness parity and isolation requirements
remain unchanged.

## Work and evidence

Local sibling repositories `agent-harness-kb/` and `harness-forge/` have
separate Git histories and no remotes. Both contain byte-for-byte copies
of playground's AGPL license. No generated-output permission has been
drafted or approved and neither destination has been published. No
knowledge-base content has moved.

Local commits: KB bootstrap `1a0204f`; Forge bootstrap `e685ad9` and
worker-spike evidence `ef7c73d`.

Forge contains a dependency-free bootstrap and disposable worker-probe
instrumentation. Its 21 offline tests cover isolated bootstrap import,
evidence completeness, tool/result correlation, permission denials,
startup leaks, unexpected writes and preserving violations after process
failure. New grading regressions were observed failing before fixes;
the complete suite then passed. A fresh GPT-6 Astra reviewer checked the
M1 changes and evidence. Its four findings were corrected in one fix
pass; no minor finding remains deferred.

The spike retained 23 attempts on macOS 27.0.1 arm64, Python 3.14.7,
codex-cli 0.160.1 and Claude Code 2.1.292. All evidence hashes were
checked after the final regrade. Three Claude separate-process role
probes have observed inventories and behavior, six attempts are
unproven, eleven failed and three configuration attempts were rejected
before model execution. Two failures are intentionally unrestricted
positive controls. `Observed` is a limited probe result, not production
support.

Claude process research had a web-only inventory and matching fetch
result; source support had an empty inventory; review had read-only
tools and actual permission errors for both prohibited file paths.
Native child inventories were not exposed, and native Claude review
returned unrelated/outside file canaries.

Codex initially made real connector web calls in no-network roles.
Explicit app disabling removed those calls in repeats. Research then
recorded a native web-result event, but no authoritative tool inventory
or enforced filesystem-denial evidence was obtained. Native Codex
launches returned startup canaries and sometimes wrote the fixture.
The streams did not confirm that a configured child role performed
every action; the evidence rejects the tested launch path rather than
establishing a child-level cause or general Codex impossibility.

The detailed report and portable hash index are local at
`../harness-forge/evals/canaries/results/worker-boundaries.md` and
`../harness-forge/evals/canaries/results/evidence-index.json`.
Raw requests, events and role configuration remain ignored local files;
no real repository data or credential values were requested by probes.

## Decisions retained

- Preserve the copied license bytes; its inherited final blank line is
  excluded from whitespace checks after byte comparison.
- Keep disposable fixture metadata JSON-compatible YAML and use only
  the Python standard library. Production YAML/schema/distribution
  decisions remain T3/T4 work.
- Do not equate voluntary refusal or absence of leaks with enforcement.
  Full role payloads, supplied-data reads, managed/user discovery,
  authentication isolation and hostile-worker containment are not
  certified by this benign spike.
- Do not declare production support, other-version/platform support or
  vendor-wide impossibility. The default Codex model id was not exposed,
  so commands can rerun candidates but cannot promise an identical model.
- Retain the local plan ledger and raw evidence for resumption. T3-T14,
  destination publication and knowledge-base migration remain outside
  this execution handoff.

## Proposed next step

Revised on 2026-10-08 after Claude Opus 5.5's review: prioritize a
disposable external boundary and independent processes in both harnesses.
The [bounded diagnostic proposal](2026-10-08-harness-forge-worker-diagnostic.md)
sets explicit model selection, common role/input/discovery/authentication
criteria, external enforcement evidence and a four-hour/30-invocation
ceiling. Tool absence and read-only capabilities remain separate checks;
a container does not automatically meet them.

Both tested native configurations have failures, including Claude's
review worker. This prioritizes the next candidate without ruling out
all native workers. Authentication material and supplied inputs remain
sensitive inside an external environment. A production container/VM
dependency also needs a design decision about who provides and controls
it, because Forge currently recommends rather than provisions outside
controls. The diagnostic is proposed; the M1 stop remains in effect.
