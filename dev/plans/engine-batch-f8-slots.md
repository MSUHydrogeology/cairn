# Plan: Engine batch, the install report by profile and the slots an upgrade adds

**Source proposal**: [dev/proposals/archive/2026-10-26-claude-engine-batch-f8-slots.md](../proposals/archive/2026-10-26-claude-engine-batch-f8-slots.md)
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-26
**In brief**: The install report moves the slots of modules a profile did not install to their own list (2 of 22 on `solo-greenfield`), and `upgrade --plan` and `--stage` name the slots an upgrade adds, with every printed `detail` made terminal-safe.

The Internal Security Review is a separate pass from the ordinary plan review. The ordinary pass never clears it (`AGENTS.md` > Review). It clears only through its own `## Plan review` pass whose `**Obligation**` line names it.

## Source proposal

The Decision (2026-10-26) accepts the proposal as revised. Q2 takes option (a): the two slots the install fills itself stay in the count. Q1, Q3 and Q4 take their defaults: the absent-module slots are listed separately; added slots are named at `--plan` and `--stage` only; the supplier table stays local to `print_report`. The Revision is the contract; this plan does not restate its argument.

## Scope

**In.** The four engine symbols the Revision names, in `bootstrap/_scaffold/`: `print_report` (`install.py:1603`), `main` (`cli.py:189`; the call at `:627`), `merge_file` (`merge.py:173`) and `_print_upgrade_report` (`upgrade.py:846`). Two new test files. `docs/quickstart.md:298`, `bootstrap/UPGRADE.md` (the `--plan` bullet) and `CHANGELOG.md` (`## Unreleased`).
**Out.** `--apply` naming (Q3); reading installed files back (Q2 options b and c); a base-copy hash check (the proposal's SR6, a board matter); `dev/PLANNING.md`, which is edited only at its serialization points; `bootstrap/BOOTSTRAP.md`; the fidelity manifest.

**Rules the code must keep (from the Revision and the Security Review):**
* No new top-level name, and no top-level import added or changed in `install.py`, `cli.py`, `merge.py` or `upgrade.py`. The AST gate does not see imports, so the code reviewer reads the diff. `parse_slots` and `SlotError` are already in `merge.py`.
* `merge_file` reads names from its own `base_raw` and `theirs_raw` arguments and the adopter's file, never from the token-filled copies (`merge.py:194-195`). Both new parses sit in one `try` that catches `SlotError` and nothing wider, as `_transplant_slots` does (`merge.py:129`). Names fill `detail` only on `clean` and `conflict`.
* At most 10 names per file, each cut to 80 characters (a longer one ends in `...`), then `(and N more)`. Both numbers are literals inside `merge_file`; `merge_file` returns the names unescaped.
* `_print_upgrade_report` prints every `detail` through `ascii(text)[1:-1]`: the `[flag]` line (`upgrade.py:889`), the review-only line (`:899`) and the new `[new slot]` line.
* `print_report` gains one keyword `modules`, only tests membership in it, and prints module names from its own table, never from the profile's list. The table lists the seven slots in the Revision's table, including `documentation-tier-home` in both files, and carries a comment naming the `model-selection` disagreement (`BOOTSTRAP.md:418-420` against `templates/modules/team-gated/model-selection.md:10-13`).

**Reuse.** The `ascii(x)[1:-1]` form already exists inline (`install.py:604`, `lockfile.py:605`; `upgrade.py:177` cuts then escapes). A shared helper would be a new top-level name, so each site uses the form inline. Searched: `grep -rn "ascii(" bootstrap/_scaffold/*.py`. The module-to-slot facts live only in `bootstrap/BOOTSTRAP.md` prose and the template placeholders (`grep -rn "coordination-additions" bootstrap/` outside tests finds `BOOTSTRAP.md` and `fidelity-check.md`), so there is no table to reuse.

### Documentation / doctrine surface

<!-- cairn:slot documentation-tier-home -->
**Doc tier home rule** — route doc and doctrine changes by layer per
[`docs/DOCUMENTATION_PLAN.md`](../../docs/DOCUMENTATION_PLAN.md):
cross-cutting prescription → governing layer (`AGENTS.md`);
deliberation about what to build → deliberation layer (`dev/`);
description of the software as it is → descriptive layer (`docs/`). A
plan's *Scope* must name the doctrine-surface touched (or an explicit
"no doctrine surface").
<!-- cairn:end documentation-tier-home -->

Descriptive layer only (`docs/quickstart.md`, `bootstrap/UPGRADE.md`) plus `CHANGELOG.md`. No `doctrine/` file and no `AGENTS.md`.

