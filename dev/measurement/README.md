# `dev/measurement/` — project self-instrumentation

This folder holds the records a project keeps to **measure its own process
health** — aggregate lifecycle metrics and the operational ledgers that feed
them.

## What belongs here

* **Aggregate lifecycle metrics** — a structured metrics store when a collector
  owns one, plus a **`snapshots/`** subdirectory for dated exports or secondary
  derived outputs. *The store's exact filename and format are owned by the
  metrics tooling, not fixed by this convention: reserve the slot, not the
  name.*
* **Operational ledgers that feed the metrics** — the collision log, the
  handoff-hazard log: records of process incidents kept so
  the team can measure and correlate them over time.
* **Closed records** — completed measurement evidence whose current owners
  and readers no longer need it among the live trackers, kept under
  `dev/measurement/archive/`. The top level remains the home for active
  trackers and measurement tools; a record stays at its current path while it
  still serves a live reader, gate or recurrence process.
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

* **Public test reports** — `tests/gauge.py --pulse` reads explicitly named
  JUnit XML reports and optional aggregate before/after inventories from
  `tests/tier_inventory.py list --json`. It prints case-record, outcome, duration,
  and tier file/line deltas. Case records are not unique tests or collected
  nodes, and equal run labels do not establish equivalence. Missing reports,
  inventories, labels, timings, and tool usage remain unknown. The pulse does
  not persist a store or join a private collector.

* **Explicit public artifact pulse** — `tests/audit_report.py --pulse-input`
  can emit a bounded snapshot from caller-named Markdown files, and
  `tests/gauge.py --pulse --artifact-input PATH` can render that snapshot beside
  the ordinary test pulse. The snapshot reports caller-declared cohort week and
  file labels, parent/sidefile word and byte counts, review records, declared
  model-tier observations, and chars/4 manifest estimates. Cohort selection,
  history completeness, actual repeated-context loading, and metered model mix
  remain unknown. No Git lookup, discovery, Markdown-link opening, or stored
  bundle is used. One reproducible example is:

  ```sh
  python tests/audit_report.py --pulse-input --root . --week 2026-W45 --project-alias cairn --artifact dev/plans/2026-11-04-metered-cost.md --always-loaded AGENTS.md --deliberation dev/agent_collaboration.md --model-tier Sol=high > /tmp/cairn-pulse-artifacts.json
  python tests/gauge.py --pulse --artifact-input /tmp/cairn-pulse-artifacts.json
  ```

  Replace the example labels with the explicit cohort and manifests being
  measured. The example is not a completeness claim.

* **Opt-in Meter collection** — `tools/meter.py` reads consent from the fixed
  OS account home at `~/.cairn/meter.json`; environment home values do not
  select consent, and installation creates no configuration or ledger. The
  config is version 1 with `enabled`, `sources`, and `projects`. Each source
  names an alias, supported tool (`codex`, `claude`, or `antigravity`), and the
  absolute root the collector may scan. Each project names an alias, absolute
  project path, and its expected direct Git remote. For example, replace these
  paths and remote with the exact local locations you intend to include:

  ```json
  {
    "version": 1,
    "enabled": true,
    "sources": [{
      "alias": "codex-main",
      "tool": "codex",
      "root": "/absolute/path/to/provider-data"
    }],
    "projects": [{
      "alias": "cairn",
      "path": "/absolute/path/to/project",
      "remote": "git@host:team/project.git"
    }]
  }
  ```

  Keep the config and private ledger under the account's protected `.cairn`
  directory. On Windows the Meter runs only when `.cairn` and `meter.json` are owned by your own account; if you made them from an administrator shell, make your account their owner. The bare `python tools/meter.py --json` command checks only
  whether configuration is disabled or unavailable; it does not collect.
  `python tools/meter.py refresh --json` explicitly reads only configured
  source roots, verifies configured projects, updates the private ledger at
  `~/.cairn/meter/ledger.json`, and writes sanitized project aggregates to
  a sanitized `meter.json` aggregate under each project's `dev/measurement/`
  folder. `rebuild --json` uses the same
  explicit refresh path. These commands are not scheduled or background work.
  Counting starts when the Meter first runs for a source: it records where
  each existing log ends and counts nothing before that, and `rebuild` does
  not back-fill history. Each later run reads only what a log has gained;
  Codex logs are read again from their first line when they grow, because their
  lines depend on earlier lines. Individual usage events are kept for up to
  14 days (fewer when more than 50,000 would pile up); older ones are folded
  into daily totals, which lose the per-artifact split. A run that stopped at
  its read limit prints `meter partial: catching_up` and exits 5; run `refresh`
  again until it prints `ok`. A Codex log over 512 MiB is skipped each run and
  the run prints `meter partial: source_too_large`. While the receipt is not
  `ok` or `disabled`, `python tools/session.py session-end --handoff` skips
  both prunes and exits 5. The per-project summary lists `incomplete` among
  its coverage reasons and the pulse report prints `INCOMPLETE` beside the
  supplied usage. An older ledger is refused with `ledger_old_schema`; move
  `~/.cairn/meter/ledger.json` aside to start a new one.
  A Claude record counts toward a project when its own working folder is the
  project's or lies inside it, its log is under an approved root, and the
  project's remote checks out. On Windows a log may have a second name (the
  Claude desktop app keeps one for each background sub-agent); the Meter reads
  it once, and only when no other account may write it. A Claude reply logged
  in several pieces is dated by its earliest piece, unless the pieces fall in
  two refreshes. Summaries of finished sub-agents are not
  counted; a reading whose summaries cannot be tied to a read transcript prints
  INCOMPLETE. The runs are kept for every session under the approved roots, so
  one untied summary anywhere marks every project, and it clears only when the
  ledger is replaced (which loses history: a new ledger counts nothing before
  its first refresh).
  Missing configuration stays disabled, and invalid or unsupported privacy
  state fails closed as unavailable. Aggregate coverage remains globally
  unknown; the output does not claim complete project history.

  To refresh and render the complete pulse, run
  `python tools/meter.py refresh --report --json`. The report joins only the
  current configured project from that successful refresh; if the current
  directory is unconfigured or ambiguous, usage remains unknown. Partial and
  failed refreshes return a closed status and reason, never an older export.
  The default `refresh --json` receipt is unchanged, and full handoff keeps its
  separate locked pre-prune refresh.

  Public pulse inputs remain explicit: add named `--junit-report PATH`,
  `--before-junit-report PATH`, `--tier-inventory PATH`,
  `--before-tier-inventory PATH`, or `--artifact-input PATH` arguments to
  `refresh --report`. These bounded files are not discovered automatically.
  Do not pass `--meter-aggregate` to this route; Meter supplies the fresh
  aggregate in memory. The standalone Gauge and pulse CLIs remain available
  for rendering explicit public inputs without private collection. Optional
  `--commit-label`, `--python-label`, `--selection-label`, and `--seed-label`
  (and their `--before-` counterparts) are caller-supplied identifiers, not
  proof that two cohorts are equivalent.

## What does NOT belong here — the membership rule

`dev/measurement/` is **measurement**, and the boundary is two-sided:

* **Not itself an archive.** Historical / closed records live under
  `dev/**/archive/`; only the `archive/` child holds closed measurement
  evidence. Keep active ledgers at their working paths.
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

The tracked `dev/measurement/archive/` home is delivered when the
`incident-trackers` module is selected. It contains no Cairn project records in
an adopter's tree; adopters place only their own closed evidence there. If the
module is unselected, the folder marker is not installed.
