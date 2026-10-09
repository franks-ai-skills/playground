# harness-forge Skills Thin-Slice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development or superpowers:executing-plans
> to implement this plan task by task. Steps use checkbox (`- [ ]`)
> syntax for tracking.

**Goal:** Deliver the skills pipeline from an idea to a portable build
and a contract-bound report in clean Claude Code and Codex installations.

**Architecture:** A Python core owns schemas, selection, checkers and
report calculation; four skills own conversations and stage handoffs.
The plugin bundles an immutable snapshot from a separate Harness KB
repository. Harness adapters run independent CLI processes for research,
source-support and review under `best-effort-v1`; configured restrictions and their
gaps are reported. Fetched content and candidate files remain data.

**Tech Stack:** Python 3.11+, standard-library `unittest`, JSON Schema
2020-12, YAML rules, Markdown skills and reports. PyYAML/jsonschema are
provisional dependencies: T3 chooses their distribution or a validated
alternative before pinning. Use the installed harness CLIs, with no
direct model API integration or personal plugins. Model access uses the
harness CLIs' existing login; Forge adds no API tokens/keys, API credits
or paid fallback (user-confirmed 2026-10-08). The owner's development
runs are subscription-only; see the account boundary below.

**Account boundary (clarified 2026-10-09):** public adapters invoke standard
`claude`/`codex` with the user's existing login at vendor-default
locations. Before the first worker launch, the adapter reads the login
type; for an API-key or unknown login it warns of possible extra cost and
asks continue/stop (parent design, "Account and development boundary"). The owner's profile and wrapper choices apply only to temporary
development on this machine; see the [local development note](harness-forge-local-development.md).
All subsequent agents must preserve this boundary. Do not require custom
profiles, manage logins, copy credentials or modify saved settings.
Temporary per-worker restrictions remain required. Optional operator-managed
profiles do not establish credential isolation. Historical diagnostic
profiles and synthetic test environments are not public installation steps.

**Spec:** [Thin-slice scope](../specs/2026-10-07-harness-forge-thin-slice.md)
and [parent design](../specs/2026-10-06-harness-forge-design.md).
Read both before execution. The user approved the design, scope and plan
together on 2026-10-07 and chose native execution with a stop after M1.
The scope's decision list distinguishes implementation choices from the
parent requirements. On 2026-10-09 the user selected option 3, documented
in the amended parent and scope: automated workers with weaker isolation,
with the gap in relevant READMEs. This resolves the M1 policy stop; T3 is
the next implementation task. Native execution remains selected.

## Global Constraints

- “The tooling runs in Claude Code and Codex as equals. OpenCode is
  best-effort.” No OpenCode builders in this slice.
- “Only the answers the user confirms from it feed the selection.”
- “Every recommendation, verification finding and verdict about a
  mechanism cites a rule id and the Harness KB page behind it.”
- “Every idea research finding cites its source with a verbatim quote.”
- “One question per message, multiple choice where possible.”
- “Checker code always comes from the pinned plugin and is never
  overridden.” Nothing from the repository under review is executed by
  static checks; runtime tests use separate disposable environments.
- “Only a contract the user confirms in the session is used.” A run
  without a user reports every goal as `not assessed`.
- “Outside controls … never built, configured or checked on the
  platform.” README status: `recommended, not verified`.
- “Rules that say ‘the chosen mechanism cannot meet a goal the user
  stated’ stay errors and trigger a goal-conflict question.”
- Re-verification labels: `Review (recommended)` and
  `Extensive review (rarely needed)`; no fixed-parts-only option.
- “All … public, all licensed AGPL-3.0.” `harness-forge` adds the
  generated-output permission decided in the parent design; T13 drafts
  its exact wording for approval before publication.
- Apply the full source policy and trusted/rejected domain tables in
  `docs/sources.md` before adding, changing or citing a research source.
  Every execution research/writing brief carries that policy. Fetch the
  original, check support, label practitioner evidence, drop unsupported
  claims, exclude X, and preserve exact numbers and quotes.
- Preserve AGENTS.md's instruction-file and attribution conventions.
  Repository skills use `.agents/skills/` and relative
  `.claude/skills/` symlinks. Packaged plugin skills use `skills/`.
- Apply the parent's `best-effort-v1` worker policy in both harnesses.
  Unproven isolation is disclosed, not counted as a passing restriction
  or a functional blocker by itself. Invalid output, missing capabilities,
  actual scope violations and unmet isolation goals still block affected
  work. Artifact `verified` never certifies worker containment.

## Review Focus

1. Repository history can forge or erase approvals and weakened goals;
   display the entire current contract and require a fresh answer (T7).
2. Linked parts, shared files and changed non-file inputs can invalidate
   earlier results; find the affected closure before reporting (T10).
3. A real source quote can support a narrower claim than research makes;
   reject it independently of quote matching (T8).
4. Malformed rules, path escapes and hostile prose can steer execution;
   use closed schemas, bounded reads and catalog-only checkers (T4/T5/T9).
5. Unavailable builders, controls or reused files can masquerade as
   success; preserve recommendation and result distinctions (T6/T9).

## Starting point and execution layout

Planning baseline: playground branch `ai-stuff`, commit `14ba931`, clean
before these documents were added. It contains `docs/`, the routing
skill and the parent design; no application code, test runner or plugin
manifest. Local versions observed on 2026-10-07: codex-cli 0.160.1 and
Claude Code 2.1.292. These are observations, not promised minimums;
rule applicability retains each cited version range.

Use `PLAY`, `KB` and `FORGE` below as repository-root labels, not literal
directories. Default local checkouts are sibling directories:
`playground/`, `agent-harness-kb/` and `harness-forge/`, under their common
parent. Separate Git repositories remain separate deliverables. Detect
existing checkouts/remotes before creating them.
Use the worktree skill when execution requires branch isolation.

Task 1 establishes local repositories; publish them only as part of an
authorized execution handoff. Do not remove playground's KB before its
destination is reviewable and published. Merging follows git-flow and
requires an explicit request. Each task ends with a Conventional Commit
in each changed repository and the actual writer's `Assisted-by` trailer.
Stage explicit paths. Planning does not create repositories or publish.

Keep `plans/` and `specs/` in playground when moving the KB. Repair the
KB's link to the playground design and all playground documentation
pointers; no planning-directory exception is needed inside `docs/`.
From T5, KB is the authoritative research checkout. Keep playground's
research copy frozen until T13; its instructions and routing skill must
direct corrections to KB. Forge rules still come from the pinned snapshot,
so updating the KB checkout does not silently change an existing run.

## Milestones and execution order

| Milestone | Tasks | Reviewable result |
| --- | --- | --- |
| M1: feasibility | T1-T2 | Minimal local bootstrap and actual worker-boundary evidence in both harnesses |
| M2: offline workflow | T3-T10 | Distribution choice, sourced rules and a complete primary workflow with stubbed research/review |
| M3: live workflow | T11 | Both research passes, acceptance, skill build, generated-skill runtime tests and fresh verification in each harness, plus a small routing smoke suite |
| M4: remaining flows | T12 | Override/drift conversations, goal conflicts, fixes and both review choices |
| M5: distribution | T13-T14 | Clean installs, published destinations, KB move, full routing evaluation and final reference evidence |

M1 checkpoint on 2026-10-07: T1 is complete; T2's negative/inconclusive
feasibility report is recorded in [M1 results](2026-10-07-harness-forge-m1-results.md).
No launcher was declared production-supported. The requested stop before
T3 remained in effect while the unchecked certification items were reviewed.
The [2026-10-08 diagnostic proposal](2026-10-08-harness-forge-worker-diagnostic.md)
prioritizes an external boundary for both harnesses, retains per-role
capability checks, and fixes the acceptance criteria and effort
limit. A no-model tool-removal gate comes first, followed by controls,
bounded diagnostics, a configuration freeze and qualification without
mid-run fixes. The user approved this diagnostic on 2026-10-08; its
[no-model gate stopped unproven](2026-10-08-harness-forge-worker-diagnostic-results.md)
without live calls. At that checkpoint T3 was stopped; no mandatory
outside-control dependency was approved.

The later [offline-init follow-up](2026-10-08-harness-forge-offline-init-results.md)
observed an empty advertised tool list for the tested `claude-tp` profile,
with a valid `Read` control. Context/discovery, profile portability,
external DNS, guest/authentication isolation and the other roles remain
unqualified; Codex's complete tool-removal configuration is also unproven.
Two blocked prompt-bearing launches are charged and both correction
allowances are spent. No further experiment follows automatically from
the 28 unused invocation slots. The [decision brief](2026-10-09-harness-forge-decisions.md)
records the subsequent policy choice.

On 2026-10-09, the user approved one final offline catalog spike. Its
[result](2026-10-09-harness-forge-catalog-spike-results.md) establishes
configuration acceptance but not complete tool absence. The diagnostic
round finished with no model calls. The user then selected automated
workers with weaker isolation in both harnesses (option 3), and requested
README disclosure. The strict isolation gate is superseded by the parent's
`best-effort-v1` policy. T3 can proceed; T11 must still establish functional
support. Earlier failed/unproven evidence and the grader are unchanged.
There is no automatic extension of the diagnostic or mandatory container.

