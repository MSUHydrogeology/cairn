# Plan: Reuse review-sweep installations

**Source proposal**: dev/proposals/archive/2026-10-29-codex-certification-cost-audit.md
**Status**: archived
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

## Implementation verification -- Codex GPT-6 -- 2026-10-30

**Boundary B mode**: wide. The changed test file is frozen in the installed manifest. The review-sweep owning family, interleaved `test_content_scan.py`, both shuffle seeds, installed-content faults, frozen-file refusal control and standing prose gates were checked.

**Certified by**: pending
**Tested commit**: `6fc4d9eaddf4dc5082022665097f6c4e5fe40bd4`
**Reviewed range**: `291ab335959cb7e6328ed06060d5af6bf87af811..6fc4d9eaddf4dc5082022665097f6c4e5fe40bd4`
**Interpreter/runtime**: `/Users/kendal30/conda_envs/lhm/bin/python3.13` — Python 3.13.13, pytest 9.0.3
**Pre-run state**: clean detached copy at `6fc4d9eaddf4dc5082022665097f6c4e5fe40bd4`.
**Post-run state**: clean; same `HEAD`, no tracked or untracked changes. Mutants wrote only to pytest temporary install trees.

The inventory found exactly four consumers in `bootstrap/tests/test_review_sweep_ships.py`: `test_installed_loop_document_carries_the_obligation`, `test_installed_agents_md_carries_the_pointer`, `test_an_install_without_the_sweep_is_reported`, and `test_an_install_leaves_no_placeholder_the_engine_cannot_fill`. They read the installed trees; the sweep-removal check edits a local string. No consumer needs a fresh tree. Three globbed shipped profiles still install through the real scaffold CLI into separate temporary trees.

| Command | Exit | Outcomes | Elapsed | Tokens |
|---|---:|---|---:|---|
| `python -m pytest bootstrap/tests/test_review_sweep_ships.py bootstrap/tests/test_content_scan.py --quality-gate-shuffle-seed=0 --durations=0 --durations-min=0` on baseline `291ab335` (two runs) | 0 | 391 passed each; 31.80s, 31.74s | pytest reported | unknown |
| Same timed selection on implementation `e270902d` (two runs) | 0 | 391 passed each; 1.06s, 0.98s | pytest reported | unknown |
| Same timed selection, baseline second-run phase sums | 0 | Review-sweep setup 31.26s, call 0.02s, teardown 0.00s; content-scan setup 0.00s, call 0.14s, teardown 0.00s | included above | unknown |
| Same timed selection, implementation phase sums | 0 | Run 1: review-sweep setup 0.58s, call 0.02s, teardown 0.00s; content-scan call 0.15s. Run 2: review-sweep setup 0.49s, call 0.02s, teardown 0.00s; content-scan call 0.16s. Other phase sums 0.00s. | included above | unknown |
| `python -m pytest -q bootstrap/tests/test_review_sweep_ships.py bootstrap/tests/test_content_scan.py --quality-gate-shuffle-seed=0` on final candidate | 0 | 391 passed | 0.88s | unknown |
| Same final-candidate selection with `--quality-gate-shuffle-seed=1` | 0 | 391 passed; same 391 nodes collected | 0.82s | unknown |
| Nine installed-copy fault probes through existing nodes, three faults per profile | 1 per mutant, expected | 9/9 killed: lens 4, matched pointer phrase, unknown placeholder, each for all three profiles; no survivors or measured equivalents | 10.9s total | unknown |
| `python -m pytest -q bootstrap/tests/test_gate_manifest.py::test_verify_holds_on_frozen_file_modification` | 0 | 1 passed; refusal control holds | 8.46s | unknown |
| `python scripts/claim_check.py dev/plans/2026-10-30-certification-cost-audit.md` | 0 | No claim-check flags | <1s | unknown |
| `python scripts/check_cairn.py`; `python scripts/link_check.py`; `python scripts/sync_doc_snippets.py --check` | 0 each | 196 Markdown files clean; 94 and 95 external links respectively not probed; 477 docs scanned with no snippet drift | 3.2s total | unknown |
| `python scripts/quality_gate.py --sub neutrality --sub redundancy` | 0 | Both gates: 0 failures; neutrality 43 informational entries, redundancy 1 informational entry | <1s | unknown |

The timed commands used the same arguments on isolated committed copies with no overlapping test family. The second full baseline report and both implementation reports include setup, call and teardown entries; the first baseline console capture was truncated, so only its 31.80s pytest total is retained. The measured review-sweep setup fell from 31.26s to 0.58s and 0.49s; total elapsed fell from 31.74s to 1.06s and 0.98s. This is a scoped interleaving result, not a whole-suite speed claim. Shuffling alternates between the two modules, so module scope can reinstall the fixture when returning to its module; session scope retains the same three profile installations.

