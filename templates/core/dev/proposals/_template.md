<!-- Author tip: if your proposal cites count claims (numbers
     adjacent to `lines` / `proposals` / `plans` / `tests` /
     `commits` / `files`), claim_check will soft-flag them.
     Four clearance paths -- see "Count claims" section below for
     details:
       1. Rephrase to a delta
       2. Cite the command that computed the count
       3. Add an inline `<!-- claim-check-allow-count: N noun -->`
          directive next to the claim
       4. Consciously accept in the implementing commit body
     -->

# Proposal template

> **This is the proposal template.** To open a proposal, copy the
> section template below the horizontal rule into
> `dev/proposals/<YYYY-MM-DD>-<author>-<short-slug>.md`, fill it,
> and commit it with status `proposed`. The doctrine above the
> rule is reference — read it once, then work from the sections
> below.

## The lifecycle

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
* **revised** — the author appends a `## Response` and, where
  needed, a `## Revised proposal`. Review and revision may repeat.
* **accepted / rejected / superseded** — the Maintainer appends
  the `## Decision`. **The Decision commit does not archive an
  *accepted* proposal**: it stays in `dev/proposals/` and moves to
  `archive/` later — at the plan-open commit (non-trivial work) or
  the trivial-implementing commit. Only a *rejected* or *superseded*
  proposal archives in the Decision commit itself. See "File moves"
  below for the full rule.

The directory location encodes **work-status** (queued without
plan / in-flight with plan / shipped); the `Status:` field encodes
**deliberation state**. Two orthogonal axes. See
[`dev/plans/_template.md`](../plans/_template.md) for the plan
counterpart and the trivial-vs-non-trivial triage rule.

Two rules are bright-line — **append-only** and **one commit per
transition** — each detailed in its own subsection below.

**A proposal is a Stage 1 Registered Report.** Scientific
publishing has the same shape: a study's design and analysis plan
are reviewed and accepted *before* any data is collected (Stage 1),
and the results are later reviewed against that pre-registered
plan (Stage 2). A proposal locks the change's design *and* its
evidence / verification plan before any code is written — that is
Stage 1. The plan and its code review (see `../plans/_template.md`)
then check the implementation against that lock — Stage 2. The
discipline is a defense against post-hoc *metric p-hacking*: the
verification plan exists before the implementation, so evidence is
judged against a commitment, not chosen after the fact to flatter
whatever the code happened to do.

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
typo-guarded). See `dev/agent_collaboration.md` / the lifecycle
doctrine, and the marker doctrine below.*

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

<!-- cairn:slot triage-extra-triggers -->
(Adopter-specific triage triggers beyond the general list above — e.g.
a domain assumption class the project guards, or a protected-contract
registry. Fill with your project's extra "open a proposal when…"
bullets, or replace with `N/A: no project-specific triggers`. An
unfilled slot is a review finding.)
<!-- cairn:end triage-extra-triggers -->

Everything else — a new helper, a test, a typo fix, a docstring
polish, a self-contained refactor — just commit. The proposal system
is for "I want to bake this in for a while; let's check it first."

Once accepted, the implementation is **trivial** (a single commit, a
single area, no follow-ups — implemented and the proposal archived
together) or **non-trivial** (multiple commits or areas, multi-stage
sequencing, or deferred follow-ups — it opens a plan; see
`../plans/_template.md`).

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
gate; see `../plans/_template.md` > "The plan-review precondition").

**Escape hatch.** If a change is urgent, clearly reversible, or
explicitly experimental, it may proceed without a proposal, but the
commit or follow-up note should say why the proposal step was
skipped. This keeps the bypass traceable without forcing process
onto bug fixes or short-lived experiments.

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

All three markers exempt only the tokens on the marker line itself;
count claims still soft-flag. See `claim_check`'s module docstring
(the "Marker lines" subsection) for the full mechanism documentation.

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
  sequencing, OR carries deferred follow-ups — see the
  [Plan triage rule](../plans/_template.md#plan-triage-rule) in
  `dev/plans/_template.md` for the canonical formulation), the
  implementing agent first opens a plan in `dev/plans/` per
  [`dev/plans/_template.md`](../plans/_template.md). The plan-open
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

## Archive preconditions

Before flipping status to `accepted` / `rejected` / `superseded` and
moving the file to `archive/`, every **deferred follow-up item**
named in the proposal must have a durable home outside the proposal
text. Acceptable homes:

