# Test once per change: scoped iteration, narrow review, one run last

**Author**: Claude Opus 5.5 (Strategy)
**Status**: accepted
**Review**: usual
**Proposed tier**: light
**Plan review**: not required(no plan: light tier)
**Opened**: 2026-10-30
**In brief**: Run a change's integration tests once, after code review, and limit every run to the tests that name the changed files, so plans stop re-running checks on unchanged code.

## Context

Issue [#41](https://github.com/MSUHydrogeology/cairn/issues/41): one adopter
plan ran its tests about six times, 5 to 6.6 minutes each. The Maintainer
asked for this change (chat, 2026-10-30):

> "1) Only iterate on tests of the files touched
> 2) When reviewing, only the tightest possible scope
> 3) Only one, narrowly-scoped integration suite after code review. Very
> little reason to run a full code suite."

Cairn's rules force the repeat and contradict each other. `AGENTS.md:196-197`
runs Boundary B "before code review" and `AGENTS.md:215` says "Changed
implementation invalidates the record", so a review fix forces a second run.
`dev/plans/_template.md:308` says Boundary B "runs once after the final
implementation commit", yet its Boundary C (`:362`) verifies that record.

Scope also leaks: iteration searches for "owning tests and readers"
(`AGENTS.md:191`), and 64 test files read templates in general. The
certifying run took 24 minutes 55 seconds against its 10-minute budget.

## Proposal

**1. Iteration (A): the tests that name a changed file.** A test names a
file when it imports it or cites its path or file name. Run those, plus the
standing prose gates for prose. `python tools/test_tiers.py for <paths>`
lists them, and the list is not widened by judgment. For most changes it is
a few files.
For governing text, pass the complete reviewed commit range with
`--range BASE..HEAD`. Narrow readers to tests pinning changed passages only
when the broad reader list exceeds 40, and report every omitted reader.
Folder sweepers are caught at the release run.

**2. Review (C): the tightest scope.** The reviewer reads the change and the
author's iteration evidence, then runs targeted checks that try to break it.
Never a suite. Where a check is missing, the reviewer names the specific test
to add; the author adds it.

