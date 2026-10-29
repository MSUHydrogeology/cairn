# Establish a forward trust baseline

**Author**: Codex (plan coordinator)
**Status**: revising
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

## Author revision -- Codex (plan coordinator) -- 2026-10-29

The Maintainer clarified the sequencing after this proposal opened:

> They can each build the machinery, the new baseline does not need to be part of their plans. It can be a work board item for v0.6.

This replaces the opening's instruction that installation precede affected-plan archival. The current proposed contract follows; it remains subject to review and a Maintainer Decision.

### Current contract

Amend the affected plans so they can finish their reviewed machinery, verification and independent reviews and archive without installing the new baseline. Record the baseline installation separately as a v0.6 work-board item, before release readiness. Installation remains Maintainer-only and separately authorized for the exact candidate, package and signer; no ref move or push is authorized here. Existing protections continue until a reviewed replacement is installed.

Replace initial historical comparison against the old anchor with a separately reviewed no-signed-predecessor baseline mechanism. Reuse existing preparation and re-anchor commands where suitable. Proposed preparation extracts a clean committed candidate from Git objects, checks containment and membership, collects without signing credentials, binds the approved roster and independently derives static manifest fields. A package binds candidate, manifest, collection, interpreter and tool hashes and an independent reader record. Proposed installation rechecks the package and candidate, runs no candidate tests, signs once, checks the signed commit's parent and manifest-only change, and atomically updates branch and anchor against observed values. Record the old anchor ID without assessing intervening changes against it. This mechanism is a proposal, not an approved design.

Retain exact approved roster membership, protected scripts, modules and fixtures, authority closure, independent derivation, protected-byte and node-loss and new-marker HOLDs, ordinary notes, unrostered-test notice, full collection and actual release skip/xfail/xpass refusal. After installation, the signed baseline supplies trusted code and roster membership for later comparisons. New protected tests require reviewed admission. Signing identifies approved bytes; it does not prove them harmless. Candidate collection can influence execution; a compromised host or overlooked malicious behavior remains a risk.

The grouped scope loss requiring Maintainer allowance includes initial P443-to-release protected-drift verification, old-P/E7 comparison, initial compatibility transitions and each affected plan's requirement to complete its installation or frozen-file ceremony before archive. The 83 prior HOLD reports remain unresolved historical evidence, not cleared findings. No roster reclassification or pilot extraction is included. Identify and amend each affected plan's actual fence rather than adding the new ceremony to every plan. Preserve its other accepted outcomes and independent reviews.

Review the current controls and proposed mechanism through ordinary and Security passes. Map affected consumers and tests, exercise the public preparation and installation paths in scratch repositories and challenge roster substitution, stale packages, signer mismatch, protected loss, ordinary notes and future signed-prior checks. Record mutation controls and omissions; run applicable documentation gates and the required canonical certification before actual re-anchor. The work-board item must retain that installation and certification dependency without holding machinery-plan archival.

### Withdrawn / superseded commitments

The opening's requirement that installation precede affected-plan archival is withdrawn to follow the Maintainer's clarification. Installation remains a separate v0.6 work-board item, with release readiness dependent on its completion.


## Review -- Codex (gpt-6.1-sol), proposal reviewer -- 2026-10-29

