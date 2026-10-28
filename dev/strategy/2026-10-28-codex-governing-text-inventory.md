# Governing text inventory and routing alternatives

**Author**: Codex (Implementation inventory); Codex (Strategy judgment)
**Model**: GPT-6 Luna (low), factual inventory; GPT-6.1 Sol (high), Strategy
**Date**: 2026-10-28
**Status**: draft
**Type**: comparative-research
**Surfaces this would feed**: `dev/plans/2026-10-28-governing-text-single-source.md` C2

## The question / felt gap

Recommend a public methodology reference under **`docs/`**, with one usable installed operative home per obligation. A separate `doctrine/` directory has historical purpose, but no demonstrated audience or delivery need that requires that name and location. This recommendation awaits the refreshed C1 evidence and the Maintainer's C2 choice; it authorizes no move.

## Method *(grounded, falsifiable — verify-before-asserting)*

Factual baseline: `0ac350c02422d8a8ba8c3b674a671b072c71a317`, recorded at `423310d4`. The [TSV](../plans/2026-10-28-governing-text-single-source/doctrine-sections.tsv) preserves all 195 heading-shaped records from 15 files (6,107 lines), with stated purpose, excerpts, history and placement relations. A fence-aware recount finds **190 actual H1–H3 headings and five example headings inside code fences**, all in `doctrine/plans.md`; its context column distinguishes them. Classification is lexical signal, not proof of each section's meaning.

Strategy read representative committed passages in roles, plans, lifecycle-contract, doc-governance, rationale and consolidation-review; installer mappings, owner tests and the documentation-plan pair; and history at `3a190c95`, `5f619be4`, `7519c5da` and `676b7c0e`. Initial installs/tests used Python 3.13.13. No public text changed and no adoption trial ran. A uniquely necessary public contract without a suitable documented home would challenge the recommendation.

## Findings

### What the public corpus does

| Files under `doctrine/` | Observed purpose and duplication |
|---|---|
| `README.md`, `doc-governance.md` | Explain documentation layers but also prescribe routing; overlap the installed documentation plan and governing-file instructions. |
| `collaboration-stance.md`, `dual-review.md` | State conduct and detailed review duties; duties recur in AGENTS, the review loop, templates and selected modules. |
| `lifecycle.md`, `proposals.md`, `plans.md` | Explain the method and repeat operating lanes, transitions, scope and verification procedures carried by installed governing text and templates. |
| `lifecycle-contract.md` | Public state/authority specification; explicitly says its checker was retired. This is useful reference, not current machine enforcement. |
| `roles.md`, `coordination.md`, `session-routines.md`, `onboarding.md` | Mix rationale with task floors and procedures; related operating text ships in core or selected modules. Mapping every clause remains open. |
| `rationale.md` | Research anchors and limitations deserve public explanation; its doctrine-evolution gate and harvest cadence are prescriptions requiring separate reach analysis. |
| `runtime-contract.md` | Public runtime/dependency contract, related to bootstrap contracts; descriptive specification remains useful outside adopter installs. |
| `consolidation-review.md` | Manual review procedure plus Cairn's historical disposition log; the log is project evidence, not a general adopter rule. |

The folder began as published method on 2026-05-19 (`3a190c95`), before the forkable documentation-plan module (`5f619be4`, May 28) and Cairn's self-adoption (`7519c5da`, June 12). That explains its origin; it does not establish today's best placement. The model-floor implementation (`676b7c0e`) again edited AGENTS, public roles and module pairs, demonstrating multiple maintained presentations.

### Installed homes and evidence limits

| Source owner | Actual installed destination / evidence |
|---|---|
| `templates/core/AGENTS.md` | `AGENTS.md`; core mapping. Source/twin tests protect review and verification duties. Claiming deliberately differs: conditional for adopters, unconditional for Cairn. |
| Core collaboration file | `dev/agent_collaboration.md`, reached from AGENTS. `test_review_sweep_ships.py` checks real profile installs, the pointer and an installed-removal control. `test_writing_rules_ship.py` checks installed writing guidance. |
| Core proposal/plan templates and board | Same relative `dev/` paths. `test_scope_reduction_trap.py` checks 14 source surfaces; this is not installed semantic coverage. |
| Default-on documentation-plan template | `docs/DOCUMENTATION_PLAN.md`, plus module guidance under `dev/modules/`. `test_documentation_plan_module.py` checks real installs and routing vocabulary. |
| Core `dev/rules/README.md` | Same path, otherwise empty. Explicitly reserved for project-owned agent discipline; excludes general lifecycle/coordination doctrine. |
| Selected module sources | Corresponding `dev/modules/` files. Optional model-selection or dual-review cannot carry a universal duty alone. |
| `doctrine/` | Absent from both measured installs and installer mappings. AGENTS defines its references as published citations, not installed files. |

