<!-- Cairn fold-back PR template.

     Generated via the active-surfacing protocol when a deployment
     has working code to contribute (not just an idea); see
     cairn/doctrine/fold-back.md > "Active surfacing" for the
     deliberation context.

     The maintainer of the source deployment fills the sections below
     before submitting.  An AI agent may have drafted the body from
     the deployment's ledger entry + the PR diff, but the maintainer
     reviews + submits by hand (the agent does not submit
     autonomously, per the export-boundary bright-line). -->

## Source proposal / plan

<!-- The deployment-side lifecycle artifact that approved this
     contribution: the archived proposal stem (and its plan, if
     any).  The artifact carries the deliberation rationale; this PR
     is the implementation crossing into Cairn. -->

## What changes in Cairn

<!-- Per-surface inventory.  For each Cairn surface touched, name
     the surface + the substantive change.  Keep this skimmable -- a
     Cairn maintainer reads it cold. -->

* `cairn/doctrine/<file>.md`:
* `cairn/templates/modules/<file>`:
* `cairn/scripts/<file>.py`:

## Tests added / extended

<!-- Cairn's test apparatus is `bootstrap/tests/`.  Name the test
     files this PR adds / extends, and the load-bearing surfaces
     each pins.  The contribution is not landable without
     test coverage matching the contribution's surface. -->

* `cairn/bootstrap/tests/test_<file>.py`:

## Deployment-side cross-link

<!-- The deployment's archived proposal + plan (URLs or stem
     references) that drove this contribution.  Cairn maintainers
     reading this PR may want the deliberation context. -->

## Export-safety affirmation

<!-- The maintainer-signed manual half of the active-surfacing
     two-gate export boundary.  The machine half
     (foldback_export_scan.py) ran fail-closed against this PR's
     body AND every changed file in the diff before submission; this
     manual affirmation covers the two no-export classes the scanner
     cannot reliably detect. -->

I affirm that, to the best of my judgment, this PR's body AND every
file it adds / modifies contain:

- [ ] **No unpublished data hints** -- no descriptive references to
  data, results, or findings that have not been published by the
  source deployment.
- [ ] **No proprietary domain detail** -- no client / project /
  customer specifics whose generalized form would be acceptable but
  whose verbatim shape is not.

The machine-half scrub
(`python scripts/foldback_export_scan.py <draft>` AND
`python scripts/foldback_export_scan.py <each-changed-file>`)
exited cleanly OR every finding was edited / explicitly
dispositioned as a documented false positive before this submission.

---

<!-- Cairn maintainers reviewing this PR: see
     cairn/doctrine/fold-back.md for the active-surfacing protocol
     this contribution came through.  Squash-merge per Cairn
     convention; the deployment-side archived artifacts (above) are
     the durable deliberation home. -->
