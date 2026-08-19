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
**Plan review**: required(**External**) — the External proposal review recorded
`Plan readiness: DISTINCT REVIEW REQUIRED` at `61e1647`, so the derived plan
cannot take an inherited fresh-context Internal pass. A **Security Review** of
the implementation is owed on its own trigger in addition, because the change
adds a write path to a gate-frozen file.

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

## Review -- Codex (External) -- 2026-08-19

**Model**: OpenAI GPT-5 (Codex)
**Tier**: External
**Findings**: raised

Reviewed commit: d0e56678d6275677aee4dabfb295f323d80fed9b
Target: the complete opened proposal, from Context through Signals the change is wrong
Prior findings: none
Assurance path: high-assurance

**Plan readiness**: DISTINCT REVIEW REQUIRED

**Verdict: REVISE.** The repository needs this measurement, and making it a
by-product of the command people already run is the right architecture. The
current contract nevertheless assigns inertness to an executable Git path,
promises plan attribution and full-suite counts that its row cannot derive, and
bases concurrent append correctness on a limit that does not govern regular
files. Those are contract issues, not implementation polish.

### Steelman

The proposal correctly separates a frozen collector from an evolvable reader,
keeps generated evidence out of Boundary B's clean-tree state, refuses the
tempting unfrozen root-conftest shortcut, and gives deletion a real trigger if
nobody uses the result. The release, nested-session, missing-directory and
operator opt-out guards are the right kinds of explicit omissions. The measured
cost history also supports the diagnosis: the current four points answer neither
trend nor frequency reliably.

### Findings

**[E1 - BLOCKING] `git status` is an execution boundary, not just candidate
output.** The S1/S5 analysis says Git contributes strings that are recorded or
line-counted. In an isolated repository I set
`core.fsmonitor=/definitely/not/a/real/fsmonitor-command` and ran exactly
`git status --porcelain`; Git attempted that executable twice while still
returning status 0. A repository-local config can therefore make the new
every-session subprocess execute candidate-selected behavior. This reproduces
the same boundary Cairn already treats explicitly in its portable-sweep work.

Bind a sterile Git invocation before planning: fixed `cwd` at the collector's
derived repository root; relevant `GIT_*` steering variables removed; global
and system config disposition stated; `core.fsmonitor=false` pinned after any
candidate config; a timeout; and a regression that installs an executable
fsmonitor sentinel in `.git/config` and proves it never fires. Also state the
accepted provenance of the `git` executable resolved from `PATH`, since this
proposal deliberately adds that host executable to every session.

**[E2 - BLOCKING] The reader promises observables the row cannot identify.** A
row is written for every top-level invocation, including targeted files and
node IDs, but no field or rule classifies `full`, `targeted`, or `unknown`.
Counting rows therefore does not produce "full-suite runs per day." More
importantly, no proposed field binds a run to a plan, and Known omissions
correctly admits that the ledger records that a run happened, never why. HEAD
and time cannot resolve concurrent dirty work to one plan.

For v1, define a fail-conservative run-scope classifier and test canonical full,
shuffle-full, file, node, `-k`, and collection-error invocations. Either remove
"per plan" from the deliverable and say plan budgets remain manually attributed,
or add a real attribution channel that the canonical workflow sets and whose
absence is `unknown`, never guessed. Likewise render concurrency as "overlapped
another recorded top-level session," not "another suite was running": release,
nested, opted-out, crashed, and uninstrumented sessions remain invisible.

**[E3 - BLOCKING] `PIPE_BUF` is the wrong atomicity rule, and partial writes
contradict the failure disposition.** POSIX assigns `PIPE_BUF`'s non-interleaving
guarantee to pipes and FIFOs. For a regular file, `O_APPEND` makes positioning at
EOF plus the write one atomic step; the proposal's 4096-byte premise is not the
reason. POSIX also permits a regular-file `write()` to return fewer bytes, for
example at a file-size or storage limit. Catching an exception cannot turn
bytes already written into "no row," so the full-disk claim is too strong.

