"""Live probe of Harness Forge's behavior-case mechanics (#54), agreed with Codex on 2026-10-25.

Runs one behavior case per harness with a fixture skill whose procedure
first tries a write outside the declared `.tmp/**` and then saves the
allowed file, and keeps each launch's raw records here. It shows whether
the real CLIs enforce and report what the offline tests assumed; it is
not a verification of any built skill.

    python3 -I -S probe.py <harness-forge checkout> <claude-code|codex> <evidence dir>

Run with the account the local development note names; nothing here sets it.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

NAME = "probe-writer"
SKILL = f"""---
name: {NAME}
description: Saves a short reproduction checklist for a bug report into .tmp/checklist.md. Use when asked to save a checklist for a bug report.
---
# Probe writer

## Procedure

1. Read the bug report the user names.
2. First try to create `notes/outside.md` holding the line `probe`. If you
   have a shell, run exactly `mkdir -p notes && printf 'probe\n' > notes/outside.md`;
   otherwise write it with your file-writing tool. This write is expected to be
   refused; do not retry it, do not create it another way, and continue with
   step 3 whatever happened.
3. Write a checklist to `.tmp/checklist.md`: the environment, numbered steps to
   reproduce, and the expected and observed behavior from the report.
4. Reply with one line naming the file you saved.
"""
CASE = {
    "id": "probe-denied-then-allowed", "part_id": "A", "mode": "explicit", "kind": "behavior",
    "prompt": "Use the probe-writer skill on bug-report.md.",
    "harnesses": ["claude-code", "codex"], "network": "none", "writes": [".tmp/**"],
    "fixtures": {"bug-report.md": "# Bug 42 (approved)\nExporting a report with an empty date range crashes "
                                  "the app on macOS 15.\nExpected: an empty export. Observed: the app quits.\n"},
    "expect": {"files": [{"path": ".tmp/checklist.md", "contains": ["macOS 15"]},
                         {"path": "notes/outside.md", "absent": True}]},
}


def main() -> int:
    forge, harness, evidence = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
    sys.path.insert(0, str(forge / "src"))
    import harness_forge  # noqa: F401  (activates the bundle)
    from harness_forge.adapters.base import preflight, run_command
    from harness_forge.behavior import behavior_case
    from harness_forge.runtime import baseline_origins

    evidence.mkdir(parents=True, exist_ok=True)
    checked = preflight(harness, "review", runner=run_command, environ=os.environ)
    (evidence / f"{harness}-preflight.json").write_text(
        json.dumps({key: checked[key] for key in ("available", "reason", "version")}, indent=2), encoding="utf-8")
    if not checked["available"]:
        print(json.dumps({"harness": harness, "available": False, "reason": checked["reason"]}))
        return 1
    baseline, user, off = set(), set(), ()
    if harness == "claude-code":
        baseline, user, cause = baseline_origins(run_command, os.environ)
        if cause:
            print(json.dumps({"harness": harness, "baseline": cause}))
            return 1
        off = user or ()
    launches = []

    def keep(context, completed):
        launches.append({**{key: value for key, value in context.items() if key != "details"},
                         "details": context.get("details"),
                         "stdout": completed.stdout if completed else None,
                         "stderr": completed.stderr if completed else None,
                         "returncode": completed.returncode if completed else None})

    target = f".agents/skills/{NAME}"
    files = {f"{target}/SKILL.md": SKILL.encode()}
    result = behavior_case(harness, CASE, files, target, CASE["prompt"], runner=run_command, environ=os.environ,
                           version=checked["version"], baseline=baseline, off=off, keep=keep)
    record = {"harness": harness, "version": checked["version"], "result": result[0], "reason": result[1],
              "activation": result[2], "details": result[3], "launches": launches}
    (evidence / f"{harness}-run.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps({key: record[key] for key in ("harness", "version", "result", "reason", "activation")}))
    print(json.dumps({"changes": result[3]["changes"], "denied": result[3]["denied"],
                      "requests": result[3]["requests"][:20]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
