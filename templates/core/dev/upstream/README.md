# `dev/upstream/` — things that flow out of this repo

This directory holds work destined for repositories **upstream** of
{{project_name}}: **bug reports, capability gaps, and evidence bundles to
file against external OSS the project depends on.** Each is a draft file at
this level (e.g. `some-lib-issue-slug.md`) carrying reproduction steps,
environment details, expected/actual behavior, and filing status.

## Lifecycle — draft to archive

```
draft file at dev/upstream/  →  filed / resolved / superseded / abandoned
                                         ↓
                                   dev/upstream/archive/
```

* Each draft lives at `dev/upstream/<slug>.md` until its upstream fate is
  decided.
* **File externally only when the Maintainer asks or approves.** The draft
  is the working form; the external issue / PR is the publication step.
* Move to [`archive/`](archive/) once the issue is filed, resolved,
  superseded by a later finding, or abandoned as not-worth-pursuing.
  A moved file is `archived` by its location — do not edit it further
  unless updating the filing status.
* **Empty at adoption.** This directory ships with only this README (and
  the tracked `archive/` placeholder). Add draft files as external-dep
  issues surface.

## Boundary: code-dependency channel vs methodology channel

This directory is the **code-dependency channel** — issues in the external
OSS libraries and tools {{project_name}} uses.

It is **not** the methodology channel. If {{project_name}} runs the Cairn
methodology and discovers an improvement to Cairn's *own* doctrine or
tooling, that belongs in `dev/.cairn/cairn_foldback.md` (the fold-back
ledger, installed by the `fold-back-ledger` module), not here.

| Channel | Home | What it carries |
|---------|------|-----------------|
| Code dependencies | `dev/upstream/` (this folder) | Bug reports + capability gaps in external OSS |
| Methodology | `dev/.cairn/cairn_foldback.md` | Improvements to the Cairn methodology itself |

A finding that spans both (e.g. a dependency bug that also reveals a gap in
Cairn's review doctrine) gets a file here for the upstream code report and
a row in the fold-back ledger for the methodology takeaway.

## What a draft file contains

A minimal draft carries enough for an upstream maintainer to reproduce and
triage. See [`_template.md`](_template.md) for the suggested shape.
Drafts that are not yet ready for filing can use loose notes; clean them up
before submitting.

See [`../README.md`](../README.md) for the full `dev/` subdirectory map.
