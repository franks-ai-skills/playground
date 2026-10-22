# Verification report

- Run: `reuse-codex-2026-10-18-local-ui-testing`
- Harness KB version: 0.1.0
- Contract digest: 70965552da16863b79b3e71b371c345382235fbe6b2e1d81562955ab03cf341d
- Confirmed parts: A
- Decision record digest: a8f6434e0810e4d0e5acac609b7e94bac8dfad18874ea96c0889698b978894bc
- Whole-idea answers and targets: `{"facts": {"bypass_mode": false, "lethal_trifecta": false, "opens_prs": false, "reach": "repository", "target_set": "both", "untrusted_repo": false}, "hosting": {"plan": "Team", "platform": "GitHub", "visibility": "private"}, "reach": "repository", "targets": ["claude-code", "codex"]}` (digest e3267fc8bcdcdd279b6ddb54c23942050d310f613b069d10cf2fe3bdec1e31f8)
- Rule content digest: 93fec41536adbe0420026720fecbe03465b27f5f457695dc9d5704d422d7488a
- Accepted Idea KB revision: f6f1a9b7ba48dbbc780350f1f90a7ed03344e159728568be5fd596e38a9912d2
- Review scope: First run: judged A
- Rule overrides: none
- Checker versions digest: 7beeb29d229339f59695dccf5877b0efc53a7e117ff8fb0b7773c93c0d92e0df

## Worker isolation

Workers ran under `best-effort-v1` with isolation status `not-certified`. Research, source-support and review workers run as independent CLI processes with explicit role inputs and the available restrictions. Complete tool absence and context, file and network isolation are not guaranteed; use trusted projects and operator-approved inputs.

