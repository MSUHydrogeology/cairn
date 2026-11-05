# Make adopter release verification an explicit choice

**Author**: Codex Sol (High)
**Status**: revising
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

1. Ordinary acquisition selects a published, non-draft, non-prerelease GitHub
   Release in `MSUHydrogeology/cairn`, with an explicit tag, never an implicit
   latest branch or a fork. Read its release notes, fetch that exact tag from
   the official repository, resolve its full commit, and use a clean detached
   checkout of that commit. Compare checkout HEAD with the selected tag's
   peeled commit before executing Cairn code. Stop for absent releases,
   identity mismatch, dirty source, or unresolved identity; these are not
   signing-key prompts. Record release URL, tag/version and full commit in the
   project's existing install/upgrade record, not a new ledger.
2. Run the existing install or upgrade workflow and installed-file integrity
   verification unchanged. Retain lockfile version, short commit, profile,
   per-file hashes and merge ancestry. Compare the recorded short commit with
   the full selected commit's prefix and version with the selection. The
   current `_cairn_commit` uses `rev-parse --short`; do not silently claim it
   already stores a full commit. Archive-only sources without Git identity
   are outside this ordinary recipe, not grounds to invent a commit value.
3. Optional stronger policy explicitly selects the existing out-of-band
   bootstrap: two fingerprint channels, external roster, signed annotated
   tag, signed-name binding, verification before candidate execution. A
   refusal never automatically falls back to ordinary mode. Existing stricter
   adopter policy remains binding unless its owner changes it; the upstream
   default is not an override.
4. Keep the contained recipe's source pins and containment. Document its
   ordinary route using existing `--unprovenanced` with the selected full
   commit, treating exit 3 only as an integrity pin with no signature checked;
   exits 1/2 stop. Do not make this flag a waiver ceremony or change the
   verifier's default, exit contract, or acceptance runner.

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

Acceptance: a fresh install and a prior-release plan/stage/apply upgrade follow
the ordinary instructions with no roster, signer environment or waiver; record
the selected version/full commit and retain valid existing lock/hash behavior.
An agent cold-read must reach execution without requesting key approval, while
an explicit stricter policy must still stop on signature failure.

Map affected readers with `tools/test_tiers.py` in the plan. Existing owners:
`bootstrap/tests/test_verify_ref.py` (documented bootstrap, wrong roster,
substitution, inside-candidate roster, integrity-only exit 3),
`bootstrap/tests/test_manifest.py` (advisory warning),
`bootstrap/tests/test_lockfile_provenance.py` (install/apply records),
`bootstrap/tests/test_verify_integrity.py` (changed apparatus rejection), and
`bootstrap/tests/test_check_release_publication.py` (publication/identity).
Extend only missing workflow assertions in those homes. Test negative cases:
missing release, fork URL, wrong selected commit, dirty checkout, changed
installed apparatus; none may be reported as authenticated or a successful
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
  channels. None of the ordinary inputs independently authenticates origin.
- **S2 -- Failure:** replace selected commit, dirty the checkout, alter one
  hash-covered installed file, substitute an older signed tag under a new
  name, or supply the wrong roster. These are planned falsification controls,
  not runs performed during proposal authoring. Matching malicious source and
  source-derived hashes cannot establish authenticity.
- **S3 -- Trigger:** an adopter follows the chosen recipe at install/upgrade;
  trusted system Git resolves the exact selected ref/HEAD, existing scaffold
  commands write records, and `bootstrap/verify_integrity.py --target` checks
  the lock-covered apparatus, not living-state files. Proposed adopter sentence:
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

Preserved: opening scope only; no implementation, Decision or current waiver.

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
