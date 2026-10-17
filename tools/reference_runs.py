"""Start and collect plan task 14's reference runs.

    python tools/reference_runs.py start <directory>
        Create the starting repository: a README and the team's existing
        bug-report-format skill in .agents/skills/ with its .claude/skills
        link, which the reference idea can reuse.

    python tools/reference_runs.py collect <result repository> <example directory> --harness <harness>
            --slug <slug> --cases <cases file inside the repository>
        Copy the reference artifacts as the session left them into the
        example directory: .harness/, README.md, the cases file, each
        built or reused skill's directory with its .claude/skills link,
        and a plugin skill's manifests. Nothing else, so a .env file or
        the agent's scratch files stay behind. Then write expected.yaml
        with the labels the report gives and run check_references on it.
        Exit 1 when the checker refuses the example.

Run both with Forge's environment: ../harness-forge/.venv/bin/python.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml

PLAYGROUND = Path(__file__).resolve().parents[1]
FORGE = PLAYGROUND.parent / "harness-forge"
sys.path[:0] = [str(FORGE / "src"), str(PLAYGROUND / "tools")]

import check_references  # noqa: E402
from harness_forge.documents import safe_path  # noqa: E402

EXISTING = "bug-report-format"
EXISTING_SKILL = (f"---\nname: {EXISTING}\ndescription: Formats an incoming bug report with the team's template of "
                  "title, environment, steps, expected and observed behavior. Use when a new bug report arrives. "
                  "Not for triage.\n---\n# Bug report format\n\nRewrite the report under these headings: Title, "
                  "Environment, Steps, Expected, Observed.\n")


def start(root: Path) -> None:
    """The starting repository of the reference runs."""
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise ValueError(f"{root} is not empty")
    (root / "README.md").write_text("# Bug intake\n", encoding="utf-8")
    skill = root / ".agents" / "skills" / EXISTING
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(EXISTING_SKILL, encoding="utf-8")
    (root / ".claude" / "skills").mkdir(parents=True)
    (root / ".claude" / "skills" / EXISTING).symlink_to(f"../../.agents/skills/{EXISTING}")


LINKS = ".claude/skills"


def located(root: Path, relative: str) -> Path:
    """root/relative inside root, through no linked directory; only a skill's own link may itself be a link."""
    parent, _, name = relative.rpartition("/")
    if parent == LINKS and name and name not in (".", ".."):
        return safe_path(root, LINKS) / name
    return safe_path(root, relative)


def artifacts(repository: Path, cases: str) -> list[str]:
    """The paths a reference example keeps, relative to the repository: what Forge reads and binds. A path
    inside another one it keeps is left out, since copying that one copies it."""
    from harness_forge.contracts import load_decision
    from harness_forge.verify import part_kind, plugin_manifests, skill_home

    decisions = sorted((repository / ".harness" / "decisions").glob("*.md"))
    if len(decisions) != 1:
        raise ValueError(f"{repository} needs exactly one decision record, found {len(decisions)}")
    paths = [".harness", "README.md", cases]
    for part in load_decision(decisions[0]).record["parts"]:
        kind = part_kind(part)
        if kind not in ("build", "local-reuse"):
            continue
        directory = f".agents/skills/{part['slug']}" if kind == "build" else part["reuse"]["path"].rstrip("/")
        paths.append(directory)
        link = f".claude/skills/{directory.rsplit('/', 1)[-1]}"
        if (repository / link).is_symlink():
            paths.append(link)
        if skill_home(part) == "plugin":
            paths += [path for path in plugin_manifests(directory) if (repository / path).is_file()]
    kept = [path for path in dict.fromkeys(paths)
            if located(repository, path).exists() or located(repository, path).is_symlink()]
    return [path for path in kept if not any(path.startswith(other + "/") for other in kept if other != path)]


def collect(repository: Path, example: Path, *, harness: str, slug: str, cases: str) -> list[str]:
    """Copy the result into ``example`` with its expected labels; return the checker's problems."""
    if example.exists():
        raise ValueError(f"{example} exists; collect into a new directory")
    if not located(repository, cases).is_file():
        raise ValueError(f"{cases} is not a file in {repository}")
    selected = artifacts(repository, cases)  # every path is checked before anything is written
    example.mkdir(parents=True)
    for relative in selected:
        source, target = located(repository, relative), located(example, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_symlink():
            target.symlink_to(source.readlink())
        elif source.is_dir():
            shutil.copytree(source, target, symlinks=True)
        else:
            shutil.copy2(source, target)
    forge = check_references._forge(FORGE)
    report = (example / ".harness" / "reports" / f"{slug}.md").read_text(encoding="utf-8")
    labels = {part["part_id"]: {"harness_result": part["harness_result"], "goal_result": part["goal_result"]}
              for part in check_references._report_data(report, forge["documents"])["parts"]}
    (example / "expected.yaml").write_text(yaml.safe_dump(
        {"harness": harness, "slug": slug, "cases": cases, "parts": labels}), encoding="utf-8")
    return check_references.check_example(example, forge)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("start").add_argument("directory", type=Path)
    collecting = commands.add_parser("collect")
    collecting.add_argument("repository", type=Path)
    collecting.add_argument("example", type=Path)
    collecting.add_argument("--harness", choices=("claude-code", "codex"), required=True)
    collecting.add_argument("--slug", required=True)
    collecting.add_argument("--cases", required=True, help="the cases file's path inside the repository")
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "start":
            start(arguments.directory)
            return 0
        problems = collect(arguments.repository, arguments.example, harness=arguments.harness,
                           slug=arguments.slug, cases=arguments.cases)
    except (OSError, ValueError) as error:
        print(f"reference_runs.py: {error}", file=sys.stderr)
        return 2
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
