# Consolidate the suite without losing fault detection

**Author**: Codex (runtime model identifier unavailable; Strategy)
**Status**: revising
**Review**: usual + Security Review
**Proposed tier**: heavy -- protected tests and collection contracts
**Plan review**: required(Internal + Internal Security Review)
**Opened**: 2026-11-02
**In brief**: Reduce repeated test setup and redundant cases, organize ordinary tests by tier, and preserve the faults and security checks the suite detects.

## Decision summary

Cairn spends too much time preparing similar test environments. Consolidate
that work before adding parallel execution. Keep the behaviors being checked,
including hostile-input refusals, and account explicitly for any moved or
removed test. This is substantial test-maintenance work, not a smaller-suite
quota or permission to weaken release checks.

## Context

The v0.7 board prioritizes consolidation and records historical full-run and
recent per-file timings; they are not a new benchmark from this proposal.
At `4d29b2ef`, `tools/test_tiers.py` already classifies tests recursively.
`bootstrap/tests/test_gate_preflight.py` repeatedly builds mutable Git
repositories through `_repo` and `_closure_repo`; those cases cannot safely
share one writable repository.

The [testing strategy](../strategy/2026-10-27-antigravity-judicious-testing-and-simulation-verification.md)
and the completed
[fixture optimization](../plans/archive/2026-10-30-certification-cost-audit.md)
provide the starting design. No suite was run to author this proposal.

## Proposal

1. **Consolidate expensive families first.** Use existing timing records and
   scoped duration reports to rank work. Separate setup cost from assertion
   time. Start with preflight/ceremony and upgrade families already named on
   the board, rather than inventing another profiler.

2. **Reuse preparation, not mutable state.** Share immutable descriptions,
   source snapshots and builders where safe. Give each mutating scenario its
   own paths, repository, environment and teardown. Consolidate repeated
   setup through existing family helpers before introducing a cross-suite
   framework. Parameterize genuine input regimes, not every word or file.

3. **Keep detection accountable.** Before removing or combining a case, map
   its assertions and plausible faults to retained checks in the plan's
   existing verification record. Keep distinct public-entry-point,
   malformed-input, permission, cleanup and security refusal cases.
   A matching test count or green replacement suite is not equivalence.
   Reusable fault probes belong in owning tests, not a new ledger.

4. **Make tier locations legible.** After the v0.6 baseline is installed,
   move ordinary tests into tier folders in reviewed batches. Keep protected
   apparatus at its approved paths unless a separate authorized transition
   changes them. Update the existing tier map, imports, collection consumers
   and explicit commands together. Record old-to-new node identities; a path
   move must not hide a lost check or silently change protection.

5. **Measure the improvement once.** Compare scoped setup/call durations on
   before/after committed snapshots under the same interpreter and conditions.
   Measure the full-run ten-minute target at an already authorized
   certification point, not in every iteration. Keep its commands, triggers,
   security outcomes and configured members unchanged. Report misses honestly.
   Add suite growth/runtime summaries to the shared pulse reporting owned by
   the [accepted meter](2026-10-30-claude-metered-cost.md), not another store.

No parallel runner is introduced here. Any later parallelization must resolve
its isolation and security prerequisites independently.

## Rationale

The up-front cost is inspecting assertions, restructuring fixtures and
reviewing collection changes. The expected recurring benefit is less setup,
shorter feedback and fewer fragile near-copies. Maintenance stays in existing
test families and the tier map; no new service or mandatory reporting form.

## Alternatives considered

Doing nothing retains the measured pain. Narrower iteration selection already
exists but does not reduce certification setup. Parallelizing first adds
scheduling and isolation risk while retaining duplicated work; reconsider only
after consolidation is measured.

## Documentation / doctrine surface

Update the existing test guide, tier configuration and affected references.
Preserve the published verification contract. Protected changes retain the
procedures in `bootstrap/REANCHOR_RUNBOOK.md`; this proposal authorizes no
ceremony or baseline installation.

## Evidence / verification plan

### Tests required

The plan maps affected families and their consumers. Preserve
`bootstrap/tests/test_test_tiers.py`, including recursive discovery and
changed-test selection, and `bootstrap/tests/test_gate_manifest.py` coverage
for dropped protected nodes, ordinary deltas and skip markers. Exercise real
CLI/install/upgrade paths where the removed cases did.

Use collection-only checks to compare membership. Challenge each distinct
fault claimed preserved with targeted negative controls or existing failing
inputs; report unresolved coverage, not a giant per-token mutation inventory.

### Examples / smoke checks

Run tier-map validation and scoped duration reports; use claim/link and
neutrality/redundancy gates for changed guidance. An authorized final
certification supplies full-tree performance evidence. No extra full suite
is authorized by writing or reviewing this proposal.

#### Security preflight

S1: collection and fixture inputs come from the candidate; expected
protection comes from approved authority and the pre-change checks, not a
candidate-generated replacement roster.
S2: a lost protected node or weakened refusal must fail its owning check.
These implementation mutations have not been run during authoring.
S3: scoped pytest and existing gate commands exercise the changed families.
Proposed guidance: "Consolidation preserves required fault detection and
release checks."
S4: missing mapped evidence keeps work open; speed never converts a failure
or skip into a pass.
S5: colluding authors can misstate equivalence; independent review and
Maintainer-controlled protection remain necessary.

