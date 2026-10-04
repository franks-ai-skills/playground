# Permissions and sandbox

The `permission` config key decides, per tool call, whether OpenCode runs the call (`allow`), prompts the user (`ask`), or refuses it (`deny`). Rules are keyed by tool name and can carry patterns over the call's input, such as a file path, a bash command, or a subagent name. Defaults are permissive: most tools are allowed without a prompt.

**Sandbox:** the notes do not describe any OS-level sandbox in OpenCode (no process, filesystem, or network isolation for tool execution). The containment mechanisms they record are permission rules, the `external_directory` gate for paths outside the working directory, the default `read` deny on `.env` files, plugin hooks that can block calls, and `experimental.policies`. The notes neither confirm nor rule out an OS-level sandbox explicitly; they record none.

## Locations and scopes

| Scope | Where | Precedence |
| --- | --- | --- |
| Global / project config | `permission` key in any config layer ([configuration.md](configuration.md)) | Merged like other config keys; later layers win. |
| Env var | `OPENCODE_PERMISSION` (inline JSON permissions) ([CLI](https://opencode.ai/docs/cli/)) | |
| Per agent | `permission` in an agent's JSON entry or markdown frontmatter ([subagents.md](subagents.md)) | Merged with the global config; agent rules take precedence ([Permissions](https://opencode.ai/docs/permissions/)). |
| Session | "always" answers to a prompt | Approves the suggested patterns for the rest of the session ([Permissions](https://opencode.ai/docs/permissions/)). |
| Auto mode | `--auto` flag or TUI palette toggle | Approves anything that would ask; explicit `deny` still applies ([Permissions](https://opencode.ai/docs/permissions/)). |
| Plugins | `permission.ask` hook | Can set `output.status` to `ask`, `deny`, or `allow` ([SRC packages/plugin/src/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts)). See [hooks.md](hooks.md). |

## Format

`permission` is either a single action string, which sets everything at once (`"permission": "allow"`), or an object mapping permission keys to an action or to a pattern object (`{ pattern: action }`) ([Permissions](https://opencode.ai/docs/permissions/)).

### Actions

| Action | Effect |
| --- | --- |
| `allow` | Runs without a prompt. |
| `ask` | Prompts. Answers: `once`; `always` (approves the tool-suggested patterns, e.g. `git status*`, for the rest of the session); `reject`. |
| `deny` | Refuses the call. |

### Keys

| Key | Pattern matches | Accepts pattern object | Default |
| --- | --- | --- | --- |
| `read` | file path | yes | `allow` for `*`; `deny` for `*.env` and `*.env.*`; `allow` for `*.env.example` |
| `edit` | file path; covers the `edit`, `write`, and `apply_patch` tools | yes | `allow` |
| `glob` | the glob pattern | yes | `allow` |
| `grep` | the regex | yes | `allow` |
| `list` | — | yes | `allow` |
| `bash` | parsed command, e.g. `git status --porcelain` | yes | `allow` |
| `task` | subagent type | yes | `allow` |
| `skill` | skill name | yes | `allow` |
| `lsp` | currently non-granular | yes | `allow` |
| `external_directory` | paths outside the working directory | yes | `ask` |
| `question` | — | no (action only) | `allow` |
| `webfetch` | the URL | no (action only) | `allow` |
| `websearch` | the query | no (action only) | `allow` |
| `todowrite` | — | no (action only) | `allow` |
| `doom_loop` | the same call repeated 3 times with identical input | no (action only) | `ask` |
| any other name | custom or MCP tool names, e.g. `"mymcp_*"` | yes | |

Sources: [Permissions](https://opencode.ai/docs/permissions/); [Agents](https://opencode.ai/docs/agents/); [Tools](https://opencode.ai/docs/tools/); action-only keys and unknown keys from [SRC core/src/v1/config/permission.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/permission.ts). Defaults: "most keys are `allow`; `doom_loop` and `external_directory` are `ask`" ([Permissions](https://opencode.ai/docs/permissions/)).

### Pattern syntax

- `*` matches any sequence; `?` matches one character.
- `~` or `$HOME` expands to the home directory.
- The last matching rule wins, so put `"*"` first.
- User key order is preserved at parse time to keep precedence correct.
- `"grep *"` allows `grep pattern file`, but `"grep"` alone does not match commands with arguments.

Sources: [Permissions](https://opencode.ai/docs/permissions/); [SRC permission.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/permission.ts).

### `external_directory`

Gates any path outside the working directory, e.g. `{"~/projects/personal/**": "allow"}`. Allowed directories inherit the workspace defaults ([Permissions](https://opencode.ai/docs/permissions/)). Directories configured under `references` are allowed through `external_directory` automatically; normal tool permissions still apply ([References](https://opencode.ai/docs/references/)).

### `task` and `skill`

- `permission.task` controls which subagents an agent may call. A denied subagent is removed from the Task tool description. Users can still `@`-invoke any subagent ([Agents – Task permissions](https://opencode.ai/docs/agents/)). See [subagents.md](subagents.md).
- `permission.skill`: `allow` loads immediately, `deny` hides the skill and rejects access, `ask` prompts first ([Skills](https://opencode.ai/docs/skills/)). See [skills.md](skills.md).

### Legacy `tools` map

Deprecated since v1.1.1. The boolean `tools` map (global or per agent) is merged into `permission` and still supported: `true` becomes `allow`, `false` becomes `deny`, and `write`, `edit`, and `patch` map to `edit` ([Permissions](https://opencode.ai/docs/permissions/); [REL v1.1.1](https://github.com/anomalyco/opencode/releases/tag/v1.1.1); [SRC core/src/v1/config/agent.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/agent.ts)).

### Related config

| Key | Effect |
| --- | --- |
| `experimental.continue_loop_on_deny` | Keeps the agent loop running after a denied tool call ([SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)). |
| `experimental.policies` | Entries like `{effect:"deny", action:"provider.use", resource:"openai"}` ([Config – Policies](https://opencode.ai/docs/config/)). |
| `snapshot` | Default `true`. Internal-git snapshots that make undo/revert possible ([SRC core config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)). |

## Loading and invocation

- Every tool call is checked against the merged rules before it runs. In a pattern object the last matching rule wins.
- `ask` shows a prompt with `once`, `always`, `reject`. `always` lasts for the rest of the session.
- Auto mode: `opencode --auto` or `opencode run --auto` approves requests that would otherwise ask. Explicit `deny` still applies. The TUI command palette has "Enable/Disable auto-approve permissions" toggles ([Permissions](https://opencode.ai/docs/permissions/)).
- Since v1.18.20, `opencode run` answers permission requests raised by subagents ([REL v1.18.20](https://github.com/anomalyco/opencode/releases/tag/v1.18.20)).
- Plugins see each request through the `permission.ask` hook and can block a call by throwing in `tool.execute.before` ([SRC packages/plugin/src/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts)). The bus emits `permission.asked` and `permission.replied` events ([Plugins – Events](https://opencode.ai/docs/plugins/)).
- Context cost: a subagent denied by `permission.task` is removed from the Task tool description; a skill denied by `permission.skill` is hidden from the skill list.

## Example

```json
{ "permission": { "*": "ask", "read": "allow",
  "bash": { "*": "ask", "git status *": "allow", "rm *": "deny" },
  "edit": { "*": "deny", "src/**": "allow" } } }
```

Per-agent override in markdown frontmatter (from the agent example in the notes):

```yaml
permission: { edit: deny, bash: { "*": ask, "git diff*": allow } }
```

## Limits and gotchas

- **No OS-level sandbox is recorded in the notes.** Permission rules are the documented control. This is an absence in the notes, not a confirmed statement from the docs.
- **Defaults are permissive.** All tools are enabled and need no permission by default ([Tools](https://opencode.ai/docs/tools/)); only `doom_loop`, `external_directory`, and `.env` reads differ.
- **Order matters.** The last matching rule wins, so a leading `"*"` must come before specific rules.
- **Bare command names do not match commands with arguments.** Use `"grep *"`, not `"grep"`.
- **Action-only keys:** `todowrite`, `question`, `webfetch`, `websearch`, `doom_loop` do not accept pattern objects.
- **`lsp` is non-granular** at this version.
- **Release history:** auto mode was introduced as "yolo mode" in v1.17.12; the auto-accept state has been kept per server since v1.18.0 ([REL v1.17.12](https://github.com/anomalyco/opencode/releases/tag/v1.17.12), [REL v1.18.0](https://github.com/anomalyco/opencode/releases/tag/v1.18.0)). The `tools` map was deprecated in v1.1.1.
- **Gap:** none of the sources describe the exact algorithm that merges agent and global rules (concatenation or key-by-key replacement). The docs only say agent rules take precedence.
- **Gap:** none of the sources say whether `` !`cmd` `` shell injection in command templates respects `bash` permissions ([commands.md](commands.md)).

## Sources

- https://opencode.ai/docs/permissions/
- https://opencode.ai/docs/agents/
- https://opencode.ai/docs/tools/
- https://opencode.ai/docs/skills/
- https://opencode.ai/docs/references/
- https://opencode.ai/docs/config/
- https://opencode.ai/docs/cli/
- https://opencode.ai/docs/plugins/
- https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/permission.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/agent.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/plugin/src/index.ts
- https://github.com/anomalyco/opencode/releases/tag/v1.1.1
- https://github.com/anomalyco/opencode/releases/tag/v1.17.12
- https://github.com/anomalyco/opencode/releases/tag/v1.18.0
- https://github.com/anomalyco/opencode/releases/tag/v1.18.20
