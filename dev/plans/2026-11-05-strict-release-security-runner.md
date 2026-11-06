# Plan: Strict release-security runner

**Source proposal**: dev/proposals/archive/2026-11-05-codex-strict-release-security-runner.md
**Author**: Codex GPT-5 (Plan author, Medium)
**Status**: implementing
**Waiting on Maintainer**: Windows executable-mode contract
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Make the release security check join native Mac and Windows evidence without losing either test order.

## Source proposal

Decision `d042dd33` accepts the heavy proposal: preserve the existing checks
and both suite orders, independently fix the expected native-node roster, and
make the existing runner the sole reader that can join two same-commit host
records into a release-security pass. Local success remains incomplete.

## Scope

Deliver the runner, release hook, focused tests and release documentation as
one independently finishable outcome. Preserve clean committed input, exact
detached bytes and pre/post checks, Bandit over the derived shipped surface
and live allowlist, `check_cairn.py`, all configured suite members and security
assertions, and fail-closed handling. Investigate Windows paths and executable
mode with native probes; change path representation only if the nested-path
probe confirms the mismatch, and retain meaningful mode detection or record an
unresolved barrier. Do not change trust records or the separate certification
pair. Candidate-controlled checks and unauthenticated record suppliers remain
limits, not claims of authentication.

**Reuse.** `bootstrap/security_check.py` already owns detached execution,
phases and byte verification; `bootstrap/tests/conftest.py` owns release
outcome enforcement; `scripts/quality_gate.py` owns the seeded suite and
other quality sub-gates. A search for release, skip, checkout and quality
entry points in those files found these owners. Extend them and their existing
test homes rather than create a second runner or evidence ledger.

### Documentation / doctrine surface

Update `SECURITY.md`, `docs/release-process.md`, `bootstrap/PROVENANCE.md`
and affected source comments to describe two local incomplete results and the
exact join command and Maintainer step. No governing doctrine change.

## Sequence

The existing runner and test infrastructure are available. Estimate two to
four focused workdays, plus availability of native Windows for probes; roster
coordination, platform behavior and review fixes are uncertain. The estimate
does not limit accepted work. Before control-flow edits, coordinate exact node
identities and fixtures with 2a's owner, reconcile committed moves, and record
the independently reviewed source and protected collection evidence. Do not
wait for 2a's remaining chunks, growth report or archive.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Establish and review the fixed native roster; probe Windows path and mode behavior. | Both plan reviews folded; 2a coordination before control-flow edits. | Roster basis and native probe evidence, with any barrier named. |
| C2 | Implement per-order evidence, local validation and same-runner join; update docs and tests. | C1; retain every existing phase and test selection. | Fail-closed runner and documented operator path. |
| C3 | Complete ordinary and Security code reviews, fixes and wide Boundary B. | C2 committed with iteration evidence. | Reviewed, verified implementation ready to archive. |

The final v0.7 strict run is a separate named release follow-up: the Maintainer
obtains Mac and Windows records at the final candidate SHA, runs the join and
puts all three outputs in existing release notes. Track this as a standalone
board wait at the board's serialization point, with owner, evidence and a
link to this implementation; no board edit is part of this opening. It stays
unpassed until that evidence exists and does not gate plan archive. Archive
does not authorize release or a trust operation.

## Acceptance criteria

**C1.** List every expected Mac-only and Windows-only node from independently
reviewed committed test source and protected collection records, not host
observations. Reconcile 2a moves and fixtures before editing control flow.
On native Windows test a nested committed path and executable-mode handling;
preserve each leaf and meaningful mode detection. An unexplained failure or
unresolved Windows barrier remains implementation work, not a release pass.

