<!-- claim-check-allow: dev/measurement/pilot-activation.md -->

# Monitoring-evidence event ledger -- the review allocation

**Purpose**: the append-only record of what the **proposal-centered review
allocation** actually cost and caught, one event per counted plan stem or
pause. Counts, pause state, the window, and the whole report are **derived
from this file** by `python tools/lifecycle.py pilot-report` and are stored
nowhere. Established by Chunk P6a of
[`dev/plans/review-efficient-lifecycle.md`](../plans/review-efficient-lifecycle.md).

**This ledger measures a policy that is already in force.** The allocation is
the default now; this is monitoring evidence, not a permission gate. Two
consequences a reader must not get backwards:

* **No activation record means no evidence window has opened yet** — the
  window opens with `dev/measurement/pilot-activation.md`, the data-only
  Maintainer commit at that plan's fence **M2**. It does **not** mean the
  review policy is disabled, and no reader or writer of these records may
  treat it that way.
* **The Decision at the boundary is `retain | revise | retire`.** There is no
  promotion Decision; `promote` is a retired token.

## Why two records instead of one state file

The authority inputs are split so that neither is a mutable
last-writer-wins file:

* **`dev/measurement/pilot-activation.md`** — an *immutable* tracked
  activation record. It names `machinery_sha` (the reviewed Boundary-B2
  commit) and the evidence section that attests it. It does **not** name the
  commit that enabled the window or the date it opened: both are **derived**
  from git as the commit that first introduced that exact record, and that
  commit's author date. A commit cannot contain its own id, so storing either
  would be circular.
* **this ledger** — *append-only*. Every event is bound to its source
  artifact and the commit that artifact was read at. Prior events are never
  edited: `pilot-report` and `pilot-record` both refuse when the events
  committed at `HEAD` are not a prefix of the events on disk.

## What counts

* **`plan-counted`** — one distinct plan stem reached the plan state the
  six-plan rule counts, under this contract. The state token is **not**
  written by hand: the CLI takes it from the single runtime status
  vocabulary (`tools/lifecycle_planner.py`) and refuses if the vocabulary
  does not declare it. Counting is by **distinct stem**; a duplicate or
  conflicting event for a stem already counted refuses.
* **`pause-set`** / **`pause-cleared`** — a pause condition began or ended.
  A `pause-set` for an already-active subject refuses, and so does a
  `pause-cleared` for a subject that is not active.

**What does NOT count**: a plan that never reached the counted state; an
event outside the window (it stays in the ledger and is reported as
excluded, never silently dropped); anything a person types straight into
this file.

## The window and the boundary

* **Six plans** — six *distinct* plan stems counted inside the window.
* **60 days** — 60 calendar days from the derived activation date, **both
  ends inclusive**: the activation date is day 1, and the last in-window day
  is `activation date + 59`.
* The monitoring boundary is reached at whichever comes first, and the
  report says which. An undersized or empty sample is a **result**, reported
  as such; it is never read as success.

## Schema

`cairn-pilot-event/1`. Each event is one fenced block whose fence names
`cairn-pilot-event`; the keys below are exact and the set is **closed** — an
unknown key, a missing mandatory key, an unknown schema version, or a value
outside the bounded grammar **refuses** rather than being ignored. Values are
printable ASCII, at most 200 characters, and contain no backslash, backtick,
or pipe.

| Key | Kinds | Value |
|---|---|---|
| `schema` | all | exactly `cairn-pilot-event/1` |
| `kind` | all | `plan-counted`, `pause-set`, or `pause-cleared` |
| `date` | all | `YYYY-MM-DD`, a real calendar date |
| `subject` | all | the plan stem, or the pause identifier |
| `source_artifact` | all | repository-relative path, existing at `source_commit` |
| `source_commit` | all | full 40-character commit id, existing in this repository |
| `plan_state` | `plan-counted` | the counted plan state, written by the CLI from the vocabulary |
| `review_input_bytes` | `plan-counted` | bytes of review input for that plan |
| `transitions_removed` | `plan-counted` | lifecycle transitions the allocation removed |
| `escaped_findings_high` | `plan-counted` | high-severity findings that escaped to a later boundary |
| `escaped_findings_low` | `plan-counted` | lower-severity findings that escaped |
| `maintainer_prompts` | `plan-counted` | Maintainer decision prompts that plan required |
| `severity` | `pause-set` | `high` or `low` |
| `note` | all | optional, one line |

The body of one `plan-counted` block, without its fence lines:

```text
schema: cairn-pilot-event/1
kind: plan-counted
date: 2026-09-14
subject: some-plan-stem
source_artifact: dev/plans/some-plan-stem.md
source_commit: 0123456789abcdef0123456789abcdef01234567
plan_state: <the counted state, from the vocabulary>
review_input_bytes: 18422
transitions_removed: 1
escaped_findings_high: 0
escaped_findings_low: 0
maintainer_prompts: 2
```

An example shown inside a fenced block like the one above is **inert**: the
parser reads only top-level blocks, so documenting the schema here can never
inject an event.

## How to append

The CLI is the only writer. Do not hand-edit:

```text
python tools/lifecycle.py pilot-record --kind plan-counted \
    --subject <plan-stem> --source-artifact dev/plans/<plan-stem>.md \
    --source-commit <40-hex> --review-input-bytes <n> \
    --transitions-removed <n> --maintainer-prompts <n>
```

`--dry-run` prints the block and writes nothing. The append is atomic with an
expected-old check: a second writer that raced loses cleanly and records
nothing rather than overwriting. Commit the file in the same turn — the
ledger is durable because it is tracked, not because it is on disk.

## Events

*None yet.* The window opens at P6d; this ledger ships with the machinery so
that the first event has somewhere to land and a schema to land in.
