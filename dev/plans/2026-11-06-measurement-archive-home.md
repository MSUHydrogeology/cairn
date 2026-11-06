# Plan: A home for closed measurement records

**Source proposal**: dev/proposals/archive/2026-11-06-codex-measurement-archive-home.md
**Author**: Codex GPT-6.1 Terra (Medium)
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-06
**In brief**: Put proven closed measurement records in an archive and deliver that home safely to adopters who select incident trackers.

## Source proposal

The Maintainer accepted the heavy proposal on 2026-11-06. It retains live
trackers and readers while giving closed records and selected adopters a
tracked archive home; the old strategy list is only a set of candidates.

## Scope

Establish current closure, owner and reader evidence for each candidate before
moving it. Move only proven closed records, preserve their bytes, repair current
references and consumers, and leave uncertain records in place with reasons.
Preserve active ledger append paths and historical references. Deliver a tracked
home for selected fresh installations, explicit module adoption and upgrades
of already-selected modules; preserve unselected behavior, existing content,
idempotence and guarded refusal of unsafe links. Update measurement and module
guidance, and affected install contract, fidelity and manifest surfaces.

**Reuse.** Searches for `incident-trackers`, `_DEV_DIRS`, `install_file` and
module-internal additions found the existing mapping in
`bootstrap/_scaffold/config.py`, guarded tree creation in `install.py` and
upgrade addition handling in `upgrade.py`. Prefer these existing mechanisms;
do not add installer logic if they meet both install paths and selection.

### Documentation / doctrine surface

`dev/measurement/README.md` and the incident-trackers module describe the
live/archive boundary and selected delivery. Software description stays in
existing documentation; no new governing doctrine is proposed.

## Sequence

The existing module mapping, guarded installer and upgrade paths are available
now; no unfinished plan is a prerequisite. Estimate 1–2 workdays including
reviews and verification; closure research, guarded upgrade behavior and
security findings may extend this. A release baseline operation, if needed,
is a separate Maintainer-owned wait, not a plan completion gate.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Map candidates, ownership, readers and installation consumers; classify and move closed records | Usual and Security plan reviews | Preserved history, repaired current references and concise closure evidence |
| C2 | Deliver and explain the selected archive home using guarded existing paths | C1 | Fresh, adoption and upgrade delivery with preservation and refusal evidence |
| C3 | Review and verify the complete change | C1–C2; usual and Security code reviews | Final wide Boundary B and recorded dispositions |

## Acceptance criteria

**C1.** Each moved record has evidence of closure and current owners/readers;
current consumers resolve and live trackers and append destinations remain
usable. Historical record bytes remain unchanged. Uncertain candidates stay
in place with a reason; the old list alone is not proof of closure.

**C2.** Real selected fresh install, explicit adoption and upgrade of an
already-selected module provide a tracked archive home. Unselected paths do
not introduce module content. Repeated runs preserve existing adopter files;
unsafe linked destinations refuse before writes. Module guidance accurately
states selection behavior and the live/archive boundary. Summary, dry-run and
manifest paths agree with the delivered mapping.

**C3.** Both code review obligations and all mapped checks pass. Any expected
engine AST mismatch from reviewed changes is recorded as unpassed pending the
separate release baseline operation; unexpected drift or unexplained integrity
failure remains implementation work.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: map candidate readers, writers, installer and manifest consumers;
run `python tools/test_tiers.py for <changed paths>` and its selected tests,
including the applicable incident-trackers and upgrade-module-addition tests.
Exercise real install and upgrade entry points for selected, unselected,
repeated, existing-file and linked-destination cases, and live record readers
and writers. Extend owning tests only for uncovered faults. Run applicable
claim, link, snippet and neutrality prose gates and required security checks.
Follow the AST and re-anchor runbooks when applicable; no release operation is
authorized by this plan.

Boundary C: an independent reviewer runs tight falsification checks; a separate
Security Review is also required. Boundary B: after review, run wide on the
clean final commit with canonical Python 3.13.x, the mapped iteration and
integration/workflow checks, public install/upgrade paths, standing gates and
plan-specific cases. Record tested SHA/range, interpreter, clean pre/post
state, commands, counts, timing, non-pass dispositions and omissions. Tree
certification remains a separate authorized ceremony.