### Independent scientific check

N/A: no scientific equation, parameter or published result changes.
Existing required scientific checks remain required.

## Signals the change is wrong

Failures appear only under ordering/concurrency, a removed fault has no
retained check, new helpers cost more than duplicated setup, or timing improves
only through deselection. Missing the runtime target is reported, not concealed.

## Scope delta

**Scope delta**: preserved -- consolidation, tier folders, detection retention
and shared growth reporting remain outcomes.

## Assurance path

**Assurance path**: high-assurance -- protected tests and collection behavior.

## Review -- Codex (fresh-context usual reviewer) -- 2026-11-02

**Model**: inherited Codex runtime; exact identifier unavailable; no downshift.
**Reviewed commit**: `9d5a69e524a2ab3a749b386dd67efe2861f2ecf0`
**Tier**: usual
**Target**: opening proposal. **Prior findings**: none.
**Assurance path**: high-assurance.

**Foundations**

1. **Should this happen as framed?** Yes: reduce preparation while retaining
   detecting checks. The repeated mutable repository builders substantiate
   the opportunity, not a measured speedup --
   `bootstrap/tests/test_gate_preflight.py`, `_repo` and `_closure_repo`.
2. **Best alternative.** Optimize existing family fixtures without moving
   files: less collection/import maintenance, but loses the board's legible
   tier-folder outcome and needs Maintainer scope disposition --
   `dev/PLANNING.md`, v0.7 suite row; `tools/test_tiers.py`, `find_test_files`.
3. **What would show it wrong?** A retained check misses a removed fault,
   sharing introduces order dependence, or savings come from deselection --
   Proposal 2-5; `bootstrap/tests/test_gate_manifest.py`,
   `test_verify_holds_on_dropped_node`.

**Verdict**: SHIP. **Findings**: one non-blocking improvement; no blockers.

1. **SC-1 -- Make order isolation an explicit experiment.** Tests required
   names membership and fault controls, but no alternate-order control for
   shared preparation. The prior audit found fixture lifetime mattered under
   interleaving (`dev/plans/archive/2026-10-30-certification-cost-audit.md`).
   Close by requiring fixed/alternate shuffle seeds on each affected sharing
   batch, with independent mutable paths and unchanged detection; use the
   existing `bootstrap/tests/conftest.py` shuffle option, not another suite run.

The folder moves, runtime target, detection accounting and shared pulse
reporting remain promised. The delivery-sequence retirement table keeps
runtime evidence open until delivered or explicitly dispositioned.

**Elapsed**: approximately 5 minutes, including shared source inspection.
**Tokens**: unknown.

**Covered**: board/source outcomes, builders, tier discovery, gate assertions,
prior audit and retirement ownership. **Not covered / low confidence**: no
tests, mutations, timings or implementation reruns; historical measurements
were read only. This pass does not discharge Security Review.

## Review -- Codex (independent Security Reviewer) -- 2026-11-02

**Model**: inherited Codex runtime; exact identifier unavailable; no downshift.
**Reviewed commit**: `9d5a69e524a2ab3a749b386dd67efe2861f2ecf0`
**Target**: opening proposal. **Prior findings**: none.
**Assurance path**: high-assurance. **Tier**: Security Review.

**Foundations**

1. **Should this happen as framed?** Yes: retain refusal behavior while
   reducing setup, with fresh mutable repositories and separately authorized
   protection changes -- Proposal 2-4;
   `bootstrap/tests/test_gate_preflight.py:45-83`.
2. **Best alternative.** Consolidate existing family fixtures first, without
   another runner --
   `dev/plans/archive/2026-10-30-certification-cost-audit.md`, Acceptance criteria.
3. **What would show it wrong?** A retained check misses an old fault, shared
   state changes outcomes, or protection changes silently -- Evidence;
   `bootstrap/tests/test_gate_manifest.py:158-242`.

**Verdict**: ACCEPT. **Findings**: one non-blocking improvement; no blockers.

1. **SC-S1 -- Make collection-time execution explicit.** The collection-only
   comparison uses machinery that imports candidate code
   (`bootstrap/tests/_gate_manifest.py:513-526`).
   `bootstrap/REANCHOR_RUNBOOK.md:20` explicitly denies containment; fresh paths
   are not host isolation. Close by carrying that residual into the prescribed
   collection procedure and retaining existing key-away/ceremony requirements.
   No new isolation framework is requested.

S1's independent protection source agrees with `_trusted_roster_from_anchor`;
ordinary deletions remain notes, not equivalent-detection evidence. Six
selected roster/tier checks passed within the combined eight-check scratch
run: Python 3.13.13, 0.26 seconds total. S2's future refusal mutations are
honestly unmeasured, not an unmet current prototype demonstration.

**Elapsed**: shared approximately six-minute review window; per-file split
unmeasured; recording approximately two minutes. **Tokens**: unknown.

**Covered**: S1-S5, fixture isolation, protection authority, collection and
detection preservation. **Not covered / low confidence**: future consolidation,
per-fault equivalence, ordering trials, performance or certification.
