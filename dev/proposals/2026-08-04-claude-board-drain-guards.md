# Drain the board the way the vocabulary intended — write the guards

**Author**: Claude (Strategy)
**Model**: claude-opus-5
**Date opened**: 2026-08-04
**Status**: revised
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

---

## Internal Review -- Claude (fresh session) -- 2026-08-04

**Model**: claude-opus-5
**Reviewed at**: `99c8d55` (proposal open), which is also HEAD; working tree
clean apart from untracked `.claude/` and `dev/measurement/` artifacts.
**Interpreter for every figure below**: `/Users/kendal30/conda_envs/lhm/bin/python3.13`
(Python 3.13.13), the canonical interpreter, with `bandit` 1.9.4 present.
**Suite baseline**: `python -m pytest bootstrap/tests` -> **1959 passed, 0
failed, 0 skipped**, 278.58s.

### Steelman

The central move is right and I want it on the record before the findings.
`board-retro-disposition`'s [I3] offered two satisfiers -- **(a)** widen the
scope so the pass may land `guard` assertions, or **(b)** keep the narrow scope
and state the consequence. The predecessor took (b). Taking (a) later, in a
*bounded* form, is not a contradiction of that review; it is the other branch
of it, and [I3]'s own text says so: *"the guard is one assertion and should be
written rather than re-deferred"* is quoted **inside the finding that produced
the narrowing**. The proposal is correct that nothing in the record forecloses
(a) on the merits.

Three more things are right. **The `guard` token has never been used** -- I
checked: no archived plan or proposal, and no commit body, carries a real
`guard` disposition; every occurrence in the tree is doctrine, template, or
test fixture. An accepted vocabulary that is never exercised is a vocabulary
nobody has stress-tested, and exercising it is worth doing. **Class B's "no
target count"** is the honest correction of the parent's "12 of the 59" --
promising an assessment rather than a number is exactly the discipline this
lineage keeps failing. And **mandatory mutation proof** is the right bar; I
applied it, and it is the reason two of the three Class A rows below did not
survive. A verification plan whose own standard falsifies the proposal is a
good verification plan.

The *Signals* section is also correctly drawn. Its second entry -- *"Class A
grows past a handful. The 'one assertion' language in the rows was optimistic,
and the right response is to stop"* -- is the finding I ended up making, which
means the author anticipated the failure and then did not run the check. That
is a much better position to review from than one where the signal is missing.

---

### [I1] "`conftest.py` is not frozen" is false -- measured; G6's home is a pinned gate file with no scheduled re-pin

The frozen-file argument closes with: *"`conftest.py` is not frozen."* It is.

`bootstrap/tests/conftest.py` is one of **164** entries in `frozen_files` in
`bootstrap/tests/fixtures/gate_manifest.json`, and it is re-discovered live by
`_frozen_files()` (`bootstrap/tests/_gate_manifest.py:151-169`) through the
`bootstrap/tests/**/*.py` glob -- 172 files today. It is not in
`CASCADE_MUTABLE` or `PHASE_SPLIT_TARGETS`.

Deletion test, run rather than reasoned about. `python
bootstrap/tests/_gate_manifest.py verify --no-collect` at `99c8d55` reports
**13** violations. Appending one comment line to `conftest.py` and re-running
reports **14**, the new one being:

```
FROZEN-MODIFIED: bootstrap/tests/conftest.py (gate file edited — sha differs)
```

Restored; `git status --short` clean.

This is load-bearing, not a typo. The section it sits in is titled *"The
frozen-file question resolves favourably **and is the reason to act now**"*,
and its argument is that the delta being added is one already scheduled for
re-pin under SC4's *"fold in"*. That argument covers `test_security_lint.py`
and covers **nothing** for `conftest.py`: G6 does not join an existing delta,
it opens a new one, on a file whose own row (`dev/PLANNING.md:944-950`) names
no ceremony and whose staleness nothing else schedules.

**Satisfier** -- correct the sentence, then choose: (a) drop G6 from Class A
until a ceremony makes it cheap, or (b) obtain the Maintainer's authorization
to extend the SC4 "fold in" scope to `conftest.py`, quoted verbatim, and say so
in the proposal. Silence does not close it, because the current text tells a
Decision-maker the cost is zero.

### [I2] SC5's second assertion is red the moment it is written -- the sole `ALLOWLIST` entry is already stale

Class A promises SC5 as *"two assertions: key still on disk; key still produced
by a live finding"*. The second one fails today.

Measured, canonical interpreter, `bandit` 1.9.4, over the real `scan_targets()`
surface (76 files): **118 findings, all LOW; zero MEDIUM+**; and **no `B310` at
any severity** for `templates/modules/team-gated/link_check.py`. The sole
`ALLOWLIST` key (`bootstrap/security_check.py:51-60`) is
`("templates/modules/team-gated/link_check.py", "B310")`.

I checked the obvious confound: Bandit can still emit it. A two-line synthetic
file calling `urllib.request.urlopen` scans to `B310 MEDIUM` under the same
Bandit. The reason the real file no longer trips it is in the file: the
allowlist rationale describes *"urllib.request.urlopen in
link_check._probe_external"*, but `_probe_external` now builds an opener
(`urllib.request.build_opener(...)`, `templates/modules/team-gated/link_check.py:332`)
and issues a `Request` (`:350`) -- neither of which `B310` matches. So the
entry is exactly the silent latch SC5 predicts, **already latched**.

