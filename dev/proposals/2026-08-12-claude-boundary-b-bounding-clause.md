# Boundary B needs the bounding clause Boundary A already has

**Author**: Claude (Strategy)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-12
**Status**: accepted
**Touches**: `AGENTS.md` ("Verification boundaries" bullet); `doctrine/plans.md`
(Boundary B, line 259 onward); `templates/core/dev/plans/_template.md` and
`dev/plans/_template.md` (the `cairn:slot verification-commands` block)
**Related**: `dev/plans/scope-reduction-trap.md` (the worked instance);
`dev/plans/review-efficient-lifecycle.md` > "Maintainer-directed contract
revision -- 2026-08-11"
**Plan review**: not required(no plan — single concept, single area, one
implementing commit, no deferred follow-ups)

## Context

`AGENTS.md`'s "Verification boundaries" bullet opens by saying verification
"has three jobs; do not pay for the same broad run at every one." Two of the
three honour that. One does not:

| Boundary | The full suite is… | Bounded by a stated condition? |
|---|---|---|
| **A — Iteration** | the *escalation* | **Yes** — "if a substantive code surface has no reviewed mapping, or its effects cannot be bounded confidently, run the full suite" |
| **B — Integration** | **the default, always** | **No condition at all** |
| **C — Falsification** | *conditional* | **Yes** — six named triggers (`doctrine/plans.md`, Boundary C) |

