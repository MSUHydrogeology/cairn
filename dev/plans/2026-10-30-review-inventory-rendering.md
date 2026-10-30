# Plan: Render the review inventory

**Source proposal**: dev/proposals/archive/2026-10-30-codex-review-inventory-rendering.md
**Status**: ready-to-implement
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Show the selected modules in the upstream review copy so local edits remain visible.

## Source proposal

The accepted proposal requires an independently rendered inventory review copy, using the lock roster and selected upstream source, while preserving installed content, raw ancestors and apply behavior. Invalid structure or unavailable faithful metadata must not produce a misleading successful comparison.

## Scope

Change `bootstrap/_scaffold/upgrade.py` and the owning tests, principally `bootstrap/tests/test_upgrade.py`. Reuse the inventory renderer and reconciliation in `bootstrap/_scaffold/install.py`; searches for `generated-modules`, `review-only`, and inventory readers found the template, install and upgrade engines, and the upgrade, module-addition, added-slot, skill and side-door tests. Keep other review pairs and reconciliation untouched. For an explicit `--to`, compare the selected source’s `bootstrap/_scaffold/config.py` and `bootstrap/_scaffold/install.py` bytes with the running source before reusing its renderer; refuse when either is absent or differs. This conservative check may refuse unrelated changes. Do not execute historical code. For the current source, render only when the source and running renderer are the same; otherwise refuse. Also refuse an unknown member or invalid upstream structure. Validate generated and per-entry markers, including duplicate, nested and unmatched markers, before using the reconciler. Treat upstream pre-existing entries as upstream text, validate their structure and identity, and use reconciliation only when it can faithfully represent the selected roster; otherwise refuse.

### Documentation / doctrine surface

No doctrine surface. Update the upgrade engine's descriptive review-pair text; change external descriptive guidance only if its existing statement becomes inaccurate.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Validate source, roster and structure; render review copy and exercise public paths | Both plan reviews | Engine and focused tests |

## Acceptance criteria

C1: The selected upstream inventory is rendered for every recorded module, including an empty roster, with independently asserted expected entries. `.ours` retains local edits, `.theirs` excludes them, and missing installed inventory has no `.ours`. Unknown members, missing or malformed upstream markers, and unavailable or different selected renderer or metadata, or an unverified current source, refuse stage without a usable partial stage; existing installed bytes and raw ancestor evidence remain unchanged. Historical tests through `--to --stage` prove that matching renderer and metadata permit rendering, and separately change descriptions and renderer behavior, the latter with unchanged metadata, to prove refusal and cleanup; current-source staging renders normally. Duplicate, nested, unmatched and pre-existing entry cases are covered. Other review pairs, path containment, staged-input protection and apply semantics remain intact. Public install, `--init-lock`, and `--stage` paths are exercised. Separate mutations removing rendering and substituting `.ours` must each be killed by independent assertions; record control, counts and outcomes. No scientific claim is touched.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A: run `python -m pytest bootstrap/tests/test_upgrade.py` for migration, staging and review pairs; `python -m pytest bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_module_merge_lockfile.py` for reconciliation and adoption; and `python -m pytest bootstrap/tests/test_upgrade_added_slots.py bootstrap/tests/test_upgrade_side_door_parity.py bootstrap/tests/test_skills_upgrade.py` for other review pairs and staged-input consumers. Run `python -m pytest bootstrap/tests/test_upgrade_lockfile_path_containment.py` for containment. Split invocations if the guard's selection limit requires it, preserving and reconciling the union. Run `python scripts/quality_gate.py --sub neutrality --sub redundancy` as standing gates. For changed prose run `python scripts/claim_check.py <changed-file>`, `python scripts/check_cairn.py`, `python scripts/link_check.py`, and `python scripts/sync_doc_snippets.py --check` after confirming the latter's supported interface; record any correction to the command. Search for changed-file readers and byte pins and run their owning checks. Exercise the two specified mutations on separate copies of the committed candidate, against an unmutated control, and record each result.

Boundary B: wide, because this changes an engine review contract. After the final implementation commit run the same mapping on a clean unchanged commit under canonical Python 3.13.x; record the full SHA, range, pre/post state, commands, counts, elapsed time, tokens or unknown, non-pass dispositions, omissions and `Certified by: pending`. Boundary C is independent targeted falsification by the code reviewer, who challenges the mapping and records its bounding verdict. Full-tree certification and re-anchor are separate ceremonies and are not authorized by this plan.

## Plan review -- Codex (gpt-6.1-sol) -- 2026-10-30

```
Reviewed commit: 3012471d
Target: opening plan
Elapsed: about 5 minutes
Tokens: unknown
```

