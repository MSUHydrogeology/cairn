<!-- claim-check-allow: tools/test_tiers.json -->
# Module: testing-discipline

**Selected when:** the project carries automated tests (or intends to)
and wants a coherent **test-tier scheme** rather than an undifferentiated
`tests/` pile. Broadly applicable; team-gated so a preset
(`governance presets`) turns it on for the profiles that warrant it
rather than every adoption paying for it by default.

**Adds to:** a test-doctrine note in the adopting repo's `tests/` guide
(and a cross-reference from `dev/agent_collaboration.md`), plus the optional
standard-library Python report `scripts/test_coupling.py`.

This module gives the suite a shape, a way to choose tests, and a budget. The guidance below is a practical summary, not a complete testing curriculum.

## Template content

Merged into the project's `tests/` guide:

> **Test tiers are a single coherent scheme.** Tests live in named tiers
> -- e.g. **unit** (pure logic, synthetic inputs), **contract** (a stable
> schema / API boundary pinned against drift), **integration**
> (multi-component dataflow), **workflow** (end-to-end against a small
> fixture), and any project-specific tiers (security, notebook,
> benchmark, ...). A tier communicates broad scope; the test name and
> assertions show its specific behavior.
>
> **The tier is a property of location, not a hand-applied label.** A
> test's tier is determined by where it lives (its directory, or a
> per-tier configuration that maps file names to tiers), applied
> automatically -- authors do not hand-tag each test, and a check fails
> when a test has no tier, so the scheme cannot rot.
>
> **Choose tests by regime and boundary.** Divide the input space into
> regimes that should behave alike (valid and malformed input; dry and
> saturated cell; laminar and turbulent flow) and test each regime once,
> plus the transitions between them (zero, empty, one, the threshold, a
> sign change). More examples inside a regime rarely find new faults.
> This is a selection heuristic, not a guarantee: keep extra cases where a
> regime is poorly understood.
>
> **Prefer properties to snapshots.** Assert what must always hold --
> conservation, symmetry, a round trip (`load(save(x)) == x`), a known
> limit -- rather than freezing whatever the code printed today. A golden
> output is a change detector: it fails on every harmless change and
> says nothing about whether the result is right.
>
> Property-based input exploration is optional: sample or generate varied
> cases to probe a stated invariant. No input generator or dependency is
> required.
>
> **Test promises, not wording or internals.** The unit is a component's
> caller-visible promise: what it does, what it refuses, and the formats it
> reads and writes. Test it through the public entry point, in-process where
> practical. Put the component's short promise list in the test file's module
> docstring: a `Promises:` line followed by one or more `- ` lines. A behavior-
> preserving refactor should change no test. A test that fails despite unchanged
> promised behavior is a pin. Protect instructional prose through exact edits
> and review of changed or removed rules. Do not freeze its wording or key
> terms in tests.
>
> **Developmental tests are scratch work; permanent tests guard promises.** A
> test written while building or debugging one change is temporary scaffolding:
> run it in scratch space, record its result in the work record, and delete it
> before merge or archive. A permanent test enters `tests/` only when it checks
> a listed external promise through a public entry point. Run each new test once on a clean checkout before keeping it, so it does not depend on state only your machine has. Before adding a test
> that differs from a neighbor only in an input value, confirm the production
> code actually branches on that difference; if a passthrough field or one
> uniform guard handles all disallowed values, one test covers it. Never add a
> test file per plan, per bug or per review finding.
>
> **A surviving mutant is a question.** If it changes promised behavior, the
> promise test is missing or weak, so strengthen that test. If callers cannot
> observe it, ask whether the code is needed. Never add a test that pins the
> mutated line.
>
> **Refusals are promises too.** Cover hostile inputs as one parameterized test
> per refusal promise, rather than a separate test per function and attack
> spelling. Hostile state is caller-visible when it changes the public result
> or refusal; a race or swapped link can break that promise too. If a
> test must inject hostile state through an internal hook, declare the
> exception in the test file and keep it. Direct tests of internal algorithms
> likewise need a one-line reason beside the test, such as when the public entry
> point is too coarse to reach the algorithm core.
>
> Investigate surviving mutations against independently confirmed expectations,
> not candidate output; no per-function or set-wide mutation quota is implied.
> Human confirmation remains for reported faults, not every discarded candidate
> or ordinary change.
>
> Do not weaken assertions, tolerances, inputs, expectations, mocks or logic
> merely to make a failed check pass. If an expected value or assertion changes,
> state the promise being changed and the independent basis for that change.
>
> **Contract tests pin stable schemas.** A boundary the project promises
> not to break silently (a config schema, a public API shape, a
> serialized format) gets a **contract test** that fails when the shape
> changes -- the change then has to be deliberate.
>
> **Negative tests prove the guards.** A validation or safety guard is
> tested by feeding it *bad* input and asserting it **fails loudly**
> (raises / rejects), not only by confirming the happy path. A guard with
> no negative test is an unproven guard.
>
> **The suite has a time budget and an owner.** The project names who owns the ordinary run's time, sets how long it may take, and measures it. Review the slowest test files on a stated schedule, such as each release.
>
> **Apply the Pareto testing principle (80/20).** Aim for the 20% of tests that
> catch 80% or more of real caller-visible failures (primary workflows,
> scientific or data invariants, and one parameterized check per refusal class)
> within the runtime budget. Delete private-helper tests, change-specific pins,
> wording pins and same-branch permutations directly once the component's
> listed promises have a passing public-entry check; no per-test mutant-
> equivalence proof is required. A size ratio is a diagnostic, never a deletion
> quota. A test that is not clearly a public promise is not kept; a higher-tier agent decides each judgment call. These are exempt and are cut only through a Security Review: tests of the surfaces your project's `AGENTS.md` names as high-risk, tests your project's release or security records name as guards, and refusal, hostile-state and negative-guard tests.



