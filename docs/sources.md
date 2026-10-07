# Source policy

Rules for every source cited in `docs/`, and the domains already
assessed against them. Read this before adding, changing or citing a
source, and include these rules in any research or writing brief given
to a subagent.

## Rules

1. **Verify every source.** Fetch the source and check that it says
   what the page cites. A claim whose source could not be fetched or
   does not say it is dropped.
2. **Drop, don't mark.** An unverifiable claim is removed. It is not
   kept with a marker such as "unverified", "secondary only", "from a
   search snippet" or "via mirror".
3. **Primary sources first.** Use the original: vendor documentation or
   source code, a standard or specification, a security advisory, a
   paper, or the first-hand report of the person or company that did the
   work.
4. **Not sources:** mirrors and copies, aggregators and link posts,
   search-result snippets, paper-copy sites, AI-generated summaries,
   news rewrites when the original is available, and vendor marketing
   about a third party.
5. **The X platform (x.com, twitter.com) is not trustworthy.** Drop
   claims that rest on X posts or on copies of them.
6. **Practitioner sources** count only when the author is identifiable,
   the report is first-hand (their own experience or measurement), and
   the page says what is cited. Label them `[Practitioner]`.
7. **Trade press** counts only from established outlets, and only when
   no primary source can be fetched.
8. **Inferences** stay only when they follow directly from sourced facts
   on the same page and are labelled as inference. An inference that
   rests on a dropped claim, or speculates beyond the facts, is removed.
9. **Gaps are allowed.** A statement that something is undocumented or
   unknown is not a claim. It must not repeat an unverified claim.
10. **Numbers and quotes must match the source exactly.** Correct them
    to the source's wording and figures, including dates and versions.
11. **Subagent output is checked before it is committed.** At minimum,
    list the cited domains and check them against the tables below.

## Assessing a new domain

1. Is it the organization that owns the product, standard, data or
   finding? Then it is a primary source.
2. Is it a named person or company reporting their own work? Then it
   is a practitioner source (rule 6).
3. Is it an established outlet reporting on a primary source that
   cannot be fetched? Then it is trade press (rule 7).
4. Anything else is not a source (rule 4). Find the original or drop
   the claim.

Add the domain to the matching table below when a page starts citing
it.

## Trusted domains

Assessed on 2026-10-05; extended on 2026-10-07.

| Category | Domains |
| --- | --- |
| Vendor documentation and repositories | `docs.gitlab.com`, `learn.microsoft.com`, `support.atlassian.com`, `gerrit-review.googlesource.com`, `git-scm.com`, `docs.aws.amazon.com`, `docs.cloud.google.com`, `developer.hashicorp.com`, `docs.semgrep.dev`, `docs.sigstore.dev`, `www.checkov.io`, `google.github.io` (OSV-Scanner), `trivy.dev`, `docs.codecov.com`, `gvisor.dev`, `firecracker-microvm.github.io`, `katacontainers.io`, `containers.dev`, `www.conftest.dev`, `www.openpolicyagent.org`, `open-policy-agent.github.io`, `kyverno.io`; GitHub `actions/*`, `gitleaks/*`, `ossf/*`, `step-security/*`; `code.claude.com`, `platform.claude.com`, `claude.com`, `anthropic.com`, `learn.chatgpt.com`, `developers.openai.com`, `cdn.openai.com`, `chatgpt.com`, `opencode.ai`, `docs.github.com`, `postmarkapp.com`; GitHub `anthropics/*`, `openai/*`, `anomalyco/opencode` |
| Standards and specifications | `slsa.dev`, `www.rfc-editor.org`, `www.icann.org`, `csrc.nist.gov`, `nvlpubs.nist.gov`, `www.nccoe.nist.gov`, `www.cisa.gov`, `www.ncsc.gov.uk`, `saif.google`, `agentskills.io`, `modelcontextprotocol.io`, `agents.md`, `json.schemastore.org`, `owasp.org`, `owasp.github.io`, `genai.owasp.org` |
| Vulnerability databases and advisories | `nvd.nist.gov`, `advisories.gitlab.com`, GitHub security advisories (`github.com/<owner>/<repo>/security/advisories`) |
| Research | `web.mit.edu` (Saltzer and Schroeder), `storage.googleapis.com` (Google research PDFs linked from `research.google`), `arxiv.org`, `iclr.cc`, `research.google`, `ai.meta.com`, `metr.org`, `dora.dev` |
| Security research, first-hand | `labs.zenity.io`, `www.lasso.security`, `blog.gitguardian.com` (its own scan data), `research.checkpoint.com`, `wiz.io`, `invariantlabs.ai`, `snyk.io`, `sentinelone.com`, `stepsecurity.io`, `embracethered.com`, `securitylab.github.com`; GitHub `trailofbits/*` |
| Company engineering blogs, first-hand | `developer.nvidia.com`, `aws.amazon.com`, `blog.cloudflare.com`, `github.blog`, `docs.docker.com`, `vercel.com`, `cognition.com`, `checklyhq.com` |
| Practitioners, first-hand | `simonwillison.net`, `humanlayer.dev`, `mariozechner.at`, `scottspence.com`, `martinfowler.com`; GitHub `obra/superpowers` |
| Trade press (rule 7) | `csoonline.com`, `securityweek.com` |

A trusted domain does not make every page on it a valid source: rule 1
still applies to each claim.

The outside-gates research on 2026-10-07 added forge, cloud, policy
and scanner documentation as primary vendor sources, standards and
government bodies (NIST, CISA, NCSC, ICANN, RFCs, SLSA), and three
first-hand security research sites.

The security pass on 2026-10-05 added GitHub's product documentation and
Security Lab as primary documentation and first-hand research, and
Postmark's own notice about an impersonating package as a first-party
incident source. The assessment concerns those source roles, not every
page published on those domains.

## Rejected domains

Removed from the knowledge base on 2026-10-05.

| Domain | Reason |
| --- | --- |
| `x.com`, `twitter.com` | X platform, not trustworthy (rule 5) |
| `gitea.maison43.duckdns.org` | Personal mirror of an X post |
| `2ooks.github.io`, GitHub `deusyu/harness-engineering`, `habr.com` | Third-party summaries of an OpenAI post that could not be fetched |
| `alphaxiv.org`, `chatpaper.com`, `emergentmind.com` | Paper-copy and summary sites; cite `arxiv.org` |
| `conffab.com` | Link aggregator; cite the original author |
| `codex.danielvaughan.com` | Third-party blog about Codex; cite the official docs |
| `labs.cloudsecurityalliance.org` | Research notes that aggregate third-party figures without verifying them |
| `thehackernews.com`, `infoq.com` | News rewrites; the primary source or an established outlet was used instead |
| `vpncentral.com`, `letsdatascience.com`, `softwareseni.com`, `zenml.io` | Aggregators and content sites |
| `arize.com`, `ai.engineer` | Vendor-reported figures that disagree across the vendor's own material |
| `software-factories.port.io` | Vendor marketing about a third party |
| `goteleport.com`, `paloaltonetworks.com` (blog summaries of OWASP) | Secondary summaries; the OWASP original was used instead |
| `jmason.ie` | Link post; cite the original research |

Example values in configuration snippets (`example.com`, `localhost`,
`127.0.0.1`, `my-org/...`) and schema URLs quoted as part of a file
format are not citations.
