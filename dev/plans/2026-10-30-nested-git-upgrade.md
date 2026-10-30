# Plan: Protect nested Git data during upgrades

**Source proposal**: dev/proposals/archive/2026-10-29-codex-nested-git-upgrade.md
**Status**: awaiting-code-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Refuse upgrade paths that name nested Git data or resolve into it, while preserving ordinary project links.

## Source proposal

The Maintainer accepted the revised proposal to protect nested Git data from upgrade reads and writes through supplied names and stable symlink targets, with explicit compatibility and security limits.

## Scope

Change `bootstrap/_scaffold/upgrade.py`, its upgrade tests and `bootstrap/UPGRADE.md`. No doctrine surface; the documentation describes existing behavior after the change. The existing Maintainer-run AST re-anchor is required separately and is not authorized here.

**Reuse.** Searching `bootstrap/_scaffold/upgrade.py` for `_contained_lockfile_path` found the common lockfile and staged-name guard; extend its existing shape and containment checks. It validates project `dst` and `base_cache`, source `src`, and six stage metadata collections. Reuse its resolved target relative to the resolved project root and return the unresolved joined path. Search callers and readers again during implementation and extend the map if needed.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Enforce and test the project-name and resolved-target boundary | Both plan reviews | Guard and public-command tests |
| C2 | Document recovery and verify the complete change | C1 | Guidance, mutation and stable verification evidence; handoff for independent code and Security reviews |

## Acceptance criteria

### C1

Before project reads or writes, refuse any supplied or resolved project-relative component equal to `.git` after case folding and stripping trailing ASCII dots and spaces, for lockfile `dst`, `base_cache`, and all staged-name collections. Keep containment, missing-target behavior, escaped diagnostics and stricter write-link refusals. Do not inspect ancestors outside the resolved project root or change source-tree handling. Public-command tests cover nested names, case and trailing variants, stable contained aliases for both fields, stage metadata, protected bytes, lockfile and stage state; preserve `.gitignore`, `.github`, `.git-notes.md` and ordinary contained read links. Test recovery by correcting or removing records or discarding the untrusted stage and creating a fresh one, without removing Git data.

### C2

Guidance explains the boundary, conservative POSIX compatibility cost, recovery, and limits: hard links under other names and races after checks are not protected. Exercise public upgrade plan, stage and apply in scratch projects. In separate copies, remove supplied-name filtering, resolved-target filtering, case folding, and trailing-character normalization; a relevant test fails for each mutant and unmutated controls pass. Record outcomes. S2 is exercised here and S3 is the public commands and gates below. Wide Boundary B and independent code and Security reviews precede archive; the AST ceremony remains Maintainer-run.

## Scope delta

**Scope delta**: preserved.

## Verification

Boundary A: under canonical Python 3.13, run `python -m pytest bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_upgrade.py bootstrap/tests/test_upgrade_side_door_parity.py` for guard, lockfile reads, source behavior and public upgrade paths; run `python -m pytest bootstrap/tests/test_upgrade_refuses_hostile_project_data.py bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_lockfile_provenance.py` for staged-name consumers, additions and lockfile metadata. Include new tests in owning files, search for other guard callers and consumers, and extend the map if needed. Split selections within the broad-run guard's file limit and reconcile the executed union without an override. Run `python -m pytest bootstrap/tests/test_security_lint.py` for the engine security gate; a skip is unmet.

Exercise `python bootstrap/scaffold.py upgrade` with `--plan`, `--stage` and `--apply` in scratch installations, including refusal and recovery; check help for exact arguments. Run `python scripts/claim_check.py` on changed prose, `python scripts/check_cairn.py`, `python scripts/link_check.py`, and `python scripts/quality_gate.py --sub neutrality`; run `python scripts/sync_doc_snippets.py` if synced snippets change. Run four mutations and their unmutated controls in separate scratch copies.

Boundary B is **wide** for the engine contract and security boundary: run the mapped owning families, public paths, mutations and standing gates on a clean, unchanged final implementation commit under the canonical interpreter. Record tested SHA and reviewed range, interpreter, clean pre/post state, commands, outcomes, timing, non-pass dispositions, omissions and **Certified by**: pending. Certification is separate. Boundary C is independent targeted falsification, including both path representations and stated limits; the reviewer records bounding and missing checks. The AST re-anchor follows its existing Maintainer-run ceremony, separately authorized.