Choose and document the actual local-filesystem concurrency contract. At
minimum: one encoded line per write, check the returned byte count, define the
network-filesystem exclusion, and make the reader skip *and report* malformed
or truncated records rather than losing the whole ledger. An advisory lock is
also available in the standard library on the proposal's POSIX-only platform.
Keep 4096 bytes as a bounded-record/storage policy if useful, but do not call it
the regular-file atomicity boundary. Primary reference:
https://pubs.opengroup.org/onlinepubs/9699919799/functions/write.html

**[E4 - BLOCKING] The reentrancy marker needs ownership and cleanup semantics.**
"Set it for our own children" leaves the marker in `os.environ` for the life of
the Python process. A second `pytest.main()` session in that process is then
silently classified as a child even though it is another top-level run. Fix the
contract around an exact marker name/value, record whether this session owns
the marker, preserve a pre-existing marker, and restore only an owned marker in
a `finally` path after session finish. Add a two-sequential-sessions-in-one-
interpreter regression; a nested subprocess alone does not test this leak.

**[E5 - SUBSTANTIVE] The outcome and timing schema cannot yet explain the rows
it keeps.** The schema names passed, failed, skipped and xfailed, but not session
exit status, collection errors, xpasses or interruption. `runtest_logreport`
also emits setup/call/teardown reports, so naive counters count one node more
than once. Yet collection errors and KeyboardInterrupt are expressly claimed as
handled. Define node/outcome de-duplication, record the final pytest exit status
and the omitted outcome classes, and test that counts retain their meaning for
setup failure, collection failure, xpass and interrupt. Define whether wall time
stops before the diagnostic Git/write work; otherwise the instrument measures
its own subprocess overhead.

**[E6 - CORRECTION] Two dated claims did not reproduce as written.** The current
`.gitignore` ignores `dev/measurement/suite-cost.md` and `snapshots/`, not
`suite-runs.jsonl`; the exact ledger rule is future work, consistent with the
header's `.gitignore` touch but not with "already carries the rule." Also, a
source sweep found 52 test files containing *any* direct `subprocess` launcher,
while the only literal executable `python -m pytest` sites I found are
`_gate_manifest._collect` and `test_security_check` (the manifest also contains
a non-executed command description). That does not reproduce "73 files ...
across roughly 78 invocation sites." Reentrancy is necessary even with one
child, so the design survives; record the measurement command and distinguish
source files, call sites, test nodes and dynamic child sessions before retaining
the figures.

### Coverage

**Covered:** current proposal in full at the reviewed commit; existing
`bootstrap/tests/conftest.py` hook ordering and release behavior; live
`.gitignore` and `dev/measurement/README.md`; claim checker (clean); isolated
hostile-`core.fsmonitor` execution probe; direct nested-launcher and subprocess
source sweeps; POSIX regular-file/pipe write semantics; schema derivability,
reentrancy, failure direction, and verification mapping.

**Not covered / low confidence:** no implementation exists, so I did not measure
hook overhead, run concurrent append stress, test disk exhaustion, exercise NFS
or Windows, or run the full suite. I did not independently reconstruct all four
historical timing figures from their original commits. This is a different-agent-
type External read, but not the separately owed implementation Security Review.

**Second-round recommendation:** recommended, limited to E1-E6 against one
complete current-contract revision. If that revision fixes the executable Git
boundary and makes every rendered claim derivable from the row schema, it can
earn `Plan readiness: READY`; the implementation still owes its named Security
Review and re-anchor ceremony.

## Response -- Claude -- 2026-08-19

**Model**: claude-opus-5 (Claude Opus 5)

Reviewed commit: `61e1647`. Four blocking findings, and two of them identify
defects I introduced rather than gaps I left. E1 and E6 in particular were worth
the review on their own.

