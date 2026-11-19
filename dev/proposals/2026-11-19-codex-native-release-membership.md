# Reconcile release checks for platform-only tests

**Author**: Codex Sol
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-19
**Rules that apply**: dev/rules/certifying-runs.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md
**In brief**: Use the existing native test list when checking the release test report.

## Decision summary

The Mac release check refuses a test file when two Windows-only tests skip as expected. Allow a skip in Cairn's file-level report only when the existing list names the exact test for the other platform. Each required file still needs a passing test. The separate Mac and Windows release records still have to show that each platform-only test ran on its own platform and join successfully. This changes the file-level checker, its tests and the release instructions.

## Context

Three focused public tests in `tests/test_portable_security_sweeps.py` produced one pass and two Windows-only skips on Mac under Python 3.13.13. `release/check_release_test_members.py` refused the report because the skipped nodes belong to a required file. `tests/security_manifest.py` already names the two exact nodes as Windows-only, and the native release join independently validates that list and their outcomes.

## Proposal

In Cairn's default file-level comparison, use the existing native-only policy for the host running the report. Read its literal records and identity from `tests/security_manifest.py` without importing candidate code. Validate record shape, unique identities and digest. Translate the opposite-platform node identifiers to the report's existing file, class and case identity, preserving parameter labels and rejecting ambiguous identities. Allow only a proper skip for an exact matching node. A listed skip does not count as a pass. Preserve required-file coverage, all failure and error checks, and strict handling for missing or malformed evidence. An explicit adopter-supplied required-file list keeps its current behavior.

Keep the current full run, both native strict runs, and their join. The native join continues to reject unauthorized skips and to require the named test to execute on the correct host. Add no platform list, tool or command option. Document which check proves each result.

## Rationale

The same platform-only classification should apply to both release checks. The file-level comparison can allow a skip only when the independent list identifies the test as belonging on the other host. The join remains the check that it actually ran there.

## Alternatives considered

Drop the file-level check or allow any skip. Either permits missing coverage that the current checker is meant to detect. Running the full suite again with the same checker would still reject the expected skips.

## Documentation / doctrine surface

Update `release/RELEASE_PROCESS.md` to describe Cairn's listed exception and the separate native evidence obligation. No shipped adopter instructions or doctrine change.

## Evidence / verification plan

Use `tests/contract/test_release_members_contract.py` to exercise an exact opposite-platform skip with another case passing in the same file. Verify that a current-platform or unknown skip, a missing passing case and a failure or error still refuse. Keep existing tests of adopter-owned lists. Run only the affected contract cases before final certification.

### Security preflight

The report supplies outcomes, while the existing manifest supplies platform ownership. Malformed policy, report identities and unknown skips refuse. The comparison grants no release authority. The native join is still required and checks the complete outcomes on both hosts.

### Independent scientific check

N/A. No scientific assumption or result changes.

## Signals the change is wrong

A required case can fail or skip on its own host and still pass the applicable checks, or an ordinary omitted security file still passes the file-level comparison.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance. The checker contributes release evidence. Obtain ordinary and Security Review before changing the rule.
