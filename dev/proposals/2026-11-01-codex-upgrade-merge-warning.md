# Explain what a clean upgrade merge does not establish

**Author**: Codex GPT-6.1 Sol (Strategy)
**Status**: awaiting-review
**Review**: usual
**Proposed tier**: light
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-11-01
**In brief**: Explain why a clean upgrade merge still needs a person to check whether local and upstream rules agree.

## Decision summary

Add a short warning to the staged-file review instructions in the upgrade guide: a clean text merge can retain local and upstream rules that conflict in meaning, even without conflict markers. Ask the operator to compare the staged result with the upstream change and resolve any disagreement before applying it. This makes the risk clearer; it does not check the meaning, require a decision, or prevent an unreviewed apply.

## Context

The previous proposal records a reproduction in which `merge_file` returned a clean result containing incompatible local and upstream policy statements, and was rejected because the proposed per-file hold and decision state were too costly and underspecified. The Maintainer retained issue #35 for a smaller redesign ([previous proposal](archive/2026-10-30-codex-upgrade-semantic-adoption.md)). The current [upgrade guide](../../bootstrap/UPGRADE.md) tells operators to review staged files and resolve conflict markers, but does not explain that a merge without markers can still disagree in meaning. The report's `locally-modified (merged clean)` label identifies a difference from the saved base, not necessarily an upstream change; stock assembled files can also receive it, as the prior review records.

## Proposal

In the guide's `--stage` review instructions, explain the distinction between clean text placement and compatible rules. Tell the operator to compare the staged result with the upstream change and their local policy, and resolve any disagreement before `--apply`. Do not claim that the label detects two-sided changes or limit the advice to that label. Change no upgrade code, output, state, gate, or disposition workflow.

## Rationale

The warning appears at the existing review step and adds no new command or per-file state. It gives a concrete reason to examine an apparently clean result. Its effectiveness depends on the operator reading and acting on the guide; no improvement in adoption has been measured.

## Alternatives considered

Leave the guide as it is: this costs nothing, but leaves the difference between textual and policy agreement implicit. A per-file hold and recorded decision could force attention, but the rejected proposal established substantial binding, partial-upgrade and operator costs. A terminal warning would reach operators who do not open the guide, but would change the protected upgrade engine and require additional assurance; this proposal does not claim to reach them.

## Documentation / doctrine surface

Change descriptive software guidance in `bootstrap/UPGRADE.md`; the deliberation stays here. No governing doctrine or installed template changes are proposed.

## Evidence / verification plan

### Tests required

Search for tests that read or pin `bootstrap/UPGRADE.md` and run those selected by `python tools/test_tiers.py for bootstrap/UPGRADE.md`. Confirm the proposed words do not promise detection or enforcement. No new behavioral test is proposed for a prose-only change.

### Examples / smoke checks

Run the applicable claim, link, snippet and neutrality prose gates. Read the workflow as an operator and check that the warning is adjacent to staged-file review. Record any unavailable or failing checks.

#### Security preflight — five questions, answered in writing

N/A: no trust boundary added or widened; no high-risk surface changed.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

The warning suggests a clean merge proves policy agreement, implies the tool enforces review, or adds a step that operators cannot perform using the information available in the workflow.

## Scope delta

**Scope delta**: preserved for this proposal. Compared with the retained issue's original outcome, this offers guidance only: it does not require upstream incorporation or an explicit disposition. The Maintainer must decide whether that narrower outcome is acceptable for #35.

## Assurance path

**Assurance path**: standard — descriptive guide only; no executable, install contract, or governing surface changes.
