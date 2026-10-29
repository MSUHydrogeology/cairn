# Re-anchor and repin as human-run commands

**Author**: Codex (gpt-6.1-terra)
**Status**: revising
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


## Review -- Codex (gpt-6.1-sol, high) -- 2026-10-29

```
Reviewed commit: 9c331e14ac232d3f7012b5bb8b9b1d068b26321b
Target: opening proposal
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes: reusable human-run commands address the recorded operator burden, and integrating the prior verifier delivers an already accepted outcome. Retain the existing ordinary path rather than replacing it. -- `dev/PLANNING.md:126`; `dev/plans/2026-10-28-test-trust-boundary.md:514`; `scripts/repin.py:1063`.
2. **Best alternative.** Extend the v0.5 driver and staged artifact with a separately reviewed transition path; keeping only the manual page leaves the recorded need unmet. The proposal chooses this stronger alternative, but needs an operator-level completion criterion. -- `dev/plans/archive/repin-build.md:13`; `bootstrap/REANCHOR_RUNBOOK.md:74`; Proposal.
3. **What would show it wrong.** If the documented commands still require improvised commands to prepare or resume the supported workflow, or invoke candidate authority in place of authenticated P, this framing fails its purpose. -- `scripts/repin.py:759`; `scripts/repin.py:1162`; Signals the change is wrong.

The strongest part is its separation of prior authority, candidate evidence and
human approval. It recognizes that collection executes candidate code, preserves
E5, keeps push separate and refuses an undemonstrated transition.

**F1 — Blocking: prove the operator workflow, including stops.** The smoke check
requires a complete scratch ceremony, but does not require following the actual
operator instructions from preparation through an owed AST write, commit, stop
and rerun. The current driver prints a Git commit command and stops; packet,
reader record and values preparation are also prerequisites. A happy-path test
can therefore pass while the Maintainer still needs a fresh sequence assembled
for each run. **Satisfier:** carry an explicit outcome into the plan: reusable
scripts prepare the required details; document who prepares and checks each
input; demonstrate both ordinary and changed-authority workflows, including
reviewed deletion and interruption/resume, through those documented entry points.
The Maintainer's actions must fit the recorded run/compare/approve/passphrase
brief. Preserve human approval and the existing no-automatic-AST-commit contract
unless its change is expressly decided. This removes no accepted outcome. --
`dev/PLANNING.md:126`; `dev/plans/2026-10-28-test-trust-boundary.md:514`;
`dev/plans/archive/repin-build.md:13`; `scripts/repin.py:759`.

**F2 — Nonblocking: separate observation from inference.** “Cannot assemble git
commands” is stronger than the recorded capability statement. **Satisfier:**
quote or accurately summarize the request for reusable scripts suitable to this
Maintainer, and label any further usability assumption. -- Context;
`dev/plans/2026-10-28-test-trust-boundary.md:514`.

**Covered:** claims/reuse/drift (#1,5,6): v0.5 driver and archived plan above;
production path/completeness/failure (#2–4): `run_ceremony`, `build_packet`,
`check_stop_records` in `scripts/repin.py` and runbook steps 1–3;
lifecycle (#7): trust plan C4–C5 and proposal documentation routing;
scope/domain/satisfiers (#8–9): queued row, F1–F2; no scientific claim.
**Not covered / low confidence:** implementation does not yet exist; no ceremony,
signing, ref movement, mutation or full suite run. This pass does not discharge
the separate Security Review.

## Review -- Codex (gpt-6.1-sol, high), Security Reviewer -- 2026-10-29

```
Reviewed commit: 9c331e14ac232d3f7012b5bb8b9b1d068b26321b
Target: opening proposal, trust-ceremony boundary
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** Yes, with the inherited independent scan preserved explicitly. Authenticating prior P, checking raw candidate C and obtaining bounded human dispositions can reduce assembly errors without granting candidate authority. -- Proposal; `scripts/repin.py:273`; `bootstrap/REANCHOR_RUNBOOK.md:74`.
2. **Best alternative.** Extend the existing driver and staged launcher, retaining its ordinary refusal until a reviewed transition can demonstrate equivalent safeguards. The manual runbook remains the stopping path if that cannot be shown. -- `scripts/repin.py:975`; `scripts/repin.py:1162`; `bootstrap/REANCHOR_RUNBOOK.md:229`.
3. **What would show it wrong.** A candidate checker can substitute its own scan digest, a protected HOLD receives an unbounded waiver, or signing starts before authenticating prior authority and completing full collection. -- `bootstrap/reanchor.sh:766`; `bootstrap/REANCHOR_RUNBOOK.md:87`; `bootstrap/REANCHOR_RUNBOOK.md:95`.

The proposal's strongest design choice is keeping prior authority separate from
candidate evidence. It explicitly retains signature authentication, immutable
candidate bytes, full collection with the key away, protected HOLDs, and human
approval. It also admits that candidate pytest code remains host-capable; byte
checks do not establish containment. A transition is work to demonstrate, not a
flag that bypasses the current refusal.

**SR1 — Blocking: retain E7 and both installation bridges explicitly.** The
promised comparison list is E1–E6, H and K. E7 is absent. E7 independently runs
the prior anchor's scanner and compares its digest with the report; the report's
own claim that its scanner is anchored is insufficient. The current runbook
requires the dormant-roster and active-checker bridges as separate reviewed,
Maintainer-authorized ceremonies, each with its own candidate, packet, reader
record, comparisons and E7. The checker deliberately retains the old scanner's
semantics during these transitions. A generic promise to preserve stage
comparisons leaves this independently established value outside the named
contract. -- Proposal; `bootstrap/REANCHOR_RUNBOOK.md:17`;
`bootstrap/REANCHOR_RUNBOOK.md:64`; `bootstrap/tests/_gate_preflight.py:1637`.

**Satisfier:** explicitly preserve E7 from authenticated prior P, require its
agreement with the report before signing, and retain both distinct bridge
ceremonies and authorizations. Map scratch tests through the delivered public
commands proving an altered candidate scan digest refuses in each bridge, with
passing controls; reuse the existing adversarial case in
`bootstrap/tests/test_repin_ceremony.py:1533`. No outcome is removed.

**Covered:** claims, production paths, completeness and refusal (#1–4):
`boot`, `manifest_status`, `build_packet`, `run_ceremony` in `scripts/repin.py`;
`bootstrap/reanchor-launcher.template.sh:42`; runbook steps 1–3.
Reuse, drift and lifecycle (#5–7): archived repin plan Source proposal;
trust plan C2–C5; runbook installation bridges; SR1.
Scope/domain and satisfiers (#8–9): proposal S1–S5 and SR1; no scientific result.
**Not covered / low confidence:** source inspection only; no implementation,
scratch ceremony, mutation, signing, key access, ref movement or full suite run.
This pass identifies the correction needed to discharge its Security Review
obligation; it does not authorize C4 or pushing.
