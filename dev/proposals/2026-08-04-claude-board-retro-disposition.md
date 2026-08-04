# Retrospective disposition of the 59 board rows deposited under the old precondition

**Author**: Claude (Strategy)
**Model**: claude-opus-5
**Date opened**: 2026-08-04
**Status**: proposed
**Touches**: `dev/PLANNING.md` > "Deferred follow-ups (durable home)" (the 59 rows); inbound `Follow-ups migrated to:` references in six artifacts, two of them archived
**Related**: split out of `2026-08-04-claude-deferral-discipline` as **D1** by its Decision (`6e349b3`); the [I8] hazard is that proposal's Internal-review finding
**Plan review**: required(Internal) — the adjudication is per-item judgment over records other artifacts point at, which is where a second read is worth most

## Context

`2026-08-04-claude-deferral-discipline` (accepted `6e349b3`, implemented across
chunks A–F) changed the archive precondition so a deferred follow-up carries a
**recorded disposition** — `accept`, `guard`, `wontfix`, or a Maintainer-authorized
`defer` — rather than requiring a durable home for everything.

**New doctrine does not clear rows deposited under the old rule.**
`dev/PLANNING.md` > "Deferred follow-ups (durable home)" holds **59 items** in
**430 lines**, 42.9% of a 1002-line file (`as_of 2026-08-04`, HEAD `4573c11`).
Every one of them was homed there because the old precondition offered no other
route. This proposal adjudicates them.

It was split from the parent deliberately. The parent's Internal review found the
bundling defective on the `identity-not-name` precedent: a per-item adjudication
of unknown batch size, gated on the Maintainer, over records that other artifacts
cite, is a different kind of work from a prose amendment. The parent's Response
conceded the point — *sequencing* the retro pass as a named successor **is** the
`defer` (successor) disposition, so applying the ladder to itself is the opposite
of self-refuting.

**The condition attached to that split is discharged by this file existing.** The
Decision required the successor to open in the same session, with its stem named
in a commit body, so its absence would be visible in `git log` rather than only in
a reader's memory.

## Proposal

Adjudicate each of the 59 rows against the accepted vocabulary, in **batches by
source artifact** rather than one pass over the whole section, so each batch is
reviewable and the Maintainer sees one `defer` list per batch rather than 59
decisions.

Expected shape — **an estimate, explicitly not a measurement.** The parent's
"12 of the 59" figure was withdrawn as unreproducible: its Internal reviewer got
4, 5, 6 and 17 under four different patterns, and established that only **18** of
the 59 carry an explicit `*Trigger:*` field at all. This proposal therefore
commits to **no** routing split in advance. The per-item adjudication produces the
first real figure, and that figure is the deliverable.

### The [I8] hazard — inbound references from closed artifacts

Six artifacts cite this section as the home against which their archive
precondition was discharged, **two of them already archived and therefore
append-only**:

* `dev/plans/archive/lockfile-provenance-fields.md`
* `dev/plans/archive/interpreter-trust-root-fallback.md`

The second is already a live instance: it records S2 as homed at a
`dev/PLANNING.md` **Queued** row, and S2 now sits inside `### Deferred
follow-ups`. **The pointer has already drifted once.** Re-routing it again —
especially to `wontfix` — would leave an archived, append-only record asserting a
migration that is no longer true and cannot be corrected in place.

Two rules govern this, both carried verbatim from the parent's accepted C4:

1. A row **named by a closed artifact's disposition block** is **ineligible for
   `wontfix` without the Maintainer**.
2. Any re-route of such a row is recorded as a **forwarding entry** in this
   pass's own commit body, so the closed artifact's claim remains
   reconstructible from the durable record even though its text cannot change.

### Sequencing note

This pass **may not begin** until the parent plan's Chunk D has landed, because
Chunk D rewrites the archive-precondition prose at `dev/PLANNING.md:433` and this
pass rewrites rows below it in the same file. Landing them in either order is
fine; landing them concurrently is a conflict.

