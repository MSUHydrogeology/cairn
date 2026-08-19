# The suite should report its own cost

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-19
**Status**: awaiting-review
**Assurance path**: **high-assurance** — the change edits `bootstrap/tests/conftest.py`,
which is gate-frozen, so landing it requires a re-anchor (a trust ceremony). It
also adds a **file write and a subprocess invocation to every test session**,
which is a trust boundary being widened in the one file that can already decide
a session's exit status.
**Touches**: `bootstrap/tests/conftest.py` (gate-frozen); `.gitignore`;
`dev/measurement/README.md`; one new test file; one new reader tool. No shipped
template, no adopter-facing surface, no doctrine text, no dependency.
**Related**: [`corpus-tier-cost`](../plans/archive/corpus-tier-cost.md) (which
attacked *how long one run takes*; this measures it continuously);
[`verification-evidence-boundaries`](../plans/archive/verification-evidence-boundaries.md)
(which bounded *how often* the suite runs); the
[boundary-b-bounding-clause](archive/2026-08-12-claude-boundary-b-bounding-clause.md)
proposal (whose bounded mode this instruments); `dev/PLANNING.md` **[TRU-4]**,
the frozen-set gap recorded at `cf8bed7`.
**Plan review**: required(**Internal**) — contingent on the External proposal
review recording `Plan readiness: READY`. A **Security Review** of the
implementation is owed on its own trigger regardless of that field, because the
change adds a write path and a subprocess to a gate-frozen file.

Proposed paths:
* `bootstrap/tests/test_suite_ledger.py` -- the hook's own contract tests
* `tools/suite_cost.py` -- the reader that aggregates the ledger

Untracked paths:
* `dev/measurement/suite-runs.jsonl` -- the gitignored live ledger this writes

## Context

**The cost question has been answered by a full profiling run at least four
times, and the answer has been lost every time.** Measured `as_of 2026-08-19`:

| date | nodes | wall | conditions | where the number landed |
|---|---:|---:|---|---|
| 2026-08-04 | 1,790 | 129.7s | clean | `dependency-advisory-coverage`, archived |
| 2026-08-10 | 2,527 | 380.2s | dirty tree, 4 failures | the corpus-tier-cost proposal, archived |
| 2026-08-13 | 4,277 | 689.5s | clean, a Boundary B record | `review-efficient-lifecycle`, archived |
| 2026-08-19 | 4,468 | 568.3s | dirty tree, 7 failures | a gitignored local file |

Every one of the first three archived. `dev/measurement/README.md` calls an
archive a graveyard — *"not an archive… this folder is live measurement, not a
graveyard of finished work"* — and that is precisely what happened: the number
survived, the place to look it up did not, so the next agent re-ran an
eleven-minute suite to rediscover it.

**These four points cannot be compared, and that is the sharper problem.** The
2026-08-19 run is *faster* than 2026-08-13 while carrying 191 more tests. The
tempting reading is that optimisation caused it. That reading is wrong:
`corpus-tier-cost` archived 2026-08-11, so its gains were already inside the
2026-08-13 figure. The likeliest cause is **concurrent load** — the 2026-08-13
run competed with a second suite in another session — and *nothing in the record
captured that*. Two of the four runs were against dirty trees carrying other
sessions' edits.

So the repository cannot presently answer *"is the suite getting slower?"*, not
because it lacks numbers but because each number was transcribed by hand, for a
different purpose, without its conditions. **Four figures taken this way are not
a time series.**

**And a second quantity is invisible entirely: how often the full suite runs.**
`dev/PLANNING.md` records the one time anyone counted — a plan that budgeted two
full suites spent **thirteen**, eleven of them by delegated subagents, *"each
independently reaching for `pytest bootstrap/tests` because that is the obvious
way to answer 'did this break anything'"*. That count exists because a human
noticed and counted by hand. Nothing measures it. A budget that cannot be
observed is not a budget; it is a wish.

## Proposal

Make the suite **report its own cost on every run**, as a by-product of running,
and read the report instead of re-measuring.

### The mechanism

Extend `bootstrap/tests/conftest.py` with two hooks:

* `pytest_runtest_logreport` — accumulate `report.duration` per test file per
  phase. This is data pytest already produces; no `--durations` flag needed and
  no measurable overhead.
* `pytest_sessionfinish` — the existing function gains one call, **last**, to a
  new `_write_ledger_row(session)` helper.

The helper appends **one JSON object per session** to
`dev/measurement/suite-runs.jsonl`, carrying: UTC timestamp; HEAD SHA; a dirty-file
count; interpreter version; the normalized invocation argv; collected node count;
passed / failed / skipped / xfailed counts; total wall-clock; and per-file
durations for the twenty-five most expensive files.

### Four guards, each load-bearing

**1. Outcome-inert — the whole helper is wrapped in `except Exception`, and it
never touches `session.exitstatus`.** A diagnostics hook that can fail a suite is
strictly worse than no hook, because it fails a suite for a reason unrelated to
the code under test. It is called *last* in `pytest_sessionfinish`, after the
release-mode rule that file already carries has decided the exit code.

**2. Reentrancy — skip when we are a child session.** This is not a nicety.
Measured `as_of 2026-08-19`: **73 files in `bootstrap/tests/` spawn a nested
`pytest`, across roughly 78 invocation sites.** Without this guard, one full-suite
run would append ~78 rows, most of them from child sessions measuring fixture
repositories. The guard is the standard one: if the marker environment variable is
already set on entry we are a child and return immediately; otherwise we set it for
our own children.

**3. Containment — skip when the resolved ledger directory is under
`tempfile.gettempdir()`.** Gate tests build repositories under `tmp_path` and run
suites inside them. Those are fixtures, not this repository, and their timings
describe a synthetic tree. Defence in depth with guard 2.

**4. Release mode — skip entirely when `CAIRN_RELEASE_GATE_ACTIVE` is set.** A
release ceremony's observable behaviour should not change because a diagnostics
feature landed. This deliberately forfeits release-run data; see *Known
omissions*.

Plus an operator opt-out, `CAIRN_SUITE_LEDGER=0`, and a silent no-op when
`dev/measurement/` does not exist.

### Why the ledger is gitignored, and why that is not a compromise

An output rewritten by every run **dirties the tree on every run**, and a clean
pre/post state is a precondition of a Boundary B record (`AGENTS.md` >
*Verification boundaries*). A tracked ledger would therefore break the very
evidence discipline it exists to serve. It would also collide across the
concurrent sessions this repository routinely runs.

The live ledger is gitignored exactly as `dev/reflections/` is, and for the same
reason. `.gitignore` already carries the rule as of `3edf482`/`9e19af7`.

### Atomicity, which sets the record size

Concurrent sessions append to one file. A single `os.write()` to a descriptor
opened `O_WRONLY|O_CREAT|O_APPEND` is atomic under POSIX **only up to
`PIPE_BUF` (4096 bytes)**. That is the reason per-file durations are capped at
twenty-five entries rather than "all of them": the cap is what keeps a row from
interleaving with another session's row. It is a correctness constraint, not a
display preference.

### The reader

`tools/suite_cost.py` renders the ledger: the current cost profile, the
concentration table, the growth curve *with conditions attached*, and — the
number nobody currently has — **full-suite runs per day and per plan**.

**The rendered view is the human artifact, and comprehensibility is a
requirement on it, not a matter of taste.** The ledger itself is JSONL — one
line per session, written for a parser. Nobody should ever have to read that to
answer a question. `tools/suite_cost.py` renders it into prose and tables a
person can read cold, and the bar is concrete:

* **It states what it is and what to do with it in the first two sentences** —
  starting with the instruction not to re-run the suite, since that is the
  action it exists to prevent.
* **Every figure carries its conditions** — date, commit, interpreter, clean or
  dirty tree, and whether another suite was running. The growth table above is
  useless precisely because its figures lack these, and a renderer that repeats
  that omission has rebuilt the problem in a new place.
* **No bare identifiers.** A reader with no plan open and no reviewer to ask
  must be able to act on it (`AGENTS.md` > *Project-specific conventions*).
* **It names its own limits** — which runs are missing (release, nested), and
  what the numbers therefore cannot be used to claim.

A rendered view that only a person who already knows the suite can interpret has
failed, however accurate its arithmetic.

