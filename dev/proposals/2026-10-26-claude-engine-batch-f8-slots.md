# Engine batch: a post-install report that matches the profile, and an upgrade that names the slots it adds

**Author**: Claude (Strategy)
**Status**: awaiting-review
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review) — the plan edits `bootstrap/_scaffold/`, a named high-risk surface
**Opened**: 2026-10-26
**In brief**: A minimal install stops mixing slots for modules it did not install into the list of work it owes, and `upgrade` says which slots it adds, so a half-filled project does not lose a new one among the old.

**Authoring tier.** I wrote this at the medium tier, although doctrine sets proposal authoring at high. The Maintainer directed: "Go ahead and spawn the lowest-tier agents you can to design, review, and implement proposals toward 0.5". That holds for this proposal only. The Security Review stays at the high tier.

**Maintainer's words, 2026-10-26** (the 0.5 board row, `dev/PLANNING.md:44`):

> "Engine batch is in"

## Context

Two changes the board has queued for 0.5, both in the scaffold engine (`bootstrap/scaffold.py` -> `bootstrap/_scaffold/`). A change there needs a proposal, a Security Review, and an AST attestation re-anchor (`AGENTS.md`, "High-risk surfaces" and "Operational pitfalls"). Batching pays each once.

**F8: the post-install report.** The archived proposal `adopter-path-consolidation` deferred it. The Maintainer's Decision on its Revision 2 reads: "Accept Revision 2 as written. Defer the install-report fix (F8) to the board. No second review round; External floor waived." (`dev/proposals/archive/2026-08-20-claude-adopter-path-consolidation.md:1548`). The report lists every block slot in every file it wrote. It does not look at which modules the profile installed.

I ran `bootstrap/scaffold.py --config bootstrap/profiles/solo-greenfield.yml` into a scratch directory outside the repository (Python 3.12.9; the report does not depend on the interpreter). The report prints `Block slots requiring agent attention (22)`. Two of the 22 are for modules the profile did not install:

| Slot | File | Filled from | Installed? |
|---|---|---|---|
| `coordination-additions` | `dev/agent_collaboration.md` | `coordination-tiers` | no |
| `role-roster-additions` | `dev/agent_collaboration.md` | `domain-agents`, `legacy-agent`, `security-review`, `issue-capture`, `model-selection` | none of the five |

`bootstrap/BOOTSTRAP.md:418-431` names the module behind each of these slots and says to mark the slot `N/A: <module> not installed` when the module is absent. The report does not say that, so a new adopter reads all 22 as work. The `collaborative-team` profile installs `coordination-tiers` and `model-selection`; there the same two slots are live, and the report prints 23.

I also compared the report with the files on disk. `bootstrap/verify_integrity.py --target <scratch>` reports `slots checked 22, listed 20`. The 22-versus-20 gap is two slots the install itself fills after the report is built: `onboarding-tasks` (`dev/PLANNING.md`, filled by the onboarding step) and `security-verification` (`AGENTS.md`, filled by the module-merge pass, which runs after the report; the run printed `[inserted] AGENTS.md > security-verification`). This proposal does not fix those two (see Questions, Q2).

`docs/quickstart.md:298` says "**22 unfilled block slots**", and `bootstrap/tests/test_quickstart_sequence.py:240-250` fails if that number differs from the one the scaffold prints.

**#8, engine half.** GitHub issue #8 is closed. The integrity command's slot note shipped in v0.4.0. It lists every slot that still holds Cairn's text. `upgrade` does not say which slots an upgrade added. The Decision deferred that: "`upgrade` does not name the slots it adds in this change. That rides with the next engine change to the upgrade path that already owes a re-anchor, or sooner if an adopter misses an upgrade-added slot" (`dev/plans/archive/neutrality-and-upgrade-slots.md:32`; board row at `dev/PLANNING.md:222`). This is the next such engine change.

Reproduction (two copies of this tree outside the repository; the second has one slot added to `templates/core/dev/README.md`). I installed `solo-greenfield` from the first, then ran `upgrade --plan`, `--stage` and `--apply` from the second.

* `--plan` prints `dev/README.md` under `clean (untouched)` and says nothing about the new slot `example-added-slot`. `--stage` and `--apply` also say nothing.
* `verify_integrity` then lists `example-added-slot` among 21 slots on this unfilled install. On an install where the adopter had filled most slots it would stand with only the few left, which is the case the Decision named. On a fully filled install it would be the only one.

I measured both results. The trees are in the session scratch directory.

## Proposal

Both changes print more precisely. Neither writes a file, reads a new path, or changes the lockfile.

