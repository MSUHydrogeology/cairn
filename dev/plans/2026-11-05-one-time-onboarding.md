# Plan: One-time onboarding tasks

**Source proposal**: dev/proposals/archive/2026-11-04-codex-one-time-onboarding.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-05
**Author**: Codex Terra (MEDIUM)
**In brief**: Deliver useful module tasks once, then leave the board under project control.

## Source proposal

Decision `2a233544` accepts one-time delivery and only the named loss of
duplicate and stale-task guarantees. Inventory, useful first-use guidance,
board duties and independent installer safeguards remain. Manual copies need
explicit adoption; the existing lock roster, not board text, decides whether
an adoption is new. A valid lock is not an authenticated history.

## Scope

Change `bootstrap/_scaffold/` install and upgrade paths, their owning tests,
board and onboarding templates, and installed bootstrap/module documentation.
Initial preset, explicit and empty selections get one usable task per selected
module, with actual entry point, inputs and expected result; inventory reflects
selection, including removals. First new-module adoption appends only its task
block at EOF, retaining every original board byte as a prefix. No heading search
or tag reconciliation. Already-locked adoption, reinstall, repair and removal
never mutate, backfill or migrate board tasks, including legacy tags; inventory
may update independently. Only explicit `--force` retains existing whole-file
overwrite authority. Preserve root board human text from `af57fc99`.

**Reuse.** Searches at `0d6d2065` for `onboarding-tasks`, `cairn:module`,
`_reconcile_generated_blocks` and `_rendered_onboarding_overlay` found
`install.py`, `upgrade.py`, `slotmerge.py`, CLI, board/preset templates and
their tests, plus the AST fixture. Reuse selection, discovery metadata,
existing validators and the board/inventory/lock transaction, path/token and
cache safeguards; do not build a parallel upgrade engine. Map other spellings,
readers, pins and plan/stage/apply inputs before editing. Live and pristine
clean-lock board baselines must agree without making shared rendering the only
selection oracle.

The independent module universe is the 22 keys of `_MODULE_MAPPINGS` in
`bootstrap/_scaffold/config.py` at `0d6d2065`, not the discovery helper:
reflections, claim-check, incident-trackers, documentation-plan, dual-review,
domain-agents, legacy-agent, dual-language-tests, coordination-tiers,
security-review, issue-capture, model-selection, testing-discipline,
doc-drift-prevention, examples-gallery, content-security, python-security,
portable-security-sweeps, api-access-security, web-hosting-security,
architecture-review and security-verification. At implementation derive the
current complete set again from committed mapping bytes and audit each shipped
task, purpose, entry, inputs and result against installed artifacts; do not
inherit prior figures or infer coverage from the helper under change.

### Documentation / doctrine surface

Update installed `bootstrap/BOOTSTRAP.md` and `templates/modules/README.md`
delivery and the board template, preserving board duties and manual adoption
instructions. Update other mapped adopter-facing readers as needed; route
cross-cutting prescription only to `AGENTS.md` if actually needed under
`docs/DOCUMENTATION_PLAN.md`. No new recurring doctrine or execution authority.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Map committed consumers, pins, module/task inventory and pristine install/lock baseline; implement delivery, independent inventory and adoption validation using existing transaction and guards. | Both plan reviews and author response | Engine, focused tests and adopter documentation. |
| C2 | Run scoped iteration, required real-entry controls and separate mutations; obtain ordinary and Security code reviews, address findings, then run wide Boundary B. | C1 | Reviewed implementation and verification record. |

Maintainer-owned AST/gate trust operations remain the separate board 12 wait;
they are not a plan completion chunk or permission to release. Do not claim
arbitrary crash rollback or turn unrelated conflicts and failed writes into
success.

## Acceptance criteria

