# Find and activate installed modules

**Author**: Codex (gpt-6.1-sol)
**Status**: awaiting-decision
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


## Review -- Codex (gpt-6.1-sol) -- 2026-10-29

```
Reviewed commit: e593133bdecef4d2da35d2ee1ab2ef0df94fa059
Target: opening proposal, Context through Assurance path
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes. Discovery and a usable first task
   repair a concrete installation gap without requiring routine execution of
   every capability: onboarding currently depends on a preset, while module
   selection also supports exact lists and defaults --
   `bootstrap/_scaffold/cli.py:328`, `bootstrap/_scaffold/cli.py:563`.
2. **Best alternative.** Extend the existing onboarding slot and module
   documentation from the resolved module mappings, rather than introducing a
   parallel workflow or scanning arbitrary files for installation authority.
   The proposal permits that simpler mechanism and requires its baseline to
   agree with installation -- `bootstrap/_scaffold/config.py:1018`,
   `bootstrap/_scaffold/install.py:1122`, `templates/modules/README.md`.
3. **What would show it wrong.** A task that cannot run from an installed
   tree, a selected module without a task, or an adoption that loses completed
   work defeats the purpose. Existing public-entry tests establish an
   appropriate starting pattern, but do not yet prove the proposed behavior --
   `bootstrap/tests/test_onboarding_seed_roster.py::TestModelMappingWaitingSeed`.

The strongest version of this proposal makes capabilities useful after both
initial installation and later adoption. It does not turn an installed
capability into an obligation to execute it. The opening contract states that
boundary explicitly and includes a manual reconciliation route when preserving
adopter work prevents a safe automatic update.

**Evidence and sweep.** Claims and production-path coverage: the committed CLI
calls preset onboarding before installing the resolved modules; the existing
onboarding tests invoke the scaffold's real `main`. Design completeness and
silent failure: the proposal covers empty/exact lists, add/remove, edited and
completed tasks, repeated operations and explicit conflicts. The plan must
choose update semantics before implementation. Cross-document consistency and
drift: the source catalog is a descriptive table, while the engine's mappings
include further entries such as `incident-trackers` and `documentation-plan`;
using the mappings as the audit set avoids treating that table as exhaustive
(`templates/modules/README.md`, `bootstrap/_scaffold/config.py`). Later
adoption is real: the bootstrap describes manual copying, and the upgrade
handler records module files and lock metadata without updating onboarding
(`bootstrap/BOOTSTRAP.md:648`, `bootstrap/_scaffold/upgrade.py:1764`).
Lifecycle placement and scope: pointers belong in existing session templates,
first-use work in the existing onboarding slot, and architectural expansion
remains separately scheduled (`dev/PLANNING.md`,
`docs/DOCUMENTATION_PLAN.md`). No scientific premise changes. No finding needs
a satisfier; the proposal's verification section already names observable
failure conditions.

**Coverage / gaps**: This is an ordinary proposal review of committed text and
its cited implementation, not verification of prospective rendering or merge
behavior. No installer or upgrade probes were run. The separate Security
Review obligation remains open. Exact module/task inventory, dependency inputs,
upgrade migration and bounded verification mapping remain owed by the plan.


## Review -- Codex Security (gpt-6.1-sol) -- 2026-10-29

```
Reviewed commit: 768b123da9a17c9ba0d78183090384954c14cc70
Target: opening proposal, Context through Assurance path
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes. Discoverability and first-use tasks can improve installed capabilities without giving inventory text authority to execute commands. The proposal expressly separates selection, discovery and execution -- opening Security preflight S1 and S4; `bootstrap/_scaffold/upgrade.py:1764`.
2. **Best alternative.** Extend the existing mapped install and adoption paths with shared rendering and conservative reconciliation. Avoid a separate filesystem scanner or mandatory execution ceremony; the current renderer already shares live and clean-baseline computation -- `bootstrap/_scaffold/install.py:1133`.
3. **What would show it wrong.** An edited or completed task overwritten during repetition or adoption, or an inventory pointing outside the installed selection, defeats this contract. The proposal explicitly makes these failures disqualifying and requires public-entry coverage -- opening Evidence / verification plan; `bootstrap/tests/test_onboarding_seed_roster.py::_scaffold`.

The strongest version provides dependable automation for ordinary installs and
adoptions, while preserving a person's work and giving a concrete recovery
instruction when edits prevent safe reconciliation. The opening contract
already requires that behavior; no additional blocking requirement is needed
at the proposal stage.

**Security evidence and sweep.** The relevant inputs are the resolved profile,
shipped mappings/templates, lock metadata and existing target files. Current
adoption accepts a named module only from the mapping, preserves existing
module destinations with advisories, and records upstream bases separately
from adopter bytes (`bootstrap/_scaffold/upgrade.py:1764`). Its already-adopted
shortcut means task repair and idempotence must be designed deliberately;
merely appending code after that return would miss repeated adoption. Current
onboarding substitutes the whole slot, so reusing it unchanged would lose local
work (`bootstrap/_scaffold/install.py:1220`). These are implementation hazards
covered by the proposal's preservation and repeat-operation criteria, rather
than evidence that its promised new behavior exists today.