**A. Group the install report by profile** (`print_report`, `bootstrap/_scaffold/install.py:1603`; call site `bootstrap/_scaffold/cli.py:627`).

1. `print_report` gains one keyword parameter, `modules` (the installed module names, which `main` already holds). Absent, it behaves as today.
2. Inside `print_report`, a small local table names the module behind each slot whose content is filled from modules: `claim-check`, `reflections`, `documentation-discipline` (from `documentation-plan`), `security-verification`, `coordination-additions`, `role-roster-additions`. The source is `bootstrap/BOOTSTRAP.md:418-427` and the placeholder text in `templates/core/AGENTS.md:405` and `templates/core/dev/agent_collaboration.md:342`.
3. A slot in the table whose modules are all absent leaves the main list and goes into a second list, printed after it: `Slots for modules this profile did not install (N):`, each with its module names, then one line: "Mark each `N/A: <reason>` (for example `N/A: coordination-tiers not installed`), or fill it yourself if your project needs it." Nothing is dropped; the main heading and its count keep their text and now count only the live slots (20 on `solo-greenfield`).
4. Any slot not in the table, or whose module is installed, stays in the main list.

**B. Name the slots an upgrade adds** (`merge_file`, `bootstrap/_scaffold/merge.py:173`; `_print_upgrade_report`, `bootstrap/_scaffold/upgrade.py:815`).

1. `merge_file` already parses the new template's slots (`merge.py:202`) and the adopter's (`merge.py:201`). It additionally parses the old base template's slots. An added slot is one in the new template and in neither the old base nor the adopter's file.
2. It returns the added names, escaped with `ascii()`, in the `detail` field `MergeResult` already has (`merge.py:235` returns `""` there today). `detail` is only ever printed (`upgrade.py:565`, `858`, `868`); no other code reads it.
3. `_print_upgrade_report` prints one line per such file, for plan and stage: `[new slot] dev/README.md: 'example-added-slot' -- new in this upgrade. Fill it, or write N/A: <reason>.` Only the kinds `clean`, `clean-locally-modified` and `conflict` print it.
4. If the old base template does not parse, no names are printed. That is today's behavior.

**What I add, and what I did not.** No option, flag, new file, new function, new top-level name, lockfile field or manifest field. A new top-level engine name would fail the AST check (see Install contract) and need a frozen file edited. I measured that: a probe constant added to a scratch copy of `merge.py` made `_ast_attest.py verify --known-new` exit 1 with "not in the pinned known-new manifest". So the table is local to `print_report` and the name list is built inside `merge_file`.

**Separate trigger, kept as it is.** The board keeps the watch for adopters who fill slots by reflex with `<!-- cairn:customized -->` (`dev/PLANNING.md:222`; archived plan `neutrality-and-upgrade-slots.md:553`): revisit if an adopter reports it. This proposal builds no mechanism for it. The new line's wording copies the slot note's: write the content or `N/A: <reason>`, and keep Cairn's text on purpose only deliberately (`bootstrap/verify_integrity.py:320-322`).

## Rationale

F8 matters because the first screen an adopter sees after install should not ask for work the profile does not need. This change moves two of 22 slots, so it does not make the list short. I say so because a reader of "match the selected profile" could expect more. What it delivers is the part the profile can decide: which slots have a module behind them.

#8's gap is real but narrow. On a partly filled tree the existing note buries a new slot among old ones (17 listed in the archived plan's measurement). `upgrade` is the one step that knows the slot is new, because it has the old and new template side by side.

## Alternatives considered

* **Do nothing.** F8 stays: the quickstart prints a count the profile does not justify, and a minimal install is told to fill `coordination-additions`. #8 stays: a new slot on a partly filled tree is found only by reading the full note. Cost: low and continuing; both were already deferred once, and the Maintainer put them in 0.5.
* **Split into two proposals.** Two Security Reviews and two AST re-anchors, for two changes that touch different files (`install.py`, `cli.py` against `merge.py`, `upgrade.py`). It loses on cost. The two share one rule (name what is new, escape what comes from the tree), so one review reads them together. The batch is the Maintainer's call ("Engine batch is in").
* **Template-only F8: wrap the two slots in `cairn:if`.** The engine already strips regions by profile axis (`strip_conditional_regions`, `bootstrap/_scaffold/config.py:1459`; used at `templates/core/AGENTS.md:494`). That needs no engine change and no Security Review, so it is the strongest rival. It loses on three points. (1) It keys on axes, not on installed modules. A profile can list `modules:` itself, and `upgrade --adopt-module` adds a module later; either leaves a module whose merge target the install stripped. (2) `role-roster-additions` has five suppliers selected by different axes. (3) It edits two core templates every adopter has, so every adopter's next upgrade merges the change.
* **Read the supplier from each module file** (a `cairn:merge-target` line or an `Adds to:` parse). Only `security-verification` carries a `cairn:merge-target` directive today (`templates/modules/default-on/security-verification.md:193`); the others say "Adds to:" in prose. Doing it means editing six or more module files and parsing them. The table needs neither and cannot be made to read a hostile file.
* **Also fix the two slots the install fills itself** (`onboarding-tasks`, `security-verification`). That makes the report read the installed files back, a new read of the adopter's tree in a function that only prints. I left it out (Q2).
* **Also print added slots at `--apply`.** `--apply` applies a staged result and has no old/new pair in hand; it would recompute. Adopters decide at `--plan` and `--stage`. Left out (Q3).

