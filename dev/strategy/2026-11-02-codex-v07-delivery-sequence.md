# v0.7 delivery sequence and closeout

**Author**: Codex / Strategy
**Model**: Codex (runtime model identifier unavailable)
**Date**: 2026-11-02
**Status**: draft
**Type**: product-strategy
**Surfaces this would feed**: v0.7 proposals, their implementation plans and `dev/PLANNING.md`; temporary release coordination, not a standing framework.

## The question / felt gap

Deliver better engineering, suite consolidation and cost measurement without
building three competing collectors or repeatedly editing the same guidance.
This is the requested "super plan" in thin form: order, ownership and shared
verification. It grants no implementation authority, changes no review floor
and cannot waive an accepted outcome.

## Method

Read the board and cited source strategies at `5c9129a5`, the current proposal
and strategy templates, testing/architecture modules, tier selector and their
test homes. Drafted three proposals below; the meter is already accepted.
Historical runtime and duplication counts remain attributed source reports,
not fresh measurements here. No implementation trial or suite ran for this note.

The release session is certifying v0.6. Further authoring uses the task-specific
separate `0.7-dev` checkout, leaving its candidate untouched; this does not
change the standing branch policy. Ordinary test moves follow the installed
v0.6 narrowed baseline, not a demand to reopen its release candidate.

## Findings

Three overlaps matter: suite setup and fault-oriented tests; measurement and
pulse reporting; architecture discovery and visual review. Grouping these
edits saves work without merging their promises or creating a program gate.

## Recommendation

Use the following order. Independent work may proceed together; a wave is
not a required wait for unrelated items. All sixteen feature rows remain.

| Order | Work | Delivery relationship |
|---|---|---|
| A1 | Suite consolidation | [Plan](../plans/2026-11-04-suite-consolidation.md) and [accepted proposal](../proposals/archive/2026-11-02-codex-suite-consolidation.md); rank setup costs first, preserve detecting checks. |
| A2 | Metered cost | [Accepted proposal](../proposals/archive/2026-10-30-claude-metered-cost.md); [plan](../plans/2026-11-04-metered-cost.md), retaining its security obligations. |
| A3 | Lightweight team measurement | Reconcile uncovered pulse, side-file attribution, product bucketing and measurement archive with A2; one collection/reporting design. |
| A4 | Tests that catch real faults | [Testing proposal](../proposals/archive/2026-11-02-codex-fault-centered-testing.md); coordinate with A1, do not equate fewer tests with better evidence. |
| A5 | Testable acceptance criteria | Same testing proposal; one template editing window. |
| B1 | Local environment notes | Independent small proposal; local discovery without committed credentials. |
| B2 | Upgrade growth | One-session Git comparison and refusal-rule proposal before choosing a replacement direction. No v0.7 replacement promise. |
| B3 | Reading old code cheaply | [Architecture/reuse proposal](../proposals/archive/2026-11-02-codex-architecture-and-reuse.md); [plan](../plans/2026-11-05-architecture-and-reuse.md); shared map, neighbors and critical homes. |
| B4 | Architecture for legacy and new systems | Same proposal and existing rubric; reuse A4's testing guidance. |
| B5 | Visual codebase review | Same proposal's bounded pilot; all four questions, not a finished interface. |
| B6 | Sterile Git helper | Own high-risk proposal; coordinate actual callers with B2, not a second runner or presumed engine rewrite. |
| C1 | Plain Language refinements | Small coordinated proposal covering rules 2, 5, 13 and 17 (scientific prose and technical-documentation fit); retain January 2027 evaluation. |
| C2 | Allow comments into configuration | Establish config contract before C3's scan edits. |
| C3 | No live finding-ID scan | Preserve its board outcome; reuse the existing scanner and C2's configuration. |
| C4 | Single file for routine multi-step work | First separate the existing light lane from the remaining standard-lane gap. |
| C5 | Ceremony return on attention | Reconcile existing cost comparison, follow-up accounting and archive judgment; add no duplicate accounting. |

Keep Stid interview/testimonial, independent adopter feedback, hosted tracker
automation and adopter-roadmap execution in v0.8. Consent and lifecycle gates
remain; these items are deferred, not discarded.

### Shared surfaces and checks

Give one writer each editing window for the plan-template pair, testing module,
architecture module/collector, measurement output and scaffold registry.
Metering owns usage ingestion; `tools/gauge.py` remains the pulse/report home.
The visual pilot consumes shared history/diff data, not another collector.
Local-notes discovery must reconcile with session tooling, not edit it blindly.

Git-backed map/pilot inspection depends on B6's shared sterile Git boundary;
without it the affected view is incomplete, not approved for unsafe fallback.
Filesystem-only mapping and rubric work can proceed independently. The pilot
remains an owed outcome, not an indefinite deferral behind that dependency.

