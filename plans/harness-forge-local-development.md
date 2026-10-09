# Harness Forge: local development account setup

Scope: temporary development on the owner's current machine only.
User clarification: 2026-10-09. Every subsequent agent must preserve
the distinction below when implementing or testing Forge.

## Public product

Use the standard `claude` and `codex` executables with the user's existing
login and vendor-default account locations. No personal alias, shell
function, profile path or plugin is a product requirement. Do not require
a separate login/profile, copy credentials, initiate login or logout,
switch accounts, or edit saved user configuration. A missing login makes
the run unavailable. An API-key or unknown login type gets a cost warning
and a continue/stop question; Forge never adds an API key or falls back
to another account. Development on this machine stays subscription-only.

Apply Forge's temporary per-worker tool, sandbox and discovery restrictions
without changing that account assumption. Record remaining gaps under
`best-effort-v1`; vendor-default account access does not mean unrestricted
worker tools. A dedicated worker profile is an optional operator precaution,
not a prerequisite or proof of credential isolation.

## This machine only

Local Forge development uses the `claude-frank` account. Start every
local Forge run, test or probe with `CLAUDE_CONFIG_DIR=$HOME/.claude-frank`
set; Forge passes the variable through to its workers and its login-type
check. Never use or change `~/.claude`: the owner switches that default
login as needed, normally to the `claude-tp` work subscription.

Before a local run, check read-only that the profile is logged in with
the expected account: `CLAUDE_CONFIG_DIR=$HOME/.claude-frank claude auth
status`. If it is not, stop and report it. Do not run the `.zshrc`
function `claude-frank` from automation: it can log out or start a login
when the account differs. Do not source `.zshrc`, copy the profile or put
this setup into product defaults, examples or fixtures.

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
