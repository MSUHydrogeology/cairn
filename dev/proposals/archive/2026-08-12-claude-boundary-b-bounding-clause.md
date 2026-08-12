# Boundary B needs the bounding clause Boundary A already has

**Author**: Claude (Strategy)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-12
**Status**: accepted (implemented, archived 2026-08-12)
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


## Code review -- Claude (Internal) -- 2026-08-12

**Model**: Claude Opus 5 (`claude-opus-5`)
**Tier**: **Internal** — fresh session, **same agent type as the implementer**.
This is the Internal *floor*, not External, and it does not satisfy an External
obligation. The proposal's §6 asked for exactly this tier and this scope.
**Reviewed commit**: `8d9e3517aa2466cb4ce178d4b8415a82363b24c4`, diffed against
its own parent `6701cb310f3a50d04cbb0c6b7a7b2636efb07170` (other agents
committed concurrently; `e249424`, `be73851`, `137e48a` are excluded).
**Reviewed proposal blob**: `b76ec7cfd4741d6141cda0941f25ce13ea897ff8`
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.x).

**Verdict**: Accept-with-followups

The clause is right, the six surfaces are faithfully delivered, and the fence
*text* says what the Decision accepted. What is weaker than it reads is the
**guard**: it catches deletion on every surface and catches nothing else, while
its docstrings and §2 claim more. And one accepted term — the already-open-plan
applicability rule — landed nowhere an agent will read it.

### Method (independent falsification, not a re-run)

I did not re-run the implementer's commands as my evidence. I extracted
`8d9e351` and its parent into two isolated trees (`git archive | tar -x`) and
ran **35 mutations of my own choosing** against the guard, restoring after each.
I differenced the gate output across the commit boundary rather than reading the
implementer's figure. Independently reproduced: guard **13 → 36** nodes
(parent test file in the commit tree: `13 passed`; landed: `36 passed`).
`quality_gate --sub neutrality --sub redundancy` is **byte-for-byte identical at
parent and at commit** (`neutrality fail=93 info=21`, `redundancy fail=0
info=2`) — so the "pre-existing and unchanged" claim is verified by difference,
which the commit body asserted but did not show.

*Not attributable to this commit*: `test_scope_reduction_trap.py::
test_the_two_planner_twins_stay_byte_identical` fails in the working tree today.
The twins are **byte-identical at `8d9e351`** (both
`cb72165be4223df0a62d4db2b12e7f2d656b74ea680eee1ec7d813b4e3d2aaa4`); the failure
comes from another agent's uncommitted edits to both planner files. Recorded so
it is not misfiled against this change.

### The four §6 checks

**1. The fence holds — on the text, yes.** All five governing/template surfaces
carry the refusal, and it reads as a refusal rather than a checklist: "Bounded
mode **refuses**, and the full suite runs, whenever…" plus "**Uncertainty
resolves to `full`** — the fence is a refusal rule, not a checklist to argue
past." Contract surfaces are enumerated (install contract, fidelity/gate
manifest, lockfile schema, published `scaffold.py --manifest`) and
trust-ceremony surfaces are pulled in by reference to the governing file's
high-risk list, which keeps the fence open-ended rather than a closed
enumeration — the failure mode Round 1 rejected alternative (c) for. Two leaks
in the *mechanism* rather than the wording are [F3] and [F6] below.

**2. The twins stayed parallel — `AGENTS.md` yes, plan templates unguarded.**
`test_installed_operational_rule_is_project_general` still means something: I
leaked `python -m pytest bootstrap/tests` into the adopter fence (**L1**) and,
separately, into adopter prose *outside* the fence (**L3**) — **both red**. The
adopter copy correctly generalises (`the project's install contract, manifests,
or lockfile schema`; `configured full suite`; `configured interpreter/runtime`)
while Cairn's names `scaffold.py --manifest` and Python 3.13.x. Semantically
parallel, lexically different, as accepted. The plan-template pair is **not**
covered by any equivalent guard — see [F5].

