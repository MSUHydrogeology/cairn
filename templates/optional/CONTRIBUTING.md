# Contributing to {{project_name}}

Welcome — this project is built by a **human + AI team** running the
**Cairn** methodology: changes are deliberated, reviewed, and recorded
in the `dev/` tree before they
land. This file is the **human contributor's entry point**. It carries
the shared workflow at a glance and points to the deeper references
rather than restating them, so there is a single source for each rule.

> **Single-source rule.** The operational detail — the development
> environment, the test command, naming conventions, the commit and
> review workflow — lives in `AGENTS.md` and the `dev/` docs, which the
> AI team also reads. This file *links* to them; it does not copy them.
> If you find yourself duplicating a rule here, link instead.

## Start here

* **`AGENTS.md`** (repo root) — the operational reference: required
  reading, the development environment and test command, project
  conventions, and the git / commit workflow. Read it first; it applies
  to human and AI contributors alike.
* **`dev/README.md`** — the entry point to the `dev/` coordination tree
  (the method: proposals, plans, reviews).
* **`dev/agent_collaboration.md`** — the team roles, review loop and
  coordination guidance.

## How a change lands

A substantive change is **deliberated, reviewed, and recorded** — it
lands because it went through a proposal, was reviewed by an independent
reviewer beside its author, and the reasoning is committed to the durable
record, not because its author was confident. The lifecycle
(`proposed → reviewed → revised → accepted`, then a plan for
non-trivial work) is in `dev/proposals/_template.md` and
`dev/plans/_template.md`. A small fix can skip the ceremony per the
triage rule there.

Two bright-line rules: **deliberation artifacts are append-only** (you
revise by appending, never by editing a prior section), and **one
commit per lifecycle transition**.

## Working norms

<!-- cairn:slot contributing-specifics -->
(Project-specific contributor guidance goes here: how to get the
development environment running, how to run the tests, the
branch/PR/issue conventions, and anything a new human contributor needs
before their first change. Keep shared rules as *links* to `AGENTS.md`
and the `dev/` docs — do not duplicate them. An empty slot at first
release is a review finding.)
<!-- cairn:end contributing-specifics -->

## Code of conduct and review

Every substantive change is reviewed by a fresh reviewer who did not write
it: they question its foundations and answer in writing
(`dev/agent_collaboration.md`). The Maintainer may ask for more distance on
one named piece of work. Reviews are asynchronous and commit-mediated: a
review is a dated, attributed section appended to the artifact, not a
conversation that leaves no record. Engage as a **collaborative skeptic** — steelman a position
before critiquing it, and treat disagreement as a way to improve the
change.
