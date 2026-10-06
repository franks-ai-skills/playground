# harness-forge design

Status: approved in brainstorming on 2026-10-06; revised after a
review and to add idea research on 2026-10-06; spec awaiting review.

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
- Recommendations and builds draw on sourced research about the idea
  itself, not only on harness knowledge.

## Decisions

| Decision | Chosen | Rejected, and why |
| --- | --- | --- |
| Structure | A pipeline of focused skills plus a reviewer subagent | One large skill: body too long for the research's skill-size guidance, the builder would review its own work, and one description would have to trigger for too many tasks. A Claude Code workflow script: Codex has no equivalent, which breaks harness parity |
| Harnesses | Claude Code and Codex equally | Claude Code first: gives up the parity the knowledge base itself keeps |
| Knowledge-base home | Its own repo; the plugin bundles a pinned snapshot | Same repo as the tooling: couples research and tooling releases. Fetching pages at run time: non-deterministic, needs network, and brings outside content into context, which the security guide warns against |
| Verification | Scripts first, then a fresh-context reviewer subagent on a fixed rule list | Model-only review: not deterministic |
| Granularity | Deciding questions per part of an idea | One round for the whole idea: fails when parts need different mechanisms |
| Build order | A thin slice for the skills concept, end to end in both harnesses, before extracting the other concepts | Extracting every rule first: the schema and contracts would only be tested after hundreds of rules depend on them |
| Overrides | Choosing another mechanism only warns; a chosen mechanism that cannot meet a stated goal stays an error | Downgrading every fit failure to a warning: "verified" would hide unmet goals |
| Re-verification | Fixed parts plus every part linked to them | Fixed parts only: a change can break the part that calls it |
| Idea research | A separate `harness-research` skill, run twice by the intake: a short survey before the split, and a deep pass per chosen part before building | Research only before the intake: the goal is not yet clear, so it covers too much or the wrong topic. Research only before building: the recommendation cannot use it, and existing solutions surface too late. A tool the user runs alone: the forge could not rely on its output |
| License | AGPL-3.0 for every repository in the organization, with an additional permission that excludes files harness-forge generates in a user's repository | Plain AGPL-3.0: leaves open whether generated configuration in a user's repository is covered |

## Repositories

All in the `franks-ai-skills` organization, all public, all licensed
AGPL-3.0. `harness-forge` adds the output exception from "Decisions".

| Repo | Contents |
| --- | --- |
| `agent-harness-kb` | The current `playground/docs/`, plus `rules/<concept>.yaml`, `rules/selection.yaml`, the check scripts' fixtures, and tagged releases with a changelog |
| `harness-forge` | The plugin: skills, the reviewer subagent, check scripts, a pinned knowledge-base snapshot, and `.claude-plugin/marketplace.json`, which Claude Code and Codex both read |
| `playground` | Scratch and test area; runs the reference ideas end to end |

## Flow

```
idea → harness-intake
         1. goal + the user's picture
         2. harness-research, survey pass ──► .harness/research/<slug>.md
         3. split into parts, questions, recommendation
         4. user decides ──────────────────► .harness/decisions/<date>-<slug>.md
                              │
                              ▼
       harness-research, deep pass per chosen part ──► .harness/research/<slug>.md
                                                       .harness/research/<slug>.rules.yaml
                              │
                              ▼
       build-<concept>, once per part
                              │
                              ▼
       harness-verify
         1. scripts: knowledge-base and idea rules with check: script, links between parts
         2. reviewer subagent, fresh context: judged rules and goal fit
         3. runtime tests where cheap
         4. report: .harness/reports/<slug>.md
```

`.harness/` lives in the repository that holds the built result and
is committed, so the reasons for each choice stay on record. When the
result is a plugin with its own repository, `.harness/` goes there.

Two kinds of knowledge feed the flow:

