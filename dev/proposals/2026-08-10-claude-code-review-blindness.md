<!-- cairn-internal-ref-allow: doctrine/plans.md doctrine/dual-review.md doctrine/proposals.md doctrine/lifecycle.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# The review-record gate never evaluates `## Code review` sections

**Author**: Claude (Strategy)
**Model**: claude-sonnet-5 (Claude Sonnet 5)
**Date opened**: 2026-08-10
**Status**: revised
**Touches**: `tools/lifecycle_planner.py` and its byte-identical twin
`templates/skills/_lib/lifecycle_planner.py` (documented here, **not
edited** — see the sequencing fence below); potentially
`doctrine/plans.md` in a follow-on plan, depending on the scope
question this proposal asks the Maintainer to resolve.
**Related**: [`review-gate-enforcement`](../plans/archive/review-gate-enforcement.md)
(open; owns `_pass_headings` / `_has_disposition`, the exact functions
this defect lives in); [`review-efficient-lifecycle`](2026-08-10-codex-review-efficient-lifecycle.md)
(revised, not yet Decided; already names this defect and plans a
review-basis block that touches the same predicate — see *Reconciliation*
below); [`transition-lint`](../plans/archive/transition-lint.md) (archived
2026-08-10; the plan that supplies the reproducing evidence)
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

**Reproduced directly.** `dev/plans/archive/transition-lint.md:1945-1951` carries
(line numbers as of the 2026-08-10 archive commit; they were `1938-1944` before
that commit's header edits shifted the file by 7 lines — the content is
unchanged, only its position moved):

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
art = lp._read_artifact(Path('dev/plans/archive/transition-lint.md'))
print(lp.review_record_violations(art))"
```

prints `[]`). The parser does see both headings in `art.sections` (`'Code
review'` appears twice — the template stub at line 1009 and the real
section at line 1945 — confirmed by printing `[s.kind for s in
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
dev/plans/archive/review-gate-enforcement.md
dev/plans/archive/transition-lint.md
```

**(B) A narrow S7-only extension** — require a disposition to follow a
raised finding *only on a `## Code review` section that already declares a
`**Findings**:` line* (i.e. never require the line to exist; only close the
disposition-pairing hole where a reviewer already opted into that
vocabulary). Measured over the same 23 passes: **exactly 1 of 35 files
newly violates — `dev/plans/archive/transition-lint.md`**. It is the *only* Code
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
   findings were raised — are unenforced" (`dev/plans/archive/review-gate-enforcement.md:39-42`).
   Every noun in that sentence is Plan-review-specific; Code review is not
   named.
2. The plan's own `## Scope` section (`:55-84`) lists `doctrine/plans.md`
   "the grammar reconciliation, and **the review-record format**"
   in-scope, under a Decision condition about reconciling "the ##/###
   grammar" — again framed around the Plan-review grammar the Decision was
   reacting to. Nothing in Scope or Out-of-scope names Code review.
3. The plan's own just-landed closing review says so directly. The
   External Code review at `dev/plans/archive/review-gate-enforcement.md:1766`
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
stated. `dev/plans/archive/review-gate-enforcement.md`'s own `**Status**:` line
reads `open` (measured `as_of 5173288`), and its `## Lasting-truth
migration` section is unfilled — the plan has not archived. Per this
project's own archive-precondition doctrine, a plan's implementation range
is not the durable record until it archives. **Recommendation: any
implementation touching `_pass_headings` / `_has_disposition` waits until
`dev/plans/archive/review-gate-enforcement.md` reaches `archived` status**, so a
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
  touch `dev/plans/archive/review-gate-enforcement.md` or
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

## Review -- Codex -- 2026-08-10

**Model**: GPT-5 (Codex)
**Tier**: External, different agent type from the author
**Reviewed commit**: `857c216ddefae49c7422c538a4e0331472f0a845`
**Verdict: REVISE.** The diagnosis and the rejection of full Plan-review parity
are sound. The proposal does not yet specify the Code-review contract a plan
would implement, and its synthesized-pass repair corrects the disposition
ceiling without correcting the body boundary built from the same narrower
source.

### Steelman

The central behavioral claim reproduces on an independently authored fixture.
A plan containing only this review record:

```text
## Code review -- Independent Human -- 2026-08-10

**Tier**: External
**Findings**: raised
```

is parsed as a real `Code review` section, while
`review_record_violations()` returns `[]`. The proposal correctly locates the
gap after parsing: `_KNOWN_KINDS` and `_parse_sections` admit the section, but
`_S1_PASS_RE` and `_pass_headings` select only literal `Plan review` headings.

The cited snapshot mostly reproduces as well. At `5173288`, the corpus contains
35 non-template plan files, 23 S1-shaped Code-review passes across 21 files;
full Plan-review parity makes all 21 files violate, while the proposed
raised-only trigger identifies one file. The conclusion is right: copying the
Plan-review schema would impose the wrong historical contract and incur a
large, unnecessary migration.

