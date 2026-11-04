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

## Implementation log -- bounded C1 P fixture repair -- 2026-11-04

Commits: plan transition `c064a02b`; fixture and changelog repair `320a140e`.
This is one bounded C1 repair only, not C1 or plan completion. At the named P
setup, `_commit_all(..., allow_empty=True)` permits an empty commit only for
this call; all existing security assertions and all other helper callers remain
unchanged. The Minor changes entry is in `CHANGELOG.md`.

Before-fix reproduction: clean committed copy `f4cd08d7b6f8a84e34b910635e652eb2aba8ea51`.
Command: `/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest
bootstrap/tests/test_gate_reanchor.py::test_rostered_stage_b_executes_only_preflight_bytes_pinned_by_p
--junitxml=/private/tmp/suite-before.xml -q`. Python 3.13.13; 1 failed,
0 passed, 6.505 seconds. P setup raised `nothing to commit` before assertions.

After-fix: clean committed copy `320a140e28df042293ad285a970c3ed298d4dfaf`.
The real mapper command `/Users/kendal30/conda_envs/lhm/bin/python3.13
tools/test_tiers.py for bootstrap/tests/test_gate_reanchor.py` selected exactly
`bootstrap/tests/test_gate_reanchor.py` and
`bootstrap/tests/test_security_marker.py`. Command:
`/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest
bootstrap/tests/test_gate_reanchor.py bootstrap/tests/test_security_marker.py
--quality-gate-shuffle-seed=0 --junitxml=/private/tmp/suite-after.xml -q`.
Python 3.13.13; 26 passed, 0 failed, 47.467 seconds. Both committed copies
were clean before and after their test runs. Collected node lists for the two
files had no diff; the named node identity is unchanged. Diff inspection found
no removed assertion.

Frozen-file drift: `bootstrap/tests/fixtures/gate_manifest.json` still records
the prior test SHA-256 `7556acfd9a850e6da584121254a48912a2d081a621e46234ce54a7aa28f6f7bd`;
the repaired test is `2047c7a71dff9f65c29de9bfd2cfb1f6c3f6267163fb3d31c593c36db32fa58e`.
No manifest, baseline or ceremony file was changed. This protected-byte
difference remains for the separately authorized human repin; it is not a
human step in this plan's completion.

Remaining: other C1 families and outcomes, independent ordinary and Security
code reviews, final wide Boundary B, and all other plan criteria. No
performance or certification claim is made. Elapsed: unknown; tokens: unknown.

## Implementation log -- C1 recovery -- Codex Terra -- 2026-11-04

One-tier-up retry after the stopped mapped run at `a2af94ce`: the reported
four-file seed-0 run stopped with 1 failed, 483 passed in 574.70 seconds.
The failing public CLI node runs the checker against its live source repository,
not a fixture clone made by the test. Its missing-ref refusal did not contain
the `bootstrap` text required by its existing assertion.

Separate disposable copies of `c2119553` (before) and `a2af94ce` (after)
were clean before and after testing. Both initially lacked
`refs/cairn/gate-anchor`. In each copy, Python 3.13.13 ran:

```sh
/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_gate_preflight.py::TestPublicCli::test_check_runs_against_the_live_repo_and_reports --quality-gate-shuffle-seed=0 --maxfail=1 -q
```

Before and after each failed 1 node in 0.38 seconds with the same missing-ref
refusal. After `git fetch -q origin
'+refs/cairn/gate-anchor:refs/cairn/gate-anchor'` in each copy, as prescribed
for fresh clones in `bootstrap/REANCHOR_RUNBOOK.md`, the same command passed
1 node in 0.33 and 0.31 seconds respectively. The source's existing anchor
was `977b5250abed59badd06b4940dccd39324644705`; no trust root was created or
changed. Future disposable copies need the documented explicit fetch from the
trusted source; this test's assertions remain unchanged. The stopped four-file
run remains incomplete and was not repeated.

The parent supplied matched eight-node timings: before, seed 0 18.12 seconds
and seed 1 17.01 seconds; after, 18.23 and 17.97 seconds, with concurrent B1
host load. These measurements show no speed benefit. The experimental cache
and clone changes in `a2af94ce` are withdrawn, including their changelog line;
the P fixture repair and its frozen-byte drift remain. C1-C4, mapped checks,
ordinary and Security code reviews, and final wide Boundary B remain open.
Elapsed: unknown; tokens: unknown.
