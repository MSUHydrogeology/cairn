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

Add a step in `docs/release-process.md` > “The cut” after the tag push: the
Maintainer creates the GitHub Release, or edits the existing Release for that
tag, using the prepared notes. The Maintainer checks the notes and opens the
source-download links, then runs a small read-only publication check. A pushed
tag alone does not create or update a GitHub Release. Link availability and
remote tag identity do not verify cached archive contents; neither force-push
nor editing Release metadata is prescribed as archive repair.

Proposed paths:
* `scripts/check_release_publication.py`
* `bootstrap/tests/test_check_release_publication.py`

`scripts/check_release_publication.py` takes the repository, tag and
**independently recorded full commit
id from the release security gate** as arguments. Using public GitHub Release
metadata and the remote Git tag ref, it refuses an absent or draft Release, a
wrong Release tag, a missing or ambiguous remote peeled tag, a different
peeled commit, and failed or malformed responses. It reports only publication
state and remote tag identity; it does not publish, edit, authenticate tag
signatures, read notes for correctness or inspect archive bytes. A missing
read-only response is incomplete, never success. No publishing credential is
needed. The plan defines the exact endpoint and Git invocation before code.

In the same guide edit, replace its “signed or on a Maintainer-approved
release commit” alternative (`docs/release-process.md:142-143`) with the
existing signed-tag requirement. `bootstrap/PROVENANCE.md:29` and
`bootstrap/PROVENANCE.md:398` require `git tag -s` after the gate on the
same commit; the accepted
release-authenticity record retired the approved-commit alternative
(`dev/proposals/archive/2026-08-03-claude-release-authenticity.md:314`).
This correction and the script widen the opened scope and require a fresh
review and Maintainer Decision. No push or publication is authorized here.

## Rationale

The guide already prepares notes. A short script makes the release-state and
remote-commit comparison repeatable while leaving publication and note reading
with the Maintainer. It needs only public reads and no stored release state.
GitHub's archive caching prevents an archive-content claim from this check.

## Alternatives considered

Keep the guide unchanged: a Maintainer can push a tag and think the Release
was updated. Copy the board's “force-push then re-save” sentence: it would
teach an unverified archive guarantee and may conflict with immutable
releases. Automate publication: it needs write credentials and failure modes
for a Maintainer action. Rely only on manual comparison: repeated hand checks
can miss a draft or wrong tag; the read-only script is narrower.

## Documentation / doctrine surface

This changes the release cut in `docs/release-process.md` and adds an internal
read-only script with owning tests. It also corrects that guide's contradictory
tag sentence to match the accepted provenance contract. No doctrine or
adopter template changes. The Maintainer's Decision authorizes both additions.

## Evidence / verification plan

### Tests required

Test `bootstrap/tests/test_check_release_publication.py` through the public
script command with local Git refs and stubbed Release replies:
published matching control; absent, draft, wrong tag, wrong commit, missing or
ambiguous peeled ref, malformed and failed response. The expected full commit
must come from a separate argument, not the Release. Search for guide readers
and byte pins before implementation. Review the guide against the accepted
signed-tag contract and current GitHub documentation. Implementation checks
follow the reviewed plan; no full suite is run for proposal prose.

### Examples / smoke checks

Run `python scripts/claim_check.py docs/release-process.md`,
`python scripts/link_check.py docs/release-process.md`, and
`python scripts/check_cairn.py docs/release-process.md`. Check the script's
public invocation against recorded gate and remote inputs in an isolated
fixture; no live Release, tag, push or publication is made for the proposal.

#### Security preflight — five questions, answered in writing

* **S1.** The Maintainer supplies the expected gate commit and tag separately;
  GitHub supplies Release metadata and the remote tag ref. Neither expected
  commit nor tag is derived from the Release being checked.
* **S2.** A wrong peeled ref or draft/missing Release must fail. Fixture
  mutations for these cases are planned, not yet run; no script exists now.
* **S3.** The human cut invokes the script after the tag push for one named
  repository, tag and expected commit. The guide will say it checks published
  Release state and remote tag identity, not cached archive contents.
* **S4.** Missing, malformed, ambiguous or failed remote replies refuse. No
  fallback to the local tag, Release target or guessed commit is allowed.
* **S5.** A compromised GitHub response or falsely transcribed gate commit can
  still pass. The script checks omission and mismatch, not provenance
  authentication or archive bytes.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The guide lets a tag push stand in for a GitHub Release, retains the retired
unsigned-tag alternative, implies cached archive identity, or the script
passes a draft/missing Release or a remote tag on the wrong gate commit.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — release ceremony and read-only remote check.

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

## Response -- Codex GPT-6.1 Sol (Strategy) -- 2026-10-30

