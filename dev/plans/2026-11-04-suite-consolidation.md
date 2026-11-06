# Plan: Consolidate the suite without losing detection

**Source proposal**: dev/proposals/archive/2026-11-02-codex-suite-consolidation.md
**Status**: awaiting-code-review
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
`bootstrap/tests/contract/test_test_tiers.py` must retain recursive discovery and
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

## Implementation log -- C1 gate-manifest profile -- Codex Luna (Implementation, low) -- 2026-11-04

On clean committed `212be448c34c2ae9e0b36f879d644de40a8d23ef`, canonical
Python 3.13.13 profiled only `bootstrap/tests/test_gate_manifest.py`
(source SHA-256 `bddde7f1850f36549ad1be04bef0bab675922fa613f0d4cfa16037ad03fa40bb`):
37 passed, pytest/JUnit 18.956s, cProfile 19.684s. Runtime measured four real
`_collect` entries (10.86s cumulative), 42 `verify` calls, `subprocess.run`
15.58s, 150 `_blob_sha256` calls (1.17s), and nine target trees / 1,500
`copy2` calls (0.49s). Nested timings overlap; do not sum. Static call counts
were not runtime counts. Retain current preparation and real collection and
verification paths: copy cost does not justify a helper or cache, and the
module fixture already shares its produced result. No source, collector mock or
temporary-state framework was added. Profile, JUnit and log: `/private/tmp/cairn-gate-manifest-212be.{pstats,xml,log}`.
C1-C4 remain open; this is not global certification. **Elapsed**: unknown.
**Tokens**: unknown.

## Implementation log -- architecture iteration timings -- Codex Terra (MEDIUM) -- 2026-11-05

The architecture C1 iteration and correction runs exceeded the 30-second
iteration target. The following files exceeded the 10-second per-file target;
values are the largest summed JUnit case times observed across the separate
Python 3.13.13 runs, not a single-run ranking or certification. Slowest first:

| File under `bootstrap/tests/` | Seconds |
|---|---:|
| `test_repin_ceremony.py` | 469.54 |
| `test_gate_preflight.py` | 162.56 |
| `test_repin.py` | 144.03 |
| `test_reanchor.py` | 59.90 |
| `test_upgrade.py` | 32.74 |
| `test_upgrade_edit_check_runs_no_project_programs.py` | 25.92 |
| `test_upgrade_module_additions.py` | 25.73 |
| `test_security_stack.py` | 25.14 |
| `test_security_marker.py` | 22.12 |
| `test_upgrade_removes_retired_files.py` | 20.99 |
| `test_portable_security_sweeps.py` | 19.99 |
| `test_security_check.py` | 19.01 |
| `test_gate_reanchor.py` | 18.55 |
| `test_code_map.py` | 18.01 |
| `test_upgrade_refuses_hostile_project_data.py` | 17.96 |
| `test_intents_tool.py` | 12.03 |
| `test_gate_manifest.py` | 11.65 |

The architecture plan's iteration record names the individual JUnit files,
failures and corrections. Timing identifies candidates, not permission to
remove checks. **Elapsed**: unknown. **Tokens**: unknown.

## Implementation log -- meter reporting iteration timings -- Codex Sol (HIGH) -- 2026-11-05

The 31-file reporting selection at `46d39ef6` under Python 3.13.13 exceeded
the 30-second iteration target: 128.65 seconds wall, then 7.24 seconds for
only 14 local-listener retries. The meter plan records initial failures and
their passing retry; this is not certification or a controlled speed comparison.
These four files exceeded 10 seconds in the initial JUnit report, slowest first:

| File under `bootstrap/tests/` | Summed testcase seconds |
|---|---:|
| `test_upgrade.py` | 31.509 |
| `test_upgrade_module_additions.py` | 24.074 |
| `test_ceremony_review_report.py` | 17.725 |
| `test_portable_security_sweeps.py` | 14.503 |

All already appear in C1's inventory. These are testcase sums, not per-file
wall times or permission to remove coverage. Source report:
`/private/tmp/cairn-meter-mapped-a.xml`. **Elapsed**: unknown. **Tokens**: unknown.

## Implementation log -- architecture C2 timings -- Codex Sol (HIGH) -- 2026-11-05

The eight-file C2 selection at `29f0835f`, Python 3.13.13, passed 446 cases
in 107.47 seconds wall, missing the 30-second iteration target. Summed JUnit
case times above 10 seconds, slowest first: `test_upgrade.py` 40.885 seconds,
`test_upgrade_module_additions.py` 26.532 seconds, `test_code_map.py` 22.132
seconds. All are already in the inventory; these are not per-file wall times
or a controlled performance comparison. Evidence:
`/private/tmp/cairn-architecture-c2-a-29f0835f.xml` and the architecture plan.
**Elapsed**: unknown. **Tokens**: unknown.

## Implementation log -- continuation iteration timings -- Codex Sol (HIGH) -- 2026-11-05

At `04afb655`, Python 3.13.13, the 31-file A-C selection passed 2,083 cases
with one native-Windows skip in 235.89 seconds wall. It exceeded the iteration
target; this was not certification or a speed comparison. Summed JUnit testcase
seconds over 10, slowest first:

| File under `bootstrap/tests/` | Seconds |
|---|---:|
| `test_upgrade.py` | 51.419 |
| `test_upgrade_module_additions.py` | 41.756 |
| `test_security_stack.py` | 26.866 |
| `test_portable_security_sweeps.py` | 22.631 |
| `test_intents_tool.py` | 12.614 |
| `test_gate_manifest.py` | 12.445 |
| `test_verify_ref.py` | 12.134 |
| `test_upgrade_lockfile_path_containment.py` | 11.705 |

`test_verify_ref.py` joins the existing consolidation candidates; the others
were already inventoried. These are testcase sums, not per-file wall times.
Source: `/private/tmp/cairn-continuation-a-04afb655.xml`.
**Elapsed**: unknown. **Tokens**: unknown.

## Implementation log -- bounded C1 retired-file reuse check -- Codex Luna (Implementation, low) -- 2026-11-05

No defensible consolidation was found in `bootstrap/tests/test_upgrade_removes_retired_files.py`; the source remains unchanged. The immutable install is already prepared once by module-scoped `pristine_install`, per-process shipped template bytes are already cached by `_shipped_versions`, and every mutable project remains an independent `project` copy or explicit copy for a distinct state. The 23 `_upgrade` and seven `verify` source call sites cover distinct path, provenance, repository, or result conditions. Sharing those calls or copies would bypass the behavior under test; no extra repeated immutable setup with evidenced cost was found.

Evidence: two separate clean clones at `bbd8a405`, source blob unchanged, Python 3.13.13, same one-file selection from `test_tiers.py for bootstrap/tests/test_upgrade_removes_retired_files.py`, same command and timing settings (`--durations=0`, JUnit, seeds 0 and 1). Before: seed 0, 97 passed, 0 skipped, pytest 29.16s / wall 30.02s; seed 1, 97 passed, 0 skipped, pytest 34.06s / wall 36.31s. After: seed 0, 97 passed, 0 skipped, pytest 31.77s / wall 32.45s; seed 1, 97 passed, 0 skipped, pytest 28.69s / wall 35.28s. All 97 node identities matched across copies and seeds. No concurrent test process ran; host load was not controlled. JUnit testcase sums were 28.91/33.96s before and 31.51/28.58s after. Fixture setup's largest observed node duration was 0.39s; individual calls reached 3.92s, with the longest calls building multiple separate states in one test. The spread with identical source yields no measured preparation saving.

Old coverage remains intact: row validity and Git-blob provenance; exact committed-byte, hostile-path, replace-ref, timeout/output-cap and Git-version decisions; both deletion branches, symlink/TOCTOU/permission protections; plan classifications and no-write guarantees; and apply/removal, lock/cache cleanup, integrity, refusal, recovery and hostile Git-program controls. No node, assertion, negative case, seed control or mutable-state boundary was changed. Checks passed with no skips or failures. No performance gain is claimed. This bounded source review does not close C1/C2 or the plan; independent ordinary and Security code reviews, other mapped families, and final wide Boundary B remain owed. **Elapsed**: approximately 7 minutes. **Tokens**: unknown.

## Implementation verification -- Codex Luna (gpt-6-luna, Implementation, low) -- 2026-11-05 -- C3 unit relocation

**Authority and selection.** The signed `refs/cairn/gate-anchor` at
`977b5250abed59badd06b4940dccd39324644705` verifies (`G`). Its pinned manifest
contains the installed roster at `bootstrap/tests/fixtures/protected_test_roster.json`,
SHA-256 `188fa76d82744be571bdc7ca91a43d605776b9df5ba0ac729e2cf22af66b8cc4`.
The anchored `ordinary_test_files` inventory has 54 entries and classifies
the root-level `test_cli_module.py` as ordinary; it is absent from anchored
`protected_python_paths`. The current tier map assigns its stem to `unit`.
The other originally considered `test_config_module.py` and
`test_slotmerge_leaf.py` are protected by that anchor and were not changed.
No trust record, roster, gate manifest, or gate code was edited.

**Move and consumers.** Commit `86058d5dac9f14ae08a27d78dbd49d1c4a16e651`
moves the root-level `test_cli_module.py` to
`bootstrap/tests/unit/test_cli_module.py`. The only content change adjusts
`_PKG` from `parents[1]` to `parents[2]`; SHA-256 changes from
`f2653af6b42adb8c23af8755566c5852d3c368836b474c7ad5a5f64649b6a497` to
`0773c043c0a3a9b5d70cb9687295ed16992686125e15bdb7188af7de4d42faba`.
Search found no live explicit command using the old path. The active onboarding
plan refers to the unchanged basename; archived duration output and the pinned
gate fixture remain historical/evidence data and were not rewritten.

