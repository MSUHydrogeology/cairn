# Plan: Render the review inventory

**Source proposal**: dev/proposals/archive/2026-10-30-codex-review-inventory-rendering.md
**Status**: awaiting-code-review
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

## Implementation verification -- Codex GPT-6 -- 2026-10-30

**Boundary B mode**: wide. The change alters the review-copy contract in
`bootstrap/_scaffold/upgrade.py`; the mapping covers upgrade, reconciliation,
other review-pair consumers, containment, public install/`--init-lock`/`--stage`
paths, and neutrality/redundancy gates.

**Certified by**: pending

**Tested commit**: `9675ea1b68241a8f86904cc02f71f962b70232a6`

**Reviewed range**: `eeec9646fbac4b1f32b4d58c80812864bd6a92e0..9675ea1b68241a8f86904cc02f71f962b70232a6`

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python`, CPython
3.13.13. This is the repository-documented 3.13 runtime named in
`bootstrap/tests/_ast_attest.py`. Session-start reported no per-worktree Git
interpreter binding; this check used the documented runtime directly and did
not change the binding.

**Pre-run state**: clean clone at the tested SHA; `git status --short` empty.

**Post-run state**: clean clone at the identical tested SHA; `git status --short`
empty.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `python -m pytest -q bootstrap/tests/test_upgrade.py` | 0 | 138 passed | 31.61 s | unknown |
| `python -m pytest -q bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_module_merge_lockfile.py` | 0 | 64 passed | 23.84 s | unknown |
| `python -m pytest -q bootstrap/tests/test_upgrade_added_slots.py bootstrap/tests/test_upgrade_side_door_parity.py bootstrap/tests/test_skills_upgrade.py` | 0 | 48 passed | 16.52 s | unknown |
| `python -m pytest -q bootstrap/tests/test_upgrade_lockfile_path_containment.py` | 0 | 93 passed | 8.76 s | unknown |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | 0 failures; neutrality 43 info, redundancy 1 info | 1.14 s | unknown |
| `python scripts/claim_check.py` on the changed engine, both owning tests, and this plan | 0 | All four files passed | <0.01 s each | unknown |
| `python scripts/check_cairn.py` | 0 | 199 Markdown files; no issues; 94 external links not probed | 1.31 s | unknown |
| `python scripts/link_check.py` | 0 | 199 Markdown files; no issues; 95 external links not probed | 0.18 s | unknown |
| `python scripts/sync_doc_snippets.py --check` | 0 | 476 documents; no drift | 0.17 s | unknown |

**Mutation summary**: unmutated control was the clean tested commit above; its
three focused review-inventory cases passed. Total 2; killed 2; survivors 0;
measured equivalents 0. Removing `_render_review_inventory` was killed by the
independent expected-entry assertion
(`test_review_inventory_renders_selected_roster_from_current_source`); the mutation run had 1 failing selected-roster
case and 1 passing empty-roster case. Replacing the rendered `.theirs` with the
installed `.ours` was killed by the local-note exclusion assertion
(`test_review_inventory_theirs_excludes_local_edit_when_roster_matches`). Each
mutation ran in its own clone of the committed candidate; both controls passed.
Mutation runs took under one second each; token use unknown.

**Non-pass disposition**: no mapped test or required gate failed. The quality
gate's informational lines include an existing R6 note for
`_apply_module_discovery`; it is unrelated to this change. Mutation test exits
of 1 are expected kills, not candidate failures.

**Plan-specific acceptance commands**: current and historical public staging,
including matching renderer, historical description, changed renderer,
changed metadata, malformed and missing markers, unknown module, cleanup,
empty roster, and `.ours`/`.theirs` separation, passed in `test_upgrade.py`.
The historical compatibility tests keep selected template bytes passive and
exercise only `git show`; no historical code was executed.

**Known omissions**: no full-tree certifying suite or re-anchor was run; neither
is authorized by this plan. Boundary C remains for the independent code
reviewer. External links reported as unprobed by the prose gates were not
fetched.

## Code review -- Codex (GPT-6) -- 2026-10-30

```
Reviewed commit: 9675ea1b68241a8f86904cc02f71f962b70232a6
Verification record: 19360fb9
Target: C1 implementation and Boundary B
Elapsed: approximately 10 minutes
Tokens: unknown
```

**Obligation**: Internal usual code review
**Verdict**: REVISE
**Bounding**: mapped wide run is sufficient; no wider run required.

**Foundations**:

1. **Should this happen as framed?** Yes. Stage renders selected upstream text and roster into `.theirs`; `.ours` reads installed bytes -- `upgrade.py::_write_stage`, `test_upgrade.py::TestInitLock::test_review_inventory_theirs_excludes_local_edit_when_roster_matches`.
2. **Best alternative.** Keep the reconciler and compatibility guard; they preserve upstream entries and refuse differing renderers -- `install.py::_reconcile_generated_blocks`, `upgrade.py::_render_review_inventory`.
3. **What would show it wrong?** A successful stage with a duplicate entry, a current renderer mismatch, or a missing installed inventory that produces `.ours` would violate C1 -- plan Acceptance criteria; `upgrade.py:1405-1423`.

**Blocking finding -- accepted edge cases lack public-path tests.** C1 requires a missing installed inventory with no `.ours` and duplicate entry markers. `rg -n 'README.md.ours|duplicate.*module|missing.*inventory' bootstrap/tests` finds only present-inventory `.ours` assertions (`test_upgrade.py:1281,1301`). The malformed fixture duplicates generated-block starts, not entries (`test_upgrade.py:1310-1355`). Close with public `--stage` cases asserting absent `.ours` and refusal/cleanup for duplicate entries. These accepted checks remain unmet, although a helper probe refused duplication.

**Falsification ledger.** Clean clone 9675ea1b: nine focused inventory tests passed (Python 3.13.13). Helper probes refused duplicate entries and mismatched current metadata, preserved a selected edited upstream entry, and refused an edited unselected one. Boundary B records 343 mapped passes and two killed mutations; I checked SHA, clean states, families and gates against the plan without rerunning them.

Coverage: claims/path/edges/fail-closed (`upgrade.py:360-437,1265-1284,1405-1423`; probes), reuse/drift (`install.py:1336-1450`; proposal Current contract), lifecycle/scope/satisfier (plan C1; finding), scientific validity (no scientific claim). No full suite, apply run, concurrent-path replacement, or code Security Review; the latter remains owed.

## Implementation verification -- Codex GPT-6 follow-up -- 2026-10-30

This record covers the two public-path tests added for the blocking findings in
the code review at `0f766e0d`; it supersedes the earlier Boundary B record for
the latest candidate.

**Boundary B mode**: wide. The prior map remains appropriate: this follow-up
adds public `--stage` coverage for missing installed inventory and duplicate
per-entry markers, while the reviewed engine behavior and its consumers remain
covered by the same owning families and standing gates.

**Certified by**: pending

**Tested commit**: `b8ab602ece9ce6102e08c726d4a77da257c46721`

**Reviewed range**: `eeec9646fbac4b1f32b4d58c80812864bd6a92e0..b8ab602ece9ce6102e08c726d4a77da257c46721`

**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python`, CPython
3.13.13; same repository-documented runtime as the prior record. The local
per-worktree Git interpreter binding is absent; this check used the documented
runtime directly and did not change the binding.

