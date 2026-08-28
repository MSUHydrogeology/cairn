# Next session

*Rewritten from scratch 2026-08-28, before a context compaction. Run
`python tools/board.py` first — it is derived and current; this file is
hand-written orientation and may already be stale.*

## Where the project stands

**The subtraction sweep's agent-side work is done.** C1–C7 landed; four
Internal code reviews ran and were answered. `dev/PLANNING.md` went **2,591 →
869**. Cairn's security debt now lives in one place: the **Live residual
register** in `dev/strategy/2026-08-05-codex-security-strategy.md`.

**Everything through the re-anchor is pushed.** The 2026-08-28 ceremony
published `master` and `refs/cairn/gate-anchor` together; before that, nothing
had ever been pushed. Pushing is still the Maintainer's, always -- that did not
become routine because it happened once.

## One thing is STOPPED, and it is stopped correctly

**The gate anchor is DONE, not stopped.** It moved `5f99273 -> bd66a70` on
2026-08-28, signed and verified, both refs pushed. It had been 362 commits
stale. The Maintainer blessed the outstanding re-review; what had actually
blocked it was arithmetic, not judgement -- the launcher on the host was the
pre-fix vulnerable one *and* was bound to a `reanchor.sh` that no longer
existed. Full record in the sweep plan, `## C8 complete`.

**Run it with `scripts/reanchor_ceremony.py`.** Without `--run` it reports and
stops: the closure printed three ways, the packet/launcher pair checked, and
the ceremony's read-only checks run *before* a key or a package is spent. With
`--run` it performs both stages and asks exactly two questions. It never
pushes.

**One finding this left open.** `bootstrap/reanchor-launcher.template.sh` is
not a closure member, so the pre-candidate trust root is pinned by nothing.
Everything the launcher does runs before the checker exists. Making it the
eleventh member is unclosed work and predates the sweep.

## The one thing that is still stopped

**`scripts/correct_pinned_digests.py` refuses on entry.**

A Codex External Security Review returned **BLOCK** — seven findings, two
CRITICAL, each reproduced. The headline: the plan digest binds only the plan's
*projection*, not the complete preimage or output. Two materially different
trees produced **identical digests**, and apply wrote the unauthorized values.
The review's final section is a redesign, not a patch. Corrections go back to
being done by hand under their runbooks until someone commissions it.

## What is genuinely next

* **C9 IS COMPLETE.** *(2026-08-28. Maintainer chose "do C9 now, then archive"
  and authorized the five-item `defer` batch as one batch.)* Both sisters
  migrated, green, and committed to branch **`cairn-0.3.0-migration`** in each;
  **both `master` branches are untouched**.

  | repo | result | baseline |
  |---|---|---|
  | `modflow_tools` | 3472 passed, 0 failed | — |
  | `lhm` | 1223 passed, 9 skipped, 0 failed | master had 1 failed |

  `verify_integrity` OK on both. `lhm` was the harder one: a 0.2.0 -> 0.3.0
  jump across 1789 commits, 17 conflict hunks in 8 files.

  **Three things the next migration must not rediscover:**

  * **`upgrade --apply` deletes nothing.** `removed-upstream` is not in
    `_ADVANCING_KINDS` and the apply path has no `unlink`. It *reports* what
    upstream dropped; removing it is the adopter's, by hand. Same for
    `slot-removed`, which is why those files are never staged.
  * **[TRU-1] cost a third and fourth ceremony.** Both sisters kept lockfile
    records for files the migration removed, and `--finalize` refuses on a
    missing record. Still no regenerate command. Resolved by a prune that
    drops a record **only when its file AND its upstream `src` are both
    gone**, never rewriting a hash.
  * **Adopter files can hold a routine that cannot run.** `lhm`'s
    `dev/rules/custom_session_routines.md` had a live goodnight step
    requiring a deleted script and a deleted ledger. It is not
    lockfile-tracked, so no upgrade classification would ever have surfaced
    it. Grep the adopter's own rule files, not just the tracked set.

* **The upgrade engine's phantom-fork defect is FIXED** (`3a99590`), and the
  AST re-anchor it needs is the Maintainer's — see *Open threads*.

* **A real gap the sweep left: Cairn still ships 24 references to the removed
  machinery across 11 template files** (`core/dev/{measurement,upstream}/README.md`,
  `modules/README.md`, `modules/default-on/{incident-trackers.md,claim_check.py,
  _onboarding/triggers.py}`, `modules/team-gated/{doc-drift-prevention.md,
  _intent/conflict.py}`, all three `onboarding/*.md`). **Every new adopter
  installs prose describing tooling that does not exist**, and both sisters
  inherited these *through* the upgrade, because a file classified `clean`
  correctly takes upstream's version. Fixing an adopter's copy without fixing
  the template is futile — the next upgrade restores it. C7's prose phase
  stopped at Cairn's own `dev/` tree.

* **C9's original framing.** Unblocked on every count: code review ran
  and was answered, the lockfile is correct, and the anchor the sisters would
  inherit is current rather than 362 commits stale. Still MAINTAINER-GATED per
  sister.
* **C8 is complete.** Nothing remains in it.
* **The four unfiled issue drafts** in `dev/measurement/queued-issue-drafts.md`
  — drafted, verified, never filed. Filing is outward-facing.
