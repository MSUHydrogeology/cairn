# `dev/measurement/` — project self-instrumentation
Written in [Cairn Plain Language 1.0](../agent_collaboration.md).

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
  handoff-hazard log: records of process incidents kept so
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

* **Opt-in Meter pulse** — Meter does not collect until the person has reviewed
  the proposed provider-log roots and project paths and explicitly enabled
  consent in `~/.cairn/meter.json`. Its private ledger is
  `~/.cairn/meter/ledger.json`; each configured project whose `dev/measurement/`
  folder already exists receives a sanitized `meter.json` export there, which on
  Windows takes that folder's access. The recurring work and cost depend on
  selected logs and are unmeasured. `python dev/tools/meter.py refresh --report
  --json` reports the complete pulse and joins only the current configured
  project from that successful refresh. Partial or failed runs return a closed
  status and reason; an older project export is never used as fallback. Full
  handoff retains its separate locked pre-prune refresh.

  Each summary row also carries weighted totals: its tokens priced at the
  model maker's public list prices, in US dollars per million tokens, from the
  table in `dev/tools/meter.py` dated 2026-11-22. A weighted total is a reference figure for
  comparing work, never a bill; the table leaves out taxes, subscriptions and
  introductory prices (Gemini 4 Argon's, which ends 2026-11-30, is not used). A
  request whose prompt is over a model's long-prompt limit (100,000 tokens for
  Claude Haiku 5.5, 272,000 for the OpenAI models listed) takes that model's
  higher weights. A model missing from the table gets counts and no weighted
  total. A reply with an unknown count gets no total, and no figure at all
  where the model has a long-prompt level. A Codex reply is weighted by the
  model its turn had selected. When the table changes, the ledger keeps
  working: replies still held one by one are weighted by the new table at the
  next refresh, and a day already folded keeps the weighting of its day. The
  table date on a summary names the current table; a day folded earlier may
  carry an earlier one. The Gemini rows wait for a reader of Antigravity logs,
  which the meter does not have; the OpenAI and Google model names are the
  makers' own and are not matched against a real log; a Codex reply whose log
  omits its cache-write count gets no total.

  After explicit consent, create the version-1 config at the fixed account
  path with only the approved provider and project paths. The aliases below
  are examples; replace every placeholder with the actual approved value.

  ```json
  {
    "version": 1,
    "enabled": true,
    "sources": [{
      "alias": "codex-main",
      "tool": "codex",
      "root": "/approved/absolute/provider-log-root"
    }],
    "projects": [{
      "alias": "project",
      "path": "/approved/absolute/project-path",
      "remote": "git@host:team/project.git"
    }]
  }
  ```

  Public pulse inputs remain explicit. Add `--junit-report PATH`,
  `--before-junit-report PATH`, `--tier-inventory PATH`,
  `--before-tier-inventory PATH`, or `--artifact-input PATH` to the report
  command to include named public files. They are bounded and are not found by
  discovery. Do not pass `--meter-aggregate` to `refresh --report`; the fresh
  aggregate is joined in memory. Standalone `dev/tools/pulse.py` and Gauge pulse
  views remain available for explicit public inputs. `--commit-label`,
  `--python-label`, `--selection-label`, and `--seed-label` (with their
  `--before-` counterparts) are caller-supplied identifiers; they do not
  establish that two cohorts are equivalent.

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

New folders under `dev/`, and committed briefs or reports used to evade length
limits, require the Maintainer’s permission. This README records purpose; it
does not grant permission.