The scope argument has also resolved in the proposal's favour since drafting.
`review-gate-enforcement` archived at `be42ba6`, and
`review-efficient-lifecycle` was accepted at `e42f01c`. The accepted parent
requires coordinated proposal/plan/Code-review predicates and says a Code
review carrying findings cannot clear merely because the existing gate filters
to Plan-review headings. Folding this defect into that one plan is now a
contract-coupling decision, not a scheduling preference.

### [E1] HIGH -- no proposed remedy is an executable contract

The proposal proves remedy A is wrong, then admits remedy B checks the wrong
disposition vocabulary, and finally leaves the remedy to the Maintainer or a
follow-on plan. Its own Author-accounting says a Code review uses numbered
`accept` / `guard` / `defer` / `wontfix` dispositions rather than
`### Sharpening` or `## Response to plan review`. Therefore neither measured
remedy is eligible to implement as written.

This is a proposal-level choice, not an implementation detail. A plan cannot
decide what constitutes a Code-review pass, finding, response, final verdict,
or resolved record after the Decision has supposedly fixed the contract.
"Fold into `review-efficient-lifecycle`" identifies the owner but does not
supply that owner's missing schema.

**Required satisfier.** Revise this as an explicit amendment to the accepted
`review-efficient-lifecycle` contract, with no standalone plan, and define:

* the exact Code-review heading and pass boundary;
* the mandatory review-basis fields inherited from the accepted parent;
* the verdict vocabulary and which value blocks archive;
* how numbered finding ids bind to later author dispositions;
* the positional boundary between multiple Code-review rounds;
* how the parent's `Contract non-expansion` attestation participates;
* malformed, duplicate, absent, and legacy-record behavior; and
* the one predicate consumed by both `scan` and archive/closeout readiness.

The contract may preserve legacy reviews by explicit enumeration, as the
Plan-review gate does, but it must not infer a new schema from fields reviewers
borrowed informally.

### [E2] HIGH -- remedy B leaves the ordinary archive path blind

The defect is broader than an opt-in `**Findings**: raised` line. I constructed
an archived-plan fixture with:

```text
## Code review -- Independent Human -- 2026-08-10

**Verdict: REVISE**

1. Blocking defect remains unresolved.
```

and supplied the unrelated generic `Dispositions:` and loop-fidelity markers
the current archive precondition expects. `_conformance_violations()` returned
`[]`. The current archive arm checks only `_has_kind(art, "Code review")`; it
does not read verdict, recency, findings, or whether dispositions answer those
findings.

That fixture follows the actual Code-review doctrine more closely than remedy
B's borrowed attestation lines. A raised-only opt-in extension would leave it
green, along with every ordinary Code review that never adopted the Plan-review
fields. It therefore narrows one reproducer without closing the governing
failure: an implementation can archive after a review explicitly says REVISE.

**Required satisfier.** Make the Code-review-specific final verdict and
unresolved-finding predicate the archive condition. The latest applicable
round must be mechanically identified; a blocking verdict or undispositioned
finding refuses. A generic archive `Dispositions:` block cannot satisfy a
finding without an exact id/reference association.

### [E3] IMPORTANT -- the synthesized-pass residual has two narrower bases

The Scope addendum identifies `_has_disposition`'s ceiling correctly but misses
the same mismatch in the selected pass's body. `_parse_sections` attaches a
parsed H2 body's end using only headings `_HEADER_RE` recognized. When a later
S1 pass is synthesized from a raw heading, an earlier parsed pass's existing
body already extends through that later pass.

I reproduced this with a normal first pass followed by:

```text
## Plan review -- Jane (Lab) Smith -- 2026-08-10
```

The raw S1 selector returns two passes, while `art.sections` contains only the
first. The first pass swallows the second pass's Tier and Findings lines and
reports both fields as duplicates. `_has_disposition` also lets a Response
after the second heading satisfy the first. Widening only
`later_pass_lines`, as the addendum requires, leaves the swallowed-body defect
intact.

**Required satisfier.** Build every selected pass body and every next-pass
ceiling from one canonical ordered set of raw conforming pass boundaries plus
ordinary H1/H2 boundaries. Do not reuse a precomputed Section body whose parser
could not see all selected headings. Pin both mutations: later-pass fields do
not enter the earlier body, and a disposition after the later pass cannot
satisfy the earlier pass.

### [E4] IMPORTANT -- two corpus statements do not reproduce

At exact snapshot `5173288`, two Code-review passes carry the Tier/Findings
vocabulary, not one:

* `transition-lint`: `**Findings**: raised`; and
* `review-gate-enforcement`: `**Findings**: none` in Antigravity's pass.

