<!-- cairn-internal-ref-allow: doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->

# Attestation-replay failures -- incident log

**Purpose**: records a release commit whose gate-attestation claim (a
"quality_gate exit 0"-class statement in the commit body) does not
reproduce when the identical gate code is replayed against the
committed cut tree. Established 2026-07-22 (Chunk D of the
`record-corrections` proposal/plan), arming the recurrence path for
that proposal's deferred, rate-limited follow-up (a machine-generated
gate transcript requirement for future release commits) — an n=1
recorded only in prose can never become an n=2; this tracker exists so
it can.

**Rate-limit gate connection**: this tracker is the parse target for
the **adaptive-doctrine rate-limit gate** specified at
`doctrine/rationale.md` > "Adaptive-doctrine rate-limit gate." The
gate's "≥2 incidents of the same shape in a rolling window" trigger
operates on this table's `Impact = occurred` rows.

**Rolling window**: 90 days — a deliberate departure from the
`review-floor-deviations.md` precedent tracker's 14 days, not a copy of
it. `review-floor-deviations.md` tracks a high-frequency event
(process deviations that can recur on nearly every proposal); this
tracker tracks an event tied to **release commits**, a much
lower-frequency cadence. Cairn's own release history (`CHANGELOG.md`'s
dated section headers) shows gaps of 1 day (0.1.0 → 0.1.1, 2026-05-20 →
2026-05-21), 6 days (0.1.1 → 0.2.0, → 2026-05-27), and 16 days (0.2.0 →
0.3.0, → 2026-06-12) — the most recent gap already exceeds a 14-day
window, during what is likely Cairn's *fastest* development phase;
release cadence is expected to slow, not quicken, as the project
matures toward 1.0. 90 days gives a logged row genuine multi-month
liveness against a realistically-spaced next release, rather than a
window that would already be too tight on the day it's adopted. The
window length is an explicit per-tracker adopter choice
(`dev/modules/incident-trackers.md` > "the window length is an adopter
choice"), not a fixed default this tracker was required to inherit.

## What counts

* **Class name** -- `attestation-replay-failure`: a release commit's
  gate-attestation claim that does not reproduce when the identical
  gate code is replayed against the committed cut tree.
* **Criteria for "same shape" recurrence** -- two entries are the same
  shape if both are a release-commit gate-attestation claim that fails
  to replay, regardless of which sub-gate, which gate tool, or which
  release is involved.
* **What does NOT count** -- a gate result that differs between the cut
  and a later replay *because the gate code itself changed* in the
  interim (a tooling update or a later unrelated commit touching the
  gate, not an attestation failure at cut time). Confirming this
  distinction is part of logging any row: check whether the gate code
  is genuinely unchanged (or changed only in ways proven non-functional,
  e.g. comment-only) between the cut commit and the replay.

## Incidents

| Date | Event Class | Description | Recurrence-Window Match | Impact | Migrated From Reflection | Resolved By |
|------|-------------|--------------|-------------------------|--------|--------------------------|-------------|
| 2026-06-12 | attestation-replay-failure | Release commit `12ec2ad` (v0.3.0, 2026-06-12) attested `quality_gate exit 0` (neutrality all-info/justified; 6 advisory R6 redundancy notes). Replay on the immutable cut tree (confirmed 2026-07-11 during the `record-corrections` proposal's drafting, re-confirmed at that plan's own preparation and again at plan-review, 2026-07-22) does not reproduce this: `--sub neutrality` exits 1 with 99 `FAIL`-class findings, not zero; `--sub redundancy` exits 1 with 6 `FAIL`-class findings — the count matches the attestation and its acceptance was honestly disclosed at the time, but the "advisory" class-label and the umbrella "exit 0" are false. Gate code between the cut and every replay differs only by a later, comment-only SPDX-header addition (commit `501efe3`), independently confirmed AST-invisible/non-functional — not a "what does NOT count" case. | none | occurred | direct | pending |

**Column contract** (the canonical 7-column semantic-field schema; see
`dev/modules/incident_log_template.md` for the full field-by-field
definitions this tracker inherits). `Resolved By` on the row above is
`pending`, not a proposal stem: the `record-corrections` proposal
records and documents this incident (the `CHANGELOG.md` erratum,
`dev/proposals/archive/2026-07-11-claude-record-corrections.md`), but
the actual recurrence-*prevention* mechanism this tracker exists to
arm — a machine-generated gate transcript requirement for release
commits — is that same proposal's own explicitly deferred, rate-limited
follow-up, and has not landed. Nothing has resolved the underlying gap
yet.

## Goodnight migration

This tracker is fed by the goodnight migration sub-step going forward
(per the `incident-trackers` module's `Adds to:` directive), for any new
attestation-replay failure a reflection reports. Row 1 above was logged
**directly** (2026-07-22), not via a reflection, as part of establishing
this tracker — hence `Migrated From Reflection: direct`.
