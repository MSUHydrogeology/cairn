# Plan: Refuse linked installed files during lockfile migration

**Source proposal**: dev/proposals/archive/2026-10-30-codex-init-lock-linked-files.md
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Lockfile migration will refuse linked installed files before hashing them, so a link cannot supply another file's digest in a stable project tree.

## Source proposal

The Maintainer accepted the revised proposal at `06af4aeb`: guard every mapped destination in `upgrade --init-lock` before its existence test or read, including planted leaf, dangling and parent links. Keep the existing lockfile format, vendor-wrapper alias behavior and ordinary-file migration. Give a usable file-or-directory remedy and document the limit under concurrent path replacement and the separate fidelity-manifest reader.

## Scope

Change `bootstrap/_scaffold/upgrade.py`'s mapped-file loop, shared `_refuse_if_linked` remedy and `_cmd_init_lock` docstring; add public tests in `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py`. Update descriptive `bootstrap/UPGRADE.md` and the existing `_cmd_init_lock` entry in `bootstrap/_scaffold/SECURITY_MUTATIONS.md`. No doctrine or install-manifest change. A link elsewhere in a project is unaffected. This check is for planted links in a stable tree; separate check and read operations do not prevent concurrent replacement. `_manifest_cairn_commit` remains a separate linked-manifest reader and must be disclosed, not silently claimed as protected.

**Reuse.** Reuse `_refuse_if_linked` and its `_assert_safe_write` path-component check; preserve `_resolve_vendor_wrapper`'s linked-alias skip. Searches for `init_lock`, `_refuse_if_linked`, `_manifest_cairn_commit` and `SECURITY_MUTATIONS.md` found those readers and the tests mapped below; add no second path policy.

### Documentation / doctrine surface

No doctrine surface. The upgrade guide and engine security behavior table describe what the software does; the docstring identifies this command's covered paths and limit.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Guard mapped destinations, correct shared remedy and documentation, add public tests | Both required plan reviews | Engine, tests and descriptive text |

## Acceptance criteria

C1: With a complete profile and no lockfile, stationary inside and outside `AGENTS.md` leaf links, a dangling `AGENTS.md` link, and a linked `docs/` parent above mapped `docs/DOCUMENTATION_PLAN.md` each return exit 2 before that mapped path is read. Each refusal names the mapped path without revealing the target, leaves project and outside snapshots unchanged, and writes no lockfile. The parent case gives a workable directory remedy; existing shared-helper refusals also name an actionable file-or-directory remedy. A regular project file migrates, with its own digest; existing vendor-wrapper alias behavior remains. The public outside-link test must first establish the unguarded digest reproduction and then kill a mutation removing the new guard. The guide and docstring state the stable-tree limit and independent manifest-reader gap. No scientific result is touched.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: run `python -m pytest bootstrap/tests/test_upgrade_refuses_hostile_project_data.py` for public refusal and ordinary controls, including the five existing assertions of the shared helper's old remedy at lines 291, 318, 387, 501 and 941; update those assertions for the accepted file-or-directory wording. Run `python -m pytest bootstrap/tests/test_upgrade.py::TestInitLock bootstrap/tests/test_upgrade.py::TestInitLockFullProfile bootstrap/tests/test_lockfile_provenance.py` for migration, vendor alias and lockfile consumers; `python -m pytest bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_upgrade_module.py` for the shared refusal and engine surface. Search changed files for other readers and byte pins, then run their owning checks. For the behavior-table change, include `python -m pytest bootstrap/tests/test_security_leaf.py`. Run `python scripts/quality_gate.py --sub neutrality --sub redundancy`, `python scripts/claim_check.py` on each changed Markdown file, `python scripts/check_cairn.py`, and `python scripts/link_check.py`. Run `python scripts/sync_doc_snippets.py --check` if its trigger shows the guide contains a synced block. On an isolated copy, compare the unmutated public test with a mutation removing the mapped-file guard; report control, killed/survived result and any equivalence with evidence. Exercise the public `bootstrap/scaffold.py upgrade --target <scratch-repo> --init-lock` refusal and regular control.

Boundary B: **wide**, because the scaffold engine and lockfile migration are protected contract surfaces. After the last implementation commit, repeat the mapped owning families, public command cases and standing engine/prose gates on one unchanged clean commit under canonical Python 3.13.x. Record SHA and range, clean pre/post state, interpreter, commands and counts, elapsed time, tokens or `unknown`, non-pass disposition, omissions and `Certified by: pending`. Boundary C is independent targeted falsification by a different code reviewer, with a bounding verdict; a separate Security Review remains owed. Full-tree certification and the Maintainer's AST re-anchor are separate ceremonies, not per-plan checks.

## Plan review -- Codex GPT-6 (Internal Reviewer) -- 2026-10-30

