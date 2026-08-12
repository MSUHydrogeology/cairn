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
