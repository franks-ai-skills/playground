# harness-forge design

Status: approved in brainstorming on 2026-10-06; revised after three
reviews and to add idea research on 2026-10-06; outside controls added
user-decided rule overrides, the goal-conflict question and the
re-verification choice on 2026-10-07; contracts for approval, outside
dependencies and routing tightened, and contract confirmation and
result states added on 2026-10-07; design, thin-slice scope and plan
approved by the user on 2026-10-07. Execution starts natively and stops
after M1 for review of worker-isolation feasibility.
On 2026-10-08 the user confirmed subscription-only model access: no
additional API tokens/keys, API credits or paid fallback.
On 2026-10-09, after M1 and its bounded follow-ups, the user selected
automated workers with weaker isolation (option 3), with the gap documented
in the relevant READMEs. The policy below replaces the original requirement
to prove worker containment before continuing implementation.

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
  and the same rule overrides always produce the same recommendation. Live research does not
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
| Structure | A pipeline of focused skills plus fresh-context worker processes for research, source support and review | One large skill: body too long for the research's skill-size guidance, the builder would review its own work, and one description would have to trigger for too many tasks. A Claude Code workflow script: Codex has no equivalent, which breaks harness parity |
| Harnesses | Claude Code and Codex equally | Claude Code first: gives up the parity the knowledge base itself keeps |
| Model access | Harness CLIs with the user's existing login. The owner's development is subscription-only, user-confirmed on 2026-10-08. Forge asks before continuing with an API-key login, which may cost extra (2026-10-09) | Direct model API adapters, additional API tokens/keys, API credits and paid fallback: outside the user's subscription-only constraint, even if promotional credits could cover usage |
| Worker isolation | Automated workers in each harness under the disclosed `best-effort-v1` policy, user-approved on 2026-10-09 | Blocking all implementation until complete tool absence and containment are proved; shared Claude backend or manual replacement of workers were not selected |
| Knowledge-base home | Its own repo; the plugin bundles a pinned snapshot | Same repo as the tooling: couples research and tooling releases. Fetching pages at run time: non-deterministic, needs network, and brings outside content into context, which the security guide warns against |
| Verification | Scripts first, then a fresh-context review worker on a fixed rule list | Model-only review: not deterministic |
| Granularity | Deciding questions per part of an idea | One round for the whole idea: fails when parts need different mechanisms |
| Build order | A thin slice for the skills concept, end to end in both harnesses, before extracting the other concepts | Extracting every rule first: the schema and contracts would only be tested after hundreds of rules depend on them |
| Overrides | Choosing another mechanism only warns; a chosen mechanism that cannot meet a stated goal stays an error | Downgrading every fit failure to a warning: "verified" would hide unmet goals |
| Re-verification | The user chooses "Review" (fixed parts, linked parts, parts with changed inputs) or "Extensive review" (every part) | Fixed parts only: a change can break the part that calls it. Always full: costs a full reviewer run for every small fix |
| Idea research | A separate `harness-research` skill, run twice by the intake: a short survey before the split, and a deep pass per chosen part before building | Research only before the intake: the goal is not yet clear, so it covers too much or the wrong topic. Research only before building: the recommendation cannot use it, and existing solutions surface too late. A tool the user runs alone: the forge could not rely on its output |
| Outside controls | Recommended with prerequisites and listed in the result's README as "recommended, not verified"; never built, configured or checked on the platform | Building them through platform APIs: the forge would need admin tokens, which the identity research advises against. Checking them with a read-only token: not wanted; the README makes each recommendation visible instead |
| Harness KB drift | The user decides: adopt the correction at once as a documented per-repository rule override, or keep the pinned rule; an issue or comment on `agent-harness-kb` is proposed for approval | Waiting for a reviewed Harness KB release: blocks the user's work on a correction they already accepted. Research changing rules without a user decision: fetched content could steer the build |
| License | AGPL-3.0 for every repository in the organization, with an additional permission that excludes files harness-forge generates in a user's repository | Plain AGPL-3.0: leaves open whether generated configuration in a user's repository is covered |

## Account and development boundary

Clarified by the user on 2026-10-09: public Forge uses standard `claude`
and `codex` CLIs, vendor-default account locations and the user's existing
login. No personal alias, profile directory or plugin is a public
prerequisite. Forge does not initiate login/logout, switch accounts, copy
credentials or change saved configuration. A missing login blocks the run;
Forge never adds an API key or selects another account.

