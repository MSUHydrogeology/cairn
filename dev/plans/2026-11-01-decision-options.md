# Plan: Show decision options' operating costs

**Source proposal**: dev/proposals/archive/2026-11-01-codex-decision-options.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-01
**In brief**: Make the additions and operating costs of Maintainer decision options visible before a choice.

## Source proposal

The Maintainer accepted the heavy proposal as revised under Option 1: add cross-cutting decision guidance to the governing instruction and its shipped counterpart, with collaboration alignment and high assurance.

## Scope

Update `AGENTS.md`, `templates/core/AGENTS.md` and relevant guidance in `dev/agent_collaboration.md`. Inspect shipped authoring templates and `docs/methodology/roles.md` and align them only where needed to carry the accepted guidance accurately. Preserve existing authority, safeguards, accepted scope and model floors; add no form, checklist or fixed option count. Do not alter trust baselines; release ceremonies remain separate.

**Reuse.** N/A: no code added.

### Documentation / doctrine surface

Cross-cutting prescription belongs in both governing files; collaboration guidance is deliberative, and any needed roles clarification is descriptive.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inspect current counterparts, readers and byte pins; align the guidance and exercise the two decision examples. | Both required plan reviews and author response | Concise governing and supporting prose, with iteration evidence. |
| C2 | Independent code and Security Reviews, response and final integration verification. | C1 committed | Review records and wide Boundary B evidence. |

## Acceptance criteria

**C1.** Material options state additions or changes and meaningful build, operation, understanding and maintenance costs, with estimates or uncertainty where needed. The least involved credible option, including doing nothing when viable, states its losses and safeguards; the recommendation and reason are separate. Comparisons cannot waive required checks, accepted scope or model floors. Existing Decisions briefly name material new recurring additions; one without such an addition needs no extra sentence or inventory. Governing copies agree in substance, and supporting guidance does not contradict them. A human comparison exercises a recurring check and a credible simpler option, and a routine Decision without a recurring addition; record the sample and reviewer. Omitting the recurring check must fail that comparison. No fixed form or invented alternative is required.

**C2.** Ordinary and separate Security Reviews assess the committed implementation. All required checks and accepted criteria are met; final wide Boundary B evidence covers review fixes.

## Scope delta

**Scope delta**: preserved.

## Verification

Before editing, inspect direct readers and byte pins and map changed paths with `python tools/test_tiers.py for <paths>`; for governing text use the complete reviewed range. Run mapped iteration tests and applicable claim, link, snippet and neutrality gates, plus `python scripts/check_cairn.py`. Compare shipped and self-hosted guidance and perform the two human examples above; record reviewer, outcomes and omissions. Security preflight S2 and S3 remain the proposal's human comparison in C1, not an automated claim.

Boundary C: independent reviewers read the committed implementation and iteration evidence, run only targeted falsification checks, and name missing coverage. After review and fixes, run wide Boundary B on a clean, unchanged final commit under canonical Python 3.13: mapped iteration and integration/workflow tests, owning families, known consumers and public paths, standing gates and plan-specific examples. Record SHA and range, interpreter, clean pre/post state, commands, counts, elapsed time, tokens, non-pass dispositions and omissions. Tree certification and trust-baseline changes are separate release work; do not run the full certifying suite here.
