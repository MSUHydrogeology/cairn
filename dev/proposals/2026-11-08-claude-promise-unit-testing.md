# Test each component's promises, not each change

**Author**: Claude Opus 5.5 (`claude-opus-5-5`; Strategy)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy -- removes tests from protected test files and edits `security_manifest.py`, both named high-risk surfaces
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-08
**In brief**: Make a component's promises, checked through its public entry point, the unit of testing, and remove the tests that only pin internal lines.

## Decision summary

Cairn's tests accumulate one change at a time. Each change adds tests for the
small piece of code it touched, and nothing ever removes them, so the suite
drifts toward pinning every line. Those tests break when code is refactored
without any change in behavior, and they slow every run.

This proposal changes the unit of testing:
- Each component keeps a short list of **promises**: what it does for callers,
  what it refuses, and the formats it reads and writes.
- Tests check those promises through the component's public entry point.
- A test written for one change is scaffolding. Before merge it is folded into
  a promise test or deleted.

It then removes existing tests that guard no promise, one component at a time.
The protected files all go under the single re-anchor already due before the
next release.

Costs:
- One plan of agent work.
- One Security Review of the removal set.
- A failing test points less precisely at the broken line.

Human operations: one re-anchor, which is already due for the release, so none
are added.

## Context

The Maintainer, in chat on 2026-11-08:

> "most of our tests are created to pin a behavior that involves the result of
> small parts of a single function, where the test was made when a particular
> change was done. This is really inefficient and will eventually lead to nearly
> all lines of code being pinned by tests. We need a different functional unit
> of testing. A strategy, not a reflexive practice"

and, on the ceremony this would need:

> "It's fine to reanchor. We need to do it for the next release anyway"

Measured at `176d2caf` (2026-11-08), counting `def test_` in `bootstrap/tests`:
- **4,068 test functions.**
- **Since `v0.6.0`:** about 506 test definitions were added and about 41
  removed, counting moves as removals.
- **862 tests (21%) call a private `_name` on a module directly.** This is a
  lower bound, since it misses `from x import _y`. They cluster in
  `test_gate_preflight.py` (98), `integration/test_meter.py` (69) and
  `test_upgrade.py` (67 of its 131).
- **Protected files:** 78 files, which `protected_test_roster.json` lists,
  hold 3,011 tests (74%). Removing a test from one of them holds the gate until
  a re-anchor. The other 59 files hold 1,057 tests, and changes there are
  report-only (`_gate_manifest.py`, `verify`).
- **Some files are already shaped this way.** 69 of the 70 tests in
  `test_claim_check_module.py` go through `check_text`, `check_file` or `main`.
  They are many input cases, not pins.

Three habits drive the growth:
1. Plan acceptance criteria ask for a test proving *that* change.
2. A mutant that survives review gets a new test pinned to the mutated line.
3. The suite-consolidation plan (`dev/plans/archive/2026-11-04-suite-consolidation.md`)
   forbade removing any test that catches a fault. Almost every pin catches
   *some* mutant.

`AGENTS.md` > Verification already says "Add or extend a test only for a
plausible uncovered fault" and asks for "a small workflow through the real
entry point". It says nothing about what the unit is, or when a test leaves.

## Proposal