**C2.** Both full selections run: direct default order and the quality gate's
seed 0, along with neutrality and redundancy. Only named opposite-platform
skips are locally eligible; unexpected or collection skips, xfails, xpasses,
failures and missing nodes refuse. Each order writes exact collected outcomes
to an external temporary path; the runner validates them against the fixed
roster and emits a structured local record with full SHA, platform, Python
3.13, roster identity, phase results and each expected outcome in both orders.
Successful local execution says `INCOMPLETE` and exits 5; a child pytest exit
5 is failure. Only the same runner's explicit join against clean final HEAD
can print `PASS` and full SHA, after exactly one native pass per expected node
per order and validation of both records. Missing, duplicate, malformed,
wrong-platform, wrong-SHA, roster-mismatched or failed-phase evidence refuses.
No report enters the byte-verified checkout. Documentation gives the actual
command, result, Maintainer ownership and residual supplier limitation.

**C3.** Independent ordinary and Security code reviews cover the committed
implementation; findings are disposed and required targeted follow-up occurs
before wide Boundary B. All accepted checks and any Windows barrier are
resolved before archive. The final native release ceremony remains separate.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: before edits use `python tools/test_tiers.py for <paths>`; run the
listed tests for changed files during iteration, plus standing prose gates.
Map changed behavior, callers, configuration, readers and public paths to
their test owners. Resolve moved paths after 2a coordination; current owners
include `test_security_check.py`, `test_broad_run_guard.py`,
`test_quality_gate_cli.py` and `test_quality_gate_order_independence.py`.
Run `python scripts/claim_check.py` on changed documents, link and snippet
checks, and the neutrality gate. Search for readers and byte pins.

Exercise the real entry point on committed fixtures: both suite processes,
all quality sub-gates, Bandit, `check_cairn`, byte-integrity refusal, external
report paths, labelled local exit 5 and join-only pass. Include the tiny
positive control and omitted or deselected expected node, duplicate outcome,
bad JSON/schema, collection skip, wrong platform or SHA, roster drift, failed
phase, xfail, xpass and unexpected skip. Test stale allowlist, removed phase
and changed checkout bytes. List the roster from the tree and mutate each
eligible native case in its own copy; retain repeatable controls in tests or
scripts and report outcomes and omissions. These are implementation checks,
not claims that they ran during planning.

Boundary C: ordinary and Security reviewers read committed work and iteration
evidence and run targeted falsification, not a suite. A substantive review
fix returns to the same reviewer for a targeted look before final integration.
Boundary B: after reviews run the iteration list for the reviewed range plus
mapped integration/workflow tests and plan-specific checks on a clean,
unchanged final commit under canonical Python 3.13.x. Use **wide** for this
trust ceremony; name owning families, public paths and standing gates. Append
the prescribed record with SHA and range, interpreter, clean pre/post state,
commands, counts, elapsed and token use, non-pass dispositions and omissions;
record timing misses. A missing required check keeps work open. Do not run the
full certifying suite during routine implementation; the separate authorized
certifying pair and the final release run remain unchanged.

## Plan review -- Codex GPT-5 (Medium) -- 2026-11-05

Reviewed commit: 9dd17bbfd6c84761c9a8e27441da0339444e432b

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the chunks preserve both full orders, fixed native expectations and the same-runner join, while leaving the final release ceremony outside archive -- plan C1-C3; proposal Decision `d042dd33`.
2. **Best alternative.** Manual comparison avoids a reader but leaves missing native outcomes to human inspection; extending the existing runner better delivers the accepted automatic refusal -- proposal Alternatives; plan Scope and C2.
3. **What would show it wrong?** A deselected native node or wrong-SHA counterpart producing a joined pass would disprove the evidence join -- plan Verification; proposal Tests required.

The plan makes roster review and 2a coordination prerequisites to control-flow edits, and specifies the two per-order reports, local incomplete result, child exit distinction and join refusals. Its final release wait has an owner and evidence without making archive a release authorization. Native Windows barriers and missing checks remain implementation work.

**Coverage:** Read the committed plan, accepted proposal and Decision, and plan template against the requested ordinary-review questions. No implementation, native execution, mutation, full suite or Security Review was performed; the roster and reader remain unbuilt.

## Plan review -- Codex Sol (High) -- 2026-11-05

