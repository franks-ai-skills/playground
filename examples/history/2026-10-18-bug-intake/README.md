# Bug intake: the owner's first live session

The owner ran Harness Forge by hand in Claude Code on 2026-10-18, from
the starting repository `tools/reference_runs.py start` creates and the
idea "Handle incoming bug reports from intake to closing", with their own
picture of the workflow instead of the runbook's six parts. `claude-code/`
holds the result as `tools/reference_runs.py collect` copies it. The
runtime cases were in the session's scratch directory; they are added as
`.harness/cases.yaml`, which no report digest binds.

The session ran Forge `7c7272d`, installed as the plugin from GitHub,
with the KB pinned at `ec829ae`, on Claude Code 2.1.302 with a
subscription login and the account's default model.

| Part | Mechanism | Outcome | Harness result | Goal result |
| --- | --- | --- | --- | --- |
| A intake | hook | outside-alongside | not applicable | not assessed |
| B reproduce | skill | harness-only | not verified | not met |
| C fix-and-pr | user-invoked skill | outside-alongside | not verified | not met |
| D no CI workarounds | hook | outside-alongside | not applicable | not assessed |
| E merge when green | none | outside-instead | not applicable | depends on outside controls |
| F close-and-label | skill | harness-only | not verified | not met |
| G untrusted reports | permissions and sandbox | outside-alongside | not applicable | not assessed |

The reviewer judged every built part's goal met. The parts are not
verified because:

- B and F post to GitHub and the model can start them, which fails
  `skills.invocation.side-effects-user-invoked`. Intake recommended
  "does not publish" for both; the owner kept the model trigger after
  verification showed the error.
- B links to A, a hook this release cannot build, so `links.parts`
  cannot check the link. The agent recorded the link without asking.
- C's explicit case asked in prose for the skill, which the model cannot
  start: `runtime.explicit-activation` failed.

`tools/check_references.py` accepts the example as a true report. It is
not a task 14 reference run: it has no local or remote reuse, no
nothing-fits part, no break/fix with a Review and no verified part.

## Fixed after this session

- Forge runs a user-invoked skill's explicit case as `/<name>` in
  Claude Code and `$<name>` in Codex.
- `prepare-contract` refuses a part whose recorded selection `build`
  would refuse, such as a control the goal needs recorded as a
  precaution. In this session that refusal came only at C's build and
  cost a third contract confirmation.
- harness-intake states controls the goal needs instead of asking, asks
  before recording a link between parts, and warns before the trigger
  question that a model-started skill with side effects fails
  verification.
