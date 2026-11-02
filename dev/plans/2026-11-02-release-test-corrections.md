# Plan: Correct release-test portability defects

**Source proposal**: dev/proposals/archive/2026-11-02-codex-release-test-corrections.md
**Status**: ready-to-implement
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

## Plan review -- Codex GPT-6 (Reviewer) -- 2026-11-02

Reviewed commit: e91de6c78e1e45438e7365083039c5e071ee1721
Target: scope, sequence, criteria and verification against the accepted proposal
Prior findings: none
Assurance path: high-assurance

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT; the plan can deliver the Decision. **Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Foundations**

1. **Should this happen as framed?** Yes. The plan retains all three accepted edits, preserved assertions, separate negative controls and independent reviews before wide final verification. -- Accepted proposal, Decision and Tests required; plan Scope, C1–C2 and Verification.
2. **Best alternative.** Using host configuration would avoid the branch edit but retain host dependence; an environment override for bytecode would retain caller dependence. The existing helpers provide the smallest direct corrections. -- Accepted proposal, Alternatives; committed `_repo` and `_child_pytest`.
3. **What would show it wrong?** A child still producing bytecode or bypassing refusal checks, a count unrelated to the changelog mapping, or a scratch test still depending on the host branch default would defeat the plan. The specified existing tests and three separate-copy mutations challenge these outcomes. -- Plan C1 and Verification; committed helper and count assertion.

Coverage: read the committed plan, accepted proposal and review record, template, and representative committed helpers and assertions. Did not run tests or mutations, enumerate all consumers, or perform Security Review; implementation must trace consumers and record the required checks.

## Plan review -- Codex gpt-6.1-sol -- 2026-11-02

Reviewed commit: 4dee65075b5c440af1c668223a52a436dc7aaa54  
Target: three protected-test corrections and retained security controls  
Prior findings: none  
Assurance path: high-assurance

**Obligation**: Internal Security Review  
**Tier**: Internal Security Review  
**Findings**: none

**Foundations**

1. **Should this happen as framed?** Yes. The plan implements the three accepted corrections without weakening production verification, manifest independence or synthetic trust assertions. The count is justified by the accepted changelog mapping and its existing install test. -- Accepted proposal, Decision and S1–S5; plan Scope/C1; config changelog entry; scaffold changelog install test.
2. **Best alternative.** Correct the existing helpers and literal count. Caller environment settings retain bytecode dependence; host Git configuration retains branch dependence; deriving the count from output removes its independent check. The proposed edits need no new mechanism. -- Existing `_child_pytest`, top-level `_repo` and fixed manifest-row assertion; proposal Alternatives.
3. **What would show it wrong?** An ignored plugin or skip bypassing release refusal, extra files admitted, count 88 masking another mapping, or tests failing under a main default. Retained behavioral assertions, three separate-copy mutations and explicit main/master controls can falsify these outcomes; prior logs alone cannot. -- Plan C1/Verification; detached-plugin and incomplete-evidence tests; branch-dependent atomic-publication/ref assertions.

**Verdict**: Accept as framed; no blocking findings. Independent reviews before final wide Boundary B preserve assurance for these protected bytes. The plan retains release requirements without introducing a full-suite implementation gate or authorizing baseline changes.

**Elapsed**: approximately 2 minutes. **Tokens**: unknown.

Coverage: read committed plan and ordinary review, accepted proposal, current template and governing rules, helpers, manifest count/mapping, install test and representative security assertions. Did not enumerate every helper consumer, reproduce logs, run mutations or suites, or compare an anchor; those implementation checks remain owed.

## Response to plan reviews -- Codex GPT-6 -- 2026-11-02

Both the Internal and Internal Security Review accept the plan without findings. No operative changes are needed; the required consumer tracing, negative controls and final verification remain open for implementation.

**Elapsed**: approximately 1 minute. **Tokens**: unknown.
