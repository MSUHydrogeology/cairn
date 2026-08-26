# Next session

*Rewritten from scratch at the 2026-08-26 pause. Read `python tools/board.py`
first — it is derived and current; this file is a hand-written orientation and
may already be stale.*

## Where the project stands

**The subtraction sweep is most of the way done.** C1 through C7's first half
have landed: **58,985 deletions against 6,865 insertions** across 167 files.
Everything below is either yours or the prose phase.

The suite is green apart from one standing fence and one pre-existing finding.

## Start here

1. **The AST baseline is the one thing genuinely waiting on you.** 13+ symbols
   changed. Self-service repair reaches only four allowlisted symbols and only
   when the target is the *sole* changed symbol, so it refuses here — the
   runbook (`bootstrap/AST_BASELINE_RUNBOOK.md`) calls this a Maintainer-run,
   dry-run-verified direct correction. Derive the CHANGED set against the
   committed baseline rather than carrying a figure forward from this file.

2. **The gate manifest is DONE** — re-anchored on your authorization, 209 → 178
   rows, verified by set equality. `verify` returns OK. Nothing owed.

3. **Onboarding is prepared but not executed.** The whole edit was validated in
   a throwaway worktree and the findings are in
   `dev/plans/subtraction-sweep.md` > "C6 onboarding". Two things there are
   decisions, not chores: `assert_always_on_complete` loses its subject, and
   the side-door parity property loses its category. Both are yours.

4. **C7's second half is the PLANNING bankruptcy** — 2,591 lines, 127 tagged
   rows, 86 in a 1,010-line security-cluster block at `:1509`. You ruled that
   the sweep supersedes `2026-08-04-claude-board-retro-disposition` on this
   row. A concurrent Strategy session gave the security-cluster block a named
   destination: fold surviving material into
   `dev/strategy/2026-08-05-codex-security-strategy.md`'s cluster map, PLANNING
   keeping pointers only. **This is the next substantive work and needs nothing
   from you.**

5. **75 unpushed commits.** Pushing is yours, always.

## What is left after that

C8 (install-contract ceremony) and C9 (both sister migrations) are
MAINTAINER-gated end to end. The sweep's Cairn-side work finishes at C7.

## What this session learned that is worth not relearning

**I ran one gate diligently and never ran the others.** `claim_check` on every
prose edit, file by file — and never `check_cairn`, which runs claim_check over
the *whole tree* plus the link and loop-fidelity checks. It went 11 issues → 93
before I noticed, and I only noticed by accident while mapping something else.
Prose work runs *all* its applicable gates.

**A guard naming more than its tests need turns an unrelated deletion into
invisible coverage loss.** Measured three times: 30 tests in
`test_lifecycle_vocabulary.py` switched off by the transition-lint removal and
recorded as verified; 37 in `test_upgrade_module_additions.py` switched off by
the metrics removal, one of them a path-traversal containment test that had
stopped attempting the traversal; 3 more in the repointed session suites.

**Reconcile skips, not just passes.** A passed→skipped transition leaves the
collected total unchanged, so a reconciliation watching passes is blind to
exactly the failure it exists to catch.

**A manifest cannot be verified against the list it summarises.** The sweep's
own inventory was checked by `wc -l` over its own file list: the sum was right
and the set was wrong, in both directions.

**Parse before writing.** Two files were left syntactically broken on disk
because a span-removal script wrote first and validated after.

## Open threads

* `2026-08-20-claude-adopter-path-consolidation` — `awaiting-review`, untouched
  all session.
* `portable-sweeps-cannot-run` and `scanner-claim-scope` — accepted, terminal,
  no plans.
* Issue #18 (`lhm` foldback #59) carries an **unsigned export affirmation** —
  yours to sign; an agent drafted it but cannot attest it.
* `dev/measurement/collision_log.md` is untracked and unclaimed; it predates
  this session.
* `templates/skills/_lib/` is outside the gate's frozen globs, so the session
  kernel — a declared executable trust root — is not fingerprinted by the
  differential gate. Pre-existing, not caused by the sweep, flagged for C8.
