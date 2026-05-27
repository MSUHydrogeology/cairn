# Fold-back ledger — {{project_name}} → Cairn

The holding pen for **Cairn-bound candidates**: generalizable
improvements proven here that should fold *up* into the Cairn
methodology so every adopter gets the proven version. This is the
deployment-side push. This file is self-contained for day-to-day use
(the status vocabulary, removal rule, and export-safety warning are all
below); the full rationale — lifecycle, the harvest relationship, the
export boundary — lives in Cairn's published methodology doctrine
(`doctrine/fold-back.md` in the **Cairn** repository, not a file in this
repo).

> **[SECURITY WARNING]** This ledger is a **cross-repository export
> surface** — its candidates are destined for *public* Cairn. Ledger
> entries carry:
> **no secrets, credentials, internal hostnames/IPs, local paths, or proprietary domain detail**.
> Describe a candidate in generalizable terms; if you cannot describe it
> without a private coordinate, it is not yet ready to capture. Before
> any item becomes a public Cairn proposal, the Maintainer confirms no
> private coordinate leaks (the upstream-submission scrub gate).

## Status vocabulary

* `candidate` — captured; not yet committed to a sync.
* `queued` — selected for the next sync.
* `scoped → <proposal>` — a tracked Cairn proposal has taken it over.
* `synced` — shipped into Cairn (transient; moves to **Already synced**
  or is deleted per the removal rule).
* `dropped` — decided not to port, with a one-line reason.

**Removal rule:** a row is deleted once `synced` *and* the archived Cairn
proposal carries the durable record; a `dropped` row is deleted with its
reason in the commit. The open-candidate set is this file's load-bearing
content; **Already synced** is a terse cadence log only.

## Open candidates

| Candidate | Type | Size | Status | Source |
|---|---|---|---|---|

*(Empty at adoption. The goodnight foldback-capture step adds rows as
Cairn-portable doctrine surfaces here.)*

## Already synced

A terse cadence record; the durable per-item detail lives in each
archived Cairn proposal.

| Sync | Shipped | Cairn | Record |
|---|---|---|---|
