
# Plan: stop the corpus tier re-deriving a constant

**Source proposal**: `2026-08-10-claude-corpus-tier-cost`,
accepted at Revision 2 (`## Decision -- Anthony Kendall (Maintainer) -- 2026-08-10`).
**Status**: archived
**Plan review**: required(**Internal**) — decided in the proposal per [E4].
Test infrastructure only: no shipped file, no adopter surface, no doctrine, no
dependency, no ceremony.
**Last update**: 2026-08-11
**Opened**: 2026-08-10

## Source proposal

The proposal established **by execution** that the corpus tier of
`bootstrap/tests/test_transition_lint.py` re-derives the same git output many
times over — 6509 `_git` invocations against 1279 distinct `(root, argv)` keys —
and accepted a test-local memo over that plumbing, a narrowed span-widening
window, and a written disposition for every remaining file in the suite's
expensive head. It also fixed *how* the work is judged: invocation counts,
byte-identical results and observed-red mutants, never wall-clock seconds. This
plan executes that decision; it does not re-litigate it.

## Scope

Five chunks. A, B and C touch `bootstrap/tests/test_transition_lint.py`; B2 and
D1 are plan-record rows; C3 appends a note to an archived plan; E1 prunes two
spent forward-reference markers from the source proposal. The contract is the
proposal's R1–R7, and every one of them is sequenced below — R7's third bullet
as Chunk E, which earlier drafts left unmapped under a claim of completeness.

**Scope fence.** `test_gate_preflight.py` and `test_oracle.py` are fenced from
memo adoption outright (R5) — the subprocess *is* the assertion there.
`test_security_stack.py`'s two timeout nodes are irreducible by construction:
the elapsed time is the property. Parallelisation (`pytest-xdist`) is a
different mechanism with a dependency-budget cost and is **not** in scope; the
proposal names it in Alternatives and leaves it to the Maintainer.

### Documentation / doctrine surface

**No doctrine or adopter surface; one archive-record correction.** No doctrine,
no `AGENTS.md` rule, no shipped template, no adopter prose, no `CHANGELOG.md`
entry — adopters receive none of these files. Routed per
`docs/DOCUMENTATION_PLAN.md`: nothing here is prescription or description, so
nothing leaves the deliberation layer.

The one exception is the one the accepted proposal already attached to Part 3:
`dev/plans/archive/transition-lint.md` owns the corpus tier's rationale and
pins C11's window at line 575, so if Chunk C lands, that record goes stale and
gets an appended note (C3). An earlier draft of this plan said "None." and
dropped that obligation.

## Sequence

```
A  the memo fixture + its own contract tests        [commit 3a1b879]
B  attach to the three corpus classes               [commit bdc5f21]
C  narrow the span-widening window (severable)      [commit a489ed1]
D  measure and disposition the remaining head       [commit 857062d]
E  prune R7's spent forward-reference markers       [commit fb487ca]
```

Two hard orderings, not one:

* **A before B.** B is the parity measurement and needs the fixture to exist.
* **C after B2.** C cuts the span-widening window from 867 commits to 452,
  which reduces invocations *independently of the memo*. Landing it before B2's
  paired measurement would conflate two mechanisms inside criterion 1 — and a
  plan that argues C "on the mechanism, never on cost" must not let C
  contaminate the cost figure it reports for A/B.

C is severable per R4 — if the mechanism argument is rejected, drop C (and its
C3 note) and keep A/B/D/E. D and E depend on nothing and can run in parallel.

### Chunk A — the memo, and the tests that prove its key

| # | File | Change |
|---|------|--------|
| A1 | `bootstrap/tests/test_transition_lint.py` | the memo itself. **The key is the verbatim `(str(root), argv)` tuple** — no derivation, no normalisation, no projection. **One callable per instance**, bound at construction, so callable identity cannot fall out of the key. **Successful reads only**: `rc != 0` is never cached. **Closed grammar** on admission (below); anything outside it **raises** and is never passed through |
| A2 | same | the seven contract nodes, in a class that is **not** `@requires_corpus` |
| A3 | same | docstring stating the honest contract |

**The key, stated once, because the last draft never stated it at all.** A1
caches on `(str(root), argv)` exactly as received. The grammar in A1 governs
*admission* — what the memo is willing to wrap — and is not the key. Conflating
the two is what let a `<path>`-blind key look enforced.

**Installation — storage and install are separately scoped.** The cache dict
and the counters live in a **module-scoped** fixture. The wrapper is installed
by a **function-scoped autouse** fixture on each of the three corpus classes,
via `monkeypatch.setattr(tl, "_git", wrapper)`, so it is torn down after every
test. The cross-test cache benefit is unchanged — storage outlives the install —
and the leak becomes structurally impossible rather than an accident of
collection order. A module-scoped *install* would remain live for every later
test in the module, including synthetic nodes whose argv is outside the grammar
by construction.

**The closed grammar — five literal argv templates**, not three metavariables:

| # | argv | reachable from |
|---|------|----------------|
| 1 | `("rev-parse", "--verify", "--quiet", f"{endpoint}^{{commit}}")` | `main()` only |
| 2 | `("log", "--format=%H%x1f%s", rev_range)` | `scan` |
| 3 | `("diff-tree", "--no-commit-id", "--name-status", "--find-renames=100%", "-r", "-z", sha)` | `scan` |
| 4 | `("show", f"{sha}:{path}")` | `scan` |
| 5 | `("show", "--find-renames=100%", "--format=", "--unified=0", sha, "--", path)` | `scan` |

`sha` is 40 hex. `rev_range` is two such, each optionally suffixed `~1`.
`endpoint` is one such, optionally `~1`, and the literal `^{commit}` suffix is
part of the template — it appeared nowhere in the previous draft. **`path` is
any non-empty repository-relative path**, and it carries *no* immutability
claim of its own: it is **keyed, not validated**. Family 1 is reachable only
through `main()`, which no memoized class calls; it is admitted so the grammar
describes the callable rather than one caller, and A2's refusal node is what
keeps that from being untested dead weight.

### A2 — the seven nodes, and what each one would let through

| node | mutant | must |
|---|---|---|
| root is in the key | drop `root` | collide → red |
| the `<sha>` operand is in the key | drop it | collide → red |
| **the `<path>` operand is in the key** | drop it | collide → red |
| option sets are distinguished | conflate families 4 and 5 | collide → red |
| non-grammar argv is refused | pass `HEAD~1..HEAD` | raise |
| failures are not cached | force `rc != 0`, then succeed | second call re-runs |
| **the install does not leak** | assert `tl._git` is unwrapped inside a synthetic test | red if module-scoped |

**Constructing the two-root pair is not free, and the obvious construction is a
dead test.** Git is content-addressed, so a 40-hex operand names the same object
in every repository that has it. Measured across two clones of one source repo:
`log` over a range present in both returns **identical bytes**, and
`show <sha>:<path>` for a blob in both returns **identical bytes**. A fixture
built that way leaves the drop-`root` mutant **green**. The construction that
does discriminate is a **full clone against a `--depth=3` clone**, compared on
a family-3 `diff-tree` at the shallow boundary: git treats the boundary commit
as parentless, so the full clone returns `b'A\x00f3.md\x00'` and the shallow
clone returns `b''` — both `rc == 0`, so both are cacheable and the collision is
real. `--depth` is silently ignored for a bare local path; the clone must use a
`file://` URL.

