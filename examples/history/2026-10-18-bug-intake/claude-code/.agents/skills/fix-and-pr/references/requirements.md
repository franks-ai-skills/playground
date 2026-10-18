# Requirements

Accepted for this skill (Idea KB revision sha256 e1805692c07794fb076d85404a8ce1d99581b7ad56af5cabea3935af53c2acde). Forge's
verification checks the skill against each one. Numbers match the
requirements in SKILL.md; each line gives the rule id, its kind and its
sources.

1. `idea.bug-intake.c.closing-keyword` (must): https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
2. `idea.bug-intake.c.regression-test` (must): https://google.github.io/eng-practices/review/developer/small-cls.html
3. `idea.bug-intake.c.ci-workaround` (must not): https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
4. `idea.bug-intake.c.pwn-request` (must not): https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/
5. `idea.bug-intake.c.self-merge` (must not): https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
6. `idea.bug-intake.c.green-before-done` (must): https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
