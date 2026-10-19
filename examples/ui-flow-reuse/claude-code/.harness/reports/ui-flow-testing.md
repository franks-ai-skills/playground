# Verification report

- Run: `ui-flow-testing-2026-10-18-r1`
- Harness KB version: 0.1.0
- Contract digest: 1a72354a28a8919100129f177f007a5d58216d73be1270a7f6d6436b85802b64
- Confirmed parts: A
- Decision record digest: 8de94681b74439697d5d5111e5a985eaf358c08c3bbed48b6de57df3f234271e
- Whole-idea answers and targets: `{"facts": {"bypass_mode": false, "lethal_trifecta": false, "opens_prs": false, "plan_controls": "available", "reach": "repository", "target_set": "both", "untrusted_repo": false}, "hosting": {"plan": "team", "platform": "github", "visibility": "private"}, "reach": "repository", "targets": ["claude-code", "codex"]}` (digest e0091612b649e65a4da56c4ee3d4ea04cc8e2b359517718d683fb627b42f19ec)
- Rule content digest: 93fec41536adbe0420026720fecbe03465b27f5f457695dc9d5704d422d7488a
- Accepted Idea KB revision: c724ac91b59e022d5ed2ecffaeedbab8332d05b79462704ef64206d1b4d21f2d
- Review scope: First run: judged A
- Rule overrides: none
- Checker versions digest: 7beeb29d229339f59695dccf5877b0efc53a7e117ff8fb0b7773c93c0d92e0df

## Worker isolation

Workers ran under `best-effort-v1` with isolation status `not-certified`. Research, source-support and review workers run as independent CLI processes with explicit role inputs and the available restrictions. Complete tool absence and context, file and network isolation are not guaranteed; use trusted projects and operator-approved inputs.

- research worker: claude-code 2.1.302 (Claude Code), model account default, launcher independent-process, configuration 8f829a4997165574f012341c9cfd6babd3d9105bc9c559508d67a78b3ae277ea, controls: command: ["claude", "--print", "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--safe-mode", "--restricted", "--setting-sources", "", "--strict-mcp-config", "--mcp-config", "{\"mcpServers\":{}}", "--disable-slash-commands", "--permission-mode", "dontAsk", "--permission-prompts", "none", "--settings", "{\"disableAllHooks\":true,\"autoMemoryEnabled\":false}", "--tools", "WebFetch,WebSearch", "--allowedTools", "WebFetch,WebSearch", "--json-schema", "{\"type\":\"object\",\"properties\":{\"findings\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"claim\":{\"type\":\"string\"},\"source\":{\"type\":\"string\"},\"fetched\":{\"type\":\"string\"},\"quote\":{\"type\":\"string\"},\"context\":{\"type\":\"string\"},\"source_role\":{\"enum\":[\"primary\",\"practitioner\",\"trade-press\"]}},\"required\":[\"claim\",\"source\",\"fetched\",\"quote\",\"context\",\"source_role\"],\"additionalProperties\":false}}},\"required\":[\"findings\"],\"additionalProperties\":false}"]; environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (claude.ai), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- source-support worker: claude-code 2.1.302 (Claude Code), model account default, launcher independent-process, configuration f79908e2f8761717b26bb5d87aed5c56e135ba70a0edb97e404129d59e06e708, controls: command: ["claude", "--print", "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--safe-mode", "--restricted", "--setting-sources", "", "--strict-mcp-config", "--mcp-config", "{\"mcpServers\":{}}", "--disable-slash-commands", "--permission-mode", "dontAsk", "--permission-prompts", "none", "--settings", "{\"disableAllHooks\":true,\"autoMemoryEnabled\":false}", "--tools", "", "--allowedTools", "", "--json-schema", "{\"type\":\"object\",\"properties\":{\"verdicts\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"finding_id\":{\"type\":\"string\"},\"verdict\":{\"enum\":[\"supported\",\"unsupported\"]},\"reasoning\":{\"type\":\"string\"}},\"required\":[\"finding_id\",\"verdict\",\"reasoning\"],\"additionalProperties\":false}}},\"required\":[\"verdicts\"],\"additionalProperties\":false}"]; environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (claude.ai), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- review worker: claude-code 2.1.302 (Claude Code), model account default, launcher independent-process, configuration bd41806234b54333f0b42bf98e08945ea9756a175b212e92e0435a771b2beb3f, controls: command: ["claude", "--print", "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--safe-mode", "--restricted", "--setting-sources", "", "--strict-mcp-config", "--mcp-config", "{\"mcpServers\":{}}", "--disable-slash-commands", "--permission-mode", "dontAsk", "--permission-prompts", "none", "--settings", "{\"disableAllHooks\":true,\"autoMemoryEnabled\":false}", "--tools", "Read,Grep,Glob", "--allowedTools", "Read,Grep,Glob", "--json-schema", "{\"type\":\"object\",\"properties\":{\"run_id\":{\"type\":\"string\"},\"verdicts\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"part_id\":{\"type\":\"string\"},\"rule_id\":{\"type\":\"string\"},\"verdict\":{\"enum\":[\"pass\",\"fail\",\"not-applicable\"]},\"reason\":{\"type\":\"string\"},\"citation\":{\"type\":\"string\"}},\"required\":[\"part_id\",\"rule_id\",\"verdict\",\"reason\",\"citation\"],\"additionalProperties\":false}},\"goal_verdicts\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"part_id\":{\"type\":\"string\"},\"verdict\":{\"enum\":[\"met\",\"not-met\"]},\"reason\":{\"type\":\"string\"}},\"required\":[\"part_id\",\"verdict\",\"reason\"],\"additionalProperties\":false}}},\"required\":[\"run_id\",\"verdicts\",\"goal_verdicts\"],\"additionalProperties\":false}"]; environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (claude.ai), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable

## Part A

- Harness result: not checked
- Goal result: not assessed
- Status: decided
- Outside dependencies: none
- Confirmed answers: `{"event_without_agent": false, "every_time": "usually", "irreversible": false, "job": "procedure", "must_survive_compromise": "not-required", "own_context": false, "trigger": "model", "who_disables": "contributor"}`

| Rule | Severity | Check | Result | Reason | Citation | Sources |
| --- | --- | --- | --- | --- | --- | --- |

## Runtime tests

none run

## Checked files

```
90f8f6627701eda7ff0c1c80f369eca8f1032b8a06dfcfaa23263431415b6377  README.md
```

## Report data

```json
{
  "answers": {
    "A": {
      "event_without_agent": false,
      "every_time": "usually",
      "irreversible": false,
      "job": "procedure",
      "must_survive_compromise": "not-required",
      "own_context": false,
      "trigger": "model",
      "who_disables": "contributor"
    }
  },
  "bound_inputs": {
    "cases": {
      "A": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
    },
    "checkers": "7beeb29d229339f59695dccf5877b0efc53a7e117ff8fb0b7773c93c0d92e0df",
    "files": {
      "README.md": "90f8f6627701eda7ff0c1c80f369eca8f1032b8a06dfcfaa23263431415b6377"
    },
    "idea": "e0091612b649e65a4da56c4ee3d4ea04cc8e2b359517718d683fb627b42f19ec",
    "kb_version": "0.1.0",
    "overrides": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "parts": {
      "A": "7698733ce87a45ab28904576f5fc07a79d0cccb2c5c8820a42873435734ceef3"
    },
    "revision": "c724ac91b59e022d5ed2ecffaeedbab8332d05b79462704ef64206d1b4d21f2d",
    "rules": "93fec41536adbe0420026720fecbe03465b27f5f457695dc9d5704d422d7488a",
    "symlinks": {},
    "worker": "cb9988f2be30ff09747816ba5776418c93488ff83c58db1c3b94386ed7c3018d"
  },
  "confirmed_parts": [
    "A"
  ],
  "contract_digest": "1a72354a28a8919100129f177f007a5d58216d73be1270a7f6d6436b85802b64",
  "decision_digest": "8de94681b74439697d5d5111e5a985eaf358c08c3bbed48b6de57df3f234271e",
  "file_hashes": {
    "README.md": "90f8f6627701eda7ff0c1c80f369eca8f1032b8a06dfcfaa23263431415b6377"
  },
  "idea_digest": "e0091612b649e65a4da56c4ee3d4ea04cc8e2b359517718d683fb627b42f19ec",
  "kb_version": "0.1.0",
  "overrides": [],
  "part_map": {
    "dirs": {},
    "files": {
      "A": [
        "README.md"
      ]
    },
    "links": {},
    "requirement_parts": [
      "A"
    ]
  },
  "parts": [
    {
      "goal_result": "not assessed",
      "goal_verdict": null,
      "harness_result": "not checked",
      "outside_dependencies": [],
      "part_id": "A",
      "rule_results": [],
      "status": "decided"
    }
  ],
  "revision_digest": "c724ac91b59e022d5ed2ecffaeedbab8332d05b79462704ef64206d1b4d21f2d",
  "rules_digest": "93fec41536adbe0420026720fecbe03465b27f5f457695dc9d5704d422d7488a",
  "run_id": "ui-flow-testing-2026-10-18-r1",
  "runtime_results": [],
  "scope": "First run: judged A",
  "scope_parts": null,
  "symlinks": {},
  "tool_versions": {
    "harness-forge-checkers": "7beeb29d229339f59695dccf5877b0efc53a7e117ff8fb0b7773c93c0d92e0df"
  },
  "whole_idea": {
    "facts": {
      "bypass_mode": false,
      "lethal_trifecta": false,
      "opens_prs": false,
      "plan_controls": "available",
      "reach": "repository",
      "target_set": "both",
      "untrusted_repo": false
    },
    "hosting": {
      "plan": "team",
      "platform": "github",
      "visibility": "private"
    },
    "reach": "repository",
    "targets": [
      "claude-code",
      "codex"
    ]
  },
  "worker_evidence": [
    {
      "configuration_digest": "8f829a4997165574f012341c9cfd6babd3d9105bc9c559508d67a78b3ae277ea",
      "configured_controls": [
        "command: [\"claude\", \"--print\", \"--output-format\", \"stream-json\", \"--verbose\", \"--no-session-persistence\", \"--safe-mode\", \"--restricted\", \"--setting-sources\", \"\", \"--strict-mcp-config\", \"--mcp-config\", \"{\\\"mcpServers\\\":{}}\", \"--disable-slash-commands\", \"--permission-mode\", \"dontAsk\", \"--permission-prompts\", \"none\", \"--settings\", \"{\\\"disableAllHooks\\\":true,\\\"autoMemoryEnabled\\\":false}\", \"--tools\", \"WebFetch,WebSearch\", \"--allowedTools\", \"WebFetch,WebSearch\", \"--json-schema\", \"{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"findings\\\":{\\\"type\\\":\\\"array\\\",\\\"items\\\":{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"claim\\\":{\\\"type\\\":\\\"string\\\"},\\\"source\\\":{\\\"type\\\":\\\"string\\\"},\\\"fetched\\\":{\\\"type\\\":\\\"string\\\"},\\\"quote\\\":{\\\"type\\\":\\\"string\\\"},\\\"context\\\":{\\\"type\\\":\\\"string\\\"},\\\"source_role\\\":{\\\"enum\\\":[\\\"primary\\\",\\\"practitioner\\\",\\\"trade-press\\\"]}},\\\"required\\\":[\\\"claim\\\",\\\"source\\\",\\\"fetched\\\",\\\"quote\\\",\\\"context\\\",\\\"source_role\\\"],\\\"additionalProperties\\\":false}}},\\\"required\\\":[\\\"findings\\\"],\\\"additionalProperties\\\":false}\"]",
        "environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER",
        "login: subscription (claude.ai)"
      ],
      "evidence_refs": [],
      "harness": "claude-code",
      "harness_version": "2.1.302 (Claude Code)",
      "isolation_status": "not-certified",
      "launcher": "independent-process",
      "model": "account default",
      "observed_behavior": [],
      "observed_tools": {
        "status": "unknown"
      },
      "role": "research",
      "unknowns": [
        "context, file and network isolation are not certified",
        "not every tool-registration path is observable"
      ],
      "worker_policy": "best-effort-v1"
    },
    {
      "configuration_digest": "f79908e2f8761717b26bb5d87aed5c56e135ba70a0edb97e404129d59e06e708",
      "configured_controls": [
        "command: [\"claude\", \"--print\", \"--output-format\", \"stream-json\", \"--verbose\", \"--no-session-persistence\", \"--safe-mode\", \"--restricted\", \"--setting-sources\", \"\", \"--strict-mcp-config\", \"--mcp-config\", \"{\\\"mcpServers\\\":{}}\", \"--disable-slash-commands\", \"--permission-mode\", \"dontAsk\", \"--permission-prompts\", \"none\", \"--settings\", \"{\\\"disableAllHooks\\\":true,\\\"autoMemoryEnabled\\\":false}\", \"--tools\", \"\", \"--allowedTools\", \"\", \"--json-schema\", \"{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"verdicts\\\":{\\\"type\\\":\\\"array\\\",\\\"items\\\":{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"finding_id\\\":{\\\"type\\\":\\\"string\\\"},\\\"verdict\\\":{\\\"enum\\\":[\\\"supported\\\",\\\"unsupported\\\"]},\\\"reasoning\\\":{\\\"type\\\":\\\"string\\\"}},\\\"required\\\":[\\\"finding_id\\\",\\\"verdict\\\",\\\"reasoning\\\"],\\\"additionalProperties\\\":false}}},\\\"required\\\":[\\\"verdicts\\\"],\\\"additionalProperties\\\":false}\"]",
        "environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER",
        "login: subscription (claude.ai)"
      ],
      "evidence_refs": [],
      "harness": "claude-code",
      "harness_version": "2.1.302 (Claude Code)",
      "isolation_status": "not-certified",
      "launcher": "independent-process",
      "model": "account default",
      "observed_behavior": [],
      "observed_tools": {
        "status": "unknown"
      },
      "role": "source-support",
      "unknowns": [
        "context, file and network isolation are not certified",
        "not every tool-registration path is observable"
      ],
      "worker_policy": "best-effort-v1"
    },
    {
      "configuration_digest": "bd41806234b54333f0b42bf98e08945ea9756a175b212e92e0435a771b2beb3f",
      "configured_controls": [
        "command: [\"claude\", \"--print\", \"--output-format\", \"stream-json\", \"--verbose\", \"--no-session-persistence\", \"--safe-mode\", \"--restricted\", \"--setting-sources\", \"\", \"--strict-mcp-config\", \"--mcp-config\", \"{\\\"mcpServers\\\":{}}\", \"--disable-slash-commands\", \"--permission-mode\", \"dontAsk\", \"--permission-prompts\", \"none\", \"--settings\", \"{\\\"disableAllHooks\\\":true,\\\"autoMemoryEnabled\\\":false}\", \"--tools\", \"Read,Grep,Glob\", \"--allowedTools\", \"Read,Grep,Glob\", \"--json-schema\", \"{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"run_id\\\":{\\\"type\\\":\\\"string\\\"},\\\"verdicts\\\":{\\\"type\\\":\\\"array\\\",\\\"items\\\":{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"part_id\\\":{\\\"type\\\":\\\"string\\\"},\\\"rule_id\\\":{\\\"type\\\":\\\"string\\\"},\\\"verdict\\\":{\\\"enum\\\":[\\\"pass\\\",\\\"fail\\\",\\\"not-applicable\\\"]},\\\"reason\\\":{\\\"type\\\":\\\"string\\\"},\\\"citation\\\":{\\\"type\\\":\\\"string\\\"}},\\\"required\\\":[\\\"part_id\\\",\\\"rule_id\\\",\\\"verdict\\\",\\\"reason\\\",\\\"citation\\\"],\\\"additionalProperties\\\":false}},\\\"goal_verdicts\\\":{\\\"type\\\":\\\"array\\\",\\\"items\\\":{\\\"type\\\":\\\"object\\\",\\\"properties\\\":{\\\"part_id\\\":{\\\"type\\\":\\\"string\\\"},\\\"verdict\\\":{\\\"enum\\\":[\\\"met\\\",\\\"not-met\\\"]},\\\"reason\\\":{\\\"type\\\":\\\"string\\\"}},\\\"required\\\":[\\\"part_id\\\",\\\"verdict\\\",\\\"reason\\\"],\\\"additionalProperties\\\":false}}},\\\"required\\\":[\\\"run_id\\\",\\\"verdicts\\\",\\\"goal_verdicts\\\"],\\\"additionalProperties\\\":false}\"]",
        "environment names: CLAUDE_CONFIG_DIR, HOME, LANG, LOGNAME, PATH, TMPDIR, USER",
        "login: subscription (claude.ai)"
      ],
      "evidence_refs": [],
      "harness": "claude-code",
      "harness_version": "2.1.302 (Claude Code)",
      "isolation_status": "not-certified",
      "launcher": "independent-process",
      "model": "account default",
      "observed_behavior": [],
      "observed_tools": {
        "status": "unknown"
      },
      "role": "review",
      "unknowns": [
        "context, file and network isolation are not certified",
        "not every tool-registration path is observable"
      ],
      "worker_policy": "best-effort-v1"
    }
  ],
  "worker_violations": []
}
```
