<!-- cairn-internal-ref-allow: doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Maintainer-view misses -- incident log

**Purpose**: records each time something waited on the Maintainer without
appearing in `python tools/board.py --maintainer`, so the list's one promise --
it shows what authors declared, and its footer names what it cannot see -- is
tested rather than trusted. **Two rows in the window mean declaring a wait by
hand is the wrong design.** That is the design's own falsifier
(`dev/proposals/archive/2026-10-17-claude-maintainer-attention.md`, "What would
falsify it"), not only a rate-limit suggestion to adjust doctrine; the gate's
suggestion is merely how a reader learns it, and it should be read as that. The
design has three other warning signs
(`dev/proposals/archive/2026-10-17-claude-maintainer-attention.md`, "Signals the
change is wrong") that no row here records, so they are read by use: a Waiting
line or board-row marker that outlives its answer; the footer's advisory line
(plans that mention a fenced step but declare no wait) naming most open plans
for most of their lives, with its first reading, 2 of 2 open plans, as the
baseline, so that the same cause (a wait declared on a board row, which the
advisory cannot see) at each of the next two plan archives is the cue to
redesign the line; and `defer` rows piling up unopened on the board.

**Rate-limit gate connection**: this tracker is the parse target for the
**adaptive-doctrine rate-limit gate** specified at
`doctrine/rationale.md` > "Adaptive-doctrine rate-limit gate." The
gate's "≥2 incidents of the same shape in a rolling window" trigger
operates on this table's `Impact = occurred` rows.

**Rolling window**: 30 days.

## What counts

* **Class name** -- `waiting-line-miss`: an item waited on the Maintainer --
  its next move was theirs -- and the Maintainer's list did not show it. **Two
  sources count under this one name**, so that one of each adds up to the two
  that matter:
  * **A code-review finding.** The code reviewer, reading `git log -p` on the
    plan over the reviewed range, finds a fenced chunk or a deviation request
    with no Waiting line written for it. The reviewer records the row.
  * **A Maintainer report.** The Maintainer says something was waiting on them
    and was not listed. This includes a board row in `dev/PLANNING.md`: for
    those, the Maintainer noticing is the only trigger, and this is where it is
    written down. The agent who hears the report records the row.
* **Criteria for "same shape" recurrence** -- two entries are the same shape if
  each is a wait that never reached the list, whichever source found it,
  whichever artifact held it (a plan, a change note, a proposal, a board row),
  and whichever way it went missing (never written, written in a form the board
  does not read, or written and then deleted early). The class is one on purpose:
  the gate counts rows per class, and a code-review miss plus a Maintainer-
  reported miss filed under two names would never reach two.
* **What does NOT count** --
  * **Pushes.** They are always the Maintainer's and the list's footer says it
    does not show them; that is stated behaviour.
  * **A wait the advisory line named.** A plan that mentions a fence but declares
    no wait is flagged on the list, so it was visible.
  * **A fence the reviewed range did not reach**, and a wait declared on a marked
    board row, which the code review checks there.
  * **A marker that outlived its answer.** That makes the list too long rather
    than too short; it is a different failure and is not counted here.

## Incidents

| Date | Event Class | Description | Recurrence-Window Match | Impact | Migrated From Reflection | Resolved By |
|------|-------------|-------------|------------------------|--------|-------------------------|-------------|

**Column contract** (the canonical 7-column semantic-field schema; see
`dev/modules/incident_log_template.md` for the full field-by-field
definitions this tracker inherits). `Event Class` is always
`waiting-line-miss`. `Impact = occurred` is a miss that happened and is the only
value the gate counts; `prevented` is for an author who caught their own missing
line before any reviewer or the Maintainer did, logged for base-rate visibility
only. Name the source in `Description` ("code review of `<plan>`" or
"Maintainer report") and the artifact that held the wait.

## Goodnight migration

Rows are written when the miss is found, not saved for the goodnight pass: the
code reviewer writes theirs with the review, and whoever hears a Maintainer
report writes that row (`Migrated From Reflection: direct`). The goodnight
migration sub-step (per the `incident-trackers` module's `Adds to:` directive)
still picks up any miss a reflection records that has no row yet.