For fail-closed behavior, new inventory and planning writes must retain target
containment, including linked destinations and parent directories; the current
write guard states those checks (`bootstrap/_scaffold/security.py:110`).
Upgrade tests already exercise linked destinations after staging and occupied
destination collisions (`bootstrap/tests/test_upgrade_module_additions.py`).
The plan must map those risks to the new writes and their real commands.
Independent selection expectations matter: sharing the renderer prevents drift
but cannot detect a wrong module roster, as S2 already acknowledges.

Placement, scope and documentation agree: this is installation/adoption work,
not automatic module execution or expansion of architecture advice. A local
inventory cannot authenticate a hostile but valid module instruction; S5 states
that limit. No scientific result changes. There are no findings needing a
satisfier. This review adds no historical trust-root reconstruction ceremony:
the concrete risks are current input selection, target writes and edit loss.

**Coverage / gaps**: Proposal Security Review only; no prospective implementation
or security checks were executed. Exact update semantics, failure ordering,
new-write containment and adversarial public-entry tests remain for the plan
and implementation. This ACCEPT clears this proposal's Security Review
obligation, not the separately declared plan Security Review.

## Response -- Codex (gpt-6.1-sol) -- 2026-10-29

Both reviews accept with no findings. The plan must settle rendering, inventory,
upgrade migration and update semantics; map new-write containment and failure
ordering; and test repeat adoption, including the existing already-adopted
shortcut. It must inventory the engine mappings rather than assume the source
catalog is exhaustive. The Security Review clears the proposal obligation;
the separately declared plan Security Review remains owed.

## Context

Preset onboarding does not cover every resolved selection. The source catalog
is not an installed inventory; explicit module adoption updates module files
and lock metadata without adding onboarding tasks. See the opening Context.

## Proposal

Audit module mappings, selection, installed outputs, entry points and adoption.
Provide an installed, agent-discoverable inventory of actual selected modules,
purpose and usable entry points; add relevant lifecycle pointers without
requiring routine use. Commands and artifacts must resolve and explain inputs.
Give each installed module a distinct actionable first-use task in the existing
onboarding slot, naming a command or artifact and expected result, including
non-preset installs. On later adoption including `upgrade --adopt-module`,
provide the task and inventory update; document concrete manual-copy steps.
Preserve existing and completed tasks, avoid duplicates and absent-module
tasks, and never silently delete edits. Where safe reconciliation is not
possible, report the conflict and a manual action. The plan decides generation,
updates and upgrades; live rendering and clean lockfile baseline must agree.
Modules remain optional. Existing architecture advice may be used for legacy,
new or mixed systems; v0.7 expansion remains separate.

## Rationale

Selection-specific tasks and a local inventory give adopters and agents a
usable starting point without requiring execution of all capabilities.

## Alternatives considered

Preset seeds alone leave gaps; a recurring requirement to run every module
would impose work regardless of selection or need.

## Documentation / doctrine surface

Route discovery and manual adoption instructions to installed bootstrap and
module documentation, operational pointers to shipped governing/session
templates, and deliberation to `dev/` under `docs/DOCUMENTATION_PLAN.md`.
This changes the install contract and engine, not a doctrine premise.

## Evidence / verification plan

Inventory every mapped module, task, expected result and entry point; search
readers and callers. Exercise real preset, explicit, empty and add/remove
installs and both later-adoption paths. Verify every task and entry point,
repeats, completed tasks, edits, removals, conflicts, containment, upgrade and
lockfile agreement. Missing tasks, broken paths, lost edits or divergent
baselines falsify the change. Map exact nodes and consumers in the plan.

### Tests required

Start with `bootstrap/tests/test_onboarding_seed_roster.py`,
`bootstrap/tests/test_module_roster.py`,
`bootstrap/tests/test_module_merge_lockfile.py`,
`bootstrap/tests/test_upgrade_module.py`, and
`bootstrap/tests/test_upgrade_module_additions.py`; add public-entry tests.

### Examples / smoke checks

Run scaffold summary, dry-run and manifest with representative profiles, real
temporary installs, `python scripts/check_cairn.py` and applicable claim, link,
snippet and neutrality gates.

#### Security preflight — five questions, answered in writing

S1: Inputs are profile, shipped mappings and templates, and adopter files;
inventory text does not authorize selection or execution. S2: Mutations removing
a task, adding an unselected task, changing preserved work and changing the
lock baseline must fail their tests; runs are owed at implementation. Shared
rendering alone does not establish selection correctness. S3: Install and
upgrade select resolved profiles and target files; the plan names exact tests
and inputs. The first-use task claim covers selected modules; manual copy needs
the documented update. S4: Invalid profiles, unsafe paths and conflicts fail
closed or require manual reconciliation, never overwrite or execute. S5: An
attacker controlling a profile or adopter file may still supply a hostile
valid instruction; inventory does not authenticate content.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Tasks are unusable, edits lost, optional capabilities made mandatory, or
maintenance costs exceed use.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance — install contract, engine and
adopter-executed surfaces.

### Withdrawn / superseded commitments

None.
