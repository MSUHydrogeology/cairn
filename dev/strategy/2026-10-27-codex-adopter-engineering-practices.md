# Helping adopters establish engineering practices through architecture review

**Author**: Codex (Strategy)
**Model**: GPT-6 (exact runtime variant unavailable)
**Date**: 2026-10-27
**Status**: draft
**Type**: product-strategy
**Surfaces this would feed**: the adopter architecture-review module and rubric; the testing-discipline module; a future proposal on their composition.

## The question / felt gap

Cairn should help scientific projects establish the engineering practices their
work needs. That does not mean Cairn itself needs every practice, or that its
methodology must teach every engineering technique. The Maintainer identified
the adopter architecture-review module as a promising home for this capability.

Three questions must stay separate: what Cairn's own tooling needs; what Cairn
helps adopters establish; and what specialist resources should teach. Testing
architecture is a live concern in Cairn itself. Numerical contracts,
reproducible simulations and checkpoint/restart are candidate adopter needs,
not demonstrated deficiencies in Cairn's tooling.

## Method

Read the current strategy template, the architecture-review module and its
rubric, testing-discipline, the documentation placement procedure, and the
judicious-testing strategy. This is a design exploration grounded in those
artifacts and the Maintainer's discussion, not an adopter study or an audit
of every module.

Evidence:

* [Architecture-review](../../templates/modules/team-gated/architecture-review.md)
  is currently a triggered remediation tool for architecture that accreted.
* Its [rubric](../../templates/modules/team-gated/architecture_review_template.md)
  already covers workflow coherence, data contracts, correctness/provenance,
  extensibility and operational maturity.
* [Testing-discipline](../../templates/modules/team-gated/testing-discipline.md)
  already provides test tiers, contract tests, negative tests and placement
  conventions. It explicitly leaves testing craft to external resources.
* The [testing strategy](2026-10-27-antigravity-judicious-testing-and-simulation-verification.md)
  explores suite consolidation and scientific verification guidance.
* The [documentation plan](../../docs/DOCUMENTATION_PLAN.md) separates governing,
  descriptive and deliberative content; this note is deliberation.

This recommendation would be weakened if adopter trials found that the existing
rubric already produces actionable practice choices without further support,
or that the proposed prompts mostly generate documents nobody uses.

## Findings

### Build on the existing architecture rubric

The gap is between asking whether architecture is sound and helping a project
choose what to establish next. Keep the five existing lenses and explore short
prompts and examples beneath them, rather than a second architecture framework.

| Existing lens | Candidate adopter support | Concrete example |
|---|---|---|
| Workflow coherence | Separate computation, input/output and orchestration where the project needs that separation | A numerical kernel accepts explicit inputs instead of reading configuration files itself |
| Data contracts | Make boundary assumptions explicit, including scientific meaning and compatibility | An input states units, array dimensions, coordinate system and missing-value convention |
| Correctness / provenance trust | Identify the evidence needed to trace and reproduce a result | Save code revision, input identifiers, configuration, environment and random seed where relevant |
| Extensibility | Identify stable interfaces and how changes reach their users | A changed configuration schema has a migration path and an explicit treatment of older files |
| Operational maturity | Choose testing, performance measurement, diagnostics and recovery practices appropriate to actual use | A long simulation records restart state; a speed comparison records both runtime and numerical error |

These are candidates to assess, not universal requirements. A small analysis
script and a shared simulation package need different answers. Security and
data-governance obligations retain their existing authority.

### Connect assessment to action through the existing lifecycle

A useful assessment identifies a concrete failure or change difficulty, what
already addresses it, the smallest improvement worth making, and evidence that
would show the improvement helped. For example, an undocumented units boundary
becomes a named contract and a conversion check, rather than a general demand
for more documentation.

Use the project's existing proposal or change process for work that follows.
The architecture rubric remains an assessment aid; it does not independently
authorize implementation or add an approval stage. Existing adequate practice
is a valid result. Specialist resources teach the underlying craft.

### Give testing a clear home

Yes, Cairn already has a testing module: testing-discipline. Architecture review
should identify whether the project's verification strategy fits its risks.
Testing-discipline should own the detailed organization and selection guidance,
with links between the two. The cross-language testing module remains a
specialization rather than a competing scheme.

Separate functional scope (unit, contract, integration, workflow) from execution
cost and scientific purpose. A tiny end-to-end run is still a workflow test;
a convergence study can exercise one solver and take much longer. The proposal
must reconcile this distinction with the current module's location-based tier
scheme before recommending new labels or directories.

## Options

1. **Do nothing:** retain the current questions and external learning pointers.
   This avoids new material but leaves practice selection to each adopter.
2. **Strengthen architecture-review and its connection to testing-discipline
   (recommended):** provide concise examples and a path from an observed gap
   to appropriately scoped work.
3. **Create a broad engineering curriculum or mandatory checklist:** offers
   more instruction but risks duplicating specialist resources and imposing
   irrelevant work on adopters.

## Recommendation

Explore option 2 in one proposal. Keep implementation guidance optional and
project-specific. Preserve one home for each practice and reuse existing
review lenses. Do not infer that every adopter need is a Cairn self-development
requirement. Cairn should demonstrate only the practices relevant to its own
software and methodology.

Test usefulness with contrasting adopter situations, such as a small research
analysis and a long-running simulation. Success means an assessment produces
an appropriate action, or an evidenced decision that existing practice is
adequate. More completed forms is not success. The main risk is turning
architecture review into a broad compliance exercise.

## Open questions

* Should support extend to deliberate greenfield design? The current module
  explicitly targets accreted architecture; broadening that selection condition
  needs a proposal, not an incidental wording edit.
* What is the smallest useful set of examples, and which specialist references
  should they point to?
* Can an existing assessment record carry the practice choices without another
  template? Prefer reuse unless a trial shows a missing function.
* How should testing-discipline express scope, cost and scientific purpose
  without competing tier schemes?

## Fold-up note

This is methodology-general adopter support. A future proposal would change
published modules and their rubric together. This note changes no module,
selection rule, roadmap commitment or standing review obligation.