## Plan review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

**Reviewed commit**: `aac2fcf9417571e30a18e1f9e951a81f05da2faa`
**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: PROCEED
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes. C1 requires closure and reader evidence before each move, and C2 covers all three selected delivery paths, preservation and refusal; C3 retains both reviews and wide final verification. The 1–2 day estimate is plausible but uncertain because closure research and security findings remain unmeasured. -- Plan Scope, Sequence, Acceptance criteria and Verification; accepted proposal Decision.
2. **Best alternative.** A tracked module file using the existing guarded mapping is the simplest identified route that retains the selected install and upgrade outcomes; the plan already prefers it if sufficient. An unconditional directory or local-only home would lose selection or adopter delivery. -- `bootstrap/_scaffold/config.py` incident-trackers mapping, `bootstrap/_scaffold/install.py` `_DEV_DIRS`, and `bootstrap/_scaffold/upgrade.py` module-internal additions.
3. **What would show it wrong?** A moved record still needed for append or read, missing home on any selected path, content introduced unselected, changed existing file on repeat, or a write through a linked destination would falsify the plan; exercise the real install and upgrade paths and live readers in the specified cases. -- Plan C1–C2 and Boundary A; `dev/measurement/attestation-replay-failures.md`.

**Coverage**: Read the committed plan and accepted proposal, template, review sweep, module mapping, directory and upgrade-addition references, and live ledger evidence. Did not establish each record's closure or run installs, tests or security checks; a separate Internal Security Review remains required.

## Plan review -- Codex GPT-6.1 Sol (High) -- 2026-11-06

**Reviewed commit**: `bfdffc0212afe1e138ae04d368b3c7a6eb73b4d5`
**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: PROCEED
**Elapsed**: approximately 5 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes. C1 makes closure and current owner/reader evidence prerequisites to movement, preserving history and active append destinations. C2 covers selected fresh installation, explicit adoption and already-selected upgrades without granting target paths more authority. C3 keeps both code reviews, required checks and unresolved integrity failures in implementation. -- Plan C1–C3; accepted source Decision; `dev/measurement/attestation-replay-failures.md` still arms recurrence rather than documenting a closed ledger.
2. **Best alternative.** Prefer a tracked file in the existing incident-trackers mapping, provided the implementation demonstrates every selected delivery path. This preserves the accepted outcome with fewer branches than new directory logic. `_DEV_DIRS` is unconditional; upgrade already enumerates module-internal additions and blocks occupied destinations rather than silently replacing them. A local directory alone loses adopter delivery. -- `bootstrap/_scaffold/config.py:1061`, `bootstrap/_scaffold/install.py:159`, `bootstrap/_scaffold/upgrade.py:997`.
3. **What would show it wrong?** Through real install, adoption and upgrade entry points, try unselected modules, existing content, repeat runs and linked destinations; any unintended content, overwrite or escaped write falsifies C2. For every proposed move, exercise current readers and appenders and compare historical bytes; a broken active ledger falsifies C1. Summary, dry-run and manifest disagreement also fails delivery. -- Plan Acceptance criteria and Verification; `bootstrap/tests/test_incident_trackers_module.py` omission path; `bootstrap/tests/test_upgrade_module_additions.py` occupied-destination and post-stage symlink controls.

**Coverage**: Examined committed scope, Decision, template, live-ledger purpose, selected mappings, directory creation and upgrade collision/refusal design. Closure classification and safety are planned requirements, not measured results here. Did not establish each candidate's closure, execute installation or tests, inspect adopter state, or perform a release/baseline operation; code and security verification remain due.

## Plan review response -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

Both Internal and Internal Security Reviews proceed with no findings. Their
coverage limits remain implementation work: establish each candidate's closure
and reader evidence, exercise guarded installation and upgrade paths, and
complete both code reviews and wide final verification. No scope or operative
plan change is needed.

**Elapsed**: approximately 1 minute. **Tokens**: unknown.

## Implementation verification -- Codex GPT-6 Luna (Low) -- 2026-11-06

**Source commits**: `6af18b6a`, `ceea7d4c`; source reviewed at `ceea7d4c`.
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python
3.13.13). **Elapsed**: approximately 15 minutes. **Tokens**: unknown.

