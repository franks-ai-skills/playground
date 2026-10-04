# Best practices

How to use each [generalized concept](../concepts/) well: which
approaches exist, how to implement them in Claude Code and Codex, what
to watch for, and how to check that a setup works. Commands have no
page of their own: they are user-invoked skills, covered in
[skills](skills.md).

Every practice carries an evidence label:

| Label | Meaning |
| --- | --- |
| [Vendor] | Guidance or documentation from Anthropic, OpenAI or the OpenCode project. |
| [Empirical] | A study, benchmark or measurement. |
| [Advisory] | A security advisory, CVE, incident report, or a standard such as agentskills.io or OWASP. |
| [Practitioner] | Experience reported by a named engineer or company. |

## Pages

| Page | Covers |
| --- | --- |
| [Instructions](instructions.md) | What goes into `AGENTS.md` and its siblings, size, structure, maintenance, injection risk. |
| [Configuration](configuration.md) | Which setting belongs in which scope, secrets, policy layer, profiles, headless runs over untrusted repositories. |
| [Permissions and sandbox](permissions-and-sandbox.md) | Rule design, sandbox setup, reducing prompts safely, bypass modes, threat model. |
| [Skills](skills.md) | When to write a skill, descriptions as triggers, structure, scripts, user-invoked skills, evals, third-party skills. |
| [Subagents](subagents.md) | When delegation helps, definitions, orchestration patterns, delegation messages, output contracts, measurement. |
| [Hooks](hooks.md) | Deterministic gates, decision design, Stop loops, performance, hook security, portable scripts, testing. |
| [MCP](mcp.md) | MCP versus CLI plus skill, limiting tools and output, building servers, server security. |
| [Plugins](plugins.md) | When to package, versioning, one repository for both leads, marketplaces, reviewing third-party plugins. |
| [Automation](automation.md) | The explore, plan, implement, verify loop, headless and CI runs, parallel work, schedules, SDKs, measuring outcomes. |

## Practices that recur across pages

- **Enforce with mechanisms, guide with text.** Instruction files and
  skills are advisory. Rules that must always hold go into permissions,
  the sandbox, hooks or CI ([instructions](instructions.md),
  [hooks](hooks.md), [permissions and sandbox](permissions-and-sandbox.md)).
- **Treat agent configuration as executable code.** Repository settings,
  hooks, MCP servers, plugins and instruction files have all been
  attack paths, with CVEs in both leads. Review them like code and
  restrict them for untrusted repositories ([configuration](configuration.md)).
- **Give the agent a check it can run, and let something other than
  the implementer grade the result** ([automation](automation.md),
  [subagents](subagents.md)).
- **Measure against a baseline.** Instruction files, skills and
  subagents have each made results worse in some measured cases. Compare
  with and without the change on real tasks before keeping it
  ([skills](skills.md), [subagents](subagents.md),
  [instructions](instructions.md)).
- **Keep always-loaded context small** and move situational material
  behind a pointer with an explicit trigger ([instructions](instructions.md),
  [skills](skills.md), [MCP](mcp.md)).

The research notes behind these pages, with all sources, are in
[`../research-notes/agent-harness-best-practices/`](../research-notes/agent-harness-best-practices/).