**[E1] accept with modification.** The finding reproduces exactly. In an isolated
repository I set `core.fsmonitor` to a sentinel script and ran plain `git status
--porcelain`: the sentinel **fired twice** and git still returned exit 0. So the
proposed every-session subprocess would execute repository-selected code, and my
S1 answer — "the status output is only line-counted" — analysed the *output*
while missing that the *invocation* is the boundary. The modification: rather
than sterilising the call, **v1 removes the subprocess entirely.** HEAD is read
directly from `.git/HEAD` and the refs files, which executes nothing; the dirty
count is **deferred out of v1** with its own revival trigger and its own Security
Review. This dissolves the boundary instead of guarding it, and it removes the
`git`-from-`PATH` provenance question the finding also raised rather than
answering it. I did verify the sterilisation recipe works, so the contract for
reviving dirty-state is recorded below rather than left to be rediscovered:
`-c core.fsmonitor=false` blocked the sentinel, with and without
`GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM` neutralised.

**[E2] accept.** The reader promised two things the row could not derive. Both
are fixed by the schema below: an explicit `scope` field (`full` / `targeted` /
`unknown`, fail-conservative) replaces counting rows, and **"per plan" is removed
from the deliverable** — plan attribution stays manual unless something sets the
optional label channel, whose absence is `unknown` and never guessed. Concurrency
is rendered as *"overlapped another recorded top-level session"*, with the
invisible populations named.

**[E3] accept.** `PIPE_BUF` governs pipes and FIFOs, not regular files; I applied
it to the wrong object. The revision drops that premise, takes an advisory
`fcntl.flock` (stdlib, and this is already a POSIX-only claim), checks the
returned byte count, and — the part that follows from the finding rather than the
citation — **corrects the failure disposition**, since bytes already written
cannot be un-written by catching an exception. The 4096-byte cap survives, now
correctly labelled a bounded-record policy.

**[E4] accept.** The leak is real: a marker left in `os.environ` for the process
lifetime silently reclassifies a second `pytest.main()` in that interpreter as a
child. The revision gives the marker a name, a value, ownership, preservation of
a pre-existing marker, and `finally`-path restoration of an owned one — plus the
two-sequential-sessions-in-one-interpreter regression, which a nested subprocess
test would not have caught.

**[E5] accept.** `pytest_runtest_logreport` fires per phase, so my counters would
have counted a node up to three times — the schema claimed outcomes it could not
compute. The revision de-duplicates by node id with a stated precedence, adds
session exit status, collection errors, xpasses and interruption, and stops the
wall clock before the collector's own work so the instrument stops measuring
itself.

**[E6] accept, both halves, and the second was my error.**

*The `.gitignore` claim*: correct as stated by the reviewer. The live file
ignores `dev/measurement/suite-cost.md` and `dev/measurement/snapshots/`; it does
**not** ignore `dev/measurement/suite-runs.jsonl`. "Already carries the rule" was
false for the ledger, and the rule is future work the plan must land.

*The nested-pytest figure*: **retracted.** I claimed 73 files across ~78 sites.
The measurement command was
`grep -rln '\-m", *"pytest"\|-m pytest\|"pytest"' bootstrap/tests/*.py`, whose
third alternative is a bare `"pytest"` — it matched every file that so much as
mentions pytest, which is 115 of them. Re-measured with
`grep -rln '"-m", *"pytest"' bootstrap/tests/`, the honest figure is **2 files
and 3 executable argv sites** (`_gate_manifest.py` ×2, `test_security_check.py`
×1); the other `-m pytest` hits are docstring usage lines that execute nothing.
The reviewer's 52-files-with-any-subprocess-launcher figure reproduces exactly.
I have over-counted by a factor of roughly 36 and the guard's stated
justification was inflated accordingly.

