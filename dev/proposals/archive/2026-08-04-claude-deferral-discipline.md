<!-- claim-marker maintenance: dev/plans/transition-lint.md moved to
     dev/plans/archive/transition-lint.md on 2026-08-10; this proposal's
     closed [I8]-adjacent citation at :906 predates the move and is
     append-only, so the path is marked here rather than rewritten. -->
<!-- claim-check-allow: dev/plans/transition-lint.md -->

# Deferral is a Maintainer-approved exception, not an author default

**Author**: Claude (Strategy)
**Model**: claude-opus-5
**Date opened**: 2026-08-04
**Status**: accepted
**Touches**: `doctrine/lifecycle.md` (archive precondition — canonical), `doctrine/proposals.md`, `doctrine/plans.md`, `doctrine/dual-review.md` (lens #9), `doctrine/lifecycle-contract.md` (plan state machine), `templates/core/dev/PLANNING.md`, `templates/core/dev/plans/_template.md`, `templates/core/dev/proposals/_template.md`, `templates/skills/_lib/lifecycle_planner.py`, `dev/plans/_template.md`, `dev/proposals/_template.md`, `dev/PLANNING.md` (retrospective pass)
**Related**: the 2026-08-04 six-plan census (`4573c11`); `dev/PLANNING.md` > "Archive-time follow-ups — the 2026-08-04 six-plan census"
**Plan review**: required(Internal) — see *Plan review tier* below for why this is the floor and what escalates it

## Context

`dev/PLANNING.md` is being consumed by its own success. The measurements, all
`as_of 2026-08-04` at HEAD `4573c11` under the canonical interpreter:

| Measure | Value |
|---|---|
| `dev/PLANNING.md`, earliest commit on 2026-07-22 | **343 lines** |
| `dev/PLANNING.md` at HEAD | **1002 lines** |
| `### Deferred follow-ups (durable home)` | **430 lines, 59 items** — 43% of the file |
| Items under `## Active` | **3** |
| The six-plan census, by its own accounting | **95 candidate follow-ups from 6 plans** — ~16 per plan |

The board tripled in thirteen days. The backlog-to-in-flight ratio is roughly
20:1. No item in `dev/` or `doctrine/` currently tracks this as a problem —
verified 2026-08-04 by grep across both trees for board-growth,
deferral-accumulation and follow-up-budget phrasings; zero hits.

### The generative mechanism is a one-way ratchet in three composed rules

None of the three is wrong alone. Composed, they have no drain.

1. **`doctrine/dual-review.md:245` (review-sweep lens #9)** — "every finding
   states the test / guard / doc / scope-cut / explicit `wontfix` that would
   close it. A finding with no satisfier is an observation, not yet a finding."
   This is a *promotion* rule: attaching a satisfier converts an observation
   into a finding. `doctrine/dual-review.md:256` then flags low finding-density
   as evidence the sweep has gone ritual — so the doctrine correctly tells
   reviewers that finding little is suspicious.
2. **The scope fence** — `doctrine/plans.md:249` makes "what must explicitly
   *not* change in this pass" a load-bearing plan question, and
   `dev/plans/_template.md:111` operationalizes it as *"work the proposal
   deferred to a follow-up"*. A finding inside the fence is fixed; a finding
   outside it is **deferred**, never discarded.
3. **`doctrine/lifecycle.md:403`** — the archive precondition: every
   explicitly-deferred follow-up must have a durable home outside the file
   before archive, and `dev/PLANNING.md` is the first-named home
   (`doctrine/proposals.md:349`).

Composed: **review → finding → outside the fence → deferred → must be homed →
board.** No step in that chain discards, and no doctrine anywhere describes
*declining* a follow-up. The only exits the board defines are the removal
preconditions for `completed` items (`doctrine/lifecycle.md:423`). Deferred
items carry a date marker and a staleness sweep that can only **reaffirm**
them.

The apparatus is working exactly as designed. The design has no drain.

### Two second-order errors the same rules produce

**The trigger rule is inverted.** Current practice, established by
`byline-classification` and now used board-wide, holds that *"a residual with a
named trigger is a decision; one without is debt."* Of the 59 deferred items,
**30 name a trigger** (`as_of 2026-08-04`). But a named *mechanical* trigger is
precisely the condition under which a board row is unnecessary. If the revival
condition is "any edit to `scan_targets()`", the correct home is an assertion or
a comment at `scan_targets()` — something that fires when the condition is met.
The board row is a strictly *worse* trigger: it fires only if a human re-reads
1002 lines during a scrub. **12 of the 59** name a trigger that is a code or
ceremony event an implementing agent would encounter anyway; those are misfiled,
not deferred.

**Nothing prices the deposit.** Deferral is today a *unilateral author act with
zero cost*. The author writes "deferred to a follow-up" and every downstream
reader is obliged to preserve it. That is an author granting themselves scope
relief and charging the cost to the board — and to every future cold reader. It
is also, structurally, the **default**: deferral is what happens when nobody
decides.

**The consequence floor is missing.** Only **10 of 59** items mention an adopter
(`as_of 2026-08-04`). On the same board, at the same weight, sit "0.3 external
correctness test — **blocks the 0.4 public release**" and "Two `test_presets.py`
nodes use `_yaml_load` as its own oracle."

## Proposal

Replace the single-route archive precondition with a **disposition ladder**.
Every finding not fixed in the current scope routes to exactly one rung, and an
author may only reach a lower rung after recording why each rung above it did
not take it.

| Rung | Disposition | Approval | Durable home |
|---|---|---|---|
| **a** | **Fix in scope** | none — the default | the implementing commit |
| **b** | **Home in code** — a test, assertion, guard, or call-site comment that *fires* when the trigger condition is met | none | the code itself |
| **c** | **Decline, with a recorded reason** | none, but **recorded** | the archive commit body |
| **d** | **Defer to the roadmap board** | **Maintainer, quoted verbatim** | `dev/PLANNING.md` |
| **e** | **Open a successor proposal** — a genuine discovered blocker whose in-scope fix would be the bundling doctrine already forbids | **Maintainer** | its own proposal |

Concretely, the changes:

**1. `doctrine/lifecycle.md` > "Archive precondition" (canonical) — the
precondition becomes a routing rule, not a preservation rule.** Its stated
purpose is *"that nothing was silently dropped"*; today it conflates *not
silent* with *kept forever*. Amended, the precondition is satisfied when every
explicitly-deferred follow-up carries **a recorded rung**, not necessarily a
board row. A decline with a reason satisfies it. The auditability requirement is
unchanged and strengthened: the `Follow-ups migrated to: …` block becomes a
**`Dispositions: …`** block naming the rung for every item, so a cold reader can
still reconstruct that nothing vanished.

**2. Rung (d) requires a quoted Maintainer authorization.** The existing
Decision-scribing attestation form is reused verbatim — the authorizing phrase
quoted and visually isolated, per `AGENTS.md` > "Scribing a Decision". Deferral
is a decision about project scope; scope is Maintainer-held.

**3. Deferral requests are batched at one serialization point.** The author
presents all rung-(d) candidates as a single list at plan review, or at
archive-preparation if the plan is review-exempt — never one at a time. This is
what bounds the Maintainer's load, and it is the load-bearing half of change 2.

**4. `doctrine/dual-review.md` lens #9 gains the ladder as its satisfier
vocabulary.** The lens currently ends at "names a satisfier"; it now requires
the satisfier to be a **rung**, which makes "what closes this" and "who pays for
it" the same question. Lens #9's promotion function is preserved intact —
reviewers should keep finding things; the change is only where findings land.

**5. `doctrine/plans.md` and `doctrine/proposals.md` restate the ladder by
pointer**, and `doctrine/lifecycle-contract.md:137`'s `review → archived` row
is amended so the state machine's precondition matches the doctrine.

**6. The templates carry the same change** —
`templates/core/dev/PLANNING.md:100`, `templates/core/dev/plans/_template.md`,
`templates/core/dev/proposals/_template.md`, and Cairn's self-hosted copies
`dev/plans/_template.md` + `dev/proposals/_template.md`. Doctrine that changes
without its template is drift, and the loop-fidelity lens catches it.

**7. `templates/skills/_lib/lifecycle_planner.py`** carries the durable-home
text at two sites (`:879` and `:1024`). Both are **unconditional** — the gate at
`:878` is literally `(True, "every deferred follow-up has a durable home…")` — a
documentary reminder the planner prints but cannot verify. The strings are
re-worded to the ladder. **No new checking is proposed**; a reminder that cannot
verify itself is stated as a reminder, per `AGENTS.md` > "Name the trigger,
check what it checks".

**8. A retrospective pass over the existing 59 items.** New doctrine does not
clear items deposited under the old rule. One bounded chunk re-routes the
current `### Deferred follow-ups (durable home)` section through the ladder.
Expected shape, not a commitment: the 12 mechanically-triggered items to rung
(b), a substantial fraction of the remainder to rung (c), and whatever survives
presented to the Maintainer as one batched rung-(d) list. **This chunk is
in-scope and must not itself be deferred** — deferring the fix for deferrals
would be self-refuting.

### The governing principle, stated so it is falsifiable

**An artifact closes more than it opens.** The measurable form: an archived
proposal or plan should have a **net effect on the board of ≤ 0**. `as_of
2026-08-04` the six-plan census puts the current figure at roughly **+16 per
plan**.

This is a target for a goodnight-scrub reading, **not** a mechanical gate. No
checker is proposed: counting "rows this artifact added" requires attributing
board rows to artifacts, which the board does not structurally record. Stating
it as a gate would be a claim at a strength not delivered.

### Documentation / doctrine surface

This proposal is **almost entirely** a doctrine and template change; the eleven
files are enumerated in `Touches` above and itemized in items 1–7. The routing
per `docs/DOCUMENTATION_PLAN.md`: the ladder is cross-cutting **prescription**,
so its canonical home is the governing/doctrine layer (`doctrine/lifecycle.md`,
with the others pointing at it) and its adopter-facing surface is the
`templates/core/` mirror. Nothing routes to `docs/` — the ladder describes what
contributors must do, not what the software is.

`AGENTS.md` is **not** touched. The rule is deliberation-process doctrine, which
`doctrine/doc-governance.md` routes to `dev/agent_collaboration.md` and
`doctrine/`, not to the operational file. This is a deliberate placement call
and a legitimate thing for a reviewer to challenge.

### Doctrine-change rate-limit

This proposal changes doctrine and must clear
`doctrine/rationale.md` > "How the doctrine evolves under evidence". A single
incident does not suffice.

The evidence is **recurrence, measured, not anecdotal**: the same failure shape
— an artifact discharging its scope by depositing follow-ups on a shared board —
occurred across **6 plans in a single review wave** (the 2026-08-04 census,
`4573c11`), producing 95 candidate items. The rolling-window trend is the
343 → 1002 line growth over thirteen days. This is a *trend across independent
artifacts*, which is exactly what the gate asks for and what a single incident
is not.

Secondary, and worth stating separately: the Maintainer raised this directly
(2026-08-04), which is also the explicit go-ahead the standing *fix defects,
build nothing new* direction requires for a new mechanism.

### Plan review tier

Proposed **`required(Internal)`**. The reasoning: the doctrine *judgment* — is
the ladder the right shape, is rung (d) gated at the right authority — is
settled here, at proposal review, not at plan review. The plan is largely
mechanical propagation across eleven named files plus one bounded retro pass.

**What escalates it to External**: if the Decision widens scope to add any
mechanical gate (a checker, a planner-verified precondition, a count guard), the
tier goes to External — a new enforcement surface is a different kind of risk
than a prose change, and item 7 deliberately declines to build one.

## Rationale

**Which workflow does it improve?** Every cold pickup. `dev/NEXT_SESSION.md`
exists to answer "what do I do next"; it is currently competing with a 1002-line
board where a release blocker and a two-assertion test guard have the same
visual weight. A board that holds only what a human must decide is readable in
one sitting.

**What contract does it clarify?** The archive precondition. Its purpose is
auditability of *disposition*; it currently delivers preservation of *everything*
and calls that the same thing. Naming the rungs separates the two.

**What correctness does it improve?** Rung (b) is the substantive one. Twelve
items currently sit on a board where their stated trigger cannot fire; moved
into code, they fire. That is a real increase in the probability the follow-up
is honoured, not just a tidier board.

**Why now?** The board grew 3× in thirteen days and Cairn is preparing a 0.4
public release. An adopter forking this methodology today inherits the ratchet
along with everything else — `templates/core/dev/PLANNING.md:100` ships it. Cairn
would be shipping a known accumulator to its first external adopter, which the
*postdoc-first* standing direction ranks above nearly everything else on the
board.

## Alternatives considered

* **Do nothing.** The board is honest debt, and honest debt is not the worst
  failure mode. Rejected on the trend: at the current rate the deferred section
  passes 1000 lines on its own before 0.4, and the census shows the rate is
  set by review *quality*, which is rising.
* **A per-artifact cap (a follow-up budget).** Cap deferrals at N per plan;
  past N the author must fix, decline, or escalate. Strong backpressure, and it
  forces prioritization directly. Rejected **for this round**: a cap prices
  deferral without saying where the overflow goes, and the ladder answers that
  question first. If the ladder proves insufficient, a cap composes on top of it
  cleanly — this is the deliberate second-wave option.
* **Mechanical expiry on board items.** An item surviving K goodnight scrubs
  unclaimed is auto-nominated for decline. Rejected for the same reason plus
  one: it deletes on a timer rather than on a judgment, and the items that
  survive longest are not obviously the least important.
* **A separate consequence floor** (a row earns the board only if it reaches an
  adopter, blocks a release, or needs a Decision). Rejected as *absorbed*, not
  wrong: a floor is exactly the argument an author makes for rung (c), so it
  needs no separate machinery. Stated in the doctrine as guidance for choosing a
  rung rather than as its own rule.
* **Approval-gate deferral without the rest of the ladder** — the narrowest
  possible change. Rejected: with declines free and deferrals costly, a rational
  author declines what should have been deferred, which is the mirror failure
  and strictly less visible than today's. The ladder's recorded-decline rung is
  what keeps the gradient flat.

**Maintainer preference during drafting.** The approval gate is the Maintainer's
own addition, given in chat 2026-08-04: *"the goal of each proposal is to CLOSE
an issue, not to OPEN a new one. Items should only be deferred if explicitly
approved, and justified with the Maintainer as being out of scope."* Rungs (a)/(b)
and the recorded-decline rung (c) were the agent's prior draft; the batching
requirement (item 3) and the successor-proposal rung (e) were added in response
to two failure modes the agent raised against the Maintainer's phrasing —
Maintainer overload, and the free-decline gradient. Per `doctrine/lifecycle.md` >
"Chat preferences are not a lifecycle Decision", this shapes the draft and is not
itself the Decision.

## Evidence / verification plan

**Tests.** **N/A for the doctrine and template prose** — Cairn's suite is
behavioral and there is no test that asserts the content of a doctrine sentence.
Two nodes *are* implicated and must be run rather than reasoned about:

* [`bootstrap/tests/test_lifecycle_contract.py`](../../bootstrap/tests/test_lifecycle_contract.py)
  — pins the plan state machine that item 5 amends. If it asserts the
  `review → archived` precondition text, it is a required edit; if it asserts
  only structure, it is untouched. **Unknown at proposal time — determined by
  running it, not by reading it.**
* [`bootstrap/tests/test_loop_fidelity_gate.py`](../../bootstrap/tests/test_loop_fidelity_gate.py)
  — the loop-fidelity surface the doctrine↔template mirror rides on.

**Examples / smoke checks.**
* `python scripts/check_cairn.py` — the prose-integrity gate; the doc smoke for
  every file in this change.
* `python -m pytest bootstrap/tests` under the canonical interpreter (Python
  3.13.x) — the full suite, because item 7 edits a shipped `templates/skills/`
  module.
* `python bootstrap/scaffold.py --summary --config <profile>` — proves the
  template edits still install.

**Docs delivered.** The doctrine sections themselves (items 1, 4, 5) and their
template mirrors (item 6); no new document is created.

### Author-accounting — invariants, failure modes, edge cases

* **Invariants.**
  1. *No follow-up is silently dropped.* **Enforcer:** the `Dispositions:` block
     in the archive commit body — a documentary requirement a reviewer checks,
     **not** a mechanical gate. This is the same enforcement strength the current
     `Follow-ups migrated to:` block has; the change does not weaken it, and does
     not strengthen it either.
  2. *Rung (d) is never taken without a Maintainer quote.* **Enforcer:** the
     archive/plan-review reviewer, reusing the Decision-scribing attestation
     form. Also unenforced mechanically.
  3. *The doctrine and its `templates/core/` mirror agree.* **Enforcer:** the
     loop-fidelity lens plus `bootstrap/fidelity-check.md`.
* **Failure modes.**
  * *Maintainer unavailable at the serialization point* — **fail-open by
    design**: the author records the rung-(d) candidates as pending and the plan
    does not archive. Archive blocks; work does not. Intentional.
  * *Author routes to (c) what should have been (d)* — **fail-open, and this is
    the change's principal risk.** Nothing mechanical catches an over-eager
    decline; the recorded reason is what makes it reviewable. Named in *Signals*
    below.
  * *Author routes to (b) and writes no code* — **fail-closed at code review**,
    because rung (b) names a file and a reviewer opens it.
* **Edge-case inventory.**
  * *Zero follow-ups* — the `Dispositions:` block is omitted; unchanged from
    today's behavior.
  * *An artifact whose entire purpose is to open successor work* (a scoping or
    census proposal) — legitimately net-positive on the board. The ≤ 0 target is
    a reading heuristic, not a gate, precisely so this case needs no exemption.
  * *A follow-up belonging to a **different** artifact's scope* — routes to (e),
    not (d).
  * *Retro pass on all 59* — in scope, chunked, and explicitly not deferrable.
  * *An adopter with no Maintainer role distinct from the author* (solo profile)
    — rung (d) collapses to a self-authorization. **Handled by stating it**: in a
    solo profile the gate is a written justification to oneself, which is weaker
    but not vacuous. A reviewer should challenge whether that is honest enough.
* **Public-path → test mapping.** The change adds **no public code path**. The
  one code edit (item 7) is two message strings inside
  `templates/skills/_lib/lifecycle_planner.py`, reached through the existing
  `session-start` / planner path and covered today by
  [`bootstrap/tests/test_lifecycle_cli.py`](../../bootstrap/tests/test_lifecycle_cli.py).
  If any node asserts those strings verbatim, it is edited with them.
* **Known omissions / intentionally untested edges.**
  * **The ≤ 0 target has no checker and is not proposed to get one** — stated in
    the *governing principle* section for exactly this reason.
  * **Invariants 1 and 2 are documentary.** This proposal adds a *rule*, not an
    *enforcement surface*. That is a real limitation and the honest framing of
    what it delivers: it changes the default, not the physics.
  * **No measurement of how the 59 actually route.** The (b)/(c)/(d) split above
    is an estimate from a keyword pass, not a per-item adjudication. The retro
    chunk produces the real figure; the estimate must not be carried forward as
    if it were measured.

## Signals the change is wrong

* **Declines get rubber-stamped.** If archive commit bodies start carrying
  rung-(c) reasons that are uniform, thin, or template-shaped, the ladder has
  become a box-tick and we have traded visible debt for invisible debt — the
  strictly worse trade. **Recovery:** require rung (c) to name the finding's
  *consequence if never fixed*, which a template cannot fake, or escalate (c) to
  require Maintainer sign-off like (d).
* **Findings stop being raised at all.** If review finding-density drops after
  this lands, the gate has leaked backwards into the review itself — the failure
  `doctrine/dual-review.md:256` already names for a different cause.
  **Recovery:** revert the lens-#9 amendment (item 4) first, keeping the archive
  rungs; the two are separable.
* **The Maintainer becomes the bottleneck.** If rung-(d) batches routinely stall
  archives, item 3's batching is insufficient. **Recovery:** a default-defer
  timeout, or delegate rung (d) to the plan reviewer for items below a stated
  consequence floor.
* **The board stops shrinking anyway.** If `dev/PLANNING.md` is still growing
  30 days after the retro pass, the ratchet was not where this proposal says it
  is. **Recovery:** revisit the per-artifact cap, which this proposal deferred to
  a second wave — and note the irony on the record.

## Internal Review -- Claude (fresh session) -- 2026-08-04

**Model**: claude-opus-5
**Reviewed at**: `9201ea3` (proposal open); tree at `894e90d`
**Interpreter for every figure below**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13), the canonical interpreter

### Steelman

The diagnosis is correct and it is the good kind of correct: it names a
*composition* failure rather than blaming any one rule. Lens #9, the scope
fence, and the archive precondition are each defensible in isolation; the
observation that they chain into `review -> finding -> outside the fence ->
deferred -> must be homed -> board` with no discarding step is a genuine
structural insight, and I could not find a counterexample to the chain. The
supporting measurements mostly hold: I independently re-derived **59 items**
and **430 lines** in `dev/PLANNING.md` > `### Deferred follow-ups (durable
home)` (lines 500-929), **42.9%** of the 1002-line file, **3** entries under
`## Active`, **10** items matching `/adopter/i`, and **30** items matching a
revival-condition/trigger pattern -- every one of those matches the proposal.

**Rung (b) is the real contribution.** "The board row is a strictly *worse*
trigger: it fires only if a human re-reads 1002 lines during a scrub" is the
sharpest sentence in the document, and it is the same argument the repo applies
to gates elsewhere. Moving a mechanically-triggered follow-up to the site where
its trigger fires is a real increase in the probability it is honoured, and
nothing in the current doctrine offers that route.

The self-accounting is also unusually honest by the standard of this tree:
item 7 explicitly refuses to claim the planner gate verifies anything (it does
not -- `templates/skills/_lib/lifecycle_planner.py:878` is literally
`gates.append((True,`, confirmed); the governing principle explicitly refuses
to become a gate; *Known omissions* concedes the (b)/(c)/(d) split is a keyword
estimate. Three of my findings below are about places where that honesty
lapses, which is a compliment to the other twenty pages.

Two smaller things that are right and worth keeping on the record: the
`Dispositions:` block is a strictly better artifact than `Follow-ups migrated
to:` for the same cost, and the *Signals* section's "declines get
rubber-stamped -- we have traded visible debt for invisible debt, the strictly
worse trade" correctly identifies the change's own worst outcome.

---

### [I1] Invariant 3's named enforcer does not enforce invariant 3 -- measured

*Author-accounting > Invariants > 3* states: "*The doctrine and its
`templates/core/` mirror agree.* **Enforcer:** the loop-fidelity lens plus
`bootstrap/fidelity-check.md`." Invariants 1 and 2 are correctly marked
"not a mechanical gate"; invariant 3 is not so marked, so it reads as the one
invariant with a real enforcer.

I ran the deletion test. I edited `templates/core/dev/PLANNING.md:100-101` so
the mirror reads *"every explicitly-deferred follow-up it carries **may be
silently discarded with no record**"* -- a flat contradiction of
`doctrine/lifecycle.md:407-408`. Results:

* `python scripts/check_cairn.py` -> **rc=0**, "196 Markdown file(s) scanned;
  no issues".
* `python -m pytest bootstrap/tests` -> **1916 passed**, 163.40s. Zero
  failures.

`bootstrap/tests/test_loop_fidelity_gate.py` (117 lines, all of it) checks a
different property entirely: whether a file under `templates/` carries a
*dangling reference into `doctrine/`* (`test_backticked_doctrine_ref_flags`,
`test_markdown_link_target_flags`, `test_check_cairn_exits_nonzero_on_dangling_ref`).
It says nothing about whether mirrored prose agrees. `bootstrap/fidelity-check.md`
answers "is what was installed what the profile said should be installed" -- a
manifest question, not a content question -- and at `:29` it explicitly exempts
`dev/PLANNING.md` from integrity checking as living state.

This is the `gate-claims-vs-enforcement` pattern, in the author-accounting of a
proposal whose own item 7 models the correct discipline one page earlier.

**Satisfier** -- either (a) mark invariant 3 documentary like 1 and 2, naming
the actual enforcer ("a reviewer opening both files at plan review"), or (b)
add a plan chunk for a real content-parity check over the named doctrine ->
template pairs, in the shape
`test_notice_install.py::test_every_self_hosted_twin_stays_byte_identical_to_its_source` (in `bootstrap/tests/`)
already uses for `.py` twins. (b) also promotes the plan-review tier to
External per the proposal's own escalation rule, so (a) is the cheaper close.

### [I2] "No doctrine anywhere describes declining a follow-up" is false; rung (c) collides with the existing `wontfix` grammar

The mechanism section rests on: "No step in that chain discards, and **no
doctrine anywhere describes *declining* a follow-up**." Cairn already has a
disposition grammar with an explicit non-action token:

* `doctrine/proposals.md:450-458` -- the canonical code-review-Response
  grammar: `accept (merged at <sha>)` / `accept (rewrote inline)` /
  `accept (followup commit <sha>)` / `reject` / `defer` -- "to a follow-up plan
  / proposal" -- / **`wontfix` -- "explicit non-action with rationale."**
* `doctrine/plans.md:492` (`* **[N4] wontfix** -- <rationale>` in the
  Sharpening template) and `doctrine/plans.md:543`
  ("`accept (commit <sha>)` / `defer` / `wontfix` dispositions").
* `doctrine/consolidation-review.md:98` extends the same token.
* And decisively: **the sentence item 4 amends already names it.**
  `doctrine/dual-review.md:246` reads "doc / scope-cut / explicit `wontfix`
  that would close it."

It is also already mechanized, which the proposal does not mention:
`templates/modules/default-on/_lifecycle_metrics/subsystems.py:87-127` defines
`_DISPOSITION_BUCKETS = ('accept', 'accept_with_modification', 'reject',
'defer', 'wontfix')` and normalizes tokens into them for the lifecycle-metrics
report.

So four of the five rungs are renamings: (a) ~ `accept`, (c) ~ `wontfix`,
(d) ~ `defer`, (e) ~ `defer` (whose existing gloss is literally "to a follow-up
plan / proposal"). Only (b) is new. This is a second vocabulary for one act, in
the tree whose doc-governance rule is that each rule has one canonical home --
and `_normalize_disposition_token` **returns `''` for an unrecognized token and
the caller drops it**, so a record written in rung vocabulary is silently
invisible to the metrics tool.

**Satisfier** -- map the rungs onto the existing tokens explicitly and amend the
grammar in place (a=`accept`, b=new token, c=`wontfix`, d=`defer` (board),
e=`defer` (successor proposal)), **or** state on the record why a parallel
vocabulary is right and add
`templates/modules/default-on/_lifecycle_metrics/subsystems.py` (plus its
`tools/_lifecycle_metrics/` twin) to `Touches`. Either way the Context
sentence needs correcting: the drain exists, it is called `wontfix`, and the
real defect is that it is available at code-review-Response time and not at
archive time. That is a *smaller and more defensible* claim than the one the
proposal makes, and it survives this finding intact.

### [I3] Rung (b) admits a call-site comment, which does not fire -- the exact defect it is introduced to cure

Rung (b) is defined as "a test, assertion, guard, **or call-site comment** that
*fires* when the trigger condition is met", approval **none**.

A call-site comment does not fire. `# NOTE: revisit X when scan_targets()
changes` is a board row relocated into a file that fewer people read than the
board. The proposal's entire case against board rows -- "it fires only if a
human re-reads 1002 lines during a scrub" -- applies verbatim to a comment: it
fires only if a human reads that function. So rung (b) contains both the
strongest artifact on the ladder (a test node) and an artifact strictly weaker
than the board row it replaces, under one approval-free label.

Because (b) sits above (c)/(d)/(e) in the ordering rule and costs nothing, it
is the cheapest exit on the ladder, and the ordering rule *requires* an author
to argue past it before reaching a rung that costs anything. The declared
failure mode -- "*Author routes to (b) and writes no code* -- **fail-closed at
code review**, because rung (b) names a file and a reviewer opens it" -- does
not cover this: the author *did* write something, the reviewer *does* find it,
and it still never fires. Applying the review brief's own test: **no test fails
when a rung-(b) comment is deleted, and none fails when it is never honoured.**

**Satisfier** -- restrict rung (b) to artifacts that execute (a test node, an
assertion, a guard) and require the routing to name the node, so "which test
fails if this is never done" has an answer; move "call-site comment" to rung
(c), where the recorded reason at least makes it reviewable. One sentence in
the ladder table closes it, and it makes the proposal's strongest claim
("moved into code, they fire") true rather than aspirational.

### [I4] The "+16 per plan" figure is computed from the wrong population; the cited source says ~4.7

*The governing principle, stated so it is falsifiable* defines the measurable
form as "a **net effect on the board of <= 0**", then states: "`as_of
2026-08-04` the six-plan census puts the current figure at roughly **+16 per
plan**."

The cited source is `dev/PLANNING.md:712-715`, which reads: "**95 candidate
items, 29 already homed, 38 judged fenced residuals rather than follow-ups, and
the 28 below with no durable home at all.**" The census's net effect *on the
board* was **28 rows across 6 plans = 4.67 per plan**. 95/6 = 15.83 is the
*candidate* rate; 67 of the 95 never became board rows. The proposal's headline
figure for its own governing metric is **3.4x** the value its own source
reports for that metric.

The Context table row is correctly labelled "95 **candidate** follow-ups"; the
governing-principle sentence drops the qualifier and re-labels it as the board
figure. That matters because 4.67 is a much easier target to bring to <= 0, and
the difference between "16 per plan" and "under 5 per plan" is the difference
between a crisis framing and a tractable one -- which bears directly on whether
the full five-rung ladder is proportionate (see the verdict).

**Satisfier** -- restate as "roughly +4.7 net board rows per plan (28/6), from
95 candidates, `as_of 2026-08-04`", and re-run the proportionality argument
against the corrected figure.

### [I5] The thirteen-day "trend" and the six-plan census are the same event, counted twice against the rate-limit gate

*Doctrine-change rate-limit* offers two evidence lines: the census across 6
plans, and "the rolling-window trend is the 343 -> 1002 line growth over
thirteen days", concluding "This is a *trend across independent artifacts*,
which is exactly what the gate asks for and what a single incident is not."

Re-derived (`git show <sha>:dev/PLANNING.md | wc -l`, last commit of each day
that touched the file):

| date | end-of-day lines |
|---|---|
| 2026-06-12 | 333 |
| 2026-07-13 | 336 |
| 2026-07-14 | 344 |
| 2026-07-22 | 344 |
| 2026-07-31 | 404 |
| 2026-08-03 | 675 |
| 2026-08-04 | **1002** |

Two problems.

**(a) The 343 label is wrong.** The proposal's table row reads
"`dev/PLANNING.md`, **earliest commit on 2026-07-22** | **343 lines**". The
five commits touching the file that day, oldest first: `57d1daf` 08:41 -> 349;
`82d24bc` 10:38 -> 344; `1ebafb1` 10:46 -> 350; `cc66d2b` 12:25 -> **343**;
`c9dc569` 13:32 -> 344. The earliest is **349**, the day closed at **344**, and
343 is the day's *minimum*, fourth of five. The ratio survives (1002/349 =
2.87x, still "tripled"); the label does not.

**(b) The trend is the census.** Of the +658 lines from 2026-07-22 to
2026-08-04, **+598 (91%)** landed in the last four days and **+327 (50%)** on
2026-08-04 alone, in `4573c11` -- which is the census commit the proposal cites
as its *other* evidence line. So the rate-limit gate is being shown one
phenomenon described two ways, not "a trend across independent artifacts" plus
a recurrence.

I do not think this sinks the gate clearance: the census genuinely spans six
independently-authored plans, and that alone is recurrence rather than a single
incident. But the proposal must not claim two independent evidence lines when
it has one, in a section whose entire purpose is to prove the evidence bar was
met.

**Satisfier** -- correct the table label (use 349 with "earliest", or 344 with
"end of day", and say which), and either drop the line-growth trend as
independent evidence or replace it with a genuinely independent series --
deferred-item count per archived artifact over the last N archives is
computable from the tree today and is the right shape.

### [I6] The enumeration is incomplete: at least four more surfaces carry the rule

*Documentation / doctrine surface* asserts "the eleven files are enumerated in
`Touches` above and itemized in items 1-7." A sweep for the archive-precondition
prose and the lens-#9 text across `doctrine/`, `templates/`, `dev/`,
`bootstrap/`, `tools/` and the shipped skills finds four more:

1. **`tools/lifecycle_planner.py:879` and `:1024`** -- a byte-identical twin of
   `templates/skills/_lib/lifecycle_planner.py` (same git blob `afa702d`),
   installed by the mapping at `bootstrap/_scaffold/config.py:564`, and the
   copy **Cairn itself runs** (`.agents/skills/session-start/SKILL.md:19`
   invokes `python tools/lifecycle.py`). This one *is* caught --
   `test_notice_install.py::test_every_self_hosted_twin_stays_byte_identical_to_its_source` (in `bootstrap/tests/`)
   fails on divergence -- but neither the file nor the test node appears in
   `Touches` or in *Public-path -> test mapping*, which names only
   `bootstrap/tests/test_lifecycle_cli.py`. I confirmed by grep that **no test
   asserts the durable-home strings at all**, so `test_lifecycle_cli.py` is not
   the coverage the mapping claims it is; the twin-parity node is.
2. **`templates/modules/team-gated/dual-review.md:69`** and
3. **`dev/modules/dual-review.md:69`** -- both quote lens #9 verbatim,
   including "explicit `wontfix`". Item 4 amends lens #9 and names only
   `doctrine/dual-review.md`. Per [I1]'s mutation result, **nothing fails** if
   these go stale.
4. **`dev/PLANNING.md:433-444`** -- Cairn's self-hosted copy of the
   archive-precondition prose, mirroring `templates/core/dev/PLANNING.md:97-108`
   and pointing at `doctrine/lifecycle.md`. `Touches` lists `dev/PLANNING.md`
   only as "(retrospective pass)", so the prose edit is unaccounted for.

Secondary, lower confidence: `templates/modules/team-gated/issue-capture.md:97`
and `dev/modules/issue-capture.md:97` require a promoted issue's closing comment
to "name the durable home" -- under the ladder, a rung-(c) decline has no
durable home to name, so that sentence needs a rung-aware phrasing or an
explicit "unaffected" note.

**Satisfier** -- extend `Touches` to at least fifteen files, and name
`test_every_self_hosted_twin_stays_byte_identical_to_its_source` in the
verification plan for item 7.

### [I7] Item 3's serialization point is upstream of where the items arise, and proposals get no ceremony at all

Item 3: "The author presents all rung-(d) candidates as a single list **at plan
review**, or at archive-preparation **if the plan is review-exempt**."

Plan review runs *before* implementation --
`doctrine/lifecycle-contract.md:134-135`: `open -> awaiting-plan-review ->
executing`, and execution does not begin until the plan-review section lands.
But the population this proposal exists to manage is discovered *after* that:
`dev/PLANNING.md:711-712` describes the census as "every deferred follow-up
named in the six plans that reached **code review** on 2026-08-04". Findings
arrive at code review and during implementation; batching them at plan review
batches a set that does not exist yet.

The fallback is conditioned on the wrong property, too: archive-preparation is
offered *only* to review-exempt plans, when the review-required plans are
precisely the ones that generate findings.

And **proposals have no plan review**. The archive precondition covers
proposals (`doctrine/proposals.md:344-355`), and a proposal archives *inside*
the plan-open commit (`doctrine/lifecycle-contract.md:133`: "the plan-open
commit creates the plan **and** archives the source proposal"). Item 3 names no
serialization point for that case, so a proposal's rung-(d) batch would have to
be authorized before a commit that is itself a lifecycle transition. This is the
lens-7 question -- *who runs this, when, at which ceremony* -- and for the
proposal half the answer is currently absent.

**Satisfier** -- name **archive-preparation** as the single serialization point
for every artifact, plan and proposal alike, with plan review as an optional
early pass for follow-ups already visible at plan time; add one sentence
covering the proposal-archives-at-plan-open case. Alternatively, scope the
ladder to plans only and say so explicitly in `Touches` (which would remove
`doctrine/proposals.md` from the change).

### [I8] The retro pass rewrites the durable home that closed artifacts point at, and archived artifacts are append-only

Item 8 re-routes all 59 rows. Six artifacts cite that section as the home
against which their archive precondition was discharged:

* `dev/plans/dependency-advisory-coverage.md:945` and `:270`
* `dev/plans/release-security-bar.md:1279` and `:103`
* `dev/plans/security-preflight-checklist.md:1086` and `:659`
* `dev/plans/default-security-stance.md:866`
* and two **already-archived** plans pointing at `dev/PLANNING.md` rows:
  `dev/plans/archive/lockfile-provenance-fields.md:407` and
  `dev/plans/archive/interpreter-trust-root-fallback.md:582`.

The second archived one is already a live instance of the hazard: it records S2
as homed "at its `dev/PLANNING.md` **Queued** row", and S2 now sits at
`dev/PLANNING.md:520`, inside `### Deferred follow-ups`. The pointer has already
drifted once, and the retro pass would move or delete it again -- this time
possibly to rung (c), at which point an archived, append-only record asserts a
migration that is no longer true and cannot be corrected in place.

The edge-case inventory covers "*Retro pass on all 59* -- in scope, chunked, and
explicitly not deferrable" and says nothing about inbound references.

**Satisfier** -- add a rule: a retro re-route of a row named by a *closed*
artifact's `Follow-ups migrated to:` block is recorded as a forwarding entry in
the retro pass's own commit body, and such rows are **not** eligible for rung
(c) without the Maintainer, because declining them retroactively changes an
archived precondition's truth value. Or scope item 8 to rows with no inbound
reference and record the remainder as explicitly out of scope. Either closes it;
silence does not.

### [I9] The ordering rule tilts toward decline -- the gradient the proposal claims the ladder flattens

*Alternatives considered* rejects the approval-gate-only option because "with
declines free and deferrals costly, a rational author declines what should have
been deferred, which is the mirror failure and strictly less visible than
today's. **The ladder's recorded-decline rung is what keeps the gradient flat.**"

It does not flatten it. Under the ladder, (c) *decline* still costs nothing
("none, but **recorded**") while (d) *defer* costs a Maintainer round-trip --
and the ordering rule *adds* a second push in the same direction by requiring
the author to record why (c) did not take a finding before reaching (d). The
ladder makes decline both cheaper **and** ordered-first. That is a steeper
gradient than the alternative it rejects, not a flatter one.

Relatedly, (e) -- "a **genuine discovered blocker**" -- sits at the *bottom*, so
routing a real blocker to its own proposal requires first arguing why it should
not simply be declined. That ordering is backwards for the one rung reserved for
serious work.

**Satisfier** -- three options, any one closes it: (1) promote the absorbed
consequence floor from rung-choice *guidance* into a routing *rule* -- a finding
that reaches an adopter, blocks a release, or needs a Decision is **ineligible**
for (c) -- which is the mechanism the *Alternatives* section claims already
exists; (2) reorder so (e) is not below (d); (3) drop strict ordering and keep
only "record why the rung you chose is right", which is what the `Dispositions:`
block delivers anyway.

### [I10] The ladder is not total over lens #9's own satisfier list

Item 4 makes the rung the required satisfier vocabulary for lens #9. Lens #9's
current list (`doctrine/dual-review.md:245-247`) is five items: **test / guard /
doc / scope-cut / explicit `wontfix`**. Mapping them onto rungs:

* *test*, *guard* -> rung (b). Fine.
* *explicit `wontfix`* -> rung (c). Fine (modulo [I2]).
* **doc** -> no rung. Rung (b) admits "a test, assertion, guard, or call-site
  comment" -- a documentation change is none of those and does not fire. So an
  out-of-scope finding whose satisfier is a doc update falls to (c) *decline*,
  which mislabels "this needs a doc update" as "we are not doing this".
* **scope-cut** -> no rung. Narrowing the artifact's claim so the finding no
  longer applies is not a fix, not a code home, not a decline, not a defer, and
  not a successor proposal. It is arguably the *cleanest* disposition available
  and the ladder has no slot for it.

The review brief's design-completeness question -- "is there a finding class
that fits none of them" -- has two answers, and both are named in the sentence
item 4 is amending.

**Satisfier** -- one paragraph stating which rung absorbs each of lens #9's five
current satisfiers, adding a rung if the mapping is not total. A doc rung and a
scope-cut rung are the obvious candidates; declaring doc-under-(b) and
scope-cut-under-(a) with a sentence of justification would also close it. What
must not happen is item 4 landing with a five-satisfier list rewritten into a
five-rung list that is not the same five.

### [I11] "Net effect on the board <= 0" is satisfiable by an artifact that closes nothing

The governing principle is "**An artifact closes more than it opens**",
operationalized as net board rows <= 0. But four of five rungs reduce board rows
without closing work: (b) relocates it into a file, (c) declines it, (e) opens a
successor proposal -- which **increases** total outstanding work while scoring
zero, or negative if it clears existing rows. Only (a) closes anything. So the
metric is fully satisfiable by an artifact that closed nothing, using the very
ladder introduced to satisfy it.

The proposal partly defends this: the target is "a reading heuristic, not a
gate", and the edge-case inventory exempts census/scoping artifacts whose
purpose is to open successor work. But rung (e) is that same shape appearing in
*every ordinary* artifact, and it is not exempted. The principle is stated "so
it is falsifiable" -- as drawn it is falsifiable in a direction that does not
track the quantity being managed.

**Satisfier** -- either state the principle over *outstanding follow-ups* rather
than *board rows*, conceding it is unmeasurable today (which is consistent with
the section's own refusal to build a checker), or keep the board-row form and add
one sentence naming rung (e) as a known exception alongside the census case.

---

### On declining to build a mechanical gate

I take the position that **declining the gate is correct, and the way the
decline is written is not**.

Correct, because the thing being changed is a *routing judgment*. A checker
could verify that a `Dispositions:` block exists and that every listed item
names a rung -- but it could not verify that the rung is the right one, and the
failure mode the *Signals* section already fears ("declines get rubber-stamped
... uniform, thin, or template-shaped") is precisely the failure a
presence-checker would certify as passing. A gate that fires green on the exact
degenerate case is worse than no gate, which is `AGENTS.md` > "Name the trigger,
check what it checks" applied correctly. The proposal's item 7 gets this exactly
right.

Not the "stated control with no mechanism" pattern, because
`gate-claims-vs-enforcement` is about claiming a strength not delivered, not
about having no mechanism. A rule honestly labelled as a rule is fine; a rule
labelled as a gate is not. The proposal labels correctly in items 7 and 8 and in
*Known omissions*.

But it lapses in exactly one place, and that lapse is [I1]: invariant 3 carries a
named enforcer that does not enforce it, one paragraph after invariants 1 and 2
are correctly marked documentary. Fix [I1] and the position is coherent
throughout.

One thing genuinely available and not claimed: `_lifecycle_metrics` already
buckets `wontfix` ([I2]). If the rungs are expressed in that grammar, the
**decline rate becomes measurable for free**, which turns the first *Signals*
entry from "someone notices the prose is template-shaped" into a number on the
existing metrics report. That is not a gate, and it is a better instrument than
the one the proposal says does not exist.

---

### Covered

* **#1 Claims** -- re-derived every load-bearing figure. **Confirmed**: 59 items
  and 430 lines in `dev/PLANNING.md:500-929` (bullet parse + `wc`); 42.9% of
  1002; 3 entries under `## Active`; 10/59 matching `/adopter/i`; 30/59 matching
  a revival-condition/trigger pattern; the census's own "95 candidate / 29 homed
  / 38 fenced / 28 unhomed" at `dev/PLANNING.md:712-715`. **Citations
  confirmed**: `doctrine/dual-review.md:245` (lens #9) and `:256` (ritual
  signal); `doctrine/plans.md:249` (scope fence); `dev/plans/_template.md:111`;
  `doctrine/lifecycle.md:403` (archive precondition heading) and `:423` (removal
  preconditions); `doctrine/proposals.md:349` (`dev/PLANNING.md` first-named
  home); `doctrine/lifecycle-contract.md:137` (`review -> archived` row);
  `templates/core/dev/PLANNING.md:100`;
  `templates/skills/_lib/lifecycle_planner.py:878` = `gates.append((True,` and
  `:879`/`:1024` carry the strings. **Refuted**: the +16/plan figure ([I4]); the
  343/earliest-commit label ([I5a]); "no doctrine anywhere describes declining"
  ([I2]); "the eleven files" ([I6]).
* **#2 Production path exercised by tests** -- at proposal-review's staged bar,
  the question is whether the evidence is promised and scoped. It is, but names
  the wrong node: `grep -rn "durable home\|Follow-ups migrated" bootstrap/tests/`
  returns **zero hits**, so `bootstrap/tests/test_lifecycle_cli.py` does not
  cover the strings item 7 edits. The node that actually governs is
  `test_notice_install.py::test_every_self_hosted_twin_stays_byte_identical_to_its_source`
  ([I6.1]).
* **#3 Design completeness** -- rungs are not disjoint at (b)/(c) ([I3]), not
  total over lens #9's satisfier list ([I10]), and the ordering rule is
  mis-signed ([I9]). Edge cases stated but two missing: inbound references from
  closed artifacts ([I8]), and the proposal-archives-at-plan-open case ([I7]).
* **#4 Silent failure / fail-closed** -- mutation test: mirror text inverted to
  "may be silently discarded with no record" at
  `templates/core/dev/PLANNING.md:100-101` -> `scripts/check_cairn.py` rc=0,
  `pytest bootstrap/tests` **1916 passed**. Invariant 3 is fail-open with a
  named enforcer ([I1]). Invariants 1 and 2 are fail-open and *say so* --
  correctly framed. The "Maintainer unavailable -> archive blocks, work does
  not" disposition is genuinely fail-closed on the right axis.
* **#5 Cross-document consistency** -- swept `doctrine/`, `templates/`, `dev/`,
  `bootstrap/`, `tools/`, `.agents/skills/` for "durable home", "Follow-ups
  migrated", "wontfix", "scope-cut". Found four unenumerated surfaces ([I6]) and
  a whole pre-existing disposition grammar ([I2]). `scripts/claim_check.py` on
  the proposal: clean.
* **#6 Drift** -- the doctrine <-> `templates/core/` mirror is unguarded ([I1]);
  the `templates/skills/_lib/` <-> `tools/` twin **is** guarded, by
  `test_notice_install.py:98-109`. `git ls-files -s` confirms both planner
  copies at blob `afa702d`.
* **#7 Lifecycle / process placement** -- item 3's ceremony is upstream of the
  finding population, and proposals have none ([I7]), verified against
  `doctrine/lifecycle-contract.md:133-137` and `dev/PLANNING.md:711-712`.
* **#8 Domain validity & scope** -- rate-limit gate cleared on one phenomenon
  presented as two ([I5b]); the board-row metric does not track the managed
  quantity ([I11]); item 8 is a different kind of work from items 1-7 (see
  verdict).
* **#9 Name the satisfier** -- every finding above names one; none is a bare
  observation.

### Not covered / low confidence

* **Same-type reviewer -- no cross-type independence on this pass.** I am
  Claude reviewing a Claude-authored proposal in a fresh session. That is the
  Internal floor and nothing more.
* **I could not reproduce "12 of the 59".** My passes over the section produced
  4 items whose `*Trigger:*` field names a code-edit event, 5 under a broader
  code-or-ceremony pattern, 6 under a looser one, and 17 mentioning any `.py`
  path -- none near 12. Only **18** of the 59 carry an explicit `*Trigger:*`
  field at all. The proposal concedes in *Known omissions* that the (b)/(c)/(d)
  split is "an estimate from a keyword pass, not a per-item adjudication" -- but
  the 12 is stated flatly as measurement in *Context* ("**12 of the 59** name a
  trigger that is a code or ceremony event") and again in *Rationale* ("Twelve
  items currently sit on a board where their stated trigger cannot fire"), where
  it is the entire answer to "what correctness does it improve?". I did not
  adjudicate the 59 individually and cannot say the true figure is not 12; I can
  say I could not reach it, and that the load-bearing correctness claim rests on
  a number the proposal elsewhere disclaims. Not numbered as a finding because I
  cannot falsify it -- but the author should either re-derive it per-item or
  soften both sentences to match *Known omissions*.
* **Did not assess Maintainer load empirically.** Whether batching actually
  bounds it is an operational question no artifact in the tree answers.
* **Did not run `bootstrap/scaffold.py --summary --config <profile>`** -- the
  proposal's third smoke check. No template file changed on this pass, so there
  was nothing to prove installs; it remains unexercised evidence.
* **Did not evaluate the solo-profile collapse of rung (d)** beyond reading the
  proposal's own handling of it. The proposal explicitly invites a reviewer to
  challenge whether self-authorization is "honest enough"; I have no independent
  basis to judge it and am leaving it open rather than rubber-stamping it.
* **The negative-existence claim** ("no item in `dev/` or `doctrine/` tracks
  this as a problem") I re-ran with a broader pattern and found no
  counterexample -- but such claims are phrasing-sensitive. Worth noting a near
  precedent the proposal does not cite: `dev/plans/transition-lint.md:203` and
  `dev/proposals/2026-07-22-claude-transition-lint.md:910` route "entries
  accumulate past a handful" to *retiring the tool, not growing the list* --
  structurally the same governing move, and a useful supporting citation.
  (I checked whether that rule reached `docs/tool-usage.md`, which the
  `transition-lint` plan's row F2 proposed; `grep -n whitelist
  docs/tool-usage.md` returns nothing, so it lives only in the deliberation
  record. Flagging that as an observation, not a finding of this proposal.)

### Second-round recommendation

**Recommended -- an External (different-agent-type) round before the Decision.**
Grounded in the negative space above, not in blast radius:

1. My pass is same-type, and the proposal's core is an *incentive-design*
   argument ([I9]: does a recorded-decline rung flatten or steepen the
   gradient?). That is exactly the class where a different prior sees first, and
   where a same-architecture reviewer is most likely to share the author's
   reasoning.
2. [I2] is the kind of miss that suggests more of its kind. Neither the author
   nor I noticed the existing `wontfix` grammar until a targeted sweep; a
   reviewer who does not share our search habits may find further collisions.
3. The change alters the archive precondition -- a contract fifteen-plus
   surfaces and one shipped code path depend on -- and per [I1] essentially
   nothing mechanical protects it. Prose-only contracts are where a second read
   is cheapest relative to what it protects.

Against: if the Decision adopts [I2]'s "map onto the existing grammar" satisfier
and cuts item 8 (below), the residual change becomes a small, well-fenced
amendment and an Internal-only round is defensible.

Note the proposal's own escalation rule already fires here: satisfying [I1] via
route (b) adds a mechanical gate, which the *Plan review tier* section says
"goes to External".

### Verdict

**REVISE.**

Not SPLIT, narrowly. Items 1-7 are one coherent change: doctrine plus its
template mirrors plus two strings in the shipped planner, held together by
loop-fidelity -- splitting them would *create* the drift the repo guards
against. But **item 8 should be cut from this proposal** and carried as its own
artifact. It is a different kind of work (a 59-item per-item adjudication,
Maintainer-blocking at unknown batch size, with the archived-pointer hazard of
[I8]), its routing estimate is unmeasured by the proposal's own admission, and
`identity-not-name` (`dev/proposals/2026-08-03-claude-identity-not-name.md:344`,
"**Verdict: REVISE / SPLIT**") is the standing precedent for exactly this
bundling shape. The proposal's argument that item 8 must stay -- "deferring the
fix for deferrals would be self-refuting" -- is rhetorically strong but does not
survive contact: *sequencing* the retro pass as a named successor with a
committed trigger is rung (e), which is the proposal's own answer to this exact
situation. Applying its own ladder to itself is the opposite of self-refuting.

REVISE rather than HOLD because the diagnosis holds, rung (b) is a real
contribution, and every finding above has a satisfier that is prose or a scope
cut -- none requires new machinery. The blocking set before Decision is
**[I1]** (an enforcer claim this repo has recorded six times in one week),
**[I2]** (a parallel vocabulary over an existing mechanized grammar), **[I3]**
(the substantive rung's escape hatch), and **[I4]** (a 3.4x error in the
headline metric). [I5]-[I11] are corrections and additions that a Response can
carry without re-opening the design.

---

## Response -- Claude (Strategy) -- 2026-08-04

**Model**: claude-opus-5

Grammar: Proposal-Response (`doctrine/proposals.md:433-444`) -- no implementing
commit exists.

The review is accepted essentially in full. Four findings are author errors
rather than design disagreements, and three of those four ([I4], [I5a], and the
unnumbered "12 of the 59") biased toward the proposal's own conclusion, which is
the shape that most deserved catching.

**[I1]** accept -- taking satisfier route (a), the cheaper close. Invariant 3 is
re-marked documentary with its real enforcer named ("a reviewer opening both
files at archive-preparation"). Route (b) would add a content-parity gate and
fire the proposal's own External-escalation rule; it is recorded as a candidate
successor, not taken here. The finding is correct and is the sixth instance of
this exact shape in a week -- a named enforcer that does not enforce, asserted
one paragraph after two others were correctly marked documentary.

**[I2]** accept -- and it restructures the proposal. Verified independently:
`doctrine/proposals.md:458` (`wontfix` -- explicit non-action with rationale),
`doctrine/plans.md:492` and `:543`, `doctrine/dual-review.md:246`, and the
mechanization at `templates/modules/default-on/_lifecycle_metrics/subsystems.py`
(`wontfix` bucketed at `:93`, normalized at `:125-126`). The Context claim "no
doctrine anywhere describes declining a follow-up" is **false and is retracted**.
The reviewer's reframing is adopted verbatim as the proposal's new spine: *the
drain exists, it is called `wontfix`, and the real defect is that it is available
at code-review-Response time and not at archive time.* Four of five rungs collapse
into existing tokens; only the code-home rung is new. This makes the change
substantially smaller and removes the parallel-vocabulary hazard, including the
silent-drop behaviour of `_normalize_disposition_token`.

**[I3]** accept -- rung (b), now the `guard` token, is restricted to artifacts
that **execute** (a test node, an assertion, a runtime guard) and must **name the
node**. "Call-site comment" is removed from it and routed to `wontfix`, where the
recorded reason makes it reviewable. The finding is right that the cheapest,
approval-free, ordered-first rung admitted the exact artifact the proposal
condemns.

**[I4]** accept -- corrected to **+4.67 net board rows per plan** (28/6), from 95
candidates, `as_of 2026-08-04`. Re-verified against `dev/PLANNING.md:712-716`.
The 3.4x error was in the proposal's own governing metric, and the corrected
figure materially changes the framing: this is tractable, not a crisis. The
proportionality argument is re-run against it below and is part of why the
revision is smaller.

**[I5]** accept -- (a) the table row is corrected: the earliest 2026-07-22 commit
is `57d1daf` at **349** lines; 343 was the day's fourth-of-five intra-day
minimum, selected by an author `sort -u` that destroyed chronological order.
Re-derived independently and the reviewer's table matches. (b) The line-growth
trend is **dropped as an independent evidence line** rather than restated -- 91%
of it landed in the census's own four-day window and 50% in `4573c11` itself, so
it is one phenomenon described twice. The gate now rests solely on the census's
six independently-authored plans, which is recurrence on its own.

**[I6]** accept -- `Touches` extended to fifteen surfaces:
`tools/lifecycle_planner.py` (byte-identical twin at blob `afa702d`, confirmed by
`cmp`; the copy Cairn actually runs), `templates/modules/team-gated/dual-review.md:69`,
`dev/modules/dual-review.md:69`, and `dev/PLANNING.md:433-444` (the self-hosted
prose, distinct from the retro pass). The public-path -> test mapping is
corrected: `grep` over `bootstrap/tests/` for the durable-home strings returns
**zero** hits, so `test_lifecycle_cli.py` was never the coverage claimed. The
governing node is
[`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
`::test_every_self_hosted_twin_stays_byte_identical_to_its_source`, confirmed
present at `:98`. The `issue-capture.md` pair is handled by the new
`Dispositions:` phrasing, which no longer assumes every follow-up has a durable
home.

**[I7]** accept -- **archive-preparation** becomes the single serialization point
for every artifact, plan and proposal alike, with plan review as an optional
early pass for follow-ups already visible then. The proposal-archives-inside-the-
plan-open-commit case (`doctrine/lifecycle-contract.md:133`) is covered
explicitly. The finding is correct that batching at plan review batches a
population that does not exist yet -- the census itself describes findings that
arrived at *code* review.

**[I8]** accept -- both halves. A retro re-route of a row named by a **closed**
artifact's migration block is recorded as a forwarding entry, and such rows are
**ineligible for `wontfix` without the Maintainer**, because declining them
retroactively changes an archived precondition's truth value in a record that is
append-only and cannot be corrected in place. The already-drifted pointer at
`dev/plans/archive/interpreter-trust-root-fallback.md:582` is cited in the
successor as a worked instance. This rule travels with the retro pass into its
own artifact (see the split below).

**[I9]** accept -- taking satisfiers (1) and (3) together. The absorbed
consequence floor is promoted from rung-choice *guidance* into a routing
**rule**: a follow-up that reaches an adopter, blocks a release, or needs a
Decision is **ineligible for `wontfix`**. And strict ordering is **dropped** --
what remains is "record why the disposition you chose is right", which the
`Dispositions:` block already delivers. That removes the second push toward
decline and the backwards placement of the successor-proposal disposition in one
move. The finding is correct that the original ladder made decline both cheaper
*and* ordered-first, which is a steeper gradient than the alternative it rejected
-- the *Alternatives* section claimed the opposite and was wrong.

**[I10]** accept -- the mapping over lens #9's five satisfiers is stated
explicitly and is total: *test* -> `guard`; *guard* -> `guard`; *doc* ->
`accept` (writing the doc is the fix, performed in scope); *scope-cut* ->
`accept` (narrowing the artifact's claim is an in-scope edit to the artifact);
*wontfix* -> `wontfix`. Adopting the existing grammar per [I2] is what makes this
mapping natural rather than forced -- four of the five satisfiers already share
its vocabulary.

**[I11]** accept with modification -- the principle is restated over
**outstanding follow-ups**, not board rows, and the concession that this is
unmeasurable today is made explicit rather than implied. The reviewer's
alternative (keep the board-row form, exempt the successor case) is declined
because it preserves a metric that does not track the managed quantity; naming it
unmeasurable is more honest than a measurable proxy pointing the wrong way. The
"An artifact closes more than it opens" slogan is kept as a *statement of intent*
with its non-measurability stated in the same breath.

**Unnumbered observation -- "12 of the 59"** accept. The reviewer could not
reproduce it under four patterns (4 / 5 / 6 / 17) and established that only 18 of
59 carry an explicit `*Trigger:*` field at all. The figure came from an author
regex over phrasings, not a per-item adjudication, and was stated flatly as
measurement in *Context* and *Rationale* while *Known omissions* disclaimed the
same estimate two pages later. **The number is withdrawn.** Both sentences are
softened to name the code-home route as the contribution without asserting a
count; the true figure is produced by the retro pass's per-item adjudication,
which is where it belongs.

**Unnumbered observation -- the `transition-lint` precedent** accept, with
thanks. `dev/proposals/2026-07-22-claude-transition-lint.md:910` routing "entries
accumulate past a handful" to *retiring the tool, not growing the list* is
structurally the same governing move and is now cited in *Rationale* as prior
art. It strengthens the rate-limit case with a genuinely independent instance,
which is what [I5b] removed.

**Verdict disposition -- item 8 (the retro pass) is SPLIT OUT.** accept. The
reviewer's argument defeats the proposal's own: *sequencing* the retro pass as a
named successor with a committed trigger **is** the successor-proposal
disposition, so applying the ladder to itself is the opposite of self-refuting.
The precedent (`identity-not-name`, REVISE/SPLIT) is on point.

**The split is conditioned, and the condition is not negotiable within this
proposal:** the successor is opened in the **same session** as this proposal's
Decision, not "when it reaches the top of the board". A retro pass that becomes a
board row would be this proposal's own thesis failing on its first test. If the
Maintainer does not want it opened today, the correct outcome is to reject the
split and keep item 8 in scope -- not to accept the split and let the successor
float.

**Second round** defer -- to the Maintainer's Decision. The reviewer recommends
External and names the condition under which Internal suffices ("if the Decision
adopts [I2]'s map-onto-the-existing-grammar satisfier and cuts item 8, the
residual change becomes a small, well-fenced amendment"). **Both** of those are
now adopted, so that condition is met on the record. The author does not get to
rule on the tier for its own proposal; the facts are stated and the call is the
Maintainer's.

---

## Revised proposal

**Status**: revised

The spine changes. Cairn already has a disposition grammar with an explicit
non-action token; this proposal no longer invents a parallel one. What it does is
**make that grammar available where the accumulation actually happens** and add
the one disposition the grammar is missing.

### The defect, restated correctly

`doctrine/proposals.md:450-458` defines the code-review-Response grammar:
`accept` / `reject` / `defer` / `wontfix` ("explicit non-action with rationale").
It is mechanized -- `_lifecycle_metrics/subsystems.py:87-127` buckets all five
tokens for the metrics report.

That grammar governs **responses to review findings**. It does **not** govern the
**archive precondition**, which instead requires (`doctrine/lifecycle.md:403`)
that every explicitly-deferred follow-up have "a durable home outside the file",
first-naming `dev/PLANNING.md`. So at the one moment an artifact disposes of
everything it did not do, the only sanctioned outcome is *preservation*. There is
a drain in the tree; it is not plumbed to the sink.

### The change

**C1 -- The archive precondition accepts a disposition, not only a home.**
`doctrine/lifecycle.md` > "Archive precondition" is amended so the precondition is
satisfied when every explicitly-deferred follow-up carries a **recorded
disposition token from the existing grammar**. `wontfix` with a rationale
satisfies it. The `Follow-ups migrated to: …` block becomes **`Dispositions: …`**,
naming the token for every item. Auditability is unchanged: a cold reader can
still reconstruct that nothing vanished, and can now also see what was declined
and why -- which the current block cannot express at all.

**C2 -- One new token: `guard`.** For a follow-up whose home is an artifact that
**executes** -- a test node, an assertion, a runtime guard. It **must name the
node** (`path::node`). This is the proposal's substantive contribution and the
only new vocabulary. Its case is unchanged from the original draft and no finding
challenged it: a follow-up whose revival condition is "any edit to
`scan_targets()`" belongs at `scan_targets()`, where the condition fires, not on
a board that fires only when a human re-reads it. Per [I3], a comment is **not**
an eligible `guard` artifact -- comments do not fire.

**C3 -- `defer` at archive time requires a quoted Maintainer authorization,** in
the existing Decision-scribing attestation form (`AGENTS.md` > "Scribing a
Decision"): the authorizing phrase quoted verbatim and visually isolated. Scope is
Maintainer-held; a deposit on a shared board is a scope decision.

**C4 -- Eligibility rules, replacing the ordering rule.** There is **no** required
order. What is required is that the `Dispositions:` block record why the chosen
token is right. Two eligibility constraints bound it:

* A follow-up that **reaches an adopter, blocks a release, or needs a Decision**
  is **ineligible for `wontfix`**. (The consequence floor, promoted from guidance
  to rule per [I9].)
* A follow-up **named by a closed artifact's migration block** is ineligible for
  `wontfix` without the Maintainer, and any re-route of it is recorded as a
  forwarding entry. (Per [I8] -- an archived record is append-only and cannot be
  corrected in place when the migration it asserts stops being true.)

**C5 -- Archive-preparation is the single serialization point**, for plans and
proposals alike. Plan review may take an optional early pass at follow-ups
already visible then. A proposal that archives inside its plan-open commit
(`doctrine/lifecycle-contract.md:133`) presents its block at that commit's
preparation.

**C6 -- Lens #9 keeps its five satisfiers and gains the mapping.**
`doctrine/dual-review.md:245-247` is amended only to state which disposition each
satisfier lands in: *test* -> `guard`, *guard* -> `guard`, *doc* -> `accept`,
*scope-cut* -> `accept`, *wontfix* -> `wontfix`. Total, by construction, because
four of the five already share the grammar's vocabulary. Lens #9's promotion
function is untouched -- reviewers keep finding things.

**C7 -- The fifteen surfaces carry it.** `doctrine/lifecycle.md` (canonical),
`doctrine/proposals.md`, `doctrine/plans.md`, `doctrine/dual-review.md`,
`doctrine/lifecycle-contract.md:137`; `templates/core/dev/PLANNING.md`,
`templates/core/dev/plans/_template.md`, `templates/core/dev/proposals/_template.md`,
`templates/modules/team-gated/dual-review.md:69`; `dev/PLANNING.md:433-444`,
`dev/plans/_template.md`, `dev/proposals/_template.md`, `dev/modules/dual-review.md:69`;
and the planner string pair in **both** `templates/skills/_lib/lifecycle_planner.py`
(`:879`, `:1024`) and its byte-identical twin `tools/lifecycle_planner.py`. The
planner strings stay **unconditional reminders** -- `:878` is literally
`gates.append((True,` -- and are re-worded, not promoted to checks.

### What is no longer in this proposal

**The 59-item retrospective pass is split out** to its own artifact, opened in the
same session as this proposal's Decision (see the Response). It carries [I8]'s
forwarding rule with it. Rationale: it is a per-item adjudication of unknown batch
size against a Maintainer, over rows that six artifacts -- two of them archived and
append-only -- cite as their discharged home. That is a different kind of work from
a prose amendment, and `identity-not-name` is the standing precedent for not
bundling them.

### Corrected figures

All `as_of 2026-08-04`, HEAD `4573c11`, canonical interpreter:

| Measure | Value |
|---|---|
| `dev/PLANNING.md`, **earliest** commit on 2026-07-22 (`57d1daf`, 08:41) | **349 lines** |
| `dev/PLANNING.md` at HEAD | **1002 lines** (2.87x) |
| `### Deferred follow-ups (durable home)` | **430 lines, 59 items** -- 42.9% of the file |
| Items under `## Active` | **3** |
| Six-plan census: candidates | **95** (29 already homed, 38 fenced residuals) |
| Six-plan census: **net new board rows** | **28 across 6 plans = +4.67 per plan** |

**Withdrawn:** the "12 of the 59" figure, and the 343-line baseline. **Dropped as
independent evidence:** the thirteen-day line-growth trend.

### Rate-limit gate, re-argued on the corrected evidence

The gate (`doctrine/rationale.md:313`) asks for recurrence, not a single incident.
What remains after [I5b] is the census alone -- and it suffices: the same failure
shape occurred across **six independently-authored plans** in one wave, producing
28 net board deposits. Six artifacts is recurrence.

Independent supporting instance, per the reviewer: `dev/proposals/2026-07-22-claude-transition-lint.md:910`
already routes "entries accumulate past a handful" to *retiring the tool, not
growing the list* -- the same governing move reached independently in a different
scope. That is the second evidence line [I5b] correctly removed, replaced with one
that is genuinely independent.

The Maintainer's direct request (2026-08-04) also clears the standing *fix
defects, build nothing new* gate.

### Proportionality, re-run against +4.67

At +16/plan the original five-rung ladder with strict ordering was arguably
proportionate. At **+4.67** it is not, and the revision is smaller for that reason
as much as for [I2]'s: one new token, one relocated grammar, two eligibility
rules, no ordering rule, no new gate, and the largest chunk of work split out.
The corrected figure is what makes "adopt the grammar you already have" the right
size of answer.

### Author-accounting -- corrections

* **Invariant 3 is documentary**, per [I1]. Its enforcer is *a reviewer opening
  both files at archive-preparation* -- not the loop-fidelity lens, which
  `test_loop_fidelity_gate.py` shows checks dangling doctrine references, and not
  `bootstrap/fidelity-check.md`, which answers a manifest question and at `:29`
  explicitly exempts `dev/PLANNING.md` as living state. The reviewer's mutation
  test is decisive: inverting the mirror to contradict the doctrine yields
  `check_cairn` rc=0 and 1916 passing tests. **All three invariants are
  documentary; none is mechanically enforced.** A content-parity gate over the
  named doctrine -> template pairs is recorded as a candidate successor, not taken
  here, because it would fire the External-escalation rule.
* **Public-path -> test mapping, corrected.** No test asserts the durable-home
  strings (`grep` over `bootstrap/tests/`: zero hits). The node that governs the
  planner edit is
  [`bootstrap/tests/test_notice_install.py`](../../bootstrap/tests/test_notice_install.py)
  `::test_every_self_hosted_twin_stays_byte_identical_to_its_source` (`:98`),
  which fails if the two planner copies diverge -- so editing one without the
  other is caught.
* **Known omissions, updated.** The (guard/wontfix/defer) routing estimate is
  withdrawn entirely rather than softened; the retro pass produces the real figure
  per-item. The "12 of the 59" is withdrawn. The board-row metric is replaced by
  an explicitly unmeasurable statement over outstanding follow-ups.

### Governing principle, restated

**An artifact closes more than it opens.** Stated over **outstanding follow-ups**,
not board rows -- and **not measurable today**, which is stated rather than
implied. The board-row form was falsifiable in a direction that did not track the
managed quantity ([I11]): four of five dispositions reduce board rows without
closing work, and the successor-proposal disposition increases outstanding work
while scoring zero. No checker is proposed, for the reason the reviewer states
better than the original draft did: a presence-checker would certify green
exactly the degenerate case the *Signals* section fears.

---

## Dispositions -- self-applied -- Claude (Strategy) -- 2026-08-04

Raised by the Maintainer immediately after the revision landed at `8a28d44`:
*"This isn't an example of narrowing scope and creating deferrals is it?"*

It partly is. The audit below applies **C1** to this proposal itself, which is
both the honest answer and a test of whether the rule is usable: a proposal that
cannot run its own grammar is evidence against the grammar.

Every forward obligation the Response and Revised proposal create, with its
token. Nothing here is authorized yet -- **C3 makes `defer` a Maintainer act, and
this block is the request, not the grant.**

| # | Forward obligation | Token | Status |
|---|---|---|---|
| D1 | The 59-item retrospective pass over `### Deferred follow-ups` | `defer` (successor) | **requested** -- conditioned on same-session opening |
| D2 | A content-parity gate over the doctrine -> `templates/core/` mirrors ([I1] route b) | `defer` (successor) | **requested** -- ineligible for `wontfix` under C4 |
| D3 | Whether rung-`defer` self-authorization is honest enough on a solo profile | `accept` | in scope -- answered below |
| D4 | Whether batching actually bounds Maintainer load | `wontfix` | declined -- rationale below |
| D5 | `bootstrap/scaffold.py --summary` unexercised on this pass | `accept` | in scope -- lands in the plan's verification commands |

**D1 -- the retro pass.** Defensible as written: it is routed to the Decision,
and the Response names the refusal path (reject the split, keep item 8 in scope).
But the "same session" condition is **a promise with no mechanism**, which is the
weaker half of what this proposal criticizes. Strengthened here: if the Decision
accepts the split, the successor's stem is named *in the Decision commit body*,
so its absence is visible in `git log` rather than only in a reader's memory.

**D2 -- this one was the defect.** The Response recorded it as "a candidate
successor, not taken here" -- an author-created forward obligation with no home,
no trigger and no approval, written into the section that was accepting findings
about exactly that pattern. It is also **adopter-reaching**: the doctrine ->
template mirror is the adopter contract, and the reviewer's mutation test showed
it is fail-open across all fifteen surfaces. Under **C4** that makes it
ineligible for `wontfix`, so it cannot be disposed of by the author at all. It is
a `defer` request, and if the Maintainer declines to authorize it, the correct
outcome is that **C1-C7 land with invariant 3 documented as fail-open and
nothing more** -- not that the gate quietly floats.

**D3 -- solo-profile self-authorization,** left open by the reviewer rather than
rubber-stamped. Answered in scope: on a solo profile C3 collapses to a written
justification to oneself, which is **weaker but not vacuous** -- the value is that
the justification is *written into the record at a serialization point*, where a
later reader (or the same person cold) can see what was claimed. Cairn's whole
premise is that recorded deliberation beats unrecorded conviction even when the
author and the decider are the same person. This is that premise applied to
deferral, and it should be stated in the doctrine text rather than left implicit.

**D4 -- Maintainer-load empiricism.** Declined. No artifact in the tree measures
it, building one would be a new mechanism this proposal explicitly avoids, and
the *Signals* section already names the failure ("the Maintainer becomes the
bottleneck") with a recovery. Declining it is only available because it reaches
no adopter, blocks no release, and needs no Decision -- the C4 eligibility test,
run rather than asserted.

**What this block demonstrates, and what it does not.** It shows the grammar is
usable on a live artifact and that the C4 eligibility rule does real work -- it
disqualified D2 from the disposition its author had already quietly chosen. It
does **not** show the rule is enforced: this block exists because the Maintainer
asked, not because anything required it. That is the same documentary-not-
mechanical limit stated throughout, now demonstrated on the proposal itself.

---

## Decision -- Human Maintainer -- 2026-08-04

**ACCEPT as revised.** Plan review tier ratified at **Internal**.

Scribed by Claude (Strategy) at the Maintainer's explicit instruction. The
authorizing words, verbatim:

> I accept as revised. Please scribe. Internal plan-review tier is fine.

and, on the work that follows:

> Please open this plan, review it internally, then implement + code review
> and archive independently.

**What this Decision carries.** The Revised proposal as it stands at `8a28d44`
-- C1 through C7 -- plus the plan-review tier at Internal, which the Response
had deferred to this Decision rather than the author ruling on its own tier.

**D1 (the retro pass) is carried**, because the split is stated inside the
Revised proposal and "as revised" is therefore authorization for it. Its
condition binds the implementing agent: the successor artifact opens in **this
session**, and its stem is named in a commit body so its absence is visible in
`git log` rather than only in a reader's memory.

**D2 (the content-parity gate over the doctrine -> `templates/core/` mirrors) is
NOT carried.** No authorizing words were given for it, and under the proposal's
own **C4** it is adopter-reaching and therefore ineligible for author
disposition -- so silence is not consent and the scribe does not supply one. The
artifact's stated default applies: **C1-C7 land with invariant 3 documented as
fail-open, and the gate is not built.** Recorded here rather than omitted so a
later reader can see the gate was considered, requested, and left unauthorized.
The Maintainer may authorize it at any time; nothing about this Decision
forecloses it.

**Note on scope narrowing.** This Decision accepts a proposal materially smaller
than the one opened at `9201ea3` -- one new grammar token rather than a
five-rung parallel vocabulary, after the Internal review established that
Cairn's existing `wontfix` disposition already provides the drain and the
governing metric had been overstated 3.4x. The narrowing is recorded as a
correction, not a concession.