Proposed paths:
* `bootstrap/tests/test_install_report_slots.py`
* `bootstrap/tests/test_upgrade_added_slots.py`

## Sequence

**Gate: implementation waits for the code review of the LP-SR-1 to 8 repair to close** (commits `1cf56d4a`, `9af86ae4`, `9b607bc8`), because it changed `upgrade.py` and `lockfile.py` and a finding there can change them again. When it closes, the implementer re-reads `upgrade.py` and `merge.py` and re-checks every line cite below before the first edit. They were verified at `f8800485` and `upgrade.py` already moved about 30 lines against the proposal's cites. The plan's own review does not wait.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **F8: the install report by profile.** Tests first, shown failing on unchanged code; then the table and second list in `print_report`; `main` passes `modules=`; `docs/quickstart.md` count 22 to 20 in the same commit, because the frozen quickstart test compares the prose to the live report | Gate line above | `install.py`, `cli.py`, `docs/quickstart.md`, `test_install_report_slots.py` |
| C2 | **#8: name added slots, escape `detail`.** Tests first, shown failing; then `merge_file` names (SR1, SR2) and `_print_upgrade_report` escape and `[new slot]` line (SR3) | C1 done | `merge.py`, `upgrade.py`, `test_upgrade_added_slots.py` |
| C3 | **Prose.** One sentence in the `--plan` bullet of `UPGRADE.md`, naming the cases not covered; the `CHANGELOG.md` entry (it names the escape on the old `[flag]` lines); lockfile check | C2 done | `UPGRADE.md`, `CHANGELOG.md` |
| C4 | **Boundary B record**: append `## Implementation verification -- <agent> -- <date>` against a clean committed tree; then status `awaiting-code-review` | C3 done | the record |
| C5 | **MAINTAINER-ONLY: the AST attestation re-anchor, then the gate-manifest re-anchor.** Not scheduled for an agent. The 0.5 cut folds one re-anchor (`dev/PLANNING.md` "### 0.5", "One re-anchor, at the cut", and the Queued re-anchor row). When work reaches it, write `**Waiting on Maintainer**: AST and gate re-anchor` in the header | Maintainer, at the cut, by `bootstrap/AST_BASELINE_RUNBOOK.md` then `bootstrap/REANCHOR_RUNBOOK.md` | `scaffold_ast_baseline.json` and the manifest fixture |

C1 and C2 each land as two commits (tests, then code) so the control run is a commit. The code reviewer reads from the tests' commit.

**Frozen files, derived** from `bootstrap/tests/fixtures/gate_manifest.json` (`frozen_files`, 195 keys) with a membership check on each path. **Frozen**: `bootstrap/scaffold.py`, `bootstrap/verify_integrity.py`, `scaffold_ast_known_new.json`, and every existing `bootstrap/tests/**/*.py`, including `test_quickstart_sequence.py`, `test_upgrade.py`, `test_install_module.py` and `test_ast_attest.py`. **Not frozen, and edited here**: `install.py`, `cli.py`, `merge.py`, `upgrade.py`, `docs/quickstart.md`, `bootstrap/UPGRADE.md`, `CHANGELOG.md`. **Chunks that add only new test files**: C1 and C2. No chunk edits a frozen file. If a frozen test fails because of this change (for example one that pins non-ASCII text on a `[flag]` line), the implementer stops and asks the Maintainer: editing it owes the gate-manifest ceremony and is a deviation.

## Acceptance criteria

Test names say the property. "New" tests are in the two new files; each goes through the real entry point (`scaffold.py`, `scaffold.py upgrade --plan|--stage`) unless stated. Every new test is first run on the unchanged code and recorded failing (its control), except the ones that pin today's behavior and pass both before and after: marked "pins".

