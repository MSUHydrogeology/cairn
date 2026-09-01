# Next session

*Rewritten from scratch 2026-09-01. Run `python tools/board.py` first — it is
derived and current; this file is hand-written orientation and may already be
stale. **Check its claims before repeating them.** A stale line in this file
was repeated four times in one session before anyone opened the repository it
described.*

## Where the project stands

**Review doctrine changed today** (`d98b4c1`), and it is the session's main
output. A tier is a **stance**, not a staffing class. **No tier requires a
different agent type** — External and Security Review included. **One loop**:
the author's revision carries the status, no clearing round except a Security
Review, and a second round needs a reason recorded on the artifact. A reviewer
**reasons** rather than re-runs. Prose-only work does not run the suite. Read
`doctrine/dual-review.md` before running any review; several habits it retires
were load-bearing yesterday.

**Both 2026-08-20 plans are archived**, and adopter issues #4, #5 and #6 are
closed — twelve days after filing, which is the number the nimbleness note
exists to bring down.

**The tree is green.** No failing tests. `check_cairn` OK across 172 files;
neutrality `fail=77`; `verify_integrity` at its long-standing baseline of 21.

**60 commits are unpushed.** Pushing is the Maintainer's, always.

## What is genuinely next

* **`2026-08-20-claude-adopter-path-consolidation`** — `revising`, nine
  blocking findings. Two are worth knowing before opening it: the proposal
  claims "the gate manifest is unchanged" and **seven frozen files change**;
  and `[R5]` is a live shipped defect independent of the proposal. The Internal
  review recommends **splitting** it — documentation consolidation is low-risk,
  the executable half is not. That call is the Maintainer's and it changes what
  a reviewer should read.
* **The `repin` tool** — designed in
  `strategy/2026-08-28-claude-repin-revitalization.md`. Its route is now
  lighter: the External round is recommended, not required, so it does not wait
  on a second agent type.
* **The deferred gate re-anchor** — 10 frozen files, on the `## Queued` board
  in `PLANNING.md` with the authorization quoted. **Maintainer-only and
  supervised**; an implementing agent must not perform it.
* **Three deposits still open** from the earlier authorized batch: `[TRU-4]`'s
  known-new graduation, the two onboarding findings behind the
  MAINTAINER-GATED `_ALWAYS_ON_MAPPINGS` fence, and the four unfiled issue
  drafts in `dev/measurement/queued-issue-drafts.md`.

## Things that are true and will look wrong

* **A green suite is not evidence the gate manifest is current.**
  `test_gate_manifest.py` verifies a freshly produced manifest and never diffs
  the committed fixture. Ten frozen files are stale right now, deliberately.
  Nothing will go red to remind you.
* **`quality_gate --sub neutrality` reports `fail=77`.** Long-standing, and
  two lower than yesterday only because a vendor-heavy passage was cut.
* **Archiving improves the gate counts without fixing anything.** Archived
  files leave the default scans. When two proposals archived today,
  `check_cairn` went 6 → 0 while nine relative links silently broke; only
  `link_check --include-archives` could see them. Read a count that improves at
  an archive as *content left the measurement*.

## Worth not relearning

**A rule outlives its reason, and then gets re-argued for months.** Six
instances surfaced in one session. Five were the same shape — the roster's
purpose overwritten by a staffing floor, the `revising-plan →
ready-to-implement` edge, `Closes on`, the C0 risk posture, and a stale fact in
this file. When landing a rule, land why it exists in the same commit.

**The sixth was worse, and different.** The `defer`-deposit rule was present
*with* its reason, in the paragraph being written — and the half that reads as
ceremony (quoting the authorization) got performed while the half that does
something (the deposit) did not. Sentence structure defeated it. Both are now
separate imperatives in the plan template.

**Confirm the instrument on a representative case.** A grep proving it can
match somewhere proves nothing about the shape you are hunting: a line-based
sweep for `clearing review` could never match it wrapped across a newline, and
the control passed on files where it happened not to wrap.

**Do not take a subagent's contradiction at face value.** One arrived with a
commit SHA and a mechanism, and was wrong. The control is what settled it.

**Name the prohibited act, not the category.** A subagent told "read-only"
committed to `master` to simulate a commit; it did not classify a commit as a
file edit.

**Exhaustiveness is not rigour.** Most of a productive day was spent building
verification apparatus around doctrine that should have made it unnecessary.
The bound has to hold against an agent incentivized toward thoroughness, or it
is not a bound.