Each milestone presents evidence, limitations and changes for review.
M1-M4 are intermediate results, not completion of the entire slice.
Once execution is authorized, milestone reports do not create automatic
permission stops. Pause for a required new design decision, or if the
user chooses milestone approval gates in the execution handoff.

T2 precedes the substantial core work and dependency pins. T3 is a
bounded packaging assessment before core implementation; it does not
delay the feasibility answer. Use independent CLI processes with explicit
role inputs and mandatory baseline controls from the parent design;
native delegation is excluded from this release's worker adapters.
T11 proves functional parity under the accepted policy; unavailable
functions still block, while unproven
containment remains visible. A stronger containment claim would require
separate evidence rather than reinterpreting the M1 results.

## File responsibilities and contracts

| Repository | Paths | Responsibility |
| --- | --- | --- |
| KB | `docs/`, `AGENTS.md`, `.agents/skills/agent-harness/`, `.claude/skills/agent-harness` | Migrated research and local routing |
| KB | `schemas/{rule,catalog,selection}.schema.json`, `rules/{skills,security,selection,outside-controls}.yaml` | Validated rules and selection data |
| KB | `checks/catalog.yaml`, `policy/severity.md`, `rules/coverage.yaml`, `fixtures/` | Checker parameters, severity rationale, extraction coverage and good/bad cases |
| KB | `kb-manifest.json`, `CHANGELOG.md`, `tools/validate.py` | Initial KB identity, content hashes and data validation |
| FORGE | `pyproject.toml`, `requirements.lock`, `scripts/forge.py`, `src/harness_forge/` | Installable deterministic core and CLI |
| FORGE | `src/harness_forge/{documents,models,selection,contracts,overrides,research,build_skill,verify,scope,report,runtime}.py` | Focused stage implementations and disposable skill tests |
| FORGE | `src/harness_forge/checks/{runner,skills,links,outside}.py` | Pinned static check implementations |
| FORGE | `src/harness_forge/adapters/{base,claude_code,codex}.py` | Worker calls, configured limits and recorded gaps; no user-message authentication |
| FORGE | `schemas/{decision,research,source-support,override,review,report,worker-request,worker-response}.schema.json` | Closed inter-stage formats |
| FORGE | `skills/{harness-intake,harness-research,build-skill,harness-verify}/SKILL.md` | User-facing pipeline procedures |
| FORGE | `skills/<name>/references/{contract,claude-code,codex}.md`, `workers/{researcher,source-support,reviewer}.md`, `adapters/codex/{researcher,source-support,reviewer}.toml` | Stage contracts and harness-specific worker instructions. Keep worker instructions out of the plugin's `agents/` directory: Claude Code loads it as native plugin subagents, which this release excludes |
| FORGE | `templates/skill/`, `snapshot/`, `tools/pin_snapshot.py`, `tools/live_checks.py`, `evals/`, `tests/` | Build defaults, pinned KB, packaging, live checks and tests |
| FORGE | `packaging/assessment.md`, `evals/canaries/`, `evals/smoke/`, `legal/generated-output-permission.md` | Distribution decision, early evidence and exact license permission proposed for approval |
| FORGE | `plugin.json`, `.claude-plugin/{plugin,marketplace}.json`, `LICENSE`, `README.md`, `AGENTS.md` | Public installation, licensing and contributor account boundary |
| PLAY | `examples/reproduction-checklist/`, `examples/pipeline-outcomes/`, `tools/check_references.py`, `README.md`, `AGENTS.md`, `plans/harness-forge-local-development.md` | Reference results, KB migration pointers and local-only development instructions |
| Target repository | `.harness/reports/<slug>.md`, `.harness/overrides/<rule-id>.yaml` | Verification reports and repository-scoped rule overrides; reference targets live under PLAY examples |

Shared types live in `models.py` as dataclasses. JSON Schema defines the
wire format; its unknown keys are rejected. `Rule`, `Decision`,
`Recommendation`, `ResearchBrief`, `Finding`, `AcceptedRevision`,
`Contract`, `Confirmation`, `CheckResult`, `ReviewResponse`,
`VerificationRun`, `WorkerEvidence`, `RuntimeResult` and `PartResult` have the fields described below.
No implicit YAML booleans: answer values are enums or JSON booleans,
and ambiguous scalars are rejected rather than silently converted.
Create `tests/__init__.py` in the bootstrap so the named unittest modules
below import consistently. Examples use `unittest.TestCase` assertions.

`Rule` extends the design example with `applicability: script | judged`
(default `script`), machine predicates and optional contested positions.
Conditions use a closed `all`/`any`/`not`/`eq`/`in` predicate grammar over
declared facts. No Python expressions, templates or dynamic imports.
An evidence-based severity elevation carries its recorded rationale.
Selection data contains question definitions and an ordered list of
rules. Its script rules use catalog id `selection.match`, whose validated
parameters contain a fact predicate and the outcome/concept it implies.
This gives selection corrections the same catalog-only override path as
other rules; changing prose alone cannot change computed routing.

`Contract` contains readable per-part goals/outcomes/mechanisms,
outside controls, accepted requirement text and revision hash, override
text/hashes, worker-policy disclosure and evidence digest, rendered `text`
and a digest. `Confirmation` contains run id,
contract digest and confirmed part ids. `Finding` contains id, pass/part,
claim, source, fetch date, quote, context and brief digest. `AcceptedRevision` contains
accepted rule ids/content, brief digest and content digest.
`VerificationRun` contains run id, decision/contract digest, applicable
rules per part, frozen inputs/hashes, static results and judged requests.
`finish_run` attaches validated runtime results to it for reporting.
`WorkerEvidence` records `worker_policy: best-effort-v1`,
`isolation_status: not-certified`, role/harness/version/model, launcher and
configuration digest, configured controls, observed tools/behavior,
unknowns and evidence references. Unknown inventory remains unknown.
Worker responses, research records and verification reports reference this
record; existing closed worker/report schemas validate it. A changed worker
policy/configuration invalidates affected evidence and contract confirmation.
`RuntimeResult` records run/part/case ids, prompt and expected behavior,
observed activation evidence, `pass | fail | error | not-run`, reason,
checked-file hashes, harness/tool versions and disposable environment.
Report schema validates these records separately from rule verdicts.
`PartResult` contains part id, lifecycle status, harness result, goal
result, outside dependencies, rule results and goal verdict. Wire schemas
use the exact result strings from T10; Python fields use snake_case.

`Decision` records the user's picture verbatim, whole-idea facts, stable
part ids, retired ids, normalized per-part answers, outcomes, cited
alternatives, chosen mechanism, research hashes, accepted revision,
connections and outside controls. Each control records prerequisites,
availability and `required_for_goal`, explicitly confirmed by the user.
Recommendations that protect configuration remain present even when
they are precautions rather than dependencies of the accepted goal.
Unknown availability never proves a requested guarantee.

`Confirmation` is scoped to the current live run and exact contract
digest. The active agent displays the full contract and asks a question
with `Confirm` and `Leave pending` choices. The user may explicitly select
Confirm or give an unambiguous textual confirmation of the displayed
parts. The agent relays `choice`, `displayed_digest`, `part_ids` and
`run_id` to the script after the answer. A preselected option is not an
answer. Silence, ambiguous text, a prior approval or changed content
leaves the affected parts pending. Partial confirmation covers only the
named parts. Scripts reject digest/run/part mismatches and never load
repository approval records as authority; they cannot authenticate that
the relayed answer came from the user. This is a session ceremony, not a
claim to resist an agent with the user's full privileges. No approval
cache, reusable approval token or user-turn reading API is introduced.

CLI interface: `python scripts/forge.py <command> --help`; commands
`validate-kb`, `select`, `research-check`, `prepare-contract`,
`check`, `report` and `scope` emit bounded JSON. Offline commands never
infer live confirmation; unattended reports remain unassessed.
Live skills use adapters for the conversation-dependent finalization.

## Task 1: Establish a minimal local bootstrap

**Files:** `KB/README.md`, `KB/LICENSE`, `FORGE/LICENSE`,
`FORGE/pyproject.toml`, `FORGE/src/harness_forge/__init__.py`,
`FORGE/tests/{__init__,test_bootstrap}.py`.

**Interfaces:** Consumes the existing repository state. Produces separate
local checkouts and an importable empty `harness_forge` package for the
feasibility probe, without runtime dependencies or a KB migration.

- [x] Write `test_bootstrap_has_no_personal_plugin_dependency`: import the
  package with an empty temporary user configuration directory. Assert
  `self.assertEqual(import_result.returncode, 0)` and verify no third-party
  modules are required by this bootstrap.
- [x] Run `python -m unittest discover -s tests -p test_bootstrap.py -v`
  from FORGE; expect failure until the package exists.
