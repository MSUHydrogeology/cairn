# Plan: Strict release-security runner

**Source proposal**: dev/proposals/archive/2026-11-05-codex-strict-release-security-runner.md
**Author**: Codex GPT-5 (Plan author, Medium)
**Status**: revising-code
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

## C1 continuation -- Terra (gpt-6.1-terra) -- 2026-11-05

Role: Implementation. Inspected committed `f7687721826681f389388215e73d156864d74277`;
no full suite or full collection was run. Elapsed and token use: unknown.

**Independent classification of the 11 failures.** These were the following
nodes in `bootstrap/tests/test_gate_manifest.py`: `test_verify_clean_tree_is_ok`,
`test_verify_allows_added_test`, `test_ordinary_file_and_node_deltas_are_notes`,
`test_trusted_verifier_detects_tamper_in_separate_target_tree`,
`TestV1V2Differential::test_a_clean_tree_passes_under_both`,
`TestV1V2Differential::test_v2_notices_a_mode_change_that_v1_cannot`, and all
five parameters of `test_ordinary_changes_are_individually_reported_without_hold`
(`edit`, `addition`, `deletion`, `rename`, `marker`).

The test's `produced` fixture calls `_gate_manifest.produce`, which pins
frozen SHA-256s from Git `HEAD` blobs; `verify` compares those pins to current
disk bytes. At Sol's run the two protected files were edited before commit,
so their FROZEN-MODIFIED outcomes were expected for that dirty comparison.
This fixture does not load the shipped release manifest as its baseline.
The separate shipped `bootstrap/tests/fixtures/gate_manifest.json` does pin
the pre-`37e70f6d` versions: `bootstrap/security_check.py` SHA-256
`b8c3d6d787c007d8f5c6dd58f98ac85ca177a26af68ced3d4762671dae5bbd6d`
versus current `1e9131bf9b370a11feaab2fefdef593a0c3cd54e5e1ee5c6d3d43312190a4116`,
and `bootstrap/tests/test_security_check.py` SHA-256
`cc7d73479399ec5acc4c66c781c4c9d6eba71bf0cba1310db89622512ad61b3a`
versus current `05293badbea4c9b598a51b83ece211cfda64493df477465dee59703ab05d50b4`.
That is genuine committed-baseline drift, not the cause of these 11 fixture
failures and not a passed trust check. No baseline or trust record changed.

In a separate no-hardlink clone of `f7687721`, canonical Python 3.13.13 ran
exactly those 11 nodes with a disposable pytest adapter replacing only
`_gate_manifest._collect` with the existing committed manifest's recorded
node and marker lists. Clean clone: 11 passed in 2.91 seconds. Adding one
comment to only `bootstrap/security_check.py` in that clone: those same 11
failed in 2.43 seconds. The adapter was
`/private/tmp/cairn_terra_no_collection.py`, SHA-256
`b18c176d9ed0ea3026662ae4d4bbfcd44939248205648935700f3c8910ea0c09`;
the invocation selected the six named single nodes and the five-parameter
node, with `-p cairn_terra_no_collection -p no:cacheprovider`. No other test
was selected. This demonstrates the dirty-byte cause on the listed assertions,
not a real-collector pass or proof against unrelated regressions. The previous
real-collector failures and required checks remain recorded; their post-commit
real-collector rerun is not authorized by this no-collection request.

**Fixed-roster progress, not an approved roster.** Source was inspected at
`f7687721`, and the existing collection record was read as data, not generated
from host skips. Its SHA-256 is
`871643a00296f695c3eebe1005636fabaf2ec60c4952eab305ff2800cf2930ed`.
The eight `test_windows_reparse_points_refuse_binding_access` cases are in
that record, contrary to the earlier checkpoint's statement. Their exact IDs
are in `bootstrap/tests/test_git_interpreter_binding_portable.py`, with these
test IDs:

- `test_windows_reparse_points_refuse_binding_access[shipped-admin]`
- `test_windows_reparse_points_refuse_binding_access[shipped-binding-directory]`
- `test_windows_reparse_points_refuse_binding_access[shipped-binding-leaf]`
- `test_windows_reparse_points_refuse_binding_access[shipped-dot-git]`
- `test_windows_reparse_points_refuse_binding_access[source-admin]`
- `test_windows_reparse_points_refuse_binding_access[source-binding-directory]`
- `test_windows_reparse_points_refuse_binding_access[source-binding-leaf]`
- `test_windows_reparse_points_refuse_binding_access[source-dot-git]`

Source also names `bootstrap/tests/test_intents_tool.py::test_windows_drive_case_normalization_for_pointer_chain`,
absent from that recorded list; source parameters and the eight recorded IDs
are independently fixed inputs for a candidate, not evidence the list is
complete. An AST read of the two upgrade test modules found 31 `posix_only`
functions with 78 recorded nodes, and 12 `posix_only` functions with 21
recorded nodes plus three `handles_only` functions with four recorded nodes,
respectively. The two session-binding modules have 43 and 37 recorded nodes
under their module-level Windows skip. Those totals are mapping aids, not a
claim that all are valid opposite-platform skips: individual case-sensitive,
root, missing-capability and conditional skips still need reconciliation.
`test_code_map.py`, `test_session_failsafe.py`, `test_session_writes_contained.py`,
`test_verify_integrity.py` and dynamic capability/fixture skips also require
node-by-node classification. No host-observed skip was promoted to authority.

**C2 preparation and fence.** `conftest.py` currently aggregates refused
runtime and collection reports, while `quality_gate.py::_run_order_independence`
launches its own seeded pytest child; the direct suite and this child both need
separate external outcome reports. The source roster, complete case mapping,
2a reconciliation and independent roster review are still missing. The plan
explicitly makes C1 a C2 gate and requires that reviewed source before
control-flow edits, so no C2 code or provisional skip allowance was added.
The Windows mode check was not changed; `docs/release-process.md` was not
claimed or edited. Ordinary and Security code reviews and wide Boundary B
remain outstanding.

**Checkpoint checks:** `tools/test_tiers.py for` this plan selected zero test
files. Under Python 3.13.13, `scripts/claim_check.py` and
`scripts/check_cairn.py` on this plan passed after correcting one malformed
path reference; `check_cairn.py` noted a missing local scanner allow file and
did not probe the external link. `scripts/quality_gate.py --sub neutrality`
passed with zero failures and 43 informational items. No executable snippet
was added. Concurrent edits to the scanner and link-check files were not
part of this checkpoint. Elapsed and token use: unknown.

## Maintainer scope allowance -- Codex (coordination) -- 2026-11-05

The Maintainer answered **"Use Git flags on Windows (Recommended)"** to the
coordinator's chat question recommending Git-recorded executable flags on
Windows and actual disk executable flags on macOS/Linux, while retaining
file-content checks on both. The question explicitly disclosed loss of
independent Windows-only disk-flag-change detection and the alternative of
leaving Windows release checking blocked or designing a larger Windows
permission checker.

