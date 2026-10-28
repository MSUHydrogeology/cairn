# Plan: Governing text inventory and routing

**Source proposal**: dev/proposals/archive/2026-10-28-codex-governing-text-single-source.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Map where rules come from and reach adopters before choosing how to reduce repeated editing.

## Source proposal

The accepted proposal makes inventory and Maintainer routing precede consolidation. The Decision also asks why a
`doctrine/` folder exists when it is not shipped to adopters, and whether its
contents belong in `dev/rules` or `docs/` instead.

## Scope

Inventory the published doctrine and the internal and installed governing
files, including `AGENTS.md`, `dev/agent_collaboration.md`, and proposal and
plan templates. Include affected modules, boards, the documentation plan and
its forkable template. The routing choice may lead to changes in these surfaces;
Preserve adopted obligations and deliberate adopter differences.

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
| C2 | MAINTAINER-GATED routing choice | C1 refreshed after model-floor and scoped-verification implementation and code review; Maintainer chooses before rule relocation or deletion | Chosen routing and explicit authorization in this plan |
| C3 | Conditional edits and property guards | C2; scoped-verification implementation and code review complete before shared governing edits; test-trust-boundary work complete before frozen prose tests change | Safe consolidation, installed guards and comparison evidence |
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
and unresolved questions. Refresh affected evidence and mapping against the
post-model-floor and post-scoped-verification reviewed HEAD before C2; commit
the inventory before the fence.

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

Boundary A starts with this map; paths after arrows are installed destinations
from `bootstrap/_scaffold/config.py` `_CORE_MAPPINGS`:

- Review and verification duties: `templates/core/AGENTS.md` → `AGENTS.md`;
  `test_review_and_verification_rules_ship.py::test_agents_md_carries_the_obligation`
  checks both source copies only. Its claiming tests distinguish conditional
  adopter claiming from unconditional Cairn claiming; do not flatten that difference.
- Review sweep: `templates/core/dev/agent_collaboration.md` →
  `dev/agent_collaboration.md`, with the `AGENTS.md` pointer. In
  `bootstrap/tests/test_review_sweep_ships.py`, source tests check both copies;
  `test_installed_loop_document_carries_the_obligation` and
  `test_installed_agents_md_carries_the_pointer` check actual installs of every
  shipped profile; `test_an_install_without_the_sweep_is_reported` removes the
  sweep from installed output as a control.
- Scope reduction: core governing files and proposal/plan templates map to the
  same relative installed paths; `test_scope_reduction_trap.py::test_scope_reduction_obligation_present`
  checks source, board and doctrine surfaces, not installed output. Compare
  source/twin meaning, and verify affected installed clauses through real installs.
- Model floors: core `AGENTS.md` → installed `AGENTS.md`;
  `test_model_tier_rule_ships.py::test_the_rule_reads_the_same_in_both_copies`
  checks parity; `test_a_profile_with_no_module_still_installs_the_rule` checks
  `bootstrap/profiles/solo-greenfield.yml` output.
- Plain language: core collaboration file → installed collaboration file;
  `test_writing_rules_ship.py::test_cairns_own_copy_says_what_it_ships` checks
  source parity, and `test_standard_with_version_and_groups_reaches_install`
  checks a real core-plus-issue-capture install.

Test paths above are under `bootstrap/tests/`. The inventory and chosen routing
extend this map to each changed obligation, source owner, installed destination,
profile and exact test or gate before edits; search for every affected reader,
record uncovered consumers and check them. For each replaced guard, check the
intact real install and removed or inverted clause in installed output; a negative
control proves sensitivity, not semantic equivalence. Compare meaning against
the inventory and check source/twin parity including intentional differences.
Run the mapped owners and real installs, `scripts/claim_check.py`,
`scripts/link_check.py`, `scripts/check_cairn.py`, and
`scripts/quality_gate.py --sub neutrality --sub redundancy` as applicable.
Inspect the frozen manifest and follow the existing ceremonies. Check the inventory’s claims, links and evidence.

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


