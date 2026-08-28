# Next session

*Rewritten from scratch 2026-08-28, before a context compaction. Run
`python tools/board.py` first — it is derived and current; this file is
hand-written orientation and may already be stale.*

## Where the project stands

**The subtraction sweep's agent-side work is done.** C1–C7 landed; four
Internal code reviews ran and were answered. `dev/PLANNING.md` went **2,591 →
869**. Cairn's security debt now lives in one place: the **Live residual
register** in `dev/strategy/2026-08-05-codex-security-strategy.md`.

**109 commits are unpushed.** Nothing has been pushed at any point. Pushing is
the Maintainer's, always.

## Two things are STOPPED, and both are stopped correctly

**1. The gate-anchor ceremony. Do not run it.**

An External Security Review of the launcher template found — and this session
independently reproduced — an **environment-injection path into the ceremony's
own values reader**. Neither reader initialised its outputs, and the schema
check asks *"is this variable set"*, which an exported environment variable
answers exactly as a values-file line does:

```
clean environment          ->  REFUSE: missing required key 'python'
V_python=/bin/echo in env  ->  OK: the values file satisfies the schema
```

`$V_python` is what executes the gate checker. Worse, the disclosure print then
showed the injected value beneath *"nothing below was discovered"* — the
operator's one moment of real oversight, handed a false statement.

Fixed at `4bb6bb4` with an `unset` in each reader plus a regression test that
**fails against the unfixed reader** (control-run). **But editing `reanchor.sh`
voided the authority-closure clearance** recorded at `57ba93a`. The three
closure files must be re-reviewed before any ceremony.

Also unresolved from that review: the **instantiated launcher is bound to the
reviewed template by nothing** — not the closure, not the frozen set, not the
packet. And the launcher performs 9 of the registry's 19 steps, including every
step that decides whether candidate code starts.

**2. `scripts/correct_pinned_digests.py`. It refuses on entry.**

A Codex External Security Review returned **BLOCK** — seven findings, two
CRITICAL, each reproduced. The headline: the plan digest binds only the plan's
*projection*, not the complete preimage or output. Two materially different
trees produced **identical digests**, and apply wrote the unauthorized values.
The review's final section is a redesign, not a patch. Corrections go back to
being done by hand under their runbooks until someone commissions it.

## What is genuinely next

* **C9 — the sister migrations.** Unblocked in principle: the Maintainer ruled
  C9 follows code review, and code review has run and been answered. The
  lockfile the sisters would inherit is now correct.
* **C8's remainder** — only the gate anchor, which is stopped above.
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
one review and one of those commits edited a file it was reading.

## Open threads

* `2026-08-20-claude-adopter-path-consolidation` — `awaiting-review`, untouched.
* Four `line-bounds` flags in `2026-08-20-claude-scanner-claim-scope.md` are a
  **known, dated non-pass**: the lockfile shrank and that proposal is
  append-only, so its citations were corrected by appending, not editing.
* `dev/measurement/collision_log.md` is untracked and predates all of this.