- [x] Create or reuse the sibling checkouts and minimal Python package.
  Copy the existing AGPL text. Leave runtime distribution to T3, research
  migration to T5 and exact generated-output permission to T13. Keep
  source research available in playground for the probe's approved brief.
- [x] Re-run bootstrap tests. Expected: the package imports using only
  the standard library. Do not publish these preliminary repositories.
- [x] Commit: `chore: establish harness KB and forge workspaces`.

## Task 2: Spike worker isolation in both harnesses before core work

**Historical acceptance criteria:** the checklist below records the
original strict-isolation experiment. Keep its failed/unproven findings
and unchecked certification items as evidence. The user superseded that
release gate with `best-effort-v1` on 2026-10-09; do not mark these checks
passed or rerun them as a prerequisite for T3.

**Files:** FORGE `tools/live_checks.py`, `tests/test_live_checks.py`,
`evals/canaries/{research,review}.yaml`,
`evals/canaries/results/{worker-boundaries.md,evidence-index.json}`; candidate adapter modules
and role files are disposable probes at this stage. T11 adopts the
supported launcher into `src/harness_forge/adapters/` and documents it.

**Interfaces:** Probe CLI:
`python tools/live_checks.py --harness <harness> --case worker-boundaries --launcher <native|process>`.
Produces a capability matrix for `research`, `source-support` and
`review`, with observed context, effective tools/policies, version/model,
OS and architecture. No library dependencies are needed for the probe.

- [ ] Define benign canaries with expected denials and one allowed web
  fetch. Put distinct canaries in the parent conversation, repository
  instructions, discovered skill material, unrelated repository files
  and an outside file. Research receives only an approved brief and
  source policy; support receives only claim/quote/context; review
  receives frozen candidate files, decisions and applicable rules.
- [x] Run the canary runner before restrictions exist; expect capability
  failures rather than a successful isolation result. A worker merely
  declining to disclose data it can access is not a passing restriction.
- [ ] Probe a fresh native subagent and an independent process in Codex;
  test Claude Code's native worker and its independent-process option
  where supported. For Codex's process use a fresh `codex exec` in an
  empty temporary directory with explicit permission/tool settings and
  controlled configuration discovery. Do not resume/fork a session.
  Test inherited environment, user/project/managed configuration, hooks,
  plugins, MCP/connectors, instruction/skill discovery and credentials
  as separate surfaces. Normal model authentication may be available to
  the harness, but must not become worker-readable repository data.
  An empty directory or `--ignore-user-config` alone is insufficient.
  Verify named permission profiles actually apply: legacy sandbox keys
  and `--sandbox` can change precedence. A new process remains subject
  to any outer OS restrictions; it is not an escape from them.
- [x] Run the CLI above for each harness/launcher candidate. Research
  must have functioning web access and no repository reads or writes
  outside research; the parent may write its returned structured output.
  Support must have no file/web/write tools. Review must have read-only
  supplied data and no network/write access. Inspect tools and startup
  context as well as actual blocked attempts. Test broad parent runtime
  overrides and record their effect. Save redacted evidence and versions;
  claim support only for tested OS/architecture/version combinations.
- [x] Record one supported launcher per role/harness or mark unavailable.
  Equal guarantees are required; identical launch methods are not. If
  no tested approach meets the restrictions, stop before substantial
  implementation and present alternatives with their design impact.
  Failed candidates do not prove all Codex approaches impossible. Retain
  the evidence; adopt probe code only after its implementation contracts
  are defined and tested in T11. No Claude workflow add-on is introduced.
- [x] Commit: `test: record worker isolation feasibility`.

Execution evidence: 23 attempts tested native and independent-process
candidates in both harnesses, broad Codex parent overrides, startup
canaries, actual tools and side effects. No tested Codex candidate proved
the complete restrictions; Claude process observations are promising but
not a production support declaration. Full role payloads, managed/user
configuration positive controls, authentication isolation, supplied-data
reads and every discovery surface remain open certification checks.
Those unchecked items did not pass. They are now disclosed limitations
under the accepted policy rather than prerequisites for core work or pins.

Historical follow-up proposal: explicitly select models and test both harnesses
against the same role payload, supplied-data, discovery, authentication
and external-boundary matrix. A container/VM is the primary experiment,
while source-support tool absence and reviewer read-only tools remain
required. Its ownership and installation impact must be settled before
adopting it for production. Those diagnostics are finished; the later
accepted policy does not mandate a container or another isolation round.

## Task 3: Choose distribution before pinning dependencies

**Files:** FORGE `packaging/assessment.md`, `requirements.lock`,
`tests/test_dependency_conformance.py`, `tests/fixtures/schema-conformance/`;
update `pyproject.toml` after recording the choice.

**Interfaces:** Consumes Draft 2020-12 and the YAML record requirements.
Produces a validator/distribution choice, supported environment matrix,
complete hashed lock and exact installation procedure. The initial
PyYAML/jsonschema choice remains provisional until this task concludes.
Test helper `validate_fixture(name: str) -> bool` lives in
`tests/test_dependency_conformance.py` and invokes the candidate library
against the named fixture. It is not an independent validator.

- [ ] Create conformance fixtures for closed objects, local references,
  enums, conditional schemas, wrong scalar types and forbidden remote
  resolution. Pin rejection with
  `self.assertFalse(validate_fixture("unknown-checker"))`. Assess parsing
  and validation of new idea/override/decision YAML, not just snapshots.
- [ ] Compare (a) platform-specific bundles using existing upstream
  wheels where available, (b) a maintained pure-Python validator with
  Draft 2020-12 support, and (c) a documented one-time isolated setup.
  Fetch the entire dependency graph and record installation effort,
  offline use, OS/architecture/Python coverage and maintenance. Include
  the native `rpds-py` dependency if retaining modern jsonschema; existing
  wheels may avoid source builds. Do not write a YAML parser or schema
  validator, or change the design's YAML formats to simplify packaging.
- [ ] Run `python -m unittest tests.test_dependency_conformance -v`
  against viable candidates in disposable environments. Expected:
  required valid/invalid fixtures classified correctly, no remote
  resolution and a working install on every claimed environment.
  Untested environments are recorded rather than claimed supported.
- [ ] Record the default and rationale in `packaging/assessment.md`.
  Bound this assessment to the three options; it follows the capability
  answer in T2. If a choice changes formats, schema dialect or public
  platform requirements, show the design change before proceeding.
  Otherwise adopt the supported option, lock runtime dependencies and
  hashes, and document the exact bootstrap. No personal config changes.
- [ ] Commit: `chore: select and pin forge runtime distribution`.

## Task 4: Define closed data schemas and a checkable rule inventory

**Files:** KB schemas, catalog, severity policy, coverage inventory and
`tools/validate.py`; FORGE schemas, `models.py`, `documents.py`,
`tests/test_documents.py`, `tests/test_rule_schema.py`,
`tests/fixtures/minimal-kb/`, `scripts/forge.py`.

**Interfaces:** `load_document(path: Path, schema: str) -> dict`;
`canonical_digest(value: dict) -> str`; `validate_kb(root: Path) -> list[str]`.
Canonical JSON uses sorted keys, compact separators and UTF-8; hashes
of files use their actual bytes. Markdown records have YAML frontmatter.

- [ ] Add `test_closed_rules_and_catalog_parameters`: both design rule
  examples validate; duplicate ids, unknown fields/checkers, script
  paths, invalid params, executable YAML tags and contested errors fail.
  Add `test_answer_scalars_and_contract_hashes`: answer key ordering
  preserves the digest; changed text changes it; `yes` is not silently
  normalized to a boolean. Add `test_document_limits`: duplicate keys,
  excessive YAML nesting, files over 1 MiB and `../` paths are rejected.
  Add worker-evidence fixtures: reject missing policy/configuration
  bindings and fabricated certified status; retain unknown tool inventory
  as unknown. Validate the same evidence record in worker/report schemas.
  Pin rejection with
  `with self.assertRaises(ValueError): load_document(bad_path, "rule")`.
- [ ] Run `python -m unittest tests.test_documents tests.test_rule_schema -v`;
  expect missing loaders/schemas or rejected-input assertions to fail.
- [ ] Implement the three interfaces and the shared types. Define a
  1 MiB document limit and depth 32; reject external schema resolution.
  Define catalog parameter schemas, rule-kind semantics and severity
  caps. `pass` always means compliance, including `must-not` rules.
  Validate stable ids and all rule citations against snapshot pages.
  Give catalog entries implementation versions, never executable paths
  supplied by a rule. Add the argparse CLI entry
  `main(argv: list[str] | None = None) -> int` in `scripts/forge.py`,
  initially with `validate-kb`; later tasks add their owned commands.
  Emit bounded JSON to stdout and diagnostics to stderr; use exit codes
  0 for success, 1 for failed checks and 2 for invalid input.
- [ ] Run the same tests; validate a minimal KB with
  `python scripts/forge.py validate-kb --kb tests/fixtures/minimal-kb`.
  The minimal fixture is labelled synthetic; the real researched KB is
  copied and validated in T5. Expected: bounded JSON with no validation
  errors; intentional malformed fixtures fail.