Reviewed commit: `2ee80c60555e85aae4634333b36f7d847b0c2d98`

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Model attribution**: Sol (High), coordinator assignment per Maintainer.
**Findings**: no blocking findings; one non-blocking recommendation
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: C1-C3 deliver the accepted independent roster, both orders and same-SHA join without treating local success as release evidence -- archived source proposal, Proposal 1-6 and Decision `d042dd33`.
2. **Best alternative.** Extend the existing runner and release hook as planned; a manual join saves parser upkeep but cannot automatically refuse missing native outcomes -- `bootstrap/security_check.py::run_suite`, `bootstrap/tests/conftest.py::pytest_collectreport`, proposal Alternatives.
3. **What would show it wrong?** Deselection of one required native node, or substitution of one order's report for the other, producing joined PASS would falsify the contract -- plan C2 and Verification; `scripts/quality_gate.py::_run_order_independence` launches the distinct seeded process.

C1 fixes expectations from reviewed committed source and protected collection evidence before control-flow edits; host observations cannot define completeness. C2 keeps reports outside the verified checkout, binds both native records to clean final HEAD and the fixed roster, and distinguishes local exit 5 from child failure. Scope preserves byte checks, scanners and security assertions while explicitly retaining candidate-controlled logic and unauthenticated suppliers as limits.

**Recommendation (non-blocking):** Include duplicate JSON object keys and substituted order labels in C2's malformed/duplicate evidence controls. Require refusal through the real join entry point; ordinary JSON decoding can otherwise discard a conflicting value. This sharpens the existing contract, not its scope.

C3 requires both code reviews and final wide verification. Native Windows barriers remain implementation work; only the final Maintainer ceremony moves to a named board wait. Coordination with 2a does not require its unfinished archive, so the outcome is independently finishable.

**Coverage:** Compared committed plan, accepted proposal, AGENTS and current plan template; traced existing direct/seeded launches, release outcome hooks and reuse owners. Not covered: implementation correctness, native Windows probes, roster enumeration, mutations or suites; these remain required implementation evidence.

## C1 implementation checkpoint -- Sol (High) -- 2026-11-05

Assignment: Maintainer chat, this continuation, explicitly Sol at High for
Windows security judgment. Coordinator reports 2a timing finished and no
runner-file edits; exact runner, test and plan claims had no active overlap.
Base inspected: `b3b4141d`; concurrent unrelated commits were left alone.
Elapsed: unknown; tokens: unknown.

**Delivered:** Normalize only native relative leaf spelling to Git's `/`
representation, including directory symlinks. Byte, leaf-set and on-disk
executable-mode checks remain unchanged. No phase, trust record, release
outcome rule, board or changelog changed. This is a partial C1 checkpoint,
not C1 completion or permission for C2 control-flow edits.

**Native evidence:** SSH to the documented `cairn-windows` VM; Python
`C:\ProgramData\miniconda3\python.exe`, 3.13.17 ARM64; Git
2.56.0.windows.4. New disposable folders:
`C:\Users\cairn\AppData\Local\Temp\cairn-sol-mode-3jx7xv3y` and
`C:\Users\cairn\AppData\Local\Temp\cairn-sol-verify-rco0g3ae`.
No native pytest suite or collection was run.

