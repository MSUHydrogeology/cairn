# Make onboarding tasks one-time

**Author**: Codex Terra (medium; opening), Codex Sol (gpt-6.1-sol; revision), Codex Terra (medium; response)
**Status**: accepted
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
module discovery and installer safety. This changes the accepted reconciliation
contract; ordinary and Security Reviews remain separate.
The cost is that a manually added task may be duplicated and a removed module's
task may remain until the project edits or deletes it.

## Context

`bootstrap/_scaffold/install.py` renders tasks from the resolved roster, then
`_reconcile_generated_blocks` interprets board markers and may refuse removal
of edited tasks. `bootstrap/_scaffold/upgrade.py` calls
`_prepare_module_discovery` both for a new module and for an already-recorded
one. It currently requires a marked board and reconciles all tasks. The lock
writer computes an expected clean board using the same rendering.

The accepted [module discovery proposal](2026-10-29-codex-module-discovery-activation.md)
and its [reconciliation design](../../plans/archive/2026-10-29-module-discovery-activation/reconciliation.md)
require usable first-use tasks, inventory, preservation and repeat safety. The
accepted [board layout proposal](2026-11-01-codex-shipped-board-layout.md)
protects existing boards from automatic replacement. The root board's cleaned
human text at `af57fc99` remains untouched by this proposal.

## Proposal

Initial creation uses existing preset/module rendering for one actionable
first-use task per selected module: plain headings and checkboxes, usable entry
points, expected results, roster-gated seeds, explicit and empty selections, no required
persistent board annotations. First adoption of a new module appends only its
heading/checkbox task block at EOF, preserving the board as an exact byte prefix.
Do not search heading locations or treat an existing Onboarding heading as
parser authority. Keep inventory selection, purpose and entry points accurate;
manual copying still requires explicit adoption.

Use the existing module lock roster for once-only delivery. An already-locked
repeat never rewrites, restores or backfills tasks; inventory updates may
continue independently. Normal reinstall leaves an existing project-owned board
byte-identical, including legacy annotations: no migration rewrite or backfill.
After delivery, edits, completion, deletion or tag removal cannot block adoption
or upgrade or trigger task regeneration/deletion. Old tags may remain as ordinary
text or be removed freely. No new registry, state file, sync, completion policing
or replacement tracking. Normal paths never replace whole boards; explicit
scaffold `--force` retains its existing whole-file overwrite authority.

This intentionally supersedes the October 29 guarantees of no duplicate tasks
and no tasks for absent modules: first adoption can append a task already added
manually, and a task for a later-removed module can remain until the project
edits or deletes it. The Maintainer must decide whether to accept this loss of
machine reconciliation.

A missing, unwritable or unsafe board is an explicit adoption failure before
claiming delivery or recording adoption, not successful stdout-only guidance.
Missing, malformed or unusable locks retain refusal and the existing
`upgrade --init-lock` recovery path; never infer history from board text or claim backfill. Prepare
board/inventory/lock outputs through the existing transaction path. Preserve
path/token guards, lock/cache safeguards, stage/apply input checks and
clean-install baseline agreement. A valid existing lock is usable for this
roster decision, not a cryptographically authenticated record. Do not turn
unrelated conflicts or failed writes into success or promise arbitrary crash rollback.

## Rationale

The existing lock distinguishes new from repeated adoption. EOF append needs no
board parser and leaves prior bytes alone. Protected-code changes and tests
cost implementation effort; no recurring tracking burden is added, and users
need not retain or complete guidance.

## Alternatives considered

Do nothing costs no build effort but retains marker-related refusals, losing
the requested freedom. Least involved: report new-module guidance for manual
addition; fewer writes and tests, but automatic first-use delivery is lost.
More reconciliation exceptions retain repair but keep parsing and ongoing
maintenance. Recommend one-time delivery: it preserves first-use help with no
ongoing task supervision, at the cost of occasional duplicate or stale tasks
instead of ongoing parsing and gates.

## Documentation / doctrine surface

Describe first-use and manual adoption in installed bootstrap/module docs and
the board template, preserving duties and layout. Keep deliberation in `dev/`;
route any needed cross-cutting prescription to `AGENTS.md` under
`docs/DOCUMENTATION_PLAN.md`. No new execution authority or recurring duty.

## Evidence / verification plan

