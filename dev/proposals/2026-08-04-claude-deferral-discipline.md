# Deferral is a Maintainer-approved exception, not an author default

**Author**: Claude (Strategy)
**Model**: claude-opus-5
**Date opened**: 2026-08-04
**Status**: proposed
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