**Node and behavior equivalence.** Clean committed baseline `30f49f69` and
candidate `86058d5d`, both under `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13), collected five nodes each. The old-to-new mapping preserves
all suffixes exactly: `test_cli_depends_only_downward`,
`test_no_submodule_imports_cli`, `test_single_identity_and_launcher_reach`,
`test_help_description_is_preserved`, and `test_engine_init_is_a_pure_facade`.
Dropped suffixes: 0; added suffixes: 0. Source comparison confirms assertions
and test bodies are byte-identical apart from the source-root constant.

**Boundary A checks.** Both clones were clean before and after. Baseline old-path
and candidate new-path tier selectors each chose exactly the respective test
file; `tools/test_tiers.py check` passed on both (134 files, five tiers).
The old-path test passed 5/5 at seed 0 in 0.12s and seed 1 in 0.11s. The new
path passed 5/5 at seed 0 in 0.11s and seed 1 in 0.12s. Candidate
`test_test_tiers.py` passed all 16 tests in 0.39s, including recursive
subfolder discovery and changed-file selection. Four focused gate-manifest
selections expanded to 8 passed tests in 6.98s: protected-node drop,
ordinary file/node deltas, ordinary marker changes, and new skip/xfail refusal.
No broader manifest family or full suite ran. No failure, skip, or omission.

This is one bounded C3 file, not completion of C3. Ordinary and Security code
reviews and final wide Boundary B remain owed with the rest of the plan.
**Elapsed**: approximately 15 minutes. **Tokens**: unknown.

## Implementation verification -- Codex Luna (gpt-6-luna, Implementation, low) -- 2026-11-05 -- plan prose gates

On the clean committed plan revision `5dafa58a`, Python 3.13.13
`tools/test_tiers.py for dev/plans/2026-11-04-suite-consolidation.md` selected
zero test files. `scripts/claim_check.py` passed with no flags; `link_check.py`
scanned this plan with no issues; `sync_doc_snippets.py --check` found no drift.
The standing neutrality gate had zero failures and 43 informational notices;
redundancy had zero failures and one informational notice in
`bootstrap/_scaffold/upgrade.py:2080`. No plan-specific test ran because the
selector found no readers. No full suite or certification ran. **Elapsed**:
approximately 2 minutes. **Tokens**: unknown.

## Implementation log -- SMART final-check timings -- Codex Terra -- 2026-11-05

The SMART plan's final wide check at `3c6459c9` measured summed JUnit testcase
times over 10 seconds for `test_upgrade.py` (32.18 s) and
`test_upgrade_module_additions.py` (25.73 s), both already in the ranked
inventory. These are not per-file wall times or a speed comparison. The
23-file run passed 1,640 cases; see the SMART plan's verification record.
**Elapsed**: unknown. **Tokens**: unknown.

## Implementation verification -- Codex Terra (gpt-6.1-terra, Implementation) -- 2026-11-05 -- C3 two-file relocation

**Selection and authority.** Signed anchor `977b5250` verifies and its installed
roster identifies the root-level `test_merge_module.py` and
`test_cairn_prefix_links.py` as ordinary, not protected or frozen. Its manifest
records 54 ordinary entries and roster SHA-256
`188fa76d82744be571bdc7ca91a43d605776b9df5ba0ac729e2cf22af66b8cc4`.
The existing tier map assigns these files to unit and contract, respectively.
At the committed baseline, exact-name searches found only those tier patterns
among live consumers; the meter, continuation and onboarding plans did not
name either file.
Historical reports and the pinned gate fixture remain unchanged.

**Move and mapping.** Commit `ecd5db099e6ca8728492e114ef7e2552ce6ba978`
moves the root-level files to `bootstrap/tests/unit/test_merge_module.py` and
`bootstrap/tests/contract/test_cairn_prefix_links.py`. Each file differs from
its predecessor only in the one source-root depth calculation. The merge
target remains `bootstrap/_scaffold/`; the prefix test's root remains the
repository root. Their nine node suffixes map one-for-one, with none dropped or
added. For merge: `test_merge_depends_only_on_stdlib_and_the_slotmerge_leaf`,
`test_no_cycle_slotmerge_does_not_import_merge`,
`test_single_identity_across_consumers`, `test_classify_verbatim_is_not_in_merge`,
`test_parse_slots_fails_closed_on_malformation`, and
`test_three_way_merge_roundtrip_clean_and_needs_value`. For prefix links:
`test_every_cairn_prefixed_template_token_resolves`,
`test_guard_catches_a_broken_token`, and `test_placeholder_tokens_are_skipped`.
Assertions and existing negative controls are unchanged.

**Boundary A.** Baseline `3b62df74e12cdafdc3f2b6fa0fecb669ee5cdf3d` and
candidate `ecd5db099e6ca8728492e114ef7e2552ce6ba978` were separate clean
copies before and after checks, using
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13). The range
also contains two unrelated metering and onboarding plan-record commits;
the only changes to the selected test paths are the two moves described here.
Old and new `tools/test_tiers.py for` selections each named exactly their
respective two files. Candidate `tools/test_tiers.py check` passed for 134 files
in five tiers. Both old and new paths collected nine nodes. Seed 0 and seed 1
passed 9/9 on baseline in 0.15s and 0.12s, and on candidate in 0.13s and
0.12s, with no skips. Candidate `test_test_tiers.py` passed all 16 tests in
0.96s. The focused protected-drop, ordinary-delta and skip/xfail manifest
selections passed eight tests in 10.35s. The over-10-second manifest file is
already on the consolidation inventory; the time includes its collection setup.

No full suite, certification, performance comparison, trust-record edit, or
Security Review ran. This batch does not complete C3. Ordinary and Security
code reviews and final wide Boundary B remain owed for the plan. **Elapsed**:
approximately 4 minutes. **Tokens**: unknown.

## Implementation verification -- Codex Terra (gpt-6.1-terra, Implementation) -- 2026-11-05 -- C3 contract batch

**Authority and scope.** Signed anchor `977b5250` verifies. Its installed
roster, SHA-256 `188fa76d82744be571bdc7ca91a43d605776b9df5ba0ac729e2cf22af66b8cc4`,
classifies the root-level `test_certifying_run_rule.py` and
`test_verification_boundaries.py` as ordinary; neither is protected or frozen.
The existing map assigns both to contract. At the committed baseline, an
exact-name search found no live old-path command or consumer needing an update;
the existing tier patterns remain valid. Metering, continuation and onboarding
paths, historical reports, protected apparatus, and trust records were untouched.

**Mapping and preservation.** Commit `4baef010c572049e6b5130184293ae4b90ca665f`
moves the two files to `bootstrap/tests/contract/test_certifying_run_rule.py`
and `bootstrap/tests/contract/test_verification_boundaries.py`. For each old
node, insert `contract/` before the basename and leave the entire `::` suffix,
including parameter IDs, unchanged. This maps 14 and 50 nodes respectively:
64 before and after, zero added or dropped. Collected node lists are in
`/private/tmp/cairn-c3-contract-baseline-nodes.txt` and
`/private/tmp/cairn-c3-contract-candidate-nodes.txt`. Byte comparison found
only `ROOT`'s `parents[2]` to `parents[3]` change in each file; both roots
resolve to the repository root in their respective copies. Assertions and
existing negative controls remain unchanged.

**Boundary A.** Baseline `9f16eb30865e99ba3d86ed537147bf60176d4f9c` and
candidate `4baef010c572049e6b5130184293ae4b90ca665f` were clean before and
after checks in separate copies, using
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13). The range
also includes unrelated parent changelog commit `b7a7a2aa`; only the two
test moves above change the selected paths. Baseline and candidate
`tools/test_tiers.py for` each selected exactly their respective two files;
candidate `tools/test_tiers.py check` passed for 134 files in five tiers.
Seed 0 and seed 1 each passed all 64 nodes: baseline 0.13s and 0.11s;
candidate 0.15s and 0.13s, no skips. Candidate `test_test_tiers.py` passed
16 tests in 0.61s. Focused gate-manifest protected-drop, ordinary-delta and
skip/xfail selections passed eight tests in 9.45s.

No full suite, certification, performance comparison, trust-record change,
or Security Review ran. C3 remains open; ordinary and Security code reviews
and final wide Boundary B remain owed. **Elapsed**: approximately 3 minutes.
**Tokens**: unknown.

## Implementation verification -- Codex Terra (gpt-6.1-terra, Implementation, low) -- 2026-11-05 -- C3 policy contract batch

**Authority and scope.** Signed anchor `977b5250` verifies. Its installed
roster, SHA-256 `188fa76d82744be571bdc7ca91a43d605776b9df5ba0ac729e2cf22af66b8cc4`,
classifies the root-level `test_comprehension_floor.py` and
`test_stewardship_rules_ship.py` as ordinary; neither is protected or frozen.
The existing tier map assigns both to contract. The only live old-path command
found was in the comprehension test's docstring; it was updated with the move.
Historical records, protected apparatus, and trust records were not edited.

**Mapping and preservation.** Commit `5a45a338cb643510fcbd71143d96ceb6d9d01c8b`
moves the files to `bootstrap/tests/contract/test_comprehension_floor.py` and
`bootstrap/tests/contract/test_stewardship_rules_ship.py`. Insert `contract/`
before each old node's basename and preserve the entire `::` suffix, including
parameter IDs: 10 and one nodes respectively, 11 before and after, zero added
or dropped. Node lists are in `/private/tmp/cairn-c3-floor-baseline-nodes.txt`
and `/private/tmp/cairn-c3-floor-candidate-nodes.txt`. Byte comparison found
only the two root-depth adjustments and the documented pytest command path;
both roots still resolve to the repository root. Assertions are unchanged.

**Boundary A.** Baseline `7da64a9180688bd156b1630ad09972806992611c` and
candidate `5a45a338cb643510fcbd71143d96ceb6d9d01c8b` were clean before and
after checks in separate copies, using
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13). The range
also includes unrelated parent board commit `d990688b`; only the two test
moves above change the selected paths. Baseline and candidate
`tools/test_tiers.py for` selected exactly their respective two files;
candidate `tools/test_tiers.py check` passed for 134 files in five tiers.
Seed 0 and seed 1 each passed all 11 nodes: baseline 0.45s and 0.17s;
candidate 0.21s and 0.19s, no skips. The updated documented pytest command
separately passed all 10 comprehension nodes in 0.06s. Candidate
`test_test_tiers.py` passed 16 tests in 0.50s. Focused gate-manifest
protected-drop, ordinary-delta and skip/xfail selections passed eight tests in
8.70s, including their collection setup.

No full suite, certification, performance comparison, trust-record change,
or Security Review ran. C3 remains open; ordinary and Security code reviews
and final wide Boundary B remain owed. **Elapsed**: approximately 3 minutes.
**Tokens**: unknown.

## Implementation verification -- Codex Terra (gpt-6.1-terra, Implementation, low) -- 2026-11-05 -- C3 shipped-policy batch

**Inventory and authority.** At committed baseline `725a23ab`, the signed
`977b5250` anchor verifies and its installed roster SHA-256 is
`188fa76d82744be571bdc7ca91a43d605776b9df5ba0ac729e2cf22af66b8cc4`.
The candidate roster bytes match that identity. Applying the anchored
`_ordinary_test_files` membership rule to committed root-level tests and
excluding the manifest's frozen paths yields 49 unmoved ordinary files: 47
in the anchored ordinary inventory and two added since the anchor. This is
membership, not a claim that every file is safe to move. The pre-batch list,
by the existing tier map, is:

| Tier | Root-level ordinary test basenames at baseline |
|---|---|
| Contract (14) | `test_agreement_retired.py`, `test_core_dev_folders.py`, `test_doc_governance.py`, `test_lockfile_provenance.py`, `test_model_tier_rule_ships.py`, `test_python_floor.py`, `test_review_and_verification_rules_ship.py`, `test_review_stance_in_shipped_files.py`, `test_review_sweep_ships.py`, `test_scientific_check_guidance_ships.py`, `test_scope_reduction_trap.py`, `test_skill_contract.py`, `test_test_tiers.py`, `test_writing_rules_ship.py` |
| Integration (23) | `test_check_cairn_counts.py`, `test_claim_check_allow_config.py`, `test_coordination_broad_intent.py`, `test_deleted_tracked_markdown.py`, `test_documentation_plan_module.py`, `test_drift_surfacing.py`, `test_evolution_infer.py`, `test_gauge.py`, `test_incident_trackers_module.py`, `test_install_report_slots.py`, `test_issue_capture_bootstrap.py`, `test_link_check_exclusions.py`, `test_model_selection_stub.py`, `test_module_roster.py`, `test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`, `test_practice_modules.py`, `test_prune_tools.py`, `test_quality_gate_redundancy.py`, `test_reference_scripts.py`, `test_skills_matrix.py`, `test_skills_onboarding.py`, `test_verify_stems.py` |
| Security (4) | `test_check_release_publication.py`, `test_code_map.py`, `test_git_interpreter_binding_portable.py`, `test_loop_fidelity_gate.py` |
| Unit (3) | `test_claim_check_module.py`, `test_module_merge.py`, `test_upgrade_module.py` |
| Workflow (5) | `test_first_session_report.py`, `test_install_time_onboarding.py`, `test_presets.py`, `test_profiles_smoke.py`, `test_quickstart_sequence.py` |

`test_gauge.py` and `test_code_map.py` were added after the anchor; the
installed rule classifies them as ordinary because they are not rostered as
protected. The four contract files moved below were in the anchored ordinary
inventory and absent from its protected and frozen sets. After this batch, 45
of the listed files remain at the root; C3 is not exhausted.

**Mapping and consumers.** Commit `9be9faba5dfe6f4e5c8719fc278fbdd1c7e942d7`
moves `test_model_tier_rule_ships.py`,
`test_review_and_verification_rules_ship.py`,
`test_scientific_check_guidance_ships.py`, and `test_writing_rules_ship.py`
to their existing contract tier under `bootstrap/tests/contract/`. Insert
`contract/` before each old node's basename and retain the entire `::` suffix,
including parameter IDs. The four files map 10, 104, one and 14 nodes: 129
before and after, none added or dropped. Node lists are in
`/private/tmp/cairn-c3-shipped-baseline-nodes.txt` and
`/private/tmp/cairn-c3-shipped-candidate-nodes.txt`. Byte comparison found
only four root-depth adjustments and two in-file pytest command paths; all
roots still resolve to the repository root and assertions are unchanged. The
onboarding plan's basename reference and historical reports remain unchanged.

**Boundary A.** Baseline `725a23ab942e5beca9696a029885768a25bb68a9` and
candidate `9be9faba5dfe6f4e5c8719fc278fbdd1c7e942d7` were separate clean
copies before and after checks, using
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13). The range
changes only the four test paths described above. Baseline and candidate
`tools/test_tiers.py for` each selected exactly their four respective files;
candidate `tools/test_tiers.py check` passed for 134 files in five tiers.
Seeds 0 and 1 each passed all 129 nodes: baseline 0.89s and 1.32s; candidate
0.84s and 0.98s, no skips. The two updated documented commands separately
passed 104 and one tests. Candidate `test_test_tiers.py` passed 16 tests in
0.43s; focused protected-drop, ordinary-delta and skip/xfail manifest controls
passed eight tests in 7.69s, including collection setup.

No full suite, certification, performance comparison, trust-record change,
or Security Review ran. C1, C2 and C3 remain open; ordinary and Security code
reviews and final wide Boundary B remain owed. **Elapsed**: approximately
6 minutes. **Tokens**: unknown.

## Implementation verification -- Codex Terra (gpt-6.1-terra, Implementation, low) -- 2026-11-05 -- C3 checker integration batch

**Authority and selection.** The signed `977b5250` anchor verifies; its
installed roster has SHA-256
`188fa76d82744be571bdc7ca91a43d605776b9df5ba0ac729e2cf22af66b8cc4`.
The eight files below are in its ordinary inventory, absent from its protected
and frozen sets, and assigned to integration by the existing tier map. At
candidate `6ff4a96e`, 37 of the 45 root-level effective ordinary files listed
at `a41e87c7` remain at the root; this is not a claim that each can be safely
moved. Protected tests and trust records were not edited.

**Mapping and consumers.** Commit `6ff4a96edad2cc0058b39221a6e9cad399f78170`
moves these root-level tests into `bootstrap/tests/integration/`:
`test_check_cairn_counts.py` (4 nodes), `test_claim_check_allow_config.py` (4),
`test_deleted_tracked_markdown.py` (16), `test_evolution_infer.py` (22),
`test_link_check_exclusions.py` (18), `test_prune_tools.py` (27),
`test_quality_gate_redundancy.py` (12), and `test_verify_stems.py` (15).
Insert `integration/` before each old node's basename and retain its entire
`::` suffix and parameter IDs: 118 nodes before and after, none added or
dropped. Node lists are in `/private/tmp/cairn-c3-checkers-baseline-nodes.txt`
and `/private/tmp/cairn-c3-checkers-candidate-nodes.txt`. Byte comparison found
only eight existing root-depth adjustments and six in-file command paths.
All roots and existing import-path targets still resolve to the same repository
locations; assertions and existing controls are unchanged. A live old-path
search found no remaining command or import, with the six new commands as a
known-positive search. Historical reports and onboarding basename references
remain unchanged.

**Boundary A.** Baseline `595a280b851b6c14acd0e6427752cc7c15cc0a44` and
candidate `6ff4a96edad2cc0058b39221a6e9cad399f78170` were separate clean
copies before and after checks, using
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13). The range
also includes unrelated continuation-review record `fe6b9481`; only the eight
moves above change the selected test paths. The existing claim-check config
test temporarily moved and restored its config in each isolated copy; it did
not touch the shared tree. Baseline and candidate `tools/test_tiers.py for`
each selected exactly their respective eight files; candidate
`tools/test_tiers.py check` passed for 134 files in five tiers. Seeds 0 and 1
each passed all 118 nodes: baseline 3.76s and 3.78s; candidate 6.39s and
5.09s, no skips. The six updated commands each passed independently: 4, 16,
22, 18, 27 and 15 tests. Candidate `test_test_tiers.py` passed 16 tests in
0.54s; focused protected-drop, ordinary-delta and skip/xfail manifest controls
passed eight tests in 8.87s, including collection setup.

No full suite, certification, performance comparison, trust-record change,
or Security Review ran. C1, C2 and C3 remain open; ordinary and Security code
reviews and final wide Boundary B remain owed. **Elapsed**: approximately
6 minutes. **Tokens**: unknown.

## Implementation log -- Codex Terra (gpt-6.1-terra, Implementation, low) -- 2026-11-05 -- C1/C2 reuse probes

**Result.** No defensible source change was found in this pass. C3 moves were
paused by the coordinator. The gate-manifest test source at `6d3faafc` still
has the earlier profiled SHA-256
`bddde7f1850f36549ad1be04bef0bab675922fa613f0d4cfa16037ad03fa40bb`.
Its module fixture already shares production; the four real collection paths
remain distinct, and caching or replacing them would forfeit real collection
evidence. The earlier measured copy cost was small relative to collection.

**Upgrade setup probe.** In a clean copy of `6d3faafc`, canonical Python
3.13.13 ran five ordinary fresh installs from
`test_upgrade_module_additions.py` into different empty, non-Git targets, then
five independent copies of the first. Each had 123 entries; relative paths,
file hashes, modes, symlink targets and regular-file link counts matched. Fresh-install
seconds were 0.0578, 0.0495, 0.0475, 0.0483 and 0.0487; copy seconds were
0.0266, 0.0360, 0.0252, 0.0247 and 0.0238. This is a narrow setup probe, not
an end-to-end speedup or proof for pre-seeded, Git, hardlink or hostile targets.
The family has explicit hardlink and refusal cases that require their own
real setup. The five changelog helper call sites alone do not establish enough
saving to justify a new shared preparation mechanism.

**Ceremony-report prototype.** The 24 existing planted-line, shell-command
and prose-control nodes use two repeated anchor inputs. On a clean `6d3faafc`
copy they passed at seeds 0 and 1 in 16.28s and 20.63s. A scoped cProfile run
passed them in 22.41s: 24 `_make_range` calls took 7.982s cumulative and 24
real `_report` calls took 13.789s cumulative; 648 subprocess calls took
20.899s cumulative. These nested figures overlap. The 20.63s one-file
selection exceeds the 10s diagnostic; this file is already in the ranked
consolidation inventory. The instrumented run is not a timing comparison.

A disposable, separately committed prototype `cb51d5e5` stored the two anchor
repositories as immutable bytes, materialized a separate repository for each
case, and kept real candidate commits and report calls. Its same 24 node IDs
and assertions passed at seeds 0 and 1 in 18.45s and 17.90s; two additional
fresh-versus-snapshot and ref-isolation controls passed in 5.70s. Host load
and concurrent processes were not measured. These mixed figures do not show a
reliable useful gain, and the extra controls and 75 added lines would add cost
and protected-test maintenance. The prototype was not applied to the shared
tree; it is not a completed consolidation or a review. No fault-injection
mutations were run for the discarded prototype. Its clean test copy is
`/private/tmp/cairn-c1-report-prototype-check-cb51`; profile and output are
`/private/tmp/cairn-c1-ceremony-report-6d3faafc.pstats` and
`/private/tmp/cairn-c1-ceremony-report-profile.log`.

**Next candidate.** Profile the higher-ranked `test_upgrade.py` family,
starting with a small `TestAdoptModule` selection: its `_install` helper has
89 static call sites across the file, while each adopter and refusal state
must remain independent. Measure actual setup versus merge work and separate
direct install assertions from setup-only uses before proposing reuse; the
expected gain and cross-path equivalence remain unmeasured. No full suite,
trust-pin change, certification or Security Review ran. C1, C2 and C3 remain
open, as do ordinary and Security reviews and final wide Boundary B.
**Elapsed**: approximately 8 minutes. **Tokens**: unknown.

## Implementation log -- Codex Terra (gpt-6.1-terra, Implementation, low) -- 2026-11-05 -- C1 adoption and re-anchor profiling

**Result and ranking.** No source change is delivered. The onboarding plan's
mapped candidate iteration reports `test_reanchor.py` at 97.05s and
`test_upgrade.py` at 78.77s in per-file phase sums, followed by the edit-check
and module-addition upgrade families at 50.79s and 50.54s. That run recorded
failures and a skip, so those are diagnostic observations, not clean or
comparable performance baselines. They support examining the higher-ranked
re-anchor family next without changing the accepted ranking or review gates.

**Adoption preparation.** On clean committed baseline `2e611ddf`, canonical
Python 3.13.13 collected and passed all 15 `TestAdoptModule` nodes at both
seeds. An instrumented run passed 15 in 5.06s: 14 `_install` calls consumed
2.979s cumulative and 20 `_cmd_adopt_module` calls consumed 0.329s; these are
profile figures, not a timing comparison. A separate five-target setup probe
found 111 identical entries across fresh empty non-Git installs and extracted
copies, comparing paths, contents, modes, symlinks and regular-file link counts.
The probe does not establish equivalence for pre-seeded or hostile targets.

A disposable committed prototype, `2465c95c`, used immutable archive bytes to
prepare independent targets in 14 setup-only cases; the different-profile case
still ran its own install. All 15 original node IDs and assertions remained;
one added control compared a separate real install and corrupted one copy's
lock while another completed real adoption. On the same original 15 nodes,
baseline seed 0 and 1 wall times were 3.30s and 3.41s; prototype times were
2.19s and 2.44s, with its extra control deselected for that comparison. Including
the control, four alternating full-class pairs were baseline 3.23s versus
prototype 2.16s, 3.03s versus 2.55s, 2.26s versus 2.63s, and 2.75s versus
2.44s. All runs passed: 15 baseline or 16 prototype nodes, no skips. Host
load and concurrent processes were not measured. The mixed inclusive results,
87 added and 42 removed lines in a protected test, and untested Python 3.11
archive compatibility do not establish enough benefit for this extra machinery.
The prototype remains only in a scratch clone; no fault-injection mutation of
production code or full mapped test selection was run for it.

**Next candidate.** On the same committed baseline, eight
`test_reanchor.py::TestTheRequiredStatesRefuse::test_a_missing_executable_bit_refuses`
nodes passed with `SSH_AUTH_SOCK` unset: seed 0 took 2.64s pytest / 4.12s
wall; seed 1 took 2.99s pytest / 4.19s wall. A separate instrumented run passed
eight in 3.56s; eight `bed` fixture calls consumed 1.572s cumulative versus
0.213s for eight validation calls. The fixture's generated keys and Git refs
were synthetic and confined to per-test temporary directories. These profile
figures overlap and are not a before/after claim. Investigate only preparation
that preserves independent repositories, mutable refs, private keys and every
refusal; measure a committed candidate before claiming a gain. Profile data:
`/private/tmp/cairn-c1-adopt-profile-2e611ddf.pstats` and
`/private/tmp/cairn-c1-reanchor-bed-2e611ddf.pstats`.

No full suite, trust-pin change, certification or Security Review ran. C1,
C2 and C3 remain open, with C3 moves paused; ordinary and Security reviews and
final wide Boundary B remain owed. **Elapsed**: approximately 14 minutes.
**Tokens**: unknown.

## Implementation verification -- Codex Terra (gpt-6.1-terra, Implementation, low) -- 2026-11-05 -- C1 re-anchor bed reuse

**Source and boundary.** Source commit `5f129ccd` changes only
`bootstrap/tests/test_reanchor.py` under accepted C1/C2. The module now creates
one pristine synthetic Git checkout and public key, then copies ordinary bytes
into each test's independent checkout, `.git` directory, ref, key and home.
Every ceremony command and refusal still uses its real public entry point.
The new control mutates one copy's key and anchor ref and proves the pristine
source is unchanged. No private key survives preparation; no agent socket or
real repository ref is shared. The eight-node refusal profile at `2e611ddf`
was 8 passed in 3.56s instrumented, with eight `bed` setups at 1.572s
cumulative and eight validation calls at 0.213s; those overlapping profile
figures motivated the experiment, not a speedup claim.

**Committed-byte comparison.** On clean `c06f7b48` and scratch-committed
`055507b9` (source bytes identical to `5f129ccd`, SHA256
`4a09c82a9752efb862b3b53c47806ec4dfb0cdceebb437d96ae948247679036c`),
canonical `/Users/kendal30/conda_envs/lhm/bin/python3.13` 3.13.13,
`SSH_AUTH_SOCK` unset, the same `pytest -q bootstrap/tests/test_reanchor.py
--quality-gate-shuffle-seed=<0|1> --durations=10` yielded:

| Seed | Original | Candidate, including new control | Wall saving |
|---|---|---|---:|
| 0 | 232 passed, 71.82s pytest / 75.36s wall | 233 passed, 59.73s pytest / 60.31s wall | 15.05s |
| 1 | 232 passed, 71.94s pytest / 72.48s wall | 233 passed, 63.89s pytest / 64.41s wall | 8.07s |

Collection sets show zero dropped original nodes and exactly the new isolation
control. Original assertions and node suffixes are unchanged. The comparison
includes clean, hostile-value, symlink, missing-executable, anchored-roster,
key-rotation, ref and no-candidate-execution cases. Host contention was not
controlled: an earlier candidate wall run took 25.20s while pytest reported
1.48s. An alternating eight-node comparison accidentally reused the candidate
as its own baseline after a scratch commit and is explicitly discarded.

**Mapped checks on clean committed source.** `tools/test_tiers.py for` selected
`test_gate_preflight.py`, `test_reanchor.py`, `test_security_marker.py`. A fresh
`5f129ccd` copy initially lacked `refs/cairn/gate-anchor`; the local source's
signed `977b5250` was verified, fetched into that copy and verified there with
the installed allowed-signers file. The first mapped seed-0 run had 576 pass,
four environment failures: two absent-anchor and two blocked local `ssh-agent`
socket cases. The two anchor nodes then passed; the two socket nodes passed
with local-socket permission. With those conditions corrected, the complete
three-file selection passed 580/580 at both seeds: seed 0 372.58s pytest /
391.01s wall; seed 1 346.05s pytest / 347.02s wall. This exceeds the 30s
iteration and 10s/file diagnostic targets; it is not full-suite certification.
`tools/test_tiers.py check` passed (134 files, five tiers). Four focused
gate-manifest frozen-change, dropped-node, skip-marker and ordinary-delta
controls passed in 7.74s. All checks used the committed source copy; no
candidate source bytes changed between seeds.

**Trust and omissions.** The existing frozen pin for this protected file is
SHA256 `1edc2da2d031849d7a3763c846538478c067cdb63f1a19c26d5c4aff1d8de766`;
the committed source is `4a09c82a9752efb862b3b53c47806ec4dfb0cdceebb437d96ae948247679036c`.
This expected mismatch is unpassed and requires separate reviewed release
baseline disposition, not a repin by this implementation. No trust record,
AST baseline, configured suite member or security/refusal rule was edited.
No production-code mutation trial, full suite, certification, push, ordinary
code review, Security Review or final wide Boundary B ran. C1/C2 across other
families and C3 remain open; C3 moves stay paused. **Elapsed**: approximately
40 minutes. **Tokens**: unknown.

## Code review -- Codex GPT-5 (Reviewer, medium) -- 2026-11-05 -- C1 re-anchor fixture

Reviewed commit: 5f129ccd2bfd109ab51cb98cd8b3486d816b11a2

**Foundations**:
1. **Should this happen as framed?** Yes: the copied checkout includes its own Git directory and anchored roster, and the copied public key matches that roster; the original test bodies are unchanged -- `test_reanchor.py` diff and `_fresh_bed`/`bed`.
2. **Best alternative.** Retaining per-test generation is simpler but costs the measured 8.07-15.05 seconds per module run; the small, local copy fixture is a reasonable trade, subject to host variability -- implementation evidence at `a7552b3f`.
3. **What would show it wrong?** A later test observing another test's ref or key mutation, a mismatched anchored roster, or a missed refusal would falsify isolation; repeat the isolation and roster nodes in varied order and test a second copy after mutation -- targeted checks below.

**Verdict**: No blocking findings. The new control checks mutation against the seed, not a second copied bed; a second-copy control would strengthen the independence claim but ordinary `copytree`/`copy2` semantics and per-test paths support it. Some stage tests use staged substitutes, so passing them does not by itself establish a full live ceremony; the existing two-ref workflow exercises the real ceremony path.

**Bounding**: ACCEPTED for this source change. The mapped selection names the changed module and its preflight and security-marker readers; the author's 580-pass runs at both seeds and explicit first-run failure dispositions are recorded at `a7552b3f`. The protected-file baseline mismatch remains unpassed, Security Review is separate, and final wide Boundary B is still owed.

**Evidence**: In an archive of the reviewed commit, canonical Python 3.13.13 with `SSH_AUTH_SOCK` unset ran `pytest -q bootstrap/tests/test_reanchor.py -k 'bed_copies_keep_refs_and_keys_independent or key_absent_from_the_anchored_roster or refuses_BEFORE_a_package_is_written or roster_key_is_accepted or check_reads_the_ANCHORED_roster or every_roster_fingerprint or a_symlink_at_the_leaf or from_the_review_outputs_to_the_two_ref_transaction' --quality-gate-shuffle-seed=1`: 8 passed, 225 deselected in 6.60s. The source diff preserves all pre-existing assertions and nodes; the new control mutates key and ref but no separate production mutation was run.

**Coverage**: Read the source diff, fixture, selected ceremony paths and implementation evidence; did not independently time both versions, run the full suite, verify the signed anchor, test every refusal or perform Security Review. Elapsed: approximately 5 minutes. Tokens: unknown.

## Security review -- Codex Sol -- 2026-11-05 -- C1 re-anchor fixture

Reviewed commit: `5f129ccd2bfd109ab51cb98cd8b3486d816b11a2`. Target: `bootstrap/tests/test_reanchor.py` fixture reuse and its isolation control. Prior finding: ordinary code review `b019e5cf`, no blocker.

**Model**: gpt-6.1-sol (high). **Tier**: Security Review.
**Findings**: none blocking. **Verdict**: ACCEPT for this source change.
**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes: every test receives a copied checkout with its own Git directory and a copied public key; the measured file-level saving is 8-15 seconds across two seeds -- source diff; implementation log `a7552b3f`.
2. **Best alternative.** Retain per-test key generation and Git initialization, preserving simple isolation but keeping the measured setup cost -- original fixture at the parent of `5f129ccd`.
3. **What would show it wrong?** Sharing a mutable seed key or Git ref between cases would let one test contaminate another -- new isolation control in `test_reanchor.py`.

On a clean detached copy under Python 3.13.13, the new isolation control passed. In a separate disposable mutation, replacing the public-key copy with a hard link made that same control fail on equal inode identity. The fixture uses ordinary byte copying for `.git` and the key; the test also checks that changing the copied ref leaves the seed ref unchanged. This supports the claimed separation without replacing real ceremony calls with stubs. The existing frozen pin is mismatched and unpassed; this review grants no baseline update or release authority.

**Coverage:** Committed source diff, fixture paths, targeted clean and key-alias mutation, ordinary review and measured evidence. **Not covered:** second-copy-after-mutation control, native Windows inode behavior, every ceremony refusal, signed-anchor provenance, full suite, final wide Boundary B or re-anchor.

## Implementation log -- Codex Terra (gpt-6.1-terra, Implementation, low) -- 2026-11-05 -- C1 upgrade InitLock no-change

**Measured scope.** In a clean copy of committed `4e07610f`, canonical
`/Users/kendal30/conda_envs/lhm/bin/python3.13` 3.13.13 ran
`bootstrap/tests/test_upgrade.py::TestInitLock` with `--durations=0
--durations-min=0 --quality-gate-shuffle-seed=<0|1>`: 27 passed at each seed,
5.01s and 4.51s pytest respectively; no skips or failures. Setup and teardown
rounded to 0.00s per node; preparation is inside the calls. A seed-0 cProfile
run passed 27 in 5.56s: 30 `_install` calls took 2.003s cumulative, 18
`_migrate` calls 1.754s, 14 `_inventory_review_case` calls 1.388s, and 78
public `s.main` calls 5.336s. These are nested, not additive; profile at
`/private/tmp/cairn-c1-init-lock-4e07610f.pstats`.

**Fault and disposition.** The existing
`test_changed_historical_metadata_refuses_and_cleans_stage` plants a changed
`HEAD:bootstrap/_scaffold/config.py` Git response, drives the real upgrade
entry point, requires exit 2 and no staged area; it passed under both seeds.
The matching historical-renderer success and separate altered-renderer refusal
also passed. A shared migrated tree would bypass the real migration these
nodes exercise. Sharing only the pre-install bytes would save at most part of
the 2.003s cumulative install cost across this 27-node slice while adding a
fixture, copy and equivalence burden. No useful, low-complexity gain is
established, so no source or node change was made and no before/after speedup
is claimed. Next ranked upgrade candidate is
`test_upgrade_refuses_hostile_project_data.py` (rank 8), whose imported
module-scoped `pristine` fixture already shares one real install while each
hostile project and CLI refusal remains independent; profile any further
candidate before editing it. This does not dispose of the rest of rank 7 or
C1/C2. No full suite, trust pin, repin, push, review waiver or C3 move.
**Elapsed:** approximately 8 minutes. **Tokens:** unknown.

## Implementation log -- Codex Terra (gpt-6.1-terra, Implementation, low) -- 2026-11-05 -- C1 hostile upgrade no-change

**Measured scope.** Clean committed `1edeb4b1`, canonical
`/Users/kendal30/conda_envs/lhm/bin/python3.13` 3.13.13,
`bootstrap/tests/test_upgrade_refuses_hostile_project_data.py`: 195 passed at
seed 0 in 47.84s pytest (`--durations=0 --durations-min=0`), and 195 passed at
seed 1 in 27.35s, no skips or failures. A seed-0 cProfile run passed 195 in
53.21s: 152 function-scoped `world` copies took 8.046s cumulative, including
8.028s in recursive `copytree`; 216 real `upgrade` CLI calls took 34.804s,
within 246 subprocess calls at 38.183s. These timings overlap. Profile:
`/private/tmp/cairn-c1-hostile-upgrade-1edeb4b1.pstats`. The large seed-time
spread makes host load a material uncertainty, not a performance gain.

**Fault and disposition.** The imported module-scoped `pristine` fixture
already makes one real install and copies it into independent projects. In
`test_apply_never_creates_a_profile_through_a_link`, each planted link drives
the real upgrade CLI, requires a plain refusal and checks that the outside
snapshot and planted link remain unchanged; its four cases passed at both
seeds. Sharing a mutable world or caching the CLI outcome would skip those
distinct attacks. The only common copy cost is about 8s across 152 worlds;
no low-complexity, portable copy that preserves byte, link and mutation
isolation is established. No source or node changed and no before/after saving
is claimed. The next ranked upgrade file is
`test_upgrade_edit_check_runs_no_project_programs.py` (rank 9), whose
`pristine_install` is also module-shared. This is a bounded disposition for
rank 8 only; rank 7 as a whole and C1/C2 remain open. No full suite, trust
record, repin, push, review waiver or C3 move. **Elapsed:** approximately 6
minutes. **Tokens:** unknown.

## Implementation log -- Codex Terra (gpt-6.1-terra, Implementation, low) -- 2026-11-05 -- C1 edit-check reuse probe

**Profile and fault.** On clean `6517c76c`, canonical
`/Users/kendal30/conda_envs/lhm/bin/python3.13` 3.13.13, the 13-node failure
and positive-control cluster passed in 15.44s under cProfile. Thirteen
`_edited_project` calls consumed 7.325s cumulative, including 6.800s in
real `--stage`; thirteen project copies took 0.864s. The 26 upgrade calls
consumed 13.663s; figures overlap and do not add. Profile:
`/private/tmp/cairn-c1-edit-cluster-6517c76c.pstats`. Each failing Git step is
tested for a hang, excessive output or non-zero exit through real `--apply`,
which must refuse without overwriting the edited file; the unmodified Git
control must identify the edit. The hostile Git-config program case remains
separate and real.

**Scratch candidate.** Disposable committed `55db23f2` prepares one staged
install and independently copies it for the 12 parametrized failures; the
positive case still stages for real. Its added control compares fresh and
copied stage paths, types, modes and bytes and Git status, then mutates a copy
and checks the source; it checks distinct Git-index inodes. Collection shows
82 original nodes retained and one added control; original assertions remain.
This is not a proof of every Git or environment state, and no production-code
mutation or complete mapped selection was run for the prototype.

**Comparison and non-passes.** Whole-file baseline seed 0/1: 82 passed,
42.90s / 52.65s pytest and 43.95s / 54.59s wall. Candidate including the
control: seed 0, 83 passed, 46.59s pytest / 49.99s wall; seed 1, 82 passed
and one failed, 30.34s / 33.03s. The candidate's failed
`[last commit-over the cap]` case had an empty Git-call log; its targeted
same-tier retry passed. A separate baseline seed-0 cluster run also had an
empty log in `[index-hang]`: one targeted retry failed and the second passed;
a subsequent cluster run passed all 13. The original full-file baseline and
profile runs had passed that case. The intermittent empty-log cause is not
established and remains a reliability observation, not an excused pass or a
proven prototype defect. Host load was uncontrolled. These runs do not show a
reliable speedup with all checks passing; the 52-addition/two-deletion
prototype is discarded and no shared source changed.

Rank 10's retired-file family already has the bounded no-change record above;
rank 11 `test_security_stack.py` is the next candidate. C1/C2, remaining
families and final wide Boundary B remain open. No trust record, repin, full
suite, review waiver, C3 move or push. **Elapsed:** approximately 15 minutes.
**Tokens:** unknown.

## Implementation log -- Codex Terra (gpt-6.1-terra, Implementation, low) -- 2026-11-05 -- C1 security-stack reuse probe

**Profile.** On clean `fe3f9dbd`, canonical
`/Users/kendal30/conda_envs/lhm/bin/python3.13` 3.13.13, rank 11's
`test_security_stack.py::TestOrchestrator` passed 11 in 6.30s pytest. A
separate instrumented run passed 11 in 9.29s: eight `_adopter` calls took
3.978s cumulative; nine `_install_modules` calls took 1.845s, nine Git
commits 1.746s, and nine Git initializations 0.894s. These figures overlap;
profile: `/private/tmp/cairn-c1-security-orch-fe3f9dbd.pstats`.

**Scratch comparison.** Disposable committed `0fd579a1` copies a pristine
two-module adopter for seven cases, retains a real fresh install in the
end-to-end case, and adds an isolation control. The control compares fresh
and copied lock data and Git tree identities, checks distinct index inodes,
and proves a copied apparatus tamper refuses while a fresh copy stays clean.
It does not compare every untracked file or Git state. Collection retains all
11 original nodes and adds one control; original assertions remain. On the
same Python and class, all seed runs passed with no skips. Wall seconds,
baseline 11 nodes versus candidate 12 including control:

| Seed | Baseline then candidate | Reversed pair, candidate then baseline |
|---|---|---|
| 0 | 3.67 / 6.47 | 5.01 / 7.78 |
| 1 | 3.92 / 3.22 | 5.84 / 6.56 |

Host load was uncontrolled. One seed-0 pair is slower and the other faster;
seed-1 differences are under a second. The protected-test prototype adds 46
lines and removes 14, without a reliable useful gain; it is discarded. No
full-file mapped checks or production mutation trial ran for it. No shared
source or node changed, and no speedup is claimed. Rank 12
`test_upgrade_module_additions.py` is next; its prior profile and setup probe
remain in this plan. This bounded slice does not close rank 11 or C1/C2.
No full suite, trust record, repin, review waiver, C3 move or push.
**Elapsed:** approximately 8 minutes. **Tokens:** unknown.

## Implementation verification -- Codex Terra (gpt-6.1-terra, Implementation, low) -- 2026-11-05 -- C1 collision preparation reuse

**Source and scope.** Source commit `e8873350` changes only protected
`bootstrap/tests/test_upgrade_module_additions.py`. Fifteen existing
single-collision cases copy a module-scoped staged seed to independent target
directories; their live adoption, authorization, refusal and mutation calls
still run. The positive stage-to-adoption case still stages independently.
The new control stages a separate fresh target and compares paths, file bytes,
modes, symlink targets and regular-file link counts, then mutates the copied
lock, collision and stage metadata and checks both other trees remain unchanged.
Collection on clean copies lists all 60 original nodes plus that one control;
an AST comparison found every original test's `assert` expressions unchanged.

**Committed-byte timing.** Baseline `309b6d9a` and disposable candidate
`cbabcbef` used canonical `/Users/kendal30/conda_envs/lhm/bin/python3.13`
3.13.13, the same file and shuffle seeds, on separate clean committed copies.
Candidate test-file SHA256 is
`8c5bd5c27dd9a2ce10f4861276080e863c33d47f883210a0a6d4cac3732e9ccc`,
identical to source commit `e8873350`. All comparisons passed with no skips.
Wall seconds are shown; the 60-node candidate explicitly deselected its added
control, while the 61-node candidate includes it:

| Seed | Baseline 60 | Candidate 60 | Candidate 61 |
|---|---:|---:|---:|
| 0 | 23.49 | 21.92 | 21.48 |
| 1 | 22.70 | 21.48 | 19.87 |

An earlier disposable version `784cc201`, with the same fixture behavior and
control but a different fixture return interface, recorded inclusive baseline
versus candidate wall pairs of 23.49/20.39 and 25.68/20.64 at seed 0, and
22.70/18.70 and 25.06/19.79 at seed 1. The coordinator reported onboarding's
wide run finished before this window. One-minute load averages were 3.80,
4.24 and 3.62 on 14 logical CPUs around these trials. Later pairs on `cbabcbef`
were 27.55/23.90 and 29.40/21.88 wall, but load rose to 10.27; they are
diagnostic only, not used to establish the saving. A later process snapshot
showed system activity and no active Python test at that instant; activity
during the trials was not independently established. Do not infer a suite
speedup from this file-level comparison.

**Controls and mapped checks.** In separate committed scratch mutations,
hardlinking the seed into a case (`cc45eb4a`) made the isolation control fail
on link counts; bypassing the observed-byte digest (`9df13f4f`) made
`test_adopt_collisions_refuses_changed_bytes_despite_rewritten_stage` fail;
bypassing the upstream digest (`e1da8532`) made
`test_adopt_collisions_refuses_a_wrong_upstream_authorization` fail. These
expected failures went through the affected real entry points. The untouched
hardlink and symlink/refusal cases passed in both file runs. On a fresh clean
copy of source `e8873350`, `tools/test_tiers.py for` selected only this test
file; it passed 61/61 at seed 0 and seed 1 (20.17s and 19.58s pytest, for
correctness, not timing comparison). `tools/test_tiers.py check` passed for
134 files in five tiers. Three recursive/selector and four focused frozen,
dropped-node, skip-marker and ordinary-delta gate controls passed in 9.44s.
The source copy was clean before and after checks.

**Trust and omissions.** The installed anchor's frozen SHA256 for this test
is `8736394ae4afed7f97eecb4d8511000b7ec80ae180648de3d9de87f045294cc9`,
not the source SHA above. This expected frozen-file mismatch remains unpassed;
no manifest, roster, anchor, AST pin or other trust record was changed.
Independent ordinary and Security code reviews and final wide Boundary B
remain owed. Native Windows behavior and other fault mutations were not
measured; C1/C2 and paused C3 remain open. No full suite, certification or
push ran. **Elapsed:** approximately 20 minutes. **Tokens:** unknown.

## Implementation log -- Codex Terra (gpt-6.1-terra, Implementation, low) -- 2026-11-05 -- C1 matched collision timing

After `69ae51e1`, a further same-node comparison used the clean `309b6d9a`
baseline and clean committed source `e8873350`, canonical Python 3.13.13,
the same 60 original nodes and both shuffle seeds. The source run explicitly
deselected its new control; inclusive control runs are recorded above. Seed 0,
baseline then source: 60 passed in 25.02s / 26.27s wall versus 60 passed in
19.73s / 20.72s wall. Seed 1, source then baseline: 60 passed in 20.09s /
20.62s wall versus 60 passed in 25.06s / 25.97s wall. No skips or failures.
One-minute load average rose from 5.51 to 7.65 on 14 logical CPUs. Process
snapshots at both ends showed no obvious active Python test process, but cannot
prove absence of contention between snapshots; system activity remains a timing uncertainty.
No additional fault, full-suite, review or release check is implied by these
timings. **Elapsed:** approximately 3 minutes. **Tokens:** unknown.

## Code review -- Codex (GPT-5, Reviewer, medium) -- 2026-11-05 -- C1 collision reuse

**Verdict:** No blocking findings. Ordinary review of source `e8873350` and
evidence `69ae51e1` and `3e2d8da6`; Security Review and wide Boundary B remain owed.

**Foundations.** (1) This should proceed as framed: the diff preserves the
existing assertions and live adoption calls, and copies the staged tree for
each affected case. (2) The best alternative is retaining per-test staging;
it avoids shared setup but gives up the measured file-level time saving. The
independent fresh-tree comparison and mutation control support reuse.
(3) A copied tree that differs from a fresh stage, leaks writes, or misses an
authorization fault would show this wrong; rerun those controls when setup or
copy semantics change.

**Evidence.** Read the committed diff and evidence, including the reported
60-node collection and assertion comparison, both digest mutations, hardlink
mutation, and matched timing pairs. The latter show a file-level improvement,
not a suite-wide result, with contention uncertainty acknowledged. On a separate
archive of `e8873350`, canonical Python 3.13.13 ran the snapshot isolation and
two digest-refusal tests: 3 passed, 58 deselected in 2.09s. The diff retains a
separately staged positive path and does not alter trust controls. The frozen
test-file mismatch remains unpassed pending its named release operation.

**Coverage:** Reviewed the changed fixture, affected test diff and recorded
evidence; did not independently repeat all 60 nodes, timing trials, mutations,
native Windows behavior, Security Review or the full suite. **Elapsed:**
approximately 3 minutes. **Tokens:** unknown.

## Security review -- Codex Sol -- 2026-11-05 -- C1 collision reuse

**Assignment:** Sol, High, by the Maintainer. The review was reported before a
model transition; this record was appended by the same assistant's continuation
running gpt-6.1-terra. The earlier runtime model is not independently known.
**Tier:** Security Review. **Verdict:** No blocking findings; accept this source
change. Wide Boundary B remains owed.

**Foundations**

1. **Should this happen as framed?** Yes: per-case `copytree` preparation preserves independent mutable paths and existing assertions; adoption and refusal still call the real `s.main`, and the positive stage-to-adoption case stages independently -- source `e8873350` diff and test bodies.
2. **Best alternative.** Retain per-case staging: it avoids shared setup but keeps the file-level setup cost documented in `69ae51e1` and `3e2d8da6`, subject to their stated contention uncertainty.
3. **What would show it wrong?** A shared-file mutation, stale authorization accepted, or symlink refusal modifying its referent would falsify preservation; repeat the isolation and refusal controls when preparation or copy semantics change.

**Evidence:** On a disposable archive of `e8873350`, Python 3.13.13 ran the
snapshot, collision adoption, action-exclusion, symlink and stage-authorization
selection at shuffle seed 1: 23 passed, 38 deselected in 8.02 seconds. In that
copy, changing `copytree` to use `os.link` caused the snapshot control to fail
on link-count differences: 1 expected failure in 0.85 seconds. The source diff
retains existing assertions and live adoption calls. The frozen protected-test
pin remains mismatched and unpassed; this review grants no repin or release
authority.

**Coverage:** Source diff, isolation, authorization and refusal paths, ordinary
review `795bfbbc` and committed evidence. **Not covered:** independent timing,
production authorization mutation, native Windows, the full suite, trust
ceremonies or final wide Boundary B. **Elapsed:** approximately 5 minutes for
the review; record and commit time not measured. **Tokens:** unknown.

## Timing observations -- Codex (coordination) -- 2026-11-05 -- joined change check

The post-review onboarding/goodnight change check at `88679232`, Python
3.13.13, exceeded the three-minute integration diagnostic (621.02 seconds wall).
It is not a full-suite timing or matched before/after benchmark. JUnit testcase
phase times, summed by file, rank the observed files over ten seconds below;
this refreshes C1/C2 triage without adding a separate store or deferring a fix.
The complete outcomes and non-pass dispositions remain in the archived
onboarding verification record. No performance benefit is inferred from counts.

| File in `bootstrap/tests/` | Observed phase seconds |
|---|---:|
| `test_repin.py` | 172.61 |
| `test_reanchor.py` | 57.31 |
| `test_upgrade.py` | 32.74 |
| `test_upgrade_edit_check_runs_no_project_programs.py` | 30.50 |
| `test_security_stack.py` | 26.17 |
| `test_upgrade_module_additions.py` | 24.97 |
| `test_portable_security_sweeps.py` | 24.38 |
| `test_upgrade_removes_retired_files.py` | 22.52 |
| `test_ceremony_review_report.py` | 21.23 |
| `test_gate_reanchor.py` | 21.23 |
| `test_security_finding_confidentiality.py` | 19.89 |
| `test_upgrade_refuses_hostile_project_data.py` | 18.97 |
| `test_oracle.py` | 14.90 |
| `test_web_hosting_security.py` | 14.88 |
| `test_intents_tool.py` | 14.45 |

Prioritize remaining immutable preparation in `test_repin.py` next, preserving
independent mutable refs, paths, keys and every fault assertion. The strict
runner's committed C1 lazy-import change must be retained; do not combine its
platform policy or collector work into this plan. New timing comparisons still
need matched committed snapshots and both seeds. C1-C4 remain open as recorded;
this observation is not a review, completed optimization or certification.
Elapsed: derived from the joined check; observation processing unknown.
Tokens: unknown.

## Implementation log -- C3 eligibility refresh and two ordinary moves -- GPT-6 Luna (Implementation, Low) -- 2026-11-06

Moved the root-level gauge pulse test to
`bootstrap/tests/integration/test_gauge.py` and the root-level release-membership
contract test to `bootstrap/tests/contract/test_release_members_contract.py`.
Both destination folders already existed. Each file's only source edit changes
the root lookup from `parents[2]` to `parents[3]`; test functions, parameters
and assertions remain byte-identical. Updated the live owner reference in
`dev/plans/2026-11-04-metered-cost.md`. Its dated Boundary A command remains a
historical record of commit `46d39ef6` and was not rewritten. No external path
reference to `test_release_members_contract.py` was found.

The older 37-root-file count at `6ff4a96e` excluded only the manifest's frozen
paths (115 tracked root tests minus 78 frozen). It is not the current move
eligibility count. Applying the verified signed roster plus manifest-frozen
exclusions to that same snapshot leaves five ordinary root files: 32 of the
old 37 are excluded by the signed roster. Current `HEAD` has six before these
moves because `test_release_members_contract.py` was added later.
The fixed 590-ID native candidate also holds `test_code_map.py` and
`test_git_interpreter_binding_portable.py`, leaving four current eligible root
files before this batch. After these two moves, four ordinary root files
remain, of which two still overlap the fixed candidate. This reconciliation
does not infer that the earlier files moved; most of the count difference is
the stricter signed-roster rule.

The gate manifest contains no old node IDs for either moved file, so exact
old-to-new node mapping and both shuffle seeds remain pending in separate
committed copies after the coordinator opens the test window. No collection,
pytest, or timing run was performed. No tier pattern, `conftest.py`, board,
changelog, protected roster, or native candidate changed. **Elapsed:** unknown.
**Tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-06 -- C3 two-file moves

**Snapshots:** separate clean local clones at baseline `a1a3dc4194fcd80cc971b0c65d5f924344d58050` and candidate `73d03574b9f5b03e30f3f73af94dfac4ca942215`, Python `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13). Both clones were clean before and after checks. `tools/test_tiers.py check` passed in each: 135 files across five tiers. `tools/test_tiers.py for` selected exactly the two moved files at each snapshot.