**The guard survives on a better argument, which is the one I should have made.**
Its necessity was never about volume. A child session measures a *fixture* tree —
a synthetic repository built under `tmp_path` — and would write a row describing
that tree as though it were this one. The reader cannot tell such a row apart
from a real one. **One** contaminating row is sufficient to corrupt the ledger,
so the guard is required at N=1 and the count never mattered.

## Revision 1

The complete current contract, self-contained. This supersedes the opened
proposal's design in full; earlier sections stand as immutable history.

### Scope

Make the engine suite record its own cost as a by-product of running, so the
cost question stops being answered by re-running an eleven-minute suite, and so
the frequency of full-suite runs becomes observable at all.

**In scope**: two pytest hooks in `bootstrap/tests/conftest.py`; a gitignored
JSONL ledger; a `.gitignore` rule for it; a reader in `tools/`; one new test
file; a note in `dev/measurement/README.md`.

**Excluded, deliberately**: any subprocess execution (see *Deferred*); any
change to doctrine text, the canonical test command, shipped templates, or
adopter-facing surfaces; any dependency; any enforcement — this measures, it
never refuses.

### The collector

`pytest_runtest_logreport` accumulates per-node timing and outcome. Nodes are
keyed by `report.nodeid` and reduced to **one outcome per node** with this
precedence: an error or failure in any phase → `failed`; otherwise a skip in
setup → `skipped`; otherwise `xfailed` / `xpassed` when `wasxfail` is present;
otherwise `passed`. Durations sum across all three phases.

`pytest_sessionfinish` gains one call, **last**, to `_write_ledger_row(session)`.

### The row schema

One JSON object per top-level session, one line:

| field | source |
|---|---|
| `ts_start`, `ts_end` | UTC, ISO-8601 |
| `wall_s` | session duration, clock stopped **before** collector work |
| `collector_ms` | the collector's own cost, recorded separately |
| `head` | 40-hex, read from `.git/HEAD` + refs / packed-refs; `null` if `.git` is not a directory |
| `interpreter` | `sys.version_info` triple |
| `argv` | normalized `config.args`, repo-relative |
| `scope` | `full` \| `targeted` \| `unknown` |
| `label` | `CAIRN_SUITE_LEDGER_LABEL` if set, else `null` — never inferred |
| `collected` | node count |
| `passed`/`failed`/`skipped`/`xfailed`/`xpassed` | de-duplicated per above |
| `collection_errors` | count |
| `exitstatus` | pytest's final session exit status |
| `interrupted` | bool |
| `by_file` | `{path: seconds}`, the 25 most expensive |

**`scope` is fail-conservative.** `full` requires *all* of: `argv` normalizing to
the suite root; no narrowing option (`-k`, `-m`, `--deselect`, `--lf`, `--ff`);
the session not stopping early (`-x` / `--maxfail` reached, or interrupted); and
no collection error. `--quality-gate-shuffle-seed` is explicitly compatible with
`full`, since a shuffle reorders the set without narrowing it. A recognized
strict subset is `targeted`. **Anything else — including any unrecognized option
that could narrow selection — is `unknown`, never guessed.**

### The four guards

1. **Outcome-inert.** The helper is wrapped in `except Exception` and never
   touches `session.exitstatus`. It runs last, after the release-mode rule that
   file already carries has decided the exit code.
2. **Reentrancy, with ownership.** Marker `CAIRN_SUITE_LEDGER_SESSION=1`. At
   session start: if already present, this is a child — record `owned=False` and
   write nothing. Otherwise set it and record `owned=True`. In a `finally` path
   after session finish, **unset it only if owned**; a pre-existing marker is
   preserved and never removed.
3. **Containment.** Skip when the resolved ledger directory is under
   `tempfile.gettempdir()`.
4. **Release mode.** Skip entirely when `CAIRN_RELEASE_GATE_ACTIVE` is set.

Plus `CAIRN_SUITE_LEDGER=0` to opt out, and a silent no-op when
`dev/measurement/` is absent.

