# harness-forge design

Status: approved in brainstorming on 2026-10-06; revised after three
reviews and to add idea research on 2026-10-06; outside controls added
on 2026-10-07; spec awaiting review.

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

- The same normalized intake answers with the same Harness KB version
  always produce the same recommendation. Live research does not
  repeat exactly; only the answers the user confirms from it feed the
  selection.
- Every recommendation, verification finding and verdict about a
  mechanism cites a rule id and the Harness KB page behind it.
- Every idea research finding cites its source with a verbatim quote.
  An accepted requirement also gets an Idea KB rule id.
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
| Outside controls | Recommended with prerequisites and listed in the result's README as "recommended, not verified"; never built, configured or checked on the platform | Building them through platform APIs: the forge would need admin tokens, which the identity research advises against. Checking them with a read-only token: not wanted; the README makes each recommendation visible instead |
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
       proposed requirements ─► user accepts ──► Idea KB revision recorded
                              │   (or: chosen mechanism cannot meet the goal → back to intake)
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

| | Harness KB | Idea KB |
| --- | --- | --- |
| Answers | How to build a good skill, hook or subagent | What the idea's domain requires: prior art, approaches, pitfalls |
| Source | `agent-harness-kb`, a pinned snapshot in the plugin | `harness-research`, live sources, per idea, in `.harness/research/` |
| Owns | Mechanism selection, harness behavior, portability, security rules, and the trusted checkers | Domain evidence, accepted requirements, existing-solution candidates |
| Changes through | Reviewed, versioned releases of `agent-harness-kb` | Research plus revisions the user approved for that idea |

Both feed the forge, and neither updates the other. They share the
rule schema, not authority: only the Harness KB provides executable
checkers.

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
  checker: skills.description-length   # id in checks/catalog.yaml
  params: {max_chars: 1024}
  statement: The description is present and within the harness limit
  applies_to: {harnesses: [claude-code, codex, opencode]}
  evidence: Vendor
  sources: [docs/vendors/claude-code/skills.md, docs/vendors/codex/skills.md]
  contested: false