**C1 closure and consumers.** Moved only `tag-pass-dispositions.md`, unchanged
at 45,899 bytes (SHA-256
`b477ae32e56bf81c4a21f528d5226b42c67f182e56c189e9ac065108d1ceacd2`). The
archived `comprehension-outlives-the-artifact` plan says no planned check was
deferred; the ledger's final corpus says every remaining occurrence is an
accounted-for keep. Its only non-archive reference is a dated ceremony report;
that historical citation remains unchanged. Kept `queued-issue-drafts.md`
because four drafts remain unfiled and one has a live revival condition; kept
`attestation-replay-failures.md`, `gitleaks-version-support.md`, and
`pip-audit-closure-ratio.md` because they still arm recurrence or feed named
tests (`test_portable_security_sweeps.py`, `test_security_stack.py`). The
review-floor and maintainer-view ledgers remain active. The ignored suite cost
files are local state, not tracked candidates. The negative path search was
checked against the known-positive gitleaks test reader.

**C2 and iteration evidence.** Added the empty marker through the existing
`incident-trackers` mapping. On a clean copy, the two plan-named owner suites
collected 125 tests: 123 passed; two new assertions initially mismatched the
existing dry-run output and direct `ScaffoldSecurityError` refusal contract.
The test-only fix is `ceea7d4c`; rerunning only those two nodes passed (2/2 in
0.17s). The other 123 passed in 24.70s and exercised fresh selected install,
unselected omission, repeat preservation, explicit adoption and already-
selected upgrade. `install_manifest` and dry-run selection are asserted. The
selected 69-file tier list (5,481 cases) was rejected before execution by the
runner's 40-file invocation cap; no tests ran in that attempt. Those mapped
checks remain due for final wide Boundary B in batches after both code reviews.

Claim, link and `check_cairn` prose checks passed for the README and module
guidance; `quality_gate.py --sub neutrality` reported 0 failures and 43
informational findings. No full suite, AST baseline update, re-anchor or release
operation ran. Code review and final Boundary B remain due.

## Iteration follow-up -- Codex GPT-6 Luna (Low) -- 2026-11-06

**Source commits**: `6af18b6a`, `ceea7d4c`, `2309df13`.
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python
3.13.13). **Elapsed**: approximately 27 minutes for the 69-file iteration
batches and targeted retries. **Tokens**: unknown.

The 69-file `test_tiers.py for` selection was rejected before running at the
40-file invocation cap. I then ran the two plan-named owner files, followed by
the remaining 67 mapped files in 34- and 33-file batches; no full-suite flag
was set. The owner run collected 125 tests (123 passed, two expectation
failures); the test-only adjustment at `ceea7d4c` corrected the dry-run output
and direct refusal expectations, and those two nodes passed on retry. Batch 1
collected 1,707 cases (1,686 passed, 19 skipped, two failed in 319.60s). Both
failures came from the fresh copy missing `refs/cairn/gate-anchor`; its signed
commit `977b5250` was verified with fingerprint
`SHA256:8R549gtP0SJPaCWlQlausCtAbRBquXCIhbM6395ESsM`, fetched from the local
trusted checkout after public DNS was unavailable, then the two affected nodes
passed (2/2, 1.37s). Batch 2 collected 3,649 tests (3,647 passed, two failed in
1,239.68s). The failures were the `index-non-zero exit` and `index-hang`
parameters in `test_a_failure_in_a_later_group_is_cannot_tell`; neither reached
the stand-in (empty call log and no counter). The default-order four-node
neighborhood used no shuffle seed (conftest default is collection order) and
passed in 2.94s. Commit `2309df13` gives only this test's Git
timeout budget 2s while its fake hang remains 5s; all six later-group
parameters then passed in 6.10s. Their refusal, second-group counter and
version-order assertions remain unchanged. The first failed results remain
part of this record.

The correction changes a protected test file. Its recorded roster hash is
`fd272a9b924f82d48dd9d747bc43e34526d9982396f33d884531ff4ff494dc84`; the
committed file hash is `f57c1671efce33a09909c9ebbf7b23de546888f9d2d404e3a454bd4ad29d7c4b`
(54,300 bytes). This is the exact change at `2309df13`, not unexplained drift.
No roster, gate manifest or AST baseline was edited, and `test_gate_manifest`
was not run after this correction; protected-file integrity remains unpassed
for the ordinary and Security code reviewers to assess. No separate baseline,
re-anchor or release operation was performed. The initial refusal, anchor
retries, batch failures, neighborhood and six-node outcomes are retained as
distinct evidence; no claim of a clean Boundary B is made. The final wide
Boundary B remains due after both reviews.