| | Mechanism knowledge | Idea knowledge |
| --- | --- | --- |
| Answers | How to build a good skill, hook or subagent | What the idea's domain requires: prior art, approaches, pitfalls |
| Source | `agent-harness-kb`, a pinned snapshot | `harness-research`, live sources, per idea |
| Becomes | Rules every build is verified against | Input to the split and recommendation, and idea rules for verification |

## Rules

Every practice, anti-pattern, wrong-mechanism case, portability trap
and security requirement in the knowledge base becomes one rule.
Extraction sweeps the "When not", Practices, Security, Portability,
"Dropped from the generalization" and checklist sections of every
page, plus the security guide, not only the checklists.

```yaml
- id: skills.description.no-workflow-steps
  concept: skills
  kind: must-not          # must | must-not | should | should-not
  severity: warning       # error fails verification; warning reports only
  check: judged           # script | judged
  statement: The description lists the skill's workflow steps
  applies_to:
    harnesses: [claude-code, codex, opencode]
    versions: {claude-code: ">=2.1.289", codex: ">=0.159.2"}
    when: []              # conditions, e.g. "targets include two harnesses"
  evidence: Practitioner  # the label used on the best-practices page
  sources:
    - docs/guide/skills.md#practices
    - https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md
  contested: false

- id: skills.description.length
  concept: skills
  kind: must
  severity: error
  check: script
  script: checks/skills/description_length.py
  statement: The description is present and within the harness limit
  applies_to: {harnesses: [claude-code, codex, opencode]}
  evidence: Vendor
  sources: [docs/vendors/claude-code/skills.md, docs/vendors/codex/skills.md]
  contested: false
```

- Rule ids are stable. Reports, decision records and recommendations
  cite them.
- `check: script` only for what a script decides without
  interpretation: presence, length, syntax, names, paths, schemas.
  Anything that needs reading prose for meaning is `judged`.
- `applies_to` limits a rule to harnesses, version ranges and
  conditions. A rule outside its scope is reported as not applicable
  with that reason.
- `evidence` and `severity` are separate. A written severity policy in
  `agent-harness-kb` sets each rule's severity; evidence only caps it.
  Vendor advice is not automatically `error`, and a rule based on
  practitioner opinion alone is at most `warning` unless the author
  raises it with a recorded reason.
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
3. **Survey research.** `harness-research` runs its survey pass on
   the goal and picture (see "harness-research"). The user confirms
   which findings to use before the split.
4. **Split into parts.** Each part has one job and a letter id: A, B,
   C. The user confirms or corrects the split by letter:
   - "Combine A and C": the result keeps A; C is retired and never
     reused in this idea.
   - "Split B": the results are B1 and B2.
   - A new part takes the next unused letter.
