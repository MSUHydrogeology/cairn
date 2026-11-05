# Make adopter release verification an explicit choice

**Author**: Codex Sol (High)
**Status**: awaiting-review
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