## Plan review -- Codex GPT-6 plan reviewer -- 2026-10-30

```
Reviewed commit: fb19301d29bac8fc134a793d688645768aa7ee21
Target: scope, sequence, acceptance criteria and verification
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: none

**Foundations**

1. **Should this happen as framed?** Yes: the plan carries the accepted name and resolved-target boundary, compatibility, recovery and limits into implementation and public-path checks -- `dev/proposals/archive/2026-10-29-codex-nested-git-upgrade.md` (Current contract); this plan, C1 and C2.
2. **Best alternative.** Extend the shared containment guard and use its existing resolution; separate per-command filters would duplicate the boundary without improving the stated race limit -- `bootstrap/_scaffold/upgrade.py:171` and `bootstrap/_scaffold/upgrade.py:3034`.
3. **What would show it wrong.** A public upgrade reading a stable alias to nested Git data, changing protected state on refusal, or rejecting an ordinary contained read link would defeat the planned criteria -- this plan, C1 and C2.

The caller map matches the current guard: lockfile `src`, `dst`, and
`base_cache` are checked centrally, and the staged metadata loop checks names
from four lists and two mappings. The plan preserves the source distinction and
requires another caller search, so newly discovered consumers must enter the
verification map. Resolving relative to the project root avoids rejecting an
external ancestor; returning the unresolved name retains existing write-link
checks. The explicit race and hard-link limits are consistent with the accepted
contract, and scratch public commands plus four focused mutations make the
promised behavior observable without a tree-certifying run.

**Covered:** accepted scope and satisfiers, caller reach, containment and link
behavior, public entry points, compatibility, recovery, verification mapping,
security obligation and separate re-anchor: the cited contract, plan and guard.
**Not covered / low confidence:** no implementation or tests run; actual mutation
effectiveness, platform-specific filesystem behavior and concurrent races remain
unmeasured. This pass does not clear the Internal Security Review obligation.


## Plan review -- Codex GPT-6 Security plan reviewer -- 2026-10-30

```
Reviewed commit: 418098c3eed8945dd0263f03e79fb48ee226ac98
Target: accepted security contract, path boundary and verification
Prior findings: none
Assurance path: high-assurance
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: none

**Foundations**

1. **Should this happen as framed?** Yes: C1 preserves the accepted supplied-name and resolved-target protection, ordinary read-link compatibility and source distinction; C2 preserves the explicit hard-link and race limits -- source proposal, Current contract and Decision; this plan, C1 and C2.
2. **Best alternative.** Extend the existing guard using its contained resolved target; a second resolver or banning all read links adds complexity or loses accepted compatibility -- `bootstrap/_scaffold/upgrade.py:171`, `bootstrap/_scaffold/upgrade.py:228`.
3. **What would show it wrong.** A stable contained alias reaching Git data, refusal changing protected state, or a normal contained read link failing would defeat the security boundary or its compatibility promise -- this plan, C1 and C2; `bootstrap/tests/test_upgrade_lockfile_path_containment.py:343`.

The plan separates supplied names from resolved targets instead of assuming
write-link refusal protects reads. Inspection of the current guard and its
readers confirms the distinction: the guard returns the unresolved path,
while destination and cache reads follow links. Checking the resolved path
relative to the resolved project root protects stable aliases without treating
an ancestor outside that root as project data. Preserving the unresolved return
also retains the stricter existing write checks rather than silently granting
write authority through links (`bootstrap/_scaffold/upgrade.py:228`,
`bootstrap/_scaffold/upgrade.py:668`, `bootstrap/_scaffold/upgrade.py:708`).

The accepted limits are meaningful: neither component inspection nor symlink
resolution establishes file identity or prevents later filesystem changes.
C2 requires those hard-link and race limits in guidance; it does not present
them as covered. Normalization conservatively refuses distinct POSIX names,
and C2 carries that compatibility cost. C1 requires escaped diagnostics and
recovery without deleting Git data.