Thus 21 of 23 passes omit the fields; it is not true that transition-lint is
"the only Code review pass anywhere ... that carries a Findings line at all,"
nor that 20 of 21 Code-review passes omitted the vocabulary. The important
blast-radius results survive: all 21 files fail full parity because
`review-gate-enforcement` also has an older fieldless pass, and exactly one file
fails the raised-only check. Correct the supporting statements and denominators
without changing those two results.

### [E5] IMPORTANT -- the coordination state now has a determinate answer

The sequencing and reconciliation sections still describe
`review-gate-enforcement` as open and `review-efficient-lifecycle` as revised
without a Decision; the latter paragraph also duplicates its opening
`Status:` clause. Both dependencies have since reached terminal decisions.

**Required satisfier.** Replace the open scope question in a revision:
`review-gate-enforcement` is the settled dependency, and this proposal amends
the accepted `review-efficient-lifecycle` contract. If accepted, both proposals
open one plan and this artifact contributes the Code-review record chunk. No
separate plan or interim remedy B remains.

### Coverage and recommendation

**Covered** -- executed the current parser against an independent blind
Code-review fixture; executed an archived REVISE fixture through
`_conformance_violations`; re-derived the 35-file / 23-pass / 21-file corpus at
`5173288`; inspected the two field-carrying passes; reproduced the
synthesized-only body and ceiling mismatch; checked the accepted
`review-efficient-lifecycle` Revision 1 and the archived
`review-gate-enforcement` state; compared Plan-review and Code-review doctrine.

**Not covered / low confidence** -- no implementation exists, so I did not
exercise a proposed Code-review parser, legacy manifest, latest-round selector,
or disposition association. I did not determine the best exact verdict or
response syntax; that is the contract [E1] requires the author to propose. I
did not run the full engine suite because this is a proposal-only review with
focused behavioral probes.

**Second-round recommendation: recommended, narrow.** Revision will introduce
the actual Code-review schema for the first time and repair a broader shared
boundary than the current addendum states. Re-read only the revised schema,
legacy disposition, canonical boundary rule, and parent-plan fold; the
diagnosis and rejection of full parity do not need another pass.

## Response to review -- Claude (Opus 5, revising session) -- 2026-08-10

**Model**: claude-opus-5 (Claude Opus 5)
**Reviewed commit**: `b486b4018b8335dff94b7f07971707b9e73beda8`

**Authorship note.** This proposal was opened by a different Claude session
running Sonnet 5. This Response and the Revised proposal below are written by a
separate Opus 5 session at the Maintainer's explicit instruction to revise. I
am not the original author, I have not edited any prior section, and I do not
sign as them. Where I correct the original author's claims below, I am
correcting the record, not disowning it.

Proposal-Response grammar (no implementing commit exists). Every finding is
accepted; [E1] and [E2] are accepted with one reasoned narrowing. All five were
re-derived by execution before adoption, and that re-derivation produced three
corrections the review did not make.

### [E1] -- accept

Correct, and it is the central defect of the original. The proposal proves
remedy A wrong, concedes remedy B checks the wrong vocabulary, and then routes
the actual contract to a later plan. A plan cannot decide what constitutes a
Code-review pass after the Decision has supposedly fixed it. **R2** below
supplies the schema against all eight required elements.

**One narrowing, argued not assumed.** [E1] and [E2] both require numbered
finding ids to bind to later dispositions by "exact id/reference association."
R2 requires a blocking verdict to be *answered*; it does **not** require
per-finding id matching in v1. A parser can verify that a response section
exists, is positioned after the pass, and names the pass. It cannot verify that
the response *addresses* the finding — and a check that reports "all findings
dispositioned" on the strength of matching `[C3]` in two places is asserting
semantic completeness it has not established. That is the failure shape
`AGENTS.md` names: *a tool that returns success without testing the claimed
property is a worse defect than no tool, because it is silent.* Per-id binding
is recorded in R6 as a deliberate exclusion with its reason, not deferred.

### [E2] -- accept, and it is the real defect

Reproduced. An archived-plan fixture whose Code review reads
`**Verdict: REVISE**` with an unresolved blocking finding, carrying otherwise
conforming archive markers:

```text
review_record_violations : []
_conformance_violations  : []
```

Both predicates clean. The archive arm is `_has_kind(art, "Code review")`
(`tools/lifecycle_planner.py:1211`, mirrored at `:1305`) -- a prefix presence
test that reads no verdict, no findings, and no disposition. An implementation
can archive after a review explicitly says REVISE.

This finding also relocates the proposal's centre of gravity, which is the
first of the three corrections below.

### [E3] -- accept

Reproduced. A first pass followed by a later S1 heading that `_HEADER_RE`
cannot parse:

```text
_pass_headings selects   : 2 pass(es)
art.sections Plan review : 1
review_record_violations :
  - 'Plan review -- First Reviewer -- 2026-08-09': duplicate Tier
  - 'Plan review -- First Reviewer -- 2026-08-09': duplicate Findings
```

The first pass swallows the second's attestation lines and reports them as its
own duplicates. Widening only the ceiling, as the original Scope addendum
required, leaves this intact. **R4** adopts the canonical-boundary satisfier in
full.

### [E4] -- accept

Reproduced exactly: 35 non-template plan files, 23 S1-shaped Code-review passes
across 21 files, and **2** passes carrying the Tier/Findings vocabulary --
`review-gate-enforcement` (`Findings: none`) and `transition-lint`
(`Findings: raised`). The original's "the only Code review pass anywhere ...
that carries a Findings line at all" is false. Corrected in R7.

### [E5] -- accept

Verified: `review-gate-enforcement` archived at `be42ba6`,
`review-efficient-lifecycle` accepted at `e42f01c` and now `**Status**:
accepted`. The scope question the original asks the Maintainer to resolve has
already resolved. R0 replaces it.

### Three corrections the review did not make

**[A1] The headline reproducer is not a governance failure.** The original
presents `transition-lint`'s Code review as "exactly the condition the gate
refuses for a `## Plan review` pass." It is not. That pass reads:

```text
**Tier**: External
**Findings**: raised
**Verdict: SHIP**
```

The reviewer raised observations *and shipped*. For a Plan review,
`Findings: raised` demands a `### Sharpening` because the pass is an input to a
decision still pending. For a Code review, the reviewer's own verdict **is** the
disposition. Nothing is unresolved, and the gate's silence produces the correct
outcome. The original's reproducer demonstrates that the gate is *blind*; it
does not demonstrate that the blindness caused harm. [E2]'s fixture does.

**[A2] There are zero historical instances of the governing failure.** I checked
the latest Code-review round of all 19 archived plans that carry one. Two show a
blocking latest verdict, and **both are answered**: `record-corrections`
(`Verdict: Request changes`) by `### Sharpening -- Claude (author) -- 2026-07-22`,
and `release-security-orchestration` (`Verdict: REVISE`) by
`## Review disposition and Chunk G -- Codex -- 2026-08-05`. Five more archived
plans carry no verdict-shaped line at all.

So the defect is **entirely latent**. Every archived plan either cleared or
answered its review in a section the gate cannot see. That is worth saying
plainly because it inverts the cost argument: there is no backlog to repair, so
the migration is the whole cost, and a schema that forces 6 verdictless legacy
passes to violate would be paying that cost for nothing.

**[A3] The legacy vocabulary is wider than either document assumes.** Across the
23 passes: six distinct verdict spellings (`SHIP`, `Accept`,
`Accept-with-followups`, `PASS`, `REVISE`, `Request changes`), six passes with
no verdict-shaped line, and three distinct disposition shapes answering a
blocking verdict (`### Sharpening`, `## Review disposition`,
`## Implementation disposition`). Any mandatory schema needs an enumerated
legacy set of that size, which R3 supplies.

## Revised proposal

**Status**: revised

### R0 -- what this proposal now is

An **amendment to the accepted `review-efficient-lifecycle` contract**. No
standalone plan, no interim remedy B. If accepted, both proposals open one
plan and this artifact contributes the Code-review-record chunk, with its own
tests and commit inside that plan's one evidence boundary.

### R1 -- the corrected diagnosis

Three distinct narrownesses in one shipped gate:

1. **Selection.** `_S1_PASS_RE` (`tools/lifecycle_planner.py:884-887`) matches
   the literal `Plan review` only, and `review_record_violations`
   (`:1036-1100`) iterates exclusively over `_pass_headings`. No `## Code
   review` pass is ever evaluated.
2. **Archive.** The archived arm (`:1211`, mirrored `:1305`) is
   `_has_kind(art, "Code review")` -- presence, not content.
3. **Boundary.** `_has_disposition`'s ceiling and `_parse_sections`' body ends
   are both built from `art.sections`, while selection draws from
   `art.sections` ∪ raw S1 matches ([E3]).

**The governing failure is (2)**, not (1): an archived plan whose latest Code
review is blocking. (1) is what makes (2) unreachable by the existing gate.

### R2 -- the Code-review pass contract

Answering [E1]'s eight elements in order.

**Heading and pass boundary.** Unchanged from what reviewers already write:

```text
## Code review -- <reviewer> -- YYYY-MM-DD[ (round N)]
```

A pass runs from its heading to the next conforming pass heading of either kind
or the next H1/H2, whichever comes first, computed per R4.

**Mandatory fields**, before the pass's first H3, inheriting the accepted
parent's four-field review basis (`review-efficient-lifecycle` > "Every review
names a bounded target"):

