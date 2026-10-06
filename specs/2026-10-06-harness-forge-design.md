# harness-forge design

Status: approved in brainstorming on 2026-10-06; spec awaiting review.

## Goal

Turn the researched agent-harness knowledge base into tooling that
takes any idea for an agent setup ("create a skill for code reviews"),
asks the questions needed to choose the right harness mechanism for
each part of it, recommends a mechanism with pros and cons, lets the
user decide, then builds the chosen mechanism to the research and
verifies the result against the research and the intake.

Users: mainly the author, but everything is public in the
`franks-ai-skills` GitHub organization and must work for anyone who
installs it, without the author's personal plugins or settings.

Success criteria:

- The same intake answers always produce the same recommendation.
- Every recommendation, finding and verdict cites a rule id and the
  knowledge-base page behind it.
- Verification is deterministic wherever a script can decide; a model
  judges only what no script can.
- The tooling runs in Claude Code and Codex as equals. OpenCode is
  best-effort.

## Decisions

| Decision | Chosen | Rejected, and why |
| --- | --- | --- |
| Structure | A pipeline of focused skills plus a reviewer subagent | One large skill: body too long for the research's skill-size guidance, the builder would review its own work, and one description would have to trigger for too many tasks. A Claude Code workflow script: Codex has no equivalent, which breaks harness parity |
| Harnesses | Claude Code and Codex equally | Claude Code first: gives up the parity the knowledge base itself keeps |
| Knowledge-base home | Its own repo; the plugin bundles a pinned snapshot | Same repo as the tooling: couples research and tooling releases. Fetching pages at run time: non-deterministic, needs network, and brings outside content into context, which the security guide warns against |
| Verification | Scripts first, then a fresh-context reviewer subagent on a fixed rule list | Model-only review: not deterministic |
| Granularity | Deciding questions per part of an idea | One round for the whole idea: fails when parts need different mechanisms |

## Repositories

All in the `franks-ai-skills` organization, all public.

| Repo | Contents |
| --- | --- |
| `agent-harness-kb` | The current `playground/docs/`, plus `rules/<concept>.yaml`, `rules/selection.yaml`, the check scripts' fixtures, and tagged releases with a changelog |
| `harness-forge` | The plugin: skills, the reviewer subagent, check scripts, a pinned knowledge-base snapshot, and `.claude-plugin/marketplace.json`, which Claude Code and Codex both read |
| `playground` | Scratch and test area; runs the reference ideas end to end |

## Flow

```
idea → harness-intake ──► .harness/decisions/<date>-<slug>.md
                              │ user decides
                              ▼
                       build-<concept>, once per part
                              │
                              ▼
                       harness-verify
                         1. scripts: rules with check: script, plus links between parts
                         2. reviewer subagent, fresh context: judged rules and goal fit
                         3. report: .harness/reports/<slug>.md
```

`.harness/` lives in the user's repository and is committed, so the
reasons for each choice stay on record.

## Rules

Every practice, anti-pattern, wrong-mechanism case, portability trap
and security requirement in the knowledge base becomes one rule.
Extraction sweeps the "When not", Practices, Security, Portability,
"Dropped from the generalization" and checklist sections of every
page, plus the security guide, not only the checklists.

```yaml
- id: skills.description.what-not-when
  concept: skills
  kind: must-not          # must | must-not | should | should-not
  severity: error         # error fails verification; warning reports only
  check: script           # script | judged
  script: checks/skills/description.py
  statement: Description summarizes the workflow instead of when to use it
  evidence: Practitioner  # the label used on the best-practices page
  sources:
    - docs/guide/skills.md#practices
    - https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md
  contested: false
```

- Rule ids are stable. Reports, decision records and recommendations
  cite them.
- `severity` follows the evidence. Vendor documentation and security
  findings may be `error`. A rule based on practitioner opinion alone
  is at most `warning` unless the author raises it.
- `contested: true` marks a point the sources disagree on, such as
  emphatic ALWAYS/NEVER wording. A contested rule only warns, and the
  report shows each position with its source.
- Extraction also exposes checklist items too vague to check. Those
  are reworded on the knowledge-base page, with a source, or left as
  judged rules.

## harness-intake

1. **Goal.** What the idea should achieve, for whom, and how the user
   will know it works. These become the success criteria.
2. **The user's picture.** How the user imagines it working, recorded
   verbatim.
3. **Split into parts.** Each part has one job and a letter id: A, B,
   C. The user confirms or corrects the split by letter:
   - "Combine A and C": the result keeps A; C is retired and never
     reused in this idea.
   - "Split B": the results are B1 and B2.
   - A new part takes the next unused letter.
