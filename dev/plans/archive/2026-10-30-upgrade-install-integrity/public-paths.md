# Public paths and wording contract


Each route uses `python bootstrap/scaffold.py` with a scratch target; tests assert the escaped supplied value and the stated outcome, not only an exit code. Keep existing surrounding wording where possible; the following phrases are the minimum operator-facing contract, and documentation and assertions must agree.

| Command and selected input | Test home | Required message or outcome |
|---|---|---|
| `upgrade --target <repo> --plan`, `--stage`, `--apply`: matching, legacy, missing, malformed, altered, unreadable and invalid UTF-8 bases, including crafted loss | `bootstrap/tests/test_upgrade.py` | Invalid ancestor: “review-only”; no automatic merge or replacement. Matching control merges. |
| Same stage/apply; change cache or digest after stage and inject change after initial apply check; inject read/write failures | `bootstrap/tests/test_upgrade.py` | “restage” on changed evidence; no affected automatic write or lock advancement; earlier unaffected writes reported, evidence retained. |
| Stage, manual reconciliation, `--apply --ack-review-only`, then next upgrade | `bootstrap/tests/test_upgrade.py` | Identify preserved evidence and new upstream ancestor; unaffected files advance and next upgrade succeeds. |
| Upgrade plan/stage/apply with rejected and accepted source, destination and cache names; existing refused-name recovery | `bootstrap/tests/test_upgrade_lockfile_path_containment.py` | Escaped rejected value and supported recovery without editing provenance; visible names pass admission. |
| Install with unknown profile module | `bootstrap/tests/test_install_module.py` | “unknown module” and escaped name; lookup remains unchanged. |
| Install with an unpaired template marker | `bootstrap/tests/test_scaffold.py` | “unpaired slot marker” and escaped slot. |
| Install with normal and absent-module slots | `bootstrap/tests/test_install_report_slots.py` | Each report displays the escaped slot, including literal-backslash distinction. |
| Install with module merge and fidelity warning | `bootstrap/tests/test_module_merge.py` | Merge and “fidelity check” output each display the escaped slot. |

