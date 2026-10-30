# Plan: Block tracked upgrade directory collisions

**Source proposal**: dev/proposals/archive/2026-10-29-codex-upgrade-directory-collisions.md
**Status**: awaiting-plan-review
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

Boundary A: use canonical Python 3.13 and run `python -m pytest bootstrap/tests/test_upgrade.py bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_upgrade_side_door_parity.py` for tracked upgrades, retired paths and containment; include new tests in the owning files. Run `python -m pytest bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_lockfile_provenance.py` for addition blocking and metadata consumers. Search actual readers and extend this map if needed. Split selections within the broad-run guard's file limit and reconcile the executed union without an override. Run `python -m pytest bootstrap/tests/test_security_lint.py` for the engine security gate; a skip is an unmet check.

Exercise `python bootstrap/scaffold.py upgrade` public `--plan`, `--stage`, and `--apply` paths in a scratch installation, including resolution and restaging; check command help for exact arguments. Run `python scripts/claim_check.py` on changed prose, `python scripts/check_cairn.py`, `python scripts/link_check.py`, and `python scripts/quality_gate.py --sub neutrality`; run `python scripts/sync_doc_snippets.py` if synced snippets change. Record the two mutation controls and failures in separate scratch copies.

Boundary B is **wide** for the engine contract and security boundary: run the mapped owning families, public paths, mutations and standing gates on a clean, unchanged final implementation commit under the canonical interpreter. Record tested SHA and reviewed range, interpreter, clean pre/post state, commands, outcomes, timing, non-pass dispositions, omissions, and **Certified by**: pending. Certification is separate. Boundary C is independent targeted falsification by the code reviewer, including the observation points and stated race limit; the reviewer records bounding and any missing check. The AST re-anchor follows its existing Maintainer-run ceremony, separately authorized.
