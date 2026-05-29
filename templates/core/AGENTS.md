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
`dev/` tree — a tree of git-committed files, which makes the
method **model-agnostic**: this project can mix or swap AI vendors
(or run a local open-weights model) without changing the
coordination layer.

* [`dev/README.md`](dev/README.md) — the entry point to the `dev/`
  tree.
* [`dev/collaboration_agreement.md`](dev/collaboration_agreement.md)
  — the working norms and decision rights.
* [`dev/agent_collaboration.md`](dev/agent_collaboration.md) — the
  roles, the review loop, and the coordination doctrine in full.

This file (`AGENTS.md`) is the **operational** reference — the
rules an agent must follow to make a correct change. The `dev/`
docs carry the deeper *why*. Which file a given rule belongs in —
and the discipline that keeps this file's operational-safety content
a compact imperative rather than a process manual — is the
**doc-governance** routing rule (`doctrine/doc-governance.md`):
build-the-software and operate-safely rules live here; the
deliberation and decision process lives in
`dev/agent_collaboration.md`; each rule has one canonical home and
the other file only points.

**Where `doctrine/` references resolve.** Throughout this file and the
`dev/` tree, a reference to a `doctrine/<name>.md` file points to **Cairn's
published methodology doctrine** — the repository you adopted from — **not
a file in your own tree**. The bootstrap installs your `AGENTS.md` + `dev/`
tree and the modules you selected, *not* Cairn's `doctrine/` directory; the
doctrine is the shared methodology you consult in the Cairn repository (or
its docs). So such a reference is a citation, never a broken local link.

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
  Show what changed first.  Pushing always needs approval.

  **Exception: proposal-, plan-, strategy-doc-, upstream-ledger-,
  and goodnight-handoff commits may proceed without per-commit
  approval.**  Commits that touch ONLY files under `dev/proposals/`,
  `dev/plans/`, `dev/strategy/`, or `dev/.cairn/` (and any
  combination) are deliberation / planning / strategy /
  upstream-coordination artifacts.  The goodnight handoff commit is
  a fifth covered shape, bundling the routine's end-of-session
  artifacts.  Covered actions:

  * **`dev/proposals/`** — opening a proposal, appending a
    Review, appending a Response, flipping status fields
    (`proposed` → `reviewed` → `revised` → `accepted` /
    `rejected` / `superseded`).
  * **`dev/plans/`** — opening a plan, appending plan-reviews /
    responses / sharpening notes, archiving a plan.  **Not
    covered**: chunk-implementing commits that ship code — those
    bundle with non-lifecycle files and the bundling-loses-
    exception rule below catches them automatically.
  * **`dev/strategy/`** — opening a strategy doc, iterative
    revisions, archiving a strategy doc when adopted /
    superseded / retired.
  * **the upstream fold-back ledger** in `dev/.cairn/` (e.g.
    `dev/.cairn/cairn_foldback.md`) — adding entries, updating
    entry status, removing landed entries.  An **agent-maintained
    coordination log** — written by agents and the fold-back tooling,
    *not* a human-deliberation surface; it earns the carve-in because
    agents maintain it and its integrity is the current-state-index
    hygiene rule, not review.  Scoped to the ledger file(s): the rest
    of `dev/.cairn/` is auto-managed machinery state (e.g. the
    onboarding-activation log), not covered here.
  * **The one-line `dev/PLANNING.md` row movement** that is the
    natural serialization point of a lifecycle-transition commit
    (proposal-open, plan-open, proposal-supersession, plan-archive)
    — a bounded carve-in to the bundling-loses-exception guard-rail
    below: the single row-move rides with its transition without
    re-triggering the gate.
  * **The goodnight handoff commit** — the full-handoff owner's
    end-of-session commit, bundling the routine artifacts:
    rewrite of `dev/NEXT_SESSION.md`, end-of-day scrub of
    `dev/PLANNING.md`, `CHANGELOG.md` additions per significant
    commit landed today, and intent-hygiene pruning of any
    intent-ledger file.  Lands as one "End-of-day handoff + doc
    refresh" commit per `doctrine/session-routines.md` >
    *Goodnight*.

  These artifacts don't ship code; their integrity comes from
  the friendly-adversary review system (proposals + plans), the
  iterative-revision review cycle (strategy docs), or the
  single-writer + once-per-day shape of the goodnight handoff.
  Three guard-rails on the exception:

  * **Pushing still requires explicit approval.**  The
    exception covers `git commit` only.
  * **The Decision commit is the Maintainer's** — see the
    scribing rules below; absent explicit unambiguous (or
    confirmed) Maintainer instruction, no agent lands a
    Decision commit.
  * **Bundling with non-lifecycle work loses the exception.**
    A commit that touches a covered lifecycle file AND a file
    outside the covered directories (code, `docs/`, `AGENTS.md`,
    etc.) falls back to the default "explicit maintainer
    approval" rule.  The goodnight-handoff bullet above lists the
    files that bundle is allowed to touch — anything beyond that
    set re-triggers the gate.  The sole standing carve-in is the
    one-line `dev/PLANNING.md` row movement named above, which
    rides with its lifecycle transition; `dev/PLANNING.md` edits
    *beyond* that single row movement re-trigger the gate.