## What is lost

* The report's first count falls from 22 to 20 on `solo-greenfield`. Anyone who scripted against "22" meets 20. The only repository consumer is the quickstart prose and its test, which I edit.
* The table can drift: a module that starts filling a slot but is not in the table would, if absent, have its slot printed in the main list as today. Drift fails toward more work shown, never less.
* The two slots the install fills itself remain in the count, so the quickstart's "unfilled" is still two too high. It was two too high before.
* Added-slot naming has the existing gap for a file new in the upgrade (`new-core`): its slots are not named. The file is announced as new, and the slot note lists its slots as before.

## Documentation / doctrine surface

Descriptive and prose layer only; no `doctrine/` file, no `AGENTS.md`. Routing per `docs/DOCUMENTATION_PLAN.md`.

* `docs/quickstart.md:298`: "22" becomes the new count, and one clause says the report lists the other slots separately. The test at `test_quickstart_sequence.py:240-250` pins the number, so the edit and the engine change land together.
* `bootstrap/UPGRADE.md`: one sentence in the `--plan` bullet (`UPGRADE.md:107-110`) saying plan and stage name slots the upgrade adds. Two tests read this file (`test_verify_integrity.py:1439` and `test_review_stance_in_shipped_files.py:1315`); the implementer runs them.
* `CHANGELOG.md`, `## Unreleased`: one entry, as the 0.5 board prescribes.
* Not edited: `bootstrap/BOOTSTRAP.md` (its gate-table is a triage trigger and its II-4 text is already right), the fidelity manifest, `dev/PLANNING.md` (a shared file, edited at its serialization points).

## Install contract and upgrade impact

* **Adopters who already installed.** Nothing on disk changes. At their next `upgrade --plan` or `--stage`, a file where Cairn added a slot gets one extra line. Their lockfile, base cache and files are written as before.
* **Lockfile schema, fidelity manifest, gate manifest, `scaffold.py --manifest`: unchanged.** `print_report` is called once (`cli.py:627`) and writes to stdout only; `install_manifest` and `format_manifest` do not call it (`grep` over `bootstrap`, `scripts`, `tools`, `docs` and `templates` finds `print_report` only in `install.py`, `cli.py`, `__init__.py`, `test_install_module.py` and the AST baseline). `merge_file` returns the same four-kind status; only `detail` for kinds that left it empty is now filled. The implementer re-verifies by running `scaffold.py --manifest` before and after and comparing bytes.
* **AST re-anchor: Maintainer-run, four changed symbols, none new.** The allowlist for self-service repair is four names (`bootstrap/tests/_ast_attest.py:143-148`: `_MODULE_MAPPINGS`, `_SKILLS_MAPPINGS`, `_CORE_MAPPINGS`, `install_onboarding`). The symbols this change touches are `print_report` (`install.py`), `main` (`cli.py`), `merge_file` (`merge.py`) and `_print_upgrade_report` (`upgrade.py`). None is on the allowlist, so by `bootstrap/AST_BASELINE_RUNBOOK.md` the correction is a Maintainer-run, dry-run-verified direct correction that an implementing agent does not perform. This list is derived by reading the proposal against the code, not measured, so the implementer re-derives the changed set from the final tree (runbook Step 1). I ran that derivation on the current tree under Python 3.13.5: 0 changed, 0 missing, 0 duplicate, 98 new (all allowed), so the baseline is clean now and the delta will be this change's alone. Under the shell's default Python 3.12.9 the same command reports 132 changed, because digests depend on the interpreter. The canonical interpreter is 3.13.x.
* **Frozen files: none edited.** Nearly every file under `bootstrap/tests/` is frozen (`bootstrap/tests/fixtures/gate_manifest.json`, `frozen_files`: 195 entries, including `test_upgrade.py`, `test_install_module.py`, `test_quickstart_sequence.py` and `scaffold_ast_known_new.json`). Editing one owes the gate-manifest ceremony. So the new tests go in two new files, which the gate manifest allows as additions.

