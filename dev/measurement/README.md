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

* **Opt-in Meter collection** — `tools/meter.py` reads consent from
  `~/.cairn/meter.json` in the account's home folder (not the `HOME` variable,
  on Mac and Linux); installation creates no configuration or ledger. It reads
  only what the file lists, and only counts leave a log (an `antigravity` source
  also has the saved text files in each conversation folder searched for project
  paths; only which listed projects matched leaves). The file's content is
  checked, not who wrote it. The config is version 1 with `enabled`, `sources`,
  and `projects`. A source names an alias, a tool (`codex`, `claude`, or
  `antigravity`) and the absolute root to scan; a project names an alias, its
  absolute path and its Git remote, taken as written. For example, replace
  these paths and remote with the locations you intend to include:
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

  The bare `python tools/meter.py --json` command checks only whether
  configuration is disabled or unavailable; it does not collect.
  `python tools/meter.py refresh --json` reads only configured source roots
  (skipping links), updates the ledger at
  `~/.cairn/meter/ledger.json`, and writes a `meter.json` summary of counts,
  times, model names and plan names into each project's existing
  `dev/measurement/` folder. It never creates that folder or `dev`, and never
  writes through a link. Where the system has file modes only you can read the
  ledger and summary; on Windows the summary takes the project folder's access,
  so whoever may read that folder may read the counts. Each file is written
  beside its place and renamed in, and a lock left by a dead run is taken over
  after 15 minutes, so a run killed mid-way can make the next say `ledger_busy` until then. `rebuild --json` takes the same path; neither is scheduled.
  Counting starts at a source's first run: the Meter records where each log ends
  and counts nothing before that, and `rebuild` does not back-fill. Later runs
  read only what a log has gained, except Codex logs, which are read again from
  their first line when they grow. Usage events older than 14 days (or beyond
  50,000) are folded into daily totals, which lose the per-artifact split. A run
  that stopped at its limit or could not open a log prints `meter partial:
  catching_up` and exits 5; run `refresh` again until it prints `ok`. A Codex
  log over 512 MiB is skipped each run (`meter partial: source_too_large`), and
  so is an Antigravity log with a line over 8 MiB.
  While the receipt is not `ok` or `disabled`, `python tools/session.py
  session-end --handoff` skips both prunes and exits 5. The summary lists
  `incomplete` among its coverage reasons and the pulse report prints
  `INCOMPLETE` beside the usage. An older ledger is refused with
  `ledger_old_schema`; move `~/.cairn/meter/ledger.json` aside to start a new one.
  A Claude record counts toward a project when its own working folder is the
  project's or lies inside it and its log is under an approved root. The Meter
  does not open the project's Git settings, so `current_local_verified` and
  `proven` mean that the folder matched; a Codex log that names its repository
  is still compared with the remote in the config. A Claude reply logged in
  several pieces is dated by its earliest piece, unless the pieces fall in two
  refreshes. Summaries of finished sub-agents are not counted; one that cannot
  be tied to a read transcript prints INCOMPLETE for every project until the
  ledger is replaced (a new ledger counts nothing before its first refresh).
  Missing configuration stays disabled, and invalid configuration is
  unavailable. Aggregate coverage remains globally unknown; the output does not
  claim complete project history.

  Each summary row also carries weighted totals: its tokens priced at the
  model maker's public list prices, in US dollars per million tokens, from the
  table in `tools/meter.py` dated 2026-11-22. A weighted total is a reference figure for
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
  carry an earlier one. A reply from an `antigravity` source states input and
  output counts only (no model, no cache counts), so its rows show
  `weighted=unknown`: they say how many tokens, not what they cost. The OpenAI
  and Google model names are the
  makers' own and are not matched against a real log; a Codex reply whose log
  omits its cache-write count gets no total. The pulse prints each row's weighted total as `weighted=`, or `weighted=unknown` where the row has none.

  An `antigravity` conversation counts toward the one listed project whose path
  its own saved files name, and toward no project if they name none or several,
  or if the search hits a limit (16 MiB, 5,000 entries or 8 folder levels per
  conversation) or cannot read a file.
  A project's export then carries `antigravity_project_inferred`, because
  matching text is an inference, not proof; a row whose source is no longer
  listed gets the same label. While any such conversation is
  unattributed, every project's export carries `antigravity_unattributed`, and
  its report shows INCOMPLETE once, on its header line, because those tokens
  may belong to any project.

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