**Login type.** A subscription login draws on the plan's usage limits; an
API-key login bills each request, so a run can cost extra. The README
tells users how to check their login type. Before the first worker launch
of a run, the adapter reads the type read-only (`claude auth status`,
`codex login status`). A subscription login continues. For an API-key
login, or a type it cannot determine, Forge states that the run may cost
extra and asks one question: continue or stop. The answer is recorded in
the run's worker evidence. A run without a user stops at that point.
The owner's own work stays subscription-only (see "Model access").

The owner's configuration is a temporary local-development exception on
this machine only, governed by the [development note](../plans/harness-forge-local-development.md).
It must not become a product default, including through later agents.
Worker-specific restrictions remain temporary launch settings. Separate
worker profiles are optional operator precautions, not required setup or
proof of authentication isolation. Existing account storage may expose
unrelated data as well as login material; that remains a disclosed gap.

## Accepted worker isolation gap

Claude Code and Codex retain the same automated workflow and functional
acceptance requirements. Their tool and context restrictions may differ;
equal features do not imply equal or certified containment. Each harness
uses independent CLI processes with explicit role inputs, no
intentional builder/researcher conversation inheritance, and the strongest
available restrictions selected and recorded by its adapter.
Native subagents are excluded from this release's three worker adapters;
the tested native launch paths had observed violations. This is a release
choice, not a claim about every possible native configuration. M1's
separate-process observations inform adapters but do not certify them.

Mandatory baseline controls: an initially empty temporary working
directory outside the target repository, only staged role inputs, a small
environment allowlist, closed extra file descriptors, no session
resume/fork, and suppressed optional settings/hooks/plugin discovery.
Pass only necessary OS environment for the existing login. When the user
has set the vendors' account-location variables `CLAUDE_CONFIG_DIR` or
`CODEX_HOME`, pass them through unchanged; Forge never sets or changes
them. This is how a user, including the owner on this machine, selects a
non-default profile without any personal setup in the product. Do not inherit
API keys, provider overrides, unrelated credentials or arbitrary parent
variables. Disable apps and configured
MCP servers in both adapters. Codex must explicitly disable apps,
including `apps._default.enabled=false`, suppress user/project discovery
and disable remaining configured MCP servers by ID; an empty merged table
alone is insufficient. Claude uses strict empty-MCP configuration and
explicit role tool lists. Record exact settings and any managed-policy
conflicts. A known failure to apply these baseline controls blocks launch;
lack of complete runtime containment proof remains the accepted gap.

Research is instructed to use web access for its brief only. Source
support is instructed to judge only the supplied claim, quotation and
context without tools. Review is instructed to read only the frozen
candidate and supplied rules, without network access or writes. Configure
the following role controls as mandatory launch settings for supported
versions; T11 records exact version-checked syntax:

- Claude: web tools only for research, an empty tool list for source
  support, and read-only file tools for review.
- Codex: a filesystem policy allowing no writes and only required input
  reads where configurable; web search enabled only for research and
  disabled for support/review. Disable shell execution and local-image
  tools for source support. Apply supported tool-removal settings for
  each role; do not interpret a read-only sandbox as scoped read access.

Known inability to apply a required setting blocks launch. Residual
model-added tools and unproved enforcement remain disclosed under this
policy, not counted as successful containment. Remaining tools, automatic
discovery,
inherited settings, credential access and outbound channels may exceed
them: complete absence or denial is not guaranteed. An empty directory,
tool list or cooperative refusal does not prove containment.

Use this mode only for trusted projects and operator-approved inputs.
Do not rely on it to keep secrets, unrelated files or credentials hidden
from workers or to contain hostile content. Fetched pages and candidate
text remain untrusted data even in a trusted project. Human acceptance of
findings does not prevent access or transmission that already occurred.
Apply Forge's own outside-control rule to research: recommend an
operator-provided disposable environment without a target-repository mount,
project secrets or unrelated credentials, with minimal supplied inputs and
operator-managed network controls blocking private, loopback, link-local
and cloud metadata destinations, including resolved/redirect destinations
where the operator controls fetching. Public-web access still permits
outbound transmission; this is not an exfiltration guarantee. Mark it
`recommended, not verified` in Forge's README. Subscription authentication
is still needed by the harness;
its separation from worker-readable data is not proved. This is not a
credential-free promise, a mandatory container or platform provisioning.