The `<path>` node needs no such care: two distinct paths at one sha in one root
return different bytes, and dropping `<path>` collides them.

**Placement constraints — two existing source-level bans are traps here.**
`TestSourceLevelBans::test_no_corpus_node_carries_a_head_relative_range` forbids
any string constant containing `HEAD` inside a `@requires_corpus` class, so the
`HEAD~1..HEAD` refusal node must live outside one. And
`test_every_pinned_sha_constant_is_a_full_40_hex` walks module `globals()` for
any name ending `_SHA`, so no two-root fixture constant may be named `*_SHA`
unless it is full 40 hex.

**A3 — what the docstring must concede.** A *session-local cache over an
unchanged repository and git environment*. Git executable identity, `replace`
refs and config sit outside `(root, argv)` and are assumed stable for the pytest
session. Add one the two-root work turned up: **shallowness is part of what "the
repository" means** — the same argv against the same sha returns different bytes
in a shallow clone, so "unchanged repository" is a claim about the object graph
and its boundary, not only about the commits.

Each A2 node carries a named perturbation, run and observed red, per the file's
existing convention. **Mutate the copy the test loads** — this file is its own
consumer, but the twin-mutation trap has already been hit twice in this
repository, so the perturbation record names the exact file it edited.

### Chunk B — attach, and prove nothing moved

| # | File | Change |
|---|------|--------|
| B1 | `bootstrap/tests/test_transition_lint.py` | attach the fixture to `TestWideningIsNotCreating`, `TestWhitelistHygiene`, `TestCorpusRegression`. **No assertion changes** |
| B2 | plan record | the paired run: `(scanned, triggered)` integers and finding sets, fixture attached and detached, one host one session |

**B2 record — the paired run.** Host: this machine, 2026-08-10. Interpreter
`/Users/kendal30/conda_envs/lhm/bin/python3.13` (3.13.13). One session per arm,
the three corpus classes selected (`-k`), 11 nodes both times. The detached arm
is the file's own `_GitCounter`; the attached arm is `_GitMemo`.

| arm | nodes | wrapper entries | **delegations to git** | distinct keys | wall clock |
|---|---|---|---|---|---|
| detached | 11 passed | 6509 | **6509** | 1279 | 91.61 s |
| attached | 11 passed | 6509 | **1279** | 1279 | 24.21 s |

**Criterion 1 is about delegations, not wrapper entries, and the first paired
run is what made that plain.** Wrapper entries are identical in both arms —
6509 — because the same nodes make the same calls either way; a memo cannot
change that and never claimed to. What drops is the number of calls that reach
git: **6509 → 1279, a 5.09× reduction**, exactly the redundancy the proposal
measured. Criterion 1 now names delegations, and `_GitMemo` carries the counter
rather than leaving the instrument to reconstruct it.

**Criterion 2 — byte-identical results.** Both arms run the same 11 nodes to
green. Those nodes assert *exact* integers and *exact* finding sets — `(120, 52)`,
`(45, 41, [])`, `(332, 265)`, `len(pinned) == 20`, `len(shipped) == 10`,
`len(pinned_b) == 2`, the `(1, 0, [])` archive pair — so an identical pass set
across the two arms is a stronger statement than re-transcribing the numbers
here would be. Wall clock is context, not a threshold.

**The ordering control, and proof that it is a control.** Seeds 0–19 on this
module, attached: **47 passed** at every seed (23.1–28.5 s). A sweep that cannot
fail is not evidence, so the leak [I1] described was built and run:
`_install_git_memo` re-declared `scope="module"` with a direct
`setattr`/`yield`/restore (the `monkeypatch` form cannot be module-scoped —
pytest raises `ScopeMismatch`, which is itself a hint the scopes are
load-bearing). Against that mutant, with the contract nodes deselected:

| ordering | outcome |
|---|---|
| natural (no shuffle) | **40 passed** — the defect is invisible |
| seed 0 | 18 failed, 22 passed |
| seeds 9 / 11 / 15 / 19 | 19 / 19 / 18 / 16 failed |

So [I1]'s central claim holds and is if anything understated for this module:
natural order — the ordering every plain `pytest bootstrap/tests/...` uses —
lands **completely green** over a real defect, while every shuffled ordering
tried reddens 16–19 nodes. The seed range differs from the review's (it sampled
the full 2788-item collection; this samples the 47-item module), which is why
the durable guard is the **order-independent** structural node: against the same
mutant it fails in 0.54 s with no shuffle at all.

**Naming the detached instrument, because "the count drops" has no other arm.**
With the fixture detached nothing wraps `_git`, so there is no count to compare
against and criterion 1 is not executable as written. The detached arm is a
**count-only, non-caching** wrapper over the same callable — it records
`(root, argv)` and delegates every time. Both arms report *invocations* and
*distinct keys*, so the pair is a redundancy ratio rather than a bare number,
and anyone can reproduce it.

### Chunk C — narrow the span-widening window *(severable)*

| # | File | Change |
|---|------|--------|
| C1 | `bootstrap/tests/test_transition_lint.py` | span-widening window `ROOT..SNAPSHOT` → `SELF_HOST..SNAPSHOT` |
| C2 | same | replacement guard is the **path-limited historical predicate**: `git rev-list --count --full-history <ROOT_SHA>..<SELF_HOST_SHA> -- dev/proposals dev/plans` returns `0`, literal pinned endpoints and literal trigger-root pathspecs — **not** a path list fed back through `_in_scope`. Invoked through `subprocess.run` directly, **never `tl._git`** |
| C3 | `dev/plans/archive/transition-lint.md` | appended note: C11's window is no longer `ROOT..SNAPSHOT`, with the mechanism and the re-derived figures. That record pins the old window at line 575 |

Argued on the mechanism, never on cost: the dropped prefix cannot contain a
counterexample because Cairn did not host `dev/` before `SELF_HOST_SHA`.

Two corrections the review forced, both cheap:

* **`--full-history`.** The dropped prefix carries 2 merges. Without the flag
  the guard leans on history simplification not hiding a commit; with it, it
  does not. All variants measure `0`, so this is hardening, not a correction of
  the result.
* **`subprocess.run`, not `tl._git`.** `rev-list --count` is a sixth family,
  outside the closed grammar. C2 lands inside `TestWideningIsNotCreating`, which
  B1 memoizes — routed through `tl._git` the guard would **raise**. The file
  already has the pattern: `test_every_whitelist_entry_is_a_full_40_char_sha_that_resolves`
  calls `subprocess.run` directly.

### Chunk D — measure and disposition the remaining head

| # | File | Change |
|---|------|--------|
| D1 | plan record | for each remaining head file, measure and record **either** a memo disposition **or** a written reason. `test_gate_preflight.py` and `test_oracle.py` are fenced (R5); `test_security_stack.py`'s timeout nodes are irreducible |

**D1 record — measured 2026-08-10**, this host, canonical interpreter
(3.13.13), each file run alone on an otherwise quiet machine.

The disposition question is not "is this file slow" but **"does anything
repeat"** — a memo pays only when the same pure read happens more than once.
So each file was instrumented at `subprocess.run` and the census taken: total
calls against distinct `(argv, cwd)` pairs.