`tools/` is outside every frozen glob, so the reader costs no ceremony and can
evolve freely. Only the collector is frozen, which is the correct split: the
thing that runs inside every test session is anchored; the thing that reads a
local file afterward is not.

## Rationale

**The measurement should be a by-product, not an errand.** Every measurement in
the table above exists because someone decided to measure. That is why there are
four points in three weeks, why two were taken against dirty trees, and why none
recorded concurrent load. Instrumentation that runs whether or not anyone
remembers produces a different *kind* of record.

**It makes the budget observable.** Cairn's verification doctrine opens with
*"do not pay for the same broad run at every one."* That is a budget. Today it is
enforced by an agent remembering it, and `PLANNING.md` documents that memory
failing at a 6.5× overrun. A ledger does not enforce anything — but it converts
"agents seem to run the suite a lot" into a number a plan can be held to, and a
reviewer can check a claim against.

**It is measurement infrastructure, which is what this folder is for.**
`dev/measurement/README.md` reserves the slot: *"Operational ledgers that feed
the metrics… records of process incidents kept so the team can measure and
correlate them over time."*

## Alternatives considered

**A repo-root `conftest.py`.** pytest loads one on every invocation this project
uses (verified by probe 2026-08-19), and it matches **none** of the five frozen
globs — so it would cost no ceremony at all. **Rejected**, and the fact that it
would work is itself the objection: a root conftest can set `session.exitstatus`
with none of the integrity coverage that `bootstrap/tests/conftest.py` carries
precisely because a conftest decides a gate's pass/fail semantics. Taking that
route would mean *using* a gap in the gate to avoid the gate. The gap is now
recorded as `dev/PLANNING.md` **[TRU-4]** (`cf8bed7`) to be closed on its own
merits, not exploited here.

**A wrapper command** (`python tools/suite.py` in place of `python -m pytest
bootstrap/tests`). Touches no frozen file. **Rejected**: the canonical command is
written into `AGENTS.md`, `doctrine/plans.md`, the plan template and
`bootstrap/tests/test_verification_boundaries.py`, so this trades a one-time
ceremony for a permanent documentation-drift surface — and it collects nothing
when an agent types the pytest command anyway, which is exactly the population
worth measuring.

**A pytest plugin via `PYTEST_PLUGINS` / `PYTEST_ADDOPTS`.** **Rejected**: an
environment variable is per-shell and silently absent, so coverage would be
whichever sessions happened to have it set — the same selection bias the current
hand-measurement has.

**Status quo — measure on demand.** This is the alternative with four data points
in three weeks, two of them unusable for comparison. It has been tried.

## Evidence / verification plan

### Author-accounting — invariants, failure modes, edge cases

**Invariants**

| must stay true | enforced by |
|---|---|
| The hook never changes a session's exit status | a test asserting exit code parity with the hook forced to raise |
| A child session never writes a row | a test running a nested pytest and asserting row count is unchanged |
| A release-mode session never writes a row | a test setting `CAIRN_RELEASE_GATE_ACTIVE=1` and asserting no write |
| One row is at most 4096 bytes | a test constructing a worst-case row (25 longest real paths) and asserting the length |
| A row is valid JSON on one line | a round-trip parse test |

**Failure modes** — all **closed toward doing nothing**: an unwritable
directory, a full disk, a JSON-encoding failure, a `git` invocation that fails
or times out, and a missing `dev/measurement/` each result in *no row and no
other effect*. There is deliberately **no open/degrading path**, because the
value of a diagnostics row never exceeds the cost of disturbing a test result.

**Edge cases** — handled: zero collected tests; a session that errors during
collection; a session interrupted by `KeyboardInterrupt` (exit code 2 preserved);
concurrent writers; a detached HEAD; a repository with no commits. Out of scope:
Windows atomicity semantics (`O_APPEND` guarantees are POSIX; the row cap is
sized for POSIX and Windows behaviour is untested and unclaimed).

**Public-path → test mapping** — the collector's public paths are the two pytest
hooks. Both are exercised through a real pytest session (a nested run against a
fixture tree), never by calling the helper directly, in
`bootstrap/tests/test_suite_ledger.py` (a proposed path — written as a plain
reference rather than a link, because the link checker resolves targets and this
file does not exist until the plan lands).