- [ ] Commit: `feat: define forge contracts and rule schemas`.

## Task 5: Extract skills rules and implement pinned checkers

**Files:** KB `rules/{skills,security,outside-controls}.yaml`,
`rules/coverage.yaml`, `checks/catalog.yaml`, `fixtures/{skills,security,outside}/`;
FORGE `checks/{runner,skills,links,outside}.py`, `tests/test_checks.py`,
`tests/{test_rule_coverage,test_bootstrap}.py`, `tools/pin_snapshot.py`,
`snapshot/`; KB `docs/`, `AGENTS.md`, `kb-manifest.json` and routing
skill/symlink; PLAY `AGENTS.md`, `.agents/skills/agent-harness/SKILL.md`.

**Interfaces:** `run_check(rule: Rule, files: dict[str, bytes],
facts: dict) -> CheckResult`; `pin_snapshot(kb: Path, destination: Path) -> dict`.
`check_migration_source(playground: Path, manifest: dict) -> list[str]`
in `tools/pin_snapshot.py` compares retained research against its source
inventory; an empty list means no unexpected changes.
`CheckResult` has part id, rule id, `pass | fail | not-applicable | error`,
severity, reason and sources. Worker failure is never a pass.

- [ ] Write a fixture-driven test for every script rule: good passes,
  bad fails. Pin description lengths at 1,024/1,025 and names at
  64/65 characters; malformed frontmatter, mismatched names, broken
  portable symlinks and dangling references fail. Test timeouts and
  output truncation as explicit errors, and assert a candidate helper
  that writes a marker is never executed by a static check.
  Core assertions: `self.assertEqual(good.status, "pass")`,
  `self.assertEqual(bad.status, "fail")` and
  `self.assertFalse(marker.exists())`.
  Add `test_kb_copy_preserves_source_bytes_and_links`: compare copied KB
  bytes, permit only enumerated cross-repository link repairs and resolve
  local Markdown links and the relative routing-skill symlink.
  Record the playground source commit and research-file hashes in the
  migration section of `kb-manifest.json`. Test that the playground
  instructions route corrections to KB after copying, and that changing,
  adding or deleting a retained research file fails T13's removal guard.
- [ ] Run `python -m unittest tests.test_checks tests.test_rule_coverage tests.test_bootstrap -v`;
  expect uncovered sections and missing checker ids to fail.
- [ ] Copy the research, source policy, instructions and routing skill to
  KB, preserving bytes except enumerated link repairs. Keep playground's
  original research files frozen until publication in T13. After the copy
  succeeds, update PLAY's AGENTS.md and routing skill to send research
  reads and corrections to KB, applying its source policy and propagation
  rules there. Retain the local copy as migration evidence. Sweep all
  skills layers, their practices, anti-patterns, portability/dropped
  sections and security/checklists. Include relevant
  cross-concept security and outside prerequisites. Re-fetch each rule's
  cited primary source under the source policy before retaining it.
  `coverage.yaml` maps every section/item to rule ids or a sourced,
  explicit exclusion; it is not a checklist-only extraction. Implement
  catalog checks for frontmatter, names, description length, paths,
  schemas, references, links and README coverage. Meaning, injection
  intent and goal fit remain judged. Advisory size guidance warns.
  Run checkers in subprocesses with a 5-second/64-KiB limit and immutable
  input bytes; disable network and candidate imports.
- [ ] Validate all fixtures and coverage, then pin `snapshot/` with
  `kb-manifest.json`: initial version, source commit and per-file hashes.
  Include docs, rules, schemas, policy, catalog and fixtures. No runtime
  KB fetch. Reproduce the manifest from the same commit and compare it.
  Validate the real copied KB with
  `python scripts/forge.py validate-kb --kb <KB>`, and re-run copy/link
  assertions before retaining the initial snapshot.
  Later KB corrections require an explicit decision about the release
  pin. If re-pinned, validate the new snapshot, invalidate affected bound
  results and re-run their checks; do not auto-sync the snapshot.
  Implement the migration guard and expose
  `python tools/pin_snapshot.py --check-migration-source <PLAY> --kb <KB>`
  as a read-only check with nonzero exit on unexpected source changes.
- [ ] Commit: `feat: add sourced skills rules and deterministic checks`.

## Task 6: Compute recommendations from confirmed answers

**Files:** KB `rules/selection.yaml`, `fixtures/selection/`;
FORGE `selection.py`, `tests/test_selection.py`,
`evals/harness-intake/behavior-selection.yaml`.

**Interfaces:** `recommend(answers: dict, whole_idea: dict,
rules: list[Rule], candidates: list[dict]) -> Recommendation`;
`next_question(part: dict, whole_idea: dict, selection: dict) -> dict | None`.
`Recommendation` contains outcome, mechanism, alternatives, controls,
pros/cons and cited rule ids/pages. All inputs must be confirmed facts.

- [ ] Add fixed answer sets for every overview concept and all five
  outcomes. Assert the same result under reordered input keys. Assert
  a missing decisive answer produces a question, not a default choice;
  remaining answers that all lead to one outcome stop questions.
  Assert fresh-context review selects a subagent, user-triggered
  recurring procedure selects a skill/command, and merge enforcement
  selects an outside control. A researched reuse candidate needs
  confirmed fit, license and maintenance facts. Unavailable controls
  produce `nothing-fits` for a guarantee; a non-skill choice is retained.
  Pin each case with `self.assertEqual(actual.outcome, expected_outcome)`
  and `self.assertEqual(actual.mechanism, expected_mechanism)`;
  `self.assertEqual(next_question(resolved_part, facts, table), None)`
  proves the stop condition.
- [ ] Run `python -m unittest tests.test_selection -v`; expect failures
  until the declarative tables and evaluator exist.
- [ ] Encode the overview's use/avoid distinctions for all ten concepts
  and outside-control conditions in selection data. Keep detailed
  non-skills rules out of this slice. Name priorities and tie-breaking
  in the data; ambiguous facts request a deciding answer. Normalize
  inputs before evaluating; never read raw research as a predicate.
  Add configuration-protection recommendations for every build, merge
  controls for agent-created PRs and isolation for the design's forced
  cases. Include prerequisites and known/unknown plan availability.
  Expose `select` through T4's CLI using confirmed normalized inputs.
- [ ] Re-run all selection fixtures and KB validation. Expected:
  recommendations cite existing rules/pages and stop-question logic
  agrees with enumerated remaining answer sets.
- [ ] Commit: `feat: compute reproducible mechanism recommendations`.

## Task 7: Bind conversations to the current contract and decision

**Files:** FORGE `contracts.py`, `overrides.py`,
`skills/harness-intake/{SKILL.md,references/contract.md}`,
`tests/test_contracts.py`, `tests/test_intake.py`, `tests/test_overrides.py`,
`evals/harness-intake/{routing,behavior}.yaml`.

**Interfaces:** `render_contract(decision: Decision, revision: AcceptedRevision,
overrides: list[dict]) -> Contract`; `confirm_contract(contract: Contract,
relay: dict, run_id: str) -> Confirmation | None`;
`effective_rules(pinned: list[Rule], overrides: list[dict],
confirmation: Confirmation | None) -> list[Rule]`;
`update_outside_section(readme: str, decision: Decision) -> str`.
Relay fields are `choice: confirm | pending`, `displayed_digest: str`,
`part_ids: list[str]` and `run_id: str`. The active agent creates the relay
only after explicit current-session confirmation, by selected option or
unambiguous text. The script checks its bindings, not its human origin.

- [ ] Add `test_forged_approval_never_confirms`: recorded approval with
  absent live response blocks; changed override bytes invalidate a
  response for the old digest. Add `test_erased_history_shows_contract`:
  weakened goals/requirements remain fully visible even when all prior
  history is deleted. Confirm the readable requirements, their revision
  hash and every override's readable content/hash are shown.
  Add tests for A+C→A with C retired, B→B1/B2, next unused letter,
  reciprocal link repairs and one question at a time.
  Test explicit selected/textual confirmation, partial confirmation,
  silence, ambiguity, a preselected but unsubmitted choice, unknown part
  ids, stale digests and a response for another run. Pending parts stay
  blocked and their goals unassessed. Nonempty rule overrides block until
  T12 implements their full adoption flow.
  Core assertion:
  `self.assertIsNone(confirm_contract(contract, pending_relay, run_id="new-run"))`.
  Pin the erased-history case with `self.assertIn(weakened_goal, contract.text)`.
- [ ] Run `python -m unittest tests.test_contracts tests.test_intake tests.test_overrides -v`;
  expect missing ceremony, state transitions and README handling.
