# Suite cost — the standing measurement

**Read this instead of re-measuring.** The engine suite costs roughly ten
minutes, and the question *"what does it cost, and where?"* has now been
answered by a full profiling run at least four separate times — each answer
landing inside a proposal or plan that then archived. `README.md` in this
folder calls an archive a graveyard for exactly this reason: the number stayed,
the *place to look it up* did not. So the next agent re-ran the suite to
rediscover it.

This file is that place. If you are about to run the full suite to find out how
long it takes or which files dominate, the answer is below and you do not need
the run.

## Standing figures

`as_of 2026-08-19`, canonical interpreter (Python 3.13.13):

| | |
|---|---|
| Collected nodes | 4,468 |
| Wall-clock, whole suite | ~570–690s (**9.5–11.5 min**) |
| Test files | 115 collected (126 `.py` files in `bootstrap/tests/`) |
| Profiled wall accounted by `--durations` | 558.6s |
| Phase split | call 451.3s · teardown 62.4s · setup 44.9s |

**The cost is concentrated, and the tail is nearly free:**

| Share of wall-clock | Files needed |
|---|---|
| 50% | top **7** files |
| 80% | top **16** files |
| 90% | top **22** files |
| 95% | top **30** files |

23 files — **425 tests** — register no duration row at all: every test in them
runs under 5ms. Most of this suite is already fast. A small, stable, and
*identifiable* minority is not.

### The expensive head

Top ten by wall-clock, `as_of 2026-08-19`. Full table:
[`snapshots/2026-08-19-suite-durations.csv`](snapshots/2026-08-19-suite-durations.csv).

| file | tests | seconds | % |
|---|---:|---:|---:|
| `bootstrap/tests/test_gate_preflight.py` | 340 | 131.7 | 23.6% |
| `bootstrap/tests/test_security_net.py` | 84 | 34.3 | 6.1% |
| `bootstrap/tests/test_portable_security_sweeps.py` | 163 | 32.7 | 5.9% |
| `bootstrap/tests/test_upgrade_module_additions.py` | 37 | 31.7 | 5.7% |
| `bootstrap/tests/test_pilot_evidence.py` | 97 | 25.1 | 4.5% |
| `bootstrap/tests/test_transition_lint.py` | 40 | 23.2 | 4.2% |
| `bootstrap/tests/test_security_check.py` | 111 | 22.5 | 4.0% |
| `bootstrap/tests/test_security_finding_confidentiality.py` | 40 | 19.8 | 3.5% |
| `bootstrap/tests/test_security_stack.py` | 98 | 19.7 | 3.5% |
| `bootstrap/tests/test_gate_manifest.py` | — | 18.9 | 3.4% |

One file, `test_gate_preflight.py`, is **a quarter of the entire suite**, and
essentially all of it is `call` time (131.64s of 131.74s) — not fixture setup.
`test_security_net.py` is the opposite shape and worth knowing about: 28.2s of
its 34.3s is **teardown**.

## What the growth curve does and does not show

Every figure below is a dated snapshot with its own conditions, recovered from
the deliberation record:

| date | commit | nodes | wall | conditions |
|---|---|---:|---:|---|
| 2026-08-04 | `7bb2072` | 1,790 | 129.7s | clean; reconciliation baseline |
| 2026-08-10 | — | 2,527 | 380.2s | **dirty tree**, diagnostic, 4 failures |
| 2026-08-13 | — | 4,277 | 689.5s | clean; a Boundary B record |
| 2026-08-19 | `cf8bed7`± | 4,468 | 568.3s | **dirty tree**, diagnostic, 7 failures |

Sources, in order:
[`dependency-advisory-coverage`](../plans/archive/dependency-advisory-coverage.md),
[the corpus-tier-cost proposal](../proposals/archive/2026-08-10-claude-corpus-tier-cost.md),
[`review-efficient-lifecycle`](../plans/archive/review-efficient-lifecycle.md),
and this file's own snapshot.

**These four points are not safely comparable, and that is the finding.** The
2026-08-19 run is *faster* than 2026-08-13 while carrying 191 more tests. The
tempting reading — that the
[`corpus-tier-cost`](../plans/archive/corpus-tier-cost.md) optimisation caused
it — is wrong: that plan archived 2026-08-11, so its gains were already inside
the 2026-08-13 figure. The likeliest explanation is **concurrent load**: the
2026-08-13 run competed with a second suite running in another session, and
nothing in the record captured that. Two of the four runs were against dirty
trees carrying other sessions' edits.

So the growth curve cannot presently answer *"is the suite getting slower?"* —
because the recorded figures do not carry the conditions needed to compare
them. Four hand-transcribed numbers, each captured for a different purpose, are
not a time series.

What *is* solid: `test_transition_lint.py` fell from **103.3s** (2026-08-10, in
isolation) to **23.2s** today. `corpus-tier-cost` targeted precisely that file
and predicted a 4.66× improvement from memoising immutable SHA-keyed git reads.
Measured 4.5×. **That optimisation worked**, and the file it dethroned is no
longer in the top five.

## How this file gets refreshed

Today, by hand:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest bootstrap/tests -q --durations=0 -p no:cacheprovider
```

then re-aggregating per file. **This is the wrong mechanism** and is the reason
the figures above have gaps: a measurement that depends on someone deciding to
measure is taken rarely, taken under uncontrolled conditions, and recorded
without them.

The intended replacement is for the suite to **emit a diagnostics record on
every run** — every run, including scoped ones — carrying the commit, tree
state, interpreter, invocation scope, node counts, outcomes, wall-clock, and
per-file durations. That turns this table into a by-product of ordinary work
rather than an errand, and it makes a second thing visible that no current
record captures at all: **how often the full suite is actually being run**,
which is the number the maintainer is trying to reduce.

That change belongs in
[`bootstrap/tests/conftest.py`](../../bootstrap/tests/conftest.py), which is
gate-frozen — so it costs a re-anchor ceremony and takes a proposal. Two
constraints any such hook must meet, both non-negotiable:

* **Outcome-inert.** It must never alter `session.exitstatus`, never raise, and
  never interfere with the release-mode outcome rule that file already carries.
  A diagnostics hook that can fail a suite is a worse defect than no hook.
* **Written outside the tracked tree.** Boundary B requires a clean, unchanged
  commit with clean pre/post state. A ledger written into a *tracked* file on
  every run would dirty the tree on every run and break that precondition
  outright — and would collide across concurrent sessions. The live ledger is
  therefore gitignored, exactly as `dev/reflections/` is, with curated dated
  exports committed to `snapshots/` at a serialization point.

## Provenance of the 2026-08-19 profile

Run against a working tree carrying uncommitted edits from two concurrent
sessions; 7 tests failed. All seven are corpus-sensitive — they scan the live
`dev/` tree, which was being mutated during the run, including by this file's
own preparatory commit. **This is a diagnostic run, not a Boundary B record**,
and it is not evidence about correctness. Timing is insensitive to which
corpus-scanning assertions failed, so the durations stand; the pass/fail line
does not.

Failing nodes, recorded so a later reader does not mistake them for a
regression signal: five in `test_lifecycle_contract.py`, one in
`test_lifecycle_board.py`, one in `test_portable_security_sweeps.py`.
