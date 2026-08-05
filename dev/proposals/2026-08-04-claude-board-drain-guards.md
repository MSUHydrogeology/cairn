# Drain the board the way the vocabulary intended — write the guards

**Author**: Claude (Strategy)
**Model**: claude-opus-5
**Date opened**: 2026-08-04
**Status**: proposed
**Touches**: `bootstrap/tests/test_security_lint.py`, `bootstrap/tests/conftest.py`, `dev/PLANNING.md` > "Deferred follow-ups"
**Related**: corrects the scope error in `2026-08-04-claude-board-retro-disposition` (archived); executes the `guard` token introduced by `2026-08-04-claude-deferral-discipline` (archived)
**Plan review**: required(Internal) — writes assertions into an already-`FROZEN-MODIFIED` gate file

## Context

Two artifacts landed on 2026-08-04. The first introduced the **`guard`**
disposition: a deferred follow-up is homed in *something that executes* — a test
node, an assertion — because a follow-up whose revival condition is mechanical
belongs where that condition fires, not on a board that fires only when a human
re-reads it.

The second proposed to adjudicate the board's 58 rows and was **withdrawn at
Internal review** on finding [I3]: a pass editing only `dev/PLANNING.md` cannot
express `accept` or `guard`, since both require touching the thing the row is
*about*, so it could reach only `wontfix`/`defer` and would lengthen the section.

**[I3] was correct and the response to it was wrong.** It constrains the
*method* — do not do a board-only pass — and says nothing about the *goal*. The
withdrawal treated a scope defect as a verdict on the objective, and so declined
to use the tool the first artifact had just built. The counter-evidence was
inside the review that produced the withdrawal: the code review's [C4] quoted
the board's own SC3 and SC5 rows saying *"the guard is one assertion and should
be written rather than re-deferred"* — and that text was copied into the board
as an argument about sampling without anyone noticing it was an argument against
the withdrawal.

Maintainer direction, 2026-08-04: *"do the focused, targeted job that actually
has a chance of success instead of deferring the goal because of the narrowest
framing."*

## Proposal

A **bounded** pass in two classes. Not a re-adjudication of 58 rows.

### Class A — write the guards

Rows whose **own text names the remedy as one or two assertions**. Each becomes
a `guard` disposition naming its node, and leaves the board.

| Row | The assertion its own text specifies | Home |
|---|---|---|
| **SC3** — `scan_targets()` union is unguarded | one assertion: the enumeration is a **union** with the manifest, not a replacement | `bootstrap/tests/test_security_lint.py` |
| **SC5** — Bandit `ALLOWLIST` has no staleness guard | two assertions: key still on disk; key still produced by a live finding | same file |
| **G6** — nothing enforces the suite's `0 skipped` invariant | one assertion at session end | `bootstrap/tests/conftest.py` |

**The frozen-file question resolves favourably and is the reason to act now.**
`bootstrap/tests/test_security_lint.py` is **already** `FROZEN-MODIFIED`
(verified 2026-08-04), and its re-pin is already scheduled by SC4's Maintainer
disposition *"fold in"* at the next supervised ceremony. Adding assertions now
joins a delta that is already going to be re-pinned — which is exactly SC5's
stated trigger, *"the next change to `bootstrap/tests/test_security_lint.py`"*.
`conftest.py` is not frozen.

### Class B — assess the imported half

The ~31 rows imported from another repository are **unassessed** — 29 of 58 rows
carry no revival condition and the shortfall concentrates there. Read them and
record, per row, whether its stated condition is **already satisfied**. A row
that is already satisfied is `accept` (the work happened) and leaves the board.

**No target count.** The deliverable is the assessment; how many close is its
output, not its promise. This is the discipline the parent's withdrawn "12 of
the 59" failed.

### Explicitly not in scope

* **Rows requiring new design** — Conda advisory coverage, the install-integrity
  trust anchor, the launch sequence. These are real work, not board clutter.
* **`wontfix` on anything.** This pass closes rows by *doing the thing*, not by
  declining it. If a row deserves declining, that is a different pass with a
  different argument.
* **G3 / G4** (`_yaml_load` self-oracle; `SKIP-XFAIL-NEW` over-report) — both
  live in `test_presets.py` / the gate manifest and their own triggers name a
  supervised ceremony. Assessed in Class B, not written here.

### Documentation / doctrine surface

**None.** No rule changes. This executes an accepted vocabulary against existing
rows.

### Doctrine-change rate-limit

**N/A** — no doctrine change.

## Rationale

**Why this and not the withdrawn pass?** Because it can actually reach `accept`
and `guard`. Class A converts three board rows into executing assertions — the
`guard` token's entire purpose, used for the first time. Class B replaces an
unassessed half with an assessed one.

**Why now?** The frozen re-pin is already scheduled; SC5's own trigger is *"the
next change to this file"*, and this is that change. Deferring means the next
toucher inherits it again.

**What makes this bounded?** Three assertions and one read. If Class A grows
past a handful of assertions, that is the signal to stop and re-scope, not to
push through.

## Alternatives considered

* **Do nothing** (what the withdrawn proposal effectively chose). Rejected: it
  declines the tool the parent built, and the board's own rows say the guards
  should be written.
* **Adjudicate all 58 with code access.** Rejected as the huge-branching-job the
  Maintainer explicitly excluded, and it reproduces the load problem.
* **Write the guards but skip Class B.** Tempting and nearly right; rejected
  because the unassessed half is the honest gap [C4] surfaced, and reading ~31
  short rows is cheap.

## Evidence / verification plan

* **Tests** — the three new assertions are themselves the deliverable, and each
  must be **mutation-proven**: break the property, confirm the assertion fails,
  restore. An assertion that passes both ways is worse than no assertion.
* **Examples / smoke checks** — `python -m pytest bootstrap/tests` (full suite,
  canonical Python 3.13.x); `python scripts/check_cairn.py`;
  `python scripts/claim_check.py dev/PLANNING.md`.
* **Docs** — no doc changes; board rows leave with `guard` / `accept` tokens
  recorded in the archive commit body.

### Author-accounting

* **Invariants.** (1) *Every row that leaves the board leaves with a token and,
  for `guard`, a named node that exists* — enforcer: the archive `Dispositions:`
  block plus the node running in the suite. This is the **first invariant in
  this lineage with a real mechanical enforcer**: a `guard` whose node does not
  exist fails collection. (2) *No row leaves without its condition being met* —
  documentary, reviewed.
* **Failure modes.** A vacuous assertion — **fails open**, which is why mutation
  proof is mandatory rather than recommended. A Class B row misjudged as
  satisfied — fails open; caught by a reviewer opening the cited evidence.
* **Edge cases.** A Class A row whose assertion turns out to need more than two
  assertions → it leaves Class A and stays on the board, unchanged. A Class B
  row that is *partly* satisfied → stays, with what was verified recorded.
* **Known omissions.** The board will still hold the design-work rows, and this
  pass makes no claim about them.

## Signals the change is wrong

* **An assertion passes under mutation.** Then it guards nothing and the row
  should go back on the board rather than be recorded as `guard`ed.
* **Class A grows past a handful.** The "one assertion" language in the rows was
  optimistic, and the right response is to stop, not to keep writing.
* **Class B closes almost nothing.** Then the imported rows are real work too,
  and the board's length is a resourcing fact — which is what the previous
  review believed and this proposal is testing rather than assuming.
