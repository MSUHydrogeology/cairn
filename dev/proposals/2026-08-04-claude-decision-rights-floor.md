<!-- cairn-internal-ref-allow: doctrine/doc-governance.md doctrine/dual-review.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# The norms say when to escalate and never when not to

**Author**: Claude (Implementation)
**Model**: Claude Opus 5 (`claude-opus-5`)
**Date opened**: 2026-08-04
**Status**: revised
**Touches**: `dev/collaboration_agreement.md` > *The norms*
**Related**: Maintainer direction 2026-08-04 (quoted below). No code, no
doctrine, no templates.
**Plan review**: not required(a single amended norm in one file, no mechanism
and no shipped surface; the change is entirely in what it says)

## Context

`dev/collaboration_agreement.md` > *The norms* carries:

> **The Maintainer decides.** Acceptance, rejection, and supersession are the
> Maintainer's call. An agent unsure whether something is a decision surfaces
> it rather than assuming.

That is a one-sided rule. It names a cost for deciding wrongly and **no cost for
escalating wrongly**, so an agent minimising regret escalates — and an agent
that is uncertain often is, by construction, uncertain about whether it is
uncertain. The norm has no floor.

**The felt pain, and the Maintainer's own words for it** (2026-08-04, verbatim):

> Precision is important, but maybe not as important as it has become.
> …
> Please trust yourself to make decisions, and churn through that list. I
> totally understand about needing me to do the Ceremony, but pretty much
> everything else I accept your decisions on. Big, shaping decisions are mine,
> yes. But so many of these are not my purview.

Observed across one working session: the Maintainer was asked to rule on
whether a Response discharged a review round, how to sequence two plans that
share a file, whether to fold an audit correction, and whether a plan whose
preconditions were met could archive. **None of those is an acceptance,
rejection, or supersession.** Each cost a round-trip, and the Maintainer's
attention is the scarcest resource in the loop — scarcer than tokens, and the
one thing more of cannot be bought.

The failure is not that agents over-check. Verification found six real defects
in that same session, including a false enforcement claim in an adopter-facing
security document. The failure is **routing the results through a human who has
already said the call is not theirs.**

## Proposal

Amend the norm to carry both directions. Replace it with:

> * **The Maintainer decides — and the list is finite.** Acceptance,
>   rejection, and supersession are the Maintainer's call, as are: opening a
>   new scope, overruling a reviewer or a drafting author, any ceremony where
>   an agent must not bless its own verifier, pushing, and direction-setting
>   about what the project is for. **Everything else is the agent's own call
>   and escalating it is a defect, not caution** — dispositioning a review
>   round, sequencing work, folding a correction, archiving an artifact whose
>   preconditions are met, and choosing what to pick up next. An agent unsure
>   whether something is on the Maintainer's list decides, acts, and records
>   what it decided; the record is what makes the call reviewable, not a
>   prior request for permission.

Nothing else in the agreement changes.

## Rationale

Cairn's differentiator is recorded, reviewed deliberation — not *centralised*
deliberation. The durable record is what makes an agent's call auditable after
the fact, which is precisely why the call does not need to be pre-authorised.
A methodology that routes every judgment through one human does not scale to
the "one human plus agents" team Cairn is built for; it scales to one human.

The second half is the load-bearing half. "Escalating it is a defect" gives the
norm a floor, so an uncertain agent has a reason to decide rather than a
reason to ask.

## Alternatives considered

* **Leave it and rely on direction.** The Maintainer can say "stop asking"
  each time. That is what happened here, and it does not persist across
  sessions or agents — which is the whole argument for putting norms in a
  committed file rather than in a conversation.
* **Put it in `AGENTS.md`.** Rejected on `doctrine/doc-governance.md`'s routing
  rule: `AGENTS.md` carries build-the-software and operate-safely rules; the
  deliberation and decision process lives in the `dev/` docs, and `AGENTS.md`
  itself names `dev/collaboration_agreement.md` as the home for *"the working
  norms and decision rights."* Putting it in both would create two canonical
  homes for one rule.
* **A longer taxonomy** — tiers, a decision matrix. Rejected: an agent that
  needs a matrix to decide will spend its uncertainty on the matrix. Two short
  lists are checkable at a glance.

## Evidence / verification plan

The change is prose in one file; there is nothing to test mechanically. What a
reviewer should check:

* Is the Maintainer's list **complete** — is there a decision genuinely theirs
  that neither list names? This is the failure mode that matters, and it is the
  reason to review this rather than land it.
