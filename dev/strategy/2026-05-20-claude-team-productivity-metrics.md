<!-- Origin: authored 2026-05-20 in modflow_tools' dev/strategy/ and migrated
     2026-06-12; see dev/strategy/MIGRATION.md. Vantage adaptation completed
     and cut to its load-bearing core 2026-08-11. -->

# What to measure while building, and what never to measure

**Author**: Claude (Strategy)
**Date**: 2026-05-20; cut to current scope 2026-08-11; revised to the
post-sweep gauge posture 2026-08-26
**Status**: living
**Type**: living-reference
**Audience**: the Maintainer and collaborating agents; secondarily an adopter
deciding what a human + AI team should instrument

## Purpose and the one principle

Cairn's `dev/` tree exists to **build software fast and well**. It is
scaffolding, not output. A measurement layer that makes the scaffolding grow
has inverted its purpose.

That gives the single principle this note exists to hold:

> **Measure structural events as they occur. Never measure prose. Any metric
> that rewards writing more is a defect to remove, not a signal to tune.**

A metric scraped from written text makes the text the optimization target.
Longer commit bodies, finer-split findings, blow-by-blow plan narration — the
numbers rise and the record degrades. The record *is* the product, so that
trades the asset for the gauge.

The corollary about history: **the archive records what was done; it is not a
dataset to mine.** Re-deriving metrics from past prose freezes the format
(every improvement to how work is written becomes a measurement
discontinuity), invites retroactive reinterpretation, and quietly pressures the
team against evolving its own practice. Human + AI development is moving fast.
Measure forward.

## What is measured, after the refocus (revised 2026-08-26)

The instrument this section previously described — `tools/lifecycle_metrics.py`
and the shipped `lifecycle-metrics` module, a corpus walker re-deriving facts
from proposal and plan prose — **is removed by the subtraction sweep**
(Maintainer decision, 2026-08-26, recorded as a scope-delta in the
`subtraction-sweep` plan). The removal is this note's own principle applied to
its own instrument: the walker parsed prose to reconstruct facts the commit
discipline already records structurally, and it parses a grammar the refocus's
constitution rewrite replaces.

What carries productivity measurement now, in three layers:

* **The gauge classifier** (the sweep's order-3 replacement, ~80 lines):
  re-derives the takeover table — weekly lines of dev / machinery / product /
  security — from `git log --numstat`. This is the number that caught the
  2026-08 drift, and it never came from the metrics layer.
* **Git as the event log.** One commit per lifecycle transition means every
  open, review, response, and decision is already a timestamped, authored,
  structural event with **one writer per fact** — which is all the retired
  emit-at-transition direction was asking for. Time-to-decision,
  cross-agent-type review share, and round counts are one-line queries run
  when a question actually arises, not columns maintained in advance.
* **The mission metrics, deliberately toolless** (nimbleness-recovery note,
  3.3): adopter issue → shipped fix ≤ 2 sessions; new adopter → first
  reviewed commit ≤ 1 hour; median artifact ≤ 150 lines; science-commit
  share in `modflow_tools` > 50% — monthly-ish glances, plus the one-line
  `Return:` verdict at each archive.

**Dated snapshot, 2026-08-11** (kept as history, not a trend to track): 49
proposals (45 accepted, **4 superseded**, 0 rejected), 38 plans, 76% reviewed
cross-agent-type, median time-to-decision 0 days. The four supersessions carry
the weight: they are the only hard evidence that adversarial review blocks
work *as written*, which a zero-rejection count cannot show on its own.

**A defect worth keeping as the removal's epitaph.** Both of the walker's
review-round regexes required an H3 heading while the plan template prescribed
dated H2 passes, so `plan_review_rounds` counted 2 across the whole corpus and
`code_review_rounds` read 0 for 28 of 38 plans — fixed 2026-08-11, but the
lesson stands: **two components independently parsed the same prose for the
same fact and disagreed.** A structural event has one writer; git's is the
one that remains.

## Constraints on any future collection

The emit-at-transition direction is retired with its emission point (the
lifecycle planner is removed by the same sweep), and git's transition commits
already deliver what it promised. If a future proposal adds collection beyond
the gauges, three constraints from that direction still bind:

* **A field, not a workflow.** If the writer already knows the answer, capture
  it there; do not add a step.
* **Transparent by construction.** Data lives where the event lives, in the
  committed record, readable by whoever it concerns. No side channel, no
  telemetry, nothing collected that was not already being written.
* **Analysis registered before the data exists** — outcome, covariates, and an
  explicit INCONCLUSIVE branch. Easier prospectively, because no results exist
  yet to fit to.

## The Measurement Compact

Operative. Its shipped home (the module doc) is removed with the module, so
as of 2026-08-26 the Compact lives **here**, binding how Cairn — and any
adopter who reads this note — holds the gauges. Nothing about retiring the
instrument retires the commitments; a gauge glanced at monthly can be misused
in the same five ways a column could.

1. **Metrics serve system learning, not member punishment.**
2. **No single composite score.**
3. **No role- or tier-confounded metric is read as capability proof.**
4. **No cross-team generality from a single corpus.**
5. **Internal-diagnostic posture, not external-marketing posture** — any
   externally-published artifact derived from them is a separate, gated act.

Enforcement is two-tier: an externally-published artifact derived from
per-member or per-tier surfaces needs an explicit Maintainer decision; internal
reading is normative-only. A contract test scans for the most mechanical Tier-1
violation pattern. The other four commitments rest on discipline, and this note
should not imply otherwise.

**Settle one application before any new collection starts.** A file-attributed
review finding would link *a file* to *a problem* to *whoever found it* — finer
than anything kept today. Say in advance that it is not a reviewer-performance
surface, and keep per-reviewer aggregation out of the declared analysis.
Retrofitting that constraint is the harder direction.

## Grounding, and the cautions that bind

Two anchors do real work. **SPACE** (Forsgren, Storey, Maddila, Zimmermann,
Houck & Butler 2021, *ACM Queue* 19(1)) establishes that productivity is
multidimensional and no single number captures it — the basis for commitment 2.
**Goodhart's law**, applied to agents, grounds the principle above: an agent
optimizes a stated criterion more literally than a human. *Evidence status:
first-principles reasoning, not a measured magnitude in a human + AI team.
A design posture, not a finding.*

Three cautions survive:

1. **Small N.** 49 proposals support descriptive narrative, not statistical
   inference. Report direction, not effect size.
2. **Survivorship.** The corpus is what got written; work that skipped the
   lifecycle is invisible. Revert events and incident logs are the
   counter-signal.
3. **Measurement-boundary discontinuities.** When a definition or an extractor
   changes, values either side are not comparable. Record the boundary rather
   than smoothing it.

**No-telemetry posture**, unchanged and load-bearing: data stays local, no
auto-upload, no central server, no implicit consent, and it leaves with the
adopter. Any future per-project efficacy-data collection stays gated on that
trust architecture landing first.

## Open questions — all three closed (2026-08-26)

1. **Prose-scraped columns**: resolved past the recommendation — the whole
   instrument retires, columns of both kinds with it. The principle that
   condemned finding counts stands on its own and now guards the gauges.
2. **Snapshots**: the takeover table, carried in strategy notes with `as_of`
   dates, is the committed dated snapshot; the gauge classifier re-derives it
   on demand. Working CSVs under `dev/measurement/snapshots/` remain
   uncommitted scratch, kept or deleted freely.
3. **Compact scope**: dissolved — with the module gone there are no module
   installers to distinguish. The Compact binds through this note; whether the
   rewritten collaboration doctrine carries a one-line pointer to it is that
   rewrite's call, not a new obligation this note creates.
