<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/proposals.md doctrine/lifecycle.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# The review-record gate never evaluates `## Code review` sections

**Author**: Claude (Strategy)
**Model**: claude-sonnet-5 (Claude Sonnet 5)
**Date opened**: 2026-08-10
**Status**: proposed
**Touches**: `tools/lifecycle_planner.py` and its byte-identical twin
`templates/skills/_lib/lifecycle_planner.py` (documented here, **not
edited** — see the sequencing fence below); potentially
`doctrine/plans.md` in a follow-on plan, depending on the scope
question this proposal asks the Maintainer to resolve.
**Related**: [`review-gate-enforcement`](../plans/review-gate-enforcement.md)
(open; owns `_pass_headings` / `_has_disposition`, the exact functions
this defect lives in); [`review-efficient-lifecycle`](2026-08-10-codex-review-efficient-lifecycle.md)
(revised, not yet Decided; already names this defect and plans a
review-basis block that touches the same predicate — see *Reconciliation*
below); [`transition-lint`](../plans/transition-lint.md) (open; the plan
that supplies the reproducing evidence)
**Plan review**: required(**External**) — this is lifecycle-enforcement
on a shipped gate, the same category `review-gate-enforcement` and
`review-efficient-lifecycle` both declared External for.

## Context

Cairn's shipped review-record gate validates `## Plan review` sections in
`dev/plans/` artifacts: the two attestation lines (`**Tier**:`,
`**Findings**:`), a calendar-valid date, the closed tier vocabulary, and a
disposition (`### Sharpening` or `## Response to plan review`) when a pass
declares `**Findings**: raised`. It is implemented in
`tools/lifecycle_planner.py` (`review_record_violations`, `_pass_headings`,
`_has_disposition`) and its byte-identical twin
`templates/skills/_lib/lifecycle_planner.py`. This schema is the deliverable
of `review-gate-enforcement`, most recently closed against a CR1/CR2
correction — see *Sequencing fence* below for exact commits.

**The defect.** `_pass_headings` (`tools/lifecycle_planner.py:917-960`,
measured `as_of` its last-touched commit `38a1ad1`) matches the raw heading
line against `_S1_PASS_RE` (`:884-887`):

```python
_S1_PASS_RE = re.compile(
    r"^## Plan review -- (?P<reviewer>[^\n]+?) -- "
    r"(?P<date>\d{4}-\d{2}-\d{2})(?: \(round (?P<round>\d+)\))?$"
)
```

The literal string `Plan review` is the only heading kind this regex can
ever match. `review_record_violations` (`:1036-1100`) iterates
*exclusively* over `_pass_headings(art)`, so **a `## Code review` section
is never evaluated by the gate** — not its Tier, not its Findings, not
whether a raised finding got a disposition. This is not a parser gap:
`_KNOWN_KINDS` (`:535-543`) includes `"code"`, so `_parse_sections`
produces a real `Section` object for every `## Code review -- ... --
YYYY-MM-DD` heading, and `_reviewers()` (`:800-812`) already reads both
kinds for the coarser "does *some* review exist" presence check. The
blindness is specifically in `_pass_headings`'s S1 regex and in
`_has_disposition`'s ceiling search (`:989-1004`), which also keys only on
`s.kind.strip().lower() == "plan review"`.

**Reproduced directly.** `dev/plans/transition-lint.md:1938-1944` carries:

```
## Code review -- Antigravity (External) -- 2026-08-10

**Tier**: External
**Findings**: raised
```

with no `### Sharpening` and no `## Response to plan review` anywhere
after it — exactly the condition the gate refuses for a `## Plan review`
pass. Loading the module and calling `review_record_violations` on that
artifact reports **zero violations** (measured `as_of` commit
`5173288d67951141562271a11d67c43855bdbc53`, reproducible with:

```
PYTHONDONTWRITEBYTECODE=1 python3 -c "
import sys; sys.path.insert(0, 'tools')
import lifecycle_planner as lp
from pathlib import Path
art = lp._read_artifact(Path('dev/plans/transition-lint.md'))
print(lp.review_record_violations(art))"
```

prints `[]`). The parser does see both headings in `art.sections` (`'Code
review'` appears twice — the template stub at line 1009 and the real
section at line 1938 — confirmed by printing `[s.kind for s in
art.sections]`), which is the direct evidence that the gap is in the
filter, not the parse.