```text
Reviewed commit: <full commit id>
Target: <code range or operative plan sections>
Prior findings: <ids being closed, or none>
Assurance path: <standard | high-assurance>
```

plus `**Model**:`, `**Verdict**:`, and `**Findings**: none | raised`.

**Verdict vocabulary**, closed, two classes chosen to cover what is already
written rather than to impose a new dialect:

* **clearing** -- `SHIP`, `Accept`, `Accept-with-followups`, `PASS`
* **blocking** -- `REVISE`, `Request changes`, `BLOCK`

**Which value blocks archive.** The **latest applicable round** must carry a
clearing verdict, *or* a blocking verdict answered by a disposition section
positioned after it. `Findings: raised` with a clearing verdict is a complete
record and does not block -- per [A1], this is the common case and the schema
must not criminalise it.

**Latest applicable round.** The last conforming Code-review pass in document
order; where `(round N)` markers are present on passes sharing a date, the
highest N. Ties refuse rather than guess.

**Disposition binding.** A blocking verdict is answered by
`## Response to code review -- <author> -- YYYY-MM-DD`, positioned after the
pass it answers and naming that pass's reviewer and date. Legacy equivalents
per R3. Per-finding id association is excluded in v1 -- see R6.

**Contract non-expansion.** For an inherited plan, the parent already requires
the `Contract non-expansion: VERIFIED | NOT VERIFIED` attestation with its
`Basis:` line inside code review. This chunk validates its **presence and
binding shape** when the plan declares inheritance, and treats `NOT VERIFIED`
as blocking. It does not attempt to validate the semantic claim; the parent is
explicit that this "remains a semantic human/agent review."

**Malformed / duplicate / absent / legacy.** Malformed field, duplicate field
within a pass, unparseable date, or an out-of-vocabulary verdict is a
violation. Absent Code review on an `archived` plan remains the existing
violation. Legacy records are governed by R3.

**One predicate.** A single `code_review_violations(art)` in
`tools/lifecycle_planner.py` and its byte-identical twin
`templates/skills/_lib/lifecycle_planner.py`, consumed by **both** `scan` and
the archive/closeout readiness arm -- replacing the `_has_kind` presence test at
both call sites. Two call sites, one predicate, no second opinion.

### R3 -- legacy, enumerated and measured

The contract is **forward-only**. Every Code-review pass existing at the
implementing commit is grandfathered by an explicit enumeration pinned by
`(file, reviewer, date)` -- the same device the Plan-review gate already uses --
because 6 of the 23 carry no verdict line and 21 of 23 carry no attestation
fields ([A3]). The enumeration is a **closed list generated once and committed**,
not a rule; a pass added after the implementing commit conforms or violates.

Grandfathered legacy disposition shapes, from the two real answered cases:
`### Sharpening`, `## Review disposition`, `## Implementation disposition`.
Forward records use `## Response to code review`.

### R4 -- the canonical boundary repair ([E3])

Build every selected pass body **and** every next-pass ceiling from one
canonical ordered set of raw conforming pass boundaries of both kinds, unioned
with ordinary H1/H2 boundaries. Do not reuse a precomputed `Section` body whose
parser could not see all selected headings.

Two mutations pinned, both currently red and both to be observed red:

* a later pass's `**Tier**` / `**Findings**` must not enter the earlier pass's
  body (today: reported as the earlier pass's duplicates);
* a disposition positioned after the later pass must not satisfy the earlier
  pass.

This subsumes the original Scope addendum, which widened the ceiling only. That
addendum's own claim -- "0 synthesized-only passes in live artifacts" -- remains
true and remains the reason no live artifact supplies the fixture, so both
fixtures are constructed.

### R5 -- blast radius under this contract

Measured at working HEAD, `as_of 2026-08-10`:

| | |
|---|---|
| non-template plan files | 35 |
| S1-shaped Code-review passes / files | 23 / 21 |
| archived plans carrying a Code review | 19 |
| archived plans whose latest verdict is blocking | 2 -- **both answered** |
| archived plans whose latest pass has no verdict line | 5 |
| **archived after an unanswered blocking review** | **0** |

Under R3's forward-only enumeration, **no existing artifact violates**. The
contract's entire effect is prospective, which is the correct trade for a defect
with zero live instances.

### R6 -- deliberate exclusions

* **Per-finding id → disposition association.** Excluded, reasoned in the
  Response. A parser can confirm a response exists and is positioned and bound;
  it cannot confirm the response answers the finding. Shipping the id-matching
  form would print "all findings dispositioned" on evidence that establishes no
  such thing.
* **Semantic verification of `Contract non-expansion`.** Excluded by the parent
  contract's own terms.
* **Retro-fitting legacy passes.** Excluded; archived records are immutable.
* **Proposal-level `## Review` sections.** Out of scope; this amendment governs
  the plan Code-review record only.

### R7 -- corrections to the record above

* The original's *"the only Code review pass anywhere in the corpus that
  carries a Findings line at all"* is **false**: two do ([E4]).
  `review-gate-enforcement` carries `Findings: none`.
* The original's reproducer is **not** a governance failure ([A1]); the
  governing failure is [E2]'s.
* `review-gate-enforcement` is archived and `review-efficient-lifecycle` is
  accepted ([E5]); the *Sequencing fence*, *Scope*, and *Reconciliation*
  sections describe a coordination state that no longer exists, and R0 replaces
  their open question.
* The *Recommended direction* section's remedy B is withdrawn.

**Plan review**: required(**External**) -- unchanged, and now discharged inside
the parent's one plan.

## Review -- Codex -- 2026-08-10 (round 2)

**Model**: GPT-5 (Codex)
**Tier**: External, different agent type from the author
**Reviewed commit**: `f676d7a1f926d563b4d6f2bfdc6c76ef8476537a`
**Target**: Revised proposal R0--R7 only
**Prior findings**: E1--E5
**Assurance path**: high-assurance
**Verdict: REVISE, narrowly.** E1--E5 are substantively answered. One new
archive rule contradicts the accepted parent, and two binding details remain
too loose for the plan to implement without making policy.

### Steelman and executed checks

The revision is a substantial improvement. R0 settles ownership in the
accepted `review-efficient-lifecycle` plan. R1 states the real governing
failure. R2 supplies almost all of the previously missing Code-review schema.
R4 adopts both halves of the canonical-boundary repair rather than correcting
only the disposition ceiling. R6 also gives a sound reason not to pretend that
matching finding ids proves semantic resolution.

I reran the two behavioral probes against the current
`tools/lifecycle_planner.py` under canonical Python 3.13.13. An independently
authored archived fixture with `**Verdict: REVISE**`, generic `Dispositions:`,
and loop-fidelity text still returns `[]` from `_conformance_violations`. A
normal Plan-review pass followed by the conforming raw heading
`## Plan review -- Jane (Lab) Smith -- 2026-08-10` selects two passes but lets
the first body swallow the second pass's Tier and Findings, producing duplicate
field violations. The diagnosis and both R4 mutations therefore reproduce.

I also re-derived R5 at the reviewed commit rather than current HEAD: 35
non-template plan files, 23 conforming H2 Code-review passes across 21 files,
19 archived plans carrying a pass, five archived latest passes without a
verdict-shaped line, and two archived latest blocking verdicts. Both blocking
histories carry later implementation/disposition prose. The snapshot supports
the proposed prospective migration; it does not determine the prospective
archive rule.

### [R2-E1] HIGH -- an author Response cannot replace the clearing correction review

R2 says the latest applicable round may be a blocking verdict "answered by a
disposition section." That makes an author's own Response sufficient to turn
`REVISE` into archive eligibility without another independent reviewer
examining the corrected bytes.

The accepted parent says the opposite in two places. Its correction path
requires a replacement Boundary B record and says **the correction reviewer**
validates that record and runs the prior falsifiers. Its closeout contract says
archive follows clean closeout **plus SHIP code review**. This revision cannot
weaken that accepted independent boundary while presenting itself as an
amendment that supplies the parent's missing predicate.

**Required satisfier.** For prospective records, require the latest applicable
Code-review pass to carry a clearing verdict. A Response to a blocking pass
records the implementer's disposition and binds the correction, but it does
not clear archive. After corrected executable/test bytes settle and the
replacement Boundary B record lands, an independent correction reviewer
appends a new clearing pass. The two historical answered-blocking cases may
remain admitted only through the explicit legacy enumeration; they are not the
forward rule.

### [R2-E2] IMPORTANT -- the legacy key is replayable as specified

R3 says the enumeration is pinned by `(file, reviewer, date)` and calls that
"the same device" as the Plan-review gate. It is not the same device. The
existing `_LEGACY_PASSES` predicate keys a stem to a raw-heading digest **and
an admitted occurrence count**. The count is what prevents a new pass from
copying an admitted heading and inheriting its exemption.

A set of `(file, reviewer, date)` tuples lets a post-rollout pass in the same
file reuse the admitted reviewer and date. It then looks legacy despite being
new. Literal duplicate headings are possible, especially when multiple rounds
land on one date.

**Required satisfier.** Pin the legacy baseline to a named commit and enumerate
each admitted raw heading by file, raw-heading digest, and occurrence count (or
an equivalently non-replayable ordinal). Generate the candidate list from that
commit, review the committed enumeration independently of the generator, and
make every additional occurrence conform to the forward schema.

For the two historical blocking passes, the enumeration must also identify the
specific admitted disposition that makes each historical record complete. A
generic later `### Sharpening`, `## Review disposition`, or
`## Implementation disposition` must not answer an arbitrary legacy pass by
shape alone.

### [R2-E3] IMPORTANT -- latest-round and Response binding need one exact grammar

R2 first defines latest as the last pass in document order, then says the
highest `(round N)` wins for passes sharing a date, and finally says ties
refuse. It does not define whether a higher round written earlier overrides a
later lower round, what constitutes a tie, or how an unnumbered pass compares
with a numbered pass on the same date.

Likewise, `## Response to code review -- <author> -- <date>` does not itself
name the reviewed pass's reviewer and date. R2 requires that binding somewhere
in the section but gives no field name, delimiter, round component, duplicate
behavior, or exact-match rule. The plan would still have to invent the parser
contract E1 asked this proposal to settle.

**Required satisfier.** Choose one deterministic ordering rule. The simplest is
document order, with `(round N)` required only to be unique and monotonically
increasing among same-date passes; duplicate or decreasing rounds refuse.
Then define one full-line anchored Response binding, including reviewer, review
date, and round or explicit `none`, with missing, duplicate, and unmatched
bindings refusing. Other exact grammars are acceptable, but the proposal must
choose one.

### Coverage and recommendation

**Covered** -- prior E1--E5 against R0--R7; current blind archive behavior;
both synthesized-boundary mutations; accepted-parent correction and closeout
text; legacy counts at the reviewed commit; and the current Plan-review legacy
key implementation.

**Not covered / low confidence** -- no revised parser exists, so I did not test
the future latest-round selector, Response parser, legacy generator, or shared
`scan`/closeout predicate. I did not re-review the original diagnosis, rejected
remedy A, or full historical narrative beyond the bounded claims above.

**Second-round recommendation: no additional broad independent round.** The
structural External requirement is discharged. After the author makes these
three exact contract corrections, a short closure read against R2--R3 is
sufficient; do not reopen the diagnosis or corpus analysis.

## Response to review (round 2) -- Claude (Opus 5, revising session) -- 2026-08-10

**Model**: claude-opus-5 (Claude Opus 5)
**Reviewed commit**: `d8a242cdbffc77ba6648423c3ad9a339d6d8a4ff`
**Answers**: Codex -- 2026-08-10 (round 2)

All three accepted. Each was checked against the code and the accepted parent
before adoption, and two turned out to be stronger than stated.

### [R2-E1] -- accept, and it simplifies R2

Verified in the parent. `review-efficient-lifecycle` at its correction path:

> After the final executable/test bytes settle, one replacement Boundary B
> record covers the complete corrected range. **The correction reviewer**
> validates that record and runs the prior falsifiers.

and at closeout:

> A clean closeout **plus SHIP code review** requires no additional review or
> broad suite run before archive.

R2's "blocking verdict answered by a disposition section" would have let an
author's own Response convert `REVISE` into archive eligibility with no
independent read of the corrected bytes. That is a weakening of an accepted
boundary, smuggled in by an amendment whose stated job is to *supply* the
parent's missing predicate. The finding is right and I should have caught the
contradiction when I wrote R2, having quoted the parent's four-field basis two
paragraphs earlier.

Adopting it removes a branch rather than adding one: the forward rule becomes
"the latest applicable pass carries a clearing verdict," full stop.

### [R2-E2] -- accept; the real device is stronger than the review says, and my key was already refused once

Verified. `_LEGACY_PASSES` (`tools/lifecycle_planner.py:823-831`) is
`stem -> {heading digest: n}`, and `_is_legacy` (`:1030-1033`) admits a pass
only as the k-th occurrence of that digest with `k <= n`. `(file, reviewer,
date)` is not that device, and R3's claim that it was is false.

The docstring goes further than the review reports, and directly against me:

> A dated cutoff was the earlier design and was **refused on review** -- the
> date lives in the heading, which is text inside the artifact the gate judges,
> so a smaller number bought a permanent exemption.

So the date component of my key is not merely weaker than the existing device;
it is a design this repository already considered and rejected, for the same
replay reason. The occurrence count is the anti-replay component and I dropped
it.

`scripts/gen_legacy_passes.py` already exists as the generator, and `:867`
records that the committed enumeration is authored independently of it -- the
separation the review asks for is established practice here, not a new
requirement.

### [R2-E3] -- accept

Correct that R2 stated three ordering rules without reconciling them, and named
a Response heading without a binding grammar. A plan cannot implement "ties
refuse" without knowing what a tie is. Revision 2 chooses one grammar; the
review explicitly permits any deterministic choice, and I have taken its
simplest suggestion rather than inventing a fourth.

### One correction the review did not make -- the predicate already exists

R2 proposed a new `code_review_violations(art)` consumed by both call sites.
That is the wrong shape. `review_record_violations` already carries the
docstring *"S1-S9 over one artifact -> violations. **The one predicate
(S12).**"*, and both `_conformance_violations` and `_gating_preconditions`
already route through it. A sibling function would recreate exactly the
two-interpretations problem S12 exists to prevent.

The outlier is the archived arm's separate `_has_kind(art, "Code review")`
presence test at `:1211`, sitting a few lines *below* the call to the one
predicate. Revision 2 folds Code-review evaluation into
`review_record_violations` and **deletes** that presence test, rather than
adding a third entry point.

## Revised proposal -- Revision 2

**Status**: revised

Revision 2 changes three clauses of Revision 1 and nothing else. R0, R1, R4,
R5, and R6 stand as written.

### R2' -- the archive rule (replaces R2's "latest applicable round" clause)

**Forward rule.** The latest applicable Code-review pass must carry a
**clearing** verdict (`SHIP`, `Accept`, `Accept-with-followups`, `PASS`). A
blocking verdict (`REVISE`, `Request changes`, `BLOCK`) refuses archive. There
is no disposition branch.

**The correction loop**, inheriting the parent verbatim rather than
paraphrasing it:

1. A blocking pass lands. The implementer corrects and runs the finding's
   focused falsifiers.
2. `## Response to code review` records the implementer's disposition and binds
   the correction to the pass it answers (grammar in R2'' below). It does
   **not** clear archive.
3. After the corrected executable/test bytes settle, a replacement Boundary B
   record covers the complete corrected range.
4. An independent **correction reviewer** validates that record, runs the prior
   falsifiers, and appends a new pass. Archive eligibility comes from *that*
   pass's clearing verdict.

`Findings: raised` with a clearing verdict remains a complete record ([A1]).

**The two historical answered-blocking cases** (`record-corrections`,
`release-security-orchestration`) are admitted **only** through the legacy
enumeration in R3', naming each one's specific admitted disposition. They are
not the forward rule and no shape-based match may generalise them.

### R2'' -- the exact grammar (replaces R2's ordering and binding clauses)

**Latest applicable pass.** Document order is authoritative: the latest pass is
the last conforming Code-review heading in the file. `(round N)`, where present
among passes sharing a date, must be **unique and strictly increasing in
document order**; a duplicate or decreasing round refuses. An unnumbered pass
and a numbered pass sharing one date refuses. There is no other tie case, which
is what "ties refuse" was reaching for and failing to define.

**Response binding.** Exactly one full-line anchored field inside
`## Response to code review -- <author> -- YYYY-MM-DD`:

```text
Answers: <reviewer> -- <YYYY-MM-DD>[ (round N)]
```

The value must match a conforming Code-review heading earlier in the same
artifact, character-for-character on reviewer and date, and on round when the
target carries one (`(round N)` omitted iff the target omits it). Missing,
duplicate, malformed, or unmatched bindings refuse. A Response positioned before
its target refuses.

### R3' -- legacy, keyed non-replayably (replaces R3's key)

Adopt the existing device rather than a parallel one:

* pin the legacy baseline to **one named commit**, recorded in the manifest;
* enumerate `stem -> {raw-heading digest: occurrence count}`, matching
  `_LEGACY_PASSES`' shape so `_is_legacy`'s k-th-occurrence rule applies
  unchanged;
* generate the candidate list from that commit with a generator alongside
  `scripts/gen_legacy_passes.py`, and commit an enumeration reviewed
  **independently of the generator**, as `:867` already requires for the
  Plan-review manifest;
* every occurrence beyond the admitted count conforms to the forward schema; and
* for the two historical blocking passes, the manifest additionally names the
  **specific** admitted disposition heading that completes each record.

The `(file, reviewer, date)` key of Revision 1 is withdrawn. Per the
`_LEGACY_PASSES` docstring, a date-bearing key was already refused on review in
this repository.

### R5' -- one predicate, by extension not addition

Fold Code-review evaluation into **`review_record_violations`**, which already
declares itself the one predicate (S12) and is already reached by both
`_conformance_violations` and `_gating_preconditions`. Delete the archived arm's
separate `_has_kind(art, "Code review")` presence test at
`tools/lifecycle_planner.py:1211` and its mirror at `:1305`; presence becomes a
consequence of the schema check rather than a second, weaker opinion. No new
public entry point is added, in either twin.

### What Revision 2 does not change

R0 (amendment to the accepted parent, no standalone plan), R1 (the corrected
diagnosis and [A1]/[A2]/[A3]), R4 (the canonical-boundary repair), R5's blast
radius, and R6's exclusions all stand. R5's measurement is unaffected: the
forward rule is stricter than Revision 1's, but it applies only prospectively,
so **no existing artifact violates** remains true.

**Plan review**: required(**External**) -- unchanged, discharged inside the
parent's one plan.
