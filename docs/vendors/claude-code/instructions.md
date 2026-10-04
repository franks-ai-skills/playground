# Instructions and memory

Claude Code has two persistent memory systems, and both load at the start of every conversation: CLAUDE.md files, which you write, and auto memory, which Claude writes. They give Claude project conventions and learned facts across sessions. Both act as context, not enforced configuration; to block an action regardless of what Claude decides, the docs point to `PreToolUse` [hooks](hooks.md) ([memory](https://code.claude.com/docs/en/memory)).

## Locations and scopes

### CLAUDE.md files

Load order, broadest first ([memory](https://code.claude.com/docs/en/memory)):

| Scope | Location |
| :- | :- |
| Managed policy | macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`; Linux/WSL `/etc/claude-code/CLAUDE.md`; Windows `C:\Program Files\ClaudeCode\CLAUDE.md` |
| User | `~/.claude/CLAUDE.md` |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` |
| Local | `./CLAUDE.local.md` (personal; add it to `.gitignore`) |

- Files are concatenated, never overridden. At launch Claude Code loads CLAUDE.md and CLAUDE.local.md from the working directory and every ancestor directory, ordered from the filesystem root down to the cwd, so closer files are read last. Within one directory, CLAUDE.local.md is appended after CLAUDE.md ([memory](https://code.claude.com/docs/en/memory)).
- CLAUDE.md files in subdirectories load on demand, when Claude reads files there ([memory](https://code.claude.com/docs/en/memory)).
- The managed-only `claudeMd` settings key puts CLAUDE.md content directly into managed settings, e.g. `{"claudeMd": "Always run \`make lint\` before committing."}`. It is ignored in user, project, and local settings ([memory](https://code.claude.com/docs/en/memory)).
- CLAUDE.md files in `--add-dir` directories are not loaded by default. `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` loads their CLAUDE.md, `.claude/CLAUDE.md`, `.claude/rules/*.md`, and CLAUDE.local.md ([memory](https://code.claude.com/docs/en/memory)).

### `.claude/rules/`

- Every `.md` file in `.claude/rules/` is discovered recursively. A rule without `paths` loads at launch with the same priority as `.claude/CLAUDE.md` ([memory](https://code.claude.com/docs/en/memory)).
- User-level rules in `~/.claude/rules/` load before project rules ([memory](https://code.claude.com/docs/en/memory)).
- Symlinks are supported. A symlink target outside the project is treated like an external import ([memory](https://code.claude.com/docs/en/memory)).
- Project rules are skipped when `--setting-sources` excludes `project` ([memory](https://code.claude.com/docs/en/memory)).

### AGENTS.md

- Default: Claude reads AGENTS.md (and `.claude/AGENTS.md`) from the cwd and its ancestors only if no CLAUDE.md, `.claude/CLAUDE.md`, or CLAUDE.local.md exists in the cwd or above it. `~/.claude/CLAUDE.md`, the managed CLAUDE.md, and `.claude/rules/` do not count for this check ([memory](https://code.claude.com/docs/en/memory)).
- A subdirectory's AGENTS.md loads when Claude reads a file there, if that subdirectory has no CLAUDE.md files of its own ([memory](https://code.claude.com/docs/en/memory)).
- Never read: `AGENTS.local.md`, `AGENTS.override.md`, and anything under `.agents/` ([memory](https://code.claude.com/docs/en/memory)).
- The behavior is controlled by the "Project instructions" setting of the built-in `agents-md` plugin (see [Format](#format)). Disabling that plugin turns AGENTS.md support off ([memory](https://code.claude.com/docs/en/memory)).

### Auto memory

- Storage: `~/.claude/projects/<project>/memory/`, with a `MEMORY.md` index plus one topic file per memory. `<project>` is derived from the git repo, so worktrees share one directory. Memory is machine-local ([memory](https://code.claude.com/docs/en/memory)).
- `autoMemoryDirectory` relocates the store (an absolute path or `~/`). It is honored from any scope, subject to workspace trust in project files. `CLAUDE_CODE_PROJECT_DIR_NAME` (v2.1.234+) overrides the `<project>` name ([memory](https://code.claude.com/docs/en/memory)).
- Auto memory is on by default in local sessions and off by default in self-hosted environments ([memory](https://code.claude.com/docs/en/memory)).
- Subagents have a separate per-agent memory via the `memory` frontmatter field; see [subagents.md](subagents.md).

## Format

### CLAUDE.md

- Plain Markdown. CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt. For system-prompt-level instructions, use `--append-system-prompt` ([memory](https://code.claude.com/docs/en/memory)).
- Block-level HTML comments (`<!-- ... -->`) are stripped before injection. Comments inside code blocks are kept ([memory](https://code.claude.com/docs/en/memory)).

### Imports (`@path`)

- `@path/to/file` accepts relative paths (resolved against the importing file) and absolute paths, including `@~/...`. Imports recurse up to 4 hops deep ([memory](https://code.claude.com/docs/en/memory)).
- Escape spaces with a backslash. A quoted path is never imported. Imports inside code spans and fences are ignored, so wrapping a path in backticks keeps it literal ([memory](https://code.claude.com/docs/en/memory)).
- An import in a project file that resolves outside the working directory is "external". The first time, Claude Code shows a one-time approval dialog; if you decline, those imports stay disabled. Imports from user-scope files load without the dialog, except in Cowork ([memory](https://code.claude.com/docs/en/memory)).

### Rule files (`.claude/rules/*.md`)

| Frontmatter field | Meaning | Default |
| :- | :- | :- |
| `paths` | YAML list or comma-separated string of globs, with brace expansion. The rule loads only when Claude uses Read, Write, or Edit on a matching file | Absent: the rule loads at launch |

- `paths` is the only frontmatter field read; any other field is ignored ([memory](https://code.claude.com/docs/en/memory)).
- Brace expansion is capped at 1,000 expanded patterns or 4 MiB per rule ([memory](https://code.claude.com/docs/en/memory)).

### "Project instructions" setting (AGENTS.md handling)

Set in `/config`. Stored as `pluginConfigs["agents-md@builtin"].options.instructionFiles`. Honored in user, `--settings`, and managed settings; ignored in project and local settings ([memory](https://code.claude.com/docs/en/memory)).

| Value | Effect |
| :- | :- |
| `claude-md-or-agents-md` (default) | CLAUDE.md files, or AGENTS.md when no CLAUDE.md exists |
| `claude-md-and-agents-md` | Both; per directory, CLAUDE.md first, then AGENTS.md, deduplicated |
| `claude-md` | CLAUDE.md only |
| `managed-only` | Managed CLAUDE.md and auto memory only |

Source: [memory](https://code.claude.com/docs/en/memory)

### Auto memory files

- Claude saves four types of notes, recorded as frontmatter `type`: `user`, `feedback`, `project`, and `reference`. Claude writes them itself and skips anything derivable from the code ([memory](https://code.claude.com/docs/en/memory)).
- Since v2.1.214, a `modified` timestamp is added to the frontmatter of memory files that have frontmatter ([memory](https://code.claude.com/docs/en/memory)).

### Related settings and environment variables

| Key / variable | Effect |
| :- | :- |
| `claudeMdExcludes` | Glob patterns matched against absolute paths; excludes CLAUDE.md files. Works from any settings layer; arrays merge across layers. The managed CLAUDE.md cannot be excluded ([memory](https://code.claude.com/docs/en/memory)) |
| `claudeMd` | Managed-only inline CLAUDE.md content ([memory](https://code.claude.com/docs/en/memory)) |
| `autoMemoryEnabled` | Toggle auto memory; `false` in project settings turns it off per project ([memory](https://code.claude.com/docs/en/memory)) |
| `autoMemoryDirectory` | Relocate the auto memory store ([memory](https://code.claude.com/docs/en/memory)) |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | `1` turns auto memory off; `0` forces it on ([env vars](https://code.claude.com/docs/en/env-vars)) |
| `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` | Prevents loading any CLAUDE.md, including auto memory files ([env vars](https://code.claude.com/docs/en/env-vars)) |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` | Load instruction files from `--add-dir` directories ([memory](https://code.claude.com/docs/en/memory)) |
| `CLAUDE_CODE_PROJECT_DIR_NAME` | Override the `<project>` directory name for auto memory (v2.1.234+) ([memory](https://code.claude.com/docs/en/memory)) |
| `CLAUDE_CODE_NEW_INIT=1` | Interactive multi-phase `/init` ([memory](https://code.claude.com/docs/en/memory)) |
| `--bare` (sets `CLAUDE_CODE_SIMPLE=1`) | Skips CLAUDE.md auto-discovery and auto memory ([env vars](https://code.claude.com/docs/en/env-vars)) |
| `--safe-mode` | Disables CLAUDE.md, skills, plugins, hooks, MCP, and more for troubleshooting (local CLI help) |

## Loading and invocation

- At launch: ancestor CLAUDE.md and CLAUDE.local.md files, their `@` imports, unscoped rules, user rules, and the first 200 lines or 25KB of `MEMORY.md` ([memory](https://code.claude.com/docs/en/memory)).
- On demand: nested CLAUDE.md files and subdirectory AGENTS.md files when Claude reads files in that directory; path-scoped rules when Claude uses Read, Write, or Edit on a matching file; auto memory topic files when Claude reads them ([memory](https://code.claude.com/docs/en/memory)).
- `@path` imports do not reduce context cost, because imported files also load at launch ([memory](https://code.claude.com/docs/en/memory)).
- After `/compact`, the project-root CLAUDE.md is re-read from disk and re-injected. Nested CLAUDE.md files and path-scoped rules reload when matching files are read again ([memory](https://code.claude.com/docs/en/memory)).
- Auto memory is not loaded into subagents, except forks ([memory](https://code.claude.com/docs/en/memory)).
- Inference (from the research notes): everything loaded at launch is an always-on context cost. Path-scoped rules, nested CLAUDE.md files, and memory topic files cost context only when triggered. [Skills](skills.md) are the on-demand alternative for procedures.

### Commands and tools

- `/memory` lists the CLAUDE.md, CLAUDE.local.md, and memory locations at user and project scope, opens them in an editor (creating missing files), toggles auto memory (writes `autoMemoryEnabled` to `~/.claude/settings.json`), and opens the auto memory folder ([memory](https://code.claude.com/docs/en/memory); [commands](https://code.claude.com/docs/en/commands)).
- `/init` generates a CLAUDE.md or suggests improvements to an existing one. It incorporates `.cursor/rules`, `.cursorrules`, and `.github/copilot-instructions.md` ([memory](https://code.claude.com/docs/en/memory)).
- With `CLAUDE_CODE_NEW_INIT=1`, `/init` runs an interactive multi-phase flow that can create CLAUDE.md files, skills, and hooks. It also reads AGENTS.md, `.devin/rules/`, `.windsurf/rules/`, and `.clinerules` ([memory](https://code.claude.com/docs/en/memory)).
- `/import` (v2.1.213+) imports configuration from Codex, Gemini CLI, or Cursor ([commands](https://code.claude.com/docs/en/commands)).
- Debugging: `/context` lists "Memory files"; `/doctor prompt-audit` (v2.1.283+) audits instruction files; the `InstructionsLoaded` hook logs which files loaded and why ([memory](https://code.claude.com/docs/en/memory)).

## Example

`.claude/rules/api.md`, loaded only when Claude reads or edits a matching file ([memory](https://code.claude.com/docs/en/memory)):

```markdown
---
paths:
  - "src/api/**/*.ts"
---
- All API endpoints must include input validation
```

## Limits and gotchas

- Size: the docs recommend under 200 lines per CLAUDE.md. A file up to 4 MiB loads in full; a larger file is skipped. A warning appears at startup and in `/status` when a file is over the recommended length, or when several files together pass a combined limit ([memory](https://code.claude.com/docs/en/memory)).
- Auto memory index: only the first 200 lines or 25KB of `MEMORY.md` load. A write that pushes the index over the limit returns an error telling Claude to rewrite it ([memory](https://code.claude.com/docs/en/memory)).
- Path-scoped rules: triggering on Write and Edit (not only Read) was fixed in v2.1.288 ([memory](https://code.claude.com/docs/en/memory); [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)). `.claude/rules/` was added in v2.0.64 ([changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- AGENTS.md version history: native support arrived in v2.1.277. v2.1.281 extended it to Bedrock, Vertex, Foundry, gateways, and sessions with telemetry off ([memory](https://code.claude.com/docs/en/memory); [changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- An AGENTS.md read through the "Project instructions" setting does not fire `InstructionsLoaded` hooks ([memory](https://code.claude.com/docs/en/memory)).
- The older workaround, a CLAUDE.md containing `@AGENTS.md` or a symlink `ln -s AGENTS.md CLAUDE.md`, still works and never double-loads. A `SessionStart` hook that prints AGENTS.md should be removed, because it now adds a duplicate ([memory](https://code.claude.com/docs/en/memory)).
- Inference (from the research notes): a repo can keep a single AGENTS.md and no CLAUDE.md. Adding a personal CLAUDE.local.md then silently disables AGENTS.md loading unless "Project instructions" is set to `claude-md-and-agents-md`.
- The "Project instructions" setting cannot be set from project or local settings, so a repository cannot opt itself into `claude-md-and-agents-md` ([memory](https://code.claude.com/docs/en/memory)).
- Gap (research notes): the docs do not publish the "combined limit" across instruction files that triggers the startup warning.
- Gap (research notes): the exact on-disk name derivation for `<project>` (path sanitization) was not verified beyond "derived from the git repository".

## Sources

- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/env-vars
- https://code.claude.com/docs/en/commands
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- Local CLI help: `claude --help` (v2.1.289)
