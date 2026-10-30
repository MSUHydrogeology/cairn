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
