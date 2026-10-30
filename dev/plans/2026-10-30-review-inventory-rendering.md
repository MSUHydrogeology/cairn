# Plan: Render the review inventory

**Source proposal**: dev/proposals/archive/2026-10-30-codex-review-inventory-rendering.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-10-30
**In brief**: Show the selected modules in the upstream review copy so local edits remain visible.

## Source proposal

The accepted proposal requires an independently rendered inventory review copy, using the lock roster and selected upstream source, while preserving installed content, raw ancestors and apply behavior. Invalid structure or unavailable faithful metadata must not produce a misleading successful comparison.

## Scope

Change `bootstrap/_scaffold/upgrade.py` and the owning tests, principally `bootstrap/tests/test_upgrade.py`. Reuse the inventory renderer and reconciliation in `bootstrap/_scaffold/install.py`; searches for `generated-modules`, `review-only`, and inventory readers found the template, install and upgrade engines, and the upgrade, module-addition, added-slot, skill and side-door tests. Keep other review pairs and reconciliation untouched. The selected-source metadata must match the running renderer's metadata before reuse; for `--to`, compare the selected source's metadata-bearing config bytes with the running source without executing historical code. Refuse if equality cannot be established, a member is unknown, or upstream structure is invalid. This conservative check may refuse a source with unrelated config changes; it never claims a faithful comparison when metadata differs. Validate generated and per-entry markers, including duplicate, nested and unmatched markers, before using the reconciler. Treat upstream pre-existing entries as upstream text, validate their structure and identity, and use reconciliation only when it can faithfully represent the selected roster; otherwise refuse.

### Documentation / doctrine surface

No doctrine surface. Update the upgrade engine's descriptive review-pair text; change external descriptive guidance only if its existing statement becomes inaccurate.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Validate source, roster and structure; render review copy and exercise public paths | Both plan reviews | Engine and focused tests |

## Acceptance criteria

C1: The selected upstream inventory is rendered for every recorded module, including an empty roster, with independently asserted expected entries. `.ours` retains local edits, `.theirs` excludes them, and missing installed inventory has no `.ours`. Unknown members, missing or malformed upstream markers, and unverified or different source metadata refuse stage without a usable partial stage; existing installed bytes and raw ancestor evidence remain unchanged. Historical tests deliberately change source descriptions and prove refusal; matching source metadata permits rendering. Duplicate, nested, unmatched and pre-existing entry cases are covered. Other review pairs, path containment, staged-input protection and apply semantics remain intact. Public install, `--init-lock`, and `--stage` paths are exercised. Separate mutations removing rendering and substituting `.ours` must each be killed by independent assertions; record control, counts and outcomes. No scientific claim is touched.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A: run `python -m pytest bootstrap/tests/test_upgrade.py` for migration, staging and review pairs; `python -m pytest bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_module_merge_lockfile.py` for reconciliation and adoption; and `python -m pytest bootstrap/tests/test_upgrade_added_slots.py bootstrap/tests/test_upgrade_side_door_parity.py bootstrap/tests/test_skills_upgrade.py` for other review pairs and staged-input consumers. Run `python -m pytest bootstrap/tests/test_upgrade_lockfile_path_containment.py` for containment. Split invocations if the guard's selection limit requires it, preserving and reconciling the union. Run `python scripts/quality_gate.py --sub neutrality --sub redundancy` as standing gates. For changed prose run `python scripts/claim_check.py <changed-file>`, `python scripts/check_cairn.py`, `python scripts/link_check.py`, and `python scripts/sync_doc_snippets.py --check` after confirming the latter's supported interface; record any correction to the command. Search for changed-file readers and byte pins and run their owning checks. Exercise the two specified mutations on separate copies of the committed candidate, against an unmutated control, and record each result.

Boundary B: wide, because this changes an engine review contract. After the final implementation commit run the same mapping on a clean unchanged commit under canonical Python 3.13.x; record the full SHA, range, pre/post state, commands, counts, elapsed time, tokens or unknown, non-pass dispositions, omissions and `Certified by: pending`. Boundary C is independent targeted falsification by the code reviewer, who challenges the mapping and records its bounding verdict. Full-tree certification and re-anchor are separate ceremonies and are not authorized by this plan.