This allows option 2 of the recorded Windows-mode Scope delta: verify Git
tree/index mode on Windows, retain actual disk-mode verification on POSIX,
and retain content, leaf-kind, containment and all other integrity checks.
No Windows ACL translator, broad skip allowance, roster approval or waiver of
remaining C1-C3 checks/reviews is granted. The fixed native roster still needs
independent reconciliation and review before C2. Elapsed: unknown; tokens: unknown.

## C1 roster Security Review -- Codex gpt-6.1-sol (High) -- 2026-11-05

Reviewed source: `88679232404f5e5ec72aab8f5f9799710f10d483`;
native source is unchanged from the isolated `210e2501` copy.
This reviewer did not author the 220-ID candidate or its earlier draft review;
both were treated as untrusted evidence. This is C1 reconciliation, not C3.

**Foundations**

1. **Should this happen as framed?** Yes, but C1 is incomplete: source-defined native requirements extend beyond the candidate's known skips -- finding R1; C1/C2.
2. **Best alternative.** Preserve exact exceptions and required host capabilities; a host-observed skip roster would conceal omitted coverage -- accepted proposal items 3-5.
3. **What would show it wrong?** Renamed source or changed parameters escaping reconciliation would defeat the inventory; the retained controls detect both. Eventual per-ID omission controls through the real join must still fail -- `bootstrap/tests/test_security_check.py`, native-roster inventory tests.

**Verdict:** HOLD C1; no C2 clearance.
**Elapsed:** unknown. **Tokens:** unknown.

Static reconciliation found no missing source names or literal-ID mismatches
among 220 candidates. The helper leaves 57 dynamic/fixture cases explicit;
manual AST expansion matched all 57. Both module-wide exclusions and aliased
markers were reconciled. Five source identities lack protected records:
Windows drive normalization, three code-map cases, and strict-reader `[fifo]`.
Committed consolidation moves do not rename these native identities.

**R1 (blocking): Finish precise source dispositions, without blanket skips.**
In `bootstrap/tests/test_security_leaf.py`, the isolated
`test_permissions_strip_execute_and_special_bits` is genuinely POSIX-only;
split `/dev/null`/FIFO assertions in `test_special_files_refused_without_blocking`
from its portable directory assertion. Similarly separate FIFO from portable
link checks in `bootstrap/tests/test_code_map.py::test_real_cli_refuses_links_and_special_files`.
Keep report containment/exclusive-write checks on both hosts, separating native
0700/0600 assertions in `bootstrap/tests/test_security_net.py`'s
`test_a9_report_directory_is_private_and_outside_the_repository` and
`bootstrap/tests/test_security_finding_confidentiality.py`'s
`test_d3_the_temporary_directory_holds_only_the_report[clean]` and `[findings]`.
The shared `templates/modules/team-gated/_security_net/report.py` uses chmod/open
modes without Windows-equivalent verification or refusal; both module doctrines
already mark Windows permission equivalence unverified. These recommendations
preserve that limitation, not a new Windows privacy claim.

Use explicit Git index-mode mutations for the two
`bootstrap/tests/test_gate_manifest.py::TestV1V2Differential` mode controls;
`_gate_manifest.py::_tree_blobs` reads raw HEAD modes, so this preserves their
committed-mode property, not a disk-mode substitute. Reconcile exact
shell/pty callers of `bootstrap/tests/test_reanchor.py::_run`,
`bootstrap/tests/test_repin_ceremony.py::drive` and `stop_after_pin`, plus the
printed-launcher case in `bootstrap/tests/test_reanchor_driver_disclosures.py`.
The published launcher contract fixes `/bin/sh`, POSIX syntax and
`PATH=/usr/bin:/bin`; terminal helpers require Unix pty. Classify those actual
callers, retaining portable source checks. Close R1 with committed exact nodes
and retained native assertions; settled fixture/mode work can proceed in C1.

**Classification: Separate native API absence from environment absence.**
Of 23 capability candidates, seven require FIFO, two fchmod, and thirteen
descriptor-relative operations/O_NOFOLLOW. Those support exact Unix-native
classification. The zsh hazard case exercises the prescribed POSIX shell and
startup-file mechanism; classify that exact mechanism, not missing-tool status.
Its `/bin/zsh` remains a required native-host prerequisite, not a tool waiver.
Missing tools, symlink rights, case-insensitive volume or non-root execution
remain fail-closed prerequisites, not extra exemptions.

**Windows mode implementation contract:** allowance `210e2501` permits comparing
the complete stage-0 Git index path/mode/object set against the committed tree
on Windows, refusing missing, extra, duplicate, unmerged or changed entries.
Retain disk leaf-kind, containment and blob-byte checks on both hosts and
actual owner-execute checks on POSIX, before and after phases. Test Windows
index-mode mutations; do not infer disk execution permission from Git or add
an ACL translator. This contract is proposed, not implemented evidence.

**Coverage:** Source/protected-record reconciliation and two bounded helper
controls (Python 3.13.13: 2 passed, 0.19 s; three existing stevedore warnings)
on a separate `210e2501` copy with exact helper/test bytes later committed at
`1cc5004b`. The three mapped owner files were not run in full under the
no-collection bound. No broad/native collection, suite, native rerun, join, trust or
release operation ran. Over target to name unresolved source obligations and
the narrow mode contract; no complete-roster claim or skip waiver is made.

## C1 roster reconciliation addendum -- Codex gpt-6.1-sol (High) -- 2026-11-05

The preceding R1's shell/terminal caller expansion is now resolved against
source and existing protected IDs, without collection. The existing temporary
candidate JSON contains 584 distinct proposed identities: nine Windows-native
and 575 Mac-native requirements. Its SHA-256 is
`80376a0047fea13506a441e5ca793b4860795bf7d84d10fcfa62cad60d81388a`.
This is a reviewed source inventory, not an approved production skip roster.

The bounded transformation reconciled 365 shell/pty identities: 205 in
`bootstrap/tests/test_reanchor.py`, 102 in
`bootstrap/tests/test_repin_ceremony.py`, 45 in
`bootstrap/tests/test_repin.py`, twelve in
`bootstrap/tests/test_gate_preflight.py` and one in
`bootstrap/tests/test_reanchor_driver_disclosures.py`. The zsh case already
appeared in the original candidate, so 364 identities were added. Literal
parameters matched source; all 64 named-constant/comprehension identities were
independently expanded and matched. No dynamic identity remains unresolved in
these caller groups. The additional source-only identity is
`bootstrap/tests/test_reanchor.py::test_bed_copies_keep_refs_and_keys_independent`;
six proposed identities now lack protected records.