## Plan review -- Codex (Internal Security Reviewer, gpt-6.1-sol high) -- 2026-10-28

```
Reviewed commit: 73d9ff63803769c4764883c7117817d444f0c5f9
Target: Source proposal through Verification; accepted revised proposal and Decision 439c7b34
Prior findings: none from this security stance
Assurance path: Internal + Internal Security Review
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The plan preserves the accepted safety contract:
   inventory actual rule homes before routing, retain installed operational
   instructions, and obtain the Maintainer's choice before relocation or deletion. Its
   verification map needs sharpening before implementation -- plan C1–C4;
   `dev/proposals/archive/2026-10-28-codex-governing-text-single-source.md` > revised
   proposal and Decision.
2. **Best alternative.** Reuse existing installed-output checks and retain distinct
   semantic guards while extending their coverage only where the inventory identifies a
   changed obligation; a new checker is unnecessary -- `bootstrap/tests/test_review_sweep_ships.py::test_an_install_without_the_sweep_is_reported`; `bootstrap/tests/test_review_and_verification_rules_ship.py::test_the_shipped_copy_makes_claiming_conditional`.
3. **What would show it wrong.** A source guard stays green while a real install loses
   an instruction, a citation substitutes for its operational home, or a
   removed/inverted clause escapes its replacement guard --
   `bootstrap/_scaffold/config.py` > `_CORE_MAPPINGS`;
   `bootstrap/tests/test_scope_reduction_trap.py` > `_REVIEW_LOOP`; plan C2–C4.

**S1 (blocking) -- Distinguish source checks from installed safety evidence in the
reviewed map.** Verification gives five starting files, then postpones the actual
mapping. They do different jobs: `test_agents_md_carries_the_obligation` in
`bootstrap/tests/test_review_and_verification_rules_ship.py` reads the source copies;
`test_installed_loop_document_carries_the_obligation` and
`test_installed_agents_md_carries_the_pointer` in
`bootstrap/tests/test_review_sweep_ships.py` inspect real CLI installs. Naming both
files does not show which installed obligation and reader path a changed guard protects.
A source-only positive/deletion pair could therefore be mistaken for the promised
installed reachability check. **Satisfier:** fold the ordinary review's F2 map into the
operative Verification cells, naming the known safety obligations, source/twin
comparison and intentional differences, installed destination/profile paths, exact
owning tests and standing gates. Distinguish source-only evidence from installed-output
evidence; identify the positive and removed/inverted-clause controls for each replaced
guard, and require the inventory/routing result to extend that map before edits. Keep
semantic comparison against the inventory: a negative control proves sensitivity to its
chosen error, not that the remaining prose means the same thing.

C2's unresolved-home refusal and C3's no-safe-cut disposition prevent silent rule loss.
The operational-safety minimum remains adopter-reachable rather than being delegated to
published rationale (`doctrine/doc-governance.md` > “The operational-safety minimum
stays minimal”). C3 also preserves frozen-test sequencing; this review authorizes
neither routing nor a trust transition.

**Covered:** #1 claims and #2 delivery: `_CORE_MAPPINGS` and the named source/installed
tests; #3 completeness and #4 failure: S1, C2–C4; #5 consistency and #6 drift: accepted
revised proposal, deliberate claiming difference, `doctrine/doc-governance.md`; #7
placement: C2 and frozen-test fence; #8 scope: conditional cuts and two-edit comparison;
#9 satisfier: S1 and ordinary F2. **Not covered / low confidence:** No install, test,
mutation, ceremony, full doctrine inventory or future semantic guard was executed. Those
remain implementation evidence; the ordinary review's sequencing finding remains
separate.

## Response to plan review -- Codex (Plan author, gpt-6.1-terra) -- 2026-10-28

| Finding | Disposition | Operative cell |
|---|---|---|
| F1 | Accepted | Sequence C2–C3; C1 refresh |
| F2 | Accepted | Verification map and C1 refresh |
| S1 | Accepted | Verification map and installed-output controls |
