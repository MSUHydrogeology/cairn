# Judicious testing and simulation verification for scientific software teams

**Author**: Antigravity (Strategy)
**Model**: Gemini 4 Argon
**Date**: 2026-10-27
**Status**: draft
**Type**: product-strategy
**Surfaces this would feed**: [`dev/PLANNING.md`](../PLANNING.md) v0.6 candidates; [`AGENTS.md`](../../AGENTS.md); [`dev/agent_collaboration.md`](../agent_collaboration.md); [`tools/gauge.py`](../../tools/gauge.py); GitHub Issue #19.

## Summary

Any program admits an infinite number of tests, yet only a small fraction provide diagnostic value. Because most scientists-as-developers are never taught formal test-selection theory, AI coding agents easily push scientific repositories from historical under-testing into **profligate over-testing**: generating thousands of lines of repetitive examples and brittle "change-detector" tests that lock in internal implementation details without verifying physical invariants. Meanwhile, standard unit-testing habits fail on **simulation models**, where a single forward run can take minutes to hours.

Cairn must model and teach **judicious testing**:
1. **Control test volume via equivalence partitioning and subsumption:** One test per physical/logical regime and boundary, expressed as rows in a shared regime table or as a universal conservation/algebraic property—never a new test file per plan chunk.
2. **Separate verification by execution timescale for simulation models:** Shrink the spatial/temporal domain (the **micro-grid principle**) rather than mocking physics for sub-second checks, gate meso-scale analytical benchmarks to solver changes, and keep full-domain simulations outside the unit-test runner as milestone certification runs.
3. **Practice what we preach on Cairn's own suite:** On `0.5-dev` (`2026-10-27`), Cairn carries **87,197 lines of test Python** across 141 files against **31,124 lines of product Python** (**2.80× ratio**). In v0.6, unfreezing non-security tests and consolidating dominated plan-fragment tests should bring Cairn's ratio below **1.50×**.

---

## The question / felt gap

The Maintainer raised two linked concerns (`2026-10-27`):
1. **Test volume grows much faster than product code.** Although an infinite number of tests can be written, very few have real utility; Cairn needs a theoretical and operational control so agents write high-signal, minimal test suites.
2. **Scientists-as-developers rarely know formal testing theory—and simulation models have long execution times.** Standard unit-test patterns either bog down on multi-minute runs or mock out the physics so nothing real is verified. Cairn must model judicious practice.

## Method *(grounded, falsifiable — verify-before-asserting)*

* **Measured Cairn's repository (`2026-10-27` on `0.5-dev`):** Counted Python files, lines, and `def test_*` functions across [`bootstrap/tests/`](../../bootstrap/tests), [`bootstrap/_scaffold/`](../../bootstrap/_scaffold), [`scripts/`](../../scripts), [`tools/`](../../tools), and [`templates/`](../../templates).
* **Grounded in established testing and V&V theory:**
  * *Equivalence partitioning & boundary value analysis* (Goodenough & Gerhart 1975; Myers 1979; Weyuker & Ostrand 1980).
  * *Test suite minimization as submodular minimum set cover* (Harrold, Gupta & Soffa 1993; Rothermel et al. 1998).
  * *The Coupling Effect & dynamic mutant subsumption* (DeMillo, Lipton & Sayward 1978; Kurtz et al. 2014).
  * *Property-based & metamorphic testing* (Claessen & Hughes 2000; Chen et al. 1998).
  * *Scientific Verification & Validation (V&V)* (Oberkampf & Roy 2010; ASME V&V 10/20).
* **What would falsify this direction:** If pruning dominated tests in Cairn lets regressions slip past Boundary B, or if micro-grid tests in adopting simulation models fail to catch conservation/discretization bugs that full-grid runs catch.

---

## Findings

### 1. Why Cairn's own test suite reached 2.80× product size (measured)

