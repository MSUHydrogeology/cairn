# Plan: Fast goodnight testing

**Source proposal**: dev/proposals/archive/2026-11-05-codex-fast-goodnight-testing.md
**Author**: Codex GPT-5 (Medium)
**Status**: ready-to-archive
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Give full handoffs a useful smoke check while preserving required release and security checks.

## Source proposal

The Maintainer accepted the heavy proposal at `65b723fc`: add a Cairn-local
profile smoke selection, clarify handoff and slow-test obligations, and compare
fresh results from the existing release pytest run against independently owned
required files. Ordinary and Security plan reviews precede implementation.
The accepted source proposal is archived at plan opening; the plan retains its
decision record and executes the authorized outcome.

## Scope

Deliver the handoff guidance and a release-only, standard-library result
comparison as one independently finishable outcome. Change the published
session routine, governing local and shipped instructions where needed, the
local custom routine, and release instructions; inspect the session-end skill
and both testing-discipline copies for consistency. Trace readers and byte
pins before editing. Coordinate shared guidance and test selections with the
suite-consolidation owner before claiming or editing them.

Reuse the existing profile smoke command, security manifest and reviewed-set
test, and the release pytest invocation. A search for `junit`,
`SECURITY_FAMILY`, and the release command in `scripts/`, the release
instructions and security tests found a JUnit producer and the manifest, but
no existing release-membership comparator. Inspect those owners again before
building. `scripts/check_release_test_members.py` adds no registry or second
suite run, and does not
modify protected security hooks. Cairn has no configured slow roster; an
adopter's authoritative configuration is independent of observed results.

### Documentation / doctrine surface

Use `AGENTS.md` and `templates/core/AGENTS.md` for governing prescription,
`docs/methodology/session-routines.md` for the published routine, and
`docs/release-process.md` for the executable release sequence. Change
`templates/skills/session-end/SKILL.md` or the testing-discipline copies only
where their wording needs alignment. The custom routine is local, not a
shipped default.

## Sequence

Estimate: 2-4 focused workdays for implementation, evidence and reviews;
JUnit identity mapping, isolated real-entry-point mutations, and coordination
may extend that estimate. The existing command, manifest and test homes are
available now; no other unfinished plan or release is a prerequisite.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Trace and implement handoff guidance and local smoke; coordinate shared surfaces. | Both required plan reviews and author dispositions; ready-to-implement. | Honest handoff reporting and unchanged required-check timing. |
| C2 | Implement and test the release comparison and executable instructions, including independent adopter slow-set proof. | C1 and the same plan-review gate. | Fresh-report comparison and falsifiable release-shaped evidence. |
| C3 | Complete ordinary code review, separate Security Review, fixes and wide Boundary B. | C1-C2 evidence and committed implementation. | Reviewed, verified work ready for archive. |

No routine human release or trust operation gates archive. A later release
must execute its own unchanged required checks and the new comparison; until
then that release result is unpassed. Archive grants no release authority.

## Acceptance criteria

**C1.** A full handoff runs the configured fast/default smoke and records its
command, result and limits; absent or failed configuration is not reported as
passed. Reflection-only participants gain no suite obligation. Cairn's local
`python -m pytest bootstrap/tests/test_profiles_smoke.py` runs under canonical
Python 3.13, with elapsed time and coverage limitations recorded before any
speed claim. Adopter examples cover configured and absent commands and a failed
command. Slow tests remain due at release and when an accepted plan, safety or
security requirement, or Maintainer requires them; change checks and Boundary B
remain due on their existing schedule. Existing certification commands and
triggers are preserved.

**C2.** The release sequence adds JUnit output to the existing pytest
selection and seed, requires a previously absent output path, immediately
compares it against `SECURITY_FAMILY` and a successful case from
`test_security_marker.py`, and preserves a nonzero result from either command.
The comparator refuses absent, stale, malformed or ambiguous reports, missing
files, files without executed cases, and skipped or failed required cases.
The reviewed security-family pin is verified. In isolated copies, omit a
required security file from the actual release-shaped invocation and a
configured slow file from an adopter-owned selection; each comparison fails
even when pytest succeeds. Exercise actual XML identity mapping, pytest failure
propagation and the other refusal cases. The comparison proves file-level
presence and reported outcomes only, not individual nodes, provenance or
semantic adequacy; the separate `bootstrap/security_check.py` run and all
existing release and security checks remain owed.

