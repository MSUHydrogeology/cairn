# Dispatcher content scan mutation ledger

The measured unmutated control is `bootstrap/tests/test_security_verification.py::TestRegistryIntegrity::test_content_entry_binds_every_immutable_apparatus_member`: all five files bind successfully. Each row below is a separate parametrized mutation in `test_content_apparatus_member_failure_refuses_before_launch`; that case first repeats the valid binding control, applies one mutation, then verifies binding degrades and `_evaluate_capability` reports `child_launched is False`.

| Bound member | Mutation | Result |
|---|---|---|
| `templates/modules/default-on/run_security_verification.py` | missing lock record | killed |
| `templates/modules/default-on/run_security_verification.py` | changed bytes | killed |
| `templates/modules/default-on/run_security_verification.py` | symlink | killed |
| `templates/modules/default-on/run_security_verification.py` | unknown record key | killed |
| `templates/modules/default-on/run_security_verification.py` | wrong-typed `living_state` | killed |
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
