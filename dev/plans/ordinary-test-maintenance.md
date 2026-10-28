# Plan: Ordinary test maintenance

**Source proposal**: dev/proposals/archive/2026-10-28-codex-ordinary-test-maintenance.md
**Status**: revising-plan
**Plan review**: required(Internal)
**Opened**: 2026-10-28
**In brief**: Simplify one board test cluster without losing fault detection and share the resulting test-maintenance practice.

## Source proposal

The Maintainer accepted the two-node pilot staged after test-trust-boundary implementation and directed that it refer to the test-practice strategy and update the testing module (`cea1299d`).

## Scope

Inventory and, if useful, simplify the named JSON-output cluster in `bootstrap/tests/test_board_json_contract.py`; update `templates/modules/team-gated/testing-discipline.md` and its self-hosted copy `dev/modules/testing-discipline.md`. The strategy `dev/strategy/2026-10-27-antigravity-judicious-testing-and-simulation-verification.md` informs concise test-maintenance practice: inventory behaviors and plausible faults, preserve detection, use public entry points, reuse setup with fresh mutable repositories, and distinguish test scope from runtime. This does not adopt its ratio target, new simulation guidance, parallel pytest, or dependencies. The broader suite work remains open.

**Reuse.** `rg -n '_build_golden_main_tree|board.main|tmp_path' bootstrap/tests/test_board_json_contract.py` locates existing builders and public entry points; assess whether they fit before extracting a fresh builder. Do not change protected cases or controlling helpers, the fixture, product code, schema or gates.

### Documentation / doctrine surface

The testing module is adopter-facing practice, with a self-hosted mirror; route it under `docs/DOCUMENTATION_PLAN.md`. No cross-cutting governing rule changes. Vendor-neutrality applies to the module; this does not alter the neutrality rule or other named high-risk controls.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inventory and baseline | Reviewed plan; completed test-trust-boundary implementation and final roster | Cluster properties, fault ledger and matched control timing |
| C2 | Simplify cluster | C1 establishes file eligibility and a useful extraction | Fresh setup reuse and preserved assertions |
| C3 | Update testing module | Reviewed plan and C1 evidence | Concise practice in shipped and self-hosted copies |

Before any board-file edit, check the installed final protected roster. If it protects the file, stop and return scope and assurance to the Maintainer; do not select another file automatically. Even if unprotected, change no protected case or shared controlling helper. If extraction adds more indirection than it removes, retain the tests and return the pilot scope to the Maintainer before changing it.

## Acceptance criteria

### C1 — inventory and baseline

Inventory both `TestRecordFactsComeFromWhereTheFileSits::test_all_record_values_and_absent_vs_blank_and_headerless_files` and `TestOutputIsDeterministic::test_archives_unique_path_key_and_deterministic_ascii_json`: setup, public behavior and plausible faults. Record baseline duplication and a timed owning-family run on the committed control using the canonical interpreter, environment and durations settings to be matched later. Document the installed roster and file eligibility before editing. For each proposed removed case, map its property and fault to a retained assertion and a probe; retain it without a convincing replacement.

### C2 — preserve behavior

Reuse immutable descriptions or builders creating fresh paths and mutable repositories per call. Preserve absent versus blank, header boundaries, headerless plain-view omission, distinct archive paths, ordering, ASCII bytes and reproducibility across roots. Keep both named nodes and the existing real CLI/subprocess failure and exit checks. Compare matched family timings, slow nodes, duplication and reviewable case/line changes; report costs and no assumed speed gain. Only a certifying run supports whole-suite timing.

### C3 — module practice

Both module copies carry consistent concise guidance for behavior and fault inventory, preserving fault detection when consolidating, public entry points, reusable setup with fresh mutable repositories, and separating scope from runtime. Retain the existing tier and negative-test guidance; do not add simulation guidance or a numerical test-volume quota. Verify installation and the mapped module owners.

## Scope delta

**Scope delta**: preserved. The module update is the Maintainer's explicit addition to the accepted pilot. A protected file or failed extraction stops the pilot for Maintainer disposition, not silent substitution or scope removal.

