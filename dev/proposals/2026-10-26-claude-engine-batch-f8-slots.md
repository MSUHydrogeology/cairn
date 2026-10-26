# Engine batch: a post-install report that matches the profile, and an upgrade that names the slots it adds

**Author**: Claude (Strategy)
**Status**: revising
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
