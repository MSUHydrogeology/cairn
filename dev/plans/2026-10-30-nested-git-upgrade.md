# Plan: Protect nested Git data during upgrades

**Source proposal**: dev/proposals/archive/2026-10-29-codex-nested-git-upgrade.md
**Status**: implementing
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
