# Offer missing functionality at upgrade and when needed

**Author**: Terra (Implementation, Medium)
**Status**: accepted
**Review**: usual
**Proposed tier**: standard — guidance across upgrade and task-time workflows; no installer change
**Plan review**: required(Internal)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md
**In brief**: Explain unselected Cairn functionality at upgrade and when a project needs it, and ask before adopting an optional module.

## Decision summary

An upgrade lists unselected modules by name without explaining their value or cost; a project can also reach a need between upgrades. Guide the agent to explain relevant choices in plain language, ask the person, and use the existing explicit module-adoption command on a yes. Keep the upgrade plan read-only. New core and skills files continue to arrive automatically on apply under the existing Decision, and the agent explains that separately. The work changes guidance, with effort and per-offer time unmeasured; no new background service is proposed.

## Context

`install/_scaffold/upgrade.py` computes available modules as shipped modules minus the lockfile roster, including previously unselected modules. `install/UPGRADE.md` says the public `--plan` writes nothing and `--adopt-module` deliberately adopts one module. The same guide and engine show that `--apply` adds new unconditional core and skills files; new files belonging to already-adopted modules also follow their selected module. Collision and provenance cases can block. The 2026-11-12 direction in `dev/PLANNING.md` covers new or omitted functionality, not only newly published modules. The [2026-11-16 Decision](archive/2026-11-16-claude-staged-modules-and-triggers.md) states: “This accepts the proposal as revised (`standard` tier, Internal plan review), adopting the author's defaults (core and skills files remain automatic on upgrade; keep the 5,000-word rules-folder threshold as a judgment starting point).”

The accepted [staged-modules proposal](archive/2026-11-16-claude-staged-modules-and-triggers.md) and its implementation already offer rules-folder guidance at the stated 5,000-word trigger, using the session-start skill and `dev/modules/offers.md`. That guidance is already shipped; its yes means help planning changes, not module installation. The 2026-11-16 [grown-projects strategy](../strategy/2026-11-16-claude-guidance-for-grown-projects.md) calls for offers when a project reaches a need, and cautions against noisy triggers.

## Proposal

At upgrade, have the agent read the public plan's unselected-module list and the descriptions in the exact Cairn source supplied to that upgrade and the installed inventory; explain each available module's purpose and concrete known costs, marking unknown costs unknown, and ask which, if any, to adopt. Correct the guide's “since install” wording to include unselected modules. A yes authorizes the existing `upgrade --adopt-module <name>` for that module, subject to its existing checks; a no leaves it unselected. `--plan` remains read-only and does not enable functionality or access credentials.

Between upgrades, when a task exposes a concrete project need, the agent consults the installed inventory and onboarding material and a verified accessible Cairn source or reference for descriptions of unselected modules, checks whether an applicable module is unselected, and offers it before adoption with the same explanation and choice. The installed inventory covers selected modules, so it alone cannot describe omitted ones. If no suitable description is accessible, say so and defer that offer until a source is available; do not invent a description or cost, or adopt on that basis. The agent does not infer consent from a task. Preserve the existing rules-folder trigger and its answer record, threshold and separate approval for changes to project rules. Do not introduce a generic trigger registry, daemon or additional store. Avoid repeated offers in the same conversation after a refusal; retain existing recorded rules-folder answers. No other persistent refusal mechanism is assumed. No new module or automatic capability activation is authorized.

Explain separately that apply adds new unconditional core and skills files and that additions to already-selected modules follow their existing selection. Preserve existing safety, collision and provenance handling. Neither the offer nor an upgrade grants new credential access or resets existing consent.

## Rationale

The public plan and adoption command already identify and install optional modules. Reusing them avoids a parallel registry and makes an offer at a real need possible without polling. The unconditional tier remains governed by the existing Decision; a different policy would require a separate proposal.

## Alternatives considered

Upgrade-only offers miss needs arising later. A generic trigger engine and persistent refusal store add recurring maintenance without evidence beyond the already deployed rules-folder trigger. Silence leaves people to discover functionality themselves.

## Documentation / doctrine surface

Update `install/UPGRADE.md`, the shipped collaboration/onboarding guidance and their Cairn counterparts as appropriate; use existing inventory and module descriptions as sources. Instructions live in the collaboration guide, implementation description beside the installer, and deliberation here.

