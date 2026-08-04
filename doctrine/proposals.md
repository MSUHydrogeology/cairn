<!-- cairn-internal-ref-allow: doctrine/lifecycle.md doctrine/dual-review.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Proposals — type-specific lifecycle doctrine

This page covers the doctrine specific to **proposal artifacts**
(`dev/proposals/<date>-<author>-<slug>.md`).  Shared lifecycle
concepts — the Registered Report analogy, why the record exists,
the claim-marker maintenance exception, deferred-follow-up revival,
roadmap management, and archive preconditions — live in
`doctrine/lifecycle.md`.  Review-tier and structural-independence
doctrine lives in `doctrine/dual-review.md`.  Doctrine-evolution
gate doctrine lives in `doctrine/rationale.md`.

---

## The proposal lifecycle

A proposal moves through:

```
proposed  ->  reviewed  ->  revised  ->  accepted (stays in dev/proposals/)
                                            |
                                            +->  trivial impl: implementing commit
                                            |    ships + archives in one commit
                                            |
                                            +->  non-trivial impl: plan opened in
                                                 dev/plans/; archive happens in
                                                 the plan-open commit, before
                                                 implementation begins
                                     ->  rejected   ->  archive/  (Decision commit)
                                     ->  superseded ->  archive/  (Decision commit)
```

* **proposed** — the author opens the proposal.
* **reviewed** — a reviewer appends a `## Review` section.
* **revised** — the author appends a `## Response` and, where needed,
  a `## Revised proposal`. Review and revision may repeat.
* **accepted / rejected / superseded** — the Maintainer appends the
  `## Decision`. **The Decision commit does not archive an *accepted*
  proposal**: it stays in `dev/proposals/` and moves to `archive/`
  later — at the plan-open commit (non-trivial work) or the
  trivial-implementing commit. Only a *rejected* or *superseded*
  proposal archives in the Decision commit itself. See "File moves"
  below for the full rule.

The directory location encodes **work-status** (queued without plan /
in-flight with plan / shipped); the `Status:` field encodes
**deliberation state**. Two orthogonal axes.

Two rules are bright-line — **append-only** and **one commit per
transition** — each detailed in its own subsection below.

**A proposal is a Stage 1 Registered Report** (see
`doctrine/lifecycle.md` > "The lifecycle as a Registered Report").
A proposal locks the change's design *and* its evidence / verification
plan before any code is written — that is Stage 1. The plan and its
code review (see `doctrine/plans.md`) then check the implementation
against that lock — Stage 2. The discipline is a defense against
post-hoc *metric p-hacking*: the verification plan exists before the
implementation, so evidence is judged against a commitment, not chosen
after the fact to flatter whatever the code happened to do.

### One commit per lifecycle transition

Each transition lands in its own commit so the discussion arc is
transparent through `git log` and a reviewer can see exactly what
changed at each round:

* Commit on **opening** a proposal (status `proposed`).
* Commit on **appending a Review** (status -> `reviewed`).
* Commit on **appending a Response and any "Revised proposal"
  section** (status -> `revised`). If multiple review rounds happen,
  each Review / Response pair gets its own commit.
* Commit on **the Maintainer's Decision** (status -> `accepted` /
  `rejected` / `superseded`).
  * For `accepted` proposals, the Decision commit flips status
    only. The proposal stays in `dev/proposals/`; the
    subsequent plan-open or trivial-implementing commit moves
    the file to `archive/` (see "File moves" below).
  * For `rejected` / `superseded` proposals, the Decision commit
    flips status AND moves the file to `archive/` — no
    implementation will follow, so the archive is the right home
    immediately.

Bundling multiple lifecycle stages into one commit hides who changed
what; bundling lifecycle work with implementation work hides when the
deliberation actually closed. Keep them separate.

### Append-only is bright-line

Each round is **append-only**. Earlier sections are **immutable** —
don't rewrite, edit, or "tighten" them. Add new content as a new
section below the existing arc. Reading the file top-to-bottom gives
the full discussion as it actually unfolded, which is what makes the
file readable cold and what gives the review system its bite: the
Maintainer's Decision is on the text they read, not on text edited
later.