On `0.5-dev` (`2026-10-27`), Cairn's Python codebase breaks down as follows:
* **Product Python** (`bootstrap/_scaffold/`, `bootstrap/scaffold.py`, `bootstrap/security_check.py`, `scripts/`, `tools/`): **47 files, 31,124 lines** (plus 31 template twin files at 20,087 lines).
* **Test Python** (`bootstrap/tests/`): **141 files, 87,197 lines, 3,384 `def test_*` functions** (**2.80×** product lines):
  * **Security, gate manifest & trust ceremony:** 46 files, **43,063 lines (49.4%)** (`test_gate_preflight.py` alone is 5,577 lines).
  * **CLI & coordination tools:** 58 files, **24,408 lines (28.0%)** (`test_board_json_contract.py` is 2,293 lines for 25 test functions—92 lines per test).
  * **Installer, upgrader & scaffold:** 19 files, **13,164 lines (15.1%)**.
  * **Prose, rule & doc regex pinning:** 18 files, **6,562 lines (7.5%)**.

**The structural ratchet:** [`bootstrap/tests/_gate_manifest.py`](../../bootstrap/tests/_gate_manifest.py) froze all existing test files (`FROZEN-MODIFIED` blocked the gate) while allowing brand-new test files (`FROZEN-NEW`). Agents were structurally penalized for adding a 1-line row to an existing test table and rewarded for creating a brand-new 500-line test file (repeating 60 lines of scratch-repo setup) for every plan.

### 2. Translating test-selection theory into plain scientific terms

Information gain per test is **strictly submodular**: once the distinct regimes and boundaries of a function are covered, more examples inside the same regime contribute **zero bits of diagnostic information** while adding permanent maintenance drag.

| Testing Theory Concept | Plain Scientific Equivalent | Judicious Practice (What to Write) | Profligate Anti-Pattern (What to Refuse) |
|---|---|---|---|
| **Equivalence Partitioning** *(Myers 1979)* | **Physical / Logical Regimes** *(laminar vs. turbulent; dry vs. ponded cell; valid vs. malformed input)* | **One test row per distinct regime** in a parameterized table. | Writing 15 separate test functions inside the same regime with arbitrary numbers. |
| **Boundary Value Analysis** | **Boundary & Initial Conditions** *(zero flux, saturation threshold, empty file)* | Test exact regime transitions (`0`, `N`, `ε`, sign flip). | Picking arbitrary interior constants (`42`, `100`) with no boundary meaning. |
| **Property & Metamorphic Testing** *(Claessen 2000; Chen 1998)* | **Conservation Laws, Symmetry & Analytical Limits** | Assert universal invariants (mass balance $= 0$, dimensional scaling, `parse(dump(x)) == x`). | Hardcoding giant "golden" output arrays from whatever the code printed today. |
| **Mutant Subsumption & Set Cover** *(Harrold 1993; Kurtz 2014)* | **Minimal Orthogonal Basis** *(dominated tests)* | Add a test only if it kills a plausible fault no existing test catches—by extending an existing table. | Creating a new `test_<plan_slug>.py` file with duplicated setup for every bug fix. |
| **Contract vs. Change-Detector** *(Google SWE 2020)* | **Observable Output vs. Scratch Derivation** | Test public contracts and invariants so internals can be refactored freely. | Pinning private helper names, call counts, or exact English sentences in Markdown docs. |

### 3. The three verification timescales for simulation models

In simulation software (groundwater, land-surface, CFD, multiphysics), forward runs take minutes to hours. Agents must separate verification into **three execution timescales** rather than treating every check as a unit test:

1. **Tier 1 — Sub-Second Kernel & Micro-Grid Invariants (`< 100 ms` per test; Boundary A & B):**
   * **Rule: Shrink the domain, never mock the physics.** If a 3D simulation model has a mass-balance bug, sign error, or boundary-flux defect, it will show up on a **1D 5-cell column or 3×3×2 synthetic micro-grid** running for 3 timesteps in memory in 10 milliseconds. Mocking numerical arrays with fake numbers hides real physics bugs; running a 10-million-cell basin in `pytest` kills iteration.