* **Scribing a Decision — the guard-rail.** The Maintainer's Decision
  (accept / reject / supersede) is theirs to land; an
  explicitly-instructed agent may *scribe and commit* it, bounded by
  three rules:
  * **Attribution — quote the authorization verbatim.** Quote the
    Maintainer's authorizing phrase(s) **verbatim and visually
    isolated** in both the `## Decision` block and the commit body. Do
    **not** paraphrase the authorization itself — paraphrase admits
    semantic drift, condition-softening, or a hallucinated approval.
    Surrounding explanatory prose is allowed, but clearly separated
    from the quoted words, so a reader can tell exactly what was
    authorized.
  * **Unambiguous instruction, or confirm.** Act only on an instruction
    unambiguous on *both* the disposition and the commit; if either is
    unclear, confirm with the Maintainer before scribing.
  * **Decision-only commit.** Flip the status and append the Decision
    section, and nothing else — no implementation, plan-open, archive,
    or roadmap work rides in a scribed Decision commit.

  Absent an explicit, unambiguous (or confirmed) instruction, no agent
  lands a Decision commit.
* **Commit with explicit paths** — `git commit <path> [<path> ...]`,
  naming exactly the files the commit should contain. **Never a bare
  `git commit`**: it commits the *entire* staged index, so anything
  another agent has staged rides into your commit under your message
  and author. A path-scoped commit makes that collision *structurally
  impossible*; the backstops below only reduce its odds.
  * **Verify the staged set as its own step** — run `git diff --cached
    --stat` and confirm it is *exactly* the files you intend, as a
    *separate* step, never chained into the `git commit` (a chained
    verify scrolls past and the commit fires regardless). Unstage
    anything swept in (`git restore --staged <path>`) before committing.
  * **Keep your staged window minimal** — don't leave a `git add` /
    `git mv` sitting exposed; stage and commit promptly.
  * **A `git mv` rename needs *both* sides named** in a path-scoped
    commit — naming only the destination commits the "add" and leaves
    the source-side deletion unstaged, so HEAD carries the file at both
    paths until a fixup. Name both source and destination (or `git add`
    the rename, then verify the `R###` line in `git diff --cached --stat`).