Use `tools/test_tiers.py for <paths>` and map promises to owning/consumer tests.
Keep mutable repositories and environments fresh; share only immutable setup.
Add tests for plausible uncovered faults, not every sentence.
Coordinate final combined ranges where the same tests genuinely cover both
changes. Evidence is reusable only for unchanged covered bytes, inputs,
environment and consumers; changed material needs its affected checks again.
Separate review obligations still stand.

Review fixes receive their required targeted look; final integration follows
review on a clean committed range. Preserve scientific, security and release
checks. No new full-suite trigger for proposals, revisions, mutations or this
coordination note: use the existing authorized certification points.
Link child evidence rather than duplicate it in a program ledger.

## Retirement ownership

The architecture/reuse proposal explicitly assigns one grouped closeout row to
the v0.7 release-closeout agent before its implementation plan archives.
That row survives early child-plan closure. It covers this note and the source
strategies below; it is not one follow-up per document.

Retirement means lasting instructions/results have a durable home, all scoped
work is delivered or explicitly dispositioned, the note is marked archived
and moved with owned assets, and live links are repaired. An unfinished item
needs its exact live home and reason; a vague future promise is insufficient.
A changed scope still needs the Maintainer's permission. Do not archive now.

| Note | Retire when |
|---|---|
| **This delivery sequence** | v0.7 ships, or its direction is cancelled/superseded, and every row has an outcome or explicit live owner/home. |
| [Judicious testing](2026-10-27-antigravity-judicious-testing-and-simulation-verification.md) | Guidance, narrowed baseline, folder moves, consolidation, runtime evidence and growth reporting are delivered/dispositioned. |
| [Outside practices](2026-11-02-claude-outside-practices-for-better-software.md) | Testing, acceptance and architecture recommendations all have outcomes; testing alone cannot close it. |
| [Architecture growth](2026-10-30-claude-architecture-growth.md) | Map, neighbors, critical homes and release assessment have outcomes; ongoing guidance resides in the module/rubric. |
| [Adopter engineering](2026-10-27-codex-adopter-engineering-practices.md) | Legacy/new/mixed guidance, examples and testing connection are resolved, including functional scope versus execution-cost distinctions. |
| [Agent-scale visual review](2026-10-28-codex-review-at-agent-scale.md) | Pilot findings address all four views; any further interface has an explicit live home. A collector alone is insufficient. |
| [Team measurement](2026-10-27-antigravity-lightweight-team-measurement.md) | Usage/size/pass/model reports, side-file attribution, product classification and measurement archive are covered. |
| [Upgrade growth](2026-10-30-claude-upgrade-growth.md) | Refusal rule and bounded trial/go-no-go are resolved; any replacement has a named later home. |
| [Nimbleness](2026-08-21-claude-nimbleness-recovery.md) | All five recommendations are reconciled with delivered rules or explicit dispositions, including compression/freezing, single-artifact work, attention and cleanup. Retire its living role first; do not silently revive historical numeric targets. |
| [Scientific writing](2026-10-27-antigravity-plain-language-and-scientific-writing.md) | Packaging/evidence-home recommendations as well as three wording gaps are resolved; keep the later evaluation live elsewhere. |
| [Security strategy](2026-08-05-codex-security-strategy.md) | **Retain while its broad residual register remains active.** Resolve the Git-helper item in place; it does not retire the whole strategy. |

Notes serving v0.8 work stay live until their own outcomes are settled.

## Options and falsification

Doing nothing avoids this note but repeats coordination. A formal parent plan
would add a lifecycle before the children are accepted. Recommend this temporary
map. It is wrong if it creates another approval queue, repeats evidence or
lets grouping drop source outcomes.

## Open questions

Child proposals still require their Decisions. The bounded upgrade trial and
visual pilot determine later direction; neither result is presumed.
No extra Maintainer choices are needed merely to order independent drafting.

## Fold-up note

Carry operational instructions into their proper modules and records. Archive
this map at its stated trigger, not as a perpetual release-management document.

## Authoring checks

On an archived copy of `f85a4210`, Python 3.13.13: scoped `check_cairn`
passed for the six changed documents; neutrality and redundancy reported
zero failures. Board-scope taxonomy checks passed: 10 passed, 79 deselected
in 0.06 seconds. `tools/board.py --json` parsed the three proposals as
awaiting-review. All sixteen original feature work cells/source records
were retained; the v0.8 section was unchanged. Both working checkouts were
clean after checking.

The tier selector also named installer/upgrade families that mention these
filenames; those fixtures do not read the changed roadmap/changelog contents
and were not run. No shipped template or code changed. No full suite or
implementation experiment ran; eight external links were not probed.
Check window: approximately 2 minutes including inspection; tokens unknown.