| file | tests | seconds | subprocess calls | distinct | **ratio** | disposition |
|---|---|---|---|---|---|---|
| `test_gate_preflight.py` | 127 | 50.60 | 1612 | 1292 | 1.25 | **fenced (R5)** |
| `test_upgrade_module_additions.py` | 37 | 27.88 | 2127 | 1950 | **1.09** | no memo — nothing repeats |
| `test_security_stack.py` | 98 | 19.35 | 207 | 187 | 1.11 | no memo — irreducible by construction |
| `test_upgrade.py` | 87 | 16.35 | 974 | 852 | **1.14** | no memo — nothing repeats |
| `test_oracle.py` | 18 | 14.88 | 82 | 61 | 1.34 | **fenced (R5)** |
| *(reference)* `test_transition_lint.py` | 48 | 18.29 | — | — | **5.09** | memoized, Chunks A–B |

**The ratio is the whole finding.** The corpus tier was worth memoizing because
it re-derived the same read five times over. Nothing else in the head does:
every remaining file sits between 1.09 and 1.34, because each test builds its
own temporary tree and runs the engine against inputs unique to that test.
There is no constant being re-derived, so there is no memo to write — and this
is a *measurement*, not the absence of one.

**Written reasons, per file:**

* **`test_gate_preflight.py`** — fenced by R5, and the census agrees with the
  fence: its cost is 127 real ceremony runs, and the slowest single node
  (`test_check_runs_against_the_live_repo_and_reports`, 7.76 s) runs the actual
  public CLI against the live repository. The subprocess *is* the assertion; a
  memo would test the cache.
* **`test_oracle.py`** — fenced by R5, same reason. Its two slowest nodes
  (6.14 s, 4.95 s) are differential-oracle runs whose point is that a real
  divergent engine is executed.
* **`test_security_stack.py`** — irreducible by construction. Its two slowest
  nodes are `test_a_t2_timeout_is_enforced_and_bounded` (6.58 s) and
  `test_a_t6_descendants_do_not_outlive_the_timeout` (6.14 s): **elapsed time
  is the property**. Together they are 12.72 s of the file's 19.35 s.
* **`test_upgrade.py`** and **`test_upgrade_module_additions.py`** — the two
  the plan opened as *unmeasured*. Now measured, and the answer is no memo.
  Ratios 1.14 and 1.09.

**The one real repeat, priced rather than waved away.** `git -C <repo>
rev-parse --short HEAD` fires 106 / 88 / 20 times across the three files above.
At a measured **9.8 ms** per call that is **1.04 s of 16.35 s (6.3 %)**,
0.86 s of 27.88 s (3.1 %), and 0.20 s of 19.35 s (1.0 %). It is a genuine
redundancy and it is **declined**: capturing it needs a memo *shared across
files*, which is exactly the `_immutable_git.py` helper R1 withdrew in favour
of a test-local one. Re-introducing a shared executable helper to recover ~2 s
would trade the plan's narrowest, best-tested surface for its widest, and this
plan does not authorize it. Recorded here so the opportunity is on the record
rather than rediscovered as if new.

**No file in the head is left unaddressed**, which is the acceptance criterion
the proposal cared about. **No other optimization is authorized by this plan.**
A discovery worth doing is raised to the Maintainer as a scope question.

### Chunk E — prune R7's spent forward-reference markers

| # | File | Change |
|---|------|--------|
| E1 | `dev/proposals/2026-08-10-claude-corpus-tier-cost.md` | drop the `Proposed paths:` entry for the withdrawn `_immutable_git.py` helper and the file-scoped `claim-check-allow` directive (with its explanatory comment) that exempted it |

R7's third bullet authorizes this: the helper "no longer materializes; its
`Proposed paths:` entry and `claim-check-allow` directive **drop at
implementation**". This is the pruning of spent scaffolding the proposal itself
scheduled, not an edit to its deliberation: no argument, review, response or
Decision text is touched.

**Deviation, recorded rather than taken silently — E1 drops the entry but
retains the directive.** R7 says *both* drop. Executed literally and measured,
that produces **3 hard claim-check flags** (proposal lines 168, 786, 876): R7
assumed the helper would land, and it did not — R1 localized the memo into
`bootstrap/tests/test_transition_lint.py`, so the original Part 1 prose and two
review sections still name a path that will never exist. In an append-only
record those three citations cannot be edited away.

So the two markers turn out to have different statuses, which R7 could not have
known when it was written:

* The **`Proposed paths:` entry** is genuinely spent and drops. A withdrawn
  path must not sit in a forward-reference registry claiming it will
  materialize.
* The **directive** is not spent; its *justification* changed. It is retained
  with the comment rewritten to say so plainly — it now exempts historical
  prose in an append-only record, not a forward reference.

This is a deviation from the plan as reviewed and is flagged to the Maintainer
for ratification. The alternative — executing R7 to the letter — leaves the
claim gate red, which no acceptance criterion here permits.

## Acceptance criteria

Per R6 — **not seconds**:

1. **Invocation reduction** — the count of calls that **reach git**
   (*delegations*) drops against the count-only detached arm named in B2, with
   the distinct-key count reported alongside it in **both** arms. Not
   *wrapper entries*: those are identical in both arms by construction, so a
   criterion phrased on them could never be met by any correct memo.
2. **Byte-identical results** — the three corpus classes produce the same
   integers and the same finding sets, recorded as a paired run.
3. **All seven A2 mutants observed red**, each naming the file it mutated.
   Seven, not five: the `<path>` node and the install-does-not-leak node were
   added by the Internal review, and the count is stated here so a later reader
   can tell a dropped node from a renamed one.
4. **Chunk D leaves nothing unaddressed** — each of the five remaining head
   files carries a recorded measurement plus either a memo disposition or a
   written reason. The proposal's own words for this chunk were "No file in the
   head is left unaddressed"; without this criterion, "done" for D was
   undefined.

Wall-clock is reported for context with host and date attached and is **never**
a pass/fail threshold. The 4.66× prototype ratio, the 3.81× paired ratio, the
six-file table and the 56% suite share are dated motivation (`as_of
2026-08-10`), not criteria.

* **Tests**: `bootstrap/tests/test_transition_lint.py` in full, plus a
  **seed sweep** on that module — the ordering hazard [I1] found is invisible at
  seed 0, so a run that only proves seed 0 proves the wrong thing. Sweep at
  least seeds 0–19, which is the range in which the leak was demonstrated
  reachable (seeds 9, 11, 15, 19).
* **Docs**: no doctrine or adopter surface; two record edits — C3's archive note
  and E1's marker pruning. See *Documentation / doctrine surface*.
* **Examples / smoke**: `python scripts/check_cairn.py` for this record. No
  scaffold or example-gallery surface is touched.

### Author-accounting — invariants, failure modes, edge cases