### Documentation / doctrine surface

**None.** This proposal changes no rule — it applies an already-accepted one to
existing rows. The only file it edits is `dev/PLANNING.md`'s deferred section.
Stated explicitly because a silent omission here would itself be a review finding.

### Doctrine-change rate-limit

**N/A** — this proposal introduces no doctrine change. It executes
`2026-08-04-claude-deferral-discipline`, whose own gate clearance is recorded in
that artifact and does not re-apply.

## Rationale

**Which workflow?** Cold pickup. `dev/NEXT_SESSION.md` competes with a 1002-line
board on which a release blocker and a two-assertion test guard carry equal
visual weight.

**Why now?** The parent lands the rule this session. A rule that governs only
future artifacts, while 59 rows sit under the superseded one, is the weaker half
of the change — and the gap is exactly where a reader concludes the rule is
decorative.

**Why not just leave them?** Because the parent's governing principle is stated
over *outstanding follow-ups*, and 59 unadjudicated rows are outstanding
follow-ups. Leaving them would make the principle true only by not looking.

## Alternatives considered

* **Do nothing; let the rows age out.** The board has no expiry — the staleness
  sweep can only reaffirm. "Aging out" is not a mechanism that exists.
* **Bulk-decline everything below a consequence threshold.** Fast, and wrong: it
  is precisely the rubber-stamped-decline failure the parent's *Signals* section
  names as its own worst outcome ("visible debt traded for invisible debt, the
  strictly worse trade").
* **Adjudicate in one pass rather than batches.** Rejected — one 59-item
  Maintainer batch is the load-bottleneck failure mode the parent's item 3
  batching rule exists to prevent, reproduced at the worst possible size.
* **Keep it inside the parent proposal** (what the parent originally proposed).
  Rejected by the parent's own Decision on the `identity-not-name` bundling
  precedent.

## Evidence / verification plan

* **Tests** — **N/A**: this pass edits one Markdown file and writes no code.
* **Examples / smoke checks** — `python scripts/check_cairn.py` after each batch;
  the board carries many path citations and re-routing is exactly where they
  break. `python scripts/claim_check.py dev/PLANNING.md` likewise.
* **Docs** — the board section is the deliverable; no other doc changes.

### Author-accounting

* **Invariants.** (1) *No row disappears without a recorded disposition* —
  enforcer: this pass's own `Dispositions:` commit bodies, reviewed. (2) *No
  closed artifact's claim is falsified* — enforcer: the forwarding-entry rule,
  reviewed. Both **documentary**; consistent with the parent, which established
  that a presence-checker would certify the degenerate case.
* **Failure modes.** Over-eager decline — **fails open**, and is the principal
  risk, same as the parent's. Under-eager decline — fails safe: the board stays
  long, which is the status quo.
* **Edge cases.** A row whose source artifact is *in flight* (not archived) →
  route to that artifact's own archive-preparation instead of adjudicating it
  here, so its author disposes of it. A row citing another row → adjudicate the
  cited one first.
* **Known omissions.** No routing estimate is offered, deliberately (above). The
  batch count is not fixed in advance; it follows the source-artifact grouping the
  section already has.

## Signals the change is wrong

* **Declines cluster in one batch.** If one artifact's rows route overwhelmingly
  to `wontfix` while others do not, the adjudicator is tiring rather than judging.
  **Recovery:** re-adjudicate that batch fresh-session.
* **A closed artifact's claim is found falsified after the fact.** The forwarding
  rule failed. **Recovery:** an appended correction note in this pass's record —
  the archived artifact still cannot be edited.
* **The board does not measurably shrink.** Then the 59 were mostly real work and
  the parent's diagnosis over-attributed to the ratchet. **Recovery:** say so on
  the record, and stop — a board of 59 genuine obligations is a resourcing
  problem, not a doctrine problem.
