# Reconcile release checks for platform-only tests

**Author**: Codex Sol
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy
**Plan review**: not required(no plan: light tier)
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
(`tests/security_manifest.py:573-608`, `release/check_release_test_members.py:48-58`).

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

## Decision -- Maintainer (recorded from chat by Claude Sonnet 5.5, not scribed by Antigravity) -- 2026-11-19

**Tier**: light

**ACCEPTED**, by the Maintainer in chat, 2026-11-19: "Accept this at light. Also, if things need to be run on Windows, go ahead."

This accepts the proposal as written, at the light tier instead of the proposed heavy: no plan; the proposal is the implementation and final verification record. The checks the Security Review left for plan review (the literal reader rejects competing bindings and mismatched policy digests; the waiver matches only a genuine `pytest.skip` with the full file, class and case identity including parameters) become required tests in the implementation. The Maintainer also authorized running whatever needs a Windows host over `ssh cairn-windows` (`dev/rules/development-environment.md`). New recurring human operations: none. If the change goes wrong, `git revert` of the implementation commit restores the strict refusal.

## Security Review of the implementation -- Claude Opus (Security Reviewer, High) -- 2026-11-19

```
Reviewed commit: 1ea3ba830fc4e361ccb811f100793bf7ed7a852c
```

**Tier**: Security Review
**Findings**: raised (non-blocking only)
**Verdict**: ACCEPT

**Elapsed**: about 4 minutes (11:30:10 to 11:34 EST, from `date`)
**Tokens**: unknown

**Obligation.** Can the new waiver let a required test go unrun, or a failing or forged result pass, on the host that should run it? No, as far as this quick pass reached.

**Steelman.** The change lets the Mac file-level check accept only the Windows-only skips the manifest already names, so the strict check stops refusing a correct report while the native join still proves each platform-only test ran on its own host.

**Foundations**

1. **Should this happen as framed?** Yes; the diff does what the accepted proposal says and no more -- `git show 1ea3ba83 --stat` (three files; `release/security_check.py` untouched, `git diff 1ea3ba83~1 1ea3ba83 --quiet -- release/security_check.py`).
2. **Best alternative.** Keep the blanket refusal; it is safer only by refusing correct Mac reports -- `release/check_release_test_members.py:303-320` (`_refuse_unless_listed`).
3. **What would show it wrong.** A same-host skip, an xfail, an unlisted skip or an all-skipped required file passing; each refuses in a synthetic run (scratchpad `nrm/run.py`: `skip-not-genuine`, `identity-ambiguous`, `required-file-no-pass`) and in the named contract tests -- `tests/contract/test_release_members_contract.py:458-644`.

**Checks against the diff.** (a) Policy read: `ast.parse`, never import; any static binding (assign, augmented, walrus, `for`, `del`, import, `global`, class or function name) beyond one refuses; values go through `ast.literal_eval`; the digest is recomputed from the literal records -- `check_release_test_members.py:117-194`. (b) Identity: file from the resolved classname, classes from the classname suffix, case name kept whole with its parameter label; type must equal `pytest.skip` (xfail is `pytest.xfail` and refuses); two report cases mapping to one node refuse -- lines 197-202, 279-284, 316-319. (c) Host: `os.name` of the checker process only; nothing in the report is read for it -- lines 112-114, 335. (d) Waived skips never enter `successes`; an empty or all-skipped required file refuses -- lines 287-300. (e) `--required-files` sets `native` to `None`, skips the manifest read and any skip refuses -- lines 335-336, 309-310. (f) The native join is not in the diff.

**Findings**

1. Non-blocking. The host tag is the checker's host, not the host that produced the report. If a Windows-produced report were ever checked on a Mac, a Windows-only test skipped on Windows would be waived here. Today the checker runs right after pytest on the same host (`release/RELEASE_PROCESS.md:171`) and the native join still requires each listed test to pass on its own host, so no action is needed now.
2. Non-blocking. A case named `TestA::test_w[x]` under the module classname maps to the same node as class `TestA`, case `test_w[x]`, and is waived. It cannot reach another file or another listed node, and pairing both forms refuses as `identity-ambiguous`; no action.
3. Non-blocking. The binding check sees only static bindings; a runtime rebind such as `globals()[...] = ...` would not change what this checker reads (the literal), only what code that imports the manifest sees, which `tests/security_manifest.py:584-608` validates itself.

**Coverage.** Read the full checker diff, the compare loop, the proposal, its two reviews and the Decision, and the test names for (a) to (e); ran one synthetic-XML reproduction with five cases. Not checked: the Windows behavior of the xunit1 `file=` backslash form reported for an old test; the Windows-host branch of `_host_tag()` on a real Windows run (the checker is Mac-run in the release block); the release shell around line 171; the test bodies beyond their names; no test suite was run.

## Implementation record -- Claude Sonnet 5.5 (coordinator) -- 2026-11-19

Built by a Sonnet implementer at `1ea3ba83` (`release/check_release_test_members.py`, `tests/contract/test_release_members_contract.py`, `release/RELEASE_PROCESS.md`; no other file). Security quick pass of the implementation: ACCEPT, 0 blocking, 3 non-blocking (`17ba5fca`).

**Measured.** Against the old checker the contract file had 87 failures and 46 passes of 133; after the change 136 pass. 32 single-line mutants, all killed. `tests/test_security_marker.py` 29 passed. `claim_check`, `link_check`, `sync_doc_snippets` and neutrality on `RELEASE_PROCESS.md` are clean. Windows (clean `git archive` of `1ea3ba83`, `cairn-windows`, x64 `lhm`): 9 failed, 127 passed; all 93 new tests pass; the 9 are older tests (8 need `bash`, which is not on the SSH path, and one timing flake), and the base commit `c45548c7` failed the same 9 (34 passed). With Git bash on the path: 2 failed, 134 passed; one is the xunit1 report whose `file=` attributes use backslashes on Windows, which the unchanged `_file` refuses. That form is not part of this change, and the file-level comparison runs where pytest runs (the Mac block).

**Interpretations.** The host is `os.name`, read where the checker runs; a genuine skip is `<skipped type="pytest.skip">` exactly; the policy is read eagerly in default mode (a bad or absent policy refuses even with no skip); every failure line ends with a stable `[code]`; the PASS line counts accepted listed skips.

**Security notes kept, not changed.** (1) The host is the checker's machine, not the report's: a Windows report checked on a Mac would let Windows-only skips through; the native join still catches it and the checker runs beside pytest today. (2) A case name containing `::` maps to its listed test, only inside the same file; the normal form beside it refuses. (3) The binding check sees only written bindings; the checker reads literal records, so this does not matter.

**Not run.** Any whole suite, the native strict runs and join, and the gate and re-anchor tests; the Windows twin of the 9 older failures was not repaired. **Owed before archive.** The Maintainer's grouped re-anchor (frozen by glob: the checker and the contract test) and the joined targeted check.

**Benefit versus cost**: a Mac release report with expected Windows-only skips is no longer refused, for one narrow exception that every other check still bounds; the cost is one new code path in a release checker and 93 tests.
