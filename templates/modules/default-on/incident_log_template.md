<!-- cairn-internal-ref-allow: doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# <tracker_name> -- incident log

**Purpose**: <describe what event class(es) this tracker records, e.g.,
"staged-index collisions in the project's dev tree" or "all
coordination + commit-discipline incidents.">

**Rate-limit gate connection**: this tracker is the parse target for
the **adaptive-doctrine rate-limit gate** specified at
`doctrine/rationale.md` > "Adaptive-doctrine rate-limit gate." The
gate's "≥2 incidents of the same shape in a rolling window" trigger
operates on this table's `Impact = occurred` rows.

**Rolling window**: <14 days | adopter-chosen value>.

## What counts

Define the event class(es) this tracker records. Each class needs:

* **Class name** -- a stable identifier the table's `Event Class`
  column references (e.g., `staged-index-collision`,
  `untracked-lifecycle-artifact`, `work-intent-claim-conflict`).
* **Criteria for "same shape" recurrence** -- the equivalence
  relation the rate-limit gate uses to count recurrences. Two
  incidents are the "same shape" if <adopter defines>.
* **What does NOT count** -- adjacent incidents that look like
  the failure mode but aren't (the `Impact = non-conflict` column
  carries these for base-rate visibility but doesn't count
  against the rate-limit gate's trigger).

## Incidents

| Date | Event Class | Description | Recurrence-Window Match | Impact | Migrated From Reflection | Resolved By |
|------|-------------|-------------|------------------------|--------|-------------------------|-------------|
| <YYYY-MM-DD> | <event-class> | <one-line description> | <none / list of prior dated entries within window> | <occurred / prevented / non-conflict> | <YYYY-MM-DD / agent-id> or `direct` | <proposal stem / commit SHA prefix / `pending`> |

**Column contract** (the canonical 7-column semantic-field schema
the Goal 7 cross-adopter harvest reads against):

* **Date** -- ISO date of the incident (`YYYY-MM-DD`).
* **Event Class** -- the adopter-defined class name from "What
  counts" above.
* **Description** -- one-line freeform description.
* **Recurrence-Window Match** -- prior dated entries in this
  tracker matching the same event class within the rolling
  window, or `none` if this is the first occurrence in the
  window. This is what the rate-limit gate evaluates against.
* **Impact** -- one of three values:
  * `occurred` -- the failure mode actually fired; counts against
    the rate-limit gate's trigger.
  * `prevented` -- the failure mode would have fired but was
    caught by a structural mechanism (work-intent claim
    collision, pre-commit hook warn, etc.); logged for base-rate
    visibility, does not count.
  * `non-conflict` -- the surface looked like the failure mode
    (two agents in the same window) but was structurally not a
    conflict (different files, different sections, etc.); logged
    for concurrency base-rate visibility, does not count.
* **Migrated From Reflection** -- the date / agent of the
  reflection that captured the incident pre-migration
  (e.g., `2026-05-28 / claude-fedda242`), or `direct` if the
  incident was logged directly without passing through a
  reflection.
* **Resolved By** -- one of three forms:
  * **Proposal stem** -- e.g., `2026-05-27-claude-foo-doctrine`.
    Names the deliberation that produced the doctrine adjustment.
  * **Commit SHA** -- the 7-12 char prefix of the implementing
    commit when no separate proposal landed (e.g., maintainer-
    directed direct edit).
  * **`pending`** -- logged but no resolution has landed yet.
    The rolling-window gate still counts the incident; pending
    signals the recurrence is unaddressed.

Adopters may **append columns to the right of `Resolved By`** for
deployment-specific tracking needs; the cross-adopter harvest tool
ignores out-of-contract columns.

## Goodnight migration

This tracker is fed by the goodnight migration sub-step (per the
`incident-trackers` module's `Adds to:` directive). The full-
handoff owner reads the day's reflections, identifies incidents
matching the event class(es) defined above, and adds a row per
incident to the table.

If a reflection records a prevented or non-conflict incident
(caught + reported), log it with the matching `Impact` value for
base-rate visibility; the rate-limit gate ignores non-`occurred`
rows when counting recurrences.