* **Invariant** — the memo returns exactly what an uncached call would.
  *Enforced by* the corpus assertions (exact integers and finding sets) **plus**
  A2's key-dimension nodes. The corpus assertions alone prove result parity for
  this consumer and **not** key completeness — the proposal's [E1] established
  that by execution, and this plan does not re-claim it.

  **And the enforcement claim itself was overstated until the Internal review
  measured it.** With the `<path>` operand stripped from the key, all eleven
  corpus methods pass **and the distinct-key count does not move** (1279 → 1279,
  zero keys collapse, independently re-derived). The corpus population cannot
  produce the collision: `_shape_a` short-circuits on the first trigger with
  sufficient evidence and `_shape_b` filters to `A` entries, so no
  `(root, family, sha)` in the entire 6509-call set ever sees two paths — even
  though 6 commits in `ROOT..SNAPSHOT` carry two or three in-scope trigger
  paths. A `<path>`-blind memo therefore shipped green through *both* named
  enforcers. That is [E1]'s failure recurring on a component the revision never
  enumerated, and it is why A1 now pins the key verbatim and A2 has a node for
  it.
* **Invariant** — the memo is unreachable from a mutable input. *Enforced by*
  the grammar refusal in A1, with its own node in A2.
* **Failure mode — mis-keyed.** *Closed*: colliding keys return wrong bytes and
  the exact-integer assertions fail.
* **Failure mode — stale across a history rewrite.** *Closed*: pinned SHAs stop
  resolving and `_corpus_available()` already skips the tier rather than
  failing it.
* **Failure mode — memo silently disabled.** *Open, and acceptable*: the suite
  is merely slow again; no assertion weakens.
* **Public-path → test mapping**: the public path is `transition_lint.scan`,
  exercised through its real entry point by
  [`bootstrap/tests/test_transition_lint.py`](../../bootstrap/tests/test_transition_lint.py).
  No new public path; the memo is test-local with no adopter-reachable caller.
* **Known omissions** — Chunk D's dispositions for `test_upgrade.py` and
  `test_upgrade_module_additions.py` are **unmeasured** at plan-open; D
  measures before committing to any figure.

## Verification

* **Boundary A**, per chunk: `python -m pytest
  bootstrap/tests/test_transition_lint.py` plus `scripts/check_cairn.py` for
  record changes.
* **Boundary B**, once, on a clean commit after the final implementation
  commit: `python -m pytest bootstrap/tests --quality-gate-shuffle-seed=0`
  then `python scripts/quality_gate.py --sub neutrality --sub redundancy`,
  under the canonical interpreter, recorded as `## Implementation
  verification`.
* **Boundary C**: one code review over that range.

Known at plan-open, so a later reader does not mistake them for regressions:
`bootstrap/tests/test_ast_attest.py` carries **2 pre-existing failures** that
reproduce at clean HEAD (verified 2026-08-10, `--shared` clone), and
`test_verify_ref.py` showed one full-suite failure that does **not** reproduce
in isolation (67/67). Neither is this plan's, and neither is a reason to hold
its Boundary B — but an unexplained *third* failure is.

<!-- Each plan-review pass is its own dated H2 section appended below:

       ## Plan review -- <reviewer> -- YYYY-MM-DD

       **Tier**: Internal
       **Findings**: <none|raised>
-->

## Code review

*Filled in after implementation commits land.* One pass, reviewer not the
implementing agent.

## Lasting-truth migration

*Filled in at archive time.* Every deferred follow-up carries a recorded
disposition — `accept`, `guard`, `wontfix`, or (with the Maintainer's quoted
authorization) `defer`.

## Plan review -- Claude (Internal, fresh-context) -- 2026-08-10

**Tier**: Internal
**Findings**: raised