```
Reviewed commit: 45cd0c2f7b7249c3e982363079b1d19383041a1a
Target: Source proposal through Verification
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised
**Verdict**: ACCEPT WITH ADVICE
**Elapsed**: 8 minutes; **Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes. The plan preserves the accepted stable-tree refusal and names the independent manifest-reader limit; the mapped loop currently reaches `exists()` and `read_bytes()` without a link check -- proposal Decision at `06af4aeb`; `bootstrap/_scaffold/upgrade.py:1679-1718`.
2. **Best alternative.** One guard in the mapped loop and a corrected shared remedy is simpler than a new path policy and delivers the same outcomes -- `bootstrap/_scaffold/upgrade.py:154-174`; `bootstrap/_scaffold/security.py:110-155`; plan Scope.
3. **What would show it wrong.** A public outside-link run still hashing the target, a dangling or `docs/` link passing, a changed snapshot, or an ordinary migration failing would defeat the plan -- plan Acceptance criteria; `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py:270-349`.

**Advice R1 — update existing remedy assertions with the shared wording.** Five assertions in `test_upgrade_refuses_hostile_project_data.py` require the old phrase “Replace it with a regular file”; the accepted file-or-directory remedy will make them fail even when the new refusal works. Update those existing assertions to check the actionable remedy alongside the new cases. This is within the named test file and Boundary A command; it does not widen scope (`bootstrap/tests/test_upgrade_refuses_hostile_project_data.py:291`, `:318`, `:387`, `:501`, `:941`).

**Covered**: claims and fail-closed order (`upgrade.py:154-174,1679-1718`); public path and edge cases (`test_upgrade_refuses_hostile_project_data.py:270-349`); design and reuse (`security.py:110-155`; plan Scope); document drift (`UPGRADE.md:430-441`; `SECURITY_MUTATIONS.md:120`); lifecycle, scope and satisfier (proposal Decision; plan Sequence, Acceptance criteria, Verification; R1). **Not covered / low confidence**: no implementation, mutation, public run or concurrent replacement was exercised; the separate Internal Security Review remains owed.

## Plan review -- Codex (gpt-6.1-sol, Security Review) -- 2026-10-30

```
Reviewed commit: 019d9620
Target: Source proposal through Verification
Prior findings: none
Assurance path: high-assurance
Elapsed time: approximately 2 minutes
Token use: unknown
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes: the mapped-path guard addresses planted links in a stable tree, with the concurrent replacement limit and separate manifest reader disclosed -- plan Scope and C1; `bootstrap/_scaffold/security.py::_assert_safe_write`.
2. **Best alternative.** Reuse the existing component guard and correct its remedy; hashing link text changes the lockfile contract, while a new policy adds complexity -- accepted proposal Alternatives considered; `bootstrap/_scaffold/upgrade.py::_refuse_if_linked`.
3. **What would show it wrong?** A stationary leaf, dangling or parent link reaching the mapped read, a refusal changing either tree, or an ordinary file failing migration defeats the contract -- plan C1; `bootstrap/_scaffold/upgrade.py::_cmd_init_lock`.

The plan places the guard before both existence and read, including dangling links, and tests the `docs/` parent without being intercepted by the earlier profile guard. The outside-digest positive control and guard-removal mutation challenge whether the public test reaches the vulnerable read. The wide mapping covers the shared helper, migration consumers, descriptive guidance and security behavior table; its named families bound cost without claiming full-tree certification -- plan Scope, C1 and Verification; `bootstrap/_scaffold/security.py::_assert_safe_write`.

Coverage: assessed source and target trust, refusal ordering, failure state, recovery wording, public entry point, consumers, verification and accepted scope against the named commit. No implementation, migration, mutation, concurrent replacement, full suite or re-anchor was run; the separate manifest reader and race remain outside this protection.

## Response to plan review -- Codex GPT-6.1 Sol (Strategy) -- 2026-10-30

Both required reviews accepted the plan. R1 accepted: C1 now includes the existing shared-helper refusals, and Boundary A names the five assertions to update in the already-scoped public test file. The Security Review had no findings. The operative plan is ready to implement; no second plan-review pass is requested. Elapsed: approximately 2 minutes; tokens: unknown.

## Implementation verification -- Codex GPT-6.1 Sol (Implementation) -- 2026-10-30