The rule is **bright-line**. Even small wording tweaks — softening
"caps" to "goals", changing a single word, "reviewability tightening"
of prior sections, fixing what reads with hindsight as an unclear
phrasing — violate append-only when applied to prior content. If
you want a section to read differently, append a new section that
revises the framing explicitly; don't quietly edit the original.

*One bounded exception: inserting a `claim_check` marker line —
`Proposed/Untracked/External-repo paths:` — adjacent to a path token
is **mechanical maintenance, not authoring a review** (additive-only,
mechanical, its own labeled `claim-marker maintenance:` commit,
typo-guarded). See the claim-marker maintenance doctrine in
`doctrine/lifecycle.md` > "The proposal lifecycle", and the marker
doctrine below.*

**The ONE content exception**: link maintenance. When a referenced
file moves on disk, you may update the path inside the link target
part `](url)` so the link still resolves. The display text and the
surrounding prose stay as written. Never use this exception as cover
for content edits.

The plan-open or trivial-implementing-commit archive move typically
triggers *two* kinds of link-target adjustment: outbound links
*into* the proposal — from sibling proposals or other `dev/` docs
that intentionally use a Markdown path link — get their target
paths updated from `proposals/foo.md` to `proposals/archive/foo.md`;
relative-path links *inside* the proposal (e.g., `../PLANNING.md`
from a Decision section) get their depth adjusted (e.g.,
`../../PLANNING.md`) to keep resolving from the deeper location.
Both fall under the link-maintenance exception; the prose around
them stays as written. `PLANNING.md` and `NEXT_SESSION.md` are
*not* in the outbound-link set — they refer to proposals by
backticked filename stem, not path link, so the archive move needs
no edit there; and `CHANGELOG.md` entries are written once at
finalization, never updated afterward. See the "File moves" note
below and `AGENTS.md > Shared communication files`.

**Archived proposals are stricter still.** Once status reaches a
terminal value (accepted / rejected / superseded) and the file moves
to `dev/proposals/archive/`, the file is **closed**. No edits beyond
link maintenance. The Maintainer's Decision is locked to the text as
it stood at terminal status.

If experience has shown an accepted proposal's convention is too
tight, too loose, or wrong, the right channel is to **open a new
proposal** that explicitly amends or supersedes the original. That
creates an honest deliberation record (and lets the friendly-
adversary review process scrutinize the amendment, which is the
whole point of the system). Don't quietly edit the archived
deliberation.

---

## Triage: trivial vs. non-trivial

A trivial fix — a typo, a one-line bug, an obvious correction — is
just made; it needs no proposal. Open a proposal (rather than just
commit) when the change:

* Touches a public API or a config contract.
* Introduces a new abstraction, class, or module.
* Moves files / restructures a directory.
* **Revives a deferred follow-up from `dev/PLANNING.md`** whose
  execution is itself proposal-worthy under this triage rule (file
  moves, public / config contract changes, new abstractions, or
  non-trivial design tradeoffs) when the original proposal/plan named
  only the trigger or revival condition and did not settle the design
  choices. Approval of a trigger is not approval of a design. Small
  pickable-cold queued items that are not otherwise proposal-worthy —
  mechanical doc cleanups, single-file test additions, typo-class
  fixes that happen to live in the queue — proceed under the normal
  "just commit" path; revival of a queued item does not by itself
  summon proposal review.
* Has implementation tradeoffs you want a second opinion on before
  baking it in.

Everything else — a new helper, a test, a typo fix, a docstring
polish, a self-contained refactor — just commit. The proposal system
is for "I want to bake this in for a while; let's check it first."

Once accepted, the implementation is **trivial** (a single commit, a
single area, no follow-ups — implemented and the proposal archived
together) or **non-trivial** (multiple commits or areas, multi-stage
sequencing, or deferred follow-ups — it opens a plan; see
`doctrine/plans.md`).

**The plan-review decision is part of accepting a non-trivial
change**, not an afterthought at plan-open. For non-trivial work the
`**Plan review**` metadata line states the anticipated plan-review
tier — `required(<tier>)` or `not required(<rationale>)`, with **no
silent default; a missing line is a review finding, like an unfilled
slot**. The author states it (they see the cross-cutting / contract /
new-abstraction risk); the Maintainer's Decision ratifies or
overrides. Valid `not required` rationales include "pure doc sync",
"trivial layout only", "straightforward follow-up to a
recently-reviewed sibling plan"; a reviewer treats an unjustified
`not required` on a clearly-risky change as a finding. A `required`
plan opens in `awaiting-plan-review` and does not start implementation
until its plan-review section lands (the *review-before-implement*
gate; see `doctrine/plans.md` > "The plan-review precondition").