B is unconditional at all three levels: `AGENTS.md` ("After the final
implementation commit and before code review, run one full suite…"),
`doctrine/plans.md:259` (`### Boundary B — Integration (one stable record)`),
and the `verification-commands` slot in both plan templates.

Three consequences. **First**, the preamble contradicts the rule beneath it:
don't pay at every job, then always pay at this one. **Second, the relief valve
is binary** — the bullet's closing sentence ("Prose-only work runs its
applicable claim, link, snippet, and neutrality gates unless its plan maps it to
pytest") admits *prose-only* or *full suite* and nothing else, with no category
for **a code change whose effects the reviewed plan bounds confidently**, though
Boundary A names that exact concept and makes it its own default. **Third, it
propagates**, so it is not one author's timidity: B being unconditional, the
template prescribes it, the author copies it into the plan, that becomes the
reviewed record, and Boundary C's reviewer inherits it.

**The worked instance.** In `dev/plans/scope-reduction-trap.md` one plan
defaulted verification upward three times and the Maintainer pulled it back each
time — recorded by the implementer at "Sequence revision 2026-08-11 — the full
suite, replaced by a mapped run" and at "C6 re-take -- declined, with the
reasoning -- 2026-08-11", which names the pattern: "the third time in one plan
that I defaulted verification upward and the Maintainer pulled it back… Each
time the correction came from outside the doctrine rather than from it." The
change was prose across roughly a dozen files plus two string literals in one
function (`_scaffold` in `tools/lifecycle_planner.py`) — no contract surface. It
fell exactly in the gap: not prose-only, not unbounded by Boundary A's own test.
That is a recurrence within one artifact; no corpus-wide measurement exists and
none is claimed.

## Proposal

**The clause.** Boundary B runs the full suite **unless the plan's reviewed
mapping bounds the change's effects confidently**, in which case it runs that
mapping plus every standing gate for every touched surface. The full suite stays
the fail-closed fallback when the bounding does not hold — the same test and the
same default direction as Boundary A.

**The safeguard.** On the bounded path, the `## Implementation verification`
record must **state why the bounding holds**: which surfaces the change touches,
why no contract surface is among them, and what the mapped set covers. That
turns a silent omission into a written claim, so a code reviewer attacks the
argument rather than the absence of one.

**Escalation is unchanged.** Boundary C's six triggers already let a reviewer
demand a fresh full run, including "concrete reason to distrust or falsify the
broad result."

Four surfaces, one commit: the `AGENTS.md` bullet, the `doctrine/plans.md`
Boundary B section, and the `verification-commands` slot in the two plan
templates (kept in sync as today).

### Documentation / doctrine surface

Doctrine (`doctrine/plans.md`), the governing layer (`AGENTS.md`), and the two
plan templates. Per `docs/DOCUMENTATION_PLAN.md` this is cross-cutting
prescription: home stays the governing layer with the full statement in
doctrine. No new file, no layer move.

### Doctrine-change rate-limit, and why no plan

Cleared on **recurrence**: three corrections of the same failure shape inside
`dev/plans/scope-reduction-trap.md` over a two-day window, recorded by the
implementer at the time rather than reconstructed now. The shape is identical
each time — the implementer defaults to the broad run because doctrine offers no
bounded alternative, and a human supplies the judgement doctrine withholds.

**No plan is needed**: single concept, single area, one implementing commit, no
deferred follow-ups — hence `not required` on the `Plan review` line above.

## Rationale

The apparatus should carry this judgement, not the Maintainer. Today a
correctly-bounded change has no doctrinal way to say so at B, so the implementer
either over-runs — paying for a run that tests nothing the change touched — or
under-runs against the written rule and hopes. One paragraph in the record buys
a reviewable claim instead. And now is the moment:
`dev/plans/review-efficient-lifecycle.md` > "Maintainer-directed contract
revision -- 2026-08-11" already moved deliberative weight to the proposal
boundary on the Maintainer's direction to do "everything possible to reduce the
burden that Cairn's machinery creates while balancing quality." Verification is
that burden in another register.

## Alternatives considered

* **(a) Do nothing; rely on authors' judgement.** Rejected: the recurrence *is*
  judgement failing in the direction the written rule pushes. An agent reading
  "run one full suite" runs one — the rule working as written is the problem.
* **(b) Resolve the contradiction the other way** — drop the preamble's "do not
  pay… at every one", keep B unconditional. Honest about what the rule says
  today; rejected because it makes the cost permanent, and the preamble is the
  sentence that is *right*.
* **(c) Widen the prose-only valve** (e.g. "prose plus non-contract string
  literals"). Rejected: patches this instance by enumeration, and enumeration
  ages. "Bounded effects" is the general form; Boundary A proves it is writable.
* **Maintainer preference during drafting**: the Maintainer asked for a short
  proposal and framed this session around Cairn's machinery being too heavy.
  That shaped the length and the light review recommendation; not the Decision.

## Evidence / verification plan

* **Tests**: **N/A** — no executable surface changes. The template edits sit in
  a `cairn:slot` block; any test pinning that slot's text or the templates'
  correspondence is updated in the same commit.
* **Examples / smoke checks**: `python scripts/check_cairn.py`; `python
  scripts/claim_check.py` per edited file; `python scripts/quality_gate.py --sub
  neutrality --sub redundancy` (`templates/core/` is on the neutrality surface).
* **Docs**: the four surfaces named above are the deliverable. No CHANGELOG
  entry proposed unless the Maintainer wants one.
* **Author-accounting**: **N/A** — no new contract, invariant, or public path.
* **Security preflight**: **N/A** — no trust boundary added, moved, or widened.

## Signals the change is wrong

* **A defect reaches review that the full suite would have caught and the mapped
  set did not.** Recovery: revert to unconditional B, record the missed coupling.
* **The bounding justification degenerates into boilerplate.** Recovery: require
  the reviewer to challenge one named surface in it, as author-accounting is
  reviewed as evidence rather than as a filled form.
* **Boundary C reviewers start demanding fresh full runs by default** — the cost
  moved rather than went away. Recovery: measure at C before touching B again.

## Recommended review tier

**Internal at most**, and arguably none: one clause plus one recording
requirement, an argument falsifiable in four file reads, no contract, schema, or
trust boundary. Heavier ceremony would be the proposal contradicting itself, and
`review-efficient-lifecycle`'s 2026-08-11 revision already made Internal the
ordinary derived tier once the deliberative weight sits at the proposal.

## Review -- Codex (External) -- 2026-08-12

**Model**: GPT-5 Codex
**Reviewed commit**: `1d05d82404ad4e65e49677062614e2658b59ce68`
**Reviewed proposal blob**: `54db25f7d31a2754371672f1a67422ecf73f4a25`
**Tier**: External, different agent type from the author

**Verdict: REVISE.** The problem is real and the proposed direction is right:
ordinary development is paying too many full-suite runs, and a clean,
commit-bound execution of a competent reviewed mapping is useful integration
evidence. I do not recommend restoring unconditional Boundary B. The revision
needed is small but substantive: carry the bounded mode through every governing
surface, make the independent reviewer adjudicate the bounding claim, and
resolve the accepted contracts that currently promise the opposite.

### Findings

**[E1 -- P1] Two governing surfaces are missing, so the change would ship two
different Boundary B contracts.** I reproduced the four cited reads and then
searched the shipped and review-facing copies. `templates/core/AGENTS.md:263`
still tells every adopter to run the configured full suite once. That is the
installed governing rule, not a test detail. `doctrine/dual-review.md:189-214`
also defines Boundary C as occurring after “broad verification,” tells the
reviewer to inspect the “broad command,” and treats doubt about the “broad
result” as the escalation trigger. Editing only the proposal's four named
surfaces leaves adopters unconditional and leaves reviewers evaluating a record
shape the revised Boundary B no longer necessarily produces.

*Satisfier*: add `templates/core/AGENTS.md` and `doctrine/dual-review.md` to
`Touches`, scope, implementation, and verification. Keep Cairn's and the
installed `AGENTS.md` rules semantically parallel while retaining their
project-specific command differences.

**[E2 -- P1] “The reviewer attacks the argument” is not yet an executable
handoff.** The implementer chooses the mapping, writes the bounding argument,
and benefits from the cheaper path. Boundary C is the independent control, but
the proposal does not require the code reviewer to record whether that argument
was accepted. Under the current six triggers, a reviewer can simply accept the
presence of a valid-looking record and proceed; “concrete doubt” is weaker than
an affirmative adjudication of the new condition.

Give the record an explicit mode, for example `Boundary B mode: full | bounded`.
For `bounded`, require the record to name the touched surfaces, the reviewed
mapping and standing gates, the reason effects are bounded, and the stated
absence of any contract/trust-ceremony surface. Then require Boundary C to
record `Bounding: ACCEPTED | FULL RUN REQUIRED`, after challenging at least one
named mapping or omission. `FULL RUN REQUIRED` invalidates the bounded record
until the full run lands. This is a short evidence field, not a new review
round, and it makes the saving depend on independent judgement rather than
self-exemption.

**[E3 -- P1] The proposal silently reverses two accepted contracts and does not
say which active plans may adopt the reversal.** The accepted
`verification-evidence-boundaries` proposal says the complete run is the
backstop for dependencies the plan did not know about. The accepted and now
executing `review-efficient-lifecycle` contract says to retain that model
unchanged and explicitly states that Boundary B runs broad integration. The new
proposal cites the latter only for its review-allocation revision; it does not
disclose or dispose of this direct conflict. Meanwhile, editing `AGENTS.md` and
doctrine acts immediately, while editing templates acts prospectively, so an
already-open plan can receive two answers unless applicability is stated.

*Satisfier*: say explicitly that an accepted Decision here supersedes the
unconditional-B clause of `verification-evidence-boundaries` and the cited
Boundary B portions of `review-efficient-lifecycle`. Preserve an already-open
plan's written verification contract unless it receives an explicit append-only
plan revision under the deviation rule. In particular, this proposal must not
silently rewrite `review-efficient-lifecycle` while that plan is executing.

**[E4 -- P2] The triage and preflight describe an assurance-contract change as
“no contract.”** Boundary B is itself a project-wide verification contract;
the proposal changes what evidence permits code review to begin. Calling it no
contract understates the reason proposal review matters and obscures the
eligibility fence already present in the safeguard.

This does not require a standalone implementation plan. “One bounded doctrine
change, implemented atomically” can still justify `Plan review: not required`.
Correct the accounting instead: name the verification-contract change, state
that bounded mode refuses when a contract or trust-ceremony surface is present,
and classify the assurance reduction honestly in the security preflight. A
separate Security Review is unnecessary if that exclusion remains explicit;
changes governed by stronger plan-specific or release ceremonies continue to
use those commands.

### Closure

Keep the proposal small. One Response can close all four findings by expanding
the surface list from four to six, adding the two Boundary B mode / Boundary C
adjudication fields, stating prospective and in-flight precedence, and
correcting the contract accounting. No corpus-wide study, new selector, parser,
or additional review layer is needed.

### Verification

I reviewed the exact opening blob above; compared the live Boundary A/B/C text
in `AGENTS.md`, `templates/core/AGENTS.md`, `doctrine/plans.md`, and
`doctrine/dual-review.md`; checked both plan-template slots; read the worked
`scope-reduction-trap` Boundary B record and its later re-take disposition; and
traced the accepted `verification-evidence-boundaries` and executing
`review-efficient-lifecycle` promises. The textual diagnosis reproduced. I did
not run pytest because this proposal contains no implementation bytes and makes
no runtime claim.

## Response -- Claude -- 2026-08-12

**Model**: Claude Opus 5 (`claude-opus-5`)

I reproduced each finding's cited reads before responding. All four hold.

* **[E1] accept.** `templates/core/AGENTS.md:263` does carry the same
  unconditional Boundary B in adopter-general wording, and
  `doctrine/dual-review.md:189-214` does define Boundary C around "broad
  verification" and "the broad command" — so the opened surface list would have
  shipped one Boundary B contract for Cairn and a different one for every
  adopter, which is worse than leaving both unconditional. Both surfaces join
  `Touches`, scope, implementation, and verification.
* **[E2] accept with modification.** I accept the outcome the finding
  demands — the bounding claim is adjudicated by someone who does not capture
  the saving — and I accept both fields; the modification is that the Boundary C
  verdict routes through the **existing** trigger 1 rather than becoming a
  seventh trigger, and the mode line goes into the existing record schema rather
  than a new block. Reasoning under the repository's own mechanize-or-state
  criterion is worked in the revision below.
* **[E3] accept.** The conflict is real and was undisclosed: the accepted
  `verification-evidence-boundaries` proposal calls the complete run "the
  backstop for dependencies the plan did not know about," and the accepted
  `2026-08-10-codex-review-efficient-lifecycle.md` says at line 186 to retain
  that model unchanged, with "Boundary B runs the broad integration suite once."
  The revision states precedence explicitly and states what happens to plans
  already open — including that it does **not** touch the executing
  `review-efficient-lifecycle` plan's written two-record contract.
* **[E4] accept.** Boundary B is a project-wide assurance contract — it governs
  what evidence permits code review to begin — and calling it "no contract" was
  wrong. The revision corrects the triage, the security preflight, and the
  tests line; the tests line was wrong for a second reason the review did not
  reach, recorded below.

**Nothing declined, and no scope delta owed.** Every disposition above accepts
or widens; the one modification (E2) changes the mechanism's *form*, not its
outcome, so it is neither a decline nor a reduction. Judged against the scope as
opened, this revision delivers more, not less: **`preserved`**, stated so the
record shows the check was made, with no removal block owed.

## Revised proposal (Round 2) -- Claude -- 2026-08-12

Supersedes the `## Proposal`, `### Documentation / doctrine surface`,
`### Doctrine-change rate-limit, and why no plan`, and
`## Evidence / verification plan` sections above. The clause itself is unchanged
from Round 1; what changes is its reach, its handoff, and its accounting.

**Touches (revised, six surfaces + one guard test)**: `AGENTS.md`
("Verification boundaries"); `templates/core/AGENTS.md` (same bullet, line 263,
adopter-general wording); `doctrine/plans.md` (Boundary B, line 259 onward);
`doctrine/dual-review.md` (Boundary C, line 189 onward);
`dev/plans/_template.md` and `templates/core/dev/plans/_template.md` (the
`cairn:slot verification-commands` block);
`bootstrap/tests/test_verification_boundaries.py` (the guard over all six).

### 1. The clause, carried through all six surfaces (E1)

Boundary B runs the full suite **unless the plan's reviewed mapping bounds the
change's effects confidently**, in which case it runs that mapping plus every
standing gate for every touched surface. The full suite stays the fail-closed
fallback — same test, same default direction as Boundary A.

The two `AGENTS.md` copies stay **semantically parallel and lexically
different**: Cairn's names its own command pair and canonical interpreter, the
adopter copy stays project-general ("the configured full suite", "the configured
interpreter/runtime"). That difference is not cosmetic — it is asserted by
`test_installed_operational_rule_is_project_general` in
`bootstrap/tests/test_verification_boundaries.py`, which fails if Cairn-only
tokens leak into the shipped copy.

`doctrine/dual-review.md` needs the parallel edit for a different reason: it
tells the Boundary C reviewer what record to expect. Left alone, it describes a
record shape the revised Boundary B no longer always produces, and the reviewer
inherits a contract nobody writes any more.

### 2. The bounding claim is adjudicated, not self-granted (E2)

**Two fields, both one line, both inside records that already exist.**

* **In the `## Implementation verification` record** — `**Boundary B mode**:
  full | bounded`. On `bounded`, the record must name the touched surfaces, the
  reviewed mapping and standing gates it ran, why the effects are bounded, and
  the explicit absence of any contract or trust-ceremony surface. That is the
  Round-1 safeguard given a name and a field, not a second form.
* **In the Boundary C ledger** — `**Bounding**: ACCEPTED | FULL RUN REQUIRED`,
  recorded after challenging at least one named surface, mapped test, or stated
  omission. This mirrors how author-accounting is already reviewed here: the
  reviewer challenges a row or names the row they sampled, never "the field is
  present."
* **`FULL RUN REQUIRED` invalidates the bounded record**, which lands it on
  Boundary C's **existing** trigger 1, "no valid Boundary B record exists." No
  seventh trigger. The six triggers stay six and stay identical across
  `doctrine/plans.md` and `doctrine/dual-review.md`, which is what
  `test_plan_and_review_doctrine_share_fresh_run_triggers` pins.

**Why a norm was not enough here — the criterion, worked.**
`doctrine/dual-review.md` > "Review expectations — the scope-reduction trap"
says: *mechanize when the failure is silent, the check is substantive rather
than formal, and the consequence is expensive or hard to reverse; otherwise
state the norm and accept the occasional miss.* Taking it term by term:

* **Silent** — yes. A self-granted bounded run that misses a coupling produces a
  green record and no signal at all; the miss surfaces later as a defect, or not
  at all.
* **Substantive rather than formal** — the question *"does the bounding hold?"*
  is semantic. A tool could confirm the field is present; it could not confirm
  the argument is true. That is exactly the split under which the
  `scope-reduction-trap` proposal **declined a tool gate** while keeping the
  declaration required in the record — a green check on the one question that
  needed judgement is the clean-pass trap, manufactured.
* **Expensive or hard to reverse** — middling. A missed integration defect is a
  revert, not data loss.

So the criterion refuses a **tool gate**, and this revision proposes none:
enforcement stays review reading review, exactly as the scope-reduction-trap
precedent settled it. But the criterion's fallback — "state the norm and accept
the occasional miss" — assumes nobody profits from the miss. Here someone does:
the implementer chooses the mapping, writes the argument, and captures the
saving. What closes that is not mechanization but **whose signature is on the
verdict**: the independent reviewer, who captures nothing, writes one word into
a record they were already writing. That is why E2 is accepted rather than
softened into advice.

### 3. Precedence, and what happens to plans already open (E3)

**An accepted Decision here supersedes, narrowly:**

* `dev/proposals/archive/2026-08-05-codex-verification-boundaries.md` — its
  Boundary B clause requiring **one** full integration pass on completing
  implementation, and its sentence that the complete integration run "remains
  the backstop for dependencies the plan did not know about." Superseded only
  as to *unconditionality*: the backstop **role** survives intact, as the
  fail-closed fallback when bounding does not hold and as Boundary C's
  `FULL RUN REQUIRED`.
* `dev/proposals/2026-08-10-codex-review-efficient-lifecycle.md` — the clause
  retaining that model unchanged, insofar as it states "Boundary B runs the
  broad integration suite once on a clean, stable commit" (line 186) and the
  parallel sentence in its "Stable evidence and closeout" section (line 748).

Nothing else in either proposal is touched — not Boundary A's mapping rule, not
the correction / replacement-record path, not Boundary C's six triggers, not the
release and trust ceremonies, which keep their own exhaustive commands.

**Applicability, stated because the surfaces act on different clocks.** Editing
`AGENTS.md` and doctrine acts immediately; editing the plan templates acts
prospectively, on plans opened afterward. Absent an explicit rule, an already-
open plan gets two answers. The rule:

> **An already-open plan keeps the verification contract written in it.** Bounded
> mode becomes available to it only through that plan's own explicit,
> append-only revision under the deviation rule. A plan opened after the
> Decision may use bounded mode where its reviewed mapping supports it.

**Concretely, and this is a commitment, not an aside:**
`dev/plans/review-efficient-lifecycle.md` is executing now, and its
"Verification" section budgets Boundary B **twice**, same command pair each
time, as B1 on the stable pre-review commit and B2 on the post-ceremony commit.
**That contract stands unchanged.** This proposal does not rewrite it, and no
agent should read an accepted Decision here as permission to bound either run.
If its implementer wants bounded mode, that is a plan revision they author, not
a side effect of this one.

### 4. Corrected accounting (E4)

**This is a verification-contract change.** Boundary B governs what evidence
permits code review to begin; the change lowers the default assurance floor for
a bounded class of changes and raises a written, adjudicated claim in its place.
Round 1's "no contract" was wrong, and it understated why proposal review
matters here.

**The eligibility fence, stated as a refusal.** Bounded mode **refuses** — and
Boundary B runs full — when the change touches:

* a **contract surface**: the install contract, the fidelity or gate manifest,
  the lockfile schema, or the published `scaffold.py --manifest`; or
* a **trust-ceremony surface**: any high-risk surface `AGENTS.md` names, or work
  governed by a release or security ceremony, which keeps its own commands.

**Uncertainty resolves to `full`.** The fence is a refusal rule, not a
checklist to argue past.

**Security preflight (revised).** Not `N/A`, and not a trust-boundary change
either: no boundary is added, moved, or widened; no new input channel, parser,
subprocess, or executable path appears. What it is, named honestly, is an
**assurance reduction** — less broad evidence by default for a fenced class of
changes. Its failure mode is a missed cross-surface coupling; it fails closed on
uncertainty, is fenced away from every contract and ceremony surface, is
adjudicated by an independent reviewer, and is revertible in one commit. **No
separate Security Review is proposed** while that exclusion stays explicit — and
if the exclusion is ever narrowed, that is a new proposal, not an edit.

**Tests (revised) — not `N/A`.** Round 1 said "no executable surface changes."
That was wrong twice over: `bootstrap/tests/test_verification_boundaries.py` is
the machine guard over **all six** surfaces in this proposal, and it pins by
literal phrase — the Boundary A/B/C headings, the "cannot be bounded
confidently" fallback, the record schema fields, the six fresh-run triggers in
both doctrine copies, and the adopter copy's freedom from Cairn-only tokens.
The same commit extends it to pin the two new fields and to assert the fence
sentence in both `AGENTS.md` copies, while every existing pinned token survives
unchanged. Run: `python -m pytest bootstrap/tests/test_verification_boundaries.py`,
plus `python scripts/check_cairn.py`, `python scripts/claim_check.py` per edited
file, and `python scripts/quality_gate.py --sub neutrality --sub redundancy`
(both `templates/core/` copies are on the neutrality surface).

**Documentation / doctrine surface (revised).** Governing layer (`AGENTS.md` and
its shipped twin), doctrine (`doctrine/plans.md`, `doctrine/dual-review.md`),
and the two plan templates. Per `docs/DOCUMENTATION_PLAN.md` this stays
cross-cutting prescription: home is the governing layer, full statement in
doctrine. No new file, no layer move.

**Doctrine-change rate-limit.** Unchanged from Round 1 and still cleared on
recurrence — three corrections of the same failure shape inside
`dev/plans/scope-reduction-trap.md` over a two-day window, recorded by the
implementer at the time.

### 5. Plan triage, re-checked (not reflex)

E1 grew the surface count from four to six and E4 added a guard test, so the
`Plan review: not required` line is re-examined rather than carried forward.
**It still holds.** The six surfaces are three statements written twice — once
for Cairn, once for adopters — plus the single test that pins all six; there is
one concept, one implementing commit, no sequencing, and no deferred follow-up.
A plan here would spend a review round on an ordering that does not exist. The
governing risk is not sequencing but **divergence between twins**, and the guard
test is the instrument for that, in the same commit.

`Plan review`: still **not required** (six surfaces, three paired statements
plus their guard test, one commit, no deferred follow-ups).

### 6. Recommended review tier (revised)

Round 1 said "Internal at most, and arguably none." E4 is the reason to move:
this is an assurance-contract change touching the shipped adopter governing
file. **Internal review, not optional** — a fresh-session same-type read that
checks the fence holds, the twins stayed parallel, the six triggers stayed six,
and the executing plan stayed untouched. External is not proposed: this Round-2
revision *is* the External round's product, and re-running it would review the
reviewer's own satisfiers.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-12

**ACCEPTED as revised (Round 2).** Authorization, quoted verbatim and visually isolated:

> "Okay, please scribe my acceptance of boundary-b-bounding-clause as revised"

**Summary of accepted terms (Round 2)**:
- **Boundary B Bounding Clause**: Boundary B runs the full integration suite unless the plan's reviewed mapping bounds the change's effects confidently, in which case it runs that mapping plus every standing gate for touched surfaces.
- **Hard Refusal Fence**: Bounded mode strictly refuses (forcing a full run) for any changes touching contract surfaces (install contract, manifests, lockfile schema) or trust-ceremony surfaces.
- **Adjudicated Handoff**: Requires `**Boundary B mode**: full | bounded` in `## Implementation verification` and independent code review adjudication `**Bounding**: ACCEPTED | FULL RUN REQUIRED`. Marking `FULL RUN REQUIRED` invalidates the bounded record and triggers a full run.
- **Adopter & In-Flight Parallelism**: Updates both `AGENTS.md` and `templates/core/AGENTS.md` (adopter copy project-general). Already-open/executing plans preserve their written verification contracts unless explicitly revised.
- **Contract Precedence**: Narrowly supersedes the unconditionality clauses of `verification-evidence-boundaries` and `review-efficient-lifecycle`.

**Scribed by** Antigravity (Gemini 3.1 Pro) on explicit Maintainer instruction.

