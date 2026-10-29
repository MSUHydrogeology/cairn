# Establish a forward trust baseline

**Author**: Codex (plan coordinator)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Establish a reviewed trust baseline during v0.6 without comparing intervening changes to the old anchor.

## Context

The Maintainer accepted the protected-test boundary in `dev/plans/2026-10-28-test-trust-boundary.md` and approved its exact roster. That plan requires an old-anchor transition and stops if its checks cannot be preserved. `dev/strategy/2026-10-29-sol-forward-baseline.md` records the Maintainer's later direction to give up comparison with the old anchor and re-anchor at v0.6. The Maintainer clarified that plans finish before v0.6 is ready: installation is part of that work and precedes affected-plan archival and release readiness. No baseline has been installed.

## Proposal

Replace the initial old-anchor transition with one explicit no-signed-predecessor baseline, prepared from a clean committed candidate and installed by the Maintainer. Reuse the existing ceremony preparation, verification and re-anchor commands where they can meet these requirements; add only the necessary reviewed mode. Do not fabricate a predecessor or silently fall back to the old first-run path.

Preparation extracts the exact candidate from Git objects, checks containment and membership, collects tests without signing credentials, builds a manifest bound to the approved roster, and independently derives its static fields. A reviewable package binds candidate, manifest, collection, interpreter and tool hashes, and independent reader record. Independent ordinary and Security reviews examine the current control surface and the package design. The Maintainer compares the recorded hashes and signer identity and authorizes the exact candidate, package and signer before installation.

The installation command rechecks the package and candidate, runs no candidate tests, signs once, verifies that the new signed commit has the candidate as parent and only the reviewed manifest change, and atomically updates the branch and gate anchor against observed old values. Record the old anchor ID without using it to assess intervening changes. The Maintainer performs this during v0.6 work; the affected plans remain open until their applicable installation, verification and reviews complete. Pushing remains separately authorized.

After installation, the signed baseline supplies trusted code and roster membership for subsequent comparisons. Preserve the exact approved roster, protected scripts, modules and fixtures, authority closure, independent derivation, protected-byte and node-loss and new-marker HOLDs, ordinary-change notes, unrostered-test notice, full collection, and actual release skip/xfail/xpass refusal. New protected tests require reviewed admission. Existing controls remain in force until reviewed changes replace them.

## Rationale

This retains forward protection while avoiding historical comparison the Maintainer has chosen to relinquish. Signing identifies approved bytes; independent review supplies the initial judgment, not proof that the baseline is harmless.

## Alternatives considered

The existing two-transition bridge preserves historical checks but conflicts with the direction. Doing nothing leaves the old checks and the affected plans' installation fences in place. A manual one-off baseline would avoid a new mode but gives up reusable, testable preparation and installation controls.

## Documentation / doctrine surface

Amend the trust, ceremony and scoped-verification plans through their lifecycle without rewriting review history. Route changed cross-cutting prescriptions to `AGENTS.md`, deliberation to `dev/`, and actual operator instructions to `bootstrap/REANCHOR_RUNBOOK.md`, following `docs/DOCUMENTATION_PLAN.md`.

## Evidence / verification plan

### Tests required

Map changed callers and owning nodes in `bootstrap/tests/test_gate_manifest.py`, `bootstrap/tests/test_gate_preflight.py`, `bootstrap/tests/test_gate_reanchor.py`, `bootstrap/tests/test_reanchor.py`, `bootstrap/tests/test_repin.py`, and `bootstrap/tests/test_repin_ceremony.py`. Exercise real preparation and installation entry points in scratch repositories: roster substitution, stale package, wrong signer, missing inputs, protected edits and node/marker loss, ordinary changes, and post-install signed-prior checks. Include release outcome checks in `bootstrap/tests/test_security_check.py` and `bootstrap/tests/test_security_marker.py`. The reviewed plan must identify exact nodes and any additional consumers.

### Examples / smoke checks

Run applicable claim, link, snippet, neutrality and prose-integrity gates. Before the Maintainer's re-anchor, run the prescribed canonical certification on the clean committed candidate. Record results and omissions; certification cannot replace a missing required check.

#### Security preflight — five questions, answered in writing

**S1.** The committed candidate supplies source and collection; the approved roster and independent reader record supply separate authority; the Maintainer supplies signer and installation approval. Candidate code can influence collection and must not supply its own expected roster.

**S2.** A substituted roster, stale package or protected loss must cause refusal. These mutations have not yet been run against the proposed mode; implementation must record failures and controls. Static derivation from the same candidate alone cannot authenticate that candidate.

**S3.** The maintained preparation and installation commands proposed above select the candidate and package; their exact command forms and adopter-facing instructions do not yet exist and must be reviewed together with their actual triggers.

**S4.** Missing, malformed, mismatched or stale authority must refuse, with no fallback granting authority. The implementation must test each fallback and error path.

**S5.** The design assumes a malicious or mistaken candidate and potentially hostile collection. A compromised host or malicious behavior overlooked by review can still affect the baseline; collection is not contained by this proposal.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Withdraw or repair if real installation permits roster substitution, a protected change or loss passes against the new baseline, the package cannot bind the reviewed candidate and signer, or the Maintainer cannot operate the reviewed commands.

## Scope delta

**Scope delta**: lost — initial P443-to-release protected-drift verification, old-P/E7 comparison and the initial compatibility transitions are relinquished together. The reported old HOLDs remain unresolved historical evidence; they are not certified or individually cleared. This proposal requests the Maintainer's explicit allowance for that grouped loss and the replacement mechanism; it does not claim that allowance has already been given. Future signed-prior comparisons remain required. No roster reclassification or ordinary-test pilot extraction is included.

## Assurance path

**Assurance path**: high-assurance
