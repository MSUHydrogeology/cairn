# Agent collaboration — {{project_name}}

This file is the **process doctrine** for {{project_name}}'s human
+ AI team: the role roster, the review loop, and the coordination
mechanics. `AGENTS.md` carries the operational rules and points
here for the deeper *why*; the working norms are in
`collaboration_agreement.md`.

## Team roles

A **role** is a frame — a stance and a kind of output — not a
person. One agent fills several roles across a session; the role
is named before substantive work, and switching roles is explicit.

* **Human Maintainer** — holds product direction, priorities, and
  final Decision authority. Not interchangeable.
* **Strategy** — surveys the landscape, frames problems, drafts
  proposals.
* **Implementation** — carries an accepted proposal through its
  plan: the code, the tests, the docs.
* **Internal Reviewer** — the constructive second read.
* **External Reviewer** — the independent, make-it-prove-itself
  read.

<!-- cairn:slot role-roster-additions -->
(Dimension-selected roles — a User Agent, a Security reviewer,
domain-specialized agents, a Legacy Agent — are added here when
the project's profile selects them. A minimal team runs the
maintainer plus one generalist agent and adds none.)
<!-- cairn:end role-roster-additions -->

## The review loop

A substantive change moves `proposed -> reviewed -> revised ->
accepted` (see `proposals/_template.md`). Review has two tiers:

* **Internal review** helps a change land — a constructive second
  read. Floor: the same agent type in a fresh session —
  independence by *time*, the mental model rebuilt from the
  artifacts.
* **External review** makes a change prove it should land — an
  independent read. Floor: a different agent type, or a human —
  independence by *structure*, a genuinely different set of
  failure modes.

Code review — the implementation-side pass, before a plan archives
— has its own floor: **not the implementing agent**.

Reviews are **asynchronous and commit-mediated**: a review is a
dated, attributed section appended to the artifact and committed.
No agent writes or commits a review attributed to another agent —
the named reviewer commits their own findings, or the maintainer
does.

## Coordination

The team coordinates **stigmergically** — through the persistent
`dev/` tree, not by message-passing. The durable record is the
source of truth, and it survives context loss and contributor
handoff.

The baseline coordination discipline — always on — guards the
shared surfaces:

* **Shared communication files** (`PLANNING.md`, `NEXT_SESSION.md`,
  and the changelog) are edited only at defined serialization
  points, and reference proposals / plans by filename stem rather
  than path link.
* **The staged git index is shared.** Commit with explicit paths
  (`git commit <path> ...`), never a bare `git commit`; a
  path-scoped commit cannot absorb another agent's staged work.

<!-- cairn:slot coordination-additions -->
(Higher coordination tiers — a pre-edit work-intent convention, a
real-time typed-event channel — are added for concurrent and
high-concurrency teams; see the Agent-team axis in `dimensions/`.
A sequential team runs only the baseline above.)
<!-- cairn:end coordination-additions -->

## Session reflections and handoff

If the `reflections` default-on module is installed (the typical
multi-agent adoption keeps it), the goodnight routine writes a
short, per-agent retrospective — the cross-agent handoff surface
that lets the next session pick up each agent's experience.

A solo, single-agent project may keep reflections as a personal
log or omit the channel entirely; the cross-agent handoff function
only earns its keep with a multi-agent team. See
`modules/default-on/reflections.md` for the module's full content.
