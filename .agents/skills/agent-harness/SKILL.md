---
name: agent-harness
description: Answers questions about, and sets up or reviews, the configuration of coding-agent harnesses (Claude Code, Codex, OpenCode) using this repository's researched knowledge base. Covers instruction files (AGENTS.md, CLAUDE.md), settings, permissions and sandbox, MCP servers, skills, slash commands, subagents, hooks, plugins and marketplaces, and headless or CI automation. Use when configuring, reviewing, comparing or porting any of these, or when asked how a harness feature works or what the best practice is.
---

# Agent harness

## Scope

Harness configuration questions and changes: how a feature works in
Claude Code, Codex or OpenCode, how the concepts compare, which
mechanism fits a goal, and what good practice is. The knowledge base in
`docs/` is the source. This skill says which page to read and how far
to trust it.

Not for using a harness to do ordinary coding work, and not for
questions about models themselves (pricing, model choice).

## The knowledge base

An overview page plus four layers, one page per concept in each. Page
names are identical across layers, so `<concept>` below is one of: `instructions`,
`configuration`, `permissions-and-sandbox`, `mcp`, `skills`,
`commands`, `subagents`, `hooks`, `plugins`, `automation`.

| Need | Read |
| --- | --- |
| Which concept fits a goal, and when a concept is the wrong choice | `docs/overview.md` |
| One concept end to end in condensed form: model, when to use and when not, key practices, security, checklist, portability | `docs/guide/<concept>.md` |
| How the concept works in general, how the harnesses compare, how to write one setup for several harnesses | `docs/concepts/<concept>.md` |
| Exact file names, fields, defaults and flags for one harness | `docs/vendors/<harness>/<concept>.md` (`claude-code`, `codex`, `opencode`) |
| Which approach to choose, how to do it well, security, verification, review checklist | `docs/best-practices/<concept>.md` (no `commands` page; commands are covered in `skills`) |
| Detail a page lacks, or the source behind a claim | `docs/research-notes/` |

Concept pages end with "Dropped from the generalization": features only
one harness has. Check it before calling something portable.

## Procedure

1. **Name the concepts and harnesses involved.** A goal like "stop the
   agent from touching `.env`" spans several concepts; `docs/overview.md`
   says which concept fits and which one is the wrong choice.
2. **Read the slice you need.** Pages run up to 500 lines. List a
   page's headings first and read the sections that answer the
   question. Read the vendor page when exact syntax matters.
3. **Check freshness.** The knowledge base was researched on 2026-10-04
   against Claude Code 2.1.289, codex-cli 0.159.2 and OpenCode 1.18.34.
   These harnesses change every few weeks. When an answer or a change
   depends on a specific field, flag, default or path, compare the
   installed version (`claude --version`, `codex --version`) and
   confirm the detail against the source the page cites or the CLI's
   `--help`. Say so when it could not be confirmed.
4. **Prefer the portable form** described on the concept page unless
   the user targets one harness: `AGENTS.md` as the shared instruction
   file, skills in `.agents/skills/` with a symlink from
   `.claude/skills/`, and hook events and decisions that both Claude
   Code and Codex share.
5. **For a review**, walk the checklist at the end of the matching
   best-practices page and report each item that fails, with the page
   section that explains it.
6. **Keep the knowledge base current.** When a fact turns out to be
   outdated or wrong, fix the vendor page with the new source and date,
   then every page that repeats it (`docs/concepts/`,
   `docs/best-practices/`, `docs/guide/`, `docs/overview.md`). Mention
   the update in the answer.

## Done when

- Every claim in the answer or change traces to a knowledge-base page
  or to a source checked in this session, and the answer names the
  pages it relied on.
- Version-sensitive details are either confirmed or marked
  unconfirmed.
- A recommendation that rests on practitioner opinion or a single
  study says so, using the evidence label from the best-practices page.

## Naming rule for new files

Name subagent material `subagents.md`. A file called `agents.md` or
`claude.md` in any directory loads as an instruction file on a
case-insensitive file system, in all three harnesses.
