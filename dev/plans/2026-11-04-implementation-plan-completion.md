# Plan: Complete implementation plans without human-run operations

**Source proposal**: `dev/proposals/archive/2026-11-03-codex-implementation-plan-completion.md`
**Status**: implementing
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

## Plan review -- Codex Terra (MEDIUM) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Yes. C1 preserves agent-owned checks and the distinction between an unpassed baseline operation and an unexplained integrity failure; C2 requires separate reviews and final wide verification -- accepted proposal, Alternatives and Decision; plan, C1-C2.
2. **Best alternative.** Continue case-by-case amendments and existing board waits; it avoids doctrine edits but repeats human intervention and leaves adopters without the general rule -- accepted proposal, Alternatives; `tools/board.py::_roadmap_waits`.
3. **What would show it wrong?** A fresh install with contradictory completion guidance that survives a per-surface mutation, or a missing agent check treated as a human wait, would show failure -- plan, C1 and Verification; `bootstrap/tests/test_review_sweep_ships.py::installs`.

Reviewed commit: 26c1133c2a0fbca7836b317ac6e98868a5d8fc95

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: SHIP

The plan names both governing copies, live and shipped templates, the shipped board and methodology; it requires isolated mutations and passing controls, without adding machinery or a release plan. Existing verification-boundary tests include wide and release-separation guards. Scientific evidence required by other work remains required; this change makes no scientific claim.

**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Coverage**: Committed plan, accepted proposal and Decision, plan template, named methodology and board guidance, and cited test and board triggers. **Not covered**: implementation, actual mutations or test runs, Security Review, scientific runs, release operations and full suite.

## Plan review -- Codex Sol (HIGH) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Yes. C1 retains failed agent-owned checks, missing scientific/functional evidence and reviews as implementation work; a named human baseline operation stays unpassed, and archive grants no activation authority -- plan, C1; accepted Decision `e2aae09f`; Terra classification `9b59ba4e` and author response.
2. **Best alternative.** Extend the existing install-test home and use existing board waits, as planned; a new operational register or release-plan lifecycle adds upkeep without strengthening authority -- plan, Scope and Verification; `bootstrap/tests/test_review_sweep_ships.py::installs`; `templates/core/dev/PLANNING.md`, Waiting on you.
3. **What would show it wrong?** Delete the split or insert human-only completion instructions separately on each listed source/installed surface: a surviving mutation, transferred functional failure or archive-as-release permission would falsify delivery -- plan, C1 and Verification; accepted proposal, S2-S4.

Reviewed commit: 26c1133c2a0fbca7836b317ac6e98868a5d8fc95
Ordinary review read: b0de365c.

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT -- plan only.

The scope names live and shipped governing text, plan templates, roadmap and
methodology, with proposal guidance adjusted where needed. C1 requires a
surface roster, isolated mutations and passing controls. The cited fixture
actually invokes the scaffold CLI and installed-output tests read its files;
this is a viable extension point, not evidence that future checks already pass.
C2 preserves separate ordinary/Security code reviews and final wide Boundary B.
Scope, Decision and unexpected-boundary stops remain; no key, pin, release
operation or added execution machinery is authorized.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Committed plan, accepted proposal/Decision/classification response,
ordinary review, governing rules, plan template, installed-test fixture and
mutation bodies, scope-floor and verification/release-separation guards.
**Not covered**: implementation, future per-surface mutation outcomes,
scientific execution, cryptographic authentication or ceremonies. No
implementation tests or full suite run; text checks cannot prove honest conduct.

## Response -- Codex LunaLOW -- 2026-11-04

Both required plan reviews are committed with matching Internal and Internal
Security Review obligations and no findings. No operative change is needed;
the accepted scope, evidence requirements and human-authority boundaries remain
as reviewed. The plan advances to `ready-to-implement`.
