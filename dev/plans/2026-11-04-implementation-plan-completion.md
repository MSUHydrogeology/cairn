# Plan: Complete implementation plans without human-run operations

**Source proposal**: `dev/proposals/archive/2026-11-03-codex-implementation-plan-completion.md`
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-04
**In brief**: Let implementation plans finish after agent-owned work is complete while tracking human trust and release operations separately.

## Source proposal

The accepted heavy proposal assigns v0.7 delivery of the completion split to
self-hosted and shipped guidance, while preserving all checks, authority and
release safeguards. Its Decision and appended reviews remain in the archived
source; archiving implementation does not authorize activation or release.

## Scope

Update `AGENTS.md`, `templates/core/AGENTS.md`, `dev/plans/_template.md`,
`templates/core/dev/plans/_template.md`, `templates/core/dev/PLANNING.md`,
and `docs/methodology/plans.md` and `docs/methodology/lifecycle.md`. Adjust
`dev/proposals/_template.md` and `templates/core/dev/proposals/_template.md`
only where needed to prevent human operations being made implementation
acceptance criteria. Use existing standalone board rows for the actual human
operation and its evidence; do not create a release plan, tool or workflow.
No retrospective rewrite of archived work, release ceremony, pin, signing,
publication or push is included.

**Reuse.** No production code is added. Search of `bootstrap/tests` for
installed doctrine and scaffold found `test_review_sweep_ships.py`, whose
`installs` fixture runs `bootstrap/scaffold.py` for each profile and whose
installed and mutation tests provide a test-home pattern. The existing
`test_review_and_verification_rules_ship.py` covers both governing copies;
`test_verification_boundaries.py` guards verification and release separation.
`tools/board.py::_roadmap_waits` reads standalone waits, as established in the
source reviews. Do not duplicate that mechanism.

### Documentation / doctrine surface

Prescription belongs in both governing files and templates, with explanatory
methodology in the two named documents. Coordinate one writer for the shared
template window in batches 4-6 before implementation; this plan does not
claim or expand into the parent work on suite consolidation or onboarding.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Align governing, template and methodology guidance; extend existing shipped-doctrine tests. | Both independent plan reviews, their disposition, and template-writer coordination. | The complete split and its installed-output and mutation checks. |
| C2 | Obtain independent ordinary and Security code reviews; address findings, then perform final wide Boundary B. | C1 and its iteration evidence. | Reviewed implementation and recorded final change verification. |

## Acceptance criteria

**C1.** Implementation plans finish only after agent-owned scope, reviews and
applicable checks are complete, with no human-run trust or release operation
as a completion prerequisite. Existing board rows independently name those
operations, owners, evidence and links to implementation; archive is not
permission to activate or release. Decision, scope and unexpected-boundary
stops remain. No agent failure, defect, missing scientific or functional
evidence, or required review is moved to a human row to close work. A reviewed
trust record awaiting a named human baseline operation remains unpassed and
distinct from an unexplained integrity failure, which remains implementation
work. Fixing an issue is not a release.

Fresh installation through `bootstrap/scaffold.py` exposes the required
guidance in each named installed doctrine, plan and roadmap surface. Extend an
existing shipped-doctrine test home: list each required source and installed
surface, then separately delete or insert contrary instruction for each in
isolated copies; each mutation must fail its relevant check against a passing
unmutated control. Keep scope-floor, verification-boundary and release-gate
controls passing. Preserve functional, scientific and security checks.

**C2.** Separate ordinary and Security code reviews by reviewers other than the
implementer assess committed work; required findings and checks are resolved.
Final wide Boundary B covers reviewed fixes on a clean final commit. No real
key, pin or release operation is exercised. Scientific check: N/A; the source
changes no scientific assumption or result.

## Scope delta

**Scope delta**: preserved. The accepted outcomes and human authority remain;
no operation or check is waived.

## Verification

Boundary A: before implementation use `tools/test_tiers.py for <changed
paths>` with the reviewed range for governing text; run its named iteration
tests and applicable claim, link, snippet, content and neutrality prose gates.
Map actual changed paths and readers, including proposal guidance if changed.
Use `bootstrap/tests/test_review_sweep_ships.py` as the existing real-install
and mutation pattern, and inspect its `installs`, installed-output and deletion
test nodes before extending it. `bootstrap/tests/test_verification_boundaries.py`
contains explicit wide-boundary and release-separation guards; retain their
passing controls and identify the actual scope-floor and release-gate nodes
by opening their triggers during implementation. Test negative searches
against a known-positive case. Record each surface and mutation outcome,
including any survivor or omission; text tests do not prove honest conduct.

Boundary C: independent ordinary and Security reviewers read the committed
implementation and iteration evidence and run tight falsification checks,
not a suite. Boundary B follows review and fixes, in `wide` mode, on a clean,
unchanged final commit using `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(3.13.13): the reviewed-range iteration list, mapped integration/workflow
tests, installed-output and mutation checks, and applicable standing gates.
Record SHA and range, clean pre/post state, commands, counts, elapsed time,
tokens or unknown, non-pass dispositions and omissions. A missing required
check keeps the work open. No full-tree certification is authorized here.
