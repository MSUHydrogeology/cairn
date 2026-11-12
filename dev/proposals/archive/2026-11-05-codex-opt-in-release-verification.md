# Make adopter release verification an explicit choice

**Author**: Codex Sol (High)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Install or upgrade an official named release without signing-key setup, while keeping signature verification available by explicit choice.

## Decision summary

Make the ordinary adopter workflow trust the official GitHub distribution
channel, not require a separately established signing key. Record the selected
version and commit; require neither fingerprint approval nor a signature waiver.
Keep the existing stronger verification procedure optional and fail-closed when
chosen. This removes work, not risk: testing and review assess content, file
hashes detect certain changes, and signatures separately authenticate a key holder.
No policy changes take effect through this proposal alone.
The complete release selection is a manual record in the adopter's own Git
history, not a claim that today's lockfile contains a full commit ID.

## Context

[Issue #52](https://github.com/MSUHydrogeology/cairn/issues/52), board item 7e
in `dev/PLANNING.md`, reports an LHM upgrade stopping for signing-key confirmation
despite selecting the official v0.6.1 release. The issue explicitly identifies a
procedure/agent blocker, not a demonstrated CLI refusal.

The [v0.6.1 provenance document](https://github.com/MSUHydrogeology/cairn/blob/v0.6.1/bootstrap/PROVENANCE.md)
and current `bootstrap/PROVENANCE.md` are byte-identical (`git diff v0.6.1 HEAD
-- bootstrap/PROVENANCE.md`, no differences at authoring). They call independent
fingerprint comparison and a human-written external roster the primary path.
Inspection of `bootstrap/_scaffold/cli.py`, `install.py`, and `upgrade.py`
finds no release-roster gate; `git_provenance_warning` is advisory. In contrast,
`bootstrap/container/verify-ref.sh` requires a roster in its default signature
mode; `test_provenance_mode_requires_a_roster` is a known-positive reader/check.

The [v0.6.1 release notes](https://github.com/MSUHydrogeology/cairn/releases/tag/v0.6.1)
name candidate `977b5250abed59badd06b4940dccd39324644705` and explicitly report
unpassed strict-runner evidence and release-specific exceptions. Official
publication must not be described as an all-green test certificate.

## Proposal

Deliver one coherent v0.7 documentation/policy change after acceptance and a
reviewed plan; coordinate the upgrade walkthrough with board item 7d without
depending on its broader growth trial.

1. Before candidate execution, fix owner `MSUHydrogeology`, repository `cairn`,
   and the explicitly requested release tag outside the candidate. Construct
   the release page as `https://github.com/MSUHydrogeology/cairn/releases/tag/`
   plus that tag, and the API request as
   `https://api.github.com/repos/MSUHydrogeology/cairn/releases/tags/`
   plus its percent-encoded tag component. Require HTTP 200 without following
   redirects, exact returned `tag_name` and canonical `html_url`, `draft=false`,
   `prerelease=false`, and a publication timestamp. Read the selected version
   and full expected commit from those release notes before fetching, never
   from candidate HEAD or `target_commitish` (which may name a branch).
   Missing or ambiguous full commit evidence stops selection.

   Fetch only the exact `refs/tags/<selected-tag>` from the fixed literal
   `https://github.com/MSUHydrogeology/cairn.git` into a fresh operator-created
   repository. Use trusted system Git, no candidate configuration/hooks,
   isolated system/global/environment configuration, no URL rewriting and
   `http.followRedirects=false`. Do not use an existing `origin`, cached local
   tag, release-supplied clone URL, fork, redirect or alternate ref. Require
   an annotated tag whose peeled commit equals the independently selected
   full expected SHA; any previously observed tag/object disagreement stops,
   never force-refreshes a stale tag into apparent agreement. Materialize a
   fresh detached checkout of that commit from the fetched objects. Immediately
   before executing any candidate bytes, compare HEAD and the tracked tree to
   that commit and require no tracked modifications or untracked files.
   Refuse wrong owner/repository, changed tag, redirected endpoint or mismatch.
   These checks bind the selected channel, not authenticate its operator.
2. Run the existing install or upgrade workflow and installed-file integrity
   verification unchanged. Retain lockfile version, short commit, profile,
   per-file hashes and merge ancestry. Compare the recorded short commit with
   the full selected commit's prefix and version with the selection. The
   current `_cairn_commit` uses `rev-parse --short`; it does not store a full
   commit. For a Git-backed adopter target, the durable home for the complete
   selection is the message of the *same target-repository commit* that records
   the reviewed install or applied upgrade, including its lockfile change;
   `bootstrap/UPGRADE.md` already treats an applied upgrade as a tracked change
   through the adopter's review lifecycle. After the install/upgrade and
   integrity check, but before that commit, manually write one line in its
   message: `Cairn release: <fixed official release URL> | <tag> | <version> |
   <full commit ID>`. Compare each value with the preselected release and
   checked-out commit; after committing, read the message back with
   `git show -s --format=%B <target-commit>` and compare all four again.
   Confirm that commit records the new lockfile and installed changes, that
   its lockfile version equals the selected version, and that its short
   `cairn_commit` is a prefix of the full source commit. A missing/mismatched
   line, missing lockfile change, or absent Git history leaves the recording
   criterion unmet; do not report a completed ordinary install/upgrade under
   this route. Do not hand-edit the machine lockfile or its hashes.
3. Optional stronger policy explicitly selects the existing out-of-band
   bootstrap: two fingerprint channels, external roster, signed annotated
   tag, signed-name binding, verification before candidate execution. Retain
   the verified tag object in the operator-created verification workspace
   until trusted system Git peels that exact verified object ID to its full
   commit. Materialize the checkout from those verified objects, not a second
   fetch or mutable tag lookup. Immediately before candidate execution require
   checkout HEAD equal that peeled commit, tracked bytes equal its tree and
   no untracked files; record that same commit in the adopter's install/upgrade
   commit message as above.
   A verification-to-checkout substitution is a refusal. This is an explicit
   addition to the documented optional walkthrough, not a claim the current
   bootstrap already checks working-tree identity. A
   refusal never automatically falls back to ordinary mode. Existing stricter
   adopter policy remains binding unless its owner changes it; the upstream
   default is not an override.
4. Keep the contained recipe's source pins and containment. Document its
   ordinary route using existing `--unprovenanced` with the selected full
   commit, treating exit 3 only as an integrity pin with no signature checked;
   exits 1/2 stop. Do not make this flag a waiver ceremony or change the
   verifier's default, exit contract, or acceptance runner.

Eligibility boundary (ordinary finding 3): stable-only is the author's proposed
ordinary route for the observed named v0.6.1 release, not a new prohibition on
all existing installer inputs. A prerelease loses this no-key convenience; its
current Git checkout can still be installed under an explicitly chosen policy,
and the stronger signed route remains available if its tag is signed. An
archive-only source lacks the Git identity this route promises; current
archive-based install/upgrade behavior remains available but cannot claim this
route's full-commit/source binding. To make that claim, obtain the matching Git
checkout. Neither route authenticates arbitrary downloaded archive bytes.
These eligibility limits were in the opening proposal, not a scope reduction
made in response. The Maintainer may choose broader eligibility in the Decision;
if that adds an ordinary prerelease or archive path, its binding and assurance
must be specified and reviewed before implementation.

## Rationale

This addresses the reported pause without adding CLI flags, policy storage,
dependencies, automatic key discovery, or a new verifier. Developer-side signed
tags, review, release testing and publication checks remain required.

Protection lost, in concrete control counts rather than invented probabilities:
the ordinary path performs **zero** release-signature checks and **zero**
independent fingerprint comparisons, versus a signature check and at least two
fingerprint channels in the stronger path. A compromised forge/distribution
channel can substitute a release, commit and matching hashes without holding
the signing key; ordinary identity comparisons can all agree on that lie.
Release-name spoofing/rollback through that channel loses the stronger path's
signed-name protection. A full commit records bytes selected, not their origin.
An already compromised adopter host can falsify Git, verification and records
in either route. The stronger path also cannot defeat stolen signing keys or
compromised initial identity channels. Neither route proves content safe, nor
does tag verification alone prove the executed working tree matches it
(`bootstrap/PROVENANCE.md`, "What this is not"). Attack frequency and adopter
exposure are unmeasured; no percentage risk reduction is claimed.

## Alternatives considered

- **Do nothing:** zero build/maintenance cost and retains mandatory documented
  origin assurance, but preserves key setup and the observed upgrade pause;
  does not meet the request.
- **Documentation-only two-route workflow (proposed):** one bounded policy/docs
  pass and targeted assurance work; removes ordinary key administration but
  requires maintaining two clearly distinguished recipes and accepts the
  distribution-channel risk above. This is the least involved credible change.
- **New CLI policy switch or automated roster:** adds parsing, persistent
  policy and security tests, plus ongoing key/rotation support; does not solve
  independent trust establishment by itself. Build cost is materially higher,
  not estimated; unnecessary for a procedure-only blocker.

Recommendation: the two-route documentation change, because the CLI already
permits the requested workflow. Maintainer choices remain whether to accept
the lost origin assurance and the proposed official-release eligibility rule.

**Record-home choice (SR3):** `bootstrap/UPGRADE.md` names the machine-owned
lockfile and a tracked applied upgrade; `bootstrap/fidelity-check.md` names a
human manifest but fixes its commit citation at seven characters. Neither holds
the full tuple today. The existing target Git commit message is a durable,
human-readable work record without a new file or field, so this proposal
specifies the manual write/read procedure above. It costs one careful message
and read-back per install/upgrade; no hook or parser enforces it. A mistaken or
forged message and rewritten history can still mislead, and it does not prove
GitHub origin. A machine-readable new lockfile field or separate artifact would
improve structured discovery but add a writer/reader contract, testing and
maintenance; short-hash-only records would abandon accepted scope. Neither is
proposed. For a non-Git target there is no existing durable home with the
specified check; supporting it under this complete-record promise would need a
separate Maintainer scope choice, not a silent fallback.

## Documentation / doctrine surface

Deliberation lives here. Descriptive edits: `bootstrap/PROVENANCE.md` (primary
route, optional bootstrap, limits and lockfile language), `bootstrap/BOOTSTRAP.md`
and `bootstrap/UPGRADE.md` (entry recipes), `bootstrap/container/recipe.md`
(two routes), `README.md` (discovery), and `docs/release-process.md` (distinguish
adopter choice from unchanged publisher duties). Security-policy alignment:
`SECURITY.md` and `bootstrap/SAFETY.md` Layer 1 references, preserving Rules 7-8
and release requirements. No new cross-cutting agent rule or template is needed.
Tests may extend the existing homes below; engine, trust rosters, manifests,
lock schema, signing ceremonies and published historical records stay unchanged.

## Evidence / verification plan

### Tests required

Acceptance: a fresh Git-backed install and a prior-release plan/stage/apply
upgrade follow the ordinary instructions with no roster, signer environment or
waiver; record the URL/tag/version/full commit in the same reviewed target Git
commit as the installed change, read it back and compare it with the selected
release and checked-out commit; retain valid existing lock/hash behavior.
An agent cold-read must reach execution without requesting key approval, while
an explicit stricter policy must still stop on signature failure.

Map affected readers with `tools/test_tiers.py` in the plan. Existing owners:
`bootstrap/tests/test_verify_ref.py` (documented bootstrap, wrong roster,
substitution, inside-candidate roster, integrity-only exit 3),
`bootstrap/tests/test_manifest.py` (advisory warning),
`bootstrap/tests/test_lockfile_provenance.py` (install/apply records),
`bootstrap/tests/test_verify_integrity.py` (changed apparatus rejection), and
`bootstrap/tests/security/test_check_release_publication.py` (publication/identity).
Extend only missing workflow assertions in those homes. Fixture expectations
must fix owner/repository, tag/version, full commit and verified object before
the candidate is built, not derive expected values from its output. Test
missing/draft/prerelease releases, coherent forks, API/page/Git redirects, URL
rewrites, stale local tags, wrong selected commits, verification-to-checkout
swaps, dirty/untracked checkout and altered installed apparatus. In disposable
target repositories, exercise the manual message write/read comparison and
deliberately wrong URL, tag, version, full SHA and short-lock prefix; each
must be reported as an incomplete record. Also test missing target Git history
and a commit that omits the lockfile change. None of the negative cases may be
reported as authenticated or a successful
ordinary selection. A coherent malicious distribution is an explicit residual,
not a test expected to fail. Final Boundary B is wide for this trust-policy
surface; certification remains separate at its existing authorized triggers.

### Examples / smoke checks

Run claim, local-link/content, snippet and neutrality gates; exercise both
documented routes through real entry points in disposable copies. Preserve
developer release requirements by reviewing their before/after diff and
existing owning checks; do not perform a release ceremony for this proposal.

Authoring checks under Python 3.12.9: `scripts/claim_check.py` and
`scripts/check_cairn.py` passed on this proposal (one Markdown file; three
external links not automatically probed); `scripts/sync_doc_snippets.py --check`
passed with no directives to synchronize; `scripts/quality_gate.py --sub neutrality`
reported zero failures. `tools/test_tiers.py for` selected zero test files;
searching test/tool sources for this proposal's unique stem found no readers,
while the provenance-document search found the known-positive verifier tests.
Issue and release notes were read through GitHub. No behavioral tests,
mutations, full suite, release verification or adopter upgrade were run.

### Security preflight

- **S1 -- Supplier:** GitHub supplies release/tag identity and Git supplies
  fetched objects; these share the distribution trust boundary. Source
  `CITATION.cff` supplies declared version; the local checkout supplies commit
  and installed hashes. Only the optional roster comes from independent
  channels. Operator-fixed owner/repository/endpoints and release-note expected
  SHA are independent of the candidate, not independent of GitHub. None of
  the ordinary inputs independently authenticates origin.
- **S2 -- Failure:** replace selected commit, dirty the checkout, alter one
  hash-covered installed file, substitute an older signed tag under a new
  name, supply the wrong roster, redirect the fetch, reuse a stale tag or swap
  the checkout after verification. These are planned falsification controls,
  not runs performed during proposal authoring. Matching malicious source and
  source-derived hashes cannot establish authenticity.
- **S3 -- Trigger:** an adopter follows the chosen recipe at install/upgrade;
  trusted host HTTP tools refuse redirects and compare the fixed endpoint
  responses; trusted system Git resolves the exact selected/verified objects,
  checks HEAD/tree/cleanliness before execution; existing scaffold
  commands write records, and `bootstrap/verify_integrity.py --target` checks
  the lock-covered apparatus, not living-state files. The adopter manually
  writes the complete tuple in the reviewed target install/upgrade commit and
  reads it back; this is procedural, not machine enforcement. The current publication
  checker is evidence of existing endpoint/redirect ownership, not an adopter
  gate to run from an unchecked candidate; its current checks do not establish
  every condition above. Proposed adopter sentence:
  "The ordinary official-release path records version and commit without
  checking a release signature; choose the stronger procedure explicitly."
- **S4 -- Failure direction:** missing identity stops the ordinary recipe,
  rather than accepting unknown identity; missing/failed stronger verification
  stops that route. No automatic downgrade, in-artifact roster fallback, or
  interpretation of exit 3 as signature success is permitted.
- **S5 -- Survivor:** assume trusted host tools but a possibly compromised
  distribution channel. Its coherent substitution wins under the ordinary
  route. A compromised host wins under both; semantic malicious instructions
  missed by review/scanning remain possible under both.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

An ordinary walkthrough still asks for key approval; optional refusal silently
downgrades; an unknown commit is accepted; or any text calls review, publication
or same-source hashes proof of origin. Any reduced publisher obligation or
relaxed install pin is outside this proposal and blocks delivery.

## Scope delta

**Scope delta**: preserved -- the opening proposal already limited the new
ordinary route to stable named releases and Git checkouts. Current prerelease
and archive install capabilities are not removed, but do not gain this route's
assurance; broadening them is a Maintainer choice at Decision, not an author
concession. The complete selection record remains required, now in the
existing target Git commit message with a manual check. Non-Git targets have
no identified complete-record home and are not claimed as delivered by this
route. No implementation, Decision or waiver.

## Assurance path

**Assurance path**: high-assurance

Heavy because adopter trust policy and named provenance/security surfaces change.
Require independent usual and High-floor Security Review, reviewed plan, usual
and Security code reviews of delivered changes, and applicable verification. No External read is
called. Authoring elapsed: approximately 12 minutes; tokens: unknown.

## Review -- Codex Terra -- 2026-11-05

Reviewed commit: 8ba061aef241b06decdcc3257ad2c5a0f312b430

**Model**: Codex Terra (Medium)
**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: approximately 5 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** The procedural change addresses the reported pause, but the official-source and stronger-route bindings need specification before acceptance; the installer warning itself is advisory. -- Issue #52; `bootstrap/_scaffold/cli.py` and `install.py`.
2. **Best alternative.** Retain the current primary signature bootstrap if the Maintainer values independent key-holder assurance over removing setup; the proposed ordinary route loses it. -- `bootstrap/PROVENANCE.md`, Controls and out-of-band bootstrap.
3. **What would show it wrong?** A cold ordinary walkthrough that stops for a key, or accepts a different repository or mismatched release/commit, would falsify the intended result. -- Issue #52; Proposal 1 and Tests required.

1. **Blocking: official identity is asserted, not bound.** Proposal 1 compares HEAD to the fetched tag, so a fork or redirected repository can supply both matching values. It does not specify how the release page, owner/repository, release tag and fetch destination are independently selected and checked, including redirects or a stale local tag. `scripts/check_release_publication.py` separately fixes the GitHub API and Git endpoints and refuses API redirects; its tests include redirect refusal, but its expected commit is supplied independently and it does not enforce this proposal's non-prerelease rule. Specify the ordinary identity checks and fail-closed redirect/repository handling before candidate code runs; test wrong owner, repository, redirect, fork, missing/draft/prerelease and changed tag against independently fixed expected values.

2. **Blocking: the stronger path is not bound to execution.** The existing external bootstrap verifies a fetched tag object in a disposable bare repository and discards it; `PROVENANCE.md` explicitly says it does not verify the working tree. Proposal 3 retains verification before execution but does not require the verified object's peeled commit to equal the clean checkout actually executed. Require that binding without executing candidate code first, and exercise substitution between verification and checkout as a negative control; preserve refusal without fallback.

3. **Non-blocking: make eligibility and evidence explicit.** Proposal 1 excludes prereleases and archives, while issue #52 requests a named official release without specifying those exclusions. Identify the practical loss for adopters selecting prereleases or archive-only sources and the route available to them. Require independent expected release/version/commit fixtures and negative controls for both routes, including altered installed apparatus; same-source tag/HEAD agreement alone is not an independent oracle. Preserve publisher signing and gate duties in `docs/release-process.md` and existing lock/hash checks.

**Coverage:** Read the committed proposal, template, issue body, provenance and release process, relevant installer and verifier code and test references. No behavioral checks, full suite, release ceremony or Security Review were run; implementation details and actual GitHub redirects were not tested. Above target to distinguish the two trust bindings and their separate controls.

## Review -- Codex Sol (Security Review) -- 2026-11-05

Reviewed commit: 8ba061aef241b06decdcc3257ad2c5a0f312b430

**Model**: gpt-6.1-sol (High)
**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** It can meet the Maintainer's request if the distribution-channel risk is explicitly accepted and both routes bind the exact executed bytes; neither binding is complete yet -- issue #52; ordinary findings 1-2.
2. **Best alternative.** Keep the existing primary signed-bootstrap procedure: it preserves independent key-holder assurance but retains the observed adopter pause -- `bootstrap/PROVENANCE.md` > Verifying a release.
3. **What would show it wrong?** A forked release whose tag and checkout agree, a verified tag followed by another checkout, or an install record that cannot identify the selected full commit would falsify the promised controls -- proposal steps 1-3; findings below.

**SR1 (blocking; ordinary finding 1):** Same-source tag/HEAD agreement cannot establish the official repository. The ordinary path needs fixed owner/repository, release and fetch endpoints, redirect/ref substitution refusals, and an independently selected expected release identity before candidate execution. The current `scripts/check_release_publication.py` is a useful owner but does not itself define this adopter walkthrough. Test a coherent fork and stale local tag, not only mismatched HEAD.

**SR2 (blocking; ordinary finding 2):** The optional signed path verifies a tag object in a bare repository, not the later executing checkout. Bind its peeled commit to that clean checkout before execution; a verification-to-checkout swap must fail without silently downgrading to ordinary mode -- `bootstrap/PROVENANCE.md` > What this is not.

**SR3 (blocking; new record gap):** The proposal promises an existing install/upgrade record containing release URL, tag/version and full commit, but names no such durable field or file. Fresh install writes `cairn_commit` from `git rev-parse --short HEAD` (`bootstrap/_scaffold/lockfile.py::_cairn_commit`); `bootstrap/fidelity-check.md` describes a seven-character human-manifest citation. Name the exact existing record home and manual write/check, or change the claim and seek the Maintainer's scope disposition. Do not present a short prefix or source-declared repository as full-commit provenance.

**Coverage:** Committed proposal, ordinary review, current provenance/verifier, lock writer and documented fidelity record. **Not covered:** live GitHub redirect behavior, signed-tag ceremony, an adopter walkthrough, implementation, or full suite. The ordinary route's coherent distribution substitution remains an explicit risk for the Maintainer's Decision, not a reviewer waiver. This pass is above target to separate the two executable bindings from the record gap.

## Response -- Codex Sol -- 2026-11-05

**Model**: Codex Sol (High), original proposal author
**Elapsed**: unknown
**Tokens**: unknown

Read ordinary review `76ebde16` and Security Review `26d6e635` together.

- **Ordinary 1 / SR1 -- accepted:** Proposal 1 now fixes official owner,
  repository, page/API/fetch endpoints and expected release/commit before
  candidate execution; refuses redirects, forks, URL rewrites and stale tags;
  and requires exact checkout identity/cleanliness. This is a documented
  selection contract, not independent origin authentication or an implemented
  control. Tests require independently fixed expectations and coherent-fork
  and stale-tag controls.
- **Ordinary 2 / SR2 -- accepted:** Proposal 3 retains the verified object,
  peels that object to the full commit, materializes from those same objects,
  and checks the exact clean executing checkout. A swap must refuse without
  fallback. Current tag verification alone is no longer presented as enough.
- **Ordinary 3 -- accepted:** Named prerelease/archive eligibility losses,
  available Git/signed routes and the Maintainer's required loss disposition;
  independent fixtures and altered-apparatus controls are explicit. Publisher
  signing/testing and current lock integrity remain unchanged.
- **SR3 -- unresolved, blocking scope choice:** no complete currently
  prescribed record home was found in lockfile/fidelity documentation. The
  alternatives compare manual use of existing commit-message history, a new
  field/artifact, and explicitly losing full-record scope. Recommend the
  manually written/read-back commit message; do not authorize it here or
  create anything. Stop at this boundary pending the Maintainer's choice.

Verification under Python 3.12.9: proposal-only claim, local-link/content,
snippet and whitespace gates passed; neutrality reported zero failures.
Tier mapping selected zero tests; stem search found no readers, with
`PROVENANCE_MD` in the verifier tests as a positive search control. Three
external links were not probed. No behavioral tests, mutations, live endpoint tests, full suite,
implementation, trust edits or push. Record-home and eligibility choices plus
distribution-compromise risk remain for the Maintainer; no finding is waived.

### Withdrawn / superseded commitments

- Withdraw the unsupported assertion that an existing install/upgrade record
  already holds the complete tuple; retain the requirement pending SR3 choice.
- Supersede same-source tag/HEAD agreement with fixed-channel selection and
  exact verified-object-to-execution binding (ordinary 1-2, SR1-2).
- Supersede implicit eligibility exclusions with explicit losses requiring
  Maintainer disposition (ordinary 3); no new route is silently promised.

## Response -- Codex Sol -- 2026-11-05 (record-home clarification)

**Model**: Codex Sol (High), original proposal author
**Elapsed**: unknown
**Tokens**: unknown

**SR3 -- closed in the proposed scope:** `bootstrap/UPGRADE.md` makes an
applied upgrade a tracked target change, while its lockfile and the human
fidelity manifest retain short commit citations. The operative proposal now
uses the message of that same target install/upgrade commit for the full
URL/tag/version/SHA tuple, with manual pre-commit comparison and post-commit
`git show` read-back. Missing history, message or lockfile change is an unmet
criterion. This is an honestly manual record, not origin proof or automatic
enforcement; non-Git targets have no identified equivalent home.

**Ordinary 3 -- clarified:** stable-only and Git-checkout eligibility were
opening author choices for the new ordinary route. Existing prerelease and
archive inputs are not disabled; they simply do not acquire the new route's
assurance. Broader ordinary eligibility would require the Maintainer to
choose it and specify its checks; this response does not widen scope.
Distribution-channel compromise remains for the Maintainer's risk decision.
No additional review requested at the current cap.

### Withdrawn / superseded commitments

- Supersede the prior response's unresolved SR3 record-home choice with the
  precise manual target-commit record; retain the full-tuple requirement.
- Supersede its assertion that prerelease/archive exclusions require a loss
  concession: no existing installer input is removed by the new route.

## Decision -- gpt-6.1-sol (High), delegated decision-maker -- 2026-11-06

**Model**: gpt-6.1-sol (High).
**Authority**: temporary Maintainer delegation -- chat, 2026-11-06, relayed by the coordinating agent. This is the Sol agent's decision under that explicit exception, not a claim that the Maintainer selected this option personally.

> "I specifically authorize you to use a Sol agent to make decisions in my stead until I return (excepting anything that cannot be undone easily). Keep track of these decisions for review. Let the other agent know to ask you if they need it, and you will spawn the Sol review and track its outcome."

**Tier**: heavy.
**Elapsed**: unknown. **Tokens**: unknown.
**Source**: operative proposal, appended usual and Security Reviews, and author responses as committed at `831d0e3b`; the proposal bytes remained unchanged through `8380bc9b`.

**ACCEPTED.** Choose the documented two-route adopter workflow for reversible local v0.7 preparation, including the manual full-selection record in the target install/upgrade commit message.

**Reason and risk choice.** The reported pause is procedural, so a new CLI
policy mechanism is unnecessary. I accept the proposed ordinary route's explicit
loss of independent key-holder assurance: zero signature checks and zero
independent fingerprint comparisons. A compromised official distribution can
supply coherent false release metadata, source and hashes. Local preparation of
this policy is reversible; this Decision does not authorize using the route on
real adopter work or publishing the changed policy while the Maintainer is away.

**Options and costs.** Retaining the primary signed bootstrap adds no build
cost and keeps that assurance, but retains key setup and the observed pause.
The proposed documentation change is the least involved credible way to remove
the pause: maintain two recipes and their targeted controls. It removes ordinary
fingerprint/roster administration but adds one careful tuple entry and one
read-back per Git-backed install/upgrade in the same reviewed target commit.
The stronger route retains its fingerprint channels/roster and now binds the
verified object to the clean executing checkout. A new CLI switch, lockfile field
or record artifact adds persistent contracts and maintenance without a required
capability. No numerical time or risk reduction is established.

**Record and eligibility choice.** Explicitly select SR3's manual target-commit
message home, with all four values, lockfile/version/prefix comparisons and
read-back. Missing history or record remains unmet. Preserve stable named
releases and Git checkouts for the new ordinary route; existing prerelease and
archive inputs retain their existing capabilities but acquire no new assurance.
No broader route is authorized. Keep fixed endpoints, redirect/stale-tag refusal,
clean exact-commit binding, stronger refusal without fallback, unchanged
publisher signing/testing duties and verifier exit meanings. No safeguard or
full-commit record is conceded.
The operative publication-test citation is updated to its existing security
subdirectory after consolidation; no test obligation or historical review is changed.

Accept the complete operative scope and its stated limitations; no outcome or
required check is waived. High-assurance treatment, both required plan reviews,
ordinary and separate Security code reviews, mapped checks and final wide
Boundary B remain due. Proposal controls described as unrun remain unrun.
This authorizes reversible local planning and implementation, not an actual
release, push, publication, signing, trust-ref movement, credentials/private-log
access or other hard-to-undo action. Those operations remain with the Maintainer.