**Known omissions** — release-mode runs are deliberately unmeasured (guard 4), so
the ledger under-counts total suite executions and can never characterise release
ceremony cost. Nested child sessions are unmeasured by design, so per-fixture
suite cost stays invisible. Windows is unclaimed. And the ledger records *that* a
run happened, never *why* — attributing a run to a plan chunk stays a human
reading of the record.

#### Security preflight — five questions

**S1 — Who supplied it?** The hook *decides* only whether to write and what to
write. Inputs: `os.environ` (the two markers), the pytest `session`/`config`
objects, `tempfile.gettempdir()`, and `git rev-parse HEAD` plus `git status
--porcelain`. **The thing being decided about — the repository under test —
supplies the git output and the file paths in the durations map.** That is
accepted because none of it is *interpreted*: paths are recorded as opaque
strings, the status output is only line-counted, and no value influences any
control-flow decision except through length capping.

**S2 — Can it fail?** Each invariant test above names its own mutation. The
load-bearing one: forcing `_write_ledger_row` to raise must leave the session's
exit code unchanged — a test that asserts this by *deleting the `try` block* is
the falsifier, and it must go red. Note the check does **not** derive its
expectation from the hook: expected exit codes come from a control run with the
hook disabled by env var.

**S3 — What fires it, over what?** Nothing "fires" it — it is a pytest hook that
runs on **every non-child, non-release session under `bootstrap/tests/`**, which
is the point: there is no selector to forget. The reader `tools/suite_cost.py`
is run by a human or by the goodnight routine. **Cairn has no CI, and nothing
here runs in one.**

**S4 — Which way does it break?** Every path lands on **less** authority: every
failure yields no row, and the guards are all *skip* conditions, so an
unrecognised state produces silence rather than a write. The one asymmetry worth
naming: guards 2 and 3 fail toward *not measuring* (a real run misclassified as a
child is silently lost), never toward writing into a fixture tree.

**S5 — Who still wins?** The change assumes an attacker who can already run
arbitrary code in the test session — which is total, since the suite executes the
repository's own code. This adds no capability such an attacker lacks; it does
add a **write to a path derived from the conftest's location**, so an attacker who
can relocate the test tree can choose where a JSON line lands. Contained by the
tempdir guard and by the row never containing attacker-chosen *content* beyond
test file paths. The class is closed **by construction** for exit-status
influence (the hook holds no reference that can alter it after the release rule
runs) and merely **by enumeration** for write-path targeting.

### Tests required

`bootstrap/tests/test_suite_ledger.py`, new, covering the five invariants above.
Standing gates for the touched surface: `bootstrap/tests/test_gate_manifest.py`
and `bootstrap/tests/test_gate_preflight.py` (the frozen surface changes),
`bootstrap/tests/test_security_check.py` (which already pins the conftest's
release-mode token pair), and `bootstrap/tests/test_python_floor.py`.

**Boundary B mode will be `full`** and the fence is not arguable here: the change
modifies a gate-frozen file and lands under a re-anchor ceremony, which is a
trust-ceremony surface on both counts.

### Examples / smoke checks

`python scripts/check_cairn.py` for the prose surfaces; a manual
`python -m pytest bootstrap/tests -q` followed by inspecting the resulting row;
and a nested-run check confirming exactly one row appears.

## Signals the change is wrong

* **The ledger disagrees with a hand-timed run** by more than a few percent —
  the accumulation is wrong; recovery is to fall back to `--durations` as the
  authority and fix or revert the collector.
* **Any suite failure is ever traced to the hook.** This is the one outcome the
  design exists to prevent; recovery is immediate revert, not repair.
* **Rows appear from fixture trees**, meaning guards 2 and 3 are both leaking —
  recovery is to disable writing until the guard is re-derived.
* **Nobody reads it after two months.** The mechanism would then be overhead
  dressed as measurement; recovery is to delete the collector and keep the
  gitignored file as a manual artifact.
* **Row cap fights the data** — if twenty-five files stop covering the expensive
  head, the suite's cost has spread out, and the concentration premise this rests
  on no longer holds.