**Node reconciliation:** exact-file collection found 64 IDs on each side. Replacing only the old two root-level prefixes with their new tier-folder prefixes makes the baseline and candidate sets equal: 64 matched, zero added or dropped, all suffixes unchanged. Captures: `/private/tmp/cairn-c3-moves-73d03574-baseline-nodes.txt` and `/private/tmp/cairn-c3-moves-73d03574-candidate-nodes.txt`. Committed-byte comparison confirms both files differ only by their `ROOT` parent depth. The existing gate-manifest ordinary-delta controls do not name either moved file, and their prior node IDs were absent from the manifest; no extra control was applicable.

**Targeted outcomes:** `env -u CAIRN_FULL_SUITE -u PYTEST_ADDOPTS PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q -rs -p no:cacheprovider --tb=short` against exactly the two files passed without skips at both seeds. Baseline seed 0: 64 passed, pytest 4.46s, wall 5.07s; candidate seed 0: 64 passed, pytest 4.51s, wall 5.05s. Candidate seed 1: 64 passed, pytest 4.47s, wall 5.01s; baseline seed 1: 64 passed, pytest 4.34s, wall 4.92s. No performance gain is inferred from this narrow pair.

No other test file, collection, full suite or timing selection was run. Independent ordinary and Security code review and final wide Boundary B remain due. **Elapsed:** approximately 4 minutes. **Tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-06 -- edit-check timeout fixture

**Change:** In `bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py`, retain the ordinary Git timeout for prelude calls and apply the short timeout only to the injected hang. Each injected fault writes its target label before acting, and the test asserts that marker alongside the existing refusal, version-order and no-write assertions. The first focused retry exposed a fixture assertion mismatch: `printf` adds a trailing newline, so exact text comparison rejected correctly written markers. Commit `23ded78f` compares marker lines to the label; it changes no product code or acceptance assertions.

**Evidence:** The original C1 run at `73aaf88d` recorded ten failures in this test family from the premature global 0.5-second budget. In a fresh clean clone of `23ded78fdd2322615f8b50c8b12d042b42f1feb3`, Python `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13) ran only `test_every_git_step_that_fails_is_cannot_tell` (all 12 parameters) and `test_the_unfailing_stand_in_lets_the_check_find_the_edit`. Seed 0: 13 passed in 13.15 seconds; seed 1: 13 passed in 15.65 seconds. Both started and ended clean. No `CAIRN_FULL_SUITE` or `PYTEST_ADDOPTS` was set; bytecode and pytest cache writes were disabled. The final focused run covers all intended injected branches and the existing positive control. No broad test selection or performance claim is made.

The intermediate retry on the pre-correction fixture had 12 failures and one positive-control pass: each failure was the marker comparison rejecting the newline, not an unreached fault branch. That evidence is retained here; it is superseded by the corrected committed-byte runs above. No product change, timeout increase, hidden skip or weakened refusal/no-write assertion was introduced.

**Coverage:** Target parametrization and positive control at seeds 0 and 1 only. **Not covered:** ordinary code review, Security Review, native Windows, full suite or final wide Boundary B; ordinary and Security reviews are due on this exact commit. **Elapsed:** approximately 4 minutes excluding test runs; tokens unknown.

## Timing observations -- Codex (coordination) -- 2026-11-06 -- joined C1 check

The C1 joined change check at `73aaf88d`, Python 3.13.13, ran 104 files in three serial batches of 35, 35 and 34. It recorded 5,664 passed, 9 skipped and 18 initial failures; wall time was 1,522.087 seconds and pytest time 1,519.35 seconds. These are diagnostic phase sums by file from the joined run, not wall time, a matched comparison or a suite-speedup claim. This refreshes the existing over-ten-second C1/C2 diagnostic list while preserving the earlier joined-change observations above.

| File in `bootstrap/tests/` | Observed phase seconds |
|---|---:|
| `test_repin_ceremony.py` | 566.931 |
| `test_gate_preflight.py` | 189.958 |
| `test_repin.py` | 175.446 |
| `test_reanchor.py` | 59.049 |
| `test_upgrade.py` | 38.251 |
| `test_security_net.py` | 34.283 |
| `test_upgrade_edit_check_runs_no_project_programs.py` | 32.992 |
| `test_security_stack.py` | 26.475 |
| `test_upgrade_module_additions.py` | 26.452 |
| `test_upgrade_removes_retired_files.py` | 23.947 |
| `test_portable_security_sweeps.py` | 23.517 |
| `test_ceremony_review_report.py` | 21.919 |
| `test_security_check.py` | 21.882 |
| `test_gate_reanchor.py` | 21.229 |
| `test_upgrade_refuses_hostile_project_data.py` | 21.015 |
| `test_security_finding_confidentiality.py` | 20.913 |
| `test_code_map.py` | 20.685 |
| `test_web_hosting_security.py` | 14.701 |
| `test_intents_tool.py` | 13.607 |
| `test_broad_run_guard.py` | 13.447 |
| `test_gate_manifest.py` | 12.511 |

The edit-check fixture repair is supported by its focused behavior checks, not by these joined phase sums. **Elapsed:** derived from the joined run; record processing unknown. **Tokens:** unknown.

## Code review -- Codex GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-06 -- edit-check fixture

**Reviewed commit:** 23ded78fdd2322615f8b50c8b12d042b42f1feb3

**Verdict:** No blocking findings. **Bounding:** ACCEPTED for this fixture repair; Security Review and final wide Boundary B remain due.

**Foundations**

1. **Should this happen as framed?** Yes: the diff retains all refusal, staging, no-write and version-order assertions while requiring the injected step's marker; its wrapper limits the short timeout to the matching hang and restores the prior value in `finally` -- test diff from `72194fea^` to `23ded78f`.
2. **Best alternative.** Keep the former global short deadline; it is simpler but can time out before the intended fault, as the joined failures and focused evidence in `c053fc23` show.
3. **What would show it wrong?** A wrong step producing the marker, a missed fault passing, or timeout state leaking into another call would falsify the repair; repeat targeted fault and restoration controls if matching or launcher behavior changes -- test fixture and `_run_git_sterile`.

**Evidence:** Examined the complete changed diff, four step patterns, shell case and argument parser, production timeout use, and focused two-seed evidence in `c053fc23`. The parametrization, skip markers and test names are unchanged; the marker is written by the matched stand-in branch before the fault. In a disposable archive of `23ded78f`, Python 3.13.13, replacing the settings hang with successful exit made the single real-entry settings-hang node fail at the expected cannot-tell assertion (1 failed in 1.08s), despite reaching its marker. Existing `monkeypatch` restores the launcher at teardown; `finally` restores the timeout even on exceptions. No product source or policy change is present in the reviewed file diff.

**Coverage:** This pass covered only the named file repair and recorded focused checks. It did not independently run all parameters, measure scheduling contention, mutate every step, test native Windows, perform Security Review or run final wide Boundary B. No plan fence became the next move in this source range. **Elapsed:** unknown. **Tokens:** unknown.

## Code Security Review -- Codex GPT-6.1 Sol (Security Review, High) -- 2026-11-06 -- edit-check fixture

**Reviewed commit:** 23ded78fdd2322615f8b50c8b12d042b42f1feb3; named artifact: `bootstrap/tests/test_upgrade_edit_check_runs_no_project_programs.py`, repair from `72194fea^`.
**Tier:** Internal Security Review. **Obligation:** Internal Security Review.

**Foundations**

1. **Should this happen as framed?** Yes: targeted timeout shortening preserves real launcher execution and every existing refusal, staging, version-order and no-write assertion; the branch marker prevents an unrelated early refusal from passing -- committed repair diff and author evidence `c053fc23`.
2. **Best alternative.** Retaining the global short timeout avoids a wrapper but admits premature refusal; this small local wrapper directly addresses the recorded ten failures without changing engine policy -- `c053fc23` and production `_run_git_sterile`.
3. **What would show it wrong?** A missed injection or wrong label passing the real upgrade node would falsify branch detection; both targeted mutations failed as expected. A future launcher bypass or lost timeout restoration would also falsify the design -- probes below.

**Evidence:** In separate committed-byte archives of `23ded78f`, Python 3.13.13 ran settings/non-zero with an unmatched injection target: 1 failed in 1.14s on absent marker; comparison/non-zero with a wrong marker: 1 failed in 1.28s on branch assertion. The committed wrapper/parser probe preserved arguments and limits, kept the normal budget for non-target/non-hang calls, shortened the matching hang, and restored the budget after return and exception. Script and captures: `/private/tmp/cairn-edit-security-LgPYFV/`. An initial probe-script replacement was ambiguous; restricting replacement to the named function fixed the harness before mutation runs. Static comparison confirms unchanged test names, parametrizations and POSIX skip classification; only this test file changes in the source range. Quoted marker paths/labels and fresh per-case paths prevent accidental marker reuse. `finally` and monkeypatch teardown preserve cleanup. Ordinary fault-removal evidence remains `cb58831e`.

**Findings:** none. **Verdict:** No blockers. **Bounding:** ACCEPTED for this repair.

**Coverage:** This first Security pass covers this named repair only, including marker false positives, delegation and cleanup; no earlier fixture review is reopened. Not covered: exhaustive per-step mutations, native Windows, timing guarantees, suites, final wide Boundary B or certification. Existing author two-seed evidence supplies positive execution; final Boundary B remains due. **Elapsed:** approximately 8 minutes. **Tokens:** unknown.

## Timing observations -- Codex (coordination) -- 2026-11-06 -- final shared check

On clean committed `f14169e8`, Python 3.13.13, the 108-file mapped union
recorded 5,978 passed and nine expected native-Windows skips in 1,428.084
seconds wall. This exceeds the three-minute integration diagnostic. These
JUnit phase sums refresh the existing consolidation list, slowest first;
they are neither setup/call splits nor a matched speed comparison. Existing
`tools/gauge.py --pulse` consumed the three reports. No full-suite flag.

| File in `bootstrap/tests/` | Observed phase seconds |
|---|---:|
| `test_repin_ceremony.py` | 563.965 |
| `test_gate_preflight.py` | 193.458 |
| `test_repin.py` | 168.940 |
| `test_reanchor.py` | 56.301 |
| `test_upgrade.py` | 37.753 |
| `test_upgrade_edit_check_runs_no_project_programs.py` | 29.101 |
| `test_upgrade_module_additions.py` | 27.097 |
| `test_upgrade_removes_retired_files.py` | 26.309 |
| `test_security_stack.py` | 26.159 |
| `test_security_check.py` | 23.924 |
| `test_gate_reanchor.py` | 23.624 |
| `test_ceremony_review_report.py` | 21.613 |
| `test_portable_security_sweeps.py` | 21.167 |
| `test_upgrade_refuses_hostile_project_data.py` | 20.287 |
| `test_gate_manifest.py` | 15.265 |
| `test_broad_run_guard.py` | 14.696 |
| `test_intents_tool.py` | 14.516 |

The public pulse growth/inventory slice is implementation work independent of
private collection; counts alone do not complete C4. **Elapsed:** run above;
processing unknown. **Tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-06 -- C4 public growth reporter

The public report input is implemented at `a9c52301`; owning-test corrections
are `eb7d7bcd`, and the exact `test_meter` integration-tier repair is
`1517de0f`. `tools/test_tiers.py list --json` exports aggregate source test
file/line totals by configured tier. `gauge --pulse` now accepts explicit
before/after JUnit and tier inventories and reports baseline observations,
total and shared-tier inventory deltas, case-record deltas, and phase/session
time deltas. Missing observations stay unknown; case records are not unique
tests or collected nodes; matching labels do not prove equivalence. No private
Meter inputs or store are used.

On clean Python 3.13.13 copy `1517de0f`, tier validation passed for 136 source
test files in five tiers. The three nodes that failed in the initial focused
run passed after correction in 0.13 seconds. The original run on `a9c52301`
had 53 passed and three failures: two fixture/assertion errors, followed by
the already-unplaced `test_meter` tier. The test-only correction and separate
one-pattern integration mapping repair preserve that evidence; no failing-case
result was erased.

The final changed-path mapping selects 30 test files. This broad mapped A
remains due and was not run; only the two owning test files and three formerly
failing nodes were executed. No real before/after suite timing or growth
comparison was performed, so C4 evidence and the ten-minute target at an
authorized certification point remain open. This implementation does not
finish C1-C4, Boundary B, or the plan. **Elapsed:** unknown. **Tokens:** unknown.

## C4 reporting observation -- Codex (coordination) -- 2026-11-06

The shared public pulse now reports real source-file/line deltas separately
from JUnit execution counts and times. At Python 3.13.13, existing
`test_tiers.py list --json` inventories for `135ddd2f` and `ee8d4ab6` show
136 files in both, 92,992 then 93,304 decoded lines (+312). Existing
`gauge.py --pulse --json` consumed those inventories and the actual 31-file
run plus its 14-node network retry. It preserved 2,697 execution records,
including 14 initial denied-listener failures and their passes; it claims
neither unique-node growth nor a comparable speed improvement. Full results
and limits are in the Meter public-slice verification record. This closes
the reporting-interface gap; C1/C2 remaining-family dispositions, C3 moves
and the accepted matched timing evidence still govern this plan's completion.

The 31-file run exceeded the integration diagnostic. Combined observed phase
sums refresh the existing over-ten-second list, slowest first; these are not
setup/call splits or matched benchmarks.

| File in `bootstrap/tests/` | Observed phase seconds |
|---|---:|
| `test_security_check.py` | 53.301 |
| `test_upgrade.py` | 38.673 |
| `test_upgrade_module_additions.py` | 28.281 |
| `test_portable_security_sweeps.py` | 23.475 |
| `test_ceremony_review_report.py` | 22.456 |
| `test_upgrade_lockfile_path_containment.py` | 12.388 |
| `test_upgrade_added_slots.py` | 10.565 |

**Elapsed:** source runs above; processing unknown. **Tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-06 -- C3 final moves and native IDs

**Source and snapshots.** Move and fixed-policy fold: `064fdc9f`;
pre-move snapshot: `3e803172`. Separate detached clones were clean before and
after. Checks used `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13);
`CAIRN_FULL_SUITE` and `PYTEST_ADDOPTS` were unset. Each moved source is byte-
identical to its prior committed file except `ROOT` changing from
`parents[2]` to `parents[3]`. The tier JSON needed no edit: existing recursive
filename patterns assign all four files to the intended tiers.

| Old node path | New node path | Nodes at each seed |
|---|---|---:|
| `bootstrap/tests/test_check_release_publication.py` | `bootstrap/tests/security/test_check_release_publication.py` | 32 |
| `bootstrap/tests/test_code_map.py` | `bootstrap/tests/security/test_code_map.py` | 35 |
| `bootstrap/tests/test_git_interpreter_binding_portable.py` | `bootstrap/tests/security/test_git_interpreter_binding_portable.py` | 23 |
| `bootstrap/tests/test_test_tiers.py` | `bootstrap/tests/contract/test_test_tiers.py` | 18 |

Exact-file collection at seeds 0 and 1 found 108 nodes on both snapshots each
time. Replacing only the four old path prefixes with their new prefixes made
each candidate node set equal to baseline: zero added, dropped or duplicate
IDs; every suffix and parameter is unchanged. Captures are
`/private/tmp/cairn-c3-before-seed{0,1}-collect.log` and
`/private/tmp/cairn-c3-after-seed{0,1}-collect.log`. `tools/test_tiers.py check`
passed: 136 source files in five tiers. `tools/test_tiers.py for` on extant
changed paths selected exactly 12 files: `bootstrap/tests/contract/test_release_members_contract.py`,
`bootstrap/tests/contract/test_test_tiers.py`,
`bootstrap/tests/security/test_check_release_publication.py`,
`bootstrap/tests/security/test_code_map.py`,
`bootstrap/tests/security/test_git_interpreter_binding_portable.py`,
`bootstrap/tests/test_broad_run_guard.py`, `bootstrap/tests/test_scaffold.py`,
`bootstrap/tests/test_security_check.py`, `bootstrap/tests/test_security_marker.py`,
`bootstrap/tests/test_session_binding_gate_and_printing_hold.py`,
`bootstrap/tests/test_session_binding_untracked.py`, and
`bootstrap/tests/test_upgrade.py`. This mapped selection was not run.

**Focused outcomes.** The four moved files passed at both seeds on the clean
candidate: seed 0, 96 passed and 12 skipped (24.18 seconds pytest, 25.79 wall);
seed 1, 96 passed and 12 skipped (23.98 seconds pytest, 24.49 wall). On this
POSIX host, the 12 skips are the four NT-native code-map cases and eight NT
interpreter-binding parameters. The exact `test_security_check.py` policy/count
and raw-report positive controls passed (2 passed, 0.22 seconds pytest). The
four newly added NT code-map roster-omission parameters passed (4 passed, 601
deselected, 0.17 seconds pytest). The fixed policy contains 605 unique rows:
13 NT and 592 POSIX; its canonical identity is
`sha256:25572c7fb58892ff5fe233c2e30e1c7dea4a06b2f3da564b14e45666616e28a3`.
This is four reviewed NT additions plus exactly 16 old-to-new path relocations:
eight code-map rows and eight interpreter-binding rows. These results are
scoped preservation evidence, not a timing or suite-speedup claim.

The live C3 criterion now names the moved recursive-tier test at its current
`contract/` path; its requirement is unchanged. `claim_check` still reports
four unresolved old source prefixes in the mapping table. Those are
intentional baseline node paths from `3e803172`, not live path references.
`link_check`, snippet check and `diff --check` pass.

No broad mapped selection, all-605 omission sweep, Windows-native execution,
full suite, Security Review, or final wide Boundary B ran. The ordinary and
Security reviews for this batch, the mapped 12-file selection, and final wide
Boundary B remain due. **Elapsed:** unknown. **Tokens:** unknown.

## Code Review -- Codex GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-06 -- C3 final moves

**Reviewed commit:** `064fdc9f`; checkpoint `0fe8d652`.

**Foundations**

1. **Should this happen as framed?** Yes: the four rename diffs change only repository-root depth in test bodies, while the runner and live descriptions use the new paths; the checkpoint maps all 108 collected IDs at both seeds.
2. **Best alternative.** Leave the tests at root; that avoids path churn but fails C3's tier-directory outcome. The frozen gate manifest retains its historical paths and is outside this authorized move.
3. **What would show it wrong?** A missing or duplicated mapped node, a live consumer using an old path, or a native-only identity mapped to the wrong host would falsify preservation; repeat collection and host-policy reconciliation after further moves.

**Evidence:** Read the complete move and policy diff, C3 criteria, checkpoint, native classification at `1edccec6`, and Windows runner. The fixed policy relocates the old native path prefixes and records four reviewed Windows additions; proof logic is unchanged. A path search found old entries in the frozen gate manifest and historical strategy text. In a disposable archive of `064fdc9f`, Python 3.13.13 tier validation passed for 136 files; the changed-module selection control passed (1 in 0.04s). Reverting the moved tier test's root depth in that copy caused collection to fail at an incorrect tools path under bootstrap, as expected. Author evidence records matched collections, focused executions, and the subsequent 605-member omission matrix at `d6d65559`.

**Findings:** none. **Verdict:** No blocking findings. **Bounding:** ACCEPTED for this batch; the mapped 12-file selection and final wide Boundary B remain due.

**Coverage:** This pass covers the named committed moves, active path consumers, and policy diff, not independent Windows execution, exhaustive mutations, the later CLI tests, Security Review, final Boundary B, or certification. Separate Security Review remains owed. **Elapsed:** unknown. **Tokens:** unknown.

## Security code review -- Codex gpt-6.1-sol (High) -- 2026-11-06 -- shared C3 fold

**Obligation:** Internal Security Review. **Verdict:** REVISE for the shared
`064fdc9f` namespace/policy fold; not a new review of C1/C2 or architecture.

This is the same actual pass recorded in
`dev/plans/2026-11-05-strict-release-security-runner.md`, Security code review
at reviewed commit `3d3a8118`; its three Foundations answers, evidence and
limits apply. Ordinary C3 review `3d3a8118` was read before this record.
The bijective path fold and four source-reviewed additions preserve the
605-member roster, but the live opposite-platform fixture in
`bootstrap/tests/test_security_check.py` still writes the old interpreter-binding
path. Its focused Python 3.13.13 control failed: eight passed instead of eight
skipped. Close shared C3 Security finding 1 by updating that fixture and
retaining listed/unlisted-ID controls; return for a targeted look before wide
Boundary B. The separate SHA-256 finding belongs to Strict C2.

**Coverage:** shared namespace/policy diff and its live fixture consumer;
not architecture behavior, other Suite chunks, native Windows execution,
mapped selection, final Boundary B or certification. **Elapsed:** unknown.
**Tokens:** unknown.

## Shared C3 Security finding response -- Codex GPT-6 Luna (Low) -- 2026-11-06

The moved-fixture finding is addressed by the shared Strict C2 correction at
`8d28b0d3`: its synthetic test now creates the interpreter-binding module at
`bootstrap/tests/security/test_git_interpreter_binding_portable.py`, with a
nearby unlisted-ID passing control. The targeted clean-copy selection passed;
the Strict plan's response records the command, counts and limits. This closes
only the shared fixture-path finding. The mapped C3 selection and final wide
Boundary B remain due. **Elapsed:** included in the Strict response. **Tokens:**
unknown.

## Targeted second Security Review -- Codex gpt-6.1-sol (High) -- 2026-11-06 -- shared C3 closure

**Obligation:** Internal Security Review. **Verdict:** ACCEPT for shared C3
fold `064fdc9f` and its fixture correction `8d28b0d3`.

This is the same actual targeted pass recorded in
`dev/plans/2026-11-05-strict-release-security-runner.md`, Targeted second
Security Review; its three Foundations answers, probes and limits apply.
Shared finding 1 at `88f15d21` closes: the corrected fixture uses the moved
policy path, and canonical Python 3.13.13 on clean `8a89bbcb` passed its
listed/unlisted control. The 605-member roster is unchanged. Ordinary C3
review `3d3a8118` and the targeted ordinary return `8a89bbcb` were read.

**Coverage:** This closes the named shared namespace/policy Security scope;
not other Suite chunks, architecture behavior, native Windows execution,
mapped selection, final wide Boundary B or certification. **Elapsed:** unknown.
**Tokens:** unknown.

## Code Review -- Codex GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-06 -- C1 fixture lifetime and ceremony observation

**Reviewed commits:** `e0cd2df2` (ordinary ceremony observation), `f9101bef` and `997e1424` (fixture lifetimes).

**Foundations**

1. **Should this happen as framed?** Yes: the ceremony still runs in a copied scratch repository and retains seven node assertions, while the later diffs change only fixture scopes; per-test mutable repositories still copy their seeds.
2. **Best alternative.** Keep module lifetimes and separate ceremony executions. That reduces sharing but repeats preparation under shuffled collection and forfeits the scoped improvement recorded for the seven ceremony nodes.
3. **What would show it wrong?** A seed changed by a consumer, a later test observing another's mutation, or a missed digest, stage-two environment, or disclosure fault would falsify preservation; repeat isolation and these fault controls after fixture or ceremony changes.

**Evidence:** Read all three diffs, ceremony fixture and seven assertion changes, lifetime consumers, earlier re-anchor and collision reviews, and author verification. Copies isolate the writable installations and repositories; report mutations use deep copies, and module patches use pytest's restoring `monkeypatch`. The shared ceremony observation freezes captured values and still uses the real scratch signing path. The `e0cd2df2` record maps all seven IDs and reports three real-entry fault kills (digest, environment and disclosure). The two setup-plan logs for `f9101bef` show one session setup per seed with function-scoped mutable beds; they ran no tests. In a separate archive of `f9101bef`, Python 3.13.13 collision isolation passed; two ceremony nodes initially failed when scratch signing refused its passphrase. With local signing permission and `SSH_AUTH_SOCK` unset, those same two nodes passed in 9.16s. The extension `997e1424` was inspected at source level; no independent test was run on it.

**Findings:** none. **Verdict:** No blocking findings. **Bounding:** ACCEPTED for the reviewed source slice, subject to outstanding mapped implementation checks, separate Security Review, and final wide Boundary B. Frozen baseline mismatches remain unpassed.

**Coverage:** This pass covers the three named commits and their preservation evidence. It did not repeat the three fault mutations, independently execute the extension, measure timings, exercise native Windows, run a suite or clear Security Review or release baselines. **Elapsed:** unknown. **Tokens:** unknown.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-06 -- C1/C2 dispositions and C4 matched phases

**Source.** `f9101bef` changes five immutable fixture decorators to session scope; `997e1424` changes nine more across seven files. Session fixtures hold only shared immutable descriptions, snapshots, report data, and dynamically loaded modules. Function-scoped `bed`, `cbed`, `project`, `repo`, `world`, `scenario`, `branch`, `staged_collision`, per-test keys/refs/paths, and `monkeypatch` cleanup remain intact. The later live-description correction is `725d7b3b`; it updates the self-hosted and shipped tier guidance, `tools/test_tiers.py` module docstring, and its owning contract-test docstring, with no assertion or node change.

**C1/C2 residual-family disposition.** No further sharing change is justified for the remaining `test_upgrade.py` classes: `TestLockfile`, `TestProfileSizedAssembly`, `TestTemplateGatingSafety`, `TestSlotParser`, `TestMerge`, `TestVerbatim`, most of `TestUpgradeModes`, `TestInitLockFullProfile`, `TestReviewOnlyMerge`, `TestRulesMdAbsentFromUpgradePlan`, `TestLivingStatePartition`, `TestDirtyTreeGuard`, `TestManifestHomeAndSelfHeal`, `TestFinalizeDirtyTreeGuard`, and `TestTrackedDirectoryCollisions`. The 89 `_install` source call sites create real installs, and many tests assert that install or the corresponding distinct plan/stage/apply/finalize/refusal mutation. The `TestInitLock` profile records 2.003s cumulative `_install` over 27 nodes; its migrations and refusal behavior remain the subject of the tests. The `TestAdoptModule` snapshot prototype and its mixed timings, added controls, and protected-test burden are already recorded above; they do not establish useful low-burden reuse for the rest of rank 7.

No new reuse is warranted for `bootstrap/tests/security/test_code_map.py`: its 35 collected nodes use independent temporary roots for real CLI scanning, path refusal, parser/whole-command deadlines, filesystem races, and budget limits. Its one repeated install is inside the installed-copy test, where a second install verifies preservation of adopter edits. Existing file-phase sums (20.685s and 22.132s in different joined selections) contain no setup/call split. The profile does not identify a common preparation cost worth sharing. The nine session-lifetime updates above address measured immutable preparation opportunities; they do not claim that every duplicated operation in every ranked family has been optimized. No test node, assertion, parameter, refusal, or mutable-state boundary was removed or changed. The mapped final Boundary B remains due.