Proposed paths:
- `dev/modules/offers.md`

## Evidence / verification plan

A read-only plan that writes, an unselected module adopted without a yes, an offer missing a relevant unselected module, or a refusal bypassing existing collision/containment rules falsifies the proposal. Verify both an upgrade and a task-time need in disposable projects, using known and unknown costs honestly.

### Tests required

Use public `install/scaffold.py upgrade --plan` and `--adopt-module` in a disposable installation with selected and unselected modules. Extend `tests/test_upgrade_module_additions.py` only for a plausible uncovered behavior: plan has no writes and the explicit adoption changes the intended module alone. The reviewed plan maps the changed files through `python tests/tier_inventory.py for <paths>` and identifies exact nodes.

### Examples / smoke checks

Follow the guidance on a synthetic upgrade and a separate task-time need, including an accessible description, an unavailable source with a deferred offer, a no and a yes; verify the existing rules-folder offer still has its stated trigger and answer behavior. Run applicable prose gates and claim check. No real adopter, provider logs or external communication is needed.

#### Security preflight

N/A: no trust boundary added or widened; existing installer checks and human authorization remain.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Assurance path

Usual proposal review, an internally reviewed standard plan, and independent implementation review. No implementation or Decision is claimed. Elapsed: unknown; tokens: unknown.

## Review -- Terra (ordinary Reviewer) -- 2026-11-18

Reviewed commit: `73c2a6c5723c6d6b1b50767ec97b54417b67e04e`

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: unknown
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: offers at upgrade and at an actual need use existing adoption while preserving explicit choice and the read-only plan. Evidence: `dev/PLANNING.md` Group 4, module-offers row; `install/UPGRADE.md`.
2. **Best alternative.** Guidance using the existing plan, inventory and adoption command is cheaper to build and maintain than a trigger engine or refusal store; upgrade-only misses later needs. Evidence: `install/_scaffold/upgrade.py`; `dev/proposals/archive/2026-11-16-claude-staged-modules-and-triggers.md`.
3. **What would show it wrong?** In a disposable project, a plan that writes or an unselected module adopted without a yes falsifies the proposal; exercise both upgrade and a later need. Evidence: proposal, Evidence / verification plan.

**Steelman and audience.** The summary makes the choice understandable; instructions belong in installed guidance and the upgrade guide. Preserve the existing rules-folder duty and separate approval; the accepted Decision already keeps core and skills automatic, so it needs no new decision. Per-offer time and maintenance are unmeasured. A light Decision could be considered for guidance-only delivery, but the proposed standard tier stands unless the Maintainer changes it.

**Blocking — make task-time discovery actionable.** The installed inventory describes selected modules only, while the proposal requires source descriptions even between upgrades; it does not say how an adopter without the Cairn source available should identify unselected choices or what to do when the source cannot be accessed. Specify a reachable existing source and a truthful fallback that does not invent costs or adopt without consent; demonstrate both availability and absence in the task-time smoke check. Evidence: `templates/core/dev/modules/README.md`; proposal, Proposal.

**Coverage.** Read both board directions, the accepted Decision, installed inventory and upgrade guide. Did not run the installer, measure offer time or inspect every module description. No other rule loss identified in the proposed prose; implementation must preserve the existing adoption and collision checks.

## Response -- Terra (author) -- 2026-11-18

**Elapsed**: unknown. **Tokens**: unknown.

- Blocking, task-time discovery: accepted. Upgrade uses its supplied Cairn source; a later offer uses a verified accessible source or reference and defers truthfully when descriptions are unavailable. The smoke check covers both cases. The selected-only installed inventory is identified as insufficient by itself; no registry or tool is added.

### Withdrawn / superseded commitments

None. The offer remains due when the need arises and is deferred only while a usable description is unavailable.

## Decision -- Maintainer (scribed by Antigravity Gemini 4 Hydrogen) -- 2026-11-18

**Tier**: standard

**ACCEPTED.**

> "Yes, please accept all four as revised."

This accepts the v0.8 module-offers proposal as revised (`standard` tier, Internal plan review). New recurring human operations: zero.

**Elapsed:** under 1 minute. **Tokens:** unknown.
