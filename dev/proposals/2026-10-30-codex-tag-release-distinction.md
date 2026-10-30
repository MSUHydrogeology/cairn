# Name the GitHub Release as a separate release-cut step

**Author**: Codex GPT-6.1 Sol (Strategy)
**Status**: revising
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

## Review -- Codex GPT-6 Astra (Reviewer) -- 2026-10-30

```
Reviewed commit: cead97a6
Target: the whole proposal, with release correctness, script reuse, staffing and cost in focus
Prior findings: none
Assurance path: high-assurance (as declared)
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** Yes to separating publication from the tag push; no to leaving the independent check as an unspecified manual read. `docs/release-process.md:133-145` prepares notes and pushes a tag but never publishes a Release; GitHub's [release instructions](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) make publication a separate action.
2. **Best alternative.** Keep the Maintainer's publication decision and action in the cut, but provide a small read-only check of the selected published Release and the remote tag against the recorded release-gate commit. This needs no publishing credential or automatic publication; `docs/release-process.md:138-144` already supplies the expected commit, and `dev/PLANNING.md`'s “The ceremony as two commands” row records the Maintainer's preference for a script over hand comparisons.
3. **What would show it wrong.** If the cut can publish the wrong or missing Release while the proposed read-back appears to pass, the check is insufficient. A pre-existing Release with stale notes, a draft, or a tag pointing to a different commit are concrete cases; the proposal's S1-S4 and GitHub's [create/edit distinction](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) expose them.

### Findings

**PR1 (blocking) — Specify the executable check and existing-Release path.** The proposal says “publish,” then “check,” but neither names a command comparing the remote tag's peeled commit with an independently supplied expected commit, nor says what to do if the Release already exists. A tag label and source links can mistake availability for provenance. The automation alternative assigns a credential cost to *checking* that belongs to *publishing*. Recommend a read-only script or existing command that takes the expected commit as input, checks the published Release's tag and state plus the remote peeled tag, and fails on absence or mismatch. The guide can direct the Maintainer to create or edit the Release and inspect its notes. Close with an invocation, negative cases for missing, draft and wrong-commit Releases, and a manual notes check. Evidence: proposal S1-S4; `docs/release-process.md:138-144`; GitHub [release instructions](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

**PR2 (non-blocking) — Bound the archive claim.** Checking that source-download links open does not establish that a cached tag archive contains the intended commit's files. GitHub says tag archives are cached and later downloads can differ after a tag moves. Recommend wording the read-back as link availability plus remote tag identity, without calling it archive-content verification; any content guarantee needs a separately specified check. Evidence: proposal Rationale/S3; GitHub [archive stability](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives).

### Cost and scope

The current proposal's one-file wording still incurs a proposal decision, usual and Security reviews, a plan with Internal and Internal Security reviews, and code reviews under its declared path. A script adds code, tests and maintenance; it also removes repeated hand comparison at each cut. I would pay that one-time cost if the check is actually enforced, but keep publication itself Maintainer-operated. Doing nothing preserves the demonstrated omission (`dev/PLANNING.md`, release-process row). This recommendation expands the proposed implementation; the author and Maintainer decide whether to accept it. The usual pass does not clear the separate Security Review.

**Covered**: claims and drift (`docs/release-process.md:133-145`, `dev/PLANNING.md` release row); test path and fail-closed design (proposal S1-S4 and the negative cases in PR1); cross-document consistency and reuse (`rg --files scripts tools | rg 'release|tag|publish|github'` found no release-publishing helper); lifecycle placement (`docs/release-process.md` > “The cut”); scope and cost (proposal Alternatives and `doctrine/plans.md` > “Plan triage rule”); satisfiers (PR1-PR2).
**Not covered / low confidence**: no live GitHub Release, remote tag, cached download or authenticated GitHub command was exercised; this is a proposal read, not an implementation test.

## Review -- Codex GPT-6 (Security Reviewer) -- 2026-10-30

```
Reviewed commit: cead97a6
Target: proposal and release-publication trust boundary
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** Separate publication is needed, but the proposed evidence must not imply that a link and tag check proves the bytes of a cached source archive. The existing source-provenance control authenticates a signed tag, not a download's materialized tree. -- proposal Rationale and S3; `bootstrap/PROVENANCE.md:359-375`
2. **Best alternative.** Keep publication with the Maintainer and use a small read-only check with the independently supplied gate commit for the remote tag and published Release; inspect notes separately and describe archive-link availability as such. A check needs no publishing authority. -- `docs/release-process.md:133-143`; proposal S1-S4
3. **What would show it wrong?** A moved tag with a stale cached archive, a draft or absent Release, or a mismatched remote tag that the proposed check reports as a successful publication would disprove its claimed coverage. -- proposal S2-S3; `bootstrap/PROVENANCE.md:402-415`

### Findings

**SR1 (blocking) — Separate archive availability from content identity.** A
remote peeled tag and working download links do not establish which tree a
cached archive contains. The rationale says the Release presents the intended
source commit, while S3 excludes checking cached downloads. Specify that the
check proves only the remote tag's relationship to the recorded gate commit and
that links are available; do not describe archive contents as verified. If
archive identity is an intended outcome, specify an independent content check
and its failure case instead. This preserves the proposed publication check
without claiming protection it does not provide. Evidence: proposal Proposal,
Rationale and S1-S3; `bootstrap/PROVENANCE.md:359-375`.

**SR2 (blocking) — Resolve the signing conflict at the cut.** The proposal
preserves the guide's existing alternative of an annotated tag on an approved
commit, but `bootstrap/PROVENANCE.md:29-32` and `:396-406` require a signed
release tag and explicitly retire that alternative. A newly explicit
publication step could complete a release that fails the published provenance
contract. Recommend making the cut refer to the signed-tag requirement and
retaining the security-gate commit comparison; this repairs an existing
inconsistency and requires the Maintainer's decision on the expanded scope.

A read-only helper, if adopted, should reject absent, draft and mismatched
Releases and failed or ambiguous remote responses, take the gate commit as an
independent input, and avoid publishing credentials. The plan should define its
actual endpoint, tag peeling and negative tests; a remote response and the
expected commit are different trust inputs. This is a design recommendation,
not evidence that such a helper already exists.

**Covered**: release identity and provenance (`bootstrap/PROVENANCE.md:26-58`,
`:387-420`); cut ordering (`docs/release-process.md:120-150`); proposal's five
security answers and expected failure behavior; feasible read-only alternative.
**Not covered**: no live Release, network response, archive bytes, tag signing,
or publishing credentials were exercised; no implementation exists to test.