- [ ] Implement the interfaces and intake procedure. Start each intake
  run with the whole existing contract; for a new idea show its empty
  contract and confirm additions when they are decided. Record survey
  use and split confirmation before selection. Show prior differences
  only as an untrusted hint. No unattended confirmation path.
  Store `.harness/decisions/<date>-<slug>.md`; intake alone maintains
  the result README's `Outside controls` section, including no-build
  parts, preserving unrelated README content. No generic Forge-isolation
  section is mandatory in a generated README. Show the `best-effort-v1`
  disclosure in the current contract and bind its policy/evidence digest
  to confirmation; T10 persists it in the run report. Display override content
  even before override handling exists; block rather than silently ignore
  a nonempty override list. `effective_rules` initially handles the pinned,
  no-override path. T12 adds validated adoption and full override precedence.
  Expose `prepare-contract` through T4's CLI. Loaded decisions or
  historical confirmations can render the question but cannot confirm it.
- [ ] Re-run tests, including missing README entries, forged approvals,
  stale/missing contract isolation disclosure, changed worker evidence, changed
  contracts and all relay bindings. Confirm that record loading
  never constructs a live Confirmation. Override update and publication
  conversations defer to T12; their presence currently blocks the part.
- [ ] Commit: `feat: confirm contracts and preserve intake decisions`.

## Task 8: Research the idea with independently supported findings

**Files:** FORGE `research.py`,
`skills/harness-research/{SKILL.md,references/contract.md}`,
`workers/{researcher,source-support}.md`, `tests/test_research.py`,
`tests/fixtures/research/`, `evals/harness-research/{routing,behavior}.yaml`.

**Interfaces:** `make_brief(decision: Decision, pass_name: str,
part_id: str | None) -> ResearchBrief`;
`validate_finding(finding: Finding, fetched_text: str,
support: dict) -> Finding | None`;
`accept_requirements(proposed: list[Rule], choices: dict,
brief_digest: str) -> AcceptedRevision`.
Support verdicts name finding ids and include quote/context reasoning.

- [ ] Test stubbed fetches: trusted domain but absent quote is dropped;
  a real Linux-only quote with an all-platform claim is dropped by the
  independent support verdict; X/mirrors are dropped; an inaccessible
  source is dropped. Reject duplicate/unknown support ids. Assert page
  instructions cannot add an accepted answer, override or requirement.
  Changed goal/targets/reach/part answers invalidate the brief digest.
  Unaccepted requirements never reach the accepted revision.
  Pin unsupported quotes as
  `self.assertIsNone(validate_finding(finding, text, unsupported_verdict))`
  and acceptance as `self.assertEqual(revision.rule_ids, accepted_ids)`.
- [ ] Run `python -m unittest tests.test_research -v`; expect missing
  source filtering, quote checks and acceptance transitions.
- [ ] Implement brief-bound survey and deep passes. Findings include
  source URL, fetch date, verbatim quote, surrounding context and source
  role. Run exact quote matching against fetched text, then a distinct
  fresh support worker before showing the finding. Treat quoted material
  as data; configure no-tool support where possible and record residual
  capability under `best-effort-v1`. An observed out-of-scope action fails
  that worker run; an unproven tool-removal setting alone does not waive
  or fail the semantic support check. Respect source reproduction limits.
  Record search mode and limits.
  Survey proposes candidates/parts/answers; user confirmation makes
  them selection inputs. Deep research proposes catalog-only/judged
  `idea.<slug>.` rules; acceptance creates the hashed revision in
  `.harness/research/<slug>.rules.yaml`. Store both passes and findings
  in `<slug>.md`. Reuse standalone research only for the same brief.
  On mechanism/goal incompatibility return to intake before building.
  Expose `research-check` through T4's CLI for deterministic validation;
  requirement acceptance remains the live agent's conversation.
- [ ] Test security/compatibility drift blocks affected parts; ordinary
  drift keeps the pinned rule. Source-support failure prevents adoption.
  T12 adds the user decision, override and issue/comment conversations;
  until then unresolved security/compatibility drift stays blocked.
  Re-run tests with simulated drift and an edited accepted requirement.
- [ ] Commit: `feat: research and accept sourced idea requirements`.

## Task 9: Build a portable skill from accepted inputs

**Files:** FORGE `build_skill.py`, `templates/skill/`,
`skills/build-skill/{SKILL.md,references/contract.md}`,
`tests/test_build_skill.py`, `evals/build-skill/{routing,behavior}.yaml`.

**Interfaces:** `plan_skill(decision: Decision, part_id: str,
revision: AcceptedRevision, rules: list[Rule]) -> dict[str, str]`;
`write_skill(root: Path, planned: dict[str, str]) -> list[Path]`.
The skill's model writes domain procedure text; scripts validate paths,
accepted inputs, templates and the resulting artifact inventory.

- [ ] Add tests for canonical `.agents/skills/reproduction-checklist/SKILL.md`
  and relative `.claude/skills/reproduction-checklist` symlink; include
  only accepted requirements and runtime-needed sourced references.
  Assert traversal/symlink escapes and overwriting unrelated files fail.
  A non-skill choice returns `builder unavailable` without changing the
  recommendation; remote reuse stays read-only and unbuilt. Require
  current contract confirmation and matching accepted-revision hash.
  Builder-unavailable parts are `blocked` before building: harness result
  `not applicable` (no artifact) and goal result `not assessed`. Keep the
  recommendation as data for the later builder; never mark it built.
  Pin portability as `self.assertTrue(claude_path.is_symlink())` and
  `self.assertEqual(claude_path.resolve(), canonical_path.resolve())`.
- [ ] Run `python -m unittest tests.test_build_skill -v`; expect the
  accepted-input and portable-artifact assertions to fail initially.
- [ ] Implement planning/writing and the focused builder procedure.
  Commands use this builder, with both leads' user-only invocation
  controls when required by the sourced rules. Do not include personal
  skill names or assume their installation. Never interpolate source
  content into shell commands. Preserve a matching existing skill;
  show a concrete diff before replacing conflicting existing content.
  Set successful builds to `built`, never `verified`. Update artifact
  lists for configuration-protection advice through intake, which owns
  README writes; builders do not write the outside section.
- [ ] Run builder and static-check tests on the reference fixture;
  inspect its files and symlink. Expected: procedure requests a checklist
  without executing the reproducer; rejected requirements are absent.
- [ ] Commit: `feat: build portable skills from accepted research`.

## Task 10: Verify completeness, goal fit and bound inputs

**Files:** FORGE `verify.py`, `scope.py`, `report.py`,
`workers/reviewer.md`,
`skills/harness-verify/{SKILL.md,references/contract.md}`,
`tests/{test_verify,test_scope,test_report}.py`,
`evals/harness-verify/{routing,behavior}.yaml`; target repository
`.harness/reports/<slug>.md`.

**Interfaces:** `prepare_run(decision: Decision, files: dict[str, bytes],
rules: list[Rule], confirmation: Confirmation | None) -> VerificationRun`;
`validate_review(run: VerificationRun, response: dict) -> ReviewResponse`;
`finish_run(run: VerificationRun, review: ReviewResponse,
runtime_results: list[RuntimeResult], current_inputs: dict) -> list[PartResult]`;
`review_scope(decision: Decision, fixed: set[str], changed: set[str]) -> set[str]`;
`render_report(run: VerificationRun, results: list[PartResult]) -> str`;
`write_report(repository: Path, slug: str, rendered: str) -> Path` writes
`.harness/reports/<slug>.md` under that target repository.

- [ ] Write table-driven tests for exact result precedence:
  unconfirmed/blocked→`not assessed`; failed build→`not verified` and
  `not met` even with outside dependencies; outside-only→`not applicable`
  and `depends on outside controls`; confirmed nothing-fits→
  `not applicable` and `not met`; remote reuse→`not checked` and
  `not assessed`; local reuse is checked read-only; verified build without
  goal dependencies→`met by the verified build`. Optional precautionary
  controls remain in README without silently becoming goal dependencies.
  Missing/error/duplicate/unknown verdicts prevent `verified`.
  Test that `best-effort-v1` plus unproven containment alone does not block
  an otherwise complete artifact result; reports must still display
  `not-certified`. An actual worker scope violation or a goal requiring
  enforced isolation cannot be converted into success by this policy.
  Pin each row as `self.assertEqual(result.harness_result, harness_expected)`
  and `self.assertEqual(result.goal_result, goal_expected)`; pin shared-file
  invalidation as `self.assertEqual(affected_parts, {"A", "B"})`.
  Test separate runtime reporting: empty evidence renders `none run`;
  unavailable tests carry reasons and never count as passes. Reject
  runtime results for another run or changed files; a failed or errored
  executed test prevents `verified`. Stub results test these contracts;
  the live producer is implemented in T11.
  Assert the exact report path and reject slug traversal or symlinks that
  would escape the target repository.
- [ ] Run `python -m unittest tests.test_verify tests.test_scope tests.test_report -v`;
  expect result, applicability and invalidation assertions to fail.