**Pre-run state**: clean clone at the tested SHA; `git status --short` empty.

**Post-run state**: clean clone at the identical tested SHA; `git status --short`
empty.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `python -m pytest -q bootstrap/tests/test_upgrade.py` | 0 | 140 passed | 32.32 s | unknown |
| `python -m pytest -q bootstrap/tests/test_upgrade_module_additions.py bootstrap/tests/test_module_merge_lockfile.py` | 0 | 64 passed | 24.25 s | unknown |
| `python -m pytest -q bootstrap/tests/test_upgrade_added_slots.py bootstrap/tests/test_upgrade_side_door_parity.py bootstrap/tests/test_skills_upgrade.py` | 0 | 48 passed | 16.96 s | unknown |
| `python -m pytest -q bootstrap/tests/test_upgrade_lockfile_path_containment.py` | 0 | 93 passed | 9.49 s | unknown |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | 0 failures; neutrality 43 info, redundancy 1 info | 1.18 s | unknown |
| `python scripts/claim_check.py` on upgrade.py, test_upgrade.py, and this plan | 0 | All three files passed | <0.01 s each | unknown |
| `python scripts/check_cairn.py` | 0 | 199 Markdown files; no issues; 94 external links not probed | 1.26 s | unknown |
| `python scripts/link_check.py` | 0 | 199 Markdown files; no issues; 95 external links not probed | 0.11 s | unknown |
| `python scripts/sync_doc_snippets.py --check` | 0 | 476 documents; no drift | 0.12 s | unknown |

**Mutation summary**: the unmutated control was a clean clone of the tested
commit; five focused inventory cases passed. Total 2; killed 2; survivors 0;
measured equivalents 0. Removing `_render_review_inventory` was killed by the
selected-entry assertion and duplicate-entry refusal/cleanup assertion; the
five-case mutation run had 4 failures and 1 pass. Substituting installed `.ours`
for `.theirs` was killed by the local-note exclusion and missing-inventory
assertions; its five-case run had 4 failures and 1 pass. Each mutant ran in a
separate clone of the tested commit. Mutation token use unknown.

**Non-pass disposition**: no mapped test or required gate failed. Mutation
exits of 1 are expected kills. The quality-gate informational lines, including
the existing R6 note for `_apply_module_discovery`, are not failures.

**Plan-specific acceptance commands**: the new missing-installed-inventory
test asserts `.theirs` exists and `.ours` does not. The duplicate-entry test
injects two markers with the same module id through the public `--stage` path,
then asserts refusal, stale-stage cleanup, and unchanged installed and ancestor
bytes. Both passed in the mapped upgrade family.

**Known omissions**: no full-tree certifying suite or re-anchor was run; neither
is authorized here. Boundary C and the code Security Review remain with
independent reviewers. External links reported as unprobed were not fetched.
