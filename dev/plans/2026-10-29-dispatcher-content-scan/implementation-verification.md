# Dispatcher content scan mutation ledger

The measured unmutated control is `bootstrap/tests/test_security_verification.py::TestRegistryIntegrity::test_content_entry_binds_every_immutable_apparatus_member`: all five files bind successfully. Each row below is a separate parametrized mutation in `test_content_apparatus_member_failure_refuses_before_launch`; that case first repeats the valid binding control, applies one mutation, then verifies binding degrades and `_evaluate_capability` reports `child_launched is False`.

| Bound member | Mutation | Result |
|---|---|---|
| `scripts/content_scan_runner.py` | missing lock record | killed |
| `scripts/content_scan_runner.py` | changed bytes | killed |
| `scripts/content_scan_runner.py` | symlink | killed |
| `scripts/content_scan_runner.py` | unknown record key | killed |
| `scripts/content_scan_runner.py` | wrong-typed `living_state` | killed |
| `scripts/content_scan.py` | missing lock record | killed |
| `scripts/content_scan.py` | changed bytes | killed |
| `scripts/content_scan.py` | symlink | killed |
| `scripts/content_scan.py` | unknown record key | killed |
| `scripts/content_scan.py` | wrong-typed `living_state` | killed |
| `scripts/content_scan_roots.txt` | missing lock record | killed |
| `scripts/content_scan_roots.txt` | changed bytes | killed |
| `scripts/content_scan_roots.txt` | symlink | killed |
| `scripts/content_scan_roots.txt` | unknown record key | killed |
| `scripts/content_scan_roots.txt` | wrong-typed `living_state` | killed |
| `scripts/content_scan_residuals.txt` | missing lock record | killed |
| `scripts/content_scan_residuals.txt` | changed bytes | killed |
| `scripts/content_scan_residuals.txt` | symlink | killed |
| `scripts/content_scan_residuals.txt` | unknown record key | killed |
| `scripts/content_scan_residuals.txt` | wrong-typed `living_state` | killed |
| `scripts/content_scan_allowlist.txt` | missing lock record | killed |
| `scripts/content_scan_allowlist.txt` | changed bytes | killed |
| `scripts/content_scan_allowlist.txt` | symlink | killed |
| `scripts/content_scan_allowlist.txt` | unknown record key | killed |
| `scripts/content_scan_allowlist.txt` | wrong-typed `living_state` | killed |

The declared control proves the accepted member set binds before each mutation is introduced. The one-member mutations do not test an attacker replacing both a file and its lock record.

Child evidence and result controls were exercised in the mapped implementation tests: invalid UTF-8/JSON, identifier mismatch, exit/result disagreement, timeout, output cap, terminal-control escaping, raw output isolation, and aggregate precedence are in `TestDispatchBehavior`. Accepted residuals, empty/stale/bad audit evidence, direct invocation, actual clean and flagged content, fresh default and opt-out installations, API/web selections, and scoped finalize/upgrade are covered by `TestComposition`, `TestRunnerExitContract`, `TestAuditRootsManifest`, and `test_scoped_finalize_updates_only_reviewed_policy_and_dispatcher_accepts_it`.

## Verification range correction -- after code review dee39093

The runner row above is `scripts/content_scan_runner.py`, the `entry.runner_repository_path` used by the positive-control and mutation test. The first version of this ledger named the installed verification runner; that label was wrong.

The first Boundary B record tested commit `3dcb5806a0442b959a81cc3287a9ded9c5b44a4a` but described `a6c151f1..3dcb5806` without separating the concurrent module-discovery work. That interval includes `d3c9b80a` and `258dbb26`, which change install/onboarding behavior and its owning tests. On a clean detached clone at `3dcb5806`, the author additionally ran:

`/Users/kendal30/conda_envs/lhm/bin/python3.13 -m pytest -q bootstrap/tests/test_install_time_onboarding.py bootstrap/tests/test_onboarding_slot_substitution.py bootstrap/tests/test_presets.py bootstrap/tests/test_scaffold.py` — **182 passed in 4.96 s**.

The module-discovery implementation and compatibility changes have their own independent wide record: [module-discovery implementation verification](../2026-10-29-module-discovery-activation.md#implementation-verification----codex----2026-10-29), committed in `f51b84b1528bcd67ad4b5a3474a781b3351f7ae2`. It covers `a6c151f1..eee603a6`, including the install/onboarding owners above, on a clean Python 3.13.13 worktree: **812 passed**, plus its stated gates and four mutation controls. The module run is independently authored evidence, not this dispatcher author's run.

The integrated tested candidate is therefore `eee603a67512f73c1e6932334057faa3474cf14e`; the dispatcher implementation commits are `dc309b0ee7efa68cc345f6d7776e41df3e1f9dbf` and `3dcb5806a0442b959a81cc3287a9ded9c5b44a4a`. The intervening module commits remain separately attributed in the module plan. The author's 290 + 38 + 182 results are on clean candidate `3dcb5806`; the module agent's 812-test result is on later integrated candidate `eee603a6`. No test result is attributed to the wrong author or commit.