**Remaining C1 work:** Commit the named mixed-test splits and reconcile their
final node identities. Move the module-level Unix `pty` import in
`bootstrap/tests/test_repin.py` into `run_pty`/`run_mixed`, preserving portable
tests and allowing function-level native markers to take effect before setup;
its import currently also affects the two modules importing its helpers.
Complete the separately authorized Windows mode work. These are implementation
steps, not an unowned caller-inventory follow-up. C1 remains HOLD; C2 is not
cleared. No broad skip or missing-tool allowance is granted.

**Coverage:** Static syntax, direct/transitive shell and terminal calls,
class helpers, source parameter declarations and protected record identities.
No test source was imported or evaluated, no host skips supplied expectations,
and no further pytest, broad/native collection, trust or release operation ran.
Elapsed and tokens: unknown.

## C1 implementation checkpoint -- Codex gpt-6-luna (Low) -- 2026-11-05

**Source commits:** Windows mode verifier and portable gate-manifest fixtures
`4f7337a65b72a1d429cfbbb021f336f1d16c9d71`; mixed native/portable test splits
and lazy pty imports `841f0036bfd9caa1cc364c5871b4c69f66d776d1`.

**Windows mode evidence:** Maintainer chat authorization: “Allow Cairn source
in this local VM (Recommended)” and “It's not egress. It's a local machine”.
Transferred only committed runner, test and direct scaffold import files from
`4f7337a65b72a1d429cfbbb021f336f1d16c9d71` to disposable local VM folder
`C:\Users\cairn\AppData\Local\Temp\cairn-luna-c1-4f7337a6`; archive
SHA-256 `b00c1e85679a20fda3324be429da7ffc1eb06e5fa92fb9f2167c2497658940bd`.
Windows Python 3.13.17, Git 2.56.0.windows.4: the four named
`test_security_check.py` selections produced six passes in 4.93 seconds.
They exercised nested committed paths, exact bytes and leaf changes,
matching 100755 tree/index mode, mode drift refusal, and malformed, duplicate
and unmerged index refusal through `_verify_committed_checkout` and
`_verify_committed_index`. This did not run the detached runner entry point,
native collection, a suite or a release operation. POSIX disk-mode checks
remain in place. Maintainer allowance `210e2501` remains the scope basis.

**Mixed-test changes:** Keep the directory refusal in
`TestReadRegularBytesRefusesAnythingElse::test_special_files_refused_without_blocking`;
move `/dev/null` and FIFO checks to
`TestReadRegularBytesRefusesAnythingElse::test_posix_special_files_refused_without_blocking`.
Keep link checks in `test_real_cli_refuses_links` (renamed from
`test_real_cli_refuses_links_and_special_files`); move FIFO diagnostics to
`test_real_cli_refuses_fifo`. Keep report containment/exclusive-write checks
in `test_a9_report_directory_is_private_and_outside_the_repository`; move
0700/0600 assertions to `test_a9_report_directory_and_file_modes_are_private`.
Keep D-3 report-only outcomes in
`test_d3_the_temporary_directory_holds_only_the_report`; move 0600 assertions
to `test_d3_report_file_mode_is_private[clean]` and `[findings]`.
`TestWriteByReplacing::test_permissions_strip_execute_and_special_bits` is
now explicitly POSIX-only. The pty import is local to `run_pty` and
`run_mixed`, so importing their helper module no longer imports Unix pty.

**Focused evidence:** Python 3.13.13 ran the nine selected node expressions
(thirteen cases including parameters), all passed in 3.70 seconds. The static
`tools/test_tiers.py for` mapping selected eleven files:
`test_api_access_security.py`, `test_code_map.py`, `test_reanchor.py`,
`test_repin.py`, `test_repin_ceremony.py`,
`test_security_finding_confidentiality.py`, `test_security_leaf.py`,
`test_security_marker.py`, `test_security_net.py`,
`test_security_verification.py` and `test_web_hosting_security.py`.
This mapped set was not run. The two `TestV1V2Differential` mode tests were
not run because their `produced` fixture starts a full collection; their
portable `update-index --chmod=+x` fixture and committed `100755` assertion
remain due for the approved no-collection control. No full collection, suite,
or broad batch ran.

**Remaining C1 gap:** The renamed/new native IDs above need incorporation into
Sol's source-based roster follow-up. The 584-ID inventory remains a reviewed
candidate, not an approved runtime roster. Exact shell/pty opposite-platform
handling remains with the roster policy owner; no scattered decorators or
broad skips were added. C1 remains incomplete and HOLD; C2 is not cleared.
Elapsed and tokens: unknown.

## C1 R1 targeted follow-up -- Codex gpt-6.1-sol (High) -- 2026-11-05

**Role:** Security Reviewer; replacement continuation after coordinator handoff,
not the original reviewer or author. This is the targeted second C1 pass on
R1 at `cc7a3a83`/`9b83c594`, not C3 code review.
Reviewed committed source: `4855ae283a9bf041019b890ebb05e9ef3b76d0fc`.

**Foundations**

1. **Should this happen as framed?** Yes: `841f0036` retains portable assertions and isolates native assertions without a blanket skip -- its five test-file diffs.
2. **Best alternative.** Put the exact fixed identities in one policy table in `bootstrap/tests/security_manifest.py`, applied by existing `conftest.py`; this avoids hundreds of repeated annotations -- existing security-family ownership.
3. **What would show it wrong?** An omitted required identity accepted by the real join would falsify C2; every identity still needs its omission control and native pass in both orders -- plan Verification.

**Verdict:** R1 closed for source reconciliation and the allowed Windows-mode
contract; no remaining classification or Windows-mode barrier identified.
Mapped implementation checks remain due; this does not clear C3 or release.

The fixed candidate now contains **590 distinct IDs: nine Windows and 581
Mac**. All original 584 test-definition syntax trees are unchanged from
`88679232`, retaining the prior 57 plus 64 manual dynamic reconciliations.
The six added Mac IDs are:

- `bootstrap/tests/test_code_map.py::test_real_cli_refuses_fifo`
- `bootstrap/tests/test_security_leaf.py::TestReadRegularBytesRefusesAnythingElse::test_posix_special_files_refused_without_blocking`
- `bootstrap/tests/test_security_leaf.py::TestWriteByReplacing::test_permissions_strip_execute_and_special_bits`
- `bootstrap/tests/test_security_net.py::test_a9_report_directory_and_file_modes_are_private`
- `bootstrap/tests/test_security_finding_confidentiality.py::test_d3_report_file_mode_is_private[clean]`
- `bootstrap/tests/test_security_finding_confidentiality.py::test_d3_report_file_mode_is_private[findings]`

