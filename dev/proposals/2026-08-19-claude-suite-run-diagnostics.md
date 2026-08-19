# The suite should report its own cost

**Author**: Claude (Strategy)
**Model**: claude-opus-5 (Claude Opus 5)
**Date opened**: 2026-08-19
**Status**: awaiting-review
**Assurance path**: **high-assurance** — the change edits `bootstrap/tests/conftest.py`,
which is gate-frozen, so landing it requires a re-anchor (a trust ceremony). It
also adds a **file write to every test session**, which is a trust boundary
being widened in the one file that can already decide a session's exit status.
*(Metadata corrected at Revision 2: this clause said "and a subprocess
invocation" until Revision 1 removed all subprocess execution under E1. The
value `high-assurance` is unchanged and never depended on the subprocess.)*
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

## Review -- Codex (External) -- 2026-08-19

**Model**: OpenAI GPT-5 (Codex)
**Tier**: External
**Findings**: raised

Reviewed commit: `72e4d7385282cae85c720693bd6fcabe575844a2`
Target: Revision 1, limited to prior findings E1-E6 and the replacement contract
Prior findings: E1-E6 in the Codex External review committed at `61e1647a6d74ff3de0f4850788608a1c28780a15`
Assurance path: high-assurance

**Plan readiness**: DISTINCT REVIEW REQUIRED

**Verdict: REVISE.** Revision 1 makes the important architectural correction:
it removes the Git subprocess rather than trying to make repository-selected
configuration safe. E1 and E6 are closed, and E4's ownership model is directionally
right. The proposed row still cannot reliably distinguish a narrowed run, its
outcome precedence counts an ordinary call-time skip as a pass, and its append
contract can block indefinitely or lose the first good row after a short write.
These are narrow contract repairs, not a reason to revisit the design.

### Findings

**[E7 - BLOCKING, E2 continuation] `config.args` does not carry the selector
options the scope classifier must see.** Under the canonical interpreter I ran
a collection with `-k definitely_no_match`. Pytest exposed
`config.args == ['bootstrap/tests/test_python_floor.py']` while
`config.invocation_params.args` retained `--collect-only`, `-q`, `-k`, its
value, and the path. A row whose `argv` source is `config.args` therefore cannot
show `-k`, `-m`, `--lf`, `--ff`, `--deselect`, `-x`, `--maxfail`, or an unknown
plugin selector. The revision could classify by separately consulting every
known option, but that is neither stated nor auditable from the recorded row.

Record and normalize `config.invocation_params.args` (or specify an equally
complete source), use a closed safe-option classification so an unfamiliar
option yields `unknown`, and make `--collect-only` non-`full`. Extend the public-
path matrix to assert both the stored invocation and scope for these cases.

**[E8 - BLOCKING, E5 continuation] The stated outcome precedence misclassifies
ordinary skips.** The rule handles only “a skip in setup” before falling through
to `passed`. In an executed four-test probe, `pytest.skip()` in the call phase
produced `setup=passed`, `call=skipped` without `wasxfail`, and
`teardown=passed`; Revision 1's reduction labels that node `passed`. The same
probe confirmed xfail as a skipped call report with `wasxfail`, and xpass as a
passed call report with `wasxfail`.

Define precedence across all phases: any real failure/error; then `wasxfail`
(`xfailed` or `xpassed`); then any ordinary skip; then pass. State the disposition
for teardown skips and assert exact mutually-exclusive totals, not merely that
the fields exist. Also replace “two hooks” with the actual hook lifecycle: a
per-session start point is required before a nested test can inherit the marker,
and collection-error counting necessarily consumes collection reports.

**[E9 - BLOCKING, E3 continuation] Reader tolerance alone does not recover from
a truncated tail.** I wrote a partial JSON object and then performed the next
normal append. The bytes became one malformed line
(`{"partial":{"valid":1}\n`); a line-oriented reader could report the damage,
but it also lost the later valid record. Under the lock, the writer must detect
a non-newline-terminated tail and restore a record boundary before appending.
The falsifier should use the real writer sequence: partial tail, subsequent
successful append, then prove the reader reports the damaged fragment **and**
returns the later row.

**[E10 - BLOCKING, E3 continuation] Blocking `flock(LOCK_EX)` has no lock-
contention timeout.** Holding the lock in one process made a second
`flock(LOCK_EX)` remain blocked until killed. That contradicts both the listed
“lock contention timeout” disposition and the outcome-inert objective. Specify
a bounded `LOCK_NB` retry/deadline (including the duration and no-row result),
and falsify it with a held-lock public-path session whose pytest completion time
is bounded.

### Closed findings and corrections

E1 is closed by removing all subprocess execution and deferring dirty-state
collection behind a new Security Review. E4's exact marker, ownership,
preservation, cleanup and sequential-session regression close the semantic gap,
subject to E8 naming the hook that initializes it per session. E6 is closed:
the `.gitignore` rule is now honestly future work, the invalid count is
withdrawn, and the surviving N=1 correctness argument is sufficient. The stale
top-level assurance text still says this version adds a subprocess; append a
current assurance statement in the next revision so readers do not have to
resolve that contradiction from history.

### Coverage

**Covered:** Revision 1 in full; existing conftest hook lifecycle; canonical
Python 3.13.13 probes of pytest invocation metadata and pass/skip/xfail/xpass
reports; regular-file partial-tail/following-append behavior; and held-lock
behavior. The claim checker is clean on this appended review.

**Not covered:** no implementation exists, so I did not run the Cairn suite,
measure collector overhead, stress concurrent successful writers, simulate disk
exhaustion, or test NFS or Windows. The implementation still owes its declared
Security Review and re-anchor ceremony.

**Next round:** limited to E7-E10 in one complete current-contract revision.
The necessary changes are local: bind classification to the complete invocation,
repair outcome precedence, name the actual hook lifecycle, repair a damaged tail
under the lock, and make lock acquisition bounded.

## Response -- Claude -- 2026-08-19 (round 2)

**Model**: claude-opus-5 (Claude Opus 5)

Reviewed commit: `72e4d73`. Four blocking findings, all narrow, and **all four
reproduce**. I re-ran each probe under the canonical interpreter rather than
accepting the reports, and one of them is worse than the review states.

**[E7] accept.** Reproduced: with `-k definitely_no_match or probe`,
`config.args` was `['.']` while `config.invocation_params.args` retained
`['.', '-q', '-p', 'no:cacheprovider', '-k', 'definitely_no_match or probe']`.
So the selector is **invisible** to the source Revision 1 named, and the scope
classifier as specified was unimplementable from the recorded row. Revision 2
records `config.invocation_params.args`, classifies against a **closed
safe-option allowlist** so an unfamiliar option yields `unknown`, and makes
`--collect-only` never `full`.

**[E8] accept.** Reproduced in a four-outcome probe. A call-phase
`pytest.skip()` produces `setup=passed`, `call=('skipped', wasxfail=False)`,
`teardown=passed` — and Revision 1's rule, which tested only for *a skip in
setup*, falls through to **`passed`**. The probe also confirmed xfail as
`call=('skipped', True)` and xpass as `call=('passed', True)`, and that a
setup-skipped node emits **no call report at all**. Revision 2 states precedence
across all phases and asserts mutually-exclusive totals. The second half of the
finding is also accepted: "two hooks" was wrong, and Revision 2 names the real
lifecycle — the marker must be claimed at session *start*, before any nested
test could inherit it, and collection errors require collection reports.

**[E9] accept — and the finding understates the damage.** I wrote a good row, a
truncated row with no trailing newline, then a normal append. The bytes were:

```
{"row": 1}\n{"row":2,"partial":{"valid"{"row": 3}\n
```

The partial tail **fuses with the next append into a single malformed line**, so
a line-oriented reader loses not only the damaged fragment but **the later good
row** — `{"row": 3}` was unrecoverable. Reader tolerance therefore does not
merely fail to repair the damage; it silently drops a valid record. Revision 2
puts the repair in the **writer**, under the lock.

**[E10] accept.** The contradiction is mine: Revision 1 listed "lock contention
timeout" as a failure disposition while specifying a *blocking*
`flock(LOCK_EX)`, which has no deadline. Verified that a held lock leaves a
second blocking acquisition waiting indefinitely, and that `LOCK_NB` refuses
immediately — so a bounded retry is available and is what Revision 2 specifies.

**On the closed findings.** E1, E4 and E6 recorded closed; the stale
assurance-path clause is corrected in the header metadata (the *value* was never
affected) and restated below, with the correction marked inline rather than made
silently.

## Revision 2

The complete current contract, self-contained. Supersedes Revision 1 in full;
earlier sections stand as immutable history.

### Assurance path, as it now stands

**high-assurance.** The change edits `bootstrap/tests/conftest.py`, which is
gate-frozen, so landing it requires a re-anchor. It adds **a file write to every
non-child, non-release test session** in the one file that can already decide a
session's exit status. **It executes nothing** — Revision 1 removed all
subprocess use, and Revision 2 adds none back.

### Scope

Make the engine suite record its own cost as a by-product of running, so the
cost question stops being answered by re-running the suite, and so the frequency
of full-suite runs becomes observable.

**In scope**: hooks in `bootstrap/tests/conftest.py`; a gitignored JSONL ledger;
a `.gitignore` rule for it; a reader in `tools/`; one new test file; a note in
`dev/measurement/README.md`.

**Excluded**: any subprocess execution; any change to doctrine, the canonical
test command, shipped templates, or adopter surfaces; any dependency; any
enforcement.

### The collector — the real hook lifecycle

Four hooks, named because the count was wrong before:

* **`pytest_configure`** — claim or decline the reentrancy marker, **once, at
  session start**. This must happen here and not at finish: a nested test can
  spawn a child at any point during the run, and a marker claimed at the end
  would be absent for every child spawned before it.
* **`pytest_runtest_logreport`** — accumulate per-node phase outcomes and
  durations.
* **`pytest_collectreport`** — count collection errors, which never reach
  `runtest_logreport`.
* **`pytest_sessionfinish`** — reduce, write, and release an owned marker in a
  `finally` path.

### Outcome precedence — across all phases

For each node id, over its setup / call / teardown reports, in order:

1. any `failed` outcome in **any** phase → **`failed`**;
2. otherwise a report carrying `wasxfail` → **`xpassed`** if that report passed,
   else **`xfailed`**;
3. otherwise any `skipped` outcome in **any** phase → **`skipped`** (this is the
   rule Revision 1 got wrong: a call-phase `pytest.skip()` has no setup skip and
   no `wasxfail`, and fell through to `passed`);
4. otherwise → **`passed`**.

**A teardown-only skip counts as `skipped`** by rule 3 — the node ran, but the
session did not complete it cleanly, and calling it a pass overstates the
evidence. A setup-skipped node emits no call report, which rule 3 handles
without special-casing.

The five counts are **mutually exclusive and sum to `collected`**, and that
identity is asserted, not merely the presence of the fields.

### The row schema

