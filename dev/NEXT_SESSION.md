# Next session

*Rewritten from scratch at the 2026-08-25 goodnight. Read
`python tools/lifecycle_planner.py board --compact` first — it is derived and
current; this file is a hand-written orientation and may already be stale.*

## Where the project stands

**Do not take a lifecycle tool's blessing as the reason to do something.** The
checkers, the board, the transition gates — these are on the removal list. They
are advisory and they are dying. A question like *"does this need another
review?"* is answered by judgement about the work, not by whether a gate reads
`[ok]`. This note was itself written once with a re-review step in it that
nothing required.

**Cairn spent this session removing its own process, and the removal is now the
work.** The Maintainer's judgement, given repeatedly and plainly, was that the
apparatus had become the bottleneck: *"This isn't nuclear launch software here,
shipping a bug is okay"* and *"they are too onerous and will ALWAYS be
circumvented."* Four things landed on that basis — the metrics module stopped
doing enforcement, event blocks were retired, `convergent-lifecycle` +
`retire-external-plan-review` shipped together, and the subtraction sweep now
has a reviewed plan.

**Two plans are live.** `adopt-into-existing-tree` is implemented and awaits
code review. `subtraction-sweep` has been through two blocking reviews and one
revision, and awaits re-review.

## Start here

1. **Two Maintainer-run ceremonies, both derived and neither performed.** These
   gate nothing else today, but they are stale until done:
   * **AST baseline** — 4 CHANGED symbols from `adopt-into-existing-tree`:
     `_cmd_adopt_module`, `_compute_upgrade`, `_superseded_surface_note`,
     `cmd_upgrade`. Digests are in that plan's `## Implementation verification`.
     None is in `_UPDATE_ALLOWLIST`, so this is the dry-run-verified direct
     correction, per `bootstrap/AST_BASELINE_RUNBOOK.md`.
   * **Gate manifest** — `bootstrap/tests/test_upgrade.py` and
     `test_profile_grammar.py` now differ from their recorded sha256.
     **This never shows up as a test failure**: `test_gate_manifest.py` only
     self-verifies a freshly-produced manifest and never diffs the committed
     fixture. Do not read a green suite as "no re-anchor needed."
2. **`subtraction-sweep` — start C1. No re-review.** Both passes blocked, the
   revision answers all seven findings, and that is the end of it. Do not send
   it round again because a status field or a checker suggests it: the plan is
   answered, deletion is recoverable, and the sweep is *dismantling* the
   machinery that would ask. If a tool's gate disagrees, the tool is wrong —
   it is on the removal list for exactly this reason.
3. **`adopt-into-existing-tree` code review.** Floor is a same-type agent in an
   independent context, not the implementing agent.
4. **35 unpushed commits.** Pushing is the Maintainer's, always.

## The sweep, in one place

Nine chunks, `awaiting-plan-review`. **C1 is the load-bearing one and must land
before C6** — it extracts a ~700-line-per-side *session kernel* from
`tools/session.py`: the interpreter trust root, `_warn_stale_once`,
`_heal_skills_fanout`, and both session commands. C6 deletes that file, and the
kept `session-start` / `session-end` SKILL.md files invoke it **by name**.

Net removal is **~51,000**, not the 61,000 headline — the estimates were wrong
on every row, the order-4/order-5 boundary double-counts ~4,300 lines, and the
surviving kernel plus ~1,500 lines of repointed tests are not removals at all.

Three build-table rows are **struck** because they name nothing in the tree
("slot ratchet", "attic notes"), or were never addressed by the accepted design
(`link-check-allow`, folded in with its own falsifiers). Each carries the
condition that revives it.

## What this session learned that is worth not relearning

**A membership claim cannot be verified against the list under test.** The sweep
manifest was checked by `wc -l` over its own file list: the sum was right and
the set was wrong — one file marked for deletion tests a module the sweep keeps,
and six coupled files were missing. This is the identical self-comparing-oracle
defect measured on the security manifest three days earlier, reproduced by
someone who knew about it. **For membership, the instrument must be something
other than the list.**

**A `skipif` guard hides the deletion it was written to survive.** The tests
covering the session kernel load `lifecycle.py` behind `pytest.mark.skipif`, so
deleting the file makes them *skip, not fail*. A falling-test-count check reads
a skip as neither pass nor failure. Any deletion sweep needs its repointed tests
shown **failing** against a tree without the target before they count.

**A passing test is not evidence that a ceremony is unnecessary.** Both
re-anchor fences were predicted wrong this session — first too few symbols, then
"no gate re-anchor needed" on the strength of a green gate suite that never
checks the property. Check what the test actually compares.

**`--root` defaults are not repo roots.** Two false regressions were nearly
recorded here from running a *template* copy of a tool from the wrong directory.
Both times the correct evidence already existed in the goodnight run's own
output.

## Open threads

* `2026-08-20-claude-adopter-path-consolidation` — `awaiting-review`, untouched
  this session.
* `portable-sweeps-cannot-run` and `scanner-claim-scope` — accepted, terminal,
  no plans yet.
* `dev/measurement/collision_log.md` is untracked and unclaimed; it predates
  this session and no intent covers it.
* Fold-back: both sisters' ledgers are drained (backlog reads 0). `lhm` #59 went
  upstream as issue #18 with its **export affirmation deliberately unsigned** —
  that signature is the Maintainer's and is still outstanding.