**3. The six triggers stayed six — in fact yes, by the guard no.** I read both
lists: `doctrine/dual-review.md:212-219` and `doctrine/plans.md:340-347` are six
items, identical, and `FULL RUN REQUIRED` routes to trigger 1 by invalidation
exactly as accepted. No seventh trigger was added. But the *guard* over that
outcome does not exist — see [F2].

**4. The executing plan stayed untouched — yes; the rule protecting it did not
land — no.** `git log 8d9e351^..8d9e351 -- dev/plans/review-efficient-lifecycle.md`
is empty; its line 559 still reads "Boundary B **twice**, same command pair each
time", and its budget table still says `| Boundary B | **2** |`. Untouched,
confirmed. The applicability rule is **absent from every landed surface** — see
[F1].

### Findings

#### [F1 -- P1] The already-open-plan applicability rule landed nowhere it governs

`grep` for `already-open`, `already open`, `plans already open`, `written
verification contract`, `keeps the verification contract` across all six landed
surfaces (`AGENTS.md`, `templates/core/AGENTS.md`, `doctrine/plans.md`,
`doctrine/dual-review.md`, both plan templates) returns **no match on any
surface**. The rule exists only in this proposal's §3.

This is an accepted term, not an inference: the Decision's summary lists
"**Adopter & In-Flight Parallelism**: … Already-open/executing plans preserve
their written verification contracts unless explicitly revised." §3 states it as
a block-quoted rule and calls the `review-efficient-lifecycle` case "a
commitment, not an aside."