- research worker: codex codex-cli 0.162.1, model account default, launcher independent-process, configuration d28f2bef0b1a2d477e3a44729b3bbe7971f0df2924cf44e48fc1fa9f21618a1b, controls: command: ["codex", "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--ephemeral", "--json", "--color", "never", "--strict-config", "-C", "<workspace>", "--output-schema", "<workspace>/output-schema.json", "-c", "approval_policy=\"never\"", "-c", "project_doc_max_bytes=0", "-c", "mcp_servers={}", "-c", "apps._default.enabled=false", "-c", "web_search=\"live\"", "-c", "default_permissions=\"forge-worker\"", "-c", "permissions.forge-worker.filesystem={\":root\"=\"deny\", \":minimal\"=\"read\", \"<workspace>\"=\"read\"}", "-c", "permissions.forge-worker.network.enabled=false", "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "features.hooks=false", "-c", "features.multi_agent=false", "-c", "features.browser_use=false", "-c", "features.browser_use_external=false", "-c", "features.computer_use=false", "-c", "features.image_generation=false", "-c", "features.remote_plugin=false", "-c", "features.tool_suggest=false", "-c", "features.view_image=false", "-c", "features.shell_tool=false", "-c", "features.unified_exec=false", "-"]; environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (ChatGPT), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- source-support worker: codex codex-cli 0.162.1, model account default, launcher independent-process, configuration faf9aa6201600adb491f3d870fcedefb9b6cf86d13bde50a61d7e3e8b755540f, controls: command: ["codex", "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--ephemeral", "--json", "--color", "never", "--strict-config", "-C", "<workspace>", "--output-schema", "<workspace>/output-schema.json", "-c", "approval_policy=\"never\"", "-c", "project_doc_max_bytes=0", "-c", "mcp_servers={}", "-c", "apps._default.enabled=false", "-c", "web_search=\"disabled\"", "-c", "default_permissions=\"forge-worker\"", "-c", "permissions.forge-worker.filesystem={\":root\"=\"deny\", \":minimal\"=\"read\", \"<workspace>\"=\"read\"}", "-c", "permissions.forge-worker.network.enabled=false", "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "features.hooks=false", "-c", "features.multi_agent=false", "-c", "features.browser_use=false", "-c", "features.browser_use_external=false", "-c", "features.computer_use=false", "-c", "features.image_generation=false", "-c", "features.remote_plugin=false", "-c", "features.tool_suggest=false", "-c", "features.view_image=false", "-c", "features.shell_tool=false", "-c", "features.unified_exec=false", "-"]; environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (ChatGPT), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable
- review worker: codex codex-cli 0.162.1, model account default, launcher independent-process, configuration 0952a1dca9b7ff5765fac8f2121e99b97aa2bce930524db4b061e9ca569f2876, controls: command: ["codex", "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--ephemeral", "--json", "--color", "never", "--strict-config", "-C", "<workspace>", "--output-schema", "<workspace>/output-schema.json", "-c", "approval_policy=\"never\"", "-c", "project_doc_max_bytes=0", "-c", "mcp_servers={}", "-c", "apps._default.enabled=false", "-c", "web_search=\"disabled\"", "-c", "default_permissions=\"forge-worker\"", "-c", "permissions.forge-worker.filesystem={\":root\"=\"deny\", \":minimal\"=\"read\", \"<workspace>\"=\"read\"}", "-c", "permissions.forge-worker.network.enabled=false", "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "features.hooks=false", "-c", "features.multi_agent=false", "-c", "features.browser_use=false", "-c", "features.browser_use_external=false", "-c", "features.computer_use=false", "-c", "features.image_generation=false", "-c", "features.remote_plugin=false", "-c", "features.tool_suggest=false", "-c", "features.view_image=false", "-"]; environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER; login: subscription (ChatGPT), observed tools: unknown, unknowns: context, file and network isolation are not certified; not every tool-registration path is observable

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
16d11facd662ff9b4357bd3f6acbfe86ca5e031934f5f929f9dae582af535377  README.md
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
      "README.md": "16d11facd662ff9b4357bd3f6acbfe86ca5e031934f5f929f9dae582af535377"
    },
    "idea": "e3267fc8bcdcdd279b6ddb54c23942050d310f613b069d10cf2fe3bdec1e31f8",
    "kb_version": "0.1.0",
    "overrides": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "parts": {
      "A": "d69a4ccc60bb432e4c3ac7f6ce523b97b088dbb1feede03f4497847b96c77049"
    },
    "revision": "f6f1a9b7ba48dbbc780350f1f90a7ed03344e159728568be5fd596e38a9912d2",
    "rules": "93fec41536adbe0420026720fecbe03465b27f5f457695dc9d5704d422d7488a",
    "symlinks": {},
    "worker": "d7b55955550d1e0ae7442dd636cfb0c68cd5c02b7c932f908d2a8ab0a0b53f92"
  },
  "confirmed_parts": [
    "A"
  ],
  "contract_digest": "70965552da16863b79b3e71b371c345382235fbe6b2e1d81562955ab03cf341d",
  "decision_digest": "a8f6434e0810e4d0e5acac609b7e94bac8dfad18874ea96c0889698b978894bc",
  "file_hashes": {
    "README.md": "16d11facd662ff9b4357bd3f6acbfe86ca5e031934f5f929f9dae582af535377"
  },
  "idea_digest": "e3267fc8bcdcdd279b6ddb54c23942050d310f613b069d10cf2fe3bdec1e31f8",
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
  "revision_digest": "f6f1a9b7ba48dbbc780350f1f90a7ed03344e159728568be5fd596e38a9912d2",
  "rules_digest": "93fec41536adbe0420026720fecbe03465b27f5f457695dc9d5704d422d7488a",
  "run_id": "reuse-codex-2026-10-18-local-ui-testing",
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
      "reach": "repository",
      "target_set": "both",
      "untrusted_repo": false
    },
    "hosting": {
      "plan": "Team",
      "platform": "GitHub",
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
      "configuration_digest": "d28f2bef0b1a2d477e3a44729b3bbe7971f0df2924cf44e48fc1fa9f21618a1b",
      "configured_controls": [
        "command: [\"codex\", \"--no-daemon\", \"exec\", \"--ignore-user-config\", \"--ignore-rules\", \"--skip-git-repo-check\", \"--ephemeral\", \"--json\", \"--color\", \"never\", \"--strict-config\", \"-C\", \"<workspace>\", \"--output-schema\", \"<workspace>/output-schema.json\", \"-c\", \"approval_policy=\\\"never\\\"\", \"-c\", \"project_doc_max_bytes=0\", \"-c\", \"mcp_servers={}\", \"-c\", \"apps._default.enabled=false\", \"-c\", \"web_search=\\\"live\\\"\", \"-c\", \"default_permissions=\\\"forge-worker\\\"\", \"-c\", \"permissions.forge-worker.filesystem={\\\":root\\\"=\\\"deny\\\", \\\":minimal\\\"=\\\"read\\\", \\\"<workspace>\\\"=\\\"read\\\"}\", \"-c\", \"permissions.forge-worker.network.enabled=false\", \"-c\", \"features.apps=false\", \"-c\", \"features.plugins=false\", \"-c\", \"features.hooks=false\", \"-c\", \"features.multi_agent=false\", \"-c\", \"features.browser_use=false\", \"-c\", \"features.browser_use_external=false\", \"-c\", \"features.computer_use=false\", \"-c\", \"features.image_generation=false\", \"-c\", \"features.remote_plugin=false\", \"-c\", \"features.tool_suggest=false\", \"-c\", \"features.view_image=false\", \"-c\", \"features.shell_tool=false\", \"-c\", \"features.unified_exec=false\", \"-\"]",
        "environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER",
        "login: subscription (ChatGPT)"
      ],
      "evidence_refs": [],
      "harness": "codex",
      "harness_version": "codex-cli 0.162.1",
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
      "configuration_digest": "faf9aa6201600adb491f3d870fcedefb9b6cf86d13bde50a61d7e3e8b755540f",
      "configured_controls": [
        "command: [\"codex\", \"--no-daemon\", \"exec\", \"--ignore-user-config\", \"--ignore-rules\", \"--skip-git-repo-check\", \"--ephemeral\", \"--json\", \"--color\", \"never\", \"--strict-config\", \"-C\", \"<workspace>\", \"--output-schema\", \"<workspace>/output-schema.json\", \"-c\", \"approval_policy=\\\"never\\\"\", \"-c\", \"project_doc_max_bytes=0\", \"-c\", \"mcp_servers={}\", \"-c\", \"apps._default.enabled=false\", \"-c\", \"web_search=\\\"disabled\\\"\", \"-c\", \"default_permissions=\\\"forge-worker\\\"\", \"-c\", \"permissions.forge-worker.filesystem={\\\":root\\\"=\\\"deny\\\", \\\":minimal\\\"=\\\"read\\\", \\\"<workspace>\\\"=\\\"read\\\"}\", \"-c\", \"permissions.forge-worker.network.enabled=false\", \"-c\", \"features.apps=false\", \"-c\", \"features.plugins=false\", \"-c\", \"features.hooks=false\", \"-c\", \"features.multi_agent=false\", \"-c\", \"features.browser_use=false\", \"-c\", \"features.browser_use_external=false\", \"-c\", \"features.computer_use=false\", \"-c\", \"features.image_generation=false\", \"-c\", \"features.remote_plugin=false\", \"-c\", \"features.tool_suggest=false\", \"-c\", \"features.view_image=false\", \"-c\", \"features.shell_tool=false\", \"-c\", \"features.unified_exec=false\", \"-\"]",
        "environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER",
        "login: subscription (ChatGPT)"
      ],
      "evidence_refs": [],
      "harness": "codex",
      "harness_version": "codex-cli 0.162.1",
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
      "configuration_digest": "0952a1dca9b7ff5765fac8f2121e99b97aa2bce930524db4b061e9ca569f2876",
      "configured_controls": [
        "command: [\"codex\", \"--no-daemon\", \"exec\", \"--ignore-user-config\", \"--ignore-rules\", \"--skip-git-repo-check\", \"--ephemeral\", \"--json\", \"--color\", \"never\", \"--strict-config\", \"-C\", \"<workspace>\", \"--output-schema\", \"<workspace>/output-schema.json\", \"-c\", \"approval_policy=\\\"never\\\"\", \"-c\", \"project_doc_max_bytes=0\", \"-c\", \"mcp_servers={}\", \"-c\", \"apps._default.enabled=false\", \"-c\", \"web_search=\\\"disabled\\\"\", \"-c\", \"default_permissions=\\\"forge-worker\\\"\", \"-c\", \"permissions.forge-worker.filesystem={\\\":root\\\"=\\\"deny\\\", \\\":minimal\\\"=\\\"read\\\", \\\"<workspace>\\\"=\\\"read\\\"}\", \"-c\", \"permissions.forge-worker.network.enabled=false\", \"-c\", \"features.apps=false\", \"-c\", \"features.plugins=false\", \"-c\", \"features.hooks=false\", \"-c\", \"features.multi_agent=false\", \"-c\", \"features.browser_use=false\", \"-c\", \"features.browser_use_external=false\", \"-c\", \"features.computer_use=false\", \"-c\", \"features.image_generation=false\", \"-c\", \"features.remote_plugin=false\", \"-c\", \"features.tool_suggest=false\", \"-c\", \"features.view_image=false\", \"-\"]",
        "environment names: HOME, LANG, LOGNAME, PATH, TMPDIR, USER",
        "login: subscription (ChatGPT)"
      ],
      "evidence_refs": [],
      "harness": "codex",
      "harness_version": "codex-cli 0.162.1",
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