## Proposed paths

*(none — this proposal creates no new files; any test/fixture/manifest
paths belong to whichever follow-on plan the Decision opens)*

## Proposal

**This proposal does not implement a fix.** It records the defect, its
measured blast radius under each credible remedy shape, why it sits
outside `review-gate-enforcement`'s existing contract, and an explicit
sequencing fence — so the Maintainer decides scope and direction before
an implementer touches `_pass_headings` / `_has_disposition` again.

### Blast radius — two credible remedy shapes, very different costs

I scanned all 35 `dev/plans/*.md` files (`dev/plans/` + `dev/plans/archive/`,
excluding `_template.md`) `as_of` commit `5173288d67951141562271a11d67c43855bdbc53`,
finding 23 `## Code review -- <reviewer> -- YYYY-MM-DD` passes (S1-shaped,
substituting "Code" for "Plan") across 21 files.

**(A) Full parity with the Plan-review schema** — require the same
`**Tier**:` / `**Findings**:` attestation lines and disposition pairing on
`## Code review` that S1-S9 requires on `## Plan review`. This would make
**21 of 35 plan files (60%) newly violate**, enumerated below. Every one but
`transition-lint.md` fails on `missing Tier` / `missing Findings` — those
lines are simply absent, because no Code review in this tree before today
was ever asked to carry them:

```
dev/plans/archive/adopter-entry-doc-refresh.md
dev/plans/archive/adopter-licensing-compliance.md
dev/plans/archive/ast-known-new-repin.md
dev/plans/archive/byline-classification.md
dev/plans/archive/default-security-stance.md
dev/plans/archive/first-session-survivability.md
dev/plans/archive/gate-claims-vs-enforcement.md
dev/plans/archive/interpreter-trust-root-fallback.md
dev/plans/archive/lockfile-provenance-fields.md
dev/plans/archive/profile-parse-fail-open.md
dev/plans/archive/record-corrections.md
dev/plans/archive/release-authenticity.md
dev/plans/archive/release-security-orchestration.md
dev/plans/archive/review-record-integrity.md
dev/plans/archive/scan-coverage.md
dev/plans/archive/separator-detection.md
dev/plans/archive/solo-legacy-adopter-path.md
dev/plans/fork-advisory-semantics.md
dev/plans/portable-security-sweeps.md
dev/plans/review-gate-enforcement.md
dev/plans/transition-lint.md
```

**(B) A narrow S7-only extension** — require a disposition to follow a
raised finding *only on a `## Code review` section that already declares a
`**Findings**:` line* (i.e. never require the line to exist; only close the
disposition-pairing hole where a reviewer already opted into that
vocabulary). Measured over the same 23 passes: **exactly 1 of 35 files
newly violates — `dev/plans/transition-lint.md`**. It is the *only* Code
review pass anywhere in the tree, live or archived, that carries a
`**Findings**:` line at all; every other Code review author never used
that vocabulary, so (B) leaves them untouched.

The 60-percentage-point gap between (A) and (B) is the actual design
question. It is not a rounding difference to wave past.

### Why (A) would be enforcing the wrong contract

`doctrine/plans.md` documents **two different, separately-authored**
formats, and Code review's is not Plan review's with the label swapped:

* **`### The record schema — what a pass must carry`**
  (`doctrine/plans.md:571-662`) is written, headed, and grammar-keyed
  entirely to `## Plan review -- <reviewer> -- YYYY-MM-DD`
  (`doctrine/plans.md:577-578`). The `**Tier**:` / `**Findings**:`
  attestation lines, the tier-ordering comparison, and the
  Sharpening-or-Response disposition pairing are all defined here, for
  this heading shape, and nowhere else.
* **`## Code review — doctrine`** (`doctrine/plans.md:724-782`) is a
  separate section with its own, different format: "Findings as a
  numbered list with `accept (commit <sha>)` / `guard (<path>::<node>)` /
  `defer` / `wontfix` dispositions" (`:731-733`). No Tier line. No
  `**Findings**: none|raised` attestation. A different disposition
  vocabulary entirely (per-finding tokens, not a Sharpening subsection).

Measured fact (B) already shows the practical consequence: 20 of 21 live
Code review passes never used the Tier/Findings vocabulary at all —
because it was never asked of them. `transition-lint.md`'s reviewer
borrowed it informally from the adjacent Plan-review convention; that is
not evidence the convention was ever adopted for Code review. Widening (A)
onto this corpus would retroactively fail the 20 files that correctly
followed the *actual* documented Code-review format, for not following a
format that was never theirs.

