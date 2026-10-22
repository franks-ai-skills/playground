# Requirements

Accepted for this skill (Idea KB revision sha256 58d06ee37346a063060acbac891c898a1183b960dca472376329769d4aec6a91). Forge's
verification checks the skill against each one. Numbers match the
requirements in SKILL.md; each line gives the rule id, its kind and its
sources.

1. `idea.bug-report-lifecycle.d.real-or-flaky` (must): https://github.blog/2020-12-16-reducing-flaky-builds-by-18x, https://martinfowler.com/articles/nonDeterminism.html
2. `idea.bug-report-lifecycle.d.flaky-source` (should): https://martinfowler.com/articles/nonDeterminism.html
3. `idea.bug-report-lifecycle.d.rerun-as-proof` (must not): https://github.blog/2020-12-16-reducing-flaky-builds-by-18x
4. `idea.bug-report-lifecycle.d.secret-quoting` (must not): https://docs.github.com/en/actions/concepts/security/secrets
5. `idea.bug-report-lifecycle.d.content-as-data` (must not): https://genai.owasp.org/llmrisk/llm01-prompt-injection/
6. `idea.bug-report-lifecycle.d.no-push` (must not): https://genai.owasp.org/llmrisk/llm01-prompt-injection/