* **Untracked lifecycle artifacts are the third commit-discipline
  hazard.**  A failure mode in the same family as the shared-comm-
  files arc and the staged-index arc: an agent writes a
  lifecycle-opening artifact (a plan, proposal, or strategy doc)
  with the *intent* of shipping it as the corresponding
  lifecycle-opening commit, but never commits it.  The file sits
  untracked under `dev/proposals/`, `dev/plans/`, or `dev/strategy/`
  for another agent to inherit cold.  Empirically anchored at the
  reference deployment by repeated incidents within a single day.

  **Doctrine bite.**  If you write a lifecycle-opening artifact
  with the intent to ship it as the corresponding lifecycle-
  opening commit, commit that commit in the same turn.  Do not
  leave the artifact untracked for another agent to inherit.

  **Two corollaries.**

  * **The lifecycle-opening commit is atomic by intent.**  Write
    + `git mv` + `git commit` together; the partial state (file
    written, not committed) is the failure surface.
  * **If you can't commit this turn, don't write the artifact
    yet.**  Draft in chat or in the harness scratch surface
    (`.claude/notes/` or equivalent) until you can ship the
    artifact + the commit atomically.

  **Cold-start recovery.**  An agent starting a session checks
  for untracked lifecycle drafts in `dev/proposals/`,
  `dev/plans/`, and `dev/strategy/` as part of the orientation
  pass.  For each untracked draft: if it carries the agent's own
  active intent claim (per the work-intent system the
  `coordination-tiers` module ships), commit it now; if another
  agent's intent claim covers it, treat it as that agent's open
  thread (don't touch); if no intent claim resolves the
  ownership, surface it to the maintainer rather than committing
  or deleting unilaterally.

  The substrate for tracking recurrences of this hazard (and the
  staged-index + shared-comm hazards) is the `incident-trackers`
  module (default-on; ships the forkable tracker template +
  goodnight migration sub-step).  Heavier structural wards
  (session-start / goodnight check; mechanical gate; intent-
  system integration) stay reserve options the deployment can
  adopt under capability-pull.
* **Shared communication files** — the roadmap boards, the
  changelog, and (when the `progressive-onboarding` mechanism is
  installed) `dev/.cairn/onboarding-activated.jsonl` — are edited
  only at defined serialization points (a lifecycle archive, the
  goodnight routine, explicit instruction).  Refer to proposals
  and plans by filename stem, not path link.
* Run the test suite after any substantive change:
  `{{test_command}}`.
* **Keep commit bodies concise.** The body is a *snapshot* — what
  shipped and how it was verified — not a restatement of the proposal,
  plan, or changelog (those are the durable audit trail). Target 15–30
  lines for a non-trivial implementing commit (soft cap ~50; a trivial
  fix is often just the subject + a one-line body): a one- or
  two-sentence opener cross-referencing the source proposal / plan, a
  short bullet list of the substantive changes by file or surface, and
  a one-line verification snapshot with concrete numbers. Optimize for
  `git log --oneline` skimmability.

## Verifying claims

<!-- cairn:slot claim-check -->
(Filled from the `claim-check` default-on module when installed — the
verify-before-asserting discipline and how to run the checker (see
`dev/modules/claim-check.md` > "Merged into"). If claim-check is not
installed, replace with `N/A: claim-check not installed`. An unfilled
slot is a review finding.)
<!-- cairn:end claim-check -->

## Documentation discipline

<!-- cairn:slot documentation-discipline -->
(Filled from the `documentation-plan` default-on module when installed
— paste content from `dev/modules/documentation-plan.md` > "Merged
into" > Block 1: AGENTS.md. The merged content names the placement-
decision procedure for documentation and doctrine, the four-layer
vision (entry / governing / deliberation / descriptive), and the
cross-reference to `docs/DOCUMENTATION_PLAN.md`. If
documentation-plan is not installed, replace with `N/A:
documentation-plan not installed`. An unfilled slot is a review
finding.)
<!-- cairn:end documentation-discipline -->

## Project-specific conventions

<!-- cairn:slot project-conventions -->
(Naming conventions, the development environment, the high-risk
surfaces, and the operational pitfalls specific to {{project_name}}.
This is judgment work: a reasoning agent and the maintainer write
the project's *real* conventions here — it is not a mechanical
fill. An empty slot at first release is a review finding.)
<!-- cairn:end project-conventions -->

## Human contributors

`AGENTS.md` is the shared operational reference — it applies to human
and AI contributors alike. When the project's profile installs the
optional **`CONTRIBUTING.md`** (the human-team axis at `small-multi` /
`large-multi`), that file is the human contributor's entry point: it
carries the welcome and the project-specific onboarding and **points
back here** for the shared rules (the development environment, the test
command, the conventions, the commit and review workflow) rather than
duplicating them. Keep the split single-sourced — shared / operational
content lives here; `CONTRIBUTING.md` links to it. A solo-maintainer
project ships no `CONTRIBUTING.md`, and this section is informational.

## Vendor addendum

`AGENTS.md` is vendor-neutral — it names no specific AI agent tool.
Doctrine specific to one agent tool (a harness path, a
session-model habit) goes in that tool's own file, which opens by
importing this one (`@AGENTS.md`), so the shared content stays
single-sourced. Cairn ships the thin wrapper as `VENDOR.md`; the
adopter renames it to their tool's auto-loaded file (`CLAUDE.md`,
`GEMINI.md`, …).

**Drift guard.** The wrapper carries *only* harness-specific habits —
this tool's session/context model, its scratch directory, its
command quirks. Everything an agent of a *different* tool would also
need — the required reading, the session routines, the CLI, the
conventions, the development environment, the test command, the git
rules — stays canonical **here**, and the wrapper points at it. A
wrapper that duplicates this content has drifted into a fat fourth
doc; fold it back and leave only the pointer. (`VENDOR.md` carries the
same guard inline; `bootstrap/fidelity-check.md` notes it as a check.)