**C3.** Independent ordinary and Security code reviews and their required
dispositions precede wide Boundary B. All accepted checks and defects are
resolved before archive; no future release substitutes for missing evidence.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: trace callers, configuration, public entry points, readers and
byte pins; map changed files to owners and consumers. Run
`python tools/test_tiers.py for <paths>` for the actual changed paths and its
selected tests, plus claim, link, snippet and neutrality prose gates. Add
focused tests for uncovered plausible failures, including the real-entry-point
mutations above, in isolated copies. Record commands, outcomes, interpreter,
elapsed time and limitations; do not run a full-tree certification merely for
this work.

Boundary C: an independent reviewer reads committed implementation and
iteration evidence and runs targeted falsification, not a suite. A separate
Security Review covers the comparison and its failure boundaries. Address
findings under the review rules before final integration.

Boundary B: after review and fixes, run the mapped iteration list for the
entire reviewed range and tier-map integration/workflow tests naming those
files, plus applicable standing gates and all acceptance checks, on a clean,
unchanged final commit under canonical Python 3.13. Use `wide` for the shared
contract and security surface. Record the tested SHA and range, interpreter,
clean pre/post state, commands and counts, timing, non-pass dispositions and
omissions in the implementation verification record. Record timing misses
and list test files over ten seconds as required. A missing required check
keeps the plan open; release certification remains a separate ceremony.

## Plan review -- Codex GPT-5 (Medium) -- 2026-11-05

Reviewed commit: c7d71287803ec06ab339512385ed663cc7f8c971

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: SHIP
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: C1-C3 carry the accepted handoff, comparison, review and verification outcomes; the independently owned security family and separate security run remain distinct -- plan, Acceptance criteria; accepted proposal, Tests required.
2. **Best alternative.** Manual release-output inspection avoids a new comparator but loses automatic detection of a required file omitted from the run; the Decision chose the comparison -- accepted proposal, Alternatives considered and Decision.
3. **What would show it wrong?** An omitted required security file or adopter-configured slow file passing comparison despite a successful pytest invocation would defeat the proof -- plan, C2.

The plan leaves routine human release and trust operations outside the archive
fence and keeps a later release unpassed until its own checks run. Its comparator
claims file-level outcomes, not node-level completeness or provenance.

**Coverage:** Committed plan, accepted proposal and Decision, plan template,
and release instructions. Not covered: implementation, mutations, a suite, or
the separately required Security plan review.

## Plan review -- Sol (High) -- 2026-11-05

Reviewed commit: 2ee80c60555e85aae4634333b36f7d847b0c2d98

**Model attribution**: Sol (High), coordinator assignment per Maintainer;
fresh reviewer, not the plan author.
**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: SHIP
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: C1 preserves required-check timing and honest incomplete reporting; C2 carries the accepted independent-set omission proof without replacing the protected security run -- plan C1-C2; accepted proposal, Decision and S1-S5.
2. **Best alternative.** Reuse the existing pytest invocation and manifest, adding only its report comparison as planned; manual inspection costs less code but loses automatic omitted-file detection, while a second runner adds unnecessary execution and maintenance -- plan Scope; accepted proposal, Alternatives considered.
3. **What would show it wrong?** A successful comparison after an actual required-file omission, ambiguous identity, stale report, or nonzero pytest exit would falsify C2; require those real-entry-point refusal tests before completion -- plan C2 and Verification.

The expected security set comes from `bootstrap/tests/security_manifest.py`,
not observed XML. The separate oracle is
`bootstrap/tests/test_security_marker.py::test_the_manifest_still_names_exactly_the_reviewed_set`;
C2 requires verifying that pin as well as a successful case from its file.
A successful case alone cannot prove the pin assertion ran; C2 explicitly
avoids node-level or provenance claims.

C2 requires a previously absent report path, immediate comparison, real XML
identity mapping, ambiguous-report refusal, and failure from either command.
These constrain accidental omission; they do not authenticate forged XML.
The accepted S5 threat limit remains intact. Skipped or failed required cases
cannot pass, and stricter handling in the separate `bootstrap/security_check.py`
run remains owed. C3 places separate Security code review before wide Boundary B;
missing evidence keeps work open rather than becoming a future-release promise.

**Coverage:** Committed plan, archived acceptance and security records, AGENTS,
plan template, review sweep, release instructions, manifest and reviewed-set
test; reuse search found the existing JUnit producer but no comparator.
**Not covered:** implementation, report-parser robustness, mutations, adopter
configuration, suite execution or release/trust operations. No runtime safety
claim is established by this plan read.

## Implementation verification -- Codex GPT-5 (Low) -- 2026-11-05

