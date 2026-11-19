# Reconcile release checks for platform-only tests

**Author**: Codex Sol
**Status**: awaiting-decision
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

## Ordinary proposal review — Terra (Reviewer, Medium) — 2026-11-19

**Verdict: ACCEPT. Findings: none.** The proposal reconciles file-level release evidence with the existing platform-specific list while retaining the separate native join.

**Should this happen as framed?** Yes. The recorded Mac XML has one pass and two Windows-only skips in the same file, and the existing file checker refuses skipped required cases. **Best alternative:** retain the present refusal; it would continue rejecting that expected evidence. An unrestricted skip allowance would weaken coverage. **What would show it wrong?** A current-platform or unlisted skip passing, a listed skip counting as a file pass, or the native join accepting a case that did not execute on its own host would falsify the assurance. The plan should specify malformed-policy and ambiguous-identity tests alongside the named cases.

**Evidence and limits.** Read proposal `ce02e4c9`, the recorded XML, the file checker's identity and outcome handling, the native-list validation and release join instructions. No tests were run; I did not independently review the join implementation, other platforms or security boundaries. **Elapsed**: unknown. **Tokens**: unknown.

## Security proposal review — Sol (High) — 2026-11-19

Reviewed commit `ce02e4c97978be86c92f244e4e794b3cd229fe65`.

**Tier**: Security Review. **Findings**: none. **Verdict**: ACCEPT.

**Should this happen as framed?** Yes. The saved Mac JUnit report contains
one pass and two `pytest.skip` outcomes for exact Windows IDs listed in
`tests/security_manifest.py:290-291`. The file check currently refuses both
(`release/check_release_test_members.py:145-150`), while the release shell
already preserves the pytest exit status (`release/RELEASE_PROCESS.md:168-173`).

**Best alternative.** Keep the blanket refusal and its false rejection of
this report. The proposed literal read lets the report supply outcomes and
the existing manifest supply platform ownership. Keep validation of the
full policy and its digest, and preserve explicit adopter-list behavior
(`tests/security_manifest.py:656-691`, `release/check_release_test_members.py:48-58`).

**What would show it wrong?** The planned contract check should refuse an
xfail encoded as a skip, ambiguous or mislabelled identities, an exact
same-host skip, and a required file with zero passes. A listed node's failure
or error must still refuse. Both native records must still name the same
commit and roster, and each listed test must pass on its own host in both
orders (`release/security_check.py:732-771`).

**Evidence and limits.** Read the saved Mac XML, the manifest validator, the
comparison and the native join. At plan review, check that the literal reader
rejects competing bindings and mismatched policy digests. The waiver should
match only a genuine `pytest.skip` with the full file, class and case identity
including parameters. No test reruns or implementation review.

**Elapsed**: unknown. **Tokens**: unknown.
