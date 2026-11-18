# Plan: Runnable worked examples

**Source proposal**: dev/proposals/archive/2026-11-09-codex-worked-examples.md
**Status**: implementing
**Plan review**: required(Internal)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/working-agreements.md
**In brief**: Show scientists four reproducible Cairn workflows using the existing greeting and water-budget projects.

## Build summary

Give readers an index and four short walkthroughs: a light change, a planned scientific change, a disposable install and upgrade, and a bounded handoff. Use existing projects, real entry points and local release history. Expected work is two to four agent sessions; upgrade compatibility is the main uncertainty. Target v0.8; repository layout is delivered and local Git contains v0.7.0 at `49dfa217102545d44e57190a48941cabcec422c3` as the prior-release input.

## Source proposal

The accepted standard proposal extends the two runnable examples without adding an application or tutorial framework. It requires an independently calculated scientific check and an upgrade demonstration that actually touches a managed file.

## Scope

Update `examples/minimal/`, `examples/scientific-minimal/`, a short index in `examples/`, the getting-started discovery link in `docs/`, and existing example and install/upgrade tests as needed. Preserve synthetic data and scientific assumptions. No doctrine surface, new installer behavior, network, agent account or checked-in installed tree. Records must identify whether illustrative or produced by the exercise; sample reviews are not independent assurance.

**Reuse.** Extend the existing greeting and water-budget projects and their self-tests; reuse the public installer and existing upgrade test homes. No new application, runner or framework.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Index, light greeting and planned water-budget traces | Accepted proposal | Examples and scientific checks |
| C2 | Disposable install, customization, staged upgrade and handoff | C1; local v0.7.0 revision | Walkthrough and focused public upgrade check |
| C3 | Reproduce commands and submit for independent code review | C1–C2 | Evidence and review-ready changes |

## Acceptance criteria

**C1.** The index identifies each question, prerequisites, commands, expected results and limits, distinguishing runnable projects from templates and case studies. Greeting shows a reviewed light proposal, Decision, implementation and result without a plan. Water budget shows a consistent proposal, plan, implementation, review, verification and archive; its units, storage sign and tolerance rationale remain visible. A closed input passes and a deliberately unbalanced input fails; conservation alone is not model validation. Existing self-tests check external results, including an independent hand-calculated residual row. Inverting a flux sign makes that independent expected-value assertion fail.

**C2.** A disposable scientific project uses the real installer and local v0.7.0 input, naming its full revision and compatibility needs. Identify an upgrade-managed file, its adopter-owned slot and lockfile record; show staged changes and manual review before apply, then verify the same customization survives. A focused test in the existing upgrade test homes checks the managed record, staged result and applied result through the public entry point. The handoff names completed work, an unresolved question, next action and verification actually run, distinguishing smoke from scientific and release evidence. No reader's real project is modified.

**C3.** Independently review code and prose, dispose of findings and record the evidence and benefit versus cost. All documented commands work offline in clean disposable copies, with interpreter, revision, outputs and omissions recorded; illustrative records match current templates.

## Scope delta

**Scope delta**: preserved

## Verification

Before implementation select tests with `python tests/tier_inventory.py for <changed paths>` and run those applicable, plus claim, link, snippet and neutrality gates under `/Users/kendal30/conda_envs/lhm/bin/python3.13`. Inspect readers and byte pins; no permanent wording pins. Execute every documented command through its public entry, checking output and exit status; compare the independent hand calculation in units with the residual, and use the inverted-sign fault and unbalanced input as negative controls. Verify the prior revision is compatible before asserting the upgrade worked; absent or failed evidence keeps the work open. Temporary probes leave before archive. Tree certification and release operations retain existing triggers.

## Plan review -- Terra (Reviewer, Medium) -- 2026-11-18

**Reviewed commit**: 651ec346e21d6f1bb7f1e7bc204d82fc6846dca3
**Obligation**: Internal
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: four reproducible workflows retain the independent scientific check, managed-file upgrade and bounded handoff without treating sample records as real assurance. -- C1–C3, accepted Proposal
2. **Best alternative.** Extend the two existing runnable projects and public upgrade path rather than maintain a tutorial framework or another application. -- Scope, Reuse
3. **What would show it wrong?** A sign inversion surviving the independent expected-value check, or a managed customization lost after staged review and apply, would falsify the result. -- C1–C2, Verification

The named local revision is an input; compatibility is an implementation check, not a human gate. Public checks cover scientific output and actual upgrade behavior without wording pins; parent-owned joined integration remains under the project verification rule. Coverage: compared the committed plan with the accepted proposal and review rules; did not run examples, inspect fixture compatibility or test an upgrade. No governing doctrine changes are planned.

## Implementation evidence -- Terra -- 2026-11-18

C1–C2 ship at `5e20fb14`. The v0.7.0 input `49dfa217102545d44e57190a48941cabcec422c3` is an annotated tag object, resolving to commit `2f9fda2ba410077e2523547b8ef3c055257ea61d`; the walkthrough identifies both. In a disposable copy, greeting output matched; the balanced budget wrote six zero-residual rows and exited 0, and the unbalanced row produced 10 mm and exited 2. Python 3.13 example and upgrade checks passed (11 in 19.96 s); the focused upgrade including `--plan` passed (1 in 28.73 s). The staged and applied managed slot retained its customization. A temporary inverted ET sign failed the independent expected-residual assertion (60 versus 0); the unmodified check passed. Claim, link, snippet, check_cairn and neutrality checks passed. The first upgrade probe used the current source accidentally and an exported archive lacked ancestry; the corrected real local checkout passed. No full suite, actual research validation or release verification was run. Independent code review remains.

**Benefit versus cost**: unknown -- reproducible workflows and a discriminating upgrade check; cost two temporary Git clones and 28.73 s for the focused upgrade check; remaining maintenance burden unknown. Revisit if fixture compatibility or runtime becomes onerous.

**Elapsed**: unknown. **Tokens**: unknown.