The verification mapping includes both project fields and all six staged-name
collections, public plan/stage/apply paths, protected bytes and metadata on
refusal, and four independently removed protections. The named Bandit test
actually invokes the scanner through its owning module; the plan explicitly
makes its possible missing-tool skip unmet, preserving the gate's meaning
(`bootstrap/tests/test_security_lint.py`). No new security-preflight answer is
needed beyond C2's specified mutation placement and named public commands.

**Covered:** claims, completeness and fail-closed boundary: guard and read sites
above; production paths and mutation design: C1, C2 and Verification; consistency
and drift: accepted Current contract and planned `bootstrap/UPGRADE.md` update;
lifecycle: separate Security obligation and Maintainer-run AST ceremony; scope
and satisfiers: preserved accepted outcomes and falsifiable C1/C2 criteria. No
scientific method changes.
**Not covered / low confidence:** source inspection only; no tests or mutations
run, implementation reviewed, Windows filesystem behavior measured, or hard-link
and race protection established. Actual test effectiveness remains for
implementation evidence and code review.


## Response to plan reviews -- Codex GPT-6.1 Sol -- 2026-10-30

Both the Internal and Internal Security Review passes found no defects. I accept their assessments; the operative plan remains unchanged. Both review obligations are cleared, and implementation may begin.


## Implementation verification -- Codex GPT-6.1 -- 2026-10-30

**Implementation commit**: `f8f96cdb`
**Interpreter**: Python 3.13.13 (`/Users/kendal30/conda_envs/lhm/bin/python3.13`)
**Boundary B mode**: wide, pending
**Certified by**: pending

**Boundary A checks** ran against the implementation bytes before commit. The
shared worktree was not clean: an unrelated proposal was modified, and
`.claude/` and `dev/measurement/collision_log.md` were untracked. The two mapped
test selections collected 456 tests: 454 passed, with these non-passes:

* `test_review_pairs_leave_no_placeholder_the_install_filled` failed because
  the generated review-pair file for the modules README differed outside its
  slots.
* `test_apply_still_applies_a_review_area_of_plain_names` failed because its
  manually planted stage says the notes file was absent at stage time, then the
  test creates it before apply.

These failures do not exercise the nested Git boundary. The targeted boundary
and metadata nodes passed 61/61. The security lint passed 11/11. `claim_check.py`
on `bootstrap/UPGRADE.md`, `check_cairn.py`, `link_check.py` (197 Markdown files),
and `quality_gate.py --sub neutrality` all passed. `git diff --check` passed.

**C2 mutation probes** ran after commit in separate fresh detached worktrees at
`f8f96cdb`, under the same interpreter. Each unmutated control passed, and each
single mutation was killed by its named test:

| Mutation | Control | Mutation result |
|---|---|---|
| Remove supplied-name filtering | `test_the_guard_refuses_a_supplied_git_name_even_when_its_link_target_is_ordinary`: 1 passed | Same test failed to raise: killed |
| Remove resolved-target filtering | `test_the_guard_refuses_a_contained_link_whose_resolved_target_is_git_data`: 1 passed | Same test failed to raise: killed |
| Remove case folding | `test_project_paths_refuse_git_components_after_conservative_normalization`: 7 passed | 3 case variants survived: killed |
| Remove trailing-dot/space normalization | Same normalization test: 7 passed | 4 trailing variants survived: killed |

The temporary worktrees were removed after each probe. Boundary B has not been
run on a clean, unchanged commit; the two mapped non-passes remain unresolved.
The public recovery rehearsal and the four mutants are measured, but C2 and the
implementation remain open pending a clean wide Boundary B record and
independent code and Security reviews. No full suite or certifying run was run.

## Interim code review -- Codex GPT-6.1 -- 2026-10-30

**Reviewed implementation**: `f8f96cdb8afbbc565de7a7bc51f9d5da586ec83d`
**Tier**: Internal
**Findings**: verification remains incomplete; this is not a completed code review.
**Bounding**: WIDER RUN REQUIRED -- the plan's wide Boundary B is pending and its two mapped failures remain unresolved; the author must supply the required clean final-commit evidence before acceptance.

**Foundations**