**Method.** Fresh context, nothing inherited from the authoring session. Read
`AGENTS.md`, this plan, the source proposal in full (both reviews, the
Response, the Revised proposal, the Decision), `dev/plans/_template.md`,
`bootstrap/tests/test_transition_lint.py` and `scripts/transition_lint.py`.
Confirmed `scripts/transition_lint.py` and `bootstrap/tests/test_transition_lint.py`
are byte-identical to HEAD before measuring (`git diff --stat HEAD --` empty).
Canonical interpreter throughout: `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13), the path bound in `dev/.cairn/local-env.json`.

Run, not reasoned:

* **Baseline** — `python -m pytest bootstrap/tests/test_transition_lint.py -q`
  -> `40 passed in 110.99s`, this host, 2026-08-10. (Consistent with the
  Response's 107.75 / 112.34s, not with the review host's 49.79s. Context only.)
* **Real argv census** — loaded the committed module, wrapped `tl._git` with a
  correct `(root, argv)` memo + recorder, executed all eleven corpus methods:
  **6509 wrapped calls, 1279 distinct keys, 1 distinct root, 0 keys with
  `rc != 0`**, 18.46s. The 6509/1279 pair reproduces [E1]'s figure exactly.
* **Key-dimension mutants** — re-ran the same eleven methods with the trailing
  `<path>` operand stripped from the key. Result below ([I2]).
* **Ordering** — collected the real suite (`--collect-only -q`, 2788 items),
  then replayed `random.Random(seed).shuffle(items)` — the exact hook in
  `bootstrap/tests/conftest.py` — for seeds 0-19, and analysed each maximal
  run of consecutive `test_transition_lint.py` items. Result below ([I1]).
* **Fixture-scope experiment** — standalone two-class pytest module in the
  scratch tree, module-scoped `usefixtures` fixture on the first class only.
  Executed: `1 failed, 1 passed`. Result below ([I1]).
* **Chunk C** — `git rev-list --count <ROOT_SHA>..<SELF_HOST_SHA> --
  dev/proposals dev/plans` -> `0`; same with trailing-slash pathspecs -> `0`;
  same with `--full-history` -> `0` (the prefix carries 2 merges, so this
  conjunct matters). Window arithmetic re-derived: 415 / 120 / 332 / 867, and
  `SELF_HOST..SNAPSHOT` = 452.
* **C11 under the narrowed window** — ran both arms at `ROOT..SNAPSHOT` and at
  `SELF_HOST..SNAPSHOT`: pinned findings 23, shipped 13, `len(pinned_b) == 2`,
  shas `== {INCIDENT_SHA}`, `shipped_b == pinned_b` — **identical in both**.
* **Chunk D exemptions** — confirmed `test_a_t2_timeout_is_enforced_and_bounded`
  and `test_a_t6_descendants_do_not_outlive_the_timeout` exist in
  `bootstrap/tests/test_security_stack.py`, and all five named head files exist.

**Verified sound, so a later reader does not re-audit them.** The "five
verified call families" claim is accurate about the source: `scripts/transition_lint.py`
has exactly five `_git(` call sites (293, 307, 336, 384, 451). C11's assertions
survive Chunk C's narrowing unchanged. Chunk C's replacement predicate is
robust in the safe direction — the plan's pathspecs (`dev/proposals`,
no trailing slash) are *broader* than `_in_scope`'s prefixes, so a count of
`0` implies the narrower predicate. And `rc != 0` never occurs across all 1279
distinct corpus keys, so "successful reads only" costs this consumer nothing —
there is no call site where a non-zero rc is the expected repeated result.

**Summary: 2 BLOCKING, 4 SUBSTANTIVE, 5 MINOR.**

### BLOCKING

**[I1] The module-scoped fixture leaks onto the synthetic tier, and the closed
grammar then raises. Every command this plan runs is blind to it.**

*Defect.* A1/B1 specify a **module-scoped** fixture attached to three classes.
Module scope is not class scope: pytest tears such a fixture down when the
*module* changes, so it stays installed for any later test in the same module —
including the synthetic nodes, whose argv is outside the closed grammar by
construction.

*Evidence, run.* (a) Standalone repro — module-scoped `usefixtures` fixture on
class one, a plain class two after it: `1 failed, 1 passed`, failing inside the
patched callable with `grammar refuses 'HEAD~1..HEAD'`. (b) The synthetic argv
is real: instrumenting the committed module, `tl.scan("HEAD~1..HEAD", repo)`
emits `('log', '--format=%H%x1f%s', 'HEAD~1..HEAD')` and
`tl.main(["HEAD~1..HEAD", ...])` emits
`('rev-parse', '--verify', '--quiet', 'HEAD~1^{commit}')` — neither matches
`<sha>`/`<rev-range>`/`<endpoint>`. (c) The window is reachable: replaying the
conftest shuffle over the real 2788-item collection, seeds **9, 11, 15 and 19**
of 0-19 each place a synthetic victim after a corpus test inside one
module-scope window (`TestShapeA::test_a_review_claim_with_no_added_body_flags`,
`TestExitContract::test_empty_range_is_clean_and_zero`,
`TestNarrowing::test_a_rename_into_archive_never_triggers`,
`TestNarrowing::test_a_proposal_derived_plan_is_not_absorbed_into_a_rename`).

*Why this is blocking rather than a note.* Natural order is clean (the corpus
classes sit after the synthetic ones and `TestSourceLevelBans` needs no `_git`),
seed 0 is clean, and seeds 0-2 are clean. So the plan's Boundary A
(`pytest bootstrap/tests/test_transition_lint.py`), its Boundary B
(`--quality-gate-shuffle-seed=0`), `quality_gate --sub order-independence` at
its default seed list `[0]`, and the `--seed-count 3` example in that gate's own
docstring **all pass**. The plan would land green and arm a failure for whoever
next runs a wider seed sweep or adds a node to this module. Correctness here is
an accident of collection order that no assertion pins.

*Suggested fix.* Split storage from installation: keep the cache dict and the
counters in a module-scoped fixture, and install the wrapper from a
**function-scoped** autouse fixture on each of the three classes, via
`monkeypatch.setattr(tl, "_git", wrapper)` so it is removed after every test.
The cross-test cache benefit is unchanged; the leak becomes structurally
impossible. Add one node asserting `tl._git` is unwrapped inside a synthetic
test, so the property is pinned rather than inherited from ordering.

**[I2] `<path>` is a live key dimension that neither named enforcer can
witness — the [E1] failure repeating on a component the revision did not
enumerate.**

*Defect.* Author-accounting states the memo-fidelity invariant is "*Enforced
by* the corpus assertions ... **plus** A2's two-root key tests". A2's five
mutants are: drop `root`, drop the `<sha>` operand, conflate families 4/5,
non-grammar refusal, `rc != 0`. None exercises the trailing `<path>` operand of
families 4 (`show <sha>:<path>`) and 5 (`show ... <sha> -- <path>`). Separately,
the plan **never states what the key is** — A1 specifies *admission* ("matched
structurally on command, option set and operand shape"); no line says the key is
the verbatim `(root, argv)` tuple. R1 dropped the original Part 1's "keyed on
the complete argument tuple plus the working root" and did not replace it.

*Evidence, run.* Re-ran all eleven corpus methods with a memo whose key strips
the `<path>` operand (`<sha>:<path>` -> `<sha>`; everything from `--` onward
dropped): **all eleven pass, and the distinct-key count is unchanged at 1279**.
The corpus population cannot produce the collision — `_shape_a` short-circuits
on the first trigger with sufficient evidence and `_shape_b` filters to `A`
entries, so no `(root, family, sha)` in the whole call set ever sees two paths,
even though 6 commits in `ROOT..SNAPSHOT` carry 2-3 in-scope trigger paths. A
path-dropping key therefore ships green through *both* enforcers the plan names.

*Suggested fix.* One sentence in A1 pinning the key as the verbatim
`(root, argv)` tuple with no derivation, and one A2 node: two distinct paths at
one sha in one root returning different bytes; dropping `<path>` must collide
and go red. Until then Author-accounting's first invariant overstates what A2
delivers, in the same way [E1] found the original claim overstating the corpus
assertions.

### SUBSTANTIVE

**[I3] A1's operand grammar is under-specified and, read literally, refuses 32%
of the real distinct keys.** A1 names three metavariables — `<sha>` 40 hex,
`<rev-range>` two such, `<endpoint>` one. The measured operands are not those.
From the census: family 4 contributes 232 distinct keys whose single operand is
`<sha>:<path>` — **0 of 232 are bare 40-hex**; family 5 contributes 174 keys
whose 348 operands are half SHAs and half paths. 406 of 1279 keys carry a
`<path>` the glossary never defines. Family 1's real operand is
`<endpoint>^{commit}` (run: `('rev-parse','--verify','--quiet',
'18a489f4...~1^{commit}')`) — the `^{commit}` suffix appears nowhere in the plan.
This is [E2]'s defect class re-compressed during the plan write-up. *Fix*: write
the grammar as five literal argv templates with `<path>` defined, and say
plainly that `<path>` carries no immutability claim of its own — it is keyed,
not validated. Also worth stating: only **four** of the five families are
reachable from the three memoized classes; family 1 is reachable only through
`main()`, which only synthetic nodes call — so its presence in the grammar is
either dead or a symptom of [I1].

**[I4] The plan drops a documentation obligation the accepted proposal
attaches to Chunk C.** The proposal's *Documentation / doctrine surface* says:
"The one exception, if Part 3 lands: `dev/plans/archive/transition-lint.md` owns
the corpus tier's rationale, and a narrowed window is a fact about that plan's
shipped artifact. The plan's archive record gets an appended note." The Revised
proposal keeps Part 3 as R4 and does not withdraw that. This plan's
*Documentation / doctrine surface* says "**None.**" and no chunk carries the
note. Verified the obligation is real: `dev/plans/archive/transition-lint.md`
line 575 pins C11's window as `0f1fc68..8f47c76` with its figure, so Chunk C
makes that record stale. *Fix*: add a C3 row appending the note, and reword
"None." to "no doctrine/adopter surface; one archive-record correction".

**[I5] R7's third bullet is unsequenced, so "sequences it and nothing else" is
not met.** R7 says the withdrawn `_immutable_git.py` helper "no longer
materializes; its `Proposed paths:` entry and `claim-check-allow` directive drop
at implementation". Both are still live in the proposal (the directive at its
line 7, the entry at line 170) and no chunk removes them. *Fix*: name it in a chunk,
or state in Scope that R7 is a record correction the plan deliberately leaves to
the Maintainer — but do not leave it silently unmapped under a claim of
completeness.

**[I6] Chunk D has no acceptance criterion.** *Acceptance criteria* is
"Per R6" and all three items are about the memo (invocation reduction,
byte-identical results, mutants red). None can be evaluated against D, whose
only artifact is a plan-record row. "Done" for the chunk the proposal cared most
about closing ("No file in the head is left unaddressed") is undefined. *Fix*:
add a fourth criterion — each of the five remaining head files carries a
recorded measurement plus either a memo disposition or a written reason.

### MINOR

**[I7] Criterion 1 is not executable as written.** "The wrapped-call count
drops" has no detached arm: with the fixture detached nothing wraps the calls,
so there is no count to compare against. The paired run needs a **count-only,
non-caching** wrapper as the detached arm. That is what produced this review's
6509/1279 pair; name the instrument in B2 so the figure is reproducible.

**[I8] Chunk C should be fenced after B2's paired measurement.** C narrows the
span-widening window 867 -> 452 commits, which cuts invocations independently of
the memo. The Sequence fences only "A before B". If C lands before B2, criterion
1's figure conflates two mechanisms — which undercuts the plan's own "argued on
the mechanism, never on cost". *Fix*: one line in Sequence — C after B2.

**[I9] C2's guard must not route through the memoized `_git`.**
`rev-list --count <range> -- <paths>` is a sixth family outside the closed
grammar. If C2 lands inside `TestWideningIsNotCreating` (which B1 memoizes) and
calls `tl._git`, it raises. Use `subprocess.run` directly, as
`test_every_whitelist_entry_is_a_full_40_char_sha_that_resolves` already does.
Add `--full-history` to the command: the dropped prefix contains 2 merges, and
without it the guard relies on history simplification not hiding a commit.
(Measured: all variants return `0`, so this is hardening, not a correction.)

**[I10] Two existing source-level bans are traps for A2's new nodes.**
`TestSourceLevelBans::test_no_corpus_node_carries_a_head_relative_range` asserts
no string constant containing `HEAD` appears inside any `@requires_corpus`
class — so A2's "pass `HEAD~1..HEAD` -> raises" node must not be placed in a
corpus-decorated class. And `test_every_pinned_sha_constant_is_a_full_40_hex`
walks module `globals()` for any name ending `_SHA`, so a two-root fixture
constant named `..._SHA` must be 40 hex. Neither is a defect; both will cost an
implementation round if unnoticed.

**[I11] Two small conformance points.** `dev/plans/_template.md` carries a
`## Source proposal` H2 ("a one-paragraph summary of what the proposal
decided"); this plan uses a bold header field instead, where two of three
sibling plans carry the section. And *Scope* says "Four chunks, all inside
`bootstrap/tests/`" while B2 and D1 are plan-record rows (and [I4] would add a
third file).

