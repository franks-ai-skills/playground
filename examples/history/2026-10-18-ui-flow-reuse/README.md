# UI flow testing: a remote reuse

Task 14's remote reuse, one session per harness, run the way
[`../2026-10-21-bug-intake/`](../2026-10-21-bug-intake/README.md) describes: Claude Opus 5.5
played the user at the owner's request, Forge `7cd81c6`, KB `ec829ae`.

The idea is "Test our web app's UI flows locally in a browser" in a
fictional team's repository with only a README. Its one part reuses
`webapp-testing` from
[`anthropics/skills`](https://github.com/anthropics/skills/tree/main/skills/webapp-testing)
(Apache-2.0) unchanged. Both surveys found it. The skill gives no
pass or fail per flow, so the user narrowed the part's goal to what it
does: drive the local app in a real browser and capture screenshots and
console logs, with the developer judging the result.

The skill is not installed, so its home stays open and the part is
`not checked` / `not assessed` in both harnesses. Nothing is built, so
no runtime cases exist and `expected.yaml` names none.

Moved here from `examples/ui-flow-reuse/` on 2026-10-22, with the bug
intake runs; their README says why and how both replay against Forge
`80244fd`.