1. **Does it do what it claims?** The shared guard checks both supplied and resolved project components, while retaining the unresolved return and the source-tree distinction; the targeted checks below did not break those claims -- `bootstrap/_scaffold/upgrade.py`, `_contained_lockfile_path` at the reviewed commit.
2. **Best alternative.** The shared guard is simpler than duplicating the check at each reader, provided the remaining verification establishes the callers and public paths -- this plan's Scope and Verification.
3. **What would show it wrong?** A protected path reaching a read or write, an ordinary contained link being refused, or state changing on refusal would break the contract -- falsification ledger below.

**Falsification ledger** (separate detached worktree at the reviewed commit, Python 3.13.13):

* Ran `python3.13 -m pytest -q bootstrap/tests/test_upgrade_lockfile_path_containment.py bootstrap/tests/test_upgrade_refuses_hostile_project_data.py -k 'git or contained_link or pristine_lockfile or stage_refuses'`: 76 passed, 198 deselected. This challenges supplied and resolved names, stage metadata and ordinary links; it is not the plan's complete verification.
* Independently called the guard with a missing target under a mixed-case, trailing-dot Git component and with a contained alias to a mixed-case trailing-space Git directory: both refused. An ordinary contained link, `.gitignore`, `.github/config`, `.git-notes.md`, a source-tree Git name, and a project under an external `.git` ancestor were accepted. This probe did not exercise the public commands.

**Covered:** shared path guard, supplied and resolved paths, benign names, source distinction and selected stage tests. **Not covered / low confidence:** the complete public-command and stage collection contract, independent mutation of each member, Windows behavior, races and hard links; the author has not supplied complete Boundary B. This interim pass does not clear the separate Security Review obligation or authorize archive.

## Interim Security Review -- Codex GPT-6 Security Reviewer -- 2026-10-30

**Reviewed implementation**: `f8f96cdb8afbbc565de7a7bc51f9d5da586ec83d`
**Obligation**: Security Review
**Tier**: Internal Security Review
**Findings**: C1's public-command test for a stable contained alias through `base_cache` is missing. The existing alias test exercises `dst` only (`bootstrap/tests/test_upgrade_refuses_hostile_project_data.py`, `test_a_contained_alias_into_git_data_is_refused_without_changing_it`). Add the `base_cache` public-path case with protected state checks and include it in the final evidence.
**Bounding**: WIDER RUN REQUIRED -- the prescribed wide Boundary B and the two mapped failures remain open, as does the missing C1 test. This interim pass does not clear the Security Review obligation.

**Foundations**

1. **Does it do what it claims?** The shared guard checks supplied and resolved project components before returning the unresolved name, but the required public cache-alias evidence is missing -- `bootstrap/_scaffold/upgrade.py`, `_contained_lockfile_path`; C1 above.
2. **Best alternative.** Retain the shared guard and add the missing public cache-alias test; duplicating filters at consumers adds separate failure points -- `bootstrap/_scaffold/upgrade.py`, `_check_lockfile_paths`.
3. **What would show it wrong?** A stable alias reaching Git data, or a refusal changing protected state, defeats the boundary -- falsification ledger below.

**Falsification ledger** (detached worktree at the reviewed commit; Python 3.13.13):

* Ran `python3.13 -m pytest -q bootstrap/tests/test_upgrade_refuses_hostile_project_data.py -k 'nested_metadata_paths_into_git_data or contained_alias_into_git_data or review_area_that_names_an_unplain_file or review_area_whose_keys_are_not_plain_names'`: 51 passed, 131 deselected. This challenged staged names, nested metadata values and the public destination alias; it did not cover a public cache alias.
* Inspected the stage metadata name collection and guard calls in `_apply_staged`; the listed nested path values enter the same project guard before use. Inspected the guard's supplied and resolved checks and its unresolved return. No independent filesystem race or hard-link protection was claimed or tested.

**Covered:** staged-name validation, nested metadata values, supplied and resolved guard behavior and destination-alias refusal, with evidence above. **Not covered / low confidence:** public cache alias, complete final verification, Windows behavior, hard links and races. No full suite or historical anchor comparison was run.

