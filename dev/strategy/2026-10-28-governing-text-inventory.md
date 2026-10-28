# Governing text inventory and routing alternatives

**Author**: Codex (Implementation)
**Model**: GPT-6 Luna (low)
**Date**: 2026-10-28
**Status**: draft
**Type**: comparative-research
**Surfaces this would feed**: `dev/plans/governing-text-single-source.md` C2

## The question / felt gap

`doctrine/` is published with Cairn but absent from adopter installs. This inventory checks its sections and operating-text reach before routing; Strategy recommends before the Maintainer's C2 fence.

## Method *(grounded, falsifiable — verify-before-asserting)*

Measured source is commit `0ac350c02422d8a8ba8c3b674a671b072c71a317`. The [per-heading TSV](../plans/governing-text-single-source/doctrine-sections.tsv) records 195 H1–H3 headings across 15 Markdown files, opening text, text-signal classification, line and Git history evidence, and each section's documentation-layer and `dev/rules` relation. The classification is a scan, not a final semantic judgment; delivery paths and tests follow.

Inspected doctrine/history, the documentation plan/template, `dev/rules`, core templates, modules, board, installer maps and owner tests. Python 3.13.13 ran fresh CLI installs for `solo-greenfield` and `high-rigor-legacy` and five mapped test files. This is scoped evidence, not full-suite or adoption-completion evidence.

## Findings

**Observed:** doctrine both publishes methodology and contains operative procedures, obligations and contracts. Many obligations also have separate installed text. The corpus is not explanation-only.

The table separates each file's stated question from observed role. Counts include the title heading; all headings are in the TSV.

| Doctrine file | H1–H3 rows | Observed role |
|---|---:|---|
| `README.md` | 9 | Describes the four documentation layers and prescribes the routing rule. |
| `collaboration-stance.md` | 1 | States a short conduct stance. |
| `consolidation-review.md` | 4 | Gives operative review checklists and a dogfood disposition record. |
| `coordination.md` | 14 | Mixes the coordination rationale with detailed tier rules and procedures. |
| `doc-governance.md` | 14 | Prescribes governance-file routing; also describes several adopter choices for `docs/`. |
| `dual-review.md` | 21 | Defines review duties, authority boundaries, evidence and falsification procedures. |
| `lifecycle-contract.md` | 7 | States legal transitions and authority; separates machine-checkable and human-owned parts. |
| `lifecycle.md` | 24 | Explains the lifecycle and prescribes lanes, transitions and archive conditions. |
| `onboarding.md` | 6 | Gives install-time and day-one procedure. |
| `plans.md` | 33 | Detailed plan, review and verification obligations. |
| `proposals.md` | 13 | Detailed proposal, response, Decision and scope obligations. |
| `rationale.md` | 11 | Explains the method's anchors and gaps; includes its doctrine-evolution gate. |
| `roles.md` | 8 | Assigns roles and model floors. |
| `runtime-contract.md` | 15 | Specifies Python, dependency and capability contracts. |
| `session-routines.md` | 15 | Gives start, handoff, goodnight and module-conditioned procedures. |

`doctrine/README.md` calls this the “explain the doctrine” home; `docs/DOCUMENTATION_PLAN.md` calls it published methodology and names `templates/core/AGENTS.md` as the operational surface. Yet `plans.md` boundaries, the authority contract, session routines and coordination tiers also instruct. Heading blame shows varied histories; no single move or consolidation covers the corpus.

### Homes, installed reach and evidence