### Scope: is this inside `review-gate-enforcement`'s contract, or new?

**Argued conclusion: new scope**, on four points, not an assertion:

1. `review-gate-enforcement`'s own *Source proposal* section frames the
   original defect as: "The gate ... clears on the *presence* of a section
   named 'Plan review' ... Four documented promises — the declared tier,
   the `##` heading level, the date, and a `### Sharpening` subsection when
   findings were raised — are unenforced" (`dev/plans/review-gate-enforcement.md:39-42`).
   Every noun in that sentence is Plan-review-specific; Code review is not
   named.
2. The plan's own `## Scope` section (`:55-84`) lists `doctrine/plans.md`
   "the grammar reconciliation, and **the review-record format**"
   in-scope, under a Decision condition about reconciling "the ##/###
   grammar" — again framed around the Plan-review grammar the Decision was
   reacting to. Nothing in Scope or Out-of-scope names Code review.
3. The plan's own just-landed closing review says so directly. The
   External Code review at `dev/plans/review-gate-enforcement.md:1766`
   (Antigravity, `2026-08-10`, closing the CR1/CR2 correction) states at
   `:1803`: "Confirmed CR1/CR2 fixes touch only `Plan review` headings and
   dispositions without widening or narrowing `## Code review` section
   handling." The reviewer of record for the functions this defect lives
   in affirms, in the same sitting, that Code-review handling was
   deliberately left alone.
4. Measured fact from *Blast radius* above: only 1 of 21 live Code review
   passes uses the attestation vocabulary S1-S9 checks for. A schema that
   0.95 of its target population never adopted was not built for that
   population.

