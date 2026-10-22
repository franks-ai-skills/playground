# Example web app

The team's web app frontend. `npm run dev` serves it at http://localhost:5173.
Developers check UI changes locally in a browser before opening a pull request.

## Outside controls

- `codeowners-agent-config` (part A): recommended, not verified. Precaution; availability available. It works as a gate only when:
  - Workflow, scanner and policy files that define a gate are under code owners or come from outside the repository at a pinned ref, and CODEOWNERS owns itself (`outside.ci.workflow-protected`)
  - A CODEOWNERS entry names an owner for every file that configures the agent, including `.agents/`, `.claude/`, `CLAUDE.md`, `.mcp.json`, `.codex/`, `AGENTS.md`, `AGENTS.override.md`, `.devcontainer/`, the CI workflow files and the CODEOWNERS file itself, and the branch rule requires code-owner review (`outside.codeowners.agent-config`)
  - It targets the real refs and resources it protects, such as the default and release branches and tags or the production accounts (`outside.gate.real-refs`)
  - Its configuration is checked periodically, because gate configuration drifts silently (`outside.gate.periodic-verification`)
