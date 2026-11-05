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

Post-withdrawal smoke: clean disposable copy of `cd0dc282`, with the same
explicit anchor fetch, remained clean before and after. Python 3.13.13:

```sh
/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_gate_preflight.py::TestPublicCli::test_check_runs_against_the_live_repo_and_reports bootstrap/tests/test_gate_preflight.py::TestSterileGitLauncher::test_a_reference_transaction_hook_cannot_move_a_third_ref bootstrap/tests/test_repin_ceremony.py::test_a_full_ceremony_signs_once_with_the_typed_passphrase --quality-gate-shuffle-seed=0 --maxfail=1 -q
```

Three passed in 9.32 seconds. An earlier invocation used the wrong class for
the second node and collected no tests in 0.51 seconds; the command above
corrects it. These are focused smoke checks, not the incomplete mapped run.

## Implementation log -- C3 selector correctness repair -- Codex Luna (Implementation, low) -- 2026-11-04

This bounded correctness repair is advanced from C3 under the plan's live-plan
sequencing freedom so a mixed-path selection cannot lose directly selected
readers. Ordinary tier relocation still waits for C1 and the installed v0.6
baseline. C1-C4 outcomes and the operative plan cells are unchanged. This
record does not claim C3 completion or authorize a tier move.

## Implementation verification -- Codex Luna (Implementation, low) -- 2026-11-04