The renamed `test_real_cli_refuses_links` remains portable. Directory refusal,
report containment/exclusive writing and report-only outcomes remain portable;
POSIX modes, device/FIFO assertions and lazy pty imports are retained. Static
reconciliation finds zero missing source names or literal-ID mismatches;
eleven IDs lack protected records and remain explicit source-derived entries.
No host skip supplied an expectation. The temporary candidate is
`/private/tmp/sol-fixed-native-roster-candidate-4855ae28.json`, SHA-256
`13cd64a497f5bd2b0aada8fdfe826032337c8d65039b3aa0763b52d2deff833c`;
its provenance retains the previous inventory and protected-record hashes.
Commit these independently fixed identities before C2 control-flow edits.

Accept the author's native evidence at `70f9f336`: source `4f7337a6`, Windows
Python 3.13.17, six passes in 4.93 s. It demonstrates the authorized complete
Git tree/index contract and leaf/byte controls, not Windows POSIX permission
equivalence or a detached-runner pass. In an isolated committed copy, Python
3.13.13 ran exactly the two changed `TestV1V2Differential` mode nodes with the
previously documented no-collection adapter: **2 passed, 2.01 s**. An initial
mistyped selector exited 4 with no tests; its corrected retry passed. This is
adapter evidence, not real-collector evidence.

**C2 advice:** The single table owns exact host requirements; existing
collection hooks can apply opposite-host skips before fixture setup. The
runner must still refuse unknown platforms, collection skips, absent IDs,
unexpected outcomes and native prerequisite skips, and require every listed
case to pass natively in both orders. This advice authorizes no C2 edit.

**Coverage:** Targeted committed diffs, fixed-ID provenance and source syntax,
accepted native summary and two adapter controls. No broad/native collection,
suite, join, production policy activation, trust or release operation ran.
The recorded mapped implementation selections remain unrun, not waived.
Over target to preserve exact new IDs and distinguish native/adapter evidence.
Elapsed and tokens: unknown.

## C1 completion -- Codex GPT-6 Luna (Low) -- 2026-11-06

**Disposition:** C1 is complete and C2 is cleared. Sol's targeted R1
follow-up at `73aaf88d` independently reviewed the 590-ID fixed source
candidate (nine Windows IDs and 581 POSIX IDs), SHA-256
`13cd64a497f5bd2b0aada8fdfe826032337c8d65039b3aa0763b52d2deff833c`.
The exact policy is committed before any runner control-flow change. Windows
mode handling follows the Maintainer allowance recorded above; no ACL
equivalence is claimed.

**C1 evidence:** The native Windows focused selection at source `4f7337a6`
passed six cases in 4.93 seconds under Python 3.13.17 and Git
2.56.0.windows.4. Root's joined bounded 104-file mapped run at `73aaf88d`
reported 5,664 passed, nine skipped and 18 initial failures in 1,522.087
seconds wall time (1,519.35 seconds pytest). All 18 initial failures passed
their affected targeted corrections: six twin controls at `0922e0e7`, two
clone-anchor nodes after importing the exact local ref, and twelve edit-check
fault parameters plus positive control at `23ded78f` (13 passed at seeds 0
and 1). The fixture repair then passed ordinary review `cb58831e` and Security
review `117e7f39`. Copy-promotion at `41b6a3b5` passed 15 mapped files and
1,073 cases in 50.71 seconds. The source AST names, decorators and native
classification were unchanged.

This closes C1 source reconciliation, Windows path/mode probes and mapped
iteration dispositions. It is not a full suite, certifying pair, release run,
trust operation or C3 review. No such operation was performed for this
checkpoint. C2 implementation checks remain due. Elapsed and tokens: unknown.

## C2 implementation checkpoint -- Codex GPT-6 Luna (Low) -- 2026-11-06

**Delivered:** The fixed source-reviewed native policy remains its own prior
commit, `8059fa3a8ea40496eadb97e7d01fc71586968915`, before the runner changes.
Runner, existing collection hook, actual-seed report selection, strict local
record validation and same-runner join are committed at
`42c72b1f425850e30b8f9361fbbbf7ac55c66c70`. Focused host-metadata test fixes
are `5a27ad153863a47b968c93eeb0adcb0e9643ff9e` and
`6203ef8552f094e27b9c1cb53b915e9d78fefac5`. The release-command references
and measured distinct template count update are `7edadbf9`; the Meter-aware
expected set for the existing scan-oracle mutation is `899f7f44`. No runtime
floor, release trust record or policy was changed by those test/documentation
follow-ups.

**Canonical focused controls:** In a clean copy at
`6203ef8552f094e27b9c1cb53b915e9d78fefac5`, using
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13),
`python -m pytest bootstrap/tests/test_security_check.py
bootstrap/tests/test_quality_gate_order_independence.py
bootstrap/tests/test_broad_run_guard.py
bootstrap/tests/test_quality_gate_cli.py -q` passed **190 tests** with three
upstream `stevedore` deprecation warnings in 40.98 seconds. The copy was clean
before and after. On clean copy `899f7f44c5db2dfeb9af8ad648b915b2a6ca4ddf`,
the Meter-dependent `test_security_lint.py::test_templates_py_count_is_pinned`
and `::test_the_on_disk_oracle_goes_red_when_a_registry_stops_delivering`
passed **2 tests** in 0.08 seconds under the same interpreter. The 33-path
count was measured by listing the full `templates/**/*.py` set at source
`280543e1` in a clean copy; it includes the newly mapped
`templates/skills/_lib/meter.py`.

**Documentation gates:** On clean copy `6203ef8552f094e27b9c1cb53b915e9d78fefac5`,
`claim_check.py` passed for `SECURITY.md`, `docs/release-process.md`,
`bootstrap/PROVENANCE.md` and `docs/methodology/runtime-contract.md`;
`link_check.py` scanned those four documents with no issues; and
`sync_doc_snippets.py --check` found no drift in them. Python 3.13.13
`quality_gate.py --sub neutrality` reported zero failures and 43 informational
findings. No external links were probed.

**Earlier Python 3.12.9 attempts, retained for context:** On commit `42c72b1f`,
the same four focused test files produced 174 passed, 13 failed and three
skipped in 17.22 seconds. The 13 strict-entry controls stopped at the runner's
Python 3.13 floor because the tests had not yet supplied synthetic 3.13 host
metadata. After that test-only correction, commit `5a27ad15` produced 176
passed, 11 failed and three skipped in 16.79 seconds; the fake `sys` object
lacked standard output/error handles. Commit `6203ef85` supplied those handles
and the same set passed on 3.12.9 (187 passed, three skipped in 18.32 seconds).
The canonical 3.13.13 run above is the controlling focused result. Python
3.13.13 was available at the absolute path recorded above; it was not
unavailable.

The first whole-file `test_security_lint.py` attempt on clean commit `7edadbf9`
reported 10 passed and one failed: Meter's new mapping made the existing
mutation fixture's two-file expected set stale. The exact expected set now
includes all three shipped helpers; only the failed mutation node and changed
count pin were rerun after `899f7f44`, and both passed as recorded above.

