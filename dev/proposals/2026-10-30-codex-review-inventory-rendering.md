# Render the module inventory in upgrade review copies

**Author**: Codex (gpt-6.1-sol)
**Status**: awaiting-review
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