Per-file durations were not collected for the 34- and 33-file batches. The
visible delays were concentrated in `test_repin.py` and
`test_repin_ceremony.py`, but their individual times were not measured; record
that uncertainty for the final wide run rather than inventing per-file values.

## Code review -- Codex GPT-6.1 Terra (Medium) -- 2026-11-06

**Reviewed commit**: `8dca92cf` (implementation through `2309df13`).
**Obligation**: Internal. **Tier**: Internal.
**Verdict**: REVISE -- one blocking evidence finding.
**Bounding**: Mapped checks include the required integrity check; it remains
unpassed. **Elapsed**: approximately 5 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** The selected-module mapping reuses the
   guarded installer, and the moved ledger is byte-identical; adoption, linked
   parent refusal and selected upgrade passed three targeted tests on the
   committed copy. The integrity evidence needs correction before completion.
   -- `config.py`, `6af18b6a`, Boundary C below and finding.
2. **Best alternative.** Retain the mapped marker and existing guarded paths;
   an unconditional directory loses selection, while a local-only archive
   loses adopter delivery. -- `config.py` incident-trackers mapping and C2.
3. **What would show it wrong?** A selected upgrade lacking the marker, a
   linked parent accepting a write, or a changed archived ledger falsifies the
   outcome. Repeat these and unselected/repeated cases in final wide Boundary B;
   the targeted checks below passed, not the whole delivery matrix. -- C1–C3.

**Finding (blocking -- C3 required check and evidence).** The follow-up says
protected-file integrity was not run after `2309df13`; it is unpassed, not an
observed failed run. Its attribution is incomplete: the trusted gate manifest
pins `test_upgrade_edit_check_runs_no_project_programs.py` at `ae1477af...`,
while the parent of `2309df13` hashes to `761a0f29...` and the reviewed file
to `f57c1671...`. Three earlier commits touched it since the anchor; the
recorded `fd272a9b...` is the roster's file digest, not the manifest's
frozen-file hash. Establish the full provenance and actual required-check disposition;
resolve any unexplained integrity failure under the governing process. An
explanation alone is not a passed check. No baseline operation is authorized
by this review. -- trusted `refs/cairn/gate-anchor` manifest, committed file
hashes, and iteration follow-up.

**Boundary C**: On a separate copy of `8dca92cf`, canonical Python 3.13.13 ran
`test_explicit_adoption_delivers_archive_home`,
`test_linked_archive_parent_refuses_without_escaping`, and
`test_selected_incident_tracker_archive_is_added_on_upgrade`: 3 passed in
0.71s. Historical and archived ledger SHA-256 values matched
`b477ae32...`. No author suite was replayed.

**Coverage**: Read the accepted proposal, plan, implementation and test diffs,
trusted manifest and author evidence. Did not run the integrity check, the
full delivery matrix, final Boundary B, or release ceremonies; separate
Security code review remains required. The finding and evidence require the
extra words above the review target.

## Code review -- Codex GPT-6.1 Sol (High) -- 2026-11-06

**Reviewed commit**: `bb5e2057e337c6551a0c3bfac767e3defbcf89c0`
(implementation through `2309df13`).
**Obligation**: Internal Security Review. **Tier**: Internal Security Review.
**Elapsed**: approximately 12 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes. The selected marker reuses guarded
   installation without new execution authority; historical ledger bytes are
   preserved. The protected-test timeout change retains the second-group counter,
   refusal and version-order assertions, with a 5s fake hang above its 2s bound.
   -- `6af18b6a`, `2309df13`, author evidence and Boundary C below.
2. **Best alternative.** Retain the existing mapping and guards; a new directory
   branch adds maintenance, and a local-only home loses adopter delivery.
   -- `config.py` incident-trackers mapping and C2.
