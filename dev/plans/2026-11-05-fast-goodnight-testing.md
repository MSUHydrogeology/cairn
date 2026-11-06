# Plan: Fast goodnight testing

**Source proposal**: dev/proposals/archive/2026-11-05-codex-fast-goodnight-testing.md
**Author**: Codex GPT-5 (Medium)
**Status**: implementing
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

Proposed paths:
* `dev/rules/custom_session_routines.md` -- local goodnight smoke selection.
* `scripts/check_release_test_members.py` -- release result comparison.

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
