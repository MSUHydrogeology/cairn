# Consolidate the suite without losing fault detection

**Author**: Codex (runtime model identifier unavailable; Strategy)
**Status**: awaiting-review
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
