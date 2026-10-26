# Next session

*Rewritten from scratch 2026-10-19. Work paused for a few days while credits
reset. Start with `python tools/session.py session-start` and
`python tools/board.py --maintainer`. This file is hand-written and may be
stale by the time you read it, so **check each claim against `git log`
before repeating it**. Three agents were told to stop cleanly as this was
written. How far each got is in the commit log, not here.*

## Where the project stands

**The goal is release 0.4, with the repository made public.** The cut line is
the "Revised 2026-10-19" block in `dev/PLANNING.md` (Release path), and the
external test is waived for 0.4. Still to land before the cut:
* the review-stance plan;
* the collaboration-agreement removal;
* board-as-basis;
* model-mapping-install-path;
* the answers to two Security Reviews.

**166 commits are unpushed** (`origin/master` is at `9832c411`). Pushing is
always the Maintainer's call. Before any push there is one **certifying run**:
the full-suite pair on a clean, committed tree. See AGENTS.md, "The full suite
runs only as a certifying run". Nobody runs the full suite for any other
reason. Until the Maintainer's re-anchor at the cut, the AST attestation test
fails on 2 nodes. That failure is expected, because engine symbols changed
and the baseline is re-pinned only at the cut.

**Archived since the last handoff:**
* plan A, verification practice;
* plan B, maintainer attention;
* plan C, `neutrality-and-upgrade-slots` (`caf3d022`);
* plan D, `independent-scientific-check` (`6c8b8eff`).

**Doctrine changed:** the full suite now runs only as a certifying run
(`12be58d9`).

**The repository was renamed** to `MSUHydrogeology/cairn` (`72248e15`).

## In flight at the pause

Each item names the next step and who holds it.

1. **The upgrade lockfile-path repair** (`d299f37c..2f07f2e7`).
   * **State:** its Security Review cleared it in a single round at `f0280ef0`
     and raised 8 findings, LP-SR-1 to LP-SR-8. The Maintainer folded the
     older LP-SR-1, a linked `dev/.cairn/profile.yml` that `upgrade --apply`
     writes through, into the same answer, and asked for one round only.
     His words:

     > "Fold into this answer (Recommended)"

     > "Let's just not iterate back and forth on the Security Review"

     > "For now let's just do the single-round Security Review for these"

     The findings are in
     `dev/reviews/2026-10-19-security-review-upgrade-lockfile-paths.md`.
     **At the pause none was fixed, and nothing was committed.** The fixer's
     drafted tests were never run. They were discarded from the tree, and a
     copy was saved outside the repository, in this session's temporary
     scratch folder, as `lpsr/lpsr-tests-uncommitted.patch`. That copy may
     not survive a reboot, so treat it as a convenience only.
   * **Next:**
     1. Answer all eight. Each has its exact fix and closing test in the
        record.
     2. Run **one code review** in a different session, covering the repair
        and the answer together.
   * **No second Security Review.**
   * **The fixer's design notes:**
     * `test_drift_surfacing.py` is frozen and pins the "git metadata
       missing" text. So in `_behind_by_n` (LP-SR-3), the new hex check goes
       *after* the "missing or `unknown`" check.
     * LP-SR-1's guard also refuses a `profile.yml` linked to a file
       *inside* the project. That is stricter than before but matches the
       `.gitignore` rule; say so in `bootstrap/UPGRADE.md`.
     * LP-SR-8's `.git` refusal should key on the project tree, not only the
       `dst` and `base_cache` fields. The shape-table test calls the guard
       with four positional arguments, so it would not see a new keyword
       parameter.
     * LP-SR-5's split must still run the `files` and `modules` structure
       checks before the advisory. The advisory crashes on a record that is
       not an object.
     * LP-SR-4 is best refused in `_check_lockfile_paths`, through a new
       `_check_staged_names`, rather than escaped in `_print_upgrade_report`.
     * All new tests go in
       `bootstrap/tests/test_upgrade_lockfile_path_containment.py`, which is
       not frozen.
