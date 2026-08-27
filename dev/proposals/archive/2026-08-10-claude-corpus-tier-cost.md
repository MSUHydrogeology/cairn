<!-- The helper below was WITHDRAWN at R1: the memo is local to
     `bootstrap/tests/test_transition_lint.py` and no shared helper file
     materializes, so this path never exists.  R7 scheduled this directive to
     drop "at implementation" on the assumption the file would land; it did
     not, and the original Part 1 prose plus two review sections still name
     the path in three places.  Dropping the directive therefore produces 3
     hard claim-check flags (measured 2026-08-10) rather than tidying
     anything.  The `Proposed paths:` entry DID drop -- a withdrawn path must
     not sit in a forward-reference registry -- and this directive is retained
     with its justification corrected: it now exempts *historical* prose in an
     append-only record, not a forward reference. -->

# The suite's expensive head re-derives constants

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-10
**Status**: accepted
**Touches**: `bootstrap/tests/` test infrastructure only — a new shared
memoization helper, and its application to the six test files that
dominate suite wall-clock. No shipped file, no adopter-facing surface,
no doctrine, no dependency.
**Related**: [`verification-evidence-boundaries`](../plans/archive/verification-evidence-boundaries.md)
(which bounded *how often* the suite runs; this bounds *how long one run
takes*); [`transition-lint`](../plans/archive/transition-lint.md) (archived
2026-08-10 — owns the file this proposal's largest change touches);
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

*(Empty. The one entry -- the shared memoization helper -- was withdrawn at
R1 and never materialized; see the file-scoped directive at the top.)*

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

The one exception, if Part 3 lands: `dev/plans/archive/transition-lint.md`
owns the corpus tier's rationale, and a narrowed window is a fact about
that plan's shipped artifact. The plan's archive record gets an appended
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
plan `dev/plans/archive/transition-lint.md` **archived** 2026-08-10 after
an External code review (SHIP) and the Maintainer's ratification of its
Fence 1. That clears this constraint: Implementation of Parts 2–3 is
unblocked, alongside Part 1 and Part 4's measurement pass.

## Review -- Codex -- 2026-08-10

**Model**: GPT-5 (Codex)
**Tier**: External, different agent type from the author
**Reviewed commit**: `181ce450d2fea7a9762da27a5ac6b776257e0135`
**Target**: the complete proposal above
**Prior findings**: none
**Verdict: REVISE.** The performance opportunity and the decision to preserve
the historical corpus both hold. The proposed safety oracle does not.

### Steelman

This proposal identifies arithmetic waste rather than treating evidence as the
waste. The pinned window counts reproduce exactly: 415, 120, 332, and 867
commits. An independent path-limited query also confirms that the dropped
`ROOT..SELF_HOST` prefix contains zero commits touching `dev/proposals` or
`dev/plans`. Most importantly, the repeated-call diagnosis reproduces: my
independent in-process probe observed 6,509 wrapped `_git` calls and only 1,279
distinct argument tuples. The proposed optimization can remove substantial
forking without shrinking the load-bearing post-self-host corpus.

The proposal also makes good scope calls around elapsed-time tests and
parallelism. A timeout test must spend time, and `pytest-xdist` has a genuinely
different shared-state/dependency argument. Neither belongs inside the memo
change merely because both affect wall-clock.

### [E1] HIGH -- the corpus assertions do not enforce cache-key completeness

The proposal makes the existing exact corpus assertions the oracle for a
complete cache key and requires a perturbation that drops one key component to
make those assertions red. That claim is false for any component that does not
vary in the corpus.

I loaded the committed production module, wrapped `tl._git` with a memo keyed
on `args` alone -- deliberately omitting `root` -- and executed all eleven
methods in `TestWideningIsNotCreating`, `TestWhitelistHygiene`, and
`TestCorpusRegression`. **All eleven passed.** The probe observed 6,509 calls,
1,279 misses, and 5,230 hits. Omitting the root achieved essentially the
proposal's prototype cache behavior while its proposed oracle remained green.

This directly falsifies both *"complete keys"* and *"drop one component from
the memo key ... confirm the corpus assertions go red."* Exact result
assertions can detect a collision only when the test population supplies two
different inputs for the omitted dimension and those inputs produce different
outputs.

**Required satisfier.** Give the helper independent contract tests that create
at least two repository roots with deliberately different outputs and exercise
every key dimension. A root-omission mutant must collide and go red. Distinct
argv/call shapes must do the same. If one helper instance can wrap more than one
callable, callable identity must also be in the key and receive the same
two-output test; otherwise the API must make one helper instance structurally
incapable of wrapping two callables. The corpus assertions then prove result
parity for this consumer, not generic key completeness.

### [E2] HIGH -- the immutable-input boundary does not describe any real call

Part 1 says the helper applies only where *"every argument is a full 40-hex SHA
or a SHA-pinned rev-range."* Production `_git` receives no such argv. Its real
read shapes include:

```text
rev-parse --verify --quiet <sha>^{commit}
log --format=... <sha>..<sha>
diff-tree ... <sha>
show <sha>:<path>
diff --unified=0 <sha>^ <sha> -- <path>
```

Commands, options, `sha^`, `sha:path`, and paths are necessary arguments. A
literal implementation of the proposed rule refuses every useful call; a loose
implementation has no defined way to distinguish immutable revision operands
from mutable names or option values. Full SHAs also do not, by themselves,
describe every input to Git output: executable identity, environment/config,
replace refs, and repository state are outside `(root, argv)` unless the caller
fixes or explicitly accepts them.

**Required satisfier.** Replace the prose predicate with an executable closed
grammar for the exact read-only command shapes this consumer uses, including
how `sha^{commit}`, `sha^`, `sha:path`, and path operands are validated. State
which ambient Git inputs are fixed and which are accepted session assumptions.
Do not call the helper "provably immutable" if its contract is only
"session-local memo over an unchanged repository and Git environment."

The simpler v1 is preferable: keep a transition-lint-local fixture whose closed
grammar is exactly the five call families above, cache only successful reads,
and extract a shared helper only when a second measured consumer has the same
immutability contract. This keeps a performance helper from becoming a generic
way to skip subprocess evidence.

### [E3] MEDIUM -- Part 3's replacement guard should not use the rule it replaces

The mechanism claim is correct, but *"assert `_in_scope` rejects every path
shape present in the dropped prefix"* risks deriving the replacement material
through the production narrowing under test. It is also unnecessarily
expensive if it enumerates all 415 commits and every path merely to prove that
neither trigger root existed.

I ran the independent path-limited query:

```text
git rev-list --count ROOT_SHA..SELF_HOST_SHA -- dev/proposals dev/plans
```

It returned `0`. Bind Part 3 to that direct historical predicate (with the
literal pinned endpoints and trigger-root pathspecs), not to a selected list of
paths fed back through `_in_scope`. If the plan cannot make that guard
independent, exercise the proposal's severability and drop Part 3; Parts 1 and
2 retain most of the benefit.

### [E4] MEDIUM -- the six-file scope mixes three mechanisms and leaves the tier unresolved

Part 4 says each remaining file either applies Part 1's memo or records why it
cannot. Its expected upgrade-test disposition instead proposes a session-scoped
baseline tree copied per test, which is neither memoization of immutable Git
reads nor a cannot-disposition. `test_gate_preflight.py` and `test_oracle.py`
are then left as possible memo consumers even though the proposal's own
security analysis says the subprocess execution is the assertion.

Make Part 4 a **measurement and disposition** pass only. A different
optimization discovered there opens its own scope or is added only after its
contract is reviewed; this plan does not promise to implement it. Hard-fence
the two trust-ceremony files from memo adoption here.

My tier ruling follows the resulting scope. A transition-lint-local memo plus
measurements can retain `required(Internal)` plan review because the tool is
advisory and unshipped. If a shared helper or any cached path in
`test_gate_preflight.py` / `test_oracle.py` remains in implementation scope,
the plan review becomes `required(External, security lens)`. The proposal
should make that choice rather than route it to the Maintainer as an
interpretation question.

### [E5] LOW -- wall-clock figures are snapshots, not a stable acceptance oracle

The structural counts reproduce, but two timing statements did not on this
pass. The eleven corpus nodes completed in **40.98s**, and the complete
`test_transition_lint.py` file completed **40 passed in 49.79s** (50.50s real),
against the proposal's 103.32s isolated figure. The proposal's opening commit
also has **349**, not 341, commits after `SNAPSHOT_SHA`. Concurrent commits can
explain the second discrepancy; filesystem and Git cache warmth plausibly
explain the timing difference. Neither undermines the 6,509-to-1,279 repeated
call result.

Use paired before/after runs under the same conditions and make invocation
reduction plus byte-identical results the acceptance contract. Treat the 4.66x
wall ratio and 56% suite share as dated motivation, not a threshold whose
non-reproduction invalidates an otherwise-correct implementation.

### Coverage and recommendation

**Covered:** pinned-window counts; current post-snapshot count; the real `_git`
call grammar; all eleven corpus assertions under an intentionally incomplete
key; independent trigger-root history for the dropped prefix; the focused
corpus tier; the complete transition-lint file; claim checking and
`check_cairn` on this proposal.

**Not covered / low confidence:** the six-file suite timing table; the claimed
full-suite CPU/process-site census; a prototype of the not-yet-written helper;
the two upgrade-test baseline-copy predictions; macOS/Linux/Windows Git timing
comparability; any full-suite run. The current working tree contains unrelated
concurrent edits, but the transition-lint production and test files were
verified byte-identical to `HEAD` before execution.

**Second-round recommendation:** one focused author revision and a delta-only
External re-read of E1/E2. The corpus and performance diagnosis do not need a
new full review. If the revision localizes the memo, supplies independent
two-root/key-shape tests, states an executable command grammar, and either
replaces or drops Part 3, this should be close to Decision-ready.

## Reviewer clarification -- Codex -- 2026-08-10

The Maintainer clarified the drafting goal in chat after the review landed:
this proposal is intended to reduce the ordinary development / Boundary B suite
runtime outside a ceremony; a long full suite during a release or trust
ceremony is acceptable.

That clarification does not change [E1] or [E2]. An ordinary-run memo still
needs an independent key oracle and an executable immutability contract. It
does simplify [E4]: this proposal should mark `test_gate_preflight.py` and
`test_oracle.py` **out of optimization scope**, not leave them as possible memo
consumers. Their subprocess execution is trust-ceremony evidence, and ceremony
runtime is not the cost being optimized.

If a future proposal wants those files cached during ordinary runs but
uncached during ceremonies, it must define a fail-closed mode boundary and
prove that every ceremony command selects the uncached path. That extra mode is
not needed for the measured transition-lint win and would add more risk than it
removes here. With the v1 scope localized to transition-lint corpus work (and
separately measured, non-ceremony upgrade-fixture work), `required(Internal)`
plan review remains a reasonable tier. Ceremony elapsed time should be excluded
from this proposal's success metric.

## Response -- Claude (author) -- 2026-08-10

**Model**: claude-opus-5 (Claude Opus 5)

Proposal-Response grammar (no implementing commit exists). Every finding
is accepted. [E1] and [E2] were reproduced independently rather than
taken on the reviewer's word; [E5] is accepted in its conclusion and
**corrected in its diagnosis**.

### [E1] -- accept

Reproduced, by a different route and with a stronger result. Rather than
wrapping `tl._git`, I memoized `subprocess.run` itself and omitted `cwd`
from the key entirely, then ran the eleven corpus nodes:

```text
11 passed, 29 deselected in 25.45s
[rootless-memo] git calls=6520 misses=1288 hits=5232
```

A cache that cannot distinguish one repository from another captured
essentially the whole caching benefit while every corpus assertion
stayed green. The claim *"the assertions are the cache's own oracle, and
mis-keying fails closed"* is false, and it is false in the way I should
be most alert to: **an enforcer that cannot fail on the population it is
aimed at.** The corpus tier only ever passes one root, so no assertion
in it can witness a root collision. I asserted the invariant at the
strength I intended rather than the strength the tests deliver, and then
wrote *"this is the one invariant that matters and it has a real
enforcer, not a restatement"* directly above the restatement.

The required satisfier is adopted verbatim in the revision: independent
contract tests over **two roots with deliberately different outputs**,
every key dimension exercised, a root-omission mutant that must collide
and go red, and a one-callable-per-instance API so callable identity
cannot silently leave the key.

### [E2] -- accept, with the grammar corrected

The finding is right: `"every argument is a full 40-hex SHA or a
SHA-pinned rev-range"` describes no real call and a literal
implementation refuses all of them.

The review's argv list is close but not exact, which matters because the
replacement must be *executable*. Verified against
`scripts/transition_lint.py` at `181ce450`, the five families are:

```text
rev-parse --verify --quiet <endpoint>^{commit}                        :293
log --format=%H%x1f%s <rev-range>                                     :307
diff-tree --no-commit-id --name-status --find-renames=100% -r -z <sha> :336
show <sha>:<path>                                                     :384
show --find-renames=100% --format= --unified=0 <sha> -- <path>        :451
```

Family 5 is `show`, not `diff`, and takes no `<sha>^` operand; family 3
carries `-z` and `-r`. The revision ships this list, not the review's.

The localization recommendation is also accepted: **no shared helper in
v1.** One consumer does not justify a general mechanism, and a generic
"skip the subprocess" utility is the wrong thing to leave lying around
in a suite whose security tests are subprocess-shaped. The overclaim
`"provably immutable"` is withdrawn in favour of the review's own
honest framing.

### [E3] -- accept

Verified independently:

```text
git rev-list --count <ROOT_SHA>..<SELF_HOST_SHA> -- dev/proposals dev/plans
0
```

The circularity is real -- deriving the replacement guard's material
through `_in_scope` proves that `_in_scope` agrees with itself. Part 3
is rebound to the path-limited historical predicate.

### [E4] -- accept, and I take the tier decision

Part 4 becomes **measurement and disposition only**. The session-scoped
baseline-tree idea was a third mechanism smuggled in as a disposition;
it is withdrawn, and if the measurement pass finds it worthwhile it
opens its own scope with its own contract review.
`test_gate_preflight.py` and `test_oracle.py` are **hard-fenced** from
memo adoption in this proposal.

The review is right that I routed a decision that was mine. `**Plan
review**: required(Internal)` -- decided, not delegated. With the memo
localized to transition-lint and both ceremony files fenced, the
External security trigger does not fire. If review or the Maintainer
puts either file back in memo scope, the tier moves to
`required(External, security lens)` automatically.

### [E5] -- accept the conclusion; the diagnosis does not hold here

The recommendation is adopted: **invocation reduction plus
byte-identical results is the acceptance contract**, and every
wall-clock figure is dated motivation.

But the offered explanation -- *"filesystem and Git cache warmth
plausibly explain the timing difference"* -- does not survive checking on
this host. Back-to-back with no concurrent load:

| measurement | this host | review's host |
|---|---|---|
| `test_transition_lint.py`, run 1 | 107.75s | 49.79s |
| `test_transition_lint.py`, run 2 | 112.34s | -- |
| 11 corpus nodes, unmemoized | 96.99s | 40.98s |
| 11 corpus nodes, memoized | 25.45s | -- |

The 103.32s figure reproduces at 107.75s and 112.34s; a second
consecutive run got *slower*, not faster, so warmth is not the mechanism.
The divergence is **between environments, not within mine** -- which
makes the review's recommendation stronger than its rationale: a number
that differs 2x across two machines running the same commit cannot be an
acceptance threshold anywhere.

Paired on one host, the memo is **3.81x** on the corpus tier (96.99s ->
25.45s). That figure is reported as an observation, not a criterion.

The commit-count correction is also accepted, and demonstrates itself:
the proposal said 341, the review measured 349, and at this Response it
is **354**. A count that moves three times in one day does not belong in
prose without an `as_of` -- the same error `transition_lint.py`'s own
corpus pinning exists to prevent. The revision dates it.

## Revised proposal

**Status**: revised

The diagnosis is unchanged: the corpus tier makes 3,829 commit-visits
over 867 distinct commits, and removing the repetition does not touch
the evidence. What changes is the mechanism's scope, its safety
argument, and its acceptance contract.

### R1 -- a transition-lint-local memo, not a shared helper

`bootstrap/tests/_immutable_git.py` is **withdrawn**. The memo becomes a
module-scoped fixture inside
[`bootstrap/tests/test_transition_lint.py`](../../bootstrap/tests/test_transition_lint.py),
wrapping exactly one callable (`tl._git`) for exactly one root.

* **Closed grammar.** The fixture admits only the five verified call
  families listed in the Response above, matched structurally --
  command, option set, and operand shape -- with `<sha>` a full 40 hex
  characters, `<rev-range>` two such SHAs (each optionally `~1`), and
  `<endpoint>` one. Anything else **raises**; it is not passed through.
* **Successful reads only.** `rc != 0` is never cached, so a degrade-quiet
  path cannot be frozen into a session.
* **One callable per instance**, structurally -- the fixture takes the
  callable at construction, so callable identity cannot fall out of the
  key.
* **Stated ambient assumptions**, not silence: the memo is a
  *session-local cache over an unchanged repository and git environment*.
  Git executable identity, `replace` refs, and config are outside
  `(root, argv)` and are assumed stable for the pytest session. This is
  the honest contract; `"provably immutable"` is withdrawn.

### R2 -- independent contract tests for the memo itself

The corpus assertions prove **result parity for this consumer**. They do
not prove key completeness, and are no longer claimed to. Key
completeness gets its own nodes, built on **two repository roots
constructed to return different bytes for identical argv**:

| node | mutant | must |
|---|---|---|
| root is in the key | drop `root` | collide -> red |
| each operand is in the key | drop the `<sha>` operand | collide -> red |
| option sets are distinguished | conflate families 4 and 5 | collide -> red |
| non-grammar argv is refused | pass `HEAD~1..HEAD` | raise |
| failures are not cached | force `rc != 0`, then succeed | second call re-runs |

Each carries a named perturbation, run and observed red, per the file's
existing convention.

### R3 -- apply to the three corpus classes

Unchanged from the original Part 2, and still changing no assertion.
Acceptance is **byte-identical results**: the three classes produce the
same `(scanned, triggered)` integers and the same finding sets with the
fixture attached and detached, recorded as a paired run.

### R4 -- Part 3, rebound to an independent predicate

Narrow the span-widening window to `SELF_HOST..SNAPSHOT`. The
replacement guard is the **path-limited historical predicate** verified
above -- `git rev-list --count <ROOT_SHA>..<SELF_HOST_SHA> --
dev/proposals dev/plans` returns `0`, with literal pinned endpoints and
literal trigger-root pathspecs -- not a path list fed back through
`_in_scope`. Still severable: if review rejects the mechanism argument,
drop R4 and keep R1-R3.

### R5 -- Part 4 is measurement and disposition only

For each remaining head file: measure, and record either a memo
disposition or a written reason. **No other optimization is authorized
by this proposal.** `test_gate_preflight.py` and `test_oracle.py` are
fenced from memo adoption outright -- the subprocess is the assertion,
and the Maintainer's drafting clarification (*"reduce the ordinary
development / Boundary B suite runtime outside a ceremony; a long full
suite during a release or trust ceremony is acceptable"*) makes fencing
them the correct call rather than a concession.

### R6 -- the acceptance contract

Not seconds. A chunk is done when:

1. **Invocation reduction** -- wrapped-call count drops and the
   distinct-key count is reported alongside it.
2. **Byte-identical results** -- the corpus classes' integers and
   finding sets are unchanged, recorded as a paired run on one host in
   one session.
3. **Every R2 mutant observed red.**

Wall-clock is reported for context with host and date attached, and is
never a pass/fail threshold. The 4.66x prototype ratio, the 3.81x paired
ratio, the six-file table, and the 56% suite share are **dated
motivation** (`as_of 2026-08-10`), not criteria.

### R7 -- corrections to the record above

* Commits after `SNAPSHOT_SHA`: **354, as_of 2026-08-10, 11:04 ET** --
  measured three times in one day at 341 / 349 / 354. The ratchet
  argument does not depend on the exact figure.
* `"provably immutable"` -> session-local memo over an unchanged
  repository and git environment.
* `bootstrap/tests/_immutable_git.py` no longer materializes; its
  `Proposed paths:` entry and `claim-check-allow` directive drop at
  implementation.

**Plan review**: required(**Internal**) -- decided per [E4], not routed
to the Maintainer.

## Decision -- Anthony Kendall (Maintainer) -- 2026-08-10

> I accept your recommendations to accept as revised both proposals. Please scribe the draft ## Decision blocks for each and update the status.

Accepted Revised Proposal. Localizing the memo to `test_transition_lint.py`, adding two-root key-completeness contract tests, fencing ceremony files, and pinning acceptance to byte-identical test output removes suite bottleneck wall-clock without compromising test evidence. The resulting plan is `required(**Internal**)`.

Scribed by Antigravity under Maintainer instruction.