**C1 partial:** Added the Cairn-local `## Goodnight` profile smoke selection
in `dev/rules/custom_session_routines.md`. The shared guidance surfaces remain
open pending coordination with the suite-consolidation owner; C1 is not complete.

**Boundary A / B:** bounded; iteration only, not final Boundary B. Tested
worktree bytes before commit; canonical interpreter:
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13).

**Evidence:** `python -m pytest -p no:cacheprovider
bootstrap/tests/test_profiles_smoke.py` -- 15 passed, 0.22 s; this covers
profile parsing, preset expansion and scaffold summaries, not general tree
correctness. Tier selection via `tools/test_tiers.py for
dev/rules/custom_session_routines.md` selected
`bootstrap/tests/test_skill_contract.py`; that test file passed, 6 tests,
0.03 s. `scripts/claim_check.py`, `scripts/link_check.py`,
`scripts/sync_doc_snippets.py --check`, and `scripts/quality_gate.py --sub
neutrality` passed; neutrality reported 0 failures. No suite, release,
mutation, adopter example, code review, Security Review or Boundary B run.

**Coverage gap:** Shared local/shipped instructions and the published routine
remain unmodified. Need owner coordination before those edits. C2 and C3 remain
unstarted. Elapsed: approximately 14 minutes; tokens: unknown.

## Verification record correction -- Codex GPT-5 (Low) -- 2026-11-05

The preceding elapsed estimate was overstated. From the first C1 implementation
claim at 21:41 EDT through commit `da46fa03` at approximately 21:45 EDT, this
partial C1 segment took about 5 minutes. Token use remains unknown.

## Implementation verification -- Codex GPT-6.1 Terra -- 2026-11-05

**C1 partial:** Coordinator reported in chat that the suite-consolidation agent
Peirce had stopped and no suite owner was editing shared guidance. Commit
`b575e913` aligns `AGENTS.md`, `templates/core/AGENTS.md` and the session-end
skill; `71a456f3` and `47da11ee` add and retain a focused skill contract and
its false-pass controls. The published routine remains open: an older active
methodology-clarity claim includes it. C1 is not complete; C2 and C3 remain
open. Release-file coordination with the active strict-runner track is owed.

**Boundary A:** On a separate copy of `b575e913`, Python 3.13.13 ran the
range-selected 15 files twice: 1,070 passed in 55.63 s and 1,070 passed in
54.64 s. `tools/test_tiers.py for --range b3b4141d..b575e913` selected
`test_engine_copy_fallback_contained.py`, `test_install_time_onboarding.py`,
`test_next_session_local_note.py`, `test_review_stance_in_shipped_files.py`,
`test_security_stack.py`, `test_session_start_drain_rules.py`,
`test_session_writes_contained.py`, `test_skill_contract.py`,
`test_skills_fanout.py`, `test_skills_install.py`, `test_skills_matrix.py`,
`test_skills_security.py`, `test_skills_self_heal.py`, `test_skills_upgrade.py`
and `test_upgrade_lockfile_path_containment.py`, all under `bootstrap/tests/`.
The selector omitted 42 broader `AGENTS.md` readers under its guard.

On a separate copy of `47da11ee`, the two selected files for the test change,
`test_session_start_drain_rules.py` and `test_skill_contract.py`, passed 10
tests in 0.05 s. In separate copies, false-pass mutations for absent and failed
commands each failed the focused contract; both controls are retained in the
test file. Claim, link and snippet checks passed on the three guidance files;
neutrality reported zero failures. These checks do not exercise a human handoff.

**Timing:** The iteration run exceeded its 30 s diagnostic. Summed JUnit case
times over 10 s, slowest first: `test_security_stack.py` 26.435 s;
`test_upgrade_lockfile_path_containment.py` 11.895 s. Add these to the existing
test-consolidation list at its serialization point. Final wide Boundary B,
ordinary and Security code reviews, C2 evidence, and release checks are not
claimed. No full suite, repin or push. Elapsed: approximately 7 minutes; tokens:
unknown.

## Implementation verification -- Codex GPT-6.1 Sol -- 2026-11-05

**C1 and C2 delivery:** C1 is implemented, including the published routine at
`2a16b0b4`; C2 is implemented at `e923b3dd`. Coordinator chat confirmed that
the stale claims were retired and the release document was available; live
claims had no overlap on these exact paths. Both testing-discipline copies were
inspected and needed no cadence change. No board or changelog was edited.
Resolved forward-path declarations were removed as required by the template;
their files now exist. No accepted scope changed.

