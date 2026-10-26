# Code review -- engine batch: the install report by profile and the slots an upgrade adds (plan `engine-batch-f8-slots`) -- Claude Sonnet 5.5 (fresh session) -- 2026-10-26

**Model**: claude-sonnet-5-5 (Sonnet 5.5, fresh session; did not write or implement the plan)
**Tier**: Internal
**Reviewed range**: `65894797^..741b79ec`, only this plan's files. The plan's commits are C1 tests `e976524b`, C1 code `24400219`, C2 tests `dd9dcd19`, C2 code `47366b20`, C3 prose `62ade210`, C4 record `741b79ec` (it edits only the plan). Other sessions' commits in the range (`5e66c74d`, `fb45584e`, `cbaa999b`, `3b19a7df` and others) were separated with `git log --oneline 65894797^..741b79ec -- <paths>` and `git show --stat`, and are not judged here. Tested bytes: a detached worktree of `741b79ec`.
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13), `PYTHONDONTWRITEBYTECODE=1`. Everything that wrote ran in two detached scratch worktrees of `741b79ec` (one unmutated control, one for mutants) or in scratch install folders; no shared tree was run, and the full suite was never run (`CAIRN_FULL_SUITE` never set).
**Called by**: none (the plan's one code review; not an External read).
**Not reopened**: the Decision, the Maintainer's word that the raw prints at `install.py:1526`, `install.py:1706` (it was `:1668` when the plan was written) and `cli.py:359`, `cli.py:590` stay out, and the Security Review's P3 queue.

**Verdict: no blocking findings.** The code does what the plan says. The four symbols (`print_report`, `main`, `merge_file`, `_print_upgrade_report`) changed as written, every `detail` print site is escaped, the new `try` in `merge_file` wraps only the name reading, and the supplier table agrees with what I derived myself from the templates and with five real installs. I broke the code 39 ways; 34 breaks were caught by a test and 5 were not. None of the 5 is a defect in the code: each is a place where the test net is thinner than the plan says (F1 to F4). All are test-only fixes. Status moves to `ready-to-archive`; the implementer decides at archive preparation which of F1 to F4 to guard and which to decline.

Terms. A **mutant** is one deliberate break made to see whether any check notices: *killed* if a test failed on it, *survived* if every test still passed, *equivalent* if it changes no behavior. A **detail** is the note text a file's plan carries (a slot name, a git error) that the upgrade report prints. A **supplier table** is the literal inside `print_report` that says which module fills which slot.

## Foundations

1. **Does it really do what it claims?** Yes. On the built code, `upgrade --plan` and `--stage` print `[new slot] dev/README.md: <names>` for an added slot and print none for the quiet cases; every `detail` print is `ascii(...)[1:-1]`; and the install report on `solo-greenfield` reads 20 and 2 (total 22), `collaborative-team` 23 and no second list, matching what is on disk. Evidence: `python -m pytest bootstrap/tests/test_upgrade_added_slots.py bootstrap/tests/test_install_report_slots.py` in a clean detached copy of `741b79ec`: 33 passed (25 and 8, as the record says); the five installs and seven upgrade probes below.
2. **Is there a simpler or safer build?** The build is already close to the minimal one (no new top-level name, no import, two new test files). One safer change is optional and not mine to add: cap the older `[flag]` detail the way the new line is capped (see O1, an observation). Evidence: `git diff 65894797 741b79ec -U0 -- bootstrap/_scaffold/{install,cli,merge,upgrade}.py` adds no `import` or `from` line (control: the same search over the two new test files finds 23).
3. **What input or run breaks it?** I found none that breaks the code. What I tried: a malformed adopter file and a malformed old base through `--plan` and `--stage`; a slot name with ESC, a bidirectional override, 1 MB, 80 non-BMP characters; 100,000 added slots; a conflicting file plus an added slot; 40 mutants across all three escape sites and all caps. The tests failed on 34. The five that no test noticed are in the ledger and in F1 to F4. Evidence: falsification ledger below; probe results under rulings 2 and 3.

## Rulings on the seven attack points

### 1. The print sites (from the tree, then each escape mutated)

The set of `detail` and slot-name print sites in `bootstrap/_scaffold/`, listed from the tree (`grep -n "\.detail\|detail\b" bootstrap/_scaffold/*.py`, and `grep -n "slot" ... | grep "print\|f\""`), not from the diff:

| Site | What prints | In the plan? | State |
|---|---|---|---|
| `upgrade.py:892` | `[flag]` detail | yes | `ascii(fp.detail)[1:-1]` |
| `upgrade.py:897` | new `[new slot]` line | yes | `ascii(fp.detail)[1:-1]` |
| `upgrade.py:908` | review-only detail | yes | `ascii(fp.detail)[1:-1]` |
| `upgrade.py:596` | stores `res.detail` into the plan; no print | n/a | n/a |
| `install.py:1526`, `:1706`, `cli.py:359`, `cli.py:590` | module names / slot names from a profile | **excluded by the Maintainer** | raw, as the plan says |
| `install.py:1717-1718` (second list) | slot name and module names | yes | slot name comes from the table's own keys, module names from the table; never from the profile (mutant I6 and test `test_profile_module_name_with_bidi_character_is_absent_from_the_report`) |
| `cli.py:658`, `cli.py:661`, `install.py:320`, `install.py:1440` | slot names from Cairn's own templates (module-merge pass, warnings) | not named by the plan | raw; names come from the shipped templates, not from the adopter or a profile. Not this plan's; noted only |

The excluded set is exactly the four the plan names (the install report's raw print moved from `:1668` to `:1706` because C1 added lines above it). The three in-scope escapes were each removed in a separate copy (U1, U2, U3 in the ledger): all killed, by the printable-ASCII cases (`[flag]`, new line) and by `test_review_only_detail_is_escaped_when_printed`. A fourth variant, `ascii()` without the `[1:-1]` cut, was also killed (U9). **The escape reaches every member of its set**; the other lines the report prints either carry `fp.dst` (raw on every line, which the record names as the lockfile-path batch's) or fixed text plus integers (`drift`, from `_behind_by_n`, `lockfile.py:219-245`).

### 2. `merge_file`: the `try` and hostile templates

Read in the current tree (`merge.py:176-263`): the new `try` (`:232-239`) wraps `parse_slots(base_raw)` and `parse_slots(theirs_raw)` only. The strict parse of the adopter's file (`:211`) and of the token-filled new text (`:213`) stay outside it. Measured, through `scaffold.py upgrade` in scratch installs of `solo-greenfield`:

* **Malformed adopter file** (an unclosed slot appended to `dev/README.md`) with a new slot also added upstream: `--plan` and `--stage` both exit 0 and print `[flag] dev/README.md: malformed slots: unclosed slot 'opened-never-closed' (opened line 63)` and no `[new slot]` line. It reports `error`, never `clean`. Mutant G15 (parse the adopter file inside the new `try`) is killed.
* **Malformed old base** (an unclosed slot appended to the cached base copy) plus an added slot: `--plan` and `--stage` exit 0, the file's kind and the whole stdout are byte-identical to the parent commit `65894797` (1,159 and 1,247 bytes on both), and no name is printed. It fails toward today's silence, as the plan chose.
* **Hostile template, 4 names at once** (ESC `\x1b[2J` in a name, U+202E and U+2066 in a name, a 1 MB name, 80 non-BMP characters): the `[new slot]` line is 1,005 characters, contains no control or bidirectional character, and shows the 1 MB name cut to 77 characters plus `...`. Exit 0, 1.2 s.
* **100,000 added slots**: one line, `n0 ... n9 (and 99990 more)`, 140 characters, 0.9 s, exit 0.
* **12 names of 79 backslashes plus a digit**: the line is 1,706 characters (the plan said backslashes exceed the 1,200 figure, as its C2.5 states).
* Nothing raises inside the handler: `ascii()` takes any `str`, and `parse_slots` raises only `SlotError` (five `raise` sites, all `SlotError`, `merge.py:72-98`).

### 3. The install report

Derived the true slot-to-module pairs independently from the templates (`templates/core/AGENTS.md:420, 443, 468`, `templates/core/dev/agent_collaboration.md:343`, the two `_template.md` placeholders, `templates/modules/default-on/documentation-plan.md:19-21`, `bootstrap/BOOTSTRAP.md:418-427`; `role-roster-additions` and `coordination-additions` appear in no module file, only in `agent_collaboration.md` and `BOOTSTRAP.md`). They equal the table's seven rows, including `documentation-tier-home` in both `_template.md` files. The `model-selection` disagreement the code comment names is real (`BOOTSTRAP.md:418-420` lists it; `templates/modules/team-gated/model-selection.md:10-13` says it adds to `doctrine/roles.md`); the table follows `BOOTSTRAP.md`, the comment says so, and the failure direction is more work, not less.

Five installs into scratch folders, compared against my own expected set and the files on disk (modules read from the lockfile):

| Profile | Main heading / lines | Second heading / lines | Absent slots expected = shown | `verify_integrity` |
|---|---|---|---|---|
| `solo-greenfield` | 20 / 20 | 2 / 2 (`coordination-additions` <- `coordination-tiers`; `role-roster-additions` <- the five suppliers) | equal | rc 0 |
| `collaborative-team` | 23 / 23 | none | equal (none) | rc 0 |
| `high-rigor-legacy` | 23 / 23 | none | equal (none) | rc 0 |
| `solo-greenfield` + `modules_add: coordination-tiers, model-selection` | 22 / 22 | none | equal (none) | rc 0 |
| `solo-greenfield` - `claim-check`, `documentation-plan` | 16 / 16 | 6 / 6 (`claim-check`, `documentation-discipline`, `documentation-tier-home` x2, plus the two above) | equal | rc 0 |

In every case the main and second lists share no (file, slot) pair, together they equal the slot pairs in the installed files (the base copies under `dev/.cairn/base/` excluded), the closing "Mark each `N/A`" line prints once when a second list prints and not otherwise, and the supplier names printed equal my derived pairs. `modules` in `cli.py` is the same list the install and the module-merge pass use (`cli.py:592`, `:631`, `:645`), and `print_report`'s only callers are `cli.py:627` and tests; the new keyword defaults to `None`, so no other caller changes.

### 4. The AST claim

`python bootstrap/tests/_ast_attest.py verify bootstrap/tests/fixtures/scaffold_ast_baseline.json --known-new bootstrap/tests/fixtures/scaffold_ast_known_new.json bootstrap/_scaffold/*.py` (read only, 3.13.13) at `741b79ec` lists 10 CHANGED: the five of S0 (`_apply_upgrade`, `_behind_by_n`, `_resolve_vendor_wrapper`, `_self_heal_profile_config`, `cmd_upgrade`), the plan's four (`print_report`, `main`, `merge_file`, `_print_upgrade_report`) and `_write_init_lock_profile_template`; plus the three known-new digest mismatches (`_check_lockfile_paths`, `_contained_lockfile_path`, `_lockfile_refusal`). The fifth extra is not this plan's: `git show 5e66c74d` changes only that function. No new symbol: the diff adds no `def`, `class` or top-level assignment. No import line moved (search above, control found 23); the sorted `note: NEW Import` list has 36 entries, the same count the record gives. The implementer's accounting is right; the plan's "four CHANGED" is literally false for the reason the record states.

### 5. Frozen files, the quickstart count

`bootstrap/tests/fixtures/gate_manifest.json` `frozen_files` has 195 keys. The files this plan's commits modify or delete, from `git diff-tree --diff-filter=MDRT` over `24400219`, `47366b20`, `62ade210`, `741b79ec` (and the two plan-only commits), are `cli.py`, `install.py`, `merge.py`, `upgrade.py`, `docs/quickstart.md`, `CHANGELOG.md`, `bootstrap/UPGRADE.md`, `dev/plans/engine-batch-f8-slots.md` and, in `47366b20`, the plan's own new `test_upgrade_added_slots.py`. **None is a frozen key** (control: `test_quickstart_sequence.py` is a key, `upgrade.py` is not). `docs/quickstart.md` now says 20; a live `solo-greenfield` install reports `Block slots requiring agent attention (20)`; `test_quickstart_sequence.py`, `test_security_leaf.py`, `test_merge_module.py` and `test_slotmerge_leaf.py` pass unchanged (35 passed). No `grep "22 unfilled|22 block|(22)"` hit outside records and the changelog's own sentence remains. `SECURITY_MUTATIONS.md` was touched only by `5e66c74d` and `fb45584e` in the range. Lockfile: no edited file is a `dst` in `dev/.cairn/cairn-lock.yml` at `741b79ec` (control: the same grep for `AGENTS.md` finds 1).

### 6. Prose against the code

The `UPGRADE.md` text (lines 112-120 of the file at `741b79ec`) and the `CHANGELOG.md` entry say what the code does: the line prints under `--plan` and `--stage`, not `--apply` (the report function is called only from the stage and plan paths); none for a file new in the upgrade, a tree with no saved old template, a `needs-value` file, or a renamed filled slot (`slot-removed`); at most ten names then a count; non-ASCII and control characters shown as escapes, and neither says "ASCII prints unchanged". One small inexactness, not worth a revision: the list of "no line" cases omits a `slot-removed` file whose slot was removed without a rename, and an `error` file; both print none, and both are reported as flags. The changelog links the plan at `dev/plans/engine-batch-f8-slots.md`, which the archive commit repoints.

### 7. Neutrality

`python scripts/quality_gate.py --sub neutrality` in the control copy: `fail=0, info=41`, exit 0. The added lines of `UPGRADE.md`, `CHANGELOG.md`, `docs/quickstart.md` and the engine files contain no vendor or model name (grep, case-insensitive; control: the same pattern matches elsewhere in the tree). Redundancy `fail=1` at `scripts/repin.py` is another session's file, not judged.

## Findings

None blocking. Each is the reviewer's recommendation; the author decides. All are test-only, none touches an implementation byte, and each names the mutant that survived.

**F1 -- Nothing through the real command proves a conflicting file gets its `[new slot]` line. (Should fix; test only; non-blocking.)** Mutant U6 (the print filter drops `conflict`) survives all 33 tests. The code is right: I ran a README that both the adopter and the new template edit on the same line, plus an added slot, and both `--plan` and `--stage` print `conflict 1: dev/README.md`, `1 file(s) need conflict resolution before --apply.` and `[new slot] dev/README.md: brand-new-slot -- new in this upgrade. ...`. The `merge_file` level is pinned (`test_detail_is_empty_or_exactly_the_name_list_on_clean_and_conflict` kills G2); the print filter's `conflict` entry is not. *Satisfier (guard):* one test in `test_upgrade_added_slots.py`: edit the same README line in the adopter file and in the new release, add one slot, assert the `conflict` summary and the `[new slot]` line under `--plan`.

**F2 -- The "exactly ten names" and "exactly 80 characters" edges are not pinned. (Low; test only; non-blocking.)** Mutant G4 (`len(added) > 10` becomes `>= 10`) survives: with exactly ten added slots the line would end `(and 0 more)`. Mutant G7 (`len(n) <= 80` becomes `< 80`) survives: an 80-character name would be rewritten as 77 characters plus `...`. The code is right at both edges (`merge.py:240-243`); the tests use 11 or more names and names well over or well under 80. *Satisfier (guard):* one `merge_file` test with exactly ten added names (no `(and`) and one name of exactly 80 characters (printed whole) and one of 81 (cut to 77 plus `...`).

**F3 -- Nothing pins that the new `try` catches only `SlotError`. (Low; test only; non-blocking.)** Mutant G17 (`except SlotError` becomes `except Exception`) survives. It is not behaviorally different today, because `parse_slots` raises only `SlotError`, so I report it as a survivor, not as equivalent (no run distinguishes it, and I did not show it equivalent by a measured behavior). The plan's rule is "`SlotError` and nothing wider" (Rules, line 26). *Satisfier (guard):* one test that makes `merge_module.parse_slots` raise a `ValueError` on the second call (monkeypatch) and asserts `merge_file` propagates it, which fails a widened `except`. Or `wontfix`, with the reason that the rule text is a reading rule the next reviewer checks in the diff.

**F4 -- Add the supplier-table pin for an empty "live" list, or decline it. (Very low; non-blocking.)** Mutant I7 (`elif not absent_slots` becomes `else`) survives: with only supplied slots present and `modules=[]` the report would print `[OK] No block slots detected.` above a second list. A real install cannot reach this (core has at least 15 non-module slots), so no run through `scaffold.py` can tell. *Satisfier (guard or wontfix):* a direct `print_report` call in `test_install_report_slots.py` with only the seven supplied slots and `modules=[]`, asserting `[OK] No block slots detected.` is absent; or `wontfix` for unreachability.

**Note on the C1 mutants.** The implementer's four C1 mutants (in `24400219`'s commit body) were not re-run in the record. I ran ten against the tests (I1 to I9 and C1): nine killed, one survived (I7, F4). Nothing to do; stated so the next reader need not.