Record `worker_policy: best-effort-v1` and `isolation_status: not-certified`
with the harness/version/model, configured controls, observed tools and
behavior, unknowns and evidence references. Bind that record to the run
and show it in the current contract. Missing isolation proof alone does
not block this policy; missing functional capabilities, invalid output,
source-support failure or an observed out-of-scope action still fails the
affected worker run and prevents its output advancing. Do not broaden
tools or switch accounts silently to recover.

All source checks, requirement acceptance, rule checks, current-session
confirmation and result precedence remain mandatory. `verified` describes
the built artifact against its confirmed rules and goals; it never certifies
Forge's worker containment. Per-run reports and Forge's own README must
display the gap alongside successful results. Generated READMEs need no
generic section about Forge's build process; their artifact-specific
limitations and `Outside controls` obligations remain unchanged. If a user's
goal requires enforced isolation, this policy cannot establish that goal;
use the existing conflict/outside-control flow without downgrading errors.
This exception concerns Forge's three workers only; disposable runtime
tests, catalog-only checkers and outside-control boundaries are unchanged.

The recorded [decision](../plans/2026-10-09-harness-forge-decisions.md)
and [last diagnostic](../plans/2026-10-09-harness-forge-catalog-spike-results.md)
distinguish the accepted policy from the observed evidence. No worker is
declared functionally supported until live checks pass in that harness.

## Repositories

All in the `franks-ai-skills` organization, all public, all licensed
AGPL-3.0. `harness-forge` adds the output exception from "Decisions".

| Repo | Contents |
| --- | --- |
| `agent-harness-kb` | The current `playground/docs/`, plus `rules/<concept>.yaml`, `rules/selection.yaml`, the check scripts' fixtures, and tagged releases with a changelog |
| `harness-forge` | The plugin: skills, worker instructions and adapters, check scripts, a pinned knowledge-base snapshot, and `.claude-plugin/marketplace.json`, which Claude Code and Codex both read |
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
         2. review worker, fresh context: judged rules and goal fit
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
   - Does it need its own context, other tools or another model? When
     a hook could be chosen: does it need a model of its own, or only
     other tools?
   - Does it reach an external system, and does a CLI exist for it?
   - Can a script decide it without judgment?
   - For a hook, when it decides whether the handler can run there: at
     which event must it run? Events and their capabilities are
     recorded per harness.
   - For a hook, when the event's capabilities decide it: must its
     result prevent the action the event is about, stop the agent's
     further work, reach the agent as feedback before its next step, or
     only report? A step
     that must run every time does not have to prevent or stop
     anything.
   - For a hook, when a capability holds only for one source of the
     event: which source must it handle, for example a session start
     after compaction or a configuration change outside managed
     policy settings?
7. **Recommendation.** An outcome per part with alternatives, pros
   and cons, each citing rule ids and pages, plus how the parts
   connect, for example "B starts A; C enforces A's result". An
   outcome is one of:
   - **harness only:** a harness mechanism, such as a skill, hook,
     subagent or the harness's own permission and sandbox settings,
     for local actions no outside system sees;
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
   are recorded. An override that cannot meet a stated goal triggers
   the goal-conflict question (see "Overrides").

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
- **Boundary.** A file that runs the agent belongs to the harness and
  can be built, for example a CI workflow that starts the agent
  (automation). Anything that enforces a rule on the repository,
  account or machine is an outside control and is only recommended:
  required checks, rulesets and branch protection, `CODEOWNERS` and
  the setting that requires code-owner review, scanner and policy
  configuration, credentials and identity, network rules, containers,
  dev containers and VMs. The harness's own sandbox and permission
  settings stay harness mechanisms.
- Each recommended control comes with its prerequisites as Harness KB
  rules, from the guide's seven conditions, for example "the agent's
  identity is on no bypass list" and "approvals reset on new pushes".
  A CI job, for example, is a gate only once the repository requires
  it to pass and its workflow definition is protected.
