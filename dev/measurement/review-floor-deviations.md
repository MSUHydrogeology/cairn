<!-- cairn-internal-ref-allow: doctrine/rationale.md doctrine/dual-review.md doctrine/plans.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Review-floor deviations -- incident log

**Purpose**: records a review, or a stated plan-review requirement, that
fell short of its `doctrine/dual-review.md` structural-independence floor
without a waiver recorded at the time. Established 2026-07-13 (Part B of
the `review-record-integrity` proposal/plan) with two retroactively-logged
2026-06-12 entries from the showcase arc's first self-hosted proposal; the
full provenance narrative lives in this proposal's implementing plan's
"Showcase-arc provenance record" section.

**Rate-limit gate connection**: this tracker is the parse target for the
**adaptive-doctrine rate-limit gate** specified at `doctrine/rationale.md` >
"Adaptive-doctrine rate-limit gate." The gate's "≥2 incidents of the same
shape in a rolling window" trigger operates on this table's `Impact =
occurred` rows.

**Rolling window**: 14 days.

## What counts

* **Class name** -- `review-floor-deviation`: a completed review that did
  not meet its doctrine floor (e.g., a same-session read where
  `doctrine/dual-review.md:46` requires fresh-session for Internal), or a
  proposal/plan's stated `Plan review: required(<tier>)` line that the
  Decision never explicitly addressed or waived.
* **Criteria for "same shape" recurrence** -- two entries are the same
  shape if they concern the same class of doctrine floor (the Internal
  fresh-session requirement, or a stated-but-unaddressed plan-review
  requirement) being missed without a recorded waiver, regardless of which
  proposal or plan they occurred in.
* **What does NOT count** -- a review or plan-review explicitly waived on
  the record at the time (a Maintainer note accepting a lighter tier, with
  rationale) is a documented exception, not a deviation; a review that
  meets its floor is not a deviation.

**Impact value note (a documented local extension).** Beyond the three
values `dev/modules/incident_log_template.md` documents (`occurred` /
`prevented` / `non-conflict`), this tracker also uses **`historical`** —
for entries logged retroactively (dated before this tracker existed) that
must be recorded for the record's integrity but must never count toward
the rate-limit gate. Verified never counted: `tools/evolution_infer.py`'s
`evaluate_tracker()` only counts rows where `Impact == "occurred"`
(case-lowered comparison); `historical` structurally falls through every
window/threshold check regardless of configuration. This extension is
scoped to this tracker only — the shipped module template's canonical
three-value enum is unchanged.

## Incidents

| Date | Event Class | Description | Recurrence-Window Match | Impact | Migrated From Reflection | Resolved By |
|------|-------------|-------------|------------------------|--------|-------------------------|-------------|
| 2026-06-12 | review-floor-deviation | The Internal review of `dev/proposals/archive/2026-06-12-claude-check_cairn-self-host-compat.md` was headed "Claude (Internal, same-session)" — below the fresh-session floor `doctrine/dual-review.md:46` requires. | none | historical | direct | `2026-07-08-claude-review-record-integrity` |
| 2026-06-12 | review-floor-deviation | That same proposal's header stated `Plan review: required(Internal)`, but the Maintainer's Decision ("Accepted — implement directly (no formal plan)") never explicitly addressed or waived it; no plan was opened and no plan-review section landed. | 2026-06-12 (same window, same event class as the row above) | historical | direct | `2026-07-08-claude-review-record-integrity` |

**Column contract** (the canonical 7-column semantic-field schema; see
`dev/modules/incident_log_template.md` for the full field-by-field
definitions this tracker inherits).

## Goodnight migration

This tracker is fed by the goodnight migration sub-step going forward (per
the `incident-trackers` module's `Adds to:` directive), for any new
review-floor deviation a reflection reports. The two rows above are the
exception: they were logged **directly** (2026-07-13), not via a
reflection, as part of establishing this tracker — hence `Migrated From
Reflection: direct` and the historical dating.