## Security Review follow-up -- Codex GPT-6 Security Reviewer -- 2026-10-30

**Reviewed test commit**: `88c93c3770c79930bb24be6db4286e797b42fbce`
**Obligation**: Security Review
**Disposition**: The missing public `base_cache` alias test identified above is addressed. The overall Security Review remains open: the required wide Boundary B and mapped failures have not been resolved.

The new test places a contained link to `.git` in a lockfile `base_cache`, exercises each action in `_ACTIONS`, and checks refusal and preservation of the project snapshot, Git description and stage state (`bootstrap/tests/test_upgrade_lockfile_path_containment.py`, `test_a_contained_base_cache_alias_into_git_data_is_refused_without_changing_it`). In a detached worktree at the reviewed commit, Python 3.13.13 ran that node: 1 passed. Removing the resolved-target check in that copy made the same node fail because the first public action returned success rather than refusing: the mutant was killed. This is targeted evidence for the finding, not final implementation verification; Windows, hard links and races remain untested.

## Sequencing amendment -- Codex GPT-6 -- 2026-10-30

The Maintainer clarified in chat, relayed by the coordinating agent:

> We only repin and reanchor at version cuts or as I ask

> The plan should not require that

Accordingly, earlier statements in this plan that require repinning or
re-anchoring are superseded as plan requirements. Neither ceremony is a
prerequisite for completing or archiving this plan. The new baseline is a
v0.6 board item; repinning and re-anchoring occur at a version cut or when
the Maintainer asks. This amendment does not authorize a ceremony or waive
other checks, reviews, or acceptance criteria. Earlier evidence remains a
record of what was known and done at the time.

## Implementation verification update -- Codex GPT-6 -- 2026-10-30

**Boundary B mode:** wide, incomplete. **Certified by:** pending.
**Candidate:** `22c49ec2bb588d1d237db14f44650caea77f4b33`, a clean detached
clone with Git history, under Python 3.13.13 at
`/Users/kendal30/conda_envs/lhm/bin/python3.13`. The reviewed implementation
range starts at `f8f96cdb`; the plain-name staged-apply fixture was repaired
at `4a76dc54`. `git status --short` was empty before and after the checks.
The shared worktree remained outside the measurement. Elapsed measured command
time was about 103 seconds for the two mapped test groups, security lint and
prose gates; token use is unknown.

* `python3.13 -m pytest -q --tb=short` on
  `bootstrap/tests/test_upgrade.py`,
  `bootstrap/tests/test_upgrade_lockfile_path_containment.py` and
  `bootstrap/tests/test_upgrade_side_door_parity.py`: **219 passed, 6 failed** (49.09 seconds
  wall). The failures are three `TestTemplateGatingSafety` assertions about
  removed template headings/conditionals, two `TestInitLock` review-copy
  assertions (generated module inventory and profile sizing), and
  `test_a_hand_built_review_area_cannot_make_apply_record_a_path_outside_the_project`,
  whose planted stage lacks the later required directory observations. These
  are unresolved mapped checks, regardless of their separate causes.
* `python3.13 -m pytest -q --tb=short` on
  `bootstrap/tests/test_upgrade_refuses_hostile_project_data.py`,
  `bootstrap/tests/test_upgrade_module_additions.py` and
  `bootstrap/tests/test_lockfile_provenance.py`:
  **254 passed** (48.01 seconds wall), including the public nested-name,
  contained `dst` and `base_cache` aliases, staged-name and repaired plain-name
  tests.
* `python3.13 -m pytest -q bootstrap/tests/test_security_lint.py`:
  **11 passed** (3.92 seconds wall).
  `python3.13 scripts/claim_check.py bootstrap/UPGRADE.md` passed;
  `python3.13 scripts/check_cairn.py` and
  `python3.13 scripts/link_check.py` passed on 195 Markdown files each;
  `python3.13 scripts/quality_gate.py --sub neutrality` reported
  `fail=0, info=43`. These prose gates took about 2.6 seconds together.