**Mutation summary**: unmutated control — final scoped selection, 391 passed under each seed. Total 9 mutants; killed 9. Each profile (`collaborative-team`, `high-rigor-legacy`, `solo-greenfield`) was tested separately for each mutation. Survivors: none. Measured equivalents: none. An initial temporary-hook attempt did not match the installed bold lens labels or line-wrapped pointer and stopped before mutating; the corrected hook matched each target and the expected existing assertion node failed. The historical pointer probe also initially survived because its search missed wrapped text; the archived evidence records that corrected matching removed the phrase and was caught.

**Non-pass disposition**: the nine fault commands intentionally exit 1 because the expected assertions reject each mutant. The first unmatched-hook attempts are instrumentation failures, not killed mutants, and are excluded from the count. All unmutated controls pass.

**Plan-specific acceptance commands**: covered by the timed repeated controls, final fixed and alternate shuffle selections, nine installed-tree fault probes, frozen-file refusal node and prose gates above. The 391-node count reconciles across both seeds; no test node was removed. No manifest hash, protection classification or live reference changed.

**Known omissions**: no full-tree certification, repin, re-anchor or anchor comparison was run; these remain separate ceremonies. **Certified by** remains pending, and the frozen-file ceremony remains due. External links were not probed by the Markdown checks. The implementation commit `e270902d` preceded the `implementing` status commit `6fc4d9ea` because the pre-implementation transition was missed; this record does not claim an earlier transition.

## Code review -- Codex GPT-6 Internal Reviewer -- 2026-10-30

Reviewed `6fc4d9ea` (implementation `e270902d`) in an isolated copy. Elapsed: about 6 minutes. Tokens: unknown. **Tier**: Internal. **Findings**: none. **Verdict / Bounding**: ACCEPT / ACCEPTED.

**Foundations**

1. **Should it happen?** Yes. The fixture invokes `bootstrap/scaffold.py` for each profile; four consumers read separate installed trees (`test_review_sweep_ships.py:318-440`). Recorded repeated controls show 391 passes and setup falling from 31.26s to 0.58s/0.49s (Implementation verification).
2. **Best alternative.** Keep module scope and repeated installs; session scope preserves the CLI and nodes (`e270902d` diff; `conftest.py:239-252`).
3. **What would show it wrong?** A shared-tree write, shuffled failure, or surviving installed-content fault. None appeared in the checks below.

**Falsification ledger**

- **Surfaces:** `rg` found four `installs` consumers; `bootstrap/profiles/*.yml` lists three profiles. Consumers write no install; one mutates local text, another inserts the source root into `sys.path` (`test_review_sweep_ships.py:366-440`).
- **Edge attempt:** each installed tree passed before and after a temporary fault; its named assertion failed under the fault.
- **Verification:** Python 3.13.13, interleaved seed 1: 391 passed in 0.86s. Nine temporary fault probes: 9 passed in 0.44s. I assessed recorded phase sums; did not rerun timings or the full suite.
- **Residual risk:** only scoped speed is measured. The changed SHA differs from `gate_manifest.json:7817`; the frozen-file ceremony remains due at the authorized cut or request.
- **Mutation:** control 391 passed; lens 4 deletion, wrapped pointer deletion and unknown placeholder, once per profile: 9 total, 9 killed, no survivors or measured equivalents.

**Covered:** claims/drift (`e270902d`, verification record); production path/design (`test_review_sweep_ships.py:318-440`); fail-closed (nine faults); cross-document/lifecycle (`protected_test_roster.json:493`, `gate_manifest.json:7817`); domain scope/satisfier (one-line diff). **Not covered / low confidence:** whole-suite speed, certification, repin, re-anchor and anchor comparison.

## Dispositions -- archive preparation -- 2026-10-30

Dispositions: none. The accepted implementation scope, mapped checks and review findings are closed. Full-tree certification and the frozen-file ceremony are separate authorized ceremonies, not per-plan archive prerequisites; the exact frozen test is carried in the v0.6 forward-baseline row in `dev/PLANNING.md`. No other follow-up remains open.

**Evidence shipped**: session-scope fixture edit (`e270902d`); repeated scoped timing reports, consumer inventory and nine installed-copy fault outcomes in `dev/plans/archive/2026-10-30-certification-cost-audit/`; final 391-node selections, frozen-file refusal and standing-gate evidence in the implementation verification record; Internal plan review (`450dd0d1`) and accepted code review (`71290cf1`). The `test_review_sweep_ships.py` nodes remain intact.

**Evidence deferred**: none of the plan-mapped evidence. Full-tree certification and the frozen-file ceremony were not run as part of this plan; they remain separate release/baseline ceremonies.

**Deferred evidence home**: `dev/PLANNING.md` > “Establish the v0.6 forward baseline” and “Earlier frozen-test changes.” The changed test file is explicitly listed there for the shared baseline ceremony; this plan creates no per-plan repin or re-anchor prerequisite.

**Fidelity sign-off**: implementation commit `e270902db03f54a5936269c198ccd706434dd5c4` matches the accepted proposal’s `## Current contract`, accepted as revised at Decision commit `3b675bb00ca15dadf6cd304e012a5bab7e9bef03`. It changes only `installs` to session scope, retains every existing node and the real separate profile installations, and meets the measured setup-reduction and fault criteria. No accepted outcome was removed.
