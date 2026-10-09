# Harness Forge: local development account setup

Scope: temporary development on the owner's current machine only.
User clarification: 2026-10-09. Every subsequent agent must preserve
the distinction below when implementing or testing Forge.

## Public product

Use the standard `claude` and `codex` executables with the user's existing
subscription login and vendor-default account locations. No personal
alias, shell function, profile path or plugin is a product requirement.
Do not require a separate login/profile, copy credentials, initiate login
or logout, switch accounts, or edit saved user configuration. A missing
usable subscription login makes the run unavailable; there is no API-key,
API-credit or alternate-account fallback.

Apply Forge's temporary per-worker tool, sandbox and discovery restrictions
without changing that account assumption. Record remaining gaps under
`best-effort-v1`; vendor-default account access does not mean unrestricted
worker tools. A dedicated worker profile is an optional operator precaution,
not a prerequisite or proof of credential isolation.

## This machine only

The owner's selected Claude account is the one associated with
`claude-frank` and `~/.claude-frank`. The `.zshrc` function can change
login state, so do not invoke it unguarded from automation. Use only a
local development launch configuration that selects the existing account
without login/logout side effects. Do not source the whole `.zshrc`,
copy the profile or export this machine's setup into product defaults.
If the selected login is unusable, report that instead of switching it.

`claude-tp` was authorized only for the completed diagnostic. That
exception is not renewed. Keep the existing Codex subscription account;
do not change its home directory or login to create test isolation.
Local launch settings remain outside distributed code, examples and
fixtures. Record only non-secret launch metadata in development evidence.

Earlier diagnostic reports name personal profiles to explain their
observations. Those observations do not establish public installation
support or transfer to other accounts. Validate public behavior against
the standard CLI/account contract as well as local development runs.
Disposable candidate-test environments remain required; their fixture
credentials must never become a model API fallback. Live model access
still needs the existing subscription, with its exposure documented.
