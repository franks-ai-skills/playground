# Instructions

Instruction files are plain Markdown files that the harness reads when a session starts and adds to the model's context as standing guidance: build and test commands, conventions, architecture notes, constraints. They let every session start with the same personal, project, and organization guidance without the user repeating it. They are context, not enforcement: to block an action, use [permissions](permissions-and-sandbox.md) or [hooks](hooks.md).

## Comparison

| Dimension | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Native file name | `CLAUDE.md`; `AGENTS.md` only as fallback ([CC](../vendors/claude-code/instructions.md#agentsmd)) | `AGENTS.md` ([Codex](../vendors/codex/instructions.md#locations-and-scopes)) | `AGENTS.md`, then `CLAUDE.md`, then deprecated `CONTEXT.md` ([OC](../vendors/opencode/instructions.md#precedence)) |
| Managed (admin) scope | Managed `CLAUDE.md` in a system directory, or the managed-only `claudeMd` settings key ([CC](../vendors/claude-code/instructions.md#claudemd-files)) | `additional_developer_instructions` in `requirements.toml`, max 10,000 estimated tokens ([Codex](../vendors/codex/instructions.md#other-instruction-sources)) | No dedicated mechanism. Inference: an `instructions` entry in a managed config layer ([OC](../vendors/opencode/instructions.md#locations-and-scopes), [config layers](../vendors/opencode/configuration.md#layers)) |
| User (global) file | `~/.claude/CLAUDE.md`; user rules in `~/.claude/rules/` ([CC](../vendors/claude-code/instructions.md#claudemd-files)) | `~/.codex/AGENTS.md` (or `$CODEX_HOME`); `AGENTS.override.md` there takes priority; first non-empty file only ([Codex](../vendors/codex/instructions.md#locations-and-scopes)) | `~/.config/opencode/AGENTS.md`; `~/.claude/CLAUDE.md` only if that file is missing ([OC](../vendors/opencode/instructions.md#precedence)) |
| Project files | `./CLAUDE.md` or `./.claude/CLAUDE.md` in the cwd and every ancestor up to the filesystem root ([CC](../vendors/claude-code/instructions.md#claudemd-files)) | One file per directory, from the project root (nearest `.git`, configurable via `project_root_markers`) down to the cwd ([Codex](../vendors/codex/instructions.md#locations-and-scopes)) | Every copy of the winning file name from the cwd up to the git worktree root ([OC](../vendors/opencode/instructions.md#precedence)) |
| Personal project file | `CLAUDE.local.md`, appended after `CLAUDE.md` in the same directory ([CC](../vendors/claude-code/instructions.md#claudemd-files)) | None | None |
| Files below the cwd | Loaded on demand when Claude reads files in that directory ([CC](../vendors/claude-code/instructions.md#loading-and-invocation)) | Never read ([Codex](../vendors/codex/instructions.md#locations-and-scopes)) | Attached when the read tool opens a file in that subtree ([OC](../vendors/opencode/instructions.md#loading-and-invocation)) |
| Choice of file name | "Project instructions" setting: `claude-md-or-agents-md` (default), `claude-md-and-agents-md`, `claude-md`, `managed-only`; user, `--settings`, or managed scope only ([CC](../vendors/claude-code/instructions.md#project-instructions-setting-agentsmd-handling)) | Per directory: `AGENTS.override.md`, then `AGENTS.md`, then each name in `project_doc_fallback_filenames` ([Codex](../vendors/codex/instructions.md#config-keys-that-control-discovery)) | Fixed order; the first file name found anywhere in the scope is the only one used in that scope ([OC](../vendors/opencode/instructions.md#precedence)) |
| Combination | Concatenated, never overridden; filesystem root first, cwd last ([CC](../vendors/claude-code/instructions.md#claudemd-files)) | Concatenated with blank lines; global first, then project root to cwd; later text takes precedence ([Codex](../vendors/codex/instructions.md#loading-and-invocation)) | Each file injected as `Instructions from: <path>`; `instructions` entries are added ([OC](../vendors/opencode/instructions.md#format)) |
| Placement in context | A user message after the system prompt ([CC](../vendors/claude-code/instructions.md#claudemd)) | First-turn instructions ([Codex](../vendors/codex/instructions.md#loading-and-invocation)) | System prompt ([OC](../vendors/opencode/instructions.md#format)) |
| Includes | `@path` imports, relative or absolute, up to 4 hops; external imports need a one-time approval ([CC](../vendors/claude-code/instructions.md#imports-path)) | None documented | None; `@file` is not parsed. The `instructions` config key takes paths, globs, and URLs ([OC](../vendors/opencode/instructions.md#instructions-config-key)) |
| Path-scoped files | `.claude/rules/*.md` with `paths` globs; loaded when Read, Write, or Edit touches a match ([CC](../vendors/claude-code/instructions.md#rule-files-clauderulesmd)) | None | None |
| Instructions from config | `--append-system-prompt` (CLI); managed `claudeMd` ([CC](../vendors/claude-code/instructions.md#claudemd)) | `developer_instructions` adds; `model_instructions_file` replaces the built-in instructions ([Codex](../vendors/codex/instructions.md#other-instruction-sources)) | `instructions` array, concatenated and deduplicated across config layers ([OC](../vendors/opencode/instructions.md#instructions-config-key)) |
| Size limit | Recommended under 200 lines per file; files over 4 MiB are skipped; a combined limit triggers a warning, value not published ([CC](../vendors/claude-code/instructions.md#limits-and-gotchas)) | `project_doc_max_bytes`, default 32 KiB; the docs contradict each other on per-file vs combined ([Codex](../vendors/codex/instructions.md#limits-and-gotchas)) | None stated ([OC](../vendors/opencode/instructions.md#limits-and-gotchas)) |
| Reload | At launch; root `CLAUDE.md` is re-read after `/compact` ([CC](../vendors/claude-code/instructions.md#loading-and-invocation)) | Once per run; restart to pick up changes ([Codex](../vendors/codex/instructions.md#loading-and-invocation)) | On every system-prompt build; URLs are re-fetched ([OC](../vendors/opencode/instructions.md#loading-and-invocation)) |
| Scaffolding | `/init` ([CC](../vendors/claude-code/instructions.md#commands-and-tools)) | `/init` ([Codex](../vendors/codex/instructions.md#tools)) | `/init` ([OC](../vendors/opencode/instructions.md#init)) |
| Inspect what loaded | `/context`, `/memory`, `/doctor prompt-audit`, `InstructionsLoaded` hook ([CC](../vendors/claude-code/instructions.md#commands-and-tools)) | `codex -c log_dir=...` and the TUI log, or ask the agent ([Codex](../vendors/codex/instructions.md#tools)) | Not recorded |

## Generalized model

**Instruction file.** A Markdown file with no required structure. The harness adds its full text to the context. It carries guidance, not enforced policy.

**Scopes**, broadest first:

1. **Managed.** Text set by an administrator through a system file or a policy key. Users cannot remove it.
2. **User.** One file in the user's harness home. Applies to every session of that user.
3. **Project chain.** Files in the directories between an anchor directory and the working directory. The anchor is the project root (a marker such as `.git`) or the filesystem root. Each directory contributes at most one resolved file.

**File name resolution.** Each scope has an ordered list of candidate file names. The first candidate that exists in a directory (or, depending on the harness, anywhere in the scope) is used. The harness's native name comes first. A harness may accept another harness's name as a fallback.

**Assembly.** Files are concatenated, broadest scope first and the working directory last. Nothing is overridden. Precedence comes from position: later text is closer to the work and is meant to win when guidance conflicts.

**Configured instructions.** Configuration can add instruction text or files next to the discovered files. This is the channel for managed instructions and for text that should not live in the repository.

**Budget.** The harness caps how much instruction text it loads, by bytes or by a recommended length. Text over the cap is skipped or truncated, and the closest files are the ones at risk because they come last.

**Lifecycle.** Discovery runs at session start. The assembled text enters the context before the first user prompt. Edits take effect in the next session; some harnesses re-read parts earlier.

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
| Scaffolding command | `/init` | `/init` | `/init` |

## Portability

**Use `AGENTS.md` as the shared file.** Codex and OpenCode read it natively. Claude Code reads `AGENTS.md` (and `.claude/AGENTS.md`) from the cwd and its ancestors since v2.1.277, but only when no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` exists in the cwd or above it ([CC](../vendors/claude-code/instructions.md#agentsmd)).

Three layouts work in both leads:

| Layout | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| `AGENTS.md` only | Read as fallback | Read | Read |
| `AGENTS.md` plus `CLAUDE.md` containing `@AGENTS.md` and Claude-only text | Reads `CLAUDE.md`, imports `AGENTS.md`; never double-loads ([CC](../vendors/claude-code/instructions.md#limits-and-gotchas)) | Reads `AGENTS.md`, ignores `CLAUDE.md` | `AGENTS.md` wins; `CLAUDE.md` is not used in that scope |
| `AGENTS.md` plus symlink `CLAUDE.md -> AGENTS.md` | Reads through the symlink; never double-loads | Reads `AGENTS.md` | `AGENTS.md` wins |

Traps:

- **A personal `CLAUDE.local.md` turns off `AGENTS.md` in Claude Code.** It counts as a `CLAUDE.md` for the fallback check. A repository cannot opt into `claude-md-and-agents-md`, because the setting is ignored in project and local settings ([CC](../vendors/claude-code/instructions.md#limits-and-gotchas)).
- **`.claude/rules/` does not count for the fallback check** ([CC](../vendors/claude-code/instructions.md#agentsmd)). Inference: a repository can keep `AGENTS.md` as the shared file and add Claude-only path-scoped rules without losing the fallback.
- **Subdirectory files reach Codex only from inside that directory.** Codex reads from the project root down to the cwd and never below it. Claude Code and OpenCode attach subdirectory files when the agent reads files there ([Codex](../vendors/codex/instructions.md#locations-and-scopes)). In Claude Code, a subdirectory `AGENTS.md` loads only if that subdirectory has no `CLAUDE.md` of its own ([CC](../vendors/claude-code/instructions.md#agentsmd)). Inference: put guidance every session needs in the root file.
- **`AGENTS.override.md` is Codex-only.** Claude Code never reads `AGENTS.override.md`, `AGENTS.local.md`, or anything under `.agents/` ([CC](../vendors/claude-code/instructions.md#agentsmd)). OpenCode does not list it either. Do not put shared content there.
- **`@path` imports work only in Claude Code.** OpenCode does not parse them ([OC](../vendors/opencode/instructions.md#format)); the Codex pages document no import syntax. In those harnesses the line stays literal text. For portable references, write a sentence that tells the agent to read the file when needed, as the OpenCode docs suggest.
- **Size.** Keep the whole chain (global plus all project files) under 32 KiB, the Codex default. The Codex docs disagree on whether the cap is per file or combined; when the combined cap is hit, the files nearest the cwd are dropped first ([Codex](../vendors/codex/instructions.md#limits-and-gotchas)). Claude Code recommends under 200 lines per file.
- **Context placement differs.** The same text arrives as a user message (Claude Code), first-turn instructions (Codex), or system prompt (OpenCode). The pages record no behavioral consequence.
- **HTML comments.** Claude Code strips block-level `<!-- -->` comments before injection ([CC](../vendors/claude-code/instructions.md#claudemd)). The Codex and OpenCode pages do not say; assume the model sees them.
- **Global files have no shared path.** Claude Code reads `~/.claude/CLAUDE.md`, Codex `~/.codex/AGENTS.md`, OpenCode `~/.config/opencode/AGENTS.md` and falls back to `~/.claude/CLAUDE.md`. To keep one source, keep the text in one file and symlink the others to it. Alternative for Claude Code: a `~/.claude/CLAUDE.md` with `@~/.codex/AGENTS.md`; imports from user-scope files load without the approval dialog ([CC](../vendors/claude-code/instructions.md#imports-path)). OpenCode would then read that `@` line literally if it falls back to `~/.claude/CLAUDE.md`, so give OpenCode its own `~/.config/opencode/AGENTS.md`. Gap: the Codex pages do not say whether a symlinked `AGENTS.md` is followed.
- **Naming.** Do not name any other Markdown file `agents.md` or `claude.md`. On a case-insensitive file system the harnesses load it as an instruction file.

## Dropped from the generalization

- **Auto memory** (Claude Code): Claude writes and loads its own notes; Codex has a `memories` feature flag (off) and a `/memories` command, but the pages do not describe their behavior, so no counterpart is established.
- **Path-scoped rules, `.claude/rules/` with `paths`** (Claude Code): Codex has no file that loads when matching files are touched.
- **`@path` imports** (Claude Code): no include syntax in Codex; OpenCode explicitly has none.
- **`CLAUDE.local.md`** (Claude Code): Codex has no personal, per-project instruction file.
- **Loading instruction files below the cwd** (Claude Code, OpenCode): Codex never reads below the cwd.
- **`AGENTS.override.md`** (Codex): Claude Code has no per-directory override file and never reads this one.
- **Configurable project root markers, `project_root_markers`** (Codex): Claude Code walks to the filesystem root and has no anchor setting.
- **`## Code Review Rules` section** (Codex): used by Codex GitHub review; the Claude Code pages record no section with special meaning.
- **Replacing the built-in instructions, `model_instructions_file`** (Codex): the Claude Code pages document only appending (`--append-system-prompt`).
- **Compaction prompt override, `compact_prompt`** (Codex): no Claude Code counterpart recorded.
- **Exclusion globs, `claudeMdExcludes`** (Claude Code): Codex has no list of instruction files to skip.
- **`InstructionsLoaded` hook and `/doctor prompt-audit`** (Claude Code): no Codex counterpart for auditing loaded instruction files.
- **URL and glob instruction sources, `instructions` and `references`** (OpenCode): neither lead loads instructions from URLs or config globs.

## Sources

- [Claude Code: instructions](../vendors/claude-code/instructions.md)
- [Codex: instructions](../vendors/codex/instructions.md)
- [OpenCode: instructions](../vendors/opencode/instructions.md)
- [OpenCode: configuration](../vendors/opencode/configuration.md)
- [Claude Code README](../vendors/claude-code/README.md), [Codex README](../vendors/codex/README.md), [OpenCode README](../vendors/opencode/README.md)
