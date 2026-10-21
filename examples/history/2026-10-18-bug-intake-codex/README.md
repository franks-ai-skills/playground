# Bug intake in Codex: the first reference run

The Codex result of task 14's reference session as it was collected on
2026-10-18, unchanged: Forge `7cd81c6`, codex-cli 0.162.1.
[`../../bug-intake/`](../../bug-intake/) describes how the session was
run. `codex/` is not a checked reference run any more:
`examples/bug-intake/codex/` replaced it on 2026-10-21.

B and C were not verified here. A `$name` invocation injects the skill
without a stream event, so their explicit cases passed only when the
model also read `SKILL.md`. In this closing review it did not.