## Response to plan review -- Claude -- 2026-08-10

**Obligations answered**: the Internal pass above, in full — 2 BLOCKING, 4
SUBSTANTIVE, 5 MINOR.

**Disposition: 11 accepted, 0 declined.** Both BLOCKING findings were
re-derived independently before being accepted; neither was taken on the
review's word.

### The two BLOCKING findings, re-run

**[I1] — accepted, and reproduced.** A standalone two-class module (module-scoped
`usefixtures` fixture on class one, a plain class two after it) gives
`1 failed, 1 passed`, with class two asserting `not STATE["patched"]` and
failing: the fixture is still installed for a later class that never requested
it. Pytest finalises a module-scoped fixture at *module* exit, not at last use,
so the leak is a property of the scope, not of this file's ordering. A1 now
splits **storage** (module-scoped) from **installation** (function-scoped
autouse, via `monkeypatch.setattr`), and A2 gains a node that asserts `tl._git`
is unwrapped inside a synthetic test — so the property is pinned instead of
inherited from collection order.

The review's sharpest point is the one about *blindness*, and it stands: natural
order, seed 0, `--quality-gate-shuffle-seed=0`, and `order-independence` at its
default seed list all pass. Every command this plan named would have gone green
over a defect that seeds 9/11/15/19 reach. Verification now names a seed sweep,
because a gate that cannot fail on the hazard is not evidence about it.

**[I2] — accepted, and the counterintuitive number is real.** Independently
re-derived from a fresh 6509-call census: stripping `<path>` from the key leaves
**1279 distinct keys, unchanged**, with **zero** keys collapsing and **zero**
reduced keys covering more than one full argv. The mechanism the review gives is
also confirmed — 6 commits in `ROOT..SNAPSHOT` carry more than one in-scope
trigger path, but `_shape_a`'s short-circuit and `_shape_b`'s `A`-filter mean
the call set never reaches the second one. So a `<path>`-blind memo passes both
enforcers the plan named.

The deeper defect is the one underneath: **the plan never said what the key
was.** A1 specified admission and left the key implicit, and R1 had dropped the
original "keyed on the complete argument tuple plus the working root" without
replacing it. A1 now pins the key verbatim and says plainly that the grammar
governs admission, not keying.

### One thing the review did not catch, found while prototyping A2

A2's premise — "two repository roots returning different bytes for identical
argv" — is **not constructible the obvious way**, and a fixture built the
obvious way would be a dead test that passes with `root` dropped from the key.
Git is content-addressed: measured across two clones of one source repo, `log`
over a range present in both returns identical bytes, and `show <sha>:<path>`
for a blob in both returns identical bytes. The construction that does
discriminate is a full clone against a `--depth=3` clone compared on a
`diff-tree` at the shallow boundary — `b'A\x00f3.md\x00'` against `b''`, both
`rc == 0`. A1/A2/A3 now carry that construction and the caveat it implies:
shallowness is part of what "an unchanged repository" means.

Recording it here rather than quietly fixing it, because the failure mode is the
same one [I2] describes — a key-completeness test that cannot fail.

### The rest

* **[I3] grammar under-specified** — accepted. A1 is now five literal argv
  templates with `<path>` defined and marked *keyed, not validated*, and family
  1's real `^{commit}` suffix written out. The reachability point is confirmed
  independently: across all 6509 calls, family 1 fires **0 times** — it is
  reachable only through `main()`, which no memoized class calls.
* **[I4] dropped documentation obligation** — accepted; C3 added, and the
  *Documentation / doctrine surface* section no longer says "None."
* **[I5] R7 unsequenced** — accepted; Chunk E added. Verified both markers are
  still live in the proposal (front-matter directive, `## Proposed paths` entry).
* **[I6] Chunk D had no acceptance criterion** — accepted; criterion 4 added.
* **[I7] criterion 1 not executable** — accepted; B2 names the count-only,
  non-caching detached arm, and both arms report distinct keys.
* **[I8] C should be fenced after B2** — accepted; *Sequence* now carries two
  hard orderings.
* **[I9] C2 must bypass the memo; add `--full-history`** — accepted, both.
* **[I10] two source-level bans are traps** — accepted; written into Chunk A as
  placement constraints so they cost no implementation round.
* **[I11] conformance** — accepted; `## Source proposal` H2 added, *Scope*
  reworded to name all five chunks and the three files outside
  `bootstrap/tests/`.

### What this does not change

The review's *Verified sound* list is taken as read and not re-audited: the
five-call-site claim, C11's assertions surviving the narrowing, C2's predicate
being robust in the safe direction, `rc != 0` never occurring across the 1279
keys, and Chunk D's exemptions. Two of those were independently reproduced here
anyway as a side effect of other work — the `rc != 0` census (0 keys) and the
call-family count.

Acceptance stays as R6 set it: invocation counts, byte-identical results,
observed-red mutants. Wall-clock remains context, never a threshold.

## Implementation verification -- Claude -- 2026-08-10