**Commit**: `a09f1ffeb724cddf007794ccd3e9706a83d4768e`; **Range**:
`27b7eb9f..a09f1ffe`; **Python**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`,
3.13.13. Tests ran in a separate clean clone, clean before and after; no files
were changed in that copy. Token use: unknown.

**Selection.** `python tools/test_tiers.py for tools/test_tiers.py
bootstrap/tests/test_test_tiers.py dev/plans/2026-11-04-suite-consolidation.md
CHANGELOG.md` selected 7 files. The seed-0 scoped run below passed 407 tests,
0 failed, in 66.01 seconds. No test file over 10 seconds was separately
measured from this combined run; no timing claim is made for individual files.

```sh
/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_board_json_contract.py bootstrap/tests/test_quickstart_sequence.py bootstrap/tests/test_scaffold.py bootstrap/tests/test_test_tiers.py bootstrap/tests/test_upgrade.py bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_verify_ref.py --quality-gate-shuffle-seed=0 --durations=0 --maxfail=1 -q
```

**Selector reproduction.** The exact committed copy selected these 6 direct
readers for `CONTRIBUTING.md`, `dev/modules/content-security.md` and
`templates/modules/team-gated/content-security.md`: `test_content_scan.py`,
`test_default_security_stance.py`, `test_review_stance_in_shipped_files.py`,
`test_scaffold.py`, `test_security_stack.py`, `test_upgrade.py`. The supplied
range `2a3ec47e..30ba0559` alone selected `test_review_stance_in_shipped_files.py`
and omitted 46 broad AGENTS readers. Combined, the CLI selected the same
independently expected 6-file union and omitted 43; direct readers
`test_scaffold.py`, `test_security_stack.py` and `test_upgrade.py` were retained.
The selection commands passed; elapsed time and token use: unknown.

```sh
/Users/kendal30/conda_envs/lhm/bin/python3.13 tools/test_tiers.py for CONTRIBUTING.md dev/modules/content-security.md templates/modules/team-gated/content-security.md
/Users/kendal30/conda_envs/lhm/bin/python3.13 tools/test_tiers.py for --range 2a3ec47e..30ba0559 AGENTS.md
/Users/kendal30/conda_envs/lhm/bin/python3.13 tools/test_tiers.py for --range 2a3ec47e..30ba0559 AGENTS.md CONTRIBUTING.md dev/modules/content-security.md templates/modules/team-gated/content-security.md
/Users/kendal30/conda_envs/lhm/bin/python3.13 tools/test_tiers.py check
```

Tier-map validation passed: 132 test files in 5 tiers. Syntax parsing of both
Python files, plan `claim_check.py`, and `git diff --check` passed before the
implementation commit. No full suite, certification, gate-anchor fetch or
trust operation was run. This is bounded iteration evidence only; C1-C4,
independent ordinary and Security code reviews, and final wide Boundary B
remain open. Elapsed for the overall implementation step: unknown.

## Implementation log -- C1 cost profile -- Codex -- 2026-11-04

**Measured bytes**: `27b7eb9f` in a separate clone, clean before and after;
Python 3.13.13 at the canonical interpreter. The existing gate anchor was
explicitly fetched from the local source; no source or authority ref moved.
The dated slow-family inventory remains board item 2a at that commit. This
measurement covers one upgrade family, not a remeasurement of that inventory.

```sh
python3.13 -m cProfile -o /private/tmp/cairn-c1-upgrade-profile.pstats -m pytest bootstrap/tests/test_upgrade_module_additions.py --quality-gate-shuffle-seed=0 --durations=0 --durations-min=0 -q
```

All 60 nodes passed in 30.69 seconds; the instrumented process recorded
31.438 seconds. Pytest's runner spent 0.049 seconds in setup, 30.324 in call
and 0.006 in teardown. Preparation inside test bodies is still preparation:
51 `_install` calls consumed 3.638 cumulative seconds. The larger cost was
1,978 `_three_way_merge` calls, 17.514 cumulative seconds; all 2,274
`subprocess.run` calls consumed 18.168 seconds. These nested measurements
overlap and must not be summed. Profiling adds overhead; this is a cost
diagnosis, not a before/after speedup claim.

A profiled run of
`test_repin_ceremony.py::test_a_full_ceremony_signs_once_with_the_typed_passphrase`
failed in the restricted environment at the throwaway signer's passphrase
step (9.02 seconds; setup 0.81, call 7.47). Repeating that unchanged node
with terminal access and without profiling passed in 8.09 seconds (setup
0.66, call 7.39). Both used only scratch keys and repositories. The failed
run is not green evidence or a basis for a performance comparison.

No cache, engine shortcut, timeout reduction or test removal follows from
these observations. The withdrawn preparation experiment remains withdrawn;
the next consolidation must address measured work while retaining the real
merge, signing and refusal assertions. No full suite, private usage-log
sample, certification or human ceremony ran. Other families, isolated fault
controls, comparable seed trials, tier relocation, reviews and final wide
Boundary B remain open. **Elapsed**: approximately 12 minutes for inspection
and the scoped measurements; **Tokens**: unknown.

## Prose verification -- parent-reported -- 2026-11-04

The parent reported a clean committed `0be476fd` copy under Python 3.13.13.
The selector named zero test files for this plan. Claim, link, content and
snippet gates passed on the plan; neutrality passed with informational output
only. No suite ran. Elapsed and tokens: unknown.

## Implementation verification -- Codex Luna (Implementation, low) -- 2026-11-04 -- committed ceremony slice

**Tested commit**: `e0cd2df2d1f2533279cb3dde8ddc4515757d3dd0`; **Reviewed range**:
`b0de365cdc5926f0b17a6b40aadd58adc8f2a128..e0cd2df2d1f2533279cb3dde8ddc4515757d3dd0`.
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python
3.13.13. **Pre-run state**: `/private/tmp/cairn-e0cd-verification` clean at
`e0cd2df2d1f2533279cb3dde8ddc4515757d3dd0`. **Post-run state**: clean, same
`HEAD`. Test source SHA-256: baseline `b0de365`
`e46a2569fe86bcd20b4abe37f09dc446f1ebf1e16db22cc27c3b2b417f470c50`;
candidate `e0cd2df2`
`f4a49df82646edb942b3dd4a42f98d39bc167e54f6db499fa16667315475c8cb`.
No local trusted anchor was needed or fetched; no authority ref, real repository
or real key was written. All ceremonies used disposable repositories and keys
with terminal access. **Boundary B mode**: wide, not run; it remains due after
review.

**Seven-node retention and fault map** (each old node remains the same node):

| Node | Retained assertion / fault |
|---|---|
| `test_a_full_ceremony_signs_once_with_the_typed_passphrase` | One prompt, new anchor equals tip and differs from old anchor, `%G?` is `G`. |
| `test_the_end_prints_both_ids_the_record_and_the_push_line_and_runs_no_push` | Record digest and push instruction, scan before stage two, no push, audit sees child processes. |
| `test_each_stage_one_disclosure_appears_in_the_output` | Every stage-one disclosure appears; deleting each line fails its named check. |
| `test_summary_two_shows_each_disclosure` | Every Summary 2 disclosure appears; deleting each line fails its named check. |
| `test_the_record_names_its_contents` | Typed yes answers, launcher/package/key facts, verified anchor, stage-two result, matching record digest and no passphrase. |
| `test_nothing_in_a_ceremony_tells_anyone_to_load_the_key` | Required key-away wording appears, unsafe load instructions stay absent; line-removal control fails. |
| `test_driver_runs_stage_two_with_only_its_short_environment` | Real stage two succeeds with exactly `HOME`, `PATH`, `TERM`, `LANG`, no `SSH_AUTH_SOCK`, and the expected shell arguments. |

The provisional pre-commit candidate, patched only in a scratch copy of
`b0de365`, passed 7/7 for seeds 0 and 1 in 8.51s and 8.39s; its clean
`b0de365` baseline passed 7/7 in 51.89s and 51.36s. Those candidate timings
were provisional. Replaying the committed `e0cd2df2` candidate passed 7/7
with the same seven collected node IDs in 8.17s (seed 0) and 7.93s (seed 1).
Against the committed baseline figures, this selection's mean fell from
51.625s to 8.05s (84.4%); these are scoped timings, not a suite claim.

The committed replay command used the seven node IDs in the table above with
`--quality-gate-shuffle-seed=0 --durations=0 --durations-min=0 -q`; the same
command was repeated with seed `1`.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| Seven-node replay, seed 0 | 0 | 7 passed; same seven IDs | 8.17s | unknown |
| Seven-node replay, seed 1 | 0 | 7 passed; same seven IDs | 7.93s | unknown |
| Committed `tools/test_tiers.py for` command below | 0 | 7 files selected | 0.7s | unknown |
| Seven-file mapped pytest command below, seed 0 | 0 | 543 passed, 0 failed, 0 skipped | 663.13s wall | unknown |

**Mapped iteration**. The committed selector command
`/Users/kendal30/conda_envs/lhm/bin/python3.13 tools/test_tiers.py for bootstrap/tests/test_repin_ceremony.py CHANGELOG.md dev/plans/2026-11-04-suite-consolidation.md`
selected exactly these seven files: `bootstrap/tests/test_board_json_contract.py`,
`bootstrap/tests/test_quickstart_sequence.py`,
`bootstrap/tests/test_repin_ceremony.py`, `bootstrap/tests/test_scaffold.py`,
`bootstrap/tests/test_upgrade.py`,
`bootstrap/tests/test_upgrade_module_additions.py`, and
`bootstrap/tests/test_verify_ref.py`.

```sh
/usr/bin/time -p /Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest bootstrap/tests/test_board_json_contract.py bootstrap/tests/test_quickstart_sequence.py bootstrap/tests/test_repin_ceremony.py bootstrap/tests/test_scaffold.py bootstrap/tests/test_upgrade.py bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_verify_ref.py --quality-gate-shuffle-seed=0 --maxfail=1 --durations=0 --durations-min=0 --junitxml=/private/tmp/cairn-e0cd-mapped.xml -q
```

Exit 0; 543 passed, 0 failed, 0 skipped; pytest 662.63s, wall 663.13s.
JUnit: `/private/tmp/cairn-e0cd-mapped.xml`; captured output:
`/private/tmp/cairn-e0cd-mapped.log`. Summed setup/call/teardown phase time by
file: `test_repin_ceremony.py` 599.54s, `test_upgrade.py` 28.88s,
`test_upgrade_module_additions.py` 22.36s, `test_verify_ref.py` 7.65s,
`test_quickstart_sequence.py` 1.53s, `test_board_json_contract.py` 0.87s,
`test_scaffold.py` 0.63s. The first three exceed the 10s per-file diagnostic
and belong on the test-consolidation list, slowest first. The 663.13s run
exceeded the 3-minute integration timing target; timing is diagnostic, not a
blocker. No full suite or certification ran.

**Non-pass disposition**: none in the committed replay or mapped iteration.
The three intentional mutation failures below are expected fault-kill outcomes,
not candidate failures. **Plan-specific acceptance commands**: the committed
seven-node replay, the actual selector for all three changed paths, the full
seven-file mapped run, and the three retained-node mutations below. **Known
omissions**: other C1 families and C2 mappings, full-suite certification, and
post-review Boundary B remain open.

**C2 fault controls**. Each was applied only in a separate scratch copy of
`e0cd2df2`; the named existing node ran a valid real scratch ceremony (code
0) and failed at the intended assertion. No candidate code was committed:

| Scratch-only mutation | Existing node and observed kill |
|---|---|
| Print 64 zeroes instead of the actual record digest in `scripts/repin.py`. | `test_the_record_names_its_contents` failed the actual record-digest assertion; 1 failed in 9.32s. |
| Add `CAIRN_CONSOLIDATION_MUTANT=1` to the stage-two child environment. | `test_driver_runs_stage_two_with_only_its_short_environment` failed the exact environment allowlist; 1 failed in 9.00s. |
| Replace only `STAGE 1 COMPLETE` in `_gate_preflight.py` with `STAGE 1 DONE`. | `test_each_stage_one_disclosure_appears_in_the_output` reported that disclosure missing; 1 failed in 9.35s. |

The earlier child profile `/private/tmp/cairn-c1-child-profile.pstats` is
separate evidence from commit `2bf9fb46`: source 1-pass 9.16s and instrumented
1-pass 8.88s. Instrumentation and the single sample mean it is not a speedup
claim. **Boundary B** remains owed after review (wide); ordinary and Security
code reviews remain owed. C1's full family ranking and other families, C2's
remaining family mappings, C3 and C4 remain open. This record does not complete
C1-C4; each criterion remains open. **Elapsed**: mapped run 11m03s, committed
replays 8.17s/7.93s, mutation probes 9.32s/9.00s/9.35s; total authoring
elapsed unknown. **Tokens**: unknown.

## Implementation log -- C1 family inventory and reuse triage -- Codex Luna (Implementation, low) -- 2026-11-04

**Inventory basis**: committed `dev/PLANNING.md` item 2a plus structured
`testcase` totals from `/private/tmp/cairn-v061-8d7448e1-cert.xml`,
`/private/tmp/cairn-v061-977b5250-cert.xml` (the supplied short path
`/private/tmp/977b5250-cert.xml` is absent), C1 JUnit files
`/private/tmp/c1-mapped-seed0.xml` and `/private/tmp/cairn-e0cd-mapped.xml`,
and the named 2c batches in the archived plan. Python 3.13.13's standard XML
parser found 20 files over 10s in `8d7448e1` and 24 in `977b5250`; the earlier
mapped set adds three names, two already among those 24. C1/2c reports add no
other distinct family. **Union: 25 files.** Ranks 1-24 below follow the
`977b5250` total file-time order; `test_security_marker.py` is earlier-mapped
only and is not ranked against that full-run sample. These are total JUnit
node/file times; the XMLs do not expose setup/call splits, so those components
are unknown. The `977b5250` run's one failure remains as recorded on the board;
its timing is not clean-certification evidence.

The source scan used Python 3.13.13 AST plus targeted fixture/helper sections.
Call figures below are static source call sites, not runtime execution counts.
“No extra share evident” means source inspection only, not that a family is
consolidated or may be narrowed.

| Rank / evidence | Family | Existing preparation and repeated work | Bounded reuse signal |
|---|---|---|---|
| 1 | `test_repin_ceremony.py` | Module `ceremony_template` and `ordinary_ceremony_observation`; function `cbed`; 38 `full_run` call sites. | The seven ordinary successes already share one observation; retain independent mutable/refusal beds. |
| 2 | `test_gate_preflight.py` | Module `_live_report`; `_repo` and `_closure_repo` builders; 160 `_run` call sites. | `_live_report` is already shared; candidate repositories encode distinct authority states. |
| 3 | `test_repin.py` | Module `template`, function `bed`; 71 `bed.run` CLI call sites. | Immutable template is already shared; each operation mutates its own bed. |
| 4 | `test_gate_manifest.py` | Module `produced` calls `G.produce` once (one full collection); 17 `G.verify` call sites, seven `_collect` monkeypatch sites and six `do_collect=False` calls. | Inspect identical read-only manifest/hash inputs; retain every `G.verify` path and its real collector. Four call sites use the default collection path, but early returns mean actual `_collect` entries are unmeasured. |
| 5 | `test_reanchor.py` | Function `bed`, `staged`, `ceremony`; `_run` wrapper has 64 call sites. | Fresh Git/ref state is central to each case; no shared mutable repo candidate. |
| 6 | `test_security_net.py` | Function `engine`, `perturbed`, `serve`; local network responder helpers. | Engine perturbations and server behaviors vary by case; no clear shared live state. |
| 7 | `test_upgrade.py` | No pytest fixture; `_install` helper has 89 call sites and integrity `verify` 14. | Each `tmp_path` carries a different merge/install state; no common result to reuse. |
| 8 | `test_upgrade_refuses_hostile_project_data.py` | Imports module `pristine` install and function `world` from the containment family; 35 `upgrade` call sites. | Keep each hostile project and real CLI action separate; the pristine base is already shared. |
| 9 | `test_upgrade_edit_check_runs_no_project_programs.py` | Module `pristine_install`; function `project`/`repo`; autouse Git-version reset; 15 `_upgrade` call sites. | Base install is shared; project Git configurations and edit states remain per-case. |
| 10 | `test_upgrade_removes_retired_files.py` | Module `pristine_install`; function `project`/`branch`; 23 `_upgrade` and seven `verify` call sites. | Retired-file provenance and branch mutations differ; keep independent project copies. |
| 11 | `test_security_stack.py` | Module `csr`, `cscan`, `orch`, `orchb`; function `_tampered_tree`; separate install/run helpers. | Existing fixtures already share prepared tools; tampered trees stay independent. |
| 12 | `test_upgrade_module_additions.py` | No pytest fixture; `_install` has 30 AST call sites. | C1 profile at `27b7eb9f` found 1,978 `_three_way_merge` calls (17.514s cumulative) and 2,274 `subprocess.run` calls (18.168s cumulative) across its 60-node profile; call/merge work, not imports, dominates. Keep variant merges real. |
| 13 | `test_portable_security_sweeps.py` | Function `sweep_target`, `installed`, `bindir`; 27 subprocess and 19 `run_runner` call sites. | Fake tools and environments vary; retain each isolated target. |
| 14 | `test_security_check.py` | Function fixture `repo`; `_repo_with_malformed_reachable_object` builder; 19 subprocess call sites. | Each Git history and scanner finding is case-specific; no common output identified. |
| 15 | `test_security_finding_confidentiality.py` | Function `tmproot`, `serve`; 26 install-helper call sites. | Secret/policy responses are deliberately distinct; keep isolated roots and servers. |
| 16 | `test_ceremony_review_report.py` | No fixture; `_make_range` has 33 and `_report` 32 call sites; each builds a two-commit repo. | Candidate: inspect common immutable anchor bytes only; report ranges and planted lines differ. |
| 17 | `test_gate_reanchor.py` | `_two_stage_repo`, `_author_A`, `_fake_oracle`, `_fake_produce`; three `R.M.produce` call sites. | Two-stage authority/ref state varies; no reusable completed transaction. |
| 18 | `test_web_hosting_security.py` | Function `serve`, `ca`; 21 `run_facade` call sites. | TLS endpoints and response modes vary; retain per-case server state. |
| 19 | `test_oracle.py` | No fixture; `_engines`, `_copy_target`, `_git_init_target`; five subprocess call sites. | Candidate trees and expected oracle outcomes differ; no common result to share. |
| 20 | `test_broad_run_guard.py` | `_tree` builds a fresh pytest tree; `_run` has 31 call sites across 21 cases. | Each invocation varies file breadth/hooks/errors; cache would bypass the real session behavior. |
| 21 | `test_upgrade_added_slots.py` | Module `installed`; function `scenario`; 17 `upgrade` call sites and each scenario makes a release-B template copy. | The installed base is already module-shared; edited release and project remain separate. |
| 22 | `test_upgrade_lockfile_path_containment.py` | Module `pristine`; function `world`; 15 `upgrade` call sites across lockfile actions. | Reuse only the pristine install; each planted path attack needs its own world. |
| 23 | `test_intents_tool.py` | Module `_ISOLATED_HOME`; `_git_repo` and `_run_tool`; 94 tool-run and 36 subprocess call sites. | Environment is already shared; ledger, hook and identity mutations must remain isolated. |
| 24 | `test_api_access_security.py` | Function `serve`; 26 `run_facade` call sites. | API policy/response cases use distinct local responders; no common live response. |
| Earlier mapped | `test_security_marker.py` | `_collect` has six real `pytest --collect-only` call sites with distinct marker expressions. | Keep the marker and complement collections real; caching would erase the membership check. |

**Candidate focus for parent review**: `test_gate_manifest.py` is the clearest
remaining repeated-collection/static-verification family. Its `produced`
fixture already shares one actual `G.produce` result, while the 17 `G.verify`
call sites include explicit mocked-collection and static-only controls. Consider
only whether immutable identical preparation can be reused without substituting
for any verification/collection call; no such optimization or change is
authorized here.

The child profile `/private/tmp/cairn-c1-child-profile.pstats` remains separate
from the ordinary-success before/after timings: its one-pass source sample was
9.16s and the instrumented sample 8.88s, not a speedup. The profile itself
reports 7.549s internal elapsed, 86 `subprocess.run` calls at 5.227s cumulative,
`run_ceremony` self time 2.055s and 45 compiles at 0.134s; no import optimization
is evidenced. No tests, benchmarks, network calls or private usage reads were
run for this inventory. No code, board or changelog was edited. C1-C4 remain
open; this is source triage, not evidence that all families can be consolidated.
**Elapsed**: approximately 20 minutes for inventory and source inspection.
**Tokens**: unknown.