**PR1 — accepted with widened scope.** The operative proposal now names a
read-only script, independent expected gate commit, public Release-state and
remote peeled-tag checks, refusal cases, and a create-or-edit path for an
existing Release. The Maintainer still publishes and reads the notes. This
adds code and tests, but no publishing credential or automated publication.
The endpoint and Git command are plan questions; the public command and
negative fixtures are acceptance evidence.

**PR2 and SR1 — accepted.** The guide will separate opened source links from
the remote tag comparison. Neither proves cached archive contents. I removed
the opening's claim that the Release “presents the intended source commit.”

**SR2 — accepted as a named scope expansion for Decision.** The current guide
offers an unsigned approved-commit path while the accepted provenance contract
requires `git tag -s` for v0.4.0 onward. The revised proposal recommends
correcting that sentence in the same guide edit, citing both the controlling
text and its accepted proposal. I have not made that Decision or changed the
guide. Publication guidance must not ship with the conflict unresolved.

The two expansions require a fresh ordinary review and second Security Review
of the widened proposal before a Maintainer Decision. The script's network and
Git reads need that review; no live call or implementation was run here.

**Elapsed**: about 3 minutes
**Tokens**: unknown

### Withdrawn / superseded commitments

The opening's doc-only approach and its implication that a Release presents
the intended source commit are superseded. The publication distinction,
Maintainer action, note and link read-back, and remote commit comparison remain.

## Review -- Codex GPT-6.1 Sol (Reviewer) -- 2026-10-30

```
Reviewed commit: fbcd6ab0
Target: widened proposal; checker, signing, cost and maintenance
Prior findings: PR1-PR2 and SR1-SR2; author response at fbcd6ab0
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: none
**Verdict**: ADVANCE after the separate Security Review and author response.

**Foundations**:

1. **Should this happen as framed?** Yes. The cut prepares notes and pushes a tag without naming publication (`docs/release-process.md:133-145`); GitHub documents publishing separately. The script checks a recurring omission while the Maintainer publishes and reads notes.
2. **Best alternative.** Manual read-back avoids code but repeats comparisons every release. A small read-only script fits the Maintainer's preference for scripted comparisons (`dev/PLANNING.md:126`); no existing release checker appeared in `rg --files scripts tools | rg 'release|tag|publish|github'` (positive control: `scripts/bootstrap_github_labels.py`).
3. **What would show it wrong?** A wrong remote tag commit passing the public command would defeat the design. Proposed public-entry fixtures include that case, draft and absent Releases, malformed replies and ambiguous peeled refs (proposal Tests required, S1-S4).

The revision addresses PR1-PR2 and SR1-SR2 in its wording: it names the command and create-or-edit path, limits archive claims, and cites the signed-tag contract (`bootstrap/PROVENANCE.md:29`, `bootstrap/PROVENANCE.md:398`). The plan must specify the endpoint, Git invocation, failure output and public-command tests. The script adds maintenance, but no publishing credential or stored state. A failed public read remains incomplete.

**Covered**: claims and drift (`docs/release-process.md:133-145`); public path, design and fail-closed cases (proposal Tests required, S1-S4); reuse search above; cross-document signing (`bootstrap/PROVENANCE.md:29`); lifecycle and scope (proposal Proposal, Alternatives); satisfier (plan and tests). **Not covered**: no live GitHub response, remote tag, archive, signature or implementation was exercised. Security Review remains open.

**Elapsed**: about 7 minutes. **Tokens**: estimated 5,000.

## Review -- Codex GPT-6 (Security Reviewer) -- 2026-10-30

```
Reviewed commit: fbcd6ab0
Target: widened release publication proposal and prior Security findings
Prior findings: SR1, SR2
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: approximately 2 minutes
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes: the revised check compares independent gate evidence to the remote tag and refuses missing or ambiguous responses, without asserting archive integrity. -- proposal Proposal and S1-S5
2. **Best alternative.** Keep the Maintainer's publication and notes inspection, with a read-only check; manual comparison alone leaves repeatable omission and mismatch checks to memory. -- proposal Alternatives and Tests required
3. **What would show it wrong?** A published-state check passing a draft, missing Release or mismatched tag, or identifying the expected commit from the response itself, would defeat the stated boundary. -- proposal S1-S4 and Tests required

SR1 is closed: the revision explicitly limits the link check and disclaims
cached archive verification. SR2 is closed in the proposed contract: the cut
will require a signed tag on the gate-checked commit, consistent with
`bootstrap/PROVENANCE.md:398-407`. The withdrawal ledger accounts for the
superseded doc-only approach and archive implication while retaining the
original publication outcome. The exact endpoint, Git invocation and executable
negative tests remain for the plan and implementation; their results are not
claimed here.

**Covered**: prior findings, trust inputs and refusal paths, release cut and
signing consistency (`docs/release-process.md:133-143`,
`bootstrap/PROVENANCE.md:398-415`), and withdrawal ledger. **Not covered**: no
live GitHub, network, tag, archive or implementation test was performed.
