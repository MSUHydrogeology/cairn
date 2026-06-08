<!-- cairn-internal-ref-allow: doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Module: incident-trackers

**Selected when:** default-on — kept by every deployment that may want
the rate-limit gate doctrine to be empirically enforceable. The cost is
one mostly-empty file (the forkable tracker template) and a cheap
nightly migration step; the payoff is that the rate-limit gate's
"≥2 incidents of the same shape in a rolling window" trigger has a
**parse target** instead of vibes.
**Adds to:** a forkable incident-tracker template at `dev/modules/`
(installed from this module's template, fork-on-demand to a live
location like `dev/measurement/incident_log.md`), plus a goodnight **incident-
tracker migration** step in the session-routines / goodnight doctrine.

The incident-trackers module is the **deployment-side measurement
substrate** the rate-limit gate doctrine (`doctrine/rationale.md` >
"Adaptive-doctrine rate-limit gate") evaluates against. Cairn's
doctrine names the structural commitment ("no doctrine change from a
single incident; recurrence ≥2 in a rolling window triggers
adjustment"); this module ships the substrate that makes the
commitment enforceable. Without it, the rate-limit gate is normative
but unreachable — adopters know the doctrine but can't observe their
own rate against it.

## What this module is

A **tracker-pattern template + the goodnight migration discipline**
that makes trackers the rate-limit gate's parse target. The module
ships:

* The **forkable tracker template** at
  `dev/modules/incident_log_template.md`. Adopters fork to one or
  more live tracker locations (e.g., `dev/measurement/incident_log.md` for a
  single combined tracker, or class-specific trackers like
  `dev/measurement/collision_log.md` + `dev/measurement/coordination_incidents.md`
  for multi-class deployments). Live trackers home under **`dev/measurement/`**
  (the self-instrumentation standard — they are measurement that feeds the
  Compact's collision-log correlation); only the forkable *template* stays in
  `dev/modules/`.
* The **canonical 7-column semantic-field schema** the template
  carries — the contract Goal 7's eventual cross-adopter harvest
  reads against.
* The **goodnight migration sub-step** wiring the tracker into the
  standing session-routines (see `Merged into:` block below).

## What this module is NOT

A one-size-fits-all incident log. Adopters fork the template and
define their own **event classes** in the "What counts" section of
each tracker. The module ships the **pattern + schema contract**;
the event taxonomy is per-deployment.

## Sensing write-path (automatic detector → recorder)

The goodnight migration is **no longer the only writer.** When the
`coordination-tiers` work-intent **pre-commit hook** (`tools/intent.py`)
detects a *provably-different live session's* claim on a staged path, it
**auto-appends an incident row** to the configured tracker — connecting the
detector to the recorder without a hand-migration step (the gap the
`self-evolution-loop` proposal closed). The row carries `Migrated From
Reflection = direct`, `Resolved By = pending`, and a `Recurrence-Window Match
= auto` placeholder (the recurrence is evaluated by the inference tool /
goodnight, not computed in the fail-safe commit hot path).

* **Impact tagging** mirrors the enforce decision (it bakes in the
  `coordination-tiers` enforce default): a **blocked** cross-claim →
  `prevented`; a **knowingly-overridden** one (`enforce=confirm` acknowledged)
  → `occurred`. A *no-token* committer's overlap is **not** recorded — ownership
  is unprovable, and tagging it would over-count the gate.
* **Best-effort & fail-safe (R1):** the append never blocks, slows, or fails a
  commit; on any error it warns visibly and skips (the commit is unaffected). It
  only ever *appends a row* — never a `git reset` or index mutation.
* **The tracker is auto-created** if absent (with a default `**Rolling window**:
  14 days` + a placeholder `## What counts`), so an incident is never silently
  dropped; the adopter then refines the `What counts` policy.
* **Configurable** via `dev/intent-config.json`: `incident_log_path` (default
  `dev/measurement/collision_log.md`) and `incident_event_class` (default
  `work-intent-claim-conflict`).

The goodnight migration remains the path for **reflection-sourced** incidents
and for **curating** auto-rows (filling `Resolved By`, reconciling
`Recurrence-Window Match`); the two are complementary.

## Adds to

The goodnight section of `dev/agent_collaboration.md > Goodnight
routine` (or its installed equivalent — see the `cairn:slot
goodnight-incident-tracker-migration` slot anchor).

## Merged into

> **Migrate incident-tracker entries.**  If a reflection reports an
> incident matching an event class defined in a tracker the
> deployment maintains (`dev/measurement/incident_log.md`,
> `dev/measurement/coordination_log.md`, etc. — per the deployment's
> `incident-trackers` module instantiation), migrate a one-line
> dated entry to the matching tracker table.
>
> The migrated entry MUST populate the `Impact` column
> (`occurred` / `prevented` / `non-conflict`) and SHOULD populate
> `Resolved By` if the resolution is already known; an unresolved
> `occurred` entry uses `pending` in `Resolved By`, which is the
> signal the rate-limit gate looks for when it bites on accumulated
> unresolved recurrences.  Prevented incidents (caught before
> propagating) and non-conflicts (looked like the failure mode but
> structurally weren't) are logged for base-rate visibility but do
> NOT count against the rate-limit gate's trigger.

## Cross-reference to `lifecycle-metrics`

The trackers feed the rate-limit gate; the `lifecycle-metrics`
module *correlates across* trackers (and across other durable
artifacts: proposals, plans, commits). The two modules compose:

* **`incident-trackers`** logs point-in-time events with the
  semantic-field schema.
* **`lifecycle-metrics`** correlates trackers over time and across
  classes for the cross-cutting signal.

The `lifecycle-metrics` module's eventual cross-adopter harvest
reads the canonical 7-column semantic-field contract; adopters with
existing trackers may ship a per-tracker schema-mapping file (e.g.,
`tracker_schema.yml`) documenting how their tracker's columns
project onto the canonical fields. Adopters using only the
canonical form ship no mapping; the harvest reads directly.

## Cross-reference to the rate-limit gate

`doctrine/rationale.md` > "Adaptive-doctrine rate-limit gate" is
the doctrine the trackers are the substrate for. The gate's
"recurrence" count operates on `Impact = occurred` rows within the
rolling-window boundary the adopter chose (typically 14 days; the
tracker's "What counts" sub-section pins the per-tracker boundary).

The gate is **machine-evaluable**, not normative-only: the
deterministic, zero-token `tools/evolution_infer.py` (installed with
this module; self-evolution-loop Part B) reads each tracker, sources
the rolling window from the tracker's `**Rolling window**:` line, counts
`Impact = occurred` rows of each event class within it, and **suggests**
a doctrine proposal when the count meets the recurrence threshold
(default `>=2`). It is **fail-closed**: a tracker whose rolling window
is unparseable is reported and not silently defaulted (the gate cannot
be evaluated until the adopter sets it). The tool **only suggests** —
the decision to open a proposal stays human. It also flags a **fold-up
backlog** from the fold-back ledger's open-candidate count. The full
handoff runs it read-only; run it any time with
`python tools/evolution_infer.py`.

## Forking the template

Adopters fork **one or many** instances of
`dev/modules/incident_log_template.md`, depending on the event-
class structure the deployment uses:

* **Single combined tracker** — copy the template once to
  `dev/measurement/incident_log.md`, define multiple event classes in the
  "What counts" section, log all incidents to one table.
* **Class-specific trackers** — copy the template multiple times
  to class-specific filenames under `dev/measurement/` (e.g.,
  `dev/measurement/collision_log.md` for staged-index incidents,
  `dev/measurement/coordination_log.md` for work-intent collisions).
  Each carries its own "What counts" + table.

The reference deployment (modflow_tools) runs class-specific
trackers; a smaller team typically runs one combined; a larger
multi-team deployment may run several.