**Outcome 1: the rule** (Cairn's own `AGENTS.md`, Verification). Replace the
sentence "Add or extend a test only for a plausible uncovered fault" with a
short rule that says:
- **The unit is a component's promise,** checked through its public entry
  point, called in-process where possible.
- **A behavior-preserving refactor should change no test.** A test that fails
  without a behavior change is a pin.
- **A test written for one change is scaffolding.** Write it to fail first,
  then fold it into the matching promise test or delete it before merge.
- **A surviving mutant is a question.** If it changes promised behavior, the
  promise test is missing or weak, so fix that test. If it doesn't, ask
  whether the mutated code is needed. Never add a test that pins the line.
- **Hostile inputs are one parameterized test per refusal promise.** For
  example, "refuses links" is one test run over many attack inputs, not one
  test per function per attack.
- **Direct tests of internals need a one-line reason in the test file.** An
  example is an algorithm core that the entry point is too coarse to reach.

This replaces rule text; it does not add a rule.

**Outcome 2: a pilot on `test_upgrade.py`** (131 tests, 72 s recorded). It is
adopter-facing, protected, and half its tests reach internals. Steps:
1. Write the upgrade path's promise list in the test file's docstring.
2. Make sure each promise has a test through `scaffold.py --upgrade` or its
   public function.
3. Remove the tests that guard no promise.
4. Record the counts and runtime before and after.

Then check the result: for each promise, one targeted mutant that changes
behavior at the entry point, one probe per mutant, no ledger. Every
behavior-changing mutant the old file caught must still be caught.

**Outcome 3: the removal pass,** component by component, in order of private
reach and runtime. This includes `test_gate_preflight.py`, `test_reanchor.py`,
`test_repin_ceremony.py` and the security families. All protected removals land
before the single release re-anchor. Edits to `security_manifest.py` keep a
reason for each removed member.

Three families wait, each on its own Decision:
- the meter tests, on the meter rescoping (weight review, item 4);
- the text-pin files, on exact-replacement editing (item 5);
- the claims tool, on whether its pre-commit half stays.

**Outcome 4, kept for later:** the same guidance in the shipped
`testing-discipline.md` module and `templates/core/AGENTS.md`. Revival
condition: the pilot meets its check below. Its home is the v0.7 board row.

## Rationale

Coupling to internals, not test count, is the cost: runtime, and edits on every
refactor. Checking promises through the entry point keeps the faults callers
can see and lets internals change freely. The weakness is that a failing test
points less precisely at the broken line, which the stack trace mostly makes up
for.

## Alternatives considered

- **Do nothing.** The suite keeps growing about 12 tests for every 1 removed,
  and the slow, protected families get slower.
- **Delete by judgment, without promise lists.** Faster, but nothing separates
  a pin from a real check, so real protection is lost silently.
- **Parameterize only.** This lowers the count, but every pin stays coupled to
  internals.

## Documentation / doctrine surface

- **Outcome 1:** Cairn's `AGENTS.md`, the governing layer.
- **Outcome 4:** the shipped module and core template, later.
- **Promise lists:** in each test file's docstring, the descriptive layer next
  to its tests.
- **Board:** a v0.7 row in `dev/PLANNING.md`.

## Evidence / verification plan

### Tests required

- Per component: counts and runtime before and after.
- The behavior-mutant check from Outcome 2.
- Collection before and after, recording every removed node. These are
  `_gate_manifest.py` `verify` notes for ordinary files and holds for
  protected ones.
- Boundary B is `wide`, because protected and trust-ceremony surfaces are
  touched.

### Examples / smoke checks

`python scripts/check_cairn.py` for prose, then the release certifying pair
after the re-anchor.

#### Security preflight — five questions, answered in writing

- **S1 — Who supplied it?** The removal set comes from the implementer's
  promise lists. The Security Review and the gate's hold on protected node loss
  check that set independently.
- **S2 — Can it fail?** The behavior-mutant check fails if a removed test was
  the only guard of a promise. Its mutants come from the promise list, not the
  removed tests.
- **S3 — What fires it, over what?** `_gate_manifest.py verify` runs over every
  collected node. The re-anchor accepts the losses one by one.
- **S4 — Which way does it break?** A wrong removal weakens a check, the less
  safe side. The hold, the Security Review and the mutant check guard it.
- **S5 — Who still wins?** A hostile input to an internal path that no promise
  names. This is closed only by enumeration, through the refusal promises.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

- A behavior-changing mutant the old file caught passes after the pilot.
- A real defect lands later that a removed test would have caught.
- Promise lists balloon until they mirror the code line by line.

## Scope delta

**Scope delta**: preserved

## Assurance path

**Assurance path**: high-assurance

## Review -- Claude Sonnet 5.5 (Reviewer) -- 2026-11-08

**Reviewed commit**: `e3f4716a9721b640203803df24242070c1189e33`
**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: approximately 6 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes: the problem and measured counts hold, but the rule shifts what the suite protects, which "Scope delta: preserved" hides (finding 1). -- `test_upgrade.py` has 131 tests; the quoted sentence is in `AGENTS.md` lines 303-304.
2. **Best alternative.** Do the pilot and the Outcome 1 rule only, deferring the Outcome 3 removal pass until the pilot's result is read; it loses nothing now and the re-anchor window is not at risk. Doing nothing keeps ~12 added per 1 removed. -- Outcome 3; `dev/plans/archive/2026-11-04-suite-consolidation.md`, C2.
3. **What would show it wrong?** Run the pilot's promise-derived mutants against the old file: any that it caught and the new file misses falsifies it. -- Outcome 2 check.

**Finding 1 -- Not blocking: name the narrowed protection.** The archived consolidation plan requires preserving fault detection (C2 "plausible faults against retained nodes"). Outcome 3 removes tests that catch mutants invisible at the entry point, which departs from it. Add one plain sentence for the Maintainer: "tests that only catch internal-only mutants are given up", and set Scope delta to match or get the allowance. Closes when the Decision text says it.

**Finding 2 -- Not blocking: specify the mutant check.** Say who writes the mutants (not the implementer who wrote the promise list; a reviewer or fixed per-promise list), how many per promise, and that "caught by the old file" is measured by running the old file at `e3f4716a` against each mutant. Also name `test_upgrade_removes_retired_files.py` (97 tests, 21 s) as in or out of the pilot.

**Finding 3 -- Not blocking: sequencing.** "All protected removals land before the single re-anchor" is a deadline, not a check. State that the gate holds (`COLLECTION-DROPPED` for protected files, `_gate_manifest.py` ~line 850) will show on every interim commit, and that ordinary-file removals are report-only. Verified: both behave as the proposal says.

**Verified:** 131 tests in `test_upgrade.py`; the file is in `protected_test_roster.json`; the quoted sentence exists. Explanation test: the Maintainer can restate the choice in one line.

**Coverage:** Not covered: the 862 private-call and 506/41 counts, other families' fit, Security Review. No tests run. About 360 words, over target because of the verification list.