I did not find a construction of "existing contract" under which this
defect is `review-gate-enforcement`'s to fix silently. It is the same
*kind* of defect (a documentary promise the gate does not enforce) but a
different *surface* (Code review's own, separately-documented format), and
opening it as its own proposal — rather than reopening a plan whose Code
review just shipped SHIP — is the position this document takes.

### Sequencing fence

The task that produced this proposal was framed to me as: "those exact
functions are under independent review right now over range
`a62a5d2..38a1ad1`." **Re-measured, that framing is stale as of this
proposal's own drafting**, and I am reporting what I found rather than
carrying the original framing forward unchecked (per this project's
re-derive-every-figure discipline):

* `a62a5d2` (2026-08-05T19:27:34-04:00) is an ancestor of `38a1ad1`
  (2026-08-10T10:48:57-04:00, "review-gate-enforcement: close CR1 and CR2
  -- exact S1 selection, exact disposition kind") — the correction commit
  the range names.
* Fourteen minutes later, `8cf0a00` (2026-08-10T11:02:00-04:00,
  "review-gate-enforcement: append external code review") lands the
  External Antigravity Code review closing that correction:
  `**Findings**: none`, `Verdict: SHIP`, quoted above at point 3.
* So as of `8cf0a00` **the correction review has closed**, not "is
  in-flight" — the range is no longer under an open reviewer.

The fence is still real, just for a different reason than originally
stated. `dev/plans/review-gate-enforcement.md`'s own `**Status**:` line
reads `open` (measured `as_of 5173288`), and its `## Lasting-truth
migration` section is unfilled — the plan has not archived. Per this
project's own archive-precondition doctrine, a plan's implementation range
is not the durable record until it archives. **Recommendation: any
implementation touching `_pass_headings` / `_has_disposition` waits until
`dev/plans/review-gate-enforcement.md` reaches `archived` status**, so a
follow-on plan for this proposal opens against those functions' settled,
historical shape rather than a freshly-landed, not-yet-archived one. This
is a weaker fence than "wait for the reviewer," and I am flagging that
weakening explicitly rather than silently keeping the stronger original
claim.

### Reconciliation with `review-efficient-lifecycle`

`dev/proposals/2026-08-10-codex-review-efficient-lifecycle.md` (Status:
`revised`, no Decision yet — **not edited by this proposal**) already
names this exact defect. Its Advisory read section states: "Found
2026-08-10: the shipped review-record gate filters to `## Plan review` and
never evaluates `## Code review`, so a code review declaring `**Findings**:
raised` with no disposition passes unflagged. This proposal adds a
review-basis block to code reviews; if the gate is widened to that section
kind, those fields become gate-checkable there. The two changes touch the
same predicate and should not be designed independently" (lines 527-533).
Its accepted Revision 1 goes further, requiring for inherited plans a
`Contract non-expansion: VERIFIED | NOT VERIFIED` attestation *inside* Code
review (lines 731-737), and states explicitly: "This plan must coordinate
the proposal, plan, and code-review section predicates so a code review
carrying findings cannot pass merely because an existing gate filters only
plan-review headings" (lines 780-783).

That proposal is itself sequenced behind `review-gate-enforcement`'s exact
review-record grammar work (its own Response, line 608: "Implementation
waits for the exact review-record grammar dependency to clear code
review"). So three lifecycle-enforcement changes now touch the same
"what must a Code review section carry" predicate: this proposal,
`review-efficient-lifecycle`'s review-basis block, and its non-expansion
attestation. Designing a Code-review record schema three times,
independently, on the same tree in the same week is the failure mode
*this* proposal exists to flag, not repeat.

### Recommended direction (for the reviewer and Maintainer to weigh, not a foregone conclusion)

1. **Do not implement remedy (A)** — full Plan-review parity — its blast
   radius (21/35 files) is collateral damage against a convention Code
   review authors were never asked to follow, and it would be enforcing a
   schema `doctrine/plans.md` does not document for that heading kind.
2. **Prefer folding this into `review-efficient-lifecycle`'s reconciliation**
   rather than shipping a standalone fix here. That proposal is already
   designing the Code-review-side predicate (the review-basis block, the
   non-expansion attestation) and has already flagged needing to reconcile
   with this exact gap. A second, independently-designed Code-review
   schema landing first would very likely need revising once that
   proposal's Decision lands.
3. **If the Maintainer wants an interim fix ahead of that proposal's
   Decision**, remedy (B) — the narrow S7-only extension, gated on an
   already-present `**Findings**:` line — is the only shape measured here
   with a blast radius proportionate to the actual defect (1 file, the one
   that reproduces it).

### Documentation / doctrine surface

None from this proposal directly — it implements nothing. **If** the
eventual direction is a standalone Code-review record schema (remedy B, or
a superset), that would add a new subsection to `doctrine/plans.md`'s
"## Code review — doctrine" (`:724-782`) analogous to "### The record
schema" (`:571-662`) but keyed to Code review's own disposition vocabulary
— a documentation change that follow-on plan owns, not this proposal.

### Doctrine-change rate-limit

This proposal changes no doctrine itself. Its live open question — whether
to formalize a Code-review record schema — **would** be a doctrine change
if a follow-on plan adopts it, and that follow-on would need to clear the
gate (`doctrine/rationale.md` > "How the doctrine evolves under evidence")
independently. Argued here rather than asserted: the single reproducing
incident (`transition-lint.md`, the one file in the whole 35-file corpus
that hit this) does not on its own clear the **recurrence** bar (≥2
occurrences in a rolling window) — it is one incident, not a pattern, by
this proposal's own measurement. The two credible routes to clearing it
are (a) the Maintainer's **high-risk classification** of lifecycle
enforcement on a shipped gate, which is a defensible read given
`review-gate-enforcement` and `review-efficient-lifecycle` both already
carry `required(External)` on exactly this basis, or (b) folding the work
into `review-efficient-lifecycle`, which has already cleared the rate
limit via the goodnight-synthesis route (its own "Doctrine-change
rate-limit" section) and already scopes a code-review predicate change.
Route (b) avoids opening a second, competing rate-limit clearance on the
same predicate and is the reading this proposal leans toward, without
deciding it — that is the Maintainer's call.

## Rationale

* **Which user workflow does it improve?** The review-record gate exists
  so an author or reviewer can trust a clean `scan` / `next` result as
  evidence a plan's review record is structurally sound. Right now that
  trust is false for half the record — a Code review can carry an
  unaddressed raised finding and the gate reports nothing. Surfacing this
  (even before any fix lands) stops the gate's clean-pass output from being
  read as stronger evidence than it is.
* **What stable contract or module boundary does it preserve or clarify?**
  It clarifies, with measurement rather than assumption, that Code
  review's documented contract (`doctrine/plans.md:724-782`) is genuinely
  different from Plan review's (`:571-662`) — a fact the corpus already
  reflects (20/21 Code reviews never used the Plan-review vocabulary) but
  that was not previously stated anywhere durable.
* **Why is now the right time?** The defect was found today, during active
  work on the exact functions it lives in (`review-gate-enforcement`,
  just closed) and adjacent to a pending proposal
  (`review-efficient-lifecycle`) already designing the same predicate.
  Recording it now, before either lands further, is cheaper than
  discovering the collision after both have shipped independently.

## Alternatives considered

* **Say nothing; let `review-efficient-lifecycle`'s reconciliation note
  carry the whole record.** Rejected: that note is two sentences inside an
  advisory read that "does not discharge any tier" and is not itself
  reviewed record for *this* defect — it names the gap but carries none of
  the measured blast radius, the doctrine-divergence argument, or the
  sequencing fence. Those need their own citable home.
* **Implement remedy (A) directly, accepting the 21-file blast radius as a
  one-time cleanup.** Rejected in the *Recommended direction* above: it
  enforces a schema Code review was never asked to follow, on evidence
  (doctrine's own separate Code-review section) that contradicts treating
  Plan-review's schema as the default.
* **Implement remedy (B) directly, in this proposal's own plan, without
  waiting on `review-efficient-lifecycle`.** Considered and not
  recommended, not rejected outright: it is the minimal, proportionate
  fix, but landing it independently means a second author designs the
  same "what must a Code review carry" predicate concurrently with
  `review-efficient-lifecycle`'s non-expansion attestation, which is the
  exact duplication this document's *Reconciliation* section argues
  against.
* **Do nothing.** Rejected: the gate's clean output is misleading for
  exactly the artifact class (implementation-side review) the archive
  precondition treats as mandatory gatekeeping ("a plan never archives
  until code review occurred," `doctrine/lifecycle.md`).

## Evidence / verification plan

This proposal implements nothing, so there are no tests to name for *this*
document. The measurements above are themselves the evidence and are each
independently reproducible from the commands quoted inline (the
`review_record_violations` zero-result on `transition-lint.md`; the 35-file
/ 23-pass / 21-file-vs-1-file blast-radius scan). Whichever remedy a
follow-on plan adopts inherits `review-gate-enforcement`'s existing test
home, `bootstrap/tests/test_lifecycle_contract.py`, and must add: a
positive fixture (a Code review declaring `**Findings**: raised` with no
disposition, refused); a negative fixture (the same, with a disposition,
accepted); and — if remedy (A) or any Tier/Findings requirement is ever
chosen — a fixture proving the legacy-manifest mechanism
(`_LEGACY_PASSES`, `scripts/gen_legacy_passes.py`) is extended to Code
review's own generated population before the 21-file corpus is asked to
carry the new attestation, mirroring how S9 protects the Plan-review
corpus today.

### Author-accounting — invariants, failure modes, edge cases

* **Invariant this proposal establishes**: none yet — it is a
  documentation-and-decision artifact, not an implementing one. The
  invariant a follow-on plan would establish (whichever remedy is chosen)
  is "a Code review section declaring `**Findings**: raised` carries a
  disposition before the plan may reach `archived`" — enforced by
  extending `review_record_violations` or a sibling function, tested by
  the fixtures named above.
* **Failure modes**: N/A for this proposal (no code path added). For a
  follow-on implementation: fail-closed is required (a malformed or
  ambiguous Code-review disposition should read as "no violation reported"
  only when a reviewer has explicitly said so, never by default), mirroring
  S1-S9's own "no condition yields a silent pass" rule
  (`doctrine/plans.md:575`).
* **Edge-case inventory**: N/A — deferred to the follow-on plan. Candidates
  it will need to account for: a Code review with no `**Findings**:` line
  at all (remedy B's design leaves this alone — confirmed correct by the
  20/21 measurement above); multiple Code review passes in one plan
  (`review-gate-enforcement.md` itself has two, `separator-detection.md`
  has two); a Code review whose disposition uses Code review's *own*
  documented vocabulary (a numbered `accept`/`guard`/`defer`/`wontfix`
  list) rather than `### Sharpening` — remedy (B) as measured above only
  checks for `### Sharpening` / `## Response to plan review`, which is the
  *wrong* disposition vocabulary for Code review's own doctrine and would
  need correcting before implementation, not copied verbatim from S7.
* **Known omissions**: this proposal does not resolve which remedy ships,
  does not draft the doctrine subsection a schema would need, and does not
  touch `dev/plans/review-gate-enforcement.md` or
  `dev/proposals/2026-08-10-codex-review-efficient-lifecycle.md` (both
  explicitly out of scope for this session).

#### Security preflight

N/A: no trust boundary added, moved, or widened. This proposal documents a
gate's blind spot in a read-only conformance checker; it adds no
deserialization, subprocess, network, or credential surface.

### Tests required

N/A for this proposal directly (no code changes). The follow-on plan's
test-home mapping is named under *Evidence / verification plan* above.

### Examples / smoke checks

* `scripts/claim_check.py dev/proposals/2026-08-10-claude-code-review-blindness.md`
  — run clean before commit.
* `scripts/check_cairn.py` — run clean before commit (link resolution +
  claim-path check over this file).

## Signals the change is wrong

* A reviewer or the Maintainer identifies a Code review in the corpus that
  legitimately uses `### Sharpening` / `## Response to plan review` as its
  disposition and remedy (B) would still refuse it — the measurement above
  found none, but a follow-on plan should re-run the scan against its own
  `as_of` commit before trusting this proposal's count.
* `review-efficient-lifecycle`'s Decision lands with a Code-review
  predicate materially different from remedy (B) — in which case this
  proposal's recommended direction (fold into that work) was correct and
  this document's job is done without a separate implementation.
* The Maintainer classifies this as *not* high-risk and declines the
  doctrine-change rate-limit route — in which case any schema-formalizing
  remedy stays blocked until `review-efficient-lifecycle` lands (or a
  second recurrence is measured), and this proposal's job was to document
  that blockage precisely, not to route around it.

## Reviewer brief

Falsify the four scope-argument points independently of my reading —
especially point 3 (the closing Code review's own "did not widen or narrow
Code review handling" statement) and the blast-radius numbers themselves
(re-run the scan at your own `as_of` commit; the tree is under concurrent
edit and a fresh count may differ from mine). Attack whether "new scope"
is actually correct, or whether `review-gate-enforcement`'s Decision
condition ("treats the adopter-facing record-format change as in scope")
is broad enough to have already covered this. If it does, the sequencing
fence in this proposal (wait for archive) would need to become "this
IS `review-gate-enforcement`'s unfinished business," which changes who
owns it.

## Scope addendum -- 2026-08-10 -- the synthesized-pass ceiling basis

Appended before any review pass, to claim a residual that would otherwise archive
without a home.

`review-gate-enforcement`'s CR1 correction (`38a1ad1`) introduced
`_synthesize_pass_section`, so `_pass_headings` now recognises S1-conforming
headings that `_HEADER_RE` cannot parse. **`_has_disposition`'s ceiling was not
updated to match**: it still derives its later-pass boundary from `art.sections`
rather than from the union of raw S1 lines `_pass_headings` now recognises. A
*synthesized-only* later pass therefore does not act as a ceiling, so a
neighbouring round in that exact shape could satisfy the wrong pass's disposition
search.

**This is a different defect from the blindness above**, and the distinction is
why it needs claiming rather than assuming: the blindness is that the ceiling keys
on `s.kind == "plan review"` and so never sees `## Code review`. This residual is
that the ceiling's *basis* (`art.sections`) is narrower than the selection's
(`art.sections` ∪ raw S1 matches). Same function, same computation, two independent
narrownesses.

**Status: reachable, and safe today.** The 2026-08-10 External code review
(Antigravity) traced it, **demonstrated reachability in Python**, then scanned all
36 files across `dev/plans/` and `dev/plans/archive/` and found **0
synthesized-only passes in live artifacts**. So it cannot currently mis-satisfy
anything; it is a latent asymmetry, not an active defect.

**Why this proposal owns it.** The change proposed above rewrites
`_has_disposition`'s ceiling search to consider `## Code review` sections. Any
implementation that touches that computation should correct its basis in the same
pass — fixing one narrowness while leaving the other in the same four lines would
be the exact "strict component over permissive neighbour" shape that produced CR1.
The implementation must widen the ceiling basis to the same union
`_pass_headings` selects from, and pin it with a synthesized-only-later-pass
fixture (which no live artifact supplies, so the fixture must be constructed).

Recorded here so `review-gate-enforcement` can archive with this residual owned
rather than orphaned.