Opened install rendering/lock baseline, CLI core/onboarding/force calls and both
adoption branches through `_record_discovery_outputs` and
`_commit_lock_and_caches`. Marker/helper searches found positive installer,
template and upgrade controls, no `tools/board.py` match; other spellings remain
unproven. The plan maps remaining readers, pins, stage/apply consumers and the
complete module set independently. No prospective behavior or mutations run.

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
completed, deleted and unmarked tasks; legacy boards; exact EOF prefix;
byte-identical normal reinstall versus explicit force; missing lock/board;
selected versus unselected tasks. Check inventory/clean lock agreement, token
refusals, linked paths, write failures and changed staged inputs. Task edits
alone cannot fail; unrelated refusals remain failures. No full-tree run.
The plan must test missing, malformed and unusable locks through the actual
adoption entry, with passing controls. `read_lockfile` checks JSON shape;
adoption cannot assume the later `_check_lockfile_paths` has already run.
This closes the existing refusal promise, not a new cryptographic trust root or
a broad lock refactor.

### Examples / smoke checks

Inspect temporary installed boards and inventory; run applicable claim, link,
snippet, content and neutrality gates on changed prose. Use the project's
scoped iteration and wide final integration rules for the protected contract.

#### Security preflight

S1: Inputs are shipped mappings/templates/presets, operator profile/request,
lock and project files. The resolved profile selects initial modules; the lock
plus valid explicit request selects adoption. Project-controlled board text
supplies neither selection authority nor executable code.

S2: At implementation, separately mutate a new-module task out of actual
install/adoption, regenerate a deleted task on repeat, overwrite unrelated
board text, permit a linked target, bypass a missing token, and ignore a changed
staged input. Each corresponding real-entry check must fail; none was run for
this proposal. Shared live/baseline rendering alone cannot independently prove
selection or preservation.

S3: The real scaffold install selects preset and explicit rosters; the real
upgrade adoption command selects a valid new or already-locked module. Test the
input cases above through those commands. Proposed adopter-facing claim:
“First use tasks are supplied once, then belong to your project.” Verify both
entry points and manual adoption; failed placement cannot count as delivery.

S4: Missing or invalid authority, unsafe paths, token errors and failed writes
must not gain permission or be reported as success. Removed task markers and
ordinary task edits alone must not be treated as unsafe; inventory conflicts and
stage/apply changes retain independent safeguards. Missing/unwritable/unsafe
boards fail before adoption is recorded; missing locks require initialization.

S5: An attacker able to edit a project board or profile can still write a
plausible hostile instruction; task ownership and lexical checks do not
authenticate it. The proposal does not close that class by enumeration.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

A newly selected module lacks usable first-use guidance, a repeat recreates
deleted work, project text is lost, inventory misstates selection, or an
unrelated safety refusal becomes success.

## Scope delta

**Scope delta**: degraded -- The October 29 no-duplicate and no-tasks-for-absent-
modules guarantees are intentionally superseded: first adoption may duplicate a
manual task, and tasks for removed modules may remain until project editing or
deletion. This narrow loss of machine reconciliation is proposed for the
Maintainer's Decision; no concession is made here. Specifying automatic cleanup
or matching would retain ongoing parsing and gates, contrary to the proposed
project ownership. First-use delivery, inventory, board preservation and the
independent safety safeguards remain in scope. **Disposition**: proposed accept,
pending Maintainer Decision.

## Assurance path

**Assurance path**: high-assurance — scaffold engine, install contract and
adopter-executed surfaces. Ordinary and Security Reviews are separate.

## Review -- Codex Terra (MEDIUM) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** One-time delivery addresses the Maintainer's concern while preserving user bytes, but the decision must expose the prior guarantees it would relax -- Proposal and Scope delta; accepted module-discovery proposal, Proposal.
2. **Best alternative.** Retain reconciliation and its conflict handling: it preserves the prior no-duplicate and no-absent-module-task guarantees, but continues policing project edits -- `bootstrap/_scaffold/install.py::_reconcile_generated_blocks`; accepted module-discovery proposal, Proposal.
3. **What would show it wrong?** A real first adoption that loses board bytes, fails to deliver a usable task, or records success after a placement failure would defeat the proposed split -- Tests required; `bootstrap/_scaffold/upgrade.py::_prepare_module_discovery`.

Reviewed commit: 8c5aabcada29ee5963ee5bb58ba45880d5948b2a

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Blocking -- Name the superseded guarantees.** The accepted October 29 proposal requires no duplicate tasks and no tasks for absent modules. An unconditional append on first lock adoption can duplicate a manually present task; project-owned tasks may remain after module removal. The new proposal clearly specifies no board parsing or deletion, but says scope is preserved without naming those consequences. The Maintainer cannot weigh that loss from the scope record. Close by explicitly identifying these superseded guarantees and their user-visible costs, and presenting the change for the Maintainer's Decision; do not silently promise both contracts.