**C1.** Real `bootstrap/scaffold.py` installs cover every current mapped module,
preset, explicit and empty rosters, selected versus unselected tasks, usable
installed entry points and accurate inventory. A pristine board and lock
baseline agree independently of the selection oracle. Real adoption tests show
exact EOF prefix and one new task, then no board mutation for repeat, edits,
completion, deletion, removed tags, legacy text, repair, removal or normal
reinstall; force alone retains its existing overwrite behavior. Inventory keeps
its independent updates and conflict checks. Missing, malformed or unusable
locks refuse at the actual adoption entry with passing controls; JSON shape and
later `_check_lockfile_paths` do not suffice. Missing, unwritable or unsafe
board placement fails before lock success or adoption is recorded. Retain
`--init-lock`, token, linked-path, write, cache, stage/apply and unrelated
refusal safeguards; no new registry or historical backfill.

**C2.** Test the real install, `upgrade --adopt-module`, and applicable
plan/stage/apply entry paths, including manual-adoption documentation. Start
with `bootstrap/tests/test_onboarding_seed_roster.py::test_selected_modules_have_usable_tasks`,
`::test_reinstall_preserves_completion_and_refuses_loss`,
`bootstrap/tests/test_upgrade_module_additions.py::test_adoption_reconciles_tasks_and_inventory`,
`::test_already_recorded_adoption_repairs_missing_discovery`,
`::test_staged_module_discovery_refuses_changed_inputs`,
`::test_adoption_refuses_linked_discovery_destinations`, and
`bootstrap/tests/test_module_merge_lockfile.py::test_writer_still_refuses_when_a_merge_target_is_tampered`;
update obsolete expectations without dropping controls. Map and retain the
relevant `test_module_roster.py`, `test_upgrade_module.py`, install, lock and
stage/apply owners. Include `--summary`, `--dry-run` and `--manifest` with
representative profiles and installed-tree checks.

S2/S3: With passing real-entry controls, separately mutate omitted new tasks in
install and adoption, regenerated deleted repeat work, overwritten prior bytes,
linked targets, missing-token refusal and changed staged inputs; each relevant
check must fail. Also independently mutate an unselected task into output and
the clean lock baseline, and check failed writes. Derive each fixture from the
committed candidate and test each module independently; report outcomes and
omissions. Structured operator profile fields select initial modules; embedded
board/profile task prose grants neither selection nor execution authority.
Hostile project text remains unauthenticated. No scientific check applies.

## Scope delta

**Scope delta**: preserved relative to Decision `2a233544`; its explicit
duplicate/stale-task concession is not extended.

## Verification

Boundary A: use `python tools/test_tiers.py for <changed paths>` and run its
iteration list, named controls and applicable claim, link, snippet, content,
neutrality and redundancy gates. Map changed files, callers, readers, pins and
consumers to tests; name missing coverage and remedy it. Use the canonical
Python 3.13 interpreter and committed candidate bytes for fixtures and mutation
copies. Boundary C: independent ordinary and Security code reviews challenge
the implementation with targeted falsification, not a suite. Boundary B: after
review and fixes, run the required wide selection on a clean unchanged final
commit, including mapped iteration and integration/workflow tests, public paths,
standing gates and these acceptance checks. Record SHA/range, interpreter,
clean pre/post state, commands, counts, elapsed time, tokens or unknown,
non-passes, omissions and timing misses in the implementation verification
record. No routine full-tree certification is authorized by this plan.

## Plan review -- Codex Terra (MEDIUM) -- 2026-11-05

Reviewed commit: 4e75521290495179d1c3e637e13e799f25400be5

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: SHIP

**Foundations**

1. **Should this happen as framed?** Yes: the plan retains first-use delivery, board ownership, inventory and refusal safeguards, and tests them at the entry points required by the Decision -- Scope and C1; source Decision `2a233544`.
2. **Best alternative.** Reusing the lock roster, existing discovery transaction and selection machinery is the simplest identified route to the same outcomes; a stdout-only task would lose automatic delivery -- Scope and C1; `bootstrap/_scaffold/upgrade.py::_record_discovery_outputs`.
3. **What would show it wrong?** A real adoption that records success without a task, changes prior board bytes, or regenerates deleted work on repeat would falsify delivery or ownership; the planned separate mutations should make the corresponding checks fail -- C1 and C2.

