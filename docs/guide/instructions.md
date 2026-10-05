# Instructions

Instruction files are plain Markdown files that the harness reads when a session starts and adds to the model's context as standing guidance: build and test commands, conventions, constraints, and what "done" means. They let every session start with the same personal, project and organization guidance without the user repeating it. They are context, not enforcement: to block an action, use [permissions and sandbox](permissions-and-sandbox.md) or [hooks](hooks.md).

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Native file name | `CLAUDE.md`; `AGENTS.md` only as fallback ([CC](../vendors/claude-code/instructions.md#agentsmd)) | `AGENTS.md` ([Codex](../vendors/codex/instructions.md#locations-and-scopes)) | `AGENTS.md`, then `CLAUDE.md`, then deprecated `CONTEXT.md` ([OC](../vendors/opencode/instructions.md#precedence)) |
| Managed (admin) scope | Managed `CLAUDE.md` in a system directory, or the managed-only `claudeMd` key ([CC](../vendors/claude-code/instructions.md#claudemd-files)) | `additional_developer_instructions` in `requirements.toml`, max 10,000 estimated tokens ([Codex](../vendors/codex/instructions.md#other-instruction-sources)) | No dedicated mechanism ([OC](../vendors/opencode/instructions.md#locations-and-scopes)) |
| User file | `~/.claude/CLAUDE.md`; user rules in `~/.claude/rules/` ([CC](../vendors/claude-code/instructions.md#claudemd-files)) | `~/.codex/AGENTS.md` (or `$CODEX_HOME`); `AGENTS.override.md` there takes priority ([Codex](../vendors/codex/instructions.md#locations-and-scopes)) | `~/.config/opencode/AGENTS.md`; `~/.claude/CLAUDE.md` only if that file is missing ([OC](../vendors/opencode/instructions.md#precedence)) |
| Project files | `./CLAUDE.md` or `./.claude/CLAUDE.md` in the cwd and every ancestor up to the filesystem root ([CC](../vendors/claude-code/instructions.md#claudemd-files)) | One file per directory, from the project root (nearest `.git`, configurable) down to the cwd ([Codex](../vendors/codex/instructions.md#locations-and-scopes)) | Every copy of the winning file name from the cwd up to the git worktree root ([OC](../vendors/opencode/instructions.md#precedence)) |
| Personal project file | `CLAUDE.local.md` ([CC](../vendors/claude-code/instructions.md#claudemd-files)) | None | None |
| Files below the cwd | Loaded when Claude reads files in that directory ([CC](../vendors/claude-code/instructions.md#loading-and-invocation)) | Never read ([Codex](../vendors/codex/instructions.md#locations-and-scopes)) | Attached when the read tool opens a file in that subtree ([OC](../vendors/opencode/instructions.md#loading-and-invocation)) |
| Combination | Concatenated, never overridden; filesystem root first, cwd last ([CC](../vendors/claude-code/instructions.md#claudemd-files)) | Concatenated; global first, then project root to cwd; later text takes precedence ([Codex](../vendors/codex/instructions.md#loading-and-invocation)) | Each file injected as `Instructions from: <path>` ([OC](../vendors/opencode/instructions.md#format)) |
| Placement in context | User message after the system prompt ([CC](../vendors/claude-code/instructions.md#claudemd)) | First-turn instructions ([Codex](../vendors/codex/instructions.md#loading-and-invocation)) | System prompt ([OC](../vendors/opencode/instructions.md#format)) |
| Includes | `@path` imports, up to 4 hops; external imports need a one-time approval ([CC](../vendors/claude-code/instructions.md#imports-path)) | None documented | None; `@file` is not parsed ([OC](../vendors/opencode/instructions.md#format)) |
| Path-scoped files | `.claude/rules/*.md` with `paths` globs ([CC](../vendors/claude-code/instructions.md#rule-files-clauderulesmd)) | None | None |
| Instructions from config | `--append-system-prompt`; managed `claudeMd` ([CC](../vendors/claude-code/instructions.md#claudemd)) | `developer_instructions` adds; `model_instructions_file` replaces the built-in instructions ([Codex](../vendors/codex/instructions.md#other-instruction-sources)) | `instructions` array of paths, globs and URLs ([OC](../vendors/opencode/instructions.md#instructions-config-key)) |
| Size limit | Recommended under 200 lines per file; files over 4 MiB skipped; unpublished combined warning threshold ([CC](../vendors/claude-code/instructions.md#limits-and-gotchas)) | `project_doc_max_bytes`, default 32 KiB; docs disagree on per file vs combined ([Codex](../vendors/codex/instructions.md#limits-and-gotchas)) | None stated ([OC](../vendors/opencode/instructions.md#limits-and-gotchas)) |
| Reload | At launch; root `CLAUDE.md` re-read after `/compact` ([CC](../vendors/claude-code/instructions.md#loading-and-invocation)) | Once per run ([Codex](../vendors/codex/instructions.md#loading-and-invocation)) | On every system-prompt build; URLs re-fetched ([OC](../vendors/opencode/instructions.md#loading-and-invocation)) |
| Inspect what loaded | `/context`, `/memory`, `/doctor prompt-audit`, `InstructionsLoaded` hook ([CC](../vendors/claude-code/instructions.md#commands-and-tools)) | Ask the agent; TUI and session logs ([Codex](../vendors/codex/instructions.md#tools)) | Not recorded |

All three scaffold a file with `/init`.

## Generalized model

- **Instruction file.** A Markdown file with no required structure. The harness adds its full text to the context. It carries guidance, not enforced policy.
- **Scopes**, broadest first: **managed** (set by an administrator through a system file or policy key; users cannot remove it), **user** (one file in the user's harness home), **project chain** (files in the directories between an anchor and the working directory; the anchor is the project root or the filesystem root; each directory contributes at most one resolved file).
- **File name resolution.** Each scope has an ordered list of candidate names. The harness's native name comes first; another harness's name may be accepted as a fallback.
- **Assembly.** Files are concatenated, broadest first and the working directory last. Nothing is overridden. Later text is closer to the work and is meant to win on conflict.
- **Configured instructions.** Configuration can add instruction text next to the discovered files. This is the channel for managed instructions and for text that should not live in the repository.
- **Budget.** The harness caps how much instruction text it loads. Text over the cap is skipped or truncated; the closest files come last and are the ones at risk.
- **Lifecycle.** Discovery runs at session start. Edits take effect in the next session; some harnesses re-read parts earlier.

| Generalized term | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Instruction file | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` |
| Accepted fallback name | `AGENTS.md` (only if no `CLAUDE.md` on the path) | Names in `project_doc_fallback_filenames` | `CLAUDE.md`, `CONTEXT.md` |
| Managed instructions | Managed `CLAUDE.md`, `claudeMd` | `additional_developer_instructions` | — |
| User instruction file | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` | `~/.config/opencode/AGENTS.md` |
| Project chain anchor | Filesystem root | Project root (`project_root_markers`, default `.git`) | Git worktree root |
| File name resolution setting | "Project instructions" (`instructionFiles`) | `project_doc_fallback_filenames` | Fixed order |
| Configured instructions | `--append-system-prompt` | `developer_instructions` | `instructions` |
| Budget | 200-line recommendation, 4 MiB skip | `project_doc_max_bytes` (32 KiB) | — |

## When to use it and when not

An instruction file is the right tool for short, stable facts that every session needs and that the agent cannot derive from the code.

| Use it when | Why |
| --- | --- |
| The agent needs build, test and lint commands with flags | Loaded every session; both vendors list these items first ([Claude Code best practices](https://code.claude.com/docs/en/best-practices), [Codex best practices](https://learn.chatgpt.com/codex/learn/best-practices)) |
| A convention differs from the language or framework default | The agent cannot infer it from the code |
| There are gotchas, boundaries ("never touch X"), or a definition of "done" with a check the agent can run | "Without a check it can run, 'looks done' is the only signal available" ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)) |
| Knowledge the model lacks must always apply (for example framework APIs released after training) | A compressed 8 KB docs index in `AGENTS.md` scored 100% vs at most 79% for a skill (53% baseline without docs) ([Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)) |
| Another mechanism needs a trigger, for example "use the `reviewer` agent after edits" | The instruction file carries the trigger; the mechanism carries the work |

| Do not use it when | Use instead | Cost or risk of using an instruction file |
| --- | --- | --- |
| The content is a multi-step procedure or matters only for some tasks | [Skills](skills.md) | Paid in context every session; "move it to a skill or a path-scoped rule" ([Claude Code memory docs](https://code.claude.com/docs/en/memory)) |
| A rule must hold every time | [Hooks](hooks.md), [permissions and sandbox](permissions-and-sandbox.md) | Instruction files are "context, not enforced configuration"; the model can skip them |
| A tool can check it (formatting, style) | Linter or formatter, run by a hook or CI | "Never send an LLM to do a linter's job" ([HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)) |
| It is long reference material, architecture or specs | Files under `docs/` with a one-line pointer | Bloat lowers adherence to the rules that matter |
| The work should run in its own context | [Subagents](subagents.md) | The main context fills with intermediate output |
| The agent needs access to an external system | [MCP](mcp.md), plus a skill that teaches its use | Text cannot provide tools |
| The preference is personal | User-scope file, or `CLAUDE.local.md` in Claude Code | The project file is shared with the team through version control |
| The note was learned by the agent during work | Agent-written memory as recall only | Memory is machine-local and unreviewed; required rules belong in the reviewed file |

## Approaches

### Single shared `AGENTS.md`

- **What:** one root `AGENTS.md` and no `CLAUDE.md` anywhere on the path.
- **When it fits:** the repository is used with more than one harness and needs no Claude-only text.
- **How:** Codex and OpenCode read the file natively. Claude Code reads it as a fallback only when no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` is on the path; `~/.claude/CLAUDE.md`, the managed file and `.claude/rules/` do not count for that check ([Claude Code memory docs](https://code.claude.com/docs/en/memory)).
- **Trade-off:** no duplication, but one developer's `CLAUDE.local.md` silently turns the fallback off. Only a user or managed setting (`claude-md-and-agents-md`) restores it.

### `AGENTS.md` plus a Claude-specific `CLAUDE.md`

- **What:** `CLAUDE.md` contains `@AGENTS.md` followed by Claude-only text, or is a symlink to `AGENTS.md`.
- **When it fits:** the repository needs Claude-only content, or developers use `CLAUDE.local.md`.
- **How:** Claude Code imports `AGENTS.md` and never double-loads it; Codex reads `AGENTS.md` and ignores `CLAUDE.md`. A symlink blocks Edit and Write through it and checks out as plain text on Windows unless `core.symlinks` is set, so prefer the import if anyone uses Windows. A `CLAUDE.md` that only says in prose "read AGENTS.md" is not equivalent: Claude "sees AGENTS.md only if it decides to open the file" ([Claude Code memory docs](https://code.claude.com/docs/en/memory)).
- **Trade-off:** two files to keep consistent. Imports organize text but save no context, because imported files load at launch.

### Nested files per directory

- **What:** a root file plus files in subdirectories, closest to the edited code.
- **When it fits:** monorepos and packages with their own commands. OpenAI's main repository had 88 `AGENTS.md` files ([agents.md](https://agents.md/)).
- **How:** generalized, files are concatenated broadest first and closer text wins. Claude Code loads subdirectory files when it reads files there; `claudeMdExcludes` skips other teams' files; path-scoped `.claude/rules/*.md` add Claude-only guidance (invalid YAML silently makes a rule unconditional). Codex reads from the project root down to the cwd and never below; "closer files override earlier ones" ([Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)).
- **Trade-off:** in Codex a subdirectory file reaches the agent only when the session starts inside that directory. No study compares nested files with one root file.

### Map plus linked docs

- **What:** a short root file that works as a table of contents into a structured `docs/` directory, read on demand.
- **When it fits:** large projects whose guidance no longer fits a short root file.
- **How:** plain-sentence pointers with a trigger ("Before changing the billing schema, read docs/billing.md") work in every harness. Codex: "reference task-specific markdown files for specialized guidance" ([Codex best practices](https://learn.chatgpt.com/codex/learn/best-practices)).
- **Trade-off:** lazy pointers save budget but depend on the agent deciding to read. Eager loading guarantees visibility and costs budget every session. Put pointers to critical material in the always-loaded file with an explicit trigger.

### Configured and managed instructions

- **What:** instruction text from configuration instead of a discovered file.
- **When it fits:** organization policy that users must not remove, or text that should not live in the repository.
- **How:** Claude Code uses a managed `CLAUDE.md` or the managed-only `claudeMd` key, and `--append-system-prompt` for system-prompt-level text. Codex uses `additional_developer_instructions` in `requirements.toml` and `developer_instructions` in config.
- **Trade-off:** counts toward the same budget and is not visible in the repository.

### Agent-written memory

- **What:** notes the agent writes for itself and reloads later.
- **When it fits:** machine-local recall of preferences and recurring corrections, not rules that must always apply.
- **How:** Claude Code auto memory is on by default; the first 200 lines or 25 KB of `MEMORY.md` load every session; it is not loaded into subagents except forks ([Claude Code memory docs](https://code.claude.com/docs/en/memory)). Codex memories are off by default (`memories = true` under `[features]`) and stored in `~/.codex/memories/` ([Codex memories](https://learn.chatgpt.com/docs/customization/memories.md?surface=app)).
- **Trade-off:** memory is invisible in code review, so team knowledge fragments per developer, and stale or injected notes persist.

## Practices

1. **Include only facts the agent cannot infer.**
   - Why: in the only controlled study, developer-written files raised success by about 4% on average (Claude Code slightly declined) and cost by up to 19%; repository overviews did not shorten the search for relevant files. Agents follow what is written: a tool named in the file was used 1.6 times per instance versus under 0.01 otherwise, so needless requirements create work.
   - How: commands with flags, non-default conventions, gotchas, boundaries ("Always do / Ask first / Never do"), and how to verify "done". Leave out directory trees, dependency lists, tutorials and "write clean code".
   - Evidence: [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices), [Codex best practices](https://learn.chatgpt.com/codex/learn/best-practices)); [Empirical] ([arXiv 2602.11988](https://arxiv.org/html/2602.11988v1)). A second study disagrees on cost: with `AGENTS.md`, median runtime fell 28.64% and output tokens 16.58% on 124 PRs ([arXiv 2601.20404](https://arxiv.org/abs/2601.20404)). The studies differ in benchmark, metric and file provenance.
2. **Keep the files short.**
   - Why: "Longer files consume more context and reduce adherence." Codex stops adding files at its byte cap. Instruction following degrades as instructions accumulate.
   - How: under 200 lines per Claude Code file, the whole chain under 32 KiB. Imports do not help: "imported files also load at launch".
   - Evidence: [Vendor] ([Claude Code memory docs](https://code.claude.com/docs/en/memory), [Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)); [Empirical] the best frontier models reached 68% with 500 instructions, on a non-coding task ([arXiv 2507.11538](https://arxiv.org/abs/2507.11538)); [Practitioner] "< 300 lines is best, and shorter is even better" ([HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)).
3. **Enforce with hooks, permissions and linters, not with instructions.**
   - Why: "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic."
   - How: "If Claude already does something correctly without the instruction, delete it or convert it to a hook." Keep only the human-readable reason in the file. If the file sets commit or PR rules, turn off the competing built-in ones (`includeGitInstructions`, `attribution`) in Claude Code.
   - Evidence: [Vendor] ([Claude Code best practices](https://code.claude.com/docs/en/best-practices), [Claude Code memory docs](https://code.claude.com/docs/en/memory)); [Practitioner] "Never send an LLM to do a linter's job" ([HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)).
4. **Move situational guidance out, and keep a trigger pointer for anything critical.**
   - Why: lazy routes are not guaranteed. In Vercel's eval a skill was not invoked in 56% of cases, while an always-loaded index scored 100%.
   - How: procedures to skills, area guidance to subdirectory files, deep knowledge to linked docs. Leave a one-line pointer that names the condition and the file.
   - Evidence: [Vendor] "only include things that apply broadly" ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)); [Empirical] Vercel's own eval on one framework ([Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)).
5. **Write concrete, verifiable statements.**
   - Why: vague rules are hard to follow and hard to check. Models generalize from a stated reason.
   - How: "Run `npm test` before committing", not "Test your changes". Group under headers, give the reason, say what to do instead of only what not to do.
   - Evidence: [Vendor] ([Claude Code memory docs](https://code.claude.com/docs/en/memory), [Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)). No controlled study covers framing in coding-agent instruction files.
6. **Remove contradictions and blanket emphasis.**
   - Why: "If two instructions contradict each other, Claude may pick one arbitrarily." Contradictory prompts are "more damaging to GPT-5". Current models over-apply shouted rules.
   - How: review the assembled chain together, not file by file. Use emphasis on one or two lines at most. Rewrite ALL-CAPS MUST/NEVER rules from older files in normal language.
   - Evidence: [Vendor] ([Claude Code memory docs](https://code.claude.com/docs/en/memory), [OpenAI cookbook](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide), [Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)).
7. **Prune generated drafts to non-inferable items.**
   - Why: LLM-generated files lowered success by 0.5 to 2% and raised cost by 20 to 23%.
   - How: if you run `/init`, delete overviews, listings and dependency lists before committing; keep commands, gotchas and conventions.
   - Evidence: sources disagree. Both vendors recommend `/init` and then refining [Vendor] ([Claude Code memory docs](https://code.claude.com/docs/en/memory), [Codex best practices](https://learn.chatgpt.com/codex/learn/best-practices)). The ETH study [Empirical] ([arXiv 2602.11988](https://arxiv.org/html/2602.11988v1)) and HumanLayer [Practitioner] ([HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)) advise against generated files. Hard pruning reconciles the positions.
8. **Put each piece of guidance at the right scope.**
   - Why: scopes are concatenated, not overridden. A personal rule in the project file affects everyone, and conflicting rules across scopes resolve arbitrarily.
   - How: team standards in the committed project file, personal preferences in the user file, organization policy in managed instructions, package rules in that package's file.
   - Evidence: [Vendor] ([Claude Code memory docs](https://code.claude.com/docs/en/memory), [Codex best practices](https://learn.chatgpt.com/codex/learn/best-practices), [agents.md](https://agents.md/)).
9. **Grow the file from observed failures and review it like code.**
   - Why: files "evolve like configuration code through frequent, small additions" and rarely shrink.
   - How: add a line when the agent makes the same mistake twice or review catches something it should have known. Review changes in pull requests and prune on a schedule.
   - Evidence: [Vendor] ([Codex best practices](https://learn.chatgpt.com/codex/learn/best-practices), [Claude Code best practices](https://code.claude.com/docs/en/best-practices)); [Empirical] 2,303 files studied ([arXiv 2511.12884](https://arxiv.org/abs/2511.12884)).
10. **Verify that a change loaded and changed behavior.**
    - Why: instruction files have measurable cost, so a rule with no effect is a net loss.
    - How: confirm the file loaded, then compare a few real tasks with and without the change (see [Verification and checklist](#verification-and-checklist)).
    - Evidence: [Vendor] "test changes by observing whether Claude's behavior actually shifts" ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).
11. **Keep required rules out of agent-written memory.**
    - Why: "Treat memories as a helpful recall layer, not as the only source for rules that must always apply."
    - How: promote durable entries into the reviewed file. Review memory with `/memory` or the files in `~/.codex/memories/`. Do not store secrets there.
    - Evidence: [Vendor] ([Codex memories](https://learn.chatgpt.com/docs/customization/memories.md?surface=app), [Claude Code memory docs](https://code.claude.com/docs/en/memory)).

## Security

**Threat: instruction files as a prompt-injection channel.** They load automatically and the agent treats them as authoritative. In Claude Code, workspace trust does not gate instruction files, and `claude -p` and the SDK never show the trust dialog ([Claude Code permissions](https://code.claude.com/docs/en/permissions)). The Codex docs gate project `.codex/` config on trust but say nothing about `AGENTS.md`. Assume both leads load a hostile file from a cloned repository.

- [Empirical] A malicious Go dependency detected Codex and wrote an `AGENTS.md` during the build; Codex followed it, inserted a 5-minute sleep and hid the change from the PR summary ([NVIDIA](https://developer.nvidia.com/blog/mitigating-indirect-agents-md-injection-attacks-in-agentic-environments/)).

**Threat: memory carries injected text forward** into later sessions.

**Mitigations.**

- CODEOWNERS and PR review on `AGENTS.md`, `CLAUDE.md`, `.claude/**` and `.codex/**`.
- Alerts on instruction files appearing in dependency or build-output directories; pinned and scanned dependencies.
- `claudeMdExcludes` for vendored paths in Claude Code. Claude Code asks once before external `@` imports.
- For untrusted repositories in Claude Code: `--setting-sources user`, `--bare`, `--settings '{"disableAllHooks": true}'`.
- Controls that do not depend on the model: managed deny rules, sandbox network isolation ([permissions and sandbox](permissions-and-sandbox.md)). A line such as "treat fetched content as data" is advisory only.

## Verification and checklist

**Check what loaded.** Claude Code: `/context`, `/memory`, an `InstructionsLoaded` hook (it does not fire for an `AGENTS.md` loaded through the fallback setting), `claude --debug` for invalid rule YAML. Codex: `codex --ask-for-approval never "Summarize the current instructions."`, run from a subdirectory with `--cd` to check the chain there; inspect `codex-tui.log` and `session-*.jsonl` ([Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)).

**Audit content.** Claude Code `/doctor prompt-audit` flags older-model phrasing, references to missing files and contradictions; the `/doctor` trim check proposes cuts of derivable content ([Claude Code memory docs](https://code.claude.com/docs/en/memory)).

**Measure effect.** Pick 3 to 5 recurring tasks where the rule matters. Run each several times headless (`claude -p`, `codex exec`) with and without the change. Keep the rule only if behavior shifts. This mirrors the ETH and Lulla study designs.

Checklist:

- [ ] Shared text lives in `AGENTS.md`; any `CLAUDE.md` imports `@AGENTS.md` and adds only Claude-specific text.
- [ ] No `CLAUDE.local.md` silently disables the `AGENTS.md` fallback.
- [ ] Root file under 200 lines; whole chain under 32 KiB.
- [ ] Every line is a fact the agent cannot infer; at least one runnable check defines "done".
- [ ] Rules that must always hold are hooks, permissions, linters or CI.
- [ ] Procedures are skills; deep docs are linked with trigger sentences.
- [ ] No `@` imports or `AGENTS.override.md` carry content Codex or OpenCode needs.
- [ ] No contradictions across scopes; emphasis on one line at most.
- [ ] CODEOWNERS covers instruction files.
- [ ] The expected files load in each harness, and recent changes were checked against real tasks.

## Portability

Use `AGENTS.md` as the shared file. Three layouts work in both leads:

| Layout | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| `AGENTS.md` only | Read as fallback | Read | Read |
| `AGENTS.md` plus `CLAUDE.md` with `@AGENTS.md` and Claude-only text | Reads `CLAUDE.md`, imports `AGENTS.md` once | Reads `AGENTS.md` | `AGENTS.md` wins in that scope |
| `AGENTS.md` plus symlink `CLAUDE.md -> AGENTS.md` | Reads through the symlink once | Reads `AGENTS.md` | `AGENTS.md` wins |

Traps:

- **`CLAUDE.local.md` turns off the `AGENTS.md` fallback in Claude Code.** A repository cannot opt into `claude-md-and-agents-md`; the setting is ignored in project and local settings. `.claude/rules/` does not count for the fallback check ([CC](../vendors/claude-code/instructions.md#agentsmd)).
- **Codex reads no file below the cwd.** Put guidance every session needs in the root file. In Claude Code, a subdirectory `AGENTS.md` loads only if that directory has no `CLAUDE.md`.
- **`AGENTS.override.md` is Codex-only.** Claude Code never reads it, `AGENTS.local.md`, or anything under `.agents/`.
- **`@path` imports work only in Claude Code.** Elsewhere the line stays literal text. Use plain-sentence pointers in shared files.
- **Size.** Keep the whole chain under 32 KiB. When the Codex cap is hit, the files nearest the cwd are dropped first, so a bloated global file can suppress subdirectory guidance ([Codex](../vendors/codex/instructions.md#limits-and-gotchas)).
- **HTML comments.** Claude Code strips block-level `<!-- -->` comments; assume the other harnesses pass them to the model.
- **Global files have no shared path.** Keep one text and symlink the others to it, or use `@~/.codex/AGENTS.md` in `~/.claude/CLAUDE.md`. OpenCode falls back to `~/.claude/CLAUDE.md` and would read that `@` line literally, so give it its own file.
- **Naming.** Do not give any other Markdown file the name of an instruction file in another letter case, such as a lower-case variant. On a case-insensitive file system the harnesses load it as an instruction file.

## Dropped from the generalization

| Feature | Vendor | Reason |
| --- | --- | --- |
| Auto memory | Claude Code | Codex `memories` behavior is not described in the vendor pages; no established counterpart |
| Path-scoped rules (`.claude/rules/` with `paths`), `@path` imports, `CLAUDE.local.md`, `claudeMdExcludes` | Claude Code | No Codex equivalent |
| `InstructionsLoaded` hook, `/doctor prompt-audit` | Claude Code | No Codex audit counterpart |
| Loading files below the cwd | Claude Code, OpenCode | Codex never reads below the cwd |
| `AGENTS.override.md`, `project_root_markers` | Codex | Claude Code has no override file and no anchor setting |
| `## Code Review Rules` section, `model_instructions_file`, `compact_prompt` | Codex | No Claude Code counterpart recorded |
| URL and glob instruction sources (`instructions`, `references`) | OpenCode | Neither lead loads instructions from URLs or globs |

## Open questions

- No controlled study isolates file length for coding agents; length guidance rests on vendor advice and a non-coding study.
- The ETH study (cost up about 20%) and Lulla et al. (runtime and output tokens down) disagree on cost; which agents Lulla et al. used is not confirmed.
- No empirical comparison of nested files versus a single root file.
- Claude Code's combined-size threshold is unpublished; Codex docs disagree on whether 32 KiB is per file or combined.
- Undocumented: whether Codex follows a symlinked `AGENTS.md`, and whether it loads `AGENTS.md` in untrusted projects.
- No study measures agent-written memory on task success, or injection success through instruction files in current versions.

## Sources

Local:

- [Claude Code: instructions](../vendors/claude-code/instructions.md), [Codex: instructions](../vendors/codex/instructions.md), [OpenCode: instructions](../vendors/opencode/instructions.md)
- [Research notes: instructions best practices](../research-notes/agent-harness-best-practices/instructions.md)
- [Research notes: Claude Code foundation](../research-notes/agent-harness-configuration/claude-code-foundation.md), [Codex foundation](../research-notes/agent-harness-configuration/codex-foundation.md), [OpenCode](../research-notes/agent-harness-configuration/opencode.md)

External:

- https://code.claude.com/docs/en/best-practices
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/permissions
- https://learn.chatgpt.com/codex/learn/best-practices
- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://learn.chatgpt.com/docs/customization/memories.md?surface=app
- https://agents.md/
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
- https://arxiv.org/html/2602.11988v1
- https://arxiv.org/abs/2601.20404
- https://arxiv.org/abs/2507.11538
- https://arxiv.org/abs/2511.12884
- https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
- https://www.humanlayer.dev/blog/writing-a-good-claude-md
- https://developer.nvidia.com/blog/mitigating-indirect-agents-md-injection-attacks-in-agentic-environments/
