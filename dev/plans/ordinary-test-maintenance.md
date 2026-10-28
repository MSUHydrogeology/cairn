# Plan: Ordinary test maintenance

**Source proposal**: dev/proposals/archive/2026-10-28-codex-ordinary-test-maintenance.md
**Status**: awaiting-plan-review
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