**Obligation**: Internal
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** Yes, with the historical-source check repaired. The selected lock roster and clean upstream text can make local edits visible without changing installed content -- plan C1; `bootstrap/_scaffold/upgrade.py::_write_stage`.
2. **Best alternative.** Reuse `_substitute_module_inventory` after validating structure and source compatibility; the existing reconciler already handles generated entries. Keep the change in the review-only branch -- `bootstrap/_scaffold/install.py::_reconcile_generated_blocks`; `bootstrap/_scaffold/upgrade.py:1303`.
3. **What would show it wrong?** A `--to` ref with identical config metadata but a different inventory renderer could yield a successful, inaccurate `.theirs` -- `_MODULE_DISCOVERY` in `bootstrap/_scaffold/config.py`; `_render_module_inventory` in `bootstrap/_scaffold/install.py`; plan Scope.

**Blocking finding 1 -- historical rendering compatibility.** The Scope checks metadata-bearing config bytes, but the selected source's rendering code can change while those bytes stay equal. Matching config alone therefore does not establish the accepted faithful comparison. Close by conservatively proving renderer compatibility too (for example, compare the selected source's renderer-bearing file bytes with the running source and refuse when unavailable or different), or by another check that proves the selected source would render the same bytes. Add a public `--to --stage` fixture that changes renderer behavior while keeping config metadata equal and asserts refusal without a usable partial stage. This is an unmet accepted criterion, not a request to execute historical code.

Coverage: claims and fail-closed behavior (`Scope`, `_render_module_inventory`), public path and edge fixtures (`test_upgrade.py::TestInitLock`), reuse (`_reconcile_generated_blocks`), drift and placement (`docs/DOCUMENTATION_PLAN.md`, `_write_stage`), and scope/satisfier (accepted proposal's Current contract) were inspected. No implementation, historical fixture, test suite, mutation, or Security Review was run; failure cleanup and stage ordering remain implementation evidence.

## Plan review -- Codex (gpt-6.1-sol, Security Review) -- 2026-10-30

```
Reviewed commit: 3012471d589113cd9c95e6766b7846fd919accb8
Target: scope, acceptance criteria and verification mapping
Prior findings: none
Assurance path: high-assurance
Elapsed time: approximately 3 minutes
Token use: unknown
```

**Obligation**: Internal Security Review
**Tier**: Internal Security Review
**Findings**: raised
**Verdict**: REVISE

**Foundations**:

1. **Should this happen as framed?** Not yet: metadata equality does not establish that the selected source renders those values the same way -- plan Scope and C1; `bootstrap/_scaffold/upgrade.py::_write_stage`.
2. **Best alternative.** Reuse the existing reconciler after validation; a second renderer adds drift, and executing historical code adds authority to a passive review -- `bootstrap/_scaffold/install.py::_substitute_module_inventory` and `_reconcile_generated_blocks`.
3. **What would show it wrong?** A successful partial stage after malformed input, a historical description silently replaced with current metadata, or an adopter edit appearing in both sides would defeat the contract -- plan C1 and Verification; `bootstrap/_scaffold/install.py::_render_module_inventory`.

**Blocking finding 1 -- renderer compatibility.** The selected source can change rendering behavior while retaining identical config bytes. Require proof of renderer compatibility or refuse, and test a historical source with changed rendering and unchanged metadata through `--to --stage`, including cleanup. This closes the accepted faithful-comparison criterion -- plan Scope and C1; `bootstrap/_scaffold/install.py::_render_module_inventory`.

The other producer and consumer boundaries are mapped: the current renderer silently skips unknown members, and the reconciler retains selected pre-existing blocks; the plan requires membership and marker validation plus faithful handling before reuse. Its public-path tests and separate mutations challenge both omission and copied local content. The wide mapping includes containment and staged-input consumers; its cost is bounded to named families rather than full-tree certification -- `bootstrap/_scaffold/install.py::_render_module_inventory`, `_reconcile_generated_blocks`, and plan Verification.

Coverage: reviewed the accepted contract, source selection, roster, marker handling, staged review and mapped checks against the named commit. No implementation, test, mutation, historical-source probe, full suite or re-anchor was run; failure cleanup and actual check cost remain to be measured during implementation.

## Response to plan review -- Codex (gpt-6.1-sol) -- 2026-10-30

Both blocking findings accepted. Scope and C1 now refuse a review-only inventory under explicit `--to`, avoiding historical code execution and compatibility machinery; the historical renderer-change and metadata-change fixtures exercise refusal and cleanup. This preserves the proposal’s explicit refusal outcome. Elapsed time: approximately 3 minutes; tokens: unknown.

## Plan correction -- Codex (gpt-6.1-sol) -- 2026-10-30

The prior response refused all explicit historical sources, including sources where fidelity is verifiable. Scope and C1 now preserve the accepted selected-source outcome by comparing renderer and metadata files and refusing only when compatibility is unverified. The changed-renderer and changed-metadata fixtures remain, with a matching-source control. Elapsed time: approximately 2 minutes; tokens: unknown.