- [ ] Implement applicability before review, with explicit out-of-scope
  reasons. Run all applicable script rules and link/README checks.
  Request exactly one judged verdict per applicable id plus a per-part
  goal verdict linked to accepted goal/requirement ids. Goal ids remain
  independent of retireable KB rules. `not applicable` is allowed only
  for judged applicability; an error-rule exclusion needs a live user
  confirmation. A model cannot reverse a script failure. Missing or
  false goal-fit verdicts prevent success. Record all file hashes,
  KB version/content, overrides, Idea revision, answers, tools/checker
  versions and runtime tests, grouped by part and rule. Freeze inputs
  before workers run and hash them again before finalization; changes
  invalidate the result even when file content stayed the same.
  Report runtime cases and their outcomes separately from static/judged
  checks. Include WorkerEvidence and the isolation disclosure beside
  overall results, including `verified`; test policy/configuration changes
  invalidate relevant evidence. Offline M2 runs execute no runtime tests
  and say `none run`;
  empty evidence never implies runtime behavior was checked.
  Persist the rendered Markdown at `.harness/reports/<slug>.md` using
  the bounded target-repository path, including the chosen review scope.
  Expose `check`, `report` and `scope` through T4's CLI. Unattended
  reporting has no live confirmation and leaves goals unassessed.
- [ ] Test transitive links, shared-file owners, deleted files and every
  bound input changing independently. `Review` includes fixed parts,
  transitive linked parts, all parts with changed inputs and link checks;
  shared checked files invalidate every owner. `Extensive review` covers
  all parts. Show exact sets and judged counts before asking; preserve
  unchanged historical checks only when all bound inputs still match
  and the current whole contract has been confirmed. No-user runs
  perform static checks but assess no goals. Run the test suite again.
- [ ] Commit: `feat: report contract-bound verification results`.

## Task 11: Prove the live vertical workflow before extending it

**Files:** FORGE `tools/live_checks.py`, `evals/smoke/vertical.yaml`,
`tests/{test_adapters,test_pipeline,test_runtime}.py`, `runtime.py`,
`src/harness_forge/adapters/{base,claude_code,codex}.py`,
`adapters/codex/{researcher,reviewer}.toml`,
`skills/<name>/references/{claude-code,codex}.md`,
`skills/harness-verify/SKILL.md`; PLAY
`examples/reproduction-checklist/{claude-code,codex}/`.

**Interfaces:** Implement an independent-process adapter informed by
T2's evidence, without claiming T2 certified it, as
`preflight(harness: str, role: str) -> dict` and
`run_worker(request: dict, harness: str) -> dict`.
Add `run_skill_runtime(run: VerificationRun, harness: str,
cases: list[dict]) -> list[RuntimeResult]` in `runtime.py` for the
verification skill and live runner to call before `finish_run`.
Consume T4-T10's stage contracts. Produce a live reference run in each
harness with accepted idea rules, a portable skill and a report. This
milestone proves the primary workflow, not the completed slice.

- [ ] Define one live no-override/no-conflict case and offline adapter/
  orchestration assertions. Require both research passes, independent
  source support, explicit requirement acceptance, a skill build and a
  fresh reviewer. Pin `report["idea_revision"] == decision["idea_revision"]`
  and check expected rule ids appear exactly once. Missing functional
  capability, absent current policy disclosure/confirmation or a request
  requiring certified containment prevents launch, with
  `self.assertFalse(worker_was_started)`. A disclosed extra tool or
  unproven denial under the accepted policy alone does not prevent launch.
  Native worker launch requests fail before spawning. Test mandatory
  account behavior: standard executable names and vendor-default account
  resolution without owner-specific paths or aliases. Test that local
  development overrides never become defaults or packaged requirements,
  missing authentication returns unavailable, no login/logout or account
  fallback is attempted, and saved settings remain unchanged. Test that a
  set `CLAUDE_CONFIG_DIR`/`CODEX_HOME` reaches the worker and the
  login-type check unchanged, and that an unset one stays unset. Test the
  login-type check with stubbed `claude auth status`/`codex login status`
  output: a subscription login launches without a question; an API-key or
  unparseable result asks continue/stop before any worker starts, `Stop`
  leaves `worker_was_started` false, the answer lands in WorkerEvidence,
  and a run without a user stops. Record Claude's `apiKeySource` from the
  init event as well.
  Check role-specific tool/web/filesystem settings against the matrix below;
  reject a known failure to apply one. Test mandatory
  baseline preparation: a temporary cwd outside the target repository with
  only staged role inputs, a small environment allowlist, closed extra
  descriptors, no resume/fork and suppressed optional discovery. Include
  seeded user/project MCP and per-app overrides; assert configured servers
  and apps are disabled, rather than assuming an empty overlay removes
  lower-layer entries. A known control-application failure blocks launch.
  Record unknown inventory honestly; test that actual out-of-scope behavior
  discards the worker output and blocks its stage, without silent retries
  that broaden access. Validate independent support/reviewer identities
  and role input digests; do not reuse the builder's conversation.
  Test runtime orchestration with a fake launcher: only frozen candidate
  files enter a disposable profile, supplied fixtures bind to the current
  run, and unavailable/timeout/error outcomes are recorded explicitly.
- [ ] Run `python -m unittest tests.test_adapters tests.test_pipeline tests.test_runtime -v`
  with stub workers; expect the new integration assertions to fail.
- [ ] Connect the active skills to independent CLI worker processes in each
  harness; never fall back to native subagents. Use
  standard `claude` and `codex` executables with the user's existing login,
  vendor account resolution (default location or a user-set
  `CLAUDE_CONFIG_DIR`/`CODEX_HOME`) and the login-type check above.
  Personal setup belongs only to the local development note, never adapter
  defaults. Give
  each
  worker only its role's request and validate its output against T4's
  schemas; relay human confirmation under T7's acceptance rule. Return
  to intake if research changes fit. Pass only necessary OS environment
  names (HOME, PATH, USER, LOGNAME, LANG, TMPDIR, plus documented platform
  needs) for the existing vendor login. Pass `CLAUDE_CONFIG_DIR` and
  `CODEX_HOME` through unchanged when set; never set them. Run the
  login-type check with the same environment as the workers, so it checks
  the profile the workers will use. Do not forward
  arbitrary parent variables, API credentials or provider endpoint overrides.
  Disable optional hooks/plugins/settings discovery. Codex must include
  `apps._default.enabled=false` and disable the apps feature and any
  conflicting per-app overrides; suppress user/project MCP discovery and
  disable remaining configured servers by ID. Claude uses strict empty-MCP
  configuration and explicit role tool lists. Required per-role controls:

  | Role | Claude launch controls | Codex launch controls |
  | --- | --- | --- |
  | Research | `--tools WebFetch,WebSearch` with the matching allowlist | Web search enabled; no-write filesystem policy with reads limited to required inputs where configurable; remove unrelated tools where supported |
  | Source support | `--tools ""` and an empty allowlist | Web search disabled; `features.shell_tool=false`, `features.unified_exec=false`, `features.view_image=false`; no-write filesystem policy and minimum configurable read access |
  | Review | `--tools Read,Grep,Glob` with the matching allowlist | Web search disabled; no-write filesystem policy; scope reads to frozen candidate/rules where configurable; disable unrelated tools where supported |

  These are starting settings from the recorded CLI/source evidence,
  not permanent vendor syntax guarantees. Verify them for supported builds
  during T11, including file-editing restrictions and network controls
  beyond web search. M1 used a named filesystem permission policy; a
  generic read-only sandbox does not by itself restrict which files can
  be read. All roles retain the common apps/MCP/discovery restrictions.
  Model-service access remains necessary even when role web access is off.
  Known setting rejection blocks launch; remaining built-in tools or
  unproved enforcement stay explicit gaps, not silent control removal.
  These are adapter preparation
  requirements, not claims that every tool-registration path is observable.
  Inspect known managed-policy conflicts and fail if required settings
  cannot apply; keep unknown runtime access labelled unknown.
  Record actual tool/configuration observations and run representative
  behavior/scope canaries on the
  adapter under `best-effort-v1`; report denials, failures and unknowns
  separately. Passing benign canaries is not containment certification.
  Missing functional capabilities return unavailable, never a broad
  fallback. Keep the M1 grader/evidence unchanged; use a distinct live
  functional assessment that does not relabel original failures as passes.
  Override/drift and fix/review conversations
  defer to T12; unsupported inputs block rather than being ignored.
  Implement the runtime producer using separate disposable harness
  profiles, synthetic credentials and explicit network allowance. Synthetic
  credentials serve only as candidate fixtures; they cannot authenticate
  model calls. Live model access uses the existing subscription without
  copying login material. Document that exposure separately; if required
  candidate-test isolation cannot be achieved, record unavailable rather
  than relaxing it. Load
  the actual generated skill and its needed references, with no forge
  skills available to substitute for it. Static checkers never launch
  candidate behavior. Record observed activation signals; absence of an
  observable signal is `not-run` with a reason, never an invented pass.