**Escape hatch.** If a change is urgent, clearly reversible, or
explicitly experimental, it may proceed without a proposal, but the
commit or follow-up note should say why the proposal step was
skipped. This keeps the bypass traceable without forcing process
onto bug fixes or short-lived experiments.

---

## Forward-reference paths — `Proposed paths:` marker doctrine

A proposal often cites paths it *plans to create* at implementation
time (new test files, new directories, new docs). At proposal-open
time those paths do not resolve, so `claim_check` hard-flags them.
The escape hatch is `claim_check`'s marker-line mechanism: a line
that begins with `Proposed paths:` (or `Proposed path:` for a single
token; case-insensitive; optional list-item prefix) exempts the
backticked path tokens **on that same line** from the hard path
check.

Use the marker when:

* The proposal opens with paths it plans to create.
* The proposal cites future test files / fixture files /
  documentation files.
* The proposal moves a file — the future archive path is
  forward-reference until the move happens.

Marker shape (preferred): one or more `Proposed paths:` lines, each
listing a batch of related tokens. Multiple tokens per line are
fine; the marker exempts everything on its own line **and any
contiguous structured block immediately beneath it** — Markdown
table rows, list rows, or bare backticked path-list rows are exempt
until the next blank line, heading, or ordinary prose line, so a
marker line placed directly above a path-bearing table covers the
whole table.

Example (place near the top of the proposal, e.g. after the Context
section):

```
Proposed paths: `path/to/new/dir/`, `path/to/new/dir/archive/`,
`path/to/new/reference.md`.

Proposed paths: `path/to/tests/test_x.py`, `path/to/tests/test_y.py`.
```

**The marker is line- and block-scoped**: it does NOT exempt a path
where the same token recurs in ordinary prose elsewhere in the
document (a Rationale sentence, a chunk description). Such an
occurrence still hard-flags. Two clean ways to handle it, in
preference order:

* **Cite the existing parent directory + the bare new filename.**
  `claim_check` treats a backticked token as a repo-path claim only
  when its first segment is a real top-level directory; a bare
  filename (no `/`) is not a claim. So in prose, name a new file as
  a bare name beside its directory — e.g. `new_helper.py` next to the
  existing `path/to/dir/` — so the directory token resolves, the bare
  name is ignored, and the full slashed path stays declared once in
  the marker. No flag, no residue.
* **Conscious-accept**, documented in the proposal-open commit body
  — the fallback when the full slashed path genuinely must appear in
  prose. It clears at the implementing commit where the path is
  created.

**Two other marker keywords** parallel `Proposed paths:`:

* `Untracked paths:` — for git-ignored paths a fresh checkout will
  not carry (e.g. local run-output or scratch directories).
* `External-repo paths:` — for paths that resolve in a sibling
  repository this project depends on, or an upstream framework
  checkout, rather than in this tree.

All three markers exempt only the tokens on the marker line itself.
See `claim_check`'s module docstring (the "Marker lines" subsection)
for the full mechanism documentation.

**The convention applies to Review / Response sections too.**
Forward-reference and sibling-repo paths land most often in
*reviewer* sections — and an external-tool reviewer will not have run
`claim_check` at its source. The agent **committing** a review
section runs `claim_check` and marks any flagged path; under the
`AGENTS.md` claim-marker-maintenance exception, inserting the marker
is permitted even inside another agent's append-only section
(additive marker line only, in its own `claim-marker maintenance:`
commit). **Typo guard**: before marking, confirm the flagged path is
not a typo of a real local path — fix or surface it rather than
silencing. **Placement safety**: an inline marker is *block-scoped* —
it exempts contiguous rows beneath it until a blank line / heading.
Place it immediately adjacent to the target token and leave a blank
line after the target row, so the continuation does not over-exempt
later rows. For a document with *many* such paths (e.g. a cross-repo
proposal whose reviewer sections cite sibling-repo paths), prefer the
file-level `<!-- claim-check-allow: <glob> -->` directive (narrow
globs only; it reports each exempted token) over scattering per-line
markers.

---

## File moves

