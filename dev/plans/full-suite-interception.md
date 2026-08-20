# Plan: an in-suite guard against an unconsidered full-suite run

**Source proposal**: [`dev/proposals/archive/2026-08-19-claude-full-suite-interception.md`](../proposals/archive/2026-08-19-claude-full-suite-interception.md)
**Status**: ready-to-implement
**Plan review**: required(**Internal**) — the Maintainer ratified this exact tier
by amendment at `6fcc9bd` (2026-08-19-claude-full-suite-interception, "amend
Decision to ratify Plan review: required(Internal)"), overriding
`doctrine/plans.md`'s default escalation for a proposal-reviewer `DISTINCT
REVIEW REQUIRED` finding. This plan deliberately carries no plan-inheritance
metadata line: the source proposal's final External review (2026-08-19)
recorded `Plan readiness: DISTINCT REVIEW REQUIRED`, and
`tools/lifecycle_planner.py::plan_inheritance_violations` refuses any plan
that pairs that readiness record with an inheritance declaration — confirmed
by running the checker against both forms before writing this header. The
tier's authority is the Maintainer's amendment, stated plainly rather than
through the inheritance mechanism.
**Last update**: 2026-08-20
**Opened**: 2026-08-20

## How this plan reached `ready-to-implement`

**One Internal plan review landed, not two.** It raised four blocking findings
and six others; all were folded into the operative cells and the plan returned
to `awaiting-plan-review` for a clearing round. That round was not held. The
Maintainer directed implementation instead, quoted verbatim and visually
isolated:

> "Yes, I don't mean this accusatorily"

— given in answer to the question *"Want me to start implementing interception
now, and leave the metrics plan where it stands?"*, in a exchange about the
cost of the deliberation itself: three accepted proposals had consumed a
half-day and produced no implementation.

**Stated plainly because a later reader will weigh it.** The plan-review
precondition normally holds a `required(...)` plan at `awaiting-plan-review`
until a review clears it. Here the fold was accepted as sufficient and the
clearing round traded away deliberately, on the judgement that the remaining
questions are ones code review answers faster and more cheaply than another
prose round. The code review floor is **unchanged and independent** — not the
implementing agent — and this plan still owes its Security Review and its
re-anchor ceremony. What was skipped is one confirmation pass over a plan whose
findings were already answered, not any part of the assurance that attaches to
the code.

## Source proposal

The accepted proposal (Revision 5, the operative contract) adds a broad-run
cost guard directly inside Cairn's own test suite rather than at the harness
level. `pytest_collection_finish` in `bootstrap/tests/conftest.py` refuses
(`pytest.UsageError`, exit 4) any cleanly-collected pytest session spanning
more than 40 distinct test files, unless `CAIRN_FULL_SUITE=1` is set, release
mode is active, or the session is `--collect-only`. The refusal is
conditioned on `session.testsfailed == 0` so a pre-existing collection
failure keeps its own (stronger) exit code rather than being overwritten.
Because `scripts/quality_gate.py`'s order-independence sub-gate spawns a full
pytest run per seed, that spawn must be given the override token on an
**additive copy** of its own environment (never a fresh mapping, which would
silently drop the release-mode token `bootstrap/security_check.py` relies on).
One vendor-neutral sentence lands in `AGENTS.md` and its shipped twin,
recording that Boundary B's canonical pair now requires the override token.
This plan executes that decision; it does not re-litigate the mechanism, the
40-file threshold, or the withdrawn `.claude/`-hook design that Revision 5
supersedes.

## Proposed paths

Proposed paths:
- `tools/suite_cost.py` — the sibling plan's reader, which lands before this plan starts; row A7 edits it and does not create it.
- `bootstrap/tests/test_suite_ledger.py` — the sibling plan's contract-test file, likewise created there and only *read* here (Boundary A mapping); it does not resolve until that plan's own chunk lands.

## Scope

**In** (Revision 5, "Scope"): the guard in `bootstrap/tests/conftest.py`; the
additive child-environment fix in `scripts/quality_gate.py`; one
vendor-neutral sentence under *Verification boundaries* in `AGENTS.md` and its
shipped twin `templates/core/AGENTS.md`; one new test file.

**This plan's Chunk A exceeds that list by two files, and the discrepancy is
declared here rather than absorbed.** Rows A4 and A5 modify
`bootstrap/tests/test_security_check.py` and
`bootstrap/tests/test_quality_gate_order_independence.py`, neither of which
Revision 5's Scope names. Both edits are consequentially necessary rather than
new work: A2 makes an existing docstring in the first file factually false (it
asserts the order-independence sub-gate launches pytest with *no* `env=` of its
own), and A5 is the falsifier for A2's own accepted change. Leaving either
alone would ship a test whose prose asserts a fact this change deletes.

**Authorized.** Accepted scope is a floor in both directions, so touching two
files the accepted artifact does not name was a deviation to authorize rather
than to justify, and the plan did not grant it to itself.

**Contract expansion**: touched-file set — `bootstrap/tests/test_security_check.py`
and `bootstrap/tests/test_quality_gate_order_independence.py` join the accepted
Scope. Authorized by the Maintainer, quoted verbatim and visually isolated:

> "Please do A4/A5 in this one, allow the scope widening"

What the allowance covers: rows A4 and A5 as written — correcting the docstring
and comment that A2 falsifies, adding the additive-copy falsifier for A2's own
change, and the third edit the row mapping places in the same file as A4
(`test_a_release_refused_outcome_is_not_masked_by_the_guard`, extending the
existing `_quality_gate_tree` fixture family — assigned to this file before
the allowance commit `e0ab524`, so "do A4/A5" plausibly covered it, and it is
named here explicitly rather than left for the row mapping alone to carry).
It does not open those two files to unrelated edits beyond these three, and it
widens nothing else. Both files are gate-frozen, which is why the re-anchor
accounting below counts four `FROZEN-MODIFIED` entries rather than two.

**A second expansion, for the cross-plan seam.** Row A7 adjusts the sibling's
reader so a session *this* guard refuses cannot be mistaken for a full run
that cost nothing; row A6 pins, rather than changes, what the sibling's
collector already does with such a session. A7 adds `tools/suite_cost.py`,
which no accepted artifact here names at all.

**Contract expansion**: touched-file set — `tools/suite_cost.py` joins the
touched set. Authorized by the Maintainer, quoted verbatim and visually
isolated:

> "I'll take your recommendation on Decision 3. b + c"

The recommendation that names — recorded here because a bare "b + c" will mean
nothing to a later reader: **(b)** the reader excludes refused sessions from
cost aggregation and reports the refusal count separately; **(c)**, as
originally proposed, would have made the `scope` classifier resolve `unknown`
rather than `full` for such a session.

**(c)'s premise did not hold, and this supersedes it.** Internal plan review
(2026-08-20) showed that the sibling's accepted contract
(`2026-08-19-claude-suite-run-diagnostics`, Revision 5 > "Scope — both
channels, combined", postcondition 2) already requires `collected > 0` **and**
`executed > 0` **and** `not_run == 0` for `scope == "full"`. A session this
guard refuses has `executed == 0` by construction — nothing ran before the
refusal fires at collection-finish — so it already resolves `unknown` under
the sibling's own accepted contract, with no classifier change needed. (c) as
authorized would have added a special case for a condition the general rule
already covers, and its falsifier could not have failed either way. Put back
to the Maintainer, whose disposition is quoted verbatim:

> "Sure, I like the regression guard idea"

**A6 is therefore a regression guard, not a classifier change.** It pins the
sibling's existing behaviour — which this plan depends on and which nothing on
this side previously pinned — rather than editing it: if a later change to the
sibling relaxes `executed > 0` or `not_run == 0`, a guard-refused session would
start being counted as a full run, and this test is what catches that. Its
falsifier is directional and able to fail on both halves: a guard-refused
session resolves `unknown`, **and** the same tree under `CAIRN_FULL_SUITE=1`
resolves `full` — a test asserting only the first half would pass against a
classifier that returns `unknown` unconditionally, which is not the property
this guards.

**(b) still stands, on a narrower falsifiable core.** Excluding refused
sessions from cost aggregation and reporting the refusal count separately is
still worth doing: a refused session carries a real `wall_s` and an empty
`by_file`, so any figure summed at the session level rather than derived
purely from `by_file` is pulled toward zero by a run that never ran, and the
refusal count is genuinely new information the reader does not otherwise
surface — `scope == "unknown"` alone does not distinguish a refusal from any
other non-full run (a `-k` run, say) unless the reader keys on
`exitstatus == 4`. The cost profile, concentration table and growth curve are
derived from `by_file`, which is empty for a refused row, so their
byte-identity with and without a refused row present may already hold
structurally, without any exclusion code; the part of A7 that is actually new
and testable is the refusal count itself, plus exclusion of any session-level
aggregate that is not purely `by_file`-derived. Chunk A's row A7 and the
corresponding row-mapping falsifier are scoped to that. Neither requires a
schema change: `exitstatus` is already a pinned field and a refusal is exit 4.

**Why this plan owns A7 rather than the sibling.** The sibling lands first,
when no session can yet be refused this way — it could only write handling
for a condition it cannot produce, and falsify it against a mock. This plan
creates the condition and can test the edit against the real guard.

**Out, and not revivable by this plan** (Revision 5, "Withdrawn and not
deferred"): everything under `.claude/` (settings object, hook script,
command grammar, blocked-form enumeration, `agent_id` predicate); the
withdrawn scope-derivation reader and the "Boundary A block" it would have
read; the `_gate_manifest.py` glob extension and `[TRU-4]` scope folding; any
entry in the root `CLAUDE.md`.
`templates/core/VENDOR.md` is explicitly untouched. These are append-only
history, not a backlog this plan may quietly re-open.

**Sequencing against the sibling proposal — read this before touching
`conftest.py`.** [`2026-08-19-claude-suite-run-diagnostics`](../proposals/archive/2026-08-19-claude-suite-run-diagnostics.md)
(accepted the same day, planned separately) also edits
`bootstrap/tests/conftest.py`, adding five telemetry hooks
(`pytest_configure`, `pytest_deselected`, an extended
`pytest_runtest_logreport`, an extended `pytest_collectreport`, and an
extended `pytest_sessionfinish`). *(An earlier draft named the fifth as "its
own collector"; that describes `_gate_manifest.py`'s
`pytest_collection_modifyitems`, a different pre-existing mechanism, cited
separately below. The name-collision check further down was therefore run
against a list with one wrong member — its conclusion happens to hold, but the
check did not.)* **The sequencing decision is already made and is not this plan's
to revisit: suite-run-diagnostics implements first; this plan implements
second and inherits its landed `conftest.py`.** Revision 5's own "Interaction
with the sibling proposal" analysis (carried from Revision 3) says the two do
not conflict semantically — one measures, one refuses — but whichever lands
second must re-verify against the other's `conftest.py`, and both share the
one re-anchor ceremony this plan's Chunk D opens. Concretely, this plan's
Chunk A:
* adds a **new** hook function (`pytest_collection_finish`) that does not
  collide by name with any of the five diagnostics hooks;
* must re-read the landed `conftest.py` before writing the guard, rather than
  writing against the **five**-hook file this plan's author read while drafting
  (`pytest_addoption`, `pytest_collection_modifyitems`,
  `pytest_runtest_logreport`, `pytest_collectreport`, `pytest_sessionfinish`
  — the pre-existing shuffle-hook and release-mode-outcome mechanisms,
  unrelated to diagnostics) — that is a live invariant to re-check at Chunk
  A's own start, not a carried-forward claim;
* must confirm `session.items` and `session.testsfailed` still mean what
  Revision 5 assumes once the diagnostics hooks are in place (they read
  reports and durations; nothing in their accepted design touches collection
  or the failure counter, but this plan re-verifies rather than asserts);
* **must pin what the sibling's ledger records for a session this guard
  refuses.** A refusal does **not** skip `pytest_sessionfinish`. Verified
  against the installed pytest (9.0.3, `_pytest/main.py`): `initstate = 2` is
  assigned *before* `doit(config, session)` runs collection, the `except
  UsageError` clause re-raises after setting the exit status, and the
  `finally` block calls `pytest_sessionfinish` whenever `initstate >= 2`. So a
  refused session still reaches the ledger append that the diagnostics plan
  places last in that hook, and writes a row with `collected` ≈ the full set
  and `executed` = 0. **The sibling's own accepted postconditions already
  resolve this row `unknown`, not `full`** — `full` requires both
  `collected > 0` **and** `executed > 0` (and `not_run == 0`), and a refused
  session's `executed == 0` by construction fails that before any narrowing
  test is even reached (verified against
  `2026-08-19-claude-suite-run-diagnostics`, Revision 5 > "Scope — both
  channels, combined", postcondition 2; an earlier draft of this bullet read
  the sibling's `full` conditions as covering only narrowing options, early
  stop and collection errors, and missed this postcondition — that draft was
  wrong, not the sibling's contract). The real cross-plan hazard is narrower
  than "mislabelled as full" and is still real: (1) the reader's cost
  concentration and trend are derived from `by_file`, which is **not** scoped
  to `full`, so a refused row — real `wall_s`, empty `by_file` — still lands
  in the trend as a zero-cost session; and (2) `scope = unknown` alone does
  not distinguish a guard refusal from any other `unknown` run (a `-k` run,
  say), so the refusal count — the number this guard exists to produce — is
  otherwise unrecoverable without keying on `exitstatus == 4`. **Resolved by
  rows A6 and A7 under a Maintainer allowance** (recorded in Scope, corrected
  there too): A6 pins the sibling's existing `unknown` resolution as a
  regression guard rather than changing the classifier; A7 gives the reader
  the `exitstatus == 4` key so a refused row is excluded from the figures it
  would otherwise pull toward zero and the refusal count is surfaced on its
  own. Also `bootstrap/tests/test_suite_ledger.py` added to the Boundary A
  mapping, since `conftest.py` is the ledger's surface by then and Boundary A
  requires the standing gates for every touched surface. Note that the
  sibling's own node-accounting falsifier enumerates the abort shapes it
  reconciles — `-x`, `--maxfail=2`, `pytest.exit()`, `KeyboardInterrupt`,
  setup error, teardown error, module-level skip — and a collection-time
  `UsageError` from a conftest hook is **absent** from that list, while this
  plan makes it the most common non-clean shape in the tree. Its stated
  invariant `0 <= executed <= collected` is satisfied by `(0, ~4,443)`, so
  that falsifier does not exercise this shape — but the classifier's own
  `executed > 0` postcondition handles it correctly regardless, as A6's
  regression guard pins.

This plan does **no** work inside the diagnostics proposal's own scope
(the cost ledger, its schema, or its standalone reader tool). If the
diagnostics plan has not yet landed when Chunk A begins, Chunk A blocks on
it rather than reordering the two proposals' accepted sequencing.

### Documentation / doctrine surface

Two files, both narrow, hand-authored edits — no doctrine-directory change,
no new doctrine rule (Revision 5 carries forward the withdrawn Part 3's "not a
doctrine rule change" framing: this is a Boundary B *procedure* clarification
inside `AGENTS.md`'s existing Verification-boundaries text, not a new
`doctrine/` rule, and does not engage the rate-limit gate):

* `AGENTS.md` — one sentence appended to the *Verification boundaries* > B
  (Integration) bullet, immediately after the existing canonical-pair
  sentence (the exact text the Decision names, quoted verbatim below in
  Chunk B).
* `templates/core/AGENTS.md` — the same substance, in that file's own
  vendor-neutral, project-generic phrasing (it never names Cairn's concrete
  `bootstrap/tests` / `--quality-gate-shuffle-seed` invocation, only "the
  configured full suite" / "the project's configured interpreter/runtime").
  **The exact adapted wording is this plan's own judgment call, flagged
  explicitly** — the proposal's Touches line commits to "one vendor-neutral
  sentence… in `AGENTS.md` and its shipped twin" but the Decision's quoted
  sentence is written in Cairn-specific terms (`CAIRN_FULL_SUITE=1`,
  "Boundary B's canonical pair"). Chunk B gives a concrete candidate and
  the acceptance criterion that governs it (no AI vendor named; same
  substance; matches the twin's existing generic register).

No other narrative doc changes. `CHANGELOG.md`: **N/A** — this is a
Cairn-internal verification-procedure clarification of existing Boundary B
text, not a new adopter-facing capability, mechanism, or doctrine rule (the
same class as the unlogged 2026-08-12 Boundary-B-bounding-clause landing;
`bootstrap/tests/` itself is not installed to adopters — 0 entries under
`scaffold.py --manifest`, unchanged by this plan).

## Sequence

```
1. Chunk A -- the guard + the additive child environment          [landed a316d75]
2. Chunk B -- the vendor-neutral sentence, AGENTS.md + its twin    [landed this commit]
3. Chunk S -- the sibling seam (rows A6/A7)                        [BLOCKED on suite-run-diagnostics]
4. Chunk C -- Security Review of the implementation                [Maintainer/reviewer-owned, not a commit]
5. Chunk D -- the gate re-anchor ceremony                           [Maintainer-owned, not this plan's commit]
```

**Rows A6 and A7 move out of Chunk A into their own chunk, and the reason is a
deadlock this plan did not create.** Both act on artifacts the sibling plan
creates: A7 edits `tools/suite_cost.py`, and A6 pins the behaviour of the ledger
written by the sibling's hooks. Neither exists — verified on disk, as_of
2026-08-20. The sequencing note below says this plan lands second, behind
`suite-run-diagnostics`; that plan is now itself blocked, on an amendment to its
accepted proposal (its Evidence table requires falsifiers that cannot be
constructed under its own guards). So waiting for the stated order would stall
the guard indefinitely behind a contract repair it has no stake in.

**What changes is sequencing, not scope.** A plan may re-order freely; the two
rows are unchanged, still carry the Maintainer's allowance, and remain
obligations of this plan. Chunk S runs when the sibling's reader and ledger
exist, and does not gate Chunks A or B. **Chunk S is a precondition of this
plan reaching `ready-to-archive`** — an unrun chunk is not a dropped one only
while something still holds it open, and this sentence is that thing.

**Chunks A and B are independent and may land as two commits or one; Chunk A's
two halves are not.** The guard and the child-environment fix are coupled and
must land in the **same commit**: `scripts/quality_gate.py --sub
order-independence` spawns a full pytest run per seed, which is exactly the
shape the guard refuses. Landing the guard without the environment fix in the
same commit would make the quality gate refuse itself the moment the guard's
commit is checked out — a real broken-window state, not a cosmetic one. (Both
files are gate-frozen regardless, so both land under the same re-anchor no
matter how the commits are split; the constraint here is behavioral, not
freeze-driven.)

### Chunk A — the guard, the additive child environment, and their tests

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/tests/conftest.py` | Add `pytest_collection_finish(session)`. Refuses (`pytest.UsageError`, exit 4) when the cleanly-collected session spans more than 40 distinct test files (count file paths, not test count — Revision 5's own measurement: a full collection spans ~115 files, the 6-file mapping this project has used spans 6, so file span separates a scoped run from a full one by nearly 20x where test count does not). Precondition: raise **only** when `session.testsfailed == 0` (and whatever additional stop/interrupt state the implementation finds it must consult to keep this precondition honest — the falsifier in row A4 below is what proves it, not inspection). Exemptions, each a strict-equality check in the existing module style (`_release_mode()`'s "equality, not truthiness" convention): `CAIRN_FULL_SUITE == "1"`; release mode via the existing `_release_mode()` helper; `session.config.getoption("--collect-only")`. |
| A2 | `scripts/quality_gate.py` | Add `import os`. In `_run_order_independence` (currently ~line 147), before the `subprocess.run(cmd, cwd=str(repo_root), capture_output=True, text=True)` call (currently ~line 164), build `env = os.environ.copy()`, set `env["CAIRN_FULL_SUITE"] = "1"` on the copy, and pass `env=env` to `subprocess.run`. **A fresh mapping is wrong** — it would drop `CAIRN_RELEASE_GATE_ACTIVE`, which `bootstrap/security_check.py` passes to this process explicitly and which the grandchild currently inherits only because no `env=` is set today; dropping it would silently stop a release run from refusing a skip as evidence while every test still passes. |
| A3 | `bootstrap/tests/test_broad_run_guard.py` *(new)* | The guard's own behavioural tests — see the row mapping below. |
| A4 | `bootstrap/tests/test_security_check.py` | **Update, not add.** `test_the_release_token_survives_the_real_grandchild_launcher` (currently ~line 806) and its docstring, and the comment inside `test_the_release_token_reaches_both_direct_children` (currently ~line 459-460), assert today that "the middle link launches pytest with **no** `env=` of its own… the token reaches the grandchild by *inheritance*." A2 makes that false: after this chunk, `_run_order_independence` always passes an explicit `env=`. The docstring/comment must be corrected to state the new mechanism (an explicit additive copy, not bare inheritance) — the underlying assertions (rc matches `expect_refusal`; the release token reaches the real grandchild) still hold and stay as regression coverage, but the prose explaining *why* they hold must not keep asserting a fact this chunk deletes. |
| A5 | `bootstrap/tests/test_quality_gate_order_independence.py` | Add a test asserting the spawn in `_run_order_independence` passes an explicit `env=` that is a **superset of the parent process's environment plus `CAIRN_FULL_SUITE=1`**, not a fresh mapping — the row-10 falsifier below, following the existing `_spy_run`-style capture pattern already used in `test_security_check.py` for the same shape of assertion. |

**Every row below constructs its own child pytest environment explicitly.**
This plan's own mandated Boundary B invocation runs `CAIRN_FULL_SUITE=1
python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0`, and a release
ceremony runs with `CAIRN_RELEASE_GATE_ACTIVE` set. A child spawned by naive
inheritance of `os.environ` would carry one of those tokens regardless of
which row is exercising it, so every refusal-expecting row would fail in
exactly the run this plan makes mandatory, and every allow-expecting row would
pass without exercising anything. `test_broad_run_guard.py` therefore builds
each child's environment the way `test_security_check.py`'s `_child_pytest`
already does (`env = dict(os.environ)`, then pop the tokens the row is not
deliberately testing — the same idiom at `test_security_check.py:669-678`,
the file row A4 extends), not by passing the parent's environment unmodified:
both `CAIRN_FULL_SUITE` and `CAIRN_RELEASE_GATE_ACTIVE` are popped by
default, and set only on the row(s) actually about them (rows 9 and 10
below deliberately set one each). Row 14 is the guard against this
construction drifting back to bare inheritance.

**Row mapping — Revision 5's Evidence table to prospective test names** (all
in `bootstrap/tests/test_broad_run_guard.py` unless noted):

| # | Revision 5 invariant | prospective test | file |
|---|---|---|---|
| 1 | ≤ 40 files, however collected, is never refused | `test_a_run_at_or_under_the_file_threshold_is_never_refused` (parametrized: single file, node id, `-k`, `-m`, `--ignore` down to ≤ 40, `PYTEST_ADDOPTS='-k …'`, the six-file mapping) | A3 |
| 2 | > 40 files, whatever the selector, is refused | `test_a_run_over_the_file_threshold_is_refused_regardless_of_selector` (parametrized: bare run, `cd <repo> && …`, env-prefixed, absolute interpreter, the canonical Boundary B argv, `--ignore` of one file at ~114 files / ~4,443 items) | A3 |
| 3 | the boundary itself | `test_the_file_threshold_boundary_is_exact` (41 refuses, 40 runs) | A3 |
| 4 | a pre-existing collection failure is never masked | `test_a_pre_existing_collection_failure_keeps_its_own_exit_code` (41 valid files + 1 syntax-error file: exit 2 and the collection diagnostic survive, refusal message absent; a clean 41-file control still exits 4) | A3 |
| 5 | the guard sees the final item list | `test_the_guard_refusal_follows_a_late_deselection` — **directional, and deliberately not the wording Revision 5's Evidence row carries.** That row says "assert the guard's count equals `len(session.items)`", which compares a **file** count to an **item** count (on a real collection, ~115 against ~4,443). Read literally it is a type mismatch; read charitably it is satisfied whenever a competing modifier removes nothing, which is the default for a modifier registered only to prove ordering — so it cannot distinguish "the guard read the post-filter list" from "the guard read a list". Instead: register a late `pytest_collection_modifyitems` that **removes** items so the distinct-file span crosses the threshold, and assert the refusal **flips** accordingly (and the converse: a late modifier that pushes the span above the threshold causes a refusal that would not otherwise fire). Revision 5's S2 names this one of two load-bearing falsifiers precisely because it must separate those two cases. | A3 |
| 6 | the override allows | `test_the_override_token_allows_a_full_run` (`CAIRN_FULL_SUITE=1`: exit 0, full execution; paired control: the same over-threshold run without the token is refused) | A3 |
| 7 | release mode is exempt | `test_release_mode_is_exempt_from_the_guard` (the module's existing predicate at its one recognized value; the suite runs; `=0` does **not** exempt) | A3 |
| 8 | `--collect-only` is exempt | `test_collect_only_is_exempt_from_the_guard` (`_gate_manifest.py`'s own collector still builds) | A3 |
| 9 | the release token survives the gate | `test_a_release_refused_outcome_is_not_masked_by_the_guard` (real `security_check → quality_gate → pytest` path, a release-refused fixture: guard does not refuse it, release phase stays non-zero; the one row that deliberately sets `CAIRN_RELEASE_GATE_ACTIVE`) | A4 (extends the existing `_quality_gate_tree` fixture family) |
| 10 | the child environment is additive | `test_the_order_independence_child_env_is_an_additive_copy` (the spawn's `env=` is a copy of the parent plus `CAIRN_FULL_SUITE=1`, not a fresh mapping; the one row that deliberately sets `CAIRN_FULL_SUITE`) | A5 |
| 11 | the bypass is real and bounded | `test_noconftest_bypasses_the_guard` (`--noconftest` collects without loading `conftest.py`; the guard does not fire; paired control: the same run **with** the conftest loaded and no token is refused) | A3 |
| 12 | a refused session is scoped `unknown` under the sibling's existing contract, and this plan guards that rather than assuming it | `test_a_refused_session_is_scoped_unknown` — run the real guard to refusal over a fixture tree, then read the ledger row it wrote: `scope` is `unknown`, not `full` (the sibling's own `executed > 0` postcondition, not a code change from this plan). Directional: the same tree under `CAIRN_FULL_SUITE=1` writes `full`, so the test fails if the sibling's postconditions stop distinguishing the two rather than passing on a constant — a regression guard on the sibling's contract, not a falsifier of this plan's own code. | A3 (regression guard, A6) |
| 13 | a refused session's refusal is countable, and does not deflate any session-level aggregate | `test_refused_sessions_are_excluded_from_cost_and_counted_separately` — build a ledger fixture mixing real runs with refusals, render it, and assert (a) the refusal count is correctly reported and differs from a fixture with no refusals, and (b) any session-level aggregate not purely `by_file`-derived is byte-identical to the same fixture with the refused rows absent. The cost profile, concentration table and growth curve are `by_file`-derived and may already be byte-identical without (b)'s exclusion code, since a refused row's `by_file` is empty; (a) is the falsifiable core, and a reader that surfaces no refusal count, or miscounts it, fails the row regardless of (b). | A3 (asserting A7) |
| 14 | a refusal-expecting child never inherits an ambient exemption token | `test_a_refusal_expecting_child_never_receives_an_exemption_token` — the meta-guard on the environment-construction discipline stated above: assert that a child built for a refusal-expecting row never carries `CAIRN_FULL_SUITE` or `CAIRN_RELEASE_GATE_ACTIVE`, so this plan's own Boundary B wrapper or a release ceremony's active token cannot leak into a spawned child by omission and make a refusal-expecting row pass without exercising anything. | A3 |

### Chunk S — the sibling seam (blocked until `suite-run-diagnostics` lands)

**Do not start this chunk while `tools/suite_cost.py` is absent.** Both rows act
on artifacts the sibling plan creates. Check for the file and for the ledger
hooks in `bootstrap/tests/conftest.py` before beginning; if either is missing,
this chunk is not ready and Chunks A and B proceed without it.

| # | File | Change |
|---|------|--------|
| A6 | `bootstrap/tests/test_broad_run_guard.py` (regression guard; no change to the sibling's classifier) | **Pin, don't change, the sibling's existing classification of a refused session.** The sibling's accepted contract already requires `executed > 0` and `not_run == 0` for `scope == "full"`; a session this guard refuses has `executed == 0` by construction, so it already resolves `unknown`. This row guards that property against a later relaxation of the sibling's postconditions, rather than adding classifier code — see Scope > "A second expansion" for the corrected derivation and the Maintainer's disposition ("Sure, I like the regression guard idea"). Falsifier: directional on both halves — a refused session resolves `unknown`, and the same tree under `CAIRN_FULL_SUITE=1` resolves `full` (mapped as `test_a_refused_session_is_scoped_unknown` in the row mapping below). |
| A7 | `tools/suite_cost.py` (the sibling's reader) | **Exclude refused sessions from any aggregate they would pull toward zero, and report the refusal count separately.** A refused session is identifiable from the pinned schema with no schema change: `exitstatus` is 4 and `by_file` is empty. The cost profile, concentration table and growth curve are derived from `by_file`, so their byte-identity with and without a refused row present may already hold structurally; what this row actually adds is (1) the refusal count itself — otherwise unrecoverable, since `scope == "unknown"` does not by itself distinguish a refusal from any other non-full run — and (2) exclusion of any session-level aggregate that is not purely `by_file`-derived. Reporting the refusal count matters because `dev/PLANNING.md` records that measuring whether the delegation rule works depends on exactly this ledger. |

**Acceptance for this chunk**: both falsifiers in the row mapping above pass —
the refused-session scope guard is directional (a refused session resolves
`unknown`, the same tree under the override resolves `full`, so a classifier
that answers `unknown` unconditionally fails it), and the reader's exclusion is
asserted by byte-identical output against the same fixture with refused rows
removed, so a reader that down-weights rather than excludes fails it.

### Chunk B — the vendor-neutral sentence

| # | File | Change |
|---|------|--------|
| B1 | `AGENTS.md`, *Verification boundaries* > **B — Integration**, immediately after "…`python scripts/quality_gate.py --sub neutrality --sub redundancy`." | Append, verbatim, the sentence the Decision names: *"Boundary B's canonical pair now requires `CAIRN_FULL_SUITE=1`; verification records written before this guard cite the bare form and are accurate for the runs they describe."* Names no AI vendor or model. **No *neutrality* gate covers this file** — the standing operational-boundaries and comprehension-floor tests do; see the verification note below. |
| B2 | `templates/core/AGENTS.md`, the same bullet's generic equivalent (the equivalent sentence currently ends "…run against a clean, unchanged commit under the project's configured interpreter/runtime.", though the bullet itself continues afterward with the bounded-mode contract — insert after that sentence specifically, not at the bullet's end) | Append the *adapted* sentence, matching the twin's existing register. **Decided, not left to implementer judgment: no literal `CAIRN_FULL_SUITE` token** — the candidate below already avoids it, and nothing in the twin's own neutrality/generality checking currently blocks a Cairn-specific token from shipping if one were used (see the hazard noted below), so the safety margin is in not writing it, not in a gate catching it. Candidate: *"A project's Boundary B command may require an explicit override token to run as a full suite; verification records written before such a guard lands cite the bare form and remain accurate for the runs they describe."* Acceptance criterion: same substance as B1, no AI vendor or model named, no literal `CAIRN_FULL_SUITE` token, phrased in the twin's own generic voice — not a byte-identical copy of B1, since the twin's surrounding sentence already diverges from `AGENTS.md`'s in the same way (`diff` shows "the configured full suite" / "the project's configured interpreter/runtime" replacing Cairn's concrete text throughout that bullet). |

**Verification for Chunk B — and the asymmetry that an earlier draft of this
plan got wrong.** `python scripts/quality_gate.py --sub neutrality` governs
**B2 only**. It does not scan the repository-root `AGENTS.md`: its file set is
built from `_NEUTRALITY_FILE_SUFFIXES`, whose eight keys are all *directories*
(`doctrine`, `dimensions`, `on-ramp`, `docs`, `examples`, `bootstrap`,
`scripts`, `templates`), and `_walk_neutrality_files` walks only those. Measured
by importing that function against this tree: **181 files scanned, root
`AGENTS.md` not among them, `templates/core/AGENTS.md` among them.** So the
criterion "clears `--sub neutrality`" that stood in an earlier draft of the B1
cell would have returned clean no matter what B1 landed, including a sentence
naming a vendor. That is the silent-tool defect `AGENTS.md` > *Verifying
claims* names outright: a tool that returns success without testing the
claimed property is worse than no tool.

* **B2** is genuinely gated. Under the `templates/` branch a denylist token is
  an unconditional failure with no exemption path.
* **B1 has no *neutrality* gate — it is not ungoverned.** No automated check
  scans root `AGENTS.md` for vendor tokens, so B1's vendor-neutrality stays a
  **reviewer obligation**, discharged by a human or reviewing agent reading
  the sentence — named here as such rather than left to look mechanized. The
  sentence the Decision fixes verbatim contains no vendor token, so the live
  risk is a later edit, not this one. But the bytes B1 changes are not
  otherwise unchecked: `bootstrap/tests/test_verification_boundaries.py`
  (`SELF_AGENTS = ROOT / "AGENTS.md"`) asserts over the exact *Verification
  boundaries* text Chunk B edits — `test_both_operational_surfaces_fail_to_full`,
  `test_installed_operational_rule_is_project_general`, and the
  `_BOUNDED_OBLIGATIONS` block — and `bootstrap/tests/test_comprehension_floor.py`
  parametrizes the comprehension-floor checks over both `AGENTS.md` and
  `templates/core/AGENTS.md`. Both are standing gates for this surface and are
  folded into Chunk B's Boundary A mapping below.
  `bootstrap/tests/test_scope_reduction_trap.py` also maps the twin
  (`templates/core/AGENTS.md`) as a governing surface.
* `python scripts/check_cairn.py` (link/claim integrity) does cover both files.

**One live hazard the B2 decision above closes rather than opens.**
`test_installed_operational_rule_is_project_general` denies the adopter file
the tokens `bootstrap/tests`, `scripts/quality_gate.py`, `Python 3.13` and
`Cairn's ordinary pair`. `CAIRN_FULL_SUITE` is **not** in that list, so
nothing would have caught a Cairn-specific token shipping to adopters through
B2 — which is exactly why B2's cell above decides the question rather than
leaving it to judgment: the candidate sentence avoids the token, and the
acceptance criterion states the constraint explicitly instead of relying on a
gate that does not check it.

### Live commands the guard breaks beyond AGENTS.md's own sentence — flagged, not authorized

Chunk B corrects exactly one Boundary B sentence, in two files. The guard
refuses a bare `pytest bootstrap/tests`, and that bare form is named, as a
literal command, in several more places this plan does not touch. Grepped,
read in context, and classified rather than lumped together:

**Live instructions — a person or Maintainer following them literally hits an
unexpected refusal mid-procedure:**
* `docs/release-process.md:78` — the "## Checks to run" command block for a
  release sweep.
* `bootstrap/AST_BASELINE_RUNBOOK.md:126` — Step 4 "apply, verify, commit" of
  the AST-baseline re-anchor procedure, a Maintainer-run ceremony step (this
  plan's own Chunk D routes the Maintainer to the neighbouring re-anchor
  runbook in the same sitting).
* `AGENTS.md:487`, *Development environment & dependency budget* — "Run the
  suite with `python -m pytest bootstrap/tests`." The same file Chunk B1
  edits, but a separate, unrelated section 160 lines from B1's corrected
  sentence, so B1's placement does not fix it.

**Trigger prose — names what a person types to run a check, not a copy-paste
procedure step; a reader who actually types the command meets the guard's own
refusal message, and (for the `AGENTS.md` case discussed next) the corrected
Boundary B sentence in the same file, rather than silently getting a wrong
result:**
* `bootstrap/SAFETY.md:537` and `:543`.
* `bootstrap/DEPENDENCY_BUDGET.md:117` and `:168`.
* `bootstrap/tests/fixtures/skills/README.md:21` reads the same way (a fixture
  harness's own description of its test trigger); found by the same grep, not
  part of the seven sites above but classed with this group on inspection.

Both classes describe a command this guard now refuses; only the first is
proposed for correction, because "documentation polish" undersells what the
runbook and release-process entries are — procedures a Maintainer executes
under a ceremony, and discovering the refusal mid-ceremony is exactly the "a
refusal arrives during setup, looks like a configuration annoyance, and
invites routing around it" hazard `AGENTS.md` names about the gate anchor.
The second class is left as prose: it documents a trigger, not a recipe, and
the guard's refusal plus (once B1 lands) the corrected sentence elsewhere in
`AGENTS.md` are enough for a reader who actually runs the command to
self-correct.

**`AGENTS.md:326` is not a fourth live-instruction site.** It is the
canonical-pair sentence itself — "Cairn's ordinary pair is `python -m pytest
bootstrap/tests --quality-gate-shuffle-seed=0` followed by…" — the exact
sentence B1 appends its corrective sentence immediately after, in the same
bullet. A reader reaching line 326 reaches B1's clarification in the same
breath; no separate action is needed there.

**Not yet authorized.** Correcting the three live-instruction sites is a
touched-file-set expansion beyond Revision 5's Scope — the same kind the
A4/A5 and (originally) A6/A7 expansions above needed the Maintainer to allow,
and this one has not been asked for or granted. **Known omission, with a
revival condition** (folded into Author-accounting's Known-omissions
paragraph below): if the Maintainer authorizes the expansion before or during
Chunk B, add three rows — one per file — prefixing the cited command with
`CAIRN_FULL_SUITE=1 `; if not, these three sites ship stale, and the omission
is revived the first time a person or Maintainer follows one of them
literally and is refused.

### Chunk C — Security Review of the implementation

**Not a commit; an explicit, owner-attributed review step.** The proposal's
own `Assurance path: high-assurance` and its Decision's "implementation
carries a Security Review trigger" commit this plan to a **distinct**
Security Review of Chunk A's landed bytes, separate from and in addition to
the ordinary Internal code-review floor (`AGENTS.md` > "Review": "A high-risk
surface named below still takes its own Security Review; that trigger is
untouched by this routing" — and every review round on the source proposal
itself states "the distinct plan/code Security Review remains owed," because
the proposal's own S1-S5 security-preflight sections are the *author's*
accounting, not an independent read).

**Owner: a different-agent-type or human reviewer, never the implementing
agent** (the same floor as every other Security Review in this repository,
e.g. `dev/plans/archive/gate-reanchor-preflight.md`'s External-security-lens
round). Scope: the exact landed bytes of Chunk A (`bootstrap/tests/conftest.py`
and `scripts/quality_gate.py`), read against Revision 5's S1-S5 security
preflight (who supplied the input; can the guard fail; what fires it, over
what; which way it breaks; who still wins) as the baseline the implementation
is checked against, not re-derived from scratch. This pass lands as a
`## Code review -- <reviewer> -- YYYY-MM-DD` section per the template (this
plan does not invent a second review-section vocabulary); it is explicitly
named here so its owner and its trigger are visible before implementation
starts, not discovered at archive time.

**Relationship to the re-anchor's own launcher review, named rather than
conflated.** `bootstrap/REANCHOR_RUNBOOK.md`'s own prerequisites separately
require "the instantiated launcher" to have been produced by "the External
Security review that read it" — a precondition of running the re-anchor
ceremony *at all*, independent of this proposal. Whether one Security Review
pass can discharge both this plan's own trigger and the launcher precondition
for Chunk D's batched ceremony is a **question for the Maintainer to
disposition, not a decision this plan makes** — the two obligations have
different subjects (this plan's implementation bytes; the re-anchor
launcher's own bytes) and may or may not be the same reviewed artifact
depending on how the Maintainer times the ceremony.

### Chunk D — the gate re-anchor ceremony

**Maintainer-owned; not performed by an implementing agent** (`AGENTS.md` >
"High-risk surfaces" > "The local interpreter binding" and the
`gate-reanchor-preflight.md` precedent both bind this: Phase 0 / Phase 4 /
Phase 5 of `bootstrap/REANCHOR_RUNBOOK.md` are the Maintainer's own act,
never scripted by the agent whose work is being anchored).

**Four `FROZEN-MODIFIED` entries, not two — an earlier draft of this plan
undercounted by half.** Chunk A touches **six** paths — five once A6 stopped
adding a distinct file of its own (see Scope) and became a row inside A3's
file, plus the sixth from A7 — and each was checked directly against
`bootstrap/tests/_gate_manifest.py::_frozen_files` rather than inferred from
the globs: `bootstrap/tests/conftest.py` (A1), `scripts/quality_gate.py` (A2),
`bootstrap/tests/test_security_check.py` (A4) and
`bootstrap/tests/test_quality_gate_order_independence.py` (A5) are all in the
frozen set, so landing Chunk A produces **four** `FROZEN-MODIFIED` entries
against the current anchor at `refs/cairn/gate-anchor`.
`bootstrap/tests/test_broad_run_guard.py` (A3, and A6's regression-guard row
alongside it) is new and takes a different code path entirely: `FROZEN-NEW` as
a note once tracked, or `FROZEN-UNTRACKED` as a **HOLD** in ceremony mode while
still untracked. `tools/suite_cost.py` (A7) carries no freeze obligation at
all — no glob in `_gate_manifest.py` covers `tools/`. A Maintainer walking
into Chunk D expecting two entries would meet four holds and one note. Derive
the set at ceremony time regardless — including from this paragraph. That does
**not** block ordinary `pytest bootstrap/tests` or `scripts/quality_gate.py`
runs — verified by reading
`bootstrap/tests/test_gate_preflight.py::TestPublicCli::test_check_runs_against_the_live_repo_and_reports`,
which already tolerates a refusal exit (0, 1, or 2) from the live-tree gate
check rather than requiring a clean pass, because the live tree is expected
to refuse until the next supervised anchor. It **does** mean the
differential-oracle gate reports `FROZEN-MODIFIED` for all **four** files
until re-anchored, and the Decision's Security Review trigger plus this
contract surface both put Boundary B verification for this plan at **full**,
never bounded (see Verification below).

**A re-anchor is already independently owed, and batching is presented, not
decided here.** `dev/PLANNING.md` > "Queued" carries the AST attestation
baseline row (`bootstrap/tests/test_ast_attest.py` reports CHANGED symbols in
`bootstrap/_scaffold/upgrade.py` and `config.py`, filed 2026-08-19, Maintainer
already authorized re-anchor over revert), and the same "Queued" section's
`[TRU-4]` entries name the interpreter-binding re-pin and two stale
install-contract artifacts as further debts already flagged to "join the
re-anchor ceremony already owed rather than creating a new obligation." This
plan's four `FROZEN-MODIFIED` entries are one more item for that same batched
sitting — **whether to actually batch them into one `bootstrap/reanchor.sh`
run is the Maintainer's call**, made when the ceremony is scheduled, not an
outcome this plan assumes.

**Procedure**: `bootstrap/REANCHOR_RUNBOOK.md` (the differential-oracle gate
anchor — distinct from `bootstrap/AST_BASELINE_RUNBOOK.md`, which governs the
unrelated AST attestation baseline debt named above; both may be run in the
same sitting but are not the same mechanism, per `AGENTS.md` >
"Operational pitfalls" > "AST attestation baseline"). Derive the expected
`FROZEN-MODIFIED` set against the committed anchor at the time the ceremony
runs, rather than carrying a figure forward from this plan.

## Acceptance criteria

* **Tests that must pass**: the full row mapping under Chunk A above (A3-A5),
  plus the full standing suite (Boundary B is `full` — see Verification).
* **Doc updates that must land**: Chunk B1 and B2, both hand-authored. No
  generated or snippet-synced doc surface is touched.
* **Examples / smoke checks required**: **N/A** — no runnable example or
  public-facing smoke artifact beyond the tests themselves; the guard's
  public path *is* a pytest session, exercised through a real invocation in
  Chunk A's tests rather than by calling an internal helper directly (mirrors
  the proposal's own "public-path → test mapping" evidence commitment).
* **Inbound path-link updates**: this plan's own opening commit moves the
  source proposal to `dev/proposals/archive/`; no other `dev/` doc links that
  filename directly (per `AGENTS.md`, `PLANNING.md`/`NEXT_SESSION.md` cite by
  stem, not path, so an archive move needs no update there).

### Author-accounting — invariants, failure modes, edge cases

**Invariants** — the 14 rows in the row-mapping table above, each bound to a
named prospective test and a named file: Revision 5's own 11 evidence-table
invariants, all still mapped, plus three this plan's own Maintainer-authorized
expansions add — the refused-session regression guard (A6), the
cost-figure/refusal-count falsifier (A7), and the guard against the tests'
own child environments inheriting an exemption token they should not carry.
No invariant in Revision 5's Evidence table is left unmapped; if a plan
reviewer finds one, that is a blocking gap, not a nice-to-have.

**Failure modes** — unchanged from Revision 5's own S1-S5, restated because
this is a plan, not a fresh derivation: the guard fails **toward refusing**
(a guard bug blocks verification rather than silently permitting an
unmeasured run) except for the one bound exception (a pre-existing collection
failure stands down the guard entirely, because the failure is the stronger
evidence). `pytest_collection_finish` is chosen over
`pytest_collection_modifyitems(trylast=True)` specifically because `trylast`
is only a priority among equal-priority implementations and does not
guarantee the guard sees the post-filter item list — Revision 5's own
falsifier (row "the guard sees the final item list" above) is what makes this
a tested claim rather than an assertion.

**Edge cases** — the `--noconftest` bypass (row 11) is accepted and pinned,
not closed; a probe exists specifically so prose cannot drift back to
claiming universal coverage. In-process `pytest.main()` calls inside a test
fall under the 40-file threshold by construction and are unaffected —
deliberate, not tested separately (Revision 5's own "Known omissions").

**Which chunk runs the mutation, and which gate command fires the check**
(the two questions a chunked plan re-answers from the proposal's S2/S3):
Chunk A alone writes the guard and the child-environment fix; no other chunk
touches executable bytes. The check fires on **every** `pytest` session over
`bootstrap/tests` that loads Cairn's conftest, in any harness, for any agent
or human. `--noconftest` is the one **known** exception, and calling it
"documented" would be false: grepping the tree outside `dev/proposals/`,
`dev/plans/`, and `dev/PLANNING.md`'s own `[TRU-4]` row (`d67f2fd`, this
plan's own Maintainer consultation, which necessarily names the flag) returns,
as_of 2026-08-20, **zero** further occurrences of `noconftest` — no doctrine,
no `AGENTS.md`, no `bootstrap/SAFETY.md`, no docstring. Revision 5 commits to a
**probe** that pins the bypass so prose cannot drift back to claiming universal
coverage; it commits to no document, and no chunk here lands one. The test name
was trimmed to match (it previously promised `_and_the_bypass_is_documented`,
a second property nothing in this plan delivers — and pinned two properties in
one name, against the naming rule in `AGENTS.md` > *Project-specific
conventions*). **Asked and answered: the Maintainer kept Revision 5's
probe-only treatment**, and routed the underlying hazard to `dev/PLANNING.md`
as its own `[TRU-4]` row instead. The reason matters more than the disposition:
`--noconftest` also disables the **release-mode outcome rule** this same file
carries — the control that refuses a release when a security gate skipped
rather than passed — so it is a release-trust exposure that predates this plan
and does not belong filed under a cost-guard change. **Do not document the flag
here.** A note reading "`--noconftest` bypasses the guard" would advertise the
release control's off-switch to the one audience motivated to get past a
refusal. Both S2/S3 answers are otherwise unchanged from the proposal's;
chunking does not narrow or widen either.

**Known omissions**, carried forward rather than re-derived: the routing
decision ("verification is not delegated; return it to the spawner") is
stated in the guard's refusal message but not enforced — a conftest has no
`agent_id` to enforce it against; no durable record of an override exists (a
silent pass-through) — the diagnostics proposal's ledger is what would make
an override countable, and this plan does not add one; a broad run that has
already failed receives no cost prompt at all, which is the correct
precedence but does mean some broad runs go uncounted; a human is refused
too, by design, since a mechanism that could tell them apart is one an agent
could claim to be. **New this revision:** three live, non-`dev/` documents
name a bare `python -m pytest bootstrap/tests` as a literal instruction and
are not touched by Chunk B — `docs/release-process.md:78`,
`bootstrap/AST_BASELINE_RUNBOOK.md:126`, and `AGENTS.md:487` (see Chunk B's
own "Live commands…" subsection for the full enumeration, the disposition
reasoning, and the four sites classed as trigger prose rather than
instruction and left alone). Correcting the three is a touched-file-set
expansion this plan has not asked the Maintainer to authorize. Revival
condition: authorize and add three one-line rows to Chunk B, or leave as-is
until a person or Maintainer following one of the three literally is refused
and the omission is revived from that report.

## Verification

**Boundary A — reviewed mapping.** During Chunk A implementation: the 14
tests named in the Chunk A row mapping, plus
`bootstrap/tests/test_security_check.py` (the two updated tests and their
surrounding class), plus `bootstrap/tests/test_quality_gate_order_independence.py`
(the new additive-copy test and the existing seed-contract tests it sits
beside, to confirm nothing there regresses), plus
`bootstrap/tests/test_suite_ledger.py` — which exists by the time this plan
starts, and pins the row-per-session and node-accounting invariants this
guard's refusal path perturbs. During Chunk B: `python
scripts/quality_gate.py --sub neutrality` (which covers B2 only — see Chunk B),
`python scripts/check_cairn.py`, and the standing gates for the surface
Chunk B touches — `bootstrap/tests/test_verification_boundaries.py`,
`bootstrap/tests/test_comprehension_floor.py`, and
`bootstrap/tests/test_scope_reduction_trap.py` (the twin only).

**Boundary B — mode: `full`, not bounded, and this is not a close call.**
Four of the changed files are gate-frozen (a contract-surface trigger on
their own — see Chunk D's re-anchor accounting), this plan's Decision carries
an explicit Security Review trigger (a trust-ceremony surface), and the
change can alter a session's exit status from the one file that already owns
the release-gate outcome rule — three independent reasons the
verification-boundaries fence in `AGENTS.md` refuses bounded mode, any one of
which would be sufficient alone.

**The self-referential bootstrapping detail, stated rather than left
implicit.** Once Chunk A is on the branch being verified, an *unmarked*
`python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` is exactly
the invocation the new guard refuses (bootstrap/tests spans far more than 40
files). Boundary B's run for **this plan's own Chunk A/B commit** must
therefore carry the override:

    CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0
    python scripts/quality_gate.py --sub neutrality --sub redundancy

exactly the form Chunk B1's new `AGENTS.md` sentence documents. A Boundary B
record for this plan that uses the bare form is not just non-canonical, it is
a run that the code under test would itself have refused — a strong falsifier
of the implementation if it somehow returned exit 0 unmarked.

**Static and prose gates**: `python scripts/quality_gate.py --sub neutrality
--sub redundancy` (already folded into the pair above); `python
scripts/check_cairn.py` once, over the final state of `AGENTS.md`,
`templates/core/AGENTS.md`, and this plan file; `python scripts/claim_check.py
dev/plans/full-suite-interception.md` at authoring time (already run before
this plan's opening commit — see the report accompanying that commit).

Only after that stable full run, append
`## Implementation verification -- <agent> -- YYYY-MM-DD` per the template's
mandatory field list (Boundary B mode `full`; tested commit; reviewed range;
interpreter/runtime; pre/post clean state; the command table; non-pass
disposition; plan-specific acceptance commands; known omissions).

## Code review

*Filled in after implementation commits land.* Two obligations, not one:
the ordinary Internal code-review floor (not the implementing agent — a
same-type agent in an independent context), **and** the distinct Security
Review named in Chunk C above, owed independently of the code-review floor
and not discharged by it.

## Lasting-truth migration

*Filled in at archive time.*

## Plan review -- Claude (Internal, fresh-context subagent) -- 2026-08-20

Reviewed commit: 1603b4f50d30b1163539429683047bc17fa5d670
Target: the whole plan as it stands -- Source proposal, Proposed paths, Scope
(both Contract expansions and the sibling-sequencing analysis), Documentation /
doctrine surface, Sequence (Chunks A-D including the A1-A7 table and the
13-row invariant mapping), Acceptance criteria, Author-accounting, and
Verification
Prior findings: none
Assurance path: high-assurance
**Tier**: Internal
**Findings**: raised
**Model**: Claude Opus 5 (claude-opus-5)

**Verdict: REVISE** -> `revising-plan`. Four blocking findings, six
non-blocking. The mechanism is right, the sequencing decision is right, and
most of the plan's own factual claims about the code it edits are *exactly*
right -- I re-derived nine of them and every one held to the digit. What
fails is narrower and specific: one of the two Maintainer-authorized
expansions rests on a premise the sibling's accepted contract already
falsifies, the guard's own tests are specified in a way the plan's own
mandated Boundary B invocation makes vacuous, Chunk B's verification note
denies a standing gate that exists, and the change breaks three live
operational commands that no chunk and no omissions list mentions.

**Checker note, declared rather than silenced.** I was briefed to expect
`python tools/lifecycle_planner.py scan` to report this section as
author-written -- the known comparator defect filed at `dev/PLANNING.md` >
`[TOOL]`, where the independence comparator takes the byline's first word and
Cairn's Internal floor is "the same agent in a fresh session", so an honest
Internal byline collides with the author's by construction. **It did not fire
here**, and the reason is worth recording: `_independent_review` is consulted
only on the `awaiting-decision` branch of the *proposal* status machine
(`tools/lifecycle_planner.py:4404-4410`). A `## Plan review` section on a plan
moving to `revising-plan` is never put to that comparator at all. So the three
correct reviews it fired on today were proposal reviews; plan reviews are
outside its reach. The scan on this artifact returns clean ("all 6 artifact(s)
structurally sound"). Either way the byline above is my real identity and my
real running model -- writing a different one to dodge a flag would be a false
attribution on a record whose integrity is its attribution.

### Blocking findings

**PR1 -- Row A6 is built on a premise the sibling's accepted contract already
refutes, and its falsifier cannot fail either way. [blocking]**

The plan states, in three places (Scope > "A second expansion"; the sequencing
bullet at "must pin what the sibling's ledger records"; row A6), that a session
this guard refuses is classified `full` by the sibling's `scope` classifier,
because "its `full` conditions test for narrowing options, early stop (`-x` /
`--maxfail` / interrupted) and collection errors, none of which a `UsageError`
at collection-finish trips."

That enumeration is incomplete. The sibling's operative contract
(`2026-08-19-claude-suite-run-diagnostics`, Revision 5 > "Scope -- both
channels, combined") makes `full` require **both** an exact-argv-family match
**and** a set of resolved postconditions, and that postcondition set reads:

> `scope_basis.targets` resolves to the suite root; `inipath` false;
> `addopts_set` and `plugins_set` false; **`collected > 0` and `executed > 0`**;
> `deselected == 0`; `collection_errors == 0`; **`not_run == 0`**; `interrupted`
> false; `truncated` false.

A refused session has `executed == 0` by construction -- the refusal fires at
`collection_finish`, before any test runs -- so `executed > 0` fails and
`not_run == 0` fails with it. `full` is therefore already unreachable, and
since the run's targets are the suite root rather than a recognized strict
subset, the classifier already resolves **`unknown`**. This is not an artifact
of one revision: the same two postconditions are present in the sibling's
Revision 3 and Revision 4, and the sibling *plan*'s row A3 commits to
implementing "both channels -- exact-argv-family membership *and* resolved
postconditions."

Three consequences, and the third is the one that matters most:

1. **A6 as written is a no-op at best.** The behaviour it asks for is the
   behaviour the accepted sibling already produces. At worst it is a net
   negative: a hand-written special case for a shape the general rule already
   covers, added to a classifier whose stated virtue is that it guesses
   nothing.
2. **The headline cross-plan hazard is overstated.** The sequencing bullet says
   a refused run "writes a row with ... `scope` = `full`", that this "silently
   deflates the very measurement the ledger exists to produce", and that a bare
   canonical invocation is "*guaranteed*" to produce one. The row is written --
   correct -- but it carries `unknown`, so the `full`-runs-per-day figure the
   reader reports is not corrupted by mislabelled rows.
3. **The falsifier cannot fail.** `test_a_refused_session_is_scoped_unknown` is
   declared directional on the grounds that "the same tree under
   `CAIRN_FULL_SUITE=1` writes `full`, so the test fails if the classifier
   stops distinguishing them." The two cases *are* distinguished -- by
   `executed > 0`, which is exactly what differs between a refused session and
   an allowed one. So the test passes identically with A6 landed, with A6
   reverted, and with A6 never written. It pins the sibling's pre-existing
   postcondition, not this plan's change. That is the same defect class the
   plan itself caught and fixed in the `len(session.items)` row.

**What I am not doing.** I am not recommending A6 be dropped. The Maintainer
authorized this expansion ("I'll take your recommendation on Decision 3. b +
c"), accepted scope is a floor in both directions, and a plan reviewer cannot
create the authority to narrow it by calling the remainder unnecessary. What
the plan owes is a corrected derivation and a return trip: re-derive the
refused-session classification against the sibling's actual postcondition set,
state plainly that `unknown` already holds and why, and put the disposition
back to the Maintainer -- whose "b + c" was chosen against a recommendation
whose (c) half rested on this premise. The two defensible landing places are
(i) keep A6 as a *regression test only* -- a row in
`test_broad_run_guard.py` pinning that a refused session classifies `unknown`,
with its docstring naming `executed > 0` as the mechanism so a later
postcondition edit cannot silently remove the property -- and no classifier
code change; or (ii) keep the code change if the Maintainer wants belt-and-
braces, in which case the plan must supply a falsifier that can actually
distinguish A6's branch from the postcondition (e.g. a constructed row where
the postconditions would pass but the session was refused). Either way the
premise text in all three locations has to be corrected before implementation
reads it.

**A7 survives, on a corrected and narrower premise.** Excluding refused rows
from cost aggregation and reporting the refusal count separately is still
worth doing -- a refused row carries a real `wall_s` and an empty `by_file`,
so any figure derived from session wall time is pulled toward zero by a run
that never ran, and the refusal count is genuinely new information the reader
does not otherwise surface. But note that the sibling's reader derives cost
concentration and trend **from `by_file`**, which is empty for a refused
session. So the byte-identity half of
`test_refused_sessions_are_excluded_from_cost_and_counted_separately` may pass
vacuously for exactly those three tables; the half that can fail is the
refusal count. Say which figures actually admit a refused row, and pin the
falsifier to those.

**PR2 -- Under this plan's own mandated Boundary B invocation, the guard's
exemption and allow rows pass vacuously and its refusal rows fail. [blocking]**

The plan correctly states that Boundary B for this change must run as
`CAIRN_FULL_SUITE=1 python -m pytest bootstrap/tests
--quality-gate-shuffle-seed=0`. It does not follow that through to the guard's
own tests, and the consequence is severe in both directions.

Every row in the Chunk A mapping exercises the guard through a real pytest
subprocess -- the plan says so ("the guard's public path *is* a pytest
session, exercised through a real invocation ... rather than by calling an
internal helper directly"). The idiom this repository already uses for that,
in the very file row A4 extends, is:

```python
def _child_pytest(root: Path, token: str | None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.pop(security_check.RELEASE_GATE_ENV, None)
```

-- `test_security_check.py:669-678`. It inherits the parent environment and
scrubs exactly one token. A guard test written to that pattern, run under the
Boundary B invocation this plan requires, hands every child
`CAIRN_FULL_SUITE=1`. Then:

* `test_a_run_over_the_file_threshold_is_refused_regardless_of_selector`,
  `test_the_file_threshold_boundary_is_exact` (the 41-file half),
  `test_a_pre_existing_collection_failure_keeps_its_own_exit_code` (its clean
  41-file control) and `test_the_guard_refusal_follows_a_late_deselection` all
  **fail** -- loudly, which is the tolerable direction, but they fail in the
  one run the plan makes mandatory, so Boundary B cannot be recorded.
* `test_a_run_at_or_under_the_file_threshold_is_never_refused` (all seven
  parametrizations), `test_the_override_token_allows_a_full_run`,
  `test_release_mode_is_exempt_from_the_guard`,
  `test_collect_only_is_exempt_from_the_guard` and
  `test_noconftest_bypasses_the_guard` all **pass without testing anything** --
  every one asserts "not refused", and the inherited override makes "not
  refused" true unconditionally. That is the silent direction, and it is five
  of the thirteen rows.

The same applies to `CAIRN_RELEASE_GATE_ACTIVE` during a release ceremony,
where `bootstrap/security_check.py::run_suite` runs the whole suite with the
token set: every refusal row inverts.

**Required.** State in the Chunk A mapping that `test_broad_run_guard.py`
constructs each child environment **explicitly** -- both exemption tokens
popped by default, and set only on the rows that are about them -- and add one
meta-row that fails if a refusal-expecting child is ever handed an exemption
token. Without that, a criterion the plan calls falsifiable is satisfied by
the environment rather than by the code, which is the defect the plan's own
`len(session.items)` correction was written to avoid.

**PR3 -- "B1 has no automated gate at all" is false, and the Boundary A mapping
omits the standing gates for the surface Chunk B touches. [blocking]**

The plan's Chunk B verification note is right about the thing it measured and
wrong about the conclusion it draws. I reproduced the measurement exactly:
`_NEUTRALITY_FILE_SUFFIXES` has eight directory keys, `_walk_neutrality_files`
walks only those, and importing it against this tree yields **181 files, root
`AGENTS.md` not among them, `templates/core/AGENTS.md` among them**. The
neutrality sub-gate does not scan root `AGENTS.md`. That part is exact and
well caught.

But "B1 has no automated gate at all" does not follow, and it is wrong.
`bootstrap/tests/test_verification_boundaries.py` opens with

```python
SELF_AGENTS = ROOT / "AGENTS.md"
ADOPTER_AGENTS = ROOT / "templates" / "core" / "AGENTS.md"
```

and asserts over **both**, specifically over the *Verification boundaries*
text Chunk B edits: `test_both_operational_surfaces_fail_to_full`,
`test_installed_operational_rule_is_project_general`, and the
`_BOUNDED_OBLIGATIONS` block. `bootstrap/tests/test_comprehension_floor.py`
likewise parametrizes over `("templates/core/AGENTS.md", "AGENTS.md")`, and
`test_scope_reduction_trap.py` maps the twin as a governing surface.

Two consequences:

1. The plan's Boundary A mapping for Chunk B lists only `--sub neutrality` and
   `check_cairn.py`. `AGENTS.md` > Verification boundaries > A requires "the
   tests and public-path probes mapped by the reviewed plan, **plus standing
   gates for every touched surface**". `test_verification_boundaries.py` and
   `test_comprehension_floor.py` are the standing gates for this surface and
   must be in the mapping.
2. The reviewer-obligation framing for B1's vendor-neutrality stays correct and
   should be kept -- it is a genuinely good catch -- but it must be stated as
   "no *neutrality* gate covers root `AGENTS.md`", not as "no gate at all",
   which tells the implementer to skip tests that do govern the bytes they are
   about to change.

One live hazard rides along: `test_installed_operational_rule_is_project_general`
denies the adopter file the tokens `bootstrap/tests`, `scripts/quality_gate.py`,
`Python 3.13` and `Cairn's ordinary pair`. `CAIRN_FULL_SUITE` is **not** in
that list. So B2's latitude -- "no literal `CAIRN_FULL_SUITE` token unless the
implementer judges the concrete token itself is project-agnostic enough to
keep" -- has no check behind it in either direction: a Cairn-specific token
would ship to adopters and every gate would stay green. Either decide it in
the plan (my read: the twin must not carry it; the candidate sentence already
avoids it) or extend the denylist as part of B2.

**PR4 -- Three live operational commands become refused commands, and no chunk
or omissions list accounts for it. [blocking]**

The guard refuses a bare `pytest bootstrap/tests`. Chunk B updates exactly one
sentence, in the Boundary B bullet of two files. These live, non-`dev/`
documents name the bare form and are not touched, not deferred, and not listed
as a known omission:

| file:line | text | what breaks |
|---|---|---|
| `AGENTS.md:487-488` | "Run the suite with `python -m pytest bootstrap/tests`." | **The same file Chunk B1 edits.** After B1, `AGENTS.md` carries a corrected Boundary B sentence and, 160 lines later, an uncorrected instruction naming a command that now exits 4. |
| `docs/release-process.md:78` | `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0` under "## Checks to run" | A human typing the documented release-sweep checks, outside `security_check.py`, gets no release token and is refused. |
| `bootstrap/AST_BASELINE_RUNBOOK.md:126` | `PYTHONDONTWRITEBYTECODE=1 python -m pytest bootstrap/tests -q`, Step 4 "apply, verify, commit" | A **Maintainer-run ceremony step** refuses -- and this plan's own Chunk D routes the Maintainer to the neighbouring re-anchor runbook in the same sitting. |

Plus trigger prose that stops being true: `bootstrap/SAFETY.md:537` and
`bootstrap/SAFETY.md:543`, and `bootstrap/DEPENDENCY_BUDGET.md:117` and
`bootstrap/DEPENDENCY_BUDGET.md:168`, each describe a check as "run by a
person typing `python -m pytest bootstrap/tests` -- Cairn has no CI", and
`bootstrap/tests/fixtures/skills/README.md:21` says the same. `AGENTS.md` >
*Verifying claims* is explicit that a document describing a check says what
runs it and that the named trigger is checked by opening it: after this change
the named trigger, opened, refuses.

Grepping for this is what the plan already did for `noconftest`, and the same
grep run one directory wider finds these. Note that the runbook and
release-process entries are not documentation polish -- they are procedures a
Maintainer executes under a ceremony, and discovering the refusal mid-ceremony
is precisely the "a refusal arrives during setup, looks like a configuration
annoyance, and invites routing around it" hazard `AGENTS.md` names about the
gate anchor.

**Required.** Enumerate them, and take a disposition. Correcting them is a
touched-file-set expansion beyond Revision 5's Scope, so it is the Maintainer's
to allow -- exactly as the A4/A5 and A6/A7 expansions were. What the plan may
not do is land the guard with the residue unnamed. If the Maintainer declines
the expansion, they belong in *Known omissions* with a revival condition, not
in silence.

### Non-blocking findings

**PR5 -- Chunk D contradicts its own corrected count, twice, and the path
count is now stale.** The section leads "**Four `FROZEN-MODIFIED` entries, not
two -- an earlier draft of this plan undercounted by half**", then says
"the differential-oracle gate reports `FROZEN-MODIFIED` for **both files**
until re-anchored" and "This plan's **two** `FROZEN-MODIFIED` entries are one
more item for that same batched sitting". Both are leftovers from the
undercount the paragraph exists to correct, and they sit in the one section
whose stated purpose is to stop a Maintainer walking in expecting two.
Separately, "Chunk A touches five paths" predates A7: it is six now. I
re-derived the whole accounting against
`bootstrap/tests/_gate_manifest.py::_frozen_files` -- `conftest.py`,
`quality_gate.py`, `test_security_check.py` and
`test_quality_gate_order_independence.py` are all in the frozen set (203
entries); `test_broad_run_guard.py` and `tools/suite_cost.py` are not, the
latter because no glob covers `tools/`. So **four** FROZEN-MODIFIED plus one
new file on the FROZEN-NEW / FROZEN-UNTRACKED path is correct, and A7 adds a
sixth touched path that carries no freeze obligation. Fix the two stale
sentences and the path count; the conclusion stands.

**PR6 -- The "eleven" invariant count is stale by two.** Author-accounting
opens "the eleven rows in the Chunk A table above" and Boundary A says "the
eleven tests named in the Chunk A row mapping". The mapping carries **13**
rows since A6 and A7 were folded in. (Revision 5's own Evidence table has
eleven, which is presumably where the figure came from and why it read
correctly before the amendment.) The internal row references survive the
change -- "row 11" for `--noconftest` and "the row-10 falsifier" for the
additive copy are both still right -- so this is a count to correct, not a
mapping to rebuild.

**PR7 -- The A4 allowance summary is narrower than what A4 actually does.**
The plan writes its own gloss on the Maintainer's authorization: "What the
allowance covers: rows A4 and A5 as written -- correcting the docstring and
comment that A2 falsifies, and adding the additive-copy falsifier for A2's own
change. It does not open those two files to unrelated edits." But the row
mapping places a **third** edit in `test_security_check.py`: the new
`test_a_release_refused_outcome_is_not_masked_by_the_guard`, "(extends the
existing `_quality_gate_tree` fixture family)". I checked the history -- that
assignment predates the allowance commit `e0ab524`, so the Maintainer's "do
A4/A5" plausibly covered it -- but the plan's own summary of what was
authorized omits it while simultaneously forbidding unlisted edits to that
file. An implementer reading the Scope section and then the mapping gets two
answers. Name the third edit in the gloss, or move the test to A3.

**PR8 -- The `--noconftest` absence figure is stale by one.** "grepping the
tree outside `dev/proposals/` and `dev/plans/` returns **zero** occurrences of
`noconftest`" is no longer true: `dev/PLANNING.md:1599-1617` carries the
`[TRU-4]` row this plan's own Maintainer consultation created (`d67f2fd`). The
enumerated claim that follows -- "no doctrine, no `AGENTS.md`, no
`bootstrap/SAFETY.md`, no docstring" -- I verified and it still holds exactly.
Re-scope the figure or date it; the reasoning it supports is unaffected, and
the decision not to document the flag is well argued and I would not disturb
it.

**PR9 -- B2's insertion point is described ambiguously.** The cell says the
twin's bullet "currently ends '…run against a clean, unchanged commit under
the project's configured interpreter/runtime.'" That phrase ends a *sentence*;
the bullet continues for another eight lines with the bounded-mode contract
(`templates/core/AGENTS.md:309-320`). Read as written, an implementer appends
after the bounded-mode text rather than at the position corresponding to B1's.
One word ("the equivalent sentence currently ends…") fixes it.

**PR10 -- Two rows are one-directional.** `test_noconftest_bypasses_the_guard`
and `test_the_override_token_allows_a_full_run` both assert only that the
guard does *not* fire, so a guard that never fires satisfies both. Other rows
catch that today, but under PR2's environment hazard they are the rows that go
quiet. Give each the control that refuses -- the same invocation with the
conftest loaded, and the same tree without the token -- in the manner the
`--collect-only` and release-mode rows already do.

### What I verified and found correct

Recorded because a plan that has been through an adversarial audit deserves to
have its surviving claims confirmed rather than re-litigated, and because each
of these is a claim a wrong implementation could have inherited:

* **The neutrality measurement is exact.** 181 files scanned; root `AGENTS.md`
  absent; `templates/core/AGENTS.md` present. Reproduced by importing
  `_walk_neutrality_files` against this tree.
* **Every line citation in the sequence table holds.**
  `_run_order_independence` at `scripts/quality_gate.py:147`; its
  `subprocess.run` at `:164`; `os` genuinely not imported (`import argparse,
  ast, re, subprocess, sys` only), so A2's "add `import os`" is right.
  `test_the_release_token_survives_the_real_grandchild_launcher` at
  `test_security_check.py:806`, and its docstring does assert the middle link
  launches pytest "with **no** `env=` of its own ... by *inheritance*"; the
  parallel comment sits at `:458-460`. A2 falsifies both, exactly as claimed.
* **The pytest analysis is right, in the installed pytest.** `wrap_session`
  (9.0.3) assigns `initstate = 2` before `doit(config, session)`, the `except
  UsageError` clause sets `ExitCode.USAGE_ERROR` and re-raises, and the
  `finally` block calls `pytest_sessionfinish` whenever `initstate >= 2`. A
  refused session does reach the sibling's ledger append. (This is what makes
  PR1 a classification question rather than a missing-row question.)
* **The re-anchor set**, per PR5 above -- four modified, one new, derived
  directly from `_frozen_files` rather than from the globs.
* **conftest.py carries exactly the five hooks the plan names** today
  (`pytest_addoption`, `pytest_collection_modifyitems`,
  `pytest_runtest_logreport`, `pytest_collectreport`, `pytest_sessionfinish`,
  plus `_release_mode` / `_record_refused_report`), and none is named
  `pytest_collection_finish`. `_release_mode()` is the strict-equality
  predicate the plan relies on. The instruction to re-read the landed file at
  Chunk A's start rather than trust this list is the right call and should
  stay.
* **115 `test_*.py` files** under `bootstrap/tests`, matching the ~115 figure
  the 40-file threshold is calibrated against.
* **`bootstrap/scaffold.py --manifest` emits 115 rows and none under
  `bootstrap/tests`** -- and I confirmed the instrument produces output before
  trusting the zero, per `AGENTS.md` > "Confirm the instrument before trusting
  an absence".
* **`test_gate_preflight.py::TestPublicCli::test_check_runs_against_the_live_repo_and_reports`**
  does assert `r.returncode in (0, 1, 2)`, so the FROZEN-MODIFIED state will
  not redden the suite.
* **`6fcc9bd`** is the Maintainer amendment ratifying `Plan review:
  required(Internal)`; **`d67f2fd`** is the `[TRU-4]` filing. The decision to
  omit `Inherited proposal basis:` while the amendment's commit body says
  "inheriting the proposal basis" is correctly handled and correctly explained
  -- the header states the authority plainly instead of routing it through a
  mechanism the checker refuses.
* **`python scripts/claim_check.py dev/plans/full-suite-interception.md`** --
  clean, with the three forward references correctly exempted by the `Proposed
  paths:` declaration.
* The Chunk A coupling argument (guard and child-env fix in one commit or the
  quality gate refuses itself), the `pytest_collection_finish`-over-`trylast`
  reasoning, the Chunk C / Chunk D ownership fences, the refusal to fold the
  re-anchor batching decision, and the replaced `len(session.items)` falsifier
  are all sound and I would not touch any of them.

### Coverage

**Read in full**: the plan; `dev/plans/_template.md` plan-review section and
scope-delta doctrine; `AGENTS.md` (lifecycle, review, verification boundaries,
verifying claims, project conventions, high-risk surfaces); the source
proposal's Revision 5 and Decision, plus the Revision 1/2/3/4 withdrawn-
commitments ledgers to confirm nothing I flag as missing was deliberately
withdrawn; `dev/plans/suite-run-diagnostics.md`; the sibling proposal's
Revision 5 schema, classifier, guards, failure dispositions and reader
sections.

**Opened and checked directly**: `scripts/quality_gate.py` (neutrality file
set, `_run_order_independence`, imports); `bootstrap/tests/conftest.py` in
full; `bootstrap/tests/test_security_check.py` (`_spy_run`, `_child_pytest`,
`_fixture_tree`, `_quality_gate_tree`, both cited tests);
`bootstrap/tests/test_quality_gate_order_independence.py` in full;
`bootstrap/tests/_gate_manifest.py` (`_frozen_files`, the FROZEN-* labels, the
`--collect-only` collector); `bootstrap/tests/test_verification_boundaries.py`;
`bootstrap/tests/test_comprehension_floor.py`;
`bootstrap/tests/test_gate_preflight.py` (the live-repo CLI test);
`bootstrap/security_check.py` (release token, `run_suite`,
`run_quality_gate`); `_pytest/main.py::wrap_session`; `AGENTS.md` and
`templates/core/AGENTS.md` Verification-boundaries bullets;
`docs/release-process.md`; `bootstrap/AST_BASELINE_RUNBOOK.md` Step 4;
`bootstrap/SAFETY.md` and `bootstrap/DEPENDENCY_BUDGET.md` trigger prose;
`dev/PLANNING.md` `[TOOL]`, `[REC]` and `[TRU-4]` rows.

**Commands run**: `python scripts/claim_check.py` on the plan; `python
tools/lifecycle_planner.py board --compact`; read-only `git log` / `git show`
against `6fcc9bd`, `d67f2fd`, `e0ab524` and the plan's own history; targeted
`python3 -c` imports of `_walk_neutrality_files` and `_frozen_files`;
`bootstrap/scaffold.py --manifest`; repository greps.

**Not covered, and why**: I did not run the test suite, in either form. No
implementation exists to run; verification is not delegated to a reviewer at
this stage; and this plan's entire subject is the cost of broad suite runs, so
spending one to review it would be self-refuting. Every behavioural claim above
is from reading source and from targeted probes of *existing* code, never from
executing the change. I did not evaluate the 40-file threshold itself, the
choice of `pytest.UsageError`, or the decision to swap away from the harness
hook -- all settled in Revision 5 and not this plan's to reopen. I did not
review the sibling plan for its own defects beyond the two seams this plan
depends on. I did not attempt the Chunk C Security Review, which is owed
separately and to a different reviewer, nor the Chunk D ceremony.

### Sharpening

**Scope delta**: preserved. Nothing in this review narrows what the plan
delivers. PR1 identifies a premise defect inside a Maintainer-authorized
expansion and routes the disposition back to the Maintainer rather than
resolving it by removal; PR3 and PR4 both *add* obligations. No accepted
outcome from Revision 5 is dropped, deferred, or reclassified by this pass.

## Response to plan review -- Claude (Implementation) -- 2026-08-20

Findings folded straight into the operative cells named below; no amendment
ledger, no replacement cells reproduced here.

| Finding | Disposition | Cell(s) |
|---|---|---|
| PR1 (blocking) -- row A6's premise is false; the sibling's accepted contract already resolves a refused session `unknown` (`executed > 0` / `not_run == 0` postconditions), so A6 as a classifier change is a no-op and its stated falsifier cannot fail. A7 survives on a narrower premise. | Corrected. A6 converted from a classifier-code change to a regression guard that pins the sibling's existing `unknown` resolution, per the Maintainer's disposition ("Sure, I like the regression guard idea"), with a falsifier directional on both halves (refused -> `unknown`; `CAIRN_FULL_SUITE=1` -> `full`). A7 kept, reason corrected to (1) `by_file`-derived trend contamination by a zero-cost refused row and (2) the refusal count's unrecoverability without `exitstatus == 4`; its byte-identity falsifier narrowed to the part that can actually fail. The false premise (sibling resolves refused sessions `full`) swept and corrected everywhere it appeared in operative cells. | Scope > "A second expansion" (fully rewritten); the sequencing bullet "must pin what the sibling's ledger records"; Chunk A table rows A6, A7; row-mapping rows 12, 13; Boundary B mode paragraph ("Both changed files" -> "Four of the changed files", a related stale-count fix found in the same pass). |
| PR2 (blocking) -- under this plan's own mandated `CAIRN_FULL_SUITE=1` Boundary B invocation, refusal-expecting guard tests inherit the token and fail, allow-expecting tests inherit it and pass vacuously; same hazard for `CAIRN_RELEASE_GATE_ACTIVE` in a release ceremony. | Corrected. Added a preface paragraph before the row-mapping table requiring every child pytest environment to be built explicitly (`test_security_check.py`'s `_child_pytest` idiom: `env = dict(os.environ)`, pop both exemption tokens by default, set either only on the row(s) actually about it), and added row 14, a meta-guard asserting a refusal-expecting child never carries either token. | New preface paragraph immediately before "Row mapping"; row-mapping row 14 (new). |
| PR3 (blocking) -- "B1 has no automated gate at all" is false; `test_verification_boundaries.py` and `test_comprehension_floor.py` govern the exact text Chunk B edits, and Boundary A's Chunk B mapping omitted them. Also: no gate blocks a Cairn-specific `CAIRN_FULL_SUITE` token from shipping in B2. | Corrected. B1's cell and the verification-note bullets reframed to "no *neutrality* gate", with the standing gates named (`test_verification_boundaries.py`, `test_comprehension_floor.py`, `test_scope_reduction_trap.py` for the twin) and folded into both Chunk B's own narrative and the Verification section's Boundary A mapping. The `CAIRN_FULL_SUITE`-token question decided in the plan rather than left to implementer judgment: B2's acceptance criterion now states no literal token, matching the candidate sentence, with the denylist gap named as the reason it had to be decided rather than gated. | Chunk B table (B1, B2 cells); "Verification for Chunk B" bullets; new "One live hazard..." paragraph; Verification > Boundary A (Chunk B gates added). |
| PR4 (blocking) -- three live operational commands (not the guard's own mapping) become refused, unaccounted for; grepping wider finds four more trigger-prose sites. | Enumerated and dispositioned, not silently landed. Seven sites classified live-instruction (3: `docs/release-process.md:78`, `bootstrap/AST_BASELINE_RUNBOOK.md:126`, `AGENTS.md:487`) vs. trigger-prose (4: `bootstrap/SAFETY.md:537`/`:543`, `bootstrap/DEPENDENCY_BUDGET.md:117`/`:168`; one further site of the same shape found and noted, `bootstrap/tests/fixtures/skills/README.md:21`). `AGENTS.md:326` resolved as not a separate site -- it is the sentence B1 appends after, in the same bullet. Correcting the 3 live-instruction sites is a touched-file-set expansion **not yet authorized**; recorded as a known omission with a revival condition rather than landed unilaterally or left silent. | New "Live commands the guard breaks beyond AGENTS.md's own sentence" subsection (end of Chunk B); folded into Author-accounting's "Known omissions" paragraph. |
| PR5 (non-blocking) -- Chunk D's own corrected-count paragraph contradicts itself twice, and "five paths" is stale by one (A7). | Fixed. "five paths" -> "six paths" with the accounting spelled out (A6 stopped adding a distinct file; A7 adds the sixth, unfrozen); "both files" -> "all four"; "two `FROZEN-MODIFIED`" -> "four" in the batching paragraph. | Chunk D, the "Four `FROZEN-MODIFIED` entries, not two" paragraph and the following "A re-anchor is already independently owed" paragraph. |
| PR6 (non-blocking) -- the "eleven" row-mapping count is stale by two (now three, after PR2's addition); it carries 13 (now 14). | Fixed at both citations, now "14", with the count broken down (11 from Revision 5's Evidence table + 3 this plan's own expansions add: A6, A7, the environment-construction meta-guard). | Author-accounting > "Invariants"; Verification > "Boundary A". |
| PR7 (non-blocking) -- the A4/A5 allowance gloss omits the third edit the row mapping actually places in `test_security_check.py`. | Named explicitly in the gloss, with the history check (`e0ab524`) carried over from the finding. | Scope > "Contract expansion" (A4/A5 paragraph). |
| PR8 (non-blocking) -- the `noconftest`-absence grep figure is stale by one (`dev/PLANNING.md`'s own `[TRU-4]` row). | Re-scoped to exclude that row explicitly and dated `as_of 2026-08-20`, per the numeric-claims discipline. | Author-accounting > "Which chunk runs the mutation...". |
| PR9 (non-blocking) -- B2's insertion-point cell is ambiguous between "end of sentence" and "end of bullet". | Reworded: "the equivalent sentence currently ends..." with an explicit note that the bullet continues past it. | Chunk B table, B2 cell. |
| PR10 (non-blocking) -- two rows (override token, `--noconftest`) are one-directional and go quiet under PR2's environment hazard. | Both given a paired control, matching the pattern the `--collect-only` and release-mode rows already use. | Row-mapping rows 6, 11. |
| False-premise sweep (Maintainer brief) | 4 locations named (lines 98, 159-162, 245, 608-609 at review time); 1 (608-609) is inside the reviewer's own append-only section and was left untouched per the append-only rule. **3 locations found and corrected** in operative cells: Scope > "A second expansion" (the "(c)" gloss), the sequencing bullet, and Chunk A table row A6. No further occurrences found outside the reviewer's section. | See cells listed under PR1 above -- same edit pass. |

**Status**: `revising-plan` -> `awaiting-plan-review`.
