# Outside gates: research notes

Researched and sources fetched on 2026-10-07. These notes cover
controls outside the agent harness ("outside gates") that can enforce
a rule when the agent errs, is prompt-injected, or has its
configuration changed by a pull request. They back the condensed
[outside-gates guide](../../guide/outside-gates.md) and the outside
control recommendations in the
[harness-forge design](../../../specs/2026-10-06-harness-forge-design.md).

Scope: general concepts that work on any platform. Products and
platform features appear only as examples. Each note records, per
claim, the source URL and a verbatim quote, and labels practitioner
sources and inferences.

| Note | Covers |
| --- | --- |
| [merge-and-ci.md](merge-and-ci.md) | Protected branches and rulesets, approvals and code owners, author/approver separation, required checks, merge queues, signing, server-side push rules, deployment environments |
| [code-analysis.md](code-analysis.md) | SAST, SCA, secret scanning and push protection, IaC scanning, license checks, SBOM and provenance, coverage gates, package hallucination |
| [identity-and-credentials.md](identity-and-credentials.md) | Agent identity, scoped and short-lived tokens, OIDC federation, just-in-time elevation, permission ceilings, separation of duties, break-glass, audit |
| [network-and-dns.md](network-and-dns.md) | Egress allowlists and DNS filtering, DNS exfiltration, CI-runner and dev-container egress, hosted agents' network limits; protecting domains and DNS records |
| [isolation-and-policy.md](isolation-and-policy.md) | Containers, gVisor, VMs and microVMs, hosted sandboxes, policy-as-code at CI, IaC, admission and cloud API, resource and cost limits, recovery and DLP |
| [selection-framework.md](selection-framework.md) | Authoritative guidance on enforcing outside the model, control taxonomy, decision criteria and intake questions, incidents |

## Gaps

- No fetchable primary postmortem shows an outside gate stopping a
  coding agent's harmful action.
- CISA's joint AI deployment guidance could not be fetched. NIST's
  agent-identity work is a draft concept paper.
- Not covered: GitLab push-rule details, Dependabot and Renovate,
  GitHub Enterprise Server and Bitbucket Data Center variants, measured
  review or CI friction for agent pull requests, false-positive rates,
  isolation escape rates.
- The Codex cloud internet-access page is labelled "Legacy"; its
  details may be superseded.

## Dropped claims

Removed under the [source policy](../../sources.md): a vendor article
restating a package-hallucination study (the study is cited instead), a
secret-leak figure not present in the fetched page, a changelog claim
seen only as a search-result title, and agent incidents that rest on X
posts.

## Knowledge-base check

The isolation research could not confirm the guide's statement that
Codex names Docker as acceptable isolation for `--yolo`. A re-fetch on
2026-10-07 confirmed it: Codex's security page says to "configure your
Docker container to provide the isolation you need" and to "let Docker
provide the outer isolation boundary"
([Codex agent approvals & security](https://learn.chatgpt.com/codex/agent-approvals-security)).
The guide line now cites that page.