Fresh CLI installs of `solo-greenfield` and `high-rigor-legacy` wrote 69 and 101 files, respectively, both exiting 0. Both included the installed homes above, including `dev/rules/README.md` and the documentation plan; neither included doctrine. The small install retained two onboarding slots; the fuller retained `FILL ME` model mapping, manual hook setup and no executed host security tool. Installation success does not establish completed adoption.

The documentation-plan pair is **not proven equivalent**: self-hosted/template versions have 437/345 lines and different section outlines, beyond worked-example paths. Its claimed shared substance needs semantic comparison before consolidation.

### Representative editing cost

| Baseline edit | Source work, checks and reader cost |
|---|---|
| Operating rule: model tier | Two AGENTS copies, related public roles passage and optional module pair: five maintained presentations. Baseline `test_model_tier_rule_ships.py` had nine cases: source clauses/parity, deletion sensitivity and a real solo install without the module. Core delivery keeps the rule readable without optional-module lookup. |
| Template instruction: `Scope delta` | Two plan templates; related contract spans 14 source surfaces. Baseline owner file had 89 cases. The installed plan carries the instruction, but that file does not semantically check installed wording. Keeping the field where authors fill it serves a purpose distinct from repeating the whole governing rule. |

At the baseline, five mapped owner files passed **373 tests under Python 3.13.13** (98 in the two example owners). These are initial controls, not post-change proof. Changing an owner test currently entails the frozen-test ceremony; ordinary unpinned prose does not. A rule change still owes its lifecycle authorization and applicable doctrine/security treatment; this inventory waives neither. No operating or template edit has yet been simplified or measured after consolidation.

## Options

| Route | Benefit / cost |
|---|---|
| Keep distinct publication and installed operation | Preserves stable citations and a visibly separate methodological identity. Could remove duplicate prescriptions, but retaining this particular directory adds no demonstrated delivery benefit. Doing nothing retains repeated editing. |
| Put public methodology under `docs/` | Groups public explanation/reference with existing reader guides; installed operative homes remain explicit. Costs citation migration and the old landmark. A folder rename alone saves no rule edits. |
| Put common methodology in `dev/rules/` | Groups prescriptions, but conflates Cairn's public product with project-local discipline. Current installs provide only its README; distribution and ownership would need redesign. |
| Generate presentations from one source | Could enforce parity, but introduces authoring machinery and maintenance without evidence it costs less. Not the accepted default. |

## Recommendation

Proposed paths:
- `docs/methodology/` — public explanation/reference after the C2 choice.

Choose the second route: proposed **`docs/methodology/`** (a future destination, not an existing path) for public explanation and reference, and installed governing files/templates/modules for operation. Preserve the public method, rationale, authority boundaries and useful specifications; remove parallel imperative retellings only after their complete installed owner and usable local pointer are demonstrated. Keep task-specific template fields and safety minima at their reading points. Keep `dev/rules/` for project-local rules.

Public explanations should point readers to the operative template/source instead of maintaining another independently editable requirement. Preserve deliberate adopter differences. Retain project history as evidence, without presenting it as universal doctrine. No new generator is needed.

What is lost is the `doctrine/` landmark and its direct citation stability, not the method or obligations; link migration must be counted. Expected savings come from fewer independently maintained requirements, not fewer headings. C3 must demonstrate that saving with the same two edits; it may not claim improvement from relocation alone.

## Open questions

Before any deletion, map remaining doctrine-only prescriptions—especially rationale's gate/harvest, coordination tiers, authority details and session/onboarding duties—to core, module, framework-only or explanation. A public citation cannot discharge an installed duty. For every changed obligation, pair intact installed output with removed/inverted-clause controls; neither lexical matches nor negative controls prove semantic equivalence.

Refresh section facts, owner tests, installs and edit-cost comparisons after model-floor and scoped-verification implementation and code review. C1 remains initial; C2 stays gated until that refresh and the Maintainer's exact choice.