* **The `defer` batch** in the sweep plan's Dispositions block — five deposits
  awaiting one Maintainer authorization, presented as a batch.

## What this session learned that is worth not relearning

**A diff review cannot find a pre-existing defect.** The authority-closure
review was scoped to what changed since the anchor, so it structurally could not
see the injection that predated it. Scoping a security review to a diff is a
briefing decision with a blind spot; say which you want.

**A guard that passes is not a guard that works.** Three times this session a
control was written, run, and found to be vacuous — a summary that reported
"docstring-only" having determined nothing; a probe aimed at the wrong twin so
the suite stayed green; a test modelling `PATH` when the channel was an exported
variable. Every one was caught by deliberately breaking the thing and checking
the test noticed. **Do that every time.**

**Numbers shrink when you look at them.** A loop-fidelity count went 128 → 99 →
smaller; a lockfile "19 stale records" was really 3 of one kind and 19 of
another. A figure that moves under inspection was standing in for a judgment
nobody made.

**Do not commit into a running review's scope.** `HEAD` moved five times during
one review and one of those commits edited a file it was reading. The same
applies to a *ceremony*: it refuses any dirty tracked file, so when two sessions
share a worktree, agree an explicit hold window before starting one. **And to a
verification run.** A full suite that was in flight while `dev/` docs were being
rewritten returned 2 failures; the same commit on a quiet tree returned 0. The
failures were real observations of a tree mid-edit, not a regression -- but a
figure produced that way is worthless in both directions, and reporting the
earlier clean run while a dirtier one was still going compounded it. Quiesce
the tree, then measure.

**Measure over what is DECLARED, not over what is PRESENT.** This error was made
twice in one day, in unrelated code: a lockfile scan that skipped records whose
file was missing and reported the intersection as the whole, and a packet check
that compared only the rows the packet happened to contain -- so a packet with
*zero* member rows would have read as matching. Both look correct while
iterating over what you have. The fix is to iterate over the declared set and
let a missing entry be visible as missing.

**A security review's findings are a specification, not an argument for
retreat.** An adversarial review of a convenience tool returned 28 confirmed
findings, and the first response was to delete the half they landed in. The
Maintainer pushed back, and they were right: only one of six root causes
genuinely resisted automation, and even it had an honest form. Retreat *feels*
like rigour and cannot be shown wrong, because the deleted version is never
built -- the same asymmetry `AGENTS.md` names for reviewers narrowing scope.
Fix what the findings describe; withdraw only what cannot be made honest.

## Open threads

* `2026-08-20-claude-adopter-path-consolidation` — `awaiting-review`, untouched.
* Four `line-bounds` flags in `2026-08-20-claude-scanner-claim-scope.md` are a
  **known, dated non-pass**: the lockfile shrank and that proposal is
  append-only, so its citations were corrected by appending, not editing.
* `dev/measurement/collision_log.md` is untracked and predates all of this.
* **The AST baseline is stale, and the re-anchor is the Maintainer's**
  *(dated 2026-08-28)*. `3a99590` changed `_apply_upgrade`, which is baselined
  but **not** in `_ast_attest._UPDATE_ALLOWLIST`, so `update-symbol` refuses it
  and the runbook makes it a Maintainer-run direct correction. Derived against
  the committed baseline, not carried forward:

  ```
  CHANGED 1   MISSING 0   DUPLICATE 0
    FunctionDef:_apply_upgrade   65a5f59ef844cfb9 -> dc53397782e91c18
  ```

  Until it runs, `test_ast_attest.py` has exactly 2 failures. **Full suite:
  3178 passed, 1 skipped, 2 failed** — those two and nothing else.

  Also open on that commit: AGENTS.md makes the scaffold engine a proposal +
  Security-Review trigger. The change is a bounded correctness fix restoring
  intent the code already states at `upgrade.py:1561`, but whether it routes
  through a proposal is the Maintainer's call, not the author's.
* **`_gate_manifest.py verify` reports HOLD, and that is correct** *(dated
  2026-08-28)*. Two violations, both `scripts/reanchor_ceremony.py`:
  FROZEN-MODIFIED and FROZEN-OID. The 2026-08-28 ceremony re-froze the manifest
  at tree `0353b32`; the `ssh-add` fix landed after it. `scripts/*.py` is a
  gate-frozen glob, so **any** edit there HOLDs the manifest until the next
  re-anchor. **Do not regenerate the fixture to clear it.** An actor that edits
  a gate-control file and then re-freezes it is the exact attack the manifest
  exists to detect, and the tool's own docstring says so. It clears at the next
  ceremony.

  Two things worth knowing about this state. First, **the suite stays green
  while it holds** -- `test_gate_manifest.py` self-verifies a freshly produced
  manifest and never diffs the committed fixture, so nothing reddens; it was
  found by running `verify` directly, not by testing. Second, the ceremony's own
  preflight reads CLEAR, because `check` re-derives the manifest from raw commit
  objects rather than diffing the fixture. The two disagree by design and answer
  different questions.

  This is also a real cost worth naming: between ceremonies, editing any file
  under `bootstrap/tests/**` or `scripts/*.py` leaves the repository in HOLD.
  That is an argument for the re-anchor cadence the repin strategy proposes,
  not an argument for looser freezing.
