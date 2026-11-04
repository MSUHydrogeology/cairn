# Plan: Consolidate the suite without losing detection

**Source proposal**: dev/proposals/archive/2026-11-02-codex-suite-consolidation.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-04
**In brief**: Reduce repeated test preparation and organize tests while preserving the faults and protections they detect.

## Source proposal

The accepted heavy proposal orders expensive families first, shares immutable
preparation, preserves fault detection, moves ordinary tests into tier folders,
and measures scoped savings and suite growth without changing certification.

## Scope

Work in `bootstrap/tests/`, `tools/test_tiers.py`, `tools/test_tiers.json`,
their consumers and existing testing guidance. Preserve protected paths and
all configured suite members. Coordinate suite-growth reporting with the
accepted meter in board item 2b; deliver it through that shared pulse, not a
second store. Coordinate strict-runner item 7a separately; its repair is not
added to this proposal. No signing, trust-record or baseline changes are
authorized. Human ceremony and release operations remain board item 12, not
plan completion requirements.

**Reuse.** Searching `bootstrap/tests/test_gate_preflight.py` found `_repo` and
`_closure_repo`; reuse family builders with separate mutable repositories.
`tools/test_tiers.py` already discovers recursively and selects changed-file
readers. `bootstrap/tests/conftest.py` supplies the existing shuffle hook.

### Documentation / doctrine surface

Update self-hosted and shipped testing guidance, including
`templates/modules/team-gated/testing-discipline.md`, and affected command and
import references. Preserve the governing verification contract and route
description and prescription to their existing homes.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inventory and rank setup/call cost; consolidate preflight, ceremony and upgrade families first. | Both plan reviews and fold | Family-local immutable preparation and independent mutable fixtures; fixture repair. |
| C2 | Consolidate remaining measured slow families; map every changed case and challenge its faults. | C1 | Retained or combined checks and verification mapping. |
| C3 | Move ordinary tests into tier folders in reviewed batches. | C1; installed v0.6 baseline | Tier map, imports, collection and command consumers, node mapping, guidance. |
| C4 | Compare timings and integrate growth reporting with 2b. | C1-C3 and 2b shared reporting | Scoped before/after evidence and shared growth/runtime summary. |

## Acceptance criteria

**C1.** Rank the board's complete over-10-second list and earlier mapped
candidates using existing records and scoped setup/call durations; retain the
recorded ranking and address each family, starting with ceremony/preflight
and upgrade. Share only immutable descriptions, source snapshots or builders;
each mutating case owns its paths, repository, environment and teardown.
In `bootstrap/tests/test_gate_reanchor.py::test_rostered_stage_b_executes_only_preflight_bytes_pinned_by_p`,
allow the P setup commit when the generated manifest is already current; keep
all security assertions unchanged. Protected-test changes receive ordinary and
Security code review and retain prescribed gate procedures.

**C2.** Before combining or removing each case, record its old node,
assertions and plausible faults against retained nodes in the existing
verification record. Run targeted negative controls or existing failing inputs
through those nodes. Preserve distinct public-entry, malformed-input,
permission, cleanup and security-refusal behavior; green tests or counts alone
do not establish equivalence. Keep reusable probes in owning tests. For each
sharing batch compare collection and outcomes under seeds 0 and 1 with fresh
mutable state. Report any missing fault coverage; it keeps work open.

**C3.** List ordinary files from the tree and their assigned tier; move them
to corresponding tier directories while leaving protected apparatus at its
approved paths. Map each old node to its new identity and reconcile collection,
imports and explicit commands, including consumers found by searching paths
and filenames. Update the tier map and both self-hosted and shipped guidance.
`bootstrap/tests/test_test_tiers.py` must retain recursive discovery and
changed-file selection; `bootstrap/tests/test_gate_manifest.py` must retain
dropped protected node, ordinary delta and skip/xfail marker coverage. A lost
node or altered protection cannot be hidden by a new roster.

**C4.** Compare scoped setup and call durations on before/after committed
snapshots with the same Python 3.13 interpreter, selections, seeds and stated
conditions; report results and misses, not test-count success. Deliver suite
growth and runtime summaries in 2b's shared pulse. Measure the ten-minute
full-run target only at an existing authorized certification point, with its
commands, triggers, configured members and security outcomes unchanged; report
the result there, not as a human-run prerequisite to this plan's completion.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: for each changed path run `python tools/test_tiers.py for <paths>`
and its selected tests, plus applicable prose gates. Use scoped pytest
`--durations=0 --durations-min=0` and `--quality-gate-shuffle-seed=0` and `=1`
for the comparisons above. Run `python tools/test_tiers.py check`, the named
tier and manifest checks, the repaired node, and affected real CLI/install and
upgrade paths. Map their consumers and actual outcomes in the implementation
record. Collection executes candidate code with host access: scratch paths are
not containment. Retain the key-away and ceremony restrictions in
`bootstrap/REANCHOR_RUNBOOK.md`; do not replace pre-change authority with a
candidate-generated roster. S2 fault controls belong to C1-C3; S3 uses their
scoped pytest and existing gate commands. No scientific equation changes.

