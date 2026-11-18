# Module: testing-discipline

**Selected when:** the project carries automated tests (or intends to)
and wants a coherent **test-tier scheme**.

**Adds to:** a test-doctrine note in the adopting repo's `tests/` guide
(and a cross-reference from `dev/agent_collaboration.md`), plus the optional
standard-library Python report `dev/tools/test_coupling.py`.

This module gives the suite a shape, a way to choose tests, and a budget. The
guidance below is a practical summary, not a complete testing curriculum.

## Template content

Merged into the project's `tests/` guide:

> **Test tiers are a single coherent scheme.** Use named unit (pure logic, synthetic
> inputs), contract (stable boundary), integration (multi-component dataflow),
> workflow (end-to-end small fixture) and project-specific tiers.
>
> **The tier is a property of location, not a hand-applied label.** A test's tier
> comes from where it lives (its directory, or a per-tier configuration that maps
> file names to tiers), not from hand-tagging, and a check fails when a test has no
> tier.
>
> **Choose tests by regime and boundary.** Test each input regime and its
> transitions once. This heuristic is not a guarantee; keep extra cases where a
> regime is poorly understood.
>
> **Prefer properties to snapshots.** Assert invariants such as conservation or
> round trips. Input exploration is optional; no generator or dependency is
> required.
>
> **Test promises, not wording or internals.** A caller-visible promise covers
> behavior, refusals and formats. Test it through the public entry point, in-
> process where practical. Put a `Promises:` line and one or more `- ` lines in
> the test file's module docstring. A behavior-preserving refactor should change
> no test; failure despite unchanged behavior is a pin. Protect instructional
> prose by exact edits and review, not tests freezing wording or key terms.
> For a reader of an external tool's output, commit the tool's first real output
> as the fixture: keep it small and free of private data. Until then, the test
> says its fixture is unverified.
>
> **Developmental tests are scratch work; permanent tests guard promises.** Run
> debugging tests in scratch, record results and delete them before merge or
> archive. Keep a test only for a listed external promise through a public entry
> point; run each new test once on a clean checkout. Before adding an input
> variation, confirm production branches differently; one uniform guard or
> passthrough needs one test. Never add a test file per plan, bug or review
> finding.
>
> **A surviving mutant is a question.** If it changes promised behavior, strengthen
> the promise test; if unobservable, ask whether the code is needed. Never pin the
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
> Investigate surviving mutations against independent expectations, not candidate
> output; no per-function or set-wide quota applies. Humans confirm reported
> faults, not every discarded candidate or ordinary change.
>
> Do not weaken assertions, tolerances, inputs, expectations, mocks or logic
> merely to make a failed check pass. If an expected value or assertion changes,
> state the promise being changed and the independent basis for that change.
>
> **Contract tests pin stable schemas.** A boundary the project promises
> not to break silently (a config schema, a public API shape, a
> serialized format) gets a **contract test** that fails when the shape
> changes.
>
> **Negative tests prove the guards.** A validation or safety guard is
> tested by feeding it *bad* input and asserting it **fails loudly**
> (raises / rejects), not only by confirming the happy path. A guard with
> no negative test is an unproven guard.
>
> **The suite has a time budget and an owner.** The project names who owns the
> ordinary run's time, sets how long it may take, and measures it. Review the slowest
> test files on a stated schedule, such as each release.
>
> **Apply the Pareto testing principle (80/20).** Aim for the 20% of tests that
> catch 80% or more of real caller-visible failures (primary workflows,
> scientific or data invariants, and one parameterized check per refusal class)
> within the runtime budget. Delete private-helper tests, change-specific pins,
> wording pins and same-branch permutations directly once the component's
> listed promises have a passing public-entry check; no per-test mutant-
> equivalence proof is required. A size ratio is a diagnostic, never a deletion
> quota. A test that is not clearly a public promise is not kept; a higher-tier agent
> decides each judgment call. These are exempt and are cut only through a Security
> Review: tests of the surfaces your project's `AGENTS.md` names as high-risk,
> tests your project's release or security records name as guards, and refusal,
> hostile-state and negative-guard tests.
>
> **Advisory report.** `python dev/tools/test_coupling.py` reports private reach and
> missing promise lists worst first. It names its Python-only gap, keeps refusal
> and hostile-state tests, and is a review prompt, not a deletion list. `--strict`
> exits nonzero for a gap or scan failure; default is advisory and exits zero.
>
> **Use public entry points and fresh state.** Reuse immutable descriptions or
> builders, and create fresh paths and mutable repositories for each case. Shared
> immutable setup may use session scope when shuffled tests interleave modules;
> mutable projects, refs, keys, paths, and monkeypatches stay per-test.
>
> **Choose change checks from affected behavior.** Trace changes through owners,
> existing test homes, callers, imports, configuration, data readers and public
> entries; map checks to affected components and consumers. Local changes use
> affected checks; shared contracts, infrastructure, language seams, solver or
> physics changes and uncertain dependencies widen to owners and consumers. Add
> tests only for plausible uncovered faults. If dependencies cannot be bounded,
> state the uncertainty and smallest useful remedy. Test each part of a large
> project where it lives. Current results may verify a change; a release never
> replaces its own whole-suite and security-family run, and may reuse results only
> under a reviewed rule.
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
> 3. **Full runs** answer a question about the model and are not tests. They
>    stay outside the ordinary test run unless configured there. A full run
>    named by a plan is taken at the end of the cycle unless the plan, proposal
>    or release names other points. Record a short summary (commit, runtime,
>    mass-balance closure, key error norms) as milestone evidence, not raw output.
>
> **Stage output first.** Compare the output of the change's own stage with its
> accepted copy. This suffices when the output should not change, or changes
> only as the plan predicted; later stages need not run just to be sure. It
> replaces no configured or named run or required check.
>
> **One reference, one control.** For a before-and-after comparison, use the
> commit immediately before the change as the control; an older run is only a
> cross-check. Keep one accepted reference run per model and mode in the run
> log, with its commit and settings. Before the runs, the Maintainer accepts
> the reference and sets pass bands. An agent may build a candidate and report
> against the bands, but may neither accept a reference nor widen a band.
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
> **Observe the failure first.** Observe a new check fail before fixing behavior;
> fix the behavior, not the expected value.
>
> **A change records which tier(s) it touched.** The implement-with-tests
> step names the tier a new test lands in.

## Learn it deeply

These rules summarize established practice: equivalence partitioning and boundary
values, property-based and metamorphic testing, and verification and
validation for scientific computing. See Cairn's own
[cairn/docs/further-reading.md] > "Software quality for scientists".