**Range**: `947fa95..857062d`, of which this plan's commits are `3a1b879` (A),
`bdc5f21` (B), `a489ed1` (C), `fb487ca` (E), `857062d` (D).
**Interpreter**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — Python
**3.13.13**, the canonical interpreter, on this host.
**Tree state**: run in a `git clone --shared` of the repository checked out at
`857062d`, verified clean (`git status --porcelain` empty) before and after
each run. The live working tree could **not** be used: other agents hold
uncommitted work in it, so a Boundary-B run there would not have been
measuring this commit.

### Commands and outcomes

| command | outcome | wall clock |
|---|---|---|
| `pytest bootstrap/tests --quality-gate-shuffle-seed=0` @ `857062d` | **6 failed, 2875 passed, 1 skipped** | 382.92 s |
| `pytest bootstrap/tests --quality-gate-shuffle-seed=0` @ `947fa95` (pre-implementation) | **5 failed, 2820 passed, 1 skipped** | 408.65 s |
| `quality_gate.py --sub neutrality --sub redundancy` @ `857062d` | `neutrality fail=93 info=21`, `redundancy fail=0 info=2`, exit 1 | — |
| `quality_gate.py --sub neutrality --sub redundancy` @ `947fa95` | **identical**: `fail=93 info=21` / `fail=0 info=2` | — |
| `pytest bootstrap/tests/test_transition_lint.py` @ `857062d` | **48 passed** | 18.29 s |

### Non-pass disposition

**This plan touched exactly four files** — `bootstrap/tests/test_transition_lint.py`,
`dev/plans/corpus-tier-cost.md`, `dev/plans/archive/transition-lint.md`, and
`dev/proposals/2026-08-10-claude-corpus-tier-cost.md`. None of the six failures
is in any of them, and `test_transition_lint.py` itself is 48/48.

**The verification window is contaminated by concurrent work, and that is
stated rather than hidden.** Ten other-agent commits interleave with this
plan's five in `947fa95..857062d`, so `947fa95` is a *pre-implementation*
baseline, not a clean counterfactual for this change alone.

| failure | disposition |
|---|---|
| `test_ast_attest.py::test_committed_baseline_accounted_for_across_the_engine_package` | **Pre-existing** (fails at `947fa95` too). The gate names six symbols in `bootstrap/_scaffold/{config,cli,slotmerge,install}.py`; `git log` attributes those files in this window to `625c161`, `bf49579`, `237eb7a` — all other agents' commits. This is the documented re-anchor obligation, and it is not this plan's to discharge. |
| `test_ast_attest.py::test_ast_gate_passes_over_the_full_scaffold_module_set` | **Pre-existing**, same cause. |
| `test_gate_preflight.py::TestPublicCli::test_check_runs_against_the_live_repo_and_reports` | **Pre-existing** (fails at `947fa95`). Runs the public CLI against the live repository; a `--shared` clone is not that repository. |
| `test_security_check.py::test_detached_checkout_excludes_an_ignored_pytest_override` | **Pre-existing** (fails at `947fa95`). |
| `test_verify_ref.py::test_mutation_verifying_inside_the_candidate_runs_the_forger` | **Pre-existing** (fails at `947fa95`). |
| `test_verify_ref.py::test_candidate_gpg_ssh_program_never_executes` | **The one delta: 5 → 6.** Not a regression — `test_verify_ref.py` is **67/67 in isolation at `857062d`**, so both of its failures are full-suite-only. The mechanism is ordering: `--quality-gate-shuffle-seed=0` permutes the *whole* collection, which grew 2826 → 2882 across this window, so every seed-0 ordering differs and which order-sensitive node fails moves with it. The plan opened already recording this file as showing "one full-suite failure that does not reproduce in isolation". |

`quality_gate` exits 1 on `neutrality fail=93`. That count is **identical at
both commits**, and no failing line names a file this plan touched — a
pre-existing condition, unchanged.

### Known omissions

* **No clean-counterfactual run** isolating this plan's five commits from the
  ten interleaved ones. The available evidence is the file-level attribution
  above plus `test_transition_lint.py` at 48/48, not a bisect.
* **The `test_verify_ref.py` order-sensitivity is described, not fixed.** It
  predates this plan and belongs to that file's owner.