```

- Rule ids are stable. Reports, decision records and recommendations
  cite them.
- `checks/catalog.yaml` in `agent-harness-kb` lists every executable
  checker by id, with a schema for its parameters. Rules refer to a
  checker by id; idea rules may only use catalog checkers.
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
3. **Whole-idea questions, asked once.** Target harnesses; reach (this
   repo, all of the user's repos, public); where the code is hosted,
   on which plan, and whether the repository is public or private,
   because many outside gates enforce only on some plans or for some
   visibilities (`docs/guide/outside-gates.md`). The survey uses
   targets and reach to look only for compatible existing solutions.
4. **Survey research.** `harness-research` runs its survey pass on
   the goal, picture, targets and reach (see "harness-research"). The
   user confirms which findings to use before the split.
5. **Split into parts.** Each part has one job and a letter id: A, B,
   C. The user confirms or corrects the split by letter:
   - "Combine A and C": the result keeps A; C is retired and never
     reused in this idea.
   - "Split B": the results are B1 and B2.
   - A new part takes the next unused letter.
6. **Per-part questions, asked only when the part's description does
   not already answer them.**
   - Must it hold every time, or may the agent occasionally skip it?
   - Must it still hold if the agent is prompt-injected or its
     configuration is changed by a pull request?
   - Who may turn it off: the agent, any contributor, or only an
     admin?
   - Does the event happen without an agent, such as a merge, deploy,
     publish or credential scope?
   - Is the action irreversible, about money, or does it publish or
     disclose data?
   - Is earlier feedback wanted than an outside gate gives?
   - Who starts it: the user, the model, or an event?
   - Does it need its own context, other tools or another model?
   - Does it reach an external system, and does a CLI exist for it?
7. **Recommendation.** An outcome per part with alternatives, pros
   and cons, each citing rule ids and pages, plus how the parts
   connect, for example "B starts A; C enforces A's result". An
   outcome is one of:
   - **harness only:** a harness mechanism, such as a skill, hook or
     subagent, or OS isolation for local actions no outside system
     sees;
   - **outside control alongside a harness mechanism:** the rule must
     survive a compromised agent and in-loop feedback saves
     iterations, or the rule protects the agent's own configuration;
   - **outside control instead of any harness build:** the event
     happens without an agent, such as a merge or deploy, so a harness
     build adds no enforcement;
   - **reuse what exists:** the survey found an existing skill, plugin
     or tool that meets the part's goal; the recommendation names it
     with its source, license and maintenance state;
   - **nothing fits:** no researched mechanism or control meets the
     part's goal, and the intake says so instead of forcing a choice.
8. **The user decides**, and may override. An override and its reason
   are recorded.

One question per message, multiple choice where possible. The intake
stops asking about a part once all remaining answers lead to the same
outcome. Parts that turn out to be the same, or a part that mixes two
jobs, trigger a proposal to re-split.

### Outside controls

An outside control is any control outside the agent harness: merge
rules, CI checks, scanners, identity and credentials, network and DNS
boundaries, isolation, policy engines, limits, recovery. A *gate* is an
outside control that prevents an action; detection and recovery
controls are outside controls but not gates.
`docs/guide/outside-gates.md` is the Harness KB source for all of
them.

- The forge recommends outside controls and never builds or
  configures them. It holds no token that could change platform
  settings.
- Each recommended control comes with its prerequisites as Harness KB
  rules, from the guide's seven conditions, for example "the agent's
  identity is on no bypass list" and "approvals reset on new pushes".
  A CI job, for example, is a gate only once the repository requires
  it to pass and its workflow definition is protected.
- Every recommendation in which an agent opens pull requests includes
  a merge rule, and every built harness setup includes code owners for
  the agent's own configuration files, as recommended outside
  controls.
- Bypass modes, untrusted repositories, or untrusted input combined
  with secrets and egress always add an isolation recommendation.
- When a control is unavailable on the user's plan or visibility, the
  recommendation says so. If the part's goal requires a guarantee, the
  outcome is "nothing fits" unless the user overrides.
- "Build it anyway": the user may choose a harness mechanism where an
  outside control was recommended. The forge builds it and labels it
  advisory, because the agent or a pull request can change it. A
  stated goal it cannot meet, such as "must hold under prompt
  injection", stays an error (see "Overrides").

**README.** Every recommended outside control, including those for
parts with no harness build, is listed in an "Outside controls"
section of the README that belongs to the result: the result's own
README when it has one, such as a plugin's, otherwise the README of
the repository that holds `.harness/`. Each entry names the control,
the part letter it serves, its prerequisites, and its status
"recommended, not verified". `build-*` skills write the section;
`harness-verify` checks with a script that every outside control in
the decision record appears there. Verification never checks whether
the control is actually configured on the platform.

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
status: decided           # decided → built → verified; blocked on unresolved drift
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
    outcome: outside-alongside     # harness-only | outside-alongside | outside-instead | reuse | nothing-fits
    recommended: automation        # a CI workflow that runs A; built
    chosen: automation
    outside_controls:              # recommended only; listed in the README
      - control: required-review-and-check
        prerequisites: [outside.merge.no-agent-bypass, outside.merge.requester-cannot-approve,
                        outside.ci.required-on-ref, outside.ci.source-pinned, outside.ci.workflow-protected]
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

**Survey pass**, after the goal, the user's picture, targets and
reach, kept short
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
  as the Harness KB rules, with ids prefixed `idea.<slug>.`. An idea
  rule is either `judged` or names a checker from the Harness KB's
  checker catalog by id, with parameters validated against that
  checker's schema. It can never name a script path.
- Each finding stores its source URL, fetch date and a verbatim quote
  that supports the claim.

**Source support check.** Two checks run on every finding before the
user sees it:

1. A script confirms that the quote appears in the fetched text.
2. A fresh-context check, separate from the researcher, judges whether
   the quote and its surrounding text support the claim. A real quote
   can still back a wrong conclusion: "supported only on Linux" does
   not support "supported on every platform".

A finding that fails either check is dropped, as `docs/sources.md`
requires.

**Acceptance.** The deep pass ends with proposed requirements, not a
build. The user accepts, edits or rejects each one. Only accepted
requirements and their idea rules form the Idea KB revision the
builders and `harness-verify` use; the decision record stores that
revision's sha256. When the deep pass shows that a chosen mechanism
cannot meet a part's goal, the forge returns to the intake with a
concrete alternative instead of building.

**Source rules.** The rules in the knowledge base's `docs/sources.md`
apply: every source is fetched and says what is cited, claims that
cannot be verified are dropped, primary sources come first, and the
X platform is not a source. The plugin ships these rules in its
snapshot.

**Safety.** Fetched pages are untrusted content.

- The research subagent receives only an approved research brief: the
  goal, the user's picture, the parts and their accepted answers. It
  gets no access to the repository's other files, because search
  arguments and fetched URLs can carry data out (OpenAI's deep-research
  security guidance, cited in `docs/guide/security.md`).
- It has web access and no tool that writes outside
  `.harness/research/`.
- Restrictions are set up per harness and tested in each. Codex
  subagents inherit the parent's sandbox and live runtime overrides
  even when the agent file says otherwise
  (`docs/vendors/codex/subagents.md`), so an agent file alone does not
  enforce them.
- It returns structured findings, each with a source. Fetched text
  reaches builders only through findings the user confirmed, never as
  instructions.
- Research never changes the computed recommendation directly. It can
  suggest answers or parts; the user confirms them, and
  `rules/selection.yaml` computes the recommendation from the
  confirmed answers.

**Knowledge-base drift.** When research finds that a fact in the
pinned Harness KB is outdated, the report lists it as drift for
`agent-harness-kb`, with its source. It never changes the pinned
rules. When the drift touches a security rule or would break
compatibility, the affected parts stop at `blocked` until the user
chooses one of two paths:

- **Adopt the correction.** This needs a Harness KB release that
  contains the corrected rule, reviewed in `agent-harness-kb`. The
  part stays `blocked` until the plugin pins that release; verification
  then runs against it like any other version. A user who cannot
  publish to `agent-harness-kb` waits for that release.
- **Keep the pinned rule.** The part continues, and every applicable
  check and stated goal must still pass against the pinned version.

The user's choice authorizes the path. It never waives a failed check,
and the forge does not unblock on the research's own say-so, because
fetched content could invent drift to steer a build.

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
- applicability was decided before review: scripts evaluate
  `applies_to` for every rule, and the reviewer receives only rules
  that apply. A rule whose applicability needs judgment carries
  `applicability: judged`; the reviewer may answer "not applicable"
  only for those, with a reason. For an `error` rule, that answer
  leaves the rule unresolved, and an unresolved rule keeps the part
  from `verified` until the user confirms the reason. That
  confirmation settles only whether the rule applies; a rule that
  applies and fails stays failed;
- no `error` rule failed;
- the bound inputs are unchanged: the sha256 of every checked file,
  the Harness KB version, the Idea KB revision, the decision record's
  answers and the checker versions. A change to any of them returns
  the affected parts to `built`, even when the generated files did not
  change.

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

- Mechanism rules and every executable checker come only from the
  pinned Harness KB snapshot inside the plugin. Accepted idea rules
  come from the Idea KB and can only be judged or call a catalog
  checker with validated parameters. Nothing from the repository being
  checked is executed as a check.
- Runtime tests run the candidate's own code, so they run in a
  separate, disposable environment with synthetic credentials and an
  explicit network allowlist.
- Check scripts run with time and output limits and do not execute
  the files they check.
- The reviewer subagent gets read-only tools and no network access,
  set up and tested per harness as for research.
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
  and every cited domain is checked against `docs/sources.md`. Fixture
  cases with stubbed fetches cover: a trusted source whose text does
  not contain the quote; a real quote that does not support its
  claim ("supported only on Linux" cited for "supported on every
  platform"); research reused after the goal
  changed; injected instructions in a fetched page; a requirement the
  user did not accept reaching a builder; an idea rule that names a
  checker outside the catalog or a script path. Each must be rejected.
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
     write the rule schema, the severity policy and the checker
     catalog;
   - the rules for the skills concept, with fixtures;
   - `rules/selection.yaml` for all concepts, but only at the level of
     the overview's "use it when / do not use it when" columns, so the
     intake can still recommend another mechanism than a skill;
   - `harness-intake`, `harness-research` (both passes), `build-skill`
     and `harness-verify`, including idea rules;
   - outside-control recommendations with prerequisite rules, and the
     README section with its check;
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
- Building, configuring or verifying outside controls on a platform.
  The forge recommends them and lists them in the README.
- A Claude Code workflow add-on for running the stages.
- Porting an existing setup from one harness to another; the
  `agent-harness` skill covers part of this.