The current repeat and first-adoption branches both call
`_prepare_module_discovery`, which reconciles board tasks and inventory;
the plan distinguishes their board behavior while retaining inventory checks.
The clean-lock baseline currently shares onboarding rendering with installation;
the independent roster and unselected-task mutation guard against shared error.
The plan correctly leaves the separate Security plan review and both code
reviews outstanding.

**Elapsed**: approximately 4 minutes. **Tokens**: unknown.

**Coverage**: Committed plan and template, accepted proposal and Decision,
install rendering and lock baseline references, adoption and transaction paths,
and named test locations. **Not covered**: implementation behavior, mutation
results, Security Review, full suite, or release and trust operations; no
implementation checks were rerun.

## Plan review -- Codex Sol (HIGH) -- 2026-11-05

Reviewed commit: 4e75521290495179d1c3e637e13e799f25400be5

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: one nonblocking recommendation
**Verdict**: ACCEPT -- Security plan only; no scope waiver.

**Foundations**

1. **Should this happen as framed?** Yes: EOF delivery and lock-roster repeat handling preserve the Decision's safety obligations while conceding only duplicate/stale tasks -- Decision `2a233544`; C1; `bootstrap/_scaffold/upgrade.py::_cmd_adopt_module`.
2. **Best alternative.** Separate board delivery from inventory reconciliation within the existing guarded transaction, retaining source verification rather than adding a registry or trusting task markers -- `bootstrap/_scaffold/upgrade.py::_prepare_module_discovery`, `_render_review_inventory` and `_commit_lock_and_caches`.
3. **What would show it wrong?** A passing real-entry control whose separate missing-task, prefix-overwrite, token-bypass or stale-stage mutation also passes would invalidate assurance; test valid existing locks alongside unusable-lock refusals -- C1/C2; `bootstrap/tests/test_upgrade_module_additions.py::test_staged_module_discovery_refuses_changed_inputs`.

**SP1 -- Nonblocking: distinguish profile fields from instructions.** C2 says
"Board/profile text cannot authorize selection", but structured operator profile
fields intentionally select initial modules. Close by distinguishing those
fields from embedded task prose, which grants neither selection nor execution
authority -- `bootstrap/_scaffold/cli.py:330`; source S1. This requests wording
precision, not a new permission or reduced safeguard.

Retain adoption's strict absent/blank/curly/angle-placeholder refusals and
lock-over-profile token precedence; the existing token tests distinguish these
cases (`bootstrap/tests/test_upgrade.py:2017`). Adoption dispatch precedes
`_check_lockfile_paths`; JSON-object parsing cannot establish usable state.
Valid migrated locks may lack recoverable bases; do not equate usability with
pristine bytes or authenticated history (`bootstrap/_scaffold/upgrade.py::_cmd_init_lock`).
Board failure must precede recording adoption. The existing transaction stages
outputs and moves the lock last; it does not guarantee arbitrary crash rollback.
C1/C2 retain these independent refusals and prospective real-entry controls.

Judgment formed before reading ordinary review `298ba178`.

**Elapsed**: unknown. **Tokens**: unknown.

**Coverage**: Committed plan/template/Decision, cited prior contracts, selection,
source verification, placeholder, install/adoption/lock/cache and stage/apply
paths, and named test bodies. **Not covered**: future implementation or mutation
results, concurrent path-swap resistance, native-platform behavior, full suite,
release or trust operations. No implementation checks replayed.

## Plan review response -- Codex Terra (MEDIUM) -- 2026-11-05

Ordinary review: no findings. Security SP1: accepted; C2 now distinguishes
structured operator profile fields from embedded task prose. Scope, checks and
lock safeguards remain unchanged.

**Elapsed**: unknown. **Tokens**: unknown.