3. **What would show it wrong?** An escaped write, overwritten adopter content,
   or an injected later-group failure that fails to reach the second group
   falsifies safety. Repeat the selected/unselected install and upgrade matrix
   in final Boundary B. -- C2 and the two targeted tests below.

**Verdict**: PROCEED; no blocking security finding.
**Bounding**: ACCEPTED -- existing guards and mapped checks cover the changed
surface; final wide Boundary B remains due.

**Integrity distinction.** P `977b5250` explicitly protects the timeout-test
path. Its manifest pins `ae1477af...`; commits `72194fea`, `23ded78f`, and
`997e1424` produce successive hashes `41f9da1f...`, `5088bfb3...`, and
`761a0f29...`; `2309df13` produces `f57c1671...`. The roster's `fd272a9b...`
is historical metadata, not the manifest pin. This accounts for the whole
file delta; it does not pass integrity or make the protected edit a cheap defect.

`REANCHOR_RUNBOOK.md` “Run the maintained verifier and ceremony” and “Prior
verifier preparation” place actual P verification behind key-away confirmation
in the separate release operation. No ordinary-plan trigger was found in
SAFETY, the runner, security/quality gates or accepted text; the runbook's
`repin verify-candidate` is the positive control. `test_gate_manifest.py`
instead builds fresh `produced()` manifests. Its mapped contract checks remain
due; actual P verification is unperformed and unpassed, without an observed
failed run or a waiver.

**Boundary C**: On a separate committed copy, canonical Python 3.13.13 ran
`test_a_failure_in_a_later_group_is_cannot_tell[index-hang]` and
`test_repeat_install_preserves_adopter_archive_content`: 2 passed in 2.68s.
The initial extraction used the wrong directory and ran no tests; corrected
extraction supplied this result.

**Coverage**: Read committed source, accepted scope, safeguards, provenance and
check triggers. Did not replay author suites, run live P verification, final
Boundary B or ceremonies. Trigger/provenance precision requires exceeding the
review word target.

## Code review response -- Codex GPT-6 Luna (Low) -- 2026-11-06

**Ordinary review finding (bb5e2057):** The earlier iteration record's
attribution was misleading. `fd272a9b` is the historical roster digest, not
the live manifest pin. The signed anchor `ae1477af` pins the protected test
path; changes `72194fea`, `23ded78f` and `997e1424` produce the successive
file hashes ending at `761a0f29` before `2309df13`; `2309df13` produces
`f57c1671`. This accounts for the candidate bytes without claiming that the
live verifier passed.

No live verifier run or failure occurred. The Security Review's trigger
inspection found actual P verification in `REANCHOR_RUNBOOK.md`'s maintained
key-away release ceremony, not an ordinary plan check. It found no standing
ordinary-plan trigger in `SAFETY.md`, the runner, security or quality gates,
or accepted text; `repin verify-candidate` is the positive control. The live
operation remains unperformed and unpassed under PLANNING item 12. No waiver
or baseline action is claimed.

**Disposition:** Treat the integrity attribution as corrected evidence, not
as a passing live check. C3 still requires the mapped `test_gate_manifest.py`
contract coverage and other mapped behavior checks in final wide Boundary B;
none is waived. Security Review `41c873d0` found no blocker and confirms this
separation. Final wide Boundary B remains due; the plan is not ready to
archive.

**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

## Verification addendum -- Codex GPT-6 Luna (Low) -- 2026-11-06

Manifest comparison on clean commit copies (`6af18b6a^` and `1ee50a7f`)
confirmed 91 versus 92 rows; the only added row is the selected archive marker
from `modules/default-on/measurement-archive/.gitkeep` to the matching
destination under `dev/measurement/archive/`. Updated only the literal
expected count in `bootstrap/tests/test_notice_install.py` at `3d543b3b`. The
active signed anchor `977b5250` lists this file in its protected roster, so a
targeted second Security source review is due; no roster, manifest, baseline
or product bytes changed. On a clean committed copy of
`3d543b3bedb55397d2571aefcafb4db0c01da149`, canonical Python 3.13.13 ran
`test_notice_appears_in_manifest_data_row_count`: 1 passed in 0.07s. No other
tests ran; the mapped 69-file Boundary B remains due and was not repeated.
Elapsed approximately 5 minutes; tokens unknown.

