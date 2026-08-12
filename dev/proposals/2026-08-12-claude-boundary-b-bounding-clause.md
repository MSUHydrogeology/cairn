# Boundary B needs the bounding clause Boundary A already has

**Author**: Claude (Strategy)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-12
**Status**: proposed
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