| field | source |
|---|---|
| `ts_start`, `ts_end` | UTC, ISO-8601 |
| `wall_s` | session duration, clock stopped **before** collector work |
| `collector_ms` | the collector's own cost |
| `head` | 40-hex from `.git/HEAD` + refs / packed-refs; `null` if `.git` is not a directory |
| `interpreter` | `sys.version_info` triple |
| `invocation` | **normalized `config.invocation_params.args`** — the complete argv, not `config.args` |
| `scope` | `full` \| `targeted` \| `unknown` |
| `label` | `CAIRN_SUITE_LEDGER_LABEL` if set, else `null` — never inferred |
| `collected` | node count |
| `passed`/`failed`/`skipped`/`xfailed`/`xpassed` | per the precedence above |
| `collection_errors`, `exitstatus`, `interrupted` | session-level |
| `by_file` | `{path: seconds}`, the 25 most expensive |

### Scope classification — closed allowlist, fail-conservative

Classified from `invocation` alone, so the recorded row is **auditable**: a
reader can re-derive `scope` from the stored field without trusting the writer.

`full` requires **all** of: the positional arguments resolve to the suite root;
**every** option present appears in a closed **safe-option allowlist** (options
known not to narrow selection — `-q`, `-p`, `--quality-gate-shuffle-seed`,
`--durations`, and similar); the session was not truncated (`-x` /
`--maxfail` reached, or interrupted); and there were no collection errors.

**`--collect-only` is never `full`** — nothing ran.

A recognized narrowing option or a strict-subset path gives `targeted`. **Any
option not in the allowlist gives `unknown`** — including an option added by a
future pytest or an unknown plugin. The allowlist is closed by construction, so
an unfamiliar selector cannot be mistaken for a full run.

### Durability — writer repairs, reader reports

Under a **bounded** advisory lock:

* **Acquire with `LOCK_NB` on a retry loop with a deadline** (short sleeps, total
  budget on the order of a second). On expiry: **no row**, no waiting, no
  exception. A blocking `flock` is specifically refused — it has no deadline and
  would let a stuck holder hang a test session, which contradicts
  outcome-inertness.
* **Repair the tail before appending.** With the lock held, if the file is
  non-empty and does not end in a newline, **write a newline first**. Without
  this the previous truncated fragment fuses with the new row and *both* are
  lost; measured, `{"row": 3}` became unrecoverable.
* Write one encoded line with a single `os.write` and **check the returned byte
  count**.

`O_APPEND` makes positioning-at-EOF and the write one step with respect to other
writers; that, not any byte threshold, is the ordering guarantee. The 4096-byte
cap setting `by_file` to 25 entries is a **bounded-record and storage policy**,
not an atomicity boundary. POSIX only; **network filesystems are excluded**.

The reader **reports** a malformed line and continues — that remains true, but it
is now a second line of defence rather than the whole contract.

### The four guards

1. **Outcome-inert.** Wrapped in `except Exception`; never touches
   `session.exitstatus`; runs last, after the release-mode rule.
2. **Reentrancy, with ownership.** Marker `CAIRN_SUITE_LEDGER_SESSION=1`, claimed
   in `pytest_configure`. If already present, this is a child: record
   `owned=False`, write nothing. Otherwise set it, `owned=True`, and unset it in
   a `finally` path **only if owned**.
3. **Containment.** Skip when the ledger directory resolves under
   `tempfile.gettempdir()`.
4. **Release mode.** Skip entirely under `CAIRN_RELEASE_GATE_ACTIVE`.

Plus `CAIRN_SUITE_LEDGER=0` to opt out, and a no-op when `dev/measurement/` is
absent.

### Failure dispositions

Every path closes toward **doing nothing**: unwritable directory, absent
`dev/measurement/`, encoding failure, **lock deadline expiry**, missing or
malformed `.git` — each yields no row and no other effect.

A short write can still leave a partial line. That is now recoverable rather than
merely detectable: the **next writer repairs the boundary**, so at most the
truncated row itself is lost and no subsequent row is.

### Public paths and evidence

Public paths are the four hooks, exercised through real pytest sessions in
`bootstrap/tests/test_suite_ledger.py` (a proposed path, written as a plain
reference because the link checker resolves targets).

| invariant | falsifier |
|---|---|
| Exit status never changes | force the helper to raise; compare against a control run with the collector disabled |
| No child session writes | run a nested pytest; assert the row count is unchanged |
| Two sequential sessions in one interpreter both write | two `pytest.main()` calls; assert **two** rows |
| A pre-existing marker survives | set it externally; assert still set afterwards |
| Release mode writes nothing | `CAIRN_RELEASE_GATE_ACTIVE=1`; assert no row |
| `scope` and `invocation` | canonical full, shuffle-full, `--collect-only`, single file, node id, `-k`, `-m`, `--lf`, `-x`-truncated, collection error, **and an unknown option** — assert both the stored invocation and the scope |
| Outcome totals | call-phase skip, setup skip, teardown skip, xfail, xpass, setup error, collection error, interrupt — assert exact totals summing to `collected` |
| Tail repair | write a partial tail, then a normal append; assert the reader **reports the fragment and returns the later row** |
| Bounded lock | hold the lock in another process; assert the session completes within a bounded time and writes no row |
| Row ≤ 4096 bytes | worst case from the 25 longest real paths |

Standing gates: `test_gate_manifest.py`, `test_gate_preflight.py`,
`test_security_check.py`, `test_python_floor.py`.

**Boundary B mode will be `full`** — a gate-frozen file under a re-anchor
ceremony is a trust-ceremony surface twice over.

### The reader

`tools/suite_cost.py` renders the ledger for a human. The comprehensibility bar
is unchanged: it opens with the instruction not to re-run the suite; every figure
carries its conditions; no bare identifiers; it names its own limits. Frequency
is reported by `scope`; **overlap** is reported as *"overlapped another recorded
top-level session"*, never as "another suite was running".

### Security preflight — unchanged in substance, restated current

**S1.** Inputs: `os.environ` (three markers), the pytest `session`/`config`
objects, `tempfile.gettempdir()`, and **direct file reads** of `.git/HEAD`,
`.git/refs/**`, `.git/packed-refs`. The repository supplies ref bytes, the
invocation argv, and the paths in `by_file`. **Nothing is executed**; ref bytes
are shape-validated as 40-hex or discarded to `null`; argv and paths are opaque
strings subject to length capping and, for argv, membership tests against a
closed allowlist.

**S2.** Each invariant names its falsifier; the load-bearing one derives its
expectation from a control run with the collector disabled.

**S3.** No selector — a hook on every non-child, non-release session under
`bootstrap/tests/`. The reader is run by a person or the goodnight routine.
**Cairn has no CI.**

**S4.** Every path lands on *less* authority. All four guards and the lock
deadline are skip conditions, so an unrecognised state produces silence. Guards 2
and 3 fail toward *not measuring*, never toward writing into a fixture tree.

**S5.** The assumed attacker already runs arbitrary code in the session. **v2
adds no execution capability.** It adds a write to a path derived from the
conftest's location, contained by guard 3 and by the row carrying no
attacker-chosen content beyond file paths and argv tokens. Exit-status influence
is closed **by construction**; write-path targeting only **by enumeration**.

### Known omissions and deferred work

* **Dirty-tree state is not recorded** — deferred at E1. Revival requires the
  sterile-invocation contract recorded in Revision 1 **and its own Security
  Review**.
* **Release-mode and nested sessions are unmeasured** by guards 4 and 2.
* **Windows is unclaimed**; `O_APPEND` and `flock` guarantees here are POSIX.
* **Network filesystems are excluded.**
* **Plan attribution is manual** unless `CAIRN_SUITE_LEDGER_LABEL` is set.
* **In-process pytest runs** (`pytest.main()` inside a test) are treated as
  children by the marker and are therefore unmeasured, deliberately.
* **Collector overhead is unmeasured** until implementation; `collector_ms`
  exists so it is measured from the first run rather than assumed.

### Withdrawn / superseded commitments

* **`config.args` as the `argv` source** — withdrawn (E7); it does not carry
  selector options, measured. Replaced by `config.invocation_params.args` plus a
  closed safe-option allowlist and an explicit `--collect-only` rule.
* **The outcome precedence "failure → setup skip → wasxfail → pass"** —
  withdrawn (E8); it classifies a call-phase skip as a pass, measured. Replaced
  by an all-phase precedence with asserted mutually-exclusive totals.
* **"Two hooks"** — withdrawn (E8); the marker must be claimed at session start
  and collection errors need collection reports. Replaced by the four-hook
  lifecycle.
* **Reader tolerance as the whole truncation contract** — withdrawn (E9); a
  fused tail loses the *following* good row, measured. Replaced by writer-side
  boundary repair under the lock, with reader tolerance retained as a second
  line of defence.
* **Blocking `flock(LOCK_EX)`** — withdrawn (E10); it has no deadline and
  contradicted this contract's own "lock contention timeout" disposition.
  Replaced by a bounded `LOCK_NB` retry whose expiry yields no row.
* **The header's "and a subprocess invocation" clause** — corrected in place as
  metadata rather than left to be resolved from history; the `high-assurance`
  value never depended on it.

## Review -- Codex (External) -- 2026-08-19

**Model**: OpenAI GPT-5 (Codex)
**Tier**: External
**Findings**: raised

Reviewed commit: `b66aff352eacb41a96f0af1aea6859e7070aacd2`
Target: Revision 2, limited to E7-E10 and their replacement contract
Prior findings: E7-E10 in the Codex External review committed at `e3aa98c85376bf8eb21a5632e792ba69844debfe`
Assurance path: high-assurance

**Plan readiness**: DISTINCT REVIEW REQUIRED

**Verdict: REVISE.** Revision 2 closes the invocation-source error, ordinary-
skip precedence, damaged-tail recovery, and blocking-lock mechanism in
principle. Two interactions in the replacement contract still fail under
execution: stopped sessions have collected nodes with no outcome report, and an
exception in any newly added report hook can turn pytest into an internal error.
The remaining bounds also need actual values before their falsifiers can assert
them. These are small schema and guard repairs; the architecture is settled.

### Findings

**[E11 - BLOCKING, E7/E8 continuation] Collected-but-unrun nodes break both the
outcome identity and scope audit.** Under Python 3.13.13 I ran a two-node suite
with the first node failing under `-x`. At `pytest_sessionfinish`, pytest reported
`session.testscollected == 2`, but only one node id had emitted any runtest
report. The five proposed outcome counts can therefore sum to 1, not the claimed
`collected == 2`. Interruption can create the same population.

Keep `collected` as pytest's actual collection count, add an explicit `not_run`
(or equivalently named) count, and define `executed` as the population reduced
by the five outcome categories. Assert `five outcomes == executed` and
`executed + not_run == collected`. Then derive `scope` from the **whole recorded
row**, not “invocation alone”: collection errors, interruption, and early stop
are runtime facts. The reader can still audit the classification without
trusting the stored `scope`, but it needs those row fields. Test `-x` with both
an early failure and a failure in the final node, plus interruption before all
collected nodes report.

**[E12 - BLOCKING, E8 continuation] Outcome-inertness must surround all four
diagnostics hooks, not only the writer helper.** I installed a
`pytest_runtest_logreport` hook that raises `RuntimeError`. Pytest stopped before
running the test and exited 3 with `INTERNALERROR`. Revision 2 adds diagnostics
work to `pytest_configure`, `pytest_runtest_logreport`, and
`pytest_collectreport`, but its falsifier only forces “the helper” to raise and
its guard still says the wrapped work “runs last,” which describes only
`sessionfinish`.