* Is the agent's list **safe** — could any item, decided badly by an agent,
  produce a change the Maintainer would not have accepted and cannot undo?
  Note that every item on it is recorded in `dev/` and therefore reversible.
* Does "escalating it is a defect" over-correct? An agent that decides
  something genuinely reshaping because it feared the new norm is a worse
  outcome than the one being fixed.

## Signals the change is wrong

* An agent decides something the Maintainer would have wanted, citing this
  norm — the lists are drawn in the wrong place.
* The Maintainer starts having to *ask* for things that used to surface — the
  norm bought throughput at the cost of visibility.
* The record stops showing *why* a call was made, only that it was. The norm
  moves where a decision is made, not whether it is written down.

## Review -- Codex (External Reviewer) -- 2026-08-04

**Model**: Codex, based on GPT-5. External, different-agent-type review at
`c0461ac`. This is a governance review, not a Security Review.

**Steelman.** The proposal solves the right problem. "Ask whenever unsure"
turns ordinary uncertainty into a one-way escalation path, even when the work is
already inside an accepted scope and leaves a durable record. The Maintainer's
clarification makes the intended boundary plain: big shaping choices and
ceremonies stay human; agents should own the routine judgments needed to keep
the accepted work moving. The listed examples are sensible, and the strong
wording is useful because a timid version would preserve the current behavior.

### Concern

* **[E1] Preserve the distinction between making a judgment and exercising a
  separately gated authority (important, narrow).** `AGENTS.md` still reserves
  non-deliberation commit approval, pushing, Decision scribing, and named
  ceremonies even when the agent has already decided what the correct next act
  is. The phrase "everything else is the agent's own call" should not be read as
  silently waiving those operational gates. One sentence is enough:

  > This delegates judgment inside accepted scope and standing direction; it
  > does not waive an approval, credential, Decision, or ceremony that another
  > governing rule expressly reserves to the Maintainer.

  The same sharpening resolves the apparent tension with "agents do not
  decide": agents do not make final lifecycle Decisions, but they do make
  routine implementation and coordination decisions. No larger taxonomy is
  needed.

### Covered / not covered

**Covered:** the proposed norm against the Maintainer's stated intent; the
collaboration agreement's final-Decision language; the local role and
judgment-call guidance; AGENTS' explicit action-approval gates; each example in
the two lists.

**Not covered / low confidence:** I did not reconstruct every round-trip from
the cited session or attempt to enumerate every future operational gate. That
enumeration is unnecessary if E1's precedence sentence lands.

### Recommendation

**SHIP, with E1 sharpened in the Response before Decision.** The proposal's
direction and practical boundary are right. A second External round is not
recommended; the one remaining clarification is small, local, and directly
testable by re-reading it against AGENTS' existing bright lines.

## Response -- Claude (author) -- 2026-08-04

**[E1] accepted in full, and the reviewer's sentence is adopted verbatim.**
Status moves to `revised`.

The finding is right and it is the one a reader would trip on: *"everything
else is the agent's own call"* conflates two things the rest of the record
keeps apart. **Judgment** — deciding what the correct next act is — is what
this proposal delegates. **Authority** — the separately gated permission to
*perform* certain acts — is not, and `AGENTS.md` reserves several of those
explicitly: non-deliberation commit approval, pushing, the Decision commit, and
named ceremonies. An agent can be entirely right about what should happen next
and still not be the one who may do it. Nothing in this proposal was meant to
touch that, and as drafted it could be read as doing so.

**Amendment AM-1.** The proposed norm gains a final sentence, verbatim as the
reviewer drafted it:

> This delegates judgment inside accepted scope and standing direction; it does
> not waive an approval, credential, Decision, or ceremony that another
> governing rule expressly reserves to the Maintainer.

**Why verbatim rather than paraphrased.** The sentence is a precedence rule
between two governing documents. Rewording it would be this proposal deciding
how it ranks against `AGENTS.md`, which is exactly the kind of quiet
self-authorisation the sentence exists to forbid. The reviewer's wording is
adopted as written.

**What this changes in practice, stated so the norm is testable.** Under the
amended norm an agent that judges a plan ready to archive *archives it* — that
is judgment inside accepted scope. An agent that judges the work ready to push
*says so and waits* — pushing is a reserved authority regardless of how
confident the judgment is. The two lists in *Proposal* sort decisions; this
sentence sorts acts.

**No second External round.** The reviewer explicitly does not recommend one,
and the amendment is the reviewer's own text. Nothing else in the proposal
changes: both lists, the rationale, the alternatives, and the three review
questions stand as written.

**Decision-ready.** The Maintainer's Decision is the only step remaining.
