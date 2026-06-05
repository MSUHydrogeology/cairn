<!-- cairn-internal-ref-allow: doctrine/fold-back.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
# Module: fold-back-ledger

**Selected when:** default-on — kept by every deployment that may ever
contribute doctrine back to Cairn (i.e. nearly all). A solo,
single-deployment adopter that will never fold improvements up may omit
it; the cost of keeping it is one mostly-empty file and a cheap nightly
glance, and the payoff is that a generalizable improvement is never
silently lost.
**Adds to:** a tracked fold-back ledger at `dev/.cairn/` (installed
from this module's template), plus a goodnight **foldback-capture** step
in the session-routines / goodnight doctrine.

The fold-back ledger is the **deployment-side improvement channel**: the
standing mechanism by which this deployment feeds generalizable doctrine
*up* into Cairn, so every adopter benefits from what was proven here. It
is the push that complements Cairn's framework-side harvest pull. This
module ships a **self-contained** working artifact (the installed ledger
carries the status vocabulary, removal rule, and export-safety warning)
and wires the capture cadence. The full *rationale* — lifecycle, the
harvest relationship, the export boundary — lives in Cairn's published
methodology doctrine (`doctrine/fold-back.md` in the **Cairn**
repository, not a file in this adopter repo).

## What the module installs

* The forkable **ledger** itself, at `dev/.cairn/` — a starter file
  carrying the `[SECURITY WARNING]` export-safety header, the status
  vocabulary, the removal rule, and the open-candidate / already-synced
  split.

## Template content

Merged into the session-routines / goodnight doctrine (or its
equivalent), gated on this module being installed:

> **Goodnight foldback-capture.** When this deployment runs the
> fold-back-ledger module, the goodnight full-handoff owner adds a
> standing step: scan the session-day's doctrine activity for
> Cairn-portable candidates and capture each in the fold-back ledger.
> Capture never lapses; an **empty capture is success** (do not
> manufacture marginal candidates). Whether to *open a sync* upstream is
> the separate, judgment-gated decision the harvest cadence governs.
> **Export safety:** ledger candidates carry no secrets, credentials,
> internal hostnames/IPs, local paths, or proprietary domain detail, and
> the Maintainer confirms no private coordinate leaks before any item
> becomes a public Cairn proposal.
>
> **Goodnight foldback-surfacing.** Adjacent to foldback-capture above,
> after the day's candidates are captured the goodnight full-handoff
> owner reviews open `candidate`-status rows older than a maintainer-
> tunable grace period (default **7 days**; configurable per
> deployment) AND not currently snoozed via a `deferred-until` ISO
> date or condition string.  For each, the agent runs the
> **active-surfacing protocol** (see Cairn's [`doctrine/fold-back.md`](../../doctrine/fold-back.md)
> > "Active surfacing"): Recap / Choose / Compose / Scrub / Submit /
> Record.  The Scrub step is a **fail-closed machine gate** --
> `python scripts/foldback_export_scan.py <draft-path>` (the export
> scanner; this module installs it alongside the ledger) must exit 0
> before the maintainer submits; non-zero fails closed.  The
> maintainer submits any filing **by hand** via
> `gh issue create --body-file <draft.md>` (or the GitHub UI) -- the
> agent never submits autonomously.  On submission, the row's status
> flips from `candidate` to `filed -> <issue-#>` or `pr -> <pr-#>`.
> Surfacing never lapses; an empty open-candidate set is success
> (mirroring the capture-side rule).

A solo, single-deployment adopter may omit this module; the upstream
improvement loop only earns its keep when the deployment intends to
contribute doctrine back.