The earlier four mutation controls and mutants were measured at `f8f96cdb`;
the nested Git guard has not changed since then, but the mutations were not
remeasured on this candidate. The earlier public recovery rehearsal was also
not repeated. No full-tree certifying suite or re-anchor was run. Boundary B
cannot be closed while the six mapped failures remain. The code and Security
reviews remain open; reviewers must assess the final corrected candidate and
the stated mutation and public-path coverage. The inventory discrepancy has a
separate awaiting-decision proposal, and this record makes no Decision or
scope concession.

## Final implementation verification -- Codex GPT-6 -- 2026-10-30

**Boundary B:** wide, complete for the reviewed mapping. **Certified by:**
pending. **Candidate:** `66b19e4bfc1fce5da14af4aae553ea2ade4e043d`;
implementation and corrections since `f8f96cdb`. The test copy was a detached
local clone with Git history. `git status --short` was empty before and after
the run. Interpreter: Python 3.13.13 at
`/Users/kendal30/conda_envs/lhm/bin/python3.13`. Elapsed measured test time
was about 140 seconds; reported token use is unknown.

The following `python3.13 -m pytest -q --tb=short` selections ran in that
clean copy, split to respect the broad-run file limit:

| Test files under `bootstrap/tests/` | Outcome | Wall time |
|---|---:|---:|
| `test_upgrade.py`, `test_upgrade_lockfile_path_containment.py`, `test_upgrade_side_door_parity.py` | 241 passed | 44.66 s |
| `test_upgrade_refuses_hostile_project_data.py`, `test_upgrade_module_additions.py`, `test_lockfile_provenance.py` | 259 passed | 47.40 s |
| `test_install_report_slots.py`, `test_install_module.py`, `test_module_merge.py` | 36 passed | 0.98 s |
| `test_scaffold.py` | 70 passed | 0.81 s |
| `test_skills_upgrade.py`, `test_upgrade_added_slots.py`, `test_upgrade_edit_check_runs_no_project_programs.py` | 123 passed | 39.57 s |
| `test_security_lint.py` | 11 passed | 1.97 s |

The first two selections are the nested Git plan's owning and consumer
families, including public `--plan`, `--stage`, `--apply`, nested destination,
base-cache alias, staged-name, protected-state and recovery cases. The later
selections are shared with the upgrade-integrity mapping. Total: **740 passed,
zero failed, skipped or xfailed**. The old inventory, template and staged
fixture failures no longer occur on these bytes.

Four separate one-line mutants of `bootstrap/_scaffold/upgrade.py` were tested
against an unmutated control at this commit. The control's two guard nodes and
seven normalization cases passed (9/9). Removing supplied-name filtering made
its guard node fail to refuse (1 failed): **killed**. Removing resolved-target
filtering made its alias node fail to refuse (1 failed): **killed**. Removing
case folding made three of seven variants fail to refuse (3 failed, 4 passed):
**killed**. Removing trailing-dot/space normalization made four of seven
variants fail to refuse (4 failed, 3 passed): **killed**. Total: **4 killed,
0 survivors, 0 measured equivalents**. Each mutant copy differed from the
candidate only at its named guard expression; `git diff --check` passed.

On the same clean candidate, `python3.13 scripts/claim_check.py
bootstrap/UPGRADE.md`, `python3.13 scripts/check_cairn.py` and
`python3.13 scripts/link_check.py` passed (the latter two scanned 196 Markdown
files each). `python3.13 scripts/quality_gate.py --sub neutrality` passed with
`fail=0, info=43`. No synced snippet changed. No non-pass remains in the mapped
checks. The earlier direct scratch public-command recovery rehearsal was not
repeated; the final owning tests exercise those public commands. Native
Windows equivalence, hard-link identity aliases and filesystem races were not
tested and are outside the stated protection. No full-tree certifying suite or
re-anchor ran. Independent code and Security reviews remain required before
archive; this verification does not clear either review.

## Final code review -- Codex GPT-6.1 Sol -- 2026-10-30

```
Reviewed candidate: 66b19e4bfc1fce5da14af4aae553ea2ade4e043d
Verification record: 88dad068a40a7029ae20df6553c91c3277823746
Tier: Internal
Elapsed time: approximately 5 minutes
Token use: unknown
```

**Verdict:** pass; no findings. **Bounding:** mapped wide run sufficient.
Security Review remains owed.