- Every recommendation in which an agent opens pull requests includes
  a merge rule, and every built harness setup includes a recommended
  `CODEOWNERS` entry for the agent's own configuration files together
  with the setting that requires code-owner review; the file alone
  enforces nothing.
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
"recommended, not verified". `harness-intake` writes and updates the
section when the user decides, so it exists even when no part is
built; builders never write it. `harness-verify` checks with a script
that every outside control in the decision record appears there. Verification never checks whether
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
status: decided           # decided → built → verified; blocked until the user decides on security or compatibility drift
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

A skill that researches the user's idea, not the harness. Its research
runs in a separate worker process and the skill can also be started on its own; a later intake then
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

- The research worker receives only an approved research brief: the
  goal, the user's picture, the parts and their accepted answers. The
  adapter limits access to other files where possible, because search
  arguments and fetched URLs can carry data out (OpenAI's deep-research
  security guidance, cited in `docs/guide/security.md`).
- It uses web access for research and returns structured findings for
  the parent to persist in `.harness/research/`. The worker is instructed
  not to write files; configured limits and gaps follow `best-effort-v1`.
- Restrictions are configured and their behavior tested per harness;
  tests do not establish complete containment. Codex
  subagents inherit the parent's sandbox and live runtime overrides
  even when the agent file says otherwise
  (`docs/vendors/codex/subagents.md`), so an agent file alone does not
  enforce them; this release's workers are independent processes.
- It returns structured findings, each with a source. Fetched text
  reaches builders only through findings the user confirmed, never as
  instructions.
- Research never changes the computed recommendation directly. It can
  suggest answers or parts; the user confirms them, and
  `rules/selection.yaml` computes the recommendation from the
  confirmed answers.

**Knowledge-base drift.** When research finds that a fact in the
pinned Harness KB is outdated, the report lists it as drift, with its
source and the source-support check result. Research never changes
the pinned snapshot. The user decides what happens next; the forge
never acts on drift on the research's own say-so, because fetched
content could invent drift to steer a build.

- **Issue.** The forge searches `agent-harness-kb` for an open issue
  on the same rule. If one exists, it proposes a comment there;
  otherwise it proposes a new issue. The user approves the text before
  anything is filed, because the text is derived from fetched content.
- **Adopt the correction.** The user overrides the pinned rule for
  this repository, effective immediately, without waiting for a
  Harness KB release. See "Rule overrides".
- **Keep the pinned rule.** The part continues, and every applicable
  check and stated goal must still pass against the pinned version.

When the drift touches a security rule or would break compatibility,
the affected parts stop at `blocked` until the user has chosen. Other
drift does not block; the pinned rule applies until the user chooses.

### Rule overrides

A rule override replaces a pinned Harness KB rule for one repository,
on the user's decision.

- **Where.** `.harness/overrides/<rule-id>.yaml`, committed. It never
  edits the snapshot and applies only to the repository that holds it.
- **Content.** The overridden rule id, the pinned version, the new
  rule or `retired: true`, the drift finding with its source and
  quote, the user's reason, the date, and the issue or comment link,
  or `pending` or `not published` when the user declined or has not
  yet approved filing. Adopting the override does not depend on
  publishing.
- **What it may change.** Statement, parameters, severity,
  `applies_to`, or retire the rule. It may only refer to catalog
  checkers; it can never add executable code.
- **Before approval** the forge shows the old and new rule side by
  side with the source quote. A finding that failed the source-support
  check cannot be adopted. When the override loosens or retires an
  `error` rule or a security rule, the forge says so explicitly before
  the user decides.
- **Precedence.** For the repository that holds it, an approved
  override replaces the pinned rule with the same id in every stage:
  intake selection, builders and verification. It changes nothing
  else. Goal-fit checks come from the decision record, not from
  Harness KB rules, so retiring a rule never removes the check that a
  part meets its accepted goal.
- **In verification** overrides are bound inputs like the Harness KB
  version. The report states "verified with N overrides" and lists
  each one, so an override is never silent.
- **Approval in the session.** An override file and its recorded
  decision can both be written into the repository under review, so a
  record in the repository never proves approval on its own. Overrides
  apply only after the contract confirmation in the current session
  (see "Contract confirmation" under harness-verify).
- **On a Harness KB update** the forge compares each override with the
  new release. If the release contains the correction, it proposes
  removing the override; if the release keeps the old rule, it asks
  the user whether to keep the override.

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
2. **Judged checks.** A review worker starts with a fresh context
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

