# v0.6 decision master — editing burden and nimbleness first

**Author**: Codex (Coordination)
**Model**: GPT-6 (exact runtime variant unavailable)
**Date**: 2026-10-28
**Status**: living
**Type**: living-reference
**Surfaces this would feed**: Maintainer decisions on the linked proposals; subsequent accepted plans; the v0.6 roadmap.

## Purpose and authority

One place to resume the v0.6 drain while the Maintainer is away. Start with
editing burden and nimbleness; preserve the release boundary: make existing
capabilities work in v0.6, add capabilities in v0.7. The
[roadmap](../PLANNING.md) remains the scope inventory and the proposal records
remain authoritative for their own status and contract. This master is a
briefing, not a Decision or a replacement board.

The Maintainer authorized proposal/plan work and delegation on October 28,
then asked for as much work as possible without decisions and a master for
later review. A general tendency to approve recommendations grants no specific
acceptance. No proposal is accepted by this document. Plans begin after the
proposal Decision; no agent pushes, publishes, changes repository settings or
closes issues under this drain.

## Decision batch

All five proposals have completed their required reviews and author responses
and are awaiting decision. No plan or implementation has begun. Consult
`python tools/board.py --maintainer` for the current declared waits.

| Item | Recommended next choice | Why / cost of being wrong |
|---|---|---|
| [Model floors](../proposals/2026-10-28-codex-model-floor-alignment.md) | Accept the reviewed floors and current Sol/Terra/Luna and Opus/Sonnet/Haiku assignment | Removes unnecessary model-cost escalation; an inadequate floor can miss defects, so retain independent review, security treatment and escalation |
| [Doctrine purpose and governing-text inventory](../proposals/2026-10-28-codex-governing-text-single-source.md) | Inventory first; choose routing at a Maintainer fence before moving or deleting rules | Avoids shortening files by hiding obligations from adopters; premature routing could preserve the wrong structure or lose rules |
| [Test trust boundary](../proposals/2026-10-28-codex-test-trust-boundary.md) | Accept narrower protection only with explicit acceptance of the recorded assurance loss | Removes routine test-edit ceremony debt; it deliberately gives up blanket freezing of ordinary pytest code that can influence other tests |
| [Ordinary test maintenance pilot](../proposals/2026-10-28-codex-ordinary-test-maintenance.md) | Accept the bounded pilot, conditional on the final protected roster leaving its file eligible | Reuse setup and preserve fault detection; eligibility must exclude protected files and helpers, and one pilot does not prove suite-wide speedup |
| [Change verification / issue #33](../proposals/2026-10-28-codex-scoped-change-verification.md) | Accept scoped change verification and separate tree certification, preserving prescribed ceremony checks | Avoids repeated per-change runs; integration regressions may appear later, and prescribed ceremony checks must remain |

Read the final author responses and Security Reviews in each artifact before
deciding. The trust-boundary choice stops blocking ordinary test deletion,
renaming and new skip markers at the manifest level; actual release-mode
skip/xfail/xpass refusal remains. Ordinary pytest code can still influence
protected execution. This loss needs an explicit Maintainer choice.

Suggested reading order: model floors; verification wording; test trust boundary;
ordinary test maintenance; governing-text inventory. The inventory can run in
parallel with accepted test work, but no rule relocates before its routing fence.
Final handoffs: `639196fe`, `a0ca1241`, `55bbbb25`, `98bed453`, `5111ca97` respectively.

## What the doctrine question means

Measured from [doctrine's index](../../doctrine/README.md), the
[documentation plan](../../docs/DOCUMENTATION_PLAN.md) and installer mappings:
`doctrine/` is published in Cairn's repository but is not copied into an
adopter's tree. Its stated purpose is explaining the invariant methodology and
its reasons. Installed operating files are intended to put that method into
practice; descriptive docs help people enter and use it.

That distinction does not itself justify every current boundary. Rules and
explanations repeat across the layers. Reading Cairn without installing it is also an intended adoption path, recorded
in the archived adopter-path-consolidation proposal. The inventory must
establish which content
needs a separate public reference, whether doctrine should remain separate
from docs, how installed references are reached, and how many places an actual
rule change requires editing. Preserve adopter access and semantics; do not
choose folder structure merely to reach a line-count target.

## Dependency order and next work

1. Decide the five reviewed proposals; their proposal-stage work is complete.
2. After acceptance, write plans and have fresh reviewers read them. The
   model-floor change can proceed separately; the doctrine audit can gather
   evidence before its routing fence.
3. Settle the test-protection boundary before renaming or deleting ordinary
   tests. Narrowing the byte glob alone leaves the existing dropped-node
   HOLDs in place.
4. Scope an ordinary test-family consolidation, starting with a measured
   behavior/fault inventory and repeated setup. Exclude the governing-text
   proposal's tests to avoid two owners editing them. Keep representative
   real entry-point checks. No line-ratio deletion quota.
5. Assess the recorded slow-suite evidence with scoped duration measurements;
   do not run another full suite merely to prepare a proposal. Parallel test
   runners and new dependencies remain separate choices, not assumed fixes.
6. Return to the remaining v0.6 roadmap corrections, including module discovery
   and first-use onboarding. They stay in v0.6; new adopter engineering guidance
   and the survey stay in v0.7.

## Open-issue triage

Read-only GitHub issue inventory on October 28 returned four open issues:

| Issue | Disposition for this drain |
|---|---|
| #31 — keep proposals/plans short | Already implemented and reviewed: commits `3ba6aba1`, `1f938bcc`, `06f32930`. Do not repeat the fix. Closure draft below |
| #32 — retired/unknown status advisories | Already implemented and reviewed: `a773e753`, `50b5fbdf`, `9bb423c2`. Do not repeat the fix. Closure draft below |
| #33 — scoped certification versus full-suite execution | Premise check found contradictory actionable clauses in the current templates. The linked change-verification proposal addresses them; `787c558e` only changes push wording |
| #19 — scientific deliverable/governance axes | Exploratory new capability and conditionally deferred in the roadmap. Keep outside this first v0.6 batch; no new axis is authorized |

Suggested closure text for #31: “The keep-it-short guidance is implemented in
the proposal and plan templates, with review and author response recorded in
3ba6aba1, 1f938bcc and 06f32930. Closing the delivered request; optional tooling
ideas are not claimed as implemented.”

Suggested closure text for #32: “The board and session tools now report active
retired or unknown statuses as advisories while retaining listings. The
implementation and follow-ups are recorded in a773e753 and 50b5fbdf, with
review at 9bb423c2. Closing the delivered request.”

These are drafts for the Maintainer, not posted comments or closure actions.

## Additional reproduced choice: handoff marker

Luna reproduced the mismatch in a scratch adopter history containing a
`Handoff:` commit: the default looked for `Goodnight` and printed fallback
history. However, `doctrine/session-routines.md` requires a handoff commit
without prescribing its subject, and the existing owner test expects
`Goodnight`. `tools/session.py` already offers `--handoff-marker`. No code was
changed: a global default change is a convention decision, not a demonstrated
restoration of the generic contract. Recommended immediate use in Cairn is
the existing explicit marker option; decide a canonical/compatible convention
before changing every adopter's default. The v0.6 roadmap item remains open.

## Work record and limits

Current default staffing follows the Maintainer's latest October 28 direction:

| Tier | OpenAI | Claude | Work |
|---|---|---|---|
| High | Sol | Opus | Strategy, premise/novel-design judgment, Security Reviews |
| Medium | Terra | Sonnet | Proposal/plan authoring and ordinary reviews |
| Low | Luna | Haiku | Implementation of reviewed plans, including high-risk/non-trivial chunks; trivial work and authorized Decision scribing |

No Astra or Fable by default. The remaining Astra subagent was stopped after
read-only work; completed reviews retain their true attribution and are not
repeated. The staffing proposal records this revised family assignment at
`639196fe`; it remains a proposal rather than a scribed Decision. Family names
were checked against [official OpenAI documentation](https://developers.openai.com/api/docs/guides/model-selection);
these local tier assignments are the Maintainer's choice, not benchmark results.
Decision scribing still needs unambiguous disposition and commit authorization.

This is the nimbleness-first batch, not a completed v0.6 release. Other roadmap
groups remain queued. No implementation, suite-consolidation outcome or new
scientific evidence is claimed. Proposal authors/reviewers own their records and commits. Claims,
links and applicable prose gates check this master; they do not verify the
engineering claims in the linked proposals. Do not mistake a populated board
for delivered functionality.
