# Skills

OpenCode supports Agent Skills: folders with a `SKILL.md` file that carries YAML frontmatter and markdown instructions. Only each skill's name and description sit in context up front; the model loads a skill's full body on demand through the native `skill` tool. OpenCode reads skills from its own directories and also from Claude Code's `.claude/skills` and the shared `.agents/skills` locations.

## Locations and scopes

One folder per skill, containing `SKILL.md` ([Skills](https://opencode.ai/docs/skills/)):

| Scope | Path |
| --- | --- |
| Project (OpenCode) | `.opencode/skills/<name>/` |
| Global (OpenCode) | `~/.config/opencode/skills/<name>/` |
| Project (Claude Code) | `.claude/skills/<name>/` |
| Global (Claude Code) | `~/.claude/skills/<name>/` |
| Project (Agent Skills) | `.agents/skills/<name>/` |
| Global (Agent Skills) | `~/.agents/skills/<name>/` |
| Config | `skills.paths` entries (extra folders) |
| Remote | `skills.urls` entries |
| Built-in | `customize-opencode` |

For project paths, OpenCode walks up from the cwd to the git worktree ([Skills](https://opencode.ai/docs/skills/)).

### Discovery patterns in source

([SRC skill/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/skill/index.ts), [SRC skill/discovery.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/skill/discovery.ts), [SRC core skills.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/skills.ts))

| Location | Pattern |
| --- | --- |
| `.claude` and `.agents` dirs | `skills/**/SKILL.md` |
| Every OpenCode config dir ([configuration.md](configuration.md#config-directories)) | `{skill,skills}/**/SKILL.md` |
| Each `skills.paths` entry (relative to cwd, `~/`, or absolute) | `**/SKILL.md` |
| Each `skills.urls` entry, e.g. `https://example.com/.well-known/skills/` | OpenCode fetches `<url>/index.json` and pulls the listed skills. |

### Switches

| Switch | Effect |
| --- | --- |
| `OPENCODE_DISABLE_EXTERNAL_SKILLS` | Turns off `.claude` and `.agents` discovery ([SRC skill/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/skill/index.ts)). |
| `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1` | Opts out of Claude Code skills ([Rules](https://opencode.ai/docs/rules/)). |
| `OPENCODE_DISABLE_CLAUDE_CODE=1` | Disables all `.claude` support ([Rules](https://opencode.ai/docs/rules/)). |

## Format

`SKILL.md` (filename in all caps) with YAML frontmatter and a markdown body ([Skills](https://opencode.ai/docs/skills/)).

| Field | Required | Constraint / meaning |
| --- | --- | --- |
| `name` | yes | 1–64 characters, `^[a-z0-9]+(-[a-z0-9]+)*$`, must match the directory name. Must be unique across all locations. |
| `description` | yes | 1–1024 characters. Shown to the model in the skill list. |
| `license` | no | License. |
| `compatibility` | no | Compatibility note. |
| `metadata` | no | String → string map. |
| any other field | — | Ignored. |

### `skills` config key

`skills: { paths?: string[], urls?: string[] }` ([SRC core/src/v1/config/config.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts)).

| Key | Meaning |
| --- | --- |
| `paths` | Extra skill folders. Searched with `**/SKILL.md`. |
| `urls` | Skill URLs. `<url>/index.json` is fetched and the listed skills are pulled. |

### `permission.skill`

Pattern object over skill names ([Skills](https://opencode.ai/docs/skills/)):

| Action | Effect |
| --- | --- |
| `allow` | Loads immediately. |
| `deny` | Hides the skill and rejects access. |
| `ask` | Prompts before loading. |

Overrides work per agent. `tools: { skill: false }` (legacy `tools` map) removes `<available_skills>` entirely. See [permissions-and-sandbox.md](permissions-and-sandbox.md).

## Loading and invocation

- **Listing (always in context):** the `skill` tool's description lists the available skills as `<available_skills><skill><name/><description/></skill>…` ([Skills](https://opencode.ai/docs/skills/)). The context cost up front is the name and description of each visible skill.
- **Loading (on demand):** the agent calls `skill({ name: "git-release" })` to load the full content ([Skills](https://opencode.ai/docs/skills/)).
- **Slash commands:** every skill is also registered as a slash command (`source: "skill"`) unless a command already has that name. The command template is the skill body plus "Base directory for this skill: <dir>" ([SRC command/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/command/index.ts)). See [commands.md](commands.md).
- **Built-in skill `customize-opencode`:** description "Use ONLY when the user is editing or creating opencode's own configuration… agents, subagents, skills, plugins, MCP servers, or permission rules" ([SRC skill/index.ts](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/skill/index.ts)).
- **Remote skills:** cached; v1.17.12 added refresh of cached remote skills ([REL v1.17.12](https://github.com/anomalyco/opencode/releases/tag/v1.17.12)).
- **Plugins:** the V2 plugin API has a `ctx.skill.transform` hook ([plugins.md](plugins.md#v2-plugin-api)).

## Example

```markdown
<!-- .opencode/skills/git-release/SKILL.md -->
---
name: git-release
description: Prepares a release tag and changelog. Use when the user asks to cut a release.
---
Steps for preparing a release ...
```

The folder name `git-release` matches `name`. The model loads it with `skill({ name: "git-release" })`.

## Limits and gotchas

- **Troubleshooting checklist** ([Skills](https://opencode.ai/docs/skills/)): the filename must be `SKILL.md` in all caps; `name` and `description` must be present; names must be unique across all locations; denied skills are hidden.
- **Claude Code skills load directly (inference from the notes).** Fields that only Claude Code understands, such as `allowed-tools`, are ignored because unknown frontmatter fields are ignored.
- **Skill vs command name clash:** a skill is not registered as a slash command when a command with the same name exists.
- **Base directory note:** since v1.17.10 the "Base directory for this skill" note is a filesystem path, not a `file://` URL ([REL v1.17.10](https://github.com/anomalyco/opencode/releases/tag/v1.17.10)).
- **Release history:** v1.16.0 added skill discovery (together with file-based agent loading) ([REL v1.16.0](https://github.com/anomalyco/opencode/releases/tag/v1.16.0)); v1.17.12 added refresh of cached remote skills and preservation of skill resource paths ([REL v1.17.12](https://github.com/anomalyco/opencode/releases/tag/v1.17.12)).
- **Gap:** none of the sources specify the format of the remote `index.json` for `skills.urls`.
- **Gap:** `skills.paths` and `skills.urls` do not appear on the user docs page; they come from source only.

## Sources

- https://opencode.ai/docs/skills/
- https://opencode.ai/docs/rules/
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/skill/index.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/skill/discovery.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/skills.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/core/src/v1/config/config.ts
- https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/command/index.ts
- https://github.com/anomalyco/opencode/releases/tag/v1.16.0
- https://github.com/anomalyco/opencode/releases/tag/v1.17.10
- https://github.com/anomalyco/opencode/releases/tag/v1.17.12
