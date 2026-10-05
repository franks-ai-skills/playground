# Generalized harness concepts

Vendor-neutral versions of the agent harness concepts, built from the
[vendor references](../vendors/). Each page compares Claude Code, Codex
and OpenCode, describes the concept without vendor names, explains how
to author it once for several harnesses, and lists what was left out.

Security is a concern across these concepts. See the
[overview's boundary map](../overview.md#security-across-the-concepts),
the [practical security guide](../guide/security.md) and the
[dated research audit](../research-notes/agent-harness-security.md).
The guide connects attacks to controls and proposed canary checks;
it does not add another generalized mechanism.

## Generalization rule

- Claude Code and Codex are equal leads. A concept or feature is kept
  when both leads have an equivalent mechanism, even under different
  names or formats.
- OpenCode appears in every comparison, but whether it has a feature
  never decides whether the feature is kept.
- A feature that only one lead has is dropped. Each page lists its
  dropped features with the vendor and the reason, under "Dropped from
  the generalization".

## How the concepts fit together

| When | Concept | Generalized summary |
| --- | --- | --- |
| Startup | [Configuration](configuration.md) | Layered settings: defaults, user, project (only once trusted), command line, admin policy. The higher layer wins, except that a stricter safety value wins from any layer. |
| Startup | [Instructions](instructions.md) | Markdown guidance files collected from admin, user and project-directory scopes and joined broadest first. `AGENTS.md` is the shared file name. |
| Startup | [MCP](mcp.md) | Named servers (stdio or streamable HTTP) whose tools appear as `mcp__<server>__<tool>`. |
| Startup | [Plugins](plugins.md) | Bundles of skills, hooks and MCP servers, listed in a marketplace, installed into a cache and enabled in config. |
| Every tool call | [Permissions and sandbox](permissions-and-sandbox.md) | Each call is allowed, asked or denied; an OS sandbox limits what an allowed command can write, read and reach over the network. |
| On demand | [Skills](skills.md) | A folder with `SKILL.md`. Only name and description stay in context; the body loads when the user calls it or the model picks it. |
| On demand | [Commands](commands.md) | Folded into skills: a command is a skill only the user can invoke. |
| On demand | [Subagents](subagents.md) | A named definition that a spawn tool runs in its own context, returning one result. |
| On events | [Hooks](hooks.md) | Event, matcher, handler. Both leads share the JSON shape, eleven event names, and the `command` and `mcp_tool` handlers. |
| Outside a session | [Automation](automation.md) | One "run" model for headless runs, SDK sessions, CI, hosted runs, schedules and worktrees. |

## Portability in short

The details and sources are on each page. The points that most often
decide whether one setup works in both leads:

- **Instructions:** Claude Code reads `AGENTS.md` only when no
  `CLAUDE.md` or `CLAUDE.local.md` exists on the path. A repo that wants
  one file for both leads keeps `AGENTS.md` and no `CLAUDE.md`.
- **Skills:** the leads share no skill directory. Claude Code reads
  `.claude/skills/`, Codex reads `.agents/skills/`. Keep the skill in
  one directory and symlink it into the other; both leads follow
  symlinked skill folders. Only `name` and `description` are read by
  every harness.
- **Hooks:** the same JSON shape works in both leads, but Codex treats
  some decisions differently. For example, a Codex `PreToolUse` hook
  that answers `ask` is marked failed and the tool call proceeds.
- **Plugins:** one repository can serve both leads, because Codex also
  reads `.claude-plugin/marketplace.json` and sets the `CLAUDE_PLUGIN_*`
  variables for plugin hooks.
- **Naming:** no file in an agent-facing directory should be named
  `agents.md` or `claude.md`. On a case-insensitive file system the
  harnesses load it as an instruction file.
