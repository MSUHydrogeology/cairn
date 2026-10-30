# Plan: Reuse review-sweep installations

**Source proposal**: dev/proposals/archive/2026-10-29-codex-certification-cost-audit.md
**Status**: awaiting-plan-review
**Plan review**: required(Internal)
**Opened**: 2026-10-30
**In brief**: Share each profile's real test installation across the session to avoid repeated setup.

## Source proposal

The accepted proposal selected one ordinary test-family change after an authorized certification report, scoped timings and fault probes: make `installs` in `bootstrap/tests/test_review_sweep_ships.py` session-scoped. The installed manifest still freezes that file, so its separate frozen-file ceremony remains owed. No extra full suite or baseline installation is authorized here.

## Scope

Change only `@pytest.fixture(scope="module")` to `scope="session"` for `installs` in `bootstrap/tests/test_review_sweep_ships.py` if the checks below hold. Retain all test nodes and real `bootstrap/scaffold.py` installations into separate temporary trees for every globbed shipped profile. Inventory every fixture consumer and any tree mutation before changing scope; stop for a separate proposal if a consumer needs a fresh tree, if protection cannot be shown, or if a protected/high-risk change, trust-boundary judgment, dependency or certification-contract change becomes necessary. Do not change protection classification, manifest hashes or live refs.

**Reuse.** Reuse the existing fixture and installation CLI; no helper is added. Searches for `installs`, `test_review_sweep_ships`, and `scope="module"` identify the owning fixture, its four consuming test functions, and no second fixture implementation.

### Documentation / doctrine surface

No doctrine or descriptive software text changes. The plan and its evidence belong in `dev/`.

## Sequence

| # | Chunk | Gate | Ships |
|---|---|---|---|
| C1 | Inventory consumers and establish repeatable scoped control; change fixture lifetime and repeat timings and fault probes | Internal plan review; stop conditions in Scope | One test-file edit and measured comparison |

## Acceptance criteria

C1: The inventory lists all current consumers and confirms they read the installed trees or mutate copies of text, with no required fresh tree. Each profile still installs through the real CLI into its own tree, all existing nodes remain collected, and shuffled interleaving with `test_content_scan.py` produces stable outcomes. On identical committed candidate bytes and stated machine conditions, repeated same-command `--durations=0 --durations-min=0` reports show setup, call and teardown phases and a useful, stable reduction in review-sweep setup time; report raw times and limits, without a whole-suite speed claim. Beside a green unmutated control, separately remove lens 4, remove the correctly matched pointer phrase, and add an unknown placeholder in installed-content copies; each fault must fail its expected nodes for every shipped profile. Report the initial historical surviving pointer probe separately. If timing is unstable or a fault survives, stop without claiming the improvement. The file's frozen-manifest ceremony remains due.

## Scope delta

**Scope delta**: preserved

## Verification

Boundary A: use canonical Python 3.13.x in an isolated copy. Inventory `installs` references and installed-tree writes with `rg`; compare the pre-edit and post-edit committed candidates using `python -m pytest bootstrap/tests/test_review_sweep_ships.py bootstrap/tests/test_content_scan.py --quality-gate-shuffle-seed=0 --durations=0 --durations-min=0`, repeated under stated conditions with phase totals. Run the same selection with at least one alternate shuffle seed for interleaving and reconcile collected nodes; run the three separate fault probes through real installed-content nodes beside an unmutated control. Check the installed roster and manifest classification and run `bootstrap/tests/test_gate_manifest.py` or its owning nodes for the frozen-file consequence. Run `python scripts/claim_check.py` on changed prose, `python scripts/check_cairn.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check` if supported, and `python scripts/quality_gate.py --sub neutrality --sub redundancy`; record inapplicable checks with reasons.

Boundary B: **wide**, because the changed test is still frozen in the installed manifest. After the final implementation commit, run the reviewed owning family, content-scan integration, shuffle/interleaving selections, fault controls and standing gates on a clean unchanged commit under canonical Python 3.13.x. Record SHA/range, touched surface, interpreter, clean pre/post state, commands and counts, elapsed time, tokens or unknown, non-pass disposition, omissions and `Certified by: pending`; preserve the owed frozen-file ceremony rather than treating a changed hash as a passing gate. Boundary C is independent code review, including fault falsification and a bounding verdict. Full-tree certification and re-anchor are separate ceremonies.
