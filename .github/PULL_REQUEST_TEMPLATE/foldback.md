<!-- Cairn fold-back PR template.

     For a deployment with working code to contribute, not just an
     idea.  The fold-back ledger and its doctrine were retired
     2026-08-26; a Cairn PR IS the channel now, and this template is
     the surviving statement of the protocol.

     The maintainer of the source deployment fills the sections below
     before submitting.  An AI agent may have drafted the body from
     the PR diff, but the maintainer reviews + submits by hand (the
     agent does not submit autonomously, per the export-boundary
     bright-line). -->

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

<!-- This affirmation is now the WHOLE export boundary, not half of
     one.  The machine-half scrub (foldback_export_scan.py) was
     retired with the fold-back ledger on 2026-08-26; it is not
     available, and no command replaces it. -->

I affirm that, to the best of my judgment, this PR's body AND every
file it adds / modifies contain:

- [ ] **No unpublished data hints** -- no descriptive references to
  data, results, or findings that have not been published by the
  source deployment.
- [ ] **No proprietary domain detail** -- no client / project /
  customer specifics whose generalized form would be acceptable but
  whose verbatim shape is not.

- [ ] **I read the diff once more with those two classes in mind**,
  after writing it -- not only while writing it.

**There is no machine-half scrub.** `foldback_export_scan.py` was retired
with the fold-back ledger on 2026-08-26 and no command replaces it, so this
affirmation is the whole export boundary rather than a second opinion on a
scanner's output. A Cairn pull request is **public**; every changed file
carries the same obligation as the description.

---

<!-- Cairn maintainers reviewing this PR: the fold-back doctrine that
     defined this protocol was retired 2026-08-26 along with the
     ledger; this template is the surviving statement of it.  Squash-merge per Cairn
     convention; the deployment-side archived artifacts (above) are
     the durable deliberation home. -->
