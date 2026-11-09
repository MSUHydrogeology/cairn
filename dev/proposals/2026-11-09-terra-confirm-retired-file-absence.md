# Confirm retired-file absence before clearing its record

**Author**: Terra (gpt-6.1-terra)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-09
**In brief**: Keep a retired file's record when the upgrade cannot confirm that the file is absent.

## Decision summary

An upgrade can currently report a retired file removed and clear its tracking
record even when access was denied and the file remains. Change the two
fallback absence confirmations to distinguish a missing file from an error,
and update the regression tests to exercise the actual error. This is a small
engine and test correction; it retains the existing path-based fallback's race
limits and adds no public interface or record format.

## Context

`bootstrap/_scaffold/security.py` uses `os.path.lexists` in the path-based
fallback both for confirmation-only calls and after an attempted unlink. It
returns false when the underlying `lstat` is denied, making denial look like
absence. The handle-based branch already distinguishes missing from other
errors. A Python 3.13.13 probe observed `lexists` return false on injected
`PermissionError` while the file and its bytes remained present. The three
regressions `test_confirmation_only_stat_denial_does_not_claim_absence`,
`test_post_unlink_stat_denial_does_not_claim_absence`, and
`test_access_denied_confirmation_cannot_clear_a_retired_record` in
`bootstrap/tests/test_upgrade_removes_retired_files.py` fail on the fallback;
the existing tests model the suppressed error at `lexists`.

## Proposal

In both fallback confirmations, call `os.lstat` explicitly: only
`FileNotFoundError` confirms absence; a successful stat or any other `OSError`
means keep the record. Preserve the existing path validation, identity checks,
handle-based behavior and documented fallback race containment. Adapt the three
regressions to inject denial at the actual confirmation `lstat`, retaining
reachability and file/record assertions. Deliver the correction for the next
upgrade capability. After acceptance, prefer incorporating this bounded work in
`dev/plans/2026-11-08-promise-unit-testing.md` if its review establishes one
coherent independently finishable outcome; otherwise use an appropriately
reviewed plan. Acceptance does not authorize crossing that plan's fences.

## Rationale

A missing-name exception is positive evidence of absence; an access error is
not. The change aligns the fallback with the handle branch without changing
what may be removed or promising stronger race protection.

## Alternatives considered

Leave the behavior unchanged: no implementation or new maintenance cost, but
an inaccessible surviving file can lose its tracking record. The narrow fix is
recommended because it preserves that record at the two failure sites without a
new mechanism.

## Documentation / doctrine surface

The existing upgrade contract in `bootstrap/UPGRADE.md` remains the target;
no doctrine or documentation change is proposed. Deliberation belongs here in
`dev/`, and any later descriptive correction belongs in the software docs.

## Evidence / verification plan

### Tests required

Run the affected test selection for the changed engine and test files, including
the three named regressions and existing removal, refusal and race tests. The
integration regression must exercise `upgrade --remove-retired` through its
existing entry point and assert a surviving file retains its record. Trace the
callers and consumers in the plan; use wide Boundary B for this high-risk
engine surface after review. A denial reported as absence, lost record, or
weakened existing containment falsifies the change. Record canonical Python,
commands, results and omissions; full-tree certification remains separate at
its authorized trigger.

### Examples / smoke checks

Run applicable claim, link, snippet and neutrality prose gates for this
proposal. Implementation verification includes the mapped public upgrade
workflow; no example gallery change is proposed.

#### Security preflight — five questions, answered in writing

- **S1:** The caller supplies a target path and expected shipped bytes from the
  upgrade's tracked data; the filesystem supplies name, metadata and errors.
  The project being upgraded can influence its paths and filesystem contents.
- **S2:** The three existing denial regressions currently fail in the fallback,
  providing a measured negative control, not a completed mutation of the
  proposed implementation. After adaptation, reintroducing error-to-absence
  behavior must fail them; that mutation has not been run yet.
- **S3:** The affected pytest file selects both fallback confirmations and the
  upgrade record case; the plan must specify the exact commands and expanded
  affected selection. The adopter contract says, “A kept file is not an error.
  It stays in the lockfile and `verify_integrity` keeps checking it.”
  The record regression checks that promise for denied confirmation; it does
  not by itself cover every kept-file case.
- **S4:** Missing means absent; successful stat or another operating-system
  error means kept, granting no additional removal or record-clearing authority.
  Existing validation and other error paths remain unchanged.
- **S5:** An actor able to alter project files or deny filesystem operations
  is in scope. An actor able to swap a parent directory in the path-based
  fallback's existing race window can still redirect removal, as documented in
  `bootstrap/SAFETY.md`; this proposal does not close that class.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Withdraw or revise if an error other than a missing name reliably establishes
absence, if the fix weakens the existing safety checks, or if the public upgrade
workflow still clears a record without confirmed absence.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance. The scaffold engine is a named high-risk
surface; usual review and a separate Security Review are required.