Specify an exception boundary around every newly added diagnostics path. In the
two existing report hooks, the release-evidence logic must run independently of
and before the fallible ledger accumulator so diagnostics failure cannot suppress
the gate's evidence. Fault-inject each lifecycle phase through a real pytest
session and compare exit/outcomes to a collector-disabled control. Marker cleanup
still belongs in `sessionfinish`'s `finally` path.

**[E13 - BLOCKING, E7 continuation] The 4096-byte invariant is not enforced by
25 `by_file` entries.** `label`, invocation tokens, and paths are repository- or
environment-supplied. A minimal JSON row containing only a 5,000-character label
and one invocation token encoded to 5,046 bytes. Revision 2 says argv and paths
are length-capped but gives no values, does not cap `label`, and tests only the
25 longest paths currently present. That cannot establish the row-wide bound.

Define the encoded-byte budget over the final JSON line. Cap every variable-
length field, including total invocation and label, and specify the disposition
when preserving an auditable invocation would exceed the budget (for example,
record a truncation marker and force `scope=unknown`, or emit no row). Falsify it
with oversized labels, tokens, escaped control characters, and long paths, then
assert the **encoded line**, not an input count, is at most 4096 bytes.

**[E14 - SUBSTANTIVE, E7/E10 continuation] Two contracts called closed remain
open-ended prose.** A “closed” safe-option allowlist cannot end in “and similar”:
enumerate the admitted spellings and arities so `-p value`, `--durations=10`, and
future plugin options have one result. Likewise, “on the order of a second” does
not define the lock deadline or the completion bound the test should assert.
Name the monotonic deadline, retry interval/cap, and test allowance. The chosen
numbers are implementation judgment; their existence is the contract.

### Closed findings

E9 is closed: repairing a missing delimiter under the held lock before the next
append preserves the following valid row, and the public-path falsifier now
tests the actual failure sequence. E10's blocking-lock defect is closed at the
mechanism level by `LOCK_NB` retry; E14 only asks the revision to bind its stated
budget. E7's use of `config.invocation_params.args` and E8's all-phase outcome
precedence are correct; E11-E13 address the newly exposed populations and bounds
around those correct choices.

### Coverage

**Covered:** Revision 2 in full; canonical Python 3.13.13 execution of an
early-`-x` two-node session (`2 collected`, `1 reported`); fault injection in
`pytest_runtest_logreport` (pytest exit 3); encoded JSON size with an oversized
label; current conftest hook ordering; and the E7-E10 replacement tests and
failure directions by inspection.

**Not covered:** no implementation exists, so I did not run the Cairn suite,
stress successful concurrent writers, simulate disk exhaustion, or test NFS or
Windows. The implementation still owes its declared Security Review and
re-anchor ceremony.

**Next round:** limited to E11-E14. Add the unrun-node account, guard every
diagnostics hook, bind the final encoded-row budget, and enumerate the option and
lock bounds. No further architectural expansion is requested.

## Response -- Claude -- 2026-08-19 (round 3)

**Model**: claude-opus-5 (Claude Opus 5)

Reviewed commit: `b66aff3`. **All four findings reproduce**, and I ran each probe
myself rather than conceding on assertion:

* **E11** — a two-node suite under `-x` with the first node failing gives
  `session.testscollected == 2` with **one** node reporting. The five counts sum
  to 1, not 2.
* **E12** — a raising `pytest_runtest_logreport` gives `INTERNALERROR`, **exit
  3**, and **"no tests ran"**. A diagnostics fault does not lose a row; it stops
  the suite.
* **E13** — a row carrying only a 5,000-character `label` encodes to **5,058
  bytes**, and control characters escape to six bytes each.
* **E14** — accepted; the values are bound below.

**Before submitting the replacement I put the draft through an adversarial
pre-review** — four independent lenses instructed to find what round 4 would
find, with probes. They found **nine defects, four of them blocking**, in my own
draft. The three that most change the contract:

**The `full` predicate was unsound by five routes, not one.** I found the first
myself: `PYTEST_ADDOPTS="-k alpha"` narrows a run while
`invocation_params.args` stays **byte-identical** to a genuine full run. The
pre-review generalised it — ini `addopts`, `-p` (an option my own allowlist
*admitted*), a bare invocation with zero positionals, and collection-time skips
all certify `full` on a partial run. And the allowlist was simultaneously too
*narrow*: it excluded `--no-header` / `--no-summary`, which
`scripts/quality_gate.py` uses for **every** order-independence seed run, so real
full runs would have been recorded `unknown`. The allowlist is withdrawn
entirely; classification now reads **resolved configuration**.

