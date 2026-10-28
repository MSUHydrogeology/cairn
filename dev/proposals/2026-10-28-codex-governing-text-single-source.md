# Make Cairn's governing text easier to edit without losing adopted rules

**Author**: Codex (Proposal author, gpt-6-sol)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-28
**In brief**: Map where adopters find each rule, then shorten repeated instructions while keeping every rule available to them.

## Context

Cairn's four internal governing files now total 1,838 lines (`wc -l` on
`AGENTS.md`, `dev/agent_collaboration.md`, and the two `_template.md` files,
2026-10-28). Their shipped counterparts add 1,731 lines. The recovery strategy
calls for shorter templates and less wording-sensitive prose tests
(`dev/strategy/2026-08-21-claude-nimbleness-recovery.md` > item 1).

The present split needs explanation before editing: `doctrine/README.md` says
published doctrine explains the method, while `bootstrap/_scaffold/config.py`
maps `templates/core/AGENTS.md` to installed `AGENTS.md` and likewise installs
the collaboration file and both templates from `templates/core/dev/`. It does
not install `doctrine/`. The adopter can read published
doctrine in Cairn's repository, but a `doctrine/` citation in an installed file
is not a local rule. `docs/DOCUMENTATION_PLAN.md` calls the former methodology
authority and the latter adopter-facing operating text. The existing tests
explicitly guard this distinction (`bootstrap/tests/test_review_and_verification_rules_ship.py`,
`test_scope_reduction_trap.py`). Which parts truly need each home, and whether
the published doctrine should remain separate from `docs/`, have not yet been
established for this compression.

## Proposal

The plan starts with a rule-by-rule routing audit of these eight internal and
shipped governing files. For each operative rule, record its current source,
adopter-installed location, pointer and published explanation; identify exact
duplicates, wording-pinned tests, and rules without an installed home. Check
the installer mapping and real installed output for a small and a fuller
profile, including where `doctrine/` references lead. Distinguish operational
rules, deliberation procedure, template fields, and explanatory rationale.

Before relocating or deleting a rule, a MAINTAINER-GATED plan fence presents
the audit and a recommended routing map. It compares retaining published
`doctrine/` as rationale with consolidating suitable explanation into `docs/`,
and keeps adopter obligations in an installed canonical home. The Maintainer
chooses that routing; this proposal does not pre-decide the doctrine/docs split.

Then remove duplicated exposition from the four governing files and their
shipped twins. Keep an imperative operating rule in installed `AGENTS.md` when
a cold agent needs it; keep deliberation detail in installed
`dev/agent_collaboration.md`; keep template fields, short triggers and pointers
beside authoring. Aim for 80–120 lines per template where the rule inventory
allows it, but do not drop an adopted obligation to hit a line count. Replace
paragraph-shaped regex pins only with checks of the same obligation in its
installed home, real entry-point reachability, and a deletion or inversion
control. Retain tests that protect distinct semantics. No new directory or
general-purpose routing tool is proposed.

## Rationale

Inventory first makes “single source” a testable routing decision. It avoids
turning an explanatory citation into a missing adopted instruction. Shorter
loaded files reduce reading and editing cost; rule-preservation checks let
wording change without silently changing the method.

## Alternatives considered

Move all detail into `doctrine/`: shortest installed templates, but required
rules would live outside the adopter tree. Keep all copies: no migration risk,
but duplication and wording freezes remain. Merge all doctrine into `docs/`:
perhaps simpler navigation, but governing rationale could become merely
descriptive; the audit must show which content can move without that loss.

## Documentation / doctrine surface

This proposal occupies `dev/`. The audit may lead to paired changes in
`doctrine/`, `docs/`, internal governing files, and `templates/core/` twins;
`docs/DOCUMENTATION_PLAN.md` and its forkable template govern the placement
decision and would update together if their structural routing changes.

## Evidence / verification plan

### Tests required

The plan maps every changed paragraph to its owning test, especially
`bootstrap/tests/test_review_and_verification_rules_ship.py`,
`test_scope_reduction_trap.py`, `test_writing_rules_ship.py`,
`test_model_tier_rule_ships.py`, and `test_review_sweep_ships.py`. Each revised
guard must pass on the rule and fail when the operative clause is removed from
the installed output. Check the eight source files for parity. Test counts,
interpreter and any unowned surface go into the implementation record; the
frozen-test and doctrine ceremonies follow their existing runbooks.

### Examples / smoke checks

Use the scaffold's real install path on representative profiles, inspect its
output and cited destinations, and run `scripts/claim_check.py`,
`scripts/link_check.py`, and applicable `scripts/quality_gate.py` subsets.
This proposal's path claims are checked before commit. A pointer that only
resolves in Cairn's repository must be labeled as published guidance, never
presented as an installed mandatory home.

#### Security preflight

**S1 — Inputs.** The routing decision reads committed source files, the
installer mapping, installed output, and existing tests; the files under
review also supply the pointers being judged, so check them against the
installer's independent mapping.
**S2 — Failure.** Removing an installed obligation must fail its guard;
restoring it must pass. Two existing deletion controls in the named tests
passed on 2026-10-28 (`pytest`, 2 passed); the new mapping's controls run
during implementation.
**S3 — Trigger.** Scoped pytest nodes, run by the implementer and reviewer,
invoke `scaffold.py` on named profiles and inspect installed output. No CI
trigger is claimed. Installed text will describe any manual trigger accurately.
**S4 — Failures.** An unresolved home or pointer blocks relocation; no
fallback treats a published citation as installed text.
**S5 — Limit.** This protects against accidental rule loss, not a deliberately
misstated rule; human review compares the meaning with the inventory.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

An adopter install omits an operative rule, a mandatory pointer has no
reachable installed target, a changed guard passes after its clause is deleted,
or compression leaves the templates harder to use despite fewer lines.

## Scope delta

N/A: opening proposal; no baseline outcome has been removed.

## Assurance path

**Assurance path**: high-assurance. The proposed changes may touch `doctrine/`
and authoring templates, named high-assurance surfaces in the proposal template.