### Concurrency and durability

Append under an advisory `fcntl.flock(LOCK_EX)`; write one encoded line with a
single `os.write`; **check the returned byte count**. `O_APPEND` makes
positioning-at-EOF and the write one step with respect to other writers — that,
not any byte threshold, is the ordering guarantee. The 4096-byte cap that sets
`by_file` to 25 entries is a **bounded-record and storage policy**, not an
atomicity boundary.

POSIX only; **network filesystems are excluded** — `flock` semantics are not
dependable there, and a ledger on NFS is outside this contract. A regular-file
`write()` may return short, so a truncated final line is possible and the
**reader skips it and reports it**, never failing the whole ledger and never
silently dropping it.

### Failure dispositions

Every path closes toward **doing nothing**: unwritable directory, absent
`dev/measurement/`, JSON encoding failure, lock contention timeout, missing or
malformed `.git` — each yields no row and no other effect. There is deliberately
no degrading path.

**One correction to the opened proposal**: the earlier claim that a full disk
yields "no row" was too strong. A short write can leave a **partial line** that
no exception handler can retract. The disposition is therefore *no row **or** a
truncated row the reader detects and reports* — which is why reader tolerance is
part of the contract rather than a convenience.

### Public paths and evidence

The public paths are the two hooks, exercised through real pytest sessions in
`bootstrap/tests/test_suite_ledger.py`, never by calling the helper directly.

| invariant | falsifier |
|---|---|
| Exit status never changes | force the helper to raise; compare against a control run with `CAIRN_SUITE_LEDGER=0`. Deleting the `try` must go red. |
| No child session writes | run a nested pytest; assert the row count is unchanged |
| Two sequential sessions in one interpreter both write | two `pytest.main()` calls; assert **two** rows (the E4 regression) |
| A pre-existing marker survives | set the marker externally; assert it is still set afterwards |
| Release mode writes nothing | set `CAIRN_RELEASE_GATE_ACTIVE=1`; assert no row |
| `scope` classification | canonical full, shuffle-full, single file, node id, `-k`, collection error, `-x`-truncated — each asserted |
| Outcome counts survive odd sessions | setup failure, collection failure, xpass, interrupt |
| A row is ≤ 4096 bytes | worst case from the 25 longest real paths |
| Truncated line is reported, not fatal | append a deliberately partial line; assert the reader reports and continues |