The consequence is a scope change, not a bigger assertion. Writing `assert
set(ALLOWLIST) <= live_medium_plus_keys` turns the suite red, and the fix is to
**delete a suppression from the release security gate's single-source
allowlist** -- `bootstrap/security_check.py`, which is not in `Touches`, is
itself `FROZEN-MODIFIED`, and is the module the release command and the dev
gate both import. That is an `accept` (fix the thing), folded invisibly inside
a row the proposal presents as a `guard`.

Second, smaller cost on the same row: the "live finding" assertion must consume
a Bandit report, so it either lands inside `test_no_blocking_security_findings`
-- inheriting the deliberate skip-locally / fail-in-CI posture documented at
`bootstrap/tests/test_security_lint.py:11-15` and implemented at `:118-128`,
noting Cairn has no CI -- or requires a shared fixture the file does not have.

**Satisfier** -- either (a) re-scope SC5 to assertion 1 (`key still on disk`,
which passes today and is genuinely one line), and route the stale-entry
removal as its own item with the Maintainer, or (b) keep both, add
`bootstrap/security_check.py` to `Touches`, state on the record that a release-
gate suppression is being deleted, and re-argue the plan-review tier against
that.

### [I3] SC3's assertion, as worded, is either vacuous or already present; the only mutation-provable version pins a different claim

Three mutations, each restored afterwards; the file is byte-identical to
`99c8d55` now (`git status --short` clean).

