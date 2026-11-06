<!-- cairn-internal-ref-allow: docs/methodology/lifecycle.md docs/methodology/dual-review.md docs/methodology/rationale.md reason=docs/methodology/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where docs/methodology/ references resolve") -->

# Proposals — type-specific lifecycle doctrine

This page covers the doctrine specific to **proposal artifacts**
(`dev/proposals/<YYYY-MM-DD>-<author>-<slug>.md`).  Shared lifecycle
concepts — the Registered Report analogy, why the record exists,
the claim-marker maintenance exception, deferred-follow-up revival,
roadmap management, and archive preconditions — live in
`docs/methodology/lifecycle.md`.  The review stance and how distance is
recorded live in `docs/methodology/dual-review.md`.  Doctrine-evolution
gate doctrine lives in `docs/methodology/rationale.md`.

---

## The proposal lifecycle

A proposal moves through:

```
proposed  ->  reviewed  ->  revised  ->  accepted (stays in dev/proposals/)
                                            |
                                            +->  light: no plan; Boundary B
                                            |    recorded in proposal, then archive
                                            |
                                            +->  standard/heavy trivial: ship +
                                            |    archive in one commit
                                            |
                                            +->  standard/heavy non-trivial: plan in
                                                 dev/plans/; archive happens in
                                                 the plan-open commit, before
                                                 implementation begins
                                     ->  rejected   ->  archive/  (Decision commit)
                                     ->  superseded ->  archive/  (Decision commit)
```

* **proposed** — the author opens the proposal.
* **reviewed** — a reviewer appends a `## Review` section.
* **revised** — the author appends a `## Response` with dispositions and
  revises the operative proposal text in place. One round carries it to the
  Decision; only widened scope receives another proposal pass.
* **accepted / rejected / superseded** — the Maintainer appends the
  `## Decision`. **The Decision commit does not archive an *accepted*
  proposal**: it stays in `dev/proposals/` and moves to `archive/`
  later — after light-tier verification, at the plan-open commit
  (non-trivial standard/heavy work), or at the standard/heavy trivial
  implementing commit. Only a *rejected* or *superseded*
  proposal archives in the Decision commit itself. See "File moves"
  below for the full rule.

The directory location encodes **work-status** (queued without plan /
in-flight with plan / shipped); the `Status:` field encodes
**deliberation state**. Two orthogonal axes.

Two rules are bright-line — append the review record without editing it, and
make **one commit per transition**. Operative proposal text revises in place;
git preserves its history.

**A proposal is a Stage 1 Registered Report** (see
`docs/methodology/lifecycle.md` > "The lifecycle as a Registered Report").
A proposal locks the change's design *and* its evidence / verification
plan before any code is written — that is Stage 1. The plan and its
code review (see `docs/methodology/plans.md`) then check the implementation
against that lock — Stage 2. The discipline is a defense against
post-hoc *metric p-hacking*: the verification plan exists before the
implementation, so evidence is judged against a commitment, not chosen
after the fact to flatter whatever the code happened to do.

### One commit per lifecycle transition

Each transition lands in its own commit so the discussion arc is
transparent through `git log` and a reviewer can see exactly what
changed at each round:

* Commit on **opening** a proposal (status `awaiting-review`).
* Commit on **appending a Review** — a *blocking* review moves status to
  `revising`; a *clearing* one moves it to `awaiting-decision`.
* Commit on **appending a Response and revising the operative text in place**.
  The Response lists one disposition and reason per finding; the operative
  wording is current in the artifact and earlier versions remain in git.
  Reviews, responses and decisions are never edited. A scope-widening revision
  gets a review of its new material only.
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

### The current proposal and its history

Revise the operative proposal sections in place while the artifact is active.
They are the current contract. Git history preserves what was believed at each
earlier commit. Reviews, responses and decisions append and are never edited;
the Maintainer's Decision is made on the proposal text at that commit. The
Response lists one disposition and reason per finding and updates the
`Withdrawn / superseded commitments` ledger; it does not repeat the design.

