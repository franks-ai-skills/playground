# Moving forward with both harnesses

Status: **last diagnostic round finished; revised acceptance policy for
the user to choose**. The user approved option A from the earlier version
of this brief, and asked to move to acceptance choices if it did not close
parity. The [catalog spike](2026-10-09-harness-forge-catalog-spike-results.md)
accepted a candidate configuration but did not prove complete tool absence.
No further Codex isolation investigation is proposed by default.

The goal is still a useful pipeline in both Claude Code and Codex, using
subscriptions only. Direct model APIs, extra API keys/credits and paid
fallbacks remain excluded. Native implementation was already selected.
The following options change the original worker or parity contract;
none is silently treated as satisfying the approved design.

## Choose the first release's acceptance policy

| Option | Claude Code and Codex experience | What changes | Main cost |
| --- | --- | --- | --- |
| **1. Human-gated first release (recommended)** | Either CLI runs intake, selection, contract confirmation, build and deterministic checks. The user supplies and checks research evidence and completes the independent review. | Defer autonomous research, source-support and review workers in both harnesses. Human evidence replaces those worker verdicts under an explicit revised contract. | More user work; reduced automation. No new isolation investigation is needed to start the revised core. |
| **2. Shared Claude workers** | Either CLI runs the main workflow; both delegate restricted roles to the same Claude CLI backend. | Parity means equal front-end features, not a complete standalone implementation in each harness. | Requires Claude access alongside Codex, couples limits/availability, and still requires Claude worker qualification before those flows can run. |
| **3. Automated workers with weaker isolation** | Each CLI runs its own separate workers with the controls actually available. | Replace proven tool absence and enforced role isolation with declared restrictions, separate contexts, observed behavior and human acceptance of the remaining exposure. | Retains automation but trusts more of the harness. Unrelated file/context access and tool use cannot be claimed prevented. |

I recommend option 1 for the first release. It lets both front ends make
progress without calling unproved worker restrictions verified or requiring
another diagnostic before implementation. Automated workers can return
later as a separately qualified capability. This is a scope reduction,
not completion of the original automated thin slice.

## What the recommended option would accept

Both research passes still produce explicit artifacts: survey evidence
before selection and detailed evidence before requirement acceptance.
For this release, the user supplies or manually checks those artifacts,
including the source, quotation, context and whether each claim follows.
Record that human source-support decision separately from the later
decision to accept a requirement; accepting an idea is not source proof.

Builds still consume accepted requirements only. Scripts still check
schemas, references, applicability and recorded inputs. A human completes
judged-rule review against the frozen files and pinned KB, with the same
part IDs, hashes and re-review invalidation rules. Missing human evidence
blocks the affected step. The main building agent cannot label its own
unreviewed judgment as an independent reviewer result.

The report identifies who or what supplied each check, says `none run`
where runtime tests were absent, and does not claim certified worker
isolation. The revised design must define whether and when human review
satisfies a required check before any overall `verified` result is allowed.
The current result strings and precedence stay unchanged unless the user
explicitly approves a separate change. Worker certification is deferred;
runtime tests of generated skills remain a separate release requirement.

No autonomous restricted worker is launched in this first release. This
avoids relying on a human approval to make an unisolated worker safe.
Ordinary use of either coding assistant still has that session's normal
permissions; this proposal adds no claim of containment for the parent.

## Conditions on the alternatives

For option 2, use subscription-authenticated `claude-frank` as the default
backend. The completed `claude-tp` exception is not renewed. Claude's
empty host startup inventory does not establish context, guest, login,
research or review isolation. This option therefore retains that future
qualification work, and a missing or rate-limited backend blocks worker
steps; no paid or permissive fallback is automatic.

For option 3, the accepted limitation must cover all three worker roles,
not only source support. Restrict work to a stated trusted-use scope,
record available tools and isolation evidence, require approval of findings
before builds, and keep policy compliance distinct from proven containment.
Passing benign canaries cannot establish prevention of a hostile worker.
This option needs revised acceptance criteria and basic live functional
checks even though it stops pursuing the original isolation guarantee.

## What follows the choice

Update the parent design, thin-slice scope and implementation plan around
the selected policy, with explicit manual/automatic steps and release
criteria. The user's choice approves that direction; no changed policy
is applied before the choice. T3 remains stopped while this decision is
pending. There is no need to re-decide subscription-only use or native
execution.

Packaging follows the revised feasibility and runtime needs. If a later
automated option requires a container/VM, decide its ownership before
making it a public prerequisite. Exact generated-output license wording
still needs approval before publication, once drafted. Those decisions
can wait; the immediate choice is **1, 2 or 3** above.