| Content / source home | Installed or reader path | Evidence and limit |
|---|---|---|
| `doctrine/` (15 files; 6,107 lines) | No `doctrine/` directory in either actual install. `AGENTS.md` defines doctrine references as citations to Cairn's published method. | `_CORE_MAPPINGS` and `_MODULE_MAPPINGS` have no doctrine destination. `test_review_and_verification_rules_ship.py` says rules present only in doctrine do not bind adopters. A citation can help a reader find Cairn's published source; it is not an installed operating instruction. |
| `AGENTS.md` / `templates/core/AGENTS.md` | `AGENTS.md` | `_CORE_MAPPINGS`; `test_model_tier_rule_ships.py` checks both source copies, parity and a real solo install. Claiming is an intentional difference: the installed copy is conditional; Cairn's own copy is unconditional (`test_review_and_verification_rules_ship.py`). |
| `dev/agent_collaboration.md` / core twin | `dev/agent_collaboration.md`, plus the root pointer in `AGENTS.md` | `_CORE_MAPPINGS`; `test_review_sweep_ships.py` checks source text, installed loop and pointer for shipped profiles, and a removal control. `test_writing_rules_ship.py` checks the installed Plain Language section and pointer. |
| Proposal and plan templates; `dev/PLANNING.md` board | Same relative `dev/` paths in adopter tree | `_CORE_MAPPINGS`; `test_scope_reduction_trap.py` maps scope-reduction obligations over 14 source surfaces, including own/shipped templates, board, AGENTS, loop and doctrine. It checks source wording; it does not test that obligation in an installed plan template. |
| `docs/DOCUMENTATION_PLAN.md` and `templates/modules/default-on/documentation_plan_template.md` | Forkable template installs as `docs/DOCUMENTATION_PLAN.md`; module guide installs under `dev/modules/` | `_MODULE_MAPPINGS` makes the module default-on. `test_documentation_plan_module.py` tests destination, actual installs, four-layer routing and adopter-relative paths. The claim that only worked-example paths differ is not confirmed: the self-hosted file is 437 lines, the template 345, and their H1–H3 outlines differ (for example, self-hosted “Scope of this map” / “Assets” versus template “Where new content goes” / “Voice rules per location”). Shared core and path differences are tested; full semantic equivalence is not. |
| `dev/rules/README.md` / core twin | `dev/rules/README.md`; the folder starts empty | `_CORE_MAPPINGS` and both actual installs. The README explicitly reserves files there for adopter-owned agent discipline and excludes Cairn-general lifecycle/coordination doctrine. It is not a template home for shared Cairn rules. |
| `dev/modules/` and modules under `templates/modules/` | Selected module docs only | Model-selection is team-gated; dual-review is team-gated. `test_model_tier_rule_ships.py` and `test_scope_reduction_trap.py` cover related rules in source. An optional module cannot by itself carry a core obligation for every profile. |

### Actual installs and representative edit cost

The small `solo-greenfield` install exited 0 and wrote 69 files; `high-rigor-legacy` exited 0 and wrote 101. Both included core governing files, plan template, `dev/rules/README.md` and `docs/DOCUMENTATION_PLAN.md`; neither included doctrine. These were fresh CLI installs. The small install reports two unfilled slots; the fuller leaves model selection as `FILL ME`, recommends manual hook setup, and says no security host tool ran.

| Example edit measured from committed readers and owner map | Source reach, tests and ceremony evidence |
|---|---|
| One operating rule: the `AGENTS.md` “Model tier” rule | The core rule is in two AGENTS copies; its related floor is also in `doctrine/roles.md` and the optional model-selection module pair. One owner file, `test_model_tier_rule_ships.py`, has 9 test cases for both copies, parity, placement, a deleted-clause mutant and a real solo install without model-selection. A wording-only change is readable on install; its reach is core and not gated on that optional module. |
| One template instruction: the plan-template `Scope delta` rule | The line is in two plan-template copies; the contract spans 14 source surfaces (`test_scope_reduction_trap.py`'s `_SURFACES`), including the board, AGENTS and loop copies, proposal templates and doctrine. Its owner file has 89 test cases. A real install carries the plan template, but this owner file does not semantically inspect the installed wording. The test file is in the frozen test tree: changing it requires the existing gate-manifest ceremony; a prose edit alone does not. |

Five owner files passed 373 tests under Python 3.13.13: `test_model_tier_rule_ships.py`, `test_scope_reduction_trap.py`, `test_documentation_plan_module.py`, `test_review_sweep_ships.py` and `test_review_and_verification_rules_ship.py`. The first pair accounts for 98 passes. These are current controls, not before/after edit results; no governing text changed. Claim, link and applicable prose gates remain to run on this note.

## Options

- **Retain the split.** Keep published doctrine as rationale/methodology and retain operational text in installed core, domain and module homes. This preserves current reach but retains repeated editing and leaves the published corpus mixed in force.
- **Move suitable explanation into `docs/`.** This may make reader-facing explanation easier to find. The documentation plan and forkable template already have different section outlines; it is unresolved which explanation could move without expanding installed content or creating another source pair.
- **Use `dev/rules/` as a destination.** Its stated purpose is adopter-owned detail, not Cairn's shared rules. The two installs provide only its README. This option would need a new distribution mechanism to reach every adopter.
- **Move operational detail into `doctrine/`.** This would shorten some installed files only if it did not remove required instructions. Actual installs do not carry doctrine, and the tests explicitly reject citation as a substitute for operational reach.

These are evidence-supported routes, not a ranking. C2 remains for Strategy's recommendation and the Maintainer's choice; no rule move is authorized by this inventory.

## Recommendation

Deferred to the Strategy role before C2. This implementation inventory does not choose a routing.

## Open questions

Which sections explain, operate, or deliberately do both? Is the documentation-plan outline difference intentional or drift? Which installed home and test cover each proposed change? Refresh after model-floor and scoped-verification reviews before C2; this evidence is tied to `0ac350c0`.

## Fold-up note *(when methodology-bound)*

None identified by this project-specific inventory.