*One bounded exception for appended review records: inserting a `claim_check` marker line —
`Proposed/Untracked/External-repo paths:` — adjacent to a path token
is **mechanical maintenance, not authoring a review** (additive-only,
mechanical, its own labeled `claim-marker maintenance:` commit,
typo-guarded). See the claim-marker maintenance doctrine in
`docs/methodology/lifecycle.md` > "The proposal lifecycle", and the marker
doctrine below.*

**Link-target maintenance in appended records**: when a referenced
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
them stays as written. A backticked filename-stem reference in a coordination
file survives the move without an edit; an inbound path link needs the same
link maintenance as other path links. See the "File moves" note below.

**Archived proposals are stricter still.** Once status reaches a
terminal value (accepted / rejected / superseded) and the file moves
to `dev/proposals/archive/`, the file is **closed**. No edits beyond
link maintenance. The Maintainer's Decision is locked to the text as
it stood at terminal status.

If experience shows an accepted commitment must change, open a new proposal
that explicitly amends or supersedes the archived one. Do not edit the archived
record.

### Outcome sequence and plan finishability

In the existing Proposal section, name each useful delivery outcome, its
prerequisites and intended release or capability. A proposal may authorize
several plans. Keep later outcomes queued on the existing board with their
immutable source and a condition for revival; do not open an active plan before
its prerequisites are available. The first plan opening archives the accepted
proposal under the existing rule. Later unchanged authorized work stays linked
to that immutable source and needs no new Decision. Preserve every accepted
outcome and check. One plan may include dependent internal chunks when each
plan's implementation, required checks, reviews and archive finish without
another unfinished plan. Do not split work by default. Keep human-operation
waits separately owned and evidenced, not final plan tasks. A failed required
check remains implementation work.

---

## Triage: three lanes, chosen by a closed triage procedure

**The canonical triage procedure — the three lanes, evaluated in
order, and the defect-repair carve-out — lives in** `docs/methodology/lifecycle.md`
**> "Three lanes, chosen by a closed triage procedure".** A proposal is
opened for substantive work: the change touches a high-risk surface
`AGENTS.md` names, breaks or widens a contract, is release or security
ceremony, is a major new feature, or the author or Maintainer elects
it for anything else genuinely architectural. Trivial work remains direct. Ordinary uncertainty about
ceremony takes the lighter lane with a reason; a newly discovered trust
boundary stops work for reassessment.

**Revives a deferred follow-up from `dev/PLANNING.md`** is a further
deliberate-lane trigger when the original proposal/plan named only the
trigger or revival condition and did not settle the design choices —
approval of a trigger is not approval of a design. Small pickable-cold
queued items that are not otherwise proposal-worthy — mechanical doc
cleanups, single-file test additions, typo-class fixes that happen to
live in the queue — proceed under the trivial lane; revival of a
queued item does not by itself summon proposal review.

Other substantive work starts with a proposal, reviewed and decided before
implementation. The Decision sets its tier. Light work uses the accepted
proposal as its implementation record and does not open a plan. Standard and
heavy work retain plan triage, required reviews and checks. There is no
parentless change-note route. Genuinely trivial work — a typo, a one-line bug
with a failing-test reproduction, a self-contained helper, a docstring polish
— is just made, with no proposal or plan.

Once accepted, a light-tier proposal has no plan or code review, regardless of
implementation size. The author appends Boundary B evidence to that proposal
after its final implementation commit and archives it with that record.

For standard/heavy proposals, the implementation is **trivial** (a single commit, a
single area, no follow-ups, and a Boundary B that would run `bounded`,
except that a defect repair meeting the lifecycle's three conditions stays
trivial on a named surface — implemented and the proposal archived together, with no code review) or
**non-trivial** (multiple commits or areas, multi-stage sequencing,
deferred follow-ups, or Boundary B in `wide` mode — it opens a plan; see
`docs/methodology/plans.md`).