The comparator reads the existing security-family declaration without executing
it, also requires the reviewed-set test file, and compares file identities and
outcomes in one fresh report. Its explicit adopter mode reads that project's
independent JSON list rather than creating a Cairn slow-file registry. The
documented sequence preserves the existing selection and seed, requires an
absent report path, compares immediately, and propagates either command's
failure. The separate strict security runner is unchanged and remains owed.

**Boundary B mode:** wide, owed after ordinary and Security code reviews; the
following is Boundary A iteration evidence, not a final integration result.
**Tested commit:** `e923b3dd7bbafd2bdf2e1b639d310ba3a1bb4801`; the methodology
selection used `2a16b0b4ac9baba6f241abf6abd24ad74232d13d`.
**Reviewed range:** upcoming review scope is `787df691..e923b3dd`, restricted
to this plan's local rule, two AGENTS copies, session-end skill, published
routine, release document, comparator, skill-contract test and
`bootstrap/tests/test_release_members_contract.py`; interleaved scanner and
strict-runner changes are not claimed by this work.
**Interpreter/runtime:** `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
Python 3.13.13, pytest 9.0.3.
**Pre-run state / Post-run state:** separate committed copy, clean at the named
HEAD before and after each selection. The shared checkout was not used for
writing checks.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---|---|---|---|
| `python -m pytest -p no:cacheprovider bootstrap/tests/test_incident_trackers_module.py bootstrap/tests/test_next_session_local_note.py bootstrap/tests/test_skill_contract.py` | 0 | 52 passed | 2.95 s | unknown |
| `python -m pytest -p no:cacheprovider bootstrap/tests/test_release_members_contract.py bootstrap/tests/test_security_marker.py::test_the_manifest_still_names_exactly_the_reviewed_set` (plus durations/JUnit reporting) | 0 | 44 passed, 0 failures/errors/skips; no xfail/xpass | 2.92 s | unknown |
| `python -m pytest -p no:cacheprovider bootstrap/tests/test_profiles_smoke.py` | 0 | 15 passed | 0.36 s | unknown |
| `python tools/test_tiers.py check` | 0 | 135 files each mapped once | unknown | unknown |
| `scripts/check_cairn.py` on the six changed guidance files; claim, link and snippet checks on both new document changes; `scripts/quality_gate.py --sub neutrality` | 0 | no issues; neutrality 0 failures | unknown | unknown |

`tools/test_tiers.py for` selected the three methodology readers above and
only the comparator contract file for C2's three paths. The independently
reviewed manifest pin was an additional accepted check. Earlier shared-rule
iteration evidence and its 42 omitted broad readers remain recorded above.

**Plan-specific acceptance commands:** The contract file executes the documented
shell block against isolated small release-shaped fixtures, removing the
certification override. Real pytest xunit1/xunit2 reports pass. Omitting
`test_security_lint.py`, the marker file, or an adopter-configured slow file
leaves pytest successful but fails comparison. A non-required pytest failure
survives a successful comparison. Existing-report refusal, freshness, malformed
and ambiguous XML/identity, missing configuration/source/cases and skipped or
failed required cases are repeatable tests. The 18-file fixture uses the real
manifest bytes and minimal test bodies: it proves omission detection through
the actual command shape, not the full security family's semantic adequacy.

**Non-pass disposition:** the initial plan claim check found a stale forward
declaration; removing resolved declarations closed it, and the rerun passed.
Intentional omission/refusal controls fail as expected inside passing tests.
No timing diagnostic was exceeded in this
segment. **Known omissions:** ordinary code review, separate Security Review
and final wide Boundary B remain C3 work. No full-tree certification, release,
repin or push ran; no release result is claimed. Elapsed: approximately 9
minutes; tokens: unknown.

## Code review -- Codex gpt-6.1-terra (Medium) -- 2026-11-05

Reviewed commit: 92b0720bcde71c0ad981ba9013f0d9445fa260b6

**Foundations**

1. **Should this happen as framed?** Yes: the handoff guidance distinguishes absent and failed smoke results, and the release block preserves both command statuses; the focused tests below exercise those claims -- `templates/skills/session-end/SKILL.md`; `docs/release-process.md`.
2. **Best alternative.** Manual inspection removes comparator maintenance but cannot reliably detect a required file omitted from a successful run; the comparator instead reads the independent manifest and rejects missing successful files -- `scripts/check_release_test_members.py::required_files` and `compare`.
3. **What would show it wrong?** A fresh real pytest report that passes after a required-file omission, or a failed pytest command reported as successful, would falsify the result; the targeted real-entry-point controls rejected those cases. A future release-shaped run using the full tree is a further test of report identity mapping -- `bootstrap/tests/test_release_members_contract.py`.

**Findings:** none.
**Verdict:** SHIP
**Elapsed:** unknown
**Tokens:** unknown

On an isolated archive of the reviewed commit, Python 3.13.13 ran the actual
pytest identity, security and adopter omission, pytest failure propagation, and
smoke false-pass control nodes: 9 passed in 1.64 s. The implementation record
reports the wider iteration checks, independent manifest pin, and remaining wide
Boundary B; this review does not substitute for them.

**Coverage:** Read the scoped committed diff, C1-C3 and implementation evidence;
exercised targeted controls above. Did not run the full security family, release
ceremony, final integration, or separate Security Review; the small fixtures do
not establish full-suite identity mapping or test semantics.

## Code review -- Codex gpt-6.1-sol (High, Security Review) -- 2026-11-05

Reviewed commit: 92b0720bcde71c0ad981ba9013f0d9445fa260b6

**Foundations**

1. **Should this happen as framed?** Yes: the comparator reads requirements independently of observed XML, refuses unsuccessful required cases, and preserves the separate security run; the smoke guidance retains required-check timing -- `scripts/check_release_test_members.py`; `docs/release-process.md`; both AGENTS copies.
2. **Best alternative.** Retain one pytest invocation and its existing manifest, as implemented; manual inspection avoids comparator maintenance but loses automatic omission detection, while another runner adds unnecessary execution -- `docs/release-process.md`, release shell block.
3. **What would show it wrong?** A stale or ambiguous report, omitted required file, or failed pytest command yielding a successful block would falsify C2; targeted controls below rejected those cases. A full-tree release report remains a forward test of identity mapping -- `bootstrap/tests/test_release_members_contract.py`.

**Obligation:** separate Security code review
**Tier:** Internal Security Review
**Findings:** none.
**Verdict:** SHIP
**Elapsed:** unknown
**Tokens:** unknown

In an isolated archive, Python 3.13.13 passed 15 targeted comparator cases
in 1.88 s: actual xunit1/xunit2 identities, security/marker and adopter slow-file
omissions, existing-path refusal, stale/future timestamps, ambiguous or
disagreeing identities, unsuccessful required cases, and pytest failure
propagation. Four independent-pin and smoke false-pass contract nodes passed
in 0.03 s. In another copy, removing `test_web_hosting_security.py` from the
manifest made the reviewed-set pin fail as expected (one failure, 0.03 s).

The default required set includes the marker file; its successful case alone
does not prove every assertion ran. Bounded UTF-8 parsing rejects declarations,
limits input size and checks report identity during reading. These controls
support accidental-omission detection, not forged-evidence authentication.

**Bounding:** ACCEPTED -- challenged report freshness, source identity and the
independent required set through the mapped contract; final wide Boundary B
remains owed.

**Coverage:** Scoped committed implementation range `787df691..e923b3dd`,
accepted proposal, C1-C3, iteration evidence and targeted controls. Not covered:
full security-family semantics, complete-suite identity mapping, final Boundary
B, strict security runner, release, baseline, signing or push operations.

## Implementation verification -- Codex (coordination) -- 2026-11-05 -- joined final check

C1-C3 are complete. Ordinary review `a9ccdc67` and separate Security Review
`46711ced` found no findings. Final **wide Boundary B** ran after both on clean
committed `88679232404f5e5ec72aab8f5f9799710f10d483`, canonical Python 3.13.13,
with clean pre/post state. The [joined onboarding record](2026-11-05-one-time-onboarding.md#implementation-verification----codex-coordination----2026-11-05----joined-final-check)
records the scoped paths, commands, permitted batches, counts and limitations:
4,459 passed, nine Windows-only Mac skips, and two reviewed expected engine-AST
failures left **UNPASSED** for the separate release baseline. No new functional
failure occurred; no release result or whole-tree pass is claimed.

The final selection includes the real release-report contract, independently
pinned security-family check, smoke and installed skill/module consumers.
Implementation omission/failure-propagation controls and both independent
reviews remain in their original records. Relevant claim/link/content/snippet
gates passed; neutrality and redundancy had zero failures. The fifteen guarded
governing-only readers remain omitted, not passed. No required scope or check
was silently removed. No additional implementation follow-up remains.

The runtime release comparison and strict security run remain due at the later
release trigger, not prerequisites to this implementation's archive. Close issue
#53 on the delivered cadence guidance. **Status: ready-to-archive.** No new plan,
full suite, trust operation, push or release. Joined batch wall time: 621.02
seconds; total coordination and tokens: unknown.