```
Reviewed commit: 5ac029eb499f6e481d1a84e16c0d1bc5f4745357
Target: opening proposal and Author revision / Current contract
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes: finish and review machinery independently, then install one explicitly approved baseline before v0.6 readiness. The revised contract names the historical assurance being surrendered instead of treating signing as proof. -- Author revision / Current contract; `dev/plans/2026-10-28-test-trust-boundary.md`, C3–C5.
2. **Best alternative.** Extend existing extraction, package, static derivation and signing paths with an explicit bootstrap mode. A manual one-off loses reusable refusal checks; keeping historical bridges defeats the stated direction. -- `scripts/repin.py`, `extract`, `build_packet`, `run_ceremony`; `bootstrap/tests/_gate_preflight.py`, `rederive_static_manifest`.
3. **What would show it wrong.** A baseline that admits another roster, signs stale bytes, or cannot subsequently detect protected loss defeats the forward guarantee; a board dependency that still prevents machinery archival defeats the sequencing. -- Current contract; `bootstrap/tests/_gate_reanchor.py`, `gather_evidence`, `promote_data_only`; trust plan C2–C5.

The strongest version is a deliberate restart of trust, with useful automation retained and the Maintainer approving the exact starting bytes. Existing commands cannot simply be relabeled: they authenticate prior authority and the ordinary driver refuses changed authority. The proposed reviewed mode acknowledges that design work rather than presenting it as already available.

**F1 — Non-blocking: make candidate preparation explicit in the plan.** A manifest-only installation commit is feasible only after other required baseline material is present in the candidate. The current driver separately prepares reviewed AST/lockfile changes and refuses an owed transaction before stage 1. Reusing that preparation avoids discovering an extra authority write during signing. **Satisfier:** the derived plan identifies whether AST/lockfile preparation is required, who reviews and commits it, and tests refusal if the candidate lacks required material. Keep those writes before the final candidate/package review; do not revive historical comparison. -- `scripts/repin.py`, `build_transaction`, `apply_reviewed_pin`, `run_ceremony`; proposal installation parent/manifest-only invariant.

The smallest route preserves reusable preparation and installation checks, amends each source plan's actual fence, and assigns installation to one v0.6 board item. It loses historical protected-drift checks and installation-before-archive guarantees as declared; only the Maintainer can allow those losses. Machinery archival must not claim the narrower boundary is active. The baseline item must retain certification, installation evidence and forward-behavior checks before release readiness.

**Covered:** claims, completeness and refusal (1,3,4: the named driver and promotion functions); production-path design (2: proposed scratch public-entry probes); reuse, consistency and drift (5,6: driver functions, runbook preparation/verifier instructions, trust plan C3–C5, ceremony-commands plan C1–C4); lifecycle and scope (7,8: Current contract, scoped-change-verification plan's pending frozen-file ceremony); satisfier (9: F1). Source was read at the reviewed commit. **Not covered / low confidence:** no tests, mutations, signing, host containment assessment or ref changes; feasibility is design inspection, not implementation evidence. This pass does not discharge Security Review.

## Security Review -- Codex (gpt-6.1-sol) -- 2026-10-29

```
Reviewed commit: 5ac029eb499f6e481d1a84e16c0d1bc5f4745357
Target: opening proposal and Author revision / Current contract
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes, subject to the Maintainer's explicit scope allowance: a deliberate new trust root can protect future comparisons without claiming historical clearance. Separate machinery archival is coherent only while release readiness retains actual installation. -- Current contract; `bootstrap/tests/_gate_reanchor.py`, `gather_evidence` and `promote_data_only`.
2. **Best alternative.** Extend existing extraction, package, independent-reader and signing machinery with a narrowly selected bootstrap mode; do not turn ordinary prior-authentication refusals into optional checks. Doing nothing preserves the unwanted historical dependency. -- `scripts/repin.py`, `build_packet`, `_verifier_prepare`, `run_ceremony`.
3. **What would show it wrong?** A candidate-selected authority roster, substituted executing installer, incorrect signer, or partial/stale ref update would defeat the starting authority; protected loss passing after installation would defeat forward protection. These are required future refusal probes, not measured successes. -- Current contract; `scripts/repin.py`, `verify_checkpoint`, `check_record`; `bootstrap/tests/_gate_reanchor.py`, `_verify_executing_authority_code`.

The reviewed proposal recognizes the central security limit: deriving hashes from candidate bytes establishes consistency, not permission to trust those bytes. The independent approval and reader must supply that permission. Existing prior-code authentication cannot simply be bypassed globally. Retaining it for subsequent ceremonies is part of the useful protection this design buys.

**S1 — Non-blocking plan requirement: pin the bootstrap authority before execution.** The plan must identify exactly which reviewed launcher, installer and imported closure execute during installation, bind those bytes to the reader record and approval, and refuse substitution before signing or ref updates. Give the signer fingerprint an independently supplied expectation; candidate `allowed_signers` membership alone is insufficient. Test changed executing code, wrong fingerprint, stale reader/package, and either ref changing before the atomic transaction, including proof that neither ref moves on refusal. The proposal's tool-hash and exact-signer promises support this; the plan must make their trigger concrete. -- `scripts/repin.py`, `load_encoder`, `build_packet`, `check_record`, `run_ceremony`; `bootstrap/tests/_gate_reanchor.py`, `_verify_executing_authority_code`, `_cas_advance_ref`.

**S2 — Non-blocking release dependency: preserve the actual release command.** Record baseline installation and canonical pre-reanchor certification separately from the release security run. The certification pair alone does not invoke the release-mode outcome refusal, Bandit or release state checks. **Satisfier:** the work-board dependency and operator instructions retain `python bootstrap/security_check.py` at the eventual clean release commit, with its required tools and no skip/xfail/xpass outcomes; no run is authorized by this review. -- `bootstrap/security_check.py`, module contract, `_release_child_env`, `run_suite`, `main`.

**Covered:** claims and authority/failure paths (lenses 1,3,4: named functions); public-path verification requirements (2: Current contract); reuse, consistency and drift (5,6: existing packet/prior-verifier/ceremony paths and release command); lifecycle and scope (7,8: revised archival boundary and grouped historical loss); concrete satisfiers (9: S1–S2). These source files are unchanged from the reviewed commit. **Not covered / low confidence:** no executable probes, mutations, signing or ref moves; no host isolation proof. Credential scrubbing is not containment of hostile collection. This clears the proposal Security Review obligation only, not future plan/code review or installation authorization.
