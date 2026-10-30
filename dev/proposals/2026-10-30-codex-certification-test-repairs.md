# Repair certification test fixtures and isolation

**Author**: Codex (GPT-6.1 Sol)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Repair test fixtures and process isolation so certification can measure the security properties it intends to test.

## Context

The certification run at `8b51bb2e20f8703e6caf4c73f2a09f0ad8deeb38` reported 5,622 passes and six failures; five concern the test infrastructure proposed here. The two aggregate-report confidentiality nodes in `bootstrap/tests/test_security_finding_confidentiality.py` fail with a hand-built lockfile that lacks the required `src` and `verbatim` fields. `bootstrap/tests/test_repin.py::test_baseline_preparation_builds_exact_package_after_reader_binding` copies a plan from its former location; the plan now lives at `dev/plans/archive/2026-10-29-forward-trust-baseline.md`.

The two failures in `bootstrap/tests/test_gate_reanchor.py`, `test_authority_pin_reads_v2_frozen_entry_digest` and `test_rostered_stage_b_executes_only_preflight_bytes_pinned_by_p`, involve module identity after `bootstrap/tests/test_repin_ceremony.py::test_record_check_uses_committed_objects_after_worktree_rewrite` invokes `REPIN.boot`: `scripts/repin.py` loads checked modules into `sys.modules`, replacing names already imported by the test process. The ordered interaction needs an explicit reproduction before a repair is chosen. The sixth failure concerns upgrade behavior and is outside this proposal.

## Proposal

Repair the hand-built records to conform to the existing lockfile contract, point the baseline test at the archived plan, and isolate the ceremony test's boot so its checked module imports cannot contaminate subsequent tests. Preserve the confidentiality test's real dispatcher and both pristine and deliberately leaking renderer cases; preserve the baseline test's independently bound evidence and refusal cases; preserve the reanchor tests' authority-pin and pinned-preflight assertions. Do not weaken production guards or alter their expected security properties. Reproduce the ordered interaction and verify isolation in both test orders.

The four test files are presently byte-pinned in `bootstrap/tests/fixtures/gate_manifest.json`. They also appear as protected Python paths in `bootstrap/tests/fixtures/protected_test_roster.json`, which describes a proposed classification, not live authority. Do not treat that proposed roster as a replacement for the current manifest or assume these are ordinary tests. A separate authorized baseline and re-anchor process handles changes to the trust anchor; this proposal does not update any live ref or compare with a historic anchor.

## Rationale

Correct fixture inputs and test isolation restore the measurements without changing the system under test. Isolating the boot must preserve the test's committed-object and rewritten-worktree checks rather than substituting a mock.

## Alternatives considered

Leave the failures in place: certification would remain unable to distinguish a regression from fixture drift and test-order contamination. Change the security checks to accept incomplete records or mixed module identities: that would weaken the protections the tests exist to exercise.

## Documentation / doctrine surface

This proposal is deliberation in `dev/proposals/`. No governing doctrine or adopter-facing contract change is proposed.

## Evidence / verification plan

### Tests required

Use the canonical Python 3.13 interpreter. Exercise both confidentiality nodes, the baseline preparation node, and the two reanchor nodes named above, including the ceremony test immediately before each reanchor node and in reverse order. Verify their existing positive and negative controls, and map other consumers and standing gates in the plan. Test in an isolated copy, with no live ref updates. A failing control, a surviving deliberate leak, or an order-dependent result falsifies the repair. Certification remains a separate authorized integration run.

### Examples / smoke checks

Run the applicable manifest and claim checks in the reviewed plan; do not run the full suite merely for this change. This proposal's claim check runs before its opening commit.

#### Security preflight

1. **Inputs:** test-authored records and scratch repositories feed the existing dispatcher and ceremony checks; the checked candidate supplies its own bytes, while authority comes from the test's independently established scratch anchor.
2. **Failure:** the confidentiality test already includes a deliberate leaking renderer; the baseline test includes missing or substituted evidence refusals. Their controls must be run after repair; no new mutation has yet been run.
3. **Trigger:** pytest selects the named nodes and the ordered sequences in the implementation plan. They exercise scratch inputs, not an adopter-facing new check; no adopter-facing sentence is changed.
4. **Failure direction:** invalid fixture records and untrusted authority must still refuse; no production fallback or parser is changed.
5. **Residual capability:** a malicious change outside the mapped tests can still evade these checks; these tests do not establish whole-tree security.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Withdraw or redesign if the ordered failures have a different cause, if isolation hides the actual committed-object behavior, or if a repaired test passes when its existing adversarial control should fail.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance
