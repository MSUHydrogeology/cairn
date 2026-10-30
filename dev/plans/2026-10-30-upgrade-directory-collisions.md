# Plan: Block tracked upgrade directory collisions

**Source proposal**: dev/proposals/archive/2026-10-29-codex-upgrade-directory-collisions.md
**Status**: implementing
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Report folders occupying tracked upgrade files and protect their contents until the operator resolves them.

## Source proposal

The Maintainer accepted the revised proposal to report tracked directory collisions, block the entire staged apply, preserve adopter data and metadata, and require resolution and a fresh stage.

## Scope

Change `bootstrap/_scaffold/upgrade.py`, its public-command tests, and `bootstrap/UPGRADE.md`. Preserve retired-record handling and containment and symlink refusals. No doctrine surface. The existing Maintainer-run AST re-anchor remains required and is not authorized by this plan.

**Reuse.** Searching `bootstrap/_scaffold` for collision, directory, stage and apply found existing hard-block kinds, stage snapshots, review buffers and apply checks in `upgrade.py`; extend those mechanisms without granting addition adoption or creating file review pairs for directories. Search readers and tests again before implementation and extend the mapping if necessary.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Classify and protect collisions at plan, stage and apply observation points | Both plan reviews | Engine behavior and public-command tests |
| C2 | Document recovery and verify the complete change | C1 | Guidance, mutation and stable verification evidence; handoff for independent code and Security reviews |

## Acceptance criteria

### C1

Plan and stage report an actionable hard block without traceback for ordinary mergeable and verbatim tracked files occupied by directories, including nested paths; unaffected files remain visible. Apply refuses the entire blocked stage before writes or lockfile or base-cache advancement, including with override flags and after live-path repair; no addition adoption or file review pair applies. Public-command tests preserve directory contents and metadata bytes, cover valid files and retired records, and demonstrate recovery by moving contents aside, restoring the file or choosing absence, restaging and applying. Controlled file-to-directory transitions after planning and after staging cover stage no-op comparison, snapshot and review-buffer reads and apply; each refuses recoverably without traceback or data loss. Existing containment and symlink, symlinked-parent and dangling-link refusals remain prior to directory handling. No protection is claimed against arbitrary concurrent changes after a check.

### C2

Guidance describes the block and recovery and agrees with the command tests. Exercise public plan, stage and apply in a scratch installation. In separate scratch copies, remove directory classification and the apply block; relevant tests fail for each mutation and unmutated controls pass. Record outcomes. S2 is exercised here; S3 is the public commands and gates below. Record wide Boundary B on the final implementation commit; unmet checks keep work open. The AST ceremony remains Maintainer-run.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: use canonical Python 3.13 and run `python -m pytest bootstrap/tests/test_upgrade.py bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_upgrade_side_door_parity.py` for tracked upgrades, retired paths and containment; include new tests in the owning files. Run `python -m pytest bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_lockfile_provenance.py` for addition blocking and metadata consumers, and `python -m pytest bootstrap/tests/test_upgrade_refuses_hostile_project_data.py` for hostile stage metadata and public apply refusal. Search actual readers and extend this map if needed. Split selections within the broad-run guard's file limit and reconcile the executed union without an override. Run `python -m pytest bootstrap/tests/test_security_lint.py` for the engine security gate; a skip is an unmet check.

Exercise `python bootstrap/scaffold.py upgrade` public `--plan`, `--stage`, and `--apply` paths in a scratch installation, including resolution and restaging; check command help for exact arguments. Run `python scripts/claim_check.py` on changed prose, `python scripts/check_cairn.py`, `python scripts/link_check.py`, and `python scripts/quality_gate.py --sub neutrality`; run `python scripts/sync_doc_snippets.py` if synced snippets change. Record the two mutation controls and failures in separate scratch copies.

Boundary B is **wide** for the engine contract and security boundary: run the mapped owning families, public paths, mutations and standing gates on a clean, unchanged final implementation commit under the canonical interpreter. Record tested SHA and reviewed range, interpreter, clean pre/post state, commands, outcomes, timing, non-pass dispositions, omissions, and **Certified by**: pending. Certification is separate. Boundary C is independent targeted falsification by the code reviewer, including the observation points and stated race limit; the reviewer records bounding and any missing check. The AST re-anchor follows its existing Maintainer-run ceremony, separately authorized.


## Plan review -- Codex GPT-6.1 Sol -- 2026-10-30

Reviewed commit: 32fda3e7fe7859cdb93cf4f862c1ade89ba207c2
Target: scope, sequence, acceptance criteria and verification
Prior findings: none
Assurance path: Internal + Internal Security Review

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**:

1. **Should this happen as framed?** The plan carries the accepted block, recovery, observation points and race limit, but its verification mapping misses an existing consumer of the changed stage and apply boundary -- `dev/proposals/archive/2026-10-29-codex-upgrade-directory-collisions.md` and `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py`.
2. **Best alternative.** Extend the existing wide map with the relevant hostile-project-data family; reuse the planned public-path tests and existing hard-block machinery -- `bootstrap/_scaffold/upgrade.py:1100` and `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py:784`.
3. **What would show it wrong.** A directory transition raises instead of refusing, a blocked stage advances, or changed stage metadata admits hostile paths -- `bootstrap/_scaffold/upgrade.py:1137` and `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py:789`.

**P1 -- Map the hostile stage consumer before implementation.** The plan changes stage bookkeeping and apply's hard-block checks, yet its wide mapping omits `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py`, which drives public apply against hostile stage metadata, including `module_blocked` and staged names. The instruction to search again before implementation does not establish the reviewed mapping required by `dev/plans/_template.md` for a trust-boundary change. Add this owning family to the mapped runs, or identify the exact relevant nodes and justify any exclusions; retain the other mapped checks.

Coverage: checked the accepted current contract and Decision, plan cells, stage reads and apply ordering, existing containment and hostile-stage test ownership, and template verification requirements. No implementation or test run was performed; arbitrary concurrent changes after a check and the separate Security Review remain outside this pass.


## Plan review -- Codex GPT-6 Security reviewer -- 2026-10-30

Reviewed commit: 6df03f2c2d750718263d9507a7508909147c4767
Target: accepted contract, plan cells, ordinary review and security observation points
Prior findings: none in this obligation; ordinary P1 remains open
Assurance path: Internal + Internal Security Review

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none additional

**Foundations**:

1. **Should this happen as framed?** Yes: the plan preserves adopter contents, blocks the entire apply before metadata advancement, and names later reads where a file may become a directory; the ordinary mapping finding still needs the author's response -- C1 and `bootstrap/_scaffold/upgrade.py:1137`.
2. **Best alternative.** Extend the existing unconditional block and guarded read paths without addition adoption, review pairs or a new cleanup mechanism; this retains the accepted recovery outcome -- C1 and `bootstrap/_scaffold/upgrade.py:3112`.
3. **What would show it wrong.** A controlled directory transition causes a traceback, changes contents or metadata, bypasses a block, or changes a symlink refusal into directory handling -- C1 and `bootstrap/_scaffold/security.py:110`.

The accepted proposal's S1 and S4–S5 remain intact: the project supplies paths and lockfile data; refusal grants no replacement authority, and arbitrary writes after a check remain outside the claim. C1 explicitly covers classification, stage no-op comparison, snapshots, review buffers and apply, including override flags and a repaired live path that must not unlock an old stage. C2 locates the two required mutations and their unmutated controls; it does not substitute certification for these checks. These are suitable security acceptance criteria, rather than a stronger race-resistance claim.

I agree with ordinary P1: hostile stage metadata is a consumer of this boundary. Its existing public apply test varies `module_blocked` and other stage fields with traversal, absolute, Git-control and non-string names (`bootstrap/tests/test_upgrade_refuses_hostile_project_data.py:784`). The author must add that owning family or justify exact-node coverage in the reviewed mapping. This pass adds no separate finding and does not dispose of P1. Keep containment and symlink checks ahead of directory classification, as C1 requires; `_assert_safe_write` rejects destination and ancestor links (`bootstrap/_scaffold/security.py:110`). A directory diagnostic must not become permission to follow a directory link or adopt a tracked directory.

Coverage: claims, fail-closed design, reuse and scope were read against C1–C2 and `upgrade.py:1032`, `:1137`, `:1191`, `:3112` and `:3140`; public-path coverage and hostile inputs against the named test family; documentation drift and lifecycle against C2, Verification and the accepted proposal's Current contract. The existing block machinery was found by searching collision, directory and `module_blocked`, with positive matches at `upgrade.py:1032` and `:1276`. No scientific result is touched. No implementation, tests, mutations, certification or arbitrary concurrent-writer resistance was verified. This clears only the plan's Security Review obligation; ordinary P1 keeps the plan in revising-plan.


## Response to plan reviews -- Codex GPT-6.1 -- 2026-10-30

| Finding | Disposition |
|---|---|
| Ordinary P1 | Accepted. Verification now maps the hostile-project-data test family for stage metadata and public apply refusal; the other checks remain. |

The Internal Security Review raised no additional findings and cleared its obligation. Both plan reviews are complete; the plan is ready to implement.


## Implementation verification -- Codex GPT-6 (Implementation) -- 2026-10-30

**Boundary B mode**: wide. The change alters tracked-file classification, stage metadata and the apply gate, so the complete mapped upgrade owners, hostile stage consumers, public plan/stage/apply paths, and engine security gate were exercised.

**Certified by**: pending

**Tested commit**: b925187e798be7cd3a1c9ce2dec7d9f8398bce6a

**Reviewed range**: c805d268cfe9720396b5ed6cb9e70877006c5a1f..b925187e798be7cd3a1c9ce2dec7d9f8398bce6a

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python`, Python 3.13.13.

**Pre-run state**: clean detached worktree at b925187e; no staged or unstaged changes.

**Post-run state**: clean detached worktree at the same b925187e; no staged or unstaged changes.

| Command | Exit | Outcomes | Elapsed |
|---|---:|---|---:|
| `python -m pytest -q bootstrap/tests/test_upgrade.py bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_upgrade_side_door_parity.py --tb=short` | 1 | 208 passed, 1 failed; failure listed below | 33.38 s |
| `python -m pytest -q bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_lockfile_provenance.py bootstrap/tests/test_upgrade_refuses_hostile_project_data.py --tb=short` | 1 | 214 passed, 1 failed; failure listed below | 33.21 s |
| `python -m pytest -q bootstrap/tests/test_security_lint.py` | 0 | 11 passed, 0 failed, 0 skipped | 1.86 s |
| `python -m pytest -q bootstrap/tests/test_upgrade.py -k TrackedDirectoryCollisions --tb=short` | 0 | 4 passed, 0 failed | 3.17 s |
| `python scripts/claim_check.py bootstrap/UPGRADE.md` | 0 | No flags | — |
| `python scripts/check_cairn.py` | 0 | 198 Markdown files scanned, no issues | — |
| `python scripts/link_check.py` | 0 | 198 Markdown files scanned, no issues; 84 external links not probed | — |
| `python scripts/quality_gate.py --sub neutrality` | 0 | 0 failures, 43 informational matches | — |

**Mutation ledger**: the unmutated control `python -m pytest -q bootstrap/tests/test_upgrade.py -k TrackedDirectoryCollisions --tb=short` exited 0: 4 passed. In a separate copy of b925187e, removing real-directory classification made `python -m pytest -q bootstrap/tests/test_upgrade.py::TestTrackedDirectoryCollisions::test_plan_stage_and_recovery_preserve_mergeable_directory --tb=short` exit 1 with `IsADirectoryError` during `--plan` (killed). In another separate copy, disabling both apply directory blocks made the same recovery test accept the repaired live path and made `test_verbatim_directory_and_directory_after_stage_block_apply` raise `IsADirectoryError` after a directory appeared; the two-node pytest command exited 1 (both killed). No mutant survived; equivalence was not observed.

**Non-pass disposition**: `TestInitLock::test_review_pairs_leave_no_placeholder_the_install_filled` fails because the generated upstream-side buffer for the modules README differs outside slots. `test_apply_still_applies_a_review_area_of_plain_names` fails because its hand-planted destination already exists despite the stage's expected-absent record. Both exact nodes failed with the same results on clean baseline c805d268, before this change. They remain required-check failures and keep this plan open; they were not repaired here because they are unrelated to directory collisions.

**Plan-specific acceptance commands**: the focused tests exercise public `upgrade --plan`, `--stage` and `--apply`, including mergeable and verbatim paths, a folder appearing between plan classification and stage, a folder appearing after stage, override flags, preservation, blocked-stage recovery, and a fresh successful stage/apply after restoring the file. `sync_doc_snippets.py` was not run because no synced snippet changed.

**Known omissions**: the full suite and tree certification were not run; certification is separate and not authorized at this change boundary. The Maintainer-run AST re-anchor remains owed and was not authorized here. Arbitrary concurrent filesystem changes after a check are outside the claim. Independent code and Security Reviews remain owed. Do not archive until the two known required-test failures are resolved through their owning work and the reviews clear.

## Interim code review -- Codex GPT-6 -- 2026-10-30

**Reviewed commit**: b925187e798be7cd3a1c9ce2dec7d9f8398bce6a
**Reviewed range**: c805d268cfe9720396b5ed6cb9e70877006c5a1f..b925187e798be7cd3a1c9ce2dec7d9f8398bce6a
**Tier**: Internal
**Findings**: raised; interim, not a completed review
**Bounding**: WIDER RUN REQUIRED -- add coverage for tracked no-op destinations becoming directories after staging and verify the corrected public apply path.

**Foundations**:

1. **Does it do what it claims?** No: a tracked file omitted from the staged write set can become a directory after staging and apply succeeds, contrary to C1 and the guidance -- `bootstrap/_scaffold/upgrade.py:3419` and the falsification ledger below.
2. **Best alternative.** Record and check the applicable tracked destinations at apply, including no-op paths, while retaining the existing containment and retired-record rules -- `bootstrap/_scaffold/upgrade.py:1219` and C1.
3. **What would show it wrong?** The controlled post-stage transition and its result are in the falsification ledger below.

**P1 -- A post-stage directory at a no-op tracked path does not block apply.** Stage omits a destination when its current bytes equal the planned result; apply checks only `staged_meta`, so that destination is never checked. In a scratch installation, after staging, replace an omitted tracked file with a folder containing adopter data and run apply with `--force`: apply returns 0 and advances, instead of refusing the entire apply before metadata advancement. The folder contents survived this run, but the accepted block and recovery contract did not. Include all applicable tracked paths in the apply observation and add a public-command regression covering this case.

**Falsification ledger**: In a detached copy of b925187e, added a scratch test using `_install`, `_diverge_base`, public stage and apply, and selected an existing tracked regular file absent from `staged_files`. Replaced `.agents/skills/_data/vendor_targets.yml` with a directory containing `data`, then invoked apply with `--force`. `/Users/kendal30/conda_envs/lhm/bin/python -m pytest -q -s bootstrap/tests/test_upgrade.py::test_review_noop_tracked_path_becomes_directory --tb=short` on Python 3.13.13 failed the expected refusal assertion: apply returned 0 (1 failed). This is a controlled change between commands, not an arbitrary concurrent change after a check. The scratch test was not added to the implementation.

Coverage: inspected the recorded Boundary B and the implementation's classification, staging and apply write-set checks, and independently challenged the no-op post-stage case. This is an interim pass: the two mapped required failures remain open, and other planned observation points, recovery, hostile metadata, symlink behavior, independent Security Review, and any corrected implementation were not independently tested here. No implementation verification or completion is claimed; the plan remains implementing.

## Interim code review follow-up -- Codex GPT-6.1 Sol -- 2026-10-30

**Reviewed commit**: a584f84d3f749b947a71e2399aa0578502208ff1
**Reviewed range**: b925187e798be7cd3a1c9ce2dec7d9f8398bce6a..a584f84d3f749b947a71e2399aa0578502208ff1
**Tier**: Internal
**Findings**: none in this follow-up; interim, not a completed code review
**Bounding**: ACCEPTED for the earlier no-op destination finding only; final Boundary B and required mapped failures remain open.

**Foundations**:

1. **Does it do what it claims?** The correction records applicable planned destinations, including no-op files, validates their stage names, and checks them before apply writes; the public regression and a distinct nested verbatim probe both refuse the post-stage directory -- `bootstrap/_scaffold/upgrade.py:1393`, `:3155`, `:3424` and the ledger below.
2. **Best alternative.** The new stage list reuses the existing path validation and apply refusal, and is smaller than adding a second planning pass at apply; no further change is recommended for this finding -- `bootstrap/_scaffold/upgrade.py:3151-3190`, `:3410-3441`.
3. **What would show it wrong?** A no-op destination becoming a directory after staging must make public apply fail without lockfile advancement or content loss; the ledger below records two attempts.

**Falsification ledger**: A separate local clone at a584f84d was used because the shared repository's Git metadata did not permit a detached worktree. The unmodified focused regression and hostile stage-name selection passed: `/Users/kendal30/conda_envs/lhm/bin/python -m pytest -q bootstrap/tests/test_upgrade.py::TestTrackedDirectoryCollisions::test_noop_tracked_file_becoming_directory_blocks_apply bootstrap/tests/test_upgrade_refuses_hostile_project_data.py -k 'directory_observed or noop_tracked_file_becoming_directory_blocks_apply' --tb=short` (9 passed, 182 deselected; Python 3.13.13). In that clone, a scratch public-command test changed a different, nested *verbatim* no-op destination into a directory after staging, then applied with both overrides. Apply returned 1, named the directory, preserved its nested bytes, left the lockfile unchanged, and retained the stage. Its invocation passed; importing an existing test class also collected 27 unrelated tests, for 28 passed total. The scratch test was not added to the implementation.

**Covered**: claims and public entry (#1-2), no-op and nested-path edge cases (#3), unconditional refusal (#4), reuse (#5), agreement with C1 and `bootstrap/UPGRADE.md` (#6), plan status and required evidence (#7), accepted scope (#8), and the earlier P1 satisfier (#9), at the code and commands cited above. **Not covered / low confidence**: no independent check of every original observation point, symlink precedence, arbitrary concurrent changes, or the full mapped run. The two recorded mapped failures, final-commit Boundary B, and separate Security Review are unresolved; the plan stays implementing.

## Interim code Security Review -- Codex GPT-6 -- 2026-10-30

**Reviewed commit**: a584f84d3f749b947a71e2399aa0578502208ff1
**Reviewed range**: c805d268cfe9720396b5ed6cb9e70877006c5a1f..a584f84d3f749b947a71e2399aa0578502208ff1
**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised; interim, not a completed review
**Bounding**: WIDER RUN REQUIRED -- verify refusal of incomplete or older stages and the complete applicable tracked destination set.

**Foundations**:

1. **Does it do what it claims?** No: a stage missing the new destination list can advance while an unchanged tracked destination is a directory -- `bootstrap/_scaffold/upgrade.py:3155`, `:3424`, and the ledger below.
2. **Best alternative.** Fail closed on incompatible or incomplete stages, or independently establish the complete applicable tracked destination set before apply; preserve containment checks -- `bootstrap/_scaffold/upgrade.py:3153` and `:3425`.
3. **What would show it wrong?** The missing-field public-apply probe and outcome are in the falsification ledger below.

**P1 -- A stage without the new observation list bypasses the post-stage block.** Apply accepts missing `directory_observed` as an empty list and checks only that list and staged writes. A stage created by the preceding implementation naturally lacks this field; removing it from project-controlled stage metadata has the same effect. An unchanged tracked file omitted from `staged_files` can then become a directory and apply advances the lock and base cache. Require a fresh stage when the needed observation data is absent or otherwise ensure the checked set is complete. Include incomplete and pre-change stage cases in the public-path verification.

**Falsification ledger**: In an isolated archive of a584f84d, modified the existing `TestTrackedDirectoryCollisions::test_noop_tracked_file_becoming_directory_blocks_apply` to remove `directory_observed` from the freshly written stage metadata before replacing the selected unchanged tracked file with a directory. `/Users/kendal30/conda_envs/lhm/bin/python -m pytest -q bootstrap/tests/test_upgrade.py::TestTrackedDirectoryCollisions::test_noop_tracked_file_becoming_directory_blocks_apply --tb=short` on Python 3.13.13 failed (1 failed): public apply with both override flags returned 0 and reported lockfile and base-cache advancement. This models the missing field in an older stage; it does not measure arbitrary concurrent changes.

Coverage: inspected the final change's metadata validation and directory gate and challenged an omitted observation list. This is an interim pass: final-commit Boundary B is absent, two mapped required test failures remain open, and other stage metadata changes, containment, symlinks, recovery and corrected implementation were not independently tested here. No Security Review clearance or implementation verification is claimed.

## Interim code review follow-up -- Codex GPT-6.1 Sol -- 2026-10-30

**Reviewed commit**: a6703b494944fdbe349d2d2173b4899af1cef8ca
**Reviewed range**: a584f84d3f749b947a71e2399aa0578502208ff1..a6703b494944fdbe349d2d2173b4899af1cef8ca
**Tier**: Internal
**Findings**: raised; interim, not a completed code review
**Bounding**: WIDER RUN REQUIRED -- establish that apply checks the applicable tracked destinations even when the project-controlled observation list is present but incomplete.

**Foundations**:

1. **Does it do what it claims?** The new guard refuses a missing `directory_observed` field, but an empty field lets the original post-stage no-op collision advance under both overrides -- `bootstrap/_scaffold/upgrade.py:3198`, `:3428` and the ledger below.
2. **Best alternative.** Validate the stage's observation list against an independently established applicable tracked set, or use that set directly at apply; retain the early missing-field refusal -- `bootstrap/_scaffold/upgrade.py:1393`, `:3198`, `:3424`.
3. **What would show it wrong?** A controlled empty-list stage and directory transition should refuse apply before lockfile advancement; the public-command result is in the ledger below.

**P1 -- A present but empty observation list bypasses the block.** Apply requires the key but accepts `[]`. In a stage with a tracked no-op destination absent from `staged_files`, replacing its observation list with `[]` and then changing that destination to a directory makes apply return 0 with `--force --ack-review-only`. A project-controlled stage can lose one or all observations, and the list's presence does not establish its completeness. The satisfier is a guard derived from an independent set of applicable tracked destinations, with public-path tests for incomplete stage metadata; the missing-field regression remains useful.

**Falsification ledger**: In a separate local clone at a6703b49, changed only the setup of `TestTrackedDirectoryCollisions::test_noop_tracked_file_becoming_directory_blocks_apply[True]` from deleting `directory_observed` to setting it to `[]`. `/Users/kendal30/conda_envs/lhm/bin/python -m pytest -q 'bootstrap/tests/test_upgrade.py::TestTrackedDirectoryCollisions::test_noop_tracked_file_becoming_directory_blocks_apply[True]' --tb=short` on Python 3.13.13 failed: public apply returned 0 where refusal was asserted (1 failed). Restoring the test file and running the unmodified two-case node passed (2 passed). This measures a controlled stage edit and path transition, not a concurrent change after a check. The scratch edit was not added to the implementation.

**Covered**: claims and public path (#1-2), empty-list edge case (#3), fail-closed behavior (#4), reuse of existing stage validation (#5), C1 and `bootstrap/UPGRADE.md:242` contract (#6), open-plan placement (#7), accepted preservation scope (#8), and the guard/test satisfier (#9), at the cited lines and ledger commands. **Not covered / low confidence**: a one-path omission, each applicable destination, symlink precedence, other original observation points, full mapped verification, and Security Review clearance. The two mapped failures and final Boundary B remain open; the plan stays implementing.

## Sequencing amendment -- Codex GPT-6 -- 2026-10-30

The Maintainer clarified in chat, relayed by the coordinating agent:

> We only repin and reanchor at version cuts or as I ask

> The plan should not require that

Accordingly, earlier statements in this plan that require repinning or
re-anchoring are superseded as plan requirements. Neither ceremony is a
prerequisite for completing or archiving this plan. The new baseline is a
v0.6 board item; repinning and re-anchoring occur at a version cut or when
the Maintainer asks. This amendment does not authorize a ceremony or waive
other checks, reviews, or acceptance criteria. Earlier evidence remains a
record of what was known and done at the time.