**Mapped selection still owed:** `python tools/test_tiers.py for` selected these
46 files for the changed C2 paths:

`bootstrap/tests/contract/test_certifying_run_rule.py`,
`bootstrap/tests/contract/test_release_members_contract.py`,
`bootstrap/tests/contract/test_scientific_check_guidance_ships.py`,
`bootstrap/tests/contract/test_verification_boundaries.py`,
`bootstrap/tests/integration/test_link_check_exclusions.py`,
`bootstrap/tests/integration/test_prune_tools.py`,
`bootstrap/tests/integration/test_quality_gate_redundancy.py`,
`bootstrap/tests/test_board_json_contract.py`,
`bootstrap/tests/test_broad_run_guard.py`,
`bootstrap/tests/test_ceremony_review_report.py`,
`bootstrap/tests/test_check_cairn_content.py`,
`bootstrap/tests/test_check_release_publication.py`,
`bootstrap/tests/test_config_module.py`,
`bootstrap/tests/test_core_dev_folders.py`,
`bootstrap/tests/test_default_security_stance.py`,
`bootstrap/tests/test_doc_governance.py`,
`bootstrap/tests/test_documentation_plan_module.py`,
`bootstrap/tests/test_finalize_retired_living_state.py`,
`bootstrap/tests/test_gate_manifest.py`,
`bootstrap/tests/test_hardening.py`,
`bootstrap/tests/test_module_roster.py`,
`bootstrap/tests/test_next_session_local_note.py`,
`bootstrap/tests/test_notice_install.py`,
`bootstrap/tests/test_onboarding_seed_roster.py`,
`bootstrap/tests/test_oracle_activation.py`,
`bootstrap/tests/test_portable_security_sweeps.py`,
`bootstrap/tests/test_presets.py`,
`bootstrap/tests/test_python_floor.py`,
`bootstrap/tests/test_quality_gate_cli.py`,
`bootstrap/tests/test_quality_gate_neutrality.py`,
`bootstrap/tests/test_quality_gate_order_independence.py`,
`bootstrap/tests/test_quickstart_sequence.py`,
`bootstrap/tests/test_reference_scripts.py`,
`bootstrap/tests/test_replacement_tools.py`,
`bootstrap/tests/test_review_stance_in_shipped_files.py`,
`bootstrap/tests/test_scaffold.py`,
`bootstrap/tests/test_scaffold_substrate.py`,
`bootstrap/tests/test_security_check.py`,
`bootstrap/tests/test_security_lint.py`,
`bootstrap/tests/test_security_marker.py`,
`bootstrap/tests/test_upgrade.py`,
`bootstrap/tests/test_upgrade_added_slots.py`,
`bootstrap/tests/test_upgrade_lockfile_path_containment.py`,
`bootstrap/tests/test_upgrade_module_additions.py`,
`bootstrap/tests/test_verify_integrity.py`, and
`bootstrap/tests/test_verify_ref.py`.

Root will batch this mapped selection with the ready scanner/continuation
selection and Meter integration work. It remains **owed**, not waived. The
mapped 46-file run, ordinary and Security code reviews, and final wide Boundary
B remain due; no strict local whole-suite execution, native Windows run, join,
certification, release pass or trust operation is claimed. Plan status remains
`implementing`. Elapsed for this checkpoint and tokens: unknown.

## C1 new Meter native classification -- Codex gpt-6.1-sol (High) -- 2026-11-06

**Role:** source-classification reviewer. First pass on the new Meter test
artifact at `2cea4dfcca4f0160ff2df31459da420654df680e`; not another clearing
pass on the original 590 or Meter's implementation/Security Review.

**Foundations**

1. **Should this happen as framed?** Yes: the new POSIX-private-file tests need exact native expectations, not exemptions inferred from skips -- `bootstrap/tests/integration/test_meter.py` and `tools/meter.py` at the reviewed commit.
2. **Best alternative.** Extend the existing single policy by the source-derived delta; a second inventory or blanket file skip would add burden or lose portable tests -- `bootstrap/tests/security_manifest.py` at `8059fa3a`.
3. **What would show it wrong?** Removing any added identity must fail strict completeness validation; an unsupported-platform refusal must not count as exercising its native assertion -- strict plan C2/Verification and Meter's `_PRIVATE_FS_SUPPORTED` guard.

**Classification:** eleven additional `posix` identities, derived from ten
`POSIX_ONLY` definitions. The sole parameter list is literal `[0o644, 0o640]`;
integer node labels are `[420]` and `[416]`. None overlaps the existing policy.
The resulting policy has **601 identities: nine `nt`, 592 `posix`**.

Exact additions, all in `bootstrap/tests/integration/test_meter.py`:

- `test_config_file_must_be_private[420]`
- `test_config_file_must_be_private[416]`
- `test_config_directory_must_be_private_and_link_free`
- `test_config_rejects_directory_and_fifo_leaves`
- `test_config_refuses_linked_leaf_and_unverifiable_owner`
- `test_private_config_open_revalidates_descriptor_identity`
- `test_safe_reader_rejects_escape_links_nonregular_and_partial_lines`
- `test_safe_reader_rejects_oversized_line`
- `test_safe_reader_open_revalidates_descriptor_identity`
- `test_enabled_cli_stops_before_source_or_ledger_io`
- `test_disabled_cli_does_not_open_configured_sources_or_ledger`

Configuration cases exercise owner/mode, no-follow, FIFO and opened-identity
checks. Reader cases pass the POSIX guard into descriptor-relative traversal
and reads; their size/partial-line assertions would otherwise pass vacuously
on early unsupported-platform refusal. Both CLI cases require private-config
acceptance and POSIX FIFO fixtures to establish their enabled/disabled path.
No marker wrongly removes a supported portable instance of those scenarios.
Byte-schema tests and the default-disabled CLI remain portable and unmarked.

The unmarked
`test_unsupported_privacy_platform_fails_closed_but_missing_config_is_disabled`
forces `_PRIVATE_FS_SUPPORTED=False`: absent configuration returns disabled,
while existing configuration and source reading refuse before POSIX APIs.
That is portable unsupported-platform evidence, not a native exception.

Source file SHA-256:
`c04f02eaedfd1ee5473df81c4c748a50d1354a10303a94710072aaced41cd642`.
Exact full IDs and provenance are retained in
`/private/tmp/sol-meter-native-delta-2cea4dfc.json`, SHA-256
`7e2f37ebc97017386b299ede8dbe861f9e6668b308becb461c63dd3f4d554be0`.
This supports the exact policy-data fold; later name/parameter changes need
reconciliation. No source or policy was edited by this reviewer.

