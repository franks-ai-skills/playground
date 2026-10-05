# Instructions

Instruction files are markdown files whose content OpenCode injects into the system prompt. They give the model project rules such as build commands, conventions, and architecture notes. OpenCode reads `AGENTS.md` natively, falls back to Claude Code's `CLAUDE.md`, and accepts extra files, globs, and URLs through the `instructions` config key.

## Locations and scopes

| Scope | Files, in lookup order | Applies to |
| --- | --- | --- |
| Project | `AGENTS.md`, then `CLAUDE.md`, then `CONTEXT.md` (deprecated). Searched by walking up from the cwd to the git worktree root. | The directory that holds the file and its subdirectories ([Rules](https://opencode.ai/docs/rules/)). |
| Global | `~/.config/opencode/AGENTS.md`, then `~/.claude/CLAUDE.md` as fallback. | All sessions ([Rules](https://opencode.ai/docs/rules/)). |
| Nested (lazy) | `AGENTS.md` / `CLAUDE.md` / `CONTEXT.md` between a file the read tool opens and the project root. | Attached when the read tool opens a file in that subtree ([SRC session/instruction.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts), [SRC tool/read.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/tool/read.ts)). |
| Config | `instructions` array in any config layer: paths, globs, `~/` paths, absolute paths, http(s) URLs. | All sessions that load that config ([Rules](https://opencode.ai/docs/rules/)). |
| MCP | Instructions sent by an MCP server. | Appended to session context since v1.17.10 ([REL v1.17.10](https://github.com/anomalyco/opencode/releases/tag/v1.17.10)). See [mcp.md](mcp.md). |
| References | Entries in the `references` config key that have a `description`. | Injected into agent system context ([References](https://opencode.ai/docs/references/)). See [configuration.md](configuration.md#references). |

### Precedence

Docs: local files found by walking up from the cwd (`AGENTS.md`, `CLAUDE.md`), then the global file, then `~/.claude/CLAUDE.md`. The first match wins in each category ([Rules](https://opencode.ai/docs/rules/)).

Source detail ([SRC session/instruction.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts)):

1. Project filenames are tried in the order `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`.
2. For the first filename that matches anywhere, all matches of that filename found walking up from the cwd to the worktree are added. Other filenames are not used in that scope.
3. Global scope: `~/.config/opencode/AGENTS.md` wins; `~/.claude/CLAUDE.md` is used only if it does not exist ([Rules](https://opencode.ai/docs/rules/)).

### Claude Code compatibility switches

| Env var | Effect |
| --- | --- |
| `OPENCODE_DISABLE_CLAUDE_CODE=1` | Disables all `.claude` support. |
| `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT=1` | Opts out of the Claude Code prompt files (`CLAUDE.md` fallback). The docs list the variable without a separate description; the mapping follows from its name. |
| `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1` | Opts out of Claude Code skills (`~/.claude/skills/`, see [skills.md](skills.md)). Same caveat as above. |
| `OPENCODE_DISABLE_PROJECT_CONFIG` | Skips the project `AGENTS.md` lookup, together with project `opencode.json` and project `.opencode` dirs ([SRC config/paths.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/paths.ts), [SRC session/instruction.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts)). |

Source for the first three rows: [Rules](https://opencode.ai/docs/rules/).

## Format

Instruction files are plain markdown. There is no frontmatter.

Each loaded file is injected into the system prompt as `Instructions from: <path>\n<content>` ([SRC session/instruction.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts)).

OpenCode does not parse `@file` references inside `AGENTS.md`. To pull in other files, list them in `instructions`, or write `AGENTS.md` text that tells the model to read the referenced files when needed ([Rules](https://opencode.ai/docs/rules/)).

### `instructions` config key

An array of strings. Entries are combined with the `AGENTS.md` files ([Rules](https://opencode.ai/docs/rules/)).

| Entry type | Example | Resolution (source) |
| --- | --- | --- |
| Relative path or glob | `"CONTRIBUTING.md"`, `".cursor/rules/*.md"`, `"packages/*/AGENTS.md"` | Glob-searched upward from the cwd to the worktree. |
| `~/` path | `"~/rules/style.md"` | Globbed directly. |
| Absolute path | `"/etc/rules/*.md"` | Globbed directly. |
| URL | `"https://raw.githubusercontent.com/my-org/rules/main/style.md"` | Fetched with a 5 s timeout on every system-prompt build. |

Resolution source: [SRC session/instruction.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts). Timeout: [Rules](https://opencode.ai/docs/rules/).

Across config layers, `instructions` arrays are concatenated and deduplicated ([SRC config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts)). See [configuration.md](configuration.md#merge-semantics).

## Loading and invocation

- **System prompt build:** project and global instruction files and all `instructions` entries are added each time the system prompt is built. URL entries are fetched again on every build ([SRC session/instruction.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts)).
- **Lazy nested files:** when the read tool reads a file, OpenCode walks upward from that file toward the project root. It attaches every `AGENTS.md`/`CLAUDE.md`/`CONTEXT.md` it finds that is not already in the system prompt. Each file is attached once per message ([SRC session/instruction.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts), [SRC tool/read.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/tool/read.ts)).
- **Context cost:** the full content of every loaded file is in the system prompt. Nested files cost context only after a read in their subtree.

### `/init`

`/init` scans the repo and may ask targeted questions. It writes `AGENTS.md`, or improves an existing one in place, with build/lint/test commands, architecture, conventions, gotchas, and pointers to existing Cursor/Copilot rules ([Rules](https://opencode.ai/docs/rules/)). In source it is a built-in command described as "guided AGENTS.md setup" ([SRC command/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/command/index.ts)). See [commands.md](commands.md).

## Example

```json
{ "$schema": "https://opencode.ai/config.json",
  "instructions": ["docs/guidelines.md", "packages/*/AGENTS.md", "https://raw.githubusercontent.com/my-org/rules/main/style.md"] }
```

## Limits and gotchas

- **`AGENTS.md` and `CLAUDE.md` are not mixed within one scope (inference from the notes).** If any project `AGENTS.md` exists, no project `CLAUDE.md` is loaded.
- **Monorepos load every ancestor copy (inference from the notes).** Starting in a package that has its own `AGENTS.md` loads both the package file and the root file, because every ancestor copy of the winning filename up to the worktree is included.
- **`CONTEXT.md` is deprecated** in source; it is still the third fallback.
- **No `@file` imports** inside `AGENTS.md`.
- **URL instructions** are re-fetched on every system-prompt build and time out after 5 s.
- **MCP server instructions** have been appended to session context since v1.17.10.
- **Gap:** none of the sources state a size limit for instruction files.

## Sources

- https://opencode.ai/docs/rules/
- https://opencode.ai/docs/references/
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/tool/read.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/paths.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/config/config.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/command/index.ts
- https://github.com/anomalyco/opencode/releases/tag/v1.17.10