2. **The session-start interpreter-binding repair** (`7e6a14e5..7832d057`).
   * **State:** SW-SR-1 cleared at `bf746470`, in a single round under the
     same words. Of the six new findings, SW-SR-10 is **accepted in writing**
     by the Maintainer:

     > "Accept in writing; move later (Recommended)"

     The gap: a binding that git does not track is still run. Moving the
     binding into the `.git` folder is deferred to a proposal after 0.4. The
     findings are in `dev/reviews/2026-10-18-security-review-session-writes.md`.
     **At the pause none was fixed, and nothing was committed**, not even
     SW-SR-10's acceptance text. The fixer's untested test hunks were saved
     outside the repository in this session's scratch folder, as
     `sw-sr-11-15-tests.patch`. That copy may not survive a reboot.
   * **Next:**
     1. Write SW-SR-10's acceptance: one docstring sentence in
        `_resolve_interpreter` and a residual-risk entry in
        `bootstrap/SAFETY.md`, with the Maintainer's words in the commit
        body.
     2. Fix SW-SR-11 to SW-SR-15.
     3. A code review checks the answer. No second Security Review.
   * **The fixer's design notes:**
     * **Where to edit.** Edit `templates/skills/_lib/session.py`, copy it to
       `tools/session.py`, and check with `cmp`.
     * **How the earlier answers were recorded.** They lived in commit bodies
       only, and each one re-finalized the lockfile line for
       `tools/session.py`.
     * **Where new tests go.** Not in
       `bootstrap/tests/test_session_binding_untracked.py`: it is frozen (a
       key in `frozen_files` of `bootstrap/tests/fixtures/gate_manifest.json`).
       So are `test_prune_tools.py`, `test_session_failsafe.py`,
       `test_session_kernel.py` and `test_session_routines.py`. Use the
       unfrozen `bootstrap/tests/test_session_binding_gate_and_printing_hold.py`.
     * **SW-SR-11.** Give `_binding_untrusted` an optional interpreter
       argument. If the interpreter lies inside the project, run the same
       index check on it, submodule rule included, and return a fixed reason.
     * **SW-SR-12.** Also compare device and inode for the binding and its
       two parent folders against the index entries.
     * **SW-SR-14.** Catch `(OSError, ValueError)` at both the read and
       `_probe_interpreter`.
     * **SW-SR-15.** Seven values still print raw. Wrap each in
       `encode_display(str(...))`:
       * `base` and `path` in `_assert_within`;
       * `dst` in `_heal_skill_symlink`;
       * `self.path` in `_reclaim_or_refuse`;
       * `sys.executable` in the stale message;
       * the exception text in `_surface_intents`, `_prune_intents` and
         `_run_evolution_infer`.
