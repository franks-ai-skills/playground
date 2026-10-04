# Instructions (AGENTS.md)

Codex reads `AGENTS.md` files before it does any work. A global file sets personal defaults and project files add repository- and directory-specific guidance, so each task starts with the same expectations in any repository ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md)). Codex builds one instruction chain per run and places it in the first turn of the session.

## Locations and scopes

| Scope | Where Codex looks | Files checked, in order | Files used |
|---|---|---|---|
| Global | Codex home: `~/.codex`, or `$CODEX_HOME` if set | `AGENTS.override.md`, then `AGENTS.md` | The first non-empty file only |
| Project | Every directory from the project root down to the current working directory (cwd) | `AGENTS.override.md`, then `AGENTS.md`, then each name in `project_doc_fallback_filenames` | At most one file per directory |

Source for the table: [AGENTS guide](https://developers.openai.com/codex/guides/agents-md).

- **Project root.** By default the project root is the nearest directory that contains `.git` (typically the Git root). `project_root_markers` changes this, for example `[".git", ".hg", ".sl"]`. `project_root_markers = []` skips the parent search and treats the cwd as the root ([Advanced config](https://developers.openai.com/codex/config-advanced)). If Codex cannot find a project root, it checks only the cwd ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md)).
- **Search end.** Codex stops searching at the cwd. Directories below the cwd are not read ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md)).
- **Override files.** An `AGENTS.md` in the same directory as an `AGENTS.override.md` is ignored ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md)). At global scope, `AGENTS.override.md` can temporarily replace `~/.codex/AGENTS.md`.
- **Fallback filenames.** Names in `project_doc_fallback_filenames` are tried when `AGENTS.md` is missing at a directory level. Names not on the list are ignored ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md)).
- **Different home.** Setting `CODEX_HOME` points Codex at a different home directory, which changes the global `AGENTS.md` and the user config, for example `CODEX_HOME=$(pwd)/.codex codex exec ...` ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md)).

### Other instruction sources

These are not `AGENTS.md` files, but they also add or replace instructions. All are set in `config.toml` (see [configuration.md](configuration.md)) or in `requirements.toml`.