2. **Tier 2 — Meso-Scale Analytical & Convergence Benchmarks (`1 s – 2 min`; Scoped Boundary B):**
   * Closed-form benchmarks (e.g., Theis drawdown, 1D advection-dispersion) and **Method of Manufactured Solutions (MMS)** grid-refinement checks ($\Delta x \to \Delta x / 2$ verifying convergence order).
   * Assert **physical and numerical tolerances** ($\|e\|_{L_2} \le \tau$, mass closure $< 10^{-12}$), not bit-exact arrays that break across CPU architectures or thread counts. Run only when solver or physics surfaces change.
3. **Tier 3 — Full-Scale Production & Watershed Simulations (`minutes to hours+`; Certifying / Milestone runs):**
   * Real-domain transient runs, calibration sweeps, or HPC jobs. **Never collected by default `pytest`.**
   * Executed as milestone certification runs or under the **Independent Scientific Check**, recording a compact provenance summary (commit SHA, runtime, mass-balance closure, key metric norms) in git rather than raw output rasters.

---

## Options

1. **Do nothing:** Rely on the single sentence in [`AGENTS.md`](../../AGENTS.md) (*"A test pins a property in one node"*). *Fails:* Cairn's suite stays at 2.80× product size and adopters get no guidance for simulation models.
2. **Consolidate Cairn's test suite only:** Prune Cairn's tests in v0.6 without shipping adopter guidance. *Incomplete:* Misses the chance to help scientists-as-developers solve their biggest AI-testing blind spot.
3. **Model and ship Judicious Scientific Testing in v0.6 (Recommended):** Pair Cairn's own test-suite consolidation with concise, shipped testing and simulation-verification doctrine for adopters.

---

## Recommendation

Queue two linked deliverables under `v0.6 (Candidate directions)` in [`dev/PLANNING.md`](../PLANNING.md):

1. **Cairn Test-Suite Consolidation (Practice What We Preach):**
   * Once non-security tests are unfrozen (**Nimbleness 3**), forbid plan-named test files (`test_<plan_slug>.py`); organize [`bootstrap/tests/`](../../bootstrap/tests) by product module using shared `conftest.py` fixtures and `@pytest.mark.parametrize` regime tables.
   * Replace the 6,562 lines of change-detector prose regex tests with [`scripts/claim_check.py`](../../scripts/claim_check.py) and [`scripts/link_check.py`](../../scripts/link_check.py), and prune dominated tests to bring Cairn's test-to-product ratio from **2.80× down to ≤ 1.50×**.
   * Add **test-to-product ratio** and **test-growth delta** to `tools/gauge.py --pulse`.
2. **Shipped Judicious Testing & Simulation Verification Guidance (For Adopters):**
   * Update [`AGENTS.md`](../../AGENTS.md) and the **Correctness / Verification review lens** in [`dev/agent_collaboration.md`](../agent_collaboration.md) so reviewers flag **profligate, dominated, or change-detector tests** and **full-grid simulations inside unit-test loops** as defects.
   * Ship a concise guide teaching the **Regime & Boundary Table pattern**, the **Micro-Grid Principle** (*shrink the domain, never mock the physics*), and the **Three Verification Timescales** (linking to Issue #19's `deliverable` axis).

## Open questions

* **Target test-to-product ceiling for Cairn:** Is `≤ 1.50×` (~45k test lines vs. 31k product lines) the right v0.6 target once the 43k lines of gate-ceremony self-tests are consolidated?
* **Marker convention for Tier 2 benchmarks:** Should Cairn's templates recommend a standard `pytest` marker (`-m "not slow"` or `-m benchmark`) for Tier 2 analytical benchmarks in adopting repositories?
