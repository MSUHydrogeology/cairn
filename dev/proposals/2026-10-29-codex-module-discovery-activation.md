# Find and activate installed modules

**Author**: Codex (gpt-6.1-sol)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-29
**In brief**: Make installed modules easy to find and give each selected module an actionable first-use task.

## Context

The v0.6 board asks for discovery and first-use tasks for existing modules,
while reserving expanded architecture-review capability for v0.7
(`dev/PLANNING.md`). Onboarding is installed only for a preset (`bootstrap/_scaffold/cli.py`);
preset seeds do not cover every selection (`templates/onboarding/`).
The module catalog is under `templates/modules/README.md`, while the installed
files go to `dev/modules/` (`bootstrap/_scaffold/install.py`). Later adoption includes manual copy and proposal (`bootstrap/BOOTSTRAP.md`)
and `upgrade --adopt-module`, which updates files and lock but not onboarding
(`bootstrap/_scaffold/upgrade.py`). An adopter cannot rely on an installed catalog or a task for every selection.

## Proposal

Audit module mappings, selection, generated files and adoption. Ship an installed,
agent-discoverable inventory that identifies each installed module, its purpose
and usable entry point; direct relevant session/lifecycle prompts to it without
making use of every module a recurring ceremony. It must represent the actual
selection, including empty and explicit lists, additions and removals, rather
than the preset name alone. Commands and linked artifacts must resolve in the installed tree and explain required inputs.

Provide one distinct, actionable first-use task per installed module in the
existing `dev/PLANNING.md` onboarding slot. Each names a command or artifact
and the expected result, and respects whether the capability is optional or
needs a human decision. Include modules selected without a preset. On later adoption, including `upgrade --adopt-module`, provide the task and
inventory update; for a manual copy, document concrete steps rather than
claiming automatic detection. Preserve
existing tasks and completed work on repeated operations; no duplicate tasks,
no tasks for absent modules, and no silent deletion of adopter edits. If safe
automatic reconciliation cannot satisfy those conditions, report the conflict
and leave the adopter a clear manual action. The plan must settle how the
inventory and tasks are generated and updated, including upgrades, before
implementation; live rendering and the clean lockfile baseline must agree.

This repairs discovery and first use of existing capabilities, not the scope of
their underlying advice. In particular, the architecture-review task points to
the existing rubric and permits an appropriate legacy, new or mixed-system
choice; it does not add the v0.7 architecture-review expansion.

## Rationale

Selection-specific tasks give adopters a next action without requiring every capability to run. A local inventory gives agents and people the same starting point.

## Alternatives considered

Leave the preset seeds and source catalog as they are: explicit-list installs
and later adoptions would still lack a dependable first-use path. Requiring all
modules at every session would impose work regardless of selection or need.

## Documentation / doctrine surface

Place adopter-facing discovery and manual adoption instructions in the
installed bootstrap and module documentation; keep operational pointers in
shipped governing/session templates only where they guide invocation. The
proposal and plan remain deliberation in `dev/`. Changes to installed files,
the install manifest and engine are install-contract changes; no new doctrine
premise is proposed. Route final wording by `docs/DOCUMENTATION_PLAN.md`.

## Evidence / verification plan

The plan must inventory every mapped module, entry point, task and expected result, and search for readers and callers before mapping verification. Exercise real scaffold
entry points for preset, explicit list, empty list, add/remove, and later adoption through both documented paths. Check an installed tree's inventory and every task against
the files and commands actually shipped. Test repeated runs, completed tasks,
adopter edits, removed modules, conflicts and clean lockfile agreement; any
missing or misleading task, broken invocation, lost edit or divergent baseline
falsifies the change. Exercise upgrade plan/stage/apply as applicable, including
an edited onboarding slot and a previously installed tree.

### Tests required

Use `bootstrap/tests/test_onboarding_seed_roster.py`,
`bootstrap/tests/test_module_roster.py` and
`bootstrap/tests/test_module_merge_lockfile.py`,
`bootstrap/tests/test_upgrade_module.py` and
`bootstrap/tests/test_upgrade_module_additions.py` as starting owners, adding
behavioral coverage in the appropriate `bootstrap/tests/` homes for the real
install and upgrade entry points. The plan must name exact nodes and the module set; these files may not exhaust consumers.

### Examples / smoke checks

Use `bootstrap/scaffold.py --summary`, `--dry-run`, and `--manifest` with
representative profiles, and install in temporary directories.
Run `python scripts/check_cairn.py` and applicable claim, link, snippet and
neutrality gates for changed prose.

#### Security preflight — five questions, answered in writing

S1: The installer receives an operator-supplied profile, shipped module
mappings and templates, and existing adopter files; an adopter may edit those
files. The proposed inventory and task renderer must not treat their content as
independent authority to select a module or authorize execution.

S2: Proposed checks are not yet implemented or mutation-tested. At
implementation, remove a selected module task, insert an unselected one, alter
a preserved task and change a lockfile baseline; each corresponding test must
fail, with the runs recorded. Baseline agreement alone cannot establish that
the underlying selection is correct.

S3: The scaffold install and upgrade commands select the resolved profile and
existing target files; the plan must name the exact tests, commands and input
sets. Proposed adopter-facing claim: “The onboarding list includes a first-use
task for each selected module.” Verify that claim against both preset and
explicit-list installs; a manual copy requires the documented update step.

S4: Invalid profile, unsafe paths, conflicting edits or unresolved merge must
fail closed or ask for manual reconciliation, never gain authority to overwrite
or execute. Existing path-containment and upgrade protections remain in force.

S5: Assume an attacker can supply profile values or modify adopter files. A
malicious instruction in a legitimately selected module or an authorized edit
can still mislead a reader; the inventory does not authenticate content.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Adopters cannot locate or perform a task from the installed tree; repeat or
upgrade loses their work; optional modules are presented as mandatory; or the
maintenance cost of keeping inventory and tasks correct exceeds their use.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance — install contract, scaffold engine and
adopter-executed surfaces are in scope.
