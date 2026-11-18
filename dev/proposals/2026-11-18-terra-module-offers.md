# Offer missing functionality at upgrade and when needed

**Author**: Terra (Implementation, Medium)
**Status**: awaiting-review
**Review**: usual
**Proposed tier**: standard — guidance across upgrade and task-time workflows; no installer change
**Plan review**: required(Internal)
**Opened**: 2026-11-18
**Rules that apply**: dev/rules/conventions.md, dev/rules/protected-surfaces.md, dev/rules/working-agreements.md
**In brief**: Explain unselected Cairn functionality at upgrade and when a project needs it, and ask before adopting an optional module.

## Decision summary

An upgrade lists unselected modules by name without explaining their value or cost; a project can also reach a need between upgrades. Guide the agent to explain relevant choices in plain language, ask the person, and use the existing explicit module-adoption command on a yes. Keep the upgrade plan read-only. New core and skills files continue to arrive automatically on apply under the existing Decision, and the agent explains that separately. The work changes guidance, with effort and per-offer time unmeasured; no new background service is proposed.

## Context

`install/_scaffold/upgrade.py` computes available modules as shipped modules minus the lockfile roster, including previously unselected modules. `install/UPGRADE.md` says the public `--plan` writes nothing and `--adopt-module` deliberately adopts one module. The same guide and engine show that `--apply` adds new unconditional core and skills files; new files belonging to already-adopted modules also follow their selected module. Collision and provenance cases can block. The 2026-11-12 direction in `dev/PLANNING.md` covers new or omitted functionality, not only newly published modules. The [2026-11-16 Decision](archive/2026-11-16-claude-staged-modules-and-triggers.md) accepted the default: “core and skills files remain automatic on upgrade”.

The accepted [staged-modules proposal](archive/2026-11-16-claude-staged-modules-and-triggers.md) and its implementation already offer rules-folder guidance at the stated 5,000-word trigger, using the session-start skill and `dev/modules/offers.md`. That guidance is already shipped; its yes means help planning changes, not module installation. The 2026-11-16 [grown-projects strategy](../strategy/2026-11-16-claude-guidance-for-grown-projects.md) calls for offers when a project reaches a need, and cautions against noisy triggers.

## Proposal

At upgrade, have the agent read the public plan's unselected-module list and the existing module descriptions in the Cairn source and installed inventory; explain each available module's purpose and concrete known costs, marking unknown costs unknown, and ask which, if any, to adopt. Correct the guide's “since install” wording to include unselected modules. A yes authorizes the existing `upgrade --adopt-module <name>` for that module, subject to its existing checks; a no leaves it unselected. `--plan` remains read-only and does not enable functionality or access credentials.

Between upgrades, when a task exposes a concrete project need, the agent consults the existing installed module inventory and onboarding material alongside the Cairn source module descriptions, checks whether an applicable module is unselected, and offers it before adoption with the same explanation and choice. The agent does not infer consent from a task. Preserve the existing rules-folder trigger and its answer record, threshold and separate approval for changes to project rules. Do not introduce a generic trigger registry, daemon or additional store. Avoid repeated offers in the same conversation after a refusal; retain existing recorded rules-folder answers. No other persistent refusal mechanism is assumed. No new module or automatic capability activation is authorized.

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

Follow the guidance on a synthetic upgrade and a separate task-time need, including a no and a yes; verify the existing rules-folder offer still has its stated trigger and answer behavior. Run applicable prose gates and claim check. No real adopter, provider logs or external communication is needed.

#### Security preflight

N/A: no trust boundary added or widened; existing installer checks and human authorization remain.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Assurance path

Usual proposal review, an internally reviewed standard plan, and independent implementation review. No implementation or Decision is claimed. Elapsed: unknown; tokens: unknown.