**Coverage:** committed syntax, literal parameter expansion, existing policy
membership and corresponding private-file guards. No test import, collection,
observed skip, execution, private source, native run or trust operation. Meter's
remaining implementation/review obligations and strict verification stay open.
Over target to preserve exact identities and the portable/native distinction.
Elapsed and tokens: unknown.

**Same classification transferred to `6eb9cb1db79fbbdc5d5e0eb9445870ead7bac7a4`.**
All ten marked function names, decorators and parameter syntax are unchanged
from `2cea4dfc`; `_PRIVATE_FS_SUPPORTED = os.name == "posix"` is unchanged.
The test-body correction intercepts the leaf opened with `dir_fd`; it changes
no identity or platform classification. The current test file SHA-256 is
`ad9a77bb58ec793aab979d27283aeb64b1e0041d797dfb02e25a441715c9c8c4`.
The same eleven-ID delta therefore applies. This comparison transfers only
the source classification, not implementation or Security clearance of the
new descriptor-binding code. No collection or execution ran. Elapsed/tokens:
unknown.

## C2 affected A verification -- Codex GPT-6 Luna (Low) -- 2026-11-06

Coordinator evidence for the strict-runner and Meter C2-affected selection:
clean commit `f14169e83110130eb30525330a7d4a990d5cc8d6`, reviewed range
`9184c3ed..f14169e8`, canonical
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13). The 46-file
strict selection recorded above passed **2,466 tests**, with no skips or
failures. The final 601-ID policy from `748882e4` was present in the tested
commit.

The shared 108-file selection ran serially as three 36-file pytest batches
with `-q -rs -p no:cacheprovider --tb=short --durations=20` and JUnit output.
Batch results were 1,661 passed; 2,294 passed and nine skipped; and 2,023
passed. The nine skips were the expected Windows junction and drive-only
cases. The aggregate was **5,978 passed, nine expected skips, zero failures**;
wall time was 1,428.084 seconds. Each batch had clean pre- and post-run state,
and no full-suite or release-mode flag was set. Exact argv, outcomes, logs and
XML are retained in `/private/tmp/cairn-v07-shared-f14169e8-{selection,results,prose}.json`
and the corresponding `b1`/`b2`/`b3` artifacts.

All 36 changed Markdown checks passed: claim checks, link/content checks and
snippet synchronization. Neutrality reported zero failures and 43 information
items; redundancy reported zero failures and two information items. No external
links were probed. The shared run recorded 17 slow test files in the suite
consolidation plan.

This closes the coordinated affected-A selection for C2. It is not final wide
Boundary B for this trust-ceremony plan. Ordinary and Security code reviews,
their fixes if any, and final wide Boundary B remain due. No strict local
whole-suite execution, native Windows run, join, certification, release pass
or trust operation is claimed. Elapsed for this record and tokens: unknown.

## Code review -- Codex gpt-6.1-terra (Medium) -- 2026-11-06

Reviewed implementation at `f14169e83110130eb30525330a7d4a990d5cc8d6`;
verification record at `a0734298`.
**Obligation:** Internal. **Verdict:** REVISE. **Bounding:** WIDER RUN REQUIRED.
**Elapsed:** unknown. **Tokens:** unknown.

**Foundations**

1. **Should this happen as framed?** Yes: C2 requires both orders and a same-SHA join; `security_check.py::_validate_local_record` checks the fixed roster and raw phases, and `_run_join` checks clean HEAD before and after.
2. **Best alternative.** Manual comparison removes the reader but leaves missing native outcomes to manual inspection; the existing runner can enforce the accepted join (proposal Alternatives and plan C2).
3. **What would show it wrong?** A missing native identity or failed child yielding joined PASS would falsify C2; the required per-member and integrated controls below test those paths.

**Blocking 1 -- per-member mutation evidence is missing.** Plan Verification requires listing the roster and mutating each eligible native case in a separate copy, retaining repeatable controls and reporting outcomes. The policy contains 601 identities (`test_fixed_native_policy_is_unique_before_mapping`); `test_join_main_refuses_mutated_native_records` supplies only one `missing-id` case. The C2 and affected-A records do not report per-member mutations. Close by exercising each identity independently through the real join entry point using committed fixtures, retaining the repeatable control and recording counts, results and omissions. This does not require 601 native suite runs.

**Blocking 2 -- integrated entry-point evidence is missing.** Plan Verification requires a committed-fixture run through the real entry point connecting both suite processes, all quality sub-gates, Bandit, `check_cairn`, integrity refusal, external paths, local exit 5 and join-only PASS. `test_main_reports_local_incomplete_and_exit_five` replaces the entire detached runner, while `test_native_context_writes_external_report_for_actual_order` runs a child separately. The C2 record expressly does not claim a strict local whole-suite run or join. Close with the specified connected fixture evidence and recorded results; this is not the final native release ceremony.

**Evidence and coverage:** On a separate archive of `f14169e8`, Python 3.13.13 ran the raw-report refusal, mutated-join and duplicate-key nodes: 19 passed in 0.35 seconds. Read the runner, collection hook, quality-gate launch, tests, C1 allowance, proposal and plan evidence. No full or mapped suite, native Windows execution, per-member mutation, full connected fixture, Security Review or release ceremony was run. Over target to state both unmet accepted checks and their closures.

## Code review response and focused C2 verification -- Codex GPT-6 Luna (Low) -- 2026-11-06

**Response to ordinary review `2fd9e4fd`:** Finding 1 is addressed by
`test_join_refuses_each_native_identity_missing_from_either_order`, whose
parameters enumerate the current committed `NATIVE_ONLY_NODE_IDS` directly.
Each of the 601 identities gets a separate temporary record copy and is
omitted independently from both `default` and `seed-0`; each mutated pair is
refused through `security_check.main(["--join", ...])`. The full source tuple
is the independent expected set. These are in-process record-join checks, not
suite runs. The fixed policy owner and identity are unchanged.

Finding 2 is addressed by
`test_committed_fixture_connects_real_record_and_join_entrypoints`. It builds
a clean committed fixture with the real runner, conftest, scanner, checker,
quality gate and a two-native/one-portable suite. The real `--record` path
refuses a tracked-byte mutation before phases, then runs Bandit, `check_cairn`,
the direct pytest child and the quality-gate seed-0 pytest grandchild. The
quality-gate output shows order-independence, neutrality and redundancy.
Both raw reports and the local record are external to the fixture. Local
success returns 5 and `INCOMPLETE`; the fixture's synthetic counterpart then
passes the real `--join` path. The synthetic record is join-validation data,
not evidence from another native host.

