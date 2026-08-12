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

`cairn-pilot-event/2`. Each event is one fenced block whose fence names
`cairn-pilot-event`; the keys below are exact and the set is **closed** — an
unknown key, a missing mandatory key, an unknown schema version, or a value
outside the bounded grammar **refuses** rather than being ignored. Values are
printable ASCII, at most 200 characters, and contain no backslash, backtick,
or pipe.

**`/1` is retired, and a `/1` block now refuses.** Chunk P2 of
[`review-efficient-lifecycle`](../plans/review-efficient-lifecycle.md) bumped the
version to add `assurance_path` and close the eligible / ineligible gap recorded
below. A `/1` block carries no `assurance_path`, so reading one as `/2` would be
exactly the half-read the version field exists to prevent. Nothing recorded is
invalidated: this ledger holds **no events** (see `## Events`), so the retirement
reaches no history.

| Key | Kinds | Value |
|---|---|---|
| `schema` | all | exactly `cairn-pilot-event/2` |
| `kind` | all | `plan-counted`, `pause-set`, or `pause-cleared` |
| `date` | all | `YYYY-MM-DD`, a real calendar date |
| `subject` | all | the plan stem, or the pause identifier |
| `source_artifact` | all | repository-relative path, existing at `source_commit` |
| `source_commit` | all | full 40-character commit id, existing in this repository |
| `plan_state` | `plan-counted` | the counted plan state, written by the CLI from the vocabulary |
| `assurance_path` | `plan-counted` | `standard`, `high-assurance`, or `not-inherited` — **derived** by the CLI from the plan, never typed |
| `review_input_bytes` | `plan-counted` | bytes of review input for that plan |
| `transitions_removed` | `plan-counted` | lifecycle transitions the allocation removed |
| `escaped_findings_high` | `plan-counted` | high-severity findings that escaped to a later boundary |
| `escaped_findings_low` | `plan-counted` | lower-severity findings that escaped |
| `maintainer_prompts` | `plan-counted` | Maintainer decision prompts that plan required |
| `severity` | `pause-set` | `high` or `low` |
| `note` | all | optional, one line |

The body of one `plan-counted` block, without its fence lines:

```text
schema: cairn-pilot-event/2
kind: plan-counted
date: 2026-09-14
subject: some-plan-stem
source_artifact: dev/plans/some-plan-stem.md
source_commit: 0123456789abcdef0123456789abcdef01234567
plan_state: <the counted state, from the vocabulary>
assurance_path: <resolved from the plan, from the vocabulary>
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

## The eligible / ineligible split — closed by Chunk P2

This section recorded two gaps. **The first is now closed**, by the
`cairn-pilot-event/2` bump this record's own schema section describes.

The accepted parent counts "six eligible **standard** plans", says high-assurance
work "remains ineligible and does not fill the sample", and requires the report
to record "eligible and ineligible plans". P6a could not derive that: no
`plan-counted` field carried a plan's assurance path, and a plan **has** none of
its own to read — the assurance path is declared by a *proposal*, and a plan
reaches it only through the inheritance chain Chunk P2 implements. So this was a
sequencing dependency on P2, recorded as **[CF1]** in that plan's
`## Carried-forward obligations`, and P2 discharges it:

* every `plan-counted` event carries `assurance_path`, **derived** by the CLI
  from the plan (plan → `Inherited proposal basis` → the accepted proposal's
  `Assurance path`), never typed by the recorder — the same rule `plan_state`
  already followed, and for the same reason;
* the vocabulary is read from `tools/lifecycle_planner.py`'s now-**public**
  `ASSURANCE_PATHS` plus its `ASSURANCE_NOT_INHERITED`, through the same
  contained loader the status vocabulary is read through, so the CLI declares no
  assurance token of its own; and
* `pilot-report` prints the split — eligible (`standard`), and ineligible or
  outside the sample (`high-assurance`, `not-inherited`) — with each counted stem
  labelled.

**A plan that declares a chain the planner cannot resolve refuses the write.**
Recording `not-inherited` for it would be a quiet lie about which population the
sample came from.

**One thing P2 deliberately did *not* decide.** The counted-stem quota still
counts **distinct stems**, not eligible stems. The accepted parent says
high-assurance work does not fill the sample; the 2026-08-11 revision says
standard *and* high-assurance proposals may both receive `READY`, which makes
high-assurance plans part of the population the policy now affects. Those two
accepted texts pull opposite ways on *whose* plans fill the six, and [CF1] asked
only for the split. Choosing between them is a Maintainer's call, so the
denominator is unchanged and the report **prints the tension** whenever the
sample contains an ineligible stem.

**The second gap is still open**: **broad-suite executions and elapsed time**,
in the accepted parent's report list and not in the revision's narrower one
(review input, removed transitions, escaped findings, Maintainer prompts,
pauses). Whether that narrowing was intended is a Maintainer's call, not an
implementer's, so it stays recorded here rather than closed by guesswork.
Closing it is another schema bump; the version field exists for that.

## Events

*None yet.* The window opens at P6d; this ledger ships with the machinery so
that the first event has somewhere to land and a schema to land in.