* `dev/PLANNING.md` — a tier item, a follow-up backlog, or a new
  dedicated subsection.
* A topic doc's "Future work" section.
* Its own queued follow-up proposal at
  `dev/proposals/<date>-<author>-<short-title>.md`.

`dev/NEXT_SESSION.md` is not an archive-time home — it is edited only
at the goodnight routine and on explicit user instruction. A small,
pickable-cold follow-up goes to `dev/PLANNING.md` here; the goodnight
scrub then surfaces it into `NEXT_SESSION.md`.

The archive commit body must name where each deferred item went, in
the form:

```
Follow-ups migrated to:
* <item> -> dev/PLANNING.md > <subsection> #N
* <item> -> docs/<topic>.md > Future work
* <item> -> dev/proposals/<date>-<author>-<title>.md (queued follow-up proposal)
```

This makes the migration auditable from `git log` alone. The same
rule applies to plan files in `dev/plans/` when they archive; the
canonical statement lives at `dev/PLANNING.md > Archive
preconditions (proposals and plans)`.

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
[Triage rule](#triage-trivial-vs-non-trivial)"). A deferred
follow-up that names only a trigger leaves a downstream agent
guessing whether the design is pre-approved.

## Count claims -- soft-flag clearance

`claim_check` soft-flags any **count claim** -- a number directly
adjacent to one of six tree-nouns: `lines`, `proposals`, `plans`,
`tests`, `commits`, `files`.  Example soft-flag triggers:

* "5-10 files at scale" (forward-looking range estimate)
* "281 tests" (live-computed from `pytest --collect-only`)
* "12,847 nodes" (-- **not** a tree-noun, doesn't flag)
* "13 CHANGELOG entries" (-- **not** a tree-noun, doesn't flag)

<!-- claim-check-allow-count: 10 files, 281 tests, 10 commits -->
<!-- ^ This template's own teaching examples are self-exempted
     here (incl. the "5-10 commits" prescriptive-rule example in
     mechanism (3) below).  The inline directive form is mechanism (3);
     this section thus demonstrates its own recommended pattern. -->

The flag's job is to catch **memory-quoted absolute counts** that
should be deltas or live-computed; the scanner can't tell legitimate
counts from misremembered ones.  Four clearance mechanisms exist;
pick one per claim:

1. **Rephrase to a delta** -- "+5 files vs current N" rather than
   an absolute number.  Best when the claim is structurally a
   change-size.
2. **Cite the command that computed the count** -- "281 tests (per
   `pytest --collect-only`)."  Best for live-from-probe claims; the
   adjacent command names the cheap defense the reader can re-run.
3. **Inline `<!-- claim-check-allow-count: N noun, ... -->`
   directive** -- exempts specific count tokens on adjacent prose.
   Best for forward-looking range estimates ("at scale")
   where rephrasing would lose information.  **Reserved for
   prescriptive rules (e.g., doctrine wording like "5-10 commits")
   or historical quotes; never for live / mutable counts where
   mechanisms (1) delta or (2) cited command would be cleaner.**
   Multiple nouns per line; multiple directives per document.
   Example:

       The catalog will hold roughly a dozen theory files at scale.

       <!-- claim-check-allow-count: 12 files -->

4. **Consciously accept in the implementing commit body** -- name
   the count, name why the soft flag is acceptable (forward-looking
   estimate, live-probe, etc.), and the commit body becomes the
   audit trail.  Use sparingly -- (3) is usually cleaner; (4) is
   the fallback when inline-exempt would clutter the prose.

**Avoid the discipline antipattern**: do **not** rephrase by
substituting non-tree-nouns purely to avoid the flag (e.g., "five
theory documents" instead of "5 files").  The discipline targets
quoted absolute counts; substituting nouns hides the count rather
than grounding it.

<!-- claim-check-allow-count: 5 files -->
<!-- ^ The "+5 files" delta-example in mechanism (1) above and
     the "5 files" antipattern example are self-exempted here. -->

---

# {{proposal title}}

**Author**: {{name / role}}
**Model**: {{your actual running model — query and state it; don't copy a label from an old template or archive}}
**Date opened**: {{YYYY-MM-DD}}
**Status**: proposed
**Touches**: {{the files / surfaces this changes}}
**Related**: {{roadmap links, prior proposals, commits, issues}}
**Plan review**: {{if non-trivial — required(<tier>) | not required(<rationale>); ratified at Decision}}

## Context

What problem is being solved? What is the felt pain that triggered
this? Cite specific files, commits, or issues.

## Proposed paths

*(Optional. Populate as forward-reference paths accrue — files this
proposal would create, surfaces it would touch into existence — so
they don't trigger `claim_check` while the proposal is being authored.
Each entry is the path **and** a one-line note on what it is / when it
materializes. Remove the section if empty. Once a path resolves on
disk, drop its line.*

*Three structural rules for the marker to work: (a) the literal
`Proposed paths:` line below is the marker `claim_check` matches —
don't drop it while bullets remain; (b) **no blank line between
the marker line and the first bullet** — `claim_check`'s
continuation check uses original line numbers, so a gap breaks
adjacency; (c) **keep each bullet on a single physical line** —
wrapped/indented bullet continuations close the marker block and
re-expose subsequent paths to hard-check.)*

Proposed paths:
- `path/to/proposed/file.md` — what it is; when it lands.

## Proposal

The change, concretely — name files, signatures, contracts. What
is added, changed, or removed.

### Documentation / doctrine surface

What documentation, doctrine, or contract surface does this change
touch? If none, say so explicitly — silent omission is a review
finding.

<!-- cairn:slot documentation-tier-home -->
(Filled from the `documentation-plan` default-on module when installed
— paste content from `dev/modules/documentation-plan.md` > "Merged
into" > Block 2: dev/proposals/_template.md. The merged content names
the per-layer routing rule for doc + doctrine changes, pointing at
`docs/DOCUMENTATION_PLAN.md`. If documentation-plan is not installed,
replace with `N/A: documentation-plan not installed`. An unfilled
slot is a review finding.)
<!-- cairn:end documentation-tier-home -->

### Doctrine-change rate-limit (if this proposal changes doctrine)

If this proposal **changes doctrine** — a rule, process, or
contract every contributor follows — it must clear the
doctrine-evolution gate (`doctrine/rationale.md` > "How the
doctrine evolves under evidence"). Link the justification here:

* the **recurrence** evidence (the same failure shape, ≥2 times in
  a rolling window), or
* the Maintainer's **high-risk classification** (a security or
  data-loss surface), or
* the **goodnight-time synthesis** that aggregated the signal into
  this proposal.

A single incident does not justify a doctrine change unless it is
the high-risk case. *This prompt applies to a proposal that
introduces a **new** doctrine change. A proposal that merely
**syncs or ports already-accepted doctrine** from one place to
another is not itself a new change — it cites the original
accepting Decision and the gate does not re-apply.*

## Rationale

Why this change, and why now — the user-facing or project-facing
improvement it delivers. Per the collaboration agreement's review
checklist:

* Which user workflow does it improve?
* What stable contract or module boundary does it preserve or clarify?
* What domain-specific transparency, reproducibility, or correctness
  does it improve? (if applicable)
* Why is now the right time?

## Alternatives considered

What else was on the table? Why does this win? Naming the alternatives
is more important than picking the best one — it forces the reviewer
to push back at the right level. Include "do nothing". If the draft
incorporates the Maintainer's chat-mode preferences, cite them here
(or in *Rationale*) as **"maintainer preference during drafting"**
with the quote or paraphrase — chat input shapes the draft but is not
the Decision (see `doctrine/lifecycle.md` > "Chat preferences are not
a lifecycle Decision").

## Evidence / verification plan

What proves the change works, and what signal would tell us it's
wrong?

The three things every change accounts for: the **tests** that prove
it, the **examples / smoke checks** that exercise it end-to-end, and
the **docs** it delivers (named earlier under `## Proposal >
Documentation / doctrine surface`). Name each, or give an explicit
"**N/A**: <reason>" — silent omission is a review finding.

### Tests required

<!-- cairn:slot tests-tier-home -->
(Adopter-specific test-tier taxonomy — name the project's test
directories and speed / environment markers so the author can route
the required tests by tier and by name. Fill from the project's test
plan, or replace with `N/A: no tiered test layout`.)
<!-- cairn:end tests-tier-home -->

### Examples / smoke checks

<!-- cairn:slot examples-smoke-home -->
(Adopter-specific examples / smoke-check surfaces — the gallery, CLI
sanity commands, notebook smokes the change can exercise end-to-end.
Fill with the project's runnable checks, or replace with `N/A: no
end-to-end exercisable surface`.)
<!-- cairn:end examples-smoke-home -->

## Signals the change is wrong

The observations that would show this change should be reverted or
rethought — and the recovery for each.

## Review -- {{reviewer}} -- {{YYYY-MM-DD}}

**Model**: <your actual running model or tier when known; "unknown" if not. Do not copy-paste old model labels from past templates or archives; query and state your running model identity.>

Proposal reviews are written into the proposal file by default.
Chat comments can help the conversation, but they are not the durable
review record. Append the review as a new section in this file,
commit that lifecycle transition, and let the author's Response
answer the numbered critiques here.

**Steelman first** (per the review norms in
`dev/collaboration_agreement.md`). What's right about this proposal?

Then critique. Number each substantive concern so the response can
address them point-by-point. Use the project's review lenses where
relevant (workflow coherence, data contracts, extensibility,
operational maturity).

Critiques are prose-first. When a critique is *also* a specific edit
suggestion, attach it in one of two forms:

* **Inline suggested edit** — a fenced code block under the critique
  showing the proposed wording / code. Best for small fixes:

      * **[R2]** The triage rule reads as too narrow. Suggested edit:

          > Open a proposal only when the change ... **or when the
          > author wants a second opinion before baking it in.**

* **Review branch** — for substantive rewrites, create a branch
  named `<reviewer>/review-of-<original-slug>` with your edits as
  commits and reference the commit hash(es) in the critique. The
  author can cherry-pick or merge selectively. Push only with
  explicit Maintainer approval (per `AGENTS.md`'s "never commit or
  push without explicit user approval" rule).

      * **[R5]** Section X needs a stronger case. Suggested rewrite
        on branch `<reviewer>/review-of-<slug>` (commits `<sha>`).

Stick to prose-only when the critique isn't an edit — conceptual
concerns, questions, and steelmans don't fit in a diff.

* **[R1]** ...
* **[R2]** ...
* **[R3]** ...

## Response -- {{author}} -- {{YYYY-MM-DD}}

**Model**: <model or tier when known; "unknown" if not>

### Disposition grammars (two normalized vocabularies)

Response sections use one of two disposition-grammar vocabularies
depending on whether the implementing commit already exists. Pick the
grammar based on context:

**Proposal-Response grammar** (this section — the implementing
commit does NOT yet exist; the Response is part of the
proposal-revision cycle, NOT a code-review record):

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
* `reject` — with reason.
* `defer` — to a follow-up plan / proposal.
* `wontfix` — explicit non-action with rationale.

The split exists because the proposal-Response context predates any
implementing commit — there is no `<sha>` to cite when the Response
is part of the proposal's revision cycle. Conflating the two grammars
created a "fill in a fake sha" failure mode that the split prevents.

### How to write the Response

For each numbered critique, write one disposition token from the
grammar above plus a one-sentence rationale. No silent dropping.
Brief is fine; precision matters more than length.

Proposal-Response example (no implementing commit yet):

* **[R1]** accept — will incorporate in the next revision.
* **[R2]** accept with modification — author-specified change named
  inline: <rephrase the reviewer's edit so the spirit is preserved
  but the exact text differs>.
* **[R3]** reject — the assumption holds for the documented case;
  see <the relevant module / section>.
* **[R4]** defer — this depends on a default only the Maintainer can
  settle.

Code-review-Response example (implementing commits exist):

* **[F1]** accept (merged at <sha>) — ...
* **[F2]** accept (rewrote inline) — ...
* **[F3]** accept (followup commit <sha>) — ...

If accepted critiques substantially change the proposal, write a short
"## Revised proposal" section above this and update `Status:` to
`revised`.

## Decision -- {{Maintainer}} -- {{YYYY-MM-DD}}

Final call: accept, reject, or supersede. Brief reasoning. Optional:
link to the commit(s) that implemented the accepted version.

If accepted and the change touches the roadmap, add a corresponding
`dev/PLANNING.md` entry in the same commit.

*If an agent scribes this Decision at the Maintainer's instruction:
quote or clearly paraphrase the Maintainer's instruction, name the
scribe, and record whether commit permission was explicitly given or
separately confirmed (per `AGENTS.md`'s Decision-commit guard-rail).*
