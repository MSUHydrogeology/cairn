# Test each component's promises, not each change

**Author**: Claude Opus 5.5 (`claude-opus-5-5`; Strategy)
**Status**: accepted
**Review**: usual + Security Review
**Proposed tier**: heavy -- removes tests from protected test files, edits `security_manifest.py`, and changes shipped methodology, templates and the install set
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-08
**In brief**: Make a component's promises, checked through its public entry point, the unit of testing in Cairn and in what Cairn ships, and remove Cairn's tests that only pin internal lines.

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

This deliberately narrows what the suite protects. Tests that catch only
internal mutants are given up: a mutant that changes code without changing
anything a caller can see. This reverses the archived suite-consolidation
plan's rule that no fault-catching test is removed, and it needs the
Maintainer's allowance at the Decision.

Adopters get the same strategy:
- the rule, in the shipped `AGENTS.md`;
- worked guidance, in the testing module;
- an acceptance prompt, in the shipped plan template;
- a small advisory tool that reports which tests reach into internals, and
  which test files have no promise list.

Costs:
- One plan of agent work.
- One shipped tool to maintain.
- One Security Review of each security or high-risk family's removal set,
  before its removals land.
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
- **Hostile state counts as caller-visible.** A fault seen only under hostile
  input or timing, such as a swapped link or a race, breaks a refusal
  promise. A test that injects that state through an internal hook is a
  declared exception, and it stays.

This replaces rule text; it does not add a rule.

<!-- claim-check-allow: tools/test_coupling.py -->
Superseded path `tools/test_coupling.py` appears only in historical records below.

Proposed paths:
- `scripts/test_coupling.py`
- `templates/modules/team-gated/test_coupling.py`

**Outcome 2: a pilot on `test_upgrade.py`** (131 tests, 72 s recorded). It is
adopter-facing, protected, and half its tests reach internals. Steps:
1. Write the upgrade path's promise list in the test file's docstring.
2. Make sure each promise has a test through `scaffold.py --upgrade` or its
   public function.
3. Remove the tests that guard no promise.
4. Record the counts and runtime before and after.

Then check the result:
1. **A fresh agent writes the mutants,** not the one who wrote the promise
   list or removed tests. It works from the promise list and the code under
   `bootstrap/_scaffold/`, without the tests. The same agent runs the probes
   and records the results.
2. **Each promise gets at least one mutant** that changes what a caller of
   the entry point sees. Each refusal promise also gets one mutant that makes
   it accept.
3. **Each mutant runs once against the old file and once against the new
   one.** The old file is taken at the commit before the pilot's first
   removal. One probe per mutant per file, with no ledger.
4. **The pilot fails if any mutant is caught by the old file and missed by
   the new one.** Restore a test or strengthen a promise test, and record the
   result in the plan.

`test_upgrade_removes_retired_files.py` (97 tests) is out of the pilot; it
goes in Outcome 3.

**Outcome 3: the removal pass,** component by component, in order of private
reach and runtime. It starts only after the pilot passes its check and the
result is recorded in the plan. It includes `test_gate_preflight.py`,
`test_reanchor.py`, `test_repin_ceremony.py`,
`test_upgrade_removes_retired_files.py` and the security families. Each family
goes through the same mutant check as the pilot, with one addition for
security families: the mutant agent also reads the code for defensive checks
and writes one "accepts" mutant for each check, whether or not the promise
list names it. That stops a narrow list from hiding a refusal.

Security and high-risk families get extra care:
- **Which families count.** Any test file guarding a security property or a
  named high-risk surface counts as protected for this proposal, held or not.
  That includes the unprotected files in `bootstrap/tests/security/`, such as
  `test_git_interpreter_binding_portable.py`.
- **Review first.** The removal set for each such family gets a Security
  Review from a fresh high-tier agent before its removals land.
