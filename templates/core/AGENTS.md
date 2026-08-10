<!-- cairn-internal-ref-allow: doctrine/ reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- claim-check-allow: dev/modules/security-verification.md -->
<!-- ^ Forward reference: security-verification-activation Chunk B creates
     Cairn's own self-hosted dev/modules/security-verification.md (matching
     the other six default-on modules); it does not exist yet at Chunk A.
     In an ADOPTER's installed tree the path always resolves (the module is
     default-on). -->
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

**Reviews are attributed and self-committed.** No agent writes or
commits a review attributed to another agent — the named reviewer
commits their own findings, or the Maintainer does. The attribution
*is* the record's integrity: a review you did not write is not yours to
sign, and a structurally-independent read is only independent if its
author is its committer.

## Session routines

* **Session start** — at a cold start, or after a context-loss
  event, run a short orientation pass: if the project keeps a
  `RULES.md` (tracked, project-owned agent rules — Cairn never
  templates it; see `doctrine/doc-governance.md`), read it *first*;
  then re-anchor on the `dev/` tree, read the commit log since the
  last handoff, note in-flight proposals, and confirm your role
  before substantive work.
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

  **Exception — deliberation / planning / strategy / upstream-ledger /
  goodnight-handoff commits proceed without per-commit approval.** A commit
  touching ONLY files under `dev/proposals/`, `dev/plans/`, `dev/strategy/`, or
  the `dev/.cairn/` fold-back ledger (any combination) is a deliberation /
  recording artifact and lands without per-commit approval — as does the single
  goodnight-handoff commit (its routine artifacts: `dev/NEXT_SESSION.md`, the
  end-of-day `dev/PLANNING.md` scrub, `CHANGELOG.md` additions, intent-ledger
  pruning) and the one-line `dev/PLANNING.md` row-move that serializes a
  lifecycle transition (proposal / plan open, supersession, archive). Three
  guard-rails, all bright-line: **pushing still needs approval** (the exception
  covers `git commit` only); the **Decision commit is the Maintainer's**
  (scribing rules below); and **bundling any non-lifecycle file (code, `docs/`,
  `AGENTS.md`, …) loses the exception** and re-triggers the approval gate. This
  compact scope plus the three guard-rails are the operative rule; the
  deliberation-layer rationale the carve-in serves is in
  `doctrine/coordination.md`.
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
  impossible*; the windowless habit below removes the staged window the
  old backstops only narrowed.
  * **Prefer the windowless commit** — for *tracked* files, `git commit
    <paths>` stages *and* commits atomically: **no separate `git add`**,
    so no staged window is ever exposed. **Verify via the working tree**
    (`git status --short`, `git diff <paths>`) as its own step —
    index-independent, and it does **not** show other agents' staged
    work; do **not** verify with `git diff --cached`, which both
    *manufactures* the window (it needs a prior `git add`) and reads back
    *everyone's* staged index.
  * **New / untracked files** — `git add <paths> && git commit <paths>`
    in one invocation. If the chain aborts on a pre-commit / intent
    check, the files are left staged — immediately `git restore --staged
    <paths>` so a failed commit leaves no residue.
  * **A `git mv` rename needs *both* sides named** in a path-scoped
    commit — naming only the destination commits the "add" and leaves
    the source-side deletion unstaged, so HEAD carries the file at both
    paths until a fixup. Name both source and destination, and verify via
    `git status --short` (the `R  source -> destination` line), not
    `git diff --cached`.
  * **Bright line** — never leave a `git add` / `git mv` sitting exposed
    across tool calls, verification, or other work.
* **Untracked lifecycle artifacts — commit atomically.** If you write a
  lifecycle-opening artifact (plan, proposal, strategy doc) meaning to ship it,
  commit it the *same turn* — write + `git mv` + `git commit` together; never
  leave it untracked for another agent to inherit (the written-but-uncommitted
  state is the failure surface). If you can't commit this turn, don't write it
  yet (draft in chat or the harness scratch surface). Cold-start orientation
  checks `dev/proposals/`, `dev/plans/`, `dev/strategy/` for untracked drafts:
  commit one your own intent claim covers, leave one another agent's claim
  covers, surface an unclaimed one to the maintainer. This is the third
  commit-discipline hazard alongside the staged-index discipline
  (`doctrine/coordination.md`); recurrences are tracked via the
  `incident-trackers` module.
* **Shared communication files** — the roadmap boards, the
  changelog, and (when the `progressive-onboarding` mechanism is
  installed) its activation log — are edited
  only at defined serialization points (a lifecycle archive, the
  goodnight routine, explicit instruction).  Refer to proposals
  and plans by filename stem, not path link.
* **Verification boundaries.** Verification has three jobs; do not pay for the
  same broad run at every one (full doctrine: `doctrine/plans.md` and
  `doctrine/dual-review.md`).
  * **A — Iteration (scoped).** During implementation, run the tests and public-
    path probes mapped by the reviewed plan, plus standing gates for every
    touched surface. If a substantive code surface has no reviewed mapping, or
    its effects cannot be bounded confidently, run the configured full suite.
  * **B — Integration (stable evidence).** After the final implementation commit
    and before code review, run the configured full suite once against a clean,
    unchanged commit under the project's configured interpreter/runtime. Append
    the tested revision/range, runtime, clean pre/post state, commands, outcomes,
    timing, non-pass disposition, and known omissions to the plan as
    `## Implementation verification -- <agent> -- YYYY-MM-DD`.
  * **C — Falsification (independent).** The code reviewer verifies that record against
    the reviewed range, then runs independent targeted falsification; copying
    Boundary B's broad command is not a falsification ledger. Missing or stale
    evidence, unexplained non-pass outcomes, newly discovered coupling, changed
    implementation/test/executable-template/fixture bytes, a stronger trust-
    ceremony rule, or concrete doubt requires a fresh full run.
  Prose-only work runs its applicable documentation and policy gates unless its
  plan maps it to the test suite. A project's release verification remains a
  separate strict ceremony.
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

## Security verification

<!-- cairn:slot security-verification -->
(Filled from the `security-verification` default-on module when installed —
the standing dispatcher command and the high-risk Security-Review
designation of the dispatcher, its registry, its child result schema, its
binding-mode schema, and every registry entry (see
`dev/modules/security-verification.md` > "Merged into"). If
security-verification is not installed, replace with `N/A:
security-verification not installed`. An unfilled slot is a review finding.)
<!-- cairn:end security-verification -->

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

<!-- cairn:if human_team in small-multi,large-multi -->
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

<!-- cairn:endif -->
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