Boundary C: independent ordinary and Security code reviews falsify the changed
checks and mapping with targeted tests, not a suite. Boundary B follows review:
use wide mode on a clean, unchanged final commit with canonical Python 3.13,
the reviewed range's iteration selection plus tier-map integration/workflow
consumers and applicable standing gates. Record SHA/range, interpreter,
pre/post state, commands, counts, elapsed, tokens, non-passes and omissions.
Unmet checks stay open. The later authorized certification is separate; no
extra full-suite run is authorized here.

## Plan review -- Codex Terra -- 2026-11-04

Reviewed commit: 46c8a55ffb6a59250276d8f627611e6d2c945ff2

**Obligation**: Internal
**Tier**: Internal
**Findings**: none

**Foundations**

1. **Should this happen as framed?** Yes: C1-C4 carry the accepted five outcomes, including independent mutable fixtures, preserved fault detection and shared reporting -- accepted proposal, Proposal 1-5; plan, Acceptance criteria.
2. **Best alternative.** Reuse existing family builders and recursive tier discovery, as the plan proposes; a separate runner would add machinery without delivering an additional accepted outcome -- `bootstrap/tests/test_gate_preflight.py`; `tools/test_tiers.py`.
3. **What would show it wrong?** A mapped fault surviving a retained check, or different outcomes under seeds 0 and 1, would falsify the implementation's preservation claim -- plan, C2 and Verification.

**Verdict**: SHIP. No blockers.

**Elapsed**: unknown. **Tokens**: unknown.

**Covered**: accepted scope, low-tier execution sequence, node and fault mapping, ordering, fixture repair, tier consumers, reporting dependency and review boundaries; findings prose: 0 words versus historical 216 and 194. **Not covered**: implementation results, timing, mutations, certification or the separate Security Review; no tests were run.

## Plan review -- Codex Sol (Security Review) -- 2026-11-04

**Model**: Sol (high; required floor).
Reviewed commit: cce8e92dace5e7a1fa7bda325a18dcc32ccc38fa
Operative plan: 46c8a55ffb6a59250276d8f627611e6d2c945ff2; later commit adds only Terra's review.

**Tier**: Internal Security Review
**Obligation**: Internal Security Review

**Foundations**

1. **Should this happen as framed?** Yes: C1-C4 preserve the heavy Decision's detection, tier-location and shared-reporting outcomes without granting ceremony authority -- accepted source proposal, Proposal 1-5 and Decision; plan, Scope and C1-C4.
2. **Best alternative.** Reuse family builders and immutable install snapshots, with separate mutable copies; another runner adds isolation work without an accepted benefit -- `bootstrap/tests/test_gate_preflight.py`, `_repo`/`_closure_repo`; `bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py`, `pristine_install`/`project`.
3. **What would show it wrong?** A removed fault surviving its retained node, seed-dependent refusal or cleanup, or protected membership changing during an ordinary move would falsify preservation -- plan C2-C3; `bootstrap/tests/_gate_manifest.py`, `verify`; `bootstrap/tests/conftest.py`, `pytest_collection_modifyitems`.

**Findings**: none.

**Verdict**: SHIP. No blockers. Ordinary deltas are notes, not detection evidence;
C2's assertion/fault mapping therefore remains necessary. Protected losses and
new skip/xfail markers HOLD; `_trusted_roster_from_anchor` rejects candidate
roster substitution. C3 preserves that classification, not a replacement roster.
The P fixture repair retains every assertion, including candidate-preflight
non-execution and unauthorized-byte refusal in the named reanchor node.
C4 waits for 2b's shared pulse; partial reporting cannot close it. Independent
ordinary and Security code reviews precede final wide Boundary B; later
certification cannot substitute for missing checks.

Seven targeted roster-authority and recursive/changed-file-selection probes
passed in a separate cce8e92d copy: Python 3.13.13, 0.50 seconds; no non-passes.

**Elapsed**: approximately 6 minutes. **Tokens**: unknown.

**Covered**: approved authority, protected nodes/markers, fixture isolation,
hostile public paths, cleanup, tier consumers and completion fences; second
real-review trial: findings prose 0 words versus historical 216/194, not a quota.
**Not covered**: implementation equivalence/mutations, seed trials, fixture-fix
execution, performance, final Boundary B or certification; no suite or ceremony
run. Source-archive link repairs remain the parent's work.

## Response -- Codex Terra -- 2026-11-04

Both the ordinary and Security plan reviews shipped with no findings. No
operative changes are needed. Elapsed: unknown; tokens: unknown.