- **`NATIVE_ONLY_NODE_IDS`.** The node list in `security_manifest.py` is
  hash-pinned, and `security_check.py` refuses if a listed node is missing. A
  listed node is removed only if that Security Review agrees, node by node.
  The list and its pinned hash and counts change under the re-anchor.
- **Reasons.** Edits to `security_manifest.py` keep a reason for each removed
  member.

Protected removals are batched for the single release re-anchor, and the
ordinary removals land as they're done:
- **Ordinary files:** `_gate_manifest.py verify` reports a removal as a note.
- **Protected files:** a removal is a `COLLECTION-DROPPED` hold until the
  re-anchor accepts it. `verify` runs in `scripts/repin.py` and
  `bootstrap/security_check.py`, not per commit, so these holds don't block
  ordinary work in between.
- **The re-anchor:** the plan hands the Maintainer the complete list of
  removed protected nodes, **grouped by promise**, so the runbook's
  per-row reasons stay a real check at this size
  (`bootstrap/REANCHOR_RUNBOOK.md`). Each group gives:
  - the removed nodes;
  - the retained check that guards the promise;
  - the mutant results.

  A node lacking a retained check or a mutant result is marked `stop` and is
  not removed. If the re-anchor comes before a family finishes, that family's
  removals wait for the next one.

Three families wait, each on its own Decision:
- the meter tests, on the meter rescoping (weight review, item 4);
- the text-pin files, on the functional-prose proposal
  (`dev/proposals/2026-11-08-claude-functional-prose-editing.md`);
- the claims tool, on whether its pre-commit half stays.

**Outcome 4: shipped capabilities for adopters.** These land after the
pilot passes, so the shipped guidance carries the measured result rather than
a guess.
- **Rule:** in `templates/core/AGENTS.md`, the same replacement sentence as
  Outcome 1, in tool-neutral wording.
- **Testing module:** in `templates/modules/team-gated/testing-discipline.md`,
  no new section. It extends the existing paragraph "Test promises, not
  wording or internals" with:
  - the promise list in a test file's docstring;
  - folding or deleting change tests;
  - surviving mutants as questions;
  - declared exceptions for testing internals.

  It sharpens "Consolidate without losing detection": map each removed test's
  caller-visible fault to a retained check, using the behavior-mutant check.
  That is the same obligation, made concrete, not a conflicting one. The
  paragraph's sentence on pinning shipped wording belongs to the
  functional-prose proposal, which replaces it.

  It also says, near the surviving-mutant rule, that refusal tests are
  promises. Tests that inject hostile state through an internal hook are
  declared exceptions that stay. The tool's report repeats this beside its
  private-reach counts, so a worst-first list is not read as a deletion list.

  The worked example sits in the module text:
  - **before:** a short pin-style test of `examples/scientific-minimal/water_budget.py`,
    written for the example;
  - **after:** the example's existing `test_water_budget.py`, which is already
    promise-shaped.
- **Plan template:** in `templates/core/dev/plans/_template.md`, the
  acceptance-criteria prompt asks which promise a change adds or alters, and
  through which entry point it is checked. It does not ask for "a test for
  this change".