Proposed paths:
* `bootstrap/tests/test_install_report_slots.py`
* `bootstrap/tests/test_upgrade_added_slots.py`

## Evidence / verification plan

I have not built this. The reproductions above are measured; the claims about the result are expected.

### Tests required

The plan maps these; unknown scope falls back to the full suite. Each goes through the real entry point.

* **F8, `bootstrap/tests/test_install_report_slots.py` (new).** Run `scaffold.py` on `solo-greenfield` and on `collaborative-team`. Assert: on solo, `coordination-additions` and `role-roster-additions` are in the second list and not the main one, the main count equals the number of main-list lines, and the totals of both lists equal 22; on collaborative-team both are in the main list and the second list is absent; a call with `modules` omitted lists every slot in the main list. A drift test: every slot name in the table exists in a core template, and every module name in it is a shipped module.
* **#8, `bootstrap/tests/test_upgrade_added_slots.py` (new).** Through `merge_file` and through `upgrade --plan` and `--stage` on an installed scratch tree: a new slot is named; a slot the adopter deleted (in the old base, absent from the adopter's file, present upstream) is not; a slot the adopter already has is not; a slot named with an escape byte prints escaped; a malformed old base prints no names and leaves the status unchanged; a file with no added slot prints no `[new slot]` line.
* **Owning tests found by searching what reads the touched code** (run for Boundary A): `test_upgrade.py::TestMerge`, `test_merge_module.py`, `test_install_module.py`, `test_first_session_report.py`, `test_quickstart_sequence.py`, `test_upgrade_module.py`, `test_upgrade_module_additions.py`, `test_verify_integrity.py` and `test_review_stance_in_shipped_files.py` (both read `UPGRADE.md`), and `test_security_leaf.py` (it AST-scans the engine for guard calls). `test_ast_attest.py` fails until the re-anchor; that is expected and Maintainer-run.

### Examples / smoke checks

