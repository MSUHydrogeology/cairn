# Name the GitHub Release as a separate release-cut step

**Author**: Codex GPT-6.1 Sol (Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: The release guide should say that pushing a tag and publishing its GitHub Release are separate steps.

## Context

The release guide's cut list names GitHub release notes and a pushed annotated
tag but does not explicitly tell the Maintainer to publish or check the GitHub
Release page (`docs/release-process.md:121-145`). The v0.6 board records a
missed Release after a tag update, but its assertion that force-pushing a tag
cannot update source tarballs is too strong. GitHub says tag-named source
archives are generated on request and later downloads **may differ if the
tag moves** ([source archives](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives)).
GitHub separately documents creating and editing a Release
([managing releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)).
An immutable Release may forbid moving its tag, so neither a forced tag push
nor “re-save the Release” is a general archive-repair step.

## Proposal

Add a short step in `docs/release-process.md` > “The cut” after the tag push:
the Maintainer publishes the GitHub Release separately, using the prepared
notes, then checks its tag, notes and source-download links and confirms that
the remote tag resolves to the intended release commit. State that a pushed
tag alone does not create or update a GitHub Release. Do not instruct a
force-push or promise that editing
Release metadata refreshes cached archives. The existing release commit,
tag-signing, provenance and gate requirements remain as written; this
proposal does not authorize a push or publication.

## Rationale

The guide already prepares notes, so one explicit publication and read-back
step closes the ambiguity without a new script or checklist. GitHub's archive
behavior is conditional on tag movement and caching; the durable check is
that the published Release names the intended tag and presents the intended
source commit, not an assumed archive refresh operation.

## Alternatives considered

Keep the guide unchanged: a Maintainer can push a tag and think the Release
was updated. Copy the board's “force-push then re-save” sentence: it would
teach an unverified archive guarantee and may conflict with immutable
releases. Add automation: new publishing credentials and failure modes for
one missing instruction, contrary to the current cost restraint.

## Documentation / doctrine surface

This changes one prescriptive release step in `docs/release-process.md`;
the board remains the queue, and the released methodology doctrine is
unchanged. The Maintainer's Decision authorizes the wording before it lands.

## Evidence / verification plan

### Tests required

Search for readers of `docs/release-process.md`; none was found under
`bootstrap/tests/` at opening. Re-run that search at implementation. This
is prose that no test or manifest pins, so verify its claim and references
rather than running the suite. A reviewer checks the new step against the
existing cut order and GitHub's current documentation.

### Examples / smoke checks

Run `python scripts/claim_check.py docs/release-process.md`,
`python scripts/link_check.py docs/release-process.md`, and
`python scripts/check_cairn.py docs/release-process.md`. No live tag,
Release or push is created to test prose.

#### Security preflight — five questions, answered in writing

* **S1.** The Maintainer supplies the release commit, tag and notes; GitHub
  supplies the Release page, source links and remote tag ref. Compare the
  remote tag's peeled commit with the already recorded release-gate commit;
  the page's own tag label alone cannot attest that commit.
* **S2.** A wrong remote tag commit must fail comparison with the recorded
  release-gate commit; wrong notes or a missing Release remain visible on the
  page. No publishing operation will be run for this proposal.
* **S3.** The human-run cut triggers this step after the tag push. It covers
  the selected Release page and the remote tag's peeled commit; it does not
  inspect every cached download over time.
* **S4.** A missing or mismatched Release is incomplete publication; do not
  infer success from the tag push. The guide leaves correction to a separate
  Maintainer decision, rather than guessing whether a tag is mutable.
* **S5.** A Maintainer can knowingly publish the wrong Release or trust a
  compromised GitHub page. This step prevents accidental omission, not
  malicious publication or remote compromise.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The guide still lets a tag push stand in for a GitHub Release, the new words
claim a forced tag move always refreshes archives, or the check cannot name
the intended release commit.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — release ceremony wording.