- **Tool:** `scripts/test_coupling.py`, standard-library only and advisory. It
  reports and exits 0 unless `--strict` is passed.
  - **Source and install:** `templates/modules/team-gated/test_coupling.py`,
    installed verbatim by a testing-discipline `InstallSpec`, with the
    module's capability row updated.
  - **A project module** is an import in the test file that resolves, by
    path and without importing, to a file under the project root outside the
    tests directory.
  - **Private reach** is `from m import _x`, or `alias._x` where `alias` is
    bound to a project module. Dunder names are excluded. Test-local helpers
    and `conftest.py` fixtures are never counted, because they aren't project
    modules.
  - **A promise list** is a module docstring line `Promises:` followed by at
    least one `- ` line.
  - **Output:** counts per file, worst first. A file it cannot parse is
    reported, never skipped silently.
  - **Gaps:** it is Python only, and other languages are named as a gap.

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
- **Outcome 4:** the shipped module, core `AGENTS.md`, plan template and
  install set. The rule must clear the doctrine rate-limit gate
  (`docs/methodology/rationale.md` > "How the doctrine evolves under
  evidence"). The Maintainer chose the basis in chat on 2026-11-08:

  > "I think we should go forward with this on the basis that it is a good
  > idea, not on recurrence"

  The change goes forward on its merits. The gate limits rule changes made
  *from an incident* ("No doctrine change from a single incident"), and this
  proposal comes from a design review, not an incident. So no gate trigger is
  claimed, and recurrence is not offered as the basis. The second usual
  review's finding 3 read the gate as applying to every doctrine change. The
  Decision records the Maintainer's reading.
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
- Contract tests for `scripts/test_coupling.py` through its command line:
  - private-reach detection;
  - no count for test-local helpers, `conftest.py` fixtures or dunder names;
  - a missing promise list;
  - exit codes with and without `--strict`;
  - an unparsable file reported, never skipped silently, including
    `RecursionError` and decode failures;
  - no import machinery is used, neither `importlib` nor `find_spec`.
    Resolution is by path only;
  - resolved paths stay inside the project root. A link out of the root is
    reported, not followed;
  - printed names are escaped.
- **Forward test:** run on `examples/scientific-minimal`, the tool must flag
  no private reach. Run on Cairn's `test_upgrade.py`, it must agree with a
  hand count of five sampled tests. A false flag in either fails the tool.
- The install test shows the tool installs with its module.
- `python bootstrap/scaffold.py --dry-run` shows the install line.
- Boundary B is `wide`, because protected and trust-ceremony surfaces are
  touched.

### Examples / smoke checks

`python scripts/check_cairn.py` for prose, then the release certifying pair
after the re-anchor.

#### Security preflight — five questions, answered in writing

- **S1 — Who supplied it?**
  - **Promise lists and the removal set:** the implementer.
  - **Mutants, probes and their record:** a fresh agent. For security
    families it also works from the code's own defensive checks.
  - **The removal set for security and high-risk families:** a fresh
    high-tier Security Review.
  - **Hold dispositions:** the Maintainer, by promise group.
- **S2 — Can it fail?** The behavior-mutant check fails if a removed test was
  the only guard of a promise. Its mutants come from the promise list, not the
  removed tests.
- **S3 — What fires it, over what?** `_gate_manifest.py verify` runs over every
  collected node. The re-anchor accepts the losses group by group.
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

Nothing opened has been dropped. The narrower protection named in the
Decision summary is the proposal's intended effect, not a scope loss. It takes
effect only with the Maintainer's allowance.

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

## Response -- Claude Opus 5.5 (author) -- 2026-11-08

**Elapsed**: about 10 minutes. **Tokens**: unknown.

- **Finding 1, accepted.** The Decision summary now says plainly that tests
  catching only internal mutants are given up. It also says this reverses the
  suite-consolidation rule and needs the Maintainer's allowance. Scope delta
  stays `preserved`: nothing opened was dropped. A note there points to the
  narrowed protection as the intended effect.
- **Finding 2, accepted.** Outcome 2 now specifies the mutant check:
  - a fresh agent writes the mutants from the promise list and code, without
    the tests;
  - at least one behavior mutant per promise, plus an "accepts" mutant per
    refusal;
  - each mutant runs against the old file, taken at the commit before the
    first removal, and against the new file;
  - the pilot fails on any mutant the old file caught and the new one missed.
  `test_upgrade_removes_retired_files.py` is out of the pilot and in
  Outcome 3.
- **Finding 3, accepted.** Outcome 3 now says how removals behave before the
  re-anchor:
  - ordinary removals are notes; protected removals are `COLLECTION-DROPPED`
    holds until the re-anchor;
  - `verify` runs only in `scripts/repin.py` and `bootstrap/security_check.py`,
    so the holds don't block ordinary commits;
  - the plan hands over the full list of removed nodes;
  - families not done in time wait for the next re-anchor.
- **Foundations 2, adopted.** Outcome 3 now starts only after the pilot passes
  its check and the result is recorded.

### Withdrawn / superseded commitments

None.

## Scope widened -- Maintainer chat -- 2026-11-08

> "Okay. Let's make two separate proposals. A text pin one and a functional
> promise testing one. Both proposals should also build the shipped Cairn
> capabilities to help improve testing in adopters."

Outcome 4 moved from "kept for later" into scope. It now names shipped
guidance, a plan-template prompt and `tools/test_coupling.py`, sequenced after
the pilot. Text pins moved to their own proposal. Status returns to
`awaiting-review` for the second pass that widened scope allows; the Security
Review follows that pass.

## Review -- Claude Sonnet 5.5 (Reviewer, widened scope) -- 2026-11-08

**Reviewed commit**: `e8790690e0237194e3b6b12c89bbb5f2ccccd2d2`
**Tier**: usual
**Findings**: raised
**Verdict**: REVISE
**Elapsed**: approximately 8 minutes
**Tokens**: unknown

**Foundations**

1. **Should this happen as framed?** Yes in aim, but the rule and the tool are specified too loosely for a plan, and the new section overlaps existing guidance (findings 1-3). -- `testing-discipline.md` already says "Test promises, not wording or internals" and "Consolidate without losing detection".
2. **Best alternative.** Ship the rule, plan prompt and module section after the pilot; defer `test_coupling.py` until reports are shown to change behavior. Doing nothing leaves adopters on the "add a test per change" default. -- Outcome 4 is sequenced after the pilot already.
3. **What would show it wrong.** Run the tool on `examples/scientific-minimal`; if it flags nothing real there, or flags test-local helpers, withdraw the tool. -- that example's `test_water_budget.py` is already promise-shaped.

**Finding 1 -- Not blocking: edit, don't add.** The new section duplicates two existing paragraphs, and "folding or deleting change tests" can read as conflicting with "Consolidate without losing detection". Say it replaces the "Test promises" paragraph and what retained-check mapping adopters still owe. The worked example needs a pin-test starting point; the example project has none. Closes when the proposal names the replaced paragraph and the example's source.

**Finding 2 -- Not blocking: specify the tool.** Undefined: "module of the project" (suggest: names imported from files inside the repo, resolved by `ast`), "promise list" (suggest: a docstring line `Promises:` followed by bullets), and false positives (underscore names defined in the test file, dunder names, conftest). The install path is wrong: modules ship scripts to `scripts/` (`config.py` ~1222, `link_check.py`); `tools/` is Cairn's own. Name the source under `templates/modules/team-gated/`, the verbatim install, and the capability-table row (~line 1516). Closes when written.

**Finding 3 -- Not blocking: the gate basis is weak.** The rate-limit gate (`rationale.md` 466-478) allows recurrence, or synthesis by the session-close routine owner. A weight review is not that routine, and one pilot is not recurrence. Cite the recurring measured pattern (about 12 tests added per 1 removed) as recurrence, or ask the Maintainer to classify it. Direction by chat is not a gate waiver.

**Not an issue:** stdlib-only holds (`ast`); advisory exit 0 fits the tools-advisory rule.

**Coverage:** Not covered: Security Review, install-manifest hashes, whether the pilot bar suits adopters. No tests run. About 400 words, over target because the tool needed specifying.

## Response -- Claude Opus 5.5 (author, widened scope) -- 2026-11-08

**Elapsed**: about 15 minutes. **Tokens**: unknown.

- **Finding 1, accepted.** Outcome 4 now extends the existing "Test promises,
  not wording or internals" paragraph rather than adding a section. It makes
  "Consolidate without losing detection" concrete through the
  behavior-mutant check. The pin-wording sentence goes to the
  functional-prose proposal. The worked example now has a written "before"
  and uses the existing test file as the "after".
- **Finding 2, accepted.** The tool now:
  - installs as `scripts/test_coupling.py` from a team-gated source, with
    an `InstallSpec` and a capability row;
  - defines a project module, private reach, the exclusions and the
    promise-list format.
- **Finding 3, accepted in part.** The gate basis is now recurrence, citing
  the suite-consolidation plan and the weight review, with high-risk
  classification as the Maintainer's alternative. Both are left to the
  Decision.
- **Foundations 2 (defer the tool), declined.** The Maintainer asked for
  shipped capabilities in this proposal. Your forward test is adopted
  instead, as a required check that can fail the tool.

### Withdrawn / superseded commitments

- **The install path** `tools/test_coupling.py` is replaced by
  `scripts/test_coupling.py` (finding 2).
- **The separate testing-module section** is replaced by an extension of the
  existing paragraph (finding 1).

## Review -- Claude Opus 5.5 (Security Review) -- 2026-11-08

```
Reviewed commit: 69704865b8174722100cd3675707a1b12e91b8f0
```

**Tier**: Security Review
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: about 25 minutes
**Tokens**: about 70,000 (estimated)

**Foundations**

1. **Should this happen as framed?** Yes for ordinary code, but not yet for security tests: the only check independent of the removal author is the mutant check, and its input is that author's promise list (findings 1-3). -- Outcome 2 check, step 1; S1.
2. **Best alternative.** Run the pilot and removal pass as framed, but keep security-relevant tests by default and remove them node by node only where the removal-set Security Review agrees. That loses some shrinkage in the largest member, `test_gate_preflight.py` (268 tests). -- `security_manifest.py` `SECURITY_FAMILY`.
3. **What would show it wrong.** Delete the descriptor recheck in `_write_by_replacing` (one mutant). If the promise-list mutants never touch that site and the new file misses it, refusals can leave silently. -- `test_security_leaf.py::TestWriteByReplacing::test_swapped_temp_cannot_change_victim_mode`.

**Finding 1 -- Not blocking: mutants must not depend on the promise list for defensive code.** The test above calls private `S._write_by_replacing` and injects a link swap through a patched `os.fchmod`. No benign caller sees that fault, so the rule calls it internal and the tool counts it as private reach. Closes when: (a) for security-relevant files, the fresh agent also writes one "accept" mutant per defensive site it finds in the code (refusal raise, link or `lstat` check, recheck after open, fail-closed parse branch); (b) that agent runs and records the old-versus-new probes; (c) the rule says a fault seen only under hostile input or timing is caller-visible.

**Finding 2 -- Not blocking: name the node-level policy.** `NATIVE_ONLY_NODE_IDS` lists 623 nodes. Its hash and its 20/603 counts are pinned (`validated_native_only_nodes`). `security_check.py` (~line 578) refuses when a listed node is missing. That fails closed, which is good, but each such removal edits a hash-pinned list. Closes when Outcome 3 names it, and when the Security Review must agree per node for manifest members and listed nodes.

**Finding 3 -- Not blocking: unprotected security files have no hold.** `bootstrap/tests/security/` holds four ordinary files (101 tests). One is `test_git_interpreter_binding_portable.py`, which guards a named high-risk surface. Removals there are only `COLLECTION-ORDINARY-DROPPED` notes. Closes when any file guarding a named high-risk surface waits for the Security Review and appears on the hand-over list.

**Finding 4 -- Not blocking: the per-row disposition does not scale.** `REANCHOR_RUNBOOK.md` line 110 asks for a reason on every HOLD row. With hundreds of rows, "one by one" is only nominal. Closes when the list groups nodes by promise, each with its retained check and mutant result, and a node without both is `stop`.

**Finding 5 -- Not blocking: tool path handling.** `ast.parse` runs nothing. But `importlib.util.find_spec("a.b")` imports `a`. Closes with contract tests for: no import machinery; resolved targets kept inside the root (a link out of the root is reported, not followed); printed names encoded; `RecursionError` and decode failures reported as unparsable.

**Finding 6 -- Not blocking: shipped wording.** "Never add a test that pins the line", plus a worst-first report, could steer adopters to delete race-injection tests. Closes when the module says refusal tests are promises and seam-injected hostile tests are declared exceptions.

**Coverage:** read the proposal, `_gate_manifest.py` 826-870, `security_manifest.py`, the roster, the runbook and two security test files. Not covered: other families' defensive-site counts, adopter install hashes. No tests run. About 560 words: over target because four security questions were owed.

## Response -- Claude Opus 5.5 (author, Security Review) -- 2026-11-08

**Elapsed**: about 10 minutes. **Tokens**: unknown.

- **F1, accepted.** Outcome 1 now says hostile input or timing is
  caller-visible: a race or a swapped link breaks a refusal promise. Tests
  that inject such state are declared exceptions that stay. For security
  families, the mutant agent also writes an "accepts" mutant for each
  defensive check it finds in the code, and it runs and records the probes.
- **F2, accepted.** Outcome 3 names `NATIVE_ONLY_NODE_IDS`. A listed node
  goes only with the family Security Review's node-by-node agreement, and the
  pinned hash and counts change under the re-anchor.
- **F3, accepted.** Any file guarding a security property or a high-risk
  surface counts as protected for this proposal, held or not. Its removals
  wait for that review and appear on the Maintainer's list.
- **F4, accepted.** The re-anchor list is grouped by promise, with the
  retained check and mutant results for each group. A node lacking either is
  marked `stop`.
- **F5, accepted.** Contract tests now cover:
  - no import machinery;
  - resolved paths kept inside the root, with links out reported;
  - escaped names;
  - `RecursionError` and decode failures reported as unparsable.
- **F6, accepted.** The testing module and the tool's report both say refusal
  tests are promises and injection tests stay.
- **"The removal set review was never scheduled," accepted.** It is now a
  Security Review per security or high-risk family, before its removals land.
  The Decision summary's cost line says so.

### Withdrawn / superseded commitments

- **"One Security Review of the removal set"** becomes one per security or
  high-risk family (the finding about scheduling).
- **"Accepts the losses one by one"** becomes group by group (F4).

## Decision -- Maintainer -- 2026-11-08

Scribed by Claude Opus 5.5 (`claude-opus-5-5`) on the Maintainer's explicit
instruction in chat, 2026-11-08.

**Elapsed**: under 1 minute to scribe. **Tokens**: unknown.

**Tier**: heavy

**ACCEPTED.** The Maintainer's authorization, verbatim:

> "Accept both. Heavy tier. Add to v0.7. I will have the agent working on that in Codex take it from here."

The same chat recorded the merit basis ("I think we should go forward with
this on the basis that it is a good idea, not on recurrence"), quoted in
Documentation / doctrine surface.

## Decision amendment -- Maintainer -- 2026-11-08

Scribed by Claude Opus 5.5 (`claude-opus-5-5`) on the Maintainer's explicit
instruction in chat, 2026-11-08. **Elapsed**: under 1 minute to scribe.
**Tokens**: unknown.

Context: the Maintainer asked whether `AGENTS.md` is the right home for these
rules ("AGENTS is getting bloated") and suggested the testing-discipline
module and the plan template instead. The Strategy agent recommended moving
the testing rule out and keeping the editing rule to one sentence, and asked
for the Maintainer's words. This amends where the two proposals place their
rules; it does not change their outcomes or tier. It applies to both this
proposal and its companion.

The Maintainer's authorization, verbatim:

> "Move the testing rule out of AGENTS.md into the templates and testing module; keep the editing rule to one sentence"
