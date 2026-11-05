# Make onboarding tasks one-time

**Author**: Codex Terra (medium)
**Status**: awaiting-review
**Review**: usual + Security Review
**Proposed tier**: heavy — the scaffold engine and install contract are high-risk surfaces.
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-04
**In brief**: Give projects first-use tasks once, then leave those tasks under project control.

## Decision summary

Onboarding should put useful first-use items on the board, not police them
afterward. The Maintainer said on 2026-11-04: “Oh, I don't think we should have
that onboarding go any further than putting the items on the PLANNING.md board.
Otherwise it's too heavy-handed.” Make task delivery one-time while retaining
module discovery and installer safety. This changes an accepted reconciliation
contract and needs careful migration and separate security review.

## Context

`bootstrap/_scaffold/install.py` renders tasks from the resolved roster, then
`_reconcile_generated_blocks` interprets board markers and may refuse removal
of edited tasks. `bootstrap/_scaffold/upgrade.py` calls
`_prepare_module_discovery` both for a new module and for an already-recorded
one. It currently requires a marked board and reconciles all tasks. The lock
writer computes an expected clean board using the same rendering.

The accepted [module discovery proposal](archive/2026-10-29-codex-module-discovery-activation.md)
and its [reconciliation design](../plans/archive/2026-10-29-module-discovery-activation/reconciliation.md)
require usable first-use tasks, inventory, preservation and repeat safety. The
accepted [board layout proposal](archive/2026-11-01-codex-shipped-board-layout.md)
protects existing boards from automatic replacement. The root board's cleaned
human text at `af57fc99` remains untouched by this proposal.

## Proposal

On initial scaffold, provide one actionable first-use task for each selected
module, including explicit and empty rosters and preset seeds, with a usable
entry point and expected result. On first explicit adoption of a new module,
offer its task once on the existing board; retain the inventory's accurate
selection, purpose and entry points. Manual-copy instructions must lead to
explicit adoption and discovery. Resolved profile/roster and the existing lock,
not board prose, remain selection authority. Already-locked adoption is repeat
adoption, not a reason to recreate a deleted task. No new task registry, state
file, recurring sync, completion policing or replacement tracking.

After delivery, tasks are ordinary project-owned text. Editing, completing or
deleting them, or removing their board tags, must not block adoption or
upgrade, trigger regeneration or deletion, or cause existing board text to be
overwritten. Source placeholders may guide initial rendering; installed boards
must not require persistent machine annotations. Existing marked boards migrate
without deleting or rewriting their human content; old annotations may remain
or be removed by the project without affecting later operations. Previously
locked modules receive no backfilled task on repeat adoption; newly adopted
modules receive only their own task. No automatic whole-board replacement.

The plan must resolve how a new task is placed on an existing, possibly
markerless board without overwriting it, and how a missing or unwritable board
is reported without falsely recording successful delivery. It must also settle
safe migration when no trustworthy lock exists: do not infer adoption history
from task text or silently claim delivery. These are unsettled design and trust
questions for the parent and reviewers, not authorization to invent another
tracking framework. Preserve roster-gated seeds, clean-install baseline
agreement, inventory reconciliation, existing path and token guards, lock/cache
commit safeguards and stage/apply input revalidation. Genuine unsafe paths,
write failures and unrelated conflicts must still refuse or report failure.

## Rationale

The existing lock already distinguishes a newly adopted module from a repeated
request. Using that distinction avoids treating a person's task edits as a
machine contract while retaining discovery and first-use guidance. The change
costs implementation and migration work in protected code; it does not make
task completion measurable or guarantee users retain the guidance.

## Alternatives considered

Do nothing: no build or migration cost, but ordinary task edits or removed
markers can still block adoption, losing the requested freedom. The least
involved credible alternative is to stop reconciling board tasks and provide
new-module guidance for a person to add manually; it reduces engine writes and
maintenance, but loses automatic first-use delivery on later adoption. Retain
marked reconciliation with more exceptions: it keeps automatic repair but
continues a fragile machine-owned board contract and its recurring complexity.
The proposal recommends one-time delivery because it preserves the useful
first-use outcome without ongoing task supervision.

## Documentation / doctrine surface