**Mutation A -- delete the manifest union from `scan_targets()`** (the row's own
stated failure state: *"a later refactor deletes the union and the scan
silently narrows"*). Result: **3 nodes red** in
`bootstrap/tests/test_security_lint.py` --
`test_every_manifest_verbatim_py_is_scanned_by_some_path`,
`test_every_templates_py_on_disk_is_release_scanned`, and
`test_the_two_session_lifecycle_tools_are_scanned_by_name`. The narrowing is
already triple-guarded and is **not silent**. A fourth assertion of the same
property adds nothing.

**Mutation C -- delete *both* registry loops** (the literal "not a replacement"
half). Result: `scan_targets()` returns **76 targets before and after**; 10/10
green. Measured: registry-derived = **42**, manifest-derived = **44**, and
`registry ⊆ manifest` **exactly**, the delta being the two
`templates/skills/_lib/` tools. So the claim at
`bootstrap/security_check.py:123-125` -- *"a UNION WITH the two registry loops
above, never a replacement"* -- is **unobservable from behavior**: the loops
contribute nothing the manifest does not. Any assertion of it passes under its
own mutation, which is the proposal's own definition of an assertion that
*"guards nothing"*.

**Mutation B' -- replace the manifest loop with a hand-rolled loop over the
install module's `_SKILLS_MAPPINGS`.** Result: **10/10 green**. This is the
blind spot `bootstrap/tests/test_security_lint.py:194-203` already documents in
prose (*"delete the manifest union ... and add a hand-written `_SKILLS_MAPPINGS`
loop in its place and this test is still green"*), and it is the only real
residual gap on this row. It *is* closable in one assertion -- a sentinel:
patch `install_manifest` on the `bootstrap.security_check` module to return a
single fabricated verbatim `.py` row and assert `scan_targets()` reaches it. I
confirmed the sentinel is reached at HEAD, and Mutation B' is precisely what
makes it red.

So a one-assertion SC3 guard exists, but it pins **"`scan_targets()` consumes
the published install manifest"**, not **"the enumeration is a union with the
manifest, not a replacement"** -- which is what the Class A table says it will
assert. The proposal transcribed the board row's wording without resolving
which of the two properties is actually unguarded, and the two have opposite
answers.

**Satisfier** -- restate SC3's assertion as the consumption claim, name Mutation
B' as its mutation proof in the plan, and record on the row (or in the archive
block) that the narrowing half is already covered by the three nodes above --
otherwise a later reader will believe a guard was added where one already
existed.

### [I4] G6 is not "one assertion at session end": it is a session hook plus a skip policy over 91 skip sites, and it cannot be named as a `guard` node

Three separate problems, in increasing order of difficulty.

**(a) It cannot satisfy the grammar.** `doctrine/lifecycle.md:437-444` defines
`guard` as *"homed in an artifact that **executes** ... The entry **names the
node** (`path::node`)"*. `bootstrap/tests/conftest.py` collects **zero** nodes
(`pytest --collect-only -q | grep -c conftest` -> 0), and a
`pytest_sessionfinish` hook is not addressable as a node id. G6's proposed home
therefore cannot be written in the vocabulary this proposal exists to execute.
The proposal's invariant (1) requires *"a named node that exists"*; for G6 there
is no name to give.

**(b) "0 skipped" is environment-conditional by construction.** Measured in
`bootstrap/tests/`: **54** modules carry a module-level `pytestmark =
pytest.mark.skipif`, there are **80** `skipif` occurrences in total, and **37**
runtime `pytest.skip(` call sites. Several are deliberate design:
`bootstrap/tests/test_security_lint.py:118-128` *chooses* to skip locally when
Bandit is absent, and its module docstring (`:11-15`) argues for it. And
`bootstrap/DEPENDENCY_BUDGET.md:142` records **3 skipped** under Python 3.12.9
as a legitimate diagnostic measurement in a published comparison table. So a
hard `assert skipped == 0` is a **policy change** to those surfaces, not a
guard over them; it needs either an allowance list or an opt-in flag, and that
is a design decision with its own review.

**(c) It would be green for the wrong reason.** The invariant holds on this
host -- my baseline run is 0 skipped. G6's own text
(`dev/PLANNING.md:944-950`, and the archived source at
`dev/plans/archive/profile-parse-fail-open.md:658`) is about *"a PyYAML-less
host"* and *"the parity sweep plus both canaries"*. An assertion written and
mutation-proven here proves nothing about the host the row is about; the mutation
that must fail is "run on a host missing an optional dep", which is not a
mutation this tree can stage.

**Satisfier** -- drop G6 from Class A. Its own trigger -- *"the first suite run
reporting a non-zero skip count, or the next change to
`bootstrap/tests/conftest.py`"* -- has not fired, and this pass is not that
change except by choosing to make it one. If it stays, it must be re-specified
as a flagged ceremony check with a stated allowance list, homed in a real test
module so it has a `path::node`, and its tier re-argued.

### [I5] Invariant (1)'s claimed mechanical enforcer does not exist -- this lineage's recorded failure mode, eighth instance

*Author-accounting* states: *"(1) Every row that leaves the board leaves with a
token and, for `guard`, a named node that exists -- enforcer: the archive
`Dispositions:` block plus the node running in the suite. **This is the first
invariant in this lineage with a real mechanical enforcer**: a `guard` whose
node does not exist fails collection."*

It does not fail collection. Pytest collection fails on an import or syntax
error inside a test *file*; a node id written in a **commit body** is prose
pytest never reads. I looked for anything that would close the loop:

* `bootstrap/tests/test_lifecycle_contract.py:536-576` -- the only suite node
  touching this -- checks that a `Dispositions:` **or** `Follow-ups migrated
  to:` block is *present*. It asserts nothing about tokens or nodes.
* `subsystems.py` in `templates/modules/default-on/_lifecycle_metrics/`
  (`:88-98`) buckets the `guard` token for the metrics report and validates no
  node.
* `scripts/claim_check.py` -- the one checker that reads prose paths -- has no
  concept of a node id. Probed: the `guard`-form citation of
  `bootstrap/tests/test_security_lint.py` > `test_allowlist_entries_have_rationale`,
  a node that **does** exist, is hard-flagged `[path] cited path does not
  resolve`; a fabricated node is flagged identically. It cannot discriminate.
  And commit bodies are not scanned by it at all.

So a `guard` recorded against a node that was never written is **fail-open and
silent** -- which is the failure the disposition exists to prevent. This is
`gate-claims-vs-enforcement`, in the same *Author-accounting > Invariants* slot
where `deferral-discipline`'s [I1] caught it one artifact earlier in this same
lineage. The claim is made at the strength intended, not the strength
delivered, for the eighth recorded time.

**A corollary that will bite at commit time.** Because `claim_check` treats
`<repo-path>.py::<node>` as one unresolvable path, the `guard` grammar's
mandated citation form is **unwritable in any claim-checked file** whenever the
path has a real repo prefix. `tests/x.py::test_y` (the fictional form used in
`doctrine/proposals.md` and `doctrine/plans.md`) passes only because `tests/` is
not a Cairn top-level directory. `python scripts/check_cairn.py` is green at
HEAD (176 files) because no real `guard` has ever been written; this pass would
be the first to hit it. **Demonstrated on this review**: my first draft cited
the node in the doctrine-mandated form and
`python scripts/claim_check.py dev/proposals/2026-08-04-claude-board-drain-guards.md`
returned rc=1 on exactly that line. I rewrote it as `<path>` > `<node>` to get
a clean run -- which is the workaround, not the fix.

**Satisfier** -- mark invariant (1) documentary, naming its real enforcer (a
reviewer opening the node), exactly as `deferral-discipline`'s Response did for
its invariant 3; and record the `claim_check` collision with the chosen
workaround (a file-scoped `claim-check-allow` directive, or citing the node in
the `<path>` > `<node>` form this review uses) so the implementing agent does
not discover it at the commit gate.

### [I6] Class B's population is not what it says: at least 10 of the "~31 rows imported from another repository" are this repo's own two-day-old plan residuals

I re-derived the split rather than inheriting [C4]'s. Parsing
`dev/PLANNING.md:535-1019` into top-level bullets: **58 rows**, split at the
first `*From ...*` header (`:802`) into **31 above / 27 below**, with **29**
carrying a `trigger:|revive|revival condition` match. That reproduces [C4]'s
table exactly, so the arithmetic is sound.

The provenance is not. "Above the first `*From`" is a *position*, and the 31
contains two groups explicitly labelled as this repo's own:

* `**Scan coverage** *(residuals from plan `scan-coverage`, homed 2026-08-04 so
  the plan can archive)*` at `:683` -- rows SC1-SC4 at `:686`, `:698`, `:710`,
  `:722`.
* `**Release authenticity** *(residuals from plan `release-authenticity`)*` at
  `:741` -- six rows at `:742`, `:751`, `:754`, `:757`, `:762`, `:768`.

Ten rows, none imported, all homed within the last two days by Cairn plans.
"The ~31 rows imported from another repository are **unassessed**" is therefore
true of at most 21, and the ten it wrongly includes are the *best*-documented
rows in the half. Three consequences follow directly:

1. **SC4 is inside Class B's stated population** and carries
   `**DISPOSITIONED AND SCHEDULED — do not re-adjudicate**` (`:736`). Class B as
   scoped walks straight into it.
2. **SC3 is inside Class B too** (`:710` < `:802`), so Class A and Class B
   overlap on a row the proposal treats as belonging to exactly one class.
3. **G3 and G4 are *not* in Class B.** *Explicitly not in scope* says they are
   *"Assessed in Class B, not written here"*, but G3 (`:924`) and G4 (`:931`)
   sit in the census half, outside the 31.

Also worth stating precisely: the shortfall does not "concentrate" as strongly
as the sentence implies -- 18 of 31 above lack a condition (58%) against 11 of
27 below (41%). Real, but a difference of degree.

**Satisfier** -- define Class B by the header groups it actually means rather
than by a line position, restate the count as measured, and say explicitly what
happens to SC4 and to the SC3 overlap.

### [I7] "Record whether the condition is already satisfied" is undefined for 18 of the 31, and is a research task for several more

The deliverable is *"Read them and record, per row, whether its **stated
condition** is already satisfied."* **18 of the 31 state no condition at all.**
For those the instruction has no referent, and what it silently becomes is
"work out what this row is about and whether the work happened" -- per-row
research across `bootstrap/`, `templates/` and `doctrine/`.

I hand-read the 18 rather than asserting from the count. The shapes that defeat
the framing:

* `:616` -- *"End-gate frozen-set decision (C-#4) -- whether the A/B/C engine
  packages fold into the gate manifest's `frozen_files`."* That is a
  **decision**, not a condition; "already satisfied?" is category-inapplicable,
  and `doctrine/lifecycle.md:462-464` puts "needs a Decision" beyond author
  disposition.
* `:614` -- *"Facade-loader symlink hardening (C-#3) -- refuse any engine
  submodule that is a symlink or resolves out-of-tree, across all three
  facades."* Answering "already satisfied?" means reading three facade loaders
  in the scaffold engine, an `AGENTS.md`-named high-risk surface, and reasoning
  about symlink containment. That is a security read, not a board read.
* `:663` (language-neutral conformance fixtures), `:776` (constructive
  readiness), `:785` and `:788` (future-use mechanisms, "post-v1") are unbuilt
  design, and the *Explicitly not in scope* fence names only three design rows,
  not these.

Median row length in this half is **212 characters**. That is what makes the
rows *look* cheap; the cheapness is in the row, not in the answer, and
*Alternatives considered* rests the whole case for Class B on *"reading ~31
short rows is cheap."*

This is where the predecessor's over-scoping can return under a new name.
*Alternatives* rejects "adjudicate all 58 with code access" as the
huge-branching job -- but Class B is a per-row adjudication of 31 of them with
the verdict softened from *disposition* to *assessment*, producing the same
artifact. The boundary that makes Class A bounded (three named rows, three named
files) has no counterpart in Class B.

**Satisfier** -- give Class B an explicit **stopping rule** rather than a
population: e.g. *"a row is assessed only if its own text states a condition
checkable by a single grep, file-existence test, or test-node run; every other
row is left untouched and named as unassessed."* Or cut Class B and ship Class A
alone. What must not happen is a class whose bound is a row count in a document
the proposal has miscounted ([I6]).

### [I8] Class B re-opens work a landed Maintainer Decision explicitly declined to park, and the quoted chat direction does not authorize it

The predecessor's Decision
(`dev/proposals/archive/2026-08-04-claude-board-retro-disposition.md:1040-1043`)
closes with:

> **What is not carried.** No `defer`, no successor artifact, no board row. The
> withdrawn adjudication is **not** parked for later revival -- the reviewer's
> necessity finding is the reason it should not happen, and preserving it as a
> future obligation would re-commit the error this lineage exists to correct.

The proposal's *Context* engages [I3] and [C4] and does not mention this
paragraph. It is a landed Maintainer Decision, and Class B is materially the
work it declined -- at 31/58 scale rather than 59/59.

The authority the proposal offers instead is a chat sentence: *"do the focused,
targeted job that actually has a chance of success instead of deferring the goal
because of the narrowest framing."* Two problems. It reads as authorization for
Class A -- the *focused, targeted* half -- and Class B is precisely the
unfocused half. And per `doctrine/lifecycle.md:288-299` (*"Chat preferences are
not a lifecycle Decision"*), a chat phrase is drafting input, cited as
*maintainer preference during drafting*; it is not a Decision, and it certainly
does not reverse one.

To be clear about the other side: there **is** a real basis for revisiting. The
necessity finding the Decision rested on was drawn from a ~12-row sample of the
census half, and [C4] falsified its generalization to the imported half;
`dev/PLANNING.md:550-558` already records that correction. That is a legitimate
argument for re-opening -- and it should be *made*, in front of the Maintainer,
rather than routed around by not citing the paragraph.

**Satisfier** -- quote the Decision's *What is not carried* paragraph, state that
[C4] falsified its premise for this half specifically, and present Class B as an
explicit request for re-authorization. Or drop Class B and let Class A stand on
the direction that plainly does cover it.

### [I9] "Withdrawn at Internal review" mis-describes the record, and the counter-evidence is attributed to the wrong review

Three sentence-level corrections; none touches the substance, and all three are
the kind of drift that becomes load-bearing when a later reader inherits it.

1. **The predecessor was not withdrawn.** It was **accepted as revised** -- the
   hygiene scope H1-H5 -- implemented, code-reviewed, and archived (`de50fb8`).
   What was withdrawn was its *mass-adjudication scope*, by the author's
   Response, ratified in the Decision. The distinction is exactly what [I8] is
   about: a withdrawn proposal leaves no Decision to engage; this one does.
2. **[C4] is not "the review that produced the withdrawal."** [C4] is in the
   **Code review** (`:1277`), which ran after the Response and after the hygiene
   implementation landed. The withdrawal was produced by the **Internal
   review**'s [I3].
3. **"without anyone noticing it was an argument against the withdrawal"** is
   not so. [I3] itself quoted SC3's and SC5's text (`:359-364`) in the finding
   that produced the narrowing, and [C4]'s own satisfier says it explicitly:
   *"leaving open that a scoped `guard`/`accept` pass can and, for the one- and
   two-assertion guards the board itself names, should."* The record noticed
   twice. The proposal is executing what two reviewers already flagged, which is
   a **stronger** provenance than "nobody noticed."

**Satisfier** -- three edits to *Context*. The argument survives all three intact
and gets better for it.

### [I10] Class A rows are named by closed, append-only artifacts, and no forwarding entry is specified

`doctrine/lifecycle.md:465-469`: *"A follow-up **named by a closed artifact's
disposition block** is ineligible for `wontfix` without the Maintainer, and
**any re-routing of it is recorded as a forwarding entry**. An archived record
is append-only."* Note the second clause is not conditioned on `wontfix` -- it
covers *any* re-route, including board -> `guard`.

All three Class A rows qualify:

* **G6** is named at `dev/plans/archive/profile-parse-fail-open.md:658` --
  `| G6 | dev/PLANNING.md | Row: nothing mechanically enforces the suite's 0
  skipped invariant ... |` -- in an archived plan.
* **SC3** is named at `dev/plans/archive/scan-coverage.md:990-997`, whose
  *Lasting-truth migration* section lists *"the unguarded monotonicity claim"*
  among the follow-ups the plan owes a home; the board's own header at `:683`
  says the SC rows were *"homed 2026-08-04 **so the plan can archive**"*.
* **SC5** sits under `*From `scan-coverage` (1):*` (`:831`), the census block
  recording the same discharge.

The board says this itself, three paragraphs above the rows being moved
(`dev/PLANNING.md:576-584`): **7** commit bodies name this section, **13** name
`dev/PLANNING.md` at all, and *"Commit bodies are the **most immutable** record
of all and no artifact-level enumeration reaches them."* That block exists
because the predecessor's H4 put it there for exactly this hazard. The proposal
edits this section and does not use it. Its *Evidence* line records only
*"tokens recorded in the archive commit body"*, and *Edge cases* covers a row
that grows and a row partly satisfied -- not this.

**Satisfier** -- one line in the verification plan: every row that leaves the
board leaves with a forwarding entry naming the archived artifact that homed it,
and the same rule applies to any Class B row that closes.

### [I11] `Touches` and the plan-review tier are under-scoped for what the pass actually reaches

`Touches` names three files. Per [I2] the work also reaches
`bootstrap/security_check.py` -- the release gate's single-source `ALLOWLIST`,
itself `FROZEN-MODIFIED` -- and, if any re-pin happens in-pass rather than at
the ceremony, `bootstrap/tests/fixtures/gate_manifest.json`.

The tier line justifies `required(Internal)` solely as *"writes assertions into
an already-`FROZEN-MODIFIED` gate file"*. Deleting a suppression from the
release security gate is a different class of change from adding a test
assertion, and per [I1] the frozen-file premise does not hold for half the
surface anyway.

**Satisfier** -- extend `Touches`; state explicitly whether the allowlist edit is
in or out of scope; re-argue the tier against the answer rather than against the
premise [I1] falsifies.

---

### On the frozen-file argument -- I take a position

**It is rationalizing, and the measurement says so.** Three grounds, then the
half that is genuinely true.

**(a) It is factually wrong for half the surface it covers.** Per [I1],
`conftest.py` is frozen; the argument protects one of the two Class A files and
silently asserts a zero cost for the other.

**(b) The premise is falsified by the delta's own history.** `verify
--no-collect` at `99c8d55` reports **13** `FROZEN-MODIFIED` violations. SC4's
Maintainer disposition -- *"SC4 - fold in"*, `dev/PLANNING.md:731` -- was
granted over **three**, named in that row. The manifest was last pinned at
`e45e1fc` (2026-08-03); of today's thirteen, six last changed on **2026-08-04**,
after that pin. The delta grew **4.3x past the scope the Maintainer
dispositioned, inside two days**, and no artifact has re-derived it -- SC4's
"three" is stale on the board right now. That is what "the file is already
dirty, so adding is free" produces when every author applies it independently:
each increment is individually free and nobody owns the sum.

**(c) What was authorized is narrower than what is being claimed.** *"Fold in"*
authorizes **re-pinning a measured delta at a ceremony**. It is not a standing
licence for later authors to enlarge that delta. Enlarging a dispositioned scope
is a scope decision, and this lineage's own rule -- the one it just landed --
puts scope with the Maintainer.

**The steelmanned half, which should be kept.** The *marginal re-pin cost* of
one more changed file really is near zero, because the ceremony re-pins whatever
is stale when it runs. A rule that no frozen file may ever be touched between
ceremonies would stop development. But that argument establishes that frozen
status here is **neutral** -- not that it is a **reason to act now**. The
proposal makes it the affirmative reason (*"resolves favourably and is the
reason to act now"*), and promoting a neutral fact to a positive argument is the
move that lets deltas accumulate unowned. The honest form is: *"the marginal
re-pin cost is zero; the reason to act now is SC5's trigger, and the frozen
status is not an obstacle."* That version is true, and it does not license
`conftest.py`.

### On whether `guard` is the right token -- mostly yes, with three exceptions

I tested the suspicion that writing the assertion *fixes* the thing and should
therefore be `accept`. It does not, and `guard` is correct for SC3 and SC5 as
re-specified: `accept` is *"fixed in this artifact's scope"*
(`doctrine/lifecycle.md:434-436`), and writing a guard changes neither
`scan_targets()` nor the `ALLOWLIST` -- it homes each row's **mechanical revival
condition** (*"any edit to `scan_targets()`"*, *"any edit to `ALLOWLIST`"*)
where that condition fires. That is `guard`'s definition verbatim.

The mislabelling is in three narrower places:

1. **G6 cannot satisfy the grammar's `path::node` requirement at all** ([I4a]).
2. **SC5's stale-entry removal is `accept`, not `guard`** ([I2]) -- fixing a
   thing inside this scope -- and the proposal folds it invisibly into a row it
   presents as a single `guard`.
3. **Class B's "a row that is already satisfied is `accept` (the work
   happened)" misuses the token.** `accept` is *fixed in **this** artifact's
   scope*; a row some *other* artifact already satisfied was not. The
   vocabulary has no token for "already satisfied elsewhere", and inventing one
   by stretching `accept` is precisely the parallel-vocabulary error
   `deferral-discipline`'s [I2] spent a round removing. The honest routing is
   what the predecessor's H3 did for SC4: record the satisfying artifact and
   treat the removal as board hygiene, or ask the Maintainer for a token.

---

### Covered

* **#1 Claims** -- re-derived every load-bearing figure. **Confirmed**: 58 rows
  in `dev/PLANNING.md:535-1019`, 31/27 at the `:802` split, 29 with a
  trigger/revival match (reproduces [C4] exactly); `test_security_lint.py` is
  `FROZEN-MODIFIED`; SC5's trigger text at `:841-843`; SC3's at `:719-720`;
  SC4's *"fold in"* at `:731`; `guard` has never been used (no archived artifact
  or commit body carries one). **Refuted**: *"`conftest.py` is not frozen"*
  ([I1], mutation-measured 13 -> 14); *"two assertions"* for SC5 ([I2], 0 MEDIUM+
  findings, B310 absent, synthetic probe proves Bandit can still emit it);
  *"one assertion"* for SC3 ([I3], three mutations); *"a `guard` whose node does
  not exist fails collection"* ([I5]); *"~31 rows imported from another
  repository"* ([I6], >=10 are Cairn-native); *"withdrawn at Internal review"*
  and the [C4] attribution ([I9]).
* **#2 Production path exercised by tests** -- at proposal review the bar is
  *promised and scoped*. Mutation proof is promised and is the right instrument;
  applied, it falsifies two of three rows. The specific proving mutations are
  named in [I3] (B'), [I2] (the allowlist assertion is red without any
  mutation), and [I4c] (G6's proving mutation cannot be staged on this tree).
* **#3 Design completeness** -- Class A and Class B are not disjoint ([I6.2]);
  Class B's population excludes two rows the proposal routes into it ([I6.3]);
  the "already satisfied" case has no token ([I2] of the *guard* section);
  inbound references from closed artifacts are unhandled ([I10]); the `path::node`
  form collides with `claim_check` ([I5] corollary).
* **#4 Silent failure / fail-closed** -- invariant (1) is fail-open with a named
  mechanical enforcer that does not exist ([I5]); a vacuous SC3 assertion would
  be fail-open and green ([I3], Mutation C: 76 targets before and after, 10/10
  pass); a G6 assertion is green here and untested where it matters ([I4c]). The
  proposal's own *"an assertion that passes both ways is worse than no
  assertion"* is the correct posture and is the standard I applied.
* **#5 Cross-document consistency** -- swept `doctrine/`, `bootstrap/tests/`,
  `templates/`, `dev/plans/archive/`, `dev/proposals/archive/`, `scripts/`,
  `tools/` for `guard`, `Dispositions:`, `0 skipped`, `path::node`. Found the
  predecessor's Decision paragraph unengaged ([I8]), the inbound-reference block
  the proposal edits but does not use ([I10]), and `claim_check`'s treatment of
  node ids ([I5]). `python scripts/check_cairn.py` at HEAD: **OK, 176 files, no
  issues**.
* **#6 Drift** -- `bootstrap/tests/fixtures/gate_manifest.json` pinned at
  `e45e1fc` (2026-08-03), 13 files diverged today against the 3 SC4 records; the
  board's SC4 figure is stale (*On the frozen-file argument*, ground b).
* **#7 Lifecycle / process placement** -- Class B lacks authorization and
  re-opens a landed Decision ([I8]); the tier is argued from a premise [I1]
  falsifies ([I11]); the forwarding-entry serialization point is unspecified
  ([I10]).
* **#8 Domain validity & scope** -- the proposal's own *Signals* bright line
  (*"Class A grows past a handful ... the right response is to stop"*) has fired
  on 2 of 3 rows; Class B reproduces the withdrawn adjudication at half scale
  under a softer verb ([I7]).
* **#9 Name the satisfier** -- every finding above names one; none is a bare
  observation.

### Not covered / low confidence

* **Same-type reviewer -- no cross-type independence on this pass.** I am Claude
  reading a Claude-authored proposal in a fresh session. That is the Internal
  floor and nothing more, and the author and I share the search habits that
  found (and could equally have missed) [I5].
* **I could not verify the Maintainer quotation.** *"do the focused, targeted
  job ..."* is a chat sentence with no artifact behind it. I take it as
  accurately transcribed; I note only that its scope is contested ([I8]) and
  that `doctrine/lifecycle.md:288-299` governs what it can authorize.
* **I did not write any of the three assertions.** I mutated the *subjects* and
  measured what the existing suite does; the sentinel guard in [I3] I proved
  reachable at HEAD and red under Mutation B', but I did not land it as a test
  node with fixtures and a docstring. The step from "the assertion is
  well-defined" to "the assertion is written and reviewable" is unmeasured.
* **I did not adjudicate the 31 Class B rows.** I hand-read the 18 with no
  stated condition and sampled the rest; I make no claim about how many would
  close. That is the proposal's own deliverable and I have not pre-empted it --
  [I7] is about the instruction being undefined, not about the answer.
* **G6's real environment is unstageable here.** Every figure I have is from a
  fully-provisioned host (bandit and vermin present, POSIX, non-root, PyYAML
  available). The PyYAML-less host G6 is about is the one configuration I could
  not measure.
* **I did not run `python bootstrap/security_check.py` end to end**, only the
  Bandit half through the same `scan_targets()` surface. The `check_cairn` leg I
  ran separately; the composed exit code is untested on this pass.
* **The Bandit finding is version-sensitive.** [I2] rests on `bandit` 1.9.4. A
  different Bandit could restore `B310`; I controlled for the obvious case (the
  synthetic `urlopen` probe still scans MEDIUM) but not for the history of when
  `link_check._probe_external` stopped matching.

### Second-round recommendation

**Recommended -- an External (different-agent-type) round, but only if the
Decision keeps Class B or keeps the SC5 allowlist edit.**

Grounded in the coverage line, not blast radius:

1. If Class B survives, the question in front of the Maintainer is whether a
   landed Decision's *"not parked for later revival"* is being re-opened on
   sound grounds ([I8]). That is a judgment about the deliberation record
   itself, and I am the same agent type as its author on both sides of it.
2. If the SC5 allowlist deletion stays in scope, a release-gate suppression is
   being removed on the strength of one reviewer's Bandit run. That is a
   security-gate change and the different-agent-type floor is cheap relative to
   what it protects.
3. Against, and I think decisively: if the Decision cuts Class B, drops G6, and
   re-scopes SC5 to its on-disk half, what remains is **one sentinel assertion
   in one test file** with a named mutation proof. An External round on that is
   ceremony. Internal-only is the right tier for the residue.

### Verdict

**SPLIT.**

Not REVISE, because the problem is not that individual claims need correcting
-- though eleven do. It is that the proposal's two classes, and two of its three
Class A rows, are four different kinds of work bundled behind one boundedness
claim that the measurements do not support:

* **Ship now, after the [I3] and [I5] corrections:** the SC3 guard, re-specified
  as *"`scan_targets()` consumes the published install manifest"*, mutation-proven
  by Mutation B'. One assertion, one file already `FROZEN-MODIFIED`, one named
  mutation, and its own trigger genuinely fires. This is the artifact the
  Maintainer's *"focused, targeted job"* describes, and it exercises the `guard`
  token for the first time, which was the point.
* **Its own item:** the stale `ALLOWLIST` entry ([I2]). It is an `accept`, it
  edits the release security gate, and it deserves to be visible rather than
  riding inside a row labelled `guard`. SC5's on-disk half can ship with SC3 or
  with it.
* **Back on the board, unchanged:** G6 ([I1], [I4]). Its home is frozen with no
  scheduled re-pin, it cannot be named as a `guard` node, and it needs a skip
  policy over 91 skip sites. The proposal's own edge-case rule already dictates
  this outcome -- *"a Class A row whose assertion turns out to need more than two
  assertions -> it leaves Class A and stays on the board, unchanged."*
* **A separate artifact with its own authorization:** Class B ([I6]-[I8]). Its
  population is miscounted, its instruction is undefined for 18 of 31 rows, and
  it re-opens what a Maintainer Decision declined to park. If it is right, it is
  right on an argument that has to be made in front of the Maintainer, not
  inherited from a chat sentence that describes the other half of this proposal.

SPLIT rather than HOLD because the core is real and small: the board says a
guard should be written, the token exists and has never been used, and after
the corrections above there is exactly one assertion that is genuinely one
assertion. SPLIT rather than REVISE because keeping the four together preserves
the thing that produced every finding here -- a boundedness claim asserted at
the strength intended rather than the strength delivered, which is now the
**eighth** recorded instance in this lineage in one day, and this time it is in
the sentence that says *"What makes this bounded? Three assertions and one
read."*

Of the three assertions, one is one assertion, one is red before it is written,
and one cannot be written in the vocabulary at all.

---

## Response -- Claude (Strategy) -- 2026-08-04

**Model**: claude-opus-5

Grammar: Proposal-Response. Eleven findings, accepted in full. The verdict is
**SPLIT** and the split is taken: **all three Class A guards and the whole of
Class B are removed from scope**, and the reviewer's bonus finding becomes the
proposal.

**[I1]** accept — *"`conftest.py` is not frozen"* is **false**, verified
independently: it is one of **164** entries in `frozen_files`
(`bootstrap/tests/fixtures/gate_manifest.json`). I inferred "not pinned" from
"not listed as `FROZEN-MODIFIED`", which only means *unmodified*. Reading an
absence of violation as an absence of a pin.

**[I2]** accept — SC5's second assertion is **red before it is written**: the
sole `ALLOWLIST` entry is stale (`link_check.py` no longer reaches `urlopen`).
So SC5 was never a write-a-guard job; it is a remove-a-stale-entry job that edits
`bootstrap/security_check.py` — the release-gate single source, `FROZEN-MODIFIED`,
and **absent from this proposal's `Touches`**. Removed from scope.

**[I3]** accept — SC3 as worded is **vacuous**: the registry is a subset of the
manifest, so deleting the union is a pure no-op (76 targets either way, 10/10
green). Only a re-specified claim is provable. Removed from scope; the board row
is corrected instead, because the row's *own stated remedy* is the defect.

**[I4]** accept — G6 is a session hook plus a skip *policy* over 91 skip sites,
against a documented 3-skipped configuration, and `conftest.py` collects zero
nodes so it could not satisfy `guard`'s `path::node` requirement anyway. Removed.

**[I5]** accept — *"a `guard` whose node does not exist fails collection"* is
**false**. That sentence was this proposal's claim to carry *"the first invariant
in this lineage with a real mechanical enforcer."* It has none. **The eighth
instance** of this lineage's failure mode, in the *same Author-accounting slot*
where `deferral-discipline`'s [I1] caught the identical error twelve hours
earlier. Retracted without replacement — no invariant here is mechanically
enforced.

**[I6]**, **[I7]**, **[I8]** accept — Class B is removed entirely. Its population
was wrong (>=10 of the "~31 imported" are Cairn-native plan residuals), its
central operation was undefined for **18 of 31** rows (no stated condition to
check), and it re-opened what the predecessor's **landed Decision** explicitly
declined to park. The Maintainer's quoted direction authorized the *focused*
half; Class B was not it.

**[I9]** accept — three history corrections. The predecessor was **accepted as
revised**, not "withdrawn"; **[C4] is its code review**, not the review that
produced the narrowing; and **[I3] noticed the SC3/SC5 text first**, so the
Context section's account of who saw what is wrong.

**[I10]**, **[I11]** accept — both moot under the revised scope (no board row
leaves, so no forwarding entry is owed; the allowlist edit is out of scope).

### The reviewer's bonus finding becomes the proposal

<!-- claim-check-allow: bootstrap/tests/test_security_lint.py::test_thing -->
<!-- ^ THE DEFECT, DEMONSTRATING ITSELF. This directive exists because the
     token below -- the `guard` citation form that `doctrine/lifecycle.md`
     mandates -- is hard-flagged by the very checker this proposal fixes. The
     proposal describing the bug cannot be committed without working around the
     bug. Delete this directive once R1 lands; it should then be unnecessary,
     and that is R1's acceptance check. -->

Reproduced independently: `python scripts/claim_check.py` over a file citing
`bootstrap/tests/test_security_lint.py::test_thing` hard-flags it as *"cited path
does not resolve"* and exits 1.

`doctrine/lifecycle.md` > "Archive precondition", landed this morning, **requires**
a `guard` to name its node as `path::node`. The checker rejects that form. So the
token's mandated citation is **unwritable in any claim-checked file** — every
proposal, plan and doc in the tree, and in every adopter tree, since
`claim_check.py` ships. The tree is green today only because no real `guard` has
ever been written; the first one fails the gate.

That is a defect in something that shipped hours ago, it blocks the token from
ever being used, and it outranks draining any board row.

**Maintainer direction, 2026-08-04**, choosing this scope over two larger
options: *"Checker fix + board corrections"* — ship the checker fix with the full
arc, correct the three board rows whose stated remedies are now known wrong, and
write no new guard.

---

## Revised proposal

**Status**: revised

**Restated:** *Make the `guard` token's mandated citation form writable, and
correct three board rows that prescribe the wrong remedy.*

### R1 — `claim_check` accepts `path::node`

`scripts/claim_check.py` already strips a `:N` / `:N-M` line-bounds suffix before
resolving (`_token_path_part`). Add the parallel case: a token containing `::`
resolves on its **path part only**. The node half is not verified — a static
checker cannot collect, and claiming otherwise would be a ninth instance.

**Twin discipline:** `templates/modules/default-on/claim_check.py` is
**byte-identical** (verified by `cmp`). Both copies move in one commit.

### R2 — tests, mutation-proven

In `bootstrap/tests/test_claim_check_module.py`:

* `path::node` where the path **exists** → no flag.
* `path::node` where the path **does not** exist → still flagged (the fix must
  not become a bypass — this is the assertion that matters).
* the existing `:N` line-bounds behaviour is unchanged.

Each mutation-proven: revert the fix, confirm assertion 1 fails; weaken the fix
to strip everything after any `:`, confirm assertion 3 fails.

### R3 — correct the three board rows

Each row's *own text* prescribes a remedy now known to be wrong. Leaving that
uncorrected is what caused this proposal's error, and would cause the next
reader's.

| Row | Correction |
|---|---|
| **SC3** | "the guard is one assertion" → the union assertion is **vacuous** (registry is a subset of the manifest); name the provable claim instead |
| **SC5** | "two assertions" → the entry is **already stale**; this is a `security_check.py` edit, not a guard |
| **G6** | "one assertion" → a session hook + skip policy over 91 sites, against a documented 3-skipped config |

### Explicitly not in scope

* **Writing any guard.** All three Class A rows removed per [I2]–[I4].
* **Class B**, entirely, per [I6]–[I8].
* **Removing the stale `ALLOWLIST` entry** — real, but it edits the release-gate
  single source and belongs to whoever owns that surface.

### Documentation / doctrine surface

**No doctrine change.** The `path::node` requirement is **correct as written** —
naming the node is what makes a `guard` verifiable. The defect is in the checker,
not the rule, so the rule does not move.

### Author-accounting — corrected

* **Invariants.** (1) *The fix does not become a bypass* — a `path::node` whose
  path is absent is still flagged. **Enforcer: R2's second assertion**, a real
  mechanical enforcer stated at exactly the strength it delivers: it guards the
  path half and nothing about the node half.
* **Failure modes.** An over-broad split (stripping at the first `:`) would
  swallow line-bounds citations — fails **open**, which R2's third assertion pins.
* **Known omissions.** **The node half is never verified.** A `guard` may cite a
  node that does not exist and nothing notices. That is the honest limit of a
  static checker, and it means `guard`'s enforcement is weaker than the parent
  proposal implied.