## Verification

Boundary A: run the two named nodes and owning `bootstrap/tests/test_board_json_contract.py` family, including real `tools/board.py` paths. Search imports and readers of touched tests and helpers before edits; add any owners found. For the module run `bootstrap/tests/test_practice_modules.py`, `bootstrap/tests/test_doc_governance.py`, `bootstrap/tests/test_presets.py` and `bootstrap/tests/test_profiles_smoke.py`; search again for readers, mirrors and manifest pins at implementation and include those found. Check copies and installation content. Run applicable claim, link, snippet, prose-integrity and neutrality gates; inspect each trigger. Run timed control and final family with identical `pytest --durations` settings and environment.

Boundary B is full if a contract or trust-ceremony surface is touched, an effect cannot be bounded, or a required mapping is missing; otherwise record bounded mode with surfaces, tests, gates, counts, rationale and explicit absence of those surfaces. After the final implementation commit, run the scoped mapping and standing gates on a clean unchanged tree under `/Users/kendal30/conda_envs/lhm/bin/python3.13`. Record tested SHA and range, interpreter, pre/post state, commands, outcomes and counts, timing, non-pass dispositions and omissions. Set **Certified by**: pending until the next authorized certifying run. The independent code reviewer challenges the evidence and fault preservation without running the full suite.

## Plan review -- Codex (Terra), Internal plan reviewer -- 2026-10-28

```
Reviewed commit: b4cae7c239c3aabf8d5952a71b5e2c9b27446991
Target: Source proposal through Verification
Prior findings: none
Assurance path: required(Internal)
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: raised

**Foundations**

1. **Should this happen as framed?** The staged pilot and matched scoped timing deliver the accepted two-node contract, but the module criterion leaves an existing contradiction in place. -- `dev/proposals/archive/2026-10-28-codex-ordinary-test-maintenance.md` > Complete current contract; `templates/modules/team-gated/testing-discipline.md` > Template content.
2. **Best alternative.** Keep the staged pilot and reconcile the module's existing tier explanation while adding the requested maintenance practice; an appended paragraph alone cannot settle both claims. -- `dev/strategy/2026-10-27-antigravity-judicious-testing-and-simulation-verification.md` > Review; `templates/modules/team-gated/testing-discipline.md` > Template content.
3. **What would show it wrong.** An installed protected roster covering the file, no useful fresh builder, or a fault without a retained probe stops the pilot; incompatible tier guidance would also leave the module update incomplete. -- plan C1–C3; `bootstrap/tests/test_board_json_contract.py` > `TestOutputIsDeterministic`.

**F1 — Blocking: reconcile existing module claims with the new practice.** C3 asks to separate scope from runtime while retaining tier guidance, but the existing module says a tier alone tells readers a test's cost and scope, and says it does not teach test craft. Adding the requested maintenance guidance without changing these claims can leave adopters with contradictory instructions. Specify that C3 revises those claims in both copies while preserving location-based tiers and negative tests, and verifies the installed wording. This carries the requested practice rather than discarding the existing scheme. -- `templates/modules/team-gated/testing-discipline.md` > introduction and Template content; `dev/modules/testing-discipline.md`; plan C3.

**Covered**: accepted scope and staging (proposal Complete current contract and Decision; plan C1); public path and fault coverage (`bootstrap/tests/test_board_json_contract.py` > `TestRecordFactsComeFromWhereTheFileSits` and `TestOutputIsDeterministic`; plan C1–C2); reuse (plan search and `rg -n 'def _build|def _run_json' bootstrap/tests/test_board_json_contract.py`); fail-closed eligibility (plan Sequence); module consistency and installation (`bootstrap/_scaffold/config.py` > testing-discipline; `bootstrap/tests/test_practice_modules.py` > `TestInstallPath`; F1); scientific scope (plan Scope). **Not covered**: future roster eligibility, implementation timing or mutations, and an adopter trial. No tests run in this plan review.