> **Advisory report.** Run `python scripts/test_coupling.py` to see private
> reach and missing promise lists, worst first. The report names its Python-
> only gap and says refusal and hostile-state tests stay. It is a review prompt,
> not a deletion list. `--strict` makes any reported gap or scan failure exit
> nonzero; the default is advisory and exits zero.
>
> **Use public entry points and fresh state.** Exercise the public command or
> API when practical. Reuse immutable descriptions or builders, and create
> fresh paths and mutable repositories for each case.
>
> **Choose change checks from affected behavior.** Start with the component
> owner and the project's existing test homes. Trace changed behavior through
> callers, imports, configuration and data readers, and public entry points;
> map existing checks to affected components and consumers. Unit checks cover
> local behavior, contract checks cover public interfaces and data formats,
> integration checks cover connected components, and a small workflow exercises
> the real entry point. Local changes default to affected checks. Shared
> contracts, common infrastructure, language seams, solver or physics behavior,
> and uncertain dependencies widen to owning families and relevant consumers.
> Add or extend a test only for a plausible uncovered fault. If dependencies
> cannot be bounded, state the uncertainty and smallest useful remedy. A large project is not one piece: test each part where it lives. A change may be verified from current results in place of a whole-suite run; a release's own whole-suite and security-family run is never replaced by earlier results, and a release may reuse results only where a reviewed rule allows it. Agents map
> routine coverage and reviewers challenge it; project leads set high-level
> needs and material exceptions.
>
> **Simulation models verify at three timescales.** Where one model run
> takes minutes or hours:
> 1. **Fast checks** shrink the domain rather than mocking the physics: a
>    few cells and a few time steps exercise the real equations in
>    milliseconds. Many sign, flux and mass-balance errors show up here,
>    though not ones that need scale, long accumulation or parallel runs.
> 2. **Benchmarks** compare against analytical solutions, manufactured
>    solutions or a convergence study, within stated tolerances rather
>    than bit-exact arrays. Run them when the solver or physics changes.
> 3. **Full runs** stay outside the ordinary test run. Record a short
>    summary (commit, runtime, mass-balance closure, key error norms) as
>    milestone evidence, not the raw output.
>
> **A passing check supports only the property it actually tests.** Conservation
> or closure can hold for a wrong result, and convergence can occur for the
> wrong equation. State independently grounded expected behavior before
> results, with its source, units, tolerance and limits. Characterization
> records established behavior and its source; it does not establish physical
> validity. Candidate-derived values are not independent evidence. Analytical,
> manufactured or observational comparisons support claims only within the
> domain and assumptions they cover; no selected check proves general
> correctness or scientific validity.
>
> **Observe the failure first.** Observe a new check fail before fixing behavior; fix the behavior, not the expected value.
>
> **A change records which tier(s) it touched.** The implement-with-tests
> step names the tier a new test lands in, so the suite's shape stays
> legible as it grows.

## Relationship to `dual-language-tests`

This module is the **base** test-tier discipline. The team-gated
`dual-language-tests` module is a
**specialization on the Language axis**: it keeps this tier scheme but
adds cross-language seam structure (each language keeps its framework; a
tier means the same thing across languages; the seam where one language
calls another is a named, tested surface). They are orthogonal -- tiering
vs. cross-language seams -- so a multi-language project selects **both**:
`testing-discipline` for the scheme, `dual-language-tests` for the seams.

## Learn it deeply

The tier scheme and the selection rules above are Cairn's summary of
established testing practice: equivalence partitioning and boundary
values, property-based and metamorphic testing, and verification and
validation for scientific computing. See Cairn's own
[cairn/docs/further-reading.md] > "Software quality for scientists" for
the pointer Cairn relies on rather than re-teaching.
