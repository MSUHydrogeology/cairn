# Render the module inventory in upgrade review copies

**Author**: Codex (gpt-6.1-sol)
**Status**: revising
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Make the upstream upgrade review copy show the generated module inventory that an install would produce.

## Context

At commit `3fd8dab395eb0cbb46953dada9297bdfbb9daf75`, the mapped verification recorded a failure of `bootstrap/tests/test_upgrade.py::TestInitLock::test_review_pairs_leave_no_placeholder_the_install_filled` in `dev/plans/2026-10-30-upgrade-install-integrity.md`. The installed module inventory has generated entries outside Cairn slots, but `_write_stage` in `bootstrap/_scaffold/upgrade.py` renders review-only upstream text with tokens and sizing alone. The archived discovery design in `dev/plans/archive/2026-10-29-module-discovery-activation/reconciliation.md` establishes the lock's module roster as upgrade authority and preserves edited entries. The current review copy therefore presents a generated difference as if it were an upstream change.

## Proposal

For the inventory's review-only upstream copy, render the upstream template's generated block for the recorded lock module roster using the existing inventory renderer. Keep `.ours` as the actual adopter bytes, so edited entries remain visible as differences. Do not render from `.ours`, change the raw upstream ancestor, mutate the installed inventory, alter other review pairs or change application and reconciliation semantics. Retain existing refusal and containment behavior. The implementation plan must establish how a historical `--to` source and missing or malformed inventory markers are handled without falsely presenting an unrendered copy as a valid comparison.

## Rationale

A review pair should compare the installed text with what the upstream version would generate for the same recorded selection. Reusing the renderer avoids a second catalog, while rendering the upstream text independently preserves the review's ability to reveal local edits.

## Alternatives considered

Leave the discrepancy: the mapped check stays red and the pair obscures real changes. Copy the live inventory into `.theirs`: local edits disappear from the comparison. Exempt the inventory from the test: the misleading review remains.

## Documentation / doctrine surface

No governing doctrine change is proposed. Update descriptive upgrade guidance only if the implementation changes its stated review-copy behavior; the deliberation belongs here under `dev/`, following `docs/DOCUMENTATION_PLAN.md`.

## Evidence / verification plan

### Tests required

In `bootstrap/tests/test_upgrade.py`, exercise the failing node through install, migration and `upgrade --stage`; independently check the expected roster and upstream text, an empty roster, and a locally edited inventory entry that appears only in `.ours`. Cover a missing inventory and a historical source, plus malformed markers and any refusal behavior chosen in the reviewed plan. Search for all inventory and review-pair readers and map affected tests and public paths, including `bootstrap/tests/test_upgrade_module_additions.py` and `bootstrap/tests/test_module_merge_lockfile.py`; preserve their reconciliation and staged-input protections. A test that derives both expected and actual catalog solely from the same renderer is insufficient. A staged pair hiding an edit, inventing a module, changing the installed bytes, or reporting success with invalid input falsifies this proposal.

### Examples / smoke checks

Exercise `python bootstrap/scaffold.py upgrade --target <repo> --init-lock` and `--stage` against isolated installed trees. Run applicable claim, link, snippet and neutrality gates for any changed prose. The reviewed plan maps the security and engine checks; full-tree certification remains separate.

#### Security preflight — five questions

**S1.** The upstream template comes from the selected Cairn source; the lock supplies the module roster and tokens; the target supplies `.ours`. Both lock and target are adopter-controlled. The inventory is passive text and authorizes no command.

**S2.** Removing inventory rendering should make an independent roster assertion fail; replacing `.theirs` with `.ours` should make an edited-entry difference assertion fail. These proposed mutations have not yet been run; the implementation must run and record them before the claim is accepted.

**S3.** The targeted pytest node above triggers the current parity check on review pairs from a migrated tree; the additional tests will be selected by the plan's named commands. The adopter-facing description in `bootstrap/_scaffold/upgrade.py` says the pair shows what changed and `.theirs` gets install tokens and sizing; this proposal extends that description to generated inventory content.

**S4.** A missing or malformed upstream generated block must not silently become a successful misleading comparison; the reviewed plan must choose and test a refusal or an explicitly identified unavailable comparison. Existing path checks and raw ancestor handling remain in force.

**S5.** An adopter able to edit the lock or installed files can still supply misleading but syntactically valid roster or content. Rendering does not authenticate that input or execute it.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Withdraw or redesign if the historical upstream inventory cannot be rendered faithfully from the available source and roster, if preserving an edit requires changing apply behavior, or if an independent test shows an inaccurate review pair.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance


## Review -- Codex (gpt-6.1-sol) -- 2026-10-30

```
Reviewed commit: 43c2ddb93604f6bdb28e70cc6147174c3fe7208c
Target: opening proposal
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: none
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes: rendering the upstream inventory independently fixes a misleading comparison while keeping adopter edits observable; doing nothing leaves the recorded parity failure -- `bootstrap/_scaffold/upgrade.py::_write_stage` and `dev/plans/2026-10-30-upgrade-install-integrity.md`.
2. **Best alternative.** Reuse the existing generated-block renderer on upstream text, as proposed; copying the installed inventory would hide edits, and a second renderer would duplicate metadata -- `bootstrap/_scaffold/install.py::_substitute_module_inventory` and `_render_module_inventory`.
3. **What would show it wrong.** A historical source rendered with current descriptions, an omitted recorded module, or a local edit appearing in both copies defeats the comparison; independent expectations and historical-source handling are therefore essential -- `bootstrap/_scaffold/install.py::_render_module_inventory` and this proposal's Tests required and Signals the change is wrong.

The narrow repair reaches the cause. Keeping raw ancestors, installed bytes and
apply behavior unchanged avoids turning a display correction into another merge
mechanism. The public-path tests proposed here exercise install, migration and
stage rather than only the helper. The archived reconciliation design makes the
recorded lock roster authoritative, so inferring selection from live inventory
entries would be the wrong shortcut --
`dev/plans/archive/2026-10-29-module-discovery-activation/reconciliation.md`.

One implementation recommendation: make the historical-source case distinguish
historical inventory metadata from the running engine's metadata, rather than
merely passing a historical ref whose descriptions happen to match. The existing
renderer reads process-local `_MODULE_DISCOVERY`, and silently skips an unknown
name; a roster assertion should therefore account for every recorded module,
including a removed or unavailable one. The proposal already requires faithful
historical rendering or an explicit unavailable/refusal outcome, so this
specifies its test rather than adding a new outcome. A fixture with deliberately
different source descriptions and a recorded unavailable module can expose both
mistakes without introducing a general historical execution system --
`bootstrap/_scaffold/install.py::_render_module_inventory`.

Coverage: claims, entry-point coverage, edge cases, silent omission, reuse and
cross-document consistency were reasoned through against the named commit;
placement and scope stay within the existing upgrade lifecycle. No scientific
claim is involved. This is a design review, not implementation verification: no
suite or mutation was run, historical compatibility has not been demonstrated,
and the separate Security Review obligation remains open.


## Review -- Codex (gpt-6.1-sol, Security Review) -- 2026-10-30

```
Reviewed commit: 9ff42456
Target: opening proposal and usual review
Prior findings: none
Assurance path: high-assurance
```

**Tier**: Security Review
**Findings**: none
**Verdict**: ACCEPT

**Foundations**:

1. **Should this happen as framed?** Yes: an independently generated upstream comparison can expose adopter edits without gaining write authority over installed content; retaining the present mismatch makes that comparison misleading -- `bootstrap/_scaffold/upgrade.py::_write_stage` and this proposal's Proposal.
2. **Best alternative.** Reuse rendering on clean upstream text with explicit source and membership validation; copying adopter text hides edits, while executing a historical engine would introduce executable trust solely for a passive display -- `bootstrap/_scaffold/install.py::_substitute_module_inventory` and `_render_module_inventory`.
3. **What would show it wrong.** A successful comparison that silently omits an unknown recorded module, uses current metadata for a different historical source, or carries an adopter edit into both sides defeats the stated boundary -- `bootstrap/_scaffold/install.py::_render_module_inventory`, `bootstrap/_scaffold/upgrade.py::_check_lockfile_paths`, and this proposal's Tests required.

The proposal keeps the right separation: the lock supplies selection, the
selected upstream source supplies the template, and the target supplies only
`.ours`. The inventory authorizes no command. Existing containment checks precede
staged destination writes, and review-only pairs remain outside applied files;
this design expressly preserves both boundaries --
`bootstrap/_scaffold/upgrade.py::_write_stage`.

For the plan, make three details explicit. First, the existing lock validator
accepts printable names rather than proving catalog membership, and the renderer
silently skips unknown names. Account independently for every recorded member;
never turn an unavailable member into an apparently complete empty catalog.
Second, the shared reconciler preserves selected edited blocks by design. Feed it
clean upstream bytes, never adopter text, and establish how upstream pre-existing
entries, duplicate or nested markers, and unmatched closing markers are treated.
A malformed block must reach the proposal's explicit unavailable/refusal outcome,
not a plausible partial comparison. These are specifications of the proposed
correctness condition -- `bootstrap/_scaffold/upgrade.py::_check_lockfile_paths`
and `bootstrap/_scaffold/install.py::_reconcile_generated_blocks`.

Third, distinguish historical metadata deliberately in the historical-source
fixture. Choosing a past ref with unchanged descriptions cannot expose accidental
use of process-local `_MODULE_DISCOVERY`. Test refusal/unavailable behavior
through `upgrade --stage`, including the state left behind after failure, and
prove installed content and raw ancestors unchanged. Record the proposed
rendering-removal and `.ours` substitution mutations with independent expected
rosters; they are future evidence, not evidence already supplied -- this
proposal's S2, S4 and Tests required.

Coverage: claims, production entry points, completeness, silent failure, reuse,
drift, placement and scope were reasoned through against the named commit and
cited functions. No scientific claim is touched. No implementation, malicious
fixture, mutation, suite, live-ref operation or historical-source rendering was
executed; containment and failure cleanup remain implementation and plan-review
obligations. This pass clears the proposal Security Review obligation, not the
separately declared plan Security Review.
