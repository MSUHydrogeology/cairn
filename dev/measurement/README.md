# `dev/measurement/` — project self-instrumentation

This folder holds the records a project keeps to **measure its own process
health** — aggregate lifecycle metrics and the operational ledgers that feed
them.

## What belongs here

* **Aggregate lifecycle metrics** — the canonical **structured metrics store**
  (the parseable record a metrics tool reads and writes) plus a **`snapshots/`**
  subdirectory for dated CSV exports or secondary derived outputs. *The store's
  exact filename and format are owned by the metrics tooling, not fixed by this
  convention: reserve the slot, not the name.*
* **Operational ledgers that feed the metrics** — the collision log, the
  handoff-hazard log, the signature log: records of process incidents kept so
  the team can measure and correlate them over time.
* **Machine-appended operational ledgers, and the readers that render them** —
  the same slot, for records a *tool* appends rather than a person: one line
  per event, accumulated as work happens, with a companion reader that renders
  the accumulation for a human without re-running whatever produced it. Reserve
  the slot for both halves, and note that they are not kept the same way: the
  ledger is a regenerated **output**, so it belongs in the project's ignore
  rules like any other generated file, while its reader is source and lives
  with the project's other tooling. The reason to keep one at all is that a
  figure which must be re-measured every time it is wanted *will* be
  re-measured every time it is wanted, and lost again in between.

## What does NOT belong here — the membership rule

`dev/measurement/` is **measurement**, and the boundary is two-sided:

* **Not an archive.** Historical / closed records live under `dev/**/archive/`.
  This folder is live measurement, not a graveyard of finished work.
* **Not framework-adopter state.** The Cairn lockfile, base cache, and
  `profile.yml` live in `dev/.cairn/` — scaffold-tool /
  framework-relationship machinery, not process-health measurement.

Two calls that are **tempting but excluded** (the guard made concrete):

* **The work-intent log is active coordination state** — who is editing what,
  right now — not a kept measurement record. It **stays put** (wherever the
  coordination tooling homes it), it does not move here.
* **`dev/reflections/` is ephemeral** — per-session, pruned — not a durable
  measurement record. It **stays put**.

The two-sided exclusion — *not an archive, not adopter state* — is what keeps
this folder from becoming a miscellaneous junk drawer. A file that is neither an
aggregate metric nor a measurement-feeding operational ledger does not belong
here.
