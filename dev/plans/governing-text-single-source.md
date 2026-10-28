# Plan: Governing text inventory and routing

**Source proposal**: dev/proposals/archive/2026-10-28-codex-governing-text-single-source.md
**Status**: revising-plan
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Map where rules come from and reach adopters before choosing how to reduce repeated editing.

## Source proposal

The accepted revised proposal makes a rule inventory and a Maintainer routing
choice precede conditional consolidation. The Decision also asks why a
`doctrine/` folder exists when it is not shipped to adopters, and whether its
contents belong in `dev/rules` or `docs/` instead.

## Scope

Inventory the published doctrine and the internal and installed governing
files, including `AGENTS.md`, `dev/agent_collaboration.md`, and proposal and
plan templates. Include affected modules, boards, the documentation plan and
its forkable template. The routing choice may lead to changes in these surfaces;
no new directory or general-purpose tool is assumed. Preserve all adopted
obligations and distinguish source parity from deliberate adopter differences.

**Reuse.** N/A: no code added. Use the existing installer, profile definitions,
rule tests, claim and link checkers, and applicable ceremonies.

### Documentation / doctrine surface

Examine `doctrine/`, `docs/DOCUMENTATION_PLAN.md`,
`templates/modules/default-on/documentation_plan_template.md`, internal and
installed governing text, and affected modules and boards. Compare their actual
purposes and history, including the Maintainer's `dev/rules` alternative;
do not assume the present placement is justified.

Proposed paths:
- `dev/strategy/2026-10-28-governing-text-inventory.md`

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inventory current rules, history, installed reach and editing cost | Plan review; may run alongside other plans | Evidence and routing alternatives in `dev/strategy/2026-10-28-governing-text-inventory.md` |
| C2 | MAINTAINER-GATED routing choice | C1; Maintainer chooses homes before operative rule relocation or deletion | Chosen routing and explicit authorization in this plan |
| C3 | Conditional edits and property guards | C2; model-floor alignment completed before shared governing-file edits; test-trust-boundary work completed before changing frozen prose tests | Safe consolidation, installed guards and comparison evidence |
| C4 | Verify and hand off | C3; applicable frozen-file and doctrine ceremonies | Scoped verification record and independent code review |

## Acceptance criteria

### C1

For every doctrine section record stated and observed purpose, relevant history,
prescription versus explanation, and relationship to `docs/` and `dev/rules`.
Compare retaining, moving and other evidence-supported routing without assuming
one wins. Inventory installed and internal rule homes, explanations, pointers,
duplicates, affected modules and boards, and owning or wording-pinned tests.
Inspect the installer's mapping and real small and fuller profile installs;
separate source claims from observed output and trace mandatory reachability.
Measure one operating-rule and one template-instruction edit: files, tests,
ceremonies and installed reader usability. Recommend a routing with its losses
and unresolved questions. Commit the inventory before the fence.

### C2

Present the inventory and alternatives to the Maintainer. Record the choice and
its exact authorization before any operative rule is relocated or deleted.
Unresolved installed homes or mandatory pointers block those edits; published
citations alone cannot carry an installed obligation.

### C3

Change only evidence-supported redundancy or misplacement within the chosen
routing; retain installed obligations, usable triggers and distinct semantics.
Compare the two C1 edits after the change using the same measures; at least one
must become simpler without loss of reach or meaning. An 80–120-line template
length is advisory. If no safe cut or no improvement exists, seek Maintainer
disposition rather than claim success. Replace wording pins only with guards
that check the same installed obligation, pass intact output, and fail on a
removed or inverted clause. Preserve deliberately different adopter wording.

### C4

Run the mapped checks, actual installs and ceremonies, and record their results.
Review tests and output against the inventory for meaning as well as presence;
failed deletion controls or lost reach block completion. Record the before/after
comparison and any accepted scope loss under Scope delta.

## Scope delta

**Scope delta**: preserved. Any proposed loss is grouped here with its reason,
individual disposition and the Maintainer's quoted allowance before archive.

## Verification

