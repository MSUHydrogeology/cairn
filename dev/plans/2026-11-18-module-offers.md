# Plan: Offer unselected modules

**Source proposal**: dev/proposals/archive/2026-11-18-terra-module-offers.md
**Status**: awaiting-code-review
**Plan review**: required(Internal)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md
**In brief**: Explain optional modules when upgrading or when a project needs them, leaving adoption to the person.

## Build summary

Give an agent practical guidance to explain available unselected modules and their known costs, ask for a choice, and use the existing adoption command only on a yes. Preserve the read-only upgrade plan and explain automatic additions separately.

## Source proposal

The accepted standard proposal calls for offers during upgrade and at a concrete later need, with truthful deferral when a usable description is unavailable. It retains the earlier Decision that new unconditional core and skills files arrive automatically on apply.

## Scope

Update `install/UPGRADE.md`, shipped collaboration and onboarding guidance, and their Cairn counterparts where applicable. Correct “since install” to include all available unselected modules. At upgrade use the public plan's list, the exact supplied Cairn source and installed inventory; explain each module's purpose and concrete known costs, mark unknowns unknown, and ask which to adopt. Explain separately that apply adds unconditional core and skills files and additions to selected modules follow their selection.

At a task-time need, consult installed inventory and onboarding plus an accessible verified Cairn source or reference. Use its actual module descriptions, including `install/BOOTSTRAP.md` and relevant module source guidance, to identify a relevant unselected module; selected-only inventory cannot describe omissions. If a suitable description is unavailable, say so and defer the offer until one is accessible; invent neither descriptions nor costs. A yes authorizes the existing `upgrade --adopt-module <name>` for that module subject to existing checks; a no leaves it unselected. Do not infer consent, enable credentials, or repeat a refused offer in the same conversation. Preserve rules-folder trigger, answer record, threshold and separate approval for project rule changes. Add no registry, daemon or refusal store. Instructions live in existing deliberation and shipped guidance; no always-loaded doctrine change.

**Reuse.** Searched `install/UPGRADE.md`, `install/BOOTSTRAP.md`, `templates/core/dev/modules/README.md`, and `templates/skills/session-start/SKILL.md`: the public plan, adoption command, selected inventory and rules-folder offer already exist. N/A: no code added.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Upgrade and task-time guidance | Accepted proposal | Guides and matching installed instructions |
| C2 | Focused scenarios and checks | C1 | Evidence for read-only plan, explicit adoption and truthful offers |

## Acceptance criteria

**C1.** Upgrade instructions cover every listed unselected module and distinguish automatic core, skills and selected-module additions. Task-time instructions identify a relevant omitted module using a verified accessible source, or defer honestly when its description cannot be accessed. Both routes explain known costs and unknowns, request a choice and retain all existing consent, collision and provenance safeguards. Existing rules-folder behavior remains distinct and unchanged.

**C2.** In disposable projects with selected and unselected modules, the public plan writes nothing; explicit adoption after a yes adds only the intended module, while a no leaves it unselected. Follow guidance for upgrade and a separate task-time need, with accessible and unavailable descriptions, known and unknown costs, no and yes. Confirm rules-folder trigger and recorded-answer behavior. No real adopter or external communication is used. Extend a public promise test only if current checks miss a plausible fault; no permanent wording test.

## Scope delta

**Scope delta**: preserved

## Verification

Before implementation run `/Users/kendal30/conda_envs/lhm/bin/python3.13 tests/tier_inventory.py for <all changed paths>` and inspect applicable tests and byte pins. For the changed public promises run the canonical interpreter with `-m pytest tests/test_upgrade.py::TestUpgradeModes::test_plan_writes_nothing tests/test_upgrade.py::TestAdoptModule::test_adopt_installs_missing_and_records`; extend an existing promise only if it cannot distinguish the C2 fault. Run the disposable scenarios in C2 using public `install/scaffold.py upgrade --plan` and `--adopt-module`, recording inputs and observed tree changes. Run claim check on changed documents and standing claim, link, snippet, neutrality and prose-integrity gates; test negative searches against known positives. Record results, limits, elapsed and tokens. Independent code review follows. The arc owner runs the joined integration once at the arc end; it is not a prerequisite to this plan's completion.

## Plan review -- Terra (Reviewer, Medium) -- 2026-11-18

**Reviewed commit**: ef1851d6707aeef4845f228673c57a408f51d968
**Obligation**: Internal
**Findings**: none
**Verdict**: ACCEPT
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: upgrade and task-time offers retain explicit choice, truthful deferral, and the existing rules-folder behavior. -- Scope, C1–C2, accepted Proposal
2. **Best alternative.** Existing source descriptions, the public plan and adoption command avoid a new trigger engine or refusal store while covering later needs. -- Scope, Reuse
3. **What would show it wrong?** A disposable plan that writes, adoption without a yes, or a task-time offer invented when descriptions are unavailable would falsify the result. -- C2, Verification

The plan names accessible verified source guidance and an honest fallback when it is unavailable. Its scenarios cover both; permanent tests are limited to public promises, not wording. Installed collaboration and onboarding guidance are appropriate homes, and the existing rules-folder duties are retained. Coverage: compared the committed plan with the accepted proposal and review rules; did not run installer or scenarios, inspect implementation, or inspect every module description.

## Response -- Terra (Implementation) -- 2026-11-18

The Internal review accepted the plan without findings. **Disposition**: ready-to-implement.

**Elapsed**: unknown. **Tokens**: unknown.

## Implementation evidence -- Terra (Implementation) -- 2026-11-18

Added upgrade and task-time offer guidance to the collaboration guides,
upgrade guide and installed onboarding tour. Under Python 3.13.13 the two
planned public upgrade tests passed (2 in 2.01 seconds). A disposable install
with `claim-check` selected showed a read-only plan listing
`architecture-review`; no left the tree unchanged, and explicit adoption
changed the roster from `claim-check` to those two modules only. Its source
described architecture review; a separate absent source was treated as a
deferred offer, with no adoption command. The dual-review source describes its
staffing cost; where no cost was found it was reported unknown. A collaborative
preset install contained both the tour and collaboration route. Reviewed the
existing rules-folder threshold and answer/approval instructions; they were
unchanged. These are synthetic walkthroughs, not observations of an adopter.

Link, snippet and neutrality gates passed; claim and Cairn checks passed for
the other three changed documents. `install/UPGRADE.md` retains five historical
path flags, reproduced on the unchanged HEAD version; no new flag appeared.
No full suite or wording tests were run. Elapsed: unknown; tokens: unknown.
