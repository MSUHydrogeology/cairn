# Plan: Correct release-test portability defects

**Source proposal**: dev/proposals/archive/2026-11-02-codex-release-test-corrections.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Correct three protected tests so release checks work consistently while retaining their safeguards.

## Source proposal

The accepted heavy proposal corrects child-test bytecode hygiene, the fixed install-manifest count and the initial branch in a disposable Git repository. It preserves the existing security assertions and requires independent ordinary and Security reviews and three negative controls.

## Scope

Change only `bootstrap/tests/test_security_check.py`, `bootstrap/tests/test_notice_install.py` and `bootstrap/tests/test_gate_preflight.py`: add `-B` to `_child_pytest`, update the fixed count and diagnostic to 88 for the accepted changelog mapping, and initialize `_repo` with `git init -b master`. Do not alter production, mappings, trust machinery, baselines or manifests. The forward-baseline work remains separate.

**Reuse.** Use the existing helpers and assertions. Searching `_child_pytest`, `_repo`, the count and changelog install test in `bootstrap/tests` found the existing helper callers and `TestInstallCore.test_installs_changelog_and_publishes_its_mapping`; trace the `_repo` consumers before choosing the affected tests.

### Documentation / doctrine surface

No doctrine surface; this plan records deliberation in `dev/`.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Correct the three tests and exercise their existing safeguards and negative controls. | Plan review folded to ready-to-implement. | Three protected test corrections and iteration evidence. |
| C2 | Independent ordinary and Security code reviews; resolve findings, then final wide Boundary B. | C1 committed. | Review and final verification records. |

## Acceptance criteria

C1: Child pytest suppresses bytecode while ignored-plugin exclusion, skip refusal and extra-file rejection remain effective. The count remains independently fixed at 88, with its diagnostic naming the accepted changelog addition; the existing changelog install and mapping test passes. Scratch `_repo` starts on `master` under both `main` and `master` host defaults; all nine reported tests and relevant consumers retain their assertions. In separate copies, removing `-B` with `PYTHONDONTWRITEBYTECODE` absent reproduces the detached-checkout failure, restoring 87 fails the count test, and removing the explicit branch under a `main` default fails an affected test. No production or trust baseline changes.

C2: Ordinary and Security code reviews cover the committed changes; any required fixes receive the targeted follow-up. Wide Boundary B passes on the clean final commit with the affected selection, consumers and applicable standing gates; record outcomes and omissions.

## Scope delta

**Scope delta**: preserved.

## Verification

Before implementation, run `python tools/test_tiers.py for` on all three test paths and trace the helpers' callers. Boundary A runs that selection under canonical Python 3.13.x, explicitly covering all `_child_pytest` callers, the detached ignored-plugin case, count and changelog install tests, nine reported Git tests and relevant `_repo` consumers under `main`, plus a helper check under `master`. Confirm the scratch HEAD is `master`. Run the three separate-copy negative controls in C1, and preserve skip and extra-file refusal checks. Record commands, results, elapsed time, interpreter, coverage mapping and omissions; failures remain open.

After independent reviews, run wide Boundary B on the clean unchanged final commit: the iteration list across the reviewed range, mapped integration/workflow consumers, applicable standing gates and the acceptance checks above. Record the full SHA and range, canonical interpreter, pre/post state, commands, counts, elapsed time, non-pass dispositions and omissions. Run claim, link, snippet and neutrality prose gates as applicable for records. The existing release and certification requirements remain unchanged; no full-suite implementation gate is added.
