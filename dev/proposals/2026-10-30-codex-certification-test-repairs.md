# Repair certification test fixtures and isolation

**Author**: Codex (GPT-6.1 Sol)
**Status**: revising
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


## Review -- Codex (GPT-6.1 Sol) -- 2026-10-30

```
Reviewed commit: 82b08e8eb2ba215e846e1275436336691cf62a7d
Target: opening proposal
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes: repair the measurement inputs and test-process isolation while retaining the existing security assertions. The certification log shows dispatcher exit 20 instead of 5, the moved-plan read failure, and two trusted-import identity refusals -- `/private/tmp/cairn-cert-20261030-pytest.log`, failures section.
2. **Best alternative.** Keep the repairs local to the existing fixtures and test, using a child process for the committed-object scenario if that is simpler than completely restoring imported module and package identities; do not relax the production loader. Its replacement of parent packages and loaded modules makes incomplete cleanup hazardous -- `scripts/repin.py::load_listed`.
3. **What would show it wrong.** A repaired dispatcher that no longer detects the intentional renderer leak, a baseline preparation that accepts substituted evidence, or continued order dependence defeats the proposal's purpose -- `bootstrap/tests/test_security_finding_confidentiality.py::TestTheDispatcherAggregateReportIsANewSweptSink`, `bootstrap/tests/test_repin.py::test_baseline_preparation_builds_exact_package_after_reader_binding`, and the opening Evidence / verification plan.

The strongest version of this work restores the tests' ability to distinguish
safe behavior from deliberate violations. The proposal preserves those outcomes
explicitly, keeps the real dispatcher subprocess chain, and separates changing
protected test bytes from authorizing a new trust anchor. Doing nothing leaves
these five observed failures unresolved; changing production guards would answer
a different question and is correctly excluded.

The current evidence supports the isolation hypothesis, but does not establish
it completely: the log proves the `_gate_manifest` conflict, while the checked
loader explains a plausible mechanism. The parent agent relayed a focused
ceremony-then-authority run with one pass and one failure and an authority-alone
pass; I did not independently measure that run or inspect a saved transcript.
The proposal appropriately requires reproduction before selecting the repair.
Record that reproduction, then both orders and the existing refusal controls in
the implementation evidence. A subprocess is a recommendation, not a new
mechanism requirement; complete in-process restoration may also satisfy the
same isolation promise. No opened outcome is removed.

**Covered**: claims and drift -- the certification failures section and the
committed fixture/path reads; production path and fail-closed behavior --
`install_dispatcher` and both aggregate-report nodes in
`bootstrap/tests/test_security_finding_confidentiality.py`; design completeness
and scope -- the opening Proposal and Signals sections; cross-document and
lifecycle placement -- `AGENTS.md` protected-test policy and the proposal's
separate baseline/re-anchor boundary; domain applicability -- Independent
scientific check; satisfiers -- the exact controls above and ordered-run
criterion. **Not covered / low confidence**: no tests or mutations run in this
proposal pass, no independent ordered reproduction, no implementation yet, and
no full-suite or historic-anchor comparison. This usual review does not clear
the separate Security Review obligation.


## Review -- Codex Security (GPT-6.1 Sol) -- 2026-10-30

```
Reviewed commit: e44555471a23bce0d55f0e8f5aa61b035375ef0c
Target: opening proposal and usual review
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes: restore the intended security measurements without relaxing their guards; incomplete runner records cannot reach the intended dispatcher leg -- `templates/modules/default-on/run_security_verification.py:539` and `bootstrap/tests/test_security_finding_confidentiality.py::install_dispatcher`.
2. **Best alternative.** Put the real boot-and-record scenario in a child process, retaining both successful record checks around the worktree rewrite; this gives imports a natural lifetime without changing the checked loader -- `bootstrap/tests/test_repin_ceremony.py:1841` and `scripts/repin.py:643`.
3. **What would show it wrong.** Loss of the deliberate renderer leak, acceptance of an incorrect preflight digest, execution of candidate preflight bytes, or a remaining order interaction defeats the repair -- `bootstrap/tests/test_security_finding_confidentiality.py::TestTheDispatcherAggregateReportIsANewSweptSink`, `bootstrap/tests/test_gate_reanchor.py:272`, and `bootstrap/tests/test_gate_reanchor.py:331`.

The security value is restored reachability of existing adversarial tests.
The confidentiality fixture currently omits runner provenance fields required
by the real dispatcher; fixing the record must retain exact runner hashes and
reach the child-launch assertions. The leaking-renderer case deliberately
expects a leak as proof that its sink sweep can observe one. It must continue
to pass by detecting the planted marker, while the pristine case passes by
finding none. Converting either into a mocked renderer or a mere successful
exit would lose that distinction.

The authority tests independently construct scratch authority and require a
bad digest to refuse. Stage B also plants executable candidate bytes after
committing its candidate, then proves those bytes were not executed. Preserve
these controls rather than changing module-identity or source-authentication
guards to tolerate polluted imports. The loader overwrites parent packages
and checked modules in `sys.modules`; a child process is my recommendation,
not a required implementation choice. The proposed reproduction must still
establish causation before implementation settles on isolation.

The moved-plan repair must retain the baseline command's credential sentinel
and evidence-refusal branches, not replace the scenario with a path-existence
assertion (`bootstrap/tests/test_repin.py:260` and `:282`). The proposal correctly
keeps current manifest pins authoritative and separates test repairs from
installation of a new trust boundary. This acceptance grants no live-ref
update, historic-anchor comparison, or ceremony waiver.

**Covered**: claims and drift -- committed dispatcher record validation and
test fixtures; production path and fail-closed -- the real dispatcher chain,
bad-pin refusal and Stage B candidate marker; completeness and alternatives
-- loader package replacement and retained committed-object checks; consistency
and lifecycle -- `AGENTS.md` protected-test policy and the opening Proposal;
domain and scope -- no scientific change and no production change proposed;
satisfiers -- existing adversarial controls and both ordered sequences in the
opening verification plan. **Not covered / low confidence**: no implementation
exists, no independent order reproduction or mutation performed in this pass,
no full suite, and no historic-anchor comparison. This clears the proposal's
Security Review obligation only; the plan and code retain their own reviews.