**Focused evidence:** The first clean-copy selection was run from commit
`49b62207bba629f2b84a65b9ba76c8907ad21307` with canonical Python 3.13.13:
`python3.13 -m pytest -q -p no:cacheprovider bootstrap/tests/test_security_check.py::test_join_refuses_each_native_identity_missing_from_either_order bootstrap/tests/test_security_check.py::test_committed_fixture_connects_real_record_and_join_entrypoints`.
It reported 601 passed and one failed in 26.94 seconds. All 601 omission
cases passed in both orders. The fixture's real phases completed; the failure
was the test observer counting the runner scratch directory together with two
nested temporary directories. Commit `fbb3affc` narrowed that observer and
cleared stale full-tree scanner exemptions from the reduced fixture.

On a clean copy of `fbb3affc4674f238ec32784a72d377dee1149f99`, the connected
node then completed all phases but failed because its assertion treated the
quality-gate's expected `seed=0: PASS` as a release PASS. Commit `ee8d4ab6`
limited the assertion to the release-level `security_check: PASS` line. On a
clean copy of `ee8d4ab6b62fa419de025c8085da7b5cb3d74c53`, canonical Python
3.13.13 ran only the connected node: **1 passed** in 12.96 seconds, with
three Bandit dependency deprecation warnings. No production runner code,
policy bytes or allowed roster changed.

**Coverage limits:** The omission matrix used synthetic records and patched
only join pre/postflight; it proves the real join parser refuses each missing
identity and both orders, not native execution. The connected fixture used
three test items, one expected opposite-host skip and a synthetic counterpart.
No full Cairn suite, native Windows run, final release join, certification,
Security Review or final wide Boundary B ran. The focused findings are ready
for targeted ordinary review; Security Review and wide Boundary B remain due.
Elapsed for this record and token use: unknown.

## Targeted code review -- Codex gpt-6.1-terra (Medium) -- 2026-11-06

Reviewed test changes `49b62207`, `fbb3affc` and `ee8d4ab6`, and response
`2675a715`, against findings at `2fd9e4fd`. **Obligation:** Internal targeted
return. **Verdict:** REVISE. **Bounding:** WIDER RUN REQUIRED. **Elapsed:**
unknown. **Tokens:** unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the connected fixture now runs real local phases and the explicit join, and the roster matrix covers all 601 committed identities; both respond to required plan Verification.
2. **Best alternative.** Keep these reusable fixture controls and strengthen their negative cases; manual inspection cannot establish the missing-identity and detached-byte refusals.
3. **What would show it wrong?** A record missing an identity in both orders, or changed bytes in the detached checkout, producing a successful local or joined result would falsify the relevant protections.

**Finding 1 remains blocking.** The per-identity test removes a node from only one order at a time. `_validate_local_record` also requires both collection sets to match, so an order mismatch can refuse every case even if fixed-roster enforcement is absent. For each identity, also omit it consistently from both orders of both host records, preserving matching collection and outcome sets, and require the fixed-roster missing-ID diagnostic through the real join. Include a valid-record positive control and a negative control showing this case fails if the roster requirement is disabled. Retain and report the separate-copy results. The recorded 601 passes do not establish that isolated property.

**Finding 2 remains blocking in part.** The connected fixture now shows the real phase chain, external records, local exit 5 and a synthetic-counterpart join. Its dirty-byte case changes the *operator* checkout before preflight; it does not change bytes in the detached checkout to test the required byte-integrity refusal. `test_nested_committed_leaf_is_verified_and_mutations_refuse` tests the verifier directly, not the entry point. Exercise detached-byte mutation through the committed-fixture record entry point and record the refusal; no full release ceremony is implied.

**Coverage:** Read the committed test delta, fixture construction, runner validation and recorded clean-copy results. No tests were rerun in this targeted return; no native execution, full suite, Security Review or final Boundary B was performed. The later architecture native-ID classification was not reviewed here.

## Response to targeted review and focused controls -- Codex GPT-6 Luna (Low) -- 2026-11-06

**Response to Terra review `ca0f4b3f`:** Finding 1 is addressed by
`test_join_refuses_each_native_identity_missing_from_all_host_orders`.
For every source-enumerated identity in the current 601-row policy, the test
removes that same ID from both order reports in both host records, from both
collection and outcome rows. It asserts all four remaining ID sets are equal
and requires the exact `local record omits fixed native IDs` diagnostic from
the real `security_check.main(["--join", ...])` entry point. No ordering or
counterpart-set mismatch can cause the refusal. The existing complete-record
positive control remains, and
`test_missing_native_roster_control_is_specific` additionally demonstrates
that a valid pair joins, the identical omission refuses under the fixed
roster, and it passes when the test temporarily disables the fixed-roster
maps and makes all remaining outcomes PASS.

Finding 2 is addressed by extending the committed connected fixture. After
the runner materializes and byte-verifies its detached checkout, a test
observer changes a tracked fixture byte immediately before the real bound
child launch and delegates to the real subprocess. The child refuses its
dirty checkout and the parent then refuses the blob mismatch; no local record
is created. The same fixture subsequently runs the positive local path through
Bandit, `check_cairn`, direct pytest and the quality-gate seed-0 grandchild,
including order-independence, neutrality and redundancy. It verifies external
reports, local exit 5/`INCOMPLETE`, and a synthetic-counterpart real join.
The counterpart remains plumbing evidence, not another native-host run.

**Focused evidence on the then-current 601-row roster:** Clean commit
`b0d602581a6394740b2bf3941787a75ca7a27b24`, canonical Python 3.13.13, ran:
`python3.13 -m pytest -q -p no:cacheprovider bootstrap/tests/test_security_check.py::test_join_refuses_each_native_identity_missing_from_all_host_orders bootstrap/tests/test_security_check.py::test_missing_native_roster_control_is_specific bootstrap/tests/test_security_check.py::test_join_main_accepts_one_complete_native_record_per_host bootstrap/tests/test_security_check.py::test_committed_fixture_connects_real_record_and_join_entrypoints`.
Result: **603 passed, one failed** in 25.57 seconds. All 601 per-ID
four-record/two-order omissions refused with the exact roster diagnostic;
the valid-record and connected fixture controls passed, including detached
byte mutation. The sole failure was the counterfactual test control: it
emptied the required set but left the paired lookup map populated, so the
validator indexed the intentionally omitted ID. Commit
`e510418f1010452ae8caeb901d899b6565be9bbb` emptied all three fixed-roster
representations only within that negative control. On its clean copy,
canonical Python 3.13.13 ran only that changed node: **1 passed** in 0.25
seconds, with three Bandit dependency deprecation warnings.

**Roster reconciliation remains pending:** the current test source derives
its per-ID cases from the committed policy tuple; the 601 cases above do not
cover the four newly classified Windows IDs. Root is coordinating their
source-reviewed policy fold and Suite C3 moved-file integration, including
the relevant collection count. Rerun the derived matrix against that final
policy before review closure; do not treat the four IDs as tested yet.
No full Cairn suite, native Windows suite, final release join, certification,
Security Review or final wide Boundary B ran. Elapsed for this record and
token use: unknown.


