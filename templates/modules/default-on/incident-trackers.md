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