* `python bootstrap/scaffold.py --config bootstrap/profiles/solo-greenfield.yml --target <scratch>`, then compare the two lists with `python bootstrap/verify_integrity.py --target <scratch>` (every slot in the main list is listed there as still holding Cairn's text, except the two the install fills).
* The upgrade reproduction above, repeated on the built code.
* `python scaffold.py --manifest` before and after, byte-compared.
* `python scripts/claim_check.py` and `python scripts/check_cairn.py` on every changed Markdown file. They are run by a person; Cairn has no CI.

### Verification boundaries (`AGENTS.md`, "Verification boundaries")

* **Boundary A (iteration):** the tests above, plus the standing gates for each touched surface: the Bandit gate (`test_security_lint.py`, a test; it skips when Bandit is missing, and `python bootstrap/security_check.py` is the Maintainer-run release trigger that does not) and the neutrality and redundancy gates (`python scripts/quality_gate.py --sub neutrality --sub redundancy`, run by a person).
* **Boundary B:** full mode, because the scaffold engine is a named high-risk surface. The change's own record is scoped, with `Certified by: pending`. The full suite is the certifying run before a push, the re-anchor ceremony or a release. I run no full suite.
* **Boundary C:** the code reviewer verifies the record and runs targeted falsification, not the full suite.

#### Security preflight — five questions, answered in writing

The engine is a high-risk surface and this change prints text derived from files, so the five questions apply. No code exists yet, so S2's "confirm you ran it" is the plan's to discharge; I name the mutation and the test that must fail.

* **S1 — Who supplied it?** Decisions: which slots are added (B) and which are for absent modules (A). Inputs to B: the new template (Cairn's own `templates/`, or a `--to <ref>` checkout; `src` is validated at `upgrade.py:195-225`); the adopter's file (project tree, already parsed strictly at `merge.py:200`); the old base copy (`dev/.cairn/base/`, in the project tree). The adopter's base copy can only remove names, never add one. Inputs to A: the installed module list (from the resolved profile) and a constant. No input is supplied by the thing being decided about.
* **S2 — Can it fail?** B: delete the old-base subtraction and the deleted-slot test must fail; subtract nothing but the adopter's names and the same test must fail. A: make the table empty and the solo test must fail; change "no supplier installed" to "not every supplier installed" and the one-of-five test (`role-roster-additions` with one supplier installed) must fail. A check that derives its expectation from its own table cannot fail, so the drift test reads slot names from the templates and module names from the shipped catalog, not from the table.
* **S3 — What fires it, over what?** `python bootstrap/scaffold.py --config <profile> --target <dir>` for A, over the files that run wrote. `python bootstrap/scaffold.py upgrade --target <dir> --plan` or `--stage` for B, over every tracked mergeable file. The adopter-facing sentence ("new in this upgrade") is true only for `clean`, `clean-locally-modified` and `conflict` files; a `new-core` file is not covered, and `UPGRADE.md` says so.
* **S4 — Which way does it break?** A: an unknown slot, a missing `modules` argument or any installed supplier lands in the main list, which is today's output (more obligations shown, no authority change). B: an unparseable old base, a parse error or a missing slot prints no name, which is today's output. Neither path adds authority; both are reports.
* **S5 — Who still wins?** Assumed attacker: someone who edits the project's lockfile or base cache, or ships a crafted template. Still succeeds: a crafted template can print a misleading slot name, escaped but readable (`'update-your-key'`); and a crafted base cache can suppress a real added-slot line by naming it. Neither writes, reads a path or runs anything. This is closed by construction for escape sequences (everything printed from the tree goes through `ascii()`), and by enumeration for misleading text, which only a human can judge.

**What the Security Review should examine** (the review is its own pass and I do not perform it):

* **Parsing of untrusted input.** The new `parse_slots` call on the base cache: failure mode, cost on a hostile file, and that a caught error is not widened. The `\S+` slot-name pattern (`bootstrap/_scaffold/slotmerge.py:40`) admits control bytes; check every new print goes through `ascii()`.
* **Path handling.** Confirm no new path is built, read or printed; that `fp.dst` in the new line is the validated lockfile name (`_check_lockfile_paths` runs first, `upgrade.py:195`); and that `print_report` takes no path it did not have.
* **Writes into a target tree.** Confirm there are none. `bootstrap/_scaffold/SECURITY_MUTATIONS.md` inventories every engine write; this change should add nothing to it, and `test_security_leaf.py` should still pass unchanged.
* The table's trust: a constant in the engine, not read from a file. Whether a mistake in it can ever hide an obligation (my claim: no, it regroups and never drops).

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

* A slot printed in the second list that an installed module does fill (the table has the wrong supplier). One such report means the table needs a second look at that slot, and the grouping is the first thing to cut.
* An `[new slot]` line for a slot the adopter deleted or already filled (a false positive). The tests above are meant to rule it out.
* Adopters filling a named slot with `<!-- cairn:customized -->` to silence the line (the board watch). If an adopter reports it, the wording is wrong, or the line should not exist.
* The quickstart count test failing after an unrelated template adds a slot: expected, and a sign the count is still pinned to output.
* The re-anchor deriving more than four changed symbols: something else moved, and this proposal's accounting is wrong.

## Questions for the Maintainer

* **Q1. List the two slots separately, or leave them out of the report?** Default: list them separately (as proposed). Leaving them out would make the report shorter but the gate in `bootstrap/BOOTSTRAP.md` (II-4) still expects each slot filled or marked N/A, so an adopter would hit it later with no warning. Cost if wrong: one more block of output.
* **Q2. Also correct the two slots the install fills itself?** Default: no, a follow-up row on the board. It needs the report to read the installed files, a new read in a printing function. Cost if wrong: the quickstart's "20 unfilled" stays two too high, as the 22 was.
* **Q3. Name added slots at `--apply` too?** Default: no; plan and stage only. Cost if wrong: an adopter who runs `--apply` without reading the plan sees nothing, and finds the slot through the existing note, as today.
* **Q4. Keep the supplier table in the engine, local to `print_report`?** Default: yes. The alternative is to declare the supplier in each module file, which means editing six or more module files and parsing them. Cost if wrong: the table is a second place to update when a module changes the slot it fills; the drift test catches a rename, not a new supplier.

## Scope delta

**Scope delta**: preserved. The baseline is the two board rows: classify the post-install report by the accepted profile, and name upgrade-added slots. Both are delivered as specified. Not in the baseline and not built: a report that asks only for live work (it needs the read-back in Q2), naming at `--apply` (Q3), and the `customized`-reflex mechanism (watched on the board, never built).

## Assurance path

**Assurance path**: high-assurance. The change edits the scaffold / merge engine, a named mandatory trigger (`AGENTS.md` and the template's `assurance-path-triggers`), and it changes an adopter-facing report and an AST baseline.
