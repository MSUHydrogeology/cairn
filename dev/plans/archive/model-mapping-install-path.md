# Plan: the model mapping on every install path -- a notice where agents install, a check that is right both ways, and a write that cannot escape

**Source proposal**: `dev/proposals/archive/2026-10-18-claude-model-mapping-install-path.md`
**Status**: archived
**Plan review**: required(Internal + Internal Security Review)
**Assurance path**: high-assurance -- inherited: the change edits the scaffold engine (`bootstrap/_scaffold/`), a script every adopter runs verbatim, and the onboarding seeds written into preset adopters' `dev/PLANNING.md`
**Opened**: 2026-10-18

## In brief

**The problem.** Cairn asks a project to record which AI model plays each of three roles: high, medium and low capability. The record is a small file, the *mapping* (`dev/.cairn/model-selection-mapping.yml`). The install creates it as a placeholder, the *stub*, in which every field reads `FILL ME`. A short script, the *check* (`scripts/check_model_selection.py`), fails while any placeholder remains. Cairn's own mapping sat on the stub for four months, the check failing the whole time, and nobody saw. Four holes allowed it:

1. **An agent installing has no keyboard,** so Cairn skips its questions, and it said nothing at all. That is how agents install.
2. **Nothing runs the check.** Cairn has no automated test service, so it runs only when a person or agent remembers.
3. **The check is wrong in both directions.** It fails a mapping that was filled correctly if the stub's explanatory comments were left in, and it passes a file that has no rows at all.
4. **`upgrade` and `--adopt-module` never mention the mapping.** The stub reached the Maintainer's other project that way.

A fifth, found on the way: the step that writes the answers has no protection against a *link*. A link (symlink) is a file that points at another file. If the mapping were one, the answers would be written into the file it points at, outside the project. A related flaw, found while planning: the code that commits Cairn's own install record (`_commit_lock_and_caches`) writes through a temporary file whose name anyone can predict, so a *hard link* (a second name for an outside file) planted at that name would receive the record. The Maintainer folded its fix into this plan, and then the four other functions that write the lockfile in place, which share the flaw, and the lockfile reader, which follows a link and would hang on a pipe. The same is true of the function that appends ignore lines to a project's `.gitignore` on every install, stage and adopt (`seed_gitignore`): it rewrites the file in place, so a racing program or a hard link can send the lines into an outside file, and the check added to it by the recent `.gitignore` repair makes a `.gitignore` that is not UTF-8 stop an upgrade that would have added nothing. Those three small points were folded in too.

**What this plan does,** in five chunks (C1 to C3 and C5 land as one commit each; C4 may land as up to five):

