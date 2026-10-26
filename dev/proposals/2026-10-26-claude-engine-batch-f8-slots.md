# Engine batch: a post-install report that matches the profile, and an upgrade that names the slots it adds

**Author**: Claude (Strategy)
**Status**: awaiting-decision
**Review**: usual + Security Review
**Plan review**: required(Internal + Internal Security Review) — the plan edits `bootstrap/_scaffold/`, a named high-risk surface
**Opened**: 2026-10-26
**In brief**: A minimal install's report moves 2 of its 22 slots (0 of 23 on the collaborative-team profile) to a separate list for modules it did not install, and `upgrade` names the slots it adds so a half-filled project does not lose a new one among the old.

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

## Review -- Claude Sonnet 5.5 (Internal) -- 2026-10-26

```
Reviewed commit: df9b05e521f8fba16950a2958af3828d4bbf36b8
Target: the whole proposal (all sections), read against the "### 0.5" section of dev/PLANNING.md, the F8 and #8 rows, GitHub issue #8 (read as data), and the engine at that commit
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual (pass 1 of 2; the Security Review is a separate pass by another reviewer and is not cleared, ruled on or pre-empted here)
**Findings**: raised (2 blocking, 6 non-blocking)
**Verdict**: REVISE

**Foundations**

1. **Should this happen as framed?** #8 yes: the Decision's trigger (an engine change that already owes a re-anchor) is met, and the change only prints. F8 yes, but not as worded: the table of module-filled slots is missing a slot, and the Scope delta and In brief say more than F8 delivers. -- `dev/plans/archive/neutrality-and-upgrade-slots.md:32`; `dev/proposals/archive/2026-08-20-claude-adopter-path-consolidation.md:1503`; scratch install with `modules_remove` (F1).
2. **Best alternative.** The proposal's own design (decide by installed modules, in the engine) is the best one. Its rival, `cairn:if` in the templates, loses by more than the proposal says: I measured that it would flag `slot-removed` on every existing solo adopter's next upgrade. Doing nothing is a fair rival and is fairly rejected. -- `python` call to `merge_file` on a base with the slot, an upstream without it: status `slot-removed` whether the adopter left the placeholder or wrote `N/A`.
3. **What would show it wrong.** The Signals section names one failure direction (a slot in the second list that an installed module fills). I found the other direction already present in the table: a slot of an absent module that would stay in the main list (F1). Add it as a signal and as a test. -- `bootstrap/BOOTSTRAP.md:418-427` against `templates/core/dev/proposals/_template.md:152`.

### Rulings on the four points

**(a) F8's yield.** It delivers the board row's words ("slots for modules it does not install"): 2 of 22 on `solo-greenfield`, 0 of 23 on `collaborative-team`. It does not deliver the archived Decision's success-criteria wording, "a post-install report that asks only for live work" (`...path-consolidation.md:1131, 1503`). The same Decision defines the F8 item itself more narrowly (`:1491`, "slots for modules the profile did not select"). So Q2 is not clearly a hidden half of F8, but it is the half the wide wording covers, and the Scope delta line "preserved" hides that (F2). Wrapping the two slots in `cairn:if` is fairly rejected; the strongest reason is measured, not argued (F4).
**(b) The supplier table.** Incomplete. It misses `documentation-tier-home`, in two files, filled from `documentation-plan` (F1). I found no other missed supplier. How I searched is in F1.
**(c) The #8 edge cases.** The four are the right ones. One is missing (a rename of a filled slot, F3) and one limit is unlisted (trees with no base copy, F6). "Quiet" on a malformed base cache is acceptable: I measured that today such a file is already reported as `conflict`, so the feature degrades to today's output.
**(d) The unchanged-contract claim.** Holds as far as it can be measured before the code exists. What I re-ran is under "Reproductions re-run", below. Nothing in it contradicts the proposal.

### Reproductions re-run (scratch folders outside the repo; interpreter Python 3.13.13, `/Users/kendal30/conda_envs/lhm/bin/python3.13`; sources are `git archive` extractions of df9b05e5)

* `solo-greenfield` install: report prints `Block slots requiring agent attention (22)`; `coordination-additions` and `role-roster-additions` are in it. Matches the proposal.
* `verify_integrity --target`: `slots checked 22, listed 20`. Matches. The two unlisted are `onboarding-tasks` and `security-verification`; the install output shows `[inserted] AGENTS.md > security-verification`. Matches. The same gap (checked minus listed = 2) appears on `collaborative-team` (23, 21) and `high-rigor-legacy` (23, 21), so the "two slots the install fills" holds for all three shipped presets.
* `collaborative-team` install: prints 23, both slots live, and its module list includes `coordination-tiers` and `model-selection`. Matches.
* #8: installed from copy A, ran `upgrade --plan`, `--stage`, `--apply` from copy B with one added slot in `templates/core/dev/README.md`. `--plan` lists `dev/README.md` under `clean (untouched)` and names no slot; `--stage` and `--apply` are silent too; `verify_integrity` then lists `example-added-slot` among 21 (23 checked). Matches.
* AST claim: on the unmodified tree `pytest bootstrap/tests/test_ast_attest.py` gives 30 passed. A probe constant added to `merge.py` gives 2 failed with "not in the pinned known-new manifest". An edited string in `print_report` gives `CHANGED FunctionDef:print_report`. Matches.
* Call-site claim: `grep print_report` over `bootstrap scripts tools docs templates` finds `install.py`, `cli.py`, `__init__.py`, `test_install_module.py` (plus an unrelated `_print_report` in `scripts/quality_gate.py`). The same grep style with `install_manifest` finds hits, so the pattern can match. `merge_file` has one engine caller, `upgrade.py:543`.
* Not re-run: the planned before-and-after `scaffold.py --manifest` byte comparison (nothing is built yet), and the lockfile and base-cache writes (read in `upgrade.py:2132` onward, not run).
* One reading, not run: `_gate_manifest.py:690-695` treats the baseline fixture `scaffold_ast_baseline.json` as `cascade_mutable`, so the re-anchor produces a `CASCADE-CHANGED` note and not a hold; two new test files add `COLLECTION-ADDED` notes. That supports "no frozen file edited".

### Findings

**F1 (blocking). The supplier table misses `documentation-tier-home`.** `documentation-discipline` is in the table. `documentation-tier-home`, filled from the same `documentation-plan` module with the same placeholder wording, is not. It appears in two files: `templates/core/dev/proposals/_template.md:152` and `templates/core/dev/plans/_template.md:168`; the module names both (`templates/modules/default-on/documentation-plan.md:21, 50, 110, 120`) and `bootstrap/_scaffold/config.py:787-788` says so. `bootstrap/BOOTSTRAP.md:418-427` lists neither, so the table inherits the gap from a hand derivation. Measured: a profile with `preset: solo-greenfield` and `modules_remove` of `documentation-plan`, `claim-check`, `reflections` and `security-verification` prints 22 slots today; under the proposed rule six would move to the second list and these two would stay in the main list although `documentation-plan` is absent. Search method: I listed every `cairn:slot` in `templates/`, read each placeholder for a module name, grepped `templates/modules` for `Adds to:`, `cairn:merge-target` and the word "slot", then grepped each slot name over `bootstrap scripts tools templates dimensions doctrine docs`. The control was the same grep on `documentation-tier-home`, which matched. Of the 22 report entries, 8 are filled from modules (the 6 in the table plus `documentation-tier-home` twice), 1 (`onboarding-tasks`) is filled by the onboarding step, and the other 13 have no module behind them. The proposed drift test checks table-to-template only, so it cannot catch this omission. Fix: add the slot (both files) to the table; add a completeness test that scans the core templates for the phrase "Filled from the `<module>`" and fails if any such slot is missing from the table; add the opposite-direction failure to the Signals.

**F2 (blocking). The Scope delta says "preserved", and the In brief and Rationale promise more than F8 delivers.** The In brief says a minimal install "stops mixing slots for modules it did not install into the list of work it owes". After the change the heading still reads "requiring agent attention" over 20 slots, 2 of which the install already filled (on solo the report would print 20 and `verify_integrity` already lists 20, but they are different sets: the report keeps the 2 filled slots and drops the 2 supplier slots, and `verify_integrity` does the reverse). The Scope delta names the baseline as "the two board rows"; the Decision it cites also deferred "a report that asks only for live work", and the Scope delta lists that as outside the baseline. That may be right, but it is the Maintainer's to concede, and the label should say so. Also, Q2 gives one reason for leaving the two slots out: the report would have to read the installed files. A second route needs no read: two more rows in the same table (`security-verification` when its module is installed; `onboarding-tasks` when a named preset is set, since `install_onboarding` fills it only then). Its cost is that the report predicts what a later step does. Fix: label the Scope delta `reduced` against the Decision's wide wording and `preserved` against the board row; say what is lost (the report still asks for 2 slots that need no work, and the quickstart's "unfilled" stays 2 high); put Q2 first, with three options (leave out, static rows, re-read), a recommended default, and the cost of each. Move the "2 of 22" figure into the In brief.

**F3 (non-blocking). A rename of a filled slot is not covered.** If upstream renames slot `a` to `b` and the adopter filled `a`, `merge_file` returns `slot-removed` at its orphan check (`merge.py:205-215`) before any added-slot logic; `slot-removed` is not a kind the new line prints. Measured: that exact case returns `slot-removed`. After the adopter resolves it by hand and applies, the base cache advances, so `b` is never named. Fix: list it in "What is lost", add a test that pins it, and put one sentence in `UPGRADE.md`. Naming `b` inside the `[flag]` line is optional and costs one more channel.

**F4 (non-blocking). The `cairn:if` rival fails for a stronger reason than the proposal gives.** Point (3) says every adopter's next upgrade "merges the change". Measured: for a solo adopter the old base has the slot, the new template (stripped by the profile) does not, and the adopter's placeholder text is non-empty, so `merge_file` flags `slot-removed`, including when the adopter wrote `N/A: coordination-tiers not installed`. That is a hand-resolve step for every existing solo adopter. Fix: state this in Alternatives. Point (2), five suppliers on different axes, I did not check.

**F5 (non-blocking). The added-slot names travel in a free-text field.** `MergeResult.detail` is "human-readable note" and `_print_upgrade_report` would print whatever it holds for three kinds. Today it is empty for those kinds, so the rule holds, but a later non-empty detail for `clean` or `conflict` would print as slot names. `needs-value` already uses `detail`, and a file can be both `needs-value` and carry a new slot; the proposal does not say which wins. Fix: state that names are filled only for `clean` and `conflict`; add a test that `detail` for those kinds is empty or exactly the escaped name list; say what `needs-value` shows. Also the proposal says "the same four-kind status"; `merge_file` returns five (clean, conflict, slot-removed, error, needs-value).

**F6 (non-blocking). Two unlisted limits of #8.** Trees with no base copy (`review-only`, "no recoverable base", for example after `--init-lock`) get no naming, and they are the trees most likely to have missed a slot. And the malformed-base case needs a test through the real `upgrade --plan` entry point, not only `merge_file`: I measured that a base with an unclosed slot makes the file `conflict` today, so the test should assert that status is unchanged and no `[new slot]` line appears. Fix: add both to "What is lost" and to the tests.

**F7 (non-blocking). `model-selection` is a role-roster supplier in `BOOTSTRAP.md:418-420`, but its own file says it adds to `doctrine/roles.md` and local configuration (`templates/modules/team-gated/model-selection.md:10-12`).** On `collaborative-team` the claim "both slots are live" rests on that one module. The table follows `BOOTSTRAP.md`, which is defensible, and the error fails toward more work. Fix: say which source the table follows, and note the disagreement for whoever next edits either file.

**F8 (non-blocking). Readability for the Maintainer.** "Supplier", "AST", "re-anchor", "contract surface", "Boundary A/B/C" are used without a definition (Plain Language rules 4 and 5). "Cost: low and continuing" under Do nothing gives an adjective, not a number (rule 14). The four questions come after about 150 lines. Fix: one-sentence definitions at first use; the Do-nothing cost as a number (2 of 22 lines on solo); lead with the questions, Q2 first.

Minor citation fixes, no finding: the strict parse of the adopter's file is `merge.py:200`, not `:201`. Every other path and line I checked resolves at df9b05e5: `install.py:1603`, `cli.py:627`, `merge.py:173, 202, 235`, `upgrade.py:565, 858, 868`, `slotmerge.py:40`, `verify_integrity.py:320-322`, `_ast_attest.py:143-148`, `UPGRADE.md:107-110`, `quickstart.md:298`, `test_quickstart_sequence.py:240-250`, `PLANNING.md:44, 222`, the archive lines `:1548` and `:32`, and `:553`. `python scripts/claim_check.py` on the proposal reports no flags (it exempted the two proposed test paths). The owning tests the proposal names exist. No existing test asserts the report's slot lines, so F8's only current guard is the quickstart count test.

### Coverage

I did not run the full suite, and built nothing. I did not check: the claim that five role-roster suppliers are selected by different axes (F4); how `--adopt-module` or `--to <ref>` interact with the new line; the Bandit and neutrality gates; the two `UPGRADE.md`-reading tests (`test_verify_integrity.py:1439`, `test_review_stance_in_shipped_files.py:1315`); the `CHANGELOG.md` entry; the claim that nothing else reads `FilePlan.detail` beyond my grep over `bootstrap/_scaffold/*.py`. For the Security Review, which I did not do: the new names are printed from an unbounded `\S+` pattern with no cap on length or number (`ascii()` escapes bytes but does not shorten); the base cache is not hash-checked at `--plan` time, though `verify_integrity` checks it, so a crafted base can suppress a line; and any Q2 variant that re-reads files adds a read in a function that now only prints. There are blocking findings (F1, F2); both are small edits to the proposal. No clearing round follows this review.

## Security Review -- Claude Opus 5.5 -- 2026-10-26

```
Reviewed commit: df9b05e521f8fba16950a2958af3828d4bbf36b8 (the proposal text; `git diff b7cf9586 -- <this file>` is empty, so pass 1 changed only its own section and the Status line)
Target: the whole proposal, as the Security Review of the scaffold engine change it designs; pass 1 read for what it left open, not re-done
Prior findings: none closed (pass 1's F1-F8 belong to the usual pass)
Assurance path: high-assurance
```

**Tier**: Security Review (pass 2 of 2)
**Obligation**: Show that this design gives nobody who controls a project file (lockfile, base cache, adopter file, profile) or the upgrade's template source any power they lack today: no new file read, write or path; no new route for control characters or unbounded text to the operator's terminal; no printed name that the proposal's stated inputs do not account for; the install contract byte-stable; and an AST accounting the gate can actually enforce.
**Findings**: raised (3 blocking, 3 non-blocking)
**Verdict**: REVISE. The Security Review **clears on conditions**: SR1, SR2 and SR3, below.

**Interpreter and method.** Every probe ran under Python 3.13.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13 -I`), against `git archive` extractions of df9b05e5 in fresh scratch folders outside the repository, removed afterwards. No full suite, no network, nothing written to this checkout but this section.

**In plain words.** Both changes only print. I found no way for them to read or write a file the engine does not already touch. Three things need fixing in the proposal before it is safe to build. (1) The upgrade's new line can be made to name a slot that is not in Cairn's template, through a value stored in the project's lockfile. The fix is to read slot names from the template before the stored values are filled in. (2) Nothing limits how long or how many names it prints: one hostile name prints a megabyte. The engine already cuts file names to 80 characters; do the same here. (3) The proposal says everything this report prints from the project is made safe for the terminal ("escaped": an unprintable character is shown as text such as `\x1b`, so the terminal displays it instead of obeying it). That is not true today: two existing lines in the same report print slot names raw, and I made one of them carry a clear-screen command. One escape rule at the place the report prints covers the old lines and the new one. A crafted base cache (Cairn's saved copy of each template, which the upgrade uses to tell the adopter's edits from Cairn's) can hide the new line. It can already decide which side of a merge wins, which is far more, so that belongs on the board, not in this change.

**Foundations**

1. **Should this happen as framed?** Yes from a security view, with three tightenings. Both changes only print, open no new path, and the only new parse runs on text the merge already parses. But the printed names have a source the preflight omits (lockfile token values), no size bound, and the "everything is escaped" claim is false for the function being edited. -- probes P1 to P3; `bootstrap/_scaffold/merge.py:127`, `:194-202`; `bootstrap/_scaffold/upgrade.py:461`, `:530`.
2. **Best alternative.** The same design, with names taken from the raw new template, cut and capped, and one escape where the report prints `detail`. Doing nothing is not the safer rival: today's `[flag]` lines already print slot names from the adopter's file raw (P3). A hash check of the base cache scoped to this line is a worse rival: it would guard one printed line while the same unchecked bytes drive the merge beside it (P5). -- P3; P5; `upgrade.py:852-858`.
3. **What would show it wrong.** A `[new slot]` name that is not in the new template's raw text; a printed line longer than the cap; a character outside printable ASCII reaching stdout from `detail`; a file opened or written that the engine does not open or write today; a fifth CHANGED symbol, a NEW non-import symbol, or a changed top-level import at the re-anchor. -- the closing tests in SR1 to SR4.

### Probes (Python 3.13.13, scratch extractions of df9b05e5)

* **P1, token injection.** A lockfile token value carrying a `<!-- cairn:slot update-your-key -->` / `<!-- cairn:end update-your-key -->` pair, used in the new template where the old one did not use it. `parse_slots` on the token-filled new template finds `{'update-your-key'}`; on the raw template it finds none. Today `merge_file` returns `clean` and the merged text carries the injected slot. Token values come from the lockfile with no check beyond `str(v)` (`upgrade.py:461`).
* **P2, size and escaping.** A 1 MB slot name parses in 0.010 s, and `ascii()` of it is 1,048,578 characters; a 1 MB run of non-ASCII (262,144 emoji) becomes 2,621,442. 100,000 slots parse in 0.145 s, and their joined escaped names are 988,888 characters. The cost is a flood of output, not CPU. `ascii()` of names carrying an ESC colour or clear-screen sequence, an OSC title sequence with BEL, U+202E (right-to-left override), the C1 control `\x9b`, U+034F (combining grapheme joiner) and U+3164 (Hangul filler): every output character was printable ASCII.
* **P3, today's raw prints.** A slot named `x\x1b[2J\x1b]0;pwned\x07\u202egnp.exe`, filled in the adopter's file and removed upstream: `merge_file` returns `slot-removed` with the raw ESC and U+202E in `detail` (built at `merge.py:211`), and `_print_upgrade_report` prints it as-is (`upgrade.py:858`). A malformed slot whose name carries an ESC reaches the same line through `malformed slots: {exc}` (`upgrade.py:546`). Both measured.
* **P4, AST gate.** Control: the unmodified tree, `_ast_attest.py verify --known-new ...` over `bootstrap/_scaffold/*.py`, exits 0 ("173 baselined symbol(s) accounted for, unchanged"). A stand-in for the design (a `modules=` keyword on `print_report`, the argument passed at `cli.py:627`, an added-slot computation in `merge_file`, a `[new slot]` loop in `_print_upgrade_report`) gives exactly four CHANGED: `print_report`, `main`, `merge_file`, `_print_upgrade_report`; exit 1. The same plus a module-level `_ADDED_CAP = 10` adds `NEW Assign:_ADDED_CAP (not in the pinned known-new manifest)`. The same plus a changed top-level import in `merge.py` (`from typing import NamedTuple, Iterable`) still reports four: imports are exempt (`bootstrap/tests/_ast_attest.py:180-189`), and the change shows only as one `note: NEW Import:` hash replacing another (36 notes before and after).
* **P5, what the base cache already decides.** Through `merge_file`, with an adopter edit on one line and an upstream fix on another: a base cache equal to the adopter's file returns `clean`, which the report labels `clean (untouched)`, and drops the adopter's edit. A base cache equal to the new template returns `clean` and drops the upstream fix.

### Answers to the seven questions

1. **Preflight S1 to S5, and the base cache.** S2 to S4 hold. S1 misses a source: lockfile token values can add a name (P1). "The adopter's base copy can only remove names" is true; "no input is supplied by the thing being decided about" is not (SR1). S5: a crafted base cache can suppress the line, as stated, and through this change it gains nothing more, because every printed name is a slot of the new template and the base and the adopter's file only subtract. That is acceptable. It is less than the base cache already controls (P5); the integrity command's slot note still lists the slot (`bootstrap/verify_integrity.py:320-322`); and the failure is today's output. What the design should **refuse**, by construction rather than by a warning: a name from any source but the new template's raw text (SR1); more than a fixed amount of printed text (SR2); any character of `detail` reaching the terminal unescaped (SR3); a caught error wider than `SlotError` (SR5). It should **not** add a base-cache hash check of its own (SR6).
2. **`ascii()`.** Safe on every route the design adds, as long as it is the last step before printing. The routes that miss it are the existing ones (P3, SR3). Against `encode_display` (`templates/skills/_lib/session.py:188`): `ascii()` escapes every non-ASCII code point, which includes everything `encode_display` escapes for safety. So it is **stronger for the terminal and weaker for readability**: an accented or CJK slot name prints as `\u` codes, and Cairn's own slot names are ASCII. It is not a second escape table: it is a Python builtin with no table, and the engine already uses it at `install.py:604` and `upgrade.py:169`. The engine does not import the skills library (a grep of the engine's import lines for `session`, `skills`, `_lib` or `encode_display` finds none; the same grep for `security` finds 6). The install report prints slot names raw (`install.py:1668`), but those come from Cairn's own templates at install time, and F8 adds no source of them.
3. **Base cache not checked at `--plan`; paths.** It allows the S5 suppression and, through the merge itself, P5. No path to a read or write outside the target tree goes through this change. B parses the bytes already read at `upgrade.py:530`, from a name `_check_lockfile_paths` contains at `upgrade.py:2592`, before `_compute_upgrade` runs (`:2691`). A opens nothing. `detail` is never written: its only readers are `upgrade.py:565, 858, 868` (the grep found all three, so the pattern can match). The change leans on lockfile paths in one place: `fp.dst` in the new line is a lockfile name, safe to print only because `_check_lockfile_paths` refused unprintable ones. The 0.5 lockfile-path batch is editing that function (`dev/PLANNING.md:85-124`), so the two must not run in parallel on `upgrade.py`, as the board already says.
4. **Q2 variants.** (i) Leave the two slots out, and (ii) static table rows: no read; acceptable. (iii) A variant the proposal does not list, also with no read: print the report after the module-merge pass (`cli.py:643`) and drop the slots that pass reports filled. It uses results already in memory, but it moves output that the quickstart test pins. (iv) Re-read the installed files: acceptable only if each read follows the no-link rule the install's writes follow (`_assert_safe_write`), is size-capped, and escapes what it prints. It adds a read to a printing function for no more accuracy than (iii); I recommend against it.
5. **AST.** Interpreter: Python 3.13.13. A faithful stand-in gives four CHANGED and nothing NEW (P4), so the author's count holds. "No new top-level symbol is allowed" holds, and is enforced, for functions, classes and assignments. It does not hold for imports: a changed or added top-level import binds a new module-level name and passes the gate (SR4).
6. **Install contract.** The design keeps it byte-stable. It adds no lockfile field; `detail` lives only in memory; `scaffold.py --manifest` is derived from the mapping tables alone (`install.py:1688-1702`), and the design touches none of them. The four changed files are not among the gate manifest's 195 `frozen_files`; the launcher `bootstrap/scaffold.py` is, and stays untouched; the AST baseline is `cascade_mutable`. What would break it: carrying the names to `--apply` by writing them into the stage metadata (Q3); adding a field to `MergeResult` or `FilePlan`; putting the F8 table into `_MODULE_MAPPINGS` or another mapping; editing the launcher or a frozen test.
7. **Other.** Hostile profile: an exact `modules:` list is not checked against known module names (`cli.py:372`; unknown names are later printed raw at `install.py:1526`, which predates this change), so F8 must only test membership and print names from its own table (SR5). Hostile module file: F8 reads none, by the proposal's choice (Alternatives, fourth bullet). Hostile template under `--to <ref>`: it already supplies every byte the upgrade writes, so its names add nothing new; SR2 bounds them. Symlinks: no new file is opened. Ordering: the design adds no refusal and no write. At `--stage` the report, the new line included, prints after the stage is written (`upgrade.py:2702`, `:2709`), as today, which is right for a line that only informs. `--adopt-collisions` also calls `_compute_upgrade` (`upgrade.py:1848`), so the new parse runs there and its result is discarded; harmless. Parse cost on a hostile base is not new: `_transplant_slots` already parses the base (`merge.py:127`).

### Findings

**SR1 (blocking; low impact). Take the names from the new template's raw text, not the token-filled text.** `merge_file` fills lockfile token values into the base and the new template before parsing them (`merge.py:194-195`, `:202`), and those values are unchecked (`upgrade.py:461`). P1: a token value can add a slot, which the proposed rule would name as new. The text is escaped, but it falsifies S1 and lets a project file choose the name in a line that tells the reader to act ("Fill it"). **Fix:** compute the added names as the slot names of `parse_slots(theirs_raw)`, minus those of `parse_slots(base_raw)`, minus those of the adopter's file; both raw parses sit in one `try ... except SlotError` that yields no names. Correct S1 to list token values as an input that can no longer add a name. **Closing test:** in `test_upgrade_added_slots.py`, through `upgrade --plan`, a lockfile token value carrying a slot pair and used only in the new template gives no `[new slot]` line; a mutant that parses the token-filled text must fail it. The obligation clears on this point once the revision adopts the fix.

**SR2 (blocking; low). Bound what is printed.** P2: one name can print a megabyte; 100,000 names print nearly as much. **Fix:** per name, the engine's existing rule for lockfile names (`upgrade.py:169-170`: `ascii(value[:80])`, then cut to 100 characters with `...`); per file, at most 10 names, then `(and N more)`. Both numbers are literals inside the function, because a module-level constant fails the AST gate (P4). **Closing test:** a new template with one 1 MB slot name, and one with 1,000 new slots: each `[new slot]` line stays under a fixed length (for example 1,200 characters) and states the count. Clears once adopted.

**SR3 (blocking; low; a record correction, with a recommended fix). S5's "everything printed from the tree goes through `ascii()`" is false for the report this change edits.** P3: `slot-removed` and malformed-slot details carry raw ESC and U+202E to the terminal today, through the `[flag]` line in `_print_upgrade_report`. **Preferred fix:** escape where the report prints `detail`. Every `fp.detail` printed at `upgrade.py:858`, `:868` and on the new line goes through `ascii(text)[1:-1]` (the `esc` form at `install.py:604`); `merge_file` then need not escape (if it does too, backslashes double, which is still safe). This edits only `_print_upgrade_report`, already one of the four symbols, so it adds no symbol and no re-anchor cost, and ASCII text prints unchanged. **Minimum fix:** correct S5 to "the new line only" and add a board row for the two raw routes. **Closing test:** through `upgrade --plan`, an adopter file with a filled slot whose name holds an ESC, removed upstream: every `[flag]` and `[new slot]` line contains only printable ASCII. On today's code the test fails, which is its control. Clears once either form is adopted; the preferred form also closes the existing routes.

**SR4 (non-blocking). The AST gate does not see top-level imports.** P4. The proposal's "a new top-level engine name would fail the AST check" is true for functions, classes and assignments, and false for imports. **Fix:** the plan states that no top-level import is added or changed in `install.py`, `cli.py`, `merge.py` or `upgrade.py`. The design needs none: `parse_slots` and `SlotError` are already in `merge.py`. The code reviewer checks it in the diff, because the gate will not. **Check:** the sorted `note: NEW Import:` lines of `_ast_attest.py verify` are identical before and after the change; P4's import mutant shows one hash swapped. Non-blocking because the design needs no import; it binds the plan.

**SR5 (non-blocking). Two design rules to write into the plan.** (a) F8's second list prints module names from the engine's own table, never from the profile's `modules` list. (b) The new parse catches `SlotError` only, as `_transplant_slots` does (`merge.py:129`), never a wider class. **Check:** for (a), a test: a profile whose exact `modules:` list holds a non-module name containing an ESC byte prints no ESC in either slot list; for (b), the code reviewer reads the `except` clause.

**SR6 (non-blocking; a board row, not this change). The upgrade does not check the base cache before the merge uses it.** P5. This change does not widen that. **Recommendation:** a board row: at `--plan`, `--stage` and `--apply`, compare each base cache's SHA-256 with the lockfile's `base_hash`, as `verify_integrity` already does (`bootstrap/verify_integrity.py:244-247`), and on a mismatch refuse the 3-way merge for that file, degrading it to `review-only` with a fixed-words reason. Its limit: someone who edits both the lockfile and the base cache passes that check. It catches drift and single-file tampering, not a coordinated edit. Not a condition of this review.

### Verdict

**Clears on conditions.** The Security Review obligation clears when the author's Response adopts SR1, SR2 and SR3 (SR3 in either form) as specified above. SR4 and SR5 bind the plan; SR6 is a board recommendation. The conditions are proposal-text edits; the Maintainer at the Decision and the plan's Internal Security Review check that they landed. I ask for no second Security Review pass on this proposal. Status stays `revising`.

### Coverage

Not checked: built code (none exists); pass 1's F1 to F8 (not re-done); the `--to <ref>` path end to end (read only, `_theirs_bytes`, `upgrade.py:280-290`); `--adopt-module`; the Bandit and neutrality gates; the two tests that read `UPGRADE.md`; whether an existing test pins a `[flag]` or review-only line with non-ASCII text that SR3's preferred fix would change (the implementer checks; the non-ASCII warning sign at `upgrade.py:865` is fixed text outside `detail` and is not affected); Windows consoles; whether an agent reading this output treats an escaped name as data (the quotes `ascii()` adds help). Found, older than this change, and outside it, for the lockfile-path batch: `isprintable()` passes invisible code points such as U+3164 and U+034F (measured `True`), which `encode_display` escapes, so a lockfile `dst` can carry them into every line of this report; and `install.py:1526` prints an unknown profile module name raw.

## Response -- Claude (author) -- 2026-10-26

I accept every finding. Two I accept with a variation (F5's detail rule, SR2's cut point), and one optional extra I decline (F3). The Revision below is the complete current contract. What changed most: Q2 is now first and has three options (F2); the supplier table gains `documentation-tier-home` (F1); the new-slot names come only from the new template's text before token values are filled in (SR1); and the report escapes `detail` where it prints, which also fixes the existing `[flag]` lines (SR3). I did not re-measure anything. Every figure I take from the reviews comes from the reviewer who measured it, at commit `df9b05e5`.

**Usual review (pass 1)**

* **F1, accepted.** `documentation-tier-home` (in `dev/proposals/_template.md` and `dev/plans/_template.md`, filled from `documentation-plan`) joins the table. A completeness test reads the core templates for placeholders that say "Filled from the `<module>`" and fails on a slot the table lacks. The opposite-direction failure joins the Signals. The test cannot see a slot whose placeholder does not use that phrase (`coordination-additions` and `role-roster-additions` do not), so those two stay hand-listed; the Revision says so.
* **F2, accepted.** The Scope delta is `degraded`: reduced against the archived Decision's wide wording, preserved against the board row. The In brief carries "2 of 22 on `solo-greenfield`, 0 of 23 on `collaborative-team`". Q2 is first, with three options and a default. The no-read route the reviewer found is option (b).
* **F3, accepted, with the optional part declined.** The rename case is listed in "What is lost", pinned by a test, and gets one sentence in `UPGRADE.md`. I decline naming the new slot inside the `[flag]` line: it opens one more channel for a rare case, and the adopter already has to resolve that file by hand.
* **F4, accepted.** Alternatives now states the measured `slot-removed` flag on every existing solo adopter's next upgrade.
* **F5, accepted, with a variation.** Five statuses, not four, and names fill `detail` only for `clean` and `conflict`. `needs-value` keeps its note and prints no names; they print on the later run that supplies the value. The variation: the test says `detail` for those two kinds is empty or exactly the name list, so it can fail.
* **F6, accepted.** Trees with no base copy get no naming and the malformed-base case has a test through the real `upgrade --plan`. Both are in "What is lost" and in the tests.
* **F7, accepted.** The table follows `bootstrap/BOOTSTRAP.md:418-420` for `role-roster-additions`; `model-selection`'s own file disagrees. I name the disagreement and do not edit either file.
* **F8, accepted.** Terms are defined where they first matter. "Low and continuing" is gone: Do nothing now gives the numbers I have, and says there is no measure of adopter time lost.
* **Citation fix, accepted.** `merge.py:200`.

**Security Review (pass 2)**

* **SR1, accepted as stated.** Names are `parse_slots(theirs_raw)` minus `parse_slots(base_raw)` minus the adopter's names, both raw parses inside one `except SlotError`. S1 is corrected: token values cannot add a name now, and I withdraw "no input can add a name". The closing test, with its mutant, is in the Revision.
* **SR2, accepted.** At most 10 names per file, each cut to 80 characters, then `(and N more)`. Both are literals inside `merge_file`. One small difference from the engine's rule at `upgrade.py:169-170`: that rule cuts after escaping. Here the escape moves to the print site (SR3), so I cut before it and state the resulting bound in the Revision.
* **SR3, accepted, the preferred fix.** `_print_upgrade_report` prints every `detail` through `ascii(text)[1:-1]`. It is already one of the four changing symbols, so it adds none. S5's false sentence is withdrawn.
* **SR4, accepted.** The plan states that no top-level import is added or changed in the four files; the code reviewer checks the diff.
* **SR5, accepted.** Both rules are written in; the test for (a) is in the Revision.
* **SR6, outside this proposal.** The upgrade does not check each saved base copy against its recorded hash before the merge uses it. The coordinator is deciding about a board row. I add no work for it here.

## Revision -- Claude (author) -- 2026-10-26

### In brief

On a minimal install, the post-install report moves 2 of its 22 slots (0 of 23 on `collaborative-team`) to a separate list for modules the profile did not install, and `upgrade` names the slots it adds so a half-filled project does not lose a new one among the old. This is less than the archived Decision's wording, "a report that asks only for live work"; Q2 asks how far to go.

### Questions for the Maintainer (each has a default; none blocks)

* **Q2. How far should the report go toward "asks only for live work"?** After this change `solo-greenfield` still lists 20 slots. Two of them (`onboarding-tasks` in `dev/PLANNING.md`, `security-verification` in `AGENTS.md`) the install fills itself after the report is built, so they need no work. Three options:
  * **(a) Leave them in the count.** No code. The quickstart's "unfilled" stays 2 too high, as it was. The report can only show too much, never too little.
  * **(b) Two more table rows, no read.** `security-verification` leaves the main list when its module is installed; `onboarding-tasks` leaves it when a named preset is set (the onboarding step fills it only then). The count becomes 18. Cost: the report predicts what a later step does. If that step is skipped or fails, an unfilled slot goes unlisted and the adopter meets it at the `BOOTSTRAP.md` II-4 gate with no warning. This is the only option that can show too little.
  * **(c) Use what the install produced.** Either re-read the installed files (a new read in a printing function; the Security Review recommends against it), or print the report after the module-merge pass (`cli.py:643`) and drop the slots that pass reports filled. The second needs no read, but it moves output that `test_quickstart_sequence.py` pins.
  * **Default: (a)**, with a board row for the second form of (c). Cost if wrong: the report keeps two lines that need no work.
* **Q1. List the two absent-module slots separately, or leave them out of the report?** Default: separately (as proposed). Leaving them out shortens the report, but the II-4 gate still expects each slot filled or marked `N/A`, so an adopter would meet it later with no warning. Cost if wrong: one more block of output.
* **Q3. Name added slots at `--apply` too?** Default: no; plan and stage only. `--apply` has no old/new pair in hand and would recompute. Cost if wrong: an adopter who runs `--apply` without reading the plan sees nothing, and finds the slot through the existing integrity note, as today.
* **Q4. Keep the supplier table in the engine, local to `print_report`?** Default: yes. The alternative is to declare the supplier in each module file, which means editing six or more module files and parsing them. Cost if wrong: the table is a second place to update when a module changes the slot it fills. The completeness test catches a missing slot; it cannot catch a supplier whose placeholder lacks the phrase it scans for.

### Context

The Context section above stands: its numbers are measurements by me and by the usual reviewer, at `df9b05e5`. One fact added by the reviews: `slot-removed` is returned before any new-slot logic runs, so a rename of a filled slot never names the new slot (measured by the usual reviewer).

### Terms

*Slot*: a block in a template between `<!-- cairn:slot NAME -->` and `<!-- cairn:end NAME -->`, which the adopter fills or marks `N/A`. *Supplier*: a module whose content fills a slot. *AST check*: `bootstrap/tests/test_ast_attest.py` fingerprints every function and top-level name in the engine against a committed baseline and fails when one changes. *Re-anchor*: the Maintainer-run correction of that baseline (`bootstrap/AST_BASELINE_RUNBOOK.md`). *Boundary A, B, C*: the implementer's scoped run, the implementer's integration record, and the code reviewer's checks (`AGENTS.md`, "Verification boundaries").

### What changes

Both changes print more precisely. Neither writes a file, reads a new path, or changes the lockfile.

**A. Group the install report by profile** (`print_report`, `bootstrap/_scaffold/install.py:1603`; call site `bootstrap/_scaffold/cli.py:627`).

1. `print_report` gains one keyword parameter, `modules` (the installed module names, which `main` already holds). Absent, it behaves as today. It only tests membership in `modules`; every module name it prints comes from its own table, never from the profile's list.
2. A table local to `print_report` names the supplier modules for each slot filled from modules:

   | Slot | Where | Supplier modules |
   |---|---|---|
   | `claim-check` | `AGENTS.md` | `claim-check` |
   | `reflections` | `dev/agent_collaboration.md` | `reflections` |
   | `documentation-discipline` | `AGENTS.md` | `documentation-plan` |
   | `documentation-tier-home` | `dev/proposals/_template.md`, `dev/plans/_template.md` | `documentation-plan` |
   | `security-verification` | `AGENTS.md` | `security-verification` |
   | `coordination-additions` | `dev/agent_collaboration.md` | `coordination-tiers` |
   | `role-roster-additions` | `dev/agent_collaboration.md` | `domain-agents`, `legacy-agent`, `security-review`, `issue-capture`, `model-selection` |

   Source: `bootstrap/BOOTSTRAP.md:418-427` for `role-roster-additions`, `coordination-additions`, `claim-check` and `reflections`; the "Filled from the `<module>`" placeholders in `templates/core/` for the others. The two sources disagree on one name: `BOOTSTRAP.md:418-420` lists `model-selection` as a `role-roster-additions` supplier, but `templates/modules/team-gated/model-selection.md:10-13` says it adds to `doctrine/roles.md` and local configuration. The table follows `BOOTSTRAP.md`. The error fails toward more work shown, and a comment at the table names the disagreement for whoever next edits either file.
3. A slot in the table whose suppliers are all absent leaves the main list and goes into a second list, printed after it: `Slots for modules this profile did not install (N):`, each with its module names, then one line: "Mark each `N/A: <reason>` (for example `N/A: coordination-tiers not installed`), or fill it yourself if your project needs it." Nothing is dropped. The main heading keeps its text and counts only the remaining slots (20 on `solo-greenfield`).
4. A slot not in the table, or with any supplier installed, stays in the main list.

**B. Name the slots an upgrade adds** (`merge_file`, `bootstrap/_scaffold/merge.py:173`; `_print_upgrade_report`, `bootstrap/_scaffold/upgrade.py:815`).

1. **Where the names come from.** `merge_file` takes the slot names of `parse_slots(theirs_raw)` (the new template as passed in, before token values are filled), removes those of `parse_slots(base_raw)` (the saved old template), and removes those of the adopter's file. Both new parses sit in one `try` that catches `SlotError` and nothing wider; on `SlotError` there are no names. Today the merge fills lockfile token values into both templates before it reads their slot names (`merge.py:194-195`, `:202`), and a stored value can carry a fake slot pair; the new parses read the text before that fill, so a stored value cannot add a name.
2. **Which results carry names.** `merge_file` returns five statuses: `clean`, `conflict`, `slot-removed`, `error` and `needs-value`. Names fill `detail` only on `clean` and `conflict`. `slot-removed` and `error` return earlier and keep their own notes. `needs-value` keeps its note and gets no names; they print on the later run that has the value. Today `detail` is `""` on `clean` and `conflict` (`merge.py:224`, `:235`).
3. **Bounds.** At most 10 names per file, each cut to 80 characters (a longer name ends in `...`), then `(and N more)`. Both numbers are literals inside `merge_file`, because a module-level constant fails the AST check. `merge_file` returns names unescaped.
4. **Printing.** `_print_upgrade_report` prints every `detail` through `ascii(text)[1:-1]` (the `esc` form at `install.py:603-604`): the `[flag]` line (`upgrade.py:858`), the review-only line (`:868`) and the new line. For `clean`, `clean-locally-modified` and `conflict` files whose `detail` is non-empty it prints one line: `[new slot] dev/README.md: example-added-slot -- new in this upgrade. Fill it, or write N/A: <reason>.` The old `[flag]` lines today print a slot name from the adopter's file raw, which the Security Review measured carrying an escape sequence to the terminal; this closes those routes too. ASCII text prints unchanged. Bound on the new line: at most 10 names of at most 80 characters, so under 1,200 characters for ASCII names and under 8,300 in the worst case, because a character outside the Basic Multilingual Plane escapes to 10 characters.
5. **No names, as today:** a file new in the upgrade (`new-core`), a tree with no base copy (`review-only`, for example after `--init-lock`), an unparseable old base, a renamed filled slot (`slot-removed`), a `needs-value` file.

**What I add, and what I did not.** No option, flag, new file, new function, new top-level name, lockfile field or manifest field. The four symbols that change are `print_report`, `main` (`cli.py`), `merge_file` and `_print_upgrade_report`. The plan states that no top-level import is added or changed in `install.py`, `cli.py`, `merge.py` or `upgrade.py`: the AST check does not see imports (measured by the Security Review), so the code reviewer checks the diff, and the design needs none (`parse_slots` and `SlotError` are already in `merge.py`).

**Separate trigger, kept as it is.** The board keeps the watch for adopters who fill slots by reflex with `<!-- cairn:customized -->` (`dev/PLANNING.md:222`). This proposal builds no mechanism for it.

**Outside this proposal.** The upgrade does not check each saved base copy against its recorded hash before the merge uses it (`verify_integrity` does). A crafted base copy can already decide which side of a merge wins, so this change adds nothing to it. The coordinator is deciding about a board row. I add no work for it.

### Rationale

F8 matters because the first screen an adopter sees after install should not ask for work the profile does not need. This change moves 2 of 22 slots on `solo-greenfield` and 0 of 23 on `collaborative-team`, so it does not make the list short. What it delivers is the part the profile can decide: which slots have a module behind them. #8's gap is real but narrow: on a partly filled tree the existing note buries a new slot among old ones (17 listed in the archived plan's measurement), and `upgrade` is the one step that has the old and new template side by side.

### Alternatives considered

* **Do nothing.** On `solo-greenfield` 2 of the 22 lines name a slot whose module is absent, and the quickstart prints a count the profile does not justify. A new slot on a partly filled tree is found only by reading a list of about 17. I have no measure of adopter time lost. Both items were deferred once and the Maintainer put them in 0.5.
* **Split into two proposals.** Two Security Reviews and two re-anchors for changes in different files. It loses on cost; the two share one rule (name what is new, escape what comes from the tree), so one review reads them together. The batch is the Maintainer's call ("Engine batch is in").
* **Template-only F8: wrap the two slots in `cairn:if`.** The engine already strips regions by profile axis (`strip_conditional_regions`, `bootstrap/_scaffold/config.py:1459`). It needs no engine change and no Security Review, so it is the strongest rival. It loses on three points. (1) It keys on axes, not on installed modules; a profile can list `modules:` itself and `upgrade --adopt-module` adds a module later. (2) It edits two core templates every adopter has. (3) The usual reviewer measured the effect on existing adopters: the old base has the slot, the new template (stripped by the profile) does not, and the adopter's placeholder is non-empty, so `merge_file` returns `slot-removed` on every existing solo adopter's next upgrade, even when they wrote `N/A: coordination-tiers not installed`. Each would have to resolve that by hand. I did not check whether the five `role-roster-additions` suppliers are chosen by different axes.
* **Read the supplier from each module file.** Only `security-verification` carries a `cairn:merge-target` line (`templates/modules/default-on/security-verification.md:193`); the others say "Adds to:" in prose. It means editing six or more module files and parsing them. The table needs neither.
* **Also fix the two slots the install fills itself.** Q2.
* **Also print added slots at `--apply`.** Q3.
* **A hash check of the base copy, scoped to this line.** It would guard one printed line while the same unchecked bytes drive the merge beside it. Rejected on the Security Review's reasoning; see "Outside this proposal".

### What is lost

* The report's first count falls from 22 to 20 on `solo-greenfield`. The only repository consumer is the quickstart prose and its test, which I edit.
* The report still lists the two slots the install fills itself (Q2), so the quickstart's "unfilled" stays two too high. It was two too high before.
* The table can drift. A missing slot fails toward more work shown; the completeness test catches a missing slot when the placeholder uses "Filled from the `<module>`", and does not for `coordination-additions` or `role-roster-additions`.
* Added-slot naming has holes, each listed in B.5. The two that matter most: a tree with no base copy, which is the tree most likely to have missed a slot, and a rename of a filled slot, where the adopter resolves the `slot-removed` flag by hand, the saved base advances, and the new name is never printed. `UPGRADE.md` says so; a test pins it.
* Existing `[flag]` lines print a non-ASCII slot name as `\u` codes. Cairn's own slot names are ASCII.
* A crafted base copy can hide the new line (S5).

### Documentation / doctrine surface

Descriptive and prose layer only; no `doctrine/` file, no `AGENTS.md`. Routing per `docs/DOCUMENTATION_PLAN.md`.

* `docs/quickstart.md:298`: "22" becomes the new count, and one clause says the report lists the other slots separately. `test_quickstart_sequence.py:240-250` pins the number, so the edit and the engine change land together.
* `bootstrap/UPGRADE.md`: one sentence in the `--plan` bullet (`UPGRADE.md:107-110`) saying plan and stage name slots the upgrade adds, and which cases they do not cover (a file new in the upgrade, a tree with no base copy, a renamed filled slot). Two tests read this file (`test_verify_integrity.py:1439`, `test_review_stance_in_shipped_files.py:1315`); the implementer runs them.
* `CHANGELOG.md`, `## Unreleased`: one entry that also names the escape on the existing `[flag]` lines.
* Not edited: `bootstrap/BOOTSTRAP.md`, the fidelity manifest, `dev/PLANNING.md` (a shared file, edited at its serialization points).

### Install contract and upgrade impact

* **Adopters who already installed.** Nothing on disk changes. At the next `upgrade --plan` or `--stage`, a file where Cairn added a slot gets one extra line, and existing `[flag]` and review-only lines print non-ASCII text as escapes.
* **Lockfile schema, fidelity manifest, gate manifest, `scaffold.py --manifest`: unchanged.** `print_report` is called once (`cli.py:627`) and writes to stdout only. `detail` lives in memory: it flows from `merge_file` into `FilePlan` (`upgrade.py:565`) and is printed at `:858` and `:868`; the reviews' greps found no other reader. The implementer runs `scaffold.py --manifest` before and after and compares bytes.
* **AST re-anchor: Maintainer-run, four changed symbols, none new.** None of the four is on the self-service allowlist (`bootstrap/tests/_ast_attest.py:143-148`), so the correction is a Maintainer-run, dry-run-verified direct correction that an implementing agent does not perform. This list comes from reading the proposal against the code; the Security Review confirmed it with a stand-in under Python 3.13.13 (four CHANGED, no NEW). The implementer re-derives the set from the final tree. The canonical interpreter is 3.13.x. The sorted `note: NEW Import:` lines of `_ast_attest.py verify` must be identical before and after.
* **Frozen files: none edited.** Nearly every file under `bootstrap/tests/` is frozen (`bootstrap/tests/fixtures/gate_manifest.json`). Editing one owes the gate-manifest ceremony, so the new tests go in two new files.

Proposed paths:
* `bootstrap/tests/test_install_report_slots.py`
* `bootstrap/tests/test_upgrade_added_slots.py`

### Evidence / verification plan

I have not built this. The reproductions in the Context are measured; the claims about the result are expected. Each test goes through the real entry point.

**F8, `bootstrap/tests/test_install_report_slots.py` (new).**
* Run `scaffold.py` on `solo-greenfield` and `collaborative-team`. On solo, `coordination-additions` and `role-roster-additions` are in the second list and not the main one, the main count equals the number of main-list lines, and both lists together total 22. On collaborative-team both are in the main list and the second list is absent. A call with `modules` omitted lists every slot in the main list.
* **Both failure directions.** A profile with `documentation-plan`, `claim-check`, `reflections` and `security-verification` removed puts every slot of those modules, `documentation-tier-home` in both files included, in the second list. A profile that installs a supplier never has its slot in the second list.
* **Completeness.** Every slot whose core-template placeholder says "Filled from the `<module>`" is in the table with that module. The test reads the templates, not the table.
* **Drift.** Every slot name in the table exists in a core template and every module name in it is a shipped module.
* **Hostile module name.** A profile whose exact `modules:` list holds a non-module name with an ESC byte prints no ESC in either list.

**#8, `bootstrap/tests/test_upgrade_added_slots.py` (new).** Through `merge_file` and through `upgrade --plan` and `--stage` on an installed scratch tree:
* A new slot is named. A slot the adopter deleted (in the old base, absent from the adopter's file, present upstream) is not. A slot the adopter already has is not.
* `detail` for `clean` and `conflict` is empty or exactly the name list. `needs-value`, `slot-removed` and `error` carry no names.
* **Token injection.** A lockfile token value that carries a slot pair, used only in the new template, gives no `[new slot]` line. A mutant that parses the token-filled text must fail this test.
* **Bounds.** A new template with one 1 MB slot name, and one with 1,000 new slots: each `[new slot]` line stays under the bounds in B.4 and states the count.
* **Escape.** An adopter file with a filled slot whose name holds an ESC byte, removed upstream: every `[flag]` and `[new slot]` line is printable ASCII. On today's code this test fails, which is its control.
* A malformed old base: status unchanged (today `conflict`, measured by the usual reviewer) and no `[new slot]` line.
* A tree with no base copy: `review-only`, no names.
* A renamed filled slot: `slot-removed`, the new name is not printed.
* A file with no added slot prints no `[new slot]` line.

**Owning tests, found by searching what reads the touched code** (Boundary A): `test_upgrade.py::TestMerge`, `test_merge_module.py`, `test_install_module.py`, `test_first_session_report.py`, `test_quickstart_sequence.py`, `test_upgrade_module.py`, `test_upgrade_module_additions.py`, `test_verify_integrity.py`, `test_review_stance_in_shipped_files.py` and `test_security_leaf.py`. The implementer also searches the tests for any that expects non-ASCII text on a `[flag]` or review-only line. `test_ast_attest.py` fails until the re-anchor; that is expected and Maintainer-run.

**Smoke checks.** `python bootstrap/scaffold.py --config bootstrap/profiles/solo-greenfield.yml --target <scratch>`, then `python bootstrap/verify_integrity.py --target <scratch>` against the two lists; the upgrade reproduction repeated on the built code; `scaffold.py --manifest` before and after; `python scripts/claim_check.py` and `python scripts/check_cairn.py` on every changed Markdown file, run by a person (Cairn has no CI).

**Boundaries.** A: the tests above, plus the Bandit gate (`test_security_lint.py`, which skips when Bandit is missing; `python bootstrap/security_check.py` is the Maintainer-run release trigger) and the neutrality and redundancy gates (`python scripts/quality_gate.py --sub neutrality --sub redundancy`). B: full mode, because the scaffold engine is a named high-risk surface; the change's own record is scoped with `Certified by: pending`, and the full suite is the certifying run before a push, a re-anchor or a release. I run no full suite. C: the code reviewer verifies the record and runs targeted falsification, and reads the `except` clause and the import diff.

#### Security preflight — five questions, answered in writing

* **S1 — Who supplied it?** Decisions: which slots are added (B) and which are for absent modules (A). Inputs to B: the new template (Cairn's `templates/`, or a `--to <ref>` checkout; `src` is validated at `upgrade.py:195-225`), the saved old template (`dev/.cairn/base/`, in the project tree) and the adopter's file (already parsed strictly at `merge.py:200`). The lockfile's token values are an input to the merge, and they can add a slot name to the token-filled text (measured by the Security Review). The names are therefore read from the text before token values are filled in, and a token value cannot add one. The saved old template and the adopter's file can only remove names. This corrects the opening preflight, which said no input can add a name. Inputs to A: the installed module list (from the resolved profile) and the table; names printed come from the table only.
* **S2 — Can it fail?** B: delete the old-template subtraction and the deleted-slot test fails; subtract only the adopter's names and the same test fails; parse the token-filled text and the token-injection test fails. A: empty the table and the solo test fails; change "no supplier installed" to "not every supplier installed" and the test with one of five role-roster suppliers installed fails. A check that derives its expectation from its own table cannot fail, so the completeness and drift tests read slot names from the templates and module names from the shipped catalog. I have not run these mutations; there is no code.
* **S3 — What fires it, over what?** `python bootstrap/scaffold.py --config <profile> --target <dir>` for A, over the files that run wrote. `python bootstrap/scaffold.py upgrade --target <dir> --plan` or `--stage` for B, over every tracked mergeable file. The adopter-facing sentence ("new in this upgrade") is true only for `clean`, `clean-locally-modified` and `conflict` files; `UPGRADE.md` says what is not covered.
* **S4 — Which way does it break?** A: an unknown slot, a missing `modules` argument or any installed supplier lands in the main list, which is today's output. B: an unparseable old template, a parse error, a missing slot or a non-printing status prints no name, which is today's output. Neither path adds authority.
* **S5 — Who still wins?** Assumed attacker: someone who edits the project's lockfile, base copy or adopter file, or ships a crafted template. Still succeeds: a crafted template can print a misleading slot name, escaped but readable; a crafted base copy can hide a real added-slot line. Neither writes, reads a path or runs anything. Control characters from `detail` are closed by construction at one place: `_print_upgrade_report` escapes every `detail` it prints, so this covers the existing `[flag]` and review-only lines as well as the new one. Not covered here: `fp.dst` in those lines, a lockfile name with an invisible code point (`isprintable()` passes some; for the lockfile-path batch), and the install report's raw slot names, which come from Cairn's own templates at install time. Misleading text is closed only by enumeration, and only a human can judge it. The opening preflight's sentence that everything this report prints from the project is terminal-safe was false for the existing `[flag]` lines; it is withdrawn.

**For the plan's Internal Security Review:** SR1 to SR3 are adopted as written above and are checked in the code. SR4 (no top-level import added or changed) and SR5 (module names from the table only; `except SlotError` only) bind the plan.

### Independent scientific check

N/A: no scientific assumption or result touched.

### Signals the change is wrong

* **A slot in the second list that an installed module does fill** (the table has the wrong supplier). One such report means the table needs a second look at that slot, and the grouping is the first thing to cut.
* **A slot of an absent module that stays in the main list** (the table misses a supplier, as `documentation-tier-home` was missed). The completeness test should catch it when the placeholder uses the phrase it scans for; a report is the signal when it does not.
* **A `[new slot]` line for a slot the adopter deleted or already filled**, or for a name that is not in the new template's text.
* **Any line from this report carrying a byte outside printable ASCII.**
* **Adopters filling a named slot with `<!-- cairn:customized -->` to silence the line** (the board watch). If an adopter reports it, the wording is wrong, or the line should not exist.
* **The quickstart count test failing after an unrelated template adds a slot:** expected; the count is still pinned to output.
* **The re-anchor deriving more than four changed symbols, any NEW symbol, or a changed import note:** something else moved, and this proposal's accounting is wrong.

### Scope delta

**Scope delta**: degraded. Reduced against the archived Decision's wide wording; preserved against the board row. The baseline is the two board rows: classify the post-install report by the accepted profile, and name upgrade-added slots. Both are delivered as the board states them. Only the Maintainer concedes the reduction (Q2).

* The archived Decision's success wording, "a post-install report that asks only for live work" (`dev/proposals/archive/2026-08-20-claude-adopter-path-consolidation.md:1131`, `:1503`). Delivered in part: 2 of 22 slots on `solo-greenfield`, 0 of 23 on `collaborative-team`. The report still asks for the 2 slots the install fills itself, and the quickstart's "unfilled" stays 2 high. **disposition**: defer. Q2 offers (b) and (c); under the default a board row holds the second form of (c). Specifying it was rejected for the default because (b) can hide an unfilled slot and (c) either adds a read or moves pinned output.

Not in the baseline and not built: naming at `--apply` (Q3), and the `customized`-reflex mechanism (watched on the board).

### Assurance path

**Assurance path**: high-assurance, unchanged. The change edits the scaffold / merge engine, a named mandatory trigger, and it changes an adopter-facing report and an AST baseline. The header keeps `usual + Security Review`; the Security Review asks for no second proposal-stage pass, and the plan's `required(Internal + Internal Security Review)` stands. I wrote neither review.

### Withdrawn / superseded commitments

* **"Scope delta: preserved" and the In brief's "stops mixing slots ... into the list of work it owes".** Replaced by `degraded` with the reduction named, and by an In brief that carries the numbers. Why: F2.
* **Q2's single reason (the report would have to read the installed files) and its place after Q1.** Replaced by Q2 first, three options and a default. Why: F2.
* **The supplier table of six slots.** Replaced by seven slots, with `documentation-tier-home` added (two files). Why: F1.
* **The one-direction Signal and the table-to-template drift test as the only check.** Replaced by both directions in Signals and a completeness test that reads the templates. Why: F1.
* **"`merge_file` returns the same four-kind status."** Replaced by five statuses, names on `clean` and `conflict` only. Why: F5.
* **B.1: names computed from the token-filled templates, "escaped with `ascii()`" inside `merge_file`.** Replaced by names from the text before the token fill, inside `except SlotError`, returned unescaped and escaped where the report prints. Why: SR1, SR3.
* **No cap on printed names.** Replaced by 10 names, 80 characters each, then `(and N more)`, as literals inside `merge_file`. Why: SR2.
* **S1's "no input is supplied by the thing being decided about" and "no input can add a name".** Replaced by the corrected S1. Why: SR1.
* **S5's "everything printed from the tree goes through `ascii()`".** Replaced by escape at the print site, covering the existing `[flag]` and review-only lines, with what it does not cover stated. Why: SR3.
* **"A new top-level engine name would fail the AST check" as the whole accounting.** Replaced by that, plus the statement that no top-level import is added or changed and that the code reviewer checks the diff. Why: SR4.
* **The "What is lost" list without the rename, no-base-copy and `needs-value` cases.** Replaced by the longer list. Why: F3, F5, F6.
* **The Do-nothing cost "low and continuing".** Replaced by the numbers I have and a statement that adopter time lost is unmeasured. Why: F8.
* **The `cairn:if` rival's point (3) "every adopter's next upgrade merges the change".** Replaced by the measured `slot-removed` on every existing solo adopter. Why: F4.
