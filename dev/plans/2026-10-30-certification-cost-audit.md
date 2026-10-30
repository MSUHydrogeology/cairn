# Plan: Reuse review-sweep installations

**Source proposal**: dev/proposals/archive/2026-10-29-codex-certification-cost-audit.md
**Status**: implementing
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

Boundary A: use canonical Python 3.13.x in an isolated copy. Inventory `installs` references and installed-tree writes with `rg`; compare the pre-edit and post-edit committed candidates using `python -m pytest bootstrap/tests/test_review_sweep_ships.py bootstrap/tests/test_content_scan.py --quality-gate-shuffle-seed=0 --durations=0 --durations-min=0`, repeated under stated conditions with phase totals. Run the same selection with at least one alternate shuffle seed for interleaving and reconcile collected nodes; run the three separate fault probes through real installed-content nodes beside an unmutated control. Check the installed roster and manifest classification, compare the changed file with its installed pin, and run `bootstrap/tests/test_gate_manifest.py::test_verify_holds_on_frozen_file_modification` during iteration for the frozen-file consequence. Run `python scripts/claim_check.py` on changed prose, `python scripts/check_cairn.py`, `python scripts/link_check.py`, `python scripts/sync_doc_snippets.py --check` if supported, and `python scripts/quality_gate.py --sub neutrality --sub redundancy`; record inapplicable checks with reasons.

Boundary B: **wide**, because the changed test is still frozen in the installed manifest. After the final implementation commit, run the reviewed owning family, content-scan integration, shuffle/interleaving selections, fault controls and standing gates on a clean unchanged commit under canonical Python 3.13.x. Record SHA/range, touched surface, interpreter, clean pre/post state, commands and counts, elapsed time, tokens or unknown, non-pass disposition, omissions and `Certified by: pending`; preserve the owed frozen-file ceremony rather than treating a changed hash as a passing gate. Boundary C is independent code review, including fault falsification and a bounding verdict. Full-tree certification and re-anchor are separate ceremonies.

## Plan review -- Codex GPT-6 Internal Reviewer -- 2026-10-30

```
Reviewed commit: 281e41d71562f0a956c13bae85d32de30119f3db
Target: opening plan, against accepted proposal and current fixture
Prior findings: none
Assurance path: standard
Elapsed: about 7 minutes
Tokens: unknown
```

**Obligation**: Internal
**Tier**: Internal
**Findings**: none
**Verdict**: ACCEPT

**Foundations**

1. **Should this happen as framed?** Yes. The one-line scope change retains every node and real profile install, while the plan makes isolation, repeated timing and fault detection acceptance conditions. -- accepted proposal `## Current contract`; plan C1; `bootstrap/tests/test_review_sweep_ships.py:318-375`.
2. **Best alternative.** Reuse the existing `installs` fixture with session lifetime; adding a cache helper or deleting nodes would increase machinery or lose behavior. -- `bootstrap/tests/test_review_sweep_ships.py:318-342`; plan Scope.
3. **What would show it wrong.** A consumer that writes a shared tree, unstable same-command phase results, a surviving fault, or shuffled state dependence would invalidate the change. -- plan Acceptance criteria; `bootstrap/tests/test_review_sweep_ships.py:345-429`.

The four fixture consumers read installed trees or alter local text copies, and the profiles are globbed through the real scaffold CLI. The plan still requires a fresh consumer inventory and shuffled evidence before accepting session sharing. The retained reports are single observations, so repeated scoped measurements are warranted; they should not trigger another full suite. During iteration, `bootstrap/tests/test_gate_manifest.py::test_verify_holds_on_frozen_file_modification` checks generic refusal more cheaply than the entire family; compare the actual changed file with its installed pin separately. The final wide map retains required owning coverage.

**Covered:** current claims and drift (proposal evidence, plan Scope); real path and design (fixture and four consumers); fail-closed behavior (C1 fault controls and stop); cross-document fit (roster and installed manifest); lifecycle, domain scope and satisfier (one-file change, separate ceremony). **Not covered / low confidence:** no tests or timing rerun, no complete consumer inventory beyond the named module, and no measured stability or full-suite speedup. The frozen-file ceremony remains owed.

## Response to plan review -- Codex (GPT-6.1 Sol) -- 2026-10-30

The Internal review accepted with no findings. I accepted its focused-manifest advice in Boundary A and retained the wide final mapping. The consumer inventory, repeated timings, shuffled runs and fault controls remain implementation acceptance checks; the review did not claim they were already measured. Elapsed time: about 2 minutes. Token use: unknown.
