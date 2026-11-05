# Plan: Fast goodnight testing

**Source proposal**: dev/proposals/2026-11-05-codex-fast-goodnight-testing.md
**Author**: Codex GPT-5 (Medium)
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**In brief**: Give full handoffs a useful smoke check while preserving required release and security checks.

## Source proposal

The Maintainer accepted the heavy proposal at `65b723fc`: add a Cairn-local
profile smoke selection, clarify handoff and slow-test obligations, and compare
fresh results from the existing release pytest run against independently owned
required files. Ordinary and Security plan reviews precede implementation.
The source remains in place for this single-path plan commit; its normal archive
move remains a separate lifecycle operation.

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