## C1 code-map native classification -- Codex gpt-6.1-sol (High) -- 2026-11-06

**Role:** source-classification reviewer; first pass on new architecture C1
source `cb612e34`, transferred to corrected committed test source
`b59d37281c90fc9b125c784988828f0709264bdf`. This is not product Code or
Security clearance.

**Foundations**

1. **Should this happen as framed?** Yes: four new tests require actual Windows APIs and must enter fixed expectations -- `bootstrap/tests/test_code_map.py`, `_WindowsAPI` and `_scan_worker` at the reviewed source.
2. **Best alternative.** Extend the existing policy once while preserving shared assertions on both backends; runtime skips or another ledger would conceal missing coverage -- `bootstrap/tests/security_manifest.py` and strict C1/C2.
3. **What would show it wrong?** A missing native ID accepted by the real join, or a shared budget test stopping before its assertion on Windows, would falsify completeness; retain per-ID omission controls and both-host execution -- strict Verification and the corrected `walk_root` test helper.

**Classification:** add exactly **four `nt` IDs**; the complete changed-file
native set is four `nt` and four `posix`. No identity is renamed or
parameterized. The policy becomes **605 IDs: 13 `nt`, 592 `posix`**.
Windows additions exercise successful CLI traversal/non-execution, per-source
budget, Job-child termination and reparse entry/root/held-parent refusal.
The existing FIFO, linked-root, race and interrupted-read controls remain
explicitly POSIX-scoped; Windows root-junction refusal is separately retained.

The eight shared symbol/budget/deadline cases initially called a POSIX-only
root opener. `b59d3728` routes them through the settled host filesystem
adapter, retaining their assertions rather than adding exemptions. Its Job
runner namespace and portable DEL filename repairs change no identities.
The malformed-buffer decoder remains portable: its pure `struct`/UTF-16 path
never constructs `_WindowsAPI`.

Exact additions and eight future move pairs are in temporary
`/private/tmp/sol-code-map-native-delta-b59d3728.json`, SHA-256
`ad4099c458000a49e99faa88fec1d8e0aece755eaa6e590f0d698665f24ca9c5`.
Test-source SHA-256:
`45312823651e10a5fe8b87abc8870071802667d00d8885556f9803746a2f07aa`.
Before the move, the folded canonical policy identity is
`sha256:8dc8a4c53bd0bdb135c4b034620b948896a8a947195025bb40056605853a0d08`.
The configured tier is `security`; moving the file there changes all eight
native path prefixes and requires reconciliation, without changing suffixes.
No policy or product was edited by this reviewer.

**Coverage:** committed source, guards, transitive helpers and literal
parameters; real project collection of this one file on a separate archive:
Python 3.13.13, 35 IDs in 0.05 seconds, with one portable decoder pass in
0.11 seconds. No host skips defined expectations. Not covered: Windows
execution, full-file behavior, product Code/Security reviews, mutation/join,
suite, certification or trust operations. Over target to preserve exact
identity provenance and the repaired portable/native distinction.
Record gates passed: claim, content/link, scoped snippet and neutrality;
one external link was not probed. The initial default snippet command could
not enumerate a Git-less archive; its explicit-file retry passed.
**Elapsed:** unknown. **Tokens:** unknown.

## Targeted proof review -- Codex gpt-6.1-terra (Medium) -- 2026-11-06

Reviewed `b0d60258`, `e510418f`, the policy fold `064fdc9f`, and response
`f15d829d`, against the remaining findings at `ca0f4b3f`. **Obligation:**
Internal targeted return. **Verdict:** REVISE pending the current-policy matrix.
**Bounding:** WIDER RUN REQUIRED. **Elapsed:** unknown. **Tokens:** unknown.

**Foundations**

1. **Should this happen as framed?** Yes: matched omissions now isolate the fixed roster, and the connected fixture changes detached bytes before the real child launch (`test_security_check.py`).
2. **Best alternative.** Retain these controls and run the source-derived current matrix; sampling cannot establish the plan's per-member check.
3. **What would show it wrong?** An omitted current identity accepted by the real join, or changed detached bytes producing a local record, would falsify the controls.

**Finding 1:** The control design now removes each identity from both orders of both host records, requires the missing-roster diagnostic, and includes a positive pair and a roster-disabled counterfactual. The recorded 601-case run predates 16 path moves and four additions in `064fdc9f`; those 601 results are not a measured 605-case run. The author response requires the final-policy matrix before review closure. Run and record all 605 current identities; final wide Boundary B is scheduled to include them. This check remains open, not waived.

**Finding 2 is closed.** The connected fixture changes a tracked byte after detached materialization, invokes the real child, and asserts both child dirty-tree and parent blob-mismatch refusals, with no record created. The same clean-copy run recorded the positive connected fixture passing (`f15d829d`: 603 passed, one separate counterfactual failure later corrected at `e510418f`).

**Coverage:** Read committed control and policy diffs and the recorded focused results. No tests were rerun in this targeted return. No native Windows suite, Security Review, final wide Boundary B, certification or release ceremony was performed.

**Claim check:** Five hard unresolved historical paths follow the `064fdc9f` test moves. The same five appear on the unchanged committed `eb5ee11a` archive; this review adds none. They remain for the moving workstream to resolve.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-06 -- current 605-member roster proof

On a clean detached copy of `064fdc9f`, Python
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13) ran exactly
`test_join_refuses_each_native_identity_missing_from_all_host_orders` and
`test_missing_native_roster_control_is_specific` from
`bootstrap/tests/test_security_check.py`, with bytecode and pytest cache
writes disabled and `CAIRN_FULL_SUITE` and `PYTEST_ADDOPTS` unset. Result:
**606 passed, zero skipped** in 7.09 seconds pytest and 8.28 seconds wall;
three upstream `verify_requirements` deprecation warnings. The detached copy
remained clean. The parametrization exercised every current policy identity:
605 omissions, including all four code-map additions and all 16 moved
identities, plus the roster-disabled negative control.

The committed policy has 605 unique IDs (13 `nt`, 592 `posix`) and canonical
identity `sha256:25572c7fb58892ff5fe233c2e30e1c7dea4a06b2f3da564b14e45666616e28a3`.
At `064fdc9f`, `bootstrap/tests/security_manifest.py` SHA-256 is
`b6bf3603ce689156f60264a8c5a3eca84007c9be4a9d32694b0157bf473e9752` and
`bootstrap/tests/test_security_check.py` SHA-256 is
`a8eb6be9bc6fde8d7ed48d03007e7ebfe44989e1579e52758f039f04ddf4da2e`.
This is the current-policy run required by Targeted proof review Finding 1;
it closes that finding's stated matrix condition. It does not claim native
Windows execution, full-suite certification, Security Review or final wide
Boundary B. **Elapsed:** 8.28 seconds. **Tokens:** unknown.