**Foundations**

1. **Does it do what it claims?** Yes on tested bytes: the shared guard refuses
   supplied and resolved project components, preserving source handling and
   ordinary links (`bootstrap/_scaffold/upgrade.py:177`; 81 focused tests).
2. **Best alternative.** Keep the shared guard. Filtering individual readers
   would duplicate it across lockfile and staged-name callers
   (`bootstrap/_scaffold/upgrade.py:282`, `bootstrap/_scaffold/upgrade.py:3304`).
3. **What would show it wrong?** A nested or aliased Git path succeeding through
   `--plan`, `--stage` or `--apply`, altered protected state on refusal, or an
   ordinary contained link being rejected (the owning tests below).

**Falsification ledger.** In a clean detached clone under Python 3.13.13,
`pytest -q` on `bootstrap/tests/test_upgrade_lockfile_path_containment.py` and
`bootstrap/tests/test_upgrade_refuses_hostile_project_data.py` with
`-k 'git or alias or contained_link or recovery'` passed 81 tests (207
deselected); two direct source/link controls passed. The author-owned wide
record reports 740 passes and four killed
guard mutants. I independently listed
the six staged lists and two maps from `_apply_upgrade` at line 3270, then
removed each member's validation in its own detached worktree. Unmutated
controls passed 24/24 list cases and 4/4 map cases; all eight mutants were
killed (six yielded four failures each; both map mutants yielded one failure
each). Survivors: none; measured equivalents: none. No full suite ran.

**Covered:** claims, public paths, completeness and fail-closed behavior
(`bootstrap/_scaffold/upgrade.py:177`, `bootstrap/_scaffold/upgrade.py:3268`,
the two tests and eight mutants); consistency and drift
(`bootstrap/UPGRADE.md:769`); lifecycle and scope (plan C1/C2 and verification);
satisfier (no finding).
**Not covered / low confidence:** native Windows behavior, hard-link identity
aliases, concurrent filesystem changes, and independent mutation of nested
`recovery_bases` and `ancestor_evidence` members. Security Review is separate.

## Final Security Review -- Codex GPT-6 Security Reviewer -- 2026-10-30

**Reviewed candidate**: `66b19e4bfc1fce5da14af4aae553ea2ade4e043d`; **verification record**: `88dad068a40a7029ae20df6553c91c3277823746`.
**Obligation**: Security Review. **Tier**: Internal Security Review. **Verdict**: pass; no findings. **Bounding**: ACCEPTED for this plan's mapped wide checks. Elapsed time: approximately 3 minutes; token use: unknown.

**Foundations**

1. **Does it do what it claims?** The project guard checks both path representations before use, and the final record covers the mapped public paths and protected state (`bootstrap/_scaffold/upgrade.py`, `_contained_lockfile_path`; verification at `88dad068`).
2. **Best alternative.** Keep the shared guard: filtering individual readers duplicates the security boundary (`bootstrap/_scaffold/upgrade.py`, `_check_lockfile_paths` and `_apply_upgrade`).
3. **What would show it wrong?** A Git path reaching project reads or writes, or protected state changing on refusal, would defeat the boundary (falsification ledger below).

**Falsification ledger.** In a detached worktree at the candidate, Python 3.13.13 ran `pytest -q bootstrap/tests/test_upgrade_refuses_hostile_project_data.py::test_apply_refuses_nested_metadata_paths_into_git_data`: the unmutated control passed 6/6. Removing `base_cache` from the `ancestor_evidence` validation list caused its corresponding public apply case to fail (exit 1 instead of the required security refusal); one mutant, one killed, no survivors or measured equivalents. The earlier independent public cache-alias control and mutant are recorded above. The author records 740 mapped passes, no non-passes and four killed guard mutants on the final candidate; the ordinary reviewer recorded eight killed outer-collection mutants. No full suite or re-anchor ran.

**Covered:** nested metadata, supplied and resolved path boundary, protected-state and public-path evidence, and final verification record (guard, test and records above). **Not covered / low confidence:** native Windows behavior, hard-link identity aliases and concurrent changes; those are outside the stated protection. Other concurrent work on the engine has its own review records.