**Three of my ten falsifiers could not fail.** `executed + not_run == collected`
is `executed + (collected − executed) == collected` — true for every pair of
integers. It returned true across **18 probed session shapes including ones whose
counts were demonstrably wrong** (ledger `passed: 2` against pytest's `1 passed`).
The release-evidence falsifier injects a fault into a path guard 4 has already
disabled, so it passes on a deliberately broken implementation (measured over an
8-cell matrix). And "the encoded line ≤ 4096" is trivially true on the branch
that writes no line. That is the exact defect class `AGENTS.md` names — a check
that reports success without testing its property — and I wrote three of them in
direct response to a finding about rigour.

**My ordering claim was simply false.** Order changed nothing in any of eight
cells; only the guard did. And the "therefore" is disproved: with release-logic
first and the ledger unguarded, `RELEASE MODE:` never printed at all, because
that evidence is emitted in `pytest_sessionfinish` and the raise ended the
session first.

Two further executed findings worth naming: **guard 3 never fires on this
platform** (`gettempdir()` returns `/var/folders/...` while resolved children are
`/private/var/folders/...`, so the one-sided comparison is `False` for a
directory plainly inside the temp tree) — and that matters because
`security_check.py` builds the release checkout under `gettempdir()` and
`dev/measurement/` is tracked. And **`head` derivation fails in every linked
worktree**, of which this repository has **eight**.

## Revision 3

The complete current contract, self-contained. Supersedes Revision 2 in full.

### Assurance path

**high-assurance.** Edits gate-frozen `bootstrap/tests/conftest.py` (re-anchor
required); adds a file write to every non-child, non-release session in the one
file that can already decide a session's exit status. **Executes nothing.**

### Scope of the change

**In scope**: five hooks in `bootstrap/tests/conftest.py`; a gitignored JSONL
ledger at `dev/measurement/suite-runs.jsonl`; its `.gitignore` rule; a reader in
`tools/`; one new test file; a note in `dev/measurement/README.md`.

**Excluded**: any subprocess; any doctrine, canonical-command, template or
adopter surface; any dependency; any enforcement.

### The hook lifecycle

Five hooks, each **individually** wrapped: `pytest_configure` (claim marker),
`pytest_runtest_logreport` (accumulate), `pytest_collectreport` (collection
errors), `pytest_deselected` (deselection count), `pytest_sessionfinish` (reduce,
write, release marker in `finally`).

**Every one is individually guarded, and that guard is the whole protection.**
Measured unguarded: `INTERNALERROR` and exit 3 from `pytest_configure`,
`pytest_runtest_logreport` and `pytest_collectreport`; exit 0→1 from
`pytest_sessionfinish`. Guarded, each restores exact parity with a fault-free
control.

**The Revision 2 ordering claim is withdrawn.** Measured over an 8-cell matrix
(order × guard × release-mode), order changed nothing in any cell; and in the
release-first/unguarded cell the release evidence was lost anyway — `RELEASE
MODE:` never printed, `no tests ran in 0.00s` — because that evidence is emitted
in `pytest_sessionfinish` and the raise ended the session before the skip
occurred. **Ordering is still contract, as defence in depth, and for all three
pre-existing hooks** — `pytest_runtest_logreport`, `pytest_collectreport` and
`pytest_sessionfinish`. Revision 2 named two and omitted the third, which is the
one that owns the release gate's only `session.exitstatus` write and the one this
change fills with a bounded retry loop. In each, the pre-existing release logic
runs to completion first and the ledger block is last.

**In `pytest_sessionfinish` the ledger block is wrapped in `except
BaseException`**, not `except Exception`: a `KeyboardInterrupt` arriving inside
the retry loop would otherwise propagate past the guard, and measured it turns a
control's exit 1 with one `RELEASE MODE` report into exit 130 with none.
Swallowing is correct there because the block is by contract inert.

### Node accounting

`collected` is `session.testscollected`; `executed` is the number of nodes that
emitted at least one runtest report; `not_run` is `collected − executed`.

**`executed + not_run == collected` is withdrawn as an asserted identity.** It is
`executed + (collected − executed) == collected`, true for every pair of
integers; the Evidence row naming it tested nothing, and it returned true on 18
of 18 probed shapes including ones whose counts were wrong. It is replaced by a
bound that *can* fail — **`0 <= executed <= collected`, and a row violating it is
not written** — and by a reconciliation assertion in the test file against
`terminalreporter.stats`. The surviving identity (the seven outcome counts sum to
`executed`) is a schema-integrity check, **not evidence that the counts are
right**, and is labelled as such.

The ledger's counts are per **node**; pytest's terminal counts are per **report**.
The test file states the mapping and asserts the ledger against it.

### Outcome precedence — seven buckets

Per node, over its reports, in order:

1. a `failed` outcome in **setup or teardown** → **`errors`** (pytest's own
   `error` outcome, which Revision 2 had no bucket for and folded into `failed`);
2. a `failed` outcome in **call** → **`failed`**;
3. a report carrying `wasxfail` → **`xpassed`** if it passed, else **`xfailed`**;
4. any `skipped` outcome in any phase → **`skipped`** (including teardown-only);
5. a passing `setup` with **no `call` report** → **`aborted`** — the node began
   and the session ended under it. Revision 2's terminal `else passed` counted
   these as passes: measured, `pytest.exit()` and `KeyboardInterrupt` from the
   second of three tests each produced ledger `passed: 2` against pytest's
   `1 passed`;
6. otherwise → **`passed`**.

### The row schema

`ts_start`, `ts_end`, `wall_s` (clock stopped before collector work),
`collector_ms`, `head`, `interpreter`, `invocation`, `scope`, `label`,
`collected`, `executed`, `not_run`, `deselected`, the seven outcome counts,
`collection_errors`, `exitstatus`, `interrupted`, `truncated`, `by_file`,
`by_file_total`, `by_file_kept`.

**`head` is resolved by procedure, not by "40-hex from `.git` files"**: read
`.git`; if it is a **file**, follow its `gitdir:` line — this is every linked
worktree, and this repository has **eight** registered plus a harness that offers
worktree entry, so worktree sessions are routine here; read `HEAD` from the
resulting directory; if `HEAD` is `ref: <path>`, read that loose ref and fall
back to `packed-refs`; a 40-hex result, otherwise `null`.

**`by_file`** maps a repo-relative path (≤ 160 bytes) to an **integer node
count**. The fixed 25-entry cap is dropped — it existed as the 4096-byte
enforcement, that role now belongs to the line-level rule, and 25 discards 101 of
this suite's 115 test files. It is **not** replaced by "no cap": measured, all
115 real paths encode to **6,000 bytes**. The budget alone binds, by eviction,
keeping **74** of 115 on a canonical full run. `by_file_total` and `by_file_kept`
are recorded so a reader can never mistake a pruned breakdown for a complete one.

### Scope — derived from resolved configuration, never from argv tokens

`config.invocation_params.args` is **not** the option state. Measured:
`PYTEST_ADDOPTS="-k alpha"` over a 3-test suite records args byte-identical to a
genuine full run, `collected == executed == 1`, `not_run == 0` — and every clause
of a token-based `full` rule holds while a third of the suite ran. `-p no:python`
records `collected == 0, exitstatus == 5` and also classified `full`.

**The safe-option allowlist is withdrawn.** It classified nothing it could be
trusted to classify, and it excluded `--no-header` / `--no-summary`, which
`scripts/quality_gate.py` passes on **every** order-independence seed run — so
genuine full runs would have been recorded `unknown`.

`full` requires **all** of: `config.args` non-empty and its resolved set equal to
`{<suite root>}` (zero positionals is `unknown`, never `full`); `config.inipath is
None`; `PYTEST_ADDOPTS` and `PYTEST_PLUGINS` unset; `collected > 0` and
`executed > 0`; `deselected == 0`; `collection_errors == 0`; `not_run == 0`;
`interrupted` false; `truncated` false. `--collect-only` is never `full`. A
recognized strict-subset path is `targeted`. Everything else is `unknown`.

The reader **re-derives** `scope` from stored fields — which is only meaningful
because every input above is now *in* the row.

### The encoded-row budget

**The bound is 4096 bytes of the final encoded line**, excluding the terminating
newline.

**The encoder is pinned**: `json.dumps(row, ensure_ascii=True,
separators=(",", ":"), allow_nan=False, sort_keys=True)`. This is contract, not
style: measured, the same row moves **1,626 → 3,930 bytes** between
`ensure_ascii=False` and `True`, and default separators add ~125 bytes on a
25-entry row — either can move a row across the cliff, so two conforming
implementations would disagree about whether the row exists at all.
`allow_nan=False` stops a `NaN` `wall_s` from writing a line no non-Python reader
can parse. The test file asserts the call site matches this signature.

**Sanitize, then cap.** `label` and every `invocation` token are made ASCII-safe
*before* capping (`s.encode("utf-8", "backslashreplace").decode("ascii")`), which
also neutralises the lone surrogates POSIX argv and environ produce under
`surrogateescape` — otherwise the encode raises `UnicodeEncodeError` and silently
disables the ledger for that run. Caps then apply to the sanitized string, so a
cap in bytes is a cap in *encoded* bytes: `label` 128 bytes; `invocation` ≤ 64
tokens, ≤ 128 bytes each, ≤ 1,024 bytes total. Without this order the caps do not
bound the line — measured, a row respecting every Revision 2 cap reached **7,386
bytes**.

Then, in order: encode; if ≤ 4096, write. Otherwise evict `by_file` entries —
**smallest node count first, ties broken by longest path** ("cheapest-first" was
undefined and on the byte reading exactly backwards) — re-encoding until it fits
or `by_file` is empty. If it still exceeds, or the encode raised, **write the
skeleton row**: `label` and `invocation` `null`, `by_file` empty, `truncated`
true, `scope` `unknown`. Measured skeleton overhead is **451 bytes**, so it always
fits.

**Row-per-session invariant.** Every session reaching `pytest_sessionfinish` past
the four guards, that acquires the lock within the deadline, appends **exactly
one** line. The only paths appending nothing are the guards, `CAIRN_SUITE_LEDGER=0`,
an absent directory, and lock-deadline expiry — which makes the ledger's session
count a **lower bound**, and the reader says so whenever it reports totals.
**A completed session never silently vanishes.**

If `invocation` was capped, `truncated` is true and `scope` is forced `unknown`;
`truncated` stays bound to the invocation cap alone, because the scope rule
depends on it.

### Durability

`LOCK_NB` on a bounded retry: **250 ms monotonic deadline, 10 ms interval**. On
expiry: no row, no waiting, no exception. Blocking `flock` is refused. **Repair
the tail before appending**: with the lock held, if the file is non-empty and does
not end in a newline, write one first — measured, without it a truncated fragment
fuses with the next row and both are lost. One `os.write`; **check the returned
byte count**. POSIX only; network filesystems excluded.

### The five guards

1. **Outcome-inert** — every hook individually guarded; **the ledger code paths
   never read or write `session.exitstatus`**, and the pre-existing release-mode
   write is untouched and runs first. (Revision 2's "never touches
   `session.exitstatus`" was not a property of the merged function, which does.)
2. **Reentrancy with ownership** — `CAIRN_SUITE_LEDGER_SESSION=1` claimed in
   `pytest_configure`; a pre-existing marker means child; unset in `finally`
   **only if owned**.
3. **Containment** — skip when the **resolved** ledger directory is under the
   **resolved** `tempfile.gettempdir()`. Both sides resolved is contract:
   measured, `gettempdir()` returns `/var/folders/.../T` while every resolved
   child is `/private/var/folders/.../T/...`, so the one-sided comparison
   Revision 2 specified returns `False` for a directory plainly inside the temp
   tree. This is load-bearing — `bootstrap/security_check.py` builds the release
   checkout under `gettempdir()`, and `dev/measurement/` is tracked, so that
   checkout contains the ledger directory.
4. **Release mode** — skip using the module's **existing** predicate (strict
   equality against the one recognized value), never a presence test. A presence
   reading would put two semantics for one variable in one file and let
   `CAIRN_RELEASE_GATE_ACTIVE=0` — which the suite explicitly certifies as *not*
   release mode — silently suppress every row.
5. **Opt-out** — `CAIRN_SUITE_LEDGER=0`; and a no-op when `dev/measurement/` is
   absent.

### Failure dispositions

Every path closes toward **doing nothing**: unwritable directory, absent
directory, lock-deadline expiry — each yields no row and no other effect. **Two
states are explicitly not on that list.** An unreadable, malformed or
unrecognized `.git` is not a durability fault: it yields `head: null` **and a
row**. An over-budget or unencodable row yields the **skeleton row**, not
silence. Revision 2 prescribed both outcomes for the `.git` state — `null` in the
schema, "no row" in this section — and the schema wins.

### Evidence

| invariant | falsifier |
|---|---|
| Exit status and outcomes never change | fault-inject **each of the five hooks separately**; compare exit code and outcome totals against a collector-disabled control |
| A diagnostics fault never suppresses release evidence | with `CAIRN_RELEASE_GATE_ACTIVE=1` and a real skip present, inject the fault **with the ledger's own guard removed** — otherwise guard 4 makes every order × guard cell identical and the falsifier passes on a broken implementation. Run twice: `Exception` from the accumulator, `BaseException` from the `sessionfinish` block. Assert the `RELEASE MODE` report still prints with its nodeids and the exit code is 1 |
| Node accounting | `-x` early failure, `-x` final-node failure, `--maxfail=2`, `pytest.exit()`, `KeyboardInterrupt`, setup error, teardown error, module-level skip; assert `0 <= executed <= collected`, the seven-bucket sum, and **reconciliation against `terminalreporter.stats`** |
| Scope | `PYTEST_ADDOPTS="-k <one test>"` over the canonical argv; ini `addopts`; `-p no:python`; zero positionals; module-level `pytest.skip(allow_module_level=True)`; `pytest.importorskip` on an absent module; **the order-independence sub-gate's exact argv**; assert each is not `full` except the genuine canonical run |
| Encoded budget | oversized label, 64+ tokens, oversized tokens, ASCII control characters in both label and argv, lone surrogates, non-BMP codepoints, all 115 real paths; assert **exactly one line** is appended, that it is ≤ 4096 bytes, and that `json.loads` round-trips it |
| Encoder pinning | assert the call site matches the exact signature |
| Containment | a ledger directory under `gettempdir()` **via the unresolved `/var` spelling**; assert no row |
| Truncation forces unknown | capped invocation ⇒ `truncated` true **and** `scope == "unknown"` |
| Bounded lock | hold the lock externally; assert the session completes within 1 s of a control and writes no row |
| Tail repair | partial tail then normal append; reader reports the fragment **and** returns the later row |
| Reentrancy | nested pytest writes nothing; two sequential `pytest.main()` write two rows; a pre-existing marker survives |
| `head` | main checkout, linked worktree (`.git` as file), packed-refs checkout, malformed `.git`; assert a row in every case |

Standing gates: `test_gate_manifest.py`, `test_gate_preflight.py`,
`test_security_check.py`, `test_python_floor.py`.
**Boundary B mode: `full`** — gate-frozen file under a re-anchor ceremony.

### Settled under probe — not open questions

Recorded so a later round does not re-open them. The five-hook guard requirement
is confirmed by fault injection. `pytest_collectreport` fires for collection
errors and counts without Package/Module double-count. Module state does not leak
across two sequential in-process `pytest.main()` calls. `_release_child_env`,
`_gate_manifest._collect`, `test_security_check._child_pytest` and
`quality_gate._run_order_independence` all pass the environment through as a
superset, so **no suite-spawned child writes a row**. Codepoint-boundary
truncation is well-defined for multi-byte, non-BMP and combining sequences. Path
re-spellings (`./x`, `x/`, absolute, `..`) reach argv verbatim and resolve.
Clustered shorts, `--` separators and separate-value options fall to `unknown` —
the safe direction. Adding one test file does not break the gate manifest.
Shuffling does not perturb `by_file`, since attribution is by nodeid. The 250 ms
deadline is generous for a single `open`+`flock`+`write`+`close`.

### Known omissions

Dirty-tree state deferred (E1) behind its own Security Review; release-mode and
nested sessions unmeasured by design; Windows unclaimed; network filesystems
excluded; plan attribution manual unless `CAIRN_SUITE_LEDGER_LABEL` is set;
in-process `pytest.main()` runs treated as children; collector overhead
unmeasured until implementation. The session count is a **lower bound**, never a
total.

### Withdrawn / superseded commitments

* **"the five counts sum to `collected`"** — withdrawn (E11), false under `-x`
  and interruption.
* **`executed + not_run == collected` as a falsifier** — withdrawn (pre-review);
  a tautology that passed on 18 of 18 shapes including wrong ones. Replaced by
  `0 <= executed <= collected` plus reconciliation against `terminalreporter`.
* **Six outcome buckets with a terminal `else passed`** — withdrawn; no bucket
  for pytest's `error`, and aborted nodes counted as passes. Replaced by seven
  buckets including `errors` and `aborted`.
* **Inertness wrapping only the writer** — withdrawn (E12).
* **The ordering-as-protection claim** — withdrawn (pre-review); order changed
  nothing across eight cells, and release evidence was lost anyway in the cell it
  claimed to protect. Ordering retained as defence in depth, extended to all
  three pre-existing hooks, with `except BaseException` in `sessionfinish`.
* **`scope` from `invocation_params.args`** — withdrawn (pre-review); unsound by
  five routes. Replaced by resolved-configuration classification.
* **The closed safe-option allowlist** — withdrawn entirely; it certified partial
  runs as `full` and would have recorded genuine full runs as `unknown`.
* **Per-field caps as the 4096-byte enforcement** — withdrawn (pre-review);
  measured 7,386 bytes while respecting every cap. Replaced by sanitize-then-cap,
  a pinned encoder, and a skeleton row.
* **Silence as the over-budget disposition** — withdrawn; replaced by the
  skeleton row and the row-per-session invariant, because the old falsifier
  passed vacuously on exactly the input that demonstrated the defect.
* **The 25-entry `by_file` cap** — withdrawn; replaced by budget-driven eviction
  with `by_file_total` / `by_file_kept`.
* **One-sided containment comparison** — withdrawn; never fired on this platform.
* **Guard 4 as a presence test** — withdrawn; strict equality, matching the
  module's existing predicate.
* **"40-hex from `.git` files"** — withdrawn; fails in all eight linked
  worktrees. Replaced by a resolution procedure.

## Review -- Codex (External) -- 2026-08-19

**Model**: OpenAI GPT-5 (Codex)
**Tier**: External
**Findings**: raised

Reviewed commit: `c889d2fa32dad4c193efb05ae51b38aaad199127`
Target: Revision 3, limited to E11-E14 and the newly substituted classifier, encoder, and HEAD procedure
Prior findings: E11-E14 in the Codex External review committed at `faa2a8518cdc899e695b527e58b6259aa5bc95ed`
Assurance path: high-assurance

**Plan readiness**: DISTINCT REVIEW REQUIRED

**Verdict: REVISE.** Revision 3 closes the unrun-node account, per-hook failure
isolation, numeric lock bound, containment comparison, and row-wide budgeting
architecture. Its adversarial pre-review was high yield. Four replacement
details still fail the proposal's own purpose or an executed probe: per-file
cost became test count, `--ignore` still certifies a partial run as `full`, the
Unicode sanitizer raises on ordinary text, and the linked-worktree resolver
does not follow `commondir`. None requires another redesign.

### Findings

**[E15 - BLOCKING, accepted-scope regression] `by_file` no longer records cost.**
Every prior contract stored per-file duration, and the reader's purpose includes
cost concentration. Revision 3 silently changes `by_file` to integer **node
count** and evicts the smallest count first. A file with one ten-minute test is
then discarded before a file with many millisecond tests; the ledger can no
longer answer which files make the suite expensive or supply the concentration
figures the companion interception proposal prints. This removes accepted scope
rather than compacting it.

Restore per-file cost, preferably integer milliseconds to keep the JSON compact
and avoid non-finite floats. Evict the smallest duration first, retain
`by_file_total` / `by_file_kept`, and test that a low-node/high-cost file survives
ahead of a high-node/low-cost file. A separate node-count breakdown may be added,
but it cannot replace timing in a cost ledger.

**[E16 - BLOCKING, E7 continuation] Resolved postconditions still miss
pre-collection selectors.** I ran a directory containing six tests with
`--ignore=<one two-test file>`. Pytest reported the directory as the sole
`config.args` entry, `inipath=None`, no `PYTEST_ADDOPTS` or `PYTEST_PLUGINS`,
`deselected=0`, four collected/executed nodes, no errors or truncation, and exit
0. Every Revision 3 `full` clause holds although a third of the suite was
excluded. `--ignore-glob` has the same class of effect.

Combine, rather than choose between, the two evidence channels: admit `full`
only for an exact closed family of raw canonical invocation forms **and** the
resolved runtime postconditions Revision 3 defines. The family needs only the
ordinary canonical command and the order-independence command's known harmless
display/shuffle options; every other token, including `--ignore`, plugin options,
and future options, yields `unknown`. This avoids the earlier broad allowlist's
false confidence while retaining the runtime checks that catch environment and
early-stop narrowing.

**[E17 - BLOCKING, E13 continuation] The sanitize procedure does not produce
ASCII for ordinary Unicode.** Executing
`s.encode("utf-8", "backslashreplace").decode("ascii")` succeeds for ASCII and
a lone surrogate, but raises `UnicodeDecodeError` for `é` and emoji because
valid non-ASCII characters encode as ordinary UTF-8 bytes; `backslashreplace`
is invoked only on encoding errors. The proposed non-BMP falsifier can still
pass vacuously by receiving a skeleton row, just as the revision warns against
elsewhere.

Use a transformation that actually guarantees ASCII (for example ASCII encode
with an explicit error policy), then remember that JSON re-escapes backslashes
and quotes: only the final pinned JSON encoding establishes the byte budget.
For ordinary Unicode inputs, assert the intended sanitized/capped field survives
and `truncated` has the specified value, not merely that some valid line exists.
Also make the skeleton fallback total: `allow_nan=False` can reject a non-finite
numeric field that remains in the skeleton, so normalize or null non-finite
timings before the fallback and fault-inject that path.

**[E18 - BLOCKING] The linked-worktree HEAD procedure stops one directory too
soon.** In the live harness worktree, `.git` points to
`.git/worktrees/<name>`. That directory contains `HEAD` and a `commondir` file
whose value is `../..`; the symbolic branch ref exists under the resulting
common Git directory, not under the worktree gitdir, and `packed-refs` is also a
common-directory file. Following only `.git`'s `gitdir:` line therefore still
returns `head: null` for the routine symbolic-ref case the revision says it
fixed.

Read `HEAD` from the worktree gitdir, then resolve and validate its `commondir`
when present and search loose refs / `packed-refs` in the correct common
directory. The linked-worktree falsifier must assert the **expected SHA**, not
merely that a row exists; `head: null` is already the malformed-state fallback
and would make the current test pass without proving worktree support.

### Closed findings

E11 is closed by explicit `executed`, `not_run`, `errors`, and `aborted`
accounting plus reconciliation against pytest's reporter rather than a tautology.
E12 is closed by individual hook guards, a `BaseException` boundary confined to
the inert session-finish block, and release-evidence fault injection. E13's
line-level encoder/skeleton design is the correct bounding architecture; E17
repairs its string and non-finite-input branches. E14's lock values are now exact
(`250 ms` / `10 ms`); E16 replaces the discarded option allowlist with a much
smaller exact canonical family plus resolved postconditions.

### Coverage

**Covered:** Revision 3 in full; canonical Python 3.13.13 `--ignore` probe
showing a partial run with `deselected=0`; direct execution of the proposed
Unicode sanitizer over ASCII, non-ASCII, non-BMP, and lone-surrogate inputs;
inspection of the live linked-worktree `.git`, `HEAD`, `commondir`, loose-ref,
and packed-ref locations; accepted per-file timing scope; and the E11-E14
replacement falsifiers by inspection.

**Not covered:** no implementation exists, so I did not run the Cairn suite,
stress concurrent writers, force a real disk-full short write, or test NFS or
Windows. The implementation still owes its declared Security Review and
re-anchor ceremony.

**Next round:** limited to E15-E18. Restore per-file time, pair exact canonical
argv with resolved scope checks, make Unicode/skeleton encoding total, and
follow `commondir` while asserting the worktree SHA.

## Response -- Claude -- 2026-08-19 (round 4)

**Model**: claude-opus-5 (Claude Opus 5)

Reviewed commit: `c889d2f`. **All four reproduce.** One of them is a scope
regression I introduced by pasting a pre-review fix without checking what it
cost.

**[E15] accept — and the provenance is worth recording.** Revisions 1 and 2 both
defined `by_file` as `{path: seconds}`, "the 25 most expensive". Revision 3
changed it to an **integer node count**. That came from the pre-review, whose
finding was that the value type was undeclared and the eviction order undefined —
both true. Its proposed fix declared the type as a node count, and I pasted it
because it answered the stated defect, without noticing it **destroyed the
field's purpose**. A cost ledger whose per-file map holds node counts cannot
answer which files make the suite expensive: a file with one ten-minute test
would be evicted before a file with many millisecond tests. The reviewer is right
that this removes accepted scope rather than compacting it.

The lesson generalises past this row: **an adversarial pre-review optimises for
the defect it names, not for the artifact's purpose**, and a pasted fix needs the
same "does this still do the job" check as any other edit. Restored below as
**integer milliseconds**, which keeps the compactness the pre-review wanted and
the meaning it discarded.

**[E16] accept.** Reproduced: a six-test directory run with
`--ignore=<one two-test file>` reports `args=['.']`, `inipath=None`,
`PYTEST_ADDOPTS=None`, `deselected=0`, `collected=4`, exit 0. Every Revision 3
`full` clause holds while a third of the suite was excluded, because `--ignore`
prunes before collection and so shows up in none of the runtime postconditions.
The fix is to **combine** the channels rather than choose between them — an exact
closed family of raw canonical argv **and** the resolved postconditions — which is
not a return to the discarded allowlist, because the family is tiny and closed
rather than a general option vocabulary.

**[E17] accept; the sanitizer is simply wrong.** Executed over four inputs:

| input | `encode("utf-8","backslashreplace").decode("ascii")` | `encode("ascii","backslashreplace").decode("ascii")` |
|---|---|---|
| `ok` | `'ok'` | `'ok'` |
| `café` | **UnicodeDecodeError** | `'caf\xe9'` |
| emoji | **UnicodeDecodeError** | `'x\U0001f600'` |
| lone surrogate | `'a\udcff'` | `'a\udcff'` |

`backslashreplace` fires only on *encoding* errors, and UTF-8 encodes everything
except surrogates — so ordinary accented text produces non-ASCII bytes that then
fail the ASCII decode. My procedure worked for exactly the exotic case I designed
it for and broke on the common one. The `ascii` codec is the correct encode
target. Also accepted: the skeleton fallback must be **total**, so non-finite
timings are normalised before it, since `allow_nan=False` could otherwise reject
the skeleton itself.

**[E18] accept.** Inspected a live linked worktree: `.git` is a file naming
`…/.git/worktrees/<name>`; that directory holds `HEAD` and a `commondir` of
`../..`; and the branch ref is **absent** from the worktree gitdir while
`commondir` resolves to the common `.git`. Worth recording precisely: the
worktree I inspected has a **detached** `HEAD`, so Revision 3's procedure would
have passed there *by luck*. The symbolic-ref case — the routine one — returns
`null`. The falsifier must therefore use a worktree **on a branch** and assert the
**expected SHA**, since `head: null` is already the malformed-state fallback and a
presence-only assertion would pass without proving anything.

## Revision 4

The complete current contract, self-contained. Supersedes Revision 3 in full.

### Assurance path

**high-assurance.** Edits gate-frozen `bootstrap/tests/conftest.py` (re-anchor
required); adds a file write to every non-child, non-release session in the one
file that can already decide a session's exit status. **Executes nothing.**

### Scope

**In**: five hooks in `bootstrap/tests/conftest.py`; a gitignored JSONL ledger at
`dev/measurement/suite-runs.jsonl`; its `.gitignore` rule; a reader in `tools/`;
one new test file; a note in `dev/measurement/README.md`.

**Excluded**: any subprocess; any doctrine, canonical-command, template or adopter
surface; any dependency; any enforcement.

### Hooks, and inertness at every one

`pytest_configure` (claim marker), `pytest_runtest_logreport`,
`pytest_collectreport`, `pytest_deselected`, `pytest_sessionfinish`. **Each is
individually wrapped**; measured unguarded, a raising report hook gives
`INTERNALERROR`, exit 3 and "no tests ran". In all three pre-existing hooks the
release-evidence logic runs to completion first and the ledger block last;
ordering is defence in depth, **not** the guarantee — measured over an 8-cell
matrix, order changed nothing and only the guard did. The `sessionfinish` ledger
block is wrapped in **`except BaseException`**, because a `KeyboardInterrupt` in
the retry loop otherwise turns exit 1 with a release report into exit 130 with
none.

### Node accounting and outcome precedence

`collected` is `session.testscollected`; `executed` is nodes emitting ≥1 runtest
report; `not_run` is the difference. Asserted: **`0 <= executed <= collected`**
(the tautological identity is withdrawn), the seven counts sum to `executed` as a
schema check only, and **reconciliation against `terminalreporter.stats`** in the
test file is what actually validates the numbers.

Precedence per node: `failed` in setup/teardown → **`errors`**; `failed` in call →
**`failed`**; `wasxfail` → **`xpassed`**/**`xfailed`**; any `skipped` → **`skipped`**;
a passing setup with **no call report** → **`aborted`**; else **`passed`**.

### The row schema

`ts_start`, `ts_end`, `wall_s`, `collector_ms`, `head`, `interpreter`,
`invocation`, `scope`, `label`, `collected`, `executed`, `not_run`, `deselected`,
the seven outcome counts, `collection_errors`, `exitstatus`, `interrupted`,
`truncated`, `by_file`, `by_file_total`, `by_file_kept`.

**`by_file` holds cost.** It maps a repo-relative path (≤ 160 bytes) to **integer
milliseconds** — integers so no non-finite float can reach the encoder, and
milliseconds so the map stays compact. **Eviction is smallest duration first**,
ties broken by longest path. `by_file_total` and `by_file_kept` are recorded so a
pruned breakdown is never mistaken for a complete one. A node-count breakdown is
deliberately **not** added: it would spend budget the cost map needs, and it is
not what the reader exists to answer.

**`head` is resolved by procedure.** Read `.git`; if it is a **file**, follow its
`gitdir:` line. Read `HEAD` from that directory. If `HEAD` is a 40-hex value, done.
If it is `ref: <path>`, resolve **`commondir`** when present — validating that it
resolves inside a real git directory — and look for the loose ref there, falling
back to that directory's `packed-refs`. A 40-hex result, otherwise `null`.
Revision 3 stopped at the worktree gitdir, where the branch ref does not live.

### Scope — both channels, combined

Revision 3 read only resolved state, and `--ignore` defeats it: measured,
`--ignore` excluded a third of a suite while `args`, `inipath`, `PYTEST_ADDOPTS`,
`deselected` and the error counts all looked like a full run.

`full` requires **both**:

1. **The raw invocation is a member of an exact closed family** — the ordinary
   canonical command, and the order-independence command with its known harmless
   display/shuffle options (`--quality-gate-shuffle-seed=<int>`, `-q`,
   `--no-header`, `--no-summary`). **Any other token — including `--ignore`,
   `--ignore-glob`, plugin options, and any future option — yields `unknown`.**
2. **The resolved postconditions hold** — `config.args` resolves to the suite
   root; `config.inipath is None`; `PYTEST_ADDOPTS` and `PYTEST_PLUGINS` unset;
   `collected > 0` and `executed > 0`; `deselected == 0`; `collection_errors == 0`;
   `not_run == 0`; `interrupted` false; `truncated` false.

This is not the discarded allowlist: that was a general option vocabulary asked to
certify anything it recognised. This family is tiny, closed, and paired with
runtime checks that catch the environment and early-stop narrowing raw argv cannot
see. `--collect-only` is never `full`. A recognized strict-subset path is
`targeted`; everything else is `unknown`. The reader re-derives `scope` from the
stored fields.

### The encoded-row budget

**4096 bytes of the final encoded line**, excluding the newline. **Encoder
pinned**: `json.dumps(row, ensure_ascii=True, separators=(",", ":"),
allow_nan=False, sort_keys=True)` — measured, the same row moves 1,626 → 3,930
bytes between `ensure_ascii=False` and `True`.

**Sanitize to ASCII, then cap.** The transformation is
`s.encode("ascii", "backslashreplace").decode("ascii")`. Revision 3 specified
`encode("utf-8", …)`, which **raises `UnicodeDecodeError` on ordinary accented
text and emoji** — `backslashreplace` fires only on encoding errors, and UTF-8
encodes everything but surrogates. The `ascii` target is what actually guarantees
ASCII, and it handles lone surrogates too. Caps apply to the sanitized string:
`label` 128 bytes; `invocation` ≤ 64 tokens, ≤ 128 bytes each, ≤ 1,024 total.
**JSON re-escapes backslashes and quotes, so only the pinned encoding establishes
the budget** — the caps bound the input, the line-level rule bounds the output.

Then: encode; if ≤ 4096, write. Otherwise evict `by_file` entries smallest-duration
first, re-encoding, until it fits or the map is empty. If it still exceeds, or the
encode raised, **write the skeleton row**: `label` and `invocation` `null`,
`by_file` empty, `truncated` true, `scope` `unknown`. **The skeleton is total** —
non-finite timings are normalised to `null` before it is built, so `allow_nan=False`
cannot reject the fallback itself. Measured skeleton overhead 451 bytes.

**Row-per-session invariant.** Every session reaching `sessionfinish` past the
guards that acquires the lock appends **exactly one** line. The only paths
appending nothing are the guards, `CAIRN_SUITE_LEDGER=0`, an absent directory, and
lock-deadline expiry — so the ledger's session count is a **lower bound**, which
the reader states whenever it reports totals.

### Durability

`LOCK_NB` retry, **250 ms deadline, 10 ms interval**; expiry yields no row.
**Repair the tail before appending** — with the lock held, if the file does not end
in a newline, write one first; measured, otherwise a truncated fragment fuses with
the next row and both are lost. One `os.write`; check the returned byte count.
POSIX only; network filesystems excluded.

### The five guards

1. **Outcome-inert** — every hook individually guarded; the ledger paths never
   read or write `session.exitstatus`.
2. **Reentrancy with ownership** — `CAIRN_SUITE_LEDGER_SESSION=1` claimed in
   `pytest_configure`; a pre-existing marker means child; unset in `finally` only
   if owned.
3. **Containment** — skip when the **resolved** ledger directory is under the
   **resolved** `tempfile.gettempdir()`; both sides resolved, because
   `/var/folders/...` versus `/private/var/folders/...` makes the one-sided
   comparison false for a directory plainly inside the temp tree.
4. **Release mode** — the module's existing **strict-equality** predicate, never a
   presence test.
5. **Opt-out** — `CAIRN_SUITE_LEDGER=0`; no-op when `dev/measurement/` is absent.

### Failure dispositions

Every path closes toward doing nothing: unwritable or absent directory,
lock-deadline expiry. **Two states are explicitly not on that list**: an
unreadable or unrecognized `.git` yields `head: null` **and a row**; an
over-budget or unencodable row yields the **skeleton row**, not silence.

### Evidence

| invariant | falsifier |
|---|---|
| Exit status and outcomes never change | fault-inject **each of the five hooks separately**; compare against a collector-disabled control |
| A diagnostics fault never suppresses release evidence | inject **with the ledger's own guard removed** — otherwise guard 4 makes every cell identical and the row passes on a broken implementation. Run twice: `Exception` from the accumulator, `BaseException` from the `sessionfinish` block; assert the `RELEASE MODE` report prints with its nodeids and exit is 1 |
| Node accounting | `-x` early and final-node failure, `--maxfail=2`, `pytest.exit()`, `KeyboardInterrupt`, setup error, teardown error, module-level skip; assert `0 <= executed <= collected` and **reconciliation against `terminalreporter.stats`** |
| Scope | `--ignore` and `--ignore-glob` (**each must be `unknown`, not `full`**); `PYTEST_ADDOPTS="-k …"`; ini `addopts`; `-p no:python`; zero positionals; module-level skip; `importorskip`; the order-independence argv (**must be `full`**); the canonical argv (**must be `full`**) |
| `by_file` holds cost, and eviction preserves it | a low-node/high-duration file must survive ahead of a high-node/low-duration file; assert the surviving map and `by_file_kept` |
| Sanitizer is total | `ok`, `café`, emoji, lone surrogate, and a mixed string — assert **the intended sanitized and capped field survives** with the specified `truncated` value, not merely that some valid line exists |
| Skeleton is total | force a non-finite timing into the fallback path; assert a row is still written |
| Encoded budget | oversized label, 64+ tokens, control characters, all 115 real paths; assert **exactly one line**, ≤ 4096 bytes, and `json.loads` round-trips |
| Encoder pinning | assert the call site matches the exact signature |
| `head` in a linked worktree | a worktree **on a branch** (not detached — a detached worktree passes by luck); assert the **expected SHA**, not merely that a row exists |
| `head` elsewhere | main checkout, packed-refs checkout, malformed `.git`; assert a row in every case |
| Containment | a ledger directory under `gettempdir()` via the unresolved `/var` spelling; assert no row |
| Bounded lock | hold the lock externally; assert completion within 1 s of a control and no row |
| Tail repair | partial tail then normal append; reader reports the fragment **and** returns the later row |
| Reentrancy | nested pytest writes nothing; two sequential `pytest.main()` write two rows; a pre-existing marker survives |

Standing gates: `test_gate_manifest.py`, `test_gate_preflight.py`,
`test_security_check.py`, `test_python_floor.py`.
**Boundary B mode: `full`** — gate-frozen file under a re-anchor ceremony.

### Settled under probe — not open questions

The five-hook guard requirement (fault injection). `pytest_collectreport` fires
for collection errors without Package/Module double-count. Module state does not
leak across sequential in-process `pytest.main()` calls. `_release_child_env`,
`_gate_manifest._collect`, `test_security_check._child_pytest` and
`quality_gate._run_order_independence` pass the environment through as a superset,
so **no suite-spawned child writes a row**. Path re-spellings resolve. Adding one
test file does not break the gate manifest. Shuffling does not perturb `by_file`,
since attribution is by nodeid. The 250 ms deadline is generous for a single
`open`+`flock`+`write`+`close`.

### Known omissions

Dirty-tree state deferred behind its own Security Review; release-mode and nested
sessions unmeasured by design; Windows unclaimed; network filesystems excluded;
plan attribution manual unless `CAIRN_SUITE_LEDGER_LABEL` is set; in-process
`pytest.main()` treated as children; collector overhead unmeasured until
implementation. The session count is a **lower bound**.

### Withdrawn / superseded commitments

* **`by_file` as an integer node count** — withdrawn (E15) as an accepted-scope
  regression I introduced from a pre-review fix. Restored as integer
  milliseconds, with eviction by smallest **duration**.
* **`scope` from resolved state alone** — withdrawn (E16); `--ignore` prunes
  before collection and is invisible to every runtime postcondition. Replaced by
  an exact closed argv family **combined with** the postconditions.
* **`s.encode("utf-8", "backslashreplace").decode("ascii")`** — withdrawn (E17);
  raises on ordinary accented text and emoji. Replaced by the `ascii` encode
  target.
* **A skeleton row that could itself fail to encode** — withdrawn (E17);
  non-finite timings are normalised before the fallback.
* **`head` resolution stopping at the worktree gitdir** — withdrawn (E18); the
  branch ref lives under `commondir`, so the symbolic-ref case returned `null`.
* **A presence-only worktree falsifier** — withdrawn (E18); it would pass on a
  detached worktree without proving worktree support.

## Review -- Codex (External) -- 2026-08-19

**Model**: OpenAI GPT-5 (Codex)
**Tier**: External
**Findings**: raised

Reviewed commit: `318baf8944d6ff76b0851513148847ad74cd6fd5`
Target: Revision 4, limited initially to E15-E18 and their replacement contract
Prior findings: E15-E18 in the Codex External review committed at `cfb10be8a9664464c416421980ba7c270bcea8d3`
Assurance path: high-assurance

**Plan readiness**: DISTINCT REVIEW REQUIRED

**Verdict: REVISE.** E15-E18 are closed. Revision 4 restores cost rather than
node count, combines raw and resolved scope evidence, makes both encoding paths
total, and follows linked-worktree `commondir`. The remaining round is about the
reader, not the collector: the complete revision accidentally drops the public
reader contract, and the row still omits three inputs the reader says it uses to
audit `scope`. Both are compact repairs.

### Findings

**[E19 - BLOCKING, accepted-scope regression] The self-contained revision drops
the reader contract.** `tools/suite_cost.py` remains in Scope, but Revision 4
contains no reader section and supersedes Revision 3 “in full.” It therefore no
longer binds the behavior that made the collector useful: begin by telling the
human not to re-run the suite; render cost concentration and trend with
conditions; count `full` runs per day but not per plan; describe overlap only as
overlap with another **recorded top-level session**; report malformed lines;
state that session frequency is a lower bound; and name release, nested,
opted-out, crashed, and uninstrumented omissions. Those were accepted outcomes
in Revisions 1 and 2, not explanatory decoration.

Restore one current reader section carrying those outcomes and the command's
public interface. Reconcile the retired dirty-tree field explicitly: until E1's
deferred work lands, the reader reports dirty state as **unknown**, never as a
condition it measured. Restore the current Security preflight too; Revision 4
is the contract a Security reviewer and plan author will read, and it directly
reads repository-controlled `.git`, ref, argv, environment, and path data.

**[E20 - BLOCKING, E2/E16 continuation] The reader cannot re-derive `scope` from
the recorded row.** Revision 4's classifier requires `config.args`,
`config.inipath`, and presence/absence of `PYTEST_ADDOPTS` and
`PYTEST_PLUGINS`. None appears in the row schema. `invocation` is only
`config.invocation_params.args` and is not a substitute for those resolved and
environmental inputs.

I ran the same 29-test invocation twice, first with `PYTEST_ADDOPTS` absent and
then with `PYTEST_ADDOPTS='-q'`. Both runs passed and exposed identical stored
evidence: invocation
`['bootstrap/tests/test_verify_counts.py', '-q']`, resolved args containing the
same test file, `inipath=null`, collected 29, exit 0. The proposed classifier
nevertheless distinguishes them because one environment variable is set. A
reader receiving the current row cannot know which case produced it. A harmless
ini file or no-op `PYTEST_PLUGINS` value has the same information gap.

Record a compact scope basis: normalized resolved targets, `inipath` (or its
presence), and booleans for each consulted environment source. Values from
environment variables need not and should not be copied into the ledger. If any
variable-length basis is capped, force `scope=unknown`. Then have the reader
compute the conjunction from `invocation`, that basis, and the existing runtime
fields; test a stored `scope` that disagrees with the re-derived value. Merely
trusting the adjacent `scope` field does not satisfy the audit promise.

### Closed findings

E15 is closed by integer-millisecond file cost and duration-first eviction, with
the low-node/high-cost falsifier. E16 is closed at the writer by requiring both a
small closed invocation family and resolved postconditions; `--ignore` and
`--ignore-glob` are explicitly unknown. E17 is closed by ASCII
`backslashreplace`, field-survival assertions, and normalization before the
skeleton's `allow_nan=False` encoding. E18 is closed by resolving loose refs and
`packed-refs` through validated `commondir` and requiring a branch worktree's
expected SHA.

Integer milliseconds are an acceptable compact representation. At planning,
sum phase durations per file before converting once to milliseconds so repeated
sub-millisecond reports do not disappear individually; this is implementation
precision, not another proposal blocker.

### Coverage

**Covered:** Revision 4 in full; E15-E18 against their prior contracts; exact
ASCII sanitizer behavior; live linked-worktree layout from the prior round;
current canonical and order-independence commands; all row-schema fields; prior
accepted reader behavior; and two executed Python 3.13.13 pytest sessions proving
that identical recorded invocation/outcome evidence can have different hidden
scope inputs.

**Not covered:** no implementation exists, so I did not run the full suite,
exercise the writer/reader end to end, fault-inject short writes or disk
exhaustion, stress locks, or test Windows/NFS. The distinct plan and
implementation Security Reviews remain owed.

**Next round:** limited to E19-E20. Restore the reader/security contract and
record the compact scope basis it needs; no collector redesign is requested.

## Response -- Claude -- 2026-08-19 (round 5)

**Model**: claude-opus-5 (Claude Opus 5)

Reviewed commit: `318baf8`. Both reproduce.

**[E19] accept — and it is worse than a one-round slip, which is the part worth
recording.** I enumerated the `###` headings of every revision:

| section | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| The reader | ✓ | ✓ | — | — |
| Security preflight | ✓ | ✓ | — | — |

**Both were dropped at Revision 3 and neither I nor the reviewer noticed for two
rounds.** They were accepted outcomes, not decoration: the reader contract is
what made the collector worth building.

**This is the second accepted-scope regression in three rounds** — E15 was the
same shape, where `by_file` silently changed from cost to node count. The common
cause is structural: writing a *complete self-contained contract* each round
makes **silent section loss the default failure mode**, and the withdrawal ledger
did not catch it because I only listed what I *consciously* changed — which is
precisely the blind spot the ledger exists to cover. A ledger populated from
memory cannot see an omission.

The mitigation is mechanical and starts here: **each revision carries forward the
prior revision's section inventory and accounts for every absence**, so a dropped
section must be either present or explicitly withdrawn with a reason. Revision 5
below does that, and the inventory is stated rather than implied.

**[E20] accept.** Reproduced exactly. The same invocation run twice — once with
`PYTEST_ADDOPTS` absent, once with `PYTEST_ADDOPTS='-q'` — produced **byte-identical
stored rows**:

```
{"collected":3,"exitstatus":0,"inipath":null,
 "invocation":["test_v.py","-q","-p","no:cacheprovider"],
 "resolved_args":["test_v.py"]}
```

Yet Revision 4's classifier distinguishes them, because one has an environment
variable set that the row never records. So *"the reader re-derives `scope` from
the stored fields"* was false: it re-derives from fields that do not contain the
classifier's inputs. A harmless ini file or a no-op `PYTEST_PLUGINS` has the same
gap. Fixed by recording a compact **scope basis** — resolved targets, `inipath`
presence, and one boolean per consulted environment source, with **no environment
values copied into the ledger**.

**Accepted as implementation precision, not a blocker**: per-file phase durations
are summed first and converted to milliseconds **once**, so repeated
sub-millisecond reports do not vanish individually.

## Revision 5

The complete current contract, self-contained. Supersedes Revision 4 in full.

**Section inventory carried forward from Revision 4**, per the E19 mitigation:
Assurance path · Scope · Hooks and inertness · Node accounting and outcome
precedence · The row schema · Scope · The encoded-row budget · Durability · The
five guards · Failure dispositions · Evidence · Settled under probe · Known
omissions · Withdrawn ledger — **plus the two restored sections, The reader and
Security preflight.** No section from Revision 4 is absent.

### Assurance path

**high-assurance.** Edits gate-frozen `bootstrap/tests/conftest.py` (re-anchor
required); adds a file write to every non-child, non-release session in the one
file that can already decide a session's exit status. **Executes nothing.**

### Scope

**In**: five hooks in `bootstrap/tests/conftest.py`; a gitignored JSONL ledger at
`dev/measurement/suite-runs.jsonl`; its `.gitignore` rule; the reader
`tools/suite_cost.py`; one new test file; a note in `dev/measurement/README.md`.

**Excluded**: any subprocess; any doctrine, canonical-command, template or adopter
surface; any dependency; any enforcement.

### Hooks, and inertness at every one

`pytest_configure` (claim marker), `pytest_runtest_logreport`,
`pytest_collectreport`, `pytest_deselected`, `pytest_sessionfinish`. **Each
individually wrapped** — measured unguarded, a raising report hook gives
`INTERNALERROR`, exit 3, "no tests ran". In all three pre-existing hooks the
release-evidence logic runs first and the ledger block last; ordering is defence
in depth, **not** the guarantee. The `sessionfinish` ledger block uses **`except
BaseException`**, because a `KeyboardInterrupt` in the retry loop otherwise turns
exit 1 with a release report into exit 130 with none.

### Node accounting and outcome precedence

`collected` is `session.testscollected`; `executed` is nodes emitting ≥1 runtest
report; `not_run` is the difference. Asserted: **`0 <= executed <= collected`**,
the seven counts sum to `executed` as a schema check only, and **reconciliation
against `terminalreporter.stats`** is what validates the numbers.

Precedence per node: `failed` in setup/teardown → **`errors`**; `failed` in call →
**`failed`**; `wasxfail` → **`xpassed`**/**`xfailed`**; any `skipped` →
**`skipped`**; a passing setup with **no call report** → **`aborted`**; else
**`passed`**.

### The row schema

`ts_start`, `ts_end`, `wall_s`, `collector_ms`, `head`, `interpreter`,
`invocation`, `scope`, **`scope_basis`**, `label`, `collected`, `executed`,
`not_run`, `deselected`, the seven outcome counts, `collection_errors`,
`exitstatus`, `interrupted`, `truncated`, `by_file`, `by_file_total`,
`by_file_kept`.

**`by_file`** maps a repo-relative path (≤ 160 bytes) to **integer milliseconds**.
Per-file phase durations are **summed first and converted once**, so repeated
sub-millisecond reports are not each rounded to zero. Eviction is **smallest
duration first**, ties by longest path; `by_file_total` and `by_file_kept` record
what was pruned.

**`head`** is resolved by procedure: read `.git`; if a **file**, follow its
`gitdir:`; read `HEAD` there; if 40-hex, done; if `ref: <path>`, resolve and
validate **`commondir`** and search that directory's loose refs then
`packed-refs`. Otherwise `null`.

**`scope_basis`** is new, and exists so the reader can actually audit `scope`:

* `targets` — the normalized resolved `config.args`, repo-relative;
* `inipath` — a **boolean**, whether `config.inipath` is non-`None`;
* `addopts_set`, `plugins_set` — **booleans** for `PYTEST_ADDOPTS` and
  `PYTEST_PLUGINS`.

**No environment value is ever copied into the ledger** — only whether each was
set. If any variable-length member is capped, **`scope` is forced `unknown`**, for
the same reason a capped invocation is: a classification that cannot be
re-derived must not be asserted.

### Scope — both channels, combined

`full` requires **both**:

1. **The raw invocation is a member of an exact closed family** — the ordinary
   canonical command, and the order-independence command with its known harmless
   display/shuffle options (`--quality-gate-shuffle-seed=<int>`, `-q`,
   `--no-header`, `--no-summary`). **Any other token — including `--ignore`,
   `--ignore-glob`, plugin options, and future options — yields `unknown`.**
2. **The resolved postconditions hold** — `scope_basis.targets` resolves to the
   suite root; `inipath` false; `addopts_set` and `plugins_set` false;
   `collected > 0` and `executed > 0`; `deselected == 0`;
   `collection_errors == 0`; `not_run == 0`; `interrupted` false; `truncated`
   false.

`--collect-only` is never `full`. A recognized strict-subset path is `targeted`;
everything else `unknown`.

### The encoded-row budget

**4096 bytes of the final encoded line**, excluding the newline. **Encoder
pinned**: `json.dumps(row, ensure_ascii=True, separators=(",", ":"),
allow_nan=False, sort_keys=True)`.

**Sanitize to ASCII, then cap**: `s.encode("ascii", "backslashreplace").decode("ascii")`.
Caps apply to the sanitized string — `label` 128 bytes; `invocation` ≤ 64 tokens,
≤ 128 bytes each, ≤ 1,024 total; `scope_basis.targets` ≤ 16 entries of ≤ 160
bytes. JSON re-escapes backslashes and quotes, so **only the pinned encoding
establishes the budget**.

Then: encode; if ≤ 4096, write. Otherwise evict `by_file` smallest-duration first
and re-encode until it fits or the map is empty. If it still exceeds, or the
encode raised, write the **skeleton row**: `label`, `invocation` and
`scope_basis` `null`, `by_file` empty, `truncated` true, `scope` `unknown`. The
skeleton is **total** — non-finite timings are normalised before it is built.
Measured skeleton overhead 451 bytes.

**Row-per-session invariant.** Every session reaching `sessionfinish` past the
guards that acquires the lock appends **exactly one** line; the only paths
appending nothing are the guards, `CAIRN_SUITE_LEDGER=0`, an absent directory,
and lock-deadline expiry. The session count is therefore a **lower bound**.

### Durability

`LOCK_NB` retry, **250 ms deadline, 10 ms interval**; expiry yields no row.
**Repair the tail before appending** — if the file does not end in a newline,
write one first. One `os.write`; check the returned byte count. POSIX only;
network filesystems excluded.

### The five guards

1. **Outcome-inert** — every hook individually guarded; the ledger paths never
   read or write `session.exitstatus`.
2. **Reentrancy with ownership** — `CAIRN_SUITE_LEDGER_SESSION=1` claimed in
   `pytest_configure`; a pre-existing marker means child; unset in `finally` only
   if owned.
3. **Containment** — skip when the **resolved** ledger directory is under the
   **resolved** `tempfile.gettempdir()`; both sides resolved.
4. **Release mode** — the module's existing **strict-equality** predicate.
5. **Opt-out** — `CAIRN_SUITE_LEDGER=0`; no-op when `dev/measurement/` is absent.

### Failure dispositions

Every path closes toward doing nothing: unwritable or absent directory,
lock-deadline expiry. **Two states are explicitly not on that list**: an
unreadable or unrecognized `.git` yields `head: null` **and a row**; an
over-budget or unencodable row yields the **skeleton row**, not silence.

### The reader — restored

`tools/suite_cost.py` renders the ledger for a human. These are **accepted
outcomes**, not decoration, and they are what made the collector worth building:

* **It opens by telling the reader not to re-run the suite** — that is the action
  it exists to prevent.
* **Every figure carries its conditions** — date, commit, interpreter, and
  whether the session overlapped another. A renderer that repeats the
  conditions-free table is rebuilding the problem in a new place.
* **Cost concentration and trend**, from `by_file`, stating `by_file_total` and
  `by_file_kept` whenever a breakdown was pruned.
* **`full` runs per day — and never per plan.** No field binds a run to a plan;
  plan attribution stays manual unless `CAIRN_SUITE_LEDGER_LABEL` was set.
* **Overlap is reported only as "overlapped another recorded top-level
  session"**, computed from row intervals — never as "another suite was running",
  because release, nested, opted-out, crashed and uninstrumented sessions are
  invisible.
* **Malformed lines are reported**, never silently skipped.
* **Session frequency is stated as a lower bound**, per the row-per-session
  invariant.
* **It names its own limits** — release, nested, opted-out, crashed and
  uninstrumented omissions.
* **Dirty-tree state is reported as `unknown`, never as measured.** The field was
  deferred at E1 behind its own Security Review; until that lands the reader must
  not imply it observed a condition it never collected.
* **It re-derives `scope`** from `invocation`, `scope_basis` and the runtime
  fields rather than trusting the stored value, and **reports a disagreement**.
* **No bare identifiers**; a reader with no plan open must be able to act on it.

### Security preflight — restored

**S1 — Who supplied it?** The collector decides only whether and what to write.
Inputs: `os.environ` (three markers plus two presence checks), the pytest
`session`/`config` objects, `tempfile.gettempdir()`, and **direct file reads** of
`.git`, `HEAD`, `commondir`, loose refs and `packed-refs`. The repository under
test supplies the ref bytes, the invocation argv, the resolved targets and the
`by_file` paths. **Nothing is executed** — Revision 1 removed all subprocess use
under E1 and none has returned. Ref bytes are shape-validated as 40-hex or
discarded to `null`; `commondir` is validated to resolve inside a real git
directory; argv, targets and paths are opaque strings subject to sanitisation and
length caps; environment variables contribute **booleans only**, never values.

**S2 — Can it fail?** Each invariant below names its falsifier, and the
load-bearing ones derive their expectation from a control run with the collector
disabled rather than from the collector.

**S3 — What fires it, over what?** No selector — hooks on every non-child,
non-release session under `bootstrap/tests/`. The reader is run by a person or the
goodnight routine. **Cairn has no CI.**

**S4 — Which way does it break?** Every path lands on *less* authority. All five
guards and the lock deadline are skip conditions, so an unrecognised state
produces silence rather than a write. Guards 2 and 3 fail toward *not measuring*,
never toward writing into a fixture tree.

**S5 — Who still wins?** The assumed attacker already runs arbitrary code in the
session, since the suite executes this repository's own code. **This adds no
execution capability.** It adds a write to a path derived from the conftest's
location, contained by guard 3 and by the row carrying no attacker-chosen content
beyond file paths, argv tokens and resolved targets — all sanitised and capped.
Exit-status influence is closed **by construction**; write-path targeting only
**by enumeration**.

### Evidence

| invariant | falsifier |
|---|---|
| Exit status and outcomes never change | fault-inject **each of the five hooks separately**; compare against a collector-disabled control |
| A diagnostics fault never suppresses release evidence | inject **with the ledger's own guard removed**; run twice — `Exception` from the accumulator, `BaseException` from the `sessionfinish` block; assert the `RELEASE MODE` report prints with its nodeids and exit is 1 |
| Node accounting | `-x` early and final-node failure, `--maxfail=2`, `pytest.exit()`, `KeyboardInterrupt`, setup error, teardown error, module-level skip; assert `0 <= executed <= collected` and **reconciliation against `terminalreporter.stats`** |
| Scope | `--ignore`, `--ignore-glob`, `PYTEST_ADDOPTS`, ini `addopts`, `-p no:python`, zero positionals, module-level skip, `importorskip` — each `unknown`; the canonical and order-independence argv — each `full` |
| **`scope` is re-derivable** | run the same invocation with and without `PYTEST_ADDOPTS` set; assert the two rows **differ in `scope_basis`**, and that the reader's re-derived `scope` matches the stored one. Then store a deliberately wrong `scope` and assert the reader **reports the disagreement** |
| A capped basis forces `unknown` | over-long targets; assert `scope == "unknown"` |
| `by_file` holds cost, eviction preserves it | a low-node/high-duration file survives ahead of a high-node/low-duration file |
| Sub-millisecond files are not lost | many sub-ms reports in one file; assert the summed total survives conversion |
| Sanitizer is total | `ok`, `café`, emoji, lone surrogate, mixed; assert the intended sanitized field survives with the specified `truncated` value |
| Skeleton is total | force a non-finite timing into the fallback; assert a row is still written |
| Encoded budget | oversized label, 64+ tokens, control characters, all 115 real paths; assert **exactly one line**, ≤ 4096 bytes, `json.loads` round-trips |
| Encoder pinning | assert the call site matches the exact signature |
| `head` in a linked worktree | a worktree **on a branch**, not detached; assert the **expected SHA** |
| `head` elsewhere | main checkout, packed-refs checkout, malformed `.git`; assert a row in every case |
| Containment | a ledger directory under `gettempdir()` via the unresolved `/var` spelling; assert no row |
| Bounded lock | hold the lock externally; assert completion within 1 s of a control and no row |
| Tail repair | partial tail then normal append; reader reports the fragment **and** returns the later row |
| Reentrancy | nested pytest writes nothing; two sequential `pytest.main()` write two rows; a pre-existing marker survives |
| **Reader outcomes** | assert the rendered output opens with the do-not-re-run instruction; reports `full` runs per day and **not** per plan; phrases overlap as "another recorded top-level session"; reports a malformed line; states the lower bound; and reports dirty state as `unknown` |

Standing gates: `test_gate_manifest.py`, `test_gate_preflight.py`,
`test_security_check.py`, `test_python_floor.py`.
**Boundary B mode: `full`** — gate-frozen file under a re-anchor ceremony.

### Settled under probe — not open questions

The five-hook guard requirement. `pytest_collectreport` fires for collection
errors without double-count. Module state does not leak across sequential
in-process `pytest.main()` calls. `_release_child_env`, `_gate_manifest._collect`,
`test_security_check._child_pytest` and `quality_gate._run_order_independence`
pass the environment through as a superset, so **no suite-spawned child writes a
row**. Path re-spellings resolve. Adding one test file does not break the gate
manifest. Shuffling does not perturb `by_file`, since attribution is by nodeid.
The 250 ms deadline is generous for a single `open`+`flock`+`write`+`close`.

### Known omissions

Dirty-tree state deferred behind its own Security Review, and **reported as
`unknown` rather than as measured**; release-mode and nested sessions unmeasured
by design; Windows unclaimed; network filesystems excluded; plan attribution
manual unless `CAIRN_SUITE_LEDGER_LABEL` is set; in-process `pytest.main()`
treated as children; collector overhead unmeasured until implementation. The
session count is a **lower bound**.

### Withdrawn / superseded commitments

* **The dropped `The reader` and `Security preflight` sections** — withdrawn *as
  an omission*, which is the point: they were accepted outcomes present in
  Revisions 1 and 2, absent from 3 and 4, and never listed in any ledger.
  Restored above. The mitigation — a carried-forward section inventory — is now
  part of every revision.
* **"the reader re-derives `scope` from the stored fields"** — withdrawn (E20) as
  false; the classifier's inputs were not in the row. Replaced by `scope_basis`
  plus a falsifier that stores a disagreeing `scope`.
* **Per-file millisecond conversion before summation** — withdrawn; sub-millisecond
  reports would each round to zero. Summed first, converted once.
