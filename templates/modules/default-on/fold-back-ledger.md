# Module: fold-back-ledger

**Selected when:** default-on — kept by every deployment that may ever
contribute doctrine back to Cairn (i.e. nearly all). A solo,
single-deployment adopter that will never fold improvements up may omit
it; the cost of keeping it is one mostly-empty file and a cheap nightly
glance, and the payoff is that a generalizable improvement is never
silently lost.
**Adds to:** a tracked fold-back ledger at `dev/upstream/` (installed
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

* The forkable **ledger** itself, at `dev/upstream/` — a starter file
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

A solo, single-deployment adopter may omit this module; the upstream
improvement loop only earns its keep when the deployment intends to
contribute doctrine back.