**Boundary B**: wide
**Certified by**: pending
**SHA/range**: `89206da8ed76baff45ce404028e4fb55d8d31b88` (final tested candidate; implementation commits `e9adb1f9`, `7aa7417b`, `89206da8`)
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` -- Python 3.13.13
**Tree state**: clean before and after in a separate clone of the candidate commit.
**Elapsed**: approximately 40 seconds; **Tokens**: unknown.

**Mapped checks**

- `python -m pytest bootstrap/tests/test_upgrade_refuses_hostile_project_data.py` -- 195 passed. This public suite invokes `bootstrap/scaffold.py`; it includes outside, inside and dangling mapped leaves, the linked `docs/` parent, ordinary mapped digest, refusal snapshots, no lockfile, and prior shared-helper cases.
- `python -m pytest bootstrap/tests/test_upgrade.py::TestInitLock bootstrap/tests/test_upgrade.py::TestInitLockFullProfile bootstrap/tests/test_lockfile_provenance.py` -- 44 passed.
- `python -m pytest bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_upgrade_module.py` -- 103 passed.
- `python -m pytest bootstrap/tests/test_security_leaf.py` -- 15 passed.
- `python scripts/quality_gate.py --sub neutrality --sub redundancy` -- pass; both subgates reported zero failures (neutrality: 43 informational notes; redundancy: one pre-existing R6 note).
- `python scripts/claim_check.py bootstrap/UPGRADE.md`, `python scripts/claim_check.py bootstrap/_scaffold/SECURITY_MUTATIONS.md`, and `python scripts/claim_check.py dev/plans/2026-10-30-init-lock-linked-files.md` -- all passed.
- `python scripts/check_cairn.py` -- passed, 199 Markdown files scanned; 94 external links not probed.
- `python scripts/link_check.py` -- passed, 199 Markdown files scanned; 95 external links not probed.
- `python scripts/sync_doc_snippets.py --check` -- passed, 476 documents scanned with no drift.

**Mutation**: unmutated control was the final candidate and the mapped suites above passed. Total: 1 mutation; killed: 1. Removing the new mapped-path guard in an isolated mutant let `--init-lock` return 0 and produced an `AGENTS.md` lock digest equal to the outside target's measured SHA-256. The public outside-link node then failed because it expected exit 2 and received exit 0. Survivors: none. Measured equivalents: none.

**Non-pass disposition**: an earlier run on `7aa7417b` had 194 passed and one failed assertion because the vendor-wrapper alias uses its own unchanged remedy rather than `_refuse_if_linked`'s shared remedy. The assertion was corrected in `89206da8`; all mapped checks above then passed. No known mapped check remains unmet.

**Omissions**: no full-tree certification or Maintainer AST re-anchor; both remain separate ceremonies. No concurrent path replacement was exercised; the check/read race and separate fidelity-manifest reader remain outside this change. The canonical Python 3.13.13 interpreter was invoked explicitly in the separate clone.

## Code review -- Codex GPT-6.1 Sol (Internal Reviewer) -- 2026-10-30

```
Reviewed commit: 89206da8 (implementation); 46a5a191 (verification)
Target: C1 and Boundary B
Prior code findings: none
Elapsed: approximately 5 minutes; tokens: unknown
```

**Tier**: Internal. **Verdict**: REVISE. **Bounding**: WIDER RUN REQUIRED.

**Foundations**

1. **Should this happen as framed?** Yes. The guard precedes `exists()` and `read_bytes()` in `bootstrap/_scaffold/upgrade.py:1793-1800`; the public linked-path and ordinary controls passed (5 tests, Python 3.13.13).
2. **Best alternative.** Reuse `_refuse_if_linked` for leaf and ancestor checks (`upgrade.py:156-175`; `security.py:110-155`). Atomic reads address a wider threat than C1 accepts.
3. **What would show it wrong?** A planted link migrating, changed snapshots, or an ordinary file failing would defeat C1. The public outside-link test failed under guard removal (exit 0 instead of 2); the unmutated control passed.

**R1 — blocking: complete guide-reader checks.** Boundary A requires finding changed-file readers and running owning checks. The Boundary B record lists none for `bootstrap/UPGRADE.md`, yet `test_install_time_onboarding.py:372,384`, `test_review_stance_in_shipped_files.py:1487,1497`, `test_upgrade_removes_retired_files.py:1783`, `test_verify_integrity.py:1439,1446`, and `test_next_session_local_note.py:526` read it. Four guide-reading nodes passed in the reviewer's isolated copy; the author still owes clean-commit Boundary B evidence. Run and record relevant owning nodes; explain omissions.

**Falsification ledger.** Surfaces: mapped loop, helper, alias resolver, guide and behavior table (`upgrade.py:1531-1580,1792-1823`; `SECURITY_MUTATIONS.md:120`). Edge attempt: outside, inside, dangling, linked-parent and ordinary digest passed (5 tests). Mutation: unmutated control 5 passed; one guard-removal mutant killed by outside-link node, 1 failed; survivors and measured equivalents none. Residual: no concurrent swap, full suite, re-anchor or per-destination mutation. Separate code Security Review remains owed.

**Covered**: claims and fail-closed order (`upgrade.py:1793-1800`); public entry and edges (5 public nodes); design/reuse (`security.py:110-155`, `upgrade.py:1531-1580`); document consistency/drift (`UPGRADE.md:430-452`, `SECURITY_MUTATIONS.md:120`); lifecycle/scope (`plan C1`, Boundary B); satisfier (R1). **Not covered / low confidence**: concurrent replacement, every mapping mutated separately, unrelated upgrade actions and certification ceremonies.