Boundary A maps each changed rule and installed path to its owner before edits;
start with `bootstrap/tests/test_review_and_verification_rules_ship.py`,
`bootstrap/tests/test_scope_reduction_trap.py`,
`bootstrap/tests/test_writing_rules_ship.py`,
`bootstrap/tests/test_model_tier_rule_ships.py`, and
`bootstrap/tests/test_review_sweep_ships.py`. Search for further readers of
each changed surface and run those owners, positive and deletion/inversion
controls, and representative real installs. Run claim, link, prose-integrity,
neutrality and redundancy checks as applicable. Inspect the frozen manifest for
changed files and follow the existing doctrine and frozen-file ceremonies;
never modify frozen prose tests before the test-trust-boundary work completes.
The inventory itself needs claim and link checks and evidence inspection.

Boundary B uses the canonical `/Users/kendal30/conda_envs/lhm/bin/python3.13`
on a clean final implementation commit. These high-risk surfaces require full
mode, with the next certifying run supplying full-suite evidence; record
`Certified by: pending` until then. Run the scoped mapping and standing gates,
record tested SHA and range, clean pre/post state, commands, counts, timing,
non-pass dispositions and omissions. The reviewer independently falsifies the
record and changed rule reach, without running the full suite.

## Plan review -- Codex (Internal reviewer, gpt-6.1-terra) -- 2026-10-28

```
Reviewed commit: 73d9ff63803769c4764883c7117817d444f0c5f9
Target: Source proposal through Verification
Prior findings: none
Assurance path: Internal + Internal Security Review
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** Yes, subject to sequencing and a usable verification map: inventory and the Maintainer's routing choice precede any operative move or deletion -- `dev/plans/governing-text-single-source.md` > C1–C3.
2. **Best alternative.** Keep the present homes where evidence does not support a safe simplification; the existing installer delivers core and module files separately, so a published citation alone is insufficient -- `bootstrap/_scaffold/config.py` > `_CORE_MAPPINGS` and `_MODULE_MAPPINGS`.
3. **What would show it wrong.** A real install loses an obligation or its usable trigger, a deletion control passes, or neither representative edit becomes simpler without lost meaning -- `dev/proposals/archive/2026-10-28-codex-governing-text-single-source.md` > "Conditional edits and evidence".

**F1 (blocking) -- Sequence the other shared-rule work.** C3 waits for model-floor alignment but not the accepted scoped-change-verification plan, whose C1 also changes `AGENTS.md`, its shipped twin, doctrine and plan templates (`dev/plans/scoped-change-verification.md` > Scope and C1). Concurrent changes can make the inventory and its chosen edits stale or overwrite another accepted outcome. **Satisfier:** gate shared governing edits on that plan's implementation and code review too; allow C1 alongside it, but refresh the affected inventory and mapping against the completed changes before routing or edits.

**F2 (blocking) -- Map the checks and source-to-install comparison before editing.** Verification lists five starting test files and defers owner mapping until before edits, but does not map changed invariants and public paths to checks for review as the plan template requires. For example, `bootstrap/tests/test_review_and_verification_rules_ship.py` reads both `AGENTS.md` copies, including a deliberately different claiming rule; naming the file alone does not identify what protects each obligation or installed path. The accepted contract also calls for source/twin parity, not just distinct wording. **Satisfier:** map the known invariants and installed paths to test nodes or files and standing gates now, including parity and intentional differences; explain how the inventory and routing choice extend that map before edits, with any uncovered consumer recorded and checked. Keep the existing single plan-review round.

**Coverage:** Claims and production path: `_CORE_MAPPINGS`, `_MODULE_MAPPINGS`, and the cited shipped-rule tests; design and failure: C1–C4, real installs and deletion/inversion controls; consistency and drift: the accepted proposal, model-floor and scoped-verification plans; placement: C2's Maintainer fence; scope and satisfiers: conditional cuts, comparison and F1–F2. **Not covered / low confidence:** No install, test, ceremony, full doctrine-section audit, or future semantic guard was executed; the separate Internal Security Review remains open.