**C4 matched setup/call evidence.** Clean before and after worktrees used `/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13), identical node IDs, seeds 0 and 1, `--durations=0 --durations-min=0`, and four small interleaving separator nodes per selection. Each run unset `CAIRN_FULL_SUITE`, release flags, `PYTEST_ADDOPTS`, `SSH_AUTH_SOCK`, `SSH_ASKPASS`, `SSH_ASKPASS_REQUIRE`, and `DISPLAY`; ceremony signing used generated temporary keys and repositories only. Uptime loads and wall times are retained in the run outputs; contention was not controlled.

| Selection and committed snapshots | Seed | Passed | Setup / call / teardown seconds | Pytest / wall seconds |
|---|---:|---:|---:|---:|
| Ceremony: seven nodes + four separators, `b0de365` | 0 | 11 | 2.69 / 59.24 / 0.00 | 62.40 / 63.03 |
| Ceremony, candidate `f7380ffb` (`test_repin.py` and `test_repin_ceremony.py` bytes from `997e1424`) | 0 | 11 | 8.80 / 0.08 / 0.00 | 9.32 / 9.92 |
| Ceremony, `b0de365` | 1 | 11 | 2.52 / 56.50 / 0.00 | 59.09 / 59.83 |
| Ceremony, `f7380ffb` | 1 | 11 | 8.81 / 0.05 / 0.00 | 8.92 / 9.49 |
| Reanchor: eight missing-executable parameters + four separators, `c06f7b48` | 0 | 12 | 0.50 / 0.17 / 0.00 | 1.22 / 1.77 |
| Reanchor, candidate `a06367c3` (`test_reanchor.py` bytes from `997e1424`) | 0 | 12 | 0.14 / 0.17 / 0.00 | 0.87 / 1.43 |
| Reanchor, `c06f7b48` | 1 | 12 | 0.50 / 0.13 / 0.00 | 0.68 / 1.24 |
| Reanchor, `a06367c3` | 1 | 12 | 0.14 / 0.13 / 0.00 | 0.31 / 1.01 |
| Collision: 60 original nodes + four separators, `309b6d9a` | 0 | 64 | 0.00 / 25.95 / 0.00 | 26.24 / 26.83 |
| Collision, candidate `858f6de3` (`e8873350` test bytes plus session fixture scope; added control deselected) | 0 | 64 | 0.67 / 19.52 / 0.00 | 20.28 / 20.85 |
| Collision, `309b6d9a` | 1 | 64 | 0.00 / 25.18 / 0.00 | 25.30 / 26.22 |
| Collision, `858f6de3` (added control deselected) | 1 | 64 | 0.64 / 19.31 / 0.00 | 20.06 / 21.06 |

The ceremony pair moves the real successful observation into one shared setup; the reanchor pair saves about 0.36s of setup per seed; collision setup/call sums fall 5.76s and 5.23s. These are scoped phase observations, not suite-wide savings or causal guarantees. The corrected collision seed-1 baseline ran after the candidate because it was the one missing leg; no unchanged baseline was repeated to restore trial order. Uptime loads before reanchor trials were 5.21, 5.20, 5.38, and 5.82; before collision seed0/candidate0/candidate1/baseline1 they were 5.36, 7.04, 5.70, and 5.02. Ceremony load was not sampled. All valid worktrees were clean before and after.

Root also consumed the six committed before/after JUnit reports through the existing public `gauge --pulse --json` interface; the pulse reports execution records and phase times while leaving equivalence `not_assessed` and private usage unknown. This is distinct from the earlier +312-line inventory growth observation.

**Preparation miss.** An initial disposable collision candidate incorrectly overlaid the later `997e1424` file onto `309b6d9a`, bringing unrelated test additions without their product prerequisites. That non-comparable run recorded 71 passed, 41 failed, and one deselected; it is preserved at `/private/tmp/cairn-c4-collision-after-seed0.log` and excluded from C4. The corrected candidate `858f6de3` starts from the reviewed `e8873350` bytes plus only the accepted session decorator. Pre-run collection at both seeds confirmed 60 original collision IDs plus the same four separators, identical before/after. The final corrected pairs all passed; the extra isolation control was retained and explicitly deselected.

**Limits and remaining gates.** The `f9101bef` 21-node mixed `--setup-plan` at both seeds preserved identical node IDs and listed each targeted session fixture once; `--setup-plan` ran no test bodies. Prose claim, link, snippet, and neutrality gates for `725d7b3b` passed. `claim_check` reports no new path flags; the four historical old-source entries in the C3 mapping table remain intentional. The owning tests for the nine latest lifetime edits and the four description paths are included in the final mapped Boundary B; this record does not claim that run. No full suite, release run, trusted anchor operation, repin, real key/ref write, or product code change was performed. **Elapsed:** timing runs above plus documentation; authoring time unknown. **Tokens:** unknown.

## Targeted Code Review -- Codex GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-06 -- testing guidance

**Reviewed commit:** `725d7b3b`, the guidance delivery correction only.

**Foundations**

1. **Should this happen as framed?** Yes: the matching self-hosted and shipped text now describes the tier folders, recursive filename map and isolated mutable cases, fulfilling the C1/C3 guidance requirement.
2. **Best alternative.** Leave the former text alone; it avoids this prose change but leaves the accepted guidance update undelivered and the tool descriptions stale.
3. **What would show it wrong?** A tier assignment or fixture consumer contradicting this description would falsify it; recheck the map and isolation when placement or fixture lifetimes change.

**Evidence:** Read the complete four-file diff, plan scope and criteria, and tier configuration. The guidance twins have identical changes; tool and test docstrings now describe first-match recursive placement. No test logic or node identity changes. Author prose gates are recorded at `343a40c1`.

**Findings:** none. **Verdict:** No blocking findings. **Bounding:** ACCEPTED for this correction; mapped checks, separate Security Review and final wide Boundary B remain due.

**Coverage:** This targeted return covers the guidance correction, not a new review of prior source, independent reruns, native platforms, certification or release. **Elapsed:** unknown. **Tokens:** unknown.

## Security code review -- Codex gpt-6.1-sol (High) -- 2026-11-06 -- C1 immutable preparation and lifetime

**Reviewed:** observation `e0cd2df2`, lifetimes `f9101bef`/`997e1424`, guidance
`725d7b3b`, evidence `343a40c1`, ordinary reviews `d82fb3db`/`a37879c7`.
**Obligation:** Internal Security Review. **Verdict:** ACCEPT for this named
C1 batch. **Bounding:** ACCEPTED for this source slice; mapped checks and
final wide Boundary B remain due. **Elapsed:** unknown. **Tokens:** unknown.

**Foundations**

1. **Should this happen as framed?** Yes: the real scratch ceremony produces an immutable observation, and fourteen scope changes retain separate mutable case copies while avoiding repeated preparation under interleaving.
2. **Best alternative.** Keep the existing seeds and immutable observations; per-case preparation preserves isolation but repeats measured work. Additional copying or caching mechanisms would add burden without improving these boundaries.
3. **What would show it wrong?** A copied key/ref alias, leaked module override or missed ceremony digest/environment/disclosure fault would falsify preservation; retain the existing isolation and fault controls and the restoration probe below.

**Evidence:** Traced the seven retained ceremony assertions to `full_run`
and its captured signature, record bytes and audit. The returned mapping
contains immutable scalar/byte values and nested tuples, without a live bed.
Refusal cases retain function-scoped `cbed`. The fourteen decorator changes
leave copied installations, repositories, keys, refs and collision targets
function-scoped. Report consumers read or deep-copy data; loaded-module
changes use restoring per-test monkeypatches.

After the timing window, canonical Python 3.13.13 on a separate clean
`efd88020` clone ran the dispatcher-patch node followed by its real clean-audit
node in `TestRunnerExitContract`: **2 passed in 0.30 seconds**, clean
before/after. This independently challenges restoration across the new
session lifetime. Earlier recorded ceremony digest/environment/disclosure
fault kills and key/collision alias controls remain relevant; they were not
repeated. Both guidance copies and the two module docstrings accurately
describe recursive tier placement and immutable session/per-case mutable state.

**Record gates:** Separate-copy links/snippets and neutrality passed (zero
failures, 43 informational items). Claim/content checks retain only the same
four historical moved-path flags; this append adds none.

**Coverage:** First pass on the original observation, new lifetime batch and
its guidance; targeted lifetime return only on previously reviewed re-anchor
and collision material. No blocking finding. Not covered: independent timings,
all-family execution, repeated mutation probes, native Windows, mapped checks,
final wide Boundary B, certification or trust/release operations. Closed
Strict/C3 and the separate Meter data fold are not reopened.
Over target to distinguish new scope from the prior targeted returns.

## Implementation verification -- GPT-6 Luna (Implementation, Low) -- 2026-11-06 -- detached clone branch setup

The frozen mapped batch at `95ea28b8` had 2525 passed, one expected skip, and one failure: `bootstrap/tests/test_repin.py::test_baseline_preparation_builds_exact_package_after_reader_binding` (reported node duration 17.9s). The scratch clone inherited the detached source checkout, so the existing `symbolic-ref HEAD` assertion failed before the test's atomic branch-and-anchor installation checks.

Commit `c0e84822` changes only this test's scratch setup: after constructing its isolated Git environment, it creates/resets deterministic branch `scratch-baseline-preparation` at the clone's current `HEAD` and checks the command result. The candidate bytes, environment/refusal checks, race controls, signature assertions and temporary repository remain unchanged.

On a clean detached copy of `c0e84822`, canonical Python 3.13.13 ran only the failed node with `--quality-gate-shuffle-seed=0 --durations=0 --durations-min=0`, with `CAIRN_FULL_SUITE`, inherited SSH agent/askpass variables and `DISPLAY` unset and local scratch-signing permission: **1 passed in 35.47s** (call 35.26s). The copy was clean before and after and remained detached. This falsifies the detached-checkout failure; an attached-source rerun is not needed because the setup explicitly resets the scratch clone's branch. No other test or source changed. **Elapsed:** 35.47s test; **Tokens:** unknown.

## Targeted Code Review -- Codex GPT-6.1 Terra (Reviewer, Medium) -- 2026-11-06 -- scratch branch setup

**Reviewed commit:** `c0e84822`, the named baseline-preparation test setup correction.

**Foundations**

1. **Should this happen as framed?** Yes: a named branch in the disposable clone supplies the active-branch precondition needed by the existing branch and anchor transaction checks, including when the source checkout is detached.
2. **Best alternative.** Depend on the source checkout's branch state; that leaves the recorded detached-checkout failure and makes this scratch test dependent on its caller's checkout state.
3. **What would show it wrong?** A branch switch that changes the candidate bytes or prevents the existing branch/anchor race assertions from detecting an error would falsify the correction; rerun the named test when this setup or transaction changes.

**Evidence:** Read the four-line committed diff and the complete named test. The switch targets `HEAD` inside the fresh clone using its sterile Git environment and asserts success; existing assertions are unchanged. The author records the original detached failure and clean-copy corrected result at `df289538`: Python 3.13.13, one pass in 35.47s. The passing node exercises the newly attached scratch branch through its existing transaction checks. A separate attached-source run was not performed.

**Findings:** none. **Verdict:** No blocking findings. **Bounding:** ACCEPTED for this correction; separate Security Review and final wide Boundary B remain due.

**Coverage:** This targeted return covers the named setup correction and author result, not other fixture changes, independent execution, certification or release. **Elapsed:** unknown. **Tokens:** unknown.

## Targeted second C1 Security Review -- Codex gpt-6.1-sol (High) -- 2026-11-06 -- scratch branch setup

**Reviewed:** `c0e84822`, author evidence `df289538`, ordinary return
`79f2e8eb`. **Obligation:** Internal Security Review.
**Verdict:** ACCEPT for this correction. **Bounding:** ACCEPTED for the
named change; final wide verification remains due. **Elapsed:** unknown.
**Tokens:** unknown.

**Foundations**

1. **Should this happen as framed?** Yes: this test exercises an active branch and anchor transaction; the four added lines establish that precondition in its disposable clone even when the source is detached.
2. **Best alternative.** Create the scratch branch explicitly at the existing HEAD; depending on source attachment leaves the recorded failure, while changing production branch handling would exceed this fixture defect.
3. **What would show it wrong?** Changed candidate bytes, a command targeting the source repository, or lost branch/anchor race detection would falsify the repair; retain the named real-entry test and its exact byte, refusal and race assertions.

**Evidence:** Read the complete committed function and four-line diff. Its
fresh `--no-hardlinks` clone lives under the test temporary directory. The
new Git command uses that explicit target and isolated environment, creates the ordinary
scratch branch at unchanged HEAD, and asserts success. It writes no source
repository branch or real authority ref. Existing collection-credential
sentinels, package hashes, signature checks, no-ref-change refusals, competing
anchor/branch transactions and protected-byte/node/marker controls remain.

The retained author record reports the original detached failure, then the
exact node passing on clean detached `c0e84822`: canonical Python 3.13.13,
**1 passed in 35.47 seconds**, clean before/after. That node exercises the
new attached scratch state; another attached-source run would add no distinct
fixture question. No independent check was rerun.

**Record check:** Separate-copy claim checking retains only the four known
historical moved-path flags; this append adds none.

**Coverage:** Capped second C1 return on this newly changed function only;
no new blocking question. Not covered: other fixture material, repeated green
checks, suites, final aggregate Boundary B, certification or baseline/release
operations. The closed fourteen-fixture, Strict/C3 and Meter reviews remain
closed.