- the user confirmed the part's contract in this session (see
  "Contract confirmation");
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
  the Harness KB version, the rule overrides, the Idea KB revision,
  the decision record's answers and the checker versions. A change to
  any of them returns the affected parts to `built`, even when the
  generated files did not change.

`verified` means the part passed the static checks and the listed
runtime tests at the recorded versions. It does not mean the part is
free of defects the rules do not cover.

**Results per part.** The report gives two separate results per
part.

Harness result, for what was built:

- `verified`: all conditions above hold;
- `not verified`: the part was built but at least one condition fails;
- `not applicable`: nothing is built for the part, as for an
  outside-only or "nothing fits" part;
- `not checked`: the part reuses an existing artifact whose files are
  not yet available locally. Once the artifact is installed or
  vendored, `harness-verify` checks its files read-only like a build,
  and the result becomes `verified` or `not verified`.

Goal result, for the part's accepted goal, decided in this order:

1. `not assessed`: the contract is unconfirmed, the part is
   `blocked`, the harness result is `not checked`, or a bound input of
   a part without a build changed after the run was prepared, so
   nothing was assessed against a trusted goal.
2. `not met`: the harness result is `not verified`, whether or not the
   goal also needs outside controls, or the confirmed outcome is
   "nothing fits". A failed build is reported as a failure, never as a
   dependency.
3. `depends on outside controls`: the goal needs at least one outside
   control, listed by name, and the harness result is `verified` or
   `not applicable`. The forge never checks platform settings, so it
   never reports such a goal as met. "Never merge without review", for
   example, stays here even when the review workflow is `verified`.
4. `met by the verified build`: the harness result is `verified` and
   the goal needs no outside control.

### Contract confirmation

Everything the verifier judges against lives in the repository under
review, and so does its history. A pull request could weaken a goal,
change the accepted requirements or the chosen mechanism, and delete
the record of having done so; checking only for recorded weakening
decisions would miss that. No trusted baseline exists outside the
session: a local approval cache would be writable by the agent, which
runs as the user.

So each intake and verification run starts with one confirmation
question showing the current contract: the idea's reach, hosting and
confirmed facts, and per part: its name, the goal, the confirmed
answers, the chosen outcome and mechanism, for a reuse part the reused
artifact (name, source, license, maintenance, form and local path), the
outside controls, the accepted Idea KB requirements as readable text
together with the revision's sha256, and every rule override with its
content and sha256. The hash binds the confirmation to exact content;
the text lets the user understand what they confirm. A record whose
facts contradict its targets or reach is refused instead of shown. Differences from the last confirmation recorded in the
repository are highlighted as a hint, labelled as coming from an
untrusted record. Only a contract the user confirms in the session is
used. A part whose contract is not confirmed is `blocked`, and its
goal result is `not assessed`. A run without a user, such as a CI run,
therefore reports every goal as `not assessed`.

### Overrides

When the user chose a mechanism other than the recommended one:

- rules that only say "a different mechanism was recommended" report
  as warnings;
- rules that say "the chosen mechanism cannot meet a goal the user
  stated" stay errors and trigger a goal-conflict question.

**Goal-conflict question.** One multiple-choice question per part,
asked when the intake detects the conflict from `rules/selection.yaml`
right after the override, and again in verification when an error of
this kind appears there. It first shows the current state: the part's
goal, the chosen mechanism, the failing rule ids with their sources,
and the recommended mechanism with its pros and cons. Then:

1. **Use the recommended mechanism** (listed first). A harness
   mechanism returns the part to its builder; an outside control
   returns it to the intake, which updates the decision record and
   the README section. The part and its linked parts are re-verified.
2. **Adjust the goal.** The forge proposes a concrete wording the
   chosen mechanism can meet, for example "must hold under prompt
   injection" → "should hold for honest work", and accepts free text.
   The decision record keeps the old goal as history. The changed goal
   then goes back through the steps it affects: the per-part
   questions and selection, the research brief and deep pass when the
   goal's domain or requirements changed, and acceptance of any
   changed requirements, before anything is rebuilt. Verification
   results bound to the old goal are invalidated.
3. **Keep as is.** Nothing changes. The error stays in the report and
   the part is never `verified`.

The answer and its reason are recorded in the decision record.

### Re-verification

On request, builders fix the failing parts. The user then chooses the
scope of the next run in one multiple-choice question that shows, for
each option, the parts and the number of judged rules it covers:

1. **Review (recommended)**: the fixed parts, every part linked to
   them through `connects_to`, every part whose bound inputs changed,
   and the link checks. This is the smallest allowed scope; there is
   no option to check the fixed parts alone.
2. **Extensive review (rarely needed)**: every part against every
   applicable rule, with a fresh reviewer. It also catches effects
   that `connects_to` does not show, such as files shared between
   parts.

The choice is recorded in the report.

### Security of the verifier

The files under review may be hostile, so the security guide applies
to harness-forge itself:

- Rule overrides change rules only through catalog checkers, and
  apply only after the contract confirmation in the current session; a
  record in the repository is not proof.
- Rules come from the pinned Harness KB snapshot inside the plugin; a
  confirmed override may replace a rule with the same id. Checker code
  always comes from the pinned plugin and is never overridden.
  Accepted idea rules come from the Idea KB and can only be judged or
  call a catalog checker with validated parameters. Nothing from the repository being
  checked is executed as a check.
- Runtime tests run the candidate's own code, so they run in a
  separate, disposable environment with synthetic credentials and an
  explicit network allowlist. Forge sets this environment up
  automatically as a throwaway workspace holding only the candidate,
  its needed references and synthetic fixtures, with a small environment
  allowlist. The harness authenticates with the user's existing login at
  its account location, passed through unchanged; Forge creates no test
  login or profile (user decision, 2026-10-09). Suppress user-level
  skills, plugins, instructions, hooks and MCP servers where the harness
  allows, and record what remains loaded and the account exposure.
  Each test declares its permitted tools and launches with matching
  harness controls; an observed tool call outside that list fails the
  test. A skill without bundled code can still cause tool calls, and
  file/web tools, hooks and MCP servers can run outside a harness's
  shell sandbox ([sandboxing](https://code.claude.com/docs/en/sandboxing)),
  so the sandbox alone does not cover a test. Candidate code a test
  executes runs only under the harness sandbox limited to that workspace.
  What remains loaded is classified:
  - executable components (hooks, MCP servers, apps, plugin monitors or
    other plugin executables) must be off; if one stays active, the
    test is unavailable;
  - a competing skill (Forge's own skills, one with the candidate's name,
    or one that could answer the test prompt in its place) invalidates
    the affected activation test, which is `not-run` with the reason;
  - context only (instruction files, unrelated skills) is disclosed; the
    test remains functional evidence with that extra context.
  Clean-installation evidence additionally needs an observed inventory
  with no user-level skills or plugins; otherwise that evidence is
  unavailable and needs a user decision, not a disclosure.
- Check scripts run with time and output limits and do not execute
  the files they check.
- The reviewer is instructed to use read-only supplied data and no network
  or writes. Apply available tool limits and report remaining exposure
  under `best-effort-v1`, as for research. Observed violations fail the run.
- Reviewer output is validated against a schema: every applicable rule
  id must appear exactly once, and unknown ids are rejected.
- A fresh session avoids intentionally forwarding the builder's
  conversation; automatic context discovery remains an accepted gap.
  It does not remove prompt injection inside reviewed files. Instructions
  treat file contents as data, and a judged verdict can never
  overrule a failed script check.

## Testing harness-forge itself

- **Rules:** every script check has good and bad fixtures in
  `agent-harness-kb` that show it fires on the bad case only.
- **Research:** the research worker's output is validated against its schema,
  and every cited domain is checked against `docs/sources.md`. Fixture
  cases with stubbed fetches cover: a trusted source whose text does
  not contain the quote; a real quote that does not support its
  claim ("supported only on Linux" cited for "supported on every
  platform"); an override file without a recorded user decision; an
  override with a forged "approved" record but no confirmation in the
  session; an override changed after its approval; a goal and its
  accepted requirements weakened with the history removed, which the
  contract confirmation must show; a failed build, reported `not met`;
  an outside-only part, reported `not applicable` and `depends on
  outside controls`; a confirmed "nothing fits" part, reported `not
  applicable` and `not met`; a reuse part before and after its
  artifact is available, reported `not checked` and `not assessed`,
  then checked like a build; an
  override that loosens a security rule without the explicit warning
  having been shown; research reused after the goal
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
- **Self-check:** harness-forge's own skills and worker instructions pass
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