**3. Integration (B): once, last.** After the final change, including review
fixes, run on a clean commit: the iteration list for every file changed in
the range, plus the integration and workflow tests (by the tier map) that
name those files. It records the mode and `Implementation verified at <SHA>`
as now. Because it runs last, a review fix invalidates nothing; the clause
saying it does is deleted. The record is read at archive, which requires a
passing record. A fix made after a failed run that changes more than the
failing test goes back to the same reviewer for a targeted look. A wider run is owed only when no valid record
exists, a cross-surface dependency surfaces, a skip, xfail or xpass is
undisposed, a trust ceremony prescribes one, or there is a concrete reason
to distrust the evidence (as #41 lists). `WIDER RUN REQUIRED` becomes the
reviewer naming one of those reasons.

**4. The full suite: rarely.** A certifying run is made before a release
cut, before a re-anchor ceremony, before a push when the Maintainer requires
one, and when the Maintainer asks; never per change. A break between distant parts
of the code is then found at the release run and bisected over the range
since the last good run.

**5. Unchanged:** trust-ceremony checks, the `CAIRN_FULL_SUITE=1` rule and
the broad-run guard.

**6. Open plans may switch** by one line in their record.

**7. Timing targets for the suite, not scores for agents.** Cairn's timing log
of 188 suite runs sets these targets: iteration run 30 seconds; any one test
file 10 seconds; integration run 3 minutes; certifying run 10 minutes, its
existing budget. In the widest logged run (70 files, 710 seconds), the median
file took 2.0 seconds and the 20 files over 10 seconds took 89% of the time. A
missed target never blocks a change: the record notes it, and a file over 10
seconds joins the consolidation list, slowest first.

No new files: `for` is a subcommand of the existing `tools/test_tiers.py`.

## Rationale

One run on the final code replaces two or more; a tool-made starting list
stops caution from widening every run. A late cross-surface break costs a
bisect and a revert; the present rules cost minutes on every plan.

## Alternatives considered

Boundary B before review: two runs per plan, as #41 measured. A parallel
runner still re-runs unchanged checks. Issue #41 alone keeps the "readers"
search that widens scope.

## Documentation / doctrine surface

`AGENTS.md` and `templates/core/AGENTS.md` (verification section, including
`AGENTS.md:185`); `dev/plans/_template.md` and its shipped copy (Boundary
A, B and C); `doctrine/plans.md:316`, `:326` and `:348`;
`doctrine/dual-review.md` where it describes Boundary C;
`tools/test_tiers.py` (`for`). Edits replace wording in place and add none
net to `AGENTS.md`. The doctrine edits clear the rate-limit gate
(`doctrine/rationale.md:458`) by recurrence: issue #41, the Maintainer's
request, and Cairn's own contradiction. The two pinned tests are frozen in
the gate manifest, so editing them owes a re-anchor, batched with the
forward-baseline ceremony already on the board.

## Evidence / verification plan

### Tests required

`bootstrap/tests/test_test_tiers.py`: `for` lists a test that imports a
module and one that cites a template path, and omits a folder sweeper.
`bootstrap/tests/test_verification_boundaries.py` and
`test_review_and_verification_rules_ship.py` pin the old phrases; update
them to pin the new rules.

### Examples / smoke checks

Implement this change under its own rules: one iteration run, one
Boundary B run.

#### Security preflight

N/A: no trust boundary added, moved, or widened; trust-ceremony checks and
the broad-run guard are unchanged.

### Independent scientific check

N/A: no scientific assumption or result touched.

## Signals the change is wrong

Release runs keep finding breaks a per-change run would have caught; a
reviewer misses a defect an earlier run would have shown; timing targets
stay missed for a release.

## Scope delta

**Scope delta**: preserved.

## Assurance path

**Assurance path**: high-assurance — governing doctrine and lifecycle
verification rules.

## Review -- Claude Sonnet 5.5 -- 2026-10-30

```
Reviewed commit: 1b28f6bbb48240da05bde3d1ccdf40e7e3e04b66
Target: whole proposal
Prior findings: none
Assurance path: high-assurance
```

**Tier**: usual
**Findings**: raised
**Verdict**: REVISE

**Elapsed**: unknown
**Tokens**: unknown

**Foundations**:

1. **Should this happen as framed?** Yes, with repairs. The cited rules are accurate (`AGENTS.md:191,197,215`, `dev/plans/_template.md:308,362`, `doctrine/plans.md:316,348`, and the pinned phrases in the two tests). Light tier with no plan fits `dev/proposals/_template.md:462`.
2. **Best alternative.** Reorder Boundary B only (issue #41) and let `for` print an advisory starting list, not a rule -- `tools/test_tiers.py` has no `for` today.
3. **What would show it wrong.** The scope rule pulling in most of the suite for this very change (finding 1).

**Findings (all non-blocking)**

1. The scope rule is not tight. `grep -l "AGENTS.md"` over `bootstrap/tests` matches 50 of 132 test files; `_template.md` matches 18. This change edits `AGENTS.md`, so it pulls about 50. It also misses sweepers: `test_cairn_prefix_links.py` globs `templates/**/*.md` and names neither file. Satisfier: state the expected list size for this change, name the gate that covers sweepers, and let the author extend the list, recording omissions.
2. With B after review, no reviewer reads the final record (`dev/plans/_template.md:362`), and a fix made after a failed B is unreviewed. Satisfier: say who reads it and that a non-trivial post-B fix returns to review.
3. Item 4 says "not per push", but `AGENTS.md:185` and `doctrine/plans.md:326,333` keep a push rule; the latter are not on the surface list. Satisfier: keep "when the Maintainer requires" and list them.
4. Missing: the doctrine rate-limit gate (`doctrine/rationale.md:466`) for `doctrine/` edits, and the re-anchor owed for frozen test edits (`_gate_manifest.py:12-16`). Satisfier: name the gate path and queue the row.

**Coverage**: did not run `for` (absent), the tests, or the fidelity manifest; grep counts are file-level, not per-edit.

## Response -- Claude Opus 5.5 -- 2026-10-30

Answers the usual review at `d3adc1bf` (REVISE, four non-blocking). The
operative sections are revised in place; the review is unchanged. Status
moves to `awaiting-decision`.

- **1, accept.** `for` gives a starting list the author may extend with a
  reason. Most lists are a few files; governing text is the stated
  exception (`AGENTS.md` is cited by 50 of 132 files), narrowed to the tests
  that pin the changed passages with the rest recorded as an omission.
  Folder-sweeping tests are caught at the release run.
- **2, accept.** The record is read at archive, which requires a passing
  record. A fix after a failed run that changes more than the failing test
  returns to the same reviewer for a targeted look.
- **3, accept.** The full suite also runs before a push when the Maintainer
  requires one; `AGENTS.md:185` and `doctrine/plans.md:326` join the
  surface list.
- **4, accept.** The rate-limit gate is cleared by recurrence (#41, the
  Maintainer's request, Cairn's own contradiction). The two pinned test
  files are frozen, so their edit owes a re-anchor, batched with the
  forward-baseline ceremony.

### Withdrawn / superseded commitments

- "The list comes from the tool, not from judgment": replaced by a tool-made
  starting list the author may extend with a reason.
- "Not per change or per push": the push case is restored.

## Response addendum -- Claude Opus 5.5 -- 2026-10-30

Two further in-place revisions at the Maintainer's request (chat,
2026-10-30: "Please do"), after "There needs to be targets for timing
too, right?":

- **Item 1 returns to tool-only.** The `for` list is no longer extended by
  judgment; anything it misses is caught at the release run.
- **Item 7 added:** timing targets for the suite (iteration 30 seconds, any
  test file 10 seconds, the integration run 3 minutes, the certifying run 10
  minutes), read from the existing timing log; a miss never blocks a change.

### Withdrawn / superseded commitments

- "A starting list the author may extend with a reason": withdrawn.

## Decision -- Maintainer -- 2026-10-30

**Elapsed**: unknown. **Tokens**: unknown.

**Tier**: light

The proposal's own tier stands; the Maintainer's words do not change it.

**ACCEPTED.** The Maintainer's authorization, quoted **verbatim and visually
isolated** (chat, 2026-10-30; scribed by Claude Opus 5.5):

> "Accept as revised. Please scribe this"

The accepted text is the operative sections as revised at `cd8aa3ee`.

## Maintainer authorization -- 2026-10-30

**Source**: Maintainer chat, 2026-10-30. The Maintainer explicitly resolved
the tier conflict and waived the additional Security Review for this accepted
implementation. The gate baseline update remains batched with the v0.6 cut.

> "Keep light; waive the extra Security Review"

Recorded by the implementation author in the commit carrying this authorization.

## Code review -- Codex GPT-6.1 Terra -- 2026-10-30

**Reviewed commit**: `d2ab8d87`. **Tier**: usual. **Verdict**: REVISE.
**Elapsed**: unknown. **Tokens**: unknown.

**Foundations**:

1. **Should this happen as framed?** Yes, after the selector meets the accepted scope: the proposal requires passage narrowing only above the runner limit and reporting omissions.
2. **Best alternative.** Retain the existing tier map and make the changed range explicit to the selector; this preserves the accepted one-run sequence.
3. **What would show it wrong?** A committed range spanning a review fix selects all tests pinning the earlier governing-text changes and reports every excluded reader.

**Blocking findings**:

1. `tools/test_tiers.py:112-130` uses the working diff or only `HEAD^..HEAD`, not the reviewed range. At a clean later commit, an earlier AGENTS change is lost; with no passages it falls back to every AGENTS reader. Today `for AGENTS.md` selects 47 files, above the 40-file guard, after the unrelated commit `11491b5e`. Add a targeted test covering a governing change followed by an unrelated or review-fix commit and select from the full reviewed range.
2. `tools/test_tiers.py:137-153` narrows whenever passages exist, regardless of broad-list size, and does not report omitted readers. This misses the accepted conditional and omission record. Add a targeted test for lists below and above the guard, including omitted-reader reporting.

**Coverage**: inspected the committed selector, accepted proposal, plan verification text and selector tests; ran the selector and counted direct AGENTS references. Did not run a suite, inspect every changed prose surface, or perform Security Review. Boundary B remains pending after fixes and review.

**Author response -- fix commit `61e0353d`**: Both blocking findings were
addressed. The selector now requires and consumes the complete reviewed commit
range for `AGENTS.md`, retains matching tests when the range is followed by an
unrelated commit, narrows only above 40 broad readers, and reports every
omitted reader. Regression coverage checks below and above the guard and CLI
omission output. Focused Python 3.13.5 checks passed: 152 tests in 0.39s.

## Implementation verification -- Codex GPT-6 Sol -- 2026-10-30

**Boundary B mode**: wide. **Certified by**: pending.
**Tested SHA**: `61e0353d171130cad2ea927bf63f5a14bd608488`.
**Reviewed range**: `f7245a8271b7784316601284cee62a4d26fe17c6..61e0353d171130cad2ea927bf63f5a14bd608488` (test-once implementation `d2ab8d87` and selector fix `61e0353d`; the range also contains unrelated committed work).
**Interpreter**: Python 3.13.5 at `/Users/kendal30/conda_envs/general/bin/python3.13`.
**Tree**: separate checkout; clean before and after (`git status --porcelain` empty).

**Surfaces**: governing instructions and shipped copy, plan template and shipped copy, planning and review doctrine, selector, selector tests, verification-boundary tests, and shipped-rule tests. Mapped tests: `test_incident_trackers_module.py`, `test_install_module.py`, `test_onboarding_seed_roster.py`, `test_presets.py`, `test_replacement_tools.py`, `test_review_and_verification_rules_ship.py`, `test_scientific_check_guidance_ships.py`, `test_session_routines.py`, `test_status_vocabulary_advisory.py`, `test_test_tiers.py`, and `test_verification_boundaries.py`.

**Commands and outcomes**:

- `python3.13 tools/test_tiers.py for --range d2ab8d87^..61e0353d <changed paths>` -- 11 test files selected; 44 broad `AGENTS.md` readers reported omitted because the list exceeded 40.
- `python3.13 -m pytest -q <the 11 mapped files>` -- 323 passed in 6.64s.
- `python scripts/quality_gate.py --sub neutrality` -- fail=0, info=43.
- `python scripts/quality_gate.py --sub redundancy` -- fail=0, info=1.
- `python scripts/link_check.py <proposal> <plan template> <planning doctrine>` -- 3 Markdown files, no issues; 1 external link not probed.
- `claim_check` -- plan template and planning doctrine passed. Proposal reports 3 historical citation flags in its immutable review record (`:165` and `:173`); no new claim-check flags were introduced by this change.

**Elapsed**: pytest 6.64s; standing gates and prose checks about 1.5s. **Tokens**: unknown. No full suite, Security Review, or re-anchor was run. The earlier 1,325-test Python 3.12.9 run predates this selector fix and is not counted as Boundary B evidence.