**C1: install report.**
1. `test_minimal_profile_lists_absent_module_slots_separately`: on `solo-greenfield`, `coordination-additions` and `role-roster-additions` are under `Slots for modules this profile did not install (2):` and not in the main list; the main heading reads 20 and equals its line count; the two lists total 22.
2. `test_team_profile_keeps_live_module_slots_in_main_list`: on `collaborative-team`, the main heading reads 23 and no second list prints.
3. `test_report_without_modules_argument_lists_every_slot_in_main_list` (calls `print_report` directly, the one exception): absent `modules`, no second list.
4. `test_removing_a_module_moves_every_slot_it_fills`: a profile that removes `documentation-plan`, `claim-check`, `reflections` and `security-verification` moves their slots, `documentation-tier-home` in both files included, to the second list. `test_a_slot_with_any_installed_supplier_stays_in_main_list`: with one of the five `role-roster-additions` suppliers installed, that slot stays in the main list. This is the mutation test for "no supplier installed" against "not every supplier installed".
5. `test_every_slot_that_says_filled_from_a_module_is_in_the_supplier_table`: scans the core templates for the phrase `Filled from the` and fails on a slot the table lacks. It reads the templates, not the table. `test_supplier_table_names_real_slots_and_real_modules`: with `modules=[]` every table slot is in the second list; each exists in a core template and each printed module is a shipped module under `templates/modules/`. Neither can see a supplier whose placeholder lacks the phrase (`coordination-additions`, `role-roster-additions`), so those two stay hand-listed. The Revision says so.
6. `test_hostile_module_name_in_profile_prints_no_escape_byte_in_the_report`: a profile whose exact `modules:` list holds a name with an ESC byte. The assertion covers the report section only (from the `Cairn scaffold complete` banner). The older raw print of unknown module names at `install.py:1526` is on the board's security row and is not this plan's.
7. The existing `test_quickstart_sequence.py::TestLayerAStepsOneThroughThree::test_step3_install_writes_expected_kernel_and_modules` (lines 240-250) is not edited; it compares `**N unfilled block slots**` in `docs/quickstart.md:298` with the live count, so it passes after the edit to **20 unfilled block slots**, with the sentence format unchanged, and one clause says the report lists the other slots separately. It must pass: `python -m pytest bootstrap/tests/test_quickstart_sequence.py`.
8. `scaffold.py --manifest`, captured before the first edit and after C3, is byte-identical (`cmp`). `git diff` of `bootstrap/_scaffold/SECURITY_MUTATIONS.md` is empty (no new write).

**C2: added slots.**
1. `test_plan_and_stage_name_a_slot_the_upgrade_adds`: a slot added to `templates/core/dev/README.md` in a second copy of the tree prints `[new slot] dev/README.md: ...` under both flags. `test_file_without_added_slot_prints_no_new_slot_line` and `test_new_core_file_names_no_slot` pin today's silence.
2. `test_slot_the_adopter_deleted_is_not_named` and `test_slot_the_adopter_already_has_is_not_named`. Mutants (S2): drop the old-base subtraction, or subtract only the adopter's names; the first test fails each.
3. `test_detail_is_empty_or_exactly_the_name_list_on_clean_and_conflict` (through `merge_file`); `test_needs_value_slot_removed_and_error_carry_no_names`.
4. `test_lockfile_token_value_carrying_a_slot_pair_adds_no_name` (SR1, through `upgrade --plan`): a token value with a slot pair, used only in the new template, gives no `[new slot]` line. Mutant: parse the token-filled text; this test must fail it.
5. `test_new_slot_line_stays_within_its_bound` (SR2): a template with one 1 MB slot name, and one with 1,000 new slots; each `[new slot]` line is under 1,200 characters for ASCII names (8,300 worst case) and states `(and N more)`.
6. `test_every_flag_and_new_slot_line_is_printable_ascii` (SR3): an adopter file with a filled slot whose name holds an ESC byte, removed upstream. Control: fails on today's code (the Security Review measured the raw print). The same test covers `malformed slots: {exc}` at `upgrade.py:546`. **The set of `detail` print sites is listed from the tree** (`grep -n "\.detail" bootstrap/_scaffold/*.py`: `:889`, `:899`, plus the new line) **and the escape is removed at each in a separate copy; each removal must fail a test.** The review-only site prints fixed text today (`upgrade.py:544`, `:557`), so no real run reaches it with a hostile byte: its test calls `_print_upgrade_report` directly with a `FilePlan` whose `detail` holds an ESC. The second direct call in the plan.
7. `test_malformed_old_base_keeps_its_status_and_prints_no_name` (pins the status; today `conflict`), `test_tree_without_base_copy_names_nothing` (`review-only`), `test_renamed_filled_slot_stays_slot_removed_and_names_no_new_slot`.
8. The `except` added in `merge.py` names `SlotError` only; `git diff` over the four files adds no `import` line. The sorted `note: NEW Import:` lines of `_ast_attest.py verify` are identical before and after.
9. `test_security_leaf.py` passes unchanged. `scaffold.py --manifest` is byte-identical.

**C3: prose.**
1. The `UPGRADE.md` sentence says plan and stage name slots an upgrade adds, and not for a file new in the upgrade, a tree with no base copy, or a renamed filled slot (B.5 of the Revision). Commands: `python -m pytest bootstrap/tests/test_verify_integrity.py bootstrap/tests/test_review_stance_in_shipped_files.py`; `python scripts/claim_check.py`, `python scripts/check_cairn.py` and `python scripts/link_check.py` on each changed Markdown file.
2. `CHANGELOG.md` `## Unreleased` has one entry naming both changes and the escape on the old `[flag]` lines, with a link to this plan.
3. **Lockfile.** None of the edited files is a `dst` in `dev/.cairn/cairn-lock.yml` (checked 2026-10-26: `grep '"dst"' dev/.cairn/cairn-lock.yml | grep -i "quickstart\|UPGRADE\|CHANGELOG\|_scaffold"` finds nothing). If an edited file is tracked when this runs, run `python bootstrap/scaffold.py upgrade --target . --finalize <path>` for it, scoped, and commit the lockfile.