Update installed bootstrap and module documentation and board template to
describe actual first-use and manual adoption behavior; keep deliberation in
`dev/` and route any cross-cutting prescription to `AGENTS.md` only if needed,
following `docs/DOCUMENTATION_PLAN.md`. Preserve board working duties and
layout. This changes the prior install contract, not authority to execute a
module or a new recurring obligation.

## Evidence / verification plan

Before implementation, map all readers, callers, pins and stage/apply paths;
the plan must identify the complete module set and independent expected tasks.
The author searched `bootstrap/_scaffold`, `templates` and `tools/board.py`
for the task markers and discovery helper: the positive installer, template and
upgrade hits establish the search worked, but do not prove other spellings or
consumers absent. Recheck broader readers during planning. No prospective
behavior or mutations have been run.

### Tests required

Exercise real `bootstrap/scaffold.py` install and `upgrade --adopt-module`,
and upgrade plan/stage/apply where applicable. Start with
`bootstrap/tests/test_onboarding_seed_roster.py::test_selected_modules_have_usable_tasks`,
`bootstrap/tests/test_onboarding_seed_roster.py::test_reinstall_preserves_completion_and_refuses_loss`,
`bootstrap/tests/test_upgrade_module_additions.py::test_adoption_reconciles_tasks_and_inventory`,
`bootstrap/tests/test_upgrade_module_additions.py::test_already_recorded_adoption_repairs_missing_discovery`,
`bootstrap/tests/test_upgrade_module_additions.py::test_staged_module_discovery_refuses_changed_inputs`,
`bootstrap/tests/test_upgrade_module_additions.py::test_adoption_refuses_linked_discovery_destinations`,
and `bootstrap/tests/test_module_merge_lockfile.py::test_writer_still_refuses_when_a_merge_target_is_tampered`.
Update obsolete task-repair expectations and add narrow public-path checks for
fresh preset, explicit and empty rosters; first and repeated adoption; edited,
completed, deleted and unmarked tasks; legacy marked boards; unrelated prose;
missing lock or board; and independent selected versus unselected tasks.
Check inventory and clean lock agreement, missing/secret tokens, linked paths,
write failures and changed staged inputs. A legitimate task edit must not fail,
but these unrelated refusals must remain failures. Map exact nodes and consumers
in the plan; no full-tree certification is requested.

### Examples / smoke checks

Inspect temporary installed boards and inventory; run applicable claim, link,
snippet, content and neutrality gates on changed prose. Use the project's
scoped iteration and wide final integration rules for the protected contract.

#### Security preflight

S1: Inputs are shipped mappings, templates and presets, operator profile and
adoption request, existing lock and project files. Project-controlled board
text may be hostile; it supplies neither module authority nor executable code.

S2: At implementation, separately mutate a new-module task out of actual
install/adoption, regenerate a deleted task on repeat, overwrite unrelated
board text, permit a linked target, bypass a missing token, and ignore a changed
staged input. Each corresponding real-entry check must fail; none was run for
this proposal. Shared live/baseline rendering alone cannot independently prove
selection or preservation.

S3: The real scaffold install selects preset and explicit rosters; the real
upgrade adoption command selects a valid new or already-locked module. The plan
must name commands, complete input sets and the test runner for each check.
Proposed adopter-facing claim: “First use tasks are supplied once, then belong
to your project.” Verify it against those entry points and documented manual
adoption; do not claim delivery when placement failed.

S4: Missing or invalid authority, unsafe paths, token errors and failed writes
must not gain permission or be reported as success. Removed task markers and
ordinary task edits alone must not be treated as unsafe; inventory conflicts and
stage/apply changes retain their independent safeguards. Exact missing-board
failure ordering remains a plan and security question.

S5: An attacker able to edit a project board or profile can still write a
plausible hostile instruction; task ownership and lexical checks do not
authenticate it. The proposal does not close that class by enumeration.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A newly selected module lacks usable first-use guidance, a repeat recreates
deleted work, project text is lost, inventory misstates selection, or an
unrelated safety refusal becomes success. Unresolved placement or migration
that cannot meet both delivery and preservation is also a reason to reconsider.

## Scope delta

**Scope delta**: preserved for this opening proposal; it proposes changing the
earlier task-reconciliation contract explicitly, subject to Maintainer Decision.

## Assurance path

**Assurance path**: high-assurance — scaffold engine, install contract and
adopter-executed surfaces. Ordinary and Security Reviews are separate.
