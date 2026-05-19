# AGENTS.md — {{project_name}}

> **Single living reference for AI agents working on this
> repository.** Read top-to-bottom on first entry; skim or jump on
> later sessions. This repository runs the **Cairn** methodology —
> a human + AI development method built on recorded, reviewed
> deliberation.

<!-- cairn:slot project-overview -->
(One or two paragraphs: what {{project_name}} is, what it does, and
who it is for. The bootstrap drafts this from the Project Profile;
the maintainer confirms it. An unfilled slot at first release is a
review finding.)
<!-- cairn:end project-overview -->

## How this project is built

Work on {{project_name}} is **deliberated, reviewed, and
recorded**. A substantive change does not land because its author
is confident; it lands because it went through a proposal, was
reviewed across structural independence, and the reasoning is
committed to the durable record. The coordination space is the
`dev/` tree:

* [`dev/README.md`](dev/README.md) — the entry point to the `dev/`
  tree.
* [`dev/collaboration_agreement.md`](dev/collaboration_agreement.md)
  — the working norms and decision rights.
* [`dev/agent_collaboration.md`](dev/agent_collaboration.md) — the
  roles, the review loop, and the coordination doctrine in full.

This file (`AGENTS.md`) is the **operational** reference — the
rules an agent must follow to make a correct change. The `dev/`
docs carry the deeper *why*.

## The lifecycle

A substantive change — a new abstraction, a cross-cutting
refactor, a contract change, anything worth a second opinion —
goes through a **proposal**:

```
proposed -> reviewed -> revised -> accepted / rejected / superseded
```

A non-trivial accepted proposal then gets a **plan**
(`open -> executing -> review -> archived`). Two rules are
bright-line:

* **Append-only.** Never edit a prior section of a proposal —
  append a revising one. The record shows what was believed *at
  each point*, not a tidied final state.
* **One commit per lifecycle transition.** Open, review, response,
  and decision each get their own commit; bundling hides who
  changed what.

The full lifecycle, the trivial-vs-non-trivial triage, and the
file-move rules are in
[`dev/proposals/_template.md`](dev/proposals/_template.md) and
[`dev/plans/_template.md`](dev/plans/_template.md).

## Review

Every substantive change is reviewed (see
`dev/agent_collaboration.md`):

* **Internal review** helps a change land — a constructive second
  read. Floor: the same agent in a fresh session.
* **External review** makes a change prove it should land — an
  independent read. Floor: a different agent type, or a human.

Review is asynchronous and commit-mediated: a review is a section
appended to the artifact and committed, not a conversation that
leaves no record.

## Session routines

* **Session start** — at a cold start, or after a context-loss
  event, run a short orientation pass: re-anchor on the `dev/`
  tree, read the commit log since the last handoff, note in-flight
  proposals, and confirm your role before substantive work.
* **Goodnight** — at the end of a session, leave a clean handoff:
  a status summary, a per-agent reflection, and (for the
  designated owner) a scrub of the roadmap boards. Committing and
  pushing are never implied by the routine — they wait on explicit
  maintainer approval.

## Roles

Work is organized by **roles**, not people — a role is a frame.
The **Human Maintainer** holds final Decision authority and is the
one role that is not interchangeable. Other roles (Strategy,
Implementation, the reviewer tiers, and any the dimensional
profile adds) are frames any capable agent fills; name your role
before substantive work, and if it is not explicit, ask. The
roster is in `dev/agent_collaboration.md`.

## Git and commit workflow

* **Never commit or push without explicit maintainer approval.**
  Show what changed first. *Exception:* a proposal-lifecycle
  commit that touches only `dev/proposals/` files may proceed
  directly — those are append-only deliberation artifacts.
  Pushing always needs approval.
* **Commit with explicit paths** — `git commit <path> ...`, never
  a bare `git commit`. The staged index is shared; a path-scoped
  commit cannot absorb another agent's staged work.
* **Shared communication files** — the roadmap boards and the
  changelog — are edited only at defined serialization points (a
  lifecycle archive, the goodnight routine, explicit instruction).
  Refer to proposals and plans by filename stem, not path link.
* Run the test suite after any substantive change:
  `{{test_command}}`.

## Project-specific conventions

<!-- cairn:slot project-conventions -->
(Naming conventions, the development environment, the high-risk
surfaces, and the operational pitfalls specific to {{project_name}}.
This is judgment work: a reasoning agent and the maintainer write
the project's *real* conventions here — it is not a mechanical
fill. An empty slot at first release is a review finding.)
<!-- cairn:end project-conventions -->

## Vendor addendum

`AGENTS.md` is vendor-neutral — it names no specific AI agent tool.
Doctrine specific to one agent tool (a harness path, a
session-model habit) goes in that tool's own file, which opens by
importing this one, so the shared content stays single-sourced.