**The plan-review decision is part of accepting a non-trivial
change**, not an afterthought at plan-open. For non-trivial work the
`**Plan review**` metadata line states the anticipated plan
review — `required(Internal)`, `required(Internal + Internal Security
Review)` for a security-sensitive surface, or `not
required(<rationale>)`, with **no silent default; a missing line is a
review finding, like an unfilled slot**. The author states it (they
see the cross-cutting / contract / new-abstraction / security risk);
the Maintainer's Decision ratifies or overrides. Valid `not required`
rationales include "pure doc sync",
"trivial layout only", "straightforward follow-up to a
recently-reviewed sibling plan"; a reviewer treats an unjustified
`not required` on a clearly-risky change as a finding. Bare `not
required` describes a plan that skips its own review. A light proposal writes
`not required(no plan: light tier)` without plan triage. A standard/heavy
change that needs no plan writes `not required(no plan: <how each skip
condition holds>)`, showing each plan triage condition in turn (single
commit, single area, no follow-up, Boundary B would run `bounded`); a
standard/heavy "no plan" claim without each condition shown is a review finding. A `required`
plan opens in `awaiting-plan-review` and does not start implementation
until its plan-review section lands (the *review-before-implement*
gate; see `docs/methodology/plans.md` > "The plan-review precondition").

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
token; case-insensitive; optional list-item prefix) exempts path and
line-bounds tokens on that line from the hard checks. Each literal path
declared on the marker line may also recur anywhere else in the document
when it does not resolve locally.

Use the marker when:

* The proposal opens with paths it plans to create.
* The proposal cites future test files / fixture files /
  documentation files.
* The proposal moves a file — the future archive path is
  forward-reference until the move happens.

Marker shape (preferred): one or more `Proposed paths:` lines, each
listing a batch of related tokens. Multiple tokens per line are
fine; each backticked token on the marker line declares a path. The
line's declared literal paths may recur anywhere else in the same
document, and each exempted occurrence is reported with the declaration
that authorized it. The marker line and any contiguous structured rows
(Markdown table rows, list rows, or bare backticked path-list rows) are
exempt from hard path and line-bounds checks until the next blank line,
heading, or ordinary prose line. Each continuation row declares only
its first backticked token; later tokens in that row's explanation are
not declarations. A standalone marker line still declares its paths
for document-wide reuse.

Example (place near the top of the proposal, e.g. after the Context
section):

```
Proposed paths:
- `path/to/new/dir/` -- a new directory.
- `path/to/new/dir/archive/` -- its future archive.
- `path/to/new/reference.md` -- a new reference page.

The reference page will live at `path/to/new/reference.md`.
```

**Document-wide reuse is exact and fail-closed.** A declaration exempts
only the identical literal path in the same document when that path does
not resolve locally. It never exempts a sibling, descendant, or
look-alike prefix. A wildcard or placeholder is not a literal
declaration; a conflicting declaration under another marker keyword
grants no authority. Do not reuse a declaration after its path resolves:
existing files and stale line-bounds citations remain subject to the
hard checks. Use a marker line or structured marker block when a
declared path recurs in ordinary prose (a Rationale sentence or chunk
description). On a mutable lifecycle artifact
(`dev/proposals/<name>.md` or `dev/plans/<name>.md`, not an
`_template.md`), each checkable declaration in a structured block is
subject to liveness: its path must not have materialized, and it must
authorize at least one would-be missing-path or line-bounds exemption
outside every marker line and block. A path the
checker cannot resolve is reported informationally because liveness
cannot be evaluated; a path now resolved by the exact lifecycle archive
rule is a non-failing migration diagnostic. Files under
`dev/proposals/archive/` or `dev/plans/archive/`, proposals with terminal
status (`accepted`, `rejected`, `superseded`), and plans with terminal
status (`archived`) are immutable, so their liveness findings are
informational. A missing or invalid status does not make an active
artifact immutable. A standalone marker line declares paths
document-wide but carries no separate liveness obligation.

**Two other marker keywords** parallel `Proposed paths:`:

* `Untracked paths:` — for git-ignored paths a fresh checkout will
  not carry (e.g. local run-output or scratch directories).