## Observations (not findings; no change recommended)

**O1 -- The older uncapped `[flag]` lines can now grow.** `slot-removed` and `error` details are uncapped (a name from the adopter's file or a duplicate name from the new template), and `ascii()` turns each non-BMP character into 10 characters. Measured: a duplicate-name error with two names of 128 Ki non-BMP characters printed a 1.31 MB line under `--plan` (about 0.5 MB raw before this change), exit 0, 0.5 s. The source is the adopter's own file or the release the adopter chose to install, so it is self-inflicted at worst, and the plan caps only the new line (Rules, line 27). If the Maintainer wants the flag lines bounded too, it is a separate small change on the security row; I recommend leaving it.

**Where the printed text comes from on the new line.** Names are read from `base_raw` and `theirs_raw` (the sized template text, before token fill), not from the token-filled copies: mutants G13 and G14 (parse the filled text, or the filled old base) are both killed, so a lockfile token value that carries a slot pair cannot add or hide a name.

## Falsification ledger

Method: control = a detached worktree of `741b79ec`; mutants = a second detached worktree of `741b79ec`. Each mutant is one exact-text replacement in one file, run once against the two new test files (`-x`, so the first failing node is shown), then the file is restored byte for byte from the saved text; a first run was discarded because a second copy of the harness wrote to the same worktree (its `NOAPPLY` lines and two false survivors were the interference); the numbers below are the clean, single run. Control (unmutated): **33 passed**. Probes and installs ran in the control copy. 40 mutants defined, 39 run, 1 pattern did not apply (I10, a scratch variant, not a mutant).

| # | Mutant (one break) | Result | Test that failed (first) |
|---|---|---|---|
| U1 | `[flag]` escape removed (`upgrade.py:892`) | killed | `test_every_flag_and_new_slot_line_is_printable_ascii[removed-filled-slot---plan]` |
| U2 | `[new slot]` escape removed (`:897`) | killed | `test_new_slot_line_stays_within_its_bound_for_names_that_escape_longest` |
| U3 | review-only escape removed (`:908`) | killed | `test_review_only_detail_is_escaped_when_printed` |
| U4 | new line also for `slot-removed`, `error`, `needs-value`, `review-only` | killed | `test_malformed_adopter_file_still_reports_error_never_clean` |
| U5 | new line drops `clean-locally-modified` | killed | `test_slot_the_adopter_deleted_is_not_named` |
| U6 | new line drops `conflict` | **survived** | none (F1) |
| U7 | new line prints when `detail` is empty | killed | `test_plan_and_stage_name_a_slot_the_upgrade_adds[--plan]` |
| U8 | new line drops plain `clean` | killed | same |
| U9 | `ascii(...)` without the `[1:-1]` cut at `[flag]` | killed | `test_every_flag_and_new_slot_line_is_printable_ascii[removed-filled-slot---plan]` |
| G1 | `merge_file` clean returns no names | killed | `test_plan_and_stage_name_a_slot_the_upgrade_adds[--plan]` |
| G2 | conflict returns no names | killed | `test_detail_is_empty_or_exactly_the_name_list_on_clean_and_conflict` |
| G3 | 11 names | killed | `test_new_slot_line_states_how_many_more_slots_it_left_out` |
| G4 | `(and N more)` at `>= 10` | **survived** | none (F2) |
| G5 | cut at 81 | killed | `test_new_slot_line_names_at_most_ten_names_of_at_most_eighty_characters` |
| G6 | no cut | killed | same |
| G7 | cut when `< 80` | **survived** | none (F2) |
| G8 | cut keeps 80 plus `...` | killed | same as G5 |
| G9 | no `(and N more)` | killed | `test_new_slot_line_states_how_many_more_slots_it_left_out` |
| G10 | `(and N more)` off by one | killed | same |
| G11 | drop the old-base subtraction | killed | `test_slot_the_adopter_deleted_is_not_named` |
| G12 | drop the adopter subtraction | killed | `test_slot_the_adopter_already_has_is_not_named` |
| G13 | names read from the token-filled new text | killed | `test_lockfile_token_value_carrying_a_slot_pair_adds_no_name` |
| G14 | old names from the token-filled base | killed | `test_lockfile_token_value_in_the_old_template_hides_no_name` |
| G15 | adopter-file parse swallowed (`SlotError` caught, `our_slots = []`) | killed | `test_every_flag_and_new_slot_line_is_printable_ascii[malformed-adopter-file---plan]` |
| G16 | strict parse of the token-filled new text swallowed | killed | `test_token_value_that_breaks_the_new_text_still_reports_error` |
| G17 | the new `try` catches `Exception` | **survived** | none (F3) |
| G18 | the new `try` catches nothing (so a malformed base raises) | killed | `test_malformed_old_base_keeps_its_status_and_prints_no_name` |
| G19 | an unparseable base yields every new-template name | killed | same |
| G20 | names also on `needs-value` | killed | `test_needs_value_slot_removed_and_error_carry_no_names` |
| I1 | supplier test `any` becomes `all` | killed | `test_team_profile_keeps_live_module_slots_in_main_list` |
| I2 | `modules` ignored | killed | `test_minimal_profile_lists_absent_module_slots_separately` |
| I3 | `documentation-discipline` under the wrong module | killed | `test_every_slot_that_says_filled_from_a_module_is_in_the_supplier_table` |
| I4 | `documentation-tier-home` row dropped | killed | `test_removing_a_module_moves_every_slot_it_fills` |
| I5 | `model-selection` dropped from the roster suppliers | killed | `test_minimal_profile_lists_absent_module_slots_separately` |
| I6 | module names printed from the profile's `modules` | killed | same |
| I7 | `[OK] No block slots` branch whenever the main list is empty | **survived** | none (F4) |
| I8 | second heading counts the main list | killed | `test_minimal_profile_lists_absent_module_slots_separately` |
| I9 | `coordination-additions` gets an extra module | killed | same |
| I10 | scratch variant (escape on the table's slot name) | not run (pattern did not apply) | n/a |
| C1 | `modules=` not passed from `cli.main` | killed | `test_minimal_profile_lists_absent_module_slots_separately` |

**34 killed, 5 survived (U6, G4, G7, G17, I7), 0 equivalent, 1 not run.** Of the survivors, U6, G4 and G7 were shown *not* equivalent (U6 by the end-to-end conflict probe, which prints a line the mutant would not; G4 and G7 by reading the changed output). G17 and I7 are reported as survivors because I did not measure a behavior difference through the real entry point (G17 has none in today's `parse_slots`; I7 has none reachable from an install).

Other evidence: the unmutated control run, the five installs (ruling 3), seven upgrade probes (ruling 2: malformed adopter file, malformed base, hostile names, 100,000 slots, backslash names, conflict plus added slot, hostile flag lines: ESC and U+202E inside an adopter's unclosed slot name print as the escapes `\x1b` and `\u202e` with no control character in stdout), the AST `verify` (ruling 4), the frozen-key derivation (ruling 5), `quality_gate --sub neutrality` (ruling 7).

## Verification record, checked against the range

The record's mode is `full` and `Certified by: pending`; I checked the parts of it that bear on the reviewed bytes. The tested commit `62ade210` and the range's last engine commit coincide (`741b79ec` edits only the plan, `git show --stat`). The 33 of the record's 1,178 that I re-ran are 33 passed, as recorded (25 and 8). Its S0 and S1 reproduce (ruling 4). Its "`scaffold.py --manifest` byte-identical" and "`SECURITY_MUTATIONS.md` has two hunks, both from other sessions" agree with `git log` (`5e66c74d`, `fb45584e`, `cdc02063`; the third is a `SAFETY.md` commit that is not this plan's). Its owner search: my wider search (`grep -lE "print_report|Block slots|slots requiring|unfilled block|\[flag\]|merge_file|_print_upgrade_report|MergeResult"` over `bootstrap/tests`) finds 11 files the record's 21-file set also covers or that match only a comment ("supplied by": `_gate_manifest.py`, `_oracle_trust.py`, `test_content_scan.py`, `test_security_net.py`), so I found no reader the record missed. Not independently re-run: the other 19 test files of the 1,178.

## Bounding

**Bounding**: ACCEPTED

The record claims no bounded mode: it states `Boundary B mode: full`, `Certified by: pending`, and no `CAIRN_FULL_SUITE`, which is what `AGENTS.md` asks for the scaffold engine. I challenged the stated omission "the full suite was not run" (it stands, because the next certifying run owes it) and the 21-file mapping (the owner search above finds no missing reader). One consequence for the author: if any of F1 to F4 is guarded, a test byte changes, which invalidates the record under the Boundary C rule; the next certifying run (before the push or the re-anchor) is the evidence, and a fresh scoped re-run of the two new test files is enough for the commit that adds them. This review did not run the full suite.

## Lenses used, with evidence

1. **Claims.** Every cited line opened in the tree: `merge.py:176-263`, `upgrade.py:846-911`, `install.py:1603-1722`, `cli.py:627-631`; the record's moved cites (`merge_file` `:176`, print sites `:892`, `:897`, `:908`) hold. Line cites in the review resolve; `python scripts/claim_check.py` and `python scripts/check_cairn.py` were run on this file.
2. **Production path.** Both new test files go through `scaffold.py` (`run_scaffold`, `_install`); the two direct calls (`_merge` and `_print_upgrade_report` with a `FilePlan`, `print_report` for the no-`modules` case) have stated reasons (plan C2.6, C1.3). The `conflict` print path is not exercised through the command (F1).
3. **Design completeness.** Empty, one, ten, eleven, 100,000 names; 1 MB name; malformed adopter, base and new text; no base; renamed slot; conflict; needs-value; five profile shapes. The two edge counts at the caps are untested (F2).
4. **Silent failure.** A malformed old base prints no name and no hint that names could not be computed (it fails toward today's output, as the plan chose); the strict parses still raise (G15, G16 killed).
5. **Cross-document consistency.** `grep` for the old figure 22 and for "unfilled block slots" finds `docs/quickstart.md` (now 20, pinned by the frozen test) and the changelog's own sentence; `BOOTSTRAP.md:418-427`, the placeholders and `model-selection.md:10-13` agree with the table and its comment.
6. **Drift.** `UPGRADE.md` and `CHANGELOG.md` match the measured behavior (ruling 6); the quickstart sentence is accurate, though its next sentence ("This recipe leaves them") now reads as if "them" were the 20 plus 2.
7. **Lifecycle / process placement.** The plan's C5 (AST and gate re-anchor) stays the Maintainer's; the changed-symbol set is as ruling 4 gives it. No new commit, status or board edit by this review beyond the plan's Status line.
8. **Scope.** No expansion: four symbols, two new tests, three prose files. The Out-line print sites are untouched, as the Maintainer decided.
9. **Name the satisfier.** Each finding above names one (a test to add, or `wontfix`).

## Coverage

**Covered:** every acceptance criterion's code path by reading the diff and the tree; the three escape sites and all caps by mutation; the report against five real installs; the upgrade against seven hostile or edge scenarios under `--plan` and `--stage`; AST, import, frozen-file and manifest claims by derivation. **Not covered / low confidence:** the full suite and any certifying run (by rule); the other 19 test files of the record's 1,178; `--apply`, `--to <ref>`, `--adopt-collisions` and `--adopt-module` with a changed template (the report function is called only from the stage and plan paths, `upgrade.py:2838`, `:2866`); a real terminal, a Windows console and a localized `git merge-file` message (checked on captured text); module files that themselves carry slots (the report counts them like any other); the lockfile-path batch's handling of a hostile `dst` (the new line prints it raw, as every line does); `scaffold.py --manifest` byte comparison and `_gate_manifest.py verify` (read from the record, not re-run); whether the plan's C2.5 length arithmetic holds beyond the five measured cases. The probes used scratch folders under the scratchpad and two detached worktrees, removed afterward.
