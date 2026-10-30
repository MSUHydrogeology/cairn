# Plan: Protect upgrade bases and install output

**Source proposal**: dev/proposals/archive/2026-10-29-codex-upgrade-install-integrity.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Check upgrade ancestors before merging and make supplied names recognizable in paths and output.

## Source proposal

The Maintainer accepted the revised proposal: check saved merge ancestors and bind staged results to the evidence checked, refuse specified invisible path characters, and escape supplied names in output. Preserve work and provide recovery; the digest is consistency evidence, not authentication.

## Scope

Change `bootstrap/_scaffold/upgrade.py`, `install.py`, and `cli.py`, shared helpers where appropriate, their tests, `bootstrap/UPGRADE.md` and relevant descriptive install/lockfile guidance. No doctrine surface. The existing Maintainer-run AST re-anchor remains required; this plan does not authorize baseline installation or old-anchor reconciliation.

**Reuse.** Searching `bootstrap/_scaffold` for `base_hash`, `_contained_lockfile_path`, `print_report`, and `fidelity_warnings` found existing digest production, shared path admission, report rendering and merge output. Extend the review-only and stage/apply mechanisms, and existing display escaping, rather than duplicate them. Search test consumers with `rg` for those symbols and command flags before implementation; update the mapping below if further consumers are found.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Verify ancestors, bind stage to checked evidence, and implement recovery | Both plan reviews | Upgrade behavior, recovery and public-command tests |
| C2 | Enforce character policy and escape supplied names at all output routes | C1 and both plan reviews | Admission, display, tests and descriptive guidance |
| C3 | Record stable verification and hand off for independent code and Security reviews | C1–C2 complete | Boundary B evidence and review handoff; AST ceremony remains Maintainer-run |

## Acceptance criteria

### C1

Hash raw saved bytes against a well-formed `sha256` base digest before decoding; merge that same read. Missing, malformed, mismatched, unreadable or invalid UTF-8 evidence, including legacy records without a valid base digest, produces review-only, preserving the adopter file and original bad cache. A staged automatic result binds the checked bytes and expected digest; changing either before apply invalidates that result, including race/error paths. Public plan, stage and apply tests cover matching control and a crafted loss case. Recovery tests reconcile the affected file, acknowledge review-only, advance unaffected files, preserve the bad cache as evidence, and complete a subsequent upgrade with a valid new ancestor derived from the applicable upstream template, never silently from the adopter file. Document exact operator steps and digest limitations.

### C2

At shared admission reject Unicode categories Cc and Cf, U+034F and variation selectors in source, destination and cache paths; escape rejected values in diagnostics. Permit decomposed accents and visible non-Latin names; test zero-width, bidi, terminal controls, contextual joiners and selectors. Explain the compatibility cost and a supported recovery for existing refused names without hand-editing tool-owned provenance. Escape supplied module and slot names for display, preserving ASCII readability and distinguishing literal backslashes from escapes; lookup uses unchanged names. Public commands cover unknown modules, unpaired-marker warnings, normal and absent-module slot reports, and merge and fidelity output. No claim of complete protection against visual deception.

### C3

Run the mapped checks and scratch install/upgrade, including the recovery sequence; record results and omissions against the exact clean implementation commit. In separate scratch copies, remove the digest check and display escaping respectively: relevant behavior tests must fail, with controls passing. Record each mutation and outcome. Security preflight S2 is exercised here; S3 is the public commands and gates below. Unmet checks keep the work open. The existing AST ceremony is not performed by this plan's implementation agent.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A uses the canonical Python 3.13 interpreter and scoped tests. For ancestor and recovery behavior run `python -m pytest bootstrap/tests/test_upgrade.py bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_upgrade_side_door_parity.py`; for module addition and provenance consumers run `python -m pytest bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_lockfile_provenance.py`; for display and install paths run `python -m pytest bootstrap/tests/test_install_report_slots.py bootstrap/tests/test_install_module.py bootstrap/tests/test_module_merge.py bootstrap/tests/test_scaffold.py`. Add public-command tests in the owning files and include their files in these commands. Split selections within the broad-run guard's file limit and reconcile the union; do not override the guard. Search actual readers and extend this mapping before execution if affected consumers are missing.

Exercise `python bootstrap/scaffold.py upgrade --target <repo>` with `--plan`, `--stage`, `--apply` and `--apply --ack-review-only` in a scratch project, and `bootstrap/scaffold.py` install with normal, absent and unknown module cases. Check command help and actual entry points before using them. The new behavior tests must cover all C1/C2 cases, not just the smoke. Run `python scripts/claim_check.py` on changed documentation, `python scripts/check_cairn.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py` where synced snippets change, and `python scripts/quality_gate.py --sub neutrality` for prose. Run `python -m pytest bootstrap/tests/test_security_lint.py` for the engine Bandit gate, treating a skip as an unmet check; do not run the full suite here.

Boundary B is **wide** for the engine contract and security boundary: repeat the mapped owning families, public paths, mutation and standing gates on a clean, unchanged final implementation commit under the canonical interpreter. Record tested SHA and reviewed range, interpreter, clean pre/post state, commands, outcomes, timing, non-pass dispositions, omissions, and **Certified by**: pending. Certification is separate. Boundary C is independent targeted falsification by the code reviewer, including the set of output routes and staged-evidence changes; the reviewer records bounding and any missing check. An AST re-anchor follows its existing Maintainer-run ceremony, separately authorized.
