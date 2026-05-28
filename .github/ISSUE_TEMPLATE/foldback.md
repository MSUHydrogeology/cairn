---
name: Fold-back from a deployment
about: A Cairn-portable improvement surfaced from a deployment's fold-back ledger via the active-surfacing protocol
title: '[Fold-back from <deployment>] <short description>'
labels: ['foldback']
assignees: []
---

<!-- Generated via the active-surfacing protocol; see
     cairn/doctrine/fold-back.md > "Active surfacing" for the
     deliberation context.

     The maintainer of the source deployment fills the sections below
     before submitting.  An AI agent may have drafted the body from
     the deployment's ledger entry, but the maintainer reviews +
     submits by hand (the agent does not submit autonomously, per
     the export-boundary bright-line).
-->

## Source deployment

<!-- The deployment repository this fold-back originated from.
     Include enough context that a Cairn maintainer can locate the
     proving artifacts: repo name, the relevant proposal/plan stem(s),
     and the commit range that demonstrates the candidate. -->

## Candidate description

<!-- One paragraph: what is the generalizable improvement?  Frame it
     in vendor-neutral, deployment-shape-neutral terms (Cairn's R-G
     vendor-neutrality discipline applies).  Avoid project-specific
     terminology unless explicitly cross-referenced under the
     export-safety affirmation below. -->

## Generalizability test

<!-- The harvest-doctrine question: would a differently-shaped team
     hit the same need?  One paragraph of evidence.  Deployment-local
     quirks (the deployment's own tools, naming, science) do NOT fold
     back -- only what crosses the generalizability bar belongs here. -->

## Proven by

<!-- Cite the deployment commits / archived proposal / archived plan
     that demonstrate the candidate works in practice.  This is the
     evidence the foldback rides on. -->

* Commit(s):
* Archived proposal:
* Archived plan:

## Suggested disposition

<!-- The active-surfacing protocol's Choose step lands a candidate on
     one of these four disposition lines.  Check one: -->

- [ ] **Cairn proposal** -- this candidate warrants a full Cairn proposal-lifecycle pass
- [ ] **Cairn doctrine sharpening** -- a `cairn/doctrine/` edit captures it
- [ ] **Cairn templates / module update** -- a `cairn/templates/modules/` change carries it
- [ ] **Other (described below)**

## Export-safety affirmation

<!-- The maintainer-signed manual half of the active-surfacing two-gate
     export boundary.  The machine half (foldback_export_scan.py) ran
     fail-closed against the drafted body before submission; this
     manual affirmation covers the two no-export classes the scanner
     cannot reliably detect. -->

I affirm that, to the best of my judgment, this issue body contains:

- [ ] **No unpublished data hints** -- no descriptive references to
  data, results, or findings that have not been published by the
  source deployment.
- [ ] **No proprietary domain detail** -- no client / project /
  customer specifics whose generalized form would be acceptable but
  whose verbatim shape is not.

The machine-half scrub (`python scripts/foldback_export_scan.py
<draft>`) exited cleanly OR every finding was edited / explicitly
dispositioned as a documented false positive before this submission.

---

<!-- Cairn maintainers reviewing this issue: see
     cairn/doctrine/fold-back.md for the active-surfacing protocol
     this filing came through, and cairn/doctrine/fold-back.md
     > "The export boundary" for the no-export class taxonomy this
     affirmation covers. -->
