# Re-anchor and repin as human-run commands

**Author**: Codex (gpt-6.1-terra)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Give the Maintainer reusable commands to check and carry out re-anchor and repin ceremonies while keeping signing and approval under human control.

## Context

The Maintainer can run commands, compare hashes and enter a passphrase, but cannot assemble git commands. The v0.6 item in `dev/PLANNING.md` records that request and the manual steps and unrecorded Y1–Y5 answers observed in the first ceremony. The scripts in `dev/measurement/ceremony-scripts-2026-10-28/` were candidate-specific.

The v0.5 `scripts/repin.py` already has status, package, packet and ceremony commands. Its ordinary ceremony checks a packet, runs both stages, prompts for approval, verifies the signed anchor and stops before push; an owed AST pin requires a commit and rerun. Its status deliberately skips full test collection. Its boot and packet paths refuse changed authority closure; `scripts/reanchor_ceremony.py` is a read-only preflight, and `bootstrap/reanchor.sh` supplies staged operations. See `dev/plans/archive/repin-build.md` and `bootstrap/REANCHOR_RUNBOOK.md`. No ceremony was run.

The accepted `dev/plans/2026-10-28-test-trust-boundary.md` requires a reusable human-run full verifier. Its narrowing is not installed until the authorized ceremony. Candidate test code can still influence collection or execution; the accepted boundary does not claim otherwise.

## Proposal

Build on the shipped tools to deliver tested reusable `reanchor` and `repin` commands. The Maintainer invokes them, confirms displayed hashes and explicit bounded dispositions, enters the passphrase, and separately runs the push. The commands prepare and present checks, execute stage 1, show raw and expected values and compare hashes for E1–E6, H and K, execute stage 2, verify the signature and record approval. Preserve the independent launcher-byte check E5: a launcher cannot establish its own integrity. Capture Y1–Y5 answers. Support reviewed AST deletions, the reader record before an AST write, stop records, and a fresh package name on repeat runs.

Deliver the trust plan's reusable human-run verifier as part of this work, not a second item. Before signing, with the key away, authenticate immutable signed prior anchor P and its checker and manifest; inspect clean committed candidate C via raw object bytes and hashes; require the anchor and full collection. Present exact and grouped protected HOLDs and ordinary notes, and require an explicit human disposition bounded to the displayed evidence. Fail closed on missing or inconsistent inputs, collection errors, or unapproved HOLDs. Explain that candidate code can influence execution even when bytes are checked. An independent reader checks verifier provenance; the Maintainer compares hashes and runs it.

Design a reviewed transition path for changed authority that preserves prior-P checks and stage comparisons. Do not weaken the existing `repin` refusal or treat candidate code as its own authority. If a safe transition cannot be demonstrated, stop rather than sign. The trust plan remains open until its own reviewed verification and Maintainer ceremony complete.

## Rationale

A maintained entry path reduces manual assembly while retaining checks and human decisions. Reusing the existing staged machinery preserves the tested ordinary path and makes the transition distinction visible. This costs implementation and Security Review effort and may require a bootstrap step.

## Alternatives considered

Keep the manual runbook: it preserves existing safeguards but leaves the Maintainer assembling commands and does not deliver the reusable verifier. Use the recorded scripts unchanged: they hard-code two candidates and do not cover later changes. Extending only ordinary `repin` leaves the transition and full-collection obligation unmet.

## Documentation / doctrine surface

Route operator instructions to `bootstrap/REANCHOR_RUNBOOK.md`; governing changes, if needed, to `AGENTS.md`; deliberation to `dev/`. Update the trust plan through its lifecycle if its implementation contract needs revision. No doctrine change is assumed.

## Evidence / verification plan

### Tests required

Map current and new behavioral nodes in `bootstrap/tests/test_repin.py`, `bootstrap/tests/test_repin_ceremony.py`, `bootstrap/tests/test_reanchor.py`, `bootstrap/tests/test_reanchor_driver_disclosures.py`, and the manifest, transition and preflight test families. Exercise public entry points with throwaway keys and scratch repositories: ordinary and changed-authority transitions; prior signature and immutable checker/manifest provenance; raw C bytes; full collection and anchor refusal; protected losses, ordinary notes, bounded human decisions, exact comparisons, tampering, interruption and repeat runs. Demonstrate one signing prompt and signature verification; no real key, ref or push. The plan must trace and name exact nodes and callers.

### Examples / smoke checks

Run `python scripts/check_cairn.py`, claim, link, snippet and neutrality gates on affected prose. Demonstrate a complete scratch ceremony and verify that the documented human command triggers the full verifier. Full-tree certification remains a separate authorized ceremony.

#### Security preflight — five questions

**S1.** P and its signature arrive from the trusted anchor and signer configuration; C, tests, manifests and proposed authority arrive from committed candidate objects. C can supply executable test code and references; it cannot select its own trusted checker or roster.

**S2.** Mutate P's signature, checker bytes, C hashes, protected membership, a comparison and a recorded disposition; each must refuse with a passing control. These are proposed mutations, not runs performed for this proposal.

**S3.** The proposed human-invoked command will select the authenticated P checker and full committed C collection, report protected HOLDs and ordinary notes, and require bounded disposition. Implementation must write and test the command and its description together.

**S4.** Missing anchors, parse failures, mismatches, incomplete collection and interrupted approvals refuse; none grants authority by fallback. A transition must not bypass the prior checker.

**S5.** Assume a candidate author can change committed ordinary code and tests but not the trusted prior signing key. Such code can influence test collection or execution; checking membership and bytes does not close that attack. Same-user compromise of the operator environment remains outside this assurance.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A candidate-controlled checker can approve itself; an unapproved protected loss signs; a changed authority bypasses prior-P checks; the human cannot reproduce the displayed values; or the actual command omits full collection. Any would block delivery.

## Scope delta

**Scope delta**: preserved. The queued two-command outcomes and the accepted trust-plan verifier remain in scope.

## Assurance path

**Assurance path**: high-assurance
