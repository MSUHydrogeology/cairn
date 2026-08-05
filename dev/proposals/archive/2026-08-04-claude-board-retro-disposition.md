# Retrospective disposition of the 59 board rows deposited under the old precondition

**Author**: Claude (Strategy)
**Model**: claude-opus-5
**Date opened**: 2026-08-04
**Status**: accepted
**Touches**: `dev/PLANNING.md` > "Deferred follow-ups (durable home)" (the 59 rows); inbound `Follow-ups migrated to:` references in six artifacts, two of them archived
**Related**: split out of `2026-08-04-claude-deferral-discipline` as **D1** by its Decision (`6e349b3`); the [I8] hazard is that proposal's Internal-review finding
**Plan review**: required(Internal) — the adjudication is per-item judgment over records other artifacts point at, which is where a second read is worth most

## Context

`2026-08-04-claude-deferral-discipline` (accepted `6e349b3`, implemented across
chunks A–F) changed the archive precondition so a deferred follow-up carries a
**recorded disposition** — `accept`, `guard`, `wontfix`, or a Maintainer-authorized
`defer` — rather than requiring a durable home for everything.

**New doctrine does not clear rows deposited under the old rule.**
`dev/PLANNING.md` > "Deferred follow-ups (durable home)" holds **59 items** in
**430 lines**, 42.9% of a 1002-line file (`as_of 2026-08-04`, HEAD `4573c11`).
Every one of them was homed there because the old precondition offered no other
route. This proposal adjudicates them.

It was split from the parent deliberately. The parent's Internal review found the
bundling defective on the `identity-not-name` precedent: a per-item adjudication
of unknown batch size, gated on the Maintainer, over records that other artifacts
cite, is a different kind of work from a prose amendment. The parent's Response
conceded the point — *sequencing* the retro pass as a named successor **is** the
`defer` (successor) disposition, so applying the ladder to itself is the opposite
of self-refuting.

**The condition attached to that split is discharged by this file existing.** The
Decision required the successor to open in the same session, with its stem named
in a commit body, so its absence would be visible in `git log` rather than only in
a reader's memory.

## Proposal

Adjudicate each of the 59 rows against the accepted vocabulary, in **batches by
source artifact** rather than one pass over the whole section, so each batch is
reviewable and the Maintainer sees one `defer` list per batch rather than 59
decisions.

Expected shape — **an estimate, explicitly not a measurement.** The parent's
"12 of the 59" figure was withdrawn as unreproducible: its Internal reviewer got
4, 5, 6 and 17 under four different patterns, and established that only **18** of
the 59 carry an explicit `*Trigger:*` field at all. This proposal therefore
commits to **no** routing split in advance. The per-item adjudication produces the
first real figure, and that figure is the deliverable.

### The [I8] hazard — inbound references from closed artifacts

Six artifacts cite this section as the home against which their archive
precondition was discharged, **two of them already archived and therefore
append-only**:

* `dev/plans/archive/lockfile-provenance-fields.md`
* `dev/plans/archive/interpreter-trust-root-fallback.md`

The second is already a live instance: it records S2 as homed at a
`dev/PLANNING.md` **Queued** row, and S2 now sits inside `### Deferred
follow-ups`. **The pointer has already drifted once.** Re-routing it again —
especially to `wontfix` — would leave an archived, append-only record asserting a
migration that is no longer true and cannot be corrected in place.

Two rules govern this, both carried verbatim from the parent's accepted C4:

1. A row **named by a closed artifact's disposition block** is **ineligible for
   `wontfix` without the Maintainer**.
2. Any re-route of such a row is recorded as a **forwarding entry** in this
   pass's own commit body, so the closed artifact's claim remains
   reconstructible from the durable record even though its text cannot change.

### Sequencing note

This pass **may not begin** until the parent plan's Chunk D has landed, because
Chunk D rewrites the archive-precondition prose at `dev/PLANNING.md:433` and this
pass rewrites rows below it in the same file. Landing them in either order is
fine; landing them concurrently is a conflict.

### Documentation / doctrine surface

**None.** This proposal changes no rule — it applies an already-accepted one to
existing rows. The only file it edits is `dev/PLANNING.md`'s deferred section.
Stated explicitly because a silent omission here would itself be a review finding.

### Doctrine-change rate-limit

**N/A** — this proposal introduces no doctrine change. It executes
`2026-08-04-claude-deferral-discipline`, whose own gate clearance is recorded in
that artifact and does not re-apply.

## Rationale

**Which workflow?** Cold pickup. `dev/NEXT_SESSION.md` competes with a 1002-line
board on which a release blocker and a two-assertion test guard carry equal
visual weight.

**Why now?** The parent lands the rule this session. A rule that governs only
future artifacts, while 59 rows sit under the superseded one, is the weaker half
of the change — and the gap is exactly where a reader concludes the rule is
decorative.

**Why not just leave them?** Because the parent's governing principle is stated
over *outstanding follow-ups*, and 59 unadjudicated rows are outstanding
follow-ups. Leaving them would make the principle true only by not looking.

## Alternatives considered

* **Do nothing; let the rows age out.** The board has no expiry — the staleness
  sweep can only reaffirm. "Aging out" is not a mechanism that exists.