3. **The review-stance-and-lenses plan** (`plans/review-stance-and-lenses.md`).
   * **State:** its code review is at `62002427`, verdict REVISE, findings
     RS-CR1 to RS-CR8. The review found the work does what the plan said. The
     author was revising:
     * pin the remaining rule sentences now, because three test files freeze
       at the cut;
     * fold about 1,400 test nodes into one per property, as the suite budget
       requires;
     * RS-CR8 may need a wider Maintainer allowance for `check_cairn` flags on
       archived proposals. If it does, put it to him as a plain question with
       a recommended answer.
     **At the pause nothing was edited:** the plan has no Response section
     yet. The reviser had worked out the following, which saves the next
     session the reading:
     * **RS-CR1.** Every sentence to pin belongs in the stance test's
       `_STANCE_OBLIGATIONS` and `_COMMON_TEMPLATE_LABELS`. Three need
       special handling:
       * "Plan review never has a second round" sits in AGENTS.md's
         lifecycle section, not in `## Review`, so it needs a check that is
         not scoped to the Review section;
       * the `**Obligation**:` line in the plan skeleton needs a node of its
         own;
       * "only by being one" extends the existing called-read pattern.
     * **RS-CR6.** Delete the 259 `test_removing_*` nodes that strip the
       pattern under test, since they cannot fail. Keep the 5 that can. Fold
       the 1,143 `test_inserting_*` nodes into 6, one per pattern set. Add one
       node checking that every pattern fails on an empty text.
       `test_review_and_verification_rules_ship.py` has the same flaw in 52
       nodes, so fold those too.
     * **RS-CR8.** The reviser never ran `check_cairn.py`, so confirm the
       count first. If it is six, put this to the Maintainer:

       > *Draft question.* Plan C7 allowed three "stale line citation" flags
       > in archived proposals. Deleting the old test file added three more,
       > citing lines in a file that no longer exists, and archives are never
       > edited. Should the plan record all six as expected and permanent?
       > Recommended: yes, the same kind of flag.
     * **No lockfile or frozen-file obstacle** for these edits.
   * **Next:** finish the revision, set `ready-to-archive`, then archive. The
     archive records the final blob ids and node counts in the re-anchor row.
   * **Collision.** RS-CR4 rewrites the roster sentence in AGENTS.md ("it adds
     no read and upgrades none") and the "standing floor" wording beside it.
     The collaboration-agreement removal plan (item 5) edits the same
     sentence in seven copies, and its stance-test pin. Whichever lands second
     builds on the first, so tell that plan's author.
   * **Downstream:** the collaboration-agreement removal starts only when this
     plan archives.
4. **Board-as-basis** (`plans/board-as-basis.md`).
   * **State:** built by the Maintainer's other agent tool, at
     `awaiting-code-review` (`4f08957d`). The Maintainer has a prompt for a
     fresh session of that tool to do the code review.
   * **At archive:** the author adds a note correcting the stale path to plan
     D at `dev/plans/board-as-basis.md:1201`. That line is inside a review
     section, so the correction is a note, not an edit.
5. **Removing the collaboration agreement**
   (`proposals/2026-10-19-claude-remove-collaboration-agreement.md`, accepted
   `90715acb`).
   * **State:** its plan was opened by the other agent tool at `013ae148`, as
     `plans/remove-collaboration-agreement.md`. At the pause its plan review
     was under way: the working copy said `revising-plan`, uncommitted.
   * **Gate:** implementation waits for item 3 to archive, and must land
     before model-mapping's chunk C2.
6. **Model-mapping-install-path** (`plans/model-mapping-install-path.md`).
   * **State:** the other agent tool started it. Status is `implementing`,
     and C1 is at `6dcbdda7`.
   * **Gate:** its chunk C2 waits for item 5 to land.

## Bookkeeping owed in `dev/PLANNING.md`

This is the coordinator's job, at the next serialization point. It goes in
the queued row "Re-anchor the gate manifest", as one **Joined** paragraph per
repair, each quoting its authorization. **Derive every figure from the
commits; these are names, not counts.**

* **Certifying-run doctrine** (`12be58d9`):
  * frozen `bootstrap/tests/conftest.py` changed;
  * the new `bootstrap/tests/test_certifying_run_rule.py` freezes at the
    ceremony.
* **Engine copy-fallback repair** (`cf707e2a`, `80c54552`):
  * no existing frozen file changed;
  * the new `bootstrap/tests/test_engine_copy_fallback_contained.py` freezes
    at the ceremony;
  * AST CHANGED: `_emit_skill_copy_fallback` and `_symlinks_available` in
    `install.py`, and `format_forked_facade_warning` in `lockfile.py`.
* **Session-binding repair** (`7e6a14e5` through its answer):
  * frozen `templates/modules/default-on/prune_reflections.py` changed;
  * the new `bootstrap/tests/test_session_writes_contained.py` and
    `bootstrap/tests/test_session_binding_untracked.py` freeze at the
    ceremony;
  * no engine symbols.
* **Upgrade lockfile-path repair** (`d299f37c` through its answer):
  * the new `bootstrap/tests/test_upgrade_lockfile_path_containment.py`
    freezes at the ceremony;
  * AST CHANGED: `_apply_upgrade`, `_theirs_bytes`, `_theirs_text` and
    `cmd_upgrade`;
  * AST NEW: `_lockfile_refusal`, `_contained_lockfile_path`,
    `_check_lockfile_paths` and `_assert_stage_has_no_links`;
  * the answer, as planned, would also change `_self_heal_profile_config`,
    `_cmd_finalize_lockfile`, `_behind_by_n` and `_resolve_vendor_wrapper`,
    change `_apply_upgrade`, `cmd_upgrade` and three of the new functions
    again, and add `_check_staged_names`. Derive the final set from the
    commits.

New roadmap rows owed:

* **Move the interpreter binding into `.git`.** A proposal after 0.4; this is
  SW-SR-10's deferred half.
* **A broken link in every install.** The link to `content_scan.py` at
  `templates/modules/team-gated/security-review.md:181` resolves only inside
  `templates/`. Installed at `dev/modules/security-review.md` it points
  nowhere. It is a small, adopter-facing fix.
* **Stale citations in the stewardship proposal** (#30). Two citations are
  stale: `scripts/quality_gate.py:498`, and the module lines 58-60 cited at
  line 689. Correct both with an appended note when the #30 plan opens.

## At the 0.4 cut (Maintainer)

1. A certifying run.
2. The combined AST correction, **then** the gate-manifest re-anchor, in the
   order the re-anchor row gives.
3. A certifying run.
4. A full-history secret scan and a read of what the history exposes.
5. The 7 release sweeps.
6. A README note that no outside project has run the install yet.
7. Make the repository public, sign the tag `v0.4.0`, run a cold bootstrap,
   then deposit on Zenodo.
8. After the push, close issues #2 and #8 on GitHub; plan C delivered both.

## Notes for whoever coordinates next

* **Every subagent in one session shares one work-intent agent id.** One
  agent's commit releases the others' claims, so check `git diff` before
  every commit. (Roadmap row: "Work-intent claims".)
* **Heavy test runs should take turns.** An earlier run overloaded the
  machine.
* **A review of a long plan is expensive.** The review-stance plan reached
  4,690 lines and its code review was costly. Tight review briefs help:
  acceptance criteria plus the verification record, not the whole history.
