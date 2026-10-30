# Test once per change: scoped iteration, narrow review, one run last

**Author**: Claude Opus 5.5 (Strategy)
**Status**: awaiting-review
**Review**: usual
**Proposed tier**: light
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-10-30
**In brief**: Run a change's integration tests once, after code review, and limit every run to the tests that name the changed files, so plans stop re-running checks on unchanged code.

## Context

Issue [#41](https://github.com/MSUHydrogeology/cairn/issues/41) reports one
adopter plan that ran its directory test set about six times, at 5 to 6.6
minutes each, mostly confirming unchanged code. The Maintainer's verdict
there: "We cannot be testing more than once per plan." The Maintainer asked
for this change in chat (2026-10-30):

> "1) Only iterate on tests of the files touched
> 2) When reviewing, only the tightest possible scope
> 3) Only one, narrowly-scoped integration suite after code review. Very
> little reason to run a full code suite."

Cairn's own rules force the repeat and contradict each other:

- `AGENTS.md:196-197` runs Boundary B "after the final implementation commit
  and before code review", and `AGENTS.md:215` says "Changed implementation
  invalidates the record", so any review fix forces a second run.
- `dev/plans/_template.md:308` already says Boundary B "runs once after the
  final implementation commit", but its Boundary C (`:362`) has the reviewer
  verify the Boundary B record, which must therefore exist before review.

Scope also leaks. Iteration searches for "owning tests and readers"
(`AGENTS.md:191`). Measured 2026-10-30, 64 test files read templates in
general, so one template edit can pull in half the suite. The certifying run
took 24 minutes 55 seconds against a 10-minute budget (`dev/PLANNING.md`,
"Faster certifying runs").

## Proposal

**1. Iteration (A): the tests that name a changed file.** A test names a
file when it imports it or cites its path or file name. Run those, plus the
standing prose gates for prose. A tool lists them:
`python tools/test_tiers.py for <paths>`. The list comes from the tool, not
from judgment, and a reader that only sweeps a whole folder is not included.

**2. Review (C): the tightest scope.** The reviewer reads the change and the
author's iteration evidence, then runs targeted checks that try to break it.
Never a suite. Where a check is missing, the reviewer names the specific test
to add; the author adds it.

**3. Integration (B): once, last.** After the final change, including review
fixes, run on a clean commit: the iteration list for every file changed in
the range, plus the integration and workflow tests (by the tier map) that
name those files. It records the mode and `Implementation verified at <SHA>`
as now. Because it runs last, a review fix invalidates nothing; the clause
saying it does is deleted. A wider run is owed only when no valid record
exists, a cross-surface dependency surfaces, a skip, xfail or xpass is
undisposed, a trust ceremony prescribes one, or there is a concrete reason
to distrust the evidence (as #41 lists). `WIDER RUN REQUIRED` becomes the
reviewer naming one of those reasons.

**4. The full suite: releases and re-anchors only.** A certifying run is
made before a release cut, before a re-anchor ceremony, and when the
Maintainer asks; not per change or per push. A break between distant parts
of the code is then found at the release run and bisected over the range
since the last good run.

**5. Unchanged:** trust ceremonies keep every prescribed check; nobody sets
`CAIRN_FULL_SUITE=1` outside a certifying run; the broad-run guard stays.

**6. Open plans may switch.** An already-open plan keeps its written
contract unless its author records one line adopting this one.

No new files: `for` is a subcommand of the existing `tools/test_tiers.py`.

## Rationale

One run on the final code replaces two or more. Mechanical scope stops
caution from widening every run. Most changes are one revert away, so a late
cross-surface break costs a bisect, while the present rules cost minutes on
every plan.

## Alternatives considered

Keep Boundary B before review: two runs per plan, as #41 measured. A parallel
runner: faster, but still re-runs unchanged checks and adds a dev-only
dependency. Issue #41 as written: fixes the order but keeps the "readers"
search that widens scope.

## Documentation / doctrine surface

`AGENTS.md` and `templates/core/AGENTS.md` (verification section);
`dev/plans/_template.md` and `templates/core/dev/plans/_template.md`
(Boundary A, B and C); `doctrine/plans.md:316` and `:348`;
`doctrine/dual-review.md` where it describes Boundary C;
`tools/test_tiers.py` (`for`). Edits replace wording in place and add none
net to `AGENTS.md`.

## Evidence / verification plan

### Tests required

`bootstrap/tests/test_test_tiers.py`: `for` lists a test that imports a
module and one that cites a template path, and omits one that only sweeps
all templates. `bootstrap/tests/test_verification_boundaries.py` and
`test_review_and_verification_rules_ship.py` pin the old phrases ("before
code review", "invalidates the record", "owning tests and readers"); update
them to pin the new rules: B once after review, naming as the scope, full
suite at release and re-anchor.

### Examples / smoke checks

Implement this change under its own rules and record the runs: one
iteration list, one Boundary B run. `claim_check`, `link_check` and the
neutrality gate.

#### Security preflight

N/A: no trust boundary added, moved, or widened; trust-ceremony checks and
the broad-run guard are unchanged.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Release runs keep finding breaks that a per-change run would have caught;
a reviewer misses a defect an earlier run would have shown; authors widen
"names" to sweep many files.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — governing doctrine and lifecycle
verification rules.