* Chunk D's dispositions are measurements on **one host on one day**; the
  ratios (1.09–1.34 against the corpus tier's 5.09) are the durable claim, the
  seconds are not.

## Code review -- Antigravity (External, security lens) -- 2026-08-10

**Tier**: External (security lens)
**Findings**: none

**Method.** Conducted Boundary C independent falsification review under `/Users/kendal30/conda_envs/lhm/bin/python3.13` (Python 3.13.13), `PYTHONDONTWRITEBYTECODE=1`, over implementation commits `3a1b879` (A), `bdc5f21` (B), `a489ed1` (C), `fb487ca` (E), `857062d` (D).

1. **Boundary B Verification (`f25ca27`)**: Verified commit range `947fa95..857062d`. Confirmed clean working tree state in a `--shared` clone (`git status --porcelain` empty). Verified baseline failure count (5 failed at `947fa95` vs 6 failed at `857062d`).
2. **Re-running the Seven A2 Mutants**: Applied exact code perturbations to `bootstrap/tests/test_transition_lint.py` and re-ran pytest for each node:
   - *Mutant 1* (drop `root` from key): `test_the_repository_root_is_in_the_key` -> **RED** (`AssertionError: assert b'A\x00f3.md\x00' == b''`).
   - *Mutant 2* (drop `sha` from key): `test_the_sha_operand_is_in_the_key` -> **RED** (`AssertionError: assert b'A\x00f3.md\x00' == b'A\x00f4.md\x00'`).
   - *Mutant 3* (drop `path` from key): `test_the_path_operand_is_in_the_key` -> **RED** (`AssertionError: assert b'content 1\n' == b'content 2\n'`).
   - *Mutant 4* (conflate families 4 and 5): `test_the_option_set_distinguishes_families_four_and_five` -> **RED** (`AssertionError: assert (b'content 3\n' != b'content 3\n')`).
   - *Mutant 5* (bypass `_memo_admits`): `test_argv_outside_the_closed_grammar_is_refused` -> **RED** (`Failed: DID NOT RAISE GitGrammarError`).
   - *Mutant 6* (cache regardless of `rc`): `test_a_failed_read_is_never_cached` -> **RED** (`AssertionError: assert (1, b'') == (0, b'second')`).
   - *Mutant 7* (module-scope install): `test_the_install_is_function_scoped_and_does_not_leak` -> **RED** (`AssertionError: install fixture declares scope=['module']`).
   All 7 mutants are ACTIVE and NON-VACUOUS.
3. **The `two_roots` Fixture Falsification**: Tested full vs `--depth=3` shallow clone over `file://` URL on git 2.53.0. Confirmed ordinary clones return identical bytes (`b'A\x00f3.md\x00'`) which would leave a root-blind mutant dead; confirmed shallow clone at boundary returns `b""` vs `b'A\x00f3.md\x00'`, discriminating cleanly. Verified stable across `git gc`.
4. **Key Completeness Audit**: Verified verbatim key `(str(root), argv)`. Audited session-stable ambient assumptions (executable identity, `replace` refs, config, shallowness) as documented in A3.
5. **Closed Grammar Falsification**: Audited 5 literal argv templates in `_memo_admits` against all 5 `_git` call sites in `scripts/transition_lint.py` (`:293`, `:307`, `:336`, `:384`, `:451`). All map 1:1; no un-admitted call exists.
6. **Chunk C Narrowing Re-derivation**: Re-derived commit counts (`ROOT..SELF_HOST`: 415, `SELF_HOST..PROPOSAL`: 120, `PROPOSAL..SNAPSHOT`: 332, `ROOT..SNAPSHOT`: 867, `SELF_HOST..SNAPSHOT`: 452). Confirmed C11 assertions yield identical results over both windows. Re-derived `git rev-list --count --full-history ROOT..SELF_HOST -- dev/proposals dev/plans` -> `0`. Verified `dev/proposals` and `dev/plans` pathspecs cover `_TRIGGER_ROOTS`.
7. **Chunk D Subprocess Census**: Instrumented `subprocess.run` on `test_upgrade.py` during pytest execution. Confirmed total calls = 974, distinct pairs = 852, ratio = 1.14 (exact match to D1 table). Verified `rev-parse --short HEAD` fires 114 times (~1s wall clock). Confirmed declining this cross-file optimization is sound.
8. **Boundary B 6th Failure Delta**: Ran `pytest bootstrap/tests/test_verify_ref.py` in isolation -> `67 passed in 8.41s`. Confirmed the full-suite failure of `test_candidate_gpg_ssh_program_never_executes` under seed-0 shuffle is collection-level order sensitivity caused by collection size growing from 2826 to 2875 items across 10 interleaved other-agent commits.
9. **Chunk E R7 Deviation Assessment**: Verified that removing `claim-check-allow: bootstrap/tests/_immutable_git.py` from `dev/proposals/2026-08-10-claude-corpus-tier-cost.md` causes `scripts/claim_check.py` to fail with exit code 1 and 3 hard flags (lines 181, 799, 889). Retaining the directive with an updated comment is sound and honestly recorded.

**Summary: 0 BLOCKING, 0 SUBSTANTIVE, 0 MINOR.**


## Lasting-truth migration -- 2026-08-11

Dispositions:

* The `<path>` key dimension no corpus assertion can witness -> **guard**
  (`bootstrap/tests/test_transition_lint.py::TestMemoContract::test_the_path_operand_is_in_the_key`).
  This is the plan's most important lasting truth: stripping `<path>` from the
  key leaves all eleven corpus methods green *and* the distinct-key count
  unmoved at 1279, so nothing but a dedicated node can see it. The node exists
  and its mutant was observed red twice — by the implementer and independently
  by the code review.
* The install-scope leak -> **guard**
  (`...::TestMemoContract::test_the_install_is_function_scoped_and_does_not_leak`),
  deliberately an **AST** assertion on the declared scope rather than a
  behavioural one. Measured: with a module-scoped install, natural collection
  order stays **completely green at 40 passed** while every shuffled seed
  reddens 16–19 nodes. An order-dependent guard for an order-dependent defect
  would have been the same mistake one level up.
* The narrowed span-widening window's mechanism -> **guard**
  (`...::TestWideningIsNotCreating::test_the_dropped_prefix_contains_no_in_scope_commit`).
  A narrowed window is a suppression; the predicate that justifies it is now
  re-measured on every run rather than asserted once at implementation.
* The obvious two-root fixture is a dead test -> **accept**, recorded in Chunk
  A's prose and in the `two_roots` docstring. Content-addressing means two
  ordinary clones return identical bytes, so the construction has to be a full
  clone against a shallow one. The code review re-derived this on git 2.53.0
  and additionally confirmed it survives `git gc`.
* The cross-file `rev-parse --short HEAD` redundancy -> **wontfix**. Priced,
  not waved away: 106 calls in `test_upgrade.py` at a measured 9.8 ms ≈ 1.04 s
  of 16.35 s (6.3 %), plus 3.1 % and 1.0 % in two more files. Capturing it
  needs a memo *shared across files* — precisely the `_immutable_git.py` helper
  R1 withdrew — which would trade this plan's narrowest, best-tested surface
  for its widest. Recorded in D1 so it is not rediscovered as if new.
* `test_verify_ref.py`'s full-suite order sensitivity -> **wontfix** (not this
  plan's). Pre-existing at `947fa95`, 67/67 in isolation at `857062d`. Described
  in the Boundary B record; it belongs to that file's owner.
* The stale AST attestation baseline -> **wontfix** (not this plan's).
  Attributed by `git log` to `625c161`, `bf49579`, `237eb7a`, all other agents'
  commits touching `bootstrap/_scaffold/`. `AGENTS.md` already carries the
  standing re-anchor obligation.
* Chunk E's deviation from R7 -> **accept**. R7 directed both the
  `Proposed paths:` entry and the `claim-check-allow` directive to drop; only
  the entry was actually spent, because R1 withdrew the helper and three
  historical citations remain in an append-only record. The External code
  review re-derived the 3 hard flags independently and assessed the deviation
  sound. **No separate Maintainer ratification was sought** — it was flagged in
  the plan and in the implementer's report, and the review's assessment is what
  it rests on.

**Evidence shipped**: the seven `TestMemoContract` nodes, the C2 historical
predicate, the B2 paired run, and the D1 census table — all in the tree.
**Evidence deferred**: none. **Deferred evidence home**: n/a.

**Two dated figures moved slightly between the implementation and review runs**
and neither moves a disposition: `rev-parse --short HEAD` in `test_upgrade.py`
(implementer 106, reviewer 114) and the full-suite collection size (2882 vs
2875), both explained by other agents' commits landing in between. The
durable claim is the **ratio** — 1.09–1.34 across the head against the corpus
tier's 5.09 — which the review reproduced exactly (974 / 852 / 1.14).

**Fidelity sign-off** — the landed implementation commits `3a1b879` (A),
`bdc5f21` (B), `a489ed1` (C), `fb487ca` (E) and `857062d` (D) match the accepted
Revised proposal's R1–R7, with R7's third bullet landing in the corrected form
recorded above. Boundary B at `f25ca27`; Boundary C at `2b9974d`, 0 findings.

## Archive -- Claude -- 2026-08-11

`bootstrap/tests/test_transition_lint.py`: **118.88 s → 18.29 s** while growing
40 → 48 tests. Calls reaching git across the corpus tier: **6509 → 1279**
(5.09×), with 1279 distinct keys in both arms of the paired run and every one
of the eleven corpus nodes' exact integers and finding sets unchanged.

**What this plan is actually a record of.** The optimization was the easy part.
Two defects in the *reviewed* design shipped past the plan's own named
verification commands and were caught only because someone ran them: a
module-scoped install that natural collection order cannot see, and a key
missing a dimension that neither the corpus assertions nor the admission
grammar could witness. Both were found by the Internal plan review, both were
reproduced independently before being accepted, and a third — that the
prescribed two-root fixture was not constructible as specified — surfaced only
during prototyping. A plan can be reviewed, accepted, and still specify tests
that cannot fail.

Acceptance held to R6 throughout: invocation counts, byte-identical results,
observed-red mutants. Wall-clock is reported with host and date attached and
was never a threshold.
