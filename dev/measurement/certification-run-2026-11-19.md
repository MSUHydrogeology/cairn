# Certifying runs of 2026-11-19 (v0.8 candidate, Mac)

A record of two full certifying runs on the Mac and the repairs between them. Interpreter: Python 3.13.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`), pytest 9.0.3. Commands: the release block of `release/RELEASE_PROCESS.md` (`CAIRN_FULL_SUITE=1 python -m pytest tests --quality-gate-shuffle-seed=0 --junitxml=<report>`, then `python release/check_release_test_members.py`), then `python tests/quality_gate.py --sub neutrality --sub redundancy` and `python tests/check_cairn.py`. Each run started on a clean committed tree. This is evidence for the release, not the strict native records (those follow the re-anchor, at the final commit).

| Run | Commit | Started | Pytest | Member check | Quality gate | Document check |
|---|---|---|---|---|---|---|
| 1 | `a6847acc` | 11:34 | 195 failed, 18 errors, 5,666 passed, 82 skipped in 58:48 | refused: `tests/test_security_capability_install.py` has a failed case | passed | passed |
| 2 | `d9e7629a` | 13:29 | **1 failed**, 5,894 passed, 66 skipped in 60:41 | refused: `tests/test_ast_attest.py` has a failed case | passed | passed |

**Run 1** failed in 46 files. The causes were the 0.8 layout move: stale paths (`tools/` to `dev/tools/`, `bootstrap/tests` to `tests`), tests that count parent folders to find the repository root, gate tests that needed a previous anchor in the new layout, one installed-file count (14 to 16, because commit `d06c0fc4` added a README per group), and stale installer hints. Three agents repaired them in about 29 commits (`a6847acc..d9e7629a`), each cluster with one deliberate break confirmed and restored. The gate tests that needed a real new-layout anchor now build a synthetic previous anchor in a scratch clone and touch nothing in the live repository or its refs. One security assertion was weakened (`test_check_runs_against_the_live_repo_and_reports` now needs a reasoned refusal line, not the word "bootstrap", because the live anchor `e5b7fd0a` still holds the old layout). A read-only Opus Security review of the gate-area repairs (2026-11-19) was ACCEPT with no blocking findings; it recommends tightening that assertion after the Maintainer re-anchors.

**Run 2** has one failure: `tests/test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package`. Cause, measured: one symbol, `FunctionDef:main` in `install/_scaffold/cli.py`, changed (baseline `98d08f97621544ba`, now `7fe8882cf74adcdc`) because the repairs corrected three installer hint strings (`python tools/intent.py ...` to `python dev/tools/intent.py ...`). The test passed in run 1. It needs a reviewed AST baseline correction, not a code revert (the old hints named a path that no longer exists).

**Not run here.** The strict native records (Mac and Windows) and their join; the candidate secrets scans; the Windows full suite. The 9 older Windows contract-test failures named in `dev/proposals/2026-11-19-codex-native-release-membership.md` are unchanged (8 need `bash`, one timing flake).

**Open after this record.** The AST baseline correction for the one symbol; then the Maintainer's grouped re-anchor.