**C4/C5.** C4's record carries the fields the template names. C5 is the Maintainer's: derive the changed set from the final tree with the runbook's Step 1 and compare it with this plan's four symbols, taken as the difference from the set LP-SR left (S0, recorded in C1 before the first edit under Python 3.13.x). Expected: four CHANGED, none NEW, no changed import note. More than four means something else moved, and the proposal's accounting is wrong.

## Scope delta

**Scope delta**: degraded, as the Decision set it. Reduced against the archived Decision's wide wording ("a post-install report that asks only for live work"), preserved against the board row. The report still lists the two slots the install fills itself.
* The second form of Q2 option (c) (print the report after the module-merge pass and drop the slots it fills) is not built. **disposition**: defer. Home: a `dev/PLANNING.md` row, written at this plan's archive commit (a serialization point). Authorization, the Maintainer's answer to the Decision: "Accept, leave 2 slots counted (Recommended)".

## Verification

**Boundary A (iteration, scoped).** Per chunk, the tests that own each touched surface (found by `grep -ln` over `bootstrap/tests` for `print_report`, `merge_file`, `MergeResult`, `_print_upgrade_report`, `[flag]`, `review-only`, `Block slots requiring`):
* C1: the new `test_install_report_slots.py`, `test_install_module.py`, `test_first_session_report.py`, `test_quickstart_sequence.py`, `test_security_leaf.py`.
* C2: the new `test_upgrade_added_slots.py`, `test_upgrade.py::TestMerge`, `test_merge_module.py`, `test_slotmerge_leaf.py`, `test_upgrade_module.py`, `test_upgrade_module_additions.py`, `test_skills_upgrade.py`, `test_upgrade_lockfile_path_containment.py`, `test_upgrade_refuses_hostile_project_data.py`, `test_upgrade_side_door_parity.py`, `test_drift_surfacing.py`, `test_fork_advisory.py`, `test_security_leaf.py`.
* C3: the two `UPGRADE.md` readers, `test_quickstart_sequence.py`.
* Every chunk: the Bandit gate (`test_security_lint.py`; it skips when Bandit is missing, so the record states the skip) and `python scripts/quality_gate.py --sub neutrality --sub redundancy`.
* `test_ast_attest.py` fails until C5; expected, and recorded as a non-pass with that disposition.

**Boundary B mode: `full`.** The scaffold engine is a named high-risk surface and `AGENTS.md` sends any high-risk surface to the full mode (it also sits beside the install contract, `scaffold.py --manifest`), so bounded mode refuses. The change's own record is scoped (the Boundary A sets above, the standing gates, the plan-specific commands) with `**Certified by**: pending`. The full suite is the next certifying run, before a push, the re-anchor or a release. **Nobody sets `CAIRN_FULL_SUITE` for this implementation.** Interpreter: Python 3.13.x; digests differ under 3.12.

Plan-specific commands the record lists: the two new test files; `scaffold.py --manifest` byte compare; the read-only AST `verify` before and after (S0 and S1); the smoke checks (install `solo-greenfield` into a scratch folder and compare both lists with `verify_integrity --target`; repeat the proposal's upgrade reproduction on the built code).

**Boundary C: what the code reviewer attacks.** Not a re-run of Boundary B.
* The `except` clause in `merge_file`: `SlotError` only. A malformed old base must not change a status.
* Token injection: parse the token-filled text in a separate copy; test 4 must fail.
* Each `detail` print site without its escape (test 6), and the cap literals (test 5).
* A hostile name from the profile in either report list (test 6 of C1). The supplier table against `bootstrap/BOOTSTRAP.md:418-427` and the template placeholders: a slot printed in the second list that an installed module fills; a slot of an absent module left in the main list.
* The import diff across the four files, and the AST set (S0 against S1).
* That no `[new slot]` line appears for `new-core`, `needs-value`, `slot-removed`, `review-only` or `error`.
* A recorded `Bounding` verdict is not needed (Boundary B is `full`).

**One code-review loop.** One code review, then the implementer's answer, then archive. There is no second Security Review for implementation unless a finding changes the design. The Internal Security Review above is the plan-stage one and does not repeat at code review.

## Dispositions

Filled at archive-preparation. The one item carried is the `defer` in Scope delta.