The November 1 board-layout duties and protection of existing content remain in scope; EOF append preserves the original bytes, not necessarily the former onboarding location. Separate Security Review remains owed.

**Elapsed**: approximately 3 minutes. **Tokens**: unknown.

**Coverage**: Committed proposal, current template, both accepted proposals, installer reconciliation and adoption entry, and named test locations. **Not covered**: prospective implementation, actual install or adoption runs, mutations, Security Review, full suite or release checks.

## Review -- Codex Sol (HIGH) -- 2026-11-04

**Foundations**

1. **Should this happen as framed?** Yes: project-owned tasks need not authorize module selection or execution; removing task reconciliation can preserve independent inventory and safety checks -- Proposal, S1/S4; `bootstrap/_scaffold/upgrade.py::_cmd_adopt_module`.
2. **Best alternative.** Guidance for manual addition costs fewer writes/tests but loses automatic delivery. EOF append and the existing lock roster retain delivery without a recurring registry; implementation/testing costs remain -- Alternatives; `bootstrap/_scaffold/upgrade.py::_record_discovery_outputs`.
3. **What would show it wrong?** Real-entry mutations that omit a new task, regenerate deleted work, overwrite prior bytes, admit links/missing tokens or ignore changed staged inputs must fail beside passing controls -- Tests required and S2; `bootstrap/tests/test_upgrade_module_additions.py::test_staged_module_discovery_refuses_changed_inputs`.

Reviewed commit: 8c5aabcada29ee5963ee5bb58ba45880d5948b2a
Ordinary review read: 988621c8.

**Tier**: Security Review
**Findings**: no additional Security findings; ordinary blocking finding remains open.
**Verdict**: ACCEPT -- Security design only, not a Decision.

Both adoption branches currently call `_prepare_module_discovery`; repeat
handling must stop board writes without disabling independent inventory checks.
`_record_discovery_outputs` feeds the existing transaction; `_commit_lock_and_caches`
stages writes, protects live caches and replaces the lock last, not arbitrary
crash rollback. `_install_one` separates ordinary preservation from explicit
force; clean-baseline refusal remains independently required.

S4's invalid-lock promise needs evidence at the actual adoption route:
`read_lockfile` accepts JSON objects, and adoption dispatch precedes
`_check_lockfile_paths`. Do not infer validation from that later guard.
The proposal already requires refusal, so this is an implementation hazard,
not an added criterion.

October 29's usable tasks/inventory and November 1's board duties remain scope.
Terra's "Name the superseded guarantees" blocker still requires an explicit
account of duplicate/stale-task costs and the Maintainer's Decision; this pass
does not waive it.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Committed proposal, ordinary review, prior Decisions, template,
install/adoption/lock/stage/apply call paths, write guards and named test bodies.
**Not covered**: prospective implementation or mutation outcomes; no
implementation tests or full suite run. S5 remains: project-controlled text
can contain hostile instructions; ownership does not authenticate it.

## Response -- Codex Terra (MEDIUM) -- 2026-11-04

- **Ordinary blocker -- accepted.** The Proposal, alternatives and Scope delta
  now name both duplicate and stale tasks and submit the loss of the October 29
  guarantees to the Maintainer. The opening's first-use delivery and safety
  commitments remain; no matching or cleanup mechanism is added.
- **Security advice -- accepted.** The plan must test missing, malformed and
  unusable locks at the actual adoption entry. JSON shape alone and a later path
  check do not establish refusal there. A usable lock is not authenticated;
  path, token, transaction and staged-input protections remain required. These
  are prospective checks, not passing results.

**Elapsed**: unknown. **Tokens**: unknown.

### Withdrawn / superseded commitments

The prior no-duplicate and no-absent-module-task guarantees are proposed for
supersession by project-owned tasks, subject to the Maintainer's Decision.

## Decision -- Maintainer -- 2026-11-05

Elapsed: unknown. Tokens: unknown.

**Tier**: heavy

**ACCEPTED.** The authorization below answers the assistant's question, “May I
record the reviewed one-time onboarding proposal as accepted? It stops managing
board tasks after adding them. The tradeoff is that first adoption may duplicate
a manually added task, and tasks may remain after a module is removed. Keeping
today’s behavior avoids those cases but retains tags, reconciliation and related
upgrade refusals. I recommend one-time delivery.” The following quoted words
are the Maintainer's answer, not the question:

> "Accept one-time onboarding (Recommended)"

Accept the reviewed heavy contract and its explicit, narrow loss: manual tasks
may be duplicated on first adoption, and tasks may remain after module removal.
Retain safety, inventory, token, path, write, refusal and lock safeguards. This
Decision adds no recurring machinery and grants no release or trust-operation
authority.
