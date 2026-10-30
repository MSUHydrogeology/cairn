# Plan: Refuse linked installed files during lockfile migration

**Source proposal**: dev/proposals/archive/2026-10-30-codex-init-lock-linked-files.md
**Status**: awaiting-plan-review
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

C1: With a complete profile and no lockfile, stationary inside and outside `AGENTS.md` leaf links, a dangling `AGENTS.md` link, and a linked `docs/` parent above mapped `docs/DOCUMENTATION_PLAN.md` each return exit 2 before that mapped path is read. Each refusal names the mapped path without revealing the target, leaves project and outside snapshots unchanged, and writes no lockfile. The parent case gives a workable directory remedy. A regular project file migrates, with its own digest; existing vendor-wrapper alias behavior remains. The public outside-link test must first establish the unguarded digest reproduction and then kill a mutation removing the new guard. The guide and docstring state the stable-tree limit and independent manifest-reader gap. No scientific result is touched.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: run `python -m pytest bootstrap/tests/test_upgrade_refuses_hostile_project_data.py` for public refusal and ordinary controls; `python -m pytest bootstrap/tests/test_upgrade.py::TestInitLock bootstrap/tests/test_upgrade.py::TestInitLockFullProfile bootstrap/tests/test_lockfile_provenance.py` for migration, vendor alias and lockfile consumers; `python -m pytest bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_upgrade_module.py` for the shared refusal and engine surface. Search changed files for other readers and byte pins, then run their owning checks. For the behavior-table change, include `python -m pytest bootstrap/tests/test_security_leaf.py`. Run `python scripts/quality_gate.py --sub neutrality --sub redundancy`, `python scripts/claim_check.py` on each changed Markdown file, `python scripts/check_cairn.py`, and `python scripts/link_check.py`. Run `python scripts/sync_doc_snippets.py --check` if its trigger shows the guide contains a synced block. On an isolated copy, compare the unmutated public test with a mutation removing the mapped-file guard; report control, killed/survived result and any equivalence with evidence. Exercise the public `bootstrap/scaffold.py upgrade --target <scratch-repo> --init-lock` refusal and regular control.

Boundary B: **wide**, because the scaffold engine and lockfile migration are protected contract surfaces. After the last implementation commit, repeat the mapped owning families, public command cases and standing engine/prose gates on one unchanged clean commit under canonical Python 3.13.x. Record SHA and range, clean pre/post state, interpreter, commands and counts, elapsed time, tokens or `unknown`, non-pass disposition, omissions and `Certified by: pending`. Boundary C is independent targeted falsification by a different code reviewer, with a bounding verdict; a separate Security Review remains owed. Full-tree certification and the Maintainer's AST re-anchor are separate ceremonies, not per-plan checks.