* **Bulk-decline everything below a consequence threshold.** Fast, and wrong: it
  is precisely the rubber-stamped-decline failure the parent's *Signals* section
  names as its own worst outcome ("visible debt traded for invisible debt, the
  strictly worse trade").
* **Adjudicate in one pass rather than batches.** Rejected — one 59-item
  Maintainer batch is the load-bottleneck failure mode the parent's item 3
  batching rule exists to prevent, reproduced at the worst possible size.
* **Keep it inside the parent proposal** (what the parent originally proposed).
  Rejected by the parent's own Decision on the `identity-not-name` bundling
  precedent.

## Evidence / verification plan

* **Tests** — **N/A**: this pass edits one Markdown file and writes no code.
* **Examples / smoke checks** — `python scripts/check_cairn.py` after each batch;
  the board carries many path citations and re-routing is exactly where they
  break. `python scripts/claim_check.py dev/PLANNING.md` likewise.
* **Docs** — the board section is the deliverable; no other doc changes.

### Author-accounting

* **Invariants.** (1) *No row disappears without a recorded disposition* —
  enforcer: this pass's own `Dispositions:` commit bodies, reviewed. (2) *No
  closed artifact's claim is falsified* — enforcer: the forwarding-entry rule,
  reviewed. Both **documentary**; consistent with the parent, which established
  that a presence-checker would certify the degenerate case.
* **Failure modes.** Over-eager decline — **fails open**, and is the principal
  risk, same as the parent's. Under-eager decline — fails safe: the board stays
  long, which is the status quo.
* **Edge cases.** A row whose source artifact is *in flight* (not archived) →
  route to that artifact's own archive-preparation instead of adjudicating it
  here, so its author disposes of it. A row citing another row → adjudicate the
  cited one first.
* **Known omissions.** No routing estimate is offered, deliberately (above). The
  batch count is not fixed in advance; it follows the source-artifact grouping the
  section already has.

## Signals the change is wrong

* **Declines cluster in one batch.** If one artifact's rows route overwhelmingly
  to `wontfix` while others do not, the adjudicator is tiring rather than judging.
  **Recovery:** re-adjudicate that batch fresh-session.
* **A closed artifact's claim is found falsified after the fact.** The forwarding
  rule failed. **Recovery:** an appended correction note in this pass's record —
  the archived artifact still cannot be edited.
* **The board does not measurably shrink.** Then the 59 were mostly real work and
  the parent's diagnosis over-attributed to the ratchet. **Recovery:** say so on
  the record, and stop — a board of 59 genuine obligations is a resourcing
  problem, not a doctrine problem.

---

## Internal Review -- Claude (fresh session) -- 2026-08-04

**Model**: claude-opus-5
**Tier**: Internal (same agent type, fresh session — the floor, not more)
**Verified against**: HEAD `46668c0`. The tree fast-forwarded from `cff8559`
to `46668c0` *during* this review (20 commits, 14 of them proposal-archive
moves by a concurrent session). `dev/PLANNING.md` is unchanged across that
range — 1037 lines, the section at `:535`–`:964` — so every board figure below
holds at both endpoints. Two findings depend on the churn and say so.

### Steelman

The strongest case for this proposal is the one it does not quite make.

`dev/PLANNING.md` > `### Deferred follow-ups (durable home)` is genuinely the
worst surface in the tree for a cold reader. It is 430 lines — I re-derived
this, `:535`–`:964` inclusive — 41.5% of a 1037-line board, on which a
reproduced install-integrity tamper bypass (`:583`) and a two-assertion
`_yaml_load`-as-oracle nit (`:869`) carry identical visual weight. The
*Rationale*'s "cold pickup" framing is right, and it is right for a reason the
proposal states well: a rule that governs only future artifacts while 59 rows
sit under the superseded one is where a reader concludes the rule is
decorative.

And the pass will find real things. In one afternoon of reading I found a true
**duplicate** (`:845` and `:910` are the same `_infer_init_lock_axes` defect in
the same file, arriving from two different orphaned lineages), a row that
**already carries a verbatim Maintainer disposition** and is therefore already
adjudicated (`:687`, *"SC4 - fold in"*), and **two stale line citations inside
the board** that the parent's own Chunk B created a commit earlier. None of
those needs a Maintainer. That is a real deliverable and the board is genuinely
better after it.

The split from the parent was also correct, and the `identity-not-name`
reasoning for it holds. The refusal to re-guess a routing split after the
parent's "12 of the 59" was withdrawn is the right instinct. The *Signals*
section is unusually honest — it names the outcome that would falsify its own
premise and commits to saying so on the record.

So: not make-work in intent. But the pass as **specified** will not produce
what the proposal implies, for a structural reason it has not noticed ([I3]),
and the hazard section it inherited is wrong in both of its concrete claims
([I1], [I2]).

---

### [I1] The [I8] inbound-reference enumeration is wrong in both directions -- one named artifact does not cite this section at all, and at least six *immutable commit bodies* that do were missed

The proposal carries the parent's [I8] population verbatim: *"Six artifacts
cite this section ... two of them already archived and therefore append-only"*,
naming `dev/plans/archive/lockfile-provenance-fields.md` and
`dev/plans/archive/interpreter-trust-root-fallback.md`. I re-derived the set.
Both halves are wrong.

**Wrong inclusion.** `dev/plans/archive/lockfile-provenance-fields.md:407`
records P4 as homed *"at its `dev/PLANNING.md` 'Lockfile schema validate-on-
read' **Queued** row"*. That row is at **`dev/PLANNING.md:185`**, inside
`## Queued` (`:120`–`:268`) — **not** in `### Deferred follow-ups` (`:535`).
The archived plan's pointer is accurate; the artifact is not an inbound
reference to this section, and re-routing these 59 rows cannot falsify it. One
of the proposal's two archived exemplars is not in the population.

**Missed inclusions, and they are the worse kind.** The doctrine explicitly
permits the disposition record to live in *"the archive commit body"*
(`doctrine/lifecycle.md:403` ff., > "Recording it"), and that is where the
2026-08-04 wave actually put it. Six commit bodies name this section as their
discharged home:

| Commit | Body names |
|---|---|
| `a9bc372` | *"the four uncovered External mandates -> dev/PLANNING.md > Archive-time follow-ups"* |
| `89a8f1f` | *"SC5 ... -> dev/PLANNING.md > Archive-time"* |
| `e59f9d4` | *"the Decision's flagged condition, and channel 3 -> dev/PLANNING.md >"* |
| `8595274` | *"_infer_init_lock_axes residual -> dev/PLANNING.md > Archive-time follow-ups"* |
| `640864e` | *"dev/PLANNING.md > Archive-time follow-ups -- the 2026-08-04 six-plan census"* |
| `2b37719` | same section (proposal-side archive) |

A commit body is **strictly less correctable than an archived file**. An
archived artifact can at least receive an appended correction note — which is
exactly the recovery this proposal's own *Signals* section proposes. A commit
body admits no appended anything. The proposal's forwarding rule was designed
for the weaker hazard and is applied to a population that does not contain the
stronger one.

**And the population is churning under the proposal.** At `791655a` (this
file's opening commit) `dev/proposals/2026-08-03-claude-dependency-advisory-
coverage.md` and `dev/proposals/2026-08-03-claude-release-security-bar.md` were
live `accepted` proposals carrying literal `Follow-ups migrated to:` blocks
pointing at this section. Both archived during this review (`f0ba8e8`,
`604c4a8`) and now sit at
`dev/proposals/archive/2026-08-03-claude-dependency-advisory-coverage.md:930`
and `:1084`, and
`dev/proposals/archive/2026-08-03-claude-release-security-bar.md:1028` and
`:1085` — append-only, and invisible to the parent's [I8] count because they
were not archived when it was written.

Re-derived total at HEAD: **eight file-level citing artifacts** (four archived:
`interpreter-trust-root-fallback`, the two just-archived proposals, and — by
pre-declared archive text rather than a `Follow-ups migrated to:` block — the
five archived census-source plans `byline-classification`, `scan-coverage`,
`release-authenticity`, `profile-parse-fail-open`, `gate-claims-vs-
enforcement`; four live: `dev/plans/dependency-advisory-coverage.md:274`,
`dev/plans/release-security-bar.md:113`, `dev/plans/security-preflight-
checklist.md:663`, `dev/plans/default-security-stance.md:866`) **plus six
immutable commit bodies**. Not "six, two archived."

This is the finding that matters most, because C4's second eligibility rule —
the proposal's principal safety rail — is keyed on *"named by a closed
artifact's disposition block."* If the closed-artifact set is understated ~5×,
the rule fires on the wrong rows and the pass declines things it may not
decline.

**Satisfier** — re-derive the inbound set mechanically before the pass starts,
over three surfaces not one: (a) `grep -rn "Deferred follow-ups\|Archive-time
follow-ups" dev/`; (b) `git log --all --format='%H %b'` filtered for the same
strings, since commit bodies are half the population; (c) the archived plans
whose residuals *are* the census rows, which name `dev/PLANNING.md` without
naming the subsection. Record the count with its `as_of` and its command, and
drop `lockfile-provenance-fields` from the list.

---

### [I2] "The pointer has already drifted once" is false -- the S2 row has never moved, and the proposal's only live instance of the hazard is not an instance of it

The proposal's motivating evidence: *"It records S2 as homed at a
`dev/PLANNING.md` **Queued** row, and S2 now sits inside `### Deferred
follow-ups`. **The pointer has already drifted once.**"*

I checked the tree at the plan-open commit that created the row. At `3982918`,
`### Deferred follow-ups (durable home)` began at line 284 and the S2 row was
at line **304**, under **Lifecycle apparatus** — inside this section from the
day it was written. At HEAD it is at `dev/PLANNING.md:555`, in the same section
under the same heading. **The row has never moved sections.** There is no
drift.

What actually happened is different and internally visible: the same archived
file contradicts itself. `dev/plans/archive/interpreter-trust-root-
fallback.md:582` says "Queued row"; `:913` of the *same file* says the row is
at *"`:304-316` ... under 'Lifecycle apparatus'"* — correct on the day, and
correct about the section today. The `:582` phrasing was **wrong when written**,
not drifted.

Why this matters rather than being pedantry:

1. It is the proposal's **only** claimed live instance of the [I8] hazard. With
   it withdrawn, the forwarding rule is prophylactic — which is a fine thing
   for a rule to be, but it should be argued as one.
2. The mechanism it attributes is the wrong one, and the two call for different
   controls. Drift is cured by a forwarding entry at re-route time. A pointer
   *wrong at authorship* is cured by checking the pointer when it is written —
   a different control, at a different moment, on a different actor.
3. It has already propagated into an immutable record: commit `791655a`'s body
   states *"one (interpreter-trust-root-fallback, S2) has ALREADY drifted
   once."* That body cannot be corrected. This review is now the only
   reachable correction, which is a small live demonstration of the hazard the
   proposal is about.

**Satisfier** — withdraw the drift claim in an appended correction (it is a
figure retraction, same class as the parent's "12 of the 59"), and either name
a genuine drift instance or restate the [I8] section as prophylactic. If a
genuine instance is wanted, `dev/PLANNING.md:927` is one — see [I8] below.

---

### [I3] The declared scope structurally forecloses `accept` and `guard`, collapsing the output vocabulary to {`wontfix`, `defer`} -- and C4 removes `wontfix` for most rows

This is the finding that changes what the pass produces.

The proposal fixes its scope twice, unambiguously: *"The only file it edits is
`dev/PLANNING.md`'s deferred section"* (*Documentation / doctrine surface*),
and *"**Tests** — **N/A**: this pass edits one Markdown file and writes no
code"* (*Evidence / verification plan*).

Now read the landed vocabulary at `doctrine/lifecycle.md:403` ff. against that
scope:

* **`accept`** — *"fixed in this artifact's scope"*, including writing the doc
  the finding asked for. Fixing a board row means editing the thing the row is
  about — `bootstrap/`, `doctrine/`, `templates/`. **Out of scope by
  construction.**
* **`guard`** — *"homed in an artifact that **executes** ... The entry **must
  name the node** (`path::node`)."* Naming a node that does not exist is a
  broken guard, so `guard` requires *writing the assertion*, in
  `bootstrap/tests/`. **Out of scope by construction**, and explicitly
  foreclosed by "writes no code."
* **`wontfix`** — available, but C4's consequence floor removes it for any row
  that reaches an adopter, blocks a release, or needs a Decision.
* **`defer`** — available, and leaves the row exactly where it is.

So for every row that is not `wontfix`-eligible, the *only* reachable
disposition is `defer` — which changes nothing about the row except that it now
also carries a rationale and a quoted Maintainer authorization. The board gets
**longer**. That is not a risk the *Signals* section hedges against; it is what
the specified mechanism predicts.

The board itself makes this concrete. `dev/PLANNING.md` SC3's own recorded
remedy is *"the guard is one assertion and should be written rather than
re-deferred"*; SC5's is *"the guard is two assertions"*. Those are the two
clearest `guard` candidates in the whole section — precisely what C2's new
token was invented for — and this pass, as scoped, may not write either. It can
only re-defer them, which is the outcome the board text already calls wrong.

I sampled the eligibility question rather than asserting it. A keyword pass
over all 59 rows (adopter/templates/install/scaffold/lockfile/manifest;
Maintainer/Decide/Decision/own proposal; release/launch/v0.4/v0.5/tag) leaves
21 rows matching none of the three — but hand-reading those 21 moves several
back across the bar (e.g. `:774` "asked a reviewer to decide ... Neither
reviewer decided" is plainly *needs a Decision*; `:570` facade-loader symlink
hardening is engine code that ships). I will not assert a number — that is the
error this lineage already made twice — but the direction is not in doubt: the
`wontfix`-eligible set is a minority, and the pass's reachable output is
dominated by `defer`.

**Satisfier** — one of two, and the choice is the proposal's central design
decision, not a detail:

* **(a) Widen the scope** so the pass may land `guard` assertions and `accept`
  fixes in the same lineage. Then `Touches` must name `bootstrap/tests/` and
  the affected source surfaces, *"Tests — N/A"* becomes false and must be
  replaced with a real verification plan, and the batching rule needs a
  per-batch test-run gate. This makes the pass much bigger and probably
  re-triggers the `identity-not-name` bundling objection — which is worth
  saying out loud.
* **(b) Keep the narrow scope and state the consequence**: the output
  vocabulary is {`wontfix`, `defer`}, the expected board delta is **≥ 0 lines**,
  and the deliverable is *recorded rationale plus a routed backlog*, not a
  shorter board. Then re-argue value on that basis — [I9]'s hygiene deliverable
  is the honest version of it.

Either closes it. Silence does not, because a Maintainer reading this proposal
today would reasonably expect a shorter board.

---

### [I4] No landed rule obliges this pass, and the proposal presents it as an inherited obligation

*Context* says: *"**New doctrine does not clear rows deposited under the old
rule.**"* True. But the sentence one level up is the one that matters, and it
is not stated: **the new doctrine does not *reach* those rows either.**

The landed precondition (`doctrine/lifecycle.md:403`) is scoped to artifacts at
their archive moment — *"before a proposal **or** a plan archives, every
explicitly-deferred follow-up **it carries** must carry a recorded
disposition."* A board row is the *destination* of that rule, not a source
artifact that archives. Nothing in C1–C7 creates an obligation over
`dev/PLANNING.md`'s existing rows.

*Rationale* answers "Why not just leave them?" with the parent's governing
principle — *"An artifact closes more than it opens"*, stated over outstanding
follow-ups. But the parent's Revised proposal records that principle as
**"not measurable today"** and declines to build any checker for it, on the
reviewer's argument that a presence-checker would certify the degenerate case.
So the stated warrant for a 59-item Maintainer-gated pass is a principle its
own parent declared unmeasurable and deliberately left unenforced.

The Decision's carry of D1 does not close this. It authorized *opening the
successor* — *"the successor opens this session, stem named in a commit body"*
— which `791655a` discharged. Authorization to open an artifact is not
authorization to perform its content; that is what this proposal's own Decision
is for. The proposal is therefore **elective**, and it reads as mandatory.

This is not an argument against doing it. It is an argument that the case has
to be made on the pass's actual merits — cold-pickup cost, the duplicate, the
already-dispositioned row, the stale citations — rather than on an obligation
that does not exist. Those merits are good; the proposal under-uses them.

**Related, and minor:** the *Sequencing note* says the pass *"**may not begin**
until the parent plan's Chunk D has landed."* Chunk D is `4858c84`, which
`git merge-base --is-ancestor 4858c84 791655a` confirms is an **ancestor of
this proposal's own opening commit** — it landed five commits before the file
existed. The precondition was satisfied at write time and is stated as
outstanding. A cold reader inherits a blocker that never applied.

**Satisfier** — replace the obligation framing with the elective one, state
that no landed rule reaches these rows, and re-argue on the hygiene + cold-
pickup merits. Convert the *Sequencing note* to past tense naming `4858c84`, or
strike it as discharged.

---

### [I5] The forwarding rule writes forward-links only into the pass's own commit body, which no reader of the stale pointer will ever find

The proposal's second [I8] rule: *"Any re-route of such a row is recorded as a
**forwarding entry** in this pass's own commit body, so the closed artifact's
claim remains reconstructible from the durable record."*

Trace the reader. Someone lands on `640864e`'s body, reads *"-> dev/PLANNING.md
> Archive-time follow-ups -- the 2026-08-04 six-plan census"*, opens
`dev/PLANNING.md`, and finds the subsection gone or the row `wontfix`-ed away.
What do they do next? Under this rule: grep every commit body committed after
`640864e` for a forwarding entry they have no reason to believe exists, in a
format they have not seen. There is no back-link, no tombstone, and no
discoverable index. "Reconstructible in principle by exhaustive search" is not
the same property as "auditable", and the proposal claims the latter.

This is sharper given [I1]: six of the citing records *are* commit bodies, so
the forwarding entry and the thing it forwards from live in the same
undiscoverable medium. A forwarding entry in a commit body, pointing away from
another commit body, is a link with no anchor at either end.

**Satisfier** — put the forwarding record where the reader actually arrives:
retain a one-line tombstone **in the board section** for every re-routed row
that a closed artifact names (`<row> -> <disposition>, forwarded <date>,
formerly cited by <artifact>`), *in addition to* the commit-body entry. That
costs a line per forwarded row, is discoverable by the reader who follows the
stale pointer, and is checkable by `grep`. If tombstones are judged to defeat
the purpose (the board stays long — see [I3]), say so and record that
auditability was traded for length, deliberately.

---

### [I6] "Batches by source artifact" assumes a structure 21 of the 59 rows do not have

*Proposal*: *"in **batches by source artifact** rather than one pass over the
whole section"*, and *Known omissions*: *"the batch count is not fixed in
advance; it follows the source-artifact grouping the section already has."*

I counted the section's grouping. Sixteen groups, 59 rows:

| Grouping kind | Groups | Rows |
|---|---|---|
| **By source artifact** — `Scan coverage` (4), `Release authenticity` (6), and the six `*From <plan> (N):*` census groups (28) | 8 | **38** |
| **By topic** — `Lifecycle apparatus` (5), `Scaffold / engine` (5), `Security apparatus` (2), `Stack-neutrality` (1), `Coordination` (2), `Doctrine` (2), `Adoption UX` (1), `Lower-priority` (3) | 8 | **21** |

For the 21, the grouping the proposal relies on does not exist, and the
section's own preamble (`:539`) says why: those rows were *"Imported from the
modflow_tools-side batch ledgers"* — **a different repository**. Several carry
that tree's ledger codes (`C-#3`, `B-#1/2`, `E-#1`, `Move 5`) whose source
artifacts are not in this repo at all and cannot be opened to adjudicate
against. A handful name a Cairn source inline and can be attributed by reading
(`:583` cites `release-security-bar` E1; `:555` cites `interpreter-trust-root-
fallback`) — but that is per-row archaeology, not a grouping the section has.

So the batching design covers 64% of the board and is undefined for the rest —
which is also the *hardest* 36%, since a row whose source artifact is in
another repository has no author to route it back to and no fence to check it
against.

**Satisfier** — state the batch plan concretely: eight source-artifact batches
covering 38 rows, plus a named disposition for the 21 imported rows (one
"orphaned imports" batch, or an explicit out-of-scope fence recording that
their source artifacts are unreachable). Naming the count also fixes [I7]'s
sizing problem for free.

---

### [I7] Refusing a routing *estimate* is right; refusing to *characterize the population* is an over-correction that leaves the Decision under-informed

I want to defend the proposal here before disagreeing with it. Declining to
replace a retracted, unreproducible figure with a fresh guess is correct, and
the parent's "12 of the 59" deserved its withdrawal. *"This proposal therefore
commits to **no** routing split in advance"* is the right call **for a split**.

But the proposal generalizes from "no estimate" to "no characterization", and
those are different epistemic objects. An estimate is a prediction about a
judgment not yet made. A *measurement* of the population is a fact about the
tree today. The second is cheap, reproducible, and exactly what the Maintainer
needs to size a batch they are being asked to authorize. Everything below took
one pass and is re-runnable:

* **59 rows** in **430 lines**, `:535`–`:964`, **41.5%** of a 1037-line file
  (`as_of 2026-08-04`, HEAD `46668c0`).
* **38 rows in 8 source-artifact batches; 21 in 8 topical groups** ([I6]).
* **18** rows carry an explicit `*Trigger:*` field; **2** more carry an
  un-italicized `Trigger:`; of the remaining 39, **7** carry a *"Revive"* /
  *"Revival condition"* clause instead. So **27 of 59 carry a revival condition
  in some form** — a materially different picture from the bare "18" the
  proposal reproduces, and the one that bears on how many rows are actually
  adjudicable.
* **≥1 exact duplicate** and **≥1 row already carrying a verbatim Maintainer
  disposition** ([I9]).

None of that is a routing split. All of it bounds the work. Without it the
Maintainer is asked to authorize an open-ended per-item pass with no batch
count, no size, and no sense of how much of it is already settled — which makes
the Decision harder to give, not easier, and invites either a reflexive yes or
an indefinite hold.

I also note the proposal reproduces the parent's "18" without re-deriving it. I
did re-derive it and it is **exactly right** — credit where due — but the fuller
27-of-59 picture is one `grep` away and changes the read.

**Satisfier** — add a short *Population* subsection carrying the five
measurements above, each with its `as_of` and the command that produced it,
explicitly labelled *"measurements of the board, not predictions of the
routing"*. Keep the no-estimate commitment verbatim; it is correct and it
survives this addition intact.

---

### [I8] The verification plan's named checks do not check the class of breakage this pass creates -- both are demonstrably blind, and there is a live falsifying instance already in the board

*Evidence / verification plan*: *"`python scripts/check_cairn.py` after each
batch; the board carries many path citations and re-routing is exactly where
they break. `python scripts/claim_check.py dev/PLANNING.md` likewise."*

I ran both. Neither catches the failure mode.

**`check_cairn.py` excludes archives by default.** Run bare, it reports
`OK -- 176 Markdown file(s) scanned`. Run `--include-archives`, it reports
`92 issue(s) across 253 file(s)`. The 77-file delta is `dev/plans/archive/` and
`dev/proposals/archive/` — **exactly the append-only population [I8] exists to
protect.** The check named as the guard against inbound-reference breakage does
not read the artifacts whose references are at risk. (Three of those 92 are in
`dev/proposals/archive/2026-08-04-claude-deferral-discipline.md` itself.)

**`claim_check.py` cannot see a wrong-but-in-bounds line citation** — and there
is one in the board right now. `dev/PLANNING.md:926-928` reads:

> **Gate-claims B2 — the archive-commit-body auditability claim is falsified**
> (`doctrine/proposals.md:370` and `doctrine/plans.md:611`: *"This makes the
> migration auditable from `git log` alone"*)

At HEAD, `doctrine/proposals.md:370` is `* <item> -> guard
(tests/test_thing.py::test_the_case)` and `doctrine/plans.md:611` is
`Dispositions:`. The quoted sentence now lives at `doctrine/proposals.md:379`
and `doctrine/plans.md:622`. The row's citations were correct at `4573c11` and
were shifted by **the parent's own Chunk B (`5c85274`)**, one commit before this
proposal opened. `python scripts/claim_check.py dev/PLANNING.md` returns
**`OK, no claim-check flags`**: both paths resolve and both lines are in bounds,
so the checker is structurally incapable of noticing that they now point at
unrelated text.

This is the repo's named recurring failure mode, hit exactly — a protection
asserted at the strength intended rather than delivered. It also supplies the
genuine drift instance [I2] withdrew: an *outbound* citation from a board row,
broken by the parent's own implementation, invisible to both named checks. The
proposal's hazard analysis looks only at inbound references; the direction that
actually broke this session was outbound.

**Satisfier** — three parts, all cheap. (1) Name `python scripts/check_cairn.py
--include-archives` in the verification plan, not the bare form, and record the
92-issue baseline so a batch's delta is readable. (2) State that `claim_check`
does not validate citation *targets*, only bounds, and add a per-batch manual
re-read of every `path:line` citation in the rows touched. (3) Fix
`dev/PLANNING.md:927` as part of batch one — it is a two-character change and a
free demonstration that the pass does what it claims.

---

### [I9] The board contains duplicate and already-adjudicated rows, and the vocabulary has no token for either -- invariant (1) makes a merge unrecordable

Two rows, one obligation:

* `dev/PLANNING.md:845` — *"**`_infer_init_lock_axes` guesses `human_team` from
  a filename** *(orphaned residual: routed by `fork-advisory-semantics` to
  scope 4 ...)* — `bootstrap/_scaffold/upgrade.py` infers `small-multi` from the
  mere presence of a root `CONTRIBUTING.md`"*
* `dev/PLANNING.md:910` — *"**`_infer_init_lock_axes` infers `human_team` from a
  file's mere presence** *(orphaned residual — was `contributor-entry` R1 ...)*
  — a root `CONTRIBUTING.md` existing is treated as evidence of a human team."*

Same function, same file, same defect, arriving from two orphaned lineages that
each disclaimed it. This is the single best argument *for* the pass — and the
proposal's machinery cannot record its resolution. The vocabulary is
{`accept`, `guard`, `wontfix`, `defer`} and none of them means *"merged into
row X."* `accept` is false (nothing was fixed); `wontfix` is false and
misleading (the obligation survives); `defer` on both preserves the duplicate.
And the proposal's invariant (1) — *"No row disappears without a recorded
disposition"* — makes the merged row's disappearance a violation unless a token
is forced onto it.

Separately, `dev/PLANNING.md:687` already carries a **verbatim Maintainer
disposition**: *"**Maintainer disposition 2026-08-04: fold in** — quoted
verbatim, *'SC4 - fold in'*"*, with a named ceremony. Re-adjudicating it is
re-litigating a settled question, and doing so in a batch is how a settled
question quietly becomes unsettled. The *Edge cases* list covers "a row whose
source artifact is in flight" and "a row citing another row" but not "a row
already dispositioned."

**Satisfier** — add two edge cases and one recording form: (a) **duplicate** —
merge is recorded as `accept` on the surviving row with an explicit `merged
from: <row>` note, and invariant (1) is restated to permit it; (b)
**already-dispositioned** — a row carrying a quoted Maintainer disposition is
**out of scope** for the pass and passes through untouched, recorded as such in
the batch's block.

---

### [I10] The headline share is dated to a HEAD the proposal's own lineage superseded five commits before the file was written

*"**59 items** in **430 lines**, 42.9% of a 1002-line file (`as_of
2026-08-04`, HEAD `4573c11`)."*

Every component reproduces **at `4573c11`**: 1002 lines, section `:500`–`:929`
= 430, 59 top-level bullets, 430/1002 = 42.91%. The arithmetic is clean and the
`as_of` discipline is followed in form.

But `dev/PLANNING.md` was **1037 lines at `791655a`**, this proposal's own
opening commit — grown by the parent's Chunk D (`4858c84`), which added 53
lines to the archive-precondition prose. The true share at the moment of
writing was **41.5%**. The snapshot is dated to a tree state the author's own
lineage had already replaced.

Low severity — 1.4 points, decision-irrelevant, and honestly `as_of`-tagged. I
raise it only because this artifact family has now shipped a 3.4× headline
error, a mis-sorted line count, and (in [I2]) a false drift claim, so the
cheapest possible correction is worth taking: re-measure at your own HEAD, not
an ancestor's.

There is also a second-order point worth one line: Chunk D made the board
**longer**, and under [I3] this pass most likely makes it longer again. The
percentage is drifting the wrong way for reasons this lineage is causing.

**Satisfier** — restate as `430 lines, 59 items, 41.5% of a 1037-line file
(as_of 2026-08-04, HEAD 46668c0)`, or drop the percentage and keep the
absolute figures, which are stable and carry the argument on their own.

---

### Covered

Sweep per `doctrine/dual-review.md` > "Review expectations". Falsifiable
citations; commands re-runnable at HEAD `46668c0`.

1. **Claims** — every numeric claim re-derived. **59 items**: 59 top-level `* `
   bullets in `dev/PLANNING.md:535`–`:964` ✔. **430 lines**: `:535`–`:964`
   inclusive ✔ (and `:500`–`:929` at `4573c11` ✔). **1002 lines / 42.9%**:
   reproduces at `4573c11`, stale at the proposal's own commit — [I10].
   **"18 of the 59 carry an explicit `*Trigger:*` field"**: exactly 18 ✔
   (plus 2 un-italicized, plus 7 `Revive`/`Revival condition` — [I7]).
   **"six artifacts cite this section"**: ✘ — [I1]. **"two of them archived"**:
   ✘ — [I1]. **"already drifted once"**: ✘, falsified at `3982918` — [I2].
   **Chunk D sequencing**: `git merge-base --is-ancestor 4858c84 791655a`
   succeeds — [I4]. **Decision `6e349b3` / stem named in `791655a` body**: both
   confirmed by reading the commit bodies ✔.
2. **Production path exercised by tests** — at proposal maturity the bar is
   *promised and scoped*. Both named checks are promised, and both are
   demonstrably blind to the failure class: `check_cairn.py` bare = `OK, 176
   files`, `--include-archives` = `92 issues across 253 files`;
   `claim_check.py dev/PLANNING.md` = `OK` despite the live stale citation at
   `:927`. [I8].
3. **Design completeness** — preconditions ([I4], stale), edge cases ([I9],
   duplicate and already-dispositioned uncovered), vocabulary totality over the
   declared scope ([I3], `accept`/`guard` unreachable). Failure modes are
   stated and the over-eager-decline analysis is sound as far as it goes.
4. **Silent failure / fail-closed** — both invariants are self-declared
   documentary with reviewers as enforcers, consistent with the parent's
   corrected accounting; no fail-open is disguised as a guard. Mutation check:
   deleting either invariant changes no test, which the proposal says. The
   *undisclosed* fail-open is the verification plan (#2 above), which reads as
   a control and is not one.
5. **Cross-document consistency** — swept `dev/plans/`, `dev/plans/archive/`,
   `dev/proposals/`, `dev/proposals/archive/`, `CHANGELOG.md`, and `git log
   --all` bodies for inbound references. Found six commit bodies (`a9bc372`,
   `89a8f1f`, `e59f9d4`, `8595274`, `640864e`, `2b37719`) and two newly-archived
   proposals the enumeration missed, and one named artifact
   (`lockfile-provenance-fields`, row at `dev/PLANNING.md:185` under
   `## Queued`) that is not in the population. `CHANGELOG.md` carries no
   pointer to the section. [I1].
6. **Drift** — the board's own outbound citations drift: `dev/PLANNING.md:927`
   cites `doctrine/proposals.md:370` / `doctrine/plans.md:611`, both moved to
   `:379` / `:622` by `5c85274`. The `'the same ones CI'` row at `:938` says to
   re-run its own grep rather than trust a count; I did — **21 tracked files,
   5 of them under `dev/plans/archive/`** — so that row's fix cascades into
   append-only artifacts, which the row does not say.
7. **Lifecycle / process placement** — the artifact is correctly placed
   (`Status: proposed`, `Plan review: required(Internal)`, split condition
   discharged by `791655a`). The gap is upstream of placement: no landed rule
   reaches the rows this pass proposes to touch. [I4].
8. **Domain / scope** — scope has not expanded; if anything it is too narrow to
   execute the vocabulary it invokes ([I3]). I hand-read ~12 rows across the
   security, scan-coverage, profile-parse-fail-open and gate-claims groups: they
   carry reproducers, measured figures (147 conda-only / 82 native; 16 LOW
   Bandit findings; 34 mis-marked nodes) and named revival conditions. **These
   read as genuine obligations, not ratchet artifacts.** The *Signals* section's
   feared outcome — "the 59 were mostly real work" — is, on my sample, the
   likely one.
9. **Name the satisfier** — every finding [I1]–[I10] names one; several name
   alternatives and mark which are sufficient alone.

### Not covered / low confidence

* **Same agent type.** Claude reviewing Claude, fresh session. This is the
  Internal floor and nothing more — no cross-type independence on this pass. I
  share the author's architecture and, plausibly, the habit that produced the
  inherited-figure errors in [I1] and [I2]; I caught those by re-running, not
  by thinking differently.
* **I did not adjudicate the 59 rows.** I hand-read ~12 and classified all 59
  with a keyword heuristic I know is wrong in both directions. My [I3] claim is
  a *direction*, deliberately not a count. If the Maintainer wants a number
  before deciding, that is a separate measured pass — see [I7]'s satisfier.
* **Commit-body sweep is not exhaustive.** I checked the 16 plan-archive
  commits and the first 25 proposal-archive commits. Older history, non-archive
  commits, and reflog-only objects were not swept. The six I found are a floor.
* **The tree moved under me.** 20 commits landed mid-review, 14 of them
  proposal-archive moves. `dev/PLANNING.md` is unchanged across the range, so
  board figures hold, but line citations into `dev/plans/*.md` shifted by ~4
  lines and I re-derived them at `46668c0`. Anyone re-running these checks
  should re-derive rather than trust my line numbers.
* **No code was run beyond the two checkers and `git`.** The proposal is
  correct that the suite is N/A; I did not run `python -m pytest
  bootstrap/tests`, so I make no claim about suite state.
* **`--include-archives`' 92 issues are uncharacterized.** I confirmed the
  count and spot-read three; I did not triage them or determine how many are
  pre-existing versus [I8]-relevant.

### Second-round recommendation

**Recommended — narrowly scoped, not a full re-read.**

The reasons are specific rather than reflexive. This proposal's two concrete
factual claims about closed artifacts were both wrong ([I1], [I2]), both were
inherited verbatim from a prior review rather than re-derived, and both took
under fifteen minutes to falsify by running `git show`. That is a *reproduction*
failure, and it is the third in this artifact family. A cross-type reader is
worth its cost on exactly the two surfaces where a wrong answer changes what the
pass does:

1. **The corrected inbound-reference enumeration** ([I1]) — mechanical, high
   demonstrated error rate, and it determines which rows C4's second eligibility
   rule protects.
2. **The scope/vocabulary interaction** ([I3]) — whether a
   `dev/PLANNING.md`-only pass can reach `accept` and `guard` at all. I believe
   it cannot; that is a reading of the landed doctrine text and deserves a
   different prior before the Maintainer relies on it.

I do **not** recommend a full cross-type re-read of the proposal's argument.
There is no code, no security surface, and no adopter-facing contract here; the
`identity-not-name` split reasoning is settled; and the remaining findings are
specification gaps whose satisfiers are stated and checkable. Spending a
cross-type round on the whole artifact would buy less than spending it on the
two items above.

The decision is the Maintainer's, per *recommend-and-decide*. The declared
`Plan review: required(Internal)` tier stands regardless of this
recommendation.

### Verdict

**REVISE.**

The work is real and should happen. The proposal as specified will not produce
it.

Three findings are load-bearing and none is cosmetic. [I3] means the pass, at
its declared scope, can only reach `wontfix` and `defer` — and C4 removes
`wontfix` for most rows — so the most likely output is a large re-`defer` batch
and a **longer** board, which is the opposite of what a reader of this proposal
would expect. [I1] and [I2] mean the hazard section this proposal inherited is
wrong in both of its concrete claims, in the direction that *understates* the
append-only population its principal safety rail is keyed on. [I4] means the
obligation the proposal leans on does not exist in any landed rule.

On the necessity question the brief is right to press: I sampled the rows and
they are **genuine obligations**, not the ratchet's artifacts. The proposal's
own *Signals* section names this as the outcome that would falsify its premise,
and on my reading it is the likely outcome. That does not make the pass
worthless — it makes it a **different pass**. What the board demonstrably needs,
and what one afternoon surfaced without a single Maintainer decision, is
*hygiene*: one duplicate to merge (`:845` / `:910`), one already-dispositioned
row to pass through (`:687`), two stale citations to repair (`:927`), 21 rows
with no in-repo source artifact to fence, and a re-derived inbound-reference
set. That is cheap, needs no `defer` authorizations, and makes the board better
on the axis the *Rationale* actually cares about.

The revision I would recommend: **re-scope around the hygiene pass as the
primary deliverable**, with per-item adjudication bounded to the subset that can
actually move under the chosen scope, and the eight source-artifact batches
named up front. That is a proposal the Maintainer can size and decide. This one,
as written, asks for authorization of an open-ended pass whose most likely
product is 59 rationales appended to 59 unchanged rows.

Not HOLD: nothing here says don't do this. Not SPLIT: the proposal is already
the split-out half, and splitting it again reproduces the seam it was created to
avoid. REVISE, with [I1], [I2] and [I3] as blocking and the rest as
should-fix.

---

## Response -- Claude (Strategy) -- 2026-08-04

**Model**: claude-opus-5

Grammar: Proposal-Response (`doctrine/proposals.md` > "Response — disposition
grammars"). Ten findings, accepted in full. **[I3] is decisive and re-scopes the
proposal**; the reviewer's position on necessity is adopted as the proposal's own.

**[I1]** accept — the inherited [I8] enumeration is wrong in both directions and
is retracted. `lockfile-provenance-fields`' row is under `## Queued`
(`dev/PLANNING.md:185`), not this section; and the closed-artifact set is
understated ~5x by omitting six immutable **archive commit bodies** and five
archived census-source plans. The corrected set is re-derived in the revision
rather than carried forward, per this repo's own rule about re-measuring rather
than restating.

**[I2]** accept — *"the pointer has already drifted once"* is **false and is
retracted**. Verified: at plan-open `3982918` the S2 row was already inside
`### Deferred follow-ups`; it has never moved. The archived plan's `:582`
"Queued row" was wrong *when written*, and its own `:913` records the correct
location. The proposal used a **pre-existing authoring error** as evidence of a
**drift hazard**, which is a different and much weaker claim. Worth naming: this
is the same failure as the parent's withdrawn figures — reaching for the reading
that supports the argument.

**[I3]** accept — **this is the finding that re-scopes the proposal.** The
declared scope (`dev/PLANNING.md` only, "writes no code") *structurally
forecloses* `accept` and `guard`: you cannot fix a follow-up or home it in a test
node while editing only the board. The available vocabulary collapses to
{`wontfix`, `defer`}, and C4 then bars `wontfix` for anything adopter-reaching,
release-blocking or Decision-needing. The predicted output of the pass as
specified is therefore **a large re-`defer` batch and a longer board** — the
proposal would have *added* rows in the name of draining them. Accepted without
reservation; the revision below removes the mass-adjudication scope entirely.

**[I4]** accept — no landed rule reaches these rows: C1's precondition is scoped
to *artifacts that archive*, and these rows are not artifacts. The premise that
"new doctrine does not clear rows deposited under the old rule" quietly assumed
the new rule *applies* to them. It does not. The sequencing note is also
stale-at-write (`4858c84` is an ancestor of `791655a`) and is dropped.

**[I5]** accept — forwarding entries in this pass's own commit body give no
back-link from the six stale commit bodies. Absorbed: the revision does not
re-route rows, so no forwarding is needed.

**[I6]** accept — "batches by source artifact" covers 38 of 59; 21 sit in topical
groups imported from another repository. The proposal assumed a structure the
board only partly has. Absorbed with the scope change.

**[I7]** accept with modification — the reviewer is right that refusing an
*estimate* was principled but refusing to *measure the population* was
over-correction, and right that **27** of 59 carry a revival condition (not the
18 with an explicit `*Trigger:*` field, which is a narrower thing than the
proposal implied). The modification: rather than measure the population to size
an adjudication, the revision drops the adjudication and measures only what the
hygiene pass acts on.

**[I8]** accept — and this one is self-inflicted. Both named checks are blind:
bare `check_cairn.py` does not read archives, and `claim_check.py dev/PLANNING.md`
returns OK over a **live stale citation at `dev/PLANNING.md:927`**, which cites
`doctrine/proposals.md:370` / `plans.md:611` for text that **the parent's own
`5c85274` moved** to `:379` / `:622`. Verified at HEAD. So the parent change
broke a citation on the board and its verification passed anyway — precisely the
"named trigger that does not check what it claims" pattern. This becomes the
revision's first deliverable.

**[I9]** accept — the duplicate `_infer_init_lock_axes` rows (`dev/PLANNING.md:845`
and `:910`, verified at HEAD) and the already-dispositioned `:687` are real board
defects with no token, and invariant (1) as written made a merge unrecordable.

**[I10]** accept — the 42.9%-of-1002 headline is dated to `4573c11`, a HEAD this
author's own lineage superseded five commits before the file was written. True
value at `791655a`: 41.5% of 1037. Corrected.

### On necessity — the reviewer's position is adopted

The reviewer hand-read ~12 rows and found *"reproducers, measured figures, and
named revival conditions — **genuine obligations, not ratchet artifacts**."*

**That falsifies this proposal's premise, and it is the most valuable thing this
review produced.** The parent proposal diagnosed a ratchet and implicitly assumed
the board's contents were its output. For future artifacts the diagnosis holds —
the composition failure is real and the rule that fixes it has landed. But the
**existing 59** are not the ratchet's residue. They are recorded work.

This proposal's own *Signals* section named exactly this as the falsifying
outcome: *"a board of 59 genuine obligations is a resourcing problem, not a
doctrine problem."* That signal has fired, before implementation rather than
after, which is what the section was for.

---

## Revised proposal

**Status**: revised

**The mass adjudication is withdrawn.** What remains is the hygiene the reviewer
identified: cheap, concrete, needing **zero Maintainer decisions**, and fixing
defects that are demonstrably real rather than presumed.

### H1 — the stale citation the parent change created

`dev/PLANNING.md:927` cites `doctrine/proposals.md:370` and `doctrine/plans.md:611`
for the sentence *"This makes the migration auditable from `git log` alone"*. The
parent's Chunk B (`5c85274`) moved that text to `:379` and `:622` while
deliberately not editing the sentence itself (it belongs to
`gate-claims-vs-enforcement` B2). The citation now points at unrelated lines —
`doctrine/proposals.md:370` is a `guard` example this change added. Re-point both.

### H2 — the duplicate row

`dev/PLANNING.md:845` and `:910` record the same `_infer_init_lock_axes` defect
from two different source plans. Merge into one row naming both provenances.

### H3 — the settled row

`dev/PLANNING.md:687` (SC4) already carries a Maintainer disposition — *"SC4 -
fold in"*, quoted verbatim in the row — and its trigger is the next supervised
ceremony. It is a scheduled item, not an undispositioned follow-up. Move it to
the section that holds scheduled ceremony work, or mark it so it is not
re-adjudicated.

### H4 — record the corrected inbound-reference set

Re-derive and record which closed artifacts actually name rows in this section —
including the **archive commit bodies**, which the original enumeration missed
entirely and which are the most immutable record of all. This is the durable
correction of [I1]; it is a *record*, not a re-route.

### H5 — correct the two false claims on the record

The "six artifacts / two archived" enumeration and the "already drifted once"
claim are wrong ([I1], [I2]). They are corrected in the Response above, which is
append-only and permanent. **No further action** — naming them here so the
revision does not appear to leave them standing.

### Explicitly NOT in scope

* **Adjudicating the 59 rows.** Withdrawn per [I3] — the scope cannot express
  `accept` or `guard`, so the pass could only lengthen the board.
* **Re-routing any row** except the H2 merge and the H3 move.
* **Any Maintainer `defer` batch.** The revised scope produces none.

### Verification

* `python scripts/claim_check.py dev/PLANNING.md` — must pass, and per [I8] this
  is known **insufficient**: it returned OK over H1's stale citation. The real
  check is opening the cited lines, which H1 does.
* `python scripts/check_cairn.py` — the bare form does not read archives ([I8]);
  stated so the check is not credited with reach it lacks.

### Author-accounting — revised

* **Invariants.** (1) *No row loses information* — the H2 merge preserves both
  provenances; enforcer: a reviewer diffing the row against its two sources.
  Documentary. (2) *No closed artifact's claim is falsified* — satisfied
  **vacuously**, because nothing is re-routed. Stronger than the original, which
  needed a forwarding mechanism to achieve it.
* **Failure modes.** H1 mis-repoints to another wrong line — fails open, caught
  by opening the line. H2 loses a provenance — fails open, caught by the diff.
* **Known omissions.** The 59 rows are **not** adjudicated and the board does not
  measurably shrink. That is the honest outcome of accepting [I3] and the
  reviewer's necessity position: the board is long because the work is real.

---

## Decision -- Human Maintainer -- 2026-08-04

**ACCEPT as revised** — the hygiene scope (H1–H5). The mass adjudication of the
59 rows is **withdrawn, not deferred**.

Scribed by Claude (Strategy) at the Maintainer's explicit instruction. The
authorizing words, verbatim:

> Honestly, I'm not going to assess how correct this proposal is. If you and the
> reviewer agree, I accept your decision. Please scribe this acceptance and
> proceed through implementation. This isn't mission critical, but is worth care.
> But it's not something that should slow us down.

**The condition is met, and what it ratifies is smaller than what was opened.**
The Internal review returned **REVISE**, not SHIP. The agreement between author
and reviewer is not that the proposal was right — it is that its central premise
was **wrong** and its scope had to be withdrawn. Recorded plainly so no later
reader mistakes this for an acceptance of the opened scope:

* **[I3]** — the declared scope structurally forecloses `accept` and `guard`, so
  the pass could only have produced a re-`defer` batch and a **longer** board.
* **The necessity finding** — a hand-read of ~12 rows found reproducers, measured
  figures and named revival conditions. The 59 are **genuine obligations, not
  ratchet artifacts**. The parent's diagnosis governs *future* artifacts; it does
  not indict the existing board.
* Two of the proposal's own factual claims were **retracted as false**.

**Plan review tier — superseded, no plan.** The header carries
`required(Internal)`, written for the withdrawn scope. Under the triage rule
(`doctrine/plans.md` > "Plan triage rule", as amended today) the revised scope is
a **trivial accept**: single-area (`dev/PLANNING.md`), one implementing commit,
and **no follow-up needing a `defer` home**. It therefore skips the plan and
archives at the implementing commit. This is the triage rule applied, not a
shortcut taken because the work was wanted quickly — and it is worth noting that
the rule reaching this verdict is one this same lineage amended hours earlier.

**Care that is still taken**, per *"worth care"*: the implementing change edits a
**shared communication file**, so it gets an independent read before the archive
even though no plan-archive precondition compels one.

**What is not carried.** No `defer`, no successor artifact, no board row. The
withdrawn adjudication is **not** parked for later revival — the reviewer's
necessity finding is the reason it should not happen, and preserving it as a
future obligation would re-commit the error this lineage exists to correct.

---

## Code review -- Claude (fresh session) -- 2026-08-04

**Model**: claude-opus-5
**Tier**: independent read of the implementing commit, per the Decision's *"the
implementing change edits a **shared communication file**, so it gets an
independent read before the archive"*
**Reviewed**: `bfb3875` ("board-retro-disposition: the hygiene pass (H1-H5)"),
one file, +48/-10, against its parent `5c752ab`
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python
3.13.13, the canonical interpreter per `bootstrap/DEPENDENCY_BUDGET.md`). The
ambient `python3` here is 3.12.9; both checkers were run under both and returned
identical output.

### What reproduced

Before the findings, the figures that hold. All commands re-runnable at
`bfb3875`.

* **Rows 59 -> 58.** `awk 'NR>=535 && NR<=964'` over `git show
  bfb3875^:dev/PLANNING.md` piped to `grep -c '^\* '` = **59**;
  `awk 'NR>=535 && NR<=1002' dev/PLANNING.md | grep -c '^\* '` = **58**. Section
  bounds derived independently: `### Deferred follow-ups (durable home)` at
  `:535` running to `### Release path` at `:965` (before) / `:1003` (after).
* **The sub-bullet claim.** The two explanatory items are `  1.` / `  2.`,
  indented and numbered; the `^\* ` count is unpolluted. Reproduced. (Under the
  looser `^\*` pattern the section goes 76 -> 78, but that pattern never equalled
  the row count — 76 != 59 before — so the commit's claim stands as worded.)
* **H1 landed on the right lines.** `doctrine/proposals.md:379` and
  `doctrine/plans.md:622` each carry *"This makes the migration auditable from
  `git log` alone"* verbatim. `grep -rn "auditable from .git log. alone"
  doctrine/` returns exactly those two lines and no other doctrine hit. The
  re-point is correct.
* **The H1 note about the checkers is true, and I verified it by execution
  rather than by reading.** I restored `bfb3875^:dev/PLANNING.md` into the
  working tree and ran both: `claim_check.py dev/PLANNING.md` -> `OK, no
  claim-check flags`; `check_cairn.py` -> `OK -- 176 Markdown file(s) scanned`.
  Both pass **over the stale citation**. The commit's account of why (path
  existence and line bounds, not target content) is accurate. Working tree
  restored; `git status --short dev/PLANNING.md` clean.
* **Both checkers at HEAD.** `claim_check.py dev/PLANNING.md` -> OK.
  `check_cairn.py` -> `OK -- 176 Markdown file(s) scanned; no issues; 48
  external link(s) not probed`. Both figures reproduce.
* **Scope fidelity.** I diffed the sorted row-title sets
  (`grep '^\* ' | sed 's/^\* //' | sort`) before vs after: a single line of
  difference — the removed `_infer_init_lock_axes` row. **No row was added, none
  was silently deleted, none was re-routed** beyond the H2 merge. Group
  membership is unchanged: byline 4, scan 1, release 2, fork 5, gate 7,
  identical before and after. One file touched.
* **"3 archived proposals cite this section by name."** Holds, and holds on the
  substantive criterion too: `dependency-advisory-coverage:930,1084` and
  `release-security-bar:1028,1085` carry literal `**Follow-ups migrated to:**
  dev/PLANNING.md > *Deferred follow-ups (durable home)*` blocks; the archived
  `deferral-discipline` proposal names the section in its D1 disposition row
  (`:1314`). Verified by opening each.
* **H3.** The SC4 marking is additive, sits on the existing row, and the
  Decision's H3 allowed *"Move it ... or mark it"*. Marking is one of the two
  authorised forms. No finding.

That is real work, correctly done, and the H1 fix in particular is exactly the
free demonstration the Internal review asked for. Nothing below contradicts any
of it.

---

### [C1] The H2 merge dropped the removed row's `*Trigger:*`, and both the board and the commit body assert that nothing was dropped -- this lineage's **sixth** recording of its own named failure mode

The removed row (`bfb3875^:dev/PLANNING.md:910-916`) carried four things:

1. provenance — *"was `contributor-entry` R1, which was superseded 2026-08-03
   without migrating it"*
2. the co-disclaimers — *"`fork-advisory-semantics` and `profile-parse-fail-open`"*
3. the defect statement — a root `CONTRIBUTING.md` read as evidence of a human team
4. **`*Trigger:*` the next proposal touching `bootstrap/_scaffold/upgrade.py`'s
   init-lock axis inference.**

Items 1-3 survive on the merged row (`dev/PLANNING.md:878-889`). **Item 4 does
not.** The merged row has no `Trigger` field of any kind:

```
$ grep -n "init-lock axis inference" dev/PLANNING.md
  (no match)
$ grep -rn "init-lock axis inference" dev/ | grep -v '/archive/'
  (no match)
$ awk 'NR>=878 && NR<=889' dev/PLANNING.md | grep -i trigger
  (no match)
```

The trigger is now reachable only from `bfb3875^` and from archived artifacts.

What the merged row *does* carry — *"Reachable only on a first `upgrade
--init-lock` in a tree with no committed `dev/.cairn/profile.yml`"* — is a
**reachability condition** (when the bug bites), not a **trigger** (when to
revisit the row). They are different fields doing different jobs, and under this
lineage's own doctrine the trigger is the load-bearing one: it is the revival
condition that makes a deferred row adjudicable rather than inert. The removed
row was one of the 18 the Internal review measured as carrying an explicit
`*Trigger:*`; the surviving row is one of the 29 that carry none.

Now the assertions. The board itself, at `dev/PLANNING.md:950-951`, states:

> *Both provenances are preserved on the surviving row; **nothing was dropped**.*

and the commit body states the same. Both are **false as written**, and the
board's copy is the durable one — it is the sentence a future reader of this
section will rely on when deciding whether the merge needs auditing.

This is the repo's named recurring failure mode — a protection asserted at the
strength intended rather than delivered — landing for the sixth time in this
lineage, and the third time in a commit body. It is also a direct violation of
the Revised proposal's own invariant (1): *"No row loses information — the H2
merge preserves both provenances; enforcer: **a reviewer diffing the row against
its two sources**."* The invariant's own enforcement mechanism is what caught
it. The stated failure mode (*"H2 loses a provenance — fails open, caught by the
diff"*) anticipated the wrong field: provenance survived, the trigger did not.

**Satisfier** — restore the trigger onto the merged row (*"`*Trigger:*` the next
proposal touching `bootstrap/_scaffold/upgrade.py`'s init-lock axis inference"*),
**and** narrow the board sentence from *"nothing was dropped"* to what is
actually true after the restore, e.g. *"both provenances and the trigger are
preserved on the surviving row."* If the trigger is judged redundant with the
reachability clause, say **that**, on the record, rather than asserting nothing
was dropped — the two are not the same field and the record should not imply
they are. **Blocking.**

---

### [C2] The "30 commit bodies" figure is reproducible only under an unstated, method-sensitive grep, and it counts a population ~4x larger than the paragraph it sits in is about

Board text (`dev/PLANNING.md:560-569`), under the heading **"Inbound references
— who points at these rows"**:

> As of 2026-08-04: **3** archived plans and **3** archived proposals cite this
> section by name, and **30** commit bodies across the repository carry a
> `Follow-ups migrated to:` / `Dispositions:` block. The commit bodies
> **dominate** and are the **most immutable** record of all [...] the
> closed-record set you might falsify is larger than the file tree suggests

I re-derived this over all 1013 reachable commits, three ways.

| Method | Result |
|---|---|
| Commits with a marker line **anchored at column 0** (`git log --all --format='%b' \| grep -cE '^(Follow-ups migrated to:\|Dispositions:)'`) | **30** |
| Commits carrying the marker **anywhere in the body** (`git log --all --grep='Follow-ups migrated to:' --grep='Dispositions:' --format=%H \| sort -u \| wc -l`) | **37** |
| Of the 30, those whose body names **this section** (`Deferred follow-ups` / `Archive-time follow-ups`) | **7** |
| Of the 30, those whose body names `dev/PLANNING.md` at all | **13** |

Verified with a Python pass over `git log --all --format=%H%x1f%s%x1f%B`; no
merge commits are in the set (checked via `%p`, zero multi-parent); `--all` and
HEAD-only agree; adding `--reflog` yields 38, so unreachable objects are not a
factor; no single body carries two anchored marker lines, so 30 lines is
genuinely 30 bodies.

Two problems.

**(a) The figure is method-sensitive by 23% and the method is not recorded.**
30 is the *column-0-anchored* count. The obvious re-derivation — the `--grep`
form any reader reaches for — returns **37**. A reader who re-derives gets a
different number and no way to tell which was intended. This is precisely what
the accepted [I1] satisfier required and did not get: *"Record the count with
its `as_of` **and its command**."* The `as_of` landed; the command did not. That
is a scope-fidelity miss against an accepted finding, not a style nit.

**(b) The figure measures a superset of what the paragraph is about.** The
heading asks *"who points at these rows"*; the conclusion is about *"the
closed-record set you might falsify"*. Only **7** of the 30 name this section —
the other 23 are archive commits pointing elsewhere entirely (`2882bab`
stage-commit-patterns, `d93c0d4` transition-lint, `add3c53` decision-rights-floor,
and 20 more, 17 of which do not mention `dev/PLANNING.md` at all). So *"the
commit bodies dominate"* rests on a number that is not counting inbound
references. On the inbound measure it is 7 commit bodies against 3-6 artifacts —
roughly parity, not dominance.

The paragraph's **conclusion** survives: the closed-record set is larger than the
file tree suggests, and commit bodies are the least correctable record. That is
directionally right and worth having on the board. The figure supporting it is
not the figure the sentence needs.

**Satisfier** — replace the clause with numbers that answer the heading's own
question, each with its command inline or footnoted, e.g.: *"7 commit bodies name
this section (13 name `dev/PLANNING.md`); 30-37 carry a disposition block
overall, the spread depending on whether the marker is required at column 0 —
`git log --all --grep=... | sort -u | wc -l`, `as_of` 2026-08-04, HEAD
`bfb3875`."* Keep the "most immutable" observation; it is the durable point and
does not depend on which number is used. **Blocking on the recorded-command
half.**

---

### [C3] The H2 merge falsified two *other* count claims in the same file, and neither was updated

The removed row lived inside the `*From `profile-parse-fail-open` (9):*` group.
Recounting every group at HEAD:

```
*From `byline-classification` (4):*        actual rows = 4   ok
*From `scan-coverage` (1):*                actual rows = 1   ok
*From `release-authenticity` (2):*         actual rows = 2   ok
*From `fork-advisory-semantics` (5):*      actual rows = 5   ok
*From `profile-parse-fail-open` (9):*      actual rows = 8   <-- STALE
*From `gate-claims-vs-enforcement` (7):*   actual rows = 7   ok
                                    census total = 27
```

Every other header matches its row count exactly, which establishes that `(N)`
is read as the group's row count and that `(9)` is now wrong.

Second, the census preamble at `dev/PLANNING.md:781-784`:

> 95 candidate items, 29 already homed, 38 judged fenced residuals rather than
> follow-ups, and **the 28 below** with no durable home at all.

There are **27** below. `4+1+2+5+9+7 = 28` before the merge; `4+1+2+5+8+7 = 27`
after. Both figures were internally consistent before `bfb3875` and are not now.

There is a defensible reading on which `(9)` and `28` are *historical* records of
what the 2026-08-04 census produced rather than live counts — in which case they
should not change. But then the merge has silently created a documented
discrepancy that nothing in the file reconciles, in a shared communication file,
one paragraph after a sentence asserting *"nothing was dropped."* Either reading
requires an edit; only the choice of edit differs.

**Satisfier** — either (a) update `(9)` -> `(8)` and *"the 28 below"* -> *"the 27
below"*, or (b) leave both as historical and add a half-line to the merge
pointer: *"(the group header's `(9)` and the preamble's `28` record the census as
taken; one of those rows is now merged above)."* (a) is cheaper and loses nothing
the pointer paragraph does not already carry. **Blocking** — this is the same
class of defect the commit exists to fix, introduced by the fix.

---

### [C4] The new section-head prose generalises a sample drawn entirely from the census half to all 58 rows, and it now governs how future readers treat the whole section

I sampled independently rather than deferring to the Internal review's read,
because this claim is the one that will outlive the commit.

Board text (`dev/PLANNING.md:542-558`): *"**These rows are recorded work, not a
backlog to be cleared**"*, supported by finding 1: *"A hand-read sample found
reproducers, measured figures and named revival conditions — **genuine
obligations, not the deferral ratchet's residue**."*

**Where the claim holds.** I hand-read the security and lifecycle rows and rows
from every census group. `dev/PLANNING.md:612-626` (install-integrity trust
anchor) carries a reproduced tamper bypass with file and line
(`verify_integrity.py:47`), a revival condition, and a stated reason it is a
proposal rather than a patch. `:628-645` (conda advisory coverage) carries
measured figures (147 conda-only / 82 native, `as_of 2026-08-03`), four named
evaluated tools, and inherited watch-outs. `:584-596` (interpreter trust-root S2)
carries the red-team result and a named revival design. These are unambiguously
genuine obligations and the claim is right about them. **I agree with the
conclusion for this half.**

**Where it does not.** The section splits cleanly at the first `*From ...*`
header: **27 census rows** below, **31 topical rows** above — the latter
imported, per the section's own preamble, *"from the modflow_tools-side batch
ledgers"*. Measured over whitespace-normalised row text with a case-insensitive
`trigger:|revive|revival condition` match:

| | rows | with a trigger / revival condition |
|---|---|---|
| topical (imported) | 31 | **13** |
| census | 27 | 16 |
| **all** | **58** | **29** |

Half the section carries no revival condition of any kind, and the shortfall is
concentrated in the imported half. Thirteen topical rows are under 200
characters with no reproducer, no measurement and no trigger — e.g.
`dev/PLANNING.md:582-583`: *"**`_agent_of` round-suffix regression test** — pin
the `## Review (Round N)` header shape in the Cairn tree."* That is a one-line
`guard` candidate, not a reproducer-bearing obligation. Others in the same class:
*"Facade residuals (B-#1/2)"*, *"End-gate frozen-set decision (C-#4)"*,
*"Side-door non-executable surfaces — **disposition for** the onboarding
activation log..."* (a row naming its own missing disposition), *"Refine the
intent tool's necessity test"*, *"Move `dev/intent-config.json` -> `dev/.cairn/`"*.

And the sample the claim rests on came from the other half. The Internal review's
own coverage line says it hand-read *"~12 rows across the **security,
scan-coverage, profile-parse-fail-open and gate-claims** groups"* — three of
those four are census groups, and none is in the imported set that [I6]
separately identified as having no in-repo source artifact at all.

I am not saying the imported rows are ratchet residue; I did not adjudicate them
and this review claims no routing. I am saying the **warrant as written**
(*reproducers, measured figures, named revival conditions*) is demonstrably
absent for 29 of 58 rows, and the sentence asserts it of all of them. Same
failure shape as [C1] and [C2]: the claim is made at the strength intended, not
the strength the evidence delivers.

The consequence is real because of where it now lives. A future agent reading
*"recorded work, not a backlog to be cleared"* at the head of the section is
being told not to try — including on rows whose own text says the opposite. SC3
at `:704-705` reads *"the guard is one assertion and **should be written rather
than re-deferred**"*; SC5 says *"the guard is two assertions."* Those rows want
`guard`, not protection from adjudication. Finding 2 of the new block is careful
and correct — it says a **board-only** pass cannot dispose of these rows, which
is exactly [I3] and is well hedged. The heading above it is not: it converts "a
board-only pass cannot clear these" into "these are not a backlog," which is a
different and stronger claim.

**Satisfier** — two narrow edits. (1) Attribute the sample: *"A hand-read sample
of ~12 rows, drawn from the census groups, found reproducers, measured figures
and named revival conditions; the imported topical rows above were not sampled,
and 29 of the 58 carry no revival condition in any form."* (2) Retitle the block
to what finding 2 actually supports — *"**A board-only pass cannot dispose of
these rows**"* — leaving open that a scoped `guard`/`accept` pass can and, for
the one- and two-assertion guards the board itself names, should. **Should-fix
before archive**; the second edit is the one that prevents the lasting damage.

---

### [C5] "3 archived plans cite this section by name" counts two artifacts' own internal headings, and re-includes the one artifact the accepted Response promised to drop

`grep -rln "Deferred follow-ups\|Archive-time follow-ups" dev/plans/archive/`
returns exactly three files, which is presumably the source of the 3. Opening
each match:

* **`lockfile-provenance-fields.md:407`** — the match is the plan's **own section
  heading**, *"**Deferred follow-ups, per the archive-preconditions rule** —
  both already homed outside this plan"*. Reading on to `:409-410`: P4 is homed
  *"at its `dev/PLANNING.md` **'Lockfile schema validate-on-read' Queued row**"*
  — `dev/PLANNING.md:185`, inside `## Queued` (`:120-268`), **not this section**.
  This is [I1]'s wrong inclusion, verbatim. The Response accepted it —
  *"`lockfile-provenance-fields`' row is under `## Queued` (`dev/PLANNING.md:185`),
  not this section"* — and [I1]'s satisfier said in terms *"**drop
  `lockfile-provenance-fields` from the list**."* H4 was supposed to be the
  durable correction of [I1]; it re-committed [I1]'s error into the board.
* **`interpreter-trust-root-fallback.md:582`** — also its own heading. This plan
  *is* a genuine inbound reference (S2, confirmed at `:913`), but not via the
  string that matched.
* **`deferral-discipline.md:846`** — a genuine mention of `### Deferred
  follow-ups (durable home)`, but as the object of the parent plan's own work,
  not as a home its archive precondition was discharged against.

So on the criterion [I1] established and the Response adopted — *artifacts that
cite this section as the home against which their archive precondition was
discharged* — the archived-plan count is **1**, not 3. On a bare-grep criterion
it is 3, but then two of the three are counting the artifacts' own headings and
the number is not measuring citation at all.

The archived-**proposal** figure of 3 survives both criteria; I verified each by
opening it. The defect is confined to the plans half.

**Satisfier** — state the criterion alongside the number and apply the one the
Response accepted: *"1 archived plan (`interpreter-trust-root-fallback`, S2) and
3 archived proposals name a row in this section as a discharged home;
`lockfile-provenance-fields`' P4 row is under `## Queued` and is **not** in this
population (corrected per [I1])."* **Should-fix** — the number is small either
way, but silently re-including the artifact a review dropped is how a correction
gets un-corrected.

---

### [C6] H1 re-applied the citation form that had just failed, in a file that already uses a stable alternative

H1 is correct and I verified both new line numbers by opening them. This finding
is about the *form*, which is the more durable fix.

The same sentence has now been cited at **three** different line pairs across
this repo's record:

* `dev/proposals/archive/2026-08-03-claude-gate-claims-vs-enforcement.md:1033` —
  *"`doctrine/proposals.md` line 360 and `doctrine/plans.md` line 602"*.
  Permanently stale, in an append-only artifact, uncorrectable.
* `dev/PLANNING.md` before `bfb3875` — `:370` / `:611`. Stale.
* `dev/PLANNING.md` after `bfb3875` — `:379` / `:622`. Correct today.

Two drifts in one lineage, both caused by edits *above* the sentence rather than
to it, and neither catchable by `claim_check.py`, which validates bounds and not
targets (demonstrated above by execution). The third citation is one insertion
above line 379 away from becoming the fourth.

The alternative is already in use in this exact file. `dev/PLANNING.md` cites by
section name at `:9`, `:19`, `:444` (`doctrine/lifecycle.md` > "Archive
precondition" — in the preamble of the very section that governs these rows) and
`:493`; `AGENTS.md` uses the same form throughout. The target sentences sit under
stable named headings: `doctrine/proposals.md` > **"Archive preconditions"**
(`:342`) and `doctrine/plans.md` > **"Lasting-truth migration doctrine"**
(`:585`). Neither heading moved in this lineage.

**Satisfier** — re-point by section name, optionally keeping the line as a
navigational aid: *"(`doctrine/proposals.md` > "Archive preconditions" and
`doctrine/plans.md` > "Lasting-truth migration doctrine" — at `:379` / `:622` as
of 2026-08-04)"*. Survives insertion above, matches the file's own convention,
and does not silently rot. **Optional** — H1 as landed is correct; this is a
robustness upgrade, not a defect.

---

### Falsification ledger

**Probed and found no defect:**

* **Did H1 land on another wrong line?** No. Opened both targets; also ran
  `grep -rn "auditable from .git log. alone" doctrine/ templates/ dev/` — the
  sentence exists at exactly two doctrine locations and both are the cited ones.
  The neighbouring lines (`:375-377`, `:618-620`) are the `Follow-ups migrated
  to:` back-compat paragraph, so an off-by-a-few would have been visible.
* **Was any row silently deleted or re-routed?** No. Sorted row-title set diff:
  exactly one deletion, zero additions, zero modifications to other titles.
  Per-group counts unchanged except `profile-parse-fail-open`.
* **Was a new board row added?** No — the Decision's *"no board row"* holds. The
  three additions are prose blocks and one italic pointer paragraph, none a
  `^\* ` row.
* **Did the commit exceed the accepted scope?** One file, `dev/PLANNING.md`. The
  section-head prose block is beyond the enumerated H1-H5, but the commit body
  declares it (*"Also recorded at the section head"*) rather than slipping it in,
  and it transcribes findings the Decision itself recorded. Disclosed, not
  silent — [C4] is about its content, not its presence.
* **Commit-authority check.** `dev/PLANNING.md` alone is *not* covered by
  `AGENTS.md`'s deliberation carve-in (neither a one-line lifecycle row-move nor
  the goodnight scrub), so this needed explicit authorisation. The Decision
  carries it verbatim — *"Please scribe this acceptance and proceed through
  implementation"* — which is also the *"explicit instruction"* serialization
  point the shared-communication-file rule requires. Clean.
* **Is the "30" inflated by merge commits, unreachable objects, or this
  lineage's own commits?** No merge commits (zero multi-parent); `--reflog` adds
  one; six of the 37 are this lineage's own, which the figure does not exclude
  but which does not explain the 30/37 gap. The gap is entirely the column-0
  anchor.
* **Is 59 -> 58 stated anywhere else that is now stale?** No live artifact
  outside the proposal itself asserts a row count for this section; the
  proposal's own "59" figures are in append-only sections and correctly stay.
* **Body length.** 49 lines against `AGENTS.md`'s *"soft cap ~50"*. Inside the
  cap, though at it for a single-file hygiene commit. Not a finding.
* **Pre-existing, not this commit:** the census preamble asserts *"A plan does
  not archive until its items here are landed"* while `scan-coverage` archived
  (`89a8f1f`) with SC4 outstanding on the board. That tension predates
  `bfb3875` and H3's marking makes it more visible rather than causing it.
  Raised for the record, not as a finding against this commit.

**Failure modes tested:** information loss across the merge (found — [C1]);
count claims elsewhere in the file invalidated by the row removal (found —
[C3]); figure reproducibility under alternative methods (found — [C2]);
citation-target correctness (clean); scope creep by row addition or re-route
(clean); sample-to-population generalisation in the new prose (found — [C4]);
re-introduction of an error a prior review retired (found — [C5]).

**Verification run:** `claim_check.py dev/PLANNING.md` and `check_cairn.py` at
HEAD *and* at `bfb3875^` (by restoring the parent file into the tree, then
restoring HEAD's), under Python 3.13.13. All four runs OK. `git log --all` sweep
over 1013 commits, twice, by two independent methods.

**Consciously not run:** `python -m pytest bootstrap/tests`. The commit touches
one Markdown file and no code; the proposal's *"Tests — N/A"* is correct for the
revised scope. I therefore assert nothing about suite state.

**Residual risks:**

* I did not adjudicate the 58 rows, and [C4] deliberately makes no routing
  claim. My topical/census split is by the first `*From ...*` header — a
  structural proxy for [I6]'s hand classification that does not match it exactly
  (31/27 vs [I6]'s 21/38, because `Scan coverage` and `Release authenticity` sit
  above the first `*From` header). The direction — revival conditions
  concentrated in the census half — holds under either split; the exact figures
  are mine, at `bfb3875`, and should be re-derived rather than carried forward.
* My revival-condition regex (`trigger:|revive|revival condition`, case-
  insensitive, over whitespace-normalised row text) misses any phrasing using
  none of those words. A first pass that did not normalise line breaks
  undercounted by three; I caught and corrected it. 29/58 is the corrected
  figure and is a floor, not a ceiling.
* Same agent type as the author — a fresh-session Claude read of Claude's work,
  structurally the Internal floor, not cross-type independence. Everything I
  found is a reproduction error (re-running a grep, opening a cited line,
  diffing a removed row), not an error of judgement; I would not claim a
  different prior on the judgement calls, particularly [C4]'s.
* `check_cairn.py --include-archives` was not run. [I8] established a 92-issue
  baseline there; I did not re-derive it or check whether `bfb3875` moved it.
  The commit adds no archive-facing citations, so I judged the risk low, but the
  claim is unverified.

### Covered / Not covered

**Covered.** *Claims* — every numeric figure in the commit body and the added
board prose re-derived independently: 59 -> 58 (reproduced), the sub-bullet
non-pollution claim (reproduced), `claim_check` / `check_cairn` OK across 176
files (reproduced, both interpreters), 3 archived proposals (reproduced under
both criteria), 3 archived plans ([C5]), 30 commit bodies ([C2]). *Citation
targets* — `doctrine/proposals.md:379` and `doctrine/plans.md:622` opened and
confirmed verbatim ([C6] on form only). *Information preservation* — removed row
diffed field-by-field against the survivor ([C1]). *Cross-document consistency
within the edited file* — all six group headers and the census preamble
recounted ([C3]). *Scope fidelity* — sorted row-set diff, group-membership diff,
file count, commit-authority chain: clean. *New governing prose* — sampled
against the population it governs ([C4]). *Silent failure* — both named checks
executed against the **pre-fix** file to confirm the commit's own claim that
they pass over a stale citation; confirmed by execution, not by reading.

**Not covered / low confidence.** No adjudication of the 58 rows. No
`--include-archives` run. No test suite. No review of the deliberation record
beyond what establishes the accepted scope (Internal review, Response, Revised
proposal and Decision read in full; the parent `deferral-discipline` proposal
consulted only for the archive-precondition rule and its Chunk B commit
`5c85274`). Same agent type, so no cross-type independence on judgement.

### Verdict

**REVISE.**

The hygiene is real and its hardest-to-fake parts landed: H1 re-points to the
right lines, H3 is a faithful marking, and the scope held exactly — one row
removed, nothing added, nothing re-routed, one file touched.

But this is a change to a **shared communication file**, and it leaves four
statements in that file that are not true as written: *"nothing was dropped"*
when a trigger was ([C1]); a group header reading `(9)` over 8 rows and a
preamble reading *"the 28 below"* over 27 ([C3]); a figure headed *"who points at
these rows"* that counts 30 commit bodies of which 7 do ([C2]); and a count that
re-includes the artifact its own accepted Response promised to drop ([C5]).
Three of the four are this lineage's named failure mode — asserting at the
strength intended rather than delivered — which is why this is REVISE rather
than APPROVE WITH FOLLOW-UPS: a follow-up leaves the falsehoods on the board
across the archive, and the archive is what makes them permanent.

[C1], [C2] (the recorded-command half) and [C3] are **blocking**. [C4] and [C5]
are **should-fix before archive**; [C4]'s second edit is the one I would not
skip, because *"recorded work, not a backlog to be cleared"* at the head of the
section is the sentence that will govern the next agent who arrives, and the
board's own SC3/SC5 rows say the opposite about themselves. [C6] is optional.

Every one of these is a line or two of text. I would expect the whole revision in
a single follow-up commit, after which this artifact archives cleanly.

On the substance the Decision cared about: I agree the mass adjudication was
rightly withdrawn, I agree a board-only pass structurally cannot dispose of these
rows, and I agree — for the census half, which I read — that they are genuine
obligations. My disagreement is with how far that last agreement was stretched,
not with the finding itself.

---

## Response to the code review -- Claude (Strategy) -- 2026-08-04

**Model**: claude-opus-5

Grammar: Code-review-Response. Six findings, all accepted, all closed by the
sharpening commit `119b645`.

* **[C1]** accept (followup commit `119b645`) — **the sixth instance**, committed
  inside the pass whose purpose was to correct the fifth. The H2 merge dropped
  the removed row's `*Trigger:*` while the board text and the commit body both
  said *"nothing was dropped"*. I read the surviving row's *"Reachable only
  on…"* — a reachability condition — as the trigger, and they are not the same
  thing. The Revised proposal named "a reviewer diffing the row against its two
  sources" as invariant (1)'s enforcer; that enforcer worked exactly as
  specified. Trigger restored with its provenance labelled.
* **[C2]** accept (followup commit `119b645`) — the "30" reproduced only under an
  unrecorded column-0-anchored grep (`git log --grep` gives 37), and the
  paragraph was headed *"who points at these rows"* while only 7 of the 30 do.
  Two questions were being conflated. Split, with the **command** recorded rather
  than the bare figure — which is what the accepted [I1] satisfier asked for and
  what the first attempt half-delivered.
* **[C3]** accept (followup commit `119b645`) — the merge falsified two counts
  elsewhere in the same file (`(9)` over 8 rows; *"the 28 below"* over 27). A
  row-count edit has file-wide consequences, and I checked none of them. Both
  corrected and annotated so the change is legible.
* **[C4]** accept (followup commit `119b645`) — the section-head prose
  generalised a ~12-row sample **drawn entirely from the census half** to all 58
  rows. Measured: 29 of 58 carry no revival condition, concentrated in the ~31
  imported rows. Restated to the defensible claim. This was the finding with the
  longest half-life, since that prose governs how every future reader treats the
  section.
* **[C5]** accept (followup commit `119b645`) — "3 archived plans" re-included
  `lockfile-provenance-fields`, the exact artifact the accepted Response had
  promised to drop. Substantive count is **1**.
* **[C6]** accept (followup commit `119b645`) — H1 re-applied the line-citation
  form that had just failed, putting the same sentence at its third line pair.
  Now cited by stable section name.

**Incidental observations, not adopted as follow-ups.** The reviewer noted (a)
the census preamble's *"A plan does not archive until its items here are landed"*
is in tension with `scan-coverage` having archived at `89a8f1f` with SC4
outstanding, and (b) `dev/measurement/collision_log.md` and
`dev/measurement/snapshots/` are untracked. Both are **pre-existing and outside
this artifact's causation**; adopting them as this artifact's follow-ups would
manufacture obligations, which is the failure this lineage exists to correct.
Recorded here so they are visible, and surfaced to the Maintainer rather than
homed on the board.

## Dispositions

```
Dispositions:
* [C1] merge dropped the row's Trigger    -> accept (commit 119b645)
* [C2] "30 commit bodies" unreproducible  -> accept (commit 119b645)
* [C3] merge falsified two other counts   -> accept (commit 119b645)
* [C4] sample over-generalised to all 58  -> accept (commit 119b645)
* [C5] archived-plan count includes a row -> accept (commit 119b645)
       under ## Queued
* [C6] line-citation form re-applied      -> accept (commit 119b645)
```

**Zero `defer` dispositions** — no Maintainer authorization needed, and **no row
is added** to `dev/PLANNING.md`. Net board delta: **−1** (59 → 58 rows), the
first negative delta this board has recorded.

### Evidence ledger

**Evidence shipped.** `claim_check` OK on `dev/PLANNING.md`; `check_cairn` OK
across 176 files. The reviewer independently re-derived the 59 → 58 row count
from its own section bounds, confirmed H1's re-point by opening both cited lines,
verified scope fidelity by a sorted row-title diff (exactly one deletion, zero
additions, zero re-routes, one file), and confirmed **by execution** that both
checkers pass over the *pre-fix* stale citation — restoring `bfb3875^`'s file and
re-running. That last one is the load-bearing negative result: it establishes
that neither named check would have caught H1's defect.

**Evidence deferred.** None.

**Residual risks.**
* The **~31 imported rows are unassessed.** [C4]'s corrected prose says so
  explicitly rather than implying coverage the sample does not have.
* **Nothing mechanically checks a group header's `(N)` against its row count** —
  [C3] was found by a reviewer, and a future row edit can break it the same way.
* The board is **still 58 rows and ~1075 lines**. This pass was hygiene; it did
  not and could not drain the section.

### Loop-fidelity sign-off

The implementation commits `bfb3875` and `119b645` match the accepted
**`## Revised proposal`** section (H1–H5) as ratified by the Decision at
`5c752ab`. The withdrawn mass adjudication was **not** performed: verified by the
reviewer's sorted row-title diff showing zero re-routes beyond the single H2
merge, and no board row was added.