## Code review -- Codex GPT-6.1 Sol (High) -- 2026-11-06

**Reviewed commit**: `3d543b3bedb55397d2571aefcafb4db0c01da149`;
evidence `54ab12f5`. Second Security pass, limited to the new protected count
assertion; not a clearing review of earlier findings.
**Obligation**: Internal Security Review. **Tier**: Internal Security Review.
**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes. The only source delta changes the
   literal expected manifest count and diagnostic from 91 to 92. The accepted
   archive mapping adds exactly one marker row; the literal assertion and
   three existing named-row uniqueness checks remain independent expectations.
   -- `3d543b3b`, `6af18b6a` mapping and `54ab12f5` manifest comparison.
2. **Best alternative.** Keep this explicit count correction; deriving the
   expectation from the current manifest would lose the independent contract,
   while leaving 91 would reject the accepted marker. No broader test or
   production change is needed. -- `test_notice_appears_in_manifest_data_row_count`.
3. **What would show it wrong?** An additional or removed manifest row beyond
   the marker would invalidate this correction. The author compared clean
   pre/post manifests and found one addition, no removals, then the named node
   passed 1/1 in 0.07s under Python 3.13.13; final wide Boundary B must include
   this consumer. -- `54ab12f5` and plan C2–C3.

**Verdict**: PROCEED; no new security finding.
**Bounding**: ACCEPTED -- the new delta is confined to this count contract.

**Coverage**: Read the committed delta, surrounding assertions, protected
membership at signed P `977b5250`, mapping attribution, prior reviews and
response. No tests replayed. Final wide Boundary B remains due; live P
verification remains unperformed and unpassed in the separate release
ceremony under PLANNING item 12. No baseline, roster or trust operation was
performed or authorized. Earlier dispositions remain intact; no third or
clearing pass is requested.

## Decision -- retain historical ledger bytes -- Codex GPT-6.1 Sol (High) -- 2026-11-06

**Role**: delegated Strategy; not a Security Review.
**Elapsed**: approximately 5 minutes. **Tokens**: unknown.
**Authority**: Maintainer -- chat, 2026-11-06, relayed by the coordinating agent:

> "I specifically authorize you to use a Sol agent to make decisions in my stead until I return (excepting anything that cannot be undone easily). Keep track of these decisions for review. Let the other agent know to ask you if they need it, and you will spawn the Sol review and track its outcome."

**DECIDED -- preserve C1 unchanged.** Keep the archived ledger byte-identical.
Its blob `0309fbd2debcbeab7c4845bc257a34c6c576c626` matches the original at
`6af18b6a^` and archive at `ec22ee0d`; its opening comment explicitly identifies
a dated historical record. The current source-plan pointer is
[comprehension-outlives-the-artifact](archive/comprehension-outlives-the-artifact.md).

**Options and costs.** Preserving bytes needs no ledger edit, new test or
maintenance mechanism; it retains C1 but loses direct navigation from the
ledger's now-broken relative link. Repairing that one link would restore
navigation without changing measurement entries, but relaxes the accepted
byte-preservation criterion and adds an edit, targeted original-reviewer look
and affected verification. Neither option adds a human trust/release operation.

**Recommendation and reason.** Preserve history: the explicit accepted
criterion and existing archive policy support the least involved option, and
no current consumer requiring that internal link was identified. The committed
ledger-name search found no test reader; the incident-trackers test supplied
the known-positive search control. **Scope delta**: preserved; no concession.

**Probe limits.** The forced explicit-path probe at `ec22ee0d` reported one
broken link and 13 `check_cairn` findings, including 12 older historical
citations; those non-passes remain reported in
`/private/tmp/cairn-artifact-ec22ee0d-checks.json`. `link_check.py`'s
`filter_sources` and `main` exclude archives from default scans and bypass the
exclusion for explicit file arguments. These probes do not establish a failed
standing archive gate. No historical citations will be rewritten and no
allowlist or live-reference file is added.

All actual required wide Boundary B checks remain required on the frozen
source; record their actual commit, counts and failures without claiming a fresh
89-file run on later record commits. This disposition changes no implementation
input and grants no schedule exception, check waiver, additional Security pass,
private operation, baseline/pin ceremony, certification, release or publication.
The coordinating agent will index this local Decision on the existing board.