| Key | Where | Effect |
|---|---|---|
| `model_instructions_file` | `config.toml` | Replaces the built-in instructions (not `AGENTS.md`). In a project config, relative paths resolve against the `.codex/` folder that contains the `config.toml` ([Config reference](https://developers.openai.com/codex/config-reference); [Advanced config](https://developers.openai.com/codex/config-advanced)) |
| `developer_instructions` | `config.toml`, custom agent files | Adds developer instructions to the session ([Config reference](https://developers.openai.com/codex/config-reference)). Required in custom agent files, see [subagents.md](subagents.md) |
| `instructions` | `config.toml` | "Reserved for future use; prefer `model_instructions_file` or `AGENTS.md`" ([Config reference](https://developers.openai.com/codex/config-reference)) |
| `compact_prompt`, `experimental_compact_prompt_file` | `config.toml` | Override the history-compaction prompt ([Config reference](https://developers.openai.com/codex/config-reference)) |
| `additional_developer_instructions` | `requirements.toml` (managed) | Adds a separate developer message. Codex rejects values over 10,000 estimated tokens ([Config reference](https://developers.openai.com/codex/config-reference)) |

## Format

`AGENTS.md` is a Markdown file. The notes record no required structure, with one exception: the `## Code Review Rules` section.

### Code Review Rules section

For GitHub code review, Codex reads a `## Code Review Rules` section in the `AGENTS.md` closest to the changed code ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md); [Review GitHub pull requests with Codex](https://learn.chatgpt.com/docs/third-party/github.md)). See [automation.md](automation.md) for `@codex review` and automatic reviews.

### Config keys that control discovery

| Key | Type | Default | Meaning |
|---|---|---|---|
| `project_doc_max_bytes` | number | `32768` (32 KiB) | "Maximum bytes read from `AGENTS.md` when building project instructions" ([Config reference](https://developers.openai.com/codex/config-reference)); default from [Sample config](https://developers.openai.com/codex/config-sample). Per-file or combined: the docs contradict each other, see Limits and gotchas |
| `project_doc_fallback_filenames` | array of strings | `[]` | Extra filenames tried, in order, after `AGENTS.override.md` and `AGENTS.md` ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md); [Sample config](https://developers.openai.com/codex/config-sample)) |
| `project_root_markers` | array of strings | `[".git"]` | Marker files or directories that identify the project root. `[]` makes the cwd the root ([Advanced config](https://developers.openai.com/codex/config-advanced); [Sample config](https://developers.openai.com/codex/config-sample)) |

With `project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]`, the per-directory order becomes `AGENTS.override.md`, `AGENTS.md`, `TEAM_GUIDE.md`, `.agents.md` ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md)).

## Loading and invocation

- **Combination order.** The global file comes first. Project files follow from the project root down to the cwd. Codex concatenates them and joins them with blank lines. Files closer to the cwd appear later in the combined prompt, so their guidance takes precedence over earlier guidance ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md)).
- **Size cap.** Codex skips empty files and stops adding files once the combined size reaches `project_doc_max_bytes`. If you hit the cap, raise the limit or split the instructions across nested directories ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md)).
- **When.** Discovery runs once per run; in the TUI, once per launched session. There is no cache, so restarting Codex picks up changes ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md)).
- **Context placement.** Project guidance goes into the first turn of a session ([Advanced config](https://developers.openai.com/codex/config-advanced)); the sample config describes this as "embed into first-turn instructions" ([Sample config](https://developers.openai.com/codex/config-sample)). Its context cost is the full text of every loaded file, up to the byte cap.
- **Delegation.** `AGENTS.md` instructions can tell Codex to spawn subagents. Current local releases delegate when the user asks directly or when applicable `AGENTS.md` or skill instructions request it ([Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)). See [subagents.md](subagents.md).

### Tools

- `/init` creates an `AGENTS.md` scaffold in the current directory ([CLI reference](https://developers.openai.com/codex/cli/reference)).
- To see which files loaded, run `codex -c log_dir=./.codex-log` and check `./.codex-log/codex-tui.log`, or ask Codex "Show which instruction files are active." ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md)).

## Example

```text
~/.codex/AGENTS.md                              # global (AGENTS.override.md temporarily replaces it)
<repo>/AGENTS.md                                # repository-wide
<repo>/services/payments/AGENTS.override.md     # replaces AGENTS.md in that directory; appended last
```

```toml
# ~/.codex/config.toml
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
project_doc_max_bytes = 65536
```

Running Codex from `<repo>/services/payments` loads `~/.codex/AGENTS.md`, then `<repo>/AGENTS.md`, then `<repo>/services/payments/AGENTS.override.md`. Source: [AGENTS guide](https://developers.openai.com/codex/guides/agents-md).

## Limits and gotchas

- **Contradiction: per-file or combined limit.** Advanced Config describes `project_doc_max_bytes` as "how much to read from each `AGENTS.md` file", which is a per-file limit ([Advanced config](https://developers.openai.com/codex/config-advanced)). The AGENTS guide says the limit applies to the combined size ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md)). The Codex source (`codex-rs`) could not be checked: the GitHub API was rate-limited and the guessed path `codex-rs/core/src/project_doc.rs` returned 404.
- **Gap: truncation behavior.** Whether Codex cuts a file in the middle or drops whole files is not documented beyond "stops adding files".
- **Inference: the nearest files are dropped first.** Concatenation runs root-first, so when the cap is hit, the files nearest the cwd are the ones left out. Large root files therefore push out more specific guidance.
- **Inference: override replaces, it does not add.** Each directory contributes at most one file, so `AGENTS.override.md` replaces that directory's `AGENTS.md`. Across directories, files accumulate.
- **Gap: project trust.** The docs gate project `.codex/` config, hooks and rules on project trust (see [configuration.md](configuration.md)). They say nothing about `AGENTS.md` and trust. Inference: untrusted projects may still load `AGENTS.md`; this is not confirmed.
- `instructions` in `config.toml` is reserved and has no effect yet ([Config reference](https://developers.openai.com/codex/config-reference)).
- Changes need a restart (or a new TUI session) because discovery runs once per run ([AGENTS guide](https://developers.openai.com/codex/guides/agents-md)).

## Sources

- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/codex/config-advanced
- https://developers.openai.com/codex/config-reference
- https://developers.openai.com/codex/config-sample
- https://developers.openai.com/codex/cli/reference
- https://learn.chatgpt.com/docs/third-party/github.md
- https://learn.chatgpt.com/docs/agent-configuration/subagents.md