* `External-repo paths:` — for paths that resolve in a sibling
  repository this project depends on, or an upstream framework
  checkout, rather than in this tree.

All three marker keywords use the same exact document-wide rules.
See `claim_check`'s module docstring (the "Typed-declaration registry"
subsection) for the full mechanism and provenance rules.

**The convention applies to Review / Response sections too.**
Forward-reference and sibling-repo paths land most often in
*reviewer* sections — and an external-tool reviewer will not have run
`claim_check` at its source. The agent **committing** a review
section runs `claim_check` and marks any flagged path; under the
`AGENTS.md` claim-marker-maintenance exception, inserting the marker
is permitted even inside another agent's appended review section
(additive marker line only, in its own `claim-marker maintenance:`
commit). **Typo guard**: before marking, confirm the flagged path is
not a typo of a real local path — fix or surface it rather than
silencing. **Placement safety**: a marker block exempts its contiguous
structured rows and lets each row's first path become an exact
document-wide declaration. A marker line's paths also declare exact
paths document-wide, even without continuation rows. Put only
intentional declarations in the block, then leave a blank line after
its rows. For a document with *many* such paths (e.g. a cross-repo
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

* A **light** proposal never opens a plan, even for multi-area or wide work.
  After its final implementation commit, append the Boundary B record to the
  proposal and archive it in that verification commit.
* For **standard/heavy**, if the implementation will be **trivial** (single commit, single
  area, no multi-stage execution, no deferred follow-ups, and a
  Boundary B that would run `bounded`, except that a defect repair meeting
  the lifecycle's three conditions stays trivial on a named surface), the implementing commit ships the
  work AND moves the proposal to `dev/proposals/archive/` in the same
  commit. It has no code review. The implementing commit re-reads each
  plan-skip condition against what it actually touched. If it touched more
  than one area, or its Boundary B would run `wide`, a plan opens then, and
  the plan-open commit archives the proposal.
* For **standard/heavy**, if the implementation is **non-trivial** (lands across multiple
  commits, OR touches multiple files / areas, OR has multi-stage
  sequencing, OR carries deferred follow-ups, OR needs Boundary B in
  `wide` mode — see the plan triage
  rule in `docs/methodology/plans.md` for the canonical formulation), the
  implementing agent first opens a plan in `dev/plans/`. The plan-open
  commit moves the proposal to `dev/proposals/archive/` in the same
  commit — the proposal's deliberation is closed AND has now been
  carried into an actionable execution artifact, so the proposal's
  home is now history.

**Rejected** and **superseded** proposals move to
`dev/proposals/archive/` in the Decision commit itself. No
implementation will follow; the archive is the right home
immediately.

As of 2026-10-29, the proposal archive contains no proposal with
`Status: rejected`; it does contain a superseded proposal. This describes
formal proposal decisions only: ideas may be set aside in conversation
before they become proposals. The count is not a success measure or a
reason to avoid rejecting a proposal when that is the right decision.

In all cases, update any inbound path links from `dev/` docs in the
same commit as the move so references stay resolved. Filename-stem references
need no link update; path links do. `CHANGELOG.md` keeps full paths, but its
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
authorization) `defer`. See `docs/methodology/lifecycle.md` > "Archive
precondition" for the vocabulary, the two `wontfix` eligibility
rules, and why a disposition is not the same thing as a durable home.
A `defer` needs a home outside the proposal text; acceptable homes:

* `dev/PLANNING.md` — a tier item, a follow-up backlog, or a new
  dedicated subsection.
* The receiving open plan's named section, with the item actually appended
  and the Maintainer's quoted authorization covering the added scope.
* A topic doc's "Future work" section.
* Its own queued follow-up proposal at
  `dev/proposals/<YYYY-MM-DD>-<author>-<short-title>.md`.

The local next-session note is not an archive-time home — it is
written only at the goodnight routine. A small, pickable-cold
follow-up goes to `dev/PLANNING.md` here; the goodnight note may then
point at that row.

The archive commit body must name each deferred item's disposition,
in the form:

```
Dispositions:
* <item> -> accept (fixed in this proposal's scope)
* <item> -> guard (tests/test_thing.py::test_the_case)
* <item> -> wontfix (<rationale>)
* <item> -> defer (<reason>) -> dev/PLANNING.md > <section>   [Maintainer: "<quote>"]
* <item> -> defer (in motion) -> dev/plans/<YYYY-MM-DD>-<slug>.md > <section>   [Maintainer: "<quote>"]
```

The older `Follow-ups migrated to:` spelling remains valid and is
still recognized; proposals archived under it are correct as they
stand and are never rewritten.

This makes the migration auditable from `git log` alone. The same
rule applies to plan files in `dev/plans/` when they archive; the
canonical statement lives at `docs/methodology/lifecycle.md` > "Archive
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
triage rule in `docs/methodology/proposals.md` > "Triage: trivial vs.
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
disposition** block (`docs/methodology/lifecycle.md` > "Archive
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

### Revise operative proposal text in place

While a proposal is active, revise its operative sections in place. Git history
preserves earlier versions. A Response records one disposition and reason per
finding; it does not repeat the proposal. Reviews, responses and decisions
remain appended and unchanged. Keep the `Withdrawn / superseded commitments`
ledger current so a later reader can see what changed. A scope-widening
revision receives a review of the new material only.

## Plan review — the derived plan's tier

A proposal's `**Plan review**:` header field states the anticipated
plan review for its non-trivial standard/heavy work's derived plan, and it is **always
one of the ruled tokens** — `required(Internal)`, `required(Internal +
Internal Security Review)` for a security-sensitive surface, or `not
required(<rationale>)`. A plan review is a fresh-context pass; there is
no mandated read from a different agent type to earn, recommend, or
inherit, so a proposal reviewer records no plan-review finding at all.
Full contract:
`docs/methodology/dual-review.md` > "Plan review is Internal, always".

## Scope reduction — the pre-Decision obligation

A revision that narrows what the proposal will deliver is judged by the
**outcome test** (`dual-review.md` > "Review expectations — the
scope-reduction trap"), which is the canonical statement of the rule.
This section states only what the *proposal stage* owes.

**The baseline is the scope as opened.** Before a Decision, a proposal's
own opening section is the comparison term — not the previous revision,
and not a summary of purpose written later. Measuring against the
previous round would make declining a reviewer's suggested addition read
as a cut, which it is not.

**Declare in the Response or the Revised proposal:**

```
**Scope delta**: preserved | degraded | lost
```

Required when the revision degrades or loses a baseline outcome; omit it
when nothing was narrowed. A `degraded` or `lost` value additionally
carries:

* a grouped **`Removed scope`** block — every removed unit with its
  source section, the reason, and a revival or closure condition, in
  **one record**, not scattered into roadmap rows; and
* a **`Disposition/home`** line naming where each entry now lives.

**Naming a home is the point of it.** "Deferred to a named follow-up"
that names no follow-up is not a deferral; it is a deletion with better
manners. The archive precondition already requires a recorded
disposition for every deferred item, but that binds at *plan-archive*
time — between "review cut this" and "someone archives the resulting
plan," removed scope otherwise lives nowhere but in prose inside a
superseded section. That window is where work disappears, which is why
the home is named at the moment of removal rather than at the end.

**Who allows the loss.** The Maintainer, via the Decision, with the
reduction visible. An author may propose a reduction and a reviewer may
recommend one; neither may concede a baseline outcome.

**Declining a reviewer's proposed expansion is not a reduction.** It
never entered the baseline, so nothing was lost, no declaration is owed,
and no remainder record exists to keep. Record the suggestion and the
reason in the ordinary Response — *Alternatives considered* is the
natural home when the idea is worth preserving.

**And the resolution that should have to argue for itself.** When review
finds a part underspecified, the default is to *specify* it. An author
who instead removes it says why specifying was rejected. That sentence is
the mechanism: it makes the easy path visible as a choice rather than as
an outcome.