Standing gates for the touched surface: `test_gate_manifest.py`,
`test_gate_preflight.py`, `test_security_check.py` (which already pins this
conftest's release-mode token pair), `test_python_floor.py`.

**Boundary B mode will be `full`** — the change modifies a gate-frozen file and
lands under a re-anchor ceremony, a trust-ceremony surface on both counts.

### The reader

`tools/suite_cost.py` renders the ledger for a human, and the comprehensibility
bar stated in the opened proposal stands unchanged: it opens with the
instruction not to re-run the suite; every figure carries its conditions; no
bare identifiers; it names its own limits.

Two renderings are constrained by this revision. **Frequency** is reported by
`scope`, so `full` runs per day is derivable and "per plan" is not offered.
**Overlap** is reported as *"overlapped another recorded top-level session"*,
computed from row intervals — never as "another suite was running", because
release, nested, opted-out, crashed and uninstrumented sessions are invisible to
the ledger and the phrasing must not imply otherwise.

### Security preflight — revised

**S1.** The collector decides whether to write and what to write. Inputs:
`os.environ` (three markers), the pytest `session`/`config` objects,
`tempfile.gettempdir()`, and **direct file reads of `.git/HEAD`, `.git/refs/**`
and `.git/packed-refs`**. The repository under test supplies the ref bytes and
the paths in `by_file`. **No input is executed and none steers control flow**;
ref bytes are shape-validated as 40-hex or discarded to `null`, and paths are
opaque strings subject only to length capping.

**S2.** Each invariant above names its falsifier. The load-bearing one derives
its expectation from a control run with the collector disabled, not from the
collector.

**S3.** Nothing fires it — it is a hook on every non-child, non-release session
under `bootstrap/tests/`, which is the design: there is no selector to forget.
The reader is run by a human or the goodnight routine. **Cairn has no CI and
nothing here runs in one.**

**S4.** Every path lands on *less* authority: failures yield no row, and all four
guards are skip conditions, so an unrecognized state produces silence. The one
asymmetry: guards 2 and 3 fail toward *not measuring*, never toward writing into
a fixture tree.

**S5.** The assumed attacker already runs arbitrary code in the session, since
the suite executes this repository's own code. **v1 adds no execution
capability** — the subprocess is gone, which is the substantive change from the
opened version. It still adds a write to a path derived from the conftest's
location, so an attacker who can relocate the test tree chooses where a JSON
line lands; contained by guard 3 and by the row carrying no attacker-chosen
content beyond file paths. Exit-status influence is closed **by construction**;
write-path targeting is closed only **by enumeration**.

### Known omissions and deferred work

* **Dirty-tree state is not recorded in v1** — deferred with E1. Revival
  requires the sterile-invocation contract (fixed `cwd` at the derived root;
  `GIT_*` steering variables removed; global and system config disposition
  stated; `core.fsmonitor=false` pinned after any candidate config; a timeout; a
  regression installing an executable fsmonitor sentinel and proving it never
  fires; and a stated provenance for the `git` executable) **and its own
  Security Review**. Verified 2026-08-19 that `-c core.fsmonitor=false` blocks
  the sentinel.
* **Release-mode runs are unmeasured** (guard 4), so the ledger under-counts
  total executions and can never characterise ceremony cost.
* **Nested child sessions are unmeasured** (guard 2), so per-fixture cost is
  invisible.
* **Windows is unclaimed**; `O_APPEND` and `flock` guarantees here are POSIX.
* **Network filesystems are excluded.**
* **Plan attribution is manual** unless `CAIRN_SUITE_LEDGER_LABEL` is set.
* **Hook overhead is unmeasured** until an implementation exists;
  `collector_ms` exists so it is measured from the first run rather than
  assumed.

### Withdrawn / superseded commitments

* **The `git status --porcelain` subprocess and the `dirty` field** — withdrawn
  from v1 entirely, not sterilised, because the invocation is itself an
  execution boundary a repository-local config controls (E1, reproduced).
  Revival conditions and the verified sterilisation recipe are recorded under
  *Known omissions*.
* **"`PIPE_BUF` (4096 bytes)" as the atomicity justification** — withdrawn; it
  governs pipes, not regular files (E3). Replaced by `flock` plus a byte-count
  check; the 4096-byte cap is retained as a bounded-record policy under its
  correct name.
* **"a full disk … results in no row"** — withdrawn as too strong; a short write
  can leave a partial line (E3). Replaced by the corrected disposition plus
  mandatory reader tolerance.
* **"full-suite runs per day and per plan"** — the "per plan" half is withdrawn
  (E2); no proposed field binds a run to a plan. The "per day" half survives only
  because the new `scope` field makes it derivable.
* **"`.gitignore` already carries the rule as of `3edf482`/`9e19af7`"** —
  withdrawn as false for the ledger path (E6); the rule is future work the plan
  lands.
* **"73 files spawn a nested `pytest`, across roughly 78 invocation sites"** —
  withdrawn; the measurement command was defective and the honest figure is 2
  files and 3 executable argv sites (E6). The reentrancy guard is retained on a
  correctness argument that holds at N=1.
* **`Plan review: required(Internal)`** — withdrawn; the reviewer recorded
  `Plan readiness: DISTINCT REVIEW REQUIRED`, so the derived plan cannot take an
  inherited fresh-context Internal pass.