Why it matters now rather than theoretically: **two plans are `executing`** —
`review-efficient-lifecycle` and `git-native-security-foundations`. An agent
orienting at session start reads `AGENTS.md`, not an accepted proposal in
`dev/proposals/`. What that agent now finds is a permission ("run the **full
suite unless** the plan's reviewed mapping bounds the change's effects
confidently") with **no in-flight carve-out attached to it**. Per
`docs/DOCUMENTATION_PLAN.md`'s own layering, a prescription that binds behaviour
belongs in the governing/doctrine layer; the deliberation layer records why.
This one is only in the deliberation layer, so it is recorded but not operative.

Mitigating, and the reason this is P1 rather than blocking: `AGENTS.md` >
*Git and commit workflow* already treats departure from an accepted plan as a
deviation, and `review-efficient-lifecycle` writes its command pair out
literally, so bounding it would require overriding explicit plan text. The
protection exists — just not in the form the Decision named.

*Satisfier*: one sentence in `doctrine/plans.md` > Boundary B, echoed in both
`AGENTS.md` copies — "A plan already open when this rule took effect keeps the
verification contract written in it; bounded mode becomes available to it only
through that plan's own append-only revision under the deviation rule." Or an
explicit Maintainer `wontfix` recording that the deviation rule is deemed
sufficient. **I have not made this edit** — reporting, not fixing.

#### [F2 -- P2] "The six triggers stay six" is asserted against the test's own literal

`test_full_run_required_routes_to_the_existing_first_trigger` closes with
`assert len(FRESH_RUN_TRIGGERS) == 6`. `FRESH_RUN_TRIGGERS` is a tuple literal
defined at the top of the *same test file*. That assertion reads a constant the
test itself owns; **no doctrine edit can ever make it fail.** The companion,
`test_plan_and_review_doctrine_share_fresh_run_triggers`, asserts the six tokens
are *present* in both files — it says nothing about a seventh.

Demonstrated, not argued. Three mutations, all **GREEN (36 passed)**:
* **T1** — added a seventh trigger to `doctrine/dual-review.md` only.
* **T2** — added a seventh trigger to `doctrine/plans.md` only (which also
  *desynchronises the two doctrine copies*, the thing the paired test is named
  for).
* **T3** — changed the prose "any of these **six** triggers" to "**seven**".

Control: **T4**, deleting trigger 2, is **red**. So the pairing catches removal
and is blind to addition and to the count itself.

This matters because §2 of the accepted revision rests an argument on it: "The
six triggers stay six and stay identical across `doctrine/plans.md` and
`doctrine/dual-review.md`, which is what
`test_plan_and_review_doctrine_share_fresh_run_triggers` pins." It does not pin
that. `AGENTS.md` > *Verifying claims* is explicit that "the document states
what that trigger actually verifies: a tool that returns success without testing
the claimed property is a worse defect than no tool, because it is silent."

*Satisfier*: count the enumerated items in each doctrine file (e.g. regex the
`^N. ` run under "A fresh full-suite run…" / "A fresh full-suite run replaces
reuse…") and assert the count is 6 and the two extractions are equal — then the
constant is derived from doctrine rather than declared beside it.

#### [F3 -- P2] `test_bounded_guard_detects_a_removed_fence` is a tautology

```python
text = _read(SELF_AGENTS).replace("trust-ceremony surface", "surface")
normalized = " ".join(text.split())
assert "trust-ceremony surface" not in normalized
```

The assertion is unconditionally true for **any** input: the token was just
replaced with a string that cannot contain it. Its own docstring says "Without
this pair an always-passing token check would look correct" — the test is itself
the always-passing check it warns about.

Demonstrated: **X2** — I truncated `AGENTS.md` to the empty string and ran this
node alone. **`1 passed`.**

This is the third instance of this shape shipped in this repository in three
days, and it deviates from the *correct* pattern already established three times
in the same file: `test_operational_guard_detects_removed_full_fallback`,
`test_record_schema_guard_detects_removed_reviewed_range`, and
`test_review_reuse_guard_detects_unconditional_reuse` each mutate, then feed the
mutant **through the violation function**, and assert the violation is
*reported*. The new one asserts on the mutated string directly and never invokes
the thing under test.

**It removes no coverage** — `test_bounded_boundary_b_contract_reaches_every_surface`
is the real guard and it genuinely fires (F1–F5, P1, P2 below all red). The
defect is that the file now contains a node that *claims* mutation coverage and
supplies none, which is precisely what makes this class hard to catch.

*Satisfier*: rewrite it in the file's own established shape — extract the
obligation check into a helper taking `text`, mutate, and assert the helper
*reports* the missing obligation.

#### [F4 -- P2] The fence binds only a record that declares itself bounded

Boundary C's new obligation is conditional on the implementer's own declaration:
"**On a bounded record** the reviewer records `**Bounding**: …`." Nothing in the
landed text says a Boundary B record **lacking** the `Boundary B mode` field is
invalid. Trigger 1 fires on "no valid Boundary B record exists", and validity is
nowhere defined to require the field.

So the fence has a silent path around it that is not a fence-wording problem:
an implementer runs a mapped subset, writes a record listing the commands they
ran and omitting the mode field, and it is indistinguishable from every
pre-2026-08-12 record in the tree. No adjudication is triggered, because nothing
declared itself bounded. The adjudication — the thing that makes the saving
depend on someone who captures nothing — is opt-in by the party who captures the
saving.

Both plan templates do say "The record uses these exact fields" with
`Boundary B mode` listed first, so a template-following author will include it.
That is a strong mitigation for plans scaffolded from the template and no
mitigation at all for the two plans already executing.

*Satisfier*: one clause in `doctrine/plans.md` — "A Boundary B record without a
`Boundary B mode` field is not a valid record (trigger 1)." That closes the
silent path without adding a seventh trigger and without a tool gate.

#### [F5 -- P3] No project-generality guard on the adopter plan template

`test_installed_operational_rule_is_project_general` covers
`templates/core/AGENTS.md` and nothing else. `templates/core/dev/plans/_template.md`
gained new fence prose in this commit and has no equivalent guard.
`_plan_template_violations` applies the **same** token set to both templates, so
it cannot detect divergence in the Cairn-specific direction.

Demonstrated: **L2** — I replaced the adopter template's generalised fence with
Cairn's own wording (`the published `scaffold.py --manifest``, `Python 3.13.x`,
`python -m pytest bootstrap/tests`, `python scripts/quality_gate.py`). **GREEN,
36 passed.** The neutrality gate does not catch this either — it looks for
*vendor* names, not Cairn-only paths.

The commit is correct as landed; the exposure is new because this commit is what
put Cairn-adjacent fence content into that file's neighbourhood.

*Satisfier*: extend the `cairn_only` tuple check to `ADOPTER_PLAN_TEMPLATE`,
adding `scaffold.py --manifest`.

#### [F6 -- P3] "Any high-risk surface the governing file names" + uncertainty→full may swallow the clause

`AGENTS.md`'s high-risk list includes **vendor-neutrality** ("Doctrine and
templates must name no AI model/vendor"). Read strictly, *every* doctrine or
template prose edit "touches" that surface — which, combined with "uncertainty
resolves to `full`", fences the most common class of change Cairn actually makes
out of bounded mode. Including the motivating worked instance: `scope-reduction-trap`
was "prose across roughly a dozen files plus two string literals", so under the
landed fence it plausibly resolves to `full` — the outcome the proposal set out
to prevent.

The natural reading — "high-risk surface" means its *mechanism or contract*, per
`AGENTS.md`'s own framing of that list as "Security-Review + proposal triggers"
— is defensible and probably intended. But the landed text supplies no
disambiguator, and the fail-closed rule pushes a careful agent toward the strict
reading. This is not a defect in the fence's tightness; it is the opposite risk,
and it makes the clause weaker than the argument for it.

*Satisfier*: qualify to "a change to a high-risk surface's mechanism or
contract (the changes that trigger a Security Review)", or add one worked
example of an eligible change. Cheapest disposition is a Maintainer `wontfix`
noting the natural reading governs.

#### [F7 -- P3] Slot placement is correct but unpinned

The fence sits inside `<!-- cairn:slot verification-commands -->` in both
templates (`dev/plans/_template.md:246-289`;
`templates/core/dev/plans/_template.md:238-277`) — correct, since the slot is
what a scaffolded plan inherits. `_BOUNDED_OBLIGATIONS` is checked against the
**whole file**, so the placement is not held. Demonstrated: **S1/S2** — I moved
the fence outside the slot end marker in each template. **Both GREEN.** The same
file already demonstrates the right pattern: `_plan_template_violations` scopes
`reviewed mapping` / `full suite` / the record fields to the slot.

### Mutation ledger — 35 mutations, chosen by me

**Held (red) — 15.** These are the ones that make the guard worth having:
| # | Mutation | Result |
|---|---|---|
| F1–F5 | Delete the fence from **each** of the five surfaces, one at a time | red on every surface |
| P1 | Drop only `trust-ceremony surface`, keep `contract surface` (Cairn `AGENTS.md`) | red |
| P2 | Drop only `contract surface`, keep trust-ceremony (adopter `AGENTS.md`) | red |
| A1–A3 | Delete the adjudication paragraph from `dual-review.md`, Cairn `AGENTS.md`, adopter `AGENTS.md`, one at a time | red on each |
| A5 | Weaken `**invalidates**` → `is noted against` | red |
| L1 | Leak `bootstrap/tests` into the adopter fence | red |
| L3 | Leak Cairn commands into adopter prose **outside** the fence | red |
| D3 | Delete the `**Boundary B mode**` record-schema bullet | red |
| T4 | Delete trigger 2 | red |
| X1 | Blank the entire Boundary B bullet | red (5 failures) |

Partial-phrase and single-surface deletion are genuinely covered — that is the
strongest thing I can say for this guard, and I could not defeat it by any
deletion I tried, on any surface, at any granularity.

**Defeated (green) — 12 substantive.** Grouped by what they show:
* *Unscoped token search* — **H1**: delete the fence body from Boundary B, then
  satisfy all four obligations from a **trailing glossary heading** appended at
  end of file that explicitly obliges no one. 36 passed.
* *Semantic inversion with tokens intact* — **I1** `Uncertainty resolves to
  `bounded`` (the fail-closed direction reversed, and the pinned token is
  `"Uncertainty resolves to"` **without its value**); **I2** "Bounded mode **is
  available**… even when the change touches [a contract surface]"; **I3** bounded
  becomes the default in `doctrine/plans.md`; **I4** the mode field made
  optional; **D1/D2** the mode bullet reduced to "The phrase Boundary B mode is
  optional and carries no obligation."
* *Adjudication gutted* — **A4**: "after challenging at least one named surface,
  mapped test, or stated omission" → "after **confirming the field is
  present**", i.e. the exact anti-pattern the same sentence forbids. Green.
  **A6**: "the reviewer additionally records" → "may, at their discretion,
  record". Green.
* *Trigger count* — **T1/T2/T3** ([F2]).
* *Slot placement* — **S1/S2** ([F7]).
* *Adopter generality* — **L2** ([F5]).
* *Tautology* — **X2** ([F3]).

**Green by design, and correct** — **W1** (whole clause reflowed onto one line)
and **W2** (a hard wrap inserted *inside* the `Boundary B mode` token). The
`" ".join(text.split())` normalisation makes the guard wrap-insensitive, which
is the right property for a prose guard and is worth recording as tested rather
than assumed.

**Calibration.** Most of the inversions are outside what any token-presence
guard can reach, and the docstring is honest that it asserts "the *obligation*,
not one exact sentence, so a rewording passes and a deletion fails" — that is an
accurate description of what it does. §2 declining a tool gate is also right, and
I am not asking for one. The three I count as defects are the ones where a
*document claims* coverage the code does not supply ([F2], [F3]) or where the
established in-file pattern was available and not used ([F7]).

### Scope fidelity — clean

The revert is complete and nothing else rode along. Verified by enumerating
**every deleted line** in the commit (`git diff 8d9e351^ 8d9e351 | grep '^-[^-]'`):
11 deletions, all inside the Boundary B / Boundary C regions of the six named
surfaces. No deletion anywhere else in any file.

Every pinned token from the accepted terms' "every existing pinned token
survives unchanged" survives, checked individually at `8d9e351`:
* `Falsification (targeted, after broad verification)` — present, ×1
* `Copying the implementation's broad command does not satisfy` — present, ×1
* `broad command is not a falsification ledger` — present in **both**
  `AGENTS.md` copies
* `distrust or falsify the broad result` — present in both doctrine copies
  (`dual-review.md:219`, `plans.md:347`)
* every `_operational_violations`, `_record_violations`, `_review_violations`,
  `RECORD_FIELDS` token — all 13 pre-existing nodes pass unchanged.

The commit body's self-report of the scope correction is accurate and the
correction is complete.

### Cross-document sweep

`grep -rln "Boundary B"` outside `dev/` returns exactly the four governing/
doctrine surfaces, the guard test, and the two `lifecycle_planner.py` twins. The
planner hits are a single blocking-verdict message string ("land a replacement
Boundary B record over the corrected range") that is **mode-agnostic** and needs
no edit; the planner does **not** parse `## Implementation verification` fields
at all (`grep` for `Implementation verification|Tested commit|Reviewed range` in
`tools/lifecycle_planner.py`: no hits), so the new field adds no executable
obligation. That is consistent with §2's "no tool gate is proposed" and is
correctly stated as a v1 omission in the guard file's module docstring. No
seventh surface was missed.

Remaining unconditional-B phrasing lives only in archived proposals and
`dev/plans/archive/verification-evidence-boundaries.md`, which are historical
records and correctly untouched.

`claim_check` on this proposal: **OK, no flags** (and I verified the checker
actually flags — injecting a deliberately non-existent proposal path into a
scratch copy produced the expected hard flag, so the clean result is a real
result rather than a silent tool). Note that §3's
citation `dev/proposals/2026-08-10-codex-review-efficient-lifecycle.md` now
resolves under `archive/`: that proposal was archived at `6701cb3` (08:42),
*after* the Round-2 revision was committed at `3f95bb1` (07:39). Correct when
written, append-only, no defect.

### The honest question: is the fence tight enough?

Arguing it rather than assuming it. **Against a change that declares itself
bounded, yes.** The enumeration covers the four contract surfaces by name; the
trust-ceremony half is open-ended by reference to the high-risk list, so it
inherits the scaffold/merge engine, the local interpreter binding, and the
portable-sweep trust root without re-enumerating them — the fence ages better
than Round 1's rejected alternative (c). Ambiguity about whether a surface is
covered is resolved by an explicit fail-closed rule stated twice. I could not
construct a plausible contract-touching change that reads as clearly eligible.

**The leak is not in the enumeration; it is in who opens the gate.** [F4]: the
fence and the adjudication both trigger on the implementer's own `bounded`
declaration. An implementer who runs less and simply does not write the field
produces a record shaped exactly like every record written before this change,
and no trigger fires. The apparatus asks the party who captures the saving to
raise their own hand. §2 argued — correctly — that mechanising *"does the
bounding hold?"* would manufacture the clean-pass trap, because the question is
semantic. But *"is the mode field present?"* is not semantic; it is the formal
half, it is exactly what §2 concedes a tool could confirm, and it is the half
that is currently unbound. One sentence making a field-less record invalid
closes it inside the existing six triggers.

**And the opposite risk is live too.** [F6]: under a strict reading of "any
high-risk surface the governing file names", plus uncertainty→full, doctrine and
template prose changes — Cairn's dominant change class, and the motivating worked
instance — may be fenced out. The clause could be safe and simultaneously
inapplicable to the work that prompted it.

So: tight enough that a contract-touching change should not slip in *by
argument*; not yet tight enough that one can slip in *by silence*. That is a
one-clause gap, not a design fault, and the direction of the change is right.

### Can this proposal archive?

**Not yet.** [F1] is an accepted term of the Decision with no landed home, and
two plans are executing under it right now. Archive once [F1] is dispositioned
— either the sentence lands in `doctrine/plans.md` + both `AGENTS.md` copies, or
the Maintainer records an explicit `wontfix` that the existing deviation rule is
deemed sufficient. [F2] and [F3] are guard-integrity defects that should be
dispositioned before archive (both are small test edits, neither changes
doctrine). [F4]–[F7] are legitimate follow-ups and do not block.

### Coverage

**Covered, with falsifiable citations**: the four §6 checks (fence wording on all
five surfaces; twin parallelism via L1/L3 red and L2 green; trigger identity read
at `dual-review.md:212-219` / `plans.md:340-347`; `review-efficient-lifecycle`
untouched per empty `git log` on that path); 35 self-chosen mutations with
per-mutation results (15 red, 12 defeated, 2 green-by-design, 6 no-op/anchor
misses re-aimed and re-run); guard node count reproduced independently (13 → 36);
neutrality/redundancy differenced across the commit boundary rather than
re-reported; complete deletion enumeration for scope fidelity; every pinned token
re-checked individually; cross-document sweep including the two `lifecycle_planner.py`
twins and the planner's record-parsing surface; claim-checker trigger verified by
injection rather than assumed; sweep lenses 1 (claims), 4 (fail-closed), 5
(cross-document consistency), 6 (drift), 7 (lifecycle placement), 8 (scope), 9
(satisfier named on every finding).

**Not covered / low confidence**: (a) sweep lens 2 (production path exercised by
tests) and lens 3 (design completeness) are **N/A by declaration** — the guard
file's docstring states it does not parse filled verification records or select
tests, and I confirmed the planner has no such parser, so there is no production
path to exercise; (b) I did **not** clear a full `bootstrap/tests` run against
this commit — my isolated tree is not a git repository, so 18 failures + 18
errors appeared in `test_gate_preflight.py`, `test_oracle.py`,
`test_security_check.py`, `test_lifecycle_contract.py` and
`test_upgrade_module_additions.py`, all git-dependent and all harness artifacts;
I verified none of them are in `test_verification_boundaries.py` or any
doc/template-pinning test, but the broad result is **not** clean evidence and I
am not offering it as such; (c) I did not attempt to estimate how often bounded
mode will actually be claimed, so [F6]'s practical severity is judgement, not
measurement; (d) I did not review the two superseded proposals for whether their
own archived text should be annotated — no annotation convention exists in this
tree for cross-proposal supersession, so I raise it as an observation without a
finding.

### Sharpening -- Claude -- 2026-08-12

**Model**: Claude Opus 5 (`claude-opus-5`)

All three actionable findings accepted and fixed; F5-F7 dispositioned below.
Every one verified before acting.

**[F1] accept.** Confirmed: `grep` for the already-open-plan rule across all six
landed surfaces returned **nothing**. It is an accepted term in the Decision
("Already-open/executing plans preserve their written verification contracts
unless explicitly revised") and I implemented every other term while dropping
this one. It now lands in `AGENTS.md`, `templates/core/AGENTS.md` and
`doctrine/plans.md`, with the reason stated: doctrine acts immediately, templates
act prospectively, so an in-flight plan would otherwise get two answers about
its own evidence obligation.

**And the finding had a second half I found by testing the fix.** Having landed
the rule, I mutated it away — and the suite stayed green at 37 passed. The rule
was *text without a guard*, which is the same shape as F2 and F3. A parametrized
guard over the three governing surfaces now fires on its deletion.

**[F2] accept.** `assert len(FRESH_RUN_TRIGGERS) == 6` asserted the length of a
tuple literal living in the same test file, so no doctrine edit could ever fail
it — and §2 of the accepted revision rests an argument on exactly that guard.
The count is now parsed from `doctrine/dual-review.md` itself. Verified against
the reviewer's own defeating mutation: adding a seventh trigger to the doctrine
now fails.

**[F3] accept, and it is the one worth dwelling on.** The test read:

```python
text = _read(SELF_AGENTS).replace("trust-ceremony surface", "surface")
assert "trust-ceremony surface" not in " ".join(text.split())
```

It asserts a token is absent from text it has just removed it from. It never
calls the guard. It passes against an **empty file**. Its docstring says
*"Without this pair an always-passing token check would look correct"* — which
is precisely what it was.

I wrote it in the same commit in which I perturbation-tested five obligations
and reported all five red. The five were real; this one was theatre, and I did
not notice because I wrote the mutation and the assertion together and they
agreed with each other. Replaced with the mutate-then-assert-the-violation-
function pattern this file already used three times, plus an explicit floor
(`test_bounded_guard_is_not_satisfied_by_an_empty_file`) pinning the case the
old version silently sat below.

**[F4] wontfix, with the reason.** A record omitting `Boundary B mode` is
indistinguishable from a pre-change record — true, and deliberate: the rule is
prospective and F1's applicability sentence is what governs records written
before it. Making a missing field invalid would retroactively invalidate every
existing record.

**[F5-F7] wontfix.** No generality guard on the adopter *plan* template (the
`AGENTS.md` pair carries the one that matters, and the plan templates are
already slot-differentiated by construction); possible over-fencing of doctrine
prose (uncertainty resolving to `full` is the intended direction — over-fencing
costs a full run, under-fencing costs the assurance the clause trades on); slot
placement correct but unpinned.

**Verification.** 40 nodes, was 13 at the start of this work and 36 at
`8d9e351`. Mutations run for this Sharpening: a seventh trigger in the doctrine
(**fails**, was green); `AGENTS.md` truncated to empty (**7 fail**, was green);
the F1 rule deleted (**fails**, was green before the guard). `check_cairn` OK
(174 files); redundancy `fail=0`; neutrality `fail=93`, unchanged and
pre-existing; `claim_check` clean on all three edited surfaces.

**On the reviewer's caution**: the working-tree failure in
`test_scope_reduction_trap.py::test_the_two_planner_twins_stay_byte_identical`
is another agent's uncommitted planner edits. Confirmed independently — the
twins are byte-identical at `8d9e351` and at this commit.