The directory move to `dev/proposals/archive/` is decoupled from the
Decision-status flip for `accepted` proposals; the two are bundled
for `rejected` / `superseded`.

**Accepted proposals** stay in `dev/proposals/` after the Decision
commit:

* If the implementation will be **trivial** (single commit, single
  area, no multi-stage execution, no deferred follow-ups), the
  implementing commit ships the work AND moves the proposal to
  `dev/proposals/archive/` in the same commit.
* If the implementation is **non-trivial** (lands across multiple
  commits, OR touches multiple files / areas, OR has multi-stage
  sequencing, OR carries deferred follow-ups — see the plan triage
  rule in `doctrine/plans.md` for the canonical formulation), the
  implementing agent first opens a plan in `dev/plans/`. The plan-open
  commit moves the proposal to `dev/proposals/archive/` in the same
  commit — the proposal's deliberation is closed AND has now been
  carried into an actionable execution artifact, so the proposal's
  home is now history.

**Rejected** and **superseded** proposals move to
`dev/proposals/archive/` in the Decision commit itself. No
implementation will follow; the archive is the right home
immediately.

In all cases, update any inbound path links from `dev/` docs in the
same commit as the move so references stay resolved. `PLANNING.md`
and `NEXT_SESSION.md` refer to proposals by filename stem, not path
link (per `AGENTS.md > Shared communication files`), so they need no
link update on the move; `CHANGELOG.md` keeps full paths, but its
entry is *written* in the archival commit — final-by-construction,
never updated afterward.

`accepted` means the **decision** is accepted; implementation
follow-up still remains. Track it via the plan in `dev/plans/`
(non-trivial) or the implementing commit message (trivial) — not by
holding the proposal open.

---

## Archive preconditions

Before flipping status to `accepted` / `rejected` / `superseded` and
moving the file to `archive/`, every **deferred follow-up item**
named in the proposal must carry a **recorded disposition** —
`accept`, `guard`, `wontfix`, or (with the Maintainer's quoted
authorization) `defer`. See `doctrine/lifecycle.md` > "Archive
precondition" for the vocabulary, the two `wontfix` eligibility
rules, and why a disposition is not the same thing as a durable home.
A `defer` needs a home outside the proposal text; acceptable homes:

* `dev/PLANNING.md` — a tier item, a follow-up backlog, or a new
  dedicated subsection.
* A topic doc's "Future work" section.
* Its own queued follow-up proposal at
  `dev/proposals/<date>-<author>-<short-title>.md`.

`dev/NEXT_SESSION.md` is not an archive-time home — it is edited only
at the goodnight routine and on explicit user instruction. A small,
pickable-cold follow-up goes to `dev/PLANNING.md` here; the goodnight
scrub then surfaces it into `NEXT_SESSION.md`.

The archive commit body must name each deferred item's disposition,
in the form:

```
Dispositions:
* <item> -> accept (fixed in this proposal's scope)
* <item> -> guard (tests/test_thing.py::test_the_case)
* <item> -> wontfix (<rationale>)
* <item> -> defer -> dev/PLANNING.md > <subsection>   [Maintainer: "<quote>"]
```

The older `Follow-ups migrated to:` spelling remains valid and is
still recognized; proposals archived under it are correct as they
stand and are never rewritten.

This makes the migration auditable from `git log` alone. The same
rule applies to plan files in `dev/plans/` when they archive; the
canonical statement lives at `doctrine/lifecycle.md` > "Archive
precondition", which the roadmap board's own section restates for a
reader who arrives there first.

**Why**: archived proposals become deliberation history — nobody
re-reads them looking for outstanding work. Without this rule,
follow-ups silt up in `archive/` where they're invisible to the
goodnight stale-item sweep and to anyone scanning PLANNING for the
next thing to pick up.