4. **Whole-idea questions, asked once.** Target harnesses; reach (this
   repo, all of the user's repos, public).
5. **Per-part questions, asked only when the part's description does
   not already answer them.**
   - Must it hold every time, or may the agent occasionally skip it?
   - Who starts it: the user, the model, or an event?
   - Does it need its own context, other tools or another model?
   - Does it reach an external system, and does a CLI exist for it?
6. **Recommendation.** A mechanism per part with alternatives, pros
   and cons, each citing rule ids and pages, plus how the parts
   connect, for example "B starts A; C enforces A's result".
7. **The user decides**, and may override. An override and its reason
   are recorded.

One question per message, multiple choice where possible. The intake
stops asking about a part once all remaining answers lead to the same
mechanism. A part that fits no mechanism, or parts that turn out to
be the same, trigger a proposal to re-split.

`rules/selection.yaml` holds the questions and what each answer
implies, so the recommendation is computed from data. The model only
phrases questions and explains the result.

### Decision record

```yaml
---
idea: "create a skill for code reviews"
goals: [...]
targets: [claude-code, codex]
reach: public
kb_version: v1.2.0
status: decided           # decided → built → verified
parts:
  - id: A
    slug: review-diff
    goal: Review the diff with fresh eyes
    answers: {every_time: no, trigger: model, own_context: yes}
    recommended: subagent
    chosen: subagent
    override_reason: null
    alternatives:
      - {concept: skill, pros: [...], cons: [...], rules: [...]}
    connects_to: []
  - id: B
    slug: start-review
    goal: Start a review when asked
    recommended: commands
    chosen: commands
    connects_to: [{to: A, how: starts}]
  - id: C
    slug: merge-gate
    goal: Never merge without a review
    recommended: hook
    chosen: hook
    connects_to: [{to: A, how: enforces}]
---
The user's own description, and a summary of the trade-offs.
```

## Builders

One skill per mechanism: `build-skill`, `build-hook`,
`build-subagent`, `build-instructions`, `build-permissions`,
`build-mcp`, `build-plugin`, `build-automation`. Commands are
user-invoked skills, so `build-skill` builds them too. Each one:

- reads its parts from the decision record;
- starts from the knowledge base's defaults and templates for the
  chosen mechanism and each target harness;
- writes files in the portable form when the targets include both
  harnesses, for example skills in `.agents/skills/` with a
  `.claude/skills/` symlink;
- sets the part's status to `built`; it never sets `verified`.

## harness-verify

1. **Deterministic checks.** For each part, run every `check: script`
   rule for its mechanism, plus the vendors' validators where they
   exist (`claude plugin validate`, hook JSON schemas, size limits).
   Then check the links between parts: a named subagent, skill or hook
   event exists and its name matches. No model is involved.
2. **Judged checks.** A reviewer subagent starts with a fresh context
   and receives only the built files, the decision record and the
   `judged` rules for the chosen mechanisms, not the conversation. It
   returns one structured verdict per rule id: pass, fail or not
   applicable, with a reason and a citation. It also checks each part
   against its goal. Free-form verdicts are rejected.
3. **Report.** `.harness/reports/<slug>.md`, grouped by part letter,
   then rule id, with severity, sources, contested positions and the
   knowledge-base version.

A part becomes `verified` only when no `error` rule fails. When the
user overrode a recommendation, the wrong-mechanism rules for that
part report as warnings. On request, builders fix only the failing
parts and verify runs again on those parts.

## Testing harness-forge itself

- **Rules:** every script check has good and bad fixtures in
  `agent-harness-kb` that show it fires on the bad case only.
- **Intake:** fixed answer sets run through `rules/selection.yaml`
  must produce the expected recommendation, without a model.
- **End to end:** reference ideas, starting with the code-review
  example, run in Claude Code and Codex in `playground`. Their
  decision records and reports are kept as reference results.
- **Self-check:** harness-forge's own skills and subagent pass
  `harness-verify`.

## Sub-projects

Each gets its own spec, plan and implementation, in this order:

1. **Rules extraction** in `agent-harness-kb`: move `docs/` out of
   `playground`, write `rules/*.yaml` and fixtures.
2. **`harness-verify`**: check scripts and the reviewer subagent;
   first used on the existing `agent-harness` skill.
3. **`harness-intake`**: `rules/selection.yaml`, the questionnaire and
   the decision record.
4. **Builders**: skills, hooks and subagents first; then
   instructions, permissions, MCP, plugins and automation.
5. **Packaging and CI**: the plugin for both harnesses, the snapshot
   sync and releases.

## Out of scope for now

- Builders that target OpenCode.
- A Claude Code workflow add-on for running the stages.
- Porting an existing setup from one harness to another; the
  `agent-harness` skill covers part of this.