5. **Whole-idea questions, asked once.** Target harnesses; reach (this
   repo, all of the user's repos, public).
6. **Per-part questions, asked only when the part's description does
   not already answer them.**
   - Must it hold every time, or may the agent occasionally skip it?
   - Who starts it: the user, the model, or an event?
   - Does it need its own context, other tools or another model?
   - Does it reach an external system, and does a CLI exist for it?
7. **Recommendation.** An outcome per part with alternatives, pros
   and cons, each citing rule ids and pages, plus how the parts
   connect, for example "B starts A; C enforces A's result". An
   outcome is one of:
   - a harness mechanism, such as a skill, hook or subagent;
   - a control outside the harness, such as a CI check or repository
     settings. The knowledge base assigns the authoritative merge gate
     to CI because committed agent configuration can be changed by a
     pull request (`docs/overview.md`, `docs/guide/hooks.md`);
   - reuse what exists: the survey found an existing skill, plugin or
     tool that meets the part's goal; the recommendation names it with
     its source, license and maintenance state;
   - nothing fits: the part's goal cannot be met by any researched
     mechanism, and the intake says so instead of forcing a choice.
8. **The user decides**, and may override. An override and its reason
   are recorded.

One question per message, multiple choice where possible. The intake
stops asking about a part once all remaining answers lead to the same
outcome. Parts that turn out to be the same, or a part that mixes two
jobs, trigger a proposal to re-split.

Builders exist only for researched outcomes. An outside control that
the knowledge base has not researched with sources, such as GitHub
branch protection today, is named in the recommendation but not
built.

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
    outcome: outside-harness
    recommended: automation-ci   # a CI job that runs A and must pass
    chosen: automation-ci
    alternatives:
      - {concept: hook, pros: [...], cons: ["agent config can be changed by a pull request"], rules: [...]}
    connects_to: [{to: A, how: enforces}]
---
The user's own description, and a summary of the trade-offs.
```

## harness-research

A skill that researches the user's idea, not the harness. It runs in a
subagent and can also be started on its own; a later intake then
reuses the existing research file.

**Survey pass**, after the goal and the user's picture, kept short
because the user is waiting inside the intake:

- what people already do for this goal, and which approaches exist;
- whether an existing skill, plugin or tool already meets it;
- findings that suggest an extra part or an answer to a deciding
  question.

**Deep pass**, after the user decides, for each chosen part only:

- what the result must contain to meet the part's goal;
- the domain's pitfalls and security concerns;
- requirements that can be checked, written as idea rules.

**Output:**

- `.harness/research/<slug>.md`: findings grouped by pass and part,
  each claim with a fetched source.
- `.harness/research/<slug>.rules.yaml`: idea rules in the same schema
  as the knowledge-base rules, with ids prefixed `idea.<slug>.`.
  `harness-verify` checks them like any other rule.
- The decision record stores the path and date of the research it
  used.

**Source rules.** The rules in the knowledge base's `docs/sources.md`
apply: every source is fetched and says what is cited, claims that
cannot be verified are dropped, primary sources come first, and the
X platform is not a source. The plugin ships these rules in its
snapshot.

**Safety.** Fetched pages are untrusted content.

- The research subagent has web access and read-only tools, and no
  tool that writes outside `.harness/research/`.
- It returns structured findings, each with a source. Fetched text
  reaches builders only through findings the user confirmed, never as
  instructions.
- Research never changes the computed recommendation directly. It can
  suggest answers or parts; the user confirms them, and
  `rules/selection.yaml` computes the recommendation from the
  confirmed answers.

**Knowledge-base drift.** When research finds that a fact in the
pinned knowledge base is outdated, the report lists it as drift for
`agent-harness-kb`. It never changes the pinned rules.

**Harness support.** Both harnesses support web search. Codex defaults
to cached search; live search needs `web_search = "live"` or
`--search` (`docs/vendors/codex/configuration.md`). When only cached
search is available, the research file says so.

## Builders

One skill per mechanism: `build-skill`, `build-hook`,
`build-subagent`, `build-instructions`, `build-configuration`,
`build-permissions`, `build-mcp`, `build-plugin`, `build-automation`. Commands are
user-invoked skills, so `build-skill` builds them too. Each one:

- reads its parts from the decision record and the deep-pass findings
  for those parts;
- puts into the result only the research the result needs at run
  time, for example a skill's `references/` file, with its sources;
  the full research file stays in `.harness/research/`;
- starts from the knowledge base's defaults and templates for the
  chosen mechanism and each target harness;
- writes files in the portable form when the targets include both
  harnesses, for example skills in `.agents/skills/` with a
  `.claude/skills/` symlink;
- sets the part's status to `built`; it never sets `verified`.

## harness-verify

1. **Deterministic checks.** For each part, run every `check: script`
   rule that applies to it, plus the vendors' validators where they
   exist (`claude plugin validate`, hook JSON schemas, size limits).
   Then check the links between parts: a named subagent, skill or hook
   event exists and its name matches. No model is involved.
2. **Judged checks.** A reviewer subagent starts with a fresh context
   and receives only the built files, the decision record and the
   applicable `judged` rules, not the conversation. It returns one
   structured verdict per rule id: pass, fail or not applicable, each
   with a reason and a citation. It also checks each part against its
   goal.
3. **Runtime tests**, where a cheap one exists: the hook blocks a
   sample bad command, the skill triggers on sample prompts. Reported
   separately from the static checks in 1 and 2.
4. **Report.** `.harness/reports/<slug>.md`, grouped by part letter,
   then rule id, with severity, sources, contested positions, the
   knowledge-base version, the version of each tool used, and the
   sha256 of every file checked.

### What "verified" means

A part is `verified` only when all of these hold:

- every applicable rule produced a result; none is missing or errored;
- every "not applicable" verdict has a reason shown in the report;
- no `error` rule failed;
- every recorded file hash still matches. A changed file returns its
  part to `built`.

`verified` means the part passed the static checks and the listed
runtime tests at the recorded versions. It does not mean the part is
free of defects the rules do not cover.

### Overrides

When the user chose a mechanism other than the recommended one:

- rules that only say "a different mechanism was recommended" report
  as warnings;
- rules that say "the chosen mechanism cannot meet a goal the user
  stated" stay errors, until the user changes that goal in the
  decision record.

### Re-verification

On request, builders fix the failing parts. Verification then runs
again on the fixed parts, on every part linked to them through
`connects_to`, and on the link checks.

### Security of the verifier

The files under review may be hostile, so the security guide applies
to harness-forge itself:

- Rules and check scripts come only from the pinned knowledge-base
  snapshot inside the plugin, never from the repository being
  checked.
- Check scripts run with time and output limits and do not execute
  the files they check.
- The reviewer subagent gets read-only tools and no network access.
- Reviewer output is validated against a schema: every applicable rule
  id must appear exactly once, and unknown ids are rejected.
- A fresh context removes the builder's conversation, not prompt
  injection inside the reviewed files. The reviewer's instructions
  treat file contents as data, and a judged verdict can never
  overrule a failed script check.

## Testing harness-forge itself

- **Rules:** every script check has good and bad fixtures in
  `agent-harness-kb` that show it fires on the bad case only.
- **Research:** the subagent's output is validated against its schema,
  and every cited domain is checked against `docs/sources.md`.
- **Intake:** fixed answer sets run through `rules/selection.yaml`
  must produce the expected recommendation, without a model.
- **End to end:** reference ideas run in Claude Code and Codex in
  `playground`. The thin slice uses an idea that ends in a skill; the
  code-review example follows once the hook, subagent and automation
  builders exist. Their
  decision records and reports are kept as reference results.
- **Self-check:** harness-forge's own skills and subagent pass
  `harness-verify`.

## Sub-projects

Each gets its own spec, plan and implementation, in this order.

1. **Thin slice: skills, end to end.** Proves the contracts before
   they spread across every concept:
   - create `agent-harness-kb`, move `docs/` out of `playground`, and
     write the rule schema and the severity policy;
   - the rules for the skills concept, with fixtures;
   - `rules/selection.yaml` for all concepts, but only at the level of
     the overview's "use it when / do not use it when" columns, so the
     intake can still recommend another mechanism than a skill;
   - `harness-intake`, `harness-research` (both passes), `build-skill`
     and `harness-verify`, including idea rules;
   - the plugin packaged for Claude Code and Codex and run in both,
     in a clean environment without the author's personal plugins.
2. **Rules for the remaining concepts**, with fixtures, using the
   schema as corrected by the slice.
3. **Builders**: hooks, subagents and automation first; then
   instructions, configuration, permissions, MCP and plugins.
4. **CI and releases**: the snapshot sync between `agent-harness-kb`
   and `harness-forge`, and tagged releases.

## Out of scope for now

- Builders that target OpenCode.
- A Claude Code workflow add-on for running the stages.
- Porting an existing setup from one harness to another; the
  `agent-harness` skill covers part of this.