**Deferred follow-up wording.** When migrating a deferred follow-up
to `PLANNING.md`, name the design choices that *are* approved ("the
implementation will live at `<path>` with `<contract>`") or
explicitly say *what* is approved ("trigger only — revival requires
a fresh proposal if the implementation is proposal-worthy under the
triage rule in `doctrine/proposals.md` > "Triage: trivial vs.
non-trivial""). A deferred follow-up that names only a trigger leaves
a downstream agent guessing whether the design is pre-approved.

---

## Count claims — the three-kind precision / `as_of` discipline

A count is not one thing.  Before writing a number into a durable
artifact, decide which of **three kinds** it is — each wants a
different treatment, and getting the kind right is what removes the
need for exact counts (and the stale-count drift they invite) at the
source:

* **Decision-irrelevant** — the number is colour, not the point ("the
  largest file by far", "a few hundred tests").  **Approximate it**
  (`~4900 lines`).  An exact count here is a maintenance liability with
  no upside: it drifts, and nothing depended on its precision.
* **Dated snapshot** — a measurement true *at a moment* the artifact
  records as evidence ("the suite had N tests when this proposal was
  written").  **Date it** (`N tests, as_of YYYY-MM-DD`) and **never
  re-measure it** — re-running *erases* the evidence the snapshot is.
* **Live invariant** — a current size cited as present fact, prone to
  drift.  This is the one number worth an exact value *and* worth
  machine verification: register it and re-measure it (the code-side
  `verify_counts` registry, where the project ships one).

"The safest stale count is the one prose did not need."  Most numbers
are decision-irrelevant; approximating them is the cheapest and most
durable fix.  Reserve exact counts for snapshots (dated) and invariants
(registered).

The write-time count soft-flag and its `claim-check-allow-count`
directive were **retired 2026-06-05** (0 catches across the
verify-before-asserting instance log; the nag generated header bloat).
`claim_check` no longer flags counts — a stray
`claim-check-allow-count` comment in an archived artifact is silently
ignored.

---

## Response — disposition grammars

Response sections use one of two disposition-grammar vocabularies
depending on whether the implementing commit already exists. Pick the
grammar based on context:

**Proposal-Response grammar** (the implementing commit does NOT yet
exist; the Response is part of the proposal-revision cycle, NOT a
code-review record):

* `accept` — accepted; the change will be incorporated in the
  Revised proposal (or in the eventual implementing chunks).
* `accept with modification` — accepted with an author-specified
  modification captured inline (different exact diff than the
  reviewer suggested, but the spirit of the suggestion is kept).
* `reject` — with reason.
* `defer` — escalate to the Maintainer's Decision (rare; use when
  the critique raises a question only the Maintainer can resolve).

**Code-review-Response grammar** (used in code-review records,
sharpening commit bodies, plan code-review sections — the
implementing commit DOES exist and is referenceable by sha):

* `accept (merged at <sha>)` — the reviewer's suggested-edit commit
  was cherry-picked or merged verbatim.
* `accept (rewrote inline)` — the suggestion was acted on with a
  different exact diff than the reviewer's.
* `accept (followup commit <sha>)` — a separate sharpening commit
  addressed the finding.
* `guard (<path>::<node>)` — homed in an artifact that **executes**:
  a test node, an assertion, a runtime guard. Names the node. A
  comment is not eligible — comments do not fire.
* `reject` — with reason.
* `defer` — to a follow-up plan / proposal.
* `wontfix` — explicit non-action with rationale.

This same grammar is the vocabulary of the **archive-time
disposition** block (`doctrine/lifecycle.md` > "Archive
precondition"), where `defer` additionally requires the Maintainer's
quoted authorization and `wontfix` is bounded by the two eligibility
rules stated there.

The split exists because the proposal-Response context predates any
implementing commit — there is no `<sha>` to cite when the Response
is part of the proposal's revision cycle. Conflating the two grammars
created a "fill in a fake sha" failure mode that the split prevents.

For each numbered critique, write one disposition token from the
grammar above plus a one-sentence rationale. No silent dropping.
Brief is fine; precision matters more than length.

**Worked example — proposal Response** (no implementing commit yet):

* **[R1]** accept — will incorporate in the next revision.
* **[R2]** accept with modification — author-specified change named
  inline (the spirit is preserved but the exact text differs).
* **[R3]** reject — the assumption holds for the documented case; see
  the relevant module / section.
* **[R4]** defer — depends on a default only the Maintainer can settle.

**Worked example — code-review Response** (implementing commits exist,
so a `<sha>` is referenceable):

* **[F1]** accept (merged at `<sha>`) — …
* **[F2]** accept (rewrote inline) — …
* **[F3]** accept (followup commit `<sha>`) — …

If accepted critiques substantially change the proposal, write a short
"## Revised proposal" section and update `Status:` to `revised`.
