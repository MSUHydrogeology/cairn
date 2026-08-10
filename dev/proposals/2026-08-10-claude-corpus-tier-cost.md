<!-- cairn-internal-ref-allow: doctrine/dual-review.md doctrine/plans.md doctrine/proposals.md doctrine/rationale.md reason=doctrine/ citation convention -- a doctrine reference is a citation to Cairn's published methodology, not an installed local file (see templates/core/AGENTS.md, "Where doctrine/ references resolve") -->
<!-- The helper below is a forward reference: it is NEW and materializes in
     Part 1.  It is also registered under `Proposed paths:` -- that marker
     exempts only its own contiguous bullet block, so this file-scoped
     directive covers the Part 1 prose that names the same path.  Marked,
     not silenced; the line drops when the file lands. -->
<!-- claim-check-allow: bootstrap/tests/_immutable_git.py -->

# The suite's expensive head re-derives constants

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-10
**Status**: proposed
**Touches**: `bootstrap/tests/` test infrastructure only — a new shared
memoization helper, and its application to the six test files that
dominate suite wall-clock. No shipped file, no adopter-facing surface,
no doctrine, no dependency.
**Related**: [`verification-evidence-boundaries`](../plans/archive/verification-evidence-boundaries.md)
(which bounded *how often* the suite runs; this bounds *how long one run
takes*); [`transition-lint`](../plans/transition-lint.md) (open — owns the
file this proposal's largest change touches);
[`review-efficient-lifecycle`](2026-08-10-codex-review-efficient-lifecycle.md)
(the adjacent axis — reviewer *context* cost, not suite wall-clock)
**Plan review**: required(**Internal**) — test infrastructure with no
shipped, doctrine, or install-contract surface. But see *Security
preflight*: a test-side cache is a mechanism for making a check pass
without running it, and two of the six target files are trust-ceremony
surfaces. If the Maintainer reads that as security-touching, the
correct tier is External.

## Context

The engine suite has grown past the point where an implementing agent
runs it comfortably. Measured **2026-08-10** under the canonical
interpreter (`/Users/kendal30/conda_envs/lhm/bin/python3.13`, Python
3.13.13):

```
python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
4 failed, 2519 passed, 3 warnings in 380.17s
real 381.13   user 130.62   sys 131.29
```

**This is a diagnostic run, not a Boundary B record.** The working tree
carried 11 modified files from concurrent sessions. Three of the four
failures do not reproduce in a clean clone of HEAD; the fourth
(`test_security_check.py::test_detached_checkout_excludes_an_ignored_pytest_override`)
does, but it exercises detached-checkout mechanics that a `--shared`
clone may itself perturb. Neither the failures nor their cause are this
proposal's subject — the timing is, and timing is insensitive to both.

Two structural facts follow from that run.

**The suite is not CPU-bound; it is fork-bound.** 261.91s of CPU across
381.13s of wall is **0.69 cores busy**, on a host with 14 logical / 10
performance cores. `sys` time (131.29s) essentially equals `user` time
(130.62s): half the work is kernel — process creation and filesystem —
not computation. The tests spawn interpreters from 65 sites and invoke
`git` from 219, roughly 50 of them `git init`.

**The cost is concentrated.** Six files, measured in isolation:

| file | tests | seconds |
|---|---|---|
| `bootstrap/tests/test_transition_lint.py` | 40 | 103.32 |
| `bootstrap/tests/test_gate_preflight.py` | 127 | 39.43 |
| `bootstrap/tests/test_upgrade_module_additions.py` | 37 | 24.00 |
| `bootstrap/tests/test_security_stack.py` | 98 | 18.51 |
| `bootstrap/tests/test_upgrade.py` | 86 | 14.11 |
| `bootstrap/tests/test_oracle.py` | 18 | 12.93 |
| **total** | **406** | **212.30** |

406 of 2,527 collected nodes — **16% of the suite by count, 56% by
wall-clock**, `as_of 2026-08-10`. (Isolated timings include per-file
interpreter startup and do not reproduce in-suite contention. The
suite's own `--durations` reported `test_transition_lint.py`'s slow
nodes summing *higher* in-suite than in isolation, so if these figures
are biased, they understate.)

And the growth is not the test count. Against figures recorded in the
archive under the same interpreter: ~1,790 tests ran in 133–187s on
2026-08-03/04; 2,527 run in 380s today. Count **+41%**, wall **+129%**.
The mean per-node cost went 0.093s → 0.150s. The *kind* of test being
added changed. (A `1710 passed in 41.20s` figure in
`dev/plans/archive/release-authenticity.md` does not reconcile with
same-day ~300s runs and is treated here as an unexplained outlier, not
a baseline.)

### What the dominant file actually spends its time on

`scripts/transition_lint.py` is an advisory lint on commit-message /
diff agreement. Its **corpus tier** runs the committed script over
SHA-pinned windows of Cairn's own history — deliberately, and for a good
reason the file states plainly:

> A property test whose domain is the author's examples is a green
> light, not a pin.

That tier is not the problem. Its *arithmetic* is. The windows are four
contiguous segments of one span:

| window | commits |
|---|---|
| `ROOT..SELF_HOST` | 415 |
| `SELF_HOST..PROPOSAL` | 120 |
| `PROPOSAL..SNAPSHOT` | 332 |
| `ROOT..SNAPSHOT` (their sum) | **867** |

Enumerating every `tl.scan` / `tl._entries` call the tier makes against
the real repository yields **3,829 commit-visits over 867 distinct
commits** — a **4.4× redundancy factor**, `as_of 2026-08-10`. Two
causes: each widening test scans the same window twice (once with
`PINNED_RULES`, once with shipped rules) even though `_triggers` takes
no rules and the entire git enumeration is byte-identical between the
two passes; and `PROPOSAL..SNAPSHOT` is enumerated four separate times
across three tests.

A prototype confirms the redundancy is the cost. Replaying that exact
call set with and without a memo on `transition_lint._git`:

```
unmemoized     106.85s   git invocations:   6510
memoized        22.94s   git invocations:   1279
```

**4.66× wall, 5.09× fewer forks.** The unmemoized figure (106.85s)
slightly exceeds the whole file's measured 103.32s, so the replay is a
faithful *upper bound* on the corpus tier rather than an exact
reproduction — the ratio is the reliable number, not the absolute.

Every one of those reads is against a **full 40-hex SHA**. That
pinning was itself hard-won; the file records why:

> measured, that range moved 332 -> 333 -> 335 -> 363 across four
> commits in two days

Immutable keys are what make memoization sound here, and they are
already a requirement the tier enforces on itself.

### One segment is carrying nothing

`ROOT..SELF_HOST` is 415 of the 867 commits. Scanned directly:

```
ROOT..SELF_HOST: scanned=415  triggered=0  findings=0   (8.85s)
```

Zero triggered — not "nothing surprising," nothing *eligible*.
`_triggers` filters on `_in_scope(path)`, and Cairn did not host its own
`dev/` tree before `SELF_HOST_SHA`, so no commit in that prefix touches
a path the rule can match. The span-widening test scans it twice.

### The window does not grow, but it ratchets

Both ends are SHA-pinned, so new commits cost nothing — that is exactly
what the pinning buys. But `ROOT_SHA` is the repository's first commit,
so only `SNAPSHOT` ever moves, and it is stale: `SNAPSHOT` is dated
2026-08-03, HEAD is 2026-08-10, and **341 commits already sit outside
every window** (`as_of 2026-08-10`). A re-pin today would take the
largest window 867 → 1,208 commits, **+39% on the suite's most
expensive file**, with no new test written. Re-pin pressure is real:
`scripts/transition_lint.py`'s own header records six new
false-positive shapes in shape (a) plus a seventh in shape (b)
appearing within twelve days of the pinned measurement.

## Proposed paths

Proposed paths:
- `bootstrap/tests/_immutable_git.py` — the shared memoization helper; lands in Part 1.

## Proposal

### Part 1 — a shared memo for provably-immutable subprocess reads

Add `bootstrap/tests/_immutable_git.py`: a small, explicit, test-only
helper that wraps a subprocess-invoking callable and caches results
keyed on the **complete** argument tuple plus the working root.

Three constraints make it safe rather than merely fast, and all three
are contract, not convention:

* **Opt-in per call site.** It is a fixture an individual test class
  requests, never a global patch and never installed in `conftest.py`.
  A test that has not asked for it is unaffected.
* **Immutable inputs only.** It applies only where every argument is a
  full 40-hex SHA or a SHA-pinned rev-range. A `HEAD`-relative or
  branch-relative argument is **refused at the boundary** (raises), not
  silently passed through — a moving input in a cache is the failure
  mode, so it fails closed and loudly.
* **Complete keys.** The key is the full argv plus the root. A key that
  drops any component makes distinct calls collide and return the wrong
  bytes — which the target assertions detect (see *Rationale*).

The helper does **not** go into `scripts/transition_lint.py` or any
other shipped file. The tool runs once per invocation and has nothing
to memoize; only the tests scan repeatedly.

### Part 2 — apply it to the transition-lint corpus tier

Attach the memo to the corpus-tier classes in
`bootstrap/tests/test_transition_lint.py`
(`TestWideningIsNotCreating`, `TestWhitelistHygiene`,
`TestCorpusRegression`), at module scope alongside the existing
module-scoped `tl` fixture.

**Not one assertion changes.** The tests still scan the full 867-commit
span, still pin `(scanned, triggered) == (332, 265)`, still assert the
exact finding sets. Only the fork count drops. The synthetic tier —
which builds throwaway repositories per test and whose inputs are
therefore *not* immutable — is untouched and does not receive the memo.

### Part 3 — retire the vacuous prefix, on the mechanism

Narrow the span-widening test's window from `ROOT..SNAPSHOT` to
`SELF_HOST..SNAPSHOT`, and add a direct assertion that `_in_scope`
rejects every path shape present in the dropped prefix.

This is argued **on the mechanism, never on cost**: the 415 dropped
commits cannot contain a counterexample because they predate the
existence of the paths the rule matches. Arguing corpus reduction from
runtime is how a project loses the exhaustiveness a reviewer demanded,
and this proposal does not do that. The replacement `_in_scope`
assertion is what preserves the tripwire the prefix incidentally
provided.

**Part 3 is severable.** If review disagrees with the mechanism
argument, drop it; Parts 1, 2 and 4 stand alone and carry most of the
win.

### Part 4 — decide every remaining file in the head

For each of the five other files in the table above, the plan produces
a measurement and then **either** applies Part 1's memo **or** records
in writing why it cannot. No file in the head is left unaddressed, and
none is deferred to a board row.

The expected dispositions, stated now so review can attack them:

* `test_security_stack.py` — **cannot.** Its two slowest nodes
  (`test_a_t2_timeout_is_enforced_and_bounded`, 6.59s;
  `test_a_t6_descendants_do_not_outlive_the_timeout`, 6.12s) assert
  bounded elapsed time. The duration *is* the property; caching it
  would delete the test. ~12.7s of that file's 18.51s is irreducible by
  construction.
* `test_gate_preflight.py`, `test_oracle.py` — **likely cannot, and the
  reason is a security reason.** These exercise trust boundaries
  end-to-end through real subprocesses; the fork is the assertion. Any
  memo here needs the Security Review lens, not a performance argument.
* `test_upgrade.py`, `test_upgrade_module_additions.py` — **likely
  can**, via a session-scoped scaffolded baseline tree copied per test
  rather than rebuilt per test. Unmeasured; the plan measures before
  committing to a figure.

### Documentation / doctrine surface

**None.** No doctrine, no `AGENTS.md` rule, no shipped template, no
adopter-facing prose, no `CHANGELOG.md` entry — this changes test
infrastructure only, and adopters receive none of these files. Routed
per `docs/DOCUMENTATION_PLAN.md`: nothing here is prescription or
description, so nothing leaves the deliberation layer.

The one exception, if Part 3 lands: `dev/plans/transition-lint.md` owns
the corpus tier's rationale, and a narrowed window is a fact about that
plan's shipped artifact. The plan's archive record gets an appended
note. That is a record correction, not a doctrine change.

### Doctrine-change rate-limit

**N/A** — this proposal changes no doctrine, so the gate in
`doctrine/rationale.md` does not apply.

## Rationale

**Which workflow it improves.** Boundary B — the one full run an
implementing agent owes before code review
(`verification-evidence-boundaries`). That proposal cut the suite from
being run two or three times per boundary to once. This cuts what the
remaining once costs. The two compose; neither substitutes for the
other.

**Why the corpus tier is the right target and not the wrong one.** The
tier exists because the earlier version of these tests quantified over
the author's own fixtures, and an Internal review found a false
positive *by running rather than reading*. That is a genuine defense and
this proposal strengthens rather than weakens it: Part 2 changes no
assertion, and Part 3 replaces an incidental tripwire with a direct one.
The waste being removed is arithmetic — 3,829 visits to 867 commits —
not evidence.

**Why the cache cannot hide a regression.** This is the load-bearing
safety argument. The corpus assertions pin exact integers derived from
git (`scanned == 332`, `triggered == 265`) and exact finding sets. A
memo that returns stale, empty, or mis-keyed bytes changes those
integers and the tests go **red**. The assertions are the cache's own
oracle, and mis-keying fails closed. This is a stronger guarantee than
the usual cache argument, and it is the reason a memo is preferable to
either of the alternatives below.

**Why now.** The head is 56% of wall-clock and the largest single file
is about to get 39% more expensive at the next corpus re-pin. Fixing the
arithmetic before the re-pin is cheaper than after, and the re-pin is
the natural moment someone would otherwise argue for cutting evidence.

## Alternatives considered

**Do nothing.** The suite is still correct, just slow. Rejected because
the trend is the problem, not the level: +129% wall in a week, and a
known +39% step queued on the largest file.

**Shrink the corpus windows to something recent.** Cheapest-looking,
most expensive. Two of the three windows are load-bearing in ways
recency destroys: the 120-commit window reproduces the accepted
proposal's exact figures ("reproduced to the digit nine months later —
the payoff for SHA-pinning it"), and the 45-commit window asserts the
must-not-flag set by construction over commits that are historical by
definition. Rejected outright, and named here so nobody reaches for it
later under time pressure.

**Skip the corpus tier when `scripts/transition_lint.py` is unchanged**
— hash the script, store the expected result, re-derive only on edit.
Tempting, because the tier genuinely does re-derive a constant. Rejected
because **it fails open**, and the file itself contains the proof: its
E4 comment records that the accepted proposal's reasoning assumed `-M`
enumeration producing `R091`, while the pinned `--find-renames=100%`
produces `D` + `A`. Git's own rename-detection behavior is an input to
the result. A key over the script alone would silently skip a tier whose
answer had changed underneath it — the exact failure the memo avoids by
keying on the complete argv and letting the assertions verify it.

**Parallelize the suite** (`pytest-xdist -n 8`). This is almost
certainly the larger win — the suite runs at 0.69 cores on a 10-core
host, and the order-independence sub-gate (`scripts/quality_gate.py
--sub order-independence`) already provides evidence the suite is
shuffle-safe. It is not proposed here because it is a **different
mechanism with a different cost**: a dev-only dependency requiring a
fourth Exception in `bootstrap/DEPENDENCY_BUDGET.md`, plus an audit of
tests touching genuinely shared state (`refs/cairn/gate-anchor`, the
intent log, `dev/measurement/`). Bundling it would make one proposal
carry two unrelated risk arguments. **This is a recommendation to the
Maintainer, not a deferral**: the two are independent and multiply
(4.66× on the head × ~6× from parallelism), and I think the
parallelization proposal is worth opening. Whether it is opened is the
Maintainer's call, and this proposal does not create a board row for it.

## Evidence / verification plan

**Tests.** No new behavioral coverage is required by Parts 1–2: the
existing corpus assertions are the acceptance criterion, and they must
produce **byte-identical results** before and after. The plan records
both. Part 1's helper gets its own nodes: the immutability refusal
(a `HEAD`-relative argument raises) and the completeness-of-key
perturbation below. Part 3 adds the direct `_in_scope` assertion that
replaces the dropped prefix.

**Examples / smoke checks.** `python scripts/check_cairn.py` for this
document. No example-gallery or scaffold surface is touched.

**Docs.** N/A — see *Documentation / doctrine surface*.

**The falsification that matters.** `test_transition_lint.py` requires
every node to carry a named perturbation, run and observed red. Part 1
inherits that: drop one component from the memo key, re-run, and confirm
the corpus assertions go red. If they stay green, the memo is not
keyed on anything the assertions depend on, and the whole safety
argument above is void.

### Author-accounting — invariants, failure modes, edge cases

* **Invariant** — the memo returns exactly what an uncached call would.
  *Enforced by*: the corpus assertions themselves (exact `scanned` /
  `triggered` integers and finding sets), plus the key-completeness
  perturbation above. This is the one invariant that matters and it has
  a real enforcer, not a restatement.
* **Invariant** — the memo is never reachable from a mutable input.
  *Enforced by*: the boundary refusal in Part 1 (raises on a
  non-40-hex argument), with its own test node.
* **Failure mode — mis-keyed.** *Closed.* Colliding keys return wrong
  bytes; the exact-integer assertions fail.
* **Failure mode — stale across a history rewrite.** *Closed.* Pinned
  SHAs stop resolving, and `_corpus_available()` already skips the tier
  rather than failing it.
* **Failure mode — memo silently disabled.** *Open, and acceptable.*
  The suite is merely slow again; no assertion weakens.
* **Edge cases** — empty rev-range (the tier already covers
  single-commit ranges at `{sha}~1..{sha}`); a window with zero
  triggered commits (measured: `ROOT..SELF_HOST`); repeated identical
  calls within one test (the common case).
* **Public-path → test mapping** — the public path is
  `transition_lint.scan`, exercised through its real entry point by
  [`bootstrap/tests/test_transition_lint.py`](../../bootstrap/tests/test_transition_lint.py).
  No new public path is added; `_immutable_git.py` is test-only and has
  no adopter-reachable caller.
* **Known omissions** — Part 4's dispositions for
  `test_upgrade.py` and `test_upgrade_module_additions.py` are
  **unmeasured predictions**, flagged as such; the plan measures before
  committing. No claim is made here about the achievable figure for
  those two files.

#### Security preflight — five questions

Answered rather than waived, because a test-side cache is precisely a
mechanism for making a check pass without running it, and two target
files are trust-ceremony surfaces.

* **S1 — Who supplied it?** The memo's inputs are argv tuples built by
  test code from constants pinned in the test file, plus the repository
  root. Nothing under test supplies its own cache key. The corpus SHAs
  are literals in `test_transition_lint.py`, not read from any artifact
  the tests evaluate.
* **S2 — Can it fail?** Yes, and the mutation is stated above: remove a
  component from the key and the corpus assertions go red. That
  perturbation must be **run and observed**, per the file's own
  convention, not asserted.
* **S3 — What fires it, over what?** `python -m pytest bootstrap/tests`
  — Cairn has no CI, so a person or an agent types it. The memo is
  selected by explicit fixture request in three named classes and
  covers only their `REPO_ROOT`-targeted calls. Nothing else in the
  suite sees it.
* **S4 — Which way does it break?** Toward *less* authority in every
  case. A non-immutable argument raises rather than passing through; a
  mis-key produces wrong bytes that fail an assertion; an absent memo
  means a slow correct run. There is no path where the memo grants a
  test a pass it would not otherwise get — because it computes no
  verdict, only relays bytes that the assertions then check.
* **S5 — Who still wins?** Assumed capability: an author who wants a
  green corpus tier without running it. This change does not close
  that — an author can already delete an assertion. What it must not do
  is make that *easier or less visible*, which is why the memo is
  opt-in per class, why it refuses mutable inputs, and why Parts 3's
  window narrowing is argued on mechanism rather than cost. The class
  is closed **by construction** for accidental staleness and **not
  closed at all** for a deliberate author — the same posture the rest
  of Cairn's trusted-contributor model takes.

## Signals the change is wrong

* **The corpus assertions produce different values after the memo.**
  Then the memo is unsound; revert Part 2. This is checkable in one
  command and is the plan's first acceptance gate.
* **The key-completeness perturbation stays green.** Then the safety
  argument is void and the whole approach needs rethinking, not
  patching.
* **The measured speedup is well under the prototype's 4.66×.** Then
  the prototype's replay is not faithful to the real call set and the
  Context section's arithmetic is wrong somewhere; re-derive before
  proceeding.
* **Review rejects Part 3's mechanism argument.** Then drop Part 3
  only. It is severable by construction, and losing it costs roughly
  9s, not the proposal.
* **A later corpus re-pin restores the cost.** The memo makes re-pinning
  cheaper but not free; if wall-clock returns to 100s+ after a re-pin,
  the right answer is the parallelization axis, not further corpus
  cutting.

## Sequencing constraint

Parts 2 and 3 touch `bootstrap/tests/test_transition_lint.py`, whose
plan `dev/plans/transition-lint.md` is **open** with an External code
review appended 2026-08-10. Implementation of Parts 2–3 waits on that
plan reaching archive, or on its owner's explicit concurrence. Part 1
and Part 4's measurement pass are unblocked and can proceed first.