- [ ] Run `python tools/live_checks.py --harness claude-code --case vertical`
  and the Codex equivalent from clean test installations using existing
  subscription authentication. Keep this machine's development account
  selection explicit; do not create/copy login profiles. Use the same
  confirmed
  answers and record actual findings. Preserve a justified reuse outcome;
  exercise the build separately with a confirmed no-reuse fixture.
  Before finalizing its report, test the generated reproduction-checklist
  skill with an explicit invocation, an implicit positive where supported,
  and an adjacent negative prompt. Define prompts and expected activation
  in `evals/smoke/vertical.yaml`; record evidence bound to the generated
  files in each harness. Require a completed explicit activation test for
  the live build case. An unavailable optional activation mode is reported
  with its reason; an unavailable required test blocks this milestone.
  Run `--case routing-smoke`: one explicit invocation, one implicit
  positive and one near miss per skill/harness, once each (24 cases).
  Record unsupported modes; do not invent an implicit-load trace marker.
- [ ] Inspect reports, generated files and acceptance records. Script
  failures cannot be reversed by review. Missing live confirmation
  leaves goals unassessed. Record restrictions, versions and model ids;
  fix integration failures and re-run affected cases. Present this
  milestone's evidence and limits before the remaining conversations.
- [ ] Commit: `test: prove the live skills vertical workflow`.

## Task 12: Complete overrides, drift, conflicts and fix/review flows

**Files:** FORGE `contracts.py`, `overrides.py`, `research.py`,
`selection.py`, `verify.py`,
`skills/{harness-intake,harness-research,harness-verify}/references/contract.md`,
`tests/{test_goal_conflicts,test_pipeline,test_overrides,test_research}.py`;
target repository `.harness/overrides/<rule-id>.yaml`.

**Interfaces:** `resolve_goal_conflict(decision: Decision, part_id: str,
choice: str, adjusted_goal: str | None, reason: str) -> dict`.
Returns the changed decision, invalidated parts and required next stage.
Choices: `recommended`, `adjust-goal`, `keep`.
Return keys are `decision`, `invalidated_parts`, `next_stage` and
`remaining_error_ids`; the last contains the retained goal-conflict errors.
Extend T7's `effective_rules` to apply confirmed catalog-only overrides
uniformly to selection, building and verification. Retiring a KB rule
never removes accepted-goal checks.
`write_override(repository: Path, override: dict) -> Path` validates the
record and writes `.harness/overrides/<rule-id>.yaml` in that repository.

- [ ] Test conflicts detected immediately after selection override and
  again during verification. Assert ordered choices and current goal,
  chosen/recommended mechanisms, failing ids/sources and pros/cons are
  shown. `keep` retains the error. A recommendation-only mismatch warns.
  `adjust-goal` preserves history and invalidates selection/research/
  acceptance when affected; it cannot jump directly to a new build.
  Pin keep-as-is as `self.assertEqual(result["next_stage"], "report")`
  and `self.assertEqual(result["remaining_error_ids"], failing_rule_ids)`.
  Add valid/forged/changed override cases and explicit weakening-warning
  assertions. Test security/compatibility drift decisions, ordinary drift
  keeping pinned rules, publication approval/decline and override handling
  after a KB update. Pending approval cannot unblock affected parts.
  Assert the exact override path, repository scope and unchanged pinned
  snapshot. Reject rule ids or symlinks that escape the target repository;
  overrides from another repository never enter the effective rules.
- [ ] Run `python -m unittest tests.test_goal_conflicts tests.test_pipeline tests.test_overrides tests.test_research -v`;
  expect incorrect warning downgrades or missing rerouting to fail.
- [ ] Implement rerouting: recommended skill→builder; another harness
  concept→intake with builder unavailable; outside control→intake and
  README; adjusted goal→questions/selection and changed-domain research/
  acceptance; keep→failed report. Require fresh confirmation of changed
  contracts. Builders repair only requested failing artifacts. Intake
  owns outside-section repairs. Prompt for Review/Extensive review with
  the calculated scope; record the choice and re-run affected links and
  the selected parts' runtime cases through T11's producer.
  Complete override adoption: validate rule identity, source support and
  catalog parameters; display old/new content and explicit warnings when
  loosening/retiring an error or security rule. Current contract confirmation
  binds each adopted override. On a new KB compare corrections, propose
  removal when incorporated or ask whether to keep it. Search KB issues
  read-only; show exact proposed issue/comment text and require approval
  before publishing either. Keep `pending`, `not published` or the link
  in the record; adoption never depends on publication.
  Store override records at `.harness/overrides/<rule-id>.yaml` as
  commit-ready repository artifacts; persisted records still require
  current-session confirmation to apply.
- [ ] Exercise a full offline pipeline with stub research/review:
  split, survey, choice, deep acceptance, build, error, fix and review.
  A changed override must alter selection/build/checking consistently.
  Re-run conflict and pipeline tests; no branch claims success after
  an unresolved error or changed contract.
  Extend the live T11 runs with one conflict, supported override/drift
  fixture and break/fix cycle, exercising both review choices. Synthetic
  drift sources/issue responses are labelled as fixtures, never presented
  as genuine findings or published to the real KB.
- [ ] Commit: `feat: route goal conflicts and scoped re-verification`.

## Task 13: Package both harnesses and finish the KB migration

**Files:** FORGE manifests, `README.md`, `tests/test_packaging.py`,
`tools/{live_checks,pin_snapshot}.py`, `legal/generated-output-permission.md`, `LICENSE`;
KB manifest/changelog/routing links;
PLAY `README.md`, `AGENTS.md`, `.agents/skills/agent-harness/SKILL.md`,
`docs/` migration and plan links.

**Interfaces:** Same four canonical skills exposed by both packages;
snapshot identity is identical after installation. Author-only skills
are neither dependencies nor silently discovered as requirements.

- [ ] Test manifest versions, four skill names, package-resource paths,
  identical snapshot hashes and all required runtime files. Include a
  clean installation whose personal skill/plugin directories are empty.
  Assert installing/copying the package does not execute candidate code.
  Pin the inventory as
  `self.assertEqual(skill_names, {"harness-intake", "harness-research", "build-skill", "harness-verify"})`
  and `self.assertEqual(installed_snapshot_digest, source_snapshot_digest)`.
  Re-run the migration hash comparison against the current playground
  research files and T5's recorded source inventory before removing any.
  Call T5's `--check-migration-source` command and require success.
  Unexpected additions, edits or deletions block removal. Reconcile them
  into KB under its source policy, record any explicit pin update and
  re-run affected evidence before updating the migration inventory.
- [ ] Draft the exact generated-output permission in
  `legal/generated-output-permission.md` and its placement in `LICENSE`.
  Show both to the user for explicit approval before publishing either
  destination repository or the plugin. The parent settles the license
  choice, not the exception's wording. Record the approved text/digest;
  changes to that wording require review again. Until approval, continue
  local packaging checks but leave publication pending.
- [ ] Run `python -m unittest tests.test_packaging -v`; expect missing
  manifests/resources to fail.
- [ ] Package root `plugin.json`, Claude `.claude-plugin/plugin.json`
  and `.claude-plugin/marketplace.json`, using tested current schemas.
  Both manifests point to the same `skills/`. Recheck marketplace
  compatibility in both CLIs; add a generated Codex marketplace file
  only if the shared entry cannot represent both formats, documenting
  evidence. Document Python dependency bootstrap, the `best-effort-v1`
  worker policy, actual failed-launch evidence and remaining per-harness
  gaps in Forge's README, with links from the KB/playground READMEs.
  Keep per-run provenance in reports; generated READMEs only need their
  artifact-specific limitations and existing outside-control disclosure.
  Forge's own `Outside controls` section must recommend a disposable
  research environment with no project secrets/unrelated credentials and
  operator-managed blocking of private, loopback, link-local and metadata
  destinations (including DNS resolution and redirects where controllable),
  labelled `recommended, not verified`; explicitly retain
  the subscription-authentication exposure and permitted-public-web egress
  gap. Dedicated worker profiles are optional precautions, not installation
  requirements or proof of keychain/credential isolation. This is not a
  mandatory container. Document the standard vendor CLI/existing-login
  setup; exclude owner-specific launchers and account paths from public
  setup examples and defaults. Add packaging checks for that boundary.
  Document configured restrictions separately from unproved ones,
  unavailable capabilities, no-user reports, KB version and generated
  output permission. Runtime setup never modifies personal config
  implicitly. Run `claude plugin validate .` and each CLI's installation
  procedure in an isolated test installation; save the exact working
  commands and account-access limitations. Use the existing subscription
  for live calls without copying credentials or silently creating logins.
