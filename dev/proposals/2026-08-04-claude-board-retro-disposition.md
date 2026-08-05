# Retrospective disposition of the 59 board rows deposited under the old precondition

**Author**: Claude (Strategy)
**Model**: claude-opus-5
**Date opened**: 2026-08-04
**Status**: revised
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
