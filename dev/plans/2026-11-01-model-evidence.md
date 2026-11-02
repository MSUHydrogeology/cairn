# Plan: Locate scientific model evidence

**Source proposal**: dev/proposals/archive/2026-11-01-codex-model-evidence.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Clarify where scientific model evidence is required without changing the configured certification suite.

## Source proposal

The Maintainer accepted the heavy proposal as revised under Option 1: associate scientific evidence with the work or release requiring it while retaining every configured suite member and other required check.

## Scope

Clarify `AGENTS.md` and `templates/core/AGENTS.md`; align `dev/plans/_template.md`, `templates/core/dev/plans/_template.md`, and `docs/methodology/plans.md` where needed. Inspect proposal templates for conflicts and reconcile any found. Preserve certification commands and triggers, independent scientific checks and their required controls, and all accepted, safety, security and release requirements. Add no form, gate, label or review round.

**Reuse.** N/A: no code added.

### Documentation / doctrine surface

Cross-cutting prescription belongs in both governing files; plan templates carry the operative workflow and methodology describes it.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inspect guidance, readers and pins; align wording and exercise both examples. | Both required plan reviews and author response | Prose and scoped iteration evidence. |
| C2 | Independent code and Security Reviews, response and final integration. | C1 committed | Review records and wide Boundary B evidence. |

## Acceptance criteria

**C1.** Scientific evidence is specified and recorded with the work or release requiring it; it does not enter routine certification merely because it is scientific. A configured suite member remains required at every required point, as do other applicable criteria, safety, security and release checks; subject and duration waive nothing. Removing or rescheduling a requirement requires separate authority. Independent scientific checks and their failing and required positive controls remain. Certification definition, commands and triggers remain intact. Compare installed and self-hosted wording using (1) a model run outside the configured suite and all other requirements, and (2) a configured suite member also serving a safety or work-specific requirement. Record the person and outcomes; a waiver must fail the second example.

**C2.** Ordinary and separate Security Reviews assess the committed implementation; all accepted criteria and required checks pass, including final wide Boundary B.

## Scope delta

**Scope delta**: preserved.

## Verification

Before edits, search direct readers and byte pins, inspect their assertions and map changed paths using `python tools/test_tiers.py for <paths>`; use the complete reviewed range for governing text. Run mapped iteration checks, applicable claim, link, snippet and neutrality gates, and `python scripts/check_cairn.py`. Compare installed and self-hosted guidance with the two examples and record the person and outcomes. Security preflight S2/S3 uses the required-run human example; no automated proof is claimed.

Boundary C: independent reviewers read the committed implementation and iteration evidence and run targeted falsification checks. After review and fixes, run wide Boundary B on a clean unchanged final commit under canonical Python 3.13, covering mapped iteration and integration/workflow tests, owning families, known consumers and public paths, prose gates and both examples. When the other accepted v0.6 plans reach the same point, combine overlapping checks on one common reviewed final commit; retain every plan's required coverage and record its own evidence, range, SHA, interpreter, clean pre/post state, commands, counts, elapsed time, tokens, non-pass dispositions and omissions. Do not run the full certifying suite for this work.