The first probe committed `nested/leaf.py`: Git spells that path with `/`,
native `str(relative_path)` with `\`, and `as_posix()` with `/`.
Both requested chmod modes, 0644 and 0755, produced stat mode 0100666,
S_IXUSR false, os.access(X_OK) true and no forced-core.filemode diff.
Git initialized core.filemode=false. Setting the index to 100755 changed
the index but left stat mode 0100666. Thus index checks or access(X_OK)
alone cannot replace the promised on-disk mode detection.
Python documents that Windows chmod changes only the read-only flag:
[Python 3.13 chmod](https://docs.python.org/3.13/library/os.html#os.chmod).

The second probe transferred the changed runner, SHA-256
`1e9131bf9b370a11feaab2fefdef593a0c3cd54e5e1ee5c6d3d43312190a4116`.
It executed its parsed source with only scaffold imports removed (the
unrelated scan imports were unavailable in this small probe, not stubbed
security verifiers). The real path/tree/blob verifier accepted the nested
0644 fixture, refused changed bytes, an extra leaf and a missing leaf, and
refused the committed 100755 fixture after chmod(0755). This tests verifier
functions, not the complete detached-runner entry point or its imports.

**Unresolved barrier / grouped Scope delta request (not authorized):**
The current native Windows representation cannot deliver POSIX executable
mode through chmod/stat. No waiver or substitute has been implemented.

1. Keep the present refusal. No new mechanism or upkeep, but native Windows
   release evidence and C1 remain blocked; this does not finish the plan.
2. Explicitly change the contract to verify Git tree/index mode on Windows
   and actual disk mode on POSIX. Small implementation and test burden,
   but loses independent Windows on-disk mode-change detection; a mode-only
   disk mutation there would not be caught. Requires Maintainer allowance.
3. Define and implement a Windows ACL execution-permission contract, with
   native positive/negative ACL mutation probes. This adds a permission
   translator and security-sensitive platform maintenance; equivalence to
   Git's owner-execute bit is not established. Estimate uncertain, at least
   several focused days including design and independent reviews. Do not
   treat it as a representation-only repair or begin it under this checkpoint.

Recommendation: option 2 only with explicit acceptance of its lost safeguard;
otherwise retain option 1 until a separately agreed Windows permission
contract is available. No option waives the remaining checks or reviews.

**Roster status:** Host skips have not been used to define expectations.
Committed test source and `bootstrap/tests/fixtures/gate_manifest.json`
collection records were inspected, rather than collecting the native suite.
The protected collection record is not a current complete platform roster:
current source includes Windows drive normalization and the parameterized
binding-reparse cases not present in its node list. Source also has module
POSIX markers, aliased markers, capability-based skips and conditional
in-test skips; a census of literal os.name decorators is insufficient.
The fixed roster, reconciliation of those cases and independent roster
review remain C1 work. No runtime-derived roster or broad skip allowance
was added. This checkpoint makes no all-native-nodes coverage claim.

**Boundary A evidence:** Canonical macOS interpreter
`/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13.
`python tools/test_tiers.py for` the three claimed paths selected 13 files.
The runner test file initially gave 113 passed, one failed in 20.89 seconds:
the new synthetic Windows path fixture called is_symlink on a pure path.
The fixture was corrected; the affected node passed in 0.16 seconds and,
after adding directory-symlink coverage, in 0.14 seconds. No production
change was needed for that fixture failure. Three existing deprecation
warnings came from stevedore. The other 12 mapped files gave 256 passed,
11 failed in 63.90 seconds. All failures were in test_gate_manifest.py;
the clean-baseline assertions reported the two edited protected files as
FROZEN-MODIFIED. This is not a clean required-check result. Re-run the
affected manifest checks against committed bytes only when their collection
is authorized; do not change a trust baseline to make this checkpoint green.
The mapped manifest tests' session-scoped produced fixture performs a full
local collection subprocess. I missed that trigger before selecting the
mapped tests, exceeding the requested no-collection bound locally; it was
not repeated. No native collection, full suite or certifying suite ran.
The iteration timing target was
exceeded; per-file timings were not captured for the combined selection.
The runner file exceeded 10 seconds and remains a test-consolidation timing
observation, not a reason to omit it.

Prose gates on this checkpoint passed under Python 3.13.13:
`scripts/claim_check.py` and `scripts/check_cairn.py` on this plan, and
`scripts/quality_gate.py --sub neutrality` (zero failures, 43 informational
items). The documentation checker did not probe the external Python link;
its primary documentation was separately read online. No executable snippet
was added. Elapsed for these short checks: unknown; tokens: unknown.

**Omissions:** Complete roster and its review, C2 records/join and docs,
ordinary and Security code reviews, final wide Boundary B, native full
release run and all trust/release operations remain undone. This is not
Implementation verification or an archive-ready result.

Checkpoint committed as `37e70f6d`; working tree was clean immediately after
that commit. The manifest failures above have not been rerun, because doing
so would repeat the unauthorized collection. This correction records the
miss explicitly rather than presenting the mapped selection as bounded
collection. Elapsed: unknown; tokens: unknown.