- [ ] **Checkpoint before publication: remove personal configuration.**
  Re-check every file that will be published in FORGE and KB, including
  evidence reports, evidence indexes and contributor instructions, for the
  owner's personal configuration: profile and wrapper names, account
  directories, home-directory paths, email addresses and pointers to the
  local development note. Replace each with neutral wording, such as
  "a tested Team-plan profile" or "the user's account location". Where a
  rule keeps evidence unchanged, do not edit it silently: present the
  conflict and let the owner choose between neutral wording, keeping the
  evidence unpublished, or publishing it as is. Confirm that ignored raw
  evidence under `evals/canaries/results/private/` stays unpublished.
  Findings on 2026-10-09, as examples:
  - `evals/canaries/results/diagnostic-2026-10-08.md` and
    `offline-init-2026-10-08.md` name `claude-frank`, `claude-tp` and
    "a separate personal login profile".
  - `diagnostic-2026-10-08-index.json`,
    `diagnostic-2026-10-08-resumed-index.json` and
    `offline-init-2026-10-08-index.json` name both profiles as launchers
    (`"default_launcher_after_diagnostic": "claude-frank"`) and in
    artifact file names such as `claude-tp-guarded.zsh`.
  - FORGE `AGENTS.md` points contributors to
    `../playground/plans/harness-forge-local-development.md`, the owner's
    local setup note.
  - The ignored raw evidence holds copies of the owner's `.zshrc` account
    functions (`claude-tp-gate.zsh`, `claude-tp-guarded.zsh`) and a
    startup event stream with the work account's email address.
  - The README row that named both profiles was already made neutral on
    2026-10-09; recheck it anyway.

  Also check the Git history that will be published: list every author
  and committer email per repository (`git log --format='%ae%n%ce' | sort
  | uniq -c`). The owner's work email must not appear. Before the first
  push of FORGE or KB, rewrite affected commits to the owner's chosen
  address (for example with `git filter-repo --mailmap`), and check that
  the global `user.email` will not reintroduce it. For playground, whose
  history is already public, present the affected commits and let the
  owner decide whether to rewrite and force-push.
- [ ] Publish destination repositories when execution authorizes it,
  and the exact license permission has been approved; then remove only
  the copied knowledge-base files from playground. Keep `plans/` and
  `specs/` in playground. Replace playground's local routing with a pointer
  to the pinned/local KB checkout and public KB for read-only reference; never
  fetch live pages to select forge rules. Update README and AGENTS.md so
  they do not claim a KB still lives locally. Inspect both install
  inventories and all migration links; re-run packaging/bootstrap tests.
  Replace local sibling paths with verified public cross-repository URLs
  on publication. Test README links as GitHub repository-relative paths:
  a link cannot traverse into a sibling checkout. Before publication,
  describe those locations as local code paths, not public Markdown links.
- [ ] Commit per repository: `feat: package forge for Claude Code and Codex`
  / `docs: move harness knowledge base to its own repository`.

## Task 14: Record real reference runs and verify the forge itself

**Files:** PLAY `examples/reproduction-checklist/{claude-code,codex}/`,
`examples/pipeline-outcomes/`, `tools/check_references.py`;
FORGE `evals/catalog/collisions.yaml`, `tools/live_checks.py` and
its own `.harness/{decisions,research,reports}/`.

**Interfaces:** Evidence artifacts include `.harness/` decision/research/
report records, generated skills and relative symlinks, result README,
redacted trace metadata and version/model ids. Never commit credentials
or raw private harness profiles.

- [ ] Define behavior cases for the reference and alternate outcomes,
  and routing cases for all four skills, including adjacent non-forge
  tasks that must not trigger them. `tools/check_references.py` asserts
  schema validity, hashes, accepted-only content, outside README coverage,
  no unexplained rules and exact result labels for each stored example.
  Offline cases cover all parent-design adversarial fixtures; maintain
  an index mapping each fixture to its owning unit test.
  The reference checker asserts
  `assert expected_rule_ids == set(report["rule_results"])` per part
  and `assert report["idea_revision"] == decision["idea_revision"]`.
  For built-skill examples, require T11's generated-skill runtime cases,
  matching run/file bindings and separate runtime outcomes; forge-skill
  routing evidence cannot satisfy this requirement.
- [ ] Run `python tools/check_references.py`; expect absent reference
  evidence to fail. Run the FORGE unit suite to check its offline
  foundation before live execution.
- [ ] In clean test installations with existing subscription authentication, run
  `python tools/live_checks.py --harness claude-code --case reproduction-checklist`
  and the Codex equivalent. Use the same confirmed reference answers;
  record live survey differences rather than demanding identical
  fetched pages. If compatible reuse appears, exercise it honestly and
  use the confirmed no-reuse fixture separately for the build path.
  The human in each run confirms the current contract and accepts
  requirements. Test one break/fix and scoped review; exercise remote
  and local reuse, outside-only and nothing-fits outcomes. No-user
  variants retain `not assessed`. Runtime candidate behavior runs in
  disposable environments with synthetic credentials and explicit
  network allowance; it is separate from static verification.
  Use T11's runtime producer for the generated skill again after fixes
  or installation changes; preserve evidence only if its bound inputs,
  harness versions and runtime setup still match.
  Reuse T11/T12 evidence only when its bound inputs remain unchanged;
  otherwise re-run the affected cases against the installed package.
- [ ] Run each skill's explicit invocation, implicit routing where
  supported and near misses in fresh sessions at this distribution
  milestone. Use about 20 routing prompts per skill and three repeats:
  20 × 3 × 4 skills × 2 harnesses = about 480 runs before baseline arms.
  The initial smoke suite already ran in T11; this broader evaluation is
  not required to reach the first live workflow. Record activation signals
  and baseline behavior. Do not invent a Codex trace marker.
  Run harness-verify against forge's own skills, using its accepted
  contract and pinned rules. Include Forge's own research-isolation
  recommendation: untrusted fetched content plus login material and egress
  triggers it even for a trusted project. Do not automatically mark the
  recommendation as an installed control or a required goal dependency.
  Fix errors; retain warnings and contested
  positions in reports. Assert exact file/hash and rule coverage using
  `python tools/check_references.py`, then run
  `python -m unittest discover -s tests -v` in FORGE and
  `python tools/validate.py` in KB. Skipped required live cases are
  completion blockers; unsupported optional modes retain explicit reasons
  and never count as passing evidence. Known worker-isolation gaps remain
  disclosed under the accepted policy; this does not waive required
  functional cases. Record any further capability needing a design change
  and return it for a concrete decision rather than weakening parity.
- [ ] Commit: `test: record portable skills pipeline reference runs`.

## Completion boundary

The slice is complete when the published KB and installable plugin,
current-session contract flow, all five outcomes, reproducible selection,
supported research, portable skill build, static/judged verification,
generated-skill runtime evidence, conflict rerouting and scoped review
have the evidence above in both
harnesses under `best-effort-v1`, with Forge README and per-run report disclosures.
Functional parity does not certify worker containment. Platform controls
remain named dependencies, never verified
by the forge. Automated snapshot sync and the other builders remain
later sub-projects.

Implementation order is T1→T2→T3→T4→T5→T6→T7→T8→T9→T10→T11→T12→
T13→T14. T2 answers worker feasibility before substantial core work;
T3 settles distribution before dependency pins. T4-T10 prove the primary
workflow offline, T11 proves it live, and T12 completes the remaining
conversations before distribution. Every task consumes the interfaces
listed above; no intermediate milestone is the completed slice.

## Planning evidence and self-review

The scope comes from the parent design's rules, intake, research,
builders, verification, security, testing and sub-project sections.
Selection uses `docs/overview.md`; extraction uses all skills layers,
`docs/guide/security.md` and `docs/guide/outside-gates.md`, with the source
policy supplied above. Re-fetch extraction sources during implementation;
this plan does not claim that every prospective rule is already verified.

Official pages fetched on 2026-10-07 establish the packaging/restriction
constraints used here: [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
describes root `plugin.json` and `skills/`;
[Claude plugin reference](https://code.claude.com/docs/en/plugins-reference)
describes the Claude manifest and component layout;
[Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
describes inherited runtime policies; and
[Claude subagents](https://code.claude.com/docs/en/sub-agents) describes
ignored plugin-agent permission fields. T2 tests restrictions and T13
rechecks installation at the actual execution versions.

The additional process candidate comes from the documented
[non-interactive Codex entry point](https://learn.chatgpt.com/docs/non-interactive-mode),
whose configuration isolation flags do not establish the whole boundary.
[Permission-profile documentation](https://learn.chatgpt.com/docs/permissions)
describes filesystem denials and legacy sandbox precedence. T2 tests the
effective boundary and automatic discovery rather than assuming it.

The distribution assessment must account for jsonschema 4.26's declared
`referencing` and `rpds-py` dependencies
([versioned package metadata](https://raw.githubusercontent.com/python-jsonschema/jsonschema/v4.26.0/pyproject.toml)).
The latter is Rust-backed and its source installation needs a Rust
toolchain ([rpds-py package](https://pypi.org/project/rpds-py/)). This adds
platform-specific distribution work; existing upstream wheels can avoid
building each target ourselves. These sources were fetched on 2026-10-07;
T3 checks the versions it actually proposes to pin.

Self-review coverage: bootstrap T1; restricted fresh workers T2/T11;
distribution choice T3; rule/schema authority T4/T5; all-concept selection
and outside prerequisites T6; identifiers/confirmation/README T7;
both research passes/source support/acceptance T8; accepted-only portable
builds T9; applicability/results/hashes/links/scope T10; primary live
workflow and generated-skill runtime producer T11;
overrides/drift/conflicts/fixes/review choices T12;
migration T5/T13; license T1/T13; clean packaging T13;
broad routing, reference ideas, adversarial cases and self-check T14.
Detailed non-skills rules and builders
are explicit exclusions.
