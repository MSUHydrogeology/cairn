# Plan: Protect nested Git data during upgrades

**Source proposal**: dev/proposals/archive/2026-10-29-codex-nested-git-upgrade.md
**Status**: awaiting-plan-review
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
