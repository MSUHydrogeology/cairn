<!-- Origin: authored 2026-05-20 in modflow_tools' dev/strategy/ and migrated
     2026-06-12; see dev/strategy/MIGRATION.md. Vantage adaptation completed
     and cut to its load-bearing core 2026-08-11. -->

# What to measure while building, and what never to measure

**Author**: Claude (Strategy)
**Date**: 2026-05-20; cut to current scope 2026-08-11
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

## What is measured now

`tools/lifecycle_metrics.py` walks the proposal and plan corpora and emits
rows. Sorted by whether the column survives the principle:

**Structural — keep.** Transitions and their dates; time between stages
(`days_*`, `hours_*`, `stage_timestamp_reliability`); declared review tier;
`cross_agent_type_review`; `revised`; review-round counts; `response_models`.
These are events; writing more cannot inflate them.

**Prose-scraped — retire.** `total_findings`, `findings_p1/p2/p3`,
`review_yield_*`. A finding count rewards splitting one finding into three,
which is the cheapest way for an agent to look thorough. These are this note's
historical showcase numbers and they are the wrong kind.

**Cairn's own corpus, 2026-08-11** — the honest current state, not a trend to
track: 49 proposals (45 accepted, **4 superseded**, 0 rejected), 38 plans, 76%
reviewed cross-agent-type, median time-to-decision 0 days. The four
supersessions carry the weight: they are the only hard evidence that
adversarial review blocks work *as written*, which a zero-rejection count
cannot show on its own.

### Two live items

* **The time series is not in the record.** `dev/measurement/snapshots/` holds
  real snapshots and is **untracked — not gitignored, merely uncommitted**
  (unlike `dev/intents.jsonl`, ignored deliberately). Decide: commit them, or
  ignore them on purpose. Under emit-at-transition the question mostly
  dissolves.
* **A fixed defect worth keeping as a lesson.** Both review-round regexes
  required an H3 heading while `dev/plans/_template.md` prescribes dated H2
  passes, so `plan_review_rounds` counted 2 across the whole corpus and
  `code_review_rounds` read 0 for 28 of 38 plans. Fixed 2026-08-11 to
  `#{2,3}`. The lesson is not the regex: **two components independently parsed
  the same prose for the same fact and disagreed.** An emitted event has one
  writer.

## The direction: emit at the transition

The corpus walk should become a one-time backfill tool, not the running
instrument. Metrics should be **emitted when the event happens**, by the
component that already knows — the lifecycle planner gates transitions, so it
is the natural emission point — and appended to a durable record as data.

What that buys: a number written once cannot be rewritten by a later tool
change; format evolution stops being measurement discontinuity; one writer per
fact.

What it costs, plainly: you give up re-deriving history under a better
definition. A recorded metric is frozen at the definition of its day. That is
the right trade, and it needs **schema versioning on emitted records** so a
definition change adds a field rather than rewriting the past.

Three constraints keep this from becoming ceremony:

* **A field, not a workflow.** If the writer already knows the answer, capture
  it there; do not add a step.
* **Transparent by construction.** Data lives where the event lives, in the
  committed record, readable by whoever it concerns. No side channel, no
  telemetry, nothing collected that was not already being written.
* **Analysis registered before the data exists** — outcome, covariates, and an
  explicit INCONCLUSIVE branch. Easier prospectively, because no results exist
  yet to fit to.

## The Measurement Compact

Operative, and shipped to adopters that install the module — its home is
`templates/modules/default-on/lifecycle-metrics.md`, **not** `AGENTS.md`, so it
binds only adopters who select the module. Whether that scope is right is open.

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
adopter. Per-project efficacy-data collection is a `0.5+` horizon item in
`dev/PLANNING.md`, gated on that trust architecture landing first.

## Open questions

1. **Retire the prose-scraped columns, or keep them with a warning?**
   *(Recommended: retire. A metric that rewards splitting findings is not
   fixable by a caveat.)*
2. **Snapshots: commit or ignore?** *(Recommended: ignore, and move to
   emit-at-transition rather than committing re-derivations.)*
3. **Does the Compact bind all adopters, or only module installers?** *(Open —
   moving it to `AGENTS.md` would bind everyone. A scope decision, not an
   editorial one.)*