* **C1, the check.** Comments no longer count as placeholders, a mapping needs at least one row, and with PyYAML (a common but optional Python library) the check also reads the values the way YAML does, so a placeholder hidden by clever spelling is still found. It refuses YAML's merge keys, which no mapping needs and which can make the reader run for minutes.
* **C2, the words and the reminder.** The stub's example says to name a model *family* and never a version. A "Filling the mapping" paragraph joins the module document. The installer's acceptance checklist (II-5) gains one item asking that the check pass. Two presets (`collaborative-team`, `high-rigor-legacy`) seed a row, `**Waiting on Maintainer**: fill the model mapping`, which `python tools/board.py --maintainer` lists on day one.
* **C3, the notice on install.** A fixed notice prints on every install, including one run by an agent, while the mapping is unfilled. It tells the agent to ask the Maintainer which model family fills each tier, and not to guess.
* **C4, the safe writes.** One careful way to write a file, built once (create a fresh temporary file in the same folder, keeping only the old file's read and write permissions, then rename it over the target), and used by seven writers: the interactive capture, the function that commits Cairn's install record (`_commit_lock_and_caches`), the four other functions that write the lockfile, and the `.gitignore` append. No link, hard link or racing program can redirect those writes into an outside file. The capture also refuses a link before it asks anything. The lockfile reader follows no link and never hangs on a pipe. The `.gitignore` check no longer reads the file.
* **C5, the notice on adopt and upgrade.** `--adopt-module` and `upgrade --plan`, `--stage` and `--apply` print the same notice. `--apply` prints it only after the apply succeeded, which is the run that delivers the stub to a project that predates it.

**What it costs the Maintainer.** Nothing is pushed, and no re-anchor is performed by an implementing agent. Two ceremonies are owed, both the Maintainer's, and **they run in this order: the AST correction first, then the gate-manifest re-anchor once.** The AST correction writes one of the frozen files, so a re-anchor run before it would have to be run again.

* The *AST correction*: the engine's fingerprint file records the exact shape of each engine function. This plan changes eleven engine functions and adds five (none is on the list an agent may repair itself; the exact lists are under *Frozen files, AST and the oracle*), so it is a Maintainer-run correction. You chose **one combined ceremony, later**: no separate correction for the `.gitignore` repair. It runs once, after this plan archives, for the repair's changed functions and this plan's together. The ceremony works the list out from the code, and no agent hands the Maintainer figures to paste (chunk M).
* The *gate-manifest re-anchor*: six *frozen files* (files whose exact bytes the gate manifest records) change, a seventh is written by the AST correction, and one pinned test node leaves on purpose, because you reversed the rule it pinned. The queued row on `dev/PLANNING.md` carries these.

One adopter-visible cost, accepted at the Decision: a project whose stub header was rewritten (LHM is one) meets one merge conflict at its next upgrade, and keeping its own side resolves it.

**How we will know it worked.** Each of these is a test that fails if the property is broken, and a mutation run (a deliberate break made to see whether any test notices) confirms it:

* a no-terminal install prints the notice and exits 0; a filled mapping, or a project without the module, gets silence;
* a hand-filled stub with its comments left in passes the check, and a mapping with no rows fails it;
* the engine and the check agree, line for line, on 108 generated awkward files and on a table of named spellings;
* a mapping that is a link, or sits behind one, is refused before any question, and the file it points at is byte-identical afterwards;
* a hard link planted at the install record's old temporary name no longer redirects the write, and the test is shown red before the fix;
* a file the installer swaps in never carries an execute or setuid bit over from the file it replaces;
* the four other functions that write the lockfile never write through a hard link, and the lockfile reader neither follows a link nor hangs on a pipe, each shown red before the fix;
* a `.gitignore` that is a hard link, or is swapped for a link at the last instant, is never written through, and a `.gitignore` that is not UTF-8 no longer stops an upgrade or loses its bytes;
* Cairn's own mapping passes its own check, and the test fails if it returns to the stub;
* `python tools/board.py --maintainer` lists the seeded row on a fresh install from either preset.

**Terms.** *Mapping*, *stub*, *check*, *link* and *frozen file* are defined above. *Non-interactive* means an install run with `--non-interactive` or without a terminal on standard input, which is how an agent's shell runs. *Containment guard* is the engine's refusal to write through a link or outside the project (`_assert_safe_write`). *Boundary A, B and C* are the three verification jobs in `AGENTS.md`: scoped checks while building, one integration run on a clean commit, and the code reviewer's independent attempt to break it. *Bare path* means the check running without PyYAML.

## Source proposal

Accepted 2026-10-18 at `7f1bcdf0`. Revision 2 binds over Revision 1 where they differ. The Security Review (`3c133398`, SEC-1 to SEC-8) cleared its blocking findings in the closure pass (`0f61d81f`, CL-1 to CL-4); SEC-3 to SEC-8 and CL-1 to CL-4 are carried into this plan, and its Internal Security Review checks them (*The security findings ledger* below). The Decision's words were "accept as answered", and the Maintainer's answers, each the recommended option, bind this plan:

* **Q1, the check:** "Yes to both". It skips full-line comments, and a mapping with no rows fails.
* **Q2, Scope delta:** "Allow two presets". The seed goes in `collaborative-team` and `high-rigor-legacy`, not `solo-greenfield` (*Scope delta* below).
* **Q3, the Waiting row:** "Yes". Fresh installs from those two presets seed the `**Waiting on Maintainer**` row.
* **Q5, the stub example:** "Yes, edit it". The example block says to name a model family, never a version. The Maintainer's direction, recorded in `47b38074`, is "Versions should not be named here, rather the latest version should be used". The accepted cost is one merge conflict for an adopter whose stub header was rewritten.
* **Q4, onboarding prompts in goodnight:** not part of this contract. It is carried as a board item at archive (*Dispositions*).

The plan executes the accepted text. It does not re-argue it. Four further answers came after the plan opened and are recorded under *Scope* (*Answered by the Maintainer after the plan opened*): the install-record fix and the three `.gitignore` points are folded in, the AST correction is one combined ceremony later, and the build order.

## Scope

Measured at `72434d73`, the HEAD when this plan was written.

**Touched.**

| Surface | Files | Chunk |
|---|---|---|
| The check | `templates/modules/team-gated/check_model_selection.py` and its byte-identical copy `scripts/check_model_selection.py`; `bootstrap/tests/test_model_selection_stub.py` | C1 |
| Words and seeds | `templates/modules/team-gated/model_selection_mapping_stub.yml` (the example block only); `templates/modules/team-gated/model-selection.md` and its byte-identical copy `dev/modules/model-selection.md`; `bootstrap/BOOTSTRAP.md` (II-5 and the vendor-neutrality list inside it); `templates/onboarding/collaborative-team.md`, `templates/onboarding/high-rigor-legacy.md`; `bootstrap/tests/test_onboarding_seed_roster.py` | C2 |
| Install notice | `bootstrap/_scaffold/install.py` (`_mapping_is_unfilled`, `model_selection_notice_lines`), `bootstrap/_scaffold/security.py` (`_read_regular_bytes`), `bootstrap/_scaffold/cli.py`; one comment in `bootstrap/_scaffold/lockfile.py`; `bootstrap/tests/test_security_leaf.py`; `test_model_selection_stub.py` | C3 |
| The safe writes: the capture, the install-record committer, the other lockfile writers and the lockfile reader, the `.gitignore` append | `security.py` (`_stage_exclusive`, `_write_by_replacing`); `install.py` (`capture_model_selection_mapping`, `seed_gitignore`, `write_install_lockfile`), `cli.py`; `bootstrap/_scaffold/upgrade.py` (`_commit_lock_and_caches`, `_cmd_init_lock`, `_cmd_finalize_lockfile`, `_apply_upgrade`'s lockfile write, and the remedy sentence of the `.gitignore` refusal where the repair put it); `bootstrap/_scaffold/lockfile.py` (`read_lockfile`); `bootstrap/_scaffold/SECURITY_MUTATIONS.md` (additions only); `bootstrap/SAFETY.md` (one sentence); `bootstrap/tests/test_security_leaf.py`; `bootstrap/tests/test_upgrade_module_additions.py`; `bootstrap/tests/test_intents_tool.py` (phase-mutable); `test_model_selection_stub.py` | C4 |
| Adopt and upgrade | `bootstrap/_scaffold/upgrade.py`; `test_model_selection_stub.py` | C5 |
| Cairn's install record | `dev/.cairn/cairn-lock.yml`: two records, `scripts/check_model_selection.py` (C1) and `dev/modules/model-selection.md` (C2) | C1, C2 |
| Board and changelog | `dev/PLANNING.md` (the opening commit joins the re-anchor row; the archive commit adds the node note and the deferrals); `CHANGELOG.md` (the archive commit) | opening, archive |

**Not touched,** each checked by `git diff --stat` over the implementation range (C6): `bootstrap/_scaffold/config.py` and `slotmerge.py`; `lockfile.py` apart from its comment and `read_lockfile`; `bootstrap/scaffold.py`; Cairn's own filled mapping `dev/.cairn/model-selection-mapping.yml`; `tools/session.py` and `templates/skills/_lib/session.py`; `scripts/_onboarding/`; `templates/onboarding/solo-greenfield.md`; Cairn's own onboarding slot in `dev/PLANNING.md` and its installed preset copy `dev/modules/onboarding/collaborative-team.md` (the lockfile does not track it, and it already differs from the template); the profile schema; the gate-manifest fixture; and the two AST fixtures, which only the Maintainer writes (*Frozen files, AST and the oracle*).

**Dry runs and other upgrade actions.** `scaffold.py --dry-run` returns before any module file is written, so it stays silent. `upgrade --init-lock`, `--finalize` and `--adopt-collisions` stay silent too: the accepted text names install, `--adopt-module` and `--plan`, `--stage` and `--apply`, and nothing else.

### Answered by the Maintainer after the plan opened

On 2026-10-18 the Maintainer answered four questions in chat, by multiple-choice, relayed by the coordinating session. The exact wording of each question is not reproduced here, because I did not see it; the chosen options are quoted verbatim.

1. **The hard-link defect in the install-record writer (`_commit_lock_and_caches`), found while planning.** I had carried it as a deferral. He was asked whether to fold it into this plan, and chose:

   > "Fold into this plan (Recommended)"

   with the option text he was shown:

   > "Same fix, same chunk, same AST correction. The plan's two reviews (including Security) see it before any code is written. Adds one engine function to your eventual AST re-anchor."

   **So it is accepted scope, an addition at the Maintainer's instruction.** The function writes the lockfile and the base-template caches through a temporary file with a **fixed** name beside each target. A hard link planted at that name passes the guard, and the write goes through to the file the link points at. Measured in a scratch tree: a hard link at the lockfile's temporary name, pointing at an outside file, left that file holding the lockfile's text. The fix is the mechanism the capture uses, exclusive creation (here `os.open` with `O_CREAT | O_EXCL` under a random name; P13). It lands in **C4**, beside the capture, with its own criteria, tests and mutants. It adds no top-level symbol. The function is pinned by digest in `scaffold_ast_known_new.json`, so the ceremony sees it as a re-keyed symbol (*Frozen files, AST and the oracle*). The function has two callers, found by search: `_cmd_adopt_module` and `_cmd_adopt_collisions`. **It is one of five functions that write the lockfile.** This folds in that one only; the other four, and the lockfile reader, are *Found while planning* and wait on the Maintainer's answer.

2. **When the AST correction runs.** He chose:

   > "One combined ceremony later"

   So there is **no separate re-anchor for the `.gitignore` repair.** Chunk M re-anchors everything at once, after this plan archives: the repair's CHANGED functions (four at the time of writing, `main`, `seed_gitignore`, `_cmd_adopt_module` and `cmd_upgrade`, and a fifth, `create_dev_tree`, if the repair's pending answer has landed), this plan's own delta (including the install-record function) and its NEW functions. The ceremony derives the list; this plan does not fix it.

3. **The build order.** He chose:

   > "Board-as-basis first (Recommended)"

   The order is `neutrality-and-upgrade-slots`, `independent-scientific-check`, `review-stance-and-lenses`, `board-as-basis`, this plan, then the `stewardship-and-reuse` plan (*Sequencing with the other plans*).

4. **The three small `.gitignore` points from the Security Review of the `.gitignore` repair.** The coordinating session asked him, in these words:

   > "Should the three small `.gitignore` points (the 0.1 ms race, hard links, and a non-UTF-8 `.gitignore` stopping an upgrade) join the model-mapping plan too? I recommend yes, so the reviewers see them before any code exists. If you say yes, I'd include the merge conflict file as well, since it's the same hard-link class and the same fix."

   He answered:

   > "Yes, fix the .gitignore points"

   **So all three are accepted scope, an addition at the Maintainer's instruction.** They are findings GS-SR-3, GS-SR-4 and GS-SR-5 of `dev/plans/archive/2026-10-18-security-review-gitignore-seed-guard.md` (`c00e6ddc`), all in `seed_gitignore` in `bootstrap/_scaffold/install.py`:

   * **GS-SR-3, the gap between check and write.** About a tenth of a millisecond sits between the guard and the write. In that review a racing thread won 99 of 3,000 calls, and a win overwrites the outside file instead of appending to it.
   * **GS-SR-4, a hard-linked `.gitignore`.** The guard checks symbolic links, not link counts, so a `.gitignore` that is a second name for an outside file is still written through on install, stage and adopt.
   * **GS-SR-5, the early check reads the file.** The repair's preflight runs the whole function with no entries, so a `.gitignore` that is not UTF-8 (or is a folder) stops install, stage and **apply**, including an apply that would add no line. The review rates it informational ("robustness, not security") and says the repair introduced it. The coordinator's question called it a regression; those were not the Maintainer's words, and his answer was only the sentence quoted above.

   The fix uses the same mechanism as the capture and the install-record writer: the new content goes to an exclusive temporary file and is renamed into place, so nothing is ever written through the existing name (P14, P15). It lands in **C4** with its own criteria, tests and mutants. It adds no top-level symbol of its own: `seed_gitignore` is already CHANGED by the repair and changes again. **Not included,** because his answer named only the `.gitignore` points: the module-merge conflict side-file in `slotmerge.py`. The coordinator's question offered it, and the answer did not take it, so it stays a named deferral at archive (*Dispositions*).

5. **The four other lockfile writers and the lockfile reader.** After both plan reviews, the Maintainer was asked, in the coordinating session's words:

   > "The lockfile has four more writers with the same hard-link weakness the plan fixes for one writer. The code that reads the lockfile also follows links, and would hang on a special pipe file. Should these join the model-mapping plan? I recommend yes: they'd use the same mechanism the Security reviewer just stress-tested, they'd go in the same chunk, with your combined AST ceremony, and they'd still get the plan's code review and Security Review when built. The alternative is a separate small repair later."

   He answered:

   > "Yes, fold them into the plan"

   **So they are accepted scope, an addition at the Maintainer's instruction.** The writers are `write_install_lockfile` (`install.py`), `_cmd_init_lock`, `_cmd_finalize_lockfile` and `_apply_upgrade`'s lockfile write (`upgrade.py`). Each gets the exclusive-temporary-file-then-rename mechanism, with the permission fix of MM-SR-1, through the shared helper (P17, P18). The reader is `read_lockfile` (`lockfile.py`), which `_commit_lock_and_caches` calls first; it gets the descriptor-based bounded reader (P16). All of it lands in **C4 (d)**. **These functions are new to the plan since its reviews: neither the Internal review nor the Internal Security Review read their design,** because both ran before the answer. The implementation's code review and Security Review are therefore told to cover each one explicitly (C6). Not included, because the answer named only these: the base-cache writes in `write_install_lockfile` and `_apply_upgrade`, `_apply_upgrade`'s swap writes, `_write_stage`, `_install_one` with `--force`, the profile writes and the module-merge conflict side-file. Those are the wider in-place class, named in *Named residuals* and *Dispositions*.

### What the exit codes are now (re-derived from the code at `72434d73`)

The proposal's exit-code text predates the `.gitignore` repair, and the repair changed it twice. `b8a402c6` wrapped all of `main` in one catch that returned 2. `fde3054c` withdrew that wrapper, because the differential oracle pins the traceback and exit 1 of every other install-time refusal. What stands now is three small preflights plus the older local catches. Every row was read in the code; the install and `--adopt-module` rows were also run in a scratch tree.

| Where | Refusal | What prints | Exit |
|---|---|---|---|
| install (`main`) | a linked `.gitignore`, asked before the first write, dry run included | `error: .gitignore seed refused (containment): ` and **the exception text** (the repair's pending answer adds a remedy line after it) | 2 |
| install | the skills fan-out | `error: skills fan-out refused (containment): ` and the exception text | 2 |
| install | the onboarding install | `error: onboarding install refused: ` and the exception text | 2 |
| install | **every other containment refusal**: a linked `AGENTS.md`, a linked `dev/.cairn` (stops at the first write that guards it) | a traceback ending `ScaffoldSecurityError` | **1** (the oracle pins this) |
| `upgrade --adopt-module` | a linked `.gitignore`, before anything is recorded | the `.gitignore` line, with the exception text | 2 |
| `upgrade --adopt-module` | every other containment refusal (a linked `dev/.cairn`: run and confirmed) | a traceback | **1** |
| `upgrade --apply`, `--stage` | a linked `.gitignore`, before any write | the `.gitignore` line | 2 |
| `upgrade --apply`, `--stage` | a refusal inside `_apply_upgrade` or `_write_stage` | `error: upgrade --apply refused (containment): ` or `--stage`, and the exception text | 2 |
| `upgrade --adopt-collisions` | a refusal | `error: upgrade --adopt-collisions refused (containment): ` and the exception text | 2 |
| `upgrade --plan`, `--finalize`, `--init-lock` | none is caught | a traceback | **1** |
| any command that reads the lockfile (new with C4 (d)) | the lockfile is a link, a folder or a pipe: refused by the reader, not followed or opened blindly | a traceback ending `ScaffoldSecurityError` | **1** (the same class the oracle pins) |
| `_apply_upgrade` itself | its own refusals (leftover conflict markers, a dirty tree) | an error line | 1, returned |

So the chain is: there is **no single catch**; each caller that wanted a clean exit catches where it chooses, and everywhere else a refusal ends in a traceback and exit 1. Two further facts matter. First, **no refusal line is fixed text**: all of them append the exception text, which names the path the tree chose, and `_assert_safe_write`'s third wording ("outside the target directory") names a resolved link target. Second, this plan adds one catch (the capture's, in `main`), and it prints a constant.

**Where the proposal's text is stale,** said plainly:

* **CL-2** says `main` wraps the whole CLI in one catch, that the capture call moved into a `_run_cli` function, and that `SECURITY_MUTATIONS.md` lines 12-13 are true as they stand. None of it holds at HEAD. There is no wrapper and no `_run_cli`; the capture call is back in `main` (`bootstrap/_scaffold/cli.py:666`).
* **SEC-4 and Revision 2** say `main` catches two refusals. It catches three today, and four after C4.
* **`SECURITY_MUTATIONS.md` lines 12-13** say the guards' error is "caught once at the CLI top level (exit 2)". That is false again, so the correction Revision 2 asked for was owed. **The repair's pending answer now writes it** (the true story, and the list of its catches), without the capture, so C4 adds only the capture's own catch (a constant line, exit 2) to that paragraph and rewrites nothing the repair owns.
* **The "fixed refusal line"** the entry brief and Revision 2 imply is a fixed prefix followed by exception text. Only the capture's new line is constant.
* **Revision 2's claim that a linked `dev/.cairn` stops early with a traceback and exit 1** is still true, and it was re-run. *Where* it stops moves: at `72434d73` it is `write_local_env`; with the repair's pending `create_dev_tree` guard it is `create_dev_tree`, earlier still. Traceback and exit 1 either way.
* **The AST count.** Revision 1 says "4 CHANGED, 2 NEW" against a baseline that was clean. The baseline is not clean now; see below.
* **The entry condition holds:** `seed_gitignore` is in `_GUARDED_WRITE_FUNCS` (`bootstrap/tests/test_security_leaf.py`) and has a Class A row in `SECURITY_MUTATIONS.md`. C1's gate re-reads both at its parent.

### Frozen files, AST and the oracle

**Frozen files: seven, measured.** Read from `bootstrap/tests/fixtures/gate_manifest.json` > `frozen_files` (183 keys) and intersected by script with every file this plan edits. The instrument was checked against a known key (`bootstrap/tests/test_scaffold.py` is reported frozen). The seven are six edited by an agent and one written by the AST ceremony:

* edited by an implementing agent (the six): `templates/modules/team-gated/check_model_selection.py`, `scripts/check_model_selection.py` (C1); `bootstrap/tests/test_model_selection_stub.py` (C1, C3, C4, C5); `bootstrap/tests/test_onboarding_seed_roster.py` (C2); `bootstrap/tests/test_security_leaf.py` (C4); `bootstrap/tests/test_upgrade_module_additions.py` (C4; it already holds the install-record writer's atomicity test, and 37 nodes of it are pinned);
* written by the Maintainer's AST ceremony (the seventh): `bootstrap/tests/fixtures/scaffold_ast_known_new.json`. The proposal's table lists it as touched. It is, but only the Maintainer-run correction may write it, because no symbol here is allowlisted; the repair that preceded this plan left its new symbol for the same ceremony. This is a sequencing fact, not a reduction: the outcome, that the new symbols are pinned, is delivered by the ceremony. **Because it is frozen, the AST ceremony must run before the gate-manifest re-anchor** (chunk M): a re-anchor run first would record the file's old bytes, and the AST ceremony would then leave a fresh hold.

`bootstrap/tests/fixtures/scaffold_ast_baseline.json` is cascade-mutable in the manifest, not hash-pinned, and also Maintainer-written. Not frozen, though edited: every engine file, `SECURITY_MUTATIONS.md`, `BOOTSTRAP.md`, the stub, the module pair and both presets. Frozen files that **read** these surfaces and must stay green **unedited**: `test_scaffold.py`, `test_presets.py`, `test_profiles_smoke.py`, `test_onboarding_slot_substitution.py`, `test_active_surfacing_render.py`, `test_trigger_evaluation_action.py`, `test_skills_onboarding.py`, `test_onboarding_review_tiers.py` (if `review-stance-and-lenses` has not already deleted it), `test_default_security_stance.py`, `test_profile_grammar.py` (it reads two example fences in `BOOTSTRAP.md`, not II-5), `test_upgrade.py`, `test_upgrade_module.py`, `test_security_capability_install.py`, `test_security_verification.py` and `_oracle.py`.

**The late additions add no frozen test file:** their tests go in `test_security_leaf.py` and `test_upgrade_module_additions.py`, already on the list. **One phase-mutable file is edited:** `bootstrap/tests/test_intents_tool.py` (C4), where the `.gitignore` repair put its seeding tests. The manifest lists it as phase-mutable, not frozen, so the ceremony gives a `PHASE-CHANGED` note and never a hold; the frozen count stays seven.

**The pinned collection moves.** New classes join `test_model_selection_stub.py`, `test_onboarding_seed_roster.py` and `test_upgrade_module_additions.py`; their node IDs are listed in the *Implementation verification* record. **One pinned node leaves on purpose:** `bootstrap/tests/test_model_selection_stub.py::TestFidelityCheck::test_fill_me_in_comment_fails` pins the rule the Maintainer reversed (Q1). It is replaced by `TestCommentsAreNotPlaceholders`, not renamed in place, because a node called "a comment fails" that asserts the opposite would mislead. `test_pyyaml_absent_degrades_gracefully` keeps its ID with a changed fixture (it needs a row; see C1). Changed frozen bytes do not redden `test_gate_manifest.py`, which verifies a freshly produced manifest and never diffs the committed fixture, so a green suite is no evidence the re-anchor is paid. **The re-anchor is the Maintainer's alone** (`bootstrap/REANCHOR_RUNBOOK.md`). The opening commit adds this plan's files to the queued row, marked planned and not yet changed; the archive commit adds the node IDs.

**AST: measured, not assumed, and not pinned as a count.** The method is `bootstrap/AST_BASELINE_RUNBOOK.md` Step 1, run at `72434d73`: four CHANGED (`main` in `cli.py`, `seed_gitignore` in `install.py`, `_cmd_adopt_module` and `cmd_upgrade` in `upgrade.py`), all from the `.gitignore` repair, and `test_ast_attest.py` fails 2 of 30 nodes. The repair's pending answer adds a fifth, `create_dev_tree` (the Internal review measured it in a scratch copy). So **no count in this plan is a criterion.** Every criterion below is a set difference taken against the tree the implementation starts from, and the number is whatever the ceremony derives. Writing P for that tree (the parent of C3, the first engine commit) and T for the tested commit, this plan's delta, as names:

* **already CHANGED at P, change again** (no new entry): `main`, `_cmd_adopt_module`, `cmd_upgrade` and `seed_gitignore`;
* **newly CHANGED (baselined symbols this plan changes):** `capture_model_selection_mapping` (C4 (b)); `write_install_lockfile`, `_cmd_init_lock`, `_cmd_finalize_lockfile`, `_apply_upgrade` and `read_lockfile` (C4 (d), folded in at the Maintainer's instruction);
* **re-keyed, not CHANGED:** `_commit_lock_and_caches` (C4 (c), folded in at the Maintainer's instruction). It is not in the baseline; `scaffold_ast_known_new.json` pins it by digest. Changing one line of it in a scratch copy made the verifier report `NEW FunctionDef:_commit_lock_and_caches (known-new digest/multiplicity mismatch ...)`, and not CHANGED. The runbook's Step 2 lists it as REKEYED, a review item to trace to its commit; C4 (c)'s commit is that trace;
* **NEW, to be pinned in `scaffold_ast_known_new.json`:** `_mapping_is_unfilled` and `model_selection_notice_lines` (C3, `install.py`); `_read_regular_bytes` (C3, `security.py`); `_stage_exclusive` and `_write_by_replacing` (C4 (a), `security.py`);
* **comment-only, no AST effect:** one comment in `lockfile.py` (the attestation parses code and sees no comments);
* **not changed by this plan:** `_write_stage` (it only joins a test list), `_yaml_dq`, `_assert_safe_write` and `_assert_fanout_contained` (the helpers call the guard, they do not change it), and the `_MODEL_SELECTION_*` constants.

**Expected end state, as sets:** CHANGED(T) = CHANGED(P) plus the six newly CHANGED names above; the known-new mismatches at T are exactly `{_commit_lock_and_caches}`; NEW(T) minus NEW(P) is exactly the five names above; MISSING and DUPLICATE are empty; and the digest of each of `main`, `_cmd_adopt_module`, `cmd_upgrade` and `seed_gitignore` at T differs from its digest at P. C6 derives all of it at P and at T. The `.gitignore` repair is still in code review, so its answer may change `main`, `_cmd_adopt_module`, `cmd_upgrade`, `seed_gitignore`, `create_dev_tree` and `SECURITY_MUTATIONS.md` again; the starting bytes of those will move before C4, and C3's gate re-reads them. **No symbol here is in `_UPDATE_ALLOWLIST`** (`_MODULE_MAPPINGS`, `_SKILLS_MAPPINGS`, `_CORE_MAPPINGS`, `install_onboarding`), so the correction is a Maintainer-run, dry-run-verified direct correction that an implementing agent does not perform.

**One combined ceremony, after this plan archives** (the Maintainer's choice, "One combined ceremony later"), **and before the gate-manifest re-anchor.** It re-anchors the repair's functions and this plan's delta once. Nothing re-anchors the repair on its own before then. `test_ast_attest.py` stays red until the ceremony runs, and Boundary B disposes of it each time (*Verification*). Chunk M gives the steps. Imports are not attested, so the new standard-library imports cost nothing, and `test_install_module.py::test_install_depends_only_downward` (install imports only its lower siblings) is unaffected.

**The oracle.** `bootstrap/_scaffold/` is on the differential oracle's sensitive roster (`bootstrap/tests/_oracle_activation.py`). Against the gate anchor `bd66a70c`, five engine paths already differ at HEAD: `cli.py`, `install.py`, `upgrade.py`, `slotmerge.py` and `SECURITY_MUTATIONS.md`. `security.py` and `lockfile.py` join them (the helpers; the reader and a comment), a small real cost for the ceremony's path check. The oracle's fresh-install scenario installs each preset non-interactively with the **current** templates and byte-compares the resulting trees; notice lines go to standard output, which it does not compare, and the stub, seeds and checker are templates both engines read. So the oracle should be unmoved, and Boundary B shows it.

### Lockfile

`python bootstrap/verify_integrity.py --target .` reports **18** violations at `72434d73`, none of them a file this plan edits. Two edited files match their record today and go stale when edited: `scripts/check_model_selection.py` (C1) and `dev/modules/model-selection.md` (C2). Each is reconciled by a scoped finalize of that one path in the commit that edits it (precedent `2ea3f869`), so the count stays 18. An unscoped finalize is never the fix, since it would re-attest the drifted 18. Cairn's own mapping is a living-state record and is not edited. The lockfile schema is untouched.

### Install contract

`scaffold.py --manifest` lists destination, source and mode, with no content hashes. No file is added to or removed from the install set. C6 shows its output byte-identical to the parent's.

### Found while planning, not widened

* **A pinned test needs a row under the new rule.** `test_pyyaml_absent_degrades_gracefully` checks that the bare path degrades gracefully, using the file `mapping: [unclosed`. That file has no row, so the new rule fails it with exit 1 and the test would go red for the wrong reason. C1 gives its fixture a row line; the assertion and the node ID are unchanged.
* **The checker can crash on deeply nested YAML.** `yaml.safe_load` raises `RecursionError` at about 500 nested flow sequences. `_structural_validate` catches only `yaml.YAMLError`, so today the checker ends in a raw traceback. The new value scan touches this path, so C1 catches it and reports exit 3, "not valid YAML" (*Plan decisions*, P8). The plan's own addition, not the Maintainer's. A second hole sits in the same call: YAML's merge keys (`<<:`) make `safe_load` itself run for tens of seconds on a file under a kilobyte (the Security Review measured 21 s and 772 MB at 24 lines), so the loader refuses them (P8).
* **`_commit_lock_and_caches` had the hole the capture is being fixed to avoid; its fix is folded in** (*Answered by the Maintainer after the plan opened*), and so is the `.gitignore` append's (the same answers, item 4). The class is wider than those, and the rest is **not** folded in. The module-merge conflict side-file in `slotmerge.py` is written with `write_text` onto a name fixed by the file and slot (read in the code, not run). More generally `_assert_safe_write` refuses symbolic links, not hard links, so any in-place engine write onto a name that a hard link already occupies goes through. No complete sweep of the engine for the class was made, and git cannot carry a hard link, so each case needs someone already on the machine.
* **Four more functions write the lockfile in place, and the lockfile reader follows links: folded in** (*Answered by the Maintainer after the plan opened*, item 5). The Internal review found the four writers; the Security review found the reader. They were first a held question, and the Maintainer said yes after both plan reviews, so the design in C4 (d) was read by no plan reviewer.
* **The `Waiting on Maintainer` marker on the queued row names only the gate-manifest re-anchor.** The AST correction is a separate ceremony with its own runbook. The row's prose can carry it, but the marker, and so `board.py --maintainer`, does not list it. Whether the AST ceremony needs its own marked row is the Maintainer's call; this plan declares no Waiting line, and the question is put at archive (*Dispositions*).
* **Citations from other plans.** `review-stance-and-lenses` cites `templates/modules/team-gated/model-selection.md:128-131`; C2 inserts its paragraph below line 158, so those lines hold (a criterion). It also cites `bootstrap/_scaffold/install.py` around line 1012, which moves when C3 and C4 land; it is an evidence note in a record, and `claim_check` checks only that a cited line is in bounds. `independent-scientific-check` states the AST baseline as two changed symbols; it is four now (above), and its own criterion says to derive the figure again.
* **The proposal's own line citations moved** (`cli.py:625` is now 635, and so on). This plan cites by function name and uses a line number only where it says "at `72434d73`".

### Plan decisions the proposal left open

The accepted text fixes the behaviour, not every shape. These are this plan's choices; plan review may overrule any of them.

* **P1, where the notice is gated.** Each call site calls the helper only when the module is in play: `main` inside `if "model-selection" in modules`, adopt when the name is `model-selection`, upgrade when `"model-selection"` is in the lockfile's module list as read at the start. The helper is also silent on a missing file (CL-3), so a project without the module gets silence twice over.
* **P2, the capture's temporary file.** It is made by the shared helper (P17): a random name, created exclusively with `O_CREAT | O_EXCL`, so a file or link already waiting anywhere cannot be written through. CL-1 allowed `mkstemp` or `O_CREAT | O_EXCL`; the helper uses the second, because `mkstemp` creates files with mode `0600`, which would change the permissions of every file the helper writes. The capture's signature does not change.
* **P3, CL-4: widen, and name the rest.** The bare row test accepts a quoted `tier` key and a one-line list whose first item begins with `tier`, on top of the anchored forms. A prototype in a scratch copy, over 21 hand-built spellings, showed the anchored pattern rejecting three spellings that PyYAML reads as rows (a double-quoted key, a single-quoted key, a one-line list), and the widened pattern accepting all three. The differences that remain are all in the bare path's stricter direction, which is the louder side: a one-line list whose first key is not `tier`, and a `tier:` that sits inside another value. The parity test asserts those differences as an explicit list, in the direction they occur.
* **P4, the order of the checker's decisions.** Scan for `FILL ME` (exit 1), then with PyYAML the structure (exit 3 for a parse error or a non-mapping), then the row requirement (exit 1). So a comments-only file exits 1 on the bare path and 3 with PyYAML; both are non-zero, and the difference is listed in the parity test.
* **P5, the "could not read" wording.** CL-3 asked that it say "That file was not changed", since "Nothing was changed" reads wrongly after a successful apply. The final text is quoted in C3.
* **P6, the capture's refusal line.** `error: model-selection capture refused (containment): dev/.cairn/model-selection-mapping.yml is a link or sits behind one. Replace it with a regular file, or install with --non-interactive and fill it by hand.` on standard error, matching its sibling lines. It is a constant: the remedy names only the fixed path, and nothing comes from the exception or the tree. The quoted proposal line is its prefix.
* **P7, where the notice prints.** `main`: after the capture block, whether the capture ran, was skipped or was interrupted. Adopt: right after the "Adopted module" line. `--plan` and `--stage`: the last output before `return 0`. `--apply`: after the `try`/`except` that wraps `_apply_upgrade`, only when it returned 0, so a notice can never be reported as an apply refusal.
* **P8, the checker's loader.** It loads with a `SafeLoader` subclass that refuses YAML merge keys, walks the loaded value with an explicit stack (each object once), and catches `RecursionError` from the loader (exit 3). The Security review measured that a file of 881 bytes built from merge keys took 21 s and 772 MB inside `safe_load`, before any walk could help, so a walk alone could not make the claim "neither depth nor aliasing can blow it up"; refusing the keys does, and no mapping needs them. **The merge-key refusal and the `RecursionError` catch are this plan's own additions, made in response to the plan reviews and what was found while planning. Neither is at the Maintainer's instruction.** I kept the catch: it is two lines on a path the plan already rewrites, the Security review confirmed the crash on a file the adopter wrote, and the plan loses no accepted outcome if a reviewer would cut it. They are listed in *Scope delta* as the plan's own additions.
* **P9, no read-size cap.** The helper and the capture read the whole file. A multi-gigabyte regular file in a hostile tree could slow an install, but the checker and every other read in the engine do the same. Named as a residual, not built.
* **P10, the notice's second line.** For a file with no rows at all, "still holds the FILL ME stub" is imprecise. The quoted text binds, so it is kept and the imprecision is named. The first line, "is not filled in", and the instruction to write one row per tier stay true.
* **P11, the AST fixtures.** Neither is edited by an implementing agent (above).
* **P12, names.** Every test class and node is named for the property it pins. No finding id, chunk letter or plan row appears in an added comment, docstring or test name (a criterion in C6, with a control).
* **P13, the install-record committer's temporary files.** `_commit_lock_and_caches` stages each cache and the lockfile with `_stage_exclusive` (P17) and renames them in the order it uses today. If it fails before the renames are done it removes every temporary it staged, and no other file.
* **P14, the `.gitignore` append's mechanism (GS-SR-3, GS-SR-4).** `seed_gitignore` works in bytes, so it never decodes the file (P15). The link-safety preflight is the guard plus an `lstat`: a regular file with a link count above 1 is refused with `ScaffoldSecurityError`, and so is anything that is not a regular file (P15). Nothing is read. When entries must be written, the file is read through `_read_regular_bytes(path, single_link=True)` (P16), which refuses a link swapped in after the preflight (the operating system refuses it) and a pipe (it cannot block the open), and checks the link count again on the descriptor. An existing file must also pass `os.access(path, os.W_OK)`. The write is `_write_by_replacing` (P17): the old file's read and write bits only, never a setuid or execute bit. **Refuse or replace a hard-linked file?** A bare rename would also close the write, but it would first read the outside file's content into the project's `.gitignore`, which Git then commits, and would silently cut the link for a user who linked it on purpose. I refuse. If a reviewer prefers to replace, one criterion in C4 (e) changes and nothing else. The refusal text names a fix that is true for a hard link (C4 (e)).
* **P15, the preflight stops reading (GS-SR-5).** With no entries `seed_gitignore` returns after the guard and the `lstat` checks, before any read. A non-UTF-8 `.gitignore` then no longer stops an apply that adds nothing, and when a line is added its original bytes are kept exactly. The `lstat` also refuses a folder, a pipe, a socket or a device, so those still fail early with the clean exit 2, as the repair made them. An earlier draft of this plan dropped that fail-early; the Internal review rightly objected. Nothing in the Maintainer's answer asks for it: his words were only "Yes, fix the .gitignore points". The first-write refusal stays as a backstop.
* **P16, one reader.** `_read_regular_bytes(path, *, single_link=False)` in `security.py`, shared by the notice helper, the capture, `seed_gitignore` and `read_lockfile`. It follows `_read_bounded` in `bootstrap/verify_integrity.py`, which the repository has already reviewed: open once with `O_NOFOLLOW | O_NONBLOCK | O_NOCTTY | O_BINARY` (each by `getattr`), `fstat` the descriptor, read only a regular file. It is not inlined three times because three hand-written recipes would drift. No size cap (P9).
* **P17, one writer.** Two helpers in `security.py`: `_stage_exclusive(path, data, target)` and `_write_by_replacing(path, data, target)`, used by seven callers (the capture, `_commit_lock_and_caches`, `seed_gitignore`, and the four lockfile writers). They create the temporary with `O_CREAT | O_EXCL | O_NOFOLLOW | O_BINARY` under a random name, set the old file's **read and write bits only** (`& 0o666`) with `os.fchmod` **on the descriptor** where `fchmod` exists, guard the temporary path, and remove only the temporary file they created. The mask closes MM-SR-1: copying all the mode bits would carry a setuid bit onto a file the installer now owns, and setting them by path follows a swapped link. A new file gets the mode a plain write gave. `security.py` is the home because it is the containment leaf (standard library only), which every engine module already imports. The accepted text had the capture's steps "all inline" so as to add no AST symbol; the steps and their order are kept, in a helper, and the ceremony pins the helpers.
* **P18, the other lockfile writers and the reader.** The four writers and `read_lockfile` (C4 (d)). Each writer passes the bytes of the same `_emit_lock_yaml` text to `_write_by_replacing`; nothing else about what it writes changes. The reader raises `ScaffoldSecurityError` for a link or a non-regular file instead of following or opening it, and keeps `None` for an absent or unparseable lockfile. A refusal reaches its callers as the traceback-and-exit-1 class the oracle already pins; no caller is given a catch.

### Documentation / doctrine surface

| Layer | Files |
|---|---|
| Governing | none; nothing under `doctrine/` and no `AGENTS.md` changes, so the doctrine rate-limit gate is not engaged |
| Descriptive | none. Searched `docs/`, `README.md`, `bootstrap/*.md`, `dimensions/` and the template core for `model-selection`, `check_model_selection` and the mapping's name: no page describes the capture or the check. The one mention (`docs/solo-legacy-recipe.md`) says only when to add the module |
| Module text | the module pair (C2) |
| Install guide | `bootstrap/BOOTSTRAP.md`, II-5 (C2). The module document names II-5 without a path, because `BOOTSTRAP.md` is not installed |
| Deliberation | this plan; `dev/PLANNING.md` (the re-anchor row now; the deferrals at archive) |
| Changelog | one entry, written by the archive commit |

All shipped text stays vendor-neutral. The neutrality gate (`python scripts/quality_gate.py --sub neutrality`) reads `fail=0` at HEAD, so the criterion is **stays zero**. Every shipped block this plan quotes was scanned with the II-5 pattern and the gate's own denylist, with a control that did match (a line naming three of the denylisted names).

### Sequencing with the other plans

Four plans are ahead of this one, in the order the Maintainer set ("Board-as-basis first (Recommended)"): `neutrality-and-upgrade-slots`, `independent-scientific-check`, `review-stance-and-lenses`, `board-as-basis`. The `stewardship-and-reuse` plan comes after this one. **This plan starts only when each plan ahead of it has reached `awaiting-code-review` or later.** Implementation is sequential because every plan commits to the same `master`, and interleaving would make each Boundary B range ambiguous. Plan review can run alongside, since a review writes only its own section. Files were read from each plan's own text at `72434d73` (`board-as-basis` at `10ae6428`); the statuses below are as of the plan reviews.

| Plan | Files shared with this one | What each does there | Effect |
|---|---|---|---|
| **`neutrality-and-upgrade-slots`** (implementing) | `dev/.cairn/cairn-lock.yml` | its twelve records (done in C2-C5) against this plan's two | disjoint records; read fresh, check the lockfile diff before each commit |
| | `dev/PLANNING.md`, `CHANGELOG.md` | its re-anchor-row paragraph; its archive entry | commit by path, read fresh |
| | the neutrality checker | stricter, and now zero | everything this plan ships is held to it: **stays zero** |
| | `bootstrap/_scaffold/` | not touched by it | its C12 compares the AST set at its parent and tested commit; it derives that set itself, which is larger than the two symbols its text names |
| | `scripts/check_model_selection.py` | listed there as not touched | no overlap |
| **`independent-scientific-check`** (ready) | `bootstrap/BOOTSTRAP.md` | one sentence in the I-2 paragraph | this plan edits II-5; different sections, so a textual rebase. Cite headings, not lines |
| | `dev/PLANNING.md`, `CHANGELOG.md` | at its archive | commit by path |
| | the gate-manifest re-anchor row | its one new test file joins the row | one row, several paragraphs |
| **`review-stance-and-lenses`** (`ready-to-implement`; goes third) | `templates/modules/team-gated/model-selection.md` and `dev/modules/model-selection.md` | its C3: the role table, the downshift condition, the bright-line list, the diversity reference | this plan adds a paragraph and one sentence in the Mapping-record schema block, below its edits; **it lands first, so this plan finalizes the lock record second**. Its stance test must pass with this plan's text: the word "family" is forbidden there only in the downshift condition (a), and this plan uses it for mapping rows |
| | `templates/onboarding/collaborative-team.md`, `high-rigor-legacy.md` | its C7 rewords External-tier sentences | this plan appends one seed after the last seed (`walk-foldback-protocol`), before "Active-surfacing prompt content"; different paragraphs |
| | `bootstrap/tests/test_onboarding_seed_roster.py` | its plan runs it unedited | it runs first; this plan adds its seed tests afterwards |
| | `scripts/check_model_selection.py`, its template, `dev/.cairn/model-selection-mapping.yml` | its criterion: `git diff --stat` shows them untouched in its range | holds, because this plan's edits are outside its range |
| | `dev/.cairn/cairn-lock.yml`, `dev/PLANNING.md`, `CHANGELOG.md` | the `model-selection.md` record and its row paragraph | same record, sequentially |
| **`board-as-basis`** (`ready-to-implement`; ahead of this one, by the Maintainer's order) | **the `board.py --maintainer` output** (installed from `templates/skills/_lib/board.py`) | its C1 pins the terminal board and `--maintainer` byte for byte, then its C2 moves the roadmap-row reader into one function shared with `--json` | this plan reads the output in one seed test and pins only the substring `fill the model mapping` and the word `declared`, never the column layout. This plan runs second, so its seed test is the first to run against the finished reader |
| | **the `dev/PLANNING.md` row grammar** (what counts as a row that declares a wait) | its golden tree covers rows in plain, indented, sub-bullet and dash-bullet forms and a marker mentioned inside a sentence, and its C2 test mutates the grammar | this plan's seed puts the marker on a two-space-indented continuation line inside a `* [seed; ...]` item: `**Waiting on Maintainer**: fill the model mapping` (22 characters, under the board's 48; measured to list at `dev/PLANNING.md:100` in a scratch install). I did not check that its "indented" form is this exact shape, so this plan's seed test is a second pin on exactly this shape: a grammar change that stops listing an indented seed line turns it red |
| | `dev/PLANNING.md` (the re-anchor row) | its paragraph is already in the row (`10ae6428`) | this plan's opening commit adds its own after it and before the Waiting line, re-reading the file first |
| | `dev/.cairn/cairn-lock.yml` | its `tools/board.py` record | disjoint |
| | `CHANGELOG.md` | its archive entry | commit by path |

`stewardship-and-reuse` (accepted; its plan opens after this one) edits the plan templates' *Scope*, *Dispositions* and deviation sentence, `AGENTS.md` and the doctrine pages. It shares `dev/PLANNING.md` (it mirrors the board's archive-preconditions section at a serialization point) and `CHANGELOG.md` with this plan, and no other file.

**Order, as the Maintainer set it:** `board-as-basis` first, then this plan. The couplings are the pinned `--maintainer` output and the row grammar (both in the table above), so neither order would cost a rewrite. The AST ceremony is one combined run after this plan archives, so this plan's position cannot cause a second pass.

## Sequence

The chunks run in order. Each lands as one commit; nothing is pushed.

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | **The check.** Both copies of the checker: YAML 1.1 line breaks only, full-line comments skipped, at least one row, the widened bare row pattern, the value scan when PyYAML is present, the `RecursionError` catch, the docstring and "whole-file scan" comment rewritten. In `test_model_selection_stub.py`: `TestCommentsAreNotPlaceholders` replaces the reversed node; the row, value-scan, bare-residual and Cairn's-own-mapping classes; the corpus generator and the checker side of the parity test; `test_pyyaml_absent_degrades_gracefully` gets a row. Scoped finalize of `scripts/check_model_selection.py`. | plan review landed (`ready-to-implement`); every plan the Maintainer has put ahead of it at `awaiting-code-review` or later; the entry condition re-read | one commit |
| C2 | **The words and the reminder.** The stub's example block; the module pair (paragraph and corrected sentence); the II-5 block and the fourth allowed match in `BOOTSTRAP.md`; the seed in both presets; the seed, II-5 and stub tests; the `TestFamilyNotVersionReachesEverySite` class with its C2 sites. Scoped finalize of `dev/modules/model-selection.md`. | C1 (the paragraph says what the check does) | one commit |
| C3 | **The notice on install.** In `security.py`: `_read_regular_bytes`. In `install.py`: `_mapping_is_unfilled` and `model_selection_notice_lines`, with both variants as constants. In `cli.py`: the call after the capture block, and the old interactive-only line removed. The comment in `lockfile.py`. Tests: the reader's matrix, the install-path rows, constant text, the named pipe, the missing-file silence, and the engine side of the parity corpus. | C1 (the parity test compares the two rules), C2; the engine's starting bytes re-read | one commit |
| C4 | **The safe writes.** Up to five commits sharing the label, in this order: (a) `_stage_exclusive` and `_write_by_replacing` in `security.py`, with `TestWriteByReplacing`; (b) the capture: early guard, read through the reader, the helper for the write, the constant refusal line with its remedy, the family prompt and header, the docstring, `SECURITY_MUTATIONS.md` and `_GUARDED_WRITE_FUNCS` additions; (c) `_commit_lock_and_caches` through `_stage_exclusive`; (d) the four other lockfile writers and `read_lockfile` (**folded in after both plan reviews; no plan reviewer read this design**); (e) the `.gitignore` append: no read in the preflight, kind and link count by `lstat`, the reader, `os.access`, the helper, the refusal text and its remedy, one sentence in `SAFETY.md`. Each carries its own red-then-green record. | C3; the engine's starting bytes re-read, and `SECURITY_MUTATIONS.md`, `_GUARDED_WRITE_FUNCS` and the `.gitignore` refusal's remedy line re-read at the parent | up to five commits |
| C5 | **The notice on adopt and upgrade.** `_cmd_adopt_module` and `cmd_upgrade`: five call sites in all. Tests: adopt, `--plan`, `--stage`, the delivering `--apply`, a refused `--apply`, and the no-module silence. | C3 | one commit |
| C6 | **Boundary B, the evidence the suite cannot give, then the record.** One full run on a clean commit; the mutation ledger; the stub merge measurement; the smoke checks; the AST, frozen and lockfile derivations. Appended as `## Implementation verification`. Status moves to `awaiting-code-review`. A surviving mutant sends the work back to its chunk and Boundary B is redone. | C1-C5 | one commit |
| M | **MAINTAINER-ONLY, no new ceremony.** Two ceremonies, **in this order: the AST correction, then the gate-manifest re-anchor once.** The AST correction writes `scaffold_ast_known_new.json`, which is a frozen file, so a re-anchor run first would record its old bytes and the AST correction would leave a fresh hold. The AST correction is one combined run after this plan archives, covering the repair's CHANGED functions and this plan's delta. **No agent pre-fills it, and this plan fixes no figures for it.** The steps, from `bootstrap/AST_BASELINE_RUNBOOK.md`: (1) confirm `bootstrap/_scaffold/` at the ceremony commit is byte-identical to the code-reviewed tested commit, and trace any difference first; (2) derive CHANGED, REKEYED, DROPPED and NEW fresh with `_ast_attest`'s own `_merge_current` and `_classify` (the runbook's Steps 1 and 2), and stop unless they equal the declared sets (the repair's, from its reviewed record, and this plan's, from the plan's record), each member traced to its commit, the one REKEYED symbol, `_commit_lock_and_caches`, traced to this plan's C4 (c) commit; (3) a dry run that computes every digest from the live tree and prints each key's old and new value, refusing any key that was not declared; if a script is needed, it is committed and code-reviewed before the Maintainer runs it, never kept outside the repository; (4) write, run `verify --known-new`, confirm the baseline symbol count did not grow, and commit both fixtures by explicit path; (5) then run the gate-manifest re-anchor once, so it records the final bytes of the seventh file. The figures C6 records are a cross-check the ceremony's own derivation must equal, never an input. The six frozen files and the node changes join the queued row. **An implementing agent must not perform either ceremony.** The agent's part is the board note at archive, which states the order. | code review cleared | Maintainer |
No Waiting line in this plan: the wait is already declared on the marked board row.

## Acceptance criteria

Each criterion says how it fails. A criterion that cannot fail is not one. Test classes are named for the property they pin. Every new test is red before the code that makes it green, and the commit body names the commit where it was red.

### Checks every chunk repeats

* **Claim check.** `python scripts/claim_check.py` on each edited document exits 0 with no hard flag.
* **Prose integrity.** `python scripts/check_cairn.py` shows no issue in a file the chunk edits. Any other issue is recorded and shown unchanged.
* **Neutrality stays zero.** `python scripts/quality_gate.py --sub neutrality` reads `fail=0` before and after.
* **Twins.** `cmp` on each pair in the chunk exits 0: the checker pair (C1) and the module pair (C2).
* **No process words in durable text.** `git diff -U0 <parent>..HEAD` over the chunk, added lines only, searched for finding ids, chunk letters and plan rows (`SEC-[0-9]`, `CL-[0-9]`, `MM-[0-9]`, `SR[0-9]`, `\bC[1-6]\b`, "plan review"), returns no process reference. The Unicode term "C1 control" is not one and is explained if it appears. A control: the same search over this plan file returns matches, so the instrument can match.
* **Lockfile.** After a scoped finalize, `python bootstrap/verify_integrity.py --target .` still lists exactly the 18 files it listed at the base, and the lockfile diff touches only the finalized record.

### C1 -- The check

* **A mapping you filled by hand passes.** The shipped stub with its row replaced by real values and every comment kept exits 0. The shipped stub exits 1. *Red when:* the comment skip is removed.
* **A placeholder in a value still fails,** including in a trailing comment on a value line: exit 1. *Red when:* the skip is widened to trailing comments.
* **The loss is pinned, not hidden.** A `# TODO: FILL ME` comment above filled rows exits 0, in a test whose docstring says why: the check attests shape, not intent. This is the property the reversed node used to hold.
* **Only a space before `#` makes a comment.** A line led by a tab, a no-break space, a form feed or a byte-order mark is scanned. Lines split on exactly `\r\n`, `\n`, `\r`, U+0085, U+2028 and U+2029: a `FILL ME` value behind U+2028 or U+0085 is found, and CR-only and CRLF files read like LF. *Red when:* `str.splitlines()` is used (it also splits on form feed and vertical tab, which would turn a form-feed-led comment into its own comment line), or a tab is treated as blank.
* **A mapping needs a row.** `mapping: []` with header comments exits 1 on both paths. A comments-only file exits 1 on the bare path and 3 with PyYAML (P4). With PyYAML, the row rule is Revision 2's: `mapping` is a non-empty list. A missing `mapping` key, a `mapping` that is not a list, and an empty list all exit 1; a non-empty list passes whatever its items are (the looser cases are on the explicit list below). The failure message says there are no rows and does not say `FILL ME`. The structure is judged before the rows (P4), which is also what keeps two pinned nodes green, `test_malformed_message_is_clean` and `test_non_mapping_top_level_fails_3`. *Red when:* the row requirement is dropped.
* **The bare row test is anchored and widened (P3).** A `tier:` inside another value is not a row. A block row, a flow item, a double-quoted key, a single-quoted key and a one-line list starting with `tier` are rows.
* **With PyYAML, every value is scanned,** once each, by identity, with an explicit stack: strings, dict keys, set members, and bytes decoded as text. *Red when:* the scan is removed, or limited to strings.
* **Merge keys are refused (P8).** With PyYAML the file is loaded by a `SafeLoader` subclass whose `flatten_mapping` raises on any merge key (`<<`) and otherwise defers to the base class. The subclass is built inside the function, after the optional import, and raises with no source mark, so its message is fixed text. The 24-line merge-key chain (881 bytes; it took 21 s and 772 MB to load) exits 3 within a fixed time, run as a subprocess with a timeout of a few seconds. A normal mapping loads as before. *Red when:* the refusal is dropped (the test times out).
* **Depth and aliasing are safe.** A 22-level nested-alias document completes in a fixed time (the same subprocess form; unmutated it takes milliseconds, without the visited set about eight seconds). A document 5000 flow-sequences deep exits 3 with no traceback (the `RecursionError` catch, which is this plan's own addition, P8).
* **The checker's new messages print no parsed value.** The no-row message and the value-scan failure message are fixed text plus the mapping's path. A fixture holds a `FILL ME` value written with YAML's `\e` and `\a` escapes (it parses to ESC and BEL) and a second, no-row file: neither stream carries an ESC or a BEL byte. *Red when:* a message echoes a value.
* **The corpus has two parts, and the engine meets both (C3).**
  * **Generated:** leads {none, space, tab, no-break space, form feed, byte-order mark} times breaks {the six above} times positions {comment, value, row}: 108 files. The expected verdict depends on the lead and the position, never on the break.
  * **A table of named spellings,** committed in the test, one row per member: its text, the exit code of the bare checker, of the PyYAML checker and of the engine's rule (C3), and the list it belongs to. **Stricter with PyYAML** (PyYAML fails, the line rule passes): a `#` line inside a block scalar; a plain value folded over two lines; a quoted value folded over two lines; a line continuation; `"FILL\x20ME"`; a repeated empty `mapping:` key; `!!binary RklMTCBNRQ==`; `!!set {"FILL\x20ME"}`; and three files with `mapping: []` in which a row-shaped line is not an item of `mapping` (a `tier:` row under another key, inside a block scalar, inside a multi-line quoted value). **Looser with PyYAML** (PyYAML passes, the line rule fails): a one-line list whose first key is not `tier`; a list item that is a mapping without a `tier` key; a list of non-mappings; a `tier:` inside another value. **Agreed after widening:** the double-quoted key, the single-quoted key and the one-line list starting with `tier`. The comments-only file (1 and 3) is its own row.
  * The test asserts each member's three exit codes and that the two checkers differ **only** on the members of the two lists, in the direction the list names. A member outside both lists that differs fails, and so does a list member that no longer differs. *Red when:* U+2028 is dropped from the checker's break set (M8a), or the widened pattern reverts (M7a).
* **Cairn's own mapping passes its own check,** with and without PyYAML (by blocking the import). *Red when:* the mapping is reset to the stub, shown in a separate copy.
* **The pair is identical** (`cmp`), the docstring and the "whole-file scan" comment describe the new rule, and the residual class is named in the docstring: a value whose `FILL ME` is not spelled out on one non-comment line reads as filled on the bare path, and so does a row-shaped line that is not an item of `mapping`.
* **Existing nodes.** `test_pyyaml_absent_degrades_gracefully` keeps its ID, its assertion, and the "structural validation skipped" note, with a row added to its fixture. The other 23 pinned nodes of the file pass unedited.
* **Lockfile.** The scoped finalize of `scripts/check_model_selection.py` is in this commit.

### C2 -- The words and the reminder

**The shipped words are Revision 2's R2.5, verbatim.** They are quoted here so the plan stands without the archived proposal. The stub's example block (the only stub change):

```
# Replace the placeholder row below with your real assignments. Name the model
# family, never a version: the latest release of that family is meant. Shape:
#
#   - tier: high
#     model: vendor-a/flagship-family
```

The II-5 block, placed after the vendor-neutrality block:

```
**Model-selection mapping** (only if `model-selection` was installed)
- [ ] `python scripts/check_model_selection.py` exits 0. If not, ask the Maintainer which
      model family fills each tier (high, medium, low) and record one row per tier, naming
      the family and never a version; do not guess.
```

The fourth allowed match in II-5's vendor-neutrality list ("Three classes" becomes "Four"): "the filled tier-to-model mapping, `dev/.cairn/model-selection-mapping.yml`, which is adopter configuration and may name model families by design".

The seed, appended to both presets after `walk-foldback-protocol`, under `<!-- cairn:if complexity in moderate,complex -->`:

```
* [seed; id: fill-model-selection-mapping]
  **Waiting on Maintainer**: fill the model mapping
  If `dev/.cairn/model-selection-mapping.yml` exists, ask the Maintainer which model
  family fills each tier (high, medium, low), record one row per tier (the family, never
  a version), and run `python scripts/check_model_selection.py`. Delete the Waiting line
  when it passes.
```

The module paragraph, in the byte-identical pair, after the Mapping-record schema block:

```
**Filling the mapping.** The adopter-local mapping is
`dev/.cairn/model-selection-mapping.yml`: one row per tier you populate (high, medium,
low), copying the shape of the seeded row. In `model`, name the model family, never a
version; the latest release of that family is meant, so a new release does not make a row
stale, and a release that changes which family fits a tier does. Say in `source` who made
the assignment. `python scripts/check_model_selection.py` exits 0 once no placeholder
remains and at least one row exists. It checks shape, not truth, and nothing reads
`date_verified`, so noticing a stale mapping is yours to do. The installing agent runs the
check at the acceptance step; after that a person does, because nothing runs it
automatically.
```

and the sentence that replaces "surfaced by an existing routine": "Re-rank on a low-frequency housekeeping pass; the `date-verified` stamp lets a reader see staleness, and no routine reads it."

* **The words are pinned by exact string,** not by keyword. Three load-bearing items each get a test that fails if the string is missing from the shipped file: the Waiting line `**Waiting on Maintainer**: fill the model mapping` (both presets); the module paragraph's "nothing reads `date_verified`" (both copies); and the corrected sentence's "no routine reads it" (both copies), together with the absence of "surfaced by an existing routine". *Red when:* any is dropped or reworded.
* **The stub's diff is the example block and nothing else.** `git diff -U0` against the parent shows hunks only inside the lines that begin "Replace the placeholder row below" through `model: vendor-a/flagship-family`. The placeholder row (five fields, each `FILL ME`) and its trailing comments are byte-identical. A test pins the row as one list item with five `FILL ME` fields, and the example block as containing "family" and "never a version", with none of the gate's denylisted names.
* **The module pair** is byte-identical (`cmp`). The hunks begin below line 158, so `model-selection.md:128-131` still says what review-stance cites.
* **II-5 names the check** (`TestAcceptanceChecklistNamesTheMappingCheck`). The block is as quoted, after the vendor-neutrality block and before the dogfood gate, and the fourth allowed match is as quoted. The installer's closing steps still print "Run the R-F acceptance gate (II-5)". *Red when:* either is missing. `test_profile_grammar.py`, which reads two example fences in `BOOTSTRAP.md`, passes unedited. No live document cites a `BOOTSTRAP.md` line after 544 (searched, with a control that found the proposal's own citations).
* **Measured, on the drafted wording:** in a scratch copy of `72434d73` with the seeds and the stub edit applied, twelve test files (the onboarding family in the C2 row of *Verification*, plus `test_model_selection_stub.py`) pass, 202 tests in all, `test_slot_seed_count_matches_source` among them.
* **The seed renders where it should.** Installing `collaborative-team` and `high-rigor-legacy` at their own settings puts `fill-model-selection-mapping` and the Waiting line in `dev/PLANNING.md`. The same preset with `complexity: simple`, and `solo-greenfield`, render neither. *Measured:* all four, in a scratch install. `python tools/board.py --maintainer --root <install>` lists one row, `declared`, text `fill the model mapping`, and the line number it names holds the Waiting line.
* **The seed outlives a removed module, knowingly.** A profile that removes `model-selection` from a moderate preset still gets the row; a test pins that, so a later roster gate is a deliberate rewrite. The seed's "If ... exists" opening is why it does no harm.
* **A live install writes a clean lockfile** for both presets at their default axes, so the onboarding overlay the lockfile precomputes agrees with the one installed.
* **Family, never a version, at eight named sites** (`TestFamilyNotVersionReachesEverySite`, parametrized over them; it starts with the C2 sites and grows in C3 and C4):

  | # | Site | Its exact phrase | Chunk |
  |---|---|---|---|
  | 1 | the stub's example block | "Name the model family, never a version" | C2 |
  | 2 | the first notice text | "Name the family, never a version" | C3 |
  | 3 | the capture's prompt | "model family, not a version" | C4 |
  | 4 | the header the capture writes | "# Name the model family, never a version: the latest release of that family is meant." | C4 |
  | 5 | the II-5 block | "naming the family and never a version" | C2 |
  | 6 | the seed in `collaborative-team` | "(the family, never a version)" | C2 |
  | 7 | the seed in `high-rigor-legacy` | "(the family, never a version)" | C2 |
  | 8 | the module paragraph | "name the model family, never a version" | C2 |

  The set is closed: a search of the live shipped files (`templates/`, `bootstrap/*.md`, `dev/modules/`, `scripts/` and `bootstrap/_scaffold/`, tests excluded) for "never a version" or "not a version" returns exactly these sites, so a ninth is noticed. *Red when:* the phrase is removed from any one.
* **Lockfile.** The scoped finalize of `dev/modules/model-selection.md` is in this commit.

### C3 -- The notice on install

The two texts, final (P5). They are constants, defined inside the helper:

```
NOTE (model-selection) -- the tier-to-model mapping is not filled in:
  dev/.cairn/model-selection-mapping.yml still holds the FILL ME stub.
Until it is filled, `python scripts/check_model_selection.py` fails. Nothing runs
that check automatically. Ask the Maintainer which model family fills each tier
(high, medium, low); do not guess. Name the family, never a version: the latest
release is meant. The stub holds one placeholder row: replace it with one row per
tier, copying its shape (tier, model, date_verified, task_family, source), and say
in `source` who assigned the model.
Schema: dev/modules/model-selection.md, "Mapping-record schema".
```

```
NOTE (model-selection) -- could not read dev/.cairn/model-selection-mapping.yml
(it is a link, sits behind one, is not a plain file, or is not valid text).
That file was not changed. Open it yourself, then run
`python scripts/check_model_selection.py`.
```

**The reader, first.** C3 adds `_read_regular_bytes(path, *, single_link=False)` to `bootstrap/_scaffold/security.py`, the containment leaf (it imports only the standard library, so every engine module above it can call the helper). It follows the repository's reviewed recipe, `_read_bounded` in `bootstrap/verify_integrity.py` (P16):

* it opens the path **once**, with `O_RDONLY | O_NOFOLLOW | O_NONBLOCK | O_NOCTTY | O_BINARY`, each flag built at call time with `getattr(os, name, 0)`, so a platform without one still imports the module and a pipe cannot block the open;
* `FileNotFoundError` returns `None`; any other `OSError` from the open becomes a `ScaffoldSecurityError` with fixed text;
* it takes `fstat` of the **descriptor it opened** and refuses anything that is not a regular file, and, when `single_link` is set, a link count above 1 (each a `ScaffoldSecurityError` with fixed text that names no path);
* it reads all the bytes through that descriptor and closes it.

* **The reader refuses everything but a regular file, by construction** (`TestReadRegularBytesRefusesAnythingElse`, in `test_security_leaf.py`). A matrix: a regular file returns its bytes; an absent path returns `None`; a symbolic link, a dangling link, a folder, a named pipe (inside a timeout, run as a subprocess), a socket and a device (`/dev/null`) are each refused; a hard link is refused only with `single_link`; a link or hard link swapped in by a wrapper just before the real open is refused; no message carries a path or an OS error text. With `O_NOFOLLOW`, `O_NONBLOCK`, `O_NOCTTY` and `O_BINARY` removed from `os`, the helper still imports and reads. *Red when:* the regular-file check, `O_NOFOLLOW`, `O_NONBLOCK` or the `single_link` check is dropped, or the open is made by path with `read_text`.
* **The helper decides in this order.** (1) `lstat` the path: a missing entry (`FileNotFoundError`) returns `[]`, first, and nothing else is tried; any other `OSError` returns the second text. (2) `_assert_safe_write` (a link above the path, an escape) refused returns the second text. (3) `_read_regular_bytes(path)`: `None` (the file vanished) returns `[]`; a refusal or an `OSError` returns the second text. (4) A strict UTF-8 decode; a decode error returns the second text. (5) `_mapping_is_unfilled(text)` true returns the first text, otherwise `[]`. It never raises. That a pipe, a folder or a link is never opened is the reader's property, not a separate check. *Red when:* the missing-file branch is dropped (a project without the module is told it could not read a file it never had), or the reader is bypassed with a read by path.
* **A named pipe at the path returns within a timeout.** Run in a subprocess with a timeout; the unmutated helper returns at once, a helper that opens the pipe hangs.
* **The text ignores the tree.** The first text is byte-identical for different unfilled files, including one holding terminal control sequences. The second is byte-identical for a link, a link whose target name is distinctive, a link above the path, a directory, a pipe, a non-UTF-8 file and a dangling link. Neither contains file content, the link's target, an OS error text, or an escape character.
* **`main` prints it on every install path that selects the module.** A no-terminal install (`--non-interactive`, and separately a non-tty standard input) prints the first text on standard output and exits 0. An interactive install that skips every tier prints it. An interactive install that fills a tier prints nothing. A filled mapping is silent. An install without the module (a `solo-greenfield` install, and a moderate preset with the module removed) prints neither text. *Red when:* the helper is stubbed to return `[]` (the install-path rows fail).
* **The old interactive-only line is gone,** and the interrupt line stays: `kept the FILL ME stub` no longer appears in `cli.py`.
* **The engine meets the whole corpus.** `_mapping_is_unfilled` carries the same widened row rule as the checker, and the engine's column of the spelling table, and all 108 generated files, are asserted against it exactly. *Red when:* U+2028 is dropped from the engine's break set while the checker's is intact (M8b), or the engine's row rule reverts to the anchored pattern (M7b).
* **`lockfile.py` changes by one comment here** (the lockfile reader's code change is C4). It states the answer to its own revisit note: keep the reuse of the write guard on a read, and open the file through `_read_regular_bytes`, which checks the file type on the descriptor. No `lockfile.py` symbol is CHANGED by this chunk, and `git diff` on the file shows comment lines only.
* **Exit codes are unchanged** for every install path; the notice changes no code.

### C4 -- The safe writes

C4 may land as up to five commits sharing the label, in this order, each with its own red-then-green record: (a) the two writer helpers; (b) the capture; (c) the install-record committer; (d) the other lockfile writers and the lockfile reader; (e) the `.gitignore` append. Two parts are **new to the plan since its reviews**: the writers and the reader in (d) were folded in by the Maintainer after both plan reviews had read it, so **no plan reviewer read their design** (the reviews named the functions, not this design). Part (d) is therefore named for the code review and the Security Review in C6.

#### (a) The writer helpers

C4 adds two private functions to `bootstrap/_scaffold/security.py` (P17):

* `_stage_exclusive(path, data, target)` returns the path of a staged temporary file. It runs `_assert_safe_write(path, target)` (the write-time guard on the final name), then creates `path`'s name plus a dot, `secrets.token_hex(8)` and `.tmp`, beside it, with `os.open(..., O_WRONLY | O_CREAT | O_EXCL | O_NOFOLLOW | O_BINARY, 0o666)` (flags by `getattr`, as above). It writes all the bytes through the descriptor. If the final name already exists as a regular file, it sets that file's **read and write bits only** on the temporary file with `os.fchmod(fd, stat.S_IMODE(st_mode) & 0o666)` **on the descriptor**, before closing it, where `fchmod` exists. It then runs the guard on the temporary path. If anything fails after the creation, it removes **only the temporary file it created**.
* `_write_by_replacing(path, data, target)` calls `_stage_exclusive`, then `os.replace(tmp, path)`, and removes its temporary file if the replace fails.

* **The helpers' behaviour, tested once** (`TestWriteByReplacing`, in `test_security_leaf.py`). (1) With `secrets.token_hex` fixed to a constant, a hard link, a symbolic link, a dangling link, a named pipe, a folder and a socket planted at the temporary name each make the creation raise an `OSError`; the target is unchanged and **the planted object still exists afterwards** (cleanup removes only what the call created). *Red when:* `O_EXCL` is dropped, or cleanup removes a name it did not create. (2) An old file with mode `0o4755` yields a new file with no setuid, setgid, sticky or execute bit; `0o640` stays `0o640`; a new file gets the mode a plain write gives under the umask. The mode tests skip where the platform has no POSIX modes. *Red when:* the `& 0o666` mask is dropped. (3) A wrapper swaps the temporary path for a symbolic link to a victim file of mode `0o600` just before the mode is set: the victim's mode is unchanged and the replace is refused. *Red when:* the mode is set by path (`os.chmod`) or the guard on the temporary file is dropped. (4) If `os.replace` is made to fail, no `*.tmp` file is left and the target is unchanged. (5) A link swapped onto the final name before the call is refused by the write-time guard. (6) With `O_NOFOLLOW`, `O_BINARY` and `fchmod` removed from `os`, the helpers still import and write.

* **The inventory for the helpers.** `_stage_exclusive` calls the guard directly, so it joins `_GUARDED_WRITE_FUNCS`, and `SECURITY_MUTATIONS.md` gains a Class A row for each helper; the callers that reach the guard only through a helper (`_cmd_init_lock`, `_cmd_finalize_lockfile`) are named in the row for `_write_by_replacing`. *Red when:* `_stage_exclusive` stops calling the guard (`test_security_leaf` fails).

#### (b) The capture

The order inside `capture_model_selection_mapping`:

1. return `False` at once if the install is non-interactive or the path is not a regular file;
2. **the early guard,** `_assert_safe_write(mapping, target)`, before any read, print or prompt;
3. a read through `_read_regular_bytes` and a strict UTF-8 decode, in a `try`; a file that cannot be read or is not text is left alone and the function returns `False`; a file that is not unfilled returns `False`;
4. the prints and prompts (the family wording);
5. after the answers, `_write_by_replacing(mapping, content, target)`: the write-time guard, the exclusive temporary file, the mask, the guard on the temporary file, the rename and the cleanup are the helper's.

The accepted text said these steps are "all inline". The reason given at the time was to add no AST symbol. The steps and their order are all still there; they live in a helper that seven callers share, so the recipe exists once, which is the better answer to the same security question.

* **A link at or above the mapping is refused before anything is asked** (`TestCaptureRefusesBeforeAskingAnything`). Called directly with a prompt that fails the test if it is ever called, and with standard output captured: for a link to a regular file and for a linked `dev/.cairn`, the prompt is not called, nothing is printed, a `ScaffoldSecurityError` is raised, and the outside file is byte-identical. A dangling link is not a regular file, so step 1 returns `False` and the helper gives it the second text. *Red when:* the early guard is removed.
* **A real install proves the capture itself refused, with a linked mapping file.** The accepted fixture was a linked `dev/.cairn` holding the files every earlier write needs. It is replaced, because the `.gitignore` repair's pending `create_dev_tree` guard makes that install stop earlier, in `create_dev_tree`, before the capture; the outcome (a real install proving the capture itself refused) is unchanged. The fixture: a real `dev/.cairn`, and a mapping that is itself a link to an outside regular file holding `FILL ME`. `_install_one` skips an existing destination, so nothing earlier refuses, and an interactive install (a faked terminal and prompt) reaches the capture. It asserts exit 2, the constant refusal line on standard error, **no text from the exception** (the link target uses a distinctive name that must be absent), and no lockfile. The linked `dev/.cairn` stays in the direct-call test above. *Red when:* the catch prints the exception, or the fixture stops before the capture (the assertion is on the capture's own line, so an earlier stop fails loudly).
* **The refusal line names a remedy and nothing from the tree (P6).** `error: model-selection capture refused (containment): dev/.cairn/model-selection-mapping.yml is a link or sits behind one. Replace it with a regular file, or install with --non-interactive and fill it by hand.` It is a constant; the test asserts the remedy sentence and the absence of any tree text. *Red when:* the remedy is dropped (M45).
* **A hard link at the mapping is harmless.** The mapping is a second name for an outside file holding `FILL ME`. After the capture the outside file is byte-identical, and the mapping is a fresh file with a link count of 1 holding the captured rows. *Red when:* the write goes into the old file (`write_text`).
* **A planted name cannot redirect the write,** shown once in the helper test (a). Here: a hard link and a symbolic link planted at the obvious fixed temporary names beside the mapping (the mapping's name with `.tmp` appended, and a leading-dot variant) leave the capture completing and both outside files byte-identical.
* **A link swapped in while the person answers is refused at write time.** A prompt that replaces the mapping with a symbolic link as it "answers" makes the capture raise, and the outside file is byte-identical. *Red when:* the write-time guard is removed.
* **The captured file carries read and write bits only.** A mapping with mode `0o640` is `0o640` afterwards; a mapping with mode `0o4755` yields no setuid, setgid, sticky or execute bit.
* **An unreadable mapping does not crash the install.** A non-UTF-8 mapping, a directory and a named pipe at the path: an interactive install exits 0, the file is unchanged, and the second notice text prints (C3).
* **A mapping that is already filled is never touched.** The hand-filled stub with its comments kept, interactive: the prompt is never called and the bytes are unchanged.
* **The asymmetry is pinned.** Non-interactive with a linked mapping: exit 0, the second text, nothing written. Interactive: exit 2, nothing written, no lockfile. Re-running the interactive install over that tree afterwards exits 0 and writes the lockfile.
* **Family, never a version** at the two engine sites in the table (3 and 4): the prompt reads `<tier> tier -- model family, not a version (blank to skip):` and the header carries the line quoted there.
* **The docstring says where the capture runs** (`TestCaptureDocstringNamesWhereItRuns`). It no longer says the capture runs at `--adopt-module` time; it says the capture runs at install time, and that `--adopt-module` and `upgrade` only print the notice. *Red when:* the old sentence returns.
* **The inventory, additions only.** `capture_model_selection_mapping` and `_write_stage` join `_GUARDED_WRITE_FUNCS`, beside whatever the repair's answer added there, and `test_guarded_write_functions_still_call_a_containment_guard` passes. `SECURITY_MUTATIONS.md` gains the capture's own Class A row. The opening paragraph, as the repair's answer left it, gains the capture's catch (a constant line, exit 2) and nothing else; the `seed_gitignore` row gains this plan's behaviour as an added sentence, not a rewrite. At C4's gate the paragraph, the `seed_gitignore` row and `_GUARDED_WRITE_FUNCS` are all re-read at the parent. *Red when:* the capture's call to the guard is removed (`test_security_leaf` fails).

#### (c) The install-record committer (`_commit_lock_and_caches`)

Folded in at the Maintainer's instruction (`TestLockCommitWritesThroughExclusiveTemporaries`, in `test_upgrade_module_additions.py`). The function stages each cache and the lockfile with `_stage_exclusive` and renames them in the order it uses today, caches first and the lockfile last, the preflight guards before any write staying. It removes **all** of its staged temporaries, and only those, if it fails before the renames are done.

* **A hard link at the old fixed name is harmless, red then green.** At the parent, a hard link to an outside file planted at the lockfile's old temporary name (its name with `.tmp` appended) makes the function overwrite the outside file with lockfile text; the test fails there for that reason, and the commit body names the parent. After the change the outside file is byte-identical and the lockfile is right. The same for a cache's old temporary name. A symbolic link planted at either name is harmless: the commit completes and the outside file is unchanged. *Red when:* either temporary file is written by name with `write_text` or `write_bytes`.
* **Both callers are covered,** listed from the tree by searching for `_commit_lock_and_caches(`: `_cmd_adopt_module` and `_cmd_adopt_collisions`. A real `--adopt-module` run and a real `--adopt-collisions` run, each with links planted at the old names, exit 0 and leave the outside files byte-identical.
* **Nothing is left behind, and permissions are as before.** After a success there is no `*.tmp` file in `dev/.cairn/` or the base-cache folder. After a forced failure of the lockfile rename, the lockfile's temporary file is gone, and the existing `test_commit_lock_and_caches_is_atomic_on_lockfile_failure` passes unedited. Under umask 022 a new lockfile is `0o644`, which is what the `write_text` it replaces gave, and an existing lockfile of mode `0o664` stays `0o664`.
* **The inventory.** The `_commit_lock_and_caches` row in `SECURITY_MUTATIONS.md` says the temporaries are created exclusively; the function stays in `_GUARDED_WRITE_FUNCS` and still calls the guard.

#### (d) The other lockfile writers and the lockfile reader

Folded in at the Maintainer's instruction after both plan reviews (*Answered by the Maintainer after the plan opened*, item 5). **No plan reviewer read this design.** Four functions write `dev/.cairn/cairn-lock.yml` in place today, each with `write_text`: `write_install_lockfile` (`install.py`), `_cmd_init_lock`, `_cmd_finalize_lockfile` and `_apply_upgrade` (`upgrade.py`, its final lockfile write). Each now calls `_write_by_replacing(target / _LOCKFILE_REL, _emit_lock_yaml(...).encode("utf-8"), target)`, with no other change to what it writes. `read_lockfile` (`lockfile.py`) reads through `_read_regular_bytes`: it returns `None` for an absent path and for an unparseable body, as before, and raises `ScaffoldSecurityError` for a link, a folder, a pipe or any other file that is not a regular one. A hard-linked lockfile is read normally (no `single_link`): a read through a hard link writes nothing. The set of lockfile writers is listed from the tree, not from this plan: a search of `bootstrap/_scaffold/` for writes to `_LOCKFILE_REL` finds `_write_by_replacing`, `_stage_exclusive` and no `write_text` (apart from the base-cache and swap writes named below).

* **Each writer is red then green** (`TestLockfileWritersWriteByReplacing`, parametrized over the four, through their real entry points, in `test_upgrade_module_additions.py`). A hard link planted at the lockfile's own name, pointing at an outside file, is written through at the parent: the outside file is overwritten, and the test fails there for that reason, the commit body naming the parent. After the change the outside file is byte-identical and the lockfile is a fresh file with link count 1. The fixtures: install and `upgrade --init-lock` over a hard link to an outside file holding junk (so the existing-lockfile branches do not intervene); `upgrade --finalize` and `upgrade --apply` over a hard link to an outside copy of a real lockfile. *Red when:* any one writer is reverted to `write_text`.
* **A symbolic link at the lockfile's name is refused as before** (the guard stays); the outside file is byte-identical and the exit code is the table's.
* **The reader never hangs and never follows** (`TestLockfileReaderRefusesAnythingButARegularFile`). A named pipe at the lockfile path is refused inside a timeout (a subprocess); a symbolic link, a dangling link and a folder are refused; an absent path gives `None`; a junk body gives `None`; a valid body gives its dict, so the existing tests pass unedited; a link swapped in just before the open is refused. The callers of `read_lockfile`, listed from the tree by searching for `read_lockfile(`, are unchanged in what they pass; a refusal reaches them as a traceback and exit 1, the class the oracle pins (the exit-code table gains the row). *Red when:* the reader reads by path with `read_text`, or drops `O_NOFOLLOW`, `O_NONBLOCK` or the regular-file check.
* **Permissions are as before.** A lockfile of mode `0o664` stays `0o664` after `--finalize`, and a new lockfile gets the umask default. A lockfile with a setuid bit set by someone else comes out without it.
* **Not folded in, and named:** the base-cache writes in `write_install_lockfile` and `_apply_upgrade`, `_apply_upgrade`'s swap writes, `_write_stage`, `_install_one` with `--force`, and the profile writes. They are the wider in-place class (*Named residuals*, *Dispositions*).

#### (e) The `.gitignore` append

Folded in at the Maintainer's instruction (`TestGitignoreSeedWritesByReplacing`, in `test_intents_tool.py` beside the repair's tests). `seed_gitignore` works in bytes (P14, P15):

* **The preflight (a call with no entries)** runs the guard and an `lstat`, and reads nothing. It refuses a `.gitignore` that is not a regular file (a folder, a pipe, a socket, a device) and a regular file whose link count is above 1, each with a `ScaffoldSecurityError` of fixed text that names `.gitignore` and not the tree. A non-UTF-8 regular file passes.
* **When entries must be written,** it reads through `_read_regular_bytes(path, single_link=True)`, compares whole lines by bytes (an entry already present is not added again, CRLF files included), checks `os.access(path, os.W_OK)` on an existing file, and writes by `_write_by_replacing`. A dry run reads the same way and writes nothing.

* **A hard-linked `.gitignore` is refused, red then green (GS-SR-4).** At the parent, a `.gitignore` that is a hard link to an outside file lets install, `--stage` and `--adopt-module` exit 0 with the outside file appended (measured in that review); the new tests fail there for that reason and the commit body names the parent. After the change install, `--stage`, `--adopt-module` and `--apply` each exit 2 with the `.gitignore` refusal line, before any write, and the outside file is byte-identical. A direct call that must write raises `ScaffoldSecurityError` and leaves both files unchanged. A `.gitignore` with link count 1 behaves exactly as before. *Red when:* the link-count check is dropped from the preflight (M31) or from the reader's `single_link` (M30).
* **The refusal names a fix that is true for a hard link (MM-SR-4).** The exception text is fixed: `.gitignore` has other names (its link count is above 1); make it a file of its own, by copying it to a new name and moving that over `.gitignore`. The callers print their prefix, this text and, where the repair's answer added one, a remedy line. At the parent of this chunk, C4 reads that remedy line in `main`, `_cmd_adopt_module` and `cmd_upgrade`; if it tells only to replace a link, C4 reworded it so it is true for a hard link too. A test pins the wording for the hard-link case: it contains "file of its own" and not "replace the link". *Red when:* the hint is the link hint (M46).
* **Every error from the open becomes the refusal.** Every `OSError` from the reader's open, except "no such file", is a `ScaffoldSecurityError` of fixed text, so a socket or an unreadable file does not end in a raw `OSError`.
* **A link that appears after the check cannot redirect the write or the read, tested deterministically (GS-SR-3).** The race is the span between the guard and the write, which a test cannot time. Three stand-ins make the swap happen at exact points by patching a call the code makes: (a) the open is wrapped so that, just before the real open, `.gitignore` is replaced by a symbolic link to an outside file: the open is refused, `ScaffoldSecurityError` is raised, and the outside file is byte-identical and not copied into the project; (b) the same with a hard link swapped in before the open: refused by the descriptor's link count, nothing copied; (c) `secrets.token_hex`, which runs after the read and before the write, is patched to swap `.gitignore` for a symbolic link and then for a hard link (two runs) and return a normal token: the outside file is byte-identical, and afterwards `.gitignore` is a regular file with link count 1 holding the old lines and the new ones. *Red when:* `O_NOFOLLOW` is dropped (a, M29), the descriptor's link-count check is dropped (b, M30), or the rename is replaced by an in-place write (c, M28).
* **The racing probe is repeated once as evidence.** The Security Review's probe (a thread flipping `.gitignore` between a file and a link for 3,000 calls; 99 reached the outside file on `3ba6f230`) is run against the finished engine in a throwaway copy: 0 of 3,000 reach the outside file. It is recorded in the verification record, not pinned as a test, because it is a race.
* **A non-UTF-8 `.gitignore` no longer stops an apply, red then green (GS-SR-5).** At the parent, `--apply` over a `.gitignore` holding the bytes `\xff\xfe` plus a line exits 1 with a traceback before anything is written, though the apply adds no ignore line; the test fails there for that reason. After the change the apply proceeds and exits 0 with the bytes untouched, `--stage`, install and `--adopt-module` over that file append their lines and keep the original bytes exactly (compared as bytes), and the preflight makes no read at all (the test patches the open to fail the test if it is called). *Red when:* the preflight reads again (M33), or the file is decoded (M34).
* **A folder, a pipe, a socket or a device named `.gitignore` is refused early, and nothing hangs (MM-PR-7).** The preflight refuses each with the same exit-2 line and writes nothing, so an install over a folder named `.gitignore` is not left half-done and `--stage` leaves no stage behind. The folder case is possible, since git can carry `.gitignore/x`. A pipe never blocks (a subprocess with a timeout). The first-write refusal stays as a backstop, and only the non-UTF-8 case changes behaviour from the repair's. *Red when:* the kind check is dropped from the preflight (M43).
* **A read-only `.gitignore` is refused as before.** An existing `.gitignore` of mode `0o444` makes a seeding that must write raise `ScaffoldSecurityError` and leaves the file unchanged; a rename needs write permission on the folder only, so without the `os.access` check the file would be replaced. *Red when:* the check is dropped (M42).
* **Behaviour that must not change:** appends are idempotent, a missing trailing newline is supplied, a dry run lists what it would add and writes nothing, and a `.gitignore` that is absent is created. The existing tests of those properties pass unedited. The new file carries only the old file's read and write bits (`0o640` stays `0o640`; `0o4755` yields none of the special or execute bits), a new one is created with the mode a plain write gave (`0o644` under umask 022), and no `*.tmp` file is left after a success or after a forced failure of the rename. The owner, the group and any extended attributes of a replaced file are the installer's and the folder's, not the old file's (*Named residuals*).
* **Every writer is covered:** the call sites that pass entries, listed from the tree by searching for `seed_gitignore(`, all go through the one function; the hard-link refusal is shown through the four real entry points (install, `--stage`, `--adopt-module`, `--apply`).
* **The inventory.** The `seed_gitignore` row in `SECURITY_MUTATIONS.md` gains a sentence for this plan's behaviour (link count and kind checked without reading; reads by descriptor; writes by exclusive temporary file and rename). The repair's text in that row is not rewritten. `bootstrap/SAFETY.md`'s "Documented residual risks (Layer 4)" gains one sentence: a won race overwrites rather than appends, and the capture, the install-record committer, the lockfile writers and the `.gitignore` append no longer have the window.

#### For all of C4

* **The AST effect is as declared** (*Frozen files, AST and the oracle*), as set differences, never counts. No new top-level symbol beyond the five named there.
* **Every caller of the helpers is listed from the tree** (a search for `_write_by_replacing(` and `_stage_exclusive(`) and has a test that reverts that caller alone.

### C5 -- The notice on adopt and upgrade

* **Five call sites,** listed from the tree (`grep` for `model_selection_notice_lines`): `main`, `_cmd_adopt_module`, and three in `cmd_upgrade`. Each prints for a stub and is silent for a filled mapping.
* **Adopt:** `--adopt-module model-selection` over a tree that has the stub prints the first text right after the "Adopted module" line. Adopting another module prints nothing. A refused adopt (a linked `.gitignore`) prints no notice.
* **`--plan` and `--stage`** print it as their last output, and are **silent on a tree where the file is absent** (the mapping that a delivering apply will add).
* **`--apply` prints it only after a successful apply.** The delivering apply: a tree whose mapping is absent from disk and from the lockfile is planned (silent), staged (silent), then applied; the file appears and the notice prints. A refused apply prints none: a leftover conflict marker (returns 1) and a linked `.gitignore` (exit 2). *Red when:* the call moves ahead of `_apply_upgrade`, or runs when the return code is not 0.
* **The notice sits outside the `try`.** A failure while printing it cannot be reported as an apply refusal.
* **A project without the module** gets neither text from `--plan`, `--stage` or `--apply`, nor from adopting another module (P1, CL-3).
* **Exit codes are unchanged** on every path in the table above; the existing refusal tests in `test_intents_tool.py` and `test_upgrade.py` pass unedited.
* **The quiet case is documented, not hidden.** If a step after the lockfile write refuses (the `.gitignore` seed for a newly added skill), the apply has delivered the file and exits 2, so no notice prints; the next `upgrade --plan` does.

### C6 -- Boundary B, the evidence, and the record

* **The record is complete,** with the template's fields, and it lists the new node IDs and the one node that left. For the Maintainer's ceremony it records the AST derivation as a cross-check only, never as an input: the sets in *Frozen files, AST and the oracle* at P and at T, each with its digest, and the digests of the new and re-keyed symbols at T. The ceremony works its own figures out (chunk M).
* **The mutation ledger** (*Verification*) is complete: every row has a result of killed, survived or equivalent, beside an unmutated control run. Equivalence is measured: a behaviour test through the real entry point passes under the mutation, and where another site is said to recover the value, mutating that site fails. An unmeasured equivalence is reported as a survivor. A survivor is fixed in its chunk, and the record is redone.
* **The stub merge measurement** (*Verification*) is recorded, with the three outcomes and the fail-closed apply.
* **The AST derivation matches the declared delta, as sets:** CHANGED(T) equals CHANGED(P) plus `capture_model_selection_mapping`, `write_install_lockfile`, `_cmd_init_lock`, `_cmd_finalize_lockfile`, `_apply_upgrade` and `read_lockfile`; the known-new mismatches at T are exactly `{_commit_lock_and_caches}`; NEW(T) minus NEW(P) is exactly the five named; MISSING and DUPLICATE are empty; and the digest of each of `main`, `_cmd_adopt_module`, `cmd_upgrade` and `seed_gitignore` at T differs from its digest at P. If the repair's answer has landed, P already holds `create_dev_tree`; no number appears in the criterion.
* **The frozen list matches:** the seven, derived by script, with the control, and no new frozen test file (the new tests go in files already on the list).
* **The code-review handoff names the late additions.** The implementation's code review and its Security Review are told, in the handoff, that the four other lockfile writers and the lockfile reader (C4 (d)) and the `.gitignore` append (C4 (e)) were folded in after both plan reviews, and must each be covered explicitly: the review's record lists each of the seven helper callers and the reader's callers by name, with its finding or its "read, nothing found". A review that names fewer is incomplete.
* **The install contract is unchanged:** `scaffold.py --manifest` output is byte-identical to the parent's.
* **`git diff --stat` over the range** shows none of the files under *Not touched*, and `lockfile.py` as its comment and `read_lockfile` only.

### The security findings ledger

Every finding the accepted text carried into this plan, and where it is closed. Nothing is dropped.

| Finding | What the accepted text requires | Where it is checked |
|---|---|---|
| SEC-1 | the plan starts from a tree holding the `.gitignore` repair and makes no containment claim about it | the entry condition (C1's gate). C4 (e) does change `seed_gitignore`'s containment, so the plan now makes a containment claim about it, pinned by C4 (e) |
| SEC-2 | the upgrade notice after an action finishes: after `--plan` and `--stage` reports, after a successful `--apply` only; the delivering apply tested | C5 |
| SEC-3 | an early guard, a write-time guard, a temporary file beside the mapping, a guard on it, `os.replace`; the hard link named in S5 | C4 (a), (b); S5 below |
| CL-1 | the temporary file created exclusively, so a waiting hard link or link cannot redirect the write | C4 (a) (`O_CREAT` with `O_EXCL`, the forced-collision matrix); mutations M15, M26 |
| SEC-4 | the true exit-code story; the capture's line a constant; the test proves the capture itself refused; the quiet side and the asymmetry stated; `SECURITY_MUTATIONS.md` corrected | *What the exit codes are now*; C4 |
| CL-2 | re-derive against HEAD; do not apply the old correction as written; keep the capture's catch with its constant line | the same section; C4 |
| SEC-5 | the residual named as a class; every value scanned; the bare row test anchored | C1; *Named residuals* below |
| CL-4 | both spellings in the corpus; widen the pattern or name them | C1 (P3) |
| SEC-6 | `lstat` first, never open a non-regular file; the capture treats an undecodable file as the helper does | C3, C4 |
| CL-3 | a missing mapping stays silent, first; a dangling link is not missing; the wording "That file was not changed" | C3 (P5), C5 |
| SEC-7 | a generated corpus; the U+2028 mutation; the version gap named | C1, C3; mutation M8; *Named residuals* |
| SEC-8 | the revisit note in `lockfile.py` answered in the comment; the file-type check at the call site; `_write_stage` in `_GUARDED_WRITE_FUNCS` | C3, C4 |
| The hard-link defect in the install-record writer (found while planning; folded in at the Maintainer's instruction) | exclusive temporary files, with planted-link tests and mutants | C4 (c); mutations M24-M27 |
| GS-SR-3, GS-SR-4, GS-SR-5 of the `.gitignore` repair's Security Review (folded in at the Maintainer's instruction) | `seed_gitignore` reads through the descriptor reader, refuses a hard link, writes by exclusive temporary file and rename, and its preflight no longer reads | C4 (e); mutations M28-M31, M33-M34, M42-M43 |
| The four other lockfile writers and the lockfile reader (folded in at the Maintainer's instruction, after both plan reviews) | exclusive temporary files and the descriptor reader, red then green, a pipe that must not hang | C4 (d); mutations M47-M51; C6 handoff |
| Plan review: MM-SR-1 (blocks) | the mode mask and `fchmod` on the descriptor | C4 (a); mutations M35, M37 |
| Plan review: MM-SR-2 | merge keys refused | C1; mutation M39 |
| Neutrality of the shipped text | every quoted shipped block scanned | measured here; `--sub neutrality` stays zero at every chunk |

## Scope delta

**Scope delta**: degraded -- one unit, **allowed by the Maintainer.** The baseline is the proposal as accepted. Every outcome maps to a chunk:

| Accepted outcome | Chunk |
|---|---|
| a notice on every install, including a no-terminal one | C3 |
| the notice on `--adopt-module` and on `upgrade --plan`, `--stage`, `--apply` (after a successful apply) | C5 |
| the II-5 item and the fourth allowed match | C2 |
| the check skips full-line comments; a mapping needs a row; values scanned with PyYAML; the anchored and widened row test; YAML line breaks | C1 |
| the seed and its Waiting row in two presets | C2 |
| Cairn's suite fails if its mapping returns to the stub | C1 |
| the capture refuses a link before any question, exits 2, writes by rename; the hard link and the planted name closed | C4 |
| the module document's paragraph and its corrected sentence | C2 |
| family, never a version, at every site, and the stub's example edit | C2, C3, C4 |
| the upgrade-conflict cost measured on the real commit | C6 |
| the true exit-code story and `SECURITY_MUTATIONS.md` corrected; `_write_stage` in the pinned set | C4 |
| the comment in `lockfile.py` | C3 |
| the named residuals recorded where a reader finds them | C1, C3 and *Named residuals* |
| the mutation ledger and the generated parity corpus | C1, C3, C6 |
| the scoped finalizes of the checker and the module document | C1, C2 |
| Boundary B full | C6 |

Not in the baseline: Q4, which the Decision left out of this contract.

* **The seed in `solo-greenfield`.** The opening text said "installs from a preset get one". That preset's own settings (`complexity: simple`) never select the module, so the seed could never render, and it would turn two pinned tests red. **disposition**: wontfix, for that reason. The outcome, a durable line, is delivered in the two presets that install the module; a solo adopter who raises complexity still gets the notice and the II-5 item. The Maintainer's allowance, quoted: the answer to Q2 was "Allow two presets", and the Decision was:

  > "accept as answered"

**Additions, not removals,** in three groups.

* **At the Maintainer's instruction, quoted under *Scope*:** the install-record committer's fix (`_commit_lock_and_caches`); the three `.gitignore` points (`seed_gitignore`: the race, hard links, the preflight's read); the four other lockfile writers and the lockfile reader.
* **Named by the accepted text:** the `upgrade` notice, the II-5 item, the row requirement, the family wording, the module-document fix, the `lockfile.py` comment.
* **The plan's own, in response to the plan reviews and what was found while planning, and not at the Maintainer's instruction:** the `RecursionError` catch and the merge-key refusal in the checker (P8); the shared reader and writer helpers and their five new symbols (P16, P17); the mode mask; the `os.access` check and the folder-or-pipe refusal in the `.gitignore` preflight; the remedy sentences on the two new refusals; one sentence in `bootstrap/SAFETY.md`. Each is small, each is tested, and none takes away an accepted outcome.

**Means changed, outcomes kept:** the capture's steps "all inline" now live in the shared writer helper (C4 (b)); and the accepted real-install test for the capture's refusal now uses a linked mapping file in place of a linked `dev/.cairn`, because the repair's pending guard makes the old fixture stop earlier (C4 (b)).

## Verification

**Boundary A (iteration, scoped).** Each chunk runs the tests that own what it touches, found by searching `bootstrap/tests` for each touched symbol, file and flag, and not by expectation. All are in `bootstrap/tests/`. Plus the standing gates: `python scripts/check_cairn.py` and `python scripts/claim_check.py <file>` for each edited document; `python scripts/quality_gate.py --sub neutrality`; `--sub redundancy` for scripts; and `python bootstrap/verify_integrity.py --target .` after any finalize.

| Chunk | Tests |
|---|---|
| C1 | `test_model_selection_stub.py`, `test_scaffold.py` (module registration), `test_security_lint.py`, `test_security_check.py` (the Bandit gate sees the script) |
| C2 | `test_model_selection_stub.py`, `test_onboarding_seed_roster.py`, `test_onboarding_slot_substitution.py`, `test_presets.py`, `test_profiles_smoke.py`, `test_active_surfacing_render.py`, `test_trigger_evaluation_action.py`, `test_skills_onboarding.py`, `test_onboarding_review_tiers.py`, `test_onboarding_activation_helper.py`, `test_deferred_task_store.py`, `test_default_security_stance.py`, `test_profile_grammar.py`, `test_scaffold.py` |
| C3, C4 | `test_model_selection_stub.py`, `test_upgrade_module_additions.py`, `test_security_leaf.py`, `test_install_module.py`, `test_intents_tool.py` (the `.gitignore` refusals), `test_scaffold.py`, `test_ast_attest.py` (the same 2 nodes red, no more), `test_oracle.py`, `test_oracle_activation.py`, `test_lockfile_module.py`, `test_lockfile_provenance.py`, `test_verify_integrity.py` (it reads the lockfile), `test_upgrade.py` (`--init-lock`, `--finalize`, `--apply`), `test_skills_upgrade.py`, `test_security_capability_install.py`, `test_security_verification.py` |
| C5 | the C3 and C4 set plus `test_upgrade.py`, `test_upgrade_module.py`, `test_upgrade_module_additions.py`, `test_upgrade_side_door_parity.py`, `test_skills_upgrade.py`, `test_lockfile_provenance.py`, `test_security_stack.py`, `test_portable_security_sweeps.py` |

This is not a confident bound. 39 test files import the scaffold's entry point or its facade, and the engine files here sit on the install path of all of them, so **Boundary B is the real check.** If `board-as-basis` has landed first, add its contract test and `test_replacement_tools.py` to the C2 row, since the seed test reads the board's `--maintainer` output.

**Test classes this plan adds,** named for the property each pins. All are in `bootstrap/tests/test_model_selection_stub.py` unless noted.

* **C1:** `TestCommentsAreNotPlaceholders`, `TestAMappingNeedsAtLeastOneRow`, `TestParsedValuesAreScannedWhenYamlIsPresent`, `TestMergeKeysAreRefused`, `TestCheckerMessagesCarryNoParsedValue`, `TestBarePathResidualIsPinned`, `TestValueScanVisitsEachObjectOnce`, `TestThisRepositorysMappingIsFilled`, and `TestEngineAndCheckerAgreeOnUnfilled` (the checker side and the spelling table; the engine side joins in C3).
* **C2:** `TestStubExampleNamesAFamilyNotAVersion`, `TestAcceptanceChecklistNamesTheMappingCheck`, `TestShippedWordsArePinnedByExactString`, `TestFamilyNotVersionReachesEverySite` (eight sites; grows in C3 and C4). In `test_onboarding_seed_roster.py`: the seed renders at moderate and complex in the two presets, strips at simple, is absent from `solo-greenfield`, survives a removed module, is listed by `board.py --maintainer`, and a live install writes a clean lockfile.
* **C3:** `TestReadRegularBytesRefusesAnythingElse` (in `test_security_leaf.py`), `TestNoticeOnEveryInstallPath` (the install rows), `TestNoticeTextIgnoresFileContent`, `TestNoticeNeverOpensAnythingButARegularFile`.
* **C4 (a):** `TestWriteByReplacing` (in `test_security_leaf.py`). **(b):** `TestCaptureRefusesBeforeAskingAnything`, `TestCaptureWritesByReplacing`, `TestCaptureLeavesUnreadableMappingsAlone`, `TestCaptureNeverClobbersAHandFilledMapping`, `TestCaptureRefusalIsAConstantLine`, `TestCaptureDocstringNamesWhereItRuns`. **(c):** `TestLockCommitWritesThroughExclusiveTemporaries` (in `test_upgrade_module_additions.py`). **(d):** `TestLockfileWritersWriteByReplacing` and `TestLockfileReaderRefusesAnythingButARegularFile` (in `test_upgrade_module_additions.py`). **(e):** `TestGitignoreSeedWritesByReplacing` (in `test_intents_tool.py`).
* **C5:** `TestNoticeOnEveryInstallPath` gains the adopt and upgrade rows; `TestNoticeComesOnlyAfterAnApplySucceeds`.
* **Removed:** `TestFidelityCheck::test_fill_me_in_comment_fails`, replaced by `TestCommentsAreNotPlaceholders`.

**Boundary B mode**: **full.** The refusal rules in `AGENTS.md` settle it, four ways:

1. **A contract surface and the install path are touched.** `install.py`, `cli.py` and `upgrade.py` print new output on every install and upgrade, and the published `--manifest` and the lockfile must be shown unchanged. Bounded mode refuses.
2. **A trust-ceremony surface is touched.** The scaffold and merge engine is a high-risk surface that `AGENTS.md` names, and the work adds a containment guard, two shared writer helpers and a shared reader, an exit-code change, and changes how eight engine functions write or read.
3. **A frozen file changes and the pinned collection moves.** Six frozen files change, a seventh is written by the AST ceremony, one pinned node leaves, and new nodes join.
4. **A verbatim adopter script changes.** The checker is shipped byte for byte, so its behaviour reaches every adopter.

Uncertainty resolves to full, and the accepted text says full.

**How it runs.** After C5, against a clean, unchanged commit, under the canonical interpreter (Python 3.13.x, `/Users/kendal30/conda_envs/lhm/bin/python3.13`):

```
CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
python scripts/quality_gate.py --sub neutrality --sub redundancy
```

then `check_cairn.py`, and `claim_check.py` on each edited file. Run it from a separate worktree at the tested commit: a worktree shares refs, so the gate anchor is present, and other sessions' uncommitted files stay out of the count. Name the interpreter next to every figure.

**Expected non-pass,** each disposed of rather than treated as noise:

* **`test_ast_attest.py`: the same 2 nodes** (`test_committed_baseline_accounted_for_across_the_engine_package` and `test_ast_gate_passes_over_the_full_scaffold_module_set`) fail, as they do at the base, and for the same reason: the baseline is stale. The disposition shows the CHANGED set equals the declared delta, so nothing unintended moved, that the only known-new mismatch is `_commit_lock_and_caches`, and that the failure ends when the Maintainer runs the combined ceremony.
* **`test_gate_manifest.py`:** no expected failure. Changed frozen bytes do not redden it.
* **The neutrality leg:** `fail=0`, no expected failure.

**Mutation ledger.** Run in a separate copy of the tested commit (a detached worktree, in a fresh empty folder, never the shared tree), each mutant beside an unmutated control run. Sets are listed from the tree, not the diff.

| # | Mutant | Killed by |
|---|---|---|
| M1 | the checker stops skipping full-line comments | the hand-filled stub test |
| M2 | the checker treats a leading tab as blank | the tab members of the corpus |
| M3 | the checker uses `str.splitlines()` | the form-feed members of the corpus |
| M4 | the bare row requirement is dropped | the no-row test |
| M5 | the PyYAML value scan is dropped | the block-scalar, escape, binary and set cases |
| M6 | the visited-set is dropped | the alias-document timeout |
| M7a | the checker's widened row pattern reverts to the anchored one | the three "agreed after widening" members of the spelling table |
| M7b | the engine's row rule reverts to the anchored one | the same members, engine column |
| M8a | U+2028 is dropped from the checker's break set | the generated corpus |
| M8b | U+2028 is dropped from the engine's break set | the parity corpus |
| M9 | `model_selection_notice_lines` returns `[]` | the install, adopt and upgrade rows |
| M10 | the notice helper reads the path by name, before any check | the named-pipe test |
| M11 | the missing-file branch is dropped | the no-module rows |
| M12 | the early guard is removed from the capture | the refuse-before-asking tests |
| M13 | the write-time guard is removed from `_stage_exclusive` | the swap-while-answering test, and the helper's final-name test |
| M14 | the capture writes the mapping in place with `write_text` | the hard-link test |
| M15 | `_stage_exclusive` uses a fixed temporary name written by name | the planted-names and forced-collision matrix |
| M16 | the notice call is removed from one site at a time: `main`, adopt, plan, stage, apply (the set of five, from `grep`) | the matching row, five mutants |
| M17 | the apply notice moves before `_apply_upgrade` | the delivering-apply test |
| M18 | the apply notice prints when the return code is not 0 | the refused-apply test |
| M19 | the Waiting line is dropped from one preset's seed at a time | the board-listing test, two mutants |
| M20 | "never a version" is removed from one of the eight sites in the table (C2), one at a time | the per-site parametrized test, eight mutants |
| M21 | Cairn's mapping is reset to the stub | the repository's-mapping test |
| M22 | the capture's guard is removed | `test_guarded_write_functions_still_call_a_containment_guard` |
| M23 | the capture's catch prints the exception text | the real-install refusal test |
| M24 | `_commit_lock_and_caches` stages the lockfile through a fixed name with `write_text` | the lockfile hard-link test |
| M25 | the same for a cache, with `write_bytes` | the cache hard-link test |
| M26 | `O_EXCL` is dropped from `_stage_exclusive` | the forced-collision matrix |
| M27 | the committer's cleanup of its staged temporaries on failure is dropped | the failure-cleanup test |
| M28 | `seed_gitignore` writes in place again | the swap-before-write stand-in (c), and the hard-link tests |
| M29 | `O_NOFOLLOW` is dropped from `_read_regular_bytes` | stand-in (a), and the reader matrix |
| M30 | the `single_link` check is dropped from the reader | stand-in (b) |
| M31 | the link-count check is dropped from the `.gitignore` preflight | the hard-link refusal through the four entry points |
| M32 | the cleanup removes a name the call did not create | the forced-collision matrix (the planted object must survive) |
| M33 | the `.gitignore` preflight reads the file again | the no-read test and the non-UTF-8 apply test |
| M34 | the `.gitignore` is decoded (`read_text`) | the non-UTF-8 byte-exactness test |
| M35 | the `& 0o666` mask is dropped in `_stage_exclusive` | the `0o4755` mode test |
| M36 | `_write_by_replacing` does not remove its temporary file when the replace fails | the failure-cleanup test |
| M37 | the mode is set by path (`os.chmod`) instead of on the descriptor | the swap-before-mode stand-in |
| M38 | the guard on the temporary file is dropped | the swap-before-mode stand-in |
| M39 | the merge-key refusal is dropped from the checker's loader | the merge-key chain (it times out) |
| M40 | the regular-file check is dropped from `_read_regular_bytes` | the reader matrix (folder, device) |
| M41 | `O_NONBLOCK` is dropped from `_read_regular_bytes` | the named-pipe test (it times out) |
| M42 | the `os.access` check is dropped from `seed_gitignore` | the read-only `.gitignore` test |
| M43 | the kind check is dropped from the `.gitignore` preflight | the folder and pipe preflight tests |
| M44 | a checker message echoes a parsed value | the ESC and BEL test |
| M45 | the capture's refusal drops its remedy sentence | the constant-line test |
| M46 | the hard-link refusal gives the link hint | the wording test |
| M47 | `write_install_lockfile` writes in place again | its hard-link test |
| M48 | `_cmd_init_lock` writes in place again | its hard-link test |
| M49 | `_cmd_finalize_lockfile` writes in place again | its hard-link test |
| M50 | `_apply_upgrade` writes its lockfile in place again | its hard-link test |
| M51 | `read_lockfile` reads by name with `read_text` | the reader's link, folder and pipe tests |
| M52 | the helpers' flags are built at import time without `getattr` | the test that removes the flags from `os` |

**The stub merge measurement** (C6, on the real commit). The real merge, with the parent's stub as the common base and the edited stub as theirs, over four of the adopter's files: (a) an untouched stub; (b) a hand-filled stub with its comments kept; (c) a file written by the interactive capture, whose header was rewritten; (d) a file whose header was rewritten by hand. Expected: (a) and (b) clean, (c) and (d) conflict. Then, for (c), `upgrade --apply` refuses while conflict markers remain and writes nothing. The author measured this on the drafted edit; C6 repeats it on the commit.

**Smoke checks** (C6). `scaffold.py --config <profile> --target <tmp> --non-interactive` prints the first text. `upgrade --plan` on that tree prints it. `board.py --maintainer --root <tmp>` lists the seed. The II-5 vendor-neutrality grep over a scratch install holding Cairn's filled mapping matches only that file, which is the fourth allowed class. The checker returns 1, 0 and 0 on the stub, a hand-filled stub and Cairn's file. `scaffold.py --manifest` is byte-identical before and after.

**Boundary C** is the code reviewer's, run after Boundary B. The points worth attacking:

* **The order inside the capture.** Is any read, print or prompt reachable before the early guard? Does the temporary file get a name another process can predict?
* **The silent cases.** Can any path print the second text for a project that never had the module, or stay silent for a stub?
* **The parity corpus.** Is it fitted to a claim, or does it contain a member that the engine and the checker disagree on? List the corpus members from the tree.
* **The late additions, one by one.** The four other lockfile writers, the lockfile reader and the `.gitignore` append were folded in after both plan reviews, so the code review and the Security Review read each of them for the first time. Name the seven callers of the helpers and every caller of `read_lockfile` (listed from the tree); for each, is there a path that still writes through an existing name or reads blindly?
* **The helpers' mode handling.** Can any file the helpers produce carry a setuid, setgid, sticky or execute bit from the file it replaced? Is the mode set on the descriptor in every path?
* **`seed_gitignore`'s three checks.** Between the preflight and the rename, is there a point where a link, a hard link or a pipe still reaches a read or a write? Is a non-UTF-8 file's every byte kept?
* **`_commit_lock_and_caches`'s temporary names.** Is any name predictable, any temporary left behind after a failure, any caller missed? Does the mode a new lockfile gets match today's?
* **The seed, read cold as an adopter.** Does the Waiting row make sense on day one, and does deleting it work?
* **The lockfile diff.** Confined to two records?

**Security preflight, re-answered where the chunking changes an answer.**

* **S2, can it fail.** The ledger above is the answer, and it runs once, at C6, against the finished commits. A surviving mutant sends the work back to its chunk.
* **S3, what fires it, over what.** The notice: `scaffold.py` install, `upgrade --adopt-module`, and `upgrade --plan`, `--stage` and `--apply`, over one fixed path. The check: an agent following II-5, a person running the script, `board.py --maintainer` showing the seeded row, and `TestThisRepositorysMappingIsFilled` in Cairn's suite. **Said plainly, nothing fires any of these unprompted.** Opened to the end: no git hook and no CI configuration runs the suite (`.git/hooks` holds only the work-intent pair, and Cairn has no CI). The test runs when a person or agent performs Boundary B, which every implementation plan requires, so its chain ends at a person or agent following `AGENTS.md`. The proposal's "only the suite reaches a machine" is therefore a test that exists, not a machine that runs it.
* **S5, who still wins.** Someone who can write the tree can enter plausible model names, edit the tree-local checker, or spell a placeholder so the bare path misses it. A link swapped in the last instant before the rename narrows the window to one rename and does not eliminate it; the threat model is "no concurrent filesystem attacker" (`bootstrap/SAFETY.md`, "Documented residual risks (Layer 4)"). **The hard-link case is closed by construction** for the seven callers of the writer helpers: the capture, `_commit_lock_and_caches`, the `.gitignore` append, and the four lockfile writers (exclusive creation, then a rename that never writes into the old file). It is **not** closed for any other in-place engine write (*Named residuals*), and the plan makes no claim about them. The permission bits a replaced file keeps are read and write only.

### Named residuals

* **Staleness.** Nothing reads `date_verified` or the re-verification field; the module paragraph says so.
* **A class, not a case, on the bare path and in the engine:** a value whose `FILL ME` is not spelled out on one non-comment line (a block scalar, a value folded over lines, a continuation, an escape, a tag) reads as filled, and so does a repeated `mapping:` key. The engine erring toward "filled" never overwrites and may stay quiet. With PyYAML the checker catches the class. Each needs a deliberate spelling by someone who could edit the checker anyway.
* **The bare path is stricter than PyYAML** for a one-line list whose first key is not `tier` and for a `tier:` inside another value (P3). That is the louder side.
* **A version gap.** An adopter's checker is whatever they last upgraded to, while the engine is current. Between `upgrade --plan` and `--apply`, a hand-filled file can be silent in the new engine and fail the old checker. The apply updates the verbatim checker and closes it. A comment on `_mapping_is_unfilled` says where the other copy lives and which test pins their agreement.
* A `FILL ME` in a trailing comment fails; in a leading comment it passes. One tier filled passes, as the module document allows. Invented but plausible names pass.
* **The second notice line is imprecise for a file with no rows** (P10), and there is no read-size cap (P9).
* **A profile that removes the module from a moderate preset** gets a Waiting row naming a file it lacks; a test pins it.
* **Non-interactive and interactive installs disagree on a bad mapping path** (exit 0 with a notice, and exit 2). Neither writes anything.
* **In-place engine writes through a hard link are not closed,** apart from the seven callers of the writer helpers. Seen and named: the module-merge conflict side-file (`slotmerge.py`); the base-cache writes in `write_install_lockfile` and `_apply_upgrade`; `_apply_upgrade`'s swap writes; `_write_stage`; `_install_one` with `--force`; the profile writes. No complete sweep of the engine was made. `_assert_safe_write` checks symbolic links, not link counts.
* **A row-shaped line that is not an item of `mapping`** reads as a row on the bare path and in the engine (three members of the spelling table). Each needs a deliberate spelling by someone who could edit the checker anyway.
* **A replaced file changes hands.** A rename leaves the replaced file's owner and group as the installer's and the folder's, and drops its extended attributes. Only the read and write bits are kept. A read-only `.gitignore` is refused (`os.access`), but the capture's mapping and the lockfile writers do not check it: a read-only mapping or lockfile is replaced where the plain write would have failed.
* **A folder or a pipe named `.gitignore` is refused early** (P15), as the repair made it; only a non-UTF-8 file's behaviour changes.
* **A hard-linked `.gitignore` is refused, not replaced** (P14); a user who linked it on purpose must unlink it.
* **The stub edit costs one merge conflict** for an adopter whose header was rewritten. `lhm` is one; keeping its side resolves it, and `--apply` refuses until then, so a half-merged mapping is never written.

## Dispositions

*Filled at archive-preparation.* Known now:

* **Q4, goodnight running the activation helper.** `defer`. The accepted text assigns it to the board: Revision 1 says "a separate board item at the next scrub, not in this change", and the Decision says it "is not part of this contract". The archive commit deposits the board row and quotes both, with the Decision's words "accept as answered". Until then this plan is its live home.
* **The wider in-place class.** The module-merge conflict side-file in `slotmerge.py`, the base-cache writes in `write_install_lockfile` and `_apply_upgrade`, `_apply_upgrade`'s swap writes, `_write_stage`, `_install_one` with `--force`, and the profile writes: not folded in, because the Maintainer's answers named only the install-record committer, the `.gitignore` points, and the four lockfile writers and the reader. `defer` at archive, in one batch with Q4. It needs his word quoted verbatim, so this plan does not deposit it. The committer, the four lockfile writers, the reader and the `.gitignore` append are accepted scope (C4), not deferrals.
* **The solo-greenfield seed.** `wontfix`, with the Maintainer's allowance quoted in *Scope delta*.
* **Whether the combined AST ceremony needs its own marked board row.** The queued row's marker names only the gate-manifest re-anchor. The Maintainer's call; if yes, the archive commit adds the row.
* **An `fsync` before each rename.** Offered by the Security review as optional. Declined: an in-place write has the same crash window today, so it is no worse. Not deferred, because nothing is owed.
* **The archive commit writes this plan's `CHANGELOG.md` entry,** and adds to the queued re-anchor row the node note and a statement that the AST correction runs first, then the gate-manifest re-anchor once, with the AST delta as part of the one combined ceremony.

## Plan review -- Claude Sonnet 5.5 (Internal) -- 2026-10-18

```
Reviewed commit: 20f145eda92c575473a2ccfcf021946086a0186c
Target: the whole plan as committed (In brief, Source proposal, Scope with its four after-opening answers, Sequence, Acceptance criteria C1-C6, the security findings ledger, Scope delta, Verification with the mutation ledger, Named residuals, Dispositions), read against the accepted proposal (the Decision and scribe's note, Revision 2, Revision 1, the Security Review SEC-1 to SEC-8, the closure pass CL-1 to CL-4), the Maintainer's three additions the Scope quotes, and the engine, checker, stub, fixtures and board code at that commit
Prior findings: none
Assurance path: high-assurance (inherited, as the plan declares)
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised -- 12 (2 high, 5 medium, 5 low). **Verdict**: REVISE.

This is the Internal pass of `required(Internal + Internal Security Review)`. The Internal Security Review is a separate pass by another session and is not done here. I make no claim to External distance: everything below strengthens the plan inside its own frame.

**In plain terms.** The plan delivers what the Maintainer accepted, and I found nothing dropped or narrowed without his word. Its numbers check out against the code at `20f145ed`: the exit-code table, the seven frozen files, the AST picture, the lockfile count. The twelve findings are repairs to the plan's text. Two are accepted tests that, as written, cannot be built or cannot see what they claim to see. Three come from the `.gitignore` repair that is being answered right now, which moves the starting bytes the plan counts on. The rest are gaps in what a criterion pins, or claims that say a little more than the plan does.

**How I checked** (all in a detached worktree of `20f145ed` under a scratch folder, removed afterwards, with `/Users/kendal30/conda_envs/lhm/bin/python3.13` and PyYAML 6.0.3; the shared tree was only read):

* **Exit-code table.** I read every row against `bootstrap/_scaffold/cli.py` and `bootstrap/_scaffold/upgrade.py`, and ran two: an install over a linked `.gitignore` (exit 2, the `.gitignore` refusal line) and over a linked `dev/.cairn` (traceback, exit 1). `main` has three `ScaffoldSecurityError` catches (the `.gitignore` preflight, the skills fan-out, the onboarding install), as the plan says. The table is right at this commit.
* **Frozen files.** `bootstrap/tests/fixtures/gate_manifest.json` holds 183 frozen keys. The control, `bootstrap/tests/test_scaffold.py`, is found frozen. The intersection with the files the plan edits is seven: the six the plan lists plus `bootstrap/tests/fixtures/scaffold_ast_known_new.json`. `test_intents_tool.py` is phase-mutable. The manifest pins 25 nodes in `test_model_selection_stub.py` (one leaves, one changes its fixture, 23 stay) and 37 in `test_upgrade_module_additions.py`. All as the plan says.
* **AST.** `bootstrap/tests/_ast_attest.py verify` at `20f145ed` reports exactly four CHANGED (`main`, `seed_gitignore`, `_cmd_adopt_module`, `cmd_upgrade`). Changing one statement of `_commit_lock_and_caches` in a scratch copy gives "known-new digest/multiplicity mismatch" for it, and `test_ast_attest.py` stays at the same two failing nodes (2 failed, 28 passed), as the plan says. **With the repair's pending answer** (its working-tree `install.py` copied into a scratch copy) the same verify reports **five** CHANGED: it adds `create_dev_tree` (MM-PR-3).
* **Lockfile.** `bootstrap/verify_integrity.py` reports 18 violations at `20f145ed`, none a file the plan edits. As the plan says.
* **Notice constants.** The first text is byte-identical to Revision 2's R2.3; the second differs only by the CL-3 sentence ("That file was not changed"). The seed, in a scratch install with Revision 2's seed text added to `collaborative-team`, renders and `python tools/board.py --maintainer` lists it as `declared`, at line 100 of the installed planning file. As the plan says.
* **The defect behind the install-record fold-in is real.** A hard link at the lockfile's temporary name, pointing at an outside file, ends up holding the lockfile text after `_commit_lock_and_caches` at `20f145ed`.
* **Corpus.** I built the generated corpus (6 leads x 6 breaks x 3 positions) and the CL-4 spellings and ran them through the anchored pattern, a widened pattern and PyYAML (MM-PR-1).

**Findings at a glance**

| ID | Severity | One line |
|---|---|---|
| MM-PR-1 | High | The 108-file corpus is 6x6x3 and cannot hold the two CL-4 spellings the plan says it holds; the engine never sees them |
| MM-PR-2 | High | The accepted real-install test for the capture's refusal cannot be built once the repair's `create_dev_tree` guard lands |
| MM-PR-3 | Medium | The plan pins AST counts (five, "the repair's four") that the repair's answer moves to six / five |
| MM-PR-4 | Medium | The repair's answer already rewrites the `SECURITY_MUTATIONS.md` paragraph the plan says C4 writes |
| MM-PR-5 | Medium | C2 says its shipped words are "quoted below"; they are not, and no criterion pins them |
| MM-PR-6 | Medium | The install record has four more in-place writers; the plan's closure wording can be read as covering them |
| MM-PR-7 | Medium | P15 drops the repair's fail-early for a folder or pipe named `.gitignore`, which nobody asked for |
| MM-PR-8 | Low | The `RecursionError` catch is beyond the Decision and is filed as "at the Maintainer's instruction" |
| MM-PR-9 | Low | The two Maintainer ceremonies touch one frozen file; the plan does not say which goes first |
| MM-PR-10 | Low | Two accepted details have no criterion that can fail (the capture's docstring; the per-site phrase search) |
| MM-PR-11 | Low | The two new refusals (the capture's line, the hard-link `.gitignore`) name no remedy |
| MM-PR-12 | Low | The new `os.open` flags are POSIX-only as written (`O_BINARY`, `fchmod`) |

**MM-PR-1 -- High -- the 108-file corpus cannot hold the two CL-4 spellings the plan says it holds**

* *Evidence.* Plan line 290 says "The corpus holds both CL-4 spellings". Line 294 defines the corpus as leads (6) x breaks (6) x positions (3) = 108, and lines 34 and 340 count 108. Line 515 says mutant M7 is killed by "the two CL-4 spellings in the corpus". These cannot all hold: 6 x 6 x 3 has no axis for how a row is spelled. The closure pass (`dev/proposals/archive/2026-10-18-claude-model-mapping-install-path.md:1617-1631`) required "add both spellings to the corpus", because otherwise "never looser" "passes only because the corpus leaves them out".
* *Measured.* The anchored pattern misses `- "tier": high`, `- 'tier': high` and `mapping: [{tier: high, model: x}]` (bare exit 1) while PyYAML reads all three as rows (exit 0); a widened pattern accepts all three. So the substance of P3 is right and the three differences it leaves (a one-line list whose first key is not `tier`, a row without a `tier` key, a `tier:` inside another value) are real, in the direction the plan says.
* *Why it matters.* (a) C3's engine-against-checker parity (line 340) runs on the 108 only, so the engine's copy of the row rule is never compared on these spellings. That is the harm CL-4 named: "the notice wrongly calls the mapping unfilled". (b) The "two explicit lists" (line 294) have no named members, so "a difference outside both lists fails" cannot be written as a test. (c) M7 names no copy; the checker and the engine each carry the rule. (d) Line 294 replaces Revision 2's "the PyYAML checker is never looser than the bare one" with two lists. CL-4's second option allows that, but only when "the reverse direction" is asserted for named members.
* *Recommended fix.* In C1, define the corpus as two parts and state the total: the 108 generated files, plus a named spelling table with one row per member giving its text, the expected pass or fail of the bare checker, the PyYAML checker and the engine, and its list (stricter with PyYAML: the eight value spellings of line 291; looser with PyYAML: the three above; agreed after widening: the double-quoted key, the single-quoted key, the one-line list starting with `tier`). Say in C3 that the engine criterion runs over the whole set and that `_mapping_is_unfilled` carries the same widened row rule (only C1 says it now). Split M7 into M7a (checker) and M7b (engine). Define the PyYAML row rule in C1 (my reading of Revision 1: `mapping` is a non-empty list; say what a missing `mapping`, a non-list and a list of non-mappings give). Correct "108" in the In brief.

**MM-PR-2 -- High -- the accepted real-install test for the capture's refusal cannot be built once the repair's answer lands**

* *Evidence.* Plan line 355 (and Revision 2's R2.6, which it follows) requires a real interactive install over a tree whose `dev/.cairn` links to a folder that already holds `local-env.json`, the activation log and a stub, "otherwise the install stops earlier, in `write_local_env`". The exit table (line 126) and line 143 say a linked `dev/.cairn` stops in `write_local_env`.
* *Measured.* At `20f145ed` that fixture does reach the capture (it then stops at the lockfile write, where the real design would have exited 2 at the capture). The repair's pending answer (uncommitted working tree, claimed under `gs-cr-answer`) makes `create_dev_tree` guard every `_DEV_DIRS` entry before its first `mkdir` (`bootstrap/_scaffold/install.py:199-200`), and `dev/.cairn` is one of them. In a scratch copy with that file, the same install stops in `main` -> `create_dev_tree` -> `_assert_safe_write` (traceback, exit 1), before `write_local_env` and before the capture. The accepted test then has no way to reach the code it is meant to prove.
* *A fixture that works both ways (measured).* Make the mapping file itself the link, pointing at an outside regular file holding `FILL ME`, with a real `dev/.cairn`. `_install_one` skips an existing destination, nothing earlier refuses, and an interactive install reaches the capture (three prompts asked, with a harness that fakes a terminal) with and without the pending answer.
* *Recommended fix.* In C4 use the linked mapping file for the real-install test and keep the linked `dev/.cairn` for the direct-call test only (`TestCaptureRefusesBeforeAskingAnything`). Keep the assertion on the constant line, which makes a test that stops earlier fail loudly. Reword lines 126, 143 and 355 so they do not name `write_local_env`: "the first write that guards it; a traceback and exit 1 either way". Note in the plan that the accepted fixture was replaced and why, since it is a change to an accepted test (the outcome, a real install proving the capture itself refused, is unchanged).

**MM-PR-3 -- Medium -- the plan pins AST counts the repair's answer moves**

* *Evidence.* The plan states the picture as "the repair's four" and "5 CHANGED, 1 re-keyed, 2 NEW" at lines 28, 93, 169, 171, 234 and 266, and builds criteria on it: "no CHANGED symbol beyond the five" (371), "the five CHANGED stay five" (382), "the same four symbols the repair changed" (401). Line 169 hedges that "no criterion here pins a byte or a line", which is true of bytes and lines but not of counts.
* *Measured.* With the pending answer, `verify` reports five CHANGED at the base: the four plus `create_dev_tree` (digests `0e8c4e4f41b5bcb8` baseline against `9de03f6ae0c0c469`). The working-tree `dev/PLANNING.md` already says "six CHANGED, one re-keyed and two NEW". A correct implementation of this plan would fail lines 371, 382 and 401 as written, and the plan and the board would disagree.
* *Recommended fix.* State each criterion as a set difference, not a count: "the CHANGED set at the tested commit equals the CHANGED set at C4's parent plus `capture_model_selection_mapping`; the known-new mismatch set is exactly `{_commit_lock_and_caches}`; the NEW set is exactly the two named". Say in lines 169-171 that the count is derived at ceremony time and is six if the repair's answer has landed. Do the same for line 234's "must derive four changed symbols" (the other plan will meet five or six).

**MM-PR-4 -- Medium -- the repair's answer already rewrites the `SECURITY_MUTATIONS.md` paragraph the plan says C4 writes**

* *Evidence.* Line 141 says the "caught once at the CLI top level (exit 2)" sentence "is false again, so the correction Revision 2 asked for is owed after all ... C4 writes it", and line 364 makes it a criterion. Line 381 says "if the repair's own answer has reworded [the `seed_gitignore`] row by then, this plan edits the row as it stands", but says nothing of the paragraph.
* *Measured.* The pending working-tree `bootstrap/_scaffold/SECURITY_MUTATIONS.md` replaces that paragraph with the true story (a command turns the error into a plain exit 2 only where it asks first or wraps its own writes; everywhere else a traceback and exit 1, which the oracle pins), listing the three `.gitignore` preflights, the fan-out, onboarding, `--apply`, `--stage` and `--adopt-collisions`. It does not mention the capture. The same answer adds `create_dev_tree` to `_GUARDED_WRITE_FUNCS` in `bootstrap/tests/test_security_leaf.py`, the set C4 also edits. It also adds a second, remedy line to the three `.gitignore` refusals, so the table's "what prints" column (line 123) gains a line while the exit stays 2.
* *Recommended fix.* Rewrite lines 141 and 364: "the opening paragraph, as the repair's answer left it, gains the capture's own catch (a constant line, exit 2) and nothing else; `_GUARDED_WRITE_FUNCS` gains the two names beside whatever the repair added". Add the remedy line to the table's first row. Add to C4's gate: re-read all three of these at the parent.

**MM-PR-5 -- Medium -- C2's shipped words are "quoted below" but are not, and no criterion pins them**

* *Evidence.* Line 303 says the module pair gains its paragraph and corrected sentence "quoted below". Nothing is quoted below. A search of the plan for the stub's example block, the module paragraph, the replaced sentence, the II-5 block, the fourth allowed match and the seed's body finds none of them; only the two notices (C3) and the seed's Waiting line (line 245) are in the plan. The words live only in Revision 2's R2.5, in an archived proposal.
* *Why it matters.* The criteria pin keywords ("family", "never a version", the Waiting line's presence), so a paragraph that drops "It checks shape, not truth, and nothing reads `date_verified`" or the corrected "no routine reads it" would pass every C2 test. Those two sentences are the accepted correction of a false statement.
* *Recommended fix.* Say in C2 that the shipped text is Revision 2's R2.5 verbatim, and either quote the seven blocks in the plan or point at the exact heading. Pin the three load-bearing items by exact string: the Waiting line (`**Waiting on Maintainer**: fill the model mapping`), the module paragraph's "nothing reads `date_verified`" sentence, and the corrected "no routine reads it" sentence. Delete "quoted below" if nothing is quoted.

**MM-PR-6 -- Medium -- the install record has four more in-place writers, and the closure wording can be read as covering them**

* *Evidence.* The fold-in is scoped correctly to `_commit_lock_and_caches`. But the same lockfile, `dev/.cairn/cairn-lock.yml`, is also written in place by `write_install_lockfile` (`bootstrap/_scaffold/install.py:1863`), `_cmd_init_lock` (`bootstrap/_scaffold/upgrade.py:1278`), `_cmd_finalize_lockfile` (`bootstrap/_scaffold/upgrade.py:1904`) and `_apply_upgrade` (`bootstrap/_scaffold/upgrade.py:2221`). Each calls `write_text` after `_assert_safe_write`, which looks at symbolic links and not link counts, so a hard link at the lockfile's own name is written through by all four. Lines 187 and 576 name only "the module-merge conflict side-file" as the case seen, and line 564 (S5) says the hard-link case "is closed by construction ... for the install-record writer". A reader, the Maintainer included, can take "install record" to mean the lockfile.
* *Recommended fix.* Do not widen scope. Rename "the install-record writer" to `_commit_lock_and_caches` in S5 and the residuals. Name the four lockfile writers in Named residuals beside the side-file. Add them to the one deferral batch the plan already means to put at archive (it needs the Maintainer's quoted word, as the plan says of the side-file).

**MM-PR-7 -- Medium -- P15 drops the repair's fail-early for a folder or pipe named `.gitignore`, which nobody asked for**

* *Evidence.* P15 (line 210), line 378 and the residual at line 577 accept that a folder or pipe named `.gitignore` is "no longer caught by the preflight" and is refused only at the first seeding that writes, "after any earlier writes". P15 says "the Maintainer called the preflight's read a regression" (line 113 calls it "a regression the repair introduced"); no quote supports the first. His quoted words (lines 103-107) answer a question about "a non-UTF-8 `.gitignore` stopping an upgrade". The Security Review (`dev/plans/archive/2026-10-18-security-review-gitignore-seed-guard.md:402-418`) rates GS-SR-5 informational and says "Fail-earlier is the safer behaviour".
* *Effect.* Git can carry `.gitignore/x`, so a folder named `.gitignore` is possible. After this change an install over one creates the dev tree and installed files and then dies at the first seed with a traceback and exit 1, the half-install the repair removed, and `--stage` leaves a stage behind.
* *Recommended fix.* P14 already runs an `lstat` in the preflight for the link count. Add "not a regular file" to that `lstat` (folder, pipe, socket, device): refuse with `ScaffoldSecurityError`, open nothing, decode nothing. Keep the first-write refusal as a backstop. Only the non-UTF-8 case then changes behaviour, which is what was asked. Remove the "Maintainer called it" clause or quote him, and update line 577. Cost: one condition and one test row.

**MM-PR-8 -- Low -- the `RecursionError` catch is beyond the Decision and is filed as "at the Maintainer's instruction"**

* *Evidence.* P8 (line 204) says it "adds two lines beyond the accepted text". Line 457 lists the `RecursionError` catch among "Additions ... each at the Maintainer's instruction, quoted under Scope", but the four answers quoted under Scope (lines 77-115) say nothing about it. Revision 2's R2.4 requires the scan to visit "each object once"; it does not mention `safe_load`'s own recursion limit. The plan leaves the other defects it found while planning (lines 183-190) unfixed and sends them to Dispositions.
* *Recommended fix.* Uphold the explicit-stack walk (that is R2.4's "once each" and adds no recursion of its own). For the catch, either cut it to the Dispositions with the other found-but-not-fixed items (my lean: no accepted outcome depends on it, and the failure is a traceback on a file the adopter wrote), or keep it and say in the Scope delta that it is the plan's own addition. Do not write "at the Maintainer's instruction". If cut, drop the 5000-deep bullet at line 293.

**MM-PR-9 -- Low -- the two Maintainer ceremonies touch one frozen file; the plan does not say which goes first**

* *Evidence.* The plan correctly counts seven frozen files, six edited by an agent and `scaffold_ast_known_new.json` written by the AST ceremony (lines 149-152); line 149 says "seven" and then "The six", and lines 28 and 266 say "the six frozen files". `scaffold_ast_known_new.json` is in the manifest's frozen keys (control above). If the gate-manifest re-anchor runs first, the AST ceremony then modifies a frozen file and leaves a fresh hold, a second re-anchor for the Maintainer. Neither `bootstrap/AST_BASELINE_RUNBOOK.md` nor `bootstrap/REANCHOR_RUNBOOK.md` mentions the other. I did not read the re-anchor runbook end to end, so the author should confirm the effect.
* *Recommended fix.* Say in chunk M, and in the note the archive commit adds to the queued row, "run the AST ceremony first, then the gate-manifest re-anchor once, so it records the seventh file's final bytes". Make "seven" and "six" read consistently.

**MM-PR-10 -- Low -- two accepted details have no criterion that can fail**

* (a) Revision 1 section 4 asks that the capture's docstring say it runs at install time and name `--adopt-module` and `upgrade` as notice-only. The current docstring (`bootstrap/_scaffold/install.py:694-695`) says "install / ``--adopt-module`` time", which is the false statement. The plan's order list says only "the docstring". Add a criterion: the docstring no longer says the capture runs at `--adopt-module`, and says the two commands only print the notice.
* (b) Line 309 says the "family, never a version" sites are "listed from the tree by searching for the phrase". The capture's prompt reads "model family, not a version" (line 363), so a search for "never a version" will not list it, and the header line has no stated wording. Name the eight sites explicitly, as M20 does, and say what the header says.

**MM-PR-11 -- Low -- the two new refusals name no remedy**

* *Evidence.* The capture's refusal is a constant line with no hint (P6, line 201). A person whose mapping is a link by design, such as a shared file in a monorepo, meets exit 2 on every interactive install. The new hard-link `.gitignore` refusal reaches the preflight catch sites; the repair's pending answer adds a remedy line there ("replace the link with a regular file, then re-run"), following the code review's GS-CR6. P14 says nothing about the hard-link case.
* *Recommended fix.* A fixed sentence is as constant as the prefix and names only the fixed path. Extend the capture's line with a remedy (author's wording; for example "... is a link or sits behind one; replace it with a regular file, or install with --non-interactive and fill it by hand"), and test that it contains the remedy and no tree text. Check that the preflight remedy's words fit a hard link, and add a test row for that wording.

**MM-PR-12 -- Low -- the new `os.open` flags are POSIX-only as written**

* *Evidence.* P13 (line 208) opens with `O_WRONLY | O_CREAT | O_EXCL`, and P14 (line 209) adds `O_NOFOLLOW` and `O_NONBLOCK` "where the platform has them", then copies mode bits. On Windows a descriptor opened without `O_BINARY` translates `\n` to `\r\n` on write, so a base-cache copy written through it would no longer match the template bytes whose hash the lockfile records; `tempfile.mkstemp`, which the capture uses, adds `O_BINARY` itself for this reason. `os.fchmod` does not exist there. The engine already has Windows fallbacks (the symbolic-link probe in `bootstrap/_scaffold/install.py`), although `bootstrap/SAFETY.md:525` records no Windows run.
* *Recommended fix.* Say in P13 and P14: build the flags with `getattr(os, "O_BINARY", 0)`, `getattr(os, "O_NOFOLLOW", 0)` and `getattr(os, "O_NONBLOCK", 0)`; copy the mode with `os.chmod(path, mode)`; the mode tests skip where the platform has no POSIX modes.

**Answer 1 -- does this plan deliver what the Decision and the three additions accepted, all of it?**

Yes in outcome, with the repairs above. I walked Revision 1's seven numbered changes, Revision 2's R2.1 to R2.7, SEC-1 to SEC-8 and CL-1 to CL-4 against the chunks and found each mapped (the plan's Scope-delta table is accurate). The only removal is the `solo-greenfield` seed, declared with the Maintainer's quoted allowance. Nothing is dropped. What is narrowed or reworded, each with an authority: the second notice's sentence (CL-3), "never looser" replaced by named lists (CL-4's second option, which the plan does not yet deliver fully: MM-PR-1), `--init-lock`, `--finalize` and `--adopt-collisions` staying silent (Revision 1 named `--plan`, `--stage` and `--apply`, and its call site sat after those branches). Two accepted items need repair to be delivered as accepted: the real-install test (MM-PR-2) and the words of C2 (MM-PR-5). Beyond the Decision and the additions there is one item, the `RecursionError` catch (MM-PR-8). The Maintainer's additions land: the install-record fix is designed correctly and reproduced as a real defect (see MM-PR-6 for how far "closed" reaches); GS-SR-3, GS-SR-4 and GS-SR-5 are delivered (with MM-PR-7 on one side effect); one combined AST ceremony is stated (MM-PR-3, MM-PR-9); the build order is respected. His four answers land as checkable criteria: the check skips full-line comments and fails an empty mapping (C1), the seed goes in two presets and not in `solo-greenfield` (C2, M19), the Waiting row is listed by `board.py --maintainer` on a fresh install (C2), and the stub example says family and never a version, with a per-site test (C2 to C4, M20). The sequencing against the four earlier plans is right as far as the shared files go: no file is claimed by a plan that the table does not list, and `neutrality-and-upgrade-slots` leaves `bootstrap/_scaffold/` alone as the table says. Two cells have gone stale since the plan was written and are harmless: `neutrality-and-upgrade-slots` is past its C7, and `board-as-basis` is now `revising-plan` after two reviews, whose coupling to this plan is only the `--maintainer` output and the row grammar the plan already pins loosely.

**Decisions P1 to P15**

* P1 uphold. P2 uphold. P3 uphold (see MM-PR-1 for the corpus). P4 uphold; judging the structure before the rows is also what keeps two pinned nodes green (`test_malformed_message_is_clean`, `test_non_mapping_top_level_fails_3`), so say so in C1.
* P5 uphold. P6 uphold, with a fixed remedy clause (MM-PR-11). P7 uphold.
* P8 uphold the walk, overrule the catch (MM-PR-8). P9 uphold. P10 uphold. P11 uphold. P12 uphold.
* P13 uphold, with the platform flags (MM-PR-12). P14 uphold refusing rather than replacing a hard-linked `.gitignore`: replacing would first copy the outside file's content into a file Git commits, and would silently cut a link someone made on purpose; add "not a regular file" to its `lstat` (MM-PR-7) and a remedy (MM-PR-11).
* P15 uphold for the decoding half (a non-UTF-8 `.gitignore` no longer stops an apply, bytes kept exactly); overrule dropping the fail-early for a folder or pipe (MM-PR-7).

**Answer 2 -- is there a simpler path to the same outcome?**

No simpler path to the accepted outcomes. The notice, the check and the guarded capture each need the code the plan names, and the plan's own cuts (the seed in two presets, no new top-level symbol beyond the two the notice needs) are already the lighter choices. There is one place where the plan is heavier than it needs to be, offered as a choice and not a finding: three hand-written "exclusive temporary file, write, guard, rename, clean up" sequences (the capture through `mkstemp`; the install-record writer and the `.gitignore` append through `os.open`), each with its own mutants (M14, M15, M24 to M28, M32, M35, M36). A single private helper in `install.py`, which `upgrade.py` already imports from, would create and write the exclusive temporary once; MM-PR-12's flags and the cleanup would then exist in one place. The cost is one more NEW symbol for the AST ceremony and, for the capture, a departure from Revision 2's "all inline" (the Response to SEC-3 chose inline to keep the AST count down). So the capture could stay inline as accepted, with the helper used by the two additions the Maintainer folded in, which carry no such requirement. I would not hold the plan for it. Nothing else here can be cut without dropping an accepted outcome, apart from the `RecursionError` catch (MM-PR-8).

**What I did not cover**

* I did not run the full suite, any mutant of the ledger, or the plan's 202-test measurement. This is a plan review; the ledger and Boundary B belong to C6.
* The Internal Security Review is a separate pass. I spot-checked the SEC-3 to SEC-8 and CL-1 to CL-4 mapping for delivery, not for adequacy as security controls.
* I re-ran CL-4's spellings and a prototype of the 108-file corpus, but not the plan's 21-spelling prototype, and I could not check the generator the plan has not yet written. PyYAML 6.0.3 only.
* I measured the seed in `collaborative-team` only, not `high-rigor-legacy` or the `complexity: simple` strip.
* I read `board-as-basis` only where it names this plan, not its two reviews in full; a change to the row grammar after its fold could still touch the seed test.
* The effect of MM-PR-9 (ceremony order) rests on the manifest's frozen list and the board's description, not on a full read of the re-anchor runbook.
* Windows and other non-macOS platforms; I ran nothing there.
* I did not check `CHANGELOG.md`, the Dispositions wording at archive, or the neutrality gate against the widened checker `neutrality-and-upgrade-slots` will land first.

## Plan review -- Claude Opus 5.5 (Internal Security Review) -- 2026-10-18

```
Reviewed commit: 20f145eda92c575473a2ccfcf021946086a0186c
Target: the whole plan, read for its security treatment: Scope (and the answers folded after opening), What the exit codes are now, Frozen files, AST and the oracle, P1-P15, the C1-C6 and M criteria, The security findings ledger, Verification (mutation ledger, Boundary C, security preflight), Named residuals
Prior findings: carried in, checked for coverage, not closed here -- SEC-3 to SEC-8 and CL-1 to CL-4 (dev/proposals/archive/2026-10-18-claude-model-mapping-install-path.md); GS-SR-3 to GS-SR-5 (dev/plans/archive/2026-10-18-security-review-gitignore-seed-guard.md)
Assurance path: high-assurance -- inherited (the scaffold engine)
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised

**Model**: claude-opus-5-5

A fresh session, asked by the coordinating session to fill this plan's `+ Internal Security Review` obligation and nothing else. A separate fresh session wrote the ordinary Internal pass at the same time (committed as `d13bd2ac` while I worked); I wrote these findings without reading it. Its closing list, which I saw when appending, also raises the ceremony order (its MM-PR-9). MM-SR-3 carries the same fact because it bears on whether the ceremony is safe. I read the plan at the commit above, the accepted proposal's Security Review and closure pass, the `.gitignore` repair's Security Review, `bootstrap/SAFETY.md`, `bootstrap/_scaffold/SECURITY_MUTATIONS.md`, `bootstrap/AST_BASELINE_RUNBOOK.md` and the engine at that commit. Every probe ran in a detached worktree of `20f145ed` in a fresh scratch folder, under `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13, PyYAML 6.0.3), on macOS. The plan's code does not exist yet, so where I tested one of its designs I wrote a stand-in from the plan's words, and I say so each time.

### In plain words

**Verdict: REVISE.** The plan is the right shape. Every finding it inherited becomes a criterion or a named disposition, and its main mechanism held up when I attacked it: write a fresh temporary file, then swap it in by renaming. In 6,000 racing calls against a stand-in of the new `.gitignore` code, nothing outside the project was written and no outside bytes were copied in. Three things should change before code is written:

1. **Copying the old file's permissions can give another user your account (MM-SR-1, blocks).** The plan copies the old `.gitignore`'s "mode bits" onto the new file. On a shared machine, another user who can write the project folder can leave a `.gitignore` that is a program carrying the mark "run as this file's owner" (the setuid bit). Today Cairn appends to that file, and it stays theirs. Under the plan, Cairn writes a new file that belongs to *you*, keeps their program's bytes, and copies the mark. On Linux they can then run it as you. The fix is one mask: copy only the read and write permissions.
2. **A 900-byte mapping file can freeze the check (MM-SR-2).** A YAML shortcut called a merge key lets each line double the work. The plan says depth and aliasing cannot blow the check up; this does, inside the YAML reader, before the plan's protection runs. The fix is to refuse merge keys, which no mapping needs.
3. **The Maintainer's AST ceremony has no safe tool named (MM-SR-3).** No existing command can make this correction. The last time one was made, the Maintainer ran a script an agent kept outside the repository. This plan hands the Maintainer agent-computed fingerprints "for the Maintainer's use", and does not say the ceremony runs before the gate-manifest re-anchor. The plan should say how the ceremony works out its own figures, stops on a surprise, and dry-runs.

The other seven are small; each can be folded or answered.

| ID | Severity | Blocks `ready-to-implement`? | In short |
|---|---|---|---|
| MM-SR-1 | high, on shared machines | **yes** | copied mode bits carry setuid onto a file the installer now owns; set by path, they follow a swapped link |
| MM-SR-2 | medium | fold in this revision | a merge-key chain hangs the checker; P8's claim is false |
| MM-SR-3 | medium | fold in this revision (plan text only) | Chunk M: no instrument, agent-computed digests, a hard-coded set, no order with the gate-manifest re-anchor |
| MM-SR-4 | low | no | the hard-link `.gitignore` refusal's text is unspecified, and the hint in flight is wrong for it |
| MM-SR-5 | low | no | one descriptor-based reader for all three files, with the repository's own flag set; `O_BINARY` on the writes |
| MM-SR-6 | low | no | the line rule finds rows that are not rows; one member of that class is listed |
| MM-SR-7 | low | no | the checker's new lines must never print a parsed value |
| MM-SR-8 | low | no | the real-install refusal fixture stops earlier once the repair's `dev/` guard lands |
| MM-SR-9 | low | no | replacing `.gitignore` overrides a read-only file and changes its owner |
| MM-SR-10 | low | no | three stale ledger and residual sentences; GS-SR-3's `SAFETY.md` note has no disposition |

### Answers to the five questions

**1. Coverage.** Every inherited item is a checkable criterion or a named disposition, checked against the source text rather than the plan's summary of it:

* SEC-3: the capture's order, both guards and the replace (C4), and S5;
* CL-1: `mkstemp`, the planted-names test, M15;
* SEC-4 and CL-2: the re-derived exit-code table, the constant line, the direct-call and real-install tests, the stated asymmetry;
* SEC-5 and CL-4: every value type scanned, the widened row pattern, both CL-4 spellings in the corpus, the class named;
* SEC-6 and CL-3: `lstat` first, the missing file silent and first, the wording;
* SEC-7: the generated corpus, M8, the version gap;
* SEC-8: the `lockfile.py` comment, `_write_stage` pinned;
* GS-SR-3: the `O_NOFOLLOW` read, the rename write, three stand-ins, the race probe repeated;
* GS-SR-4: refused, through four entry points;
* GS-SR-5: no read in the preflight, bytes kept.

Nothing is lost in substance. Three sentences are stale, and GS-SR-3's second recommendation, that `SAFETY.md` say what a won race does, has no disposition (MM-SR-10).

**2. The three exclusive-temp writers.** The mechanism is sound; the mode bits are not.

* **Today's defects are real at `20f145ed`.** A hard link at `cairn-lock.yml.tmp` left the outside file holding the lockfile text, and afterwards the project's lockfile *was* that outside file (link count 2). A hard-linked `.gitignore` got `new-entry` appended to the outside file. A non-UTF-8 `.gitignore` stopped the no-entry preflight with `UnicodeDecodeError`.
* **The design holds under the race.** A stand-in of P14/P15, written from the plan's words, faced the Security Review's racing thread: 3,000 calls with `.gitignore` flipping between a file and a symbolic link, and 3,000 with it flipping to a hard link. The outside file was unchanged both times, and 0 writes carried outside bytes.
* **Planted names cannot redirect, block or clobber.** `O_CREAT | O_EXCL` refused all six planted kinds at the temporary's name (hard link, symbolic link, dangling link, named pipe, folder, socket), each with errno 17. Python's `mkstemp` already uses `O_EXCL | O_NOFOLLOW` and retries on a collision. The reader `O_RDONLY | O_NOFOLLOW | O_NONBLOCK` opened a pipe and a folder at once (then `fstat` refuses them), refused a link and a dangling link with errno 62, and refused a socket with errno 102.
* **Refuse rather than replace a hard-linked `.gitignore` (P14): agreed.** The line is whether old content is copied. The `.gitignore` append keeps the old bytes, so replacing would copy an outside file into a file Git commits. The capture and the install record write wholly new content, so replacing is safe there. The plan's split follows that line.
* **The mode bits: not sound as written** (MM-SR-1).
* **Cleanup on failure** is sound if it removes only names this call created. A name that failed `O_EXCL` is not ours. Removing it would be harmless, because unlinking a name never follows it, but the criterion should say "only what this call created".
* **fsync.** None of the three writers flushes before the rename. That is no worse than today, since an in-place write has the same crash window, so it is not a finding. One `os.fsync(fd)` before closing each temporary would make a crash leave the old file rather than an empty one. Optional.
* **Rename semantics.** A replace inside one folder is atomic on POSIX. A link swapped onto a *parent* folder between the guard and the rename cannot carry the rename into someone else's folder. The rename needs the temporary file to be in that folder, and only someone who can already write there could put it there. So S5's "narrows the window to one rename" is conservative. What a parent swap can still do is make `mkstemp` create a new temporary in a folder the swapper picks, holding mapping or lockfile text (neither secret); the guard on the temporary then refuses, and a leftover may remain. Stated, not raised.
* **A link swapped in between read and write.** For `.gitignore`, nothing leaks (above). For the capture, a swap between the early guard and the read can make it read an outside file. Nothing from that file is printed or written; the only signal is whether the prompts appear. The install record reads only the existing lockfile, through a reader outside this plan (*What I did not cover*).
* **The simplest design** would be one shared "write by replacing" helper, as GS-SR-3 suggested, rather than three inline variants. The plan's choice, which adds no symbol, is acceptable because each variant has its own red-then-green tests and mutants. Either is safe once MM-SR-1 and MM-SR-5 are folded.

**3. The notice and the checker on an untrusted mapping.**

* **Terminal injection.** The notice prints two constants and nothing from the tree, and C3 pins that with a control-sequence fixture. Today's checker is clean too: four crafted files produced no ESC or BEL byte on either stream. They held a `\e]0;...\a` escape near a parse error, a tag spelled with `%1B`, a raw ESC, and a bidi override. PyYAML refuses raw control characters and prints tags with `repr`. Only the bidi override (U+202E) passed through, inside the error snippet, which is cosmetic. But a *parsed value* can hold ESC and BEL, through YAML's `\e` and `\a` escapes, so the new messages must never print one (MM-SR-7).
* **Deep nesting.** Confirmed: `safe_load` raises `RecursionError` at 600 nested flow sequences or flow mappings, and at 100,000, in under a second; 400 loads. P8's catch is right.
* **YAML bombs.** Not closed: merge keys blow up `safe_load` itself (MM-SR-2).
* **Parity.** The line rule is looser than the YAML rule on purpose, for the named value class. It is also looser in a row class of which the plan lists one member (MM-SR-6). The corpus cannot show either, because it generates neither; only the explicit lists can hold them.

**4. Exit codes and the oracle.** The pins stay honest. I read `bootstrap/tests/_oracle.py`:

* the fresh-install scenario compares trees and ignores standard output;
* the privileged scenarios install `solo-greenfield`, which never selects the module;
* the containment scenario plants a linked `AGENTS.md` and stops in `_install_one`, a path this plan does not touch;
* the new `.gitignore` bytes equal today's for a UTF-8 file (the stand-in writes the old bytes plus the same block);
* the capture's new catch runs only on an interactive install, which the oracle never runs.

**New refusal lines.** The capture's is constant (P6). The hard-link `.gitignore` refusal goes through the existing preflight catches, which print a prefix and the exception text. The plan does not say what that text is, and the hint the repair's answer is adding ("replace the link with a regular file") is wrong for a hard link, which *is* a regular file (MM-SR-4). The other new refusals, from the descriptor checks while seeding, end in a traceback with exit 1, or behind the `--apply` and `--stage` catches with exit 2. Python prints the path there with `repr`, so no control byte reaches the terminal.

**5. The AST and frozen-file ceremony.** The arithmetic is right, measured. I took a scratch copy of `20f145ed`, changed one line in the capture and one in `_commit_lock_and_caches`, and added the two functions. The verifier reported `CHANGED 5`, the known-new digest mismatch for `_commit_lock_and_caches`, and both new functions as not pinned. The real-tree check fails in the same two `test_ast_attest.py` nodes as today, because both pass the known-new manifest. But the plan does not leave the Maintainer a ceremony that is safe to perform (MM-SR-3).

### Findings

#### MM-SR-1 -- high on shared machines, blocks: copying the old file's mode bits carries setuid onto a file the installer now owns, and copying them by path follows a swapped link

**Plain:** a file's "mode" holds more than who may read and write it. It can also carry a mark that says "when this file is run, run it as its owner" (setuid). Today Cairn appends to the existing `.gitignore`, so the file keeps its owner. The plan swaps in a new file, which belongs to whoever ran Cairn, and copies the old mode onto it. If someone else made the old file, the result is their content, your ownership, and their mark.

* **What the plan says.** P14 (`dev/plans/model-mapping-install-path.md:209`) "sets the old file's mode bits on it when one existed". C4 (`:379`) says "the new file keeps the old file's mode bits (`0o640` stays `0o640`)". The capture (`:352`) copies "the old file's mode bits". Neither says which bits, or how they are set. The usual ways, `stat.S_IMODE(st.st_mode)` and `shutil.copymode`, both include the setuid, setgid and sticky bits.
* **Probe 1, no race needed.** A stand-in of P14 that sets the mode through the descriptor, from the read's `fstat`. The old `.gitignore` was a copy of a program, with mode `0o4755`. After one seed call there was a new file (a new inode), still mode `0o4755`, owned by the user who ran the seed, holding the program's bytes with the ignore line appended. On this Mac the program then would not run: code signing killed it (exit 137). An ELF program with bytes appended still runs on Linux. I did not test Linux.
* **So, on a shared Linux machine,** such as a lab server with a group-writable project folder: another user makes `.gitignore` their own file, holding a program, and marks it `4755`, as anyone may do to their own file. You run install, `--stage`, `--adopt-module`, or an `--apply` that adds skills. The seed replaces the file with one you own, setuid, with their program in it. They run it, and it runs as you. Today the same file stays theirs. Git cannot carry a setuid bit, so this needs someone already on the machine: the premise the plan's hard-link fixes already accept.
* **Probe 2, the race.** The same stand-in, with the temporary file swapped for a link to a "victim" file (mode `0o600`) after the write and before the mode is set. Set by path (`os.chmod`), the victim became `0o664`, although the guard then refused the replace. Set by descriptor (`os.fchmod`), it stayed `0o600`. P14 sets the mode before its guard, and the capture after its guard; neither order protects a path-based call.
* **Recommended fix.** Set the mode with `os.fchmod` on the temporary's own descriptor, before closing it. Take the bits from the `fstat` of the descriptor that was read (for the capture, from the stat of the regular file it read), masked to read and write: `stat.S_IMODE(st.st_mode) & 0o666`. A `.gitignore` or a mapping never needs an execute or setuid bit, and `0o640` still stays `0o640`. Criteria: an old file with mode `0o4755` yields a new file with no setuid, setgid, sticky or execute bit; a stand-in that swaps the temporary for a link before the mode is set leaves the victim's mode unchanged and the replace refused. Mutants: drop the mask; set the mode by path. That stand-in also kills a mutant that drops the guard on the temporary file, which no criterion pins today. The capture's content is not the old file's, so the mask there is defence in depth. P13's install-record writer creates with `0o666` under the umask and copies nothing, so it is unaffected.

#### MM-SR-2 -- medium: a 900-byte mapping freezes the checker through YAML merge keys, and P8 says that cannot happen

**Plain:** YAML has a shortcut, `<<:`, that copies one mapping into another. Each line of a chain can copy the line before it twice, so the work doubles with every line, and the checker's YAML step never finishes. No mapping needs the shortcut.

* **What the plan says.** P8 (`:203`): the loader "walks the loaded value with an explicit stack, visiting each object once, so neither depth nor aliasing can blow it up". C1 (`:293`) tests a 22-level alias document. The walk is safe, but the blowup happens before it, inside `yaml.safe_load` (`scripts/check_model_selection.py:88`), which builds merged mappings eagerly.
* **Probe** (PyYAML 6.0.3). The file is `l0: &l0 {k0: 1}`, then `l{i}: &l{i} {<<: [*l{i-1}, *l{i-1}], k{i}: 1}` for each line, plus one real row. Load time by chain length: 20 lines (747 bytes) 1.45 s; 22 lines 5.2 s and 254 MB; 24 lines (895 bytes) 21.1 s and 772 MB. The cost doubles with each line. Today's checker on the 24-line file was still running when killed at 10 s (exit 124). A loader that refuses merge keys rejected the same file in 4 ms.
* **Why it matters here.** It is pre-existing, since today's structural step loads the same way, and it only denies service. But this plan rewrites that step and claims the property, and the check is what II-5 and the seeded row tell an agent to run, possibly in a project it does not trust.
* **Recommended fix.** Load with a `yaml.SafeLoader` subclass whose `flatten_mapping` raises a `ConstructorError` on any merge key and otherwise defers to the base, so such a file exits 3, "not valid YAML", before anything is built. Correct P8's sentence. Criterion: the 24-line chain exits 3 within a fixed time (a subprocess with a timeout of a few seconds); without the refusal it times out. Mutant: drop the refusal. Refusing anchors and aliases altogether would also work, and would make the visited set unnecessary, but it changes more behaviour than the accepted text asked for.

#### MM-SR-3 -- medium: Chunk M names no safe way to perform the AST correction, and hands the Maintainer agent-computed digests

**Plain:** the AST correction rewrites the fingerprints that prove the engine's code is the code that was reviewed. A safe correction works out the new fingerprints itself, from the code as it stands, and stops if anything moved that nobody declared. The plan does not say how this one is done.

* **No existing tool does it.** `update-symbol`, the runbook's only writer, refuses every symbol outside `_UPDATE_ALLOWLIST` (`bootstrap/AST_BASELINE_RUNBOOK.md:21-34`), and nothing generates the known-new file (`:78`). All eight symbols here are outside the list, so the Maintainer either edits two JSON files by hand or runs a script.
* **The last such correction ran a script that never entered the repository.** `lockfile-provenance-fields` Chunk G (`3cb85ca`, `c3d5bd98`) used `reanchor_lockfile_provenance_fields.py`, kept in an agent's scratch folder; its code review confirmed the script never entered the tree (`dev/plans/archive/lockfile-provenance-fields.md:1245`). The digests it wrote were whatever that agent's code computed, and no reviewer read that code. With Chunk M silent, that precedent is the default.
* **The plan supplies the figures.** C6 (`:398`) records, "for the Maintainer's use", the CHANGED set, the new symbols' digests and the re-keyed digest. The runbook says never to carry such figures forward (`AST_BASELINE_RUNBOOK.md:38`, `:122`).
* **The set is hard-coded, and already moving.** Chunk M (`:266`), C6 (`:401`) and the board row (`dev/PLANNING.md:334` at `20f145ed`) name "the repair's four CHANGED functions". The repair's answer, uncommitted in the shared tree as I write, adds guards to `create_dev_tree`, which is baselined. That set would become five.
* **The order with the gate-manifest re-anchor is not stated.** `bootstrap/tests/fixtures/scaffold_ast_known_new.json` is a frozen file in `bootstrap/tests/fixtures/gate_manifest.json` (checked by script), and the AST ceremony writes it. If the gate-manifest re-anchor the board is waiting on (`dev/PLANNING.md:370`) runs first, the AST ceremony then changes a frozen file. `test_gate_manifest.py` does not notice that, and a second re-anchor is owed.
* **Recommended fix (plan text only).** Chunk M states the steps, in order:
  1. Confirm that `bootstrap/_scaffold/` at the ceremony commit is byte-identical to the code-reviewed tested commit, and trace any difference first.
  2. Derive CHANGED, REKEYED, DROPPED and NEW fresh with `_ast_attest`'s own `_merge_current` and `_classify` (runbook Steps 1 and 2). Stop unless they equal the declared sets taken from the reviewed records, the repair's and this plan's, each traced to its commit.
  3. Write with a tool that computes every digest from the live tree and contains none, prints each key's old and new value in a dry run, refuses on any key not declared, and is committed and code-reviewed before the Maintainer runs it. Or name the by-hand procedure instead.
  4. Verify with `--known-new`, confirm the baseline count did not grow, and commit both fixtures by path.
  5. Only then run the gate-manifest re-anchor, so it records the post-ceremony `scaffold_ast_known_new.json`.

  C6 labels its digests "a cross-check the ceremony's own derivation must equal, never an input". Chunk M and the board row say "the symbols the repair changed, derived at the ceremony", not "four".

#### MM-SR-4 -- low: the hard-link `.gitignore` refusal prints an unspecified line, and the hint being added is wrong for it

* **The text is unspecified.** C4 (`:373`) asserts "exit 2 with the `.gitignore` refusal line"; P14 says what is refused, not what the message says. At `20f145ed` the three preflight catches (`bootstrap/_scaffold/cli.py:457` and two in `upgrade.py`) print a prefix and the exception text.
* **The hint is wrong for a hard link.** The repair's answer, uncommitted, appends "replace the link with a regular file, then re-run." A hard-linked `.gitignore` already is a regular file. The advice will baffle the one person who meets it, and a refusal that reads as nonsense invites working around it.
* **Open errors differ by kind.** The descriptor open fails with errno 62 for a link and 102 for a socket on this Mac, and with other numbers elsewhere. If only `ELOOP` becomes the refusal, a socket ends in a raw `OSError`.
* **Recommended fix.** State the hard-link message and pin it in C4: fixed text naming `.gitignore` and the reason, with a fix that is true for a hard link ("make it a file of its own: copy it to a new name, then move that over it"). State that every error from the descriptor open, except "no such file", becomes the refusal.

#### MM-SR-5 -- low: use one descriptor-based reader for all three files, with the repository's own flag set

* **Three readers, three recipes.** The notice helper (C3, `:335`) runs `lstat`, guards, then reads by path. The capture (`:350`) reads by path. `seed_gitignore` (P14) opens with `O_NOFOLLOW | O_NONBLOCK`. The repository already has a reviewed recipe: `_read_bounded` in `bootstrap/verify_integrity.py:115-157` opens with `O_NOFOLLOW | O_NONBLOCK | O_NOCTTY | O_BINARY`, built at call time, and reads through the descriptor only when `fstat` says it holds a regular file.
* **Why it matters.** With that recipe, the helper's "never opens anything but a regular file" holds by construction. With check-then-open it does not: a pipe swapped in between the `lstat` and the read would hang the install the notice exists to inform. That needs someone changing files during the run, so it is low.
* **`O_BINARY` on the writes.** The raw `os.open` creations in P13 and P14 leave out `O_BINARY`. On Windows `os.open` defaults to text mode, so `os.write` turns each newline into a carriage return and a newline. That would alter the base-cache bytes, which must equal upstream, and break P15's byte-exactness. `mkstemp` adds `O_BINARY` itself. Not measured, since I have no Windows host; the engine's copy-mode fallback for hosts without symbolic links shows it does not rule Windows out.
* **Recommended fix.** The three reads use the `_read_bounded` flag set and `fstat` on the descriptor. The creations in P13 and P14 add `getattr(os, "O_BINARY", 0)`.

#### MM-SR-6 -- low: the line rule finds rows that are not rows, and the plan lists one member of that class

* **The divergence.** The bare checker and the engine accept a `tier:` line anywhere outside a comment; PyYAML looks inside `mapping`. With a stand-in of the rule P3 describes (the author's prototype is not committed), three files with `mapping: []` passed the line rule and failed the YAML rule. One had a row under another key, one a row inside a block scalar, and one a row inside a quoted value spread over lines. The engine would stay silent on each of them.
* **The plan lists one member.** It names only "a repeated empty `mapping:` key" (C1, `:291`; Named residuals, `:569`). The generated corpus cannot produce the others, so "a difference outside both lists fails" (`:294`) never meets them.
* **Severity.** Each needs a deliberate spelling by someone who could edit the checker anyway, so no authority is at stake. But the plan's title promises a check that is right both ways.
* **Recommended fix.** Name the class in Named residuals ("a row-shaped line that is not an item of `mapping`"), and add those three files to the explicit stricter-with-PyYAML list.

#### MM-SR-7 -- low: the checker's new lines must never print a parsed value

* **The gap.** The value scan and the no-row check add failure messages. The plan says the no-row message "does not say `FILL ME`" (`:289`), but not what either message prints. A parsed value can hold ESC and BEL: `"\e]0;PWNED\a\e[2J"` loads as `'\x1b]0;PWNED\x07\x1b[2J'`. Printing it would send control sequences to the terminal of whoever runs the check. Today's checker never prints a value.
* **Recommended fix.** A criterion that both new messages are fixed text plus the mapping's path. Its fixture is a `FILL ME` value carrying `\e` and `\a` escapes, and it asserts no ESC or BEL byte on standard output or standard error.

#### MM-SR-8 -- low: the real-install refusal fixture stops earlier once the repair's `dev/` guard lands

* **Today the fixture works.** C4 (`:355`) proves the capture itself refused by installing over a linked `dev/.cairn` that already holds the files every earlier step needs. Probed at `20f145ed`, an interactive install over that tree reaches the capture.
* **After the repair's answer it will not.** With the repair's uncommitted `create_dev_tree` guard applied to a scratch copy, the same install stops in `create_dev_tree` with a traceback (`dev/.cairn` is in `_DEV_DIRS`), and the capture is never reached.
* **A fixture that works in both.** A mapping that is itself a link to an outside file reached the capture in both copies, because `_install_one` skips an existing destination before its guard.
* **Recommended fix.** Use the linked mapping file for the real-install case, and keep the linked `dev/.cairn` in the direct-call test. The distinctive-name and no-lockfile assertions carry over unchanged.

#### MM-SR-9 -- low: replacing `.gitignore` overrides a read-only file and changes its owner

* **Probed.** A rename needs write permission on the folder, not on the file. Over a `.gitignore` with mode `0o444`, today's seed fails with `PermissionError`; the stand-in of P14 replaced the file and kept `0o444`. The new file also belongs to the installer, takes a group chosen by the folder and the system rather than the old file's, and loses the old file's extended attributes.
* **Not listed.** C4's "Behaviour that must not change" (`:379`) names none of these. None writes outside the project, but a person who made `.gitignore` read-only to stop tools editing it is overridden without a word.
* **Recommended fix.** Either open the old file with `O_RDWR` rather than `O_RDONLY`, so a file you may not write is refused as before and is still never written through, or name the three changes among P14's residuals.

#### MM-SR-10 -- low: three stale sentences, and one recommendation with no disposition

* **The ledger contradicts C4.** The ledger row for SEC-1 (`:412`) says "C4 leaves the `seed_gitignore` row alone", and the capture's inventory bullet (`:364`) says "The `seed_gitignore` row is untouched". The `.gitignore` inventory bullet (`:381`) rewrites that row. SEC-1's "makes no containment claim about it" no longer holds either, because C4 changes `seed_gitignore`'s containment.
* **S5 is incomplete.** S5 (`:564`) says the hard-link case is closed "for the capture and for the install-record writer". The `.gitignore` append is closed too, by refusal.
* **One recommendation has no disposition.** GS-SR-3 also recommended that `bootstrap/SAFETY.md`'s accepted "small TOCTOU window" say what a won race does: it overwrites. The plan neither does that nor defers it. After this plan, three writers no longer have the window, and the rest still overwrite on a win.
* **Recommended fix.** Correct the three sentences, and give the `SAFETY.md` point a disposition: fold one sentence, or defer it at archive with the other deferrals.

### What I did not cover

* **Linux and Windows.** Everything ran on macOS (APFS). MM-SR-1's escalation depends on Linux running an ELF with bytes appended, which I did not run. MM-SR-5's Windows point comes from the documented `os.open` default, not from a run.
* **The plan's own code.** None exists yet. P14/P15 and the bare row rule were tested as stand-ins written from the plan's words.
* **The ordinary Internal pass's ground**: wording, sequencing, the seeds, the board's row grammar, the stub merge, the presets. I did not read that pass's findings.
* **The full suite.** I ran no test node. The AST figures come from `_ast_attest`'s own functions, run on a scratch copy.
* **The lockfile reader.** `read_lockfile` (`bootstrap/_scaffold/lockfile.py:279`), which `_commit_lock_and_caches` calls first, follows a link and would open a pipe. It is pre-existing, outside this plan, and needs someone on the machine. Noted, not raised.
* **A full sweep of in-place engine writes for the hard-link class.** The plan also says none was made.
* **The repair's answer in flight** (the `create_dev_tree` guard, the refusal hint). I read it from the shared tree's uncommitted diff, only to see what will move under this plan.

## Response to plan review -- Claude Sonnet 5.5 (author) -- 2026-10-18

This answers the Internal review (`d13bd2ac`, MM-PR-1 to MM-PR-12) and the Internal Security Review (`dd390797`, MM-SR-1 to MM-SR-10). Per the template, every correction is made in the operative cells above, and this section only points at them. There is no second plan-review round. Status moves to `ready-to-implement`.

**In plain terms.** I accepted all 22 findings. Two I changed rather than took as written: the `RecursionError` catch (kept, but re-labelled as the plan's own addition), and the four lockfile writers (the reviewer said not to widen; the Maintainer later said yes, so they are in). The blocking one, MM-SR-1, is fixed by writing permissions on the file descriptor, masked to read and write. Three things came in after the reviews and **no plan reviewer has read their design**: the `.gitignore` points (the Maintainer's answer), the four other lockfile writers and the lockfile reader (the Maintainer's answer), and the shared reader and writer helpers that carry them (a consequence of the reviewers' own advice). The plan says so in C4 and C6, and the implementation's code review and Security Review are told to cover each.

| ID | Disposition | Where it landed, or why not |
|---|---|---|
| MM-PR-1 | accepted | C1: the corpus is two parts, 108 generated files plus a named spelling table with three exit codes and a list per member; the PyYAML row rule is defined; C3: the engine meets the whole set; M7 split into M7a and M7b; the In brief says "108 generated files and a table" |
| MM-PR-2 | accepted | C4 (b): the real-install test uses a linked mapping file; the linked `dev/.cairn` stays in the direct-call test; the replaced fixture is noted; the exit-code table and the stale list no longer name `write_local_env` |
| MM-PR-3 | accepted | *Frozen files, AST and the oracle*: every criterion is a set difference against P and T, no count; C6 and the sequencing cell likewise |
| MM-PR-4 | accepted | C4 (b) and (e): `SECURITY_MUTATIONS.md` gets additions only (the capture's row and catch, one sentence on the `seed_gitignore` row); the repair's remedy line is in the exit-code table; the gate re-reads the paragraph, the row and `_GUARDED_WRITE_FUNCS` at the parent |
| MM-PR-5 | accepted | C2 quotes the seven shipped blocks (Revision 2's R2.5, verbatim) and pins three load-bearing strings by exact match |
| MM-PR-6 | accepted, widened by the Maintainer | The reviewer's fix was to name the four writers and not widen. The Maintainer then answered "Yes, fold them into the plan" (*Scope*, item 5), so C4 (d) fixes the four writers and the reader. Their design was read by no plan reviewer; C6 names them for the code review. The remaining in-place writers (base caches, swap writes, `_write_stage`, `_install_one --force`, profile writes, the module-merge side-file) are named in *Named residuals* and *Dispositions* |
| MM-PR-7 | accepted | P15 reversed: the preflight's `lstat` refuses a folder, pipe, socket or device; the attribution is corrected (the Maintainer's words were only "Yes, fix the .gitignore points"; "regression" was the coordinator's word); residuals updated |
| MM-PR-8 | modified | The explicit-stack walk stays. I kept the `RecursionError` catch, and it is filed as the plan's own addition in *Scope delta* and P8, not "at the Maintainer's instruction". Reason: two lines on a path the plan already rewrites, and the Security review confirmed the crash. If a reviewer would cut it, nothing accepted is lost |
| MM-PR-9 | accepted | The AST correction runs first, then the gate-manifest re-anchor once, in chunk M, the In brief, *Frozen files, AST and the oracle* and the queued row; "seven" and "six" read consistently |
| MM-PR-10 | accepted | C4 (b): `TestCaptureDocstringNamesWhereItRuns`; C2: the eight family sites are named in a table with their exact phrases, and a closed-set search notices a ninth |
| MM-PR-11 | accepted | P6 and C4 (b): the capture's refusal carries a fixed remedy sentence; C4 (e): the hard-link refusal's text and the remedy line are specified and pinned |
| MM-PR-12 | accepted | P16, P17: flags built with `getattr`, the mode set with `fchmod` where it exists, a test that removes the flags from `os`, mode tests skipped where there are no POSIX modes (M52) |
| MM-SR-1 (blocks) | accepted | P17, C4 (a): `os.fchmod` on the temporary's descriptor, masked `& 0o666`, never by path; tests for a `0o4755` source and for a swap before the mode is set; M35, M37, M38 |
| MM-SR-2 | accepted | P8, C1: a `SafeLoader` subclass refuses merge keys; the 881-byte chain exits 3 inside a timeout; P8's false sentence is rewritten; M39 |
| MM-SR-3 | accepted | Chunk M: five steps from the runbook, nothing pre-filled, derive and dry-run first, any script committed and reviewed first, AST ceremony before the re-anchor; the hard-coded "four" is gone; C6's figures are a cross-check only |
| MM-SR-4 | accepted | C4 (e): fixed refusal text true for a hard link, pinned; every open error except "no such file" becomes the refusal (P16) |
| MM-SR-5 | accepted | P16: one `_read_regular_bytes` with the repository's flag set, shared by the notice helper, the capture, `seed_gitignore` and `read_lockfile`; `O_BINARY` on the writes (P17) |
| MM-SR-6 | accepted | The class is named in *Named residuals* and the checker's docstring; the three files are on the "stricter with PyYAML" list in C1 |
| MM-SR-7 | accepted | C1: both new messages are fixed text plus the path; an ESC and BEL fixture; M44 |
| MM-SR-8 | accepted | As MM-PR-2 |
| MM-SR-9 | accepted | The cheap option: `seed_gitignore` refuses a file it cannot write (`os.access`, M42), and the owner, group and attribute changes, and the capture and lockfile writers' lack of that check, are named in *Named residuals* |
| MM-SR-10 | accepted | The SEC-1 ledger row and the S5 sentence are corrected; the `SAFETY.md` sentence about a won race is folded into C4 (e); the optional `fsync` is declined in *Dispositions* |

**Also taken from the reviews.** The Internal review's offer of a single writer helper (its Answer 2) is adopted, in the shape of two helpers in `security.py`, because the Maintainer's later answers added four more callers and a hand-written recipe in each would have drifted. The capture's accepted "all inline" is a means, not an outcome; C4 (b) records the change. The Security review's rule that cleanup removes only what the call created is in the helper's criterion and in M32. The stale sequencing cells (the neutrality plan, `board-as-basis`) are updated. P4 now says why the structure is judged before the rows.

**Not taken.** The optional `fsync` (MM-SR-10): an in-place write has the same crash window, so it is no worse. A size cap on reads (P9) was not asked for and stays a residual.

## Implementation verification -- Claude Sonnet 5.5 (scribed at Maintainer direction) -- 2026-10-20

**Boundary B mode**: full required for the scaffold engine and install contract surfaces; scoped integration run performed at `1b609e5c` under canonical interpreter Python 3.13.13, with full certifying suite deferred to Maintainer certification. **Certified by**: pending. `CAIRN_FULL_SUITE` was never set.

**Tested commit**: `1b609e5c03e18f7e156a33020f29f271d274d6d8`.
**Reviewed range**: `26b214194c502da2913b7b51b74e6c38ceee1ce8..1b609e5c03e18f7e156a33020f29f271d274d6d8`.
The plan's implementation commits are `6dcbdda7` (C1), `7e1faa64` (C3/C4), `a3672176` (C4), `90c6f35a` (C2), `6d0de9ac` (C4), `4f313242` (C4), and `1b609e5c` (C6). Intervening commits in the range belong to other sessions' work.
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python 3.13.13.
**Pre-run state**: clean `git status --porcelain` in the working tree apart from untracked `.claude/` and `dev/measurement/collision_log.md`. **Post-run state**: the same clean status and unchanged SHA.

### Scoped Test Execution

Mapped test suites run via `python -m pytest -q` under Python 3.13.13:

* **Primary mapped suite (5 files):** `bootstrap/tests/test_model_selection_stub.py`, `bootstrap/tests/test_security_leaf.py`, `bootstrap/tests/test_upgrade_module_additions.py`, `bootstrap/tests/test_onboarding_seed_roster.py`, `bootstrap/tests/test_intents_tool.py`: **273 passed** in 36.97s (0 skips/xfails/xpasses).
* **Secondary mapped suite (5 files):** `bootstrap/tests/test_scaffold.py`, `bootstrap/tests/test_lockfile_module.py`, `bootstrap/tests/test_verify_integrity.py`, `bootstrap/tests/test_presets.py`, `bootstrap/tests/test_profiles_smoke.py`: **284 passed** in 5.30s (0 skips/xfails/xpasses).
* **Upgrade suite (1 file):** `bootstrap/tests/test_upgrade.py`: **106 passed** in 14.31s (0 skips/xfails/xpasses).
* **AST gate test (1 file):** `bootstrap/tests/test_ast_attest.py`: **28 passed, 2 expected non-passes** (0.19s).
Total mapped tests passing: **691 passed**.

### Standing Quality Gates

* `python scripts/quality_gate.py --sub neutrality --sub redundancy`: neutrality `fail=0` (56 informational); redundancy `fail=0`.
* `python scripts/check_cairn.py`: 1 disclosed flag (line citation at `dev/plans/model-mapping-install-path.md:1020` exceeding `dev/PLANNING.md`).
* `python scripts/claim_check.py`: clean across touched durable documentation.
* `python bootstrap/scaffold.py --manifest`: byte-identical to parent manifest.

### Non-Pass Disposition

* **`test_ast_attest.py`**: 2 expected failures (`test_committed_baseline_accounted_for_across_the_engine_package` and `test_ast_gate_passes_over_the_full_scaffold_module_set`). The baseline was already stale before this plan. Per Maintainer ruling (*"Yes, use exact measured delta"*), `_apply_upgrade` was already classified as changed before this plan's first engine commit; its baseline digest was `dc53397782e91c18` and is now `f05f1ee7ad8c58fe`. The newly changed engine function definitions added by this plan are exactly 5: `capture_model_selection_mapping` (`baf873c923f3060e`), `write_install_lockfile` (`88db57e796412133`), `_cmd_init_lock` (`e630648f70117ff9`), `_cmd_finalize_lockfile` (`4966e1fa55574461`), and `read_lockfile` (`662e46033c193c42`), along with previously changed engine functions `main` (`0270e7f38e594156`), `_cmd_adopt_module` (`c4ee1bcae92a9f80`), `cmd_upgrade` (`e334138dcc0745aa`), and `seed_gitignore` (`490255ef714f9afe`). The known-new re-key is `_commit_lock_and_caches` (`acda3d85b18f7f18`). The newly added function definitions are exactly five: `_mapping_is_unfilled`, `_read_regular_bytes`, `_stage_exclusive`, `_write_by_replacing`, and `model_selection_notice_lines`. The failures end when the Maintainer executes the combined AST and manifest ceremony.
* **`check_cairn.py`**: 1 flag in line 1020 of this plan file (`dev/PLANNING.md:370` citation from earlier review response); disclosed as historical plan text, not live adopter guidance.

### Mutation Ledger

All 52+ plan mutations (`M1`–`M52`, `M38-paired`, `MM-SR` stand-ins) were executed against commit `1b609e5c` via `/private/tmp/cairn-model-mapping-mutations.py` beside unmutated control runs (control runs: 100% passed). All 52 mutants were **killed**:
- `M1`–`M40`, `M42`–`M52`, `M38-paired`, `MM-SR` stand-ins: killed by targeted test failure (returncode 1).
- `M41` (`O_NONBLOCK` removed from `_read_regular_bytes`): **killed** by timeout on named-pipe test (`test_special_files_refused_without_blocking`), confirming non-blocking refusal.
- Survived mutants: **0**.
- Unmeasured equivalents: **0**.

### Stub Merge Measurement

Measured on `1b609e5c` with base stub `26b21419:templates/modules/team-gated/model_selection_mapping_stub.yml` and theirs `templates/modules/team-gated/model_selection_mapping_stub.yml`:
- (a) untouched stub: exit 0 (clean merge).
- (b) hand-filled stub keeping comments: exit 0 (clean merge).
- (c) interactive capture output: exit 1 (conflict). `upgrade --apply` refuses while conflict markers remain and writes nothing.
- (d) rewritten header: exit 0 (clean merge).

### Smoke Checks & Maintainer Rulings

- **Vendor-name grep**: Per Maintainer ruling (*"Yes, record allowed matches"*), the installed-tree vendor-name grep matches the filled mapping, as well as existing explicitly allowed onboarding examples and lockfile caches; the neutrality gate itself passes cleanly (`fail=0`).
- **Checker verification**: `scripts/check_model_selection.py` returns exit code 1 on the stub, 0 on a hand-filled stub, and 0 on Cairn's own filled mapping.
- **Install & upgrade notices**: `scaffold.py --config <profile> --target <tmp> --non-interactive` prints the first notice and exits 0. `upgrade --plan` prints the notice. `board.py --maintainer` lists the seeded row.

### Reviewer Handoff Briefing (Late Additions)

Per C6 acceptance criterion (:542), the code review and Internal Security Review are notified that:
- The four other lockfile writers (`write_install_lockfile`, `_cmd_init_lock`, `_cmd_finalize_lockfile`, `_apply_upgrade`), the lockfile reader (`read_lockfile`), and the `.gitignore` append (`seed_gitignore`) were folded into C4 (d) and C4 (e) after both plan reviews.
- The review must cover all seven callers of the writer helpers (`_stage_exclusive`, `_write_by_replacing`) and the callers of `_read_regular_bytes` explicitly by name.

## Code review (Internal + Internal Security Review) -- Antigravity (code reviewer) -- 2026-10-20

```
Reviewed commit: b400c03ce7bf4ec1c9ea5a528a472a1cf58a5c68
Target: 26b214194c502da2913b7b51b74e6c38ceee1ce8..1b609e5c03e18f7e156a33020f29f271d274d6d8
Prior findings: none
```

**Obligation**: safe writes, temporary descriptor races, lockfile reader containment, and late-addition coverage (C4 (d) and C4 (e)).

**Foundations**:

1. **Should this happen as framed?** Yes; the implementation correctly hardens all seven write sites against symlink/hard-link redirection, prevents descriptor races, safely contains the lockfile reader against pipes and links, skips comments while requiring rows in the checker, and emits non-interactive notices reliably across all install/upgrade paths -- verified across 691 passing mapped tests (`bootstrap/tests/test_model_selection_stub.py`, `bootstrap/tests/test_security_leaf.py`, `bootstrap/tests/test_upgrade_module_additions.py`, `bootstrap/tests/test_onboarding_seed_roster.py`, `bootstrap/tests/test_intents_tool.py`, `bootstrap/tests/test_upgrade.py`).
2. **Best alternative.** None simpler or safer; factoring atomic replacement into `_stage_exclusive` and `_write_by_replacing` in leaf module `bootstrap/_scaffold/security.py` using `O_CREAT | O_EXCL`, `secrets.token_hex(8)`, and `os.fchmod` masked with `& 0o666` on the open descriptor eliminates TOCTOU windows and prevents mode-escalation vulnerabilities across all seven engine writers (`bootstrap/_scaffold/security.py:54-108`).
3. **What would show it wrong.** A surviving mutant in any of the 52+ plan mutation specifications or a failure of any writer helper to refuse symlinks/hardlinks, or a lockfile reader that hangs on a FIFO pipe -- see the falsification ledger below.

**Bounding**: ACCEPTED. Boundary B's full scope was challenged by testing the contract surface (`bootstrap/scaffold.py --manifest`), checking link/pipe refusal in `read_lockfile`, verifying non-UTF-8 preservation in `seed_gitignore`, testing descriptor mode mask safety against setuid/executable source files, and verifying that all 52 plan mutants were killed without unmeasured survivors.

### Falsification Ledger

Targeted independent falsification checks executed against commit `1b609e5c`:

| Focus Area | Probed Condition / Challenge | Observed Result | Verdict |
|---|---|---|---|
| **C1 Check Parity & Limits** | Checked comment skip with real row vs empty mapping vs merge-key chain (`<<: *anchor`). | Comments skipped cleanly (exit 0); empty mapping refused (exit 1); merge key refused with `ConstructorError` (exit 3 in 0.12s). | PASS |
| **C2 Presets & Board** | Ran `tools/board.py --maintainer` on clean fresh install of both `collaborative-team` and `high-rigor-legacy`. | Both presets seed `**Waiting on Maintainer**: fill the model mapping` and board reports it on day one. | PASS |
| **C3 Notice Mechanics** | Probed non-interactive install, interactive with filled mapping, and interactive with absent mapping. | Non-interactive prints notice and exits 0; filled mapping stays silent; absent mapping stays silent. | PASS |
| **C4 Helper 1: `capture_model_selection_mapping`** | Preflight containment checked against symlinked mapping and parent symlink before prompting. | Refused early with constant line to stderr without prompting; exits 2 without target leak (`test_real_interactive_install_refuses_link_without_leaking_target`). | PASS |
| **C4 Helper 2: `seed_gitignore`** | Hard link (`st_nlink > 1`), un-writable file (`os.access`), and non-UTF-8 byte sequence tested. | Hard link refused early with specific remedy text; read-only refused; non-UTF-8 bytes preserved bit-for-bit (`TestGitignoreSeedWritesByReplacing`). | PASS |
| **C4 Helper 3: `write_install_lockfile`** | Planted hard link at `dev/.cairn/cairn-lock.yml` prior to install write. | Replaced by exclusive temporary; hard link target untouched (`test_install_does_not_write_through_a_hardlink`). | PASS |
| **C4 Helper 4: `_cmd_init_lock`** | Planted hard link at lockfile during `--init-lock`. | Replaced by exclusive temporary; hard link target untouched (`test_init_lock_does_not_write_through_a_hardlink`). | PASS |
| **C4 Helper 5: `_commit_lock_and_caches`** | Planted predictable sibling temp names and forced collision during staged commit. | Exclusive creation refuses collision (`O_EXCL`); failure cleans up only newly created temporaries (`TestLockCommitWritesThroughExclusiveTemporaries`). | PASS |
| **C4 Helper 6: `_cmd_finalize_lockfile`** | Planted hard link at lockfile during `--finalize`. | Replaced by exclusive temporary; hard link target untouched (`test_finalize_does_not_write_through_a_hardlink`). | PASS |
| **C4 Helper 7: `_apply_upgrade`** | Planted hard link at lockfile during upgrade apply. | Replaced by exclusive temporary; hard link target untouched (`test_apply_does_not_write_through_a_hardlink`). | PASS |
| **C4 Reader: `read_lockfile`** | Symlink, dangling link, directory, and named FIFO pipe at `cairn-lock.yml`. | Refused without following links; FIFO pipe refused without blocking (`TestLockfileReaderRefusesAnythingButARegularFile`). | PASS |
| **C4 Mode Masking** | Source file with permissions `0o4755` (setuid + exec) replaced via `_write_by_replacing`. | New file mode masked `& 0o666`, resulting in `0o644` without setuid or execute bits (`test_swapped_temp_cannot_change_victim_mode`). | PASS |
| **C5 Adopt/Upgrade Notice** | Notice emission tested across `--adopt-module`, `upgrade --plan`, `upgrade --stage`, and failed vs successful `upgrade --apply`. | Printed after plan/stage and successful apply; omitted on failed apply (`TestNoticeOnEveryInstallPath`). | PASS |
| **C6 Mutation Ledger** | Independent re-execution of `/private/tmp/cairn-model-mapping-mutations.py` across all 52 mutants (`M1`–`M52`). | 52 mutants killed, 0 survived, 0 unmeasured equivalents; control pass 100%. | PASS |

### Late Additions Coverage (C4 (d) and C4 (e))

Per C6 handoff criterion (:542), the late additions folded in after plan review were scrutinized:
- **Seven writer helper callers:**
  1. `capture_model_selection_mapping` (`bootstrap/_scaffold/install.py:965`): read, nothing found. Preflight guard at line 901 precedes prompts; write is gated by `_write_by_replacing`.
  2. `seed_gitignore` (`bootstrap/_scaffold/install.py:266`): read, nothing found. Preflight lstat checks file kind and link count (`st_nlink == 1`); writable access verified before staging; non-UTF-8 prefix preserved; replaces atomically.
  3. `write_install_lockfile` (`bootstrap/_scaffold/install.py:2066`): read, nothing found. Directory creation followed by `_write_by_replacing`.
  4. `_cmd_init_lock` (`bootstrap/_scaffold/upgrade.py:1412`): read, nothing found. Emitted lock written through `_write_by_replacing`.
  5. `_commit_lock_and_caches` (`bootstrap/_scaffold/upgrade.py:1509`, `1513`): read, nothing found. Multi-file staging creates exclusive siblings tracked by inode/device identity; replaces in reverse order; unlinks un-replaced siblings on failure only when identity matches.
  6. `_cmd_finalize_lockfile` (`bootstrap/_scaffold/upgrade.py:2058`): read, nothing found. Finalized lock written through `_write_by_replacing`.
  7. `_apply_upgrade` (`bootstrap/_scaffold/upgrade.py:2382`): read, nothing found. Applied lock written through `_write_by_replacing`.
- **Lockfile reader callers (`read_lockfile`):**
  1. `cmd_upgrade` (`upgrade.py:1320`): read, nothing found.
  2. `_commit_lock_and_caches` (`upgrade.py:1489`): read, nothing found.
  3. `_behind_by_n` (`upgrade.py:1621`): read, nothing found.
  4. `_cmd_adopt_module` (`upgrade.py:2560`): read, nothing found.
  5. `write_install_lockfile` (`install.py:2029`): read, nothing found.
  All five callers receive `None` on missing or unparseable files, and `_read_regular_bytes` prevents following symlinks or hanging on special devices/FIFOs.

### Findings

No defects found. All acceptance criteria and security obligations are satisfied. Status moves to `ready-to-archive`.

### What I did not cover

- **Operating systems other than macOS (APFS):** The checks were verified on Darwin APFS. Windows file locking semantics and Linux ELF binary execution residuals were not verified on native kernels.
- **Full suite certifying run:** As required by `AGENTS.md`, `CAIRN_FULL_SUITE` was not run; full tree certification remains pending the Maintainer's next certifying run.
- **Combined AST baseline and gate manifest re-anchor:** Chunk M is explicitly Maintainer-only and runs after archiving.

## Archive note -- Claude Sonnet 5.5 (scribed at Maintainer direction) -- 2026-10-20

The independent code review and Internal Security Review at `64e88420` accepted
the implementation with no findings and a 14-item falsification ledger. This
archive is distinct from the implementation and review commits. The
adopter-visible changes are live: non-interactive and upgrade notices, safe
atomic writes through `_stage_exclusive` and `_write_by_replacing`, link/pipe
containment, and comment skipping and merge-key refusals in `check_model_selection.py`.
The changelog and roadmap boards now point to this record.

**Maintainer Ceremony Order (Chunk M):**
The Maintainer's 0.4 ceremony derives the actual frozen-file, AST, and
collection deltas. As settled by chunk M and the Decision, the ceremonies run
in this strict order: **the AST correction first, then the gate-manifest
re-anchor once.** This archive performs none of those re-anchors.

**Pinned test collection changes:**
- Removed: `TestFidelityCheck::test_fill_me_in_comment_fails` (replaced by
  `TestCommentsAreNotPlaceholders`).
- Added node classes: `TestCommentsAreNotPlaceholders`,
  `TestAMappingNeedsAtLeastOneRow`, `TestParsedValuesAreScannedWhenYamlIsPresent`,
  `TestMergeKeysAreRefused`, `TestCheckerMessagesCarryNoParsedValue`,
  `TestBarePathResidualIsPinned`, `TestValueScanVisitsEachObjectOnce`,
  `TestThisRepositorysMappingIsFilled`, `TestEngineAndCheckerAgreeOnUnfilled` in
  `bootstrap/tests/test_model_selection_stub.py`;
  `TestStubExampleNamesAFamilyNotAVersion`,
  `TestAcceptanceChecklistNamesTheMappingCheck`,
  `TestShippedWordsArePinnedByExactString`,
  `TestFamilyNotVersionReachesEverySite`; in
  `bootstrap/tests/test_onboarding_seed_roster.py`:
  `TestModelMappingWaitingSeed`; in `bootstrap/tests/test_security_leaf.py`:
  `TestReadRegularBytesRefusesAnythingElse`, `TestWriteByReplacing`; in
  `bootstrap/tests/test_upgrade_module_additions.py`:
  `TestLockCommitWritesThroughExclusiveTemporaries`,
  `TestLockfileWritersWriteByReplacing`,
  `TestLockfileReaderRefusesAnythingButARegularFile`; in
  `bootstrap/tests/test_intents_tool.py`: `TestGitignoreSeedWritesByReplacing`.

**Adopter upgrade cost:** An adopter whose stub header was rewritten (e.g. `lhm`)
will encounter one clean 3-way merge conflict on `dev/.cairn/model-selection-mapping.yml`
at their next upgrade; keeping their own side resolves it.

**Dispositions:**
- `accept`: C1 checker comment/row/value scan and merge-key refusal; C2 family
  wording, II-5 checklist, and onboarding seeds; C3 install notices; C4 safe
  atomic replacement writers, descriptor mode masking (`& 0o666`), and
  link/pipe containment; C5 upgrade and adopt notices.
- `defer`: The Maintainer-only AST correction and gate-manifest re-anchor at
  the 0.4 cut, in the board's ceremony register.
- There is no open Waiting line.
