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

The Maintainer authorized delegated work and continuous handoffs on October 28.
This briefing grants no approval: proposal Decisions and explicit plan fences
remain authoritative. Pushing, publishing, settings changes and issue closure
are not authorized.

## Accepted batch and execution order

All five proposals were accepted in committed Maintainer Decisions:
`63e315fa` (model floors), `f110d263` (verification), `cca436a9` (test trust),
`cea1299d` (test maintenance), and `439c7b34` (governing text).
The Maintainer then instructed: “Okay, go ahead with all five in the order you
deem most appropriate”. Opening each plan archived its accepted source unchanged.
Use `python tools/board.py` for current lifecycle status rather than treating
this briefing as another status board.

| Order | Plan | Accepted outcome and remaining constraint |
|---|---|---|
| 1 | [Model floors](../plans/archive/2026-10-28-model-floor-alignment.md) | Implemented and code-reviewed task floors and Cairn-only assignments, including Antigravity; certification/re-anchor pending |
| 2 | [Change verification / issue #33](../plans/2026-10-28-scoped-change-verification.md) | Implemented; split evidence covers 2,700 collected/executed nodes; independent example adjudication complete; code review holds closure for the required frozen-file ceremony |
| 3, parallel inventory | [Governing text](../plans/2026-10-28-governing-text-single-source.md) | Establish why each home exists and compare doctrine with docs/dev/rules; the Maintainer chooses routing before rule relocation/deletion |
| 4 | [Test trust boundary](../plans/2026-10-28-test-trust-boundary.md) | Exact protected roster requires Maintainer approval; root/re-anchor remains Maintainer-only; narrower assurance loss already accepted |
| 5 | [Ordinary test maintenance](../plans/2026-10-28-ordinary-test-maintenance.md) | Follows implemented trust boundary and board-file eligibility; references the test-practice strategy and updates the existing testing module |

The trust Decision explicitly accepts loss of blanket ordinary-test byte
protection and ordinary-node deletion/rename/new-marker HOLDs. Actual
release-mode skip/xfail/xpass refusal remains. Ordinary pytest code can still
influence protected execution; do not claim equivalent tamper resistance.
The ordinary test pilot stops for a scope decision if its file remains protected.

The approved testing-module update stays within existing maintenance practice;
new simulation guidance remains v0.7. No plan waives its recorded fence.

## Remaining Maintainer decisions and actions

I will carry reviews, fixes and handoffs forward without check-ins. The explicit
fences below remain; recommendations are prepared here before asking for a decision.

| Item | Recommendation / choice | Readiness |
|---|---|---|
| Governing-text routing | Put public explanation/reference under the proposed methodology home; retain complete duties in installed operating files and project-specific rules in `dev/rules/`. Alternative: retain the current split. Moving loses the familiar doctrine landmark and requires citation migration. | C1 semantic mapping and post-review refresh in progress; no relocation authorized |
| Exact protected-test roster | Approve the refreshed, source-bound roster before narrowing. Initial proposal: 90 protected Python paths, 51 ordinary test files; retain other existing protection. | Counts and hashes must be refreshed after verification review; initial counts are not approval targets |
| Test-maintenance pilot scope | Separately authorize extracting the two ordinary clusters into an ordinary file while retaining security cases and helpers. Alternative: retain the protected file and pause the pilot. | Initial classification protects the board file; extraction adds review and ceremony work and is not authorized |
| Frozen-file ceremony / trust installation | Perform the applicable existing Maintainer ceremony on the final reviewed tree; keep certification and root changes explicit. | Verification code review records this as an unmet required check; trust-boundary installation comes after roster approval and implementation |

Proposed path: `docs/methodology/` (not yet created).

These are recommendations and pending actions, not scribed Decisions. Exact
roster evidence and final review dispositions will replace provisional facts.

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

## Work sequence

Fresh ordinary and Security plan reviews precede implementation where required.
Luna executes reviewed plans; Terra independently reviews code. Sol handles
Security Reviews and new strategy or premise judgments.

Serialize changes to shared governing files. Governing-text inventory can run
alongside model/verification work because it gathers evidence rather than moving
rules. Settle the test-protection boundary before ordinary test deletion or
renaming; narrowing only the byte glob would leave collection HOLDs in place.
Use scoped measurements for the pilot; a full-suite speedup is measured only at
the next authorized whole-tree integration run, not by creating another broad run.

Maintain the existing release and certification ceremonies. Root changes,
re-anchors and routing decisions remain the Maintainer's actions; pushing,
publishing, issue closure and repository settings changes are not authorized.
Other v0.6 groups, including module discovery and onboarding, remain in the
[roadmap](../PLANNING.md). The five-plan batch does not claim to finish v0.6.

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

Antigravity maps high/medium/low to Argon/Pro/Flash under Decision `63e315fa`.
All three vendor mappings are Cairn-local assignments; shipped tiers remain
generic. No Astra or Fable by default. The remaining Astra subagent was stopped after
read-only work; completed reviews retain their true attribution and are not
repeated. The staffing Decision at `63e315fa` now authorizes the local assignments and
the reviewed task floors. These local assignments are the Maintainer's choice, not benchmark results.
Decision scribing still needs unambiguous disposition and commit authorization.

Other v0.6 groups remain queued. Plans and their verification records own
implementation claims; no suite-wide speedup or new scientific evidence is
claimed. Prose gates check this briefing, not its linked engineering evidence.
